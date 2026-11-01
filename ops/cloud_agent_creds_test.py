#!/usr/bin/env python3
"""Phản chứng cho `ops/cloud_agent_creds.py` + khối hook (CLOUD-SETUP-P2B-WIRE r1, `nghiem_thu` A–D, H, F2). Ca = hàm `<a-h><số>_…`;
`nap` chạy con trên cây tạm có `scripts/tl.py` GIẢ, `cai-agy` in-process (tải giả ĐẾM lời gọi). Đột biến sửa BẢN SAO TẠM; chỉ `bang()`
ném `TinHieuChotCa` (con thoát 3 + `DO:<ca>:`); lỗi vô can thoát 4 = TÍN DỤNG GIẢ; 5 = bỏ qua (Windows, hay cây rời không .git).
Ca `p3<a|b|c|s><số>_…` (#1089, spec CLOUD-SETUP-P3-WRITEBACK r2 `nghiem_thu`): `ghi-nguoc` in-process trên Drive giả GIỮ TRẠNG THÁI;
B trích NGUYÊN VĂN `agent_creds_put` từ references/Code.2.21.2q.gs, chạy bằng `node` với LockService/Drive/... giả."""
import ast, atexit, base64, contextlib, ctypes, hashlib, importlib.util, inspect, io, json, os, re, shutil, subprocess, sys, tarfile, tempfile, time  # noqa: E401
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

sys.dont_write_bytecode = True
for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding="utf-8", errors="backslashreplace")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bash_nen  # noqa: E402 — bộ giải `bash` dùng chung (#570)
sys.path.insert(0, str(HERE.parent / "scripts"))
import gas, gws_cred_store, tl_gws  # noqa: E401,E402 — CHÍNH các module helper import (sys.modules dùng chung ⇒ vá được)
_CODEX_TAM = tempfile.mkdtemp(prefix="cac_codex_home_")   # nap/ghi-nguoc ghi/xoá DẤU ở CODEX_HOME: không bao giờ đụng ~/.codex thật
os.environ["CODEX_HOME"] = _CODEX_TAM
atexit.register(shutil.rmtree, _CODEX_TAM, True)

MA = Path(os.environ.get("CAC_MA") or HERE / "cloud_agent_creds.py")
HOOK = Path(os.environ.get("CAC_HOOK") or HERE.parent / ".claude/hooks/session-start.sh")
GS = Path(os.environ.get("CAC_GS") or HERE.parent / "references/Code.2.21.2q.gs")
SETTINGS = Path(os.environ.get("CAC_SETTINGS") or HERE.parent / ".claude/settings.json")
BASE_P3 = "8f123b27b338e5e173a668209eb4904f49dd611b"   # base của lease wp1089 — vế âm S1
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
def _git_base(path, base=BASE):   # tệp ở BASE; chỉ tha (BoQua) khi cây là bản sao rời không `.git` (CLAUDE.md, "ca có MẶT ≠ ca có ĐO")
    if not (HERE.parent / ".git").exists():
        raise BoQua("cây không có .git — không đo được vế âm trên base")
    r = subprocess.run(["git", "-C", str(HERE.parent), "show", f"{base}:{path}"], capture_output=True)
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
# ---------- P3 (#1089): `ghi-nguoc` — A/C in-process, Drive giả GIỮ TRẠNG THÁI ----------
SEN_KHOA, SEN_RT, SEN_ENV = "SENTINEL-khoa-p3-abcdefghijklmnop", "SENTINEL-refresh-p3-77c1", "SENTINEL-env-p3-claude"
LR_CU, LR_MOI, TEN_DAU, TIEN_TO = "2026-10-27T11:35:54.511Z", "2026-11-01T02:00:00.000Z", ".tra-luat-agent-creds-dau.json", "agent_creds_ghi_nguoc: "
def _auth(lr):
    return {"auth_mode": "chatgpt", "tokens": {"refresh_token": SEN_RT, "access_token": "a"}, "last_refresh": lr}
def _bundle(rev, lr, claude="tok-claude-cu", ag="ag-cu"):
    return gws_cred_store.encrypt(json.dumps({"schema": 1, "rev": rev, "codex_auth": _auth(lr), "claude_oauth_token": claude,
                                              "antigravity_api_key": ag, "updated_at": "x"}).encode("utf-8"), SEN_KHOA)
def _md5(b):
    return hashlib.md5(b).hexdigest()
