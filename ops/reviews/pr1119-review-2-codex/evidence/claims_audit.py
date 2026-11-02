from common import *
import yaml,re,collections
checks=[]
def ck(name,a,b):checks.append(dict(name=name,actual=a,expected=b,ok=a==b))
def j(src,name):return json.loads((S/'nguon'/src/'evidence'/name).read_text())
def tx(src,name):return (S/'nguon'/src/'evidence'/name).read_text()
def receipt(stem):return yaml.safe_load((R/'ops/reviews'/f'{stem}-verdict.receipt.yaml').read_text())
def rows(s):return collections.Counter(l for l in s.splitlines() if l.startswith('| '))
for turn,src in [(1,'review1110a'),(2,'review1110b')]:
    stem=f'pr1110-review-{turn}-codex';d=receipt(stem);v=(S/'nguon'/src/'VERDICT.md').read_text()
    mapping=j(src,'archive-mapping.json' if turn==1 else 'byte-mapping.json')
    ck(stem+' historical mapped files',len(mapping),41)
    ck(stem+' historical mapped all equal',all(x['equal'] for x in mapping),True)
    saved=j(src,'archive.json' if turn==1 else 'bytes.json');omitted=saved['omitted' if turn==1 else 'omissions']
    ck(stem+' historical omitted count',len(omitted),2);ck(stem+' historical omitted correct',all(x['declared_correct'] for x in omitted),True)
    rc=j(src,'receipt-checks.json');ck(stem+' historical receipt count',len(rc),116 if turn==1 else 91);ck(stem+' historical receipt recorded pass',all(x['ok'] for x in rc),True)
    descriptions={'run copy','launcher JSON equals run'} if turn==2 else set()
    ck(stem+' literal receipt values',all(x['actual']==x['expected'] for x in rc if x.get('check') not in descriptions),True)
    if turn==2:
        ck(stem+' descriptive placeholders',[x['check'] for x in rc if x['actual']!=x['expected']],['run copy','launcher JSON equals run'])
        run=json.loads(git('show',d['reviewed_sha']+':ops/reviews/pr1075-review-1-codex/run/run.json'))
        launcher=json.loads(git('show',d['reviewed_sha']+':ops/reviews/pr1075-review-1-codex/launcher.out'))
        ck(stem+' historical archived run/launcher',run,launcher)
    before=rows(git('show',d['base_sha']+':ops/reviews/README.md').decode());after=rows(git('show',d['reviewed_sha']+':ops/reviews/README.md').decode())
    ck(stem+' historical README added',sum((after-before).values()),4);ck(stem+' historical README removed',sum((before-after).values()),0)
    for name in ['bien-nhan','direct']:
        suffix='stdout' if turn==1 else 'log';raw=tx(src,'mutant-'+name+'.'+suffix)
        if turn==1:raw+=tx(src,'mutant-'+name+'.stderr')
        ck(stem+' historical mutation '+name,'pr1075-review-1-codex-verdict.receipt.yaml' in raw,True)
    ck(stem+' ket_luan 0 finding','0 finding' in d['ket_luan'],True)
    if turn==1:
        for phrase in ['41 tệp','hai tệp','116 đối chiếu','bốn hàng']:ck(stem+' verdict '+phrase,phrase in v,True)
        for phrase in ['41 tep','2 tep','116 doi chieu','4 hang']:ck(stem+' receipt '+phrase,phrase in d['ket_luan'],True)
    else:
        ck(stem+' diff empty',len(git('diff','e137f8c','3a3aac5','--','ops/reviews')),0)
        ck(stem+' diff supplied empty',len((S/'nguon'/src/'DIFF-OPS-REVIEWS-TU-LUOT1.patch').read_bytes()),0)
for src,turn in [('review1114a',1),('review1114b',2)]:
    stem=f'pr1114-review-{turn}-codex';d=receipt(stem);v=(S/'nguon'/src/'VERDICT.md').read_text()
    for side in ['base','head']:
        raw=tx(src,side+'.log')
        for phrase in ['CA: 52/52 dat','DOT BIEN: 80/80 bi giet dung ly do','TONG: DAT']:ck(stem+' '+side+' '+phrase,phrase in raw,True)
    for phrase in ['52/52','80/80']:ck(stem+' conclusion '+phrase,phrase in d['ket_luan'] and phrase in v,True)
