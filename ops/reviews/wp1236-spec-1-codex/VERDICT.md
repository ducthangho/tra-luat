Đã review tại `b9766fe2cafbede82547a6336ab2a9093084b609`, tree `9d87fe4feb35753b6c8a95b72b666fcafd939606`. Kho không đổi: đối chiếu băm 12.375 tệp và Git status đều sạch. Clone báo shallow, nhưng có đủ ba commit cần kiểm. Không gọi mạng.

Các lỗ thiết kế dưới đây được suy từ hợp đồng đặc tả; module mới chưa tồn tại để chạy. Phép đo lưu trong [census.txt](work/census.txt), [history.txt](work/history.txt) và [spec_probes.txt](work/spec_probes.txt).

# VERDICT wp1236 r1 vòng 1
spec_sha256: d599ff336ac68eb0cb30f36167cf1c9f2beeea04fc2909de7324670b93fa8eee

## Findings

- id: F01
  severity: P1
  vi_tri: SPEC.md dòng 105–112, K3–K5
  van_de: Bộ kiểm chưa buộc tên và kết luận của từng job khớp provenance, nên có thể chọn sai luật hoặc bỏ qua kết luận thất bại.
  bang_chung: K3 đối chiếu tập ID; K4 đối chiếu băm; K5 đọc tên/kết luận trong tệp bổ sung. Không điều kiện nào đối chiếu `JOB.name/conclusion` với job cùng ID trong provenance. Trong dữ liệu thật, job `124998175208` của #1127 là `gate (ubuntu-latest)`, đòi 18 bước; `chuan-bi` chỉ đòi một bước. Đổi tên được khai vẫn giữ nguyên ID/băm sẽ chọn luật nhẹ hơn. Đây là thiếu đối chiếu dữ liệu đã có, độc lập với giới hạn không giữ log.
  de_xuat: Chọn luật bằng tên trong provenance; kiểm tên, conclusion và trạng thái lỗi của job cùng ID. Thêm ca đổi riêng tên/kết luận trong tệp bổ sung.

- id: F02
  severity: P1
  vi_tri: SPEC.md dòng 113–115 và 143–144, hàm dùng chung/L-7/D2b
  van_de: Bằng chứng có thể tự nhất quán nhưng thuộc commit hoặc lượt CI khác với kết quả đang được xác nhận landed.
  bang_chung: K1 chỉ nối tệp bổ sung với provenance; hàm hồ sơ chỉ đòi hai tệp cùng `run_id`. D2b nối tiếp với `ci_master.run_id` do biên bản khai, nhưng không nối `head` với `merge_commit`. D3 hiện tại chỉ kiểm quan hệ Git giữa merge/head/tree, không kiểm head của CI. Protocol §10.2.3 yêu cầu chọn đúng SHA/run/attempt/context.
  de_xuat: Quy định nguồn run/attempt/SHA mong đợi cho từng lời khai; đối chiếu với nguồn ấy. Với M8, buộc bằng chứng thuộc merge đang đóng; trường hợp đo trên hậu duệ phải có disposition riêng đúng phạm vi.

- id: F03
  severity: P2
  vi_tri: SPEC.md dòng 86–112, định dạng `gate_output/2` và điều kiện passed
  van_de: Định dạng mới vẫn có thể đạt khi chưa đo mã thoát của lệnh, thiếu thành phần bắt buộc của mốc Gate output.
  bang_chung: Định dạng chỉ có header, JOB, BUOC và tổng; K5 đòi `conclusion=success` cùng marker, không đòi bằng chứng `command/rc`. Protocol §10.2.2 quy định rõ `command/rc`. Hồ sơ `pr679-wp678-land-evidence.yaml`, trường `gate_output_nguon_va_gioi_han`, cũng phân biệt `step_conclusion success` với phép đo rc.
  de_xuat: Bổ sung command và rc có nguồn cho từng bước bắt buộc, hoặc giữ `not_measured` khi thiếu và biểu diễn waiver riêng; không suy rc từ conclusion.

- id: F04
  severity: P2
  vi_tri: SPEC.md dòng 105–111, K3/K5/K6
  van_de: Tập job rỗng vẫn thỏa các điều kiện để được passed.
  bang_chung: Khi ba tập ở K3 đều rỗng, K4/K5 không còn phần tử để kiểm và K6 cho phép `passed (0/0 job)` vì không đòi `M > 0`. Bộ sinh cũ `danh_gia_gate.py` có chốt `kq and all(...)`; đặc tả mới làm mất chốt này. Kho có trường hợp CI thực tế không có job, ghi trong hồ sơ #1137.
  de_xuat: Đòi tập job thực thi khác rỗng; quy định riêng trường hợp toàn bộ job skipped. Thêm ca rỗng và toàn-skipped cùng đột biến gỡ chốt.

- id: F05
  severity: P2
  vi_tri: SPEC.md dòng 131–136, 191–205 và Q1
  van_de: Định nghĩa lời khai bỏ qua các dạng đang dùng trong kho và không tái lập được bảng B.
  bang_chung: `python -B work/census.py` cho `TABLE B records=14 claims=21`, thay vì 15/22; `pr696` không có lời khai dương dạng chuỗi theo định nghĩa. `python -B work/spec_probes.py` đo được **15 khóa dạng mapping/list trong 9 hồ sơ**; việc duyệt tiếp không nhận các trường con như `marker`, `rc`, `jobs`. Vì vậy L8 bỏ qua những dạng này. Tổng theo định nghĩa hiện tại là **35 hồ sơ/45 lời khai**, không phải 36/46.
  de_xuat: Quy định cách xử lý mapping/list: hỗ trợ schema rõ ràng hoặc báo không đo được khi gặp dạng chưa hỗ trợ. Đo lại bảng B và Q1 bằng cùng bộ nhận diện. Bổ sung hệ quả L-7: hiện có 24/49 hồ sơ landed không có lời khai dương theo định nghĩa này.

