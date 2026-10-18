Reviewed commit: a5dc392b0ad2bec3b1277f5f41665ca176982c43

verdict: approve
P1=0 P2=0 P3=1

Reviewer: Codex, provider OpenAI, thực thi shell/tool trực tiếp trong sandbox của phiên review, độc lập với executor Claude. Tree `0830482b3b257627ede7af48612a298952e2f0a8`. Vai read-only với KHO; không tự chứng nhận launcher, receipt hoặc assurance `human_audited`. Ngưỡng áp dụng: approve khi P1=P2=0. Trần 700 và review không giới hạn lượt lấy từ chỉ thị người dùng; g1 không đồng nghĩa packet đã xong g2.

## Finding còn mở

### F07 — P3 — `ops/land_evidence_nguon_test.py:136`: chưa canh thứ tự ưu tiên phân giải nguồn Q3

Các ca có đo từng nền phân giải, nhưng chưa đặt cùng tên tệp ở hai nền với nội dung khác nhau. Đảo vòng lặp tại `ops/land_evidence_nguon.py:108` từ `(prov, goc / THU_MUC, goc)` sang `(goc, goc / THU_MUC, prov)` trên bản sao `/tmp/rv773-r5-priority.py`: **14/14 ca riêng vẫn rc=0**. Đây là mutation sống, không phải chết vì lỗi vô can.

PHÉP ĐO: `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/extra.py > evidence/extra.log` ⇒ rc=0. Script gọi test qua `LAND_EVIDENCE_NGUON_MA=<bản sao> --mot-ca <từng ca>`, lưu từng lệnh/rc ở [extra.json](evidence/extra.json). Đối chứng riêng: hồ sơ có `positive: '1/1'`, `nguon_positive: result.txt`; provenance chứa `result.txt` với `2/2`, gốc chứa tệp cùng tên với `1/1`. **Head rc=1 L2**, đúng ưu tiên Q3; **mutation rc=0** vì chọn nhầm nền. [Log](evidence/extra.log).

Không phải fail-open hiện hữu trên head; không vi phạm ngưỡng nghiệm thu tối thiểu một mutation mỗi L1–L5, nên không chặn approve. Owner đề nghị: executor/bảo trì test #773. HINT: thêm ca trùng tên nguồn ở provenance và gốc với số trái nhau, đo cả hai chiều đổi nội dung; thêm mutation đảo ưu tiên và đòi rc=3 cùng `DO:<ca>:`.

## Vá lượt 5

F06 lượt 4 **đóng**. `evidence/regression.py` được chép nguyên từ lượt 4: chạy lại trên 3.11–3.14 đều **rc=0** cho bốn tổ hợp root/file tương đối/tuyệt đối. c14 CLI thật cũng xanh. Mutation bỏ resolve gốc trong bộ chính thức bị c14 giết đúng lý do. Probe riêng root chứa đoạn `..` để trở về chính cây thử và `--tep` qua symlink thư mục nội bộ đều **rc=0**, đủ hai dòng tổng kết; không ném ValueError. Không soạn đường dẫn thoát cây mới.

Khoảng trống readback mâu thuẫn lượt 4 đã được thêm ca và mutation. Chạy lại `evidence/conflict.py` nguyên từ lượt 4 ⇒ script rc=0: **head rc=2**, lý do hai `merged_at` khác nhau; bản sao bỏ chốt cũ **rc=0**. c14 hiện đo tên hồ sơ không `pr<N>-`, kiểm cả rc=2 và thông báo mâu thuẫn; mutation chính thức bỏ chốt này đã bị giết. [Đối chứng](evidence/conflict.log).

## Đã đo

Quy ước: `KHO=/home/user/rv773`; `SP=/tmp/claude-0/-home-user-tra-luat/25822fa2-ac40-52b8-b361-6687f0dd1ccb/scratchpad`. Python dùng `-B`/`PYTHONDONTWRITEBYTECODE=1`. Bản sao và cây dựng nằm ngoài KHO. Các script evidence ghi lệnh con; kết quả dưới đây là phép chạy của reviewer.

