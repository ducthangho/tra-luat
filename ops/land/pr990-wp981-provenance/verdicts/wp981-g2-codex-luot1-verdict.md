verdict: changes_requested
reviewed_sha: a75d3ec3d8986f25fdfafc7c106a112393ce3504

Có **1 finding P2**: bộ chấm đột biến nhận lỗi thực thi của tiến trình con thành bằng chứng giết đúng ca. Chưa phát hiện lỗi hành vi sản phẩm trong M1–M3 qua các phép đo dưới đây. Không approve khi finding này còn mở.

## Phạm vi và định danh

- Packet `wp981`, r2, lượt 1/2, lớp `sensitive`; reviewer Codex/họ OpenAI, độc lập với executor họ Claude theo assignment. Thực thi bằng công cụ shell cục bộ của phiên API, transport machine; không có receipt model/effort của launcher để xác minh riêng trong bundle này.
- Base: `74132ce20cb1f9f74e163717908eca384f672dd0`; head: `a75d3ec3d8986f25fdfafc7c106a112393ce3504`; tree: `f090e39fac8095c0b44f75696896f7a5acb715c0`.
- Tự băm `SPEC.md`: `3d026415193d3f3b1ceef005cdc99fcc73871b0c7539697f82b4b0198f578079`, đúng giá trị được cấp. Diff sinh lại từ Git khớp từng byte với `diff.patch`.
- `git diff --numstat BASE HEAD`: `47 11 ops/kiem_ho_so_land.py`; `98 3 ops/kiem_ho_so_land_test.py`. Đúng 2 tệp cho phép, **145 dòng thêm ≤ 200**. `ops/land/` không đổi.
- Python `3.13.17`. Mọi fixture, bản sao đột biến và output nằm trong `evidence/`; `TMPDIR` trỏ `evidence/tmp`, tắt ghi bytecode. Selftest toàn kho chạy trên clone cục bộ `evidence/gate-copy/`, cùng head/tree.
- Không push, không sửa branch executor. `cay-kho/` sạch ở đầu và cuối: tracked/untracked/ignored, working diff, index diff đều rỗng; HEAD/tree không đổi. Đây là so sánh hai mốc, không phải chứng nhận lịch sử mọi lần ghi. [Bằng chứng cuối](evidence/integrity-final.json); [nhật ký cập nhật theo hướng](evidence/progress.md).

## Finding

### mutant-crash-counted-as-kill  [P2]  Ngoại lệ vô can vẫn được công nhận là giết đúng ca đích

**TỆP/DÒNG:** `ops/kiem_ho_so_land_test.py:355`; liên quan `_wp981_ket_qua` dòng 309–322 và mutant `bo_loi_khoi` dòng 341.

**VẤN ĐỀ:** `_wp981_ket_qua` trả cùng loại chuỗi cho sai khác hành vi và cho trường hợp không có kết quả vì tiến trình con chết. `ca_wp981_dot_bien` chỉ hỏi kết quả của tên ca có khác `None` hay không, nên không phân biệt hai loại này. Trong tám mutant đang giao, `bo_loi_khoi` bỏ chốt ánh xạ nhưng sau đó gọi `.get()` trên chuỗi: ca đích đỏ do `AttributeError`, rc 1, stdout rỗng/không có JSON. Đây không phải phép đo ngữ nghĩa thay `LOI/3` bằng một kết quả xử lý sai hợp lệ. Bốn mutant bắt buộc đích (i), (iii), (vi), (viii) chết đúng tính chất; riêng bằng chứng mutation cho (v) chưa đáp ứng yêu cầu “đỏ vì chốt đang thử, không vì lỗi vô can”.

Lỗ hổng của bộ chấm được xác nhận độc lập: thay mutant `bo_da_duyet` bằng một biểu thức **ném `RuntimeError`**, không thực hiện phép thử bỏ luật `da_duyet`, vẫn được `ca_wp981_dot_bien()` công nhận PASS. Khi một hồ sơ làm tiến trình gom chết, tất cả ca trong lô còn bị gán chuỗi `vắng`; chọn tên ca đích không tự chứng minh ca đó đã được đo.

**ĐÃ THỬ NGHIỆM:**

