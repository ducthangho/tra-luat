verdict: changes_requested
reviewed_sha: 12f21b269a1c2ffaf9bbfbba5b51e616ced73ef2
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1051, lượt 12. Các phản chứng VT/FF và metadata tiêu đề của lượt 11 đã bị chặn. Còn một đường xanh sai trong chính lớp chọn mục: tiền tố điều khiển Unicode RLO được nhận như ký hiệu, dù làm đảo chữ hiển thị của tiêu đề.

## Finding

### F1 — P2 — `t27-heading-bidi-format-prefix`

**Tệp:dòng:** `cay-kho/ops/lease_publish_test.py:1645`, trong `_bang`; ca phản chứng cấu trúc hiện tại ở dòng 2384 trở đi chưa phủ đường này.

Lớp ký tự phủ định trong `re.fullmatch` nhận mọi ký tự ngoài tập loại trừ, bao gồm `U+202E RIGHT-TO-LEFT OVERRIDE` (nhóm Unicode `Cf`). Vì thế, cả hai tiêu đề sau đều bật `lay`:

```text
## \u202eCảnh báo đang có hiệu lực
## \u202eMục lục
```

Ở đây `\u202e` là cách ghi rõ codepoint; fixture chứa ký tự thật. RLO ép các ký tự theo sau hiển thị theo hướng phải sang trái. [Unicode UAX #9](https://www.unicode.org/reports/tr9/#Explicit_Directional_Overrides) quy định tác dụng này. Kết quả tự đo bằng GFM/Pandoc và ICU 74:

| Tên mục trong nguồn sau RLO | Thứ tự chữ khi hiển thị |
|---|---|
| `Mục lục` | `cụl cụM` |
| `Cảnh báo đang có hiệu lực` | `cựl uệih óc gnađ oáb hnảC` |

Pandoc giữ RLO nguyên trong `<h2>`. ICU `ubidi_setPara`/`ubidi_writeReordered` đo thứ tự hiển thị trên chính chuỗi tiêu đề đó. `_bang` vẫn đọc bảng dưới các tiêu đề này như bảng của tên mục đích. Đây là lỗ còn sót của yêu cầu chọn theo **chữ hiển thị**: có thể không có tiêu đề hiển thị đúng tên mục mà gate vẫn xanh. README thật hiện không chứa RLO.

**Tái hiện đã chạy:** `PYTHONDONTWRITEBYTECODE=1 python3 -B review_bidi.py`, rc=0. Hai fixture riêng chỉ thêm RLO trước tên mục cảnh báo hoặc mục lục; verdict được commit trong Git riêng, receipt v2 có SHA/băm/anchor hợp lệ. Kết quả cho từng fixture:

| Phép đo | rc / kết quả |
|---|---|
| `_kiem_muc_luc(thu_muc, goc)` | XANH |
| CLI `--chi-ca=t27_canh_` | 0, 1/1 |
| CLI `--chi-ca=t27_` | 0, 3/3, không bỏ qua |
| CLI `--chi-ca=t26_` | 0, 1/1 |
| `bien_nhan_v2.py --root <fixture>` | 0, 1 ĐẠT v2, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC |

CLI không sửa README. Bỏ RLO thì các phép kiểm tiếp tục xanh. RLE, RLI và ZWSP được đo làm đối chứng; không gộp các ký tự ấy thành finding chỉ vì chúng vô hình.

Chạy lại trực tiếp một phản chứng đã giữ trên đĩa:

```bash
cd review-evidence/fixtures/bidi-ml-0x202e
PYTHONDONTWRITEBYTECODE=1 python3 -B ops/lease_publish_test.py --chi-ca=t27_
```

Lệnh trả 0, `lease_publish: 3/3 đạt`, dù tên mục hiển thị bị đảo. [Runner](review_bidi.py), [kết quả đủ tám đối chứng](review-evidence/bidi-results.json), [HTML mục lục](review-evidence/bidi-ml-0x202e.html), [HTML cảnh báo](review-evidence/bidi-cb-0x202e.html), [log toàn nhóm t27](review-evidence/bidi-ml-0x202e-all-t27.stdout).

**Đề xuất:** thay lớp ký tự phủ định bằng các tiền tố hiển thị được phép rõ ràng, chẳng hạn tên mục nguyên văn hoặc `⚠ ` như README thật. Nếu cần cho phép nhiều ký hiệu hơn, phải loại các ký tự điều khiển định dạng/hướng chữ và kiểm được tác dụng hiển thị. Thêm hai fixture RLO ở hai mục, đồng thời giữ đối chứng tiêu đề thường, `⚠ ` và dấu `#` đóng.

Đã thử một prototype chỉ thu hẹp tiền tố thành dạng trống/`⚠` trong file tạm: cả hai phản chứng RLO đỏ bằng `AssertionError`; README thật và ca mới của PR vẫn xanh. [Prototype](review-evidence/prototype.py), [runner](review_extra.py), [kết quả](review-evidence/prototype-results.json). Không sửa kho Executor.

## Phạm vi đã kiểm

Đối chiếu cả `git diff b29da0b HEAD`, `git diff 000e0fa HEAD` và `git diff d74612a HEAD`. Delta lượt 12 chỉ chạm `ops/lease_publish_test.py`, 31 dòng thêm/16 dòng bỏ. Đọc finding gốc, các verdict và script được cung cấp; tái dựng harness còn thiếu ở ngoài kho và cập nhật kỳ vọng của những script vốn dùng để chứng minh lỗi ở head cũ.

Các đầu vào sai sau đã bị chặn qua `_kiem_muc_luc` và CLI, có đối chứng sửa đúng xanh:

- **47 ca hiện tại:** ba ID span dính nhau; 36 biến thể delimiter với VT/FF/NBSP và các ký tự trắng Unicode; tám tiêu đề chứa tên mục trong title/đích link/thuộc tính HTML hoặc sau chữ khác. Bao phủ các phản chứng lượt 10 và 11, kể cả 12 vị trí VT/FF đầu/cuối/ngoài hàng gạch.
- **31 fixture lượt 9:** 24 dòng trắng Unicode giả, hai bảng thứ hai ngăn bằng NBSP, hai ranh giới rào backtick và ba ID nằm trong metadata/link.
- **26 fixture lượt 8:** HTML block, delimiter chỉ dấu hai chấm, rào đóng thụt 4/tab, đoạn văn/danh sách/trích dẫn dính bảng, VT/FF/NEL/U+2028/U+2029 thay xuống dòng.
- **18 ca lượt 6–7:** ba ô tên và ô ID có comment trong span, comment cắt ngang hàng, tám cách thụt bảng, ba nhãn trần `_x_` bị Markdown đổi chữ.
- **96 ca lượt 5 và các biên ô tên:** control xanh, 95 đầu vào sai đỏ; link tham chiếu, HTML, ảnh, entity, link trong span, span dính tiền tố/hậu tố, tên dài hơn và pipe thoát.

[Tổng hợp](review-evidence/probe-summary.json), [47 ca](review-evidence/current-rechecks.json), [31 ca](review-evidence/r9-recheck.json), [26 ca](review-evidence/r8-recheck.json), [18 ca](review-evidence/r6-r7-recheck.json), [96 ca](review-evidence/table-probes.json).

Đã đo thêm **136 biến thể cấu trúc/tiêu đề** với Pandoc: setext mang tên mục, entity, tiêu đề trùng, ký hiệu/invisible/bidi, bảng thứ hai, hàng sau dòng trống, rào thụt lề/tab, blockquote, danh sách và HTML. Các đầu vào được chấp nhận có đủ hàng/cột hiển thị; đường sai về tên tiêu đề là F1. Không báo các trường hợp bị từ chối hẹp hơn thành finding. [Runner](review_explore.py), [dữ liệu](review-evidence/explore.json).

Ngữ pháp tên được thử ở **90 biến thể trên ba cột**, bảy biến thể được đo thêm bằng fixture v2/CLI đầy đủ, cùng **2.048 ký tự hậu tố**. Đã xét chuỗi mục hợp lệ ghép mục có nhãn lệch danh tính, mục sau dấu phẩy, chú thích chứa Markdown/link/entity, phân cách Unicode, nhãn lạ, `..`/`./`/`//`, tên Unicode và đuôi `.yml`/`.YML`. Không tìm thêm xanh sai trong các phép đo này. **Bốn fixture alias** gốc/con và hai thư mục con cùng basename đều đỏ; thêm hàng đường dẫn riêng thì xanh. [Ngữ pháp](review-evidence/grammar.json), [alias](review-evidence/aliases.json), [runner](review_grammar.py).

Rà AST của `_bang`, `_tach_o`, `_ten_tep`, `_id_hien_thi`, `_kiem_muc_luc`: còn `.strip()` Unicode ở chuẩn hóa header/dữ liệu mặc định và các trường YAML; `_ten_tep` còn `.isspace()` ở biên mục/chú thích; `\s` của `_id_hien_thi` dùng để loại khoảng trắng trong span. Phân cách ID hiện không khớp rỗng. Các phép đo trên không chứng minh thêm xanh sai từ những vị trí này. [Danh sách vị trí](review-evidence/whitespace-audit.json).

## README thật

Đo cùng README head bằng module `000e0fa` và module reviewed head:

- CB **750 hàng**, ML **321 hàng**; hàng ở cả hai chế độ `giu_span` bằng nhau.
- **1.362/1.362 ô tên có cùng tập**, không có token mới hay tập con thực sự.
- **1.631 vector theo hàng** không đổi cả tập vị trí thỏa: 284 verdict đĩa, 306 receipt, 306 đường verdict và 735 caveat.
- ID của 750 hàng và alias của **22 đường dẫn con** không đổi.
- `_kiem_muc_luc` lịch sử và head đều xanh trên README thật.

[Từng ô](review-evidence/real-cells.json), [từng vector](review-evidence/real-vectors.json), [tổng hợp/alias](review-evidence/real-summary.json), [runner](review_static_real.py).

## Răng của ca mới

**31/31 mutant riêng** biên dịch được, làm ca tên mới đỏ bằng **AssertionError**; CLI rc=1, **0/1**, tại đúng bước đã định. Control rc=0, **1/1**. Không tính SyntaxError hoặc lỗi giàn giáo là giết.

| Đột biến | Bước bắt được |
|---|---|
| Bỏ IGNORECASE | (1) |
| Nhận ảnh như link; bỏ luật nhãn; nhãn `.` bất kỳ; nhận ký tự dính sau mục | (6) |
| Span nhận khoảng trắng; bỏ chốt tên | (2) |
| Bỏ giữ span riêng ML / CB | (1) / (6) |
| Tách ô bỏ thoát; ML dùng basename | (6) |
| Bỏ alias; alias không cần duy nhất; tập danh tính chỉ từ `ds_verdict` | (6) |
| Alias theo luật cũ chỉ chống va với verdict trong `ds_verdict` | (7) |
| Bỏ chốt đuôi; bỏ gọi chốt receipt riêng t26 / t27 | (1) |
| Bỏ gọi chốt verdict t27; sidecar gộp hoa thường | (3) / (5) |
| Bỏ chốt comment; thụt lề; số ô delimiter | (6) |
| Dòng trắng Unicode; đuôi rào dùng strip; bỏ luật info backtick; ID token thô | (8) |
| ID cho phân cách rỗng; ô dùng strip Unicode; nhận lại VT/FF; chọn tiêu đề bằng chuỗi con nguồn | (8) |

Thêm **4/4 mutant listing** biên dịch được và chết bằng AssertionError ở ca listing: helper quay glob, bỏ `is_file`, riêng receipt t27 quay glob, riêng verdict t27 quay glob. F1 vẫn qua 3/3 `t27_`, thể hiện khoảng trống còn lại ở tiền tố tiêu đề.

[Runner/cặp thay thế](review_mutations.py), [rc/kiểu lỗi/bước](review-evidence/mutations.json), [listing](review-evidence/listing-mutants.json).

## Đã đo

Mọi suite và mutant chạy trong bản sao/fixture ngoài `cay-kho/`. `copy-head` và `copy-base` có `.git`, index/refs riêng, chia sẻ object chỉ đọc từ nguồn. Module trong hai bản sao khớp byte Git tương ứng. Python không ghi bytecode, `TMPDIR` nằm trong scratch.

| Lệnh / phạm vi | rc | Kết quả |
|---|---:|---|
| `python3 -B ops/lease_publish_test.py`, head copy | 1 | 267/269; chạy 269, bỏ qua 0; 736,279 s |
| Cùng lệnh, base `b29da0b` copy | 1 | 266/268; chạy 268, bỏ qua 0; 732,073 s |
| `CONG_CU_TEST_BAN_KINH=manh python3 -B ops/cong_cu_test.py`, head copy | 0 | 60/60 thực chạy; tổng 61, bỏ qua 1; 672,972 s; cổng cây thật và tự kiểm đạt |
| `python3 -B review_rechecks.py previous` | 0 | 31 + 26 + 18 đầu vào sai đỏ, sửa đúng xanh |
| `python3 -B review_current.py` | 0 | 47 đầu vào sai đỏ; sửa đúng xanh |
| `python3 -B review_probes.py matrix` | 0 | 96 ca, chỉ control được nhận |
| `python3 -B review_grammar.py grammar / aliases` | 0 / 0 | 90 biến thể, 2.048 suffix, bốn fixture alias |
| `python3 -B review_explore.py` | 0 | 136 biến thể và HTML GFM |
| `python3 -B review_bidi.py` | 0 | Tám fixture; hai ca RLO xanh sai, sửa tiêu đề xanh |
| `python3 -B review_mutations.py` | 0 | 31 mutant hợp lệ chết đúng bước; control đạt |
| `python3 -B review_extra.py listing / prototype` | 0 / 0 | Bốn listing mutant chết; prototype chặn RLO, giữ README/ca mới xanh |
| `python3 -B review_static_real.py` | 0 | 1.362 ô / 1.631 vector không đổi; static delta 0 |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head / base | 1 / 1 | Cùng 7 F401 + 2 F541; delta nội dung 0 |
| `compile()` với `warnings.catch_warnings`, head / base | 0 / 0 | Cùng hai SyntaxWarning cũ `\s`, `\d`; delta nội dung 0 |
| `git -C cay-kho diff --check b29da0b HEAD` | 0 | Không lỗi whitespace |
| `python3 -B review_finalize.py regression / probes / source` | 0 / 0 / 0 | Audit marker, 1.188 CLI có bằng chứng dương và tính toàn vẹn nguồn đạt |

Hai suite lease đầy đủ đều **failed**. **268 ca chung không đổi trạng thái**; thêm đúng một ca tên mới đạt. Đã đối chiếu marker vào/ra cấp ngoài với AST: đủ **269/269** và **268/268**. `t125` A/B đạt ở cả hai. Hai lỗi cùng tên và cùng thông báo:

- `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck`: thiếu `shellcheck`.
- `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`: chưa tới consumer ShellCheck vì cùng thiếu công cụ.

Phần ShellCheck **not_measured do môi trường**. Không coi hai suite là N/N đạt. [Delta/lỗi nguyên văn](review-evidence/regression-summary.json), [log head](review-evidence/lease-head.stdout), [log base](review-evidence/lease-base.stdout), [runner](review_runner.py).

Cong có một ca **skipped**: `t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet`, vì không dựng được INDEX chưa hòa giải (`stage={'0'}`). Chế độ gate giao bảng bán kính **490 mutant** cho job mảnh/gom: bảng đó **not_measured** trong review này; không cộng vào 35 mutant tự chạy ở trên. [Log cong hoàn tất](review-evidence/cong-head.stdout), [rc/thời lượng](review-evidence/cong-head.result.json).

[Static/Ruff/warnings](review-evidence/static.json), [audit CLI](review-evidence/cli-audit.json), [audit hồi quy](review-evidence/regression-audit.stdout), [audit tổng hợp](review-evidence/probe-audit.stdout).

Kiểm cuối: **8.468 tệp tracked giữ nguyên băm byte so snapshot đầu**; status kể cả untracked/ignored rỗng; HEAD vẫn đúng reviewed SHA; tree `b530016daa9d2932a6ee75bc9607c9cdf1722ebe`. Module head/base copy khớp revision. [Tính toàn vẹn](review-evidence/source-integrity.json).

Môi trường Linux, Python 3.13.17, Pandoc 3.1.3, ICU 74, Ruff 0.16.9; thiếu ShellCheck. Kho báo `--is-shallow-repository=true`; mọi revision cần cho phép đo đều đọc được. Windows thật, CI GitHub và ảnh chụp giao diện GitHub **not_run/not_measured**. Chứng cứ hiển thị F1 là HTML GFM/Pandoc cộng phép đo Unicode ICU, có nêu rõ ở trên. Tool `environment_status` không có trong inventory phiên này.

Reviewer: OpenAI Codex, phiên API độc lập với Executor; provider `openai_codex`, execution surface `codex_service`, transport `machine`. Không có attestation độc lập cho model ID/effort. Chỉ ghi artifact và bản sao ngoài kho được review; không push, không gọi API ghi GitHub, không merge/land/deploy/LIVE.
