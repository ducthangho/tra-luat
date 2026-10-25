import sys, os, json, importlib.util, subprocess, hashlib, copy
from pathlib import Path
from unittest import mock
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent; root=R.parent
s=importlib.util.spec_from_file_location('pt',root/'ops/ci_provenance_test.py'); t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
m=t.nap(); results={}; x='python '+t.DUONG_GIA

def probe(name,log,wf=None,job=None,run=None):
    try:
        rc,out,p,rest=t.chay([(job or t.job(1),log)],wf=wf,run=run)
        g=t.gate(p) if p else None
        results[name]={'rc':rc,'stdout':out,'gate':g,'checkout':t.co(p) if p else None,'workflow':wf,'log':log}
    except Exception as e:
        results[name]={'exception':type(e).__name__,'message':str(e),'workflow':wf}
    return results[name]

# Exact r4 mechanisms, independent fixed workflow instead of deriving YAML from the log.
envlog=t.log_voi([f'{t.T} ##[group]Run python ops/khac.py',f'{t.T} \x1b[36;1mpython ops/khac.py\x1b[0m',f'{t.T} env:',f'{t.T} \x1b[36;1m{x}\x1b[0m',f'{t.T} ##[endgroup]',f'{t.T} THU: 4/4 dat'])
mixedlog=t.log_voi([f'{t.T} ##[group]Run if false; then',f'{t.T} if false; then',f'{t.T} \x1b[36;1m{x}\x1b[0m',f'{t.T} fi',f'{t.T} ##[endgroup]',f'{t.T} THU: 4/4 dat'])
probe('r4_F02_env_metadata',envlog,t.wf_tu('python ops/khac.py'))
probe('r4_F02_mixed_color',mixedlog,t.wf_tu('if false; then\n'+x+'\nfi'))
# Collision with an unchanged minimal step elsewhere in the same workflow.
w=__import__('yaml').safe_load(t.wf_tu('if false; then\n'+x+'\nfi'))
w['jobs']['other']={'if':False,'runs-on':'x','steps':[{'run':x+'\n'}]}
probe('F02_mixed_color_other_job',mixedlog,__import__('yaml').safe_dump(w))
w2=__import__('yaml').safe_load(t.wf_tu('python ops/khac.py'))
w2['jobs']['other']={'if':False,'runs-on':'x','steps':[{'run':'python ops/khac.py\n'+x+'\n'}]}
probe('F02_env_metadata_other_job',envlog,__import__('yaml').safe_dump(w2))
# Block and scalar shapes.
for name,script in [('simple',x),('blank_middle',x+'\n\n'+x),('indent','  '+x+'  '),('trailing_newlines',x+'\n\n\n'),('two_calls',x+'\npython ops/khac.py'),('continuation','python \\\n'+t.DUONG_GIA),('expression','python ${{ matrix.test }}'),('arguments',x+' --gop-dich manh'),('VAR','A=1 '+x)]:
    log=t.log_voi(t.khoi(script.rstrip('\n').split('\n'),'THU: 4/4 dat'))
    probe('script_'+name,log,t.wf_tu(script))
base=t.log_voi(t.buoc(x,'THU: 4/4 dat'))
for name,log in [('missing_end',base.replace(f'{t.T} ##[endgroup]\n','')),('end_suffix',base.replace('##[endgroup]','##[endgroup]trailing')),('CRLF',base.replace('\n','\r\n')),('no_ANSI',base.replace('\x1b[36;1m','').replace('\x1b[0m','')),('header_only',t.LINUX+f'{t.T} ##[group]Run {x}\n{t.T} THU: 4/4 dat\n'),('nested',base.replace(f'{t.T} shell:',f'{t.T} ##[group]details\n{t.T} shell:')),('no_marker',t.log_voi(t.buoc(x,'nothing')))]:
    probe('block_'+name,log,t.wf_tu(x))
for key,values in {'env':[{},None,'${{ inputs.env }}',{'A':'1'}],'shell':['bash','pwsh','sh','bash -e {0}',None,{},'${{ inputs.shell }}'],'working-directory':['.','d'],'name':['n'],'continue-on-error':[True],'timeout-minutes':[1]}.items():
    for i,v in enumerate(values): probe(f'step_{key}_{i}',base,t.wf_tu(x,buoc_them={key:v}))
