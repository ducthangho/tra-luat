# Cross-review vòng 4 — PR #455

**`approve_with_findings`: hai P2, một P3; không có P1 mới được chứng minh.** Hai phản chứng cụ thể R3-01/R3-02 đã được vá thật. Lớp thiếu khóa hồi quy vẫn còn; không đọc kết luận này thành đủ điều kiện land.

- `reviewed_sha`: `4ef73e69d5f3c419634118983723355e25e38305`
- `reviewed_tree`: `79a6e88301c83ad4e59f9308d47d4a46f706b4ae`
- Diff đã review: `cb212847375c2319fe0ccad3f7c00c90b870e3ba..4ef73e69d5f3c419634118983723355e25e38305`, 7 tệp.
- Vai trò: Reviewer độc lập với context Executor Claude; hai trục `spec`, `standards_security`; review class `sensitive` vì cổng evidence/identity.
- Provider `openai_codex`; execution surface **Codex service/API với shell trong Linux container**; transport `machine`. Chỉ thị định danh agent GPT-6; không có chứng thực độc lập backend/model version. Không tự khai là ChatGPT Web hoặc Codex CLI được launcher chứng thực.
- Authority/phạm vi: yêu cầu trực tiếp của user cho vòng 4, exact head/base và write set duy nhất `VERDICT.md`. Không được cung cấp Packet revision/spec hash/generation/lease riêng; không tự tạo chúng, không xác nhận state điều phối. Yêu cầu này cho phép vòng đang giao, không tự cấp vòng tiếp theo hoặc quyền land.

Preflight **đã đo**: origin `https://github.com/ducthangho/tra-luat`; detached HEAD (`git symbolic-ref -q HEAD` không có ref); `git rev-parse --is-shallow-repository=false`; `git rev-list --count HEAD=1727`; worktree ban đầu sạch. Đã đọc ba verdict trước, CONTEXT, protocol, CLAUDE và kế hoạch đa provider trước khi kiểm bản vá. Không gọi mạng/GitHub. Không sửa mã nguồn trong clone, không commit/push; chỉ dùng fixture/phản chứng có sẵn và đột biến mã trên bản sao `/tmp`.

## R3-01 và R3-02 đã đóng đến đâu

| Chốt | Bằng chứng độc lập |
|---|---|
| Đối chứng chạy dưới đột biến | Trích nguyên lambda m7 hỏng từ AST tại `c595292cb63fb8c09d7d7b482cda20f9d5f0917f`, đưa vào bản sao test hiện tại: rc=1, 31/31 ca nền, 20/21 tín dụng; **m7 KHÔNG RĂNG vì c18 dương bị từ chối**. Không còn được cấp tín dụng như R3. |
| `_sach_hoan_toan` đọc trạng thái thứ ba | Dùng nguyên m9 cũ (`_doc_loai` luôn trả protected ref): c18 vẫn `qua`, nhưng `_sach_hoan_toan(c18)` trả **False** với `loi=[]` và một `chua_do`. Nó có phân biệt được đúng lỗi đã báo. |
| m13 đi tới child | Trace subprocess: chạy `/tmp/bnv2-dotbien-…/ops/bien_nhan_v2.py`; **child rc=1**, hằng unknown của parent vẫn **2**; c23 đòi số 2 độc lập và bắt đúng việc mất ưu tiên trạng thái hỗn hợp. Đối chứng c23 trên nguồn gốc qua. m13 hiện đo ưu tiên hỗn hợp, không còn là mutant gỡ toàn bộ nhánh unknown cũ. |
| Ba nhánh R3-02 | Lặp đúng ba phép gỡ: c24, c25, c26 lần lượt đỏ vì mất `chua_do`, mất từ chối non-ancestor, mất trạng thái lỗi merge-base. Mỗi lần 30/31 ca nền, rc=1. Các mutant nội bộ còn báo neo stale vì nguồn đã bị gỡ; **bằng chứng kill được tính là assertion của ca nền**, không lấy lỗi giàn giáo ấy làm bằng chứng. |
| Cây gương/khôi phục | Chưa tìm được lệch môi trường mới làm sai tín dụng của sáu mutant mức tệp hiện có. Chạy hai lượt với bytecode **bật** trên bản sao: 12 đường tệp khác nhau, tất cả được dọn; mỗi lượt 21/21 tín dụng, module/CONG phục hồi, danh sách tạm rỗng, không có `bnv2_db_*` trong `sys.modules`. |
| Ngoại lệ và thứ tự | Bơm `LoiDungCa` ngay sau khi nạp mutant: 20/21, báo lỗi đo; bơm `RuntimeError`: truyền ngoại lệ ra ngoài nhưng `finally` vẫn phục hồi module/CONG và dọn tệp. Sau mỗi lỗi, chạy lại 21/21. Hai lượt runner rồi chạy ngược danh sách ca: 31/31 `qua`. Không tái hiện rò trong các đường này. |

