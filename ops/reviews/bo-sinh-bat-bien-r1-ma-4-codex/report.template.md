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

@@FINDINGS@@

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

@@GATES@@

Bốn dòng hợp đồng giữ đủ trong mọi mẫu A/B. Ruff bare lint trên hai tệp base/head là phép riêng; `RUFF CI: 3/3` là pin/probe contract, không thay lint. Commands, cwd, rc, thời gian và hash log ở `VERDICT.json`, `measure.json`, `results-summary.json`. Không có skipped được đổi thành pass.

@@SELFTEST@@

## Thời gian — R3-03

Nguyên văn SPEC §4: “bộ test đợt B không chậm hơn base quá 30 giây, bộ test đợt A không chậm hơn base quá 5 giây. Đo hai vế trong cùng một lệnh, cùng máy, Linux.”

@@TIMES@@

**Đạt trong cả năm cặp đã đo**, vì mọi delta nằm trong trần nguyên văn. Một lệnh `measure.py` chạy tuần tự, cặp 1 base→head, cặp 2 head→base, cặp 3 base→head (A). Không có việc nặng khác của reviewer trong cả 10 mẫu suite và 9 mẫu standalone. Chỉ sau khi chúng hoàn tất mới chạy probes/cổng song song. Giữ mọi mẫu; không dùng trung vị hoặc CPU để thay tiêu chí.

Độ trải cùng vế: A base 10,78s, head 6,47s; B base 14,46s, head 7,60s. Độ trải A lớn hơn +5s nên không thể diễn giải delta âm thành tăng tốc thực hay đo chính xác overhead. Tuy nhiên, không có cặp nào vượt trần trong loạt này; kết luận đóng R3-03 chỉ áp cho các phép đo trên SHA/môi trường đã nêu, không là bảo đảm thống kê cho mọi máy/lượt chạy. Không quan sát được tải ngoài namespace.

@@COST@@

Ca a135/a136/c40 vắng ở base: ghi “không có ca”, không giả một lần chạy `--mot-ca` ở base bằng 0 giây. Mẫu combined sau đó có thể trùng functional gates, chỉ dùng giải thích cache, không dùng xét trần. Thời gian CI/selftest/probes cũng không dùng xét SPEC §4.

## Luật 9, Windows, phạm vi E và phần chưa chạy

Hai module sản phẩm byte-identical với base; SHA-256 trong `static-review.json`. Luật 9 bước 8 trên exact `97ec968` là **not_run** theo assignment. Chỉ chấp nhận handoff bổ sung executor trên đúng SHA/tree, bộ quét ghim, đủ base/head cả A/B, hoàn tất trọn vẹn và **0 mutant GIET ở base sang hạng khác ở head**; giữ riêng nợ SONG/VO_CAN.

Bộ sinh nằm trong test, không đọc module sản phẩm. `_mot` ở bộ quét ghim tạo subprocess mới cho từng mutant, nên cache không sống xuyên mutant; key hàm tách bộ sinh thật/giả. Không thấy đường cache mới che mutant MODULE từ việc đọc mã và probe cache, nhưng điều này không thay full audit còn thiếu.

M3 **required** theo ADR-0060 M3.2: diff thêm `read_text(encoding=...)`, kể cả dòng AST mới. Windows local base/head và Windows CI **not_run**, giao điều phối; Linux không thay Windows.

E1–E5 theo **phạm vi diff** đều `khong`: chỉ hai tệp test, không đổi điều kiện hồ sơ land trong module sản phẩm, không đổi lease/merge authority, không chạm secrets hay LIVE. Checkpoint E2 do hết 4/4 lượt là trạng thái điều phối riêng. M9 `ci-dot-bien-du.yml`, CI/connector và audit uỷ quyền **not_run** trong review offline này.

@@SNAPSHOT@@

**CHƯA ĐỦ ĐIỀU KIỆN MERGE:** R4-01/R4-02 P3 còn mở; selftest nếu còn đỏ cần xử lý evidence đúng phạm vi; Luật 9 exact SHA, Windows, CI/connector/M9 và audit còn thiếu. Không tự miễn, push, merge, land hoặc mở thêm review.

KET_LUAN: changes_requested
