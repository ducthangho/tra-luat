"""Doi chieu output GraphQL WorkflowRun.file do chu kho dan voi REST run + blob tai OID.
Dung: python3 -I moc_wd.py <thu_muc_do> <run_id> <oid> <tep_graphql_json>"""
import base64, hashlib, json, os, subprocess, sys, urllib.request
D, RUN, OID, G = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
API = "https://api.github.com/repos/ducthangho/tra-luat/"
H = {"Authorization": "Bearer " + os.environ["GITHUB_PAT"], "Accept": "application/vnd.github+json"}
KHO = "/home/user/tra-luat"


def get(p):
    with urllib.request.urlopen(urllib.request.Request(API + p, headers=H)) as r:
        return json.loads(r.read())


g = json.load(open(G, encoding="utf-8"))["data"]["node"]
run = get(f"actions/runs/{RUN}")
path = g["file"]["path"]
c = get(f"contents/{path}?ref={OID}")
blob_rest = c["sha"]
raw = base64.b64decode(c["content"])
blob_git = subprocess.run(["git", "-C", KHO, "rev-parse", f"{OID}:{path}"], capture_output=True, text=True, check=True).stdout.strip()
git_bytes = subprocess.run(["git", "-C", KHO, "cat-file", "blob", blob_git], capture_output=True, check=True).stdout
url_oid = g["file"]["repositoryFileUrl"].split("/blob/")[1].split("/")[0]
r = {
    "graphql_databaseId_khop_run": g["databaseId"] == RUN,
    "graphql_url_neo_oid": url_oid == OID,
    "graphql_checksuite_oid": g["checkSuite"]["commit"]["oid"] == OID,
    "rest_head_sha": run["head_sha"] == OID,
    "rest_path": run["path"] == path,
    "blob_rest_bang_git": blob_rest == blob_git,
    "bytes_rest_bang_git": raw == git_bytes,
}
with open(os.path.join(D, f"workflow-definition-{OID[:7]}.txt"), "w", encoding="utf-8") as f:
    f.write(f"# Moc Workflow definition §10.2.2 cho run {RUN} — doi chieu 2026-10-27 (cach do theo tien le pr870 moc_workflow_definition_20261026)\n\n")
    f.write(f"GraphQL (chu kho chay ngoai phien, ban chep: {os.path.basename(G)}): databaseId {g['databaseId']}, runNumber {g['runNumber']}, createdAt {g['createdAt']}\n")
    f.write(f"  file.path {path}\n  file.repositoryFileUrl {g['file']['repositoryFileUrl']} (OID trong URL: {url_oid})\n  checkSuite.commit.oid {g['checkSuite']['commit']['oid']}\n\n")
    f.write(f"REST GET actions/runs/{RUN}: head_sha {run['head_sha']}, path {run['path']}, run_attempt {run['run_attempt']}, node_id {run['node_id']} (= gia tri -f id= trong lenh dua chu kho chay), conclusion {run['conclusion']}\n")
    f.write(f"REST GET contents/{path}?ref={OID}: blob {blob_rest}, sha256 bytes {hashlib.sha256(raw).hexdigest()}\n")
    f.write(f"$ git rev-parse {OID}:{path}\n{blob_git}\nsha256 bytes git = {hashlib.sha256(git_bytes).hexdigest()}\n\n## Ket qua\n{json.dumps(r)}\n")
print(OID[:7], "OK" if all(r.values()) else "LECH", json.dumps(r), blob_git, hashlib.sha256(git_bytes).hexdigest(), run["node_id"])
