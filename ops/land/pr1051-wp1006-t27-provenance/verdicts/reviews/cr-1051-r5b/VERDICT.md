verdict: changes_requested
reviewed_sha: 000e0fa2e29f973b8521f5510838f344c9e76c99
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1051, lượt 5. Những phản chứng cụ thể của lượt 4 đã bị chặn thật, nhưng lớp “ô ghi tên/cột khác vẫn thoả cho danh tính trên đĩa” chưa đóng. Gộp các biểu hiện bên dưới thành **một finding P2**, giữ ID của lớp từ các lượt trước. Theo PROMPT, chưa đủ điều kiện approve.

Base: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`; head lượt 4: `3e034594c08ecd758a5d5fb23368d0930692a910`; reviewed tree: `308c98d5d91d3a15a0d1965aeb42665df8db0cca`. Diff toàn PR: 347 dòng thêm, 17 dòng bỏ; diff lượt này: 148 dòng thêm, 44 dòng bỏ. Cả hai chỉ thay `ops/lease_publish_test.py`.

## Finding F1 — P2 — `wp1006-case-insensitive-listing-case-sensitive-consumer`

**Tệp:dòng:** `ops/lease_publish_test.py:1719` (nhận link trước khi nhận span, cũng nhận phần `[...]` của ảnh); `:1730`–`:1733` (fallback trích tên từ cấu trúc chưa đọc, entity và thuộc tính HTML; thiếu biên của chính span/link đã nhận); `:1917` (chống basename trùng chỉ nhìn tập `*-verdict.md` ở gốc). Consumer tại `:1905`, `:1919`, `:1932`. Ca mới tại `:2022` chưa khoá các đường dưới đây.

**Tác động.** CLI t27 có thể xác nhận một biên nhận/verdict đã xuất hiện ở đúng cột hoặc một caveat đã được nâng lên đúng hàng, trong khi ô người đọc thấy trỏ tệp khác, chỉ chứa một tên dài hơn, chứa ảnh/cú pháp mã, hoặc hàng cảnh báo thuộc verdict khác. Đây là lỗi của kiểm mục lục/cảnh báo; không diễn giải thành bypass lược đồ v2.

**Phản chứng có receipt v2 đầy đủ.** Chạy `PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=ignore python3 review_finding.py`: driver rc=0. Mỗi fixture nằm ngoài `cay-kho/`, có Git thật, verdict đã commit, băm đúng, URL blob ghim commit tồn tại trong fixture, receipt đủ trường. Identity/URL của fixture là dữ liệu thử. Mã suite chép nguyên byte từ head; validator chạy nguyên mã head với `--root`, không mock Git hoặc nới schema. Đối chứng tên đúng xanh. Các ô biên nhận sau đều cho **helper xanh, t27 rc=0 (1/1), t26 rc=0, v2 rc=0 (1/1 receipt đạt)**:

| Ô thay thế | Vì sao không được thoả cho `x-verdict.receipt.yaml` |
|---|---|
| ``[`x-verdict.receipt.yaml`][1]`` với định nghĩa `[1]: other.yaml` | Đích thật là `other.yaml`; bộ đọc không hiểu reference link rồi lấy tên từ nhãn. |
| `<a href="other.yaml" title="x-verdict.receipt.yaml">other.yaml</a>` | Cả nhãn lẫn đích đều là `other.yaml`; tên cần kiểm chỉ nằm trong thuộc tính `title`. |
| `![.receipt.yaml](x-verdict.receipt.yaml)` | Cú pháp ảnh bị nhận làm link; ô hiển thị ảnh/alt `.receipt.yaml`, không phải hàng nêu tên receipt. |
| `` `[.receipt.yaml](x-verdict.receipt.yaml)` `` | Cả span là một chuỗi cú pháp khác; regex link chạy trước và cộng tên vào `ra`, không thể thu hồi ở bước đọc span. |
| `two&#46;x-verdict.receipt.yaml` | Entity hiển thị thành dấu chấm: tên là `two.x-verdict.receipt.yaml`; parser lấy hậu tố sau dấu `;` trong nguồn. |
| ``other`x-verdict.receipt.yaml` `` | Span đã được cộng vào `ra` dù dính tiền tố; chuỗi hiển thị liền thành tên dài hơn. NUL chỉ chặn phần chữ trần còn lại, không kiểm biên của tên đã cộng. |

