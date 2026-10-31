#!/usr/bin/env python3
"""Phản chứng cho `ops/cloud_agent_creds.py` + khối hook (CLOUD-SETUP-P2B-WIRE r1, `nghiem_thu` A–D, H, F2). Ca = hàm `<a-h><số>_…`;
`nap` chạy con trên cây tạm có `scripts/tl.py` GIẢ, `cai-agy` in-process (tải giả ĐẾM lời gọi). Đột biến sửa BẢN SAO TẠM; chỉ `bang()`
ném `TinHieuChotCa` (con thoát 3 + `DO:<ca>:`); lỗi vô can thoát 4 = TÍN DỤNG GIẢ; 5 = bỏ qua (Windows, hay cây rời không .git)."""
import contextlib, ctypes, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys, tarfile, tempfile, time  # noqa: E401
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

sys.dont_write_bytecode = True
for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding="utf-8", errors="backslashreplace")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bash_nen  # noqa: E402 — bộ giải `bash` dùng chung (#570)

MA = Path(os.environ.get("CAC_MA") or HERE / "cloud_agent_creds.py")
HOOK = Path(os.environ.get("CAC_HOOK") or HERE.parent / ".claude/hooks/session-start.sh")
BASE = "97120d3c76ebb7c3eda4b585ff46f1c51e30c91b"   # base của lease wp1039 — vế âm L6a
LA_WINDOWS = os.name == "nt"
SPEC = HERE / "specs" / "cloud-setup-p2b-wire-r1.md"   # B8 so với CHÍNH bảng "Hằng ghim agy" của spec đóng băng, không chép lại
SPEC_SHA256 = "67b448acc825fdd29f118c3b9082583773b4ad218a7c83ab4db496daa8f26d81"
class TinHieuChotCa(AssertionError):
    """Chỉ `bang()` ném lớp này ⇒ phân biệt giết thật (chốt) với chết vì lỗi vô can."""
class BoQua(Exception):
    pass
def bang(dieu_kien, thong_diep):
    if not dieu_kien:
        raise TinHieuChotCa(thong_diep)
def _nem(loi):
    raise loi
def _posix():
    if LA_WINDOWS:
        raise BoQua("đồ giả là script POSIX / nhóm tiến trình POSIX")
def nap_mod():
    (spec := importlib.util.spec_from_file_location("cloud_agent_creds_duoi_test", MA)).loader.exec_module(m := importlib.util.module_from_spec(spec))
    return m
def _git_base(path):   # tệp ở BASE; chỉ tha (BoQua) khi cây là bản sao rời không `.git` (CLAUDE.md, "ca có MẶT ≠ ca có ĐO")
    if not (HERE.parent / ".git").exists():
        raise BoQua("cây không có .git — không đo được vế âm trên base")
    r = subprocess.run(["git", "-C", str(HERE.parent), "show", f"{BASE}:{path}"], capture_output=True)
    bang(r.returncode == 0, f"không đọc được {path} ở base: {r.stderr[-200:]!r}")
    return r.stdout.decode("utf-8")

# ---------- A: `nap` ----------
TL_GIA = r'''import json, os, subprocess, sys, time
kb = json.loads(os.environ["CAC_KICH_BAN"])
CHAU = "import subprocess, sys, time; open(sys.argv[1], 'w').write(str(subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)']).pid)); time.sleep(60)"
con = subprocess.Popen([sys.executable, "-c", CHAU, os.environ["CAC_NHAT_KY"] + ".chau"]).pid if kb.get("con") else None   # con + cháu cùng nhóm
with open(os.environ["CAC_NHAT_KY"], "a", encoding="utf-8") as f:
    f.write(json.dumps({"argv": sys.argv[1:], "pid": os.getpid(), "con": con, "exe": sys.executable}) + "\n")
[(k.buffer.write(kb.get(n, "").encode("utf-8")), k.flush()) for k, n in ((sys.stdout, "in"), (sys.stderr, "loi"))]
time.sleep(kb.get("ngu", 0)); sys.exit(kb.get("rc", 0))
'''
def chay_nap(kb=None, khoa="khoa-thu", them=None, xoa_tl=False, argv=("nap",)):
    with tempfile.TemporaryDirectory(prefix="cac_nap_") as t:
        t, bo = Path(t), ("TL_MASTER_KEY", "TL_CLOUD_BOOTSTRAP_TIMEOUT_GIAY")
        (t / "ops").mkdir(), (t / "scripts").mkdir(), shutil.copy(MA, t / "ops" / "cloud_agent_creds.py")
        xoa_tl or (t / "scripts" / "tl.py").write_text(TL_GIA, encoding="utf-8")
        nk, env = t / "nk.jsonl", {k: v for k, v in os.environ.items() if k not in bo}
        env.update(CAC_NHAT_KY=str(nk), CAC_KICH_BAN=json.dumps(kb or {}), **(them or {}), **({} if khoa is None else {"TL_MASTER_KEY": khoa}))
        t0 = time.monotonic()
        r = subprocess.run([sys.executable, "-B", str(t / "ops" / "cloud_agent_creds.py"), *argv], capture_output=True, env=env, timeout=150)
        ra = r.stdout.decode("utf-8", "replace")
        return SimpleNamespace(rc=r.returncode, ra=ra, loi=r.stderr.decode("utf-8", "replace"), giay=time.monotonic() - t0,
                               nk=[json.loads(x) for x in nk.read_text(encoding="utf-8").splitlines()] if nk.exists() else [],
                               chau=[int(c.read_text())] if (c := Path(str(nk) + ".chau")).exists() and c.read_text() else [],
                               ag=[d for d in ra.splitlines() if "agent_creds:" in d])
def _con_song(pid):   # zombie tính là chết (CLAUDE.md)
    try:
        return os.kill(pid, 0) is None and Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0] != "Z"
    except (ProcessLookupError, FileNotFoundError):
        return False
