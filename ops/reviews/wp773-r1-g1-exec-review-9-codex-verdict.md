Reviewed commit: 8b496f9e9909496ab6a66e502ed334e31b24c3b1

verdict: approve
P1=0 P2=0 P3=0

Reviewer: Codex, họ model OpenAI, provider `openai_codex`; execution surface coding-agent sandbox, transport shell/tool trực tiếp (`machine`). Phiên độc lập với executor Claude. Không tự chứng nhận launcher, receipt hoặc assurance `human_audited`. Tree: `a7269e1451ab25b3236ba8874fc95eccbb02ac3f`. Review g1, lượt 9, trên exact head nêu trên; KHO chỉ đọc.

## Finding

Không có finding mới được xác nhận. F01 P3 lượt 8 đã đóng bằng phép đo: c06 mới kiểm cả hai chiều quy đổi với offset khác 0, không chỉ nhận dạng cách viết múi giờ.

Đột biến bỏ quy đổi tất cả offset bị giết bởi trường hợp `03:00+0100` (=02:00Z, trước merge). Để loại khả năng ca này che mất chốt offset âm, tôi chạy thêm đột biến **chỉ bỏ quy đổi khi offset âm**: c06 trả **rc=3 + `DO:c06_l3_luot2_moc_sau_merged_at:`**, đúng assertion `02:00-01:00` phải ĐỎ nhưng mutant cho ĐẠT. Không có traceback hoặc rc=4. Chi tiết neo/thay, lệnh và kết quả nằm trong [script](evidence/measure.py), [mutation toàn bộ offset](evidence/mutation-tz.log), [mutation chỉ offset âm](evidence/mutation-tz-negative-only.log).

Vá `93ef97e..8b496f9` chỉ đổi test và thêm mutation, không đổi validator; không thấy mở lại lỗi thực thi đã đóng. Đã đọc lại toàn bộ hai tệp và diff so `1022a33`, đối chiếu L1–L5, Q1–Q6 và bảng nghiệm thu.

## Đã đo

Quy ước: `KHO=/home/user/rv773`; `SP=/tmp/claude-0/-home-user-tra-luat/25822fa2-ac40-52b8-b361-6687f0dd1ccb/scratchpad`. Mọi Python chạy với `PYTHONDONTWRITEBYTECODE=1` và `-B`. Script bằng chứng ghi rõ lệnh con, đầu vào, rc và stdout/stderr; chỉ tạo cây trong `/tmp` hoặc thư mục ra.

