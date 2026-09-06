# Cross-review vòng 3 — PR #455

**Không phát hiện P0/P1 mới trong phạm vi đã đo. Approve with findings: còn 2 P2 về phép đo và độ phủ.** Lỗi production R2-01 đã được vá thật trên các phản chứng cũ; không nâng lỗi test thành P1 để kéo dài vòng review. Tuy nhiên, tuyên bố “16/16 có răng” vẫn mạnh hơn bằng chứng mà runner tạo ra.

- `reviewed_sha`: `cb212847375c2319fe0ccad3f7c00c90b870e3ba`
- `reviewed_tree`: `7272596dc056c0550077ad6af308f7816f978616`
- Base bản vá: `c595292cb63fb8c09d7d7b482cda20f9d5f0917f`; diff 7 tệp.
- Vai trò: Reviewer độc lập với context Executor Claude; axes `spec`, `standards_security`; class `sensitive` vì đây là cổng receipt/evidence.
- Provider `openai_codex`; execution surface Codex service/API với shell trong Linux container; transport `machine`. Chỉ thị phiên định danh GPT-6; không có chứng thực độc lập backend/model version. Không tự nhận là ChatGPT Web hay một Codex CLI run đã được launcher chứng thực.
- Authority: user trực tiếp chỉ tới `prompt.snapshot` giao **vòng 3**, exact head và write set duy nhất `VERDICT.md`. SHA-256 chỉ thị: `24e1f261d991a41c119bb2dcbcb87ae73e866f27b497b8bb7ec239dee6ec447a`. Không có Packet revision/spec hash/generation/lease riêng được cung cấp; không tự tạo chúng. Chỉ thị trực tiếp này cho phép làm vòng 3 đang giao, không tự mở vòng 4 hoặc tăng budget điều phối.

Preflight: origin `https://github.com/ducthangho/tra-luat`, detached HEAD đúng SHA, `--is-shallow-repository=false`, 1.723 commit, worktree ban đầu sạch, `core.abbrev=7` có sẵn. Đã đọc hai verdict trước, bản vá và các điều khoản liên quan của CONTEXT/protocol/CLAUDE/kế hoạch đa provider. Không đổi Git config. Phản chứng dùng fixture/script có sẵn và đột biến mã trên bản sao tạm ngoài clone; không soạn nội dung tấn công mới, không sửa mã sản phẩm, không commit/push.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding vòng 2 | Phân loại và bằng chứng tự đo |
|---|---|
| R2-01 — chưa đo vẫn xanh/dispatch đi vòng | **ĐÃ VÁ THẬT** trong các đường đã báo. Replay fixture cũ: đối chứng rc=0; SHA vắng rc=2; protected ref và check object mỗi loại rc=2; canonical có whitespace + URL PR rc=1. Các ca chưa đo không còn `TỔNG: ĐẠT`. Bỏ nhánh tổng hợp `chua_do` trên bản sao làm c21 đỏ đúng vì child trả 0 thay vì 2. |
| R2-02 — băm byte chuẩn hóa | **ĐÃ VÁ THẬT** với fixture LF đã báo. Byte gốc rc=0; digest của `.strip()` rc=1, `RAW_HASH_DIFFERS=True`. Đột biến quay về băm text đã strip làm suite đỏ (21/25, 14/16). Chưa đo CRLF/Windows. |
| R2-03 — ma trận bỏ nhánh | **ĐÃ VÁ THẬT ba phản chứng cụ thể, CHƯA VÁ hết lớp.** Bỏ actor hoặc nhánh MRI không-phải-dict đều rc=1, c17 đỏ. Đổi điều kiện mới `or` thành `and` làm c4e/c4f đỏ, 23/25. Các nhánh Git mới còn lọt: R3-02. |
| R2-04 — đột biến đo sai thuộc tính | **VÁ HỜ ở cơ chế đối chứng.** m7 mới nhắm đúng phép tra path, nhưng runner khôi phục module trước khi chạy đối chứng; đưa nguyên m7 hỏng của vòng 2 trở lại vẫn 25/25, 16/16, rc=0. m9 còn dùng một đối chứng không đọc `chua_do`. Xem R3-01. |

