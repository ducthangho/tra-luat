verdict: changes_requested
reviewed_sha: 7c4bc1773f83d4c1fd8adc3566ff0b1b646b91ab
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1051, lượt 6. Các phản chứng cụ thể của lượt 5 đã bị chặn thật, nhưng lớp F1 chưa đóng: bước xoá comment của `_bang` vẫn có thể biến một tên KHÁC trong code span thành tên hợp lệ trước khi ngữ pháp mới được áp dụng. Một lớp, một finding P2. Ngưỡng theo PROMPT: approve chỉ khi 0 finding P0–P3.

Base `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`; lượt 5 `000e0fa2e29f973b8521f5510838f344c9e76c99`; reviewed tree `3f186d609be63f926dab841e6a3417df4fab2c7e`. Diff toàn PR: 422 dòng thêm / 23 dòng bỏ; diff lượt này: 140 thêm / 71 bỏ. Cả hai chỉ thay `ops/lease_publish_test.py`. Chỉ thị hiện tại cấp quyền review; đặc tả wp1006 và các verdict được đọc như nguồn yêu cầu/lịch sử.

## Finding F1 — P2 — `wp1006-case-insensitive-listing-case-sensitive-consumer`

**Tệp:dòng:** `ops/lease_publish_test.py:1593` xoá comment trên toàn văn bản, kể cả nội dung code span; `:1861`, `:1862` đưa các ô đã bị viết lại vào consumer; ngữ pháp tại `:1696` và phép kiểm cảnh báo tại `:1944` không còn nhận được chuỗi nguyên bản.

**Mô tả.** Trong code span Markdown, `<!-- h -->` là chữ hiển thị, không phải comment bị ẩn. Nhưng `_bang` chạy `re.sub(r"<!--.*?-->", "", van, flags=re.S)` trước khi đọc cấu trúc. Ví dụ:

```text
ô nguồn:        `x-verdict<!-- h -->.receipt.yaml`
sau _bang:      `x-verdict.receipt.yaml`
_ten_tep(nguồn): set()
_ten_tep(sau):   {'x-verdict.receipt.yaml'}
```

Vì thế allowlist của `_ten_tep` đúng khi gọi riêng nhưng không bảo vệ được đầu vào thực tế. Mục lục/cảnh báo hiển thị tên khác vẫn được xác nhận đúng cột, đúng hàng. Đây là lỗi kiểm mục lục; không phải bypass lược đồ v2.

**Tái hiện đã chạy:** `PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=ignore python3 review_finding_r6.py`, rc=0 của driver xác nhận tái hiện. Fixture có Git riêng, receipt v2 đủ trường, băm đúng, commit neo có thật trong fixture và URL/identity là dữ liệu thử. Module head được chép nguyên byte; gọi validator thật, không mock Git hoặc nới schema.

| Vị trí đổi duy nhất | Ô tên sai | Helper | CLI t27 | t26 / v2 |
|---|---|---|---|---|
| Biên nhận trong Mục lục | `` `x-verdict<!-- h -->.receipt.yaml` `` | Xanh sai | rc=0, 1/1 | 0 / 0 |
| Verdict trong Mục lục | `` `x-verdict<!-- h -->.md` `` | Xanh sai | rc=0, 1/1 | 0 / 0 |
| Verdict trong bảng cảnh báo | `` `x-verdict<!-- h -->.md` `` | Xanh sai | rc=0, 1/1 | 0 / 0 |

Chạy cả `--chi-ca=t27_` trên từng cây sai vẫn **rc=0, 3/3, bỏ qua=0**: hai ca phản chứng hiện có không phát hiện đường này. Đã băm README trước/sau mỗi lượt để xác nhận đúng input sai không đổi. Cùng cơ chế còn biến ô id `` `C<!-- h -->1` `` thành C1 và thoả caveat C1.

