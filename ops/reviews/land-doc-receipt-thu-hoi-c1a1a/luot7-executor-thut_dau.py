import audit as A, pathlib, tempfile
for ten, tien_to in (("space", " "), ("tab", "\\t"), ("nbsp", "\\u00a0")):
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td) / "m.py"; p.write_text(A.edit('[f"{k} stale', '[f"{k} stale').replace('    ghi("K4", [f"{k} stale, chay lai"', '    ghi("K4", [f"{k} stale, chay lai"'))
        src = A.SRC.replace('    ghi("K4", [', '    ghi("K4X", [', 1)
        # ghi() tự thêm "K4: " — dựng lý do thụt đầu trực tiếp thay cho dòng ghi K4
        src = src.replace('    ghi("K4X", [f"{k} stale, chay lai" for k, v in (("S", base_hien_hanh), ("H", head_hien_hanh)) if v != r[k]])',
            '    _l = [f"' + tien_to + 'K4: {k} stale, chay lai" for k, v in (("S", base_hien_hanh), ("H", head_hien_hanh)) if v != r[k]]\n    luat["K4"] = "do" if _l else "qua"\n    ly_do += _l')
        assert "_l = " in src
        p.write_text(src); m = A.load(p, ten)
        A.emit(name=ten, **{c: A.target(m, p, c) for c in ("duong_fixture", "k4_base", "k4_head", "k4_ca_hai", "a11_k3_k4", "kieu_S")})