- id: F06
  severity: P2
  vi_tri: SPEC.md dòng 83–85, 96–109 và fixture dòng 282–284
  van_de: Hợp đồng regex đơn dòng chưa biểu diễn được các điều kiện quan trọng của bảng LUAT được chọn làm nguyên mẫu.
  bang_chung: `python -B work/spec_probes.py` đo LUAT có **10 loại job, 31 bước, 36 mẫu**, gồm **8 `JSON_OK`, 6 `CUOI:`, 1 `KHONG:`**. Chúng lần lượt kiểm JSON cấp gốc, dòng tổng cuối và sự vắng mặt của lỗi; không tương đương “có một dòng fullmatch”. Mẫu tiền tố `^cong_cu_test: (\d+)/\1 đạt;` cũng cho `search=True`, `fullmatch=False` trên dòng kết quả thật. Fixture ba job chưa kiểm các trường hợp này.
  de_xuat: Chốt cách chuyển từng loại luật sang định dạng mới, giữ ngữ nghĩa JSON/cuối/không-có và yêu cầu đủ từng mẫu bắt buộc. Thêm fixture đại diện cho cả 10 loại job trước khi chốt ước lượng đợt A.

- id: F07
  severity: P2
  vi_tri: SPEC.md dòng 294 và 335, A5/m-A5 và C6/m-C6
  van_de: Hai đột biến nghiệm thu được chỉ định không thể làm các ca đích đổi màu như yêu cầu.
  bang_chung: A5 giữ regex neo cả dòng rồi đổi `fullmatch` thành `search`; trên dòng đơn, chuỗi bị cắt vẫn trượt cả hai. Probe cho `full=True/True`, `cut=False/False`. C6 yêu cầu gỡ L8 làm **C1–C3 đỏ**, nhưng C1 là đầu vào hợp lệ với kỳ vọng **0 vi phạm L8**; bỏ kiểm L8 vẫn trả đúng kỳ vọng đó. Đây là vi phạm L3.
  de_xuat: A5 phải dùng đột biến thực sự nới điều kiện đang đo và chứng minh ca đổi màu. C6 giao C2/C3 bắt việc bỏ L8; giữ C1 kiểm đường dương bằng đột biến luôn từ chối.

- id: F08
  severity: P2
  vi_tri: SPEC.md dòng 160–162 và cột “neo” bảng A
  van_de: Cột neo khẳng định đã kiểm K1 nhưng một số tệp chỉ ghi SHA rút gọn, không đáp ứng phép so head đầy đủ của K1.
  bang_chung: `python -B work/spec_probes.py` thấy tệp của `pr1095` ghi head 8 ký tự, `pr1127` ghi `f2102fc3`, `pr1128` ghi `c165a5d0`, `pr1141` ghi `b3249c3`. Băm/tập job khớp thật, nhưng không chứng minh header thỏa `head=<sha40>` và bằng head provenance. Ít nhất 5 lời khai được tính neo ở bốn hồ sơ này thiếu điều kiện đó.
  de_xuat: Tách phép đo tập job/băm khỏi phép đo run/attempt/head đầy đủ; sửa tên cột hoặc đo lại theo đúng K1. Không dùng kết quả khớp băm để ghi rằng cả K1/K3/K4 đã đạt.

## Đã đo lại, khớp

- SHA-256 đặc tả, HEAD, tree; diff so `origin/master` chỉ thêm `ops/specs/wp1236-r1.md`, 419 dòng.
- Hai cổng: `98 ĐẠT · 25/28 miễn trừ · 0 vi phạm · tổng 123`; `49/49 hồ sơ landed True đạt · 0 miễn trừ`; đều rc 0. D2 đúng là kiểm lời khai theo `DAT_MOC`.
- 123 hồ sơ; 27 hồ sơ chứa 32 provenance hợp lệ: 728 job `not_measured`, 1 `failed`, 0 `passed`.
- Bảng A: 21 hồ sơ/24 lời khai, trạng thái L-6 và phép đối chiếu tập job/băm khớp; ngoại trừ khẳng định K1 nêu tại F08.
- Các dạng tệp `.txt`: `danh_gia` 6 hồ sơ/2 riêng dạng; `tom` 7/3; `tu_do` 16/11. Bảy bản `danh_gia_gate.py` cùng băm `b87f9697…9fcd`.
- Tám tệp `tom` được trích: chỉ #1127 qua bộ kiểm cũ; băm #1127 khớp 37/37, #1231 khớp 23/23.
- Ba bản #1127 đều qua hai cổng hiện tại. Bản đính chính đầu có **17 job gate** thiếu marker, cộng `chuan-bi` thành **18/37 job**; bản cuối có 7 marker ở `gate (ubuntu-latest)`, so với 18 bước của LUAT.
- Ruff 0.17.3: `packet_loop.py` 1 F841, test 2 F541; năm tệp còn lại 0 lỗi. Hai test hiện có dài 719 và 418 dòng.
- Đăng ký test mới qua `MOI` có đường chạy CI; registry dùng checkout đầy đủ. Write set có chỗ sửa cách nạp module và fixture. Lease #1240 giao đúng hai đường dẫn; ràng buộc giữ `_url_hop_le` tương thích spec #1210.
- `doctrine-scan`: rc 0, 10 tệp, 0 chỗ chép doctrine.
KET_LUAN: changes_requested