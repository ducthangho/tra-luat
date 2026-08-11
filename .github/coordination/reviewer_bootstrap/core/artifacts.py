"""Artifact manifest + locator bền + SHA-256 từng file (acceptance §3, mục "Artifact retention").

Bất biến:
  - Mỗi lượt chạy sinh manifest có locator BỀN + SHA-256 cho TỪNG file, đủ năm hạng mục:
    source, corpus, per_case_matrix, runner_env_digest, cleanup_record.
  - Manifest tự kiểm được: nó khai chính locator của mình, và hash của nó nằm ở tệp sidecar
    RIÊNG (`manifest.sha256`). Một manifest tự chứa hash của chính nó là bài toán con gà - quả
    trứng; sidecar là cách giải đúng của mệnh đề "hoặc có hash riêng ghi ở nơi khác".
  - "Comment summary" và "bundle gửi ngoài luồng" KHÔNG phải retention. Vì vậy locator được ghi
    dạng TƯƠNG ĐỐI so với run_root và verify() nhận root truyền vào: artifact còn truy xuất được
    sau khi tiến trình sinh ra nó đã kết thúc, và cả khi thư mục bị di chuyển.
  - **Locator bị RÀNG BUỘC trong run_root.** Xem bên dưới.

verify() trả về báo cáo máy đọc được và gọi ĐÍCH DANH tên file thiếu - "gate đỏ" mà không nói
thiếu cái gì thì không dùng được để sửa.

──────────────────────────────────────────────────────────────────────────────
LOCATOR CONTAINMENT (finding wp77-g1-sec-01)
──────────────────────────────────────────────────────────────────────────────
g1 nối thẳng `relative_name` vào root và `verify()` đi theo locator không kiểm gì. Auditor dùng
locator `../escaped.txt`: file được ghi NGOÀI `run_root`, manifest ghi đúng locator đó, và
`verify(run_root)` vẫn trả `ok=true`. Một manifest như vậy chứng nhận cho một object nằm ngoài
phạm vi nó tuyên bố mô tả - tức là chữ ký đúng trên tài liệu sai.

Bản này ràng buộc ở CẢ HAI đầu - lúc ghi (`ArtifactSet.add`) và lúc kiểm (`verify`), vì hai đầu có
hai kẻ tấn công khác nhau: đầu ghi chống code gọi sai, đầu kiểm chống MANIFEST thù địch (manifest
có thể do người khác soạn, sidecar vẫn khớp, mà locator vẫn trỏ ra ngoài).

Bốn phép từ chối, mỗi phép có phản chứng hồi quy riêng:
  - đường dẫn tuyệt đối (POSIX `/x`, Windows `C:\\x`, UNC `\\\\host\\share`);
  - thành phần `..` hoặc `.`, và dấu `\\` (nghĩa của nó lệch nhau giữa hai nền);
  - kết quả resolve nằm ngoài `run_root` (kiểm bằng realpath + commonpath);
  - symlink - bất kỳ thành phần nào dưới root là symlink đều bị từ chối, và `verify()` chỉ hash
    TỆP THƯỜNG. Không có điều này thì hash "khớp" chỉ chứng nhận NỘI DUNG, không chứng nhận rằng
    thứ nằm trong run_root chính là thứ đã được hash.
"""

import hashlib
import json
import ntpath
import os
import posixpath
import re
import stat
import unicodedata

# `\Z` + fullmatch, không phải `$` + match: `$` khớp cả trước newline cuối chuỗi.
_SHA256_HEX = re.compile(r"[0-9a-f]{64}\Z")


def locator_identity(locator):
    """Khoá so sánh CANONICAL của một locator (protocol §5: NFC + case-fold).

    So chuỗi nguyên là sai trên Windows và macOS: `Source.txt` và `SOURCE.txt` là HAI locator
    khác nhau nhưng CÙNG một tệp, nên năm hạng mục có thể cùng trỏ một file mà phép kiểm trùng
    không thấy gì. Cũng chuẩn hoá Unicode, vì `é` dựng sẵn và `é` tổ hợp cho cùng tên tệp trên
    macOS mà khác chuỗi.
    """
    return unicodedata.normalize("NFC", str(locator)).casefold()


