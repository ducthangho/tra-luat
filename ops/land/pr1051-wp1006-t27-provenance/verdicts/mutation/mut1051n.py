"""Đột biến các chốt của #1051 lượt 6 (ngữ pháp cho phép); mỗi cái phải làm ca đích ĐỎ. Chạy trên bản sao tạm."""
import shutil, subprocess, sys, tempfile
from pathlib import Path
KHO = Path(sys.argv[1])
CA = "t27_phan_chung_ten_bien_nhan_sai"
NL = chr(10)
BS = chr(92)
DOT_BIEN = [
    ("bo_chot_duoi", "if bien_nhan and not p.name.endswith(DUOI_BIEN_NHAN):", "if False:"),
    ("bo_chot_ten", 'if _ten_tep(f"`{p.name}`") != {p.name}:', "if False:"),
    ("bo_goi_t27_bien_nhan", "    _doi_ten_hop_le(ds)" + NL + "    _doi_ten_hop_le(ds_verdict, bien_nhan=False)" + NL,
     "    _doi_ten_hop_le(ds_verdict, bien_nhan=False)" + NL),
    ("bo_goi_t27_verdict", "    _doi_ten_hop_le(ds_verdict, bien_nhan=False)" + NL, ""),
    ("bo_goi_t26", "    _doi_ten_hop_le(ds)" + NL + "    for p in ds:", "    for p in ds:"),
    ("sidecar_khong_phan_biet", 'bn = next((p for p in ds if p.name == f"{f.stem}{DUOI_BIEN_NHAN}"), None)',
     'bn = next((p for p in ds if p.name.lower() == f"{f.stem}{DUOI_BIEN_NHAN}".lower()), None)'),
    ("bo_IGNORECASE", "                     re.IGNORECASE)" + NL + "    o = o.strip(\" " + BS + "t\")", ")" + NL + "    o = o.strip(\" " + BS + "t\")"),
    ("anh_thanh_link", "    o = o.strip(\" " + BS + "t\")" + NL + "    ra, i = set(), 0", "    o = o.strip(\" " + BS + "t\")" + '.lstrip("!")' + NL + "    ra, i = set(), 0"),
    ("bo_luat_nhan", "            if not (nhan == co_so or", "            if False and (nhan == co_so or"),
    ("nhan_cham_bat_ky", "                                      and co_so.endswith(nhan))):", "                                      )):"),
    ("dinh_sau_van_nhan", "            return set()                    # ký tự dính sau mục", "            return ra  # "),
    ("span_cho_khoang_trang", "    ten = r\"[" + BS + "w" + BS + "-][" + BS + "w." + BS + "-]*", "    ten = r\"[" + BS + "w" + BS + "-][" + BS + "w. " + BS + "-]*"),
    ("bo_giu_span", "        if giu_span:" + NL + "            o = tho", "        if False:" + NL + "            o = tho"),
    ("id_dung_split", 'ma in _id_hien_thi(h.get(k_cb_id, ""))', 'ma in {x.strip().strip("`") for x in h.get(k_cb_id, "").split()}'),
    ("dong_trong_unicode", '        if re.fullmatch(r"[ ' + BS + 't]*", dong):', '        if not dong.strip():'),
    ("rao_info_co_nhay", 'if m and m.group(1)[0] == "`" and "`" in dong[m.end():] and rao is None:', 'if False:'),
    ("rao_dong_unicode", 're.fullmatch(r"[ ' + BS + 't]*", dong[m.end():])', 'not dong[m.end():].strip()'),
    ("tach_o_bo_thoat", 're.split(r"(?<!' + BS + BS + ')' + BS + '|", d)', 'd.split("|")'),
    ("muc_luc_basename", "        return vp[len(goc_tm):] if vp.startswith(goc_tm) else vp", "        return PurePosixPath(vp).name"),
    ("canh_bao_khong_basename", '            ten_cb.add(PurePosixPath(ten_verdict).name)', '            pass'),
    ("basename_khong_duy_nhat", 'dem_co_so.get(PurePosixPath(ten_verdict).name) == 1', 'True'),
    ("dinh_danh_chi_ds_verdict", "    dinh_danh = {duong_verdict(d) for _, d in du_lieu} | {f.name for f in ds_verdict}",
     '    dinh_danh = {duong_verdict(d) for _, d in du_lieu if "/" in duong_verdict(d)} | {f.name for f in ds_verdict}'),
    ("bo_cam_comment", 'bang("' + BS + 'x01" not in dong,', 'bang(True or "' + BS + 'x01" not in dong,'),
    ("tach_dong_splitlines", 'return re.split(r"' + BS + 'r' + BS + 'n|' + BS + 'r|' + BS + 'n", x)', 'return x.splitlines()'),
    ("rao_thut_bat_ky", 'm = re.match(r"^ {0,3}(`{3,}|~{3,})", dong)', 'm = re.match(r"^' + BS + 's*(`{3,}|~{3,})", dong)'),
    ("bo_cam_html", 'bang(not re.match(r"^ {0,3}<[A-Za-z/?!]", dong),', 'bang(True or not re.match(r"^ {0,3}<[A-Za-z/?!]", dong),'),
    ("tieu_de_khong_thut", 'tieu = re.match(r"^ {0,3}(#{1,6})', 'tieu = re.match(r"^(#{1,6})'),
    ("bo_setext", "            lay = False                                    # tiêu đề setext", "            pass  # "),
    ("bo_trong_doan", "            if trong_doan:" + NL + "                continue                                   # dính", "            if False:" + NL + "                continue                                   # dính"),
    ("gach_bat_ky", 'all(re.fullmatch(r":?-+:?", x) for x in o)', 'all(x and set(x) <= set("-: ") for x in o)'),
    ("bo_cam_thut_le", 'bang(dong.startswith("|"), f"mục', 'bang(True, f"mục'),
    ("gach_khong_dem_o", "if la_gach(dong) and len(_tach_o(dong)) == len(dau_bang):", "if la_gach(dong):"),
    ("nhan_tran", "(?P<nhan>`[^`" + BS + "[" + BS + "]]+`)" + BS + "]", "(?P<nhan>`[^`" + BS + "[" + BS + "]]+`|[^`" + BS + "[" + BS + "]]+)" + BS + "]"),
    ("id_phan_cach_rong", "(?:(?:[ " + BS + "t]*,[ " + BS + "t]*|[ " + BS + "t]+)`", "(?:[ " + BS + "t]*,?[ " + BS + "t]*`"),
    ("tach_o_strip_unicode", "    d = dong.strip(TRANG)", "    d = dong.strip()"),
    ("o_strip_unicode", '.strip(TRANG) for x in re.split', '.strip() for x in re.split'),
    ("trang_vt_ff", '    TRANG = " ' + BS + 't"', '    TRANG = " ' + BS + 't' + BS + 'x0b' + BS + 'x0c"'),
    ("tieu_de_chuoi_con", "== 2 and chu in {tieu_de,", "== 2 and tieu_de in dong or None and chu in {tieu_de,"),
    ("tien_to_nhom_So", 'chu in {tieu_de, "' + BS + 'u26a0 " + tieu_de}', '(chu.endswith(tieu_de) and all(c in " " or __import__("unicodedata").category(c) in ("So", "Sc") for c in chu[:-len(tieu_de)]))'),
]
goc = (KHO / "ops/lease_publish_test.py").read_text(encoding="utf-8")
for ten, tu, sang in [("doi_chung", "", "")] + DOT_BIEN:
    with tempfile.TemporaryDirectory() as t:
        ban = Path(t) / "kho"
        shutil.copytree(KHO / "ops", ban / "ops", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(KHO / ".claude", ban / ".claude", ignore=shutil.ignore_patterns("__pycache__"))
        s = goc
        if tu:
            if s.count(tu) != 1:
                print(f"[{ten}] NEO SAI count={s.count(tu)}", flush=True); continue
            s = s.replace(tu, sang)
        (ban / "ops/lease_publish_test.py").write_text(s, encoding="utf-8")
        r = subprocess.run([sys.executable, "-B", "ops/lease_publish_test.py", f"--chi-ca={CA}"],
                           cwd=ban, capture_output=True, text=True, timeout=900)
        out = r.stdout + r.stderr
        dong = [x for x in out.splitlines() if "ĐỎ" in x[:6] or x.startswith("lease_publish:")]
        print(f"[{ten}] rc={r.returncode} :: " + " || ".join(d[:170] for d in dong), flush=True)
