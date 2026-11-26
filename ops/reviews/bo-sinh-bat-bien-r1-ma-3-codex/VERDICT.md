# Review mã bo-sinh-bat-bien r1 g1 — lượt 3

**changes_requested — 3 finding P3 thuộc 2 lớp (1 cũ, 1 mới); không phát hiện P0/P1/P2.** R1-01, R1-02, R2-01 đã vá thật. Bảng 108 ô tái lập hoàn toàn nhưng chưa đủ đóng lớp: bỏ bộ đối số thứ tư/thứ năm vẫn lọt, và inventory bỏ sót hai predicate. Hai cặp thời gian A đều vượt trần +5s (R3-03).

HEAD `485387fb1e0e6e49837623ba9df7843d5dca782f` · tree `dd18e43c2781f3ec0d227832083c5f46d40a14cd` · base `a89c83acf998008caecba9084a7d295845bf1976`.
Spec SHA-256 `bdde0a9bdba79a19fbbc77cfee8311e209b0c91cc16612bb8029167cca186577`; Git blob `a47f5bfb9648181f489a20d59c326caf300ab1ef` tại `d22fe11f9bf35517c70333c567481be460173eee` khớp. Revision 1, generation 1, Review Class sensitive. Diff 2 tệp, +235/−9; trong trần 320.

Reviewer: openai_codex / codex_cli / machine/local; run `90b98ca07a414787926b0d8c5fcb2812`, session `01a21757-d21e-7e22-b138-9e61f256d588`. CLI 0.172.0 công bố gpt-6-astra/high; model/effort từng request KHONG_DO_DUOC. Linux, Python 3.13.18, Unicode 15.1.0, PyYAML 6.0.3, Ruff 0.15.15, core.abbrev=7. Sandbox workspace-write; kho được review giữ chỉ đọc, mọi clone/đột biến/log dưới work/.

## Bảng lớp và đối chiếu lượt trước

| Lớp | Trạng thái | Biểu hiện | Cao nhất mở |
|---|---|---|---|
| nghiem-thu-khong-co-lap-chot-dich | VA_MOT_PHAN | R1-01/R1-02/R2-01 đóng; R3-01/R3-02 mở | P3 |
| nghiem-thu-thoi-gian-chua-dat | MỚI | R3-03: cả hai cặp A vượt +5s | P3 |

Giữ nguyên lịch sử B02 → lượt 1 ded4128 → lượt 2 ef82ed9 → lượt 3 485387f. Tỷ lệ đóng lớp của chuyển tiếp này 0/1; không đổi slug, không tự miễn P3. Cần checkpoint xét lại phần còn thiếu theo §8.3/§12; không tự mở thêm vòng vá hay ngân sách.

| Finding cũ | Nhãn | Bằng chứng tự đo |
|---|---|---|
| R1-01 | DA_VA_THAT | Gỡ riêng tổng158/648 làm c39 rc3; c37 khỏe chạy648 ô, thiếu ô đỏ trước vòng; gỡ chốt648 thì647 ô vẫn chạy. probes.json, guard-witnesses.json. |
| R1-02 | DA_VA_THAT | Đúng cặp nguồn/thay a129:35/36 khác nhau rc3 DO:c36; a126:51/52. Bỏ chốt khác nhau thì cả hai rc0. distinct-target.json. |
| R2-01 | DA_VA_THAT | Đổi ==→>= làm c40 rc3 DO:c40 ở thêm bản sao a126. Nhân chứng a12937 phần tử: chốt gốc rc3, sàn rc0; controls nguyên vẹn rc0. excess-probe.json. |

14 phép gỡ riêng của lịch sử đều rc3 đúng ca; một phép legacy sửa hai vế cũng đỏ nhưng không tính là phép gỡ độc lập. Hai B02 nguyên gốc: bỏ Mn làm c36 báo1723/1733 và c37 báo157/158 thiếuMn; bỏ lời gọi cấu trúc a129 làm c36 báo35/36, tất cả rc3 đúng DO. Lệnh và nguyên văn từng dòng nằm trong probes.json, b02-targeted.json, guard-witnesses.json.

