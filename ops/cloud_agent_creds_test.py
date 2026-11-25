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
TLGWS = Path(os.environ.get("CAC_TLGWS") or HERE.parent / "scripts" / "tl_gws.py")
if os.environ.get("CAC_TLGWS"):   # WP1334: đột biến tl_gws chạy trên BẢN SAO TẠM, nạp dưới đúng tên `tl_gws` trước mọi import khác
    (_sp := importlib.util.spec_from_file_location("tl_gws", TLGWS)).loader.exec_module(sys.modules.setdefault("tl_gws", importlib.util.module_from_spec(_sp)))
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
BASE_PD = "ded5d41b1754ef05d87815f20c48203e6b00e58d"   # base của lease wp1334 — vế âm N1/N5b
LA_WINDOWS = os.name == "nt"
SPEC = HERE / "specs" / "cloud-setup-p2b-wire-r2.md"   # B8 so với CHÍNH bảng "Hằng ghim agy" của spec đóng băng, không chép lại
SPEC_SHA256 = "c43c08cd71e1f1580beb5abfc0cb9c57fe16c8ee9fe80e9035cca558e2ed8ee2"
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
        shutil.copy(TLGWS, t / "scripts" / "tl_gws.py")   # WP1334: `_ghi_dau` hỏi chốt `_trong_kho_git` của tl_gws
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
def _song_roi_don(pids, cho_chet=5.0):   # PID còn sống TRƯỚC khi dọn, rồi giết hết để ca không để rác
    # v1.36.69 (#1114: a11 sr=False đỏ trên CI — cháu đã nhận SIGKILL vẫn ở trạng thái R khi ống đã đóng, ~1,9% dưới tải,
    # tái hiện 34/1800) — chờ có hạn cho tiến trình đang thoát; ca CẦN còn sống (a9) gọi cho_chet=0
    het = time.monotonic() + cho_chet
    while (song := [x for x in pids if x is not None and _con_song(x)]) and time.monotonic() < het:
        time.sleep(0.02)
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
        song = _song_roi_don([nk.get("con"), *([int((t / "nk.chau").read_text())] if (t / "nk.chau").exists() else [])], cho_chet=0)
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
NOI_DUNG = b'#!/bin/sh\n[ -n "$CAC_AGY_NK" ] && echo "$*" >> "$CAC_AGY_NK"\necho antigravity 1.5.16\n'
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
    for cu, n in ((("antigravity 1.5.16", 0), 0), (("antigravity 1.6.0", 0), 0), (("antigravity 1.5.15", 0), 1), (("antigravity 1.5.16", 1), 1), (("\\0377", 0), 1),
                  (("antigravity 1.4.120", 0), 1), (("antigravity 1.5.16rc1", 0), 1), (("antigravity 1.5.16beta", 0), 1)):   # spec r2: SÀN, bản mới hơn được giữ
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
    bang(m.AGY_VER == "1.5.16" and sorted(m.NEN) == sorted(spec), f"AGY_VER={m.AGY_VER} khoá={sorted(m.NEN)}")
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
def d1_env_file_khong_dung():   # spec r2 D1': bật tự cập nhật ⇒ `cai-agy` không đụng CLAUDE_ENV_FILE
    with tempfile.TemporaryDirectory() as t, san_agy(nen="freebsd_amd64", env_them={"CLAUDE_ENV_FILE": str(f := Path(t) / "env.sh")}) as s:
        _ghi(f, "export FOO=1\n")
        truoc, _, _ = f.read_bytes(), s.chay(), s.chay()
        bang(f.read_bytes() == truoc, f"env file bị đổi: {f.read_bytes()!r}")
# ---------- G: `ghim-agy` (spec r2 Thay đổi 3) — MỘT HỢP ĐỒNG QUAN SÁT trên vòng đời tiến trình THẬT, lớp `ghim-output-oracle` (cross-review #1505 lượt 1–4) ----------
# Mỗi LỜI GỌI CLI là MỘT tiến trình con `python -I -B` chạy mã sản phẩm như `__main__` tới khi THOÁT THẬT (`sys.exit` của chính nó,
# `threading._shutdown`, atexit, finalizer, dọn module). rc, stdout, stderr lấy từ HỆ ĐIỀU HÀNH. Không có bản ghi "hoàn tất" nào:
# tiến trình cha chỉ đọc bằng chứng SAU KHI con đã chết (F01-t).
#   (1) audit hook của CPython sống tới hết vòng đời; mỗi sự kiện bị đẩy NGAY ra kênh riêng bằng `os.write` trên fd mở TRƯỚC khi
#       hook tồn tại (`os.write` không phát audit). Sự kiện ngoài `SU_KIEN_LANH` (danh sách CHO PHÉP) ⇒ ghi nhận rồi TỪ CHỐI.
#       `open` chỉ được coi là đọc khi chế độ ⊆ {r,b,t} VÀ cờ ⊆ `CO_DOC_CHO_PHEP` (danh sách CHO PHÉP, `g4` chứng minh từng cờ trên
#       runtime đang chạy); mọi cờ khác — kể cả `O_TEMPORARY` xoá-khi-đóng — là tác động tệp (F01-v).
#   (2) trạng thái ĐẦY ĐỦ của cwd/HOME/TEMP (có tệp mồi): chụp trước khi sinh con và sau khi con chết; thêm/mất/byte đổi đều ĐỎ.
#   (3) transport: `urllib`/`http.client` THẬT chạy nguyên (Request, opener, kiểm header/body, `socket.settimeout`); chỉ giả đúng biên
#       KẾT NỐI (ổ cắm trong bộ nhớ). Lời gọi nào thư viện thật bác thì vào `sai`; harness không tự viết lại luật của thư viện (F01-u).
#       Oracle URL/phương thức đọc từ BYTE TRÊN DÂY, độc lập với mã sản phẩm.
# Hai kiểu lời gọi, cùng một người quan sát: "lenh" (mã chạy như `__main__`, mọi ca) và "nap" (chỉ nạp module, một lần trong g1).
# MỘT hàm hậu điều `_hau_dieu_chung` cho MỌI lời gọi (rc 0/1/2). Oracle nền -> tên tài sản chép từ bảng spec r2 Thay đổi 1, ĐỘC LẬP
# với `TAI_SAN_AGY` (F01-g). So TOÀN transcript theo byte (F01-e/f). Ma trận lỗi chạy cho CẢ latest lẫn `--ban` (F01-s).
from concurrent.futures import ThreadPoolExecutor  # noqa: E402 — 72 tiến trình con của g2 chạy song song, mỗi cái vẫn một vòng đời riêng
ORACLE_TAI_SAN = {"linux_amd64": "agy_cli_linux_x64.tar.gz", "linux_arm64": "agy_cli_linux_arm64.tar.gz",
                  "linux_amd64_musl": "agy_cli_linux_x64_musl.tar.gz", "linux_arm64_musl": "agy_cli_linux_arm64_musl.tar.gz",
                  "darwin_amd64": "agy_cli_mac_x64.tar.gz", "darwin_arm64": "agy_cli_mac_arm64.tar.gz"}
KHOA_6 = tuple(ORACLE_TAI_SAN)
_API = "https://api.github.com/repos/google-antigravity/antigravity-cli/releases/"
HONG_TAI_SAN = ("lech", "thieu", "hai_tep", "ten_sai", "khong_thuong")   # F01-k/l/m/o/p, đặt ở TỪNG nền
LOI_CHUNG = ("release", "json", "tai")   # mạng hỏng khi đọc release · release không phải JSON · mạng hỏng ở lượt tải tài sản THỨ HAI
CHE_DO = (("ghim-agy",), ("ghim-agy", "--ban", "2.3.4"))   # F01-s: MỌI hàng âm chạy ở cả hai chế độ
ARGV_SAI = (("--ban", "../x"), ("--ban",), ("--ban", "2.3"), ("--ban", "v2.3.4"), ("--ban", "2.3.4", "thua"), ("thua",))
# Danh sách CHO PHÉP sự kiện audit: không cái nào tự nó ghi đĩa/sinh tiến trình/mở ổ cắm. Tên nào ngoài đây ⇒ ĐỎ (fail-closed).
SU_KIEN_LANH = ("compile", "exec", "import", "marshal.loads", "os.listdir", "os.scandir", "sys._getframe", "sys._getframemodulename",
                "object.__getattr__", "object.__setattr__", "object.__delattr__", "builtins.id", "code.__new__", "function.__new__",
                "sys.excepthook", "sys.unraisablehook", "time.sleep", "urllib.Request", "http.client.send",   # hai cái sau: transport THẬT nói vào ổ cắm GIẢ
                "cpython.PyInterpreterState_Clear", "cpython._PySys_ClearAuditHooks")   # trình thông dịch tự phát khi tắt
# Danh sách CHO PHÉP cờ của `open` đọc: đúng các cờ mà `open(p)`/`os.open(p, O_RDONLY)` của CPython dùng trên Windows và POSIX.
CO_DOC_CHO_PHEP = ("O_RDONLY", "O_BINARY", "O_NOINHERIT", "O_CLOEXEC")
# Nạp TRƯỚC khi hook tồn tại. Danh sách CỐ ĐỊNH, không suy từ nguồn đang thử — bản đột biến không quyết định được cái gì chạy ngoài tầm đo.
LAM_NONG = ("base64", "contextlib", "ctypes", "gzip", "hashlib", "io", "json", "math", "os", "pathlib", "platform", "re", "shutil",
            "signal", "subprocess", "tarfile", "tempfile", "threading", "time", "urllib.request")