Regression vòng 1 vẫn giữ: tái đóng băng băm nợ bị c13 bắt (24/25, rc=1); hai receipt lịch sử `phan-bien-quy-trinh-review-{1,2}` vẫn `review_deferred`, verdict nguyên byte so với `663da644d6edae52e5542e592614073d11f4e0f4`. Gỡ toàn bộ chốt assurance làm c4d/e/f đỏ (22/25, rc=1).

## R3-01 — P2: đối chứng chạy sau khôi phục; m13 đổi oracle thay vì đổi child

**Vá ở đâu:** `ops/bien_nhan_v2_test.py:724–750` (`_dot_bien.do`), helper `_kiem:190`, c18 và m9/m13 tại khoảng dòng 802–823. Đây là vấn đề giàn đo, không phải bằng chứng CLI hiện tại trả 0 khi còn `chua_do`.

**Bằng chứng đã chạy:**

1. Trace hai lần runner gọi c18 làm đối chứng: cả hai có `_git` và `_doc_loai` **đã trở về hàm gốc**. `finally` khôi phục tại dòng 738–740; đối chứng gọi sau đó tại 747.
2. Trích nguyên lambda m7 từ AST của test tại base vòng 2, thay riêng lambda m7 trên bản sao hiện tại. Kết quả **rc=0, 25/25, 16/16** và m7 vẫn được cấp “CÓ RĂNG”. Chạy c18 thật sự khi lambda hỏng ấy còn hiệu lực: **`giet_that`**, mỏ neo hợp lệ bị từ chối vì URL. Chính lỗi cần đối chứng ngăn đã đi qua bản vá.
3. Chỉ chuyển vị trí restore vẫn chưa đủ: dưới m9 hiện tại (`_doc_loai` luôn đọc thành protected ref), c18 vẫn `qua`; đọc toàn bộ `kiem` lại cho `loi=[]` nhưng **một mục `chua_do`**. `_kiem` vứt thống kê đi nên “đối chứng xanh” không có nghĩa phép xác minh còn thành công. Chỉ **2/16** lời gọi `do` khai `doi_chung`, không phải mỗi đột biến như prose tuyên bố.
4. Với m13, spy lời gọi subprocess ghi **child rc=2**, trong khi hằng kỳ vọng ở parent bị đổi thành **0**. c21 chết với thông báo `CLI phải trả rc=0 ... được 2`. Đột biến không truyền sang chương trình child: nó đo oracle sai, không đo CLI bị làm yếu. Đối chứng reviewer sửa thật nhánh `main` trên bản sao thì c21 bắt đúng child rc=0, nên **test c21 có giá trị**, chỉ tín dụng của m13 đang sai nghĩa.

**Vá thế nào:** cho target và control chạy trong cùng phạm vi đột biến, chỉ restore sau cả hai, kể cả khi lỗi. Control cho verifier phải đòi cả `loi` và `chua_do` rỗng, hoặc kiểm CLI rc=0 kèm marker dương. Đừng đổi helper dùng chung một cách mù quáng vì các ca schema cố ý không có Git thật. Với m13, chạy CLI từ module/file đã đột biến trên bản sao và giữ oracle 0/1/2 độc lập. Chọn mutant thực sự nới predicate và xác nhận child đã chạy nó. Thu hẹp lời khai CHANGELOG cho tới khi chứng minh được từng thuộc tính.

**Ca test khóa:** script B dưới tái hiện nguyên m7 hỏng: sau vá runner phải từ chối cấp răng do control đỏ, còn m7 bỏ kiểm path đúng phải giữ control sạch cả hai danh sách. Một ca riêng phải bác c18 “qua nhưng chưa đo” dưới m9. m13 mới phải đo được child rc=0 trên mutant và rc=2 trên control, rồi chính assertion nghiệp vụ giết mutant; không chấp nhận chỉ thay expected return code ở parent.

**Bản vá có thể đẻ ra gì:** restore quá muộn hoặc thiếu `finally` làm bẩn các ca sau; sửa `_kiem` toàn cục sẽ bắt oan fixture chỉ kiểm schema; mutant m9 hiện tại không còn giữ control sạch khi control thật sự đọc ba trạng thái, nên phải sửa ý nghĩa mutant cùng lúc. Đừng chữa bằng cách xóa control hay tự hạ chuẩn “xanh”.

