verdict: changes_requested
reviewed_sha: c75df5671d1282adbdf748b1e068b44e1b386326
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1051, lượt 8. Các phản chứng nguyên bản lượt 5–7 đã bị chặn, nhưng **P2 lượt 7 chưa đóng ở cấp lớp**: t27 vẫn xác nhận bảng/hàng không tồn tại như vậy trong GFM. Chốt cấm comment mới cũng có đường vòng. Một lớp lỗi, một finding P2.

Base: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`; reviewed tree: `3f2b032a0cbdd3a72455aa07126633ab1cfa64e7`. Diff toàn PR chỉ `ops/lease_publish_test.py`, 471 thêm / 25 bỏ; lượt 7 → 8 là 49 thêm / 16 bỏ. Provider `openai_codex`, execution surface `codex_service`, transport `machine`; model thực phục vụ không đo được từ công cụ của phiên. Chỉ thị hiện tại cấp quyền review; các đặc tả/verdict cũ là nguồn yêu cầu và lịch sử.

## Finding F1 — P2 — `wp1006-case-insensitive-listing-case-sensitive-consumer`

**Tệp:dòng:** `ops/lease_publish_test.py:1601` quét mục khác trạng thái với bộ đọc bảng; `:1607` thay comment xuyên dòng; `:1615` tách dòng rộng hơn GFM; `:1618` nhận rào mã sai thụt lề; `:1613` nhận hàng phân cách không có gạch; `:1633` không xét khối HTML/đoạn văn trước bảng. Consumer tại `:1873` trở đi tin các hàng này.

**Mô tả và tác động.** CI có thể báo rằng verdict/receipt/caveat đã có đúng cột và cùng hàng, dù người đọc chỉ thấy khối mã, văn bản thường, hoặc hai hàng không có đúng cặp tên/id. Đây là lỗi chứng nhận mục lục/cảnh báo; các receipt trong phản chứng vẫn qua validator v2 thật.

**Đường vòng ngay chốt mới.** Thêm một tiêu đề giả trong khối mã trước bảng cảnh báo:

````markdown
## Cảnh báo đang có hiệu lực

```
## Đây chỉ là ví dụ
```

| tệp verdict | id |
|---|---|
| `x-verdict.md` <!--
| --> | `C1` |

## Mục lục

| tệp verdict | biên nhận |
|---|---|
| `x-verdict.md` | `x-verdict.receipt.yaml` |
````

Lượt quét comment ở `:1601` không nhớ rào mã, nên tiêu đề giả làm `lay=False` và comment không bị từ chối. Lượt đọc bảng nhớ rào mã, bỏ tiêu đề giả và vẫn ở mục cảnh báo. `re.sub(..., flags=re.S)` co hai hàng cuối thành một hàng, `_ten_tep` nhận tên trước khoảng trắng và coi phần tiếp theo là chú thích. Kết quả parser là tên x cùng id C1; HTML GFM thực đo là hàng x có id rỗng, hàng `-->` có C1. Cùng đường vòng ở Mục lục ghép verdict với receipt từ hai hàng khác nhau.

**Tái hiện đã chạy:** `PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=ignore python3 review_prepass.py` — rc=0 của driver xác nhận hai phản chứng. Mỗi fixture: `_kiem_muc_luc` xanh sai, CLI `--chi-ca=t27_canh_` **rc=0, 1/1**, CLI `--chi-ca=t27_` **rc=0, 3/3**, t26/v2 **0/0**. Bỏ tiêu đề giả thì comment bị chặn; sửa lại thành một hàng thật thì xanh với cùng verdict/receipt.

Bằng chứng: [driver](review_prepass.py), [kết quả và các hàng HTML](run/evidence/prepass-results.json), [README cảnh báo](run/evidence/fixtures/prepass-cb/ops/reviews/README.md), [HTML cảnh báo](run/evidence/prepass-cb.html), [CLI 3/3](run/evidence/prepass-cb-all-t27.stdout).

**Các cửa khác của cùng lớp đã xác nhận:**

| Thay đổi riêng trong mục CB hoặc ML | Kết quả render GFM / nguyên nhân |
|---|---|
| Bọc bảng trong `<pre>…</pre>` hoặc `<div>…</div>`, không dòng trống ở trong | Không có bảng Markdown; `_bang` không theo dõi khối HTML |
| Đổi hàng gạch thành `\|:\|:\|` | Đoạn văn, không có bảng; `la_gach` chỉ kiểm tập ký tự, không đòi gạch |
| Mở rào bằng ba backtick, thêm dòng bốn dấu cách rồi ba backtick trước bảng | Bảng vẫn nằm trong khối mã; `^\s*` lại coi dòng thụt 4 dấu cách/tab là rào đóng |
| Đổi LF giữa các dòng bảng thành U+000B, U+000C, U+0085, U+2028 hoặc U+2029 | Không có bảng; Python `splitlines()` tạo các dòng mà GFM không có |
| Đặt prose, `- prose` hoặc `> prose` ngay trước tiêu đề bảng, không ngắt đoạn | Không có bảng trong render; `_bang` bỏ dòng ngữ cảnh rồi công nhận bảng phía sau |

`python3 review_confirm.py` rc=0: **26 fixture xanh sai**, phủ cả CB/ML, đều qua helper, CLI t27 1/1, **toàn selector t27 3/3**, t26 và v2. README không bị test thay đổi. Mỗi fixture có đối chứng sửa đúng xanh; module nguyên byte head, Git riêng, receipt đủ trường v2 và reviewed commit tồn tại thật. URL/identity là dữ liệu thử. Ở các ca rào mã CB, có thêm dòng rào thụt lề sau rào đóng thật để trạng thái parser trở lại trước ML; fixture nguyên văn được lưu. Cách bọc đơn giản làm cả ML bị nuốt và đỏ an toàn không được tính là finding.

[Driver xác nhận](review_confirm.py), [26 kết quả và historical controls](run/evidence/confirmed-findings.json), [fixture hàng chỉ có dấu hai chấm](run/evidence/fixtures/confirm-ml-colon-separator/ops/reviews/README.md), [HTML tương ứng](run/evidence/confirm-ml-colon-separator.html), [fixture rào mã](run/evidence/fixtures/confirm-ml-fence-four-space/ops/reviews/README.md), [fixture U+2028](run/evidence/fixtures/confirm-ml-unicode-line-u2028/ops/reviews/README.md).

Đối chiếu quy tắc với [GFM về dòng](https://github.github.com/gfm/#characters-and-lines), [rào mã](https://github.github.com/gfm/#fenced-code-blocks), [HTML block](https://github.github.com/gfm/#html-blocks) và [delimiter bảng](https://github.github.com/gfm/#tables-extension-). Tài liệu GitHub cũng yêu cầu [ngắt đoạn trước bảng](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables). Render địa phương dùng Pandoc 3.1.3 `--from=gfm --to=html`; không khai đã đăng fixture hoặc đo UI trực tiếp trên GitHub. Historical controls cho thấy những cửa cấu trúc này đã tồn tại trước lượt 8; không quy mọi biểu hiện thành hồi quy vừa sinh trong commit này.

**Đề xuất.** Dùng cùng một phép phân định block/mục cho kiểm comment và đọc bảng; tiêu đề trong khối mã/HTML không được đổi mục. Không dùng phép thay comment làm mất ranh giới dòng. Với lựa chọn nhận hẹp, từ chối cấu trúc không chắc, nhưng phải xét ngữ cảnh từ trước tiêu đề: raw HTML, rào mã, đoạn văn/danh sách/blockquote và dòng phân cách. Chỉ coi CR/LF là biên dòng GFM, đòi delimiter có gạch và ràng thụt lề rào mã. Thêm các phản chứng trên qua consumer/CLI cùng đối chứng dương; giữ chốt tên/đuôi/sidecar/alias và đối chiếu README thật. Không chỉ thêm mẫu vào `_ten_tep`: các lỗi xảy ra trước khi nó nhận ô.

## Đối chiếu các lượt trước và ngữ pháp ô

Các phản chứng **nguyên bản** đã đóng thật:

| Nhóm | Kết quả độc lập |
|---|---|
| Lượt 5 | 96 ca: control xanh, 95 ca sai đỏ; ba ô tên, link tham chiếu, HTML, ảnh, link trong span, entity, tiền/hậu tố và escaped pipe; helper/CLI đồng ý, t26 xanh |
| Lượt 6 | Ba span tên có comment và span id comment đều đỏ đúng chốt `comment HTML`; t26/v2 vẫn xanh |
| Lượt 7 | Comment cắt ngang hàng, bảng ML/CB thụt 4 dấu cách đều đỏ; ba nhãn `_x_` trần đỏ, bọc nháy lại xanh |
| Alias | Ba cặp gốc/con `y-verdict.md`, `VERDICT.md`, `report.md`, chiều ngược và hai thư mục con cùng basename đều đỏ đúng caveat; ghi đường dẫn riêng sửa được; hai receipt cùng một đường dẫn vẫn giữ alias dương |

[96 ca](run/evidence/table-probes.json), [v2 và va chạm basename](run/evidence/finding-results.json), [alias bổ sung](run/evidence/collision-extra.json), [20 probe lượt 6–7](run/evidence/r7-extra-results.json), [nhãn emphasis](run/evidence/label-emphasis-results.json). Chốt mới cố ý từ chối cả comment sau khoảng trắng trong mục; đó là đỏ an toàn.

`review_supplement.py grammar` và `review_grammar_extra.py`: **138 + 54 = 192 ca**, 42 xanh / 150 đỏ đúng kỳ vọng. Đã thử ghép mục đúng/sai, mục sau dấu phẩy, chú thích chứa code/link/ảnh/HTML/entity, nhãn literal có ký tự lạ, zero-width/bidi/escape, đích có `..`, `./`, `//`. Bổ sung dùng nhãn bọc nháy để không chỉ bị loại bởi chốt nhãn trần. Chưa tìm thấy xanh sai mới trong `_ten_tep` trên ô nguyên bản; F1 nằm ở cách xác định bảng/hàng trước scanner. Không báo các trường hợp từ chối hẹp là finding. [138 ca](run/evidence/grammar-results.json), [54 ca](run/evidence/grammar-extra-results.json).

