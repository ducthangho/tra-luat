RL = "scripts/tl_core/release.py"; TF = "scripts/tl_core/test_fragments.py"
SO = "    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n"
EXN = "                       and p.name not in {n for n, _ in expected_modules})\n"
MUT = [
 ("doi_chung", (), []),
 # --- bundle-gate-fixture-oracle (release.py) ---
 ("rv_hai_manh_hong_ok", (24,), [(RL, SO, "    if extra or sum(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)) == 1:\n")]),
 ("rv_hai_lac_ok", (23,), [(RL, SO, SO.replace("if extra or any(", "if len(extra) == 1 or any("))]),
 ("rv_lac_chi_bao_dau", (23,), [(RL, '            "extra_shards": extra,\n', '            "extra_shards": extra[:1],\n')]),
 ("rv_lac_mot_manh_bo_qua", (23,), [(RL, EXN, "                       and p.name not in {n for n, _ in expected_modules} and len(expected_modules) > 1)\n")]),
 ("rv_lac_symlink_bo_qua", (23, 32), [(RL, EXN, "                       and p.name not in {n for n, _ in expected_modules} and not p.is_symlink())\n")]),
 ("rv_thieu_chinh_nhieu_manh_bao_stale", (26,), [(RL, "    if not bundled_path.is_file():\n", '    if not bundled_path.is_file() and not (bundled_path.parent / "tl_test_fragments_bundled_2.py").is_file():\n')]),
 ("rv_trao_noi_dung_giua_manh", (24,), [(RL, SO, '    if extra or sorted(x or b"" for _, x in actual_modules) != sorted(x for _, x in expected_modules) or any(x is None for _, x in actual_modules):\n')]),
 ("rv_vung_mu_1_den_giua", (24, 27), [(RL, SO, "    if extra or any((a is None or len(a) != len(d) or a[:1] + a[len(d) // 2:] != d[:1] + d[len(d) // 2:]) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n")]),
 ("rv_thieu_phu_actual_bytes_sai", (25,), [(RL, '"actual_bytes": len(actual),\n            "extra_shards"', '"actual_bytes": len(actual) if all(x is not None for _, x in actual_modules) else -1,\n            "extra_shards"')]),
 ("rv_generator_loi_thanh_ok", (), [(RL, '            "status": "invalid",\n            "error": "GENERATED_BUNDLE_INPUT_INVALID",\n', '            "ok": True,\n            "status": "invalid",\n            "error": "GENERATED_BUNDLE_INPUT_INVALID",\n')]),
 ("rv_regex_toi_da_hai_chu_so", (23,), [(TF, 'r"tl_test_fragments_bundled_([2-9]|[1-9][0-9]+)[.]py\\Z"', 'r"tl_test_fragments_bundled_([2-9]|[1-9][0-9])[.]py\\Z"')]),
 ("rv_regex_hai_chu_so_chi_1x", (23,), [(TF, 'r"tl_test_fragments_bundled_([2-9]|[1-9][0-9]+)[.]py\\Z"', 'r"tl_test_fragments_bundled_([2-9]|1[0-9]+)[.]py\\Z"')]),
 # --- shard-ast-shape-oracle (generator) ---
 ("rv_manh_phu_sources_la_list", (8,), [(TF, '        body = header + lines + [")"]\n', '        body = header + lines + [")"]\n        if index > 1:\n            body = body[:3] + ["BUNDLED_FRAGMENT_SOURCES = ["] + lines + ["]"]\n')]),
 ("rv_manh_chinh_sources_annassign_gia_tri", (3, 8), [(TF, '        body = header + lines + [")"]\n', '        body = header + lines + [")"]\n        if index == 1:\n            body[3] = "BUNDLED_FRAGMENT_SOURCES: tuple = ("\n')]),
 ("rv_manh_phu_hai_docstring", (8,), [(TF, '        body = header + lines + [")"]\n', '        body = header + lines + [")"]\n        if index > 1:\n            body = body[:2] + [body[1]] + body[2:]\n')]),
 ("rv_manh_chinh_shards_truoc_sources", (8, 9), [(TF, '        out.append((_bundled_shard_name(index),', '        if index == 1 and len(groups) > 1:\n            body = body[:3] + [body[-1]] + body[3:-1]\n        out.append((_bundled_shard_name(index),')]),
]
