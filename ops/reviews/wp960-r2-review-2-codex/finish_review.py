"""Assemble final offline verdict only after all requested evidence is complete."""
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE=Path.cwd();repo=HERE/'cay-kho';p=HERE/'VERDICT.md'
SHA='ae0d06c23fb777545fd7547a07d9f368e4122f49'
def git(*a):
 q=subprocess.run(['git','-C',str(repo),*a],capture_output=True,check=True);return q.stdout
assert git('rev-parse','HEAD').decode().strip()==SHA
assert not git('status','--porcelain')
assert git('rev-parse','HEAD^{tree}').decode().strip()=='7312e5d65f57740d8673b5491357532c2b09c9a9'
assert hashlib.sha256((repo/'ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md').read_bytes()).hexdigest()=='9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca'
for name in ('ops/bien_nhan_v2.py','ops/bien_nhan_v2_test.py'):
 assert (repo/name).read_bytes()==git('show',SHA+':'+name)

def results(name):
 return [json.loads(x) for x in (HERE/'evidence'/name).read_text().splitlines() if x.startswith('{') and '"cases"' in x]
new=results('new-mutants.log');old=results('old-mutants.log')
assert len(new)==7,len(new)
assert len(old)==5,len(old)
assert all(r['cases']==89 for r in new+old)
survivors={'n1-vang-stat','n2-vang-oserror','n3-peel-rc','n4-ref-show-error','n7-peel-noncommit'}
assert {r['mutation'] for r in new if not r['red']}==survivors,new
assert all(r['passed']==88 and all(x[1]=='giet_that' for x in r['red']) for r in new if r['mutation'] not in survivors)
assert all(r['passed']==(87 if r['mutation']=='r8-receipt-encoding' else 88) and all(x[1]=='giet_that' for x in r['red']) for r in old)
s=p.read_text()
s+='''

Bổ sung hoàn tất Hướng 11 — bảng cuối (tất cả đã chạy hết 89 ca, không chỉ target):

| mutant reviewer | chốt thay đổi trên bản sao | kết quả | ca đỏ đúng |
|---|---|---|---|
'''
labels={
'n1-vang-stat':'_vang: lstat → stat',
'n2-vang-oserror':'_vang: OSError → return True',
'n3-peel-rc':'_peel_commit: bỏ kiểm rc / OID đầu ra',
'n4-ref-show-error':'_nhanh_mac_dinh: lỗi show-ref → continue',
'n5-sinh-no-utf8':'_sinh_no: bỏ riêng UnicodeDecodeError',
'n6-sinh-no-yaml':'_sinh_no: bỏ riêng yaml.YAMLError',
'n7-peel-noncommit':'_commit_cua: bỏ lọc None sau peel',
}
for r in new:
 red=', '.join(x[0].split('_')[0]+'/'+x[1] for x in r['red']) or '**KHÔNG CÓ**'
 s+=f"| {r['mutation']} | {labels[r['mutation']]} | {r['passed']}/{r['cases']} | {red} |\n"