Unicode/`.yml`: fixture v2 đầy đủ xanh; bỏ `é-verdict.md` đỏ đúng tên, đổi cảnh báo `report.yml` thành `report.yaml` đỏ CY. Trong **2.048** biến thể đuôi receipt, chỉ `alias.receipt.yaml` được chốt tên nhận. [Kết quả](run/evidence/unicode-yml-suffix.json).

74 probe cấu trúc và 10 probe phạm vi đã thử thêm tab, rào thụt lề, blockquote, danh sách, raw HTML, heading giả/trùng, bảng thứ hai và hàng sau dòng trống. Các hàng thụt lề/tiền tố vô hình bị từ chối; hàng tách sau dòng trống không có header bị từ chối; bảng thứ hai thật và heading trùng có bảng thật có thể được nhận. Chỉ các trường hợp đã xác nhận xanh sai được đưa vào F1. [Cấu trúc](run/evidence/structure-results.json), [phạm vi](run/evidence/scope-results.json).

## README thật

So với consumer tại `000e0fa2e29f973b8521f5510838f344c9e76c99`, dùng chính README ở head:

| Phép đo | Kết quả |
|---|---|
| Ba cột tên | **1.362/1.362 cùng tập**; 0 thêm token, 0 tập con thực sự |
| Hàng parser | CB 750; ML 321, trong đó 306 có các cột tên |
| Kết luận theo hàng | **1.631 vector, delta 0**: 284 verdict đĩa + 612 receipt/verdict + 735 caveat |
| Alias basename | **0 tập alias đổi**, 22 đường dẫn con giữ kết luận, 50 hàng cảnh báo dùng basename |
| Toàn checker / `_bang` mặc định | Cả hai checker xanh; bảng mặc định bằng nhau |
| Hình thức nguồn | Đúng **1.081** dòng bảng cột 0 trong hai mục, 0 comment và 0 dòng bảng thụt lề |

