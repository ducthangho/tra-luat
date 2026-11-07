Đã review tại HEAD `308a14ac2c944e0209eb410d6cdf52de57ec9f0d`, tree `21eecac0643e2910d3f61e916b1dcd142bffe23d`. Không gọi mạng, không sửa kho; đối chiếu băm 12.375 tệp đầu/cuối không có thay đổi, Git sạch.

Số đo lưu trong [census.txt](work/census.txt) và [probes.txt](work/probes.txt). Module mới chưa tồn tại, nên đánh giá đột biến mới dưới đây là đối chiếu hợp đồng, không phải lời khai đã chạy test triển khai. Không kiểm được nguồn N1/N2 trên nhánh #1240 bằng clone được cấp.

# VERDICT wp1236 r2 vòng 2
spec_sha256: 570b10851be95875662da56df3dcb6d6f028429f4cb2e2f1291c3604eb618a0c

## Finding vòng 1 của tôi

- F01: ĐÓNG — K5 đã buộc tên, nhãn và kết luận khớp provenance, đồng thời chọn luật từ provenance; lỗi nghiệm thu A4 được nêu riêng tại G04.
- F02: CÒN MỞ — D2b đã nối head với merge, nhưng neo bên ngoài vẫn thiếu attempt và L-7 chưa buộc bằng chứng thuộc phạm vi hậu merge; xem G02.
- F03: CÒN MỞ — Đã thêm CMD và đề xuất rc gián tiếp, nhưng phép nối CMD với bước REST của K7 không đúng trên dữ liệu thật; xem G01.
- F04: ĐÓNG — K3 đã cấm tập job rỗng và toàn skipped, kèm A3d/e.
- F05: CÒN MỞ — Định nghĩa mới đã bắt mapping/list/chuỗi tự do, nhưng bảng dạng giá trị và số hồ sơ L8 đổi kết quả vẫn sai; xem G03.
- F06: ĐÓNG — Bốn loại dấu hiệu đã biểu diễn được ngữ nghĩa cũ, kèm fixture phủ đủ mười loại job và A10–A12/A18.
- F07: ĐÓNG — C1 có đột biến riêng, C2/C3 canh việc gỡ L8; A5 chuyển sang yêu cầu ca hậu tố phân biệt được `search` với `fullmatch`.
- F08: ĐÓNG — Cột neo đã giới hạn đúng vào tập job/băm, đồng thời A8 kiểm head rút gọn.

## Findings mới

- id: G01
  severity: P1
  vi_tri: SPEC.md dòng 175–180, 431–438, 600–601
  van_de: K7 bác các bước CI hợp lệ vì đồng nhất tên REST với `Run <CMD>`, khiến đường dương dự kiến không dùng được trên run thật.
  bang_chung: "`python -B work/probes.py`: run 42032872356 có ba bước bắt buộc đều `success`, nhưng `k7_match=false`: `chuan-bi`, `gate-packet-loop`, `gate-registry`; bước chạy `python .claude/dev/packet_loop_test.py` mang tên REST `packet-loop selftest`. `ci_provenance.py:208–212` ưu tiên `name:` của bước YAML, chỉ dùng `Run ...` khi không có tên. F-ok tự dựng tên `Run ...` nên che lỗi này."
  de_xuat: Chốt ánh xạ nhóm log với định danh/tên REST thực của bước, rồi kiểm conclusion; bổ sung fixture từ provenance và header log thật trước khi đóng băng, thay vì giao executor giải quyết sau.

- id: G02
  severity: P1
  vi_tri: SPEC.md dòng 161–162, 224–229, 237–238
  van_de: Neo run vẫn cho phép chọn bằng chứng tự nhất quán nhưng sai attempt hoặc sai phạm vi của kết quả landed.
  bang_chung: "K1 chỉ so attempt với `provenance.attempt_yeu_cau`; Neo run và D2b không so với attempt kỳ vọng của lời khai/`ci_master`. Một lần chạy lại giữ nguyên run_id và head vì vậy chưa được phân biệt. L-7 chỉ đòi lời khai ở bất kỳ độ sâu nào, còn head gần nhất che head tổ tiên: phép đo trên pr1023 xác nhận lời khai pre-merge dùng run 41004664516/head 5b76266d…, khác run hậu merge 41017062295/head 09e05945…; hợp đồng chưa đòi phải có lời khai hậu merge."
  de_xuat: Khai rõ bộ neo kỳ vọng gồm run, attempt, SHA và context; đối chiếu toàn bộ bộ neo, yêu cầu L-7 có bằng chứng hoặc waiver cho phạm vi hậu merge, và từ chối kế thừa qua một context run khác.

- id: G03
  severity: P2
  vi_tri: SPEC.md dòng 69–87, 263–302, 371, 565–566
  van_de: Bảng dạng giá trị đếm thừa bốn chuỗi khác và bảng tác động L8 bỏ sót pr679 đã mất miễn trừ L5.
  bang_chung: "`python -B work/census.py`: 64 giá trị = 44 measured + 1 passed + 3 not_measured + **1** chuỗi khác + 9 mapping + 6 list, không phải 5 chuỗi khác. Có chín hồ sơ thuộc danh sách L5 nhưng chỉ **tám** còn khớp băm; pr679 có băm `e187218b…916c67`, khác băm miễn trừ `f409cacf…1b3be`. Kết quả là **36** hồ sơ L8 đỏ; 35 hàng đã ghi khớp, thiếu pr679."
  de_xuat: Sửa bảng giá trị, thêm hàng pr679 và cập nhật các số tác động/ước lượng/Q1 liên quan; khi tính miễn trừ phải kiểm cả tên lẫn băm.

