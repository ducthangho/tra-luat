Đã review tại HEAD `b4041b94df07f0187811a2834b885c83d3943d81`, tree `b52b723df453cb03cea2f289f286007a588cd1fe`. Không gọi mạng; đối chiếu đầu/cuối **12.599 mục**, không thay đổi nội dung, index nguyên vẹn, Git sạch.

Giới hạn: clone chỉ có refs master nên không xác minh được phép đo lease trên 768 nhánh lúc 04:00–04:05Z. Module mới chưa tồn tại: phép kiểm hợp đồng dưới đây không phải test triển khai. Ước lượng A1 chưa phải numstat thi công.

# VERDICT wp1236 r7 vòng 7

spec_sha256: 31415a8a840c63c3b3a16eefe83dc90739698c3d10afb2348b5e7c5011ae26ba

## Finding vòng 6 của tôi

Vòng 6 không có finding mới; ba finding được đóng trong verdict ấy vẫn đóng:

- G16: ĐÓNG — Biến thể `duong_nhanh` tiếp tục nằm ngoài phạm vi, chuyển sang #1257; hệ quả `owner_waived` hoặc `landed: false` được giữ rõ.
- G17: ĐÓNG — D2b vẫn dùng chung `la_run_land`, đòi `ci.yml` và `event == push`, có ca D10 cùng đột biến tương ứng.
- G18: ĐÓNG — `nang_tran` neo băm của chính bản đang duyệt; bảng và căn cứ thống nhất 720–900, trần riêng A1 ≤3 tệp/≤950 dòng thêm.

## Findings mới

- id: G19
  severity: P3
  vi_tri: SPEC.md:208–210, 665
  van_de: Ba điều kiện mới của `kiem_so_luat()` chưa có ca âm và đột biến riêng để chứng minh chúng được thực thi.
  bang_chung: A20 giữ nguyên so với r6, chỉ thử sai băm, chồng miền và hai miền mở; A3j/j′ thử tập job của provenance, không thử sổ luật sai. `python -B work/contracts.py` cho mô hình A20a–e giữ nguyên kết quả khi lần lượt bỏ kiểm tên bắt buộc trùng, thiếu năm tên chuẩn, hoặc số mục luật khớp tên.
  de_xuat: Thêm ca sổ luật sai từng điều kiện, gồm khớp 0 hoặc 2 mục luật; giữ băm và miền hợp lệ, đòi lý do `so_luat_hong`, rồi gỡ từng chốt để chính ca tương ứng đỏ.

- id: G20
  severity: P3
  vi_tri: SPEC.md:886
  van_de: Run sớm nhất trong 29 tệp provenance `ci.yml`/`push` bị ghi sai.
  bang_chung: `python -B work/measure.py census` trả run nhỏ nhất **40268583940**, tại `pr945-wp899-provenance/do-1026-cebb5b2/ci-provenance-40268583940.yaml`, J=22; không phải 40842340568 của pr1013.
  de_xuat: Sửa run và hồ sơ sớm nhất; giữ kết luận 29/29 có đúng tập 22 tên vì phép đo này khớp.

## Đã đo lại, khớp

- **37 provenance = 29 `ci.yml`/push + 4 dispatch + 4 launcher/push**; cả 29 tập J có đúng 22 tên, mỗi tên một lần.
- Run **41397205258**: J=14, thiếu đúng tám mảnh `gate-cong-cu`; 13 job thiếu bước luật.
- Q7: đúng **sáu hồ sơ** có Windows cùng head land; pr1115 bị loại đúng vì head ngoài H.
- `51d6509..b796259`: `ops/`, `.github/` không đổi; `packet_loop.py` +7/−1 và các số dòng cập nhật đều khớp.
- `F-ok`: **23 job T, 22 job J, 43 bước luật** khớp tên REST/YAML; workflow nguyên văn tại `fe84620` đọc được trong kho tạm giữ objects gốc.
- Mô hình hợp đồng A3d–g/A3k phân biệt được bằng danh sách lý do, kể cả khi trạng thái vẫn `not_measured`; A16b/c nhắm đúng chốt STEP ngoài J.
- Probe A22: `runpy` nạp `.pyc` lọt ba lớp r6 nhưng bị audit r7 bắt; nạp `.pyc` của `ci_provenance` không bị chặn.
- Căn cứ kích thước: **1049, 597, 403** dòng; hai nguyên mẫu **196, 103** dòng. Thành phần ước A1: **290+600+1=891**, nằm trong khoảng và dưới trần 950.
- Hai cổng nền và `doctrine-scan`: **rc 0**; **101 ĐẠT, 25/28 miễn trừ, 0 vi phạm**; **52/52** hồ sơ landed đạt.

KET_LUAN: approve