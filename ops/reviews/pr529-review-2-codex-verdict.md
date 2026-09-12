verdict: changes_requested
reviewed_sha: f01a35033856888354136a6379d16dba8cbffcdd
so_p1: 0  so_p2: 3  so_p3: 0
so_the_hien: 5

## ĐỐI CHIẾU LƯỢT TRƯỚC

Phán theo cơ chế, không theo lời khai executor. Cả năm slug giữ nguyên; phép làm ĐỎ kiểm bản vá lượt trước không cộng vào N hướng săn.

| slug | hạng lượt 1 | phán canonical | bằng chứng tự đo |
|---|---|---|---|
| `sai-dai-luong-hoi-tu` | P1 | **VÁ SINH LỖI MỚI** | M5 work:150–166 đã khôi phục công thức và ngưỡng, #508 cho hai kết luận khác nhau. Hướng 1–2 phát hiện miền 0/0 và đơn vị lớp/thể hiện chưa chốt trong công thức mới; xem hai thể hiện hiện hành. |
| `gop-dieu-kien-dung-review-class` | P2 | **ĐÃ VÁ THẬT** | cross:375–379 có đúng ba hàng riêng, routine cho P2 thành nợ có tên, systemic không cho P2, sensitive cần approve. work:122–124 buộc đọc bảng đó. A1 gốc True, đổi sensitive/gộp class đều False. Bảng hành động đọc cùng điều kiện dừng, không coi hàng P1/P2 là phủ định ngưỡng routine đã trỏ rõ. |
| `thieu-hop-dong-ban-va-theo-lop` | P2 | **ĐÃ VÁ THẬT** | cross:386–394 đòi BẢNG LỚP, mỗi finding đúng một lớp và cột phương án/lý do; work:126 buộc ĐỌC trước sửa. A2 bỏ cột hoặc bỏ tính toàn phần đều False. Khung dán chưa nhắc lại bảng không vô hiệu nghĩa vụ tường minh phía trên. Lỗi authority mới ở work:131 là cơ chế khác, báo riêng, không đổi tên lớp này. |
| `mat-dau-vet-thu-hep-pham-vi` | P2 | **ĐÃ VÁ THẬT** | work:174–183 có chua_do_duoc, không tính vá, giữ lớp/phạm vi/nợ và reviewer gọi tên; cross:414 đòi gọi tên. probes/extra.py xác nhận kênh handoff/evidence lên Issue + PR trong §7. Không bắt tạo kho lưu mới ngoài scope chỉ vì mục M6 không lặp lại địa chỉ giao handoff. |
| `phep-do-doctrine-khong-du-rang` | P2 | **CHƯA VÁ** | EVIDENCE:49 vẫn chỉ dùng rc=0 để phán A7. Scanner gốc 0, chép trần 0, chép §5.1 0; chép §12 6 làm đối chứng dương. Cơ chế khớp danh sách cụm vẫn sống; không tính phép thử này vào bảng săn. |

**Kiểm lời khai “gốc là một”:** r1 giải thích cụ thể bốn thiếu sót nội dung M1/M3/M5/M6; lời khai bỏ đọc r1 tương thích với bốn thiếu sót ấy, nhưng không thể xác minh lịch sử đọc của executor từ mirror. Với lớp doctrine, r2 **A13 đã tự ghi phép làm ĐỎ ngay tại SPEC.md:116–120**; không cần mở r1 mới biết hai phép đó. Vì vậy “không đọc r1” không đủ giải thích cả năm, và “đọc r1 + viết lại hai khối” không đóng cơ chế đo sai. Đây được ghi thành thể hiện trong chính lớp `phep-do-doctrine-khong-du-rang`, không nhân thành lớp META thứ hai.

## BẢNG SĂN

Các ca dưới đây là phép đọc hợp đồng kèm phản chứng số học/lịch sử; không tự nhận là cổng cưỡng chế đang có. Chúng khảo sát biến thể chưa đi ở lượt 1. Mỗi khối được nối ngay sau khi chạy hướng ấy.

HƯỚNG 1: M5: miền xác định khi lượt trước sạch nhưng chưa approve (biến thể mới)
  giả thuyết : Nếu sensitive có verdict chưa approve với 0 lớp, lượt sau vẫn phải tính M5 nhưng mẫu số bằng 0.
  lệnh       : `python3 probes/hunt.py 1`
  output     :
