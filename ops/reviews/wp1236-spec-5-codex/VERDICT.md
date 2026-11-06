Đã review tại HEAD `05a1adaa60a746f791c9810cfbbd9bb2d99d9a65`, tree `abe414e099df505abf7684bf1daa68e1c9d70dbc`. Không gọi mạng; đối chiếu đầu/cuối 12.874 tệp không có delta, Git sạch.

Bằng chứng: [số đếm](work/census.json), [workflow và job thật](work/workflow.json), [kết quả chạy](work/checks.json), [đối chiếu K7](work/k7.json). Module mới chưa tồn tại nên các nhận xét về nó là kiểm hợp đồng đặc tả. N1/N2 chỉ được đối chiếu theo mô tả đã cấp; chưa xác minh lại nguồn gốc và các lease ngoài clone.

# VERDICT wp1236 r5 vòng 5

spec_sha256: 9e1ffa3e94c716b77626ce254ce463c0cdfcd5c1c62b2eb3071a8ce2f7603f34

## Finding vòng 4 của tôi

- F01: ĐÓNG — K5 vẫn đối chiếu danh tính và chọn luật từ provenance.
- F02: ĐÓNG — Neo bắt buộc attempt, không thừa kế và phải khớp head.
- F03: ĐÓNG — Bước vẫn ghép theo tên REST/YAML.
- F04: ĐÓNG — K3 bác T/J rỗng và tập chỉ có `chuan-bi`.
- F05: ĐÓNG — Định nghĩa lời khai được giữ; các số cập nhật đã đo khớp.
- F06: ĐÓNG — Bốn loại dấu hiệu giữ đủ ngữ nghĩa đã yêu cầu.
- F07: ĐÓNG — C1–C3 và quy tắc loại tín dụng đột biến giả được giữ.
- F08: ĐÓNG — Phạm vi cột neo rõ; K1 vẫn bác head rút gọn.
- G01: ĐÓNG — Ghép được 43 bước luật trên 22 job thật.
- G02: ĐÓNG — Thiếu attempt, thừa kế neo và head khác vẫn bị chặn.
- G03: ĐÓNG — Miễn trừ tính theo băm; đo lại được 25 khớp, 3 mất.
- G04: ĐÓNG — A4a vẫn canh trực tiếp phép so tên.
- G05: ĐÓNG — Theo chính sách chủ kho, readback phải có dòng `mien_gate_output` đúng SHA/OS/ngày; comment thật pr1130 không có dòng ấy, bị loại.
- G06: ĐÓNG — K2 vẫn kiểm miền hiệu lực của luật.
- G07: ĐÓNG — Lời khai phụ `not_measured` vẫn được phép qua B8.
- G08: ĐÓNG — Mô phỏng vị từ r5 trên `F-that` cho 0 bước bị chặn; `chan_buoc` cũ chặn 19 job.
- G09: ĐÓNG — Phân loại land độc lập token; B9/B11 giữ kiểm lời khai hỗn hợp và thiếu neo.
- G10: ĐÓNG — `tom` chọn luật theo run lịch sử, có T6.
- G11: ĐÓNG — Giới hạn OS được giữ và ví dụ pr1127/pr1128 đã sửa thành dispatch `ci.yml`.
- G12: ĐÓNG — Tự kiểm sổ luật và đột biến T3 vẫn được giữ.
- G13: ĐÓNG — Đã bỏ các cột số đếm sai của bảng ba dạng tệp.
- G14: ĐÓNG — A22 chuyển sang đường dẫn nguồn và hook loader, có hai đối chứng package/direct-load.
- G15: ĐÓNG — D8 thêm vế dương đủ ba tệp; m-D8a làm vế này nhận rc 8 thay vì rc 0.

## Findings mới

- id: G16
  severity: P2
  vi_tri: SPEC.md dòng 202–206, A23 dòng 614, B15 dòng 660
  van_de: Biến thể `duong_nhanh` đòi hai điều không thể thỏa cho `gate-cong-cu-gop`, khiến run đường nhanh thật không thể đạt.
  bang_chung: "`python -B work/measure.py workflow` ⇒ run push master 41397205258 có 14 job J; `gate-cong-cu-gop (ubuntu-latest)` success nhưng số bước liệt kê trong cả YAML và REST đều bằng 0. Bước gộp tại `ci.yml:676` không có `if:` theo chế độ, nên dòng 206 còn buộc giữ marker `SỐ LIỆU GOM…` của `day_du`. `python -B work/checks.py` chạy đường gộp nhanh ⇒ rc 0, output `GOM: KHÔNG ĐO…`, `gop_day_du_marker_matches=False`."
  de_xuat: Chỉ đòi bước liệt kê ở những job thực sự có bước ấy; quy định riêng marker đường nhanh của `gate-cong-cu-gop`. Giữ job này trong J và các chốt K3/K5/K7. F-nhanh/A23/B15 phải chứa đầy đủ tập job thật; thêm đột biến khôi phục marker đầy đủ hoặc đòi bước liệt kê không tồn tại để làm chính ca dương đỏ.

