# Review mã bo-sinh-bat-bien r1 g1 — lượt 4 (cuối)

**changes_requested — 2 finding P3 thuộc lớp cũ; không phát hiện P0/P1/P2.** Các biểu hiện cụ thể R3-01/R3-02 đã vá. R3-03 đạt trong năm cặp đo. Lớp chốt miền vẫn `VA_MOT_PHAN`: đổi đồng thời hai nguồn có thể làm mất bộ đối số; thay ASCII mà giữ cardinality vẫn lọt.

HEAD `97ec9686184fdf55dc1736007e6fdcb186122465` · tree `9f8123cc4de66c59968a1b8a3c8d8ef05be0b5eb` · base `a89c83acf998008caecba9084a7d295845bf1976`.

SPEC SHA-256 `bdde0a9bdba79a19fbbc77cfee8311e209b0c91cc16612bb8029167cca186577` khớp tệp và blob Git tại `d22fe11f9bf35517c70333c567481be460173eee`. Revision 1, generation 1, Review Class sensitive. Diff 2 tệp, +274/−9 trong trần 320; `diff --check` rc 0.

Reviewer: `openai_codex / codex_cli / machine/local`; run `d2200510e4904e5dba88cc0a9fa468b5`, session `01a2183b-5d3d-7040-9185-2d23d0c482ab`. CLI 0.172.0 công bố gpt-6-astra/high; model/effort thực phục vụ từng request `KHONG_DO_DUOC`. Linux, Python 3.13.18, Unicode 15.1.0, Ruff 0.15.15, core.abbrev=7. Không gọi mạng/GitHub; authority dùng assignment và snapshot lease, không chứng nhận trạng thái online.

## Bảng lớp và đối chiếu lượt trước

| Lớp | Nhãn | Biểu hiện mở | Mức |
|---|---|---|---|
| nghiem-thu-khong-co-lap-chot-dich | VA_MOT_PHAN | R4-01, R4-02 | P3 |
| nghiem-thu-thoi-gian-chua-dat | DA_VA_THAT | Không | — |

Giữ lịch sử B02 → ded4128 → ef82ed9 → 485387f → 97ec968. Đóng 1/2 lớp cũ, không có lớp mới; không reset slug hay budget. Lượt 4/4 đã hết: điều phối trả checkpoint E2 với kết quả này; không tự mở thêm vòng vá/review hoặc miễn finding.

| Finding cũ | Nhãn | Bằng chứng tự đo |
|---|---|---|
| R3-01 | DA_VA_THAT trong các biểu hiện cũ | `repro_R3.py` rc 0, bốn kết quả con 3/3/3/3, đúng DO. Bỏ từng bộ 1–5 và thay bộ 5 bằng bản sao bộ 2 đều rc 3 DO:a136. Khoảng trống cùng lệch danh tính còn mở dưới R4-01. |
| R3-02 | DA_VA_THAT | Bỏ/đảo `bang(not lech,…)`, `if True`/`if False`/`is None` đều rc 3 đúng meta-case; a131 nguyên vẹn xanh. Hai predicate có hàng riêng trong bảng. |
| R3-03 | DA_VA_THAT trong năm cặp đo | A: 3/3 cặp ≤+5s; B: 2/2 cặp ≤+30s; mọi mẫu rc 0. Công bố độ dao động bên dưới, không suy ra tăng tốc thực. |

Lượt 1–2: 14 phép gỡ riêng đều rc 3 đúng ca; một phép legacy sửa hai vế cũng đỏ nhưng không tính vào 14. Gỡ tổng 158/648 bị c39 bắt. `guard_witnesses.py` xác nhận bản khỏe chạy 648 ô, thiếu ô đỏ trước vòng; bỏ cả guard thì 647 ô thật vẫn chạy. Chốt khác nhau bắt a126:51/52 và a129:35/36; bỏ chốt thì rc 0. Đổi `==`→`>=` bị c40 bắt; chứng nhân a129 có 37 phần tử bị chốt gốc bắt rc 3, nhưng sàn nhận rc 0. Controls cùng đường xanh. Hai phản chứng B02 nguyên gốc vẫn đỏ đúng c36/c37. Raw output ở `probes.json`, `guard-witnesses.json`, `distinct-target.json`, `excess-probe.json`, `b02-targeted.json`.

