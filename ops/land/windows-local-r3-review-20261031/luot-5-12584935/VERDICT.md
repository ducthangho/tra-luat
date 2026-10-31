verdict: changes_requested
reviewed_sha: 27b6effb633c11f268b6e66692d14458b6a647f4
Kết quả: 0 P0, 0 P1, 0 P2, 1 P3.

Review độc lập hai trục **Spec** và **Standards/Security**, theo ngưỡng packet: hết toàn bộ P0–P3. Có 1 lớp / 1 biểu hiện P3 về lời khai chứng cứ; chưa thấy lỗi luật hoặc sai kết quả ba ca.

- Base: `adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc`; reviewed tree: `b9d6ae0622e9e5793eee09a0310fe875b3db1572`.
- Đã xác minh HEAD, SHA-256 của đặc tả và chứng cứ, nội dung spec/lease trên ref được giao, cùng byte của `diff.patch` so với diff Git thật.
- Reviewer: provider `openai_codex`, model family `openai`, model GPT-6 theo danh tính system của phiên; bề mặt quan sát là phiên Codex API có công cụ shell (`codex_service`), transport công cụ `machine/local`, môi trường Linux. Không có log đo model/effort từng request hoặc receipt launcher bên ngoài trong phạm vi đọc; không tự khai đã đo chúng.
- Không sửa nội dung `cay-kho/`; chỉ đặt `core.abbrev=7` theo chỉ thị tường minh của prompt. Sandbox thực tế `workspace-write`; quy tắc không sửa checkout còn dựa trên phân công reviewer. Worktree, kể cả ignored/untracked, sạch khi kiểm cuối. Snapshot đầu/cuối do phiên điều phối quản lý ngoài sandbox theo prompt, không phải phép đo do reviewer tự xác nhận.

### suy-cau-hinh-tu-su-kien-rong [P3]

- **Vị trí:** `cay-kho/docs/adr/0059-windows-local-nhip-tim-khoa.md:64–65`.
- **Lớp:** lời khai về cấu hình vượt phạm vi phép đo âm. Có 1 biểu hiện trong candidate này.
- **Bằng chứng:** ADR viết “máy không bật nhật ký tạo tiến trình (Security 4688 rỗng ngày 30-10)”. Trong `chung-cu-d10.txt:50–52`, phép đo được mô tả là `Get-WinEvent Security 4688 ngay 30-10`; output thực là `No events were found that match the specified selection criteria.` Dòng 52 là chú giải suy diễn, không kèm phép đọc cấu hình audit. Không tìm thấy sự kiện phù hợp chỉ chứng minh thiếu sự kiện trong kết quả truy vấn; nó chưa xác minh trạng thái bật/tắt audit của máy. Đây là lỗi lời khai nhỏ, không làm mất cận dưới giờ tạo PID dựa trên nguồn khác ở dòng 67–78.
- **Sửa cụ thể:** thay mệnh đề về bật/tắt bằng “không tìm thấy sự kiện Security 4688 ngày 30-10 trong lần đọc lại, nên không có số đo giờ tạo tiến trình từ nguồn này”. Không cần thay luật mục 2 hoặc kết luận D10.
- **Quét cùng lớp:** đã đối chiếu toàn bộ lập luận D10 ở dòng 62–78 với script và output gốc, cùng các lời khai số đo dòng 20–22, giới hạn nguyên tử dòng 52/84 và cổng dòng 90–93. Chưa thấy biểu hiện cùng lớp khác. Cận dưới từ `TAI_TRUOC` đã được gọi đúng là phép suy, không phải `CreationDate` đo trực tiếp.

## Ba ca

Các bước dưới đây dùng quy tắc trong ADR-0057/0058/0059; số liệu D10 được đối chiếu riêng với bản chứng cứ đã đóng băng.

### (i) A bị ngắt, quá hạn, B tiếp nhận, A kết nối lại

1. Khoá A quá hạn nên hết hiệu lực theo ADR-0058, mục 3(a), dòng 33–35. Tiến trình A đã dừng là dữ kiện của ca.
2. B áp ADR-0059, mục 2, dòng 33–37: kiểm tải theo ADR-0057 mục 4, không thấy tiến trình thuộc tiêu chí còn sống. B được tiếp nhận.
3. B theo thứ tự ADR-0058 dòng 38–40, được ADR-0059 dòng 39 giữ nguyên: kiểm tải → ghi sổ nêu session/UTC khoá A và lý do (a) → thay bằng dòng B. Dòng mới có năm trường theo ADR-0059 dòng 26–30.
4. A kết nối lại và định ghi nhịp tim/gia hạn: ADR-0059 mục 4, dòng 44–48, buộc đọc lại trước. Dòng hiện tại mang session B, không phải A; A không còn giữ khoá, không được ghi lại dòng A.
5. Với khoá B còn hiệu lực như ca mô tả tại dòng 58–60, A phải đợi. **Kết quả: dòng B giữ nguyên.** Không có nhánh nào cho A tự khôi phục quyền cũ vì đã từng giữ khoá. Nếu sau đó khoá B cũng hết hiệu lực, đó là một lần lấy khoá mới theo mục 2/4 và ADR-0058 mục 3, không phải gia hạn A.