- id: G04
  severity: P2
  vi_tri: SPEC.md dòng 169–174, 422, 447
  van_de: Đột biến m-A4a không thể làm ca đổi riêng tên job chuyển màu khi chốt so tên của K5 vẫn còn.
  bang_chung: "A4a đổi tên trong tệp nhưng giữ provenance; K5 bắt buộc hai tên bằng nhau nên trả `not_measured` cả trước lẫn sau đột biến chọn luật từ tên trong tệp. Trên đầu vào qua phép so tên, hai nguồn tên lại bằng nhau, nên đổi nguồn chọn luật là đột biến tương đương dưới bất biến này."
  de_xuat: Dùng ca và đột biến riêng để canh phép so tên; bỏ yêu cầu giết đột biến tương đương, hoặc chỉ định rõ đột biến kết hợp cùng đầu vào làm chốt mục tiêu thực sự đổi màu.

- id: G05
  severity: P2
  vi_tri: SPEC.md dòng 218–219, 237, 256–258, 460, 485
  van_de: L-7 nhận `owner_waived` chỉ nhờ hình dạng URL, chưa chứng minh có waiver của owner cho đúng SHA và phạm vi.
  bang_chung: "`ops/kiem_ho_so_land.py:46–47` chỉ kiểm tiền tố URL và fragment; đặc tả nói rõ không kiểm nội dung waiver. A17/B7 vì vậy nhận cả liên kết tới comment không chứa quyết định miễn trừ, trong khi protocol §10.2.3 đòi nguồn/actor, exact SHA, context/OS, lý do và phạm vi."
  de_xuat: Quy định nguồn readback/receipt waiver và kiểm actor, SHA, context cùng phạm vi; có thể thêm bộ kiểm riêng mà giữ nguyên bốn thành phần bị khóa bởi #1210.

- id: G06
  severity: P2
  vi_tri: SPEC.md dòng 124–130, 163, 452
  van_de: Sổ luật chỉ-thêm chưa giới hạn phiên bản được phép áp dụng cho từng run, nên luật cũ có thể tiếp tục hợp thức hóa bằng chứng của run mới.
  bang_chung: "K2 nhận mọi hash còn trong sổ; không điều kiện nào nối phiên bản luật với run hoặc workflow được kiểm. Khi v2 bổ sung bước/dấu hiệu bắt buộc, bộ sinh v1 vẫn có thể tạo tệp cho run mới và được kiểm bằng luật v1; A9 chỉ bảo vệ việc tiếp tục nhận v1."
  de_xuat: Tách lưu phiên bản để kiểm lịch sử khỏi quyền áp dụng cho run mới; bổ sung miền hiệu lực hoặc ánh xạ phiên bản được phép, cùng ca nhận bằng chứng lịch sử và từ chối dùng luật cũ ngoài miền ấy.

- id: G07
  severity: P2
  vi_tri: SPEC.md dòng 237, 583–588
  van_de: Khuyến nghị Q7 cho phép khai run Windows `not_measured` nhưng không nêu rằng lựa chọn ấy làm hồ sơ landed trượt L-7.
  bang_chung: "L-7 đòi MỌI khóa lời khai là dương hợp lệ hoặc `owner_waived`; Q8 nhắc lại việc cấm `not_measured`. Vì vậy một lời khai gate_output Windows `not_measured` vẫn làm trượt hồ sơ dù bằng chứng Ubuntu hậu merge đầy đủ."
  de_xuat: Sửa Q7 để nêu rõ hệ quả và chỉ dẫn nhất quán, hoặc giới hạn L-7 theo context bắt buộc và giữ trạng thái chưa đo của các context khác.

## Đã đo lại, khớp

- SHA đặc tả; HEAD/tree; clone không shallow; diff với origin/master chỉ thêm đặc tả r2, 633 dòng.
- 123 hồ sơ; 28 hồ sơ chứa 34 provenance; 753 job `not_measured`, 1 `failed`; tập job không skipped khớp `log_day_du` ở cả 34 tệp.
- Bảng tên khóa: 42/22/2/1/1; 46 hồ sơ có lời khai, 44 có lời khai khác `not_measured`, tổng 61 lời khai loại ấy; chia 22 có provenance và 22 không có.
- L-7 hồi tố: 49/49 = 32 hồ sơ có lời khai + 17 không có.
- Hai cổng hiện tại đều rc 0: `98 ĐẠT · 25/28 miễn trừ · 0 vi phạm`; `49/49 landed True đạt`.
- LUAT gốc: 10 loại job, 31 bước, 36 dấu hiệu; bảy bản `danh_gia_gate.py` cùng băm.
- Ruff 0.17.3: 1 F841 ở packet_loop, 2 F541 ở test; năm tệp còn lại không lỗi F. Đây là nền rc 1, không phải lint xanh.
- Tỷ lệ kích thước nguồn/test 412/719 và 177/418 khớp; OID hiệu lực ADR-0052/0053 qua ba phép kiểm trên ref cục bộ.
- `doctrine-scan`: rc 0, 10 tệp, 0 chỗ chép doctrine.

KET_LUAN: changes_requested