```text
python -B evidence/review_probes.py mutations
rc=0 của script đo
baseline: cả 16 ca con đều đạt
bo_loi_khoi -> khoi-chuoi:
  rc 1 (cần 3, LOI)
  AttributeError: 'str' object has no attribute 'get'
  json=null; stdout=""; classification=CRASH
harness-unrelated-runtimeerror:
  result="PASS (false credit)"
  criterion="bo_da_duyet -> b-tt"
  RuntimeError: REVIEW_UNRELATED_FAULT
```

Output/raw stderr và mọi bản sao: [mutations.json](evidence/mutations.json), [mutations.out](evidence/mutations.out), [script đo](evidence/review_probes.py).

**GỢI Ý VÁ:**

1. Vá ở `_wp981_ket_qua`/`ca_wp981_dot_bien`, nơi kết quả được phân loại; mã sản phẩm hiện trả `LOI/3` đúng, không cần đổi để chữa lỗi thước đo.
2. Trả kết quả có phân loại rõ: ca đích đã chạy và sai kỳ vọng, lỗi thực thi/thiếu JSON, hoặc đạt. Chỉ loại thứ nhất được tính là giết đúng tính chất; lỗi thực thi phải làm phép chứng minh thất bại. Giữ baseline dương và kiểm đích cụ thể.
3. Đổi mutant (v) sang sai lệch ngữ nghĩa có thể chạy, chẳng hạn chỉ đổi return của khối sai kiểu từ `LOI` thành `BO_QUA`. Thêm phép tự kiểm bộ chấm bằng lỗi import/ngoại lệ vô can; những lỗi này phải bị từ chối, còn bốn mutant bắt buộc vẫn được nhận.
4. Rủi ro khi vá: phân loại bằng chuỗi `AssertionError`/`Traceback` có thể lại cấp tín dụng giả hoặc chặn nhầm lỗi nghiệp vụ có chủ đích. Nên giữ trạng thái tiến trình và kết quả ca dưới dạng cấu trúc, phân biệt `LOI/3` hợp lệ với crash, và kiểm cả đối chứng dương lẫn âm.

**ĐÃ THỬ VÁ:** chưa đổi harness trong repo. Đã thử mutant thay thế trên bản sao: `ignore-bad-block-semantic` làm `khoi-chuoi` và `khoi-ds` đỏ vì `rc 0 (cần 3, LOI)`, JSON có `BO_QUA`, không có traceback. Lệnh `python -B evidence/review_probes.py own`, output [own.json](evidence/own.json): `9/10` ở bộ kiểm hành vi. Phép này cô lập đúng thuộc tính mà N1(v) yêu cầu.

**ĐỘ TIN:** cao; tái hiện được với đúng head, có baseline và raw output. Đây là lỗi bằng chứng kiểm thử, không phải kết luận mã sản phẩm đang chấp nhận hồ sơ sai.

## Đối chiếu M1–M3 từng điều kiện

Các lệnh dưới đây chạy từ thư mục chứa `VERDICT.md`; script tự đặt fixture ngoài checkout. Output từng ca nằm trong các tệp JSON cùng tên.

