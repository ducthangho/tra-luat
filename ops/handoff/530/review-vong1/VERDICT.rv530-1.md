verdict: changes_requested
reviewed_sha: a1c7d7ffbac710346400650b94e2d2a8035f62b5
vong: 1/10
so_p1: 0
so_p2: 4
so_p3: 2
so_no_ngoai_write_set: 4

Trạng thái: hoàn tất review offline trên exact SHA nêu trên.
Reviewer: OpenAI Codex / GPT-6, execution surface: Codex service, transport: machine; review độc lập với executor Claude.
Chỉ chạy offline trên Linux; full CI và Windows: KHÔNG ĐO ĐƯỢC.

Bằng chứng cổng đang thu thập (`python3 ket-qua/run_gates.py`, PATH ghim `cong-cu/`):
- `--chi-ca=t161`: `catalog 512: mẫu số=16, giết=16, không giết=0, KHÔNG ĐO ĐƯỢC=0`; rc=0, 49.663s.
- `--chi-ca=t162`: `control 512: 10/10 ca đúng phân hạng`; rc=0, 2.241s.
- SHA đặc tả revision 3 đo qua `git show ... | sha256sum` đúng `47c3b1fe70da6976cf802436fa8883c2ba48ac8f706b3d9ec103deaeb5f37778`.
- `--chi-ca=t163`: đạt 7/7, rc=0, 53.788s.
- Wrapper nguyên lệnh: rc=5 trước suite, `tar: actionlint: Cannot change ownership to uid 1001, gid 996: Invalid argument`. Đây là giới hạn sandbox; A5 ở lần này KHÔNG ĐO ĐƯỢC. Đang chạy lại với `TAR_OPTIONS=--no-same-owner`, cùng gói offline và mã nguồn.
- A5 chạy lại: `TAR_OPTIONS=--no-same-owner AL_VER=1.7.7 AL_GOI=<gói offline> bash ops/chay_lease_publish_test.sh`: rc=0, 316.407s. `python3 ket-qua/verify_gates.py` rc=0: ba dòng CHA/A/B đều 158/158, đã chạy=158, bỏ qua=0; 0 dòng `^  ĐỎ  `. Log: `logs/wrapper-no-same-owner.log`.
- A6: doctrine-scan rc=0 (7 tệp, 0 chỗ chép); adr-song rc=0 (48 ADR/48 dòng, ngoại lệ trạng thái ADR-0016 có khai trong output).
- A7: numstat đúng `802 61 ops/lease_publish_test.py`, một đường; dư 198 so trần đã cấp 1000.

## vat-hoa-tuong-duong-qua-rong — P2

**Có.** Hai phép vật hoá chỉ tương đương trên control hiện có ở lần đọc đầu; kết luận tương đương toàn bộ trong `doc_kenh` (:6592–6600), bảng M5 (:7045–7055), prompt và BANG_KHAI #22 rộng hơn phép đo. Chúng có đầu vào phân biệt, và mục gỡ CẢ HAI bỏ sót hai đường đó.

Phép đo: `python3 ket-qua/probe.py declared` và `python3 ket-qua/retry_materialize.py`, cả hai rc=0. Log `logs/declared.log`, `logs/retry-materialize.log`; nguồn và cặp đột biến lưu trong hai script.

**Hai thể hiện độc lập:**
1. Giữ control dương có sẵn, chạy `main()` thật hai lần; seam `doc` đọc kênh thật rồi cho lần đầu KDD để đi đường retry. Bản gốc: `real_readings=[GIET,GIET]`, kết quả GIET. Chỉ gỡ tuple ở `_ten_day_du_512`: `[GIET,KHONG_DO_DUOC]`, kết quả KDD với `đích RỖNG`. Tuple ở `doc_kenh` không cứu được iterator đã tiêu thụ ở lượt đầu.
2. Kênh do `main()` thật chạy t160 nguyên trạng sinh ra: rc=0, `1/1`, nhãn DAT (`logs/live-main.jsonl`). Đọc bằng `dich=iter(tên ca thật)`: bản gốc KHONG_GIET; chỉ gỡ tuple ở `doc_kenh` thì GIET dù không ca nào đỏ. Đây là đường gọi bộ đọc trực tiếp; không khai rằng caller `_chay_mot_mutant_512` hiện tại truyền iterator.

