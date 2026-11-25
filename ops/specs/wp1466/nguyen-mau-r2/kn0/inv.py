# NGUYEN MAU do kich thuoc cong canh bang INV — KHONG phai ma giao nop.
import re, sys, unicodedata
from pathlib import Path
INV_DA_BIET = tuple(f"INV-{i:02d}" for i in range(1, 22))   # danh sách CHO PHÉP: thêm/bỏ ID = sửa hằng này qua review
INV_NEO_PROTOCOL = ("### 8.3 Lịch sử lớp finding và giới hạn nghiệm thu", "Bảng lớp của mỗi lượt.", "ADR-0068")
_INV_TIEU_DE = re.compile(r"^\|\s*INV\s*\|")
_INV_PHAN_CACH = re.compile(r"^\|[\s:|-]+\|\s*$")
_INV_CONG = re.compile(r"cổng: (\S+) [^·]+((?: · ca: \S+::[A-Za-z0-9_]+)+)")
_INV_NO = re.compile(r"kỷ luật, 0 cổng · nợ: ([A-Z0-9]+(?:-[A-Z0-9]+)*)")


def _kiem_bang_inv(root: Path, raw_da_che: str, adr0068: str) -> list:
    """Bảng `| INV |` ở §1: tập ID = INV_DA_BIET, mỗi ID đúng một dòng bốn ô khác rỗng, ô cổng đúng MỘT trong ba dạng, ca trỏ tới phải TỒN TẠI."""
    m = re.search(r"(?m)^## 1\. ", raw_da_che)
    ke = re.search(r"(?m)^## ", raw_da_che[m.end():]) if m else None
    dong = (raw_da_che[m.end(): m.end() + ke.start()] if ke else raw_da_che[m.end():]).split("\n") if m else []
    hang, loi = [], [f"thiếu neo protocol {n!r}" for n in INV_NEO_PROTOCOL if n not in raw_da_che]
    for i, d in enumerate(dong):
        if _INV_TIEU_DE.match(d) and i + 1 < len(dong) and _INV_PHAN_CACH.match(dong[i + 1]):
            j = i + 2
            while j < len(dong) and dong[j].startswith("|"):
                hang.append([unicodedata.normalize("NFC", o.strip().replace("`", "")) for o in dong[j].strip().strip("|").split("|")])
                j += 1
    ids = [h[0] for h in hang]
    if sorted(ids) != sorted(INV_DA_BIET):
        loi.append(f"tập ID của bảng INV lệch danh sách đã biết: thiếu {sorted(set(INV_DA_BIET) - set(ids))}, lạ {sorted(set(ids) - set(INV_DA_BIET))}, "
                   f"trùng {sorted({x for x in ids if ids.count(x) > 1})}")
    for h in hang:
        if len(h) != 4 or not all(h) or len(h[1]) < 20:
            loi.append(f"{h[0]}: cần đúng bốn ô khác rỗng (ID, bất biến, nguồn, cổng)")
            continue
        cong, no = _INV_CONG.fullmatch(h[3]), _INV_NO.fullmatch(h[3])
        if cong:
            for tep, ten in [x.split("::") for x in re.findall(r"ca: (\S+)", cong[2])]:
                try:
                    than = (root / tep).read_text(encoding="utf-8") if (root / cong[1]).is_file() and not Path(tep).is_absolute() and ".." not in Path(tep).parts else None
                except (OSError, UnicodeDecodeError):
                    than = None
                if than is None:
                    loi.append(f"{h[0]}: KHÔNG ĐO ĐƯỢC cổng {cong[1]} hoặc tệp ca {tep}")
                elif not re.search(rf'(?m)^def (?:case_)?{re.escape(ten)}\(|\("{re.escape(ten)}",', than):
                    loi.append(f"{h[0]}: ca {tep}::{ten} không tồn tại")
        elif no:
            if no[1] not in adr0068:
                loi.append(f"{h[0]}: nợ {no[1]} không có trong ADR-0068")
        elif h[3] != "chưa đo":
            loi.append(f"{h[0]}: ô cổng không thuộc ba dạng (cổng + ca · kỷ luật, 0 cổng + nợ · chưa đo)")
    return loi


if __name__ == "__main__":
    root = Path(sys.argv[1])
    raw = (root / "docs/PROTOCOL_DA_PHIEN.md").read_text(encoding="utf-8")
    loi = _kiem_bang_inv(root, raw, next((root / "docs/adr").glob("0068-*.md")).read_text(encoding="utf-8"))
    print("\n".join(loi) or f"inv: sạch — {len(INV_DA_BIET)} ID"); sys.exit(9 if loi else 0)
