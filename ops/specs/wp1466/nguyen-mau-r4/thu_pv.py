import pathlib, subprocess, sys
N = "../r2/cay0/.claude/dev/"; che_do = sys.argv[1]
h = pathlib.Path("cay/.claude/dev/" + ("packet_loop.py" if che_do == "ma" else "packet_loop_test.py")).read_text(encoding="utf-8")
dem = [0, 0]
def thu(ten, s, doi):
    pathlib.Path(f"tmp_{che_do}.py").write_text(s, encoding="utf-8")
    r = subprocess.run([sys.executable, "-B", "do_pham_vi.py", che_do, N + ("packet_loop.py" if che_do == "ma" else "packet_loop_test.py"), f"tmp_{che_do}.py"], capture_output=True, text=True)
    ok = (r.returncode == 0) == doi; dem[ok] += 1
    print(f"{'OK ' if ok else 'SAI'} {che_do:4s} {ten:36s} rc={r.returncode} {r.stdout.strip().splitlines()[-1][:74]}", flush=True)
def R(s, a, b): assert s.count(a) >= 1, a[:40]; return s.replace(a, b, 1)
if che_do == "ma":
    i = h.index("# --- ADR-0068: bảy đơn vị khoá"); moc = "def cmd_doctrine_scan(a, state_dir: Path) -> int:\n"
    thu("pass_cuoi_ham_cu_sat_khoi_chen", h[:i].rstrip("\n") + "\n    pass\n\n\n" + h[i:], False)
    thu("gan_nhieu_dich_co_ten_cu", R(h, moc, "INV_X = RC_ADR = 9\n\n\n" + moc), False)
    thu("gan_bo_co_ten_cu", R(h, moc, "INV_A, RC_ADR = 1, 9\n\n\n" + moc), False)
    thu("import_de_ten_cu", R(h, moc, "import os as RC_ADR\n\n\n" + moc), False)
    thu("pass_trong_cmd_adr_song", R(h, "def cmd_adr_song(a, state_dir: Path) -> int:\n", "def cmd_adr_song(a, state_dir: Path) -> int:\n    pass\n"), False)
    thu("pass_cuoi_cmd_doctrine_scan", R(h, "    return RC_OK\n\n\n# --- adr-song", "    pass\n    return RC_OK\n\n\n# --- adr-song"), False)
    thu("ham_moi_ten_la", R(h, moc, "def ham_la():\n    return 1\n\n\n" + moc), False)
    thu("cau_lenh_moi_khong_ten", R(h, moc, "print('x')\n\n\n" + moc), False)
    thu("ham_ho_inv_sai_vi_tri", h + "\n\ndef _inv_them():\n    return 1\n", False)
    thu("comment_roi_giua_ham_cu", R(h, "\n\ndef _die(", "\n# lạ\n\ndef _die("), False)
    thu("doi_comment_trong_ham_cu", R(h, "    # `proto_words` luôn khác rỗng", "    # `proto_words` luôn  khác rỗng"), False)
    thu("sua_hang_chuoi_khac_trong_parser", R(h, '"Cưỡng chế vài stop condition của work packet bằng mã thoát. "', '"Cưỡng chế vài stop condition của work packet bằng mã thoát.  "'), False)
    thu("ham_ho_inv_dung_vi_tri (dat)", R(h, moc, "def _inv_them():\n    return 1\n\n\n" + moc), True)
else:
    cuoi = "\n\nif __name__ =="
    thu("pass_trong_ca_cu", R(h, "def case_doctrine_scan_sach_xanh(c: Ctx):\n", "def case_doctrine_scan_sach_xanh(c: Ctx):\n    pass\n"), False)
    thu("sua_mot_dot_bien_cu", R(h, '"r1187_drop_doc_guard"] = (\'        if s == "0063":\'', '"r1187_drop_doc_guard"] = (\'        if s == "0063": \''), False)
    thu("sua_them_trong_repo_gia", R(h, "    (r / \"docs\").mkdir(parents=True, exist_ok=True)\n    (r / \"docs\" / \"PROTOCOL_DA_PHIEN.md\").write_text(\n", "    (r / \"docs\").mkdir(parents=True, exist_ok=True)\n    pass\n    (r / \"docs\" / \"PROTOCOL_DA_PHIEN.md\").write_text(\n"), False)
    thu("gan_lai_ham_cu", R(h, cuoi, "\n_doi = lambda *a: None\n\n" + cuoi), False)
    thu("gan_nhieu_dich_co_ten_cu", R(h, cuoi, "\n_INV_Y = ROOT = ROOT\n\n" + cuoi), False)
    thu("cau_lenh_vo_danh_la", R(h, cuoi, "\nos.environ['X'] = '1'\n\n" + cuoi), False)
    thu("them_mot_ca_moi (dat)", R(h, cuoi, "\nCASES.append((\"doctrine_inv_them\", _inv_ca(lambda g: g + 'x', 0)))\n\n" + cuoi), True)
print(f"TONG {che_do}: dung {dem[1]} sai {dem[0]}")