def _song_roi_don(pids):   # PID còn sống TRƯỚC khi dọn, rồi giết hết để ca không để rác
    song = [x for x in pids if x is not None and _con_song(x)]
    for x in song:   # dọn bằng syscall, không dựa tiện ích ngoài (F15)
        with contextlib.suppress(OSError):
            os.kill(x, 9)
    return song
def _ghi(f, noi_dung, chay=False):
    f.parent.mkdir(parents=True, exist_ok=True), f.write_text(noi_dung, encoding="utf-8"), chay and f.chmod(0o755)
def a1_thieu_khoa_khong_goi_tl():
    for khoa in (None, ""):
        k = chay_nap({"in": "[bootstrap] agent_creds: ĐÃ NẠP — x\n"}, khoa=khoa)
        bang(k.rc == 0 and k.ag == ["agent_creds: BỎ QUA — thiếu TL_MASTER_KEY"], f"khoa={khoa!r}: rc={k.rc} {k.ag}")
        bang(len(k.nk) == 0, f"khoa={khoa!r}: tl.py giả chạy {len(k.nk)} lần")
def a2_loc_dong_agent_cua_bootstrap():
    k = chay_nap({"in": "[bootstrap] dòng thường\n[bootstrap] agent_creds: ĐÃ NẠP — rev=7\n"})
    bang(len(k.ag) == 1 and k.ag[0].startswith("agent_creds: ĐÃ NẠP — rev=7"), f"dòng agent {k.ag}")
    bang("[bootstrap] agent_creds:" not in k.ra and "[bootstrap] dòng thường" in k.ra, f"chuyển tiếp sai: {k.ra!r}")
def a3_bang_sau_ca_hop_dong():
    hai = "agent_creds: ĐÃ NẠP — a\nagent_creds: ĐÃ NẠP — b\n"
    for i, (kb, xoa, s, ly_do) in enumerate([
            ({"rc": 2}, 0, "KHÔNG ĐO ĐƯỢC", "rc=2"), ({"rc": 3}, 0, "KHÔNG ĐO ĐƯỢC", "rc=3"),
            ({"in": hai}, 0, "KHÔNG ĐO ĐƯỢC", "không đúng hợp đồng"), ({"in": "agent_creds: LẠ — x\n"}, 0, "KHÔNG ĐO ĐƯỢC", "không đúng hợp đồng"),
            ({}, 1, "KHÔNG ĐO ĐƯỢC", "không chạy được"), ({"rc": 1, "in": "[bootstrap] agent_creds: KHÔNG CẤU HÌNH — y\n"}, 0, "KHÔNG CẤU HÌNH", "rc=1")], 1):
        k = chay_nap(kb, xoa_tl=xoa)
        bang(k.rc == 0 and len(k.ag) == 1, f"ca {i}: rc={k.rc} dòng agent {k.ag}")
        bang(k.ag[0].startswith(f"agent_creds: {s} — ") and ly_do in k.ag[0], f"ca {i}: {k.ag[0]!r} (mong {s}/{ly_do})")
def a4_qua_han_giet_ca_nhom():
    _posix()
    sen = "SENTINEL-khoa-a4-55d1"   # F12: log chẩn đoán (hai kênh) đã nhận trước khi treo vẫn được chuyển tiếp, đã che
    k = chay_nap({"ngu": 60, "con": 1, "in": f"chẩn đoán {sen}\n[bootstrap] agent_creds: ĐÃ NẠP — cũ\n", "loi": "lỗi chẩn đoán\n"},
                 khoa=sen, them={"TL_CLOUD_BOOTSTRAP_TIMEOUT_GIAY": "2"})
    pids = [k.nk[0]["pid"], k.nk[0]["con"], *(k.chau or [None])] if k.nk else [None]
    song = _song_roi_don(pids)
    bang(k.giay < 20, f"nap mất {k.giay:.1f} s")
    bang(k.rc == 0 and k.ag == ["agent_creds: KHÔNG ĐO ĐƯỢC — bootstrap quá 2 s, đã dừng"], f"rc={k.rc} {k.ag}")
    bang(None not in pids and not song, f"PID {pids} (cha, con, cháu cùng nhóm): còn sống {song}")
    bang("chẩn đoán ***" in k.ra and "lỗi chẩn đoán" in k.ra and sen not in k.ra + k.loi, f"log khi quá hạn mất/lộ: {k.ra!r}")
def a9_loi_gui_tin_hieu_khong_bao_da_dung():   # F11: killpg lỗi (TIÊM), chỉ cha chết ⇒ cấm in "đã dừng"
    _posix()
    with tempfile.TemporaryDirectory() as t:
        m, t, that, buf = nap_mod(), Path(t), os.killpg, io.StringIO()
        _ghi(t / "scripts" / "tl.py", TL_GIA)
        m.GOC, m.HAN_DON = t, 1
        gia = lambda pg, sig: _nem(PermissionError("tiêm lỗi")) if sig and not os.kill(pg, 9) else that(pg, sig)   # noqa: E731
        kb = {"ngu": 60, "con": 1, "in": "chẩn đoán SENTINEL-a9\n[bootstrap] agent_creds: ĐÃ NẠP — cũ\n", "loi": "lỗi chẩn đoán\n"}
        moi = {"TL_MASTER_KEY": "SENTINEL-a9", "CAC_NHAT_KY": str(t / "nk"), "CAC_KICH_BAN": json.dumps(kb)}
        with mock.patch.dict(os.environ, moi), mock.patch.object(m.os, "killpg", gia), contextlib.redirect_stdout(buf):
            m.nap({"TL_MASTER_KEY": "SENTINEL-a9", "TL_CLOUD_BOOTSTRAP_TIMEOUT_GIAY": "1"})
        nk = json.loads((t / "nk").read_text(encoding="utf-8")) if (t / "nk").exists() else {}
        song = _song_roi_don([nk.get("con"), *([int((t / "nk.chau").read_text())] if (t / "nk.chau").exists() else [])])
    bang(song, "fixture hỏng: con/cháu phải còn sống khi chỉ cha bị giết")
    bang("KHÔNG xác minh được việc dừng" in buf.getvalue() and "đã dừng" not in buf.getvalue(), f"báo dừng khi nhóm còn sống: {buf.getvalue()!r}")
    ra = buf.getvalue()   # F12: nhóm KHÔNG dừng được vẫn chuyển tiếp log đã nhận, đúng một lần, đã che, bỏ dòng agent cũ
    bang(ra.count("chẩn đoán ***") == 1 and ra.count("lỗi chẩn đoán") == 1 and "SENTINEL-a9" not in ra and ra.count("agent_creds:") == 1, f"log: {ra!r}")
