# PX-TRIEN-KHAI-VM r1 — `proxima-control` 2.2.0 trên endpoint VM, chạy thật `gemini:auto`: 2/2 `ask_ok`

**Căn cứ:** đặc tả `ops/specs/px-trien-khai-vm-r1.md` (sha256 `9fc895a1da0a56185b53bc471abc890ca3aaee52856c3a765d6da5bc6c5a6243`,
duyệt https://github.com/ducthangho/tra-luat/issues/1562#issuecomment-7198340124), lease `ops/leases/px-trien-khai-vm-r1-g1-operator.yaml`,
Issue #1562. Hiện vật đã lược (log, băm, mốc giờ): `issuecomment-7198874574` (B0–B3) và `issuecomment-7199996503` (bổ sung).
Bí danh: `D` = thư mục làm việc của packet trên VM (ngoài `<base>`), `BAK` = thư mục sao lưu `control.bak-*`, Q1/Q2 = hai lời gọi.

## 1. Kết luận
`<base>\control\` chuyển từ 1.0.1 sang **2.2.0**, bản cũ giữ ở `BAK`. Hai lời gọi `px ask gemini -Model gemini:auto` chạy chế độ Local
bằng module 2.2.0 (manifest `2.2.0`, `.psm1` nạp từ `D`, băm `d26bf828…339f`): cả hai HTTP **200**, `outcome: ok`. Bộ lọc 2.2.0 trả
`answerMarkup: none`, `answerMarkupRemoved: 0` trên đúng hai câu trả lời nhận được; r1 không đo gateway sinh khối `ElicitationsGroup`
với tần suất nào (N4 không đòi). Inference: **2/2**. Có hai lệch đặc tả, chủ kho đã chấp nhận (mục 5).

## 2. Các lượt chạy (đủ mọi lượt)
| lượt | thời điểm (UTC) | kết quả | hiện vật |
|---|---|---|---|
| B0 | 17:12:24 | mục `px-active` mới nhất 11:13:01 (cách 359,4 phút), 164 mục; không tiến trình client `px`; `control\` = `.psd1` `3f2ac59e…ee77` + `.psm1` `ef4821cc…1344` (1.0.1) | `7198874574` |
| B1/B2 lượt 1 | ~17:15:42 | dừng ở bước kiểm băm NGUỒN (hàm `H` trùng alias `Get-History`), trước tiền điều kiện, trước sao lưu, trước mọi ghi | `B12.log` `f637d12c…a43b` |
| B1/B2 lượt 2 | 17:17:40–41 | nguồn = clone kho public `HEAD 4f954fec…`, băm nguồn khớp; `control\` còn y B0; sao lưu `BAK` khớp B0; `control\` = đúng 3 tệp 2.2.0 | `B12b.log` `16720128…26db` |
| B3 | ~17:19:14 | clone sạch, 4 tệp module khớp; cấu hình Local `6d8c4098…9721`; `px config` ok; `px status` ⇒ `RuntimeUnverified` | `B3.log` `e0f821da…a0e7f` |
| B4 lần 1 (chủ kho, admin, RDP) | 17:32:51–53 | `R1.ps1` bản `b1bc95a9…13c8`: dừng ở kiểm phiên bản (`Get-Module` báo `0.0` vì `Run-Px` nạp thẳng `.psm1`); không `status`/`models`/`ask`; không tệp đánh dấu; `px-active` vẫn 164, mới nhất 11:13:01 | `r1-vm.lan1.json` `9407a1d5…33c0` |
| B4 lần 2 (chủ kho, admin, RDP) | 17:37:13–17:37:28 | `R1.ps1` bản `9a622246…d7ce` (kiểm `ModuleVersion` của `.psd1` cạnh tệp đã nạp + băm `.psm1`); admin, session 3, PS 7.6.9; manifest `2.2.0`, đường dẫn nạp đúng; `status` HTTP 200; `models gemini` có `gemini:auto`; WhatIf; Q1; Q2 | `r1-vm.json` `3d304b87…88c7` |

Số chủ kho dán sau mỗi lần B4 khớp băm phiên đo lại qua Desktop Commander. Tệp đánh dấu của lần 2: `17:37:13.6691616Z`.

## 3. Hai lời gọi thật (lần 2)
| câu | `outcome` | HTTP | `requestedModel` | `reportedModel` | `answerMarkup` / removed | độ dài `answer` | bản ghi journal |
|---|---|---|---|---|---|---|---|
| Q1 `Reply with exactly one word: OK` | ok | 200 | `gemini:auto` | `gemini` | `none` / 0 | 2 | một bản mới, `completed` |
| Q2 câu tóm tắt Luật Ban hành VBQPPL | ok | 200 | `gemini:auto` | `gemini` | `none` / 0 | 354 | một bản mới, `completed` |

- Câu trả lời Q1 (dữ liệu không tin cậy): `OK`. Câu trả lời Q2 không chép vào kho (chỉ độ dài).
- `reportedModel` = `gemini`: id này có trong danh sách `models gemini` của chính lần chạy ⇒ đúng luật 2.2.0.
- `px-active`: 164 → 166, đúng hai bản ghi mới (mốc 17:37:21 và 17:37:28), mỗi bản ghép đúng `recordId` của một kết quả.

## 4. Nghiệm thu
| tiêu chí | trạng thái |
|---|---|
| N1 cửa sổ | **đạt** — mốc `LastWriteTimeUtc` lớn nhất của `px-active` là 11:13:01 ở B0 và vẫn 11:13:01 ở phép đọc lại sau B4 lần 1; mọi lần ghi nâng mốc ấy ⇒ không hoạt động nào bao trọn lần ghi đầu 17:17:40 (cách 364,6 phút) |
| N2 sao lưu | **đạt** — `BAK`, băm từng tệp = B0 |
| N3 triển khai (tĩnh Remote) | **đạt** — băm `control\ProximaControl.psm1`/`ProximaConfig.psm1` = 2.2.0; `control\` chỉ thêm `ProximaConfig.psm1` |
| N4 chạy thật | **đạt** — 2/2 `ask_ok`, mỗi lời gọi đúng một bản ghi `px.active.v1` mới |
| N5 ranh giới | **đạt theo quyết định chủ kho** (mục 5.2) — phiên không mở tệp nào trong `profile\`, không đọc thông tin đăng nhập, không chạm dịch vụ hay cấu hình; module tự đọc hai điểm ghi ở 5.2 |
| N6 sổ sách | tệp này viết xong trước review offline và trước lần push duy nhất |

## 5. Lệch đặc tả, chủ kho đã chấp nhận (`issuecomment-7199981461`)
1. **Chạy lại sau lỗi** (`live-retry-outside-authority`): đặc tả đòi mỗi bước một lần, lỗi thì dừng; lease `native_runs_limit_per_host: 1`.
   Thực tế B1/B2 chạy 2 lượt (lượt 1 dừng trước mọi ghi) và B4 chạy 2 lần (lần 1 dừng trước mọi lời gọi gateway); `R1.ps1` được sửa
   giữa hai lần. Inference vẫn 2/2. Chủ kho chấp nhận hồi tố; đây vẫn là lệch, không phải tuân thủ.
2. **Điểm đọc của module** (`runtime-access-outside-boundary`): đặc tả ghi "không đọc profile"; module 2.2.0 tự đọc
   `<base>\profile\rest-port.json` (port/pid; `ProximaControl.psm1` dòng 155) và tra biến môi trường `PROXIMA_API_KEY` (dòng 205, không
   in giá trị). Chủ kho xếp hai điểm đọc này vào phạm vi.

## 6. Còn lại trên VM
`BAK` và `D` (clone kho, cấu hình, các script, log) để lại; dọn khi chủ kho yêu cầu. Đường Remote chạy thật (WinRM) chưa đo.