## R4-01 — P3 — hai nguồn cùng lệch làm mất bộ đối số bắt buộc

Lớp `nghiem-thu-khong-co-lap-chot-dich`; SPEC §2.3.1. Vị trí `ops/gate_output_doi_chieu_test.py:1137`, `:1177`, `:1193`.

Trên clone, đổi đúng hai neo:

```python
_mau_loai_unicode("\r\n", {"Cs"})
# thành
_mau_loai_unicode("\r", {"Cs"})

("\r\n", ("Cs",), 30, ("Cs",))
# thành
("\r", ("Cs",), 30, ("Cs",))
```

`a135` và `a136` đều rc 0, giống controls nguyên vẹn; không có `DO:`. Bộ thứ năm nguyên văn của SPEC đã biến mất. AST đối chiếu với bảng kỳ vọng, nhưng cả hai đều lấy danh tính từ mã có thể cùng đổi; `goi` cũng được sinh từ bảng ấy. Bộ phản chứng `rieng` lại lấy miền từ cùng AST, nên chuyển sang chứng minh bộ mới thay cho bộ bắt buộc.

Đã quét đồng thời hai nguồn cho cả năm bộ: a136 bắt bộ 1/2 (rc 3), còn bộ 3/4/5 vẫn rc 0. Với bộ sinh giả chỉ sai tại bộ thứ năm nguyên văn, bản gốc trả rc 3 `DO:a135:…so_phan_tu/cuoi_ngoai_bmp`; bản cùng lệch trả rc 0 và trace không còn lời gọi `("\r\n", ("Cs",))`. Controls khỏe đều rc 0. Xem `ast-review.json`, `co-drift-witness.json`.

Đây là đột biến ngoài tập toán tử cố định nhưng **trong miền đặc tả**, đúng yêu cầu kiểm đổi dữ liệu ở hai nơi. Không suy thành lỗi module sản phẩm ở HEAD nguyên vẹn.

Phép đóng: ghim danh tính năm bộ từ SPEC bằng nguồn kỳ vọng độc lập với các caller và bảng đang bị đột biến; tạo phản chứng riêng theo miền cố định này và đối chiếu cả AST lẫn các bộ đã kiểm với nó. Thêm phản chứng đổi đồng thời caller + kỳ vọng: bộ sinh chỉ sai tại bộ nguyên văn phải vẫn bị bắt. Ước **15–25 dòng thêm**, hoặc ít hơn nếu thay cơ chế AST bằng miền cố định. Rủi ro sửa: tăng trùng lặp hằng / chi phí meta-test; giữ kiểm mỗi bộ, các controls và đo lại thời gian. Nếu miễn: hồi quy đồng thời caller/kỳ vọng có thể bỏ hẳn một bộ đối số, còn bộ test vẫn tuyên bố đã kiểm đủ năm.

## R4-02 — P3 — tổng 158 không bảo vệ đủ 128 giá trị ASCII

Lớp `nghiem-thu-khong-co-lap-chot-dich`; SPEC §2.1.1. Vị trí `ops/land_evidence_nguon_test.py:914`, `:924–928`, `c39`.

```python
vu_tru = [*map(chr, range(128)), ...]
# thành (neo/thay đầy đủ trong domain-review4.json)
vu_tru = [chr(0x81), *map(chr, range(1, 128)), ...]
```