Phạm vi của `_sach_hoan_toan` vẫn hẹp: nó chạy ca được truyền rồi dựng **một fixture canonical riêng**, không thu kết quả của mọi fixture bên trong ca đó. Hiện cả bảy lời gọi đối chứng đều dùng c18, cùng dạng fixture, nên chưa có bằng chứng cơ chế này xanh sai cho các đối chứng hiện hành. Không gọi nó là verifier tổng quát hoặc đã đo mọi đường CLI. Tương tự, parity bốn hằng chỉ so bản sao với module đang kiểm; nó không chứng minh các hằng của chính module đúng theo hợp đồng.

## R4-01 — P2: còn tám phép làm yếu mà toàn suite vẫn xanh

**Vá ở đâu:** `ops/bien_nhan_v2_test.py`, nhất là c14/c17/c4g và các ca Git; nhằm khóa `ops/bien_nhan_v2.py` tại `_mri`, `_provider_chinh_tac`/`PROVIDER_CHO_PHEP`, `_neo_git`, `main`. Đây là **một hình dạng lỗi thiếu ca nhánh**, không phải tám P1.

**Bằng chứng:** giữ nguyên toàn bộ suite trên từng bản sao độc lập, chỉ đổi một đoạn mã sản phẩm. Tất cả tám trường hợp dưới đều **rc=0 · 31/31 · 21/21 · `TỔNG: ĐẠT`**, không lỗi giàn giáo:

| ID phép đo | Phép làm yếu |
|---|---|
| `cli_violation_returns_clean` | `return RC_VI_PHAM` → `return RC_SACH` |
| `mri_rid_str_coercion` | Phục hồi ép `str(rid)` thay vì đòi run ID là chuỗi ở `_mri` |
| `provider_back_to_handcopy` | Phục hồi nguyên tập provider chép tay cũ, bỏ đọc `_TRANSPORT_CONTRACTS` |
| `head_failure_drop_unknown` | Gỡ ghi `chua` khi không tra được HEAD |
| `anchor_object_drop_unknown` | Gỡ ghi `chua` khi commit của evidence URL không tra được |
| `blob_error_drop_unknown` | Gỡ ghi `chua` khi tiến trình đọc blob trả lỗi |
| `blob_exception_drop_unknown` | Gỡ ghi `chua` khi đọc blob ném OSError/SubprocessError |
| `reviewed_git_unavailable_drop_unknown` | Gỡ ghi `chua` riêng nhánh Git rc=127 khi tra reviewed SHA |

Đối chứng hành vi cho mutant CLI: dùng **đúng phép bỏ `receipt_id` có sẵn trong c23**, nhưng chỉ giữ receipt vi phạm ấy. Nguồn gốc trả **1**; mutant trả **0**, stderr vẫn `TỔNG: ĐỎ`, không có marker dương trên stdout. Như vậy mutant thực sự làm hỏng mã thoát, không phải phép thay tương đương; suite vẫn không thấy. c14 mang tên “ba trạng thái” nhưng chỉ chạy CLI sạch và thiếu thư mục; c23 chỉ khóa kết quả hỗn hợp, bỏ lọt nhánh **chỉ có vi phạm**.

Hai điểm ngay trong bản vá cũng lọt: c4g còn được chốt kiểu ở `_thieu` bảo vệ nên không khóa riêng chốt kiểu vừa thêm ở `_mri`; và parity cây gương vẫn xanh khi cả bản thật lẫn bản sao cùng dùng danh sách provider sai đã chép tay. Sự có mặt của kiểm tra trong nguồn không có nghĩa đã khóa hồi quy.

