verdict: changes_requested
reviewed_sha: 8d5cccbb13b0b2c5ba1c9bbc4f8af410a19f87b8
reviewed_tree: 817f593f0d53e4e2e9546783d3b29216ac163692
base_sha: e63961f27b53e66db8e6600009f97d5706743063
Kết quả: 0 P0, 0 P1, 1 P2, 0 P3.

Phạm vi: chỉ đọc/đo `cay-kho/`; không mạng, không push, không sửa cây reviewed. Các script và evidence đều ở thư mục cha. Provider `openai_codex`, model family `openai`; phiên Codex có shell cục bộ, không đi qua `codex exec` hay Desktop nên theo phân loại của kho là `execution_surface: codex_service`, `transport: machine`. Không có runtime receipt để machine-verify model/effort/session identity; không tự cấp assurance/approval land. Authority cho review và artifact là chỉ thị trực tiếp trong `runs/9f946d71/prompt.snapshot`.

## BẢNG ĐO

Các lệnh `python3 -B ../audit_review.py <hướng>` dưới đây chạy được từ **gốc `cay-kho/`**. Script chỉ đọc nguồn/YAML, trích AST hoặc dùng Git cục bộ; kết quả chi tiết nằm ở BẢNG SĂN và `evidence/`. `Khớp cấu hình` không có nghĩa là đã chạy Windows/GitHub Actions.

| khẳng định | PR khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Mốc đo mới, dòng 164/180–181 | 23-10-2026, `e63961f` | `history`: SHA đầy đủ `e63961f27b53e66db8e6600009f97d5706743063`, commit ngày 23-10; blob workflow và cong_cu_test tại base = reviewed SHA; `expression` tái đo biểu thức thật | Khớp đối tượng và tái đo; không chứng nhận phiên đo lịch sử của tác giả |
| Truy nguồn thay đổi runner, dòng 164 | #878 thêm nhánh thứ ba | `history`: `5585abe8499e920e2a6ae8236e70c4096f95e71d` thêm input/nhánh đứng đầu; ancestor rc=0; merge #880 tại `747f983` | Có; #878 là packet/issue, không phải số PR merge |
| Push master (đối chứng) | Ngoài dispatch/nhãn Windows vẫn Ubuntu | `expression`: evaluator AST nguyên hàm trên YAML thật → push master `["ubuntu-latest"]` | Có |
| Dispatch `windows-only`, dòng 164–165 | `["windows-latest"]` | `expression`: `workflow_dispatch` + input chính xác → `["windows-latest"]` | Có |
| Phạm vi “KHÔNG có Ubuntu”, dòng 165 | Mảng os không có Ubuntu | `expression` + `census`: output không có Ubuntu; `chuan-bi` vẫn `runs-on: ubuntu-latest` cố định | Có trong phạm vi output `os`, không phải toàn bộ run không có Ubuntu |
| Mặc định của input, dòng 165 | `windows-and-ubuntu` | `expression`: `on.workflow_dispatch.inputs.runner_set.default = windows-and-ubuntu` | Có |
| Dispatch mặc định/vắng input, dòng 165 | Hai nền | `expression`: cả input mặc định và input vắng → `["ubuntu-latest", "windows-latest"]` | Có |
| PR có/không nhãn (đối chứng) | Nhãn `windows` chọn hai nền khi có run | `expression`: PR thường → Ubuntu; PR có nhãn → Ubuntu + Windows; input windows-only không lọt sang push | Có; không suy nhãn tự tạo run |
| Truy nguồn Windows subset, dòng 180 | Từ #879 | `history`: `be00ef723eca3fae90932e476d683f233588f2b3` và diff/chú thích đúng thay đổi; ancestor rc=0, merge #883 là `e63961f` | Có; #879 là packet/issue |
| Gate Windows chỉ là một phần, dòng 180 | Không phải hai bản gate tương đương | `windows`, `merger`, `census`, `steps`: mất 7 mảnh Windows, mất gom Windows, 5/6 điều kiện OS false ở Windows trong chế độ đầy đủ | Khớp cấu hình |
| `gate-cong-cu` Windows, dòng 181 | Chỉ mảnh 0 | `windows`: matrix manh 0..7, exclude Windows 1..7; mở ma trận → đúng `{os: windows-latest, manh: 0}` | Có |
| Chế độ thực của bước G5, dòng 181–182 | Ca nền rồi dừng ở Windows | `windows`: env thật của mảnh 0 → `_doc_che_do = ('manh', (0,8,...))`; `_TEN_NEN='nt'`; main thật duyệt danh sách ca trước nhánh return; spy không có lời gọi đột biến/ghi mảnh | Có ở luồng điều khiển; đây là giả lập nt, không phải Windows thật |
| “Chạy đủ ca nền”, dòng 182 | Có thể hiểu mọi ca nền đều được đo | `windows`: main thật chấp nhận `BoQuaMoiTruong`; ca thật t51 với Path giả thiếu /bin/sh → skipped; main vẫn rc=0 với 2 đạt/3 tổng, 1 bỏ qua | Thiếu điều kiện: duyệt mọi ca không chứng minh đo đủ; cùng finding P2 bên dưới |
| Bán kính `cong_cu_test.py`, dòng 182 | Chỉ đo trên Ubuntu trong CI này | `windows` + `provenance`: nhánh nt/manh return trước vòng đột biến; job gate dùng chế độ `gate`, không `du`; chỉ các mảnh Ubuntu còn đường bán kính và gom | Khớp cấu hình; chưa đo mutant trên runner Ubuntu thật. Không áp câu này cho mọi bộ tự đột biến khác |
| `gate-cong-cu-gop`, dòng 182–183 | Loại `windows-latest` | `merger`: exclude đúng `{os: windows-latest}`; hai nền mở ra chỉ một hàng Ubuntu | Có |
| Điều kiện gom, dòng 183 | Đòi `ubuntu-latest` trong output `os` | `merger`: job.if nguyên văn có `!cancelled()` và `contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest')` | Có; có cả điều kiện không canceled |
| `windows-only` → `skipped`, dòng 183 | Job gom skipped | `merger`: điều kiện job false; nếu ép mở matrix thì rỗng. `jobs.<job_id>.if` được xét trước `strategy.matrix` theo ngữ nghĩa Actions, nên dự kiến skip trước expansion | Đúng theo suy luận cấu hình; KHÔNG ĐO ĐƯỢC trạng thái GitHub thực/scheduler trong sandbox. Không kết luận skip chỉ từ exclude |
| Mọi `gate*` còn lại, dòng 183–184 | Vẫn có Windows ở mức JOB | `census`: liệt kê đủ 9 job, 8 gate*, mọi matrix/exclude/job.if; trừ gom cong-cu, mọi gate* còn hàng Windows | Có ở cấu trúc job; không bảo đảm dependency thành công/runner được cấp khi run lỗi hoặc hủy |
| Số bước, dòng 184–185 | 6 bước `ci.yml` có if theo runner.os | `steps`: 6 node YAML: dòng if 430, 575, 697, 786, 819, 860; có đếm cả 2 `${{ }}` | Có, chính xác 6 |
| Tắt/thay riêng trên Windows, dòng 185 | 6 điều kiện OS khiến coverage khác | `steps`: 5 điều kiện false trên Windows; bước lifecycle non-Linux true khi day_du; cgroup Linux false; không có step.if theo matrix.os, không kiểu runner/matrix bracket khác bị bỏ sót | Có |
| Đường bỏ qua khác (đối chứng) | Có job không có nghĩa mọi bước chạy | `steps`: 25 shell bash, 1 pwsh, 71 mặc định; continue-on-error chỉ 2 bước chuan-bi phân loại PR, không riêng Windows; RUNNER_OS chỉ nhãn evidence, matrix.os còn dùng tên artifact | Không có cơ chế Windows-only khác ở cấp step bị câu bỏ sót; shell chọn trình chạy, không tự skip |
| Một run xanh → ca nền đạt, dòng 185 | `windows-only` xanh chứng minh ca nền đạt trên Windows | `windows`: main thật + ca t51 thật bị bỏ qua vẫn rc=0; `dat_windows` chỉ đòi số ca còn lại >0, đỏ=0, bảng đột biến >0 | P2: chỉ chứng minh các ca không bị bỏ qua; phải giữ/đọc danh sách ca chưa đo |
| Run Windows xanh không chứng minh bán kính, dòng 186 | Cần evidence Ubuntu | `windows` + `provenance`: nhánh Windows manh không gọi vòng đột biến, không ghi mảnh; Windows không có gom cong-cu | Có trong phạm vi bán kính cong_cu |
| Ubuntu của CÙNG head, dòng 186 | Không tái dùng từ head khác | `provenance` + `contradictions`: phù hợp protocol 10.2.2; workflow checkout không ghim ref PR head, chú thích phân biệt synthetic merge và dispatch | Đúng yêu cầu. Chưa có cặp run để đo; phải so checkout SHA/tree/workflow/runtime, không chỉ run head |
| Tính nhất quán phần (c) cũ | Câu hai nền ở `9e9a74b` có bị bỏ quên? | `contradictions`: tái chạy evaluator trên YAML `9e9a74b`: dispatch hai nền; câu cũ ghi rõ ngày/SHA, câu mới cập nhật ngay sau | Không phải lỗi: lịch sử có neo, không phải lời khai hiện hành vô điều kiện |
| Các chỗ khác của CLAUDE.md | Có câu “gọi tay ⇒ hai nền” vô điều kiện khác? | `contradictions`: quét toàn tệp các cụm workflow_dispatch/gọi tay/hai nền; output đầy đủ các hit | Không có câu KHÁC như vậy |
| API riêng nền / lane cloud / ADR / protocol | Có mâu thuẫn mới? | `contradictions`: API là bài học lịch sử, launcher có labeled; lane cloud nói rõ ca bỏ qua khác nền; ADR-0049 giữ cổng deploy; protocol tách skipped/passed | Không có mâu thuẫn cấu hình khác. Lời “ca nền đạt” cần sửa theo cùng finding P2 |

“Skips trước ma trận” ở đây là diễn giải ngữ nghĩa job.if, không phải kết quả thực thi GitHub. Môi trường không có mạng, không có bản triển khai scheduler hoặc readback run mới ở exact reviewed_sha; không lấy chú thích #879 làm bằng chứng scheduler. Vì vậy không báo lỗi ma trận rỗng và cũng không khai đã quan sát job skipped thật.

## BẢNG SĂN

Biên bản được tạo ngay với `verdict: dang_lam`, nối sau mỗi hướng thử; phần dưới gom các kết quả mới nhất của cùng hướng (hướng 2 được bổ sung phản chứng với ca t51 thật). Mọi output là output thật hoặc các trường trích nguyên giá trị từ output JSON, không phải kết quả giả định. Dữ liệu giả lập được ghi rõ.