## R3-01 — P3: mất miền đối số bắt buộc mà a136 vẫn xanh

Vị trí: `ops/gate_output_doi_chieu_test.py:1143` và ca a136 từ dòng1160. Căn cứ **§2.3.1: kiểm với đúng năm bộ đối số**; đây là giá trị miền bắt buộc, dù toán tử lát cắt nằm ngoài tập cố định.

Hai mutant trên clone riêng:

```python
for cam, bo_loai, so, vang in BO_SINH_MONG:
# lần lượt thay bằng
for cam, bo_loai, so, vang in BO_SINH_MONG[:3] + BO_SINH_MONG[4:]:
for cam, bo_loai, so, vang in BO_SINH_MONG[:-1]:
```

Cả hai cho a136 rc0. Mutant bỏ bộ5 còn cho c38/c39/c40/a136 đều rc0 (`fifth-allmeta.json`). Probe sửa trực tiếp hằng cũng cho cùng kết quả: xóa bộ4, xóa bộ5, hoặc thay bộ5 bằng bản sao bộ2 (giữ đủ5 hàng) đều a136 rc0; xóa bộ1–3 thì a136 rc3 (`data-domain.json`).

| Bộ sinh giả chỉ sai tại | a135 gốc | a135 thiếu bộ đó | Control khỏe |
|---|---|---|---|
| bộ4: cam="", bo_loai=() | rc3 DO:a135…, so_phan_tu/cuoi_ngoai_bmp | rc0 | rc0 ở cả hai vế |
| bộ5: cam="\r\n", bo_loai=("Cs",) | rc3 DO:a135…, so_phan_tu/cuoi_ngoai_bmp | rc0 | rc0 ở cả hai vế |

Bộ sinh giả chỉ bỏ phần tử ngoài BMP ở đúng bộ chỉ định; các bộ khác giữ nguyên. Trace ghi chính xác danh sách đối số đã gọi, tránh suy từ tổng suite. Xem fourth-witness.json, fifth-witness.json. Đây là lỗ bảo vệ hồi quy của test mới, không khẳng định HEAD nguyên vẹn đang thiếu bộ đối số hoặc sản phẩm có lỗi, nên P3.

Gợi ý: thêm phản chứng sai riêng tại từng bộ đối số bắt buộc, đặc biệt bộ4 và bộ5; chốt danh tính miền độc lập, không chỉ đếm5 từ chính BO_SINH_MONG. Phép đóng: lần lượt bỏ/lặp/thay từng bộ phải làm a136 rc3 đúng DO, healthy controls cùng đường xanh; giữ các probe cũ.

## R3-02 — P3: inventory bảng chưa đủ predicate

`bang(not lech, ...)` cuối kiem_bo_sinh (dòng1150) vắng phép đột biến riêng. Hàng a135.gom ghi cả nó và `if not dat`, nhưng mã M chỉ thay `if not dat`. Hai phép đảo không tương đương khi danh sách có cả mệnh đề đạt và lệch. Probe độc lập bỏ/đảo bang cuối đều a136 rc3 đúng DO; cần đưa bằng chứng này vào hàng riêng, không dùng tên hàng thay phép đo.

`if tru is not None` ở c36 (dòng899) kích hoạt hai chốt bắt buộc §2.2.2 nên không thể loại chỉ vì đó là if. Đảo thành `is None` hoặc bỏ bằng `if False` đều c40 rc3 ở Mn→Mc. Đổi thành `if True` lại cho c40 rc0, trong khi c36 với riêng a131 rc4 TypeError; xác nhận đường a131 chưa được c40 bảo vệ. Xem independent.json, exclusions-probe.json. Không gọi rc4 là giết đúng chốt.

Gợi ý: map từng predicate chi phối acceptance tới hàng/toán tử thật; tách aggregation cuối a135 và nhánh chọn miền c36, phân biệt biến thể non-equivalent/HONG với tương đương. Các chốt đã bị ca hiện có bắt không cần sửa chỉ để làm bảng đẹp; bổ sung công cụ/bằng chứng đúng phạm vi. Phép đóng lớp phải gồm inventory nghĩa vụ §2–3, cả miền đối số và ma trận predicate.

