# PX-TRIEN-KHAI-VM r1 — `proxima-control` 2.2.0 trên endpoint VM, chạy thật `gemini:auto`: 2/2 `ask_ok`

**Căn cứ:** đặc tả `ops/specs/px-trien-khai-vm-r1.md` (sha256 `9fc895a1da0a56185b53bc471abc890ca3aaee52856c3a765d6da5bc6c5a6243`,
duyệt https://github.com/ducthangho/tra-luat/issues/1562#issuecomment-7198340124), lease `ops/leases/px-trien-khai-vm-r1-g1-operator.yaml`,
Issue #1562. Máy `tra-luat-win`; bước đọc/ghi tệp qua Desktop Commander thiết bị `f7281f27…` (`tlcommander`, không admin).

## 1. Kết luận
Endpoint `<base>\control\` chuyển từ 1.0.1 sang **2.2.0** (bản sao lưu giữ lại). Hai lời gọi `px ask gemini -Model gemini:auto` chạy ở
chế độ Local bằng module 2.2.0: cả hai HTTP **200**, `outcome: ok`, `answerMarkup: none`, `answerMarkupRemoved: 0`. Gateway không sinh
khối `ElicitationsGroup` cho cả hai câu; đó là dữ kiện đo, không phải tiêu chí đạt (N4). Inference đã dùng: **2/2**.

## 2. Các bước
| bước | thời điểm (UTC) | kết quả |
|---|---|---|
| B0 | 17:12:24 | mục `px-active` mới nhất 11:13:01 (cách 359,4 phút), 164 mục; không tiến trình client `px`; `control\` = `ProximaControl.psd1` `3f2ac59e…ee77` + `ProximaControl.psm1` `ef4821cc…1344` (1.0.1) |
| B1 | 17:17:40 | sao lưu `<base>\control.bak-20261126T171740Z`, băm 2 tệp = B0 |
| B2 | 17:17:40 | nguồn: clone kho public, `HEAD 4f954fec…`; `control\` = đúng 3 tệp `ProximaConfig.psm1` `59abfa86…6e7d`, `ProximaControl.psd1` `a8af40d8…cb8d`, `ProximaControl.psm1` `d26bf828…339f` |
| B3 | ~17:2x | clone sạch, 4 tệp module khớp; cấu hình Local sha256 `6d8c4098…9721`; `px config` ok; `px status` từ Desktop Commander ⇒ `ProximaControl.RuntimeUnverified` ⇒ chủ kho chạy `R1.ps1` (admin, RDP) |
| B4 lần 1 | 17:32:51 | dừng TRƯỚC ask: kiểm phiên bản đọc `Get-Module` (module nạp từ `.psm1` báo `0.0`) — lỗi của script; không tệp đánh dấu, `px-active` vẫn 164; log `r1-vm.lan1.json` sha256 `9407a1d5…33c0` |
| B4 lần 2 | 17:37:13–17:37:28 | admin, session 3, PS 7.6.9; manifest `2.2.0`, `.psm1` nạp đúng đường dẫn, băm `d26bf828…339f`; `status` HTTP 200; `models gemini` có `gemini:auto`; WhatIf rồi 2 lời gọi thật |

Lần 2 dùng `R1.ps1` sha256 `9a622246ef131548dfe47fd67abd90568850ae6940144312c846bd7f725fd7ce` (sửa kiểm phiên bản: đọc `ModuleVersion` của
`.psd1` cạnh tệp đã nạp và đòi băm `.psm1` = 2.2.0). Bản ghi `r1-vm.json` sha256 `3d304b876da27d8fc518999830a474791d40190da3a0578dcc669a513ce188c7`
(số chủ kho dán khớp số phiên đo lại); tệp đánh dấu `2026-11-26T17:37:13.6691616Z`.

## 3. Hai lời gọi thật
| câu | `outcome` | HTTP | `requestedModel` | `reportedModel` | `answerMarkup` / removed | độ dài `answer` | `recordId` |
|---|---|---|---|---|---|---|---|
| Q1 `Reply with exactly one word: OK` | ok | 200 | `gemini:auto` | `gemini` | `none` / 0 | 2 | `5f713764…` |
| Q2 câu tóm tắt Luật Ban hành VBQPPL | ok | 200 | `gemini:auto` | `gemini` | `none` / 0 | 354 | `79b38b25…` |

- Câu trả lời Q1 (dữ liệu không tin cậy): `OK`. Câu trả lời Q2 không chép vào kho (chỉ độ dài).
- `reportedModel` = `gemini`: id này có trong danh sách `models gemini` của chính lần chạy ⇒ đúng luật 2.2.0.
- `px-active`: 164 → 166, đúng hai bản ghi mới `5f713764-….json` (17:37:21) và `79b38b25-….json` (17:37:28), cả hai
  `requestedModel: gemini:auto`, `state: completed`, cùng `targetFingerprint` `7811451c…b4a7`.

## 4. Nghiệm thu
| tiêu chí | trạng thái |
|---|---|
| N1 cửa sổ | **đạt** — 359,4 phút ≥ 15 |
| N2 sao lưu | **đạt** — `control.bak-20261126T171740Z`, băm = B0 |
| N3 triển khai (tĩnh Remote) | **đạt** — băm `control\ProximaControl.psm1`/`ProximaConfig.psm1` = 2.2.0; `control\` chỉ thêm `ProximaConfig.psm1` |
| N4 chạy thật | **đạt** — 2/2 `ask_ok`, mỗi lời gọi đúng một bản ghi `px.active.v1` mới |
| N5 ranh giới | **đạt** — không chạm dịch vụ, cấu hình, profile, thông tin đăng nhập; module nạp ở B4 = 2.2.0 |
| N6 sổ sách | tệp này viết xong trước review offline và trước lần push duy nhất |

## 5. Còn lại trên VM
`<base>\control.bak-20261126T171740Z` và thư mục làm việc `C:\Users\tlcommander\pxtk-r1\` (clone kho, cấu hình, `R1.ps1`, log) để lại;
dọn khi chủ kho yêu cầu. Đường Remote chạy thật (WinRM) chưa đo.