`pandoc --from=gfm --to=html <README fixture>` rc=0 cho ô receipt `<code>x-verdict&lt;!-- h --&gt;.receipt.yaml</code>`: người đọc thấy nguyên chuỗi khác. Đối chứng đổi về tên đúng xanh; code span `two x-…` đỏ; tên chỉ nằm trong comment thật bên ngoài span đỏ. T26/v2 đều xanh ở các đối chứng, nên lỗi được cô lập ở mục lục. Helper base và lượt 5 cũng nhận các fixture span-comment: đây là phần còn sót của F1, không khẳng định hồi quy mới do commit lượt 6.

Bằng chứng: [driver](review_finding_r6.py), [kết quả đầy đủ](review-evidence/finding-r6-results.json), [ba lượt t27 3/3 và băm input](review-evidence/finding-r6-all-t27.json), [README tối thiểu](review-evidence/fixtures/r6-finding-receipt-span-comment/ops/reviews/README.md), [HTML render](review-evidence/r6-receipt-span-comment.html). Sáu probe bổ sung ở ba ô cũng xác nhận comment trong span và trong nhãn code của link đều được nhận sau khi `_bang` viết lại: [kết quả](review-evidence/comment-probes.json).

**Đề xuất.** Sửa ở `_bang`, trước khi ngữ pháp nhận ô: giữ nguyên nội dung code span khi xử lý comment, và chỉ loại HTML comment thực sự nằm ngoài span. Nếu tiếp tục chọn cách nhận hẹp, có thể từ chối ô có cấu trúc chưa phân định được; tuyệt đối không xoá rỗng rồi nối các mảnh thành một tên mới. Không chỉ thêm một nhánh từ chối ở `_ten_tep`, vì đến đó dấu hiệu đã mất. Giữ chốt bỏ tên/id chỉ nằm trong comment HTML thật.

**Ca khoá và rủi ro.** Đưa ba ô trên và id span-comment qua `_kiem_muc_luc`/CLI, đòi đỏ đúng tên/cột/caveat; đổi ô đúng phải xanh với cùng receipt v2. Giữ chiều âm cho tên/id chỉ còn trong comment thật và đối chứng README hiện hành. Đột biến quay lại xoá comment toàn văn bản phải bị ca mới giết. Cần xét span một/nhiều backtick và bảng/rào mã để tránh tạo thêm phép viết lại trước allowlist. Reviewer chỉ cung cấp dữ liệu phản chứng; không sửa cây executor.

## ĐỐI CHIẾU LƯỢT TRƯỚC

F1 P2 lượt 5: **VÁ HỜ ở cấp lớp; các biểu hiện cụ thể đã vá thật**. Kết quả tự đo:

- Lặp lại driver lượt 5, chỉ đổi bộ nối đường dẫn và kỳ vọng sau vá: 96 ca bảng gồm control xanh và 95 ô/hàng sai đỏ đúng chốt. Bao phủ ba ô tên, link tham chiếu, HTML, ảnh, link trong span, entity, tiền/hậu tố dính và hai hàng `\|`. Helper và CLI đồng ý; t26 vẫn 1/1.
- Driver v2 đầy đủ: sáu ô receipt sai cũ đều t27 đỏ, t26/v2 xanh. Ba cặp gốc/con `y-verdict.md`, `VERDICT.md`, `report.md` đều đỏ C9; thêm cảnh báo ghi đường dẫn con làm xanh. Chiều ngược, hai thư mục con cùng basename cũng đỏ đúng caveat. Mỗi đường dẫn có hàng riêng làm xanh.
- Hai receipt cùng trỏ MỘT đường dẫn con vẫn dùng được alias basename: tập danh tính được deduplicate theo đường dẫn, không đếm số receipt thành xung đột.

Bằng chứng: [driver lượt 5 đã điều chỉnh](review_probes.py), [96 ca](review-evidence/table-probes.json), [driver v2](review_finding.py), [kết quả v2](review-evidence/finding-results.json), [bổ sung alias](review-evidence/collision-extra.json).