def _co_subreaper():   # PR_GET_CHILD_SUBREAPER của CHÍNH tiến trình test
    return c.value if ctypes.CDLL(None).prctl(37, ctypes.byref(c := ctypes.c_int(-1)), 0, 0, 0) == 0 else None
def a11_subreaper_va_esrch():   # (B, #1039): CHỈ ESRCH sau khi thu hồi cháu mồ côi mới "đã dừng"; không subreaper ⇒ không xác minh
    _posix()
    for co_sr in (True, False):
        (m := nap_mod())._SUBREAPER = None if co_sr else False
        bang(m._dat_subreaper() is co_sr and (not co_sr or _co_subreaper() == 1), f"subreaper={co_sr}: không đặt được thật")
        p = subprocess.Popen(["sh", "-c", "sleep 30 & echo $!; sleep 30"], stdout=subprocess.PIPE, start_new_session=True)
        q = subprocess.Popen([sys.executable, "-c", "raise SystemExit(7)"])   # con NGOÀI nhóm: waitpid không được thu nhầm (F14)
        time.sleep(0.3), os.waitid(os.P_PID, q.pid, os.WEXITED | os.WNOWAIT)   # q CHẮC đã thoát, trạng thái chưa bị thu
        da, ra = m._giet_nhom(p)
        song = _song_roi_don([int(x) for x in ra.split()[:1]])
        bang(ra.split() and da is co_sr and not song and q.wait(timeout=10) == 7, f"sr={co_sr}: dừng={da}, sống {song}, q={q.returncode}")
    m, that, p = nap_mod(), os.killpg, subprocess.Popen(["sleep", "30"], start_new_session=True)   # F14: EPERM ≠ ESRCH
    with mock.patch.object(m.os, "killpg", lambda pg, sig: that(pg, sig) if sig else _nem(PermissionError("tiêm"))):
        bang(m._giet_nhom(p)[0] is False, "EPERM của killpg(pg, 0) bị nhận là đã dừng")
    for goi in (lambda m: (setattr(m, "GOC", HERE.parent), m.nap({"TL_MASTER_KEY": "k"})), lambda m: m._ban_khop(Path("/khong-co-agy"))):   # F14: subreaper TRƯỚC Popen
        m, thu = nap_mod(), []   # Popen giả ném lỗi: KHÔNG chạy tiến trình thật nào
        with mock.patch.object(m, "_dat_subreaper", lambda: thu.append("sr")), mock.patch.object(m.subprocess, "Popen", lambda *a, **k: _nem(OSError(thu.append("popen")))), contextlib.redirect_stdout(io.StringIO()):
            goi(m)
        bang(thu[:2] == ["sr", "popen"], f"thứ tự subreaper/Popen: {thu}")
def a5_doc_timeout():
    m = nap_mod()
    for v in ("abc", "-5", "0", "inf", "1e300", "2147484"):
        bang(m.doc_timeout(v) == 180, f"doc_timeout({v!r}) = {m.doc_timeout(v)}")
def a6_argv_va_trinh_thong_dich():
    k = chay_nap({"in": "agent_creds: ĐÃ NẠP — x\n"})
    bang(len(k.nk) == 1 and k.nk[0]["argv"] == ["bootstrap", "--env", "code", "--no-nlm"], f"argv {k.nk}")
    bang(os.path.realpath(k.nk[0]["exe"]) == os.path.realpath(sys.executable), f"trình thông dịch {k.nk[0]['exe']}")
def a7_che_master_key():
    s = "SENTINEL-khoa-a7-9f3c2e"
    for kenh in ("in", "loi"):   # đo CẢ hai kênh của bootstrap (F04)
        k = chay_nap({kenh: f"dòng {s}\n[bootstrap] agent_creds: ĐÃ NẠP — {s}\n"}, khoa=s)
        bang(s not in k.ra + k.loi and "***" in k.ra and len(k.ag) == 1, f"{kenh}: TL_MASTER_KEY lọt / không che / dòng agent {k.ag}")
def a8_nap_luon_rc0():
    for rc in range(5):
        bang(chay_nap({"rc": rc}).rc == 0, f"bootstrap rc={rc} ⇒ nap rc khác 0")
    bang(chay_nap({"ngu": 30}, them={"TL_CLOUD_BOOTSTRAP_TIMEOUT_GIAY": "1"}).rc == 0, "quá hạn ⇒ nap rc khác 0")
    k = chay_nap({}, argv=("nap", "--la"))
    bang(k.rc == 2 and len(k.nk) == 0, f"`nap --la`: rc={k.rc}, tl.py chạy {len(k.nk)} lần")
# ---------- B/C/D: `cai-agy` ----------
NOI_DUNG = b'#!/bin/sh\n[ -n "$CAC_AGY_NK" ] && echo "$*" >> "$CAC_AGY_NK"\necho antigravity 1.4.12\n'
def _tar(muc):   # (tên, byte | None = symlink tới /etc/passwd)
    with tarfile.open(fileobj=(b := io.BytesIO()), mode="w:gz") as tf:
        for ten, du in muc:
            ti = tarfile.TarInfo(ten)
            ti.type, ti.linkname, ti.size = (tarfile.SYMTYPE, "/etc/passwd", 0) if du is None else (tarfile.REGTYPE, "", len(du))
            tf.addfile(ti, None if du is None else io.BytesIO(du))
    return b.getvalue()
