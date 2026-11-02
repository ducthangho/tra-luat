verdict: approve
reviewed_sha: de55985fcae2984a2038ef1ceca018fc9b5620fa
so_lop: P0 0 / P1 0 / P2 0 / P3 0

Review độc lập PR #1051, lượt 14. Không có finding P0–P3 trong phạm vi được giao. Tập tiền tố literal đã chặn biểu hiện chữ khoanh tròn/đóng khung của lượt 13; các phản chứng lịch sử được yêu cầu đều đỏ, sửa đúng xanh. Hai suite đầy đủ vẫn **failed** vì thiếu ShellCheck ở cả head và base; delta hồi quy bằng 0.

Base: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`. Reviewed tree: `fe7018a1db5175f8e1f59149088d4da66231103e`. Đã đọc diff toàn PR `git -C cay-kho diff b29da0b HEAD` và diff lượt này `git -C cay-kho diff bc3bbb5 HEAD`: chỉ `ops/lease_publish_test.py`; toàn PR +617/−39, lượt này +9/−6. Authority và ngưỡng approval là `PROMPT.md`: phải hết mọi finding P0–P3.

## Finding

Không có finding cần yêu cầu sửa.

## ĐỐI CHIẾU LƯỢT TRƯỚC

F1 P2 lượt 13, lớp `wp1006-case-insensitive-listing-case-sensitive-consumer`: **ĐÃ VÁ THẬT** đối với biểu hiện tiền tố mang thêm chữ thuộc `So`. Tại `cay-kho/ops/lease_publish_test.py:1648`, điều kiện chỉ nhận tên mục nguyên văn hoặc `⚠ ` cộng tên mục.

Đã lấy nguyên ba đầu vào `tieu_de_chu_khoanh_tron`, `tieu_de_chu_dong_khung`, `tieu_de_ky_hieu_khac` từ AST của ca test hiện tại, đưa qua fixture Git/receipt v2 riêng: helper ném AssertionError, CLI t27 một ca và toàn nhóm đều rc=1; t26/v2 rc=0. Sửa tiêu đề đúng làm helper/t26/t27/v2 xanh. Đột biến mở lại toàn bộ `So`/`Sc` cũng bị chính ca t27 đích giết. Không soạn chuỗi tấn công mới. [Runner](review_existing_r13.py), [ba kết quả](review-evidence/existing-r13/existing-r13.json), [mutant tiền tố](review-evidence/mutations.json).

| Nguồn lịch sử | Phạm vi tự chạy trên head | Kết quả |
|---|---|---|
| Lượt 13, SHA `bc3bbb5…` | 31 ID/delimiter + 6 metadata tiêu đề + 12 vị trí VT/FF + 8 Unicode/bidi | 57 đầu vào sai đỏ, sửa đúng xanh |
| Lượt 12, SHA `12f21b2…` | Script bidi nguyên bản, cập nhật kỳ vọng sau vá | 8 đầu vào sai đỏ, sửa đúng xanh |
| Lượt 11, SHA `d74612a…` | Hai script nguyên bản: ID/delimiter, metadata và VT/FF | 49 đầu vào sai đỏ, sửa đúng xanh |

Đây là **114 lần dựng fixture lịch sử**, có đầu vào trùng giữa các lượt; cộng ba fixture lấy từ ca hiện tại là **117**. Không cộng thành 117 kiểu tấn công độc nhất. Mỗi fixture sai đều được cô lập bằng receipt v2 hợp lệ: helper AssertionError, t27 rc=1, t26/v2 rc=0; sửa README đúng thì helper và ba CLI xanh. [Audit từng nhóm](review-evidence/measurement-audit.json).

Các script tham chiếu thiếu mô-đun hỗ trợ. Tôi phục dựng phần chạy, Git fixture, receipt và phép đo ở ngoài kho; giữ các bộ sinh đầu vào cũ. Bản lượt 13 được chạy nguyên byte; lượt 11–12 chỉ đổi kỳ vọng xanh sai thành đỏ và thay prototype lịch sử bằng head hiện tại. Băm/diff từng bản thích nghi ở [history-adaptations.json](review-evidence/history-adaptations.json). Nhánh prototype vẫn là tên lịch sử, không phải bản vá mới vào kho.

## Đọc mã tiền tố literal

Đã kiểm `cay-kho/ops/lease_publish_test.py:1637`, `:1647` và `:1648`:

- Phép so tên mục là membership trong tập hai chuỗi, phân biệt hoa thường. Không có NFC/NFKC, casefold, IGNORECASE hoặc phép so hậu tố/chuỗi con ở đường chọn tiêu đề.
- `.strip(" \t")` chỉ bóc space/tab ở hai biên. `#` đóng chỉ bị bỏ khi có space/tab đứng trước, tiếp theo chỉ còn dãy `#` và space/tab. Các dòng đã tách theo CR/LF, nên `$` ở đây không bỏ qua một dòng nội dung khác.
- `.lower()` và `.strip()` Unicode còn lại trong `_bang` áp dụng cho ô/header bảng, không chuẩn hóa `chu` hay mở rộng tập tiền tố.
- Không còn cho phép cả nhóm `So`/`Sc`; ngoài ký hiệu `U+26A0` cố định, các chữ khoanh tròn/đóng khung, ký tự hướng chữ và variation selector bổ sung không thể khớp hai chuỗi được nhận.

