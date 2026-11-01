import shutil
from audit_common import *

config = S / 'audit.gitconfig'
p = run(['git', 'config', '--file', str(config), 'core.abbrev', '7'], S)
assert p.returncode == 0
assert git('config', '--get', 'core.abbrev').strip() == b'7'
save('original-snapshot.json', snapshot())
paths = git('diff', '--name-only', BASE, 'HEAD').decode().splitlines()
pre = dict(head=git('rev-parse', 'HEAD').decode().strip(),
           tree=git('rev-parse', 'HEAD^{tree}').decode().strip(),
           merge_base=git('merge-base', 'HEAD', 'origin/master').decode().strip(),
           status=git('status', '--porcelain=v1', '--untracked-files=all', '--ignored').decode(),
           branch=run(['git', 'symbolic-ref', '-q', 'HEAD']).returncode,
           changed_count=len(paths), changed_paths=paths,
           outside_reviews=[x for x in paths if not x.startswith('ops/reviews/')],
           patch_equal=git('diff', BASE, 'HEAD') == (S / 'DIFF.patch').read_bytes(),
           core_abbrev=git('config', '--get', 'core.abbrev').decode().strip())
save('preflight.json', pre)
assert pre['head'] == HEAD and pre['merge_base'] == BASE
assert not pre['status'] and not pre['outside_reviews'] and pre['patch_equal']
print(json.dumps({k: v for k, v in pre.items() if k != 'changed_paths'}, ensure_ascii=False), flush=True)
(S / 'work').mkdir(exist_ok=True)
for label, ref in [('head', HEAD), ('base', BASE), ('mutant', HEAD)]:
    target = S / 'work' / label
    if not target.exists():
        shutil.copytree(REPO, target)
    assert run(['git', 'checkout', '--detach', ref], target).returncode == 0
    assert run(['git', 'config', 'core.abbrev', '7'], target).returncode == 0
    assert not git('status', '--porcelain=v1', cwd=target).strip()
    print(f'prepared {label}: {ref}', flush=True)