## R3-02 — P2: ba nhánh mỏ neo mới có thể bị gỡ mà toàn suite vẫn xanh

**Vá ở đâu:** ca Git trong `ops/bien_nhan_v2_test.py`, nhằm khóa `_neo_git` ở `ops/bien_nhan_v2.py:415`, `:450`, `:455`. Ma trận tên/schema không thay được ca hành vi Git.

**Bằng chứng:** script A giữ nguyên suite, mỗi lần sửa đúng một predicate trên một bản sao mới:

| Neo nguyên văn → thay | Kết quả thật |
|---|---|
| `if loai in ("protected_evidence_ref", "check_object"):` → `if False:` | rc=0, **25/25 · 16/16** |
| `if rc_tt == 1:` → `if False:` | rc=0, **25/25 · 16/16** |
| `if rc_tt not in (0, 1):` → `if False:` | rc=0, **25/25 · 16/16** |

Đột biến đầu xóa chính đường ghi chưa đo cho hai loại anchor mà R2-01 yêu cầu vá. Hai đột biến sau bỏ từ chối non-ancestor và bỏ báo chưa đo khi phép hỏi ancestry lỗi. Đây là các đột biến làm yếu thật, không phải sửa oracle. **Không kết luận mã hiện tại đã thiếu các chốt này**; chúng có mặt và đường protected/check đã được replay xác nhận đúng. P2 là độ phủ hồi quy, không nâng thành P1 chỉ vì chốt liên quan evidence.

Đối chứng về chất lượng phép đo: gỡ provider allowlist, surface hoặc run/reason của `_mri` đều bị c17 bắt; bỏ tổng hợp CLI bị c21 bắt. Đổi cả hai phép đọc loại về thô giữ 25/25 ca nhưng làm m9 mất răng (15/16, rc=1): đó là phát hiện do tương tác mutant, chưa phải ca trực tiếp khóa whitespace. Không coi mọi đột biến sống/chết có cùng ý nghĩa.

**Vá thế nào:** thêm ca âm độc lập cho từng loại anchor chưa có verifier; giữ đủ trạng thái đến CLI. Dùng Git fixture thật để phân biệt ancestor và một commit có object/blob đúng nhưng không phải ancestor; thêm fault injection ở riêng phép `merge-base` cho rc ngoài 0/1. Có đối chứng thành công đi cùng, độc lập với bảng predicate sản phẩm. Không cần dựng verifier GitHub mới để khóa ba nhánh này.

**Ca test khóa:** ba cặp neo/thay ở bảng phải lần lượt làm ca protected/check trả 0 oan, ca non-ancestor trả 0 oan, ca lỗi ancestry mất rc=2 bị bắt; lỗi giàn giáo không được tính kill. Thêm cặp canonical có/không whitespace trên cùng Git fixture để chứng minh dispatch nhất quán. Những ca bổ sung này là đề xuất cho Executor; tôi đã chạy các đột biến và replay hiện có, chưa khai đã chạy toàn bộ ca mới.

**Bản vá có thể đẻ ra gì:** fixture “non-ancestor” vô tình chọn object không tồn tại sẽ đo nhánh thiếu object; mock Git quá rộng sẽ phá mọi phép hỏi và tái tạo R3-01. Phân biệt clone thiếu lịch sử với vi phạm; không biến `chua_do` thành cáo buộc giả mạo. Đây là hình dạng thiếu ca nhánh đã lặp: nên kiểm toán bảng nhánh và giàn đo một lần có phạm vi, không tiếp tục thêm một mutant theo từng finding rồi coi tổng đếm là bảo đảm.

## Bằng chứng tái lập

Script A/B bên dưới đã chạy từ root exact clone bằng `PYTHONDONTWRITEBYTECODE=1 python3 <script-ngoai-kho>`, rc=0 và marker hoàn tất. Chỉ bản sao trong `/tmp` được sửa; `.git` của bản sao chỉ trỏ về object database gốc cho truy vấn đọc. Đây là dữ liệu phản chứng, không phải patch sản phẩm. Các file log tại `/tmp/pr455-r3-evidence` là tiện ích phiên này; mã được nhúng để báo cáo không phụ thuộc việc giữ thư mục tạm.