TAR_TOT = _tar([("antigravity", NOI_DUNG)])
@contextlib.contextmanager
def san_agy(tar=TAR_TOT, nen="linux_amd64", sha=None, agy_cu=None, env_them=None, settings=None):
    m = nap_mod()
    with tempfile.TemporaryDirectory(prefix="cac_agy_") as t:
        (home := (t := Path(t)) / "home").mkdir()
        nk, dem = t / "agy_goi.log", []
        m.tai, m.khoa_nen_hien_tai = (lambda url: (dem.append(url), tar)[1]), (lambda: nen)
        m.NEN = {"linux_amd64": ("https://gia.invalid/agy.tar.gz", sha or hashlib.sha512(tar).hexdigest())}
        agy, st = home / ".local" / "bin" / "agy", home / ".gemini/antigravity-cli/settings.json"
        settings is None or _ghi(st, settings)
        agy_cu is None or _ghi(agy, f'#!/bin/sh\necho "$*" >> "{nk}"\nprintf \'%b\\n\' "{agy_cu[0]}"\nexit {agy_cu[1]}\n', True)
        def chay():
            buf = io.StringIO()
            with mock.patch.dict(os.environ, {"CAC_AGY_NK": str(nk)}), contextlib.redirect_stdout(buf):
                rc = m.cai_agy({"HOME": str(home), **(env_them or {})})
            return rc, buf.getvalue()
        yield SimpleNamespace(m=m, t=t, dem=dem, chay=chay, agy=agy, nk=nk, settings=st,
                              tep=lambda: sorted(str(p.relative_to(t)) for p in t.rglob("*") if p.is_symlink() or p.is_file()))
def b1_chua_co_thi_tai_va_ghi():
    with san_agy() as s:
        rc, ra = s.chay()
        bang(rc == 0 and len(s.dem) == 1, f"rc={rc}, tải {len(s.dem)} lần")
        bang(s.agy.is_file() and s.agy.read_bytes() == NOI_DUNG, f"~/.local/bin/agy sai: {ra}")
        bang(LA_WINDOWS or s.agy.stat().st_mode & 0o111, "agy không có bit thực thi")
def b2_sha512_lech_khong_ghi():
    _posix()
    with san_agy(sha="0" * 128) as s:
        rc, ra = s.chay()
        bang(rc == 0 and not s.agy.exists() and "agy: ✗ sha512 lệch" in ra, f"rc={rc} tạo={s.agy.exists()} {ra!r}")
    with san_agy(sha="0" * 128, agy_cu=("antigravity 1.4.0", 0)) as s:
        truoc, _ = s.agy.read_bytes(), s.chay()
        bang(s.agy.read_bytes() == truoc, "bản cũ bị đổi dù sha512 lệch")
def b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay():   # B3 (đếm 0) + B4 (đếm 1, tệp được thay)
    _posix()
    for cu, n in ((("antigravity 1.4.12", 0), 0), (("antigravity 1.4.13", 0), 1), (("antigravity 1.4.12", 1), 1), (("\\0377", 0), 1), (("antigravity 1.4.120", 0), 1), (("antigravity 1.4.12rc1", 0), 1), (("antigravity 1.4.12beta", 0), 1)):
        with san_agy(agy_cu=cu) as s:
            s.chay()
            bang(len(s.dem) == n and (n == 0 or s.agy.read_bytes() == NOI_DUNG), f"{cu}: tải {len(s.dem)} lần (mong {n}) / không thay tệp")
def b10_version_treo_giet_ca_nhom():   # F01: `--version` treo + con cùng nhóm ⇒ cả nhóm chết, vẫn tải/thay
    _posix()
    with san_agy() as s:
        _ghi(s.agy, f'#!/bin/sh\necho $$ > "{s.t}/cha"\nsleep 60 &\necho $! > "{s.t}/con"\nwait\n', True)
        s.m.HAN_VERSION, _ = 1, s.chay()
        pids = [int(Path(s.t, f).read_text()) for f in ("cha", "con") if Path(s.t, f).exists()]
        song = _song_roi_don(pids)
        bang(len(pids) == 2 and not song, f"PID {pids} của `agy --version`: còn sống {song}")
        bang(len(s.dem) == 1 and s.agy.read_bytes() == NOI_DUNG, f"treo mà không tải/thay (tải {len(s.dem)})")
def b5_nen_ngoai_bang():
    with san_agy(nen="freebsd_amd64") as s:
        rc, ra = s.chay()
        bang(rc == 0 and "agy: CHƯA HỖ TRỢ freebsd_amd64" in ra and len(s.dem) == 0, f"rc={rc} tải {len(s.dem)} {ra!r}")
def d2_khong_env_file_khong_tao_tep():   # chủ kho duyệt cách hiểu (#1039 issuecomment-6541865575): ngoài settings.json do C1 tạo, không tệp nào
    with san_agy(nen="freebsd_amd64") as s, contextlib.chdir(s.t):
        rc, _ = s.chay()
        bang(rc == 0 and s.tep() == [str(s.settings.relative_to(s.t))], f"rc={rc} tệp lạ ở cwd/HOME: {s.tep()}")
def b6_tarball_doc_tu_choi():
    for i, muc in enumerate(([("../x", b"x")], [("antigravity", NOI_DUNG), ("khac", b"y")], [("antigravity", None)]), 1):
        with san_agy(tar=_tar(muc)) as s:
            rc, ra = s.chay()
            bang(rc == 0 and not s.agy.exists() and not s.agy.is_symlink(), f"tarball độc {i}: tạo agy ({ra!r})")
            bang(s.tep() == [str(s.settings.relative_to(s.t))], f"tarball độc {i}: ghi lạ {s.tep()}")
def b7_khong_goi_agy_install():
    _posix()
    with san_agy(agy_cu=("antigravity 1.4.13", 0)) as s:
        s.chay(), s.chay()
        goi = s.nk.read_text(encoding="utf-8").splitlines() if s.nk.exists() else []
        bang(goi and all(g == "--version" for g in goi), f"lời gọi agy: {goi}")
