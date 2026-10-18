#!/usr/bin/env python3
"""Offline counterexamples for exact head 783463b5d62efbc43c6a6116e32c43accbc485f7.
Usage: python3 REPRO.py --copy /tmp/rv812-review-copy
All fixture mutations and state writes are confined to a new /tmp directory.
"""
import argparse
import copy
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
args = argparse.ArgumentParser()
args.add_argument('--copy', type=Path, required=True)
repo = args.parse_args().copy.resolve()
if repo == Path('/home/user/rv812'):
    raise SystemExit('Use a temporary repository copy, as required by the review contract.')
sys.path.insert(0, str(repo / '.claude/dev'))

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

t = load('packet_tests_review812', repo / '.claude/dev/packet_loop_test.py')
yaml = __import__('yaml')
out = Path(tempfile.mkdtemp(prefix='review812-repro-'))

def ctx(name):
    p = out / name
    p.mkdir()
    return t.Ctx(t.CANONICAL, p)

def report(name, rc, sd, err, before):
    raw = (sd / 'wp55.json').read_bytes()
    print(json.dumps(dict(probe=name, rc=rc, state=json.loads(raw)['state'], unchanged=raw == before,
                          error=err.decode('utf-8', 'replace')), ensure_ascii=False), flush=True)

def real_h_baseline(c, sd, reviewing_bytes):
    # A real Git blob and digest, verified through the complete canonical validator.
    (sd / 'wp55.json').write_bytes(reviewing_bytes)
    w = c.tmp / 'kho/w'
    verdict = w / 'ops/reviews/v.md'
    verdict.parent.mkdir(parents=True, exist_ok=True)
    verdict.write_text('Reviewed commit: ' + json.loads(reviewing_bytes)['reviewing_head_sha'] + '\nVerdict: approve\n')
    t._g(w, 'add', 'ops/reviews/v.md')
    t._g(w, 'commit', '-qm', 'frozen reviewer evidence')
    oid = t._g(w, 'rev-parse', 'HEAD')
    receipt = yaml.safe_load((c.tmp / 'bn.yaml').read_bytes())
    receipt['evidence_url'] = 'https://github.com/o/r/blob/' + oid + '/ops/reviews/v.md'
    receipt['verdict_sha256'] = __import__('hashlib').sha256(verdict.read_bytes()).hexdigest()
    (c.tmp / 'bn.yaml').write_text(yaml.safe_dump(receipt))
    bnv = load('canonical_receipt_for_baseline', repo / 'ops/bien_nhan_v2.py')
    assert bnv.PROVIDER_NGUON_HONG is None and not bnv._thieu(receipt)
    assert bnv._neo_git(w, 'bn.yaml', receipt) == ([], [])
    rc, _, err = t.run(t.CANONICAL, ['record-review', '--packet', 55, '--provider', 'codex', '--verdict', 'approve',
        '--reviewed-sha', receipt['reviewed_sha'], '--codex-call', 'g1', '--bien-nhan', c.tmp / 'bn.yaml', '--root', w], sd)
    assert rc == 0, err
    return rc, err

c = ctx('review')
rc, sd, err, before = t._r812(c, 'review')
assert rc == 0, err
rc, err = real_h_baseline(c, sd, before)
report('positive-review-real-H', rc, sd, err, before)
st = json.loads(before)
h = st['reviewing_head_sha']
bn_path = c.tmp / 'bn.yaml'
bn = yaml.safe_load(bn_path.read_bytes())
for name, changes in [
    ('chatgpt-as-codex', {'model_reviewer_identity': {**bn['model_reviewer_identity'], 'provider': 'openai_chatgpt'}}),
    ('wrong-transport', {'model_reviewer_identity': {**bn['model_reviewer_identity'], 'transport': 'human'}}),
    ('absent-git-anchor', {'verdict_path': 'ops/reviews/absent.md', 'evidence_url': 'https://github.com/o/r/blob/' + 'f' * 40 + '/ops/reviews/absent.md'}),
    ('invalid-slug-newline', {'bang_lop': [{'slug': 'a\n', 'hang': 'P3'}]}),
]:
    (sd / 'wp55.json').write_bytes(before)
    bn_path.write_text(yaml.safe_dump({**bn, **changes}))
    rc, _, err = t.run(t.CANONICAL, ['record-review', '--packet', 55, '--provider', 'codex', '--verdict', 'approve',
        '--reviewed-sha', h, '--codex-call', 'g1', '--bien-nhan', bn_path, '--root', c.tmp / 'kho/w'], sd)
    report(name, rc, sd, err, before)
(sd / 'wp55.json').write_bytes(before)
rc, _, err = t.run(t.CANONICAL, ['record-review', '--packet', 55, '--provider', 'codex', '--verdict', 'changes_requested',
    '--reviewed-sha', h, '--codex-call', 'g1', '--finding-id', 'executor-invented-class'], sd)
report('negative-review-without-H', rc, sd, err, before)
c = ctx('lease')
rc, sd, err, before = t._r812(c, 'lease')
assert rc == 0, err
(sd / 'wp55.json').write_bytes(before)
(c.tmp / 'kho/w/ops/specs/wp55.md').unlink()
rc, _, err = t.run(t.CANONICAL, ['record-lease', '--packet', 55, '--root', c.tmp / 'kho/w', '--lease-ref', 'origin/ops/wp55-spec',
    '--lease-path', 'ops/leases/l.yaml', '--lease-comments', c.tmp / 'cm.json'], sd)
report('valid-spec-only-in-ref', rc, sd, err, before)
print(json.dumps({'scratch': str(out)}))
