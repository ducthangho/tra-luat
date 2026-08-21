
codex
*Không tệp nào bị sửa: sandbox khóa filesystem ở chế độ chỉ đọc nên không thể tạo tệp Markdown ngoài `./kho`.*

# C1

**ĐO ĐƯỢC — hiệu chỉnh tiền đề.** Kho có 45 ADR, 24 receipt, 24 verdict, 1 `TONG_HOP_*`; `NO_KY_THUAT.md` có 481 dòng/8 mục, `CHANGELOG.md` có 7.648 dòng. Khối “Bài học đắt giá” dài **160 dòng**; 161 chỉ khi tính cả tiêu đề mục kế tiếp. Chỉ **14/24** receipt có `verdict_usage_caveats`.

**ĐO ĐƯỢC.** Không hoàn toàn đúng rằng review artefact không bị máy đòi: `t26` kiểm receipt–verdict–băm; `t27` buộc verdict/receipt vào mục lục và nâng caveat đã khai lên bảng cảnh báo. Nhưng máy **không buộc bài học phải được khai**: thiếu hẳn caveat vẫn hợp lệ; `bai_hoc` xuất hiện 0 lần trong hai bộ điều phối được nêu.

**SUY LUẬN.** “Kho bài học” là khung sai. “Truy xuất” đúng hơn nhưng vẫn thiếu một tầng: ba bên đã đọc bẫy `$?`, còn bài ratchet nằm ngay trong tệp mà vẫn tái phát. Nút thắt là **kích hoạt đúng phép kiểm tại đúng quyết định**. Tất định hóa lưu trữ chỉ mua kiểm kê và truy vết, không tự ngăn tái phạm.

# C2

1. **`hinh_dang_lap` — KHÔNG hoàn vốn nguyên dạng.**  
   **Lách rẻ:** đổi `shape_id`/seam, không khai predecessor, hoặc điền `quyet_dinh_kien_truc` vô nghĩa.  
   **Báo oan:** ba lần cùng triệu chứng “thiếu tệp sandbox” có thể có ba nguyên nhân khác nhau. Chỉ đáng làm nếu máy suy số đếm từ cùng một `finding_id` ổn định và chỉ **pause để người có thẩm quyền xét**.

2. **`doi_ke_hoach` — liên kết hoàn vốn, boolean không.**  
   **Lách rẻ:** ghi `can: false` hoặc đổi tên seam.  
   **Báo oan:** protocol cho phép **Packet revision hoặc MCR**; lỗi riêng của acceptance/write-set không nên bị ép thành MCR. Máy chỉ nên kiểm revision/MCR đã khai có thật, đúng phiên bản, đúng người duyệt và lease cũ đã bị thu hồi.

3. **`rXX_ | chi_la_chu` — chỉ hoàn vốn như sổ kế toán.**  
   **Lách rẻ:** trỏ test không liên quan hoặc luôn chọn `chi_la_chu: true`.  
   **Báo oan:** bài học về branch protection, quyền duyệt hay thứ tự land không nhất thiết có unit test. Chỉ nên gate khi `rXX_` tồn tại, thuộc suite bắt buộc và đổi màu dưới phản chứng. `chi_la_chu` phải được tính là nợ, không phải bảo đảm.

**SUY LUẬN.** Không cạnh nào hoàn vốn nguyên dạng. Hai phần đáng giữ là **toàn vẹn tham chiếu** của (2) và (3).

# C3

**ĐỌC ĐƯỢC.** §3.1.1 đã quy định MCR; §3.2 đã liệt kê các trường buộc Packet revision: objective, acceptance, write-set, dependency, executor, environment.

**KẾT LUẬN.** “Kế hoạch sai” là phán đoán, không gate được từ văn bản bài học. Gate được **hậu quả sau phán đoán**:

- Trường material của Mission đổi ⇒ cần MCR human-approved.

- Chỉ trường Packet đổi ⇒ cần Packet revision/generation mới.

- Đã ghi `mcr_candidate` ⇒ pause phần bị ảnh hưởng cho tới quyết định bền và readback khớp.

Nên thay boolean bằng:

```yaml
plan_impact: none | packet_revision | mcr_candidate | new_mission
```

