"""Do 3/4 moc §10.2.2 (Run, Checkout, Gate output) cho mot run gate push master; Workflow definition = not_measured.
Cach do theo ho so pr931 (PR #937). Dung: python3 -I bon_moc.py <thu_muc_provenance> <run_id> <merge_sha> <job_id> <artifact_id>
Ghi vao <thu_muc>/do-1026-<sha7>/: bon-moc-10-2-2.txt, log-gate-<job>-trich.txt, readback-artifacts-<run>.json,
artifact-<id>/<tep giai nen>. Khong kem zip va log day du (chi sha256)."""
import datetime, hashlib, io, json, os, re, subprocess, sys, urllib.error, urllib.request, zipfile
NGAY = datetime.datetime.now(datetime.timezone.utc)

P, RUN, M, JOB, ART = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
API = "https://api.github.com/repos/ducthangho/tra-luat/"
H = {"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"}
KHO = "/home/user/tra-luat"


class _KhongTheo(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def get(path, raw=False):
    if raw:  # artifact/log: 302 sang kho blob — tai URL dich KHONG kem token (giong curl -L)
        try:
            urllib.request.build_opener(_KhongTheo).open(urllib.request.Request(API + path, headers=H))
            raise RuntimeError("khong co redirect")
        except urllib.error.HTTPError as e:
            if e.code not in (301, 302, 303, 307):
                raise
            with urllib.request.urlopen(e.headers["Location"]) as r:
                return r.read()
    with urllib.request.urlopen(urllib.request.Request(API + path, headers=H)) as r:
        return json.loads(r.read())


def git(*a):
    return subprocess.run(["git", "-C", KHO, *a], capture_output=True, text=True, check=True).stdout.strip()


s7 = M[:7]
D = os.path.join(P, f"do-{NGAY:%m%d}-{s7}")
os.makedirs(D, exist_ok=True)
run = get(f"actions/runs/{RUN}")
assert run["head_sha"] == M and run["event"] == "push" and run["conclusion"] == "success", run["head_sha"]
arts = get(f"actions/runs/{RUN}/artifacts?per_page=100")
with open(os.path.join(D, f"readback-artifacts-{RUN}.json"), "w", encoding="utf-8") as f:
    json.dump(arts, f, ensure_ascii=False, indent=1); f.write("\n")
a = [x for x in arts["artifacts"] if x["id"] == ART][0]
z = get(f"actions/artifacts/{ART}/zip", raw=True)
zh = hashlib.sha256(z).hexdigest()
assert a["digest"] == "sha256:" + zh, (a["digest"], zh)
AD = os.path.join(D, f"artifact-{ART}")
os.makedirs(AD, exist_ok=True)
zf = zipfile.ZipFile(io.BytesIO(z))
tep = {}
for n in zf.namelist():
    b = zf.read(n)
    with open(os.path.join(AD, os.path.basename(n)), "wb") as f:
        f.write(b)
    tep[os.path.basename(n)] = b
jn = [k for k in tep if k.endswith(".json")][0]
on = [k for k in tep if k.endswith(".out")][0]
j = json.loads(tep[jn])
out_h = hashlib.sha256(tep[on]).hexdigest()
log = get(f"actions/jobs/{JOB}/logs", raw=True)
lt = log.decode("utf-8", "replace").splitlines()
trich, kq = [], {}
for i, l in enumerate(lt, 1):
    if i <= 18 and re.search(r"Runner Image Provisioner|Version:|Operating System|Ubuntu|24\.04|Image:", l):
        trich.append(f"{i}:{l}")
for i, l in enumerate(lt):
    if l.endswith("[command]/usr/bin/git log -1 --format=%H") and i + 1 < len(lt):
        trich.append(f"{i + 1}:{l}"); trich.append(f"L: {lt[i + 1]}"); kq["checkout"] = lt[i + 1].split()[-1]
    m = re.search(r"\b(head_sha|base_sha) = ([0-9a-f]{40})$", l)
    if m:
        trich.append(f"L: {l}"); kq[m[1]] = m[2]
    if re.search(r"== tl selftest \d+/\d+ ==", l):
        trich.append(f"L: {l}")
with open(os.path.join(D, f"log-gate-{JOB}-trich.txt"), "w", encoding="utf-8") as f:
    f.write(f"# trich log job {JOB} 'gate (ubuntu-latest)' run {RUN} attempt {run['run_attempt']} (REST /actions/jobs/{JOB}/logs)\n")
    f.write(f"# log day du: {len(log)} byte, sha256 {hashlib.sha256(log).hexdigest()} (khong kem — qua lon; tai lai duoc toi khi het han luu log)\n")
    f.write("\n".join(trich) + "\n")
ci = {c: git("rev-parse", f"{c}:.github/workflows/ci.yml") for c in (M, M + "^1", M + "^2")}
blob = ci[M]
blob_sha = hashlib.sha256(subprocess.run(["git", "-C", KHO, "cat-file", "blob", blob], capture_output=True, check=True).stdout).hexdigest()
ident = j.get("identity") or {}
r = {
    "checkout_log": kq.get("checkout") == M, "head_sha_log": kq.get("head_sha") == M,
    "artifact_identity_head": ident.get("head_sha") == M, "artifact_identity_tree": ident.get("tree_sha") == git("rev-parse", M + "^{tree}"),
    "cay_sach": bool(ident.get("tracked_clean")) and bool(ident.get("worktree_clean")),
    "output_sha_khop": out_h == j.get("output_sha256"), "rc0": j.get("returncode") == 0, "positive": j.get("positive_verified") is True,
    "identity_after_bang": j.get("identity_after") == j.get("identity"),
}
with open(os.path.join(D, "bon-moc-10-2-2.txt"), "w", encoding="utf-8") as f:
    f.write(f"# 4 moc §10.2.2 cho ci.yml push master run {RUN} attempt {run['run_attempt']} tren {s7} — do {NGAY:%Y-%m-%d}, cach do theo ho so pr931 (PR #937)\n\n")
    f.write("## Run\n" + f"REST run {RUN}: event {run['event']}, attempt {run['run_attempt']}, head {run['head_sha']}, conclusion {run['conclusion']}, path {run['path']}\n\n")
    f.write("## Checkout (git, ban sao day du)\n" + f"$ git rev-parse {s7}^{{commit}} {s7}^{{tree}} {s7}^1 {s7}^2\n")
    f.write("\n".join(git("rev-parse", M + "^{commit}", M + "^{tree}", M + "^1", M + "^2").split()) + "\n")
    f.write(f"log job {JOB}: git log -1 sau checkout = {kq.get('checkout')}; head_sha = {kq.get('head_sha')}; base_sha = {kq.get('base_sha')}\n\n")
    f.write("## Gate output — artifact\n" + f"sha256 zip tai tu REST /actions/artifacts/{ART}/zip = {zh}\ndigest REST: {a['digest']} (readback-artifacts-{RUN}.json)\n")
    f.write(f"zip KHONG kem; tep giai nen nguyen byte vao artifact-{ART}/ ({', '.join(sorted(tep))}).\n")
    f.write(f"{on} sha256 {out_h} == output_sha256 trong json: {out_h == j.get('output_sha256')}\n")
    f.write("json: " + str({k: j.get(k) for k in ("status", "returncode", "positive_verified", "positive_match", "command")}) + "\n")
    f.write("json.identity: " + str({k: ident.get(k) for k in ("head_sha", "tree_sha", "tracked_clean", "worktree_clean", "system", "system_release", "python_version")}) + "\n")
    f.write(f"identity_after == identity: {r['identity_after_bang']}\n\n")
    f.write("## Workflow definition\nnot_measured — GraphQL WorkflowRun.file bi 403 trong phien Claude Code tren web (cung ly do ho so pr931).\n")
    f.write("Bang chung phu (KHONG thay cho exact definition OID):\n" + f"REST run path: {run['path']}, referenced_workflows: {run.get('referenced_workflows')}\n")
    for c, b in ci.items():
        f.write(f"blob ci.yml tai {c[:7] if '^' not in c else s7 + c[40:]} = {b}\n")
    f.write(f"sha256 bytes blob {blob[:8]}… = {blob_sha}\n\n## Ket qua\n" + json.dumps(r, ensure_ascii=False) + "\n")
print(s7, "OK" if all(r.values()) else "LECH", json.dumps(r), "zip", zh[:8], "out", out_h[:8], "marker", j.get("positive_match", "").strip(), "blob", blob[:8], "env", ident.get("system_release"), ident.get("python_version"))
