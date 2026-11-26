# NGUYEN MAU `bat-bien` r2 — do kich thuoc + chay thu luat G1–G14; KHONG phai ma giao nop.
import ast, re, sys, unicodedata, warnings
from pathlib import Path
INV_DA_BIET = tuple(f"INV-{i:02d}" for i in range(1, 29))
INV_THA_CHUA_DO = frozenset({"INV-03"})
INV_NEO_PROTOCOL = ()  # nap tu dac ta khi thu; ma that ghi hang
_INV_TEP = re.compile(r"(?!\.{1,2}(?:/|$))[A-Za-z0-9._-]+(?:/(?!\.{1,2}(?:/|$))[A-Za-z0-9._-]+)*")
_INV_CONG = re.compile(r"cổng: (\S+) [^·]+((?: · ca: \S+::[A-Za-z0-9_]+)+)((?: · còn nợ: [A-Z0-9]+(?:-[A-Z0-9]+)*)?)")
_INV_NO = re.compile(r"kỷ luật, 0 cổng · nợ: ([A-Z0-9]+(?:-[A-Z0-9]+)*)")
_INV_CAU = re.compile(r"(?<=\.)\s+|(?<=\.\*\*)\s+")


def _inv_chuan(s: str) -> str:
    return " ".join(unicodedata.normalize("NFC", s).split())


def _inv_doc(root: Path, rel: str):
    """Hợp đồng đọc tệp CHUNG: đường tương đối chuẩn, đích resolve nằm dưới gốc, tệp thường, UTF-8. Sai một điều ⇒ None."""
    try:
        goc, p = root.resolve(strict=True), (root / rel).resolve(strict=True)
        if not _INV_TEP.fullmatch(rel) or not p.is_relative_to(goc) or not p.is_file():
            return None
        return p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, ValueError):
        return None


def _inv_che(raw: str, ten: str, che_khong_render) -> tuple:
    che, van_de = che_khong_render(raw)
    loi = [f"KHÔNG ĐO ĐƯỢC: {ten}: {x}" for x in van_de]
    loi += [f"KHÔNG ĐO ĐƯỢC: {ten} dòng {i}: dòng mở bằng `<` — cổng không phân tích khối HTML"
            for i, d in enumerate(che.split("\n"), 1) if re.match(r" {0,3}<", d)]
    return che, loi


def _inv_don_vi(che: str) -> list:
    """Đơn vị cấu trúc: ('tieu_de', dòng) · ('o', ô bảng) · ('van_xuoi', khối dòng liền nhau không thụt ≥ 4 ở dòng đầu)."""
    ra, khoi = [], []
    for d in che.split("\n") + [""]:
        if d.strip() and not d.startswith(("#", "|")):
            khoi.append(d)
            continue
        if khoi and not khoi[0].startswith("    "):
            ra.append(("van_xuoi", _inv_chuan(" ".join(khoi))))
        khoi = []
        if d.startswith("#"):
            ra.append(("tieu_de", _inv_chuan(d)))
        elif d.startswith("|"):
            ra += [("o", _inv_chuan(o)) for o in d.strip().strip("|").split("|")]
    return ra


def _inv_kiem_neo(che: str) -> list:
    """Neo `tieu_de`/`o` bằng TRỌN một đơn vị; neo `cau` bằng TRỌN một dãy câu liền nhau của MỘT đơn vị văn xuôi."""
    dv, loi = _inv_don_vi(che), []
    cua_so = set()
    for loai, t in dv:
        if loai == "van_xuoi":
            cau = _INV_CAU.split(t)
            cua_so |= {" ".join(cau[i:j]) for i in range(len(cau)) for j in range(i + 1, min(len(cau), i + 6) + 1)}
    for so, loai, neo in INV_NEO_PROTOCOL:
        if _inv_chuan(neo) not in (cua_so if loai == "cau" else {t for k, t in dv if k == loai}):
            loi.append(f"neo {so} ({loai}) vắng hoặc đã đổi: {neo[:48]!r}…")
    return loi