Mất U+0000, thêm U+0081, vẫn 158 giá trị khác nhau và 648 ô. `c37`, `c39`, `c40` đều rc 0. Biến thể mất DEL U+007F (`range(127)` rồi U+0081) cũng làm `c37/c39` rc 0. Controls nguyên vẹn cùng đường xanh. Chốt chỉ kiểm category ở `vu_tru[128:]`, không kiểm danh tính 128 phần tử đầu. Các phép range±1/cắt trong bảng hiện tại đổi cả cardinality nên chưa cô lập nghĩa vụ này.

Đây là **mất giá trị miền bắt buộc**, khác thay một ô cấu trúc bằng ô mới được §8 loại khỏi phạm vi. Nếu miễn: bốn ô tương ứng NUL hoặc DEL tại các vị trí văn bản tự do biến mất mà chốt vẫn nhận đủ miền và đủ 648 ô.

Phép đóng: kiểm tập ASCII là chính xác U+0000…U+007F trước vòng ô; thêm phản chứng thay NUL/DEL bằng ký tự ngoài ASCII mà giữ cardinality/uniqueness, đòi rc 3 `DO:c37:` và 0 ô, bản nguyên vẹn rc 0/648 ô. Ước **8–14 dòng thêm**. Rủi ro sửa: không vô tình đòi thứ tự ASCII nếu SPEC chỉ đòi tập; đảm bảo guard mới cũng có phản chứng gỡ riêng.

Lệnh tái lập chung (clone tạm mới mỗi lần, chỉ dưới work/):

```bash
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/../work/tmp" python3 -B ../work/repro_R4.py
```

Đã chạy rc 0 của script; tám kết quả con (bốn controls, bốn mutant) đều rc 0. `domain_review4.py` đo thêm DEL và các mutant ±2/nhánh/aggregation; raw rc/stdout/stderr ở `domain-review4.json` và `repro-R4.json`.


## AST, inventory và miền ngoài tập toán tử

Inventory reviewer theo từng nghĩa vụ ở `obligations.md`: 128 giá trị ASCII, 29 category, năm bộ đối số, tám số đếm, P1–P7. Số ô bảng toán tử không phải mẫu số độ phủ nghĩa vụ. So với `nghia-vu.md`: executor gộp ASCII vào tổng/khác nhau nhưng chưa kiểm replacement giữ cardinality; danh tính miền AST/bảng chưa được ghim độc lập khi cả hai cùng đổi. Đây là hai nghĩa vụ không có phản chứng đỏ đúng ca.

`_mien_doi_so()` đọc **tệp trên đĩa** bằng `Path(__file__).read_text`, không dùng `inspect` hay hàm đã patch trong bộ nhớ. Nó chỉ nhận direct call theo tên; ghép positional arguments với keyword values, không bind theo tên keyword. `goi` so với AST và đòi len=5; `BO_SINH_MONG` so gián tiếp qua `goi`. Lệch riêng caller, bảng kỳ vọng hoặc vòng đã kiểm đều bị bắt; hai nguồn cùng lệch thiếu chuẩn danh tính từ SPEC.

| Probe | a135 / a136 | Diễn giải |
|---|---|---|
| Lọc thêm a129, đổi prefix thành b, trả tập rỗng | 3/3 | Miền thiếu/rỗng không làm xanh sai |
| Alias hoặc partial tại bộ 5 | 3/3 | Bỏ sót call → thiếu miền → đỏ |
| `**kwargs`, hằng đặt tên, đảo thứ tự keyword | 4/4 | Fail-close bằng lỗi AST/binding; không tính là kill đúng chốt |
| Không đọc được tệp hoặc AST lỗi cú pháp | 4/4 | Không xanh sai; không giả thành rc 3 |
| Đổi tên hàm nhưng không đổi detector | 3/3 | Không tìm thấy direct call |
| Đổi tên đồng bộ; bỏ loại trừ a135/a136; trả hằng đúng năm bộ | 0/0 | Không mất giá trị bắt buộc trong miền hiện hành; không là finding |
| Cùng đổi hai nguồn ở bộ 1/2 | 0/3 | Meta-test bắt nhờ thông báo kỳ vọng cố định |
| Cùng đổi hai nguồn ở bộ 3/4/5 | 0/0 | R4-01 |