- `sha256sum /home/user/rv773-spec-r1.md` ⇒ rc=0, đúng `063ccaa692372d8f431af07fcb86acccef32435e4b69e7a63e3b0a4ee67e02dd`. Đọc spec trước diff. `git -C KHO rev-parse HEAD` và `git -C KHO rev-parse HEAD^{tree}` ⇒ rc=0, đúng head/tree ở trên. Đọc `AGENTS.md`, ngữ cảnh, protocol, CLAUDE và hợp đồng đa provider liên quan; đối chiếu verdict các lượt trước.
- `git -C KHO diff 1022a33 HEAD` ⇒ rc=0, [diff đầy đủ](evidence/full.patch); `git -C KHO diff 93ef97e 8b496f9` ⇒ rc=0. `git -C KHO diff --numstat 1022a33 HEAD` ⇒ rc=0: **2 tệp / 723 dòng thêm; trần ngoại lệ 750 theo prompt lượt này**. Write set đúng g1. [Numstat](evidence/numstat.log).
- `python3.13 -B KHO/ops/land_evidence_nguon_test.py` ⇒ **rc=0; CA 14/14; DOT BIEN 37/37 bi giet dung ly do; TU KIEM PHAN HANG DAT (2); TONG DAT**. [Log 3.13](evidence/test-3.13.log).
- Với `v=3.11,3.12,3.14`: `PYTHONPATH=$SP/yaml-python$v python$v -B KHO/ops/land_evidence_nguon_test.py` ⇒ **cả ba rc=0**, cùng 14/14, 37/37, tự kiểm đạt và tổng đạt. Đã đợi cả ba tiến trình kết thúc. [3.11](evidence/test-3.11-absolute.log), [3.12](evidence/test-3.12-absolute.log), [3.14](evidence/test-3.14-absolute.log).
- Lần chạy đầu ba Python phụ dùng `PYTHONPATH=../yaml-python<v>` ⇒ **rc=1**, c14 đổi cwd nên không tìm thấy PyYAML trong subprocess: 13/14, 35/37, tổng đỏ. Đây là lỗi cấu hình lệnh reviewer; đã sửa thành đường dẫn tuyệt đối như prompt yêu cầu và chạy lại toàn bộ. Giữ log lỗi tại `evidence/test-3.11.log`, `test-3.12.log`, `test-3.14.log`; không tính chúng là pass hay finding của mã.
- `python3.13 -B KHO/ops/land_evidence_nguon.py --root KHO` ⇒ **rc=0; 0 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 28; TỔNG: ĐẠT**. [Log](evidence/tree.log).
- `python3.13 -B evidence/measure.py` ⇒ **rc=0**. Script chạy `git -C KHO archive <c> ops/land` (đều rc=0), giải nén ngoài KHO rồi chạy validator `--root <tmp> --tep ops/land/pr765-wp743-land-evidence.yaml`: `c6e2401` ⇒ **rc=1, 2 L1**, gồm `khong_xung_dot`; `1a4c417` ⇒ **rc=1, 1 L1 + 2 L2 + 1 L3**, mốc 02:58:54Z sau 02:58:26Z; `d60b9e6` ⇒ **rc=1, 1 L1 tại `$.spec.nguon`**. [Lượt 1](evidence/history-c6e2401.log), [lượt 2](evidence/history-1a4c417.log), [lượt 3](evidence/history-d60b9e6.log).
- Trong module riêng ở bộ nhớ, đặt `MIEN_TRU_CUTOVER={}` rồi gọi `main(['--root', KHO])` ⇒ **rc=1, 16 ĐẠT, 12 ĐỎ, 82 vi phạm toàn L1, 0 KHÔNG ĐO ĐƯỢC**. [Log](evidence/no-exempt.log).
- Dựng ảnh cutover độc lập bằng `git ls-tree -r --name-only c73af7b ops/land` và `git show c73af7b:<path>` (đều rc=0): **28 tên**, băm từng blob khớp dictionary; fingerprint `5311e7557cd75ef2f3b06371c66a4830d4970613c1e98a8fd4af732d7dab2257` khớp hằng kỳ vọng riêng trong test. Mutation đổi tên `plat-x8` thành `plat-x9` ⇒ **rc=3 + đúng DO:c10**. Mutation thêm tên nằm trong 37/37 chính thức. c09 kiểm băm khớp rồi đổi một byte; c11 đòi đúng m=k=28. [Mutation đổi tên](evidence/mutation-rename.log).
- Mutation bổ sung bỏ kiểm nội dung L2 ⇒ **rc=3 + đúng DO:c05**, metadata không có token số bị phát hiện; mutation offset nêu trên cũng rc=3 đúng ca. Tất cả chạy qua `LAND_EVIDENCE_NGUON_MA=<bản sao /tmp>` và `--mot-ca <tên ca>`, không sửa KHO. [L2](evidence/mutation-l2-content.log).
- Probe CLI riêng: khóa YAML trùng ⇒ **rc=2**; `nguon_positive: 123` ⇒ **rc=1 L2**; `positive: 123` có nguồn thật ⇒ **rc=0**; mốc trong khóa mapping ⇒ **rc=1 L3**; mốc phân số `.001Z` sau merge ⇒ **rc=1 L3**; `02:00-01:00` ⇒ **rc=1 L3**, `03:00+01:00` ⇒ **rc=0**. Hai nguồn chứa riêng `195/195` và `hong 0` ⇒ **rc=0**. Symlink nội bộ tới nguồn thật ⇒ **rc=0**, tới chính hồ sơ ⇒ **rc=1 L2**. Từng argv/rc/stdout trong `evidence/probe-*.log`, [tổng hợp](evidence/measure.log).
- c01–c08/c14 còn đo glob có/rỗng/sai loại, thư mục, token thoát cây có sẵn c03, precedence từng cặp nền Q3, tự trỏ hồ sơ/thư mục chứa nó, `pre_merge_checks` dạng dict, readback lân cận, ngày sai, YAML trùng/null/merge/alias/kiểu ngoài mô hình, lỗi đọc nguồn và readback mâu thuẫn. Không thấy ca trả sớm bỏ đo. c01 kiểm L2 tự trỏ không dựa vào một lỗi L1 đi kèm.
- Đọc cơ chế `chay_ca`, `chay_dot_bien`, `phan_hang`: bản gốc phải xanh trước; chỉ rc=3 với đúng `DO:<ca>:` được tính GIET; rc=4 là tín dụng giả. Tự kiểm lỗi KeyError và thay đổi vô hại đều đạt trên bốn Python. Không thấy mutation chính thức chết vì lỗi vô can mà vẫn được tính giết; mỗi luật L1–L5 có mutation đúng ca.
- `ruff check --no-cache --select F KHO/ops/land_evidence_nguon.py KHO/ops/land_evidence_nguon_test.py` ⇒ **rc=0, All checks passed**, F delta=0 vì hai tệp mới không có lỗi F. `git -C KHO diff 1022a33 HEAD --check` ⇒ **rc=0**. [Ruff](evidence/ruff.log), [diff-check](evidence/diff-check.log).
- `git -C KHO status --porcelain --ignored` trước/sau ⇒ rc=0, đều rỗng; `cmp evidence/status-before evidence/status-after` ⇒ **rc=0**. Không ghi vào KHO.

