# Cross-review PR #455 — yêu cầu sửa

- `reviewed_sha`: `663da644d6edae52e5542e592614073d11f4e0f4`
- `reviewed_tree`: `15bdb6c8cc6159130841b18b4300cee65c0d237b`
- Base diff: `3bc2895b3915486631a44c392145a8d2aeba7768`
- Vai trò: reviewer độc lập với context Executor Claude; hai trục `spec`, `standards_security`.
- Provider: `openai_codex`; execution surface: Codex service/API với công cụ shell trong container; transport: `machine`. Không phải ChatGPT Web/human-mediated. Model được chỉ thị hệ thống định danh là GPT-6; không có chứng thực độc lập backend/model version.
- Authority: yêu cầu review trực tiếp trong `prompt.snapshot` do người dùng chỉ tới; write set duy nhất `VERDICT.md`. Không tự nhận Packet lease/generation mà prompt không cung cấp. Revision của chỉ thị được neo bằng SHA-256 `eed876691951f8d40965c4e2a31b9340dfd8ed2e683e207caa42b28af1163976`; locator run `ea42cb41` không được coi là chứng thực launcher.
- Review class áp dụng: `sensitive` do thay đổi identity/evidence gate. Báo cáo này không tạo approval, land authorization hay `cross_approved`.

Preflight: đúng origin `https://github.com/ducthangho/tra-luat`, detached HEAD đúng SHA, clone không nông, 1.718 commit; worktree ban đầu sạch. Đã đọc protocol, đặc biệt dòng 448–462 trước mã cổng. Diff gồm 13 tệp, bao gồm nối CI và đăng ký suite ngoài hai tệp Python/năm receipt; đã kiểm các phần đó. Không sửa cây được review; mọi đột biến nằm trong thư mục tạm ngoài repository. Không soạn nội dung tấn công mới.

## Kết quả đo lại lời khai

| Lời khai | Số đo độc lập | Kết luận |
|---|---|---|
| Trước vá: 62 receipt, 10 v2, 4 đủ, 6 thiếu | Đọc từng blob tại base, parse YAML và đối chiếu các trường tối thiểu: 62/10/4/6 | Khớp; “đủ” chỉ là cấu trúc theo bộ kiểm, không phải identity đã xác thực |
| Sau vá: 9 đạt, 11 miễn, 42 nợ, 0 vi phạm, tổng 62 | CLI in đúng 9/11/42/0/62; rc=0, `TỔNG: ĐẠT` | Khớp |
| Cutover đúng 11 tệp v1 | `ls-tree` + parse từng blob: 11/11 v1 | Khớp |
| 11 tệp byte-identical, allowlist đúng hash | 11/11 so byte và 11/11 so SHA-256 | Khớp |
| 15 ca, 5 đột biến có răng | 15/15; 5/5; rc=0 | Khớp, nhưng độ phủ có lỗ bên dưới |
| Release 180 → 180, không chứa hai tệp mới | Hai manifest đều 180, không có đường `ops/`; `release-verify --strict --json`: `ok=true`, checked=expected=180, failures=[] | Khớp |

Năm evidence URL mới: commit tra được; blob tại URL khớp từng byte với verdict hiện tại và khớp `verdict_sha256` **5/5**. Năm `reviewed_sha` đều là commit thật, mỗi `git cat-file -e <sha>^{commit}` rc=0. Điều này chưa chứng minh provenance của phiên reviewer hay trạng thái bảo vệ ref trên GitHub.

## F1 — P1: bánh cóc nợ khóa tên nhưng không khóa băm

**Vá ở đâu:** `ops/bien_nhan_v2_test.py:260`, `c13_no_chi_duoc_CO_LAI` và `NO_TRAN_DONG_BANG`. Cổng so băm tại `ops/bien_nhan_v2.py:278` nhưng giá trị chuẩn của nợ chỉ sống trong chính module được sửa. Test đóng băng tập tên, không đóng băng các cặp tên+băm.