### A — ma trận đột biến và trace control

```python
import os, sys, tempfile, shutil, subprocess, importlib.util, copy, json
from pathlib import Path
R=Path.cwd(); E={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
def mod(p):
 s=importlib.util.spec_from_file_location('probe_module',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
t=mod(R/'ops/bien_nhan_v2_test.py');m=t.bnv2
source=(R/'ops/bien_nhan_v2.py').read_text()
mutations={
 'no_unmeasured_anchor_dispatch':('if loai in ("protected_evidence_ref", "check_object"):','if False:'),
 'raw_anchor_dispatch':('loai = _doc_loai(a)','loai = str(a.get("loai") or "")'),
 'no_ancestor_rejection':('if rc_tt == 1:','if False:'),
 'no_ancestor_unknown':('if rc_tt not in (0, 1):','if False:'),
 'normalized_blob_hash':('hashlib.sha256(pb.stdout).hexdigest()','hashlib.sha256(pb.stdout.decode().strip().encode()).hexdigest()'),
 'no_mri_provider_allowlist':('if prov not in PROVIDER_CHO_PHEP:','if False:'),
 'no_mri_surface':('if not str(v.get("surface") or "").strip():','if False:'),
 'no_mri_run_or_reason':('if not str(v.get("session_run_id") or "").strip() and not str(v.get("KHONG_do_duoc") or "").strip():','if False:'),
 'remove_unknown_cli_branch':('if tk.get("chua_do"):', 'if False:'),
}
for name,(a,b) in mutations.items():
 with tempfile.TemporaryDirectory(prefix='pr455-r3-mut-') as td:
  r=Path(td);shutil.copytree(R/'ops',r/'ops');(r/'.git').write_text('gitdir: '+str(R/'.git')+'\n')
  assert source.count(a)==(2 if name=='raw_anchor_dispatch' else 1),(name,source.count(a))
  (r/'ops/bien_nhan_v2.py').write_text(source.replace(a,b))
  p=subprocess.run([sys.executable,str(r/'ops/bien_nhan_v2_test.py')],cwd=r,env=E,capture_output=True,text=True)
  Path('/tmp/pr455-r3-evidence/'+name+'.log').write_text(p.stdout+p.stderr)
  print('MUTANT',name,'rc',p.returncode,p.stdout.splitlines()[-2:],'failures',[x for x in p.stdout.splitlines() if x.startswith('  ĐỎ')],flush=True)
# Trace what the built-in runner actually uses for controls and child exit expectations.
old=t._chay_1
original_git=m._git; original_kind=m._doc_loai
trace=[]
def wrapped(fn):
 if fn.__name__.startswith('c18'):
  trace.append({'case':fn.__name__,'git_restored':m._git is original_git,'kind_restored':m._doc_loai is original_kind})
 return old(fn)
t._chay_1=wrapped
rows=t._dot_bien();print('CONTROL_TRACE',trace)
t._chay_1=old
m._doc_loai=lambda a:'protected_evidence_ref'
print('ACTUAL_M9_CONTROL',t._chay_1(t.c18_neo_git_DUNG_thi_qua))
m._doc_loai=original_kind
# Same existing c18 fixture, collect full three-state result under m9.
with tempfile.TemporaryDirectory(prefix='pr455-r3-control-') as td:
 r=Path(td);sha,bam,path=t._kho_git(r,'noi dung verdict\n');d=t._bn_neo(sha,bam,path)
 t._cay(r,{'a-verdict.receipt.yaml':d})
 m._doc_loai=lambda a:'protected_evidence_ref'
 print('M9_CONTROL_FULL_RESULT',m.kiem(r,allowlist={},no_da_do={}))
 m._doc_loai=original_kind
for n in [1,2]:
 import yaml
 p=R/f'ops/reviews/pr455-bien-nhan-v2-review-{n}-codex-verdict.receipt.yaml';d=yaml.safe_load(p.read_text())
 print('RECEIPT',n,'exempt',p.name in m.ALLOWLIST_CUTOVER,'debt',p.name in m.NO_DA_DO,'schema',m._thieu(d),'git',m._neo_git(R,p.name,d),'hash_match',m._bam(R/d['verdict_path'])==d['verdict_sha256'])
print('PROBE_COMPLETE',flush=True)
```