for where in ('job','workflow'):
    for key,value in [('env',{'CI_DANG_KY_X':'1'}),('env',{'PYTHONUTF8':'1'}),('env','${{ inputs.env }}'),('env',None),('defaults',{}),('defaults',{'run':{'shell':'bash'}})]:
        kw={'job_them' if where=='job' else 'goc_them':{key:value}}
        probe(f'{where}_{key}_{str(value)}',base,t.wf_tu(x,**kw))
for name,content in [('no_jobs','x: y'),('bad_yaml','jobs: ['),('deep','jobs: '+('['*1100)+(']'*1100)),('nonstring_key','jobs:\n  j:\n    steps:\n    - run: '+x+'\n      7: a\n'),('on_bool','on: push\n'+t.wf_tu(x)),('alias','jobs:\n  j:\n    steps:\n    - &s\n      run: '+x+'\n    - *s\n'),('self_alias','jobs: &j {j: {steps: [*j]}}'),('folded','jobs:\n  j:\n    steps:\n    - run: >\n        '+x+'\n'),('strip_scalar','jobs:\n  j:\n    steps:\n    - run: |-\n        '+x+'\n')]:
    probe('yaml_'+name,base,content)
# Missing/SHA/path shapes, including genuinely invoking local git_blob.
for sha,path in [(t.H,'.github/workflows/ci.yml'),('0'*40,'.github/workflows/ci.yml'),(t.H,'not-present.yml'),(t.H,'./.github/workflows/ci.yml'),(t.H,'.github/workflows/ci.yml@refs/heads/master')]:
    r=m.git_blob(sha,path); results['git_'+sha[:7]+'_'+path]={'is_none':r is None,'sha256':hashlib.sha256(r.encode()).hexdigest() if r else None}
with mock.patch.object(m.subprocess,'run',return_value=__import__('types').SimpleNamespace(returncode=0,stdout=b'\xff')):
    results['git_non_utf8']={'result':m.git_blob(t.H,'p')}
for k in ('head_sha','event','path','check_suite_id'):
    z=probe('run_missing_'+k,base,t.wf_tu(x),run={k:None})
for k,v in [('steps',[]),('steps',[{}]),('steps','x'),('steps',[1]),('check_run_url',1),('check_run_url',[1]),('check_run_url','https://api.github.com/repos/o/r/check-runs/1\n')]:
    probe('job_shape_'+k+'_'+repr(v),base,t.wf_tu(x),job=t.job(1,**{k:v}))
# Collection invariants, each independently measured for jobs/artifacts.
for key in ('jobs','artifacts'):
    for mode in ('stable','changed','empty_early','duplicate','underreported'):
        counter=[]
        def fake(url):
            n=int(url.rsplit('page=',1)[1]); counter.append(n)
            total=2 if mode=='changed' and n==1 else 3
            if mode=='underreported': total=1
            ids=[] if n>3 or mode=='empty_early' and n>1 else [1 if mode=='duplicate' else n]
            return 200,json.dumps({'total_count':total,key:[{'id':i} for i in ids]}).encode()
        old=m.TRANG; m.TRANG=1; oldmax=m.TRANG_TOI_DA; m.TRANG_TOI_DA=5
        try: results['page_'+key+'_'+mode]={'result':m.lay_trang(fake,'https://api.github.com/x',key),'pages':counter}
        finally: m.TRANG=old; m.TRANG_TOI_DA=oldmax
# Fake REST route checks.
f=t.RestGia({'id':5},[t.job(1)],{1:t.LINUX},[{'id':1}])
results['routes']={p:f('https://api.github.com/repos/o/r/actions/'+p)[0] for p in ('runs/6','runs/6/attempts/1/jobs','runs/6/artifacts','jobs/999/logs','runs/5/attempts/2/jobs')}
(R/'probes.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print('PROBES',len(results))
for k in ('r4_F02_env_metadata','r4_F02_mixed_color','F02_mixed_color_other_job','F02_env_metadata_other_job','block_missing_end','block_end_suffix','block_nested'):
    v=results[k]; print(k,v.get('rc'),v.get('gate',{}).get('trang_thai'),v.get('gate',{}).get('kich_ban'),v.get('gate',{}).get('dau_duong'))