MOI_NHU, MOI_BYTE = "moi-nhu.txt", b"moi nhu\n"   # tệp mồi đặt sẵn ở cwd/HOME/TEMP của từng lời gọi: mất hay đổi byte đều bị thấy
CON_GHIM = r'''"""Tiến trình con của harness `ghim-agy` (sinh từ ops/cloud_agent_creds_test.py). argv: <viec.json> <kênh>.
MỘT lời gọi CLI = MỘT tiến trình này. Sau dòng `mo`, tệp này không còn quyết định gì: mã sản phẩm chạy như `__main__` và tiến trình
thoát bằng đúng đường của nó; hook và kênh sống tới khi trình thông dịch gỡ hook."""
import base64, functools, http.client, importlib, io, json, os, socket, ssl, sys, types, urllib.error, urllib.request  # noqa: E401
sys.dont_write_bytecode = True
VIEC = json.loads(open(sys.argv[1], encoding="utf-8").read())
for _ten in VIEC["lam_nong"]:
    importlib.import_module(_ten)
KENH = os.open(sys.argv[2], os.O_WRONLY | os.O_APPEND | os.O_CREAT)
def tao_ghi(viet=os.write, kenh=KENH, ma_hoa=ascii):
    def ghi(loai, noi_dung):   # một dòng = một bản ghi, ra đĩa NGAY; chỉ dùng thứ đã buộc sẵn nên chạy được cả khi module đang bị dọn
        viet(kenh, (loai + "\t" + ma_hoa(noi_dung) + "\n").encode("ascii"))
    return ghi
GHI = tao_ghi()
MIEN = [0]   # > 0: CHÍNH harness đang cố ý làm một việc có phát audit (tạo ổ cắm CHƯA NỐI để hỏi `settimeout` thật)
class TuChoi(BaseException):
    """Không phải `Exception` ⇒ `except Exception` của mã sản phẩm không nuốt được; có nuốt bằng `except BaseException` thì dấu vẫn ở kênh."""
class LoiMangGia(OSError):
    """Lỗi MẠNG do fixture dựng — không phải lỗi đối số, không vào `sai`."""
CO_DOC = 0
for _co in VIEC["co_doc"]:
    CO_DOC |= getattr(os, _co, 0)
def tao_canh(ghi=GHI, lanh=frozenset(VIEC["lanh"]), co_doc=CO_DOC, mien=MIEN, tu_choi=TuChoi,
             ban=[False], che_do_doc=frozenset("rbt"), len=len, type=type, set=set, repr=repr, int=int, str=str):
    def canh(ten, ds):
        if mien[0] or ban[0] or ten in lanh:
            return
        if (ten == "open" and len(ds) >= 3 and type(ds[2]) is int and not ds[2] & ~co_doc
                and (ds[1] is None or (type(ds[1]) is str and "r" in ds[1] and set(ds[1]) <= che_do_doc))):
            return   # đọc: chế độ ⊆ {r,b,t} và KHÔNG cờ nào ngoài danh sách cho phép
        ban[0] = True   # `repr` của đối số không được tái nhập hook
        try:
            mo_ta = ten + "(" + ", ".join([repr(x)[:120] for x in ds]) + ")"
        except Exception as e:
            mo_ta = ten + "(<repr lỗi " + type(e).__name__ + ">)"
        finally:
            ban[0] = False
        ghi("sk", mo_ta)
        raise tu_choi(mo_ta)
    return canh
# ----- transport: thư viện THẬT, ổ cắm GIẢ -----
BAN = VIEC["ban"]
class OngHong:
    """Phản hồi đứt giữa chừng: lỗi nổ khi http.client ĐỌC dòng trạng thái, như một kết nối thật bị ngắt."""
    def __init__(self, loi):
        self.loi = loi
    def readline(self, *a):
        raise self.loi
    read = readinto = readline
    def close(self):
        pass
    flush = close
class OcGia:
    def __init__(self, kn, luoc_do):
        self.kn, self.luoc_do, self.vao = kn, luoc_do, b""
    def sendall(self, du, *a):
        self.vao += memoryview(du).cast("B")
    def makefile(self, *a, **kw):   # http.client đọc phản hồi ⇒ lúc này yêu cầu đã nằm trọn trong `vao`
        dau = self.vao.split(b"\r\n\r\n", 1)[0].decode("iso-8859-1").split("\r\n")
        pt, duong = dau[0].split(" ")[:2]
        tieu_de = dict(d.split(": ", 1) for d in dau[1:] if ": " in d)
        url = self.luoc_do + "://" + tieu_de.get("Host", self.kn.host) + duong
        han = self.kn.timeout
        GHI("nk", json.dumps({"url": url, "pt": pt, "han": None if han is socket._GLOBAL_DEFAULT_TIMEOUT else repr(han), "tieu_de": tieu_de}))
        muc = BAN.get(url)
        if pt != "GET":
            GHI("sai", "phương thức " + pt + " tới " + repr(url) + " — đọc release/tải tài sản là GET")
            return io.BytesIO(b"HTTP/1.1 405 Method Not Allowed\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
        if muc is None:
            GHI("sai", "URL ngoài bảng phục vụ: " + repr(url))
            return io.BytesIO(b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
        if "nem" in muc:
            return OngHong(LoiMangGia(muc["nem"]))
        than = base64.b64decode(muc["than"])
        return io.BytesIO(b"HTTP/1.1 200 OK\r\nContent-Length: " + str(len(than)).encode("ascii") + b"\r\nConnection: close\r\n\r\n" + than)
    def close(self):
        pass
def ket_noi_gia(self):
    """Thay `HTTP(S)Connection.connect`. Thứ duy nhất của biên kết nối thật còn giữ: `sock.settimeout(timeout)` mà
    `socket.create_connection` gọi — hỏi CHÍNH `socket` thật trên một ổ cắm chưa nối (không DNS, không gói tin)."""
    han, https = self.timeout, isinstance(self, http.client.HTTPSConnection)
    if han is not socket._GLOBAL_DEFAULT_TIMEOUT:
        MIEN[0] += 1   # miễn ĐÚNG một sự kiện: `socket.__new__` của ổ cắm thử
        try:
            thu = socket.socket()
        finally:
            MIEN[0] -= 1
        try:
            thu.settimeout(han)
            khong_chan = thu.gettimeout() == 0
        finally:
            thu.close()
        if khong_chan:
            raise BlockingIOError("timeout=0: ổ cắm không chặn, connect() thật chưa xong đã trả lỗi")
    if https and not isinstance(self._context, ssl.SSLContext):
        raise AttributeError(repr(type(self._context).__name__) + " object has no attribute 'wrap_socket'")
    self.sock = OcGia(self, "https" if https else "http")
http.client.HTTPConnection.connect = ket_noi_gia
http.client.HTTPSConnection.connect = ket_noi_gia
def bao_sai(e):
    """Lời gọi bị thư viện THẬT bác (không phải lỗi mạng giả, không phải TuChoi, không phải 404/405 đã ghi ở ổ cắm) ⇒ một bản ghi `sai`."""
    for x in (e, getattr(e, "reason", None)):
        if isinstance(x, (LoiMangGia, TuChoi, urllib.error.HTTPError, SystemExit)) or getattr(x, "_cac_da_bao", False):
            break
    else:
        GHI("sai", "thư viện thật bác lời gọi: " + type(e).__name__ + ": " + str(e)[:200])
    try:
        e._cac_da_bao = True
    except Exception:
        pass
def quan_sat(that):   # chỉ NHÌN: gọi nguyên hàm thật, ghi lại ngoại lệ nó ném, rồi ném tiếp
    @functools.wraps(that)
    def boc(*a, **kw):
        try:
            return that(*a, **kw)
        except BaseException as e:
            bao_sai(e)
            raise
    return boc
urllib.request.urlopen = quan_sat(urllib.request.urlopen)
urllib.request.OpenerDirector.open = quan_sat(urllib.request.OpenerDirector.open)
http.client.HTTPConnection.request = quan_sat(http.client.HTTPConnection.request)
# ----- mã sản phẩm: kiểu "lenh" = chạy như `__main__` (đúng lệnh CLI); kiểu "nap" = chỉ NẠP module (đường mà mọi nơi import nó đi) -----
MA = VIEC["ma"]
TEN = "__main__" if VIEC["kieu"] == "lenh" else "cloud_agent_creds_duoi_test"
MODULE = types.ModuleType(TEN)
MODULE.__file__ = MA
sys.modules[TEN] = MODULE
sys.argv = [MA] + list(VIEC["argv"])
MA_DA_DICH = compile(open(MA, encoding="utf-8").read(), MA, "exec")   # lỗi cú pháp của bản đột biến nổ Ở ĐÂY, trước `mo` ⇒ lỗi harness
sys.addaudithook(tao_canh())
GHI("mo", "")
try:
    exec(MA_DA_DICH, MODULE.__dict__)
except SystemExit:
    GHI("roi", "SystemExit")
    raise
except BaseException as e:
    GHI("roi", type(e).__name__ + ": " + str(e)[:300])
    raise
GHI("roi", "het-tep")
'''
_TAR_NHO = {}
def _tar_nen(ban, k, hong=None):
    if (ban, k, hong) not in _TAR_NHO:
        _TAR_NHO[ban, k, hong] = (_tar([("antigravity", NOI_DUNG), ("khac", b"y")]) if hong == "hai_tep" else _tar([("khac", NOI_DUNG)]) if hong == "ten_sai"
                                  else _tar([("antigravity", None)]) if hong == "khong_thuong"
                                  else _tar([("antigravity", NOI_DUNG + f"{ban}/{k}".encode())]))   # sáu nền × hai phiên bản: byte KHÁC nhau
    return _TAR_NHO[ban, k, hong]
