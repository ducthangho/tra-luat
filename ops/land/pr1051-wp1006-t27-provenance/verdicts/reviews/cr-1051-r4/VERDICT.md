verdict: changes_requested
reviewed_sha: 3e034594c08ecd758a5d5fb23368d0930692a910
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1051, lượt 4. Các phản chứng cụ thể của lượt 3 đã được vá thật. Tuy nhiên, lớp “ô ghi tên/cột khác vẫn thoả cho tệp trên đĩa” chưa đóng: span hai dấu nháy và dấu `\|` vẫn làm t27 xanh sai. Một lớp, một finding P2; không đếm riêng từng cách viết.

Base: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`. Lượt trước: `cceb0b356136bf445d07ea2bb653cc1fa97f7e8a`. Head tree: `533c92f8563acd016a85df4980fd59ad138048b0`. Diff toàn PR và diff lượt này đều chỉ có `ops/lease_publish_test.py`. Ngưỡng theo PROMPT: chỉ approve khi không còn P0–P3.

## Finding F1 — P2 — `wp1006-case-insensitive-listing-case-sensitive-consumer`

**Vị trí:** `ops/lease_publish_test.py:1675`, `:1676` (đọc span), `:1609` (tách ô); consumer tại `:1815` và `:1868`. Ca mới ở `:2079` chưa phủ các biểu hiện dưới đây.

**Mô tả và tác động.** `giu_span=True` giữ được byte đầu vào, nhưng `_ten_tep` chỉ hiểu cặp backtick đơn. Với ô sau:

```text
``two x-verdict.receipt.yaml``
``two x-verdict.md``
```

hai cặp backtick ngoài bị regex coi là hai span rỗng. `ngoai` còn lại `two x-…`, rồi trích tên `x-…`. Đây là một code span chứa nguyên một chuỗi khác, nhưng lại thoả cho tên trên đĩa. Đã đo cùng kết quả ở cả ba vị trí: cột `biên nhận` và `tệp verdict` của Mục lục, cùng cột `tệp verdict` của bảng cảnh báo. Span có backtick bên trong cũng lọt. Quy tắc span đóng bằng một dãy backtick có cùng độ dài được nêu trong [GFM §6.3](https://github.github.com/gfm/#code-spans).

Ngoài ra, `_bang` dùng `.split("|")`, nên coi `\|` là ranh giới cột. Hai hàng dưới đây cũng được `_kiem_muc_luc` và CLI t27 nhận:

```text
# Trong bảng Mục lục: tệp verdict | biên nhận
| `x-verdict.md` \| x-verdict.receipt.yaml | other.receipt.yaml |

# Trong bảng cảnh báo: tệp verdict | id
| `x-verdict.md` \| C1 | C2 |
```

Ở hàng đầu, cột biên nhận thật ghi `other.receipt.yaml`; parser lấy tên receipt từ cột verdict. Ở hàng sau, cột id thật ghi `C2`; parser lấy `C1` từ cột verdict để thoả caveat C1. `\|` là nội dung ô theo [GFM §4.10, ví dụ 200](https://github.github.com/gfm/#tables-extension-), nên đây là sai cột có thể tái hiện, không chỉ là khác định dạng. Tác động: CI có thể xác nhận mục lục/cảnh báo đã được nâng đúng tên, đúng cột trong khi bảng người đọc thấy vẫn sai.

**Tái hiện đã chạy:**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 review_finding.py
PYTHONDONTWRITEBYTECODE=1 python3 review_probes.py repro
```

Driver thứ nhất rc=0, xác nhận tái hiện lỗi; không có nghĩa các hàng sai đạt yêu cầu. Nó dựng Git fixture đầy đủ riêng, dùng receipt v2 đủ trường, băm đúng và URL neo commit thật. Mã suite và validator được lấy nguyên byte từ head; không mock Git/validator. Kết quả:

