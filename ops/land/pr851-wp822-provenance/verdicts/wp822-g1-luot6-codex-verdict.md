Reviewed commit: 039dbe3c25e6148606227107d143f960f552bfe6
Verdict: changes_requested — P0=0 P1=0 P2=6 P3=0

## Phạm vi và định danh

Reviewer độc lập OpenAI/Codex, họ `openai`, thực thi bằng công cụ shell cục bộ, offline. Run tham chiếu `63570626` theo đường dẫn prompt; không suy exact model/runtime attestation từ tên tài khoản. Không dùng context executor, không gọi reviewer khác, không ghi KHO, không push/PR/comment/CI từ xa. Đây là lượt 6/8 theo chỉ thị được giao.

- Exact head `039dbe3c25e6148606227107d143f960f552bfe6`, tree `d934ec396d29c2fd82c3d74cb37eb93f4f6ff54c`; full clone, detached, sạch ở các mốc kiểm.
- Base `f712205aa39e0b54d04a5bd8145fa69a84601fed`. Đã đọc trọn M1–M6, K01–K37, D1–D6, A1–A12, điều kiện dừng và lease. Spec hash khớp `6bcac18917516e89119065a249037cb81f13d77b01bb77e7b557f6d23d5c0b07`.
- Diff đúng một tệp `.claude/dev/packet_loop_test.py`, **+717/−20**. `packet_loop.py` không đổi. Vượt 450 đã được chủ kho cho phép trong prompt, không tính finding.

[Định danh](evidence/repository-identity.json), [spec](evidence/wp822-spec.md), [lease](evidence/wp822-lease.yaml).

## Bảng lớp

Các dòng dưới đây thuộc tệp trên exact head, không phải số dòng HINT. Có **75 đột biến kiểm toán sống đủ 184/184 ca kg**, mỗi đột biến có phản chứng CLI thường làm ca đúng đỏ mà không crash, thuộc năm lớp phủ; lớp thứ sáu là fixture vi phạm nhiều chốt. Không đếm mỗi biến thể thành một finding.

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| `kiem-kieu-chi-do-mot-loai-sai` | P2 | `packet_loop_test.py:5947`, `:6220`, `:6226`, `:6252` | 14 mutant sống: bỏ run null/bool/float/string/list; bỏ suite object bool/int/float/string; bỏ run thiếu id/name/head; suy count từ list/dict. Phản chứng rc12→0 hoặc rc12 giữ nguyên nhưng mất đúng lý do schema | Tích kiểu JSON và vắng khóa cho mọi tầng run/suite/count, ở mọi vị trí; HINT |
| `chi-kiem-kieu-trang-dau` | P2 | `packet_loop_test.py:5947`, `:5957`, `:5970` | 8 mutant sống: chỉ kiểm hai đầu trang đối với schema/run/suite/count/âm/hiện diện; chỉ kiểm count âm/hiện diện ở trang cuối. Trang giữa hoặc đầu vẫn lọt, hay đổi lý do sang count | Tích vị trí run × trang đầu/giữa/cuối, có trang hợp lệ trước và sau; HINT |
| `so-khop-so-nguyen-chua-chinh-xac` | P2 | `packet_loop_test.py:5970`, `:5990`, `:6211` | 16 mutant sống: alias suite qua float/abs/prefix ở danh tính, lọc neo và cảnh báo; alias run-id; alias id cảnh báo; hạn chế sai miền int suite. Ví dụ suite 2^53 và 2^53+1 làm rc12→0; run-id khác nhau bị nhập làm một khiến rc0→12; cảnh báo giữ rc0 nhưng sai id/count | Cặp số × hai thứ tự, dấu âm/0/biên 2^53/số lớn; đo riêng identity/filter/warning và chiều int hợp lệ; HINT |
| `so-khop-tuyet-doi-chua-du` | P2 | `packet_loop_test.py:5863`, `:5864`, `:5880`, `:5912`, `:6237` | 35 mutant sống: khử trùng chuẩn hóa/biên/giữa/thứ tự, cắt ký tự đầu status, trim ký tự biên, bỏ ký tự giữa hoặc so chuỗi sau sắp xếp, ở các phép so/tuple danh tính. Mẫu đổi ký tự đầu của completed dùng c nên tự bằng gốc và bị bỏ. Hai tên bị gộp, hoặc chuỗi thiếu ký tự biên được nhận: rc12→0 | Thay ký tự luôn khác gốc ở mọi vị trí, xóa/lặp ký tự, hoán đổi cặp kề, hai tên gần đúng × thứ tự × màu; HINT |
| `check-suite-chua-phu-bien-chuoi` | P2 | `packet_loop_test.py:6006`, `:6234` | 2 mutant sống: chỉ đòi ASCII ở hai đầu, nới Unicode hoặc space ở giữa. `1١1` rc2→0; `1 1` rc2→12/VẮNG, đổi lý do từ chối | Ký tự sai ở đầu/giữa/cuối; Unicode parse được neo suite 111. Space giữ làm ca từ chối; mutant khai trong HINT dùng Unicode để đích ra rc0 |
| `fixture-vi-pham-nhieu-chot` | P2 | `packet_loop_test.py:5435`, `:5502`, `:5562`, `:5786`, `:5974` | 15 fixture K24 sửa riêng đối số hỏng vẫn rc12 VẮNG. Quét tiếp: 12 ca tên cũ và 6 ca suite dưới guard gỡ đều rc2→12, bị VẮNG chặn hộ; một ca suite parse được có đối chứng rc0 | Dựng run cho mọi tên, kể cả tên hỏng; neo JSON suite theo giá trị int của đối số sai dạng nhưng parse được. Giữ abc là ca âm, chuyển ca đích mutant sang các giá trị có thể tách chốt. HINT |