Đồng thời đã tái lập đúng lời khai hẹp: gỡ riêng từng nửa rồi chạy t162 hiện có vẫn 10/10, rc=0; gỡ cả hai làm control dương lệch GIET→KHONG_GIET, t162 rc=1. Những số này đúng; suy luận “một bộ tương đương” không đúng trên toàn giao diện/đường retry.

Đề xuất: trong chính tệp test, thêm tự kiểm riêng cho retry tiêu thụ iterator và bộ đọc nhận iterator trên kênh DAT thật; chỉnh lời khai về phạm vi tương đương. Khóa bằng việc gỡ riêng mỗi tuple phải làm ca tương ứng đỏ. Rủi ro khi vá: không đổi tập đích thành iterator mới mỗi lần theo cách che mất dữ liệu cấu hình; giữ 155 ca cũ và trần +1000.

## stdout-giai-ma-lam-mat-phep-do — P2

**Có. Một thể hiện đã đo.** `_chay_mot_mutant_512` (:6938–6944) vẫn buộc stdout/stderr giải mã văn bản bằng `text=True`, dù phân hạng đã chuyển sang JSONL và không dùng hai chuỗi đó. Ngoại lệ giải mã thoát ngoài khối chỉ bắt `TimeoutExpired`, làm mất cả phân hạng lẫn lượt retry M3.

Phép đo: `python3 ket-qua/probe_transport.py`, rc=0, `logs/transport.log`. Đột biến chỉ thêm một byte không UTF-8 vào hàm nhật ký stdout, giữ điều kiện ca và kênh JSONL. Dùng control dương t160 có sẵn:

```
escaped UnicodeDecodeError attempts 1
actual_main_rc 1 channel_reading ('GIET', '')
```

Lượt `main()` thật đã chết bằng `TinHieuChotCa`, phát `DO_CHOT` và đóng rc=1 (`logs/transport-real-channel.jsonl`), nhưng đường chạy mutant không trả được trạng thái và chỉ thử một lần. Đây là một phép đo bị mất; không phải `KHONG_GIET`, cũng không phải retry KDD đúng hợp đồng.

Đề xuất: nhận stdout/stderr dưới dạng byte hoặc dùng chế độ giải mã chẩn đoán không ném; phân hạng chỉ đọc JSONL. Với lỗi vận chuyển thực sự, đưa về KDD và retry đúng một lần. Khóa bằng chính control thật có nhật ký không giải mã được, đòi GIET qua kênh; thêm kiểm số lượt với lỗi vận chuyển còn lại. Rủi ro: không dùng `errors=replace` cho chính kênh JSONL, vì sẽ che kênh hỏng.

## m5-van-cham-chet-bang-chuoi — P2

**Có. Sáu thể hiện (sáu mục DO) trong cùng một lớp.** `t163` (:7125–7169) bỏ kênh JSONL của lượt t162 con, rồi nhận diện “giết đúng” bằng `"  ĐỎ  t162" in ra` và dòng bắt đầu `"  LỆCH"` chứa tên control. Lớp lỗi đọc chuỗi của F6 vẫn tồn tại ở tầng tự kiểm, nên lời khai M6 “bộ chấm thôi đọc hình dạng chuỗi” chưa đúng cho toàn bộ bộ chấm.

Phép đo: `python3 ket-qua/probe.py m5_unrelated_exception`, rc=0; log `logs/m5-unrelated-probe.log`. Thay đúng chốt cuối t162 từ `chot(not lech, …)` thành `if lech: raise Exception(…)`, giữ mọi điều kiện và kết quả control. Chạy t163 thật trên bản sao:

```
sáu mục DO: GIET
tự kiểm bộ chấm 512: đạt 7/7
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
rc=0
```

Đo riêng lượt con với cùng một mục M5: t162 rc=1, dòng đỏ ghi `Exception: control LỆCH phân hạng`; JSONL thật do `main()` phát ghi **`nhan=DO_KHAC`**, không phải DO_CHOT (`logs/m5-exception-real-channel.jsonl`). Tuy vậy t163 đã cấp GIET. Chưa cần giả tên ca, giả kênh hay sửa trạng thái khung: chỉ đổi loại ngoại lệ tại điểm mà bộ chấm phải phân biệt.

