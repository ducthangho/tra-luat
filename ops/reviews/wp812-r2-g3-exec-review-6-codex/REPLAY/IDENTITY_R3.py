#!/usr/bin/env python3
"""Real CLI + H for Antigravity, using each valid declared model family."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
repo = Path('/tmp/wp812-r6-suite')
sys.path.insert(0, str(repo / '.claude/dev'))


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    sys.modules[n] = m
    s.loader.exec_module(m)
    return m


t = load('ag_r3_tests', repo / '.claude/dev/packet_loop_test.py')
v = load('ag_r3_receipt', repo / 'ops/bien_nhan_v2.py')
import yaml

out = Path(tempfile.mkdtemp(prefix='review812-r3-ag-'))
for family, model in (('gemini', 'gemini'), ('openai', 'gpt')):
    d = out / family
    d.mkdir()
    c = t.Ctx(t.CANONICAL, d)
    w = t._kho812(c)
    t._r812_doi_lease(w, {'provider': 'google_antigravity', 'executor': 'google_antigravity', 'model_family': family,
        'execution_surface': 'antigravity', 'reviewer': 'claude', 'reviewer_model_family': 'claude',
        'reviewer_execution_surface': 'claude_code', 'reviewer_transport': 'machine/local'})
    sd = c.sd()
    rc, _, e = c.init(sd, executor='google_antigravity', reviewer='claude', lease=False,
        extra=('--executor-model-family', family, '--executor-execution-surface', 'antigravity', '--executor-transport', 'machine/local'))
    assert rc == 0, e
    (d / 'cm.json').write_text(json.dumps([{'user': {'login': 'github-actions[bot]'},
        'body': 'lease_id: wp55-r1-g1-claude', 'issue_url': 'https://api.github.com/repos/o/r/issues/55'}]))
    rc, _, e = t.run(t.CANONICAL, ['record-lease', '--packet', 55, '--lease-ref', 'origin/ops/wp55-spec',
        '--lease-path', 'ops/leases/l.yaml', '--lease-comments', d / 'cm.json', '--root', w], sd)
    assert rc == 0, e
    h = t._g(w, 'rev-parse', 'refs/remotes/origin/agent/wp55-g1-claude')
    for args in (
        ['begin-attempt', '--packet', 55, '--provider', 'google_antigravity', '--model-family', family,
         '--execution-surface', 'antigravity', '--transport', 'machine/local'],
        ['record-post', '--packet', 55, '--for', 'reviewing', '--comment-id', '9000055002'],
        ['transition', '--packet', 55, '--to', 'reviewing', '--comment-id', '9000055002', '--head-sha', h],
    ):
        rc, _, e = t.run(t.CANONICAL, args, sd)
        assert rc == 0, e
    before = (sd / 'wp55.json').read_bytes()
    sh = json.loads(before)['ngu_canh_lease']['spec_hash']
    bn = t._bn812(w, h, sh, bn={'executor_provider': 'google_antigravity',
        'model_executor_identity': {'model_family': model, 'model_evidence': 'do_may', 'model_evidence_ref': 'r'},
        'model_reviewer_identity': {'provider': 'anthropic_claude', 'surface': 'claude_code', 'transport': 'machine/local', 'session_run_id': 's'}})
    assert v._thieu(bn) == [], v._thieu(bn)
    assert v._neo_git(w, 'bn.yaml', bn) == ([], [])
    (d / 'bn.yaml').write_text(yaml.safe_dump(bn))
    rc, _, e = t.run(t.CANONICAL, ['record-review', '--packet', 55, '--provider', 'claude', '--verdict', 'approve',
        '--reviewed-sha', h, '--bien-nhan', d / 'bn.yaml', '--root', w], sd)
    print(json.dumps({'probe': 'ag-' + family, 'thieu': [], 'neo': [[], []], 'rc': rc,
        'state': json.loads((sd / 'wp55.json').read_bytes())['state'], 'unchanged': before == (sd / 'wp55.json').read_bytes(),
        'error': e.decode()}, ensure_ascii=False), flush=True)
