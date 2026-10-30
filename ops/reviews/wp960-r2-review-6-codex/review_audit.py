import ast
import json
from pathlib import Path
import re
import subprocess
import sys
import yaml
from review_checks import ROOT, TMP, record
from review_mutations import load

t=load(TMP/'head/ops/bien_nhan_v2_test.py','audit')
b=t.bnv2

def g(*args):
    return subprocess.run(['git','-C',str(ROOT),*args],capture_output=True,text=True,env=b._env_git())

if sys.argv[1]=='baseline':
    base=load(TMP/'base/ops/bien_nhan_v2.py','base_gate')
    t.bnv2=base
    results=[]
    for name in ['c86_B1_moc_dung_tai_KHONG_con_mien','c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback','c87_B3_OID_khong_tra_duoc_theo_NGU_CANH','c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan']:
        result=t._chay_1(getattr(t,name))
        results.append(result)
        print(name,result,flush=True)
    assert all(x[0]=='giet_that' for x in results)
    record('Hướng 14 — B8 hồi dựng trên exact base', 'Lệnh `python3 -B -u review_audit.py baseline`: dùng module gốc từ4488444 với bốn ca hiện hữu c86/c89/c87/c88. Lần lượt đỏ đúng: mốc còn miễn câu (rc0), receipt-thư-mục thoát IsADirectoryError, OID40 thiếu thànhrc0, dòng trích dẫn bị nhậnrc1. Đây là kết quả nền cần ĐỎ theo B8, không phải finding ở HEAD; ca tương ứng trên HEAD đã qua. Log `evidence/baseline.log`. Không khai đã chứng kiến thời điểm executor trước khi bắt tay; đây là hồi dựng ngoại tuyến.')
else:
    receipts={p.name:yaml.safe_load(p.read_text()) for p in (ROOT/'ops/reviews').glob('*.receipt.yaml')}
    def at(d,field):
        for word,index in re.findall(r'([^.[\]]+)|\[(\d+)\]',field):
            d=d[int(index)] if index else d[word]
        return d
    default=g('rev-parse','refs/remotes/origin/HEAD').stdout.strip()
    rows=[]
    cache={}
    for name,field,rule in sorted(b.NO_CAU_LICH_SU):
        d=receipts[name]
        text=' '.join(str(at(d,field)).split())
        proof=[]
        for sentence in b._RE_CAU.split(text):
            norm=b._bo_dau(sentence)
            if rule=='L-ANCESTRY' and b._RE_ANCESTRY.search(norm):
                for token in b._RE_OID.findall(sentence):
                    if token not in cache:
                        p=g('rev-parse','--verify','--quiet',token+'^{commit}')
                        cache[token]=p.stdout.strip() if p.returncode==0 else None
                    sha=cache[token]
                    if sha:
                        p=g('merge-base','--is-ancestor',sha,default)
                        assert p.returncode in (0,1) and not p.stderr
                        if p.returncode==0: proof.append((token,sha))
            elif rule=='L-REVIEW' and b._RE_CHUA_REVIEW.search(norm):
                for token in re.findall(r'(?<![0-9a-z])[0-9a-f]{40}(?![0-9a-z])',sentence):
                    for other,nd in receipts.items():
                        if other!=name and isinstance(nd,dict) and nd.get('reviewed_sha')==token and nd.get('luot',0)>d.get('luot',0):
                            proof.append((other,nd.get('luot')))
        assert proof,(name,field,rule,text)
        rows.append(dict(file=name,field=field,rule=rule,proof=proof))
        print(json.dumps(rows[-1],ensure_ascii=False),flush=True)
    tree=ast.parse((ROOT/'ops/bien_nhan_v2.py').read_text())
    forbidden=[n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and (n.name.startswith('_moc_') or n.name in ['_commit_them_cau','_co_cau'])]
    forbidden += [n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and n.value=='dung_tai']
    assert not forbidden
    print('audit_debt_keys=',len(rows),'all_independent_git_or_receipt_proofs=true','forbidden_executable_moc=',forbidden,flush=True)
    record('Hướng 15 — bằng chứng độc lập cho61khóa nợ và mã bỏ mốc', 'Lệnh `python3 -B -u review_audit.py debt`: duyệt từng khóa đóng băng;60khóa ancestry có ít nhất1commit tra bằng `git rev-parse --verify --quiet <token>^{commit}` rồi Git merge-base=0/stderr rỗng;1khóa review có biên nhận khác đúng40hex và luot lớn hơn. **61/61 có bằng chứng độc lập**, không dùng `_commit_cua`/kết quả vi_pham_cau làm oracle. AST mã sản phẩm không còn literal dung_tai hay hàm mốc/lịch sử bị cấm. Log `evidence/debt-audit.log`. Regex vẫn chỉ chọn ứng viên theo phạm vi đặc tả.')
