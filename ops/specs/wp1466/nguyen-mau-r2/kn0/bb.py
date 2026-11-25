# NGUYEN MAU `bat-bien` (ban 2) — do kich thuoc + chay thu luat G1–G8; KHONG phai ma giao nop.
import re, sys, unicodedata
from pathlib import Path
INV_DA_BIET = tuple(f"INV-{i:02d}" for i in range(1, 22))
INV_THA_CHUA_DO = frozenset({"INV-03"})
INV_NEO_PROTOCOL = (
    "### 8.3 Lịch sử lớp finding và giới hạn nghiệm thu",
    "**Bảng lớp của mỗi lượt.**",
    "`ĐÃ VÁ THẬT` · `VÁ HỜ` · `VÁ SINH LỖI MỚI` · `CHƯA VÁ`",
    "11. Mọi lượt review — mã, đặc tả và kế hoạch — theo §8.3: mỗi finding một `class_slug`, mỗi lượt một bảng lớp, từ lượt hai đối chiếu từng finding của lượt trước bằng bốn nhãn của §8 (`ADR-0068`).",
    "12. Mỗi bất biến của protocol có ID ổn định ở bảng §1.1 và khai cổng máy đọc nó; bất biến chưa có cổng mang nhãn kỷ luật kèm một nợ có tên (`ADR-0068`).",
    "Mục này là bất biến `INV-12` và áp cho mọi lượt review: mã, đặc tả và kế hoạch (`ADR-0068`).",
    "Mọi lượt review (mã, đặc tả, kế hoạch) xuất verdict theo lớp: mỗi finding một `class_slug`, bảng lớp, đối chiếu lượt trước bằng bốn nhãn",
    "Một lớp xuất hiện ở ba lượt review khác nhau đòi xem lại cách làm tại checkpoint",
)
_INV_CONG = re.compile(r"cổng: (\S+) [^·]+((?: · ca: \S+::[A-Za-z0-9_]+)+)")
_INV_NO = re.compile(r"kỷ luật, 0 cổng · nợ: ([A-Z0-9]+(?:-[A-Z0-9]+)*)")
nfc = lambda s: unicodedata.normalize("NFC", s)  # noqa: E731


def _doc_utf8(p: Path):
    try:
        return p.read_text(encoding="utf-8") if p.is_file() else None
    except (OSError, UnicodeDecodeError):
        return None


def kiem_bat_bien(root: Path, che_khong_render) -> tuple:
    raw = _doc_utf8(root / "docs/PROTOCOL_DA_PHIEN.md")
    adr = sorted((root / "docs/adr").glob("0068-*.md")) if (root / "docs/adr").is_dir() else []
    if raw is None:
        return ["KHÔNG ĐO ĐƯỢC: không đọc được docs/PROTOCOL_DA_PHIEN.md"], {}
    che, van_de = che_khong_render(raw)
    loi = [f"KHÔNG ĐO ĐƯỢC: {x}" for x in van_de]
    doan = [" ".join(nfc(d).split()) for d in re.split(r"\n[ \t]*\n", che)]
    loi += [f"thiếu neo protocol: {n!r}" for n in INV_NEO_PROTOCOL if not any(" ".join(nfc(n).split()) in d for d in doan)]
    m = re.search(r"(?m)^## 1\. ", che)
    ke = re.search(r"(?m)^## ", che[m.end():]) if m else None
    dong = (che[m.end(): m.end() + ke.start()] if ke else che[m.end():]).split("\n") if m else []
    hang = []
    for i, d in enumerate(dong):
        if re.match(r"^\|\s*INV\s*\|", d) and i + 1 < len(dong) and re.match(r"^\|[\s:|-]+\|\s*$", dong[i + 1]):
            j = i + 2
            while j < len(dong) and dong[j].startswith("|"):
                hang.append([nfc(o.strip().replace("`", "")) for o in dong[j].strip().strip("|").split("|")])
                j += 1
    ids = [h[0] for h in hang]
    if sorted(ids) != sorted(INV_DA_BIET):
        loi.append(f"bảng §1.1 lệch danh sách ID: thiếu {sorted(set(INV_DA_BIET) - set(ids))}, lạ {sorted(set(ids) - set(INV_DA_BIET))}, trùng {sorted({x for x in ids if ids.count(x) > 1})}")
    dem = {"cổng": 0, "kỷ luật": 0, "chưa đo": 0}
    than_adr = _doc_utf8(adr[0]) if len(adr) == 1 else None
    for h in hang:
        if len(h) != 4 or not all(h):
            loi.append(f"{h[0]}: cần đúng bốn ô khác rỗng")
            continue
        cong, no = _INV_CONG.fullmatch(h[3]), _INV_NO.fullmatch(h[3])
        if cong:
            dem["cổng"] += 1
            if not (root / cong[1]).is_file():
                loi.append(f"{h[0]}: KHÔNG ĐO ĐƯỢC: tệp cổng {cong[1]} không tồn tại")
            for tep, ten in (x.split("::") for x in re.findall(r"ca: (\S+)", cong[2])):
                than = None if Path(tep).is_absolute() or ".." in Path(tep).parts else _doc_utf8(root / tep)
                if than is None:
                    loi.append(f"{h[0]}: KHÔNG ĐO ĐƯỢC: tệp ca {tep} không đọc được")
                elif not re.search(rf'(?m)^def (?:case_)?{re.escape(ten)}\(|\("{re.escape(ten)}",', than):
                    loi.append(f"{h[0]}: ca {tep}::{ten} không tồn tại")
        elif no:
            dem["kỷ luật"] += 1
            if than_adr is None:
                loi.append(f"{h[0]}: KHÔNG ĐO ĐƯỢC: cần đúng một tệp docs/adr/0068-*.md đọc được, thấy {len(adr)}")
            elif f"`{no[1]}`" not in than_adr:
                loi.append(f"{h[0]}: nợ {no[1]} không có trong ADR-0068")
        elif h[3] == "chưa đo" and h[0] in INV_THA_CHUA_DO:
            dem["chưa đo"] += 1
        else:
            loi.append(f"{h[0]}: ô cổng không thuộc ba dạng, hoặc `chưa đo` ngoài danh sách tha {sorted(INV_THA_CHUA_DO)}")
    return loi, dem
