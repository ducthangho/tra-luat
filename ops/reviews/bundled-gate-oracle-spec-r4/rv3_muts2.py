RL = "scripts/tl_core/release.py"; TF = "scripts/tl_core/test_fragments.py"
SO = "    if extra or any(a != d for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n"
EXN = ""
MUT = [
 ("doi_chung", (), []),
 ("rv_p1_bo_qua_dong_tron_ven_noi_them", (24, 27), [(RL, SO, '    if extra or any((a is None or (a != d and not (len(a) > len(d) and a.startswith(d) and d.endswith(b"\\n") and a.endswith(b"\\n")))) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
 ("rv_p1_bo_qua_chu_thich_cuoi_tep", (24, 27), [(RL, SO, '    if extra or any((a is None or (a != d and not (a.startswith(d) and a.endswith(b"\\n") and all(l.startswith(b"#") for l in a[len(d):].splitlines())))) for (_, d), (_, a) in zip(expected_modules, actual_modules)):\n')]),
]