**Bằng chứng:** trên bản sao, thêm một comment vô hại vào receipt nợ đầu tiên rồi thay băm tương ứng trong `NO_DA_DO`; giữ nguyên bộ test. Kết quả vẫn **rc=0, 15/15 ca, 5/5 đột biến CÓ RĂNG**. Thay đổi này đã tái đóng băng một bản không đạt v2, đúng hành vi mà cổng nói là cấm. Sửa `frozenset(bnv2.NO_DA_DO)` thành tập tên chép cứng chỉ đóng được việc thêm tên, chưa đóng lớp đổi nội dung rồi cập nhật baseline.

**Vá thế nào:** rẻ nhất là đóng băng độc lập 42 cặp tên+băm trong test và yêu cầu mỗi cặp còn lại của module khớp; chỉ cho phép bỏ cặp sau khi nâng receipt. Không sinh oracle từ module lúc import. Neo baseline vào blob Git bất biến mua thêm khả năng kiểm provenance nhưng cần phân biệt thiếu object với baseline sai. Đây là chốt regression/review, không thể chống người cố ý sửa cả cổng lẫn oracle nếu review cũng bỏ qua.

**Ca khóa:** script A bên dưới, nhánh `refreeze_debt_hash`, là phép đo đã chạy. Sau vá, subprocess đó phải rc khác 0 vì **c13 báo băm baseline lệch**, không vì lỗi giàn giáo. Giữ đối chứng dương cho nợ nguyên byte và cho xóa một mục đã nâng v2. Đột biến đổi băm baseline mà không đổi tập tên phải chết.

**Rủi ro bản vá:** đóng băng equality toàn bộ dict sẽ vô tình cấm co nợ; phải so tập con các cặp. Lấy baseline từ head đang kiểm tái tạo chính lỗi này. Baseline có thẩm quyền bị sửa đồng thời cần người review nhận ra.

## F2 — P1: “ĐẠT v2” vẫn nhận reviewed SHA viết tắt; test bỏ lọt việc gỡ trường bắt buộc

**Vá ở đâu:** `ops/bien_nhan_v2.py:200–225` (`_thieu`) và các ca cấu trúc trong `ops/bien_nhan_v2_test.py`. `reviewed_sha` hiện chỉ cần chuỗi không rỗng; protocol đòi exact Git OID. `t26` của suite lease kiểm path/hash verdict và tiền tố HTTPS, không kiểm `reviewed_sha`, nên không bù được lỗ này.

**Bằng chứng:** script B chỉ đổi format trường SHA trong fixture có sẵn từ `{sha}` thành `{sha:.7}`. Cả suite vẫn **rc=0, 15/15, 5/5**; ca đối chứng dương c4 nhận receipt có SHA dài 7 ký tự. Đây là lỗi hình dạng xác định được tại chỗ, độc lập với việc commit có thật hay clone nông.

Script A còn đo ba đột biến mã sản phẩm riêng rẽ: bỏ `TRUONG_CO_MAT`, bỏ `cuong_do` khỏi `ANCHOR_KHOA`, bỏ `reviewed_sha` khỏi `TRUONG_VO_HUONG`. **Cả ba đều rc=0, 15/15, 5/5.** Tên m3 “bỏ đòi hai identity” thực tế chỉ gỡ model identity; không đo submitter identity. Đây là cùng hình dạng lỗi: thiếu ca âm độc lập cho từng trường bắt buộc. Không nên tiếp tục vá từng tên ca riêng lẻ mà vẫn giữ ma trận thiếu trường rỗng.

**Vá thế nào:** kiểm `reviewed_sha` là full 40-hex theo hợp đồng kho này; kiểm hình dạng digest/URL có kiểu tương ứng, tách khỏi phép xác minh object/provenance. Dùng ma trận test các yêu cầu bắt buộc được chép từ spec, không sinh danh sách kỳ vọng từ hằng module; mỗi lần chỉ bỏ một trường. `github_submitter_identity: null` vẫn là đối chứng dương hợp lệ khi chưa đăng; vắng khóa phải đỏ. Không bắt null thành lỗi chỉ để làm ca đỏ.

