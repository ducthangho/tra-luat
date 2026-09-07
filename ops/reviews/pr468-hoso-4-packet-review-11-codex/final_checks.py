import collections
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess

B = Path(__file__).resolve().parents[1]
R = B / 'cay-kho'
O = B / 'do-review10'
SHA = 'c43347d1e2c2f76bb21dc2d9d28bd6bfa153d355'

def git(*args):
    return subprocess.check_output(['git', '-C', str(R), *args]).decode().strip()

vp = B / 'VERDICT.md'
text = vp.read_text()
findings = re.findall(r'^### ([a-z0-9]+(?:-[a-z0-9]+)*)  \[(P[123])\]  (.+)$', text, re.M)
report = dict(utc=dt.datetime.now(dt.timezone.utc).isoformat(), head=git('rev-parse','HEAD'),
    tree=git('rev-parse','HEAD^{tree}'), status=git('status','--porcelain'),
    tracked_diff=git('diff','--name-only'), index_diff=git('diff','--cached','--name-only'),
    new_commits=git('rev-list','--count',SHA+'..HEAD'),
    finding_ids=[x[0] for x in findings], severities=dict(collections.Counter(x[1] for x in findings)))
assert report['head'] == SHA and report['tree'] == '799a4b2549d68c6a3ad44cc70f9257e794cd1db8'
assert report['status'] == report['tracked_diff'] == report['index_diff'] == ''
assert report['new_commits'] == '0'
assert report['severities'] == {'P1':1,'P2':2}
reconciliation = text.split('## ĐỐI CHIẾU LƯỢT TRƯỚC')[1].split('## BẢNG ĐO')[0]
slugs = ['bia-mo-mot-ref-khong-thu-hoi-moi-ban','a2-neo-nen-cu-trai-write-set-hien-tai',
    'bien-do-khac-head-khong-phai-nhieu-runner','quyet-dinh-tiep-h-con-bi-phu-dinh',
    'manifest-luot8-liet-ke-hien-vat-khong-duoc-giao']
assert len(re.findall(r'^- `', reconciliation, re.M)) == 5
assert all(reconciliation.count('`'+slug+'`')==1 for slug in slugs)
for block in re.split(r'^### ',text,flags=re.M)[1:]:
    for label in ['TỆP/DÒNG:','VẤN ĐỀ:','ĐÃ THỬ VÁ:','ĐÃ THỬ NGHIỆM:','ĐỘ TIN:',
        'chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit']:
        assert label in block, label
assert text.count('reviewed_sha: '+SHA)==1
assert text.strip().splitlines()[-1]=='verdict: changes_requested'
table=text.split('## BẢNG ĐO')[1].split('\n### ')[0]
assert '|\n\n|' not in table
for gate in ['lease-check','lease-publish-test','bien-nhan-v2','doc-claims','doctrine-scan','adr-song','eol']:
    assert json.loads((O/f'{gate}.json').read_text())['rc']==0
assert json.loads((O/'doc-claims.stdout').read_text())['ok'] is True
assert json.loads((O/'eol.stdout').read_text())['ok'] is True

report_path=O/'final-check.json'
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
files=[vp]+[p for p in O.rglob('*') if p.is_file() and not p.is_symlink() and
    not any(part == 'tmp' or part.endswith('.tmp') for part in p.relative_to(O).parts)]
files=sorted(files,key=lambda p:str(p.relative_to(B)))
assert all(p.resolve().is_relative_to(B) for p in files)
assert all(not any(parent.is_symlink() for parent in [p,*p.parents] if parent.is_relative_to(B)) for p in files)
report['manifest_files']=len(files)
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
final_rows=(f'| Kiểm cuối {report["utc"]} | cây read-only, exact SHA | HEAD/tree đúng; status/diff/index rỗng; 0 commit sau reviewed_sha | có |\n'
            f'| Manifest hiện vật lượt 10 | chỉ tệp thường, không tmp/symlink | {len(files)}/{len(files)} tệp khớp SHA-256; gồm VERDICT và hiện vật tự tạo | có |\n')
text=text.replace('\n### bia-mo-mot-ref-khong-thu-hoi-moi-ban', '\n'+final_rows+'\n### bia-mo-mot-ref-khong-thu-hoi-moi-ban',1)
text=text.replace(' |\n\n| Kiểm cuối',' |\n| Kiểm cuối')
vp.write_text(text)
manifest=B/'ARTIFACTS.sha256'
manifest.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(B))+'\n' for p in files))
check=subprocess.run(['sha256sum','-c','ARTIFACTS.sha256'],cwd=B,capture_output=True)
assert check.returncode==0,check.stderr.decode()
assert check.stdout.count(b': OK\n')==len(files)
print(json.dumps(report,ensure_ascii=False,indent=2))
print(f'ARTIFACTS.sha256: rc={check.returncode}, {len(files)}/{len(files)} OK')
