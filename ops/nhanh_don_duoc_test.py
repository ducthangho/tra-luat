#!/usr/bin/env python3
"""Phan chung bang kho bare that, kem bang dot bien tren ban sao tam."""
from __future__ import annotations
import contextlib
import importlib.util
import io
import json
import os
import secrets
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TOOL = HERE / "nhanh_don_duoc.py"

# ---- M1: tin hieu "chot cua CHINH ca nay hong" -------------------------------
# Ma HA TANG (`run`, `nap_tool`, `chay_dot_bien`) nem `AssertionError` TRAN va
# KHONG bao gio nem lop nay. Nho vay bo cham phan biet duoc "dich chet dung chot"
# voi "mot ca chet vi loi vo can" — thu ma `AssertionError` tran KHONG phan biet
# duoc (da tra gia: CASE T4 chet vi `rc=128: git commit -m A`).
class TinHieuChotCa(AssertionError):
    pass


def chot(dieu_kien, ten_ca: str = "") -> None:
    if not dieu_kien:
        raise TinHieuChotCa(f"chot cua ca {ten_ca} that bai")


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
    """Doc kenh va phan BA trang thai. Moi nhanh tu choi deu neu ly do.

    Chi nhan ban ghi neo DUNG luot vua phong: (dau_phien, mutant, lan_thu).
    Thieu ban ghi dong luot => KHONG DO DUOC (mot luot bi giet giua chung van co
    the de lai du so ban ghi).
    """
    if not duong.exists():
        return KHONG_DO_DUOC, "kenh khong ton tai"
    neo = {"dau_phien": dau_phien, "mutant": mutant, "lan_thu": lan_thu}
    theo_ca, chi_tiet, dong = {}, {}, None
    for dong_txt in duong.read_text(encoding="utf-8").splitlines():
        if not dong_txt.strip():
            continue
        try:
            r = json.loads(dong_txt)
        except json.JSONDecodeError:
            return KHONG_DO_DUOC, "ban ghi khong phai JSON"
        if any(r.get(k) != v for k, v in neo.items()):
            return KHONG_DO_DUOC, f"ban ghi khong neo dung luot: {r.get('ca') or 'dong_luot'}"
        if r.get("dong_luot"):
            dong = r
            continue
        ca = r.get("ca")
        if ca is None:
            return KHONG_DO_DUOC, "ban ghi thieu ten ca"
        if ca in theo_ca:
            return KHONG_DO_DUOC, f"ban ghi TRUNG cho ca {ca}"
        theo_ca[ca] = r.get("nhan")
        chi_tiet[ca] = r.get("chi_tiet", "")
    if dong is None:
        return KHONG_DO_DUOC, "thieu ban ghi dong luot"
    # F01 — `rc` la MOT CHIEU NEO, khong phai trang tri. Thieu chieu nay thi mot
    # luot con bao "xong rc=0" trong khi tien trinh that thoat 1 van duoc nhan.
    if not isinstance(dong.get("rc"), int):
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
    do_chot = {t for t, n in theo_ca.items() if n == NHAN_DO_CHOT}
    if do_chot == set(dich):
        return GIET, ""
    return KHONG_GIET, f"tap ca do chot {sorted(do_chot)} != dich {sorted(dich)}"
def run(args: list[str], cwd: Path, check: bool = True, env: dict[str, str] | None = None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env, check=False)
    if check and p.returncode:
        raise AssertionError(f"rc={p.returncode}: {' '.join(args)}\n{p.stdout}\n{p.stderr}")
    return p