| Ca | `_kiem_muc_luc` thực đo | CLI t27 | CLI v2 |
|---|---|---:|---:|
| Tên đúng, id đúng | Xanh | 0, 1/1 | 0, 1/1 |
| Span hai backtick chứa `two x-…`, tại mỗi trong ba ô tên | **Xanh sai** | **0, 1/1** | 0, 1/1 |
| `\|` đưa tên receipt từ cột verdict sang cột receipt | **Xanh sai** | **0, 1/1** | 0, 1/1 |
| `\|` đưa C1 từ cột verdict sang cột id đang ghi C2 | **Xanh sai** | **0, 1/1** | 0, 1/1 |

Các biểu hiện double-backtick và lệch cột cũng tái hiện trên base và lượt trước. Đây là phần còn sót của cùng lớp, không khẳng định là hồi quy mới của lượt 4. V2 vẫn validate đúng receipt thật; không diễn giải thành bypass schema v2. Bằng chứng: [driver tối thiểu](review_finding.py), [kết quả](review-evidence/finding-results.json), [ma trận ba revision](review-evidence/table-probe-results.json), [README span sai](review-evidence/head-receipt-double-tick-literal-README.md), [README lệch cột](review-evidence/head-escaped-pipe-column-receipt-README.md).

**Đề xuất vá ở đâu và thế nào.** Tại `_ten_tep`, nhận diện dãy backtick mở/đóng cùng độ dài và chỉ nhận nguyên nội dung span là một tên; không đưa nội dung code đã từ chối trở lại nhánh văn bản trần. Tại `_bang`, tách ô theo quy tắc escape của bảng, giữ nguyên cột cho `\|`, cả header và dữ liệu. Nhánh tên trần nên kiểm nguyên token theo tập dấu phân cách đã xác định: hiện `x-verdict.receipt.yaml+backup` và `…@backup` vẫn bị cắt thành tên ngắn. Với link Markdown, xử lý nhãn/đích theo chính sách danh tính rõ ràng thay vì gộp token của cả hai; phép đo hiện tại cho thấy nhãn sai hoặc đích sai đều có thể thoả tên.

**Ca khoá.** Mở rộng bước (6) qua `_kiem_muc_luc`/CLI với double-backtick, backtick bên trong và hai hàng `\|` trên, ở đủ ba ô tên và cột id. Mỗi ca sai phải đỏ đúng thông báo thiếu tên/caveat; đối chứng tên đúng, nhiều span độc lập đúng tên, link đúng, dấu phẩy/ngoặc/dấu chấm kết câu phải xanh. Đột biến bỏ xử lý độ dài backtick và bỏ nhận diện escape phải làm các ca này đỏ. Giữ phép so từng ô trên README thật.

**Rủi ro của cách vá.** Parser chặt hơn có thể từ chối các hàng đang đúng: nhiều tên trong một ô, tên trong link, id có backtick, dấu kết câu, Unicode hoặc tên có hoa/thường. Không chữa bằng lowercase toàn tên hoặc lấy basename của một đường khác. Tiếp tục giữ quy tắc bỏ comment/rào mã, cùng hàng/cùng cột và header đã chuẩn hoá.

## ĐỐI CHIẾU LƯỢT TRƯỚC

F1 lượt 3: **VÁ HỜ ở cấp lớp** — các biểu hiện cụ thể đã vá thật, nhưng còn các biểu hiện F1 nói trên. Không phát hiện lỗi mới do giữ span trên các hàng thật đã đo.

Đã chạy lại nguyên script được cấp, chỉ thay dòng import sang bộ nối đường dẫn/fixture ngoài nguồn: [review_r3_repeat.py](review_r3_repeat.py), [bộ nối](review_r3_support.py), [kết quả](review-evidence/r3-repeat/repro-results.json). Driver rc=0. Ở head, span đơn sai, `.bak`, `/child` tại receipt và cảnh báo đều t27 rc=1; ở base chúng đều rc=0. Tên đúng xanh, tên khác hoàn toàn đỏ; t26/v2 đều rc=0. Duyệt lại 2.048 biến thể đuôi chỉ nhận `x.receipt.yaml`; các tên Unicode, bắt đầu dấu chấm/gạch và cặp khác dấu vẫn qua t26/t27/v2, bỏ hàng của tên có dấu làm t27 đỏ.

Ma trận độc lập bổ sung cột verdict của Mục lục, đo cả helper và CLI ở head, base, lượt trước:

| Ô tên thử, ở đủ ba vị trí | Head t27 | Chốt đỏ |
|---|---:|---|
| Span đơn chứa `two x-…` | 1 | Thiếu đúng tên ở cột receipt/verdict, hoặc thiếu C1 đúng hàng cảnh báo |
| `x-….bak` | 1 | Như trên |
| `x-…/child` | 1 | Như trên |
| Tên khác hoàn toàn | 1 | Như trên |
| Tên đúng trần, trong span đơn, link đúng, sau ngoặc/phẩy/chấm | 0 | Đối chứng dương |

Tổng 12 đối chứng âm cũ đều đỏ đúng chốt, 19 đối chứng dương xanh. Toàn bộ 131 biến thể của ma trận (83 head, 24 base, 24 lượt trước) đều có t26/v2 rc=0; helper và CLI t27 đồng ý từng ca. [Kết quả đối chiếu](review-evidence/probe-analysis.json).

## Hàng thật và consumer

So cùng README thật giữa parser/consumer base và head, theo từng hàng/cột, giữ nguyên case/Unicode, đồng thời so tập tên khớp tệp trên đĩa:

| Bảng | Hàng parser trả | Ô tên | Ô id | Delta token / khớp tệp / id |
|---|---:|---:|---:|---|
| Cảnh báo đang có hiệu lực | 750 | 750 | 750 | 0 / 0 / 0 |
| Mục lục | 321, gồm 306 hàng có cột tên | 612 | 0 | 0 / 0 / 0 |

`_bang` mặc định cho kết quả bằng hệt base trên cả hai bảng. `_cot_duy_nhat` vẫn dùng chế độ mặc định; header không đổi. Hai caller trực tiếp còn lại của `_bang` hiện hành là hai bảng trong `_kiem_muc_luc`, đã chủ ý bật giữ span. `_kiem_muc_luc` được gọi bởi t27 và các fixture của suite; đã chạy các caller này. Các `_bang` trong bản lưu lịch sử là định nghĩa riêng; `_bang` trong `bien_nhan_v2.py` là hàm khác đọc hằng. Probe lưu trữ `pr915-review-1-codex/review_probe.py` gọi mặc định, nên không chịu đổi chế độ. Không tìm thấy consumer hiện hành khác đổi hành vi vì tham số mới. [Mỗi ô đã so](review-evidence/real-tables.json), [điểm gọi AST](review-evidence/consumers.json).

## Các đường cùng lớp đã thử qua bảng thật

Mỗi ô dưới đây đều được ghi thành README fixture rồi chạy `_kiem_muc_luc`, CLI t26/t27 và v2; không chỉ assert `_ten_tep` trực tiếp. [Script](review_probes.py), [đủ kết quả/ô/rc](review-evidence/table-probe-results.json).

| Đường | Head t27 ở ba ô tên | Nhận xét |
|---|---|---|
| Nhiều span độc lập, có một span đúng nguyên tên | 0 | Đối chứng hợp lệ |
| Nhiều span, chỉ có tên khác hoặc span đơn `two x-…` | 1 | Chặn đúng |
| Span hai/ba backtick, có hoặc không có backtick bên trong | **0** | Biểu hiện F1 |
| Backtick không đóng | 0 | Đã đo; GFM có thể coi delimiter không đóng là chữ thường, không dùng riêng kết quả này để kết luận bypass span |
| Nhãn link khác/đích đúng, hoặc nhãn đúng/đích khác | 0 | Bộ trích hiện nhận tên ở một trong hai phần; cần định nghĩa chính sách nhãn/đích khi vá |
| Entity khoảng trắng trong code span `two&#32;x-…` | 1 | Không thấy bypass ở dạng này |
| Entity khoảng trắng ngoài span | 0 | Đã đo; không khẳng định đây là một tên đơn có khoảng trắng |
| Entity mã hoá một ký tự của tên đúng | 1 | Bộ đọc hiện không giải mã entity; không tính riêng thành finding |
| Tên verdict chỉ nằm trong ô id, cột verdict ghi tên khác | 1 | Chặn đúng |
| `\|` bên trong span đơn sai tên | 1 | Ca đơn giản chặn; không chứng minh tách cột đúng |
| `\|` dịch tên receipt hoặc id sang cột khác | **0** | Biểu hiện F1, đã có README tối thiểu ở trên |
| Tên trần nối liền `+backup` hoặc `@backup` | **0** | Vẫn cắt tiền tố, cùng lớp sai danh tính |