## Ngữ pháp, README thật và răng của ca khoá

`python3 review_supplement.py grammar` rc=0: **138 ca**, gồm 36 đối chứng xanh và 102 ca đỏ an toàn, qua cả helper và CLI. Đã thử ghép mục hợp lệ với mục lệch nhãn/đích, mục sai sau dấu phẩy, chú thích chứa code/link/ảnh/HTML/entity, nhãn có dấu lạ/escape/zero-width/bidi và đích có `..`, `./`, `//`. Không tìm đường xanh sai mới trong chính scanner trên ô nguyên bản; F1 nằm ở bước tiền xử lý làm mất nguyên bản. Các trường hợp từ chối hẹp không được tính là finding. [Chi tiết](review-evidence/grammar-results.json).

Đối chứng v2 Unicode, tên khác case/dấu và `.yml` xanh; bỏ hàng `é-verdict.md` đỏ đúng tên, đổi cảnh báo `report.yml` thành `report.yaml` đỏ CY. Duyệt 2.048 biến thể đuôi receipt, chỉ `alias.receipt.yaml` được chốt tên nhận. [Kết quả](review-evidence/unicode-yml-suffix.json).

`python3 review_supplement.py real` rc=0, so với consumer thật tại `000e0fa`:

| Phép đo | Kết quả |
|---|---|
| Ba cột tên trên README thật | 1.362/1.362 ô cùng tập; 0 ô thêm token, 0 tập con thực sự |
| Hai bảng | 750 hàng cảnh báo; 321 hàng dưới Mục lục, trong đó 306 có các cột tên; `_bang` mặc định bằng nhau |
| Kết luận theo từng hàng | 1.631 vector: 284 verdict trên đĩa + 612 yêu cầu receipt/verdict + 735 caveat; 0 delta |
| Alias | 0 tập alias thay đổi; 22 đường dẫn con, 50 hàng cảnh báo dùng basename vẫn giữ kết luận |
| Checker toàn README | Cả lượt 5 và head xanh |

[Từng ô](review-evidence/real-r6-cells.json), [từng vector](review-evidence/real-r6-vectors.json), [tổng hợp](review-evidence/real-r6-summary.json). Không dùng kết quả trên dữ liệu thật để phủ định phản chứng F1.

`python3 review_mutations.py` và lượt bổ sung chính sách alias cũ: control **rc=0, 1/1**; **21 mutant riêng rc=1, 0/1**. Thêm `python3 review_listing_mutations.py`: control 1/1; **4 mutant riêng 0/1**. Tổng **25/25 bị giết**, không có SyntaxError được tính là giết. Mỗi bản nằm ngoài `cay-kho/`; runner dùng CLI/main thật và trace exception.

| Chốt bị đột biến | Bước bắt được |
|---|---|
| Bỏ IGNORECASE | (1), mất token alias HOA |
| Nhận ảnh; bỏ luật nhãn; nhãn `.` bất kỳ; nhận hậu tố dính | (6), lần lượt ảnh, nhãn khac, `.md` sai đuôi, `+bak` được nhận sai |
| Span nhận khoảng trắng; bỏ chốt tên | (2), thông báo không còn đủ lỗi tên và đuôi |
| Bỏ giữ span riêng ML/CB/cả hai | (1) mất đối chứng tên đúng ở ML, hoặc (6) mất cảnh báo C1 đúng |
| Tách ô bỏ escape | (6), C1 tràn từ cột verdict sang cột id |
| Mục lục dùng basename | (6), link trỏ `con/x-verdict.md` được nhận nhầm cho x ở gốc |
| Bỏ alias; alias không cần duy nhất | (6), mất đối chứng verdict con hoặc nhận nhầm cảnh báo gốc |
| Tập danh tính chỉ ds_verdict | (6), mất alias dương của verdict con do đếm=0 |
| Quay đúng chính sách alias lượt 5 (chỉ chống trùng với ds_verdict) | (7), hàng `VERDICT.md/C9` thoả nhầm cho verdict con |
| Bỏ chốt đuôi; bỏ gọi chốt receipt riêng t26/t27 | (1), alias HOA được nhận |
| Bỏ gọi chốt tên verdict t27 | (3), đỏ sai chốt thay vì hướng dẫn đổi tên |
| Sidecar không phân biệt case stem | (5), nhận `c-verdict.receipt.yaml` cho `c-VERDICT.md` |
| Helper glob; bỏ is_file; riêng receipt/verdict consumer về glob | Ca listing, đúng biên file/đuôi HOA ở mỗi mutant |