Lệnh tái lập hai finding, luôn tạo clone tạm mới:

```bash
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/../work/tmp" python3 -B ../work/repro_R3.py
```

Đã chạy rc0; bốn kết quả con lần lượt 0,0,3,3 (`repro-R3.json`). Nguyên văn neo/thay và stdout/stderr có trong independent.json. Đây là bằng chứng reviewer, không phải patch vào branch Executor.

## Công cụ bảng, độ đủ và tương đương

Đã băm lại công cụ và bang.md đúng hồ sơ. Chạy `python3 -B bang_toan_tu.py --goc work/head --ra work/table --song-song 3`: rc0; baseline4/4 xanh;104GIET,4TUONG_DUONG,0SONG,0HONG; worker sạch. **108/108 ô khớp hạng/ca/rc, 0 lệch.** Neo108/108 duy nhất, bytes thực đổi, AST hợp lệ. 145 ô không áp dụng đã được xét và ghi từng ô ở na-audit.json. Inventory độc lập và lý do theo từng nhóm ở coverage-review.md, clause-inventory.json.

Phân hạng GIET đòi rc3 và stdout bắt đầu đúng DO của ca phản chứng đang gọi. Đã thử: sửa chú thích→SONG rc0; SyntaxError→HONG rc1; TypeError ở a136→HONG rc4; rc3 sai tên→HONG. Chạy main với bảng một mutant SONG hoặc HONG đều trả rc1. Mỗi worker một luồng, mỗi ca tiến trình mới -B; khôi phục trong finally; không dùng bytecode cũ trên clone mới.

Giới hạn quan trọng: phân hạng ở **ca phản chứng bên ngoài**. TypeError cố ý trong a135 làm a136 ném chốt rc3 nên công cụ gọi GIET. Trong bảng thật, bool(ra)/bo tạo IndexError ở a135 cho bộ sinh rỗng rồi a136 bắt sai hợp đồng rc3. Đó là kiểm bảo vệ tín hiệu của mục tiêu, không được kể thành bằng chứng a135 đã đỏ đúng chốt ở mutant ấy. Bản nguyên vẹn được trace riêng và không có rc4. Công cụ bỏ stderr/cắt dong400 ký tự; không phải bộ phân biệt mọi lỗi vô can ở mọi tầng. Chi tiết tool-method.md và tool-audit.json.

Bốn ô tương đương: |set(x)|≤|x| chứng minh c37.tong/le, c37.khac_nhau/ge và a135.lap_category/le; với cuối ngoài BMP thì n−bmp≥1, nên a135.cuoi.duy_nhat/le tương đương ==1. Kiểm hữu hạn độc lập cardinality 0..164/0..39 đều đạt; suy luận bất đẳng thức là căn cứ tổng quát (equivalence-checks.json).

## Mẫu độc lập và ba loại ngoài bảng

Đã tự soạn hơn8 mutant, có phép thuộc tập cố định và ngoài tập. Mỗi neo/thay, rc, stdout/stderr nằm trong independent.json. Bỏ/đảo bang cuối; đảo/bỏ nhánh c36; biênASCII+1; ngưỡngASCII+2; đổi chỉ số cuối; số khác nhau−2; chỉ chạy bộ đối số đầu đều bị ca phù hợp bắt. Bỏ bộ4/5 là R3-01. Các mutant sống còn lại được xử lý riêng:

- Đảo hai vế != của c37 tương đương trên int/bool.
- Thay ô cấu trúc a129 bằng ô mới không trùng: a129 và c36 rc0; đúng giới hạn §8, không là finding.
- Bỏ assertion của c40: c40 rc0; dev-side bảng với chốt category bị bỏ trở thành SONG. §3 không đòi hồi quy vô hạn của chính meta-assertions; ghi giới hạn này, không thêm nghĩa vụ đệ quy.
- Bỏ deepcopy cache: c40 rc0 nhưng chưa chứng minh mất giá trị miền §2–3; code hiện tại có deepcopy và probe riêng kiểm tính không nhiễm. Không nâng mọi mutant sống ngoài tập thành finding.

