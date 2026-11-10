# WP1287 — thiết kế đo kế nhiệm R6

Trạng thái: **design_only / chưa triển khai helper / chưa admission / chưa cấp lease**.
Chỉ thị hiện hành của chủ kho: “Đồng ý, sửa thiết kế theo khuyến nghị”.
Người ghi: dispatcher `openai_codex / codex_service / machine`.
Write set của bước thiết kế: `ops/checkpoints/wp1287-r7-design/`.
Tên thư mục R7-design không kích hoạt Packet revision hoặc generation mới.

## 1. Đầu vào và giới hạn

- Control base: `3d512b4d26aa232b7f52920a4ba8982e95133eb9`.
- Acceptance B: `bf9914cb1a8e6f5047468f4d130b587015f8d73f`.
- Candidate H2: `2a5803e17b7ca4910c7188bfcc2276190e2d0b4b`, tree `bfb2fad8df2634ae8dd4c839a4565b76d1cfae45`.
- Advisory: run `8e843b37bb8a42dd9fe6fbd0656dbcec`, model thực `gpt-6-astra/xhigh`, rc0; [biên nhận](../wp1287-r6/advisory-completion.json). SHA256 bản trả lời native: `f141c784086d20d06b31009c00f1a4d9f6fdd9eaeff451b4aaa5d80d7f0ccd3f`.
- Shared3/8, design-advisory1/1, formal0/2, author3/3, productpush0/1; reservations0. R4 và R6 đều đã dùng riêng1/1, lease đã retired. Bước này không phát sinh model call, measurement, author4 hoặc allowance mới.

Mục tiêu là đo được startup/readiness và cleanup, đồng thời phân biệt lỗi quan sát với dữ liệu module/WCT. Không cần giả định nguyên nhân để làm cho phép đo đúng. Không đổi tiêu chuẩn native fullflow của r3 hoặc tự yêu cầu phải tìm ra nguyên nhân mới được xét bằng chứng compatibility.

Giữ đúng Desktop `a5f7076e-a491-4f84-829b-8d1fbcc1c767`, Node26.13.0/npm11.20.0, CLI0.1.23/core1.65.0-alpha-2026-10-30, full CFT1252/157.0.8103.15, channel chromium/headless/isolated, launch timeout30000. Giữ các action timeout gốc; không kéo dài timeout của lệnh đóng để làm mất lỗi R6. Không đổi launch flags, target, sandbox, policy, module hoặc profile để lấy PASS.

## 2. Các kết quả phải độc lập

| Trục | Giá trị | Bằng chứng tối thiểu |
|---|---|---|
| Admission | passed / failed / not_run | Exact source, runtime, scope, budget, ownership, lease và host fences |
| Startup | not_run / failed / acknowledged | Child rc, thời gian, nguyên stdout/stderr; rc0 chỉ là acknowledged |
| Readiness | not_run / unknown / failed / fixture_verified | URL của tab hiện hành và response bytes của fixture đúng nonce |
| Native fullflow | not_run / failed / passed | Toàn bộ proof native r3, gồm cài candidate, signatures, capture và cleanup |
| Observer quality | complete_walk / partial / unavailable / inconsistent | Kết quả từng API, identity bracket, timing và coverage |
| Cleanup | not_run / pending / failed / verified | Named commands, closed-session result đúng nonce và census theo identity |

Giữ riêng `open_cli_rc`, `operator_child_rc`, `transport_shell_rc` và lỗi của từng stage. Lưu cả trường hợp Windows shell trả1 trong khi child trả2; không suy chúng là cùng một lỗi. Một lỗi cleanup không sửa lại kết quả startup. `skipped/not_run/unknown` không được đổi thành passed.

Chỉ ghi run success khi các proof bắt buộc của mode đã chọn và cleanup đều đạt. Một flow có capture đạt nhưng cleanup thất bại vẫn là run thất bại. Observer không đầy đủ làm giới hạn kết luận chẩn đoán; nó không tự biến một phép capture thành công thành bằng chứng loader hỏng, hoặc tự thêm gate mới vào acceptance sản phẩm. U10/Packet không tự đóng từ trường `open_cli_rc=0` hay từ báo cáo helper.

## 3. Identity và timeline