**Ca khóa:** script B phải làm c4 đỏ vì fixture SHA ngắn, trong khi fixture full SHA gốc vẫn xanh. Ba đột biến của script A phải làm ca thiếu submitter/SHA/strength tương ứng đỏ. Thêm ca riêng cho null hợp lệ; nới lại kiểm độ dài SHA phải chết. Các mã script là phép đo, không phải bản vá sản phẩm.

**Rủi ro bản vá:** nhầm “hex đủ dài” với “commit có thật”; hoặc dùng tập trường từ module để sinh oracle khiến test tự co theo cổng. Đừng áp quy tắc URL blob cho mọi anchor: check object/protected ref có dạng khác. Các trường identity chưa có schema chi tiết cần giữ trạng thái không đo được, không tự suy identity từ dict không rỗng.

## F3 — P2: hai receipt mới nâng vẫn khai assurance vượt bằng chứng độc lập

**Vá ở đâu:** `ops/reviews/phan-bien-quy-trinh-review-{1,2}-claude-verdict.receipt.yaml:22,34–40` và caveat tương ứng trong `ops/reviews/README.md` nếu thay caveat. Chính các đoạn mới ghi tính độc lập KHÔNG ĐO ĐƯỢC, chạy subagent trong phiên điều phối, nhưng giải thích đó là lý do dùng `same_provider_approved`.

**Bằng chứng:** script C đọc hai receipt: cả hai `same_provider_approved`, `che_do=subagent_trong_phien_dieu_phoi`, `neo_boi_launcher=null`. Protocol §2/§8 yêu cầu same-provider cũng là phiên mới, context/worktree riêng. Thiếu chứng minh độc lập không trở thành mức approval cùng provider. Không kết luận subagent chắc chắn đã dùng chung context: điều đo được là chính receipt chưa chứng minh điều kiện cần.

**Vá thế nào:** giữ verdict lịch sử nguyên byte, sửa assertion assurance của delivery metadata thành `review_deferred`/ghi rõ chưa đủ authority theo schema hiện hành; chỉ phục hồi approved assurance nếu tìm được evidence độc lập có thể kiểm. Không bịa run ID hay prompt hash hồi tố. V1 cutover vẫn bất biến; finding này nói về hai receipt v2 đang được nâng trong PR.

**Ca khóa:** script C hiện in `DEFERRED_REQUIRED_ASSERTION False` hai lần. Khi chọn đường hạ assurance, biến biểu thức đó thành assertion cho đúng hai receipt lịch sử; phải true 2/2. Đột biến phục hồi `same_provider_approved` khi bằng chứng vẫn thiếu phải chết. Một cổng provenance tổng quát là phạm vi lớn hơn; chỉ bắt một từ trong prose không chứng minh được độc lập.

**Rủi ro bản vá:** không được đọc `review_deferred` thành “review chưa từng xảy ra”; verdict đã tồn tại nhưng authority chưa đủ. Lượt 3–5 có run ID/hash/đường launcher được ghi, nên không đồng nhất với lượt 1–2. Tôi không có run artifacts bên ngoài để chứng thực độc lập các lời khai lượt 3–5; chỉ xác minh được receipt/verdict/Git. Không yêu cầu bịa model version hoặc hạ mọi cross-provider receipt chỉ vì không biết tên model cụ thể.

## F4 — P2: lý do hoãn kiểm commit dựa trên cấu hình CI không đúng

**Vá ở đâu:** `ops/bien_nhan_v2.py:40–48`, chú thích clone nông trong `ops/bien_nhan_v2_test.py:13–16,241–251`, cùng đường kiểm anchor nếu triển khai nợ.

**Bằng chứng:** `.github/workflows/ci.yml:81–86` đã checkout `fetch-depth: 0`; suite mới được nối vào chính job `gate`. Script C parse cấu trúc workflow, xác nhận checkout depths `[0]`. Đây không phải lời khuyên dựa trên mặc định của một phiên bản Actions ngoài kho. Script A xác minh được cả năm blob URL và commit thật trên clone đầy đủ. Lý do “cần đổi workflow fetch-depth nhưng chưa làm” sai trên exact head này.

