# Cross-review vòng 2 — PR #455

**Yêu cầu sửa: 1 P1 và 3 P2.** Các con số chạy nền khớp, nhưng chưa đủ để đóng bản vá.

- `reviewed_sha`: `c595292cb63fb8c09d7d7b482cda20f9d5f0917f`
- `reviewed_tree`: `7c222dcf02eb663ea79fe1fd04867698947990bd`
- Base của bản vá: `663da644d6edae52e5542e592614073d11f4e0f4`.
- Vai trò: Reviewer độc lập với Executor Claude, hai trục `spec` và `standards_security`; review class `sensitive` vì đây là cổng bằng chứng/identity.
- Provider `openai_codex`; execution surface **Codex service/API, shell trong Linux container**; transport `machine`. Model được chỉ thị hệ thống định danh GPT-6; không có chứng thực độc lập backend/version. Không khai đây là ChatGPT Web hay một run Codex CLI được launcher chứng thực.
- Authority: yêu cầu review trực tiếp trong `prompt.snapshot` mà user chỉ tới; SHA-256 chỉ thị `2f091abac3779eae6510b9b3ca82bbfe96c1025ea9ef510512b4474538576767`. Revision review là vòng 2 trên exact head trên. Prompt không cấp Packet lease/generation riêng; không tự tạo các giá trị đó hay quyền transition/land. Write set duy nhất: `VERDICT.md`.

Preflight đo được: origin `https://github.com/ducthangho/tra-luat`, detached HEAD đúng SHA, full clone (`is-shallow-repository=false`), 1.720 commit, worktree ban đầu sạch. Đã đọc verdict vòng 1 và đối chiếu bản vá 9 tệp với hợp đồng protocol về review, receipt và ba trạng thái. Mọi fixture/đột biến chạy ngoài repository; không sửa mã sản phẩm, không commit/push. Phép đo dùng fixture có sẵn và đột biến bản vá, không soạn nội dung tấn công nhạy cảm.

## Đóng finding vòng 1 đến đâu

| Finding cũ | Kết quả độc lập |
|---|---|
| F1 — khóa tên mà không khóa băm | **Đóng trong phạm vi regression đã nêu.** Sửa receipt nợ bằng comment vô hại rồi cập nhật băm sản phẩm: suite rc=1, chính c13 báo băm baseline lệch; 22/23 ca. Không còn sống như vòng 1. |
| F2 — SHA viết tắt và thiếu độ phủ | Kiểm full SHA và ba đột biến cũ đã được khóa. **Chưa đóng lớp thiếu nhánh**: ba đột biến mới vẫn rc=0, 23/23, 12/12; xem R2-03. |
| F3 — hai receipt nâng assurance quá bằng chứng | **Đóng sửa metadata của đúng hai receipt**: cả hai `review_deferred`; hai verdict `.md` khớp byte với base, Git đọc blob rc=0. Gỡ toàn bộ chốt assurance làm c4d đỏ đúng, rc=1. Chốt tổng quát vẫn chưa được chứng minh đầy đủ; xem R2-03 và giới hạn bên dưới. |
| F4 — tiền đề depth sai | Tài liệu trong diff đã rút tiền đề. `_neo_git` thực sự chạy trên full clone; receipt vòng 1 cũng tự qua, không miễn trừ/nợ. **Phần xác minh mới còn lỗi R2-01/R2-02**. Không đo được mô tả PR/commit message đã công bố trên remote có được sửa hay chưa. |

Lưu ý dữ kiện nguồn: verdict vòng 1 trong cây ghi F1/F2 là P1 và F3/F4 là P2, không phải 3 P1 + 1 P2 như bảng dẫn trong prompt. CHANGELOG nói thêm một reviewer khác; không gộp mức độ của reviewer đó thành nội dung verdict đang kiểm.

## R2-01 — P1: trạng thái chưa xác minh vẫn thành cổng xanh, và dispatch còn bỏ qua mỏ neo

**Vá ở đâu:** `ops/bien_nhan_v2.py:354` (`_neo_git`), `:442` (`kiem`, nhận `g_chua` rồi vẫn tăng `dat`), `:493–497` (`main`); `_anchor` tại `:134` chuẩn hóa loại bằng `strip()` nhưng dispatch tại `:354` so giá trị thô. Test liên quan c21/c22/c14.

**Bằng chứng chạy được:** script A dùng lại `_kho_git`/`_bn_neo` của c18–c21; đối chứng commit/path/hash đúng: rc=0, 1 đạt, 0 chưa đo. Sau mỗi đột biến độc lập:

