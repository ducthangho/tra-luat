_CAP = re.compile(r"(\d+)/(\d+)")

def _cap(g):
    return None if len(g) % 2 else [(g[i], g[i + 1]) for i in range(0, len(g), 2)]

def bang_chung_xanh(text, mau):
    span, tong = (mau, ()) if isinstance(mau, str) else mau
    m = re.search(span, text, re.M)
    if not m or _cap(m.groups()) is None:
        return False                                    # không khớp · nhóm LẺ (mẫu lỗi)
    if not tong:                                        # chuỗi trần (tương thích): số CHỈ từ SPAN
        return bool(m.groups()) and all(int(a) > 0 and a == b for a, b in _cap(m.groups()))
    cap = []                                            # có TONG: SPAN chỉ là điều kiện khớp (luật 5)
    lines = text.splitlines()
    for chon, grammar in tong:
        hits = [l for l in lines if re.match(chon, l)]
        if len(hits) != 1:                              # luật 3: 0 hay ≥ 2 bản ghi cùng loại
            return False
        g = re.fullmatch(grammar, hits[0])              # luật 4: trọn dòng
        c = _cap(g.groups()) if g else None
        if c is None:
            return False
        if len(_CAP.findall(hits[0])) != len(c) + len(_CAP.findall(grammar)):
            return False                                # luật 7: cặp trên dòng tổng mà grammar không giải trình
        cap += c
    return all(int(a) > 0 and a == b for a, b in cap)
