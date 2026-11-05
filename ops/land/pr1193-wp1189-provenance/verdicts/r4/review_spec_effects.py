"""Read-only probes for adding the frozen spec; no full kiem-merge/network call."""
import ast
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace

import review_checks as r


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    os.environ.update({k: r.ENV[k] for k in ('PATH', 'PYTHONDONTWRITEBYTECODE', 'GIT_OPTIONAL_LOCKS')})
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(r.REPO / '.claude/dev'))
    packet_path = r.REPO / '.claude/dev/packet_loop.py'
    packet = load_module('review_packet_loop', packet_path)
    source = ast.parse(packet_path.read_text(encoding='utf-8'))
    cmd = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'cmd_kiem_merge')
    k1 = next(n for n in cmd.body if isinstance(n, ast.FunctionDef) and n.name == 'k1')
    code = compile(ast.Module(body=[k1], type_ignores=[]), str(packet_path), 'exec')
    outcomes = {}
    for label, head in [('before_spec', r.MERGE), ('candidate', r.HEAD)]:
        namespace = dict(packet.__dict__, root=r.REPO, h=head,
                         a=SimpleNamespace(spec=r.SPEC), lease={'spec_hash': r.SPEC_HASH})
        exec(code, namespace)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            try:
                value = namespace['k1']()
                outcomes[label] = {'rc': 0, 'returns_exact_spec': value == (r.ROOT / 'SPEC.md').read_bytes()}
            except SystemExit as e:
                outcomes[label] = {'rc': e.code, 'stderr': stderr.getvalue()}
    assert outcomes['before_spec']['rc'] == 12
    assert outcomes['candidate'] == {'rc': 0, 'returns_exact_spec': True}

    ci = load_module('review_ci_fast', r.REPO / 'ops/ci_duong_nhanh.py')
    paths = [line.split('\t')[2] for line in r.git('diff', '--numstat', r.MASTER, r.HEAD).stdout.decode().splitlines()]
    ci_mode, reason = ci.phan_loai_tu_diff(paths)
    assert ci_mode == 'day_du'
    windows = packet._phan_loai_windows(r.REPO, r.MASTER, r.HEAD, (r.ROOT / 'SPEC.md').read_bytes())
    assert windows == 'required'

    sys.path.insert(0, str(r.REPO / 'scripts'))
    release = load_module('review_release', r.REPO / 'scripts/tl_core/release.py')
    workflow = load_module('review_workflow', r.REPO / 'scripts/tl_core/workflow.py')
    include_spec = release._release_should_include(r.REPO / r.SPEC, r.REPO)
    assert include_spec is False
    roots = list(workflow._DOC_CLAIMS_DEFAULT_PATHS)
    assert not any(r.SPEC == p or r.SPEC.startswith(p + '/') for p in roots)
    targets = sorted((r.REPO / '.claude/skills').rglob('*.md'))
    targets += sorted((r.REPO / '.agents/skills').rglob('*.md'))
    targets.append(r.REPO / 'CLAUDE.md')
    assert r.REPO / r.SPEC not in targets and len(targets) == 10
    doc = json.loads((r.EVIDENCE / 'doc-claims-check.log').read_text(encoding='utf-8'))
    assert doc['ok'] is True and doc['flags'] == [] and doc['layers_skipped'] == {}
    result = {'K1_real_function_isolated': outcomes,
              'K1_scope': 'Nested k1 AST from exact candidate source; real local Git. Other kiem-merge gates not executed; no network.',
              'ci_classifier': {'paths': paths, 'mode': ci_mode, 'reason': reason},
              'release_include_spec': include_spec,
              'doc_claims_default_roots': roots,
              'doc_claims_scans_spec': False,
              'doc_claims_result': {k: doc[k] for k in ('ok', 'files_scanned', 'flags', 'advisory_count', 'layers_skipped')},
              'doctrine_scan_default_targets': [p.relative_to(r.REPO).as_posix() for p in targets],
              'doctrine_scans_spec': False,
              'windows_actual_classifier': windows,
              'windows_execution': 'not_run: ngoài phạm vi chỉ thị review OFFLINE lượt 4; không suy not_required từ câu trong bản đặc tả lưu byte'}
    r.dump(r.EVIDENCE / 'spec-effects.json', result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