Ô id riêng: id đúng có backtick và nhiều span id đều xanh; chỉ id khác đỏ. Không dùng việc bộ đọc chấp nhận danh sách id chứa C1 để tính thêm một finding.

## Răng của ca mới

`PYTHONDONTWRITEBYTECODE=1 python3 review_mutations.py`, bổ sung lệnh `python3 review_mutations.py drop-keep-span-ML drop-keep-span-CB`: mỗi mutant riêng trong bản sao tạm, chạy tệp suite bằng `runpy` với `__name__='__main__'`, selector CLI và `main` thật; trace ghi dòng lỗi và lời gọi helper. Control rc=0, 1/1, chạy hết bước (6), 7 lần helper t26 và 18 lần helper t27. Cả 14 mutant đều rc=1, 0/1. [Script](review_mutations.py), [kết quả](review-evidence/mutation-results.json).

| Mutant | rc | Bước / nguyên nhân bị bắt |
|---|---:|---|
| Bỏ giữ span cả hai bảng | 1 | (6), receipt span đơn sai tên được nhận |
| Bỏ giữ span riêng Mục lục | 1 | (6), receipt span sai |
| Bỏ giữ span riêng bảng cảnh báo | 1 | (6), cảnh báo span sai |
| Bỏ biên sau token | 1 | (6), receipt `.bak` được nhận |
| Bỏ bóc backtick của id | 1 | (6), đối chứng đúng `C1` bị báo thiếu |
| Bỏ chốt đuôi | 1 | (1), t26 nhận alias HOA |
| Bỏ chốt tên | 1 | (2), thông báo thiếu lỗi tên chứa khoảng trắng |
| Bỏ lời gọi chốt receipt ở t27 | 1 | (1), t27 nhận alias HOA |
| Bỏ lời gọi chốt verdict ở t27 | 1 | (3), đỏ sai chốt thay vì chốt tên verdict |
| Bỏ lời gọi chốt ở helper t26 | 1 | (1), t26 nhận alias HOA |
| Sidecar so không phân biệt hoa/thường | 1 | (5), nhận nhầm sidecar khác tiền tố |
| Bỏ IGNORECASE ngoài span | 1 | (2), assert tên trần HOA, dòng 2045 |
| Bỏ biên trước token | 1 | (2), assert `plus+name…`, dòng 2042 |
| Bỏ đọc nguyên span | 1 | (2), assert span chứa khoảng trắng, dòng 2042 |

Lần chạy trace đầu bị timeout 60 giây do driver scratch gọi `Path.resolve()` trên mọi sự kiện. Đã sửa driver để chỉ trace tệp suite; control và toàn bộ mutant sau đó hoàn tất. Không coi timeout của driver là mutant bị bắt. Các mutant được yêu cầu có răng, nhưng không phủ double-backtick/escape như F1 đã chứng minh.

## Đã đo

Các lệnh chạy với `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`; Ruff không ghi cache. Bản sao head/base đều ngoài `cay-kho/`, có `.git` riêng và `core.abbrev=7`. Lệnh, cwd, rc, thời lượng và stdout/stderr của các subprocess nằm trong `review-evidence/`; [runner](review_runner.py).

