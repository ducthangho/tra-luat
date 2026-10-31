import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys

SANDBOX = Path(__file__).resolve().parent.parent
REPO = SANDBOX / 'cay-kho'
OUT = SANDBOX / 'review_evidence'
HEAD = '6f23a4e68805b4af3e2efe77be6e10b513843e93'
BASE = '5a174b958a05e13f5c9a968a2596ca37267d0466'
PREV = '48b54d89b152871063c7296df33a60308667599e'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')


def command(name, args):
    run = subprocess.run(args, cwd=REPO, env=ENV, capture_output=True)
    (OUT / (name + '.stdout')).write_bytes(run.stdout)
    (OUT / (name + '.stderr')).write_bytes(run.stderr)
    record = {'cwd': str(REPO), 'argv': args, 'rc': run.returncode,
              'stdout_file': name + '.stdout', 'stderr_file': name + '.stderr',
              'stdout_bytes': len(run.stdout), 'stderr_bytes': len(run.stderr)}
    (OUT / (name + '.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    return run


def git(*args):
    run = subprocess.run(['git', *args], cwd=REPO, env=ENV, capture_output=True, check=True)
    return run.stdout


def snapshot():
    files = {}
    for directory, dirs, names in os.walk(REPO):
        dirs[:] = sorted(d for d in dirs if d != '.git')
        for name in sorted(names):
            path = Path(directory) / name
            mode = path.lstat().st_mode
            data = os.fsencode(os.readlink(path)) if stat.S_ISLNK(mode) else path.read_bytes()
            files[path.relative_to(REPO).as_posix()] = [stat.S_IMODE(mode), hashlib.sha256(data).hexdigest()]
    return {'files': files, 'head': git('rev-parse', 'HEAD').decode().strip(),
            'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
            'index_sha256': hashlib.sha256((REPO / '.git/index').read_bytes()).hexdigest(),
            'status': git('status', '--porcelain=v1', '--untracked-files=all', '--ignored').decode()}


def tree(sha):
    records = git('ls-tree', '-r', '-z', sha).split(b'\0')
    return {r.split(b'\t', 1)[1].decode(): r.split(b'\t', 1)[0].decode() for r in records if r}


def static_audit():
    before = snapshot()
    (OUT / 'before.json').write_text(json.dumps(before, ensure_ascii=False, indent=2) + '\n')
    h, m, p = tree(HEAD), tree(BASE), tree(PREV)
    outside = sorted(k for k in h.keys() | m.keys() if h.get(k) != m.get(k) and k != 'CLAUDE.md')
    since_previous = sorted(k for k in h.keys() | p.keys() if h.get(k) != p.get(k))
    not_from_master = [k for k in since_previous if h.get(k) != m.get(k)]
    patch = command('head-diff', ['git', 'diff', BASE, HEAD])
    prev_patch = command('claude-since-previous', ['git', 'diff', PREV, HEAD, '--', 'CLAUDE.md'])
    files_disk = sorted(k for k in before['files'] if k.lower().endswith('.ps1'))
    files_git = sorted(k for k in h if k.lower().endswith('.ps1'))
    content_lines = []
    casts = []
    for name in files_disk:
        raw = (REPO / name).read_text(encoding='utf-8-sig')
        for number, line in enumerate(raw.splitlines(), 1):
            if re.search(r'Get-Content', line, re.I):
                content_lines.append(f'{name}:{number}:{line}')
        for match in re.finditer(r'\[string\](?:\s|`)*\((?:\s|`)*Get-Content\b', raw, re.I):
            number = raw.count('\n', 0, match.start()) + 1
            casts.append({'file': name, 'line': number, 'excerpt': raw[match.start():match.start()+500]})
    (OUT / 'powershell-get-content.stdout').write_text('\n'.join(content_lines) + '\n')
    report = {'head': before['head'], 'tree': before['tree'],
              'parents': git('show', '-s', '--format=%P', HEAD).decode().strip().split(),
              'base_merge_base': git('merge-base', HEAD, BASE).decode().strip(),
              'previous_master_merge_base': git('merge-base', PREV, BASE).decode().strip(),
              'merge_commit_parents': git('show', '-s', '--format=%P', 'b653574b117fa1496fbf58f09a22a8cbed5cc5dc').decode().strip().split(),
              'diff_matches_patch_bytes': patch.returncode == 0 and patch.stdout == (SANDBOX / 'diff.patch').read_bytes(),
              'diff_sha256': hashlib.sha256(patch.stdout).hexdigest(),
              'diff_numstat': git('diff', '--numstat', BASE, HEAD).decode(),
              'claude_since_previous_empty': prev_patch.returncode == 0 and not prev_patch.stdout,
              'head_vs_master_other_paths': outside,
              'changed_since_previous_count': len(since_previous),
              'changed_since_previous_not_from_master': not_from_master,
              'changed_since_previous_paths': since_previous,
              'powershell_tracked_files': files_git,
              'powershell_disk_files': files_disk,
              'powershell_file_lists_equal': files_git == files_disk,
              'powershell_get_content_line_count': len(content_lines),
              'powershell_expression_casts': casts,
              'pwsh': shutil.which('pwsh'), 'powershell': shutil.which('powershell'),
              'snapshot_file_count': len(before['files']), 'initial_status': before['status']}
    (OUT / 'static-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    summary = {k: v for k, v in report.items() if k not in ['changed_since_previous_paths', 'powershell_expression_casts']}
    summary['powershell_expression_casts'] = [{k: x[k] for k in ['file', 'line']} for x in casts]
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def checks():
    commands = [
        ('doctrine-scan', ['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.']),
        ('adr-song', ['python3', '.claude/dev/packet_loop.py', 'adr-song', '--root', '.']),
        ('doc-claims-check', ['python3', 'scripts/tl.py', 'doc-claims-check', '--json']),
        ('diff-check', ['git', 'diff', '--check', BASE, HEAD]),
    ]
    results = []
    for name, args in commands:
        run = command(name, args)
        info = {'name': name, 'argv': args, 'rc': run.returncode,
                'stderr': run.stderr.decode(errors='replace')}
        if name == 'doc-claims-check':
            doc = json.loads(run.stdout)
            info['result'] = {k: doc.get(k) for k in ['ok', 'files_scanned', 'claims_flagged', 'flags', 'advisory_count', 'layers_skipped']}
        else:
            info['stdout'] = run.stdout.decode(errors='replace')
        results.append(info)
        print(json.dumps(info, ensure_ascii=False))
    after = snapshot()
    before = json.loads((OUT / 'before.json').read_text())
    (OUT / 'after.json').write_text(json.dumps(after, ensure_ascii=False, indent=2) + '\n')
    results.append({'checkout_unchanged': before == after, 'file_count': len(after['files']),
                    'final_status': after['status'], 'head': after['head'], 'tree': after['tree']})
    (OUT / 'checks.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(results[-1], ensure_ascii=False))


if __name__ == '__main__':
    {'static': static_audit, 'checks': checks}[sys.argv[1]]()
