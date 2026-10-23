"""Local read-only review runner; evidence is written outside cay-kho/."""
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT / "cay-kho"
REPORT = ROOT / "VERDICT.md"

def hunt(number, title, hypothesis, commands, conclusion):
    chunks = [f"\n### HƯỚNG {number}: {title}\n", f"  giả thuyết : {hypothesis}\n"]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", GIT_OPTIONAL_LOCKS="0")
    for command in commands:
        result = subprocess.run(command, cwd=REPO, env=env, shell=True,
                                executable="/bin/bash", text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        chunks += ["\n  lệnh (cwd=cay-kho/) :\n```bash\n", command, "\n```\n",
                   f"  output thật (rc={result.returncode}) :\n```text\n",
                   result.stdout, "\n```\n"]
        print(f"$ {command}\nrc={result.returncode}\n{result.stdout}", flush=True)
    chunks += [f"\n  kết luận : {conclusion}\n"]
    with REPORT.open("a") as report:
        report.write("".join(chunks))

def row(claim, declared, measured, matches):
    fields = [claim, declared, measured, matches]
    line = "| " + " | ".join(x.replace("|", "&#124;").replace("\n", "<br>") for x in fields) + " |\n"
    content = REPORT.read_text()
    marker = "\n## BẢNG SĂN"
    content = content.replace(marker, line + marker, 1)
    REPORT.write_text(content)
