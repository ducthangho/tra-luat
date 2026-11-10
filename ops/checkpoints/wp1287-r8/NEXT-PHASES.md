# Mission1238 — dependency và phần chuẩn bị còn dùng được

Đối chiếu handoff đã hash-verify và `ops/plans/PROXIMA-PLAYWRIGHT-v1.md`; giữ nguyên đồ thị, không activation hoặc đổi chuẩn nghiệm thu để vượt lỗi Desktop.

| Phase | Trạng thái sau R8 | Đầu vào cần trước khi thực thi |
|---|---|---|
| P2 #1287 | Chặn bởi PNG native timeout5000; readiness/cleanup có proof | Remediation được chốt riêng trên bằng chứng mới, rồi original fullflow và PS5.1/7 positives; formal exact-H review, current-base gates/CI/MCI/M8 và đủ sensitive assurance |
| P3 #1297 | Chưa thực thi | P2 landed; giữ target, auth/WhatIf/isolation U11, evidence→legal verify; Proxima chỉ khi được yêu cầu |
| P4 #1298 | Planning/read-only được phép, activation chưa đủ | U4/U5/U7/U8/U12, provenance policy và rollback binary+matching testprofile; không dùng checksum thay attestation |
| P5 #1299 | Chưa rollout | Desktop/P4 PASS; ASUS rồi VM, authority và fingerprints riêng, không đổi gateway/account/endpoint/profile |
| P6 #1300 | Chưa nghiệm thu | U1–U12, mọi Packet M8, host acceptance/lease closure/handover đủ proof |

P4 giữ upstream updater survey là đầu vào, chưa viết updater thay thế chỉ vì thiếu provenance. Ma trận cần đo trong Packet riêng sau admission:

| Trigger | Hành vi cần chứng minh | Đầu ra bắt buộc |
|---|---|---|
| Artifact hỏng/sai nguồn/thiếu provenance-policy proof | Dừng trước activation | Staging hash/signature/provenance verdict, active binary/profile không bị thay |
| Máy bận/khóa trùng | Hoãn, không cưỡng bức dừng công việc | Target/lock-owner/expiry/idle proof, không promote |
| Cập nhật lỗi/file khóa/đĩa đầy | Bounded failure rồi giữ hoặc khôi phục bản trước | Actual rc, disk reserve, matching binary+testprofile identity |
| Migration/profile rollback thất bại | Dừng, giữ dữ liệu phục hồi/log | Không tự lặp hoặc hứa giữ login khi chưa đo |
| Healthcheck | Không inference, không suy auth/quota từ model-list | Phiên bản/giao thức/kết nối theo scope; local isolated browser proof |
| Promotion | Chỉ artifact đã đạt Desktop/soak | Cùng immutable hash, retention/soak và ASUS→VM host receipts riêng |

Đây là planning matrix để handoff, không phải kết quả test P4, không cấp host activation mới và không mượn budget Packet khác. P1 đã landed, không mở lại. Raw/private evidence giữ đúng nơi đã đo.