**Vá thế nào:** bổ sung bảng ca theo **kết quả của từng thao tác**, dùng fixture Git và cơ chế bơm lỗi hẹp đã có ở c26. Đo CLI riêng ba trạng thái đơn và kết quả hỗn hợp, với số 0/1/2 độc lập cùng nội dung dương/âm tương ứng. Khóa hợp đồng provider bằng đối chứng chấp nhận từng provider chính tắc, so nguồn AST độc lập; khóa `_mri` riêng khỏi chốt assurance, dùng lại giá trị sai kiểu có sẵn ở c4g. Không sinh kỳ vọng từ hằng/predicate đang đột biến.

**Ca test khóa:** tám cặp neo/thay nguyên văn trong script A dưới phải chết ở ca hành vi đích. Đặc biệt mutant CLI phải bị ca “chỉ vi phạm” bắt do rc=0; phục hồi provider cũ phải làm đối chứng `anthropic_claude` đỏ; từng lỗi Git chỉ bơm vào đúng thao tác, đối chứng commit/blob bình thường vẫn sạch. Script A hiện ghi nhận trạng thái trước sửa, không phải assertion rằng tám mutant đã chết.

**Bản vá có thể đẻ ra gì:** mock Git quá rộng sẽ giết fixture trước khi tới nhánh cần đo; oracle lấy từ module lại co theo mutant; trộn lỗi schema vào ca `_mri` sẽ để chốt khác che lỗ; đếm lỗi neo đột biến như kill sẽ tái tạo tín dụng giả. Cùng hình dạng đã lặp nhiều vòng: nên kiểm toán bảng nhánh trong phạm vi này một lần và ghi nợ phần chưa đo, không mở một vòng riêng cho mỗi dòng bảng. **Không kết luận mã sản phẩm hiện tại đã bỏ tám chốt này.**

## R4-02 — P2: nguồn provider không đọc được bị đổi thành kết luận receipt vi phạm

**Vá ở đâu:** `ops/bien_nhan_v2.py:103`, `_provider_chinh_tac`, hằng tại dòng 127 và đường đưa lỗi này tới `kiem/main`. Đây là phụ thuộc mới do bản vá thêm.

**Bằng chứng chạy được:** script B giữ nguyên mã sản phẩm và fixture Git hợp lệ của c18. Bản sao có `launcher.py`: **rc=0, 1 đạt, 0 vi phạm, 0 chưa đo**. Bản sao thiếu riêng tệp nguồn đó: **rc=1, 1 vi phạm, 0 chưa đo**; thông báo kết tội `openai_codex` ngoài allowlist `['anthropic', 'human']`, “chuỗi tự do không phải attestation”. Không có thông báo thiếu nguồn hợp đồng. `_provider_chinh_tac` nuốt ngoại lệ rồi trả tập rỗng; câu “đọc không được … KHAI ra, không im lặng” ở docstring không được thực hiện.

Đây là **lỗi phân loại khi phụ thuộc không khả dụng**, không phải bypass trên full clone hiện tại: ở clone này nguồn có thật và cổng đọc đúng. Mức P2 vì không chứng minh được đường cấp approval sai; lỗi đo bị báo thành lỗi receipt và có thể dẫn đến sửa nhầm dữ liệu hợp lệ.

**Vá thế nào:** giữ nguyên nguồn chính tắc duy nhất, nhưng giữ cả trạng thái/lý do thất bại khi đọc hoặc không tìm được hợp đồng; đưa nó tới trạng thái **KHÔNG ĐO ĐƯỢC** của CLI. Không lặng lẽ coi hai bí danh lịch sử là toàn bộ tập chính tắc; không chữa bằng danh sách dự phòng chép tay mới. Có thể trì hoãn việc phát lỗi tới `main/kiem` để import vẫn dùng được trong test.

**Ca test khóa:** fixture c18 với cây nguồn đầy đủ vẫn rc=0; thiếu `launcher.py` phải rc=2 và chỉ rõ nguồn không đọc được, không kết luận provider hợp lệ là “chuỗi tự do”. Khóa thêm trường hợp không tìm được assignment và lỗi parse bằng đột biến nguồn trên bản sao. Đột biến nuốt trạng thái lỗi/biến nó trở lại allowlist hai bí danh phải chết. Trong vòng này đã chạy trường hợp **thiếu tệp**; hai trường hợp còn lại là đề xuất, chưa đo.

