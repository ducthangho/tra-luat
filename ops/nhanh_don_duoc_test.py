#!/usr/bin/env python3
"""Phan chung bang kho bare that, kem bang dot bien tren ban sao tam."""
from __future__ import annotations
import importlib.util
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


def doc_kenh(duong: Path, dau_phien: str, mutant: str, lan_thu: int, dich):
    """Doc kenh va phan BA trang thai. Moi nhanh tu choi deu neu ly do.

    Chi nhan ban ghi neo DUNG luot vua phong: (dau_phien, mutant, lan_thu).
    Thieu ban ghi dong luot => KHONG DO DUOC (mot luot bi giet giua chung van co
    the de lai du so ban ghi).
    """
    if not duong.exists():
        return KHONG_DO_DUOC, "kenh khong ton tai"
    neo = {"dau_phien": dau_phien, "mutant": mutant, "lan_thu": lan_thu}
    theo_ca, dong = {}, None
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
    if dong is None:
        return KHONG_DO_DUOC, "thieu ban ghi dong luot"
    ten_ca = {t for t, _ in CA}
    if set(theo_ca) != ten_ca:
        thieu = sorted(ten_ca - set(theo_ca))
        la = sorted(set(theo_ca) - ten_ca)
        return KHONG_DO_DUOC, f"thieu ca {thieu} / ca la {la}"
    if any(n == NHAN_DO_KHAC for n in theo_ca.values()):
        xau = sorted(t for t, n in theo_ca.items() if n == NHAN_DO_KHAC)
        return KHONG_DO_DUOC, f"ca do vi ngoai le KHONG phai TinHieuChotCa: {xau}"
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
        run([sys.executable, Path(__file__).name], ban_sao, check=False, env=env)
        trang_thai, ly_do = doc_kenh(kenh, dau_phien, ten, lan_thu, dich)
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


def r501_tin_hieu_chot_khong_gia_mao_duoc(d: Path):
    """A1 — ca NGOAI dich do bang duong ha tang => KHONG DO DUOC, khong phai GIET."""
    ph = sinh_dau_phien()
    k = _kenh_tam(_du_ca(ph, {"T1": NHAN_DO_CHOT, "T7": NHAN_DO_KHAC})
                  + [_ban_ghi(ph, dong_luot=True, rc=1)], d)
    tt, _ = doc_kenh(k, ph, "m", 1, ("T1",))
    chot(tt == KHONG_DO_DUOC, "r501")


def r502_assert_ha_tang_khong_duoc_cap_lop_chot():
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


def r506_moi_kho_deu_tat_ky_commit():
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


def r509_dau_phien_phai_sinh_moi_moi_luot():
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
    """A5b (ca chinh) — ma bi thu IN ra stdout mot dong mang dung hinh dang ket qua.

    Bo cham KHONG duoc doc dong ay: ket qua chi lay tu KENH RIENG. Ca nay BAT BUOC
    di qua subprocess THAT — lo hong nam o RANH GIOI TIEN TRINH, ma mot phep thu
    trong bo nho khong co ranh gioi ay de ma thung.
    """
    ph = sinh_dau_phien()
    kenh = d / "k.jsonl"
    kich = d / "kich.py"
    kich.write_text(
        "import json,os,sys\n"
        "print('CASE T1: DO — gia mao qua stdout')\n"
        "k=open(os.environ['K'],'a',encoding='utf-8')\n"
        "for c in %r:\n"
        "    k.write(json.dumps({'ca':c,'dau_phien':os.environ['P'],'mutant':'m',"
        "'lan_thu':1,'nhan':'DAT'},sort_keys=True)+'\\n')\n"
        "k.write(json.dumps({'dau_phien':os.environ['P'],'mutant':'m','lan_thu':1,"
        "'dong_luot':True,'rc':0},sort_keys=True)+'\\n')\n"
        "k.close()\n" % [x for x, _ in CA], encoding="utf-8")
    env = dict(os.environ, K=str(kenh), P=ph)
    p = run([sys.executable, str(kich)], d, check=False, env=env)
    chot("CASE T1: DO" in p.stdout, "r512")        # stdout THAT SU co dong gia mao
    tt, _ = doc_kenh(kenh, ph, "m", 1, ("T1",))
    # Kenh khai T1 DAT => khong phai GIET. Neu bo cham doc stdout thi no se thay
    # "CASE T1: DO" va cham GIET — do dung la thu ca nay chan.
    chot(tt == KHONG_GIET, "r512")


TU_KIEM = [
    ("r501", r501_tin_hieu_chot_khong_gia_mao_duoc, True),
    ("r502", r502_assert_ha_tang_khong_duoc_cap_lop_chot, False),
    ("r503", r503_chot_cua_ca_KHAC_khong_tinh_la_giet, True),
    ("r504", r504_ba_trang_thai_khong_gop, True),
    ("r505", r505_chay_lai_dung_mot_lan, True),
    ("r506", r506_moi_kho_deu_tat_ky_commit, False),
    ("r507", r507_kenh_ket_qua_ba_bien, True),
    ("r508", r508_ban_ghi_luot_TRUOC_chi_khac_dau_phien, True),
    ("r509", r509_dau_phien_phai_sinh_moi_moi_luot, False),
    ("r510", r510_ban_ghi_thieu_dau_dong_luot, True),
    ("r511", r511_ma_san_pham_phat_khong_doat_duoc_ten_ca, True),
    ("r512", r512_kenh_khong_lan_voi_stdout, True),
]