### B — tái đưa m7 hỏng và đo child của m13

```python
import ast, os, sys, tempfile, shutil, subprocess, importlib.util
from pathlib import Path
R=Path.cwd();E={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
def mod(p):
 s=importlib.util.spec_from_file_location('probe_runner',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
t=mod(R/'ops/bien_nhan_v2_test.py')
old=subprocess.run(['git','show','c595292cb63fb8c09d7d7b482cda20f9d5f0917f:ops/bien_nhan_v2_test.py'],capture_output=True,text=True);assert old.returncode==0
for node in ast.walk(ast.parse(old.stdout)):
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='do' and isinstance(node.args[0],ast.Constant) and node.args[0].value.startswith('m7_'):
  old_mutator=ast.get_source_segment(old.stdout,node.args[1]);break
with tempfile.TemporaryDirectory(prefix='pr455-r3-runner-') as td:
 r=Path(td);shutil.copytree(R/'ops',r/'ops');(r/'.git').write_text('gitdir: '+str(R/'.git')+'\n')
 p=r/'ops/bien_nhan_v2_test.py';s=p.read_text();a='lambda: setattr(bnv2, "_git", _git_bo_kiem_duong_dan)';assert s.count(a)==1;p.write_text(s.replace(a,old_mutator))
 q=subprocess.run([sys.executable,str(p)],env=E,cwd=r,capture_output=True,text=True)
 print('RESTORE_BROKEN_R2_M7','rc',q.returncode,q.stdout.splitlines()[-2:]);print([x for x in q.stdout.splitlines() if 'm7_' in x]);print('EXACT_MUTATOR',old_mutator)
 Path('/tmp/pr455-r3-evidence/broken_m7.log').write_text(q.stdout+q.stderr)
 eval(old_mutator,{'bnv2':t.bnv2})()
 print('ACTUAL_BROKEN_M7_C18',t._chay_1(t.c18_neo_git_DUNG_thi_qua))
t=mod(R/'ops/bien_nhan_v2_test.py');orig=t.subprocess.run;calls=[]
def spy(*args,**kw):
 q=orig(*args,**kw)
 if 'bien_nhan_v2.py' in str(args[0]):calls.append({'rc':q.returncode,'expected_in_parent':t.bnv2.RC_KHONG_DO_DUOC})
 return q
t.subprocess.run=spy
t.bnv2.RC_KHONG_DO_DUOC=t.bnv2.RC_SACH
print('M13_CASE',t._chay_1(t.c21_object_khong_tra_duoc_la_KHONG_DO_DUOC_chu_khong_phai_DO));print('M13_CHILD_TRACE',calls)
t.subprocess.run=orig
print('RUNNER_PROBE_COMPLETE')
```

## TÔI ĐÃ ĐO ĐƯỢC GÌ / KHÔNG ĐO ĐƯỢC GÌ

Môi trường: Linux container, Python 3.11.15, Git 2.43.0, PyYAML khả dụng, full clone, `core.abbrev=7`. Python dùng `PYTHONDONTWRITEBYTECODE=1`; mã thoát lấy từ kết quả tiến trình/subprocess, không suy từ stdout. Số đo dưới đây neo exact head/tree ở đầu báo cáo.

