# Hiện vật cross-review ĐẶC TẢ `THU-HOI-LEASE-VA-CAP-LAI` (PR #475) — 8 lượt, 9 lời gọi (+ 7a chết preflight, không tính)

Thư mục con **cố ý** (không phải `*-verdict.md` mức gốc): đây là review **đặc tả**, chưa có Packet
Issue/lease/biên nhận v2, nên không đi vào bảng `t26/t27`. Mọi tệp là **nguyên văn** của reviewer
(`codex exec -m gpt-6-astra`, effort ghi ở bảng) hoặc của phiên điều phối — **không sửa**; đính chính
ghi ở đây hoặc ở §0 của `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md`.

| lượt | lời gọi | spec | effort | VERDICT | HINT | PROMPT | thời lượng | kết luận |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | r1 `43844cb2…` | high | `b60a755f…` | `1aeb9621…` | `4c69677e…` | 1842,8 s | 11 P1 + 3 P2 |
| 2 | 2 | r2 `9e775a15…` | xhigh | `bb293295…` | `02b562b3…` | `3e2ed2bf…` | 3322,4 s | 9 P1 + 2 P2 (N1–N11) |
| 3 | 3 | r3 `ef9b3700…` | xhigh | `6b8dde21…` | `0a81bd8b…` | `39bfa3f3…` | 2737,1 s | 9 P1 + 1 P2 (R1–R10) |
| 4a | 4 | r4 `415ce35d…` | xhigh | — (CHẾT) | — | `0d8a5172…` | 1601,5 s, rc=1 | bộ lọc nội dung của nền; xem `luot4a-CHET.md` |
| 4b | 5 | r4 `415ce35d…` | xhigh, đổi phân công | `7d3017ec…` | `4a0321fd…` | `1a2e3d6c…` | 2076,6 s | 4 P1 + 2 P2 (S1–S6) |
| 5 | 6 | r5 `23a7deaf…` | xhigh | `1596d562…` | `8ca8474b…` | `704183b1…` | 2394,7 s | **3 P1** (S1, S2, S3) + **2 P2** (S5, S6); S4 ĐÓNG |
| 6 | 7 | r6 `f78135cf…` | xhigh, trần mới `5578460203` (tới hết P1), harness dựng lại (scratch cũ mất) | `9090aadd…` | `47fbf8cb…` (7 hunk) | `e5006b15…` | 2889,1 s · stdout 85 B · stderr 4 049 518 B · rc=0 | **3 P1** (S1 một phần; S3 một phần; **S7 mới**: tệp retired xung đột schema M1) + **3 P2** (S5, S6 một phần; **S8 mới**: layout/ngân sách object-store) + P3 S9 (kế toán); **S2, S4 ĐÓNG** |
| 7a | — (preflight, KHÔNG tính) | r8 `48ea894a…` | xhigh | — (CHẾT trước khi sinh output) | — | `169d3248…` | 5,4 s, rc=1, stdout 0 B | `refresh_token_invalidated` — ảnh chụp `CODEX_AUTH_JSON` 65 h đã bị xoay vòng; xem `luot7a-CHET-preflight.md` |
| 7 | 8 | r8 `48ea894a…` | xhigh, auth mới (device-auth), tái dùng scratch lượt 6 | `f28b7d0c…` | `95b63772…` (5 hunk) | `c7b65a25…` | 1377,1 s · stdout 465 B · stderr 866 272 B · rc=0 | **0 P1**; `changes_requested` chỉ 2 P2 (S8 một phần, **S10 mới**: biên ADR/spec); S1/S3/S5/S6/S7 ĐÓNG, S2/S4/S9 ĐÓNG ⇒ **điều kiện dừng đạt**; r9 = r8 + HINT (chưa review) |
| 8 | 9 | **r9 `46553836…` (bản đóng băng, Issue #488) + ADR-0047 `b9975929…`** | xhigh, tái dùng scratch lượt 6/7 | `85d10868…` | `10e35e99…` (1 hunk, KHÔNG áp — ghi chú hồ sơ A0) | `d665f94a…` | 1430,7 s · stdout 301 B · stderr 810 147 B · rc=0 | **0 P1**; S8/S10 ĐÓNG, mọi ĐÓNG lượt 7 giữ; `changes_requested` chỉ vì **S11/P2** (hồ sơ Issue #488 ↔ §3.2) ⇒ sửa Issue, spec r9 KHÔNG đổi băm |

`spec-rN.md` = đúng bản spec reviewer đã đọc (sha256 khớp cột "spec"). `luotN-EVIDENCE.md` = lời khai
điều phối gửi reviewer (số đo offline, mốc commit; lượt 6 cộng dồn lượt 1–5 + mục "Bổ sung lượt 6"). `phong.sh.mau` = lệnh
phóng lượt 6 nguyên văn (`<scratchpad>` = thư mục scratchpad của container đang chạy).

## Cảnh báo đang có hiệu lực

| id | phải làm gì |
|---|---|
| `MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU` | `gpt-6-astra`/`xhigh` là thứ **ta yêu cầu**; `codex` không phát `modelUsage`, model đã phục vụ là **KHÔNG ĐO ĐƯỢC**. |
| `phan-cong-CAM-tu-soan-phan-chung` | Từ 4b: reviewer **cấm** tự soạn helper giả / `remote.*.vcs` / `insteadOf` / `refs/replace` / env đổi nguồn / bytes lệch OID / đường thoát cây / đồng tự Unicode. Lượt 4a chết vì đúng việc ấy. ⇒ độ phủ các hướng ấy **chỉ là mô tả bằng lời**; ca âm phải do phiên điều phối dựng. |
| `DONG-la-dong-HOP-DONG-khong-phai-chung-nhan-ban-ke` | "ĐÓNG" ở bảng lượt N là đóng vấn đề hợp đồng trên bản lượt ấy đọc. **r9** (bản đóng băng, Issue #488) ĐÃ được lượt 8 đọc đúng băm: **0 P1**; S11/P2 xử ở hồ sơ Issue, không đổi spec. Mọi lượt review sau chỉ chạy khi có revision spec mới. |
| `TRAN-MOI-toi-het-P1-comment-5578460203` | Trần 6 (`5575587924`) đã hết ở lượt 5 ⇒ checkpoint `5576397733`; chủ kho reroute bằng comment `5578460203` (08-09-2026): review **tới hết P1**, bộ đếm KHÔNG reset (lời gọi 8 = lượt 7 trên r8 ⇒ **0 P1**, vòng dừng). |
| `hinh-dang-nguon-tin-cay-trung-6-lan` | S1 lượt 6 (nền thực thi/trust store chưa được duyệt độc lập) là lần **6** của hình dạng "nguồn tin cậy cho cổng đọc lease". **ADR-0047** (`docs/adr/0047-nguon-tin-cay-cho-cong-doc-lease.md`, Proposed) đã soạn theo quyết định chủ kho 08-09-2026; lớp 2 của ADR cập nhật theo S1 lượt 6. |
| `CODEX-AUTH-ANH-CHUP-CHET` | Lời gọi 8 (lượt 7a) chết preflight vì `CODEX_AUTH_JSON` 65 h bị vô hiệu (`refresh_token_invalidated`); §12: không tính. Lượt kế cần chuỗi auth MỚI từ chủ kho hoặc `codex login --device-auth` hoàn tất. |
| `scratch-luot-1-5-MAT` | Harness reviewer lượt 1–5 nằm ở scratchpad container cũ, **không** được chép vào kho ⇒ mất; lượt 6 dựng lại toàn bộ (`scratch/luot6/`). Từ lượt 6, scratch của reviewer cũng không vào kho (kích thước) — số đo tái lập bằng lệnh trong VERDICT. |