```text
Công thức có mặt: True
ZeroDivisionError: division by zero
Miền/nhánh mẫu số 0 trong M5: False
```
  kết luận   : LỖI

Phản chứng số học của công thức văn bản, không phải báo crash của packet_loop. Cần quy định N/A và cách ngắt chuỗi khi mẫu số 0; thuộc sai-dai-luong-hoi-tu.

HƯỚNG 2: M5: bất biến khi một lớp có nhiều thể hiện (biến thể mới, không tráo severity)
  giả thuyết : Nếu finding vừa được đếm theo lớp vừa được hiểu theo thể hiện, cùng verdict có thể cho hai quyết định dừng trái nhau.
  lệnh       : `python3 probes/hunt.py 2`
  output     :
```text
vòng 2: 3 lớp trước, 2 lớp VÁ THẬT (mỗi lớp 1 thể hiện), 1 lớp CHƯA VÁ (8 thể hiện); theo lớp=2/3=0.667; theo thể hiện=2/10=0.200
vòng 3: 3 lớp trước, 2 lớp VÁ THẬT (mỗi lớp 1 thể hiện), 1 lớp CHƯA VÁ (8 thể hiện); theo lớp=2/3=0.667; theo thể hiện=2/10=0.200
Hai vòng: theo lớp STOP=False; theo thể hiện STOP=True
cross: findings_ids = slug của LỚP; work: mẫu số finding + Giữ ánh xạ thể hiện khi đếm
```
  kết luận   : LỖI

Công thức không khóa đơn vị vào slug LỚP, dù chỉ thị chủ kho đếm lớp. Không kết luận mọi người sẽ chọn thể hiện; chính hai cách tính cho kết luận khác nhau là lỗ hổng hợp đồng. Thuộc sai-dai-luong-hoi-tu.

HƯỚNG 3: M4: lớp xuất hiện muộn, biến mất rồi quay lại
  giả thuyết : Nếu khoảng trống reset lịch sử lớp thì xuất hiện lần ba có thể vẫn được vá lẻ.
  lệnh       : `python3 probes/hunt.py 3`
  output     :
```text
Chuỗi vòng 1..5: [A], [], [A], [], [A]; số lần xuất hiện A: [1,1,2,2,3]
M4 định nghĩa 3 finding cùng lớp trong một vòng là lần 1: True
Protocol: Cùng hình dạng lỗi xuất hiện lần
thứ ba bắt buộc xem lại có nên tiếp tục cách làm đó, không chỉ vá lần thứ tư.

## 13. Hợp đồng ba skil
Slug giữ nguyên qua lượt: True
```
  kết luận   : KHÔNG PHẢI LỖI

Đọc cả con trỏ §12: ngưỡng là số lần xuất hiện, không phải số thứ tự review toàn packet hay số lần liên tiếp. Không có quyền reset khi vắng. Ca A tới lần 3 ở vòng 5; một lớp mới ở review 3 chỉ là lần 1.

HƯỚNG 4: Bảng dừng với packet không khai review_class
  giả thuyết : Nếu thiếu review_class được ngầm coi routine thì có thể dừng sớm.
  lệnh       : `python3 probes/hunt.py 4`
  output     :
```text
§3.2: review_class nằm trong schema tối thiểu: True
§8: Review Class được tính fail-closed từ `risk`, effective write set và diff thật. Packet khai `review_class` là
mức tối thiểu; dispatcher ghi `effective_review_class` bằng mức cao hơn giữa khai báo và classifier. Executor
không được hạ lớp. Path không biết, classifier lỗi hoặc bằng chứng không đọc được đều thành `sensitive`; human
chỉ override bằng quyết định có audit.

- `sensitive`: workflow/CI authority, security/credential bou
```
  kết luận   : KHÔNG PHẢI LỖI

Không có mặc định routine. Schema/preflight từ chối thiếu; classifier và effective_review_class xử lý fail-closed. Bảng là bước dùng class đã xác định, không phải nơi cấp class mới.

HƯỚNG 5: M7: run_id của loại (b) và write_set không có ops/reviews
  giả thuyết : Nếu mọi lượt CI của #523 buộc có biên nhận loại (b), packet hai tệp không thể thi hành.
  lệnh       : `python3 probes/hunt.py 5`
  output     :
```text
N=0 trước merge: True
Loại (a) gồm CI hậu merge: True
Loại (b) 0 lượt => nghĩa vụ run_id loại (b) 0 lần; loại (a) không dùng ngân sách N
```
  kết luận   : KHÔNG PHẢI LỖI

