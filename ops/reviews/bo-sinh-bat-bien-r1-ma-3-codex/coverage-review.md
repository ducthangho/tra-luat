# Kiểm kê độc lập mệnh đề và tập toán tử

Nguồn: diff a89c83a..485387f, AST đầy đủ ở `clause-inventory.json`. Không lấy M làm bộ lọc: AST được trích từ các hàm đích và helper, sau đó mới đối chiếu M. Các nhóm dưới đây phân biệt chốt chấp nhận với tính toán đầu vào, nhánh hiệu năng và chốt của ca phản chứng.

| Nơi | Mệnh đề / tính toán chi phối chốt | Đối chiếu bảng 23 |
|---|---|---|
| c36 | `rc == 0` | Có trong neo c36.so_phan_tu nhưng không bị đột biến riêng; có sẵn ở base, không phải chốt packet thêm |
| c36 | `dem[0]-truoc == mong` | c36.so_phan_tu |
| c36 | `len(van_tay) == mong-lap` | c36.khac_nhau |
| c36 | `if tru is not None` | Vắng; điều kiện kích hoạt hai chốt bắt buộc §2.2.2; không thể loại chỉ vì mang cú pháp if |
| c36 | `not thieu` và tập bắt buộc trừ category thực đo | c36.category (toán tử yếu hóa kiểm thiếu một phần) |
| c36 | `any(ord(c)>0xFFFF for c in thay)` | c36.ngoai_bmp |
| c36 | `len(LOAI)-len(tru or())+1` | c36.cong_thuc; `tru or()` chuẩn hóa None/tuple rỗng, hằng kỳ vọng là dữ liệu riêng |
| c36 | `m.nap_yaml(...) == du_lieu`, `rc == 4`, `Path(thu) != a.ROOT` | Có sẵn ở base, chỉ di chuyển rc==4 vào context cache |
| c36 | `t.is_file()` khi thu mọi byte provenance | Phép chiếu dữ liệu, không phải predicate chấp nhận; cần kiểm nội dung đưa qua L8, không phải thêm yêu cầu file/dir ngoài spec |
| helper ky_tu | kiểu bytes/str/dict/list/tuple, `ord(c)>127` | Chiếu ký tự ngoài ASCII theo §2.2.2; chưa có hàng trong M. Probe độc lập biên +1 và kiểm chuỗi dữ liệu bao trùm helper |
| c37 | tổng 158; khác nhau 158; not lech; hai and | c37.tong / khac_nhau / category; or ở hai vị trí |
| c37 | count != expected; category != Cs | c37.lech; đảo vế trong và các chiều phép so ngoài |
| c37 | biên BMP <=0xFFFF | c37.bien_bmp |
| c37 | lát cắt 128 | c37.phan_bo_sinh |
| c37 | số ô ==648 | c37.so_o |
| nap_sua | neo count ==1 | nap_sua.neo |
| a135/kiem_bo_sinh | duyệt đúng năm bộ đối số BO_SINH_MONG (§2.3.1) | Không có trong bảng; probe bỏ riêng bộ thứ tư/thứ năm và bộ sinh giả chỉ sai tại bộ bị bỏ |
| a135/kiem_bo_sinh | len(ra)==so | a135.so_phan_tu |
| a135/kiem_bo_sinh | tập vắng == vang | a135.category_vang |
| a135/kiem_bo_sinh | len(bmp)==len(set(bmp)) | a135.lap_category |
| a135/kiem_bo_sinh | not any(c in cam) | a135.thuoc_cam |
| a135/kiem_bo_sinh | all(ord(c)>=0x80) | a135.tu_0080 |
| a135/kiem_bo_sinh | bool(ra), cuối >0xFFFF, hiệu độ dài ==1, hai and | ba hàng a135.cuoi.* |
| a135/kiem_bo_sinh | ord(c)<=0xFFFF | a135.bien_bmp |
| a135/kiem_bo_sinh | `if not dat` | a135.gom |
| a135/kiem_bo_sinh | `bang(not lech,...)` | Tiêu đề a135.gom ghi cả hai nhưng M chỉ đổi `if not dat`; không có phép đảo riêng bang(not lech) |
| nho_dem | x thuộc str/bytes hay pickle; `khoa in NHO_YAML`; deepcopy | Đường chọn/cô lập cache, không phải chốt chấp nhận. Có phép đo bật/tắt và va chạm độc lập; không suy rằng mọi kiểu đầu vào tùy ý đều an toàn |
| c39/c40/a136 | len(bien), rc/DO/so_o bằng kỳ vọng; dau None; neo sai phải ném chốt | Mục 3 đòi những phép này kiểm helper/ca đích. Không đòi đệ quy vô hạn “ca phản chứng của ca phản chứng”; xem probe bỏ assertion c40 và giới hạn dev-side |

