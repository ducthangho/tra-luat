from pathlib import Path
import difflib, hashlib, json, shutil, subprocess
S=Path(__file__).resolve().parent;R=S.parent/'cay-kho';G=R/'ops/reviews/full-gate-pr468-20260907';O=S/'goi-y';O.mkdir(exist_ok=True)
old=(G/'README.md').read_text()
start=old.index('Mọi số dưới đây');end=old.index('## KẾT QUẢ')
replacement='''Bảng dưới tách số tự đếm được từ hiện vật đã giữ và số chỉ đọc lại từ log tổng hợp.
Không có `fullgate.sh`, stdout thô của năm bộ, stderr đầy đủ hoặc timestamp đầu/cuối
trong gói này. Chạy mới không tái tạo được bằng chứng của lần chạy lịch sử.

| số | cách trích từ gói | loại nguồn |
|---|---|---|
| `rc`, `out`, `giay` | đọc các trường trong `nen.rc` / `sau.rc` | log tổng hợp do executor giao; chưa có nguồn độc lập để xác thực lần chạy |
| `doc-claims-check` 70861 B mỗi vế | `wc -c nen.doc-claims.json sau.doc-claims.json` | tự đếm lại từ output được giữ |
| `cidk` / `ploop` | `wc -lc *.tail.txt`; đọc marker tổng | tự đếm tail 5 dòng, 206 B / 96 B; không tự đếm được stdout gốc 2934 B / 8752 B |
| `lease` | `wc -lc *.lease.norm.out`; `diff -u nen.lease.norm.out sau.lease.norm.out` | tự đếm 50 dòng, 8827 B mỗi bản norm; không tự đếm được raw 8971 B |
| 31 dòng đột biến, 0 dòng có `ĐỎ=[]` | `grep -c 'đột biến' nen.lease.norm.out`; `grep -Fc 'ĐỎ=[]' nen.lease.norm.out` (lặp lại cho sau) | tự đếm marker trong bản norm; không thay kết quả thực thi mutation |
| doctrine-scan / adr-song 69 B / 113 B | chỉ có trường out trong hai tệp rc | nội dung output lịch sử chưa được giao |
| thời lượng từng bộ | chỉ có trường giay trong hai tệp rc | thiếu timestamp đầu/cuối; chưa xác thực thời lượng và sai số lịch sử |

Bộ lọc và phần bỏ sót:

- `*.lease.norm.out` đã chuẩn hoá bằng `sed -E 's/lp_[a-z0-9_]+/LP/g'`.
  Không có raw để kiểm rằng chỉ tên thư mục tạm bị thay. Phép so chỉ chứng minh
  hai bản norm đang được giao bằng nhau; lần chạy mới không phục dựng byte lịch sử.
- `cidk` và `ploop` chỉ giữ 5 dòng cuối. Lỗi/warning giữa stdout không xem lại được.
  Marker tổng có giá trị trong phạm vi harness, chưa thay full stdout/command/launcher.
- doctrine-scan và adr-song thiếu nội dung output lịch sử; stderr các bộ không được
  giao đầy đủ. Không dùng output ở một gói/lần chạy khác thay thế mà không khai nguồn.
- Phạm vi là sáu bộ trong bảng, không phủ CI trên GitHub Actions hoặc mọi suite của kho.
- Cách kiểm danh sách số của tài liệu này: đọc mọi dòng README có chữ số bằng
  `python3 -c 'from pathlib import Path; import re; [(print(i, s)) for i, s in enumerate(Path("README.md").read_text().splitlines(), 1) if re.search(r"[0-9]", s)]'`,
  rồi phân loại bằng người thành số đo, định danh/SHA, câu lệnh hoặc lời khai lịch sử.
  Bộ lọc bắt cả ID/command và bỏ số viết bằng chữ, ý ngầm, tài liệu khác; đây là danh sách
  ứng viên, không phải danh sách các khẳng định đã chứng minh. Mỗi mục bỏ sót mà reviewer
  tìm ra vẫn được tính là finding; danh sách không giới hạn phạm vi review.

'''
new=old[:start]+replacement+old[end:]
new=new.replace('**DELTA = 0.** Khác duy nhất là số giây và tên thư mục tạm ngẫu nhiên. Chuẩn hoá xong,\n`nen.lease.norm.out` và `sau.lease.norm.out` giống hệt từng byte, **50/50 dòng**.', '**DELTA = 0 trong phần hiện vật giữ lại:** bốn cặp tail/norm/JSON bằng byte;\nrc và out trong hai log tổng hợp khớp, số giây khác. Chưa chứng minh toàn bộ stdout\nthô chỉ khác tên temp. Hai bản lease norm bằng nhau, **50/50 dòng, 8827/8827 B**.')
new=new.replace('**Không bộ nào `out=0B`.** Đây là phép kiểm có chủ đích:', '**Không trường `out` nào trong 12 dòng rc bằng 0B.** Bốn bộ có output/tail/norm\nđược giữ đều không rỗng; hai bộ còn lại chỉ có số trong log tổng hợp. Output không rỗng\nkhông đủ chứng minh pass: phải kiểm rc mong đợi và marker dương. Đây là phép kiểm có chủ đích:')
new=new.replace('Hệ quả phải ghi thẳng: **ca `t33` chưa từng được đo trong lần gate này.** Nó không đỏ, cũng\nkhông xanh — nó không chạy. Ai muốn đóng nó phải cài `actionlint` rồi chạy lại.', 'Hệ quả phải ghi thẳng: **t33 đã được gọi và thất bại ở tiền điều kiện thiếu actionlint;\nthao tác lint workflow chưa chạy trong lần gate này.** Log ghi ĐỎ t33 và tổng\n120/121 đạt; đã chạy=121, bỏ qua=0; suite rc=1. Muốn có kết quả lint phải cung cấp\nactionlint và đo mới có phạm vi/mốc riêng; không đổi kết quả lịch sử thành pass.')
(O/'full-gate-README.md').write_text(new)
oldmanifest=(G/'ARTIFACTS.sha256').read_text();newmanifest=oldmanifest.replace(hashlib.sha256(old.encode()).hexdigest()+'  ./README.md',hashlib.sha256(new.encode()).hexdigest()+'  ./README.md')
assert newmanifest!=oldmanifest
patch=''
for name,before,after in [('README.md',old,new),('ARTIFACTS.sha256',oldmanifest,newmanifest)]:
    path='ops/reviews/full-gate-pr468-20260907/'+name
    patch+=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/'+path,tofile='b/'+path))
