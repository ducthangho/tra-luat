# Review Codex offline lượt 1 — packet #1266 THU-HOI-ADMISSION-MERGE-BASE-B r13 g1 (Review Class: sensitive)

Bạn là reviewer ĐỘC LẬP (họ OpenAI). Executor là một phiên Claude khác. Lượt này CHỈ ĐỌC trên thư mục làm việc.

**Không ghi bất kỳ tệp nào trong thư mục làm việc.** Lệnh cấm gồm tệp ignored, `__pycache__`, `.git/**` và `git config`. Lượt chạy bằng `launcher.py run --chup-workspace`; chỉ cần một lần ghi vào cây là cả lượt vô hiệu. Gốc workspace có thể có sẵn hai thư mục rỗng `.aws/` và `.codex/`; đừng xoá chúng.

**Bước đầu tiên:** chạy `git clone --no-hardlinks <thư mục làm việc> /tmp/rv1266-copy`, rồi `git -C /tmp/rv1266-copy checkout --detach 802a5665df9ae512d5b2df125b8e219f496fa9f9` và `git -C /tmp/rv1266-copy config core.abbrev 7`. Mọi lệnh chạy TRONG bản sao (hoặc trong các bản sao tạm khác dưới `/tmp`). Đặt `TMPDIR` và `PYTHONDONTWRITEBYTECODE=1` ngoài cả hai cây. Bản sao có đủ lịch sử (không nông) và có `origin/master`.

## Neo
- HEAD phải là `802a5665df9ae512d5b2df125b8e219f496fa9f9`, tree `e31934fdfd70774abfe444604d27d4510211a037`, cha DUY NHẤT là base `997b383f824ca63d7cee4a659bb6f9cf19bc439f`. Khác ⇒ `request_changes`.
- Đặc tả trong cây: `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-B-r13.md`, sha256 phải là `e8ba54b72abffe80f1177d406b2bbdfa63441b4826ff6b45cbd2f798cb6a7d02`. Tự đo; lệch thì DỪNG và `request_changes`.
- Packet A (ADR-0066) đã land trong base; đọc `docs/adr/0066-admission-thu-hoi-theo-merge-base.md` làm hợp đồng mà B thi hành.
- Write set của lease gồm ĐÚNG năm tệp: `ops/lease_publish.py`, `ops/lease_publish_test.py`, `.github/workflows/ops-thu-hoi-admission.yml` (CHỈ khối chú thích đầu tệp, không đổi bước nào), `.claude/dev/doc_receipt_thu_hoi.py`, `.claude/dev/doc_receipt_thu_hoi_test.py`. Trần: ≤ 6 tệp, ≤ 780 dòng thêm theo `git diff --numstat 997b383..HEAD`.
- Bundle chưa push: chưa có CI, PR, connector. B13 (CI Linux), B14 (Windows), B15 (`ci-dot-bien-du.yml`), B18 (canary sau land) NGOÀI phạm vi lượt này; B17 Linux executor tự đo, bạn chỉ đo lại nếu còn thời gian (mục Việc 5).

## Executor tự khai (đừng tin, đo lại)
- numstat: doc_receipt 41/4 · doc_receipt_test 68/7 · workflow 3/2 · lease_publish 119/5 · lease_publish_test 540/9 ⇒ 771 dòng thêm.
- `ops/lease_publish_test.py` trên H 303/303 (285 nền + 18 ca mới t238–t255, ~500 giây). `.claude/dev/doc_receipt_thu_hoi_test.py` trên H 296/296 ca, 344/344 đột biến giết (nền 270/270 · 318/318).
- Catalog đột biến t139 (gồm `amb-m*` của mục 5.1): mẫu số 37 → 83; 80 giết thật, 3 SỐNG có chủ đích (của A0, có sẵn), 0 tín dụng giả. Mỗi hàng `amb-m*` đòi ca đỏ ở đúng tiền tố khẳng định.
- ruff `--select F` trên 4 tệp .py: H 11 = base 11. `doctrine-scan`, `adr-song` sạch.
- B17 Linux đạt N 10/50/100 (1,1 s · 2,3 s · 17,2 s); số commit bước tô màu đọc 169/367/2874/3828 khớp bảng mục 0.
- Màu trên nền (tệp test của H chạy trên mã base): xanh t129, t151, B9 (t254); đỏ bằng assertion t133, t137, B1–B8b, B10; B5d không đo được trên nền (`AttributeError`, thiếu `to_mau_hai_phia`); 6 ca validator xanh trên nền vì nền cũng từ chối.
- Thiết kế cần soi: `vung_tai_S` chỉ gồm entry trực tiếp dưới `ops/thu-hoi` cộng tệp policy; lọc cực đại duyệt đủ tổ tiên các ứng viên còn lại, chung ngân sách `max_commits_merge_base`, không dùng timestamp để suy quan hệ tổ tiên.
- Chốt cố định đã sửa: t133 (ca con "S không tổ tiên H" nay đòi rc 0 và `merge_base`; thêm ca vùng lệch ⇒ 12 `VUNG_LECH`), t137 (chốt B10), t138 (khoá `ngan_sach` 8 → 9), t139 (khung đột biến thêm neo nhiều chỗ, đột biến trên workflow, tiền tố khẳng định).

