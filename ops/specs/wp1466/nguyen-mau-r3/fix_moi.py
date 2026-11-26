_PROTO_CO_KHOA: list = []


def _proto_co_khoa() -> str:
    """Nguồn trung tính + ĐÚNG những đơn vị của protocol THẬT mà cổng ADR-0068 khoá (dựng từ hằng của module chuẩn)."""
    if not _PROTO_CO_KHOA:
        m = importlib.util.module_from_spec(sp := importlib.util.spec_from_file_location("pl1466_khoa", CANONICAL))
        sp.loader.exec_module(m)
        che = m._che_khong_render((ROOT / "docs" / "PROTOCOL_DA_PHIEN.md").read_text(encoding="utf-8"))[0]
        can = {b for _, _, b in m.INV_KHOA_PROTOCOL}
        khoi = [k for k in re.split(r"\n[ \t]*\n", che) if k.strip() and m._inv_bam(m._inv_khoi(k)[0]) in can]
        muc = [x for x in re.split(r"(?m)^(?=#)", che) if x.startswith("#") and m._inv_bam("\n\n".join(m._inv_khoi(x))) in can]
        _PROTO_CO_KHOA.append("\n\n".join([_PROTO_TRUNG_TINH] + khoi + [x.rstrip("\n") for x in muc]) + "\n\n## Hết\n")
    return _PROTO_CO_KHOA[0]