def b8_hang_ghim_dung_spec():
    m, b = nap_mod(), SPEC.read_bytes()
    bang(hashlib.sha256(b).hexdigest() == SPEC_SHA256, "spec đóng băng đổi băm")
    bang(len(spec := dict((k, (u, h)) for k, u, h in re.findall(r"^\| `(\w+)` \| `(https://\S+)` \| `([0-9a-f]{128})` \|$", b.decode("utf-8"), re.M))) == 6, "spec phải có 6 nền")
    bang(m.AGY_VER == "1.4.12" and sorted(m.NEN) == sorted(spec), f"AGY_VER={m.AGY_VER} khoá={sorted(m.NEN)}")
    for k, v in spec.items():
        bang(tuple(m.NEN[k]) == v, f"hằng ghim {k} lệch spec")
def _goi_doi_kieu(f, *a):
    try:
        return f(*a)
    except Exception as e:  # CỐ Ý — bẫy F2: đổi lỗi vô can thành AssertionError; bộ phân hạng KHÔNG được nhận nó là giết
        raise AssertionError(f"lỗi {type(e).__name__}") from e
def b9_luat_chon_nen():
    m = nap_mod()
    for vao, mong in ((("Linux", "x86_64", False), "linux_amd64"), (("Linux", "aarch64", True), "linux_arm64_musl"), (("Darwin", "arm64", False), "darwin_arm64")):
        bang(_goi_doi_kieu(m.khoa_nen, *vao) == mong, f"{vao} ⇒ {m.khoa_nen(*vao)}, mong {mong}")
    bang(_goi_doi_kieu(m.khoa_nen, "Linux", "i686", False) not in m.NEN, "Linux/i686 rơi vào bảng")
def c13_gop_model_provider_khong_ghi_khoa():   # C1 + C3 (khoá trong môi trường không được vào settings.json)
    sen = "SENTINEL-gemini-c3-71ab"
    for truoc, mong in (('{"a": 1, "modelProvider": "x"}', {"a": 1, "modelProvider": "gemini"}), (None, {"modelProvider": "gemini"})):
        with mock.patch.dict(os.environ, {"GEMINI_API_KEY": sen, "GOOGLE_API_KEY": sen}), san_agy(nen="freebsd_amd64", settings=truoc) as s:
            s.chay()
            bang(json.loads(s.settings.read_text(encoding="utf-8")) == mong, f"{truoc!r}: settings sai")
            bang(sen not in s.settings.read_text(encoding="utf-8"), "settings.json chứa khoá từ môi trường")
def c2_settings_khong_phai_object_khong_dung():
    for nd in ("[1,2]", "{không phải json"):
        with san_agy(nen="freebsd_amd64", settings=nd) as s:
            truoc = hashlib.sha256(s.settings.read_bytes()).hexdigest()
            rc, ra = s.chay()
            bang(rc == 0 and hashlib.sha256(s.settings.read_bytes()).hexdigest() == truoc and "agy: ⚠" in ra, f"{nd!r}: tệp bị đổi / không cảnh báo")
def d1_env_file_dung_mot_dong():
    with tempfile.TemporaryDirectory() as t, san_agy(nen="freebsd_amd64", env_them={"CLAUDE_ENV_FILE": str(f := Path(t) / "env.sh")}) as s:
        _ghi(f, "export FOO=1\n"), s.chay(), s.chay()
        dong = f.read_text(encoding="utf-8").splitlines()
        bang(dong.count("export AGY_CLI_DISABLE_AUTO_UPDATE=1") == 1 and "export FOO=1" in dong, f"env file: {dong}")
# ---------- H: khối trong hook ----------
MO, DONG = "# >>> agent-creds (wp1039)", "# <<< agent-creds (wp1039)"
PY_GIA = "#!{exe}\nimport json, sys\nopen({log!r}, 'a').write(json.dumps(sys.argv[1:]) + '\\n')\nsys.exit(3)\n"   # argv nguyên danh sách (F09)
RE_NAP, RE_CAI = re.compile(r'cloud_agent_creds\.py"?\s+nap\b'), re.compile(r'cloud_agent_creds\.py"?\s+cai-agy\b')
def h1_vi_tri_khoi_trong_hook():
    dong = HOOK.read_text(encoding="utf-8").splitlines()
    bang(dong.count(MO) == 1 and dong.count(DONG) == 1, "dấu khối phải xuất hiện đúng 1 lần mỗi dấu")
    i, j = dong.index(MO), dong.index(DONG)
    pip = max(n for n, d in enumerate(dong) if re.match(r'\s*(if\s+)?"\$PY" -m pip install --quiet -r requirements\.txt', d))   # lệnh pip THẬT
    pol = next(n for n, d in enumerate(dong) if "codex_env_policy.py" in d)
    bang(pip < i < j < pol, f"khối ở dòng {i}–{j}, phải sau {pip} và trước {pol}")
    lenh = [d if not d.lstrip().startswith("#") else "" for d in dong]   # chữ trong chú thích không phải lời gọi (F05)
    khoi, ngoai = lenh[i + 1:j], lenh[:i] + lenh[j + 1:]
    for rx in (RE_NAP, RE_CAI):
        bang([bool(rx.search(d)) for d in khoi].count(True) == 1, f"{rx.pattern}: trong khối phải đúng 1")
        bang(not any(rx.search(d) for d in ngoai), f"{rx.pattern}: ngoài khối phải 0")
        bang(not rx.search(_git_base(".claude/hooks/session-start.sh")), f"vế âm: base đã có {rx.pattern}")
    vt = [next(n for n, d in enumerate(khoi) if rx.search(d)) for rx in (RE_NAP, RE_CAI)]
    bang(vt[0] < vt[1], "nap phải đứng trước cai-agy")