## Việc
1. Đọc toàn bộ đặc tả: mục 3 (bảng ba trạng thái), mục 4 (mục tiêu), mục 5 (B1–B18, ma trận nhãn, mục 5.1 bảng ca ↔ đột biến), mục 7 (luật dừng).
2. Đọc diff `997b383..HEAD`, từng hunk.
3. **Tự đo lại** B1–B12 và B16 trong bản sao: chạy các ca mới (`python -u ops/lease_publish_test.py --chi-ca=<tiền tố>`) và toàn bộ `doc_receipt_thu_hoi_test.py`. Với mỗi hàng của mục 5.1, chạy ít nhất đột biến đặc tả nêu trên một bản sao tạm khác, xác nhận ca đích đỏ **đúng ở khẳng định của nó** (không phải lỗi vô can), rồi khôi phục. Đột biến chỉ đổi giá trị (`amb-m34`, `amb-m35`, `amb-m30`, `amb-m31`…) phải được kiểm riêng vế âm.
4. Chạy toàn bộ `ops/lease_publish_test.py` một lần (bằng chứng dương N/N hai số bằng nhau; thiếu `shellcheck` thì ghi rõ ca nào bị ảnh hưởng và đo trên nền xem có đỏ sẵn không).
5. (Nếu còn thời gian) Đo B17 Linux theo đúng mục "Đầu vào của B17" của đặc tả, N ∈ {10, 50}, bằng script của bạn đặt NGOÀI cây.
6. Soi tính đúng của bộ kiểm mới trong `ops/lease_publish.py`: phân nhánh `to_tien` / `merge_base`, tô màu hai phía, lọc cực đại, ngân sách, replace objects (`GIT_NO_REPLACE_OBJECTS`), committer hỏng, ứng viên stale, receipt v2 (khoá, thứ tự, phép chiếu), và validator C1a1a trong `.claude/dev/doc_receipt_thu_hoi.py`. Đối chiếu từng nhánh với bảng ba trạng thái mục 3: mọi đường "không đo được" phải ra rc 12, không bao giờ rc 0.
7. Kiểm khối chú thích workflow (B10) đúng câu đặc tả, và workflow không đổi bước nào (`git diff -U0 997b383..HEAD -- .github/workflows/ops-thu-hoi-admission.yml`).
8. Chạy `python3 -B .claude/dev/packet_loop.py adr-song --root .` và `doctrine-scan --root .`; `python -m ruff check --select F` trên bốn tệp .py ở H và ở base, so delta.

## Giới hạn
- Không gọi mạng. Không push, không đăng gì.
- Không đề xuất sửa tệp ngoài write set. Mức dư dòng chỉ còn 9: finding nào đòi thêm dòng thì nói rõ ước lượng số dòng.
- Hướng thử nào cần tự soạn nội dung dựng đường dẫn thoát khỏi cây hay tương tự thì MÔ TẢ bằng lời, đừng tự soạn.

## Đầu ra
In ra stdout một báo cáo, có ba phần:
- Bảng B1–B12, B16 (và B17 nếu đo): tiêu chí · lệnh · số đo · đột biến đã chạy · kết quả.
- Danh sách finding, mỗi cái gồm: mức P0–P3, tệp:dòng, mô tả, phản chứng chạy được hoặc lý do.
- Đánh giá các lời tự khai ở mục "Executor tự khai": câu nào khớp, câu nào lệch số đo của bạn.

Dòng CUỐI CÙNG của stdout phải là đúng một trong hai: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`.

Chỉ chọn `approve` khi đủ cả hai điều kiện:
- không còn finding P0, P1 hay P2;
- B1–B12 và B16 đều đạt bằng phép đo của chính bạn.
