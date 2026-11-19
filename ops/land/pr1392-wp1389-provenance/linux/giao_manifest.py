"""Giao tap ten tep cua mot merge (merge^1..merge) voi duong dan trong RELEASE_MANIFEST.json tai mot commit. Dung: python giao_manifest.py <merge> <commit_manifest>"""
import json, subprocess, sys
M, C = sys.argv[1], sys.argv[2]
man = json.loads(subprocess.run(["git", "show", f"{C}:RELEASE_MANIFEST.json"], capture_output=True, text=True, check=True).stdout)
paths = {f["path"] for f in man["files"]}
ch = subprocess.run(["git", "diff", "--name-only", f"{M}^1", M], capture_output=True, text=True, check=True).stdout.split()
print(f"manifest {C}: {len(paths)} duong dan; merge {M}: {len(ch)} tep; giao = {sorted(set(ch) & paths)}")