def h2_khoi_song_sot_set_e():
    _posix()
    dong = HOOK.read_text(encoding="utf-8").splitlines()
    bash = bash_nen.tim_bash()[0]
    bang(bash, "POSIX mà không có bash dùng được — không được bỏ qua (F06)")
    with tempfile.TemporaryDirectory() as t:
        _ghi(py := Path(t) / "py_gia", PY_GIA.format(exe=sys.executable, log=str(Path(t, "argv"))), True)
        than = "\n".join(dong[dong.index(MO) + 1:dong.index(DONG)])
        r = subprocess.run([bash, "-c", 'set -euo pipefail; PY="$1"; GOC="$2"\n' + than, "h2", str(py), t], capture_output=True, text=True, timeout=60)
        goi = [json.loads(x) for x in Path(t, "argv").read_text(encoding="utf-8").splitlines()] if Path(t, "argv").exists() else []
    bang(r.returncode == 0 and "[session-start] " in r.stdout, f"rc={r.returncode} {r.stdout!r} {r.stderr!r}")
    bang(goi == [[f"{t}/ops/cloud_agent_creds.py", "nap"], [f"{t}/ops/cloud_agent_creds.py", "cai-agy"]], f"PY nhận {goi}")
def h3_ten_nang_luc():
    moi, cu = [set(next(x for x in v.splitlines() if x.startswith("# hook-nang-luc:")).split()[2:])
               for v in (HOOK.read_text(encoding="utf-8"), _git_base(".claude/hooks/session-start.sh"))]
    bang({"agent-creds-bootstrap", "agy-ghim"} <= moi, f"thiếu tên năng lực mới: {moi}")
    bang(cu <= moi, f"mất tên cũ: {cu - moi}")
CA = {k: v for k, v in dict(globals()).items() if re.fullmatch(r"[a-h]\d+_\w+", k) and callable(v)}
# ---------- đột biến: (tên, tệp, chuỗi gốc | None, thay (chuỗi | hàm), ca đích). Chuỗi gốc phải xuất hiện ĐÚNG MỘT lần ----------
def _doi_khoi_len_tieu_de(s):   # đặt khối ngay sau dòng tiêu đề pip, TRƯỚC lệnh pip thật
    i, j = s.index(MO), s.index(DONG) + len(DONG) + 1
    k = s.index("\n", s.index("# --- phụ thuộc Python của kho")) + 1
    return s[:k] + s[i:j] + s[k:i] + s[j:]
def _doi_khoi_ra_sau(s):
    i, j = s.index(MO), s.index(DONG) + len(DONG) + 1
    return s[:i] + s[j:] + s[i:j]