def _inv_ten_ca(src: str) -> set:
    """Tên ca mà nguồn Python ĐỊNH NGHĨA theo cấu trúc: `def` mức module (kèm dạng `case_`), hoặc bộ đôi đăng ký vào `CASES`."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cay = ast.parse(src)
    ten = set()
    for nut in cay.body:
        if isinstance(nut, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ten |= {nut.name, nut.name.removeprefix("case_")}
            continue
        dich = getattr(nut, "target", None) or (getattr(nut, "targets", None) or [None])[0]
        goi = nut.value.func if isinstance(nut, ast.Expr) and isinstance(nut.value, ast.Call) else None
        if isinstance(goi, ast.Attribute) and goi.attr in ("append", "extend"):
            dich = goi.value
        if isinstance(dich, ast.Name) and dich.id == "CASES":
            ten |= {c.elts[0].value for c in ast.walk(nut.value) if isinstance(c, ast.Tuple) and len(c.elts) == 2
                    and isinstance(c.elts[0], ast.Constant) and isinstance(c.elts[0].value, str)}
    return ten


def kiem_bat_bien(root: Path, che_khong_render) -> tuple:
    raw = _inv_doc(root, "docs/PROTOCOL_DA_PHIEN.md")
    if raw is None:
        return ["KHÔNG ĐO ĐƯỢC: không đọc được docs/PROTOCOL_DA_PHIEN.md dưới gốc"], {}
    che, loi = _inv_che(raw, "protocol", che_khong_render)
    loi += _inv_kiem_neo(che)
    adr = sorted(p.name for p in (root / "docs/adr").glob("0068-*.md")) if (root / "docs/adr").is_dir() else []
    than_adr = _inv_doc(root, f"docs/adr/{adr[0]}") if len(adr) == 1 else None
    no_adr = None
    if than_adr is not None:
        che_adr, loi_adr = _inv_che(than_adr, "ADR-0068", che_khong_render)
        loi += loi_adr
        muc = re.search(r"(?ms)^## Nợ[ \t]*\n(.*?)(?=^## |\Z)", che_adr)
        no_adr = set(re.findall(r"(?m)^- `([A-Z0-9]+(?:-[A-Z0-9]+)*)`: \S", muc[1])) if muc else None
    dong = che.split("\n")
    dau = [i for i, d in enumerate(dong) if d.startswith("### 1.1 ")]
    cuoi = next((i for i in range(dau[0] + 1, len(dong)) if dong[i].startswith("#")), len(dong)) if len(dau) == 1 else 0
    bang = [i for i in range(dau[0], cuoi) if re.match(r"\|\s*INV\s*\|", dong[i])] if len(dau) == 1 else []
    if len(bang) != 1 or dong[bang[0] - 1].strip() or not re.fullmatch(r"\|[\s:|-]+\|\s*", dong[bang[0] + 1]):
        return loi + ["bảng §1.1: cần đúng một tiểu mục `### 1.1 ` chứa đúng một bảng `| INV |` đứng sau một dòng trống"], {}
    hang, j = [], bang[0] + 2
    while j < cuoi and dong[j].startswith("|"):
        hang.append([_inv_chuan(o.replace("`", "")) for o in dong[j].strip().strip("|").split("|")])
        j += 1
    lac = [i + 1 for i in range(j, cuoi) if "INV-" in dong[i] and dong[i].lstrip().startswith("|")]
    if lac:
        loi.append(f"bảng §1.1: dòng dạng bảng nằm ngoài bảng ở dòng {lac}")
    ids = [h[0] for h in hang]
    if sorted(ids) != sorted(INV_DA_BIET):
        loi.append(f"bảng §1.1 lệch danh sách ID: thiếu {sorted(set(INV_DA_BIET) - set(ids))}, lạ {sorted(set(ids) - set(INV_DA_BIET))}, trùng {sorted({x for x in ids if ids.count(x) > 1})}")
    dem, ten_ca = {"cổng": 0, "còn nợ": 0, "kỷ luật": 0, "chưa đo": 0}, {}
    for h in hang:
        if len(h) != 4 or not all(h):
            loi.append(f"{h[0]}: cần đúng bốn ô khác rỗng")
            continue
        cong, no = _INV_CONG.fullmatch(h[3]), _INV_NO.fullmatch(h[3])
        ten_no = [no[1]] if no else re.findall(r"còn nợ: (\S+)", cong[3]) if cong else []
        if cong:
            dem["cổng"] += 1
            dem["còn nợ"] += bool(cong[3])
            if _inv_doc(root, cong[1]) is None:
                loi.append(f"{h[0]}: KHÔNG ĐO ĐƯỢC: tệp cổng {cong[1]} không đọc được dưới gốc")
            for tep, ten in (x.split("::") for x in re.findall(r"ca: (\S+)", cong[2])):
                if tep not in ten_ca:
                    than = _inv_doc(root, tep)
                    try:
                        ten_ca[tep] = None if than is None else _inv_ten_ca(than)
                    except (SyntaxError, ValueError):
                        ten_ca[tep] = None
                if ten_ca[tep] is None:
                    loi.append(f"{h[0]}: KHÔNG ĐO ĐƯỢC: tệp ca {tep} không đọc được dưới gốc hoặc không phân tích được")
                elif ten not in ten_ca[tep]:
                    loi.append(f"{h[0]}: ca {tep}::{ten} không được định nghĩa")
        elif no:
            dem["kỷ luật"] += 1
        elif h[3] == "chưa đo" and h[0] in INV_THA_CHUA_DO:
            dem["chưa đo"] += 1
        else:
            loi.append(f"{h[0]}: ô cổng không thuộc ba dạng, hoặc `chưa đo` ngoài danh sách tha {sorted(INV_THA_CHUA_DO)}")
        for n in ten_no:
            if no_adr is None:
                loi.append(f"{h[0]}: KHÔNG ĐO ĐƯỢC: cần đúng một tệp docs/adr/0068-*.md đọc được và có mục `## Nợ`, thấy {len(adr)} tệp")
            elif n not in no_adr:
                loi.append(f"{h[0]}: nợ {n} không phải một mục của `## Nợ` trong ADR-0068")
    return loi, dem