- `sha256sum /home/user/rv773-spec-r1.md` ⇒ rc=0, đúng `063ccaa692372d8f431af07fcb86acccef32435e4b69e7a63e3b0a4ee67e02dd`. Đọc spec L1–L5, Q1–Q6, nghiệm thu; AGENTS và tài liệu repo liên quan; verdict trước; toàn bộ hai tệp và diff. `git -C KHO rev-parse HEAD HEAD^{tree}` ⇒ rc=0, đúng head/tree trên. `git -C KHO diff c73af7b a5dc392` ⇒ rc=0, lưu [diff.log](diff.log); đọc riêng `git -C KHO diff a3cfc53 a5dc392` ⇒ rc=0.
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B KHO/ops/land_evidence_nguon_test.py` ⇒ **rc=0, CA 14/14, DOT BIEN 31/31 giết đúng lý do, TU KIEM PHAN HANG DAT (2), TONG DAT**. [3.13](tests-3.13.log).
- Với `v=3.11,3.12,3.14`: `PYTHONPATH=$SP/yaml-python$v PYTHONDONTWRITEBYTECODE=1 python$v -B KHO/ops/land_evidence_nguon_test.py` ⇒ **cả ba rc=0**, cùng **14/14, 31/31, tự kiểm đạt, tổng đạt**. [3.11](tests-abs-3.11.log), [3.12](tests-abs-3.12.log), [3.14](tests-abs-3.14.log). Lần đầu dùng `PYTHONPATH=../yaml-python$v` ⇒ cả ba rc=1 do c14 đổi cwd làm tiến trình con thiếu PyYAML; log `tests-3.11.log`, `tests-3.12.log`, `tests-3.14.log`. Đã sửa cách chạy bằng đường dẫn tuyệt đối, không sửa mã KHO; không tính lần đầu là lỗi implementation hay mutation giết thật.
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/measure.py > evidence/measure.log` ⇒ script **rc=0**. Script chép từ lượt 4, chỉ đổi head diff sang `a5dc392` và thư mục archive tạm sang `rv773-r5-history`. [Kết quả](evidence/measure.log), [script](evidence/measure.py).
- Lệnh con `python3.13 -B KHO/ops/land_evidence_nguon.py --root KHO` ⇒ **rc=0: 0 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 28; TỔNG ĐẠT**. [Cây thật](evidence/tree.log).
- Với `c=c6e2401,1a4c417,d60b9e6`: `git -C KHO archive <c> ops/land` ⇒ mỗi lệnh rc=0; giải nén vào `/tmp/rv773-r5-history/<c>`. `python3.13 -B KHO/ops/land_evidence_nguon.py --root <tmp> --tep ops/land/pr765-wp743-land-evidence.yaml` ⇒ **mỗi lệnh rc=1**. Lần lượt **2 L1**, gồm `khong_xung_dot`; **1 L1 + 2 L2 + 1 L3**, mốc 02:58:54Z ≥ 02:58:26Z; **1 L1 tại `$.spec.nguon`**. [c6e2401](evidence/history-c6e2401.log), [1a4c417](evidence/history-1a4c417.log), [d60b9e6](evidence/history-d60b9e6.log).
- Trong `measure.py`, import module riêng, đặt `MIEN_TRU_CUTOVER={}` trong bộ nhớ rồi gọi `main` ⇒ **rc=1, 16 ĐẠT, 12 ĐỎ, 82 vi phạm toàn L1, 0 KHÔNG ĐO ĐƯỢC**. [Không miễn trừ](evidence/no-exemption.log). Đọc độc lập blob base bằng `git ls-tree --name-only c73af7b ops/land/` và `git show c73af7b:<path>` ⇒ **28 tên**, fingerprint `5311e7557cd75ef2f3b06371c66a4830d4970613c1e98a8fd4af732d7dab2257`, khớp hằng test. Hằng này không tính lại từ dictionary đang kiểm.
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/probes.py > evidence/probes.log` ⇒ **script rc=0**. Hai ca merge trùng chuỗi/null và ngày sai không nháy ⇒ **rc=2**, không traceback; nguồn thường/glob/thư mục ⇒ rc=0; mapping pre-merge có timestamp ở khoá ⇒ **rc=1 L3**; mốc phân số sau merge ⇒ **rc=1 L3**; symlink nguồn nội bộ ⇒ rc=0; root tương đối/file tuyệt đối ⇒ rc=0. `positive: 123` với nguồn thật ⇒ rc=0 (không có token L2 cần so). Mốc offset có nháy ⇒ rc=0, ngoài regex Z đóng băng của spec. [Từng đầu vào/rc](evidence/probes.json).
- Cũng trong `probes.py`: độ sâu 100,300,450,480,490 qua loader và walker; 495,500,600,1000 ném RecursionError ở loader. Mutation bổ sung bỏ riêng so nội dung L2 trên bản sao `/tmp/rv773-r4-l2-content.py`, chạy `--mot-ca c05_l2_luot2_positive_phai_co_nguon_chua_nguyen_van` qua `LAND_EVIDENCE_NGUON_MA` ⇒ **rc=3 + đúng `DO:c05...:`**.
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/regression.py` ⇒ **rc=0**. `extra.py` còn gọi `PYTHONPATH=$SP/yaml-python$v PYTHONDONTWRITEBYTECODE=1 python$v -B evidence/regression.py` cho v=3.11–3.14 ⇒ **bốn rc=0**. `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/conflict.py` ⇒ **script rc=0**, đối chứng head/mutation như trên.
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/extra.py > evidence/extra.log` ⇒ **rc=0**. Ngoài F07 và probe đường dẫn, mutation đổi tên `plat-x8` thành `plat-x9` chạy `--mot-ca c10_l5_danh_sach_dong_bang` ⇒ **rc=3 + đúng `DO:c10...:`**. Mutation thêm tên chính thức cũng bị giết. c09 đo băm khớp rồi sửa một byte mất miễn trừ; c11 đòi đúng **m=k=28**.
- `ruff check --no-cache --select F KHO/ops/land_evidence_nguon.py KHO/ops/land_evidence_nguon_test.py` ⇒ **rc=0**, All checks passed, F delta=0 (hai tệp mới). `git -C KHO diff --check c73af7b a5dc392` ⇒ **rc=0**. `git -C KHO diff --numstat c73af7b a5dc392` ⇒ **rc=0: 2 tệp / 694 dòng thêm; trần ngoại lệ 700 theo prompt**. Write set đúng, không sửa workflow/hồ sơ cũ.
- `git -C KHO status --porcelain --ignored > status-before` và lệnh tương tự cho `status-after`; `cmp status-before status-after` ⇒ **rc=0**, KHO không đổi.

## Đối chiếu phạm vi và nghiệm thu

Không phát hiện fail-open hiện hữu trên head trong các phép đo đã chạy. Các chốt nghiệm thu g1 về cây thật, dựng lại L1/L2/L3, chuyển post-merge, đổi số nguồn, YAML lỗi/provenance vắng, băm lệch, thêm/đổi tên miễn trừ, m=k, mutation từng L1–L5, thực địa lịch sử, lint và diff-check đều đạt. Không thấy mutation chính thức được đếm giết bằng rc=4 hoặc thiếu `DO:<ca>:`; bộ phân hạng có đối chứng KeyError vô can và thay đổi vô hại. c14 kiểm subprocess thật, còn ca readback tên chung dựng đúng provenance tương ứng nên không xanh nhờ miễn trừ hoặc thiếu nhánh.

Docstring khai rõ L1 chỉ kiểm tồn tại, L2 chỉ so token số và không xác minh ngữ nghĩa bằng chứng. So `measured` không phân biệt hoa thường và loại tự trỏ hồ sơ được khai và đo. Chọn readback theo PR trong tên hồ sơ được khai tại hàm, c07 đo việc loại readback lân cận; hợp lý với cấu trúc thực địa này. Mốc có nháy dạng offset không thuộc regex Z của đặc tả; phân số Z được hỗ trợ thêm và đã đo. Từ chối merge/alias/kiểu YAML ngoài mô hình bằng rc=2 là giới hạn được khai, không phải ĐẠT ngầm. F07 là nợ tăng độ phủ, không phải thiếu điều kiện nghiệm thu bắt buộc.

## KHÔNG ĐO ĐƯỢC

- Không xác minh issue/lease/ngoại lệ kích thước trên GitHub; dùng chỉ thị trực tiếp trong prompt về trần 700 và số lượt. Không xác nhận g2 đã nối CI hoặc land, launcher/receipt hay assurance land. Verdict này chỉ xét nội dung g1 exact head.
- Không soạn đường dẫn thoát cây hoặc mã khai thác mới, không dựng symlink thoát gốc. Chạy c03 hiện hữu nguyên trạng; bổ sung symlink nội bộ và chuẩn hoá root trong cây thử. Không tuyên bố vét hết lỗi filesystem/quyền truy cập; lỗi đọc nguồn L2 được test đo bằng mock.
- Không chạy toàn bộ test repo/CI hoặc kiểm ngữ nghĩa nguồn chứng minh câu văn (ngoại phạm vi). Độ sâu bổ sung lượt này đo trên 3.13; bộ chính thức chạy cả bốn Python. Không suy kết quả này cho mọi parser, cấu hình recursion limit hay nền hệ điều hành.