| Command/phép đo | rc thật | Trạng thái và bằng chứng dương |
|---|---:|---|
| `python3 ops/bien_nhan_v2_test.py` | 0 | **passed theo suite**: 25/25 ca, 16/16 tín dụng mutant; Git cutover khớp 11 tên. Ý nghĩa tín dụng bị giới hạn bởi R3-01. |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | **passed**: 11 đạt, 11/11 miễn trừ có băm khớp, 42 nợ, 0 vi phạm, 0 chưa đo, tổng 64, `TỔNG: ĐẠT`. |
| `python3 ops/lease_publish_test.py` | 0 | **passed**: 121/121, đã chạy 121, bỏ qua 0. Warning clone empty thuộc fixture. |
| `python3 .claude/dev/packet_loop_test.py` | 0 | **passed**: 278/278, bỏ qua 0, 81 đột biến, 78 lớp lách, 35 ca bắt-oan, 0 ngoại lệ AC18, `TỔNG: ĐẠT`. |
| `python3 ops/cong_cu_test.py` | 0 | **passed**: 23/23, bỏ qua 0, 7 tự kiểm phân hạng, đối chứng qua subprocess, 18 đột biến, lỗi đột biến 0. |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | **passed**: `ok=true`, checked=expected=180, failed/extra/missing/errors rỗng; package hash `f21be9bb83b58d7d127e5c87127328914400caa6204f994bc3a29c839e08abb2` khớp. Có doc-pointer advisory; không gọi mọi pointer là sạch. |
| `python3 /tmp/pr455-r3-evidence/replay_r2.py` | 1 | **failed giàn đo do neo cũ stale**: các phép CLI và hai mutant đầu đã chạy; dừng ở assertion `assurance_or_to_and` không còn neo trong source. Không tính đây là test sản phẩm thất bại hay replay hoàn tất. |
| `python3 /tmp/pr455-r3-evidence/replay_r2_adapted.py` | 0 | **replay hoàn tất**, `MEASUREMENTS_COMPLETE`. Trích nguyên script A từ verdict vòng 2, chỉ thay hai neo assurance sang tên/điều kiện hiện tại. Control rc=0; SHA vắng/protected/check rc=2; whitespace URL PR/digest strip rc=1; 5 mutant cũ đều bị bắt. |
| `python3 /tmp/pr455-r3-evidence/probe.py` (A) | 0 | **phép đo hoàn tất**, `PROBE_COMPLETE`: 9 mutant sản phẩm, 3 sống và 6 bị bắt; trace control khôi phục 2/2; m9 có chưa đo nhưng c18 vẫn qua; receipt 2/2 khớp. Không đọc việc script hoàn tất thành “mutant đã bị diệt hết”. |
| `python3 /tmp/pr455-r3-evidence/runner_probe.py` (B) | 0 | **phép đo hoàn tất**, `RUNNER_PROBE_COMPLETE`: m7 hỏng cũ vẫn nhận răng; control dưới nó thực sự đỏ; m13 child rc=2/parent expected=0. |
| Hai receipt PR455 vòng 1–2 | trong A, rc=0 | Cả hai không thuộc allowlist/nợ; `_thieu=[]`, `_neo_git=([],[])`; băm verdict cục bộ khớp. Git verifier đọc commit, ancestry tới HEAD của clone và blob/hash. |
| `git diff --check c595292cb63fb8c09d7d7b482cda20f9d5f0917f HEAD` | 0 | **passed**: không lỗi whitespace trong diff. |

**skipped:** không có ca bị bỏ qua trong ba suite có bộ đếm skip nêu trên. Không suy các suite này thành full repository gate.

**not_run:** full legacy selftest, workflow-audit/golden/determinism, release-bundle, Windows/CRLF parity, remote CI readback, LIVE, merge/deploy. Đây là review bản vá được giao, không phải xác nhận đủ điều kiện land. Những nhánh lỗi I/O, Git timeout, YAML scalar/types và nhánh identity chưa được ma trận đột biến này bao trọn không được coi là đã phủ chỉ vì suite xanh.

**KHÔNG ĐO ĐƯỢC:** remote PR head hiện thời, provenance thật của model/session lịch sử từ launcher artifacts ngoài clone, bảo vệ ref/canonical authority/check object trên GitHub. Quan hệ tới HEAD local không chứng minh HEAD ấy là canonical được bảo vệ. Hai receipt tự qua chỉ chứng minh các kiểm cấu trúc/Git/hash đã nêu, không chứng minh danh tính hay quyền người đăng. Không tạo `cross_approved`, approval GitHub hoặc land authorization bằng báo cáo này.

Hai P2 cần được ghi nhận/xử lý đúng authority; tôi không tự mở thêm lượt review. Chỉ `VERDICT.md` được tạo trong clone; head/tree vẫn nguyên exact OID. Chọn `approve_with_findings` theo tập verdict mà prompt vòng này cho phép vì P1 cũ đã đóng trong tập phản chứng và chưa có P1 mới được chứng minh.

verdict: approve_with_findings
