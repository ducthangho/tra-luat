"""Trich moi dong nhac wp1404/r1404 trong log mot job launcher cua run launcher-windows.yml. Dung: python trich_dong_khop.py <job_id> <tep_ra>"""
import hashlib, os, re, sys, urllib.error, urllib.request
J, OUT = sys.argv[1], sys.argv[2]
API = "https://api.github.com/repos/ducthangho/tra-luat"
H = {"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"}
class _K(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None
try:
    b = urllib.request.build_opener(_K).open(urllib.request.Request(f"{API}/actions/jobs/{J}/logs", headers=H), timeout=120).read()
except urllib.error.HTTPError as e:
    b = urllib.request.urlopen(e.headers["Location"], timeout=120).read()  # URL ky san, khong gui token
s = b.decode("utf-8", "replace")
dong = [ln for ln in s.splitlines() if re.search(r"wp1404|r1404|DA CHAY QUA|DOT BIEN:", ln)]
with open(OUT, "w", encoding="utf-8") as f:
    f.write(f"# job {J} log_sha256={hashlib.sha256(b).hexdigest()}; moi dong khop /wp1404|r1404|DA CHAY QUA|DOT BIEN:/ ({len(dong)} dong)\n")
    f.write("\n".join(dong) + "\n")
print(len(dong), sum("r387" in d for d in dong), sum("BO QUA" in d and "r387" in d for d in dong))