[90 kiểm toán: 75 sống có phản chứng native, 15 không thuộc nhóm sống. Tất cả biểu hiện/cặp tìm-thay và phân loại](evidence/audit-by-class.json). Mỗi `evidence/audit-<name>.json` có đủ 184 tên và màu; mỗi `evidence/confirm-<name>.json` có fixture, đầu ra CLI nền/đột biến và phân loại đúng. [Fixture vị trí](evidence/position-fixture-isolation.json), [quét mọi ca đích đối số cũ](evidence/argument-targets.json).

Đủ biểu hiện còn sót đã quét theo lớp:

- **Kiểu/hiện diện:** run sai cấu trúc 5 dạng; suite sai cấu trúc 4 dạng; thiếu riêng id/name/head; total_count list/dict. Status/conclusion thiếu và các kiểu sai của sáu field đã được các ca r5 khóa, không gộp chúng thành lỗi mới.
- **Phân trang:** schema field, cấu trúc run, cấu trúc/id suite, total_count hiện diện/kiểu/âm. Bộ sinh r5 đặt field hỏng ở một trang hoặc trang cuối của hai trang; chưa có trang hợp lệ sau nó. K05 dạng chính trang đã khóa đầu/giữa/cuối, không báo lại lỗi đó.
- **Số:** đầy đủ name của 16 biến thể trong bảng JSON. Với map identity, HINT chuẩn hóa cùng một key ở cả setdefault và lookup chẩn đoán, tránh lấy tín dụng từ KeyError của phản chứng.
- **Chuỗi:** còn hở cả khử trùng tên lẫn một số phép so trực tiếp/tuple khi trim ký tự biên. Đã chạy đủ 35 kiểm toán biên/vị trí/thứ tự bổ sung: 31 sống, 4 bị ca cũ giết. Cộng 4 mutant khử trùng chuẩn hóa có trước thành 35 biểu hiện của cùng lớp. `_kg_gan` phải tạo giá trị thực sự khác ở mọi vị trí, gồm xóa/lặp ký tự và đổi chỗ cặp kề; HINT mở rộng cơ chế này cho mọi vị trí so.
- **Đối số:** tên rỗng, space, mọi ký tự splitlines có sẵn, vị trí trong nhiều tên; suite âm/0/0 đầu/dấu cộng/Unicode đều phải có JSON neo phù hợp để mutant ra xanh giả. Không xóa tên ca base.

## Kiểm kê độc lập, M3 và M5/M6

Đã đọc cả hai hàm cùng hằng/hook và đối chiếu các nhánh với K01–K41. Có 54 nút AST điều kiện/so sánh/bool/except/comprehension trong cách đếm của probe. **Không tìm thấy thành phần hoàn toàn ngoài bảng**, không có dòng `tuong_duong`. K38–K40 bổ sung hành vi có thật; K41 help nằm ngoài hai hàm và được giữ cho M5(a). Các finding là khoảng trống của K đã có, không kích hoạt H2 lên 9. [Kiểm kê độc lập](evidence/inventory-independent.md), [AST](evidence/independent-predicates.json), [bảng runtime](evidence/inventory-runtime.json).

