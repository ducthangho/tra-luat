verdict: changes_requested
reviewed_sha: 82a5ef5056e1baf2e285d69b09e4ebf376bf529d
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Biểu hiện vượt cổng v2 của lượt 1 đã được chặn ở t26/t27. Tuy nhiên, lớp bất nhất giữa bộ liệt kê và bộ đọc tên mục lục còn một biểu hiện: tên chứa khoảng trắng. Làm đúng lời chữa đổi đuôi sang thường vẫn không làm t27 xanh, dù receipt hợp lệ và hàng mục lục đúng tên. Một lớp, một finding F1.

## Phạm vi và mỏ neo

- Head đầu/cuối: `82a5ef5056e1baf2e285d69b09e4ebf376bf529d`; tree: `abbade322073df9f348fdead0a206b8febded50e`.
- Base: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`; head lượt 1: `4f9774aecfb14340fcbe59e89d5781d9603457b7`.
- Diff toàn PR và diff lượt này đều chỉ có `ops/lease_publish_test.py`. Toàn PR: 122 dòng thêm, 9 dòng bỏ.
- Chỉ thị hiện tại trong `PROMPT.md` cấp quyền review độc lập, đọc nguồn và ghi scratch bên ngoài `cay-kho/`. Áp ngưỡng approve chỉ khi không còn finding P0–P3.

## Finding F1 — P2 — `wp1006-case-insensitive-listing-case-sensitive-consumer`

**Vị trí:** `ops/lease_publish_test.py:1663` (`_ten_tep`); biểu hiện qua `:1784` và lời chữa mới tại `:1678`. Ca mới tại `:1926` chỉ dùng tên không có khoảng trắng.

**Mô tả.** `_liet_ke_theo_duoi` nhận tên nguyên có khoảng trắng, nhưng regex `_ten_tep` chỉ giữ phần sau khoảng trắng. Ví dụ, `` `two words.receipt.yaml` `` bị trích thành `{"words.receipt.yaml"}`. Vì vậy t27 báo thiếu tên ở đúng cột ngay cả khi ô đã chứa nguyên tên. Chốt đuôi mới từ chối `two words.RECEIPT.YAML` và yêu cầu đổi đuôi sang `.receipt.yaml`; làm theo, đồng thời sửa hàng mục lục, vẫn đỏ bởi cùng sự bất nhất này. Thêm lại chính hàng ấy không chữa được.

Đây là **biểu hiện còn sót của lớp được giao kiểm**, đã có ở base đối với tên chứa khoảng trắng; không quy nó thành hồi quy mới do thay đổi glob ở lượt 2. Phạm vi hiện tại yêu cầu kiểm lời chữa làm được và đường thứ ba cùng lớp, kể cả tên có khoảng trắng. Không thấy hợp đồng trong README review, protocol hay validator v2 cấm khoảng trắng trong tiền tố tên receipt. Validator thật cũng chấp nhận tên đó trong đối chứng bên dưới.

**Tái hiện đã chạy:** [review_mini_cli.py](review_mini_cli.py), rc=0. Script dựng một kho Git fixture có lịch sử đầy đủ, một verdict đã commit và receipt v2 hợp lệ với mỏ neo Git thật trong kho fixture. URL và identity là dữ liệu giả của fixture, không phải chứng cứ review bên ngoài. Mã `lease_publish_test.py` được chép nguyên byte từ head; gọi nguyên validator head bằng `--root`, không vá mã hay mock chốt Git.

| Cùng byte receipt v2 hợp lệ; hàng mục lục luôn đúng tên | t26 CLI | t27 CLI | v2 CLI |
|---|---:|---:|---:|
| `two words.RECEIPT.YAML` | 1, từ chối đuôi | 1, từ chối đuôi | 0, chỉ đếm receipt nền |
| Đổi theo lời chữa thành `two words.receipt.yaml` | **0** | **1**, báo thiếu ở cột `biên nhận` | **0**, đếm đủ **2 receipt đạt v2** |
| Đổi thêm tiền tố thành `two-words.receipt.yaml` | 0 | 0 | 0, đếm đủ 2 |

Lỗi sau khi đổi đuôi:

```text
README.md: biên nhận two words.receipt.yaml KHÔNG có trong CỘT 'biên nhận' của bảng 'Mục lục'
```

Kết quả và hash byte receipt: [mini-results.json](review-evidence/mini-results.json). Log trực tiếp: [t27 sau đổi đuôi](review-evidence/mini-valid-space-renamed-t27.stdout), [v2 nhận cùng receipt](review-evidence/mini-valid-space-renamed-v2.stdout). Cả ba biến thể hợp lệ có cùng hash receipt.

Đã đối chứng thêm trên bản sao đầy đủ cây head bằng receipt wp929 nguyên byte: `review alias.RECEIPT.YAML` → `review alias.receipt.yaml` vẫn đỏ t27; đổi thêm thành `review-alias.receipt.yaml` thì t26/t27 xanh. Validator trên bản sao này không đo được vì lịch sử shallow, nên bằng chứng validator dương lấy từ kho fixture đầy đủ ở trên. [schema-results.json](review-evidence/schema-results.json). Probe helper xác nhận base cũng có lỗi tên chứa khoảng trắng; `plus+name.receipt.yaml` là biểu hiện cùng cơ chế. [boundary-results.json](review-evidence/boundary-results.json).

**Đề xuất — vá ở đâu, thế nào.** Đồng bộ hợp đồng tên ở `_ten_tep`, consumer mục lục/cảnh báo và chốt tên. Nếu tiếp tục nhận tiền tố có khoảng trắng, đọc nguyên token trong code span/đích liên kết Markdown và so nguyên danh tính, thay vì trích hậu tố của tên bằng regex hiện tại. Nếu chọn từ chối các tiền tố không biểu diễn được, cần chốt tên rõ ràng trước consumer và lời chữa nêu cả tiền tố cần sửa; chỉ yêu cầu đổi đuôi chưa đủ.

**Ca khóa.** Dùng receipt v2 đầy đủ, đúng băm/URL và đúng hàng, thử cả alias lẫn sidecar có khoảng trắng. Tên HOA phải đỏ đúng chốt; thực hiện nguyên hướng dẫn phải làm **cả t26 và t27 xanh**. Bỏ hàng phải đỏ đúng cột. Kiểm thêm token `words.receipt.yaml` không được nhận nhầm từ ô chỉ ghi `two words.receipt.yaml`.

**Rủi ro của cách vá.** Không dùng substring hoặc lowercase toàn tên để chữa parser; không làm mất sự phân biệt stem, nhận tên chỉ nằm trong comment HTML, hay nhận nhầm tên từ cột khác. Giữ kiểm đường dẫn đầy đủ và băm. Owner đề xuất: maintainer `ops/lease_publish_test.py`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Nguồn / biểu hiện | Phân loại và bằng chứng hiện tại |
|---|---|
| F1 lượt 1, `4f9774a`: alias HOA `schema_version: 999` vượt cả t26/t27/v2 | **ĐÃ VÁ THẬT đối với biểu hiện bypass này**: CLI t26/t27 head cùng đỏ ở chốt đuôi, kể cả mixed case. Đuôi thường vẫn bị validator chặn đúng schema. Bảng dưới đo bằng CLI thật trên Git fixture đầy đủ. |
| F1 kiểm toán #1007: consumer không xử lý nhất quán tên đã được liệt kê; lời chữa không làm xanh | Đuôi HOA của tên thông thường và lookup sidecar đã được xử lý bằng chính sách từ chối. **CHƯA VÁ hết lớp**: F1 lượt này là tên có khoảng trắng, đã có ở base; làm đúng lời chữa vẫn đỏ. Không tuyên bố đóng cả lớp chỉ từ đối chứng `alias` không chứa khoảng trắng. |

Phản chứng lượt 1 được lặp với một receipt nền hợp lệ và alias có đầy đủ trường, chỉ đổi `schema_version` thành 999. Giữa các tên alias, byte YAML giữ nguyên; hàng mục lục luôn có:

| Alias lỗi | t26 | t27 | v2 | Validator đếm |
|---|---:|---:|---:|---|
| `alias.receipt.yaml` | 0 | 0 | **1**, `schema_version=999, đòi 2` | 2 receipt, 1 vi phạm |
| `alias.RECEIPT.YAML` | **1** | **1** | 0 | Chỉ 1 receipt nền; alias bị bỏ qua |
| `alias.reCeipt.YamL` | **1** | **1** | 0 | Chỉ 1 receipt nền; alias bị bỏ qua |

Như vậy glob v2 vẫn bỏ tên HOA trên POSIX, nhưng tổ hợp cổng đã chặn chúng ở t26/t27. Không diễn giải rc=0 riêng của validator thành alias được validate. [mini-results.json](review-evidence/mini-results.json).

## Biên tên và các consumer

- Duyệt đủ **2.048** biến thể hoa/thường ASCII của `.receipt.yaml` qua chốt mới: chỉ nhận đúng `.receipt.yaml`. Với tệp con trực tiếp tồn tại, kể cả symlink tới tệp, tập tên t26/t27 có thể nhận vì thế nằm trong tập glob thường mà v2/packet đọc trên Linux. Không tìm thấy bypass kiểu suffix khác còn được cả t26/t27 nhận trong tập đã đo.
- Tiền tố HOA với đuôi thường được giữ nguyên. Verdict `.MD`/`-VERDICT.md`, caveat cùng hàng và sidecar đúng stem hoạt động; đổi case tên trong hàng caveat hoặc trỏ sang đường dẫn archive khác đều đỏ. Sidecar chỉ khác case tiền tố bị từ chối; không gộp danh tính.
- Symlink tới tệp, đuôi thường: t26/t27 xanh và packet đọc được; đuôi HOA: t26/t27 đỏ. Đây đúng nghĩa `Path.is_file()`, không phải cổng cấm symlink.
- Thư mục, symlink tới thư mục và symlink gãy mang đuôi thường: helper của t26/t27 loại khỏi tập tệp; glob của reader vẫn thấy chúng. Packet reader thật trả `SystemExit(11)` khi không đọc được. Đây là khác biệt tập entry đã có ở base và chặn khi đọc, không phải bypass nhận receipt lỗi. CLI v2 trên cây thật trả rc=2 từ chốt shallow trước khi tới các entry này, nên không khai đã đo lỗi I/O của v2 ở đó.
- README dùng sidecar `*.receipt.yaml`; protocol và validator không hứa nhận receipt suffix HOA. Không thấy mâu thuẫn hợp đồng do riêng chính sách từ chối suffix HOA. F1 là phần tiền tố/parser và lời chữa còn thiếu.

Quét tĩnh consumer đang hoạt động tại [static-inventory.json](review-evidence/static-inventory.json); không tính các snapshot review/land/evidence thành consumer đang chạy. Các vị trí glob ngoài PR còn nguyên: `bien_nhan_v2.py:1442`, `:1601`; `bien_nhan_v2_test.py:1705`, `:1908`; `packet_loop.py:2121`. Đã chạy reader packet thật và CLI sinh nợ: đuôi thường sinh 1 mục lỗi, HOA/mixed sinh 0. Không khai đã chạy toàn suite `bien_nhan_v2_test.py` hay c38/c42. [boundary-results.json](review-evidence/boundary-results.json), [additional-results.json](review-evidence/additional-results.json).

## Răng của ca mới

Chạy CLI chọn đúng tên ca mới trên từng bản sao riêng, mỗi mutant chỉ đổi một chốt. [review_mutations.py](review_mutations.py), [mutation-results.json](review-evidence/mutation-results.json).

| Bản / đột biến | rc / số ca | Điểm phát hiện |
|---|---|---|
| Control | 0 / 1/1 | Chạy hết ca |
| Bỏ assertion đuôi trong helper | 1 / 0/1 | Bước 1, t27 nhận alias HOA nên phản chứng đỏ |
| Bỏ lời gọi chốt đuôi trong t27 | 1 / 0/1 | Bước 1, cùng lý do |
| Bỏ lời gọi chốt đuôi trong thân t26 (`_kiem_bam_bien_nhan`) | 1 / 0/1 | Phép t26 ở bước 1: bắt lỗi NỬA VỜI thay vì lỗi đuôi, assertion “SAI chốt” làm đỏ |
| So tiền tố sidecar không phân biệt case | 1 / 0/1 | Bước 4: nhận nhầm `c-verdict.receipt.yaml` |
| Bỏ IGNORECASE riêng ở `_ten_tep` | 1 / 0/1 | Assertion token HOA ở bước 1 |

Trace [mutation-trace.json](review-evidence/mutation-trace.json) xác nhận 5 lời gọi `_kiem_muc_luc`, 1 lời gọi `_kiem_bam_bien_nhan`, và tới bước kiểm stem cuối. Ca không còn nhánh `phan_biet`/`except OSError` để bỏ phép đo như lượt 1.

**Giới hạn:** đối chứng đổi đuôi về xanh trong ca mới chỉ gọi t27; fixture của nó thiếu băm/URL nên không chứng minh chiều dương t26. Review này đo chiều dương t26 bằng fixture đầy đủ và CLI ở trên. Đột biến bổ sung bỏ hẳn delegation ở entry point t26 (`:1693`) còn sống qua riêng ca mới: nó gọi helper trực tiếp. Đây là giới hạn wiring của ca, tách với năm đột biến chốt nêu trên; không tính thành finding độc lập về hành vi head.

## Đã đo

Mọi clone, mutant, fixture, cache/output đều ngoài `cay-kho/`. Python chạy với `PYTHONDONTWRITEBYTECODE=1`; Ruff dùng `--no-cache`. Wrapper [review_runner.py](review_runner.py) ghi argv/cwd/rc/thời lượng và stdout/stderr riêng cho các lệnh con.

| Lệnh / phạm vi | rc | Kết quả |
|---|---:|---|
| `git -C cay-kho rev-parse HEAD HEAD^{tree} b29da0b 4f9774a` | 0 | Khớp các OID đã nêu |
| `python3 review_runner.py setup` | 0 sau sửa bootstrap scratch | Hai clone, đủ refs đã cấp, `core.abbrev=7`. Lần bootstrap đầu rc=1 do batch update trùng symref; sửa riêng scratch bằng `update-ref --no-deref`, không sửa nguồn |
| `python3 ops/lease_publish_test.py`, clone head | **1** | **267/269**, chạy 269, bỏ qua 0; **502.199s** |
| Cùng lệnh, clone base | **1** | **266/268**, chạy 268, bỏ qua 0; **499.881s** |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head / base | 1 / 1 | Mỗi bên 7 F401 + 2 F541; so code/message chuẩn hóa: **delta 0** |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_mutations.py` | 0 | Control, năm mutant bắt buộc, trace và mutant wiring bổ sung; rc con ghi riêng |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_probes.py` | 0 sau sửa import scratch | Biên tên/file kind, CLI trên bản sao cây thật; từng rc tại JSON. Lần đầu rc=1 do thiếu đường import `launcher`, chưa chạy probe; thêm đường module của clone rồi chạy lại |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_additional.py` | 0 | Cấu trúc v2 dương/âm, 2.048 suffix, reader sinh nợ, Ruff delta |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_mini_cli.py` | 0 | CLI thật trên Git fixture đầy đủ: bypass bị chặn; F1 tái hiện bằng receipt v2 hợp lệ |
| `python3 ops/bien_nhan_v2.py --root .`, clone cây thật trước thêm alias | **2** | **not_measured** về tính hợp lệ toàn kho: lịch sử shallow |
| `git --git-dir=review-evidence/history-check.git fsck --connectivity-only --no-dangling` | **2** | Object store được cấp thiếu commit cha; không tự xóa marker shallow để làm cổng xanh |
| `git -C cay-kho diff --check b29da0b HEAD` | 0 | Không lỗi whitespace |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, clone head | 0 | Không phát hiện chép doctrine |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_runner.py snapshot-final` | 0 | Snapshot nguồn đầu/cuối khớp, 8.468 tệp |

