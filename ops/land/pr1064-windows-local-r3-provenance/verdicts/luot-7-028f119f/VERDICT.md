verdict: approved
reviewed_sha: cb9bd240c269811f14331b827879b271498c6628
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

Đã review cả **Spec** và **Standards/Security**, áp ngưỡng của packet `sensitive`: hết P0–P3. Không phát hiện finding có bằng chứng trên candidate này. Tổng: **0 lớp finding, 0 biểu hiện**.

Tree: `0cbbc58aa8f6a6a887317029ed7511a83baa0b9b`. Reviewer `openai_codex`, `execution_surface: codex_cli`, `transport: machine`, run `028f119fb8084bc58aab08887b9039a7`; nguồn nhận dạng bề mặt/transport là `../run/028f119f/run.json` của chính lượt này. Họ model GPT-6 theo chỉ dẫn hệ thống; model ID/effort phục vụ từng request không đo độc lập. Executor theo lease là `anthropic_claude`, `claude-opus-5-5`, Claude Code remote Linux. Reviewer dùng phiên mới, không có ngữ cảnh Executor.

## Đối chiếu đặc tả và lời khai

Vị trí dưới đây tính trong `cay-kho/`; số dòng là của exact HEAD được review.

| Yêu cầu | Bằng chứng và kết quả |
|---|---|
| Neo và đầu vào bất biến | HEAD đúng yêu cầu; clone không shallow. SHA-256 `spec-r3.md` = `f1a666a32161f0607ac27bc8c3be6963bb6367e64f02825635a75cc8185fa973`; `chung-cu-d10.txt` = `2e802ecf92f21c8c73552096344c9d6da3c5445aa82bd6534e838fdc9914d60a`. Spec trùng từng byte với blob `93f1248aeca8c0d229f0f896434115f246e7b621` ở ref lease đã cấp. |
| Phạm vi diff và merge master | Diff `b653574b117fa1496fbf58f09a22a8cbed5cc5dc..HEAD` đúng hai tệp write set, **103 dòng thêm / 2 dòng xoá**. Diff lease base `adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc..HEAD^1` cũng đúng hai tệp, cùng số dòng. Hai parent là `c13505a2c36a70c47f5c740146fd5ad6794a9882` và master nêu trên; master là tổ tiên của HEAD. Diff `HEAD^1..HEAD` trên hai tệp packet rỗng: merge không thêm thay đổi vào chúng. `diff.patch` trùng byte với diff Git thật. ADR-0057/0058 không bị sửa. |
| Nhịp tim | ADR-0059:26–32 có trường thứ năm, giờ hiện tại, ít nhất 30 phút một lần, hạn ≤2 giờ kể từ lần ghi; giữ UTC bắt đầu khi gia hạn. Không dùng tuổi nhịp tim làm điều kiện hết hiệu lực mới; dòng bốn trường vẫn đọc theo ADR-0058. Khớp spec:29–32. |
| Tiếp nhận khoá còn tiến trình | ADR-0059:33–39 áp cho **khoá phiên khác** theo 3(a)/(b), kiểm tải theo ADR-0057 mục 4; so `CreationDate` UTC với UTC bắt đầu, lọc `python.exe`, loại MCP; thấy tiến trình phù hợp thì ghi PID/lệnh và đợi. 3(c) được loại trừ tường minh. Giữ thứ tự kiểm tải → ghi sổ → thay dòng của ADR-0058:38–40. Khớp spec:33–36. |
| Lượt bị ngắt | ADR-0059:40–43 ghi `ngat=co` vào `ghi_chu`, khoảng ngắt nếu đo được, loại thời lượng khỏi rà soát ADR; giữ quyền thay power policy ở chủ kho. Tham chiếu ADR-0057 mục 10 tồn tại ở dòng 48–49; protocol §3.1 dòng 95–97 thực sự cấm tự sửa power policy. Khớp spec:37–40. |
| Đọc lại và gia hạn | ADR-0059:44–52 chỉ cho ghi lại dòng còn đúng chủ, phân biệt mất khoá với khoá của mình quá hạn, giữ đường lấy mới khi tệp rỗng/khoá khác hết hiệu lực. Gia hạn của chính chủ không bị mục 2 chặn bởi tiến trình của mình. Không khai đọc lại làm khoá nguyên tử. Khớp spec:41–47. |
| Nhả khoá | ADR-0059:53–54 yêu cầu 0 byte, đọc lại theo mục 4 và nhả ngay khi xong, kể cả đỏ/bỏ. Kết hợp điều kiện đúng chủ ở dòng 45–48 để bảo vệ khoá đã sang phiên khác. Khớp spec:48–49. |
| D10–D12 | ADR-0059:20–22 trùng ba dòng spec:21–23 sau khi bỏ dấu backtick định dạng. D10 khớp thêm nguồn gốc tại `chung-cu-d10.txt`:24–34, 46–48. 14:03:16Z − 14:01:44Z = 92 giây, phù hợp “khoảng 1,5 phút”; D12 từ 21:17:25Z đến ~01:35Z hôm sau là hơn 4 giờ. D11/D12 được đối chiếu với spec đóng băng; không khai đã đọc lại máy Windows. |
| Protocol §20 | Dòng 1539 có đúng một hàng ADR-0059, cột cổng đúng `không cổng — kỷ luật executor`. Dòng 1538 chỉ thêm `; khoá bổ sung bởi ADR-0059` vào ô mô tả ADR-0058, giữ các ô khác. Câu tại dòng 1015 chỉ dẫn nơi chứa quy ước, nhắc đủ 0057/0058/0059 và trung tính. Phép dựng lại toàn bộ protocol từ master chỉ bằng ba chỉnh sửa cho phép khớp từng ký tự; không có doctrine mới chép vào protocol. |
| Những điểm giữ nguyên và security | ADR-0059:9–10, 31–32, 38–39, 80–86 bảo toàn phạm vi, khoá/sổ theo máy, 3(a)–(c), cột sổ đo, check CI, cô lập và cấm dừng tiến trình phiên khác. Không thấy nghĩa vụ mạnh hơn/rộng hơn spec hoặc xung đột mới với phần được giữ của ADR-0057/0058. |
| Lời khai cổng | ADR-0059:88–93 phân biệt kiểm metadata với cưỡng chế nội dung. Quét sáu tệp cổng được protocol §20 liệt kê không thấy `KHOA.txt`, `CreationDate`, `ngat=co`, `UTC nhịp tim` hoặc ADR-0059. Đã đọc `cmd_adr_song`: kiểm số/tên/trạng thái/hàng ADR, không thực thi các luật khoá. Không coi scanner xanh là bằng chứng đã cưỡng chế luật. |