Các trường hợp rc 4 được khai rõ là lỗi vô can, không được tính “giết”. HEAD hiện dùng literal và đọc được nguồn; SPEC không đòi hỗ trợ mọi cách refactor kể trên, nên không nâng chúng thành finding riêng.

Đã lấy hơn 8 mutant độc lập: drop/invert, lát cắt bỏ bộ, đổi chỉ số cuối, tráo hai phần tử, hằng +2/−2, thay ASCII giữ cardinality, đổi đồng thời dữ liệu ở hai nguồn. Raw neo/thay và rc/stdout/stderr nằm ở `ast-review.json`, `domain-review4.json`, `probes.json`. Một ô cấu trúc khác không trùng vẫn thuộc giới hạn §8; không đòi đệ quy vô hạn cho chính các meta-assertion. Các mutant sống chỉ được nâng thành finding khi mất giá trị §2–3 bắt buộc.

## Bảng 140 ô và tín dụng thật

Chạy lại công cụ nguyên vẹn, rc 0: **136 GIET, 4 TUONG_DUONG, 0 SONG, 0 HONG**; baseline 4/4 xanh, worker sạch. **140/140 ô khớp tất cả trường, 0 lệch**. Cả 140 neo duy nhất, bytes thực đổi, AST hợp lệ. Bốn ô tương đương giữ chứng minh `|set(x)|≤|x|` và phần tử cuối ngoài BMP suy ra `n−bmp≥1`.

Công cụ đòi rc 3 và stdout bắt đầu bằng đúng `DO:<meta-case>:`. Audit độc lập:

| Đầu vào audit | Phân hạng | rc ca |
|---|---|---:|
| Chỉ sửa chú thích | SONG | 0 |
| SyntaxError | HONG | 1 |
| TypeError ở a136 | HONG | 4 |
| rc 3 nhưng sai tên DO | HONG | 3 |
| TypeError ở a135 | GIET do a136 phát hiện sai hợp đồng | 3 ở a136, 4 ở a135 |

Chạy `main()` với bảng một mutant SONG hoặc HONG đều rc 1. Phải phân biệt hai tầng: inner rc 4 bị meta-test bắt không có nghĩa inner case đã đỏ đúng chốt nghiệp vụ. Bảng thật có `bool(ra)/bo` gây inner IndexError; không nhận tín dụng sai tầng. Công cụ bỏ stderr/cắt `dong` còn 400 ký tự; các probe độc lập lưu stdout/stderr đầy đủ.

Lượt bảng đầu bị script nháp của reviewer tên `queue.py` che module chuẩn. Đã đổi thành `probe_tasks.py`, chạy lại công cụ không sửa, rc 0. Giữ `table-first-attempt.log`; không tính lỗi setup này là lỗi ứng viên. Bằng chứng: `table-rerun-receipt.json`, `tool-review4.json`, `table/bang.json`.

Trace độc lập trên HEAD: c39 có 39 âm + 3 dương; c40 có 9 âm + 4 dương ca đích và 13 lượt A xanh; a136 có 20 âm + 3 dương. Tổng **68 âm đúng rc 3/DO, 10 control đích xanh, thêm 13 lượt A xanh, 0 rc 4**. c38 thêm 24/24 âm đúng DO. Trong c39, ba control chạy 648 ô, 39 âm đều 0 ô. Con số 14 xanh của executor gồm 4 lượt A qua `nap_sua`; profiler còn thấy 9 lượt qua `nap_a`, không có kết quả lệch trong cùng phạm vi.

## Nhớ đệm

Cache bật/tắt cho **25/25 kết quả rc/DO giống nhau**. Với 1.000 lambda, 1.000 function vẫn được key giữ tham chiếu: không có tái dùng `id()`. Key chứa chính đối tượng hàm và đối số; lambda mỗi biến thể khác đối tượng, `patch.dict` không làm trùng key với hàm thật. Tuple kết quả bất biến; sửa list nguồn không làm bẩn bản đã cache; đối số khác tách key.

