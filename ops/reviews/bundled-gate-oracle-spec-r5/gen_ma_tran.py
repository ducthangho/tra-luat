"""Sinh ma_tran_r11.py (r5) từ ma trận g5 (r1/mt.py = bf38a110) + đột biến lớp F10/F11 + m1–m8 (review r2) + ca gỡ chốt a7."""
from pathlib import Path

H = Path(__file__).resolve().parent
src = (H.parent / "r1" / "mt.py").read_text(encoding="utf-8")
pr = (H.parent / "r1" / "probe.py").read_text(encoding="utf-8")
ns = {}
exec(pr[pr.index("TF, RL, FR ="):pr.index("# go ban va (A7)")], ns)
M = ns["MUT"]
RV3 = {}
n4 = {"__name__": "rv4"}
_t = (H / "rv4_san.py").read_text(encoding="utf-8")
exec(_t[_t.index("TF, RL ="):_t.index("RUN = ")], n4)
RV4 = {ten: subs for ten, subs in n4["MUT"] if ten != "doi_chung"}
for f in ("rv3_muts.py", "rv3_muts2.py"):
    n3 = {}
    exec((H / f).read_text(encoding="utf-8"), n3)
    RV3.update({ten: subs for ten, _, subs in n3["MUT"] if ten != "doi_chung"})
TF, RL, FR = ns["TF"], ns["RL"], ns["FR"]
SO = "    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n"


def so(expr):
    return [(RL, SO, SO.replace("a != d", expr))]


R2 = {  # tám đột biến tự nghĩ của review độc lập r2 (định nghĩa nguyên văn, /dev/shm/rv2-r11b/mine/mk2.py)
    "m1": so("(a is None or a[:len(d)] != d)"),
    "m2": so("(a is None or d[:len(a)] != a)"),
    "m3": so('(a is None or a.replace(b"\\r\\n", b"\\n") != d)'),
    "m4": [(RL, '"error": "GENERATED_BUNDLE_STALE",\n            "expected_sha256": expected_sha256,',
            '"error": "GENERATED_BUNDLE_STALE",\n            "expected_sha256": actual_sha256,')],
    "m5": [(RL, '"expected_bytes": len(expected),\n            "actual_bytes": len(actual),\n            "extra_shards"',
            '"expected_bytes": len(actual),\n            "actual_bytes": len(actual),\n            "extra_shards"')],
    "m6": [(RL, '"actual_bytes": len(actual),\n            "extra_shards"', '"actual_bytes": len(expected),\n            "extra_shards"')],
    "m7": [(RL, "p.read_bytes() if p.is_file() and not p.is_symlink() else None",
            "p.read_bytes()[:len(_)] if p.is_file() and not p.is_symlink() else None")],
    "m8": [(TF, 'r"tl_test_fragments_bundled_([2-9]|[1-9][0-9]+)[.]py\\Z"', 'r"tl_test_fragments_bundled_([2-9])[.]py\\Z"')],
}
LAT3 = "        bien = (lat(lambda n: 0), lat(lambda n: n // 2), lat(lambda n: n - 1),     # giữ độ dài: đầu | giữa | cuối\n"
NOI_CAT = '                lambda d: d + b"#", lambda d: d[:-1],                              # đổi độ dài: nối | cắt\n'
BASE_DONG = '                lambda d: d + b"# sua\\n",                                         # nhiễu loạn của BASE (nối dòng trọn) — giữ nguyên\n'
CRLF = '                lambda d: d.replace(b"\\n", b"\\r\\n", 1))                          # kết thúc dòng: LF -> CRLF\n'
DOI = NOI_CAT + BASE_DONG + CRLF
QUYET = 'return quyet(rc, j) == (2, False, "stale", _STALE) and truong(j) == [_bam(e), _bam(a), len(e), len(a)]'
GAN_OK = """        if type(n) is ast.Assign and [type(t) for t in n.targets] == [ast.Name] and n.targets[0].id in (_SRC, _SHA):
            gan.setdefault(n.targets[0].id, ast.literal_eval(n.value))
"""
CHOT = {  # gỡ TỪNG chốt của bản vá (văn bản theo va.py r3)
    "go_ho_doi_do_dai": [(FR, DOI, "                )\n")],
    "go_nhieu_loan_base": [(FR, BASE_DONG, "")],
    "go_ho_giu_do_dai": [(FR, LAT3, "        bien = (\n")],
    "go_moi_vi_tri_mot_fixture": [(FR, LAT3, "        bien = (lambda d: lat(lambda n: 0)(lat(lambda n: n // 2)(lat(lambda n: n - 1)(d))),\n")],
    "go_bon_truong_quyet_dinh": [(FR, QUYET, QUYET.replace('quyet(rc, j) == (2, False, "stale", _STALE)', 'j.get("error") == _STALE'))],
    "go_bon_truong_bam": [(FR, QUYET, 'return quyet(rc, j) == (2, False, "stale", _STALE)')],
    "go_lan_dau_thang": [(FR, "            gan.setdefault(n.targets[0].id, ast.literal_eval(n.value))\n",
                          "            gan[n.targets[0].id] = ast.literal_eval(n.value)\n")],
    "go_phep_gan_chuan": [(FR, GAN_OK, """        for t in getattr(n, "targets", [getattr(n, "target", None)]):
            if isinstance(t, ast.Name):
                gan.setdefault(t.id, ast.literal_eval(n.value))
""")],
    "go_lac_hai_chu_so": [(FR, "        return all([mot_lac(ten) for ten in (_M9, _M10)])\n",
                           "        return all([mot_lac(ten) for ten in (_M9,)])\n")],
    "go_moi_lac_mot_fixture": [(FR, "            mods, dia, rc, j = cong(ba, lambda s: (s / ten).write_bytes(b\"x = 0\\n\"))\n",
                                "            mods, dia, rc, j = cong(ba, lambda s: [(s / n).write_bytes(b\"x = 0\\n\") for n in (_M9, _M10)])\n"),
                               (FR, "and lac == [ten] and", "and ten in lac and")],
}


