#!/usr/bin/env python3
"""Phan chung bang kho bare that, kem bang dot bien tren ban sao tam."""
from __future__ import annotations
import ast
import builtins
import contextlib
import hashlib
import importlib.util
import io
import json
import math
import os
import secrets
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import types
import warnings
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TOOL = HERE / "nhanh_don_duoc.py"

# #593 r3 M1 — TAT bao tri git NEN o moi tien trinh git con, NOI THEM vao GIT_CONFIG_* (moi truong co the
# da mang credential git qua chinh co che nay — ghi de la mat no). gate-registry do master 4c53c76 (job
# 107949420933): `td.cleanup()` cua `kho_bare` gap ENOTEMPTY tren `remote.git`. Gia thuyet — KHONG DO DUOC
# tai cho (git 2.43 o day, 2.55 tren CI): `maintenance`/`gc --auto` tach nen sau push/fetch van ghi vao do.
GIT_TAT_BAO_TRI = (("gc.auto", "0"), ("gc.autoDetach", "false"), ("maintenance.auto", "false"),
                   ("maintenance.autoDetach", "false"), ("receive.autogc", "false"))
def _tat_bao_tri_git(env) -> None:
    # r3 vong 1 P2: git dung muc CUOI cua moi khoa (ten khoa khong phan biet hoa/thuong) — co cap tat
    # o truoc ma cap bat o sau thi van BAT. Nen xet GIA TRI HIEU LUC, khong xet su co mat cua cap.
    n = int(env.get("GIT_CONFIG_COUNT") or 0)
    cuoi = {}
    for i in range(n):
        cuoi[(env.get(f"GIT_CONFIG_KEY_{i}") or "").lower()] = env.get(f"GIT_CONFIG_VALUE_{i}")
    for k, v in GIT_TAT_BAO_TRI:
        if cuoi.get(k.lower()) != v:
            env[f"GIT_CONFIG_KEY_{n}"], env[f"GIT_CONFIG_VALUE_{n}"] = k, v
            n += 1
    env["GIT_CONFIG_COUNT"] = str(n)
    # r3 vong 2 P2: `GIT_CONFIG_PARAMETERS` (tu `git -c`) THANG cac muc dem so; co thi noi duoi cua ta vao CUOI.
    duoi = " ".join(f"'{k}'='{v}'" for k, v in GIT_TAT_BAO_TRI)
    tham = env.get("GIT_CONFIG_PARAMETERS") or ""
    if tham and not tham.endswith(duoi):
        env["GIT_CONFIG_PARAMETERS"] = f"{tham} {duoi}"
_tat_bao_tri_git(os.environ)
def _tat_bao_tri_kho_bare(remote: Path) -> None:
    # r3 CI 88afd8d van ENOTEMPTY: transport cuc bo GO GIT_CONFIG_COUNT/PARAMETERS khoi receive-pack (do: hook
    # pre-receive khong thay gc.auto). Nen ghi THANG vao config kho dich — ghi tep, KHONG phong tien trinh.
    with (remote / "config").open("a", encoding="utf-8", newline="\n") as f:
        f.write("".join(f"[{k.split('.')[0]}]\n\t{k.split('.')[1]} = {v}\n" for k, v in GIT_TAT_BAO_TRI))

# ---- M1: tin hieu "chot cua CHINH ca nay hong" -------------------------------
# Ma HA TANG (`run`, `nap_tool`, `chay_dot_bien`) nem `AssertionError` TRAN va
# KHONG bao gio nem lop nay. Nho vay bo cham phan biet duoc "dich chet dung chot"
# voi "mot ca chet vi loi vo can" — thu ma `AssertionError` tran KHONG phan biet
# duoc (da tra gia: CASE T4 chet vi `rc=128: git commit -m A`).
class _KhongBaoGioXayRa(Exception):
    """Chi de dot bien `bo-bat-loi-phong-con` thu HEP lop bat, khong ai nem."""


class TinHieuChotCa(AssertionError):
    pass


class TinHieuKhongDoDuoc(Exception):
    """#593 M2 — TIEN DE cua phep do khong dung duoc => KHONG DO DUOC.

    KHONG phai DAT, va KHONG phai "chot that bai". Ba trang thai chu khong hai:
    mot ca khong do duoc thi phai noi the, chu khong duoc lam tron len DAT (loi
    #401) cung khong duoc gia lam mot chot sai. No KHONG ke thua `TinHieuChotCa`
    nen `chay_tu_kiem` xep no vao DO_KHAC — do la lop DUNG: ca do vi mot le
    KHONG PHAI chot cua no. Nho M2 cua r1 va M6 cua r2, cha in nguyen thong diep
    nay ra chu khong chi ten ca.
    """


def chot(dieu_kien, ten_ca: str = "") -> None:
    if not dieu_kien:
        raise TinHieuChotCa(f"chot cua ca {ten_ca} that bai")


# ---- #593 r2 / M1+M2: SO LOI HA TANG dung chung -----------------------------
# Moi cho NUOT mot `OSError` thanh GIA TRI (KDD, `do`, `None`) GHI doi tuong vao
# day truoc; `chay_tu_kiem` (M3) doi nhan ca co muc moi. Song o `sys.modules` de ban
# goc va MOI ban sao `_nap_ban_sao` dung CHUNG mot so: ca long chay trong ban sao `m`.
_SO_HA_TANG = sys.modules.setdefault("_nhanh_don_duoc_so_ha_tang",
                                     types.ModuleType("_nhanh_don_duoc_so_ha_tang"))
_SO_HA_TANG.__dict__.setdefault("loi", [])
_SO_HA_TANG.__dict__.setdefault("tiem", [])


def _tiem(exc):
    """M2 — loi TIEM CO CHU Y: dang ky theo DOI TUONG, khong theo ten kich ban."""
    _SO_HA_TANG.tiem.append(exc)
    return exc


def _la_ha_tang_that(exc) -> bool:
    return isinstance(exc, OSError) and not any(exc is t for t in _SO_HA_TANG.tiem)


def _chuoi_that(exc) -> list:
    """OSError THAT tren chuoi `exc` -> `__cause__`/`__context__`, chong chu trinh."""
    ra, thay, e = [], set(), exc
    while e is not None and id(e) not in thay:
        thay.add(id(e))
        if _la_ha_tang_that(e):
            ra.append(e)
        e = e.__cause__ or e.__context__
    return ra


def _ghi_ha_tang(exc, truoc=None) -> None:
    """Ghi CA CHUOI. SO LAN = moi lan DIEM NUOT goi (`truoc=None`) cong MOI doi tuong ha tang tren
    chuoi, ke ca to tien da ghi; hop runner (`truoc`) chi them doi tuong CHUA co trong cua so ca.
    NO CO TEN `SO-LAN-THEO-DOI-TUONG-KHONG-THEO-SU-KIEN` (#593 vong 8-10, chu kho chon (b), mo rong):
    dem THIEU khi cung doi tuong phat sinh LAI trong cung ca; dem THUA khi nhieu loi moi chung mot
    to tien (3 su kien -> 4 muc). NHAN khong doi. Sua dung doi MA SU KIEN tai bien I/O —
    traceback KHONG dung duoc (vong 9 do: dem doi/thieu)."""
    for e in _chuoi_that(exc):
        if truoc is None or not any(e is x for x in _SO_HA_TANG.loi[truoc:]):
            _SO_HA_TANG.loi.append(e)


def _bo_cua(ds) -> None:
    """LOP HAI (vong 5 F2): fixture don DUNG doi tuong no giu, theo danh tinh — doc lap voi
    so dang ky (lop mot). Hai lop: hong MOT lop thi loi co y van khong lot ra runner."""
    _SO_HA_TANG.loi[:] = [e for e in _SO_HA_TANG.loi if not any(e is x for x in ds)]


@contextlib.contextmanager
def _vang_co_chu_y(m):
    """Con CO Y khong phat proof: chi nhan `FileNotFoundError` o DUNG duong proof ma `m.run`
    giao cho con qua env (vong 6 F1) — loi doc tep KHAC thoat nguyen trang, khong dang ky."""
    cua, doc, run_goc, proof = [], Path.read_text, m.run, set()

    def run_ghi(args, cwd, check=True, env=None):
        proof.add(Path((env or {}).get(TU_KIEM_FILE_ENV, "")))
        return run_goc(args, cwd, check=check, env=env)

    def doc_bat(self, *a, **k):
        try:
            return doc(self, *a, **k)
        except FileNotFoundError as e:
            if self in proof:
                cua.append(_tiem(e))
            raise
    m.run, Path.read_text = run_ghi, doc_bat
    try:
        yield cua
    finally:
        m.run, Path.read_text = run_goc, doc
        _bo_cua(cua)


def _tom_tat_ha_tang(ds) -> str:
    gom: dict[str, list] = {}
    for e in ds:
        gom.setdefault(type(e).__name__, [str(e), 0])[1] += 1
    return "; ".join(f"{ten}: {tho} ({so} lan)" for ten, (tho, so) in gom.items())


def _ha_tang_cua_ca(truoc: int, goc=None) -> None:
    """M3 — muc so MOI tu vi tri `truoc` (+ chuoi cua `goc`): co => KHONG DO DUOC, du ca DAT
    hay chot. Theo VI TRI, khong xoa so: runner LONG khong xoa bang chung cua ca NGOAI."""
    _ghi_ha_tang(goc, truoc)             # chuoi vao SO: runner NGOAI cung thay (vong 4 F1)
    ds = [e for e in _SO_HA_TANG.loi[truoc:] if _la_ha_tang_that(e)]   # loc CA luc doc (lop mot)
    if ds:
        khong_do = TinHieuKhongDoDuoc(f"tien de ha tang hong: {_tom_tat_ha_tang(ds)}")
        raise khong_do


# ---- M6 + M7: kenh ket qua rieng, va MO HINH TIN CAY cua no ------------------
# Lop ngoai le KHONG qua duoc ranh gioi tien trinh: bo cham goi tien trinh con roi
# doc CHUOI. Nen luot con phat ket qua ra mot KENH RIENG (tep JSONL), khong tron
# voi stdout cua ma dang bi thu.
KENH_ENV = "NHANH_DON_DUOC_KENH"
DAU_PHIEN_ENV = "NHANH_DON_DUOC_DAU_PHIEN"
MUTANT_ENV = "NHANH_DON_DUOC_MUTANT"
LAN_THU_ENV = "NHANH_DON_DUOC_LAN_THU"
NHAN_DAT, NHAN_DO_CHOT, NHAN_DO_KHAC = "DAT", "DO_CHOT", "DO_KHAC"
GIET, KHONG_GIET, KHONG_DO_DUOC = "GIET", "KHONG_GIET", "KHONG_DO_DUOC"


# #593 — TRAN lan rut lai. Voi khong gian 256 (tuc duoi dot bien
# `entropy-giu-mot-byte`) xac suat CA 64 lan deu trung la (1/256)^64, tuc 0 tren
# moi thang do thuc te. Voi khong gian 1 (bo sinh HANG) thi no CAN, va do la
# duong duy nhat toi `TinHieuKhongDoDuoc` — chan tren ton tai de khong bao gio
# co vong lap khong chan.
TRAN_RUT_DAU_PHIEN = 64


def _hai_dau_phien_phan_biet() -> tuple[str, str]:
    """#593 M1 — HAI dau phien KHAC NHAU, do duoc thay vi cau may.

    Benh: `r508` mo dau bang `sinh_dau_phien(), sinh_dau_phien()` roi dung ngay.
    Tinh phan biet ay la TIEN DE cua ca — ca do rang `doc_kenh` tra KHONG_DO_DUOC
    khi ban ghi mang dau phien KHAC — chu KHONG phai thu ca ay do. Duoi dot bien
    `entropy-giu-mot-byte` khong gian tut xuong 256, nen 1/256 luot hai lan rut
    TRUNG nhau; ban ghi hoa ra KHOP dau phien dang hoi, va `r508` chet vi mot le
    VO CAN. Dung hinh dang TIN DUNG GIA ma kho nay dat ten, lan nay NAM BEN
    TRONG mot ca test. Do 200 000 cap, hai luot: 0,3840% va 0,3615%; ly thuyet
    1/256 = 0,3906%. Hau qua: `gate-registry` — mot REQUIRED CHECK — do ~1/256
    luot tren MOI head, MOI nhanh.

    Chua bang cach bien tien de NGAM thanh tien de DO DUOC, ba trang thai.
    """
    dau = sinh_dau_phien()
    for _ in range(TRAN_RUT_DAU_PHIEN):
        khac = sinh_dau_phien()
        if khac != dau:
            return dau, khac
    raise TinHieuKhongDoDuoc(
        f"khong rut duoc HAI dau phien PHAN BIET sau {TRAN_RUT_DAU_PHIEN} lan — "
        "khong gian sinh qua hep, tien de cua r508 khong dung duoc")


def sinh_dau_phien() -> str:
    """Dau phien NGAU NHIEN, SINH MOI MOI LUOT.

    KHONG duoc lay moc thoi gian do phan giai giay: hai luot chay nhanh se trung.
    KHONG duoc lay bo dem tang: moi dau van KHAC nhau nen phep so "hai dau khac
    nhau" mu voi no — chi phep DEM SO LAN GOI nguon ngau nhien moi bat duoc.
    """
    return secrets.token_hex(16)


class KhungPhat:
    """Phat ket qua ca ra kenh rieng.

    M7 — ten ca do KHUNG dong dau tu trang thai cua CHINH khung (`_ca_dang_chay`),
    KHONG lay tu doi so nguoi goi. Nho vay ma san pham goi `phat()` trong luc ca
    `T3` dang chay chi tao duoc mot ban ghi mang ten `T3` — tuc mot ban ghi THU HAI
    cua `T3` (=> KHONG DO DUOC), chu khong doat duoc danh tinh cua `T1`.
    """

    def __init__(self, duong: Path, dau_phien: str, mutant: str, lan_thu: int):
        self._f = duong.open("a", encoding="utf-8", newline="\n")
        self._neo = {"dau_phien": dau_phien, "mutant": mutant, "lan_thu": lan_thu}
        self._ca_dang_chay = None

    def vao_ca(self, ten: str) -> None:
        self._ca_dang_chay = ten

    def phat(self, nhan: str, chi_tiet: str = "") -> None:
        ban_ghi = dict(self._neo, ca=self._ca_dang_chay, nhan=nhan, chi_tiet=chi_tiet)
        self._f.write(json.dumps(ban_ghi, ensure_ascii=False, sort_keys=True) + "\n")
        self._f.flush()

    def dong_luot(self, rc: int) -> None:
        ban_ghi = dict(self._neo, dong_luot=True, rc=rc)
        self._f.write(json.dumps(ban_ghi, ensure_ascii=False, sort_keys=True) + "\n")
        self._f.flush()
        self._f.close()


def doc_kenh(duong: Path, dau_phien: str, mutant: str, lan_thu: int, dich, rc_that=None):
    """Vo FAIL-CLOSE: moi ngoai le BAT NGO thanh KHONG DO DUOC, khong thoat ra.

    F01 (luot 7) — de mot ngoai le thoat ra thi luot CHAY LAI bien mat: do duoc,
    JSON `null`/`[]` lam bo cham chay 1 lan thay vi 2. KDD lam suite DO chu khong
    cap tin dung, nen day la huong an toan.
    """
    # F04 (luot 11) — `dich` phai duoc VAT HOA MOT LAN. Phep xac thuc F01 doc
    # `dich` BA lan (`not dich`, `set(dich) - ten_ca`, `set(dich)`); voi mot
    # iterable MOT-LAN-DOC (iterator/generator) thi lan doc dau TIEU THU no, nen
    # `set(dich)` cuoi cung ra RONG va `do_chot == set(dich)` lai dung khi khong
    # ca nao chet => GIET GIA. Tuc ban va F01 TU TAI TAO dung cai lo no sinh ra
    # de chan, qua mot cua khac. Do duoc: `iter(("T1",))` va `(x for x in ...)`
    # deu tra GIET tren mot kenh 8 ca DAT.
    # Chot nay che duong goi TRUC TIEP `doc_kenh`; duong qua `chay_mot_mutant`
    # co chot RIENG (vat hoa TRUOC vong lap) vi o do con phai song qua HAI lan
    # thu — bo mot trong hai chot deu co dau vao phan biet duoc, khong tuong duong.
    try:
        return _doc_kenh_xac_thuc(duong, dau_phien, mutant, lan_thu, tuple(dich), rc_that)
    except Exception as exc:                      # noqa: BLE001 — fail-close co chu y
        _ghi_ha_tang(exc)                         # r2 M1 diem nuot: doc_kenh
        return KHONG_DO_DUOC, f"bo doc kenh nem {type(exc).__name__}: {exc}"


def _doc_kenh_xac_thuc(duong: Path, dau_phien: str, mutant: str, lan_thu: int, dich, rc_that=None):
    """Doc kenh va phan BA trang thai. Moi nhanh tu choi deu neu ly do.

    Chi nhan ban ghi neo DUNG luot vua phong: (dau_phien, mutant, lan_thu).
    Thieu ban ghi dong luot => KHONG DO DUOC (mot luot bi giet giua chung van co
    the de lai du so ban ghi).
    """
    if not duong.exists():
        return KHONG_DO_DUOC, "kenh khong ton tai"
    # F01 (luot 7, TANG SAN PHAM) — LOI THAT trong chinh bo cham, khong phai mot
    # o chua phu cua ca do. Bon duong da do duoc tren ban NGUYEN GOC:
    #   · HAI ban ghi dong luot: ban sau GHI DE ban truoc, nen cay `rc=99` roi
    #     `rc=1` van qua phep so rc va tra GIET — pha thang chieu neo rc cua E3;
    #   · mot ban ghi mang CA `ca` LAN `dong_luot` di nhanh dong TRUOC phep kiem
    #     trung ca;
    #   · `nhan` khong duoc xac thuc, nen xoa `nhan` cua T2 van tra GIET;
    #   · JSON `null`/list, ten ca list/dict, UTF-8 hong nem AttributeError /
    #     TypeError / UnicodeDecodeError RA NGOAI, nen `chay_mot_mutant` KHONG
    #     chuyen chung thanh KHONG DO DUOC va MAT luot chay lai (do duoc: chay
    #     1 lan thay vi 2).
    # Nep: XAC THUC truoc, TIN sau. Moi duong tu choi deu ve KHONG DO DUOC —
    # huong fail-close, vi KDD lam suite DO chu khong cap tin dung.
    try:
        noi_dung = duong.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        _ghi_ha_tang(exc)                         # r2 M1 diem nuot: _doc_kenh_xac_thuc
        return KHONG_DO_DUOC, f"khong doc duoc kenh: {type(exc).__name__}: {exc}"
    neo = {"dau_phien": dau_phien, "mutant": mutant, "lan_thu": lan_thu}
    NHAN_HOP_LE = {NHAN_DAT, NHAN_DO_CHOT, NHAN_DO_KHAC}
    theo_ca, chi_tiet, dong = {}, {}, None
    for dong_txt in noi_dung.split("\n"):
        if not dong_txt.strip():
            continue
        try:
            r = json.loads(dong_txt)
        except json.JSONDecodeError:
            return KHONG_DO_DUOC, "ban ghi khong phai JSON"
        if not isinstance(r, dict):
            return KHONG_DO_DUOC, f"ban ghi khong phai object: {type(r).__name__}"
        if dong is not None:
            return KHONG_DO_DUOC, "co ban ghi SAU ban ghi dong luot"
        if any(r.get(k) != v for k, v in neo.items()):
            ten_bg = r.get("ca") if isinstance(r.get("ca"), str) else "dong_luot"
            return KHONG_DO_DUOC, f"ban ghi khong neo dung luot: {ten_bg}"
        # R13-F02 (luot 13, codex trong PR) — `bool(...)` la mot phep EP KIEU, va
        # ep kieu o day chinh la cap tin dung cho thu KHONG dung dinh dang. Do
        # duoc tren ban truoc: mot kenh du 8 ca, `T1=DO_CHOT`, dong luot khai
        # `{"dong_luot": 1}` hoac `{"dong_luot": "yes"}` deu tra GIET.
        # Kenh la HOP DONG: dau dong phai la bool JSON `true`, khong phai bat cu
        # thu gi truthy. Mot writer hong hoac mot ban ghi meo phai lam suite DO,
        # khong duoc nhan tin dung. Cung ho `nhan-rc-bool` (loai `bool` khoi `int`
        # cho `rc`) — o day la chieu NGUOC: doi DUNG bool, khong nhan thay the.
        co_dong = r.get("dong_luot") is True
        if "dong_luot" in r and not co_dong:
            return KHONG_DO_DUOC, f"dau dong luot khong phai bool true: {r.get('dong_luot')!r}"
        co_ca = "ca" in r
        if co_ca and co_dong:
            return KHONG_DO_DUOC, "ban ghi vua mang ten ca vua khai dong luot"
        if co_dong:
            dong = r
            continue
        ca = r.get("ca")
        if ca is None:
            return KHONG_DO_DUOC, "ban ghi thieu ten ca"
        if not isinstance(ca, str):
            return KHONG_DO_DUOC, f"ten ca khong phai chuoi: {type(ca).__name__}"
        if ca in theo_ca:
            return KHONG_DO_DUOC, f"ban ghi TRUNG cho ca {ca}"
        nhan = r.get("nhan")
        if nhan not in NHAN_HOP_LE:
            return KHONG_DO_DUOC, f"nhan khong hop le cho ca {ca}: {nhan!r}"
        ct = r.get("chi_tiet", "")
        if not isinstance(ct, str):
            return KHONG_DO_DUOC, f"chi tiet khong phai chuoi cho ca {ca}"
        theo_ca[ca] = nhan
        chi_tiet[ca] = ct
    if dong is None:
        return KHONG_DO_DUOC, "thieu ban ghi dong luot"
    # F01 — `rc` la MOT CHIEU NEO, khong phai trang tri. Thieu chieu nay thi mot
    # luot con bao "xong rc=0" trong khi tien trinh that thoat 1 van duoc nhan.
    # `bool` la con cua `int` trong Python, nen phai loai RIENG: `True` se so
    # bang `1` va lot qua phep neo rc.
    if not isinstance(dong.get("rc"), int) or isinstance(dong.get("rc"), bool):
        return KHONG_DO_DUOC, "ban ghi dong luot thieu rc kieu int"
    if rc_that is not None and dong["rc"] != rc_that:
        return KHONG_DO_DUOC, f"rc dong luot {dong['rc']} != rc tien trinh {rc_that}"
    ten_ca = {t for t, _ in CA}
    if set(theo_ca) != ten_ca:
        thieu = sorted(ten_ca - set(theo_ca))
        la = sorted(set(theo_ca) - ten_ca)
        return KHONG_DO_DUOC, f"thieu ca {thieu} / ca la {la}"
    if any(n == NHAN_DO_KHAC for n in theo_ca.values()):
        xau = sorted(t for t, n in theo_ca.items() if n == NHAN_DO_KHAC)
        ct = "; ".join(f"{c}: {chi_tiet.get(c, '')}" for c in xau)
        return KHONG_DO_DUOC, f"ca do vi ngoai le KHONG phai TinHieuChotCa: {xau} | {ct}"
    # F01 (luot 10) — DICH la DU LIEU MO TA, va no chua tung duoc xac thuc.
    # Phep so `do_chot == set(dich)` DUNG khi CA HAI ve rong, nen mot muc bang
    # khai `dich=()` duoc cap GIET trong khi KHONG ca nao chet va dot bien
    # khong doi mot byte nao. Do duoc (cross-review luot 10, HUONG 7): mot muc
    # no-op `(ten, (), neo, neo)` cho `0/0`, tong `10/0/0`, `rc=0` — cong XANH
    # trong khi khong do gi. Day dung la benh packet nay sinh ra de chan, o
    # ngay TANG TREN CUNG: cap tin dung cho thu chet vi ly do vo can — o day
    # con te hon, cap tin dung cho thu KHONG chet.
    # Huong tu choi la KDD chu khong phai KHONG_GIET: descriptor sai la loi
    # CAU HINH, khong phai ket luan ve suc manh cua bo test.
    if not dich:
        return KHONG_DO_DUOC, "dich RONG: khong cap GIET khi khong ca nao phai chet"
    dich_la = sorted(set(dich) - ten_ca)
    if dich_la:
        return KHONG_DO_DUOC, f"dich co ten ca KHONG ton tai: {dich_la}"
    do_chot = {t for t, n in theo_ca.items() if n == NHAN_DO_CHOT}
    if do_chot == set(dich):
        return GIET, ""
    return KHONG_GIET, f"tap ca do chot {sorted(do_chot)} != dich {sorted(dich)}"
# WP748 r16 — tran giay cho MOI tien trinh con; None (mac dinh) = hanh vi cu. Chi
# `chay_manh_dich` dat no. Qua tran => rc 124 + dong khai trong stderr, KHONG nem: nguoi
# goi phan hang rc != 1 thanh TIN DUNG GIA / KHONG DO DUOC, tuc manh DO (fail-closed).
_TRAN_GIAY_CON = None
_GIAY_THU_SAU_GIET = 5.0
# WP748 r22 l2 (Codex F02 lo 1) — DAU MOI LUOT trong env cua con, ke thua xuong MOI hau due. Chau mo coi da `setsid`
# roi bi doi PPID ve 1 thi thoat phep di PPID, nhung KHONG thoat phep quet dau nay. Gioi han da khai: tien trinh tu
# XOA env cua minh thi thoat ca hai — `duong` noi ro phep quet nao da chay.
DAU_CAY_ENV = "NHANH_DON_DUOC_CAY"
MA_KHONG_RANH_GIOI = 126     # WP748 r22 l2 lo 2: KHONG dung duoc ranh gioi ca cay => khong chay con (fail-closed)


def _stat_posix(pid, goc_proc="/proc"):
    try:
        return Path(f"{goc_proc}/{pid}/stat").read_text().rsplit(")", 1)[1].split()
    except (OSError, IndexError):
        return None


def _hau_due_posix(goc: int, goc_proc: str = "/proc") -> dict:
    """WP748 r22 (Codex l22 F02) — `{pid: starttime}` MOI hau due dang song cua `goc`, doc `/proc` theo PPID, KE CA chau
    da `setsid` sang phien khac (`killpg` khong thay no). Chup TRUOC tin hieu: cha chet thi con mo coi doi PPID ve 1.
    `starttime` la khoa danh tinh. Khong co `/proc` => {}."""
    con, bat_dau = {}, {}
    try:
        ten = os.listdir(goc_proc)
    except OSError:
        return {}
    for t in ten:
        truong = _stat_posix(t, goc_proc) if t.isdigit() else None
        if truong is None:
            continue
        con.setdefault(int(truong[1]), []).append(int(t))
        bat_dau[int(t)] = truong[19]
    ra, hang = {}, [goc]
    while hang:
        for c in con.get(hang.pop(), []):
            if c not in ra:
                ra[c] = bat_dau[c]
                hang.append(c)
    return ra


def _quet_dau_posix(ten: str, gia_tri: str, goc_proc: str = "/proc"):
    """WP748 r22 l2 lo 1 — `{pid: starttime}` moi tien trinh co `ten=gia_tri` trong `/proc/<pid>/environ`, KHONG phu
    thuoc PPID (bat chau mo coi). `None` = KHONG quet duoc (khong `/proc`): nguoi goi phai noi ra, khong duoc doc thanh
    "khong co ai"."""
    try:
        ds = os.listdir(goc_proc)
    except OSError:
        return None
    can = f"{ten}={gia_tri}".encode()
    ra = {}
    for t in ds:
        if not t.isdigit():
            continue
        try:
            moi_truong = Path(f"{goc_proc}/{t}/environ").read_bytes().split(b"\0")
        except OSError:
            continue                                  # tien trinh cua nguoi khac / da chet: khong phai cua ta
        truong = _stat_posix(t, goc_proc)
        if can in moi_truong and truong is not None:
            ra[int(t)] = truong[19]
    return ra


def _con_song_posix(pid: int, khoa: str, goc_proc: str = "/proc") -> bool:
    """Song = cung `starttime` VA khong phai zombie (zombie da chet, chi cho thu hoi)."""
    truong = _stat_posix(pid, goc_proc)
    return truong is not None and truong[19] == khoa and truong[0] != "Z"


def _giet_dinh_danh(pid: int, khoa: str, goc_proc: str = "/proc") -> str:
    """WP748 r22 l2 lo 4 — giet `pid` CHI KHI no van la tien trinh da chup (`starttime` == `khoa`). Co `pidfd`: mo fd
    TRUOC, kiem danh tinh SAU, gui tin hieu qua fd — fd ghim dung mot tien trinh nen PID bi tai su dung giua kiem va
    giet KHONG nhan tin hieu (khe dong). Khong co `pidfd` thi lui ve kill theo PID va TRA DUNG su that: khe con mo."""
    mo, gui = getattr(os, "pidfd_open", None), getattr(signal, "pidfd_send_signal", None)
    if mo is not None and gui is not None:
        try:
            fd = mo(pid)
        except OSError:
            return "da chet"
        try:
            if not _con_song_posix(pid, khoa, goc_proc):   # WP748 r22 l2: kiem danh tinh pidfd
                return "khac danh tinh"
            gui(fd, getattr(signal, "SIGKILL", 9))
            return "pidfd"
        except OSError as e:
            return f"pidfd loi {type(e).__name__}"
        finally:
            os.close(fd)
    if not _con_song_posix(pid, khoa, goc_proc):
        return "khac danh tinh"
    try:
        os.kill(pid, getattr(signal, "SIGKILL", 9))
    except OSError as e:
        return f"kill loi {type(e).__name__}"
    return "kill theo PID (khong co pidfd: khe tai su dung PID CON MO)"


class _VeWindows:
    """WP748 r22 (Codex l22 F02) — ranh gioi vong doi CUONG CHE cho ca cay tren Windows: Job Object rieng moi luot,
    dat `KILL_ON_JOB_CLOSE`. Con tao TREO (`CREATE_SUSPENDED`), gan vao job, roi moi chay tiep (`NtResumeProcess`) —
    nen KHONG hau due nao sinh truoc khi job co hieu luc. Qua tran => `TerminateJobObject`; dong job (moi duong ra,
    ke ca ngoai le) cung giet ca cay. WP748 r22 l2 lo 2: hong o tao/dat/gan/chay tiep => KHONG co ranh gioi =>
    `run` tra `MA_KHONG_RANH_GIOI` chu KHONG cho con chay ngoai job (truoc day: van chay, chi ghi `loi`)."""
    CREATE_SUSPENDED = 0x4
    _KILL_ON_JOB_CLOSE, _LOP_GIOI_HAN_MO_RONG = 0x2000, 9

    def __init__(self):
        import ctypes
        self.k32, self.ntdll, self.job, self.loi = None, None, None, None
        try:
            self.k32 = ctypes.WinDLL("kernel32", use_last_error=True)
            self.k32.CreateJobObjectW.restype = ctypes.c_void_p
            self.k32.SetInformationJobObject.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p,
                                                         ctypes.c_uint)
            self.k32.AssignProcessToJobObject.argtypes = (ctypes.c_void_p, ctypes.c_void_p)
            self.k32.TerminateJobObject.argtypes = (ctypes.c_void_p, ctypes.c_uint)
            self.k32.CloseHandle.argtypes = (ctypes.c_void_p,)
            self.ntdll = ctypes.WinDLL("ntdll")
            self.ntdll.NtResumeProcess.argtypes = (ctypes.c_void_p,)
            self.job = self.k32.CreateJobObjectW(None, None)
            if not self.job:
                self.loi = f"CreateJobObjectW loi {ctypes.get_last_error()}"
                return
            u64, sz = ctypes.c_ulonglong, ctypes.c_size_t

            class _Co(ctypes.Structure):
                _fields_ = [("a", ctypes.c_longlong), ("b", ctypes.c_longlong), ("LimitFlags", ctypes.c_uint32),
                            ("c", sz), ("d", sz), ("e", ctypes.c_uint32), ("f", sz), ("g", ctypes.c_uint32),
                            ("h", ctypes.c_uint32)]

            class _MoRong(ctypes.Structure):
                _fields_ = [("co", _Co), ("io", u64 * 6), ("m1", sz), ("m2", sz), ("m3", sz), ("m4", sz)]
            gh = _MoRong()
            gh.co.LimitFlags = self._KILL_ON_JOB_CLOSE
            if not self.k32.SetInformationJobObject(self.job, self._LOP_GIOI_HAN_MO_RONG, ctypes.byref(gh),
                                                    ctypes.sizeof(gh)):
                self.loi = f"SetInformationJobObject loi {ctypes.get_last_error()}"
                self.dong()
        except (OSError, AttributeError) as e:
            self.loi = f"khong nap duoc kernel32/ntdll: {type(e).__name__}"
            self.job = None

    def dung_duoc(self) -> bool:
        return self.job is not None and self.ntdll is not None

    def gan_va_chay(self, q) -> bool:
        """True = con dang chay TRONG job. False = con (dang treo, chua chay dong nao) da bi giet; `loi` noi vi sao."""
        import ctypes
        h = int(q._handle)
        if not self.k32.AssignProcessToJobObject(self.job, h):
            self.loi = f"AssignProcessToJobObject loi {ctypes.get_last_error()}"
            q.kill()
            return False
        try:
            ma = self.ntdll.NtResumeProcess(h)
        except (OSError, AttributeError) as e:
            ma = f"{type(e).__name__}"
        if ma != 0:
            self.loi = f"NtResumeProcess loi {ma}"
            q.kill()
            return False
        return True

    def ket_thuc(self, q) -> str:
        if self.job and self.k32.TerminateJobObject(self.job, 1):
            return "TerminateJobObject (ca cay trong job)"
        ghi = f"TerminateJobObject HONG ({self.loi}) -> taskkill, CAY CO THE CON SONG toi khi dong job"
        tk = shutil.which("taskkill")
        if tk:
            try:
                r = subprocess.run([tk, "/T", "/F", "/PID", str(q.pid)], capture_output=True, text=True,
                                   timeout=_GIAY_THU_SAU_GIET)
                ghi += f" rc={r.returncode}"
            except (OSError, subprocess.TimeoutExpired) as e:
                ghi += f" loi {type(e).__name__}"
        q.kill()
        return ghi

    def dong(self) -> None:
        if self.job:
            self.k32.CloseHandle(self.job)              # KILL_ON_JOB_CLOSE: dong = giet moi thu con trong job
            self.job = None


def _ket_thuc_cay(q, ve, dau: str = "") -> str:
    """WP748 r22 F02 — giet CA CAY cua `q`, tra mot dong DO DUOC (ke ca phan KHONG lam duoc). POSIX: chup hau due qua
    PPID VA qua dau env (`dau`, bat chau mo coi) TRUOC, `killpg` nhom con (CHI khi nhom = pid con va KHAC nhom minh),
    roi giet tung tien trinh da chup bang `_giet_dinh_danh`, quet lai dau toi khi sach hoac het han: "da goi lenh
    giet" != "da chet". Windows: `ve.ket_thuc`. DIEM GOI DUY NHAT cua viec don cay (dot bien `timeout-chi-giet-con`)."""
    if ve is not None:
        return ve.ket_thuc(q)
    import time as _t
    chup = _hau_due_posix(q.pid)
    theo_dau = _quet_dau_posix(DAU_CAY_ENV, dau) if dau else None
    ghi = [f"chup {len(chup)} hau due PPID",
           f"dau env {len(theo_dau)}" if theo_dau is not None else "dau env KHONG QUET DUOC (chau mo coi co the SONG)"]
    chup.update(theo_dau or {})
    try:
        nhom = os.getpgid(q.pid)
        if nhom == q.pid and nhom != os.getpgid(0):
            os.killpg(nhom, signal.SIGKILL)
            ghi.append(f"killpg {nhom}")
        else:
            q.kill()
            ghi.append("KHONG co nhom rieng -> giet con")
    except OSError as e:
        q.kill()
        ghi.append(f"getpgid/killpg loi {type(e).__name__} -> giet con")
    cach = set()
    han = _t.monotonic() + _GIAY_THU_SAU_GIET
    while True:
        for pid, khoa in chup.items():
            if _con_song_posix(pid, khoa):
                cach.add(_giet_dinh_danh(pid, khoa))
        song = sorted(pid for pid, k in chup.items() if _con_song_posix(pid, k))
        moi = (_quet_dau_posix(DAU_CAY_ENV, dau) or {}) if dau else {}
        moi = {p: k for p, k in moi.items() if p not in chup}   # sinh SAU luc chup (fork giua chup va giet)
        chup.update(moi)
        if (not song and not moi) or _t.monotonic() >= han:
            break
        _t.sleep(0.05)
    if cach:
        ghi.append("giet: " + ", ".join(sorted(cach)))
    ghi.append(f"tien trinh CON SONG {song}" if song else "0 tien trinh da chup con song")
    return " · ".join(ghi)


def run(args: list[str], cwd: Path, check: bool = True, env: dict[str, str] | None = None):
    if _TRAN_GIAY_CON is None:
        p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", env=env, check=False)
    else:
        # WP748 r22 F02 — ranh gioi ca cay (POSIX: phien rieng + chup PPID + dau env; Windows: Job Object rieng
        # KILL_ON_JOB_CLOSE, con tao TREO roi moi gan job). Thu output SAU giet CO HAN va KHONG dong ong dong bo (tren
        # Windows luong doc dang giu khoa cua ong thi `close()` cung treo): qua han thi BO output, ghi ro. rc 124.
        ve = _VeWindows() if os.name == "nt" else None
        if ve is not None and not ve.dung_duoc():   # WP748 r22 l2 lo 2: khong job thi KHONG chay
            ve.dong()
            p = subprocess.CompletedProcess(args, MA_KHONG_RANH_GIOI, "",
                                            f"KHONG DUNG DUOC ranh gioi job ({ve.loi}): KHONG chay con")
        else:
            dau = secrets.token_hex(16)
            env = dict(os.environ if env is None else env, **{DAU_CAY_ENV: dau})
            tach = ({"start_new_session": True} if ve is None else
                    {"creationflags": getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | _VeWindows.CREATE_SUSPENDED})
            q = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                 encoding="utf-8", errors="replace", env=env, **tach)
            try:
                if ve is not None and not ve.gan_va_chay(q):
                    q.wait()
                    p = subprocess.CompletedProcess(args, MA_KHONG_RANH_GIOI, "",
                                                    f"KHONG DUNG DUOC ranh gioi job ({ve.loi}): con bi giet truoc khi chay")
                else:
                    try:
                        ra, loi = q.communicate(timeout=_TRAN_GIAY_CON)
                        p = subprocess.CompletedProcess(args, q.returncode, ra, loi)
                    except subprocess.TimeoutExpired:
                        # WP748 r22 l2 lo 3: don cay NEM thi van rc 124 + noi that, KHONG de ngoai le thay ket qua
                        try:
                            duong = _ket_thuc_cay(q, ve, dau)   # WP748 r22 F02: diem goi don cay
                        except Exception as e:                  # noqa: BLE001 — ghi vao `duong`, rc van 124
                            _ghi_ha_tang(e)
                            duong = f"LOI don cay {type(e).__name__}: {e} — CAY CO THE CON SONG"
                            try:
                                q.kill()
                            except OSError:
                                pass
                        try:
                            ra, loi = q.communicate(timeout=_GIAY_THU_SAU_GIET)
                        except subprocess.TimeoutExpired:
                            ra, loi = "", f"output BO sau {_GIAY_THU_SAU_GIET}s (con giu ong)"
                        p = subprocess.CompletedProcess(args, 124, ra or "",
                                                        f"{loi or ''}\nQUA TRAN {_TRAN_GIAY_CON}s: con bi giet ({duong})")
            finally:
                if ve is not None:
                    ve.dong()
    if check and p.returncode:
        raise AssertionError(f"rc={p.returncode}: {' '.join(args)}\n{p.stdout}\n{p.stderr}")
    return p
def viet(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
def _dau_hieu_kho_bare(remote: Path, khi: str) -> None:
    """Chot BA DAU HIEU CAU TRUC cua mot kho bare con ton tai.

    KHONG CHUNG MINH `core.bare = true`. Do duoc (cross-review luot 4 tren
    8de4e66): ham nay CHAP NHAN `.git` cua mot kho lam viec binh thuong, noi
    `core.bare = false`. Doc `config` de biet chac doi mot phep do khac; con
    hoi `git` thi phai PHONG TIEN TRINH, ma chinh viec ay da lam `gate-registry`
    chuyen tu xanh sang do o 0c89a6e. Nen ten va thong diep cua chot nay duoc
    THU HEP ve dung cai no do, thay vi noi long phep do de khop mot ten rong.

    #568 — mot loi VO CAN khong ten la dung benh goi nay chua. `git push` bao
    "does not appear to be a git repository" o mot buoc CACH XA cho tao kho, nen
    thong diep ay khong noi duoc kho bien mat luc nao. Chot nay dat o hai moc va
    mang theo DU KIEN: buoc nao, thu muc con gi, va git noi gi.
    """
    # KHONG phong tien trinh. Ban truoc cua chot nay goi `git rev-parse` HAI lan
    # moi `kho_bare()`, tuc them hai tien trinh tren duong ma hang chuc ca va 112
    # tien trinh con deu di qua. `gate-registry` CHUYEN TU XANH (7d0b012) SANG DO
    # (0c89a6e) ngay o commit them chot ay, voi
    #     VO CAN r506: OSError: [Errno 39] Directory not empty: '.../remote.git'
    # Chua chung minh duoc co che, nhung mot phep DO khong duoc lam doi TAI cua
    # thu no dang do — do la loi thiet ke cua chot, khong phai xui. Nay chot doc
    # DAU HIEU tren dia: mot kho bare co `HEAD`, `objects/`, `refs/`.
    # KHONG lay `remote` lam `cwd` (ban dau cua chot nay sap voi `FileNotFoundError`
    # vo danh khi thu muc bien mat — dung lop benh no di chua).
    try:
        dau_hieu = {
            "ton tai": remote.is_dir(),
            "HEAD": (remote / "HEAD").is_file(),
            "objects/": (remote / "objects").is_dir(),
            "refs/": (remote / "refs").is_dir(),
        }
    except OSError as exc:
        raise AssertionError(
            f"dau hieu kho bare hong {khi}: {remote} | KHONG DOC DUOC: {type(exc).__name__}: {exc}")
    if all(dau_hieu.values()):
        return
    try:
        co = sorted(x.name for x in remote.iterdir())
    except OSError as exc:
        _ghi_ha_tang(exc)                    # r2 vong 4: loi bi doi thanh CHUOI truoc khi AssertionError
        co = f"KHONG DOC DUOC THU MUC: {type(exc).__name__}: {exc}"
    thieu = sorted(k for k, v in dau_hieu.items() if not v)
    raise AssertionError(
        f"dau hieu kho bare hong {khi}: {remote} | thieu={thieu} | thu muc con={co}")


def kho_bare(*, mac_dinh: str = "main", a: bool = False, b: bool = False,
             c_mot: bool = False, c_hai: bool = False):
    td = tempfile.TemporaryDirectory()
    root, remote, work = Path(td.name), Path(td.name) / "remote.git", Path(td.name) / "work"
    run(["git", "init", "--bare", str(remote)], root)
    _tat_bao_tri_kho_bare(remote)
    _dau_hieu_kho_bare(remote, "ngay sau `git init --bare`")
    run(["git", "init", "-b", mac_dinh, str(work)], root)
    run(["git", "config", "user.name", "test"], work)
    run(["git", "config", "user.email", "test@example.invalid"], work)
    # M4 — kho THU NHAT. Moi truong ep ky commit (container ky moi commit) lam
    # `git commit` hong => `run()` nem AssertionError TRAN, khong phan biet duoc
    # voi chot cua ca. Tat o CA HAI kho bo test dung, khong phai mot.
    run(["git", "config", "commit.gpgsign", "false"], work)
    run(["git", "config", "tag.gpgsign", "false"], work)
    viet(work / "ops/leases/base.yaml", "lease_id: base\n")
    viet(work / "state.txt", "A\n")
    run(["git", "add", "--", "ops/leases/base.yaml", "state.txt"], work)
    run(["git", "commit", "-m", "A"], work)
    viet(work / "state.txt", "S\n")
    run(["git", "commit", "-am", "S"], work)
    if a:
        run(["git", "branch", "ops/a"], work)
    viet(work / "state.txt", "D\n")
    run(["git", "commit", "-am", "D"], work)
    if b:
        run(["git", "switch", "-c", "ops/b"], work)
        with (work / "ops/leases/base.yaml").open("a", encoding="utf-8", newline="\n") as f:
            f.write("posted_comment_id: 123   # workflow ghi, DUNG sua tay\n")
        run(["git", "commit", "-am", "posted_comment_id"], work)
        run(["git", "switch", mac_dinh], work)
    if c_mot:
        run(["git", "switch", "-c", "ops/c-mot"], work)
        viet(work / "rieng.txt", "khac posted_comment_id\n")
        run(["git", "add", "--", "rieng.txt"], work)
        run(["git", "commit", "-m", "mot commit thuong"], work)
        run(["git", "switch", mac_dinh], work)
    if c_hai:
        run(["git", "switch", "-c", "ops/c-hai"], work)
        for i in (1, 2):
            viet(work / "rieng.txt", f"{i}\n")
            run(["git", "add", "--", "rieng.txt"], work)
            run(["git", "commit", "-m", f"commit rieng {i}"], work)
        run(["git", "switch", mac_dinh], work)
    run(["git", "remote", "add", "origin", str(remote)], work)
    # Windows (log chu kho, 2026-09-21): `git push --all origin` tra rc=128 voi
    # "does not appear to be a git repository" cho DUNG duong vua `init --bare`
    # thanh cong o tren — mot lan trong ba luot, tren CA #590 lan #591. Khong tai
    # lap duoc tren Linux. Chua biet nguyen nhan, nen o day KHONG doan: chi DO
    # ngay truoc khi day, de luot Windows sau NEU TEN duoc buoc that su hong.
    _dau_hieu_kho_bare(remote, "ngay truoc `git push --all origin`")
    run(["git", "push", "--all", "origin"], work)
    run(["git", "symbolic-ref", "HEAD", f"refs/heads/{mac_dinh}"], remote)
    run(["git", "fetch", "origin"], work)
    return td, remote, work
def tool(work: Path):
    p = run([sys.executable, str(TOOL), "--repo", str(work)], work, check=False)
    if p.returncode:
        raise AssertionError(f"tool rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    nhom = {}
    for line in p.stdout.splitlines():
        if re.match(r"^[ABC]\t", line):
            n, ten, ly_do = line.split("\t", 2)
            nhom[ten] = (n, ly_do)
    dong_lenh = next(x for x in p.stdout.splitlines() if x.startswith("git push "))
    return nhom, shlex.split(dong_lenh)[4:], p.stdout
def nap_tool():
    spec = importlib.util.spec_from_file_location("nhanh_don_duoc", TOOL)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod
def T1():
    td, _, work = kho_bare(a=True)
    try:
        nhom, lenh, _ = tool(work)
        chot(nhom["ops/a"][0] == "A" and "ops/a" in lenh, "T1")
    finally:
        td.cleanup()
def T2():
    td, _, work = kho_bare(c_hai=True)
    try:
        nhom, _, _ = tool(work)
        chot(nhom["ops/c-hai"][0] == "C", "T2")
    finally:
        td.cleanup()
def T3():
    td, _, work = kho_bare(b=True, c_mot=True)
    try:
        nhom, lenh, _ = tool(work)
        chot(nhom["ops/b"][0] == "B" and "ops/b" in lenh, "T3")
        chot(nhom["ops/c-mot"][0] == "C" and "ops/c-mot" not in lenh, "T3")
    finally:
        td.cleanup()
def T4():
    td, _, work = kho_bare(a=True)
    try:
        ref = "refs/remotes/origin/ops/a"
        tip = run(["git", "rev-parse", ref], work).stdout.strip()
        base_ref = "refs/remotes/origin/main"
        base = run(["git", "rev-parse", base_ref], work).stdout.strip()
        run(["git", "update-ref", "-d", ref], work)
        kq = nap_tool().phan_loai(work, ref, tip, base_ref, base)
        chot(kq.nhom == "C" and ("bien mat" in kq.ly_do or "khong doc" in kq.ly_do), "T4")
    finally:
        td.cleanup()
def T5():
    td, remote, _ = kho_bare(c_hai=True)
    try:
        reader = Path(td.name) / "shallow"
        run(["git", "clone", "--depth", "1", "--no-single-branch", remote.as_uri(), str(reader)], Path(td.name))
        nhom, lenh, _ = tool(reader)
        chot(nhom and all(v[0] == "C" and "kho nong" in v[1] for v in nhom.values()) and not lenh, "T5")
    finally:
        td.cleanup()
def T6():
    td, _, work = kho_bare(mac_dinh="ops/main", a=True)
    try:
        nhom, lenh, _ = tool(work)
        chot(nhom["ops/main"][0] == "A" and "ops/main" not in lenh, "T6")
    finally:
        td.cleanup()
def T7():
    td, _, work = kho_bare()
    try:
        _, _, out = tool(work)
        chot("nhanh mac dinh co the bi ep lui" in out, "T7")
        chot("KHONG co phep kiem nao luc chay" in out, "T7")
    finally:
        td.cleanup()
def T8():
    td, remote, work = kho_bare(a=True)
    try:
        chot(run(["git", "rev-parse", "--is-bare-repository"], remote).stdout.strip() == "true", "T8")
        ref = "refs/remotes/origin/ops/a"
        tip = run(["git", "rev-parse", ref], work).stdout.strip()
        base_ref = "refs/remotes/origin/main"
        base = run(["git", "rev-parse", base_ref], work).stdout.strip()
        chot(run(["git", "rev-list", "--count", f"{base}..{tip}"], work).stdout.strip() == "0", "T8")
        chot(run(["git", "merge-base", "--is-ancestor", tip, base], work, check=False).returncode == 0, "T8")
        remote.rename(Path(td.name) / "remote.offline")
        nhom, lenh, _ = tool(work)
        chot(nhom["ops/a"][0] == "C" and "fetch loi:" in nhom["ops/a"][1], "T8")
        chot("ops/a" not in lenh, "T8")
    finally:
        td.cleanup()
CA = [(f"T{i}", globals()[f"T{i}"]) for i in range(1, 9)]
DOT_BIEN = [
    ("dao-chieu-to-tien", ("T1",), 'p = _git(repo, "merge-base", "--is-ancestor", tip, base_oid)', 'p = _git(repo, "merge-base", "--is-ancestor", base_oid, tip)'),
    ("bo-kiem-commit-rieng", ("T2",), 'return KetQua("C", f"con {so_rieng} commit rieng")', 'return KetQua("A", "dot bien bo kiem commit rieng")'),
    ("noi-B-thanh-mot-commit", ("T3",), "if la_posted:", "if True:"),
    ("loi-thanh-khong-commit-rieng", ("T4",), 'return KetQua("C", f"ref bien mat/khong doc duoc: {loi}")', 'return KetQua("A", "dot bien coi loi la khong co commit rieng")'),
    ("in-ca-C", ("T3", "T5", "T8"), 'kq.nhom in {"A", "B"} and ten != mac_dinh', 'kq.nhom in {"A", "B", "C"} and ten != mac_dinh'),
    ("bo-loai-mac-dinh", ("T6",), 'kq.nhom in {"A", "B"} and ten != mac_dinh', 'kq.nhom in {"A", "B"}'),
    ("xoa-khai-gioi-han", ("T7",), '"GIOI HAN: lenh in ra KHONG co phep kiem nao luc chay; phai doc lai ket qua truoc khi dan lenh."', '"GIOI HAN: da bi dot bien xoa."'),
    ("bo-chan-fetch-loi", ("T8",), "if fetch.returncode:", "if False:"),
    ("go-nhanh-kho-nong", ("T5",), '    elif shallow:\n        loi_chung = "kho nong; lich su khong du de phan loai an toan"\n', ""),
    ("dao-khop-base-remote", ("T1", "T3", "T6"), "base_oid != remote_oid", "base_oid == remote_oid"),
]
def chay_ca(khung: "KhungPhat | None" = None):
    do = []
    for ten, fn in CA:
        if khung is not None:
            khung.vao_ca(ten)          # M7: KHUNG dong dau ten ca, khong phai ca
        try:
            fn()
            print(f"CASE {ten}: DAT")
            if khung is not None:
                khung.phat(NHAN_DAT)
        except TinHieuChotCa as exc:
            do.append(ten)
            print(f"CASE {ten}: DO — {exc}")
            if khung is not None:
                khung.phat(NHAN_DO_CHOT, str(exc))
        except Exception as exc:
            # M2 — ngoai le KHONG phai TinHieuChotCa: ca chet vi thu VO CAN voi
            # dot bien dang thu. Day la trang thai THU BA, khong phai "khong giet".
            _ghi_ha_tang(exc)                     # r2 M1 diem nuot: chay_ca
            do.append(ten)
            print(f"CASE {ten}: DO — {type(exc).__name__}: {exc}")
            if khung is not None:
                khung.phat(NHAN_DO_KHAC, f"{type(exc).__name__}: {exc}")
    return do
def chay_dot_bien(muc=None):
    dat = khong_giet = khong_do = 0
    with tempfile.TemporaryDirectory() as d:
        root, src = Path(d), Path(d) / "source"
        run(["git", "init", "-q", str(src)], root)
        run(["git", "config", "user.name", "mutation"], src)
        run(["git", "config", "user.email", "mutation@example.invalid"], src)
        # M4 — kho THU HAI. Sua moi `kho_bare` thi tam ca qua nhung suite day du
        # van chet o dung lan commit nguon mutant nay.
        run(["git", "config", "commit.gpgsign", "false"], src)
        run(["git", "config", "tag.gpgsign", "false"], src)
        shutil.copy2(TOOL, src / TOOL.name)
        shutil.copy2(Path(__file__), src / Path(__file__).name)
        run(["git", "add", "--", TOOL.name, Path(__file__).name], src)
        run(["git", "commit", "-qm", "source"], src)
        for ten, dich, neo, thay in (DOT_BIEN if muc is None else muc):
            # F07 (luot 12) — cho THU BA cua cung benh F04, va la cho ban va
            # luot 11 BO SOT. `chay_mot_mutant` co `dich = tuple(dich)` nhung do
            # chi gan lai ten CUC BO cua no; iterator cua NGUOI GOI van bi tieu
            # thu. Nen `set(dich)` o duoi day nhin thay RONG va dong bao cao in
            # `|  | 0/0` cho mot mutant DA BI GIET THAT. Do duoc (cross-review
            # luot 12, HUONG 2): cung muc `in-ca-C`, tuple in `T3,T5,T8 | 3/3`
            # con iterator/generator in `|  | 0/0`, trong khi con THAT tra GIET
            # voi do_chot = T3,T5,T8. Bo dem tong van dung — chi DONG BAO CAO
            # noi doi, va mot bo cham noi doi ve tung muc thi khong dung de doc.
            dich = tuple(dich)
            ban_sao = root / ten
            ban_sao.mkdir()
            # Moi mutant bat dau bang dung duong `git archive ... | tar -x`.
            archive = subprocess.Popen(["git", "-C", str(src), "archive", "HEAD"], stdout=subprocess.PIPE)
            assert archive.stdout is not None
            tar = subprocess.run(["tar", "-x", "-C", str(ban_sao)], stdin=archive.stdout, check=False)
            archive.stdout.close()
            if archive.wait() or tar.returncode:
                raise AssertionError("git archive | tar -x that bai")
            tep = ban_sao / TOOL.name
            text = tep.read_text(encoding="utf-8")
            if text.count(neo) != 1:
                raise AssertionError(f"neo mutant {ten} khong duy nhat")
            # F01 (luot 10) — muc `neo == thay` qua duoc phep kiem neo duy nhat
            # roi sinh ra mot "dot bien" khong doi mot byte nao. Chot nay KHONG
            # thay chot dich-khong-rong o tren: kiem byte khong loai duoc dot
            # bien TUONG DUONG ve hanh vi, con chot dich moi la thu doi phai co
            # ca chet DUNG cho. Hai chot do hai thu khac nhau.
            if thay == neo:
                raise AssertionError(f"dot bien {ten} KHONG doi byte nao (thay == neo)")
            tep.write_text(text.replace(neo, thay), encoding="utf-8", newline="\n")
            trang_thai, ly_do, so_lan = chay_mot_mutant(ban_sao, ten, dich)
            # F05 (luot 11) — `len(dich)` dem CA BAN TRUNG: mot muc khai
            # `("T3", "T3", "T5")` in ra `3/3` trong khi chi 2 ca chet, vi phep so
            # o `doc_kenh` dung `set(dich)`. Con so in ra phai la so dich PHAN BIET.
            dich_pb = sorted(set(dich))
            so_ca = len(dich_pb)
            if trang_thai == GIET:
                dat += 1
                print(f"MUTANT {ten} | {','.join(dich_pb)} | {so_ca}/{so_ca}")
            elif trang_thai == KHONG_DO_DUOC:
                khong_do += 1
                print(f"MUTANT {ten} | {','.join(dich)} | KHONG DO DUOC (sau {so_lan} lan): {ly_do}")
            else:
                khong_giet += 1
                print(f"MUTANT {ten} | {','.join(dich)} | 0/{so_ca}: {ly_do}")
    return dat, khong_giet, khong_do


# #593 r1 / M3 — `stderr[-200:]` cat tu DAU (CO Y: nguyen nhan o CUOI) ma khong noi da bo
# bao nhieu — cung lop `_goi_chan_doan` truoc #568. Nhan chi sinh KHI CO cat (`r544`).
TRAN_DUOI_STDERR = 200


def _khai_cat_dau_stderr(stderr: str) -> str:
    """Nhan KHAI so ky tu DAU da bo khi `stderr` dai hon tran; RONG khi khong cat."""
    bo = len(stderr) - TRAN_DUOI_STDERR
    return f" …[CAT {bo} ky tu dau]" if bo > 0 else ""


def chay_mot_mutant(ban_sao: Path, ten: str, dich):
    """M3 — `KHONG DO DUOC` thi chay lai DUNG MOT lan. Khong bao gio qua 2.

    Tra `(trang_thai, ly_do, so_lan_da_goi)`. So lan la de ca tu kiem DEM duoc,
    chu khong doc ma thoat — nep da tra gia o `ops-don-ref` (40/40 trong khi mot
    dot bien xoa han lenh pha van qua).
    """
    # R13-F01 (luot 13) — `ban_sao` duoc dung theo HAI he quy chieu cung luc:
    # lam goc de dung `kenh` (roi truyen NGUYEN chuoi ay qua `KENH_ENV`), va lam
    # `cwd` cua con. Voi mot duong TUONG DOI `r` va cwd cha `P`, con chay tai
    # `P/r` nhung duoc bao mo `r/.ket-qua-N.jsonl` => duong hieu luc thanh
    # `P/r/r/...`. Con hong ngay khi mo kenh, ca HAI lan thu lap dung sai dia chi
    # do. Do duoc (cross-review luot 13, HUONG 6): cung mot thu muc VAT LY, chi
    # doi cach viet doi so — tuyet doi GIET lan 1, tuong doi KHONG DO DUOC ca 2
    # lan. Bo doc tu choi kenh vang la DUNG; loi la o launcher tu lam hong phep
    # do voi mot doi so `Path` hoan toan hop le.
    # Chuan hoa MOT LAN roi dung CUNG gia tri cho ca hai cho — bat bien can giu
    # la "mot he quy chieu", khong phai "duong phai tuyet doi".
    # Chon `resolve()`: no vua tuyet doi hoa vua go symlink, nen `kenh` va `cwd`
    # tro cung mot inode ke ca khi nguoi goi dua symlink. Duong CHUA TON TAI van
    # duoc chap nhan (`strict=False` mac dinh) va se hong o buoc phong con voi
    # dung loi that, chu khong bi bien thanh mot dia chi khac ngoai y dinh.
    ban_sao = Path(ban_sao).resolve()
    # F04 (luot 11) — vat hoa TRUOC vong: neu `dich` la iterator thi lan thu 1
    # tieu thu no va lan thu 2 nhin thay RONG, tuc hai lan thu do HAI thu khac
    # nhau. Chot nay khac chot trong `doc_kenh` (xem o do) — moi chot che mot
    # duong vao, khong cai nao thay cai nao.
    dich = tuple(dich)
    trang_thai = ly_do = None
    for lan_thu in (1, 2):
        dau_phien = sinh_dau_phien()          # M7: SINH MOI moi luot
        kenh = ban_sao / f".ket-qua-{lan_thu}.jsonl"
        env = dict(os.environ,
                   NHANH_DON_DUOC_KHONG_DOT_BIEN="1", PYTHONDONTWRITEBYTECODE="1",
                   KENH_ENV_PLACEHOLDER="")
        env[KENH_ENV] = str(kenh)
        env[DAU_PHIEN_ENV] = dau_phien
        env[MUTANT_ENV] = ten
        env[LAN_THU_ENV] = str(lan_thu)
        env.pop("KENH_ENV_PLACEHOLDER", None)
        # F03 (luot 10, phat sinh khi vá F01) — `dict(os.environ, ...)` KE THUA
        # ca `NHANH_DON_DUOC_CHI_TU_KIEM`, ma `main` kiem co AY TRUOC TIEN. Nen
        # khi `chay_dot_bien` duoc goi tu BEN TRONG mot con tu-kiem, con chau sinh
        # ra lai chay tu kiem thay vi 8 ca T — tuc goi lai chinh duong da goi no.
        # DO DUOC: 526 tien trinh `ban_sao_*` con song, bo kiem bi OOM giet o phut
        # thu 12 (nen chay tron 112 s). Con nay PHAI o che do mutant, khong duoc
        # de moi truong cua cha quyet dinh — cung nep voi `env.pop(KENH_ENV)` ma
        # `chay_dot_bien_tu_kiem` da lam cho chieu nguoc lai.
        env.pop("NHANH_DON_DUOC_CHI_TU_KIEM", None)
        # F02 (luot 10) — vo fail-close cua `doc_kenh` chi chay SAU khi `run`
        # tra ve. `subprocess.run` ném `OSError` ngay luc tao pipe/phong con
        # (vd EMFILE), va `check=False` KHONG bien ngoai le khoi chay thanh
        # `CompletedProcess` — nen loi ay THOAT khoi vong `(1, 2)` va lam MAT
        # lan thu hai, dung nghia vu M3 ma duong doc kenh da lam. Do duoc
        # (cross-review luot 10, HUONG 8): ha `RLIMIT_NOFILE` quanh lan phong
        # dau ⇒ `[Errno 24]` thoat ra, nhat ky chi `[1]`; tra lai tai nguyen
        # thi cung mutant GIET binh thuong.
        # Bat HEP o dung loi khoi chay: khong dung `except Exception` (se nuot
        # ca loi lap trinh), va KHONG cham `p.returncode` khi `p` chua ton tai.
        try:
            p = run([sys.executable, Path(__file__).name], ban_sao, check=False, env=env)
        except (OSError, ValueError, UnicodeError) as exc:
            # F06 (luot 11) — `OSError` mot minh KHONG du. `subprocess.run` nem
            # `ValueError` (byte NUL trong gia tri env) va `UnicodeEncodeError`
            # (surrogate) NGAY LUC PHONG, va ca hai deu KHONG phai `OSError` nen
            # van thoat khoi vong `(1, 2)`. Do duoc o luot 11. Van bat HEP theo
            # loai — khong dung `except Exception`, de loi lap trinh con noi ra.
            _ghi_ha_tang(exc)                     # r2 M1 diem nuot: chay_mot_mutant
            trang_thai = KHONG_DO_DUOC
            ly_do = f"khong phong duoc tien trinh con: {type(exc).__name__}: {exc}"
            continue
        trang_thai, ly_do = doc_kenh(kenh, dau_phien, ten, lan_thu, dich, p.returncode)
        if trang_thai == KHONG_DO_DUOC:
            # F09 — giu chi tiet ngoai le, khong chi giu ten ca: chinh chi tiet ay
            # la du kien can de chan doan "khong do duoc" o lan thu hai.
            ly_do = (f"{ly_do} | rc_con={p.returncode} | "
                     f"stderr[-{TRAN_DUOI_STDERR}:]={p.stderr[-TRAN_DUOI_STDERR:]!r}"
                     + _khai_cat_dau_stderr(p.stderr))
        if trang_thai != KHONG_DO_DUOC:
            return trang_thai, ly_do, lan_thu
    return trang_thai, ly_do, 2
# ---- M5: ca TU KIEM cho CHINH bo cham ---------------------------------------
# Khong co nhung ca nay thi bo cham la thu DUY NHAT trong tep khong ai canh.
# Moi ca duoi day phai co MOT dot bien rieng lam DUNG no do — ca khong doi mau
# theo dot bien duoc chi dinh thi KHONG duoc tinh vao so nhom cua A6.
def _kenh_tam(dong_list, thu_muc: Path, ten="k.jsonl") -> Path:
    d = thu_muc / ten
    d.write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in dong_list), encoding="utf-8")
    return d


def _ban_ghi(dau_phien, mutant="m", lan_thu=1, **kw):
    return dict(dau_phien=dau_phien, mutant=mutant, lan_thu=lan_thu, **kw)


def _du_ca(dau_phien, nhan_theo_ca, **kw):
    return [_ban_ghi(dau_phien, ca=t, nhan=nhan_theo_ca.get(t, NHAN_DAT), **kw) for t, _ in CA]


# ---- L1 (luot 2): do CHINH duong ra quyet dinh, khong do BAN SAO -------------
# Ba ca cu (`r504` bo dem rieng, `r501` khoi `except` rieng, `r506` chi AST) deu
# do mot BAN SAO logic dung trong than ca, nen dot bien vao SAN PHAM song sot:
# do duoc `counter-fold`, `final-gate-open`, `exception-broad`, `src-signing-
# unreachable` — bon con, cung mot goc. Hai cong cu duoi day cho ca goi THANG
# vao `main()` / `chay_dot_bien()` / `chay_ca()` that.
def _nap_ban_sao(d: Path):
    """Nap BAN SAO cua CHINH tep nay lam module RIENG (ten ngau nhien).

    Ten ngau nhien la CO Y: hai ban sao cung kich thuoc ghi trong CUNG mot giay
    se dung `.pyc` cua nhau — bai hoc da tra gia cua kho (mutant chua tung chay).
    """
    d.mkdir(parents=True, exist_ok=True)
    ten = f"ban_sao_{secrets.token_hex(8)}"
    tep = d / f"{ten}.py"
    tep.write_text(Path(__file__).read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    shutil.copy2(TOOL, d / TOOL.name)
    spec = importlib.util.spec_from_file_location(ten, tep)
    if not (spec and spec.loader):
        raise AssertionError("khong nap duoc ban sao")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[ten] = mod
    spec.loader.exec_module(mod)
    return mod


@contextlib.contextmanager
def _git_config_sach():
    """Trung hoa cau hinh git global/system trong mot khoi.

    Nho vay `commit.gpgsign=false` doc duoc tren kho THAT chi co the den TU chinh
    san pham, khong phai tu may dang chay — va ca do KHONG con phu thuoc may.
    """
    luu = {k: os.environ.get(k) for k in ("GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM")}
    os.environ["GIT_CONFIG_GLOBAL"] = os.devnull
    os.environ["GIT_CONFIG_SYSTEM"] = os.devnull
    try:
        yield
    finally:
        for k, v in luu.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)


@contextlib.contextmanager
def _moi_truong(**cap):
    """Dat/xoa bien moi truong trong mot khoi roi tra NGUYEN trang thai cu."""
    luu = {k: os.environ.get(k) for k in cap}
    for k, v in cap.items():
        os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
    try:
        yield
    finally:
        for k, v in luu.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)


def _chay_main_gia(d: Path, dat, kgiet, kdo, tu_kiem_do=(), tk_giet=None, tk_hong=0,
                   bo_khoi_nhom=(), bo_khoi_tu_kiem=(), bo_khoi_dich=()):
    """Chay CHINH `main()` cua mot ban sao; chi cac ham THU THAP bi thay bang do
    gia, con BA DIEU KIEN CONG van la cua san pham. Tra `(rc, dong in)` — dong in
    can de chan kieu hong am tham nhat: IN mot dang, QUYET DINH mot dang khac."""
    m = _nap_ban_sao(d)
    m.chay_ca = lambda khung=None: []
    m.chay_dot_bien = lambda: (dat, kgiet, kdo)
    m.chay_tu_kiem = lambda: list(tu_kiem_do)
    # F03 (luot 3) — `tk_giet` phai dat DOC LAP voi `tk_hong`: do gia cu luon bu
    # tong (`len - tk_hong`) nen `tk_giet` chua bao gio la mot bien, va mot bo tra
    # `(0, 0)` khong kich duoc cong nao. Do duoc: `main-ignore-self-kills` SONG SOT
    # full voi dong in `dot bien giet 0/23`.
    tkg = len(m.DOT_BIEN_TU_KIEM) - tk_hong if tk_giet is None else tk_giet
    m.chay_dot_bien_tu_kiem = lambda: (tkg, tk_hong, 0)
    # F03 — ba cach lam `thieu`/san khac nhau, moi cach CHI cham MOT ve:
    #   · `bo_khoi_tu_kiem` -> chi (NHOM - da_chay)
    #   · `bo_khoi_dich`    -> chi (NHOM - nhom_co_dot_bien)
    #   · `bo_khoi_nhom`    -> chi `len(NHOM_BAT_BUOC) < SAN_NHOM`, va do HANG SAN
    #     THAT chu khong tu dat lai no. Kich ban cu `nhom_them` pha CA HAI ve cua
    #     `thieu`, con `san_cong` tu gan lai `SAN_NHOM` nen `lower-floor` song sot.
    if bo_khoi_tu_kiem:
        m.TU_KIEM = [x for x in m.TU_KIEM if x[0] not in set(bo_khoi_tu_kiem)]
    if bo_khoi_dich:
        bo = set(bo_khoi_dich)
        m.DOT_BIEN_TU_KIEM = [(t, tuple(c for c in dch if c not in bo), a, b)
                              for t, dch, a, b in m.DOT_BIEN_TU_KIEM]
    if bo_khoi_nhom:
        m.NHOM_BAT_BUOC = m.NHOM_BAT_BUOC - set(bo_khoi_nhom)
    with _moi_truong(**{KENH_ENV: None, "NHANH_DON_DUOC_CHI_TU_KIEM": None,
                        "NHANH_DON_DUOC_KHONG_DOT_BIEN": None}):
        ra = io.StringIO()
        with contextlib.redirect_stdout(ra):
            rc = m.main()
    return rc, ra.getvalue()


# Tien trinh con THAT cho `r512`: mot lan chay cap DONG THOI stdout, rc va kenh
# cho chinh `chay_mot_mutant`. Do gia trong bo nho khong co RANH GIOI TIEN TRINH,
# ma lo hong A5b nam dung o ranh gioi ay.
_KICH_CON = '''import json, os, sys
CA = %r
if os.environ.get("IN_GIA_MAO"):
    print("CASE T1: DO - gia mao qua stdout")
if os.environ.get("IN_NHIEU"):
    print("CASE T99: DO - nhieu NGOAI dich")
ph = os.environ["NHANH_DON_DUOC_DAU_PHIEN"]
mu = os.environ["NHANH_DON_DUOC_MUTANT"]
lan = int(os.environ["NHANH_DON_DUOC_LAN_THU"])
do = os.environ.get("CA_DO", "")
rc = 1 if do else 0
with open(os.environ["NHANH_DON_DUOC_KENH"], "a", encoding="utf-8") as k:
    for c in CA:
        k.write(json.dumps({"ca": c, "dau_phien": ph, "mutant": mu, "lan_thu": lan,
                            "nhan": "DO_CHOT" if c == do else "DAT"}, sort_keys=True) + "\\n")
    k.write(json.dumps({"dau_phien": ph, "mutant": mu, "lan_thu": lan,
                        "dong_luot": True, "rc": rc}, sort_keys=True) + "\\n")
sys.exit(rc)
'''


def _kich_con(d: Path, ten: str) -> Path:
    bs = d / ten
    bs.mkdir(parents=True, exist_ok=True)
    (bs / Path(__file__).name).write_text(_KICH_CON % [t for t, _ in CA],
                                          encoding="utf-8", newline="\n")
    return bs


def r501_tin_hieu_chot_khong_gia_mao_duoc(d: Path):
    """A1 — ca NGOAI dich do bang duong HA TANG => KHONG DO DUOC, khong phai GIET.

    F02 (luot 2) — ca nay phai goi CHINH `chay_ca`, VA loi phai di vao qua `run()`.
    Ban truoc tu vong `CA` roi tu viet mot khoi `except` RIENG, tuc no do mot BAN
    SAO cua phep phan loai: doi lop bat cua runner THAT tu `except TinHieuChotCa`
    sang `except AssertionError` KHONG lam no do — do duoc, `exception-broad`
    SONG SOT full.

    Rut `CA` con HAI ca la de giu thoi gian (ca nay chay lai trong TUNG dot bien
    tu kiem; tron ven 8 ca ton 1,38s so voi 0,38s). Ca hai nhanh phan loai can
    canh deu duoc di qua: `T7` chet bang `AssertionError` TRAN tu `run`, `T2`
    chay sach. `doc_kenh` doc `CA` ngay luc goi nen phai goi TRONG cung khoi.
    """
    ph = sinh_dau_phien()
    k = d / "k.jsonl"

    class KhungTheoDoi(KhungPhat):
        def vao_ca(self, ten):
            globals()["_CA_HIEN_TAI"] = ten
            super().vao_ca(ten)

    kh = KhungTheoDoi(k, ph, "m", 1)
    that_run = globals()["run"]

    def run_gia(args, cwd, check=True, env=None):
        # F02 (luot 3) — KHONG tu nem. Ban truoc `run_gia` tu `raise
        # AssertionError`, nen ca KHONG di qua `run` that va doi lop nem CUA `run`
        # (AssertionError -> TinHieuChotCa) van xanh: do duoc, `run-infra-as-signal`
        # SONG SOT full. Nay bat CHINH `run` that bai voi `check=True`, de ngoai le
        # sinh ra TU dong `raise` cua san pham.
        if globals().get("_CA_HIEN_TAI") == "T7":
            return that_run(["git", "rev-parse", "--verify", "khong-ton-tai-xxx"],
                            cwd, check=True)
        return that_run(args, cwd, check=check, env=env)

    goc_ca = list(CA)
    try:
        globals()["run"] = run_gia
        globals()["CA"] = [c for c in goc_ca if c[0] in ("T2", "T7")]
        with contextlib.redirect_stdout(io.StringIO()):
            do = chay_ca(kh)
        kh.dong_luot(1)
        tt, ly_do = doc_kenh(k, ph, "m", 1, ("T2",), 1)
    finally:
        globals()["run"] = that_run
        globals()["CA"] = goc_ca
        globals().pop("_CA_HIEN_TAI", None)
    chot(do == ["T7"], "r501")
    chot(tt == KHONG_DO_DUOC and "T7" in ly_do, "r501")


def r502_assert_ha_tang_khong_duoc_cap_lop_chot(d: Path):
    """A1b — HAI assert ha tang phai o NGUYEN ngoai lop tin hieu."""
    import ast as _ast
    cay = _ast.parse(Path(__file__).read_text(encoding="utf-8"))
    ten_ca = {t for t, _ in CA}
    ha_tang = {}
    for fn in cay.body:
        if isinstance(fn, _ast.FunctionDef) and fn.name not in ten_ca:
            n = sum(1 for x in _ast.walk(fn) if isinstance(x, _ast.Assert))
            if n:
                ha_tang[fn.name] = n
    chot(ha_tang == {"nap_tool": 1, "chay_dot_bien": 1}, "r502")
    trong_ca = sum(sum(1 for x in _ast.walk(fn) if isinstance(x, _ast.Assert))
                   for fn in cay.body
                   if isinstance(fn, _ast.FunctionDef) and fn.name in ten_ca)
    chot(trong_ca == 0, "r502")
    # F02 (luot 3) — AST chi dem HINH DANG. Mot boc
    #   try: assert ...
    #   except AssertionError as e: raise TinHieuChotCa(str(e))
    # GIU NGUYEN so node Assert ma doi HAN lop nem, nen ca cu mu: do duoc,
    # `nap-wrap-infra` va `archive-wrap-infra` SONG SOT full. Phai EP hai assert
    # ay hong THAT va doi lop nem van la `AssertionError` TRAN.
    m = _nap_ban_sao(d / "nap")
    khong_py = d / "khong-phai-python.txt"
    khong_py.write_text("x", encoding="utf-8")
    m.TOOL = khong_py                      # spec_from_file_location -> None
    # F02 (luot 4) — phai so DANH TINH LOP, khong so TEN. Ban truoc luu
    # `type(exc).__name__` roi so chuoi "AssertionError", nen mot lop
    # `type("AssertionError", (TinHieuChotCa,), {})` — TRUNG TEN ma la tin hieu
    # chot — di qua sach. Cung benh voi `endswith` gia mao danh tinh va voi danh
    # sach cam "phan biet CACH VIET chu khong phan biet THAM QUYEN".
    loai = []
    try:
        m.nap_tool()
    except Exception as exc:
        loai.append(type(exc))
    chot(loai == [AssertionError], "r502")

    class _SubGia:
        PIPE = subprocess.PIPE
        run = staticmethod(subprocess.run)

        @staticmethod
        def Popen(*a, **k):
            class _P:
                stdout = None

                def wait(self):
                    return 0
            return _P()

    m2 = _nap_ban_sao(d / "archive")
    m2.subprocess = _SubGia                # archive.stdout is None -> assert hong
    loai2 = []
    try:
        with _git_config_sach(), contextlib.redirect_stdout(io.StringIO()):
            m2.chay_dot_bien()
    except Exception as exc:
        loai2.append(type(exc))
    chot(loai2 == [AssertionError], "r502")


def r503_chot_cua_ca_KHAC_khong_tinh_la_giet(d: Path):
    """A2 — ca ngoai dich do bang TinHieuChotCa THAT => KHONG GIET (khong phai
    KHONG DO DUOC): day la tin hieu that cua mot ca khac."""
    ph = sinh_dau_phien()
    k = _kenh_tam(_du_ca(ph, {"T1": NHAN_DO_CHOT, "T7": NHAN_DO_CHOT})
                  + [_ban_ghi(ph, dong_luot=True, rc=1)], d)
    tt, _ = doc_kenh(k, ph, "m", 1, ("T1",))
    chot(tt == KHONG_GIET, "r503")


def r504_ba_trang_thai_khong_gop(d: Path):
    """A3 — ba trang thai ton tai RIENG BIET, khong gop."""
    ph = sinh_dau_phien()
    giet = _kenh_tam(_du_ca(ph, {"T1": NHAN_DO_CHOT}) + [_ban_ghi(ph, dong_luot=True, rc=1)], d, "g.jsonl")
    kgiet = _kenh_tam(_du_ca(ph, {}) + [_ban_ghi(ph, dong_luot=True, rc=0)], d, "n.jsonl")
    kdo = _kenh_tam(_du_ca(ph, {"T1": NHAN_DO_KHAC}) + [_ban_ghi(ph, dong_luot=True, rc=1)], d, "x.jsonl")
    ra = {doc_kenh(giet, ph, "m", 1, ("T1",))[0],
          doc_kenh(kgiet, ph, "m", 1, ("T1",))[0],
          doc_kenh(kdo, ph, "m", 1, ("T1",))[0]}
    chot(ra == {GIET, KHONG_GIET, KHONG_DO_DUOC}, "r504")
    # F07 — so tap nhan KHONG do bo dem. Suite that thuong chi di qua 10 GIET, nen
    # cong nham hai loai con lai khong ai thay. Do TUNG SO HANG tren ba ket qua that.
    dem = {GIET: 0, KHONG_GIET: 0, KHONG_DO_DUOC: 0}
    for kenh in (giet, kgiet, kdo):
        dem[doc_kenh(kenh, ph, "m", 1, ("T1",))[0]] += 1
    chot(dem[GIET] == 1 and dem[KHONG_GIET] == 1 and dem[KHONG_DO_DUOC] == 1
         and sum(dem.values()) == 3, "r504")


def _run_gia(nhat_ky, ket_theo_lan, stdout=""):
    """Do gia GIU TRANG THAI: ghi kenh THAT theo kich ban tung lan, ghi nhat ky goi."""
    that = globals()["run"]

    def gia(args, cwd, check=True, env=None):
        rc = 0
        if env and KENH_ENV in env:
            lan = env[LAN_THU_ENV]
            nhat_ky.append(lan)
            dong = ket_theo_lan(env[DAU_PHIEN_ENV], env[MUTANT_ENV], int(lan))
            Path(env[KENH_ENV]).write_text(
                "".join(json.dumps(x, sort_keys=True) + "\n" for x in dong), encoding="utf-8")
            # F05 (luot 2) — do gia phai TRA rc KHOP voi kenh, y nhu tien trinh
            # that. Rc LUON 0 thi moi dot bien gai dieu kien o `p.returncode`
            # deu thoat sach (do duoc: `stdout-rc1` song sot tron ven).
            for r in dong:
                if r.get("dong_luot") and isinstance(r.get("rc"), int):
                    rc = r["rc"]
        p = that(["git", "--version"], cwd, check=False)
        p.stdout = stdout
        p.returncode = rc
        return p

    return that, gia


def r505_chay_lai_dung_mot_lan(d: Path):
    """A4 — dem SO LAN GOI, khong doc ma thoat. Do gia GIU TRANG THAI."""
    nhat_ky = []
    that = globals()["run"]

    def gia(args, cwd, check=True, env=None):
        if env and KENH_ENV in env:
            nhat_ky.append(env[LAN_THU_ENV])
            Path(env[KENH_ENV]).write_text("", encoding="utf-8")   # luon KHONG DO DUOC
        return that(["git", "--version"], cwd, check=False)

    globals()["run"] = gia
    try:
        tt, _, so_lan = chay_mot_mutant(d, "m", ("T1",))
    finally:
        globals()["run"] = that
    chot(tt == KHONG_DO_DUOC and nhat_ky == ["1", "2"] and so_lan == 2, "r505")
    # F03 — kich ban thu HAI cua A4, truoc day THIEU: lan 1 khong do duoc, lan 2 GIET.
    nk2 = []
    def kb(ph, mu, lan):
        if lan == 1:
            return []                                   # kenh rong => KHONG DO DUOC
        return (_du_ca(ph, {"T1": NHAN_DO_CHOT}, mutant=mu, lan_thu=lan)
                + [_ban_ghi(ph, mutant=mu, lan_thu=lan, dong_luot=True, rc=0)])
    that2, gia2 = _run_gia(nk2, kb)
    globals()["run"] = gia2
    try:
        tt2, _, so_lan2 = chay_mot_mutant(d, "m", ("T1",))
    finally:
        globals()["run"] = that2
    chot(tt2 == GIET and nk2 == ["1", "2"] and so_lan2 == 2, "r505")
    # F06 (luot 3) — KHONG GIET cung la trang thai TERMINAL: phai DUNG o lan 1.
    # Ban truoc chi do KDD->KDD va KDD->GIET, nen doi dieu kien dung tu
    # `!= KHONG_DO_DUOC` sang `== GIET` van xanh — ma doi ay CAP TIN DUNG: mot
    # ket qua KHONG GIET o lan 1 se thanh GIET o lan 2. Do duoc:
    # `retry-ignore-status` SONG SOT full.
    nk3 = []

    def kb_kg_roi_giet(ph, mu, lan):
        nhan = {} if lan == 1 else {"T1": NHAN_DO_CHOT}
        return (_du_ca(ph, nhan, mutant=mu, lan_thu=lan)
                + [_ban_ghi(ph, mutant=mu, lan_thu=lan, dong_luot=True, rc=1 if nhan else 0)])

    that3, gia3 = _run_gia(nk3, kb_kg_roi_giet)
    globals()["run"] = gia3
    try:
        tt3, _, so_lan3 = chay_mot_mutant(d, "m", ("T1",))
    finally:
        globals()["run"] = that3
    chot(tt3 == KHONG_GIET and nk3 == ["1"] and so_lan3 == 1, "r505")
    # F05 (luot 4) — va GIET cung la terminal: phai dung NGAY lan 1. Thieu ca nay
    # thi doi dieu kien dung thanh `== KHONG_GIET` van xanh, ma doi ay LAM MAT
    # TIN DUNG: mot ket luan GIET hop le bi mot loi vo can o lan 2 thay bang KDD
    # — dung chieu hong ma packet nay sinh ra de chan.
    nk4 = []

    def kb_giet_ngay(ph, mu, lan):
        if lan == 1:
            return (_du_ca(ph, {"T1": NHAN_DO_CHOT}, mutant=mu, lan_thu=lan)
                    + [_ban_ghi(ph, mutant=mu, lan_thu=lan, dong_luot=True, rc=1)])
        return []                                   # lan 2 (neu bi goi) => KDD

    that4, gia4 = _run_gia(nk4, kb_giet_ngay)
    globals()["run"] = gia4
    try:
        tt4, _, so_lan4 = chay_mot_mutant(d, "m", ("T1",))
    finally:
        globals()["run"] = that4
    chot(tt4 == GIET and nk4 == ["1"] and so_lan4 == 1, "r505")
    # F03 (luot 5) — lan HAI truoc day chi co GIET hoac KHONG DO DUOC. Thieu o
    # KDD -> KHONG GIET, nen mot duong "chuan hoa lan 2: KHONG GIET thanh GIET"
    # di qua sach: do duoc, `retry-normalize-second-kg` SONG SOT quick. Day dung
    # la TIN DUNG GIA — mutant khong giet dich van duoc ghi cong GIET.
    nk5 = []

    def kb_kdd_roi_kg(ph, mu, lan):
        if lan == 1:
            return []                               # lan 1 KHONG DO DUOC
        return (_du_ca(ph, {"T2": NHAN_DO_CHOT}, mutant=mu, lan_thu=lan)
                + [_ban_ghi(ph, mutant=mu, lan_thu=lan, dong_luot=True, rc=1)])

    that5, gia5 = _run_gia(nk5, kb_kdd_roi_kg)
    globals()["run"] = gia5
    try:
        tt5, _, so_lan5 = chay_mot_mutant(d, "m", ("T1",))
    finally:
        globals()["run"] = that5
    chot(tt5 == KHONG_GIET and nk5 == ["1", "2"] and so_lan5 == 2, "r505")


def r506_moi_kho_deu_tat_ky_commit(d: Path):
    """A5 — CA HAI kho bo test dung deu tat ky. Hai dot bien rieng, khong gop."""
    # Dung AST chu KHONG dem chuoi: mot phep dem chuoi se tu khop chinh no trong
    # than ca nay (do duoc: dem ra 3 thay vi 2) — ca xanh/do vi ly do vo can.
    import ast as _ast
    cay = _ast.parse(Path(__file__).read_text(encoding="utf-8"))
    kho_tat_ky = set()
    for fn in cay.body:
        if not isinstance(fn, _ast.FunctionDef):
            continue
        for n in _ast.walk(fn):
            if not (isinstance(n, _ast.Call) and getattr(n.func, "id", "") == "run"):
                continue
            if not (n.args and isinstance(n.args[0], _ast.List)):
                continue
            phan = [x.value for x in n.args[0].elts if isinstance(x, _ast.Constant)]
            if phan[:3] == ["git", "config", "commit.gpgsign"] and phan[3:4] == ["false"]:
                kho_tat_ky.add(fn.name)
    chot(kho_tat_ky == {"kho_bare", "chay_dot_bien"}, "r506")
    # F04 — AST chi chung minh LENH CO MAT; dat no trong `if False:` van qua.
    # Phai DOC cau hinh cua kho THAT da duoc dung len.
    with _git_config_sach():
        td, _, work = kho_bare()
        try:
            ra = run(["git", "config", "--get", "commit.gpgsign"], work, check=False)
            chot(ra.stdout.strip() == "false", "r506")
        finally:
            td.cleanup()
    # F04 (luot 2) — kho `src` cua vong mutant van chi duoc cong nhan qua AST, nen
    # dat CHINH dong ay trong `if False:` van qua: do duoc, `src-signing-
    # unreachable` SONG SOT full thuong. Phai DOC cau hinh cua `src` THAT, tren
    # duong ma san pham dung no len. Trung hoa global/system de chuoi "false"
    # chi co the den TU san pham chu khong tu may dang chay.
    m = _nap_ban_sao(d / "src")
    m.DOT_BIEN = m.DOT_BIEN[:1]
    doc = []

    def bat_src(ban_sao, ten, dich):
        nguon = Path(ban_sao).parent / "source"
        doc.append(m.run(["git", "config", "--get", "commit.gpgsign"], nguon,
                         check=False).stdout.strip())
        return (m.GIET, "", 1)

    m.chay_mot_mutant = bat_src
    with _git_config_sach(), contextlib.redirect_stdout(io.StringIO()):
        m.chay_dot_bien()
    chot(doc == ["false"], "r506")


def r507_kenh_ket_qua_ba_bien(d: Path):
    """A5b — ba bien cua kenh: dong TRUNG · thieu dong · dong cua ca KHONG ton tai."""
    ph = sinh_dau_phien()
    dong = [_ban_ghi(ph, dong_luot=True, rc=1)]
    trung = _kenh_tam(_du_ca(ph, {}) + [_ban_ghi(ph, ca="T1", nhan=NHAN_DAT)] + dong, d, "a.jsonl")
    thieu = _kenh_tam(_du_ca(ph, {})[:-1] + dong, d, "b.jsonl")
    ca_la = _kenh_tam(_du_ca(ph, {}) + [_ban_ghi(ph, ca="T99", nhan=NHAN_DAT)] + dong, d, "c.jsonl")
    for k in (trung, thieu, ca_la):
        tt, _ = doc_kenh(k, ph, "m", 1, ("T1",))
        chot(tt == KHONG_DO_DUOC, "r507")


def r508_ban_ghi_luot_TRUOC_chi_khac_dau_phien(d: Path):
    """A5c(1) — ban ghi hop le MOI MAT KHAC, chi khac DAU PHIEN => KHONG DO DUOC.

    Dau phien phai la bien DUY NHAT: neu ban ghi cay vao mang ten mutant cua luot
    TRUOC thi chot so ten mutant da bac no roi, nen go chot dau phien KHONG doi mau
    gi va ca tro thanh xanh-vo-nghia.
    """
    # #593 M1 — TIEN DE, khong phai thu ca nay do. Xem `_hai_dau_phien_phan_biet`.
    try:
        ph_that, ph_khac = _hai_dau_phien_phan_biet()
    except TinHieuKhongDoDuoc as e:
        # DO DUOC o luot chay dau, va no la MOT KHUYET TAT CUA CHINH BAN VA NAY:
        # hai dot bien CO SAN — `dau-phien-thanh-moc-giay` va (moi) ha tran xuong
        # 0 — lam bo sinh SUY BIEN, `TinHieuKhongDoDuoc` thoat ra, va bo phan hang
        # xep no vao DO_KHAC = "chet vi loi VO CAN" = TIN DUNG GIA. Tuc ban va
        # chong chap lai SINH ra dung hinh dang ma packet nay di chua.
        #
        # Phan biet phai giu cho ro: tran CAN co HAI nghia khac han.
        #   · Duoi mot bo sinh NGAU NHIEN NHUNG HEP (khong gian 256, tuc dot bien
        #     `entropy-giu-mot-byte`) tran KHONG BAO GIO can — (1/256)^64.
        #   · Tran chi can khi bo sinh SUY BIEN (hang, hoac moc giay). Do khong
        #     phai "toi khong do duoc" ma la CHINH phat hien r508 phai bao: mot bo
        #     sinh khong cho noi hai dau phan biet la mot bo sinh HONG.
        # Nen o DAY no phai ra DO_CHOT — chot cua CHINH ca nay.
        #
        # Trang thai THU BA van ton tai va van do duoc: no song o HOP DONG cua
        # `_hai_dau_phien_phan_biet`, va `r527` do thang no. Cai bi cam la de no
        # THOAT RA khoi r508 thanh mot loi vo can.
        raise TinHieuChotCa(f"chot cua ca r508 that bai: bo sinh SUY BIEN — {e}") from None
    k = _kenh_tam(_du_ca(ph_khac, {"T1": NHAN_DO_CHOT})
                  + [_ban_ghi(ph_khac, dong_luot=True, rc=1)], d)
    # #593 — `doc_kenh` doi LOI DOC thanh KHONG DO DUOC, dung gia tri ca nay cho: 2000
    # loi doc tung ra r528 DAT (lam tron LEN). Chot DUNG ly do bac; loi doc thi `doc_kenh`
    # GHI vao so ha tang va runner doi nhan (r2 M1/M3) — khong con buoc doc thu (r2 M4).
    tt, ly = doc_kenh(k, ph_that, "m", 1, ("T1",))
    chot(tt == KHONG_DO_DUOC and ly.startswith("ban ghi khong neo dung luot"), "r508")


def r509_dau_phien_phai_sinh_moi_moi_luot(d: Path):
    """A5c(1b) — do BO SINH, khac ca r508 von do PHEP SO.

    Ghim nguon clock: hai lan sinh trong CUNG mot tick van phai cho hai dau KHAC.
    Va dem SO LAN GOI nguon ngau nhien = so luot — dot bien "bo dem tang" cho moi
    dau KHAC nhau nen phep so "hai dau khac nhau" mu voi no.
    """
    import time as _t
    moc = _t.time
    _t.time = lambda: 1_700_000_000.0          # clock GHIM o mot tick
    dem = {"n": 0}
    that = secrets.token_hex

    def dem_goi(n=None):
        dem["n"] += 1
        return that(n) if n is not None else that()

    secrets.token_hex = dem_goi
    try:
        a, b = sinh_dau_phien(), sinh_dau_phien()
    finally:
        secrets.token_hex = that
        _t.time = moc
    # `len(a) >= 32` la rang buoc BIEU DIEN, khong phai rang buoc entropy: no bac
    # ca Base64 cua du 16 byte ngau nhien (24 ky tu). Da BO — cung ho voi chot
    # `goc_hex in dau_ra` da bo o luot 4. Chi doi hai dau KHAC nhau va nguon duoc
    # goi DU so luot; phep vi sai 128 bit ben duoi moi la thu do entropy.
    chot(a != b and dem["n"] == 2, "r509")
    # F06 (luot 2) — fixture phai GIU NGU NGHIA THAM SO. Ban truoc dung
    # `lambda n=None: moc_hex`, tra 32 ky tu hex BAT KE n, nen mot bo sinh xin
    # `token_hex(0)` roi ghep bo dem van qua sach: do duoc, `zero-entropy-counter`
    # SONG SOT quick 12/12. Nay do HAI dieu: xin bao nhieu BYTE, va dau ra co
    # PHAI CHINH entropy ay khong.
    # F06 (luot 2) doi fixture giu ngu nghia tham so; F04 (luot 3) cho thay the
    # VAN CHUA DU theo HAI huong nguoc nhau:
    #   · chuoi LAP ("ab"*16) khong phan biet "giu 16 byte" voi "giu 1 byte roi
    #     lap 16 lan" — do duoc, `entropy-last-byte` SONG SOT full;
    #   · chot `e == "ab"*16` lai QUA CHAT: no bac ca mot tien to hop le
    #     ("session-" + token_hex(16)) von giu nguyen entropy.
    # Nen nay do PHU THUOC VI SAI theo TUNG BYTE: doi rieng byte DAU, roi rieng
    # byte CUOI, dau ra deu phai doi — cong voi doi hoi entropy co MAT trong dau ra.
    xin = []

    # F02 (luot 6) — ca cu chi dem `secrets.token_hex`, nen mot trien khai dung
    # `secrets.token_bytes(16).hex()` hay `os.urandom(16).hex()` — A5c(1b) CHO
    # PHEP ca `secrets` lan `os.urandom` — bi bac OAN (do duoc: ca hai lam r509
    # do). Day la lan THU BA ca nay rang buoc CACH TRIEN KHAI thay vi THUOC TINH
    # (truoc do: `goc_hex in dau_ra`, roi `len(a) >= 32`). Nen nay bom CA BA API
    # va dem TONG so byte duoc xin qua bat ky duong nao.
    that_bytes, that_urandom = secrets.token_bytes, os.urandom

    def _bom_nguon(gia_tri_hex):
        b = bytes.fromhex(gia_tri_hex)

        def f_hex(n=None):
            xin.append(16 if n is None else n)
            return gia_tri_hex

        def f_bytes(n=None):
            xin.append(16 if n is None else n)
            return b

        def f_urandom(n):
            xin.append(n)
            return b

        secrets.token_hex, secrets.token_bytes, os.urandom = f_hex, f_bytes, f_urandom

    def _tra_nguon():
        secrets.token_hex, secrets.token_bytes, os.urandom = that, that_bytes, that_urandom

    def nguon(gia_tri):
        def f(n=None):
            xin.append(n)
            return gia_tri
        return f

    # F06 (luot 4) — hai sua, nguoc chieu nhau:
    #  · vi sai chi o byte DAU va byte CUOI la phu MOT DIEM tren moi dau mut, bo
    #    trong 14 byte GIUA. Te hon: fixture cu toan byte < 128 nen mot bo sinh
    #    XOA BIT CAO cua 14 byte giua tra NGUYEN chuoi cu va qua sach. Nay lat
    #    bit cao cua TUNG byte — 16 doi chung, khong phai 2.
    #  · `goc_hex in dau_ra` la rang buoc BIEU DIEN ma dac ta KHONG doi: no bac
    #    ca mot bo sinh bam SHA256 tu du 16 byte entropy that. Da BO.
    def _sinh_voi(v):
        xin.clear()
        _bom_nguon(v)
        try:
            return sinh_dau_phien()
        finally:
            _tra_nguon()

    # F04 (luot 5) — lat rieng BIT CAO cua tung byte moi la 16 doi chung, tuc do
    # DUNG 16 bit trong 128: mot bo sinh giu `x & 0x80` van tao 16 dau ra khac
    # nhau va qua sach (do duoc: SONG SOT quick), dau chi con 16 bit tu nguon.
    # Nay lat TUNG BIT trong ca 128, cong mot doi chung HOAN VI BYTE — phep lat
    # bit mu hoan toan voi mot bo sinh sap xep lai byte.
    goc_hex = "".join(format((i * 7 + 3) % 256, "02x") for i in range(16))
    chuan = _sinh_voi(goc_hex)
    chot(xin == [16], "r509")                       # phai XIN du 16 byte
    khac = {}
    for bit in range(128):
        i, mat_na = bit // 8, 1 << (bit % 8)
        b = int(goc_hex[2 * i:2 * i + 2], 16) ^ mat_na
        khac[bit] = _sinh_voi(goc_hex[:2 * i] + format(b, "02x") + goc_hex[2 * i + 2:])
        chot(xin == [16], "r509")                   # moi luot deu phai xin du
    chot(len(set(khac.values())) == 128, "r509")    # 128 dau ra doi mot khac nhau
    chot(chuan not in set(khac.values()), "r509")   # va khac ca ban chuan
    # HOAN VI hai byte dau: cung DA SO byte, cung do dai, khac THU TU.
    hoan_vi = goc_hex[2:4] + goc_hex[0:2] + goc_hex[4:]
    chot(hoan_vi != goc_hex and _sinh_voi(hoan_vi) != chuan, "r509")
    # F02 (luot 6) — lat bit chi do DO NHAY CUC BO quanh MOT mau, khong chung
    # minh GIU THONG TIN. Mot bo sinh nen `int(...) % 1000000007` phan biet duoc
    # ca 128 doi chung lat bit lan phep hoan vi, ma mien dau ra chi con duoi
    # 2**30 gia tri — do duoc, no qua tron quick 16/16. Nen do them VA CHAM giua
    # cac nguon XA nhau, khong chi lan can mot mau.
    xa = ["00" * 16, "%032x" % 1, "%032x" % 1000000007,
          "%032x" % (2 ** 64), "%032x" % (2 ** 127), "ff" * 16]
    ra_xa = [_sinh_voi(v) for v in xa]
    chot(len(set(ra_xa)) == len(xa), "r509")
    # DOI CHUNG DUONG: mot trien khai dung `token_bytes` phai duoc CHAP NHAN.
    # Thieu doi chung nay thi khong gi canh viec ca lai siet vao mot API.
    that_sinh = globals()["sinh_dau_phien"]
    globals()["sinh_dau_phien"] = lambda: secrets.token_bytes(16).hex()
    try:
        chot(_sinh_voi(goc_hex) == goc_hex and xin == [16], "r509")
    finally:
        globals()["sinh_dau_phien"] = that_sinh
    # A5c(1b) — va HAI LUOT PHONG THAT qua chinh `chay_mot_mutant` phai cho hai
    # dau KHAC nhau: chot tren moi do ham sinh, chua do duong dung no.
    dau = []
    that_run = globals()["run"]

    def run_ghi(args, cwd, check=True, env=None):
        if env and KENH_ENV in env:
            dau.append(env[DAU_PHIEN_ENV])
            Path(env[KENH_ENV]).write_text("", encoding="utf-8")   # luon KHONG DO DUOC
        return that_run(["git", "--version"], cwd, check=False)

    globals()["run"] = run_ghi
    try:
        chay_mot_mutant(d, "m", ("T1",))
    finally:
        globals()["run"] = that_run
    chot(len(dau) == 2 and dau[0] != dau[1], "r509")
    # A5c(1b) ve THU HAI, truoc day THIEU: cay ban ghi cua luot MOT vao kenh cua
    # luot HAI => KHONG DO DUOC. "Hai dau khac nhau" moi la dieu kien CAN; phep
    # PHAT LAI moi cho thay dau phien that su CHAN duoc ban ghi luot truoc.
    ph_luot = []

    def kb_phat_lai(ph, mu, lan):
        ph_luot.append(ph)
        if lan == 1:
            return _du_ca(ph, {}, mutant=mu, lan_thu=lan)      # THIEU dong luot
        # luot HAI: cay NGUYEN ban ghi cua luot MOT (mang dau phien cua luot 1),
        # moi mat khac deu hop le voi luot 2.
        return (_du_ca(ph_luot[0], {}, mutant=mu, lan_thu=lan)
                + [_ban_ghi(ph_luot[0], mutant=mu, lan_thu=lan, dong_luot=True, rc=0)])

    that2, gia2 = _run_gia([], kb_phat_lai)
    globals()["run"] = gia2
    try:
        tt2, _, so_lan2 = chay_mot_mutant(d, "m", ("T1",))
    finally:
        globals()["run"] = that2
    chot(tt2 == KHONG_DO_DUOC and so_lan2 == 2 and ph_luot[0] != ph_luot[1], "r509")
    # A5c(1b) ve THU BA — HAI LUOT PHONG DOC LAP, CUNG DINH DANH nghiep vu
    # (cung mutant, cung `lan_thu` = 1, cung rc = 0). F04 (luot 3): hai phep tren
    # deu lay dau cua `lan_thu` 1 va 2 TRONG MOT lan goi, nen mot bo nho dem theo
    # `(ten, lan_thu)` van goi nguon moi luot ma TAI DUNG dau khi phong lai cung
    # dinh danh — do duoc, `cached-business-nonce` SONG SOT full.
    dau2 = []

    def run_ghi2(args, cwd, check=True, env=None):
        if env and KENH_ENV in env:
            ph2, mu2, lan2 = env[DAU_PHIEN_ENV], env[MUTANT_ENV], int(env[LAN_THU_ENV])
            dau2.append((env[LAN_THU_ENV], ph2))
            dong = (_du_ca(ph2, {}, mutant=mu2, lan_thu=lan2)
                    + [_ban_ghi(ph2, mutant=mu2, lan_thu=lan2, dong_luot=True, rc=0)])
            Path(env[KENH_ENV]).write_text(
                "".join(json.dumps(x, sort_keys=True) + "\n" for x in dong), encoding="utf-8")
        return that_run(["git", "--version"], cwd, check=False)

    globals()["run"] = run_ghi2
    try:
        chay_mot_mutant(d, "m", ("T1",))            # luot phong THU NHAT
        chay_mot_mutant(d, "m", ("T1",))            # luot phong THU HAI, cung dinh danh
    finally:
        globals()["run"] = that_run
    chot([l for l, _ in dau2] == ["1", "1"], "r509")
    chot(dau2[0][1] != dau2[1][1], "r509")


def r510_ban_ghi_thieu_dau_dong_luot(d: Path):
    """A5c(2) — du ket qua nhung KHONG dong luot => KHONG DO DUOC."""
    ph = sinh_dau_phien()
    k = _kenh_tam(_du_ca(ph, {"T1": NHAN_DO_CHOT}), d)
    tt, ly_do = doc_kenh(k, ph, "m", 1, ("T1",))
    chot(tt == KHONG_DO_DUOC and "dong luot" in ly_do, "r510")


def r511_ma_san_pham_phat_khong_doat_duoc_ten_ca(d: Path):
    """A5c(3) — ma san pham goi `phat()` trong luc T3 chay, tu khai la T1.

    Khung dong dau ten ca tu TRANG THAI cua chinh no => ban ghi mang T3, tuc ban
    ghi THU HAI cua T3 => KHONG DO DUOC; va T1 KHONG nhan ket qua gia nao.
    PHAM VI: ca nay do MOT CO CHE THUC THI DUOC, khong do mot ranh gioi quyen —
    ranh gioi ay khong ton tai (xem MO HINH DE DOA trong dac ta).
    """
    ph = sinh_dau_phien()
    k = d / "m.jsonl"
    kh = KhungPhat(k, ph, "m", 1)
    for ten, _ in CA:
        kh.vao_ca(ten)
        kh.phat(NHAN_DAT)
        if ten == "T3":
            kh.phat(NHAN_DO_CHOT, "ma san pham tu khai la T1")   # bi dong dau T3
    kh.dong_luot(1)
    noi_dung = k.read_text(encoding="utf-8")
    chot('"ca": "T1", "chi_tiet": "ma san pham' not in noi_dung, "r511")
    tt, ly_do = doc_kenh(k, ph, "m", 1, ("T1",))
    chot(tt == KHONG_DO_DUOC and "TRUNG cho ca T3" in ly_do, "r511")


def r512_kenh_khong_lan_voi_stdout(d: Path):
    """A5b — ket luan chi lay tu KENH; stdout cua tien trinh con KHONG duoc du vao.

    F05 (luot 2) — hai lo cung MOT goc, deu la "do ban sao thay vi do san pham":
      · do gia cu lay `CompletedProcess` cua `git --version` nen `p.returncode`
        LUON 0, tuc nhanh con rc=1 — nhanh PHO BIEN khi mutant giet mot ca — bi
        bo trong. Do duoc: `stdout-rc1` SONG SOT full.
      · chot cu la chot DIEM (dung MOT kich ban). Mot dot bien gai dieu kien o
        bien KHAC thoat sach khoi mot chot diem.
    Nay: tien trinh con THAT, mot lan chay cap DONG THOI stdout + rc + kenh cho
    chinh `chay_mot_mutant`; va chot la BAT BIEN VI SAI — giu KENH co dinh, doi
    STDOUT, ket qua KHONG duoc doi, tren CA HAI nhanh rc.

    SAN PHAM dang do la `chay_mot_mutant` + `doc_kenh` — chay NGUYEN, khong thay.
    FIXTURE la tien trinh con (`_KICH_CON`): viec cua no chi la PHAT stdout, rc va
    kenh, dung nhu mot mutant that phat. Noi ro de khong ai doc nham rang ca nay
    do mot ban sao cua bo cham.
    """
    ket = {}
    for nhanh, ca_do in (("rc0", ""), ("rc1", "T2")):
        for so, in_gia in (("sach", None), ("gia-mao", "1")):
            bs = _kich_con(d, f"{nhanh}-{so}")
            with _moi_truong(CA_DO=ca_do, IN_GIA_MAO=in_gia):
                ket[(nhanh, so)] = chay_mot_mutant(bs, "m", ("T1",))[0]
    # `dich` la ("T1",) ma ca do (neu co) la "T2" => moi kich ban deu KHONG GIET.
    chot(ket == {("rc0", "sach"): KHONG_GIET, ("rc0", "gia-mao"): KHONG_GIET,
                 ("rc1", "sach"): KHONG_GIET, ("rc1", "gia-mao"): KHONG_GIET}, "r512")
    chot(ket[("rc0", "sach")] == ket[("rc0", "gia-mao")]
         and ket[("rc1", "sach")] == ket[("rc1", "gia-mao")], "r512")
    # RANH GIOI TIEN TRINH — chung minh stdout THAT SU mang dong gia mao va rc
    # THAT SU theo kich ban; thieu phep nay thi bat bien tren co the dung vi
    # stdout rong chu khong phai vi bo cham bo qua stdout.
    # F04 (luot 6) — moi kich ban tren deu co KENH ket luan KHONG GIET, nen mot
    # duong "chi doc stdout KHI kenh noi GIET" van xanh — va no pha bat bien theo
    # huong MAT TIN DUNG: mot GIET hop le bi stdout vo can thu hoi. Bo sung nhanh
    # KENH = GIET, nhan hai stdout khac nhau, ca hai deu phai GIET.
    ket_giet = {}
    for so, in_nhieu in (("sach", None), ("nhieu-ngoai-dich", "1")):
        bsg = _kich_con(d, f"giet-{so}")
        with _moi_truong(CA_DO="T1", IN_GIA_MAO=None, IN_NHIEU=in_nhieu):
            ket_giet[so] = chay_mot_mutant(bsg, "m", ("T1",))[0]
    chot(ket_giet == {"sach": GIET, "nhieu-ngoai-dich": GIET}, "r512")
    bs = _kich_con(d, "chung")
    env = dict(os.environ, IN_GIA_MAO="1", CA_DO="T2",
               NHANH_DON_DUOC_DAU_PHIEN=sinh_dau_phien(), NHANH_DON_DUOC_MUTANT="m",
               NHANH_DON_DUOC_LAN_THU="1", NHANH_DON_DUOC_KENH=str(bs / "k.jsonl"))
    p = run([sys.executable, Path(__file__).name], bs, check=False, env=env)
    chot("CASE T1: DO" in p.stdout and p.returncode == 1, "r512")


def r513_moi_dieu_kien_cong_cua_main_phai_do_duoc(d: Path):
    """A7 — MOI dieu kien cong trong `main()` phai co MOT ca lam no DO.

    F07 (luot 2) — truoc luot nay KHONG ca nao goi `main()`, nen ca ba dieu kien
    cong deu ngoai tam do; dot bien `return 0 if (dat == len(DOT_BIEN) and not
    tu_kiem_do) else 1` -> `return 0` SONG SOT tron ven (full rc=0, moi so xanh).
    Moi kich ban duoi day lam DUNG MOT dieu kien bat, va ket qua duoc so bang
    CA BANG — do TUNG SO HANG, khong do quan he (quan he song sot qua troi so).

    F03 (luot 3) — "dung MOT dieu kien" la LOI KHAI, phai lam cho no DUNG. Ban
    truoc sai o hai cho: `nhom_them=("r999",)` pha CA HAI ve cua `thieu` (bo mot
    ve thi ve kia van bac), va `san_cong` TU DAT LAI `SAN_NHOM` nen hang san THAT
    khong bao gio duoc do — `lower-floor` (`SAN_NHOM=1`) song sot vi the.
    """
    n = len(DOT_BIEN)
    kich = {
        # sum != len => cong "ba so hang khong cong dung tong" (va CHI no)
        "tong-lech":           dict(dat=n, kgiet=1, kdo=0),
        # sum dung, dat < n => chi CONG CUOI bat
        "thieu-giet":          dict(dat=n - 1, kgiet=1, kdo=0),
        "co-khong-do-duoc":    dict(dat=n - 1, kgiet=0, kdo=1),
        "tu-kiem-do":          dict(dat=n, kgiet=0, kdo=0, tu_kiem_do=("r501",)),
        # cong "nhom bat buoc" — BA ve, moi ve mot kich ban RIENG (F03)
        # F03 (luot 4) — phai dat `tk_giet` TUONG MINH: mac dinh keo no ve
        # `len - tk_hong`, tuc kich ban nay bat CA HAI ve, va bo rieng `tk_hong`
        # khoi cong khong lam ca nao do.
        "tu-dot-bien-hong":    dict(dat=n, kgiet=0, kdo=0,
                                    tk_giet=len(DOT_BIEN_TU_KIEM), tk_hong=1),
        "tu-dot-bien-thieu-giet": dict(dat=n, kgiet=0, kdo=0, tk_giet=0),
        "ca-chua-chay":        dict(dat=n, kgiet=0, kdo=0, bo_khoi_tu_kiem=("r509",)),
        "ca-khong-co-dot-bien": dict(dat=n, kgiet=0, kdo=0, bo_khoi_dich=("r509",)),
        "san-nhom-tut":        dict(dat=n, kgiet=0, kdo=0, bo_khoi_nhom=("r509",)),
        # doi chung DUONG: khong dieu kien nao bat => rc 0. Thieu ca nay thi mot
        # cong "luon do" cung qua duoc bang tren.
        "du-dieu-kien":        dict(dat=n, kgiet=0, kdo=0),
    }
    ket = {t: _chay_main_gia(d / t, **kw) for t, kw in kich.items()}
    chot({t: v[0] for t, v in ket.items()}
         == {"tong-lech": 1, "thieu-giet": 1, "co-khong-do-duoc": 1,
             "tu-kiem-do": 1, "tu-dot-bien-hong": 1, "tu-dot-bien-thieu-giet": 1,
             "ca-chua-chay": 1, "ca-khong-co-dot-bien": 1, "san-nhom-tut": 1,
             "du-dieu-kien": 0}, "r513")
    # F07 — va DONG IN phai khop CHINH ba so hang da quyet dinh. Mot ban in mot
    # dang roi quyet dinh mot dang khac la kieu hong am tham nhat: nguoi doc log
    # thay so dung, con cong thi an so sai.
    chot(f"MUTANT: giet = {n} · khong giet = 1 · khong do duoc = 0"
         in ket["tong-lech"][1], "r513")
    chot(f"MUTANT: giet = {n - 1} · khong giet = 0 · khong do duoc = 1"
         in ket["co-khong-do-duoc"][1], "r513")


def r514_bo_cong_that_phan_dung_ba_nhanh(d: Path):
    """A3b — bo CONG THAT trong `chay_dot_bien` phai cong dung nhanh cho ba trang thai.

    F07 (luot 2) — `r504` dung mot bo dem RIENG dung trong than ca, nen no do BAN
    SAO chu khong do san pham: do duoc, `counter-fold` (cong nham mot loai sang
    loai khac) SONG SOT full. Boi so ba loai co chu y LECH NHAU (1 · 2 · 3) de
    KHONG hoan vi nao cho ra cung mot bo ba — bang nhau thi mot phep cong sai
    nhanh van ra dung tong.
    """
    m = _nap_ban_sao(d)
    # F05 (luot 3) — do gia phai BAT DOI XUNG ca o chieu `so_lan`: ban truoc tra
    # 1 cho MOI trang thai, trong khi mot ket qua KHONG DO DUOC that su da chay
    # HAI lan. Vi the `khong_do += so_lan` (dem LAN THU thay vi dem MUTANT) van
    # qua. Do duoc: `counter-count-attempts` SONG SOT full.
    # F04 (luot 4) — phu TICH hai truc (trang thai x so lan), khong chi mot diem
    # tren moi truc: ban truoc chi cho `so_lan=2` o KDD, nen `dat += so_lan` va
    # `khong_giet += so_lan` deu qua sach. Boi so ba loai van LECH NHAU (2·3·3
    # khac nhau tung doi mot theo cach cong sai nhanh).
    # F02 (luot 5) — `(2,3,3)` co HAI so 3 TRUNG nhau, nen doi cheo KHONG GIET
    # voi KHONG DO DUOC van tra dung `(2,3,3)`: do duoc, `counter-swap-kg-kdd`
    # SONG SOT full. Loi khai "khac nhau tung doi mot" cua ban truoc SAI.
    # Nay `(2,3,5)`: doi mot tung doi, va KHONG phep gop/hoan vi nao tra lai
    # dung bo ba ay (kiem ngay duoi bang phep thu VET CAN).
    kich = [(m.GIET, 1), (m.GIET, 2),
            (m.KHONG_GIET, 1), (m.KHONG_GIET, 2), (m.KHONG_GIET, 2),
            (m.KHONG_DO_DUOC, 2), (m.KHONG_DO_DUOC, 2), (m.KHONG_DO_DUOC, 2),
            (m.KHONG_DO_DUOC, 2), (m.KHONG_DO_DUOC, 2)]
    m.DOT_BIEN = m.DOT_BIEN[:len(kich)]

    def mot_mutant(ban_sao, ten, dich):
        tt, so_lan = kich.pop(0)
        return (tt, "ly do gia", so_lan)

    m.chay_mot_mutant = mot_mutant
    with _git_config_sach(), contextlib.redirect_stdout(io.StringIO()):
        ra = m.chay_dot_bien()
    chot(ra == (2, 3, 5), "r514")
    # F05 (luot 6) — TONG CHE DUOC HAI DONG GOP SAI BU TRU NHAU. Mot dot bien
    # chuyen 2 don vi tu GIET sang KHONG GIET o o (GIET, lan 2) roi tra 1 don vi
    # nguoc lai o moi o (KG, lan 2) van cho dung `(2,3,5)` — do duoc, bo cong that
    # tra `(-1, 2, 0)` cho MOT GIET-lan-2, tuc SO AM, ma tong van dung.
    # Tap `hoan_vi`/`gop` o tren chi phu lop CHUYEN NGUYEN NHANH; no KHONG phai
    # chung minh cho moi phep cong sai, va loi giai thich cu de khien nguoi doc
    # hieu nham la co. Nen do TUNG VECTO CO SO: moi o (trang thai x so lan) chay
    # RIENG voi DUNG MOT mutant, va doi dung vecto don vi.
    CO_SO = {
        ("giet", 1):    ((m.GIET, 1), (1, 0, 0)),
        ("giet", 2):    ((m.GIET, 2), (1, 0, 0)),
        ("kg", 1):      ((m.KHONG_GIET, 1), (0, 1, 0)),
        ("kg", 2):      ((m.KHONG_GIET, 2), (0, 1, 0)),
        ("kdd", 1):     ((m.KHONG_DO_DUOC, 1), (0, 0, 1)),
        ("kdd", 2):     ((m.KHONG_DO_DUOC, 2), (0, 0, 1)),
    }
    do_co_so = {}
    for ten_o, ((tt, so_lan), _) in CO_SO.items():
        m2 = _nap_ban_sao(d / f"coso-{ten_o[0]}-{ten_o[1]}")
        m2.DOT_BIEN = m2.DOT_BIEN[:1]
        m2.chay_mot_mutant = lambda a, b, c, _t=tt, _s=so_lan: (_t, "ly do gia", _s)
        with _git_config_sach(), contextlib.redirect_stdout(io.StringIO()):
            do_co_so[ten_o] = m2.chay_dot_bien()
    chot(do_co_so == {k: v[1] for k, v in CO_SO.items()}, "r514")
    # VET CAN chinh bo ba: khong hoan vi nao, va khong phep gop hai nhanh nao,
    # tra lai `(2,3,5)`. Thieu phep nay thi "boi so lech nhau" lai chi la LOI KHAI.
    boi = (2, 3, 5)
    hoan_vi = {(boi[a], boi[b], boi[c])
               for a, b, c in ((0, 1, 2), (0, 2, 1), (1, 0, 2),
                               (1, 2, 0), (2, 0, 1), (2, 1, 0))}
    gop = {(boi[0] + boi[1], 0, boi[2]), (boi[0], boi[1] + boi[2], 0),
           (0, boi[0] + boi[1], boi[2]), (boi[0], 0, boi[1] + boi[2]),
           (boi[0] + boi[2], boi[1], 0), (0, boi[1], boi[0] + boi[2])}
    chot(len(hoan_vi) == 6 and (hoan_vi | gop) - {boi} and boi not in gop, "r514")
    chot(sum(1 for x in hoan_vi if x == boi) == 1, "r514")


def r515_moi_chieu_neo_deu_co_ca_am(d: Path):
    """A5c(1c) — BON chieu neo (dau phien · mutant · lan thu · rc) moi chieu mot ca am.

    F01 (luot 2) — ban truoc chi co ca am cho DAU PHIEN (r508). Bo rieng phep so
    `rc`, `mutant` hay `lan_thu` KHONG lam ca nao do: do duoc, `ignore-rc` song
    ca quick lan full, `ignore-mutant`/`ignore-attempt` song quick. Moi kich ban
    duoi doi DUNG MOT chieu va giu nguyen moi chieu con lai, nen mau do quy dung
    ve chieu ay chu khong ve mot thay doi gop.
    """
    ph = sinh_dau_phien()
    k0 = _kenh_tam(_du_ca(ph, {}) + [_ban_ghi(ph, dong_luot=True, rc=0)], d, "k0.jsonl")
    k1 = _kenh_tam(_du_ca(ph, {}, mutant="khac")
                   + [_ban_ghi(ph, mutant="khac", dong_luot=True, rc=0)], d, "k1.jsonl")
    k2 = _kenh_tam(_du_ca(ph, {}, lan_thu=2)
                   + [_ban_ghi(ph, lan_thu=2, dong_luot=True, rc=0)], d, "k2.jsonl")
    k3 = _kenh_tam(_du_ca(ph, {"T1": NHAN_DO_CHOT})
                   + [_ban_ghi(ph, dong_luot=True, rc=1)], d, "k3.jsonl")
    ket = {
        "chuan":   doc_kenh(k0, ph, "m", 1, ("T1",), 0)[0],
        "mutant":  doc_kenh(k1, ph, "m", 1, ("T1",), 0)[0],
        "lan_thu": doc_kenh(k2, ph, "m", 1, ("T1",), 0)[0],
        # cung mot kenh k0, chi rc cua TIEN TRINH lech so voi rc kenh khai
        "rc":      doc_kenh(k0, ph, "m", 1, ("T1",), 1)[0],
        # F03 (luot 6) — CHIEU NGUOC: kenh khai dong luot rc=1 va co T1 DO_CHOT
        # (tuc dang le GIET), ma TIEN TRINH thoat 0. Ban truoc chi thu MOT huong
        # (kenh 0 / tien trinh 1) tren mot kenh toan DAT, nen bo phep so o nhanh
        # child-0 van xanh — mot kenh lech rc van duoc cap GIET.
        "rc-nguoc": doc_kenh(k3, ph, "m", 1, ("T1",), 0)[0],
    }
    chot(ket == {"chuan": KHONG_GIET, "mutant": KHONG_DO_DUOC,
                 "lan_thu": KHONG_DO_DUOC, "rc": KHONG_DO_DUOC,
                 "rc-nguoc": KHONG_DO_DUOC}, "r515")


def r516_bo_cham_tu_dot_bien_phan_hang_dung(d: Path):
    """A6b — BO CHAM TU DOT BIEN phai phan hang dung, khong cap TIN DUNG GIA.

    Day la tang NGOAI CUNG. Ca nay goi CHINH `chay_dot_bien_tu_kiem`, chi thay
    `run` bang do gia kich ban hoa STDOUT + RC cua tien trinh con — tuc do DUONG
    PHAN HANG that, khong do mot ban sao.

    LUOT 5 — DOI CACH DUNG, khong them o nua. Ba luot lien tiep (3, 4, 5) deu tim
    ra dung mot HINH DANG loi: tap kich ban thieu MOT O trong khong gian dau vao
    (luot 3: khong co lop ngoai le; luot 4: khong co dau vao TRON; luot 5: khong
    co tap do RONG, va khong co rc NGOAI {0,1}). Va tung o mot la danh du —
    §12 doi hoi xem lai CACH LAM khi mot hinh dang lap den lan thu ba.
    Nen nay khong liet ke o bang tay nua: SINH TICH DE-CAC cua ba truc, va ky
    vong duoc suy TU MOT LUAT chu khong tu mot bang chep tay. Bo sot mot O tro
    thanh khong the; chi con co the bo sot mot TRUC — khong gian nho hon nhieu
    va nhin thay duoc.
    """
    m = _nap_ban_sao(d)
    # LUOT 6 — SINH TICH VAN CHUA DU: ban truoc chieu `ca_chot` thanh `None` hoac
    # DUNG MOT ten, va `DICH` luon la singleton. Vi the KHONG BIEU DIEN NOI quan
    # he "dung dich VA THEM chot ngoai dich", hay "moi chet MOT PHAN cua nhieu
    # dich" — hai bien doi `bao-ham` va `giao-khac-rong` di qua tron 18 o.
    # Bai hoc: sinh tich chi chuyen rui ro tu "sot O" sang "sot TRUC", va thu bi
    # sot lan nay la TRUC QUAN HE TAP HOP / LUC LUONG, khong phai mot gia tri nua.
    TRUC_DICH = {"mot-dich": ("r515",), "hai-dich": ("r515", "r514")}
    TRUC_QUAN_HE = {
        "bang-dich":      lambda dc: set(dc),
        "du-ngoai-dich":  lambda dc: set(dc) | {"r511"},
        "thieu-mot-dich": lambda dc: set(list(dc)[:-1]),
        "rong":           lambda dc: set(),
        "roi-dich":       lambda dc: {"r511"},
    }
    TRUC_KHAC = {"khong-loi-vo-can": None, "co-loi-vo-can": "r510"}
    TRUC_RC = (0, 1, 2)                       # 2 = con chet vi ly do khac

    def _stdout(tap_chot, ca_khac):
        d_ = ""
        for c in sorted(tap_chot):
            d_ += f"TU KIEM {c}: DO_CHOT — chot cua ca {c} that bai\n"
        if ca_khac:
            d_ += f"TU KIEM {ca_khac}: DO_KHAC — AttributeError: NoneType\n"
        return d_

    kich, mong_doi, dich_cua = {}, {}, {}
    for ten_d, dich in TRUC_DICH.items():
        for ten_q, quan_he in TRUC_QUAN_HE.items():
            for ten_k, ca_khac in TRUC_KHAC.items():
                for rc in TRUC_RC:
                    ten = f"{ten_d}__{ten_q}__{ten_k}__rc{rc}"
                    tap = quan_he(dich)
                    kich[ten] = (_stdout(tap, ca_khac), rc)
                    dich_cua[ten] = dich
                    # LUAT, khong phai bang chep tay: chi GIET khi ca ba chieu dat,
                    # va phep so tap phai la BANG NHAU — khong bao ham, khong giao.
                    mong_doi[ten] = (ca_khac is None and rc == 1 and tap == set(dich))
    goi = []

    def run_gia(args, cwd, check=True, env=None):
        ten = Path(cwd).name
        goi.append(ten)
        out, rc = kich[ten]
        ids = [c for c, _, _ in m.TU_KIEM]
        failed = len(m._khoi_chan_doan(out, "DO_CHOT")) + len(m._khoi_chan_doan(out, "DO_KHAC"))
        out += f"TU KIEM: {len(ids) - failed}/{len(ids)}\n"
        Path(env[m.TU_KIEM_FILE_ENV]).write_text(json.dumps({"nonce": env[m.TU_KIEM_NONCE_ENV], "cases": ids}), encoding="utf-8")
        return subprocess.CompletedProcess(args, rc, out, "")

    m.run = run_gia

    def ghep(*phan):
        """Ghep neo LUC CHAY, khong viet nguyen van.

        Viet nguyen van thi chinh than ca nay lam chuoi ay xuat hien THEM mot lan
        ngoai bang, va phep doi hoi "neo duy nhat NGOAI bang" se bac het — ca do
        vi ly do VO CAN, dung benh ma chinh no sinh ra de bat.
        """
        return "".join(phan)

    # MOI muc dung CHUNG mot neo: phep doi hoi duy nhat duoc kiem DOC LAP cho tung
    # muc (dem tren TEP, khong dem cheo cac muc), va noi dung thay the KHONG bao
    # gio duoc chay vi `run` la do gia. Neo phai la dong KHONG dot bien nao KHAC
    # cham toi — neu mot muc trong bang THAT sua dung dong ay thi o luot chay cua
    # muc do, neo cua `r516` bien mat va ca do vi ly do vo can (da tra gia: nam
    # muc keo r516 do theo dung kieu ay).
    NEO = ghep("    if not ", "duong.exists():")
    m.DOT_BIEN_TU_KIEM = [(ten, dich_cua[ten], NEO, "    pass") for ten in kich]
    with contextlib.redirect_stdout(io.StringIO()) as ra:
        giet, hong, khong_do = m.chay_dot_bien_tu_kiem()
    dong_in = ra.getvalue()
    chot(sorted(goi) == sorted(kich), "r516")       # MOI o deu THAT SU duoc chay
    so_giet = sum(1 for v in mong_doi.values() if v)
    chot((giet, hong) == (so_giet, len(kich) - so_giet), "r516")
    chot((so_giet, len(kich), khong_do) == (2, 60, 0), "r516")   # truc khong bi thu nho am tham
    # Va TUNG o phai ra dung nhan cua no, khong chi tong dung: mot bo cham cong
    # nham van co the ra dung cap so.
    for ten, la_giet in mong_doi.items():
        dau_giet = f"{ten} | {','.join(dich_cua[ten])} | {len(dich_cua[ten])}/{len(dich_cua[ten])}"
        chot((dau_giet in dong_in) == la_giet, "r516")
    # va moi NHANH TU CHOI deu phai duoc di qua it nhat mot lan, dung ly do cua no
    chot("TIN DUNG GIA: ca chet vi loi VO CAN" in dong_in, "r516")
    chot("TIN DUNG GIA: child rc=0 != 1" in dong_in, "r516")
    chot("TIN DUNG GIA: child rc=2 != 1" in dong_in, "r516")
    chot("0 — ca do THUC TE: r511" in dong_in, "r516")
    chot("0 — ca do THUC TE: (rong)" in dong_in, "r516")
    # Va RUNNER tu kiem phai TACH hai lop khi in. Gop lam mot thi moi loi VO CAN
    # doi lot thanh chot cua ca, va ba chot tren khong con gi de loc — tuc chuoi
    # phong thu day sap tu dong DAU TIEN.
    def ca_chot():
        m.chot(False, "r901")

    def ca_vo_can():
        raise AttributeError("loi vo can gia lap")

    m.TU_KIEM = [("r901", ca_chot, False), ("r902", ca_vo_can, False)]
    with contextlib.redirect_stdout(io.StringIO()) as ra2:
        do2 = m.chay_tu_kiem()
    in2 = ra2.getvalue()
    chot(do2 == ["r901", "r902"], "r516")
    chot("TU KIEM r901: DO_CHOT" in in2, "r516")
    chot("TU KIEM r902: DO_KHAC" in in2, "r516")


def r517_kenh_phai_duoc_xac_thuc_truoc_khi_tin(d: Path):
    """A5d (luot 7, TANG SAN PHAM) — bo cham phai XAC THUC kenh truoc khi TIN.

    Day la ca DUY NHAT sinh ra tu mot loi THAT cua ma san pham, khong phai tu mot
    o chua phu cua ca do. Bon duong duoi day deu do duoc tren ban NGUYEN GOC:
      · HAI ban ghi dong luot — ban sau GHI DE ban truoc, nen cay `rc=99` roi
        `rc=1` van qua phep neo rc va tra GIET;
      · mot ban ghi mang CA `ca` LAN `dong_luot` di nhanh dong TRUOC kiem trung;
      · `nhan` khong duoc xac thuc — xoa `nhan` cua mot ca van tra GIET;
      · JSON `null`/list, ten ca sai kieu, UTF-8 hong nem ngoai le RA NGOAI, nen
        luot CHAY LAI bien mat (chay 1 lan thay vi 2).
    Moi duong tu choi phai ve KHONG DO DUOC — huong FAIL-CLOSE.
    """
    ph = sinh_dau_phien()
    dong_ok = _ban_ghi(ph, dong_luot=True, rc=1)

    def _ke(ten, dong_list):
        return _kenh_tam(dong_list, d, ten)

    def doc(k):
        """Goi `doc_kenh` va bien MOI ngoai le thanh chot cua CHINH ca nay.

        Thieu phep nay thi dot bien go vo fail-close lam ca chet bang
        `AttributeError` TRAN — bo cham phan hang dung la TIN DUNG GIA, va mutant
        khong bao gio bi giet DUNG LY DO. Da do duoc: 3 muc bao TIN DUNG GIA.
        """
        try:
            return doc_kenh(k, ph, "m", 1, ("T1",), 1)
        except Exception as exc:                  # noqa: BLE001
            raise TinHieuChotCa(f"doc_kenh nem {type(exc).__name__}: {exc}")

    thieu_nhan = _du_ca(ph, {"T1": NHAN_DO_CHOT})
    for r in thieu_nhan:
        if r["ca"] == "T2":
            r.pop("nhan")
    k_null = d / "null.jsonl"
    k_null.write_text("null\n[]\n", encoding="utf-8")
    k_byte = d / "byte.jsonl"
    k_byte.write_bytes(b"\xff\xfe khong phai utf-8\n")
    # Dau vao ma phep XAC THUC KHONG luong truoc duoc — day la ly do vo fail-close
    # ton tai. `json.loads` tren JSON long qua sau nem `RecursionError`, KHONG phai
    # `JSONDecodeError`, nen no thoat khoi `try` ben trong; CHI vo bat duoc.
    # Thieu dau vao nay thi `bo-vo-fail-close` la DOT BIEN TUONG DUONG: moi dau vao
    # khac deu da duoc xac thuc chan tu truoc, vo khong bao gio chay. Da do duoc:
    # 62/63, dung mot muc do, va do vi ly do ay.
    k_sau = d / "sau-qua.jsonl"
    k_sau.write_text("[" * 100000 + "]" * 100000 + "\n", encoding="utf-8")
    ket = {
        # doi chung DUONG: kenh HOP LE phai van GIET. Thieu no thi moi chot duoi
        # co the dung vi ly do vo can ma ca van xanh.
        "hop-le": doc(_ke("ok.jsonl", _du_ca(ph, {"T1": NHAN_DO_CHOT}) + [dong_ok])),
        # HAI ban ghi dong luot: rc=99 roi rc=1 — ban sau tung GHI DE ban truoc
        "hai-dong-luot": doc(_ke("hai.jsonl", _du_ca(ph, {"T1": NHAN_DO_CHOT})
                                 + [_ban_ghi(ph, dong_luot=True, rc=99), dong_ok])),
        # ban ghi vua mang ten ca vua khai dong luot
        "ca-kiem-dong-luot": doc(_ke("vua.jsonl", _du_ca(ph, {"T1": NHAN_DO_CHOT})
                                     + [_ban_ghi(ph, ca="T1", nhan=NHAN_DO_KHAC,
                                                 dong_luot=True, rc=1)])),
        "thieu-nhan": doc(_ke("nhan.jsonl", thieu_nhan + [dong_ok])),
        "nhan-la": doc(_ke("nhanla.jsonl", _du_ca(ph, {"T1": "NHAN_BIA"}) + [dong_ok])),
        "ten-ca-sai-kieu": doc(_ke("kieu.jsonl",
                                   [_ban_ghi(ph, ca=["T1"], nhan=NHAN_DAT), dong_ok])),
        # `rc` la bool — `True == 1` nen no tung lot qua phep neo rc
        "rc-bool": doc(_ke("rcbool.jsonl", _du_ca(ph, {"T1": NHAN_DO_CHOT})
                           + [_ban_ghi(ph, dong_luot=True, rc=True)])),
        "sau-dong-luot": doc(_ke("sau.jsonl", _du_ca(ph, {"T1": NHAN_DO_CHOT}) + [dong_ok]
                                 + [_ban_ghi(ph, ca="T99", nhan=NHAN_DAT)])),
        "khong-phai-object": doc(k_null),
        "utf8-hong": doc(k_byte),
        "json-long-qua-sau": doc(k_sau),
        # R13-F02 — dau dong luot phai la bool JSON `true`, khong phai "thu
        # truthy". `bool(...)` la mot phep EP KIEU, va ep kieu o day chinh la
        # cap tin dung cho thu khong dung dinh dang.
        "dong-luot-int": doc(_ke("dlint.jsonl", _du_ca(ph, {"T1": NHAN_DO_CHOT})
                                 + [_ban_ghi(ph, dong_luot=1, rc=1)])),
        "dong-luot-chuoi": doc(_ke("dlstr.jsonl", _du_ca(ph, {"T1": NHAN_DO_CHOT})
                                   + [_ban_ghi(ph, dong_luot="yes", rc=1)])),
    }
    # PHAI so CA TRANG THAI LAN LY DO. Chi so trang thai thi VO FAIL-CLOSE che mat
    # tung chot: go mot phep xac thuc, ngoai le roi vao vo va VAN ra KHONG DO DUOC
    # — ca xanh, dot bien song. Do duoc: `bo-xac-thuc-object`,
    # `bo-xac-thuc-kieu-ten-ca`, `bo-vo-fail-close` deu bao TIN DUNG GIA.
    LY_DO = {
        "hop-le":             (GIET, ""),
        "hai-dong-luot":      (KHONG_DO_DUOC, "co ban ghi SAU ban ghi dong luot"),
        "ca-kiem-dong-luot":  (KHONG_DO_DUOC, "vua mang ten ca vua khai dong luot"),
        "thieu-nhan":         (KHONG_DO_DUOC, "nhan khong hop le cho ca T2"),
        "nhan-la":            (KHONG_DO_DUOC, "nhan khong hop le cho ca T1"),
        "ten-ca-sai-kieu":    (KHONG_DO_DUOC, "ten ca khong phai chuoi"),
        "rc-bool":            (KHONG_DO_DUOC, "thieu rc kieu int"),
        "sau-dong-luot":      (KHONG_DO_DUOC, "co ban ghi SAU ban ghi dong luot"),
        "khong-phai-object":  (KHONG_DO_DUOC, "khong phai object"),
        "utf8-hong":          (KHONG_DO_DUOC, "khong doc duoc kenh"),
        "json-long-qua-sau":  (KHONG_DO_DUOC, "bo doc kenh nem RecursionError"),
        "dong-luot-int":      (KHONG_DO_DUOC, "dau dong luot khong phai bool true: 1"),
        "dong-luot-chuoi":    (KHONG_DO_DUOC, "dau dong luot khong phai bool true: 'yes'"),
    }
    chot({t: v[0] for t, v in ket.items()} == {t: v[0] for t, v in LY_DO.items()}, "r517")
    chot(all(LY_DO[t][1] in ket[t][1] for t in LY_DO), "r517")

    # VA luot CHAY LAI phai con nguyen: mot kenh nem ngoai le tung lam
    # `chay_mot_mutant` chay DUNG MOT lan thay vi hai.
    nk = []
    that_run = globals()["run"]

    def run_hong(args, cwd, check=True, env=None):
        if env and KENH_ENV in env:
            nk.append(env[LAN_THU_ENV])
            Path(env[KENH_ENV]).write_text("null\n", encoding="utf-8")
        return that_run(["git", "--version"], cwd, check=False)

    globals()["run"] = run_hong
    try:
        tt, ly_do, so_lan = chay_mot_mutant(d, "m", ("T1",))
    finally:
        globals()["run"] = that_run
    chot(tt == KHONG_DO_DUOC and nk == ["1", "2"] and so_lan == 2, "r517")



def r518_kenh_chiu_duoc_ky_tu_phan_dong_unicode(d: Path):
    """F01 (luot 8) — U+2028 / U+2029 / U+0085 trong `chi_tiet` KHONG duoc lam vo ban ghi.

    HUONG DO nay den tu cross-review luot 8. Luot ay bi BO LOC NEN cat o giay
    154 truoc khi kip ghi `VERDICT.md`, nhung da neu huong BANG LOI truoc do:
    *"ky tu phan dong Unicode trong chi_tiet"*. Phep do duoi day do phien chinh
    viet — dung nep "doi phan cong, khong doi provider" cua CLAUDE.md. Mot huong
    NEU RA ma khong ai CHAY thi khong ton tai; day la luc bien no thanh ca.

    GOC LOI. Ben GHI dung `json.dumps(..., ensure_ascii=False)` — CO Y, de van
    ban tieng Viet trong kenh con doc duoc — nen U+2028 / U+2029 / U+0085 di
    THO vao kenh (ba ky tu nay KHONG phai ma dieu khien < 0x20 nen JSON khong
    buoc thoat; do la ly do `chr(11)` `chr(12)` `chr(28)` VO HAI con ba ky tu
    nay thi khong). Ben DOC tach ban ghi bang `splitlines()`, ma `splitlines()`
    coi CA BA la dau xuong dong. Mot ban ghi HOP LE vi the bi cat lam DOI, nua
    dau thanh JSON hong.

    DO DUOC TRUOC KHI VA (cung mot rig, chi doi mot ky tu):
      chi_tiet sach        -> KHONG_GIET     (dung)
      chi_tiet co U+2028   -> KHONG_DO_DUOC "ban ghi khong phai JSON"
      chi_tiet co U+2029   -> KHONG_DO_DUOC "ban ghi khong phai JSON"
      chi_tiet co U+0085   -> KHONG_DO_DUOC "ban ghi khong phai JSON"
    Tuc MOT KY TU trong van ban thong diep DOI HAN verdict cua luot.

    VI SAO KHONG PHAI "VO HAI VI FAIL-CLOSE". Huong hong dung la fail-close
    (KDD khong cap tin dung gia), nhung KDD lam suite DO. Mot ca hop le bi doi
    thanh "khong do duoc" chi vi NOI DUNG thong diep ngoai le la bao dong GIA —
    va bao dong gia la cach nhanh nhat de nguoi ta ngung tin mot cong. Duong
    toi duoc: `chi_tiet` mang `f"{type(exc).__name__}: {exc}"`, tuc VAN BAN
    NGOAI LE, va thong diep ngoai le thuong CHEP LAI dau vao (JSON hong, van
    ban git, noi dung tep) — khong co gi cam dau vao ay chua U+2028.

    VI SAO SUA BEN DOC, KHONG SUA BEN GHI — va day la phan dang nho nhat.
    Ca hai deu dong duoc lo:
      · ben GHI `ensure_ascii=True` -> ky tu bi thoat, `splitlines()` het thay;
      · ben DOC tach dung dau phan ban ghi that -> khong con cat nham.
    Nhung SUA CA HAI thi moi ben BIEN THANH DOT BIEN TUONG DUONG cua ben kia:
    neu ben ghi da thoat het thi ben doc tach kieu nao cung nhu nhau, va nguoc
    lai — KHONG dau vao nao phan biet duoc, tuc khong do duoc RANG cua ben nao.
    Do la cai bay "dot bien tuong duong" ma kho nay da tra gia mot lan
    (`bo-vo-fail-close`, luot 7). Chon DUY NHAT ben DOC vi no MANH HON: no dung
    ke ca khi ben ghi doi, va no giu duoc `ensure_ascii=False`. Ben GHI GIU
    NGUYEN CO CHU Y — khong phai bo sot.

    HAI CHOT, vi mot minh khong du:
      (A) duong DO_CHOT -> verdict phai la GIET, khong con KDD;
      (B) duong DO_KHAC -> ly do phai chua `chi_tiet` NGUYEN VAN.
    Thieu (B) thi mot ban "va" bang cach XOA hoac thay ky tu van qua duoc (A)
    trong khi da lam hong bang chung. Thieu (A) thi khong do duoc hau qua that.
    """
    KY_TU = [("U+2028", chr(0x2028)), ("U+2029", chr(0x2029)), ("U+0085", chr(0x85))]
    for ten_ky_tu, ch in KY_TU:
        ct = "loi" + ch + "phan hai"

        # (A) duong DO_CHOT: ket luan phai la GIET.
        ph_a = sinh_dau_phien()
        k_a = d / f"k{ord(ch):04x}a.jsonl"
        kh_a = KhungPhat(k_a, ph_a, "m", 1)
        for ten, _ in CA:
            kh_a.vao_ca(ten)
            kh_a.phat(NHAN_DO_CHOT if ten == "T1" else NHAN_DAT, ct if ten == "T1" else "")
        kh_a.dong_luot(1)
        tt_a, ly_a = doc_kenh(k_a, ph_a, "m", 1, ("T1",), 1)
        chot(tt_a == GIET, "r518")

        # (B) duong DO_KHAC: `chi_tiet` phai ve NGUYEN VAN trong ly do.
        ph_b = sinh_dau_phien()
        k_b = d / f"k{ord(ch):04x}b.jsonl"
        kh_b = KhungPhat(k_b, ph_b, "m", 1)
        for ten, _ in CA:
            kh_b.vao_ca(ten)
            kh_b.phat(NHAN_DO_KHAC if ten == "T1" else NHAN_DAT, ct if ten == "T1" else "")
        kh_b.dong_luot(1)
        tt_b, ly_b = doc_kenh(k_b, ph_b, "m", 1, ("T1",), 1)
        chot(tt_b == KHONG_DO_DUOC, "r518")
        chot(ct in ly_b, "r518")



def r519_dich_phai_duoc_xac_thuc_truoc_khi_cap_tin_dung(d: Path):
    """F01 (luot 10) — `dich` la DU LIEU MO TA, phai xac thuc TRUOC khi cap GIET.

    Cross-review luot 10 (HUONG 7) dung phan chung: doi DUY NHAT descriptor dau
    cua `DOT_BIEN` thanh `(ten cu, (), neo cu, neo cu)` — dich RONG, va ban "thay"
    y het ban "neo" nen KHONG doi mot byte nao — roi chay TRON bo kiem. Ket qua:
    muc ay duoc ghi `0/0`, tong `MUTANT giet=10 khong-giet=0 khong-do-duoc=0`,
    tu kiem `18/18`, tu dot bien `64/64`, **`rc=0`**. Cong XANH trong khi khong
    do gi.

    Goc loi la mot dong: `if do_chot == set(dich)`. Phep so tap DUNG khi CA HAI
    ve rong. Khong ca nao chet, khong byte nao doi, van GIET.

    VI SAO NANG HON MOT LOI CAU HINH. Packet nay sinh ra de chan "cap tin dung
    cho thu chet vi ly do VO CAN". Day la mat cuc doan cua chinh benh ay: cap tin
    dung cho thu **KHONG chet**. Va no o TANG TREN CUNG — bo cham san pham — chu
    khong o tang meta.

    HAI CHOT DOC LAP, do HAI thu khac nhau, khong thay nhau duoc:
      (A) `dich` khong rong + moi ten trong `dich` phai la ca CO THAT;
      (B) `thay != neo` — mot muc khong doi byte nao la loi cau hinh.
    Chi co (B) thi mot muc `dich=()` van cap GIET khi dot bien CO doi byte.
    Chi co (A) thi mot muc `neo == thay` van chay va bao "khong giet" thay vi
    noi thang cau hinh sai. Reviewer canh bao dung: kiem byte KHONG loai duoc
    dot bien TUONG DUONG ve hanh vi, nen (B) khong duoc dung thay (A).

    Huong tu choi la KDD, khong phai KHONG_GIET: descriptor sai la loi CAU HINH,
    khong phai ket luan ve suc manh cua bo test.
    """
    ph = sinh_dau_phien()
    TEN = [x for x, _ in CA]

    def kenh_day_du(ten_tep, do_chot=()):
        k = d / ten_tep
        kh = KhungPhat(k, ph, "m", 1)
        for x in TEN:
            kh.vao_ca(x)
            kh.phat(NHAN_DO_CHOT if x in do_chot else NHAN_DAT)
        kh.dong_luot(1 if do_chot else 0)
        return k

    # (A1) dich RONG + khong ca nao chet  -> phai KDD, KHONG duoc GIET.
    k0 = kenh_day_du("rong.jsonl")
    tt, ly = doc_kenh(k0, ph, "m", 1, (), 0)
    chot(tt == KHONG_DO_DUOC, "r519")
    chot("dich RONG" in ly, "r519")

    # (A2) dich mang ten ca KHONG ton tai -> KDD (truoc kia tra KHONG_GIET,
    #      tuc lan mot loi CAU HINH vao mot ket luan ve suc manh bo test).
    k1 = kenh_day_du("la.jsonl", do_chot=("T1",))
    tt, ly = doc_kenh(k1, ph, "m", 1, ("T99",), 1)
    chot(tt == KHONG_DO_DUOC, "r519")
    chot("KHONG ton tai" in ly, "r519")

    # (A3) DOI CHUNG DUONG: dich hop le van GIET binh thuong. Thieu o nay thi
    #      mot ban "va" bang cach tu choi TAT CA van qua duoc (A1)+(A2).
    tt, _ = doc_kenh(k1, ph, "m", 1, ("T1",), 1)
    chot(tt == GIET, "r519")

    # (B) muc dot bien KHONG doi byte nao phai bi TU CHOI ngay khi ap.
    m = _nap_ban_sao(d / "noop")
    # Neo phai la neo THAT cua TOOL (chay_dot_bien ap len tep san pham, khong
    # phai tep test) — neo bia se chet o phep kiem duy nhat TRUOC khi toi chot
    # noop, tuc ca se do vi ly do VO CAN. Dung lai neo cua muc dau bang.
    neo_that = DOT_BIEN[0][2]
    m.DOT_BIEN = [("noop-gia", ("T1",), neo_that, neo_that)]
    # CHAN duong PHONG bang mot ban ghi lai. Neu de `chay_dot_bien` phong con
    # THAT thi khi chot noop bi go (dot bien `bo-tu-choi-dot-bien-noop`) ca nay
    # se chay mot mutant that — va vi con KE THUA `CHI_TU_KIEM`, con chau lai
    # chay tu kiem => DE QUY KHONG DAY. Da tra gia: 526 tien trinh song, OOM.
    # Ban ghi lai vua NHANH vua do duoc THEM mot dieu: chot phai raise TRUOC khi
    # bat ky lan phong nao xay ra, khong phai "raise o dau do sau do".
    da_phong = []

    def khong_phong(*_a, **_k):
        da_phong.append(1)
        return KHONG_GIET, "", 1

    m.chay_mot_mutant = khong_phong
    try:
        m.chay_dot_bien()
    except AssertionError as exc:
        chot("KHONG doi byte nao" in str(exc), "r519")
    else:
        chot(False, "r519")
    chot(da_phong == [], "r519")

    # (D) F05 — con so IN RA phai la so dich PHAN BIET. `("T3","T3","T5")` tung
    #     in `3/3` trong khi phep so o `doc_kenh` dung `set(dich)` nen chi 2 ca
    #     chet. Mot bo cham in con so phong len la mot bo cham noi doi nhe.
    m_d = _nap_ban_sao(d / "demdich")
    m_d.DOT_BIEN = [("trung-gia", ("T3", "T3", "T5"), neo_that, neo_that + " ")]
    m_d.chay_mot_mutant = lambda *a, **k: (m_d.GIET, "", 1)
    ra_d = io.StringIO()
    with contextlib.redirect_stdout(ra_d):
        m_d.chay_dot_bien()
    dong_d = ra_d.getvalue()
    chot("| T3,T5 | 2/2" in dong_d, "r519")
    chot("3/3" not in dong_d, "r519")

    # (C) con cua `chay_mot_mutant` phai o DUNG che do mutant: co `CHI_TU_KIEM`
    #     cua CHA khong duoc chay sang con (neu chay sang thi con lai chay tu
    #     kiem => de quy). Do bang cach chan `run` va soi CHINH env da truyen.
    m2 = _nap_ban_sao(d / "chedo")
    env_con = {}

    def run_soi(args, cwd, check=True, env=None):
        env_con.update(env or {})
        return subprocess.CompletedProcess(args, 1, "", "")

    m2.run = run_soi
    with _moi_truong(**{"NHANH_DON_DUOC_CHI_TU_KIEM": "1"}):
        m2.chay_mot_mutant(d / "chedo", "x", ("T1",))
    chot("NHANH_DON_DUOC_CHI_TU_KIEM" not in env_con, "r519")
    chot(env_con.get("NHANH_DON_DUOC_KHONG_DOT_BIEN") == "1", "r519")


def r520_loi_phong_con_phai_o_lai_trong_vong_chay_lai(d: Path):
    """F02 (luot 10) — `OSError` luc PHONG con khong duoc thoat khoi vong `(1,2)`.

    Cross-review luot 10 (HUONG 8) do bang tai nguyen THAT: ha `RLIMIT_NOFILE`
    quanh lan phong dau ⇒ `subprocess.run` nem `[Errno 24] Too many open files`;
    nhat ky lan thu chi `[1]`, ham thoat bang NGOAI LE thay vi bo ba
    (trang thai, ly do, so lan). Tra lai tai nguyen thi cung mutant GIET binh
    thuong ⇒ day la loi thoang qua, dung loai ma lan thu HAI sinh ra de cuu.

    Vi sao vo fail-close cua luot 7 KHONG che duoc: no nam TRONG `doc_kenh`, ma
    `doc_kenh` chi duoc goi SAU khi `run` tra ve. `check=False` cung khong giup —
    no chi tat phep nem theo MA THOAT, khong bien ngoai le KHOI CHAY thanh
    `CompletedProcess`. Tuc M3 (chay lai mot lan) da duoc thuc hien o duong DOC
    ma bo sot o duong PHONG.

    Ca nay dung `run` gia nem `OSError` dung lan DAU rồi tra ve binh thuong lan
    sau — mo phong TRANG THAI (tai nguyen can roi hoi phuc), khong dien kich ban.

    BA chot, vi mot minh khong du:
      (1) loi thoang qua  -> phai di tiep lan 2 va GIET, nhat ky dung `[1, 2]`;
      (2) loi KEO DAI     -> phai KDD sau DUNG hai lan, giu nguyen `OSError`;
      (3) doi chung duong -> khong loi thi van GIET o lan 1.
    Thieu (2) thi mot ban "va" bang cach lap vo han van qua; thieu (1) thi mot
    ban "va" bang cach bien moi loi thanh KDD ngay lap tuc cung qua.
    """
    cua = []                             # lop hai: doi tuong CA NAY tao, doc lap so dang ky

    def dung_mod(so_lan_hong):
        m = _nap_ban_sao(d / f"phong-{so_lan_hong}-{secrets.token_hex(4)}")
        goi = []
        that = m.run

        def run_gia(args, cwd, check=True, env=None):
            goi.append(len(goi) + 1)
            if len(goi) <= so_lan_hong:
                raise _tiem(cua.append(e := OSError(24, "Too many open files")) or e)   # r2 M2
            return that(args, cwd, check=check, env=env)

        m.run = run_gia
        return m, goi

    # Con TOI GIAN — co y, va day la mot phep DANH DOI da do chu khong phai cat goc.
    # Ca nay do duong PHONG + CHAY LAI cua `chay_mot_mutant`; noi dung con KHONG
    # thuoc thu dang do. Cho con chay tron 8 ca T that thi moi lan goi ton ~1,4 s,
    # ma `chay_dot_bien_tu_kiem` chay LAI CA BO tu kiem cho MOI muc trong bang
    # (68 muc) — do duoc: bo kiem tu 112 s vot len >10 phut roi BI GIET.
    # Con toi gian van nap tep GOC va dung `KhungPhat` THAT, nen khong chep lai
    # dinh dang kenh (chep lai la hai ban se troi lech).
    STUB = (
        "import importlib.util, os\n"
        "from pathlib import Path\n"
        "s = importlib.util.spec_from_file_location('goc', r'@@GOC@@')\n"
        "m = importlib.util.module_from_spec(s)\n"
        "s.loader.exec_module(m)\n"
        "kh = m.KhungPhat(Path(os.environ[m.KENH_ENV]), os.environ[m.DAU_PHIEN_ENV],\n"
        "                 os.environ[m.MUTANT_ENV], int(os.environ[m.LAN_THU_ENV]))\n"
        "for _t, _ in m.CA:\n"
        "    kh.vao_ca(_t)\n"
        "    kh.phat(m.NHAN_DO_CHOT if _t == 'T1' else m.NHAN_DAT)\n"
        "kh.dong_luot(1)\n"
        "raise SystemExit(1)\n"
    ).replace("@@GOC@@", str(Path(__file__).resolve()))

    def chay(m, thu_muc):
        bs = thu_muc / "bs"
        bs.mkdir(parents=True, exist_ok=True)
        (bs / Path(m.__file__).name).write_text(STUB, encoding="utf-8", newline="\n")
        # Bo chấm CUA CHINH packet nay da bat loi cua ban va: khi dot bien
        # `bo-bat-loi-phong-con` go chot F02 ra thi `OSError` THOAT thang vao
        # than ca, ca chet bang DO_KHAC va bo cham xep dung la TIN DUNG GIA.
        # Doi thanh tin hieu chot cua CHINH ca — cung nep r517 da dung.
        try:
            return m.chay_mot_mutant(bs, Path(m.__file__).stem, ("T1",))
        except Exception as exc:                  # noqa: BLE001
            raise TinHieuChotCa(f"chay_mot_mutant nem {type(exc).__name__}: {exc}")
        finally:
            _bo_cua(cua)                         # lop hai trong FINALLY: ca chet giua chung van don

    # (1) hong DUNG mot lan -> lan hai cuu duoc.
    m1, goi1 = dung_mod(1)
    tt1, _, lan1 = chay(m1, d / "thoang-qua")
    chot(goi1 == [1, 2], "r520")
    chot((tt1, lan1) == (GIET, 2), "r520")

    # (2) hong CA HAI lan -> KDD sau dung hai lan, giu nguyen loai loi.
    m2, goi2 = dung_mod(2)
    tt2, ly2, lan2 = chay(m2, d / "keo-dai")
    chot(goi2 == [1, 2], "r520")
    chot((tt2, lan2) == (KHONG_DO_DUOC, 2), "r520")
    chot("OSError" in ly2 and "phong duoc tien trinh con" in ly2, "r520")

    # (3) doi chung duong: khong loi thi GIET ngay lan 1.
    m3, goi3 = dung_mod(0)
    tt3, _, lan3 = chay(m3, d / "sach")
    chot((tt3, lan3, goi3) == (GIET, 1, [1]), "r520")



def r521_dich_mot_lan_doc_khong_duoc_bi_tieu_thu(d: Path):
    """F04 (luot 11) — `dich` la iterable MOT-LAN-DOC thi khong duoc bi TIEU THU.

    Huong do den tu cross-review luot 11 (`evidence-r11/target-types.log`). Luot
    ay bi bo loc nen cat truoc khi kip ghi `VERDICT.md`, nhung log probe con
    nguyen; phien chinh do lai va xac nhan tung ca.

    GOC LOI — va day la cho dang nho nhat cua ca luot: ban va F01 (luot 10) doc
    `dich` BA lan (`not dich`, `set(dich) - ten_ca`, roi `set(dich)`). Voi mot
    iterator/generator, lan doc DAU tieu thu no, nen `set(dich)` cuoi cung ra
    RONG va phep so `do_chot == set(dich)` LAI dung khi khong ca nao chet.
    Tuc ban va sinh ra de chan "cap GIET cho thu khong chet" TU TAI TAO dung cai
    lo ay, qua mot cua khac. Do duoc tren ban nguyen goc cua `2e7ec60`:

        dich = ("T1",)                -> KHONG_GIET   (dung)
        dich = iter(("T1",))          -> GIET         (SAI)
        dich = (x for x in ("T1",))   -> GIET         (SAI)
        dich = iter(())               -> GIET         (SAI)

    va lan chay THAT voi con that (`iterator-T1-real-child`) cho kenh 8 ca DAT,
    khong ca nao DO_CHOT, ma ket qua van `GIET`.

    HAI CHOT cho HAI DUONG VAO, khong cai nao thay cai nao:
      (A) goi TRUC TIEP `doc_kenh` — vat hoa o VO `doc_kenh`;
      (B) qua `chay_mot_mutant` — vat hoa TRUOC vong `(1, 2)`, vi o day con phai
          song qua HAI lan thu: neu chi vat hoa trong `doc_kenh` thi lan thu 1
          da tieu thu iterator cua NGUOI GOI, lan thu 2 nhin thay RONG.
    Bo bat ky chot nao cung co dau vao phan biet duoc => KHONG tuong duong.
    """
    ph = sinh_dau_phien()
    k = d / "k.jsonl"
    kh = KhungPhat(k, ph, "m", 1)
    for ten, _ in CA:
        kh.vao_ca(ten)
        kh.phat(NHAN_DAT)
    kh.dong_luot(0)

    # (A) moi dang mot-lan-doc phai cho DUNG ket qua nhu tuple.
    mong = doc_kenh(k, ph, "m", 1, ("T1",), 0)
    chot(mong[0] == KHONG_GIET, "r521")
    chot(doc_kenh(k, ph, "m", 1, iter(("T1",)), 0) == mong, "r521")
    chot(doc_kenh(k, ph, "m", 1, (x for x in ("T1",)), 0) == mong, "r521")
    tt, ly = doc_kenh(k, ph, "m", 1, iter(()), 0)
    chot(tt == KHONG_DO_DUOC and "dich RONG" in ly, "r521")

    # (B) qua `chay_mot_mutant`: CA HAI lan thu phai nhan DUNG cung mot `dich`.
    m = _nap_ban_sao(d / "vong")
    nhan_duoc = []

    def doc_gia(duong, dau_phien, mutant, lan_thu, dich, rc_that=None):
        nhan_duoc.append(tuple(dich))
        return (m.KHONG_DO_DUOC, "ep chay lai") if lan_thu == 1 else (m.GIET, "")

    m.doc_kenh = doc_gia
    m.run = lambda args, cwd, check=True, env=None: subprocess.CompletedProcess(args, 1, "", "")
    bs = d / "vong" / "bs"
    bs.mkdir(parents=True, exist_ok=True)
    tt2, _, lan2 = m.chay_mot_mutant(bs, "x", (y for y in ("T1", "T2")))
    chot(nhan_duoc == [("T1", "T2"), ("T1", "T2")], "r521")
    chot((tt2, lan2) == (GIET, 2), "r521")

    # (C) DUONG THU BA: `chay_dot_bien` phai in DUNG dong bao cao. `chay_mot_mutant`
    #     gan lai `dich` o pham vi CUC BO cua no, nen iterator cua NGUOI GOI van bi
    #     tieu thu — day la cho ban va luot 11 bo sot, luot 12 tim ra.
    #     Do bang mot `chay_mot_mutant` gia TIEU THU dich Y HET ban that (`tuple(dich)`)
    #     roi tra GIET: hop dong can do la "bat ke callee lam gi voi iterable, dong
    #     bao cao cua CALLER phai dung". Dung ban gia vi ban that phong con that
    #     (~1,4 s) va `chay_dot_bien_tu_kiem` chay lai ca bo nay 73 lan.
    def in_ra(dich_vao):
        mm = _nap_ban_sao(d / f"bc-{secrets.token_hex(4)}")
        e = DOT_BIEN[0]
        mm.DOT_BIEN = [(e[0], dich_vao, e[2], e[3])]

        def mutant_gia(ban_sao, ten, dich):
            tuple(dich)                      # TIEU THU y het ban that
            return mm.GIET, "", 1

        mm.chay_mot_mutant = mutant_gia
        ra = io.StringIO()
        with contextlib.redirect_stdout(ra):
            mm.chay_dot_bien()
        return ra.getvalue().strip()

    mong_in = in_ra(("T3", "T5"))
    chot("| T3,T5 | 2/2" in mong_in, "r521")
    chot(in_ra(iter(("T3", "T5"))) == mong_in, "r521")
    chot(in_ra(x for x in ("T3", "T5")) == mong_in, "r521")


def r522_loi_phong_ngoai_oserror_cung_phai_o_lai_vong(d: Path):
    """F06 (luot 11) — `OSError` MOT MINH khong du o duong phong con.

    Cross-review luot 11 (`evidence-r11/exec-non-oserrors.log`) do duoc HAI loai
    ngoai le sinh NGAY LUC PHONG ma KHONG phai `OSError`, nen chung van thoat
    khoi vong `(1, 2)` du ban va F02 da co:

        ten mutant chua byte NUL   -> ValueError: embedded null byte
        ten mutant chua surrogate  -> UnicodeEncodeError: ... surrogates not allowed

    Ca hai den tu chinh `subprocess` khi no ma hoa `env`, tuc cung LOP voi F02
    (that bai KHOI CHAY, chua co tien trinh nao) chu khong phai loi logic.

    Van bat HEP theo loai — `(OSError, ValueError, UnicodeError)` — chu khong
    `except Exception`: mot vo qua rong se nuot ca loi lap trinh va bien mot ca
    do THAT thanh "khong do duoc", tuc doi mot bao dong that lay mot bao dong gia.

    BA chot: loi keo dai -> KDD sau DUNG hai lan, giu nguyen loai loi · loi
    thoang qua -> lan hai cuu duoc · doi chung duong -> khong loi thi GIET ngay
    lan 1. Thieu chot cuoi thi mot ban "va" bien MOI thu thanh KDD van qua.
    """
    def dung(*loi):
        m = _nap_ban_sao(d / f"le-{secrets.token_hex(4)}")
        goi = []

        def run_gia(args, cwd, check=True, env=None):
            goi.append(len(goi) + 1)
            e = loi[len(goi) - 1] if len(goi) <= len(loi) else None
            if e is not None:
                raise e
            return subprocess.CompletedProcess(args, 1, "", "")

        m.run = run_gia
        m.doc_kenh = lambda *a, **k: (m.GIET, "")
        bs = d / f"bs-{secrets.token_hex(4)}"
        bs.mkdir(parents=True, exist_ok=True)
        return m, goi, bs

    def goi_mutant(m, bs):
        """Bo cham cua CHINH packet nay da bat: khi dot bien thu hep lop bat thi
        `ValueError` THOAT vao than ca, ca chet bang DO_KHAC va bi xep dung la
        TIN DUNG GIA. Doi thanh tin hieu chot cua ca — nep r517/r520."""
        try:
            return m.chay_mot_mutant(bs, "x", ("T1",))
        except Exception as exc:                  # noqa: BLE001
            raise TinHieuChotCa(f"chay_mot_mutant nem {type(exc).__name__}: {exc}")

    def surrogate():
        return UnicodeEncodeError("utf-8", "x" + chr(0xD800), 1, 2, "surrogates not allowed")

    for ten_loi, tao in (("ValueError", lambda: ValueError("embedded null byte")),
                         ("UnicodeEncodeError", surrogate)):
        # keo dai ca hai lan -> KDD sau dung 2 lan, giu nguyen loai loi
        m, goi, bs = dung(tao(), tao())
        tt, ly, lan = goi_mutant(m, bs)
        chot(goi == [1, 2], "r522")
        chot((tt, lan) == (KHONG_DO_DUOC, 2), "r522")
        chot(ten_loi in ly and "phong duoc tien trinh con" in ly, "r522")
        # thoang qua -> lan hai cuu duoc
        m, goi, bs = dung(tao())
        tt, _, lan = goi_mutant(m, bs)
        chot((goi, tt, lan) == ([1, 2], GIET, 2), "r522")

    # doi chung duong: khong loi thi GIET ngay lan 1
    m, goi, bs = dung()
    tt, _, lan = goi_mutant(m, bs)
    chot((goi, tt, lan) == ([1], GIET, 1), "r522")



def r523_ban_sao_tuong_doi_khong_duoc_lam_lech_kenh(d: Path):
    """R13-F01 (luot 13) — cach VIET doi so khong duoc doi ket qua do.

    Cross-review luot 13, HUONG 6. `chay_mot_mutant` dung `ban_sao` theo HAI he
    quy chieu cung luc: lam goc dung `kenh` (truyen nguyen chuoi qua `KENH_ENV`)
    va lam `cwd` cua con. Duong TUONG DOI vi the bi ghep hai lan:

        cwd cha = P, doi so = r  ->  con chay tai P/r, duoc bao mo r/.ket-qua-N
                                 ->  duong hieu luc P/r/r/.ket-qua-N   (khong ton tai)

    Do duoc tren ban nguyen goc, CUNG MOT thu muc vat ly, chi doi cach viet:
        tuyet doi        -> GIET, 1 lan, 9 ban ghi, DO_CHOT = T3,T5,T8
        tuong doi        -> KHONG DO DUOC, 2 lan, 0 ban ghi, FileNotFoundError
        tuong doi + resolve -> GIET, 1 lan

    Huong hong la FAIL-CLOSE (mat kha nang do, khong cap GIET gia) nhung van sai:
    launcher tu lam hong phep do cua chinh no voi mot doi so `Path` HOAN TOAN
    HOP LE, va lan thu hai khong cuu duoc vi no lap lai dung sai dia chi ay.

    Ca nay dung cung mot thu muc that cho ca hai cach viet — duong tuong doi tinh
    bang `os.path.relpath` tu cwd hien hanh, nen KHONG phai doi cwd (doi cwd giua
    bo test la mot nguon nhieu khac). Con la ban TOI GIAN nhu r520: no chi doc
    `KENH_ENV` roi phat qua `KhungPhat` THAT, du de lo bug dia chi ma khong ton
    ~1,4 s moi lan.
    """
    STUB = (
        "import importlib.util, os\n"
        "from pathlib import Path\n"
        "s = importlib.util.spec_from_file_location('goc', r'@@GOC@@')\n"
        "m = importlib.util.module_from_spec(s)\n"
        "s.loader.exec_module(m)\n"
        "kh = m.KhungPhat(Path(os.environ[m.KENH_ENV]), os.environ[m.DAU_PHIEN_ENV],\n"
        "                 os.environ[m.MUTANT_ENV], int(os.environ[m.LAN_THU_ENV]))\n"
        "for _t, _ in m.CA:\n"
        "    kh.vao_ca(_t)\n"
        "    kh.phat(m.NHAN_DO_CHOT if _t == 'T1' else m.NHAN_DAT)\n"
        "kh.dong_luot(1)\n"
        "raise SystemExit(1)\n"
    ).replace("@@GOC@@", str(Path(__file__).resolve()))

    # WP540 — temp mac dinh/supplied co the khac o dia voi cwd tren Windows;
    # relpath khi do nem ValueError. Chi fixture con can cung o dia voi cwd.
    # Context don fixture ca khi chot do, khong doi cwd hay temp policy toan cuc.
    with tempfile.TemporaryDirectory(prefix="r523-", dir=Path.cwd()) as td:
        m = _nap_ban_sao(d / f"bs-{secrets.token_hex(4)}")
        bs = Path(td).resolve() / Path(m.__file__).stem
        bs.mkdir()
        (bs / Path(m.__file__).name).write_text(STUB, encoding="utf-8", newline="\n")

        duong_tuong_doi = Path(os.path.relpath(bs, Path.cwd()))
        chot(not duong_tuong_doi.is_absolute() and duong_tuong_doi.resolve() == bs, "r523")
        tuyet_doi = m.chay_mot_mutant(bs, Path(m.__file__).stem, ("T1",))
        chot(tuyet_doi == (GIET, "", 1), "r523")
        # Cung fixture vat ly, nhung kenh phat append phai sach cho luot so sanh.
        (bs / ".ket-qua-1.jsonl").unlink()
        tuong_doi = m.chay_mot_mutant(duong_tuong_doi, Path(m.__file__).stem, ("T1",))
        # Chot THAT: cach VIET khong duoc doi ket qua. Thieu chot nay thi mot ban
        # "va" bang cach tu choi moi duong tuong doi van qua.
        chot(tuong_doi == tuyet_doi, "r523")



def r524_chan_doan_cua_con_khong_duoc_mat_o_lop_phan_hang(d: Path):
    r"""#568 — bo phan hang phai CHUYEN TIEP chan doan cua con, khong chi ten ca.

    Benh do duoc: `gate-registry` DO tren head 57f85a1 cua PR #567 voi dung mot
    dong `TIN DUNG GIA: ca chet vi loi VO CAN ['r506']`. Tu do KHONG cach nao
    biet r506 nem AssertionError (git that bai — `run(check=True)` nem lop ay
    TRAN), TypeError, OSError hay TimeoutExpired. Bon nguyen nhan can bon cach
    xu KHAC NHAU, va con DA IN du thong tin ay; cha vut no di o lop cuoi.

    Ca nay do THANG hai ham trich/goi, KHONG chay lai ca vong mutant (~2,4s moi
    luot): san pham dang do la `_khoi_chan_doan` + `_goi_chan_doan`, va dau vao
    la mot stdout DUNG DINH DANG do chinh `chay_tu_kiem` sinh ra.

    BON chot doc lap — moi chot mot DUONG VAO rieng, de mot dot bien go tung
    cai deu doi mau duoc (bai hoc "va dung cho duoc chi roi bo sot duong thu ba"):
      (1) than NGOAI LE phai toi noi: ca KIEU lan THONG DIEP, khong chi ten ca;
      (2) than NHIEU DONG phai toi noi — mot AssertionError cua `run()` mang ca
          stdout lan stderr cua git, nen dong thu hai moi la cho co chan doan;
      (3) khi phai CAT thi phai KHAI so ky tu da cat — nuot lang la dung benh
          dang chua, chi nho hon;
      (4) PHAN HANG khong doi: tap ten ca `_khoi_chan_doan` tra ve phai BANG
          tap ma mau cu (`^TU KIEM (r\d+): DO_KHAC`) bat duoc, tren cung dau vao.
    """
    stdout = (
        "TU KIEM r505: DAT\n"
        "TU KIEM r506: DO_KHAC — AssertionError: rc=128: git init --bare\n"
        "dong-thu-hai-MOC-A\n"
        "dong-thu-ba\n"
        "TU KIEM r507: DAT\n"
        "TU KIEM r512: DO_CHOT — chot r512 hong\n"
        "TU KIEM: 21/23\n"
    )
    khoi = _khoi_chan_doan(stdout, "DO_KHAC")
    chot([ca for ca, _ in khoi] == ["r506"], "r524")
    than = khoi[0][1]
    # (1) kieu VA thong diep, khong chi ten ca
    chot("AssertionError" in than and "rc=128" in than, "r524")
    # (2) dong thu HAI phai toi noi — khong duoc dung o cuoi dong dau
    chot("dong-thu-hai-MOC-A" in than, "r524")
    # ...va khoi phai DUNG o ranh gioi, khong nuot dong `TU KIEM` ke tiep
    chot("r507" not in than and "21/23" not in than, "r524")
    # (3) cat thi phai KHAI so ky tu da cat
    dai = "x" * (TRAN_CHAN_DOAN + 37)
    goi = _goi_chan_doan(dai)
    chot("CAT" in goi and "37" in goi, "r524")
    chot(_goi_chan_doan("ngan") == "ngan", "r524")
    # (4) PHAN HANG khong doi — so voi CHINH mau cu
    cu = set(re.findall(r"^TU KIEM (r\d+): DO_KHAC", stdout, re.M))
    chot({ca for ca, _ in khoi} == cu == {"r506"}, "r524")
    # va nhanh DO_CHOT cung phai trich duoc, vi duong vao THU BA dung no
    chot([ca for ca, _ in _khoi_chan_doan(stdout, "DO_CHOT")] == ["r512"], "r524")


def r525_nhanh_thu_ba_phai_noi_vi_sao_ca_khi_con_chet_truoc_khi_in(d: Path):
    """#568 r2/M6 — ca SUY BIEN cua nhanh THU BA: con chet TRUOC khi in duoc gi.

    Benh: r1 dong ba nhanh in nhan o ca THUONG cua chung, roi bo sot ca SUY BIEN
    cua nhanh thu ba. Khi con chet vi mot ngoai le KHONG bat duoc, CPython thoat
    rc=1 va stdout RONG — khong nhan nao. Dinh tuyen: `do_khac` rong nen bo qua
    nhanh mot; `rc != 1` SAI vi rc DUNG BANG 1 nen bo qua nhanh hai; `do_chot ==
    dich` sai nen bo qua nhanh ba; roi vao `else`, in nhan tran roi lap `kh_chot`
    RONG => stderr mang nguyen nhan BI VUT.

    Ca nay goi CHINH `chay_dot_bien_tu_kiem`, chi thay `run` bang do gia kich ban
    hoa (stdout, rc, STDERR) — tuc do DUONG PHAN HANG that. Do gia cua `r516` luon
    tra stderr RONG, nen no di QUA duong nay ma khong thay gi; day la ly do lo song
    sot qua ca mot bo test co 80 dot bien.

    HAI o, va chung phai phan biet duoc bang DAU VAO — neu khong thi hai chot la
    bo TUONG DUONG va ta chi dang do MOT thu:
      (P2) suy bien: stdout RONG  => PHAI in stderr (mang chuoi moc)
      (P1) thuong  : co DO_CHOT   => PHAI in CHOT, va KHONG duoc in stderr
    """
    m = _nap_ban_sao(d)
    MOC = "MOC-STDERR-R525"
    tb = ("Traceback (most recent call last):\n"
          '  File "nhanh_don_duoc_test.py", line 1, in <module>\n'
          f"ModuleNotFoundError: No module named '{MOC}'\n")
    DICH = ("r515",)
    # M9 (r3) — do gia CU luon tra `tb` NGAN (~130 ky tu) nen A8 xanh ma thuc te
    # SAI: stderr THAT cua mot tien trinh con mang 425 ky tu canh bao dung TRUOC
    # nguyen nhan, va `_goi_chan_doan` cat TU DAU. Kich thich HEP HON hien thuc
    # la dung hinh dang TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO (lan thu 3, #568 r3).
    # O thu ba dung stderr DUNG HINH DANG THAT: rac dai hon TRAN_CHAN_DOAN,
    # nguyen nhan o CUOI.
    RAC = (r"ban_sao.py:2213: SyntaxWarning: invalid escape sequence '\d'" "\n"
           r'  """mot dong docstring dai, chep dung hinh dang that cua canh bao' "\n")
    tb_dai = RAC * 4 + tb
    kich = {
        "suy-bien": ("", 1, tb),
        "suy-bien-dai": ("", 1, tb_dai),
        "thuong": ("TU KIEM r511: DO_CHOT — chot cua ca r511 that bai\n"
                   "TU KIEM: 23/24\n", 1, tb),
    }

    def run_gia(args, cwd, check=True, env=None):
        out, rc, err = kich[Path(cwd).name]
        if Path(cwd).name == "thuong":
            out = re.sub(r"^TU KIEM: [0-9]+/[0-9]+\n", "", out, flags=re.MULTILINE)
            ids = [c for c, _, _ in m.TU_KIEM]
            out += f"TU KIEM: {len(ids) - 1}/{len(ids)}\n"
            Path(env[m.TU_KIEM_FILE_ENV]).write_text(json.dumps({"nonce": env[m.TU_KIEM_NONCE_ENV], "cases": ids}), encoding="utf-8")
        return subprocess.CompletedProcess(args, rc, out, err)

    m.run = run_gia

    def ghep(*phan):
        """Ghep neo LUC CHAY — viet nguyen van thi chinh than ca nay lam chuoi ay
        xuat hien THEM mot lan ngoai bang, va phep doi neo duy nhat se bac het."""
        return "".join(phan)

    NEO = ghep("    if not ", "duong.exists():")
    m.DOT_BIEN_TU_KIEM = [(ten, DICH, NEO, "    pass") for ten in kich]
    with contextlib.redirect_stdout(io.StringIO()) as ra, _vang_co_chu_y(m):
        giet, hong, khong_do = m.chay_dot_bien_tu_kiem()
    dong_in = ra.getvalue()

    # Tach theo TUNG MUC: mot chuoi co mat "o dau do" khong chung minh no o DUNG
    # muc can no — dung benh "loi khai rong hon phep do".
    khoi = {}
    hien = None
    for dong in dong_in.splitlines():
        if dong.startswith("DOT BIEN TU KIEM "):
            # "DOT BIEN TU KIEM <ten>" — BON tu roi moi toi ten, nen chi so 4.
            # Ban dau viet 3 va lay ra "KIEM": ca DO tren ma CHUA dot bien, roi
            # keo ca bang xuong 2/82 vi moi mutant khac cung thay r525 trong
            # `do_chot`. Mot ca do vi ly do VO CAN — dung benh ho hang.
            hien = dong.split()[4]
            khoi[hien] = []
        elif hien:
            khoi[hien].append(dong)
    chot(set(khoi) == set(kich), "r525")          # ca hai o deu THAT SU chay
    sb, th = "\n".join(khoi["suy-bien"]), "\n".join(khoi["thuong"])

    # (P2) suy bien: nguyen nhan PHAI toi noi
    chot(MOC in sb, "r525")
    chot("ModuleNotFoundError" in sb, "r525")
    # (P1) thuong: van in CHOT.
    #
    # #568 r5 / M14 — DONG `chot(MOC not in th, "r525")` DA BI BO. No cam mot the
    # ma A8 cua r2 KHONG doi: A8 chi noi "rc=1, stdout rong, stderr mang chuoi
    # moc => dong cha phai chua chuoi moc ay". Khong co ve cam.
    # Te hon, no BAC TRUOC mot trien khai giu CA HAI chan doan, tuc KHOA CHET
    # duong "con da bao mot chot roi CHET TIEP vi mot le khac" — duong ay co that
    # (do duoc: (giet,hong)=(0,1), in "CHOT r511", KHONG in nguyen nhan tren
    # stderr). Hinh dang loi MOI, dat ten trong dac ta r5:
    # CHOT-CAM-THU-DAC-TA-KHONG-DOI. Nguy hon mot chot yeu, vi mot chot yeu chi
    # khong bat duoc loi, con chot nay CHAN duong sua dung.
    # Hanh vi hien tai nay do bang `r532` va khai bang hang so co ten.
    chot("CHOT r511" in th, "r525")
    # (P3) A15 cua r3 — LOI KHAI TRUNG THUC ve mot HAN CHE, KHONG phai mot ca
    # xanh ve mot kha nang. Voi `TRAN_CHAN_DOAN` hien tai va huong cat TU DAU,
    # nguyen nhan nam o CUOI stderr KHONG toi duoc dong cha. Doi huong cat (cat
    # tu giua / uu tien duoi / loc canh bao) la MO RONG PHAM VI, NGOAI closure
    # r3 — xem dac ta 596e1614, luu y gan vao A15.
    sbd = "\n".join(khoi["suy-bien-dai"])
    chot(MOC not in sbd, "r525")            # nguyen nhan BI CAT — khai thang
    chot("…[CAT " in sbd, "r525")           # va cha PHAI noi la no da cat
    chot("SyntaxWarning" in sbd, "r525")    # cai toi noi la phan DAU, tuc rac
    # r7: hai crash thieu bang chung la KHONG DO DUOC; o thuong la hong.
    chot((giet, hong, khong_do) == (0, 1, 2), "r525")


def _dem_canh_bao_escape(ma: str, ten: str) -> int:
    r"""Dem canh bao `invalid escape sequence` khi BIEN DICH `ma`.

    Tach RIENG ra de `r526` do duoc HAI CHIEU bang CUNG mot phep do: ma that
    phai ra 0, va mot mau BAN co chu phai ra >= 1. Mot phep do chi chay mot
    chieu thi so 0 cua no khong phan biet duoc "sach" voi "khong do duoc gi".
    """
    with warnings.catch_warnings(record=True) as thu:
        warnings.simplefilter("always")
        compile(ma, ten, "exec")
    return sum(1 for w in thu if "escape sequence" in str(w.message))


def r526_ma_nguon_khong_duoc_sinh_canh_bao_escape_sequence(d: Path):
    r"""#568 r3/M7+M8 — chinh tep nay phai bien dich SACH tren Python >= 3.12.

    Benh do duoc tu goi chay Windows cua chu kho: hai docstring KHONG raw chua
    `\d` (dong 2213 va 2723, do `18d6519` cua r1 dua vao) khien MOI tien trinh
    con in 425 ky tu `SyntaxWarning` ra stderr TRUOC khi chay. `TRAN_CHAN_DOAN`
    = 400 va `_goi_chan_doan` cat TU DAU, nen 100% ngan sach bi rac chiem va
    nguyen nhan that bi cat sach. Hai nhanh doc `p.stderr` la nhanh `rc != 1`
    (M2 cua r1) va nhanh P2 (M6 cua r2) — dung hai nhanh danh cho "con chet
    truoc khi in duoc gi", tuc dung luc stderr la cho DUY NHAT con nguyen nhan.

    So do do duoc: nen `dc85dd0a` = 0 canh bao, `18d6519` = 2, `45ea292` = 2;
    `nen-*.err.txt` = 0 B con `ung-vien-*.err.txt` = 17 222 B moi luot.

    Vo hinh tren Python 3.11 (DeprecationWarning, im lang mac dinh) va hien tu
    3.12 (SyntaxWarning). CI ghim `python-version: "3.12"`, runner chay 3.12.14
    — nen day KHONG phai mot lo ly thuyet.

    A14 — phep do phai an DUNG tep dang chay. Doc mot BAN CHEP sach thi ca nay
    se XANH trong khi tep that BAN, tuc hinh dang TIN-HIEU-DO-CHINH-MA-TEST-GIA
    -MAO lan thu TU. Hai chot dau chan dung cho do, va co dot bien rieng.
    """
    import inspect as _ins
    nguon = Path(__file__).resolve()
    ma = nguon.read_text(encoding="utf-8")
    # #568 r4 / M12 — CROSS-REVIEW CODEX, P2 tren 1486689, DA TAI HIEN: hai chot
    # cu (`len > 50_000` va "ten ham co trong ma") chi xac thuc HINH DANG. Mot
    # ban chep SACH dai hon 50 000 ky tu co chua ten ham ay thoa CA HAI, nen ca
    # van DAT trong khi nguon dang chay BAN. Loi khai A14 rong hon phep do.
    #
    # KHONG the chung minh "van ban nay LA tep dang chay" tu chinh van ban. Thu
    # chung minh duoc la: PHEP DOC chua bi thay. Nen doc bang HAI DUONG DOC LAP
    # roi doi bang nhau TUNG BYTE — dot bien thay MOT duong van vo vi duong kia
    # khong doi. Day la loi khai HEP HON va DUNG, thay cho loi khai rong cua A14.
    #
    # KHAI THANG cho no KHONG chung minh: neu ai do thay duong HAI bang chinh
    # bieu thuc cua duong MOT, dang thuc thanh tam thuong va chot nay mu. Hai
    # dot bien di kem chi dong duong "thay mot duong bang HANG SACH".
    ma_2 = _ins.getsource(sys.modules[__name__])
    chot(ma == ma_2, "r526")
    chot(len(ma) > 50_000, "r526")
    # A13 — ve can do.
    chot(_dem_canh_bao_escape(ma, str(nguon)) == 0, "r526")
    # ... va phep do PHAI CO RANG. Dung `chr` de mau ban khong tu no lam chinh
    # tep nay ban tro lai — mot ca do "thanh cong" bang cach tai lap benh.
    mau_ban = "x = " + chr(34) * 3 + chr(92) + "d" + chr(34) * 3 + chr(10)
    chot(_dem_canh_bao_escape(mau_ban, "<mau-ban>") >= 1, "r526")


def r527_tien_de_hai_dau_phien_phai_do_duoc_ba_trang_thai(d: Path):
    """#593 M3/A1-A3 — `_hai_dau_phien_phan_biet` phai co BA trang thai phan
    biet duoc BANG DAU VAO, va chan tren phai CO THAT.

    Ba o, moi o mot bo sinh khac nhau — neu hai o khong phan biet duoc bang dau
    vao thi chung la bo TUONG DUONG va ta chi dang do MOT thu:
      (1) bo sinh HANG, khong gian 1  => KHONG DO DUOC, khong DAT, khong treo
      (2) chan tren do duoc bang SO LAN GOI nguon = 1 + TRAN (chot bang HANG SO,
          khong bang chinh `TRAN_RUT_DAU_PHIEN` — chot theo bien la tu noi mot
          dang thuc, dot bien ha tran xuong 0 se van "dung")
      (3) khong gian 256, gieo TAT DINH => luon ra hai dau KHAC, 1 000 luot
    """
    m = _nap_ban_sao(d)

    # (1) + (2) — bo sinh HANG, va DEM so lan goi.
    dem = {"n": 0}

    def hang():
        dem["n"] += 1
        return "DAU-PHIEN-HANG"

    m.sinh_dau_phien = hang
    try:
        m._hai_dau_phien_phan_biet()
    except m.TinHieuKhongDoDuoc as e:
        chot("PHAN BIET" in str(e), "r527")        # noi RO vi sao, khong nhan tran
    except m.TinHieuChotCa:
        chot(False, "r527")   # A3: KHONG duoc gia lam mot chot sai
    else:
        chot(False, "r527")   # A1: KHONG duoc lang le tra ve mot cap TRUNG
    # A1 — chan tren CO THAT: 1 lan rut dau + dung TRAN lan rut lai, khong hon.
    # 65 viet bang HANG SO co chu dich: xem docstring.
    chot(dem["n"] == 65, "r527")

    # (3) — khong gian 256, gieo tat dinh. Dung `random` chu khong `secrets`:
    # phep do nay phai LAP LAI DUOC, khong duoc doi theo luot chay.
    import random as _r
    rng = _r.Random(20260921)
    m.sinh_dau_phien = lambda: f"{rng.randrange(256):02x}" * 16
    for _ in range(1000):
        a, b = m._hai_dau_phien_phan_biet()
        chot(a != b, "r527")


def _chay_r508_tach_nguon_do(m, d: Path, so_luot: int) -> int:
    """#593 r1 / M1+M2 — chay CHINH `r508` cua ban sao `m` `so_luot` lan, TACH BA NGUON DO.

    Benh (TIEN-DE-HA-TANG-KHONG-DUOC-THANH-CHOT, do tren 18d42ca): vong (c2) cua
    `r528` bat `BaseException` va dem MOI ngoai le vao `do`, nen 2000 lan
    `OSError(28)` tiem vao `_kenh_tam` ra `chot cua ca r528 that bai` — mot chot
    THUOC TINH trong khi khong do duoc thuoc tinh nao, va nguyen nhan "dia day"
    MAT khoi thong bao. Doi chung duong, cung do ga, khong tiem: r528 DAT (2,0 s).

    Ba nguon do, ba cach xu, bat HEP theo loai — KHONG `except Exception` o day:
      · `TinHieuChotCa` cua ca long -> dem vao `do`: thuoc tinh SAI, ra DO_CHOT
      · `OSError` va con chau (dia day, het fd, het quyen) -> KHONG DO DUOC,
        mang LOAI + THONG DIEP + SO LAN, qua `TinHieuKhongDoDuoc`
      · moi thu khac (NameError, TypeError...) -> THOAT RA nguyen ven: mot loi
        lap trinh khong duoc bien thanh mot con so.
    Tra so lan chot cua `r508` that bai. `r543` do ca bon duong tren CHINH ham nay.
    """
    do = 0
    ha_tang: dict[str, list] = {}
    for i in range(so_luot):
        thu = d / f"r508-{i}"
        try:
            thu.mkdir(parents=True, exist_ok=True)
            m.r508_ban_ghi_luot_TRUOC_chi_khac_dau_phien(thu)
        except m.TinHieuChotCa:
            do += 1
        except OSError as loi_ha_tang:
            _ghi_ha_tang(loi_ha_tang)             # r2 M1 diem nuot: _chay_r508_tach_nguon_do
            ghi = ha_tang.setdefault(type(loi_ha_tang).__name__, [str(loi_ha_tang), 0])
            ghi[1] += 1
    if ha_tang:
        chi_tiet = "; ".join(f"{loai}: {msg} ({n} lan)" for loai, (msg, n) in ha_tang.items())
        # Gan roi `raise`: viet thang `raise TinHieuKhongDoDuoc(` o day se lam neo
        # cua muc `dau-phien-can-tran-ma-lang-le-tra-cap-trung` het DUY NHAT ngoai bang.
        khong_do = TinHieuKhongDoDuoc(
            f"tien de ha tang cua r528 (c2) hong trong {so_luot} luot — {chi_tiet}")
        raise khong_do
    return do


def r528_tien_de_khong_con_chap_duoi_chinh_dot_bien(d: Path):
    """#593 A9 — CHOT DUY NHAT chung minh benh DA HET, va no phai co doi chung.

    Phai chay duoi CHINH bo sinh cua dot bien `entropy-giu-mot-byte`. Duoi ma
    thuong khong gian la 2**128 nen "0 lan trung" dung mot cach VO NGHIA: mot
    phep do khong phan biet duoc "da chua" voi "chua tung benh" la mot phep do
    RONG. Do la vi sao ca nay do HAI VE bang CUNG mot bo sinh:
      (a) HINH DANG CU (hai lan rut doc lap) PHAI con chap — neu khong thi phep
          do nay mu, va moi con so cua ve (b) vo nghia
      (b) HINH DANG MOI (qua `_hai_dau_phien_phan_biet`) phai 0 lan

    N = 100 000 va ty le 1/256 => ve (a) ky vong ~390 lan. Xac suat no ra 0 la
    (255/256)**100000, tuc e**-390 — khong phai mot rui ro ta dang chay.
    """
    m = _nap_ban_sao(d)
    N = 100_000
    # Y HET `thay` cua muc `entropy-giu-mot-byte` trong DOT_BIEN_TU_KIEM.
    m.sinh_dau_phien = lambda: secrets.token_hex(16)[-2:] * 16

    cu = sum(1 for _ in range(N) if m.sinh_dau_phien() == m.sinh_dau_phien())
    chot(cu > 0, "r528")        # (a) phep do CO RANG

    moi = 0
    for _ in range(N):
        try:
            a, b = m._hai_dau_phien_phan_biet()
        except m.TinHieuKhongDoDuoc:
            # Khong gian 256 ma VAN can tran la mot that bai cua CHINH ca nay,
            # nen no phai ra DO_CHOT. De `TinHieuKhongDoDuoc` thoat ra thi bo
            # phan hang xep vao DO_KHAC = "chet vi loi VO CAN" = TIN DUNG GIA,
            # va mutant thanh `hong` du `dich` ghi dung ten. Da do that.
            chot(False, "r528")
        if a == b:
            moi += 1
    chot(moi == 0, "r528")      # (b) hai so BANG NHAU: 0 tren 100 000

    # (c) — CROSS-REVIEW CODEX, P2 tren 1486689, DA TAI HIEN: hai ve tren chi
    # chung minh HAM da chua, KHONG chung minh CA THAT da chua. Noi lai benh goc
    # vao chinh dong dau cua `r508` (`sinh_dau_phien(), sinh_dau_phien()`) ma giu
    # ham nguyen ven thi CA HAI ve tren van DAT — do duoc, khong phai lo ngai.
    # Do dung hinh dang TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO: chot mang ten A9 mà
    # khong he cham vao thu A9 hua.
    #
    # Hai chot duoi day dong dung cho ay:
    #   (c1) `r508` phai THAT SU di qua bo tien de — dem SO LAN GOI, tat dinh
    #   (c2) va chay that N508 luot duoi bo sinh ay, khong chap lan nao
    # N508 nho hon N vi moi luot `r508` dung he tep (~1,1 ms) chu khong chi rut
    # so; chot (c2) KHONG can can duoi xac suat nao — duoi ma da chua no la 0
    # voi xac suat 1 - (1/256)**64 moi luot.
    that = m._hai_dau_phien_phan_biet
    dem = {"n": 0}

    def dem_goi():
        dem["n"] += 1
        return that()

    m._hai_dau_phien_phan_biet = dem_goi
    N508 = 2000
    # #593 r1 — vong (c2) nam trong `_chay_r508_tach_nguon_do`: loi HA TANG ra
    # KHONG DO DUOC mang nguyen nhan, khong con bi `except BaseException` dem
    # vao `do` (do tren 18d42ca: 2000 x OSError(28) -> "chot cua ca r528 that bai").
    do = _chay_r508_tach_nguon_do(m, d, N508)
    chot(dem["n"] == N508, "r528")   # (c1) ca THAT co di qua bo tien de
    chot(do == 0, "r528")            # (c2) va khong chap lan nao


def r529_tach_dong_phai_bang_dung_bo_doc_cu(d: Path):
    r"""#568 r4 / M10 — tap dong `_khoi_chan_doan` nhan phai BANG DUNG tap bo doc cu.

    Benh (cross-review codex, P1 tren 1486689, da tai hien): ban truoc tach dong
    bang `str.splitlines()`, von coi CHIN ky tu ngoai `
` la het dong, trong khi
    bo doc cu `re.findall(..., re.M)` thi KHONG — `$` voi re.M chi khop truoc `
`
    va o cuoi chuoi. Chenh lech ay cho MA SAN PHAM DOAT DUOC TEN CA:

        stdout = "TU KIEM r501: DAT" + U+2028 + "TU KIEM r512: DO_CHOT" + LF
        regex CU -> set()          splitlines -> {"r512"}

    Voi rc=1 va dich=("r512",), cung mot dau vao chuyen tu `hong` sang GIET. Day
    la mot duong CAP GIET GIA, dung lop loi ma `r511` ton tai de chan — va M3 cua
    r1 tu khai "tap ten ca KHONG DOI so bo doc cu", loi khai ay SAI.

    BA o, va o thu ba la DOI CHUNG DUONG — thieu no thi mot bo doc khong bao gio
    nhan gi ca cung qua duoc o thu hai.
    """
    m = _nap_ban_sao(d)
    # (1) Hang so phai DAN XUAT duoc tu chinh `splitlines` luc chay. Chep tay ma
    #     thieu mot ky tu thi o (2) van xanh trong khi van ho dung ky tu do.
    thua = {c for c in map(chr, range(0x110000))
            if len(("a" + c + "b").splitlines()) > 1} - {chr(10)}
    chot(set(m.KY_TU_TACH_DONG_LE) == thua, "r529")
    # (2) Voi TUNG ky tu le, hai bo doc phai cho CUNG mot tap ten ca.
    cu = re.compile(r"^TU KIEM (r\d+): DO_CHOT", re.M)
    for c in m.KY_TU_TACH_DONG_LE:
        s = ("TU KIEM r501: DAT" + c
             + "TU KIEM r512: DO_CHOT - gia mao" + chr(10))
        chot(set(cu.findall(s))
             == {ca for ca, _ in m._khoi_chan_doan(s, "DO_CHOT")}, "r529")
    # (3) DOI CHUNG DUONG: voi LF THAT, CA HAI bo doc phai thay r512.
    s = ("TU KIEM r501: DAT" + chr(10)
         + "TU KIEM r512: DO_CHOT - that" + chr(10))
    chot(set(cu.findall(s)) == {"r512"}, "r529")
    chot({ca for ca, _ in m._khoi_chan_doan(s, "DO_CHOT")} == {"r512"}, "r529")


def r530_hai_nhanh_chuyen_tiep_con_lai_phai_co_dot_bien_canh(d: Path):
    r"""#568 r4 / M11 — nhanh `DO_KHAC` va nhanh `rc != 1` phai THAT SU in chan doan.

    Benh (cross-review codex, P2 tren 1486689, da tai hien): thay CA HAI dong
    `print` chuyen tiep bang `pass` thi `r516 DAT`, `r524 DAT`, `r525 DAT`. Tuc
    bo tron phan chuyen tiep o hai nhanh ay ma moi ca lien quan van xanh — dung
    cai benh #568 cam ket khoa, va A1/A2 chua khoa duoc no o LOP CHA. `r524` chi
    do hai helper; `r525` do nhanh CUOI; `r516` kiem phan hang nhung cho `stderr`
    rong.

    HAI o, phan biet duoc bang DAU VAO:
      (P1) `vo-can` : stdout co DO_KHAC  => nhanh mot  => phai in "VO CAN <ca>: "
      (P2) `rc-khac`: stdout RONG, rc=7  => nhanh hai  => phai in "stderr: "
    """
    m = _nap_ban_sao(d)
    MOC_VC, MOC_SE = "MOC-VOCAN-R530", "MOC-STDERR-R530"
    kich = {
        "vo-can": ("TU KIEM r511: DO_KHAC - RuntimeError: " + MOC_VC + chr(10),
                   1, ""),
        "rc-khac": ("", 7, "Traceback ... OSError: " + MOC_SE + chr(10)),
    }

    def run_gia(args, cwd, check=True, env=None):
        out, rc, err = kich[Path(cwd).name]
        if Path(cwd).name == "vo-can":
            out = re.sub(r"^TU KIEM: [0-9]+/[0-9]+\n", "", out, flags=re.MULTILINE)
            ids = [c for c, _, _ in m.TU_KIEM]
            out += f"TU KIEM: {len(ids) - 1}/{len(ids)}\n"
            Path(env[m.TU_KIEM_FILE_ENV]).write_text(json.dumps({"nonce": env[m.TU_KIEM_NONCE_ENV], "cases": ids}), encoding="utf-8")
        return subprocess.CompletedProcess(args, rc, out, err)

    m.run = run_gia

    def ghep(*phan):
        """Ghep neo LUC CHAY: viet nguyen van thi chinh than ca nay lam chuoi ay
        xuat hien THEM mot lan ngoai bang, va phep doi neo duy nhat se bac het."""
        return "".join(phan)

    NEO = ghep("    if not ", "duong.exists():")
    m.DOT_BIEN_TU_KIEM = [(ten, ("r515",), NEO, "    pass") for ten in kich]
    with contextlib.redirect_stdout(io.StringIO()) as ra, _vang_co_chu_y(m):
        giet, hong, khong_do = m.chay_dot_bien_tu_kiem()
    dong_in = ra.getvalue()

    khoi, hien = {}, None
    for dong in dong_in.split(chr(10)):
        if dong.startswith("DOT BIEN TU KIEM "):
            hien = dong.split()[4]     # BON tu roi moi toi ten
            khoi[hien] = []
        elif hien:
            khoi[hien].append(dong)
    chot(set(khoi) == set(kich), "r530")
    vc, rk = chr(10).join(khoi["vo-can"]), chr(10).join(khoi["rc-khac"])

    # (P1) nhanh DO_KHAC phai CHUYEN TIEP, khong chi neu ten ca.
    chot("VO CAN r511" in vc, "r530")
    chot(MOC_VC in vc, "r530")
    # (P2) nhanh rc != 1 phai in stderr, va KHONG duoc lan sang o kia.
    chot("stderr: " in rk, "r530")
    chot(MOC_SE in rk, "r530")
    chot(MOC_SE not in vc, "r530")
    # r7: DO_KHAC da hoan tat la hong; rc7 thieu bang chung la KHONG DO DUOC.
    chot((giet, hong, khong_do) == (0, 1, 1), "r530")


def r531_ranh_gioi_bo_dong_nao_thi_phai_khai(d: Path):
    r"""#568 r5 / M13 — mat im lang la cam; ba trang thai phai phan biet duoc.

    BON o. Ba o dau la BA TRANG THAI cua viec mat than, o thu tu tach trang thai
    "cat theo tran" ra cho khoi lan:
      (1) KHONG MAT      -> KHONG duoc co nhan nao
      (2) than mang `LOI:` -> PHAI GIU (ranh gioi da hep lai)
      (3) than lo mang tien to THAT -> khoi dong (chong gia mao) VA phai KHAI
      (4) cat theo TRAN  -> nhan `CAT`, KHONG phai `BO QUA`

    Chieu (1) la cho de khai rong nhat: mot trien khai LUON in nhan van thoa moi
    chot cua chieu "co mat thi co nhan". Thieu o (1) thi loi khai "khai dung phan
    bi bo" lai rong hon phep do.
    """
    m = _nap_ban_sao(d)
    L = chr(10)

    # (1) KHONG MAT
    out1 = ("TU KIEM r506: DO_KHAC - RuntimeError: x" + L
            + "TU KIEM r507: DAT" + L + "TU KIEM: 1/2" + L)
    ra1 = m._khoi_chan_doan(out1, "DO_KHAC")
    chot(ra1 == [("r506", "RuntimeError: x")], "r531")
    chot(ra1[0][1].bo_qua == 0, "r531")
    chot("CHA BO" not in m._goi_chan_doan(ra1[0][1]), "r531")

    # (2) than mang `LOI:` — dung ca ma cross-review codex bao cao
    out2 = ("TU KIEM r506: DO_KHAC - AssertionError: first" + L
            + "LOI: root-cause" + L + "more-details" + L + "TU KIEM: 0/1" + L)
    than2 = m._khoi_chan_doan(out2, "DO_KHAC")[0][1]
    chot("root-cause" in than2, "r531")
    chot("more-details" in than2, "r531")
    chot(than2.bo_qua == 0, "r531")
    chot("CHA BO" not in m._goi_chan_doan(than2), "r531")

    # (3) than lo mang tien to THAT: van dong khoi, NHUNG phai khai
    out3 = ("TU KIEM r506: DO_KHAC - RuntimeError: x" + L
            + "TU KIEM r512: DAT" + L + "chi tiet mot" + L + "chi tiet hai" + L
            + "TU KIEM: 1/2" + L)
    than3 = m._khoi_chan_doan(out3, "DO_KHAC")[0][1]
    chot(than3.bo_qua == 2, "r531")
    chot("[CHA BO 2 dong]" in m._goi_chan_doan(than3), "r531")
    chot("chi tiet mot" not in than3, "r531")   # VAN bi bo — nhung DA KHAI

    # (4) cat theo TRAN la trang thai KHAC, phan biet duoc bang nhan
    goi = m._goi_chan_doan("x" * (m.TRAN_CHAN_DOAN + 50))
    chot("[CAT " in goi, "r531")
    chot("CHA BO" not in goi, "r531")


def r532_khai_dung_duong_da_bao_chot_roi_chet_tiep(d: Path):
    r"""#568 r5 / M14 — LOI KHAI phai khop HANH VI, hai chieu.

    `r525` cu chot `MOC not in th`, tuc CAM cha in `stderr` khi da co `DO_CHOT`.
    A8 cua r2 KHONG doi the. Chot ay BAC TRUOC moi trien khai giu ca hai chan
    doan — hinh dang CHOT-CAM-THU-DAC-TA-KHONG-DOI. Da bo.

    Thay bang mot LOI KHAI co ten: `CHAN_DOAN_STDERR_KHI_DA_CO_CHOT`. Ca nay doi
    hanh vi luc chay KHOP voi loi khai, HAI CHIEU:
      doi HANH VI ma khong doi LOI KHAI => DO
      doi LOI KHAI ma khong doi hanh vi => DO
    Ai chua duong nay chi viec dat lai hang so; ca xanh tro lai. Do la khac biet
    giua mot LOI KHAI va mot DIEU CAM.

    r5 KHONG hua chua duong ay — chua no doi dinh dang dau ra ma r516/r524/r530
    dang do. Xin revision rieng.
    """
    m = _nap_ban_sao(d)
    MOC = "MOC-SAU-CHOT-R532"
    kich = {"chot-roi-chet": ("TU KIEM r511: DO_CHOT - chot cua ca r511 that bai"
                              + chr(10), 1, "SystemExit: " + MOC + chr(10))}

    def run_gia(args, cwd, check=True, env=None):
        out, rc, err = kich[Path(cwd).name]
        return subprocess.CompletedProcess(args, rc, out, err)

    m.run = run_gia

    def ghep(*phan):
        """Ghep neo LUC CHAY — xem ghi chu cung ten o r525."""
        return "".join(phan)

    NEO = ghep("    if not ", "duong.exists():")
    m.DOT_BIEN_TU_KIEM = [(ten, ("r515",), NEO, "    pass") for ten in kich]
    with contextlib.redirect_stdout(io.StringIO()) as ra, _vang_co_chu_y(m):
        giet, hong, khong_do = m.chay_dot_bien_tu_kiem()
    dong_in = ra.getvalue()

    chot("CHOT r511" in dong_in, "r532")        # chot CO duoc chuyen tiep
    chot((giet, hong, khong_do) == (0, 0, 1), "r532")        # r7: CHOT roi chet, chua co bang chung hoan tat
    # HAI CHIEU — day la ca chot cua ca nay.
    chot((MOC in dong_in) == m.CHAN_DOAN_STDERR_KHI_DA_CO_CHOT, "r532")


def r533_ranh_gioi_phai_dung_hinh_ban_ghi(d: Path):
    r"""#568 r5 / cross-review P2 tren be5c3f2 — trung TIEN TO khong phai la ranh gioi.

    `DOT BIEN ` la tien to TRAN. Mot dong THAN bat dau bang no dong khoi roi bien
    mat MA KHONG duoc dem: chinh dong ranh gioi khong nam trong `bo_qua`. Nen
    khong nhan `BO QUA`, khong nhan `CAT` — mat IM LANG, dung lop benh #568.

    BON o:
      (1) than `DOT BIEN root-cause` -> PHAI GIU (khong con la ranh gioi)
      (2) than `DOT BIEN root-cause` + dong sau -> GIU CA HAI, KHONG nhan
      (3) ban ghi THAT `DOT BIEN TU KIEM <ten> | ...` -> VAN dong khoi
      (4) HAI CHIEU cua loi khai `DONG_RANH_GIOI_DUNG_HINH_KHONG_DUOC_DEM`

    O (4) la cho khong do duoc: mot dong than trung DUNG HINH ban ghi that van
    dong khoi va van khong duoc dem. Ta KHAI no chu khong lam tron — dem no se
    sinh nhan tren dau vao BINH THUONG, tuc khai RONG hon phep do (A30 cam).
    """
    m = _nap_ban_sao(d)
    L = chr(10)

    # (1) trung tien to, KHONG phai ban ghi -> giu
    out1 = ("TU KIEM r506: DO_KHAC - RuntimeError: first" + L
            + "DOT BIEN root-cause" + L + "TU KIEM: 0/1" + L)
    than1 = m._khoi_chan_doan(out1, "DO_KHAC")[0][1]
    chot("root-cause" in than1, "r533")
    chot(than1.bo_qua == 0, "r533")

    # (2) va dong ke tiep cung phai con
    out2 = ("TU KIEM r506: DO_KHAC - RuntimeError: first" + L
            + "DOT BIEN root-cause" + L + "more-details" + L + "TU KIEM: 0/1" + L)
    than2 = m._khoi_chan_doan(out2, "DO_KHAC")[0][1]
    chot("root-cause" in than2 and "more-details" in than2, "r533")
    chot(than2.bo_qua == 0, "r533")

    # (3) ban ghi THAT van dong khoi — chot chong gia mao KHONG duoc noi long
    out3 = ("TU KIEM r506: DO_KHAC - x" + L
            + "DOT BIEN TU KIEM abc | r1 | 1/1" + L + "chi tiet" + L
            + "TU KIEM: 0/1" + L)
    than3 = m._khoi_chan_doan(out3, "DO_KHAC")[0][1]
    chot("chi tiet" not in than3, "r533")
    chot(than3.bo_qua == 1, "r533")
    chot("[CHA BO 1 dong]" in m._goi_chan_doan(than3), "r533")

    # (4) HAI CHIEU: dong ranh gioi DUNG HINH khong duoc dem — day la LOI KHAI.
    # Dau vao co DUNG mot dong bi bo, va do la chinh dong ranh gioi.
    out4 = ("TU KIEM r506: DO_KHAC - x" + L + "TU KIEM r512: DAT" + L
            + "TU KIEM: 1/2" + L)
    than4 = m._khoi_chan_doan(out4, "DO_KHAC")[0][1]
    chot((than4.bo_qua == 0) == m.DONG_RANH_GIOI_DUNG_HINH_KHONG_DUOC_DEM, "r533")


def r534_nhan_bo_dong_phai_song_qua_tran(d: Path):
    r"""#568 r5 / cross-review P2 tren be5c3f2 — tran KHONG duoc nuot chinh loi khai.

    `…[BO QUA n dong]` la sieu du lieu ve phep do. Ban truoc noi no vao cuoi
    than roi `_goi_chan_doan` cat TU DAU, nen than dai lam nhan bi cat: cha in ra
    so ky tu bi cat ma MAT HAN so dong bi bo. A29 khai mot thu khong den duoc
    nguoi doc log.

    BA o, phan biet duoc bang dau vao:
      (1) than DAI + co dong bi bo -> PHAI co CA HAI so
      (2) than NGAN + co dong bi bo -> co BO QUA, KHONG co CAT
      (3) than DAI + KHONG dong bi bo -> co CAT, KHONG co BO QUA
    """
    m = _nap_ban_sao(d)
    L = chr(10)
    dai = "x" * (m.TRAN_CHAN_DOAN + 50)

    # (1) ca hai so
    out1 = ("TU KIEM r506: DO_KHAC - " + dai + L + "TU KIEM r512: DAT" + L
            + "a" + L + "b" + L + "TU KIEM: 0/1" + L)
    goi1 = m._goi_chan_doan(m._khoi_chan_doan(out1, "DO_KHAC")[0][1])
    chot("[CHA BO 2 dong]" in goi1, "r534")
    chot("[CAT " in goi1, "r534")

    # (2) chi BO QUA
    out2 = ("TU KIEM r506: DO_KHAC - ngan" + L + "TU KIEM r512: DAT" + L
            + "a" + L + "b" + L + "TU KIEM: 0/1" + L)
    goi2 = m._goi_chan_doan(m._khoi_chan_doan(out2, "DO_KHAC")[0][1])
    chot("[CHA BO 2 dong]" in goi2, "r534")
    chot("[CAT " not in goi2, "r534")

    # (3) chi CAT
    goi3 = m._goi_chan_doan(dai)
    chot("[CAT " in goi3, "r534")
    chot("CHA BO" not in goi3, "r534")


def r535_moi_ho_tien_to_deu_phai_dung_hinh(d: Path):
    r"""#568 r5 / cross-review luot 2 tren 15c487c — siet MOT ho la chua du.

    Luot 1 chi siet `DOT BIEN `. Ba ho con lai (`TU KIEM r<n>: `, `MUTANT: `,
    `CASE T<n>: `) VAN la tien to TRAN, nen van nuot chan doan IM LANG:

        "TU KIEM r506: DO_KHAC - RuntimeError: first" + LF + "MUTANT: root-cause"
          -> [('r506', 'RuntimeError: first')]   · khong nhan nao

    Ca nay do CA BON ho bang mot bang, moi ho HAI ve — phan biet duoc bang dau vao:
      · mot dong THAN chi TRUNG TIEN TO  -> PHAI GIU, khong nhan
      · mot BAN GHI THAT cung ho         -> PHAI dong khoi va PHAI khai
    Thieu ve thu hai thi mot `ranh` rong (`^(?!)`) cung qua duoc ve thu nhat.
    """
    m = _nap_ban_sao(d)
    L = chr(10)
    # (gia mao, ban ghi THAT) cho tung ho
    ho = [
        ("TU KIEM r512: root-cause",        "TU KIEM r512: DAT"),
        ("MUTANT: root-cause",              "MUTANT: giet = 1 · khong giet = 0 · khong do duoc = 0 / tong 1"),
        ("CASE T6: root-cause",             "CASE T6: DO — gia mao"),   # hinh cua `chay_ca`
        ("DOT BIEN root-cause",             "DOT BIEN TU KIEM abc | r1 | 1/1"),
    ]
    for gia, that in ho:
        # ve 1 — chi trung TIEN TO: phai GIU nguyen, khong sinh nhan
        o1 = ("TU KIEM r506: DO_KHAC - dau" + L + gia + L + "TU KIEM: 0/1" + L)
        t1 = m._khoi_chan_doan(o1, "DO_KHAC")[0][1]
        chot(gia in t1, "r535")
        chot(t1.bo_qua == 0, "r535")
        # ve 2 — BAN GHI THAT: phai dong khoi, va phan sau phai duoc KHAI
        o2 = ("TU KIEM r506: DO_KHAC - dau" + L + that + L + "chi tiet" + L
              + "TU KIEM: 0/1" + L)
        t2 = m._khoi_chan_doan(o2, "DO_KHAC")[0][1]
        chot("chi tiet" not in t2, "r535")
        chot(t2.bo_qua == 1, "r535")


def r536_con_khong_duoc_doat_so_do_cua_cha(d: Path):
    r"""#568 r5 / cross-review luot 2 tren 15c487c — dao ly 6, o lop sieu du lieu.

    Ban va DAU TIEN cua P2-2 giu nhan `…[BO QUA n dong]` ngoai tran bang cach
    DOC NGUOC con so ra tu van ban than. Khi ay mot chuoi do mã DANG BI THU phat
    ra tro thanh bang chung phep do cua cha. Do duoc tren 15c487c:

        than = "x"*450 + LF + "…[BO QUA 7 dong]"     # cha KHONG bo dong nao
        -> "x"*400 + " …[CAT 50 ky tu] …[BO QUA 7 dong]"

    Cha khai bo bay dong trong khi no bo KHONG dong nao. Ca nay chot HAI ve:
      (1) con in nhan GIA          -> cha KHONG duoc nhan no lam so cua minh
      (2) cha THAT SU bo n dong    -> cha PHAI khai dung n
    Chi co ve (1) thi mot trien khai KHONG BAO GIO khai gi cung xanh.
    """
    m = _nap_ban_sao(d)
    L = chr(10)
    NHAN_GIA = "…[BO QUA 7 dong]"

    # (1) con gia mao: cha khong bo dong nao, nen KHONG duoc khai so nao
    o1 = ("TU KIEM r506: DO_KHAC - " + "x" * 450 + L + NHAN_GIA + L
          + "TU KIEM: 0/1" + L)
    t1 = m._khoi_chan_doan(o1, "DO_KHAC")[0][1]
    chot(t1.bo_qua == 0, "r536")
    goi1 = m._goi_chan_doan(t1)
    chot("CHA BO" not in goi1, "r536")
    chot("[CAT " in goi1, "r536")          # van phai khai phan bi CAT

    # (1b) nhan gia o mot than NGAN: van khong duoc thanh so do cua cha
    o1b = ("TU KIEM r506: DO_KHAC - dau" + L + NHAN_GIA + L + "TU KIEM: 0/1" + L)
    t1b = m._khoi_chan_doan(o1b, "DO_KHAC")[0][1]
    chot(t1b.bo_qua == 0, "r536")
    chot("CHA BO" not in m._goi_chan_doan(t1b), "r536")
    # van ban con PHAI con NGUYEN: cach lam ro khong duoc la SUA than con
    chot(NHAN_GIA in m._goi_chan_doan(t1b), "r536")

    # (2) chieu nguoc: cha THAT SU bo hai dong thi PHAI khai dung hai
    o2 = ("TU KIEM r506: DO_KHAC - " + "x" * 450 + L + "TU KIEM r512: DAT" + L
          + "a" + L + "b" + L + "TU KIEM: 0/1" + L)
    t2 = m._khoi_chan_doan(o2, "DO_KHAC")[0][1]
    chot(t2.bo_qua == 2, "r536")
    goi2 = m._goi_chan_doan(t2)
    chot("[CHA BO 2 dong]" in goi2, "r536")
    chot("[CAT " in goi2, "r536")

    # (3) `_goi_chan_doan` tren mot `str` THUONG (vd stderr) khong duoc sinh nhan
    chot("CHA BO" not in m._goi_chan_doan("stderr binh thuong " + NHAN_GIA), "r536")


def r537_chuan_hoa_than_khong_duoc_sua_noi_dung(d: Path):
    r"""#568 r5 / cross-review luot 3 tren 7d0b012 — go dau phan cach, khong `lstrip`.

    Ban truoc dung `lstrip(" —-")` — mot TAP KY TU, nen no an het dau cach va
    dau gach o dau than KE CA khi chung la NOI DUNG. Do duoc truoc khi va:

        "TU KIEM r1: DO_CHOT — -42"            -> than "42"       (mat dau AM)
        "TU KIEM r1: DO_CHOT — --gio-cao-nhat" -> than "gio-cao-nhat"

    Mot con so doi dau la SUA NOI DUNG chan doan. BON o:
      (1) dau phan cach ` — ` bi go, than con NGUYEN (ke ca dau am)
      (2) dau phan cach ` - ` (dang cac ca dung) cung duoc go, va CHI MOT
      (3) than khong co dau phan cach thi KHONG bi cat xen
      (4) HAI CHIEU cua `THAN_BO_DONG_TRANG_KHONG_DEM`
      (5) HAI CHIEU cua `THAN_BO_KHOANG_TRANG_TUNG_DONG`, chuoi mong doi suy tu
          loi khai — khong khoa cung hanh vi hien tai (luot 5)
    """
    m = _nap_ban_sao(d)
    L = chr(10)

    # (1) dau AM phai con
    t1 = m._khoi_chan_doan("TU KIEM r1: DO_CHOT — -42" + L + "TU KIEM: 0/1", "DO_CHOT")[0][1]
    chot(str(t1) == "-42", "r537")
    t1b = m._khoi_chan_doan("TU KIEM r1: DO_CHOT — --gio-cao-nhat" + L + "TU KIEM: 0/1",
                            "DO_CHOT")[0][1]
    chot(str(t1b) == "--gio-cao-nhat", "r537")

    # (2) dang ` - ` cung duoc go, va CHI MOT dau
    t2 = m._khoi_chan_doan("TU KIEM r1: DO_KHAC - -7" + L + "TU KIEM: 0/1", "DO_KHAC")[0][1]
    chot(str(t2) == "-7", "r537")

    # (3) khong co dau phan cach thi khong duoc cat xen ky tu nao
    t3 = m._khoi_chan_doan("TU KIEM r1: DO_KHAC:x" + L + "TU KIEM: 0/1", "DO_KHAC")[0][1]
    chot(str(t3) == ":x", "r537")

    # (4) HAI CHIEU, VE MOT: dong TRANG trong than bi loai va KHONG dem
    t4 = m._khoi_chan_doan("TU KIEM r1: DO_KHAC - a" + L + "" + L + "b" + L + "TU KIEM: 0/1",
                           "DO_KHAC")[0][1]
    bi_bo = ("" not in str(t4).split(L)) and t4.bo_qua == 0
    chot(bi_bo == m.THAN_BO_DONG_TRANG_KHONG_DEM, "r537")

    # (5) HAI CHIEU, VE HAI: khoang trang TUNG DONG. Ban truoc gop ve nay vao
    # cung mot hang voi ve (4), va no SAI — ma van xanh nho ve (4) dung. Do la
    # ly do hai loi khai phai la hai hang, moi hang mot chot.
    t5 = m._khoi_chan_doan("TU KIEM r1: DO_KHAC -  a  " + L + "  b  " + L + "TU KIEM: 0/1",
                           "DO_KHAC")[0][1]
    goi5 = m._goi_chan_doan(t5)
    bo_tung_dong = "a | b" in goi5
    chot(bo_tung_dong == m.THAN_BO_KHOANG_TRANG_TUNG_DONG, "r537")
    # va khai CHINH XAC cai no LAM — chuoi mong doi SUY TU loi khai. Luot 5 do
    # duoc: `goi5 == "a   |   b"` khoa cung hanh vi hien tai, nen mot trien khai
    # doi CA hanh vi LAN loi khai (hop le theo A29-A36) van bi bac — dung hinh
    # CHOT-CAM-THU-DAC-TA-KHONG-DOI ma M14 go o r525.
    chot(goi5 == ("a | b" if m.THAN_BO_KHOANG_TRANG_TUNG_DONG else "a   |   b"), "r537")


def r538_bien_phai_cua_nhan_phai_co(d: Path):
    r"""#568 r5 / cross-review luot 3 tren 7d0b012 — `DO_CHOT` thieu bien PHAI.

    `ranh` cu bat `TU KIEM r\d+: DO_CHOT` KHONG co bien phai, nen mot dong THAN
    la `TU KIEM r512: DO_CHOT_fake-root` cung dong khoi va bien mat IM LANG. Do
    duoc truoc khi va: than chi con 'first', `bo_qua == 0`.

    Luot 6 (tren 273de20): nam duoi van la tien to, ho TU KIEM rong hon hinh
    that, va loi khai "ranh rong bang dau" bi phan chung — nay khai thanh
    `DAU_RONG_HON_RANH_THEO_HOP_DONG_TEN_CA` va do hai chieu o cuoi ca.

    Luot 5 (tren 31127d7): NGU PHAP phai bang TAP HINH cua MOI diem phat that,
    doi chieu tung `print` cot 0 — ba cho lech va bon ho chua ke, xem chu thich
    tren dong `ranh`. Danh sach `that` duoi day la bang doi chieu ay.

    Cung the voi ba ho kia: ban ghi THAT cua chung con dai hon hinh ma luot 2 da
    siet (`MUTANT: giet = <so> `, `CASE T<n>: DO - `,
    `DOT BIEN TU KIEM <ten>: NEO KHONG DUY NHAT `), nen mot dong than chi trung
    phan DAU van lot qua. Ca nay do CA BON, moi ho mot ve GIA.
    """
    m = _nap_ban_sao(d)
    L = chr(10)
    gia = [
        "TU KIEM r512: DO_CHOT_fake-root",
        "MUTANT: giet = root-cause",
        "CASE T6: DO root-cause",
        "DOT BIEN TU KIEM abc: root-cause",
        # luot 4 — TIEN TO DAI HON van khong phai BAN GHI. Co chu so sau
        # `giet = ` chua thanh ban tong ket; co MOT dau `|` chua thanh dong
        # ket qua; co `NEO KHONG DUY NHAT ` chua thanh ban ghi neo.
        "MUTANT: giet = 1 root-cause",
        "DOT BIEN TU KIEM abc | root-cause",
        "DOT BIEN TU KIEM abc: NEO KHONG DUY NHAT root-cause",
        # luot 5 — HAI dau `|` van chua thanh ban ghi; cach truoc dau hai cham
        # la hinh khong ai phat; `DO - ` la hinh cua fixture, khong phai runner.
        "DOT BIEN TU KIEM abc | r1 | root-cause",
        "DOT BIEN TU KIEM : KHONG DO DUOC — phep cat bang hong",
        "CASE T6: DO - gia mao",
        "MUTANT abc | T1 | root-cause",
        "TU KIEM co dot bien rieng: root-cause",
        "LOI: root-cause",
        "8/8x",
        # luot 6 — nam duoi con la tien to, va ho TU KIEM rong hon hinh that
        "DOT BIEN TU KIEM abc | r1 | TIN DUNG GIA: root-cause",
        "DOT BIEN TU KIEM abc | r1 | 0 — ca do THUC TE: root-cause",
        "MUTANT abc | T1 | KHONG DO DUOC (sau 2 lan): ",
        "MUTANT abc | T1 | 0/1: ",
        "LOI: nhom bat buoc THIEU (chua chay hoac chua co dot bien): root-cause",
        "TU KIEM r512: DO_CHOT root-cause",
        # luot 7 — bon nhom L/D/S/K (phan chung cua reviewer, moi dong mot mien)
        "MUTANT abc | T1 | 0/1: root-cause",
        "MUTANT abc | T1 | KHONG DO DUOC (sau 2 lan): root-cause",
        "MUTANT abc | T1 | KHONG DO DUOC (sau 3 lan): kenh khong ton tai | rc_con=1 | stderr[-200:]=''",
        "DOT BIEN TU KIEM abc | root-cause | 1/1",
        "MUTANT abc | root-cause | 1/1",
        "TU KIEM: ٠/١",
        "MUTANT: giet = 01 · khong giet = 0 · khong do duoc = 0 / tong 1",
        "DOT BIEN TU KIEM abc | r1 | TIN DUNG GIA: child rc=-0 != 1",
        "DOT BIEN TU KIEM abc | r1 | TIN DUNG GIA: child rc=1 != 1",
        "DOT BIEN TU KIEM abc | r1 | 1/2",
        "DOT BIEN TU KIEM abc: NEO KHONG DUY NHAT (1)",
        "MUTANT abc | T1 | 0/0: tap ca do chot [] != dich []",
    ]
    for dong in gia:
        t = m._khoi_chan_doan(
            "TU KIEM r506: DO_KHAC - first" + L + dong + L + "TU KIEM: 0/1" + L, "DO_KHAC")[0][1]
        chot(dong in str(t), "r538")
        chot(t.bo_qua == 0, "r538")
    # chieu nguoc — BAN GHI THAT cua ca bon ho VAN phai dong khoi
    # luot 5 — MOI diem phat cot 0 cua ma chay, moi hinh mot dong (so dong la
    # cua 31127d7). Them mot `print` cot 0 ma khong them vao day la lech.
    that = [
        "TU KIEM r512: DAT",                                          # :4039
        "TU KIEM r512: DO_CHOT — chot",                               # :4047
        "TU KIEM: 38/38",                                             # :4051
        "TU KIEM co dot bien rieng: 38/38 nhom bat buoc · dot bien giet 114/114",  # :4080
        "MUTANT: giet = 1 · khong giet = 0 · khong do duoc = 0 / tong 1",           # :4083
        "MUTANT abc | T1 | 1/1",                                      # :564
        "MUTANT abc | T1 | KHONG DO DUOC (sau 2 lan): kenh khong ton tai | rc_con=1 | stderr[-200:]=''",  # :567
        "MUTANT abc | T1 | KHONG DO DUOC (sau 1 lan): khong phong duoc tien trinh con: OSError: [Errno 24] x",
        "MUTANT abc | T1 | 0/1: tap ca do chot ['T2'] != dich ['T1']",  # :570
        "MUTANT in-ca-C | T1,T3 | 2/2",                                # ten muc co chu hoa
        "DOT BIEN TU KIEM abc: NEO KHONG DUY NHAT (2)",
        "DOT BIEN TU KIEM abc | r1 | TIN DUNG GIA: child rc=-15 != 1",
        "CASE T6: DAT",                                               # :493
        "CASE T6: DO — chot cua ca T6 that bai",                      # :498
        "CASE T6: DO — RuntimeError: x",                              # :505
        "DOT BIEN TU KIEM: KHONG DO DUOC — phep cat bang hong",       # :3961
        "DOT BIEN TU KIEM abc: NEO KHONG DUY NHAT (0)",               # :3967
        "DOT BIEN TU KIEM abc | r1 | TIN DUNG GIA: ca chet vi loi VO CAN ['r5']",  # :3992
        "DOT BIEN TU KIEM abc | r1 | 1/1",                            # :4005
        "DOT BIEN TU KIEM abc |  | 0/0",                              # dich rong
        "DOT BIEN TU KIEM abc | r1 | 0 — ca do THUC TE: r2",          # :4008
        "8/8",                                                        # :4069 :4072 :4082
        "LOI: ba so hang khong cong dung tong",                       # :4088
        "LOI: nhom bat buoc THIEU (chua chay hoac chua co dot bien): ['r1']",  # :4096
        # luot 6 — hinh that cua cac duoi da siet
        "DOT BIEN TU KIEM abc | r1 | TIN DUNG GIA: child rc=2 != 1",  # :3998
        "DOT BIEN TU KIEM abc | r1 | 0 — ca do THUC TE: (rong)",      # :4008 do_chot rong
        "DOT BIEN TU KIEM abc | r1 | 0 — ca do THUC TE: r1,r2",
    ]
    for dong in that:
        t = m._khoi_chan_doan(
            "TU KIEM r506: DO_KHAC - first" + L + dong + L + "chi tiet" + L
            + "TU KIEM: 0/1" + L, "DO_KHAC")[0][1]
        chot("chi tiet" not in str(t), "r538")
        chot(t.bo_qua == 1, "r538")
    # luot 6 — BAT DOI XUNG dau/ranh, do HAI CHIEU theo loi khai co ten: cung mot
    # dong `TU KIEM r512: DO_CHOT_fake-root` la BAN GHI khi doc DO_CHOT (hop dong
    # lay ten ca) va la THAN khi doc DO_KHAC (khong phai hinh that).
    o = "TU KIEM r506: DO_KHAC - first" + L + "TU KIEM r512: DO_CHOT_fake-root" + L + "TU KIEM: 0/1" + L
    la_ban_ghi = [ca for ca, _ in m._khoi_chan_doan(o, "DO_CHOT")] == ["r512"]
    t = m._khoi_chan_doan(o, "DO_KHAC")[0][1]
    la_than = "DO_CHOT_fake-root" in str(t) and t.bo_qua == 0
    chot((la_ban_ghi and la_than) == m.DAU_RONG_HON_RANH_THEO_HOP_DONG_TEN_CA, "r538")
    # luot 6 — ho DO_KHAC phai do khi doc nhan DO_CHOT: doc DO_KHAC thi dong ay la
    # DAU ban ghi (mo khoi moi), khong phai ranh gioi. Hinh that `DO_KHAC — <Kieu>: `
    # dong khoi va khai; hinh thieu `DO_KHAC — root-cause` (khong co `<Kieu>: `) GIU.
    o = "TU KIEM r1: DO_CHOT — first" + L + "TU KIEM r512: DO_KHAC — RuntimeError: x" + L + "chi tiet" + L + "TU KIEM: 0/1" + L
    t = m._khoi_chan_doan(o, "DO_CHOT")[0][1]
    chot("chi tiet" not in str(t) and t.bo_qua == 1, "r538")
    o = "TU KIEM r1: DO_CHOT — first" + L + "TU KIEM r512: DO_KHAC — root-cause" + L + "TU KIEM: 0/1" + L
    t = m._khoi_chan_doan(o, "DO_CHOT")[0][1]
    chot("DO_KHAC — root-cause" in str(t) and t.bo_qua == 0, "r538")
    # luot 7 — ten ngoai le la BAT KY chuoi nao: dung `type()` tao that, doc DO_CHOT
    for ten_kieu in ("Échec", "Bad-Error", ""):
        try:
            raise type(ten_kieu, (Exception,), {})("root-cause")
        except Exception as exc:
            dong_that = f"TU KIEM r512: DO_KHAC — {type(exc).__name__}: {exc}"
        t = m._khoi_chan_doan("TU KIEM r1: DO_CHOT — first" + L + dong_that + L + "chi tiet" + L
                              + "TU KIEM: 0/2" + L, "DO_CHOT")[0][1]
        chot("chi tiet" not in str(t) and t.bo_qua == 1, "r538")
    # luot 7 — `ly_do` trong `ranh` phai la NGUYEN VAN ngu phap sinh tu AST cua nguon:
    # doi mot cau `return KHONG_DO_DUOC, "..."` ma quen `ranh` la lech, va do duoc.
    src = Path(m.__file__).read_text(encoding="utf-8")
    dong_ranh = re.search(r'^    ranh = re\.compile\(r"(.*)"\)$', src, re.M).group(1)
    chot(m._ngu_phap_ly_do(src) in dong_ranh, "r538")



def r539_bang_chung_phai_den_tu_con_chay_that(d: Path):
    """A37-A39: real subprocesses, no mocked run and no full nested suite."""
    m = _nap_ban_sao(d)
    # One real case keeps this protocol-boundary test cheap; parent expects it.
    m.TU_KIEM = [("r515", None, False)]
    entry = 'if __name__' + ' == "__main__":'
    real = ('def ca_that():\n    chot(False, "r515")\n'
            'TU_KIEM = [("r515", ca_that, False)]\n')
    fake = 'TU KIEM r515: DO_CHOT - fabricated\nTU KIEM: 0/1\n'
    forged = json.dumps({"nonce": "literal-not-parent", "cases": ["r515"]})
    # Each named entry differs by process termination or completion semantics.
    matrix = [
        ("system-exit", f"print({fake!r}, flush=True)\nraise SystemExit(1)\n"),
        ("zero-division", f"print({fake!r}, flush=True)\n1 / 0\n"),
        ("os-exit", f"print({fake!r}, flush=True)\nos._exit(1)\n"),
        ("literal-proof", f"Path(os.environ[TU_KIEM_FILE_ENV]).write_text({forged!r}, encoding='utf-8')\nprint({fake!r}, flush=True)\nraise SystemExit(1)\n"),
        ("invalid-utf8", "Path(os.environ[TU_KIEM_FILE_ENV]).write_bytes(bytes([255]))\nraise SystemExit(1)\n"),
        ("deep-proof", "Path(os.environ[TU_KIEM_FILE_ENV]).write_text('[' * 100000, encoding='utf-8')\nraise SystemExit(1)\n"),
        ("oversized-numerator", "Path(os.environ[TU_KIEM_FILE_ENV]).write_text(json.dumps({'nonce': os.environ[TU_KIEM_NONCE_ENV], 'cases': ['r515']}), encoding='utf-8')\nprint('TU KIEM: ' + '9' * 5000 + '/1')\nraise SystemExit(1)\n"),
        ("oversized-denominator", "Path(os.environ[TU_KIEM_FILE_ENV]).write_text(json.dumps({'nonce': os.environ[TU_KIEM_NONCE_ENV], 'cases': ['r515']}), encoding='utf-8')\nprint('TU KIEM: 0/' + '9' * 5000)\nraise SystemExit(1)\n"),
        ("real-case", real),
        ("nested-before-exit", 'def inner():\n    chot(False, "r515")\ndef outer():\n    global TU_KIEM\n    TU_KIEM = [("r515", inner, False)]\n    chay_tu_kiem()\n    raise SystemExit(1)\nTU_KIEM = [("r515", outer, False)]\n'),
        ("no-case", 'TU_KIEM = []\n'),
    ]
    m.DOT_BIEN_TU_KIEM = [(name, ("r515",), entry, code + entry) for name, code in matrix]
    with contextlib.redirect_stdout(io.StringIO()) as out, _vang_co_chu_y(m):
        try:
            result = m.chay_dot_bien_tu_kiem()
        except (ValueError, RecursionError):
            chot(False, "r539")
    text = out.getvalue()
    chot(result == (1, 0, 10), "r539")
    chot("real-case | r515 | 1/1" in text, "r539")
    for name, _ in matrix:
        if name != "real-case":
            chot(f"KHONG DO DUOC: {name}" in text, "r539")
            chot(f"{name} | r515 | 1/1" not in text, "r539")

    # Completion-destroying mutations cannot earn credit: their own proof is
    # necessarily incomplete. Keep the exact mutation as a required negative
    # protocol control, outside the table whose entries must all earn GIET.
    fixture = Path(m.__file__)
    fixture.write_text(fixture.read_text(encoding="utf-8").replace(entry, real + entry),
                       encoding="utf-8", newline="\n")
    m.DOT_BIEN_TU_KIEM = [("tk-drop-completion", ("r515",),
                          "            completed." + "append(ten)", "            pass")]
    with contextlib.redirect_stdout(io.StringIO()) as out, _vang_co_chu_y(m):
        missing = m.chay_dot_bien_tu_kiem()
    chot(missing == (0, 0, 1), "r539")
    chot("ca do THUC TE: r515" in out.getvalue(), "r539")
    chot("KHONG DO DUOC: tk-drop-completion" in out.getvalue(), "r539")


def r540_so_hang_va_bang_chung_phai_nhat_quan(d: Path):
    """A40 plus malformed channel data: every bad field stays unmeasurable."""
    m = _nap_ban_sao(d)
    token = secrets.token_hex(32)
    expected = ["r515", "r514"]
    proof = {"nonce": token, "cases": expected}
    good = json.dumps(proof)
    failed = [("r515", "failure")]
    cases = [
        (good, "TU KIEM: 1/2\n", failed, True),
        (None, "TU KIEM: 1/2\n", failed, False),
        (good + good, "TU KIEM: 1/2\n", failed, False),
        ("{", "TU KIEM: 1/2\n", failed, False),
        ("[" * 2000, "TU KIEM: 1/2\n", failed, False),
        ("[]", "TU KIEM: 1/2\n", failed, False),
        (json.dumps(dict(proof, nonce="wrong")), "TU KIEM: 1/2\n", failed, False),
        (json.dumps(dict(proof, cases=["r515"])), "TU KIEM: 1/2\n", failed, False),
        (good, "", failed, False),
        (good, "TU KIEM: 1/2\nTU KIEM: 1/2\n", failed, False),
        (good, "TU KIEM: 2/3\n", failed, False),
        (good, "TU KIEM: 3/2\n", failed, False),
        (good, "TU KIEM: " + "9" * 5000 + "/2\n", failed, False),
        (good, "TU KIEM: 0/2\n", failed, False),
        (good, "TU KIEM: 0/2\n", failed * 2, False),
        (good, "TU KIEM: 1/2\n", [("r999", "unknown")], False),
    ]
    for raw, text, chot_cases, want in cases:
        try:
            got = m._bang_chung_tu_kiem(text, raw, token, expected, chot_cases, [])
        except (ValueError, TypeError, RecursionError):
            chot(False, "r540")  # pure parser must return a state, not escape
        chot(got == want, "r540")


def r541_khong_do_duoc_khong_duoc_lam_xanh_main(d: Path):
    m = _nap_ban_sao(d)
    m.chay_ca = lambda khung=None: []
    m.chay_dot_bien = lambda: (len(m.DOT_BIEN), 0, 0)
    m.chay_tu_kiem = lambda: []
    m.chay_dot_bien_tu_kiem = lambda: (len(m.DOT_BIEN_TU_KIEM), 0, 1)
    with _moi_truong(**{KENH_ENV: None, "NHANH_DON_DUOC_CHI_TU_KIEM": None,
                        "NHANH_DON_DUOC_KHONG_DOT_BIEN": None}):
        with contextlib.redirect_stdout(io.StringIO()):
            rc = m.main()
    chot(rc == 1, "r541")



def r542_kenh_hoan_tat_khong_duoc_xoa_chan_doan(d: Path):
    """Real completed cases retain control-looking text in both error classes."""
    m = _nap_ban_sao(d)
    m.TU_KIEM = [("r515", None, False)]
    entry = 'if __name__' + ' == "__main__":'
    body = "first\nTU KIEM XONG: ROOT-CAUSE-MUST-SURVIVE"
    matrix = []
    for name, error in [("chot", "TinHieuChotCa"), ("vo-can", "RuntimeError")]:
        code = (f"def ca_that():\n    raise {error}({body!r})\n"
                'TU_KIEM = [("r515", ca_that, False)]\n')
        matrix.append((name, ("r999",), entry, code + entry))
    m.DOT_BIEN_TU_KIEM = matrix
    with contextlib.redirect_stdout(io.StringIO()) as out:
        result = m.chay_dot_bien_tu_kiem()
    text = out.getvalue()
    chot(result == (0, 2, 0), "r542")
    chot(text.count("TU KIEM XONG: ROOT-CAUSE-MUST-SURVIVE") == 2, "r542")


def r543_tien_de_ha_tang_cua_r528_phai_ra_trang_thai_thu_ba(d: Path):
    """#593 r1 / A1-A4 — vong (c2) cua `r528` phai tach BA nguon do; do tren CHINH ham no goi.

    Tai lap tren 18d42ca (do ga: `_kenh_tam` nem `OSError(28)`): 2000 loi ha tang
    bi `except BaseException` nuot thanh `chot cua ca r528 that bai`, 'dia day'
    mat. Doi chung duong cung do ga: r528 DAT trong 2,0 s.

    Bon chieu, moi chieu mot DAU VAO rieng — thieu chieu nao thi mot trien khai
    "luon KHONG DO DUOC" (thieu A2) hay "moi thu deu la chot" (thieu A1/A4) van xanh:
      A2  khong tiem gi              -> 0 lan do, khong ngoai le
      A1  OSError(28) o `_kenh_tam`  -> KHONG DO DUOC mang LOAI + THONG DIEP + SO LAN
          = N, KHONG phai DO_CHOT; hai loai XEN KE -> ke RIENG tung loai, moi loai N/2
      A3  chot cua r508 that bai     -> dem = N, khong ngoai le
      A4  NameError trong r508       -> THOAT RA nguyen ven, khong thanh con so
    N nho: ca nay do PHAN LOAI chu khong do xac suat, va so lan khai phai BANG N.
    """
    m = _nap_ban_sao(d)
    # #661 M7: khong gian 256 nhu r528 nhung KHONG lap LIEN TIEP (lap => chet LAY 10/300 duoi `dau-phien-bo-vong-rut-lai`).
    truoc = {"v": None}

    def hep():
        while (v := secrets.token_hex(1) * 16) == truoc["v"]:
            pass
        truoc["v"] = v
        return v
    m.sinh_dau_phien = hep
    N = 8
    goc = {"_kenh_tam": m._kenh_tam, "doc_kenh": m.doc_kenh}

    def chay(ten, **thay):
        """Goi ham THAT cua ban sao. Ba duong ra duoc ky vong tra ve co nhan; moi
        duong ra KHAC la chot cua CHINH ca nay do — nep r517/r520, khong de mot
        ngoai le la thoat ra thanh DO_KHAC roi bi xep la TIN DUNG GIA.
        r2 M2: moi loi ca nay TIEM deu dang ky bang `_tiem`; loi THAT (vd `mkdir`
        that hong o BAT KY nhanh nao) van vao so, va runner doi nhan ca nay."""
        for k, v in {**goc, **thay}.items():
            setattr(m, k, v)
        try:
            return "tra", m._chay_r508_tach_nguon_do(m, d / ten, N)
        except m.TinHieuKhongDoDuoc as e:
            return "kdd", str(e)
        except NameError as e:
            return "lap-trinh", str(e)
        except Exception as exc:                  # noqa: BLE001
            raise TinHieuChotCa(f"chot cua ca r543 that bai: duong ra la {type(exc).__name__}: {exc}")
        finally:
            _bo_cua(cua)                         # lop hai trong FINALLY (nhu r520)

    cua = []                             # lop hai: doi tuong CA NAY tao

    def tiem(e):
        cua.append(e)
        return _tiem(e)

    def nem(tao):
        def hong(*a, **k):
            raise tiem(tao())
        return hong

    # A2 — doi chung duong: khong tiem gi thi r508 THAT chay tron N lan.
    chot(chay("sach") == ("tra", 0), "r543")
    # A1 — dia day o tien de: KHONG DO DUOC mang loai + thong diep + so lan; KHONG DO_CHOT.
    tt, ly = chay("day", _kenh_tam=nem(lambda: OSError(28, "No space left on device")))
    chot(tt == "kdd", "r543")
    chot(f"OSError: [Errno 28] No space left on device ({N} lan)" in ly, "r543")
    chot(f"trong {N} luot" in ly, "r543")
    # A1b — hai loai xen ke: moi loai duoc ke RIENG voi so lan cua no.
    dem = {"i": 0}

    def xen_ke(*a, **k):
        dem["i"] += 1
        raise tiem(PermissionError(13, "Permission denied") if dem["i"] % 2
                    else FileNotFoundError(2, "No such file"))
    tt, ly = chay("xen-ke", _kenh_tam=xen_ke)
    chot(tt == "kdd", "r543")
    chot(f"PermissionError: [Errno 13] Permission denied ({N // 2} lan)" in ly, "r543")
    chot(f"FileNotFoundError: [Errno 2] No such file ({N // 2} lan)" in ly, "r543")
    # A3 — chot cua ca long that bai: dem vao `do`, KHONG ngoai le.
    chot(chay("chot", doc_kenh=lambda *a, **k: (m.GIET, "")) == ("tra", N), "r543")
    # A4 — loi lap trinh: thoat ra nguyen ven, khong thanh con so.
    tt, ly = chay("lap-trinh", _kenh_tam=nem(lambda: NameError("ten_khong_ton_tai")))
    chot(tt == "lap-trinh" and "ten_khong_ton_tai" in ly, "r543")
    # ---- DIEM PHAT SINH x LOAI (cross-review v2 F2): helper phai bat CA HO OSError ----
    # B1 — `mkdir` hong (PermissionError that tu `Path.mkdir`), khong chi `_kenh_tam`.
    goc_mkdir = Path.mkdir

    def mkdir_hong(self, *a, **k):
        if self.parent == d / "mkdir":
            raise tiem(PermissionError(13, "mkdir hong"))
        return goc_mkdir(self, *a, **k)
    Path.mkdir = mkdir_hong
    try:
        tt, ly = chay("mkdir")
    finally:
        Path.mkdir = goc_mkdir
    chot(tt == "kdd" and f"PermissionError: [Errno 13] mkdir hong ({N} lan)" in ly, "r543")
    # B2 — con chau OSError NGOAI ba loai da thu: ca HO, khong phai danh sach.
    tt, ly = chay("con-chau", _kenh_tam=nem(lambda: BlockingIOError(11, "tam het")))
    chot(tt == "kdd" and f"BlockingIOError: [Errno 11] tam het ({N} lan)" in ly, "r543")

    # B4 — loi doc AN trong `doc_kenh` (ly do khac `khong neo dung luot`): KHONG lam tron len DAT.
    chot(chay("doc-an", doc_kenh=lambda *a, **k: (m.KHONG_DO_DUOC, "khong doc duoc kenh: X"))
         == ("tra", N), "r543")


def r544_stderr_cat_dau_phai_khai_so_ky_tu_bi_bo(d: Path):
    """#593 r1 / M3 + A5 — `stderr[-200:]` cat tu dau ma khong noi da bo bao nhieu.

    Hai chieu tren HAM, roi mot lan tren DUONG THAT (`chay_mot_mutant` voi `run`
    gia tra stderr dai): do ham ma khong do duong thi mot ban va quen goi ham van
    xanh (L1 — do CHINH duong ra quyet dinh, khong do ban sao).
      (1) stderr dai TRAN + 37 -> nhan ` …[CAT 37 ky tu dau]`
      (2) stderr bang tran / rong -> KHONG nhan nao
      (3) duong that: `ly_do` KHONG DO DUOC giu DUOI (huong cat khong doi) VA khai dau
    """
    m = _nap_ban_sao(d)
    T = m.TRAN_DUOI_STDERR
    dai = "d" * 37 + "c" * T
    chot(m._khai_cat_dau_stderr(dai) == " …[CAT 37 ky tu dau]", "r544")   # (1)
    chot(m._khai_cat_dau_stderr("c" * T) == "", "r544")                   # (2)
    chot(m._khai_cat_dau_stderr("") == "", "r544")
    # (3) — `run` gia tra stderr, `doc_kenh` gia tra KHONG DO DUOC (nep r522). Vong 3
    # (cross-review v2 F2): HAI chieu tren DUONG THAT — 0/T-1/T/T+37, khong chi dai.
    m.doc_kenh = lambda *a, **k: (m.KHONG_DO_DUOC, "kenh khong ton tai")
    for se in ("", "c" * (T - 1), "c" * T, dai):
        m.run = lambda args, cwd, check=True, env=None, se=se: subprocess.CompletedProcess(args, 1, "", se)
        (bs := d / f"bs{len(se)}").mkdir()
        try:
            tt, ly, _ = m.chay_mot_mutant(bs, "x", ("T1",))
        except Exception as exc:                  # noqa: BLE001 — phan hang, nep r520
            raise TinHieuChotCa(f"chay_mot_mutant nem {type(exc).__name__}: {exc}")
        bo = len(se) - T
        chot(tt == m.KHONG_DO_DUOC and ("…[CAT" in ly) == (bo > 0), "r544")
        chot(f"stderr[-{T}:]={se[-T:]!r}" + (f" …[CAT {bo} ky tu dau]" if bo > 0 else "") in ly, "r544")


def r545_so_ha_tang_moi_diem_nuot_ghi_va_runner_doi_nhan(d: Path):
    """#593 r2 / B1 — co che tren BAN SAO: diem nuot GHI; runner doi nhan theo VI TRI.

    (a) goi THANG NAM diem nuot (diem thu sau, bang chung tu kiem, do o r546);
    (b) runner that tren sau ca gia — DAT/chot co muc so moi, chot trong `except` cua
    mot OSError => DO_KHAC mang loai + thong diep + so lan; ca sach DAT; chot that
    DO_CHOT; loi DA DANG KY khong doi nhan; muc cua ca TRUOC khong lan sang ca SAU.
    """
    m = _nap_ban_sao(d)
    so, cua_ca = m._SO_HA_TANG, []          # CHI loi CA NAY tao; loi that khac o lai so
    ngoai = OSError(5, "r545")              # loi CA NGOAI, CUNG thong diep loi cua ca: phai SONG
    so.loi.append(ngoai)

    La = type("OSError", (OSError,), {})    # MOT lop cho loi cua ca LAN loi thoat `la`: chi DANH TINH phan biet

    def moi(thong_diep):
        cua_ca.append(La(5, thong_diep))
        return cua_ca[-1]

    def hong(*a, **k):
        raise moi("r545")

    class K:                                                 # kenh ma lan DOC nem loi CUA CA NAY
        exists = staticmethod(lambda: True)
        read_text = staticmethod(hong)
    k = K()

    class KB:                                                # kho bare gia: liet ke thu muc nem loi CUA CA
        is_dir = is_file = staticmethod(lambda: False)
        iterdir, __truediv__ = staticmethod(hong), lambda s, _: s
    try:
        la = La(5, "r545")                                  # loi NGOAI CUNG loai/ma/thong diep: phai THOAT ra
        dem = {}
        try:
            for ten, goi in (
                    ("xac_thuc", lambda: m._doc_kenh_xac_thuc(k, "p", "m", 1, ("T1",))),
                    ("doc_kenh", lambda: (setattr(m, "_doc_kenh_xac_thuc", hong),
                                          m.doc_kenh(k, "p", "m", 1, ("T1",)))),
                    ("chay_ca", lambda: (setattr(m, "CA", [("T9", hong)]), m.chay_ca())),
                    ("mutant", lambda: (setattr(m, "run", hong), m.chay_mot_mutant(d, "x", ("T1",)))),
                    ("r508", lambda: (setattr(m, "r508_ban_ghi_luot_TRUOC_chi_khac_dau_phien", hong),
                                      m._chay_r508_tach_nguon_do(m, d / "c", 1))),
                    ("kho-bare", lambda: m._dau_hieu_kho_bare(KB(), "r545")),
                    ("la", lambda: (_ for _ in ()).throw(la))):
                t = len(so.loi)
                try:                     # OSError THOAT ra = diem nuot mat khoi bat: cung la KHONG GHI
                    with contextlib.redirect_stdout(io.StringIO()), contextlib.suppress(m.TinHieuKhongDoDuoc, AssertionError):
                        goi()
                except OSError as loi:
                    if not any(loi is x for x in cua_ca):
                        raise                  # loi THAT, khong phai cua ca: khong duoc nuot
                dem[ten] = sum(1 for e in so.loi[t:] if any(e is x for x in cua_ca))
        except La:                                          # loi cua ca da bi nuot ben trong: chi `la` toi day
            dem["la"] = 1
        chot(all(dem.values()) and "la" in dem, "r545")     # (a)

        def chot_trong_oserror():
            try:
                raise moi("chuoi")
            except OSError:
                m.chot(False, "x")
        tiem, lap, boc = m._tiem(moi("tiem")), moi("lap"), moi("boc")

        def ghi_roi_boc():                    # ghi o diem nuot ROI boc vao chot: dem MOT lan
            m._ghi_ha_tang(boc)
            try:
                raise boc
            except OSError:
                m.chot(False, "x")
        m.TU_KIEM = [("nuot-dat", lambda: [m._ghi_ha_tang(moi("nuot")) for _ in "ab"], False),
                     ("sach", lambda: None, False),
                     ("nuot-chot", lambda: (m._ghi_ha_tang(moi("nuot")), m.chot(False, "x")), False),
                     ("chuoi", chot_trong_oserror, False),
                     ("chot-that", lambda: m.chot(False, "x"), False),
                     ("da-dang-ky", lambda: (m._ghi_ha_tang(tiem), m.chot(False, "x")), False),
                     ("lap-1", lambda: m._ghi_ha_tang(lap), False), ("lap-2", lambda: m._ghi_ha_tang(lap), False),
                     ("ghi-roi-boc", ghi_roi_boc, False)]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            m.chay_tu_kiem()
        nhan = {ln.split(":")[0][8:]: ln for ln in buf.getvalue().splitlines() if ln.startswith("TU KIEM ")}
        kdd = "DO_KHAC — TinHieuKhongDoDuoc: tien de ha tang hong: OSError: [Errno 5] "
        chot(f"{kdd}nuot (2 lan)" in nhan["nuot-dat"] and f"{kdd}nuot (1 lan)" in nhan["nuot-chot"], "r545")
        chot(f"{kdd}chuoi (1 lan)" in nhan["chuoi"], "r545")
        chot(nhan["sach"].endswith(": DAT"), "r545")
        chot(": DO_CHOT" in nhan["chot-that"] and ": DO_CHOT" in nhan["da-dang-ky"], "r545")
        chot(all(f"{kdd}lap (1 lan)" in nhan[c] for c in ("lap-1", "lap-2")), "r545")      # vong 5 F1
        chot(f"{kdd}boc (1 lan)" in nhan["ghi-roi-boc"], "r545")
    finally:                 # xoa DUNG loi cua ca nay: xoa theo vi tri se nuot ca loi THAT (lam tron LEN)
        for e in cua_ca:                  # lop mot: dang ky SAU khi do; lop hai: don theo danh tinh
            m._tiem(e)
        m._bo_cua(cua_ca)   # don r545
        con = any(e is ngoai for e in so.loi)
        m._bo_cua([m._tiem(ngoai)])       # don TRUOC chot: khoi thanh DO_KHAC
    chot(con, "r545")


def r546_ma_tran_doc_hong_qua_runner_that(d: Path):
    """#593 r2 / B2 — MOI ca `TU_KIEM` that, qua `chay_tu_kiem` THAT, duoi loi doc `.json/.jsonl`.

    Truoc r2 do tren 3eb5bd9: 19 ca ra DO_CHOT va 2 ca DAT du loi doc da ban (lam tron
    LEN). Nhan `tien de ha tang` co mat KHI VA CHI KHI ca bi tiem (doi chung duong). Ca khong
    tiem KHONG bi doi DAT: do lai thuoc tinh moi ca la viec cua luot SACH (dac ta B3).
    """
    m = _nap_ban_sao(d)
    so, cua_ca = m._SO_HA_TANG, []
    ngoai = OSError(13, "r546")             # nhu r545: loi CA NGOAI, CUNG thong diep, phai song
    so.loi.append(ngoai)
    g_rt, g_open, dem, sai = Path.read_text, builtins.open, {"n": 0}, []

    def moi():
        dem["n"] += 1
        cua_ca.append(OSError(13, "r546"))
        return cua_ca[-1]

    def rt(self, *a, **k):
        if str(self).endswith((".json", ".jsonl")):
            raise moi()
        return g_rt(self, *a, **k)

    def mo(f, mode="r", *a, **k):
        if not any(c in mode for c in "wax+") and str(f).endswith((".json", ".jsonl")):
            raise moi()
        return g_open(f, mode, *a, **k)
    try:
        for ca in [c for c in m.TU_KIEM if c[0] not in ("r545", "r546")]:
            m.TU_KIEM, dem["n"], buf = [ca], 0, io.StringIO()
            Path.read_text, builtins.open = rt, mo
            try:
                with contextlib.redirect_stdout(buf):
                    m.chay_tu_kiem()
            finally:
                Path.read_text, builtins.open = g_rt, g_open
            dong = [ln for ln in buf.getvalue().splitlines() if ln.startswith(f"TU KIEM {ca[0]}:")]
            if not dong or ("tien de ha tang" in dong[0]) != bool(dem["n"]):
                sai.append(f"{ca[0]}(tiem={dem['n']}): {dong[:1]}")
    finally:                 # xoa DUNG loi cua ca nay, nhu r545
        for e in cua_ca:
            m._tiem(e)
        m._bo_cua(cua_ca)   # don r546
        if not any(e is ngoai for e in so.loi):
            sai.append("loi cua ca NGOAI bi don mat")
        m._bo_cua([m._tiem(ngoai)])
    if sai:
        raise TinHieuChotCa(f"chot cua ca r546 that bai: {'; '.join(sai)[:600]}")


def r547_mien_tru_phai_co_rang_ma_khong_nuot_loi_khac(d: Path):
    """#593 r2 vong 4-5 F2 — moi quyen mien tru/don so, HAI doi tuong CUNG loai/ma/thong diep.

    (1) loc dang ky luc GHI; (2) loc luc DOC cua runner; (3) `_bo_cua` xoa dung doi tuong, giu
    doi tuong CUNG thong diep; (4) tep bang chung VANG khong vao so; (5) `_vang_co_chu_y` bat,
    dang ky va don. Don TRUOC chot: dot bien go mot quyen ra DO_CHOT, khong thanh DO_KHAC.
    """
    so, ok = _SO_HA_TANG, []
    tiem, la = _tiem(OSError(5, "r547")), OSError(5, "r547")
    try:
        _ghi_ha_tang(tiem)
        _ghi_ha_tang(la)
        ok.append(not any(e is tiem for e in so.loi) and any(e is la for e in so.loi))   # (1)
        t = len(so.loi)
        so.loi.extend([tiem, la])                  # CUNG thong diep trong cua so: chi `la` duoc dem
        try:
            _ha_tang_cua_ca(t)
            ok.append(False)
        except TinHieuKhongDoDuoc as exc:
            ok.append("OSError: [Errno 5] r547 (1 lan)" in str(exc))                     # (2)
        _bo_cua([tiem])
        ok.append(not any(e is tiem for e in so.loi) and any(e is la for e in so.loi))   # (3)
    finally:                                   # HAI lop, nhu moi fixture: dang ky roi don
        _bo_cua([_tiem(la), tiem])
    m, vang, bat, doc = _nap_ban_sao(d), [], [], Path.read_text
    proof, run_goc = set(), m.run          # (4) CHI thu loi o DUNG duong proof m.run giao (vong 7)
    entry = 'if __name__' + ' == "__main__":'
    m.DOT_BIEN_TU_KIEM = [("khong-phat-proof", ("r547",), entry, "raise SystemExit(1)\n" + entry)]

    def doc_ghi(self, *a, **k):
        try:
            return doc(self, *a, **k)
        except FileNotFoundError as e:
            if self in proof:
                vang.append(e)
            raise

    def run_ghi(args, cwd, check=True, env=None):
        proof.add(Path((env or {}).get(TU_KIEM_FILE_ENV, "")))
        return run_goc(args, cwd, check=check, env=env)
    Path.read_text, m.run = doc_ghi, run_ghi
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            m.chay_dot_bien_tu_kiem()
        with contextlib.suppress(FileNotFoundError):
            (d / "khac-r547.json").read_text()   # tep KHAC cung loai/ma: KHONG duoc thu
        ok.append(bool(vang) and all(Path(e.filename) in proof for e in vang)
                  and not any(e is x for e in so.loi for x in vang))                    # (4)
        with _vang_co_chu_y(m) as bat:
            m.run([sys.executable, "-c", "pass"], d, check=False, env={TU_KIEM_FILE_ENV: str(d / "p.json")})
            for ten in ("p.json", "khac.json"):      # dung duong proof VA mot tep khac: chi cai dau
                with contextlib.suppress(FileNotFoundError):
                    (d / ten).read_text()
            ok.append(len(bat) == 1 and bat[0].filename == str(d / "p.json"))
            if bat:
                so.loi.append(bat[0])            # ghi THANG, vuot mien tru: lop dang ky + don phai do
            ok.append(bool(bat) and any(bat[0] is t for t in so.tiem))
        ok.append(not any(e is x for e in so.loi for x in bat))                          # (5)
    finally:
        Path.read_text, m.run = doc, run_goc
        _bo_cua([_tiem(e) for e in vang + bat])
    chot(all(ok), "r547")
def r548_git_con_phai_tat_bao_tri_nen(d: Path):
    """#593 r3 M2 — trong tien trinh con moi truong SACH khoa ta (co canh + xung dot `gc.auto` 0-roi-1), CHI
    NAP module roi chup ngay: canh giu nguyen, gia tri HIEU LUC (muc cuoi) cua moi khoa dung, va git con qua
    `m.run()` TRONG tien trinh ay thay dung. Sau do goi lan hai phai khong doi gi. Bang khoa ghi CUNG (F08)."""
    can = {"gc.auto": "0", "gc.autoDetach": "false", "maintenance.auto": "false",
           "maintenance.autoDetach": "false", "receive.autogc": "false"}
    goc = {k: v for k, v in os.environ.items() if not k.startswith("GIT_CONFIG_")}
    dau = [("r548.canh", "giu"), ("gc.auto", "0"), ("GC.auto", "1")]
    tham = "'gc.auto'='1' 'maintenance.auto'='true'"
    ma = ("import importlib.util as u, json, os, sys\n"
          "from pathlib import Path\n"
          "s = u.spec_from_file_location('m548', sys.argv[1]); m = u.module_from_spec(s); s.loader.exec_module(m)\n"
          "chup = lambda: {k: v for k, v in os.environ.items() if k.startswith('GIT_CONFIG_')}\n"
          "sau_nap = chup(); k = Path(sys.argv[2]); m.run(['git', 'init', '-q', str(k)], k.parent)\n"
          "gia = {x: m.run(['git', 'config', '--get', x], k, check=False).stdout.strip() for x in sys.argv[3:]}\n"
          "m._tat_bao_tri_git(os.environ)\n"
          "print(json.dumps([sau_nap, gia, chup()]))\n")
    ok = []
    for i, them in enumerate(({}, {"GIT_CONFIG_PARAMETERS": tham})):
        env = dict(goc, GIT_CONFIG_COUNT=str(len(dau)), **them, **{f"GIT_CONFIG_{t}_{j}": x for j, kv in
                                                                  enumerate(dau) for t, x in zip(("KEY", "VALUE"), kv)})
        p = run([sys.executable, "-c", ma, str(Path(__file__).resolve()), str(d / f"k{i}"), *can], d, check=False, env=env)
        if p.returncode:
            raise AssertionError(f"r548 nap module rc={p.returncode}: {p.stderr[-300:]}")
        sau_nap, gia, lan_hai = json.loads(p.stdout.strip().splitlines()[-1])
        cap = [(sau_nap.get(f"GIT_CONFIG_KEY_{j}"), sau_nap.get(f"GIT_CONFIG_VALUE_{j}"))
               for j in range(int(sau_nap["GIT_CONFIG_COUNT"]))]
        cuoi = {k.lower(): v for k, v in cap}
        ok += [cap[:len(dau)] == dau, all(cuoi.get(k.lower()) == v for k, v in can.items()),
               gia == can, lan_hai == sau_nap, sau_nap.get("GIT_CONFIG_PARAMETERS", "").startswith(them.get("GIT_CONFIG_PARAMETERS", ""))]
    td, remote, _ = kho_bare()      # kho DICH doc tu tep config cua no, moi truong KHONG co GIT_CONFIG_*
    with td:
        ok += [run(["git", "config", "--get", k], remote, env=goc, check=False).stdout.strip() == v for k, v in can.items()]
    chot(all(ok), "r548")

def _manh_gia(d: Path):
    """Ban sao voi BON ham thu thap thay bang do gia DAT TRON; `goi` ghi bang da nhan."""
    m, goi = _nap_ban_sao(d), {}
    m.chay_ca = lambda khung=None: goi.update(ca=True) or []        # Codex #661 luot 2: ghi DAU GOI
    m.chay_tu_kiem = lambda: goi.update(tu_kiem=True) or []
    m.chay_dot_bien = lambda muc=None: goi.update(db=muc, env=MANH_ENV in os.environ or MANH_RA_ENV in os.environ) \
        or (len(muc or m.DOT_BIEN), 0, 0)
    m.chay_dot_bien_tu_kiem = lambda muc=None: goi.update(dbtk=muc) or (len(muc or m.DOT_BIEN_TU_KIEM), 0, 0)
    return m, goi


def _main_manh(m, gia_tri, ra):
    with _moi_truong(**{MANH_ENV: gia_tri, MANH_RA_ENV: ra and str(ra)}):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            return m.main(), out.getvalue()


def r549_manh_sai_hinh_thi_khong_chay_gi(d: Path):
    """#661 A3 — `k/N` sai hinh, hoac vang `..._RA`, => rc 2 va KHONG chay mot ham nao."""
    m, goi = _manh_gia(d)
    m.chay_manh = lambda k, n, db, dbtk, ra: goi.update(db=(k, n)) or 0
    for gia_tri, ra in [(s, d / "x.json") for s in ("4/4", "0/1", "a/4", "0/9", " 0/4", "0/4\n", "00/4", "0/4x", "1/10")] \
            + [("0/4", None), ("0/4", ""), (None, d / "x.json")]:     # sai hinh; vang/rong RA; vang MANH
        chot(_main_manh(m, gia_tri, ra)[0] == 2 and not goi, "r549")
    for dung in ("3/4", "0/2", "7/8"):
        chot(_main_manh(m, dung, d / "x.json")[0] == 0 and goi.pop("db", None) == tuple(map(int, dung.split("/"))), "r549")


def r550_phan_hoach_phu_dung_bang_va_roi_nhau(d: Path):
    """#661 A3 — N manh phu DUNG bang, doi mot roi nhau; ten trung => rc 2, khong chay gi."""
    m, goi = _manh_gia(d)
    for bang in (m.DOT_BIEN, m.DOT_BIEN_TU_KIEM):
        for n in (2, 4, 8):
            ten = [x[0] for k in range(n) for x in m.phan_hoach(bang, k, n)]
            chot(sorted(ten) == sorted(x[0] for x in bang) and len(ten) == len(bang), "r550")
    m.DOT_BIEN_TU_KIEM = list(m.DOT_BIEN_TU_KIEM) + [m.DOT_BIEN_TU_KIEM[5]]
    chot(_main_manh(m, "1/4", d / "x.json")[0] == 2 and not goi, "r550")


def r551_manh_chi_chay_phan_hoach_va_chi_ghi_khi_dat_tron(d: Path):
    """#661 M1 — phan hoach DUNG toi hai vong, bien manh KHONG ro, KHONG in MAU_DAY_DU, ghi CHI khi DAT TRON."""
    m, goi = _manh_gia(d)
    ra = d / "ra" / "m.json"
    rc, out = _main_manh(m, "1/4", ra)
    db, dbtk = m.phan_hoach(m.DOT_BIEN, 1, 4), m.phan_hoach(m.DOT_BIEN_TU_KIEM, 1, 4)
    chot(rc == 0 and goi == {"ca": True, "tu_kiem": True, "db": db, "dbtk": dbtk, "env": False}, "r551")
    x = json.loads(ra.read_text(encoding="utf-8"))
    chot(x == {"phien_ban": 1, "manh": 1, "so_manh": 4, "giet": [y[0] for y in db],
               "tk_giet": [y[0] for y in dbtk], "sha256_tool": hashlib.sha256(TOOL.read_bytes()).hexdigest(),
               "sha256_test": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}, "r551")
    chot(f"MANH 1/4: MUTANT giet = {len(db)} / {len(db)} · TU DOT BIEN giet = {len(dbtk)} / {len(dbtk)}" in out
         and not re.search(r"^MUTANT: giet", out, re.M), "r551")
    hong = {"ca": ("chay_ca", lambda khung=None: ["T1"]), "tu-kiem": ("chay_tu_kiem", lambda: ["r501"])}
    for i in range(6):   # dung MOT so hang cua sau lech
        hong[f"so-{i}"] = ("chay_dot_bien" if i < 3 else "chay_dot_bien_tu_kiem",
                           lambda muc=None, i=i: tuple(len(muc or "") - (j == i % 3) if j == 0 else int(j == i % 3) for j in range(3)))
    for ten, (ham, gia) in hong.items():
        ra.unlink(missing_ok=True)
        m2, _ = _manh_gia(d / ten)
        setattr(m2, ham, gia)
        chot(_main_manh(m2, "1/4", ra)[0] == 1 and not ra.exists(), "r551")
    # `muc` THAT SU la thu vong lap: do gia NEM o muc DAU kem ten, KHONG cham duong bang chung (A1: cham => giet lay).
    m3, dung = _nap_ban_sao(d / "vong"), type("Dung", (Exception,), {})
    nem = lambda ten: (_ for _ in ()).throw(dung(ten))   # noqa: E731
    m3.chay_mot_mutant = lambda ban_sao, ten, dich: nem(ten)
    for ham, muc in ((m3.chay_dot_bien, m3.DOT_BIEN[2:3]), (m3.chay_dot_bien_tu_kiem, m3.DOT_BIEN_TU_KIEM[4:5])):
        try:
            ham(muc)
        except dung as e:
            chot(e.args[0] == muc[0][0], "r551")
        else:
            chot(False, "r551")
        m3.run = lambda args, cwd, *a, **k: nem(Path(cwd).name)


def r552_gop_chi_dat_khi_phu_dung_hai_bang(d: Path):
    """#661 A1/A2 — GOP bon manh THAT (ghi boi `chay_manh`) => DAT; moi lech => rc 1."""
    m, _ = _manh_gia(d)
    goc = d / "goc"
    for k in range(4):
        chot(_main_manh(m, f"{k}/4", goc / f"manh-{k}.json")[0] == 0, "r552")

    def gop(ten, sua=lambda t: None):
        t = d / ten
        shutil.copytree(goc, t)
        sua(t)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            return m.gop(t), out.getvalue()

    def sua(k, f):
        def s(t):
            x = json.loads((t / f"manh-{k}.json").read_text(encoding="utf-8"))
            f(x)
            (t / f"manh-{k}.json").write_text(json.dumps(x), encoding="utf-8")
        return s
    rc, out = gop("dat")
    n, tk = len(m.DOT_BIEN), len(m.DOT_BIEN_TU_KIEM)
    chot(rc == 0 and out == f"GOP MANH 4/4\nMUTANT: giet = {n} · khong giet = 0 · khong do duoc = 0 / tong {n}\n"
         f"TU DOT BIEN: giet = {tk} / {tk}\n", "r552")
    chuyen = m.DOT_BIEN_TU_KIEM[0][0]
    kich = {
        "thieu-tep": lambda t: (t / "manh-3.json").unlink(),
        "thua-manh-rong": lambda t: (t / "manh-9.json").write_text(json.dumps(dict(
            json.loads((t / "manh-1.json").read_text(encoding="utf-8")), giet=[], tk_giet=[])), encoding="utf-8"),
        "manh-bool": sua(1, lambda x: x.update(manh=True)),
        "chuyen-ten": lambda t: (sua(0, lambda x: x["tk_giet"].remove(chuyen))(t),
                                 sua(1, lambda x: x["tk_giet"].append(chuyen))(t)),
        "xoa-ten-giet": sua(2, lambda x: x["giet"].pop()),
        "xoa-ten-tk": sua(2, lambda x: x["tk_giet"].pop()),
        "lap-ten": sua(0, lambda x: x["tk_giet"].append(chuyen)),
        "sha-test": sua(2, lambda x: x.update(sha256_test="0" * 64)),
        "sha-tool": sua(2, lambda x: x.update(sha256_tool="0" * 64)),
        "so-manh": sua(1, lambda x: x.update(so_manh=5)),
        "json-hong": lambda t: (t / "rac.json").write_text("{", encoding="utf-8"),
        "khoa-thua": sua(0, lambda x: x.update(them=1)),
        "phien-ban": sua(3, lambda x: x.update(phien_ban=2)),
        "phien-ban-bool": sua(0, lambda x: x.update(phien_ban=True)),
        "so-manh-float-tep-sau": sua(2, lambda x: x.update(so_manh=4.0)),
        "object-thay-mang": lambda t: [sua(k, lambda x: x.update({c: dict.fromkeys(x[c], False) for c in ("giet", "tk_giet")}))(t)
                                       for k in range(4)],
        "mot-manh": lambda t: [(t / f"manh-{k}.json").unlink() for k in (1, 2, 3)] and sua(0, lambda x: x.update(
            so_manh=1, giet=[y[0] for y in m.DOT_BIEN], tk_giet=[y[0] for y in m.DOT_BIEN_TU_KIEM]))(t),
    }
    for ten, f in kich.items():
        rc, out = gop(ten, f)
        chot(rc == 1 and "GOP: LOI" in out and "GOP MANH" not in out, "r552")
    nhom = m.NHOM_BAT_BUOC
    m.NHOM_BAT_BUOC = nhom | {"r999"}
    chot(gop("nhom")[0] == 1, "r552")
    m.NHOM_BAT_BUOC = nhom - {"r549"}             # khong `thieu`, chi duoi san
    chot(gop("san")[0] == 1, "r552")
    m.NHOM_BAT_BUOC = nhom
    # Duong CLI THAT; `KHONG_DOT_BIEN` de neu `--gop` bi bo qua thi con chi chay T1..T8.
    env = {k: v for k, v in os.environ.items() if not k.startswith("NHANH_DON_DUOC_")}
    p = run([sys.executable, m.__file__, "--gop", str(d / "dat")], d, check=False,
            env=dict(env, NHANH_DON_DUOC_KHONG_DOT_BIEN="1"))
    chot(p.returncode == 0 and p.stdout.startswith("GOP MANH 4/4\n"), "r552")


def r553_ram_windows_du_phong_cap_du_PROCESS_MEMORY_COUNTERS(d: Path):
    """WP748 r20 (connector Codex, PR #849 tren 4e89dd9, P2) — duong du phong `job=None` cua `_ram_dinh_mb`
    cap `_PMC` thieu `PeakPagefileUsage` (7 SIZE_T thay vi 8 theo psapi.h), nen tren Win64 bo dem 64 byte
    thay vi 72, `GetProcessMemoryInfo` that bai, RAM thanh KHONG DO DUOC va `gop_dich` bac mot manh xanh.
    Do HANH VI tren moi nen: psapi gia tu choi `cb` nho hon kich thuoc tai lieu, nhu API that."""
    import ctypes
    from unittest import mock
    # psapi.h: 2 DWORD roi DUNG 8 SIZE_T tu `PeakWorkingSetSize`. Do so O SIZE_T tinh tu `peak_ws`, KHONG do
    # kich thuoc tuyet doi: tren Linux `wintypes.DWORD` la c_ulong 8 byte, so tuyet doi khong phan biet 7 voi 8.
    o = ctypes.sizeof(ctypes.c_size_t)
    nhan = {}

    class _Ham:
        def __init__(self, f):
            self.f = f

        def __call__(self, *a):
            return self.f(*a)

    def _gpmi(_h, ref, cb):
        nhan["o_size_t"] = (cb - type(ref._obj).peak_ws.offset) // o
        if nhan["o_size_t"] < 8 or ctypes.sizeof(ref._obj) < cb:
            return 0                                # ERROR_INSUFFICIENT_BUFFER o API that
        ref._obj.peak_ws = 512 * 2 ** 20
        return 1

    psapi = type("P", (), {})()
    psapi.GetProcessMemoryInfo = _Ham(_gpmi)
    k32 = type("K", (), {})()
    k32.GetCurrentProcess = _Ham(lambda: 1)
    with mock.patch.object(os, "name", "nt"), \
            mock.patch.object(ctypes, "WinDLL", lambda ten, **k: psapi if ten == "psapi" else k32, create=True):
        mb, pham_vi = _ram_dinh_mb(None)
    chot(nhan.get("o_size_t") == 8, "r553")
    chot(mb == 512.0 and pham_vi.startswith("windows PeakWorkingSet CHI tien trinh manh"), "r553")


_PHAN_CHUNG_MOC = frozenset({"moc-sai-dinh-dang", "moc-dao-nguoc", "moc-lech-giay"})


def r554_gop_dich_bac_moc_thoi_gian_hong(d: Path):
    """WP748 r22 F01 (Codex 03c4f6be, P2) — phep gom `_loi_gop_dich` phai bac ba phan chung moc thoi gian (sai dinh
    dang · dao nguoc · lech `giay`) va nhan bo hop le. Moi chot moc co dot bien rieng. Chi do LOP chot moc: do tron
    bo phan chung thi dot bien `gop-bo-kiem-nhom`/`gop-bo-kiem-san` (dich r552) giet them r554 (full_mutant_audit
    39738880374 manh 7 do dung cho nay)."""
    global TU_KIEM
    cu, TU_KIEM = TU_KIEM, _TU_KIEM_DAY_DU
    try:
        # CHI lop chot moc (ban kinh dot bien): chot nhom/bang da co r552 do, khong de r554 chet theo dot bien cua no
        lot, tong, hop_le = _phan_chung_gop_dich(chi=_PHAN_CHUNG_MOC)
    finally:
        TU_KIEM = cu
    chot(not lot and (tong, hop_le) == (1 + len(_PHAN_CHUNG_MOC), 1), "r554")


_NHIP_CHAU = """import os, pathlib, sys, time
p = pathlib.Path(sys.argv[1])
(p.parent / (p.name + ".pid")).write_text(str(os.getpid()))
for i in range(1200):                    # ~60 s: LAU hon moi han cho, de nhip chi dung khi BI GIET
    p.write_text(str(i))
    time.sleep(0.05)
"""


R555_DAU_ENV = "NHANH_DON_DUOC_R555"


def _don_r555(dau: str) -> None:
    """WP748 r22 l2 lo 5 — don chau cua r555 THEO DANH TINH, khong theo PID tu tep: POSIX quet dau env rieng cua r555
    roi `_giet_dinh_danh`; Windows: `run` da dong job `KILL_ON_JOB_CLOSE` nen KHONG giet theo PID nao ca."""
    import time as _t
    han = _t.monotonic() + _GIAY_THU_SAU_GIET
    while os.name != "nt" and _t.monotonic() < han:
        con = _quet_dau_posix(R555_DAU_ENV, dau) or {}
        song = {p: k for p, k in con.items() if _con_song_posix(p, k)}
        if not song:
            return
        for pid, khoa in song.items():
            _giet_dinh_danh(pid, khoa)
        _t.sleep(0.05)


def r555_tran_giay_con_giet_ca_chau(d: Path):
    """WP748 r22 F02 (Codex 03c4f6be + l22, P2) — qua `_TRAN_GIAY_CON` thi `run` phai giet CA CHAU, khong chi con, va tra
    co han. Chau GIU ong stdout cua con (dung dieu kien lam Windows treo o `communicate()`) va ghi nhip tim: sau khi
    `run` tra rc 124 thi nhip phai DUNG. Ba bien the: chau cung nhom; chau TACH phien/nhom (POSIX `setsid` thoat
    `killpg`; Windows nhom moi van nam trong job); va (l2 lo 1) chau tach phien MO COI — con thoat ngay, chau doi PPID
    ve 1 nen phep di PPID khong thay, chi dau env bat duoc. Chau chua kip chay truoc han = KHONG DO DUOC = DO."""
    global _TRAN_GIAY_CON
    import time as _t
    tach_phien = ("start_new_session=True" if os.name != "nt"
                  else "creationflags=subprocess.CREATE_NEW_PROCESS_GROUP")
    for ten, tach, ngu in (("cung", "", 60), ("tach", tach_phien, 60), ("mo-coi", tach_phien, 0)):
        nhip = d / f"nhip-{ten}"
        con = ("import subprocess, sys, time; "
               f"subprocess.Popen([sys.executable, '-c', {_NHIP_CHAU!r}, {str(nhip)!r}]{', ' + tach if tach else ''}); "
               f"time.sleep({ngu})")
        dau = secrets.token_hex(16)
        cu = _TRAN_GIAY_CON
        try:
            _TRAN_GIAY_CON = 1.5
            t0 = _t.monotonic()
            p = run([sys.executable, "-c", con], cwd=d, check=False, env=dict(os.environ, **{R555_DAU_ENV: dau}))
            troi = _t.monotonic() - t0
        finally:
            _TRAN_GIAY_CON = cu
        try:
            chot(p.returncode == 124 and "QUA TRAN" in p.stderr, "r555")
            # giet dung ca cay thi khong co gi giu ong: tra ngay. Han 3 s < `_GIAY_THU_SAU_GIET` nen mot cay con song
            # (kiem-lai cho ca han, roi thu output cho ca han) cung lam ca nay DO, doc lap voi nhip tim.
            chot(troi < 1.5 + 3.0, "r555")
            chot(nhip.is_file(), "r555")
            _t.sleep(0.3)
            v1 = nhip.read_text()
            _t.sleep(0.6)
            chot(nhip.read_text() == v1, "r555")
        finally:
            _don_r555(dau)


def r556_tran_giay_khong_ranh_gioi_va_don_cay_nem(d: Path):
    """WP748 r22 l2 lo 2 + lo 3 (Codex l22 F02) — gia lap, MOI nen: (a) khong dung duoc job => rc
    `MA_KHONG_RANH_GIOI`, con KHONG duoc tao; (b) gan job / chay tiep hong => con (dang treo) bi giet va cho, KHONG
    `communicate`; (c) don cay NEM => van rc 124, dong khai `LOI don cay`, con bi giet (`_ghi_ha_tang` chi ghi
    `OSError` that, nen loi tiem o day khong vao so)."""
    global _TRAN_GIAY_CON, _VeWindows, _ket_thuc_cay
    from unittest import mock
    tao = []

    class _Q:
        pid, _handle, returncode = 4242, 0, None

        def __init__(self, *a, **k):
            tao.append(self)
            self.lam = []

        def kill(self):
            self.lam.append("kill")

        def wait(self, timeout=None):
            self.lam.append("wait")
            return -9

        def communicate(self, timeout=None):
            self.lam.append("communicate")
            return "", ""

    def ve_gia(dung, gan):
        class _V:
            CREATE_SUSPENDED, loi = 0x4, "gia"

            def __init__(self):
                self.dong_goi = 0

            def dung_duoc(self):
                return dung

            def gan_va_chay(self, q):
                if not gan:
                    q.kill()
                return gan

            def dong(self):
                self.dong_goi += 1
        return _V
    cu_tran, cu_ve, cu_kt = _TRAN_GIAY_CON, _VeWindows, _ket_thuc_cay
    try:
        _TRAN_GIAY_CON = 1.0
        for dung, gan in ((False, True), (True, False)):
            tao.clear()
            _VeWindows = ve_gia(dung, gan)
            with mock.patch.object(os, "name", "nt"), mock.patch.object(subprocess, "Popen", _Q):
                p = run(["khong-chay"], cwd=d, check=False)
            chot(p.returncode == MA_KHONG_RANH_GIOI and "KHONG DUNG DUOC ranh gioi job" in p.stderr, "r556")
            if not dung:
                chot(tao == [], "r556")
            else:
                chot(len(tao) == 1 and tao[0].lam == ["kill", "wait"], "r556")
        _VeWindows = cu_ve
        loi = RuntimeError("r556 don cay nem")

        def nem(*a, **k):
            raise loi
        _ket_thuc_cay = nem
        try:
            p = run([sys.executable, "-c", "import time; time.sleep(30)"], cwd=d, check=False)
        except Exception:                             # noqa: BLE001 — ngoai le thoat ra chinh la loi can bat
            p = None
        chot(p is not None and p.returncode == 124 and "LOI don cay RuntimeError" in p.stderr, "r556")
    finally:
        _TRAN_GIAY_CON, _VeWindows, _ket_thuc_cay = cu_tran, cu_ve, cu_kt


def r557_quet_dau_va_giet_dinh_danh(d: Path):
    """WP748 r22 l2 lo 1 + lo 4 — tren `/proc` GIA (moi nen): `_quet_dau_posix` chi tra tien trinh mang dung dau, ke ca
    khi khong ai la con cua ai; `None` khi khong co `/proc`. `_giet_dinh_danh`: `starttime` lech => KHONG gui tin hieu;
    khop => gui qua `pidfd`; khong co `pidfd` => lui ve kill theo PID va TRA DUNG la khe con mo."""
    from unittest import mock
    goc = d / "proc"

    def tt(pid, ppid, bat_dau, moi_truong):
        (goc / str(pid)).mkdir(parents=True)
        (goc / str(pid) / "stat").write_text(f"{pid} (x) S {ppid} " + " ".join(["0"] * 17) + f" {bat_dau}\n")
        if moi_truong is not None:
            (goc / str(pid) / "environ").write_bytes(moi_truong)
    tt(101, 1, "500", b"A=1\0" + DAU_CAY_ENV.encode() + b"=abc\0")
    tt(102, 1, "501", b"A=1\0" + DAU_CAY_ENV.encode() + b"=abcd\0")
    tt(103, 1, "502", None)
    chot(_quet_dau_posix(DAU_CAY_ENV, "abc", str(goc)) == {101: "500"}, "r557")
    chot(_quet_dau_posix(DAU_CAY_ENV, "abc", str(d / "khong-co")) is None, "r557")
    gui = []
    with mock.patch.object(os, "pidfd_open", lambda pid: os.open(os.devnull, os.O_RDONLY), create=True), \
            mock.patch.object(signal, "pidfd_send_signal", lambda fd, sig: gui.append(sig), create=True):
        chot(_giet_dinh_danh(101, "499", str(goc)) == "khac danh tinh" and gui == [], "r557")
        chot(_giet_dinh_danh(101, "500", str(goc)) == "pidfd" and len(gui) == 1, "r557")
    giet = []
    with mock.patch.object(os, "pidfd_open", None, create=True), \
            mock.patch.object(os, "kill", lambda pid, sig: giet.append(pid)):
        chot(_giet_dinh_danh(101, "499", str(goc)) == "khac danh tinh" and giet == [], "r557")
        chot("KHE" in _giet_dinh_danh(101, "500", str(goc)).upper() and giet == [101], "r557")

TU_KIEM = [
    ("r542", r542_kenh_hoan_tat_khong_duoc_xoa_chan_doan, True),
    ("r539", r539_bang_chung_phai_den_tu_con_chay_that, True),
    ("r540", r540_so_hang_va_bang_chung_phai_nhat_quan, True),
    ("r541", r541_khong_do_duoc_khong_duoc_lam_xanh_main, True),
    ("r501", r501_tin_hieu_chot_khong_gia_mao_duoc, True),
    ("r502", r502_assert_ha_tang_khong_duoc_cap_lop_chot, True),
    ("r503", r503_chot_cua_ca_KHAC_khong_tinh_la_giet, True),
    ("r504", r504_ba_trang_thai_khong_gop, True),
    ("r505", r505_chay_lai_dung_mot_lan, True),
    ("r506", r506_moi_kho_deu_tat_ky_commit, True),
    ("r507", r507_kenh_ket_qua_ba_bien, True),
    ("r508", r508_ban_ghi_luot_TRUOC_chi_khac_dau_phien, True),
    ("r509", r509_dau_phien_phai_sinh_moi_moi_luot, True),
    ("r510", r510_ban_ghi_thieu_dau_dong_luot, True),
    ("r511", r511_ma_san_pham_phat_khong_doat_duoc_ten_ca, True),
    ("r512", r512_kenh_khong_lan_voi_stdout, True),
    ("r513", r513_moi_dieu_kien_cong_cua_main_phai_do_duoc, True),
    ("r514", r514_bo_cong_that_phan_dung_ba_nhanh, True),
    ("r515", r515_moi_chieu_neo_deu_co_ca_am, True),
    ("r516", r516_bo_cham_tu_dot_bien_phan_hang_dung, True),
    ("r517", r517_kenh_phai_duoc_xac_thuc_truoc_khi_tin, True),
    ("r518", r518_kenh_chiu_duoc_ky_tu_phan_dong_unicode, True),
    ("r519", r519_dich_phai_duoc_xac_thuc_truoc_khi_cap_tin_dung, True),
    ("r520", r520_loi_phong_con_phai_o_lai_trong_vong_chay_lai, True),
    ("r521", r521_dich_mot_lan_doc_khong_duoc_bi_tieu_thu, True),
    ("r522", r522_loi_phong_ngoai_oserror_cung_phai_o_lai_vong, True),
    ("r523", r523_ban_sao_tuong_doi_khong_duoc_lam_lech_kenh, True),
    ("r524", r524_chan_doan_cua_con_khong_duoc_mat_o_lop_phan_hang, True),
    ("r525", r525_nhanh_thu_ba_phai_noi_vi_sao_ca_khi_con_chet_truoc_khi_in, True),
    ("r526", r526_ma_nguon_khong_duoc_sinh_canh_bao_escape_sequence, True),
    ("r527", r527_tien_de_hai_dau_phien_phai_do_duoc_ba_trang_thai, True),
    ("r528", r528_tien_de_khong_con_chap_duoi_chinh_dot_bien, True),
    ("r529", r529_tach_dong_phai_bang_dung_bo_doc_cu, True),
    ("r530", r530_hai_nhanh_chuyen_tiep_con_lai_phai_co_dot_bien_canh, True),
    ("r531", r531_ranh_gioi_bo_dong_nao_thi_phai_khai, True),
    ("r532", r532_khai_dung_duong_da_bao_chot_roi_chet_tiep, True),
    ("r533", r533_ranh_gioi_phai_dung_hinh_ban_ghi, True),
    ("r534", r534_nhan_bo_dong_phai_song_qua_tran, True),
    ("r535", r535_moi_ho_tien_to_deu_phai_dung_hinh, True),
    ("r536", r536_con_khong_duoc_doat_so_do_cua_cha, True),
    ("r537", r537_chuan_hoa_than_khong_duoc_sua_noi_dung, True),
    ("r538", r538_bien_phai_cua_nhan_phai_co, True),
    ("r543", r543_tien_de_ha_tang_cua_r528_phai_ra_trang_thai_thu_ba, True),
    ("r544", r544_stderr_cat_dau_phai_khai_so_ky_tu_bi_bo, True),
    ("r545", r545_so_ha_tang_moi_diem_nuot_ghi_va_runner_doi_nhan, True),
    ("r546", r546_ma_tran_doc_hong_qua_runner_that, True),
    ("r547", r547_mien_tru_phai_co_rang_ma_khong_nuot_loi_khac, True),
    ("r548", r548_git_con_phai_tat_bao_tri_nen, True),
    ("r549", r549_manh_sai_hinh_thi_khong_chay_gi, True),
    ("r550", r550_phan_hoach_phu_dung_bang_va_roi_nhau, True),
    ("r551", r551_manh_chi_chay_phan_hoach_va_chi_ghi_khi_dat_tron, True),
    ("r552", r552_gop_chi_dat_khi_phu_dung_hai_bang, True),
    ("r553", r553_ram_windows_du_phong_cap_du_PROCESS_MEMORY_COUNTERS, True),
    ("r554", r554_gop_dich_bac_moc_thoi_gian_hong, True),
    ("r555", r555_tran_giay_con_giet_ca_chau, True),
    ("r556", r556_tran_giay_khong_ranh_gioi_va_don_cay_nem, True),
    ("r557", r557_quet_dau_va_giet_dinh_danh, True),
]
# WP748 r22 — ban DAY DU, `main` cua con targeted thu hep `TU_KIEM` nhung khong dung toi ten nay: r554 do phep gom tren
# TRON phan hoach (`_muc_dich` doi GIAY_CA_HO_SO khop du bang), nen chay ca ay voi bang day du.
_TU_KIEM_DAY_DU = list(TU_KIEM)

# ---- A6: MOI ca tu kiem phai co MOT dot bien rieng lam no DO --------------
# Ca khong doi mau theo dot bien duoc chi dinh thi KHONG duoc tinh vao so nhom.
DOT_BIEN_TU_KIEM = [
    ('tk-inherit-outer-proof', ('r539',), '    nonce = os.environ.pop(TU_KIEM_NONCE_ENV, None)\n    proof_path = os.environ.pop(TU_KIEM_FILE_ENV, None)', '    nonce = os.environ.get(TU_KIEM_NONCE_ENV)\n    proof_path = os.environ.get(TU_KIEM_FILE_ENV)'),
    ('tk-proof-decode-escape', ('r539',), '            except (OSError, UnicodeError):', '            except OSError:'),
    ('tk-unbounded-number', ('r539', 'r540'), '    if any(len(number) > len(str(len(expected))) for number in totals[0]):', '    if False:'),
    ('tk-json-recursion-escape', ('r539',), '    except (ValueError, TypeError, RecursionError):\n        return False', '    except (ValueError, TypeError):\n        return False'),
    ('tk-diagnostic-prefix-erasure', ('r542',), '            kh_chot = _khoi_chan_doan(p.stdout, "DO_CHOT")', '            p.stdout = "\\n".join(line for line in p.stdout.split("\\n") if not line.startswith("TU KIEM XONG: "))\n            kh_chot = _khoi_chan_doan(p.stdout, "DO_CHOT")'),
    ('tk-proof-malformed', ('r525', 'r530', 'r532', 'r539', 'r540'), '    except (ValueError, TypeError, RecursionError):\n        return False', '    except (ValueError, TypeError, RecursionError):\n        return True'),
    ('tk-proof-nonce', ('r539', 'r540'), '    if not isinstance(proof, dict) or proof.get("nonce") != nonce:\n        return False', '    if not isinstance(proof, dict) or proof.get("nonce") != nonce:\n        return True'),
    ('tk-proof-cases', ('r539', 'r540'), '    if proof.get("cases") != expected:\n        return False', '    if proof.get("cases") != expected:\n        return True'),
    ('tk-summary-count', ('r540',), '    if len(totals) != 1:\n        return False', '    if len(totals) != 1:\n        return True'),
    ('tk-summary-total', ('r540',), '    if total != len(expected):\n        return False', '    if total != len(expected):\n        return True'),
    ('tk-summary-diagnostics', ('r540',), '    return total - passed == len(failed)', '    return True'),
    ('tk-duplicate-diagnostic', ('r540',), '    if len(failed) != len(set(failed)) or not set(failed) <= set(expected):', '    if not set(failed) <= set(expected):'),
    ('tk-unknown-diagnostic', ('r540',), '    if len(failed) != len(set(failed)) or not set(failed) <= set(expected):', '    if len(failed) != len(set(failed)):'),
    ('tk-always-unmeasurable', ('r516', 'r525', 'r530', 'r539', 'r540', 'r542'), '    return total - passed == len(failed)', '    return False'),
    ('tk-main-ignore-unmeasurable', ('r541',), '    if tk_khong_do:', '    if False:'),
    ("bo-phan-biet-lop-ngoai-le", ("r501", "r504", "r518"),
     "if any(n == NHAN_DO_KHAC for n in theo_ca.values()):", "if False:"),
    ("cap-lop-chot-cho-assert-ha-tang", ("r502",),
     "    assert spec and spec.loader", '    chot(spec and spec.loader, "nap_tool")'),
    # r512 cung do: bo phep so bien KHONG_GIET thanh GIET, ma r512 doi KHONG_GIET.
    ("bo-so-tap-ca-do-voi-dich", ("r503", "r504", "r505", "r512", "r515", "r521"),
     "    if do_chot == set(dich):", "    if True:"),
    # r509 do kem: no dem HAI dau phien tu HAI luot phong that.
    ("bo-tran-chay-lai", ("r505", "r509", "r517", "r520", "r521", "r522"), "    for lan_thu in (1, 2):", "    for lan_thu in (1,):"),
    ("go-tat-ky-o-kho-mutant", ("r506",),
     '        run(["git", "config", "commit.gpgsign", "false"], src)', "        pass"),
    ("bo-kiem-ban-ghi-trung", ("r507", "r511"), "        if ca in theo_ca:", "        if False:"),
    # r509 do kem tu luot 2: bo so dau phien thi ban ghi luot MOT duoc nhan o luot HAI.
    # #593 — `dich` len ba ten. Tu khi `r528` chay CHINH `r508` 2 000 luot (chot
    # (c1)/(c2), them theo P2 cua cross-review codex), moi dot bien lam `r508` do
    # qua mot duong ma `r528` KHONG de len deu giet ca `r528`. Muc nay dung the:
    # no sua phep so dau phien trong `doc_kenh`, cho ma `r528` khong thay.
    # Doi chung: `dau-phien-thanh-moc-giay` van 2/2, vi no sua CHINH
    # `sinh_dau_phien` — thu ma `r528` de len bang bo sinh cua rieng no. Hai muc
    # phan biet duoc bang dau vao, khong phai bo tuong duong.
    # Ca ba deu chet bang DO_CHOT — chot cua chinh chung.
    # #593 r1 — `r543` cung chet (DO tu luot day du, khong chep tay): doi chung duong A2
    # cua no chay `r508` THAT N lan, nen moi dot bien lam r508 do deu lam A2 do. Cung
    # le voi `dau-phien-ha-tran-xuong-khong`.
    ("bo-so-dau-phien", ("r508", "r509", "r528", "r543"),
     '    neo = {"dau_phien": dau_phien, "mutant": mutant, "lan_thu": lan_thu}',
     '    neo = {"mutant": mutant, "lan_thu": lan_thu}'),
    # r508 cung do: dau theo moc giay thi ph_that va ph_khac cua r508 TRUNG nhau
    # trong cung mot giay, nen ban ghi "chi khac dau phien" duoc NHAN => ca do.
    ("dau-phien-thanh-moc-giay", ("r508", "r509"),
     "    return secrets.token_hex(16)",
     '    import time as _tg\n    return str(int(_tg.time()))'),
    # F01 (luot 3) — ban cu (`if dong is None:` -> `if False:`) giet r505/r509/r510
    # bang BA `AttributeError` o `dong.get("rc")`, tuc TIN DUNG GIA: no chung minh
    # mot ngoai le vo can, khong chung minh A5c(2). Nay dung mot duong CHAP NHAN
    # ban ghi dong GIA hop le, de r509/r510 toi duoc CHINH chot cua chung.
    # luot 7 — r538 co mat: xoa mot cau `return KHONG_DO_DUOC` cua doc_kenh thi ngu
    # phap sinh tu AST lech khoi `ranh` (loi khai cot vao nguon). DO DUOC, khong chep tay.
    ("bo-doi-ban-ghi-dong-luot", ("r509", "r510", "r538"),
     '    if dong is None:\n        return KHONG_DO_DUOC, "thieu ban ghi dong luot"',
     '    if dong is None:\n        dong = {"rc": 0 if rc_that is None else rc_that}'),
    ("khung-lay-ten-ca-tu-doi-so", ("r511",),
     "        ban_ghi = dict(self._neo, ca=self._ca_dang_chay, nhan=nhan, chi_tiet=chi_tiet)",
     '        _ca = chi_tiet.split("la ")[-1] if "tu khai la" in chi_tiet else self._ca_dang_chay\n'
     "        ban_ghi = dict(self._neo, ca=_ca, nhan=nhan, chi_tiet=chi_tiet)"),
    # L3 (luot 2) — `cham-doc-stdout-thay-vi-kenh` cu SUA CHINH ASSERTION cua r512,
    # tuc no chung minh "viet duoc mot assert sai", KHONG chung minh ca co rang voi
    # mot bo cham hong. Da BO. Hai dot bien duoi day doi DUONG RA QUYET DINH THAT.
    ("cham-doc-stdout-vo-dieu-kien", ("r512",),
     "        trang_thai, ly_do = doc_kenh(kenh, dau_phien, ten, lan_thu, dich, p.returncode)",
     "        trang_thai, ly_do = doc_kenh(kenh, dau_phien, ten, lan_thu, dich, p.returncode)\n"
     '        if set(re.findall(r"^CASE (T\\d+): DO", p.stdout, re.M)) == set(dich):\n'
     "            trang_thai = GIET"),
    # Bien the GAI DIEU KIEN o mot bien KHAC — dung ca da song sot qua chot DIEM.
    # r505 do kem TU luot 4: fixture terminal GIET co rc=1 va stdout RONG, nen
    # duong doc stdout lat no thanh KHONG GIET. Khai dung tap do THUC TE.
    # F04 (luot 6) — THU HOI mot GIET hop le vi stdout mang ten NGOAI dich.
    ("cham-thu-hoi-giet-vi-stdout", ("r512",),
     "        trang_thai, ly_do = doc_kenh(kenh, dau_phien, ten, lan_thu, dich, p.returncode)",
     "        trang_thai, ly_do = doc_kenh(kenh, dau_phien, ten, lan_thu, dich, p.returncode)\n"
     '        if trang_thai == GIET and set(re.findall(r"^CASE (T\\d+): DO", p.stdout, re.M)) - set(dich):\n'
     "            trang_thai = KHONG_GIET"),
    ("cham-doc-stdout-khi-rc-mot", ("r505", "r512", "r520", "r521", "r522", "r523"),
     "        if trang_thai == KHONG_DO_DUOC:",
     "        if p.returncode == 1 and trang_thai != KHONG_DO_DUOC:\n"
     '            trang_thai = GIET if set(re.findall(r"^CASE (T\\d+): DO", p.stdout, re.M)) == set(dich) else KHONG_GIET\n'
     "        if trang_thai == KHONG_DO_DUOC:"),
    # F02 — doi LOP BAT cua runner THAT: loi ha tang (AssertionError tran) bi
    # nhan nham thanh chot cua ca. Ban cu cua r501 tu viet `except` nen mu.
    # Neo phai keo them dong sau: `    except TinHieuChotCa as exc:` nay khop
    # CA `chay_ca` LAN `chay_tu_kiem` (chuoi con cua dong 12-space).
    ("runner-bat-assertion-tran", ("r501",),
     '        except TinHieuChotCa as exc:\n            do.append(ten)\n'
     '            print(f"CASE {ten}: DO — {exc}")',
     '        except AssertionError as exc:\n            do.append(ten)\n'
     '            print(f"CASE {ten}: DO — {exc}")'),
    # F04 — GIU dong tat ky (AST van thay) nhung KHONG CHAY no.
    ("src-tat-ky-khong-chay", ("r506",),
     '        run(["git", "config", "commit.gpgsign", "false"], src)',
     '        if False:\n            run(["git", "config", "commit.gpgsign", "false"], src)'),
    # F06 — xin ZERO byte ngau nhien roi ghep bo dem: dau van dai va van khac nhau.
    ("zero-entropy-bo-dem", ("r509",),
     "    return secrets.token_hex(16)",
     '    globals()["_dem_ph"] = globals().get("_dem_ph", 0) + 1\n'
     '    return secrets.token_hex(0) + format(globals()["_dem_ph"], "032x")'),
    # F07 — ba dieu kien cong cua `main()`, moi cai mot dot bien RIENG.
    # F07 — IN mot dang, QUYET DINH mot dang khac: rc van dung, chi dong in sai.
    ("in-sai-so-hang", ('r513',),
     '    print(f"MUTANT: giet = {dat} · khong giet = {khong_giet} · khong do duoc = {khong_do}"',
     '    print(f"MUTANT: giet = {dat} · khong giet = {khong_giet} · khong do duoc = {khong_giet}"'),
    ("mo-cong-tong", ('r513',),
     "    if dat + khong_giet + khong_do != len(DOT_BIEN):", "    if False:"),
    ("mo-cong-nhom-bat-buoc", ('r513',),
     "    if thieu or len(NHOM_BAT_BUOC) < SAN_NHOM or tk_hong or tk_giet != len(DOT_BIEN_TU_KIEM):",
     "    if False:"),
    ("mo-cong-cuoi", ('r513',),
     "    return 0 if (dat == len(DOT_BIEN) and not tu_kiem_do) else 1", "    return 0"),
    # F07 — bo cong THAT: cong nham mot loai sang loai khac.
    # F04 — dem LAN THU thay vi dem MUTANT, o hai nhanh con lai.
    # F05 (luot 6) — CONG BU: chuyen 2 don vi GIET->KG o (GIET, lan 2) roi tra 1
    # don vi nguoc lai o moi (KG, lan 2). Tong van `(2,3,5)`; chi phep do TUNG
    # VECTO CO SO moi thay (bo cong that tra `(-1, 2, 0)` cho mot GIET-lan-2).
    ("cong-bu-theo-lan-thu", ("r514",),
     "                dat += 1", "                dat += 3 - 2 * so_lan"),
    ("cong-giet-theo-so-lan", ("r514",),
     "                dat += 1", "                dat += so_lan"),
    ("cong-khong-giet-theo-so-lan", ("r514",),
     "                khong_giet += 1", "                khong_giet += so_lan"),
    # F02 (luot 5) — DOI CHEO hai nhan: `(2,3,3)` cu khong phan biet duoc, `(2,3,5)`
    # thi co.
    ("doi-cheo-khong-giet-va-khong-do", ("r514",),
     "            elif trang_thai == KHONG_DO_DUOC:", "            elif trang_thai == KHONG_GIET:"),
    ("gop-khong-do-vao-khong-giet", ("r514",),
     "                khong_do += 1", "                khong_giet += 1"),
    # F01 — bo TUNG chieu neo, moi chieu mot dot bien rieng.
    ("bo-so-mutant", ("r515",),
     '    neo = {"dau_phien": dau_phien, "mutant": mutant, "lan_thu": lan_thu}',
     '    neo = {"dau_phien": dau_phien, "lan_thu": lan_thu}'),
    ("bo-so-lan-thu", ("r515",),
     '    neo = {"dau_phien": dau_phien, "mutant": mutant, "lan_thu": lan_thu}',
     '    neo = {"dau_phien": dau_phien, "mutant": mutant}'),
    # F01 (luot 7) — moi chot XAC THUC KENH mot dot bien rieng.
    ("ban-sau-ghi-de-ban-dong-luot", ("r517",),
     "        if dong is not None:\n            return KHONG_DO_DUOC, \"co ban ghi SAU ban ghi dong luot\"",
     "        if False:\n            return KHONG_DO_DUOC, \"co ban ghi SAU ban ghi dong luot\""),
    ("bo-tach-ca-voi-dong-luot", ("r517",),
     "        if co_ca and co_dong:", "        if False:"),
    # R13-F02 — quay ve ep kieu: moi thu truthy lai duoc nhan la dau dong.
    ("ep-kieu-dau-dong-luot", ("r517",),
     '        co_dong = r.get("dong_luot") is True',
     '        co_dong = bool(r.get("dong_luot"))'),
    ("bo-xac-thuc-nhan", ("r517",),
     "        if nhan not in NHAN_HOP_LE:", "        if False:"),
    ("bo-xac-thuc-kieu-ten-ca", ("r517",),
     "        if not isinstance(ca, str):", "        if False:"),
    ("bo-xac-thuc-object", ("r517",),
     "        if not isinstance(r, dict):", "        if False:"),
    ("nhan-rc-bool", ("r517",),
     '    if not isinstance(dong.get("rc"), int) or isinstance(dong.get("rc"), bool):',
     '    if not isinstance(dong.get("rc"), int):'),
    # Ban dau toi viet dot bien nay THEM mot `except ZeroDivisionError` TRUOC vo —
    # cu phap hop le nhung `except Exception` van bat, tuc dot bien KHONG tat duoc
    # thu no dinh tat. Phai THU HEP chinh lop bat.
    # F01 (luot 8) — do RANG cua ben DOC. Ben GHI giu `ensure_ascii=False`
    # CO Y, nen day la chot DUY NHAT chan ba ky tu phan dong Unicode; khong
    # co dot bien song doi o ben ghi vi sua ca hai se lam CA HAI tuong duong.
    ("doc-tach-dong-bang-splitlines", ("r518",),
     '    for dong_txt in noi_dung.split("\\n"):',
     "    for dong_txt in noi_dung.splitlines():"),
    # F01 (luot 10) — HAI chot cua r519 do HAI thu khac nhau, nen HAI dot bien.
    ("bo-xac-thuc-dich-rong", ("r519", "r521", "r538"),
     '    if not dich:\n        return KHONG_DO_DUOC, "dich RONG: khong cap GIET khi khong ca nao phai chet"',
     "    if False:\n        pass"),
    ("bo-xac-thuc-ten-dich-la", ("r519",),
     '    dich_la = sorted(set(dich) - ten_ca)',
     "    dich_la = []"),
    # F04 (luot 11) — HAI duong vao, HAI chot, nen HAI dot bien rieng.
    ("bo-vat-hoa-dich-o-doc-kenh", ("r521",),
     "lan_thu, tuple(dich), rc_that)",
     "lan_thu, dich, rc_that)"),
    # #568 — BON duong vao cua r524, moi duong mot dot bien RIENG. Go tung cai
    # phai doi mau r524; neu hai cai khong phan biet duoc bang dau vao thi chung
    # la bo TUONG DUONG va ta chi dang do MOT thu.
    # #568 r4 — `dich` len ("r524","r530"): tu khi `r530` do NHANH DO_KHAC o LOP
    # CHA, dot bien vut than chan doan giet THAT ca hai. Chet bang DO_CHOT, chot
    # cua chinh chung.
    ("chan-doan-chi-lay-ten-ca", ('r524', 'r530', 'r531', 'r534', 'r536', 'r537'),
     '            khoi.append([m.group(1), [_go_dau_phan_cach(m.group(2))], 0])',
     '            khoi.append([m.group(1), [""], 0])'),
    ("chan-doan-dung-o-dong-dau", ('r524', 'r531', 'r533', 'r535', 'r536', 'r537', 'r538', 'r542'),
     "        elif dang_mo:", "        elif False:"),
    # #568 r5 — NEO DOI theo M13: dong `ranh` da hep lai, nen neo CU dem ra 0 va
    # muc nay CHET LANG (bao "NEO KHONG DUY NHAT (0)" roi thanh `hong`). Mot dot
    # bien chet lang la mot cho mu — do dung thu ma bang nay ton tai de chan.
    # Chung mot dong neo voi `chan-doan-tra-ranh-gioi-ve-ban-rong` la binh thuong:
    # hai muc thay HAI thu khac nhau nen phan biet duoc bang dau vao.
    # r3/M9 — `dich` nang len ("r524","r525"): o `suy-bien-dai` MOI cung chot
    # rang cha PHAI noi la no da cat, nen dot bien nay giet THAT ca hai. Khai
    # dung hai ten la khai CHAT HON, khong phai noi long: bo cham doi tap ca do
    # BANG DUNG `dich`, nen thieu mot ten la ca DO. Ca chet bang DO_CHOT — chot
    # cua chinh no — chu khong phai mot loi VO CAN. Da do: 84/85 -> 85/85.
    ("chan-doan-cat-lang-khong-khai", ('r524', 'r525', 'r531', 'r534', 'r536'),
     '    return f"{than[:TRAN_CHAN_DOAN]} \u2026[CAT {len(than) - TRAN_CHAN_DOAN} ky tu]{duoi}"',
     "    return than[:TRAN_CHAN_DOAN]"),
    # #568 r2/M6 — HAI duong cua nhanh thu ba, moi duong mot dot bien RIENG.
    # Chung phan biet duoc bang DAU VAO: (1) go han phep in stderr o ca suy bien;
    # (2) in stderr KE CA khi co DO_CHOT, tuc xoa han phan biet P1/P2.
    ("chan-doan-bo-stderr-o-ca-suy-bien", ('r525',),
     '                    print(f"    stderr: {_goi_chan_doan(p.stderr)}")',
     "                    pass"),
    ("chan-doan-xoa-phan-biet-P1-P2", ('r525', 'r532', 'r542'),
     "                if kh_chot:", "                if False:"),
    # --- #568 r3 ---------------------------------------------------------
    # A13 — bo `r` khoi MOT docstring la du lam ban ca tep. r526 do TOAN TEP nen
    # mot neo la du: them neo thu hai cho docstring kia se la BO TUONG DUONG
    # (cung giet dung r526, khong phan biet duoc bang dau vao).
    ("chan-doan-bo-raw-o-docstring-khoi-chan-doan", ("r526",),
     '    r\"\"\"Trich NGUYEN chan doan cua con cho tung ca mang `nhan` (DO_KHAC / DO_CHOT).',
     '    \"\"\"Trich NGUYEN chan doan cua con cho tung ca mang `nhan` (DO_KHAC / DO_CHOT).'),
    # A14 — cho r526 do mot HANG SACH thay vi tep dang chay. Khong co chot
    # "`ma` LA tep nay" thi dot bien nay SONG SOT va r526 thanh mot ca xanh ve
    # mot thu no khong he do.
    ("chan-doan-r526-doc-hang-sach-thay-vi-tep-that", ("r526",),
     '    ma = nguon.read_text(encoding="utf-8")',
     '    ma = "x = 1" + chr(10)'),
    # A15 — noi TRAN ma khong doi huong cat: nguyen nhan o CUOI stderr bong toi
    # duoc dong cha, tuc loi khai "bi cat" cua o `suy-bien-dai` thanh SAI.
    ("chan-doan-noi-tran-ma-khong-doi-huong-cat", ('r525', 'r536'),
     "TRAN_CHAN_DOAN = 400", "TRAN_CHAN_DOAN = 100000"),
    # --- #568 r5 ------------------------------------------------------------
    ("chan-doan-quay-ve-lstrip-tap-ky-tu", ("r537",),
     '    return re.sub(r"^ ?[\\u2014-] ?", "", than, count=1)',
     '    return than.lstrip(" \\u2014-").strip()'),
    # #568 r5 luot 3 — o day TUNG co `chan-doan-go-nhieu-hon-mot-dau-phan-cach`
    # (bo `count=1`). Da BO vi no la DOT BIEN TUONG DUONG, va luot day du chung
    # minh: no SONG SOT voi `child rc=0`. Ly do: mau neo `^` (khong `re.M`) chi
    # khop duoc o vi tri 0, nen `re.sub` VON da thay toi da mot lan — `count=1`
    # khong them rang buoc nao. Giu `count=1` trong ma la de NOI RO y dinh, va
    # cho nay ghi lai rang no KHONG phai mot rang buoc do duoc.
    # Hai loi khai TACH ROI thi phai co HAI dot bien — mot hang gop hai loi khai
    # chi can MOT dot bien, va do chinh la cho mot ve sai nup duoc sau ve kia.
    ("chan-doan-lat-khai-bo-dong-trang", ("r537",),
     "THAN_BO_DONG_TRANG_KHONG_DEM = True",
     "THAN_BO_DONG_TRANG_KHONG_DEM = False"),
    ("chan-doan-lat-khai-bo-khoang-trang-tung-dong", ("r537",),
     "THAN_BO_KHOANG_TRANG_TUNG_DONG = False",
     "THAN_BO_KHOANG_TRANG_TUNG_DONG = True"),
    # Ve HAI phai do duoc bang HANH VI, khong chi bang hang so: neu bo dong goi
    # THAT SU bo khoang trang tung dong thi o (5) cua r537 phai DO.
    ("chan-doan-bo-khoang-trang-tung-dong-that", ("r537",),
     '    than = than.replace("\\n", " | ")',
     '    than = " | ".join(x.strip() for x in than.split("\\n"))'),
    # #568 r5 luot 3 — CA CUM dot bien cua dong `ranh` dung chung MOT neo, va neo
    # ay duoc sinh TU CHINH DONG THAT (script, khong go tay), vi luot 3 do duoc:
    # doi dong that ma quen bang thi CA NAM muc dem ra 0 va CHET LANG.
    # `dich` o day de tam ('r531'); luot day du se nang dung theo phep do.
    ("chan-doan-nuot-ca-ranh-gioi", ("r524", "r531", "r533", "r534", "r535", "r536", "r537", "r538"),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?!)")'),
    ("chan-doan-tra-ranh-gioi-ve-ban-rong", ('r531', 'r533', 'r535', 'r538', 'r542'),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM|DOT BIEN|MUTANT|LOI:)")'),
    ("chan-doan-ranh-gioi-noi-long-ve-tien-to-tran", ("r531", "r533", "r535", "r538"),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: |DOT BIEN |MUTANT: giet = \\d+ |MUTANT \\S+ \\| |CASE T\\d+: |\\d+/\\d+$|LOI: )")'),
    ("chan-doan-noi-long-ho-tu-kiem", ("r535", "r538"),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: |TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-noi-long-ho-mutant", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = \\d+ |MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    # luot 5 — `CASE T<n>: DO - ` la hinh cua FIXTURE `_KICH_CON`, khong phai cua
    # runner (`chay_ca` phat `DAT` / `DO — `). Chinh loi khai o 31127d7.
    ("chan-doan-ho-case-t-lay-hinh-fixture-thay-hinh-runner", ("r535", "r538"),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: DO - |(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-bo-bien-phai-cua-nhan", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT|DO_KHAC)|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-noi-long-duoi-ban-ghi-dot-bien", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| | [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    # luot 5 (cross-review tren 31127d7) — bon cho lech giua NGU PHAP va DIEM PHAT
    # THAT, moi cho mot dot bien. Ca r538 giu bang doi chieu tung diem phat.
    ("chan-doan-doi-khoang-trang-truoc-tong-ket-dot-bien", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$| : KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-quen-ho-mutant-tung-muc", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-quen-dong-tong-ket-nhom", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-quen-dong-ti-so-va-loi", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — ))")'),
    # luot 6 (cross-review tren 273de20) — NAM duoi van la TIEN TO du luot 5 khai
    # "du hinh": `TIN DUNG GIA: `, `0 — ca do THUC TE: `, hai duoi MUTANT that bai,
    # `LOI: ... THIEU ...: `. Diem phat that LUON co phan sau (hai cau co dinh /
    # danh sach ca hoac `(rong)` / `ly_do` khong rong / repr danh sach). Va ho TU
    # KIEM: `DO_CHOT(?: |$)` rong hon hinh that `DO_CHOT — ` / `DO_KHAC — <Kieu>: `.
    ("chan-doan-noi-long-duoi-tin-dung-gia", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: |0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-noi-long-duoi-ca-do-thuc-te", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: )| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-noi-long-duoi-mutant-that-bai", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau \\d+ lan\\): |0/\\d+: )|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-noi-long-duoi-loi-thieu-nhom", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): ))")'),
    ("chan-doan-bo-dau-phan-cach-cua-nhan", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT(?: |$)|DO_KHAC(?: |$))|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    # luot 7 (cross-review tren e7f15cb) — bon nhom lech giua ngu phap va MIEN GIA
    # TRI ma ma bao dam: L `ly_do` (chi kiem khong rong), D cot dich (`[^|]*`),
    # S so (`\d` nhan chu so Unicode, so dem `01`, `-0`, va `rc=1` o nhanh `!= 1`),
    # K ten ngoai le (`[A-Za-z_]\w*` bac `Échec`, `Bad-Error`, ten rong). Moi nhom
    # mot dot bien; ti so `n/n` doi HAI SO BANG NHAU bang tham chieu nguoc.
    ("chan-doan-ly-do-chi-kiem-khong-rong", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): .+$|0/[1-9][0-9]*: .+$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-cot-dich-nhan-moi-thu", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| [^|]* \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| [^|]* \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-so-nhan-chu-so-unicode-va-dem", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: \\d+/\\d+$|TU KIEM co dot bien rieng: \\d+/\\d+ nhom bat buoc · dot bien giet \\d+/\\d+$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>\\d+)/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = \\d+ · khong giet = \\d+ · khong do duoc = \\d+ / tong \\d+$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|\\d+/\\d+$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-rc-con-nhan-1-va-am-0", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=-?\\d+ != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-ti-so-hai-so-khong-can-bang", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:[1-9][0-9]*/[1-9][0-9]*$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    ("chan-doan-ten-ngoai-le-chi-ascii", ("r538",),
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")',
     '    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — [A-Za-z_]\\w*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \\| (?:r[0-9]+(?:,r[0-9]+)*)? \\| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \\[\'r\\d+\'(?:, \'r\\d+\')*\\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\\d+(?:,r\\d+)*|\\(rong\\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \\((?:0|[2-9]|[1-9][0-9]+)\\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \\| (?:T[0-9]+(?:,T[0-9]+)*)? \\| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \\(sau [12] lan\\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\\ ghi\\ TRUNG\\ cho\\ ca\\ .*|ban\\ ghi\\ dong\\ luot\\ thieu\\ rc\\ kieu\\ int|ban\\ ghi\\ khong\\ neo\\ dung\\ luot:\\ .*|ban\\ ghi\\ khong\\ phai\\ JSON|ban\\ ghi\\ khong\\ phai\\ object:\\ .*|ban\\ ghi\\ thieu\\ ten\\ ca|ban\\ ghi\\ vua\\ mang\\ ten\\ ca\\ vua\\ khai\\ dong\\ luot|bo\\ doc\\ kenh\\ nem\\ .*:\\ .*|ca\\ do\\ vi\\ ngoai\\ le\\ KHONG\\ phai\\ TinHieuChotCa:\\ .*\\ \\|\\ .*|chi\\ tiet\\ khong\\ phai\\ chuoi\\ cho\\ ca\\ .*|co\\ ban\\ ghi\\ SAU\\ ban\\ ghi\\ dong\\ luot|dau\\ dong\\ luot\\ khong\\ phai\\ bool\\ true:\\ .*|dich\\ RONG:\\ khong\\ cap\\ GIET\\ khi\\ khong\\ ca\\ nao\\ phai\\ chet|dich\\ co\\ ten\\ ca\\ KHONG\\ ton\\ tai:\\ .*|kenh\\ khong\\ ton\\ tai|khong\\ doc\\ duoc\\ kenh:\\ .*:\\ .*|nhan\\ khong\\ hop\\ le\\ cho\\ ca\\ .*:\\ .*|rc\\ dong\\ luot\\ .*\\ !=\\ rc\\ tien\\ trinh\\ .*|ten\\ ca\\ khong\\ phai\\ chuoi:\\ .*|thieu\\ ban\\ ghi\\ dong\\ luot|thieu\\ ca\\ .*\\ /\\ ca\\ la\\ .*) \\| rc_con=(?:0|-?[1-9][0-9]*) \\| stderr\\[-200:\\]=.*)$|0/[1-9][0-9]*: tap ca do chot \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\] != dich \\[(?:\'T[0-9]+\'(?:, \'T[0-9]+\')*)?\\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \\(chua chay hoac chua co dot bien\\): \\[\'r[0-9]+\'(?:, \'r[0-9]+\')*\\]$))")'),
    # luot 6 — lat LOI KHAI bat doi xung dau/ranh ma khong doi hanh vi: r538 do hai chieu.
    ("chan-doan-lat-loi-khai-dau-rong-hon-ranh", ("r538",),
     "DAU_RONG_HON_RANH_THEO_HOP_DONG_TEN_CA = True",
     "DAU_RONG_HON_RANH_THEO_HOP_DONG_TEN_CA = False"),
    # #568 r5 (cross-review P2 tren be5c3f2) — HOI QUY ve dung ban truoc khi va:
    # `DOT BIEN ` la tien to TRAN. Dot bien nay tai lap CHINH phep do cua reviewer,
    # nen no la neo GIU cho ban va khoi bi go lai ma khong ai thay.
    # Lat LOI KHAI ma khong doi hanh vi — chieu thu hai cua o (4) r533.
    ("chan-doan-lat-khai-dong-ranh-gioi-khong-dem", ("r533",),
     "DONG_RANH_GIOI_DUNG_HINH_KHONG_DUOC_DEM = True",
     "DONG_RANH_GIOI_DUNG_HINH_KHONG_DUOC_DEM = False"),
    # Doi HANH VI ma khong doi loi khai: dem ca dong ranh gioi. Dau vao BINH
    # THUONG cung sinh nhan, nen o (4) cua r533 va o (1) cua r531 deu DO.
    ("chan-doan-dem-ca-dong-ranh-gioi", ("r531", "r533", "r534", "r535", "r536", "r537", "r538"),
     "            dang_mo = False\n", "            dang_mo = False\n            bo_qua += 1\n"),
    # Bo phep giu nhan BO QUA ngoai tran: than dai lam nhan bi cat, mat so dong.
    ("chan-doan-de-tran-nuot-nhan-bo-qua", ("r531", "r533", "r534", "r536"),
     '    duoi = f" \u2026[CHA BO {so_bo} dong]" if so_bo else ""',
     '    duoi = ""'),
    # Bo han phep tach nhan: y het tren nhung o mot cho khac, phan biet duoc bang
    # dau vao o (2) cua r534 (than NGAN + co dong bi bo).
    # #568 r5 luot 2 — o day TUNG co muc `chan-doan-bo-sieu-du-lieu-so-dong-bo`
    # (`_so_dong_bo` tra 0). Da BO: `_so_dong_bo` chi co MOT cho goi, nen no va
    # `chan-doan-de-tran-nuot-nhan-bo-qua` (`duoi = ""`) cho dung mot hanh vi tren
    # MOI dau vao — do duoc, ca hai cung tap ca do va cung dau ra. Do la BO TUONG
    # DUONG: giu ca hai la tu bao minh do hai thu trong khi chi do MOT.
    # #568 r5 luot 2 — DUNG duong gia mao ma cross-review do duoc: doc so dong bo
    # NGUOC ra tu VAN BAN than. Con in dung chuoi la cha khai so khong phai cua no.
    ("chan-doan-doc-so-dong-bo-tu-van-ban", ("r531", "r533", "r534", "r536"),
     '    return getattr(than, "bo_qua", 0)',
     '    return int((re.search(r"\\[BO QUA (\\d+) dong\\]", str(than)) or ["", "0"])[1])'),
    # Vut SIEU DU LIEU luc dong goi: `bo_qua` luon 0, nen khong bao gio khai.
    ("chan-doan-vut-so-dong-bo-luc-dong-goi", ("r531", "r533", "r534", "r535", "r536", "r538"),
     "        o.bo_qua = bo_qua", "        o.bo_qua = 0"),
    # Noi long TUNG ho tien to — moi ho mot muc, phan biet duoc bang dau vao.
    # #568 r5 — luot day du (99 dot bien) bao rc=1 voi SAU muc lech `dich`:
    # chan-doan-chi-lay-ten-ca, chan-doan-dung-o-dong-dau,
    # chan-doan-nuot-ca-ranh-gioi, chan-doan-cat-lang-khong-khai,
    # chan-doan-xoa-phan-biet-P1-P2, tu-dot-bien-nhan-moi-tap-ca.
    # Nguyen nhan: r531/r532 la ca MOI cua r5, va chung do THAT cac dot bien cu
    # ay; `dich` cu do do HEP hon phep do. Bo cham doi `do_chot == set(dich)`
    # BANG DUNG, nen khai thieu mot ten la HONG — dung nhu thiet ke.
    # Bai hoc ghi lai de khong lap: TU KIEM 32/32 KHONG thay duoc luot day du.
    # `dich` o sau muc tren duoc nang len TU PHEP DO, khong tu suy doan.
    # M13/A29 — tra ranh gioi ve ban RONG. O (2) cua r531 mat lai than.
    # M13/A29 — bo phep DEM: mat lai im lang o o (3).
    ("chan-doan-bo-dem-phan-bi-bo", ("r531", "r533", "r534", "r535", "r536", "r538"),
     "        elif dong.strip():", "        elif False:"),
    # M13/A30 — KHAI ca khi KHONG mat: dong rong cuoi chuoi cung duoc dem, nen
    # dau vao BINH THUONG sinh nhan. Day la dot bien canh chieu (1) — chieu ma
    # mot ca chi kiem "co mat thi co nhan" se BO SOT.
    ("chan-doan-khai-bo-qua-ca-khi-khong-mat", ("r531", "r533", "r534", "r535", "r536", "r538"),
     "        elif dong.strip():", "        else:"),
    # M14/A32 — lat LOI KHAI ma khong doi hanh vi.
    ("chan-doan-lat-loi-khai-stderr-sau-chot", ('r532',),
     "CHAN_DOAN_STDERR_KHI_DA_CO_CHOT = False",
     "CHAN_DOAN_STDERR_KHI_DA_CO_CHOT = True"),
    # M14/A32 — chieu NGUOC: doi HANH VI ma khong doi loi khai. Day moi la chieu
    # ma mot ca mot-chieu bo sot, va cung la chieu chung minh hang so KHONG phai
    # mot dieu cam: ai chua duong nay ma nho dat lai hang so thi ca xanh.
    ("chan-doan-in-them-stderr-khi-da-co-chot", ('r532',),
     '                        print(f"    CHOT {ca}: {_goi_chan_doan(than)}")',
     '                        print(f"    CHOT {ca}: {_goi_chan_doan(than)}")\n'
     '                        print(f"    stderr: {_goi_chan_doan(p.stderr)}")'),
    # --- #568 r4 ------------------------------------------------------------
    # M10/A20 — tra phep tach dong ve `splitlines()`, tuc mo lai duong CAP GIET
    # GIA ma cross-review codex tim ra.
    ("chan-doan-tach-dong-lai-nuot-dau-tach-unicode", ("r529",),
     "    for dong in stdout.split(chr(10)):",
     "    for dong in stdout.splitlines():"),
    # M10/A20 — bo MOT ky tu khoi danh sach. Khong co chot (1) cua r529 — von DAN
    # XUAT lai danh sach tu chinh `splitlines` luc chay — thi dot bien nay SONG
    # SOT: o (2) chi lap tren danh sach, nen danh sach ngan di thi no kiem it di
    # ma van xanh. Do dung hinh dang LOI-KHAI-RONG-HON-PHEP-DO.
    ("chan-doan-bo-mot-ky-tu-khoi-danh-sach-tach-dong", ("r529",),
     'KY_TU_TACH_DONG_LE = "\\r\\v\\f\\x1c\\x1d\\x1e\\x85\\u2028\\u2029"',
     'KY_TU_TACH_DONG_LE = "\\r\\v\\f\\x1c\\x1d\\x1e\\x85\\u2028"'),
    # M11/A22 — bo chuyen tiep o nhanh DO_KHAC.
    ("chan-doan-bo-chuyen-tiep-o-nhanh-do-khac", ('r530', 'r542'),
     '                    print(f"    VO CAN {ca}: {_goi_chan_doan(than)}")',
     "                    pass"),
    # M11/A23 — bo chuyen tiep o nhanh `rc != 1`. NEO PHAI HAI DONG: dong `print`
    # 16 dau cach la CHUOI CON cua dong 20 dau cach o nhanh P2, nen neo mot dong
    # dem ra HAI lan ngoai bang va phep doi neo duy nhat bac het. Da do.
    ("chan-doan-bo-chuyen-tiep-o-nhanh-rc-khac-1", ('r530',),
     '                # rong va stderr la cho DUY NHAT con chan doan.\n'
     '                print(f"    stderr: {_goi_chan_doan(p.stderr)}")',
     "                pass"),
    # M12/A24 — thay DUONG HAI bang mot hang sach. Duong MOT da co dot bien rieng
    # (`chan-doan-r526-doc-hang-sach-thay-vi-tep-that`); hai duong, hai dot bien.
    ("chan-doan-r526-doc-duong-hai-bang-hang-sach", ("r526",),
     "    ma_2 = _ins.getsource(sys.modules[__name__])",
     '    ma_2 = "x = 1" + chr(10)'),
    # --- #593 --------------------------------------------------------------
    # A1 — can tran ma LANG LE tra ve mot cap TRUNG thay vi khai KHONG DO DUOC.
    # Chi giet r527: duoi bo sinh THAT (khong gian 256) duong `raise` gan nhu
    # khong bao gio toi, nen r528 mu voi dot bien nay — do la ly do no la mot
    # dot bien RIENG chu khong gop.
    ("dau-phien-can-tran-ma-lang-le-tra-cap-trung", ("r527",),
     "    raise TinHieuKhongDoDuoc(", "    return dau, dau\n    raise TinHieuKhongDoDuoc("),
    # A9 — bo PHEP SO, tuc bo vong rut lai. Day la dot bien tai lap DUNG benh
    # goc: `_hai_dau_phien_phan_biet` tro lai thanh hai lan rut doc lap.
    ("dau-phien-bo-vong-rut-lai", ("r527", "r528"),
     "        if khac != dau:", "        if True:"),
    # A1 — ha tran xuong 0: chan tren khong con "tren" nua. r527 bat bang SO LAN
    # GOI (chot theo HANG SO 65, khong theo bien), r528 bat vi khong gian 256 ma
    # van can tran.
    # `dich` co r508: ha tran xuong 0 lam moi bo sinh thanh "suy bien" duoi mat
    # `_hai_dau_phien_phan_biet`, nen r508 cung chet — bang CHOT cua chinh no, sau
    # khi da sua duong thoat DO_KHAC. Khai du BA ten la khai CHAT HON.
    # CROSS-REVIEW CODEX P2 — dot bien noi lai BENH GOC o dong goi cua `r508`,
    # giu ham nguyen ven. Truoc khi co chot (c1) cua r528, dot bien nay SONG SOT
    # tron ven: ca hai ve do cua A9 chi cham vao HAM. Khoi try/except o lai nen
    # cu phap van dung; nhanh `except` chi khong bao gio chay nua.
    ("dau-phien-r508-khong-di-qua-bo-tien-de", ("r528",),
     "        ph_that, ph_khac = _hai_dau_phien_phan_biet()",
     "        ph_that, ph_khac = sinh_dau_phien(), sinh_dau_phien()"),
    ("dau-phien-ha-tran-xuong-khong", ("r508", "r527", "r528", "r543"),
     "TRAN_RUT_DAU_PHIEN = 64", "TRAN_RUT_DAU_PHIEN = 0"),
    ("bo-chuan-hoa-ban-sao", ("r523",),
     "    ban_sao = Path(ban_sao).resolve()",
     "    pass"),
    ("bo-vat-hoa-dich-o-chay-dot-bien", ("r521",),
     "            dich = tuple(dich)\n            ban_sao = root / ten",
     "            ban_sao = root / ten"),
    ("bo-vat-hoa-dich-o-chay-mot-mutant", ("r521",),
     "    dich = tuple(dich)\n    trang_thai = ly_do = None",
     "    trang_thai = ly_do = None"),
    # F06 — thu hep lai chi con OSError: hai loai kia lai thoat vong.
    ("hep-lai-loi-phong-chi-oserror", ("r522",),
     "        except (OSError, ValueError, UnicodeError) as exc:",
     "        except OSError as exc:"),
    # F05 — dem ke ca ban trung.
    ("dem-dich-ke-ca-trung", ("r519",),
     "            so_ca = len(dich_pb)",
     "            so_ca = len(dich)"),
    ("bo-xoa-co-chi-tu-kiem", ("r519",),
     '        env.pop("NHANH_DON_DUOC_CHI_TU_KIEM", None)',
     "        pass"),
    ("bo-tu-choi-dot-bien-noop", ("r519",),
     '            if thay == neo:',
     "            if False:"),
    # F02 (luot 10) — go nhanh bat loi PHONG: loi thoat ra, mat lan thu hai.
    ("bo-bat-loi-phong-con", ("r520", "r522", "r545"),
     "        except (OSError, ValueError, UnicodeError) as exc:",
     "        except _KhongBaoGioXayRa as exc:"),
    ("bo-vo-fail-close", ("r517", "r545"),
     "    except Exception as exc:                      # noqa: BLE001 — fail-close co chu y",
     "    except ZeroDivisionError as exc:"),
    ("bo-so-rc-tien-trinh", ("r515",),
     '    if rc_that is not None and dong["rc"] != rc_that:', "    if False:"),
    # F03 (luot 6) — bo phep so CHI o nhanh child-0: mot huong cua chieu neo.
    ("bo-so-rc-khi-child-khong", ("r515",),
     '    if rc_that is not None and dong["rc"] != rc_that:',
     '    if rc_that not in (None, 0) and dong["rc"] != rc_that:'),
    # ---- F02 (luot 3): lop NEM cua duong ha tang, khong phai hinh dang AST ----
    ("run-nem-tin-hieu-chot", ("r501",),
     '        raise AssertionError(f"rc={p.returncode}: {\' \'.join(args)}\\n{p.stdout}\\n{p.stderr}")',
     '        raise TinHieuChotCa(f"rc={p.returncode}: {\' \'.join(args)}\\n{p.stdout}\\n{p.stderr}")'),
    # Boc GIU NGUYEN so node Assert (AST khong thay gi) ma doi HAN lop nem.
    # F02 — lop TRUNG TEN "AssertionError" nhung la tin hieu chot: chi phep so
    # DANH TINH moi bac duoc, phep so TEN thi khong.
    ("nap-boc-lop-dong-ten", ("r502",),
     "    assert spec and spec.loader",
     '    _Gia = type("AssertionError", (TinHieuChotCa,), {})\n'
     "    try:\n        assert spec and spec.loader\n"
     "    except AssertionError as _e:\n        raise _Gia(str(_e))"),
    ("archive-boc-lop-dong-ten", ("r502",),
     "            assert archive.stdout is not None",
     '            _Gia = type("AssertionError", (TinHieuChotCa,), {})\n'
     "            try:\n                assert archive.stdout is not None\n"
     "            except AssertionError as _e:\n                raise _Gia(str(_e))"),
    ("nap-boc-lop-chot", ("r502",),
     "    assert spec and spec.loader",
     "    try:\n        assert spec and spec.loader\n"
     "    except AssertionError as _e:\n        raise TinHieuChotCa(str(_e))"),
    # Neo phai la DONG DAY DU (12 space). Ban dau viet 8 space: no van "khop"
    # nhu CHUOI CON cua dong that, de lai 4 space thua truoc `try:` =>
    # IndentationError, mutant chet luc BIEN DICH nen KHONG ca nao do va bo cham
    # bao `(rong)`. Mot mutant chet truoc khi chay thi khong do duoc gi.
    ("archive-boc-lop-chot", ("r502",),
     "            assert archive.stdout is not None",
     "            try:\n                assert archive.stdout is not None\n"
     "            except AssertionError as _e:\n                raise TinHieuChotCa(str(_e))"),
    # ---- F06: KHONG GIET phai la trang thai TERMINAL -------------------------
    # r509 do kem: no dem dau phien cua HAI luot phong, ma dieu kien dung sai lam
    # moi luot chay them mot lan.
    ("dung-chi-khi-giet", ("r505", "r509"),
     "        if trang_thai != KHONG_DO_DUOC:\n            return trang_thai, ly_do, lan_thu",
     "        if trang_thai == GIET:\n            return trang_thai, ly_do, lan_thu"),
    # F03 (luot 5) — CHUAN HOA lan HAI: mot KHONG GIET o lan 2 bi ghi cong GIET.
    ("chuan-hoa-lan-hai-thanh-giet", ("r505",),
     "        trang_thai, ly_do = doc_kenh(kenh, dau_phien, ten, lan_thu, dich, p.returncode)",
     "        trang_thai, ly_do = doc_kenh(kenh, dau_phien, ten, lan_thu, dich, p.returncode)\n"
     "        if lan_thu == 2 and trang_thai == KHONG_GIET:\n            trang_thai = GIET"),
    # F05 — chieu NGUOC lai: GIET khong con la terminal.
    ("dung-chi-khi-khong-giet", ("r505", "r520", "r522", "r523"),
     "        if trang_thai != KHONG_DO_DUOC:\n            return trang_thai, ly_do, lan_thu",
     "        if trang_thai == KHONG_GIET:\n            return trang_thai, ly_do, lan_thu"),
    # ---- F04: entropy phai phu thuoc MOI byte; dau phai moi moi LUOT PHONG ----
    ("entropy-giu-mot-byte", ("r509",),
     "    return secrets.token_hex(16)", "    return secrets.token_hex(16)[-2:] * 16"),
    # F06 — xoa BIT CAO cua 14 byte GIUA: vi sai chi o hai dau mut hoan toan mu
    # voi no, vi fixture cu toan byte < 128 nen chuoi khong doi.
    # F04 (luot 5) — GIU DUNG BIT CAO moi byte: phep lat rieng bit cao cho 16 dau
    # ra khac nhau nen mu hoan toan; phep lat TUNG BIT thi khong.
    # F02 (luot 6) — NEN mien dau ra xuong duoi 2**30: lat bit van phan biet het.
    ("entropy-nen-bang-modulo", ("r509",),
     "    return secrets.token_hex(16)",
     "    return str(int(secrets.token_hex(16), 16) % 1000000007)"),
    ("entropy-chi-giu-bit-cao", ("r509",),
     "    return secrets.token_hex(16)",
     "    _e = secrets.token_hex(16)\n"
     '    return "".join(format(int(_e[2 * i:2 * i + 2], 16) & 0x80, "02x")\n'
     "                   for i in range(16))"),
    # F04 — SAP XEP LAI byte: cung da so byte, khac thu tu. Phep lat bit mu voi no.
    ("entropy-sap-xep-byte", ("r509",),
     "    return secrets.token_hex(16)",
     "    _e = secrets.token_hex(16)\n"
     '    return "".join(sorted(_e[2 * i:2 * i + 2] for i in range(16)))'),
    ("entropy-bo-bit-cao-byte-giua", ("r509",),
     "    return secrets.token_hex(16)",
     "    _e = secrets.token_hex(16)\n"
     '    return _e[:2] + "".join(format(int(_e[2 * i:2 * i + 2], 16) & 0x7F, "02x")\n'
     "                            for i in range(1, 15)) + _e[30:]"),
    ("cache-dau-phien-theo-dinh-danh", ("r509",),
     "        dau_phien = sinh_dau_phien()          # M7: SINH MOI moi luot",
     "        _c = globals().setdefault(\"_cache_ph\", {})\n"
     "        dau_phien = _c.setdefault((ten, lan_thu), sinh_dau_phien())"),
    # ---- F05: bo cong dem MUTANT, khong dem LAN THU --------------------------
    ("cong-theo-so-lan", ("r514",),
     "                khong_do += 1", "                khong_do += so_lan"),
    # ---- F03: ve `tk_giet` cua cong nhom bat buoc ----------------------------
    # F03 — ve `tk_hong` cua cong nhom bat buoc, do RIENG.
    ("mo-cong-tu-dot-bien-hong", ('r513',),
     "    if thieu or len(NHOM_BAT_BUOC) < SAN_NHOM or tk_hong or tk_giet != len(DOT_BIEN_TU_KIEM):",
     "    if thieu or len(NHOM_BAT_BUOC) < SAN_NHOM or tk_giet != len(DOT_BIEN_TU_KIEM):"),
    ("mo-cong-tu-dot-bien-thieu-giet", ('r513',),
     "    if thieu or len(NHOM_BAT_BUOC) < SAN_NHOM or tk_hong or tk_giet != len(DOT_BIEN_TU_KIEM):",
     "    if thieu or len(NHOM_BAT_BUOC) < SAN_NHOM or tk_hong:"),
    # ---- F01: BA chot cua bo cham tu dot bien, moi chot mot dot bien RIENG ----
    # #568 r4 — `dich` len ("r516","r530"): `if do_khac:` -> `if False:` lam
    # nhanh DO_KHAC KHONG BAO GIO chay, nen dong chuyen tiep cua no bien mat va
    # `r530` do. Khai du hai ten la khai CHAT HON.
    ("tu-dot-bien-bo-loc-loi-vo-can", ('r516', 'r530', 'r542'),
     "            if do_khac:", "            if False:"),
    # F01 — "chuan hoa" dau vao TRON: giu bo loc nhung xoa do_khac khi CO do_chot.
    # #568 — NEO DOI theo ban va (khoi trich chan doan thay cho mot re.findall).
    # Y NGHIA cua dot bien GIU NGUYEN: chuan hoa lan lon de giau DO_KHAC khi co
    # DO_CHOT, tuc mot duong cap TIN DUNG GIA. r516 van la ca dich.
    ("tu-dot-bien-chuan-hoa-hon-hop", ('r516',),
     "            do_khac = {ca for ca, _ in kh_khac}",
     "            do_khac = {ca for ca, _ in kh_khac}\n"
     "            if do_chot:\n                do_khac = set()"),
    ("tu-dot-bien-bo-so-rc-con", ('r516',),
     "            elif p.returncode != 1:", "            elif False:"),
    # r2/M6 — r525 cung lai CHINH `chay_dot_bien_tu_kiem`, nen hai dot bien vao
    # vi tu cap GIET giet CA no. Ghi du `dich` la ghi SU THAT da do, va no lam
    # dot bien CHAT HON: runner doi `do_chot == set(dich)` BANG NHAU, nen muc nay
    # gio phai giet ca hai ca moi duoc cong.
    ("tu-dot-bien-nhan-moi-tap-ca", ('r516', 'r525', 'r532', 'r539', 'r542'),
     "            elif bang_chung and do_chot == set(dich):", "            elif True:"),
    # F01 (luot 5) — TAP DO RONG duoc chuan hoa thanh dich: con chet ma KHONG in
    # chot nao van duoc ghi cong GIET.
    # F01 (luot 6) — QUAN HE TAP: bao ham, va giao khac rong.
    ("tu-dot-bien-nhan-bao-ham", ('r516', 'r539'),
     "            elif bang_chung and do_chot == set(dich):", "            elif set(dich) <= do_chot:"),
    ("tu-dot-bien-nhan-giao-khac-rong", ('r516', 'r539'),
     "            elif bang_chung and do_chot == set(dich):", "            elif do_chot & set(dich):"),
    ("tu-dot-bien-nhan-tap-rong-lam-dich", ('r516', 'r525', 'r539'),
     "            elif bang_chung and do_chot == set(dich):",
     "            elif do_chot == set(dich) or not do_chot:"),
    # F01 (luot 5) — rc NGOAI {0,1} duoc chuan hoa thanh 1: con in dung chot roi
    # chet vi mot ly do KHAC van duoc ghi cong GIET.
    ("tu-dot-bien-chuan-hoa-rc-khac", ('r516',),
     "            elif p.returncode != 1:", "            elif p.returncode == 0:"),
    # Runner tu kiem KHONG duoc gop hai lop lam mot — gop thi moi loi vo can
    # deu doi lot thanh chot cua ca.
    ("tu-kiem-gop-hai-lop-ngoai-le", ('r516', 'r545'),
     '                print(f"TU KIEM {ten}: DO_KHAC — {type(exc).__name__}: {exc}")',
     '                print(f"TU KIEM {ten}: DO_CHOT — {type(exc).__name__}: {exc}")'),
    ("tu-kiem-bo-ghi-nhan-loi-vo-can", ('r516', 'r542'),
     '            except Exception as exc:\n                do.append(ten)\n'
     '                print(f"TU KIEM {ten}: DO_KHAC',
     '            except Exception as exc:\n'
     '                print(f"TU KIEM {ten}: DO_KHAC'),
    # #593 r1 — TIEN-DE-HA-TANG-KHONG-DUOC-THANH-CHOT. Bay muc canh `_chay_r508_tach_nguon_do`
    # (r543) va ba muc canh `_khai_cat_dau_stderr` + duong that (r544). Tung cap phan
    # biet duoc bang DAU VAO (ghi o docstring r543/r544), khong cap nao la bo tuong duong.
    # `dich` DO tu luot day du, khong chep tay.
    ("r528-ha-tang-dem-vao-do", ("r543", "r545"),
     "        except m.TinHieuChotCa:\n            do += 1\n        except OSError as loi_ha_tang:",
     "        except (m.TinHieuChotCa, OSError):\n            do += 1\n        except _KhongBaoGioXayRa as loi_ha_tang:"),
    ("r528-ha-tang-bat-rong", ("r543",),
     "        except OSError as loi_ha_tang:", "        except Exception as loi_ha_tang:"),
    ("r528-ha-tang-bo-dem-chot-long", ("r543",),
     "        except m.TinHieuChotCa:\n            do += 1", "        except m.TinHieuChotCa:\n            pass"),
    ("r528-ha-tang-khong-ra-trang-thai-thu-ba", ("r543",),
     "    if ha_tang:\n        chi_tiet", "    if False:\n        chi_tiet"),
    ("r528-ha-tang-mat-so-lan", ("r543",), "            ghi[1] += 1", "            ghi[1] = 1"),
    ("r528-ha-tang-mat-thong-diep", ("r543",),
     'f"{loai}: {msg} ({n} lan)"', 'f"{loai} ({n} lan)"'),
    ("r528-ha-tang-gop-mot-loai", ("r543",),
     "ha_tang.setdefault(type(loi_ha_tang).__name__, [str(loi_ha_tang), 0])",
     'ha_tang.setdefault("OSError", [str(loi_ha_tang), 0])'),
    ("stderr-cat-khong-khai", ("r544",),
     '    return f" …[CAT {bo} ky tu dau]" if bo > 0 else ""', '    return ""'),
    ("stderr-khai-ca-khi-khong-cat", ("r544",),
     '    return f" …[CAT {bo} ky tu dau]" if bo > 0 else ""', '    return f" …[CAT {bo} ky tu dau]"'),
    ("stderr-duong-that-bo-khai", ("r544",),
     "                     + _khai_cat_dau_stderr(p.stderr))", '                     + "")'),
    # Vong 3 (cross-review v2): moi duong moi mot muc; dau vao phan biet ghi o r543 (B1, B2, B4).
    ("r508-nhan-moi-kdd", ("r543",), " and ly.startswith(\"ban ghi khong neo dung luot\")", ""),
    ("r528-ha-tang-mkdir-ngoai-try", ("r543",), "        try:\n            thu.mkdir(parents=True, exist_ok=True)",
     "        thu.mkdir(parents=True, exist_ok=True)\n        try:"),
    ("r528-ha-tang-chi-ba-loai-da-thu", ("r543", "r545"), "        except OSError as loi_ha_tang:",
     "        except (PermissionError, FileNotFoundError, OSError) as loi_ha_tang:\n"
     "            if type(loi_ha_tang) not in (OSError, PermissionError, FileNotFoundError):\n                raise"),
    ("stderr-duong-that-khai-ca-khi-ngan", ("r544",), "                     + _khai_cat_dau_stderr(p.stderr))",
     '                     + (_khai_cat_dau_stderr(p.stderr) or " …[CAT 0 ky tu dau]"))'),
    # #593 r2 — moi diem nuot, moi nhanh doi nhan cua runner: MOT muc, phan biet bang DAU VAO.
    ("ghi-so-doc-kenh", ("r545",), "        _ghi_ha_tang(exc)                         # r2 M1 diem nuot: doc_kenh\n", ""),
    ("ghi-so-doc-kenh-xac-thuc", ("r545", "r546"),
     "        _ghi_ha_tang(exc)                         # r2 M1 diem nuot: _doc_kenh_xac_thuc\n", ""),
    ("ghi-so-chay-ca", ("r545",), "            _ghi_ha_tang(exc)                     # r2 M1 diem nuot: chay_ca\n", ""),
    ("ghi-so-phong-mutant", ("r545",),
     "            _ghi_ha_tang(exc)                     # r2 M1 diem nuot: chay_mot_mutant\n", ""),
    ("ghi-so-helper-r528", ("r545",),
     "            _ghi_ha_tang(loi_ha_tang)             # r2 M1 diem nuot: _chay_r508_tach_nguon_do\n", ""),
    ("ghi-so-bang-chung", ("r546",), "                    _ghi_ha_tang(sys.exc_info()[1])\n", "                    pass\n"),
    ("runner-bo-doi-nhan-dat", ("r545", "r546"),
     "                _ha_tang_cua_ca(truoc)\n                print(f\"TU KIEM {ten}: DAT\")",
     "                print(f\"TU KIEM {ten}: DAT\")"),
    ("runner-bo-doi-nhan-chot", ("r545", "r546"), "                    _ha_tang_cua_ca(truoc, goc)\n", ""),
    ("runner-bo-duyet-chuoi", ("r545",), "        e = e.__cause__ or e.__context__", "        e = None"),
    ("runner-khong-theo-vi-tri", ("r545", "r546", "r547"), "_SO_HA_TANG.loi[truoc:] if _la", "_SO_HA_TANG.loi if _la"),
    ("tom-tat-mat-so-lan", ("r545",), "[str(e), 0])[1] += 1", "[str(e), 0])[1] = 1"),
    ("tom-tat-mat-thong-diep", ("r545", "r547"), 'f"{ten}: {tho} ({so} lan)"', 'f"{ten} ({so} lan)"'),
    # #593 r2 vong 4 (cross-review F1+F2): moi quyen ghi/don/mien tru mot muc; dich do tu luot day du.
    ("ghi-so-bo-duyet-chuoi", ("r545",), "    for e in _chuoi_that(exc):", "    for e in [exc][:_la_ha_tang_that(exc)]:"),
    ("ghi-so-kho-bare-liet-ke", ("r545",), "        _ghi_ha_tang(exc)                    # r2 vong 4: loi bi doi", "        pass  #"),
    ("runner-bo-doi-nhan-loi-khac", ("r546",), "                    _ha_tang_cua_ca(truoc, goc)   # loi khac", "                    pass  #"),
    ("r545-nuot-moi-oserror", ("r545",), "                    if not any(loi is x for x in cua_ca):\n                        raise", "                    pass"),
    ("r545-don-het-so", ("r545",), "   # don r545", "; so.loi.clear()"),
    ("r546-don-het-so", ("r546",), "   # don r546", "; so.loi.clear()"),
    # vong 5 (F1 khu trung, F2 hai lop): dich do tu luot day du.
    ("khu-trung-toan-so", ("r545",), "        if truoc is None or not any(e is x for x in _SO_HA_TANG.loi[truoc:]):",
     "        if not any(e is x for x in _SO_HA_TANG.loi):"),
    ("khu-trung-bo-cua-so", ("r545",), "        if truoc is None or not any(e is x for x in _SO_HA_TANG.loi[truoc:]):", "        if True:"),
    ("runner-bo-loc-luc-doc", ("r547",), " if _la_ha_tang_that(e)]   # loc", " if True]   # loc"),
    ("bo-cua-khong-lam-gi", ("r547",), "if not any(e is x for x in ds)]", "if True]"),
    ("bo-cua-xoa-het", ("r545", "r546", "r547"), "if not any(e is x for x in ds)]", "if False]"),
    ("bo-cua-theo-thong-diep", ("r545", "r546", "r547"), "if not any(e is x for x in ds)]", "if not any(str(e) == str(x) for x in ds)]"),
    ("vang-khong-bat", ("r547",), "            cua.append(_tiem(e))\n", ""),
    ("vang-khong-dang-ky", ("r547",), "            cua.append(_tiem(e))\n", "            cua.append(e)\n"),
    ("vang-khong-don", ("r547",), "run_goc, doc\n        _bo_cua(cua)", "run_goc, doc"),
    ("bo-mien-tru-vang-tep", ("r547",), "if not isinstance(sys.exc_info()[1], FileNotFoundError):", "if True:"),
    ("loc-luc-doc-theo-thong-diep", ("r547",), " if _la_ha_tang_that(e)]   # loc",
     " if not any(str(e) == str(t) for t in _SO_HA_TANG.tiem)]   # loc"),
    ("r545-nuot-theo-loai", ("r545",), "if not any(loi is x for x in cua_ca):", "if not any(type(loi) is type(x) for x in cua_ca):"),
    ("vang-moi-tep", ("r547",), "            if self in proof:\n                cua.append(", "            if True:\n                cua.append("),
    ("r547-thu-moi-tep", ("r547",), "            if self in proof:\n                vang.append(e)", "            if True:\n                vang.append(e)"),
    ("loc-dang-ky-theo-thong-diep", ("r547",), "not any(exc is t for t in _SO_HA_TANG.tiem)", "not any(str(exc) == str(t) for t in _SO_HA_TANG.tiem)"),
    ("bo-loc-dang-ky", ("r545", "r547"), " and not any(exc is t for t in _SO_HA_TANG.tiem)", ""),
    ("git-bao-tri-bo-nap", ("r548",), "\n_tat_bao_tri_git(os.environ)\n", "\n"),
    ("git-bao-tri-ghi-de", ("r548",), 'n = int(env.get("GIT_CONFIG_COUNT") or 0)', "n = 0"),
    ("git-bao-tri-noi-trung", ("r548",), "        if cuoi.get(k.lower()) != v:\n            env", "        if True:\n            env"),
    ("git-bao-tri-bo-tham-so", ("r548",), '        env["GIT_CONFIG_PARAMETERS"] = f"{tham} {duoi}"', "        pass"),
    ("git-bao-tri-bo-kho-bare", ("r548",), "    _tat_bao_tri_kho_bare(remote)\n", ""),
    ("git-bao-tri-gia-tri-dau", ("r548",), 'cuoi[(env.get(f"GIT_CONFIG_KEY_{i}") or "").lower()] = env.get(f"GIT_CONFIG_VALUE_{i}")',
     'cuoi.setdefault((env.get(f"GIT_CONFIG_KEY_{i}") or "").lower(), env.get(f"GIT_CONFIG_VALUE_{i}"))'),
    ("git-bao-tri-thieu-khoa", ("r548",), ',\n                   ("maintenance.autoDetach", "false"), ("receive.autogc", "false"))',
     ',\n                   ("maintenance.autoDetach", "false"))'),
    # #661 M3 — moi chot cua che do MANH/GOP: go chot ay => ca cua no DO.
    ("manh-regex-long", ("r549",), 're.fullmatch(r"[0-9]/[2-8]", gia_tri', 're.fullmatch(r"[0-9]+/[0-9]+", gia_tri'),
    ("manh-fullmatch-thanh-match", ("r549",), 'not re.fullmatch(r"[0-9]/[2-8]"', 'not re.match(r"[0-9]/[2-8]"'),
    ("manh-bo-k-nho-hon-n", ("r549",), "    if k >= n:\n", "    if False:\n"),
    ("manh-bo-doi-ra", ("r549",), "            if not ra:\n", "            if False:\n"),
    ("phan-hoach-lech-du", ("r550", "r552"), "if i % n == k]", "if i % n <= k]"),
    ("phan-hoach-bo-kiem-trung", ("r550",), "    if len(set(ten)) != len(ten):\n", "    if False:\n"),
    ("manh-chay-truoc-xac-thuc", ("r549", "r550"), "        gia_tri, ra = os.environ.pop(", "        chay_ca(None)\n        gia_tri, ra = os.environ.pop("),
    ("manh-bo-tu-kiem", ("r551",), "    tu_kiem_do = chay_tu_kiem()\n    tk_giet, tk_hong, tk_khong_do = chay_dot_bien_tu_kiem(dbtk)", "    tu_kiem_do = []\n    tk_giet, tk_hong, tk_khong_do = chay_dot_bien_tu_kiem(dbtk)"),
    ("manh-bo-pop-env", ("r551",), "os.environ.pop(MANH_ENV, None), os.environ.pop(MANH_RA_ENV, None)", "os.environ.get(MANH_ENV), os.environ.get(MANH_RA_ENV)"),
    ("manh-vong-tron-bang", ("r551", "r552"), "= chay_dot_bien(db)", "= chay_dot_bien()"),
    ("manh-tu-kiem-tron-bang", ("r551", "r552"), "= chay_dot_bien_tu_kiem(dbtk)", "= chay_dot_bien_tu_kiem()"),
    ("manh-bo-chay-ca", ("r551",), "    if chay_ca(None):\n", "    if False:\n"),
    ("manh-bo-tu-kiem-do", ("r551",), "    if tu_kiem_do or (dat, khong_giet", "    if (dat, khong_giet"),
    ("manh-bo-so-hang-khong-do", ("r551",), "khong_do, tk_giet, tk_hong, tk_khong_do) != (len(db), 0, 0, len(dbtk), 0, 0)", "tk_giet, tk_hong) != (len(db), 0, len(dbtk), 0)"),
    ("manh-in-dong-day-du", ("r551",), '    print(f"MANH {k}/{n}: MUTANT giet = ',
     '    print(f"MUTANT: giet = {dat} · khong giet = 0 · khong do duoc = 0 / tong {dat}")\n    print(f"MANH {k}/{n}: MUTANT giet = '),
    ("manh-bam-sai-tep", ("r551", "r552"), '"sha256_test": _bam(__file__)', '"sha256_test": _bam(TOOL)'),
    ("dot-bien-bo-tham-so-muc", ("r551",), "in (DOT_BIEN if muc is None else muc):", "in DOT_BIEN:"),
    ("tu-dot-bien-bo-tham-so-muc", ("r551",), "in (DOT_BIEN_TU_KIEM if muc is None else muc):", "in DOT_BIEN_TU_KIEM:"),
    ("gop-bo-qua-json-hong", ("r552",), '            return [f"{tep.name}: JSON hong ({e})"], None', "            continue"),
    ("gop-bo-kiem-khoa", ("r552",), " or set(x) != _KHOA_MANH for x in doc)", " for x in doc)"),
    ("gop-bo-kiem-phien-ban", ("r552",), '    if any(x["phien_ban"] != PHIEN_BAN_MANH for x in doc):', "    if False:"),
    ("gop-bo-kiem-so-manh", ("r552",), ' or any(x["so_manh"] != n for x in doc):', ":"),
    ("gop-bo-kiem-khoang-n", ("r552",), "    if not 2 <= n <= 8 or any(", "    if any("),
    ("gop-bo-kieu-int-manh", ("r552",), 'for k in ("phien_ban", "so_manh", "manh")):', 'for k in ("phien_ban", "so_manh")):'),
    ("gop-bo-kieu-int-so-manh", ("r552",), 'for k in ("phien_ban", "so_manh", "manh")):', 'for k in ("phien_ban", "manh")):'),
    ("gop-bo-kieu-int-phien-ban", ("r552",), 'for k in ("phien_ban", "so_manh", "manh")):', 'for k in ("so_manh", "manh")):'),
    ("gop-bo-kieu-mang", ("r552",), '    if any(type(x[k]) is not list for x in doc for k in ("giet", "tk_giet")):', "    if False:"),
    ("gop-bo-kiem-tap-manh", ("r552",), '    if sorted(x["manh"] for x in doc) != list(range(n)):', "    if False:"),
    ("gop-bo-kiem-bam", ("r552",), '    if any([x["sha256_test"], x["sha256_tool"]] != bam for x in doc):', "    if False:"),
    ("gop-bo-bam-tool", ("r552",), '[x["sha256_test"], x["sha256_tool"]] != bam', '[x["sha256_test"], bam[1]] != bam'),
    ("gop-bo-kiem-thanh-vien", ("r552",), "            if any(ten not in thuoc for ten in x[khoa]):", "            if False:"),
    ("gop-bo-kiem-hop", ("r552",), "        if set(hop) != {y[0] for y in bang}:", "        if False:"),
    ("gop-bo-kiem-lap", ("r552",), "        if len(hop) != len(set(hop)):", "        if False:"),
    ("gop-chi-mot-bang", ("r552",), 'in (("giet", DOT_BIEN), ("tk_giet", DOT_BIEN_TU_KIEM)):', 'in (("tk_giet", DOT_BIEN_TU_KIEM),):'),
    ("gop-bo-kiem-nhom", ("r552",), "    thieu = (NHOM_BAT_BUOC - nhom) | (NHOM_BAT_BUOC - {t for t, _, _ in TU_KIEM})", "    thieu = set()"),
    ("gop-bo-kiem-san", ("r552",), "    if thieu or len(NHOM_BAT_BUOC) < SAN_NHOM:\n", "    if thieu:\n"),
    ("gop-rc-0-khi-loi", ("r552",), "    if loi:\n        return 1\n    g, tk", "    if False:\n        return 1\n    g, tk"),
    ("ghi-so-gop", ("r546",), "            _ghi_ha_tang(e)                       # r2 M1 diem nuot: _loi_gop\n", ""),
    ("gop-cli-bo-qua", ("r552",), '    if sys.argv[1:2] == ["--gop"]:', "    if False:"),
    ("ram-pmc-thieu-truong", ("r553",), "for i in range(7)]   # WP748 r20 (r553)", "for i in range(6)]   # WP748 r20 (r553)"),
    ("moc-nhan-sai-dinh-dang", ("r554",), "        return None  # WP748 r22 F01 sai dinh dang",
     "        return datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)"),
    ("moc-bo-kiem-dao-nguoc", ("r554",), "        if moc and moc[1] < moc[0]:   # WP748 r22 F01 dao nguoc", "        if False:"),
    ("moc-bo-kiem-lech-giay", ("r554",), "and not khoang - LECH_MOC_GIAY <= x[\"giay\"] <= khoang + LECH_MOC_GIAY:   # WP748 r22 F01 lech",
     "and False:"),
    ("ghi-so-gop-dich", ("r546",), "            _ghi_ha_tang(e)                       # WP748 r22: diem nuot _loi_gop_dich (r546 qua r554)\n", ""),
    # r556 (c) do CHINH diem goi nay (don cay nem => van rc 124) nen cung phai chet: dich hai ca, moi nen.
    ("timeout-chi-giet-con", ("r555", "r556"), "                            duong = _ket_thuc_cay(q, ve, dau)   # WP748 r22 F02: diem goi don cay",
     "                            q.kill(); duong = \"chi con\""),
    # Khong `if False:` o day: bo han phep quet thi bien the mo-coi cua r555 cung chet tren POSIX (khong tren Windows,
    # noi job lo viec ay) => ban kinh phu thuoc nen. Dot bien chi lam sai DO CHINH XAC cua phep khop (r557 do).
    ("cay-dau-khop-tien-to", ("r557",), "        if can in moi_truong and truong is not None:",
     "        if any(x.startswith(can) for x in moi_truong) and truong is not None:"),
    ("giet-bo-kiem-danh-tinh", ("r557",), "            if not _con_song_posix(pid, khoa, goc_proc):   # WP748 r22 l2: kiem danh tinh pidfd",
     "            if False:"),
    ("windows-khong-job-van-chay", ("r556",), "        if ve is not None and not ve.dung_duoc():   # WP748 r22 l2 lo 2: khong job thi KHONG chay",
     "        if False:"),
    ("windows-gan-hong-van-chay", ("r556",), "                if ve is not None and not ve.gan_va_chay(q):",
     "                if ve is not None and not ve.gan_va_chay(q) and False:"),
    ("don-cay-nem-thay-124", ("r556",), "                        except Exception as e:                  # noqa: BLE001 — ghi vao `duong`, rc van 124",
     "                        except ZeroDivisionError as e:"),
]


# F08 — tap nhom BAT BUOC ghi CUNG, doc lap voi `TU_KIEM`. Neu suy tu
# `len(TU_KIEM)` thi mau so TU CO: bo mot ca khoi ca danh sach chay lan tap dich
# thi bo dem van bao du, du da mat A5c(1b).
NHOM_BAT_BUOC = frozenset({"r501", "r502", "r503", "r504", "r505", "r506",
                           "r507", "r508", "r509", "r510", "r511", "r512",
                           "r513", "r514", "r515", "r516", "r517", "r518",
                           "r519", "r520", "r521", "r522", "r523", "r524",
                           "r525", "r526", "r527", "r528", "r529", "r530",
                           "r531", "r532", "r533", "r534", "r535",
                           "r536", "r537", "r538"})
NHOM_BAT_BUOC = NHOM_BAT_BUOC | {"r539", "r540", "r541", "r542"}
NHOM_BAT_BUOC = NHOM_BAT_BUOC | {"r543", "r544"}      # #593 r1
NHOM_BAT_BUOC = NHOM_BAT_BUOC | {"r545", "r546", "r547"}      # #593 r2
NHOM_BAT_BUOC = NHOM_BAT_BUOC | {"r548"}      # #593 r3
NHOM_BAT_BUOC = NHOM_BAT_BUOC | {"r549", "r550", "r551", "r552"}      # #661
NHOM_BAT_BUOC = NHOM_BAT_BUOC | {"r553"}      # WP748 r20
NHOM_BAT_BUOC = NHOM_BAT_BUOC | {"r554", "r555"}      # WP748 r22
NHOM_BAT_BUOC = NHOM_BAT_BUOC | {"r556", "r557"}      # WP748 r22 l2

SAN_NHOM = 57                                 # WP748 r22 l2: san = tron tap bat buoc (them r556, r557)


# #568 r4 / B1 — `str.splitlines()` coi CHIN ky tu NGOAI `\n` la het dong, con
# bo doc cu (`re.findall(..., re.M)`) thi KHONG: `$` voi re.M chi khop truoc `\n`
# va o cuoi chuoi. Chenh lech ay cho MA SAN PHAM DOAT DUOC TEN CA — mot chuoi
# chua tung la dong ket qua thanh bang chung chot, tuc cap GIET GIA.
#
# Do duoc: stdout = "TU KIEM r501: DAT" + U+2028 + "TU KIEM r512: DO_CHOT" + LF
#          regex CU -> set()      parser dung splitlines -> {"r512"}
#
# Hang so nay KHONG duoc chep tay. `r529` DAN XUAT lai no tu chinh `splitlines`
# luc chay roi doi BANG NHAU — chep tay ma thieu mot ky tu thi chot van xanh
# trong khi van ho dung ky tu do.
KY_TU_TACH_DONG_LE = "\r\v\f\x1c\x1d\x1e\x85\u2028\u2029"

# #568 r5 / M14 — LOI KHAI, khong phai mot doi hoi.
#
# Khi con IN mot nhan `DO_CHOT` roi CHET TIEP vi mot le khac, le ay nam tren
# `stderr` va HIEN GIO bi vut: cha chi in dong `CHOT <ca>`. Hang so nay khai
# dung the, va `r532` doi hanh vi luc chay KHOP voi no.
#
# Vi sao la mot HANG SO chu khong phai mot chot cam: chot cam (`MOC not in th`
# cua `r525` cu) BAC TRUOC moi trien khai giu ca hai chan doan. Hang so thi
# khong: ai chua duong nay chi viec dat lai `True`, va `r532` xanh tro lai.
# Doi HANH VI ma khong doi LOI KHAI => `r532` DO. Doi LOI KHAI ma khong doi
# hanh vi => cung DO. Hai chieu, khong mot chieu.
#
# r5 KHONG hua chua duong ay: chua no doi dinh dang dau ra ma r516/r524/r530
# dang do, tuc mo rong pham vi. Xin revision rieng.
CHAN_DOAN_STDERR_KHI_DA_CO_CHOT = False

# #568 r5 / cross-review P2 tren be5c3f2 — phan CON LAI sau khi da siet `ranh`:
# mot dong THAN trung DUNG HINH mot ban ghi that (vd `TU KIEM r512: DAT`) VAN
# dong khoi — do la chot chong gia mao, giu nguyen — va chinh dong ay KHONG
# duoc dem vao `BO QUA`. Khong the phan biet no voi mot ban ghi that bang van
# ban, nen day la trang thai KHONG DO DUOC; ta KHAI no thay vi lam tron.
# Dem no se sinh nhan tren dau vao BINH THUONG (moi khoi deu ket o mot ban ghi),
# tuc lai khai RONG hon phep do — dung benh ma A30 cam.
DONG_RANH_GIOI_DUNG_HINH_KHONG_DUOC_DEM = True

# #568 r5 / cross-review luot 4 tren 8de4e66 — TACH hai ve. Ban truoc gop chung
# vao MOT hang `CHUAN_HOA_THAN_BO_DONG_TRANG_VA_KHOANG_TRANG`, va ve thu hai SAI:
# ma KHONG bo khoang trang tung dong. Do duoc: than ' a  ' + LF + '  b  ' ra
# 'a   |   b' — khoang trang BEN TRONG con nguyen. Mot hang gop hai loi khai thi
# mot ve sai van xanh nho ve kia dung; va `r537` cu chi do ve dong trang, nen bo
# rieng `.strip()` cua bo dong goi van DAT. Hai loi khai, hai chot, tung ve mot.
THAN_BO_DONG_TRANG_KHONG_DEM = True
# Chi bo o HAI DAU cua CA THAN (`_goi_chan_doan`), KHONG bo tung dong.
THAN_BO_KHOANG_TRANG_TUNG_DONG = False

# #568 r5 / cross-review luot 6 tren 273de20 — BAT DOI XUNG co ten. `dau` (mo
# khoi) nhan MOI hau to sau nhan: do la HOP DONG LAY TEN CA (A33 — phan hang
# khong doi so voi mau cu `^TU KIEM (r\d+): DO_KHAC`). `ranh` (dong khoi) chi
# nhan HINH THAT `DO_CHOT — ` / `DO_KHAC — <Kieu>: `. He qua do duoc:
#   `TU KIEM r512: DO_CHOT_fake-root`  doc DO_CHOT -> BAN GHI (ten r512 duoc lay)
#                                     doc DO_KHAC -> THAN (giu, khong dem)
# Luot 5 khai sai rang `ranh` "rong bang dau"; khong the siet `dau` (doi phan
# hang) va khong noi `ranh` theo `dau` (tai nuot `_fake-root`), nen KHAI va DO.
DAU_RONG_HON_RANH_THEO_HOP_DONG_TEN_CA = True

TRAN_CHAN_DOAN = 400


class ThanChanDoan(str):
    """Than chan doan, MANG THEO so dong cha da bo — sieu du lieu, khong van ban.

    #568 r5 / cross-review P2 tren 15c487c. Ban truoc noi `…[BO QUA n dong]` vao
    CUOI than roi `_goi_chan_doan` doc NGUOC con so ay ra bang regex. Con chi can
    in dung chuoi ay la cha khai mot con so KHONG PHAI CUA MINH. Do duoc:

        than = "x"*450 + LF + "…[BO QUA 7 dong]"      # con in ra, cha KHONG bo gi
        -> goi = "x"*400 + " …[CAT 50 ky tu] …[BO QUA 7 dong]"

    Cha khong bo dong nao ma khai bo bay dong. Do la dao ly 6 cua kho nay: mot
    chuoi do ma DANG BI THU phat ra khong duoc tro thanh bang chung cua phep do.
    So dong bo di theo DOI TUONG, khong di theo van ban, nen con khong gia mao duoc.
    """

    bo_qua: int = 0

    def __new__(cls, s: str, bo_qua: int = 0):
        o = super().__new__(cls, s)
        o.bo_qua = bo_qua
        return o


def _go_dau_phan_cach(than: str) -> str:
    """Go DUNG MOT dau phan cach giua nhan va than. KHONG dung `lstrip`.

    #568 r5 / cross-review luot 3 tren 7d0b012. Ban truoc dung
    `lstrip(" \u2014-")`, tuc mot TAP KY TU — no an het moi dau cach va moi dau
    gach o DAU THAN, ke ca khi chung la NOI DUNG. Do duoc:

        "TU KIEM r1: DO_CHOT \u2014 -42"            -> than "42"
        "TU KIEM r1: DO_CHOT \u2014 --gio-cao-nhat" -> than "gio-cao-nhat"

    Mot dau AM bien mat la SUA NOI DUNG chan doan, khong phai chuan hoa dinh
    dang — nguoi doc log nhan mot con so KHAC voi con so con bao.
    """
    return re.sub(r"^ ?[\u2014-] ?", "", than, count=1)


def _so_dong_bo(than) -> int:
    """SO DONG cha da bo. Doc tu SIEU DU LIEU, KHONG BAO GIO tu van ban than."""
    return getattr(than, "bo_qua", 0)


def _ngu_phap_ly_do(src: str) -> str:
    """Sinh NGU PHAP cua `ly_do` KHONG DO DUOC tu CHINH cac `return` cua bo doc kenh.

    #568 r5 / cross-review luot 7 tren e7f15cb — `.+` chi kiem "khong rong", bo
    cau truc ma ma bao dam: moi `ly_do` KHONG DO DUOC la MOT trong cac cau co
    tien to co dinh o `doc_kenh`/`_doc_kenh_xac_thuc`, noi them ` | rc_con=<int>
    | stderr[-200:]=<repr>` (chay_mot_mutant), hoac `khong phong duoc tien trinh
    con: <Kieu>: <exc>`. Doc bang AST de loi khai trong `ranh` KHONG the lech
    khoi nguon: r538 chot rang chuoi nay nam NGUYEN VAN trong dong `ranh`.
    """
    cau = []
    for fn in ast.walk(ast.parse(src)):
        if isinstance(fn, ast.FunctionDef) and fn.name in ("doc_kenh", "_doc_kenh_xac_thuc"):
            for n in ast.walk(fn):
                if (isinstance(n, ast.Return) and isinstance(n.value, ast.Tuple)
                        and getattr(n.value.elts[0], "id", "") == "KHONG_DO_DUOC"):
                    a = n.value.elts[1]
                    ph = a.values if isinstance(a, ast.JoinedStr) else [a]
                    cau.append("".join(re.escape(v.value) if isinstance(v, ast.Constant) else ".*"
                                       for v in ph))
    return ("(?:khong phong duoc tien trinh con: .*: .*|(?:" + "|".join(sorted(set(cau)))
            + r") \| rc_con=(?:0|-?[1-9][0-9]*) \| stderr\[-200:\]=.*)$")


def _khoi_chan_doan(stdout: str, nhan: str) -> list[tuple[str, str]]:
    r"""Trich NGUYEN chan doan cua con cho tung ca mang `nhan` (DO_KHAC / DO_CHOT).

    #568 — ban truoc bat `^TU KIEM (r\d+): DO_KHAC` tuc CHI TEN CA roi vut phan
    con lai, trong khi con IN DU `DO_KHAC — <Kieu>: <thong diep>`. Cha giu
    `p.stdout` trong tay ma in ra mot dong khong mang kieu ngoai le lan thong
    diep, nen tu log CI khong cach nao biet ca ay nem AssertionError (git that
    bai — `run(check=True)` nem lop ay TRAN), TypeError, OSError hay
    TimeoutExpired. Bon nguyen nhan can bon cach xu KHAC NHAU.

    Than ngoai le CO THE NHIEU DONG: mot AssertionError cua `run()` mang ca
    stdout lan stderr cua git. Nen khoi keo dai toi dong `TU KIEM ` / `DOT BIEN `
    ke tiep, chu KHONG dung o cuoi dong dau — dung o dong dau la tai lap dung
    cai loi dang chua, chi khac do sau.

    Mau neo giu Y HET ban truoc (`DO_KHAC` khong bat buoc co ` — `) de phep
    PHAN HANG khong doi: tap ten ca tra ve phai bang tap cu tren moi dau vao.
    """
    dau = re.compile(rf"^TU KIEM (r\d+): {nhan}(.*)$")
    # KHONG co dau cach sau "TU KIEM": dong TONG KET cua con la `TU KIEM: 21/23`
    # — dau hai cham, khong phai cach. Ban dau cua ham nay doi dau cach nen dong
    # ay KHONG duoc coi la ranh gioi va bi nuot vao than chan doan. Ca r524 bat
    # duoc ngay luot chay dau.
    # #568 r5 / M13 — ranh gioi CU dong khoi o BAT KY dong nao mang mot trong bon
    # tien to, ke ca khi do la NOI DUNG HOP LE cua ngoai le. Phan bi bo KHONG bao
    # gio toi `_goi_chan_doan`, nen khong co nhan `CAT` va khong co so ky tu mat.
    # Do duoc (cross-review codex, P2 tren eb4a9ab):
    #     "TU KIEM r506: DO_KHAC - AssertionError: first" + LF
    #     "LOI: root-cause" + LF + "more-details" + LF + "TU KIEM: 0/1" + LF
    #   -> [('r506', 'AssertionError: first')] · 'root-cause' co: False
    #   -> sau _goi_chan_doan: khong co nhan CAT
    # Mat hai dong than MA KHONG mot dau hieu nao noi la da mat — dung lop benh
    # #568 ton tai de chua, o mot tang khac. Xay ra KE CA khi thong diep ngan hon
    # tran 400, nen KHONG phai truong hop cat da khai cua `_goi_chan_doan`.
    #
    # Chua bang HAI nuoc, can ca hai:
    #  (a) HEP ranh gioi lai con dung nhung dong THAT SU la dau mot ban ghi cua
    #      bo do. `LOI:` roi khoi tap ay: trong bo do no chi xuat hien o cuoi
    #      `main`, con mot dong THAN bat dau bang `LOI:` la chuyen binh thuong.
    #  (b) Con lai thi DEM va KHAI. Mot dong than lo bat dau bang tien to THAT
    #      (vd `TU KIEM r512: DAT`) VAN dong khoi — do la chot chong gia mao,
    #      giu nguyen — nhung tu do den ban ghi ke tiep, moi dong KHONG phai dau
    #      ban ghi deu duoc dem va khai bang `[BO QUA n dong]`.
    # #568 r5 / cross-review P2 tren be5c3f2 — `DOT BIEN ` la tien to TRAN,
    # khong phai hinh mot ban ghi. Mot dong THAN "DOT BIEN root-cause" dong khoi
    # roi bien mat, KHONG duoc dem (no la chinh dong ranh gioi), nen khong co
    # nhan nao — dung lop mat IM LANG goi nay ton tai de chua. Do duoc:
    #   "TU KIEM r506: DO_KHAC - RuntimeError: first" + LF + "DOT BIEN root-cause"
    #   -> [('r506', 'RuntimeError: first')]   · khong nhan BO QUA, khong nhan CAT
    # Ban ghi THAT cua bo do luon la `DOT BIEN TU KIEM <ten> | `, `... <ten>: `
    # hoac `DOT BIEN TU KIEM: `. Siet ve DUNG ba hinh ay thi dong than tren roi
    # khoi tap ranh gioi va duoc GIU nguyen — khong mat, nen khong can nhan.
    # #568 r5 / cross-review luot 5 tren 31127d7 — NGU PHAP phai la TAP HINH cua
    # MOI ban ghi cot 0 ma bo do THAT phat (`print` trong ma chay, khong phai
    # fixture), doi chieu TUNG diem phat. Do duoc ba cho lech giua loi khai
    # va ma phat:
    #   · `DOT BIEN TU KIEM abc | r1 | root-cause` la RANH — duoi sau dau `|`
    #     thu hai khong bi rang buoc, tuc van la TIEN TO (lan thu 10 cua
    #     hinh dang "loi khai rong hon phep do" trong goi nay);
    #   · `DOT BIEN TU KIEM: KHONG DO DUOC — ...` THAT (khong co cach truoc dau
    #     hai cham) la THAN, con ban CO cach — thu khong ai phat — la RANH;
    #   · `CASE T<n>: DO - ` la hinh cua FIXTURE `_KICH_CON`, khong phai cua
    #     runner: `chay_ca` phat `CASE T<n>: DAT` va `CASE T<n>: DO — `.
    # Va bon ho bo do phat ma ngu phap chua ke: `MUTANT <ten> | <dich> | ...`
    # tung muc (ba hinh), `TU KIEM co dot bien rieng: ...`, dong ti so
    # `<n>/<n>`, va hai dong `LOI: ...` cuoi `main` (r5 da bo TIEN TO `LOI:` vi
    # qua rong; nay ke lai bang DU HINH, cung nguyen tac voi `MUTANT:`).
    # Dong con (`    VO CAN`, `    CHOT`, `    stderr:`) thut dau, khong phai
    # dau ban ghi.
    # Luot 6 (tren 273de20) — luot 5 van con NAM duoi la tien to (`TIN DUNG
    # GIA: `, `0 — ca do THUC TE: `, hai duoi MUTANT that bai, `LOI: ...
    # THIEU ...: `) va ho TU KIEM `DO_CHOT(?: |$)` rong hon hinh that. Nay moi
    # hau to co dinh deu DU, truong co cau truc dung cau truc (danh sach ca,
    # repr danh sach, `ly_do` khong rong). Loi khai "`ranh` rong bang `dau`"
    # cua luot 5 SAI va bi phan chung: xem `DAU_RONG_HON_RANH_THEO_HOP_DONG_TEN_CA`.
    # Luot 7 (tren e7f15cb) — tung TRUONG theo MIEN GIA TRI ma ma bao dam, khong
    # phai theo lop ky tu rong nhat: so nguyen in tu int la ASCII khong dem
    # (`0|[1-9][0-9]*`), rc o nhanh `!= 1` khong the la 1 hay `-0`, so lan neo
    # `!= 1`, `sau <n> lan` chi 1|2, ti so `n/n` la HAI SO BANG NHAU (tham chieu
    # nguoc), cot dich la danh sach ten ca (`r<n>` bang tu kiem, `T<n>` bang CA),
    # `ly_do` la mot trong cac cau cua `doc_kenh` (sinh tu AST — `_ngu_phap_ly_do`,
    # r538 doi chieu nguyen van) hoac `tap ca do chot [...] != dich [...]`, ten
    # ngoai le la BAT KY chuoi nao (`type("Échec", ...)` hop le) nen `.*: `. Ten ca
    # lay tu `dau` (hop dong `r\d+`) giu `\d`; ten tu bang la `[0-9]`.
    ranh = re.compile(r"^(?:TU KIEM r[0-9]+: (?:DAT$|DO_CHOT — |DO_KHAC — .*: )|TU KIEM: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|TU KIEM co dot bien rieng: (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*) nhom bat buoc · dot bien giet (?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|DOT BIEN TU KIEM(?: [A-Za-z0-9-]+ \| (?:r[0-9]+(?:,r[0-9]+)*)? \| (?:(?P<db>(?:0|[1-9][0-9]*))/(?P=db)$|TIN DUNG GIA: (?:ca chet vi loi VO CAN \['r\d+'(?:, 'r\d+')*\]$|child rc=(?:0|-[1-9][0-9]*|[2-9]|[1-9][0-9]+) != 1$)|0 — ca do THUC TE: (?:r\d+(?:,r\d+)*|\(rong\))$)| [A-Za-z0-9-]+: NEO KHONG DUY NHAT \((?:0|[2-9]|[1-9][0-9]+)\)$|: KHONG DO DUOC — phep cat bang hong$)|MUTANT: giet = (?:0|[1-9][0-9]*) · khong giet = (?:0|[1-9][0-9]*) · khong do duoc = (?:0|[1-9][0-9]*) / tong (?:0|[1-9][0-9]*)$|MUTANT [A-Za-z0-9-]+ \| (?:T[0-9]+(?:,T[0-9]+)*)? \| (?:(?P<mm>[1-9][0-9]*)/(?P=mm)$|KHONG DO DUOC \(sau [12] lan\): (?:khong phong duoc tien trinh con: .*: .*|(?:ban\ ghi\ TRUNG\ cho\ ca\ .*|ban\ ghi\ dong\ luot\ thieu\ rc\ kieu\ int|ban\ ghi\ khong\ neo\ dung\ luot:\ .*|ban\ ghi\ khong\ phai\ JSON|ban\ ghi\ khong\ phai\ object:\ .*|ban\ ghi\ thieu\ ten\ ca|ban\ ghi\ vua\ mang\ ten\ ca\ vua\ khai\ dong\ luot|bo\ doc\ kenh\ nem\ .*:\ .*|ca\ do\ vi\ ngoai\ le\ KHONG\ phai\ TinHieuChotCa:\ .*\ \|\ .*|chi\ tiet\ khong\ phai\ chuoi\ cho\ ca\ .*|co\ ban\ ghi\ SAU\ ban\ ghi\ dong\ luot|dau\ dong\ luot\ khong\ phai\ bool\ true:\ .*|dich\ RONG:\ khong\ cap\ GIET\ khi\ khong\ ca\ nao\ phai\ chet|dich\ co\ ten\ ca\ KHONG\ ton\ tai:\ .*|kenh\ khong\ ton\ tai|khong\ doc\ duoc\ kenh:\ .*:\ .*|nhan\ khong\ hop\ le\ cho\ ca\ .*:\ .*|rc\ dong\ luot\ .*\ !=\ rc\ tien\ trinh\ .*|ten\ ca\ khong\ phai\ chuoi:\ .*|thieu\ ban\ ghi\ dong\ luot|thieu\ ca\ .*\ /\ ca\ la\ .*) \| rc_con=(?:0|-?[1-9][0-9]*) \| stderr\[-200:\]=.*)$|0/[1-9][0-9]*: tap ca do chot \[(?:'T[0-9]+'(?:, 'T[0-9]+')*)?\] != dich \[(?:'T[0-9]+'(?:, 'T[0-9]+')*)?\]$)|CASE T[0-9]+: (?:DAT$|DO — )|(?:0|[1-9][0-9]*)/(?:0|[1-9][0-9]*)$|LOI: (?:ba so hang khong cong dung tong$|nhom bat buoc THIEU \(chua chay hoac chua co dot bien\): \['r[0-9]+'(?:, 'r[0-9]+')*\]$))")
    khoi: list[list] = []
    # `dang_mo` la CO TRANG THAI, khong phai `khoi` khac rong: gap ranh gioi thi
    # khoi phai DONG HAN. Ban dau chi BO QUA dong ranh gioi roi nhat tiep, nen
    # moi thu sau mot ca DAT lai chay nguoc vao khoi truoc no.
    dang_mo = False
    # M13(b) — so dong BI BO sau khi mot khoi dong lai, tinh den ban ghi ke tiep.
    # CHI dem dong KHONG phai dau ban ghi: mot ban ghi ke tiep la ket thuc binh
    # thuong, khong phai mat mat. Nho the, dau vao BINH THUONG khong sinh nhan
    # nao — do la chieu ma A30 doi, va la cho de khai rong nhat.
    bo_qua = 0
    for dong in stdout.split(chr(10)):
        m = dau.match(dong)
        if m:
            if khoi and bo_qua:
                khoi[-1][2] = bo_qua
            bo_qua = 0
            khoi.append([m.group(1), [_go_dau_phan_cach(m.group(2))], 0])
            dang_mo = True
        elif ranh.match(dong):
            dang_mo = False
        elif dang_mo:
            khoi[-1][1].append(dong)
        elif dong.strip():
            bo_qua += 1
    if khoi and bo_qua:
        khoi[-1][2] = bo_qua
    return [(ca, ThanChanDoan("\n".join(x for x in than if x.strip()), n))
            for ca, than, n in khoi]


def _goi_chan_doan(than: str) -> str:
    """Goi mot than chan doan, va KHAI TUONG MINH khi phai cat.

    Nuot lang phan du la dung benh #568 o quy mo nho hon, nen cat thi phai noi
    da cat BAO NHIEU ky tu — nguoi doc log biet minh dang thieu bao nhieu.
    """
    so_bo = _so_dong_bo(than)
    than = (str(than) or "").strip() or "(rong)"
    than = than.replace("\n", " | ")
    # #568 r5 / cross-review P2 tren be5c3f2 — `…[BO QUA n dong]` la SIEU DU LIEU
    # ve phep do, khong phai noi dung chan doan. Ban truoc noi no vao CUOI than
    # roi cat TU DAU, nen than dai lam tran nuot mat chinh no: cha chi con so ky
    # tu bi cat, mat han so DONG bi bo — tuc A29 khai ma khong den duoc nguoi doc.
    # Giu nhan NGOAI ngan sach tran. Huong cat GIU NGUYEN (ngoai pham vi r5).
    #
    # Luot 2 (tren 15c487c) — ban va DAU TIEN cua P2 nay doc con so NGUOC ra tu
    # van ban than bang regex, nen con chi can in dung chuoi la cha khai mot con
    # so khong phai cua minh. Nay so ay den tu `ThanChanDoan.bo_qua` — SIEU DU
    # LIEU do CHINH cha dat — con van ban than khong con quyen gi voi no.
    # Ten RIENG cho nhan cua CHA. Ca r536 o (1b) do duoc: neu cha dung chung
    # chuoi `…[BO QUA n dong]` voi than con, thi mot than con mang dung chuoi ay
    # se doc y het mot loi khai cua cha — nguoi doc log khong phan biet duoc.
    # Doi ten la cach duy nhat khong phai SUA than con de lam ro chuyen ay.
    duoi = f" …[CHA BO {so_bo} dong]" if so_bo else ""
    if len(than) <= TRAN_CHAN_DOAN:
        return than + duoi
    return f"{than[:TRAN_CHAN_DOAN]} …[CAT {len(than) - TRAN_CHAN_DOAN} ky tu]{duoi}"


TU_KIEM_NONCE_ENV = "NHANH_DON_DUOC_TU_KIEM_NONCE"
TU_KIEM_FILE_ENV = "NHANH_DON_DUOC_TU_KIEM_FILE"


def _bang_chung_tu_kiem(stdout, proof_text, nonce, expected, kh_chot, kh_khac):
    """M15/M16 completion on a separate channel; stdout remains diagnostic data.

    Guards literal prewritten output, not an arbitrary child reading the nonce
    and implementing this protocol without running tests.
    """
    try:
        proof = json.loads(proof_text)
    except (ValueError, TypeError, RecursionError):
        return False
    if not isinstance(proof, dict) or proof.get("nonce") != nonce:
        return False
    if proof.get("cases") != expected:
        return False
    totals = re.findall(r"^TU KIEM: ([0-9]+)/([0-9]+)\r?$", stdout, re.MULTILINE)
    if len(totals) != 1:
        return False
    # Bound conversion by the parent's known count, including Python's int limit.
    if any(len(number) > len(str(len(expected))) for number in totals[0]):
        return False
    passed, total = map(int, totals[0])
    if total != len(expected):
        return False
    failed = [case for case, _ in kh_chot + kh_khac]
    if len(failed) != len(set(failed)) or not set(failed) <= set(expected):
        return False
    return total - passed == len(failed)


def chay_dot_bien_tu_kiem(muc=None, chi_dich=False):
    """Chay tung dot bien tren BAN SAO cua CHINH tep nay, doi DUNG ca dich do.

    WP748 r16 `chi_dich=True` (targeted_mutant_gate): con chi chay CA DICH da khai, khong
    chay 52 ca — KHONG do duoc ca ngoai dich con xanh duoi dot bien; do la viec cua
    full_mutant_audit (`chi_dich=False`, mac dinh, nghia cu)."""
    giet = hong = khong_do_tk = 0
    goc = Path(__file__).read_text(encoding="utf-8")
    # Moi mau neo xuat hien HAI lan: mot o ma that, mot o CHINH bang duoi day.
    # Chi ap len phan TRUOC bang — cung lop loi ma r506 da dinh (dem chuoi thi tu
    # khop chinh than minh). Do duoc: khong cat thi ca 11 neo deu "KHONG DUY NHAT (2)".
    # L3 (luot 2) — phai CAT BO RIENG BANG, khong phai cat bo TAT CA phia duoi.
    # Ban truoc chi thay phan TRUOC bang, nen `main`, `chay_tu_kiem`,
    # `chay_dot_bien_tu_kiem`, `NHOM_BAT_BUOC`/`SAN_NHOM` deu NAM NGOAI tam dot
    # bien — mot vung mu THAT, do duoc: `final-gate-open` song tron ven full.
    # PHEP CAT PHAI NEO THEO DAU DONG, va phai TU KIEM. Da tra gia: khi
    # `_chay_main_gia` co dong `m.DOT_BIEN_TU_KIEM = [`, phep `goc.index(...)`
    # khong neo dau dong khop NGAY TRONG THAN HAM ay, nen `bang` nuot tron ca
    # r501..r516 lan `TU_KIEM`, con bang THAT roi xuong `duoi` — moi neo hoa ra
    # "khong duy nhat" va ca bo dot bien tu kiem hong lang le. Cung ho voi bai
    # hoc "cong vang mat trong giong cong xanh".
    dau_bang = "\nDOT_BIEN_TU_KIEM = [\n"
    cat = goc.index(dau_bang) + 1
    het = goc.index("\n]\n", cat) + len("\n]\n")
    dau, bang, duoi = goc[:cat], goc[cat:het], goc[het:]
    # FAIL-CLOSE theo CAU TRUC: `bang` phai mo dung bang o cot 0 va dong o cot 0.
    # KHONG kiem duoc bang NOI DUNG (kieu "ten muc khong duoc ro ri ra ngoai
    # bang"): `DOT_BIEN_TU_KIEM` co the da bi THAY trong bo nho — `r516` lam dung
    # the — nen ten muc luc do la cua fixture va nam hop le trong than ca. Da thu
    # va chot ay bao dong gia ngay lan chay dau.
    if not bang.startswith("DOT_BIEN_TU_KIEM = [\n") or not bang.endswith("\n]\n"):
        print("DOT BIEN TU KIEM: KHONG DO DUOC — phep cat bang hong")
        return 0, 0, len(DOT_BIEN_TU_KIEM)
    with tempfile.TemporaryDirectory() as td:
        for ten, dich, neo, thay in (DOT_BIEN_TU_KIEM if muc is None else muc):
            ngoai_bang = dau.count(neo) + duoi.count(neo)
            if ngoai_bang != 1:
                print(f"DOT BIEN TU KIEM {ten}: NEO KHONG DUY NHAT ({ngoai_bang})")
                hong += 1
                continue
            d = Path(td) / ten
            d.mkdir()
            tep = d / Path(__file__).name
            tep.write_text(dau.replace(neo, thay) + bang + duoi.replace(neo, thay),
                           encoding="utf-8", newline="\n")
            shutil.copy2(TOOL, d / TOOL.name)
            env = dict(os.environ, NHANH_DON_DUOC_CHI_TU_KIEM="1", PYTHONDONTWRITEBYTECODE="1")
            env.pop(KENH_ENV, None)
            env.pop(TU_KIEM_CHI_CA_ENV, None)
            if chi_dich:
                env[TU_KIEM_CHI_CA_ENV] = ",".join(dich)
            nonce = secrets.token_hex(32)
            env[TU_KIEM_NONCE_ENV] = nonce
            proof_path = d / "tu-kiem-hoan-tat.json"
            env[TU_KIEM_FILE_ENV] = str(proof_path)
            p = run([sys.executable, tep.name], d, check=False, env=env)
            # F01 (luot 3) — BA chot doc lap, khong gop: (1) khong ca nao duoc
            # chet vi loi VO CAN; (2) tien trinh con phai THAT SU thoat 1 — bo
            # ghi nhan danh sach do thi no van in "DO" ma rc ve 0; (3) tap ca do
            # dung bang dich. Thieu bat ky chot nao la mot duong cap TIN DUNG GIA.
            try:
                proof_text = proof_path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                # r2 M1 diem nuot: chay_dot_bien_tu_kiem. VANG tep la TIN HIEU con chua
                # xong (thu ca nay do), khong phai ha tang; moi OSError khac thi ghi.
                if not isinstance(sys.exc_info()[1], FileNotFoundError):
                    _ghi_ha_tang(sys.exc_info()[1])
                proof_text = None
            kh_chot = _khoi_chan_doan(p.stdout, "DO_CHOT")
            kh_khac = _khoi_chan_doan(p.stdout, "DO_KHAC")
            bang_chung = _bang_chung_tu_kiem(
                p.stdout, proof_text, nonce,
                [c for c, _, _ in TU_KIEM if not chi_dich or c in dich], kh_chot, kh_khac)
            do_chot = {ca for ca, _ in kh_chot}
            do_khac = {ca for ca, _ in kh_khac}
            # r7 preserves diagnostic routing; missing completion evidence
            # changes the final state to KHONG DO DUOC after forwarding.
            if do_khac:
                hong += 1
                print(f"DOT BIEN TU KIEM {ten} | {','.join(dich)} | TIN DUNG GIA: "
                      f"ca chet vi loi VO CAN {sorted(do_khac)}")
                for ca, than in kh_khac:
                    print(f"    VO CAN {ca}: {_goi_chan_doan(than)}")
            elif p.returncode != 1:
                hong += 1
                print(f"DOT BIEN TU KIEM {ten} | {','.join(dich)} | TIN DUNG GIA: "
                      f"child rc={p.returncode} != 1")
                # Nhanh nay thuong la con chet TRUOC khi in duoc gi, nen stdout
                # rong va stderr la cho DUY NHAT con chan doan.
                print(f"    stderr: {_goi_chan_doan(p.stderr)}")
            elif bang_chung and do_chot == set(dich):
                giet += 1
                print(f"DOT BIEN TU KIEM {ten} | {','.join(dich)} | {len(dich)}/{len(dich)}")
            else:
                hong += 1
                print(f"DOT BIEN TU KIEM {ten} | {','.join(dich)} | 0 — ca do THUC TE: "
                      f"{','.join(sorted(do_chot)) or '(rong)'}")
                # Duong vao THU BA co DUNG HAI duong, va r1 chi dong duong dau.
                # Liet ke het TRUOC khi va: `kh_chot` khac rong (P1) hoac RONG
                # (P2) — vet can, vi mot tap chi co hai kha nang ay.
                if kh_chot:
                    # P1 — ca THUONG: biet ca NAO do van chua noi vi SAO no do,
                    # ma day dung la nhanh "dot bien giet nham ca khac" — can nhat.
                    for ca, than in kh_chot:
                        print(f"    CHOT {ca}: {_goi_chan_doan(than)}")
                else:
                    # P2 — r2/M6. CA SUY BIEN cua CHINH nhanh nay, r1 de ho.
                    # `main` duoi CHI_TU_KIEM tra `1 if chay_tu_kiem() else 0`, va
                    # `chay_tu_kiem` in DO_CHOT hoac DO_KHAC cho MOI ca hong. Nen
                    # rc=1 ma KHONG nhan nao <=> con chet NGOAI ham ay (loi muc
                    # module: SyntaxError / NameError / ImportError) — luc do
                    # stdout RONG con stderr mang nguyen nhan.
                    # Bo qua day la tai lap DUNG benh (B) ma packet nay sinh ra de
                    # chua, chi nho hon: mot nhan tran khong noi nguyen nhan.
                    print(f"    stderr: {_goi_chan_doan(p.stderr)}")
            if not bang_chung:
                # Preserve existing diagnostic routing, but never collapse an
                # incomplete/contradictory measurement into an ordinary failure.
                hong -= 1
                khong_do_tk += 1
                print(f"    KHONG DO DUOC: {ten} — thieu hoac mau thuan bang chung hoan tat")
    return giet, hong, khong_do_tk


def chay_tu_kiem():
    do = []
    completed = []
    nonce = os.environ.pop(TU_KIEM_NONCE_ENV, None)
    proof_path = os.environ.pop(TU_KIEM_FILE_ENV, None)
    # WP748 r22 l2 — DON thu muc tam hong (Windows: tien trinh vua bi giet chua nha handle) KHONG duoc nuot bang
    # chung hoan tat cua ca luot: CI 39741391940 manh 5 do `timeout-chi-giet-con` thanh KHONG DO DUOC vi `rmtree`
    # nem SAU dong tong ket, TRUOC khi ghi proof. Don hong thi noi ra stderr, khong im.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        for ten, fn, can_thu_muc in TU_KIEM:
            d = Path(td) / ten
            d.mkdir()
            truoc = len(_SO_HA_TANG.loi)
            try:
                # #593 r2 M3 — loi HA TANG that (so, hoac chuoi ngoai le) => KHONG DO DUOC
                # cho ca DAT (lam tron LEN) lan chot: `_ha_tang_cua_ca` nem => DO_KHAC.
                try:
                    fn(d) if can_thu_muc else fn()
                except TinHieuChotCa as goc:
                    _ha_tang_cua_ca(truoc, goc)
                    raise
                except Exception as goc:     # noqa: BLE001 — chi de GHI + doi nhan; luon nem lai
                    _ha_tang_cua_ca(truoc, goc)   # loi khac: runner long cung phai de lai nguon
                    raise
                _ha_tang_cua_ca(truoc)
                print(f"TU KIEM {ten}: DAT")
            # F01 (luot 3) — PHAI tach hai lop, y het `chay_ca` da tach cho ca T*.
            # Ban truoc in CHUNG mot tien to `DO`, nen bo cham tu dot bien khong
            # phan biet duoc "chet dung chot" voi "chet vi loi VO CAN" va cap TIN
            # DUNG GIA: do duoc, muc `bo-doi-ban-ghi-dong-luot` cua bang goc duoc
            # cong nhan 3/3 bang BA `AttributeError`.
            except TinHieuChotCa as exc:
                do.append(ten)
                print(f"TU KIEM {ten}: DO_CHOT — {exc}")
            except Exception as exc:
                do.append(ten)
                print(f"TU KIEM {ten}: DO_KHAC — {type(exc).__name__}: {exc}")
            completed.append(ten)
    if Path(td).exists():
        print(f"TU KIEM: thu muc tam KHONG don duoc: {td}", file=sys.stderr)
    print(f"TU KIEM: {len(TU_KIEM) - len(do)}/{len(TU_KIEM)}")
    if nonce and proof_path:
        Path(proof_path).write_text(json.dumps({"nonce": nonce, "cases": completed}), encoding="utf-8")
    return do


# ---- #661 CI-DOT-BIEN-CHIA-MANH: MANH (M1) chi tinh GIET qua bo phan hang SAN CO; GOP (M2) --
MANH_ENV, MANH_RA_ENV, PHIEN_BAN_MANH = "NHANH_DON_DUOC_MANH", "NHANH_DON_DUOC_MANH_RA", 1
_KHOA_MANH = {"phien_ban", "manh", "so_manh", "sha256_test", "sha256_tool", "giet", "tk_giet"}


def doc_manh(gia_tri) -> tuple[int, int]:
    """M1 — `k/N` khop DUNG `^[0-9]/[2-8]$` (fullmatch: khong LF cuoi) va k < N."""
    if not re.fullmatch(r"[0-9]/[2-8]", gia_tri or ""):
        raise ValueError(f"{MANH_ENV}={gia_tri!r} sai hinh k/N")
    k, n = map(int, gia_tri.split("/"))
    if k >= n:
        raise ValueError(f"{MANH_ENV}={gia_tri!r}: can k < N")
    return k, n


def phan_hoach(bang, k: int, n: int) -> list:
    """M1 — muc thu i vao manh `i % n`. Ten TRUNG thi phan hoach theo ten vo nghia."""
    ten = [x[0] for x in bang]
    if len(set(ten)) != len(ten):
        raise ValueError("ten mutant TRUNG trong bang")
    return [x for i, x in enumerate(bang) if i % n == k]


_bam = lambda tep: hashlib.sha256(Path(tep).read_bytes()).hexdigest()   # noqa: E731


def chay_manh(k: int, n: int, db, dbtk, ra) -> int:
    """M1 — T1..T8 + tron TU_KIEM + CHI hai phan hoach; ghi `ra` KHI DAT TRON (nen `giet` = tap da giet); KHONG in dong MAU_DAY_DU."""
    ra = Path(ra).resolve()               # MOT lan, truoc moi con (cwd khong doi)
    if chay_ca(None):
        print(f"MANH {k}/{n}: T1..T8 DO — khong ghi bang chung")
        return 1
    dat, khong_giet, khong_do = chay_dot_bien(db)
    tu_kiem_do = chay_tu_kiem()
    tk_giet, tk_hong, tk_khong_do = chay_dot_bien_tu_kiem(dbtk)
    print(f"MANH {k}/{n}: MUTANT giet = {dat} / {len(db)} · TU DOT BIEN giet = {tk_giet} / {len(dbtk)}")
    if tu_kiem_do or (dat, khong_giet, khong_do, tk_giet, tk_hong, tk_khong_do) != (len(db), 0, 0, len(dbtk), 0, 0):
        print(f"MANH {k}/{n}: DO — khong ghi bang chung")
        return 1
    ra.parent.mkdir(parents=True, exist_ok=True)
    ra.write_text(json.dumps({"phien_ban": PHIEN_BAN_MANH, "manh": k, "so_manh": n,
                              "sha256_test": _bam(__file__), "sha256_tool": _bam(TOOL),
                              "giet": [x[0] for x in db], "tk_giet": [x[0] for x in dbtk]}), encoding="utf-8")
    return 0


def _loi_gop(thu_muc: Path):
    """M2 — `(loi, N)`; moi chot MOT dieu kien (`r552`). Thanh vien + hop = tron bang + khong lap => manh BANG phan hoach."""
    doc = []
    for tep in sorted(Path(thu_muc).glob("*.json")):
        try:
            doc.append(json.loads(tep.read_text(encoding="utf-8")))
        except OSError as e:
            _ghi_ha_tang(e)                       # r2 M1 diem nuot: _loi_gop
            return [f"{tep.name}: {type(e).__name__}: {e}"], None
        except ValueError as e:
            return [f"{tep.name}: JSON hong ({e})"], None
    if not doc:
        return ["khong co tep manh nao"], None
    if any(not isinstance(x, dict) or set(x) != _KHOA_MANH for x in doc):
        return ["tep manh sai khoa"], None
    # Codex #661 luot 1 F02 — KIEU TRUOC gia tri, MOI tep: `True == 1`, `4.0 == 4`, `{ten: ..}` duyet nhu mang.
    if any(type(x[k]) is not int for x in doc for k in ("phien_ban", "so_manh", "manh")):
        return ["phien_ban/so_manh/manh phai la int"], None
    if any(type(x[k]) is not list for x in doc for k in ("giet", "tk_giet")):
        return ["giet/tk_giet phai la mang"], None
    if any(x["phien_ban"] != PHIEN_BAN_MANH for x in doc):
        return ["phien_ban lech"], None
    n = doc[0]["so_manh"]
    if not 2 <= n <= 8 or any(x["so_manh"] != n for x in doc):
        return [f"so_manh lech: {[x['so_manh'] for x in doc]}"], None
    if sorted(x["manh"] for x in doc) != list(range(n)):
        return [f"can dung {n} manh 0..{n - 1}, thay {[x['manh'] for x in doc]}"], None
    bam = [_bam(__file__), _bam(TOOL)]
    if any([x["sha256_test"], x["sha256_tool"]] != bam for x in doc):
        return ["sha256 lech tep DANG CHAY"], None
    loi = []
    for khoa, bang in (("giet", DOT_BIEN), ("tk_giet", DOT_BIEN_TU_KIEM)):
        for x in doc:
            thuoc = {y[0] for y in phan_hoach(bang, x["manh"], n)}
            if any(ten not in thuoc for ten in x[khoa]):
                loi.append(f"manh {x['manh']}: {khoa} co ten NGOAI phan hoach")
        hop = [ten for x in doc for ten in x[khoa]]
        if set(hop) != {y[0] for y in bang}:
            loi.append(f"{khoa}: hop cac manh != tron bang")
        if len(hop) != len(set(hop)):
            loi.append(f"{khoa}: ten LAP")
    loi += _loi_nhom_bat_buoc()
    return loi, n


def _loi_nhom_bat_buoc() -> list:
    """Nhom bat buoc phai DU (moi ca bat buoc co trong TU_KIEM VA co tu dot bien nham vao) va KHONG duoi san.

    WP748 r20 (Codex WP748-R2 tren 9d471d9) — chot nay tung chi nam trong `_loi_gop`, nen `gop_dich`
    (duong CI moi, ca targeted lan full) nhan bang thieu ca bat buoc ma van tra 0. Dung CHUNG cho ca
    hai duong gom; mot ban sao thu hai se troi lech, va neo dot bien `gop-bo-kiem-nhom`/`-san` doi duy nhat."""
    nhom = {c for _, dich, _, _ in DOT_BIEN_TU_KIEM for c in dich}
    thieu = (NHOM_BAT_BUOC - nhom) | (NHOM_BAT_BUOC - {t for t, _, _ in TU_KIEM})
    if thieu or len(NHOM_BAT_BUOC) < SAN_NHOM:
        return [f"nhom bat buoc thieu {sorted(thieu)} hoac duoi san {SAN_NHOM}"]
    return []


def gop(thu_muc) -> int:
    """M2 — `--gop <thu muc>`: DAT in ba dong duong (dong MUTANT khop `MAU_DAY_DU`)."""
    loi, n = _loi_gop(thu_muc)
    for x in loi:
        print(f"GOP: LOI — {x}")
    if loi:
        return 1
    g, tk = len(DOT_BIEN), len(DOT_BIEN_TU_KIEM)
    print(f"GOP MANH {n}/{n}")
    print(f"MUTANT: giet = {g} · khong giet = 0 · khong do duoc = 0 / tong {g}")
    print(f"TU DOT BIEN: giet = {tk} / {tk}")
    return 0


# ---- WP748 r16 `targeted_mutant_gate` — cong PR, KHONG phai full_mutant_audit ----------------
# Hai muc (spec ops/specs/wp748-windows-gates-r16.md). Muc PR: 52 ca nen + 239 tu dot bien, MOI
# con chi chay CA DICH da khai, + 10 dot bien san pham; chia N manh can theo CHI PHI do duoc.
# Muc truoc merge/land/release: full_mutant_audit = `chay_manh`/`gop` cu (moi con chay du 52 ca),
# chay rieng (`ci-dot-bien-du.yml`). Bien nhan, dong in va UI cua muc PR KHONG BAO GIO duoc goi
# la full mutant audit: muc PR KHONG do ca ngoai dich con xanh duoi moi dot bien.
TU_KIEM_CHI_CA_ENV = "NHANH_DON_DUOC_TU_KIEM_CHI_CA"
DICH_ENV, DICH_RA_ENV, PHIEN_BAN_DICH = "NHANH_DON_DUOC_DICH", "NHANH_DON_DUOC_DICH_RA", 1
CHE_DO_DICH = "targeted_mutant_gate"
# full_mutant_audit qua CUNG bo bien nhan (head, rc that, tien do, RAM, thanh vien): `NHANH_DON_DUOC_DICH_DU=1`
# => moi tu dot bien chay DU 52 ca (`chi_dich=False`, nghia goc), KHONG ap tran duong gang.
CHE_DO_DU, DICH_DU_ENV, TRAN_GIAY_CON_DU = "full_mutant_audit", "NHANH_DON_DUOC_DICH_DU", 3600
_MAU_DICH = r"[0-9]/[2-8]"         # cung mien k/N voi `doc_manh`
TRAN_DUONG_GANG_GIAY = 540          # spec r16: duong gang DO DUOC, khong phai so ly thuyet
TRAN_GIAY_CON_DICH = 600            # mot con qua tran => rc 124 => manh DO
TRAN_NHAT_KY = 64 * 1024            # nhat ky manh co tran (ky tu), giu PHAN CUOI
TRANG_THAI_KQ = ("passed", "failed", "skipped", "not_run", "not_measured", "inconclusive")
# Giay moi ca nen — bien nhan ho so g12 (52 ca 274.8 s, rc0, JSON sha256 e74ad932...). Chi
# dung de CAN manh; sai so chi lam lech can bang, KHONG doi phan quyet. Thieu/thua ten => LOI.
GIAY_CA_HO_SO = {
    "r501": 5.61, "r502": 2.04, "r503": 0.03, "r504": 0.06, "r505": 0.65, "r506": 8.16,
    "r507": 0.18, "r508": 0.08, "r509": 1.43, "r510": 0.03, "r511": 0.03, "r512": 7.45,
    "r513": 10.66, "r514": 25.69, "r515": 0.15, "r516": 7.75, "r517": 1.08, "r518": 0.3,
    "r519": 12.21, "r520": 3.37, "r521": 8.06, "r522": 2.43, "r523": 1.43, "r524": 0.01,
    "r525": 0.57, "r526": 0.55, "r527": 0.4, "r528": 58.57, "r529": 1.47, "r530": 0.66,
    "r531": 0.92, "r532": 0.56, "r533": 0.47, "r534": 0.46, "r535": 0.44, "r536": 0.41,
    "r537": 0.42, "r538": 0.92, "r539": 9.77, "r540": 0.74, "r541": 0.39, "r542": 4.96,
    "r543": 0.65, "r544": 0.53, "r545": 0.49, "r546": 72.02, "r547": 1.12, "r548": 4.41,
    "r549": 0.58, "r550": 0.52, "r551": 5.72, "r552": 2.19, "r553": 0.05,
    "r554": 0.05, "r555": 7.2,          # WP748 r22 (l2: ba bien the)
    "r556": 1.2, "r557": 0.05,          # WP748 r22 l2
}
GIAY_PHONG_CON, GIAY_DOT_BIEN_SP, GIAY_NEN_SP = 1.5, 30.0, 27.0
_KHOA_DICH = {"phien_ban", "che_do", "manh", "so_manh", "head", "sha256_test", "sha256_tool",
              "rc", "bat_dau", "ket_thuc", "giay", "ram_dinh_mb", "pham_vi_ram", "so_lan_chay_lai",
              "tien_do", "ca_dich", "ket_qua", "nhat_ky_duoi"}


def _loc_tu_kiem(chi_ca: str) -> list:
    """Con: tap ca dich KHAC RONG, KHONG trung, MOI ten la ca co that; sai => ValueError."""
    ten = chi_ca.split(",") if chi_ca else []
    co = {t for t, _, _ in TU_KIEM}
    if not ten or len(ten) != len(set(ten)) or not set(ten) <= co:
        raise ValueError(f"{TU_KIEM_CHI_CA_ENV}={chi_ca!r}: rong, trung hoac ten la")
    return [x for x in TU_KIEM if x[0] in set(ten)]


def doc_dich(gia_tri) -> tuple[int, int]:
    """`k/N` khop DUNG `[0-9]/[2-8]` (fullmatch) va k < N."""
    if not re.fullmatch(_MAU_DICH, gia_tri or "") or int(gia_tri[0]) >= int(gia_tri[2]):
        raise ValueError(f"{DICH_ENV}={gia_tri!r} sai hinh k/N (k < N, N 2..8)")
    return int(gia_tri[0]), int(gia_tri[2])


def _muc_dich(du=False):
    """Moi muc: `(khoa, trong so, muc)`. `du` => trong so tu dot bien = DU 52 ca. Fail-closed khi lech."""
    ten_tk = [t for t, _, _ in TU_KIEM]
    if set(GIAY_CA_HO_SO) != set(ten_tk) or len(ten_tk) != len(set(ten_tk)):
        raise ValueError("GIAY_CA_HO_SO lech TU_KIEM (thieu/thua/trung ten)")
    muc = [(f"ca:{t}", GIAY_CA_HO_SO[t], x) for x in TU_KIEM for t in [x[0]]]
    for x in DOT_BIEN_TU_KIEM:
        if not x[1] or not set(x[1]) <= set(ten_tk):
            raise ValueError(f"tu dot bien {x[0]}: tap dich rong hoac ten la")
        ca_chay = GIAY_CA_HO_SO if du else sorted(set(x[1]))
        muc.append((f"tk:{x[0]}", GIAY_PHONG_CON + sum(GIAY_CA_HO_SO[c] for c in sorted(ca_chay)), x))
    muc += [(f"db:{x[0]}", GIAY_DOT_BIEN_SP, x) for x in DOT_BIEN]
    khoa = [k for k, _, _ in muc]
    if len(khoa) != len(set(khoa)):
        raise ValueError("khoa muc TRUNG (ten mutant lap)")
    return muc


def phan_hoach_dich(n: int, du=False) -> list:
    """LPT tat dinh: muc nang truoc (hoa: theo khoa), vao manh dang nhe nhat (hoa: chi so nho)."""
    tai, manh = [0.0] * n, [[] for _ in range(n)]
    for khoa, w, x in sorted(_muc_dich(du), key=lambda m: (-m[1], m[0])):
        i = min(range(n), key=lambda j: (tai[j], j))
        tai[i] += w
        manh[i].append((khoa, x))
    return manh


def _git_head():
    try:
        p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=HERE, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    h = p.stdout.strip()
    return h if p.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}", h) else None


def _bat_dau_do_ram():
    """Windows: dua manh vao Job Object de do dinh commit CA CAY tien trinh. Tra handle/None."""
    if os.name != "nt":
        return None
    try:
        import ctypes
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.CreateJobObjectW.restype = ctypes.c_void_p
        k32.GetCurrentProcess.restype = ctypes.c_void_p
        k32.AssignProcessToJobObject.argtypes = (ctypes.c_void_p, ctypes.c_void_p)
        job = k32.CreateJobObjectW(None, None)
        if job and k32.AssignProcessToJobObject(job, k32.GetCurrentProcess()):
            return job
    except (OSError, AttributeError):
        pass
    return None


def _ram_dinh_mb(job):
    """`(MB, pham_vi)` — dinh RAM do duoc; `(None, ly do)` khi KHONG DO DUOC (gop se DO)."""
    if os.name != "nt":
        import resource
        kb = max(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        return round(kb / 1024, 1), "posix ru_maxrss: max(manh, con lon nhat da thu hoi)"
    import ctypes
    from ctypes import wintypes

    class _IO(ctypes.Structure):
        _fields_ = [(f, ctypes.c_ulonglong) for f in ("r", "w", "o", "rb", "wb", "ob")]

    class _CB(ctypes.Structure):
        _fields_ = [("a", ctypes.c_longlong), ("b", ctypes.c_longlong), ("c", wintypes.DWORD),
                    ("d", ctypes.c_size_t), ("e", ctypes.c_size_t), ("f", wintypes.DWORD),
                    ("g", ctypes.c_size_t), ("h", wintypes.DWORD), ("i", wintypes.DWORD)]

    class _EXT(ctypes.Structure):
        _fields_ = [("cb", _CB), ("io", _IO), ("pml", ctypes.c_size_t), ("jml", ctypes.c_size_t),
                    ("peak_p", ctypes.c_size_t), ("peak_j", ctypes.c_size_t)]

    class _PMC(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("pf", wintypes.DWORD), ("peak_ws", ctypes.c_size_t)] + \
                   [(f"x{i}", ctypes.c_size_t) for i in range(7)]   # WP748 r20 (r553): du 8 SIZE_T, ke ca PeakPagefileUsage
    try:
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        if job:
            k32.QueryInformationJobObject.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p,
                                                      wintypes.DWORD, ctypes.c_void_p)
            ext = _EXT()
            if k32.QueryInformationJobObject(job, 9, ctypes.byref(ext), ctypes.sizeof(ext), None) and ext.peak_j:
                return round(ext.peak_j / 2 ** 20, 1), "windows job PeakJobMemoryUsed: commit dinh CA CAY"
        k32.GetCurrentProcess.restype = ctypes.c_void_p
        psapi = ctypes.WinDLL("psapi")
        psapi.GetProcessMemoryInfo.argtypes = (ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD)
        pmc = _PMC()
        pmc.cb = ctypes.sizeof(pmc)
        if psapi.GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb) and pmc.peak_ws:
            return round(pmc.peak_ws / 2 ** 20, 1), "windows PeakWorkingSet CHI tien trinh manh (khong vao duoc job)"
    except (OSError, AttributeError, ValueError) as e:
        return None, f"KHONG DO DUOC: {type(e).__name__}: {e}"
    return None, "KHONG DO DUOC: API tra 0"


def _iso_utc():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class _GhiCoTran(io.TextIOBase):
    """Chuyen tiep stdout THAT (flush moi dong) va giu PHAN CUOI co tran cho bien nhan."""

    def __init__(self, that):
        self.that, self.duoi, self.bo = that, [], 0

    def write(self, s):
        self.that.write(s)
        self.that.flush()
        self.duoi.append(s)
        dai = sum(map(len, self.duoi))
        while dai > TRAN_NHAT_KY and len(self.duoi) > 1:
            dai -= len(self.duoi[0])
            self.bo += len(self.duoi.pop(0))
        return len(s)

    def noi_dung(self):
        than = "".join(self.duoi)[-TRAN_NHAT_KY:]
        return (f"[CAT {self.bo} ky tu dau]\n" if self.bo else "") + than


def _chay_muc_dich(khoa, x, nen_sp_dat, lan_lai, du=False):
    """Mot muc -> trang thai trong `TRANG_THAI_KQ`. Ghi lan chay lai vao `lan_lai`."""
    global TU_KIEM, chay_mot_mutant
    loai = khoa.split(":", 1)[0]
    if loai == "ca":
        goc_tk = TU_KIEM
        TU_KIEM = [x]
        try:
            return "failed" if chay_tu_kiem() else "passed"
        finally:
            TU_KIEM = goc_tk
    if loai == "tk":
        ra = io.StringIO()
        with contextlib.redirect_stdout(ra):
            g, h, kd = chay_dot_bien_tu_kiem([x], chi_dich=not du)
        print(ra.getvalue(), end="")
        if (g, h, kd) == (1, 0, 0):
            return "passed"
        return "not_measured" if kd else ("inconclusive" if "TIN DUNG GIA" in ra.getvalue() else "failed")
    if not nen_sp_dat:
        return "not_run"
    goc_m = chay_mot_mutant

    def dem(ban_sao, ten, dich):
        kq = goc_m(ban_sao, ten, dich)
        lan_lai.append(kq[2] - 1)
        return kq
    chay_mot_mutant = dem
    try:
        dat, kg, kd = chay_dot_bien([x])
    finally:
        chay_mot_mutant = goc_m
    return "passed" if (dat, kg, kd) == (1, 0, 0) else ("not_measured" if kd else "failed")


def chay_manh_dich(k: int, n: int, ra, du=False) -> int:
    """Mot manh (targeted, hoac `du` = full_mutant_audit). LUON ghi bien nhan (ke ca khi DO); rc that."""
    global _TRAN_GIAY_CON
    import time as _thoi_gian
    ra = Path(ra).resolve()
    job = _bat_dau_do_ram()
    t0, bat_dau = _thoi_gian.monotonic(), _iso_utc()
    bam_dau = (_bam(__file__), _bam(TOOL))     # nguon doi GIUA luot => manh DO (khong tron hai ban)
    nhat_ky = _GhiCoTran(sys.stdout)
    che_do = CHE_DO_DU if du else CHE_DO_DICH
    phan = phan_hoach_dich(n, du)[k]
    ket_qua = {khoa: "not_run" for khoa, _ in phan}
    ca_dich = {khoa: sorted(set(x[1])) for khoa, x in phan if khoa[:3] in ("tk:", "db:")}
    lan_lai, tien_do, rc = [], "chua bat dau", 1
    _TRAN_GIAY_CON = TRAN_GIAY_CON_DU if du else TRAN_GIAY_CON_DICH
    try:
        with contextlib.redirect_stdout(nhat_ky):
            print(f"{che_do} MANH {k}/{n}: {len(phan)} muc" + ("" if du else " — KHONG phai full mutant audit"))
            nen_sp_dat = True
            if any(khoa.startswith("db:") for khoa in ket_qua):
                tien_do = f"MANH {k}/{n} nen san pham T1..T8"
                print(f"TIEN DO {tien_do}")
                nen_sp_dat = not chay_ca(None)
            for i, (khoa, x) in enumerate(phan, 1):
                dich = ",".join(ca_dich.get(khoa, [khoa[3:]]))
                tien_do = f"MANH {k}/{n} [{i}/{len(phan)}] {khoa} ca={dich}"
                t = _thoi_gian.monotonic()
                print(f"TIEN DO {tien_do}")
                ket_qua[khoa] = _chay_muc_dich(khoa, x, nen_sp_dat, lan_lai, du)
                print(f"KET QUA {khoa}: {ket_qua[khoa]} ({_thoi_gian.monotonic() - t:.1f}s)")
            rc = 0 if nen_sp_dat and all(v == "passed" for v in ket_qua.values()) else 1
            print(f"{che_do} MANH {k}/{n}: rc={rc} · passed "
                  f"{sum(v == 'passed' for v in ket_qua.values())}/{len(ket_qua)}")
    finally:
        _TRAN_GIAY_CON = None
        ram, pham_vi = _ram_dinh_mb(job)
        bam_test = bam_dau[0]
        if (_bam(__file__), _bam(TOOL)) != bam_dau:
            rc, tien_do = 1, f"NGUON DOI GIUA LUOT — {tien_do}"
        ra.parent.mkdir(parents=True, exist_ok=True)
        ra.write_text(json.dumps({
            "phien_ban": PHIEN_BAN_DICH, "che_do": che_do, "manh": k, "so_manh": n,
            "head": _git_head(), "sha256_test": bam_test, "sha256_tool": bam_dau[1],
            "rc": rc, "bat_dau": bat_dau, "ket_thuc": _iso_utc(),
            "giay": round(_thoi_gian.monotonic() - t0, 2), "ram_dinh_mb": ram, "pham_vi_ram": pham_vi,
            "so_lan_chay_lai": sum(lan_lai), "tien_do": tien_do, "ca_dich": ca_dich,
            "ket_qua": ket_qua, "nhat_ky_duoi": nhat_ky.noi_dung()}, ensure_ascii=False), encoding="utf-8")
    return rc


def _so_huu_han(v) -> bool:
    """int/float (KHONG bool) va huu han — NaN, Infinity, -Infinity deu sai. int luon huu han; KHONG goi
    math.isfinite tren int vi int json khong lo (10**400) nem OverflowError thay vi ra mot dong loi."""
    return type(v) is int or (type(v) is float and math.isfinite(v))


# WP748 r22 F01 (Codex 03c4f6be) — moc `bat_dau`/`ket_thuc` tung chi can la CHUOI khac rong va tran duong gang chi do
# bang `giay` khai rieng: moc "invalid", moc dao nguoc, hay khoang 900 s voi `giay=0` deu ra DAT. Moc phai la DUNG
# dang `_iso_utc` (UTC, mili giay, hau to Z); `ket_thuc - bat_dau` khong am va lech `giay` (monotonic) toi da
# LECH_MOC_GIAY — du cho lam tron va chinh dong ho nho, lech hon thi fail-closed chu khong doan.
_MOC_ISO_UTC = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z", re.ASCII)   # chi chu so ASCII (Codex l22 F04)
LECH_MOC_GIAY = 5.0


def _doc_moc_utc(v):
    import datetime
    if not isinstance(v, str) or not _MOC_ISO_UTC.fullmatch(v):
        return None  # WP748 r22 F01 sai dinh dang
    try:
        return datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        return None


def _loi_gop_dich(thu_muc: Path, head=None, du=False):
    """`(loi, doc)` — MOI dieu kien la mot dong loi; rong <=> moi manh, moi muc deu duong."""
    doc = []
    for tep in sorted(Path(thu_muc).glob("*.json")):
        try:
            doc.append(json.loads(tep.read_text(encoding="utf-8")))
        except OSError as e:
            _ghi_ha_tang(e)                       # WP748 r22: diem nuot _loi_gop_dich (r546 qua r554)
            return [f"{tep.name}: {type(e).__name__}: {e}"], []
        except ValueError as e:
            return [f"{tep.name}: {type(e).__name__}: {e}"], []
    if not doc:
        return ["khong co bien nhan manh nao"], []
    if any(not isinstance(x, dict) or set(x) != _KHOA_DICH for x in doc):
        return ["bien nhan sai khoa"], []
    if any(type(x[c]) is not int for x in doc for c in ("phien_ban", "manh", "so_manh", "rc", "so_lan_chay_lai")):
        return ["phien_ban/manh/so_manh/rc/so_lan_chay_lai phai la int"], []
    if any(x["phien_ban"] != PHIEN_BAN_DICH or x["che_do"] != (CHE_DO_DU if du else CHE_DO_DICH) for x in doc):
        return ["phien_ban/che_do lech (bien nhan full audit KHONG thay duoc targeted, va nguoc lai)"], []
    n = doc[0]["so_manh"]
    if n not in range(2, 9) or any(x["so_manh"] != n for x in doc) or sorted(x["manh"] for x in doc) != list(range(n)):
        return [f"can dung N manh 0..N-1 cung N: {[(x['manh'], x['so_manh']) for x in doc]}"], []
    loi = []
    head = head if head is not None else _git_head()
    if head is None:
        loi.append("KHONG DO DUOC head hien tai")
    bam = [_bam(__file__), _bam(TOOL)]
    phan = phan_hoach_dich(n, du)
    for x in doc:
        m = x["manh"]
        if x["head"] != head:
            loi.append(f"manh {m}: head {x['head']} != {head} (cu/lech)")
        if (x["sha256_test"], x["sha256_tool"]) != tuple(bam):
            loi.append(f"manh {m}: sha256 lech tep DANG CHAY")
        if x["rc"] != 0:
            loi.append(f"manh {m}: rc={x['rc']}")
        if x["so_lan_chay_lai"] < 0:
            loi.append(f"manh {m}: so_lan_chay_lai am")
        # WP748 r19 (Codex P2: giay=NaN + ram=NaN o manh 0 => 0 loi) — json.loads nhan NaN/Infinity,
        # moi so sanh voi NaN la False nen `< 0`/`<= 0` khong bao gio ban: doi so HUU HAN truoc khi so.
        if not _so_huu_han(x["giay"]) or x["giay"] < 0:
            loi.append(f"manh {m}: giay khong hop le")
        if not _so_huu_han(x["ram_dinh_mb"]) or x["ram_dinh_mb"] <= 0:
            loi.append(f"manh {m}: RAM KHONG DO DUOC ({x['pham_vi_ram']})")
        if not all(isinstance(x[c], str) and x[c] for c in ("bat_dau", "ket_thuc", "tien_do", "pham_vi_ram")):
            loi.append(f"manh {m}: thieu moc thoi gian/tien do")
        moc = [_doc_moc_utc(x[c]) for c in ("bat_dau", "ket_thuc")]
        if None in moc:
            loi.append(f"manh {m}: moc thoi gian sai dinh dang {x['bat_dau']!r}/{x['ket_thuc']!r}")
            moc = None
        if moc and moc[1] < moc[0]:   # WP748 r22 F01 dao nguoc
            loi.append(f"manh {m}: ket_thuc truoc bat_dau")
        # so sanh KHOANG (khong tru): int json khong lo (10**400) tru float se nem OverflowError, so sanh thi khong
        khoang = (moc[1] - moc[0]).total_seconds() if moc else None
        if moc and _so_huu_han(x["giay"]) and not khoang - LECH_MOC_GIAY <= x["giay"] <= khoang + LECH_MOC_GIAY:   # WP748 r22 F01 lech
            loi.append(f"manh {m}: khoang moc {khoang}s lech giay qua {LECH_MOC_GIAY}s")
        if not isinstance(x["nhat_ky_duoi"], str) or len(x["nhat_ky_duoi"]) > TRAN_NHAT_KY + 64:
            loi.append(f"manh {m}: nhat ky vang hoac vuot tran")
        mong = {khoa: x2 for khoa, x2 in phan[m]}
        kq = x["ket_qua"] if isinstance(x["ket_qua"], dict) else {}
        if set(kq) != set(mong):
            loi.append(f"manh {m}: thanh vien lech phan hoach (thieu {sorted(set(mong) - set(kq))[:3]},"
                       f" thua {sorted(set(kq) - set(mong))[:3]})")
        xau = sorted(f"{khoa}={v}" for khoa, v in kq.items() if v != "passed")
        if xau:
            loi.append(f"manh {m}: {len(xau)} muc khong passed: {xau[:5]}")
        if any(v not in TRANG_THAI_KQ for v in kq.values()):
            loi.append(f"manh {m}: trang thai ngoai tu vung {TRANG_THAI_KQ}")
        dich_mong = {khoa: sorted(set(x2[1])) for khoa, x2 in mong.items() if khoa[:3] in ("tk:", "db:")}
        if x["ca_dich"] != dich_mong:
            loi.append(f"manh {m}: bang ca dich lech bang khai")
    hop = [khoa for x in doc if isinstance(x["ket_qua"], dict) for khoa in x["ket_qua"]]
    tat_ca = [k for k, _, _ in _muc_dich(du)]
    if sorted(hop) != sorted(tat_ca):
        loi.append(f"hop cac manh != tron {len(tat_ca)} muc (thay {len(hop)}, phan biet {len(set(hop))})")
    duong_gang = max((x["giay"] for x in doc if _so_huu_han(x["giay"])), default=None)
    if duong_gang is None or (not du and duong_gang > TRAN_DUONG_GANG_GIAY):
        loi.append(f"duong gang {duong_gang}s vuot tran {TRAN_DUONG_GANG_GIAY}s")
    loi += _loi_nhom_bat_buoc()                   # WP748 r20 (Codex R2): cung chot voi `_loi_gop`
    return loi, doc


def _phan_chung_gop_dich(chi=None) -> list:
    """Phep gom phai CO RANG truoc khi duoc tin: bo bien nhan TONG HOP hop le => 0 loi; MOI hong
    MOT dieu kien => co loi. Tra danh sach phan chung LOT (rong <=> moi chot co rang).

    WP748 r22 — `chi` (tap ten phan chung) cho ca do MOT lop chot: chi chay bo hop le + cac phan chung ay, BO bang
    nhom (chot nhom la viec cua r552). `gop_dich` luon goi day du (`chi=None`)."""
    n, head, bam = 8, "a" * 40, (_bam(__file__), _bam(TOOL))

    def bo_hop_le(du=False):
        phan = phan_hoach_dich(n, du)             # tinh LAI moi lan: ca bang-hong (duoi) doi bang truoc khi dung bo
        return [{"phien_ban": PHIEN_BAN_DICH, "che_do": CHE_DO_DU if du else CHE_DO_DICH, "manh": m, "so_manh": n, "head": head,
                 "sha256_test": bam[0], "sha256_tool": bam[1], "rc": 0,
                 "bat_dau": "2026-01-01T00:00:00.000Z", "ket_thuc": "2026-01-01T00:05:00.000Z",
                 # manh 0 dung int, cac manh khac float — bo hop le phai nhan CA HAI kieu so (WP748 r19)
                 "giay": 300.0 if m else 300, "ram_dinh_mb": 100.0 if m else 100, "pham_vi_ram": "tong hop", "so_lan_chay_lai": 0,
                 "tien_do": "xong", "ca_dich": {k: sorted(set(x[1])) for k, x in phan[m] if k[:3] in ("tk:", "db:")},
                 "ket_qua": {k: "passed" for k, _ in phan[m]}, "nhat_ky_duoi": "ok"} for m in range(n)]

    def dat(b, k, v):
        b[k] = v

    def kq(b, khoa, v):
        b["ket_qua"][khoa] = v

    k0 = next(iter(bo_hop_le()[0]["ket_qua"]))
    k_tk = next(k for k in bo_hop_le()[1]["ket_qua"] if k.startswith("tk:"))
    hong = {
        "thieu-manh": lambda bo: bo.pop(),
        "rc-1": lambda bo: dat(bo[2], "rc", 1),
        "muc-failed": lambda bo: kq(bo[0], k0, "failed"),
        "muc-not_measured": lambda bo: kq(bo[0], k0, "not_measured"),
        "muc-inconclusive": lambda bo: kq(bo[0], k0, "inconclusive"),
        "muc-skipped": lambda bo: kq(bo[0], k0, "skipped"),
        "muc-not_run": lambda bo: kq(bo[0], k0, "not_run"),
        "muc-ngoai-tu-vung": lambda bo: kq(bo[0], k0, "killed"),
        "thieu-muc": lambda bo: bo[0]["ket_qua"].pop(k0),
        "muc-sang-manh-khac": lambda bo: kq(bo[1], k0, bo[0]["ket_qua"].pop(k0)),
        "muc-la": lambda bo: kq(bo[0], "tk:khong-co-that", "passed"),
        "head-cu": lambda bo: dat(bo[3], "head", "b" * 40),
        "head-vang": lambda bo: dat(bo[3], "head", None),
        "sha-test-lech": lambda bo: dat(bo[4], "sha256_test", "0" * 64),
        "sha-tool-lech": lambda bo: dat(bo[4], "sha256_tool", "0" * 64),
        "che-do-full": lambda bo: dat(bo[5], "che_do", "full_mutant_audit"),
        "phien-ban": lambda bo: dat(bo[5], "phien_ban", PHIEN_BAN_DICH + 1),
        "so-manh-lech": lambda bo: dat(bo[6], "so_manh", 7),
        "manh-trung": lambda bo: dat(bo[7], "manh", 6),
        "duong-gang-vuot": lambda bo: dat(bo[1], "giay", TRAN_DUONG_GANG_GIAY + 0.5),
        "ram-vang": lambda bo: dat(bo[1], "ram_dinh_mb", None),
        # WP748 r19 — so KHONG huu han di qua json (NaN/Infinity/-Infinity), dat o manh 0 (manh dau cua max)
        "giay-ram-nan-manh-0": lambda bo: (dat(bo[0], "giay", float("nan")), dat(bo[0], "ram_dinh_mb", float("nan"))),
        "giay-nan": lambda bo: dat(bo[0], "giay", float("nan")),
        "giay-inf": lambda bo: dat(bo[0], "giay", float("inf")),
        "giay-am-inf": lambda bo: dat(bo[0], "giay", float("-inf")),
        "ram-nan": lambda bo: dat(bo[0], "ram_dinh_mb", float("nan")),
        "ram-inf": lambda bo: dat(bo[0], "ram_dinh_mb", float("inf")),
        "giay-int-khong-lo": lambda bo: dat(bo[0], "giay", 10 ** 400),
        "chay-lai-am": lambda bo: dat(bo[1], "so_lan_chay_lai", -1),
        "rc-bool": lambda bo: dat(bo[1], "rc", False),
        "tien-do-rong": lambda bo: dat(bo[1], "tien_do", ""),
        "nhat-ky-vuot-tran": lambda bo: dat(bo[1], "nhat_ky_duoi", "x" * (TRAN_NHAT_KY + 100)),
        "ca-dich-lech": lambda bo: bo[1]["ca_dich"].update({k_tk: ["r501"] if bo[1]["ca_dich"][k_tk] != ["r501"] else ["r502"]}),
        "thua-khoa": lambda bo: dat(bo[1], "thua", 1),
        # WP748 r22 F01 — moi chot moc mot phan chung rieng, dung sao cho CHI chot ay ban duoc (r554 + dot bien rieng)
        "moc-sai-dinh-dang": lambda bo: (dat(bo[0], "bat_dau", "invalid"), dat(bo[0], "ket_thuc", "invalid"),
                                         dat(bo[0], "giay", 0)),
        "moc-dao-nguoc": lambda bo: (dat(bo[0], "bat_dau", "2026-01-01T00:00:01.000Z"),
                                     dat(bo[0], "ket_thuc", "2026-01-01T00:00:00.000Z"), dat(bo[0], "giay", 0)),
        "moc-lech-giay": lambda bo: (dat(bo[0], "ket_thuc", "2026-01-01T00:15:00.000Z"), dat(bo[0], "giay", 0)),
    }
    if chi is not None:
        if not set(chi) <= set(hong):
            raise ValueError(f"phan chung la: {sorted(set(chi) - set(hong))}")
        hong = {k: v for k, v in hong.items() if k in chi}
    lot = []
    with tempfile.TemporaryDirectory() as td:
        for ten, sua in [("hop-le", None)] + list(hong.items()):
            d = Path(td) / ten
            d.mkdir()
            bo = bo_hop_le()
            if sua is not None:
                sua(bo)
            for i, b in enumerate(bo):
                (d / f"manh-{i}.json").write_text(json.dumps(b), encoding="utf-8")
            loi, _ = _loi_gop_dich(d, head=head)
            if bool(loi) != (sua is not None):
                lot.append(f"{ten}: {'CHAP NHAN' if sua else loi[:2]}")
            if sua is None and not _loi_gop_dich(d, head=head, du=True)[0]:
                lot.append("hop-le-targeted: gom full_mutant_audit CHAP NHAN bien nhan targeted")
        # WP748 r20 (Codex WP748-R2) — BANG bat buoc hong ma bien nhan van khop bang ay: ca hai che do
        # phai tu choi, va tu choi DUNG vi chot nhom (moi loi khac la chet vi ly do vo can, khong tinh).
        # Bo bien nhan dung SAU khi doi bang, nen phan hoach/thanh vien van khop — chi chot nhom con ban.
        if chi is not None:
            return lot, 1 + len(hong), 1
        g = globals()
        bang_hong = [
            ("nhom-thieu-dot-bien", "DOT_BIEN_TU_KIEM", [x for x in DOT_BIEN_TU_KIEM if "r549" not in x[1]]),
            ("nhom-bat-buoc-la", "NHOM_BAT_BUOC", NHOM_BAT_BUOC | {"r999"}),
            # dung SAN_NHOM - 1 ca CO THAT (khong `thieu`), khong ghi cung ten: them ca bat buoc khong lam ca nay mat rang
            ("nhom-duoi-san", "NHOM_BAT_BUOC", frozenset(sorted(NHOM_BAT_BUOC)[:SAN_NHOM - 1])),
        ]
        for du in (False, True):
            for ten, bien, gia_tri in [("hop-le", None, None)] + bang_hong:
                cu = g[bien] if bien else None
                try:
                    if bien:
                        g[bien] = gia_tri
                    d = Path(td) / f"bang-{'du' if du else 'dich'}-{ten}"
                    d.mkdir()
                    for i, b in enumerate(bo_hop_le(du)):
                        (d / f"manh-{i}.json").write_text(json.dumps(b), encoding="utf-8")
                    loi, _ = _loi_gop_dich(d, head=head, du=du)
                finally:
                    if bien:
                        g[bien] = cu
                nhan = f"{ten}{' (du)' if du else ''}"
                if bien is None and loi:
                    lot.append(f"{nhan}: {loi[:2]}")
                elif bien is not None and not (loi and all(x.startswith("nhom bat buoc") for x in loi)):
                    lot.append(f"{nhan}: {'CHAP NHAN' if not loi else 'chet vi ly do vo can ' + repr(loi[:2])}")
    return lot, 1 + len(hong) + 2 * (1 + len(bang_hong)), 3


def gop_dich(thu_muc, du=False) -> int:
    """`--gop-dich`/`--gop-du <thu muc>`: DAT khi DU N manh, DUNG head, MOI muc passed (+ duong gang <= tran neu targeted)."""
    lot, tong, hop_le = _phan_chung_gop_dich()
    for x in lot:
        print(f"GOP DICH: PHAN CHUNG LOT — {x}")
    if lot:
        print(f"{CHE_DO_DICH}: DO — phep gom KHONG co rang")
        return 1
    print(f"GOP DICH: phan chung {tong}/{tong} dung ({hop_le} hop le + {tong - hop_le} hong)")
    loi, doc = _loi_gop_dich(Path(thu_muc), du=du)
    for x in loi:
        print(f"GOP DICH: LOI — {x}")
    if loi:
        print(f"{CHE_DO_DU}: DO" if du else f"{CHE_DO_DICH}: DO — KHONG phai full mutant audit")
        return 1
    if du:
        print(f"{CHE_DO_DU} GOP {len(doc)}/{len(doc)} manh · head {doc[0]['head']} · ca nen {len(TU_KIEM)}/{len(TU_KIEM)}"
              f" · tu dot bien (DU 52 ca moi con) {len(DOT_BIEN_TU_KIEM)}/{len(DOT_BIEN_TU_KIEM)}"
              f" · dot bien san pham {len(DOT_BIEN)}/{len(DOT_BIEN)} · manh dai nhat {max(x['giay'] for x in doc)}s")
        print(f"{CHE_DO_DU}: DAT")
        return 0
    dem = lambda tien_to: sum(k.startswith(tien_to) for x in doc for k in x["ket_qua"])   # noqa: E731
    print(f"{CHE_DO_DICH} GOP {len(doc)}/{len(doc)} manh · head {doc[0]['head']}")
    print(f"CA NEN: {dem('ca:')}/{len(TU_KIEM)} passed · TU DOT BIEN (chi ca dich): {dem('tk:')}/"
          f"{len(DOT_BIEN_TU_KIEM)} giet · DOT BIEN SAN PHAM: {dem('db:')}/{len(DOT_BIEN)} giet")
    print(f"DUONG GANG: {max(x['giay'] for x in doc)}s / tran {TRAN_DUONG_GANG_GIAY}s · RAM dinh "
          f"{max(x['ram_dinh_mb'] for x in doc)} MB · chay lai {sum(x['so_lan_chay_lai'] for x in doc)}")
    print(f"{CHE_DO_DICH}: DAT — KHONG phai full mutant audit; full_mutant_audit van BAT BUOC truoc merge/land/release")
    return 0


def main() -> int:
    # WP748 r16 — con cua targeted_mutant_gate: chi chay ca dich (POP truoc moi thu, khong thua ke).
    if TU_KIEM_CHI_CA_ENV in os.environ:
        global TU_KIEM
        chi_ca = os.environ.pop(TU_KIEM_CHI_CA_ENV)
        if not os.environ.get("NHANH_DON_DUOC_CHI_TU_KIEM"):
            print(f"{TU_KIEM_CHI_CA_ENV}: LOI — chi hop le cung NHANH_DON_DUOC_CHI_TU_KIEM")
            return 2
        try:
            TU_KIEM = _loc_tu_kiem(chi_ca)
        except ValueError as e:
            print(f"TU KIEM CHI CA: LOI — {e}")
            return 2
        return 1 if chay_tu_kiem() else 0
    if DICH_ENV in os.environ or DICH_RA_ENV in os.environ or DICH_DU_ENV in os.environ:
        gt_dich, ra_dich = os.environ.pop(DICH_ENV, None), os.environ.pop(DICH_RA_ENV, None)
        co_du = os.environ.pop(DICH_DU_ENV, None)
        try:
            k, n = doc_dich(gt_dich)
            if ra_dich in (None, ""):
                raise ValueError(f"thieu {DICH_RA_ENV}")
            if co_du not in (None, "1"):
                raise ValueError(f"{DICH_DU_ENV}={co_du!r}: chi duoc vang hoac '1'")
            phan_hoach_dich(n, co_du == "1")
        except ValueError as e:
            print(f"DICH: LOI — {e}")
            return 2
        return chay_manh_dich(k, n, ra_dich, co_du == "1")
    # #661 M1 — POP truoc moi thu (con chep `os.environ` => khong thua ke bien manh); sai hinh => rc 2, KHONG chay gi.
    if MANH_ENV in os.environ or MANH_RA_ENV in os.environ:
        gia_tri, ra = os.environ.pop(MANH_ENV, None), os.environ.pop(MANH_RA_ENV, None)
        try:
            k, n = doc_manh(gia_tri)
            if not ra:
                raise ValueError(f"thieu {MANH_RA_ENV}")
            db, dbtk = phan_hoach(DOT_BIEN, k, n), phan_hoach(DOT_BIEN_TU_KIEM, k, n)
        except ValueError as e:
            print(f"MANH: LOI — {e}")
            return 2
        return chay_manh(k, n, db, dbtk, ra)
    if os.environ.get("NHANH_DON_DUOC_CHI_TU_KIEM"):
        return 1 if chay_tu_kiem() else 0
    duong = os.environ.get(KENH_ENV)
    khung = None
    if duong:
        khung = KhungPhat(Path(duong), os.environ[DAU_PHIEN_ENV],
                          os.environ[MUTANT_ENV], int(os.environ[LAN_THU_ENV]))
    do = chay_ca(khung)
    tong = len(CA)
    rc = 1 if do else 0
    if khung is not None:
        khung.dong_luot(rc)
    if do:
        print(f"{tong - len(do)}/{tong}")
        return 1
    if os.environ.get("NHANH_DON_DUOC_KHONG_DOT_BIEN"):
        print(f"{tong}/{tong}")
        return 0
    dat, khong_giet, khong_do = chay_dot_bien()
    tu_kiem_do = chay_tu_kiem()
    tk_giet, tk_hong, tk_khong_do = chay_dot_bien_tu_kiem()
    print(f"TU DOT BIEN KHONG DO DUOC: {tk_khong_do}")
    if tk_khong_do:
        return 1
    nhom_co_dot_bien = {c for _, dich, _, _ in DOT_BIEN_TU_KIEM for c in dich}
    da_chay = {t for t, _, _ in TU_KIEM}
    thieu = (NHOM_BAT_BUOC - nhom_co_dot_bien) | (NHOM_BAT_BUOC - da_chay)
    print(f"TU KIEM co dot bien rieng: {len(nhom_co_dot_bien & NHOM_BAT_BUOC)}/{len(NHOM_BAT_BUOC)}"
          f" nhom bat buoc · dot bien giet {tk_giet}/{len(DOT_BIEN_TU_KIEM)}")
    print(f"{tong}/{tong}")
    print(f"MUTANT: giet = {dat} · khong giet = {khong_giet} · khong do duoc = {khong_do}"
          f" / tong {len(DOT_BIEN)}")
    # M2 — ba so hang phai CONG DUNG tong. Kiem SO HANG, khong kiem quan he:
    # quan he "tong = 10" song sot qua moi troi so.
    if dat + khong_giet + khong_do != len(DOT_BIEN):
        print("LOI: ba so hang khong cong dung tong")
        return 1
    # M3 — KHONG DO DUOC KHONG bao gio thanh GIET; no lam suite DO.
    # A6 — ca nao KHONG co dot bien rieng lam no do thi KHONG duoc tinh vao so nhom.
    # F03 (luot 3) — phai kiem CA `tk_giet`: do gia cua ca cu luon bu tong nen
    # `tk_giet` chua bao gio duoc nhin toi, va mot bo tra `(0, 0)` van qua cong.
    if thieu or len(NHOM_BAT_BUOC) < SAN_NHOM or tk_hong or tk_giet != len(DOT_BIEN_TU_KIEM):
        if thieu:
            print(f"LOI: nhom bat buoc THIEU (chua chay hoac chua co dot bien): {sorted(thieu)}")
        return 1
    return 0 if (dat == len(DOT_BIEN) and not tu_kiem_do) else 1
if __name__ == "__main__":
    if sys.argv[1:2] == ["--gop-dich"]:     # WP748 r16: gom targeted_mutant_gate
        raise SystemExit(gop_dich(sys.argv[2]) if len(sys.argv) == 3 else 2)
    if sys.argv[1:2] == ["--gop-du"]:       # WP748 r16: gom full_mutant_audit
        raise SystemExit(gop_dich(sys.argv[2], du=True) if len(sys.argv) == 3 else 2)
    if sys.argv[1:2] == ["--gop"]:          # #661 M2: dung MOT doi so
        raise SystemExit(gop(sys.argv[2]) if len(sys.argv) == 3 else 2)
    raise SystemExit(main())