Đề xuất: cho tầng M5 nhận kết quả t162 bằng kênh có nhãn/neo/rc và kiểm đúng tín hiệu, kèm kết quả control có cấu trúc; tránh suy nguyên nhân từ dòng chẩn đoán. Khóa bằng phản chứng đã chạy: Exception/raw AssertionError ở t162 phải khiến tự kiểm đỏ, còn TinHieuChotCa đúng chốt vẫn được nhận. Rủi ro: giữ hai cực DO/XANH, không làm mất phép bất biến A2 hoặc đếm một lỗi hạ tầng là đã giết mutant.

## control-bo-sot-chot-va-trang-thai — P2

**Có. Đã đo được 9 thể hiện ngoài danh sách 9 đã khai.** `CHOT_CHUA_CO_CONTROL_512` (:7059) là số phần tử của một danh sách chưa đủ, không phải kiểm kê đầy đủ những chốt chưa được canh.

Phép đo: `python3 ket-qua/probe.py guards`, `python3 ket-qua/probe.py uncatalogued`, `python3 ket-qua/probe.py widen_raw_assertion`; các driver rc=0. Log `logs/guards.log`, `logs/uncatalogued.log`, `logs/widen-raw-assertion-probe.log`.

1–7. Gỡ đồng thời các kiểm tra sau, t161 vẫn **16/16**, t162 **10/10**, t163 **7/7**, cả ba rc=0:
- bản ghi sau đóng lượt (:6636);
- neo sai phiên/mutant/lần thử (:6638);
- bản ghi vừa có tên ca vừa đóng lượt (:6647);
- thiếu tên ca (:6653);
- rc đóng lượt phải int và không phải bool (:6672);
- kênh không có ca nào (:6676);
- vỏ `doc_kenh` bắt ngoại lệ bất ngờ (:6606).

Sáu điều kiện trong bộ đọc còn được gỡ riêng, mỗi lần t162 vẫn 10/10 rc=0. Không gộp chúng thành “7 chốt độc lập”: một số có thể được chốt sau hấp thụ. Kết luận đã đo là **chúng không được catalogue/control/tự kiểm hiện tại phân biệt**, và không nằm trong danh sách 9. Ngoài ra còn kiểm tồn tại/đọc được tệp; chưa dùng số lượng nhánh làm bằng chứng độc lập.

8. Comment :6874 khai một mutant M5 tên `noi-AssertionError-thanh-DO_CHOT`, nhưng bảng không có mục ấy. Nới nhánh main cho đúng kiểu `AssertionError` trần nhận DO_CHOT (giữ TinHieuChotCa rơi nhánh này theo quy tắc cũ khi mục đổi-except chạy): t162 **10/10**, t163 **7/7**, rc=0. Tập control không có ngoại lệ AssertionError trần để phân biệt trường hợp M1b cấm; control dương t96 đã đổi chính nó sang chot.

Đề xuất: bổ sung tự kiểm cho các lớp trạng thái bị thiếu, dùng kênh sinh qua main thật; kiểm kê theo hành vi phân biệt được, khai rõ các nhóm bị chốt khác hấp thụ. Thêm control riêng cho AssertionError trần, giữ M1b t96 dương. Nếu phải đổi mẫu số đã đóng băng, trình điều phối xử lý revision; không tự nới đặc tả. Rủi ro: đếm số nhánh/mutant thay cho số hành vi độc lập sẽ tái tạo đúng lỗi kiểm kê này.

Bổ sung nghiệm thu: A2 chiều ngược đã tái lập (`python3 ket-qua/probe.py a2_reverse`): A2 `XANH_SAI`, rc con `[1,1]`, t163 6/7, rc=1. Đây là bằng chứng có răng thật của mục A2, không xóa các lỗ ở các cực/kênh khác.

