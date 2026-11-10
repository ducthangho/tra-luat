# WP1287 R8 — native readiness đạt, capture vẫn chặn

Đo đúng một lượt ở Desktop được chỉ định, source H2 `2a5803e17b7ca4910c7188bfcc2276190e2d0b4b` / tree `bfb2fad8df2634ae8dd4c839a4565b76d1cfae45`. Spec r8, helper thực thi và grant đóng băng tại `7c3be4e8c6fbfe6a974581ea7c132fdce9290fb5`. Các helper sửa sau run không được hồi tố vào byte đã thực thi. Ba tệp sản phẩm không đổi, candidate chưa push.

| Bằng chứng thực tế | Kết quả |
|---|---|
| Counterexamples trước run | Linux11/11 và Desktop11/11 |
| Native observer selfcheck | 64-bit, ME1080/WN280, complete walk29modules/4threads |
| Fresh exact-H2 installation | npm-ci/signatures/browser-install rc0, lock không đổi, hash nguồn/helper/CFT khớp |
| Open | rc0, khoảng3,317s, acknowledged |
| Browser readiness | Một current tab đúng final URL, redirect302→200, response-body UTF8 đúng nonce/hash |
| PNG | CLIrc1, Timeout5000ms; không coi partial output là PNG proof |
| PDF | not_run do PNG thất bại |
| Native fullflow | FAILED; U10 OPEN |
| Observer | 18 complete API walks; post-open8/8 workers hoàn tất, deadline0 |
| Cleanup | close0/delete0/expected-closed1, đúng nonce, stderr rỗng; ownership gaps0, remaining0 |
| Khóa | Giữ qua lỗi reporting; recovery đọc lại proof rồi nhả, readback khóa trống |

Khác R6: `chrome.dll` được liệt kê trong14/18 snapshots, chrome_elf18/18 và uvh64.dll8/18. Đây là quan sát API-visible của từng process, không chứng minh module vắng thật ở các mẫu khác, không chứng minh tính toàn vẹn bộ nhớ và không quy lỗi cho UltraViewer. Call-log screenshot có “taking page screenshot”, “waiting for fonts”, “fonts loaded”; không đủ xác định nguyên nhân timeout. Min free RAM1.139.863.552bytes, min free commit6.057.926.656bytes, peak working set observer được đo19.316.736bytes; không suy OOM hoặc quan hệ nhân quả từ số đo này.

## Reporting failure và recovery

Sau khi cleanup commands/census hoàn tất, glob `probe-*.json` đọc nhầm `probe-schedule.json` (array) như probe dict, gây AttributeError. Original Python child và shell thực trả1; giá trị2 là mã operator dự kiến cho failed measurement, không phải mã thực đã thoát. Lỗi xảy ra trước terminal/manifest/ledger và trước release lock. Raw measurement/helper không bị ghi đè và không chạy lại browser.

`recover_terminal.py` chỉ đọc bằng chứng/identity, kiểm lại ba phản hồi cleanup và census, ghi receipt/ledger riêng, nhả khóa khi proof hợp lệ; recovery child/shell0. Native receipt SHA256 `c2e29c44683da5537fdca77ac025b11dfd5fd35580381b7d3bed79762bca8937`. `native-summary.json` là phép chiếu JSON tương đương được ghi lại với newline của Cloud, không giả là byte-identical native file. Raw stdout/probe paths/profile tiếp tục giữ native; bản chia sẻ chỉ có summary và hashes được cho phép.

Lỗi glob đã sửa trên helper cho lần sử dụng tương lai: chỉ nhận probe số, loại schedule/identity sidecars và giữ malformed actual probe là unavailable. Hai regression dùng tệp thật, không browser; Linux tổng13/13. Bản sửa sau run chưa chạy lại native/fullflow và không được mô tả là candidate PASS.

## Terminal

Allowance R8 used1/limit1, reservation0; lease g8 retired sau cleanup/readback. R4/R6 vẫn retired/exhausted. Author3/3, shared3/8, design1/1, formal0/2, productpush0/1 giữ nguyên. Không model call mới, không product edit, không timeout/pin/target đổi, không global kill/policy/AV/auth/profile mutation, không WindowsCI/LIVE/merge/land.

OP-F01 formal OPEN; hai mẫu PowerShell positive fullflow còn thiếu và sensitive assurance HOLD. Không có actual runtime remediation được chứng minh trong scope này; repeating capture hoặc nới timeout không phải cách đóng U10. Dừng allowance đã chốt, giữ checkpoint này làm đầu vào quyết định kế nhiệm. Không tự gắn Mission complete khi P2 chưa đạt.
