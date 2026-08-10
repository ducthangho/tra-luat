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

verify() trả về báo cáo máy đọc được và gọi ĐÍCH DANH tên file thiếu - "gate đỏ" mà không nói
thiếu cái gì thì không dùng được để sửa.
"""

import hashlib
import json
import os

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


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        if isinstance(data, str):
            data = data.encode("utf-8")
        target = os.path.join(self.run_root, relative_name)
        os.makedirs(os.path.dirname(target) or self.run_root, exist_ok=True)
        with open(target, "wb") as fh:
            fh.write(data)
        self.entries.append(
            {
                "category": category,
                "locator": relative_name.replace(os.sep, "/"),
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
        path = os.path.join(root, locator.replace("/", os.sep))
        if not os.path.exists(path):
            report["missing_files"].append(locator)
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
    )
    return report
