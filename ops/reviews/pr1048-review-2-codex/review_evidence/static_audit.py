import hashlib
import json
from pathlib import Path
import re
import subprocess

sandbox = Path(__file__).resolve().parent.parent
repo = sandbox / 'cay-kho'
evidence = sandbox / 'review_evidence'
commands = []
def run(args):
    p = subprocess.run(args, cwd=repo, capture_output=True)
    result = {'command': args, 'rc': p.returncode, 'stdout': p.stdout.decode('utf-8', 'replace'), 'stderr': p.stderr.decode('utf-8', 'replace')}
    commands.append(result)
    return p

base = '8cdb15a786304bab084b43c8b30c127ae87e2594'
previous = '16e992a01c0a4ec8cfcc793dac9c1def5e288ae8'
head = run(['git', 'rev-parse', 'HEAD']).stdout.decode().strip()
tree = run(['git', 'rev-parse', 'HEAD^{tree}']).stdout.decode().strip()
actual = run(['git', 'diff', base, 'HEAD'])
previous_diff = run(['git', 'diff', previous, 'HEAD'])
numstat = run(['git', 'diff', '--numstat', base, 'HEAD'])
diff_check = run(['git', 'diff', '--check', base, 'HEAD'])
ancestry = run(['git', 'merge-base', '--is-ancestor', base, 'HEAD'])
shallow = run(['git', 'rev-parse', '--is-shallow-repository'])
abbrev = run(['git', 'config', '--get', 'core.abbrev'])
ps_listing = run(['git', 'ls-files', '-z', '--', '*.ps1'])
tracked = sorted(x.decode() for x in ps_listing.stdout.split(b'\0') if x)
physical = sorted(p.relative_to(repo).as_posix() for p in repo.rglob('*') if p.is_file() and p.suffix.lower() == '.ps1' and '.git' not in p.relative_to(repo).parts)
scan = run(['rg', '-n', '-i', '--hidden', '--no-ignore', '-g', '!**/.git/**', '-g', '*.ps1', 'Get-Content', '.'])
(evidence / 'powershell-get-content.stdout').write_bytes(scan.stdout)
context_scan = run(['rg', '-n', '-i', 'Get-Content|Value cannot be null|null-valued|Ép.*string|ép.*kiểu|BOM|KHOA\\.txt|ErrorActionPreference|7\\.6\\.9|5\\.1\\.26100', 'CLAUDE.md', 'docs/', '-g', '*.md'])
(evidence / 'docs-context.stdout').write_bytes(context_scan.stdout)
casts = []
for rel in physical:
    content = (repo / rel).read_text(encoding='utf-8-sig')
    for match in re.finditer(r'\[string\]\s*\(\s*(?:`\s*)?Get-Content\b', content, re.I):
        line = content.count('\n', 0, match.start()) + 1
        lines = content.splitlines()
        casts.append({'file': rel, 'line': line, 'context': '\n'.join(f'{i+1}: {lines[i]}' for i in range(max(0,line-2), min(len(lines),line+5)))})
claude = (repo / 'CLAUDE.md').read_text(encoding='utf-8')
section = claude.split('- **PowerShell — 3 bẫy đã trả giá**',1)[1].split('\n- **',1)[0]
bullet_lines = [line for line in section.splitlines() if line.lstrip().startswith('·')]
lock_files = run(['git', 'ls-files', '--', '*KHOA.txt'])
report = {
    'head': head, 'tree': tree, 'base': base,
    'diff_patch_matches_git_bytes': actual.stdout == (sandbox / 'diff.patch').read_bytes(),
    'previous_diff_matches_git_bytes': previous_diff.stdout == (sandbox / 'diff-tu-luot-1.patch').read_bytes(),
    'numstat': numstat.stdout.decode().strip(), 'diff_check_rc': diff_check.returncode,
    'base_is_ancestor_rc': ancestry.returncode, 'shallow': shallow.stdout.decode().strip(),
    'core_abbrev': abbrev.stdout.decode().strip(),
    'ps1_tracked_count': len(tracked), 'ps1_physical_count': len(physical), 'ps1_inventory_equal': tracked == physical,
    'ps1_files': physical, 'cast_matches': casts,
    'powershell_bullet_count': len(bullet_lines), 'powershell_bullet_indents': [len(s)-len(s.lstrip()) for s in bullet_lines],
    'adr0057_exists': (repo / 'docs/adr/0057-windows-local-may-chu-kho.md').is_file(),
    'adr0058_exists': (repo / 'docs/adr/0058-windows-local-han-khoa-va-pham-vi-may.md').is_file(),
    'tracked_khoa_txt': lock_files.stdout.decode(),
    'prompt_sha256': hashlib.sha256((sandbox / 'run/33584cff/prompt.snapshot').read_bytes()).hexdigest(),
    'commands': commands,
}
(evidence / 'static-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['commands', 'ps1_files']}, ensure_ascii=False, indent=2))