def _open_regular_for_write(path, locator):
    """Mở để GHI, từ chối symlink và mọi thứ không phải tệp thường.

    Ba lớp, vì không lớp nào một mình đủ trên mọi nền:
      islink TRƯỚC khi mở - lớp duy nhất còn tác dụng ở Windows, nơi O_NOFOLLOW không tồn tại;
      O_NOFOLLOW           - đóng khe TOCTOU trên POSIX;
      lstat vs fstat SAU khi mở - `fstat` ĐI THEO symlink tới một tệp thường, nên riêng nó không
                             phân biệt được "tệp thật" với "symlink trỏ tới tệp thật"; so danh
                             tính (st_dev, st_ino) của đường dẫn với của descriptor thì phân biệt
                             được, và bắt luôn ca bị tráo giữa hai lời gọi.
    """
    if os.path.islink(path):
        raise LocatorError(locator, "target is a symlink")
    # KHÔNG O_TRUNC ở đây. `O_TRUNC` cắt tệp NGAY LÚC MỞ, tức trước khi các phép kiểm dưới đây
    # chạy - và một lời từ chối phát ra sau khi dữ liệu đã mất thì không bảo vệ được gì. Cắt sau,
    # khi đã biết chắc mình đang giữ đúng đối tượng.
    flags = os.O_WRONLY | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o600)
    handle = os.fdopen(fd, "wb")
    try:
        opened = os.fstat(handle.fileno())
        if not stat.S_ISREG(opened.st_mode):
            raise LocatorError(locator, "target is not a regular file after open")
        on_disk = os.lstat(path)
        if not stat.S_ISREG(on_disk.st_mode):
            raise LocatorError(locator, "path is not a regular file (symlink or device)")
        if (on_disk.st_dev, on_disk.st_ino) != (opened.st_dev, opened.st_ino):
            raise LocatorError(locator, "path and opened file are different objects")
        # HARD LINK: một inode có NHIỀU tên. Ba phép kiểm trên đều xanh cho một hardlink trỏ ra
        # ngoài `run_root` - nó LÀ tệp thường, KHÔNG phải symlink, và path với descriptor đúng là
        # cùng một object. Thứ phân biệt được chỉ có số liên kết: một artifact do ta vừa tạo phải
        # có đúng một tên. Đây là đường auditor dùng để ghi đè tệp ngoài run_root qua manifest.json.
        if opened.st_nlink != 1:
            raise LocatorError(
                locator, "target has %d hard links - it is reachable from outside run_root"
                % opened.st_nlink
            )
        handle.truncate(0)
    except BaseException:
        handle.close()
        raise
    return handle


def _read_regular(path, locator):
    """Đọc một tệp PHẢI là tệp thường. Trả bytes, hoặc ném LocatorError.

    Dùng cho chính `manifest.json` và `manifest.sha256`: bản trước mở thẳng bằng `open()`, nên
    manifest CỦA CHÍNH LƯỢT CHẠY có thể là symlink trỏ ra ngoài `run_root` và cả hai đầu ghi/kiểm
    đều không thấy. Ràng buộc containment áp cho entry mà không áp cho tài liệu mô tả chúng thì
    vẫn còn nguyên một cửa.
    """
    try:
        on_disk = os.lstat(path)
    except OSError as exc:
        raise LocatorError(locator, "cannot be inspected: %s" % exc) from exc
    if stat.S_ISLNK(on_disk.st_mode):
        raise LocatorError(locator, "is a symlink")
    # Reject directories/FIFOs/devices before open: a FIFO may block forever, while hostile
    # manifest input must become a failed report rather than a traceback or a hang.
    if not stat.S_ISREG(on_disk.st_mode):
        raise LocatorError(locator, "is not a regular file")
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(fd, "rb") as handle:
            opened = os.fstat(handle.fileno())
            if not stat.S_ISREG(opened.st_mode):
                raise LocatorError(locator, "is not a regular file after open")
            if (on_disk.st_dev, on_disk.st_ino) != (opened.st_dev, opened.st_ino):
                raise LocatorError(locator, "path and opened file are different objects")
            # A hardlink is regular and path/fd identity matches, but the same inode still has a
            # second name outside run_root. The sealed documents keep the same single-link
            # containment invariant as artifacts created by this module.
            if opened.st_nlink != 1:
                raise LocatorError(
                    locator,
                    "has %d hard links - it is reachable from outside run_root"
                    % opened.st_nlink,
                )
            return handle.read()
    except LocatorError:
        raise
    except OSError as exc:
        # Directory/device/permission race đều là đầu vào thù địch. Contract của verify() là báo
        # cáo máy đọc được, không để OSError của host thoát thành traceback.
        raise LocatorError(locator, "cannot be read as a regular file: %s" % exc) from exc