# ---- A6: MOI ca tu kiem phai co MOT dot bien rieng lam no DO --------------
# Ca khong doi mau theo dot bien duoc chi dinh thi KHONG duoc tinh vao so nhom.
DOT_BIEN_TU_KIEM = [
    ("bo-phan-biet-lop-ngoai-le", ("r501", "r504"),
     "if any(n == NHAN_DO_KHAC for n in theo_ca.values()):", "if False:"),
    ("cap-lop-chot-cho-assert-ha-tang", ("r502",),
     "    assert spec and spec.loader", '    chot(spec and spec.loader, "nap_tool")'),
    # r512 cung do: bo phep so bien KHONG_GIET thanh GIET, ma r512 doi KHONG_GIET.
    ("bo-so-tap-ca-do-voi-dich", ("r503", "r504", "r512"),
     "    if do_chot == set(dich):", "    if True:"),
    ("bo-tran-chay-lai", ("r505",), "    for lan_thu in (1, 2):", "    for lan_thu in (1,):"),
    ("go-tat-ky-o-kho-mutant", ("r506",),
     '        run(["git", "config", "commit.gpgsign", "false"], src)', "        pass"),
    ("bo-kiem-ban-ghi-trung", ("r507", "r511"), "        if ca in theo_ca:", "        if False:"),
    ("bo-so-dau-phien", ("r508",),
     '    neo = {"dau_phien": dau_phien, "mutant": mutant, "lan_thu": lan_thu}',
     '    neo = {"mutant": mutant, "lan_thu": lan_thu}'),
    # r508 cung do: dau theo moc giay thi ph_that va ph_khac cua r508 TRUNG nhau
    # trong cung mot giay, nen ban ghi "chi khac dau phien" duoc NHAN => ca do.
    ("dau-phien-thanh-moc-giay", ("r508", "r509"),
     "    return secrets.token_hex(16)",
     '    import time as _tg\n    return str(int(_tg.time()))'),
    ("bo-doi-ban-ghi-dong-luot", ("r510",), "    if dong is None:", "    if False:"),
    ("khung-lay-ten-ca-tu-doi-so", ("r511",),
     "        ban_ghi = dict(self._neo, ca=self._ca_dang_chay, nhan=nhan, chi_tiet=chi_tiet)",
     '        _ca = chi_tiet.split("la ")[-1] if "tu khai la" in chi_tiet else self._ca_dang_chay\n'
     "        ban_ghi = dict(self._neo, ca=_ca, nhan=nhan, chi_tiet=chi_tiet)"),
    ("cham-doc-stdout-thay-vi-kenh", ("r512",),
     "    chot(tt == KHONG_GIET, \"r512\")",
     '    ca_do = re.findall(r"^CASE (T\\d+): DO", p.stdout, re.M)\n'
     "    chot(tt == KHONG_GIET and not ca_do, \"r512\")"),
]


def chay_dot_bien_tu_kiem():
    """Chay tung dot bien tren BAN SAO cua CHINH tep nay, doi DUNG ca dich do."""
    giet = hong = 0
    goc = Path(__file__).read_text(encoding="utf-8")
    # Moi mau neo xuat hien HAI lan: mot o ma that, mot o CHINH bang duoi day.
    # Chi ap len phan TRUOC bang — cung lop loi ma r506 da dinh (dem chuoi thi tu
    # khop chinh than minh). Do duoc: khong cat thi ca 11 neo deu "KHONG DUY NHAT (2)".
    cat = goc.index("DOT_BIEN_TU_KIEM = [")
    dau, duoi = goc[:cat], goc[cat:]
    with tempfile.TemporaryDirectory() as td:
        for ten, dich, neo, thay in DOT_BIEN_TU_KIEM:
            if dau.count(neo) != 1:
                print(f"DOT BIEN TU KIEM {ten}: NEO KHONG DUY NHAT ({dau.count(neo)})")
                hong += 1
                continue
            d = Path(td) / ten
            d.mkdir()
            tep = d / Path(__file__).name
            tep.write_text(dau.replace(neo, thay) + duoi, encoding="utf-8", newline="\n")
            shutil.copy2(TOOL, d / TOOL.name)
            env = dict(os.environ, NHANH_DON_DUOC_CHI_TU_KIEM="1", PYTHONDONTWRITEBYTECODE="1")
            env.pop(KENH_ENV, None)
            p = run([sys.executable, tep.name], d, check=False, env=env)
            do = set(re.findall(r"^TU KIEM (r\d+): DO", p.stdout, re.M))
            if do == set(dich):
                giet += 1
                print(f"DOT BIEN TU KIEM {ten} | {','.join(dich)} | {len(dich)}/{len(dich)}")
            else:
                hong += 1
                print(f"DOT BIEN TU KIEM {ten} | {','.join(dich)} | 0 — ca do THUC TE: "
                      f"{','.join(sorted(do)) or '(rong)'}")
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
            except Exception as exc:
                do.append(ten)
                print(f"TU KIEM {ten}: DO — {type(exc).__name__}: {exc}")
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
    print(f"TU KIEM co dot bien rieng: {len(nhom_co_dot_bien)}/{len(TU_KIEM)} nhom · "
          f"dot bien giet {tk_giet}/{len(DOT_BIEN_TU_KIEM)}")
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
    if len(nhom_co_dot_bien) != len(TU_KIEM) or tk_hong:
        print("LOI: co ca tu kiem thieu dot bien rieng, hoac dot bien khong doi mau dung ca")
        return 1
    return 0 if (dat == len(DOT_BIEN) and not tu_kiem_do) else 1
if __name__ == "__main__":
    raise SystemExit(main())
