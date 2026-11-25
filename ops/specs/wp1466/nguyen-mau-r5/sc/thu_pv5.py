"""Ma trận biến thể N8 (r5). Dùng: python -B thu_pv5.py <thư mục r5b> ma|test [số tiến trình].

Ba nguồn biến thể, mỗi biến thể ghi nguồn của nó:
  r4    — 13 (ma) + 7 (test) biến thể của `nguyen-mau-r4/thu_pv.py`, chép lại với mốc của nguyên mẫu r5;
  rv4   — các biến thể độc lập của reviewer lượt 4 (`review/r4-l4/evidence-n8_run.py`), chép nguyên văn phần chèn;
  r5    — đường vào cùng cơ chế do người soạn r5 tự liệt kê (gán ở phạm vi module qua phần mới, hay đổi bản ghi sổ).
"""
import concurrent.futures, json, pathlib, subprocess, sys, time
S, che_do = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2]
so_tt = int(sys.argv[3]) if len(sys.argv) > 3 else 3
tep = "packet_loop.py" if che_do == "ma" else "packet_loop_test.py"
h = (S / "cay/.claude/dev" / tep).read_text(encoding="utf-8")
nen = S / "n8" / ("nen-" + tep)
ra = S / "n8" / che_do
ra.mkdir(parents=True, exist_ok=True)
V = []
def thu(nguon, ten, s, doi):
    V.append((nguon, ten, s, doi))
def R(s, a, b):
    assert s.count(a) >= 1, a[:60]
    return s.replace(a, b, 1)
