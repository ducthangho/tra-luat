import collections, importlib.util, json, pathlib, random, yaml
R=pathlib.Path(__file__).resolve().parent;root=R.parent
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load(root/'ops/ci_provenance.py','m8');t=load(root/'ops/ci_provenance_test.py','t8');_,green=m.doc_moi();rng=random.Random(899011)
rows=[];coverage=collections.Counter();errors=[]
def blocked(d):return 'env' in d and (type(d['env']) is not dict or any(str(k).startswith('CI_DANG_KY_') for k in d['env']))
for case in range(2000):
    steps=[];rest=[];logs=[];expected=[];prior=[];valid_runs=0;wf={'jobs':{}};job_yaml={'runs-on':'ubuntu-latest','steps':steps};key='job'+str(case);wf['jobs'][key]=job_yaml
    alias=rng.choice(['Build (release)','Xây dựng','A+B.*',' Build ',key]);job_yaml['name']=alias;jobname=rng.choice([key,alias,key+' (ubuntu-24.04)',alias+' (linux, 5)'])
    for scope in (wf,job_yaml):
        choice=rng.randrange(8)
        if choice==1:scope['env']=None
        elif choice==2:scope['env']={'CI_DANG_KY_X':''}
        elif choice==3:scope['env']={'A':'1'}
        elif choice==4:scope['defaults']={}
    n=rng.randint(1,6);skipped=[];number=2
    for i in range(n):
        choice=rng.randrange(7);prefix='A=1 ' if choice==1 else '';path='ops/p'+str(i)+'.py';known=choice!=2
        script=prefix+'python '+path if choice<=3 else 'echo GITHUB_PATH' if choice==4 else 'echo done'
        step={'uses':'actions/setup-python@v5'} if choice==6 else {'run':script+'\n'}
        if rng.randrange(3)==0:step['name']=rng.choice(['Run tests','Xây dựng','  literal  ',f'check {i}'])
        mode=rng.randrange(7)
        if mode==1:step['env']={}
        elif mode==2:step['shell']='zsh'
        elif mode==3:step['shell']='pwsh'
        elif mode==4:step['continue-on-error']=False
        is_skip=rng.randrange(5)==0;skipped.append(is_skip);steps.append(step);number+=rng.randint(1,5)
        name=step.get('name','Run '+(step.get('run',step.get('uses'))).split('\n')[0])
        rest.append({'name':name,'number':number,'conclusion':'skipped' if is_skip else 'success','started_at':'2026-10-19T23:45:04Z','completed_at':'2026-10-19T23:45:04Z'})
        if not is_skip:
            if 'uses' in step:logs += [f'{t.T} ##[group]Run {step["uses"]}',f'{t.T} ##[endgroup]']
            else:
                ok=rng.choice([True,False]);output='THU: 4/4 dat' if ok else 'THU: 3/4 dat';logs+=t.buoc(script,output);valid_runs+=1
                if choice<=3:
                    block=blocked(wf) or blocked(job_yaml) or 'defaults' in wf or 'defaults' in job_yaml or 'env' in step or step.get('shell','bash') not in ('bash','pwsh','sh') or bool(prefix) or any('GITHUB_ENV' in x or 'GITHUB_PATH' in x for x in prior)
                    expected.append({'lenh':script,'duong_dan':path,'trang_thai':'not_measured' if not known or block else 'passed' if ok else 'failed',**({'ly_do':'khong_co_trong_MOI' if not known else 'che_do_khong_xac_dinh'} if not known or block else {'dong_khop':[output] if ok else []})})
        prior.append(step.get('run',''))
    rest=[{'name':'Set up job','number':1,'conclusion':'success'},*rest,{'name':'Post cleanup','number':number+1,'conclusion':'success'},{'name':'Complete job','number':number+2,'conclusion':'success'}]
    perturb=rng.choice(['none','none','none','bad_name','bad_time','bad_number','bad_count','bad_job'])
    gh='passed';reason=None
    active=[x for x in rest[1:-2] if x['conclusion']!='skipped']
    if perturb=='bad_name':rest[1]['name']='different';reason='b_ten_buoc_lech'
    elif perturb=='bad_time' and active:active[-1]['started_at']='2026-10-19T23:45:05Z';reason='c_gio_header_ngoai_cua_so'
    elif perturb=='bad_number':rest[0]['number']=0;reason='steps_rest_sai_dang'
    elif perturb=='bad_count':rest.append({'name':'extra','number':number+3,'conclusion':'skipped'});reason='a_so_buoc_rest_khac_so_buoc_yaml'
    elif perturb=='bad_job':jobname='missing';reason='d_job_yaml_khong_duy_nhat'
    rng.shuffle(rest);job=t.job(1,name=jobname,steps=rest);moi={f'ops/p{i}.py':r'^THU: (\d+)/(\d+) dat$' for i in range(n) if 'run' in steps[i]}
    # Choice 2 is the independently designated unknown path; retain its index explicitly from the generated expectation.
    for x in expected:
        if x.get('ly_do')=='khong_co_trong_MOI':moi.pop(x['duong_dan'],None)
    got=m.moc_gate(job,logs,moi,green,wf);coverage[perturb]+=1
    if reason:
        want={'trang_thai':'not_measured','ly_do':reason,'so_buoc':sum(not x for x in skipped)};expected=[];valid_runs=0
    else:want={'trang_thai':'passed','so_buoc':sum(not x for x in skipped)}
    want_gate='failed' if any(x['trang_thai']=='failed' for x in expected) else 'passed' if any(x['trang_thai']=='passed' for x in expected) else 'not_measured'
    ok=got['ghep_buoc']==want and got['dau_duong']==expected and got['kich_ban']['buoc_xac_thuc']==valid_runs and got['trang_thai']==want_gate
    row={'case':case,'perturbation':perturb,'passed':ok,'ghep':got['ghep_buoc'],'marker_states':[x['trang_thai'] for x in got['dau_duong']]};rows.append(row)
    if not ok:errors.append({'case':case,'workflow':wf,'rest_job':job,'log':logs,'expected':{'ghep_buoc':want,'markers':expected,'count':valid_runs,'gate':want_gate},'actual':got})
(R/'product11-results.json').write_text(json.dumps({'seed':899011,'coverage':dict(coverage),'rows':rows,'mismatches':errors},ensure_ascii=False,indent=1));print('PRODUCT',len(rows),'mismatches',len(errors));print(dict(coverage));print(json.dumps(errors[:2],ensure_ascii=False,indent=2));assert not errors