Bổ sung thể hiện 9 cho `control-bo-sot-chot-va-trang-thai`: **không có control đòi KHONG_GIET** (8 KDD + 2 GIET). `python3 ket-qua/probe.py live_false_credit` gỡ điều kiện phải có ca đỏ tại điểm cấp GIET (`if not do_chot or do_chot == set(dich)`): t161 16/16, t162 10/10, t163 7/7, cả ba rc=0. `python3 ket-qua/probe_live.py` rc=0 đọc đúng kênh DAT/rc=0 đã sinh qua main thật: bản gốc KHONG_GIET; bản đột biến GIET. Log `logs/live-false-credit-probe.log`, `logs/live-reader.log`. Cần control sống sót/no-op có đích không rỗng, đòi KHONG_GIET. Đây là điểm mù một trong ba trạng thái, không nằm trong 9 chốt đã khai.

## mo-ta-thua-ke-kenh-sai-duong-chay — P3

**Có. Một thể hiện, lặp ở nhiều hiện vật.** Comment `_mo_kenh` (:6566–6574), commit 540b6f1 và handoff nói con của t155 “chạy TRỌN 157 ca” khi gỡ selector, dùng chuyện đó giải thích kênh bị ghi tiếp. Con số 157 cũng không có mục riêng trong BANG_KHAI.

Phép đo: `python3 ket-qua/probe.py inheritance`, driver rc=0, t161 rc=1. Đã tái lập đúng **15 GIET / 1 KDD** và lý do `có bản ghi SAU bản ghi đóng lượt`. Nhưng kênh thật (`logs/inherited-channel-1.jsonl`, lần 2 tương tự) chỉ có **3 bản ghi ca và 4 bản ghi đóng**: t01, t01, t155. Lượt con selector sai in **0/0, rc=0**; không chạy 157 ca. Các lượt t01 hợp lệ đã làm nhiễm kênh trước đó. Cùng tổng 15/1 không chứng minh câu chuyện về các số hạng/đường chạy.

Đề xuất: chỉnh comment trong write set theo đường đã đo (hai lượt t01 thừa kế kênh; selector sai chạy 0 ca), ghi rõ nếu 157 là một bản nháp khác cần log/source riêng. Commit/handoff cũ chỉ đính chính ngoài packet, không sửa lịch sử. Khóa bằng kiểm tập tên và số bản ghi từ chính phép gỡ môi trường, không chỉ tổng catalogue. Rủi ro: thay “157” bằng “158” sẽ tiếp tục sai vì lỗi ở đường chạy, không phải cập nhật số ca.

## phan-ra-dong-them-khong-phai-so-do-chinh-xac — NỢ

**Có chênh lệch số; không diễn giải ước lượng đã ghi `~` thành lời khai chính xác. Bốn thể hiện.** Phạm vi: BANG_KHAI #15, hai commit message, bảng handoff và bản chiếu lease — ngoài write set. Theo yêu cầu “mỗi con số đo khác là finding”, ghi đủ các số hạng, không đòi packet sửa các hiện vật ngoài phạm vi.

Phép đo: `python3 ket-qua/count_claims.py`, rc=0; `logs/count-claims.log`. Phân loại từng dòng THÊM theo diff -U0: dòng trống, dòng bắt đầu `#`, dòng thuộc docstring xác định bằng AST, còn lại là mã/dữ liệu Python. Danh sách số dòng và loại lưu ở `logs/added-lines-*.json` để đổi quy tắc đếm nếu cần.

| Mốc | Chú thích | Trống | Docstring: khai → đo | Mã/dữ liệu: khai → đo | Tổng |
|---|---:|---:|---:|---:|---:|
| 540b6f1 | 137 | 67 | ~87 → 89 | ~470 → 471 | 764 |
| a1c7d7f | 148 | 67 | ~90 → 89 | ~497 → 498 | 802 |

Hai số không xấp xỉ 148 và 67 đúng; hai số cuối ở HEAD lệch ±1 trong phạm vi “đo thô”. Kết luận “cắt hết văn vẫn vượt 300” vẫn đúng. Ở commit đầu, bốn số khai cộng 761 chứ không phải 764; các ước lượng không được dùng như phân rã chính xác.