M7 không gây xung đột mới này trên #523. Nghĩa vụ lưu verdict/receipt review là hợp đồng khác, EVIDENCE đã khai giới hạn, không được lấy nó để suy M7 thất thi.

HƯỚNG 6: Bản vá theo lớp biến gợi ý reviewer thành mệnh lệnh
  giả thuyết : Nếu reviewer đề nghị một cách vá nhưng executor tái dẫn xuất được cách khác đóng lớp tốt hơn, bảng mới buộc chép đúng cách cũ và trái protocol.
  lệnh       : `python3 probes/hunt.py 6`
  output     :
```text
| lớp P1/P2 còn mở, lớp khai **bản vá theo lớp** | thực hiện ĐÚNG bản vá theo lớp ấy |
Gợi ý là gợi ý, không phải chỉ thị: người vá được làm khác, và lượt sau Reviewer
không được coi *đã làm theo gợi ý của tôi* là bằng chứng đúng — vẫn phải đo. Finding
không có gợi ý, hoặc gợi ý chỉ nhắc lại chính finding, thì v
Fixture: reviewer gợi ý sửa bộ đọc; executor đo được sửa bộ sinh đóng cùng lớp và giữ acceptance. §7 cho phép làm khác; hàng work-packet không cho phép.
```
  kết luận   : LỖI

Đây là quyền quyết định cách vá, độc lập với thiếu cột/thiếu bước đọc của lượt 1. Sửa nghĩa vụ thành tái dẫn xuất + đo cách đóng lớp, cho phép khác gợi ý với lý do và evidence.

## Đo lại phép làm ĐỎ A1–A13 (không tính vào số hướng săn)

Lệnh: `python3 probes/acceptance.py`. Mỗi đột biến được ghi vào mirror, đọc lại và phục hồi trong `finally`. A1–A6/A8/A10–A12 dùng vị từ đọc hẹp do reviewer viết, không phải cổng của kho; chỉ chứng minh phân biệt các phép ĐỎ đã nêu. A7/A13 gọi scanner thật. Chi tiết: `probes/acceptance.json`.

```text
{"ca": "A1", "variant": "original", "predicate": true, "expected": true}
{"ca": "A2", "variant": "original", "predicate": true, "expected": true}
{"ca": "A3", "variant": "original", "predicate": true, "expected": true}
{"ca": "A4", "variant": "original", "predicate": true, "expected": true}
{"ca": "A5", "variant": "original", "predicate": true, "expected": true}
{"ca": "A6", "variant": "original", "predicate": true, "expected": true}
{"ca": "A8", "variant": "original", "predicate": true, "expected": true}
{"ca": "A10", "variant": "original", "predicate": true, "expected": true}
{"ca": "A11", "variant": "original", "predicate": true, "expected": true}
{"ca": "A12", "variant": "original", "predicate": true, "expected": true}
{"ca": "A1", "variant": "sensitive=hết P1 P2", "predicate": false, "expected": false}
{"ca": "A1", "variant": "gộp routine/systemic", "predicate": false, "expected": false}
{"ca": "A2", "variant": "bỏ cột bản vá", "predicate": false, "expected": false}
{"ca": "A2", "variant": "finding không có lớp", "predicate": false, "expected": false}
{"ca": "A3", "variant": "CẤM -> nên xem xét", "predicate": false, "expected": false}
{"ca": "A4", "variant": "thay công thức bằng tổng", "predicate": false, "expected": false}
{"ca": "A5", "variant": "bỏ điều khoản scope", "predicate": false, "expected": false}
{"ca": "A6", "variant": "gộp b/c", "predicate": false, "expected": false}
{"ca": "A6", "variant": "bỏ run_id", "predicate": false, "expected": false}
{"ca": "A8", "variant": "bỏ khai giới hạn", "predicate": false, "expected": false}
{"ca": "A10", "variant": "giữ câu cũ trước r2", "predicate": false, "expected": false}
{"ca": "A10", "variant": "nghĩa vụ -> nên kiểm", "predicate": false, "expected": false}
{"ca": "A11", "variant": "bỏ (2)", "predicate": false, "expected": false}
{"ca": "A11", "variant": "bỏ (3)", "predicate": false, "expected": false}
{"ca": "A12", "variant": "để N mở", "predicate": false, "expected": false}
{"ca": "A4", "variant": "#508 supplied data", "total_stop": false, "ratio_stop": true, "rates": [0.3076923076923077, 0.25]}
{"ca": "A12", "variant": "#512 supplied automatic-only trace", "manual_runs": 0, "allowed": true, "historical_trace_verified": false}
{"ca": "A7/A13", "variant": "original", "rc": 0, "output": "doctrine-scan: sạch — đã quét 7 tệp, 0 chỗ chép doctrine\n"}
{"ca": "A7/A13", "variant": "A7-copy-section12", "rc": 6, "output": ".claude/skills/cross-review/SKILL.md:500: [nguong-so-stop-conditions] chép doctrine: '3 attempt/packet'\n.claude/skills/cross-review/SKILL.md:501: [nguong-so-stop-conditions] chép doctrine: 'tối đa 20 packet'\n.claude/skills/cross-review/SKILL.md:502: [nguong-so-stop-conditions] chép doctrine: 'độ sâu kế nhiệm 5'\n.claude/skills/cross-review/SKILL.md:502: [nguong-so-stop-conditions] chép doctrine: '3"}
{"ca": "A7/A13", "variant": "A7-A13-copy-cap", "rc": 0, "output": "doctrine-scan: sạch — đã quét 7 tệp, 0 chỗ chép doctrine\n"}
{"ca": "A7/A13", "variant": "A13-copy-section5.1", "rc": 0, "output": "doctrine-scan: sạch — đã quét 7 tệp, 0 chỗ chép doctrine\n"}
```