**Vá thế nào:** tối thiểu sửa mô tả nợ và đánh giá lại quyết định defer bằng cấu hình thật. Đường rẻ để làm phép kiểm: tái dùng lịch sử đã fetch trong job hiện tại, kiểm commit type và blob/path/hash đối với anchor Git; có thể gom truy vấn bằng Git batch. Không cần thêm fetch toàn lịch sử lần nữa. Với môi trường thật sự nông/thiếu object, khai KHÔNG ĐO ĐƯỢC, không suy là SHA bịa. Check object/protected ref cần verifier riêng; không bắt tất cả đi qua ancestry. Nếu vẫn giữ cổng chỉ kiểm cấu trúc thì khai nợ như quyết định phạm vi, không viện dẫn điều kiện CI sai. Finding này riêng lẻ không buộc phải mở rộng cổng sang xác minh mọi loại anchor.

**Ca khóa:** script C khóa tiền đề checkout của job; script A là đối chứng dương 5/5 blob/path/hash. Khi thêm verifier, dùng commit thật có sẵn nhưng không chứa verdict được yêu cầu làm ca âm; ca phải đỏ vì không có blob, và đột biến bỏ kiểm object/blob phải chết. Cần ca clone nông cho trạng thái không đo được. Các ca âm verifier tương lai này chưa chạy vì verifier chưa tồn tại; không nhận là pass.

**Rủi ro bản vá:** object tồn tại không chứng minh canonical ancestry, ref protection hay model identity; chỉ kiểm `cat-file -e <sha>` mà không kiểm type/path/bytes vẫn chưa đủ. Thiếu lịch sử không phải bằng chứng giả mạo. Không biến nợ xác minh Git thành lời tuyên bố đã chứng minh authority trên GitHub.

## Mã đo tái lập

Lưu từng khối vào tệp ngoài repository, chạy từ root clone bằng `PYTHONDONTWRITEBYTECODE=1 python3 <tệp>`. A/B/C là script đo đã chạy; assertion về đột biến sống mô tả trạng thái **trước sửa**, cần đảo kỳ vọng như các finding khi dùng làm regression. Bản sao chỉ dùng Git directory gốc cho các truy vấn đọc; không lệnh Git ghi nào được gọi.

### A — số đếm, Git anchors và bốn đột biến