(O/'full-gate-prose.patch').write_text(patch)
(O/'README.md').write_text('''# Gói gợi ý — hai P3 lượt 14

**chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**

`full-gate-prose.patch` sửa đúng README và hash README trong manifest full-gate.
`full-gate-README.md` là bản đầy đủ để đọc. Giữ nguyên rc/output/log; không chạy lại
full-suite/CI và không sửa verdict hoặc manifest reviewer lịch sử.

Finding áp dụng:

- `evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu`: phân loại số từ hiện vật,
  log tổng hợp và nguồn chưa giao; thu hẹp DELTA; khai cách trích ứng viên/giới hạn.
- `full-gate-t33-nham-that-bai-voi-khong-chay`: t33 đã chạy và fail ở tiền điều kiện;
  lint workflow chưa chạy, không đổi kết quả lịch sử.

Hai bổ sung prose tùy executor tái dẫn xuất (không nằm trong patch):

- DOC-MANIFEST13: nói rõ 55 tệp trong thư mục = 47 hiện vật có băm + 6 bundle đầu
  vào ngoài manifest + ARTIFACTS + DOC-MANIFEST; verdict ở ngoài nhưng có băm.
- Receipt13: trước mô tả model/session thêm “TỰ KHAI của bên vận chuyển; raw session
  và run.json lượt 13 chưa kèm để reviewer14 kiểm độc lập”; thêm giới hạn tương ứng
  vào KHONG_do_duoc. Nếu có đúng nguồn gốc, giao chúng với hash và mốc thay vì đoán.
  Không dùng run.json lượt 14; không tự sửa model_da_chay/assurance/verdict lịch sử.

Kiểm nghiệm ở bản sao scratch: patch --dry-run, áp bằng patch, đối chiếu byte với
bản gợi ý rồi sha256sum -c manifest full-gate. Kết quả ở ../prose-hint-check.json.
Rủi ro: đổi README quên hash sẽ phá 12/12; bộ lọc chữ số vẫn bỏ ý ngầm/số viết bằng
chữ; không được gọi nhãn “chưa đo” thành quyền bỏ qua gate hay nâng kết quả cũ.
''')
copy=S/'prose-check';target=copy/'ops/reviews/full-gate-pr468-20260907'
shutil.copytree(G,target)
checks=[]
for extra in [ ['--dry-run'], [] ]:
    cmd=['patch',*extra,'-p1','-d',str(copy)]
    p=subprocess.run(cmd,input=patch,text=True,capture_output=True)
    checks.append({'command':cmd,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    assert p.returncode==0,checks[-1]
assert (target/'README.md').read_text()==new
p=subprocess.run(['sha256sum','-c','ARTIFACTS.sha256'],cwd=target,capture_output=True,text=True)
checks.append({'command':['sha256sum','-c','ARTIFACTS.sha256'],'cwd':'do-review14/prose-check/ops/reviews/full-gate-pr468-20260907','rc':p.returncode,'ok':sum(s.endswith(': OK') for s in p.stdout.splitlines()),'stdout':p.stdout,'stderr':p.stderr})
assert p.returncode==0
(S/'prose-hint-check.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
print('Scratch patch dry-run/apply rc=0; exact suggested README bytes; manifest 12/12 rc=0')
