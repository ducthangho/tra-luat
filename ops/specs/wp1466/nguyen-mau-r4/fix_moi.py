_PROTO_CO_KHOA: list = []


def _proto_co_khoa() -> str:
    """Nguồn trung tính + bảy đơn vị khoá của protocol THẬT đặt ĐÚNG ĐỊA CHỈ (khối đứng trước là khối đệm)."""
    if not _PROTO_CO_KHOA:
        m = importlib.util.module_from_spec(sp := importlib.util.spec_from_file_location("pl1466_khoa", CANONICAL))
        sp.loader.exec_module(m)
        che = m._che_khong_render((ROOT / "docs" / "PROTOCOL_DA_PHIEN.md").read_text(encoding="utf-8"))[0]
        can, ra, mo = {}, [_PROTO_TRUNG_TINH], []
        for _, duong, thu_tu, _ in m.INV_KHOA_PROTOCOL:
            can.setdefault(duong, set()).add(thu_tu)
        for duong, khoi, _, _ in m._inv_muc(che):
            tieu_de = khoi[0].split("\n")[0]
            cap = len(tieu_de) - len(tieu_de.lstrip("#"))
            mo = [x for x in mo if x[0] < cap] + [(cap, tieu_de, duong in can)]
            if duong in can:
                ra += [t for _, t, co in mo[:-1] if not co and t not in ra]
                ra += [khoi[0]] if 0 in can[duong] else [tieu_de] + [khoi[i] if i in can[duong] else f"khối đệm {i}" for i in range(1, max(can[duong]) + 1)]
        _PROTO_CO_KHOA.append("\n\n".join(ra) + "\n\n## Hết\n")
    return _PROTO_CO_KHOA[0]