**Bản vá có thể đẻ ra gì:** ném ngoại lệ ngay lúc import có thể làm suite crash trước bộ phân ba trạng thái; miễn kiểm provider khi nguồn mất sẽ fail-open; bỏ bí danh lịch sử có thể bắt oan receipt cũ. Lỗi môi trường phải được phân biệt với một provider thực sự ngoài danh sách khi nguồn đã đo được.

## R4-03 — P3: tổng tín dụng và số đối chứng vẫn dùng hai mẫu số khác nhau

**Vá ở đâu:** `ops/bien_nhan_v2_test.py:1150` (tổng kết), chú thích cụm mutant và CHANGELOG phần “Răng”/“6/21”.

**Bằng chứng:** AST có **21** lời gọi `do`, **7** khai `doi_chung`, trong đó **1** (`m14`) là tự kiểm với `mong_khong_rang=True`. Stdout thực tế có **20** dòng `CÓ RĂNG` và **1** `TỰ KIỂM ok`, rồi tổng lại gọi tất cả **21/21 đột biến CÓ RĂNG**. “6/21 khai đối chứng” không đúng theo nghĩa đếm lời gọi; đúng là **6/20 mutant thường có đối chứng**, cộng **1/1 tự kiểm có đối chứng**. Việc loại m14 khỏi tử nhưng giữ trong mẫu gây lệch ngay ở đoạn vừa sửa lời khai rộng.

**Vá thế nào:** tách tổng mutant thường và tự kiểm; ghi 20/20 mutant bị bắt, 1/1 tự kiểm đạt, 6/20 mutant thường có đối chứng (hoặc 7/21 lời gọi có đối chứng với giải thích). Không đổi ý nghĩa tự kiểm để khớp prose.

**Ca test khóa:** đối chiếu AST/rows/stdout như phép đếm trong script C. Đột biến gộp `mong_khong_rang=True` trở lại số “CÓ RĂNG” phải làm kiểm tra tổng kết đỏ; m14 vẫn phải bị từ chối cấp tín dụng thông thường.

**Bản vá có thể đẻ ra gì:** chỉ đổi số chép tay tạo drift mới; bỏ m14 khỏi runner làm mất ca tự kiểm. Đây là lỗi báo cáo P3, không phủ nhận 20 mutant thường hiện đã bị bắt.

## TÔI ĐÃ ĐO ĐƯỢC GÌ / KHÔNG ĐO ĐƯỢC GÌ

Môi trường: Linux container, Python **3.11.15**, Git **2.43.0**, PyYAML có sẵn, `core.abbrev=7` có sẵn; không sửa Git config. Python chạy trên clone dùng `PYTHONDONTWRITEBYTECODE=1`; phép thử bật bytecode chỉ chạy trên bản sao tạm. Mã thoát lấy từ công cụ tiến trình/subprocess, không suy từ stdout.