1. Tạo `run_id` và session nonce mới; đóng băng command/config/fixture/source hashes trước launch. Ghi thời điểm UTC và monotonic nanoseconds từ cùng một máy. Thời lượng và thứ tự dựa trên monotonic; UTC dùng đối chiếu log, không thay monotonic khi đồng hồ bị chỉnh.
2. Neo tiến trình bằng PID **và creation time** từ process handle, image path, vai trò và cạnh parent/child đã quan sát. Giữ handle query tới khi thu exit. PID trần hoặc image nằm dưới cache không đủ chứng minh ownership.
3. Bắt đầu census trước launch; ghi từng gap thực tế. Nếu mất cạnh parent hoặc không xác minh được birth time thì ownership là UNKNOWN. Không suy PID browser từ trường `pid` trong CLI JSON trước khi xác minh ý nghĩa của trường trong source CLI đã ghim.
4. Profile tạm chỉ được nhận là owned khi có liên kết với session/tiến trình của lượt này và được tạo mới. Không đọc cookie/profile contents; không tìm rồi xóa mọi thư mục có tên tương tự trong TEMP.
5. PID bị tái sử dụng, handle/query bị từ chối hoặc identity thay đổi làm mẫu không hợp lệ. Không tiếp tục thao tác cleanup theo PID đó.

Mỗi probe có `scheduled_offset_ns`, `actual_start_mono_ns`, `actual_end_mono_ns`, UTC, scheduling lag, identity trước/sau và trạng thái hoàn thành. Nhãn5/15/25 là lịch dự kiến, không phải thời gian lấy mẫu thực tế.

## 4. Liệt kê module có kiểm soát lỗi

Dùng observer64-bit đã xác minh ABI, `TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32` cho đúng owned PID. Ghi flags, bitness và `dwSize`. Mỗi lời gọi BOOL có `SetLastError(0)` trước đó; khi thất bại phải chụp `GetLastError` ngay, trước mọi WinAPI/cleanup khác. Không diễn giải last-error còn sót từ một lời gọi thành công.

| Điểm đo | Xử lý bắt buộc |
|---|---|
| `CreateToolhelp32Snapshot` thất bại | Ghi mã lỗi và attempt. Chỉ `ERROR_BAD_LENGTH(24)` được thử lại một lần ngay trong cửa sổ probe đã đóng băng; tổng tối đa2 snapshot attempts. Hết cửa sổ hoặc lỗi khác ⇒ unavailable. Đây không phải quyền launch browser lại. |
| `Module32FirstW` trả FALSE | Ghi mã lỗi, entries0 và trạng thái unavailable/empty_snapshot. Kể cả `ERROR_NO_MORE_FILES(18)` cũng không đủ để gọi một live Chrome “không có module”. |
| `Module32NextW` trả FALSE với18 | Kết thúc API walk bình thường nếu đã có main-image entry và identity bracket hợp lệ. |
| `Module32NextW` trả FALSE với mã khác, kể cả0 | Partial; giữ các entries đã thu nhưng không dùng sự thiếu entry để suy module vắng mặt. |
| Main image không khớp, PID/birth thay đổi, duplicate/inconsistent entries | Inconsistent; giữ dữ liệu thô và không kết luận absence. |

`complete_walk` chỉ mô tả một lần đi hết danh sách API-visible trong snapshot. Nếu không có `chrome.dll`, nhãn kết quả là `NOT_LISTED_IN_COMPLETE_WALK`, không phải “DLL thực sự chưa được nạp” hoặc “kẹt loader”. Toolhelp có giới hạn khi loader đang khởi tạo/thay đổi; không thấy module còn có thể phản ánh giới hạn quan sát. `partial/unavailable/inconsistent` ⇒ module presence UNKNOWN. Không đưa ra kết luận trên toàn lượt chạy từ vài mẫu định kỳ.

Đặt các mốc dự kiến5/15/25s và **một probe sau khi open kết thúc** nếu owned process vẫn sống. Ghi `not_run_process_exited`, `identity_unknown` hoặc `deadline_exhausted` nếu không thể lấy probe sau-open; không dùng lại mẫu25s để thay. Có snapshot cuối trước cleanup khi còn đủ thời gian, nhưng nó không được trì hoãn cleanup.

## 5. Nối module với tệp và giới hạn WCT

Khi module được liệt kê: lưu module base/size, đường dẫn thực API trả về và process identity cùng thời điểm trong bằng chứng native. Mở đúng đường dẫn đã quan sát bằng quyền đọc tối thiểu, giữ sharing thông thường để không khóa cập nhật của ứng dụng khác. Ghi final path, volume/file identity, size/mtime và thời điểm hash; đối chiếu lại sau khi hash. Thay đổi tệp hoặc read bị từ chối ⇒ bridge UNKNOWN. Không lấy một tệp cùng basename ở nơi khác làm bằng chứng cho module đã nạp.

