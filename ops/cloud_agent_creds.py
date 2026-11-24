#!/usr/bin/env python3
"""`nap` (bootstrap + ĐÚNG MỘT dòng `agent_creds:` kể cả khi bootstrap thoát sớm/quá hạn/sai hợp đồng) và `cai-agy` (agy ghim,
sha512, settings) cho phiên cloud — spec CLOUD-SETUP-P2B-WIRE r1 (#1039) + r2 (bản ghim là SÀN, `ghim-agy`). `ghi-nguoc [--neu-doi]` (#1089, spec CLOUD-SETUP-P3-WRITEBACK r2): ghi
NGƯỢC auth.json Codex vào tl_agent_creds.enc qua webapp `agent_creds_put` (CAS md5). Cả ba luôn rc 0. Test: *_test.py."""
import base64, contextlib, ctypes, hashlib, io, json, math, os, platform, re, shutil, signal, subprocess, sys, tarfile, tempfile, threading, time, urllib.request  # noqa: E401
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
TRANG_THAI = ("ĐÃ NẠP", "KHÔNG CẤU HÌNH", "KHÔNG ĐO ĐƯỢC")
TIMEOUT_MAC_DINH, HAN_VERSION, HAN_DON = 180, 15, 10
# Hằng ghim — chép NGUYÊN VĂN spec r2 mục "Thay đổi 1". Là SÀN: bản cài sẵn mới hơn (agy tự cập nhật) được giữ.
# Ghim lại: `cloud_agent_creds.py ghim-agy` in khối mới ⇒ dán vào revision đặc tả kế tiếp rồi vào đây.
AGY_VER = "1.5.16"
_U = "https://github.com/google-antigravity/antigravity-cli/releases/download/1.5.16/"
NEN = {
    "linux_amd64": (_U + "agy_cli_linux_x64.tar.gz", "3dee9f26e298156db673f6ce2a0f5dfed5b30006e04ceb9809c68070e7b717587b33a3da0f8bc2eda45af81a50bc8b14c82b28ae5832bcfe3e7fd49397117b31"),
    "linux_arm64": (_U + "agy_cli_linux_arm64.tar.gz", "23c193151499a4986fd5fa0d8132665cc8ffbad6cc0b3ff4fd53a2cb68abb76b149a992b836d53063443cd89add335f14d8134fb02abdcecbf6e1eaef6c53d33"),
    "linux_amd64_musl": (_U + "agy_cli_linux_x64_musl.tar.gz", "9f868c13f308557192b8c3fa30f1251283167b7e551e9f0f05ed0fa2640e91e02accaeacd41692a0422e8de90c1cc0b6e327f2b6befbd11080a4881d45bf61b1"),
    "linux_arm64_musl": (_U + "agy_cli_linux_arm64_musl.tar.gz", "4bc5c802c97ca19404c666136f1e74dc880a3b0346e7c6950ad4e217056c6cc86ae5afa633aa5989a260600f49cb6e71db438558c4f2d44e5f5bdab8bb38980c"),
    "darwin_amd64": (_U + "agy_cli_mac_x64.tar.gz", "b3eae073ee633032e9d473cdc7725c30bdfe2e09436bc36cfb3422e7e5fa3733de9591a7f78d02362294e7bf87e345d70e5d839689e526129a6f3fc041857a05"),
    "darwin_arm64": (_U + "agy_cli_mac_arm64.tar.gz", "33f5617dc74fea606d47b2483c6d271c850c9f3c9c55b724c664c3c0d4b82100d819fbcf55714f851765f6628d4296883ac8939b4fdeb55d5e6b9ce923135d18"),
}
TAI_SAN_AGY = {"linux_amd64": "linux_x64", "linux_arm64": "linux_arm64", "linux_amd64_musl": "linux_x64_musl",
               "linux_arm64_musl": "linux_arm64_musl", "darwin_amd64": "mac_x64", "darwin_arm64": "mac_arm64"}
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
_SUBREAPER = None
def _dat_subreaper():
    """`prctl(PR_SET_CHILD_SUBREAPER)` (Linux), gọi TRƯỚC Popen; không đặt được ⇒ False ⇒ không bao giờ báo "đã dừng" (#1039 (B))."""
    global _SUBREAPER
    if _SUBREAPER is None:
        try:
            _SUBREAPER = ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) == 0
        except (OSError, AttributeError, TypeError):
            _SUBREAPER = False
    return _SUBREAPER
