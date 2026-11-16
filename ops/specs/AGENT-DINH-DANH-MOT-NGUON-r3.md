tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# Đặc tả packet — `AGENT-DINH-DANH-MOT-NGUON` (revision 3)

| trường | giá trị |
|---|---|
| `packet_id` | `AGENT-DINH-DANH-MOT-NGUON` |
| `packet_issue` | #1335 |
| `revision` | 3 |
| `nguon_cap_viec` | #379 (mở lại ở issuecomment-6906802466) và #387, các nợ D2–D4. Vòng hỏi `soan-spec` của phiên điều phối #1206 ngày 16-11-2026: Q1 (đây là P-B), Q3 = (c), Q4 = băm tệp thực thi, Q6; chủ kho trả lời "Đồng ý theo khuyến nghị". |
| `review_class` | `sensitive` (`.claude/dev/launcher.py` là đường phóng agent và ghi định danh reviewer) |
| `base` | nhánh mặc định lúc cấp lease; số đo lấy trên `a97a1ca` |
| `khung_thiet_ke` | §3 và §4 của `ops/specs/PROBE-AGENT-KHONG-BIEN-MAT-r2.md` tại commit `49a07a9`. Đặc tả này DẪN, không chép lại. Ba điểm ở mục 3 dưới đây thay hoặc bổ sung cho r2. |

## 0. Vấn đề (đo 16-11-2026 03:5x–04:4xZ, master `a97a1ca`)

1. **Probe biến mất.** `chay_cac_probe(ws, lenh, "do thu")` chỉ thêm `claude_trust` khi
   `Path(lenh[0]).name.casefold()` thuộc `("claude", "claude.exe")`. Đo các lệnh:

   ```
   ["claude","-p","x"]           -> workspace, ghi, spawn, claude_trust
   ["bash","-c","claude -p x"]   -> workspace, ghi, spawn
   ["cmd","/c","claude",…]       -> workspace, ghi, spawn
   ["/usr/bin/env","claude",…]   -> workspace, ghi, spawn
   ["claude.cmd","-p","x"]       -> workspace, ghi, spawn
   ```
2. **Định danh lấy theo TÊN tệp (D2).** `_dinh_danh_van_chuyen(['/x/malware/codex'])` và
   `_dinh_danh_van_chuyen(['CODEX.CMD'])` đều trả `provider=openai_codex`.
3. **`transport_sha256` không đo transport (D3).** Giá trị là sha256 của JSON contract hằng, nên mọi lượt
   codex đều cho `5c77b6e9…`, bất kể chạy tệp nào.
4. **Mã chết (D4).** Chốt `RuntimeError("provider co nhieu transport")` không bao giờ chạy, vì mỗi provider
   chỉ có một dòng trong `_TRANSPORT_CONTRACTS`.
5. **Hai cửa định danh.** Lượt review 2 của PR #394 tìm được P1: khi có `--agent`, `_chon_agent` (chọn probe)
   và `_dinh_danh_van_chuyen` (ghi vào `run.json`) cho kết quả mâu thuẫn ở 6/6 tổ hợp. Cũng lượt ấy còn P1
   thứ hai: đuôi Windows chưa được chuẩn hoá. PR #394 đã đóng ngày 02-11 mà không merge.
6. Người đọc `transport_sha256` (đo 16-11): chỉ có `launcher.py` sinh ra giá trị này. Các bản ghi trên
   master chỉ là `run.json` cũ trong `ops/land/**`, không validator nào so giá trị ấy. Đổi nghĩa của trường
   không làm gãy cổng nào, nhưng phải tăng `VERSION` để phân biệt bản ghi cũ với bản ghi mới.

