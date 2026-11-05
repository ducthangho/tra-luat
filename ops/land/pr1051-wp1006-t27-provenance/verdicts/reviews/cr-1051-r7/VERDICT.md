verdict: changes_requested
reviewed_sha: 2327d0634dffbe9d104717ae305f3ee44bae0705
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1051, lượt 7. Các phản chứng cụ thể của lượt 6 đã đóng thật, nhưng F1 còn ở cấp lớp: bộ đọc vẫn xác nhận hàng/tên khác với bảng người đọc thấy. Một lớp, một finding P2; ba biểu hiện dưới đây không được đếm thành ba finding.

Base `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`; lượt 5 `000e0fa2e29f973b8521f5510838f344c9e76c99`; lượt 6 `7c4bc1773f83d4c1fd8adc3566ff0b1b646b91ab`; reviewed tree `c993737d02a64a0055a6bd9c618dab9182405e61`. Diff toàn PR chỉ `ops/lease_publish_test.py`: 437 thêm / 24 bỏ; diff lượt 6 → 7: 18 thêm / 4 bỏ. Chỉ thị hiện tại cấp quyền review; tài liệu wp1006 và các verdict cũ là nguồn yêu cầu/lịch sử.

## Finding F1 — P2 — `wp1006-case-insensitive-listing-case-sensitive-consumer`

**Tệp:dòng:** `ops/lease_publish_test.py:1597` thay comment nhiều dòng trước khi tách hàng; `:1623` và `:1562` bỏ thông tin thụt lề; `:1700`, `:1715` kiểm nhãn link bằng chuỗi nguồn. Consumer tại `:1948` tin những hàng/tên đã được bộ đọc công nhận.

**Mô tả và tác động.** Thay comment bằng `\x01` ngăn nối hai mảnh của MỘT tên, nhưng vẫn xoá các dấu xuống dòng bên trong match DOTALL. Vì vậy có thể ghép verdict và id từ HAI hàng thành một hàng cảnh báo. Ví dụ bảng nguồn:

```markdown
| tệp verdict | id |
|---|---|
| `other.md` | `OTHER` |
| `x-verdict.md` <!--
| --> | `C1` |
```

Sau `_bang(..., giu_span=True)`, hai dòng cuối thành:

```text
{'tệp verdict': '`x-verdict.md` \x01', 'id': '`C1`'}
```

`_ten_tep` nhận tên đứng trước khoảng trắng, coi `\x01` là chú thích. Kết quả: caveat C1 được xác nhận cùng hàng với x-verdict.md. Render GFM bằng Pandoc cho HAI hàng riêng: hàng x-verdict.md có ô id RỖNG, hàng có C1 mang ô verdict là `-->`. Không có hàng cảnh báo đúng cặp tên/id. Đây là xanh sai thực sự, không phải trường hợp từ chối hẹp có chủ ý.

