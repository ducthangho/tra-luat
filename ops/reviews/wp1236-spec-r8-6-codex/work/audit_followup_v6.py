import builtins, collections, copy, inspect, json, pathlib, re, sys, unicodedata
W=pathlib.Path(__file__).resolve().parent
setup=(W/'audit_integration_v6.py').read_text().split('\nresults={',1)[0]
exec(compile(setup,str(W/'audit_integration_v6.py'),'exec'))
# `setup` defines the unmodified scratch implementation, fixture, and loading helpers.
report={}
checks=[]
for j in pv0['moc']['gate_output']['jobs']:
    if j['conclusion']=='skipped' or 'ubuntu-latest' not in j['labels'] or j['name']=='chuan-bi':continue
    names={b['name'] for b in j['buoc'] if b['conclusion']=='success'}
    rule=m._muc(m.LUAT_v1,j['name']); names &={x for b in rule[0]['buoc'] for x in b['ten']}
    for b in wf0['jobs'][j['name'].split(' (')[0]]['steps']:
        if b.get('name') in names:checks.append((b['name'],gram.cp(b.get('run'),b.get('shell'))))
report['A15']={'pairs':len(checks),'pass':sum(ly is None for _,ly in checks),'reject':sum(ly is not None for _,ly in checks),'names':len(set(checks)),'names_pass':sum(ly is None for _,ly in set(checks)),'names_reject':sum(ly is not None for _,ly in set(checks))}
w=copy.deepcopy(wf)
step=next(b for b in w['jobs']['gate-packet-loop']['steps'] if b.get('name')=='packet-loop selftest')
step['run']='python .claude/dev/packet_loop_test.py | python ops/tee_test.py';step.pop('shell',None)
report['A14_i_prime']=m.kiem(text,prov(w),t.goc())
original=dict(m.LUAT_PHIEN_BAN); domains=dict(m.MIEN_HIEU_LUC)
report['A20']={}
for label in ('e_prime','f','g','h','i','i_prime'):
    rule=copy.deepcopy(m.LUAT_v1)
    if label=='f':rule['JOB_BAT_BUOC'].append(rule['JOB_BAT_BUOC'][0])
    if label in ('g','i_prime'):rule['JOB_BAT_BUOC'].remove(m.CHECK_BAT_BUOC[0])
    if label=='h':rule['JOB_BAT_BUOC'].append('gate-moi (ubuntu-latest)')
    if label=='i':rule['MUC'].append(copy.deepcopy(rule['MUC'][0]))
    key=m.bam(rule)
    m.LUAT_PHIEN_BAN={key:rule};m.MIEN_HIEU_LUC={key:(1,None)}
    if label=='e_prime':m.MIEN_HIEU_LUC={key:(1,p['moc']['run']['run_id']+1)}
    if label=='i_prime':
        m.LUAT_PHIEN_BAN.update(original)
        m.MIEN_HIEU_LUC={key:(1,2),next(iter(original)):(3,None)}
    tt=text.replace(next(iter(original)),key) if label!='i_prime' else text
    report['A20'][label]={'registry':m.kiem_so_luat(),'kiem':m.kiem(tt,p,t.goc())}
    m.LUAT_PHIEN_BAN=original;m.MIEN_HIEU_LUC=domains
# A benign wrapper on the actual integration model: only instrumentation, same decisions.
transparent='''
import functools
_original = cu_phap_run
_calls = 0

def counted(run, shell):
    global _calls
    _calls += 1
    return _original(run, shell)

cu_phap_run = functools.update_wrapper(counted, _original)
'''
(W/'model_counted.py').write_text(src+transparent)
cm=load('model_counted',W/'model_counted.py'); f=cm.cu_phap_run
report['counted_model_structure']={
    'h':all(getattr(cm,h)==getattr(gram,h) for h in ('P','W','DANG','LENH')),
    're':all(type(getattr(cm,h)) is re.Pattern and getattr(cm,h).pattern==getattr(gram,h).pattern and getattr(cm,h).flags==re.ASCII for h in ('RE_DON','RE_ONG')),
    'globals_builtins':f.__globals__ is vars(cm) and f.__builtins__ is vars(builtins),
    'closure_defaults':all(getattr(f,k) is None for k in ('__closure__','__defaults__','__kwdefaults__')),
    'no_shadowing':not {'type','str'}&set(vars(cm)),
    'AST':ka.dump_doi_tuong(inspect.getsource(f))==ka.dump_doi_tuong(ka.THAM_CHIEU),
    'actual_code_AST':ka.dump_doi_tuong(inspect.getsource(f.__code__))==ka.dump_doi_tuong(ka.THAM_CHIEU)}
report['counted_F_ok']=cm.kiem(text,p,t.goc())
report['counted_F_ok_goc']=cm.kiem(text,pv0,t.goc())
orig_calls=cm._calls;seen=[]
def record(r,s):seen.append((r,s));return None
cm.cu_phap_run=record
cm.kiem(text,p,t.goc());first=list(seen);seen.clear();cm.kiem(text,pv0,t.goc())
report['counted_spy']={'ok_calls':len(first),'goc_calls':len(seen),'wrapper_calls_during_spy':cm._calls-orig_calls,'NFC_changed_workflow_args':sum(type(r) is str and unicodedata.normalize('NFC',r)!=r for r,s in first+seen)}
# Existing author evidence is deterministic; compare readbacks with its stored JSON.
report['artifact_parity']={}
for name in ('khoa_ast_r8.json','probes_r8.json','dot_bien_r8.json','g1_probes_qua_grammar.json','sinh_r8.json'):
    report['artifact_parity'][name]=json.loads((W/name).read_text())==json.loads((R/'ops/reviews/wp1236-r8-soan'/name).read_text())
report['gen1_numstat']=git('diff','--numstat','d26b36f...508d678','--','ops/gate_output_doi_chieu.py','ops/gate_output_doi_chieu_test.py','.claude/dev/ci_dang_ky_test.py')
(W/'audit_followup_v6.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