| Điều kiện | Kết quả mã thật và bằng chứng |
|---|---|
| M1: chỉ khóa mức gốc, fullmatch `landed_\d{8}` | Đúng tại `kiem_ho_so_land.py:100`; `python -B evidence/review_probes.py names` rc 0: 7/9 chữ số, tiền/hậu tố, LF cuối, khóa lồng đều `BO_QUA`; 8 chữ số nhận. Chữ số Unicode được nhận đúng ngữ nghĩa `\d`; không tự thêm luật ngày lịch. |
| M1: khóa không phải `str` | Được lọc trước regex/sort. Khóa null, bool, int, float, date trong hồ sơ b hợp lệ đều `DAT`, không traceback (`names.json`). |
| M1: a OR b và thứ tự kiểu a | Đúng tại dòng 93–110. `python -B evidence/review_probes.py a` rc 0: ma trận 60 tổ hợp root/nested × b × URL, thêm 8 ca ưu tiên. Khi có `trang_thai_packet`, không quay về `landed` gốc. `trang_thai_packet` sai kiểu vẫn `LOI/3`, kể cả b hợp lệ. |
| M2: khối có tên khớp phải là ánh xạ | Đúng tại dòng 101–103. `python -B evidence/review_probes.py types` rc 0: null/list/str/int/bool đều `LOI/3`, cả khi a đã True. Không dùng a để bỏ qua cấu trúc khối hỏng. N1(v) làm rõ phải bắt cả khối scalar chưa thể đọc `landed`. |
| M2: quyết định là ánh xạ | Đúng tại dòng 64–67. Null/list/str/bool/int/set đều `TRUOT/1`, nêu `<khối>.quyet_dinh_chu_kho`; không crash, không đổi thành `LOI` (`types.json`). |
| M2: `trang_thai` đúng chuỗi `da_duyet`, không ép kiểu | Đúng tại dòng 69–71. Null/list/dict/bool/int, sai hoa thường hoặc khoảng trắng đều `TRUOT/1`, nêu khóa trạng thái (`types.json`). |
| M2: comment đúng cả kiểu/prefix/mảnh | Đúng qua `_url_hop_le` dùng chung. N1(ii) và phép đối chiếu 19 giá trị × base-a/head-a/head-b đều đúng (`hunt-url-parity.json`, 57 phép đo). Các dạng URL lỏng mà luật cũ vốn nhận vẫn nhận; không tự siết hợp đồng ngoài SPEC. |
| M2: **mọi** khối active đều phải hợp lệ | Hai khối, một khối hỏng nằm trước hoặc sau khối tốt, đều `TRUOT` đúng tên khóa; có/không a không đổi kết quả (`types.json`). Ba khối active với khối cuối thiếu comment cũng `TRUOT` (`hunt-many-block-count.json`). |
| M2: SHA gốc bắt buộc như cũ | Hàm `_menh_de_truot` luôn kiểm SHA ở dòng 54–56. Pure b với SHA thiếu, số, rỗng, 39 ký tự, chữ hoa, LF cuối, dict/list đều `TRUOT/1` (`types.json`). |
| M2: pure b không đòi URL gốc | URL gốc vắng/KHONG_AP_DUNG/null/bool/số/list/dict/rỗng đều không làm b hợp lệ trượt; khi comment thiếu vẫn `TRUOT`, kể cả URL gốc vắng (`types.json`, `mutations.json`). |
| M2: a không được nới ở bất kỳ đường mới nào | Điều khiển `doi_url_goc=landed is True` tại dòng 108. URL gốc sai vẫn `TRUOT` ở cả a gốc và a nested, b vắng/True/False/chuỗi/số. Cả a True + b True hợp lệ vẫn phải qua URL gốc (`a.json`). |
| M2: landed khác bool True không kích hoạt b | `"true"`, `1`, `1.0`, False, null, list, dict đều `BO_QUA` khi a không landed (`names.json`); so `is True` tại dòng 104. |
| M3: nguồn landed ở DAT/TRUOT | Đúng: a gốc ghi `landed (mức gốc)`, a nested ghi `trang_thai_packet.landed`, b ghi `<khối>.landed`; hỗn hợp ghi đầy đủ nguồn. Kiểm cả dòng đạt/trượt qua `a.json`, `types.json` và dữ liệu thật. |
| M3: docstring và miễn trừ | Docstring đầu tệp giải thích OR a/b, comment, ngoại lệ URL chỉ cho b và nguồn báo cáo. AST của `MIEN_TRU` giống hệt base, vẫn đúng một mục pr672. `TRUOT` ở mục ấy được miễn, `LOI` vẫn rc 3 (`cli.json`). |
| Không đổi mã thoát/`--json` | `python -B evidence/review_probes.py cli` rc 0: sạch/skip rc 0; trượt rc 1; lỗi cùng trượt rc 3; root sai + thiếu PyYAML rc 2 trước quét. Text và JSON cùng rc; schema khóa ngoài/dòng không đổi. Giá trị `ly_do` thay theo M3. |

Không thấy đường nới kiểu a trong bản sản phẩm đang review. Các mutant sống ở phần dưới là giới hạn bộ test, không được dùng để gán hành vi mutant cho head thật.

## N1: có ca và đã đo từng ca

`python -B evidence/review_probes.py mutations` chạy lại từng fixture độc lập, lưu rc, trạng thái, lý do và stderr. Bộ WP981 gồm **14 ca thường + 2 ca LOI = 16 ca con**; baseline đều đạt.