**Tái hiện đã chạy:**

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=ignore python3 review_extra.py
PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=ignore python3 review_labels.py
PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=ignore python3 review_confirm.py
```

Các driver cuối đều rc=0, xác nhận các kết quả trong bảng sau. Fixture ở ngoài kho, module head chép nguyên byte, Git riêng, receipt v2 đủ trường, băm đúng, reviewed commit tồn tại thật trong fixture; không mock validator/Git. URL và identity là dữ liệu thử.

| Input sai | `_kiem_muc_luc` | CLI t27 thật | t26 / v2 | Bằng chứng người đọc thấy |
|---|---|---|---|---|
| Comment cắt ngang hai hàng cảnh báo như trên | **Xanh sai** | **0, 1/1** | 0 / 0 | Verdict và C1 nằm trên hai hàng khác nhau |
| Thụt cả bảng cảnh báo 4 dấu cách | **Xanh sai** | **0, 1/1** | 0 / 0 | `<pre><code>`, không có bảng cảnh báo |
| Thụt cả bảng Mục lục 4 dấu cách | **Xanh sai** | **0, 1/1** | 0 / 0 | `<pre><code>`, không có bảng Mục lục |
| Nhãn `[_x_-verdict.receipt.yaml](_x_-verdict.receipt.yaml)` | **Xanh sai** | **0, 1/1** | 0 / 0 | Nhãn hiển thị **x-verdict.receipt.yaml**, mất hai `_` |
| Nhãn `[_x_-verdict.md](_x_-verdict.md)` ở mỗi cột verdict của ML/CB | **Xanh sai** | **0, 1/1**, mỗi vị trí | 0 / 0 | Nhãn hiển thị **x-verdict.md**, mất hai `_` |

Hai biểu hiện cuối minh hoạ thêm ranh giới còn thiếu của cùng lớp:

- `strip()` làm một bảng nằm trong khối mã thụt lề được đo như bảng thật, dù nhánh rào backtick/tilde đã loại được các ví dụ có fence.
- Nhãn link không bọc backtick vẫn được Markdown phân tích emphasis. So nhãn nguồn bằng basename không chứng minh tên hiển thị bằng basename. Fixture có cả `x-verdict.md` và `_x_-verdict.md`, nên hai danh tính thực sự hiện cùng một tên. Với receipt và hai cột verdict đều tái hiện; bọc nhãn bằng backtick sửa được, giữ nguyên verdict/receipt.

Cả bảy fixture được xác nhận thêm bằng `--chi-ca=t27_`: **rc=0, 3/3, bỏ qua=0**, gồm chính ca phản chứng mới của PR. Băm README trước/sau không đổi. Checker tại base, lượt 5 và lượt 6 cũng nhận các fixture này: đây là phần còn sót của F1, không khẳng định hồi quy vừa sinh trong commit lượt 7. Đây là lỗi chứng nhận mục lục/cảnh báo; không phải bypass lược đồ v2.

Bằng chứng: [driver xác nhận](review_confirm.py), [kết quả/parsed rows/historical controls](review-evidence/confirmed-findings.json), [fixture tối thiểu](review-evidence/fixtures/r7-multiline-cb-leading-pipe/ops/reviews/README.md), [HTML GFM](review-evidence/multiline-cb-leading-pipe.html), [CLI 3/3](review-evidence/confirm-multiline-cb-leading-pipe.stdout), [receipt v2 và các rc](review-evidence/strong-multiline-result.json), [các probe tiền xử lý](review-evidence/r7-extra-results.json), [ba nhãn emphasis](review-evidence/label-emphasis-results.json), [HTML nhãn cảnh báo](review-evidence/label-emphasis-warning.html).

**Đề xuất — vá ở đâu và thế nào.** Ở `_bang`, bảo toàn mọi ranh giới dòng khi che comment; có thể đánh dấu/loại từng phần comment trên từng dòng hoặc từ chối cấu trúc không phân định được, nhưng không co nhiều dòng thành một hàng mới. Xét ngữ cảnh khối mã thụt lề trước khi gọi `strip()`. Ở `_ten_tep`, ràng nhãn link là nội dung literal an toàn: nhãn chứa delimiter Markdown phải được bọc bằng code span, hoặc bị từ chối; không so nguyên source markup rồi coi đó là tên người đọc thấy. Có thể tiếp tục ngữ pháp cho phép, không cần mở thành bộ đọc Markdown tự do.

**Ca khoá.** Đưa bảng comment cắt hàng, hai bảng thụt lề và nhãn `_x_` ở ba vị trí qua `_kiem_muc_luc`/CLI, đòi đỏ đúng thiếu caveat/cột/bảng. Sửa thành một hàng thật, bỏ thụt lề, hoặc bọc nhãn backtick phải xanh với cùng receipt v2. Giữ đối chứng tên/id chỉ trong comment thật, bốn ca lượt 6 và so từng ô README thật. Prototype dữ liệu của reviewer chỉ giữ thêm newline trong replacement đã làm fixture comment đỏ đúng C1/cột id, đối chứng một hàng đúng xanh; README thật vẫn xanh. Đây là thử nghiệm trong scratch, không phải bản vá áp vào cây executor.

**Rủi ro.** Không chữa bằng bỏ lọc comment, bỏ `giu_span`, mở lại chữ trần, lấy basename cho Mục lục hoặc lowercase toàn tên. Việc nhận hẹp nhãn/indentation có thể làm một số cách trình bày hợp lệ đỏ; phải kiểm README hiện hành và báo rõ cách viết được nhận. Bảo toàn newline cần bao phủ cả comment nằm trong span và quanh fence; không để bước trước ngữ pháp tiếp tục sáng tạo tên/hàng.

## Đối chiếu lượt 6 và lượt 5

F1 P2 lượt 6: **đã vá thật ở bốn phản chứng cụ thể, chưa đóng lớp**.

| Chỉ đổi ô trong cùng fixture v2 | Helper / CLI t27 | t26 / v2 |
|---|---|---|
| `` `x-verdict<!-- h -->.receipt.yaml` `` ở cột receipt | Đỏ đúng cột receipt / rc=1 | 0 / 0 |
| `` `x-verdict<!-- h -->.md` `` ở cột verdict Mục lục | Đỏ đúng tên/cột verdict / rc=1 | 0 / 0 |
| Cùng span ở cột verdict cảnh báo | Đỏ đúng C1/cột id / rc=1 | 0 / 0 |
| `` `C<!-- h -->1` `` ở ô id | Đỏ đúng C1/cột id / rc=1 | 0 / 0 |

Tên/id chỉ trong comment thật đỏ; comment sau khoảng trắng của mục đúng xanh. Comment nhiều dòng bên trong tên không nối lại thành tên hợp lệ. Fence backtick, tilde và fence bốn backtick có ba backtick bên trong đều đỏ an toàn. Hai probe `\\|`/`\\\|` chuyển tên receipt sai cột đều đỏ. [Kết quả](review-evidence/r7-extra-results.json).

Lặp driver lượt 5 sau đổi bộ nối đường dẫn/kỳ vọng sau vá: **96 ca**, control xanh và **95 ca sai đỏ**, qua helper và CLI t27; t26 đều 1/1. Bao phủ ba ô tên, tham chiếu, HTML, ảnh, link trong span, entity, span dính tiền/hậu tố và hai hàng escaped pipe. [Driver](review_probes.py), [kết quả](review-evidence/table-probes.json).

Driver receipt v2 đầy đủ xác nhận sáu ô receipt sai cũ đỏ, t26/v2 xanh. Ba cặp gốc/con `y-verdict.md`, `VERDICT.md`, `report.md` đỏ đúng C9; hàng ghi đường dẫn riêng sửa được. Chiều ngược và hai thư mục con cùng basename đỏ đúng caveat; hai receipt trỏ CÙNG đường dẫn vẫn giữ alias dương. [Driver](review_finding.py), [kết quả](review-evidence/finding-results.json), [bổ sung alias](review-evidence/collision-extra.json).

## Ngữ pháp và README thật

`review_supplement.py grammar`: **138 ca**, 36 xanh và 102 đỏ đúng kỳ vọng; helper/CLI đồng ý. Đã ghép mục đúng với mục sai nhãn/đích, thử mục sau dấu phẩy, chú thích chứa code/link/ảnh/HTML/entity, nhãn chứa dấu lạ/escape/zero-width/bidi và đường có `..`, `./`, `//`. Các trường hợp đỏ an toàn không được tính finding. Phần còn lọt là nhãn emphasis ở F1. [Kết quả](review-evidence/grammar-results.json).