HƯỚNG 0: Neo đối tượng và ranh giới chỉ đọc

  giả thuyết : HEAD đúng reviewed_sha; diff thật chỉ có 9 dòng tài liệu.
  lệnh       : chạy trong `cay-kho/`:

```text
$ git rev-parse HEAD
8d5cccbb13b0b2c5ba1c9bbc4f8af410a19f87b8
rc=0
$ git rev-parse HEAD^{tree}
817f593f0d53e4e2e9546783d3b29216ac163692
rc=0
$ git rev-parse e63961f
e63961f27b53e66db8e6600009f97d5706743063
rc=0
$ git diff --numstat e63961f HEAD
9	0	CLAUDE.md
rc=0
$ git status --porcelain=v1
(stdout rỗng)
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI. Authority là prompt.snapshot của người dùng; reviewer read-only, chỉ ghi artifact ngoài cay-kho. Provider OpenAI; model GPT-6 (không có định danh biến thể được cung cấp); execution surface Codex agent có shell cục bộ; transport local tools. Không gọi mạng, không suy identity từ GitHub submitter.

HƯỚNG 1: Ba nhánh outputs.os và mặc định runner_set

  giả thuyết : Đối chiếu trực tiếp khẳng định trong 9 dòng mới với cấu hình và mã tại reviewed_sha.
  lệnh       : từ cay-kho/: `python3 -B ../audit_review.py expression`
  output     :

```text
AST exact ops/lease_publish_test.py:7848-7923 _danh_gia_bieu_thuc_chuan_bi
REAL outputs.os = ${{ (github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only') && '["windows-latest"]' || (github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'windows')) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]' }}
runner_set.default = windows-and-ubuntu
push master => ["ubuntu-latest"]
dispatch windows-only => ["windows-latest"]
dispatch default => ["ubuntu-latest", "windows-latest"]
dispatch missing inputs => ["ubuntu-latest", "windows-latest"]
PR without label => ["ubuntu-latest"]
PR windows label => ["ubuntu-latest", "windows-latest"]
push with irrelevant windows-only input => ["ubuntu-latest"]
e63961f workflow-identical-to-checkout = True
HEAD workflow-identical-to-checkout = True
probe_rc=0
```

  kết luận   : KHÔNG PHẢI LỖI: ma trận đo khớp; windows-only không bao gồm các job ma trận Ubuntu, không loại job chuan-bi Ubuntu cố định.

HƯỚNG 2: Mảnh Windows, vị từ và luồng ca nền

  giả thuyết : Đối chiếu trực tiếp khẳng định trong 9 dòng mới với cấu hình và mã tại reviewed_sha.
  lệnh       : từ cay-kho/: `python3 -B ../audit_review.py windows`
  output     :

```text
matrix = {"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}", "manh": [0, 1, 2, 3, 4, 5, 6, 7], "exclude": [{"os": "windows-latest", "manh": 1}, {"os": "windows-latest", "manh": 2}, {"os": "windows-latest", "manh": 3}, {"os": "windows-latest", "manh": 4}, {"os": "windows-latest", "manh": 5}, {"os": "windows-latest", "manh": 6}, {"os": "windows-latest", "manh": 7}]}
expanded ['windows-latest'] => [{'os': 'windows-latest', 'manh': 0}]
expanded ['ubuntu-latest', 'windows-latest'] => [{'os': 'ubuntu-latest', 'manh': 0}, {'os': 'ubuntu-latest', 'manh': 1}, {'os': 'ubuntu-latest', 'manh': 2}, {'os': 'ubuntu-latest', 'manh': 3}, {'os': 'ubuntu-latest', 'manh': 4}, {'os': 'ubuntu-latest', 'manh': 5}, {'os': 'ubuntu-latest', 'manh': 6}, {'os': 'ubuntu-latest', 'manh': 7}, {'os': 'windows-latest', 'manh': 0}]
AST exact ops/cong_cu_test.py:118-119 BoQuaMoiTruong
AST exact ops/cong_cu_test.py:5989-6268 t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi
AST exact ops/cong_cu_test.py:7900-7902 nen_bo_qua_dot_bien
AST exact ops/cong_cu_test.py:7905-7911 dat_windows
AST exact ops/cong_cu_test.py:7914-7918 dong_windows
AST exact ops/cong_cu_test.py:7971-7997 _doc_che_do
AST exact ops/cong_cu_test.py:8880-8974 main
nen_bo_qua_dot_bien nt => True
nen_bo_qua_dot_bien posix => False
nen_bo_qua_dot_bien java => False
dat_windows (61, 0, 470) => True
dat_windows (0, 0, 470) => False
dat_windows (61, 1, 470) => False
dat_windows (61, 0, 0) => False
dong_windows => TỔNG: CA 60/61 đạt · ĐỘT BIẾN 470 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
real shard env at Windows shard 0 = {'CONG_CU_TEST_MANH': '0/8', 'CONG_CU_TEST_MANH_RA': 'manh/manh-0.txt'} => ('manh', (0, 8, 'manh/manh-0.txt'))
real gate env = {'CONG_CU_TEST_BAN_KINH': 'manh'} => ('gate', None)
main AST, fake nt + real shard mode, real main/helpers, fake cases/prechecks; no native Windows execution:

cong_cu_test: 2/2 đạt; tổng=2, bỏ qua=0, tiền kiểm bỏ qua=0

TỔNG: CA 2/2 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
scenario all-pass rc= 0 events= ['first', 'last']
  BỎ QUA skipped_middle: fake missing capability

cong_cu_test: 2/2 đạt; tổng=3, bỏ qua=1, tiền kiểm bỏ qua=0

TỔNG: CA 2/2 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
scenario one-skipped rc= 0 events= ['first', 'middle', 'last']
  ĐỎ  failed_middle: fake baseline failure

cong_cu_test: 2/3 đạt; tổng=3, bỏ qua=0, tiền kiểm bỏ qua=0

TỔNG: CA 2/3 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
scenario one-failed rc= 1 events= ['first', 'middle-fail', 'last']
  BỎ QUA skipped_middle: fake missing capability

cong_cu_test: 0/0 đạt; tổng=1, bỏ qua=1, tiền kiểm bỏ qua=0

TỔNG: CA 0/0 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
scenario all-skipped rc= 1 events= ['middle']
  BỎ QUA t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi: nền này không có `/bin/sh` để dựng ứng viên giả — KHÔNG ĐO ĐƯỢC

cong_cu_test: 2/2 đạt; tổng=3, bỏ qua=1, tiền kiểm bỏ qua=0

TỔNG: CA 2/2 đạt · ĐỘT BIẾN 1 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)
scenario REAL t51 absent-/bin/sh rc= 0 events= ['first', 'last']
REAL t51 AST + fake absent /bin/sh => BoQuaMoiTruong nền này không có `/bin/sh` để dựng ứng viên giả — KHÔNG ĐO ĐƯỢC
5996:     CẢ HAI CHIỀU trước khi vá:
5997:       tốt → xấu: cache trả `/tmp/f1cache/bash` trong khi đo lại trả `None` ("phép argv: rc=7");
5998:       xấu → tốt: cache trả `None` trong khi đo lại trả đúng đường ấy.
5999:     Chiều THỨ HAI mới là chiều độc: cổng báo "KHÔNG CÓ bash" trên một máy ĐÃ CÓ, và người đọc
6000:     log không có cách nào biết mình đang đọc một câu trả lời quá hạn.
6001: 
6002:     N94 (r26) — CACHE ĐÃ GỠ theo quyết định chủ kho, sau lần thứ SÁU cùng hình dạng (codex vòng 20:
6003:     NỘI DUNG tệp mà `BASH_ENV` trỏ tới đổi, cache vẫn trả đường cũ). Đo trước khi chọn: trúng
6004:     cache 3,0 ms, đo lại 5,7 ms. Chốt (3) nay ĐẢO CHIỀU: mọi lần gọi phải ĐO LẠI. Các chốt (1),
6005:     (2), (4), (6), (7) giữ nguyên làm hàng rào: một cache dựng lại sẽ làm chúng đỏ. Chốt (8) đo
6006:     đúng ca vòng 20. Tên ca giữ nguyên vì mỏ neo đột biến trỏ tới nó.
6007:     """
6008:     if not Path("/bin/sh").exists():
6009:         raise BoQuaMoiTruong("nền này không có `/bin/sh` để dựng ứng viên giả — KHÔNG ĐO ĐƯỢC")
6010:     m = runpy.run_path(str(BASH_NEN))
6011:     tim = m["tim_bash"]
8891:     # de to cao. In rieng, dem rieng.
8892:     qua, hong, bo_qua = 0, [], []
8893:     for fn in CA:
8894:         try:
8895:             fn()
8896:             qua += 1
8897:         except BoQuaMoiTruong as ex:
8898:             bo_qua.append((fn.__name__, str(ex)))
8899:         except AssertionError as ex:
8900:             hong.append((fn.__name__, str(ex)))
8901:         except Exception as ex:  # noqa: BLE001
8902:             hong.append((fn.__name__, f"{type(ex).__name__}: {ex}"))
8903:     for ten, ly in tien_kiem_bo_qua:
8904:         print(f"  BỎ QUA (TIỀN KIỂM) {ten}: {ly}")
8905:     for ten, ly in bo_qua:
8906:         print(f"  BỎ QUA {ten}: {ly}")
8907:     for ten, ly in hong:
8908:         print(f"  ĐỎ  {ten}: {ly}")
8909:     print(f"\ncong_cu_test: {qua}/{len(CA) - len(bo_qua)} đạt; tổng={len(CA)}, "
8910:           f"bỏ qua={len(bo_qua)}, tiền kiểm bỏ qua={len(tien_kiem_bo_qua)}")
8911: 
8912:     if che_do == "manh":
8913:         # Mảnh CHỈ đo bán kính của phần mình. Cổng cây thật + các tự kiểm chạy ở job `gate` (chế độ `gate`), một lần.
8914:         if nen_bo_qua_dot_bien():
8915:             # wp879: Windows chỉ chạy ca nền (ở trên, ĐỦ) — không phóng con, không ghi tệp mảnh (job gom Windows đã bỏ).
8916:             so_ca = len(CA) - len(bo_qua)
8917:             print("\n" + dong_windows(qua, so_ca, len(DOT_BIEN)))
8918:             return 0 if dat_windows(so_ca, len(hong) + len(tien_kiem_bo_qua), len(DOT_BIEN)) else 1
8919:         k, n, ra = tham_so
probe_rc=0
```

  kết luận   : LỖI: main vẫn có thể xanh khi một ca nền BoQuaMoiTruong, nên không chứng minh mọi ca nền đã đạt; chi tiết finding bên dưới. Không phóng vòng đột biến ở nhánh nt/manh.

HƯỚNG 3: Gom Ubuntu, ma trận rỗng và skip

  giả thuyết : Đối chiếu trực tiếp khẳng định trong 9 dòng mới với cấu hình và mã tại reviewed_sha.
  lệnh       : từ cay-kho/: `python3 -B ../audit_review.py merger`
  output     :

```text
needs = ['chuan-bi', 'gate-cong-cu']
job.if = ${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}
matrix = {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}', 'exclude': [{'os': 'windows-latest'}]}
os= ['windows-latest'] cancelled= False job-condition(!cancelled && ubuntu in os)= False expanded-if-forced= []
os= ['windows-latest'] cancelled= True job-condition(!cancelled && ubuntu in os)= False expanded-if-forced= []
os= ['ubuntu-latest'] cancelled= False job-condition(!cancelled && ubuntu in os)= True expanded-if-forced= [{'os': 'ubuntu-latest'}]
os= ['ubuntu-latest'] cancelled= True job-condition(!cancelled && ubuntu in os)= False expanded-if-forced= [{'os': 'ubuntu-latest'}]
os= ['ubuntu-latest', 'windows-latest'] cancelled= False job-condition(!cancelled && ubuntu in os)= True expanded-if-forced= [{'os': 'ubuntu-latest'}]
os= ['ubuntu-latest', 'windows-latest'] cancelled= True job-condition(!cancelled && ubuntu in os)= False expanded-if-forced= [{'os': 'ubuntu-latest'}]
582:   # Job GOM: KHÔNG tin phán quyết của mảnh — dựng lại phân hoạch từ `DOT_BIEN` của chính nó, kiểm từng bản ghi bằng
583:   # cùng bộ nhận của đường song song, ĐỎ khi thiếu/trùng mảnh, lệch băm/HEAD, lệch tổng. `!cancelled()`: mảnh đỏ thì
584:   # gom VẪN chạy và ĐỎ vì thiếu mảnh — `needs` mặc định sẽ cho nó `skipped`, mà `skipped` đọc như xanh ở check bắt buộc.
585:   # Sau land: chủ kho thêm context `gate-cong-cu-gop (ubuntu-latest)` vào ruleset (spec #668 §7).
586:   # wp879: gom CHỈ trên ubuntu-latest (Windows không còn mảnh để gom). `os` vẫn lấy từ `chuan-bi` (chốt nguồn duy nhất,
587:   # `t161`) và loại `windows-latest`; `if` theo cùng output ⇒ lượt `runner_set=windows-only` (#878) thì job này `skipped`
588:   # trước khi ma trận rỗng, không đỏ oan vì "thiếu mảnh 0..7".
589:   gate-cong-cu-gop:
590:     needs: [chuan-bi, gate-cong-cu]
591:     if: ${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}
592:     strategy:
593:       fail-fast: false
594:       matrix:
595:         os: ${{ fromJson(needs.chuan-bi.outputs.os) }}
596:         exclude:
597:           - {os: windows-latest}
598:     runs-on: ${{ matrix.os }}
Measured: YAML condition false and forced matrix empty for windows-only.
NOT MEASURED: GitHub server job.if-before-matrix scheduling, actual skipped state/run ID/attempt/runner.
Reasoned expectation: job.if evaluated before strategy.matrix means skipped; exclude alone does not prove skipped.
probe_rc=0
```

  kết luận   : KHÔNG ĐO ĐƯỢC trạng thái GitHub thực. Điều kiện YAML false với windows-only; theo thứ tự job.if trước matrix thì dự kiến skipped; exclude riêng lẻ tạo ma trận rỗng, không đủ để gọi skipped.

HƯỚNG 4: Toàn bộ job, matrix, exclude và job.if

  giả thuyết : Đối chiếu trực tiếp khẳng định trong 9 dòng mới với cấu hình và mã tại reviewed_sha.
  lệnh       : từ cay-kho/: `python3 -B ../audit_review.py census`
  output     :

```text
chuan-bi {"runs-on": "ubuntu-latest", "needs": null, "job.if": null, "matrix": null, "windows-only matrix rows": []}
gate {"runs-on": "${{ matrix.os }}", "needs": "chuan-bi", "job.if": null, "matrix": {"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}, "windows-only matrix rows": [{"os": "windows-latest"}]}
gate-cong-cu {"runs-on": "${{ matrix.os }}", "needs": "chuan-bi", "job.if": null, "matrix": {"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}", "manh": [0, 1, 2, 3, 4, 5, 6, 7], "exclude": [{"os": "windows-latest", "manh": 1}, {"os": "windows-latest", "manh": 2}, {"os": "windows-latest", "manh": 3}, {"os": "windows-latest", "manh": 4}, {"os": "windows-latest", "manh": 5}, {"os": "windows-latest", "manh": 6}, {"os": "windows-latest", "manh": 7}]}, "windows-only matrix rows": [{"os": "windows-latest", "manh": 0}]}
gate-cong-cu-gop {"runs-on": "${{ matrix.os }}", "needs": ["chuan-bi", "gate-cong-cu"], "job.if": "${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}", "matrix": {"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}", "exclude": [{"os": "windows-latest"}]}, "windows-only matrix rows": []}
gate-ops {"runs-on": "${{ matrix.os }}", "needs": "chuan-bi", "job.if": null, "matrix": {"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}, "windows-only matrix rows": [{"os": "windows-latest"}]}
gate-nhanh-manh {"runs-on": "${{ matrix.os }}", "needs": "chuan-bi", "job.if": null, "matrix": {"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}", "manh": [0, 1, 2, 3, 4, 5, 6, 7]}, "windows-only matrix rows": [{"os": "windows-latest", "manh": 0}, {"os": "windows-latest", "manh": 1}, {"os": "windows-latest", "manh": 2}, {"os": "windows-latest", "manh": 3}, {"os": "windows-latest", "manh": 4}, {"os": "windows-latest", "manh": 5}, {"os": "windows-latest", "manh": 6}, {"os": "windows-latest", "manh": 7}]}
gate-nhanh-gop {"runs-on": "${{ matrix.os }}", "needs": ["chuan-bi", "gate-nhanh-manh"], "job.if": "${{ !cancelled() }}", "matrix": {"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}, "windows-only matrix rows": [{"os": "windows-latest"}]}
gate-registry {"runs-on": "${{ matrix.os }}", "needs": ["chuan-bi", "gate-nhanh-gop"], "job.if": "${{ !cancelled() }}", "matrix": {"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}, "windows-only matrix rows": [{"os": "windows-latest"}]}
gate-packet-loop {"runs-on": "${{ matrix.os }}", "needs": "chuan-bi", "job.if": null, "matrix": {"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}, "windows-only matrix rows": [{"os": "windows-latest"}]}
Job definitions: 9 ; gate* definitions: 8
windows-only includes fixed Ubuntu chuan-bi; input removes Ubuntu MATRIX rows only.
Declared job rows are not evidence of an allocated Windows runner or completed steps.
probe_rc=0
```

  kết luận   : KHÔNG PHẢI LỖI ở MỨC KHAI BÁO JOB: ngoài gate-cong-cu-gop, mọi gate* có hàng Windows; vẫn phụ thuộc chuan-bi/thành công dependency/hủy. Không nhận hàng matrix là bằng chứng thực thi.

HƯỚNG 5: Kiểm đếm step.if và đường bỏ qua khác

  giả thuyết : Đối chiếu trực tiếp khẳng định trong 9 dòng mới với cấu hình và mã tại reviewed_sha.
  lệnh       : từ cay-kho/: `python3 -B ../audit_review.py steps`
  output     :

```text
step if runner.os count = 6
["gate", 29, 429, "ci-phamvi selftest (phan chung — cong co rang)", "runner.os != 'Windows'"]
["gate-cong-cu", 9, 575, "actions/upload-artifact@v4", "runner.os != 'Windows'"]
["gate-ops", 9, 696, "ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)", "runner.os == 'Linux'"]
["gate-ops", 12, 785, "don-nhanh selftest (chốt xoá nhánh)", "runner.os != 'Windows'"]
["gate-ops", 13, 818, "bo ca gate chay TRONG cgroup duoc uy quyen (Linux)", "${{ runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"]
["gate-ops", 14, 859, "gate lifecycle selftest (nen khong co cgroup)", "${{ runner.os != 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"]
step if matrix.os = []
shell census = {'(runner default)': 71, 'bash': 25, 'pwsh': 1}
continue-on-error = [['chuan-bi', 1, True, "${{ github.event_name == 'pull_request' }}"], ['chuan-bi', 2, True, "${{ github.event_name == 'pull_request' }}"]]
all step OS references (including script/env/name) =
["gate", 22, 293, "tl selftest (co bang chung exact-identity)", "${{ github.event_name != 'pull_request' }}"]
["gate", 23, 327, "tai len gate-evidence", "always()"]
["gate", 29, 429, "ci-phamvi selftest (phan chung — cong co rang)", "runner.os != 'Windows'"]
["gate", 32, 470, "release-verify strict (lane WORKER — manifest TẠM ngoài repo)", "github.ref != 'refs/heads/master'"]
["gate-cong-cu", 8, 565, "G5 manh ban kinh dot bien (#668)", ""]
["gate-cong-cu", 9, 575, "actions/upload-artifact@v4", "runner.os != 'Windows'"]
["gate-cong-cu-gop", 5, 617, "actions/download-artifact@v4", ""]
["gate-ops", 9, 696, "ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)", "runner.os == 'Linux'"]
["gate-ops", 12, 785, "don-nhanh selftest (chốt xoá nhánh)", "runner.os != 'Windows'"]
["gate-ops", 13, 818, "bo ca gate chay TRONG cgroup duoc uy quyen (Linux)", "${{ runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"]
["gate-ops", 14, 859, "gate lifecycle selftest (nen khong co cgroup)", "${{ runner.os != 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"]
["gate-nhanh-manh", 4, 893, "chạy mảnh nhanh_don_duoc (targeted_mutant_gate)", ""]
["gate-nhanh-manh", 5, 898, "actions/upload-artifact@v4", ""]
["gate-nhanh-gop", 4, 929, "actions/download-artifact@v4", ""]
raw OS/alternate-syntax references:
73:       # `continue-on-error` o HAI buoc phan loai la CO CHU DICH, khong phai nuot loi: khong phan loai duoc thi phai roi
77:       # ⇒ buoc that bai ⇒ `continue-on-error` giu job xanh ⇒ `che_do` vang ⇒ `day_du`.
80:         continue-on-error: true
88:         continue-on-error: true
110:     runs-on: ${{ matrix.os }}
156:         shell: bash
161:         shell: bash
164:         shell: bash
167:         shell: bash
193:         shell: bash
231:       # CHẶN NGAY TỪ F2-A, KHÔNG `continue-on-error`: đây là CI policy, thuộc commit policy.
295:         shell: bash
316:           NEN="${RUNNER_OS}"
331:           name: gate-evidence-${{ matrix.os }}-${{ github.run_attempt }}
430:         if: runner.os != 'Windows'
447:       # thứ hai: biểu thức này đã dùng nguyên văn ở `concurrency` và ở `matrix.os` phía trên.
472:         shell: bash
496:         shell: bash
513:   # (`.claude/dev/ci_dang_ky_test.py`) ghim hình dạng hai job này; `N` trong `CONG_CU_TEST_MANH` phải khớp matrix.
531:     runs-on: ${{ matrix.os }}
555:         shell: bash
560:         shell: bash
563:         shell: bash
566:         shell: bash
569:           CONG_CU_TEST_MANH: ${{ matrix.manh }}/8
570:           CONG_CU_TEST_MANH_RA: manh/manh-${{ matrix.manh }}.txt
575:       - if: runner.os != 'Windows'
578:           name: gate-cong-cu-manh-${{ matrix.os }}-${{ matrix.manh }}
579:           path: manh/manh-${{ matrix.manh }}.txt
598:     runs-on: ${{ matrix.os }}
619:           pattern: gate-cong-cu-manh-${{ matrix.os }}-*
623:         shell: bash
640:     runs-on: ${{ matrix.os }}
668:         shell: bash
671:         shell: bash
684:         shell: bash
697:         if: runner.os == 'Linux'
744:         shell: bash
786:         if: runner.os != 'Windows'
787:         shell: pwsh
819:         if: ${{ runner.os == 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}
860:         if: ${{ runner.os != 'Linux' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}
875:     runs-on: ${{ matrix.os }}
895:           NHANH_DON_DUOC_DICH: ${{ matrix.manh }}/8
896:           NHANH_DON_DUOC_DICH_RA: manh/manh-${{ matrix.manh }}.json
900:           name: gate-nhanh-${{ matrix.os }}-${{ matrix.manh }}
901:           path: manh/manh-${{ matrix.manh }}.json
911:     runs-on: ${{ matrix.os }}
931:           pattern: gate-nhanh-${{ matrix.os }}-*
955:     runs-on: ${{ matrix.os }}
979:         shell: bash
984:         shell: bash
987:         shell: bash
990:         shell: bash
1021:     runs-on: ${{ matrix.os }}
1047:         shell: bash
1052:         shell: bash
1055:         shell: bash
1058:         shell: bash
Explicit bash/pwsh chooses interpreter; no implicit Windows skip inferred from shell choice.
probe_rc=0
```

  kết luận   : KHÔNG PHẢI LỖI: đúng 6 step.if theo runner.os, gồm 2 biểu thức bọc ${{ }}; không có step.if theo matrix.os, không có continue-on-error riêng cho Windows. shell bash/pwsh không tự bỏ bước Windows.

HƯỚNG 6: Truy nguồn SHA, packet #878/#879 và chú thích

  giả thuyết : Đối chiếu trực tiếp khẳng định trong 9 dòng mới với cấu hình và mã tại reviewed_sha.
  lệnh       : từ cay-kho/: `python3 -B ../audit_review.py history`
  output     :

```text
$ git show --no-patch --format=%H%n%aI%n%s%n%b 5585abe
5585abe8499e920e2a6ae8236e70c4096f95e71d
2026-10-22T16:09:14+00:00
wp878(#878): ci.yml workflow_dispatch nhan runner_set=windows-only — bo cac job ma tran Ubuntu khi chi can do Windows
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QFJQm8mNRrRmPUhkqciiC2

rc= 0
$ git show --no-patch --format=%H%n%aI%n%s%n%b 747f983
747f983ccbcaf29a8e5228d09fd05b5a5ab6e479
2026-10-23T08:19:34+07:00
Merge pull request #880 from ducthangho/agent/wp878-g1-claude
wp878(#878): ci.yml workflow_dispatch nhận runner_set=windows-only
rc= 0
$ git show --no-patch --format=%H%n%aI%n%s%n%b be00ef7
be00ef723eca3fae90932e476d683f233588f2b3
2026-10-23T01:32:16+00:00
wp879: gate-cong-cu Windows chỉ chạy ca nền (một job), bán kính đột biến đo trên Ubuntu (#879)
- ops/cong_cu_test.py: vị từ thuần nen_bo_qua_dot_bien / dat_windows / dong_windows
  (khuôn #456); chế độ mảnh trên nền nt chạy ĐỦ ca nền rồi dừng, không phóng con,
  không ghi tệp mảnh. _TEN_NEN là cửa để giàn giáo --tu-kiem-main (t54) ép cả hai
  nhánh trên Linux; sáu kịch bản nt mới + bảng vị từ. CA vẫn 61, DOT_BIEN vẫn 470,
  mọi mỏ neo đột biến giữ nguyên số lần xuất hiện.
- ci.yml: gate-cong-cu loại windows mảnh 1..7 (Windows một job), tải lên chỉ khi
  không phải Windows; gate-cong-cu-gop loại windows-latest, if theo output os của
  chuan-bi (lượt windows-only thì skipped, không đỏ vì thiếu mảnh).
- ci_dang_ky_test.py: ghim hình dạng mới + 8 phản chứng wp879.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QFJQm8mNRrRmPUhkqciiC2

rc= 0
$ git show --no-patch --format=%H%n%aI%n%s%n%b e63961f
e63961f27b53e66db8e6600009f97d5706743063
2026-10-23T11:04:54+07:00
Merge pull request #883 from ducthangho/agent/wp879-g1-claude
wp879: gate-cong-cu Windows chỉ chạy ca nền (một job), bán kính đột biến đo trên Ubuntu (#879)
rc= 0
$ git show --no-patch --format=%H%n%aI%n%s%n%b 8d5cccb
8d5cccbb13b0b2c5ba1c9bbc4f8af410a19f87b8
2026-10-23T07:11:13+00:00
docs(CLAUDE.md): (c) do lai 23-10 — nhanh runner_set=windows-only (#878) va Windows chi la MOT PHAN gate (#879)
Dong 162 khai goi tay => [ubuntu, windows]; tu #878 runner_set=windows-only
=> [windows-latest]. Them cau: tu #879 gate-cong-cu tren Windows chi con manh 0
(ca nen roi dung, ban kinh dot bien chi do tren Ubuntu), gate-cong-cu-gop loai
windows-latest va skipped voi windows-only; 6 buoc ci.yml co if theo runner.os.

Do tren e63961f bang evaluator _danh_gia_bieu_thuc_chuan_bi tren bieu thuc that:
push+master => [ubuntu]; dispatch windows-only => [windows];
dispatch windows-and-ubuntu => [ubuntu, windows].
Kiem: doctrine-scan rc=0; doc-claims-check ok=true; ai-dang-giu CLAUDE.md => NGUOI_GIU 0.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01V2PEqhkb91vD5PCBM5yXbm

rc= 0
$ git merge-base --is-ancestor 5585abe e63961f
rc= 0
$ git show --format= 5585abe -- .github/workflows/ci.yml
diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
index 685d6dc..bc0c240 100644
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -16,7 +16,20 @@ on:
   # từng chạy lần nào. `workflow_dispatch` cho phép soi gate theo yêu cầu trên BẤT KỲ ref nào, không
   # phải mở PR mới biết. (GitHub đòi workflow có mặt ở nhánh mặc định thì nút này mới dùng được ⇒ chỉ
   # hiệu lực SAU khi bản này lên master.)
+  #
+  # packet #878 (CI-DISPATCH-CHI-WINDOWS): dispatch hầu như luôn được gọi để đo WINDOWS cho một head ĐÃ có lượt PR
+  # Ubuntu, nên phần Ubuntu (250–330 phút/lượt, đo 19→22-10-2026) là lặp. `windows-only` bỏ phần ấy; mặc định
+  # GIỮ hành vi cũ (hai nền). Cùng từ vựng với `launcher-windows.yml` — ghim ở `.claude/dev/ci_dang_ky_test.py`.
   workflow_dispatch:
+    inputs:
+      runner_set:
+        description: "windows-and-ubuntu (mặc định) hoặc windows-only (bỏ các job ma trận Ubuntu)"
+        required: false
+        default: windows-and-ubuntu
+        type: choice
+        options:
+          - windows-and-ubuntu
+          - windows-only
 
 # r245 — CẮT PHÚT ACTIONS. Đo ngày 13-08: gate chạy 6,6 phút tường, nhân hệ số
 # Windows x2 thành ~20 phút TÍNH TIỀN mỗi lượt, x13,6 lượt/ngày = ~8.100 phút/tháng.
@@ -47,7 +60,10 @@ jobs:
     # ngan thoi gian chan tu 360 phut mac dinh xuong day. Tran trong o hai buoc phan loai ben duoi (het gio => roi day_du).
     timeout-minutes: 20
     outputs:
-      os: ${{ (github.event_name == 'workflow_dispatch'
+      # #878: vế đầu chỉ đúng khi dispatch CHỌN `windows-only`; dispatch không input (API cũ) rơi xuống vế hai như cũ.
+      os: ${{ (github.event_name == 'workflow_dispatch' && inputs.runner_set == 'windows-only')
+              && '["windows-latest"]'
+              || (github.event_name == 'workflow_dispatch'
                || contains(github.event.pull_request.labels.*.name, 'windows'))
               && '["ubuntu-latest","windows-latest"]'
               || '["ubuntu-latest"]' }}
rc= 0
$ git merge-base --is-ancestor be00ef7 e63961f
rc= 0
$ git show --format= be00ef7 -- .github/workflows/ci.yml
diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
index d9e2e39..f618cdb 100644
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -511,6 +511,8 @@ jobs:
   # nên chỉ nhiều RUNNER mới rút được thời gian tường. Mỗi mảnh chạy lại ĐÚNG phần thiết lập G5 của `gate` (ca của
   # mảnh cần đủ công cụ, thiếu thì ca đích bị BỎ QUA và bán kính KHÔNG ĐO ĐƯỢC). `loi_g5_workflow`
   # (`.claude/dev/ci_dang_ky_test.py`) ghim hình dạng hai job này; `N` trong `CONG_CU_TEST_MANH` phải khớp matrix.
+  # wp879 (#879): Windows chỉ còn MỘT job (mảnh 0) và `cong_cu_test.py` ở đó chạy ĐỦ ca nền rồi dừng (`nen_bo_qua_dot_bien`)
+  # — 111/118 lượt mảnh Windows không xanh vì lý do của nền (#853), mỗi lượt 570–650 phút. Bán kính đo trên ubuntu-latest.
   gate-cong-cu:
     needs: chuan-bi
     strategy:
@@ -518,6 +520,14 @@ jobs:
       matrix:
         os: ${{ fromJson(needs.chuan-bi.outputs.os) }}
         manh: [0, 1, 2, 3, 4, 5, 6, 7]
+        exclude:
+          - {os: windows-latest, manh: 1}
+          - {os: windows-latest, manh: 2}
+          - {os: windows-latest, manh: 3}
+          - {os: windows-latest, manh: 4}
+          - {os: windows-latest, manh: 5}
+          - {os: windows-latest, manh: 6}
+          - {os: windows-latest, manh: 7}
     runs-on: ${{ matrix.os }}
     # WP748 r20 (chu kho, PR #849): 45 -> 150. Do run 39304938900 tren 9983615: CA 8 manh Windows bi huy
     # o dung phut 45 (18:45:15 -> 19:29:33), khong mot assertion nao do; Ubuntu cung dot xong trong 18-32 phut.
@@ -561,7 +571,9 @@ jobs:
         run: |
           python ops/cong_cu.py kiem-tra --json
           python ops/cong_cu_test.py
-      - uses: actions/upload-artifact@v4
+      # wp879: Windows không ghi tệp mảnh (không đo bán kính) và không có job gom ⇒ không tải gì lên.
+      - if: runner.os != 'Windows'
+        uses: actions/upload-artifact@v4
         with:
           name: gate-cong-cu-manh-${{ matrix.os }}-${{ matrix.manh }}
           path: manh/manh-${{ matrix.manh }}.txt
@@ -571,13 +583,18 @@ jobs:
   # cùng bộ nhận của đường song song, ĐỎ khi thiếu/trùng mảnh, lệch băm/HEAD, lệch tổng. `!cancelled()`: mảnh đỏ thì
   # gom VẪN chạy và ĐỎ vì thiếu mảnh — `needs` mặc định sẽ cho nó `skipped`, mà `skipped` đọc như xanh ở check bắt buộc.
   # Sau land: chủ kho thêm context `gate-cong-cu-gop (ubuntu-latest)` vào ruleset (spec #668 §7).
+  # wp879: gom CHỈ trên ubuntu-latest (Windows không còn mảnh để gom). `os` vẫn lấy từ `chuan-bi` (chốt nguồn duy nhất,
+  # `t161`) và loại `windows-latest`; `if` theo cùng output ⇒ lượt `runner_set=windows-only` (#878) thì job này `skipped`
+  # trước khi ma trận rỗng, không đỏ oan vì "thiếu mảnh 0..7".
   gate-cong-cu-gop:
     needs: [chuan-bi, gate-cong-cu]
-    if: ${{ !cancelled() }}
+    if: ${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}
     strategy:
       fail-fast: false
       matrix:
         os: ${{ fromJson(needs.chuan-bi.outputs.os) }}
+        exclude:
+          - {os: windows-latest}
     runs-on: ${{ matrix.os }}
     timeout-minutes: 10
     env:
rc= 0
base and reviewed blobs .github/workflows/ci.yml
$ git rev-parse e63961f:.github/workflows/ci.yml HEAD:.github/workflows/ci.yml
f618cdb469016ac585724d286b498b7e1dcc80ea
f618cdb469016ac585724d286b498b7e1dcc80ea
rc= 0
base and reviewed blobs ops/cong_cu_test.py
$ git rev-parse e63961f:ops/cong_cu_test.py HEAD:ops/cong_cu_test.py
0053da2ca150f881235b604c833aa91430ca059c
0053da2ca150f881235b604c833aa91430ca059c
rc= 0
No local exact-run receipt found under filenames wp878/wp879/pr880/pr883; commit comments are source claims, not independent Actions runtime evidence.
probe_rc=0
```

  kết luận   : KHÔNG PHẢI LỖI: commit #878/#879 đều là tổ tiên e63961f; lời trích đúng commit/chú thích và workflow/code không đổi từ base tới reviewed_sha. Không lấy chú thích skipped làm bằng chứng runtime.

HƯỚNG 7: Đối chiếu doctrine, lời khai cũ và ADR-0049

  giả thuyết : Đối chiếu trực tiếp khẳng định trong 9 dòng mới với cấu hình và mã tại reviewed_sha.
  lệnh       : từ cay-kho/: `python3 -B ../audit_review.py contradictions`
  output     :

```text
CLAUDE.md
156:   là chỗ mù, và đăng thêm một lời gọi review với cái cớ sai — trong khi kết luận sạch đã có từ 20 phút
157:   trước. **Muốn biết đã review chưa thì tìm dòng `Reviewed commit:` cho ĐÚNG commit đang xét.**
158:   · **(c) Ma trận `os` của `ci.yml` KHÔNG phân biệt PR với master — và câu ngược lại từng nằm ở đây.**
159:   Bản cũ của mục này viết: *"PR thường chỉ chạy `ubuntu`, còn master chạy CẢ `ubuntu` LẪN `windows`"*.
160:   Câu ấy **ĐÃ CHẾT** từ packet #548 (`CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND`, bỏ vế
161:   `github.ref == 'refs/heads/master'` khỏi output `os` của job `chuan-bi`). **Đo 22-10-2026** trên
162:   `9e9a74b`: `os` = `["ubuntu-latest","windows-latest"]` CHỈ KHI `github.event_name == 'workflow_dispatch'`
163:   HOẶC PR mang nhãn `windows`; mọi trường hợp khác — **kể cả push lên master** — là `["ubuntu-latest"]`.
164:   **Đo lại 23-10-2026** trên `e63961f`: #878 thêm nhánh thứ ba — gọi tay với `runner_set=windows-only` ⇒
165:   `["windows-latest"]` (KHÔNG có Ubuntu); gọi tay mặc định (`windows-and-ubuntu`) vẫn ra hai nền.
166:   Bằng chứng chạy được: run `ci.yml` **39354156843** (push merge commit `3a3a3ca` lên master,
167:   20-10-2026) có **23 job, cả 23 nhãn `ubuntu-latest`**, 0 job Windows — readback giữ ở
168:   `ops/land/pr848-wp744-provenance/readback-jobs-39354156843.json`. Doctrine cũ đã kịp làm một biên
169:   bản land (commit `3f6c694`) khai `jobs: '23/23 success (gom windows)'`; Codex connector bắt thành P1 trên PR #859 (comment
170:   `r4323607674`), sửa ở PR #865. Đúng bệnh mục này đang dạy: tin một câu GẦN TAY thay vì đọc nhãn job.
171:   **Windows tự động khi push master hiện chỉ đến từ `launcher-windows.yml`**, và CÓ ĐIỀU KIỆN: chỉ bắn
172:   khi đổi `.claude/dev/**` hoặc chính tệp workflow ấy (`paths:`), ma trận `windows-latest` + `ubuntu-latest`;
173:   PR chỉ chạy khi mang nhãn `windows` (workflow này CÓ khai `types: [..., labeled]`). Nó chỉ đo lane
174:   launcher, KHÔNG phải gate. Các workflow còn lại (`ci-dot-bien-du` `ops-*`) đều `ubuntu-latest`.
175:   Hệ quả: với một PR THƯỜNG — không nhãn `windows`, không ai gọi tay — **các lượt PR và push hậu merge
176:   của `ci.yml` theo ma trận hiện tại chỉ đo Ubuntu**; merge không còn là "lần đo Windows đầu tiên" như bản cũ viết.
177:   Muốn biết master có Windows hay không thì **đọc nhãn từng job của lượt chạy**, đừng suy từ tên sự kiện.
178:   **Muốn có Windows cho gate thì đường CHẮC CHẮN là gọi tay `workflow_dispatch` trên ref đó** — kèm
179:   `runner_set=windows-only` (#878) khi head ĐÃ có lượt PR Ubuntu, để khỏi trả lại 250–330 phút Ubuntu; mặc định vẫn hai nền.
180:   **Nhưng "gate trên Windows" từ #879 là MỘT PHẦN gate, không phải bản song song** (đo 23-10-2026 trên
181:   `e63961f`, `exclude:` của ma trận): `gate-cong-cu` trên Windows chỉ còn mảnh 0 và ở đó `cong_cu_test.py`
182:   chạy đủ ca nền rồi DỪNG — **bán kính đột biến chỉ đo trên Ubuntu**; `gate-cong-cu-gop` loại hẳn
183:   `windows-latest`, và với `windows-only` thì job ấy `skipped` (`if:` đòi `ubuntu-latest` trong `os`). Các job
184:   `gate*` còn lại vẫn có mặt trên Windows ở MỨC JOB — nhưng 6 bước trong `ci.yml` mang `if:` theo
185:   `runner.os` (tắt hoặc thay riêng trên Windows), nên "có job Windows" chưa phải "mọi bước chạy". Nên một lượt `windows-only` xanh chứng minh **ca nền đạt trên Windows**,
186:   KHÔNG chứng minh bán kính đột biến — phần đó phải lấy từ lượt Ubuntu của CÙNG head.
187:   Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai
188:   trên PR #109): `ci.yml` khai `pull_request:` mà KHÔNG khai `types:`, nên mặc định chỉ bắn ở
189:   `opened`/`synchronize`/`reopened` — **`labeled` không nằm trong đó**. Gắn nhãn không tự sinh lượt
190:   chạy nào; ma trận chỉ đọc nhãn ở lượt bắn KẾ TIẾP. Người làm theo sẽ gắn nhãn, thấy vẫn đúng một
191:   check Ubuntu, rồi merge mà tưởng đã có Windows. Muốn dùng nhãn thì phải kèm một cò mới sau khi gắn
192:   (đẩy thêm commit, hoặc đóng rồi mở lại PR) — hoặc khai `types: [..., labeled]` cho workflow.
193:   (Đợt 14-08 không dùng đường nào; khi ấy ma trận còn vế master nên sáu lần merge là sáu lần đo
194:   Windows đầu tiên — nay cùng tình huống thì là **không lần nào**.)
195:   Kèm theo: trên lượt master, bước `PR head contains required EOL base` LUÔN `skipped` vì nó có
196:   `if: github.event_name == 'pull_request'` — nên tiêu chí "không bước nào `skipped`" chỉ đúng cho
197:   lượt PR; bê nguyên sang lượt master là tự báo động giả.
198:   Cả ba cùng họ với bài học "cổng không nói dối, nó VẮNG MẶT": **"vắng mặt vì sạch" và "vắng mặt vì
CLAUDE.md
810: - **API CHỈ CÓ TRÊN MỘT NỀN: hỏi trước, đừng đụng thẳng — và một job CI mặc định SKIP
811:   là một cổng KHÔNG TỒN TẠI.** Hai lần trong cùng một ngày: `os.O_NOFOLLOW` (bot review
812:   bắt) và `os.getpgid` trong chốt cô lập — cái sau làm suite **0/103** trên
813:   `windows-latest`, tức bộ test **chưa từng chạy** trên Windows kể từ lúc có chốt ấy.
814:   Không ai biết, vì job Windows chỉ chạy khi PR có nhãn `windows`. Năm lượt cross-review
815:   trên Linux không thể thấy, và đã không thấy.
816:   Ba luật: (1) `hasattr`/`getattr(..., mặc_định)` trước khi đụng API riêng nền; (2)
817:   truyền **lambda** vào hàm bọc lỗi, đừng truyền thẳng `os.getpgid` — tra thuộc tính
818:   xảy ra TRƯỚC lời gọi, tức NGOÀI `try`; (3) gán thêm một API mà nền vốn không có thì
819:   phải **gỡ lại** khi ra khỏi chốt, kẻo nền tự nhận có thứ nó không có.
820:   Gắn nhãn `windows` cho PR đụng `.claude/dev/**` — nó tốn ~40 phút và trả lại thứ mà
821:   năm lượt review không mua được.
CLAUDE.md
914: **Không phải packet nào cũng route sang phiên cloud được.** Lane launcher đo hành vi phụ thuộc nền:
915: cùng `.claude/dev/launcher_test.py`, CI 17-08-2026 đo được Linux bỏ qua 1 ca còn Windows bỏ qua 13. Packet nào
916: đo hạn chót xuyên trạng thái ngủ của máy thì cần `QueryUnbiasedInterruptTime`, chỉ chạy thật trên
917: Windows. Chọn nền theo thứ packet ĐO, đừng chọn theo nền nào đang rảnh.
Every manual/two-platform phrase in CLAUDE.md:
162:   `9e9a74b`: `os` = `["ubuntu-latest","windows-latest"]` CHỈ KHI `github.event_name == 'workflow_dispatch'`
164:   **Đo lại 23-10-2026** trên `e63961f`: #878 thêm nhánh thứ ba — gọi tay với `runner_set=windows-only` ⇒
165:   `["windows-latest"]` (KHÔNG có Ubuntu); gọi tay mặc định (`windows-and-ubuntu`) vẫn ra hai nền.
175:   Hệ quả: với một PR THƯỜNG — không nhãn `windows`, không ai gọi tay — **các lượt PR và push hậu merge
178:   **Muốn có Windows cho gate thì đường CHẮC CHẮN là gọi tay `workflow_dispatch` trên ref đó** — kèm
179:   `runner_set=windows-only` (#878) khi head ĐÃ có lượt PR Ubuntu, để khỏi trả lại 250–330 phút Ubuntu; mặc định vẫn hai nền.
374:   không phân biệt được hai nền đo ấy (đo thẳng: có ⇒ `rc=1` 1 finding · vắng ⇒ `rc=0` 0 finding).
377: - **Workflow chỉ chạy khi có người bấm là workflow KHÔNG có ai canh.** `workflow_dispatch` không chạy
380:   workflow `workflow_dispatch` phải có phản chứng chạy được ở CI, và bộ ấy phải **trích thân bước TỪ
570: Đường dùng được: `.github/workflows/ops-don-ref.yml` (`workflow_dispatch`, kích hoạt được từ phiên web
952:    có chốt, trôi lệch theo máy) đã BỎ — cả hai nền dùng script TRONG repo.
AST exact ops/lease_publish_test.py:7848-7923 _danh_gia_bieu_thuc_chuan_bi
9e9a74b real dispatch os = ['ubuntu-latest', 'windows-latest']
docs/PROTOCOL_DA_PHIEN.md
880: |---|---|---|
881: | T0 | inner loop của Executor | test/fragment trực tiếp cho thay đổi; không phải promotion evidence |
882: | T1 | packet worker gate | affected fragments/groups cùng always-on write-set, EOL, security, manifest/package và selector guards |
883: | T2 | trước `ready_for_rereview` | chạy lại T1 trên exact head; full nếu packet sensitive hoặc classifier yêu cầu |
884: | T3 | integration freeze/`land prepare` | full selftest và release gates trên Windows + Linux cho frozen integration SHA |
885: | T4 | canonical/`merge_group` | full trên candidate canonical, hoặc reuse duy nhất evidence T3 khi toàn bộ exact identity khớp |
886: | T5 | exact release artifact | full smoke/verify trên bundle/artifact có hash sẽ phát hành |
887: 
888: Unknown/unmapped path, selector/catalog/runner/shared fixture hoặc global state thay đổi, security/workflow,
889: release/manifest/package, EOL hay gate policy thay đổi phải fallback full; classifier lỗi/không đọc được cũng
890: fallback full. Top-level path filter hoặc job `skipped` không phải evidence: classifier + aggregator bắt buộc tạo
891: kết quả dương và chặn merge khi required tier thiếu. Evidence chỉ được reuse khi tested SHA/tree, policy/catalog,
892: runner, OS/runtime matrix và artifact hash (nếu có) khớp chính xác; head hoặc một identity đổi thì chạy lại.
893: 
docs/PROTOCOL_DA_PHIEN.md
950: | Run | repository, run ID, attempt, event, run head SHA từ API của đúng run |
951: | Checkout | SHA thực sự chạy, parents và tree từ checkout/log/artifact của đúng job/attempt |
952: | Workflow definition | repository/path, exact commit OID, blob OID và SHA-256 của bytes định nghĩa |
953: | Gate output | job/check-run/context, runner/OS/runtime, command/rc, marker dương và artifact ID/hash |
954: 
955: Không đồng nhất REST run head với checkout hay workflow-definition SHA. Với synthetic merge,
956: chứng minh parents trỏ đúng head/base và tree từ checkout/log/artifact tương ứng; chỉ đo
957: `refs/pull/.../merge` hiện tại không chứng minh run cũ đã test ref ấy. Tree bằng nhau không
958: đồng nhất commit, thời điểm, workflow, loại test hoặc runtime; không tự nâng test head thành
959: test merge hoặc test Windows. Thiếu một mốc bắt buộc thì ghi thiếu, không suy để lấp receipt.
docs/PROTOCOL_DA_PHIEN.md
968: #### 10.2.3 Evidence thiếu, skipped và tiêu chí riêng
969: 
970: Ghi `passed`, `failed`, `skipped`, `not_run` và `not_measured` riêng. API thiếu quyền chỉ
971: cho biết endpoint/field ấy chưa đo được; giữ HTTP status và lỗi thực. Có thể thu tiếp theo
972: chuỗi GraphQL aggregate → jobs/logs → commit statuses, nhưng mỗi nguồn chỉ chứng minh phần
973: nó chứa. Paginate đủ, chọn đúng SHA/run/attempt/context/producer; statuses không tự có
974: workflow/runner/command/output. Chỉ nhận khi tổng evidence đủ identity và nội dung dương,
975: không đổi 403 hay list rỗng thành pass.
976: 
977: Job `skipped` không được cấp runner là chưa thực thi, không là Windows execution dù tên job
978: có Windows. `owner_waived` là disposition riêng chỉ khi có waiver bền của owner: nguồn/actor,
979: exact SHA, context/OS, lý do, phạm vi/hạn và điều kiện thay thế. Giữ nguyên kết quả skipped;
980: waiver không viết lại nó thành passed, không tự gỡ branch protection. Không có waiver đúng
981: scope thì required evidence còn thiếu và tiếp tục chặn gate.
982: 
983: Tiêu chí đột biến riêng phải có receipt dương (baseline) và âm (mutant bị bắt vì đúng tính
984: chất), gắn exact consumer, criterion, command/rc, output/hash và phạm vi đo. **A7 chỉ bắt
985: buộc khi Packet có A7**; khi có, tổng suite không thay receipt cho đúng consumer/tiêu chí A7.
docs/adr/0049-cong-hai-nen-truoc-phat-hanh-khong-phai-moi-lan-land.md
1: # ADR-0049 — Cổng hai nền trước phát hành, không phải mỗi lần land
2: 
3: - **Trạng thái:** Accepted (2026-09-16, chỉ thị chủ kho `ducthangho`; packet #548 `CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND`)
4: 
5: ADR này ghi nhận việc **đổi tiêu chuẩn gate**: cổng kiểm thử hai nền (Linux và Windows) trước khi phát hành được bảo đảm bằng **cổng tại chỗ của `deploy-package.*`**, KHÔNG phải bằng lane `master` của `.github/workflows/ci.yml`.
6: 
7: ## 1. Bối cảnh & Hiện trạng đo được
8: 
9: Từ quyết định grilling 2026-07-09 (#8), `ci.yml` chạy cả `ubuntu-latest` và `windows-latest` để bắt lớp lỗi phụ thuộc nền (mã hóa cp1258, ký tự xuống dòng, đường dẫn file). Tuy nhiên, các phép đo thực tế (16-09-2026, nền `f27a28f`) cho thấy hai bất cập lớn:
10: 
11: 1. **Hậu quả chặn = 0:** Lane Windows trên `master` chạy **SAU** khi PR đã merge. Không có cổng nào chặn land theo kết quả này. Thực tế PR #545 và #547 đều merge thành công trong khi lane Windows của `master` đỏ sẵn (delta = 0). Tức kho trả chi phí đầy đủ cho một tín hiệu không chặn được gì.
12: 2. **Chi phí Actions cạn kiệt:** Runner Windows tính phí gấp đôi (hệ số 2). Đo r245 (13-08): ~20 phút tính tiền mỗi lượt × 13,6 lượt/ngày ≈ 8.100 phút/tháng, vượt xa hạn mức Free 2.000 phút/tháng và đã cạn kiệt thật vào ngày 12-08.
13: 3. **Trôi lệch cấu trúc:** Ba job `gate`, `gate-registry`, `gate-packet-loop` mang ba bản chép nguyên văn cùng một biểu thức ma trận phức tạp.
14: 
15: ## 2. Quyết định: Đổi tiêu chuẩn gate
16: 
17: 1. **Đổi cò Windows trong `ci.yml`:** Bỏ điều kiện `github.ref == 'refs/heads/master'`. Windows chỉ còn kích hoạt khi gọi tay qua `workflow_dispatch` hoặc khi PR có nhãn `windows` (dành cho các thay đổi chạm mã phụ thuộc nền tảng).
18: 2. **Khử trùng lặp qua job `chuan-bi`:** Thêm job `chuan-bi` (chạy trên `ubuntu-latest`, không checkout mã nguồn), tính danh sách nền một lần và xuất qua `outputs.os`. Ba job `gate`, `gate-registry`, `gate-packet-loop` khai `needs: chuan-bi` và đọc `needs.chuan-bi.outputs.os`.
19: 3. **Cổng hai nền tại chỗ của `deploy-package.*`:** Trước khi phát hành gói (`tl drive-push` lên LIVE), người vận hành bắt buộc phải chạy bộ cổng kiểm tra tại chỗ của `deploy-package.ps1` / `deploy-package.sh` (8 cổng: `selftest`, `gen_inst`, `workflow`, `golden`, `docclaims`, `determinism`, `relcheck`, `relverify`). Cổng này chặn thật khi đỏ (dòng 234: `Bad 'GATE ĐỎ — DỪNG, không build/không đẩy'`).
20: 
21: ## 3. Phần mất mát & Rủi ro đã nhận
22: 
23: - **Mất soi Windows tự động cho ~22 bước test:** Việc bỏ Windows khỏi mỗi lần land vào `master` đồng nghĩa ~22 bước kiểm thử trong `ci.yml` (như `lease_publish_test`, `ci_dang_ky_test`, `packet-loop selftest`) không còn được chạy tự động trên Windows sau mỗi commit vào master.
24: - **Cổng Windows đang đỏ biến mất khỏi CI không phải vì được chữa:** Tại thời điểm land (commit `a612c70`, run `35232106589`, job `105238582317`), lane `gate (windows-latest)` trên `master` đang đỏ sẵn 15 ca ở bước 18 `lease-publish selftest` (`133/148 đạt`, do `shutil.which("git", path="/usr/bin:/bin")` hardcode tại `ops/lease_publish.py:1106`, nợ WP541). Việc bỏ Windows khỏi `master` làm tín hiệu đỏ này biến mất khỏi CI, nhưng ADR-0049 **KHÔNG** chữa nợ WP541. Nợ WP541 vẫn còn nguyên và được xử lý ở packet riêng.
25: - **Độ phủ Windows tự động về 0 trên thực tế cho `ops/`, `scripts/`, `.github/`:**
26:   - `ci.yml` dùng trigger `pull_request` mặc định (không khai `types: [labeled]`), nên gắn nhãn `windows` lên PR đang đứng yên không tự kích hoạt run mới mà chỉ ăn ở lần push kế tiếp (`synchronize`) hoặc khi tạo PR đã có nhãn.
27:   - Dưới chính sách `manual_ci_budget: 0` (cấm `workflow_dispatch`), Windows tự động không còn chạy cho `ops/**`, `scripts/**`, `.github/**` (WP541 là bằng chứng sống).
28:   - 8 cổng tại chỗ của `deploy-package.*` là script chạy tay và **không bao gồm** `lease_publish_test` hay các test của `ops/`, nên không thay thế được toàn bộ lane CI bị gỡ.
29:   - Đây là **rủi ro đã nhận** (K4), được chấp nhận để bảo toàn hạn mức CI. Người điều phối và người phát hành chịu trách nhiệm khi thay đổi chạm mã phụ thuộc nền tảng. Nợ có tên `BATTERY-DEPLOY-HEP-HON-LANE-CI` ghi nhận việc mở rộng danh mục kiểm thử của script deploy khi cần thiết.
30: 
31: ## 4. Lời khai trung thực về Windows CI khi land
32: 
33: Tuyên bố *"land không còn chạy Windows"* là **KHÔNG đúng tuyệt đối**:
34: - Workflow `.github/workflows/launcher-windows.yml` (với `paths: .claude/dev/**`) vẫn được giữ nguyên. Mọi thay đổi chạm `.claude/dev/**` khi push vào `master` vẫn kích hoạt và tiêu tốn ~5 phút Windows (Đ6, run `35125176975`).
launcher pull_request trigger = {'types': ['opened', 'synchronize', 'reopened', 'labeled'], 'paths': ['.claude/dev/**']}
launcher job.if = github.event_name != 'pull_request' || contains(github.event.pull_request.labels.*.name, 'windows')
c) old two-platform claim is explicitly dated 22-10 at 9e9a74b; new lines supersede it, not an unconditional present-day claim.
No OTHER unconditional "manual dispatch => two platforms" statement found in CLAUDE.md.
API-only-platform lesson is historical; labeled launcher exists; platform-specific cloud lesson agrees that different OS coverage is not interchangeable.
Protocol distinguishes skipped/not_measured from passed: baseline skipped cases must remain explicit (finding). ADR-0049 does not say dispatch Windows replaces local release gates.
probe_rc=0
```

  kết luận   : LỖI về phạm vi ca nền đạt như HƯỚNG 2 (cùng một finding); không tạo finding cho lời khai lịch sử có neo ngày/SHA, không thấy câu gọi tay => hai nền vô điều kiện khác. Quy tắc cùng SHA/hai nền trước phát hành vẫn giữ.

HƯỚNG 8: Cổng doctrine-scan

  giả thuyết : 9 dòng mới vẫn qua cổng tài liệu theo yêu cầu.
  lệnh       : trong cay-kho/, với PYTHONDONTWRITEBYTECODE=1 và PYTHONUTF8=1: `python3 .claude/dev/packet_loop.py doctrine-scan --root .`
  output     :

```text
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI: cổng passed; không tự chứng minh ngữ nghĩa CI.

HƯỚNG 9: Cổng doc-claims-check

  giả thuyết : 9 dòng mới vẫn qua cổng kiểm trích dẫn tài liệu.
  lệnh       : tại cay-kho/, PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 `python3 scripts/tl.py doc-claims-check --json`
  output     : trích các trường thật từ JSON đầy đủ ở `evidence/09-doc-claims-check.txt` (không chạy lại gate):

```json
{
  "ok": true,
  "schema": "doc_claims_check.v1",
  "files_scanned": 113,
  "flags": [],
  "advisory_count": 381,
  "layers_skipped": {},
  "strict": false
}
```

```text
rc=0
```

  kết luận   : KHÔNG PHẢI LỖI: passed, `"ok": true`, 0 flags, không lớp nào skipped. 381 advisory lịch sử không phải lỗi blocking; cổng này không kiểm ngữ nghĩa coverage CI.

HƯỚNG 10: Phạm vi bán kính, default checkout và cùng head

  giả thuyết : Đối chiếu trực tiếp khẳng định trong 9 dòng mới với cấu hình và mã tại reviewed_sha.
  lệnh       : từ cay-kho/: `python3 -B ../audit_review.py provenance`
  output     :

```text
All cong_cu_test.py workflow invocations and their mode env:
gate step= G5 kiem ban ke cong cu + T1..T8 (packet step.if= None env= {'CONG_CU_TEST_BAN_KINH': 'manh'} run= 'python ops/cong_cu.py kiem-tra --json\npython ops/cong_cu_test.py\n'
gate-cong-cu step= G5 manh ban kinh dot bien (#668) step.if= None env= {'CONG_CU_TEST_MANH': '${{ matrix.manh }}/8', 'CONG_CU_TEST_MANH_RA': 'manh/manh-${{ matrix.manh }}.txt'} run= 'python ops/cong_cu.py kiem-tra --json\npython ops/cong_cu_test.py\n'
gate-cong-cu-gop step= G5 gom manh ban kinh dot bien (#668) step.if= None env= None run= 'python ops/cong_cu_test.py --gop manh'
Main gate checkout (real YAML):
{"uses": "actions/checkout@v4", "with": {"fetch-depth": 0}}
.github/workflows/ci.yml
130:     steps:
131:       - name: Force LF checkout (hash parity với manifest)
132:         run: |
133:           git config --global core.autocrlf false
134:           git config --global core.eol lf
135:           # r226 — NGƯỠNG L2 CỦA doc-claims-check PHẢI TẤT ĐỊNH. `sha_lens` lấy từ `git rev-parse --short`,
136:           # mà git tự nới độ dài viết tắt theo SỐ OBJECT của kho. ĐO trên chính kho này: clone `--depth 1`
137:           # → 7 · clone đủ lịch sử (281 commit, 17.783 object) → 8. Mà 8 đúng bằng độ dài tiền tố UUID
138:           # notebook (743ed200, 45739ff7, dbe706a0…) ⇒ ngưỡng trôi lên 8 thì 18 tiền tố UUID bị hô
139:           # SHA_NOT_A_COMMIT và ca r218_docclaims_l2_sha_khong_ton_tai (mồi `deadbee`, 7 ký tự) cũng đỏ
140:           # theo. Ghim 7 = giữ ĐÚNG ngưỡng mọi phép đo của r218 dựa vào, KHÔNG phải nới lỏng guard.
141:           git config --global core.abbrev 7
142:       - uses: actions/checkout@v4
143:         with:
144:           # r226 — `fetch-depth` mặc định (1) làm L2 MÙ: `cat-file -e` trượt với mọi SHA cũ nên trích dẫn
145:           # ĐÚNG bị hô sai (đo: `ad413e7`/`78d6bfe` — cả hai là commit thật 09-07 và 07-07 — bị gắn cờ
146:           # SHA_NOT_A_COMMIT trên clone `--depth 1`). Guard chỉ kết luận được khi có lịch sử để tra.
147:           fetch-depth: 0
148:       - uses: actions/setup-python@v5
.github/workflows/ci.yml
284:       #
285:       # Không có cách nào làm đúng ở lượt PR mà không đổi thứ CI đang test: cây
286:       # merge chính là thứ đáng test trước khi vào master. Nên bằng chứng chỉ sinh
287:       # ở `push`/`workflow_dispatch`, đúng luồng `gate-targeted.md` mô tả ("T1
288:       # push/handoff: chờ CI tạo full evidence exact-head"). Lượt PR vẫn chạy
289:       # selftest, chỉ không giả vờ sinh ra chứng cho một commit không có trong lịch sử.
290:       - name: tl selftest (luot PR — khong sinh bang chung)
291:         if: ${{ github.event_name == 'pull_request' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}
292:         run: python scripts/tl.py --selftest
293:       - name: tl selftest (co bang chung exact-identity)
294:         if: ${{ github.event_name != 'pull_request' }}
295:         shell: bash
296:         run: |
297:           set -euo pipefail
298:           mkdir -p scripts/.tl_state/gate
299:           # KHÔNG dùng `--depth`: checkout ở trên cố ý đặt `fetch-depth: 0` cho
300:           # `doc-claims` L2 (`cat-file -e` trượt mọi SHA cũ trên clone nông). Một
301:           # `--depth=50` ở đây có thể làm nông lại chính thứ bước kia cần, và tệ hơn
302:           # là `merge-base` sẽ trượt khi nhánh rẽ xa hơn 50 commit (P2 review "#141").
303:           # FAIL-CLOSE: `base_sha` sai làm bằng chứng vô dụng một cách IM LẶNG.
304:           git fetch --no-tags origin master
305:           # HEAD ĐÚNG LÀ HEAD CỦA PR, không phải `$GITHUB_SHA`. Trên `pull_request`,
306:           # `$GITHUB_SHA` là commit MERGE TỔNG HỢP do GitHub dựng — dòng 73 của chính
307:           # tệp này đã cảnh báo đúng điều đó, và tôi vẫn viết sai ở đây (P2 review
308:           # "#141"). Evidence neo vào commit tổng hợp thì không ai validate lại được
309:           # vì commit ấy không có trong lịch sử nhánh.
310:           # `HEAD` của cây, không phải biến nào cả: bằng chứng phải khai ĐÚNG
311:           # thứ vừa đo. Bước này chỉ chạy khi HEAD là commit thật (xem `if:` trên).
312:           HEAD_SHA="$(git rev-parse HEAD)"
313:           BASE_SHA="$(git merge-base FETCH_HEAD "$HEAD_SHA")"
314:           echo "head_sha = $HEAD_SHA"
315:           echo "base_sha = $BASE_SHA"
316:           NEN="${RUNNER_OS}"
317:           python .claude/dev/gate_lifecycle.py run \
318:             --kind heavy --name tl-selftest --repo . \
.github/workflows/ci.yml
864:   # (MỖI con chỉ chạy CA ĐÍCH đã khai) + 10 đột biến sản phẩm, chia 8 mảnh cân theo chi phí đo được; mỗi mảnh
865:   # ghi biên nhận (head, sha256, rc, mốc giờ, tiến độ, nhật ký có trần, RAM đỉnh, số lần chạy lại). Gom đòi đủ
866:   # thành viên + đúng head + đường găng <= 540 s. full_mutant_audit (52 ca dưới MỖI đột biến) chạy riêng ở
867:   # `ci-dot-bien-du.yml` trên đúng SHA ứng viên, BẮT BUỘC trước merge/land/release.
868:   gate-nhanh-manh:
869:     needs: chuan-bi
gate-nhanh-manh has Windows rows and targeted mutants: "no mutation radius" in the new text is scoped to cong_cu_test, not every mutation test in the repository.
Same PR branch head alone does not establish same tested checkout: PR may test synthetic merge; dispatch tests selected ref. Need exact checkout/head/tree/runtime evidence per protocol 10.2.2.
No current native Windows execution, GitHub API jobs/logs, actual Ubuntu mutant killing, or exact paired-run provenance was measured here (offline read-only review).
probe_rc=0
```

  kết luận   : KHÔNG PHẢI LỖI ở yêu cầu cùng head và giới hạn cong_cu; cần checkout identity để áp dụng. KHÔNG ĐO ĐƯỢC kết quả Windows/Ubuntu thật hay paired-run identity trên reviewed_sha.

HƯỚNG 12: Kiểm gợi ý vá trong cây riêng

  giả thuyết : HINT.patch áp được bằng patch -p0 từ gốc cay-kho, chỉ đổi lời khai ca nền.
  lệnh       : sao CLAUDE.md sang evidence/hint-check; patch --dry-run -p0 rồi patch -p0 ở bản sao.
  output     :

```text
$ patch --dry-run -p0 < ../../HINT.patch (cwd=evidence/hint-check)
checking file CLAUDE.md
rc=0
$ patch -p0 < ../../HINT.patch (cwd=evidence/hint-check)
patching file CLAUDE.md
rc=0
scratch CLAUDE.md matches intended text=True
patch_paths=[CLAUDE.md]; original cay-kho/CLAUDE.md unchanged=True
```

  kết luận   : KHÔNG PHẢI LỖI ở patch: áp/dry-run rc=0 trên BẢN SAO; chưa áp trên cây thật. Không đổi mã kiểm thử hay tiêu chí dat_windows.

### windows-green-does-not-prove-all-baselines  [P2]  Thu hẹp lời khai ca nền đạt: run xanh vẫn có ca bị bỏ qua

TỆP/DÒNG: `CLAUDE.md:185` (dòng mới), liên quan `CLAUDE.md:182`. Chứng cứ triển khai: `ops/cong_cu_test.py:6008`, `:8893`, `:8897`, `:8909`, `:8916` và `:7905`.

VẤN ĐỀ: “chạy đủ ca nền” rồi kết luận một lượt Windows xanh “chứng minh ca nền đạt” thiếu ranh giới **ca bị bỏ qua chưa được đo**. `main()` có duyệt toàn bộ `CA`, nhưng bắt `BoQuaMoiTruong` riêng và trừ chúng khỏi mẫu số. Nhánh Windows truyền `len(CA)-len(bo_qua)` vào `dat_windows`; các ca bỏ qua không cộng vào số đỏ. Chỉ cần còn ít nhất một ca đo được, không có ca đỏ/tiền kiểm bị bỏ qua và bảng đột biến không rỗng thì vẫn rc=0. Đây là overclaim coverage trong tài liệu, không phải đề nghị đổi chính sách skip của code.

ĐÃ THỬ NGHIỆM: trong `cay-kho/`, `python3 -B ../audit_review.py windows` rc=0. Trích AST nguyên `main`, ba helper Windows, `_doc_che_do`, lớp `BoQuaMoiTruong` và ca **t51 thật**; không import cả module test. Dùng `_TEN_NEN='nt'`, env mảnh 0 thật từ YAML; hai ca pass giả, hai tiền kiểm giả đạt và Path giả không có /bin/sh. Kết quả:

```text
BỎ QUA t51_cache_phai_HET_HIEU_LUC_khi_chinh_TEP_ung_vien_doi: nền này không có `/bin/sh` để dựng ứng viên giả — KHÔNG ĐO ĐƯỢC
cong_cu_test: 2/2 đạt; tổng=3, bỏ qua=1, tiền kiểm bỏ qua=0
scenario REAL t51 absent-/bin/sh rc= 0 events= ['first', 'last']
```

Đối chứng: all-pass rc=0; một ca đỏ rc=1; tất cả ca bị bỏ qua rc=1. Spy không có lời gọi đột biến/ghi mảnh. Đã đo luồng và điều kiện bằng giả lập trên Linux, **KHÔNG ĐO ĐƯỢC** số ca bỏ qua của Windows runner thật tại reviewed_sha (không mạng/runner Windows). Không biến giả lập thành lời khai đã chạy native Windows. Protocol §10.2.3 (`docs/PROTOCOL_DA_PHIEN.md:970`) yêu cầu giữ `passed`, `skipped`, `not_measured` riêng; bài học lane cloud tại `CLAUDE.md:914` cũng lưu số ca bỏ qua theo nền.

GỢI Ý VÁ — bốn phần:

- **Ở đâu:** hai câu mới tại `CLAUDE.md:182` và `:185`, vì vấn đề nằm ở lời khai về phép đo, không ở `dat_windows`.
- **Thế nào:** viết “duyệt toàn bộ ca nền” và nói rõ ca thiếu năng lực vẫn có thể BỎ QUA; run xanh chỉ chứng minh các ca không bị bỏ qua đạt, cần ghi riêng danh sách BỎ QUA. `HINT.patch` chỉ đổi hai câu này, dạng `patch -p0` từ gốc `cay-kho/`.
- **Phép thử khóa:** giữ phản chứng AST “2 đạt + t51 bỏ qua → rc=0”, đối chứng “1 ca đỏ → rc=1” và “tất cả bỏ qua → rc=1” khi đối chiếu lời văn. Đây là phép thử coverage đã chạy, không phải test chỉ so chuỗi tài liệu; chưa có cổng tự động nào kiểm được ngữ nghĩa câu tiếng Việt. Không thêm test repo cho thay đổi lời văn nhỏ này.
- **Nguy cơ:** đừng đổi chính sách skip thành lỗi để làm câu cũ đúng; có thể gây đỏ oan trên nền thiếu năng lực và mở rộng scope khỏi doc-only. Cũng đừng bỏ yêu cầu baseline đạt cho những ca thực sự chạy hoặc biến thiếu coverage thành pass. Patch được dry-run và áp trên bản sao `evidence/hint-check/` rc=0, **chưa áp trên cây thật**; executor phải tự tái dẫn xuất/đo.

ĐỘ TIN: cao về luồng/điều kiện và việc câu thiếu phạm vi; không có kết luận về kết quả native Windows của một run cụ thể.

## GIỚI HẠN VÀ TRẠNG THÁI GATE

- `passed`: doctrine-scan rc=0, “sạch — đã quét 10 tệp, 0 chỗ chép doctrine”; doc-claims-check rc=0, `"ok": true`, 113 tệp, 0 flags, 381 advisory lịch sử, không lớp nào skipped.
- `passed`: các probe cục bộ và phép áp hint trên bản sao; không phải full suite/Windows parity.
- `not_run` / `not_measured`: workflow GitHub mới, native Windows, actual job skipped, bán kính đột biến Ubuntu trên head này, cặp run cùng checkout identity. Không gọi mạng theo nhiệm vụ.
- Không có P0/P1. Không báo finding cho con số 6 (đúng), câu lịch sử hai nền có ngày/SHA (đúng tại mốc đó), hoặc giả định `exclude` tự gây lỗi trước job.if (chưa có bằng chứng đó).

HƯỚNG 13: Kiểm trạng thái cuối và hiện vật

  giả thuyết : cây reviewed vẫn nguyên, hai hiện vật đủ cấu trúc và hint chỉ chạm tài liệu.
  lệnh       : các lệnh Git dưới đây chạy tại cay-kho/; Python đọc cấu trúc VERDICT.md và đường dẫn HINT.patch ở thư mục cha.
  output     :

```text
$ git rev-parse HEAD
8d5cccbb13b0b2c5ba1c9bbc4f8af410a19f87b8
rc=0
$ git status --porcelain=v1 --untracked-files=all
(stdout rỗng)
rc=0
$ git diff --exit-code
(stdout rỗng)
rc=0
$ git diff --cached --exit-code
(stdout rỗng)
rc=0
$ git hash-object CLAUDE.md
44b0bd119b9f521895ce4059a5d0fca057b638c0
rc=0
$ git rev-parse HEAD:CLAUDE.md
44b0bd119b9f521895ce4059a5d0fca057b638c0
rc=0
artifact_structure=passed
HINT.patch sha256=abfeaa000582a7169640e85307e0824c4ca0f7b8aeb3e87090c04d966cdc6109
```

  kết luận   : KHÔNG PHẢI LỖI: HEAD và blob CLAUDE.md khớp, worktree sạch, diff index/worktree rỗng, hiện vật đủ cấu trúc.