| Mục | Ca trong repository | Output của mã thật | Mutant và kết quả đích |
|---|---|---|---|
| (i) | `b-du` | `DAT`, rc 0, nguồn `landed_20261027.landed` | `bo_nhanh_b`: `BO_QUA`, chết đúng tính chất |
| (ii) | `b-cmt-manh`, `b-cmt-tien-to`, `b-cmt-so`; thiếu comment ở `b-kad-cmt-vang` | Tất cả `TRUOT`, rc 1, đúng `.comment` | `bo_kiem_comment`: các ca này thành `DAT`, chết đúng tính chất |
| (iii) | `b-tt` | `TRUOT`, rc 1, đúng `.trang_thai` | `bo_da_duyet`: `DAT`, chết đúng tính chất |
| (iv) | `b-landed-chuoi`, `b-landed-mot` | `BO_QUA`, rc 0 | `ep_kieu_landed_khoi`: `DAT`, chết đúng tính chất |
| (v) | `khoi-chuoi`, `khoi-ds` | `LOI`, rc 3, không traceback | `bo_loi_khoi`: crash rc 1; **bằng chứng mutation chưa đạt**, finding P2 |
| (vi) | `a-khong-manh` | `TRUOT`, rc 1, `authorization_url` | `noi_kieu_a`: `DAT`, chết đúng tính chất |
| (vii) | `ten-7so`, `ten-x` | `BO_QUA`, rc 0 | `noi_ten_khoi`: `DAT`, chết đúng tính chất |
| (viii) | `b-kad`, `b-vang-url`, `b-kad-cmt-vang` | `DAT/0`, `DAT/0`, `TRUOT/1` | `doi_url_goc_kieu_b`: `b-kad`, `b-vang-url` thành `TRUOT`, chết đúng tính chất |

Ca cộng thêm `b-ab` cũng `DAT/0`. Repository chưa có ca tổ hợp URL gốc vắng + comment vắng; reviewer đã bổ sung phép đo này, kết quả `TRUOT/1` đúng `.comment`. Bốn mutant bắt buộc được đo độc lập, đều chết đúng lý do. Tổng: **7 mutant chết bằng sai khác hành vi, 1 crash bị cấp tín dụng**, không phải 8/8 bằng chứng hợp lệ.

## Năm đột biến riêng

Lệnh: `python -B evidence/review_probes.py own` (rc 0 của script đo). Mỗi mutant có tệp riêng, baseline dương, phản chứng đích riêng. Chạy toàn bộ **10 ca kiểm hành vi** của repository (9 cũ + ca WP981), loại duy nhất `ca_wp981_dot_bien` vì nó tự sinh mutant và kiểm mẫu văn bản, không phải phép kiểm hành vi trực tiếp của candidate. Không gọi kết quả này là 11/11.

| Mutant độc lập | Thay đổi | Output test hành vi | Phản chứng reviewer, baseline → mutant |
|---|---|---|---|
| `skip-sha-pure-b` | Chỉ kiểm SHA nếu còn đòi URL gốc | **SỐNG: `10/10`, rc 0** | Pure b SHA `bad`: `TRUOT/1` → `DAT/0` |
| `only-first-active-block` | `for k in khoi_true[:1]` | **SỐNG: `10/10`, rc 0** | Khối active thứ hai thiếu comment: `TRUOT/1` → `DAT/0` |
| `relax-a-if-active-b` | Đòi URL gốc chỉ khi a True và không có b active | **SỐNG: `10/10`, rc 0** | a True + b hợp lệ + URL gốc thiếu mảnh: `TRUOT/1` → `DAT/0` |
| `accept-b-integer-one` | Đổi `is True` thành `== True` riêng ở b | **CHẾT: `9/10`, rc 1**, ca `b-landed-mot` | `BO_QUA/0` → `DAT/0` |
| `ignore-bad-block-semantic` | Khối sai kiểu trả `BO_QUA` thay `LOI` | **CHẾT: `9/10`, rc 1**, hai ca `khoi-*` | `LOI/3` → `BO_QUA/0`, JSON hợp lệ |

Ba mutant sống chỉ ra các ca nên bổ sung để khóa M2: SHA không hợp lệ ở pure b, nhiều khối active, và a+b cùng active với URL gốc sai. Bản thật đã vượt qua các phản chứng này. Xem [mỏ neo/thay thế, output và dữ liệu phản chứng](evidence/own.json).