```python
import os, sys, json, hashlib, subprocess, tempfile, shutil, importlib.util
from pathlib import Path
import yaml
R=Path.cwd()
os.environ['PYTHONDONTWRITEBYTECODE']='1'
def git(*args):
 p=subprocess.run(['git',*args],capture_output=True,cwd=R); assert p.returncode==0,(args,p.returncode,p.stderr); return p.stdout
def module(p):
 s=importlib.util.spec_from_file_location('measure_bnv2',p); m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=module(R/'ops/bien_nhan_v2.py')
base='3bc2895b3915486631a44c392145a8d2aeba7768'
paths=[p for p in git('ls-tree','-r','--name-only',base,'--','ops/reviews/').decode().splitlines() if p.endswith('.receipt.yaml')]
ds=[yaml.safe_load(git('show',base+':'+p)) for p in paths];v2=[d for d in ds if d.get('schema_version')==2]
print('BASE',json.dumps(dict(total=len(ds),v2=len(v2),complete=sum(not m._thieu(d) for d in v2),incomplete=sum(bool(m._thieu(d)) for d in v2))))
ps=[p for p in git('ls-tree','-r','--name-only','2f84531','--','ops/reviews/').decode().splitlines() if p.endswith('.receipt.yaml')]
print('CUTOVER',len(ps),'v1',sum(yaml.safe_load(git('show','2f84531:'+p))['schema_version']==1 for p in ps),'same_bytes',sum(git('show','2f84531:'+p)==(R/p).read_bytes() for p in ps),'hash_match',sum(hashlib.sha256(git('show','2f84531:'+p)).hexdigest()==m.ALLOWLIST_CUTOVER[Path(p).name] for p in ps))
for p in sorted((R/'ops/reviews').glob('phan-bien-quy-trinh-review-*.receipt.yaml')):
 d=yaml.safe_load(p.read_text());sha,path=d['evidence_url'].split('/blob/')[1].split('/',1);blob=git('show',sha+':'+path)
 q=subprocess.run(['git','cat-file','-e',d['reviewed_sha']+'^{commit}'],capture_output=True)
 print('ANCHOR',p.name,'reviewed_commit_rc',q.returncode,'bytes_match',blob==(R/d['verdict_path']).read_bytes(),'hash_match',hashlib.sha256(blob).hexdigest()==d['verdict_sha256'])
for rev in (base,'HEAD'):
 d=json.loads(git('show',rev+':RELEASE_MANIFEST.json'));print('MANIFEST',rev,d['file_count'],'ops_files',sum(f['path'].startswith('ops/') for f in d['files']))
source=(R/'ops/bien_nhan_v2.py').read_text()
mutations={
 'drop_submitter_requirement':('TRUONG_CO_MAT = ("github_submitter_identity",)','TRUONG_CO_MAT = ()'),
 'drop_anchor_strength_requirement':('ANCHOR_KHOA = ("loai", "cuong_do")','ANCHOR_KHOA = ("loai",)'),
 'drop_reviewed_sha_requirement':('TRUONG_VO_HUONG = ("receipt_id", "reviewed_sha",','TRUONG_VO_HUONG = ("receipt_id",'),
}
for name in [*mutations,'refreeze_debt_hash']:
 with tempfile.TemporaryDirectory(prefix='review455-') as td:
  t=Path(td);shutil.copytree(R/'ops',t/'ops');(t/'.git').write_text('gitdir: '+str(R/'.git')+'\n')
  code=source
  if name in mutations:
   a,b=mutations[name];assert code.count(a)==1;code=code.replace(a,b)
  else:
   n,old=next(iter(m.NO_DA_DO.items()));p=t/'ops/reviews'/n;p.write_bytes(p.read_bytes()+b'\n# review measurement\n');new=hashlib.sha256(p.read_bytes()).hexdigest();assert code.count(old)==1;code=code.replace(old,new)
  (t/'ops/bien_nhan_v2.py').write_text(code)
  p=subprocess.run([sys.executable,str(t/'ops/bien_nhan_v2_test.py')],capture_output=True,text=True,cwd=t)
  print('MUTATION',name,'rc',p.returncode,'summary',p.stdout.splitlines()[-2:]);assert p.returncode==0,p.stdout+p.stderr
print('MEASUREMENTS_COMPLETE')
```

### B — fixture SHA viết tắt vẫn được nhận

```python
import tempfile, shutil, subprocess, os
from pathlib import Path
r=Path.cwd()
with tempfile.TemporaryDirectory(prefix='review455-shape-') as td:
 t=Path(td)
 shutil.copytree(r/'ops',t/'ops')
 (t/'.git').write_text('gitdir: '+str(r/'.git')+'\n')
 f=t/'ops/bien_nhan_v2_test.py'
 s=f.read_text()
 assert s.count('reviewed_sha: {sha}')==1
 f.write_text(s.replace('reviewed_sha: {sha}','reviewed_sha: {sha:.7}'))
 p=subprocess.run(['python3',str(f)],capture_output=True,text=True,cwd=t,
                  env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 print('short_sha_fixture rc=',p.returncode)
 print('\n'.join(p.stdout.splitlines()[-2:]))
 assert p.returncode==0 and '15/15' in p.stdout and '5/5' in p.stdout
```

### C — cấu hình checkout và assertion assurance