| Đột biến fixture có sẵn | rc thật | CLI |
|---|---:|---|
| SHA không có object, đúng dữ liệu c21 | 0 | `1 ĐẠT v2`, `1 KHÔNG ĐO ĐƯỢC`, **`TỔNG: ĐẠT`** |
| Loại `protected_evidence_ref`, URL PR có sẵn từ c22 | 0 | 1 đạt, **0 chưa đo**, `TỔNG: ĐẠT` |
| Loại `check_object`, cùng URL PR | 0 | 1 đạt, **0 chưa đo**, `TỔNG: ĐẠT` |
| Thêm khoảng trắng quanh `canonical_ancestry`, cùng URL PR | 0 | 1 đạt, **0 chưa đo**, `TỔNG: ĐẠT` |

Hai loại anchor khác được protocol cho phép, nên không kết luận URL của chúng phải là blob. Lỗi là **không có verifier mà cũng không ghi trạng thái chưa đo**. Ca khoảng trắng chứng minh chính chốt c22 vừa thêm còn bị bỏ qua do schema và dispatch dùng hai cách đọc khác nhau. Khi `_neo_git` có ghi chưa đo, CLI lại biến nó thành pass. Đây là một lớp thất bại xuyên pipeline, không phải bốn P1 riêng.

**Vì sao P1:** chỉ cần đổi metadata của receipt là có thể bỏ phép xác minh vừa thêm, hoặc trình object chưa xác minh như gate đạt; không cần sửa test/cổng, không cần đặc quyền hay lỗi môi trường. Đây là hở trực tiếp ở đường quyết định của bản vá. Không khẳng định cổng này tự cấp merge authority.

**Vá thế nào:** chuẩn hóa/kiểm loại một lần và dùng cùng kết quả cho dispatch. Mỗi loại hợp lệ phải có kết quả xác minh hoặc trạng thái chưa đo rõ ràng; chưa có verifier cho protected ref/check object thì giữ nợ xác minh rõ ràng, không giả định đã qua. Tổng hợp `chua_do` ra rc=2 và không in marker tổng đạt; lỗi xác định vẫn rc=1. Tách số đạt cấu trúc khỏi số đã xác minh nếu muốn giữ thống kê cấu trúc. Không cần dựng verifier GitHub đầy đủ chỉ để đóng đường báo sạch này.

**Ca test khóa:** dùng nguyên các ca của script A, yêu cầu SHA vắng ⇒ rc=2 và không có `TỔNG: ĐẠT`; loại chưa có verifier ⇒ chưa đo/rc=2; loại canonical có whitespace phải đi cùng đường kiểm như dạng chuẩn (hoặc bị từ chối hình dạng), không pass URL PR. Đột biến bỏ tổng hợp trạng thái thứ ba và đột biến quay về so loại thô phải chết. Giữ đối chứng commit/blob đúng rc=0 và path sai rc=1.

**Rủi ro bản vá:** clone nông/thiếu object sẽ chặn gate với **chưa đủ bằng chứng**, không phải bị kết tội SHA giả. Không ép mọi anchor thành canonical ancestry; không vô tình áp xác minh mới vào 11 receipt v1 miễn trừ hoặc 42 nợ nguyên byte.

## R2-02 — P2: so băm blob chấp nhận cả byte đã bị chuẩn hóa

**Vá ở đâu:** `_git` tại `ops/bien_nhan_v2.py:315–317` và `_neo_git:377–391`. `_git` dùng text mode và `.strip()`; `_neo_git` băm kết quả ấy, chỉ đọc lại nhị phân nếu băm đã chuẩn hóa khác băm khai.

**Bằng chứng:** script A dùng chính nội dung fixture c18 có newline cuối. Giữ nguyên blob Git, đổi riêng digest của receipt thành digest của nội dung `.strip()`. Đo `RAW_HASH_DIFFERS=True`, nhưng CLI vẫn rc=0, 1 đạt, 0 chưa đo, `TỔNG: ĐẠT`. Đối chứng digest byte gốc cũng rc=0. Như vậy một blob đang được chấp nhận với **hai digest khác nhau**; đây không phải va chạm SHA-256 mà là băm hai biểu diễn.

**Vá thế nào:** đọc blob bằng đường bytes ngay từ đầu và chỉ băm đúng stdout khi tiến trình thành công. Giữ helper text cho OID nếu cần. Lỗi đọc/timeout phải vào chưa đo; kiểm returncode của đường bytes, không băm stdout của tiến trình thất bại. Không cần normalize nội dung verdict.

