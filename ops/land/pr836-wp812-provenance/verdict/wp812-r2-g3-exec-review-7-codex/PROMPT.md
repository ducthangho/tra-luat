# Cross-review độc lập — Packet #812 (MAY-ADR-0054-a) revision 2, lượt 7, OFFLINE trên SHA cục bộ

Bạn là reviewer Codex, khác họ với executor (Claude). Vai READ-ONLY với kho: KHÔNG sửa tệp nào trong `KHO`. Chỉ ghi vào
thư mục ra (thư mục làm việc hiện tại) hoặc /tmp. Kết quả bắt buộc: tệp `VERDICT.md` trong thư mục ra. Nếu có finding,
kèm `HINT.patch` (diff gợi ý, áp được bằng `git apply` trên exact head) cho những lớp phức tạp.

## Định danh (băm là định danh, không phải tên nhánh)

- Kho `ducthangho/tra-luat`, bản sao đầy đủ (không shallow) tại `KHO=/home/user/rv812`, detached ở exact head.
- Exact head: `91c6d8c31190f5f9ea08e4da42ecafd898ee8935` (kiểm bằng `git -C KHO rev-parse HEAD`). Dòng 1 của VERDICT phải là `Reviewed commit: <sha40 đó>`.
- Base: `4c7c29858220ae575bebc5e0a343842cd3db4546`. Diff cần review: `git -C KHO diff 4c7c298 HEAD`, gồm 3 tệp
  `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`, `docs/PROTOCOL_DA_PHIEN.md`. Nhánh chưa đẩy, không có PR.
- **Đặc tả hiện hành: revision 2.** Đọc bằng `git -C KHO show origin/ops/wp812-spec:ops/specs/wp812-r2.md`, sha256
  `d64987461d89429ca97230ec5e796bf987bb9383d765279543e6a7fc14513eef`.
  - Phần chung: `ops/specs/may-adr-0054-chung.md`, sha256 `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`.
  - Lease: `origin/ops/wp812-spec:ops/leases/wp812-r2-g3-claude.yaml`.
  - Kiểm băm bằng `git show … | sha256sum`.
- **r2 tách M3 `accept` + I7 sang packet #834** (`origin/ops/wp812-spec:ops/specs/wp834.md`), do chủ kho quyết ở #812
  issuecomment-6248507114. Không đòi `accept`, readback CI hay connector ở packet này. Mọi lớp ấy ghi ở mục "ngoài phạm vi"
  và không tính vào hạng.
- Lượt 1 (trên `783463b`, đặc tả r1): `changes_requested — P0=0 P1=4 P2=6`. Verdict ở
  `origin/ops/wp812-g2-reviews:ops/reviews/wp812-r1-g2-exec-review-1-codex/VERDICT.md`. Thay đổi kể từ lượt 1:
  `git -C KHO diff 783463b HEAD`.

## Cách review — chuẩn connector, KHÔNG lọc

Review như connector review PR: tìm MỌI lỗi thật trong phạm vi r2 — đúng đắn, an ninh/thẩm quyền, fail-open, lệch đặc tả,
test không đo gì, hồi quy hành vi cũ. Không lọc theo "mô hình tin cậy". Đo mã thật theo từng bất biến I1–I11, M1/M2/M4/M5
và bảng `nghiem_thu` của r2.

**Tìm theo LỚP, không theo lỗi riêng lẻ** (ADR-0054 §4): khái quát mỗi biểu hiện thành một lớp, rồi quét MỌI biểu hiện cùng
lớp trước khi báo. VERDICT có bảng lớp gồm các cột: `slug` · hạng (`P0`–`P3`) · biểu hiện (file:dòng) · phép đo đã chạy ·
hướng vá. Lớp phức tạp kèm HINT.

- **Lượt 2** (trên `97f3bc1`): `changes_requested — P0=0 P1=1 P2=4 P3=1`. Verdict, HINT và REPRO ở
  `origin/ops/wp812-g2-reviews:ops/reviews/wp812-r2-g3-exec-review-2-codex/`. Thay đổi kể từ lượt 2: `git -C KHO diff 97f3bc1 HEAD`.
- **Lượt 3** (trên `4686672`): `changes_requested — P0=0 P1=1 P2=3 P3=0`. Hiện vật ở
  `origin/ops/wp812-g2-reviews:ops/reviews/wp812-r2-g3-exec-review-3-codex/`. Thay đổi kể từ lượt 3: `git -C KHO diff 4686672 HEAD`.
- **Lượt 4** (trên `4504b80`): `changes_requested — P0=0 P1=1 P2=2 P3=0`. Hiện vật ở
  `origin/ops/wp812-g2-reviews:ops/reviews/wp812-r2-g3-exec-review-4-codex/`. Executor đã áp `HINT.patch` lượt 4 rồi tự đo lại
  (ca r812 74/74, đột biến r812 74/74 giết). Thay đổi kể từ lượt 4: `git -C KHO diff 4504b80 HEAD`.
- **Lượt 5** (trên `77393f6`): `changes_requested — P0=0 P1=0 P2=4 P3=0`. Hiện vật ở
  `origin/ops/wp812-g2-reviews:ops/reviews/wp812-r2-g3-exec-review-5-codex/`. Executor đã áp `HINT.patch` lượt 5 rồi tự đo lại
  (ca r812 94/94, đột biến r812 85/85 giết). Thay đổi kể từ lượt 5: `git -C KHO diff 77393f6 HEAD`.