def sub(*names):
    out = []
    for n in names:
        out += list(R2.get(n) or CHOT.get(n) or RV3.get(n) or RV4.get(n) or M[n])
    return out


NEW = [
    ("r11_size_only", (24, 27), sub("size-only")),
    ("r11_size_only_raw", (24, 25, 27, 32), sub("size-only-raw")),
    ("r11_one_stale_ok", (27,), sub("one-stale-ok")),
    ("r11_ann_empty", (8,), sub("ann-empty")),
    ("r11_duplicate", (8,), sub("duplicate")),
    ("r11_missing_ok_narrow", (26,), sub("missing-ok-narrow")),
    ("r11_missing_ok", (26, 32), sub("missing-ok")),
    ("r11_missing_status", (26,), sub("missing-status")),
    ("r11_stale_rc1", (23, 24, 25, 26, 27), sub("stale-rc1")),
    ("r11_stale_status_current", (23, 24, 25, 27), sub("stale-status-current")),
    ("r11_extra_ok", (23,), sub("extra-ok")),
    ("r11_absent_ok", (25, 32), sub("absent-ok")),
    ("r11_absent_status", (25,), sub("absent-status")),
    ("r11_extra_status", (23,), sub("extra-status")),
    ("r11_stale_sha_swap", (24, 27), sub("stale-sha-swap")),
    ("r11_stale_flip_only_firstbyte", (24, 27), sub("stale-flip-only-firstbyte")),
    ("r11_stale_ignore_lastbyte_region", (24, 27), sub("stale-ignore-lastbyte-region")),
    ("r11_stale_head_only", (24, 27), sub("stale-head-only")),
    ("r11_stale_tail_only", (24, 27), sub("stale-tail-only")),
    ("r11_stale_sha_len_cmp", (24, 27), sub("stale-sha-len-cmp")),
    ("r11_m1_chi_so_tien_to", (24, 27), sub("m1")),
    ("r11_m2_chap_nhan_cat_cut", (24, 27), sub("m2")),
    ("r11_m3_chuan_hoa_crlf", (24, 27), sub("m3")),
    ("r11_m4_stale_expected_sha_sai", (24, 27), sub("m4")),
    ("r11_m5_stale_expected_bytes_sai", (24, 27), sub("m5")),
    ("r11_m6_stale_actual_bytes_sai", (24, 27), sub("m6")),
    ("r11_m7_doc_toi_da_len_ky_vong", (24, 27), sub("m7")),
    ("r11_m8_regex_lac_mot_chu_so", (23,), sub("m8")),
    ("r11_rv3_bo_qua_dong_tron_noi_them", (24, 27), sub("rv_p1_bo_qua_dong_tron_ven_noi_them")),
    ("r11_rv3_bo_qua_chu_thich_cuoi_tep", (24, 27), sub("rv_p1_bo_qua_chu_thich_cuoi_tep")),
    ("r11_rv3_sources_annassign_gia_tri", (1, 2, 3, 4, 5, 6, 8), sub("rv_manh_chinh_sources_annassign_gia_tri")),
    ("r11_rv3_manh_phu_hai_docstring", (8,), sub("rv_manh_phu_hai_docstring")),
    ("r11_rv3_shards_truoc_sources", (8,), sub("rv_manh_chinh_shards_truoc_sources")),
    # review r4: rác hình dạng chỉ ở mảnh MỘT fragment (gói lech/lon) — base giết qua V5/V6, nay V8 soi mọi gói
    ("r11_rv4_s1_manh_don_trung_sources", (8,), sub("s1_manh_don_trung_SOURCES_sau_rong")),
    ("r11_rv4_s2_manh_don_gan_khong_literal", (8,), sub("s2_manh_don_gan_khong_literal")),
    ("r11_rv4_s3_manh_don_annassign_rong", (8,), sub("s3_manh_don_annassign_rong")),
    ("r11_rv4_s4_manh_don_augassign_sources", (8,), sub("s4_manh_don_augassign_SOURCES")),
    ("r11_rv4_s5_manh_qua_co_trung_sources", (8,), sub("s5_manh_qua_co_trung_SOURCES")),
    ("r11_rv4_s6_phi_ascii_annassign", (8,), sub("s6_phi_ascii_annassign")),
    ("r11_rv4_s7_manh_don_for_loop", (8,), sub("s7_manh_don_for_loop")),
    ("r11_rv4_g1_cong_bo_qua_noi_dong_chu_thich", (24, 27), sub("g1_cong_bo_qua_noi_dong_chu_thich")),
    ("r11_rv4_g2_missing_bao_stale", (26,), sub("g2_missing_bao_stale")),
    ("r11_rv4_g3_extra_chi_khi_khong_lech", (23,), sub("g3_extra_chi_khi_khong_lech")),
    # NỢ (Q7, E1 chốt phạm vi): đột biến SỐNG trên cả base lẫn bản vá, ghi nhận bằng đích RỖNG.
    # Ai đóng nợ thì ca này SAI ⇒ phải khai lại đích, nên nợ không biến mất trong im lặng.
    ("no_hai_manh_hong_ok", (), sub("rv_hai_manh_hong_ok")),
    ("no_trao_noi_dung_giua_manh", (), sub("rv_trao_noi_dung_giua_manh")),
    ("no_hai_lac_ok", (), sub("rv_hai_lac_ok")),
    ("no_lac_chi_bao_dau", (), sub("rv_lac_chi_bao_dau")),
    ("no_lac_mot_manh_bo_qua", (), sub("rv_lac_mot_manh_bo_qua")),
    ("no_lac_symlink_bo_qua", (), sub("rv_lac_symlink_bo_qua")),
    ("no_thieu_chinh_nhieu_manh_bao_stale", (), sub("rv_thieu_chinh_nhieu_manh_bao_stale")),
    ("no_vung_mu_1_den_giua", (), sub("rv_vung_mu_1_den_giua")),
    ("no_thieu_phu_actual_bytes_sai", (), sub("rv_thieu_phu_actual_bytes_sai")),
    ("no_generator_loi_thanh_ok", (), sub("rv_generator_loi_thanh_ok")),
    ("no_regex_toi_da_hai_chu_so", (), sub("rv_regex_toi_da_hai_chu_so")),
    ("no_regex_hai_chu_so_chi_1x", (), sub("rv_regex_hai_chu_so_chi_1x")),
    ("no_manh_phu_sources_la_list", (), sub("rv_manh_phu_sources_la_list")),
    # A3: gỡ TỪNG chốt. Một mình ⇒ xanh; kèm đột biến đích ⇒ đột biến SỐNG (đích rỗng) hoặc lan rộng.
    ("a7_go_ho_doi_do_dai", (), sub("go_ho_doi_do_dai")),
    ("a7_go_ho_doi_do_dai__m7_song", (), sub("go_ho_doi_do_dai", "m7")),
    ("a7_go_ho_giu_do_dai", (), sub("go_ho_giu_do_dai")),
    ("a7_go_ho_giu_do_dai__size_only_song", (), sub("go_ho_giu_do_dai", "size-only")),
    ("a7_go_moi_vi_tri_mot_fixture", (), sub("go_moi_vi_tri_mot_fixture")),
    ("a7_go_moi_vi_tri__head_only_song", (), sub("go_moi_vi_tri_mot_fixture", "stale-head-only")),
    ("a7_go_bon_truong_quyet_dinh", (), sub("go_bon_truong_quyet_dinh")),
    ("a7_go_bon_truong_quyet_dinh__one_stale_ok_song", (), sub("go_bon_truong_quyet_dinh", "one-stale-ok")),
    ("a7_go_bon_truong_bam", (), sub("go_bon_truong_bam")),
    ("a7_go_bon_truong_bam__m6_song", (), sub("go_bon_truong_bam", "m6")),
    ("a7_go_lan_dau_thang", (), sub("go_lan_dau_thang")),
    ("a7_go_lan_dau_thang__duplicate_lan", (4, 5, 6, 8), sub("go_lan_dau_thang", "duplicate")),
    ("a7_go_phep_gan_chuan", (), sub("go_phep_gan_chuan")),
    ("a7_go_phep_gan_chuan__ann_empty_van", (4, 5, 6, 8, 9), sub("go_phep_gan_chuan", "ann-empty")),
    ("a7_go_lac_hai_chu_so", (), sub("go_lac_hai_chu_so")),
    ("a7_go_lac_hai_chu_so__m8_song", (), sub("go_lac_hai_chu_so", "m8")),
    ("a7_go_nhieu_loan_base", (), sub("go_nhieu_loan_base")),
    ("a7_go_nhieu_loan_base__dong_tron_song", (), sub("go_nhieu_loan_base", "rv_p1_bo_qua_dong_tron_ven_noi_them")),
    ("a7_go_moi_lac_mot_fixture", (), sub("go_moi_lac_mot_fixture")),
    ("a7_go_moi_lac_mot_fixture__extra_ok_song", (), sub("go_moi_lac_mot_fixture", "extra-ok")),
]
VAN_CO_Y = {"r11_size_only_raw", "r11_missing_ok", "r11_absent_ok", "a7_go_phep_gan_chuan__ann_empty_van"}
KV = sorted(t for t, _, _ in NEW if t not in VAN_CO_Y)