def viet(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
def kho_bare(*, mac_dinh: str = "main", a: bool = False, b: bool = False,
             c_mot: bool = False, c_hai: bool = False):
    td = tempfile.TemporaryDirectory()
    root, remote, work = Path(td.name), Path(td.name) / "remote.git", Path(td.name) / "work"
    run(["git", "init", "--bare", str(remote)], root)
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
            do.append(ten)
            print(f"CASE {ten}: DO — {type(exc).__name__}: {exc}")
            if khung is not None:
                khung.phat(NHAN_DO_KHAC, f"{type(exc).__name__}: {exc}")
    return do
def chay_dot_bien():
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
        for ten, dich, neo, thay in DOT_BIEN:
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
            tep.write_text(text.replace(neo, thay), encoding="utf-8", newline="\n")
            trang_thai, ly_do, so_lan = chay_mot_mutant(ban_sao, ten, dich)
            so_ca = len(dich)
            if trang_thai == GIET:
                dat += 1
                print(f"MUTANT {ten} | {','.join(dich)} | {so_ca}/{so_ca}")
            elif trang_thai == KHONG_DO_DUOC:
                khong_do += 1
                print(f"MUTANT {ten} | {','.join(dich)} | KHONG DO DUOC (sau {so_lan} lan): {ly_do}")
            else:
                khong_giet += 1
                print(f"MUTANT {ten} | {','.join(dich)} | 0/{so_ca}: {ly_do}")
    return dat, khong_giet, khong_do


def chay_mot_mutant(ban_sao: Path, ten: str, dich):
    """M3 — `KHONG DO DUOC` thi chay lai DUNG MOT lan. Khong bao gio qua 2.

    Tra `(trang_thai, ly_do, so_lan_da_goi)`. So lan la de ca tu kiem DEM duoc,
    chu khong doc ma thoat — nep da tra gia o `ops-don-ref` (40/40 trong khi mot
    dot bien xoa han lenh pha van qua).
    """
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
        p = run([sys.executable, Path(__file__).name], ban_sao, check=False, env=env)
        trang_thai, ly_do = doc_kenh(kenh, dau_phien, ten, lan_thu, dich, p.returncode)
        if trang_thai == KHONG_DO_DUOC:
            # F09 — giu chi tiet ngoai le, khong chi giu ten ca: chinh chi tiet ay
            # la du kien can de chan doan "khong do duoc" o lan thu hai.
            ly_do = f"{ly_do} | rc_con={p.returncode} | stderr[-200:]={p.stderr[-200:]!r}"
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
    m.chay_dot_bien_tu_kiem = lambda: (tkg, tk_hong)
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
    loai = []
    try:
        m.nap_tool()
    except Exception as exc:
        loai.append(type(exc).__name__)
    chot(loai == ["AssertionError"], "r502")

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
        loai2.append(type(exc).__name__)
    chot(loai2 == ["AssertionError"], "r502")


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
    ph_that, ph_khac = sinh_dau_phien(), sinh_dau_phien()
    k = _kenh_tam(_du_ca(ph_khac, {"T1": NHAN_DO_CHOT})
                  + [_ban_ghi(ph_khac, dong_luot=True, rc=1)], d)
    tt, _ = doc_kenh(k, ph_that, "m", 1, ("T1",))
    chot(tt == KHONG_DO_DUOC, "r508")


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
    chot(a != b and dem["n"] == 2 and len(a) >= 32, "r509")
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

    def nguon(gia_tri):
        def f(n=None):
            xin.append(n)
            return gia_tri
        return f

    goc_hex = "".join(format((i * 7 + 3) % 256, "02x") for i in range(16))
    ra = {}
    for ten_v, v in (("goc", goc_hex),
                     ("khac_byte_dau", "ff" + goc_hex[2:]),
                     ("khac_byte_cuoi", goc_hex[:-2] + "ff")):
        xin.clear()
        secrets.token_hex = nguon(v)
        try:
            ra[ten_v] = sinh_dau_phien()
        finally:
            secrets.token_hex = that
        chot(xin == [16], "r509")                   # phai XIN du 16 byte, moi luot
    chot(ra["goc"] != ra["khac_byte_dau"]
         and ra["goc"] != ra["khac_byte_cuoi"], "r509")
    chot(goc_hex in ra["goc"], "r509")              # entropy phai CO MAT trong dau
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
        "tu-dot-bien-hong":    dict(dat=n, kgiet=0, kdo=0, tk_hong=1),
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
    kich = [(m.GIET, 1), (m.KHONG_GIET, 1), (m.KHONG_GIET, 1),
            (m.KHONG_DO_DUOC, 2), (m.KHONG_DO_DUOC, 2), (m.KHONG_DO_DUOC, 2)]
    m.DOT_BIEN = m.DOT_BIEN[:len(kich)]

    def mot_mutant(ban_sao, ten, dich):
        tt, so_lan = kich.pop(0)
        return (tt, "ly do gia", so_lan)

    m.chay_mot_mutant = mot_mutant
    with _git_config_sach(), contextlib.redirect_stdout(io.StringIO()):
        ra = m.chay_dot_bien()
    chot(ra == (1, 2, 3), "r514")


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
    ket = {
        "chuan":   doc_kenh(k0, ph, "m", 1, ("T1",), 0)[0],
        "mutant":  doc_kenh(k1, ph, "m", 1, ("T1",), 0)[0],
        "lan_thu": doc_kenh(k2, ph, "m", 1, ("T1",), 0)[0],
        # cung mot kenh k0, chi rc cua TIEN TRINH lech so voi rc kenh khai
        "rc":      doc_kenh(k0, ph, "m", 1, ("T1",), 1)[0],
    }
    chot(ket == {"chuan": KHONG_GIET, "mutant": KHONG_DO_DUOC,
                 "lan_thu": KHONG_DO_DUOC, "rc": KHONG_DO_DUOC}, "r515")


def r516_bo_cham_tu_dot_bien_phan_hang_dung(d: Path):
    """A6b — BO CHAM TU DOT BIEN phai phan hang dung, khong cap TIN DUNG GIA.

    F01 (luot 3) — day la tang NGOAI CUNG va truoc luot nay KHONG ca nao canh no.
    `chay_dot_bien_tu_kiem` chi so TAP TEN ca do, nen mot mutant chet bang
    `AttributeError` van duoc tinh GIET: do duoc, CHINH muc `bo-doi-ban-ghi-dong-luot`
    cua bang goc duoc cong nhan 3/3 bang BA `AttributeError`, va bien the boc lop
    ngoai le trong runner tu kiem van cho `23/23`.

    Ca nay goi CHINH `chay_dot_bien_tu_kiem`, chi thay `run` bang do gia kich ban
    hoa STDOUT + RC cua tien trinh con — tuc do DUONG PHAN HANG that, khong do mot
    ban sao. Bon ket cuc, bon nhan khac nhau, va bon la SO HANG chu khong phai
    quan he: 1 giet + 3 hong.
    """
    m = _nap_ban_sao(d)
    kich = {
        # (stdout cua con, rc cua con) -> ket cuc mong doi
        "giet-that":    ("TU KIEM r515: DO_CHOT — chot cua ca r515 that bai\n", 1),
        "loi-vo-can":   ("TU KIEM r510: DO_KHAC — AttributeError: NoneType\n", 1),
        "rc-khong-mot": ("TU KIEM r515: DO_CHOT — chot cua ca r515 that bai\n", 0),
        "sai-dich":     ("TU KIEM r511: DO_CHOT — chot cua ca r511 that bai\n", 1),
    }
    goi = []

    def run_gia(args, cwd, check=True, env=None):
        ten = Path(cwd).name
        goi.append(ten)
        out, rc = kich[ten]
        return subprocess.CompletedProcess(args, rc, out, "")

    m.run = run_gia

    def ghep(*phan):
        """Ghep neo LUC CHAY, khong viet nguyen van.

        Viet nguyen van thi chinh than ca nay lam chuoi ay xuat hien THEM mot lan
        ngoai bang, va phep doi hoi "neo duy nhat NGOAI bang" se bac ca bon — ca
        do vi ly do VO CAN, dung benh ma chinh no sinh ra de bat. Da tra gia mot
        luot chay: `(0, 4)` thay vi `(1, 3)`.
        """
        return "".join(phan)

    # Bon neo THAT, moi neo duy nhat NGOAI bang — `chay_dot_bien_tu_kiem` van doc
    # tep va cat bo bang y nhu luc chay that; chi TIEN TRINH CON la do gia. Noi
    # dung thay the KHONG bao gio duoc chay, nen chi tinh duy nhat cua NEO.
    # Bon neo nay phai la nhung dong KHONG dot bien nao KHAC cham toi: neu mot
    # muc trong bang that sua dung dong ay thi o luot chay cua MUC DO, neo cua
    # `r516` bien mat va ca do vi ly do VO CAN. Da tra gia: nam muc
    # (`bo-kiem-ban-ghi-trung` `bo-so-dau-phien` `bo-so-mutant` `bo-so-lan-thu`
    # `bo-so-rc-tien-trinh`) keo `r516` do theo dung kieu ay.
    m.DOT_BIEN_TU_KIEM = [
        ("giet-that", ("r515",), ghep("    if not ", "duong.exists():"), "    pass"),
        ("loi-vo-can", ("r510",), ghep("        if not ", "dong_txt.strip():"), "        pass"),
        ("rc-khong-mot", ("r515",),
         ghep("    theo_ca, chi_tiet, ", "dong = {}, {}, None"), "    pass"),
        # dich KHAI la r507 nhung con bao r511 do => SAI DICH, phai la `hong`.
        ("sai-dich", ("r507",), ghep('        theo_ca[ca] = ', 'r.get("nhan")'), "        pass"),
    ]
    with contextlib.redirect_stdout(io.StringIO()) as ra:
        giet, hong = m.chay_dot_bien_tu_kiem()
    chot(sorted(goi) == sorted(kich), "r516")     # bon mutant deu THAT SU duoc chay
    chot((giet, hong) == (1, 3), "r516")
    # Va ly do TUNG ket cuc phai dung, khong chi tong dung: mot bo cham cong nham
    # van co the ra (1, 3).
    dong_in = ra.getvalue()
    chot("loi-vo-can | r510 | TIN DUNG GIA: ca chet vi loi VO CAN" in dong_in, "r516")
    chot("rc-khong-mot | r515 | TIN DUNG GIA: child rc=0 != 1" in dong_in, "r516")
    chot("sai-dich | r507 | 0 — ca do THUC TE: r511" in dong_in, "r516")
    chot("giet-that | r515 | 1/1" in dong_in, "r516")
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


TU_KIEM = [
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
]

# ---- A6: MOI ca tu kiem phai co MOT dot bien rieng lam no DO --------------
# Ca khong doi mau theo dot bien duoc chi dinh thi KHONG duoc tinh vao so nhom.
DOT_BIEN_TU_KIEM = [
    ("bo-phan-biet-lop-ngoai-le", ("r501", "r504"),
     "if any(n == NHAN_DO_KHAC for n in theo_ca.values()):", "if False:"),
    ("cap-lop-chot-cho-assert-ha-tang", ("r502",),
     "    assert spec and spec.loader", '    chot(spec and spec.loader, "nap_tool")'),
    # r512 cung do: bo phep so bien KHONG_GIET thanh GIET, ma r512 doi KHONG_GIET.
    ("bo-so-tap-ca-do-voi-dich", ("r503", "r504", "r505", "r512", "r515"),
     "    if do_chot == set(dich):", "    if True:"),
    # r509 do kem: no dem HAI dau phien tu HAI luot phong that.
    ("bo-tran-chay-lai", ("r505", "r509"), "    for lan_thu in (1, 2):", "    for lan_thu in (1,):"),
    ("go-tat-ky-o-kho-mutant", ("r506",),
     '        run(["git", "config", "commit.gpgsign", "false"], src)', "        pass"),
    ("bo-kiem-ban-ghi-trung", ("r507", "r511"), "        if ca in theo_ca:", "        if False:"),
    # r509 do kem tu luot 2: bo so dau phien thi ban ghi luot MOT duoc nhan o luot HAI.
    ("bo-so-dau-phien", ("r508", "r509"),
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
    ("bo-doi-ban-ghi-dong-luot", ("r509", "r510"),
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
    ("cham-doc-stdout-khi-rc-mot", ("r512",),
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
    ("in-sai-so-hang", ("r513",),
     '    print(f"MUTANT: giet = {dat} · khong giet = {khong_giet} · khong do duoc = {khong_do}"',
     '    print(f"MUTANT: giet = {dat} · khong giet = {khong_giet} · khong do duoc = {khong_giet}"'),
    ("mo-cong-tong", ("r513",),
     "    if dat + khong_giet + khong_do != len(DOT_BIEN):", "    if False:"),
    ("mo-cong-nhom-bat-buoc", ("r513",),
     "    if thieu or len(NHOM_BAT_BUOC) < SAN_NHOM or tk_hong or tk_giet != len(DOT_BIEN_TU_KIEM):",
     "    if False:"),
    ("mo-cong-cuoi", ("r513",),
     "    return 0 if (dat == len(DOT_BIEN) and not tu_kiem_do) else 1", "    return 0"),
    # F07 — bo cong THAT: cong nham mot loai sang loai khac.
    ("gop-khong-do-vao-khong-giet", ("r514",),
     "                khong_do += 1", "                khong_giet += 1"),
    # F01 — bo TUNG chieu neo, moi chieu mot dot bien rieng.
    ("bo-so-mutant", ("r515",),
     '    neo = {"dau_phien": dau_phien, "mutant": mutant, "lan_thu": lan_thu}',
     '    neo = {"dau_phien": dau_phien, "lan_thu": lan_thu}'),
    ("bo-so-lan-thu", ("r515",),
     '    neo = {"dau_phien": dau_phien, "mutant": mutant, "lan_thu": lan_thu}',
     '    neo = {"dau_phien": dau_phien, "mutant": mutant}'),
    ("bo-so-rc-tien-trinh", ("r515",),
     '    if rc_that is not None and dong["rc"] != rc_that:', "    if False:"),
    # ---- F02 (luot 3): lop NEM cua duong ha tang, khong phai hinh dang AST ----
    ("run-nem-tin-hieu-chot", ("r501",),
     '        raise AssertionError(f"rc={p.returncode}: {\' \'.join(args)}\\n{p.stdout}\\n{p.stderr}")',
     '        raise TinHieuChotCa(f"rc={p.returncode}: {\' \'.join(args)}\\n{p.stdout}\\n{p.stderr}")'),
    # Boc GIU NGUYEN so node Assert (AST khong thay gi) ma doi HAN lop nem.
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
    # ---- F04: entropy phai phu thuoc MOI byte; dau phai moi moi LUOT PHONG ----
    ("entropy-giu-mot-byte", ("r509",),
     "    return secrets.token_hex(16)", "    return secrets.token_hex(16)[-2:] * 16"),
    ("cache-dau-phien-theo-dinh-danh", ("r509",),
     "        dau_phien = sinh_dau_phien()          # M7: SINH MOI moi luot",
     "        _c = globals().setdefault(\"_cache_ph\", {})\n"
     "        dau_phien = _c.setdefault((ten, lan_thu), sinh_dau_phien())"),
    # ---- F05: bo cong dem MUTANT, khong dem LAN THU --------------------------
    ("cong-theo-so-lan", ("r514",),
     "                khong_do += 1", "                khong_do += so_lan"),
    # ---- F03: ve `tk_giet` cua cong nhom bat buoc ----------------------------
    ("mo-cong-tu-dot-bien-thieu-giet", ("r513",),
     "    if thieu or len(NHOM_BAT_BUOC) < SAN_NHOM or tk_hong or tk_giet != len(DOT_BIEN_TU_KIEM):",
     "    if thieu or len(NHOM_BAT_BUOC) < SAN_NHOM or tk_hong:"),
    # ---- F01: BA chot cua bo cham tu dot bien, moi chot mot dot bien RIENG ----
    ("tu-dot-bien-bo-loc-loi-vo-can", ("r516",),
     "            if do_khac:", "            if False:"),
    ("tu-dot-bien-bo-so-rc-con", ("r516",),
     "            elif p.returncode != 1:", "            elif False:"),
    ("tu-dot-bien-nhan-moi-tap-ca", ("r516",),
     "            elif do_chot == set(dich):", "            elif True:"),
    # Runner tu kiem KHONG duoc gop hai lop lam mot — gop thi moi loi vo can
    # deu doi lot thanh chot cua ca.
    ("tu-kiem-gop-hai-lop-ngoai-le", ("r516",),
     '                print(f"TU KIEM {ten}: DO_KHAC — {type(exc).__name__}: {exc}")',
     '                print(f"TU KIEM {ten}: DO_CHOT — {type(exc).__name__}: {exc}")'),
    ("tu-kiem-bo-ghi-nhan-loi-vo-can", ("r516",),
     '            except Exception as exc:\n                do.append(ten)\n'
     '                print(f"TU KIEM {ten}: DO_KHAC',
     '            except Exception as exc:\n'
     '                print(f"TU KIEM {ten}: DO_KHAC'),
]


# F08 — tap nhom BAT BUOC ghi CUNG, doc lap voi `TU_KIEM`. Neu suy tu
# `len(TU_KIEM)` thi mau so TU CO: bo mot ca khoi ca danh sach chay lan tap dich
# thi bo dem van bao du, du da mat A5c(1b).
NHOM_BAT_BUOC = frozenset({"r501", "r502", "r503", "r504", "r505", "r506",
                           "r507", "r508", "r509", "r510", "r511", "r512",
                           "r513", "r514", "r515", "r516"})
SAN_NHOM = 16


def chay_dot_bien_tu_kiem():
    """Chay tung dot bien tren BAN SAO cua CHINH tep nay, doi DUNG ca dich do."""
    giet = hong = 0
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
        return 0, len(DOT_BIEN_TU_KIEM)
    with tempfile.TemporaryDirectory() as td:
        for ten, dich, neo, thay in DOT_BIEN_TU_KIEM:
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
            p = run([sys.executable, tep.name], d, check=False, env=env)
            # F01 (luot 3) — BA chot doc lap, khong gop: (1) khong ca nao duoc
            # chet vi loi VO CAN; (2) tien trinh con phai THAT SU thoat 1 — bo
            # ghi nhan danh sach do thi no van in "DO" ma rc ve 0; (3) tap ca do
            # dung bang dich. Thieu bat ky chot nao la mot duong cap TIN DUNG GIA.
            do_chot = set(re.findall(r"^TU KIEM (r\d+): DO_CHOT", p.stdout, re.M))
            do_khac = set(re.findall(r"^TU KIEM (r\d+): DO_KHAC", p.stdout, re.M))
            if do_khac:
                hong += 1
                print(f"DOT BIEN TU KIEM {ten} | {','.join(dich)} | TIN DUNG GIA: "
                      f"ca chet vi loi VO CAN {sorted(do_khac)}")
            elif p.returncode != 1:
                hong += 1
                print(f"DOT BIEN TU KIEM {ten} | {','.join(dich)} | TIN DUNG GIA: "
                      f"child rc={p.returncode} != 1")
            elif do_chot == set(dich):
                giet += 1
                print(f"DOT BIEN TU KIEM {ten} | {','.join(dich)} | {len(dich)}/{len(dich)}")
            else:
                hong += 1
                print(f"DOT BIEN TU KIEM {ten} | {','.join(dich)} | 0 — ca do THUC TE: "
                      f"{','.join(sorted(do_chot)) or '(rong)'}")
    return giet, hong


def chay_tu_kiem():
    do = []
    with tempfile.TemporaryDirectory() as td:
        for ten, fn, can_thu_muc in TU_KIEM:
            d = Path(td) / ten
            d.mkdir()
            try:
                fn(d) if can_thu_muc else fn()
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
    print(f"TU KIEM: {len(TU_KIEM) - len(do)}/{len(TU_KIEM)}")
    return do


def main() -> int:
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
    tk_giet, tk_hong = chay_dot_bien_tu_kiem()
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
    raise SystemExit(main())
