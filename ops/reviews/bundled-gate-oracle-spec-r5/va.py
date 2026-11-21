"""Áp nguyên mẫu r4 (M1 mở rộng + M2) lên fragment của một cây. Dùng: python3 va.py <cây>"""
import sys

p = sys.argv[1] + "/scripts/test_fragments/wp433_bundled_tach_manh.py"
s = open(p, encoding="utf-8").read()
R = [
("""    gan = {t.id: ast.literal_eval(n.value) for n in body for t in getattr(n, "targets", [getattr(n, "target", None)])
           if isinstance(t, ast.Name)}                     # GIÁ TRỊ đọc rộng; HÌNH DẠNG (`ten`) mới theo luật loader
""",
"""    gan = {}                                               # DỮ LIỆU: chỉ phép gán CHUẨN (Assign một đích Name), lần ĐẦU thắng;
    for n in body:                                         # HÌNH DẠNG (`ten`) mới theo luật loader (V3/V8)
        if type(n) is ast.Assign and [type(t) for t in n.targets] == [ast.Name] and n.targets[0].id in (_SRC, _SHA):
            gan.setdefault(n.targets[0].id, ast.literal_eval(n.value))
"""),
("""    return ten, [n for n, _ in gan[_SRC]], gan.get(_SHA)
""",
"""    return ten, [n for n, _ in gan.get(_SRC, ())], gan.get(_SHA)   # thiếu phép gán chuẩn ⇒ RỖNG, không văng (V3/V8 phán hình dạng)
"""),
("""    def hong(t, nhom=ba):                                  # sửa bytes mảnh `t` của cây cổng ⇒ mã lỗi của cổng
        return cong(nhom, lambda s: (s / t).write_bytes((s / t).read_bytes() + b"# sua\\n"))[3].get("error")
""",
"""    def quyet(rc, j):                                      # quyết định CLI đủ bốn trường
        return rc, j.get("ok"), j.get("status"), j.get("error")

    def hong(t, nhom=ba):                                  # MỖI nhiễu loạn một fixture riêng trên mảnh `t` ⇒ stale đủ quyết định
        def lat(k):                                        # và đủ bốn trường băm/độ dài, tính ĐỘC LẬP từ vế kỳ vọng + bytes đĩa
            return lambda d: d[:k(len(d))] + bytes([d[k(len(d))] ^ 1]) + d[k(len(d)) + 1:]
        bien = (lat(lambda n: 0), lat(lambda n: n // 2), lat(lambda n: n - 1),     # giữ độ dài: đầu | giữa | cuối
                lambda d: d + b"#", lambda d: d[:-1],                              # đổi độ dài: nối | cắt
                lambda d: d + b"# sua\\n",                                         # nhiễu loạn của BASE (nối dòng trọn) — giữ nguyên
                lambda d: d.replace(b"\\n", b"\\r\\n", 1))                          # kết thúc dòng: LF -> CRLF

        def mot(f):
            mods, dia, rc, j = cong(nhom, lambda s: (s / t).write_bytes(f((s / t).read_bytes())))
            ghep = (lambda m: m[_M1]) if len(mods) == 1 else (
                lambda m: b"".join(n.encode("utf-8") + b"\\0" + m[n] for n, _ in mods))
            e, a = ghep(dict(mods)), ghep(dia)
            return quyet(rc, j) == (2, False, "stale", _STALE) and truong(j) == [_bam(e), _bam(a), len(e), len(a)]
        return all([mot(f) for f in bien])
"""),
("""        mods, dia, rc, j = cong(ba, lambda s: (s / _M9).write_bytes(b"x = 0\\n"))
        lac = sorted(set(dia) - {n for n, _ in mods})      # tệp đánh số trên đĩa mà generator KHÔNG trả tên
        return rc != 0 and j.get("error") == _STALE and _M9 in lac and j.get("extra_shards") == lac
""",
"""        def mot_lac(ten):                                  # MỖI mảnh lạc một fixture riêng: MỘT chữ số và HAI chữ số
            mods, dia, rc, j = cong(ba, lambda s: (s / ten).write_bytes(b"x = 0\\n"))
            lac = sorted(set(dia) - {n for n, _ in mods})  # tệp đánh số trên đĩa mà generator KHÔNG trả tên
            return quyet(rc, j) == (2, False, "stale", _STALE) and lac == [ten] and j.get("extra_shards") == lac
        return all([mot_lac(ten) for ten in (_M9, _M10)])
"""),
("""_M2, _M3, _M9 = (f"tl_test_fragments_bundled_{k}.py" for k in (2, 3, 9))
""",
"""_M2, _M3, _M9, _M10 = (f"tl_test_fragments_bundled_{k}.py" for k in (2, 3, 9, 10))
"""),
("""        return rc != 0 and j.get("error") == _STALE and j["shards"][1]["actual_bytes"] is None
""",
"""        return quyet(rc, j) == (2, False, "stale", _STALE) and j["shards"][1]["actual_bytes"] is None
"""),
("""                and (rc, j.get("ok"), j.get("status")) == (0, True, "current") and hong(_M1, [mot[1]]) == _STALE)
""",
"""                and quyet(rc, j) == (0, True, "current", None) and hong(_M1, [mot[1]]))
"""),
("""        lambda: [hong(_M1), hong(_M2)] == [_STALE, _STALE],                    # V24: mảnh CHÍNH và mảnh phụ
""",
"""        lambda: [hong(_M1), hong(_M2)] == [True, True],                        # V24: mảnh CHÍNH và mảnh phụ
"""),
("""        lambda: cong([mot[1]], lambda s: (s / _M1).unlink())[3].get("error") == _MISSING,                  # V26
""",
"""        lambda: quyet(*cong([mot[1]], lambda s: (s / _M1).unlink())[2:]) == (2, False, "missing", _MISSING),  # V26
"""),
('    def v5():\n        d = "đ" * 100                                      # 2 byte UTF-8 mỗi ký tự: đếm KÝ TỰ thay vì BYTE sẽ lệch ranh\n        fx = ("lech", [(f"wp9001_x{i}.py", d + "x" * (i == 3)) for i in range(4)])\n        x, s = [n for n, _ in fx[1]], len(_dong("wp9001_x0.py", d).encode("utf-8"))   # x0–x2 cỡ s; x3 = s + 1; hạn = 2s\n        return len(_dong(x[3], d + "x").encode("utf-8")) == s + 1 and nhom(fx, 2 * s) == [x[:2], x[2:3], x[3:]]\n\n    def v6():\n        g = ["wp9001_g0.py", "wp9001_g1.py", "wp9001_g2.py"]\n        return nhom(("lon", [(g[0], ""), (g[1], "x" * 150 * 1024), (g[2], "")])) == [g[:1], g[1:2], g[2:]]\n\n',
 '    d5 = "đ" * 100                                         # 2 byte UTF-8 mỗi ký tự: đếm KÝ TỰ thay vì BYTE sẽ lệch ranh\n    lech = ("lech", [(f"wp9001_x{i}.py", d5 + "x" * (i == 3)) for i in range(4)])\n    s5 = len(_dong("wp9001_x0.py", d5).encode("utf-8"))   # x0–x2 cỡ s5; x3 = s5 + 1; hạn = 2·s5\n    g6 = ["wp9001_g0.py", "wp9001_g1.py", "wp9001_g2.py"]\n    lon = ("lon", [(g6[0], ""), (g6[1], "x" * 150 * 1024), (g6[2], "")])\n\n    def v5():\n        x = [n for n, _ in lech[1]]\n        return len(_dong(x[3], d5 + "x").encode("utf-8")) == s5 + 1 and nhom(lech, 2 * s5) == [x[:2], x[2:3], x[3:]]\n\n    def v6():\n        return nhom(lon) == [g6[:1], g6[1:2], g6[2:]]\n\n    def v8():                                              # hình dạng MỌI gói nhiều mảnh fragment sinh ra (deu, lech, lon)\n        hinh = [[_gan(d)[0] for _, d in sinh(fx, *han_fx)[1]] for fx, *han_fx in ((deu,), (lech, 2 * s5), (lon,))]\n        return hinh[0] == [[_SRC, _SHA], [_SRC], [_SRC]] and all(\n            len(h) > 1 and h == [[_SRC, _SHA]] + [[_SRC]] * (len(h) - 1) for h in hinh)\n\n'),
('        lambda: [_gan(d)[0] for _, d in sinh(deu)[1]] == [[_SRC, _SHA], [_SRC], [_SRC]],                   # V8 (+ mảnh phụ)\n',
 '        v8,                                                                                                # V8 (+ mảnh phụ, mọi gói nhiều mảnh)\n'),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("da ap", len(R), "thay the")
