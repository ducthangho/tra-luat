verdict: changes_requested
reviewed_sha: bc3bbb5d207507779eab4ca88d6be6b539791a58
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1051, lượt 13. Các phản chứng lượt 11–12 đã bị chặn; ca t27 có răng trên 33 đột biến riêng. Còn một điểm P2 qua đọc mã theo yêu cầu (b): cho phép toàn bộ nhóm `So` vẫn cho phép tiền tố mang thêm chữ.

## F1 — P2 — `wp1006-case-insensitive-listing-case-sensitive-consumer` — tiền tố chữ thuộc nhóm So

**Tệp:dòng:** [ops/lease_publish_test.py:1648](cay-kho/ops/lease_publish_test.py#L1648), điều kiện `lay` trong `_bang`; dòng 1649 cho phép mọi ký tự thuộc `So`/`Sc`.

Đây đúng là **danh sách cho phép**, đã loại được ký tự định dạng `Cf` như RLO. Tuy nhiên, nó chưa đủ hẹp để bảo đảm hợp đồng ngay phía trên: trước tên mục chỉ có ký hiệu trang trí, **không thêm chữ**. `So` không đồng nghĩa với ký hiệu không mang chữ. Nó chứa nguyên các bảng chữ Latin khoanh tròn/đóng khung, gồm:

- U+24B6–U+24CF: chữ Latin hoa khoanh tròn;
- U+24D0–U+24E9: chữ Latin thường khoanh tròn;
- U+1F130–U+1F149: chữ Latin hoa đóng khung;
- U+1F150–U+1F169 và U+1F170–U+1F189: các bộ chữ tương ứng trên nền kín.

Đã kiểm riêng từng codepoint bằng `unicodedata` của Python đang chạy: **130/130 là `So`**. Các bộ chữ này được mô tả trong bảng chính thức [Enclosed Alphanumerics](https://www.unicode.org/charts/PDF/U2460.pdf) và [Enclosed Alphanumeric Supplement](https://www.unicode.org/charts/PDF/U1F100.pdf). Ví dụ ở mức ký tự riêng: U+24B6 có tên `CIRCLED LATIN CAPITAL LETTER A`, U+1F130 có tên `SQUARED LATIN CAPITAL LETTER A`; NFKC của từng ký tự là chữ A. Đây là bằng chứng về bảng chữ, **không phải** tuyên bố renderer chuẩn hóa NFKC.

**Mô tả và tác động:** một dãy chữ từ các bộ này có thể viết thêm từ ở trước tên mục. Mọi ký tự trong dãy vẫn qua `all(...)`; điều kiện còn lại chỉ đòi hậu tố bằng tên mục, không giới hạn dãy ấy vào vài ký hiệu đã biết. Do đó `_bang` vẫn có thể chọn một tiêu đề mang thêm chữ, rồi `_kiem_muc_luc` công nhận bảng thuộc mục cần kiểm. Cùng loại tiền tố viết bằng chữ Latin thường đã bị ca `tieu_de_chu_khac_dung_truoc` từ chối. Phân loại Unicode đã thay thế việc xác định tiền tố trang trí, nên lớp chọn sai tên mục chưa đóng hết. Đây không phải lỗi RLO còn lọt, cũng không phải bypass validator receipt v2.

**Tái hiện/ranh giới bằng chứng:** đúng chỉ thị (b), tôi chỉ nêu nhóm ký tự bằng lời, kiểm thuộc tính từng ký tự và đọc đường điều kiện; **không ghép một heading tấn công mới, không dựng fixture mới cho F1**. Kết luận nhận tiền tố suy ra từ điều kiện `endswith` cộng `all(category in ...)`. Bằng chứng thuộc tính nằm ở [unicode-audit.json](review-evidence/unicode-audit.json). Chưa đo CLI/render của một từ ghép bằng bảng chữ này; Executor tự dựng phản chứng theo nhóm nêu trên. Các kết quả CLI bên dưới chỉ thuộc những đầu vào lịch sử đã chạy.

**Đề xuất đủ bốn phần:**

1. **Vá ở đâu:** tại phép chọn tiêu đề trong `_bang`, dòng 1647–1649, vì đây là nơi quyết định một bảng thuộc tên mục nào; `_ten_tep` và validator receipt không giải quyết được sai tên tiêu đề.
2. **Vá thế nào:** dùng tập tiền tố literal nhỏ đã có nhu cầu thật, chẳng hạn không tiền tố hoặc ký hiệu cảnh báo hiện dùng, cùng space/tab được quy định rõ. Không dùng toàn bộ `So`/`Sc` làm đại diện cho “không có chữ”. Đây là hướng rẻ nhất; bộ phân tích chữ hiển thị đầy đủ mua thêm khả năng hỗ trợ cú pháp nhưng tốn phạm vi hơn.
3. **Ca khóa:** Executor dựng tiền tố có từ bằng bảng chữ khoanh tròn/đóng khung cho cả hai mục; helper và CLI t27 phải đỏ. Giữ đối chứng tên thường, ký hiệu cảnh báo thật và dấu `#` đóng xanh. Đột biến mở lại toàn bộ `So` phải làm ca khóa đỏ. Tôi không soạn chuỗi mới cho các ca này.
4. **Nguy cơ bản vá:** tập literal quá chặt có thể từ chối một ký hiệu trang trí hợp lệ được dùng về sau; thêm ký hiệu phải là thay đổi có chủ đích và có đối chứng. Giữ phép so nguyên văn tên mục, tránh chuẩn hóa toàn heading để vô tình gộp các tiêu đề khác nhau.

## Đã đo

Nguồn được giữ read-only. Hai clone hồi quy, fixture, module lịch sử và mutant đều nằm dưới `review-evidence/`, ngoài `cay-kho/`. Các clone có index/refs riêng và đọc object qua alternate; không thao tác ghi vào Git nguồn. Python chạy với `-B`, `PYTHONDONTWRITEBYTECODE=1`; `TMPDIR` nằm ngoài nguồn.

Base đầy đủ: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`. Đã đọc diff toàn PR `git -C cay-kho diff b29da0b HEAD` và diff lượt này `git -C cay-kho diff 12f21b2 HEAD`; chỉ `ops/lease_publish_test.py` thay đổi. Delta lượt 13 là whitelist tiền tố và bốn ca âm khóa nó.

### Chạy lại phản chứng có sẵn

Các script tham chiếu thiếu mô-đun hỗ trợ. Tôi phục dựng harness ngoài kho, giữ các bộ sinh đầu vào của script gốc, đổi kỳ vọng từ “chứng minh xanh sai trên head cũ” thành “phải đỏ trên head này”. Riêng nhánh `prototype` của script lượt 11 đo trực tiếp head hiện tại thay cho bản vá thử của lượt cũ. Có lưu [diff và băm các bản thích nghi](review-evidence/history-adaptations.json); không soạn chuỗi tấn công mới.

| Lệnh đã chạy tại thư mục làm việc | rc | Kết quả |
|---|---:|---|
| `python3 -B review_bidi.py` | 0 | 8/8 fixture lượt 12 đỏ bằng AssertionError; CLI t27 một ca và toàn nhóm đỏ; t26/v2 và sửa đúng xanh. Hai fixture RLO gốc đã đóng. |
| `python3 -B review_current.py` | 0 | 3 ID span dính và 28 delimiter lượt 11 đều đỏ; sửa đúng xanh. |
| `python3 -B review_additional.py headings` | 0 | 6/6 tiêu đề giấu tên trong metadata đỏ; sửa đúng xanh. |
| `python3 -B review_additional.py prototype` | 0 | 12/12 vị trí VT/FF đỏ; sửa đúng xanh qua helper, t26, t27 và v2; kiểm lại 6 heading, README thật và ca khóa xanh. |

Tổng cộng **57 lần dựng fixture lịch sử** trong bốn nhóm trên, có phần đầu vào delimiter trùng nhau giữa các script. Đối với mỗi fixture sai: helper ném `AssertionError`, CLI t27 rc=1, t26 và validator v2 thật rc=0; sửa README đúng thì helper/t26/t27/v2 xanh. Không đổi README bằng CLI. Các script còn đo HTML GFM bằng Pandoc; không tuyên bố đã chạy giao diện GitHub thật.

[8 fixture Unicode](review-evidence/bidi-results.json), [31 fixture ID/delimiter](review-evidence/r11-boundaries.json), [6 heading](review-evidence/heading-findings.json), [12 vị trí VT/FF](review-evidence/extra-delimiters.json), [kết quả bổ sung](review-evidence/prototype-results.json).

### Răng của ca t27

`python3 -B review_mutations.py` — **rc=0**. Control xanh. **33/33 mutant riêng biên dịch được**, giữ nguyên AST của ca đích, làm chính ca `t27_phan_chung_ten_bien_nhan_sai_bi_TU_CHOI_kem_cach_chua_lam_XANH_ca_t26_t27` ném **AssertionError**; mỗi CLI rc=1, **0/1**, bỏ qua 0. Không tính lỗi cú pháp hoặc lỗi import làm giết mutant.

Đã giết riêng từng chốt được yêu cầu:

| Đột biến | Kết quả |
|---|---|
| Quay tiền tố về lớp phủ định | AssertionError, CLI 0/1 |
| Chọn mục bằng chuỗi con nguồn | AssertionError, CLI 0/1 |
| Bỏ chốt comment / bỏ chốt HTML | Mỗi mutant AssertionError, CLI 0/1 |
| Hàng gạch không cần dấu gạch / không cần đúng số ô | Mỗi mutant AssertionError, CLI 0/1 |
| Bỏ chốt đoạn văn trước bảng | AssertionError, CLI 0/1 |
| Bỏ ngữ pháp ô tên / bỏ ngữ pháp ô ID | Mỗi mutant AssertionError, CLI 0/1 |
| Alias không cần duy nhất | AssertionError, CLI 0/1 |

Các mutant còn lại phủ giữ span ML/CB, pipe thoát, đường dẫn/basename, IGNORECASE, nhãn link, nhãn đuôi, tên có khoảng trắng/ký tự dính, chốt đuôi receipt, gọi chốt tên ở t26/t27, sidecar phân biệt case, tập danh tính alias, tắt alias, dòng trắng Unicode, rào mã, ID dính span, VT/FF và thụt lề. [Runner và cặp thay thế](review_mutations.py), [kết quả/traceback từng mutant](review-evidence/mutations.json), [log driver](review-evidence/mutations-driver.stdout).

### Hồi quy đầy đủ và delta

| Lệnh / phạm vi | rc thật | Kết quả |
|---|---:|---|
| `python3 -B ops/lease_publish_test.py` tại `review-evidence/head/` | 1 | **267/269**, chạy 269, bỏ qua 0; 365,030 s |
| Cùng lệnh tại `review-evidence/base/` | 1 | **266/268**, chạy 268, bỏ qua 0; 364,746 s |
| `python3 -B review_static.py regression` | 0 | Đủ marker vào/ra khớp AST: 269/269 và 268/268; 268 ca chung không đổi trạng thái; thêm đúng ca tên mới xanh. |
| `python3 -B review_static.py real` | 0 | `_bang` head và `12f21b2` trả **cùng toàn bộ hàng/ô**, cả hai chế độ `giu_span`: ML 321, CB 750. Helper cả hai xanh; toàn `t27_` trên README thật rc=0, **3/3**. |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head / base | 1 / 1 | Cùng **7 F401 + 2 F541**; delta nội dung diagnostic = **0**. |
| `python3 -B review_static.py static` | 0 | Xác nhận Ruff delta 0; hai SyntaxWarning cũ `\s`/`\d` không đổi. |
| `git -C cay-kho diff --check b29da0b HEAD` | 0 | Không lỗi whitespace. |
| `python3 -B review_static.py source` | 0 | 8.468 tệp tracked giữ nguyên băm; HEAD/status nguồn không đổi; module trong hai clone khớp byte revision tương ứng. |

**Hai suite đầy đủ đều failed**, không ghi thành N/N đạt. Hai ca đỏ cùng tên và thông báo bằng nhau ở head/base:

- `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck`: thiếu `shellcheck`.
- `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`: chưa tới consumer ShellCheck vì cùng thiếu công cụ.

Phần ShellCheck **not_measured do môi trường**, delta hồi quy PR bằng 0. `t125` A/B xanh ở cả hai. [Delta và lỗi nguyên văn](review-evidence/regression-summary.json), [log head](review-evidence/lease-head.stdout), [log base](review-evidence/lease-base.stdout), [README thật](review-evidence/real-readme.json), [Ruff/warnings](review-evidence/static.json).

Audit thêm các manifest CLI: **307** lượt chọn ca có tổng kết dương khớp rc, **114** lượt validator v2 đều có bằng chứng 1 receipt đạt; không chỉ dựa vào rc. [Số đếm audit](review-evidence/cli-audit-summary.json).

## Tính toàn vẹn và giới hạn

Kiểm cuối: HEAD vẫn đúng reviewed SHA; tree `4b7bfe9c5c57a27347dd27d0047a646be8c5c508`; status kể cả untracked/ignored rỗng; 8.468 tệp tracked khớp snapshot đầu. [Tính toàn vẹn nguồn](review-evidence/source-integrity.json). Kho báo shallow=true, nhưng cả head, base và `12f21b2` cần dùng đều đọc được.

Môi trường Linux, Python 3.13.17, Unicode database 15.1.0, Pandoc 3.1.3, Ruff 0.16.9. Windows thật, CI GitHub và render GitHub thật **not_run/not_measured**. F1 là nhận xét đọc mã theo yêu cầu (b), không phải một fixture mới đã chạy. Không sửa kho Executor, không push, không gọi API ghi GitHub.

Reviewer: OpenAI Codex, phiên API độc lập với Executor; provider `openai_codex`, execution surface `codex_service`, transport `machine`. Không có attestation độc lập cho model ID/effort; không suy danh tính model từ tài khoản vận chuyển verdict.