def _giet_nhom(p):
    """SIGKILL nhóm, thu output, thu hồi thành viên (subreaper); CHỈ ESRCH của `killpg(pg, 0)` là đã dừng. (đã dừng?, bytes)."""
    ra = b""
    with contextlib.suppress(OSError):
        os.killpg(p.pid, signal.SIGKILL) if os.name != "nt" else p.kill()
    try:
        ra = p.communicate(timeout=HAN_DON)[0] or b""
    except subprocess.TimeoutExpired as e:   # nhóm còn giữ ống: vẫn giữ phần đã nhận (F12)
        ra = e.output or b""
    except (OSError, ValueError):
        pass
    if os.name == "nt" or not _dat_subreaper():
        return False, ra
    het = time.monotonic() + HAN_DON
    while True:
        with contextlib.suppress(OSError):
            while os.waitpid(-p.pid, os.WNOHANG)[0] > 0:   # thu hồi zombie của nhóm (con cháu đã về tay subreaper)
                pass
        try:
            os.killpg(p.pid, 0)
        except ProcessLookupError:
            return True, ra
        except OSError:
            return False, ra
        if time.monotonic() >= het:
            return False, ra
        time.sleep(0.05)
def nap(env=os.environ):
    khoa, rc = env.get("TL_MASTER_KEY") or "", None
    if not khoa:
        print("agent_creds: BỎ QUA — thiếu TL_MASTER_KEY")
        return _dau_sau_nap("BỎ QUA") or 0
    han, tl = doc_timeout(env.get("TL_CLOUD_BOOTSTRAP_TIMEOUT_GIAY")), GOC / "scripts" / "tl.py"
    try:
        if not tl.is_file():
            raise FileNotFoundError(str(tl))
        _dat_subreaper()
        p = subprocess.Popen([sys.executable, str(tl), "bootstrap", "--env", "code", "--no-nlm"], cwd=str(GOC),
                             stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             start_new_session=os.name != "nt")
    except OSError as e:
        print(f"agent_creds: KHÔNG ĐO ĐƯỢC — không chạy được bootstrap ({type(e).__name__})")
        return _dau_sau_nap("KHÔNG ĐO ĐƯỢC") or 0   # review lượt 1 P2: mọi đường thoát của nap đều xử lý dấu
    try:
        (ra, _), rc, het_han = p.communicate(timeout=han), p.returncode, None
    except Exception as e:  # noqa: BLE001 — quá hạn hay lỗi chờ: dọn cả nhóm, vẫn chuyển tiếp log đã nhận (F12), đúng một dòng
        (da, ra), ly = _giet_nhom(p), f"bootstrap quá {han:g} s" if isinstance(e, subprocess.TimeoutExpired) else f"lỗi chờ bootstrap ({type(e).__name__})"
        het_han = f"KHÔNG ĐO ĐƯỢC — {ly}, {'đã dừng' if da else 'KHÔNG xác minh được việc dừng'}"
    dong_agent = []
    for d in ra.decode("utf-8", "replace").replace(khoa, "***").splitlines():
        if "agent_creds:" in d:
            dong_agent.append(d)
        else:
            print(d)
    print("agent_creds: " + (kl := het_han or ket_luan(dong_agent, rc)))
    _dau_sau_nap(kl)
    return 0  # nap: luôn 0 (mục tiêu 1)
