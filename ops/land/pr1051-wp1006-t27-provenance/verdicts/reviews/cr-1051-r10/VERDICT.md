verdict: changes_requested
reviewed_sha: b5a51fc7ac53da54d9b24b0b7b84985915c945d4
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1051, lượt 10. **31 phản chứng lượt 9 và 26 phản chứng lượt 8 đã được chặn. Tuy nhiên, còn hai đường cùng lớp t27 xanh sai: ID dính code span, và hàng gạch chứa ký tự trắng Unicode.** Giữ một finding P2 theo ID lịch sử của lớp lỗi này; không tính các trường hợp đỏ an toàn thành finding.

Base: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`. Reviewed tree: `ea6d1129d2f9795ea04e70816b51eed423a5e96c`. Toàn PR chỉ sửa `ops/lease_publish_test.py` (571 thêm / 39 bỏ); lượt 9 → 10 là 34 thêm / 6 bỏ. `PROMPT.md` là authority của review này; không dùng lease lịch sử làm quyền ghi.

## F1 — P2 — `wp1006-case-insensitive-listing-case-sensitive-consumer`

**Vị trí:** `ops/lease_publish_test.py:1893` và `:1895`, `_id_hien_thi`, consumer tại `:1995`; `:1562` và `:1567`, `_tach_o`, consumer nhận hàng gạch trong `_bang` tại `:1612`.

**Biểu hiện A — ID dính code span:** phần phân cách `[ \t]*,?[ \t]*` có thể khớp chuỗi rỗng. Vì vậy, `_id_hien_thi` nhận nguồn `` `C1``OTHER` `` như hai ID `C1` và `OTHER`. GFM lại dựng **một** code span có nội dung `C1``OTHER`: hai nháy liền nhau ở giữa là một backtick string độ dài hai, không đóng code span mở bằng một nháy. Bảng không có ID độc lập `C1`, nhưng t27 vẫn xác nhận caveat `C1` đã được nâng lên đúng cột. Quy tắc delimiter theo [GFM §6.3](https://github.github.com/gfm/#code-spans); đã kiểm render địa phương bằng Pandoc GFM, không khai đã đo UI GitHub.

**Tái hiện tối thiểu:** với verdict `x-verdict.md`, receipt hợp lệ có caveat `id: C1`, giữ Mục lục đúng và thay hàng cảnh báo bằng:

```text
| tệp verdict | id |
|---|---|
| `x-verdict.md` | `C1``OTHER` |
```

Kết quả đã chạy:

- `_id_hien_thi` cho `{'C1', 'OTHER'}`; HTML có `<td><code>C1``OTHER</code></td>`.
- `_kiem_muc_luc`: xanh sai.
- CLI `python3 ops/lease_publish_test.py --chi-ca=t27_canh_`: **rc=0, 1/1**.
- Toàn selector `--chi-ca=t27_`: **rc=0, 3/3**; ca phản chứng mới của PR không phát hiện lỗi.
- t26: **rc=0, 1/1**; validator v2 thật: **rc=0**. Đây không phải fixture bỏ qua schema hoặc băm.
- Sửa ô thành `` `C1` `` trên cùng verdict/receipt làm t26/t27/v2 xanh đúng.

Đã xác nhận **ba biến thể**: ID ở đầu, cuối và giữa chuỗi span dính nhau. Nội dung ô render lần lượt là `C1``OTHER`, `OTHER``C1`, `OTHER``C1``ELSE`; không trường hợp nào có ID `C1` độc lập. Tất cả đều có Git riêng, verdict đã commit, băm đúng và receipt v2 đủ trường; URL/identity là dữ liệu thử. Module suite chép nguyên byte reviewed head, không mock Git hoặc validator. README không bị phép thử sửa ngoài thay đổi fixture chủ ý.

**So lịch sử:** checker tại `b29da0b`, `000e0fa` và **lượt 9 `5c6b5e2` đều đỏ đúng caveat trên cả ba đầu vào này**. Đường xanh sai này mới được đưa vào khi thay `.split()` bằng `_id_hien_thi` ở lượt 10. Các mẫu cũ của lượt 9 đã đóng, nhưng finding chưa đóng ở cấp lớp.

**Cách chạy lại:** từ thư mục chứa verdict, chạy `PYTHONDONTWRITEBYTECODE=1 python3 review_rechecks.py finding` (driver rc=0 xác nhận tái hiện xanh sai, không có nghĩa chốt đã được sửa). Fixture giữ nguyên đầu vào sai tại [README](review-evidence/fixtures/id-adjacent-first/ops/reviews/README.md). Có thể vào thư mục fixture và chạy CLI t27 trực tiếp.

Bằng chứng: [driver](review_rechecks.py), [ba kết quả cùng đối chứng lịch sử](review-evidence/finding-adjacent-id.json), [CLI toàn t27](review-evidence/id-adjacent-first-all-t27.stdout), [HTML](review-evidence/id-adjacent-first.html), [đọc lại ô HTML](review-evidence/finding-render-audit.json).

**Biểu hiện B — hàng gạch giả được chuẩn hóa thành hợp lệ:** lượt 10 đã sửa ngữ nghĩa dòng trống ở `_bang`, nhưng `_tach_o` vẫn gọi `dong.strip()` và `x.strip()`. Thay delimiter chuẩn bằng chuỗi Python `"|\u00a0---|---|"` trong CB hoặc ML: NBSP bị xóa, `la_gach` nhận `---`, và t27 xanh dù GFM không dựng bảng tại mục đó. Tương tự với `"|---\u00a0|---|"` hoặc `"|---|---|\u00a0"`; dạng cuối bị `dong.strip()` xóa ký tự ngoài pipe. Đây là thay đổi cấu trúc hiển thị, không phải khác biệt thẩm mỹ ở tên. Đối chiếu [GFM §4.10](https://github.github.com/gfm/#tables-extension).

Đã chạy **28 fixture v2 đầy đủ**: 12 ký tự U+000B, U+000C, U+0085, U+00A0, U+1680, U+2000, U+2003, U+2028, U+2029, U+202F, U+205F, U+3000 đứng trước dấu gạch đầu tiên × hai mục = 24; thêm NBSP sau dấu gạch và ngoài pipe cuối × hai mục = 4. Mỗi fixture: `_kiem_muc_luc` xanh sai; CLI t27 **rc=0, 1/1**; toàn t27 **rc=0, 3/3**; t26/v2 **rc=0**; sửa hàng gạch về ASCII thì xanh đúng. Render chỉ còn **một bảng** ở mục không bị sửa, còn mục bị sửa là đoạn văn. Hai mẫu NBSP đại diện CB/ML cũng xanh ở `b29da0b`, `000e0fa`, `5c6b5e2`: đây là đường còn mở của lớp lỗi cũ, khác với hồi quy ID ở A.

Chạy lại bằng `PYTHONDONTWRITEBYTECODE=1 python3 review_delimiters.py`. [Driver](review_delimiters.py), [28 kết quả](review-evidence/finding-delimiters.json), [README NBSP](review-evidence/fixtures/delimiter-ml-prefix-xa0/ops/reviews/README.md), [HTML mất bảng ML](review-evidence/delimiter-ml-prefix-xa0.html). Không tách A/B thành hai finding vì cùng một lớp gate xác nhận nội dung không hiển thị đúng trong bảng.

**Đề xuất:** trong `_id_hien_thi`, bắt buộc phân cách giữa hai mục phải tiêu thụ ít nhất một ký tự: một hoặc nhiều space/tab, hoặc một dấu phẩy với space/tab tùy chọn. Chẳng hạn, thay phần phân cách bằng `(?:[ \t]+|[ \t]*,[ \t]*)`; giữ việc fullmatch toàn ô và từ chối dạng ngoài ngữ pháp. Với cấu trúc bảng, thay hai lần trim Unicode ở `_tach_o` bằng trim space/tab rõ ràng, hoặc kiểm nguyên bản hàng gạch trước mọi chuẩn hóa có thể xóa ký tự cấu trúc. Owner đề xuất: maintainer của `ops/lease_publish_test.py`.

**Ca khóa:** bổ sung ba ô ID dính trên qua `_kiem_muc_luc`/CLI, đòi đỏ tại caveat; đối chứng một span, hai span cách space/tab, dấu phẩy và dấu phẩy có khoảng trắng phải xanh. Bổ sung 28 delimiter Unicode qua consumer cùng đối chứng ASCII. [Prototype](review_prototype.py) chỉ ghi ngoài `cay-kho/`, đã chạy: **31/31 sai đỏ bằng AssertionError, 31/31 sửa đúng xanh**, README thật xanh, ca tên mới **rc=0, 1/1**. [Kết quả](review-evidence/prototype.json). Prototype chưa chạy toàn suite và không phải patch đã áp vào branch Executor; Executor cần tự dẫn xuất và đo lại toàn gate.

## Đối chiếu các yêu cầu còn lại

| Phạm vi | Kết quả tự đo |
|---|---|
| 31 fixture lượt 9 | **31/31 đỏ** qua helper, CLI t27 1 ca và toàn selector t27; t26/v2 xanh, sửa đúng xanh. Bao gồm 24 dòng trắng Unicode, hai bảng thứ hai, hai rào mã và ba ID trong thuộc tính/đích link. |
| 26 fixture lượt 8 | **26/26 đỏ** qua cùng các consumer; đối chứng sửa đúng xanh. Giữ nguyên dữ liệu thử từ script tham chiếu, kể cả rào phụ để phục hồi trạng thái ở mục CB. |
| Lượt 6–7 | **18 đầu vào sai đỏ**, bao gồm ba ô tên và ID có comment, comment cắt ngang hàng, bảng CB/ML thụt space/tab, ba nhãn `_x_` trần; sửa đúng xanh. Hai bypass tiêu đề giả trong rào rồi comment ghép hàng cũng đỏ. |
| Lượt 5 | Ma trận **96 ca** qua helper/CLI: control xanh, **95 sai đỏ**. Sáu mẫu đại diện được chạy thêm với receipt v2 đầy đủ; t26/v2 xanh, t27 đỏ, sửa đúng xanh. |
| Ngữ pháp tên | **138 ca**, 36 xanh / 102 đỏ đúng kỳ vọng, qua helper/CLI. Phủ mục ghép đúng/sai, mục sau phẩy, chú thích chứa code/link/ảnh/HTML/entity, nhãn bọc nháy có ký tự lạ/zero-width/bidi/escape và đường `..`/`./`/`//`. Không tìm thêm xanh sai trong các ô tên đã thử. |
| Alias | **12 phép đo**: va gốc/con với `y-verdict.md`, `VERDICT.md`, `report.md` và chiều ngược đều đỏ; hai thư mục con cùng basename đỏ; đường dẫn riêng sửa được; hai receipt cùng một danh tính vẫn giữ alias dương. |
| Unicode / `.yml` | Fixture đủ xanh; bỏ tên `é-verdict.md` hoặc đổi cảnh báo `report.yml` sang `report.yaml` đỏ đúng chốt. **2.048** biến thể suffix: chỉ `alias.receipt.yaml` được chốt tên nhận. |
| Cấu trúc bổ sung | **84 biến thể** qua helper/CLI và render GFM: tab, rào/khối mã thụt lề, blockquote/danh sách, heading trùng/giả/setext, bảng thứ hai, hàng sau dòng trống, ký tự vô hình. 26 trường hợp xanh có bảng và ô cần kiểm thực sự hiển thị; không tìm thêm xanh sai trong nhóm này. |

