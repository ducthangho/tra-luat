"""Áp nguyên mẫu r2 (M1 mở rộng + M2) lên fragment của một cây. Dùng: python3 va.py <cây>"""
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
("""    def hong(t, nhom=ba):                                  # sửa bytes mảnh `t` của cây cổng ⇒ mã lỗi của cổng
        return cong(nhom, lambda s: (s / t).write_bytes((s / t).read_bytes() + b"# sua\\n"))[3].get("error")
""",
"""    def quyet(rc, j):                                      # quyết định CLI đủ bốn trường
        return rc, j.get("ok"), j.get("status"), j.get("error")

    def hong(t, nhom=ba):                                  # đổi MỘT byte (đầu | giữa | cuối), GIỮ độ dài ⇒ stale đủ quyết định
        def mot_vi_tri(vt):                                # MỖI vị trí một fixture riêng: cổng so một phần byte thì lộ
            def sua(s):
                d = bytearray((s / t).read_bytes())
                d[vt(len(d))] ^= 1
                (s / t).write_bytes(bytes(d))
            mods, dia, rc, j = cong(nhom, sua)            # + băm/độ dài VẾ ĐĨA tính độc lập từ bytes đã sửa
            a = dia[_M1] if len(mods) == 1 else b"".join(n.encode("utf-8") + b"\\0" + dia[n] for n, _ in mods)
            return (quyet(rc, j) == (2, False, "stale", _STALE) and len(dia[t]) == len(dict(mods)[t])
                    and (j.get("actual_sha256"), j.get("actual_bytes")) == (_bam(a), len(a)))
        return all([mot_vi_tri(vt) for vt in (lambda n: 0, lambda n: n // 2, lambda n: n - 1)])
"""),
("""        return rc != 0 and j.get("error") == _STALE and _M9 in lac and j.get("extra_shards") == lac
""",
"""        return quyet(rc, j) == (2, False, "stale", _STALE) and _M9 in lac and j.get("extra_shards") == lac
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
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("da ap", len(R), "thay the")
