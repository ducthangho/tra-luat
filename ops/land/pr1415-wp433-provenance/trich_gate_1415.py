"""Trich log job gate (ubuntu-latest) cua run ci.yml tren 417b593: dong tl selftest va buoc release-verify strict (lane LAND) toi het log.
Dung: python trich_gate_1415.py <job_id> <run_id> <tep_ra>. Redirect log theo tay, khong gui token sang kho blob."""
import hashlib, os, re, sys, urllib.error, urllib.request
J, R, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
API = "https://api.github.com/repos/ducthangho/tra-luat"
H = {"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"}
class _K(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None
try:
    b = urllib.request.build_opener(_K).open(urllib.request.Request(f"{API}/actions/jobs/{J}/logs", headers=H), timeout=120).read()
except urllib.error.HTTPError as e:
    b = urllib.request.urlopen(e.headers["Location"], timeout=120).read()  # URL ky san, khong gui token
ls = b.decode("utf-8", "replace").splitlines()
out = [f"# trich log job {J} gate (ubuntu-latest), run {R} attempt 1, head 417b593; log_sha256={hashlib.sha256(b).hexdigest()}",
       "", "# (a) moi dong '== tl selftest' va '[FAIL]' cua log"]
out += [x for x in ls if "== tl selftest" in x or "[FAIL]" in x]
i = next(k for k, x in enumerate(ls) if "##[group]Run python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json" in x)
out += ["", "# (b) tu dong buoc release-verify LAND toi het log"] + ls[i:]
open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out))