def _goi(ten, argv=("ghim-agy",), hong=None, loi=None, kieu="lenh"):
    """Mô tả MỘT lời gọi CLI: tên hàng, argv, {nền: kiểu hỏng}, lỗi chung. `pb` = phiên bản mà lời gọi phải ra. `kieu="nap"`: chỉ nạp module."""
    argv = tuple(argv)
    return SimpleNamespace(ten=ten, argv=argv, hong=dict(hong or {}), loi=loi, kieu=kieu, pb=argv[2] if len(argv) == 3 else "9.8.7",
                           duong=_API + (f"tags/{argv[2]}" if len(argv) == 3 else "latest"))
def _ban_phuc_vu(hong, loi):
    """Bảng URL -> phản hồi cho MỘT lời gọi (luôn phục vụ CẢ hai phiên bản) và kỳ vọng {phiên bản: {nền: (url, sha512)}}."""
    ban, mong = {}, {}
    for pb, duong in (("9.8.7", ("latest", "tags/9.8.7")), ("2.3.4", ("tags/2.3.4",))):
        ts = {k: (f"https://gia.invalid/{pb}/{ten}", _tar_nen(pb, k, hong.get(k))) for k, ten in ORACLE_TAI_SAN.items()}
        rel = json.dumps({"tag_name": pb, "assets": [
            {"name": ORACLE_TAI_SAN[k], "browser_download_url": u, "digest": "sha256:" + ("0" * 64 if hong.get(k) == "lech" else hashlib.sha256(b).hexdigest())}
            for k, (u, b) in ts.items() if hong.get(k) != "thieu"]}).encode("utf-8")
        for d in duong:
            ban[_API + d] = {"nem": "giả lập mạng hỏng"} if loi == "release" else {"than": b"{khong phai json" if loi == "json" else rel}
        for i, (u, b) in enumerate(ts.values()):
            ban[u] = {"nem": "giả lập tải hỏng"} if loi == "tai" and i == 1 else {"than": b}
        mong[pb] = {k: (u, hashlib.sha512(b).hexdigest()) for k, (u, b) in ts.items()}
    return {u: ({"than": base64.b64encode(m["than"]).decode("ascii")} if "than" in m else m) for u, m in ban.items()}, mong
def _chup(goc):
    """Trạng thái ĐẦY ĐỦ của một cây: mỗi mục -> (loại, quyền[, cỡ, mtime_ns, sha256] | đích liên kết)."""
    kq = {}
    for d, thu_muc, tep in os.walk(goc):
        for x in thu_muc + tep:
            p = Path(d, x)
            st = p.lstat()
            kq[p.relative_to(goc).as_posix()] = (("l", os.readlink(p)) if p.is_symlink() else ("d", st.st_mode) if p.is_dir()
                                                 else ("f", st.st_mode, st.st_size, st.st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest()))
    return kq
def _so_trang_thai(truoc, sau):
    return sorted([f"thêm {k}" for k in sau.keys() - truoc.keys()] + [f"mất {k}" for k in truoc.keys() - sau.keys()]
                  + [f"đổi {k}" for k in truoc.keys() & sau.keys() if truoc[k] != sau[k]])
def _van(b):   # văn bản như mã in ra: giải mã, đổi xuống dòng của nền về "\n" (so byte nguyên vẹn nằm ở `ra_tho`)
    return b.decode("utf-8", "backslashreplace").replace(os.linesep, "\n")
def _mot_loi_goi(t, i, g, ban, mong, ma):
    """MỘT lời gọi = MỘT tiến trình con. Chỉ sau khi con CHẾT mới đọc kênh (tới hết tệp) và chụp lại trạng thái."""
    d = t / str(i)
    for x in ("cwd", "home", "tmp"):
        (d / "dung" / x).mkdir(parents=True)
        (d / "dung" / x / MOI_NHU).write_bytes(MOI_BYTE)
    (d / "viec.json").write_text(json.dumps({"ma": str(ma), "argv": g.argv, "kieu": g.kieu, "ban": ban, "lanh": SU_KIEN_LANH, "co_doc": CO_DOC_CHO_PHEP,
                                             "lam_nong": LAM_NONG}), encoding="utf-8")
    nha, tam, truoc = str(d / "dung" / "home"), str(d / "dung" / "tmp"), _chup(d / "dung")
    moi_truong = {k: v for k, v in os.environ.items() if not k.lower().endswith("_proxy")}   # proxy của máy không được chen vào transport
    r = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", str(t / "con.py"), str(d / "viec.json"), str(d / "kenh")], cwd=str(d / "dung" / "cwd"),
                       env=dict(moi_truong, HOME=nha, USERPROFILE=nha, TEMP=tam, TMP=tam, TMPDIR=tam, no_proxy="*"),
                       stdin=subprocess.DEVNULL, capture_output=True, timeout=120)
    kenh = {"mo": [], "roi": [], "sk": [], "sai": [], "nk": []}
    for dong in ((d / "kenh").read_text(encoding="ascii").splitlines() if (d / "kenh").is_file() else ()):
        loai, _, nd = dong.partition("\t")
        kenh[loai].append(ast.literal_eval(nd))
    if not kenh["mo"]:   # chưa tới được mã sản phẩm: hỏng ở phần dựng (kể cả lỗi cú pháp của bản đột biến) ⇒ lỗi harness, thoát 4
        raise RuntimeError(f"{g.ten}: tiến trình con hỏng trước khi mở tầm đo (rc={r.returncode}): {_van(r.stderr)[-400:]}")
    return SimpleNamespace(ten=g.ten, goi=g, mong=mong, rc=r.returncode, ra_tho=r.stdout, ra=_van(r.stdout), loi=_van(r.stderr), sk=kenh["sk"], sai=kenh["sai"],
                           nk=[json.loads(x) for x in kenh["nk"]], roi=(kenh["roi"] or [None])[-1], doi=_so_trang_thai(truoc, _chup(d / "dung")))
def _chay_ghim(ds, ma=None):
    """Chạy từng lời gọi của `ds` trong tiến trình con RIÊNG (song song, kết quả giữ thứ tự)."""
    viec = [(i, g, *_ban_phuc_vu(g.hong, g.loi)) for i, g in enumerate(ds)]
    with tempfile.TemporaryDirectory(prefix="cac_ghim_") as t:
        t = Path(t).resolve()
        (t / "con.py").write_text(CON_GHIM, encoding="utf-8", newline="\n")
        with ThreadPoolExecutor(min(8, os.cpu_count() or 2)) as nhom:
            return list(nhom.map(lambda v: _mot_loi_goi(t, v[0], v[1], v[2], v[3], ma or MA), viec))
def _hau_dieu_chung(kq, stderr_tu_do=False):
    """Hậu điều của MỌI lời gọi `ghim-agy`, bất kể rc: không tác động tệp/tiến trình/mạng trong CẢ vòng đời (F01-n/r/t/v), transport đúng (F01-q/u)."""
    bang(not kq.sk, f"{kq.ten}: sự kiện ngoài danh sách cho phép trong vòng đời tiến trình — ghi đĩa/tiến trình/mạng ({len(kq.sk)} lần): {kq.sk[:5]}")
    bang(not kq.doi, f"{kq.ten}: trạng thái cwd/HOME/TEMP đổi sau khi tiến trình chết: {kq.doi}")
    bang(not kq.sai, f"{kq.ten}: transport — thư viện thật bác lời gọi / sai phương thức / URL ngoài bảng: {kq.sai}")
    if kq.roi not in ("SystemExit", "het-tep"):   # không dấu ghi, không sai transport mà rời bằng ngoại lệ/`os._exit` ⇒ lỗi VÔ CAN (thoát 4)
        raise RuntimeError(f"{kq.ten}: mã rời tiến trình không qua SystemExit: {kq.roi!r} (rc={kq.rc}) {kq.loi[-300:]}")
    bang(stderr_tu_do or kq.loi == "", f"{kq.ten}: stderr không rỗng: {kq.loi!r}")
def _transcript_mong(ban, mong):
    d = mong[ban]
    return ([f'AGY_VER = "{ban}"', "NEN = {"] + [f'    "{k}": ("{u}", "{h}"),' for k, (u, h) in d.items()] + ["}", ""]
            + [f"| `{k}` | `{u}` | `{h}` |" for k, (u, h) in d.items()])
def _bang_thanh_cong(kq):
    _hau_dieu_chung(kq)
    bang(kq.rc == 0, f"{kq.ten}: rc={kq.rc}, mong 0 — stdout={kq.ra!r}")
    bang(kq.ra_tho == "".join(d + os.linesep for d in _transcript_mong(kq.goi.pb, kq.mong)).encode("utf-8"), f"{kq.ten}: transcript lệch hợp đồng: {kq.ra!r}")
    bang([x["url"] for x in kq.nk] == [kq.goi.duong] + [kq.mong[kq.goi.pb][k][0] for k in KHOA_6], f"{kq.ten}: nhật ký mạng {[x['url'] for x in kq.nk]}")