`a135.gom/bo` (lọc `if False`) và bỏ `bang(not lech)` cho cùng kết quả chấp nhận trên dữ liệu đã tính xong; nhưng **đảo** chúng không tương đương: khi có cả mệnh đề đúng lẫn sai, `if dat` vẫn khiến bang đỏ, còn `bang(lech)` xanh. Không được dùng hàng gộp để tuyên bố đã đo cả hai phép đảo.

## Các ô không áp dụng

- `ge/le/ne`: phép == đã được áp cả ba chiều; != dùng ne/gt/lt; biên > hoặc >= dùng thay biên/đảo. Các tên ge/le là nhãn họ toán tử, không phải ánh xạ AST phổ quát (ví dụ a135.tu_0080/ge là >=→>).
- `gt/lt`: tập đã định nghĩa chúng cho !=; không yêu cầu bổ sung >/< cho mọi phép == ngoài tập đã đóng. c37.lech áp cả hai.
- `dao`: not/so đảo được đã có ở hàng tương ứng, ngoại trừ hai điểm thiếu nêu trên. Hai mệnh đề bằng nhau đã có ne, không cần thêm nhãn trùng.
- `cong1/tru1`: áp hằng hoặc kỳ vọng số. Không áp vào tập category hoặc chuỗi tên; hằng tên/miền kiểm riêng bằng spec và baseline. C36 công thức và lát c37 có hàng riêng.
- `or`: hai dấu and ở mỗi chuỗi đều có phép riêng; vế cuối chung dấu and với vế trước nên không tạo thêm toán tử giống hệt.
- `yeu`: any/all và quan hệ chứa có hàng; phép chứa `c in cam` nằm trong not-any, phép yếu hóa any→all được kiểm. Các phép đổi membership/đảo bổ sung được thảo luận như mẫu độc lập, không ngầm bổ sung toán tử tùy ý vào bảng cố định.
- Ô `bo` không có ở hàng chỉ tính hằng (+1 ngoài BMP) hoặc lát cắt không phải bỏ mệnh đề Boolean; phép bỏ cả tính toán cần định nghĩa mới, không coi là ô bỏ sót theo tập đã đóng.

## Bốn tương đương

1. c37.tong/le: với d=|set(x)|≤n=|x|, d=158 và n≤158 suy ra n=158.
2. c37.khac_nhau/ge: n=158 và d≥158 cùng d≤n suy ra d=158.
3. a135.lap_category/le: d≤n nên n≤d tương đương n=d.
4. a135.cuoi.duy_nhat/le: vế trước đảm bảo phần tử cuối ngoài BMP, vì vậy n-b≥1. Kết hợp n-b≤1 tương đương n-b=1.

Bốn suy luận đúng với chuỗi Unicode hữu hạn trong miền spec, không cần giả thuyết nội dung đại diện. `equivalence-checks.json` kiểm độc lập mọi cặp cardinality trong các miền hữu hạn 0..164 hoặc 0..39; đây là kiểm bổ sung, suy luận bất đẳng thức mới là chứng minh tổng quát.

## Kết quả ngoài bảng sau khi đo

`independent.json` và `exclusions-probe.json` xác nhận:

- Bỏ hoặc đảo `bang(not lech)` cuối a135: a136 rc3 đúng DO. Đây là thiếu hàng của bảng, chưa phải chốt mã đang hở.
- `if tru is None` hoặc `if False`: c40 rc3 ở Mn→Mc. Nhánh chi phối nghĩa vụ §2.2.2 nên nằm trong miền kiểm. `if True` lại cho c40 rc0, nhưng c36 trên riêng a131 rc4 TypeError; bằng chứng này xác nhận giới hạn a131 của meta-test, không nhận rc4 làm chốt đúng.
- Bỏ bộ đối số thứ tư hoặc thứ năm của a135: a136 rc0. Với bộ sinh giả chỉ sai ở bộ bị bỏ, a135 gốc rc3 đúng DO, bản thiếu bộ rc0. Bỏ thứ năm còn cho cả c38/c39/c40/a136 rc0. Đây là mất nghĩa vụ §2.3.1, không được loại chỉ vì thao tác lát cắt ở ngoài tập toán tử cố định.
- Bỏ assertion của chính c40: c40 vẫn rc0; khi chạy phép bỏ chốt category của c36 trên bản ấy, công cụ dev-side thấy SONG. §3 không bắt đệ quy test-of-test không giới hạn; khai giới hạn tầng này, không nhân thành yêu cầu mới cho ca trong kho.
- Dữ liệu kỳ vọng không đồng nhất với predicate. Các hằng số lượng sai thường làm baseline đỏ; tuy nhiên tuyên bố “mọi thay đổi hằng đều bị baseline bắt” không đủ cho danh sách đối số: bỏ một hàng làm mất một nghĩa vụ mà vẫn xanh. Phải kiểm toàn miền năm đối số độc lập.