[31 ca](review-evidence/r9-recheck.json), [26 ca](review-evidence/r8-recheck.json), [lượt 6–7](review-evidence/r6-r7-recheck.json), [96 ca](review-evidence/table-probes.json), [v2 lượt 5 / bypass comment](review-evidence/previous-extra.json), [138 ca ngữ pháp](review-evidence/grammar.json), [alias](review-evidence/aliases.json), [Unicode/suffix](review-evidence/unicode-yml.json), [84 cấu trúc và các bảng render](review-evidence/blocks.json).

### README thật

So trên **cùng README head** bằng parser/consumer `000e0fa` và reviewed head:

- CB **750 hàng**, ML **321 hàng**; dữ liệu hàng với `giu_span=True` và dạng mặc định đều bằng nhau.
- **1.362/1.362 ô tên cùng tập**; không có token mới hoặc tập con thực sự.
- **1.631 vector kết luận theo hàng** có delta **0** (284 verdict đĩa + 612 receipt/verdict + 735 caveat).
- ID ở cả 750 ô giữ cùng tập; alias không đổi tập hoặc kết luận nào; **22 đường dẫn con** giữ nguyên kết quả.
- Checker lịch sử và head đều xanh trên README thật.

[Từng ô](review-evidence/real-cells.json), [từng vector](review-evidence/real-vectors.json), [tổng hợp](review-evidence/real-summary.json).