Nhánh tru: trong miền §2.2.2, R3-02. Các phép so của chính c39/c40/a136: giới hạn tầng meta-test như trên. Hằng kỳ vọng: giá trị phải theo spec; baseline bắt nhiều thay đổi số, nhưng không bắt mất/lặp bộ đối số cuối, nên không được blanket-exclude mọi thay đổi dữ liệu (R3-01).

## Phản chứng, cache và tín dụng thật

c39:39 đỏ+3 xanh; c40:9 đỏ+3 xanh ở c36, thêm12 lượt ca A xanh; a136:10 đỏ+2 xanh. Tổng58 đích đỏ,8 control đích xanh;12 lượt A bổ sung xanh,0 rc4. c38 giữ24/24 âm đúng chốt. Executor ghi12 xanh vì wrapper chỉ thu4/12 lượt A tạo qua nap_sua; profiler thu thêm8 lượt nap_a. Không có khác biệt ở58 phản chứng đích. Trace line-event1296 không là số ô: bộ đếm append xác nhận648 ở3 control và0 ở39 âm.

Bản sao nguyên vẹn nap_sua có inventory, globals được so, Python code equality và toàn bộ thuộc tính code chuẩn hóa khớp; mutant mất ô đổi đúng mã c37. Raw marshal byte khác ở một số ca không dùng làm bằng chứng ngữ nghĩa. Healthy U+10000 và bản sao nguyên vẹn thực đi cùng đường kiểm của phản chứng. guard-witnesses dùng ky8 thật; c39 chỉ đếm ô nên không nhận là kiểm consumer.

Cache YAML bật/tắt: **8955** đầu vào L8 cùng thứ tự, cùng byte SHA-256, mọi rc/DO và mọi kết quả ca A đều trùng. c36+c40 đều rc0; cache bật3619 khóa, tắt0. Chạy riêng --mot-ca c36 rc0; c40 riêng rc0. Hai tệp một byte khác nhau cho hai lần parse/kết quả khác nhau; sửa bản trả về không nhiễm lần đọc sau; tên hàm và kwargs phân tách. Warm c36→c40 không nhận dữ liệu nguyên vẹn thay mutant. a136 bật/tắt cùng trace, tuple bất biến và cache mới mỗi lời gọi; hai cam khác một byte có hai khóa riêng.

Giới hạn cache: key không gắn kiểu cho nhánh pickle; safe_dump(dict) và safe_dump(bytes bằng pickle của dict) có thể trùng khóa trong probe nhân tạo. Đường c36/c40 hiện tại dump dict, không dùng kiểu bytes đó; không có sai khác trong8955 đầu vào thực. Ghi limits, không suy đây là hồi quy hiện tại hoặc cache dùng chung an toàn cho mọi kiểu.

## Các cổng và R3-03 — P3: nghiệm thu thời gian A chưa đạt

| Lượt | rc | Trạng thái / bằng chứng dương |
|---|---:|---|
| base-B | 0 | passed: CA: 38/38 dat; DOT BIEN: 145/145 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| head-B | 0 | passed: CA: 40/40 dat; DOT BIEN: 145/145 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| base-A | 0 | passed: CA: 51/51 dat; DOT BIEN: 158/158 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| head-A | 0 | passed: CA: 53/53 dat; DOT BIEN: 158/158 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| head-land | 0 | passed: TỔNG: ĐẠT |
| head-ci | 0 | passed: RUFF CI: 3/3 hợp đồng; PHẢN CHỨNG: 1677/1677 đỏ đúng; TỔNG: ĐẠT |
| base-selftest | 1 | failed: == tl selftest 1773/1789 == |
| head-selftest | 1 | failed: == tl selftest 1773/1789 == |
| base-ruff | 0 | passed: All checks passed! |
| head-ruff | 0 | passed: All checks passed! |

Lệnh/cwd/giây/hash log đầy đủ trong VERDICT.json và gates.json. Diff --check rc0; numstat 2 tệp +235−9. Ruff bare lint base/head rc0 delta0; contract pin/probe RUFF CI3/3 thuộc cổng ci riêng. Không có skipped được đổi thành pass.

