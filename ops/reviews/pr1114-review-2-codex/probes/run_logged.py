import json, os, pathlib, subprocess, sys, time
root = pathlib.Path(__file__).resolve().parents[1]
label, cwd, *cmd = sys.argv[1:]
out = root / 'evidence' / (label + '.log')
start = time.monotonic()
with out.open('w') as f:
    r = subprocess.run(cmd, cwd=root / cwd, stdout=f, stderr=subprocess.STDOUT,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', RUFF_NO_CACHE='true', GIT_OPTIONAL_LOCKS='0'))
result = dict(label=label, cwd=cwd, command=cmd, rc=r.returncode, seconds=round(time.monotonic()-start, 6), output=out.read_text())
(root / 'evidence' / (label + '.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False), flush=True)
raise SystemExit(r.returncode)