Hash là của tệp trên đĩa đã quan sát, không chứng minh loaded memory bytes giống tệp đó. Không dump bộ nhớ để nâng mức khẳng định. Raw path/file identity giữ native; phần chia sẻ chỉ dùng allowlisted summary/hash đã có quyền. Module `uvh64.dll` xuất hiện không tự chứng minh UltraViewer hoặc injection gây lỗi.

WCT giữ nguyên flags0, tối đa16 nodes/lần và64 owned threads/probe; ghi rõ thread count, phần bị cắt, từng API error, cycle flag và type/status. `WaitTime` giữ tên/value theo API, không tự gán đơn vị `ms`. Không có lock node/cycle chỉ có nghĩa chưa quan sát được quan hệ đó trong mẫu, không loại trừ deadlock/I/O/loader delay.

Observer phải có deadline riêng và không chặn luồng theo dõi open/readiness/cleanup. Implementation cần worker sở hữu riêng hoặc cơ chế async có timeout đã kiểm chứng; observer timeout ⇒ UNKNOWN, không tăng timeout browser. Không nâng SeDebugPrivilege, không dump private process, không đọc đối tượng ngoài scope. Ghi overhead, peak memory và sampling gaps của observer; không coi R4/R6/R7 là A/B chỉ vì cùng pin.

## 6. Readiness và đường đi fullflow

Future Packet phải chốt mode trước khi chạy: `readiness_diagnostic` hoặc `candidate_native_fullflow`. Không tự chuyển mode giữa chừng. Cả hai chỉ có một lần open; mode đầu không được gọi U10 fullflow PASS.

Chuẩn bị HTTP fixture chỉ bind loopback, không có script/resource ngoài, với body UTF-8 cố định chứa nonce của run. Freeze requested redirect URL, expected final URL, status302→200, body bytes/length/hash trước open. Cổng do OS cấp phải được ghi từ socket đã bind thật; không mở endpoint ngoài loopback.

1. Kiểm source-byte bridge H2 và runtime/pin trước launch. Mode native-fullflow còn phải có candidate install/signatures/browser provenance theo r3; không mượn survey/H1 làm candidate proof.
2. Open `about:blank` đúng một lần bằng config/timeout gốc. Ghi argv, start/end, child rc, output shape và nonce. Rc khác0 hoặc metadata không hợp lệ ⇒ startup failed, không chạy các bước capture phụ thuộc.
3. Rc0 chỉ chuyển thành acknowledged. Dùng `tab-list` của đúng nonce để xác nhận query thành công, không có error và có một current tab theo schema đã ghim trước khi navigation; query này không được phép tự launch browser. Thiếu URL about:blank chỉ ghi UNKNOWN cho URL ban đầu, không thêm một acceptance gate mới. Không chứng minh được session/query hợp lệ ⇒ dừng dependent actions. Readiness thực sự vẫn chờ fixture ở bước4–5.
4. `goto` fixture một lần; lưu nguyên output `tab-list` và `requests --static`. Xác nhận duy nhất current tab ở expected final URL và đúng chuỗi redirect/status. Chọn request index từ chính output lượt này, không hardcode index từ lần trước.
5. Dùng `response-body` vào đường dẫn tuyệt đối và so bytes/hash với expected UTF-8 fixture, gồm nonce. Tất cả đạt mới ghi `fixture_verified`. Đây là proof browser phục vụ controlled source, độc lập với rc của lệnh open hoặc empty snapshot.
6. Trong mode native-fullflow mới chạy PNG/PDF theo r3, kiểm kích thước PNG, PDF parse được và có marker fixture. Lỗi ở bước trước ⇒ các bước sau not_run, không chạy lại để “xanh hóa”. Giữ timeout/action semantics gốc.

Operator có thể kiểm wrapper JSON và fixture có dạng cố định. Việc đọc Markdown `tab-list`/request index theo đúng hợp đồng SKILL hiện hành phải được ghi rõ; không thêm parser web tổng quát, eval, CDP, thư viện thay CLI hay adapter vào sản phẩm. Response-body text là dữ liệu đã giải mã rồi ghi UTF-8; phép so với fixture UTF-8 cố định không được mô tả là hash byte trên dây/TLS. Một snapshotfile rỗng của about:blank không chứng minh thành công hoặc thất bại.

## 7. Cleanup, khóa và terminal

Cleanup chạy từ mọi nhánh lỗi sau khi attempt có thể đã tạo tài nguyên. Mỗi close/delete/verify có command record, stdout/stderr và child rc riêng; tên output mới, không ghi đè bằng chứng trước. Giữ timeout cleanup đã chốt; timeout là một failure thật, không âm thầm nới rồi đổi thành PASS.