**Ca test khóa:** `normalized_hash` trong script A phải rc=1 do băm blob lệch, đối chứng byte gốc vẫn rc=0. Thêm cặp LF/CRLF và whitespace đầu/cuối để khóa việc đổi byte qua text mode. Đột biến khôi phục nhánh chấp nhận digest sau `.strip()` phải chết. Ca fixture LF đã chạy; CRLF là đề xuất, chưa chạy.

**Rủi ro bản vá:** receipt trước đây khai digest của nội dung đã chuẩn hóa sẽ bị phát hiện; đó là lệch byte thật, không phải lý do nới so băm. Không suy byte-match thành canonical ancestry hay identity đã chứng thực.

## R2-03 — P2: ma trận khóa tên yêu cầu, chưa khóa các nhánh của yêu cầu

**Vá ở đâu:** `ops/bien_nhan_v2_test.py:127–139` (`MA_TRAN`), c16/c17 tại `:263–292`, c4d tại `:205`; tương ứng `_mri`, `_gsi`, `_thieu` trong sản phẩm.

**Bằng chứng:** script A sửa mã sản phẩm trên bản sao, giữ nguyên test. Cả ba đều **rc=0, 23/23 ca, 12/12 đột biến CÓ RĂNG**:

1. Bỏ kiểm `actor` trong `_gsi`.
2. Cho nhánh MRI không phải dict/rỗng trả `None`.
3. Đổi điều kiện assurance từ `trong_phien or khong_neo` thành `trong_phien and khong_neo`.

Ma trận chỉ thử submitter sai kiểu, MRI dict có khóa không đúng, và c4d bật **cả hai** điều kiện cùng lúc. Vì thế tên yêu cầu vẫn đủ nhưng một số nhánh không còn được kiểm vẫn xanh. Đối chứng gỡ hẳn chốt assurance chết đúng c4d (rc=1), nên không phải mọi phép đo đều vô hiệu. Đây là finding độ phủ, không tuyên bố sản phẩm hiện đã bỏ ba kiểm tra trên; vì vậy xếp P2.

**Vá thế nào:** giữ bảng yêu cầu độc lập, nhưng cho mỗi yêu cầu có nhiều ca theo nhánh cần thiết: vắng/null/sai kiểu/rỗng/đủ tối thiểu; với assurance cần từng điều kiện đơn độc, cả hai, và không điều kiện. Khóa dữ kiện cũ của F3 riêng. Không tự sinh oracle từ predicate đang được kiểm; không dùng “đúng một ca mỗi yêu cầu” làm trần độ phủ.

**Ca test khóa:** cả ba cặp neo/thay trong script A phải làm ca đích đỏ sau vá, trong khi đối chứng MRI hợp lệ, submitter null và assurance deferred vẫn xanh. Các đột biến giữ nguyên tên `YEU_CAU` nên c16 không phải oracle đủ; phải có assertion về hành vi.

**Rủi ro bản vá:** không biến mọi thiếu launcher thành bằng chứng không độc lập. Protocol cho human audit và session độc lập không bắt buộc launcher; chốt hiện tại suy quá rộng từ `neo_boi_launcher: null` và tìm chữ `subagent` trong prose. Cần làm rõ trường nào là attestation có kiểu trước khi mở rộng chốt tổng quát. Chưa đo một receipt hợp lệ thực tế bị từ chối oan, nên không thêm finding production riêng về khả năng đó. Tương tự, fallback `assurance or assurance_dat` chưa chứng minh hai trường đồng thời nhất quán; không dùng nó làm bằng chứng provenance tổng quát.

## R2-04 — P2: m9 không nới URL như tên khai, vẫn nhận tín dụng đo sai thuộc tính

**Vá ở đâu:** `_dot_bien` trong `ops/bien_nhan_v2_test.py`, m7/m9 và cách đối chiếu ca đích c19. Đây là lỗi ý nghĩa của phép đo, không phải exception giàn giáo.

**Bằng chứng:** script B trích **nguyên regex từ AST của bản vá**, không viết regex thay thế. Cả m7 và m9 đều không match URL blob hợp lệ. Khi áp từng mutant:

- c18 (mỏ neo đúng) trả `giet_that`: bị từ chối ở hình dạng URL.
- c19 cũng trả `giet_that`: cổng không tới phép kiểm path mà trả lỗi URL.
- **c22 vẫn `qua`**: URL không ghim vẫn bị chặn.