### Răng của ca mới

**27/27 mutant** dưới đây biên dịch được và làm ca tên mới đỏ bằng **AssertionError**, CLI **rc=1, 0/1**; control **rc=0, 1/1**. Đã đọc traceback để kiểm đúng bước, không tính SyntaxError hoặc lỗi giàn giáo là giết.

| Đột biến riêng | Bước bắt được |
|---|---|
| Bỏ IGNORECASE | (1) |
| Nhận ảnh như link; bỏ luật nhãn; nhãn `.` bất kỳ; nhận ký tự dính sau mục | (6) |
| Span nhận khoảng trắng; bỏ chốt tên | (2) |
| Bỏ giữ span riêng ML / CB | (1) / (6) |
| Tách ô bỏ escape; ML dùng basename | (6) |
| Bỏ alias; alias không cần duy nhất; danh tính chỉ lấy từ `ds_verdict` | (6) |
| Alias chỉ chống va với `ds_verdict` như lượt 5 | (7) |
| Bỏ chốt suffix; bỏ gọi chốt receipt riêng t26 / t27 | (1) |
| Bỏ gọi chốt verdict t27; gộp case stem sidecar | (3) / (5) |
| Bỏ chốt comment; bỏ chốt thụt lề; bỏ kiểm số ô delimiter | (6) |
| Quay về dòng trắng Unicode; rào đóng dùng strip; bỏ luật info backtick; ID quay lại token thô | (8) |