if che_do == "ma":
    i = h.index("# --- ADR-0068: bảy đơn vị khoá"); moc = "def cmd_doctrine_scan(a, state_dir: Path) -> int:\n"
    them = lambda x: R(h, moc, x + "\n\n\n" + moc)  # noqa: E731
    # --- r4 (13)
    thu("r4", "pass_cuoi_ham_cu_sat_khoi_chen", h[:i].rstrip("\n") + "\n    pass\n\n\n" + h[i:], False)
    thu("r4", "gan_nhieu_dich_co_ten_cu", them("INV_X = RC_ADR = 9"), False)
    thu("r4", "gan_bo_co_ten_cu", them("INV_A, RC_ADR = 1, 9"), False)
    thu("r4", "import_de_ten_cu", them("import os as RC_ADR"), False)
    thu("r4", "pass_trong_cmd_adr_song", R(h, "def cmd_adr_song(a, state_dir: Path) -> int:\n", "def cmd_adr_song(a, state_dir: Path) -> int:\n    pass\n"), False)
    thu("r4", "pass_cuoi_cmd_doctrine_scan", R(h, "    return RC_OK\n\n\n# --- adr-song", "    pass\n    return RC_OK\n\n\n# --- adr-song"), False)
    thu("r4", "ham_moi_ten_la", them("def ham_la():\n    return 1"), False)
    thu("r4", "cau_lenh_moi_khong_ten", them("print('x')"), False)
    thu("r4", "ham_ho_inv_sai_vi_tri", h + "\n\ndef _inv_them():\n    return 1\n", False)
    thu("r4", "comment_roi_giua_ham_cu", R(h, "\n\ndef _die(", "\n# lạ\n\ndef _die("), False)
    thu("r4", "doi_comment_trong_ham_cu", R(h, "    # `proto_words` luôn khác rỗng", "    # `proto_words` luôn  khác rỗng"), False)
    thu("r4", "sua_hang_chuoi_khac_trong_parser", R(h, '"Cưỡng chế vài stop condition của work packet bằng mã thoát. "', '"Cưỡng chế vài stop condition của work packet bằng mã thoát.  "'), False)
    thu("r4", "ham_ho_inv_dung_vi_tri (dat)", them("def _inv_them():\n    return 1"), True)
    # --- rv4 (6, chép nguyên văn phần chèn của reviewer)
    thu("rv4", "new_function_default_binding", them("def _inv_probe(x=(RC_ADR := RC_ADR)):\n    return x"), False)
    thu("rv4", "new_function_annotation_binding", them("def _inv_probe(x: (RC_ADR := RC_ADR)):\n    return x"), False)
    thu("rv4", "new_function_decorator_binding", them("@(_INV_identity := (lambda f: f))\n@((RC_ADR := RC_ADR) and _INV_identity)\ndef _inv_probe():\n    return None"), False)
    thu("rv4", "new_class_body_binding", them("class _inv_probe:\n    global RC_ADR\n    RC_ADR = RC_ADR"), False)
    thu("rv4", "except_binding", them("try:\n    pass\nexcept Exception as RC_ADR:\n    pass\n_INV_probe = None"), False)
    thu("rv4", "old_function_decorator", R(h, moc, "@staticmethod\n" + moc), False)
    # --- r5: mọi đường vào "phần mới gán hay đổi tên cũ ở phạm vi module", và chỗ chèn được phép
    thu("r5", "lambda_mac_dinh_walrus", them("_INV_X = lambda a=(RC_ADR := RC_ADR): a"), False)
    thu("r5", "lambda_mac_dinh_ten", them("_INV_X = lambda a=RC_ADR: a"), False)
    thu("r5", "gan_goi_ham", them("_INV_X = setattr(sys.modules[__name__], 'RC_ADR', 9)"), False)
    thu("r5", "gan_comprehension_walrus", them("_INV_X = [(RC_ADR := 9) for _ in ()]"), False)
    thu("r5", "gan_co_chu_thich", them("_INV_X: int = 1"), False)
    thu("r5", "gan_tang_ten_cu", them("RC_ADR += 0"), False)
    thu("r5", "ham_moi_global_trong_than", them("def _inv_f():\n    global RC_ADR\n    RC_ADR = 0"), False)
    thu("r5", "ham_moi_global_long", them("def _inv_f():\n    def g():\n        global RC_ADR\n        RC_ADR = 0\n    return g"), False)
    thu("r5", "ham_moi_mac_dinh_ten_cu", them("def _inv_f(x=RC_ADR):\n    return x"), False)
    thu("r5", "ham_async_moi", them("async def _inv_f():\n    return 1"), False)
    thu("r5", "lop_moi_khong_global", them("class _InvC:\n    pass"), False)
    thu("r5", "def_trong_if", them("if True:\n    def RC_ADR():\n        return 9\n    _INV_X = 1"), False)
    thu("r5", "for_dich_ten_cu", them("for RC_ADR in (9,):\n    _INV_X = 1"), False)
    thu("r5", "with_as_ten_cu", them("with open(__file__) as RC_ADR:\n    _INV_X = 1"), False)
    thu("r5", "match_bat_ten_cu", them("match 9:\n    case RC_ADR:\n        _INV_X = 1"), False)
    thu("r5", "del_ten_cu", them("del RC_ADR"), False)
    thu("r5", "kieu_type_alias", them("type _INV_T = int"), False)
    thu("r5", "chen_global_trong_doctrine_scan", R(h, "    loi_inv = _inv_kiem_protocol(root)\n", "    global _die\n    loi_inv = _inv_kiem_protocol(root)\n"), False)
    thu("r5", "chen_gan_bien_cu", R(h, "    loi_inv = _inv_kiem_protocol(root)\n", "    loi_inv = _inv_kiem_protocol(root)\n    muc_tieu = []\n"), False)
    thu("r5", "chen_doi_ten_bien", R(h, "    loi_inv = _inv_kiem_protocol(root)\n    if loi_inv:\n        for x in loi_inv:", "    loi_inv = _inv_kiem_protocol(root)\n    if loi_inv:\n        for y in loi_inv:"), False)
    thu("r5", "chen_doi_loi_nhan (dat)", R(h, "doctrine-scan: {x}", "doctrine-scan:  {x}"), True)
    thu("r5", "hang_moi_dung_ho (dat)", them("_INV_THEM = (1, 'a', {'k': [2, 3]})"), True)
    thu("r5", "ham_moi_mac_dinh_hang (dat)", them("def _inv_g(a, b=1, *, c=None):\n    global_ = a\n    return global_"), True)