def _co_musl():
    try:
        return any(Path(f).exists() for f in ("/lib/libc.musl-x86_64.so.1", "/lib/libc.musl-aarch64.so.1")) or "musl" in subprocess.run(["ldd", "/bin/ls"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10).stdout
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
def _bo_so(ban):
    return tuple(int(x) for x in ban.split("."))
def _ban_khop(agy):   # spec r2: rc 0 và có TOKEN đúng dạng X.Y.Z (không hậu tố rc/beta) với bộ số >= AGY_VER; thiếu/hỏng ⇒ False
    try:
        _dat_subreaper()
        p = subprocess.Popen([str(agy), "--version"], stdin=subprocess.DEVNULL, stderr=subprocess.STDOUT, stdout=subprocess.PIPE,
                             start_new_session=os.name != "nt")
    except OSError:
        return False
    try:
        ra = p.communicate(timeout=HAN_VERSION)[0].decode("utf-8", "replace")
    except Exception:  # noqa: BLE001 — quá 15 s: giết CẢ NHÓM (tiến trình con của agy), không chỉ cha (F01)
        return _giet_nhom(p)[0] and False
    return p.returncode == 0 and any(re.fullmatch(r"\d+\.\d+\.\d+", t) and _bo_so(t) >= _bo_so(AGY_VER)
                                     for t in re.split(r"[\s,;()]+", ra))
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
        return print(f"agy: ✓ đã có bản >= {AGY_VER} — không tải")
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
    if (thay := shutil.which("agy")) is None or Path(thay).resolve() != agy.resolve():
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
def cai_agy(env=os.environ):
    home = Path(env.get("HOME") or Path.home())
    for buoc in (lambda: cai_dat_agy(home), lambda: gop_settings(home)):
        try:
            buoc()
        except Exception as e:  # noqa: BLE001 — mục tiêu 2: lỗi mạng/ghi chỉ là MỘT dòng `agy: …`, rc 0
            print(f"agy: ✗ lỗi {type(e).__name__}")
    return 0
# ---------- ghim-agy (spec r2 Thay đổi 3): in khối ghim mới, KHÔNG ghi tệp ----------
_REL = "https://api.github.com/repos/google-antigravity/antigravity-cli/releases/"
def doc_release(ban=None):
    url = _REL + (f"tags/{ban}" if ban else "latest")
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "tra-luat-ghim-agy"}), timeout=30) as r:
        return json.load(r)
def ghim_agy(ban=None):
    try:
        rel = doc_release(ban)
        tag, tai_san = str(rel["tag_name"]).lstrip("v"), {a["name"]: a for a in rel["assets"]}
        if not re.fullmatch(r"\d+\.\d+\.\d+", tag):
            return print(f"ghim-agy: ✗ tag lạ {tag!r}") or 1
        dong = []
        for k, t in TAI_SAN_AGY.items():
            a = tai_san.get(f"agy_cli_{t}.tar.gz")
            if a is None:
                return print(f"ghim-agy: ✗ thiếu tài sản {k}") or 1
            du = tai(a["browser_download_url"])
            if "sha256:" + hashlib.sha256(du).hexdigest() != a.get("digest"):
                return print(f"ghim-agy: ✗ sha256 lệch digest GitHub ({k})") or 1
            with tarfile.open(fileobj=io.BytesIO(du), mode="r:gz") as tf:
                tvg = tf.getmembers()
            if len(tvg) != 1 or tvg[0].name != "antigravity" or not tvg[0].isreg():
                return print(f"ghim-agy: ✗ tarball {k} không đúng MỘT tệp thường `antigravity`") or 1
            dong.append((k, a["browser_download_url"], hashlib.sha512(du).hexdigest()))
    except Exception as e:  # noqa: BLE001 — mạng/JSON hỏng ⇒ một dòng, rc 1
        return print(f"ghim-agy: ✗ lỗi {type(e).__name__}") or 1
    print(f'AGY_VER = "{tag}"')
    print("NEN = {")
    for k, u, h in dong:
        print(f'    "{k}": ("{u}", "{h}"),')
    print("}")
    print()
    for k, u, h in dong:
        print(f"| `{k}` | `{u}` | `{h}` |")
    return 0
# ---------- ghi-nguoc (#1089, spec CLOUD-SETUP-P3-WRITEBACK r2 mục tiêu 2–3) ----------
TEN_DAU, HAN_GHI_NGUOC, LAN_CAS, BAN_TOI_THIEU = ".tra-luat-agent-creds-dau.json", 25.0, 3, (2, 21, 2, "q")
def _codex_dir():   # cùng luật với tl_gws._codex_auth_path (bootstrap ghi auth.json ở đây)
    return Path(os.environ.get("CODEX_HOME") or os.path.expanduser("~/.codex"))
def _doc_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
def _ghi_dau(last_refresh, md5):   # chỉ hai khoá; 0600; nguyên tử — không bao giờ chứa token
    if str(GOC / "scripts") not in sys.path:
        sys.path.insert(0, str(GOC / "scripts"))
    try:   # WP1334: CODEX_HOME trong kho git, hoặc không nạp được chốt của tl_gws ⇒ KHÔNG ghi dấu (fail-closed)
        import tl_gws
        if tl_gws._trong_kho_git(str(_codex_dir())) is not None:
            return
    except Exception:  # noqa: BLE001
        return
    _ghi_nguyen_tu(_codex_dir() / TEN_DAU, (json.dumps({"last_refresh": last_refresh, "md5": md5}) + "\n").encode("utf-8"), 0o600)
