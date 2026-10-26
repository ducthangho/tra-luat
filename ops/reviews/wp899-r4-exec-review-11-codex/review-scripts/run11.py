import hashlib, json, os, pathlib, subprocess, sys, time
R = pathlib.Path(__file__).resolve().parent
(R / 'tmp').mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(R/'tmp'), TMP=str(R/'tmp'), TEMP=str(R/'tmp'))
label, *cmd = sys.argv[1:]
start = time.time()
p = subprocess.run(cmd, capture_output=True, env=env)
for kind, data in [('stdout', p.stdout), ('stderr', p.stderr)]:
    (R / f'{label}.{kind}.txt').write_bytes(data)
record = {'command': cmd, 'rc': p.returncode, 'elapsed_seconds': time.time()-start,
          'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(), 'stderr_sha256': hashlib.sha256(p.stderr).hexdigest()}
(R/f'{label}.json').write_text(json.dumps(record, indent=2))
print(json.dumps(record), flush=True)
print(p.stdout.decode('utf-8','replace')[-1500:])
print(p.stderr.decode('utf-8','replace')[-1000:])
sys.exit(p.returncode)
