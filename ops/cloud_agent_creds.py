#!/usr/bin/env python3
"""`nap` (bootstrap + ĐÚNG MỘT dòng `agent_creds:` kể cả khi bootstrap thoát sớm/quá hạn/sai hợp đồng) và `cai-agy` (agy ghim,
sha512, settings, CLAUDE_ENV_FILE) cho phiên cloud — spec CLOUD-SETUP-P2B-WIRE r1 (#1039). Cả hai luôn rc 0. Test: *_test.py."""
import contextlib, hashlib, io, json, math, os, platform, re, shutil, signal, subprocess, sys, tarfile, tempfile, time, urllib.request  # noqa: E401
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
TRANG_THAI = ("ĐÃ NẠP", "KHÔNG CẤU HÌNH", "KHÔNG ĐO ĐƯỢC")
TIMEOUT_MAC_DINH, HAN_VERSION, HAN_DON = 180, 15, 10
DONG_ENV = "export AGY_CLI_DISABLE_AUTO_UPDATE=1"
# Hằng ghim — chép NGUYÊN VĂN spec r1 mục "Hằng ghim agy". Đổi bản ⇒ revision mới của spec, không sửa tại chỗ.
AGY_VER = "1.4.12"
_U = "https://storage.googleapis.com/antigravity-public/antigravity-cli/1.4.12-4768735748292608/"
NEN = {
    "linux_amd64": (_U + "linux-x64/cli_linux_x64.tar.gz", "ea01c73b772187bca928852cf96235f0d846d6da5ebdac188b9ae719597465737f325540d483ee5f3f62d151029001713344972a187ddfb98cc7b97f7204b7f4"),
    "linux_arm64": (_U + "linux-arm/cli_linux_arm64.tar.gz", "7cae317fb6a02eb387982f06bfb234b366879cf9a80ad8969b571e5a55d1e37a6a5a49cd6b703c0443bb417937cf5e3b14a8c80cb26917ad79eef723a9f374c7"),
    "linux_amd64_musl": (_U + "linux-x64-musl/cli_linux_x64_musl.tar.gz", "60a2705b9d0446a88fe2a685a044e0f9ec65f9742492d96e6fa3a87c9c477d3fddd9c4d7f22bca7bdb2a99d6dd5833de9d6e690eb8fd9e77ebe25794fdb4555a"),
    "linux_arm64_musl": (_U + "linux-arm-musl/cli_linux_arm64_musl.tar.gz", "767902b8569d08e7283139f3aba05eacdc0070b96d940ca4d2fad863ea6c2f3c35bb79ab079fcfeb87f6f79272bb4c0b666af8829873883dc1c9798321dd28f6"),
    "darwin_amd64": (_U + "darwin-x64/cli_mac_x64.tar.gz", "1d78368cd5a136dc4c7cc71cfe4649d1b1e643630d79327ff3c4efd4b19a90d5603e2cf65a54f80c7eaef973dd09f854dae8a8228b4edd4c6466c679ded9babf"),
    "darwin_arm64": (_U + "darwin-arm/cli_mac_arm64.tar.gz", "e858cfc02fb5bb500a760643da270accd2847aa986b7e2973da97ad1928b99d62f62bad28c039e25b65e1ca073d27b2f30b13ed0919d0329774eb1e0ee5b4748"),
}
def doc_timeout(gia_tri):
    try:   # rác/âm/0/inf/nan và > 1 ngày (Popen.communicate tràn — F02) ⇒ mặc định
        return v if math.isfinite(v := float(gia_tri)) and 0 < v <= 86400 else TIMEOUT_MAC_DINH
    except (TypeError, ValueError):
        return TIMEOUT_MAC_DINH
def ket_luan(dong_agent, rc):
    if not dong_agent:
        return f"KHÔNG ĐO ĐƯỢC — bootstrap thoát rc={rc} trước bước agent"
    if len(dong_agent) > 1:
        return f"KHÔNG ĐO ĐƯỢC — đầu ra bootstrap không đúng hợp đồng ({len(dong_agent)} dòng agent_creds:)"
    s, sep, ct = dong_agent[0].split("agent_creds:", 1)[1].strip().partition(" — ")
    if not sep or s not in TRANG_THAI:
        return "KHÔNG ĐO ĐƯỢC — đầu ra bootstrap không đúng hợp đồng (trạng thái lạ)"
    return f"{s} — {ct} (bootstrap rc={rc})"
