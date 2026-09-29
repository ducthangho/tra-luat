from pathlib import Path
import collections,datetime as dt,hashlib,json,re,subprocess
B=Path(__file__).resolve().parents[1];R=B/'cay-kho';O=B/'do-review9';SHA='0bc6e56e1a1fd21cedfc18557320941d51db866c'
def git(*a):return subprocess.check_output(['git','-C',str(R),*a]).decode().strip()
s=json.loads((O/'state.json').read_text());text=(B/'VERDICT.md').read_text();matches=re.findall(r'^### ([a-z0-9]+(?:-[a-z0-9]+)*)  \[(P[123])\]  (.+)$',text,re.M)
report=dict(utc=dt.datetime.now(dt.timezone.utc).isoformat(),head=git('rev-parse','HEAD'),tree=git('rev-parse','HEAD^{tree}'),status=git('status','--porcelain'),tracked_diff=git('diff','--name-only'),index_diff=git('diff','--cached','--name-only'),new_commits=git('rev-list','--count',SHA+'..HEAD'),finding_ids=[x[0] for x in matches],severities=dict(collections.Counter(x[1] for x in matches)),rows=len(s['rows']),last_line=text.strip().splitlines()[-1])
assert report['head']==SHA and report['tree']=='86b3f017010575bd37b612242acb7e60bbf2db03'
assert report['status']==report['tracked_diff']==report['index_diff']=='' and report['new_commits']=='0'
old=['a2-neo-nen-cu-trai-write-set-hien-tai','bia-mo-mot-ref-khong-thu-hoi-moi-ban','bien-do-khac-head-khong-phai-nhieu-runner','quyet-dinh-tiep-h-con-bi-phu-dinh']
assert len(s['reconciliations'])==4 and all(sum(x.startswith('`'+slug+'`') for x in s['reconciliations'])==1 for slug in old)
assert len(matches)==5 and report['severities']=={'P1':1,'P2':4}
for block in re.split(r'^### ',text,flags=re.M)[1:]:
 for label in ['TỆP/DÒNG:','VẤN ĐỀ:','ĐÃ THỬ VÁ:','ĐÃ THỬ NGHIỆM:','ĐỘ TIN:','chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit']:assert label in block,label
assert '## ĐỐI CHIẾU LƯỢT TRƯỚC' in text and '## BẢNG ĐO' in text
assert text.count('reviewed_sha: '+SHA)==1
assert report['last_line'] in ['verdict: dang-do','verdict: changes_requested']
(O/'final-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