m9 được đặt tên “cho canonical ancestry dùng URL không ghim”, nhưng nó không cho qua URL ấy. Các dấu escape trong regex hiện tại khiến nó không thực hiện sự nới được mô tả. m7 và m9 đều khiến verifier từ chối ngay ở URL, thay vì bỏ/nới đường đo như tên gọi. Số **12/12** đúng theo bộ phân hạng hiện tại, nhưng không chứng minh 12 thuộc tính đã được khóa. Không gọi đây là crash bị tính thành kill; phép assert có chạy, nhưng đo khác điều được công bố.

**Vá thế nào:** dùng mutant thực sự làm yếu đúng predicate; kiểm tiền điều kiện của mutant bằng readback hành vi. Chạy thêm đối chứng dương dưới mutant để phát hiện kiểu “từ chối tất cả”. Chốt URL không ghim phải có ca đích c22; bỏ phép kiểm path phải nhắm đúng đường đó, không phá parser URL để c19 chết vì lý do khác.

**Ca test khóa:** script B đã cho phép tái lập sai khác. Sau thay mutant, yêu cầu mutant URL vẫn nhận dạng URL hợp lệ, làm c22 phát hiện chấp nhận URL không ghim, và giữ c18 qua. Mutant bỏ path phải để c18 qua, c19 chết do path sai được nhận. Nếu mutant không đạt tiền điều kiện ấy thì ghi lỗi giàn giáo/đột biến, không cấp “CÓ RĂNG”.

**Rủi ro bản vá:** sửa escape đơn thuần có thể tạo regex match nhưng thiếu capture groups, sinh crash; đó cũng không phải kill đúng nghiệp vụ. Không dùng bán kính đúng một ca làm luật cứng cho mọi mutant: có predicate dùng chung, nhưng phải giải thích và đo đúng thuộc tính.

## Mã đo tái lập

Hai script dưới đã chạy từ root clone với `PYTHONDONTWRITEBYTECODE=1`; chỉ ghi thư mục tạm ngoài repository. Script A giữ assertion hiện tại để ghi nhận phép đo; khi chuyển thành regression, đảo kỳ vọng các ca lỗi theo finding. Script không phải bản vá sản phẩm.

### Script A