### (ii) Khoá A quá hạn, chưa ai tiếp nhận, A kết nối lại

1. Quá hạn làm khoá hết hiệu lực theo ADR-0058 mục 3(a); ADR-0059 dòng 31–32 không thêm tiêu chí hết hiệu lực theo tuổi nhịp tim.
2. A đọc lại theo ADR-0059 dòng 44–45; dòng vẫn mang session A, nên không đi vào nhánh mất quyền ở dòng 46–48.
3. Dòng 49–51 quy định trực tiếp trường hợp này: A chạy bước kiểm tải rồi được gia hạn. ADR-0057 dòng 38–39 yêu cầu ghi nhận tiến trình không thuộc mình và cấm tự dừng chúng; bước đó tự nó không cấm gia hạn.
4. A ghi lại dòng A theo ADR-0059 dòng 27–30: giữ UTC bắt đầu lúc lấy khoá, nhịp tim là giờ hiện tại, hạn không quá hai giờ từ lần ghi. **Kết quả: A gia hạn được.** Không lấy điều kiện tiếp nhận khoá của phiên khác ở mục 2 để chặn A.

### (iii) D10

1. Dòng cũ của `session_015GtxrbUPS7zGdffB8Sfo8Y` không có hạn, UTC bắt đầu `2026-10-30T09:01:16Z`. Tới mốc tiếp nhận đã quá hai giờ: ADR-0058 mục 3(b), dòng 35, làm khoá hết hiệu lực; ADR-0059 dòng 62 nhắc đúng nhánh đó.
2. Phiên khác muốn tiếp nhận phải qua ADR-0059 mục 2, dòng 33–37. PID 26296 chạy `tl.py --selftest`, không phải MCP, được ghi trong sổ đo ở dòng 13:59:37Z (ADR-0059 dòng 20/62–63; chứng cứ dòng 47). Mốc thay dòng khoá thực là 14:01:44Z, trong khi lượt selftest kết thúc 14:03:16Z (chứng cứ dòng 33–34/48).
3. Điều kiện còn lại là giờ tạo PID sau UTC bắt đầu khoá. ADR-0059 dòng 64 và 78 phân biệt rõ thời lượng lượt, cận dưới suy được và `CreationDate` đo trực tiếp. Không dùng phép lấy giờ kết thúc trừ 18113 s làm giờ tạo PID; cũng không dùng kết luận về audit đang bị finding P3 để chứng minh điều kiện này.
4. ADR-0059 dòng 67–74 nêu nguồn có thể kiểm: script `C:\Users\admin\tl-work\session_015GtxrbUPS7zGdffB8Sfo8Y\selftest.ps1` ghi bắt đầu/khoá, ngủ 3 s, fetch/checkout, lấy toàn bộ `python.exe` bằng bộ lọc nêu rõ, rồi mới gọi Python selftest. Bản script nguyên văn ở chứng cứ dòng 85–108 khớp thứ tự, không có bộ lọc loại PID/session nào sau `Name='python.exe'`.
5. Output `BAT_DAU=2026-10-30T09:01:16.5807497Z` và `TAI_TRUOC` tại chứng cứ dòng 24–30 cho bốn PID 23252, 5772, 12720, 26716; không có 26296. Hai mục hiện đuôi `browser-use.exe` vẫn là kết quả của bộ lọc `python.exe`, đúng chú giải chứng cứ dòng 119–120. Mẫu nằm sau lúc ghi khoá và checkout; mốc ghi `scripts/tl.py` 09:01:22.7691466Z ở dòng 13 cũng khớp phần giải thích ADR.
6. Theo chuỗi chứng cứ đó, PID Python selftest được tạo sau mẫu, vì vậy sau 09:01:16Z; ADR-0059 dòng 76–78 chỉ nhận đây là cận dưới, không khai số đo `CreationDate`. Áp mục 2: khoá còn sống, **không tiếp nhận; ghi PID/lệnh vào sổ, đợi**. Không đi tiếp tới bước thay nội dung khoá của ADR-0058. Finding P3 ở mệnh đề về cấu hình audit không đổi kết quả này.