class DriveGia:
    """byte + md5 đổi THẬT sau mỗi lần ghi thành công; đếm tải/ping/post/ghi. `chen`: phiên khác ghi đúng trước lần post đầu."""
    def __init__(s, blob, ping="2.21.2q", ma=None, md5_sai=False, sau_ghi=None, chen=None, treo=0):
        s.blob, s.ping, s.ma, s.md5_sai, s.sau_ghi, s.chen, s.treo = blob, ping, ma, md5_sai, sau_ghi, chen, treo
        s.dem, s.gui = {"tai": 0, "ping": 0, "post": 0, "ghi": 0}, []
    def tai(s, fid, timeout=120.0):
        s.dem["tai"] += 1
        return s.sau_ghi if s.sau_ghi and s.dem["ghi"] else s.blob
    def get(s, action, **kw):
        s.dem["ping"] += 1
        if s.ping == "nem":
            raise RuntimeError("Thiếu TL_WEBAPP/TL_TOKEN")
        return {"ok": False, "error": "webapp GET ping: URLError"} if s.ping is None else {"ok": True, "version": s.ping}
    def post(s, action, fileId=None, expect_md5=None, b64=None, timeout=None, **kw):
        s.dem["post"] += 1
        s.gui.append(b64)
        if s.treo:
            return time.sleep(s.treo) or {"ok": False, "error": "TREO"}
        if s.chen and s.dem["post"] == 1:
            s.blob = s.chen
        if s.ma:
            return {"ok": False, "error": s.ma}
        if fileId != tl_gws.AGENT_CREDS_FILEID or expect_md5 != _md5(s.blob):
            return {"ok": False, "error": "CAS_CONFLICT", "md5": _md5(s.blob)}
        s.blob, s.dem["ghi"] = base64.b64decode(b64), s.dem["ghi"] + 1
        return {"ok": True, "md5": "0" * 32 if s.md5_sai else _md5(s.blob), "size": len(s.blob)}
class _Buf(io.StringIO):   # `main` gọi reconfigure trên stdout/stderr
    def reconfigure(self, **k):
        pass
def chay_gn(dr, dia=LR_MOI, khoa=SEN_KHOA, remote="true", neu_doi=False, dau=None, han=25.0, auth=None, argv=None):
    m = nap_mod()
    with tempfile.TemporaryDirectory(prefix="cac_gn_") as t:
        ch, out, err = Path(t), _Buf(), _Buf()
        (ch / "auth.json").write_text(json.dumps(_auth(dia)) if auth is None else auth, encoding="utf-8")
        dau is None or (ch / TEN_DAU).write_text(dau, encoding="utf-8")
        auth_truoc, env = (ch / "auth.json").read_bytes(), {k: v for k, v in (("CLAUDE_CODE_REMOTE", remote), ("TL_MASTER_KEY", khoa)) if v is not None}
        with mock.patch.dict(os.environ, {"CODEX_HOME": t, "CLAUDE_CODE_OAUTH_TOKEN": SEN_ENV, "GEMINI_API_KEY": SEN_ENV, **env}), \
             mock.patch.object(tl_gws, "_public_curl_bytes", dr.tai), mock.patch.object(gas, "get", dr.get), mock.patch.object(gas, "post", dr.post), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            t0 = time.monotonic()
            rc = m.ghi_nguoc(neu_doi, env=env, han=han) if argv is None else m.main(argv)
            giay = time.monotonic() - t0
        f = ch / TEN_DAU
        return SimpleNamespace(rc=rc, ra=out.getvalue() + err.getvalue(), giay=giay, dr=dr, auth_doi=(ch / "auth.json").read_bytes() != auth_truoc,
                               dau=f.read_text(encoding="utf-8") if f.exists() else None, quyen=f.stat().st_mode & 0o777 if f.exists() else None,
                               dong=[d for d in (out.getvalue() + err.getvalue()).splitlines() if d.startswith(TIEN_TO)])
def _mang(k):
    return k.dr.dem["tai"] + k.dr.dem["ping"] + k.dr.dem["post"]
def _trang(k, s):
    bang(k.rc == 0 and len(k.dong) == 1 and k.dong[0].startswith(f"{TIEN_TO}{s}"), f"mong {s}: rc={k.rc} {k.dong} {k.ra[-300:]!r}")
def p3a1_khong_phai_cloud():
    for remote in (None, "false"):
        k = chay_gn(DriveGia(_bundle(3, LR_CU)), remote=remote)
        _trang(k, "BỎ QUA — không phải phiên cloud")
        bang(_mang(k) == 0, f"remote={remote!r}: {k.dr.dem}")
def p3a2_khoa_yeu():
    for khoa in (None, "abcdefghijkl" + "a" * 19, "abcdefghijk" + "a" * 29):
        k = chay_gn(DriveGia(_bundle(3, LR_CU)), khoa=khoa)
        _trang(k, "BỎ QUA")
        bang(_mang(k) == 0, f"khoá {len(khoa or '')} ký tự: {k.dr.dem}")
    k = chay_gn(DriveGia(_bundle(3, LR_CU), ping="2.21.2p"), khoa="abcdefghijkl" + "a" * 20)
    bang(k.dr.dem["ping"] == 1 and not k.dong[0].startswith(f"{TIEN_TO}BỎ QUA"), f"khoá 32/12 phải đi tiếp: {k.dong}")