- **Lượt 6** (trên `e93dad7`): **không có verdict**. Lượt bị bộ lọc nội dung của nền chặn ("flagged for possible cybersecurity
  risk") khi reviewer đang tự soạn phép thử. Hiện vật dở dang (HINT, OWN_MUTANTS, MORE_R6) ở
  `origin/ops/wp812-g2-reviews:ops/reviews/wp812-r2-g3-exec-review-6-codex/`. Executor đã áp HINT lượt 6 rồi tự đo lại: ca r812
  115/115, đột biến r812 96/96 giết. Sáu đột biến sống của lượt 6 nay có ca giết. Thay đổi kể từ lượt 5: `git -C KHO diff 77393f6 HEAD`.
- **Ngân sách:** đây là lời gọi Codex **7/8**. Quét RỘNG theo lớp; mỗi lớp còn sót phải liệt kê ĐỦ biểu hiện, kèm HINT đóng trọn lớp.

## Phân công lượt này — KHÔNG tự soạn nội dung nhạy cảm

Lượt trước chết vì reviewer tự soạn phản chứng dạng đường dẫn thoát cây / tên tệp byte thô / symlink / argv khổng lồ. Mọi phản chứng
loại ấy **đã nằm sẵn trong cây** (các ca `r812_*`, xem `.claude/dev/packet_loop_test.py`). Lượt này:
1. **CHẠY** các ca có sẵn, và **ĐỘT BIẾN BẢN VÁ** (trên bản sao tạm) để đo răng của từng chốt.
2. Hướng thử nào cần SOẠN nội dung dạng ấy thì **MÔ TẢ BẰNG LỜI** trong VERDICT (đầu vào, kỳ vọng). Executor sẽ tự viết ca.
3. Mọi phép thử khác (logic, kiểu, thứ tự, thẩm quyền, độ phủ đột biến) cứ dựng như bình thường.
- **Chủ kho quyết** (#812 issuecomment-6250555271): lặp tới hết P1, P2, P3; #812 r2 **được vượt** trần 450 dòng của ADR-0053. Vẫn ghi số
  đo kích thước, nhưng KHÔNG tính vượt 450 là finding. Trần lời gọi Codex (ADR-0052, 8) giữ nguyên.

## Nhiệm vụ — ĐO, đừng chỉ đọc

1. Với từng lớp **lượt 5** (`receipt-validation-incomplete`, `identity-compared-by-provider-family`, `new-input-schema-incomplete`,
   `required-mutation-coverage-missing`) và các biểu hiện ghi trong hiện vật dở dang lượt 6: bản vá đã đóng lớp chưa, có
   răng không, có mở lỗ mới không? Chạy lại các script/REPLAY của lượt 5–6 (KHÔNG chạy lại phần tự soạn nội dung nhạy cảm) ở chỗ còn áp
   dụng. Rồi soi lại các lớp đã đóng ở lượt 1–6 xem có tái phát không. Các lớp lượt 1 thuộc phạm vi r2 (`receipt-validation-incomplete`, `identity-compared-by-provider-family`,
   `findings-not-receipt-bound` phần record-review, `stop-validation-order`, `lease-checks-worktree`,
   `new-input-schema-incomplete`, `required-mutation-coverage-missing`): bản vá đã đóng lớp chưa, có răng không, có mở lỗ mới
   không? Chạy lại các phép tái hiện của lượt 1 (`REPRO.py` ở thư mục verdict lượt 1) ở chỗ còn áp dụng.
2. Kiểm `nghiem_thu` r2: mỗi mục có ca `r812_*` tương ứng, baseline dương đầy đủ, đổi đúng một yếu tố; đột biến khoá `r812_*`
   làm ca đích ĐỎ vì đúng lý do. Liệt kê mục THIẾU hoặc đo sai thứ. Thử thêm đột biến kiểm toán của riêng bạn.
3. Chạy suite trong BẢN SAO TẠM (`cp -a KHO /tmp/x && python3 /tmp/x/.claude/dev/packet_loop_test.py`, ~12 phút). Đòi
   `nền: N/N` hai số bằng nhau, mọi đột biến bị giết, `TỔNG: ĐẠT`.
4. I4/I5: tìm đường ghi state rồi mới từ chối, traceback thay cho mã thoát có kiểm soát, hoặc cửa khép bị chặn. Packet không
   chịu ADR-0054 phải đi đường cũ y như trước (I9).
5. Kích thước: `git -C KHO diff --numstat 4c7c298 HEAD` ⇒ 3 đường dẫn. Ghi số đo; chủ kho đã cho vượt 450.

Mục bắt buộc trong VERDICT: **ĐỐI CHIẾU LƯỢT TRƯỚC** — mỗi lớp lượt 5 ghi một nhãn: đã vá thật / vá hờ / vá sinh lỗi mới.

**NGƯỠNG: chủ kho đòi hết P1, P2 VÀ P3.** Verdict `approve` chỉ khi P0=P1=P2=P3=0; ngược lại `changes_requested`.
Dòng 2 của VERDICT: `Verdict: <approve|changes_requested> — P0=a P1=b P2=c P3=d`, đếm theo LỚP.
Thứ ngoài phạm vi r2 (#834 `accept`/I7, #813–#816) ghi mục riêng.
Hướng thử cần SOẠN nội dung nhạy cảm thì mô tả bằng lời, đừng soạn.
