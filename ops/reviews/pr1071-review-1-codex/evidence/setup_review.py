import json
import os
from pathlib import Path
import subprocess

s = Path(__file__).resolve().parent
r = s / 'cay-kho'
out = s / 'evidence'
out.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
def git(*args):
    return subprocess.check_output(['git', *args], cwd=r, env=env)
head = git('rev-parse', 'HEAD').decode().strip()
base = '97120d3c76ebb7c3eda4b585ff46f1c51e30c91b'
changed = git('diff', '--name-only', base, 'HEAD').decode().splitlines()
patch = git('diff', base, 'HEAD')
result = {'head': head, 'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
          'base': base, 'merge_base_origin_master': git('merge-base', 'HEAD', 'origin/master').decode().strip(),
          'parents': git('show', '-s', '--format=%P', 'HEAD').decode().strip(),
          'status': git('status', '--porcelain=v1', '--untracked-files=all').decode(),
          'core_abbrev': git('config', 'core.abbrev').decode().strip(),
          'changed_count': len(changed), 'outside_reviews': [p for p in changed if not p.startswith('ops/reviews/')],
          'patch_equal': patch == (s / 'DIFF.patch').read_bytes()}
(out / 'preflight.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
(out / 'changed-paths.txt').write_text('\n'.join(changed) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
for name, ref in [('base-copy', base), ('mutation-copy', head)]:
    dest = s / name
    if not dest.exists():
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', str(r), str(dest)], check=True, env=env)
        subprocess.run(['git', 'config', 'core.abbrev', '7'], cwd=dest, check=True, env=env)
        subprocess.run(['git', 'checkout', '--detach', ref], cwd=dest, check=True, env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    print(name, subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=dest, env=env).decode().strip())
