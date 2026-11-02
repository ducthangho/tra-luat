# Cross-review độc lập — Packet #812 (MAY-ADR-0054-a), lượt 1, OFFLINE trên SHA cục bộ

Bạn là reviewer Codex, khác họ với executor (Claude). Vai READ-ONLY với kho: KHÔNG sửa tệp nào trong `KHO`. Chỉ ghi vào
thư mục ra (thư mục làm việc hiện tại) hoặc /tmp. Kết quả bắt buộc: tệp `VERDICT.md` trong thư mục ra; nếu có finding,
kèm `HINT.patch` (diff gợi ý, áp được bằng `git apply` trên exact head) cho những lớp phức tạp.

## Định danh (băm là định danh, không phải tên nhánh)

- Kho `ducthangho/tra-luat`, bản sao đầy đủ (không shallow) tại `KHO=/home/user/rv812`, detached ở exact head.
- Exact head: `783463b5d62efbc43c6a6116e32c43accbc485f7` (kiểm bằng `git -C KHO rev-parse HEAD`; dòng 1 của VERDICT phải
  là `Reviewed commit: <sha40 đó>`). Base: `4c7c29858220ae575bebc5e0a343842cd3db4546` (origin/master lúc cấp).
  Diff cần review: `git -C KHO diff 4c7c298 HEAD` — 3 tệp: `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`,
  `docs/PROTOCOL_DA_PHIEN.md`. Nhánh chưa đẩy (ADR-0054: đẩy một lần sau khi review sạch), nên không có PR.
- Đặc tả packet: `ops/specs/wp812.md` sha256 `6b8b6c79703bc21949adf006ffc4bb351374254f5a27a0d85ed908ece6511d26` và phần chung
  `ops/specs/may-adr-0054-chung.md` sha256 `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0` — cả hai có trong
  KHO; kiểm băm bằng `sha256sum`. Lease: `git -C KHO show origin/ops/wp812-spec:ops/leases/wp812-r1-g2-claude.yaml`
  (executor claude, reviewer codex, `cross_approved`, review_class `sensitive`). Dòng `executor` (antigravity) ở đầu
  `wp812.md` đã được lease g2 thay theo quyết định chủ kho (#812 issuecomment-6247356060) — không phải mâu thuẫn.
- Nguồn quy tắc: `docs/PROTOCOL_DA_PHIEN.md`, `docs/adr/0054-…`, `docs/adr/0052-…` (ba phép đo land-OID), `CLAUDE.md`.

## Cách review — chuẩn connector, KHÔNG lọc

Review như connector review PR: tìm MỌI lỗi thật (đúng đắn, an ninh/thẩm quyền, fail-open, lệch đặc tả, test không đo gì,
hồi quy hành vi cũ), không lọc theo "mô hình tin cậy" hay theo việc bạn nghĩ executor có thể gian lận. Đặc tả là dạng BẤT
BIẾN (I1–I11 của phần chung + M1–M5 + bảng `nghiem_thu` của wp812.md): đo mã thật theo từng bất biến.

**Tìm theo LỚP, không theo lỗi riêng lẻ** (ADR-0054 §4): khái quát mỗi biểu hiện thành một lớp nguyên nhân, rồi quét MỌI
biểu hiện cùng lớp trên candidate trước khi báo. VERDICT có **bảng lớp**: `slug` (kebab-case, ổn định) · hạng
(`P0`/`P1`/`P2`/`P3`) · các biểu hiện (file:dòng) · phép đo/tái hiện đã chạy · hướng vá. Lớp phức tạp ⇒ HINT trong `HINT.patch`.

## Nhiệm vụ — ĐO, đừng chỉ đọc

1. Kiểm `nghiem_thu`: mỗi ca bắt buộc trong bảng có ca `r812_*` tương ứng, dựng baseline dương rồi đổi đúng một yếu tố; mỗi
   bất biến chạm tới có đột biến (bảng `MUTANTS` khoá `r812_*`) làm ca đích ĐỎ đúng lý do (không phải traceback vô can).
   Liệt kê ca bắt buộc nào THIẾU hoặc đo sai thứ.
2. Chạy suite trong BẢN SAO TẠM của KHO (suite ghi tệp tạm, KHO read-only): `cp -a KHO /tmp/x && python3 /tmp/x/.claude/dev/packet_loop_test.py`
   (~12 phút) — đòi `nền: N/N` hai số bằng nhau, mọi đột biến giết, `TỔNG: ĐẠT`. Có thể chạy riêng một tập ca qua
   `chay_suite(..., chi_chay=...)` trong module test.
3. Soi các đường lỗi thẩm quyền: `record-lease --lease-ref` (I2 đủ ba vế; lease chỉ ở ref cục bộ; validator lấy từ
   `origin/master`; `ai-dang-giu`), `_che_do_0054` (đúng một dòng khai, ba phép đo, kích hoạt; shallow ⇒ false),
   `_du_dieu_kien_approve` (I8 qua hàm chuẩn hoá của `ops/bien_nhan_v2.py`, I10, miền đóng hạng), `accept` (Đ đầu nhánh
   remote = pending_sha; I7 app/workflow/job, attempt mới nhất của run mới nhất; readback neo một kho + một PR + một head,
   đủ trang theo tập ID phân biệt; P3 quyết định), `_xet_dung` (I5: cửa khép không bị chặn). Với mỗi chốt, thử dựng đầu vào
   làm nó cấp quyền sai hoặc chặn oan. Packet không chịu ADR-0054 phải đi đường cũ y như trước (I9).
4. I4: mọi lỗi đầu vào phải từ chối với state nguyên byte — tìm đường nào ghi state rồi mới từ chối, hoặc traceback thay vì
   mã thoát có kiểm soát (KeyError/TypeError trên đầu vào lạ).
5. Kích thước: `git -C KHO diff --numstat 4c7c298 HEAD` ⇒ 3 đường dẫn, ≤ 450 dòng thêm (ADR-0053). Ghi số đo.

**NGƯỠNG: chủ kho đòi hết P1, P2 VÀ P3.** Verdict `approve` chỉ khi P0=P1=P2=P3=0; ngược lại `changes_requested`. Dòng 2 của
VERDICT: `Verdict: <approve|changes_requested> — P0=a P1=b P2=c P3=d` (đếm theo LỚP). Thứ ngoài phạm vi đặc tả (vd `mo-lai`,
checkpoint, vòng P3, generation kế tiếp, kích hoạt — #813–#816) ghi mục riêng, không tính vào hạng.
Hướng thử cần SOẠN nội dung nhạy cảm (vd đường dẫn thoát khỏi cây) thì mô tả bằng lời, đừng soạn.
