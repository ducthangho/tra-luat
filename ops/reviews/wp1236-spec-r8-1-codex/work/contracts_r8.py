import copy, importlib.util, json, os, pathlib, sys, tempfile, collections
import yaml
BASE = pathlib.Path(__file__).resolve().parent.parent
WORK = BASE / 'work'
tempfile.tempdir = str(WORK / 'tmp')
os.environ['GATE_OUTPUT_DOI_CHIEU_GOC'] = str(BASE / 'repo')
sys.dont_write_bytecode = True

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

gram = load('grammar', WORK / 'artifacts/gram.py')
t = load('fixture_gen1', WORK / 'candidate/ops/gate_output_doi_chieu_test.py')
pth = WORK / 'candidate/ops/gate_output_doi_chieu.py'
src = pth.read_text()
old = 'elif ly := che_do_shell(str(y.get("run", "")), y.get("shell")):\n                nm.append(f"{ly}:{s[\'name\'][:30]}")'
new = 'elif ly := cu_phap_run(y.get("run"), y.get("shell")):\n                nm.append(f"cu_phap_run:{ly}:{p[\'name\']}:{s[\'name\']}")'
assert src.count(old) == 1
m = type(sys)('model_r8')
m.__file__ = str(pth)
exec(compile(src.replace(old, new), str(pth), 'exec'), m.__dict__)
m.cu_phap_run = gram.cp
t.nap = lambda: m
text, orig = t.f_ok()
wf = yaml.safe_load(t.ci_goc())
rewrites = {
 'tl selftest (co bang chung exact-identity)': 'bash .github/checks/tl_selftest_bang_chung.sh\n',
 'release-bundle x2 cùng SHA-256': 'bash .github/checks/release_bundle_x2.sh\n',
 'G5 manh ban kinh dot bien (#668)': 'python ops/cong_cu_test.py\n',
 'lease-publish selftest (đo lại setup sau G5)': 'bash ops/chay_lease_publish_test.sh\n',
 'don-nhanh selftest (chốt xoá nhánh)': 'pwsh -NoProfile -File scripts/don-nhanh_test.ps1\n',
 'bo ca gate chay TRONG cgroup duoc uy quyen (Linux)': 'bash ops/ci/gate_cgroup.sh\n',
}

def provenance_for(w):
    p = copy.deepcopy(orig)
    sha = t.commit_ci(yaml.safe_dump(w, allow_unicode=True, sort_keys=False))
    for c in p['moc']['checkout']:
        c['sha'] = sha
    return p

result = {}
state, reasons = m.kiem(text, orig, t.goc())
result['F_ok_goc'] = {'state': state, 'reason_count': len(reasons), 'affected_J': len({x.split(':')[2] for x in reasons}), 'reasons': reasons}
assert state == 'not_measured' and len(reasons) == 13
counts = collections.Counter()
names = {}
chan = []
for j in orig['moc']['gate_output']['jobs']:
    if j['name'] == 'chuan-bi' or 'ubuntu-latest' not in (j.get('labels') or []): continue
    k = m.cp.ghep_job(j['name'], wf)
    law = m._muc(m.LUAT_v1, j['name'])[0]
    for b in law['buoc']:
        rest = [s for s in j['buoc'] if s['name'] in b['ten'] and s['conclusion'] == 'success']
        assert len(rest) == 1
        found = [(i, s) for i,s in enumerate(wf['jobs'][k]['steps']) if m.cp.ten_du_kien(s) == rest[0]['name']]
        assert len(found) == 1
        i,s = found[0]
        reason = gram.cp(s.get('run'), s.get('shell'))
        counts['rejected' if reason else 'accepted'] += 1
        names[s['name']] = reason
        c = m.chan_k7(wf, k, i, b['env'], m.LUAT_v1['ENV_JOB_CHO_PHEP'])
        if c: chan.append((j['name'], s['name'], c))
all_names = {n for b in m.LUAT_v1['MUC'] for s in b['buoc'] for n in s['ten']}
result['F_that_A15'] = {'invocations': sum(counts.values()), 'by_invocation': dict(counts), 'distinct_names': len(names), 'distinct_accepted': sum(v is None for v in names.values()), 'distinct_rejected': sum(v is not None for v in names.values()), 'law_names_without_success_rest': sorted(all_names-set(names)), 'chan_k7':chan}
changed = []
for j in wf['jobs'].values():
    for s in j.get('steps', []):
        if s.get('name') in rewrites:
            s['run'] = rewrites[s['name']]
            if s['name'] == 'don-nhanh selftest (chốt xoá nhánh)': s.pop('shell')
            changed.append(s['name'])
assert len(changed) == 6
p = provenance_for(wf)
result['F_ok_VL_F'] = m.kiem(text, p, t.goc())
assert result['F_ok_VL_F'] == ('passed', [])
step = next(s for s in wf['jobs']['gate-packet-loop']['steps'] if s.get('name') == 'packet-loop selftest')
saved = dict(step)
step['run'] = 'python .claude/dev/packet_loop_test.py | python ops/tee_test.py'
step['shell'] = 'bash'
result['A14_i'] = m.kiem(text, provenance_for(wf), t.goc())
step.pop('shell')
result['A14_i_prime'] = m.kiem(text, provenance_for(wf), t.goc())
step.clear(); step.update(saved)
# Check precedence: chan_k7 should stop the grammar even with an invalid run.
checks=[]
for level in ('workflow', 'job', 'step'):
    for key in ('BASH_ENV', 'SHELLOPTS', 'BASH_FUNC_python%%'):
        w = copy.deepcopy(wf)
        j=w['jobs']['gate-packet-loop']; s=next(s for s in j['steps'] if s.get('name')=='packet-loop selftest')
        target = w if level == 'workflow' else j if level == 'job' else s
        target.setdefault('env', {})[key] = 'sentinel'
        s['run'] = None
        st, rs = m.kiem(text, provenance_for(w), t.goc())
        assert st == 'not_measured' and not any(x.startswith('cu_phap_run:') for x in rs)
        checks.append([level,key,st])
result['env_precedence'] = checks
# Baseline guards not involved in obsolete shell checks, using the r8 positive fixture.
t.f_ok = lambda:(text, copy.deepcopy(p))
selected=['a01_duong_f_ok','a02_bam_log','a03_tap_job','a04_danh_tinh','a05_ca_dong','a06_sai_loai','a07_n_tren_m','a08_neo_run','a09_so_luat_mien','a10_cuoi','a11_khong','a12_json','a13_buoc_rest','a16_dong_la','a17_loi_khai','a18_neo_trich_tep','a19_owner_waived','a20_so_luat','a21_pham_vi_land']
result['inherited_cases'] = {}
for name in selected:
    try: getattr(t,name)(); result['inherited_cases'][name] = 'passed'
    except Exception as e: result['inherited_cases'][name] = f'{type(e).__name__}: {e}'
# Fixed order changes reasons, even if both variants reject.
result['order_counterexample'] = {'run':None, 'shell':'pwsh', 'specified':gram.cp(None,'pwsh'), 'shell_first':'shell_ngoai_cu_phap'}
(WORK/'contracts_r8.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(json.dumps(result, ensure_ascii=False, indent=2))
