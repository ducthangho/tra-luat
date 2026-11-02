from audit_common import *
import yaml, re
from collections import Counter

out={'conclusion_checks':[], 'omission_caveats':[], 'precedent':[], 'unmeasured':[
 'GitHub CI/Windows jobs, current PR state, remote blob availability, expectedHeadSha API, submitter credential and owner instruction: KHÔNG ĐO ĐƯỢC offline.',
 'Historical command argv/CLI version, full session independence and provider identity beyond supplied artifacts: KHÔNG ĐO ĐƯỢC; no new historical test run claimed.'
]}
def ck(label,actual,expected):
    out['conclusion_checks'].append({'check':label,'actual':actual,'expected':expected,'ok':actual==expected})
for pr,round_,source in CASES:
    stem=f'pr{pr}-review-{round_}-codex'
    arc=REPO/'ops/reviews'/stem
    src=ROOT/'nguon'/source
    d=yaml.safe_load((REPO/'ops/reviews'/(stem+'-verdict.receipt.yaml')).read_text())
    v=(src/'VERDICT.md').read_text()
    ck(stem+'.approve',v.splitlines()[0],'Verdict: approve')
    ck(stem+'.no_finding',bool(re.search(r'0 P0, 0 P1, 0 P2, 0 P3|Không có finding P0/P1/P2/P3|Không có \(0/0/0/0\)',v)),True)
    c=next(x for x in d['verdict_usage_caveats'] if x['id']=='TEP-LON-KHONG-VAO-KHO')
    diff=arc/'DIFF.patch'
    out['omission_caveats'].append({'receipt':stem,'text':c['mo_ta'],'claims_DIFF_omitted':'DIFF.patch' in c['mo_ta'] and 'KHONG vao kho' in c['mo_ta'],
        'DIFF_present':diff.is_file(),'DIFF_bytes':diff.stat().st_size if diff.exists() else None,
        'DIFF_in_manifest':bool(re.search(r'  ./DIFF.patch$',(arc/'SHA256SUMS').read_text(),re.M)),
        'DIFF_in_OMITTED':'DIFF.patch' in (arc/'OMITTED.txt').read_text()})
    ck(stem+'.launcher_equals_run',json.loads((arc/'launcher.out').read_text()),json.loads((arc/'run/run.json').read_text()))
    # Keep this equality check compact.
    out['conclusion_checks'][-1]['actual']='sha256:'+sha((arc/'launcher.out').read_bytes())
    out['conclusion_checks'][-1]['expected']='sha256:'+sha((arc/'run/run.json').read_bytes())
    cp=json.loads((arc/'run/checkpoint.json').read_text())
    ck(stem+'.checkpoint_head',cp['head'],d['reviewed_sha'])
    ck(stem+'.checkpoint_prompt',cp['prompt_sha256'],sha((arc/'PROMPT.md').read_bytes()))

s=ROOT/'nguon/review1110a'
mapping=json.loads((s/'evidence/archive-mapping.json').read_text())
checks=json.loads((s/'evidence/receipt-checks.json').read_text())
ck('1110r1.saved_mapping_count',len(mapping),41)
ck('1110r1.saved_receipt_check_count',len(checks),116)
ck('1110r1.saved_omission_count',len(json.loads((s/'evidence/archive.json').read_text())['omitted']),2)
for pr,round_,source in CASES[:2]:
    stem=f'pr{pr}-review-{round_}-codex'
    d=yaml.safe_load((REPO/'ops/reviews'/(stem+'-verdict.receipt.yaml')).read_text())
    old=Counter(x for x in git('show',d['base_sha']+':ops/reviews/README.md').decode().splitlines() if x.startswith('| '))
    new=Counter(x for x in git('show',d['reviewed_sha']+':ops/reviews/README.md').decode().splitlines() if x.startswith('| '))
    ck(stem+'.historical_readme_added',sum((new-old).values()),4)
    ck(stem+'.historical_readme_removed',sum((old-new).values()),0)
ck('1110r2.round1_diff_ops_reviews',len(git('diff','e137f8c','3a3aac5','--','ops/reviews')),0)
ck('1110r2.saved_round1_diff',git('diff','e137f8c','3a3aac5','--','ops/reviews'),(ROOT/'nguon/review1110b/DIFF-OPS-REVIEWS-TU-LUOT1.patch').read_bytes())
out['conclusion_checks'][-1]['actual']=out['conclusion_checks'][-1]['actual'].decode()
out['conclusion_checks'][-1]['expected']=out['conclusion_checks'][-1]['expected'].decode()
ck('1114r2.saved_round1_diff',sha(git('diff','e101b11','51435a4','--','ops/cloud_agent_creds_test.py')),sha((ROOT/'nguon/review1114b/DIFF-TU-LUOT1.patch').read_bytes()))
for round_,source in [(1,'review1114a'),(2,'review1114b')]:
    for version in ('base','head'):
        log=(ROOT/'nguon'/source/'evidence'/(version+'.log')).read_text()
        ck(f'1114r{round_}.{version}.suite',re.findall(r'^(?:CA:|DOT BIEN:|TONG:).*$',log,re.M),['CA: 52/52 dat','DOT BIEN: 80/80 bi giet dung ly do','TONG: DAT'])