```python
from pathlib import Path
import yaml, subprocess, sys, json
r=Path.cwd()
w=yaml.safe_load((r/'.github/workflows/ci.yml').read_text())
for name,job in w['jobs'].items():
 steps=job.get('steps',[])
 if any(s.get('run')=='python ops/bien_nhan_v2_test.py' for s in steps):
  depths=[s.get('with',{}).get('fetch-depth',1) for s in steps if s.get('uses','').startswith('actions/checkout@')]
  print('V2_JOB',name,'checkout_depths',depths);assert depths==[0]
for n in (1,2):
 p=r/f'ops/reviews/phan-bien-quy-trinh-review-{n}-claude-verdict.receipt.yaml'
 d=yaml.safe_load(p.read_text());print('ASSURANCE',n,d['assurance'],'mode',d['model_reviewer_identity']['che_do'],'launcher',d['model_reviewer_identity']['neo_boi_launcher'])
 print('DEFERRED_REQUIRED_ASSERTION',d['assurance']=='review_deferred')
print('POLICY_MEASUREMENTS_COMPLETE')
```

## TÔI ĐÃ ĐO ĐƯỢC GÌ / KHÔNG ĐO ĐƯỢC GÌ

Môi trường: Linux container, Python 3/PyYAML khả dụng, Git full clone; không sửa Git config. Các tiến trình Python dùng `PYTHONDONTWRITEBYTECODE=1`. Mã thoát dưới đây lấy từ công cụ tiến trình hoặc `subprocess.returncode`, không suy từ stdout.

| Command/phép đo | rc thật | Trạng thái và bằng chứng dương |
|---|---:|---|
| `python3 ops/bien_nhan_v2_test.py` | 0 | passed: 15/15 ca, 5/5 đột biến; tầng Git đo được 11 tên |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | passed theo cổng hiện tại: 9 đạt/11 miễn/42 nợ/0 vi phạm/62 tổng |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | passed: `ok=true`, checked=expected=180, failed/extra/missing rỗng, package hash khớp `397e9bf1f58dcf0400d6638dcc04090a6d1dfe4ba313fc6e6a8c628f6bf26cd2` |
| `python3 .claude/dev/ci_dang_ky_test.py` | 0 | passed: đăng ký 22/22, phản chứng 43/43 đỏ đúng |
| `python3 ops/lease_publish_test.py` | 0 | passed: 121/121, đã chạy=121, bỏ qua=0; có warning clone empty của fixture, không suy warning thành lỗi |
| `python3 /tmp/review455_measure.py` (A) | 0 | phép đo hoàn tất; Git/count/5 anchors khớp; **4/4 đột biến sống**, mỗi subprocess rc=0 + 15/15 + 5/5 — thất bại về khả năng khóa regression, không phải 4 tests an toàn pass |
| `python3 /tmp/review455_shape.py` (B) | 0 | tái hiện nhận SHA 7 ký tự; subprocess rc=0 + 15/15 + 5/5 — lỗi cấu trúc đã đo |
| `python3 /tmp/review455_policy.py` (C) | 0 | job gate depth=0; assertion mong muốn deferred hiện false 2/2; script đo không tự nhận assurance đạt |

`failed`: bất biến chống tái đóng băng nợ và exact-SHA bị phản chứng; không có suite gốc nào trả failed. `skipped`: lease suite báo 0; v2 đo được tầng Git, không bỏ qua tầng này. `not_run`: full runtime selftest, toàn bộ release/deploy gate, GitHub CI run/readback, Windows parity, LIVE và kiểm ref protection. Không tuyên bố gate toàn repository xanh hay PR đủ điều kiện land. Không đo được model/session identity của các run lịch sử từ launch artifacts bên ngoài clone; không đo được remote PR head hiện thời. Review chỉ neo local exact SHA nêu trên.

Kết luận: các số đếm công bố đúng nhưng chưa đủ để approve. Cần sửa F1/F2 và khai assurance đúng bằng chứng ở F3; F4 cần sửa tiền đề nợ, còn việc mở rộng verifier phải được quyết định rõ phạm vi. Không sửa mã sản phẩm, không commit/push/merge/deploy.

verdict: changes_requested