DOT_BIEN = (
    ("A1_goi_bat_ke_khoa", "ma", "    if not khoa:\n", "    if False:\n", "a1_thieu_khoa_khong_goi_tl"),
    ("A2_chuyen_tiep_nguyen_van", "ma", '        if "agent_creds:" in d:\n            dong_agent.append(d)\n        else:\n            print(d)', "        print(d)", "a2_loc_dong_agent_cua_bootstrap"),
    ("A3_bo_nhanh_khong_dong", "ma", '    if not dong_agent:\n        return f"KHÔNG ĐO ĐƯỢC — bootstrap thoát rc={rc} trước bước agent"\n', "", "a3_bang_sau_ca_hop_dong"),
    ("A3_bo_kiem_tap_trang_thai", "ma", " or s not in TRANG_THAI", "", "a3_bang_sau_ca_hop_dong"),
    ("A4_bo_giet", "ma", "os.killpg(p.pid, signal.SIGKILL) if", "None if", "a4_qua_han_giet_ca_nhom"),
    ("A4_chi_giet_cha", "ma", "os.killpg(p.pid, signal.SIGKILL) if", "p.kill() if", "a4_qua_han_giet_ca_nhom"),
    ("A9_mat_log_khi_khong_dung_duoc", "ma", "        ra = e.output or b\"\"\n", "        ra = b\"\"\n", "a9_loi_gui_tin_hieu_khong_bao_da_dung"),
    ("A4_bo_chuyen_tiep_log_khi_qua_han", "ma", "(da, ra), ly = _giet_nhom(p),", "(da, _), ra, ly = _giet_nhom(p), b\"\",", "a4_qua_han_giet_ca_nhom"),
    ("A9_bo_hau_kiem_nhom", "ma", "            os.killpg(p.pid, 0)\n", "            raise ProcessLookupError\n", "a9_loi_gui_tin_hieu_khong_bao_da_dung"),
    ("A11_bo_subreaper", "ma", "_SUBREAPER = ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) == 0", "_SUBREAPER = True", "a11_subreaper_va_esrch"),
    ("A11_waitpid_toan_cuc", "ma", "os.waitpid(-p.pid, os.WNOHANG)", "os.waitpid(-1, os.WNOHANG)", "a11_subreaper_va_esrch"),
    ("A11_eperm_la_dung", "ma", "        except OSError:\n            return False, ra\n        if time", "        except OSError:\n            return True, ra\n        if time", "a11_subreaper_va_esrch"),
    ("A11_subreaper_muon_nap", "ma", None, lambda s: s.replace("        _dat_subreaper()\n        p = subprocess.Popen([sys", "        p = subprocess.Popen([sys", 1).replace("    except OSError as e:\n        print(f\"agent_creds: KHÔNG ĐO ĐƯỢC — không chạy", "    except OSError as e:\n        _dat_subreaper()\n        print(f\"agent_creds: KHÔNG ĐO ĐƯỢC — không chạy", 1), "a11_subreaper_va_esrch"),
    ("A11_subreaper_muon_version", "ma", None, lambda s: s.replace("        _dat_subreaper()\n        p = subprocess.Popen([str(agy)", "        p = subprocess.Popen([str(agy)", 1).replace("    except OSError:\n        return False\n    try:", "    except OSError:\n        return _dat_subreaper() and False\n    try:", 1), "a11_subreaper_va_esrch"),
    ("A11_bo_waitpid", "ma", "            while os.waitpid(-p.pid, os.WNOHANG)[0] > 0:", "            while False:", "a11_subreaper_va_esrch"),
    ("A11_khong_prctl_van_bao_dung", "ma", "    if os.name == \"nt\" or not _dat_subreaper():\n        return False, ra\n", "", "a11_subreaper_va_esrch"),
    ("A4_bo_timeout", "ma", "p.communicate(timeout=han)", "p.communicate()", "a4_qua_han_giet_ca_nhom"),
    ("A5_nhan_0", "ma", "0 < v <= 86400", "0 <= v <= 86400", "a5_doc_timeout"),
    ("A5_bo_tran_tren", "ma", "0 < v <= 86400", "0 < v", "a5_doc_timeout"),
    ("A6_bo_no_nlm", "ma", '"code", "--no-nlm"]', '"code"]', "a6_argv_va_trinh_thong_dich"),
    ("A6_them_require", "ma", '"code", "--no-nlm"]', '"code", "--no-nlm", "--require-agent-creds"]', "a6_argv_va_trinh_thong_dich"),
    ("A7_stderr_ke_thua", "ma", "stdout=subprocess.PIPE, stderr=subprocess.STDOUT,\n", "stdout=subprocess.PIPE, stderr=None,\n", "a7_che_master_key"),
    ("A7_bo_che", "ma", '.replace(khoa, "***")', "", "a7_che_master_key"),
    ("A8_tra_rc_bootstrap", "ma", "    return 0  # nap: luôn 0", "    return rc  # nap", "a8_nap_luon_rc0"),
    ("B1_khong_ghi", "ma", "        _ghi_nguyen_tu(agy, tf.extractfile(tv[0]).read(), 0o755)", "        pass", "b1_chua_co_thi_tai_va_ghi"),
    ("B2_bo_kiem_sha", "ma", "    if hashlib.sha512(du_lieu).hexdigest() != muc[1]:", "    if False:", "b2_sha512_lech_khong_ghi"),
    ("B3_luon_tai", "ma", "    if _ban_khop(agy):", "    if False:", "b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay"),
    ("B4_loi_giai_ma_thoat_khoi_kiem_ban", "ma", "    return p.returncode == 0 and AGY_VER in", '    return p.returncode == 0 and ra.encode("ascii") and AGY_VER in', "b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay"),
    ("B4_qua_han_chi_giet_cha", "ma", "        return _giet_nhom(p)[0] and False", "        return p.kill() or False", "b10_version_treo_giet_ca_nhom"),
    ("B4_so_chuoi_con", "ma", 'AGY_VER in re.split(r"[\\s,;()]+", ra)', "AGY_VER in ra", "b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay"),
    ("B4_bien_chi_chan_so", "ma", 'AGY_VER in re.split(r"[\\s,;()]+", ra)', 're.search(r"(?<![\\d.])" + re.escape(AGY_VER) + r"(?!\\.?\\d)", ra) is not None', "b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay"),
    ("B4_chi_kiem_co_mat", "ma", "    if _ban_khop(agy):", "    if agy.is_file():", "b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay"),
    ("B5_roi_ve_linux_amd64", "ma", "    muc = NEN.get(k)", '    muc = NEN.get(k) or NEN["linux_amd64"]', "b5_nen_ngoai_bang"),
    ("B6_extractall", "ma", "        tv = tf.getmembers()\n", '        tf.extractall(agy.parent, filter="fully_trusted")\n        tv = tf.getmembers()\n', "b6_tarball_doc_tu_choi"),
    ("B7_goi_agy_install", "ma", '    print(f"agy: ✓ đã cài', '    subprocess.run([str(agy), "install"], capture_output=True, timeout=15)\n    print(f"agy: ✓ đã cài', "b7_khong_goi_agy_install"),
    ("B8_doi_mot_ky_tu_sha", "ma", '"ea01c73b77', '"fa01c73b77', "b8_hang_ghim_dung_spec"),
    ("B9_bo_musl", "ma", ' + ("_musl" if he == "linux" and musl else "")', "", "b9_luat_chon_nen"),
    ("C1_ghi_de_ca_tep", "ma", '    d = {**d, "modelProvider": "gemini"}', '    d = {"modelProvider": "gemini"}', "c13_gop_model_provider_khong_ghi_khoa"),
    ("C2_ghi_de_khi_parse_loi", "ma", 'return print(f"agy: ⚠ settings.json không đọc được', 'd = {}; print(f"', "c2_settings_khong_phai_object_khong_dung"),
    ("C3_ghi_api_key", "ma", '    d = {**d, "modelProvider": "gemini"}', '    d = {**d, "modelProvider": "gemini", "apiKey": os.environ.get("GEMINI_API_KEY", "")}', "c13_gop_model_provider_khong_ghi_khoa"),
    ("D2_ghi_cwd_khi_khong_dat_bien", "ma", '    if env.get("CLAUDE_ENV_FILE"):\n        p = Path(env["CLAUDE_ENV_FILE"])', '    if True:\n        p = Path(env.get("CLAUDE_ENV_FILE") or "env.sh")', "d2_khong_env_file_khong_tao_tep"),
    ("D1_noi_moi_luot", "ma", "        if cu.count(DONG_ENV) != 1:\n            _ghi_nguyen_tu(p, (\"\\n\".join([x for x in cu if x != DONG_ENV] + [DONG_ENV])",
     "        if True:\n            _ghi_nguyen_tu(p, (\"\\n\".join(cu + [DONG_ENV])", "d1_env_file_dung_mot_dong"),
    ("H1_doi_khoi_ra_sau_doctor", "hook", None, _doi_khoi_ra_sau, "h1_vi_tri_khoi_trong_hook"),
    ("H1_khoi_ngay_sau_tieu_de_truoc_pip", "hook", None, _doi_khoi_len_tieu_de, "h1_vi_tri_khoi_trong_hook"),
    ("H2_bo_or_true", "hook", "\"$GOC/ops/cloud_agent_creds.py\" nap 2>&1 | sed 's/^/[session-start] /' || MA_AC=$?", "\"$GOC/ops/cloud_agent_creds.py\" nap 2>&1 | sed 's/^/[session-start] /'", "h2_khoi_song_sot_set_e"),
    ("H2_gop_doi_so", "hook", '"$GOC/ops/cloud_agent_creds.py" nap 2>&1', '"$GOC/ops/cloud_agent_creds.py nap" 2>&1', "h2_khoi_song_sot_set_e"),
    ("H2_va_cham_ngoac", "hook", '"$GOC/ops/cloud_agent_creds.py" nap 2>&1', '"$GOC/ops/cloud_agent_creds.py][nap" 2>&1', "h2_khoi_song_sot_set_e"),
    ("H2_bo_qua_nap", "hook", 'MA_AC=0; "$PY" "$GOC/ops/cloud_agent_creds.py" nap', 'MA_AC=0; : "$PY" "$GOC/ops/cloud_agent_creds.py" nap', "h2_khoi_song_sot_set_e"),
    ("H3_xoa_ten_cu", "hook", " rg-co-chay-truoc-cargo ", " ", "h3_ten_nang_luc"),
)
TU_KIEM = (   # F2 — (tên, tệp, gốc, thay, ca đích, hạng mong đợi)
    ("vo_can_qua_except_doi_kieu", "ma", "    he = he.lower()\n", "    raise AttributeError('vo can')\n", "b9_luat_chon_nen", "TIN_DUNG_GIA"),
    ("chi_them_chu_thich", "ma", "TIMEOUT_MAC_DINH, HAN_VERSION, HAN_DON = 180, 15, 10\n", "TIMEOUT_MAC_DINH, HAN_VERSION, HAN_DON = 180, 15, 10  # vo hai\n", "a5_doc_timeout", "SONG_SOT"),
)
def phan_hang(rc, ra, ten_ca):
    """GIET chỉ khi con thoát 3 VÀ có dòng `DO:<đúng ca đích>:` — `AssertionError` trần hay ca khác là tín dụng giả."""
    if rc == 3:
        return "GIET" if re.search(rf"^DO:{re.escape(ten_ca)}:", ra, re.M) else "TIN_DUNG_GIA"
    return {0: "SONG_SOT", 5: "BO_QUA", 4: "TIN_DUNG_GIA"}.get(rc, "HONG")