s=ROOT/'nguon/review1114a/evidence'
ck('1114r1.wrapper_base', 'WINLIMIT206' in (s/'base-p3b4-limit.log').read_text() and 'DO:p3b4_co_blob' in (s/'base-p3b4-limit.log').read_text(),True)
for f in ['mutation-argv-read.log','mutation-no-input.log']:
    ck('1114r1.'+f+'.rejects',bool(re.search(r'DO:p3b4_co_blob', (s/f).read_text())),True)
s=ROOT/'nguon/review1114b/evidence'
for name,wanted in [('before',26),('after',0)]:
    d=json.loads((s/('repro-'+name+'.json')).read_text())
    ck('1114r2.repro_'+name+'.bad',sum(x['bad'] for x in d['rows']),wanted)
    ck('1114r2.repro_'+name+'.total',sum(x['total'] for x in d['rows']),1800)
d=json.loads((s/'mechanism.json').read_text())
ck('1114r2.R_to_Z_count',sum(x['after_return']['state']=='R' and x['final']['state']=='Z' for x in d['transitions']),20)
ck('1114r2.transition_total',d['total'],1200)
b=json.loads((s/'base.json').read_text())['seconds']; h=json.loads((s/'head.json').read_text())['seconds']
ck('1114r2.suite_seconds_increase',round(h-b,3),15.017)
ck('1114r2.suite_percent_increase',round(100*(h-b)/b,2),4.92)

precedent_names=['pr1058-review-1-codex','pr1058-review-2-codex','pr1075-review-1-codex']
ps={n:yaml.safe_load((REPO/'ops/reviews'/(n+'-verdict.receipt.yaml')).read_text()) for n in precedent_names}
fixed=['schema_version','kind','packet_id','role','provider','executor_provider','cross_provider','review_class','effective_review_class',
       'nguon_tep','so_dem_theo','independent_from_executor_session','independent_ghi_chu','review_axes','nguon_co_tham_quyen']
identity=['provider','surface','transport','model_yeu_cau','model','model_da_chay','model_evidence']
for pr,round_,_ in CASES:
    stem=f'pr{pr}-review-{round_}-codex'
    d=yaml.safe_load((REPO/'ops/reviews'/(stem+'-verdict.receipt.yaml')).read_text())
    for pn,p in ps.items():
        mismatches={k:[d.get(k),p.get(k)] for k in fixed if d.get(k)!=p.get(k)}
        mismatches.update({'model_reviewer_identity.'+k:[d['model_reviewer_identity'].get(k),p['model_reviewer_identity'].get(k)] for k in identity if d['model_reviewer_identity'].get(k)!=p['model_reviewer_identity'].get(k)})
        out['precedent'].append({'receipt':stem,'precedent':pn,'fixed_fields_compared':len(fixed)+len(identity),'mismatches':mismatches,
           'new_top_level_keys':sorted(set(d)-set(p)),'missing_top_level_keys':sorted(set(p)-set(d))})
out['conclusion_failures']=[x for x in out['conclusion_checks'] if not x['ok']]
save('claims.json',out)
print(json.dumps({'conclusion_checks':len(out['conclusion_checks']),'conclusion_failures':out['conclusion_failures'],
   'omission_caveats':out['omission_caveats'],'precedent_fixed_mismatches':[x for x in out['precedent'] if x['mismatches']]},ensure_ascii=False))
append('Nội dung kết luận/tiền lệ — `PYTHONDONTWRITEBYTECODE=1 python3 audit_claims.py`: '+str(len(out['conclusion_checks']))+' đối chiếu kết luận/hiện vật lịch sử, '+str(len(out['conclusion_failures']))+' lệch; 22 trường cố định × 3 tiền lệ × 4 biên nhận, lệch '+str(sum(bool(x['mismatches']) for x in out['precedent']))+'. Không coi đối chiếu log cũ là chạy lại suite lịch sử. Hai caveat #1114 cùng `claims_DIFF_omitted=true`, `DIFF_present=true`, `DIFF_in_manifest=true`, `DIFF_in_OMITTED=false` (P3 caveat-loai-diff-sai). Chi tiết `evidence/claims.json`.')