Thêm **4/4 mutant listing** (helper quay glob, bỏ `is_file`, riêng receipt t27 quay glob, riêng verdict t27 quay glob) cũng compile được, đỏ bằng AssertionError ở ca listing. Các chốt đã phủ có răng; ba fixture F1 vẫn toàn t27 3/3 chứng minh còn thiếu ca ở ranh giới delimiter ID.

[Cặp thay thế và runner](review_mutations.py), [traceback / bước / mã thoát của 27 mutant](review-evidence/mutation-results.json), [listing](review-evidence/listing-mutants.json).

## Đã đo

Các suite dùng bản sao head/base có `.git`, index và refs riêng ngoài `cay-kho/`; object qua alternate chỉ đọc. Module suite khớp nguyên byte revision tương ứng. CLI dùng `PYTHONDONTWRITEBYTECODE=1`, UTF-8, và `TMPDIR` dưới `review-evidence/`. Mã thoát driver xác nhận phép đo không được nhầm với mã thoát chốt đang thử.

Hai suite lease đầy đủ đều **failed**, không khai N/N đạt: head **267/269**, base **266/268**, không bỏ qua. Cùng hai lỗi thiếu ShellCheck, thông báo bằng nhau:

- `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck`: thiếu `shellcheck`.
- `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`: chưa tới consumer ShellCheck vì cùng thiếu công cụ.

Phần ShellCheck **not_measured do môi trường**; không kết luận là hồi quy PR và không đổi thành pass. **268 ca chung giữ nguyên trạng thái**, thêm đúng ca tên mới đạt. Đã đối chiếu toàn bộ marker vào/ra cấp ngoài với danh sách `@ca` từ AST; `t125` A/B đạt ở cả head/base. [Delta và lỗi nguyên văn](review-evidence/lease-delta.json).

Cong chạy xong theo chế độ gate của CI `CONG_CU_TEST_BAN_KINH=manh`: **rc=0, 60/60 ca thực chạy**, tổng 61, bỏ qua 1, tiền kiểm bỏ qua 0; tự kiểm giàn giáo/song song và cổng cây thật đạt. `t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet` **skipped** vì không dựng được INDEX chưa hòa giải (`stage={'0'}`). Bán kính **490** đột biến được giao các job mảnh/gom trong chế độ này: **not_measured**, không tính vào số mutant đã giết ở review này. Lượt cong mặc định trước đó đã bị ngắt bằng Ctrl-C (outer rc=130), không được tính là một lượt pass; kết luận dựa trên lượt gate hoàn tất. [Tổng hợp hồi quy](review-evidence/regression-summary.json), [stdout cong gate](review-evidence/cong-cu-head-gate.stdout).