Đối chiếu ngữ nghĩa với [GFM §6.6: đích reference link nằm ở định nghĩa](https://github.github.com/gfm/#links), [§6.10: HTML và thuộc tính](https://github.github.com/gfm/#raw-html), [§6.7: ảnh và alt](https://github.github.com/gfm/#images), [§6.3: ưu tiên code span](https://github.github.com/gfm/#code-spans), [§6.2: entity ngoài span](https://github.github.com/gfm/#entity-and-numeric-character-references). Không dựa vào việc entity tạo ra delimiter Markdown: ở ca này entity chỉ đổi ký tự trong tên hiển thị.

Ma trận qua bảng thật và CLI xác nhận HTML anchor/attribute, reference link, ảnh, link trong span và tiền tố entity `&#46;`/`&#43;` đều xanh sai ở **cả ba ô tên**: biên nhận, verdict trong Mục lục, verdict trong bảng cảnh báo. `<code>two x-… </code>` và span dính hậu tố `+backup` cũng được nhận. Không lấy những ca xanh nhưng chưa chứng minh sai danh tính làm finding. [Driver](review_probes.py), [96 ca và rc](review-evidence/table-probes.json), [driver v2 đầy đủ](review_finding.py), [kết quả v2 đầy đủ](review-evidence/finding-results.json), [README HTML](review-evidence/fixtures/valid-html/ops/reviews/README.md), [README reference](review-evidence/fixtures/valid-reference/ops/reviews/README.md), [README entity](review-evidence/fixtures/valid-entity/ops/reviews/README.md).

**Basename trùng: chốt mới vẫn hở với verdict gốc có receipt nhưng không mang hậu tố `-verdict.md`.** Fixture có ba verdict `x-verdict.md`, `VERDICT.md`, `ho-so/VERDICT.md`; ba receipt hợp lệ tương ứng, hai receipt sau cùng có caveat `C9`. Mục lục đủ ba đường dẫn. Bảng cảnh báo chỉ có hàng `x-verdict.md/C1` và hàng gốc sau:

```markdown
| tệp verdict | id |
|---|---|
| `x-verdict.md` | `C1` |
| `VERDICT.md` | `C9` |
```

Không có cảnh báo cho `ho-so/VERDICT.md`, nhưng **helper xanh, t27 rc=0, t26 rc=0, v2 rc=0 (3/3)**. `ds_verdict` chỉ liệt kê `*-verdict.md`, nên không chứa verdict gốc `VERDICT.md`; điều kiện dòng 1917 nhận nhầm rằng không có verdict gốc cùng basename. Đổi thành cặp `report.md`/`ho-so/report.md` cũng xanh sai. Đối chứng `y-verdict.md`/`ho-so/y-verdict.md` **đỏ đúng C9**; thêm hàng link ghi đích `ho-so/y-verdict.md` làm xanh. Vì vậy mutant và ca mới chỉ khoá được trường hợp tên có hậu tố đã chọn, chưa khoá hợp đồng chung của vòng duyệt receipt.

Đã kiểm chiều ngược: hàng cảnh báo ghi rõ link đích thư mục con không thoả cho caveat của verdict gốc, cả ba kiểu tên đều t27 rc=1. Hai verdict trong `first/y-verdict.md` và `second/y-verdict.md`, cùng caveat C9, cũng bị một hàng basename `y-verdict.md/C9` thoả cho cả hai (t26/t27/v2 đều rc=0). Đây là cùng lỗi dùng alias mơ hồ. [Kết quả đầy đủ](review-evidence/finding-results.json), [chiều ngược và hai thư mục con](review-evidence/collision-extra.json), [driver bổ sung](review_supplement.py). Driver bổ sung rc=0; đối chứng sửa hàng đều đã chạy.

**Đề xuất vá ở đâu, thế nào.** Trong `_ten_tep`, dùng một lượt đọc giữ phạm vi cấu trúc: span đã từ chối không được sinh link, thuộc tính HTML không được rơi vào nhánh tên trần, ảnh không được coi như link. Với reference link/entity/HTML chưa hỗ trợ, có thể từ chối nguyên cấu trúc đó theo chính sách nhận hẹp hiện tại; không lấy token ở bên trong để làm bằng chứng. Áp biên cho cả tên từ span/link, không chỉ cho chữ trần. Đây là phương án rẻ hơn tích hợp một parser GFM hoàn chỉnh; parser hoàn chỉnh mua thêm hỗ trợ cú pháp và quy tắc ưu tiên, nhưng vẫn cần chính sách danh tính của mục lục.

Tại `_kiem_muc_luc`, lập tập danh tính đường dẫn từ **mọi receipt**, cộng verdict được phát hiện trên đĩa; chỉ cấp alias basename khi nó xác định duy nhất một đường dẫn. Không chỉ tra tập `*-verdict.md`, cũng không chỉ kiểm xung đột với gốc. Các alias receipt cùng trỏ một verdict phải gộp theo đường dẫn trước khi xét tính duy nhất.

**Ca khoá.** Đưa các fixture trên qua `_kiem_muc_luc` và CLI t27, giữ t26/v2 xanh để cô lập chốt mục lục. Mỗi ô sai phải đỏ đúng cột/caveat; tên đúng, link inline đúng, nhiều tên tách rõ và README thật tiếp tục xanh. Khoá ba dạng basename `y-verdict.md`, `VERDICT.md`, `report.md`, cả chiều gốc/con và hai thư mục con. Sau khi vá, đột biến cho link chạy trong span, cho ảnh/reference/HTML/entity rơi xuống nhánh trần, bỏ biên span/link hoặc thu tập xung đột về `ds_verdict` phải bị các ca này giết. Không lấy bộ 27 mutant hiện tại thay cho các ca còn thiếu này.

**Rủi ro của cách vá.** Chặn toàn bộ ô có markup có thể từ chối cả tên hợp lệ đi kèm một cấu trúc không hỗ trợ; decoder entity áp sai phạm vi có thể tạo span/link giả. Giữ nội dung code span nguyên văn; giữ case/Unicode và danh tính đường dẫn; không normalize toàn tên hoặc dùng substring/basename để chữa. Siết alias cần tiếp tục nhận 22 verdict trong thư mục con hiện tại khi basename còn duy nhất.

## Đối chiếu lượt 4 và README thật

Đã chạy lại script phản chứng được cấp, giữ nguyên năm ô sai; chỉ thay bộ nối đường dẫn/fixture, đổi prefix log để tách bằng chứng và cập nhật assertion cuối thành kỳ vọng **đã vá**. `python3 review_r4_repeat.py` rc=0: control helper xanh, t27/v2 rc=0; năm ca double-span ở ba ô tên và hai hàng `\|` đều helper đỏ, t27 rc=1, v2 vẫn rc=0. [Driver](review_r4_repeat.py), [bộ nối](review_r4_support.py), [kết quả](review-evidence/r4-repeat-results.json), [log](review-evidence/r4-repeat-driver.stdout).

Ma trận độc lập thêm span đơn/hai/ba nháy, `.bak`, `/child`, `+backup`, `@backup`, nhãn/đích inline link khác nhau: tất cả đều đỏ đúng chốt ở ba ô tên. Nhãn link dùng span nhiều nháy nhưng ghi tên khác, đích có `#anchor`, `?q`, ngoặc nhọn và các dạng backtick thoát đã đo đều bị từ chối; không tính sự từ chối hẹp đó thành finding. Như vậy các biểu hiện cụ thể của P2 lượt 4 **đã vá thật**; ở cấp lớp, F1 vẫn còn các đường nêu trên.

`review_probes.py real` và `review_supplement.py` so từng ô và từng kết luận trên chính README head, với parser/consumer tại `3e03459` và head:

| Phép đo | Kết quả |
|---|---|
| Bảng cảnh báo | 750 hàng, 750 ô tên và 750 ô id; không đổi token/id. |
| Dưới Mục lục | 321 hàng parser trả, 306 hàng có cột tên; 612 ô tên. |
| Tổng 1.362 ô tên | 1.034 ô cùng tập; 328 ô là tập con thực sự; **0 ô thêm token**. Phần bị bỏ là nhãn `.receipt.yaml` và basename nhãn link của verdict con. |
| Ô id | **0 delta** sau đúng phép chuẩn hoá ở từng consumer. |
| Kết luận theo hàng của từng yêu cầu receipt/verdict/caveat | **1.347 vector hàng** đã so, **0 delta**; cả hai `_kiem_muc_luc` xanh. `_bang` mặc định cũng trả hai bảng bằng nhau. |
| Verdict thư mục con | 22 đường dẫn; tất cả dùng link đường dẫn trong Mục lục và basename trong cảnh báo. Đếm trực tiếp có **50 hàng cảnh báo** liên quan (16 tên có 2 hàng, 6 tên có 3 hàng), không phải chỉ 22 hàng. Không có hàng cảnh báo ghi đường dẫn đầy đủ. |

Lời khai “cùng tập hoặc tập con” được xác nhận trên README thật; không có hàng thật đổi kết luận. Điều đó không phủ định các phản chứng F1 ngoài tập hàng hiện tại. [Mỗi ô](review-evidence/real-cells.json), [tổng hợp](review-evidence/real-summary.json), [mỗi kết luận theo hàng](review-evidence/real-conclusions.json). Duyệt 2.048 biến thể hoa/thường của suffix: chỉ `alias.receipt.yaml` được chốt tên nhận, giữ việc đóng đường alias HOA của các lượt trước. [Kết quả suffix](review-evidence/suffix-results.json).

## Răng của các ca khoá

`python3 review_mutations.py` rc=0: control **1/1, rc=0**; **23 mutant riêng** đều **0/1, rc=1**. Mỗi bản nằm trong thư mục riêng ngoài nguồn, chạy `runpy` với `__name__='__main__'`, selector và `main` thật; trace ghi dòng exception, tiến độ và số lần gọi helper. Không tính exception âm được test cố ý bắt làm thất bại của control. [Driver](review_mutations.py), [kết quả và trace](review-evidence/mutation-results.json).

| Chốt bị đột biến | Chỗ ca mới bắt được |
|---|---|
| Tách ô bỏ nhận diện `\|` | (6), hàng receipt bị đẩy sang sai cột. |
| Bỏ luật nhãn link khác đích | (6), nhãn `khac.receipt.yaml` trỏ receipt x được nhận. |
| Quay về scanner span một nháy | (6), span hai nháy chứa nháy đơn bị nhận sai. |
| NUL thành khoảng trắng | (6), receipt dính sau span `two`. |
| Biên trước rỗng hoặc nới thêm `+`/`@` (2 mutant) | (2), cắt hậu tố từ `plus+name…`. |
| Biên sau rỗng hoặc nới thêm `+`/`@` (2 mutant) | (6), `.bak` hoặc `+bak`. |
| Mục lục dùng basename | (6), đối chứng dương link đường dẫn thư mục con mất danh tính. |
| Cảnh báo không nhận basename | (6), đối chứng dương cảnh báo của verdict con bị mất. |
| Bỏ chốt trùng basename với verdict gốc | (6), ca `y-verdict.md` nhận nhầm hàng gốc. |
| Bỏ giữ span riêng ML, riêng CB, cả hai (3 mutant) | (6), đối chứng hoặc ô sai tại đúng bảng bị ảnh hưởng. |
| Bỏ chốt đuôi; bỏ gọi chốt receipt t27; bỏ gọi chốt t26 (3 mutant) | (1), alias HOA được nhận. |
| Bỏ chốt tên | (2), thông báo không còn đồng thời nêu lỗi tên có khoảng trắng. |
| Bỏ chốt tên verdict t27 | (3), đỏ sai chốt thay vì hướng dẫn đổi tên. |
| So stem sidecar không phân biệt hoa/thường | (5), sidecar khác stem được nhận. |
| Bỏ IGNORECASE ở chữ trần | (2), assert token đuôi HOA thất bại. |
| Bỏ bóc backtick của id | (6), đối chứng dương C1 đỏ. |
| Bỏ yêu cầu span trọn một tên | (2), assert nguyên span thất bại. |

`python3 review_listing_mutations.py` rc=0 kiểm thêm ca `t27_phan_chung_verdict_duoi_HOA_thieu_muc_luc_phai_DO_tren_moi_nen`: control 1/1; **4 mutant** quay helper về glob, bỏ `is_file`, quay riêng consumer receipt về glob, quay riêng consumer verdict về glob đều 0/1, rc=1, đúng thông báo. [Driver](review_listing_mutations.py), [kết quả](review-evidence/listing-mutation-results.json). Tổng **27/27 mutant bị giết**; đây là bằng chứng các chốt được phủ có răng, không phải bằng chứng F1 đã đóng.

## Đã đo

Các lệnh ghi log dùng `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`; Ruff không ghi cache. Suite head/base và các lượt cong_cu chạy trong các bản sao riêng ngoài `cay-kho/`, có `.git` riêng, `core.abbrev=7`; không thay đổi mã nguồn head/base của các suite để làm xanh. [Runner và argv/rc từng subprocess](review_runner.py), [thư mục bằng chứng](review-evidence/).

| Lệnh / phạm vi | rc | Kết quả |
|---|---:|---|
| `python3 ops/lease_publish_test.py`, bản sao head | **1** | **267/269**, chạy 269, bỏ qua 0; **713,488 s**. |
| Cùng lệnh, bản sao base `b29da0b` | **1** | **266/268**, chạy 268, bỏ qua 0; **706,451 s**. |
| `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py`, bản sao head riêng, đúng chế độ CI | **0** | **60/60** ca thực chạy, tổng 61, bỏ qua 1; **444,928 s**. Cổng cây thật và tự kiểm đạt. |
| `python3 ops/cong_cu_test.py`, lượt mặc định ban đầu | cancelled; wrapper **130** | Nền 60/60, tổng 61, bỏ qua 1; đã vào lô 490 mutant nhưng chủ động ngắt để chạy chế độ CI. Không có kết luận cho 490 mutant. |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head/base | 1 / 1 | Mỗi bên 7 F401 + 2 F541; delta code/message chuẩn hoá **0**. |
| `python3 review_r4_repeat.py` | 0 | Năm phản chứng cũ đỏ; control/v2 xanh. |
| `python3 review_probes.py matrix` và `python3 review_supplement.py` | 0 / 0 | Tổng 96 ca bảng; helper/CLI t27 đồng ý, t26 xanh; đã kiểm marker 1/1 hoặc 0/1, không chỉ rc. Có các đối chứng dương/âm F1 với v2 thật. |
| `python3 review_probes.py real` và phép so kết luận trong supplement | 0 / 0 | 1.362 ô tên, 750 ô id, 1.347 vector kết luận theo hàng; không có token mới hoặc kết luận đổi. |
| `python3 review_finding.py` | 0 | Receipt v2 đủ trường/băm/anchor; các ô F1 và hai ca gốc/con vẫn t27 xanh sai. |
| `python3 review_mutations.py`; `python3 review_listing_mutations.py` | 0 / 0 | Hai control xanh; 23 + 4 mutant đều đỏ đúng chốt. |
| `git -C cay-kho diff --check b29da0b HEAD` | 0 | Không lỗi whitespace. |
| `git -C cay-kho status --porcelain=v1 --untracked-files=all` | 0 | Output rỗng; head/tree đúng mỏ neo. |
| `python3 review_runner.py snapshot-final` | 0 | 8.505 entry, delta 0 so snapshot sau preflight. |

Hai suite lease đầy đủ đều **failed**, không khai pass toàn bộ. Chúng đỏ đúng cùng hai ca `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck` và `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`, đều vì thiếu ShellCheck; phần phép đo công cụ này là **not_measured**. **268 ca chung không đổi trạng thái**, thêm đúng ca tên biên nhận mới đạt. Đã kiểm đủ cặp marker vào/ra cấp ngoài: head 269/269, base 268/268, không trùng/thiếu ca, không bỏ qua; t125 đạt ở cả hai (420,446 s / 416,699 s), tách riêng 538/536 marker A/B lồng.

`cong_cu_test.py` được chạy hoàn tất theo đúng chế độ của `.github/workflows/ci.yml:167`: chạy mọi ca, cổng trên cây thật và các tự kiểm; giao bán kính 490 mutant cho các job mảnh/gom. Ca `t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet` **skipped** vì fixture INDEX chưa hoà giải không dựng được (`stage={'0'}`); không ghi thành 61/61. Cổng cây thật, tự kiểm phân hạng, giàn giáo và song song đều đạt. Hai helper mà cong_cu gọi trực tiếp qua `lpt` là `_goi_actionlint_gia` và `_bam_tep`, không đổi trong diff.

**490 mutant của cong_cu: delegated/not_measured**, không phải 490 đạt. Lượt mặc định đã khởi chạy được chủ động ngắt qua session, wrapper rc=130; không có rc/kết luận sản phẩm cho lượt chưa hoàn tất đó. Phép đo hoàn tất là chế độ CI ở hàng trên. [Lệnh và môi trường chọn chế độ](review-evidence/cong-gate.invocation.json), [rc/thời lượng](review-evidence/cong-gate.result.json), [stdout gate](review-evidence/cong-gate.stdout), [trạng thái lượt đã huỷ](review-evidence/full-cong.cancelled.json).

Mã `lease_publish_test.py` sau chạy vẫn khớp nguyên byte revision tương ứng trong cả bốn bản sao. [Audit log và delta](review-evidence/log-audit.json), [script chỉ tiêu hoá log](review_log_audit.py), [head stdout](review-evidence/full-head.stdout), [base stdout](review-evidence/full-base.stdout), [cong_cu stdout lượt đã huỷ](review-evidence/full-cong.stdout), [Ruff](review-evidence/ruff-comparison.json), [kiểm marker CLI](review-evidence/cli-marker-audit.json), [băm module](review-evidence/suite-module-integrity.json).

## Tính toàn vẹn và giới hạn

Snapshot nguồn sau preflight và sau các phép đo gồm 8.505 entry tệp/symlink, kể cả `.git`: so tên, loại, mode tệp, băm nội dung và đích symlink cho **delta 0**. Đây là không có thay đổi quan sát được giữa hai snapshot, không phải chứng nhận OS cưỡng chế read-only hoặc chưa từng ghi rồi hoàn nguyên. [Trước](review-evidence/source-before.json), [sau](review-evidence/source-after.json), [delta](review-evidence/source-delta.json).

Linux, Python 3.13.17, PyYAML 6.0.3, Ruff 0.16.9, actionlint 1.7.7; ShellCheck vắng. Windows thật và CI GitHub: **not_run/not_measured**. `environment_status` không có trong tập tool. Kho được cấp báo `git rev-parse --is-shallow-repository` = `true`, trái mô tả “đủ lịch sử”; không xoá marker shallow hoặc sửa lịch sử. Các revision cần diff vẫn tra được; phép đo v2 dương của finding dùng các kho fixture đầy đủ riêng và không thay cho xác nhận v2 toàn kho thật.

Reviewer: Codex, phiên API độc lập với Executor; provider `openai_codex`, execution surface `codex_service`, transport `machine`, theo ánh xạ của kho. Model ID/effort thực phục vụ không có runtime attestation trong bằng chứng này: `KHONG_DO_DUOC`. Theo `CLAUDE.md` §Quy trình sửa code bước 5, một sub-agent chỉ tiêu hoá log hồi quy dài và so kết quả; phiên chính tự đọc mã, dựng/chạy phản chứng và kết luận finding. Không dùng context Executor.

Chỉ ghi verdict, script đo và bản sao dưới workspace ngoài `cay-kho/`; không push, không gọi API ghi GitHub, không merge/deploy/LIVE. Verdict này không tự cấp quyền land hoặc tạo trạng thái approval có thẩm quyền.
