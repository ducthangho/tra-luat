# --- ADR-0068: bảy đơn vị khoá của protocol (§1, §1.1, §8, §8.3, §12) -----------------------------------------------
# Chữ của luật ở protocol, KHÔNG chép vào đây. Mỗi đơn vị có một ĐỊA CHỈ (băm đường tiêu đề của mục chứa nó + thứ tự
# khối trong mục, 0 = trọn mục) và một băm BYTE. Không chuẩn hoá gì: đổi một byte, dời chỗ hay nhân đôi đều đỏ.
INV_KHOA_PROTOCOL = (  # (nhãn, băm đường tiêu đề, thứ tự, băm byte của đơn vị)
@KHOA@
)
_INV_ID_TRAN = re.compile(r"INV-[0-9]{2}(?![0-9A-Za-z-])")


def _inv_bam(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _inv_muc(che: str) -> list:
    """Các mục của văn bản: (băm đường tiêu đề, [trọn mục, khối 1, khối 2, …], dòng đầu, dòng sau cuối).

    Mục = một dòng tiêu đề (mở bằng `#`) và mọi dòng tới dòng tiêu đề kế. Đường tiêu đề = các dòng tiêu đề cấp cao hơn
    đang mở, nối tới dòng của chính mục. Khối = các dòng khác trống liền nhau. Mọi đơn vị là BYTE nguyên của tệp.
    """
    dong, ra, duong = che.split("\n"), [], []
    dau = [i for i, d in enumerate(dong) if d.startswith("#")] + [len(dong)]
    for a, b in zip(dau, dau[1:]):
        cap = len(dong[a]) - len(dong[a].lstrip("#"))
        duong = [x for x in duong if x[0] < cap] + [(cap, dong[a])]
        than = "\n".join(dong[a:b]).rstrip()
        khoi = [k for k in re.split(r"\n(?:[ \t]*\n)+", "\n".join(dong[a + 1:b]).strip("\n")) if k.strip()]
        ra.append((_inv_bam("\n".join(h for _, h in duong)), [than] + khoi, a, b))
    return ra


def _inv_kiem_protocol(root: Path) -> list:
    """Lỗi của bảy đơn vị khoá trong protocol DƯỚI `root`; rỗng là sạch. Không đo được cũng là lỗi."""
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
    muc, vung = _inv_muc(che), (0, 0)
    for so, duong, thu_tu, bam in INV_KHOA_PROTOCOL:
        o = [m for m in muc if m[0] == duong]
        if len(o) != 1:
            loi.append(f"đơn vị khoá {so} : mục chứa nó phải có đúng 1 lần, thấy {len(o)}")
            continue
        vung = (o[0][2], o[0][3]) if so == INV_KHOA_PROTOCOL[0][0] else vung
        dung_cho = thu_tu < len(o[0][1]) and _inv_bam(o[0][1][thu_tu]) == bam
        so_ban = sum(_inv_bam(k) == bam for m in muc for k in (m[1][:1] if thu_tu == 0 else m[1][1:]))
        if not dung_cho:
            loi.append(f"đơn vị khoá {so} : không còn nguyên ở đúng địa chỉ của nó")
        elif so_ban != 1:
            loi.append(f"đơn vị khoá {so} : có {so_ban} bản trong protocol, phải đúng 1")
    lac = [i + 1 for i, d in enumerate(dong) if "|" in d and _INV_ID_TRAN.search(d) and not vung[0] <= i < vung[1]]
    if lac:
        loi.append(f"ID bất biến trên dòng bảng nằm ngoài tiểu mục §1.1: dòng {lac[:5]}")
    return loi