**D1–D6 đạt A1–A3:** đúng tìm/thay nguyên văn, mọi ca đích riêng rc12→0, phân loại GIẾT thật, đối chứng khác họ xanh. D6 trên cả tên cũ `kg_m2_thieu_conclusion` cũng rc0, không THỪA id. [Biên nhận CLI](evidence/D1-D6.json). Đã đối chiếu 333 ca đích trong toàn bộ 248 mutant: mọi ca có rc hoặc nội dung CLI đổi, không ca chết mà CLI giữ nguyên; các fixture đối số bị chốt khác chặn hộ được tính ở lớp fixture trên.

**M5:** ba phép độc lập (đổi tên K27 giữ toàn ánh xạ; thêm tên mutant không tồn tại; thêm kg ngoài bảng) lần lượt làm đúng (c)/(b)/(a) đỏ. Ba t822 tương ứng cũng đỏ.

**M6:** chạy nguyên các ca có sẵn: các vỏ × hai kênh, Unicode escape 1–2 lớp, rc ngoài bộ, help, cause/context/from None/BoQua/group và banner ở fixture/đối số. Chín guard t822_m6, classifier coi mọi đỏ là GIẾT và bốn mutant độc lập (cause/context/except thường/chỉ stdout) đều làm tự kiểm đỏ; đối chứng xanh. Module nhắm test nạp riêng có lớp marker khác danh tính, classifier của đúng module được dùng. [Tự kiểm](evidence/selfcheck-results.json). Các kết quả TIN_DUNG_GIA của kiểm toán không được nhận làm GIẾT; ví dụ run_identity_prefix có 11 ca chỉ crash nên bị loại khỏi nhóm 75 sống có phản chứng hợp lệ.

## Gate và nghiệm thu

Lệnh đã chạy trên bản sao nguyên vẹn của exact head:

```text
cp -a /home/user/rv822 /tmp/wp822-rv6-gate
python3 -B /tmp/wp822-rv6-gate/.claude/dev/packet_loop_test.py
```

**rc0 · nền 634/634 · BỎ QUA 1 · TỔNG: ĐẠT.** Có 502 mutant: **501 GIẾT**, **1 BỎ QUA** (`luong_canonical_chay_that_dao_os_name`, Windows, ngoài họ kg). Không khai đã giết cả 502. [Log đầy đủ](gate.log), [tổng gate](evidence/full-suite-summary.json).

A11 hoàn tất **248/248** mutant, mỗi mutant đủ 186 tên (184 kg + cp1252/cp1258); đủ 46.128 màu, gồm mọi ca ngoài đích đổi màu. 14 kết quả crash ngoài đích được ghi TIN_DUNG_GIA, không cấp GIẾT. [Target CLI deltas](evidence/target-cli-delta-summary.json). Tổng chốt: **248/248 mutant × 186 tên**, **123412 kết quả lệnh dưới mutant trong biên nhận**; lỗi probe/target tín dụng giả: 0. [CSV](evidence/A11-colors.csv), [tổng](evidence/A11-summary.json).

Để chạy đầy đủ ma trận, các ca ngoài đích dùng toàn bộ source entrypoint trong process fork mới; **mọi ca đích vẫn subprocess Python thông thường**. Không import/gọi thẳng hàm nội bộ sản phẩm. Source/argv/env/stdout/stderr riêng; rc ngoài bộ hợp lệ được phát lại bằng CLI thường để giữ chẩn đoán native. Đã đối chiếu **512/512** lượt nền, gồm các chương trình M6 thật có sẵn, với rc/stdout/stderr bằng nhau (chuẩn hóa địa chỉ bộ nhớ). Chỉ cache source đã băm/biên dịch và launcher bất biến; cache được giới hạn, GC tắt trong con ngắn hạn. [Parity](evidence/entry-parity-bounded.json), [runner](evidence/fast_entry.py), [probe cuối](evidence/matrix_final.py). Tổng lệnh đếm các kết quả gọi harness được ghi; fallback có thể thực thi lại, không cộng lượt sơ bộ vào tổng này. Hai ca codepage chạy đầy đủ ở nền; dưới mutant phát lại đúng CLI kiem-gate/fixture/encoding, đòi rc0 và stdout có nội dung, không lặp lệnh ngoài phạm vi. M6 selfcheck và gate đầy đủ được đo CLI thường độc lập.