Unicode và `.yml`: đối chứng đầy đủ xanh; bỏ `é-verdict.md` đỏ đúng tên, đổi cảnh báo `report.yml` thành `report.yaml` đỏ CY. Trong **2.048** biến thể đuôi receipt, chỉ `alias.receipt.yaml` được chốt tên nhận. [Kết quả](review-evidence/unicode-yml-suffix.json).

So với consumer tại `000e0fa` trên cùng README thật:

| Phép đo | Kết quả |
|---|---|
| Ba cột tên | **1.362/1.362 cùng tập**, không thêm token, không có tập con thực sự |
| Bảng cảnh báo / Mục lục | 750 / 321 hàng parser; 306 hàng Mục lục có các cột tên |
| Kết luận từng hàng | **1.631 vector, delta 0**: 284 verdict đĩa + 612 receipt/verdict + 735 caveat |
| Alias basename mới | **0 tập alias đổi**, 22 đường dẫn con giữ kết luận; 50 hàng cảnh báo dùng basename |
| Checker toàn README / `_bang` mặc định | Cả hai checker xanh; bảng mặc định bằng nhau |

[Từng ô](review-evidence/real-r6-cells.json), [từng vector](review-evidence/real-r6-vectors.json), [tổng hợp](review-evidence/real-r6-summary.json). Tên `r6` của artifact kế thừa driver tham chiếu; module thực chạy là head lượt 7, không dùng kết quả lượt cũ.

## Răng của ca mới

`review_mutations.py`: control rc=0, 1/1; **22 mutant riêng rc=1, 0/1**. `review_listing_mutations.py`: control 1/1; **4 mutant riêng 0/1**. Tổng **26/26 bị giết bằng AssertionError ở phép kiểm liên quan**. Mỗi mutant là bản sao riêng ngoài kho, chạy selector/main thật qua wrapper trace; đã compile trước chạy, không tính SyntaxError là giết.

