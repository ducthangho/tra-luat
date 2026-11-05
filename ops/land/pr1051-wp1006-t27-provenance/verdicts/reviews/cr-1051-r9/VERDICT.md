verdict: changes_requested
reviewed_sha: 5c6b5e28621f884eb2fbe8354f94d519f9fdf866
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1051, lượt 9. **26 phản chứng nguyên bản lượt 8 đã bị chặn; lớp lỗi t27 xác nhận nội dung không hiện đúng trong bảng vẫn chưa đóng.** Giữ một finding P2 cùng ID lịch sử; không báo các trường hợp đỏ an toàn thành finding.

Base `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`; reviewed tree `047397f37211bc6775a73d5cded0448c9db8df6b`. Diff toàn PR chỉ `ops/lease_publish_test.py`: 540 thêm / 36 bỏ; lượt 8 → 9: 84 thêm / 26 bỏ. Chỉ thị trong `PROMPT.md` là authority cho review hiện tại.

**F1 — P2 — `wp1006-case-insensitive-listing-case-sensitive-consumer`**

**Tệp:dòng:** `ops/lease_publish_test.py:1641` dùng `str.strip()` để nhận dòng trống; `:1616`–`:1621` nhận rào mở/đóng chưa đúng GFM; `:1979` so ID bằng token nguồn thô. Ca mới tại `:2356` chưa phủ các đường dưới đây.

**Tác động:** t27 vẫn có thể báo verdict/receipt/caveat đã xuất hiện đúng cột, dù người đọc chỉ thấy văn bản thường, khối mã, hoặc ô ID ghi `OTHER`. Không phải bypass lược đồ v2: các fixture phản chứng vẫn qua validator v2 thật.

**Tái hiện đã chạy:** `PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=ignore python3 review_r9_findings.py` — rc=0, xác nhận **29 fixture xanh sai**; `python3 review_extra_blocks.py` — rc=0, xác nhận thêm **2 fixture**. Mỗi fixture có Git riêng, verdict đã commit, băm đúng, receipt v2 đủ trường và commit mỏ neo tồn tại. URL/identity là dữ liệu thử. Mã suite chép nguyên byte từ reviewed head; validator chạy mã head, không mock Git/schema.

Ở **31/31 fixture**: `_kiem_muc_luc` xanh sai; CLI `--chi-ca=t27_canh_` **rc=0, 1/1**; toàn selector `--chi-ca=t27_` **rc=0, 3/3**; t26 **rc=0, 1/1**; validator v2 **rc=0**. Sửa README về dạng đúng trên cùng verdict/receipt làm cả t26/t27/v2 xanh.

| Đường xanh sai | Thay đổi tối thiểu và kết quả GFM |
|---|---|
| Dòng Unicode bị coi là dòng trống | Trước bảng CB hoặc ML, thêm chuỗi Python `"prose\n\u00a0\n"`. `str.strip()` xoá NBSP, reset `trong_doan=False`, rồi parser nhận bảng. Render chỉ có đoạn văn ở mục đó. Đã xác nhận 12 ký tự × 2 mục = **24 fixture**: U+000B, U+000C, U+0085, U+00A0, U+1680, U+2000, U+2003, U+2028, U+2029, U+202F, U+205F, U+3000. |
| Bảng thứ hai giả | Đặt bảng `other/other` + delimiter trước bảng đúng, ngăn bằng một dòng NBSP thay dòng trống thật. Parser nhận bảng sau với các cột cần kiểm; render chỉ có bảng `other/other` rỗng và phần tên/ID ở đoạn văn. **2 fixture CB/ML**. |
| Rào mở không hợp lệ làm lệch trạng thái | Thay ML bằng `` "```info`\n```\n\n" + ML + "\n```\n" ``. Dòng đầu chứa backtick trong info nên không mở rào theo GFM; dòng sau mới mở rào và giấu ML. `_bang` lại mở ở dòng đầu, đóng ở dòng sau, rồi công nhận ML. **1 fixture**. |
| Rào đóng có NBSP | Thay ML bằng `` "```\n```\u00a0\n\n" + ML + "\n```\n" ``. `strip()` coi NBSP sau rào là rỗng và đóng sớm; render giữ ML trong khối mã. **1 fixture**. |
| ID chỉ có trong cú pháp ẩn | Ô ID là `<span data-x=" C1 ">OTHER</span>`, `<span C1 >OTHER</span>`, hoặc `[OTHER]( C1 )`. `.split()` vẫn cho token `C1`; văn bản ô render là **OTHER**, còn ID nằm trong thuộc tính hoặc đích link. **3 fixture**. Ngữ pháp `_ten_tep` không bảo vệ cột ID. |