Hai suite đầy đủ cùng đỏ đúng hai ca: `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck` và `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`, đều do thiếu ShellCheck. Hai lệnh suite giữ nhãn **failed**; các phép đo ShellCheck là **not_measured**, không quy cho PR. Delta đúng một ca mới đạt, không thêm ca thất bại hoặc bỏ qua; đủ 269/268 cặp nhật ký cấp ngoài, không cộng các lượt A/B lồng trong t125. [full-comparison.json](review-evidence/full-comparison.json), [head stdout](review-evidence/full-head.stdout), [base stdout](review-evidence/full-base.stdout).

## Giới hạn và tính toàn vẹn

Linux, Python 3.13.17, PyYAML 6.0.3, Ruff 0.16.9; có actionlint, thiếu ShellCheck. Windows thật và CI GitHub: **not_measured**. Kho được giao thực tế shallow dù prompt mô tả đủ lịch sử; phép fsck ở bare scratch riêng xác nhận thiếu object cha. Kết quả CLI v2 dương/âm trên Git fixture đầy đủ không thay cho chứng nhận toàn kho thật đạt validator.

Snapshot nguồn so nội dung tracked/untracked/ignored, HEAD/tree, refs, diff/index và hash HEAD/index/config/packed-refs; các trường đã chụp khớp đầu/cuối. Không có hash đầu kỳ của mọi tệp phụ trong `.git` (đặc biệt shallow), nên không mở rộng kết luận sang toàn bộ `.git`. Đây là không có delta quan sát được trong phạm vi snapshot, không phải chứng nhận OS cưỡng chế read-only hay chưa từng ghi rồi hoàn nguyên. [source-before.json](review-evidence/source-before.json), [source-after.json](review-evidence/source-after.json).

Reviewer: OpenAI Codex, phiên API độc lập, provider `openai_codex`, execution surface `codex_service` theo ánh xạ của kho, transport `machine`. Model ID/effort thực phục vụ không có runtime attestation trong bằng chứng lượt này: **KHONG_DO_DUOC**. Executor Claude là thông tin phân công trong prompt, không phải phép đo runtime của reviewer. Không push, không gọi API ghi GitHub, không merge/deploy/LIVE; verdict không tự tạo state approval hoặc quyền land.
