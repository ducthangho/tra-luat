# VERDICT — cross-review LƯỢT 2, PR #452

- **reviewed_sha:** `ba76a7874489252b2fff9f90063a95ed7ee06a2e`
- **verdict:** `changes_requested` · **assurance:** `same_provider_approved`
- **Reviewer:** hai phiên Claude độc lập — (A) đo RĂNG của bản vá, (B) tấn công chính cú đảo.
- **XUẤT XỨ:** như lượt 1 — subagent trong phiên, không qua `launcher.py run`; mỗi finding đã được phiên
  điều phối đo lại độc lập.

## Hướng A — bản vá có RĂNG không

Phán quyết: **có răng 4/14 · nửa vời 8/14 · rỗng 2/14.**

- **A1 · Vá theo LỖI, không theo HÌNH DẠNG lỗi.** Bản 2 nhận lỗi `grep -l` cho `spec_hash` rồi để nguyên
  **năm** trường đo y hệt cách ấy. Đo lỏng/chặt: `review_rounds_used` **10/4** · `codex_review_calls_used`
  **2/0** · `assurance` **31/19** · `thoi_luong_giay` **9/1** · `luot` **39/7** · `cross_provider` 40 với
  **11 giá trị `false`**. Và `assurance` mắc **ĐÚNG bệnh bốn tên**: `assurance` 19 · `assurance_KHONG_dat`
  **17** · `assurance_ghi_chu` 15 · `assurance_dat` 12 — mười bảy tệp **TỪ CHỐI khai** bị đếm thành đã khai.
  Vi phạm đúng doctrine mà F5 của tài liệu trích: *"đếm HÌNH DẠNG lỗi, đừng chỉ đếm lỗi"*.
- **A2 · Sửa §0/§1 rồi quên §2/§5** — nơi chủ kho đọc để hành động vẫn còn "17%", "co giãn", "M1–M5",
  và vẫn bác 6 mục bằng đúng công thức *"đã có ⇒ trùng lặp"* mà §1 vừa tuyên vô hiệu.
- **A3 · "44%" trộn nền đo** — 61 − 17, trong đó 17 vừa bị rút. Đúng là **40/82 = 48,8%**.
- **A4 · §9 dòng 10 sai** — `bien-nhan` lọc `role: reviewer` (**55**/57) rồi khử trùng ⇒ **52** vòng, không 57.
- **A5 · §9 dòng 14 là no-op** — §0 **chưa hề bị sửa**, vẫn in "cạn ~ngày 11".
- **A6 · HAI LƯỢT REVIEW ĐỂ LẠI 0 HIỆN VẬT** — `git show --stat ba76a78` = 1 tệp. Không biên nhận, không
  verdict. Đúng khuyết tật MVP-1 xếp là **việc số một**, phạm trong cùng commit xếp hạng nó. Hệ quả: "bị bỏ
  im lặng" và "chưa từng nêu" nhìn giống hệt nhau.
- **A7 · Chuẩn kép** — MVP-1 BỎ `review_rounds_used` vì không mã nào tính nó, rồi F3 và MVP-4 lại đề xuất
  `nang_luc_do` và cổng "khẳng định định lượng" — **cũng** không mã nào tính.

## Hướng B — cú đảo là SỬA QUÁ TAY

- **B1 · Bằng chứng KHÔNG GIAO với kết luận.** Không mục nào trong 9 mục neo vào bất kỳ ADR nào trong 8 ADR
  `0 cổng`. Nơi neo thật là §10.1/§3.2/§12/`PROTOCOL:198`/skill/**ADR-0036**, mà §20 xếp ADR-0036 là
  `có nhắc: packet_loop.py×29`.
- **B2 · `ADR-0038 | 0 cổng` SAI TẠI HEAD.** Cổng thật ở `ops/lease_publish.py:189`, fail-closed, **7** ca
  phản chứng `RC_LOP`, ghim băm trong workflow, **land 23-08-2026** — đúng **một ngày sau** mốc `22-08-2026`
  mà §20 tự ghi. Dùng phép đo **có ghi ngày** mà không kiểm ngày.
- **B3 · Tiền đề bị chính §0 bác.** Mỏ neo đặc tả: **0** lần xuất hiện trong cả 6 tệp cổng của §20, mà
  **50/82 = 61%** hiện vật vẫn tuân. `nang_tran`: **1/82** ⇒ **81/82** giữ trần ADR-0043 mà không ai canh.
  **Luật không cổng vẫn ràng buộc được.**
- **B4 · "phần lớn" sai** — `0 cổng` là **9/30 = 30%** của bảng §20 (15 `có nhắc`, 6 `chưa đo`), thiểu số.
- **B5 · MVP xếp theo CHI PHÍ trong khi kết luận nói xếp theo RỦI RO**, và **ba** thứ cùng được gọi "số một".
  Không MVP nào đụng **M4 (răng của cổng)** — thứ chính tài liệu gọi là khoảng trống sâu nhất.
- **B6 · Vật bị phản biện KHÔNG có hiện vật trong kho.** Đề xuất 13 mục không tồn tại dưới dạng tệp; mọi
  câu *"Đề xuất viết: …"* không kiểm được. Luật "nguồn có thẩm quyền là tệp có băm" được áp cho bản phản
  biện và **không** áp cho vật bị phản biện.
- **B7 · Điều CẢ BA bản đều im lặng.** `.claude/dev/duyet_danh_tinh.py`: *"phiên chạy bằng credential CỦA
  CHỦ KHO, nên **mọi chốt dựng trong kho đều là chốt chủ kho tự dựng cho chính mình**… Cổng này chạy trên
  runner của GitHub bằng `GITHUB_TOKEN`… **cơ chế đầu tiên ở đây không tự chứng nhận**."* Nên *"biến luật
  thành cổng"* chưa phải việc thứ ba; việc thứ ba là làm cổng ràng buộc được **người dựng ra nó**.

## Kết luận

Bản 1 suy *"có trong tài liệu ⇒ có hiệu lực"*. Bản 2 suy *"không có mã trong 6 tệp ⇒ không hiệu lực"*.
**Cùng một phép suy một chiều từ CÓ MẶT sang KHẢ NĂNG, chỉ đảo dấu.** Biến đúng là **"luật có bị VI PHẠM
không"**, đo được từ 82 lease + 57 biên nhận, và chưa ai đo.