[Từng ô](run/evidence/real-r6-cells.json), [từng vector](run/evidence/real-r6-vectors.json), [tổng hợp](run/evidence/real-r6-summary.json), [hình thức README](run/evidence/real-geometry.json). Tên artifact `r6` kế thừa driver tham chiếu; module thực chạy là head lượt 8.

## Răng của ca mới

`review_mutations.py`: control **0, 1/1**; **25/25 mutant riêng 1, 0/1**. `review_listing_mutations.py`: control **0, 1/1**; **4/4 mutant riêng 1, 0/1**. Tất cả compile được trước khi chạy; lỗi là AssertionError tại chốt liên quan, không tính SyntaxError hay lỗi giàn giáo là giết.

| Đột biến | Bước bắt được trong ca tên mới |
|---|---|
| Bỏ IGNORECASE | (1), mất token alias HOA |
| Nhận ảnh; bỏ luật nhãn; nhãn `.` bất kỳ; nhận ký tự dính sau mục | (6), nhận sai tên/đích |
| Span nhận khoảng trắng; bỏ chốt tên | (2), không còn báo đủ lỗi tên/đuôi |
| Bỏ giữ span ML / CB / cả hai | (1) / (6) / (1), mất đối chứng dương |
| Tách ô bỏ escape; ML dùng basename | (6), sai cột / sai danh tính |
| Bỏ alias; alias không cần duy nhất; danh tính chỉ từ `ds_verdict` | (6), sai chiều âm hoặc dương |
| Quay alias chỉ chống va chạm với `ds_verdict` | (7), một basename thoả nhầm nhiều verdict |
| Bỏ chốt đuôi; bỏ gọi chốt receipt riêng t26/t27 | (1), nhận alias HOA |
| Bỏ gọi chốt verdict t27; sidecar gộp case stem | (3) / (5), sai chốt tên / sai sidecar |
| Bỏ cấm comment; bỏ cấm thụt lề; bỏ kiểm số ô delimiter; nhận lại nhãn trần | (6), đúng chốt mới tương ứng |
| Helper về glob; bỏ `is_file`; riêng receipt/verdict t27 về glob | Ca listing, đúng biên đuôi HOA/file tương ứng |