Thứ tự: named close → named delete-data → expected closed-session query của đúng nonce theo mẫu r3 → census owned process/observer handles. Rc0 riêng lẻ không đủ. Lỗi start process, JSON sai/rỗng, sai nonce, rc lạ hoặc verification error không đúng mẫu ⇒ cleanup chưa được chứng minh.

Không nhả khóa trong `finally` trước khi kiểm cleanup. Chỉ nhả sau `cleanup=verified`, census không còn tiến trình owned và đọc lại lock vẫn là session của mình. Nếu lock đã đổi chủ thì không ghi đè. Nếu còn owned process hoặc ownership UNKNOWN: ghi `cleanup=pending/failed`, terminal nonzero và handoff paused, giữ deadline/heartbeat/ownership rõ theo ADR57–59. Không tuyên bố lock expired là đủ chứng minh máy rảnh.

Không kill-all hoặc kill theo cache prefix/PID trần. Nếu future scope cho phép last-resort terminate owned process, phải có quyền cụ thể và kiểm handle/PID/birth/image/lineage ngay trước thao tác; không chứng minh được thì không terminate. Việc recovery về sau được append thành receipt riêng, không xóa timeout hay terminal lỗi ban đầu. Ledger ghi riêng startup/readiness/fullflow/observer/cleanup và cả child/shell rc.

## 8. Các ca phản chứng phải có trước admission

| Ca | Kết quả bắt buộc |
|---|---|
| First FALSE/18, entries0 trên live PID | empty_snapshot; presence UNKNOWN |
| Next FALSE/5 sau vài entries | partial; không được kết luận DLL vắng mặt |
| Walk kết thúc18, main image/identity hợp lệ, không có DLL | NOT_LISTED_IN_COMPLETE_WALK; không gọi loader hang |
| PID được tái sử dụng giữa probe/cleanup | identity invalid; không thao tác PID mới |
| Basename trùng nhưng path/file identity không nối được | hash bridge UNKNOWN |
| Open0 và empty snapshotfile | acknowledged; readiness UNKNOWN |
| Tab/response status đúng nhưng body khác nonce | readiness failed; không capture tiếp |
| Fullflow đạt nhưng close timeout/census còn process | run failed; khóa chưa được nhả; recovery append riêng |
| Missing/malformed command output, hoặc closed-session khác nonce | cleanup failed, không CLEANUP OK |
| Child operator2 nhưng shell1 | giữ cả hai; không gán lỗi này cho open |

Các ca này là yêu cầu thiết kế, **chưa phải test đã chạy**. Implementation phải kiểm observer ABI/API errors với own-process/controlled fixtures trước khi xin thực thi browser. Không dùng fixture assertion phản chiếu code để tự chứng nhận native behavior.

## 9. Điều kiện bước tiếp theo

Thiết kế sửa xong không phải execution grant. Trước run cần helper kế nhiệm đáp ứng các ca trên, exact helper/source/config/fixture hashes, new spec/descriptor/generation/lease/host ownership và allowance hữu hạn được ghi trước. Stage chuẩn bị và đo có deadline tách biệt; mỗi stage phải nằm trong host-lock deadline ≤2h và heartbeat theo ADR57–59. Nếu đề xuất ngưỡng RAM/idle thì ghi trước dưới dạng điều kiện vận hành, không gọi đó là tiêu chuẩn U10 mới hoặc bằng chứng OOM.

Current design measurement allowance: **chưa cấp**, used0/reserved0. Không tự tăng author3/3 hoặc design-advisory1/1; formal/sensitive assurance, current-base gates, PRCI/MCI/M8 và dependency vẫn giữ. Không WindowsCI/full Windows mutant CI, rollout hay LIVE. Không sửa ba tệp sản phẩm của H2 trong bước thiết kế này.

## 10. Nguồn API

- [Module32FirstW](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-module32firstw): phân biệt thất bại lấy entry đầu với danh sách đi hết.
- [Module32NextW](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-module32nextw): ghi mã kết thúc walk ngay khi FALSE.
- [CreateToolhelp32Snapshot](https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/nf-tlhelp32-createtoolhelp32snapshot): flags/bitness, BAD_LENGTH/PARTIAL_COPY và giới hạn khi loader thay đổi. Thiết kế này cố ý giới hạn retry thay vì vòng lặp vô hạn.
- [WAITCHAIN_NODE_INFO](https://learn.microsoft.com/en-us/windows/win32/api/wct/ns-wct-waitchain_node_info): type/status, WaitTime và ContextSwitches; không suy lock cause khi chỉ có thread nodes.