Đề xuất ngoài packet: công bố quy tắc phân loại và bảng exact theo AST, gắn đúng SHA; hoặc giữ ký hiệu xấp xỉ và không nói tổng thành phần là một phép cộng exact. Kiểm bằng script trên. Rủi ro: chuỗi dữ liệu trong catalogue không phải docstring; chuyển hết chuỗi đa dòng sang “văn” sẽ làm sai đại lượng mã cần giữ.

## neo-blob-cua-mau-so-493-sai — NỢ

**Có. Một thể hiện**, tại đặc tả rev 3 và BANG_KHAI #25, ngoài write set. Con số 493 đúng trên tệp của commit 36f68c7, nhưng tệp ấy không có blob `13a2af8c…` như lời khai.

Phép đo (log `logs/blob-anchor.json`):
- `git -C kho-guong.git rev-parse 36f68c7:ops/lease_publish_test.py`: rc=0, **5acd563297fea3b8e37dedcd750acd8794d68bec**.
- `git -C kho-guong.git cat-file -t 13a2af8c`: rc=128, `Not a valid object name`.
- `python3 ket-qua/count_claims.py`: rc=0, **493** lời gọi bang/chot trên blob thật.

Đề xuất điều phối: đính chính nguồn neo ở revision/hồ sơ được phép; không sửa đặc tả đóng băng trong PR này. Test khóa: đối chiếu OID từ `rev:path` trước khi kiểm số lượng. Rủi ro: giữ một tổng đúng rồi coi nguồn trích cũng đúng sẽ che việc đang đo nhầm phiên bản. Nội dung blob mang tiền tố đã khai: KHÔNG ĐO ĐƯỢC trong gương; không kết luận blob đó chưa từng tồn tại nơi khác.

## dem-cau-truc-sai-don-vi — P3

**Có. Ba thể hiện theo lời khai; riêng lời khai về neo sai trên 16 mục.** Các lời khai nằm ngay trong write set, còn số tương ứng bị BANG_KHAI bỏ sót.

Phép đo: `python3 ket-qua/count_extra.py`, rc=0, `logs/count-extra.log`; script đọc AST và dùng chính các chuỗi neo trong catalogue/control, không tự soạn payload.

1. `_mo_kenh` (:6565) nói sinh tiến trình con “của CHÍNH nó ở 18 chỗ”. Có 18 biểu thức AST `sys.executable`, nhưng chỉ **5** vị trí mảng lệnh gọi chính tệp/bản sao test: 4287, 5848, 6303, 6940, 7133. 13 chỗ còn lại: 3 lệnh gọi mã sản phẩm, 6 lệnh fixture inline, 1 tệp fixture khác, 3 tham chiếu không phải lệnh sinh tiến trình. Đếm biểu thức không bằng đếm lần tự gọi. Điều này không phủ nhận nguy cơ sửa tệp giữa suite; cảnh báo ấy vẫn đúng.
2. Comment :6727 nói “Hai vùng cắt”, docstring :6757 nói “ngoài hai bảng”; `_VUNG_CAT_512` thật có **3** vùng. Hai chỗ văn trôi trong cùng một thể hiện.
3. Comment :6720 và commit 540b6f1 nói **mỗi neo xuất hiện ít nhất hai lần** do bảng nằm trong tệp. Đếm nguyên chuỗi trên 26 mục: **16 mục khớp 1 lần, 8 mục khớp 2 lần, 2 mục khớp 3 lần**. 16 neo không thỏa cận dưới đã khai, vì escape trong literal nguồn không bằng giá trị chuỗi lúc chạy. Phép cắt vẫn cần: hai control dương không cắt thực sự khớp 3/2 và làm 8/10, đã tái lập; lý do phổ quát “mọi neo” sai.

Đề xuất: chỉnh lời khai về đúng đơn vị (biểu thức/vị trí tự gọi; 3 vùng; chỉ một số neo va chạm), dùng cùng script đếm đã ghi. Không cần thay cơ chế cắt đúng chỉ để hợp với văn. Rủi ro: grep toàn nguồn đếm cả chuỗi fixture và chú thích, dễ tạo một tổng mới tiếp tục sai.

## bang-khai-bo-sot-dai-luong — NỢ

