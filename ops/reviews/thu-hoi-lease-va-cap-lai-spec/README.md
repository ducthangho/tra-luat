# Hiện vật cross-review ĐẶC TẢ `THU-HOI-LEASE-VA-CAP-LAI` (PR #475) — 5 lượt, 6 lời gọi

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

`spec-rN.md` = đúng bản spec reviewer đã đọc (sha256 khớp cột "spec"). `luot5-EVIDENCE.md` = lời khai
điều phối gửi reviewer (số đo offline, mốc commit). `phong.sh.mau` = lệnh phóng lượt 5 nguyên văn
(đường dẫn scratchpad của container cũ — thay bằng của phiên mới).

## Cảnh báo đang có hiệu lực

| id | phải làm gì |
|---|---|
| `MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU` | `gpt-6-astra`/`xhigh` là thứ **ta yêu cầu**; `codex` không phát `modelUsage`, model đã phục vụ là **KHÔNG ĐO ĐƯỢC**. |
| `phan-cong-CAM-tu-soan-phan-chung` | Từ 4b: reviewer **cấm** tự soạn helper giả / `remote.*.vcs` / `insteadOf` / `refs/replace` / env đổi nguồn / bytes lệch OID / đường thoát cây / đồng tự Unicode. Lượt 4a chết vì đúng việc ấy. ⇒ độ phủ các hướng ấy **chỉ là mô tả bằng lời**; ca âm phải do phiên điều phối dựng. |
| `DONG-la-dong-HOP-DONG-khong-phai-chung-nhan-r6` | "ĐÓNG" ở bảng lượt 5 là đóng vấn đề hợp đồng trên **r5**. r6 (`f78135cf…`, commit `2aee80a`) vá theo hint lượt 5 và **chưa được lượt nào review**. |
| `TRAN-6-DA-HET-theo-comment-5575587924` | Trần 6 lời gọi (Q14, comment PR #475 `5575587924`) đã dùng hết ở lượt 5. Lượt kế **phải** có neo trần mới của chủ kho trên PR trước khi phóng — xem `ops/handoff/thu-hoi-lease-va-cap-lai-spec-1-claude-20260908-handoff.md`. |
| `hinh-dang-nguon-tin-cay-trung-5-lan` | S1/S2 (và R1/N1/L1 trước đó) cùng một hình dạng "nguồn tin cậy cho cổng đọc lease". Reviewer lượt 4b và 5 cùng khuyến nghị **ADR** trước khi thi công. Chưa có ADR. |