| Command/phép đo | rc thật | Trạng thái và bằng chứng dương |
|---|---:|---|
| `python3 ops/bien_nhan_v2_test.py` | 0 | **passed theo suite**: 31/31, stdout tổng 21/21; phân rã thực tế 20 mutant + 1 tự kiểm như R4-03. Bản sao baseline trong A cũng rc=0. |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | **passed**: 12 đạt v2 · 11/11 miễn trừ băm khớp · 42 nợ · 0 vi phạm · 0 chưa đo · tổng 65; `TỔNG: ĐẠT`. |
| `python3 ops/lease_publish_test.py` | 0 | **passed**: 121/121; đã chạy 121, bỏ qua 0. Warning empty repository thuộc fixture. |
| `python3 .claude/dev/packet_loop_test.py` | 0 | **passed**: 278/278, bỏ qua 0; 81 mutant, 78 lớp lách, 35 ca bắt-oan, 0 ngoại lệ AC18; `TỔNG: ĐẠT`. |
| `python3 ops/cong_cu_test.py` | 0 | **passed**: 23/23, bỏ qua 0; 18 mutant, lỗi mutant 0. |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | **passed**: `ok=true`, checked=expected=180, `failed`, `extra_files`, `missing_from_current_manifest`, `required_missing`, `errors` rỗng; package hash khớp `cb6d8f2d0dfb5e6ce44c02bbd08a9005597d26b1a95220b8d10a891245dd6e2c`. Có doc-pointer advisory. |
| `git diff --check cb212847375c2319fe0ccad3f7c00c90b870e3ba HEAD` | 0 | **passed**, không lỗi whitespace. Manifest delta chỉ đổi mục CHANGELOG và tổng byte/hash; file_count giữ 180. |
| Script A — `probe.py` | 0 | **phép đo hoàn tất**, `MATRIX_COMPLETE`: 3 phép gỡ R3 bị ca nền bắt; 8 mutant mới sống; m7 hỏng cũ bị bác; baseline qua. Tám mutant sống là **failed về khóa hồi quy**, không phải tám test an toàn passed. |
| Script B — `witness.py` | 0 | **phép đo hoàn tất**, `WITNESS_COMPLETE`: CLI vi phạm gốc rc=1/mutant rc=0; fixture hợp lệ gốc rc=0/thiếu nguồn provider rc=1. |
| Script C — `rig.py` | 0 | **phép đo hoàn tất**, `RIG_COMPLETE`: trace child m13, đối chứng cũ, lặp runner/đảo ca, đếm AST, receipt/hash/provider. |
| Script D — `cleanup.py` | 0 | **phép đo hoàn tất**, `CLEANUP_COMPLETE`: bytecode bật, 12/12 đường riêng được dọn; hai ngoại lệ được bơm, phục hồi rồi chạy lại xanh. Không gọi lỗi được bơm là lỗi sản phẩm tự phát. |

**Biên nhận R3 tự qua:** không thuộc allowlist/nợ; `_thieu=[]`, `_neo_git=([],[])`. `git show 0c46443a12e0cb3c8114c16e861df69d3841579e:ops/reviews/pr455-bien-nhan-v2-review-3-codex-verdict.md` rc=0; byte khớp tệp verdict hiện tại, SHA-256 **`9f3c781842913fbffedd9198d88a1e2be2a6eb80a905f293223659a19a7a398c`**. `git merge-base --is-ancestor 0c46443a12e0cb3c8114c16e861df69d3841579e HEAD` rc=0. Đây là ancestry tới HEAD **local**, không chứng minh canonical authority/ref protection trên GitHub.

**Provider:** AST `_TRANSPORT_CONTRACTS` hiện trả `anthropic_claude`, `openai_api`, `openai_codex`; `PROVIDER_CHO_PHEP` thực tế thêm hai bí danh `anthropic`, `human`. Lời khai “đọc từ launcher, không chép tay” đúng với phần chính tắc hiện tại; không đồng nghĩa regression đã được khóa, hoặc fallback đã khai đủ.

**skipped:** không ca bị bỏ qua trong ba suite có bộ đếm skip trên. **not_run:** full legacy selftest, workflow-audit/golden/determinism, release-bundle, Windows/CRLF parity, remote CI readback, LIVE/merge/deploy; không chạy lại nguyên mọi script vòng 1–2, chỉ trích/lặp những phản chứng đã mô tả. Chưa bao trọn mọi nhánh kiểu YAML/I/O, tín hiệu giết tiến trình, lỗi dọn thư mục hay mọi dạng lệch cây gương. Không suy các phép chạy lặp hữu hạn thành chứng minh không thể rò.

**KHÔNG ĐO ĐƯỢC:** trạng thái GitHub trực tiếp — head PR hiện thời, CI/required checks, protection, delivery trên remote, authority điều phối; model/session provenance thật của các receipt lịch sử từ artifact ngoài clone. Không gọi shell trong container này là chứng thực launcher của bất kỳ lượt nào. Báo cáo không tự tạo `cross_approved`, approval GitHub hoặc land authorization.

Chỉ tạo `VERDICT.md` trong clone. HEAD/tree được đọc lại và giữ nguyên OID ở đầu báo cáo. Không tự mở thêm lượt review; hai P2 và một P3 được giao lại để người điều phối quyết định xử lý/nợ theo authority.

## Phụ lục — mã đo đã chạy

