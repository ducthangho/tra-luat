#!/usr/bin/env python3
"""luu.py ROUND RUN_SHORT_ID REVIEWED_SHA — luu verdict luot ROUND vao nhanh ops/review-674-ci-duong-nhanh (clone tam), day len."""
import hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path
S = Path("/tmp/claude-0/-home-user-tra-luat/7ccc7ea3-39e6-5592-a374-909e124275e1/scratchpad")
rd, sid, sha = sys.argv[1:4]
R = S / f"rv{rd}"
run = json.loads((S / "runs" / sid / "run.json").read_text(encoding="utf-8"))
def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
BR = "ops/review-674-ci-duong-nhanh"
def sh(*a, cwd=None):
    r = subprocess.run(a, cwd=cwd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(f"{a} rc={r.returncode}: {r.stderr[:300]}")
    return r.stdout.strip()
tam = Path(tempfile.mkdtemp(dir=S, prefix="luu_"))
sh("git", "clone", "-q", "--no-local", "/home/user/tra-luat", str(tam / "k"))
k = tam / "k"
ls = sh("git", "ls-remote", "--heads", "https://github.com/ducthangho/tra-luat.git", BR) if False else ""
have = subprocess.run(["git", "-C", "/home/user/tra-luat", "ls-remote", "--heads", "origin", BR], capture_output=True, text=True).stdout.strip()
sh("git", "remote", "set-url", "origin", sh("git", "-C", "/home/user/tra-luat", "remote", "get-url", "origin"), cwd=k)
if have:
    sh("git", "fetch", "-q", "origin", BR, cwd=k); sh("git", "checkout", "-q", "-b", BR, "FETCH_HEAD", cwd=k)
else:
    sh("git", "fetch", "-q", "origin", "master", cwd=k); sh("git", "checkout", "-q", "-b", BR, "FETCH_HEAD", cwd=k)
sh("git", "remote", "set-url", "origin", sh("git", "-C", "/home/user/tra-luat", "remote", "get-url", "origin"), cwd=k)
d = k / "ops" / "reviews" / "ci-duong-nhanh-674"
d.mkdir(parents=True, exist_ok=True)
v = d / f"luot-{rd}-verdict.md"
shutil.copyfile(R / "out" / "VERDICT.md", v)
if (R / "out" / "HINT.patch").exists():
    shutil.copyfile(R / "out" / "HINT.patch", d / f"luot-{rd}-HINT.patch")
prompt = R / "PROMPT.md"
bn = d / f"luot-{rd}-bien-nhan.yaml"
bn.write_text(f"""# Bien nhan luot review {rd} — packet #674 CI-DUONG-NHANH-HO-SO. Nguon co tham quyen = tep verdict (co bam); comment tren Issue chi la ban chieu.
luot: {rd}
reviewed_sha: {sha}
reviewer: codex (OpenAI Codex CLI)
model_yeu_cau: gpt-6-astra
effort_yeu_cau: high
model_thuc_chay: KHONG DO DUOC (codex khong xuat modelUsage; header stderr chi la khai cua CLI)
run_short_id: {sid}
run_id: {run.get('run_id')}
trang_thai: {run.get('trang_thai')}
ma_thoat: {run.get('ma_thoat')}
thoi_luong_giay: {run.get('thoi_luong_giay')}
stdout_byte: {run.get('stdout_byte')}
stderr_byte: {run.get('stderr_byte')}
prompt_sha256: {h(prompt)}
verdict_tep: ops/reviews/ci-duong-nhanh-674/luot-{rd}-verdict.md
verdict_sha256: {h(v)}
verdict_bytes: {v.stat().st_size}
ghi_chu: run.json nam ngoai kho (scratchpad phien thi cong); scalar tren chep tu do, khong tu doi chieu duoc tu kho.
""", encoding="utf-8")
sh("git", "add", "-A", cwd=k)
sh("git", "-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com", "commit", "-q", "-m",
   f"review(#674): luu verdict Codex luot {rd} (reviewed {sha[:7]}) + bien nhan co bam\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01BxzKQaSmg6qVeSaQWH4dr5", cwd=k)
sh("git", "push", "-q", "origin", BR, cwd=k)
print(sh("git", "rev-parse", "HEAD", cwd=k), h(v), v.stat().st_size)
