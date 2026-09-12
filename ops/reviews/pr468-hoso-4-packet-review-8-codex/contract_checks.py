import csv, hashlib, json, pathlib, re, subprocess, yaml
B=pathlib.Path(__file__).resolve().parents[1];R=B/'cay-kho';O=B/'do-review8';src=R/'ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5';rows=list(csv.DictReader((src/'buoc.tsv').open(),delimiter='\t'))
report={'manifest':{}}
for turn in [6,7]:
 p=R/f'ops/reviews/pr468-hoso-4-packet-review-{turn}-codex';m=p/'ARTIFACTS.sha256';items=[]
 for line in m.read_text().splitlines():
  wanted,rel=line.split(maxsplit=1);rel=rel.lstrip('*');f=p/rel;f.resolve().relative_to(B)
  items.append(dict(file=rel,match=f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest()==wanted))
 report['manifest'][str(turn)]={'listed':len(items),'matched':sum(x['match'] for x in items),'mismatches':[x for x in items if not x['match']]}
def baseline(head):
 return [{'job':r['job_name'],'step':r['step_name'],'platform':'windows' if 'windows' in r['job_name'] else 'ubuntu','conclusion':r['step_conclusion'],'number':int(r['step_number'])} for r in rows if r['head7']==head]
def triples(rr):return {(r['step'],r['platform'],r['conclusion']) for r in rr}
old=baseline('1b3caa1');current=baseline('d28c4b1');split=[]
for r in current:
 p='gate-registry' if r['step'].startswith('test registry') else 'gate-packet-loop' if r['step']=='packet-loop selftest' else 'gate'
 split.append({**r,'job':p})
 if 2<=r['number']<=10:
  for p in ['gate-registry','gate-packet-loop']:split.append({**r,'job':p})
a,b,c=map(triples,[old,current,split]); dropped={x for x in c if x[0]!='bien-nhan v2 selftest'}
report['a2']={'model':'Move two heavy steps and duplicate setup 2..10 from the exact lease-base observations; preserve every conclusion. This is a model, not a new CI run.','old_head':'1b3caa1','lease_base_head':'d28c4b1','before_old':len(a),'before_exact_base':len(b),'split_distinct_triples':len(c),'added_vs_A2_old_baseline':sorted(c-a),'removed_vs_A2_old_baseline':sorted(a-c),'M2_preserved':b==c,'A2_old_baseline_pass':a==c,'suggested_same_base_pass':b==c,'drop_receipt_old_A2_pass':a==dropped,'drop_receipt_same_base_pass':b==dropped}
assert b==c and a!=c and a==dropped and b!=dropped
report['a2']['yaml_steps']={}
for h in ['1b3caa1','d28c4b1']:
 data=yaml.safe_load(subprocess.check_output(['git','-C',str(R),'show',h+':.github/workflows/ci.yml']))['jobs']['gate']['steps'];report['a2']['yaml_steps'][h]=len(data)
s=(B/'tai-lieu/LO-319-LINUX-BANG-CHUNG-XANH.md').read_text();l=(B/'tai-lieu/lo-319-linux-bang-chung-xanh-exec-1-claude-20260906.yaml.nhap').read_text();i=(B/'tai-lieu/464-LO-319-LINUX-BANG-CHUNG-XANH.md').read_text();url='https://github.com/ducthangho/tra-luat/issues/464#issuecomment-5567158069'
report['h_decision']={'url_in_three_files':[url in t for t in [s,l,i]],'selected_spec':'lựa chọn (1), tiếp H trong write set hiện tại' in s,'selected_issue':'lựa chọn (1) — tiếp H' in i,'selected_lease_comment':'chủ kho đã chọn §12 = tiếp H' in l,'draft_grant_is_null':yaml.safe_load(l)['granted_on_instruction'] is None,'stale_heading':'CHƯA được chọn' in s,'stale_lease_denial':'Spec KHÔNG khai §12 đã xong' in l}
# Demonstrate a text-only repair direction without changing spec bytes or lease authority in the checkout.
fixed_s=s.replace('(ứng viên, đã đo, CHƯA được chọn)','(chủ kho đã chọn theo quyết định §12; chưa thi công)')
fixed_l=l.replace('Spec KHÔNG khai §12 đã xong:', 'Chủ kho đã chọn tiếp H theo comment 5567158069; giữ lịch sử ba lựa chọn:')
report['h_decision']['text_only_repair_check']={'stale_heading_removed':'CHƯA được chọn' not in fixed_s,'stale_denial_removed':'Spec KHÔNG khai §12 đã xong' not in fixed_l,'authority_url_preserved':url in fixed_s and url in fixed_l,'draft_grant_still_null':yaml.safe_load(fixed_l)['granted_on_instruction'] is None}
report['runtime_diff']=subprocess.check_output(['git','-C',str(R),'diff','--numstat','origin/master','HEAD','--','.claude/dev/ci_dang_ky_test.py'],text=True)
(O/'contract-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