| Lệnh / phạm vi | rc | Kết quả |
|---|---:|---|
| `python3 ops/lease_publish_test.py`, bản sao head | **1** | **267/269**, chạy 269, bỏ qua 0; **697.057 s** |
| Cùng lệnh, bản sao base | **1** | **266/268**, chạy 268, bỏ qua 0; **701.826 s** |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head/base | 1 / 1 | Mỗi bên 7 F401 + 2 F541; delta code/message chuẩn hoá **0** |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_probes.py real` | 0 | 1.362 ô tên + 750 ô id, delta token/khớp tệp/id 0; liệt kê consumer |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_probes.py repro` | 0 | 131 biến thể qua helper và 393 CLI; kiểm thêm marker N/N và v2 đạt, không chỉ rc |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_r3_repeat.py` | 0 | Chạy lại script lượt 3 sau đổi import; các phản chứng cũ bị chặn ở head |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_finding.py` | 0 | Tái hiện F1 bằng 5 biến thể sai vẫn xanh và 1 đối chứng đúng |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_mutations.py` và lệnh bổ sung hai bảng | 0 sau sửa driver scratch | Control 1/1; 14 mutant 0/1, rc con 1, đúng bước |
| `git -C cay-kho diff --check b29da0b HEAD` | 0 | Không lỗi whitespace |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, bản sao head | 0 | Không phát hiện chép doctrine |
| `python3 ops/bien_nhan_v2.py --root .`, bản sao cây thật head | **2** | **not_measured**: kho shallow; không coi là chứng nhận v2 toàn kho |
| `git -C cay-kho status --porcelain=v1 --untracked-files=all` | 0 | Output rỗng |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_runner.py snapshot-final` | 0 | 8.505 entry, delta 0 |

Hai suite đầy đủ đều **failed**, không khai pass toàn bộ. Chúng đỏ đúng hai ca giống nhau:

- `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck`: thiếu `shellcheck`.
- `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`: chưa tới consumer shellcheck vì cùng công cụ bị thiếu.

Phần phép đo ShellCheck là **not_measured** do môi trường. Delta hồi quy: thêm đúng ca tên biên nhận mới đạt; không đổi kết quả ca chung, không thêm ca thất bại hoặc bỏ qua. T125 đạt ở cả hai. Đã kiểm đủ 269/268 cặp marker cấp ngoài, đúng danh sách/thứ tự ca và summary/rc; các log A/B lồng được tách riêng. Mã suite sau chạy còn nguyên byte khớp revision nguồn. [So sánh full](review-evidence/full-comparison.json), [head stdout](review-evidence/full-head.stdout), [base stdout](review-evidence/full-base.stdout), [Ruff](review-evidence/ruff-comparison.json), [393 marker CLI](review-evidence/cli-positive-markers.json).

## Tính toàn vẹn và giới hạn

Snapshot sau preflight và cuối lượt gồm **8.505 entry tệp/symlink**, kể cả tệp trong `.git`: so đường dẫn, loại, mode, băm nội dung và đích symlink cho **delta 0**. HEAD/tree cuối lượt vẫn đúng mỏ neo trên. Đây là không có thay đổi quan sát được giữa hai snapshot, không phải chứng nhận OS cưỡng chế read-only hoặc chưa từng ghi rồi hoàn nguyên. [Trước](review-evidence/source-before.json), [sau](review-evidence/source-after.json), [delta](review-evidence/source-delta.json).

Môi trường Linux, Python 3.13.17, PyYAML 6.0.3, Ruff 0.16.9; actionlint 1.7.7 có sẵn, ShellCheck vắng. Windows thật và CI GitHub: **not_run/not_measured**. Công cụ `environment_status` không có trong tập tool phiên này. Kho nguồn được cấp có `--is-shallow-repository=true`, trái mô tả đủ lịch sử trong prompt; không gỡ marker shallow hay sửa lịch sử để làm xanh. Những phép đo v2 dương/âm ở fixture dùng kho Git đầy đủ riêng và không thay cho việc xác nhận toàn kho thật. [Môi trường](review-evidence/environment.json), [history](review-evidence/history.stdout), [v2 cây thật](review-evidence/v2-real-head.stderr).

Reviewer: Codex, phiên API độc lập; provider `openai_codex`, execution surface `codex_service`, transport `machine` theo ánh xạ của kho. Model ID/effort phục vụ thực tế không có runtime attestation trong bằng chứng này: `KHONG_DO_DUOC`. Theo `CLAUDE.md` §Quy trình sửa code bước 5, một sub-agent chỉ tiêu hoá log suite dài và so kết quả; phiên chính tự đọc mã, dựng/chạy phản chứng và kết luận finding. Không dùng context Executor.

Không push, không gọi API ghi GitHub, không merge/deploy/LIVE; verdict không tự tạo approval/state hoặc quyền land.
