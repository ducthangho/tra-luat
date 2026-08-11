# -*- coding: utf-8 -*-
"""F2-A (ADR-0018) — validator EOL dùng chung cho pre-commit hook và CI.

Thay cho khối EOL-FLIP GUARD bằng shell trong `.githooks/pre-commit`, vốn hỏng bốn đường:

1. Nó so DẠNG xuống dòng của bản stage với bản **HEAD**, tức là hỏi "tệp này có ĐỔI dạng không",
   chứ không hỏi "tệp này có ĐÚNG policy không". Tệp CRLF từ trước vẫn CRLF thì lọt.
2. `git cat-file -e "HEAD:$f" || continue` bỏ qua HOÀN TOÀN tệp MỚI — đúng chỗ dễ đưa CRLF mới
   vào kho nhất, vì tệp mới chưa có bản HEAD nào để so.
3. `for f in $staged` tách theo KHOẢNG TRẮNG. Kho này checkout ở `D:/Quốc hội/tra-luat`; tên có
   dấu cách và dấu tiếng Việt không phải giả định, và word-splitting biến một tên thành hai path
   không tồn tại rồi im lặng trôi qua.
4. RENAME/COPY lọt sạch. Đo được: `git mv references/golden/fix.json moved.txt` trên blob CRLF —
   `references/golden/**` khai `-text` nên CRLF ở đó HỢP LỆ, còn `moved.txt` là text nên KHÔNG.
   `--diff-filter=ACM` không có `R`, nên bản ghi `R100` bị lọc mất và validator báo `scanned: 0,
   ok: true`. Đường ngắn nhất đưa CRLF hợp lệ sang chỗ không hợp lệ đi lọt không một dấu vết.

Validator này đọc blob trong **Git index** (không tin working tree, không tin `core.autocrlf`),
lấy path bằng bản ghi NUL-delimited, và lấy policy từ chính `.gitattributes` qua `git check-attr`
thay vì chép cứng luật — hai nguồn không thể trôi lệch nhau.

Cả `--staged` (hook) lẫn `--all` (CI) đi qua CÙNG `evaluate()`; khác nhau CHỈ ở tập entry đầu vào.

Dev-side: nằm dưới `.githooks/` nên bị `_RELEASE_EXCLUDE_DIRS` loại khỏi gói phát hành. Việc nối
vào CLI `tl` thuộc F3-06 (worker gate), không thuộc F2-A: nối bây giờ phải sửa
`scripts/tl_core/command_registry.py` và `scripts/tl.py` — cả hai đang là CRLF trong index, và
`git add` dưới policy mới sẽ renormalize chúng, tức là kéo việc của F2-B vào trong F2-A.

Dùng:
    python .githooks/eol_policy.py --staged [--json]
    python .githooks/eol_policy.py --all [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

# Blob text trong index LUÔN là LF, kể cả tệp khai `eol=crlf`: `eol` chỉ quyết định dạng lúc
# CHECKOUT. Đây là lý do policy vẫn tất định trên cả Windows lẫn Linux.
_OK = "ok"
_SKIP_BINARY = "binary"
_SKIP_UNSET = "not-text"

_ERR_CRLF = "CRLF_IN_INDEX"
_ERR_MIXED = "MIXED_EOL_IN_INDEX"
_ERR_LONE_CR = "LONE_CR_IN_INDEX"

# Trạng thái có HAI path trong bản ghi `--raw -z`: `R<score>` (rename) và `C<score>` (copy) in ra
# `meta NUL source NUL destination NUL`. Mọi trạng thái còn lại chỉ có một path.
_TWO_PATH_STATUS = ("R", "C")


class EolPolicyError(RuntimeError):
    """Lỗi hạ tầng (không phải vi phạm policy): git vắng mặt, không phải kho, v.v."""


def _git(root, args, stdin=None):
    """Chạy git bằng DANH SÁCH tham số — không shell, không command substitution (ADR-0018)."""
    proc = subprocess.run(
        ["git", "-C", str(root)] + list(args),
        input=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()
        raise EolPolicyError("git %s: %s" % (" ".join(args[:2]), detail))
    return proc.stdout


def repo_root(start=None):
    """Đỉnh cây làm việc. `--root` của test trỏ vào kho tạm, mặc định là kho đang đứng."""
    start = start or os.getcwd()
    out = _git(start, ["rev-parse", "--show-toplevel"])
    return out.decode("utf-8", "surrogateescape").strip()


def _split_nul(raw):
    """Bản ghi NUL-delimited -> list. Bỏ phần tử rỗng cuối do dấu NUL kết thúc sinh ra."""
    parts = raw.split(b"\x00")
    if parts and parts[-1] == b"":
        parts.pop()
    return parts


def _decode(raw_path):
    """Path -> str. `surrogateescape` giữ nguyên byte lạ thay vì ném, để báo cáo không mất tên."""
    return raw_path.decode("utf-8", "surrogateescape")


def parse_raw_z(raw):
    """`git diff --raw -z` -> [(path_ĐÍCH, oid_ĐÍCH)].

    Bản ghi là `:<srcmode> <dstmode> <srcsha> <dstsha> <status>` rồi tới path. Với `R`/`C` có
    HAI path (nguồn, đích) — phải nhảy 3 ô chứ không phải 2, nếu không con trỏ lệch và mọi bản
    ghi sau đó bị đọc sai hoàn toàn.

    LUÔN trả path/oid của ĐÍCH. Policy của rename/copy phải theo path MỚI: blob CRLF nằm hợp lệ
    dưới `references/golden/** -text` mà bị đổi tên sang `.py` thì nó là vi phạm KỂ TỪ chỗ mới.
    Áp theo path nguồn là đúng cách bỏ lọt ca đó.
    """
    fields = _split_nul(raw)
    out = []
    i = 0
    while i < len(fields):
        meta = fields[i].decode("ascii", "replace").split()
        if len(meta) < 5 or not meta[0].startswith(":"):
            break
        status, dst_oid = meta[4], meta[3]
        step = 3 if status[:1] in _TWO_PATH_STATUS else 2
        if i + step - 1 >= len(fields):
            break
        out.append((_decode(fields[i + step - 1]), dst_oid))
        i += step
    return out


def staged_entries(root):
    """(path, blob_oid) của mọi ĐÍCH đang stage: add, copy, modify, rename, type-change.

    `--abbrev=40`: `--raw` mặc định VIẾT TẮT oid (CI còn ghim `core.abbrev 7`), mà
    `cat-file --batch` in ra oid ĐẦY ĐỦ trong header — tra cứu theo chuỗi sẽ trượt sạch và mọi
    tệp bị bỏ qua trong IM LẶNG. Đối chiếu theo THỨ TỰ ở read_blobs() là lớp chặn thứ hai.

    `D` (deleted) cố ý nằm ngoài bộ lọc: không có blob đích để kiểm.
    """
    raw = _git(root, ["diff", "--cached", "--raw", "-z", "--abbrev=40",
                      "--diff-filter=ACMRT"])
    return parse_raw_z(raw)


def tracked_entries(root):
    """(path, blob_oid) của mọi tệp trong index."""
    raw = _git(root, ["ls-files", "--stage", "-z"])
    out = []
    for rec in _split_nul(raw):
        head, sep, path = rec.partition(b"\t")
        if not sep:
            continue
        cols = head.decode("ascii", "replace").split()
        if len(cols) >= 2:
            out.append((_decode(path), cols[1]))
    return out


def check_attrs(root, paths):
    """{path: (text, eol)} lấy từ `.gitattributes` trong index.

    Policy KHÔNG được chép cứng vào đây: đọc lại từ `git check-attr` là thứ giữ validator và
    `.gitattributes` không thể trôi lệch. `--cached` để hook đọc đúng bản đang commit.
    """
    if not paths:
        return {}
    stdin = b"\x00".join(p.encode("utf-8", "surrogateescape") for p in paths) + b"\x00"
    raw = _git(root, ["check-attr", "--cached", "-z", "--stdin", "text", "eol"], stdin=stdin)
    fields = _split_nul(raw)
    attrs = {}
    for i in range(0, len(fields) - 2, 3):
        path = _decode(fields[i])
        name = fields[i + 1].decode("ascii", "replace")
        value = fields[i + 2].decode("ascii", "replace")
        attrs.setdefault(path, {})[name] = value
    return {p: (v.get("text", "unspecified"), v.get("eol", "unspecified")) for p, v in attrs.items()}


def read_blobs(root, oids):
    """oid -> bytes qua MỘT tiến trình `cat-file --batch` (286 tệp × spawn trên Windows là đắt).

    Khoá kết quả theo oid ĐÃ HỎI, không theo oid trong header: `--batch` in ra oid đầy đủ còn
    caller có thể đưa vào bản viết tắt. `--batch` trả bản ghi ĐÚNG THỨ TỰ dòng vào (kể cả dòng
    `missing`), nên ghép theo thứ tự là phép đối chiếu duy nhất không phụ thuộc độ dài oid.
    """
    wanted = [o for o in dict.fromkeys(oids) if o and set(o) <= set("0123456789abcdef")]
    if not wanted:
        return {}
    stdin = ("\n".join(wanted) + "\n").encode("ascii")
    raw = _git(root, ["cat-file", "--batch"], stdin=stdin)
    blobs = {}
    pos, idx = 0, 0
    while pos < len(raw) and idx < len(wanted):
        nl = raw.find(b"\n", pos)
        if nl < 0:
            break
        header = raw[pos:nl].decode("ascii", "replace").split()
        pos = nl + 1
        asked = wanted[idx]
        idx += 1
        if len(header) < 3:          # "<oid> missing" — không có phần nội dung theo sau
            continue
        size = int(header[2])
        blobs[asked] = raw[pos:pos + size]
        pos += size + 1              # bỏ newline chốt bản ghi
    return blobs


def classify(path, attrs, blob):
    """Một tệp -> (verdict, chi tiết). Verdict `_OK`/`_SKIP_*` là đạt; còn lại là vi phạm."""
    text_attr, eol_attr = attrs
    if text_attr == "unset":
        # `-text` khai TƯỜNG MINH: golden byte fixture và các họ binary. Git không chuẩn hoá,
        # byte là hợp đồng. Nhánh này KHÔNG phụ thuộc NUL — binary không có NUL (PDF toàn ASCII
        # ở đầu, .docx là zip) vẫn được tha đúng vì `.gitattributes` đã khai, chứ không nhờ đoán.
        return _SKIP_UNSET, {}
    if b"\x00" in blob:
        # `text=auto` coi blob có NUL là binary và cũng không chuẩn hoá. Đây là lưới CUỐI cho
        # tệp chưa kịp khai `-text`, không phải cơ chế chính.
        return _SKIP_BINARY, {}

    cr = blob.count(b"\r")
    lf = blob.count(b"\n")
    crlf = blob.count(b"\r\n")
    if cr == 0:
        return _OK, {}
    if cr == crlf and crlf == lf:
        verdict = _ERR_CRLF
    elif crlf == 0:
        verdict = _ERR_LONE_CR
    else:
        verdict = _ERR_MIXED
    return verdict, {"cr": cr, "lf": lf, "crlf": crlf, "eol_attr": eol_attr}


def evaluate(root, entries):
    """Danh sách (path, oid) -> (findings, counts). findings rỗng nghĩa là ĐẠT.

    LÕI DÙNG CHUNG: `--staged` và `--all` chỉ khác nhau ở hàm dựng `entries`; mọi phán quyết
    đi qua đây. Hook và CI không thể lệch luật vì không có đường thứ hai để lệch.
    """
    paths = [p for p, _ in entries]
    attrs = check_attrs(root, paths)
    blobs = read_blobs(root, [o for _, o in entries])
    findings, checked, skipped = [], 0, 0
    for path, oid in entries:
        blob = blobs.get(oid)
        if blob is None:
            continue
        verdict, detail = classify(path, attrs.get(path, ("unspecified", "unspecified")), blob)
        if verdict in (_SKIP_UNSET, _SKIP_BINARY):
            skipped += 1
            continue
        checked += 1
        if verdict == _OK:
            continue
        item = {"path": path, "error": verdict}
        item.update(detail)
        # Tệp `eol=crlf` vẫn phải LF trong index. Nói thẳng ra, nếu không người sửa sẽ mở tệp
        # trên đĩa, thấy CRLF đúng như mong đợi, và kết luận validator sai.
        # Thông điệp RUNTIME không dấu — cùng khuôn với `.githooks/pre-commit`: hook chạy trong
        # mọi console, kể cả cp1258/cp437, và một guard làm vỡ UnicodeEncodeError là guard hỏng.
        item["expected"] = ("LF trong index (checkout tu vat chat hoa CRLF)"
                            if detail.get("eol_attr") == "crlf" else "LF trong index")
        findings.append(item)
    findings.sort(key=lambda d: d["path"])
    return findings, {"checked": checked, "skipped": skipped}


def run(root, mode):
    entries = staged_entries(root) if mode == "staged" else tracked_entries(root)
    findings, counts = evaluate(root, entries)
    return {
        "schema": "eol_policy.v1",
        "ok": not findings,
        "mode": mode,
        "scanned": len(entries),
        "checked": counts["checked"],
        "skipped": counts["skipped"],
        "violations": findings,
    }


def _report(payload, stream):
    if payload["ok"]:
        return
    stream.write("\n=== EOL POLICY CHAN: blob trong INDEX khong dung ADR-0018 ===\n")
    for item in payload["violations"]:
        stream.write("  %s: %s (cr=%s lf=%s) — can %s\n" % (
            item["path"], item["error"], item.get("cr"), item.get("lf"), item["expected"]))
    stream.write("Chua: chuyen tep ve LF roi stage lai (vd `git add --renormalize <path>`).\n")
    stream.write("`--no-verify` KHONG phai duong migration chuan (ADR-0018).\n")


def _force_utf8_output():
    """Console Windows mac dinh cp1258/cp437 — PATH co dau tieng Viet lam vo UnicodeEncodeError.

    Guard chet vi khong in noi TEN tep vi pham la guard hong. CI da dat PYTHONIOENCODING=utf-8;
    o may dev thi ep tai day, `errors=replace` de khong bao gio nem.
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass


def main(argv=None):
    _force_utf8_output()
    ap = argparse.ArgumentParser(description="Validator EOL theo ADR-0018 (doc blob trong index).")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--staged", action="store_true", help="chi kiem tep dang stage (mac dinh)")
    group.add_argument("--all", action="store_true", help="kiem moi tep trong index")
    ap.add_argument("--root", default=None, help="goc kho; mac dinh suy tu thu muc hien tai")
    ap.add_argument("--json", action="store_true", help="in payload JSON")
    a = ap.parse_args(argv)

    try:
        root = repo_root(a.root)
        payload = run(root, "all" if a.all else "staged")
    except EolPolicyError as exc:
        sys.stderr.write("eol_policy: %s\n" % exc)
        return 2

    if a.json:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    else:
        _report(payload, sys.stderr)
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