| Tiêu chí | Kết quả |
|---|---|
| A1–A3 | Đạt: D1–D6 đúng, rc12→0; D6 tên cũ rc0; đối chứng xanh |
| A4, A12 | Đạt: từng chốt M5/M6 tự kiểm có răng |
| A5 | Không có tuong_duong hoặc thành phần hoàn toàn vắng; còn sáu lớp finding |
| A6 | Đạt: full gate rc0, 634/634, TỔNG ĐẠT |
| A7 | Base 554 xanh +1 skip; head 634 xanh +1 skip; đủ 555 tên base, vắng/trùng/đổi màu 0 |
| A8 | doctrine-scan/adr-song base và head đều rc0, có đầu ra dương |
| A9 | Một tệp +717/−20, vượt 450 đã được phép |
| A10 | Base/head cùng 2 F541; F401=F821=0, delta F=0 |
| A11 | Xem số hoàn tất và CSV phía trên; không dùng màu xanh gate để thay biên nhận |

[A7 từng tên](evidence/A7-colors.csv), [A7 tổng](evidence/A7-summary.json), [base exact](evidence/A7-base-exact.json), [base/head gates](evidence/baseline-gates.json), [Ruff](evidence/ruff-delta.json). Đã đo lại đầy đủ base trên checkout cố định f712205: HEAD trước/sau trùng base, 554 xanh + 1 skip. Lượt đo này thay metadata HEAD chụp sớm của phép đo ban đầu; không dùng metadata đó để kết luận A7.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| lượt | lớp | nhãn | bằng chứng/quét lại |
|---|---|---|---|
| 1 | tin-dung-giet-sai | đã vá thật | ca sẵn và mọi guard đã thử có răng; classifier đúng module |
| 1 | trung-id-chi-do-mot-chieu | đã vá thật | bản đỏ status/conclusion ở mọi vị trí trong ba bản cùng id |
| 1 | ten-trang-chi-khoa-space | đã vá thật | TAB/NBSP và tên hợp lệ đã có răng; space fixture chưa thuần là lớp riêng |
| 1 | fixture-vi-pham-nhieu-chot | vá hờ | bốn fixture cũ đã sửa; lớp tái phát ở đối số và bộ sinh vị trí |
| 2 | tin-dung-giet-sai | đã vá thật | JSON/repr/log/escape có sẵn, rc, cause/context đều được đo |
| 2 | sha-chi-do-ngan-va-hoa | đã vá thật | 39/41/phi-hex/hoa, trim/NFKC và Unicode chữ/số đều khóa |
| 2 | id-lon-nhat-chua-do-so-hoc | đã vá thật | max số qua hai thứ tự/hai màu, âm và biên 2^53; alias identity là lớp khác |
| 2 | canh-bao-chi-do-mot-id | đã vá thật | ba id/ba tên/bản lặp/số thứ tự đã khóa; alias số là lớp mới |
| 2 | chi-kiem-kieu-trang-dau | vá hờ | các ca cũ chết đúng, nhưng trang giữa và phạm vi chỉ-cuối còn sống |
| 3 | chi-kiem-kieu-trang-dau | vá hờ | cùng khoảng trống vị trí trang trong K07–K15/K37 |
| 3 | khoa-trung-chua-phu-moi-tang | đã vá thật | suite.id và extra root/object/array đều bị guard tương ứng bắt |
| 3 | so-khop-tuyet-doi-chua-du | vá hờ | khử trùng tên và trim biên còn lọt; status đổi ký tự đầu c→c không tạo phản chứng |
| 3 | bao-loi-chi-do-mot-ten | đã vá thật | đủ ba dòng lý do và tổng; cắt đầu/cuối/giữa bị bắt |
| 3 | tin-dung-giet-sai | đã vá thật | cause-only, banner chỉ đối số, BoQua/group có răng riêng |
| 4 | so-khop-tuyet-doi-chua-du | vá hờ | họ gần đúng thiếu xóa/lặp biên; lỗi c→c ở completed; chưa dùng đồng thời hai tên gần nhau |
| 4 | bao-loi-chi-do-mot-ten | đã vá thật | ba tên đỏ đầy đủ, cùng tổng chính xác |
| 4 | canh-bao-chi-do-mot-id | đã vá thật | đủ ba tên/id và thứ tự số, không tái phát phép cắt |
| 5 | kiem-kieu-chi-do-mot-loai-sai | vá hờ | sáu field đã phủ kiểu; thiếu cấu trúc run/suite/count và một số khóa vắng |
| 5 | kiem-tra-toan-bo-chua-phu-vi-tri | vá sinh lỗi mới | vị trí được quét nhưng 15 fixture tên hỏng thiếu run của các tên còn lại, vi phạm M3 |
| 5 | chi-kiem-kieu-trang-dau | vá hờ | K05 đã khóa mọi vị trí; các guard schema/count mới chỉ có trang hỏng ở cuối |
| 5 | id-lon-nhat-chua-do-so-hoc | đã vá thật | các mutant r5 max/abs/float/đầu/cuối bị giết |
| 5 | sha-chi-do-ngan-va-hoa | đã vá thật | dạng sai ở --head đã có fixture khớp head nguyên văn |
| 5 | check-suite-chua-phu-bien-chuoi | vá hờ | trim/NFKC/biên đã khóa, Unicode/space giữa còn lọt |
| 5 | trung-id-chi-do-mot-chieu | đã vá thật | status/conclusion một đỏ trong ≥3 bản ở mọi vị trí |

