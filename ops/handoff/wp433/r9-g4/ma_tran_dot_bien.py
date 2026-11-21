"""Ma tran dot bien N2 (dac ta r4): moi dot bien chay tren BAN SAO cay (git ls-files), khong dung tep that.
Dung: python -B dotbien.py <repo>. Thoat 0 khi MOI dong tap do == tap dich khai, khong vang."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
TF, RL = "scripts/tl_core/test_fragments.py", "scripts/tl_core/release.py"
NHAN = tuple(f"V{i}" for i in range(1, 33))
P = {i + 1: n for i, n in enumerate(NHAN)}
LOAD_ALL = "sorted(p.name for p in path.parent.iterdir() if _BUNDLED_SHARD_NAME_RE.fullmatch(p.name)"
RENDER = r'''out.append((_bundled_shard_name(index), ("\n".join(body) + "\n").encode("utf-8")))'''
WRAP = "    return generate_bundled_modules(fragment_root, candidate_paths=candidate_paths)[0][1]\n"
CAT = "if groups[-1] and used + size > _BUNDLED_SHARD_LIMIT:"
ALLOW = "if targets not in (allowed if primary else allowed[:1]):"
SHCHK = "        if not shards or shards != expected:\n"
SO = "    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n"
MUT = [  # (ten, tap dich, [(tep, cu, moi)])
 ("doi_chung", (), []),
 ("v1_generator_mot_manh_them_LF_wrapper_bu_lai", (1,), [(TF, RENDER, RENDER.replace(r'+ "\n")', r'+ ("\n\n" if len(groups) == 1 else "\n"))')),
    (TF, WRAP, WRAP.replace("[0][1]", r'[0][1].rstrip(b"\n") + b"\n"'))]),
 ("v2_wrapper_mot_manh_them_LF", (2,), [(TF, WRAP, "    m = generate_bundled_modules(fragment_root, candidate_paths=candidate_paths)\n" + r'    return m[0][1] + (b"" if len(m) > 1 else b"\n")' + "\n")]),
 ("v3_mot_manh_nhieu_fragment_van_khai_shards", (3,), [(TF, "if index == 1 and len(groups) > 1:", "if index == 1 and (len(groups) > 1 or len(lines) > 1):")]),
 ("v4_dao_thu_tu_dong_trong_manh", (4,), [(TF, 'body = header + lines + [")"]', 'body = header + lines[::-1] + [")"]')]),
 ("v5_cat_khi_bang_han", (5,), [(TF, CAT, CAT.replace("> _BUNDLED", ">= _BUNDLED"))]),
 ("v5b_don_vi_byte_bo_LF", (5,), [(TF, 'size = len(line.encode("utf-8")) + 1', 'size = len(line.encode("utf-8"))')]),
 ("v6_hang_xom_ghep_vao_manh_qua_han", (6,), [(TF, "            used = 0\n", "            used = 0 if size <= _BUNDLED_SHARD_LIMIT else -size\n")]),
 ("v7_ten_manh_3_sai", (7,), [(TF, "out.append((_bundled_shard_name(index),", "out.append((_bundled_shard_name(index if index < 3 else index + 1),")]),
 ("v8_manh_1_them_phep_gan", (8,), [(TF, 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n', 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n            body.append("X = 0")\n')]),
 ("v9_khai_thieu_manh_cuoi", (9,), [(TF, "for k in range(2, len(groups) + 1)).rstrip()", "for k in range(2, len(groups))).rstrip()")]),
 ("v10_wrapper_tra_manh_cuoi", (10,), [(TF, WRAP, WRAP.replace("[0][1]", "[-1][1]"))]),
 ("v11_writer_ghi_sai_bytes_manh_phu", (11,), [(TF, "        (scripts / name).write_bytes(data)\n", r'        (scripts / name).write_bytes(data if name == _BUNDLED_MODULE_NAME else data + b"\n")' + "\n")]),
 ("v12_writer_khong_xoa_lac", (12,), [(TF, "            stale.unlink()\n", "            pass\n")]),
 ("v13_nap_them_tep_khong_khai", (13,), [(TF, "    for shard in shards:\n", f"    for shard in list(shards) + {LOAD_ALL} and p.name not in shards):\n")]),
 ("v14_manh_phu_thieu_ma_loi_khac", (14,), [(TF, '        raise FragmentReadError("BUNDLED_MODULE_MISSING", rel)\n', '        raise FragmentReadError("BUNDLED_MODULE_MISSING" if primary else "BUNDLED_MODULE_READ", rel)\n')]),
 ("v15_duong_manh_thieu_sai", (15,), [(TF, '    rel = _BUNDLED_RELATIVE_PATH if primary else f"scripts/{path.name}"\n', "    rel = _BUNDLED_RELATIVE_PATH\n")]),
 ("v16_bo_thu_tu_xuyen_manh", (16,), [(TF, "            or names != sorted(names, key=lambda name: _stable_name(Path(name)))):\n", "            ):\n")]),
 ("v17_bo_kiem_trung_o_loader", (17,), [(TF, "    if (len(set(portable_keys)) != len(portable_keys)\n", "    if (False\n")]),
 ("v18_manh_k_duoc_mang_shards", (18,), [(TF, ALLOW, "if targets not in allowed:")]),
 ("v19_nhan_shards_rong", (19,), [(TF, SHCHK, "        if shards != expected:\n")]),
 ("v20_nhan_shards_khong_lien_tuc", (20,), [(TF, SHCHK, "        if not shards or expected is None:\n")]),
 ("v21_manh_1_bo_qua_cau_lenh_thua", (21,), [(TF, "    targets = []\n", "    body = [n for n in body if not primary or isinstance(n, ast.Assign)]\n    targets = []\n")]),
 ("v22_manh_k_bo_qua_cau_lenh_thua", (22,), [(TF, "    targets = []\n", "    body = [n for n in body if primary or isinstance(n, ast.Assign)]\n    targets = []\n")]),
 ("v23_cong_bo_manh_lac", (23,), [(RL, "if extra or any(", "if any(")]),
 ("v24_cong_chi_xet_manh_phu_co_mat", (24,), [(RL, SO, "    if extra or any((a != d) if i == 0 else (a is None) for i, ((_, d), (_, a)) in enumerate(zip(expected_modules, actual_modules))):\n")]),
 ("v25_manh_phu_thieu_doc_thanh_rong", (25,), [(RL, "p.read_bytes() if p.is_file() and not p.is_symlink() else None", 'p.read_bytes() if p.is_file() and not p.is_symlink() else b""')]),
 ("v26_thieu_manh_1_bao_stale", (26,), [(RL, 'return {**payload, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}', 'return {**payload, "status": "missing", "error": "GENERATED_BUNDLE_STALE"}')]),
 ("v27_mot_manh_bam_theo_chuoi_ten", (27,), [(RL, "    if len(expected_modules) == 1:", "    if False:")]),
 ("v28_bam_nhieu_manh_bo_ten", (28,), [(RL, r'expected = b"".join(n.encode() + b"\0" + d for n, d in expected_modules)', 'expected = b"".join(d for n, d in expected_modules)')]),
 ("v29_shards_expected_bytes_lech", (29,), [(RL, 'shards = [{"name": n, "expected_bytes": len(d),', 'shards = [{"name": n, "expected_bytes": len(d) + 1,')]),
 ("v30_han_manh_200000", (30,), [(TF, "_BUNDLED_SHARD_LIMIT = 192 * 1024\n", "_BUNDLED_SHARD_LIMIT = 200000\n")]),
 ("v31_manh_that_phinh_40000B", (31,), [(TF, 'body = header + lines + [")"]', 'body = header + lines + [")"] + (["# " + "x" * 40000] if sum(map(len, lines)) > 160000 else [])')]),
 ("f01_dem_ky_tu_thay_vi_byte", (5,), [(TF, 'size = len(line.encode("utf-8")) + 1', 'size = len(line) + 1')]),
 ("f02_manh_1_them_bieu_thuc", (8,), [(TF, 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n', 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n            body.append("0")\n')]),
 ("f02b_mot_manh_nhieu_fragment_them_bieu_thuc", (3,), [(TF, 'body = header + lines + [")"]', 'body = header + lines + [")"] + (["0"] if len(groups) == 1 and len(lines) > 1 else [])')]),
 ("f03_cong_bo_so_manh_chinh", (24,), [(RL, SO, "    if extra or any((a != d) if i > 0 else (a is None) for i, ((_, d), (_, a)) in enumerate(zip(expected_modules, actual_modules))):\n")]),
 ("v32a_loader_doc_xuyen_symlink", (32,), [(TF, "    if path.is_symlink():   # không đọc xuyên symlink tại tên mảnh (cùng chốt với `_candidate_path`)\n", "    if False:\n")]),
 ("v32c_cong_doc_xuyen_symlink", (32,), [(RL, "p.read_bytes() if p.is_file() and not p.is_symlink() else None", "p.read_bytes() if p.is_file() else None")]),
 ("v32d_writer_ghi_xuyen_symlink", (32,), [(TF, "        if (scripts / name).is_symlink():\n", "        if False:\n")]),
 ("g_doi_chu_thich_dau_tep", (1, 2), [(TF, '\'"""Generated by tl_core.test_fragments; do not edit."""\'', '\'"""Generated by tl_core.test_fragments; do not edit!"""\'')]),
 ("a_nap_moi_tep_danh_so_bo_khai_bao", (13, 14, 15), [(TF, "    for shard in shards:\n", f"    for shard in {LOAD_ALL}):\n")]),
 ("q_cong_chi_so_manh_1", (24, 25, 32), [(RL, SO, SO.replace("zip(expected_modules, actual_modules)", "zip(expected_modules[:1], actual_modules[:1])"))]),
 ("c_bo_han_manh", (4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 29, 31), [(TF, CAT, "if False:")]),
]
RUN = r'''
import sys, json, importlib.util
sys.dont_write_bytecode = True
sys.path.insert(0, "scripts")
import tl
spec = importlib.util.spec_from_file_location("frag", "scripts/test_fragments/wp433_bundled_tach_manh.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r = m.run(tl)
print("KQ " + json.dumps({"run": r, "kq": m._KQ}))
'''
files = subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True, text=True, check=True).stdout.splitlines()
sai = 0
for ten, dich, subs in MUT:
    with tempfile.TemporaryDirectory(prefix="db_") as t:
        d = Path(t) / "r"
        for rel in files:
            src = repo / rel
            if src.is_file():
                (d / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, d / rel)
        for rel, a, b in subs:
            p = d / rel; s = p.read_text(encoding="utf-8")
            assert s.count(a) == 1 and a != b, (ten, a, s.count(a))
            p.write_text(s.replace(a, b), encoding="utf-8", newline="\n")
        pr = subprocess.run([sys.executable, "-B", "-c", RUN], cwd=d, capture_output=True, text=True)
        kq = [l for l in pr.stdout.splitlines() if l.startswith("KQ ")]
        if pr.returncode != 0 or not kq:
            sai += 1; print(ten, "VANG rc=%d" % pr.returncode, pr.stderr[-400:]); continue
        j = json.loads(kq[-1][3:])
        do = [n for n in NHAN if j["kq"].get(n) is not True]   # khoa vang tinh la do
        ky = [P[i] for i in sorted(dich)]
        dat = do == ky and j["run"] is (not dich) and len(j["kq"]) == 32
        sai += not dat
        print(("DAT " if dat else "SAI ") + ten, "run=%s" % j["run"], "so_nhan=%d" % len(j["kq"]), "do=" + ",".join(do), "dich=" + ",".join(ky))
print("TONG: %d dot bien + doi chung, sai=%d" % (len(MUT) - 1, sai))
sys.exit(1 if sai else 0)