- id: G17
  severity: P2
  vi_tri: SPEC.md dòng 242–245, 362–371 và D2b dòng 381
  van_de: Điều kiện lời khai land phải thuộc sự kiện `push` chưa được thi hành ở D2b, nên M8 vẫn có thể đóng bằng một run dispatch chỉ được đặc tả coi là bằng chứng phụ.
  bang_chung: "K1 cho phép `{push, workflow_dispatch}`; D2b(a) chỉ đòi `kiem == passed` và so run/attempt/head, không đòi event `push` hoặc phân loại lời khai land. D1–D9 cũng không có ca bác dispatch. Vì vậy một bằng chứng dispatch hợp lệ, cùng merge SHA và khớp `ci_master`, thỏa D2b dù không thể làm lời khai land duy nhất theo L-7. Đây là đối chiếu hợp đồng, chưa chạy mã mới."
  de_xuat: Tại D2b(a), đòi provenance thuộc `ci.yml` và event `push`, dùng cùng quy tắc phân loại với L-7. Thêm ca dương push và ca âm dispatch cùng head; đột biến bỏ kiểm event phải làm ca âm đỏ. Giữ khả năng kiểm bằng chứng dispatch phụ ở API `kiem`.

- id: G18
  severity: P2
  vi_tri: SPEC.md dòng 515, 523–531
  van_de: Khối nâng trần lên 900 dòng vẫn neo hiệu lực vào duyệt `spec_hash r4`, trong khi r4 chỉ xin 750 dòng.
  bang_chung: "`rg -n 'spec_hash r4|Ước 520–700|tran_moi' SPEC_R4.md SPEC.md` ⇒ r4 dòng 438: 750; r5 dòng 530: 900; cả hai vẫn ghi hiệu lực khi duyệt r4. `can_cu` r5 còn giữ ước 520–700, trái bảng mới 640–840."
  de_xuat: Neo `ai_nang` vào việc chủ kho duyệt băm của bản sửa hiện hành, đồng bộ khoảng ước và lý do tăng phạm vi. Trước cấp lease, kiểm revision/băm được duyệt cùng cặp trần; approval r4 không được cấp mức 900 của r5.

## Đã đo lại, khớp

- Đo ngày 06-11-2026, khoảng 01:55–01:59 UTC: **126** hồ sơ; **31/37** hồ sơ/tệp provenance; **121** hồ sơ có `merge_commit` gốc.
- **67** giá trị lời khai = **47·1·3·1·9·6**; **49** hồ sơ có lời khai; **39** hồ sơ trượt L8 hồi tố.
- L5 **25 khớp / 3 mất**; L-6 **52 DAT**, trong đó **17** không có lời khai; không có tệp `gate_output/2`, nên **52** hồ sơ trượt L-7 hồi tố.
- `ops/land/` không đổi giữa `4f03566` và HEAD; ba hồ sơ thêm là pr1229, pr1230, pr1242.
- `ENV_JOB_CHO_PHEP` đúng ba khóa; 22/22 job J của pr1231 có checkout passed cùng SHA `fe84620f897913c7f6c2ce5a0c7316a49655e82f`.
- K7 trên `F-that`: 43 bước, 22 job, 0 lệch ghép, 0 bước bị vị từ mới chặn, 0 cờ ống thiếu pipefail.
- Dòng in `kiem-re` đúng `ops/ci_duong_nhanh.py:766`; lane LAND đúng `ci.yml:500–501`. Các bước đường nhanh đã đối chiếu; ngoại lệ sai nằm ở G16.
- Hai cổng nền rc 0: `101 ĐẠT · 25/28 miễn trừ · 0 vi phạm` và `52/52`; `doctrine-scan` rc 0.
- Băm SPEC khớp bản trong kho; clone không nông; diff với base chỉ thêm đặc tả r5.

KET_LUAN: changes_requested