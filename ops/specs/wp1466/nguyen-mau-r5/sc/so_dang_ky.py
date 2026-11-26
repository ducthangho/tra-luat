import json, os, subprocess, sys
NAP = ("import json, os, sys; sys.dont_write_bytecode = True; sys.path.insert(0, os.path.join(sys.argv[1], '.claude', 'dev')); os.chdir(sys.argv[1]);"
       "import packet_loop_test as t, packet_loop_test_manh as m;"
       "print(json.dumps(dict(cases=[n for n, _ in t.CASES], linux=list(m.ca_dang_ky(t)),"
       " mutants={k: [v[0], v[1], list(v[2])] for k, v in t.MUTANTS.items()}, nham=sorted(t.MUTANTS_NHAM_TEST))))")
def nap(cay):
    r = subprocess.run([sys.executable, "-B", "-W", "ignore", "-c", NAP, os.path.abspath(cay)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"SỔ ĐĂNG KÝ: KHÔNG ĐO ĐƯỢC — nạp {cay} rc={r.returncode}: {r.stderr.strip()[-300:]}")
    return json.loads(r.stdout.strip().splitlines()[-1])
a, b = nap(sys.argv[1]), nap(sys.argv[2])
it = iter(b["cases"])
con = all(n in it for n in a["cases"])  # dãy tên nền là dãy con GIỮ THỨ TỰ của dãy ở H
doi = sorted(k for k, v in a["mutants"].items() if b["mutants"].get(k) != v)
T = sorted(set(b["cases"]) - set(a["cases"]))
dk = dict(day_con_giu_thu_tu=con, T_bang_hai_hieu=len(T) == len(b["cases"]) - len(a["cases"]) == len(b["linux"]) - len(a["linux"]),
          T_dung_tien_to=all(n.startswith("doctrine_inv_") for n in T), mutants_cu_giu_nguyen=not doi, nham_nen_trong_h=set(a["nham"]) <= set(b["nham"]))
print(json.dumps(dict(cases=[len(a["cases"]), len(b["cases"])], linux=[len(a["linux"]), len(b["linux"])], T=len(T),
                      mutants=[len(a["mutants"]), len(b["mutants"])], mutants_cu_doi=doi[:5], **dk), ensure_ascii=False))
print("SỔ ĐĂNG KÝ:", "ĐẠT" if all(dk.values()) else "KHÔNG ĐẠT")
sys.exit(0 if all(dk.values()) else 1)
