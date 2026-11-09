from common import *
import re
H='15ad82f56924a0ccc99833ec73eec078ce00b726';auth=json.loads((W/'land-authority-binding.json').read_text());aux=json.loads((W/'AUX6-transport-receipt.json').read_text());assert aux['verdict']=='passed'
assert not (W/'Ready-intent.json').exists() and json.loads((W/'owner-H2-human-delivery-binding.json').read_text())['v2_rc']==0
assert datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(auth['until'].replace('Z','+00:00'))
raw=gitb('ls-remote','origin');(W/'Ready-fullrefs.raw').write_bytes(raw)
def refs(raw):
 d={}
 for line in raw.decode().splitlines():
  oid,ref=line.split();assert re.fullmatch('[0-9a-f]{40}',oid) and ref not in d;d[ref]=oid
 return d
old=refs((W/'land-authority-fullrefs.raw').read_bytes());new=refs(raw);deltas=[]
for ref in sorted(set(old)|set(new)):
 if old.get(ref)!=new.get(ref):
  assert ref=='refs/heads/ops/wp1296-spec' and old.get(ref) and new.get(ref),(ref,old.get(ref),new.get(ref))
  subprocess.run([GIT,'-C',str(P),'fetch','--no-tags','origin',ref],env=env,check=True,capture_output=True)
  paths=git('diff','--name-only',old[ref],new[ref]).splitlines();assert paths and all(p.startswith(('ops/checkpoints/wp1296-r3/land-authority/','ops/checkpoints/wp1296-r3/land-ready/')) for p in paths),paths
  deltas.append({'ref':ref,'old':old[ref],'new':new[ref],'paths':paths,'classification':'ownauthorizedlandmetadataonly; no product/spec/policy/authorityscopechange'})
assert new['refs/heads/master']==B and new['refs/pull/1301/head']==H and new['refs/heads/agent/wp1296-r3-g3-codex']==H
s=(W/'grant.py').read_text();prefix=s[:s.index("assert not[x for x in matches if x['active']],matches")];ns=dict(globals());exec(compile(prefix.replace('before-lease-remote-heads.raw','Ready-holder-heads.raw'),'readonly-holder-scan','exec'),ns);ids=sorted({v['lease'] for v in ns['matches'] if v['active']});assert ids==['wp1296-r3-g3-codex'],ids
rules=api('repos/ducthangho/tra-luat/rules/branches/master');save(W/'Ready-rules.json',rules);assert rules==json.loads((W/'current-master-rules.json').read_text())
repo=api('repos/ducthangho/tra-luat');assert repo['allow_merge_commit'] and not repo['delete_branch_on_merge'];pr=api('repos/ducthangho/tra-luat/pulls/1301');assert pr['head']['sha']==H and pr['base']['sha']==B and pr['draft'] and not pr['merged']
c=json.loads((W/'land-final-inputs/K0-K7-preReady.json').read_text())['command'];q=subprocess.run(c,env=env,capture_output=True);save(W/'Ready-K0-K7.json',{'command':c,'rc':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode()});assert q.returncode==0
save(W/'Ready-fence-classification.json',{'at':now(),'full_ref_count':len(new),'fullref_sha256':hashlib.sha256(raw).hexdigest(),'deltas':deltas,'sole_holder_ids':ids,'head':H,'base':B,'rules_unchanged':True,'real_human_receipt':'ops/reviews/wp1296-r3-human2.receipt.yaml','AUX6':'passed'});
b=json.loads((W/'live-budget.json').read_text());assert b['shared_used']==6;b['shared_used']=7;next(v for v in b['shared_calls'] if v['n']==6).update(state='terminal_provenance_audit_passed',receipt_sha256=sha(W/'AUX6-transport-receipt.json'));b['shared_calls'].append({'n':7,'purpose':'Ready-triggered automatic exactH2 connector ifactualstarts; no newformalround','state':'reserved_before_Ready_conditional_actualtelemetry','at':now(),'head':H});save(W/'live-budget.json',b)
save(W/'Ready-intent.json',{'at':now(),'head':H,'target':B,'source':auth['source'],'operation':'gh pr ready; NONIDEMPOTENT do not repeat unknownoutcome','gate_rc':0,'AUX6':'passed','not_yet_merged':True})
cmd=[GH,'pr','ready','1301','--repo','ducthangho/tra-luat'];q=subprocess.run(cmd,env=env,capture_output=True);save(W/'Ready-result.json',{'at':now(),'command':cmd,'rc':q.returncode,'stdout':q.stdout.decode(),'stderr':q.stderr.decode()});assert q.returncode==0
pr=api('repos/ducthangho/tra-luat/pulls/1301');save(W/'Ready-PR-readback.json',pr);assert not pr['draft'] and pr['head']['sha']==H and pr['base']['sha']==B and not pr['merged'];print(json.dumps({'Ready':True,'head':H,'merged':False,'wait':'actualReadyauto connector terminal then freshfinalmergefence'}),flush=True)