src='review1114a'
for phrase in ['DO:p3b4_co_blob','32767','TONG: DO']:ck(src+' old wrapper '+phrase,phrase in tx(src,'base-limit.log'),True)
ck(src+' new wrapper','TONG: DAT' in tx(src,'head-limit.log'),True)
for name in ['mutation-argv-read.log','mutation-no-input.log']:ck(src+' '+name,'DO:p3b4_co_blob:node rc=1' in tx(src,name),True)
src='review1114b';d=receipt('pr1114-review-2-codex');v=(S/'nguon'/src/'VERDICT.md').read_text()
for mode,expect in [('before',26),('after',0)]:
    r=j(src,'repro-'+mode+'.json');ck(src+' '+mode+' worker bad',sum(x['bad'] for x in r['rows']),expect);ck(src+' '+mode+' worker total',sum(x['total'] for x in r['rows']),1800)
    ck(src+' '+mode+' worker rc',all(x['rc']==0 for x in r['rows']),True)
mechanism=j(src,'mechanism.json');ck(src+' transitions',len(mechanism['transitions']),20);ck(src+' mechanism total',mechanism['total'],1200);ck(src+' R to Z',all(x['after_return']['state']=='R' and x['final']['state']=='Z' for x in mechanism['transitions']),True)
matrix=j(src,'mutation-matrix.json')['rows']
for variant in ['no_kill','parent_only']:
    selected=[x for x in matrix if x['variant']==variant and x['case'].startswith(('a4_','a11_','b10_'))]
    ck(src+' '+variant+' cases',len(selected),3);ck(src+' '+variant+' red',all(x['rc']!=0 for x in selected),True)
bs=j(src,'base.json')['seconds'];hs=j(src,'head.json')['seconds'];ck(src+' seconds delta',round(hs-bs,3),15.017);ck(src+' percent delta',round((hs-bs)*100/bs,2),4.92)
for phrase in ['26/1800','0/1800','20/1200','15,017','4,92%']:ck(src+' conclusion '+phrase,phrase in d['ket_luan'] and phrase in v,True)
# Compare the invariant receipt structure and classifications with three local precedents.
fields=['schema_version','kind','packet_id','role','provider','executor_provider','cross_provider','review_class','effective_review_class','nguon_tep','so_dem_theo','independent_from_executor_session','review_axes','nguon_co_tham_quyen','anchor.loai','anchor.cuong_do','model_reviewer_identity.provider','model_reviewer_identity.surface','model_reviewer_identity.transport','model_reviewer_identity.model_evidence','model_reviewer_identity.model','model_reviewer_identity.model_yeu_cau','model_reviewer_identity.model_da_chay']
def get(d,key):
    for p in key.split('.'):d=d[p]
    return d
precedent=[]
for old in ['pr1058-review-1-codex','pr1058-review-2-codex','pr1075-review-1-codex']:
    od=receipt(old)
    for pr,turn,src in ITEMS:
        stem=f'pr{pr}-review-{turn}-codex';nd=receipt(stem)
        differences=[f for f in fields if get(od,f)!=get(nd,f)]
        precedent.append(dict(old=old,new=stem,differences=differences,new_keys=sorted(set(nd)-set(od)),old_keys=sorted(set(od)-set(nd))))
        ck('precedent '+old+' '+stem,differences,[])
        ck(stem+' assurance appropriate to approve',nd['assurance'],'cross_approved')
        ck(stem+' original verdict approval',(R/nd['verdict_path']).read_text().splitlines()[0],'Verdict: approve')
save('claims.json',dict(checks=checks,failures=[c for c in checks if not c['ok']],precedent=precedent,precedent_fields=fields))
print(json.dumps(dict(checks=len(checks),failures=[c for c in checks if not c['ok']],precedent=precedent),ensure_ascii=False,indent=2))
note('Kết luận/tiền lệ — `PYTHONDONTWRITEBYTECODE=1 python3 claims_audit.py`: '+str(len(checks))+' đối chiếu, failures='+str(sum(not c['ok'] for c in checks))+'. `evidence/claims.json` đối chiếu ket_luan với verdict và log/JSON nguồn; các số lịch sử là kiểm tính nhất quán hiện vật, KHÔNG phải chạy lại review lịch sử. 23 trường cố định × 3 tiền lệ × 4 biên nhận không lệch; khác khóa ở pr1058 lượt 1 do changes_requested (assurance_KHONG_dat), còn bốn verdict mới approve (ket_luan).')