[Cặp thay thế và runner](review_mutations.py), [trace/rc](run/evidence/mutation-results.json), [25 bước kiểm lại độc lập](run/evidence/mutation-step-audit.json), [listing](run/evidence/listing-mutation-results.json). Các ca có răng ở các chốt đã phủ; **28 fixture F1 vẫn t27 3/3** chứng minh còn thiếu độ phủ ngữ cảnh.

## Đã đo

Python dùng `PYTHONDONTWRITEBYTECODE=1`; `TMPDIR` nằm ngoài `cay-kho/`; `GIT_OPTIONAL_LOCKS=0`. Hai suite đầy đủ và cong chạy trong ba bản sao độc lập ngoài kho, `.git`/refs riêng, `core.abbrev=7` chỉ đặt trong bản sao. [Runner](review_runner.py), [dựng bản sao](review_full.py), [rc các driver](run/evidence/driver-exits.json).

| Lệnh / phạm vi | rc | Kết quả |
|---|---:|---|
| `python3 ops/lease_publish_test.py`, head copy | 1 | **267/269**, chạy 269, bỏ qua 0; 987.805 s |
| Cùng lệnh, base `b29da0b` copy | 1 | **266/268**, chạy 268, bỏ qua 0; 983.702 s |
| `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py`, head copy riêng | 0 | **60/60 thực chạy**, tổng 61, bỏ qua 1; cổng/tự kiểm đạt; 908.169 s |
| `python3 review_probes.py matrix`; `python3 review_finding.py`; `python3 review_supplement.py collisions` | 0 / 0 / 0 | Các ca lượt 5 và alias, có đối chứng v2 |
| `python3 review_previous.py`; `python3 review_labels.py` | 0 / 0 | Các ca nguyên bản lượt 6–7 đỏ, control/nhãn sửa đúng xanh |
| `python3 review_prepass.py`; `python3 review_confirm.py` | 0 / 0 | Hai bypass comment + 26 fixture cấu trúc xanh sai, có CLI 3/3 và đối chứng sửa đúng |
| `python3 review_structure.py`; `python3 review_scope.py` | 0 / 0 | 74 + 10 probe cấu trúc/phạm vi |
| `python3 review_supplement.py real / grammar / unicode`; `python3 review_grammar_extra.py` | 0 / 0 / 0 / 0 | README, 192 ca ngữ pháp, Unicode/`.yml`, 2.048 đuôi |
| `python3 review_mutations.py`; `python3 review_listing_mutations.py`; `python3 review_audit.py` | 0 / 0 / 0 | 25 + 4 mutant chết đúng chốt, compile hợp lệ; source sạch |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head/base copy | 1 / 1 | Mỗi bên 7 F401 + 2 F541; **delta 0** |
| Compile trong `warnings.catch_warnings`, head/base | 0 / 0 | Hai SyntaxWarning cũ `\s`, `\d` mỗi bên; **delta nội dung 0** |
| `git diff --check b29da0b HEAD`; `doctrine-scan --root .` trong head copy | 0 / 0 | Không lỗi |
| `python3 review_finalize.py` | 0 | 984 CLI chọn ca có marker/số ca/rc khớp; đối chiếu đủ ca đầy đủ và băm source |