else:
    cuoi = "\n\nif __name__ =="
    them = lambda x: R(h, cuoi, "\n" + x + "\n\n" + cuoi)  # noqa: E731
    # --- r4 (7)
    thu("r4", "pass_trong_ca_cu", R(h, "def case_doctrine_scan_sach_xanh(c: Ctx):\n", "def case_doctrine_scan_sach_xanh(c: Ctx):\n    pass\n"), False)
    thu("r4", "sua_mot_dot_bien_cu", R(h, '"r1187_drop_doc_guard"] = (\'        if s == "0063":\'', '"r1187_drop_doc_guard"] = (\'        if s == "0063": \''), False)
    thu("r4", "sua_them_trong_repo_gia", R(h, "    (r / \"docs\").mkdir(parents=True, exist_ok=True)\n    (r / \"docs\" / \"PROTOCOL_DA_PHIEN.md\").write_text(\n", "    (r / \"docs\").mkdir(parents=True, exist_ok=True)\n    pass\n    (r / \"docs\" / \"PROTOCOL_DA_PHIEN.md\").write_text(\n"), False)
    thu("r4", "gan_lai_ham_cu", them("_doi = lambda *a: None"), False)
    thu("r4", "gan_nhieu_dich_co_ten_cu", them("_INV_Y = ROOT = ROOT"), False)
    thu("r4", "cau_lenh_vo_danh_la", them("os.environ['X'] = '1'"), False)
    thu("r4", "them_mot_ca_moi (dat)", them("CASES.append((\"doctrine_inv_them\", _inv_ca(lambda g: g + 'x', 0)))"), True)
    # --- rv4 (2)
    thu("rv4", "new_function_default_binding", R(h, cuoi, "\ndef _inv_probe(x=(ROOT := ROOT)):\n    return x\n" + cuoi), False)
    thu("rv4", "new_function_decorator_binding", R(h, cuoi, "\n@(_INV_identity := (lambda f: f))\n@((ROOT := ROOT) and _INV_identity)\ndef _inv_probe():\n    return None\n" + cuoi), False)
    # --- r5
    thu("r5", "so_walrus_trong_comprehension", them("CASES += [(ROOT := ROOT) for _ in ()]"), False)
    thu("r5", "so_walrus_mac_dinh_lambda", them("CASES += [(\"doctrine_inv_z\", lambda c, _=(ROOT := ROOT): None)]"), False)
    thu("r5", "so_gan_chi_so", them("MUTANTS[\"inv_z\"] = (\"a\", \"b\", [])"), False)
    thu("r5", "so_gan_chi_so_cases", them("CASES[0] = CASES[0]"), False)
    thu("r5", "so_chen_dau", them("CASES.insert(0, CASES[0])"), False)
    thu("r5", "so_gan_lai_ca_so", them("CASES = CASES + []"), False)
    thu("r5", "ham_moi_global", them("def _inv_z():\n    global ROOT\n    ROOT = ROOT"), False)
    thu("r5", "ham_moi_de_ten_dung_san", them("def len(x):\n    return 0"), False)
    thu("r5", "gan_moi_de_ten_dung_san", them("print = print"), False)
    thu("r5", "lop_moi", them("class _InvC:\n    pass"), False)
    thu("r5", "gan_goi_ham", them("_INV_Z = setattr(sys.modules[__name__], 'ROOT', ROOT)"), False)
    thu("r5", "ham_moi_ten_la (dat)", them("def _hoan_toan_moi_1466():\n    return 1"), True)
    thu("r5", "so_update (dat)", them("MUTANTS.update({\"inv_z\": (\"a\", \"b\", [])})"), True)
    thu("r5", "so_or_bang (dat)", them("MUTANTS_NHAM_TEST |= {\"inv_z\"}"), True)
def chay(v):
    nguon, ten, s, doi = v
    p = ra / (nguon + "-" + ten.split(" ")[0] + ".py")
    p.write_text(s, encoding="utf-8")
    t = time.time()
    r = subprocess.run([sys.executable, "-B", str(S / "sc/do_pham_vi.py"), che_do, str(nen), str(p)], capture_output=True, text=True)
    return dict(nguon=nguon, ten=ten, doi_dat=doi, rc=r.returncode, dung=(r.returncode == 0) == doi, out=r.stdout.strip().splitlines()[-1][:160] if r.stdout.strip() else r.stderr.strip()[-160:], giay=round(time.time() - t, 1))
with concurrent.futures.ThreadPoolExecutor(max_workers=so_tt) as ex:
    hang = list(ex.map(chay, V))
for x in hang:
    print(f"{'OK ' if x['dung'] else 'SAI'} {x['nguon']:4s} {x['ten']:40s} rc={x['rc']} {x['out']}", flush=True)
(S / "n8" / f"ket_qua_{che_do}.json").write_text(json.dumps(hang, ensure_ascii=False, indent=1))
for ng in ("r4", "rv4", "r5"):
    xs = [x for x in hang if x["nguon"] == ng]
    print(f"TONG {che_do} {ng}: {len(xs)} biến thể · đỏ {sum(x['rc'] != 0 for x in xs)} · đạt {sum(x['rc'] == 0 for x in xs)} · đúng kỳ vọng {sum(x['dung'] for x in xs)}")
print(f"TONG {che_do}: dung {sum(x['dung'] for x in hang)} sai {sum(not x['dung'] for x in hang)}")