Với `none`, máy chỉ đòi người quyết, lý do và dấu vết. **SUY LUẬN:** đây là triage có audit, không phải oracle.

# C4

**ĐỌC ĐƯỢC.** Chính docstring `t27` thừa nhận nâng caveat lên mục lục vẫn không cứu người mở thẳng verdict. Có chỉ mục khác với được gọi đúng lúc.

Tag `khi:*` chỉ hữu ích nếu là trường máy đọc được và hook tự suy trigger từ lệnh/diff/state. Nếu agent phải nhớ nguy cơ để tự nghĩ chuỗi grep, vòng lặp là hình tròn.

**ĐO ĐƯỢC sau triển khai:** ghi bốn tỷ lệ:

- Bài liên quan được hiện trước hành động / số cơ hội.

- Bài hữu ích / tổng bài được hiện.

- Lỗi hình dạng cũ / số cơ hội.

- Số lần bỏ qua và thời gian tăng thêm.

Chạy replay ghép cặp có/không hook trước khi bắt buộc. Hiện chưa có số nên hiệu quả của chỉ mục theo cò vẫn là **SUY LUẬN**.

# C5

**MỘT thứ:** một `evidence-preflight` tại cửa chuyển state: đọc Packet Spec trên canonical, tự chạy `required_checks` bằng subprocess không qua shell pipeline, rồi phát receipt máy. State không nhận mã thoát gõ tay.

**SUY LUẬN — phản thực 3/3:**

1. `$?`: runner lấy `CompletedProcess.returncode`; `tail`, `printf` hay command substitution bên ngoài không thể biến bằng chứng đỏ thành xanh.

2. Manifest/ratchet: trigger `docs/**/*.md` chọn full selftest chứa `r291_docs_ngoai_goi`; chỉ chạy `release-manifest` không đủ receipt.

3. Kế hoạch chưa merge: không resolve được `plan/spec path + hash` từ canonical nên không cấp lease.

Runner chỉ chặn **bằng chứng dùng để chuyển state**; nó không ngăn ai tự chạy sai trong terminal.

# C6

**ĐO ĐƯỢC.** First-parent log ngày 21-08 có đúng 4 merge PR vào master.

**TÔI SẼ KHÔNG XÂY — SUY LUẬN:** kho bài học thứ tám, knowledge graph/vector DB, bộ phân loại LLM “cùng hình dạng”, auto-MCR, backfill toàn bộ changelog, hoặc hook in hàng loạt lời nhắc. Chúng tăng control-plane và vẫn để ngỏ đường lách tự khai.

# TOI_KY

1. Gắn `evidence-preflight` vào transition cấp lease/review/land. **CƯỠNG CHẾ MÁY:** spec phải đọc được từ canonical theo băm; check do runner chạy và receipt khớp exact head.

2. Dùng receipt hiện có làm nơi tham chiếu: `trigger`, `evidence`, `guard_ref | advisory`. **CƯỠNG CHẾ MÁY:** `guard_ref` phải tồn tại, thuộc suite bắt buộc và có phản chứng; `advisory` là **CHỈ LÀ CHỮ**.

3. Thay `doi_ke_hoach.can` bằng `plan_impact` và dấu vết người quyết. **CƯỠNG CHẾ MÁY:** chỉ kiểm state/revision/MCR sau quyết định; việc chọn enum là **CHỈ LÀ CHỮ** có trách nhiệm của human/reviewer.

4. Thử `khi:*` ở shadow/replay trước khi bắt buộc. **CƯỠNG CHẾ MÁY:** thu bốn phép đo ở C4; không giảm recurrence thì bỏ.

# TOI_KHONG_KY

1. `hinh_dang_lap >= 3 ⇒ quyet_dinh_kien_truc` dựa trên số/tên tự khai.

2. `doi_ke_hoach.can` như oracle, hoặc ép mọi `true` thành MCR.

3. `rXX_ | chi_la_chu` như cổng xanh khi chưa kiểm test tồn tại, được chạy và có răng.

4. Kho bài học mới hoặc chỉ mục thủ công không có caller và phép đo hiệu quả.
tokens used
159,453