### Các biến thể gần

| Biến thể | Áp dụng câu nào | Kết quả |
|---|---|---|
| Chính tiến trình A còn chạy trong thư mục riêng khi A gia hạn dòng vẫn là A | ADR-0059 dòng 49–51, đối chiếu ADR-0057 mục 4–5 | Kiểm tải rồi gia hạn; tiến trình chính A không chặn. |
| Dòng bốn trường của ADR-0058 | ADR-0059 dòng 31–32; ADR-0058 mục 3(a) | Vẫn đọc như cũ; thiếu trường nhịp tim không tự làm hết hiệu lực. Gia hạn/nhịp tim mới ghi theo mẫu năm trường, không đổi UTC bắt đầu. |
| Dòng ba trường cũ, quá hai giờ, có Python không phải MCP tạo sau giờ bắt đầu | ADR-0058 mục 3(b), ADR-0059 mục 2 | Không tiếp nhận, dù chưa có trường hạn/nhịp tim. |
| Python tạo trước hoặc đúng giờ bắt đầu, hoặc tiến trình MCP | ADR-0059 dòng 35–37 dùng “sau” và loại MCP | Không thoả tiêu chí chặn mới; vẫn kiểm tải/ghi nhận và không dừng tiến trình theo ADR-0057 mục 4. |
| Khoá được chính chủ tuyên bố bỏ, có bằng chứng, nhưng tiến trình còn chạy | ADR-0058 mục 3(c), ADR-0059 dòng 38–39 | Không áp tiêu chí chặn mục 2; vẫn giữ kiểm tải → sổ đo → thay dòng, cấm dừng tiến trình phiên khác. |
| A định nhả nhưng đọc thấy dòng đã là B còn hiệu lực | ADR-0059 dòng 53 dẫn mục 4; dòng 45–48 xác nhận A không còn giữ khoá | A không ghi rỗng/xoá khoá B; đợi theo nhánh lấy khoá nếu còn cần máy. |
| A đọc thấy tệp rỗng khi kết nối lại | ADR-0059 dòng 46–48 | A không còn giữ khoá; kiểm tải rồi lấy mới, không gia hạn quyền cũ. |
| Lượt đỏ hoặc bị bỏ, dòng vẫn là của A | ADR-0059 dòng 53–54 | Đọc lại rồi nhả bằng tệp 0 byte, không giữ khoá vì lượt thất bại. |

Các bước trên không đóng khe giữa đọc và ghi; ADR-0059 dòng 52/84 và ADR-0058 dòng 48–49 đã khai rõ giới hạn không nguyên tử. Không coi đây là lỗi mới hoặc đòi công cụ ngoài spec.

## Đối chiếu Spec và Standards/Security

| Phạm vi | Bằng chứng trên candidate | Kết quả |
|---|---|---|
| Chỉ bổ sung phần khoá; giữ các điểm còn lại | ADR-0059 dòng 9–10, 82–86; Git so bytes hai ADR cũ với base | Đúng phạm vi; ADR-0057/0058 không bị sửa. |
| Nhịp tim, hạn, định dạng | ADR-0059 dòng 26–32 | Trường thứ năm; ít nhất mỗi 30 phút; hạn ≤ 2 giờ từ lần ghi; giữ UTC bắt đầu và tương thích dòng bốn trường. |
| Tiếp nhận còn tiến trình sống | ADR-0059 dòng 33–39 | Đủ kiểm tải, tên `python.exe`, so giờ UTC, loại MCP, sổ PID/lệnh, đợi; ngoại lệ 3(c) rõ. |
| Lượt bị ngắt và nguồn điện | ADR-0059 dòng 40–43; ADR-0057 mục 10 dòng 48–49; protocol §3.1 dòng 95–97 | Đủ `ngat=co`, khoảng mất truy cập nếu đo được, bỏ thời lượng khỏi rà soát, không tự đổi nguồn/ngủ. |
| Đọc lại/gia hạn/nhả | ADR-0059 dòng 44–54 | Đủ các nhánh bắt buộc và tệp 0 byte; xem ba ca/biến thể trên. |
| Số đo D10–D12 | ADR-0059 dòng 20–22 so spec dòng 21–23 | Ba hàng bằng nhau sau khi bỏ dấu backtick; tên phiên, PID, giờ, N/N, thời lượng và SHA không đổi. |
| Dẫn số mục ADR | ADR-0057 mục 3/4/5/10; ADR-0058 mục 3(a)/(b)/(c) | Đều tồn tại đúng nội dung được viện dẫn; số mục là số trong danh sách Quyết định. |
| Protocol §10.2 | Dòng 1015 | Con trỏ nhắc 0057/0058/0059, chỉ nêu nơi đặt quy ước, không tạo nghĩa vụ mới. |
| Protocol §20 | Dòng 1538–1539 | Đúng một hàng 0059, cột cổng đúng nguyên văn; hàng 0058 chỉ đổi ô mô tả để thêm con trỏ. |
| Không sao doctrine sang protocol | Diff thật của protocol + phép phục hồi về base trong `review_audit.py` | Chỉ có ba thay đổi được giao; hàng mới liệt kê phạm vi và dẫn sang ADR, không chép luật vận hành. |
| Không cổng cưỡng chế | ADR-0059 dòng 88–93; quét sáu tệp cổng được protocol §20 định danh | Không tìm thấy thuật ngữ khoá/nhịp tim/`CreationDate`/`ngat=co`/sổ đo ở sáu tệp đó; `adr-song` kiểm metadata/bảng, không thực thi luật khoá. |
| Security và phần không đổi | ADR-0059 dòng 82–86; toàn diff | Không đổi CI, credential, đường vào máy, phạm vi theo `list_devices`, cột sổ đo hoặc quyền dừng tiến trình; không viết công cụ hay sửa hồi tố. |

