# Phạm vi và lập luận kiểm tra

## `nap_sua` và tín dụng cho 648

`nap_sua` đọc `HERE/ten` UTF-8, đòi `nguon.count(cu)==1` rồi compile toàn bộ nguồn với đúng một phép replace. Trong c39, bản sao nguyên vẹn dùng `cu==moi`; bản thiếu ô chỉ xoá `(nhan,"",dung)`, giữ nguyên vũ trụ. Hai bản đều gọi `mod.chay_ca`, patch globals của `mod.CA[c37]`, không gọi nhầm c37 của module mẹ. Gỡ chốt trên tệp bản sao ở work/mut làm cả đường nạp in-memory mất chốt; vì vậy ca c39 phải đỏ. Không suy từ việc control xanh đơn lẻ rằng mọi bản sao tuỳ ý tương đương: phải kiểm nguồn tạo bản sao, mã ca đăng ký và đường dispatch. `nap-code-audit.json` đo tính bằng nhau của code/constant và `nap-sua.json` đo inventory/globals/neo, còn guard-witnesses đo 648 ô với ky8 thật.

c39 cố ý thay ky8 bằng bộ đếm vì kiểm hai chốt trước vòng ô. Nó không chứng nhận consumer. c37 thật trong suite và guard_witnesses mới đo consumer. Phản chứng phải có rc3 DO:c37, đúng thông điệp, 0 ô; hai control phải rc0 và648 ô. Thiếu ô nhưng thực chạy647 mà c39 vẫn xanh sẽ là tín dụng giả; phản chứng gỡ chốt kiểm riêng điều đó.

## Cache YAML

Khoá gồm tên hàm, toàn nội dung input (str/bytes hoặc pickle cho cấu trúc), kwargs đã sort; safe_load và safe_dump không dùng chung namespace. Trả deepcopy để biến thể đổi provenance không làm nhiễm bản gốc. Context patch kết thúc ở mỗi hàng; cache giữ giá trị theo input, không giữ đối tượng có thể bị sửa. `nap_yaml` sản phẩm dựng lớp SafeLoader riêng, không đi qua wrapper safe_load. `cache_audit.py` bỏ cache chỉ trong bản in-memory của test, vẫn chạy toàn chín nhánh c40, ghi SHA256 từng bộ byte hồ sơ/provenance tại đầu `main` thật và từng rc/DO của c36. Chỉ khi hai chuỗi dữ liệu/đầu ra trùng mới nhận cache giữ nguyên thứ được đo.

## Phần ngoài đặc tả

Mục 2.2.1 đòi số phần tử đúng; 2.2.2 đòi CHỨA category bắt buộc và có ngoài BMP; 2.2.3 giữ24 phản chứng registry. Mục3 P5 đòi bỏ một lời gọi cấu trúc phải đỏ. Không có điều khoản ghim nội dung/ID từng ô cấu trúc; mục8 đã khai rõ thay một ô bằng ô khác cùng số lượng/category là giới hạn. R1-02 cụ thể (thay bằng bản sao ô đầu) phải được đóng bằng đo lại; bản thay KHÔNG trùng còn sống không tự mở lại finding đó.

`scope_scan.py` gồm hai minh hoạ: thay marker `[khong khop]` bằng `[khac]` giữ cả nghĩa; và thay ô ấy bằng `kiem(dong + " ", ten_goc)` có thể làm mất chính ví dụ delimiter sớm nhưng vẫn36 phần tử khác nhau, miền category/non-BMP không đổi. Đã đo cả hai ca A/c36 qua L8 đều xanh; đây minh hoạ đúng giới hạn đã khai, không phải mất category, thiếu số phần tử, thiếu ngoài BMP hoặc sai648 thuộc mục2–3. Không dùng lập luận 'mutant sống' để mở rộng đặc tả; cũng không dùng giới hạn này để miễn mutant bỏMn hay bỏ lời gọi (chúng thuộcP4/P5).

## M3 và E

M3 **required**, bước2: dòng thêm `nap_sua(...).read_text(encoding="utf-8")`; không phải làn lưu trữ. Kế thừa required từ lượt1; diff lượt2 vẫn có dòng mã `encoding=`. Windows local base/head và CI chưa chạy trong review offline. Đặc tả giao điều phối chạy Windows; không tự miễn hoặc coi Linux thay Windows.

E1–E5 đối với diff đều **khong**: chỉ test, không đổi điều kiện land ở module sản phẩm, lease/merge gate, authority, workflow hoặc LIVE. Không suy đây là quyền merge. M9 full_mutant_audit vẫn cần exact head vì chạm ops/**/*.py.

## Luật9

Module A/B byte-identical base (product-identical.json). Không chạy lại bốn lượt full theo chỉ thị. Bước8 trên ef82ed9 **chua_do_duoc**, ghi not_run ở review này. Kết quả lượt1 trên ded4128 không chuyển sang SHA mới. Điều kiện chấp nhận: handoff bổ sung neo ef82ed9/tree, đủ hai cặp module/test trên base/head, đúng công cụ/kho/Python, manifest và dấu HOAN_TAT, so từng ID không có GIET-base→hạng khác-head; giữ riêng nợ SONG/VO_CAN và không tính không áp dụng thành GIET. Việc chưa đo không tự tạo finding mã, nhưng không thể ghi nghiệm thu bước8 đạt.