## 1. `write_set`

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
docs/GOI_AGENT_DA_NEN.md
```

`docs/GOI_AGENT_DA_NEN.md` thuộc write set chỉ để ghi cách dùng `--agent` cùng hệ quả bị chặn khi gọi qua
vỏ shell. Không sửa đoạn nào khác trong tệp.

## 2. `ngoai_pham_vi`

- `review_verdict.v1.schema.json` và các nợ D5–D7 thuộc P-C. P-C chạy SAU packet này vì cùng chạm
  `launcher_test.py`.
- Không đổi `_KhoCodex`; P-D sửa đường credential ở tệp khác.
- Không sửa `docs/AUDIT_LAUNCHER_VONG_3.md:398`, ví dụ `-- bash -c` trong tệp ấy. Đó là biên bản lịch sử;
  sau packet này ví dụ ấy sẽ bị chặn, và đó là hành vi đúng.
- Không đoán agent bằng cách đọc chuỗi shell trong `lenh[1:]` (r2 §0, "Vì sao KHÔNG chữa bằng cách đọc
  chuỗi shell").

## 3. Thay đổi so với khung r2

- **T1, một nguồn sự thật.** Chỉ còn MỘT hàm quyết định agent từ cặp (`--agent`, `lenh`). Cả bộ probe
  lẫn định danh ghi vào `run.json` (`provider`, `execution_surface`, `transport`) đều lấy từ kết quả của
  hàm ấy. Khi `--agent` được khai thì nó thắng suy luận từ tên ở CẢ HAI chỗ. Đây là phần đóng P1
  "6/6 mâu thuẫn".
- **T2, chuẩn hoá đuôi Windows.** Trước khi so với danh sách cho phép, cắt đúng một đuôi trong
  `.exe`, `.cmd`, `.bat`, `.ps1` và casefold. Danh sách vỏ shell gồm thêm `env`,
  `powershell.exe`, `pwsh.exe`, `cmd.exe`, `wsl`, `wsl.exe` (danh sách gốc ở r2 §3.3). Tên agent
  khai qua `--agent` thì so BẰNG NHAU, không casefold (r2 §4, dòng cuối của ma trận).
- **T3, `transport_sha256` đo tệp thật.** Resolve `lenh[0]` **theo đúng ngữ cảnh của tiến trình con**: `cwd` là workspace (`kq["workspace"]`, chính `cwd` mà `Popen` dùng) và `PATH` của môi trường con. Sau đó `os.path.realpath`. Rồi **phóng tiến trình con bằng chính đường tuyệt đối vừa băm** (thay `lenh_con[0]`), để bytes được băm là bytes được chạy (finding P2 4582005789 trên PR #1333: `which` resolve theo `cwd` của launcher sẽ băm một tệp khác tệp mà con chạy trong workspace).
  `transport_sha256` = sha256 của bytes tệp đã resolve, đọc tối đa theo trần sẵn có của launcher hoặc
  dạng băm luồng. `run.json` có thêm `thuc_thi_duong_dan` (đường đã resolve). Không resolve được, hoặc
  không đọc được, thì `transport_sha256 = null` kèm `thuc_thi_ly_do`, **không** lùi về băm hằng. Định
  danh `provider` lấy theo T1, không theo đường dẫn. Bỏ chốt chết D4, hoặc thay bằng chốt đo được thật
  (ví dụ kiểm `_TRANSPORT_CONTRACTS` không có tên lệnh trùng giữa hai provider), kèm ca test làm nó đỏ.
  Tăng `VERSION` của launcher (hiện `1.5.0`).

## 4. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Cờ `--agent claude\|codex\|khong` cho lệnh `run`; lặp cờ hoặc giá trị lạ ⇒ `MA_THAM_SO` (r2 §3.1) | `launcher.py` |
| M2 | Vỏ shell đã biết mà không có `--agent` ⇒ `Chan(MA_THAM_SO)`, thông điệp đủ ba ý theo r2 §3.3 | `launcher.py` |
| M3 | T1: một hàm quyết định agent, dùng cho cả probe và `run.json` | `launcher.py` |
| M4 | T2: chuẩn hoá đuôi `.exe/.cmd/.bat/.ps1` cho cả suy luận agent và nhận diện vỏ shell | `launcher.py` |
| M5 | T3: `transport_sha256` là băm tệp thực thi đã resolve; thêm `thuc_thi_duong_dan`/`thuc_thi_ly_do`; xử lý D4; tăng `VERSION` | `launcher.py` |
| M6 | `run.json` ghi `agent_da_khai`, `agent_suy_ra`, `probe_da_chay`, `probe_bo_qua` (r2 §3.4) | `launcher.py` |
| M7 | Ma trận ca của r2 §4, cộng: `claude.cmd`/`claude.ps1`/`CLAUDE.EXE` không khai cờ ⇒ chạy `claude_trust`; `env claude` không cờ ⇒ CHẶN; với mọi tổ hợp (`--agent` × `lenh[0]` ∈ {claude, codex, bash, claude.cmd, git}): bộ probe và `provider` trong `run.json` KHỚP nhau (đóng P1 6/6); `['/x/malware/codex']` không cờ ⇒ `transport_sha256` = băm tệp giả đã tạo ở đường dẫn ấy (khác băm hằng cũ `5c77b6e9…`); lệnh không resolve được ⇒ `transport_sha256 null` + lý do; launcher chạy từ thư mục A, workspace B, cả A lẫn B có `./agent` KHÁC nhau, `lenh[0]` = `./agent` ⇒ `transport_sha256` là băm của `B/agent`, và tiến trình con chạy đúng `B/agent` (con in dấu riêng của tệp mình) | `launcher_test.py` |
| M8 | Đột biến cho từng chốt (bảng tối thiểu ở r2 §4, cộng: T1 tách lại hai nguồn; T2 bỏ cắt `.cmd`; T3 lùi về băm hằng; T3 bỏ `thuc_thi_ly_do`), đăng ký vào bảng đột biến sẵn có. Mỗi đột biến phải giết đúng ca đích, đúng khẳng định (luật phân hạng `TinHieuChotCa`, CLAUDE.md) | `launcher_test.py` |
| M9 | Mục ngắn trong `docs/GOI_AGENT_DA_NEN.md`: khi nào khai `--agent`, ví dụ `-- bash -c` bị chặn, cách chữa | `docs/GOI_AGENT_DA_NEN.md` |

## 5. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Ma trận M7 xanh trên head; trên **base**, ca `bash`+`--agent claude` và ca `claude.cmd` ĐỎ (vế âm, chính phép đo ở mục 0) | đột biến tương ứng ở M8 |
| N2 | Ca "khớp hai cửa" xanh với đủ 15 tổ hợp, đếm và in theo từng tổ hợp (L6c) | đột biến T1: tách nguồn ⇒ ca đỏ, kèm danh sách tổ hợp lệch |
| N3 | `_dinh_danh_van_chuyen`/hàm mới với `/x/malware/codex` không khai `--agent` ⇒ `transport_sha256` bằng sha256 của tệp giả; với `--agent codex` vẫn khác băm hằng `5c77b6e9…` | đột biến T3 lùi về băm hằng ⇒ đỏ |
| N3b | Ca "khác cwd" của M7: băm là băm của tệp trong workspace, và dấu in ra của con khớp tệp đã băm | đột biến: resolve theo `cwd` của launcher (bỏ `cwd=workspace`) ⇒ đỏ |
| N3c | Ca "chọn tệp thực thi" RIÊNG: `lenh[0]` là symlink trỏ tới đích X (in dấu X). Ca test dùng một điểm tiêm nằm giữa bước băm và bước phóng (ví dụ thay hàm phóng bằng một hàm bọc) để đổi đích của symlink sang Y (in dấu Y), rồi mới cho phóng. Kết quả đúng: con in dấu X và `transport_sha256` = băm X. | đột biến: phóng `lenh_con` gốc (symlink) thay vì đường tuyệt đối đã resolve ⇒ con in dấu Y ⇒ đỏ. Phạm vi của ca này chỉ là CHỌN tệp thực thi. Ca không hứa chống việc sửa NỘI DUNG của chính tệp đã băm giữa lúc băm và lúc chạy; khe ấy ghi ở `chua_do_duoc`. |
| N4 | `python -u .claude/dev/launcher_test.py` ra N/N, hai số bằng nhau. Bảng đột biến: mọi đột biến mới bị giết đúng lý do, 0 tín dụng giả. `t117` (mỗi mẫu tìm-thay khớp đúng một chỗ) xanh, và đọc từng dòng của nó (r2 §8.1) | ca đỏ, số lệch, hoặc mutant cũ đột nhiên `giết 0/1` |
| N5 | **Windows native** trên `tra-luat-win` (ADR-0057/58/59), Python 3.12, không `PYTHONUTF8`: ma trận M7 chạy thật với shim `claude.cmd`/`codex.cmd` giả, và ca mới không bị `BO QUA` lặng lẽ (r2 §8.2). Vế âm: ca `claude.cmd` đỏ trên base | ca đỏ hoặc bị bỏ qua không khai |
| N6 | CI: gắn nhãn `windows` trước khi merge để `launcher-windows.yml` chạy (r2 §8.3: workflow ấy có `labeled`). Lượt `launcher (Windows that)` trên head xanh, đọc nhãn job và `runner_id` | job Windows đỏ, hoặc vắng mặt |
| N7 | `adr-song`, `doctrine-scan` rc 0; ruff `--select F` delta 0 trên hai tệp `.py` | — |
| N8 | Gate hậu merge đủ bốn mốc §10.2.2 | — |

## 6. Kích thước và trần

PR #394 (thiết kế r2, không có T1/T3) thêm 220 dòng trên 2 tệp. Packet này dự kiến 3 tệp và 300–450 dòng
thêm. Trần `ADR-0053`: ≤ 6 tệp, ≤ 450 dòng thêm, đo bằng `numstat <base>...HEAD`. Đây là packet dễ chạm
trần nhất trong bốn packet: chạm trần thì dừng ở `luat_dung`, không tự cắt ca của M7.

## 7. `luat_dung`

- Vượt trần `ADR-0053` ⇒ dừng; nâng trần là quyết định của chủ kho (E2), mang theo `numstat` và danh sách
  ca không cắt được.
- Chạm trần lời gọi Codex theo `ADR-0055` (E2).
- Lượt Windows (N5) không chạy được thì không merge; ghi `KHÔNG ĐO ĐƯỢC`, phiên điều phối tự xếp lại.

## 8. `pham_vi_e`

Không chạm E4, không chạm E5. Packet đổi cách launcher xác định agent và ghi hồ sơ, không đổi ai được
review hay merge.

## 9. `hinh_dang_ke_thua`

Từ #363 (r1, dừng không viết mã), #379 và PR #394 (r2, hai lượt review `changes_requested`, chạm trần
review, đóng 02-11 vì tụt 3425 commit và 2 xung đột). Hình dạng đếm được:
- **"Hai cửa cho cùng một câu hỏi"**: probe và định danh mỗi cửa tự đoán agent. Lần 1 ở PR #394. T1 đóng
  hình dạng này theo kiến trúc, không theo bản vá.
- **"Danh sách tên đoán trước"**: đuôi Windows, vỏ shell. Lần 2 (lần 1 là `claude`/`claude.exe` ở master).
- **"Khai rộng hơn đo"**: `transport_sha256` mang tên "transport" mà không đo transport. Lần 1.

## 10. `chua_do_duoc`

- Shim npm thật `claude.cmd`/`codex.cmd` trên `tra-luat-win`: chưa đo có cài hay không. N5 dùng shim giả
  do ca test dựng.
- Với shim `.cmd`/`.ps1`, `transport_sha256` là băm của shim, không phải băm của bản Node thật sau shim.
  Đây là giới hạn đã biết, phải ghi vào docstring.
- Khe giữa lúc băm và lúc chạy với NỘI DUNG của chính tệp đích (sửa tệp tại chỗ sau khi băm): không đóng. T3 chỉ bảo đảm tệp được phóng chính là tệp đã được chọn để băm.
- Vỏ shell chưa có tên trong danh sách vẫn rơi vào nhánh "còn lại ⇒ `khong`", như r2 §3.3 đã nói. Packet
  không đóng được ca này.

## 11. Thay đổi so với r1

r1: `ops/specs/AGENT-DINH-DANH-MOT-NGUON-r1.md`, sha256 `9fd344a628862597213f6181c916abd0a7fda6637367d5cd8ebdfc1c815344cc`. Chủ kho đã duyệt r1 nhưng chưa lease nào dùng nó.
r2 đóng finding P2 4582005789 của connector trên PR #1333 (head `99c8ee8`). Phiên điều phối đo lại: `lenh_run`
phóng `subprocess.Popen(lenh_con, cwd=kq["workspace"], …)` (`launcher.py:2677`), nên `which` theo `cwd` của
launcher có thể băm một tệp khác tệp được chạy. Thay đổi: T3 resolve theo `cwd` và `PATH` của tiến trình con
rồi phóng bằng chính đường đã băm; M7 thêm ca khác `cwd`; thêm tiêu chí N3b.

Ghi kèm, không phải thay đổi của đặc tả: ngày 16-11 chủ kho bỏ **CI Windows**. N6 (gắn nhãn `windows` để chạy
`launcher-windows.yml`) được ghi là `owner_waived` trong lease. Lượt native trên `tra-luat-win` (N5) giữ nguyên.

## 12. Thay đổi so với r2

r2: `ops/specs/AGENT-DINH-DANH-MOT-NGUON-r2.md`, sha256 `5bf87a4649a97d8c91aeb5c3207580fb23fd25e76311d6eaac210466781ec431`. r2 chưa được duyệt, chưa lease nào dùng.
r3 đóng finding P2 4582022758 của connector trên PR #1333 (head `3f9fb47`). Trong fixture khác `cwd`, phóng
`./agent` gốc với `cwd=B` cũng chạy đúng `B/agent`, nên đột biến "phóng `lenh_con` gốc" không đổi màu N3b.
Thay đổi: tách đột biến ấy sang tiêu chí mới N3c, dùng fixture symlink đổi đích giữa lúc băm và lúc phóng.
Ghi khe "sửa nội dung tệp đã băm" vào `chua_do_duoc`.