Đối chiếu nguồn tham chiếu:

- ADR-0059 dòng 3–7 khớp [comment duyệt đặc tả 6537481455](https://github.com/ducthangho/tra-luat/pull/1062#issuecomment-6537481455): tác giả `ducthangho`, đúng spec hash đầy đủ, blob `93f1248aeca8c0d229f0f896434115f246e7b621`, PR head `471ad5391c2bcc1d0ee7871907233313db28e9b6`, revision 3/generation 1 và mission `gh-1035`. Đã đọc bằng GitHub connector; phần cần dùng lưu tại `github-reference-evidence.json`.
- [PR #1062](https://github.com/ducthangho/tra-luat/pull/1062) đang mở, chưa merge, đúng head trên. Spec ở commit đó và ref lease có SHA-256 bằng bản đóng băng. Vì vậy chỉ dẫn tìm ở master rồi ref lease là phù hợp. Không dùng hash cũ trong thân PR thay cho hash đã được duyệt ở comment.
- [Issue #1035](https://github.com/ducthangho/tra-luat/issues/1035) tồn tại và là Mission chứa các packet vận hành sau #748; thông tin mission trong ADR/lease khớp. Không dùng nội dung issue để mở thêm phạm vi review.
- Git có các commit `356a27e1378b2162bbc0be2ec06ff08fdacbdead` (#1021, trailer session `session_015GtxrZ1Tt93F4NLUUhKYQy`) và `e9f7872b2fd71eacf30413c48aafdca4d76061ae` (#1030, trailer `session_015GtxrcrefBJpLr7fGUSPtB`), khớp vai trò phiên trong số đo. Session giữ khoá D10 khớp giữa bảng, đường dẫn script và output gốc; không có phép truy cập trực tiếp máy chủ kho trong lượt này.
- Base là merge PR #1049. Hồ sơ `ops/land/pr1029-windows-local-r2-land-evidence.yaml:207` có bản ghi bổ sung `landed: true`; ADR-0058 đã có trong base. D10–D12 được so với spec theo yêu cầu; chứng cứ D10 không được dùng như phép đo độc lập lại toàn bộ D11/D12.

## Đã chạy

Các lệnh Python kiểm cổng chạy trong `cay-kho/`, bật `PYTHONDONTWRITEBYTECODE=1` để không ghi cache vào checkout. `review_audit.py` chạy ở thư mục sandbox hiện tại. Rc dưới đây là mã thoát thật của tiến trình/lệnh.

| Lệnh | Rc | Kết quả thật |
|---|---:|---|
| `git -C cay-kho rev-parse HEAD` | 0 | `27b6effb633c11f268b6e66692d14458b6a647f4`, giữ nguyên khi kiểm cuối. |
| `git -C cay-kho rev-parse HEAD^{tree}` | 0 | `b9d6ae0622e9e5793eee09a0310fe875b3db1572`. |
| `git -C cay-kho rev-parse --is-shallow-repository` | 0 | `false`. |
| `sha256sum spec-r3.md chung-cu-d10.txt` | 0 | Lần lượt `f1a666a32161f0607ac27bc8c3be6963bb6367e64f02825635a75cc8185fa973`, `2e802ecf92f21c8c73552096344c9d6da3c5445aa82bd6534e838fdc9914d60a`. |
| `git -C cay-kho config core.abbrev 7` và `git -C cay-kho config --get core.abbrev` | 0 | Giá trị đọc lại `7`, đặt trước `doc-claims-check`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py adr-song --root .` | 0 | `adr-song: sạch — 58 ADR trên đĩa, 58 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` |
| `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/tl.py doc-claims-check --json` | 0 | JSON: `"ok": true`, `"files_scanned": 118`, `"claims_flagged": 381`, `"flags": []`, `"advisory_count": 381`, `"strict": false`. Các advisory không được gọi là hard failure hoặc số finding của review này. |
| `git -C cay-kho diff --numstat adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc HEAD` | 0 | `3 2 docs/PROTOCOL_DA_PHIEN.md`; `100 0 docs/adr/0059-windows-local-nhip-tim-khoa.md`. Tổng 2 tệp, +103/−2; đạt trần 2 tệp/+140. |
| `python3 -B review_audit.py` | 0 | `"ok": true`, 23/23 đối chiếu đạt; 2 tệp, 103 dòng thêm, 2 dòng xoá. Kiểm nguyên byte diff/spec/lease, write set, hai ADR cũ, đúng ô §20, con trỏ, cả ba hàng số đo, HEAD/tree và worktree sạch. |
| `rg -n 'audit\|4688\|CreationDate\|TAI_TRUOC\|không.*(bật\|đọc)\|Nguồn\|mẫu\|Vậy\|nên' cay-kho/docs/adr/0059-windows-local-nhip-tim-khoa.md chung-cu-d10.txt` | 0 | Định vị mệnh đề ADR dòng 64–65 và dữ liệu `Get-WinEvent`/chú giải ở chứng cứ dòng 50–52; dùng cho finding P3 và quét cùng lớp. |
| `rg --hidden -n -i 'CreationDate' cay-kho/.claude cay-kho/scripts cay-kho/ops --glob '*.py' --glob '*.ps1' --glob '!**/reviews/**' --glob '!**/land/**' --glob '!**/evidence/**'` | 0 | Chỉ có ba lần nhắc tên ca `t81_chup_cay_windows_thieu_creationdate_phai_fail_closed` trong `launcher_test.py`; không có consumer luật khoá mới. |
| `rg -n -i 'CreationDate\|KHOA\.txt\|ngat=co\|do-luong\.csv\|nhịp tim\|nhip tim' cay-kho/.claude/dev/launcher.py cay-kho/.claude/dev/packet_loop.py cay-kho/.claude/dev/gate_lifecycle.py cay-kho/ops/lease_publish.py cay-kho/.github/workflows/ci.yml cay-kho/.github/workflows/ops-publish-lease.yml` | 1 | Không có kết quả khớp; đây là rc “không tìm thấy”, không phải gate lỗi. |
| `git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored=matching` | 0 | Output rỗng; audit cuối cũng xác nhận sạch. |

Đã đọc có đánh số dòng ADR-0057/0058/0059, spec, chứng cứ D10 và các đoạn protocol §3.1/§8/§10.2/§13/§20; đã xem diff thật và Git object/trailer nêu trên (rc 0 ở các lượt đọc đúng đường dẫn). Một lượt đọc đầu gọi nhầm tên ADR-0058 không tồn tại trả rc 1; đã sửa đường dẫn và đọc đủ tệp đúng. Lỗi tra schema connector ban đầu trả `INVALID_ARGUMENT`; các lượt gọi đúng tham số sau đó đều `isError: false` và có dữ liệu PR/comment/issue. Không tính các lỗi tra cứu này là finding của candidate.

**Phần không đo:** không chạy Windows local, Windows CI, full selftest hoặc toàn worker/land gate; không truy cập máy ASUS-LAPTOP; không kiểm snapshot/launcher receipt do phiên điều phối giữ ngoài sandbox. Các cổng được yêu cầu riêng cho lượt review này đã chạy và đạt; kết luận vẫn `changes_requested` vì còn 1 P3 nêu trên.

Kiểm cuối: `git -C cay-kho diff --exit-code` và `git -C cay-kho diff --cached --exit-code` đều rc 0, output rỗng; HEAD/tree giữ nguyên các OID trên. Kiểm định dạng báo cáo bằng `python3 -B -` rc 0, output `report_format_ok=true; finding_classes=1; manifestations=1`; ba dòng đầu và mục cuối đúng khuôn yêu cầu.