Các script dưới là dữ liệu đo, không phải bản vá sản phẩm. Lưu ngoài clone, chạy từ root exact clone; tạo trước `/tmp/pr455-r4-evidence`. A/B/C dùng `PYTHONDONTWRITEBYTECODE=1 python3 <script>`; D dùng `python3 <script>` để đo bytecode mặc định trên bản sao tạm. Các log là tiện ích phiên này; mã nhúng giữ phép đo tái lập được khi thư mục tạm mất.

### A — probe.py

```python
import os,sys,subprocess,tempfile,shutil,importlib.util,ast,json,hashlib
from pathlib import Path
R=Path.cwd(); E=Path('/tmp/pr455-r4-evidence'); env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
sys.dont_write_bytecode=True
S=(R/'ops/bien_nhan_v2.py').read_text()
def mod(p):
 s=importlib.util.spec_from_file_location('probe',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def mirror(r):
 shutil.copytree(R/'ops',r/'ops',ignore=shutil.ignore_patterns('__pycache__'))
 (r/'.claude/dev').mkdir(parents=True); shutil.copyfile(R/'.claude/dev/launcher.py',r/'.claude/dev/launcher.py')
 (r/'.git').write_text('gitdir: '+str(R/'.git')+'\n')
def suite(label,code,testcode=None):
 with tempfile.TemporaryDirectory(prefix='r4-mut-') as td:
  r=Path(td);mirror(r);(r/'ops/bien_nhan_v2.py').write_text(code)
  if testcode is not None:(r/'ops/bien_nhan_v2_test.py').write_text(testcode)
  q=subprocess.run([sys.executable,str(r/'ops/bien_nhan_v2_test.py')],cwd=r,env=env,capture_output=True,text=True)
  (E/(label+'.log')).write_text(q.stdout+q.stderr)
  out={'name':label,'rc':q.returncode,'summary':q.stdout.splitlines()[-2:],'failures':[l for l in q.stdout.splitlines() if l.startswith(('  ĐỎ','  KHÔNG ĐO','  KHÔNG RĂNG'))]}
  print(json.dumps(out,ensure_ascii=False),flush=True)
mut={
 'r3_dispatch':('if loai in ("protected_evidence_ref", "check_object"):','if False:'),
 'r3_ancestry':('if rc_tt == 1:','if False:'),
 'r3_merge_error':('if rc_tt not in (0, 1):','if False:'),
 'cli_violation_returns_clean':('return RC_VI_PHAM','return RC_SACH'),
 'mri_rid_str_coercion':('if not (isinstance(rid, str) and rid.strip()) and','if not str(rid or "").strip() and'),
 'provider_back_to_handcopy':('frozenset(_provider_chinh_tac()) | PROVIDER_LICH_SU','frozenset({"anthropic", "openai_codex", "openai_api", "google_antigravity", "human"})'),
 'head_failure_drop_unknown':('chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC tổ tiên — cây không có HEAD để so")','pass'),
 'anchor_object_drop_unknown':('chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC commit `{commit[:12]}…` trong `evidence_url`")','pass'),
 'blob_error_drop_unknown':('chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC nội dung blob {oid[:12]}… (git rc={pb.returncode})")','pass'),
 'blob_exception_drop_unknown':('chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC nội dung blob {oid[:12]}… ({type(ex).__name__})")','pass'),
 'reviewed_git_unavailable_drop_unknown':('chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC `reviewed_sha` — không gọi được git")','pass'),
}
for label,(a,b) in mut.items():
 assert S.count(a)==1,(label,S.count(a));suite(label,S.replace(a,b))
# Replay original broken m7 directly from the old test AST.
old=subprocess.run(['git','show','c595292cb63fb8c09d7d7b482cda20f9d5f0917f:ops/bien_nhan_v2_test.py'],capture_output=True,text=True,check=True).stdout
node=next(n for n in ast.walk(ast.parse(old)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='do' and n.args and isinstance(n.args[0],ast.Constant) and str(n.args[0].value).startswith('m7_'))
a='lambda: setattr(bnv2, "_git", _git_bo_kiem_duong_dan)'; ts=(R/'ops/bien_nhan_v2_test.py').read_text();assert ts.count(a)==1
suite('r2_broken_m7',S,ts.replace(a,ast.get_source_segment(old,node.args[1])))
suite('baseline',S)
print('MATRIX_COMPLETE',flush=True)
```