Không thấy nhóm `So`/`Sc` nào còn đi qua điều kiện literal để thêm chữ vào tiêu đề. Đây là kết luận đọc mã, không phải tuyên bố đã thử mọi renderer. Đối chứng tên thường, `⚠ ` và `#` đóng đã được chạy trong ca t27 nguyên vẹn. [Audit AST và các phép biến đổi](review-evidence/heading-audit.json).

## Răng của ca t27

**37/37 mutant riêng** biên dịch được, giữ nguyên AST của `t27_phan_chung_ten_bien_nhan_sai_bi_TU_CHOI_kem_cach_chua_lam_XANH_ca_t26_t27`, và làm chính ca này đỏ bằng **AssertionError**. Mỗi CLI rc=1, **0/1**, bỏ qua=0. Control rc=0, **1/1**. Không tính SyntaxError hoặc lỗi import là giết mutant.

| Chốt bắt buộc bị đột biến riêng | Kết quả |
|---|---|
| Tiền tố quay về lớp phủ định; mở lại `So`/`Sc` | Mỗi mutant AssertionError, 0/1 |
| Chọn mục bằng chuỗi con nguồn | AssertionError, 0/1 |
| Bỏ chốt comment; bỏ chốt HTML | Mỗi mutant AssertionError, 0/1 |
| Hàng gạch chỉ có dấu hai chấm; bỏ kiểm số ô | Mỗi mutant AssertionError, 0/1 |
| Bỏ chốt đoạn văn trước bảng | AssertionError, 0/1 |
| Bỏ ngữ pháp ô tên; bỏ ngữ pháp ô ID | Mỗi mutant AssertionError, 0/1 |
| Bỏ yêu cầu alias duy nhất | AssertionError, 0/1 |

Các mutant còn lại kiểm giữ span ML/CB, IGNORECASE, nhãn link và nhãn đuôi, ảnh, nhãn trần, khoảng trắng trong span, ký tự dính tên, escaped pipe, danh tính đường dẫn, chốt tên/đuôi và các caller t26/t27, sidecar phân biệt hoa thường, tập danh tính alias, alias theo luật cũ hoặc bị tắt, dòng trắng Unicode, rào mã, thụt lề, VT/FF và ID span dính nhau. [Runner/cặp thay thế](review_mutations.py), [từng kiểu lỗi và rc](review-evidence/mutations.json), [log 29 mutant đầu](review-evidence/mutations-driver.stdout), [8 mutant bổ sung](review-evidence/mutations-extra-driver.stdout).

## Đã đo

Tất cả suite, fixture và mutant chạy ngoài `cay-kho/`, dưới `review-evidence/`. Hai clone có Git/index/refs riêng, đọc objects nguồn qua alternate; `core.abbrev=7`, `core.autocrlf=false`. Python dùng `-B`, `PYTHONDONTWRITEBYTECODE=1`, TMPDIR ngoài nguồn; Ruff dùng `--no-cache`.

