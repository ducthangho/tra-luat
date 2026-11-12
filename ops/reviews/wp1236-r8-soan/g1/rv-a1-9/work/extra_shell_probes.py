"""Offline K7 measurements; executed scripts contain only false/true/cat/control flow."""
import importlib.util
import json
import os
import subprocess
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
WORK, REPO = BASE / 'work', BASE / 'repo'
os.environ.update(TMPDIR=str(WORK / 'tmp'), PYTHONDONTWRITEBYTECODE='1',
                  GIT_OPTIONAL_LOCKS='0', GIT_CONFIG_GLOBAL='/dev/null')
tempfile.tempdir = str(WORK / 'tmp')
spec = importlib.util.spec_from_file_location('test_extra_shell', REPO / 'ops/gate_output_doi_chieu_test.py')
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
m = t.nap()
text, p = t.f_ok()
CMD = 'python .claude/dev/packet_loop_test.py'
PIPE = CMD + ' | cat'
R = '        run: ' + CMD + '\n'

def variant(run, shell='bash', env=None):
    block = (f'        shell: {shell}\n' if shell is not None else '')
    if env:
        block += '        env:\n' + ''.join(f'          {k}: {json.dumps(v)}\n' for k, v in env.items())
    block += '        run: |\n' + ''.join('          ' + line + '\n' for line in run.splitlines())
    return t.bien_the_yaml(p, lambda s: s.replace(R, block))

# Normal shell grammar, no destructive or external operations.
cases = [
    ('straight', PIPE, 'bash', None, True),
    ('if_condition', f'if {PIPE}; then\n  true\nfi', 'bash', None, True),
    ('while_condition', f'while {PIPE}; do\n  break\ndone', 'bash', None, True),
    ('until_condition', f'until {PIPE}; do\n  break\ndone', 'bash', None, True),
    ('and_list', f'{PIPE} && true\ntrue', 'bash', None, True),
    ('or_list', f'{PIPE} || true', 'bash', None, True),
    ('negated_pipeline', f'! {PIPE}\ntrue', 'bash', None, True),
    ('background_pipeline', f'{PIPE} &\nwait', 'bash', None, True),
    ('for_body', f'for x in one; do\n  {PIPE}\ndone', 'bash', None, True),
    ('for_or', f'for x in one; do\n  {PIPE}\ndone || true', 'bash', None, True),
    ('case_body', f'case x in\n  x) {PIPE} ;;\nesac', 'bash', None, True),
    ('trap_success', f"trap 'exit 0' ERR\n{PIPE}", 'bash', None, True),
    ('trap_no_override', f"trap ':' ERR\n{PIPE}", 'bash', None, True),
    ('alias_unused', f'alias nothing=true\n{PIPE}', 'bash', None, True),
    ('exec_redirect', f'exec 3>/dev/null\n{PIPE}', 'bash', None, True),
    ('source_after_separator', f'true; . /dev/null\n{PIPE}', 'bash', None, True),
    ('source_with_args', f'true; . /dev/null +o pipefail\n{PIPE}', 'bash', None, True),
    ('env_shellopts', PIPE, 'bash', {'SHELLOPTS': 'braceexpand:hashall:interactive-comments'}, False),
    ('env_bash_env', PIPE, 'bash', {'BASH_ENV': '/dev/null'}, False),
    ('custom_bash_e', PIPE, 'bash -e {0}', None, False),
    ('custom_bash', PIPE, 'bash {0}', None, False),
    ('custom_bash_pipefail', PIPE, 'bash --noprofile --norc -eo pipefail {0}', None, False),
    ('implicit', PIPE, None, None, True),
    ('explicit_sh', PIPE, 'sh', None, True),
    ('no_pipe_straight', CMD + '\ntrue', 'bash', None, True),
    ('no_pipe_if', f'if {CMD}; then\n  true\nfi', 'bash', None, True),
]
rows = []
for name, run, shell, env, execute in cases:
    result = m.kiem(text, variant(run, shell, env), t.goc())
    row = {'name': name, 'shell': shell, 'run': run, 'env': env,
           'mode_result': m.che_do_shell(run, shell), 'gate_result': result}
    if execute:
        args = ['sh', '-e'] if shell == 'sh' else ['bash', '--noprofile', '--norc', '-e']
        if shell == 'bash':
            args += ['-o', 'pipefail']
        proc = subprocess.run(args + ['-c', run.replace(CMD, 'false')], cwd=WORK,
                              capture_output=True, timeout=5)
        row.update(actual_shell_rc=proc.returncode, stdout=proc.stdout.decode(), stderr=proc.stderr.decode())
    rows.append(row)
    print(name, result, 'rc=' + str(row.get('actual_shell_rc')), flush=True)
(WORK / 'extra-shell-probes.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