def chay_dot_bien(ten, tep, cu, moi, ten_ca):
    nguon = MA if tep == "ma" else HOOK
    goc = nguon.read_text(encoding="utf-8")
    if cu is not None and (goc.count(cu) != 1 or cu == moi):
        return "HONG", f"neo phải xuất hiện đúng 1 lần (thấy {goc.count(cu)})"
    with tempfile.TemporaryDirectory(prefix="cac_db_") as t:
        kq = []
        for nhan, nd in (("goc", goc), ("db_" + ten, moi(goc) if cu is None else goc.replace(cu, moi))):
            (ban := Path(t) / f"{nhan}_{nguon.name}").write_text(nd, encoding="utf-8", newline="\n")
            r = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--mot-ca", ten_ca], capture_output=True, timeout=600,
                               env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", **{"CAC_MA" if tep == "ma" else "CAC_HOOK": str(ban)}))
            kq.append((r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")))
            if nhan == "goc" and r.returncode != 0:
                return ("BO_QUA", "") if r.returncode == 5 else ("HONG", f"ca đích không xanh trên bản gốc (rc={r.returncode}): {kq[0][1][-200:]}")
    return phan_hang(kq[1][0], kq[1][1], ten_ca), kq[1][1].strip()[-200:]
def chay_ca(ten):
    try:
        return CA[ten]() or (0, "")
    except TinHieuChotCa as e:
        return 3, f"DO:{ten}:{e}"
    except BoQua as e:
        return 5, f"BO QUA {ten}: {e}"
    except Exception as e:
        return 4, f"HONG:{ten}:{type(e).__name__}: {e}"
def main(argv):
    if len(argv) == 2 and argv[0] == "--mot-ca" and argv[1] in CA:
        rc, dong = chay_ca(argv[1])
        return print(dong) or rc
    if argv:
        return print("dung: cloud_agent_creds_test.py [--mot-ca TEN]", file=sys.stderr) or 2
    kq = [chay_ca(ten) for ten in CA]
    print("".join(f"[{d}]\n" for rc, d in kq if rc), end="")
    dat, tong = sum(rc == 0 for rc, _ in kq), sum(rc != 5 for rc, _ in kq)
    db = [(ten, *chay_dot_bien(ten, tep, cu, moi, dich)) for ten, tep, cu, moi, dich in DOT_BIEN]
    tk = [(ten, mong, chay_dot_bien(ten, tep, cu, moi, dich)[0]) for ten, tep, cu, moi, dich, mong in TU_KIEM]
    tk += [("ca_khac_ca_dich", "TIN_DUNG_GIA", phan_hang(3, "DO:a1_thieu_khoa_khong_goi_tl:x", "a2_loc_dong_agent_cua_bootstrap")),
           ("assertion_tran", "TIN_DUNG_GIA", phan_hang(4, "HONG:b9_luat_chon_nen:AssertionError: lỗi", "b9_luat_chon_nen"))]
    xau = [f"{ten}: {h} {ct}" for ten, h, ct in db if h not in ("GIET", "BO_QUA")]
    n_db = sum(h != "BO_QUA" for _, h, _ in db)
    loi_tk = [f"{ten}: mong {mong}, duoc {h}" for ten, mong, h in tk if h != mong]
    print(f"CA: {dat}/{tong} dat\n" + "".join(f"[DOT BIEN KHONG BI GIET DUNG] {x}\n" for x in xau) + f"DOT BIEN: {n_db - len(xau)}/{n_db} bi giet dung ly do")
    print("".join(f"[TU KIEM] {x}\n" for x in loi_tk) + f"TU KIEM PHAN HANG: {'DAT' if not loi_tk else 'DO'} ({len(tk)} dot bien)")
    ok = dat == tong > 0 and n_db > 0 and not xau and not loi_tk
    return print(f"TONG: {'DAT' if ok else 'DO'}") or (0 if ok else 1)
if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