```python
import os, sys, tempfile, shutil, subprocess, importlib.util, hashlib, copy
from pathlib import Path
import yaml
R=Path.cwd(); os.environ['PYTHONDONTWRITEBYTECODE']='1'
def mod(p):
 s=importlib.util.spec_from_file_location('probe',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
t=mod(R/'ops/bien_nhan_v2_test.py'); m=t.bnv2
# Reuse the existing c18-c21 fixture; only mutate fields/representation.
with tempfile.TemporaryDirectory(prefix='r2-fixture-') as td:
 root=Path(td); sha,bam,path=t._kho_git(root,'noi dung verdict\n')
 d=t._bn_neo(sha,bam,path); p=root/m.THU_MUC/'a-verdict.receipt.yaml'
 def run(label,d):
  p.write_text(yaml.safe_dump(d),encoding='utf-8')
  q=subprocess.run([sys.executable,str(R/'ops/bien_nhan_v2.py'),'--root',str(root)],capture_output=True,text=True)
  print(label,'rc',q.returncode,' '.join(q.stdout.split()),'stderr',q.stderr.strip())
  return q
 assert run('control',d).returncode==0
 x=copy.deepcopy(d); x['reviewed_sha']='deadbeef'*5; run('c21_missing_object_CLI',x)
 for kind in ['protected_evidence_ref','check_object']:
  x=copy.deepcopy(d); x['anchor']['loai']=kind
  x['evidence_url']='https://github.com/o/r/pull/1'
  run('unmeasured_'+kind,x)
 x=copy.deepcopy(d); x['anchor']['loai']=' canonical_ancestry '
 x['evidence_url']='https://github.com/o/r/pull/1';run('anchor_whitespace_dispatch',x)
 raw=(root/path).read_bytes(); x=copy.deepcopy(d)
 x['verdict_sha256']=hashlib.sha256(raw.decode().strip().encode()).hexdigest()
 print('RAW_HASH_DIFFERS',bam!=x['verdict_sha256']);run('normalized_hash',x)
# Repeat product mutations against the unchanged full suite in isolated copies.
source=(R/'ops/bien_nhan_v2.py').read_text()
mutations={
 'drop_submitter_actor':('if not str(v.get("actor") or "").strip():','if False:'),
 'drop_mri_container':('return "thiếu/rỗng ánh xạ `model_reviewer_identity`"','return None'),
 'assurance_or_to_and':('(trong_phien or khong_neo)','(trong_phien and khong_neo)'),
 'drop_assurance_check':('if (trong_phien or khong_neo) and khai in ASSURANCE_CAN_DOC_LAP:','if False:'),
}
for label in [*mutations,'refreeze_debt_hash']:
 with tempfile.TemporaryDirectory(prefix='r2-mutant-') as td:
  root=Path(td); shutil.copytree(R/'ops',root/'ops')
  (root/'.git').write_text('gitdir: '+str(R/'.git')+'\n')
  s=source
  if label=='refreeze_debt_hash':
   n,b=next(iter(m.NO_DA_DO.items()));p=root/m.THU_MUC/n
   p.write_bytes(p.read_bytes()+b'\n# review measurement\n')
   s=s.replace(b,hashlib.sha256(p.read_bytes()).hexdigest())
  else:
   a,b=mutations[label];assert s.count(a)==1,(label,s.count(a));s=s.replace(a,b)
  (root/'ops/bien_nhan_v2.py').write_text(s)
  q=subprocess.run([sys.executable,str(root/'ops/bien_nhan_v2_test.py')],cwd=root,capture_output=True,text=True)
  print('MUTANT',label,'rc',q.returncode,'SUMMARY',q.stdout.splitlines()[-2:])
  print('FAILURES',[l for l in q.stdout.splitlines() if l.startswith('  ĐỎ') or l.startswith('  KHÔNG ĐO')])
# Static/byte facts on exact tree.
for n in [1,2]:
 p=R/f'ops/reviews/phan-bien-quy-trinh-review-{n}-claude-verdict.receipt.yaml'
 d=yaml.safe_load(p.read_text());q=subprocess.run(['git','show','663da644d6edae52e5542e592614073d11f4e0f4:'+d['verdict_path']],capture_output=True)
 print('HISTORICAL',n,'git_rc',q.returncode,'same_bytes',q.stdout==(R/d['verdict_path']).read_bytes(),'assurance',d['assurance'])
p=R/'ops/reviews/pr455-bien-nhan-v2-review-1-codex-verdict.receipt.yaml';d=yaml.safe_load(p.read_text())
print('R1_RECEIPT', 'exempt',p.name in m.ALLOWLIST_CUTOVER,'debt',p.name in m.NO_DA_DO,'schema_errors',m._thieu(d),'git',m._neo_git(R,p.name,d),'local_hash',m._bam(R/d['verdict_path'])==d['verdict_sha256'])
print('MEASUREMENTS_COMPLETE')
```

### Script B

```python
import ast, importlib.util, re
from pathlib import Path
p=Path('ops/bien_nhan_v2_test.py');s=importlib.util.spec_from_file_location('probe',p);t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
for n in ast.walk(ast.parse(p.read_text())):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='do' and isinstance(n.args[0],ast.Constant) and n.args[0].value.startswith(('m7_','m9_')):
  patterns=[x for x in ast.walk(n.args[1]) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='compile']
  pat=ast.literal_eval(patterns[0].args[0]);old=t.bnv2._BLOB_URL;t.bnv2._BLOB_URL=re.compile(pat)
  print(n.args[0].value,'matches_valid',bool(t.bnv2._BLOB_URL.search(t.v2_du()['evidence_url'])))
  for name in ['c18_neo_git_DUNG_thi_qua','c19_neo_git_SAI_DUONG_DAN_thi_DO','c22_canonical_ancestry_ma_URL_khong_ghim_thi_DO']:
   print(name,t._chay_1(getattr(t,name)))
  t.bnv2._BLOB_URL=old
print('MUTATOR_MEASUREMENT_COMPLETE')
```

## TÔI ĐÃ ĐO ĐƯỢC GÌ / KHÔNG ĐO ĐƯỢC GÌ

Môi trường: Linux container, Python 3.11.15, Git 2.43.0, PyYAML khả dụng, full clone; `core.abbrev=7` có sẵn, không sửa Git config. Mọi tiến trình Python chạy với `PYTHONDONTWRITEBYTECODE=1`. Mã thoát lấy từ kết quả tiến trình hoặc `subprocess.returncode`, không suy từ dòng tổng kết.

