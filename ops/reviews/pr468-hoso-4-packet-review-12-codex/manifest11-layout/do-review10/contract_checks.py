# Adapted from archived round9 contract_checks.py; executed anew on revision4 in round10.
import csv, hashlib, json, pathlib, re, subprocess, yaml
B=pathlib.Path(__file__).resolve().parents[1];R=B/'cay-kho';O=B/'do-review10';S=R/'ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5';rows=list(csv.DictReader((S/'buoc.tsv').open(),delimiter='\t'));jobs=list(csv.DictReader((S/'job.tsv').open(),delimiter='\t'))
def git(*args):return subprocess.check_output(['git','-C',str(R),*args])
def data(h):return [dict(job=r['job_name'],step=r['step_name'],platform='windows' if 'windows' in r['job_name'] else 'ubuntu',conclusion=r['step_conclusion'],number=int(r['step_number'])) for r in rows if r['head7']==h]
def triples(rr):return {(r['step'],r['platform'],r['conclusion']) for r in rr}
def split(rr):
 out=[]
 for r in rr:
  job='gate-registry' if r['step'].startswith('test registry') else 'gate-packet-loop' if r['step']=='packet-loop selftest' else 'gate'
  out.append({**r,'job':job})
  if 2<=r['number']<=10:
   for job in ['gate-registry','gate-packet-loop']:out.append({**r,'job':job})
 return out
report={};old=data('1b3caa1');base=data('d28c4b1');a,b,c=map(triples,[old,base,split(base)]);dropped={x for x in c if x[0]!='bien-nhan v2 selftest'}
report['round8_countermodel']=dict(old_count=len(a),lease_base_count=len(b),split_count=len(c),old_A2_full_pass=a==c,old_A2_drop_pass=a==dropped,r4_same_base_full_pass=b==c,r4_same_base_drop_pass=b==dropped,missing_if_drop=sorted(c-dropped))
assert a!=c and a==dropped and b==c and b!=dropped
base_sha=yaml.safe_load((B/'tai-lieu/gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906.yaml').read_text())['start_from_sha'];base_yaml=git('show',base_sha+':.github/workflows/ci.yml');steps=yaml.safe_load(base_yaml)['jobs']['gate']['steps']
# No offline run exists at the same branch/base. Model ONLY the two lane conclusions from the actual YAML; do not claim a new Actions run.
dispatch=[];changes=[]
for r in base:
 conclusion='skipped' if r['step'].startswith('release-verify strict (lane LAND') else 'success' if r['step'].startswith('release-verify strict (lane WORKER') else r['conclusion']
 if conclusion!=r['conclusion']:changes.append(dict(step=r['step'],platform=r['platform'],before=r['conclusion'],after=conclusion))
 dispatch.append({**r,'conclusion':conclusion})
for prefix,cond in [('release-verify strict (lane LAND',"github.ref == 'refs/heads/master'"),('release-verify strict (lane WORKER',"github.ref != 'refs/heads/master'")]:assert next(x for x in steps if x.get('name','').startswith(prefix))['if']==cond
u,v=map(triples,[dispatch,split(dispatch)]);missing={x for x in v if x[0]!='bien-nhan v2 selftest'}
report['r4_dispatch_model']=dict(context='workflow_dispatch, refs/heads/claude/gate-tach-job-cat-chi-phi, start_from_sha=d28c4b1, before and after same lane/OS; success model, not a recorded GitHub run',yaml_steps=len(steps),before=len(u),after=len(v),full_pass=u==v,drop_receipt_pass=u==missing,removed=sorted(v-missing),lane_changes_from_stored_master=changes,compare_master_same_yaml_wrong_lane_pass=b==v,wrong_lane_added=sorted(v-b),wrong_lane_removed=sorted(b-v))
assert u==v and u!=missing and b!=v
candidates=[]
for j in jobs:
 if j['event']=='pull_request' and 'ubuntu' in j['job_name']:
  equal=git('show',j['head7']+':.github/workflows/ci.yml')==base_yaml
  candidates.append(dict(head=j['head7'],run=j['run_id'],event=j['event'],branch=j['head_branch'],ci_yaml_equal=equal,started=j['started_at']))
assert any(x['ci_yaml_equal'] for x in candidates)
pr=max([j for j in candidates if j['ci_yaml_equal']],key=lambda x:x['started']);rr=[r for r in data(pr['head']) if r['platform']=='ubuntu'];p,q=map(triples,[rr,split(rr)]);pd={x for x in q if x[0]!='bien-nhan v2 selftest'}
report['r4_pr_model']=dict(candidates=candidates,chosen=pr,projection='ubuntu only, pull_request, worker lane; split is model over saved observed baseline',before=len(p),after=len(q),full_pass=p==q,drop_receipt_pass=p==pd,removed=sorted(q-pd))
assert p==q and p!=pd
s=(B/'tai-lieu/LO-319-LINUX-BANG-CHUNG-XANH.md').read_text();l=(B/'tai-lieu/lo-319-linux-bang-chung-xanh-exec-1-claude-20260906.yaml.nhap').read_text();i=(B/'tai-lieu/464-LO-319-LINUX-BANG-CHUNG-XANH.md').read_text();url='https://github.com/ducthangho/tra-luat/issues/464#issuecomment-5567158069';d=yaml.safe_load(l)
report['h_decision']=dict(url_in_three=[url in t for t in [s,l,i]],selected_spec='lựa chọn (1), tiếp H trong write set hiện tại' in s,selected_heading='chủ kho CHỌN 07-09-2026 — lựa chọn 1' in s,selected_lease='CHỦ KHO ĐÃ CHỌN 07-09-2026' in d['ly_do_cap'],selected_issue='lựa chọn (1) — tiếp H' in i,draft_grant_null=d['granted_on_instruction'] is None,null_keys=[k for k,v in d.items() if v is None],stale_heading='CHƯA được chọn' in s,stale_lease_denial='Spec KHÔNG khai §12 đã xong' in l,conditions=[bool(re.search(r'^\| '+x+r' \|',s,re.M)) for x in ['Đ1','Đ2','Đ3','Đ4','Đ5']],no_implementation_lease_in_heading='thi công chưa bắt đầu, lease chưa cấp, Đ1–Đ5 còn ràng buộc' in s,lease_conditions_retained='Đ1–Đ5 tiếp tục ràng buộc' in d['ly_do_cap'])
assert all(report['h_decision'][k] for k in ['selected_spec','selected_heading','selected_lease','selected_issue','draft_grant_null','no_implementation_lease_in_heading','lease_conditions_retained'])
assert not report['h_decision']['stale_heading'] and not report['h_decision']['stale_lease_denial']
g=(B/'tai-lieu/GATE-TACH-JOB-CAT-CHI-PHI.md').read_text();a2=g[g.index('**A2 (M2)'):g.index('**A3 (M3)')]
report['a2_text']=dict(text=a2,same_base_event_lane='cùng base, cùng event, cùng lane' in a2,forbid_other_lane='không dùng lượt khác event/lane' in a2,pr_byte_exact='ci.yml` nền BẰNG BYTE' in a2,stale_ordering_row=[(n,t) for n,t in enumerate(g.splitlines(),1) if 'A1/A2/A5' in t and 'còn đúng' in t])
report['yaml_steps']={h:len(yaml.safe_load(git('show',h+':.github/workflows/ci.yml'))['jobs']['gate']['steps']) for h in ['1b3caa1','d28c4b1']}
(O/'contract-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