def _dau_sau_nap(kl):
    """Mục tiêu 3: ghi dấu CHỈ KHI bootstrap đã đè auth.json bằng bản bundle (đĩa == bundle); mọi kết luận khác ⇒ xoá dấu."""
    try:
        d = _doc_json(_codex_dir() / "auth.json")
        if kl.startswith("ĐÃ NẠP — ") and "codex auth.json → " in kl and isinstance(d, dict):
            return _ghi_dau(d.get("last_refresh"), None)
        (_codex_dir() / TEN_DAU).unlink(missing_ok=True)
    except OSError:
        pass
def ban_webapp(v):   # (số, số, số, chữ) hoặc None — so theo bộ, không so chuỗi thô ("2.21.10" > "2.21.2q")
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)([a-z]?)", v) if isinstance(v, str) else None
    return (int(m[1]), int(m[2]), int(m[3]), m[4]) if m else None
def _ma_loi(r):   # chỉ mã dạng HẰNG (server tự đặt); văn bản tự do của tầng vận chuyển không được in
    e = r.get("error") if isinstance(r, dict) else None
    return e if isinstance(e, str) and re.fullmatch(r"[A-Z][A-Z0-9_]{0,63}", e) else "LỖI_GỌI"
def _giai(store, khoa, blob):
    p = json.loads(store.decrypt(blob, khoa).decode("utf-8"))
    if not isinstance(p, dict) or p.get("schema") != 1 or type(p.get("rev")) is not int:
        raise ValueError("schema")
    return p