def _bang_tu_choi(kq):
    _hau_dieu_chung(kq)
    dong, url, d = kq.ra.splitlines(), [x["url"] for x in kq.nk], kq.mong[kq.goi.pb]
    bang(kq.rc == 1 and len(dong) == 1 and dong[0].startswith("ghim-agy: ✗") and kq.ra.endswith("\n"), f"{kq.ten}: rc={kq.rc} stdout={kq.ra!r}")
    bang(url[:1] == [kq.goi.duong] and set(url[1:]) <= {u for u, _ in d.values()}, f"{kq.ten}: nhật ký mạng {url}")
    for k, h in kq.goi.hong.items():   # bằng chứng nguyên nhân: không thể biết digest/tarball hỏng nếu chưa tải chính tài sản ấy
        bang(h == "thieu" or d[k][0] in url, f"{kq.ten}: từ chối mà chưa tải tài sản {k} — không phải vì kiểu hỏng đang thử ({url})")
    bang(kq.goi.loi != "tai" or d[KHOA_6[1]][0] in url, f"{kq.ten}: chưa tới lượt tải bị làm hỏng ({url})")
def _bang_argv_sai(kq):   # F01-r: rc 2 KHÔNG miễn hậu điều chung; usage ở stderr được phép, stdout (kênh dữ liệu) phải rỗng, không tải gì
    _hau_dieu_chung(kq, stderr_tu_do=True)
    bang(kq.rc == 2 and kq.nk == [] and kq.ra_tho == b"", f"{kq.ten}: rc={kq.rc} tải={[x['url'] for x in kq.nk]} stdout={kq.ra!r}")
def g1_ghim_in_dung_sau_cap():   # release latest: đủ sáu tải đúng nền đúng thứ tự, transcript ĐÚNG từng byte, không ghi
    lenh, nap = _chay_ghim([_goi("latest"), _goi("nạp module (không chạy lệnh)", (), kieu="nap")])
    _bang_thanh_cong(lenh)
    # Lệnh thật `sys.exit` ngay trong guard `__main__` nên không bao giờ chạy tới mã mức module đứng SAU guard; đường NẠP thì có.
    _hau_dieu_chung(nap)
    bang((nap.rc, nap.ra_tho, nap.nk, nap.roi) == (0, b"", [], "het-tep"), f"nạp module mà có đầu ra/tải/thoát: rc={nap.rc} stdout={nap.ra!r} nk={nap.nk} roi={nap.roi!r}")
def g3_ghim_ban_chi_dinh():   # F01-h/i: `--ban` hợp lệ đi xuống `tags/<ban>` và ra đúng phiên bản ấy
    _bang_thanh_cong(_chay_ghim([_goi("--ban 2.3.4", CHE_DO[1])])[0])
def g2_ghim_tu_choi_khi_sai():   # (năm kiểu hỏng × sáu nền + mạng/JSON/tải) × (latest, --ban) ⇒ rc 1, ĐÚNG một dòng; argv sai ⇒ rc 2, không tải
    ds = []
    for argv in CHE_DO:
        nhan = " ".join(argv[1:]) or "latest"
        ds += [_goi(f"{nhan}: {h}@{k}", argv, hong={k: h}) for h in HONG_TAI_SAN for k in KHOA_6]
        ds += [_goi(f"{nhan}: {loi} hỏng", argv, loi=loi) for loi in LOI_CHUNG]
    n_loi = len(ds)
    ds += [_goi("argv sai " + " ".join(map(repr, a)), ("ghim-agy",) + a) for a in ARGV_SAI]
    kq = _chay_ghim(ds)
    bang(n_loi == len(CHE_DO) * (len(HONG_TAI_SAN) * len(KHOA_6) + len(LOI_CHUNG)) == 66, f"ma trận lỗi phải đủ 66 hàng, có {n_loi}")
    for x in kq[:n_loi]:
        _bang_tu_choi(x)
    for x in kq[n_loi:]:
        _bang_argv_sai(x)