Đã đọc trực tiếp [comment duyệt của chủ kho trên PR #1062](https://github.com/ducthangho/tra-luat/pull/1062#issuecomment-6537481455): actor `ducthangho`, association `OWNER`, lúc `2026-10-31T01:57:22Z`, duyệt đúng hash đầy đủ, blob `93f1248a…`, head đặc tả `471ad5391c2bcc1d0ee7871907233313db28e9b6` và lease r3 g1 mission gh-1035. Vì vậy khai `Accepted` và mốc authority tại ADR-0059:3–7 khớp nguồn. [PR #1062](https://github.com/ducthangho/tra-luat/pull/1062) tồn tại, còn mở tại lúc đọc; [Issue #1035](https://github.com/ducthangho/tra-luat/issues/1035) tồn tại với đúng vai trò Mission. Dùng comment duyệt exact hash, không dùng hash cũ trong thân PR làm authority. Trích xuất dữ liệu đọc được lưu ở `remote-evidence.json`.

Các session trong D10/D11/D12 trùng spec; hai session D10 còn khớp bản chép gốc. Các commit `757bde561d09738858506aecf5de2f050a5f0d5e`, `356a27e1378b2162bbc0be2ec06ff08fdacbdead`, `e9f7872b2fd71eacf30413c48aafdca4d76061ae` đều resolve trong kho đầy đủ. Các tham chiếu ADR-0058 mục 3, ADR-0057 mục 3/4/5/10 tồn tại và chỉ đúng chủ đề được viện dẫn.

Đã quét toàn bộ ADR-0059 theo các lớp rủi ro: mở rộng luật ngoài spec; ghi/gia hạn/nhả sai chủ; chặn gia hạn đúng chủ; suy đo vượt nguồn; tham chiếu và lời khai cổng sai. Không phát hiện biểu hiện có bằng chứng. Bundle không có verdict cũ; không xác nhận đóng finding lịch sử hoặc suy slug từ thông điệp commit.

## Ba ca

### (i) A bị ngắt, quá hạn; tiến trình đã dừng; B tiếp nhận; A kết nối lại

1. Hạn của A đã qua: ADR-0058:33–34 xác định hết hiệu lực theo 3(a). ADR-0059:31–32 không thêm điều kiện hết hiệu lực khác.
2. B làm bước kiểm tải theo ADR-0059:33–37 và ADR-0057:38–39. Theo tiền đề, không còn tiến trình phù hợp của A; giả thiết ca tại ADR-0059:58–59 cũng nêu không thấy tiến trình nào theo mục 2. Vì vậy mục 2 không cấm tiếp nhận.
3. B ghi dòng sổ đo nêu session/UTC/lý do 3(a), rồi thay dòng khoá bằng dòng của B theo ADR-0058:38–40 và ADR-0059:39. B đã lấy khoá hợp lệ.
4. A kết nối lại, phải đọc trước theo ADR-0059:44–45. Thấy `session_id` của B thì điều kiện cho A ghi lại không đạt; ADR-0059:46 xác định A không còn giữ khoá.
5. Khi khoá B còn hiệu lực, ADR-0059:47 bắt A đợi. A không được nhịp tim, gia hạn hoặc nhả thay B; bước nhả cũng phải qua mục 4 theo dòng 53. Kết quả: **dòng của B giữ nguyên**, khớp ví dụ ADR-0059:58–60 và yêu cầu spec.

### (ii) Khoá A quá hạn, chưa ai tiếp nhận; A kết nối lại

1. Hết hạn theo ADR-0058:33–34. Quy tắc này không tự xoá tệp hoặc đổi session trong dòng.
2. A đọc lại theo ADR-0059:44–45 và thấy dòng vẫn của chính mình. Không đi vào nhánh “đổi sang phiên khác hoặc tệp rỗng” ở dòng 46.
3. ADR-0059:49–51 cho phép chính trường hợp dòng vẫn của A, quá hạn, chưa ai tiếp nhận: A chạy kiểm tải rồi gia hạn. ADR-0057:38–39 yêu cầu ghi nhận tải ngoài phiên và không tự dừng tiến trình; không đặt lệnh cấm gia hạn vì tải ấy.
4. Tiến trình trong thư mục riêng của A không chặn gia hạn, vì ADR-0059:50–51 loại trừ rõ việc áp mục 2 cho khoá của chính mình. A ghi lại với UTC bắt đầu giữ nguyên, nhịp tim hiện tại, hạn mới ≤2 giờ kể từ lần ghi theo dòng 26–30. Kết quả: **A gia hạn được**; ADR-0059:61 cũng nêu đúng kết quả này.

### (iii) D10

1. Dòng cũ của `session_015GtxrbUPS7zGdffB8Sfo8Y` có UTC 09:01:16Z và không có hạn (ADR-0059:20, 62). Đến thời điểm tiếp nhận đã hơn 2 giờ: thuộc ADR-0058:35, 3(b).
2. Phiên khác phải kiểm tải trước tiếp nhận theo ADR-0059:33–37. Ca tại dòng 62–63 cho biết thấy PID 26296 chạy `tl.py --selftest`, không phải MCP. Còn phải xác lập nó tạo sau giờ bắt đầu khoá.
3. ADR-0059:64–65 nói rõ sổ đo không có `CreationDate`; 18113 giây không phải giờ tạo tiến trình; truy vấn Security 4688 không tìm thấy sự kiện phù hợp. Do đó không dùng ba thứ này để giả lập số đo `CreationDate` hoặc kết luận máy không bật audit.
4. Dòng 67–74 xác định nguồn thay thế: script đã ghi khoá, ngủ, fetch/checkout, rồi lấy mẫu **mọi** `python.exe` thành `TAI_TRUOC`, sau đó mới gọi selftest. Đối chiếu `chung-cu-d10.txt`:56, 89–108 xác nhận path, mốc sửa 09:00:26Z, bộ lọc không loại PID và thứ tự đó. Dòng 13 của chứng cứ ghi checkout `scripts/tl.py` lúc 09:01:22.7691466Z, sau UTC bắt đầu khoá; mẫu trong script được lấy sau checkout.
5. `TAI_TRUOC` tại `chung-cu-d10.txt`:30 liệt kê 23252, 5772, 12720, 26716; không có 26296. Sổ đo tại dòng 47 ghi thấy PID 26296 chạy selftest lúc 13:59:37Z. Vì mẫu phủ đúng loại tiến trình và được lấy sau giờ bắt đầu khoá, sự vắng PID ấy cung cấp cận dưới giờ tạo sau mẫu, như ADR-0059:76–78 trình bày. Đây là suy luận có nguồn, không phải số đo trực tiếp.
6. Cận dưới đó thoả điều kiện “khởi động sau UTC bắt đầu” ở ADR-0059:35. Chưa có bằng chứng 3(c) trong ca. Áp dòng 36–37: khoá còn sống, **không tiếp nhận; ghi PID và lệnh vào sổ đo, rồi đợi**. Không đi tới bước thay dòng khoá của ADR-0058:39.

### Biến thể gần đã đọc xuyên luật

| Biến thể | Đường đi và kết quả |
|---|---|
| A gia hạn trong khi selftest của A còn chạy | Dòng còn của A → ADR-0059:49–51 cho gia hạn sau kiểm tải; chính tiến trình của A không chặn. Giữ UTC bắt đầu theo dòng 29. |
| Dòng bốn trường của ADR-0058 | ADR-0059:31–32 giữ cách đọc cũ. Có trường hạn thì xét 3(a), không biến thành dòng ba trường thuộc 3(b). Gia hạn thêm trường nhịp tim theo dòng 26–30; không có luật từ chối vì thiếu nhịp tim. |
| Dòng ba trường dạng cũ | Xét tuổi từ UTC bắt đầu theo ADR-0058:35; khi tiếp nhận theo 3(b), vẫn phải qua ADR-0059 mục 2. D10 là một ca cụ thể. |
| A xong lượt nhưng dòng đã của B còn hiệu lực | ADR-0059:53 dẫn về mục 4; dòng 45–47 không cho A ghi/xoá dòng B. A không còn là phiên giữ khoá để thực hiện câu “nhả ngay”. Tệp rỗng chỉ được ghi khi A còn quyền giữ khoá. |
| Dòng đã của B và cũng hết hiệu lực | A không được dùng quyền giữ khoá cũ để xoá B. Phải đi đường lấy mới theo dòng 46–48, qua kiểm tải, mục 2 và ghi sổ trước thay dòng theo ADR-0058:38–39. Đây là tiếp nhận mới có điều kiện. |
| Tệp rỗng khi A kết nối lại | Dòng 46–48 xác định mất khoá; kiểm tải rồi lấy mới. Không dùng hạn hoặc UTC bắt đầu cũ để tự nhận là đang giữ khoá. |
| Chỉ thấy MCP hoặc Python tạo trước UTC bắt đầu khoá khác | Không thoả đủ điều kiện ADR-0059:35–37 nên mục 2 không chặn; kiểm tải/ghi sổ/thứ tự tiếp nhận của ADR-0057/0058 vẫn áp dụng. |
| Chủ khoá đã tuyên bố bỏ, có bằng chứng; còn tiến trình | ADR-0058:36–40 yêu cầu bằng chứng của chính phiên giữ khoá và kiểm tải/ghi sổ; ADR-0059:38 loại trừ mục 2 cho 3(c). Cấm tự dừng tiến trình vẫn giữ tại dòng 85. |
| Heartbeat cũ hơn 30 phút nhưng hạn chưa qua | Có vi phạm nhịp tim của chủ khoá, nhưng ADR-0059:31 không cho dùng tuổi heartbeat làm lý do thu hồi mới; bên khác vẫn đợi khi khoá còn hiệu lực. |

Giới hạn được giữ đúng: đọc rồi ghi vẫn có khe đua (ADR-0059:52, 84; ADR-0058:48–49). Không đưa yêu cầu khoá nguyên tử vào nghiệm thu vì spec §5 đã loại khỏi packet.

## Phạm vi bằng chứng

Các phép đo chạy thật trên Linux, Python 3.13.18. Không truy cập được máy ASUS-LAPTOP; D10 dùng bản chép gốc đã khớp hash, D11/D12 dùng spec đóng băng. Không khai đã đo lại các tiến trình lịch sử, CI hoặc Windows local.

Theo chỉ thị đầu vào, snapshot checkout trước/sau do phiên điều phối chụp ngoài sandbox; reviewer chưa trực tiếp xác minh các snapshot đó. Sandbox thực tế là `workspace-write`; checkout được đối xử read-only. Đã kiểm HEAD/tree, tracked diff, index, untracked và ignored ở cuối; đều sạch. Riêng `git config core.abbrev 7` thực hiện đúng yêu cầu bootstrap trong prompt. Mọi log, dữ liệu đọc lại và script nháp ghi trong sandbox ngoài `cay-kho/`; Python chạy với `PYTHONDONTWRITEBYTECODE=1`.

## Đã chạy

Các lệnh Python kiểm tra packet chạy trong `cay-kho/`. Script `audit_scope.py` và các log nằm ở thư mục sandbox hiện tại. Rc dưới đây là mã thoát thật; `rg` rc=1 được ghi đúng là không có kết quả khớp.

| Lệnh | Rc | Kết quả thật |
|---|---:|---|
| `git -C cay-kho rev-parse HEAD` | 0 | `cb9bd240c269811f14331b827879b271498c6628` |
| `git -C cay-kho rev-parse --is-shallow-repository` | 0 | `false` |
| `sha256sum spec-r3.md chung-cu-d10.txt` | 0 | Hai hash đầy đủ như bảng đối chiếu ở trên. |
| `git -C cay-kho config core.abbrev 7` và `git -C cay-kho config --get core.abbrev` | 0 / 0 | `7` |
| `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py adr-song --root .` | 0 | `adr-song: sạch — 58 ADR trên đĩa, 58 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` |
| `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/tl.py doc-claims-check --json` | 0 | `"ok": true`, `"files_scanned": 118`, `"flags": []`, `"advisory_count": 381`, `"layers_skipped": {}`. Không advisory thuộc ADR-0059; stderr 0 byte. |
| `git -C cay-kho diff --numstat b653574b117fa1496fbf58f09a22a8cbed5cc5dc HEAD` | 0 | `3  2  docs/PROTOCOL_DA_PHIEN.md`; `100  0  docs/adr/0059-windows-local-nhip-tim-khoa.md`. Tổng 2 tệp / 103 thêm / 2 xoá. |
| `git -C cay-kho diff --numstat adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc HEAD^1` | 0 | Cùng hai hàng và số dòng như trên. |
| `git -C cay-kho merge-base --is-ancestor b653574b117fa1496fbf58f09a22a8cbed5cc5dc HEAD` | 0 | Master là tổ tiên của HEAD. |
| `git -C cay-kho diff --name-status HEAD^1 HEAD -- docs/PROTOCOL_DA_PHIEN.md docs/adr/0059-windows-local-nhip-tim-khoa.md` | 0 | Rỗng. Merge không thay nội dung packet. |
| `git -C cay-kho diff --name-only b653574b117fa1496fbf58f09a22a8cbed5cc5dc HEAD -- 'docs/adr/0057-*' 'docs/adr/0058-*'` | 0 | Rỗng. |
| `git -C cay-kho diff --check b653574b117fa1496fbf58f09a22a8cbed5cc5dc HEAD` | 0 | Rỗng. |
| `git -C cay-kho ls-tree origin/ops/windows-local-may-chu-kho-r3-lease ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r3.md` | 0 | `100644 blob 93f1248aeca8c0d229f0f896434115f246e7b621` tại đúng path. |
| `PYTHONDONTWRITEBYTECODE=1 python3 audit_scope.py` — bản hoàn tất | 0 | `ALL_SCOPE_CHECKS_PASSED`; gồm so byte diff/spec, giới hạn write set, merge, chỉ ba chỉnh sửa protocol, D10–D12 và thứ tự script/mẫu PID. |
| `PYTHONDONTWRITEBYTECODE=1 python3 audit_scope.py` — lần dựng probe đầu | 1 | Probe của reviewer tìm sai literal `Ghi checkout_rc` do thừa dấu ngoặc, phát sinh `ValueError: substring not found`; đã sửa literal trong script sandbox và chạy lại đạt. Đây là lỗi setup phép đo, không phải finding của candidate. Giữ log `audit_scope.setup-failure.log`. |
| Quét sáu tệp cổng bằng `rg`, lệnh nguyên văn dưới bảng | 1 | Không có kết quả. |
| `git -C cay-kho status --porcelain=v1 --untracked-files=all` | 0 | Rỗng. |
| `git -C cay-kho ls-files --others --ignored --exclude-standard` | 0 | Rỗng. |
| `git -C cay-kho diff --exit-code` và `git -C cay-kho diff --cached --exit-code` | 0 / 0 | Rỗng; working tree và index sạch. |
| `git -C cay-kho rev-parse HEAD HEAD^{tree}` | 0 | Exact HEAD và tree nêu đầu verdict. |

Lệnh quét cổng nguyên văn, rc của `rg` = 1:

```sh
rg -n 'KHOA\.txt|CreationDate|ngat=co|UTC nhịp tim|ADR-0059' cay-kho/ops/lease_publish.py cay-kho/.claude/dev/packet_loop.py cay-kho/.claude/dev/launcher.py cay-kho/.claude/dev/gate_lifecycle.py cay-kho/.github/workflows/ci.yml cay-kho/.github/workflows/ops-publish-lease.yml
```

Đọc GitHub bằng công cụ connected, không gán mã thoát shell cho công cụ: `github_fetch` URL comment `6537481455`, `github_get_pr_info(repository_full_name="ducthangho/tra-luat", pr_number=1062)` và `github_fetch_issue(repository_full_name="ducthangho/tra-luat", issue_number=1035)` đều trả `isError=false`. Một lần gọi thử `github_get_pr_info` ban đầu dùng sai tên tham số `repo_full_name`, nhận lỗi schema; gọi lại với `repository_full_name` thành công. Các lệnh đọc `nl`, `sed`, `cat`, `rg` và `git show/log` phục vụ đối chiếu chỉ đọc, không sửa candidate.

Bằng chứng đầy đủ: `adr-song.log`, `doctrine-scan.log`, `doc-claims-check.json`, `doc-claims-check.stderr`, `audit_scope.py`, `audit_scope.log`, `audit_scope.setup-failure.log`, `remote-evidence.json`.
