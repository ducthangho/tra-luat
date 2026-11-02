from pathlib import Path
import hashlib,json,re,subprocess,difflib,platform,shutil
R=Path(__file__).resolve().parents[1]; E=R/'evidence'; S=R/'cay-kho'
def git(*a): return subprocess.check_output(['git','--no-optional-locks','-C',str(S),*a])
def data(name): return json.loads((E/f'{name}.json').read_text())
pre=data('preflight'); out={}
assert git('rev-parse','HEAD').decode().strip()==pre['head']=='90b3f1cd9ff8a3459285796da37dc96b8553690e'
assert git('rev-parse','HEAD^{tree}').decode().strip()==pre['tree']=='b077af062b784383994a556f165e54abb947fcf2'
assert git('rev-parse','origin/master').decode().strip()==pre['base']=='90c101b8d1f8895b66607de8582a18c5e72d834c'
assert git('status','--porcelain=v1','--untracked-files=all','--ignored')==b''
for name,args in [('tracked',['diff','--binary','HEAD']),('index',['diff','--cached','--binary']),('untracked',['ls-files','--others','--exclude-standard']),('ignored',['ls-files','--others','--ignored','--exclude-standard'])]:
 b=git(*args); (E/f'final-{name}.snapshot').write_bytes(b); assert b==b'',name
for p,h in pre['files'].items():
 b=(S/p).read_bytes(); assert hashlib.sha256(b).hexdigest()==h
 assert b==git('show',f"{pre['head']}:{p}")
 assert b==(R/'copies/head'/p).read_bytes()==(R/'copies/control'/p).read_bytes()
assert git('diff','origin/master...HEAD')==(R/'diff.patch').read_bytes()
assert (R/'PROMPT.md').read_bytes()==(R/'runs/4eb21f94/prompt.snapshot').read_bytes()
out['source']=dict(head=pre['head'],tree=pre['tree'],base=pre['base'],status='clean',files_match_git_and_preflight=len(pre['files']))
assert (E/'head-tests.rc').read_text().strip()=='0'
assert (E/'head-tests.log').read_text().strip()=='cap-nhat-cong-cu tests: 118/118 ca QUA'
assert all(data('provenance')[k] for k in ['head_test_equals_old_plus_hint','product_equals_round1','round1_delta_matches'])
assert data('provenance')['hint_applies_rc']==0
out['head_tests']='118/118 rc0'
mut=data('mutations'); assert len(mut)==14 and len({m['name'] for m in mut})==14
by={m['name']:m for m in mut}
for m in mut:
 name=m['name']; log=(E/f'{name}.log').read_text()
 assert not m['parser_error'] and 'ParserError' not in log
 assert re.findall(r'cap-nhat-cong-cu tests: (\d+)/(\d+) ca QUA',log)==[tuple(v) for v in m['summary']]
 assert m['failed']==re.findall(r'  DO  (.+)',log)
 assert len(m['failed'])==118-int(m['summary'][0][0])
 assert m['rc']==(0 if not m['failed'] else 1)
 delta=''
 for p,key in [('ops/vm/cap-nhat-cong-cu.ps1','product_sha256'),('ops/vm/cap-nhat-cong-cu_test.ps1','test_sha256')]:
  original=(S/p).read_text(); changed=(R/'copies'/name/p).read_text()
  assert hashlib.sha256(changed.encode()).hexdigest()==m[key]
  delta+=''.join(difflib.unified_diff(original.splitlines(True),changed.splitlines(True),fromfile=p,tofile=p))
 assert delta==(E/f'{name}.patch').read_text()
 assert (name=='control')==(delta=='')