src = src.replace('"""Ma tran dot bien N2 (dac ta r4)',
                  '"""Ma tran dot bien A2 cua BUNDLED-GATE-ORACLE-FRESHNESS r5 = ma tran g5 (bf38a110, 49; khai lai dich f05 V8,V9 · v28 V24,V28 · f01 V5,V31)\n'
                  '+ %d dot bien lop F10/F11 (r11_) + %d ca no ghi nhan (no_) + %d ca go chot (a7_). Sinh boi gen_ma_tran.py.\nGoc: ma tran dot bien N2 (dac ta r4)'
                  % (sum(t.startswith("r11_") for t, _, _ in NEW), sum(t.startswith("no_") for t, _, _ in NEW), sum(t.startswith("a7_") for t, _, _ in NEW)), 1)
for old, new in (('("f05_manh_1_gan_nhieu_dich", (8,),', '("f05_manh_1_gan_nhieu_dich", (8, 9),'),
                 ('("v28_bam_nhieu_manh_bo_ten", (28,),', '("v28_bam_nhieu_manh_bo_ten", (24, 28),'),
                 ('("f01_dem_ky_tu_thay_vi_byte", (5,),', '("f01_dem_ky_tu_thay_vi_byte", (5, 31),')):
    assert src.count(old) == 1, old
    src = src.replace(old, new)