[Driver và cặp thay thế chính xác](review_mutations.py), [trace/kết quả](review-evidence/mutation-results.json), [bốn mutant listing](review-evidence/listing-mutation-results.json). Những ca này có răng trong phạm vi đã phủ; chúng chưa phủ comment bên trong span như F1.

## Đã đo

Các lệnh Python dùng `PYTHONDONTWRITEBYTECODE=1`; `TMPDIR` nằm trong workspace ngoài `cay-kho/`; `GIT_OPTIONAL_LOCKS=0`. Suite chạy trên các bản sao riêng có `.git` riêng, giữ ref/config nguồn và ghim `core.abbrev=7`. [Runner/argv/rc](review_runner.py), [thư mục bằng chứng](review-evidence/).

| Lệnh / phạm vi | rc | Kết quả |
|---|---:|---|
| `python3 ops/lease_publish_test.py`, bản sao head | **1** | **267/269**, chạy 269, bỏ qua 0; **722,690 s** |
| Cùng lệnh, bản sao base `b29da0b` | **1** | **266/268**, chạy 268, bỏ qua 0; **723,933 s** |
| `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py`, bản sao head riêng | **0** | **60/60 thực chạy**, tổng 61, bỏ qua 1; **655,018 s**; cổng cây thật và các tự kiểm đạt |
| `python3 review_probes.py matrix`; `python3 review_probes.py real` | 0 / 0 | 96 ca cũ; 1.362 ô tên và 750 ô id không đổi |
| `python3 review_finding.py`; `python3 review_supplement.py collisions` | 0 / 0 | Phản chứng lượt 5 có v2 đầy đủ và các alias trùng đã bị chặn; đối chứng sửa hàng xanh |
| `python3 review_supplement.py real / grammar / unicode` (ba lượt) | 0 / 0 / 0 | So 1.631 vector; 138 ca ngữ pháp; Unicode, `.yml` và 2.048 biến thể đuôi |
| `python3 review_mutations.py` và lượt bổ sung alias cũ; `python3 review_listing_mutations.py` | 0 / 0 / 0 | Các control xanh; 21 + 4 mutant đỏ đúng chốt; không tính SyntaxError |
| `python3 review_finding_r6.py` | **0** | Tái hiện F1 với v2 đầy đủ; ba ô tên và id span-comment vẫn xanh sai |
| `python3 ops/lease_publish_test.py --chi-ca=t27_`, trên ba fixture F1 | **0 / 0 / 0** | Mỗi cây sai vẫn 3/3; input README được băm và không đổi trong lượt chạy |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head/base | 1 / 1 | Delta F = 0 |
| `python3 review_static.py` | 0 | Compile và SyntaxWarning delta so base; Ruff và diff check được ghi riêng |
| `git -C cay-kho diff --check b29da0b HEAD` | 0 | Không lỗi whitespace |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, bản sao head | 0 | Không phát hiện chép doctrine |
| `python3 review_finalize.py` | 0 | Kiểm marker, kết quả từng ca, băm module và snapshot nguồn |