| Đột biến riêng | Bước bắt được trong ca tên mới |
|---|---|
| Bỏ IGNORECASE | (1), mất token alias HOA |
| Nhận ảnh; bỏ luật nhãn; nhãn `.` bất kỳ; nhận ký tự dính sau mục | (6), lần lượt ảnh / nhãn khac / `.md` sai đuôi / `+bak` được nhận sai |
| Span nhận khoảng trắng; bỏ chốt tên | (2), thông báo không nêu đủ lỗi tên và đuôi |
| Bỏ giữ span ML, CB, hoặc cả hai | (1) mất đối chứng đúng ở ML; hoặc (6) mất cảnh báo C1 đúng ở CB |
| Tách ô bỏ escape | (6), C1 tràn từ cột verdict sang id |
| Mục lục dùng basename | (6), link trỏ `con/x-verdict.md` thoả nhầm x ở gốc |
| Bỏ alias; tập danh tính chỉ ds_verdict | (6), mất đối chứng alias dương của verdict con |
| Alias không cần duy nhất | (6), nhận nhầm cảnh báo gốc cho verdict con |
| Alias quay chính sách lượt 5, chỉ chống trùng ds_verdict | (7), `VERDICT.md/C9` thoả nhầm verdict con |
| Bỏ chốt đuôi; bỏ gọi chốt receipt riêng t26/t27 | (1), alias HOA được nhận |
| Bỏ gọi chốt verdict t27 | (3), đỏ sai chốt thay vì hướng dẫn đổi tên |
| Sidecar không phân biệt case stem | (5), nhận `c-verdict.receipt.yaml` cho `c-VERDICT.md` |
| Quay lại xoá rỗng comment | (6), span receipt lượt 6 được nhận sai |
| Helper glob; bỏ is_file; riêng receipt/verdict t27 về glob | Ca listing, đúng biên đuôi HOA/file tương ứng |

[Cặp thay thế và wrapper](review_mutations.py), [rc/trace](review-evidence/mutation-results.json), [listing driver](review_listing_mutations.py), [listing rc/trace](review-evidence/listing-mutation-results.json). Những phép đo này xác nhận các ca có răng trong phạm vi đã phủ; CLI 3/3 trên fixture F1 chứng minh chúng chưa phủ các đường còn lọt.

## Đã đo

Các lệnh Python dùng `PYTHONDONTWRITEBYTECODE=1`; `TMPDIR` ở workspace ngoài `cay-kho/`; `GIT_OPTIONAL_LOCKS=0`. Ba suite đầy đủ dùng ba bản sao độc lập, `.git`/refs riêng chép từ nguồn, `core.abbrev=7` đặt chỉ trong bản sao. [Runner/argv/cwd/rc](review_runner.py), [bằng chứng](review-evidence/).

| Lệnh / phạm vi | rc | Kết quả |
|---|---:|---|
| `python3 ops/lease_publish_test.py`, bản sao head | **1** | **267/269**, chạy 269, bỏ qua 0; 901.719 s |
| Cùng lệnh, bản sao base `b29da0b` | **1** | **266/268**, chạy 268, bỏ qua 0; 902.722 s |
| `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py`, bản sao head riêng | **0** | **60/60 thực chạy**, tổng 61, bỏ qua 1; 819.285 s; gate cây thật, tự kiểm phân hạng/giàn giáo/song song đạt |
| `python3 review_probes.py matrix`; `python3 review_finding.py`; `python3 review_supplement.py collisions` | 0 / 0 / 0 | 96 ca cũ; v2 đầy đủ và các alias trùng đã bị chặn |
| `python3 review_supplement.py real / grammar / unicode` (ba lệnh) | 0 / 0 / 0 | 1.362 ô tên, 1.631 vector; 138 ca; Unicode/`.yml` và 2.048 biến thể đuôi |
| `python3 review_extra.py`; `python3 review_labels.py`; `python3 review_confirm.py` (lượt cuối) | 0 / 0 / 0 | Lượt 6 đỏ đúng chốt; tái hiện các đường xanh sai F1; control sửa hàng/nhãn xanh |
| `python3 review_mutations.py`; `python3 review_listing_mutations.py` | 0 / 0 | Control xanh, **22 + 4 mutant đỏ đúng chốt**, không có SyntaxError được tính là giết |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head/base | 1 / 1 | Delta F = 0 |
| `python3 review_static.py` | 0 | Compile/SyntaxWarning delta 0, diff check và doctrine rc=0 |
| `python3 review_finalize.py` | 0 | Marker/rc, delta ca chung, băm module và snapshot nguồn |

