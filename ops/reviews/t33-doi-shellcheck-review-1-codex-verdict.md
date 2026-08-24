verdict: approve
reviewed_sha: efcf5757403bd989c0ebbd388fa7a7180171b49f

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| NỀN | `rc=0`; 97/97; chạy 97; bỏ qua 0 | `rc=0`; 97/97; chạy 97; bỏ qua 0 | có |
| NỀN + X2 | `rc=0`; 97/97; chạy 97; bỏ qua 0 | `rc=0`; 97/97; chạy 97; bỏ qua 0 | có |
| VÁ | `rc=0`; 98/98; chạy 98; bỏ qua 0 | `rc=0`; 98/98; chạy 98; bỏ qua 0 | có |
| VÁ + X1 | `rc=1`; 89/90; chạy 90; bỏ qua 8; đỏ `t73` | `rc=1`; 89/90; chạy 90; bỏ qua 8; đỏ `t73` | có |
| VÁ + X2 | `rc=1`; 97/98; chạy 98; bỏ qua 0; đỏ `t98` | `rc=1`; 97/98; chạy 98; bỏ qua 0; đỏ `t98` | có |
| VÁ + X1 · gỡ t70 | `rc=1`; 88/89; chạy 89; bỏ qua 8; đỏ `t73` | `rc=1`; 88/89; chạy 89; bỏ qua 8; đỏ `t73` | có |
| VÁ + X2 · gỡ t70 | `rc=1`; 96/97; chạy 97; bỏ qua 0; đỏ `t98` | `rc=1`; 96/97; chạy 97; bỏ qua 0; đỏ `t98` | có |
| Giải thích `bỏ qua=8` ở X1 | tám ca thân đi qua workflow Ubuntu bị skip; `t73` đỏ | tám dòng `BỎ QUA` là các ca đi qua `_chay_buoc_dang`; `t73` vẫn chạy và đỏ | có |
| Số dòng chứa `_ly_do_bo_qua_workflow` | 5 | `rg -n`: 5 dòng (189, 2308, 2612, 3136, 3151) | có |
| Số định nghĩa + lời gọi thật | 4 | AST/đọc cú pháp: định nghĩa 189; lời gọi 2308, 2612, 3151 | có |
| Ca gọi thẳng `_ly_do_bo_qua_workflow` | chỉ `t70` | AST: chỉ `t70` ở dòng 2612; 2308 và 3151 thuộc dây nối/mã sản phẩm | có |
| Q8 gỡ mọi ca gọi thẳng | vẫn còn đỏ ở dây nối | gỡ `@ca` của ca duy nhất `t70`: X1 đỏ `t73`; X2 đỏ `t98` | có |
| Khối `t98` chép nguyên văn từ r3 | SHA-256 14 dòng cùng tiền tố `4c9b223d3e5edd4a` | hai băm đầy đủ cùng là `4c9b223d3e5edd4ae6e232d0361d0ee047cfef8708f35425e556dc45ac059827`; `cmp` rỗng | có |
| Mối nối `_chay_main_meta` có phản chứng | PR chưa khai phép đo | đột biến bỏ mock `os.name` bị giết: `96/98`, rc=1; đỏ `t72` và `t98` | có |
| Có cơ chế canh docstring `t33` | PR khai không có | hoàn nguyên lời rộng cũ vẫn: suite 98/98 rc=0; `doc-claims-check --strict`, `doctrine-scan`, `adr-song` đều rc=0 | có |
| Windows thật | bảy ô Linux, chưa đo | KHÔNG ĐO ĐƯỢC — sandbox không có runner Windows; mock `os.name` không phải Windows thật | có |
| Trạng thái GitHub trực tiếp | KHÔNG ĐO ĐƯỢC | KHÔNG ĐO ĐƯỢC — `origin` là mirror cục bộ, không có nguồn GitHub trực tiếp trong sandbox | có |
| Spec r3 có đúng băm được giao | `78c3ecb4…` | `78c3ecb40eb8dd7dcf628ef7ea9a372aae5cfbf7a4fcfd25bb4ec7f32fe6ea0d` | có |
| Exact head/base và numstat | head `efcf575…`, base `f33c12d…`, một tệp +22/−1 | head `efcf5757403bd989c0ebbd388fa7a7180171b49f`; base `f33c12db19e7bcc0b18b394635a142c9d45d671d`; `22 1 ops/lease_publish_test.py` | có |

Ghi chú môi trường: sandbox thực tế có các thư mục `.git` rỗng, read-only tại `tmpdir/.git` và `/tmp/.git`, trái với hồ sơ. Exact head sạch vì vậy tái hiện Issue #296. Bảy ô và các đột biến trên được đo trong bản sao phản chứng sau khi áp đúng bản vá #296 đã cung cấp vào `ops/lease_publish.py`; hiệu chỉnh này tách biệt với X1/X2 và không được tính là thay đổi của PR #293. Cây `cay-kho/` vẫn sạch.

Không có finding trong write set của PR #293. M3 bắt đúng lỗ X2 còn sống trên base, giữ răng X1, sống sót khi gỡ ca gọi thẳng, và chính `t98` còn giết được đột biến ở dây nối nền. M4 hạ lời khai docstring đúng với phạm vi thực; phép hoàn nguyên xác nhận thiếu cổng mà PR đã tự khai, không tìm thấy cơ chế bị bỏ sót nên không tăng bộ đếm A=8.
