from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import tempfile

import yaml
import measure as m


def workflow_modes():
    ns = m.extract('ops/cong_cu_test.py', ['_doc_che_do', '_van_tay', '_gom_manh'], {
        'Path': Path, 'subprocess': subprocess, 'json': json,
        '_BIEN_BAN_KINH': 'CONG_CU_TEST_BAN_KINH', '_BIEN_MANH': 'CONG_CU_TEST_MANH',
        '_BIEN_MANH_RA': 'CONG_CU_TEST_MANH_RA', '_TRAN_MANH': 16,
        'GOC': m.REPO, 'TEP_TEST': m.REPO / 'ops/cong_cu_test.py',
        '_KHOA_DAU_MANH': frozenset({'phien_ban', 'manh', 'so_manh', 'sha256_test', 'head'}),
        '_PHIEN_BAN_MANH': 1,
    })
    for jid, job in m.jobs.items():
        for step in job.get('steps', []):
            if 'ops/cong_cu_test.py' in step.get('run', ''):
                env = {**job.get('env', {}), **step.get('env', {})}
                env = {k: str(v).replace('${{ matrix.manh }}', '0') for k, v in env.items()}
                print('callsite:', jid, 'step-if=', step.get('if'), 'continue-on-error=', step.get('continue-on-error', False))
                print(' command:', step['run'].strip().replace('\n', ' ; '))
                if '--gop' in step['run']:
                    print(' mode: gop (artifact consumer)')
                else:
                    print(' mode:', ns['_doc_che_do'](env))
    fingerprint = ns['_van_tay']()
    print('actual fingerprint:', json.dumps(fingerprint, sort_keys=True))
    assert fingerprint['head'] == m.SHA
    assert fingerprint['sha256_test'] == hashlib.sha256((m.REPO/'ops/cong_cu_test.py').read_bytes()).hexdigest()
    # Only a synthetic artifact header is created, outside the reviewed repository.
    with tempfile.TemporaryDirectory(prefix='same-head-', dir=m.ROOT/'review-evidence') as d:
        header = {'phien_ban': 1, 'manh': 0, 'so_manh': 8, **fingerprint, 'head': '0'*40}
        (Path(d)/'manh-0.txt').write_text('MANH '+json.dumps(header)+'\n')
        lines, errors = ns['_gom_manh'](d, fingerprint)
        print('foreign-head artifact:', ' | '.join(lines), 'errors=', errors)
        assert errors == 1 and '[G-van-tay]' in '\n'.join(lines)
    print('PROVEN: CI main gate delegates full mutation radius; Windows shard stops after baseline; gom uses exact HEAD+test hash.')
    print('NOT MEASURED: full Ubuntu mutation pass or Windows runner pass at this SHA; no live CI readback.')


def history_anchored():
    for short in ['e63961f', '5585abe', '747f983', 'be00ef7']:
        oid=m.git('rev-parse', short)
        rc=subprocess.run(['git','merge-base','--is-ancestor',oid,m.SHA]).returncode
        print('ancestor:', oid, 'rc=', rc)
        assert rc == 0
    print('base timestamp:', m.git('show','-s','--format=%aI | %cI | %s','e63961f'))
    for pattern in ['#878', '#879']:
        print('history <= reviewed_sha',pattern+':')
        print(m.git('log', m.SHA, '--format=%h %ad %s','--date=short','--grep='+pattern,'-6'))
    f=m.evaluator()
    old_yaml=yaml.safe_load(m.source('.github/workflows/ci.yml','5585abe^'))
    old=old_yaml['jobs']['chuan-bi']['outputs']['os']
    new=m.jobs['chuan-bi']['outputs']['os']
    print('literal branches before #878:',len(re.findall(r"'\[[^']*\]'",old)))
    print('literal branches at HEAD:',len(re.findall(r"'\[[^']*\]'",new)))
    for value in ['windows-only','windows-and-ubuntu','unknown']:
        ctx={'event_name':'workflow_dispatch','inputs':{'runner_set':value}}
        print('before #878 vs HEAD', value, ':',f(old,ctx),'->',f(new,ctx))
    old_jobs=yaml.safe_load(m.source('.github/workflows/ci.yml','be00ef7^'))['jobs']
    for jid in ['gate-cong-cu', 'gate-cong-cu-gop']:
        print('before #879',jid,'exclude=',old_jobs[jid]['strategy']['matrix'].get('exclude'),'job-if=',old_jobs[jid].get('if'))
        print('at HEAD',jid,'exclude=',m.jobs[jid]['strategy']['matrix'].get('exclude'),'job-if=',m.jobs[jid].get('if'))
    print('All history used above is reachable from reviewed_sha; no later file version used.')


{'workflow-modes':workflow_modes,'history-anchored':history_anchored}[sys.argv[1]]()