def p3a3_cong_phien_ban():
    for v in ("2.21.2p", "2.21.2", "abc", None, "nem"):
        k = chay_gn(DriveGia(_bundle(3, LR_CU), ping=v))
        _trang(k, "KHÔNG HỖ TRỢ — webapp " + ("không đo được" if v in (None, "nem") else v))
        bang(k.dr.dem["post"] == 0, f"{v!r}: post {k.dr.dem}")
    for v in ("2.21.2q", "2.22.0", "2.21.10"):
        k = chay_gn(DriveGia(_bundle(3, LR_CU), ping=v))
        _trang(k, "ĐÃ GHI — rev=4")
def p3a4_da_cu():
    for lr in (LR_MOI, "2026-11-02T00:00:00Z"):
        k = chay_gn(DriveGia(_bundle(3, lr)))
        _trang(k, "ĐÃ CŨ — bỏ ghi")
        bang(k.dr.dem["post"] == 0 and not k.auth_doi, f"bundle {lr}: post {k.dr.dem}, auth.json đổi={k.auth_doi}")
def p3a5_da_ghi_giu_khoa_cu():
    k = chay_gn(DriveGia(_bundle(3, LR_CU)))
    _trang(k, "ĐÃ GHI — rev=4")
    p = json.loads(gws_cred_store.decrypt(k.dr.blob, SEN_KHOA))
    bang(p["codex_auth"] == _auth(LR_MOI) and p["schema"] == 1 and p["rev"] == 4, f"payload: rev={p.get('rev')}")
    bang(p.get("claude_oauth_token") == "tok-claude-cu" and p.get("antigravity_api_key") == "ag-cu", "rơi/đổi khoá cũ")
    bang(SEN_ENV not in json.dumps(p), "khoá từ môi trường lọt vào payload")
def p3a6_cas_tai_lai_dung_ban_moi():
    k = chay_gn(DriveGia(_bundle(3, LR_CU), chen=_bundle(10, "2026-10-30T00:00:00Z", claude="tok-phien-khac")))
    _trang(k, "ĐÃ GHI — rev=11")
    p = json.loads(gws_cred_store.decrypt(k.dr.blob, SEN_KHOA))
    bang(k.dr.dem["post"] == 2 and k.dr.dem["tai"] >= 2 and p["rev"] == 11 and p["claude_oauth_token"] == "tok-phien-khac", f"{k.dr.dem} rev={p['rev']}")
def p3a7_cas_lap_dung_ba():
    for ma in ("CAS_CONFLICT", "LOCK_BUSY"):
        k = chay_gn(DriveGia(_bundle(3, LR_CU), ma=ma))
        _trang(k, "KHÔNG ĐO ĐƯỢC — xung đột CAS lặp")
        bang(k.dr.dem["post"] == 3, f"{ma}: {k.dr.dem['post']} lời gọi post")
def p3a8_readback_lech():
    for dr in (DriveGia(_bundle(3, LR_CU), md5_sai=True), DriveGia(_bundle(3, LR_CU), sau_ghi=_bundle(9, LR_MOI))):
        k = chay_gn(dr, dau='{"last_refresh": "x", "md5": null}')
        _trang(k, "KHÔNG ĐO ĐƯỢC — readback lệch")
        bang(k.dau == '{"last_refresh": "x", "md5": null}', f"dấu bị đổi: {k.dau!r}")
SC = (dict(remote=None), dict(khoa="ngan"), dict(ping="2.21.2p"), dict(lr_bundle=LR_MOI), dict(), dict(chen=1), dict(ma="CAS_CONFLICT"),
      dict(ma="WEBAPP_LOI"), dict(md5_sai=True), dict(auth="{hỏng"))
def p3a9_mot_dong_khong_lo():
    for sc in SC:
        sc = dict(sc)
        dr = DriveGia(_bundle(3, sc.pop("lr_bundle", LR_CU)), **{k: sc.pop(k) for k in ("ping", "ma", "md5_sai") if k in sc},
                      chen=_bundle(10, LR_CU) if sc.pop("chen", None) else None)
        k = chay_gn(dr, **sc)
        bang(len(k.dong) == 1 and k.ra.count(TIEN_TO) == 1, f"{sc}: {len(k.dong)} dòng")
        lo = [x for x in (SEN_KHOA, SEN_RT, *[g for g in dr.gui if g]) if x in k.ra]
        bang(not lo, f"{sc}: đầu ra lộ {len(lo)} chuỗi bí mật")