def _nhom_song(pgid):
    """Nhóm còn thành viên KHÔNG phải zombie: True / False; không đo được ⇒ None (F11 — đo cả nhóm, không chỉ cha)."""
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except OSError:
        return None
    if not Path("/proc/self/stat").exists():
        return None
    tt = []
    for f in Path("/proc").glob("[0-9]*/stat"):   # tiến trình biến mất giữa chừng: bỏ qua đúng tệp ấy
        with contextlib.suppress(OSError, IndexError):
            tt.append(f.read_text().rsplit(")", 1)[1].split())
    return any(len(x) > 2 and x[2] == str(pgid) and x[0] != "Z" for x in tt)
def _giet_nhom(p):
    """Giết cả nhóm, thu output còn lại, rồi KIỂM LẠI cả nhóm (hạn HAN_DON). (đã chết?, bytes đã nhận)."""
    ra = b""
    with contextlib.suppress(OSError):
        os.killpg(p.pid, signal.SIGKILL) if os.name != "nt" else p.kill()
    try:
        ra = p.communicate(timeout=HAN_DON)[0] or b""
    except subprocess.TimeoutExpired as e:   # nhóm còn giữ ống: vẫn giữ phần đã nhận (F12)
        ra = e.output or b""
    except (OSError, ValueError):
        pass
    if p.poll() is None or os.name == "nt":
        return p.poll() is not None, ra
    het = time.monotonic() + HAN_DON
    while (song := _nhom_song(p.pid)) and time.monotonic() < het:
        time.sleep(0.1)
    return song is False, ra
def nap(env=os.environ):
    khoa, rc = env.get("TL_MASTER_KEY") or "", None
    if not khoa:
        print("agent_creds: BỎ QUA — thiếu TL_MASTER_KEY")
        return 0
    han, tl = doc_timeout(env.get("TL_CLOUD_BOOTSTRAP_TIMEOUT_GIAY")), GOC / "scripts" / "tl.py"
    try:
        if not tl.is_file():
            raise FileNotFoundError(str(tl))
        p = subprocess.Popen([sys.executable, str(tl), "bootstrap", "--env", "code", "--no-nlm"], cwd=str(GOC),
                             stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             start_new_session=os.name != "nt")
    except OSError as e:
        print(f"agent_creds: KHÔNG ĐO ĐƯỢC — không chạy được bootstrap ({type(e).__name__})")
        return 0
    try:
        (ra, _), rc, het_han = p.communicate(timeout=han), p.returncode, None
    except Exception as e:  # noqa: BLE001 — quá hạn hay lỗi chờ: dọn cả nhóm, vẫn chuyển tiếp log đã nhận (F12), đúng một dòng
        (da, ra), ly = _giet_nhom(p), f"bootstrap quá {han:g} s" if isinstance(e, subprocess.TimeoutExpired) else f"lỗi chờ bootstrap ({type(e).__name__})"
        het_han = f"KHÔNG ĐO ĐƯỢC — {ly}, {'đã dừng' if da else 'KHÔNG dừng được'}"
    dong_agent = []
    for d in ra.decode("utf-8", "replace").replace(khoa, "***").splitlines():
        if "agent_creds:" in d:
            dong_agent.append(d)
        else:
            print(d)
    print("agent_creds: " + (het_han or ket_luan(dong_agent, rc)))
    return 0  # nap: luôn 0 (mục tiêu 1)
