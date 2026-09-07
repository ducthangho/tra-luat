import ast, contextlib, copy, datetime, io, json, re, statistics, subprocess, yaml
from harness import BASE, BASE_FN, BASE_MOI, C, H, OUT, ROOT, module, replay
r={'measured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
path='.claude/hooks/pretooluse_guard_test.py'
texts=['TONG: CA 39/39 dat · DOT BIEN 34/34 bi giet','TONG: CA 39/39 dat · DOT BIEN 0/0 bi giet','TONG: CA 0/39 dat · DOT BIEN 34/34 bi giet']
r['issue464_literal_samples']=[dict(input=s,claimed=v,base_actual=BASE_FN(s,BASE_MOI[path]),H_actual=H['bang_chung_xanh'](s,C.MOI[path]),base_with_terminator=BASE_FN(s+'\nTONG: DAT\n',BASE_MOI[path]),H_with_terminator=H['bang_chung_xanh'](s+'\nTONG: DAT\n',C.MOI[path])) for s,v in zip(texts,[True,True,False])]
r['issue465_wrong_path_exists']=(ROOT/'.claude/dev/subagent_ghi_detect_test.py').exists()
r['issue465_true_path_exists']=(ROOT/'.claude/hooks/subagent_ghi_detect_test.py').exists()
r['new_MOI_equals_old']={p:C.MOI[p]==BASE_MOI[p] for p in C.MOI}
r['old_SPAN_preserved']={p:C.MOI[p][0]==BASE_MOI[p] for p in C.MOI}
# Reproduce GATE consumer on the YAML split as specified, keeping the source untouched.
source=(ROOT/'.github/workflows/ci.yml').read_text(); doc=yaml.safe_load(source)
old_steps=copy.deepcopy(doc['jobs']['gate']['steps'])
for name,needle in [('gate-registry','test registry'),('gate-packet-loop','packet-loop selftest')]:
    moved=[s for s in old_steps if s.get('name','').startswith(needle)]
    assert len(moved)==1
    new=copy.deepcopy(doc['jobs']['gate']); new['steps']=copy.deepcopy(old_steps[:9])+moved
    doc['jobs'][name]=new
    doc['jobs']['gate']['steps']=[s for s in doc['jobs']['gate']['steps'] if s not in moved]
raw=module(ROOT/'.claude/dev/ci_dang_ky_test.py','consumer_raw_contract')
r['ruff_consumer_baseline']=raw.loi_ruff_ci(source)
r['ruff_consumer_split']=raw.loi_ruff_ci(yaml.safe_dump(doc,allow_unicode=True))
r['split_jobs']=len(doc['jobs'])
r['split_setup_lengths']={j:len(d['steps'][:9]) for j,d in doc['jobs'].items()}
# Only recompute printed arithmetic; original jobs, rounding and attribution remain unverified.
minutes=[40.20,41.65,42.28,43.83,45.58,46.02,47.18,48.00,49.37,49.62,50.48]
prior=[x for x in minutes if x not in (48.00,50.48)]
r['printed_job_arithmetic']={label:{'n':len(xs),'min':min(xs),'max':max(xs),'range':max(xs)-min(xs),'median':statistics.median(xs),'mean':statistics.mean(xs),'margin60':60-max(xs)} for label,xs in [('11',minutes),('9',prior)]}
r['printed_split_arithmetic']={'Windows_gate':43.17-17.7-9.7,'Windows_registry':3.33+17.7,'Windows_packet':3.33+9.7,'Windows_sum':43.17+2*3.33,
 'Ubuntu_gate':24.20-13.13-3.65,'Ubuntu_registry':1.18+13.13,'Ubuntu_packet':1.18+3.65,'Ubuntu_sum':24.20+2*1.18,
 'billing_before':43.20*2+24.25,'billing_after':(43.17+2*3.33)*2+(24.20+2*1.18),
 'longest_job_saved':43.20-(3.33+17.70),'a1_margin':25-(3.33+17.70),'split_estimated_percent_change':((3.33+17.70)/43.20-1)*100}
# Known D9 boundary: explicitly not counted as a new D1 finding.
big='9'*5000
text=f'CA         : 42/42 đạt · 0 đỏ · ĐẠT\nĐỘT BIẾN   : đã đo {big}/{big} tập giết · ĐẠT\nTỔNG: ĐẠT\n'
path='.claude/dev/mcp_gh_test.py'
try:r['D9_H']=replay(path,text)
except Exception as e:r['D9_H']=type(e).__name__
r['D9_BASE']=replay(path,text,base=True)
# Missing denominator in issue scalar (CA == 8); use real module declarations only.
nhanh=module(ROOT/'ops/nhanh_don_duoc_test.py','nhanh_static_review')
r['nhanh_CA']=len(nhanh.CA)
r['nhanh_mutants']=len(nhanh.DOT_BIEN)
# Evaluate printed equal-scope constraints directly.
r['gate_acceptance28']={'A1_le25':28<=25,'if_revised_to_estimate_plus_observed_range':28<=(21.03+10.28)}
(OUT/'contracts.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(r,ensure_ascii=False,indent=2))
