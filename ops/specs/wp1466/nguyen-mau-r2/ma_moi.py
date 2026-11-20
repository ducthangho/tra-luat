# --- ADR-0068: bảng bất biến §1.1 khoá theo băm; câu neo của §1, §8, §8.3, §12 ---------------
# Chữ của luật ở protocol, KHÔNG chép vào đây: mã chỉ giữ băm sha256 của đơn vị đã chuẩn hoá (NFC, gộp khoảng trắng).
# Sửa bảng hay sửa một câu neo ⇒ phải sửa băm ở đây, tức đi qua một packet có review chạm tệp cổng này.
INV_BANG_SHA256 = "@BANG@"
INV_NEO_PROTOCOL = (  # (nhãn, loại đơn vị, băm) — `tieu_de`: trọn một dòng tiêu đề; `cau`: trọn một dãy câu liền nhau của một khối văn xuôi
@NEO@
)
_INV_CAU = re.compile(r"(?<=\.)\s+|(?<=\.\*\*)\s+")
_INV_CUA_SO = 6  # số câu tối đa của một neo `cau`


def _inv_bam(s: str) -> str:
    return hashlib.sha256(" ".join(unicodedata.normalize("NFC", s).split()).encode("utf-8")).hexdigest()


def _inv_don_vi(che: str) -> dict:
    """Băm của mọi đơn vị cấu trúc: dòng tiêu đề, và mọi dãy ≤ `_INV_CUA_SO` câu liền nhau của MỘT khối văn xuôi.

    Khối văn xuôi = các dòng khác trống liền nhau, không phải tiêu đề hay dòng bảng, và dòng đầu không thụt ≥ 4 dấu cách
    (khối thụt là khối mã). Đọc CẤU TRÚC, không tìm chuỗi con: một câu neo bị nối thêm hậu tố là một câu KHÁC.
    """
    ra, khoi = {"tieu_de": set(), "cau": set()}, []
    for d in che.split("\n") + [""]:
        if d.strip() and not d.startswith(("#", "|")):
            khoi.append(d)
            continue
        if khoi and not khoi[0].startswith("    "):
            cau = _INV_CAU.split(" ".join(" ".join(khoi).split()))
            ra["cau"] |= {_inv_bam(" ".join(cau[i:j])) for i in range(len(cau)) for j in range(i + 1, min(len(cau), i + _INV_CUA_SO) + 1)}
        khoi = []
        if d.startswith("#"):
            ra["tieu_de"].add(_inv_bam(d))
    return ra


def _inv_kiem_protocol(root: Path) -> list:
    """Lỗi của bảng §1.1 và các câu neo trong protocol DƯỚI `root`; rỗng là sạch. Không đo được cũng là lỗi."""
    p = root / "docs" / "PROTOCOL_DA_PHIEN.md"
    try:
        if not p.resolve(strict=True).is_relative_to(root.resolve(strict=True)):
            return [f"KHÔNG ĐO ĐƯỢC: {p} trỏ ra ngoài --root"]
        che, van_de = _che_khong_render(p.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as e:
        return [f"KHÔNG ĐO ĐƯỢC: không đọc được {p}: {e}"]
    dong = che.split("\n")
    loi = [f"KHÔNG ĐO ĐƯỢC: {x}" for x in van_de]
    loi += [f"KHÔNG ĐO ĐƯỢC: protocol dòng {i}: dòng mở bằng `<` — cổng không phân tích khối HTML"
            for i, d in enumerate(dong, 1) if re.match(r" {0,3}<", d)]
    dv = _inv_don_vi(che)
    loi += [f"neo {so} ({loai}) vắng hoặc đã đổi trong protocol" for so, loai, bam in INV_NEO_PROTOCOL if bam not in dv[loai]]
    dau = [i for i, d in enumerate(dong) if d.startswith("### 1.1 ")]
    if len(dau) != 1:
        return loi + [f"bảng bất biến: cần đúng một tiểu mục `### 1.1 `, thấy {len(dau)}"]
    cuoi = next((i for i in range(dau[0] + 1, len(dong)) if dong[i].startswith("#")), len(dong))
    bam = _inv_bam2("\n".join(" ".join(d.split()) for d in dong[dau[0]:cuoi] if d.startswith("|")))
    if bam != INV_BANG_SHA256:
        loi.append(f"bảng bất biến §1.1 lệch băm trong mã cổng: thấy {bam}")
    return loi