## HINT.patch

**Chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit.**

[HINT.patch](HINT.patch) chỉ chạm `.claude/dev/packet_loop_test.py`; apply-check, áp thật trên copy pristine exact head, diff-check và đối chiếu bytes đều đạt. Diff **+229/−31 dòng**; SHA-256 `6fd9a9eb106606c063277ca4dd237fdeccdfe7048e48f96879695c1d6dc9d3b9`. [Biên nhận](evidence/hint-apply.json).

HINT dùng bộ sinh tích kiểu/thiếu khóa/cấu trúc × vị trí run × vị trí trang; cặp số và miền int; cả họ hai tên gần đúng × thứ tự × chiều màu; ký tự sai trong suite; và sửa toàn bộ fixture đối số có cùng hình dạng. Bảng kiểm kê nối các họ mutant trực tiếp vào dòng K; cập nhật mỏ neo tự kiểm K25 cùng thay đổi bảng. Giữ mọi tên ca base.

Các rủi ro đã canh: count toàn cục và id bool không alias với id run hợp lệ; lookup chẩn đoán dùng cùng key đã chiếu để không lấy KeyError làm tín dụng; suite id JSON vẫn được là mọi int trong khi CLI chỉ nhận số dương; chuỗi abc/space không parse được vẫn có ca âm nhưng không làm ca đích khai rc0; không siết hoặc chuẩn hóa tên hợp lệ của sản phẩm.

**HINT cuối: nền 197/197 xanh; 94 mutant r6 mới, 58 mutant r4 và 8 mutant r5 vị trí đều GIẾT đúng ca đích; 7 mutant đối số cũ và 3 mutant M5 cũng GIẾT, các đối chứng xanh.** CLI thường cho các ca đích; nền HINT dùng runner đã kiểm parity. Đo riêng 32 cặp ca đích đối số và 15 fixture vị trí: tất cả rc2→0 dưới guard gỡ, không còn VẮNG chặn hộ. [Đối số](evidence/hint-argument-targets.json), [vị trí](evidence/hint-position-isolation.json). [Tổng HINT](evidence/hint-results-final.json), [160 mutant](evidence/hint-position-mutants.jsonl), [đối số/M5](evidence/hint-position-legacy.json), [nền](evidence/hint-position-baseline.json). Bản HINT cuối đã cập nhật mỏ neo K25, kiểm kê đủ mutant và không đổi mã sản phẩm. Không chạy full suite trên HINT. Full gate phía trên thuộc commit đang review.

## Ngoài phạm vi và giới hạn

Không sửa packet_loop.py, chứng minh nguồn gốc JSON/API, hoặc quy hạng ca ngoài họ kg. Không chạy Windows; skip được ghi riêng. Không có thao tác GitHub/land/approve/đẩy nhánh.

Theo phân công, không tự viết mã in/giả/bọc traceback hay payload crash. Dùng nguyên các phản chứng sẵn trong cây. Hướng chỉ mô tả, chưa chạy, không tính finding: banner được escape sâu hơn ba lớp hoặc codec khác; fixture mang banner đồng thời CLI có rc ngoài bộ; path thoát cây, byte thô bất thường, symlink. Kỳ vọng vẫn loại crash và không gán tín dụng giả cho assertion đúng; không suy các mẫu đã đo thành chứng minh mọi codec/độ sâu.

Sáu lớp P2 còn mở nên **changes_requested**, dù full gate xanh. Ngưỡng Q6 đòi mọi P0/P1/P2/P3 bằng 0. Các lớp tái phát đã được ghi rõ; việc vá và lời gọi review tiếp theo thuộc quyền quyết định của chủ kho, không tự mở thêm vòng.