Chạy riêng `--mot-ca a135`, `a136`, `c40` đều rc 0. Không suy kết luận này thành bảo đảm cho mọi callable có custom equality/hash hoặc phần tử mutable ngoài miền string hiện tại. Xem `cache-review4.json` và `new-code-cost.json`.

## Cổng tự chạy

| Phép đo | rc | Bằng chứng dương / trạng thái |
|---|---:|---|
| base-A-1 | 0 | CA: 51/51 dat; DOT BIEN: 158/158 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| head-A-1 | 0 | CA: 53/53 dat; DOT BIEN: 158/158 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| base-B-1 | 0 | CA: 38/38 dat; DOT BIEN: 145/145 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| head-B-1 | 0 | CA: 40/40 dat; DOT BIEN: 145/145 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| head-land | 0 | land_evidence_nguon: 153 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 178; TỔNG: ĐẠT |
| head-ci | 0 | RUFF CI: 3/3 hợp đồng; PHẢN CHỨNG: 1677/1677 đỏ đúng; TỔNG: ĐẠT |
| base-selftest | 1 | == tl selftest 1773/1789 == |
| head-selftest | 1 | == tl selftest 1773/1789 == |
| base-ruff | 0 | All checks passed! |
| head-ruff | 0 | All checks passed! |

Bốn dòng hợp đồng giữ đủ trong mọi mẫu A/B. Ruff bare lint trên hai tệp base/head là phép riêng; `RUFF CI: 3/3` là pin/probe contract, không thay lint. Commands, cwd, rc, thời gian và hash log ở `VERDICT.json`, `measure.json`, `results-summary.json`. Không có skipped được đổi thành pass.

Selftest **failed**; tập ID đỏ base/head giống nhau: True. Delta mới bằng 0 không được đổi thành N/N passed. Không sửa credential/signer/tổ tiên `/tmp` để làm xanh.

Các ID đỏ ở cả hai vế:

- r973_bootstrap_khong_kiem_khoa
- r973_bootstrap_ba_trang_thai
- r973_bootstrap_require_agent_creds
- r973_bootstrap_giu_auth_json_moi_hon
- r973_bootstrap_last_refresh_hong_khong_pha
- r973_bootstrap_auth_json_nguyen_tu
- r973_bootstrap_sai_dinh_dang_khong_nap
- r973_bootstrap_khong_export_khong_ghi_gemini
- r226_nguong_l2_troi_theo_abbrev_va_ci_ghim
- r268_l2_trichotomy_theo_trang_thai_object
- wp433_gws_cred_dich_ngoai_kho
- wp433_gws_cred_dich_ngoai_kho_b
- wp433_gws_cred_no
- wp433_gws_cred_win_reparse
- wp433_nlm_gws_dich_ngoai_kho
- wp727_tl_gws_refresh

## Thời gian — R3-03

Nguyên văn SPEC §4: “bộ test đợt B không chậm hơn base quá 30 giây, bộ test đợt A không chậm hơn base quá 5 giây. Đo hai vế trong cùng một lệnh, cùng máy, Linux.”

| Bộ | Cặp | Base (s) | Head (s) | Delta (s) | Trần |
|---|---:|---:|---:|---:|---:|
| A | 1 | 338.30 | 337.75 | -0.54 | +5 |
| A | 2 | 349.08 | 344.22 | -4.86 | +5 |
| A | 3 | 343.68 | 339.96 | -3.73 | +5 |
| B | 1 | 303.85 | 311.42 | +7.57 | +30 |
| B | 2 | 318.31 | 319.01 | +0.71 | +30 |