end = src.index("\n]\nRUN = r'''")
src = src[:end] + "\n" + "\n".join(" (%r, %r, %r)," % x for x in NEW) + src[end:]
src = src.replace('print("KQ " + json.dumps({"run": r, "kq": m._KQ}))',
                  'print("KQ " + json.dumps({"run": r, "kq": m._KQ, "ly_do": m._LY_DO}))')
# R5: moi khoa V1-V32 phai la dich cua >=1 dot bien DON dich (tinh tu chinh bang MUT, truoc khi chay)
src = src.replace("sai = 0\nfor ten, dich, subs in MUT:",
                  "KHONG_VANG = set(%r)\n"
                  "DON = {d[0] for _, d, _ in MUT if len(d) == 1}\n"
                  "thieu = [P[i] for i in range(1, 33) if i not in DON]\n"
                  "print(\"DON_DICH: %%d/32 khoa co dot bien don dich\" %% (32 - len(thieu)) + (\" THIEU=\" + \",\".join(thieu) if thieu else \"\"))\n"
                  "sai = len(thieu)\nfor ten, dich, subs in MUT:" % KV)
# khong ap duoc => SAI, chay tiep (khong dung ca script)
old = '''        for rel, a, b in subs:
            p = d / rel; s = p.read_text(encoding="utf-8")
            assert s.count(a) == 1 and a != b, (ten, a, s.count(a))
            p.write_text(s.replace(a, b), encoding="utf-8", newline="\\n")
'''
assert src.count(old) == 1, "khong thay vong ap"
src = src.replace(old, '''        khong_ap = None
        for rel, a, b in subs:
            p = d / rel; s = p.read_text(encoding="utf-8")
            if s.count(a) != 1 or a == b:
                khong_ap = (rel, s.count(a)); break
            p.write_text(s.replace(a, b), encoding="utf-8", newline="\\n")
        if khong_ap:
            sai += 1; print("SAI " + ten, "KHONG_AP_DUOC", khong_ap); continue
''')
src = src.replace('dat = do == ky and j["run"] is (not dich) and len(j["kq"]) == 32',
                  'dat = do == ky and j["run"] is (not dich) and len(j["kq"]) == 32 and not (ten in KHONG_VANG and j.get("ly_do"))')
(H / "ma_tran_r11.py").write_text(src, encoding="utf-8", newline="\n")
print("so dot bien moi:", len(NEW), "tong:", src.count("\n ("))