| Lệnh / phạm vi | rc | Kết quả |
|---|---:|---|
| `python3 ops/lease_publish_test.py`, head copy | 1 | 267/269; chạy 269, bỏ qua 0; 786.082 s |
| Cùng lệnh, base copy | 1 | 266/268; chạy 268, bỏ qua 0; 782.055 s |
| `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py`, head copy | 0 | 60/60 thực chạy; tổng 61, bỏ qua 1; 457.956 s; cổng cây thật đạt |
| `python3 review_rechecks.py finding` | 0 | Ba xanh sai; t26/v2 và sửa đúng xanh; helper lịch sử đỏ |
| `python3 review_rechecks.py previous` | 0 | 31 + 26 + 18 phản chứng bị chặn, sửa đúng xanh |
| `python3 review_delimiters.py` | 0 | 28 xanh sai ở delimiter; t26/v2 và sửa đúng xanh |
| `python3 review_probes.py matrix` | 0 | 96 ca: 1 xanh / 95 đỏ |
| `python3 review_extra.py` | 0 | 8 phản chứng v2/comment + 4 mutant listing |
| `python3 review_grammar_alias.py grammar / aliases / unicode` | 0 / 0 / 0 | 138 ca / 12 phép đo alias / Unicode và 2.048 suffix |
| `python3 review_blocks.py` | 0 | 84 biến thể, không thêm xanh sai |
| `python3 review_mutations.py` | 0 | 27 mutant compile hợp lệ, chết đúng bước |
| `python3 review_real_static.py` | 0 | 1.362 ô / 1.631 vector không đổi; static delta 0 |
| `python3 review_prototype.py` | 0 | 31 phản chứng đỏ, 31 sửa đúng/README thật/ca mới xanh |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head / base | 1 / 1 | Mỗi bên 7 F401 + 2 F541; delta nội dung 0 |
| `compile()` với `warnings.catch_warnings`, head / base | 0 / 0 | Hai SyntaxWarning cũ `\s`, `\d`; delta nội dung 0, chỉ dịch dòng |
| `git -C cay-kho diff --check b29da0b HEAD` | 0 | Không lỗi |
| `python3 review_finalize.py` | 0 | Đủ marker 269/268 ca; 268 ca chung không đổi; 1.165 CLI chọn ca có rc/tổng kết khớp; nguồn sạch |

[Runner hồi quy](review_runner.py), [static / Ruff / warnings](review-evidence/static.json), [facts và phiên bản công cụ](review-evidence/facts.json).

Kiểm cuối: **8.468 tệp tracked trùng băm**, HEAD không đổi, status gồm cả untracked/ignored rỗng; hai module trong bản sao khớp byte Git của head/base. [Nguồn](review-evidence/source-final-integrity.json), [bản sao](review-evidence/copy-integrity.json), [audit CLI](review-evidence/cli-audit.json). Checkout được đối xử chỉ đọc bằng kỷ luật của phiên; không tuyên bố đây là chứng nhận OS cưỡng chế read-only.

Môi trường: Linux, Python 3.13.17, Pandoc 3.1.3, Ruff 0.16.9; không có ShellCheck hoặc Windows runner. Nguồn trả `--is-shallow-repository=true`, khác lời mô tả “đủ lịch sử”; mọi revision cần dùng trong review vẫn đọc được. Windows thật và CI GitHub **not_run/not_measured**, không suy từ Linux. `environment_status` không có trong tập công cụ hiện tại.

Reviewer: OpenAI Codex, phiên API độc lập với Executor; provider `openai_codex`, execution surface `codex_service`, transport `machine`. Không có runtime attestation để tự chứng nhận model ID/effort. Không push, không gọi API ghi GitHub, không merge/land/deploy/LIVE; chỉ ghi artifact review và bản sao ngoài `cay-kho/`.
