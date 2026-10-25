import importlib.util, pathlib, json, sys, os, subprocess
import yaml
R = pathlib.Path(__file__).resolve().parent
root = R.parent
s = importlib.util.spec_from_file_location('tt', root/'ops/ci_provenance_test.py')
t = importlib.util.module_from_spec(s); s.loader.exec_module(t)

def independent(case):
    w0 = t.wf_tu(t.X)
    w = yaml.safe_load(w0)
    if case == 'yaml_steps_absent':
        w['jobs']['j'].pop('steps')
    elif case == 'yaml_steps_null':
        w['jobs']['j']['steps'] = None
    elif case == 'yaml_steps_integer':
        w['jobs']['j']['steps'] = 1
    elif case == 'yaml_job_integer':
        w['jobs']['j'] = 0
    elif case == 'rest_number_zero':
        p=t.g1(w0,t.buoc(t.X,'THU: 4/4 dat'),sua=lambda st:st[0].update(number=0))
        t.bang(t.ghep(p)=='steps_rest_sai_dang' and t.gate(p)['dau_duong']==[],str(t.gate(p)))
        return t.gate(p)
    p = t.g1(yaml.safe_dump(w), t.buoc(t.X, 'THU: 4/4 dat'), w_rest=w0)
    t.bang(t.ghep(p) == 'd_job_yaml_khong_duy_nhat' and t.gate(p)['dau_duong'] == [], str(t.gate(p)))
    return t.gate(p)

if len(sys.argv)>1 and not sys.argv[1].startswith('--'):
    case=sys.argv[1]
    try:
        data=independent(case)
    except t.TinHieuChotCa as e:
        print('DO:'+case+':'+str(e)); sys.exit(3)
    except Exception as e:
        # For the independent property, no-throw is itself the assertion being tested.
        try: t.bang(False, 'must return not_measured without throwing: '+type(e).__name__+': '+str(e))
        except t.TinHieuChotCa as failure: print('DO:'+case+':'+str(failure)); sys.exit(3)
    print('DAT:'+case+':'+json.dumps(data,ensure_ascii=False)); sys.exit(0)

src=(root/'ops/ci_provenance.py').read_text()
rows=[]
mutants=([('yaml_steps_bo_list_guard', ' or type(sy) is not list', '', 'yaml_steps_absent'),
          ('rest_steps_bo_list_guard', 'type(st) is list and all(', 'all(', None)] if '--containers' in sys.argv else
         [('rest_number_cho_zero', '_so(s.get("number"), 1)', '_so(s.get("number"), 0)', 'rest_number_zero')])
out=R/'shape-mutants';out.mkdir(exist_ok=True)
for name,old,new,target in mutants:
    assert src.count(old)==1
    dest=out/(name+'.py');dest.write_text(src.replace(old,new))
    env=dict(os.environ,CI_PROVENANCE_MA=str(dest),PYTHONDONTWRITEBYTECODE='1')
    cmd=[sys.executable,'-B',str(R/'extra_mutants_r4.py'),'cases']
    p=subprocess.run(cmd,capture_output=True,env=env)
    (out/(name+'.stdout.txt')).write_bytes(p.stdout)
    (out/(name+'.stderr.txt')).write_bytes(p.stderr)
    cases=json.loads(p.stdout)
    bad=[c for c in cases if c['rc']]
    row={'name':name,'old':old,'new':new,'command':cmd,'rc':p.returncode,'cases':cases,
         'rank':'SONG_SOT' if not bad else 'GIET' if all(c['rc']==3 and c['output'].startswith('DO:'+c['case']+':') for c in bad) else 'TIN_DUNG_GIA'}
    if target:
        row['counterexamples']=[]
        for case in (('yaml_steps_absent','yaml_steps_null','yaml_steps_integer','yaml_job_integer') if '--containers' in sys.argv else (target,)):
            for source in (None,str(dest)):
                e=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
                if source:e['CI_PROVENANCE_MA']=source
                q=subprocess.run([sys.executable,'-B',str(__file__),case],capture_output=True,env=e)
                row['counterexamples'].append({'case':case,'source':source or 'HEAD','rc':q.returncode,'output':(q.stdout+q.stderr).decode()})
    rows.append(row)
    (R/('shape-audit.json' if '--containers' in sys.argv else 'shape-zero-audit.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2))
    print(name,row['rank'],[(c['case'],c['rc']) for c in bad],flush=True)