GFM chỉ coi dòng rỗng hoặc chứa space/tab là dòng trống; info của rào backtick không được chứa backtick; nội dung HTML/đích link không đồng nghĩa chữ hiển thị trong ô. Đối chiếu [quy tắc dòng](https://github.github.com/gfm/#characters-and-lines), [rào mã](https://github.github.com/gfm/#fenced-code-blocks), [HTML nội dòng](https://github.github.com/gfm/#raw-html) và [link](https://github.github.com/gfm/#links).

Bằng chứng: [driver chính](review_r9_findings.py), [29 kết quả](run/evidence/r9-confirmed.json), [hai bảng thứ hai](run/evidence/r9-extra-confirmed.json), [README NBSP](run/evidence/fixtures/finding-blank-ml-xa0/ops/reviews/README.md), [HTML NBSP](run/evidence/finding-blank-ml-xa0.html), [rào mã](run/evidence/finding-fence-invalid-opener.html), [ID link](run/evidence/finding-id-link.html). Render địa phương dùng Pandoc `--from=gfm --to=html`; không khai đã đo UI GitHub trực tiếp.

Historical controls trên cùng fixture cho thấy cả năm mẫu đại diện cũng xanh ở `b29da0b`, `000e0fa`, `c75df56`: đây là **phần còn mở của lớp lỗi**, không phải năm hồi quy mới do commit lượt 9 sinh ra. [Kết quả lịch sử](run/evidence/r9-historical.json).

**Đề xuất vá ở đâu và thế nào:** trong `_bang`, dùng ngữ nghĩa space/tab rõ ràng cho dòng trống và phần đuôi rào; kiểm info của rào mở, hoặc từ chối cấu trúc chưa hỗ trợ. Tại vòng kiểm caveat, định nghĩa ngữ pháp cho phép cho **toàn ô ID**, ví dụ danh sách code span literal, để token trong thuộc tính/đích link không được tính. Giữ nguyên chốt tên/đuôi/alias/sidecar hiện có.

**Ca khoá và bản vá thử:** thêm 31 phản chứng trên qua consumer/CLI cùng đối chứng sửa đúng; giữ các fixture cũ. [Prototype](review_prototype.py) và [diff minh hoạ](run/evidence/prototype.patch) chỉ nằm ngoài kho: **31/31 đầu vào sai đỏ bằng AssertionError, 31/31 sửa đúng xanh**, README thật xanh, ca tên mới **1/1**. [Kết quả](run/evidence/prototype-results.json). Prototype chưa chạy toàn suite, không phải patch đã áp lên branch Executor; Executor cần tự dẫn xuất và chạy lại gate.

**Đối chiếu lượt 5–8 và ngữ pháp**

| Phạm vi | Kết quả độc lập ở head |
|---|---|
| Lượt 8 | **26/26** fixture cấu trúc cũ đỏ ở helper và CLI t27, kể cả toàn selector 3 ca; t26/v2 vẫn xanh; sửa đúng xanh. Hai bypass tiêu đề giả trong rào mã rồi comment ghép hàng cũng đỏ đúng chốt `comment HTML`. |
| Lượt 6–7 | 20 probe: control xanh, **19 đầu vào sai đỏ**; gồm ba span tên + span ID có comment, comment cắt ngang hàng, bảng CB/ML thụt 4, và rào mã. Ba nhãn `_x_` trần đỏ; bọc nháy lại xanh. |
| Lượt 5 | Ma trận **96 ca** qua helper/CLI: control xanh, **95 sai đỏ**. Reference link, HTML, ảnh, link trong span, entity, tiền/hậu tố, escaped pipe đều bị chặn. Các mẫu v2 đầy đủ và ba loại va basename gốc/con cũng đã chạy lại. |
| Alias | Va `y-verdict.md`, `VERDICT.md`, `report.md`, chiều ngược và hai thư mục con cùng basename đều đỏ đúng caveat. Đường dẫn riêng sửa được; nhiều receipt cùng một đường dẫn giữ alias dương. |
| Ngữ pháp ô tên | **138 + 54 = 192 ca**, 42 xanh / 150 đỏ đúng kỳ vọng. Đã thử ghép mục đúng/sai, dấu phẩy, chú thích chứa code/link/ảnh/HTML/entity, nhãn lạ/zero-width/bidi/escape, đích `..`/`./`/`//`; có nhóm nhãn bọc nháy để tránh chỉ bị chặn ở nhãn trần. Chưa tìm thêm xanh sai trong `_ten_tep` trên ô nguyên bản. |
| Unicode và `.yml` | Fixture v2 đầy đủ xanh; bỏ `é-verdict.md` hoặc đổi cảnh báo `report.yml` thành `report.yaml` đỏ đúng chốt. **2.048** biến thể suffix: chỉ `alias.receipt.yaml` được chốt tên nhận. |

[26 ca](run/evidence/r8-recheck.json), [bypass comment cũ](run/evidence/prepass-results.json), [lượt 6–7](run/evidence/r7-extra-results.json), [nhãn](run/evidence/label-emphasis-results.json), [96 ca](run/evidence/table-probes.json), [v2 lượt 5](run/evidence/finding-results.json), [alias](run/evidence/collision-extra.json), [ngữ pháp](run/evidence/grammar-results.json), [ngữ pháp bổ sung](run/evidence/grammar-extra-results.json), [Unicode/suffix](run/evidence/unicode-yml-suffix.json).

74 probe cấu trúc bổ sung đã xét tab, khối mã thụt lề, blockquote, danh sách, heading trùng/giả, setext, bảng thứ hai và hàng sau dòng trống. Bảng thứ hai thật/heading trùng có bảng thật có thể xanh hợp lệ; hàng lẻ sau dòng trống bị từ chối. Không tính literal `<!--` chưa đóng nằm sau tên hiển thị hợp lệ thành finding. [Dữ liệu probe](run/evidence/r9-blocks.json).

**README thật**

So chính README head với parser/consumer `000e0fa`: **1.362/1.362 ô tên cùng tập**, 0 token mới, 0 tập con thực sự. CB **750** hàng; ML **321** hàng, trong đó 306 có cột tên. **1.631 vector kết luận theo hàng** (284 verdict đĩa + 612 receipt/verdict + 735 caveat) có delta **0**. Alias có **0 tập thay đổi**, 22 đường dẫn con / 50 hàng cảnh báo giữ kết luận. Hai checker đều xanh; `_bang` mặc định bằng nhau. Đo nguồn có **1.081 dòng bảng cột 0**, 0 dòng bảng thụt lề, 0 comment và 0 rào mã trong hai mục.

[Từng ô](run/evidence/real-r6-cells.json), [từng vector](run/evidence/real-r6-vectors.json), [tổng hợp](run/evidence/real-r6-summary.json), [hình thức nguồn](run/evidence/real-geometry.json). Tên artifact `r6` kế thừa driver tham chiếu; module thực chạy là head lượt 9.

**Răng của ca mới**

**25/25 mutant chốt tên/alias**, **4/4 mutant listing**, **7/7 mutant cấu trúc lượt 9** đều compile được và làm ca tương ứng đỏ bằng AssertionError, rc=1, 0/1. Control xanh 1/1. Không tính SyntaxError hoặc lỗi giàn giáo là giết.

| Đột biến | Bước bắt được trong ca tên mới |
|---|---|
| Bỏ IGNORECASE | (1) |
| Nhận ảnh; bỏ luật nhãn; nhãn `.` bất kỳ; nhận ký tự dính sau mục | (6) |
| Span nhận khoảng trắng; bỏ chốt tên | (2) |
| Bỏ giữ span ML / CB / cả hai | (1) / (6) / (1) |
| Tách ô bỏ escape; ML dùng basename | (6) |
| Bỏ alias; alias không duy nhất; tập danh tính chỉ từ `ds_verdict` | (6) |
| Alias chỉ chống va với `ds_verdict` như lượt 5 | (7) |
| Bỏ chốt đuôi; bỏ gọi chốt receipt riêng t26/t27 | (1) |
| Bỏ gọi chốt verdict t27; gộp case stem sidecar | (3) / (5) |
| Bỏ cấm comment/thụt lề; bỏ kiểm số ô delimiter; nhận lại nhãn trần | (6) |
| Quay `splitlines`, rào thụt rộng, delimiter lỏng, nhận HTML block, bỏ ngữ cảnh đoạn, bỏ heading thụt/setext | (8), cả 7 mutant |

Bốn mutant listing (helper về glob, bỏ `is_file`, riêng receipt/verdict về glob) chết ở ca listing. [Cặp thay thế/runner](review_mutations.py), [25 bước kiểm độc lập](run/evidence/mutation-step-audit.json), [listing](run/evidence/listing-mutation-results.json), [bảy mutant cấu trúc](run/evidence/r9-mutation-results.json). Các chốt được phủ có răng; 31 fixture F1 vẫn toàn t27 3/3 chứng minh còn thiếu độ phủ.

## Đã đo

Các suite chạy trong ba bản sao đầy đủ, `.git`/refs riêng ngoài `cay-kho/`, `core.abbrev=7`, `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`; `TMPDIR` nằm ngoài kho. [Runner hồi quy](regression/run.py), [báo cáo](regression/REPORT.md), [summary](regression/summary.json), [runner fixture](review_runner.py).

| Lệnh / bản sao | rc | Kết quả |
|---|---:|---|
| `python3 ops/lease_publish_test.py`, head | 1 | **267/269**; chạy 269, bỏ qua 0; 856.674 s |
| Cùng lệnh, base `b29da0b` | 1 | **266/268**; chạy 268, bỏ qua 0; 856.395 s |
| `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py`, head | 0 | **60/60** thực chạy, tổng 61; bỏ qua=1, tiền kiểm bỏ qua=0; 785.382 s |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head/base | 1 / 1 | 9 cảnh báo mỗi bên, delta nội dung 0 |
| `compile()` trong `warnings.catch_warnings`, head/base | 0 / 0 | Hai SyntaxWarning cũ mỗi bên, delta nội dung 0 |
| `git -C cay-kho diff --check b29da0b HEAD` | 0 | Không lỗi |

Hai suite lease đầy đủ đều **failed**, không khai N/N đạt. Cùng hai ca đỏ, thông báo bằng nhau:

- `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck`: KHÔNG ĐO ĐƯỢC: thiếu `shellcheck` — actionlint IM LẶNG bỏ toàn bộ luật shell khi vắng nó
- `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`: chưa tới consumer shellcheck ở t137: KHÔNG ĐO ĐƯỢC: thiếu `shellcheck` — actionlint IM LẶNG bỏ toàn bộ luật shell khi vắng nó

Phần ShellCheck là **not_measured do thiếu công cụ**. **268 ca chung không đổi trạng thái**, thêm đúng ca tên biên nhận mới đạt; không có ca cũ đổi trạng thái hoặc thêm bỏ qua. Đã đối chiếu đủ cặp marker vào/ra cấp ngoài với danh sách `@ca` từ AST; không lấy marker A/B lồng để tăng số ca. `t125` đạt ở cả head/base.

Cong chạy theo chế độ gate của CI `CONG_CU_TEST_BAN_KINH=manh`: **60/60 thực chạy**, tổng 61, bỏ qua 1. Ca `t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet` skipped vì không dựng được INDEX chưa hoà giải (`stage={'0'}`). Cổng cây thật và phần tự kiểm sau summary được kiểm với mã thoát cuối. Bán kính mutant được giao các job mảnh/gom theo chế độ này: **not_measured**, không tính thành mutant đã đạt ở lượt review này.

| Driver/phép đo khác | rc | Kết quả |
|---|---:|---|
| `python3 review_probes.py matrix`; `python3 review_r5_confirm.py` | 0 / 0 | Ma trận 96 ca, các mẫu v2 và alias |
| `python3 review_previous.py`; `python3 review_labels.py` | 0 / 0 | Phản chứng lượt 6–7 đỏ, đối chứng sửa đúng xanh |
| `python3 review_r9_blocks.py`; `python3 review_r8_prepass.py` | 0 / 0 | 26 fixture cũ đóng; 74 probe mới; bypass comment cũ bị chặn |
| `python3 review_r9_findings.py`; `python3 review_extra_blocks.py` | 0 / 0 | 29 + 2 xanh sai; t26/v2 và đối chứng sửa đúng xanh |
| `python3 review_supplement.py real / grammar / unicode`; `python3 review_grammar_extra.py` | 0 / 0 / 0 / 0 | README, 192 ca ngữ pháp, Unicode/`.yml`, 2.048 suffix |
| `python3 review_mutations.py`; `python3 review_listing_mutations.py`; `python3 review_r9_mutations.py` | 0 / 0 / 0 | 25 + 4 + 7 mutant chết đúng chốt |
| `python3 review_prototype.py` | 0 | README thật/ca mới xanh; 31 sai đỏ; 31 sửa đúng xanh |
| `python3 review_evidence_audit.py` | 0 | 1029 CLI chọn ca có số ca/marker/rc khớp; source sạch; 25 bước đúng |

Ruff mỗi bên **7 F401 + 2 F541**; Counter `(code, message)` bằng nhau, delta **0**. Hai SyntaxWarning cũ `\s` và `\d` mỗi bên, delta nội dung **0**, chỉ dịch dòng. [Static](regression/static.json), [so message Ruff](run/evidence/ruff-message-delta.json), [audit CLI](run/evidence/cli-marker-audit.json).

Nguồn sau review vẫn sạch và module khớp nguyên byte HEAD; cả ba bản sao suite khớp revision tương ứng. [Audit nguồn](run/evidence/source-audit.json), [integrity bản sao](regression/summary.json). Repo được cấp trả `--is-shallow-repository=true`, khác mô tả “đủ lịch sử”; mọi revision cần diff/đối chứng trong lượt này vẫn đọc được, không sửa shallow marker. Windows thật và CI GitHub: **not_run/not_measured**; không suy từ Linux.

Reviewer: Codex, phiên API độc lập với Executor; provider `openai_codex`, execution surface `codex_service`, transport `machine`. Không có runtime attestation để khai model ID/effort cụ thể. Theo `CLAUDE.md` §Quy trình sửa code bước 5, một sub-agent chỉ chạy/tiêu hoá hồi quy dài; phiên chính tự đọc mã, chạy phản chứng/ngữ pháp/mutation và kết luận. Tool `environment_status` không có trong tập công cụ hiện tại. Chỉ ghi bằng chứng/bản sao/verdict ngoài `cay-kho/`; không push, không gọi API ghi GitHub, không merge/deploy/LIVE.