Hai suite lease đầy đủ đều **failed**, không khai N/N đạt. Cùng hai ca đỏ, thông báo bằng nhau:

- `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck`: `KHÔNG ĐO ĐƯỢC: thiếu shellcheck`.
- `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`: cùng thiếu công cụ, chưa tới phép đo consumer ShellCheck.

Phần phép đo ShellCheck là **not_measured do môi trường**, không quy thành hồi quy PR. **268 ca chung không đổi trạng thái**; thêm đúng ca tên biên nhận mới đạt, không thêm thất bại/bỏ qua. `t125` đạt cả hai phía. Đã đối chiếu đủ 269/268 cặp marker cấp ngoài, đúng thứ tự/tên, tách các lượt A/B lồng. [So sánh đầy đủ](review-evidence/full-comparison.json), [head log](review-evidence/full-head.stdout), [base log](review-evidence/full-base.stdout).

Cong: `t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet` **skipped**, vì fixture INDEX chưa hoà giải không dựng được (`stage={'0'}`); không gọi là 61/61. **490 mutant bán kính của cong: giao mảnh / not_measured trong lượt này**, không phải 490 đạt. Chế độ `manh` chạy các ca nền và tự kiểm/gate như CI; không chứng nhận full radius mặc định. [Invocation và môi trường](review-evidence/full-cong.invocation.json), [rc](review-evidence/full-cong.result.json), [log cuối](review-evidence/full-cong.stdout).


Ruff không xanh tuyệt đối: mỗi bên 7 F401 + 2 F541; delta code/message bằng 0. Compile không có SyntaxError; mỗi bên đúng hai SyntaxWarning cũ (`invalid escape sequence '\s'`, `'\d'`), delta nội dung bằng 0, chỉ dịch dòng. [Static results](review-evidence/static-results.json). `git diff --check b29da0b HEAD` rc=0; `doctrine-scan --root .` trong bản sao head rc=0.

`review_finalize.py` rc=0 tự kiểm **573 CLI chọn ca có invocation/result** với marker dương và số ca thực chạy; mutant được kiểm riêng bằng rc/trace. Ba bản sao suite giữ nguyên byte module: head/cong khớp head, base khớp blob `b29da0b`. [Tổng hợp](review-evidence/final-summary.json), [marker CLI](review-evidence/cli-marker-audit.json).

Snapshot trước/sau có **8,468 tệp tracked** trùng mode/băm hoặc đích symlink; HEAD/tree, diff/index và danh sách untracked/ignored không đổi, delta 0. HEAD nguồn ở trạng thái detached và vẫn khớp SHA dòng 2. Snapshot không băm toàn bộ `.git`, không chứng nhận OS cưỡng chế read-only hay lịch sử chưa từng ghi rồi hoàn nguyên. [Snapshot trước](review-evidence/source-before.json), [sau](review-evidence/source-after.json), [delta](review-evidence/source-delta.json).


Môi trường Linux, Python 3.13.17; Ruff, actionlint và Pandoc có sẵn; ShellCheck vắng. [Môi trường](review-evidence/environment.json). Kho được cấp báo shallow, trái mô tả đủ lịch sử; không sửa `.git` nguồn hay gỡ marker shallow. Những revision cần review/diff đều đọc được. Windows thật và CI GitHub: **not_run/not_measured**; các receipt v2 dương trong fixture không thay việc chứng nhận toàn kho thật/CI.

Reviewer: Codex, phiên API độc lập; provider `openai_codex`, execution surface `codex_service`, transport `machine`. Model/effort phục vụ thực tế không có runtime attestation trong bằng chứng này: `KHONG_DO_DUOC`. Theo `CLAUDE.md` §Quy trình sửa code bước 5, agent `tl_auditor` chỉ đọc/tiêu hoá log hồi quy; phiên chính tự đọc mã, dựng/chạy phản chứng và quyết định finding. Không dùng context Executor.

Chỉ ghi script, fixture/bản sao và verdict ngoài `cay-kho/`; không push, không gọi API GitHub, không merge/deploy/LIVE. Verdict không tự tạo approval/state hay quyền land.