Đo bổ sung (không tăng N): `python3 probes/extra.py`
```text
{"ca": "A9", "original": [2, 179], "mutant_add_301_lines": [2, 480], "original_pass": true, "mutant_pass": false}
{"case": "M5_reverse", "previous_classes": 3, "fixed_classes": 1, "class_rate": 0.3333333333333333, "previous_instances": 10, "fixed_instances": 8, "instance_rate": 0.8, "class_stop_after_two": true, "instance_stop_after_two": false}
{"case": "M6_delivery", "must_keep_scope_and_debt": true, "reviewer_names_it": true, "handoff_post_issue_pr": true}
```

## BẢNG ĐO

Lệnh nền: `python3 probes/measure.py`; các phép đọc/đột biến: `python3 probes/acceptance.py`, `python3 probes/extra.py`. Các lệnh cổng chạy từ `cay-kho`, với `TMPDIR` trỏ `probes/tmp` trong sandbox và `PYTHONDONTWRITEBYTECODE=1`. Không gọi mạng, không gọi CI tay, không commit.

| khẳng định | SPEC/EVIDENCE/PR khai | bạn đo được | khớp? |
|---|---|---|---|
| Exact head | `f01a35033856888354136a6379d16dba8cbffcdd` | `rev-parse HEAD` đúng SHA; tree `c40ee5d733339868e3cb10456b7d870e3352646c` | Có |
| Base | `85fcbf8aea75f0577f47d7332c02a50f993a9d1b` | `origin/master` đúng SHA; ancestry rc=0 | Có đối với ref đã đóng băng; không xác minh master trên máy chủ hiện tại |
| Mirror | detached, không shallow, abbrev 7, sạch | HEAD đúng; shallow=false; local abbrev=7; status rỗng trước/sau đột biến | Có |
| Hash SPEC r2 | `4ada6921503da3748ef54b019633e440d21a8f23c3c15f7e1064fe8f3ae85a58` | `sha256sum` trùng nguyên giá trị | Có |
| Hash verdict r1 | `9695e0ebd787bcc8f915b6b28fea6c60404dfe07ad39f4b8fe787e89de11c400` | `sha256sum` trùng nguyên giá trị | Có |
| Số hạng cross-review | 77 thêm, 1 xoá | `git diff --numstat <base> HEAD`: 77/1 | Có |
| Số hạng work-packet | 102 thêm, 0 xoá | Cùng lệnh: 102/0 | Có |
| A9: tổng/phạm vi | 2 đường, 179 thêm, ≤300 | Đúng hai đường skill; 77+102=179; thêm 301 dòng trong mirror ⇒ 480, vị từ nghiệm thu ĐỎ; đã phục hồi | Có |
| Docs | 73 tệp Markdown không đổi | `rglob('*.md')`=73, diff docs rỗng | Có |
| Manifest | Không tệp thuộc manifest đổi | Giao tập changed paths với `manifest.files[].path` rỗng | Có |
| A1 | 3 hàng class khác nhau; sensitive cần approve | Parse đúng tập, điều kiện đôi một khác; đổi sensitive hoặc gộp class đều ĐỎ | Có |
| A2 | Có cột kế hoạch lớp và phải đọc trước sửa | Header bảng đủ cột; nghĩa vụ ĐỌC ở work:126; bỏ cột hoặc cho phép finding không có lớp ⇒ ĐỎ | Có về thiếu sót lượt 1; câu work:131 sinh vấn đề authority riêng |
| A3 | Cấm vá lẻ lần thứ ba, đơn vị lớp | M4 có hành động bắt buộc, ba thể hiện một vòng vẫn lần 1; thay CẤM bằng nên xem xét ⇒ ĐỎ | Có |
| A4, dữ liệu được giao của #508 | TỔNG không bắn; PHÂN HẠNG bắn | 4/13=30.769%, 3/12=25%; luật tổng=False, tỉ lệ=True ở vòng 3; bỏ công thức ⇒ ĐỎ | Có trên bộ dữ liệu được giao; không phải chứng thực nguồn số lịch sử GitHub |
| M5 trên ca biên mới | Công thức finding vòng trước | 0/0 không xác định; 1/3 lớp và 8/10 thể hiện cho quyết định ngược nhau | Không đủ hợp đồng miền/đơn vị |
| A5 | `chua_do_duoc` ×2, gọi tên ở cả hai skill | Đếm đúng 2; M6 giữ lớp/phạm vi/nợ, cấm tính đã vá; bỏ mục M6 ⇒ ĐỎ | Có |
| A6 | (b) N đóng băng + run_id; (c) cấm | Đủ 3 hàng; gộp b/c hoặc bỏ run_id ⇒ ĐỎ | Có |
| A7 — lệnh gốc | Scanner rc=0 | `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: rc=0, 7 tệp, 0 hit | Có về output gốc |
| A7 — phép ĐỎ | Chép §12 hoặc trần ⇒ scanner ĐỎ | Chép toàn §12 ⇒ rc=6; chép câu trần từ ADR-0043 ⇒ rc=0 | Không: một nhánh ĐỎ không chết |
| A8 | Khai kỷ luật đọc, 0 cổng, packet cưỡng chế | Đủ câu ở work:217–220; bỏ khối khai giới hạn ⇒ ĐỎ | Có |
| A10 | Phân biệt nguyên nhân và buộc đo drift trước vòng dự đoán cuối | Hai nhánh khác hành động; thay bằng câu cũ hoặc “nên kiểm” ⇒ ĐỎ | Có trên văn bản |
| A11 | 3 mệnh đề hậu merge | Bỏ riêng (ii) hoặc (iii) ⇒ ĐỎ | Có trên phép thử SPEC đã nêu |
| A12 | N=0, gọi tay trước merge là cấm | Bỏ N=0 ở hàng ngân sách ⇒ ĐỎ; chuỗi tự động/0 gọi tay được chấp nhận | Có về quy tắc; lịch sử gọi CI #512 không đo trực tiếp |
| A13 | Chép §5.1 hay con số trần ⇒ ĐỎ | Chép nguyên đoạn §5.1 ⇒ rc=0; chép trần ⇒ rc=0 | Không |
| Gốc năm lớp | Chỉ vì không đọc r1 | A13 r2:116–120 đã đòi hai phép ĐỎ của scanner, không phụ thuộc đọc r1; lỗi này vẫn sống sau lượt vá | Không đủ giải thích cả năm lớp |
| idiom | rc=0 | `python3 .claude/dev/idiom_py_test.py`: rc=0; 7 ca, 0 bỏ qua, 9 đột biến, 7 tệp, ĐẠT | Có |
| adr-song | rc=0 | `python3 .claude/dev/packet_loop.py adr-song --root .`: rc=0; 48 ADR/48 dòng | Có |
| doc-claims-check | rc=0 | `python3 scripts/tl.py doc-claims-check --strict`: rc=0, ok=true, strict=true | Có |
| release-verify | rc=0 | `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`: rc=0, ok=true, expected=checked=180, hash match=true | Có |
| diff whitespace | rc=0 | `git diff --check <base> HEAD`: rc=0, stdout rỗng | Có |
| lease-publish wrapper | rc=0 | NOT_RUN: wrapper gọi installer actionlint; không có bằng chứng công cụ trong sandbox để chạy nguyên đường mà không cài/tải. Không dùng test con để giả tương đương wrapper | KHÔNG ĐO ĐƯỢC |
| 357↔357; thiếu ref=0 trên nguồn | Đã đo trước clone | Chỉ thấy 359 remote refs hiện có trong mirror; không có tập nguồn độc lập để so. Hai số này không cùng phạm vi/thời điểm | KHÔNG ĐO ĐƯỢC, không phán lệch |
| Cổng nền↔sandbox | Bốn cặp rc bằng nhau tại cùng SHA | Đo được vế sandbox; cấm đọc nguồn ngoài sandbox | KHÔNG ĐO ĐƯỢC vế nguồn |
| gate/thu-hoi f01a350; M10 thực thi | Chưa kết luận; không gọi tay | Không có kết quả CI trực tiếp trong bundle, không gọi GitHub | KHÔNG ĐO ĐƯỢC; không tính xanh |
| Lưu verdict #523 | ops/reviews ngoài write set | Đúng write set chỉ hai skill; nguồn lần này là VERDICT.md theo chỉ thị người dùng | Có về phạm vi; chưa chứng thực bản chiếu PR |

Các phép đọc tự viết chỉ có sức phân biệt trên các mẫu đã chạy; chúng không chứng minh mọi diễn đạt tương đương, và không chứng minh executor thực hiện luật. Lần chạy đầu A1 bị lỗi khoảng trắng ở **probe của reviewer**: chưa `strip()` ô bảng. Đã sửa probe, chạy lại: gốc True, hai mutant False. Không coi lỗi probe ấy là finding sản phẩm. Log có thẩm quyền cuối là `probes/acceptance.json`.

### sai-dai-luong-hoi-tu  [P2]  Công thức được khôi phục nhưng chưa khóa miền xác định và đơn vị LỚP

CƠ CHẾ SINH LỚP: Đại lượng dùng để quyết định dừng chưa được định nghĩa đủ để hai người cùng tính một kết quả. Giữ slug lượt trước vì vẫn là hợp đồng đại lượng hội tụ; lỗi heuristic cũ đã hết, đây là hai thể hiện mới sau khi khôi phục phép chia.

BẢNG THỂ HIỆN:

| tệp:dòng | khai | đo |
|---|---|---|
| `.claude/skills/work-packet/SKILL.md:150` | Chia số finding được vá cho số finding trước, rồi xét hai vòng liên tiếp | Sensitive có thể 0 finding mà chưa approve (chưa đủ bảng săn/độ phủ); lượt sau có 0/0. Không có nhánh N/A hay quy tắc nối/ngắt hai vòng khi mẫu số 0. Phản chứng số học phát `ZeroDivisionError`; đây không phải crash của công cụ kho |
| `.claude/skills/work-packet/SKILL.md:156` | Mẫu số “finding”, phân hạng theo đối chiếu, nhưng lại “giữ ánh xạ thể hiện khi đếm” | cross:397–403 và chỉ thị chủ kho đếm LỚP. Cùng 3 lớp/10 thể hiện, 1 lớp vá thật có 8 thể hiện: theo lớp 1/3<50%, theo thể hiện 8/10≥50%. Lặp hai lần thì một cách DỪNG, cách kia tiếp tục |

VẤN ĐỀ: Ca #508 chỉ kiểm dữ liệu mẫu có mẫu số dương; nó không khóa được đơn vị sau khi packet chuyển sang đếm lớp. r1 dùng “finding” theo dữ liệu vận hành cũ, trong khi chỉ thị hiện hành đếm lớp. Hai thứ hòa được bằng định nghĩa rõ finding dùng trong M5 là slug lớp, và thể hiện chỉ để truy vết; bản hiện tại chưa làm việc ấy, còn câu đếm thể hiện kéo theo hướng ngược. Không báo việc đổi severity thành tỉ lệ nữa. Hạng hiện tại là P2, không giữ P1 lịch sử một cách máy móc: lỗi quyết định có điều kiện, với miền biên và cách đọc đơn vị đang mơ hồ.

ĐÃ THỬ VÁ: không — ở M5 work-packet, định nghĩa tử/mẫu theo tập slug lớp duy nhất của lượt trước; nói rõ cách xử lý mẫu số 0 (không tự gán 0% hay 100%) và ảnh hưởng lên chuỗi hai vòng. Bên reviewer xuất đủ phân hạng lớp để executor tính lại. Không đổi ngưỡng đã được giao.

ĐÃ THỬ NGHIỆM: `python3 probes/hunt.py 1`, `python3 probes/hunt.py 2`, `python3 probes/extra.py`: 0/0 không xác định; 2/3 so với 2/10 và 1/3 so với 8/10 đều đảo quyết định. Ca khóa sau vá: nhân số thể hiện trong một lớp không được đổi tỉ lệ; lượt mẫu số 0 phải có trạng thái xác định và không tự tạo hai vòng <50%. Rủi ro bản vá: hồi tố dữ liệu #508 sang đơn vị khác; phải giữ chú thích đây là bộ dữ liệu finding lịch sử, không tự đổi số hạng.

ĐỘ TIN: vừa về cách người đọc chọn đơn vị; cao về 0/0 và việc hai phép tính cho quyết định trái nhau.

### phep-do-doctrine-khong-du-rang  [P2]  Scanner vẫn lọt phép ĐỎ; lời khai một gốc bỏ sót cơ chế đo sai

CƠ CHẾ SINH LỚP: Dùng không khớp danh sách cụm từ để chứng minh thuộc tính nội dung, rồi sửa văn bản theo chẩn đoán đọc thiếu nguồn mà không sửa/giới hạn phép đo. Đây là cơ chế lượt 1, giữ nguyên slug; không mở lớp META riêng để đếm lại cùng thiếu sót nghiệm thu.

BẢNG THỂ HIỆN:

| tệp:dòng | khai | đo |
|---|---|---|
| `EVIDENCE.md:49` | A7 ĐẠT vì doctrine-scan rc=0 | Gốc xanh; chép nguyên §12 đỏ rc=6; chép câu trần từ ADR-0043 vẫn xanh rc=0. A13 còn cho phép chép toàn §5.1 mà vẫn rc=0. Nhánh làm ĐỎ bắt buộc chưa có răng |
| `EVIDENCE.md:11` | Gốc cả năm là không đọc r1, nên đọc r1 và viết lại hai khối là vá theo lớp | R2 A13:116–120 đã ghi rõ phép chép trần/§5.1 ⇒ ĐỎ; lớp scanner không cần r1 mới biết nghĩa vụ. Sau khi khai đọc r1, EVIDENCE vẫn tự phán A7 bằng đúng rc=0, và cả hai phản chứng cũ vẫn sống |

VẤN ĐỀ: Bốn lớp nội dung cũ tương thích với giải thích đọc thiếu M1/M3/M5/M6 chi tiết. Lớp đo doctrine thì không được lời khai ấy giải thích đầy đủ: nó có yêu cầu trực tiếp trong r2 và cần phép âm khác với việc viết lại hai khối. Không thể xác minh sự kiện tâm lý “đã/không đọc” từ Git; kết luận ở đây là **chẩn đoán một gốc không đủ và sửa theo chẩn đoán ấy chưa đóng cơ chế**, không phải cáo buộc executor nói dối. Việc r1 tự khẳng định scanner đã có răng cũng là lời khai phải đo, không phải căn cứ nhận ĐẠT.

ĐÃ THỬ VÁ: không — trong bằng chứng nghiệm thu, bỏ tự phán A7/A13 đầy đủ từ rc=0 và tách chẩn đoán lớp đo khỏi bốn thiếu sót nội dung. Cần đo dương/âm của cả hai nhánh SPEC; nếu bắt buộc chính scanner phải đỏ thì cần chủ kho cấp phạm vi/dependency cho công cụ, vì write set hiện không có packet_loop.py. Không tự vá scanner ngoài hợp đồng. Một phép đọc bổ sung chỉ thay thế được yêu cầu scanner khi chủ kho sửa nghiệm thu tương ứng; không lén hạ A7/A13.

ĐÃ THỬ NGHIỆM: `python3 probes/acceptance.py`: gốc rc=0; chép §12 rc=6; chép trần rc=0; chép §5.1 rc=0. Các đoạn được lấy nguyên từ mirror; đã phục hồi byte gốc. Output đầy đủ: `probes/A7-copy-section12.txt`, `probes/A7-A13-copy-cap.txt`, `probes/A13-copy-section5.1.txt`. Ca khóa: bản gốc và con trỏ thuần xanh, mỗi bản chép đỏ riêng. Rủi ro: chỉ thêm từ khóa của hai mẫu sẽ đóng hai câu nhưng vẫn chưa chứng minh mọi cách chép nghĩa; phải khai giới hạn phép đo.

ĐỘ TIN: cao.

### bien-goi-y-thanh-menh-lenh  [P2]  Bảng vòng vá buộc executor thực hiện đúng phương án của reviewer

CƠ CHẾ SINH LỚP: Chuyển dữ liệu bàn giao thành quyền quyết định cách triển khai. Đây là lớp **mới**, khác thiếu cột/thiếu bước ĐỌC của lượt 1: bảng có thể đầy đủ và đã được đọc mà vẫn ép sai authority. Không dùng slug này để đổi tên lớp cũ đã vá.

BẢNG THỂ HIỆN:

| tệp:dòng | khai | đo |
|---|---|---|
| `.claude/skills/work-packet/SKILL.md:131` | Với lớp P1/P2 khai bản vá theo lớp, “thực hiện ĐÚNG bản vá theo lớp ấy” | Protocol:448–450 nói gợi ý không phải chỉ thị, người vá được làm khác; §8:520–523 buộc executor tái dẫn xuất, tự đo. Một cách sửa khác đóng cùng lớp và giữ acceptance được protocol cho phép nhưng hàng mới không cho phép |

VẤN ĐỀ: M3 đòi có phương án đóng lớp hoặc lý do vá lẻ, không cấp cho reviewer quyền ra lệnh về implementation. Ví dụ reviewer đề nghị sửa bộ đọc; executor đo được sửa bộ sinh đóng toàn bộ lớp và tránh lặp logic. Nghĩa vụ đọc bảng vẫn giữ, nhưng executor phải được chọn cách khác với lý do/evidence. Lỗi xuất hiện trong dòng mới, không phải chỉ là mâu thuẫn nền có sẵn.

ĐÃ THỬ VÁ: không — sửa riêng hợp đồng hành động work-packet: phải đọc, tái dẫn xuất và đóng cả lớp; khác gợi ý thì giải thích và đo lại. Giữ cột remediation và điều kiện M4, không biến quyền làm khác thành quyền quay về vá lẻ không lý do.

ĐÃ THỬ NGHIỆM: `python3 probes/hunt.py 6` in hai nghĩa vụ trái nhau và ca quyết định bộ đọc/bộ sinh. Đây là phép đọc phản chứng, không giả chạy executor. Ca khóa sau vá: phương án khác có bằng chứng đóng lớp được chấp nhận; chép nguyên hint nhưng chưa tự đo vẫn không đạt. Rủi ro: nới câu quá rộng làm mất trách nhiệm đóng cả lớp, nên phải giữ điều kiện đầu ra và evidence.

ĐỘ TIN: cao.

## BẢNG LỚP

| lop_loi | các slug thuộc lớp | bản vá theo lớp hoặc lý do vá lẻ |
|---|---|---|
| `sai-dai-luong-hoi-tu` | `sai-dai-luong-hoi-tu` | Định nghĩa thống nhất miền/đơn vị M5; hai thể hiện không vá bằng hai ngoại lệ rời |
| `phep-do-doctrine-khong-du-rang` | `phep-do-doctrine-khong-du-rang` | Sửa chẩn đoán và hợp đồng bằng chứng; chạy đủ phép âm, xử lý scope công cụ với chủ kho |
| `bien-goi-y-thanh-menh-lenh` | `bien-goi-y-thanh-menh-lenh` | Phân biệt nghĩa vụ đóng lớp với quyền chọn phương án, giữ tái dẫn xuất và tự đo |

`findings_ids`: [`sai-dai-luong-hoi-tu`, `phep-do-doctrine-khong-du-rang`, `bien-goi-y-thanh-menh-lenh`].

Đếm hiện hành: **0 P1 + 3 P2 + 0 P3 = 3 LỚP; 5 THỂ HIỆN**. Mỗi hàng thể hiện thuộc đúng một lớp. Hạng lượt trước được giữ làm lịch sử, không cộng vào hạng hiện tại.

Reviewer: Codex/OpenAI, phiên độc lập với executor Claude; execution surface: Codex service, transport: machine, shell cục bộ trong sandbox. Không dùng tài khoản đăng GitHub để suy danh tính reviewer. Review hai trục spec và standards/protocol trên exact SHA đầu tệp. Không đăng PR, không commit, không sửa nguồn ngoài sandbox. Mirror đã phục hồi sạch. `VERDICT.md` này là nguồn có thẩm quyền theo chỉ thị người dùng.

**Không approve lượt 2.** Các giới hạn ngoài sandbox không được tính thành pass hoặc thêm finding suy đoán. Việc sửa công cụ ngoài write set cần điều phối xử lý, không phải quyền được cấp bởi verdict này.