**Có. 39 thể hiện đã liệt kê**, ngoài các số sai đã có lớp riêng. Phạm vi BANG_KHAI và hồ sơ định lượng, ngoài write set. Danh sách chi tiết có nguồn, phép đếm và giới hạn ở [BO_SOT_SO.md](BO_SOT_SO.md). Ví dụ quan trọng: +764/137/~87/~470 của commit đầu; thời lượng 107.4s tuyệt đối của t125 ở commit đầu khác đại lượng delta +107.4s của HEAD; 4 biến môi trường; 3 vùng cắt; 8 control âm; chiều ngược A2 6/7; các số hạng của mẫu 493.

Phép đo và rc: `python3 ket-qua/count_claims.py`, `python3 ket-qua/count_extra.py`, `python3 ket-qua/spec_counts.py` đều rc=0, log tương ứng trong `logs/`; các phép chạy thật t162/t163, retry và kênh đã dẫn ở các lớp trên. Những số lịch sử thiếu log được đánh **KHÔNG ĐO ĐƯỢC**, không đoán kết quả.

Đề xuất ngoài packet: kiểm kê theo đại lượng + nguồn + exact SHA/lượt đo, giữ số hạng và số âm/0; không chỉ gom tập chữ số hay regex theo đơn vị. Kiểm bằng cách đối chiếu từng dòng đã liệt kê về nguồn. Rủi ro: một danh sách mới vẫn có thể thiếu; không biến số 39 này thành tuyên bố đầy đủ. Nguyên văn PR/comment không có trong bundle nên phần chỉ tồn tại ở hai nguồn đó chưa kiểm được offline.

## thoi-luong-khac-giua-cac-luot-do — NỢ

**Có chênh lệch định lượng; không có bằng chứng regression mới cần PR sửa. Chín thể hiện khác ở độ chính xác đã công bố.** Ghi theo yêu cầu mỗi số trong bảng đo ra khác phải được báo; đây là số đo phụ thuộc lượt/môi trường ở BANG_KHAI/handoff, ngoài write set. Quyết định chấp nhận chi phí ba ca mới được giữ nguyên.

Phép đo: `python3 ket-qua/measure_cost.py`, rc=0. Hai clone từ cùng gương, core.abbrev=7, exact base/head, chạy liên tiếp trong cùng lệnh; cả hai suite đầy đủ, bỏ qua=0, rc=0. `cost/results.json`, `logs/cost-measurement.log` và hai log đầy đủ trong `cost/` giữ giá trị thô.

| Đại lượng | Khai | Đo lại |
|---|---:|---:|
| suite nền | 104.4s | 105.964561s |
| suite HEAD | 319.4s | 317.002692s |
| delta suite | +214.9s | +211.038131s |
| hệ số | ×3.06 | ×2.991592 |
| t125 nền | 53.0s | 54.083s |
| t125 HEAD | 160.4s | 159.517s |
| delta t125 | +107.4s | +105.434s |
| t161, cha wrapper | 49.4s | 49.301s (~49.3) |
| t163, cha wrapper | 53.7s | 53.542s (~53.5) |

`t162` cha wrapper =2.172s, vẫn 2.2 ở độ chính xác bảng. Các số lịch sử 104.4/319.4 và 53.039/160.378 có đúng trong log đã cấp; giá trị chưa làm tròn của **thời lượng toàn suite lịch sử** không được lưu nên không xác minh được +214.9 đến độ chính xác cao hơn. Không dùng 319.4−104.4 đã làm tròn để tuyên bố phép delta lịch sử sai.

Đề xuất ngoài packet: giữ thời lượng thô, SHA và điều kiện theo từng lượt thay vì ghi đè số cũ; nếu cần so hiệu năng như cổng, xác định dung sai và cách lấy mẫu. Không đề nghị skip ba ca trong t125 hoặc thay timeout. Rủi ro: biến nhiễu thời gian vài giây thành finding chức năng sẽ trái quyết định phạm vi đã có. Trong lượt Linux này chưa đo thấy trần thời gian bị vượt; Windows vẫn KHÔNG ĐO ĐƯỢC.

## Đối chiếu bảy mục tự kiểm đã khai