MANIFEST_NAME = "manifest.json"
SIDECAR_NAME = "manifest.sha256"
SCHEMA_VERSION = 1

REQUIRED_CATEGORIES = (
    "source",
    "corpus",
    "per_case_matrix",
    "runner_env_digest",
    "cleanup_record",
)


class LocatorError(ValueError):
    """Locator không an toàn. Mang `locator` và `reason` máy đọc được, không chỉ là chuỗi."""

    def __init__(self, locator, reason):
        self.locator = locator
        self.reason = reason
        super().__init__("unsafe artifact locator %r rejected: %s" % (locator, reason))


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


# Tên thiết bị DOS. Trên Windows chúng phân giải thành THIẾT BỊ chứ không phải tệp, ở BẤT KỲ thư
# mục nào, và kể cả khi có phần mở rộng (`NUL.txt`) hoặc dấu chấm/khoảng trắng ở cuối. Ghi vào
# `NUL` là ghi vào hư vô mà `open()` vẫn báo thành công - manifest sẽ chứng nhận một tệp không
# tồn tại.
_DOS_DEVICES = frozenset(
    {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
    | {"COM%d" % i for i in range(1, 10)}
    | {"LPT%d" % i for i in range(1, 10)}
)


def _is_dos_device(component):
    stem = component.split(".")[0].rstrip(" .").upper()
    return stem in _DOS_DEVICES


def _is_absolute_anywhere(locator):
    """Tuyệt đối theo BẤT KỲ nền nào - một manifest di chuyển được giữa Windows và POSIX."""
    return (
        posixpath.isabs(locator)
        or ntpath.isabs(locator)
        or bool(ntpath.splitdrive(locator)[0])
        or locator.startswith("//")
    )


def safe_locator(root, locator):
    """Trả đường dẫn tuyệt đối an toàn cho `locator` dưới `root`, hoặc ném LocatorError.

    Không chạm đĩa ngoài các phép kiểm symlink; không tạo thư mục.
    """
    if not isinstance(locator, str) or not locator:
        raise LocatorError(locator, "locator must be a non-empty string")
    if "\x00" in locator:
        raise LocatorError(locator, "locator contains a NUL byte")
    if "\\" in locator:
        raise LocatorError(locator, "backslash is not a portable separator; use '/'")
    if any(ord(ch) < 32 for ch in locator):
        raise LocatorError(locator, "locator contains a control character")
    # Dấu hai chấm phục vụ HAI thứ trên Windows và cả hai đều là lối thoát: NTFS alternate data
    # stream (`carrier.txt:payload` - dữ liệu nằm trong stream, thư mục KHÔNG có tệp độc lập nào,
    # mà hash vẫn khớp) và đường dẫn drive-relative (`C:x`). Không có ca dùng hợp lệ nào trong
    # locator portable, nên chặn thẳng thay vì cố phân biệt.
    if ":" in locator:
        raise LocatorError(locator, "':' is not portable (NTFS data stream or drive-relative path)")
    if _is_absolute_anywhere(locator):
        raise LocatorError(locator, "absolute paths are not locators")

    parts = locator.split("/")
    for part in parts:
        if part == "":
            raise LocatorError(locator, "empty path component")
        if part == ".":
            raise LocatorError(locator, "'.' component is not allowed")
        if part == "..":
            raise LocatorError(locator, "parent-directory escape ('..') is not allowed")
        if part != part.rstrip(" ."):
            raise LocatorError(locator, "component %r ends with a dot or space" % part)
        if _is_dos_device(part):
            raise LocatorError(locator, "component %r is a reserved DOS device name" % part)

    root_abs = os.path.abspath(str(root))
    target = os.path.join(root_abs, *parts)

    # No-follow: symlink ở BẤT KỲ tầng nào dưới root đều bị từ chối. Root tự nó được phép nằm dưới
    # symlink (tempdir trên nhiều hệ là vậy) - ta chỉ kiểm phần do locator sinh ra.
    for index in range(1, len(parts) + 1):
        step = os.path.join(root_abs, *parts[:index])
        if os.path.islink(step):
            raise LocatorError(locator, "path component %r is a symlink" % parts[index - 1])

    real_root = os.path.realpath(root_abs)
    real_target = os.path.realpath(target)
    try:
        contained = os.path.commonpath([real_root, real_target]) == real_root
    except ValueError:  # khác ổ đĩa trên Windows
        contained = False
    if not contained:
        raise LocatorError(locator, "resolves outside run_root")
    return target


class ArtifactSet:
    """Gom artifact của một lượt chạy rồi niêm phong bằng manifest + sidecar."""

    def __init__(self, run_root, run_id):
        self.run_root = os.path.abspath(str(run_root))
        self.run_id = str(run_id)
        self.entries = []
        os.makedirs(self.run_root, exist_ok=True)

    def add(self, category, relative_name, data):
        """Ghi một artifact và ghi nhận locator + SHA-256 của nó."""
        if category not in REQUIRED_CATEGORIES:
            raise ValueError(
                "unknown artifact category %r; required categories: %s"
                % (category, ", ".join(REQUIRED_CATEGORIES))
            )
        if relative_name in (MANIFEST_NAME, SIDECAR_NAME):
            raise ValueError("artifact name %r collides with manifest files" % relative_name)
        identity = locator_identity(relative_name)
        if any(locator_identity(e["locator"]) == identity for e in self.entries):
            raise LocatorError(
                relative_name,
                "locator already recorded in this manifest (case-folded and NFC-normalised)",
            )
        target = safe_locator(self.run_root, relative_name)
        if isinstance(data, str):
            data = data.encode("utf-8")
        os.makedirs(os.path.dirname(target) or self.run_root, exist_ok=True)
        if os.path.islink(target):
            raise LocatorError(relative_name, "target already exists as a symlink")
        # O_NOFOLLOW chặn ca chen symlink giữa hai lời gọi (TOCTOU); fstat trên CHÍNH descriptor
        # bắt phần còn lại - `os.open` thành công không có nghĩa ta đang giữ một tệp thường, và
        # trên Windows `NUL` mở được, nuốt mọi thứ, trong khi O_NOFOLLOW không tồn tại ở đó.
        with _open_regular_for_write(target, relative_name) as fh:
            fh.write(data)
        self.entries.append(
            {
                "category": category,
                "locator": relative_name,
                "sha256": sha256_bytes(data),
                "bytes": len(data),
            }
        )
        return target

    def finalize(self):
        """Niêm phong: ghi manifest rồi ghi sidecar chứa SHA-256 của chính manifest.

        Từ chối niêm phong khi thiếu hạng mục bắt buộc - một manifest khuyết hạng mục vẫn "xanh"
        chính là kiểu retention giả mà acceptance đang chặn.
        """
        present = {e["category"] for e in self.entries}
        missing_categories = [c for c in REQUIRED_CATEGORIES if c not in present]
        if missing_categories:
            raise ValueError(
                "cannot finalize manifest - missing required categories: %s"
                % ", ".join(missing_categories)
            )

        manifest = {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "created_in_run_root": self.run_root,
            "required_categories": list(REQUIRED_CATEGORIES),
            "locator_policy": {
                "relative_to": "run_root",
                "rejects": ["absolute", "..", ".", "backslash", "symlink", "outside run_root"],
                "hashes_regular_files_only": True,
            },
            "self": {
                "locator": MANIFEST_NAME,
                "sha256_recorded_in": SIDECAR_NAME,
                "note": "manifest hash lives in the sidecar; verify() checks manifest against it",
            },
            "entries": sorted(self.entries, key=lambda e: e["locator"]),
        }
        blob = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        raw = blob.encode("utf-8")
        # Chính manifest và sidecar cũng phải là tệp thường trong run_root - xem _read_regular.
        with _open_regular_for_write(os.path.join(self.run_root, MANIFEST_NAME), MANIFEST_NAME) as fh:
            fh.write(raw)
        with _open_regular_for_write(os.path.join(self.run_root, SIDECAR_NAME), SIDECAR_NAME) as fh:
            fh.write((sha256_bytes(raw) + "\n").encode("utf-8"))
        return manifest


def verify(run_root):
    """Kiểm một lượt chạy đã niêm phong. Trả báo cáo máy đọc được.

    Chỉ cần `run_root` - KHÔNG cần tiến trình sinh ra artifact còn sống, cũng không cần bất kỳ
    trạng thái nào trong RAM. Đó chính là nghĩa của "locator bền".

    Manifest ở đây được coi là ĐẦU VÀO KHÔNG TIN CẬY: sidecar chỉ chứng minh manifest không đổi kể
    từ lúc niêm phong, nó KHÔNG chứng minh người niêm phong có thiện chí.
    """
    root = os.path.abspath(str(run_root))
    report = {
        "ok": False,
        "run_root": root,
        "manifest_present": False,
        "sidecar_present": False,
        "manifest_hash_ok": False,
        "missing_files": [],
        "hash_mismatches": [],
        "missing_categories": [],
        "rejected_locators": [],
        "not_regular_files": [],
        "manifest_invalid": None,
        "verified_files": 0,
    }

    manifest_path = os.path.join(root, MANIFEST_NAME)
    sidecar_path = os.path.join(root, SIDECAR_NAME)
    report["manifest_present"] = os.path.exists(manifest_path)
    report["sidecar_present"] = os.path.exists(sidecar_path)
    if not report["manifest_present"]:
        report["missing_files"].append(MANIFEST_NAME)
        return report
    if not report["sidecar_present"]:
        report["missing_files"].append(SIDECAR_NAME)
        return report

    try:
        raw = _read_regular(manifest_path, MANIFEST_NAME)
        # `errors="replace"`: một sidecar UTF-8 hỏng là ĐẦU VÀO THÙ ĐỊCH, không phải lỗi lập trình.
        # Để nó ném UnicodeDecodeError là biến "báo cáo đỏ máy đọc được" thành một traceback -
        # đúng thứ contract của module hứa sẽ không xảy ra. Chuỗi thay thế sẽ không khớp hash,
        # nên ca này rơi vào `manifest_hash_ok: false` một cách tự nhiên.
        expected = _read_regular(sidecar_path, SIDECAR_NAME).decode("utf-8", "replace").strip()
    except LocatorError as exc:
        report["rejected_locators"].append({"locator": exc.locator, "reason": exc.reason})
        return report
    report["manifest_hash_ok"] = sha256_bytes(raw) == expected
    if not report["manifest_hash_ok"]:
        # Manifest bị sửa sau khi niêm phong. Dừng ở đây: mọi entry bên trong nó đã mất thẩm quyền.
        return report

    # ── Manifest là ĐẦU VÀO KHÔNG TIN CẬY, kể cả về SCHEMA của chính nó ─────────────────────
    # Lỗ đã bị bắt: một manifest reseal với {"entries": [], "required_categories": []} trả
    # `ok=true`, `verified_files=0`. Vì `verify()` hỏi chính manifest xem nó có nghĩa vụ gì.
    # Nghĩa vụ do MODULE quy định, không phải do tài liệu đang bị kiểm tự khai.
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except ValueError as exc:
        report["manifest_invalid"] = "manifest is not valid JSON: %s" % exc
        return report
    if not isinstance(manifest, dict):
        report["manifest_invalid"] = "manifest is not an object"
        return report
    if manifest.get("schema_version") != SCHEMA_VERSION:
        report["manifest_invalid"] = "unsupported schema_version %r" % manifest.get("schema_version")
        return report
    def _invalid(reason):
        report["manifest_invalid"] = reason
        # Vẫn NÊU ĐỦ năm hạng mục còn thiếu. "Manifest hỏng" mà không nói thiếu gì thì người đọc
        # không sửa được - cùng lý do vì sao xoá artifact phải gọi đúng tên tệp.
        report["missing_categories"] = list(REQUIRED_CATEGORIES)
        return report

    entries = manifest.get("entries")
    if not isinstance(entries, list) or not entries:
        return _invalid("manifest declares no entries")
    declared = manifest.get("required_categories")
    if declared != list(REQUIRED_CATEGORIES):
        return _invalid(
            "manifest narrowed its own obligations - required_categories must be %s, got %r"
            % (list(REQUIRED_CATEGORIES), declared)
        )
    # `manifest.get("self") or {}` sập với một scalar: `1 or {}` là `1`, rồi `.get` ném
    # AttributeError. Manifest là đầu vào không tin cậy KỂ CẢ về kiểu của từng trường.
    self_block = manifest.get("self")
    if not isinstance(self_block, dict):
        return _invalid("manifest self-description is not an object: %r" % (self_block,))
    if self_block.get("locator") != MANIFEST_NAME:
        return _invalid("manifest does not describe itself")
    # Vị trí sidecar là HỢP ĐỒNG CỦA MODULE, không phải thứ manifest tự khai lại. Chấp nhận một
    # giá trị khác nghĩa là tài liệu tự mô tả sai mà vẫn được chứng nhận - và người đọc tin lời
    # khai đó sẽ đi tìm hash ở nhầm chỗ.
    if self_block.get("sha256_recorded_in") != SIDECAR_NAME:
        return _invalid(
            "manifest claims its hash lives in %r, but the contract fixes it at %r"
            % (self_block.get("sha256_recorded_in"), SIDECAR_NAME)
        )

    # Một locator phục vụ nhiều hạng mục là retention GIẢ: manifest reseal cho cả năm category
    # cùng trỏ MỘT tệp vẫn cho ok=true, verified_files=5, trong khi acceptance đòi SHA-256 cho
    # TỪNG file. Đếm entry không thay được đếm OBJECT rời nhau.
    seen_locators = set()
    seen_objects = {}
    present = set()
    for entry in entries:
        if not isinstance(entry, dict):
            return _invalid("malformed entry: %r" % (entry,))
        identity = locator_identity(entry.get("locator"))
        if identity in seen_locators:
            return _invalid("duplicate locator %r - each artifact needs its own file "
                            "(compared case-folded and NFC-normalised)" % (entry.get("locator"),))
        seen_locators.add(identity)
        locator_value, sha_value, bytes_value = (
            entry.get("locator"), entry.get("sha256"), entry.get("bytes"),
        )
        if not isinstance(locator_value, str):
            return _invalid("entry locator must be a string, got %r" % (locator_value,))
        if not isinstance(sha_value, str) or not _SHA256_HEX.fullmatch(sha_value):
            return _invalid("entry %r has a malformed sha256: %r" % (locator_value, sha_value))
        if not isinstance(bytes_value, int) or isinstance(bytes_value, bool) or bytes_value < 0:
            return _invalid("entry %r has a malformed byte count: %r" % (locator_value, bytes_value))
        if entry.get("category") not in REQUIRED_CATEGORIES:
            report["rejected_locators"].append(
                {"locator": locator_value, "reason": "unknown category %r" % entry.get("category")}
            )
            continue
        locator = entry["locator"]
        try:
            path = safe_locator(root, locator)
        except LocatorError as exc:
            report["rejected_locators"].append({"locator": locator, "reason": exc.reason})
            continue
        if not os.path.lexists(path):
            report["missing_files"].append(locator)
            continue
        # lstat, KHÔNG stat: câu hỏi là "thứ NẰM TẠI locator là gì", không phải "nó trỏ tới đâu".
        mode = os.lstat(path).st_mode
        if not stat.S_ISREG(mode):
            report["not_regular_files"].append(locator)
            continue
        # Danh tính VẬT LÝ, không phải tên: hai locator khác chuỗi vẫn có thể là CÙNG một inode
        # (hard link, hoặc trùng tên sau khi hệ tệp case-fold). Tên là thứ manifest tự khai;
        # (st_dev, st_ino) là thứ hệ tệp trả lời.
        st_info = os.lstat(path)
        object_id = (st_info.st_dev, st_info.st_ino)
        if object_id in seen_objects:
            return _invalid(
                "locators %r and %r are the same file on disk - five categories need five files"
                % (seen_objects[object_id], locator)
            )
        seen_objects[object_id] = locator
        if sha256_file(path) != entry["sha256"]:
            report["hash_mismatches"].append(locator)
            continue
        present.add(entry["category"])
        report["verified_files"] += 1

    # Đối chiếu với HẰNG của module, KHÔNG với danh sách manifest tự khai.
    report["missing_categories"] = [c for c in REQUIRED_CATEGORIES if c not in present]
    report["ok"] = (
        report["manifest_hash_ok"]
        and report["manifest_invalid"] is None
        and report["verified_files"] > 0
        and not report["missing_files"]
        and not report["hash_mismatches"]
        and not report["missing_categories"]
        and not report["rejected_locators"]
        and not report["not_regular_files"]
    )
    return report
