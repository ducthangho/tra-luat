_CAP = re.compile(r"(\d+)/(\d+)")

def _cap(g):
    return None if len(g) % 2 else [(g[i], g[i + 1]) for i in range(0, len(g), 2)]

def bang_chung_xanh(text, mau):
    span, tong = (mau, ()) if isinstance(mau, str) else mau
    m = re.search(span, text, re.M)
    if not m or _cap(m.groups()) is None:
        return False
    if not tong:
        pairs = _cap(m.groups())
        return bool(pairs) and all(a and b and a.isdecimal() and b.isdecimal()
                                  and int(a) == int(b) > 0 for a, b in pairs)
    cap = []
    for chon, grammar in tong:
        hits = [line for line in text.splitlines() if re.match(chon, line)]
        if len(hits) != 1:
            return False
        g = re.fullmatch(grammar, hits[0])
        c = _cap(g.groups()) if g else None
        if not c:
            return False
        actual = [(p.span(1), p.span(2)) for p in _CAP.finditer(hits[0])]
        covered = [(g.span(i), g.span(i + 1)) for i in range(1, len(g.groups()) + 1, 2)]
        if covered != actual:
            return False
        cap += c
    return bool(cap) and all(int(a) == int(b) > 0 for a, b in cap)