def p3a13_phien_ban_la_van_mot_dong():   # review lượt 1 P3: version không hợp lệ có xuống dòng ⇒ vẫn ĐÚNG MỘT dòng
    k = chay_gn(DriveGia(_bundle(3, LR_CU), ping="abc\nphien-ban-khong-hop-le\r\x1b[2J"))
    _trang(k, "KHÔNG HỖ TRỢ — webapp abc?")
    bang(len(k.ra.splitlines()) == 1 and k.dr.dem["post"] == 0, f"đầu ra {len(k.ra.splitlines())} dòng: {k.ra!r}")
def p3a10_rc0_va_cu_phap():
    k = chay_gn(DriveGia(_bundle(3, LR_CU)), argv=["ghi-nguoc", "--la"])
    bang(k.rc == 2 and _mang(k) == 0, f"--la: rc={k.rc} {k.dr.dem}")
    for dr in (DriveGia(_bundle(3, LR_CU), ma="CAS_CONFLICT"), DriveGia(_bundle(3, LR_CU), ma="KHAC")):
        k = chay_gn(dr, argv=["ghi-nguoc"])
        bang(k.rc == 0 and len(k.dong) == 1, f"CAS thua: rc={k.rc} {k.dong}")
def p3a11_han_chot():
    k = chay_gn(DriveGia(_bundle(3, LR_CU), treo=2.5), han=0.5)
    _trang(k, "KHÔNG ĐO ĐƯỢC — quá 0.5 s")
    bang(k.giay < 1.5, f"xong sau {k.giay:.1f} s (hạn 0.5)")
SAU_TEN = ("AGENT_CREDS_FILEID", "_AGENT_CREDS_KEYS", "_MASTER_KEY_MIN_LEN", "_MASTER_KEY_MIN_DISTINCT", "_last_refresh_key", "_public_curl_bytes")
def p3a12_khong_dinh_nghia_lai_ten_tl_gws():
    cay, gan, nhap = ast.parse(MA.read_text(encoding="utf-8")), [], {}
    for n in ast.walk(cay):   # (a) AST mọi cấp
        if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)) and n.id in SAU_TEN:
            gan.append(n.id)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name in SAU_TEN:
            gan.append(n.name)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                if (ten := a.asname or a.name.split(".")[0]) in SAU_TEN:
                    (nhap.setdefault(ten, []).append(1) if isinstance(n, ast.ImportFrom) and n.module == "tl_gws" else gan.append(ten))
    bang(not gan, f"(a) helper tự gắn tên của tl_gws: {gan}")
    tran = {n.id for n in ast.walk(cay) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id in SAU_TEN}
    bang(all(len(nhap.get(t, [])) == 1 for t in tran), f"(a) tên trần không import đúng một lần từ tl_gws: {tran}")
    m = nap_mod()   # (b) chỉ hai hàm — hằng nhỏ/chuỗi intern làm `is` vô nghĩa (errata r2)
    for ten in ("_last_refresh_key", "_public_curl_bytes"):
        bang(not hasattr(m, ten) or getattr(m, ten) is getattr(tl_gws, ten), f"(b) {ten} không phải đối tượng của tl_gws")
def p3c1_nap_ghi_xoa_dau():
    _posix()
    for in_, co_dau in (("agent_creds: ĐÃ NẠP — rev=3; codex auth.json → /x (0600)\n", True),
                        ("agent_creds: ĐÃ NẠP — rev=3; codex auth.json: giữ bản đĩa (last_refresh mới hơn hoặc bằng)\n", False),
                        ("agent_creds: KHÔNG ĐO ĐƯỢC — y\n", False)):
        with tempfile.TemporaryDirectory() as t:
            (f := Path(t) / TEN_DAU).write_text('{"last_refresh": "cu", "md5": null}', encoding="utf-8")
            (Path(t) / "auth.json").write_text(json.dumps(_auth(LR_MOI)), encoding="utf-8")
            chay_nap({"in": in_}, them={"CODEX_HOME": t})
            d = json.loads(f.read_text(encoding="utf-8")) if f.exists() else None
            bang((d == {"last_refresh": LR_MOI, "md5": None} and f.stat().st_mode & 0o777 == 0o600) if co_dau else d is None, f"{in_.strip()}: dấu {d}")
def p3c4_nap_khong_chay_duoc_xoa_dau():   # review lượt 1 P2: lỗi KHỞI CHẠY bootstrap cũng phải xoá dấu
    with tempfile.TemporaryDirectory() as t:
        (f := Path(t) / TEN_DAU).write_text(json.dumps({"last_refresh": LR_MOI, "md5": None}), encoding="utf-8")
        k = chay_nap({}, xoa_tl=True, them={"CODEX_HOME": t})
        bang(k.ag and "không chạy được bootstrap" in k.ag[0] and not f.exists(), f"{k.ag}: dấu còn={f.exists()}")