| Bộ | Mẫu | Base (s) | Head (s) | Delta (s) | Trần | Quan sát |
|---|---:|---:|---:|---:|---:|---|
| B | 1 | 310.31 | 314.65 | +4.34 | +30 | trong trần |
| B | 2 | 339.09 | 327.38 | -11.71 | +30 | trong trần |
| A | 1 | 356.60 | 365.82 | +9.22 | +5 | **vượt trần** |
| A | 2 | 341.80 | 355.49 | +13.69 | +5 | **vượt trần** |

Biến động giữa hai mẫu của cùng vế: B: base 28.78s, head 12.73s; A: base 14.80s, head 10.34s. Đây là độ trải của hai quan sát, không phải khoảng tin cậy thống kê.

Mẫu1 chạy base→head; mẫu2 head→base, tuần tự xen kẽ, không probe nặng của reviewer chạy cùng lúc. Cả hai cặp A đều vượt5s: +9,22s và +13,69s. Đây là R3-03 theo §4/§5, một lớp mới tách khỏi lớp predicate. Chưa cô lập được toàn delta do mã hay do nhiễu; không chọn mẫu xanh hoặc lấy rc0 suite thay chứng nhận hiệu năng. Đóng finding bằng đo chi phí/nhiễu, tối ưu nếu cần và nộp bằng chứng base/head ổn định đạt trần trên exactSHA, công bố mọi mẫu. Hai mẫu cho biết biến động ở môi trường này; tải ngoài namespace chưa đo. Chưa đủ căn cứ khẳng định luôn đạt trần A hoặc tự miễn điều kiện §4.

Lệnh tái lập R3-03 từ `repo/`, chạy lần lượt; các clone `work/base` và `work/head` đã được giữ lại:

```bash
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/../work/tmp" python3 -B ../work/run_gates.py
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/../work/tmp" python3 -B ../work/timing2.py
```

## Selftest, Luật9, M3 và phạm vi E

Selftest base và head đều rc1, 1773/1789; cùng 16 ID đỏ, delta0 (selftest-delta.json). Giữ failed, không biến delta0 thành N/N passed. Không lặp chẩn đoán nhân quả từng lỗi môi trường, không sửa /tmp/.git, signer hay credential để làm xanh.

Hai module sản phẩm byte-identical base: product-identical.json. Luật9 bước8 exact485387f: **not_run**, theo chỉ thị không chạy lại4 lượt. Chỉ chấp nhận handoff bổ sung của executor trên đúng SHA/tree với đủ base/head cho cả A/B, công cụ/kho ghim, hoàn tất rõ ràng và0 mutant GIET-base→hạng khác-head; giữ riêng nợ SONG/VO_CAN. _mot (quet_dot_bien.py:263) tạo tiến trình mới cho mỗi mutant; _CHAY_CA chỉ chia cache giữa các ca trong cùng mutant. NHO_YAML không sống qua ranh giới mutant; main/chay_con của test cũng dùng subprocess mới. Điều này không thay bằng chứng quét còn thiếu.

M3 **required**: dòng thêm read_text(encoding="utf-8"), ADR-0060 bước2. Windows local base/head và Windows CI not_run, giao điều phối; Linux không thay Windows. E1–E5 **khong**: chỉ test, không thay điều kiện land trong module sản phẩm, lease/merge gate, quyền hay LIVE. M9 full_mutant_audit trên exacthead vẫn cần.

CHƯA ĐỦ ĐIỀU KIỆN MERGE: R3-01/R3-02/R3-03 P3 mở; hiệu năng A không đạt hai cặp đo; Luật9 exactSHA, Windows, CI/connector/M9 và audit uỷ quyền chưa được review offline này chứng nhận. Không push/merge/land.

Snapshot đầu/cuối: HEAD/tree không đổi, 18703 tệp quan sát được có cùng SHA-256, status tracked/untracked sạch (ignored .codex có sẵn). Snapshot chỉ chứng minh hai mốc; repo nguồn ngoài checkout được cấp không nằm trong phạm vi quan sát. Mọi bằng chứng ở work/, không sửa branch Executor.

KET_LUAN: changes_requested