## Bảng SĂN — sáu hướng bổ sung độc lập

Không dùng việc băm spec, đếm dòng, chạy lại N2 hay chạy nguyên bộ test làm sáu hướng săn. Các lệnh dưới chạy fixture mới; output là trích từ log thật, rc của mỗi script đều 0 vì các khẳng định kiểm tra đều đạt.

| Hướng/giả thuyết | Lệnh | OUTPUT THẬT (trích) | Kết luận |
|---|---|---|---|
| Alias/merge YAML có thể bỏ kiểm thẩm quyền hoặc làm đệ quy vỡ | `python -B evidence/hunt.py aliases` | `approval-alias-valid`: `DAT`, rc 0; `approval-alias-bad`: `TRUOT`, rc 1; `recursive-decision-alias`: `TRUOT`, rc 1; `merge-key-block`: `DAT`, rc 0 | KHÔNG PHẢI LỖI — [4 phép đo](evidence/hunt-aliases.json) |
| Tách helper URL có thể thay luật cũ ở biên kiểu/prefix/mảnh | `python -B evidence/hunt.py url-parity` | 19 đầu vào × 3 đường = 57 phép so đạt; `url-18-base-a`, `url-18-head-a`, `url-18-head-b` cùng `statuses: ["DAT"], rc: 0`; các URL sai bị từ chối cùng nhau | KHÔNG PHẢI LỖI — [57 phép đo](evidence/hunt-url-parity.json) |
| Đếm theo khối thay vì theo hồ sơ, hoặc bỏ khối hỏng cuối | `python -B evidence/hunt.py many-block-count` | `three-active-count-once`: `counts: [1,1,0]`; `a-plus-three-b-count-once`: `[1,1,0]`; `invalid-last-block-count-once`: `TRUOT`, rc 1, `[0,1,0]` | KHÔNG PHẢI LỖI — [3 phép đo](evidence/hunt-many-block-count.json) |
| Thứ tự khóa YAML có thể thay trạng thái/lý do, che khối lỗi | `python -B evidence/hunt.py serialization-order` | Sáu hoán vị đều `TRUOT/1` ở `landed_20261028.quyet_dinh_chu_kho.comment`; `JSON_IDENTICAL_ALL_6_PERMUTATIONS` | KHÔNG PHẢI LỖI — [log](evidence/hunt-serialization-order.out) |
| Quyết định cũ sai kiểu trong khối inactive có thể làm hồ sơ b hợp lệ trượt | `python -B evidence/hunt.py inactive-stale-approval` | Năm giá trị inactive False/`"true"`/1/null/vắng đều `statuses: ["DAT"], rc: 0, counts: [1,1,0]` | KHÔNG PHẢI LỖI — [5 phép đo](evidence/hunt-inactive-stale-approval.json) |
| Giá trị YAML lỗi nằm trong nhánh mới có thể thoát khỏi cơ chế rc 3 | `python -B evidence/hunt.py reader-errors` | `bad-timestamp`: `LOI/3`, `YAML không đọc được (AttributeError)`; `invalid-date`: `(ValueError)`; `python-tag`: `(ConstructorError)`; `invalid-utf8`: `byte 118`; `set-block`: `không phải ánh xạ (set)` | KHÔNG PHẢI LỖI — [5 phép đo](evidence/hunt-reader-errors.json) |

Hướng kiểm thước đo bổ sung: `python -B evidence/review_probes.py mutations` → `PASS (false credit)` khi đưa `RuntimeError: REVIEW_UNRELATED_FAULT`; **LỖI**, finding P2 trên.

## N2: đo nền và sáu hồ sơ thật

Các lệnh này có cwd `cay-kho/`; stdout nguyên vẹn trong log, không chỉ số tổng.

```text
python ../evidence/base-tool.py --root .
TỔNG: 17/17 hồ sơ landed True đạt · 0 miễn trừ · rc=0

python ops/kiem_ho_so_land.py --root .
TỔNG: 23/23 hồ sơ landed True đạt · 0 miễn trừ · rc=0
```

`base-tool.py` lấy bằng `git show 74132ce20cb1f9f74e163717908eca384f672dd0:ops/kiem_ho_so_land.py`. Chạy trên cùng tập hồ sơ; `git diff BASE HEAD -- ops/land` rỗng nên tập dữ liệu này bằng tập ở base.