def p3c2_neu_doi():
    k = chay_gn(DriveGia(_bundle(3, LR_CU)), neu_doi=True, dau=json.dumps({"last_refresh": LR_MOI, "md5": None}))
    bang(k.ra == "" and _mang(k) == 0, f"dấu == đĩa: {k.ra!r} {k.dr.dem}")
    for dau in (json.dumps({"last_refresh": LR_CU, "md5": None}), None, "[1]"):
        k = chay_gn(DriveGia(_bundle(3, LR_CU)), neu_doi=True, dau=dau)
        bang(k.dr.dem["tai"] >= 1 and len(k.dong) == 1, f"dấu {dau!r}: phải đi mạng {k.dr.dem}")
def p3c3_dau_sau_ghi_va_cu():
    k = chay_gn(DriveGia(_bundle(3, LR_CU)))
    bang(k.dau and json.loads(k.dau) == {"last_refresh": LR_MOI, "md5": _md5(k.dr.blob)} and (LA_WINDOWS or k.quyen == 0o600), f"sau ĐÃ GHI: {k.dau}")
    k = chay_gn(DriveGia(b := _bundle(3, "2026-11-05T00:00:00Z")))
    bang(k.dau and json.loads(k.dau) == {"last_refresh": "2026-11-05T00:00:00Z", "md5": _md5(b)}, f"sau ĐÃ CŨ: {k.dau}")
    bang(SEN_RT not in k.dau and "tokens" not in k.dau, "tệp dấu chứa token")
# ---------- P3 B: `agent_creds_put` trích NGUYÊN VĂN từ Code.2.21.2q.gs, chạy bằng node ----------
JS_GIA = r"""const c = require('crypto'), st = JSON.parse(require('fs').readFileSync(0, 'utf8')), nk = [];
let tep = Buffer.from(st.tep, 'base64'), ghi = 0, doc = 0;
const md5 = b => c.createHash('md5').update(b).digest('hex');
globalThis.PropertiesService = {getScriptProperties: () => ({getProperty: k => (st.prop && k === 'TL_AGENT_CREDS_FILEID') ? st.prop : null})};
globalThis.LockService = {getScriptLock: () => ({tryLock: ms => (nk.push('tryLock'), st.lock !== false), releaseLock: () => nk.push('releaseLock')})};
globalThis.Utilities = {newBlob: (b, mime) => ({b, mime}), base64Decode: s => {
  if (!/^[A-Za-z0-9+/]*={0,2}$/.test(s)) throw new Error('Could not decode string.');
  return Array.from(Buffer.from(s, 'base64')).map(x => x > 127 ? x - 256 : x); }};
globalThis.Drive = {Files: {get: (id, o) => (nk.push('get'), doc++, {md5Checksum: md5(tep)}),
  update: (r, id, blob, o) => { nk.push('update'); if (st.nem) throw new Error('ghi lỗi');
    ghi++; tep = Buffer.from(blob.b.map(x => x & 255)); return {id}; }}};
globalThis.DriveApp = {};
"""
JS_CHAY = r"""
let ra; try { ra = dispatchAction_('agent_creds_put', st.p); } catch (e) { ra = {nem: String(e.message)}; }
console.log(JSON.stringify({ra, nk, ghi, doc, sha: c.createHash('sha256').update(tep).digest('hex'), md5: md5(tep)}));
"""
def _node():
    if not (n := shutil.which("node")):
        bang(not (HERE.parent / ".git").exists(), "thiếu node trong kho có .git — ca B phải ĐO, không được bỏ qua")
        raise BoQua("cây rời không .git và không có node")
    return n
def _trich_gs():
    s = GS.read_text(encoding="utf-8")
    i, j = s.find("/* ============ AGENT CREDS (v2.21.2q, #1089) ============ */"), s.find("/* ============ /AGENT CREDS ============ */")
    case = [d for d in s.splitlines() if d.strip().startswith("case 'agent_creds_put':")]
    bang(0 <= i < j, "không tìm thấy khối AGENT CREDS trong Code.2.21.2q.gs")
    return s[i:j] + "\nfunction dispatchAction_(action, p){ switch(action){\n" + "\n".join(case) + "\n    default: throw new Error('Action không hỗ trợ: '+action);\n  }\n}\n"
TEP0, FID = b"ban-cu-cua-tl_agent_creds.enc", "fid-dung"
def chay_b(p=None, tep=TEP0, prop=FID, **st):
    with tempfile.TemporaryDirectory(prefix="cac_gs_") as t:
        (js := Path(t) / "b.js").write_text(JS_GIA + _trich_gs() + JS_CHAY, encoding="utf-8")
        # v1.36.69 (#1110: WinError 206 ở p3b4 — payload ~87K ký tự qua argv vượt trần 32767 của Windows) — đưa payload qua stdin
        r = subprocess.run([_node(), str(js)], input=json.dumps({"tep": base64.b64encode(tep).decode(), "prop": prop, "p": p or {}, **st}).encode(),
                           capture_output=True, timeout=60)
    bang(r.returncode == 0, f"node rc={r.returncode}: {r.stderr[-300:]!r}")
    return SimpleNamespace(**json.loads(r.stdout))
