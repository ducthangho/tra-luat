_PROTO_CO_KHOA = []


def _proto_co_khoa() -> str:
    """Nguồn trung tính + bảy đơn vị khoá của protocol THẬT đặt ĐÚNG ĐỊA CHỈ (khối đứng trước là khối đệm)."""
    if not _PROTO_CO_KHOA:
        sp = importlib.util.spec_from_file_location("pl1466_khoa", CANONICAL)
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        tho = (ROOT / "docs" / "PROTOCOL_DA_PHIEN.md").read_bytes()
        d, c = tho.split(b"\n"), m._che_khong_render(tho.decode("utf-8"))[0].split("\n")
        can, ra, mo = {}, [_PROTO_TRUNG_TINH], []
        for _, duong, thu_tu, _ in m.INV_KHOA_PROTOCOL:
            can.setdefault(duong, set()).add(thu_tu)
        for duong, dv, a, _ in m._inv_muc(d, c):
            cap, tieu_de = len(c[a]) - len(c[a].lstrip("#")), d[a].decode("utf-8")
            mo = [x for x in mo if x[0] < cap] + [(cap, tieu_de, duong in can)]
            if duong in can:
                lay = [b"\n".join(d[s:e]).decode("utf-8") for _, s, e in dv]
                ra += [t for _, t, co in mo[:-1] if not co and t not in ra]
                ra += [lay[0]] if 0 in can[duong] else [tieu_de] + [lay[i] if i in can[duong] else f"khối đệm {i}" for i in range(1, max(can[duong]) + 1)]
        _PROTO_CO_KHOA.append("\n\n".join(ra) + "\n\n## Hết\n")
    return _PROTO_CO_KHOA[0]