Hai suite lease đầy đủ đều **failed**, không khai N/N đạt. Cùng 2 ca đỏ có thông báo bằng nhau: `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck`: KHÔNG ĐO ĐƯỢC: thiếu `shellcheck` — actionlint IM LẶNG bỏ toàn bộ luật shell khi vắng nó; `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`: chưa tới consumer shellcheck ở t137: KHÔNG ĐO ĐƯỢC: thiếu `shellcheck` — actionlint IM LẶNG bỏ toàn bộ luật shell khi vắng nó. Phần ShellCheck là **not_measured do thiếu công cụ**. **268 ca chung không đổi trạng thái**, thêm đúng 1 ca tên biên nhận mới đạt; không thêm thất bại/bỏ qua. Đủ cặp marker cấp ngoài, đúng tên/thứ tự; đã tách log A/B lồng. `t125` đạt cả hai phía.

Cong: **60/60 thực chạy**, tổng 61, bỏ qua 1; `t47_INDEX_phai_duoc_doc_TRUNG_THUC_va_nguon_py_nhan_du_moi_cach_viet`: không dựng được INDEX chưa hoà giải trên máy này: stage={'0'}. Cổng cây thật, tự kiểm phân hạng, giàn giáo và song song đạt. Chạy chế độ gate của CI `CONG_CU_TEST_BAN_KINH=manh`; **490 mutant bán kính giao mảnh / not_measured trong lượt này**, không ghi thành 490 đạt.

[Đối chiếu từng ca](run/evidence/full-comparison.json), [head log](run/evidence/full-head.stdout), [base log](run/evidence/full-base.stdout), [cong log](run/evidence/full-cong.stdout), [static delta](run/evidence/static-results.json), [kiểm marker CLI](run/evidence/cli-marker-audit.json), [tổng hợp cuối](run/evidence/final-summary.json).

HEAD/tree cuối vẫn khớp đầu review; `git status --porcelain` và `git diff HEAD` ở nguồn rỗng. Module nguồn khớp byte Git; ba module trong bản sao sau test khớp revision tương ứng. [Kiểm nguồn](run/evidence/source-audit.json). Không đo nền Windows hay CI GitHub trong lượt này; không suy các kết quả đó từ Linux. Không push, không gọi API ghi GitHub và không sửa cây Executor.