def _co_musl():
    if any(Path(f).exists() for f in ("/lib/libc.musl-x86_64.so.1", "/lib/libc.musl-aarch64.so.1")):
        return True
    try:
        return "musl" in subprocess.run(["ldd", "/bin/ls"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError, ValueError):
        return False
def khoa_nen(he, may, musl):
    """Luật chọn nền của install.sh chính thức (spec mục Hằng ghim)."""
    he = he.lower()
    may = {"x86_64": "amd64", "amd64": "amd64", "arm64": "arm64", "aarch64": "arm64"}.get(may.lower(), may.lower())
    return f"{he}_{may}" + ("_musl" if he == "linux" and musl else "")
def khoa_nen_hien_tai():
    return khoa_nen(platform.system(), platform.machine(), platform.system() == "Linux" and _co_musl())
def tai(url):
    with urllib.request.urlopen(url, timeout=300) as r:
        return r.read()
def _ban_khop(agy):   # `agy --version` rc 0 và có TOKEN đúng bằng AGY_VER (1.4.120, 1.4.12rc1 ⇒ lệch); thiếu/hỏng ⇒ False
    try:
        p = subprocess.Popen([str(agy), "--version"], stdin=subprocess.DEVNULL, stderr=subprocess.STDOUT, stdout=subprocess.PIPE,
                             start_new_session=os.name != "nt")
    except OSError:
        return False
    try:
        ra = p.communicate(timeout=HAN_VERSION)[0].decode("utf-8", "replace")
    except Exception:  # noqa: BLE001 — quá 15 s: giết CẢ NHÓM (tiến trình con của agy), không chỉ cha (F01)
        return _giet_nhom(p)[0] and False
    return p.returncode == 0 and AGY_VER in re.split(r"[\s,;()]+", ra)
def _ghi_nguyen_tu(p, du_lieu, quyen=None):
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tam = tempfile.mkstemp(dir=str(p.parent), prefix=f".{p.name}.")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(du_lieu), f.flush(), os.fsync(f.fileno())
        if quyen is not None:
            os.chmod(tam, quyen)
        os.replace(tam, p)
    except BaseException:
        Path(tam).unlink(missing_ok=True)
        raise
def cai_dat_agy(home):
    agy = home / ".local" / "bin" / "agy"
    if _ban_khop(agy):
        return print(f"agy: ✓ đã có {AGY_VER} — không tải")
    k = khoa_nen_hien_tai()
    muc = NEN.get(k)
    if muc is None:
        return print(f"agy: CHƯA HỖ TRỢ {k}")
    du_lieu = tai(muc[0])
    if hashlib.sha512(du_lieu).hexdigest() != muc[1]:
        return print("agy: ✗ sha512 lệch — không ghi gì")
    with tarfile.open(fileobj=io.BytesIO(du_lieu), mode="r:gz") as tf:
        tv = tf.getmembers()
        if len(tv) != 1 or tv[0].name != "antigravity" or not tv[0].isreg():
            return print("agy: ✗ tarball không đúng MỘT tệp thường `antigravity` — từ chối toàn bộ")
        _ghi_nguyen_tu(agy, tf.extractfile(tv[0]).read(), 0o755)
    print(f"agy: ✓ đã cài {AGY_VER} ({k}) → {agy}")
    thay = shutil.which("agy")
    if thay is None or Path(thay).resolve() != agy.resolve():
        print(f"agy: ⚠ `agy` trong PATH là {thay!r}, không phải {agy} — thêm ~/.local/bin vào PATH")
def gop_settings(home):
    p, d = home / ".gemini" / "antigravity-cli" / "settings.json", {}
    if p.exists():
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            return print(f"agy: ⚠ settings.json không đọc được ({type(e).__name__}) — không đụng tệp")
        if not isinstance(d, dict):
            return print("agy: ⚠ settings.json không phải JSON object — không đụng tệp")
    d = {**d, "modelProvider": "gemini"}
    _ghi_nguyen_tu(p, (json.dumps(d, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print("agy: settings.json modelProvider = gemini")
def dat_env_file(env):   # `CLAUDE_ENV_FILE` có ĐÚNG MỘT dòng DONG_ENV (chạy lại không nhân bản); giữ dòng khác và quyền tệp
    if env.get("CLAUDE_ENV_FILE"):
        p = Path(env["CLAUDE_ENV_FILE"])
        cu = p.read_text(encoding="utf-8").splitlines() if p.exists() else []
        if cu.count(DONG_ENV) != 1:
            _ghi_nguyen_tu(p, ("\n".join([x for x in cu if x != DONG_ENV] + [DONG_ENV]) + "\n").encode("utf-8"),
                           p.stat().st_mode & 0o777 if p.exists() else None)
        print("agy: CLAUDE_ENV_FILE có AGY_CLI_DISABLE_AUTO_UPDATE=1")
def cai_agy(env=os.environ):
    home = Path(env.get("HOME") or Path.home())
    for buoc in (lambda: cai_dat_agy(home), lambda: gop_settings(home), lambda: dat_env_file(env)):
        try:
            buoc()
        except Exception as e:  # noqa: BLE001 — mục tiêu 2: lỗi mạng/ghi chỉ là MỘT dòng `agy: …`, rc 0
            print(f"agy: ✗ lỗi {type(e).__name__}")
    return 0
def main(argv):
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="backslashreplace")
    if argv in (["nap"], ["cai-agy"]):
        return {"nap": nap, "cai-agy": cai_agy}[argv[0]]()
    return print("dùng: cloud_agent_creds.py nap | cai-agy", file=sys.stderr) or 2
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