def _p(blob=b"ban-moi", md5=None, fid=FID):
    return {"fileId": fid, "expect_md5": _md5(TEP0) if md5 is None else md5, "b64": base64.b64encode(blob).decode()}
def p3b1_cas_khop_thi_ghi():
    k = chay_b(_p(b"ban-moi"))
    bang(k.ra.get("ok") is True and k.ghi == 1 and k.md5 == _md5(b"ban-moi") == k.ra.get("md5") and k.ra.get("size") == 7, f"{k.ra} ghi={k.ghi}")
def p3b2_cas_lech_khong_ghi():
    k = chay_b(_p(md5="f" * 32))
    bang(k.ra == {"ok": False, "error": "CAS_CONFLICT", "md5": _md5(TEP0)} and k.ghi == 0 and k.sha == hashlib.sha256(TEP0).hexdigest(), f"{k.ra} ghi={k.ghi}")
def p3b3_tham_so_sai_khong_ghi():
    for p, prop, ma in (({**_p(), "expect_md5": None}, FID, "EXPECT_MD5_REQUIRED"), (_p(md5="abc"), FID, "EXPECT_MD5_REQUIRED"),
                        (_p(), None, "AGENT_CREDS_NOT_CONFIGURED"), (_p(fid="fid-khac"), FID, "AGENT_CREDS_FILEID_MISMATCH")):
        k = chay_b(p, prop=prop)
        bang(k.ra == {"ok": False, "error": ma} and k.ghi == 0 and k.nk == [], f"mong {ma}: {k.ra} ghi={k.ghi} {k.nk}")
def p3b4_co_blob():
    for n, ok in ((65537, False), (0, False), (65536, True)):
        k = chay_b(_p(b"x" * n))
        bang((k.ra.get("ok") is True and k.ghi == 1) if ok else (k.ra == {"ok": False, "error": "BLOB_SIZE"} and k.ghi == 0), f"{n} byte: {k.ra}")
def p3b5_lock_ban():
    k = chay_b(_p(), lock=False)
    bang(k.ra == {"ok": False, "error": "LOCK_BUSY"} and k.doc == 0 and k.ghi == 0, f"{k.ra} đọc={k.doc} ghi={k.ghi}")
def p3b6_thu_tu_va_finally():
    bang(chay_b(_p()).nk == ["tryLock", "get", "update", "get", "releaseLock"], "thứ tự lock/đọc/ghi/đọc/nhả sai")
    k = chay_b(_p(), nem=True)
    bang("nem" in k.ra and k.nk[-1] == "releaseLock", f"ném ở bước ghi mà không nhả lock: {k.nk}")
def p3b7_ban_va_nhanh_case():
    s = GS.read_text(encoding="utf-8")
    bang(s.count("APP_VERSION = '2.21.2q'") == 1 and s.count("case 'agent_creds_put'") == 1, "APP_VERSION/case trong 2q")
    bang((HERE.parent / "references/Code.2.21.2p.gs").read_text(encoding="utf-8").count("case 'agent_creds_put'") == 0, "vế âm: 2p đã có case")
    bang(subprocess.run([_node(), "--check"], input=GS.read_bytes(), capture_output=True, timeout=60).returncode == 0, "node --check 2q đỏ")
# ---------- P3 S: hook `Stop` trong .claude/settings.json ----------
def _lenh_stop():
    h = json.loads(SETTINGS.read_text(encoding="utf-8"))["hooks"].get("Stop") or []
    bang(len(h) == 1 and len(h[0].get("hooks", [])) == 1, f"hooks.Stop phải đúng 1 hook: {h}")
    return h[0]["hooks"][0]
def p3s1_settings_co_stop():
    h, cu = _lenh_stop(), json.loads(_git_base(".claude/settings.json", BASE_P3))
    bang('ops/cloud_agent_creds.py\\" ghi-nguoc --neu-doi'.replace("\\", "") in h["command"].replace("\\", "") and "|| true" in h["command"] and h.get("timeout") == 30, f"Stop: {h}")
    moi = json.loads(SETTINGS.read_text(encoding="utf-8"))
    bang("Stop" not in cu["hooks"] and {k: v for k, v in moi["hooks"].items() if k != "Stop"} == cu["hooks"] and {k: v for k, v in moi.items() if k != "hooks"} == {k: v for k, v in cu.items() if k != "hooks"}, "khoá cũ của settings bị đổi")
