"""trich_rv.py <job_id> <run_id> <sha> <tep_ra>: tai log job (GITHUB_PAT), in sha256 + cac dong selftest / release-verify / ok / failed / error."""
import hashlib, os, re, sys, urllib.request, urllib.error
J, R, SHA, OUT = sys.argv[1:5]
class _K(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
try:
    with urllib.request.build_opener(_K).open(urllib.request.Request(f"https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/{J}/logs", headers={"Authorization": "Bearer " + os.environ["GITHUB_PAT"]}), timeout=60) as r0:
        b = r0.read()                      # may chu tra thang 200 (khong chuyen huong)
except urllib.error.HTTPError as e:
    if e.code not in (301, 302, 303, 307, 308): raise
    with urllib.request.urlopen(e.headers["Location"], timeout=60) as r:   # URL ky san, KHONG gui token
        b = r.read()
dong = b.decode("utf-8", "replace").splitlines()
pat = re.compile(r"== tl selftest|release-verify RELEASE_MANIFEST.json --strict|\"ok\": false|\"expected_file_count\"|\"checked_file_count\"|\"path\": \"scripts/tl_|##\[error\]")
with open(OUT, "w", encoding="utf-8") as f:
    f.write(f"# trich log job {J} gate (ubuntu-latest), run {R} push master {SHA[:7]}; log_sha256={hashlib.sha256(b).hexdigest()}\n")
    for i, l in enumerate(dong, 1):
        if pat.search(l):
            f.write(f"{i}: {re.sub(r'^[0-9T:.Z-]+ ', '', l)}\n")
print("ok", len(dong))
