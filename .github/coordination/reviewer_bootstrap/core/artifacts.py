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
import stat

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
        target = safe_locator(self.run_root, relative_name)
        if isinstance(data, str):
            data = data.encode("utf-8")
        os.makedirs(os.path.dirname(target) or self.run_root, exist_ok=True)
        if os.path.islink(target):
            raise LocatorError(relative_name, "target already exists as a symlink")
        # O_NOFOLLOW: chặn cả ca chen symlink vào giữa hai lời gọi (TOCTOU) trên nền hỗ trợ nó.
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(target, flags, 0o600)
        with os.fdopen(fd, "wb") as fh:
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
        with open(os.path.join(self.run_root, MANIFEST_NAME), "wb") as fh:
            fh.write(raw)
        with open(os.path.join(self.run_root, SIDECAR_NAME), "wb") as fh:
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

    with open(manifest_path, "rb") as fh:
        raw = fh.read()
    with open(sidecar_path, "r", encoding="utf-8") as fh:
        expected = fh.read().strip()
    report["manifest_hash_ok"] = sha256_bytes(raw) == expected
    if not report["manifest_hash_ok"]:
        # Manifest bị sửa sau khi niêm phong. Dừng ở đây: mọi entry bên trong nó đã mất thẩm quyền.
        return report

    manifest = json.loads(raw.decode("utf-8"))
    present = set()
    for entry in manifest["entries"]:
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
        if sha256_file(path) != entry["sha256"]:
            report["hash_mismatches"].append(locator)
            continue
        present.add(entry["category"])
        report["verified_files"] += 1

    report["missing_categories"] = [
        c for c in manifest.get("required_categories", REQUIRED_CATEGORIES) if c not in present
    ]
    report["ok"] = (
        report["manifest_hash_ok"]
        and not report["missing_files"]
        and not report["hash_mismatches"]
        and not report["missing_categories"]
        and not report["rejected_locators"]
        and not report["not_regular_files"]
    )
    return report