def p3s2_stop_chay_that():
    _posix()
    bash = bash_nen.tim_bash()[0]
    bang(bash, "POSIX mà không có bash dùng được")
    with tempfile.TemporaryDirectory() as t:
        _ghi(Path(t) / "ops" / "cloud_agent_creds.py", f"import json, sys\nopen({str(Path(t, 'argv'))!r}, 'a').write(json.dumps(sys.argv[1:]) + '\\n')\nsys.exit(3)\n")
        r = subprocess.run([bash, "-c", _lenh_stop()["command"]], capture_output=True, text=True, timeout=60, env=dict(os.environ, CLAUDE_PROJECT_DIR=t))
        goi = Path(t, "argv").read_text(encoding="utf-8").splitlines() if Path(t, "argv").exists() else []
    bang(r.returncode == 0 and [json.loads(x) for x in goi] == [["ghi-nguoc", "--neu-doi"]], f"rc={r.returncode} argv={goi} {r.stderr[-200:]!r}")
CA = {k: v for k, v in dict(globals()).items() if re.fullmatch(r"(?:[a-h]|p3[abcs])\d+_\w+", k) and callable(v)}
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
    ("P3A1_bo_kiem_remote", "ma", '    if env.get("CLAUDE_CODE_REMOTE") != "true":\n        kq["v"] = ("BỎ QUA", "không phải phiên cloud")\n    elif', "    if", "p3a1_khong_phai_cloud"),
    ("P3A2_nguong_31", "ma", "if len(khoa) < tl_gws._MASTER_KEY_MIN_LEN or", "if len(khoa) < tl_gws._MASTER_KEY_MIN_LEN - 1 or", "p3a2_khoa_yeu"),
    ("P3A3_so_chuoi_tho", "ma", "if (b := ban_webapp(v)) is None or b < BAN_TOI_THIEU:", 'if (b := ban_webapp(v)) is None or v < "2.21.2q":', "p3a3_cong_phien_ban"),
    ("P3A4_lon_hon_thay_lon_hon_bang", "ma", "if tl_gws._last_refresh_key(ca) >= k_dia:", "if tl_gws._last_refresh_key(ca) > k_dia:", "p3a4_da_cu"),
    ("P3A5_doc_khoa_claude_tu_env", "ma", '"codex_auth": dia, "schema": 1,', '"codex_auth": dia, "claude_oauth_token": os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", ""), "schema": 1,', "p3a5_da_ghi_giu_khoa_cu"),
    ("P3A5_roi_khoa_cu", "ma", "**{k: cu[k] for k in tl_gws._AGENT_CREDS_KEYS if k in cu}, ", "", "p3a5_da_ghi_giu_khoa_cu"),
    ("P3A6_payload_tren_ban_lan_1", "ma", "            cu = _giai(store, khoa, blob)\n", '            cu = locals().get("cu") or _giai(store, khoa, blob)\n', "p3a6_cas_tai_lai_dung_ban_moi"),
    ("P3A7_mot_lan", "ma", "25.0, 3, (2, 21, 2", "25.0, 1, (2, 21, 2", "p3a7_cas_lap_dung_ba"),
    ("P3A7_lap_vo_han", "ma", "    for _ in range(LAN_CAS):\n", "    for _ in iter(int, 1):\n", "p3a7_cas_lap_dung_ba"),
    ("P3A8_bo_tai_lai", "ma", 'lai = _giai(store, khoa, tl_gws._public_curl_bytes(fid, timeout=con()) or b"")', "lai = moi", "p3a8_readback_lech"),
    ("P3A9_in_payload_loi", "ma", "        if isinstance(r, dict) and r.get(\"ok\") is True:\n            break\n", "        print(base64.b64encode(gui).decode(), file=sys.stderr)\n        if isinstance(r, dict) and r.get(\"ok\") is True:\n            break\n", "p3a9_mot_dong_khong_lo"),
    ("P3A10_rc_khac_0_khi_thua", "ma", "    return 0\ndef main(argv):", '    return 1 if kq.get("v", ("",))[0] == "KHÔNG ĐO ĐƯỢC" else 0\ndef main(argv):', "p3a10_rc0_va_cu_phap"),
    ("P3A11_bo_han_chot", "ma", "        t.join(han)\n", "        t.join()\n", "p3a11_han_chot"),
    ("P3A12_chep_hang_32", "ma", "def _codex_dir():", "_MASTER_KEY_MIN_LEN = 32\ndef _codex_dir():", "p3a12_khong_dinh_nghia_lai_ten_tl_gws"),
    ("P3A12_chep_fileid", "ma", "def _codex_dir():", f"AGENT_CREDS_FILEID = {tl_gws.AGENT_CREDS_FILEID!r}\ndef _codex_dir():", "p3a12_khong_dinh_nghia_lai_ten_tl_gws"),
    ("P3A12_dinh_nghia_lai_ham", "ma", "def _codex_dir():", inspect.getsource(tl_gws._last_refresh_key).replace("\n    import datetime as _dt\n", "\n    import datetime as _dt, re\n") + "def _codex_dir():", "p3a12_khong_dinh_nghia_lai_ten_tl_gws"),
    ("P3C1_ghi_dau_bat_ke", "ma", 'if kl.startswith("ĐÃ NẠP — ") and "codex auth.json → " in kl and isinstance(d, dict):', "if isinstance(d, dict):", "p3c1_nap_ghi_xoa_dau"),
    ("P3C2_so_khac", "ma", "and k_dia <= tl_gws._last_refresh_key(dau):", "and k_dia != tl_gws._last_refresh_key(dau):", "p3c2_neu_doi"),
    ("P3C2_bo_doc_dau", "ma", "    if neu_doi and isinstance(dau := _doc_json(_codex_dir() / TEN_DAU), dict)", "    if neu_doi and isinstance(dau := None, dict)", "p3c2_neu_doi"),
    ("P3C4_nap_loi_khoi_chay_giu_dau", "ma", '        return _dau_sau_nap("KHÔNG ĐO ĐƯỢC") or 0', "        return 0", "p3c4_nap_khong_chay_duoc_xoa_dau"),
    ("P3A13_in_version_tho", "ma", "re.sub(r'[^0-9A-Za-z._+-]', '?', v[:40])", "v[:40]", "p3a13_phien_ban_la_van_mot_dong"),
    ("P3C3_khong_dau_sau_cu", "ma", '            huy.is_set() or _ghi_dau(ca.get("last_refresh"), md5)\n', "", "p3c3_dau_sau_ghi_va_cu"),
    ("P3B1_khong_ghi", "gs", "    Drive.Files.update({}, fid, Utilities.newBlob(bytes, 'application/octet-stream'),\n                       {supportsAllDrives:true, fields:'id'});\n", "", "p3b1_cas_khop_thi_ghi"),
    ("P3B2_bo_so_cas", "gs", "    if (cur !== expect) return {ok:false, error:'CAS_CONFLICT', md5:cur};\n", "", "p3b2_cas_lech_khong_ghi"),
    ("P3B3_bo_kiem_fileid", "gs", "  if (String(p.fileId == null ? '' : p.fileId) !== fid) return {ok:false, error:'AGENT_CREDS_FILEID_MISMATCH'};\n", "", "p3b3_tham_so_sai_khong_ghi"),
    ("P3B4_nguong_lon_hon_bang", "gs", "bytes.length > AGENT_CREDS_MAX_BYTES_", "bytes.length >= AGENT_CREDS_MAX_BYTES_", "p3b4_co_blob"),
    ("P3B5_doc_md5_truoc_lock", "gs", "error:'BLOB_SIZE'};\n  var lock = LockService.getScriptLock();\n", "error:'BLOB_SIZE'};\n  Drive.Files.get(fid, {fields:'md5Checksum', supportsAllDrives:true});\n  var lock = LockService.getScriptLock();\n", "p3b5_lock_ban"),
    ("P3B6_bo_finally", "gs", "  } finally {\n    lock.releaseLock();\n  }\n}\n/* ============ /AGENT CREDS", "  } catch (e) { throw e; }\n}\n/* ============ /AGENT CREDS", "p3b6_thu_tu_va_finally"),
    ("P3B7_xoa_case", "gs", "    case 'agent_creds_put': return doAgentCredsPut_(p);", "   ", "p3b7_ban_va_nhanh_case"),
    ("P3S1_doi_lenh_subagentstop", "settings", '\\"$D/.claude/hooks/subagent_ghi_detect.py\\"\'"\n          }\n        ]\n      }\n    ],\n    "Stop"', '\\"$D/.claude/hooks/subagent_ghi_detect.py\\" --x\'"\n          }\n        ]\n      }\n    ],\n    "Stop"', "p3s1_settings_co_stop"),
    ("P3S2_bo_or_true", "settings", "ghi-nguoc --neu-doi || true'", "ghi-nguoc --neu-doi'", "p3s2_stop_chay_that"),
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
    nguon, bien = {"ma": (MA, "CAC_MA"), "hook": (HOOK, "CAC_HOOK"), "gs": (GS, "CAC_GS"), "settings": (SETTINGS, "CAC_SETTINGS")}[tep]
    goc = nguon.read_text(encoding="utf-8")
    if cu is not None and (goc.count(cu) != 1 or cu == moi):
        return "HONG", f"neo phải xuất hiện đúng 1 lần (thấy {goc.count(cu)})"
    with tempfile.TemporaryDirectory(prefix="cac_db_") as t:
        kq = []
        for nhan, nd in (("goc", goc), ("db_" + ten, moi(goc) if cu is None else goc.replace(cu, moi))):
            (ban := Path(t) / f"{nhan}_{nguon.name}").write_text(nd, encoding="utf-8", newline="\n")
            r = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--mot-ca", ten_ca], capture_output=True, timeout=600,
                               env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", **{bien: str(ban)}))
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