Hai suite lease đầy đủ đều **failed**, không khai N/N đạt. Cùng hai ca đỏ có thông báo giống nhau: `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck` và `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`, đều vì thiếu ShellCheck. Phần phép đo công cụ này là **not_measured** do môi trường. **268 ca chung không đổi trạng thái**; thêm đúng ca tên biên nhận mới đạt. Đủ 269/268 cặp marker cấp ngoài, đúng thứ tự, không thiếu/trùng và không bỏ qua; các lượt A/B lồng được tách riêng. `t125` đạt ở cả hai. [So sánh đầy đủ](review-evidence/full-comparison.json), [head log](review-evidence/full-head.stdout), [base log](review-evidence/full-base.stdout).

Cong chạy đúng chế độ CI tại `.github/workflows/ci.yml`: `t47` **skipped** vì fixture INDEX chưa hoà giải không dựng được (`stage={'0'}`); không ghi thành 61/61. Cổng cây thật, tự kiểm phân hạng, giàn giáo và song song đều đạt. **490 mutant của cong: giao mảnh / not_measured trong lượt này**, không phải 490 đạt. [Lệnh và môi trường](review-evidence/full-cong.invocation.json), [rc/thời lượng](review-evidence/full-cong.result.json), [log](review-evidence/full-cong.stdout).

Ruff không xanh tuyệt đối: mỗi bên 7 F401 + 2 F541; delta code/message bằng 0. Compile trong `warnings.catch_warnings` không có SyntaxError; mỗi bên có đúng hai SyntaxWarning cũ (`invalid escape sequence '\s'`, `'\d'`), delta nội dung bằng 0, chỉ dịch dòng. [Lệnh và kết quả](review-evidence/static-results.json).

`review_finalize.py` rc=0 tự đối chiếu toàn bộ 564 CLI chọn ca có invocation/result được lưu với marker dương và số ca thực chạy; các mutant qua wrapper còn được kiểm marker/trace riêng trong driver. Ba bản sao suite sau chạy giữ nguyên byte module tương ứng: head và cong khớp head, base khớp `b29da0b`.

Snapshot trước/sau có **8.468 tệp tracked trùng mode/băm hoặc đích symlink**, HEAD/tree, diff/index và danh sách untracked/ignored không đổi; delta 0. Phạm vi snapshot này không băm toàn bộ `.git` và không chứng nhận OS cưỡng chế read-only hay lịch sử chưa từng ghi rồi hoàn nguyên. [Tổng hợp cuối](review-evidence/final-summary.json), [marker CLI](review-evidence/cli-marker-audit.json), [snapshot trước](review-evidence/source-before.json), [sau](review-evidence/source-after.json), [delta](review-evidence/source-delta.json).

Linux, Python 3.13.17, PyYAML 6.0.3, Ruff 0.16.9, actionlint 1.7.7, Pandoc 3.1.3; ShellCheck vắng. Windows thật và CI GitHub: **not_run/not_measured**. Kho được cấp báo `--is-shallow-repository=true`, trái mô tả đủ lịch sử; không gỡ marker shallow hay sửa lịch sử. Ba revision cần diff/review đều tra được; các phép v2 dương dùng Git fixture đầy đủ, không thay cho chứng nhận v2 toàn kho thật. Công cụ `environment_status` không có trong tập tool; không dùng mạng.

Reviewer: Codex, phiên API độc lập; provider `openai_codex`, execution surface `codex_service`, transport `machine`. Model/effort phục vụ thực tế không có runtime attestation trong bằng chứng này: `KHONG_DO_DUOC`. Theo `CLAUDE.md` §Quy trình sửa code bước 5, agent `tl_auditor` chỉ tiêu hoá log hồi quy read-only; phiên chính tự đọc mã, chạy phản chứng và quyết định finding. Không dùng context Executor.

Chỉ ghi script, fixture/bản sao và verdict ngoài `cay-kho/`; không push, không gọi API GitHub, không merge/deploy/LIVE. Verdict này không tự tạo approval/state hoặc quyền land.