s+='''
Năm mutant n1/n2/n3/n4/n7 ở năm chốt khác vị trí với m103–m113. n5/n6 là hai phép gỡ nhỏ hơn tại nhóm except mà m109 gỡ cả nhóm; ghi riêng kết quả, không dùng chúng thay cho năm chốt độc lập. Hai mutant n5/n6 giết đúng c92 vì UnicodeDecodeError/ParserError thoát CLI; không tính exception từ giàn giáo làm răng.

Bổ sung finding chot-loi-do-moi-chua-co-rang: n3 và n4 cũng sống sót 89/89. n3 bỏ bảo vệ `_peel_commit:1123`, làm object zlib hỏng từ nguyên trạng rc=2 thành rc=0. n4 bỏ bảo vệ `_nhanh_mac_dinh:1155` với git show-ref rc=128, làm ref chứa OID không có từ rc=2 thành fallback/rc=1. Gộp cùng n1/n2 vì đều là chốt lỗi đo mới chưa có ca khóa. Bằng chứng `evidence/new-mutants.log` và `evidence/witness-n{3,4}-*.log`.

### loc-ung-vien-commit-chua-co-rang [P1] Bỏ lọc object không peel thành commit mà 89 ca vẫn xanh
HÌNH DẠNG: bo-chon-ung-vien
TỆP/DÒNG: `ops/bien_nhan_v2.py:1141`; ca mơ hồ c91 tại `ops/bien_nhan_v2_test.py:3130`, đột biến m105 tại `3845`.
VẤN ĐỀ: Resolver mới phải phân ứng viên là commit với blob/tag không trỏ commit; chốt `if c` loại None sau peel quyết định điều đó. Ca c91/m105 chỉ dùng hai commit trùng tiền tố. Bỏ riêng `if c` làm `{commit, None}` bị báo là hai commit và đẩy lời khai có thể đo sang trạng thái mơ hồ/rc=2, trong khi tất cả 89 ca hiện hữu vẫn đạt. M6 đòi chốt này có răng.
ĐÃ THỬ NGHIỆM: `python3 -u new_mutations.py ... n7-peel-noncommit` ⇒ `89/89, red=[]`. `python3 -u mutant_witnesses.py`, cùng fixture commit `8ac070d5f378d156c368085f9bd62a4b9257b14a` + blob `8ac070dd934a9b962f63a96d2eec64e4304e8d46`: Git peel chọn được commit; nguyên trạng CLI rc=1, mutant rc=2/`mơ hồ — 2 commit chung tiền tố`. Cặp commit+tag trỏ blob cũng đổi sai tương tự. Log `evidence/collisions.log`, `evidence/witness-n7-peel-noncommit.log`, `evidence/new-mutants.log`.
ĐỘ TIN: cao

Bổ sung đóng finding lượt 1: năm mutant r2/r4/r5/r6/r8 đã kết thúc: bốn mutant selector **88/89**, đúng một ca đỏ `giet_that` c87/c87/c88/c88; mutant UTF8 r8 **87/89**, cả c91 và c92 đỏ đúng UnicodeDecodeError ở đường đọc receipt. Đây là chạy lại cả bộ ca trên từng bản sao, xác nhận răng mới khóa đúng năm chốt từng sống sót ở lượt trước (`evidence/old-mutants.log`).

## TÍNH TOÀN VẸN VÀ GIỚI HẠN

'''
checks={'head':SHA,'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'status':git('status','--short').decode(),'files':{name:hashlib.sha256((repo/name).read_bytes()).hexdigest() for name in ('ops/bien_nhan_v2.py','ops/bien_nhan_v2_test.py')},'diff_check':0}
git('diff','--check','44884446f71c89e25f9a72ac58e4f597db63c1ba','HEAD')
(HERE/'evidence/final-tree.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
s+=f"Kiểm cuối (`evidence/final-tree.json`): HEAD vẫn `{SHA}`, tree `{checks['tree']}`, status rỗng; hai tệp byte-identical với blob tại SHA; `git diff --check 4488444 HEAD` rc=0. SHA256 cổng `{checks['files']['ops/bien_nhan_v2.py']}`, test `{checks['files']['ops/bien_nhan_v2_test.py']}`.\n"
s+='''
Không sửa cay-kho/, không push, không gọi mạng. Chỉ đo code/fixture hiện hữu và đột biến trên bản sao. Không tạo HINT.patch; verdict này không đưa bản vá. Các log thử giàn giáo bị lỗi đã chỉ rõ và loại khỏi kết luận; corpus, suite, target mutation và phản chứng dùng các log cuối được nêu trong từng hướng.

Không xác minh PR/check run online hoặc việc ghi numstat vào PR. Shallow và partial clone (blob:none qua file://, có promisor pack/blob thiếu) đã đo trên fixture local; không đo máy chủ từ xa hoặc mọi filter, không bảo đảm ancestry ngoài lịch sử có sẵn. FIFO không thử vì có thể chặn đọc vô hạn; không gán kết quả chưa đo thành pass. Thời gian benchmark chỉ có ý nghĩa ở lượt chạy quan sát này. Không suy execution surface/transport từ tên launcher hoặc tên reviewer.

Các hình dạng **loi-do** và **bo-chon-ung-vien** tái xuất. Theo spec r2 Q8 / lease M-4, executor phải dừng để chủ kho quyết định trước khi vá tiếp; verdict không cấp quyền sửa, merge hoặc land.
'''
s=s.replace('Đang đo; từng hướng sẽ được nối thêm cùng lệnh và output.','Đã hoàn tất 12 hướng dưới đây; từng hướng có lệnh và output thật, cùng log/script tái lập trong thư mục giao việc này.')
s=s.replace('Hướng 11: 7 mutant độc lập đang chạy cả 89 ca trên từng clone; đã xác nhận n1/n2 sống sót và có phản chứng không tương đương','Hướng 11: 7 mutant chạy cả 89 ca; 5 chốt khác vị trí m103–m113 đều sống sót, 2 mutant nhỏ của except bị c92 giết')
s=s.replace('Chưa đạt M6; bảng đầy đủ được nối khi chạy xong','Không đạt M6; bảng cuối đủ 7 mutant và phản chứng không tương đương')
s=s.replace('Chốt phân biệt nguồn vắng và nguồn hỏng vẫn có thể bị gỡ mà 89 ca xanh','Bốn chốt lỗi đo vẫn có thể bị gỡ mà 89 ca xanh')
s=s.replace('`ops/bien_nhan_v2.py:1123`, `1168`–`1173`; ca c91','`ops/bien_nhan_v2.py:1123`, `1155`, `1168`–`1173`; ca c91')
sevs=collections.Counter(re.findall(r'^### [a-z0-9-]+ \[(P[0-3])\]',s,re.M))
assert sevs=={'P1':5},sevs
lines=s.splitlines();lines[0]='verdict: changes_requested';lines[1]='reviewed_sha: '+SHA;lines[2]='Kết quả: '+', '.join(f"{sevs[f'P{i}']} P{i}" for i in range(4))+'.'
p.write_text('\n'.join(lines)+'\n')
print(lines[0]);print(lines[1]);print(lines[2]);print('new_mutants=7; old_mutants=5; source_clean=true')
