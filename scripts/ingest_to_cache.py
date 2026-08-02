#!/usr/bin/env python3
"""ingest_to_cache.py — Cổng nạp toàn văn VBQPPL vào cache theo THỨ TỰ ƯU TIÊN.

Mục tiêu: một đường vào duy nhất, chọn phương án hiệu quả + verbatim nhất hiện có,
parse đúng (docx/text/markdown/pdf/html), KHÓA số hiệu canonical, gắn method +
evidence_status=verified + nlm_source_id, rồi cache.

THỨ TỰ ƯU TIÊN NẠP (ingest priority) — VERIFIED 2026-06-09 (134/2025/QH15: 35 Điều):

  0. CACHE đã có (phiên này)                         -> dùng luôn, 0 chi phí.
  1. DRIVE (Google Doc native), theo độ sạch verbatim & tính sẵn sàng:
       a. Apps Script  exportdocx  -> .docx -> python-docx   (✅ PASS rank 95 — ƯU TIÊN NHẤT)
       b. MCP download_file_content (export DOCX) -> .docx   (✅ PASS rank 94 — FALLBACK 1a fail)
       c. Apps Script  exporttext  -> text/plain             (✅ PASS rank 80 — FALLBACK)
       d. MCP read_file_content     -> markdown              (✅ PASS rank 60 — FALLBACK cuối, fix v1.9.9.10)
  2. URL do source policy của môi trường cho phép — định dạng hiệu quả nhất TRƯỚC:
       a. .docx  -> python-docx          (cấu trúc rõ nhất)
       b. .doc   -> convert -> python-docx
       c. .pdf   -> pdfplumber/pypdf
       d. .html  -> bóc nội dung chính    (kém tin cậy nhất, chỉ khi không có file)
  3. NLM (notebook_query) — CHỈ để ĐỊNH VỊ Điều/Khoản, KHÔNG phải trích dẫn chính thức.

Phương án chạy được hoàn toàn trong bash (Claude tự động hoá): 1a, 1c, 2*.
Phương án MCP (1b, 1d) do Claude gọi tool rồi truyền file qua --input (--method tương ứng).

Cách dùng tiêu biểu:
  # 1a — Drive exportdocx (ưu tiên cao nhất khi Apps Script sẵn sàng)
  ingest_to_cache.py --so-hieu 18/VBHN-VPQH --gdoc-id <ID> --nlm-source-id <UUID> \
      --method exportdocx --webapp "$WEBAPP" --token "$TOKEN"
  # 1b/1d/file — đã có file (vd MCP tải về) thì truyền thẳng
  ingest_to_cache.py --so-hieu 18/VBHN-VPQH --input /tmp/x.docx --method download_file_content
  # 2 — URL công khai
  ingest_to_cache.py --so-hieu 79/2025/NĐ-CP --url "https://vbpl.vn/.../vanban.docx" --method url
"""
import argparse, atexit, contextlib, hashlib, json, os, platform, re, shutil, subprocess, sys, tempfile, time, unicodedata, urllib.request, urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_CACHE = os.path.expanduser("~/.tra_luat_cache")
DEFAULT_MAX_DOWNLOAD_BYTES = 35 * 1024 * 1024
_OWNED_TEMP_PATHS: list[str] = []


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name) or default)
    except (TypeError, ValueError):
        return int(default)


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        # v1.34.45 (audit merge): on Windows os.kill(pid, 0) routes to CTRL_C_EVENT — it is
        # NOT a liveness probe (a dead pid is reported alive, and a console-group leader would
        # receive a real Ctrl+C). Probe via OpenProcess; stay conservatively "alive" on any
        # uncertainty so a genuinely-held lock is never broken out from under a live writer.
        return _pid_alive_windows(pid)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except (PermissionError, OSError):
        return True


def _pid_alive_windows(pid: int) -> bool:
    try:
        import ctypes
        from ctypes import wintypes
    except Exception:  # noqa: BLE001
        return True
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    STILL_ACTIVE = 259
    ERROR_INVALID_PARAMETER = 87
    try:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    except Exception:  # noqa: BLE001
        return True
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
    if not handle:
        # Only a definitive "no such process" (ERROR_INVALID_PARAMETER) proves it is dead;
        # any other error (e.g. access denied) means the process exists → treat as alive.
        return ctypes.get_last_error() != ERROR_INVALID_PARAMETER
    try:
        code = wintypes.DWORD()
        if not kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
            return True
        return code.value == STILL_ACTIVE
    finally:
        kernel32.CloseHandle(handle)


def _break_abandoned_lock(path: Path, *, stale_s: float) -> bool:
    """Remove only the same observed lock when its owner is gone or it is stale."""
    try:
        before = path.stat()
        payload = json.loads(path.read_text(encoding="utf-8") or "{}")
    except FileNotFoundError:
        return True
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        payload = {}
        try:
            before = path.stat()
        except FileNotFoundError:
            return True
    same_host = str(payload.get("host") or "") == platform.node()
    try:
        owner_pid = int(payload.get("pid") or 0)
    except (TypeError, ValueError):
        owner_pid = 0
    owner_gone = same_host and not _pid_alive(owner_pid)
    stale = (time.time() - before.st_mtime) > max(1.0, float(stale_s))
    if not (owner_gone or stale):
        return False
    try:
        after = path.stat()
        if (after.st_ino, after.st_mtime_ns, after.st_size) != (before.st_ino, before.st_mtime_ns, before.st_size):
            return False
        path.unlink()
        return True
    except FileNotFoundError:
        return True


