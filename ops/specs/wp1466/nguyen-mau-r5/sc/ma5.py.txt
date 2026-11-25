# --- ADR-0068: bảy đơn vị khoá của protocol (§1, §1.1, §8, §8.3, §12) -----------------------------------------------
# Chữ của luật ở protocol, KHÔNG chép vào đây. Mỗi đơn vị có một ĐỊA CHỈ (băm đường tiêu đề của mục chứa nó + thứ tự
# khối trong mục, 0 = trọn mục) và một băm trên BYTE THÔ của tệp. Không chuẩn hoá: chỉ dòng RỖNG (0 byte) là biên.
INV_KHOA_PROTOCOL = (  # (nhãn, băm đường tiêu đề, thứ tự, băm byte của đơn vị)
@KHOA@
)
_INV_ID_TRAN = r"INV-[0-9]{2}(?![0-9A-Za-z-])"


def _inv_muc(d: list, c: list) -> list:
    """Các mục: (băm đường tiêu đề, [(băm, dòng đầu, dòng sau cuối) của trọn mục, khối 1, …], dòng đầu, dòng sau cuối).

    `d`: các dòng BYTE thô; `c`: cùng các dòng ấy đã che vùng không render. Tiêu đề (dòng mở bằng `#`) và cấp đọc trên
    `c`; băm luôn trên `d`. Dòng rỗng là dòng 0 byte; dòng chỉ có dấu cách, tab hay `\\r` là dòng có nội dung.
    """
    bam = lambda a, b: hashlib.sha256(b"\n".join(d[a:b])).hexdigest()  # noqa: E731
    dau, ra, duong = [i for i, x in enumerate(c) if x.startswith("#")] + [len(c)], [], []
    for a, b in zip(dau, dau[1:]):
        cap = len(c[a]) - len(c[a].lstrip("#"))
        duong = [x for x in duong if x[0] < cap] + [(cap, d[a])]
        e = max(i + 1 for i in range(a, b) if d[i])
        bien = [i for i in range(a + 1, b + 1) if i == b or not d[i]]
        khoi = [(bam(s + 1, t), s + 1, t) for s, t in zip([a] + bien, bien) if t > s + 1]
        ra.append((hashlib.sha256(b"\n".join(h for _, h in duong)).hexdigest(), [(bam(a, e), a, e)] + khoi, a, b))
    return ra


def _inv_kiem_protocol(root: Path) -> list:
    """Lỗi của bảy đơn vị khoá trong protocol DƯỚI `root`; rỗng là sạch. Không đo được cũng là lỗi."""
    p = root / "docs" / "PROTOCOL_DA_PHIEN.md"
    try:
        if not p.resolve(strict=True).is_relative_to(root.resolve(strict=True)):
            return [f"KHÔNG ĐO ĐƯỢC: {p} trỏ ra ngoài --root"]
        tho = p.read_bytes()
        che, van_de = _che_khong_render(tho.decode("utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as e:
        return [f"KHÔNG ĐO ĐƯỢC: không đọc được {p}: {e}"]
    d, c = tho.split(b"\n"), che.split("\n")
    if len(d) != len(c):
        return [f"KHÔNG ĐO ĐƯỢC: phép che đổi số dòng của {p}"]
    loi = [f"KHÔNG ĐO ĐƯỢC: {x}" for x in van_de]
    loi += [f"KHÔNG ĐO ĐƯỢC: protocol dòng {i}: dòng mở bằng `<` — cổng không phân tích khối HTML"
            for i, x in enumerate(c, 1) if re.match(r" {0,3}<", x)]
    hien = [x == y.decode("utf-8") for x, y in zip(c, d)]  # dòng không bị che byte nào
    muc, vung = _inv_muc(d, c), (0, 0)
    for so, duong, thu_tu, bam in INV_KHOA_PROTOCOL:
        o = [m for m in muc if m[0] == duong]
        if len(o) != 1:
            loi.append(f"đơn vị khoá {so} : mục chứa nó phải có đúng 1 lần, thấy {len(o)}")
            continue
        vung = (o[0][2], o[0][3]) if so == INV_KHOA_PROTOCOL[0][0] else vung
        dv = o[0][1][thu_tu] if thu_tu < len(o[0][1]) else ("", 0, 0)
        so_ban = sum(k[0] == bam and all(hien[k[1]:k[2]]) for m in muc for k in (m[1][:1] if thu_tu == 0 else m[1][1:]))
        if dv[0] != bam or not all(hien[dv[1]:dv[2]]):
            loi.append(f"đơn vị khoá {so} : không còn nguyên, hoặc bị che, ở đúng địa chỉ của nó")
        elif so_ban != 1:
            loi.append(f"đơn vị khoá {so} : có {so_ban} bản hiển thị trong protocol, phải đúng 1")
    lac = [i + 1 for i, x in enumerate(c) if "|" in x and re.search(_INV_ID_TRAN, x) and not vung[0] <= i < vung[1]]
    if lac:
        loi.append(f"ID bất biến trên dòng bảng nằm ngoài tiểu mục §1.1: dòng {lac[:5]}")
    return loi


