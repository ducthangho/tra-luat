# --- ADR-0068: các đơn vị khoá của protocol (§1, §1.1, §8, §8.3, §12) -------------------------------
# Chữ của luật ở protocol, KHÔNG chép vào đây: mã chỉ giữ băm sha256 của đơn vị đã chuẩn hoá. Sửa một đơn vị khoá
# ⇒ phải sửa băm ở đây, tức đi qua một packet có review chạm tệp cổng này. Không chọn câu đại diện: khoá TRỌN đơn vị.
INV_KHOA_PROTOCOL = (  # (nhãn, loại, băm) — `muc`: từ một dòng tiêu đề tới dòng tiêu đề kế; `khoi`: một khối dòng liền nhau
@KHOA@
)


def _inv_bam(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _inv_khoi(che: str) -> list:
    """Dạng chuẩn của từng khối. Khối = các dòng khác trống liền nhau; dòng tiêu đề luôn là một khối riêng.

    Khối BẢNG (dòng đầu mở bằng `|`) giữ từng dòng, nên tách một bảng bằng dòng trống hay gộp hai hàng đều đổi băm.
    Khối khác gộp thành một dòng (ngắt dòng lại không đổi băm); khối thụt từ 4 dấu cách mang dấu riêng (khối mã).
    """
    chuan = lambda x: " ".join(unicodedata.normalize("NFC", x).split())  # noqa: E731
    ra, khoi = [], []
    for d in che.split("\n") + [""]:
        if d.strip() and not d.startswith("#"):
            khoi.append(d)
            continue
        if khoi:
            ra.append("\n".join(map(chuan, khoi)) if khoi[0].startswith("|") else
                      ("    " if khoi[0].startswith("    ") else "") + chuan(" ".join(khoi)))
        khoi = []
        if d.startswith("#"):
            ra.append(chuan(d))
    return ra


def _inv_kiem_protocol(root: Path) -> list:
    """Lỗi của các đơn vị khoá trong protocol DƯỚI `root`; rỗng là sạch. Không đo được cũng là lỗi."""
    p = root / "docs" / "PROTOCOL_DA_PHIEN.md"
    try:
        if not p.resolve(strict=True).is_relative_to(root.resolve(strict=True)):
            return [f"KHÔNG ĐO ĐƯỢC: {p} trỏ ra ngoài --root"]
        che, van_de = _che_khong_render(p.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as e:
        return [f"KHÔNG ĐO ĐƯỢC: không đọc được {p}: {e}"]
    loi = [f"KHÔNG ĐO ĐƯỢC: {x}" for x in van_de]
    loi += [f"KHÔNG ĐO ĐƯỢC: protocol dòng {i}: dòng mở bằng `<` — cổng không phân tích khối HTML"
            for i, d in enumerate(che.split("\n"), 1) if re.match(r" {0,3}<", d)]
    khoi, muc = _inv_khoi(che), []
    for k in khoi:
        if k.startswith("#"):
            muc.append([k])
        elif muc:
            muc[-1].append(k)
    co = {"khoi": {_inv_bam(k) for k in khoi}, "muc": {_inv_bam("\n\n".join(m)) for m in muc}}
    loi += [f"đơn vị khoá {so} ({loai}) vắng hoặc đã đổi trong protocol" for so, loai, bam in INV_KHOA_PROTOCOL if bam not in co[loai]]
    dem = lambda ks: sum(d.startswith("| `INV-") for k in ks for d in k.split("\n"))  # noqa: E731
    bang = [m for m in muc if _inv_bam("\n\n".join(m)) == INV_KHOA_PROTOCOL[0][2]]
    if bang and dem(khoi) != dem(bang[0]):
        loi.append(f"dòng `INV` nằm ngoài tiểu mục §1.1 đã khoá: {dem(khoi) - dem(bang[0])} dòng")
    return loi