### B — witness.py

```python
import importlib.util,sys,subprocess,tempfile,shutil,os,json,copy
from pathlib import Path
R=Path.cwd();sys.dont_write_bytecode=True;env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
s=importlib.util.spec_from_file_location('witness',R/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
S=(R/'ops/bien_nhan_v2.py').read_text()
with tempfile.TemporaryDirectory(prefix='r4-witness-') as td:
 root=Path(td); fixture=root/'fixture';fixture.mkdir();sha,bam,path=t._kho_git(fixture,'noi dung verdict\n');d=t._bn_neo(sha,bam,path);t._ghi_bn(fixture,d)
 def writecopy(name,code,launcher=True):
  r=root/name;(r/'ops').mkdir(parents=True);p=r/'ops/bien_nhan_v2.py';p.write_text(code)
  if launcher:
   (r/'.claude/dev').mkdir(parents=True);shutil.copyfile(R/'.claude/dev/launcher.py',r/'.claude/dev/launcher.py')
  return p
 clean=writecopy('clean',S);bad=writecopy('return0',S.replace('return RC_VI_PHAM','return RC_SACH'));missing=writecopy('missing_launcher',S,False)
 def cli(label,p):
  q=subprocess.run([sys.executable,str(p),'--root',str(fixture)],capture_output=True,text=True,env=env)
  print(label,json.dumps({'rc':q.returncode,'stdout':q.stdout,'stderr':q.stderr},ensure_ascii=False))
 cli('BASE_VALID',clean);cli('MISSING_PROVIDER_SOURCE',missing)
 # EXACT existing c23 invalid fixture transformation.
 x=copy.deepcopy(d);x.pop('receipt_id');t._ghi_bn(fixture,x)
 cli('BASE_VIOLATION',clean);cli('MUTANT_VIOLATION',bad)
print('WITNESS_COMPLETE')
```

### C — rig.py

```python
import importlib.util,sys,os,subprocess,tempfile,shutil,ast,hashlib,json,contextlib,io
from pathlib import Path
R=Path.cwd(); E=Path('/tmp/pr455-r4-evidence');sys.dont_write_bytecode=True
s=importlib.util.spec_from_file_location('rig_probe',R/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
orig=t.bnv2;cong=t.CONG;before=set(sys.modules); saved=t._sach_hoan_toan;trace=[];run=t.subprocess.run;children=[]
def control(fn):
 result=saved(fn);trace.append({'module_changed':t.bnv2 is not orig,'git_changed':t.bnv2._git is not orig._git,'file':str(t.CONG),'result':result});return result
def spy(*a,**kw):
 q=run(*a,**kw)
 if 'bien_nhan_v2.py' in str(a[0]):children.append({'file':str(a[0][1]),'rc':q.returncode,'parent_unknown':t.bnv2.RC_KHONG_DO_DUOC,'stderr':q.stderr[-120:]})
 return q
t._sach_hoan_toan=control;t.subprocess.run=spy
with contextlib.redirect_stdout(io.StringIO()) as out:rows=t._dot_bien()
t.subprocess.run=run;t._sach_hoan_toan=saved
print('RUN',len(rows),sum(x[2] for x in rows));print('CONTROL_TRACE',json.dumps(trace,ensure_ascii=False));print('CHILD_TRACE',json.dumps(children,ensure_ascii=False))
print('RESTORED',t.bnv2 is orig,t.CONG==cong,'temps',t._TAM_DOT_BIEN,'module_leaks',[k for k in set(sys.modules)-before if k.startswith('bnv2')], 'removed',all(not Path(x['file']).exists() for x in trace if x['module_changed']))
with contextlib.redirect_stdout(io.StringIO()):rows2=t._dot_bien()
print('REPEAT',len(rows2),sum(x[2] for x in rows2));print('REVERSE_CASES',[(f.__name__,t._chay_1(f)[0]) for f in reversed(t.CA)])
# The old m9 is already present verbatim in R3; apply it and check strict control.
saved_kind=t.bnv2._doc_loai
t.bnv2._doc_loai=lambda a:'protected_evidence_ref'
print('OLD_M9_CONTROL',t._chay_1(t.c18_neo_git_DUNG_thi_qua),saved(t.c18_neo_git_DUNG_thi_qua))
t.bnv2._doc_loai=saved_kind
# Actual receipt and source facts, freshly imported.
s=importlib.util.spec_from_file_location('receipt_probe',R/'ops/bien_nhan_v2.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
import yaml
p=R/'ops/reviews/pr455-bien-nhan-v2-review-3-codex-verdict.receipt.yaml';d=yaml.safe_load(p.read_text());sha,path=d['evidence_url'].split('/blob/')[1].split('/',1)
b=run(['git','show',sha+':'+path],capture_output=True);a=run(['git','merge-base','--is-ancestor',sha,'HEAD'])
print('RECEIPT',json.dumps({'schema':m._thieu(d),'git':m._neo_git(R,p.name,d),'exempt':p.name in m.ALLOWLIST_CUTOVER,'debt':p.name in m.NO_DA_DO,'blob_rc':b.returncode,'ancestry_rc':a.returncode,'sha256':hashlib.sha256(b.stdout).hexdigest(),'local_match':b.stdout==(R/d['verdict_path']).read_bytes()},ensure_ascii=False))
nodes=[n for n in ast.walk(ast.parse((R/'ops/bien_nhan_v2_test.py').read_text())) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='do']
print('COUNT',len(nodes),'controls',sum(any(k.arg=='doi_chung' for k in n.keywords) for n in nodes),'selfchecks',sum(any(k.arg=='mong_khong_rang' for k in n.keywords) for n in nodes));print('PROVIDERS',sorted(m._provider_chinh_tac()),sorted(m.PROVIDER_CHO_PHEP))
print('RIG_COMPLETE')
```