Các tiêu chí nghiệm thu g1 đã đo đều đạt: cây thật m=k, tái dựng L1/L2/L3 cả chiều xanh/đỏ, ba trạng thái L4, cutover L5, mutation mỗi luật, ba head thực địa, lint và diff-check. Không tìm được chốt thiếu coverage đủ để xác nhận thêm P3 trong lượt này; kết luận không có nghĩa bộ test bao phủ mọi biến thể có thể tưởng tượng.

## Lựa chọn đã khai và ngoài phạm vi — không tính P3

Docstring khai đúng giới hạn: L1 chỉ kiểm tồn tại, L2 chỉ kiểm các token số, không chứng minh ngữ nghĩa câu văn. `positive` kiểu số vẫn phải có nguồn, nhưng `123` không chứa token `N/M` hoặc `hong N`. `measured` không phân biệt hoa thường, loại tự trỏ và từ chối YAML merge/alias/kiểu ngoài mô hình đều là lựa chọn đã khai và có phép đo.

Chọn readback đúng PR theo tên hồ sơ có giải thích trong hàm và c07 kiểm việc loại readback lân cận; không tính là sai lệch spec cần sửa. `measured - ./` với provenance rỗng hiện hữu ⇒ rc=0: token phân giải về provenance trước, không phải thư mục chứa hồ sơ; Q3 cho nguồn thư mục và L1 không đo ngữ nghĩa. Không suy rằng mọi token `./` đều bị cấm từ ví dụ trong docstring.

G2 nối CI chưa thuộc write set g1. Packet tổng thể vẫn cần g2; approve g1 này không xác nhận packet đã hoàn tất hoặc đã được phép land.

## KHÔNG ĐO ĐƯỢC

- Không xác minh GitHub issue, lease, ngoại lệ kích thước hay required checks từ xa; dùng spec đã kiểm băm, Git OID và authority trực tiếp trong prompt (trần lượt này 750). Không xác nhận launcher, review receipt, model/effort từ receipt bên ngoài hoặc assurance land.
- Không soạn token thoát cây hay mã tấn công mới; chỉ chạy token có sẵn ở c03. Symlink bổ sung chỉ trỏ nội bộ cây tạm. Lỗi đọc được đo bằng mock c08; không suy sang mọi filesystem, OS hoặc quyền truy cập.
- Không chạy toàn bộ CI/repo hoặc g2; không kiểm ngữ nghĩa nội dung nguồn. Probe/mutation bổ sung dùng Python 3.13; bộ chính đã chạy đủ 3.11–3.14 với PyYAML như chỉ dẫn.