**Đạt trong cả năm cặp đã đo**, vì mọi delta nằm trong trần nguyên văn. Một lệnh `measure.py` chạy tuần tự, cặp 1 base→head, cặp 2 head→base, cặp 3 base→head (A). Không có việc nặng khác của reviewer trong cả 10 mẫu suite và 9 mẫu standalone. Chỉ sau khi chúng hoàn tất mới chạy probes/cổng song song. Giữ mọi mẫu; không dùng trung vị hoặc CPU để thay tiêu chí.

Độ trải cùng vế: A base 10,78s, head 6,47s; B base 14,46s, head 7,60s. Độ trải A lớn hơn +5s nên không thể diễn giải delta âm thành tăng tốc thực hay đo chính xác overhead. Tuy nhiên, không có cặp nào vượt trần trong loạt này; kết luận đóng R3-03 chỉ áp cho các phép đo trên SHA/môi trường đã nêu, không là bảo đảm thống kê cho mọi máy/lượt chạy. Không quan sát được tải ngoài namespace.

Chạy riêng (ba mẫu, đều rc 0): a135: 0.869s, 0.916s, 0.912s; a136: 1.289s, 1.371s, 1.227s; c40: 13.000s, 12.717s, 14.121s. a135+a136 cùng tiến trình, không profiler: 1.093s, 1.052s, 1.234s.

Ca a135/a136/c40 vắng ở base: ghi “không có ca”, không giả một lần chạy `--mot-ca` ở base bằng 0 giây. Mẫu combined sau đó có thể trùng functional gates, chỉ dùng giải thích cache, không dùng xét trần. Thời gian CI/selftest/probes cũng không dùng xét SPEC §4.

## Luật 9, Windows, phạm vi E và phần chưa chạy

Hai module sản phẩm byte-identical với base; SHA-256 trong `static-review.json`. Luật 9 bước 8 trên exact `97ec968` là **not_run** theo assignment. Chỉ chấp nhận handoff bổ sung executor trên đúng SHA/tree, bộ quét ghim, đủ base/head cả A/B, hoàn tất trọn vẹn và **0 mutant GIET ở base sang hạng khác ở head**; giữ riêng nợ SONG/VO_CAN.

Bộ sinh nằm trong test, không đọc module sản phẩm. `_mot` ở bộ quét ghim tạo subprocess mới cho từng mutant, nên cache không sống xuyên mutant; key hàm tách bộ sinh thật/giả. Không thấy đường cache mới che mutant MODULE từ việc đọc mã và probe cache, nhưng điều này không thay full audit còn thiếu.

M3 **required** theo ADR-0060 M3.2: diff thêm `read_text(encoding=...)`, kể cả dòng AST mới. Windows local base/head và Windows CI **not_run**, giao điều phối; Linux không thay Windows.

E1–E5 theo **phạm vi diff** đều `khong`: chỉ hai tệp test, không đổi điều kiện hồ sơ land trong module sản phẩm, không đổi lease/merge authority, không chạm secrets hay LIVE. Checkpoint E2 do hết 4/4 lượt là trạng thái điều phối riêng. M9 `ci-dot-bien-du.yml`, CI/connector và audit uỷ quyền **not_run** trong review offline này.

Snapshot đầu/cuối: 18703→18703 tệp, 0 delta; HEAD/tree không đổi, tracked/untracked/index sạch; ignored `.codex/` có sẵn. Sandbox `workspace-write`, không phải mount read-only. Snapshot chỉ chứng minh hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Repo nguồn ngoài checkout được cấp không nằm trong phạm vi quan sát. Mọi clone/log/đột biến nằm dưới `work/`.

**CHƯA ĐỦ ĐIỀU KIỆN MERGE:** R4-01/R4-02 P3 còn mở; selftest nếu còn đỏ cần xử lý evidence đúng phạm vi; Luật 9 exact SHA, Windows, CI/connector/M9 và audit còn thiếu. Không tự miễn, push, merge, land hoặc mở thêm review.

Validator `kiem_verdict_lop.py --vong 4`: rc 0, `HOP_LE (§8.3): 2 finding, 2 lop`; stdout ở `kiem_verdict.txt`.

KET_LUAN: changes_requested
