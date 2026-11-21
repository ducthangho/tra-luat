"""Ma tran dot bien A2 cua BUNDLED-GATE-ORACLE-FRESHNESS r5 = ma tran g5 (bf38a110, 49; khai lai dich f05 V8,V9 · v28 V24,V28 · f01 V5,V31)
+ 43 dot bien lop F10/F11 (r11_) + 13 ca no ghi nhan (no_) + 20 ca go chot (a7_). Sinh boi gen_ma_tran.py.
Goc: ma tran dot bien N2 (dac ta r4): moi dot bien chay tren BAN SAO cay (git ls-files), khong dung tep that.
Dung: python -B ma_tran_dot_bien.py <repo>. Thoat 0 khi MOI dong tap do == tap dich khai, khong vang."""
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
 ("v28_bam_nhieu_manh_bo_ten", (24, 28), [(RL, r'expected = b"".join(n.encode() + b"\0" + d for n, d in expected_modules)', 'expected = b"".join(d for n, d in expected_modules)')]),
 ("v29_shards_expected_bytes_lech", (29,), [(RL, 'shards = [{"name": n, "expected_bytes": len(d),', 'shards = [{"name": n, "expected_bytes": len(d) + 1,')]),
 ("v30_han_manh_200000", (30,), [(TF, "_BUNDLED_SHARD_LIMIT = 192 * 1024\n", "_BUNDLED_SHARD_LIMIT = 200000\n")]),
 ("v31_manh_that_phinh_40000B", (31,), [(TF, 'body = header + lines + [")"]', 'body = header + lines + [")"] + (["# " + "x" * 40000] if sum(map(len, lines)) > 160000 else [])')]),
 ("f01_dem_ky_tu_thay_vi_byte", (5, 31), [(TF, 'size = len(line.encode("utf-8")) + 1', 'size = len(line) + 1')]),
 ("f02_manh_1_them_bieu_thuc", (8,), [(TF, 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n', 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n            body.append("0")\n')]),
 ("f02b_mot_manh_nhieu_fragment_them_bieu_thuc", (3,), [(TF, 'body = header + lines + [")"]', 'body = header + lines + [")"] + (["0"] if len(groups) == 1 and len(lines) > 1 else [])')]),
 ("f03_cong_bo_so_manh_chinh", (24, 27), [(RL, SO, "    if extra or any((a != d) if i > 0 else (a is None) for i, ((_, d), (_, a)) in enumerate(zip(expected_modules, actual_modules))):\n")]),
 ("v32a_loader_doc_xuyen_symlink", (32,), [(TF, "    if path.is_symlink():   # không đọc xuyên symlink tại tên mảnh (cùng chốt với `_candidate_path`)\n", "    if False:\n")]),
 ("v32c_cong_doc_xuyen_symlink", (32,), [(RL, "p.read_bytes() if p.is_file() and not p.is_symlink() else None", "p.read_bytes() if p.is_file() else None")]),
 ("v32d_writer_ghi_xuyen_symlink", (32,), [(TF, "        if (scripts / name).is_symlink():\n", "        if False:\n")]),
 ("f05_manh_1_gan_nhieu_dich", (8, 9), [(TF, '            body.append("BUNDLED_FRAGMENT_SHARDS = ("', '            body.append("BUNDLED_FRAGMENT_SHARDS = EXTRA = ("')]),
 ("f05b_manh_phu_annassign", (8,), [(TF, 'body = header + lines + [")"]', 'body = header + lines + [")"] + (["X: int = 0"] if index > 1 else [])')]),
 ("f06_one_skip_chap_nhan_mot_manh_stale", (27,), [(RL, SO, SO.replace("if extra or any(", "if extra or len(expected_modules) > 1 and any("))]),
 ("f06_one_red_tu_choi_mot_manh_current", (27,), [(RL, SO, SO.replace("if extra or any(", "if extra or len(expected_modules) == 1 or any("))]),
 ("f06_multi_red_tu_choi_nhieu_manh_current", (28,), [(RL, SO, SO.replace("if extra or any(", "if extra or len(expected_modules) > 1 or any("))]),
 ("f07_topology_bo_qua_symlink_dut", (32,), [(TF, "    if bundled_path.exists() or bundled_path.is_symlink():", "    if bundled_path.exists():")]),
 ("g_doi_chu_thich_dau_tep", (1, 2), [(TF, '\'"""Generated by tl_core.test_fragments; do not edit."""\'', '\'"""Generated by tl_core.test_fragments; do not edit!"""\'')]),
 ("a_nap_moi_tep_danh_so_bo_khai_bao", (13, 14, 15), [(TF, "    for shard in shards:\n", f"    for shard in {LOAD_ALL}):\n")]),
 ("q_cong_chi_so_manh_1", (24, 25, 32), [(RL, SO, SO.replace("zip(expected_modules, actual_modules)", "zip(expected_modules[:1], actual_modules[:1])"))]),
 ("c_bo_han_manh", (4, 5, 6, 7, 8, 9, 10, 11, 31), [(TF, CAT, "if False:")]),
 ('r11_size_only', (24, 27), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', "    if extra or any(len(a or b'') != len(d) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n")]),
 ('r11_size_only_raw', (24, 25, 27, 32), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any(len(a) != len(d) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('r11_one_stale_ok', (27,), [('scripts/tl_core/release.py', '            "status": "stale",\n', '            "status": "stale",\n            "ok": len(expected_modules) == 1,\n')]),
 ('r11_ann_empty', (8,), [('scripts/tl_core/test_fragments.py', 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n', 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n            body.append("X: int")\n')]),
 ('r11_duplicate', (8,), [('scripts/tl_core/test_fragments.py', 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n', 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n            body.append("BUNDLED_FRAGMENT_SOURCES = ()")\n')]),
 ('r11_missing_ok_narrow', (26,), [('scripts/tl_core/release.py', 'return {**payload, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}', 'return {**payload, "ok": not bundled_path.is_symlink(), "status": "missing", "error": "BUNDLED_MODULE_MISSING"}')]),
 ('r11_missing_ok', (26, 32), [('scripts/tl_core/release.py', 'return {**payload, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}', 'return {**payload, "ok": True, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}')]),
 ('r11_missing_status', (26,), [('scripts/tl_core/release.py', 'return {**payload, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}', 'return {**payload, "status": "stale", "error": "BUNDLED_MODULE_MISSING"}')]),
 ('r11_stale_rc1', (23, 24, 25, 26, 27), [('scripts/tl_core/release.py', '    return 0 if payload.get("ok") else 2\n\n\ndef cmd_release_check', '    return 0 if payload.get("ok") else 1\n\n\ndef cmd_release_check')]),
 ('r11_stale_status_current', (23, 24, 25, 27), [('scripts/tl_core/release.py', '            "status": "stale",\n', '            "status": "current",\n')]),
 ('r11_extra_ok', (23,), [('scripts/tl_core/release.py', '            "status": "stale",\n', '            "status": "stale",\n            "ok": bool(extra) and len(extra) == 1,\n')]),
 ('r11_absent_ok', (25, 32), [('scripts/tl_core/release.py', '            "status": "stale",\n', '            "status": "stale",\n            "ok": all(a is not None for _, a in actual_modules) is False,\n')]),
 ('r11_absent_status', (25,), [('scripts/tl_core/release.py', '            "status": "stale",\n', '            "status": "stale" if all(a is not None for _, a in actual_modules) else "current",\n')]),
 ('r11_extra_status', (23,), [('scripts/tl_core/release.py', '            "status": "stale",\n', '            "status": "current" if extra else "stale",\n')]),
 ('r11_stale_sha_swap', (24, 27), [('scripts/tl_core/release.py', '            "actual_sha256": actual_sha256,\n            "expected_bytes": len(expected),\n            "actual_bytes": len(actual),\n            "extra_shards": extra,', '            "actual_sha256": expected_sha256,\n            "expected_bytes": len(expected),\n            "actual_bytes": len(actual),\n            "extra_shards": extra,')]),
 ('r11_stale_flip_only_firstbyte', (24, 27), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any((a is None or a[:1] != d[:1] or len(a) != len(d)) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('r11_stale_ignore_lastbyte_region', (24, 27), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any((a is None or a[:-1] != d[:-1] or len(a) != len(d)) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('r11_stale_head_only', (24, 27), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any((a is None or a[:64] != d[:64] or len(a) != len(d)) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('r11_stale_tail_only', (24, 27), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any((a is None or a[-64:] != d[-64:] or len(a) != len(d)) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('r11_stale_sha_len_cmp', (24, 27), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', "    if extra or any((a is None or (len(a), a.count(b'#')) != (len(d), d.count(b'#'))) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n")]),
 ('r11_m1_chi_so_tien_to', (24, 27), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any((a is None or a[:len(d)] != d) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('r11_m2_chap_nhan_cat_cut', (24, 27), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any((a is None or d[:len(a)] != a) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('r11_m3_chuan_hoa_crlf', (24, 27), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any((a is None or a.replace(b"\\r\\n", b"\\n") != d) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('r11_m4_stale_expected_sha_sai', (24, 27), [('scripts/tl_core/release.py', '"error": "GENERATED_BUNDLE_STALE",\n            "expected_sha256": expected_sha256,', '"error": "GENERATED_BUNDLE_STALE",\n            "expected_sha256": actual_sha256,')]),
 ('r11_m5_stale_expected_bytes_sai', (24, 27), [('scripts/tl_core/release.py', '"expected_bytes": len(expected),\n            "actual_bytes": len(actual),\n            "extra_shards"', '"expected_bytes": len(actual),\n            "actual_bytes": len(actual),\n            "extra_shards"')]),
 ('r11_m6_stale_actual_bytes_sai', (24, 27), [('scripts/tl_core/release.py', '"actual_bytes": len(actual),\n            "extra_shards"', '"actual_bytes": len(expected),\n            "extra_shards"')]),
 ('r11_m7_doc_toi_da_len_ky_vong', (24, 27), [('scripts/tl_core/release.py', 'p.read_bytes() if p.is_file() and not p.is_symlink() else None', 'p.read_bytes()[:len(_)] if p.is_file() and not p.is_symlink() else None')]),
 ('r11_m8_regex_lac_mot_chu_so', (23,), [('scripts/tl_core/test_fragments.py', 'r"tl_test_fragments_bundled_([2-9]|[1-9][0-9]+)[.]py\\Z"', 'r"tl_test_fragments_bundled_([2-9])[.]py\\Z"')]),
 ('r11_rv3_bo_qua_dong_tron_noi_them', (24, 27), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any((a is None or (a != d and not (len(a) > len(d) and a.startswith(d) and d.endswith(b"\\n") and a.endswith(b"\\n")))) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('r11_rv3_bo_qua_chu_thich_cuoi_tep', (24, 27), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any((a is None or (a != d and not (a.startswith(d) and a.endswith(b"\\n") and all(l.startswith(b"#") for l in a[len(d):].splitlines())))) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('r11_rv3_sources_annassign_gia_tri', (1, 2, 3, 4, 5, 6, 8), [('scripts/tl_core/test_fragments.py', '        body = header + lines + [")"]\n', '        body = header + lines + [")"]\n        if index == 1:\n            body[3] = "BUNDLED_FRAGMENT_SOURCES: tuple = ("\n')]),
 ('r11_rv3_manh_phu_hai_docstring', (8,), [('scripts/tl_core/test_fragments.py', '        body = header + lines + [")"]\n', '        body = header + lines + [")"]\n        if index > 1:\n            body = body[:2] + [body[1]] + body[2:]\n')]),
 ('r11_rv3_shards_truoc_sources', (8,), [('scripts/tl_core/test_fragments.py', '        out.append((_bundled_shard_name(index),', '        if index == 1 and len(groups) > 1:\n            body = body[:3] + [body[-1]] + body[3:-1]\n        out.append((_bundled_shard_name(index),')]),
 ('r11_rv4_s1_manh_don_trung_sources', (8,), [('scripts/tl_core/test_fragments.py', '        body = header + lines + [")"]\n', '        body = header + lines + [")"] + ([\'BUNDLED_FRAGMENT_SOURCES = ()\'] if (len(lines) == 1 and len(groups) > 1) else [])\n')]),
 ('r11_rv4_s2_manh_don_gan_khong_literal', (8,), [('scripts/tl_core/test_fragments.py', '        body = header + lines + [")"]\n', '        body = header + lines + [")"] + ([\'BUNDLED_FRAGMENT_COUNT = len(BUNDLED_FRAGMENT_SOURCES)\'] if (len(lines) == 1 and len(groups) > 1) else [])\n')]),
 ('r11_rv4_s3_manh_don_annassign_rong', (8,), [('scripts/tl_core/test_fragments.py', '        body = header + lines + [")"]\n', '        body = header + lines + [")"] + ([\'X: int\'] if (len(lines) == 1 and len(groups) > 1) else [])\n')]),
 ('r11_rv4_s4_manh_don_augassign_sources', (8,), [('scripts/tl_core/test_fragments.py', '        body = header + lines + [")"]\n', '        body = header + lines + [")"] + ([\'BUNDLED_FRAGMENT_SOURCES += ()\'] if (len(lines) == 1 and len(groups) > 1) else [])\n')]),
 ('r11_rv4_s5_manh_qua_co_trung_sources', (8,), [('scripts/tl_core/test_fragments.py', '        body = header + lines + [")"]\n', '        body = header + lines + [")"] + ([\'BUNDLED_FRAGMENT_SOURCES = ()\'] if (len(lines) == 1 and len(lines[0].encode("utf-8")) + 1 > _BUNDLED_SHARD_LIMIT) else [])\n')]),
 ('r11_rv4_s6_phi_ascii_annassign', (8,), [('scripts/tl_core/test_fragments.py', '        body = header + lines + [")"]\n', '        body = header + lines + [")"] + ([\'X: int\'] if any(ord(c) > 127 for l in lines for c in l) else [])\n')]),
 ('r11_rv4_s7_manh_don_for_loop', (8,), [('scripts/tl_core/test_fragments.py', '        body = header + lines + [")"]\n', '        body = header + lines + [")"] + ([\'for BUNDLED_FRAGMENT_N in (): pass\'] if (len(lines) == 1 and len(groups) > 1) else [])\n')]),
 ('r11_rv4_g1_cong_bo_qua_noi_dong_chu_thich', (24, 27), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any(a != d and not (a is not None and a.startswith(d) and a[len(d):].startswith(b"#")) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('r11_rv4_g2_missing_bao_stale', (26,), [('scripts/tl_core/release.py', 'return {**payload, "status": "missing", "error": "BUNDLED_MODULE_MISSING"}', 'return {**payload, "status": "missing", "error": "GENERATED_BUNDLE_STALE"}')]),
 ('r11_rv4_g3_extra_chi_khi_khong_lech', (23,), [('scripts/tl_core/release.py', '    if extra or any(', '    if (extra and len(expected_modules) == 1) or any(')]),
 ('no_hai_manh_hong_ok', (), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or sum(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)) == 1:\n')]),
 ('no_trao_noi_dung_giua_manh', (), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or sorted(x or b"" for _, x in actual_modules) != sorted(x for _, x in expected_modules) or any(x is None for _, x in actual_modules):\n')]),
 ('no_hai_lac_ok', (), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if len(extra) == 1 or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('no_lac_chi_bao_dau', (), [('scripts/tl_core/release.py', '            "extra_shards": extra,\n', '            "extra_shards": extra[:1],\n')]),
 ('no_lac_mot_manh_bo_qua', (), [('scripts/tl_core/release.py', '                       and p.name not in {n for n, _ in expected_modules})\n', '                       and p.name not in {n for n, _ in expected_modules} and len(expected_modules) > 1)\n')]),
 ('no_lac_symlink_bo_qua', (), [('scripts/tl_core/release.py', '                       and p.name not in {n for n, _ in expected_modules})\n', '                       and p.name not in {n for n, _ in expected_modules} and not p.is_symlink())\n')]),
 ('no_thieu_chinh_nhieu_manh_bao_stale', (), [('scripts/tl_core/release.py', '    if not bundled_path.is_file():\n', '    if not bundled_path.is_file() and not (bundled_path.parent / "tl_test_fragments_bundled_2.py").is_file():\n')]),
 ('no_vung_mu_1_den_giua', (), [('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any((a is None or len(a) != len(d) or a[:1] + a[len(d) // 2:] != d[:1] + d[len(d) // 2:]) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('no_thieu_phu_actual_bytes_sai', (), [('scripts/tl_core/release.py', '"actual_bytes": len(actual),\n            "extra_shards"', '"actual_bytes": len(actual) if all(x is not None for _, x in actual_modules) else -1,\n            "extra_shards"')]),
 ('no_generator_loi_thanh_ok', (), [('scripts/tl_core/release.py', '            "status": "invalid",\n            "error": "GENERATED_BUNDLE_INPUT_INVALID",\n', '            "ok": True,\n            "status": "invalid",\n            "error": "GENERATED_BUNDLE_INPUT_INVALID",\n')]),
 ('no_regex_toi_da_hai_chu_so', (), [('scripts/tl_core/test_fragments.py', 'r"tl_test_fragments_bundled_([2-9]|[1-9][0-9]+)[.]py\\Z"', 'r"tl_test_fragments_bundled_([2-9]|[1-9][0-9])[.]py\\Z"')]),
 ('no_regex_hai_chu_so_chi_1x', (), [('scripts/tl_core/test_fragments.py', 'r"tl_test_fragments_bundled_([2-9]|[1-9][0-9]+)[.]py\\Z"', 'r"tl_test_fragments_bundled_([2-9]|1[0-9]+)[.]py\\Z"')]),
 ('no_manh_phu_sources_la_list', (), [('scripts/tl_core/test_fragments.py', '        body = header + lines + [")"]\n', '        body = header + lines + [")"]\n        if index > 1:\n            body = body[:3] + ["BUNDLED_FRAGMENT_SOURCES = ["] + lines + ["]"]\n')]),
 ('a7_go_ho_doi_do_dai', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '                lambda d: d + b"#", lambda d: d[:-1],                              # đổi độ dài: nối | cắt\n                lambda d: d + b"# sua\\n",                                         # nhiễu loạn của BASE (nối dòng trọn) — giữ nguyên\n                lambda d: d.replace(b"\\n", b"\\r\\n", 1))                          # kết thúc dòng: LF -> CRLF\n', '                )\n')]),
 ('a7_go_ho_doi_do_dai__m7_song', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '                lambda d: d + b"#", lambda d: d[:-1],                              # đổi độ dài: nối | cắt\n                lambda d: d + b"# sua\\n",                                         # nhiễu loạn của BASE (nối dòng trọn) — giữ nguyên\n                lambda d: d.replace(b"\\n", b"\\r\\n", 1))                          # kết thúc dòng: LF -> CRLF\n', '                )\n'), ('scripts/tl_core/release.py', 'p.read_bytes() if p.is_file() and not p.is_symlink() else None', 'p.read_bytes()[:len(_)] if p.is_file() and not p.is_symlink() else None')]),
 ('a7_go_ho_giu_do_dai', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '        bien = (lat(lambda n: 0), lat(lambda n: n // 2), lat(lambda n: n - 1),     # giữ độ dài: đầu | giữa | cuối\n', '        bien = (\n')]),
 ('a7_go_ho_giu_do_dai__size_only_song', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '        bien = (lat(lambda n: 0), lat(lambda n: n // 2), lat(lambda n: n - 1),     # giữ độ dài: đầu | giữa | cuối\n', '        bien = (\n'), ('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', "    if extra or any(len(a or b'') != len(d) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n")]),
 ('a7_go_moi_vi_tri_mot_fixture', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '        bien = (lat(lambda n: 0), lat(lambda n: n // 2), lat(lambda n: n - 1),     # giữ độ dài: đầu | giữa | cuối\n', '        bien = (lambda d: lat(lambda n: 0)(lat(lambda n: n // 2)(lat(lambda n: n - 1)(d))),\n')]),
 ('a7_go_moi_vi_tri__head_only_song', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '        bien = (lat(lambda n: 0), lat(lambda n: n // 2), lat(lambda n: n - 1),     # giữ độ dài: đầu | giữa | cuối\n', '        bien = (lambda d: lat(lambda n: 0)(lat(lambda n: n // 2)(lat(lambda n: n - 1)(d))),\n'), ('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any((a is None or a[:64] != d[:64] or len(a) != len(d)) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('a7_go_bon_truong_quyet_dinh', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', 'return quyet(rc, j) == (2, False, "stale", _STALE) and truong(j) == [_bam(e), _bam(a), len(e), len(a)]', 'return j.get("error") == _STALE and truong(j) == [_bam(e), _bam(a), len(e), len(a)]')]),
 ('a7_go_bon_truong_quyet_dinh__one_stale_ok_song', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', 'return quyet(rc, j) == (2, False, "stale", _STALE) and truong(j) == [_bam(e), _bam(a), len(e), len(a)]', 'return j.get("error") == _STALE and truong(j) == [_bam(e), _bam(a), len(e), len(a)]'), ('scripts/tl_core/release.py', '            "status": "stale",\n', '            "status": "stale",\n            "ok": len(expected_modules) == 1,\n')]),
 ('a7_go_bon_truong_bam', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', 'return quyet(rc, j) == (2, False, "stale", _STALE) and truong(j) == [_bam(e), _bam(a), len(e), len(a)]', 'return quyet(rc, j) == (2, False, "stale", _STALE)')]),
 ('a7_go_bon_truong_bam__m6_song', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', 'return quyet(rc, j) == (2, False, "stale", _STALE) and truong(j) == [_bam(e), _bam(a), len(e), len(a)]', 'return quyet(rc, j) == (2, False, "stale", _STALE)'), ('scripts/tl_core/release.py', '"actual_bytes": len(actual),\n            "extra_shards"', '"actual_bytes": len(expected),\n            "extra_shards"')]),
 ('a7_go_lan_dau_thang', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '            gan.setdefault(n.targets[0].id, ast.literal_eval(n.value))\n', '            gan[n.targets[0].id] = ast.literal_eval(n.value)\n')]),
 ('a7_go_lan_dau_thang__duplicate_lan', (4, 5, 6, 8), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '            gan.setdefault(n.targets[0].id, ast.literal_eval(n.value))\n', '            gan[n.targets[0].id] = ast.literal_eval(n.value)\n'), ('scripts/tl_core/test_fragments.py', 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n', 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n            body.append("BUNDLED_FRAGMENT_SOURCES = ()")\n')]),
 ('a7_go_phep_gan_chuan', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '        if type(n) is ast.Assign and [type(t) for t in n.targets] == [ast.Name] and n.targets[0].id in (_SRC, _SHA):\n            gan.setdefault(n.targets[0].id, ast.literal_eval(n.value))\n', '        for t in getattr(n, "targets", [getattr(n, "target", None)]):\n            if isinstance(t, ast.Name):\n                gan.setdefault(t.id, ast.literal_eval(n.value))\n')]),
 ('a7_go_phep_gan_chuan__ann_empty_van', (4, 5, 6, 8, 9), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '        if type(n) is ast.Assign and [type(t) for t in n.targets] == [ast.Name] and n.targets[0].id in (_SRC, _SHA):\n            gan.setdefault(n.targets[0].id, ast.literal_eval(n.value))\n', '        for t in getattr(n, "targets", [getattr(n, "target", None)]):\n            if isinstance(t, ast.Name):\n                gan.setdefault(t.id, ast.literal_eval(n.value))\n'), ('scripts/tl_core/test_fragments.py', 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n', 'for k in range(2, len(groups) + 1)).rstrip() + ")")\n            body.append("X: int")\n')]),
 ('a7_go_lac_hai_chu_so', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '        return all([mot_lac(ten) for ten in (_M9, _M10)])\n', '        return all([mot_lac(ten) for ten in (_M9,)])\n')]),
 ('a7_go_lac_hai_chu_so__m8_song', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '        return all([mot_lac(ten) for ten in (_M9, _M10)])\n', '        return all([mot_lac(ten) for ten in (_M9,)])\n'), ('scripts/tl_core/test_fragments.py', 'r"tl_test_fragments_bundled_([2-9]|[1-9][0-9]+)[.]py\\Z"', 'r"tl_test_fragments_bundled_([2-9])[.]py\\Z"')]),
 ('a7_go_nhieu_loan_base', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '                lambda d: d + b"# sua\\n",                                         # nhiễu loạn của BASE (nối dòng trọn) — giữ nguyên\n', '')]),
 ('a7_go_nhieu_loan_base__dong_tron_song', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '                lambda d: d + b"# sua\\n",                                         # nhiễu loạn của BASE (nối dòng trọn) — giữ nguyên\n', ''), ('scripts/tl_core/release.py', '    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n', '    if extra or any((a is None or (a != d and not (len(a) > len(d) and a.startswith(d) and d.endswith(b"\\n") and a.endswith(b"\\n")))) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ('a7_go_moi_lac_mot_fixture', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '            mods, dia, rc, j = cong(ba, lambda s: (s / ten).write_bytes(b"x = 0\\n"))\n', '            mods, dia, rc, j = cong(ba, lambda s: [(s / n).write_bytes(b"x = 0\\n") for n in (_M9, _M10)])\n'), ('scripts/test_fragments/wp433_bundled_tach_manh.py', 'and lac == [ten] and', 'and ten in lac and')]),
 ('a7_go_moi_lac_mot_fixture__extra_ok_song', (), [('scripts/test_fragments/wp433_bundled_tach_manh.py', '            mods, dia, rc, j = cong(ba, lambda s: (s / ten).write_bytes(b"x = 0\\n"))\n', '            mods, dia, rc, j = cong(ba, lambda s: [(s / n).write_bytes(b"x = 0\\n") for n in (_M9, _M10)])\n'), ('scripts/test_fragments/wp433_bundled_tach_manh.py', 'and lac == [ten] and', 'and ten in lac and'), ('scripts/tl_core/release.py', '            "status": "stale",\n', '            "status": "stale",\n            "ok": bool(extra) and len(extra) == 1,\n')]),
]
RUN = r'''
import sys, json, importlib.util
sys.dont_write_bytecode = True
sys.path.insert(0, "scripts")
import tl
spec = importlib.util.spec_from_file_location("frag", "scripts/test_fragments/wp433_bundled_tach_manh.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r = m.run(tl)
print("KQ " + json.dumps({"run": r, "kq": m._KQ, "ly_do": m._LY_DO}))
'''
files = subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True, text=True, check=True).stdout.splitlines()
KHONG_VANG = set(['a7_go_bon_truong_bam', 'a7_go_bon_truong_bam__m6_song', 'a7_go_bon_truong_quyet_dinh', 'a7_go_bon_truong_quyet_dinh__one_stale_ok_song', 'a7_go_ho_doi_do_dai', 'a7_go_ho_doi_do_dai__m7_song', 'a7_go_ho_giu_do_dai', 'a7_go_ho_giu_do_dai__size_only_song', 'a7_go_lac_hai_chu_so', 'a7_go_lac_hai_chu_so__m8_song', 'a7_go_lan_dau_thang', 'a7_go_lan_dau_thang__duplicate_lan', 'a7_go_moi_lac_mot_fixture', 'a7_go_moi_lac_mot_fixture__extra_ok_song', 'a7_go_moi_vi_tri__head_only_song', 'a7_go_moi_vi_tri_mot_fixture', 'a7_go_nhieu_loan_base', 'a7_go_nhieu_loan_base__dong_tron_song', 'a7_go_phep_gan_chuan', 'no_generator_loi_thanh_ok', 'no_hai_lac_ok', 'no_hai_manh_hong_ok', 'no_lac_chi_bao_dau', 'no_lac_mot_manh_bo_qua', 'no_lac_symlink_bo_qua', 'no_manh_phu_sources_la_list', 'no_regex_hai_chu_so_chi_1x', 'no_regex_toi_da_hai_chu_so', 'no_thieu_chinh_nhieu_manh_bao_stale', 'no_thieu_phu_actual_bytes_sai', 'no_trao_noi_dung_giua_manh', 'no_vung_mu_1_den_giua', 'r11_absent_status', 'r11_ann_empty', 'r11_duplicate', 'r11_extra_ok', 'r11_extra_status', 'r11_m1_chi_so_tien_to', 'r11_m2_chap_nhan_cat_cut', 'r11_m3_chuan_hoa_crlf', 'r11_m4_stale_expected_sha_sai', 'r11_m5_stale_expected_bytes_sai', 'r11_m6_stale_actual_bytes_sai', 'r11_m7_doc_toi_da_len_ky_vong', 'r11_m8_regex_lac_mot_chu_so', 'r11_missing_ok_narrow', 'r11_missing_status', 'r11_one_stale_ok', 'r11_rv3_bo_qua_chu_thich_cuoi_tep', 'r11_rv3_bo_qua_dong_tron_noi_them', 'r11_rv3_manh_phu_hai_docstring', 'r11_rv3_shards_truoc_sources', 'r11_rv3_sources_annassign_gia_tri', 'r11_rv4_g1_cong_bo_qua_noi_dong_chu_thich', 'r11_rv4_g2_missing_bao_stale', 'r11_rv4_g3_extra_chi_khi_khong_lech', 'r11_rv4_s1_manh_don_trung_sources', 'r11_rv4_s2_manh_don_gan_khong_literal', 'r11_rv4_s3_manh_don_annassign_rong', 'r11_rv4_s4_manh_don_augassign_sources', 'r11_rv4_s5_manh_qua_co_trung_sources', 'r11_rv4_s6_phi_ascii_annassign', 'r11_rv4_s7_manh_don_for_loop', 'r11_size_only', 'r11_stale_flip_only_firstbyte', 'r11_stale_head_only', 'r11_stale_ignore_lastbyte_region', 'r11_stale_rc1', 'r11_stale_sha_len_cmp', 'r11_stale_sha_swap', 'r11_stale_status_current', 'r11_stale_tail_only'])
DON = {d[0] for _, d, _ in MUT if len(d) == 1}
thieu = [P[i] for i in range(1, 33) if i not in DON]
print("DON_DICH: %d/32 khoa co dot bien don dich" % (32 - len(thieu)) + (" THIEU=" + ",".join(thieu) if thieu else ""))
sai = len(thieu)
for ten, dich, subs in MUT:
    with tempfile.TemporaryDirectory(prefix="db_") as t:
        d = Path(t) / "r"
        for rel in files:
            src = repo / rel
            if src.is_file():
                (d / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, d / rel)
        khong_ap = None
        for rel, a, b in subs:
            p = d / rel; s = p.read_text(encoding="utf-8")
            if s.count(a) != 1 or a == b:
                khong_ap = (rel, s.count(a)); break
            p.write_text(s.replace(a, b), encoding="utf-8", newline="\n")
        if khong_ap:
            sai += 1; print("SAI " + ten, "KHONG_AP_DUOC", khong_ap); continue
        pr = subprocess.run([sys.executable, "-B", "-c", RUN], cwd=d, capture_output=True, text=True)
        kq = [l for l in pr.stdout.splitlines() if l.startswith("KQ ")]
        if pr.returncode != 0 or not kq:
            sai += 1; print(ten, "VANG rc=%d" % pr.returncode, pr.stderr[-400:]); continue
        j = json.loads(kq[-1][3:])
        do = [n for n in NHAN if j["kq"].get(n) is not True]   # khoa vang tinh la do
        ky = [P[i] for i in sorted(dich)]
        dat = do == ky and j["run"] is (not dich) and len(j["kq"]) == 32 and not (ten in KHONG_VANG and j.get("ly_do"))
        sai += not dat
        print(("DAT " if dat else "SAI ") + ten, "run=%s" % j["run"], "so_nhan=%d" % len(j["kq"]), "do=" + ",".join(do), "dich=" + ",".join(ky))
print("TONG: %d dot bien + doi chung, sai=%d" % (len(MUT) - 1, sai))
sys.exit(1 if sai else 0)
