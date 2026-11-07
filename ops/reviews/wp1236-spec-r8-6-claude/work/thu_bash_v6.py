"""Bash/dash THẬT trên ba thân một dòng KHÔNG LF (dạng `run:` plain scalar của YAML): chương trình hỏng thoát 1 rồi `|| :`/`|| true`/`|| exit 0`.
Dùng ĐÚNG ba dòng lệnh GitHub. Chạy: python3 -I thu_bash_v6.py"""
import json, os, pathlib, subprocess, sys, tempfile
SH = {None: ["/usr/bin/bash", "-e"], "bash": ["/usr/bin/bash", "--noprofile", "--norc", "-eo", "pipefail"], "sh": ["/bin/sh", "-e"]}
kq = {}
for than in ["python ops/hong.py || :", "python ops/hong.py || true", "python ops/hong.py || exit 0"]:
    for sh, lenh in SH.items():
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d); (p / "ops").mkdir(); (p / "bin").mkdir(); os.symlink(sys.executable, p / "bin/python")
            (p / "ops/hong.py").write_text("import pathlib, sys; pathlib.Path('DA_CHAY').touch(); sys.exit(1)\n")
            (p / "s.sh").write_text(than)
            rc = subprocess.run(lenh + [str(p / "s.sh")], cwd=d, env={"PATH": f"{p}/bin:/usr/bin:/bin", "HOME": d}, capture_output=True,
                                stdin=subprocess.DEVNULL).returncode
            kq[f"{than} | {sh}"] = {"rc": rc, "DA_CHAY": (p / "DA_CHAY").exists()}
            print(f"{than:32} shell={str(sh):5} rc={rc} DA_CHAY={(p / 'DA_CHAY').exists()}")
json.dump(kq, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "thu_bash_v6.json"), "w"), ensure_ascii=False, indent=1)