| Hồ sơ | Base | Head |
|---|---|---|
| pr870-claude-md-bai-hoc-c | BO_QUA | DAT |
| pr889-claude-md-bai-hoc-c | BO_QUA | DAT |
| pr896-claude-md-bai-hoc-c-tro-nguon | BO_QUA | DAT |
| pr924-wp923 | BO_QUA | DAT |
| pr950-wp834 | BO_QUA | DAT |
| pr963-wp943 | BO_QUA | DAT |

[Bản nền](evidence/base-real.json), [head](evidence/head-real.json). Không thay hồ sơ hoặc thêm miễn trừ.

## N3/N4 và giới hạn môi trường

| Lệnh/cổng | Kết quả đo | Trạng thái |
|---|---|---|
| `python -B ops/kiem_ho_so_land_test.py` | `11/11`, rc 0 | passed; không thay bằng chứng đột biến riêng |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`, rc 0 | passed |
| `git diff --check BASE HEAD` | stdout/stderr rỗng, rc 0 | passed |
| `python .claude/dev/ci_dang_ky_test.py` (không `--chay`) | `ĐĂNG KÝ: 28/28`, `TRẠNG THÁI: chan=28 cach_ly=0`, `LAUNCHER WINDOWS: 4/4 hợp đồng`, `RUFF CI: 3/3 hợp đồng`; sau đó `CalledProcessError` ở git commit kho tạm, rc 128; lệnh Python rc 1 | failed trong sandbox, chưa có `TỔNG: ĐẠT` |
| `python scripts/tl.py --selftest` trên clone cùng head/tree | `== tl selftest 1729/1731 ==`, rc 1, 204.187 giây | failed trong sandbox |
| N4: check run `ci.yml` đúng head | Không được cấp receipt check run; assignment không cho dùng mạng | not_measured, KHÔNG ĐO ĐƯỢC |

Hai selftest đỏ: `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`, `r268_l2_trichotomy_theo_trang_thai_object`. Đã chạy riêng bằng `python -B evidence/diagnose_gates.py`: cả hai vẫn False, ba lệnh `git commit` đều rc 128 do dịch vụ ký commit cục bộ báo `socket: operation not permitted`. Toàn bộ `scripts/tl_selftest.py` ở base/head giống nhau (`base_head_selftest_identical=True`); registry và workflow cũng không đổi. Đây là bằng chứng giới hạn hạ tầng, không quy thành regression của hai tệp trong diff. Không tắt ký hoặc đổi quyền để làm cổng xanh.

Clone selftest đầu tiên chưa kế thừa `core.abbrev=7`; phép chẩn đoán đã ghim đúng 7 và tái hiện hai ca đỏ với lỗi ký commit nêu trên. Cây review gốc có `core.abbrev=7` ngay từ đầu. Không tuyên bố đã chạy lại toàn bộ selftest trên base hoặc có kết quả N3 xanh.

Log: [registry](evidence/registry.json), [doctrine](evidence/doctrine.json), [selftest](evidence/selftest.json), [chẩn đoán hai ca](evidence/gates-diagnosis.json). Không chạy bare Ruff hay CI từ xa; các dòng `RUFF CI` chỉ chứng minh hợp đồng workflow mà registry đã kiểm trước khi lỗi.

## Bảng lớp và bàn giao

| Slug lớp | Hạng cao nhất | Biểu hiện | Điều kiện đóng |
|---|---|---|---|
| mutant-crash-counted-as-kill | P2 | Mutant (v) chết vì `.get()` trên str; lỗi RuntimeError vô can cũng được ghi giết ca (iii) | Chấm được sai khác hành vi riêng với lỗi thực thi; mutant (v) ngữ nghĩa chết đúng ca; phản chứng ngoại lệ vô can bị từ chối; chạy lại N1 trên SHA mới |

Lượt 1 nên không có findings lượt trước để đối chiếu. Có 1 lớp/1 finding mở, không có P0/P1 đã phát hiện. Ba mutant sống được báo rõ là giới hạn độ phủ. Cần executor sửa finding, đo lại trên commit mới, và bổ sung bằng chứng N3/N4 ở môi trường có đủ năng lực; reviewer không tự sửa hoặc land bản vá.
