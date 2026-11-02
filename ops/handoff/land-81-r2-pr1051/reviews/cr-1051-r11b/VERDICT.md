verdict: changes_requested
reviewed_sha: d74612a964a6c91dac89aa2255658a21b31fbb4f
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1051, lượt 11. P2 lượt 10 **chưa đóng hết**: ba span ID dính nhau đã bị chặn, nhưng bốn fixture VT/FF trong chính ma trận delimiter lượt 10 vẫn xanh sai. Có thêm đường nhận nhầm mục từ chữ chỉ nằm trong thuộc tính/đích link của tiêu đề. Giữ một finding P2 cho lớp lịch sử “t27 công nhận nội dung không hiển thị đúng trong bảng/mục cần kiểm”; hai biểu hiện dưới đây không đếm thành hai finding.

## Finding F1 — P2 — `wp1006-case-insensitive-listing-case-sensitive-consumer`

**Tệp:dòng:** [ops/lease_publish_test.py:1565](cay-kho/ops/lease_publish_test.py#L1565), `:1566`, `:1571` và [ops/lease_publish_test.py:1640](cay-kho/ops/lease_publish_test.py#L1640). Consumer `_kiem_muc_luc` tin các hàng mà `_bang` trả về. Ca khóa ở `:2092` vẫn xanh trên các phản chứng này.

**A. VT/FF vẫn bị bóc thành hàng gạch hợp lệ.** `TRANG = " \t\x0b\x0c"` thay `strip()` Unicode nhưng vẫn nhận `U+000B` và `U+000C` ở chỗ GFM không nhận delimiter bảng. Đổi riêng dòng `|---|---|` của một trong hai bảng thành chuỗi Python `"|\x0b---|---|"` hoặc `"|\x0c---|---|"`: `_tach_o` trả `['---', '---']`, `_bang` nhận đủ hàng, `_kiem_muc_luc` xanh và CLI t27 xanh **1/1**. `pandoc --from=gfm --to=html` chỉ dựng bảng còn lại; bảng bị đổi thành đoạn `<p>`, không có cột/hàng bảng mà checker vừa công nhận. Đây là phần còn sót của phản chứng delimiter lượt 10, không phải hồi quy mới của lượt 11.

Tự đo lại đủ **28** delimiter lượt 10: **24 đỏ, 4 xanh sai** (VT/FF × CB/ML). Mở rộng VT/FF sang đầu ô, cuối ô và sau pipe cuối: **12/12 xanh sai**, mỗi bản render chỉ còn một bảng. Cùng fixture, selector toàn bộ `t27_` vẫn **rc=0, 3/3**; t26 **rc=0, 1/1** và validator v2 thật **rc=0, 1 receipt đạt**, không miễn trừ legacy. Bỏ VT/FF, giữ nguyên verdict/receipt, các đối chứng đều xanh.

**B. Tên mục chỉ nằm trong metadata tiêu đề vẫn bật `lay`.** Dòng `lay = ... and tieu_de in dong` tìm chuỗi trong nguồn Markdown, nên những tiêu đề sau được coi là mục cần kiểm dù chữ hiển thị chỉ là **Khác**:

```markdown
## [Khác](other.md "Cảnh báo đang có hiệu lực")
## [Khác](<Mục lục>)
## <span title="Mục lục">Khác</span>
```

Thay riêng tiêu đề CB hoặc ML bằng các dạng title link, đích link, hoặc thuộc tính HTML: **6/6 helper xanh, CLI t27 rc=0 (1/1), toàn `t27_` rc=0 (3/3), t26/v2 xanh**. HTML GFM có `<h2 ...>Khác</h2>` chứa link/span tương ứng và bảng dưới mục **Khác**; không có bảng dưới tiêu đề hiển thị mang tên mục cần kiểm. Thay lại tiêu đề đúng làm mọi đối chứng xanh. Đây là phần còn sót trong phạm vi đọc cấu trúc được PROMPT yêu cầu kiểm, không gọi là lỗi mới do delta lượt 10 → 11.

**Tác động:** t27 xác nhận mục lục/cảnh báo đúng chỗ khi bảng không được dựng hoặc thuộc một mục khác. Không diễn giải thành bypass lược đồ v2; v2 xanh dùng để cô lập lỗi ở phép kiểm mục lục.

**Tái hiện đã chạy:**

- `python3 -B review_current.py` — driver rc=0; ba ID dính đỏ, xác nhận bốn delimiter xanh sai còn sót. [Kết quả](review-evidence/r11-boundaries.json).
- `python3 -B review_additional.py headings` — driver rc=0; sáu tiêu đề ẩn tên mục xanh sai, sửa đúng xanh. [Kết quả](review-evidence/heading-findings.json), [HTML CB/title](review-evidence/heading-cb-link-title.html), [HTML ML/đích](review-evidence/heading-ml-link-destination.html).
- `python3 -B review_additional.py prototype` — driver rc=0; đo thêm 12 delimiter xanh sai trên head. [Kết quả](review-evidence/extra-delimiters.json), [HTML VT](review-evidence/extra-delimiter-ml-0xb-prefix.html).
- Fixture giữ nguyên module head, Git riêng, commit neo tồn tại, verdict băm đúng và receipt v2 đầy đủ. URL/identity là dữ liệu thử. Có thể vào `review-evidence/fixtures/r11-delimiter-ml-prefix-x0b/` hoặc `review-evidence/fixtures/heading-cb-link-title/` rồi chạy `python3 -B ops/lease_publish_test.py --chi-ca=t27_` để thấy **3/3 đạt** trên README sai đang được giữ lại.

**Đề xuất:** chỉ bóc space/tab trong bước nhận delimiter bảng; không lấy định nghĩa whitespace chung thay cho quy tắc riêng của bảng. Với tiêu đề, định nghĩa các dạng tiêu đề literal được phép, hoặc đối chiếu phần chữ thực sự hiển thị; không tìm tên mục trong toàn bộ nguồn của heading. Thêm fixture VT/FF ở cả CB/ML và heading có tên mục trong title/URL/thuộc tính HTML qua consumer/CLI. Các ca sai phải đỏ đúng chốt, sửa đúng xanh; giữ README thật và alias hiện hành. Quy tắc bảng và link tham khảo [đặc tả GFM](https://github.github.com/gfm/#tables-extension-); bằng chứng render trong review dùng Pandoc GFM cục bộ, không tuyên bố đã chạy trên giao diện GitHub thật.

[Prototype trong scratch](review-evidence/prototype.py) chỉ đổi `TRANG` thành space/tab và từ chối heading có `[]<>` khi chọn mục: **18/18 đầu vào sai đỏ bằng AssertionError**, đối chứng sửa đúng, README thật và ca tên mới xanh. [Kết quả](review-evidence/prototype-results.json). Đây là phép thử hẹp, không phải bản vá hoàn chỉnh hoặc bản đã áp vào `cay-kho/`; chưa chạy full suite trên prototype.

## Đối chiếu các yêu cầu

| Phạm vi | Kết quả tự đo |
|---|---|
| Lượt 10: span ID | **3/3 đỏ** qua helper, CLI một ca và toàn `t27_`; t26/v2 và sửa đúng xanh. |
| Lượt 10: 28 delimiter | **24 đỏ / 4 xanh sai** tại F1-A; sửa đúng xanh. |
| 31 fixture lượt 9 | **31/31 đỏ** qua helper, CLI t27 và toàn `t27_`; t26/v2 và sửa đúng xanh. |
| 26 fixture lượt 8 | **26/26 đỏ** qua cùng consumer; giữ nguyên các rào bổ sung của fixture tham chiếu; sửa đúng xanh. |
| Lượt 6–7 | **18 đầu vào sai đỏ**: comment trong ba ô tên và ID, comment cắt hàng, bảng CB/ML thụt space/tab, nhãn `_x_` trần; sửa đúng xanh. |
| Lượt 5 | Ma trận **96 ca: 1 control xanh / 95 sai đỏ**, qua `_kiem_muc_luc` và CLI. Thêm sáu mẫu có receipt v2 đầy đủ cùng hai bypass tiêu đề giả trong fence rồi comment ghép hàng: **8/8 đỏ**, t26/v2/sửa đúng xanh. |
| Ngữ pháp ô tên | **138 ca: 36 xanh / 102 đỏ đúng kỳ vọng**, qua helper/CLI. Phủ mục ghép, mục sau phẩy/space/tab, mục sai danh tính ở trước/sau, chú thích có code/ảnh/HTML/entity, nhãn có Unicode/zero-width/bidi/escape, đường `..`/`./`/`//`. Không tìm thêm xanh sai trong nhóm này. |
| Alias | **12 phép đo**, va gốc/con với `y-verdict.md`, `VERDICT.md`, `report.md`, hai thư mục con, gốc không caveat và hai receipt cùng danh tính. Va danh tính đỏ, đường riêng sửa được; cùng danh tính giữ alias xanh. |
| Unicode / `.yml` | Fixture đầy đủ xanh; bỏ `é-verdict.md` hoặc đổi cảnh báo `report.yml` sang `report.yaml` đỏ. **2.048** biến thể case suffix: chỉ `alias.receipt.yaml` qua chốt tên. |
| Cấu trúc bổ sung | **84 biến thể**, gồm tab, fence thụt lề, blockquote, danh sách, heading trùng/giả/setext, bảng thứ hai, hàng sau dòng trống, ký tự vô hình. **26 xanh** đều có bảng/ô cần kiểm hiển thị trong HTML GFM; không thêm xanh sai trong nhóm này. Sáu tiêu đề metadata ở F1-B được đo riêng. |

[31 ca](review-evidence/r9-recheck.json), [26 ca](review-evidence/r8-recheck.json), [18 ca](review-evidence/r6-r7-recheck.json), [96 ca](review-evidence/table-probes.json), [8 ca bổ sung](review-evidence/previous-extra.json), [ngữ pháp](review-evidence/grammar.json), [alias](review-evidence/aliases.json), [Unicode/suffix](review-evidence/unicode-yml.json), [84 cấu trúc](review-evidence/blocks.json).

Đã rà các site xử lý trắng ở năm hàm được hỏi, có lưu [danh sách AST](review-evidence/whitespace-audit.json). Vẫn còn `.strip()` Unicode khi chuẩn hóa header/dạng bảng mặc định, khi đọc trường YAML và ID; `_ten_tep` còn `.isspace()` ở ranh giới mục/chú thích; `\s` trong `_id_hien_thi` dùng để **loại** ký tự trắng khỏi nội dung span. Không báo việc còn dùng chúng thành finding nếu không chứng minh được xanh sai. Phân cách ID hiện bắt buộc comma hoặc space/tab khác rỗng; phép đột biến quay về phân cách có thể rỗng chết ở bước (8). Đường xanh sai đã chứng minh nằm ở F1.

### README thật

So **cùng README head** bằng code `000e0fa` và reviewed head, không lấy số của Executor:

- CB **750 hàng**, ML **321 hàng**; dữ liệu hàng ở cả hai chế độ `giu_span` bằng nhau.
- **1.362/1.362 ô tên có cùng tập**; không có token mới hoặc tập con thực sự. Không đếm 30 vị trí cột vốn không tồn tại thành ô dữ liệu.
- **1.631 vector theo hàng** không đổi: 284 verdict đĩa, 612 kiểm receipt/verdict, 735 caveat. So cả tập vị trí hàng thỏa, không chỉ kết luận tổng.
- ID của 750 ô cùng tập; **22 đường dẫn con** có tập alias và kết luận không đổi.
- `_kiem_muc_luc` lịch sử và head đều xanh trên README thật.

[Từng ô](review-evidence/real-cells.json), [từng vector](review-evidence/real-vectors.json), [tổng hợp và alias](review-evidence/real-summary.json).

### Răng của ca mới

**29/29 mutant** biên dịch được, làm ca tên mới đỏ bằng **AssertionError**, CLI **rc=1, 0/1**; control **rc=0, 1/1**. Đã kiểm traceback và bước bắt lỗi; không tính SyntaxError hoặc lỗi giàn giáo là giết.

| Đột biến riêng | Bước bắt được |
|---|---|
| Bỏ IGNORECASE | (1) |
| Nhận ảnh như link; bỏ luật nhãn; nhãn `.` bất kỳ; ký tự dính sau mục | (6) |
| Span nhận khoảng trắng; bỏ chốt tên | (2) |
| Bỏ giữ span riêng ML / CB | (1) / (6) |
| Tách ô bỏ thoát; ML dùng basename | (6) |
| Bỏ alias; alias không cần duy nhất; tập danh tính chỉ từ `ds_verdict` | (6) |
| Alias theo luật chống va cũ chỉ nhìn `ds_verdict` | (7) |
| Bỏ chốt suffix; bỏ gọi chốt receipt riêng t26 / t27 | (1) |
| Bỏ gọi chốt verdict t27; gộp case stem sidecar | (3) / (5) |
| Bỏ chốt comment; bỏ chốt thụt lề; bỏ kiểm số ô delimiter | (6) |
| Dòng trắng Unicode; rào đóng dùng strip; bỏ luật info backtick; ID token thô | (8) |
| ID lại cho delimiter rỗng; ô lại dùng strip Unicode | (8) |

Thêm **4/4 mutant listing** biên dịch được và chết bằng AssertionError ở ca listing: helper quay glob, bỏ `is_file`, riêng receipt t27 quay glob, riêng verdict t27 quay glob. Các chốt đã phủ có răng; F1 vẫn qua toàn `t27_` chứng minh còn thiếu ca ở hai ranh giới nêu trên.

[Cặp thay thế và runner](review_mutations.py), [rc/traceback/bước của 29 mutant](review-evidence/mutation-results.json), [audit bước](review-evidence/mutation-audit.stdout), [4 mutant listing](review-evidence/listing-mutants.json).

## Đã đo

Mọi suite, fixture và đột biến chạy trong bản sao ngoài `cay-kho/`. Hai clone có `.git`, index/refs riêng; object alternate chỉ đọc từ nguồn. Module suite khớp byte Git của revision tương ứng. CLI dùng Python UTF-8, không ghi bytecode, `TMPDIR` trong scratch. Driver rc=0 xác nhận phép đo, không đổi một phản chứng xanh sai thành ca đạt yêu cầu.

Hai suite lease đầy đủ đều **failed**, không khai N/N đạt: head **267/269**, base **266/268**, không bỏ qua. Cùng hai lỗi thiếu ShellCheck, thông báo bằng nhau:

- `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck`: thiếu `shellcheck`.
- `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`: chưa tới consumer ShellCheck vì cùng thiếu công cụ.

Phần ShellCheck **not_measured do môi trường**, không tính thành hồi quy PR hoặc đổi thành pass. **268 ca chung không đổi trạng thái**, thêm đúng ca tên mới đạt. Đã đối chiếu toàn bộ marker vào/ra cấp ngoài với danh sách `@ca` từ AST: đủ **269/269** ở head, **268/268** ở base. `t125` A/B đạt ở cả hai. [Delta và lỗi nguyên văn](review-evidence/regression-summary.json).

Cong ở chế độ gate CI đã kết thúc **rc=0**, **60/60 ca thực chạy**, tổng 61, bỏ qua 1, tiền kiểm bỏ qua 0; tự kiểm giàn giáo/song song và cổng cây thật đạt. `t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet` **skipped** vì không dựng được INDEX chưa hòa giải (`stage={'0'}`). Bán kính **490** đột biến được giao cho job mảnh/gom trong chế độ này: **not_measured**, không tính vào 33 mutant tự chạy trong review. [Log hoàn tất](review-evidence/cong-head.stdout), [rc/thời lượng](review-evidence/cong-head.result.json).

| Lệnh / phạm vi | rc | Kết quả |
|---|---:|---|
| `python3 -B ops/lease_publish_test.py`, head copy | 1 | 267/269; chạy 269, bỏ qua 0; 682,739 s |
| Cùng lệnh, base `b29da0b` copy | 1 | 266/268; chạy 268, bỏ qua 0; 679,591 s |
| `CONG_CU_TEST_BAN_KINH=manh python3 -B ops/cong_cu_test.py`, head copy | 0 | 60/60 thực chạy; tổng 61, bỏ qua 1; 613,668 s; cổng cây thật đạt |
| `python3 -B review_rechecks.py previous` | 0 | 31 + 26 + 18 đầu vào sai bị chặn, sửa đúng xanh |
| `python3 -B review_current.py` | 0 | Ba ID dính bị chặn; 24/28 delimiter bị chặn, bốn xanh sai |
| `python3 -B review_probes.py matrix` | 0 | 96 ca: control xanh, 95 sai đỏ |
| `python3 -B review_grammar_alias.py grammar / aliases / unicode` | 0 | 138 ca / 12 phép đo / Unicode, `.yml`, 2.048 suffix |
| `python3 -B review_blocks.py` | 0 | 84 biến thể; không thêm xanh sai trong nhóm này |
| `python3 -B review_additional.py headings / prototype` | 0 | Sáu heading xanh sai; prototype chặn 18 đầu vào sai |
| `python3 -B review_mutations.py`; `python3 -B review_extra.py` | 0 | 29 + 4 mutant hợp lệ chết; 8 phản chứng bổ sung đỏ |
| `python3 -B review_real_static.py` | 0 | README: 1.362 ô / 1.631 vector không đổi |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head / base | 1 / 1 | Cùng 7 F401 + 2 F541; delta nội dung 0 |
| `compile()` với `warnings.catch_warnings`, head / base | 0 / 0 | Cùng hai SyntaxWarning cũ `\s`, `\d`; delta nội dung 0, chỉ dịch dòng |
| `git -C cay-kho diff --check b29da0b HEAD` | 0 | Không lỗi whitespace |
| `python3 -B review_audit.py regression` | 0 | Đủ marker 269/268; 268 ca chung giữ trạng thái; cùng hai lỗi ShellCheck |
| `python3 -B review_finalize.py` | 0 | 1.385 CLI có rc và tổng kết/bằng chứng dương khớp |
| `python3 -B review_audit.py source` | 0 | HEAD/status/băm nguồn và module trong bản sao giữ nguyên |

[Runner hồi quy](review_runner.py), [static/Ruff/warnings](review-evidence/static.json), [mã thoát driver](review-evidence/driver-completions.json), [audit CLI](review-evidence/cli-audit.json), [audit hồi quy](review-evidence/regression-audit.stdout).

Tính toàn vẹn: **8.468 tệp tracked khớp index** sau quy tắc checkout; 8.465 khớp blob nguyên byte, ba `.cmd` có chuyển đổi CRLF được `.gitattributes` khai báo. Snapshot băm byte thô giữ nguyên qua kiểm cuối. HEAD vẫn đúng reviewed SHA, tree `0a1c04b08981a9d5447332adb3697579016e5cfa`; status kể cả untracked/ignored rỗng; module head/base copy khớp revision. [Kết quả](review-evidence/source-integrity.json). Checkout được giữ chỉ đọc bằng kỷ luật của phiên, không tuyên bố có khóa OS cưỡng chế.

Môi trường Linux, Python **3.13.17**, Pandoc **3.1.3**, Ruff **0.16.9**; thiếu ShellCheck. Nguồn trả `--is-shallow-repository=true`, khác mô tả “đủ lịch sử”; các revision cần dùng đều đọc được. Windows thật và CI GitHub **not_run/not_measured**. Tool `environment_status` không có trong inventory hiện tại.

Reviewer: OpenAI Codex, phiên API độc lập với Executor; provider `openai_codex`, execution surface `codex_service`, transport `machine`. Không có runtime attestation để tự chứng nhận model ID/effort. Không push, không gọi API ghi GitHub, không merge/land/deploy/LIVE; chỉ ghi artifact review và bản sao ngoài `cay-kho/`.