| Lệnh, từ thư mục làm việc trừ khi ghi rõ | rc thật | Kết quả |
|---|---:|---|
| `REVIEW_GROUP=r13 python3 -B review_r13_current.py` | 0 | 31 đầu vào sai đỏ; sửa đúng xanh |
| `REVIEW_GROUP=r13 python3 -B review_r13_additional.py headings` | 0 | 6 metadata tiêu đề đỏ; sửa đúng xanh |
| `REVIEW_GROUP=r13 python3 -B review_r13_additional.py prototype` | 0 | 12 vị trí VT/FF đỏ; sửa đúng xanh; README/ca đích xanh |
| `REVIEW_GROUP=r13 python3 -B review_r13_bidi.py` | 0 | 8 Unicode/bidi đỏ; sửa đúng xanh |
| `REVIEW_GROUP=r12 python3 -B review_r12_bidi.py` | 0 | 8 Unicode/bidi đỏ; sửa đúng xanh |
| `REVIEW_GROUP=r11 python3 -B review_r11_current.py` | 0 | 31 đầu vào sai đỏ; sửa đúng xanh |
| `REVIEW_GROUP=r11 python3 -B review_r11_additional.py headings` | 0 | 6 metadata tiêu đề đỏ; sửa đúng xanh |
| `REVIEW_GROUP=r11 python3 -B review_r11_additional.py prototype` | 0 | 12 vị trí VT/FF đỏ; sửa đúng xanh; README/ca đích xanh |
| `REVIEW_GROUP=existing-r13 python3 -B review_existing_r13.py` | 0 | 3 fixture từ ca hiện tại đỏ; sửa đúng xanh |
| `python3 -B review_mutations.py`, rồi `python3 -B review_mutations.py --resume` | 0 / 0 | Control xanh; 29 + 8 mutant bị giết đúng loại lỗi |
| `python3 -B ops/lease_publish_test.py`, cwd `review-evidence/head/` | 1 | **267/269**, chạy 269, bỏ qua 0; 431,196 s |
| Cùng lệnh, cwd `review-evidence/base/` | 1 | **266/268**, chạy 268, bỏ qua 0; 427,607 s |
| `python3 -B review_static.py regression` | 0 | Marker vào/ra đủ 269/269 và 268/268, khớp AST; 268 ca chung giữ nguyên trạng thái; thêm đúng ca mới xanh |
| `python3 -B review_static.py real` | 0 | `_bang` head và `12f21b2` bằng toàn bộ hàng/ô ở cả hai chế độ `giu_span`: ML 321, CB 750; helper cả hai xanh; CLI toàn t27 3/3 |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, cwd head / base | 1 / 1 | Cùng 7 F401 + 2 F541; so code/message/dòng nguồn, delta 0 |
| `python3 -B review_static.py static` | 0 | Ruff delta 0; hai SyntaxWarning cũ `\s`, `\d` không đổi |
| `git -C cay-kho diff --check b29da0b HEAD` | 0 | Không lỗi whitespace |
| `python3 -B review_heading_audit.py` | 0 | Xác nhận tập literal và các phép biến đổi tiêu đề |
| `python3 -B review_audit.py` | 0 | 117 fixture sai đỏ/sửa đúng xanh; 37 mutant; audit **600** CLI chọn ca có tổng kết dương khớp rc và **234** validator v2 có đúng 1 receipt đạt |
| `python3 -B review_static.py integrity` | 0 | 8.468 tệp tracked giữ nguyên băm; HEAD/tree/index/status không đổi; module hai clone khớp byte revision |

Hai lỗi giống nhau ở head và base:

- `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck`: `KHÔNG ĐO ĐƯỢC: thiếu shellcheck`.
- `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`: chưa tới consumer ShellCheck của t137 vì cùng thiếu công cụ.

Hai suite đầy đủ **failed**, phần ShellCheck **not_measured do môi trường**; không ghi chúng thành N/N passed. Ca A/B `t125` xanh ở cả hai. Bare Ruff lint cũng **failed** với nợ nền không đổi. [Delta/lỗi nguyên văn](review-evidence/regression-summary.json), [log head](review-evidence/lease-head.stdout), [log base](review-evidence/lease-base.stdout), [README thật](review-evidence/real-readme.json), [Ruff và môi trường](review-evidence/static.json), [lệnh/rc harness lịch sử](review-evidence/history-runs.json).

## Tính toàn vẹn và giới hạn

Kiểm cuối nguồn: HEAD vẫn là reviewed SHA; tree `fe7018a1db5175f8e1f59149088d4da66231103e`; status gồm untracked/ignored rỗng; index và 8.468 tệp tracked không đổi so snapshot đầu. [Snapshot đầu](review-evidence/source-before.json), [kiểm cuối](review-evidence/source-integrity.json). Snapshot chỉ chứng minh không có delta quan sát được giữa hai mốc. Không sửa branch Executor, không push, không gọi API ghi GitHub.

Môi trường Linux, Python 3.13.17, Unicode database 15.1.0, Pandoc 3.1.3, Ruff 0.16.9; thiếu ShellCheck. Kho thực tế báo shallow=true; toàn bộ head/base/`bc3bbb5`/`12f21b2` cần cho phép đo đều đọc được. Windows thật, CI GitHub và giao diện GitHub thật **not_run/not_measured**. Chứng cứ render ở harness dùng Pandoc GFM/ICU địa phương.

Reviewer: OpenAI Codex, phiên API độc lập với Executor; provider `openai_codex`, execution surface `codex_service`, transport `machine`. Không có attestation độc lập cho model ID/effort hoặc session/run ID; không suy danh tính model từ actor vận chuyển verdict. Approval này là verdict nội dung trên exact SHA, không tự cấp quyền merge/land/deploy.