assert len({(m['product_sha256'],m['test_sha256']) for m in mut})==14
assert by['control']['summary']==[['118','118']] and by['control']['rc']==0
assert by['reset_no_T']['summary']==[['117','118']] and by['reset_no_T']['failed']==['dk_chay_reset_ca_cay_long_va_tep_an']
assert by['reset_after_copy_cached_condition']['summary']==[['117','118']] and by['reset_after_copy_cached_condition']['failed']==['dk_chay_sua_tep_dacl_rong_truoc_khi_chep']
assert by['model_reset_noop']['summary']==[['116','118']] and set(by['model_reset_noop']['failed'])=={'dk_chay_sua_tep_dacl_rong_truoc_khi_chep','dk_chay_reset_ca_cay_long_va_tep_an'}
assert sum(m['rc']!=0 for m in mut)==12
assert [m['name'] for m in mut if m['name']!='control' and m['rc']==0]==['model_copy_no_denial']
assert (E/'mutations-driver.rc').read_text().strip()=='0'
out['mutations']=dict(control='118/118 rc0',mutants=13,killed=12,survived=['model_copy_no_denial'],target_mutants_killed='3/3')
expected={'NT AUTHORITY\\SYSTEM':'FullControl','BUILTIN\\Administrators':'FullControl','BUILTIN\\Users':'ReadAndExecute, Synchronize'}
for name,nodes in [('head_empty',4),('head_nested',9),('head_nested_previous_recursive',9),('head_hidden_only',5)]:
 d=data(name); assert d['tasks']==1 and d['error']=='OFFLINE-DUNG-TRUOC-MAT-KHAU'
 assert len(d['states'])==nodes
 for n in d['states']:
  assert n['owner']=='BUILTIN\\Administrators' and n['violations']==[]
  assert len(n['access'])==3
  assert {a['IdentityReference']:a['FileSystemRights'] for a in n['access']}==expected
  assert all(a['AccessControlType']=='Allow' for a in n['access'])
for name in ['no_reset_empty','after_copy_empty','after_copy_cached_empty']:
 d=data(name); assert d['tasks']==0 and 'denied' in d['error']
 assert not [e for e in d['events'] if e['type']=='do_acl']
for name,bad in [('no_T_nested_head_model',3),('no_T_nested_original_model',0),('no_T_nested_recursive_model',3),('no_Force_hidden_only',1)]:
 d=data(name); assert d['tasks']==1 and d['error']=='OFFLINE-DUNG-TRUOC-MAT-KHAU'
 assert sum(bool(n['violations']) for n in d['states'])==bad
state_rows=data('state-probes'); assert len(state_rows)==9 and all(d['rc']==0 for d in state_rows)
assert (E/'state-probes-driver.rc').read_text().strip()=='0'
edge={x['name']:x for x in data('edge-probes')}; assert len(edge)==5
for name,message in [('reset_failure','RESET-FAIL-INJECTED'),('enumeration_failure','ENUM-FAIL-INJECTED'),('copy_sharing_failure','SHARING-LOCK-INJECTED')]:
 assert edge[name]['error']==message and edge[name]['tasks']==0
assert edge['reset_failure']['copies']==0 and edge['enumeration_failure']['copies']==0
assert edge['head_hidden_only']['resets']==1 and edge['head_hidden_only']['bad_nodes']==0
assert edge['no_Force_hidden_only']['resets']==0 and edge['no_Force_hidden_only']['bad_nodes']==1
assert (E/'edge-probes-driver.rc').read_text().strip()=='0'
out['state_oracles']='9/9; controls have exact 3 grants on every modeled node'
out['edge_oracles']='5/5; model injection only for I/O failures'
native=data('native-wrapper'); assert native['native_ntfs']=='KHONG_DO_DUOC'
assert len(native['checks'])==4 and native['checks'][0]['ordinary']==3 and native['checks'][0]['forced']==4
for c in native['checks'][1:]: assert c['exact_argv'] and c['threw']==(c['requested_rc']!=0)
assert (E/'native-wrapper.rc').read_text().strip()=='0'
out['native_wrapper']='3/3 argv/rc; Linux enumeration 1/1; native Windows KHONG_DO_DUOC'
out['environment']=dict(system=platform.system(),platform=platform.platform(),icacls=shutil.which('icacls.exe'))
assert out['environment']['system']=='Linux' and out['environment']['icacls'] is None
out['artifacts']={}
for folder in ['probes','evidence']:
 for p in sorted((R/folder).iterdir()):
  if p.is_file() and p.name not in ['final-audit.json','final-audit.log','final-audit.rc']:
   out['artifacts'][str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
(E/'final-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='artifacts'},ensure_ascii=False,indent=2))
print('Final audit: PASS; source unchanged; exact SHA, suite, target mutants, state/edge/argv oracles verified.')