| Command/phép đo | rc thật | Trạng thái và bằng chứng dương |
|---|---:|---|
| `python3 ops/bien_nhan_v2_test.py` | 0 | **passed theo suite**: 23/23, 12/12; tầng Git đối chiếu 11 tên. Giới hạn ý nghĩa mutant ở R2-04. |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | **passed trên dữ liệu hiện tại**: 10 đạt, 11/11 miễn trừ, 42 nợ, 0 vi phạm, 0 chưa đo, tổng 63; `TỔNG: ĐẠT`. |
| `python3 ops/lease_publish_test.py` | 0 | **passed**: 121/121, đã chạy 121, bỏ qua 0. Warning clone empty thuộc fixture, không phải test skipped. |
| `python3 .claude/dev/packet_loop_test.py` | 0 | **passed**: 278/278, bỏ qua 0, 81 đột biến, 78 lớp lách, 35 ca bắt-oan, 0 ngoại lệ AC18, `TỔNG: ĐẠT`. |
| `python3 ops/cong_cu_test.py` | 0 | **passed**: 23/23, bỏ qua 0; 7 tự kiểm phân hạng, đối chứng crash qua subprocess, 18 đột biến, lỗi đột biến 0. |
| `python3 .claude/dev/cong_cu_test.py` | 2 | **failed invocation**: tôi dùng nhầm đường dẫn, tệp không tồn tại. Đã tìm bằng `rg --files` và chạy đúng `ops/cong_cu_test.py` ở dòng trên; không tính lần gọi nhầm là test sản phẩm thất bại. |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | **passed**: `ok=true`, checked=expected=180, failed/extra/missing/errors rỗng, package hash khớp `613eec52c5a072d31e8f881f78c96142a5be7f386c495654dddd11fbae89735e`. Có doc-pointer advisory, không khai mọi con trỏ đều sạch. |
| `python3 /tmp/pr455_r2_measure.py` (A) | 0 | **phép đo hoàn tất**, marker `MEASUREMENTS_COMPLETE`; đối chứng rc=0; 5 ca lỗi CLI đều rc=0; 3 mutant sống rc=0; 2 mutant bị bắt rc=1 đúng c4d/c13. Kết quả này tái hiện lỗi, không phải xác nhận 5 ca CLI an toàn. |
| `python3 /tmp/pr455_r2_mutator_check.py` (B) | 0 | **phép đo hoàn tất**, marker `MUTATOR_MEASUREMENT_COMPLETE`; hai mutant cùng giết c18/c19 nhưng để c22 qua, và không match URL hợp lệ. |
| Receipt review vòng 1 tự qua | trong A, rc=0 | Không thuộc allowlist/nợ; `_thieu=[]`, `_neo_git=([],[])`, digest verdict cục bộ khớp. |
| Hai verdict lịch sử vòng 1–2 | Git subprocess rc=0, 2/2 | Byte-identical với base, metadata `review_deferred` 2/2. |
| `git diff --check 663da644d6edae52e5542e592614073d11f4e0f4 HEAD` | 0 | Không có lỗi whitespace trong diff được review. |

**skipped:** không có ca bị bỏ qua trong ba suite có bộ đếm skip nêu trên. Không dùng việc các suite đạt để suy full repository gate đạt.

**not_run:** full legacy selftest, golden/determinism, release-bundle, Windows parity, LIVE, remote CI/check readback và kiểm ref protection. Không có yêu cầu land/deploy trong nhiệm vụ này; báo cáo không xác nhận required gate đầy đủ hay đủ điều kiện merge. Đã có finding trực tiếp trên bản vá; không cần chạy thêm release gate để quyết định yêu cầu sửa.

**KHÔNG ĐO ĐƯỢC:** remote PR head hiện thời, provenance thật của model/session lịch sử từ launcher artifacts bên ngoài clone, canonical ancestry/ref protection/check object trên GitHub. Việc receipt vòng 1 qua cổng chỉ chứng minh cấu trúc và những phép Git cục bộ đã nêu. Không tạo `cross_approved`, approval hoặc land authorization bằng báo cáo này.

Chỉ `VERDICT.md` được tạo trong clone. Head/tree giữ nguyên exact OID ở đầu báo cáo. Đây là review vòng 2 được giao; không tự mở vòng 3 hay nâng budget. Cần sửa R2-01 trước khi cân nhắc thông qua; các P2 vẫn là nợ cụ thể phải được xử lý/ghi nhận bằng authority phù hợp.

verdict: changes_requested