def _lam_ghi_nguoc(neu_doi, khoa, het, huy):
    """Trả (TRẠNG THÁI, chi tiết) hoặc None (im lặng). Không in gì — luồng chính in đúng MỘT dòng."""
    con = lambda: max(0.5, het - time.monotonic())   # noqa: E731 — hạn còn lại cho từng lời gọi mạng
    try:
        if str(GOC / "scripts") not in sys.path:
            sys.path.insert(0, str(GOC / "scripts"))
        import gas, gws_cred_store as store, tl_gws  # noqa: E401 — dùng NGUYÊN tên của tl_gws qua thuộc tính (A12)
    except Exception as e:  # noqa: BLE001
        return "KHÔNG ĐO ĐƯỢC", f"không import được scripts/ ({type(e).__name__})"
    if len(khoa) < tl_gws._MASTER_KEY_MIN_LEN or len(set(khoa)) < tl_gws._MASTER_KEY_MIN_DISTINCT:
        return "BỎ QUA", f"TL_MASTER_KEY yếu (cần ≥{tl_gws._MASTER_KEY_MIN_LEN} ký tự VÀ ≥{tl_gws._MASTER_KEY_MIN_DISTINCT} ký tự khác nhau)"
    dia = _doc_json(_codex_dir() / "auth.json")
    if not isinstance(dia, dict) or not isinstance(dia.get("tokens"), dict):
        return "KHÔNG ĐO ĐƯỢC", "auth.json không hợp lệ"
    k_dia = tl_gws._last_refresh_key(dia)
    if neu_doi and isinstance(dau := _doc_json(_codex_dir() / TEN_DAU), dict) and k_dia <= tl_gws._last_refresh_key(dau):
        return None
    try:
        r = gas.get("ping", timeout=con())
    except Exception:  # noqa: BLE001 — thiếu TL_WEBAPP/TL_TOKEN cũng là "ping lỗi"
        r = None
    v = r.get("version") if isinstance(r, dict) and r.get("ok") is True else None
    if (b := ban_webapp(v)) is None or b < BAN_TOI_THIEU:
        # review lượt 1 P3: chuỗi từ server có thể mang xuống dòng/ký tự điều khiển ⇒ chỉ giữ ký tự an toàn (một dòng)
        return "KHÔNG HỖ TRỢ", f"webapp {re.sub(r'[^0-9A-Za-z._+-]', '?', v[:40]) if isinstance(v, str) else 'không đo được'}"
    fid = tl_gws.AGENT_CREDS_FILEID
    for _ in range(LAN_CAS):
        if (blob := tl_gws._public_curl_bytes(fid, timeout=con())) is None:
            return "KHÔNG ĐO ĐƯỢC", "tải công khai tl_agent_creds.enc lỗi"
        md5 = hashlib.md5(blob).hexdigest()
        try:
            cu = _giai(store, khoa, blob)
        except Exception:  # noqa: BLE001
            return "KHÔNG ĐO ĐƯỢC", "bundle không giải mã/đúng định dạng"
        ca = cu.get("codex_auth") if isinstance(cu.get("codex_auth"), dict) else {}
        if tl_gws._last_refresh_key(ca) >= k_dia:
            huy.is_set() or _ghi_dau(ca.get("last_refresh"), md5)
            return "ĐÃ CŨ", f"bỏ ghi (bundle rev={cu['rev']} mới hơn hoặc bằng đĩa)"
        moi = {**{k: cu[k] for k in tl_gws._AGENT_CREDS_KEYS if k in cu}, "codex_auth": dia, "schema": 1, "rev": cu["rev"] + 1,
               "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        gui = store.encrypt(json.dumps(moi, ensure_ascii=False).encode("utf-8"), khoa)
        if huy.is_set():
            return None
        r = gas.post("agent_creds_put", timeout=con(), fileId=fid, expect_md5=md5, b64=base64.b64encode(gui).decode("ascii"))
        if isinstance(r, dict) and r.get("ok") is True:
            break
        if (ma := _ma_loi(r)) not in ("CAS_CONFLICT", "LOCK_BUSY"):
            return "KHÔNG ĐO ĐƯỢC", f"webapp {ma}"
    else:
        return "KHÔNG ĐO ĐƯỢC", "xung đột CAS lặp"
    try:   # readback (Q16): md5 server == md5 blob gửi; tải lại công khai: rev và last_refresh khớp
        lai = _giai(store, khoa, tl_gws._public_curl_bytes(fid, timeout=con()) or b"")
        dung = (r.get("md5") == hashlib.md5(gui).hexdigest() and lai["rev"] == moi["rev"] and isinstance(lai.get("codex_auth"), dict)
                and lai["codex_auth"].get("last_refresh") == dia.get("last_refresh"))
    except Exception:  # noqa: BLE001
        dung = False
    if not dung:
        return "KHÔNG ĐO ĐƯỢC", "readback lệch"
    huy.is_set() or _ghi_dau(dia.get("last_refresh"), r["md5"])
    return "ĐÃ GHI", f"rev={moi['rev']}"
def ghi_nguoc(neu_doi=False, env=os.environ, han=HAN_GHI_NGUOC):
    """Mục tiêu 2: đúng MỘT dòng `agent_creds_ghi_nguoc: …` (trừ ca im lặng của --neu-doi); luôn rc 0; không ghi auth.json."""
    khoa, kq = env.get("TL_MASTER_KEY") or "", {}
    if env.get("CLAUDE_CODE_REMOTE") != "true":
        kq["v"] = ("BỎ QUA", "không phải phiên cloud")
    elif not khoa:
        kq["v"] = ("BỎ QUA", "thiếu TL_MASTER_KEY")
    else:
        huy, het = threading.Event(), time.monotonic() + han
        def chay():
            try:
                kq["v"] = _lam_ghi_nguoc(neu_doi, khoa, het, huy)
            except Exception as e:  # noqa: BLE001 — chỉ TÊN lớp lỗi, không bao giờ thông điệp (có thể mang dữ liệu)
                kq["v"] = ("KHÔNG ĐO ĐƯỢC", f"lỗi {type(e).__name__}")
        (t := threading.Thread(target=chay, daemon=True)).start()
        t.join(han)
        if t.is_alive():
            huy.set()
            kq["v"] = ("KHÔNG ĐO ĐƯỢC", f"quá {han:g} s")
    if kq.get("v") is not None:
        s, ct = kq["v"]
        print(f"agent_creds_ghi_nguoc: {s} — {ct.replace(khoa, '***') if khoa else ct}")
    return 0
def main(argv):
    [s.reconfigure(encoding="utf-8", errors="backslashreplace") for s in (sys.stdout, sys.stderr)]
    if argv in (["nap"], ["cai-agy"]):
        return {"nap": nap, "cai-agy": cai_agy}[argv[0]]()
    if argv == ["ghim-agy"] or (len(argv) == 3 and argv[:2] == ["ghim-agy", "--ban"] and re.fullmatch(r"\d+\.\d+\.\d+", argv[2])):
        return ghim_agy(argv[2] if len(argv) == 3 else None)
    if argv in (["ghi-nguoc"], ["ghi-nguoc", "--neu-doi"]):
        return ghi_nguoc(neu_doi=len(argv) == 2)
    return print("dùng: cloud_agent_creds.py nap | cai-agy | ghim-agy [--ban X.Y.Z] | ghi-nguoc [--neu-doi]", file=sys.stderr) or 2
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