`python3 ket-qua/probe.py declared` rc=0. Mỗi mục DO bên dưới thực sự làm đúng control được khai lệch và t162 đỏ rc=1; điều này xác nhận lời khai hẹp, không bảo đảm tầng chấm M5 không cấp tín dụng giả.

| Mục | Control được khai | Lệch thật |
|---|---|---|
| đổi nhánh except TinHieuChotCa | dương t160 | GIET → KDD |
| bỏ chốt DO_KHAC | Exception trần | KDD → KHONG_GIET |
| đóng lượt rc=0 cứng | dương t160 | GIET → KDD, rc0≠rc1 |
| không ghi đóng lượt | dương t160 | GIET → KDD, thiếu đóng |
| đóng lượt bằng số1 | dương t160 | GIET → KDD, sai kiểu bool |
| gỡ cả hai vật hoá | dương t160 | GIET → KHONG_GIET |
| A2 làm rỗng chi_tiet | trọn catalogue/control | t16116/16, t16210/10, rc=[0,0]; chiều ngược đã làm6/7 và rc1 |

Bốn mục DO có cùng control dương và cùng phép chiếu GIET→KDD. Các **lý do** kênh khác nhau đã được log, nhưng chỉ vector phân hạng đó không chứng minh “bốn chốt độc lập”. Bộ đôi vật hoá đã được mở thêm hai đường phân biệt thật; không nhận lời khai tương đương chỉ từ control một lần đọc.

## Hồi quy, phạm vi và giới hạn cuối lượt

- **Không thấy đổi điều kiện khẳng định của 155 ca cũ**: `count_claims.py` so AST tất cả ca cũ sau chuẩn hoá riêng tên hàm chot/bang cho kết quả `old_case_AST_changes_after_signal_normalization []`. Chín ca đổi đúng59 lời gọi; các đối số/điều kiện giữ nguyên. Hai suite nền và HEAD đều đạt đủ số ca, không bỏ qua. Đây là bằng chứng trên mã và Linux, không phải kết luận Windows.
- **Không thấy thay đổi ngoài write set trong PR**: `git diff --name-status dc02c9b a1c7d7f` chỉ có `M ops/lease_publish_test.py`; numstat +802/−61. Không sửa cây reviewed, spec, lease, workflows hay ops/reviews. Các mutant/bản sao đo nằm ngoài `cay/` và đã kết thúc trước khi chốt verdict.
- Kênh `doc_kenh` nguyên trạng đã phân đúng các đầu vào thật đã chạy; **chưa tìm được tín dụng giả trên chính bộ đọc nguyên trạng trong phạm vi đó**. Các phản chứng trực tiếp GIET cho kênh DAT ở trên đều ghi rõ chốt nào bị gỡ. Tín dụng giả **có thật ở oracle t163** dùng chuỗi; mất phép đo **có thật ở runner** giải mã stdout. Không đánh tráo hai phạm vi kết luận.
- Chống mã cùng interpreter sửa thẳng khung, full CI, Windows, receipt GitHub và tập ref GitHub lịch sử độc lập: **KHÔNG ĐO ĐƯỢC**. Không chạy CI, không dùng mạng, không push.
- Gương xác nhận412 ref =8 heads +365 remotes +39 tags, master2175 commit, không shallow. Số365/365 lúc cấp lease chưa có hai tập độc lập để chứng minh; không lấy đối chiếu gương với chính nó làm bằng chứng.
- Reviewer: OpenAI Codex / GPT-6 qua Codex service, transport machine; độc lập với executor Claude. HEAD cuối lượt vẫn `a1c7d7ffbac710346400650b94e2d2a8035f62b5`, tree `270643b511f3fb8fe0a807f9083c399a1513aa13`; `git status --porcelain` rỗng.

Bảng đầy đủ từng số: [DOI_CHIEU_BANG_KHAI.md](DOI_CHIEU_BANG_KHAI.md). Các số bị bỏ sót: [BO_SOT_SO.md](BO_SOT_SO.md). Giữ verdict **changes_requested** vì 4 lớp P2 và 2 lớp P3 trong write set; 4 lớp NỢ ngoài write set không phải yêu cầu PR mở rộng phạm vi. Không có P1 đã xác nhận.