# Tự kiểm của CHÍNH harness, HAI CHIỀU: một CLI GIẢ làm đúng từng việc bị cấm ⇒ hậu điều chung PHẢI đỏ; việc hợp lệ (kể cả những thứ
# harness lượt trước bác oan) ⇒ PHẢI xanh. Chạy bằng đúng đường của g1/g2/g3: một tiến trình con mỗi ca, sống tới khi thoát thật.
MA_THU = r'''import atexit, os, socket, subprocess, sys, tempfile, threading, urllib.request  # noqa: E401
from pathlib import Path
U, MOI = "https://gia.invalid/9.8.7/agy_cli_linux_x64.tar.gz", "moi-nhu.txt"
YC = urllib.request.Request
class GhiKhiHuy:   # lúc module bị dọn `builtins.open` đã bị gỡ (CPython thật cũng vậy) ⇒ finalizer muốn ghi phải giữ sẵn os.open
    def __del__(self, mo=os.open, dong=os.close, co=os.O_WRONLY | os.O_CREAT):
        dong(mo("g.txt", co))
def main(argv):
    ca, tam, mo = argv[0], os.environ["TEMP"], urllib.request.urlopen
    if ca == "lanh":   # đọc, liệt kê, mở CHỈ ĐỌC, callback lúc tắt KHÔNG ghi, sáu dạng lời gọi transport mà thư viện thật nhận
        open(__file__, encoding="utf-8").read(), os.listdir("."), Path(MOI).read_bytes(), os.close(os.open(MOI, os.O_RDONLY))
        threading._register_atexit(lambda: None), atexit.register(lambda: None)
        __import__("time").sleep(0), threading.Event().wait(0)   # F01-x: chờ thuần không phải tác động tệp
        with mo(U, timeout=30) as r:
            r.read()
        mo(YC(U, headers={"User-Agent": "x"}), None, 2.5).read(), mo(U).read(), mo(U, timeout=True).read(), mo(U, timeout=None).read()
        urllib.request.build_opener().open(U, timeout=1).read()
        mo(YC(U, data=[b"A"], method="GET", headers={"Content-Length": "1"}), timeout=30).read()   # F01-w: body iterable bytes hợp lệ
        mo(YC(U, data=[b"A"], method="GET"), timeout=30).read()   # F01-w: chunked hợp lệ
        print("ok")
    elif ca == "path_tuyet_doi":
        Path(tam, "a.txt").write_text("x", encoding="utf-8")
    elif ca == "os_open":
        os.close(os.open(os.path.join(tam, "b.bin"), os.O_WRONLY | os.O_CREAT | os.O_TRUNC))
    elif ca == "temporaryfile":
        tempfile.TemporaryFile().close()
    elif ca == "tao_roi_xoa":
        Path("c.txt").write_text("x", encoding="utf-8"), Path("c.txt").unlink()
    elif ca == "nuot_loi":
        try:
            open("d.txt", "w").close()
        except BaseException:
            pass
    elif ca == "them_vao":
        open(MOI, "a").close()
    elif ca == "doc_ghi":
        open(MOI, "r+").close()
    elif ca == "mkdir":
        os.mkdir("e")
    elif ca == "doi_ten":
        os.replace(MOI, "khac.txt")
    elif ca == "xoa":
        os.remove(MOI)
    elif ca == "xoa_khi_dong":   # Windows: O_RDONLY|O_TEMPORARY xoá tệp lúc đóng; POSIX không có cờ ấy ⇒ O_RDONLY|O_TRUNC cắt tệp về 0
        os.close(os.open(MOI, os.O_RDONLY | getattr(os, "O_TEMPORARY", os.O_TRUNC)))
    elif ca == "fdopen":
        os.fdopen(1, "w", closefd=False)
    elif ca == "tien_trinh":
        subprocess.run([sys.executable, "-c", "pass"])
    elif ca == "o_cam_tho":
        socket.socket().close()
    elif ca == "hen_luc_thoat":   # main trả 0 sạch sẽ; việc ghi chỉ xảy ra khi tiến trình thoát ...
        atexit.register(lambda: open("f.txt", "w").close())
    elif ca == "tat_luong_ghi":   # ... hoặc trong `threading._shutdown`, TRƯỚC cả atexit (F01-t) ...
        threading._register_atexit(lambda: open("t.txt", "w").close())
    elif ca == "ghi_khi_huy":   # ... hoặc khi module bị dọn
        globals()["_giu"] = GhiKhiHuy()
    elif ca == "luong":
        threading.Thread(target=lambda: open("h.txt", "w").close()).start()
    else:   # lời gọi transport SAI: nuốt lỗi như `ghim_agy` vẫn làm ⇒ chỉ nhật ký `sai` mới tố được
        try:
            {"timeout_chuoi": lambda: mo(U, timeout="30"), "timeout_am": lambda: mo(U, timeout=-1), "timeout_khong": lambda: mo(U, timeout=0),
             "req_sai_kieu": lambda: mo(U.encode()), "doi_so_la": lambda: mo(U, thoi_han=3), "post": lambda: mo(U, b"x"),
             "url_la": lambda: mo(U + "?x=1"), "tieu_de_none": lambda: mo(YC(U, headers={"User-Agent": None})),
             "than_chuoi_get": lambda: mo(YC(U, data="than", method="GET")), "ngu_canh_chu": lambda: mo(U, context="chu")}[ca]()
        except Exception:
            pass
    return 0
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''
# (ca, mảnh phải có trong sự kiện ĐẦU TIÊN). Ca nào cũng phải để nguyên ba tệp mồi: người quan sát TỪ CHỐI chứ không chỉ ghi nhận.
THU_GHI = (("path_tuyet_doi", "a.txt"), ("os_open", "b.bin"), ("temporaryfile", "open("), ("tao_roi_xoa", "c.txt"), ("nuot_loi", "d.txt"),
           ("them_vao", MOI_NHU), ("doc_ghi", MOI_NHU), ("mkdir", "os.mkdir"), ("doi_ten", "os.rename"), ("xoa", "os.remove"), ("xoa_khi_dong", MOI_NHU),
           ("fdopen", "open(1"), ("tien_trinh", "subprocess.Popen"), ("o_cam_tho", "socket."), ("hen_luc_thoat", "f.txt"), ("tat_luong_ghi", "t.txt"),
           ("ghi_khi_huy", "g.txt"), ("luong", "_thread.start"))
THU_SAI = ("timeout_chuoi", "timeout_am", "timeout_khong", "req_sai_kieu", "doi_so_la", "post", "url_la", "tieu_de_none", "than_chuoi_get", "ngu_canh_chu")
def _bi_chot(kq):
    try:
        _hau_dieu_chung(kq)
    except TinHieuChotCa:
        return True
    return False
def g4_quan_sat_va_transport_co_rang():   # F01-n/q/t/u/v: đối chứng dương VÀ đối chứng âm của người quan sát, transport và nhân chứng trạng thái
    with tempfile.TemporaryDirectory(prefix="cac_thu_") as t:
        (ma := Path(t) / "ma_thu.py").write_text(MA_THU, encoding="utf-8", newline="\n")
        kq = {x.ten: x for x in _chay_ghim([_goi(ten, (ten,)) for ten in ("lanh",) + tuple(c for c, _ in THU_GHI) + THU_SAI], ma=ma)}
        # nhân chứng trạng thái, đo thẳng: mất · byte đổi (cùng cỡ) · thêm đều phải hiện; không đổi gì thì phải im
        (cay := Path(t) / "cay").mkdir()
        for ten in ("mat.txt", "doi.txt", "yen.txt"):
            (cay / ten).write_bytes(b"1234")
        truoc = _chup(cay)
        bang(_so_trang_thai(truoc, _chup(cay)) == [], "nhân chứng trạng thái tự báo động khi không ai đụng")
        (cay / "mat.txt").unlink(), (cay / "doi.txt").write_bytes(b"4321"), (cay / "them.txt").write_bytes(b"")
        bang(_so_trang_thai(truoc, _chup(cay)) == ["mất mat.txt", "thêm them.txt", "đổi doi.txt"], f"nhân chứng trạng thái mù: {_so_trang_thai(truoc, _chup(cay))}")
        # danh sách CHO PHÉP cờ đọc, chứng minh trên CHÍNH runtime này: cờ được phép không đổi gì; cờ ngoài danh sách có tác động thật
        (thu := cay / "co.txt").write_bytes(b"1234")
        truoc = _chup(cay)
        for co in CO_DOC_CHO_PHEP:
            os.close(os.open(thu, os.O_RDONLY | getattr(os, co, 0)))
            bang(_so_trang_thai(truoc, _chup(cay)) == [], f"cờ {co} trong danh sách cho phép mà làm đổi tệp")
        ngoai = "O_TEMPORARY" if hasattr(os, "O_TEMPORARY") else "O_TRUNC"
        os.close(os.open(thu, os.O_RDONLY | getattr(os, ngoai)))
        bang(ngoai not in CO_DOC_CHO_PHEP and _so_trang_thai(truoc, _chup(cay)) == [("mất" if ngoai == "O_TEMPORARY" else "đổi") + " co.txt"],
             f"đối chứng {ngoai}: {_so_trang_thai(truoc, _chup(cay))}")
    x = kq["lanh"]
    bang(not _bi_chot(x) and (x.rc, x.ra, x.loi, x.roi) == (0, "ok\n", "", "SystemExit"), f"việc hợp lệ bị chốt oan: sk={x.sk} sai={x.sai} doi={x.doi} rc={x.rc} {x.loi!r}")
    bang([(n["url"], n["pt"], n["han"]) for n in x.nk] == [("https://gia.invalid/9.8.7/agy_cli_linux_x64.tar.gz", "GET", h) for h in ("30", "2.5", None, "True", "None", "1", "30", "30")],
         f"nhật ký transport (đọc từ byte trên dây) lệch: {x.nk}")
    bang(x.nk[1]["tieu_de"].get("User-Agent") == "x", f"header không tới dây: {x.nk[1]}")
    for ten, dau in THU_GHI:
        x = kq[ten]
        bang(x.sk and dau in x.sk[0] and not x.doi and not x.sai and _bi_chot(x), f"{ten}: người quan sát mù, không từ chối, hoặc hậu điều không đỏ — sk={x.sk} doi={x.doi}")
    for ten in ("nuot_loi", "hen_luc_thoat", "tat_luong_ghi", "ghi_khi_huy"):   # main về 0 và tiến trình thoát mã 0: CHỈ kênh sự kiện tố được
        bang((kq[ten].rc, kq[ten].roi) == (0, "SystemExit"), f"{ten}: phải là ca mà mã che được lỗi, lại thấy rc={kq[ten].rc} roi={kq[ten].roi!r}")
    for ten in THU_SAI:
        x = kq[ten]
        bang(x.sai and not x.sk and not x.doi and (x.rc, x.roi) == (0, "SystemExit") and _bi_chot(x), f"{ten}: lời gọi sai mà không vào `sai` — sai={x.sai} sk={x.sk} rc={x.rc}")
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
# ---------- PD (#1334, spec CODEX-HOME-NGOAI-KHO r2 M5): chốt "không ghi credential vào trong kho git" — dữ liệu GIẢ ----------
SEN_PD, LR_PD = "SENTINEL-token-pd-GIA-1334", "2099-01-01T00:00:00Z"
def _tam_pd(t):   # tiền đề của vế dương, đo ĐỘC LẬP với mã đang thử: thư mục tạm không được nằm dưới một kho
    d = os.path.realpath(t)
    while os.path.dirname(d) != d:
        if os.path.lexists(os.path.join(d, ".git")):
            raise RuntimeError(f"thư mục tạm nằm dưới {d}/.git — dọn rồi đo lại")
        d = os.path.dirname(d)
    return Path(os.path.realpath(t))
def _kho_pd(t):
    r = subprocess.run(["git", "init", "-q", str(kho := _tam_pd(t) / "kho")], capture_output=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"git init rc={r.returncode}")
    return kho
def _sach_pd(kho):   # không tệp nào lọt vào cây kho, kể cả tệp tạm
    r = subprocess.run(["git", "-C", str(kho), "status", "--porcelain", "--untracked-files=all"], capture_output=True, text=True, timeout=60)
    bang(r.returncode == 0 and r.stdout == "" and not list(kho.rglob("*auth.json*")), f"cây kho có tệp mới: rc={r.returncode} {r.stdout!r}")
def _lien_ket(lk, dich, la_thu_muc=False):
    try:
        os.symlink(dich, lk, target_is_directory=la_thu_muc)
    except (OSError, NotImplementedError) as e:
        if LA_WINDOWS:
            raise BoQua(f"Windows không tạo được symlink ({type(e).__name__})")
        raise
def chay_bs(codex_home, mod=None):   # đồ giả ở cùng ranh giới với mục 0 của spec: tải + giải mã; không bundle, không khoá thật
    mod, goi = mod or tl_gws, json.dumps({"schema": 1, "rev": 9, "codex_auth": {"tokens": {"refresh_token": SEN_PD}, "last_refresh": LR_PD}}).encode("utf-8")
    with mock.patch.dict(os.environ, {"CODEX_HOME": str(codex_home)}), mock.patch.object(mod, "_public_curl_bytes", lambda *a, **k: b"gia"), \
         mock.patch.object(gws_cred_store, "decrypt", lambda b, k: goi), mock.patch.object(mod, "_imp", importlib.import_module, create=True):
        return mod._bootstrap_agent_creds("x" * 40)
def _chan_pd(kq, kho, auth):
    bang(not auth.exists(), f"auth.json bị ghi vào trong kho: {kq[0]}")
    bang(kq[0] == "KHÔNG ĐO ĐƯỢC" and "nằm trong kho git" in kq[1] and "không ghi auth.json" in kq[1] and SEN_PD not in kq[1], f"kết luận {kq}")
    _sach_pd(kho)
def _tl_gws_base():
    (m := importlib.util.module_from_spec(importlib.util.spec_from_loader("tl_gws_base_pd", loader=None))).__dict__["__file__"] = str(TLGWS)
    exec(compile(_git_base("scripts/tl_gws.py", BASE_PD), "tl_gws@base", "exec"), m.__dict__)
    return m
def pd1_codex_home_trong_kho_khong_ghi():   # M5(a) + vế âm N1 trên base
    with tempfile.TemporaryDirectory(prefix="cac_pd_") as t:
        (ch := (kho := _kho_pd(t)) / "codexhome").mkdir()
        _chan_pd(chay_bs(ch), kho, ch / "auth.json")
        bang(os.listdir(ch) == [], f"thư mục đích có tệp: {os.listdir(ch)}")
        cu = chay_bs(ch, _tl_gws_base())
        bang(cu[0] == "ĐÃ NẠP" and (ch / "auth.json").exists(), f"vế âm: base {BASE_PD[:7]} không ghi vào kho ({cu[0]})")
def pd2_codex_home_ngoai_kho_van_nap():   # M5(b): vế dương, hành vi cũ
    with tempfile.TemporaryDirectory(prefix="cac_pd_") as t:
        kq, f = chay_bs(ch := _tam_pd(t) / "ngoai" / "codexhome"), ch / "auth.json"
        bang(kq[0] == "ĐÃ NẠP" and f.exists() and SEN_PD not in kq[1], f"ngoài kho mà không nạp: {kq}")
        bang(json.loads(f.read_text(encoding="utf-8"))["tokens"] == {"refresh_token": SEN_PD} and (LA_WINDOWS or f.stat().st_mode & 0o777 == 0o600), "auth.json sai nội dung/quyền")
def pd3_git_la_tep_van_chan():   # M5(c): worktree/submodule
    with tempfile.TemporaryDirectory(prefix="cac_pd_") as t:
        (ch := (wt := _tam_pd(t) / "wt") / "con" / "codexhome").mkdir(parents=True), (wt / ".git").write_text("gitdir: /khong/co\n", encoding="utf-8")
        kq = chay_bs(ch)
        bang(not (ch / "auth.json").exists() and kq[0] == "KHÔNG ĐO ĐƯỢC" and str(wt) in kq[1] and os.listdir(ch) == [], f".git là TỆP mà không chặn: {kq}")
def pd4_git_la_symlink_van_chan():   # M5(d): symlink TREO (stat hụt, lstat thấy) và symlink tới thư mục thật
    for dich in ("khong-ton-tai", "that"):
        with tempfile.TemporaryDirectory(prefix="cac_pd_") as t:
            (ch := (goc := _tam_pd(t) / "g") / "codexhome").mkdir(parents=True), (goc / "that").mkdir()
            _lien_ket(goc / ".git", dich, dich == "that")
            kq = chay_bs(ch)
            bang(not (ch / "auth.json").exists() and kq[0] == "KHÔNG ĐO ĐƯỢC" and os.listdir(ch) == [], f".git là symlink → {dich} mà không chặn: {kq}")
def pd5_dich_chua_ton_tai_khong_tao_thu_muc():   # M5(e)
    with tempfile.TemporaryDirectory(prefix="cac_pd_") as t:
        kq = chay_bs(ch := (kho := _kho_pd(t)) / "a" / "b" / "codexhome")
        bang(not (kho / "a").exists(), f"đã tạo thư mục trong kho trước khi kiểm: {kq[0]}")
        _chan_pd(kq, kho, ch / "auth.json")
def pd6_ghi_dau_trong_kho_khong_ghi():   # M5(f) + vế dương của `_ghi_dau`
    m = nap_mod()
    with tempfile.TemporaryDirectory(prefix="cac_pd_") as t:
        (trong := (kho := _kho_pd(t)) / "codexhome").mkdir(), (ngoai := _tam_pd(t) / "ngoai").mkdir()
        for ch, co in ((trong, False), (kho / "chua" / "co", False), (ngoai, True)):
            with mock.patch.dict(os.environ, {"CODEX_HOME": str(ch)}):
                m._ghi_dau(LR_PD, None)
            bang((ch / TEN_DAU).exists() == co, f"tệp dấu ở {ch.name}: mong {co}")
        (ngoai / TEN_DAU).unlink()
        with mock.patch.dict(os.environ, {"CODEX_HOME": str(ngoai)}), mock.patch.dict(sys.modules, {"tl_gws": None}):
            m._ghi_dau(LR_PD, None)   # không nạp được chốt ⇒ không đo được đích ⇒ không ghi
        bang(not (ngoai / TEN_DAU).exists(), "không nạp được tl_gws mà vẫn ghi tệp dấu")
        bang(os.listdir(trong) == [] and not (kho / "chua").exists(), "`_ghi_dau` để lại tệp/thư mục trong kho")
        _sach_pd(kho)
def pd7_symlink_ngoai_kho_tro_vao_kho():   # M5(g) + vế âm N5b trên base
    with tempfile.TemporaryDirectory(prefix="cac_pd_") as t:
        (ch := (kho := _kho_pd(t)) / "codexhome").mkdir()
        _lien_ket(lk := _tam_pd(t) / "lk", ch, True)
        _chan_pd(chay_bs(lk), kho, ch / "auth.json")
        cu = chay_bs(lk, _tl_gws_base())
        bang(cu[0] == "ĐÃ NẠP" and (ch / "auth.json").exists(), f"vế âm: base {BASE_PD[:7]} không ghi qua symlink ({cu[0]})")
    with tempfile.TemporaryDirectory(prefix="cac_pd_") as t:   # chiều ngược: symlink TRONG kho trỏ ra ngoài ⇒ chuỗi từ vựng vẫn chặn
        (ngoai := _tam_pd(t) / "ngoai").mkdir(), _lien_ket(lk := _kho_pd(t) / "lk", ngoai, True)
        kq = chay_bs(lk)
        bang(os.listdir(ngoai) == [] and kq[0] == "KHÔNG ĐO ĐƯỢC", f"đường khai nằm trong kho (symlink ra ngoài) mà không chặn: {kq[0]}")
def pd8_symlink_roi_hai_cham_vao_kho():   # review PR #1367: `..` đứng SAU symlink — kernel đi lên từ ĐÍCH của symlink, `abspath` thì không
    for duoi in ("lk/../codexhome", "lk2/../codexhome", "lk/../chua/co", "lk/.."):   # giữa · symlink lồng · đích chưa tồn tại · `..` ở cuối
        with tempfile.TemporaryDirectory(prefix="cac_pd_") as t:
            (kho := _kho_pd(t)).joinpath("con").mkdir(), (kho / "codexhome").mkdir(), (ngoai := _tam_pd(t) / "ngoai" / "codexhome").mkdir(parents=True)
            _lien_ket(ngoai.parent / "lk", kho / "con", True), _lien_ket(ngoai.parent / "lk2", ngoai.parent / "lk", True)
            kq = chay_bs(ch := str(ngoai.parent) + os.sep + duoi.replace("/", os.sep))   # thư mục từ vựng CÓ tồn tại ⇒ bản cũ ghi trọn vào kho
            bang(not list(kho.rglob("auth.json")) and not (kho / "chua").exists(), f"{duoi}: auth.json/thư mục lọt vào kho: {kq[0]}")
            bang(kq[0] == "KHÔNG ĐO ĐƯỢC" and "nằm trong kho git" in kq[1] and os.listdir(ngoai) == [], f"{duoi}: kết luận {kq}")
            with mock.patch.dict(os.environ, {"CODEX_HOME": ch}):
                nap_mod()._ghi_dau(LR_PD, None)
            bang(not list(kho.rglob(TEN_DAU)) and not (kho / "chua").exists(), f"{duoi}: tệp dấu lọt vào kho")
            _sach_pd(kho)
    with tempfile.TemporaryDirectory(prefix="cac_pd_") as t:   # vế dương: symlink + `..` mà đích thật vẫn NGOÀI kho ⇒ không chặn nhầm
        (that := _tam_pd(t) / "that" / "con").mkdir(parents=True), (_tam_pd(t) / "codexhome").mkdir(), _lien_ket(lk := _tam_pd(t) / "lk", that, True)
        kq = chay_bs(f"{lk}{os.sep}..{os.sep}codexhome")
        bang(kq[0] == "ĐÃ NẠP" and (that.parent / "codexhome" / "auth.json").exists(), f"ngoài kho (symlink + ..) mà bị chặn: {kq}")
CA = {k: v for k, v in dict(globals()).items() if re.fullmatch(r"(?:[a-h]|p3[abcs]|pd)\d+_\w+", k) and callable(v)}
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
    ("B4_loi_giai_ma_thoat_khoi_kiem_ban", "ma", "    return p.returncode == 0 and any(", '    return p.returncode == 0 and ra.encode("ascii") and any(', "b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay"),
    ("B4_qua_han_chi_giet_cha", "ma", "        return _giet_nhom(p)[0] and False", "        return p.kill() or False", "b10_version_treo_giet_ca_nhom"),
    ("B4_so_chuoi_con", "ma", ' and any(re.fullmatch(r"\\d+\\.\\d+\\.\\d+", t) and _bo_so(t) >= _bo_so(AGY_VER)\n                                     for t in re.split(r"[\\s,;()]+", ra))', " and AGY_VER in ra", "b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay"),
    ("B4_bang_thay_san", "ma", "_bo_so(t) >= _bo_so(AGY_VER)", "_bo_so(t) == _bo_so(AGY_VER)", "b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay"),
    ("B4_san_thanh_tran", "ma", "_bo_so(t) >= _bo_so(AGY_VER)", "_bo_so(t) <= _bo_so(AGY_VER)", "b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay"),
    ("B4_chi_kiem_co_mat", "ma", "    if _ban_khop(agy):", "    if agy.is_file():", "b34_dung_ban_khong_tai_lech_hoac_hong_thi_thay"),
    ("B5_roi_ve_linux_amd64", "ma", "    muc = NEN.get(k)", '    muc = NEN.get(k) or NEN["linux_amd64"]', "b5_nen_ngoai_bang"),
    ("B6_extractall", "ma", "        tv = tf.getmembers()\n", '        tf.extractall(agy.parent, filter="fully_trusted")\n        tv = tf.getmembers()\n', "b6_tarball_doc_tu_choi"),
    ("B7_goi_agy_install", "ma", '    print(f"agy: ✓ đã cài', '    subprocess.run([str(agy), "install"], capture_output=True, timeout=15)\n    print(f"agy: ✓ đã cài', "b7_khong_goi_agy_install"),
    ("B8_doi_mot_ky_tu_sha", "ma", '"3dee9f26e2', '"4dee9f26e2', "b8_hang_ghim_dung_spec"),
    ("B9_bo_musl", "ma", ' + ("_musl" if he == "linux" and musl else "")', "", "b9_luat_chon_nen"),
    ("C1_ghi_de_ca_tep", "ma", '    d = {**d, "modelProvider": "gemini"}', '    d = {"modelProvider": "gemini"}', "c13_gop_model_provider_khong_ghi_khoa"),
    ("C2_ghi_de_khi_parse_loi", "ma", 'return print(f"agy: ⚠ settings.json không đọc được', 'd = {}; print(f"', "c2_settings_khong_phai_object_khong_dung"),
    ("C3_ghi_api_key", "ma", '    d = {**d, "modelProvider": "gemini"}', '    d = {**d, "modelProvider": "gemini", "apiKey": os.environ.get("GEMINI_API_KEY", "")}', "c13_gop_model_provider_khong_ghi_khoa"),
    ("D2_ghi_cwd_khi_khong_dat_bien", "ma", "lambda: gop_settings(home)):", 'lambda: gop_settings(home), lambda: open(env.get("CLAUDE_ENV_FILE") or "env.sh", "a").write("x\\n")):', "d2_khong_env_file_khong_tao_tep"),
    ("D1_ghi_lai_dong_tat", "ma", "lambda: gop_settings(home)):", 'lambda: gop_settings(home), lambda: env.get("CLAUDE_ENV_FILE") and open(env["CLAUDE_ENV_FILE"], "a").write("export AGY_CLI_DISABLE_AUTO_UPDATE=1\\n")):', "d1_env_file_khong_dung"),
    ("G1_sha256_thay_sha512", "ma", 'a["browser_download_url"], hashlib.sha512(du).hexdigest()))', 'a["browser_download_url"], hashlib.sha256(du).hexdigest()))', "g1_ghim_in_dung_sau_cap"),
    ("G1_nen_python_rong", "ma", """        print(f'    "{k}": ("{u}", "{h}"),')""", "        pass", "g1_ghim_in_dung_sau_cap"),
    ("G1_cat_bam_python", "ma", """        print(f'    "{k}": ("{u}", "{h}"),')""", """        print(f'    "{k}": ("{u}", "{h[:64]}"),')""", "g1_ghim_in_dung_sau_cap"),
    ("G1_tai_mot_lan_dung_lai", "ma", '            du = tai(a["browser_download_url"])', '            du = du if dong else tai(a["browser_download_url"])', "g1_ghim_in_dung_sau_cap"),
    ("G2_in_nen_truoc_kiem", "ma", "        dong = []", '        dong = []; print("NEN = {}")', "g2_ghim_tu_choi_khi_sai"),
    # Lớp `ghim-output-oracle` lượt 2 (F01-e…p): mỗi biểu hiện một đột biến SẢN PHẨM, chết ở chốt hợp đồng đúng ca
    ("F01e_khoi_thua_sau_dong", "ma", '    print("}")', '    print("}"); print("NEN = {}")', "g1_ghim_in_dung_sau_cap"),
    ("F01f_thieu_dong_dong", "ma", '    print("}")', "    pass", "g1_ghim_in_dung_sau_cap"),
    ("F01g_doi_cho_ten_tai_san", "ma", '"darwin_amd64": "mac_x64", "darwin_arm64": "mac_arm64"}', '"darwin_amd64": "mac_arm64", "darwin_arm64": "mac_x64"}', "g1_ghim_in_dung_sau_cap"),
    ("F01h_bo_ban_chi_dinh", "ma", "return ghim_agy(argv[2] if len(argv) == 3 else None)", "return ghim_agy(None)", "g3_ghim_ban_chi_dinh"),
    ("F01i_luon_latest", "ma", '(f"tags/{ban}" if ban else "latest")', '"latest"', "g3_ghim_ban_chi_dinh"),
    ("F01j_loi_mang_rc0", "ma", 'return print(f"ghim-agy: ✗ lỗi {type(e).__name__}") or 1', 'return print(f"ghim-agy: ✗ lỗi {type(e).__name__}") or 0', "g2_ghim_tu_choi_khi_sai"),
    ("F01k_thieu_chi_kiem_cuoi", "ma", """            if a is None:
                return print(f"ghim-agy: ✗ thiếu tài sản {k}") or 1""", """            if a is None and k != "darwin_arm64":
                continue
            if a is None:
                return print(f"ghim-agy: ✗ thiếu tài sản {k}") or 1""", "g2_ghim_tu_choi_khi_sai"),
    ("F01l_digest_chi_kiem_cuoi", "ma", '!= a.get("digest"):', '!= a.get("digest") and k == "darwin_arm64":', "g2_ghim_tu_choi_khi_sai"),
    ("F01m_tarball_chi_kiem_cuoi", "ma", 'if len(tvg) != 1 or tvg[0].name != "antigravity" or not tvg[0].isreg():',
     'if (len(tvg) != 1 or tvg[0].name != "antigravity" or not tvg[0].isreg()) and k == "darwin_arm64":', "g2_ghim_tu_choi_khi_sai"),
    ("F01n_ghi_tep", "ma", "        dong = []", '        dong = []; open("ghim-agy.log", "a").close()', "g1_ghim_in_dung_sau_cap"),
    ("F01o_bo_kiem_ten_member", "ma", ' or tvg[0].name != "antigravity"', "", "g2_ghim_tu_choi_khi_sai"),
    ("F01p_bo_kiem_tep_thuong", "ma", " or not tvg[0].isreg()", "", "g2_ghim_tu_choi_khi_sai"),
    ("G2_bo_kiem_digest", "ma", '    if "sha256:" + hashlib.sha256(du).hexdigest() != a.get("digest"):', "    if False:", "g2_ghim_tu_choi_khi_sai"),
    ("G2_bo_kiem_tarball_ghim", "ma", '                return print(f"ghim-agy: ✗ tarball', '                pass; print(f"ghim-agy: ✗ tarball', "g2_ghim_tu_choi_khi_sai"),
    ("G2_bo_kiem_ban", "ma", ' and re.fullmatch(r"\\d+\\.\\d+\\.\\d+", argv[2])):', "):", "g2_ghim_tu_choi_khi_sai"),
    # Lớp `ghim-output-oracle` lượt 5 (F01-w): socket giả phải giữ buffer protocol như socket thật
    ("F01w_body_phan_tu_int", "ma", 'urllib.request.Request(url, headers={"User-Agent": "tra-luat-ghim-agy"})', 'urllib.request.Request(url, headers={"User-Agent": "tra-luat-ghim-agy", "Content-Length": "1"}, data=[1], method="GET")', "g1_ghim_in_dung_sau_cap"),
    ("F01w_body_phan_tu_list", "ma", 'urllib.request.Request(url, headers={"User-Agent": "tra-luat-ghim-agy"})', 'urllib.request.Request(url, headers={"User-Agent": "tra-luat-ghim-agy", "Content-Length": "1"}, data=[[65]], method="GET")', "g1_ghim_in_dung_sau_cap"),
    ("F01w_body_khong_lien_tuc", "ma", 'urllib.request.Request(url, headers={"User-Agent": "tra-luat-ghim-agy"})', 'urllib.request.Request(url, headers={"User-Agent": "tra-luat-ghim-agy"}, data=memoryview(b"ABCD")[::2], method="GET")', "g1_ghim_in_dung_sau_cap"),
    # Lớp `ghim-output-oracle` lượt 3 (F01-n/q/r/s): đột biến SẢN PHẨM, mỗi cái chỉ chết được ở hậu điều chung của đúng ca
    ("F01n_path_write_text_tuyet_doi", "ma", "        dong = []", '        dong = []; Path(os.environ.get("TMPDIR") or os.environ.get("TEMP") or "/tmp", "ghim-agy-lot.txt").write_text("x", encoding="utf-8")', "g1_ghim_in_dung_sau_cap"),
    ("F01n_os_open", "ma", "        dong = []", '        dong = []; os.close(os.open(os.path.join(os.environ.get("TMPDIR") or os.environ.get("TEMP") or "/tmp", "ghim-agy-lot.bin"), os.O_WRONLY | os.O_CREAT | os.O_TRUNC))', "g3_ghim_ban_chi_dinh"),
    ("F01n_temporaryfile", "ma", "        dong = []", "        dong = []; tempfile.TemporaryFile().close()", "g1_ghim_in_dung_sau_cap"),
    ("F01n_tao_roi_xoa", "ma", "        dong = []", '        dong = []; Path("ghim-agy-tam.txt").write_text("x", encoding="utf-8"); Path("ghim-agy-tam.txt").unlink()', "g1_ghim_in_dung_sau_cap"),
    ("F01n_ghi_roi_nuot_loi", "ma", "        dong = []", '        dong = []\n        try:\n            open("ghim-agy.log", "a").close()\n        except BaseException:\n            pass', "g3_ghim_ban_chi_dinh"),
    ("F01n_ghi_o_nhanh_loi", "ma", '        return print(f"ghim-agy: ✗ lỗi {type(e).__name__}") or 1', '        Path(os.environ.get("TMPDIR") or os.environ.get("TEMP") or "/tmp", "ghim-agy-loi.txt").write_text(type(e).__name__, encoding="utf-8")\n        return print(f"ghim-agy: ✗ lỗi {type(e).__name__}") or 1', "g2_ghim_tu_choi_khi_sai"),
    ("F01q_timeout_chuoi_release", "ma", "timeout=30) as r:", 'timeout="30") as r:', "g3_ghim_ban_chi_dinh"),
    ("F01q_timeout_chuoi_tai", "ma", "timeout=300) as r:", 'timeout="300") as r:', "g1_ghim_in_dung_sau_cap"),
    ("F01r_argv_sai_ghi_tep", "ma", '    return print("dùng: cloud_agent_creds.py', '    open("ghim-agy-argv.log", "a").close()\n    return print("dùng: cloud_agent_creds.py', "g2_ghim_tu_choi_khi_sai"),
    ("F01r_argv_sai_van_tai", "ma", '    return print("dùng: cloud_agent_creds.py', '    try:\n        doc_release()\n    except Exception:\n        pass\n    return print("dùng: cloud_agent_creds.py', "g2_ghim_tu_choi_khi_sai"),
    ("F01s_ban_bo_kiem_digest", "ma", '    if "sha256:" + hashlib.sha256(du).hexdigest() != a.get("digest"):', '    if ban is None and "sha256:" + hashlib.sha256(du).hexdigest() != a.get("digest"):', "g2_ghim_tu_choi_khi_sai"),
    ("F01s_ban_bo_kiem_tarball", "ma", 'if len(tvg) != 1 or tvg[0].name != "antigravity" or not tvg[0].isreg():', 'if ban is None and (len(tvg) != 1 or tvg[0].name != "antigravity" or not tvg[0].isreg()):', "g2_ghim_tu_choi_khi_sai"),
    ("F01s_ban_bo_kiem_thieu", "ma", '            if a is None:\n                return print(f"ghim-agy: ✗ thiếu tài sản {k}") or 1', '            if a is None and ban is not None:\n                continue\n            if a is None:\n                return print(f"ghim-agy: ✗ thiếu tài sản {k}") or 1', "g2_ghim_tu_choi_khi_sai"),
    ("F01s_ban_loi_rc0", "ma", 'return print(f"ghim-agy: ✗ lỗi {type(e).__name__}") or 1', 'return print(f"ghim-agy: ✗ lỗi {type(e).__name__}") or (0 if ban else 1)', "g2_ghim_tu_choi_khi_sai"),
    # Lớp `ghim-output-oracle` lượt 4 (F01-t/u/v): vòng đời tiến trình thật · validation của urllib thật · cờ `open` theo danh sách cho phép
    ("F01t_ghi_luc_tat_luong", "ma", "        dong = []", '        dong = []; threading._register_atexit(lambda: open("ghim-agy-tat.log", "a").close())', "g1_ghim_in_dung_sau_cap"),
    ("F01t_ghi_luc_atexit_nhanh_loi", "ma", '        return print(f"ghim-agy: ✗ lỗi {type(e).__name__}") or 1', '        __import__("atexit").register(lambda: open("ghim-agy-thoat.log", "a").close())\n        return print(f"ghim-agy: ✗ lỗi {type(e).__name__}") or 1', "g2_ghim_tu_choi_khi_sai"),
    ("F01u_tieu_de_none", "ma", 'headers={"User-Agent": "tra-luat-ghim-agy"}', 'headers={"User-Agent": None}', "g3_ghim_ban_chi_dinh"),
    ("F01u_get_kem_than_chuoi", "ma", 'headers={"User-Agent": "tra-luat-ghim-agy"})', 'headers={"User-Agent": "tra-luat-ghim-agy"}, data="than", method="GET")', "g2_ghim_tu_choi_khi_sai"),
    ("F01v_mo_doc_co_tac_dong_tep", "ma", "        dong = []", '        dong = []; os.close(os.open("moi-nhu.txt", os.O_RDONLY | getattr(os, "O_TEMPORARY", os.O_TRUNC)))', "g1_ghim_in_dung_sau_cap"),
    ("F01n_ghi_muc_module_truoc_guard", "ma", "def main(argv):", 'open("ghim-agy-dau.log", "a").close()\ndef main(argv):', "g3_ghim_ban_chi_dinh"),
    ("F01n_ghi_muc_module_sau_guard", "ma", None, lambda s: s + 'open("ghim-agy-nap.log", "a").close()\n', "g1_ghim_in_dung_sau_cap"),
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
    ("PD1_bo_chot_bootstrap", "tlgws", "        if (kho := _trong_kho_git(os.path.dirname(dst))) is not None:", "        if (kho := None) is not None:", "pd1_codex_home_trong_kho_khong_ghi"),
    ("PD2_luon_tra_duong_dan", "tlgws", "    return None   # không tổ tiên nào có `.git`", "    return os.path.abspath(path)", "pd2_codex_home_ngoai_kho_van_nap"),
    ("PD3_git_phai_la_thu_muc", "tlgws", "                os.lstat(g)\n", "                if not os.path.isdir(g): raise FileNotFoundError(g)\n", "pd3_git_la_tep_van_chan"),
    ("PD4_theo_symlink", "tlgws", "                os.lstat(g)\n", "                os.stat(g)\n", "pd4_git_la_symlink_van_chan"),
    ("PD5_makedirs_truoc_khi_kiem", "tlgws", "        if (kho := _trong_kho_git(os.path.dirname(dst))) is not None:", "        os.makedirs(os.path.dirname(dst), exist_ok=True)\n        if (kho := _trong_kho_git(os.path.dirname(dst))) is not None:", "pd5_dich_chua_ton_tai_khong_tao_thu_muc"),
    ("PD5_khong_len_to_tien", "tlgws", "            if os.path.dirname(d) == d:\n                break\n", "            break\n", "pd5_dich_chua_ton_tai_khong_tao_thu_muc"),
    ("PD6_bo_chot_ghi_dau", "ma", "        if tl_gws._trong_kho_git(str(_codex_dir())) is not None:\n            return\n", "", "pd6_ghi_dau_trong_kho_khong_ghi"),
    ("PD6_khong_nap_duoc_chot_van_ghi", "ma", "    except Exception:  # noqa: BLE001\n        return\n    _ghi_nguyen_tu(_codex_dir() / TEN_DAU", "    except Exception:  # noqa: BLE001\n        pass\n    _ghi_nguyen_tu(_codex_dir() / TEN_DAU", "pd6_ghi_dau_trong_kho_khong_ghi"),
    ("PD7_bo_chuoi_realpath", "tlgws", "    for d in dict.fromkeys((os.path.abspath(path), os.path.realpath(path))):", "    for d in (os.path.abspath(path),):", "pd7_symlink_ngoai_kho_tro_vao_kho"),
    ("PD7_bo_chuoi_tu_vung", "tlgws", "    for d in dict.fromkeys((os.path.abspath(path), os.path.realpath(path))):", "    for d in (os.path.realpath(path),):", "pd7_symlink_ngoai_kho_tro_vao_kho"),
    ("PD8_realpath_sau_abspath", "tlgws", "os.path.abspath(path), os.path.realpath(path))):", "os.path.abspath(path), os.path.realpath(os.path.abspath(path)))):", "pd8_symlink_roi_hai_cham_vao_kho"),
    ("P3S2_bo_or_true", "settings", "ghi-nguoc --neu-doi || true'", "ghi-nguoc --neu-doi'", "p3s2_stop_chay_that"),
)
TU_KIEM = (   # F2 — (tên, tệp, gốc, thay, ca đích, hạng mong đợi)
    ("vo_can_qua_except_doi_kieu", "ma", "    he = he.lower()\n", "    raise AttributeError('vo can')\n", "b9_luat_chon_nen", "TIN_DUNG_GIA"),
    ("chi_them_chu_thich", "ma", "TIMEOUT_MAC_DINH, HAN_VERSION, HAN_DON = 180, 15, 10\n", "TIMEOUT_MAC_DINH, HAN_VERSION, HAN_DON = 180, 15, 10  # vo hai\n", "a5_doc_timeout", "SONG_SOT"),
    ("vo_can_trong_tien_trinh_con", "ma", '    if argv == ["ghim-agy"] or (', '    ten_khong_ton_tai\n    if argv == ["ghim-agy"] or (', "g1_ghim_in_dung_sau_cap", "TIN_DUNG_GIA"),
    ("callback_tat_luong_khong_ghi", "ma", "        dong = []", "        dong = []; threading._register_atexit(lambda: None)", "g1_ghim_in_dung_sau_cap", "SONG_SOT"),
    ("mo_chi_doc_thuan", "ma", "        dong = []", '        dong = []; os.close(os.open("moi-nhu.txt", os.O_RDONLY))', "g1_ghim_in_dung_sau_cap", "SONG_SOT"),
    ("timeout_bool_thu_vien_that_nhan", "ma", "timeout=30) as r:", "timeout=True) as r:", "g3_ghim_ban_chi_dinh", "SONG_SOT"),
    ("loi_cu_phap_la_loi_dung_harness", "ma", "def main(argv):", "def main(argv:", "g1_ghim_in_dung_sau_cap", "TIN_DUNG_GIA"),
)
def phan_hang(rc, ra, ten_ca):
    """GIET chỉ khi con thoát 3 VÀ có dòng `DO:<đúng ca đích>:` — `AssertionError` trần hay ca khác là tín dụng giả."""
    if rc == 3:
        return "GIET" if re.search(rf"^DO:{re.escape(ten_ca)}:", ra, re.M) else "TIN_DUNG_GIA"
    return {0: "SONG_SOT", 5: "BO_QUA", 4: "TIN_DUNG_GIA"}.get(rc, "HONG")
def chay_dot_bien(ten, tep, cu, moi, ten_ca):
    nguon, bien = {"ma": (MA, "CAC_MA"), "hook": (HOOK, "CAC_HOOK"), "gs": (GS, "CAC_GS"), "settings": (SETTINGS, "CAC_SETTINGS"), "tlgws": (TLGWS, "CAC_TLGWS")}[tep]
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