### D — cleanup.py

```python
import importlib.util,sys,tempfile,shutil,contextlib,io,os
from pathlib import Path
R=Path.cwd()
with tempfile.TemporaryDirectory(prefix='r4-bytecode-') as td:
 r=Path(td);shutil.copytree(R/'ops',r/'ops',ignore=shutil.ignore_patterns('__pycache__'));(r/'.claude/dev').mkdir(parents=True);shutil.copyfile(R/'.claude/dev/launcher.py',r/'.claude/dev/launcher.py');(r/'.git').write_text('gitdir: '+str(R/'.git')+'\n')
 s=importlib.util.spec_from_file_location('cleanup_probe',r/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
 original=t.bnv2;cong=t.CONG;fn=t._dot_bien_tep;created=[]
 # Default bytecode writing is enabled, in this TEMP copy only.
 print('BYTECODE_ENABLED',not sys.dont_write_bytecode)
 def track(*args):
  fn(*args);created.append(Path(t.CONG)); print('',end='')
 t._dot_bien_tep=track
 for i in range(2):
  with contextlib.redirect_stdout(io.StringIO()):rows=t._dot_bien()
  print('CACHED_RUN',i,len(rows),sum(x[2] for x in rows),t.bnv2 is original,t.CONG==cong,len(t._TAM_DOT_BIEN))
 print('UNIQUE_FILES',len(created),len(set(created)),'ALL_REMOVED',all(not p.exists() for p in created))
 for error in (t.LoiDungCa, RuntimeError):
  fired=[]
  def broken(*args):
   fn(*args)
   if not fired:
    fired.append(Path(t.CONG));raise error('fault injection')
  t._dot_bien_tep=broken
  try:
   with contextlib.redirect_stdout(io.StringIO()):rows=t._dot_bien()
   status='returned '+str(sum(x[2] for x in rows))+'/'+str(len(rows))
  except RuntimeError:status='RuntimeError propagated'
  print('AFTER_ERROR',error.__name__,status,'restored',t.bnv2 is original,t.CONG==cong,'temps',t._TAM_DOT_BIEN,'removed',all(not p.exists() for p in fired))
  t._dot_bien_tep=fn
  with contextlib.redirect_stdout(io.StringIO()):rows=t._dot_bien()
  print('RECOVERY_RUN',len(rows),sum(x[2] for x in rows))
 print('MODULE_REGISTRY',[k for k in sys.modules if k.startswith('bnv2_db_')])
print('CLEANUP_COMPLETE')
```

verdict: approve_with_findings
