import ast
from fnmatch import fnmatchcase
import json
import re
import subprocess

import yaml

SHA = '06a50c5feea77c2654f31edd26efeed7eeee62f5'
def show(path):
    return subprocess.check_output(['git', 'show', f'{SHA}:{path}'], text=True)

paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', SHA, '.github/workflows'], text=True).splitlines()
assert len(paths) == 7
for path in paths:
    wf = yaml.safe_load(show(path))
    events = wf.get('on', wf.get(True))  # PyYAML YAML 1.1 parses the key on as True
    print(f'{path}: name={wf["name"]} events={json.dumps(events, ensure_ascii=False)}')
    for name, job in wf['jobs'].items():
        print(f'  {name}: runs-on={job.get("runs-on")} matrix={job.get("strategy", {}).get("matrix", {})} if={job.get("if", "(none)")}')
        if path not in ('.github/workflows/ci.yml', '.github/workflows/launcher-windows.yml'):
            assert job['runs-on'] == 'ubuntu-latest'

launcher = yaml.safe_load(show('.github/workflows/launcher-windows.yml'))
events = launcher.get('on', launcher.get(True))
job = launcher['jobs']['launcher']
assert events['push']['branches'] == ['master']
assert events['push']['paths'] == ['.claude/dev/**', '.github/workflows/launcher-windows.yml']
assert events['pull_request']['types'] == ['opened', 'synchronize', 'reopened', 'labeled']
assert events['pull_request']['paths'] == ['.claude/dev/**']
assert 'contains(github.event.pull_request.labels.*.name' in job['if']
assert "github.event_name != 'pull_request'" in job['if']
matrix = job['strategy']['matrix']['os']
assert matrix == '${{ fromJSON(github.event_name == \'workflow_dispatch\' && inputs.runner_set == \'windows-only\' && \'["windows-latest"]\' || \'["windows-latest","ubuntu-latest"]\') }}'
print('launcher paths/types/job-if/matrix: exact assertions PASS')
for event, paths_changed, labels, runner_set in [
    ('push', ['CLAUDE.md'], [], None),
    ('push', ['.claude/dev/launcher.py'], [], None),
    ('push', ['.github/workflows/launcher-windows.yml'], [], None),
    ('pull_request', ['.claude/dev/launcher.py'], [], None),
    ('pull_request', ['.claude/dev/launcher.py'], ['windows'], None),
    ('pull_request', ['.github/workflows/launcher-windows.yml'], ['windows'], None),
    ('workflow_dispatch', ['CLAUDE.md'], [], 'windows-only'),
    ('workflow_dispatch', ['CLAUDE.md'], [], 'windows-and-ubuntu'),
]:
    triggered = event == 'workflow_dispatch' or any(fnmatchcase(p, pattern) for p in paths_changed for pattern in events[event]['paths'])
    allowed = event != 'pull_request' or 'windows' in labels
    os = ['windows-latest'] if event == 'workflow_dispatch' and runner_set == 'windows-only' else ['windows-latest', 'ubuntu-latest']
    print(f'launcher modeled event={event} paths={paths_changed} labels={labels} runner_set={runner_set}: triggered={triggered} job_allowed={allowed} selected_os={os if triggered and allowed else []}')
print('launcher executable steps:')
for step in job['steps']:
    if 'run' in step:
        print(' ', step.get('name', '(unnamed)'), ':', step['run'].splitlines()[0])
ci = yaml.safe_load(show('.github/workflows/ci.yml'))
ci_events = ci.get('on', ci.get(True))
assert ci_events['pull_request'] is None
print(f'ci pull_request config={ci_events["pull_request"]!r}; explicit types absent=True; labeled absent=True')
for job_name, ci_job in ci['jobs'].items():
    for step in ci_job.get('steps', []):
        if step.get('name') == 'PR head contains required EOL base':
            print(f'EOL step in {job_name}: if={step["if"]}')
            condition = step['if'].strip()
            if condition.startswith('${{') and condition.endswith('}}'):
                condition = condition[3:-2].strip()
            assert condition == "github.event_name == 'pull_request'"
