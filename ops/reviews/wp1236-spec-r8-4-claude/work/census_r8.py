"""Đo hệ quả K7-S trên `ci.yml` thật (ops/specs/wp1236-r8.md, mục *Hệ quả trên ci.yml thật*).
Nạp `LUAT_v1` từ module A1 generation 1 (`git show 508d678:ops/gate_output_doi_chieu.py`, cần fetch `claude/wp1236-a1-g1`),
khớp bước luật theo `name:` nguyên văn, phân loại bằng cài đặt tham chiếu gram.py.
Chạy từ gốc kho: python3 -I ops/reviews/wp1236-r8-soan/census_r8.py d26b36f fe84620 8983e1b"""
import os, subprocess, sys, json, collections
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gram import cu_phap_run

src = subprocess.check_output(["git", "show", "508d678:ops/gate_output_doi_chieu.py"], text=True)
src = src.replace('Path(__file__).with_name("ci_provenance.py")', 'Path("ops/ci_provenance.py")')
ns = {"__name__": "gate_output_508d678"}
exec(compile(src, "508d678:ops/gate_output_doi_chieu.py", "exec"), ns)
ten = {t for m in ns["LUAT_v1"]["MUC"] for b in m["buoc"] for t in b["ten"]}
print("luat_sha256", ns["bam"](ns["LUAT_v1"]), "· so ten buoc luat", len(ten))
for ref in sys.argv[1:]:
    wf = yaml.safe_load(subprocess.check_output(["git", "show", f"{ref}:.github/workflows/ci.yml"]))
    hang = [(jk, s["name"], s.get("shell"), len(str(s.get("run", "")).rstrip("\n").split("\n")), cu_phap_run(s.get("run"), s.get("shell")))
            for jk, j in wf["jobs"].items() for s in j.get("steps", []) if s.get("name") in ten]
    dat = collections.Counter((h[2], str(next(s for s in wf["jobs"][h[0]]["steps"] if s.get("name") == h[1]).get("run")).split()[0])
                              for h in hang if h[4] is None)
    print(json.dumps({"ref": ref, "buoc_luat": len(hang), "ten_khac_nhau": len({h[1] for h in hang}),
                      "do_duoc": sum(h[4] is None for h in hang), "dat_theo_shell_lenh": {f"{k[0]}|{k[1]}": v for k, v in dat.items()}},
                     ensure_ascii=False))
    for h in hang:
        if h[4]:
            print("   KHONG", json.dumps({"job": h[0], "buoc": h[1], "shell": h[2], "so_dong": h[3], "ly_do": h[4]}, ensure_ascii=False))
