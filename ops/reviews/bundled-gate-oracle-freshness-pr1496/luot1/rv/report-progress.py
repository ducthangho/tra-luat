"""Nhập các kết quả đã có vào verdict đang rà soát."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
LOG = ROOT / "log"
VERDICT = ROOT.parent / "VERDICT.md"
GATE_START = "<!-- ket-qua-cong -->"
GATE_END = "<!-- het-ket-qua-cong -->"
HUNT_START = "<!-- ket-qua-san -->"
HUNT_END = "<!-- het-ket-qua-san -->"
NAMES = {
    "control": ("Đối chứng", "Fragment nguyên bản trả 32 khoá xanh."),
    "hai_swapped_ast": ("Hình dạng gói hai fragment", "Thay gán một đích bằng gán unpack trên `hai`. V3 phải đỏ dù C đọc dữ liệu rỗng."),
    "deu_source_content": ("Bảo toàn nguồn trong bundle", "Một mục trên `deu` giữ nguyên tên và kích thước nhưng đổi thân `run()`. Các phép so tên và sao bundle có bắt được nội dung sai."),
    "lech_assert": ("Thân mảnh phụ ở ranh UTF-8", "Một mảnh phụ của `lech` có thêm `assert True`. V8 phải đọc cả mảnh đó."),
    "lon_nonliteral": ("Giá trị chuẩn ở mảnh quá cỡ", "`SOURCES` của fixture `lon` chuyển sang lời gọi `tuple`. Ngoại lệ đọc literal phải làm đỏ khoá."),
    "deu_manifest_reverse": ("Thứ tự metadata mảnh", "Đảo thứ tự `SHARDS` trên `deu` mà giữ nguyên các mục nguồn. V9 phải đỏ."),
    "loader_relaxes_sources_type": ("Kiểu dữ liệu ở loader", "Loader nới kiểu container `SOURCES` từ tuple sang tuple/list. Các fixture loader phải phân biệt hai kiểu."),
    "writer_primary_eol": ("Ranh generator/writer", "Writer cắt LF ở cuối mảnh chính trong khi byte generator giữ nguyên. V11 phải đỏ."),
    "extra_duplicate_names": ("V23 đối chiếu danh sách mảnh lạc", "Cổng trả mỗi tên mảnh lạc hai lần dù quyết định stale đúng."),
    "stale_rc_wrong": ("Mã thoát CLI", "Nhánh thất bại trả rc 1 thay cho rc 2 và giữ nguyên payload."),
    "absent_shard_empty_field": ("V25 phân biệt thiếu mảnh", "Cổng báo `actual_bytes=-1` cho mảnh vắng. Khoá phải đòi `None`."),
    "missing_numeric_ok": ("V26 kiểm kiểu JSON", "Cổng trả số `0` ở `ok` trên nhánh missing, giữ rc 2, status và error."),
    "current_has_error": ("V27 trạng thái current tự mâu thuẫn", "Cổng giữ rc 0 và `ok=true` nhưng thêm mã lỗi stale vào JSON current."),
    "stale_wrong_size": ("Kích thước từng mảnh khi stale", "Nhánh stale ghi kích thước kỳ vọng đè số byte thực tế của từng mảnh có mặt trong khi số tổng hợp vẫn đúng."),
}


def span(start, end):
    return f"{start[11:19]}–{end[11:19]}"


def gate_out(name, raw):
    out = raw.strip()
    if name == "selftest":
        result = re.findall(r"== tl selftest \d+/\d+ ==", raw)
        return (result[-1] if result else out.splitlines()[-1], result == ["== tl selftest 1786/1786 =="])
    if name == "eol":
        result = next(line for line in out.splitlines() if re.fullmatch(r"\d+/\d+ dat", line))
        return (result, result == "32/32 dat")
    if name == "ruff":
        return (out, out == "All checks passed!")
    if name in ("ruff-version", "doctrine", "adr"):
        return (out, bool(out))
    if name in ("diffcheck", "regen-bundle", "regen-bundle-diff", "status"):
        return (out or "stdout/stderr rỗng", not out)
    if name == "names":
        return (" · ".join(out.splitlines()), bool(out))
    data = json.loads(out)
    ok = data.get("ok")
    if name == "fragments":
        return (f"ok={ok}, status={data['status']}, expected/actual bytes {data['expected_bytes']}/{data['actual_bytes']}",
                ok is True and data["status"] == "current" and data["expected_sha256"] == data["actual_sha256"])
    if name == "bundle":
        return (f"ok={ok}, failed={len(data['failed'])}, case_count={data['case_count']}",
                ok is True and data["failed"] == [] and data["case_count"] == 20)
    if name == "verify":
        return (f"ok={ok}, expected_file_count={data['expected_file_count']}, checked_file_count={data['checked_file_count']}",
                ok is True and data["expected_file_count"] == data["checked_file_count"] == 186)
    if name == "workflow":
        py = data["py_size"]
        return (f"ok={ok}, py_size.fail={py['fail']}, py_size.warn={py['warn']}, files_scanned={py['files_scanned']}",
                ok is True and py["fail"] == py["warn"] == [] and py["files_scanned"] == 74)
    if name == "golden":
        return (f"ok={ok}, case_count={data['case_count']}", ok is True and data["case_count"] == 20)
    if name == "regen-manifest":
        return (f"package_hash={data['package_hash']}", bool(data["package_hash"]))
    raise ValueError(name)


def gate_rows():
    rows = ["| Lệnh | RC | Giờ UTC | Kết quả |", "|---|---:|---|---|"]
    for line in (LOG / "gates.tsv").read_text().splitlines():
        lane, name, rc, start, end, command = line.split("\t", 5)
        log = LOG / f"{lane}-{name}.out"
        raw = log.read_text()
        try:
            output, positive = gate_out(name, raw)
        except (ValueError, KeyError, IndexError):
            output, positive = "Không có dấu hiệu đạt theo định dạng yêu cầu", False
        state = "Đạt" if rc == "0" and positive else "Đỏ"
        if name == "status" and all(line.startswith("!! ") for line in raw.splitlines()):
            state = "Snapshot trước dọn"
            output = f"{len(raw.splitlines())} tệp ignored do phép đo tạo, tracked và untracked sạch"
        if name == "regen-bundle":
            command = command.replace("python3 -c ", 'python3 -c "', 1) + '"'
        output = output.replace("|", "\\|").replace("\n", " · ")
        rows.append(f"| `{lane}` · `{command}` | {rc} | {span(start, end)} | {state} · `{output}` · [log](rv/log/{log.name}) |")
    return rows


def read_hunt(lane):
    source = LOG / f"hunt-{lane}.out"
    retry = LOG / f"hunt-{lane}-retry.out"
    lines = source.read_text().splitlines()
    if retry.exists():
        lines.extend(retry.read_text().splitlines())
    return {
        name: json.loads(raw)
        for name, raw in (
            line.split(" ", 1) for line in lines
        )
    }


def describe(result):
    if "anchor" in result:
        return f"không áp được, số neo={result['anchor'][1]}"
    if "run" not in result:
        return f"văng, rc={result['rc']}"
    msg = f"rc={result['rc']} run={result['run']} so_nhan={result['so_nhan']} do=" + ",".join(result["do"])
    if result["ly_do"]:
        reasons = [f"{key}:{reason.split(':', 1)[0]}" for key, reason in result["ly_do"].items()]
        msg += " ly_do=" + ",".join(reasons)
    return msg


def hunt_rows():
    base = read_hunt("nen")
    candidate = read_hunt("sau")
    rows = ["| Hướng | Giả thuyết | Lệnh | Output thật | Kết luận |", "|---|---|---|---|---|"]
    for key, (name, assumption) in NAMES.items():
        if key not in base or key not in candidate:
            continue
        b, c = base[key], candidate[key]
        if any(result.get("so_nhan") != 32 for result in (b, c)):
            conclusion = "KHÔNG ĐO ĐƯỢC"
        elif not b["run"] and c["run"]:
            conclusion = "LỖI — C để sống ca base giết"
        elif key != "control" and b["run"] and c["run"]:
            conclusion = "KHÔNG PHẢI LỖI hồi quy. Cùng sống, P3 theo Q7."
        else:
            conclusion = "KHÔNG PHẢI LỖI"
        command = f"`python3 -B rv/hunt.py nen {key}` và `python3 -B rv/hunt.py sau {key}`"
        rows.append(f"| {name} | {assumption} | {command} | base `{describe(b)}`, C `{describe(c)}` | {conclusion} |")
    return rows


def replace_block(text, start, end, rows, anchor):
    body = f"{start}\n" + "\n".join(rows) + f"\n{end}"
    if start in text:
        return text[:text.index(start)] + body + text[text.index(end) + len(end):]
    return text.replace(anchor, body + "\n\n" + anchor)


def main():
    text = VERDICT.read_text()
    text = replace_block(text, GATE_START, GATE_END, gate_rows(), "## Săn hồi quy")
    text = replace_block(text, HUNT_START, HUNT_END, hunt_rows(), "## Lớp finding")
    temp = ROOT / ".verdict-progress"
    temp.write_text(text)
    temp.replace(VERDICT)


if __name__ == "__main__":
    main()