@contextlib.contextmanager
def _cache_lock(cache_dir: str, so_hieu: str, variant: str, *, timeout_s: float | None = None):
    """Serialize writers for one cache identity without a global bottleneck."""
    from cache import cache_dir as _resolved_cache_dir  # type: ignore
    root = Path(_resolved_cache_dir(cache_dir))
    lock_dir = root / ".ingest-locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    identity = unicodedata.normalize("NFC", f"{so_hieu.strip().casefold()}\0{variant.strip().casefold()}")
    token = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    lock_path = lock_dir / f"{token}.lock"
    if timeout_s is None:
        try:
            timeout_s = float(os.environ.get("TL_CACHE_LOCK_TIMEOUT_S") or 10.0)
        except (TypeError, ValueError):
            timeout_s = 10.0
    try:
        stale_s = float(os.environ.get("TL_CACHE_LOCK_STALE_S") or 3600.0)
    except (TypeError, ValueError):
        stale_s = 3600.0
    deadline = time.monotonic() + max(0.0, float(timeout_s))
    fd = None
    while fd is None:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            lock_record = {"host": platform.node(), "pid": os.getpid(), "started_epoch": int(time.time())}
            os.write(fd, json.dumps(lock_record, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        except FileExistsError:
            if _break_abandoned_lock(lock_path, stale_s=stale_s):
                continue
            if time.monotonic() >= deadline:
                raise RuntimeError(f"CACHE_WRITE_LOCK_TIMEOUT:{lock_path.name}")
            time.sleep(0.05)
    try:
        yield
    finally:
        os.close(fd)
        try:
            os.unlink(lock_path)
        except FileNotFoundError:
            pass


def _owned_temp_path(suffix: str = "") -> str:
    fd, path = tempfile.mkstemp(prefix="tra_luat_ingest_", suffix=suffix)
    os.close(fd)
    _OWNED_TEMP_PATHS.append(path)
    return path


def _cleanup_owned_temps() -> None:
    for path in list(_OWNED_TEMP_PATHS):
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass


atexit.register(_cleanup_owned_temps)

# Thứ hạng độ tin cậy verbatim của từng method (cao = sạch hơn) — chỉ để ghi vào metadata.
# v1.9.9.10: Verified bằng test 134/2025/QH15 (35 Điều + 8 Chương):
#  - exportdocx (1a): ✅ PASS (rank 95) — ưu tiên cao nhất, sạch nhất
#  - download_file_content (1b): ✅ PASS (rank 94) — fallback nếu 1a fail, không cần Apps Script
#  - exporttext (1c): ✅ PASS (rank 80) — fallback, nhanh hơn 1a
#  - read_file_content (1d): ✅ PASS after fix (rank 60) — fallback cuối, cần strip markdown
# v1.9.9.11: PDF (CÓ lớp text máy đọc) xếp TRÊN .doc theo cấu hình người dùng.
#   Lý do: .pdf official thường là bản gốc đáng tin, giữ phụ lục/bảng nguyên khối;
#   chỉ XẾP SAU .docx (cấu trúc đoạn rõ nhất). PDF SCAN (không text layer) bị CHẶN
#   ở fetch_url (raise ScannedPDFError) -> KHÔNG bao giờ nạp, chuyển nguồn web khác.
METHOD_RANK = {
    "exportdocx": 95, "download_file_content": 94,
    "exporttext": 80, "read_file_content": 60,
    "url_docx": 90, "url_pdf": 80, "url_doc": 75, "url_html": 40,
    "file": 50, "url": 50,
}


class ScannedPDFError(RuntimeError):
    """PDF không có lớp text máy đọc (bản scan/ảnh). KHÔNG nạp — phải đổi nguồn web khác."""


class PdfProbeUnavailableError(RuntimeError):
    """KHÔNG ĐO ĐƯỢC lớp text (thiếu cả pdfplumber lẫn pypdf) — CHƯA biết gì về tài liệu.

    ★KHÔNG kế thừa ScannedPDFError: hai chuyện khác hẳn nhau và phải ra hai lối xử lý khác nhau
    (sửa MÁY vs đổi NGUỒN). Gộp họ là tái lập đúng cái lỗi mà r314 đi chữa."""


def _pdf_chars_pdfplumber(path: str, max_pages: int):
    """Trả số ký tự đo được, hoặc None nếu KHÔNG đo được bằng đường này."""
    try:
        import pdfplumber  # type: ignore
    except Exception:  # noqa: BLE001 — thiếu thư viện: câu trả lời là "không biết", không phải 0
        return None
    try:
        with pdfplumber.open(path) as pdf:
            return sum(len((pg.extract_text() or "").strip()) for pg in pdf.pages[:max_pages])
    except Exception:  # noqa: BLE001 — có thư viện mà đọc hỏng cũng là "không đo được"
        return None


def _pdf_chars_pypdf(path: str, max_pages: int):
    """Trả số ký tự đo được, hoặc None nếu KHÔNG đo được bằng đường này."""
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:  # noqa: BLE001
        return None
    try:
        r = PdfReader(path)
        return sum(len((pg.extract_text() or "").strip()) for pg in r.pages[:max_pages])
    except Exception:  # noqa: BLE001
        return None


def pdf_text_layer_chars(path: str, max_pages: int = 5):
    """Đếm ký tự text trích được từ <= max_pages trang đầu.

    Trả **None** khi KHÔNG đo được (thiếu/hỏng cả hai đường dò) — KHÁC HẲN 0 = đo được và RỖNG.

    r314 (v1.36.47): trước đây thiếu cả hai thư viện cũng `return 0`, mà 0 nghĩa là «PDF scan»
    ⇒ khuyết tật của MÁY bị báo thành thuộc tính của TÀI LIỆU, kèm lời khuyên đi tìm nguồn khác.
    `requirements.txt` khai «uses only Python standard library» nên CÀI SẠCH LÀ KHÔNG CÓ CÁI NÀO
    ⇒ MỌI PDF đều bị chặn oan. Đo 02-08 trên `54-2025-g7.pdf` (PDF text thật, pdftotext bóc
    167.433 ký tự, riêng trang 1 có 2.536): chưa cài pypdf ⇒ `{"reason":"scanned_pdf",…0 ký tự…}`
    · cài pypdf ⇒ `{"ok":true,"n_articles":72}`. CÙNG một tệp.
    ★Đồng thời sửa lỗi CỘNG DỒN: bản cũ nuôi CHUNG biến `total` cho cả hai đường dò, nên
     pdfplumber hỏng giữa chừng rồi pypdf chạy tiếp là cộng CHỒNG lên phần dở dang.
    """
    for _probe in (_pdf_chars_pdfplumber, _pdf_chars_pypdf):
        n = _probe(path, max_pages)
        if n is not None:
            return n
    return None


def assert_pdf_not_scanned(path: str, min_chars: int = 120) -> None:
    """Chặn PDF scan: < min_chars text trên các trang đầu => coi là scan -> raise.
    Quy tắc cứng (người dùng): PDF scan TUYỆT ĐỐI KHÔNG tải/nạp, đi tìm nguồn khác.

    r314: «không đo được» vẫn fail-CLOSED (không nạp mù), nhưng ném lỗi KHÁC + thông điệp chỉ
    đúng người phải sửa. Vẫn chặn, nhưng không còn vu cho tài liệu."""
    n = pdf_text_layer_chars(path)
    if n is None:
        raise PdfProbeUnavailableError(
            "KHÔNG ĐO ĐƯỢC lớp text của PDF: thiếu (hoặc hỏng) cả `pdfplumber` lẫn `pypdf`. "
            "ĐÂY LÀ KHUYẾT CỦA MÁY, KHÔNG phải kết luận về tài liệu — ĐỪNG đi tìm nguồn khác. "
            "Cài rồi chạy lại CÙNG lệnh: pip install pypdf")
    if n < min_chars:
        raise ScannedPDFError(
            f"PDF có vẻ là bản SCAN (chỉ {n} ký tự text ở trang đầu). "
            f"KHÔNG nạp theo quy tắc cứng — hãy chuyển sang nguồn web TEXT khác "
            f"(thuvienphapluat .docx > .pdf-text khác > luatvietnam > vbpl/Công báo...).")


def _host_allowed(host: str, patterns) -> bool:
    """Match an optional environment-owned host policy (exact or ``*.suffix``)."""
    host = str(host or "").strip().rstrip(".").casefold()
    if not host:
        return False
    rules = [str(x or "").strip().rstrip(".").casefold() for x in (patterns or []) if str(x or "").strip()]
    if not rules:
        return True
    for rule in rules:
        if rule.startswith("*."):
            suffix = rule[2:]
            if host.endswith("." + suffix):
                return True
        elif host == rule:
            return True
    return False


def _url_host_public_ok(host: str) -> tuple[bool, str]:
    """Blunt SSRF: reject hosts that resolve to a non-global address (loopback, RFC1918,
    link-local incl. 169.254.169.254 cloud metadata, reserved, multicast, unspecified).
    Opt out for trusted internal use with TL_SOURCE_ALLOW_PRIVATE=1."""
    if str(os.environ.get("TL_SOURCE_ALLOW_PRIVATE") or "").strip().lower() in {"1", "true", "yes", "on"}:
        return True, ""
    import ipaddress
    import socket
    h = str(host or "").strip().rstrip(".")
    if not h:
        return False, "EMPTY_HOST"
    addrs = set()
    try:
        addrs.add(ipaddress.ip_address(h))
    except ValueError:
        try:
            for info in socket.getaddrinfo(h, None):
                raw = str(info[4][0]).split("%", 1)[0]
                try:
                    addrs.add(ipaddress.ip_address(raw))
                except ValueError:
                    continue
        except socket.gaierror as exc:
            return False, f"DNS_RESOLUTION_FAILED:{exc}"
    if not addrs:
        return False, "NO_ADDRESS"
    for ip in addrs:
        if not ip.is_global:
            return False, f"BLOCKED_NON_PUBLIC_ADDRESS:{ip}"
    return True, ""


def _stream_get(url: str, out_path: str, *, timeout: int = 180, max_bytes: int = DEFAULT_MAX_DOWNLOAD_BYTES,
                max_redirects: int = 5, allowed_schemes=("https",), allowed_hosts=(),
                block_private: bool = False) -> tuple[bool, str, str]:
    """Environment-policy-aware streaming GET with bounded resources.

    ``block_private`` adds an address-level egress filter (SSRF guard) — set by the
    arbitrary-URL document fetch path, left off for the trusted config webapp path."""
    allowed = {str(s).lower() for s in allowed_schemes}
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme.lower() not in allowed or parsed.scheme.lower() == "file":
        return False, "", f"SOURCE_SCHEME_NOT_ALLOWED:{parsed.scheme or '<empty>'}"
    if parsed.username or parsed.password:
        return False, "", "CREDENTIALS_IN_URL_NOT_ALLOWED"
    if not _host_allowed(parsed.hostname or "", allowed_hosts):
        return False, "", f"SOURCE_HOST_NOT_ALLOWED:{parsed.hostname or '<empty>'}"
    if block_private:
        _ok_pub, _why = _url_host_public_ok(parsed.hostname or "")
        if not _ok_pub:
            return False, "", f"SOURCE_HOST_BLOCKED:{_why}"

    class _Redirects(urllib.request.HTTPRedirectHandler):
        def __init__(self):
            self.count = 0

        def redirect_request(self, req, fp, code, msg, headers, newurl):
            self.count += 1
            if self.count > int(max_redirects):
                raise RuntimeError("TOO_MANY_REDIRECTS")
            redirected = urllib.parse.urlsplit(newurl)
            if redirected.scheme.lower() not in allowed:
                raise RuntimeError("REDIRECT_SCHEME_NOT_ALLOWED")
            if not _host_allowed(redirected.hostname or "", allowed_hosts):
                raise RuntimeError("REDIRECT_HOST_NOT_ALLOWED")
            if block_private:
                _rok, _rwhy = _url_host_public_ok(redirected.hostname or "")
                if not _rok:
                    raise RuntimeError(f"REDIRECT_HOST_BLOCKED:{_rwhy}")
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    try:
        opener = urllib.request.build_opener(_Redirects())
        req = urllib.request.Request(url, headers={"User-Agent": "tra-luat-cache-ingest/1"})
        total = 0
        with opener.open(req, timeout=timeout) as response, open(out_path, "wb") as dst:
            final_url = urllib.parse.urlsplit(response.geturl())
            final_scheme = final_url.scheme.lower()
            if final_scheme not in allowed:
                raise RuntimeError("FINAL_URL_SCHEME_NOT_ALLOWED")
            if not _host_allowed(final_url.hostname or "", allowed_hosts):
                raise RuntimeError("FINAL_URL_HOST_NOT_ALLOWED")
            if block_private:
                _fok, _fwhy = _url_host_public_ok(final_url.hostname or "")
                if not _fok:
                    raise RuntimeError(f"FINAL_URL_HOST_BLOCKED:{_fwhy}")
            ct = str(response.headers.get("Content-Type") or "")
            declared = response.headers.get("Content-Length")
            if declared:
                try:
                    if int(declared) > int(max_bytes):
                        raise RuntimeError(f"DOWNLOAD_LIMIT_EXCEEDED:{declared}>{max_bytes}")
                except ValueError:
                    pass
            while True:
                chunk = response.read(min(1024 * 1024, int(max_bytes) - total + 1))
                if not chunk:
                    break
                total += len(chunk)
                if total > int(max_bytes):
                    raise RuntimeError(f"DOWNLOAD_LIMIT_EXCEEDED:{total}>{max_bytes}")
                dst.write(chunk)
        if total <= 0:
            raise RuntimeError("DOWNLOAD_EMPTY")
        return True, ct, ""
    except Exception as e:
        try:
            os.unlink(out_path)
        except FileNotFoundError:
            pass
        return False, "", str(e)


def _appsscript(webapp: str, token: str, action: str, **params) -> dict:
    q = {"token": token, "action": action, **params}
    url = webapp + "?" + urllib.parse.urlencode(q)
    tmp = _owned_temp_path(".json")
    ok, _ct, err = _stream_get(url, tmp, allowed_schemes=("https",), max_bytes=10 * 1024 * 1024)
    if not ok:
        raise RuntimeError(f"Apps Script {action} lỗi: {err}")
    with open(tmp, encoding="utf-8") as fh:
        data = json.load(fh)
    if not data.get("ok", False):
        raise RuntimeError(f"Apps Script {action} trả lỗi: {data.get('error')}")
    return data


def fetch_drive_exportdocx(gdoc_id: str, webapp: str, token: str) -> str:
    """1a. Apps Script exportdocx -> .docx (base64) -> file tạm. Trả path .docx."""
    import base64
    data = _appsscript(webapp, token, "exportdocx", fileId=gdoc_id)
    b64 = data.get("b64") or data.get("base64") or ""
    raw = base64.b64decode(b64)
    out = _owned_temp_path(".docx")
    with open(out, "wb") as fh:
        fh.write(raw)
    return out


def fetch_drive_exporttext(gdoc_id: str, webapp: str, token: str) -> str:
    """1c. Apps Script exporttext -> text -> file .txt. Trả path."""
    data = _appsscript(webapp, token, "exporttext", fileId=gdoc_id)
    txt = data.get("text", "")
    out = _owned_temp_path(".txt")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(txt)
    return out


def fetch_drive_convert_docx(file_id: str, webapp: str, token: str) -> str:
    """v1.12.9: file .docx/.doc/.pdf NHỊ PHÂN trên Drive (KHÔNG Google-native) →
    copy_convert sang Google Doc tạm rồi exportdocx. Trả path .docx."""
    raise RuntimeError("CACHE_ONLY_NO_DRIVE_CONVERSION: convert through the confirmed ingest engine, then pass --input")


def fetch_url(url: str, *, source_policy: str = "public-https", max_bytes: int = DEFAULT_MAX_DOWNLOAD_BYTES,
              max_redirects: int = 5, timeout: int = 180) -> tuple[str, str]:
    """Fetch through a policy selected by the host environment.

    No host allowlist is embedded in the skill. ``TL_SOURCE_ALLOW_HOSTS`` is an
    optional comma-separated policy (exact host or ``*.suffix``); empty means
    that the embedding environment has not imposed a host restriction.
    """
    if source_policy == "environment":
        # v1.34.45 (audit merge): default https-ONLY. Plaintext http is a footgun for byte-exact
        # legal text (on-path tampering recorded as verified) — it must be opted into explicitly
        # via TL_SOURCE_SCHEMES, not enabled as a side effect of selecting the environment policy.
        requested = [s.strip().lower() for s in os.environ.get("TL_SOURCE_SCHEMES", "https").split(",")]
        schemes = tuple(s for s in requested if s in {"https", "http"})
    else:
        schemes = ("https",)
    if not schemes:
        raise RuntimeError("SOURCE_POLICY_GRANTED_NO_NETWORK_SCHEMES")
    allowed_hosts = tuple(x.strip() for x in os.environ.get("TL_SOURCE_ALLOW_HOSTS", "").split(",") if x.strip())
    tmp = _owned_temp_path()
    ok, ct, err = _stream_get(url, tmp, max_bytes=max_bytes, max_redirects=max_redirects,
                              timeout=max(1, int(timeout)), allowed_schemes=schemes,
                              allowed_hosts=allowed_hosts, block_private=True)
    if not ok:
        raise RuntimeError(f"Tải URL lỗi: {err}")
    ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
    ctl = ct.lower()
    with open(tmp, "rb") as fh:
        magic = fh.read(16)
    if ext == ".docx" or "wordprocessingml" in ctl or magic.startswith(b"PK\x03\x04"):
        dst, m = tmp + ".docx", "url_docx"
    elif ext == ".doc" or "msword" in ctl or magic.startswith(bytes.fromhex("D0CF11E0A1B11AE1")):
        dst, m = tmp + ".doc", "url_doc"
    elif ext == ".pdf" or "pdf" in ctl or magic.startswith(b"%PDF-"):
        dst, m = tmp + ".pdf", "url_pdf"
    else:
        dst, m = tmp + ".html", "url_html"
    final_path = _owned_temp_path(Path(dst).suffix)
    os.replace(tmp, final_path)
    dst = final_path
    if m in {"url_docx", "url_doc", "url_pdf"}:
        from tl_core.ingest_contract import validate_source_file
        checked = validate_source_file(dst, allowed_exts={Path(dst).suffix.lower()}, direct_upload=False)
        if not checked.get("ok"):
            raise RuntimeError(f"URL_CONTENT_VALIDATION_FAILED:{checked}")
    if m == "url_pdf":
        assert_pdf_not_scanned(dst)   # PDF scan -> raise ScannedPDFError, đổi nguồn
    return dst, m


def suy_doan_phu_luc(so_hieu: str) -> tuple:
    """r297 (P16-F10) — suy đoán «tệp này CHỈ là phụ lục» CHỈ TỪ SỐ HIỆU, theo TOKEN có ranh giới.
    Trả `(bat, ly_do)`; `ly_do` rỗng khi không suy đoán.

    Bản cũ: `_ap_hint = (so_hieu + " " + title).lower()` rồi `any(k in _ap_hint ...)` với
    `("phu_luc","phu luc","phuluc","phụ lục","-pl","_pl")`. HAI khuyết, cộng lại thành mất dữ liệu:
      (a) quét CẢ TIÊU ĐỀ — Luật/Nghị định CÓ phụ lục thường ghi thẳng «… và Phụ lục …» trên tiêu đề,
          nên chính TOÀN VĂN bị đóng dấu là phụ lục;
      (b) `-pl`/`_pl` khớp KHỚP-CON, trúng bất kỳ chỗ nào có hai chữ đó liền nhau.
    Hậu quả ở `normalize_document`: `body=""` (bỏ phân tích thân), `khoi_dau=""` — mà r215 nói rõ khối
    đầu là NGUỒN DUY NHẤT chứng minh danh tính — T1 bị đặt `ok:true` vô điều kiện, `coverage` thành
    `appendix_only`, `document_variant` đổi ⇒ ĐỔI LUÔN doc_key. Toàn bộ diễn ra IM LẶNG với `ok:true` rc=0.

    Nay: chỉ `so_hieu`; tách token ở mọi ký tự không phải chữ/số (nên `_`/`-` là ranh giới); khớp token
    NGUYÊN VẸN `pl`/`pl<số>`/`phuluc`, hoặc cặp token liền kề `phu|phụ` + `luc|lục`.
    """
    s = unicodedata.normalize("NFC", str(so_hieu or "")).lower()
    toks = [t for t in re.split(r"[^0-9a-zà-ỹ]+", s) if t]
    for i, t in enumerate(toks):
        if re.fullmatch(r"pl\d*", t) or t == "phuluc":
            return True, f"token số hiệu {t!r} = phụ lục"
        if t in ("phu", "phụ") and i + 1 < len(toks) and toks[i + 1] in ("luc", "lục"):
            return True, "cụm 'phụ lục' trong số hiệu"
    return False, ""


def run_normalize(input_path: str, so_hieu: str, title: str, variant: str,
                  cache_dir: str, extra: dict) -> dict:
    """Gọi normalize_document.py (đã vá: VBHN, markdown, full_text) với số hiệu KHÓA."""
    out_json = _owned_temp_path(".json")
    cmd = [sys.executable, str(HERE / "normalize_document.py"),
           "--input", input_path, "--out", out_json,
           "--structure-level", "article",          # article = giữ nguyên văn từng Điều
           "--document-variant", variant,
           "--origin", extra.get("origin", "drive"),
           "--source-type", extra.get("source_type", "google_drive"),
           "--cache", "--cache-dir", cache_dir]
    if so_hieu:
        cmd += ["--number-symbol", so_hieu]
    if title:
        cmd += ["--title", title]
    if extra.get("source_url"):
        cmd += ["--source-url", extra["source_url"]]
    if extra.get("issuing_agency"):
        cmd += ["--issuing-agency", extra["issuing_agency"]]
    if extra.get("effective_status"):
        cmd += ["--effective-status", extra["effective_status"]]
    if extra.get("officialness"):
        cmd += ["--officialness-level", extra["officialness"]]
    if extra.get("goc"):
        cmd += ["--goc", extra["goc"]]
    if extra.get("aliases"):
        cmd += ["--aliases", extra["aliases"]]
    if extra.get("as_appendix"):
        cmd += ["--as-appendix"]
    if extra.get("as_appendix_auto"):        # r297: báo cho con biết đây là SUY ĐOÁN ⇒ nội dung được quyền phủ quyết
        cmd += ["--as-appendix-auto"]
    if extra.get("loc_congbao"):        # r217: chuyển thẳng cho normalize_document (đường nạp DUY NHẤT)
        cmd += ["--loc-congbao"]
    if extra.get("loc_congbao_audit"):
        cmd += ["--loc-congbao-audit", extra["loc_congbao_audit"]]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    sys.stderr.write(p.stderr)
    if p.returncode != 0:
        raise RuntimeError(f"normalize_document lỗi: {p.stdout}\n{p.stderr}")
    with open(out_json, encoding="utf-8") as fh:
        return json.load(fh)


def patch_cache_metadata(cache_dir: str, doc_key: str, so_hieu: str, method: str,
                         nlm_source_id: str, gdoc_id: str, source_url: str,
                         *, source_sha256: str, source_policy: str, source_provider: str):
    """Patch the exact cache record emitted by normalize and verify identity/quality."""
    from cache import cache_dir as _cd  # type: ignore
    cd = _cd(cache_dir)
    if not doc_key or any(x in doc_key for x in ("/", "\\", "..")):
        raise RuntimeError(f"CACHE_DOC_KEY_INVALID:{doc_key!r}")
    key = so_hieu.replace("/", "-").lower()
    target = Path(cd) / "docs" / f"{doc_key}.json"
    if not target.is_file():
        raise RuntimeError(f"CACHE_IDENTITY_NOT_FOUND:{doc_key}")
    with open(target, encoding="utf-8") as fh:
        d = json.load(fh)
    if d.get("doc_key") != doc_key:
        raise RuntimeError(f"CACHE_IDENTITY_MISMATCH:{doc_key}:{d.get('doc_key')}")
    src = d.get("source", {}) or {}
    src.update({"method": method, "method_rank": METHOD_RANK.get(method, 50),
                "sha256": source_sha256, "policy": source_policy, "provider": source_provider})
    if gdoc_id:
        src["gdoc_id"] = gdoc_id
    if source_url:
        src["url"] = source_url
    d["source"] = src
    number_now = str(d.get("number_symbol") or d.get("so_hieu") or "").replace("/", "-").lower()
    content_present = bool(d.get("full_text") or d.get("articles") or d.get("phu_luc"))
    method_verbatim = METHOD_RANK.get(method, 0) >= 75 and method not in {"url_html", "read_file_content"}
    quality_checks = {"identity_exact": d.get("doc_key") == doc_key,
                      "number_matches": number_now == key, "content_present": content_present,
                      "provenance_hash": bool(source_sha256), "method_verbatim": method_verbatim}
    d["evidence_status"] = "verified" if all(quality_checks.values()) else "staged"
    d["quality_checks"] = quality_checks
    if nlm_source_id:
        d["nlm_source_id"] = nlm_source_id
    if so_hieu:
        d["so_hieu"] = so_hieu
    fd, tmp = tempfile.mkstemp(prefix=target.name + ".", suffix=".tmp", dir=str(target.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, target)
    except Exception:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise
    return str(target)


def main():
    ap = argparse.ArgumentParser(description="Nạp toàn văn VBQPPL vào cache theo thứ tự ưu tiên.")
    ap.add_argument("--so-hieu", required=True, help="Số hiệu canonical, vd 18/VBHN-VPQH")
    ap.add_argument("--method", default="auto",
                    choices=["auto", "exportdocx", "exporttext", "download_file_content",
                             "read_file_content", "url", "file"],
                    help="Phương án nạp. auto: thử exportdocx->exporttext (cần --gdoc-id+webapp).")
    ap.add_argument("--input", default="", help="File đã tải sẵn (docx/doc/pdf/html/txt/md).")
    ap.add_argument("--gdoc-id", default="", help="Google Doc id (cho exportdocx/exporttext).")
    ap.add_argument("--url", default="", help="URL công khai (method=url).")
    ap.add_argument("--source-policy", choices=["public-https", "environment"],
                    default=os.environ.get("TL_SOURCE_POLICY", "public-https"),
                    help="quyền host/scheme do môi trường cấp; skill không hard-code domain")
    ap.add_argument("--source-provider", default=os.environ.get("TL_SOURCE_PROVIDER", "standalone-cli"))
    ap.add_argument("--max-download-mb", type=int, default=35)
    ap.add_argument("--max-redirects", type=int, default=_env_int("TL_SOURCE_MAX_REDIRECTS", 5))
    ap.add_argument("--source-timeout-s", type=int, default=_env_int("TL_SOURCE_TIMEOUT_S", 180))
    ap.add_argument("--webapp", default="", help="Apps Script WebApp URL.")
    ap.add_argument("--token", default="", help="Apps Script token.")
    ap.add_argument("--nlm-source-id", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--variant", default="consolidated")
    ap.add_argument("--cache-dir", default=DEFAULT_CACHE)
    ap.add_argument("--issuing-agency", default="")
    ap.add_argument("--effective-status", default="in_force")
    ap.add_argument("--officialness", default="official")
    ap.add_argument("--goc", default="", help="VBHN: chuỗi số hiệu gốc+sđbs, phân tách ';' (vd 81-2021-ND-CP;104-2022-ND-CP;97-2023-ND-CP)")
    ap.add_argument("--aliases", default="", help="Số hiệu tra cứu bổ sung, ';'. Bỏ trống => tự lấy từ --goc.")
    ap.add_argument("--vbhn-first", action="store_true",
                    help="Nếu số hiệu đã bị VBHN còn hiệu lực hợp nhất (vb_status) => NẠP VBHN thay thế.")
    ap.add_argument("--as-appendix", action="store_true",
                    help="Văn bản CHỈ là phụ lục/mẫu (không có Điều nghị định): lưu nguyên khối phu_luc, không ép thành Điều.")
    ap.add_argument("--no-as-appendix", dest="no_as_appendix", action="store_true",
                    help="(r297) TẮT suy đoán phụ lục theo số hiệu. Dùng khi số hiệu có chữ 'PL' nhưng "
                         "tệp là TOÀN VĂN văn bản. Không ảnh hưởng --as-appendix gõ tường minh.")
    ap.add_argument("--loc-congbao", dest="loc_congbao", action="store_true",
                    help="(r217) Nguồn bóc từ PDF Công báo: BỎ dòng chạy đầu trang + dòng số trang + khối chữ ký "
                         "số. Không bật thì chỉ KHAI BÁO vào verify_flags (cảnh báo, KHÔNG chặn).")
    ap.add_argument("--loc-congbao-audit", dest="loc_congbao_audit", default="",
                    help="(r217) Ghi JSON audit TỪNG DÒNG bị bỏ ra file (bằng chứng đối chiếu).")
    args = ap.parse_args()
    sys.path.insert(0, str(HERE))
    # B3: tự nạp webapp/token như `tl` nếu chưa truyền — env TL_WEBAPP/TL_TOKEN, rồi config (key `webappUrl`/`token`,
    # KHÔNG phải `webapp`). Bỏ pain phải truyền tay --webapp/--token + nhầm tên key.
    if not args.webapp or not args.token:
        args.webapp = args.webapp or os.environ.get("TL_WEBAPP") or ""
        args.token = args.token or os.environ.get("TL_TOKEN") or ""
        if not args.webapp or not args.token:
            for _p in [os.environ.get("TL_CONFIG"), os.path.expanduser("~/.tra_luat_config.json"),
                       str(HERE.parent / "tra_luat_config.v2.json"), "/tmp/tra_luat_config.json"]:
                if _p and os.path.exists(_p):
                    try:
                        _c = json.load(open(_p, encoding="utf-8"))
                    except Exception:
                        continue
                    args.webapp = args.webapp or _c.get("webappUrl") or _c.get("TL_WEBAPP") or _c.get("webapp") or ""
                    args.token = args.token or _c.get("token") or _c.get("TL_TOKEN") or ""
                    if args.webapp and args.token:
                        break
    # r297 (P16-F10): tự nhận diện phụ lục — CHỈ theo SỐ HIỆU, theo TOKEN, và KHÔNG BAO GIỜ IM LẶNG.
    # Suy đoán này ĐỔI CÁCH LƯU cả văn bản (xem `suy_doan_phu_luc`), nên nó phải (1) hẹp, (2) nói ra,
    # (3) tắt được, và (4) chịu PHỦ QUYẾT của nội dung thật ở `normalize_document` (`--as-appendix-auto`).
    args.as_appendix_auto = False
    if not args.as_appendix:
        _ap_bat, _ap_ly_do = suy_doan_phu_luc(args.so_hieu)
        if _ap_bat and args.no_as_appendix:
            sys.stderr.write(f"[cache-build] ⓘ số hiệu gợi ý phụ lục ({_ap_ly_do}) nhưng có "
                             f"--no-as-appendix ⇒ nạp như văn bản THƯỜNG.\n")
        elif _ap_bat:
            args.as_appendix = True
            args.as_appendix_auto = True
            sys.stderr.write(
                f"[cache-build] ⚠ TỰ BẬT --as-appendix vì {_ap_ly_do} (số hiệu {args.so_hieu!r}).\n"
                f"[cache-build]   ⇒ lưu NGUYÊN KHỐI vào `phu_luc`: KHÔNG tách Điều, KHÔNG giữ khối đầu\n"
                f"[cache-build]   (danh tính văn bản), KHÔNG kiểm T1, và doc_key mang biến thể `appendix`.\n"
                f"[cache-build]   Nếu đây là TOÀN VĂN văn bản, chạy lại với --no-as-appendix.\n")

    # ----- VBHN-FIRST: số hiệu bị thay thế => chuyển hướng nạp VBHN hợp nhất -----
    redirect_note = None
    if args.vbhn_first and not args.webapp:
        raise RuntimeError("VBHN_FIRST_REQUIRES_STATUS_PROVIDER")
    if args.vbhn_first and args.webapp:
        try:
            vs = _appsscript(args.webapp, args.token, "vb_status", sohieu=args.so_hieu)
            live = [v for v in (vs.get("superseded_by") or [])
                    if str(v.get("hieuluc", "")).strip().lower().startswith("còn hiệu lực")
                    and v.get("drive_id")]
            live = sorted(live, key=lambda v: (str(v.get("sohieu") or ""), str(v.get("drive_id") or "")))
            if len(live) > 1:
                raise RuntimeError(f"VBHN_FIRST_AMBIGUOUS:{[(v.get('sohieu'), v.get('drive_id')) for v in live]}")
            if live:
                v = live[0]
                orig = args.so_hieu
                args.aliases = ";".join(x for x in [args.aliases, orig] if x)
                args.so_hieu = v.get("sohieu") or args.so_hieu
                args.gdoc_id = v.get("drive_id")
                args.nlm_source_id = v.get("nlm_source_id") or args.nlm_source_id
                args.effective_status = "Còn hiệu lực"
                if args.method in ("url", "file"):
                    args.method = "auto"
                args.input = ""
                redirect_note = f"VBHN-first: '{orig}' đã bị VBHN '{args.so_hieu}' (còn hiệu lực) hợp nhất ⇒ NẠP VBHN thay thế (gdoc={args.gdoc_id})."
                sys.stderr.write("[ingest] " + redirect_note + "\n")
        except Exception as e:
            raise RuntimeError(f"VBHN_FIRST_STATUS_FAILED:{type(e).__name__}:{e}") from e

    method = args.method
    input_path = args.input
    src_url = args.url
    requested_max_bytes = max(1, args.max_download_mb) * 1024 * 1024
    try:
        environment_max_bytes = int(os.environ.get("TL_SOURCE_MAX_BYTES") or requested_max_bytes)
    except (TypeError, ValueError):
        environment_max_bytes = requested_max_bytes
    source_max_bytes = min(requested_max_bytes, max(1, environment_max_bytes))

    # ----- Lấy file theo thứ tự ưu tiên -----
    if input_path:
        if method in ("auto", "url"):
            method = "file"
        if input_path.lower().endswith(".pdf"):
            assert_pdf_not_scanned(input_path)   # PDF scan -> raise, đổi nguồn
    elif method in ("auto", "exportdocx") and args.gdoc_id and args.webapp:
        try:
            input_path = fetch_drive_exportdocx(args.gdoc_id, args.webapp, args.token)
            method = "exportdocx"
        except Exception as e:
            msg = str(e).lower()
            if "native" in msg or "403" in msg:
                raise RuntimeError("CACHE_ONLY_NO_DRIVE_CONVERSION: use confirmed ingest conversion, then --input") from e
            else:
                sys.stderr.write(f"[ingest] exportdocx lỗi ({e}); thử exporttext...\n")
                input_path = fetch_drive_exporttext(args.gdoc_id, args.webapp, args.token)
                method = "exporttext"
    elif method == "exporttext" and args.gdoc_id and args.webapp:
        input_path = fetch_drive_exporttext(args.gdoc_id, args.webapp, args.token)
    elif method == "url" and src_url:
        input_path, method = fetch_url(src_url, source_policy=args.source_policy,
                                       max_bytes=source_max_bytes,
                                       max_redirects=max(0, args.max_redirects),
                                       timeout=max(1, args.source_timeout_s))
    else:
        ap.error("Thiếu nguồn: cần --input, hoặc --gdoc-id+--webapp, hoặc --url.")

    # ----- Parse + cache (normalize đã vá VBHN/markdown/full_text) -----
    # Tự suy aliases từ goc nếu không truyền tường minh (để tra số gốc/sđbs trúng VBHN).
    goc = args.goc.strip()
    aliases = args.aliases.strip()
    if goc and not aliases:
        aliases = ";".join(s.strip() for s in goc.split(";") if s.strip())
    _from_url = method.startswith("url_") or method == "url"
    _from_drive = bool(args.gdoc_id) and not _from_url
    extra = {
        "origin": "fetch_url" if _from_url else ("drive" if _from_drive else "local"),
        "source_type": "fetch_url" if _from_url else ("google_drive" if _from_drive else "file"),
        "source_url": src_url,
        "issuing_agency": args.issuing_agency,
        "effective_status": args.effective_status,
        "officialness": args.officialness,
        "goc": goc,
        "aliases": aliases,
        "as_appendix": args.as_appendix,
        "as_appendix_auto": getattr(args, "as_appendix_auto", False),    # r297
        "loc_congbao": getattr(args, "loc_congbao", False),              # r217
        "loc_congbao_audit": getattr(args, "loc_congbao_audit", ""),     # r217
    }
    if not Path(input_path).is_file():
        raise RuntimeError(f"SOURCE_NOT_FILE:{input_path}")
    from tl_core.ingest_contract import sha256_file, validate_source_file
    source_check = validate_source_file(
        input_path, allowed_exts={".docx", ".doc", ".pdf", ".html", ".htm", ".txt", ".md"},
        direct_upload=True, max_upload_bytes=source_max_bytes)
    if not source_check.get("ok"):
        raise RuntimeError(f"SOURCE_VALIDATION_FAILED:{json.dumps(source_check, ensure_ascii=False, sort_keys=True)}")
    source_sha256 = sha256_file(input_path)
    with _cache_lock(args.cache_dir, args.so_hieu, args.variant):
        normalized = run_normalize(input_path, args.so_hieu, args.title, args.variant, args.cache_dir, extra)
        doc_key = str(normalized.get("doc_key") or "")
        target = patch_cache_metadata(args.cache_dir, doc_key, args.so_hieu, method,
                                      args.nlm_source_id, args.gdoc_id, src_url,
                                      source_sha256=source_sha256, source_policy=args.source_policy,
                                      source_provider=args.source_provider)

    # r217 (đo 27-07 trên Windows locale cp1258): `open(target)` không khai encoding ⇒ đọc lại record
    # cache UTF-8 bằng codec locale và NỔ UnicodeDecodeError. Chỗ này nằm SAU khi cache đã ghi xong
    # (patch_cache_metadata ở trên), nên lệnh in `{"ok": false, "reason": "ingest_failed"}` rc=2 TRONG
    # KHI KHO ĐÃ ĐỔI — đúng lớp bẫy "rc≠0 không có nghĩa là chưa ghi gì". Toàn bộ đường `--method file`
    # (cache-build offline, không đụng Drive) chưa từng chạy nổi trên máy tiếng Việt vì dòng này.
    d = json.load(open(target, encoding="utf-8")) if target else {}
    arts = d.get("articles", {})
    n_arts = len(arts) if isinstance(arts, dict) else len(arts or [])
    print(json.dumps({
        "ok": True, "so_hieu": d.get("so_hieu") or args.so_hieu,
        "method": method, "method_rank": METHOD_RANK.get(method, 50),
        "evidence_status": d.get("evidence_status"),
        "effective_status": d.get("document_status") or d.get("effective_status"),
        "aliases": d.get("aliases", []),
        "n_articles": n_arts,
        "redirected": redirect_note,
        "nlm_source_id": d.get("nlm_source_id", ""),
        "cache_file": target,
    }, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except ScannedPDFError as e:
        print(json.dumps({"ok": False, "reason": "scanned_pdf",
                          "action": "switch_source", "message": str(e)},
                         ensure_ascii=False))
        sys.exit(5)   # exit 5 = PDF scan, đổi nguồn web khác
    # r314: PHẢI đứng TRƯỚC `except Exception`, và KHÔNG được gộp vào nhánh scanned_pdf ở trên —
    # hai lối xử lý khác nhau: đây là «sửa MÁY rồi chạy lại CÙNG lệnh», kia là «đổi NGUỒN».
    # exit 6 riêng để agent-loop/script không nuốt thành `ingest_failed` chung chung.
    except PdfProbeUnavailableError as e:
        print(json.dumps({"ok": False, "reason": "pdf_probe_unavailable",
                          "action": "install_dep", "install": "pip install pypdf",
                          "message": str(e)}, ensure_ascii=False))
        sys.exit(6)   # exit 6 = KHÔNG đo được (thiếu thư viện), KHÔNG kết luận gì về tài liệu
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "reason": "ingest_failed",
                          "error": f"{type(e).__name__}: {e}"}, ensure_ascii=False))
        sys.exit(2)
