import json
import re
import subprocess
from pathlib import Path


BASE = 'e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8'
HEAD = '4f648e5b784aa4e19f0385eee68cd75e69e1dd18'
MERGE = 'bac598d4e4ab9a50242e496405ec7548ba38b807'
CASE = 'wp433_bundled_tach_manh'
COMMANDS = {
    'eol': 'python .githooks/eol_policy_test.py',
    'bfc': 'python .github/checks/bundle_fragment_check.py --json',
    'selftest': 'python scripts/tl.py --selftest',
}
TIMESTAMP = re.compile(r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+Z ')
ANSI = re.compile(r'\x1b\[[0-9;]*m')


def unique_line(rows, expected):
    line, = [line for line, value in rows if value == expected]
    return line


def check_result(label, rows):
    if label == 'eol':
        assert sum(value.startswith('PASS ') for _, value in rows) == 32
        return f'32/32 dat @ {unique_line(rows, "32/32 dat")}'

    if label == 'selftest':
        total = unique_line(rows, '== tl selftest 1786/1786 ==')
        cases = [(line, value) for line, value in rows if total - 1786 <= line < total]
        assert len(cases) == 1786 and all(value.startswith('  [OK] ') for _, value in cases)
        fragment = unique_line(cases, f'  [OK] {CASE}')
        return f'1786/1786 @ {total}, final case block @ {cases[0][0]}–{cases[-1][0]}, fragment OK @ {fragment}'

    start = next(index for index, (_, value) in enumerate(rows) if value == '{')
    end = next(index for index, (_, value) in enumerate(rows) if value == '}')
    payload = json.loads('\n'.join(value for _, value in rows[start:end + 1]))
    assert payload['schema'] == 'bundle_fragment_check.v1'
    assert payload['ok'] is True and payload['failed'] == []
    assert len(payload['cases']) == payload['case_count'] == 20
    assert all(item['ok'] is True for item in payload['cases'])
    assert sum(item['test_id'] == CASE for item in payload['cases']) == 1
    return f'JSON @ {rows[start][0]}–{rows[end][0]}, ok=true, case_count=20, failed=[], fragment OK'


def step_payload(rows, command):
    start = unique_line(rows, f'##[group]Run {command}')
    assert rows[start][1] == command
    end = next(
        line for line, value in rows[start:]
        if value.startswith('##[group]Run ') or value == 'Post job cleanup.'
    )
    step = rows[start:end - 1]
    header_end = unique_line(step, '##[endgroup]')
    return start, end - 1, rows[header_end:end - 1]


for job in (136949922299, 136950323162):
    log = Path(f'bang-chung/job-{job}.log').read_text().splitlines()
    lines = [(n, TIMESTAMP.sub('', ANSI.sub('', value))) for n, value in enumerate(log, 1)]
    checkout = unique_line(lines, '[command]/usr/bin/git checkout --progress --force refs/remotes/pull/1496/merge')
    short_head = unique_line(lines, f'HEAD is now at {MERGE[:7]} Merge {HEAD} into {BASE}')
    full_head = unique_line(lines[short_head:short_head + 8], MERGE)
    assert not any(value.startswith('##[error]') or 'Process completed with exit code' in value for _, value in lines)
    print(f'CI {job}: checkout @ {checkout}, checkout HEAD @ {short_head}, full merge SHA @ {full_head}')
    if job == 136949922299:
        pr_head = unique_line(lines, '  PR_HEAD_SHA: ' + HEAD)
        unique_line(lines[pr_head - 20:pr_head], 'git cat-file -e "${PR_HEAD_SHA}^{commit}"')
        print(f'CI {job}: PR_HEAD_SHA @ {pr_head}')
        for label, command in COMMANDS.items():
            start, end, rows = step_payload(lines, command)
            print(f'CI {job}: {label} step @ {start}–{end}, {check_result(label, rows)}')
    else:
        start, end, rows = step_payload(lines, 'python ops/nhanh_don_duoc_test.py --gop-dich manh')
        joined = unique_line(rows, f'targeted_mutant_gate GOP 8/8 manh · head {MERGE}')
        assert any(value.startswith('targeted_mutant_gate: DAT') for _, value in rows)
        print(f'CI {job}: aggregate step @ {start}–{end}, 8/8 @ {joined}')


def show_evidence(name):
    return subprocess.check_output(
        ['git', '-C', 'kho', 'show', f'bc4fc8e:ops/handoff/wp433/r11-g1/do/{name}'],
        text=True,
    ).splitlines()


assert show_evidence('dinh-danh.txt') == [
    f'nen {BASE} shallow=false obj358451e8=commit',
    f'sau {HEAD} shallow=false obj358451e8=commit',
]
receipts = list(enumerate(show_evidence('tong.txt'), 1))
for side in ('nen', 'sau'):
    for label, command in COMMANDS.items():
        name = f'{side}-{label}'
        (line, receipt), = [row for row in receipts if row[1].startswith(name + ' | ')]
        _, rc, begin, end, actual = receipt.split(' | ')
        assert rc == 'rc=0' and actual == command.replace('python ', 'python3 ', 1)
        outcome = check_result(label, list(enumerate(show_evidence(name + '.out'), 1)))
        print(f'Executor {name}: tong.txt @ {line}, {rc}, {begin}–{end}, {outcome}')
