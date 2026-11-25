# Verdict PR #1503 lượt 2 — Codex

reviewed_sha: ec0722ad128e3439899ba210ee567142f5552b34
base_sha: 168d562b824db709ad88aa14f81d0ce3038cbfcb
tree: 22e588557bca2b5a88d1e178b35d6c3ab4c1e8ac
provider: openai_codex
execution_surface: codex_cli
transport: machine
run_id: 88d61cf0b6104b36ba239a9dd2eaf11d

HEAD detached khớp snapshot. `git merge-base HEAD refs/remotes/origin/master` trả đúng base, rc 0. SHA-256 prompt `0a9e4af9000617ba2a05f899ccd54cb62f8bf1c2870e0ac8bc0234475550c2e7` khớp `checkpoint.json` và `run.json`. Bản vá là `c3ba150b0b0843de98f420b92584098f438f3244`. `git diff --name-status c3ba150 HEAD`, rc 0, chỉ có `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py` và `docs/adr/0063-merge-spec-ref-va-human-audit.md`. Diff theo base có 24 tệp và `git diff --check` rc 0. Phạm vi ghi được giao là `.review/VERDICT.md`; phục vụ đo kiểm dùng scratch `/tmp/tra-luat-pr1503-r2.Z0AlvVdW`.

Môi trường Linux x86_64, Python 3.13.18, Git 2.43.0, `core.abbrev=7`, sandbox workspace-write. `codex --version` báo 0.172.0. Prompt và checkpoint cấp review offline trên đúng SHA. Áp dụng `sensitive` do hồ sơ cục bộ thiếu Review Class, revision, spec hash và generation chính thức.

## Đối chiếu lượt 1

Nguồn F1–F12 là verdict trên `257beee354cf4861c2d2978d195dfebaf81904d0`, lưu tại `ops/reviews/pr1503-review-1-codex/VERDICT.md`.

| # | Trạng thái | Bằng chứng |
|---|---|---|
| F1 [P1] | VÁ SINH LỖI MỚI | `probe-core`, rc 0. Trên đúng văn bản hai khoản, các ca cắt, thiếu, rỗng và tráo từ `lech=[]` ở lượt 1 thành `[1]`, `[2]`, `[1, 2]`, `[1, 2]`. Khoản có số xuống dòng sau `là` và Điều 3a có điểm đều đạt. Nhánh nguồn mất số có thể bỏ cả khoản hoặc tạo khoản giả, xem N1. |
| F2 [P1] | VÁ MỘT PHẦN | `probe-core`, rc 0. Cạn lượt sửa schema, hết lượt và hết ngân sách đều trả `Dung`, chỉ gọi sub. Hạn mức vẫn chuyển, lỗi thiếu `is_error` và `is_error=0` không được nhận thành công. `modelUsage` là mảng vẫn ném `AttributeError`, bản ghi rỗng vẫn nhận 0 token. `stop_reason` chưa được xét và subtype sai kiểu phát sinh lỗi mới, xem N2. |
| F3 [P1] | VÁ MỘT PHẦN | Suite core kiểm Bedrock, Gateway, Foundry, cờ lạ và base URL khác host đều bị từ chối trước subprocess giả. CLI 2.1.331 có đúng 11 tên trong họ `CLAUDE_CODE_USE_*`. Nguồn credential của CLI còn rộng hơn phần chốt tiền kiểm, xem N4. |
| F4 [P1] | ĐÃ VÁ THẬT | `probe-cli`, rc 0. Cả hai ca kết quả lệch trả rc 5. Byte đích cũ được giữ và đích chưa tồn tại vẫn vắng. Khi làm `os.replace` thất bại, byte cũ được giữ và tệp tạm được dọn. Đối chứng đúng ghi JSON đầy đủ. Thay đổi quyền tệp khi ghi thành công được ghi riêng ở N5. |
| F5 [P1] | ĐÃ VÁ THẬT | `probe-cli`, rc 0. Parser con thật nhận `('requested.json', 'Demo', [3])` từ `--config requested.json --profile Demo` đặt trước lệnh. Model giả chạy đúng một lần. |
| F6 [P1] | VÁ SINH LỖI MỚI | `probe-cli`, rc 0. Dấu cảnh báo CAP làm handler trả rc 2 với 0 lần gọi model và hướng dẫn cache no-cap. Chốt hiện chặn theo toàn văn nên cả Điều đã kết thúc trước điểm cắt cũng phải đi đường no-cap, xem N6. |
| F7 [P2] | VÁ MỘT PHẦN | `probe-core`, API SDK 2.13.0 + `httpx2.MockTransport`, rc 0. HTTP 503 và 529 thử sub. 400 thường dừng, 429 chuyển; 408 thông thường giữ `Dung`. 504 `api_error` giữ `Dung` theo chính sách an toàn được ghi trong patch, nhưng 504 có type `overloaded_error` vẫn thử sub, xem N7. |
| F8 [P2] | VÁ MỘT PHẦN | t162 rc 0, 1/1. HTTP 200 rỗng, object không có Message, mảng và usage sai kiểu trả `KHONG_DO_DUOC`. HTTP 401 body mảng giữ `CHUA_XAC_THUC`; đối chứng Message + usage trả `DUNG_DUOC`. Biên kiểm Message còn hở, xem N8. |
| F9 [P2] | ĐÃ VÁ THẬT | `probe-cli`, rc 0. Cờ rỗng bị từ chối kể cả khi env ưu tiên API, symlink đứt trả rc 2 khi đọc, reset xóa được link và sau đó mới dùng env. `llm-order '' --reset` trả rc 2. |
| F10 [P2] | ĐÃ VÁ THẬT | Suite core rc 0, `31/31` và `34/34`. Các đột biến bỏ riêng rc, `is_error` và đọc lại user settings bị chính ca đích bắt. Chi tiết assertion ở phần đột biến. |
| F11 [P2] | VÁ MỘT PHẦN | `probe-cli`, rc 0. Tệp UTF-8 thường nhận số Điều 15 hoặc 3a từ tiêu đề. `--dieu 7` mâu thuẫn và ghép số hiệu với `--tep` đều rc 2, 0 lần gọi model. Với BOM, tiêu đề Điều 15 biến mất khỏi phép kiểm và Điều 7 được báo đạt, xem N3. |
| F12 [P3] | ĐÃ VÁ THẬT | `probe-cli`, rc 0. Byte legacy trả rc 2, 0 lần gọi model, stderr hướng dẫn lưu UTF-8. Đối chứng UTF-8 có dấu chạy thành công. |

Các tên `probe-*` ở đây là các tệp `.py` tại scratch. `run-check <tên> checkout python -B <đường dẫn probe> [đối số]` tạo `.stdout`, `.stderr` và `.rc` cho từng phép đo trong `logs/`. `probe-core.py` nhận thêm `legacy/llm_route.py`, xuất từ Git OID của lượt 1.

## Findings mới

### N1 [P1] Tách khoản đoán theo từng dòng có thể bỏ nội dung nguồn mà vẫn báo đạt — scripts/tl_core/llm_route.py:382–421

**Kịch bản và bằng chứng.** `probe-core.py`, rc 0. Với Điều 3a không có số, khoản đầu xuống dòng ngay sau `là` và khoản kế tiếp nằm trên một dòng. Chỉ trả khoản kế tiếp, dán `stt=1`, được `khoan=1 lech=[]`. Cùng kết quả sai khi số khoản đầu dính sát thân (`1.Hồ sơ…`) và số khoản sau có khoảng trắng. Ở chiều ngược lại, khoản không số giới thiệu danh sách điểm bằng dấu `:` bị loại (`[0]`), còn câu tiếp dòng có ` là ` bị hiểu thành khoản mới (`[1, 2]`). Nhánh có số xử lý được xuống dòng và điểm `a)`/`b)`, nhưng bỏ giá trị của số khoản gốc. Ca nguồn đánh `1.` rồi `4.` vẫn báo đạt khi đầu ra đổi `4` thành `2`. Dạng `(1)` và khoản dùng `bao gồm` thay cho `là` bị từ chối. Phép kiểm ghép hai trường còn chấp nhận tách tại chữ `là` thứ hai nếu ghép lại vẫn trùng (`lech=[]`). Các fixture là văn bản giả để đo định dạng. `probe-entrypoint.py`, rc 0, tái hiện ca mất khoản qua `scripts/tl.py` và executable Claude giả, với `rc=0`, `ok=true`, Điều 3a và chỉ một kết quả.

**Đề xuất.** Đặt kiểm ranh giới thân, số khoản và từng trường tại `tach_khoan`/`lech_nguyen_van`, trước khi một kết quả được gắn `ok=true`. Tái dùng đơn vị có mốc từ trình tách nguồn nếu có. Với văn bản mất số, yêu cầu cấu trúc xác định được hoặc báo rõ nguồn mơ hồ. Chỉ bỏ tiêu đề/câu dẫn đã nhận diện. So thuật ngữ và định nghĩa theo vị trí chữ `là` đầu tiên đã xác định. Khóa bằng cả hai chiều của fixture trên. Mutant bỏ qua đoạn trước khoản đầu, đánh số theo vị trí hoặc so chuỗi ghép phải đỏ. Quy tắc nghiêm hơn cần giữ các ca nguồn mất số thật sự rõ ranh giới, xuống dòng, có điểm và Điều mang hậu tố.

### N2 [P1] Bộ phân loại sub bỏ qua lý do kết thúc và chưa kiểm kiểu envelope — scripts/tl_core/llm_route.py:243–271

**Kịch bản và bằng chứng.** `probe-core.py`, rc 0. Envelope lỗi có `stop_reason=refusal` hoặc `max_tokens` vẫn gọi API giả sau sub. Fixture success kèm lý do từ chối và structured output còn được nhận ở sub. Đây là phép đo contract khi CLI trả trường lý do, chưa quan sát một phiên Claude thật. Binary 2.1.331 khai `stop_reason` là trường tùy chọn trong schema kết quả lỗi; `error_during_execution` được dùng cả cho lỗi trước khi model chạy. Vì vậy riêng subtype này không giải nghĩa được chi phí hay khả năng thử lại. Với `subtype=[]`, lượt 1 nhận nhầm envelope, còn lượt 2 ném `TypeError` ở phép tra `frozenset`. `modelUsage` dạng mảng hoặc bản ghi null vẫn ném `AttributeError`; bản ghi rỗng vẫn báo tổng 0 token. Đối chứng hết hạn mức chuyển đường, cạn lượt schema dừng như yêu cầu.

**Đề xuất.** Giải mã envelope một lần trong `duong_sub`, xác thực kiểu trước khi tra cứu và ưu tiên các lý do kết thúc đã biết như nhánh API. Dùng tín hiệu hạn mức, xác thực và lỗi khởi động rõ ràng để cho phép fallback. Với kết quả không phân loại được, trả trạng thái có chủ ý và giữ dấu thiếu số đo. Ca đích phải đếm 0 lượt API khi lý do là từ chối hoặc cắt đầu ra, đồng thời giữ ca hạn mức có fallback. Mutant bỏ `stop_reason` và bỏ kiểm kiểu phải đỏ độc lập. Tránh biến lỗi mất kết nối thành lỗi yêu cầu chỉ vì hai loại chia sẻ subtype.

### N3 [P1] BOM UTF-8 làm `--tep` nhận sai số Điều — scripts/tl_core/ops_misc.py:2999–3011

**Kịch bản và bằng chứng.** `probe-cli.py`, rc 0. Cùng byte nội dung Điều 15 với khoản `1.`, tệp UTF-8 thường và `--dieu 7` trả rc 2, 0 lượt model. Khi lưu UTF-8 có BOM, handler trả rc 0, `ok=true`, `dieu="7"` và gọi một lượt model giả. Bỏ `--dieu` thì `dieu=null` dù tiêu đề có mặt. Việc đọc bằng `utf-8` giữ U+FEFF, nên regex đầu dòng bỏ lỡ tiêu đề. Đây là trường hợp lưu tệp hợp lệ trên nền hỗ trợ BOM, cùng lỗi gán nhãn của F11.

**Đề xuất.** Xử lý BOM khi đọc tệp local hoặc khi nhận diện tiêu đề, trước cả xác minh số Điều và tách khoản. Giữ hành vi báo rc 2 trên byte không giải mã được. Khóa bằng một fixture UTF-8 có BOM, cùng Điều ở bản không BOM, một ca không truyền `--dieu` và một ca nhập số xung đột. Mutant quay về đọc BOM như ký tự văn bản phải đỏ. Chỉ gỡ BOM ở đầu tệp để giữ nguyên ký tự trong thân khoản.

### N4 [P1] Tuyến sub gắn nhãn subscription khi danh tính tính tiền chưa được xác nhận — scripts/tl_core/llm_route.py:195–238

**Kịch bản và bằng chứng.** `claude --version`, rc 0, cho `2.1.331`. Quét chỉ tên `CLAUDE_CODE_USE_*` trong binary và chạy `probe-routing.py`, rc 0, thấy 11 tên. Guard từ chối đúng bảy tên chọn provider/gateway và cho qua đúng bốn tên trong allowlist (`CCR_V2`, `COWORK_PLUGINS`, `NATIVE_FILE_SEARCH`, `POWERSHELL_TOOL`). Help cũng có cờ `--setting-sources`. Trong mã phân phối, nguồn policy luôn được cộng vào lựa chọn settings. Bộ giải credential nhận API key đã lưu từ `/login`, API key qua cơ chế file descriptor và `apiKeyHelper` từ cấu hình hiệu lực. Các nhánh này nằm ngoài ba biến mà `env_cho_sub` gỡ. Một máy đăng nhập bằng chế độ API hoặc nhận policy tổ chức tương ứng vẫn có thể thỏa tiền kiểm. CLI còn biết trạng thái extra usage của chính tài khoản. `duong_sub` chỉ chứng minh model đã phản hồi, rồi handler khẳng định kết quả dùng hạn mức gói. Đây là bằng chứng tĩnh về các nguồn và hành vi tiền kiểm bằng đồ giả. Việc một tài khoản cụ thể bị tính tiền chưa được đo.

**Đề xuất.** Kiểm nguồn auth và provider hiệu lực ngay trước subprocess trong `duong_sub`, bằng tín hiệu máy đọc được có cùng môi trường/config với lời gọi. Khi đường tính tiền chưa có bằng chứng, dừng hoặc báo trạng thái chưa xác minh theo hợp đồng đã chốt. Đối chứng bằng fixture auth status subscription, API lưu sẵn, policy và thông tin thiếu. Mutant bỏ đòi hỏi bằng chứng danh tính phải đỏ trước bất kỳ lượt model giả nào. Môi trường CLI được broker cấp danh tính có thể cần tín hiệu riêng để giữ tương thích. Nếu sản phẩm yêu cầu phân biệt hạn mức gói với extra usage, cần ghi rõ giới hạn của tín hiệu đó.

### N5 [P2] Ghi `--out` thay quyền truy cập và lỗi I/O thoát khỏi mã lỗi CLI — scripts/tl_core/ops_misc.py:2955–2971, 3050–3063

**Kịch bản và bằng chứng.** `probe-cli.py`, rc 0. Ghi thành công trên tệp mode `0644` đổi mode thành `0600`. Tiến trình khác có thể mất quyền đọc kết quả đã cập nhật. Đích `--out` là thư mục gọi model giả trước, rồi `IsADirectoryError` thoát khỏi `tl.main`. Cùng hiện tượng ngoại lệ ở `llm-order sub` hoặc `--reset` khi tệp cấu hình là thư mục. `probe-entrypoint.py`, rc 0, xác nhận tiến trình CLI trả rc 1 và traceback `IsADirectoryError` cho cả đích `--out` và `llm-order sub`. Khi mô phỏng `os.replace` lỗi, phần bảo toàn byte cũ và dọn tệp tạm hoạt động đúng. `probe-cli-mutations.py` cho thấy ca r380 mới vẫn qua nếu thay ghi nguyên tử bằng ghi trực tiếp.

**Đề xuất.** Ở hai handler, báo lỗi I/O đã biết qua mã lỗi CLI và kiểm trước các đích sai rõ ràng. Giữ thay thế nguyên tử và giữ quyền của tệp thường hiện hữu theo quy ước writer của repo. Khóa bằng ca tệp cũ `0644`, đích thư mục và lỗi replace, xác nhận cả stdout/rc, byte cũ và tệp tạm. Mutant ghi trực tiếp phải đỏ bằng ca lỗi ghi giữa chừng. Kiểm lại tệp mới giữ quyền mặc định an toàn và xử lý lỗi một cách nhất quán khi đích thay đổi trong lúc chạy.

### N6 [P2] Cảnh báo CAP của toàn văn chặn cả Điều đã có ranh giới kết thúc — scripts/tl_core/llm_route.py:497–513

**Kịch bản và bằng chứng.** `probe-cli.py`, rc 0. `extract_dieu` thật cắt Điều 3 đầy đủ gồm 62 ký tự từ tài liệu fixture 199.086 ký tự, có tiêu đề Điều 4 ngay sau khối đã chọn. Tiến trình con giả trả khối đầy đủ và đúng cảnh báo CAP của nguồn. Handler vẫn rc 2, 0 lượt model. Cảnh báo CAP của `cmd_extract` phát theo `len(text)` toàn văn, nên chốt text hiện tại không có thông tin để phân biệt ca này với Điều cuối bị cắt.

**Đề xuất.** Truyền trạng thái ranh giới của Điều cùng cờ CAP từ `cmd_extract`, vì tầng đó thấy cả phần văn bản kế tiếp. Chặn khi chưa xác nhận được cuối Điều. Giữ đường no-cap cho mẫu cuối nguồn. Khóa hai fixture cùng CAP với ranh giới đã thấy và ranh giới chưa thấy. Mutant bỏ xét ranh giới hoặc cho qua mọi cảnh báo CAP phải đỏ. Tránh dựa vào một dòng giống tiêu đề nếu trình phân tích nguồn không xác nhận đó là Điều tiếp theo.

### N7 [P2] Mã 504 có thể kích hoạt fallback trái chính sách của bản vá — scripts/tl_core/llm_route.py:112–134

**Kịch bản và bằng chứng.** `probe-core.py`, rc 0, ép SDK 2.13.0 trả cùng lớp `GatewayTimeoutError` qua transport giả, đã tắt retry để cô lập bộ phân loại. HTTP 504 với `api_error` trả `Dung` và chỉ dùng `api`. Cùng status với `overloaded_error` gọi tiếp `sub`. Nhánh `or kieu in ...` cho loại lỗi trong body thắng mã lỗi HTTP mà comment của bản vá quy định phải dừng vì yêu cầu có thể đã được xử lý.

**Đề xuất.** Chốt thứ tự ưu tiên status/type trong `phan_loai_loi_api` và mã hóa quyết định 504 biểu kiến. Khóa trực tiếp 504 với hai body qua transport giả. Mutant khôi phục quyền ưu tiên body trước 504 phải đỏ. Giữ đối chứng 503, 529, 429 và đường có type rõ khi thiếu mã HTTP. Chính sách retry bên trong SDK cần được xét cùng mục tiêu chi phí vì nó chạy trước bộ phân loại này.

### N8 [P2] Doctor chấp nhận Message thiếu bằng chứng hoặc sai model và t162 chưa khóa riêng trường `type` — .claude/dev/launcher.py:4814–4827

**Kịch bản và bằng chứng.** `probe-mutations.py`, rc 0. HTTP 200 giả cho `DUNG_DUOC` khi chỉ có hai số token âm hoặc khi `model` trong Message là `other-model`. Mô tả vẫn in tên model đã yêu cầu. Ca đối chứng có usage hợp lệ nhưng thiếu `type` trả `KHONG_DO_DUOC` trên head. Khi bỏ riêng phép kiểm `type == "message"` trên bản sao tạm, t162 vẫn qua. Ca t162 giết được mutant bỏ toàn bộ kiểm 2xx nhưng chưa kiểm độc lập phần Message.

**Đề xuất.** Tại `_do_anthropic_api`, xác nhận trường model và các trường Message cần thiết, token nguyên không âm, rồi báo model trả về thay cho tên giả định. Bổ sung t162 với mẫu cùng usage mà thiếu `type`, token âm, model khác và đối chứng model hợp lệ. Mutant bỏ riêng kiểm loại, model hoặc dấu token phải đỏ. Chốt cách xử lý alias model đã được provider hỗ trợ để tránh biến kết quả dùng được thành báo đỏ oan.

## Bảng lớp nguyên nhân

| Slug lớp | Biểu hiện | Mức còn mở | Cách đóng |
|---|---|---|---|
| `ranh-gioi-khoan` | F1, N1 | P1 | Đối chiếu cấu trúc nguồn, kiểm số và từng trường, fixture hai chiều trong `probe-core`. |
| `phan-loai-sub` | F2, N2 | P1 | Kiểm kiểu, lý do kết thúc, số đo token, và đếm lượt fallback bằng đồ giả. |
| `dinh-tuyen-sub` | F3, N4 | P1 | Chứng minh provider/auth hiệu lực, kiểm nguồn policy và trạng thái chưa xác minh. |
| `ghi-tep-local` | F4, N5 | P2 | Giữ guard đầu ra, kiểm quyền tệp, lỗi I/O và tính nguyên tử. |
| `chon-config-profile` | F5 | Đã đóng | Hợp đồng parser con và kiểm argv. |
| `day-du-dieu` | F6, N6 | P2 | Ca có ranh giới Điều tiếp theo và ca cuối nguồn khi chạm CAP. |
| `phan-loai-http-api` | F7, N7 | P2 | Ma trận status/type và mutant 504. |
| `bang-chung-doctor` | F8, N8 | P2 | Message/model/usage hợp lệ và đột biến từng trường. |
| `thu-tu-duong` | F9 | Đã đóng | Cờ rỗng, symlink đứt và reset trên Linux. |
| `tin-hieu-subprocess` | F10 | Đã đóng | Mutant riêng rc, `is_error` và setting sources. |
| `so-dieu-tu-tep` | F11, N3 | P1 | Kiểm chéo tiêu đề/cờ trên UTF-8 với và không có BOM. |
| `giai-ma-utf8` | F12 | Đã đóng | Fixture byte legacy và UTF-8 có dấu. |

Tổng 12 lớp đã rà, 8 lớp còn mở, gồm 4 lớp P1 và 4 lớp P2. Mỗi N nối với lớp của lượt 1 tương ứng. Lỗi I/O của `llm-order` cùng cơ chế xử lý ngoại lệ ghi local trong N5.

## Đã kiểm mà không thấy lỗi

| Lệnh | Trạng thái và bằng chứng dương |
|---|---|
| `python scripts/tl_core/llm_route_test.py` | `passed`, rc 0. `31/31 ca QUA`, `34/34 dot bien GIET`. |
| `python .claude/dev/launcher_test.py --lap-ca t162 --lan 1` | `passed`, rc 0. `1/1 qua`, `0 bo qua`, `0 hong`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed`, rc 0, `ok=true`, 194 lệnh, 26 cards, 0 lỗi và 0 cảnh báo. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed`, rc 0, `ok=true`, tất cả 20 ca đạt. `hygiene_sweep_fixture` báo `projection_stable=true`, `raw_stable=false`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed`, rc 0, `ok=true`, 187/187 tệp, 0 lỗi, `package_hash_match=true`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed`, rc 0, `ok=true`, 15 checks. |
| `python scripts/gen_instructions.py --selftest` | `passed`, rc 0, `44/44`. |
| `loi_ruff_ci()` từ `.claude/dev/ci_dang_ky_test.py` qua `runpy.run_path` | `passed`, rc 0, `RUFF_CONTRACT 3 []`. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | `failed`, rc 1 ở cả HEAD và base. Ruff 0.15.15 trả cùng 12 chẩn đoán theo mã và thông điệp. Delta 0 theo tiêu chí repo. |

**Đột biến trên bản sao tạm.** `probe-mutations.py`, rc 0, xác nhận lại 15/15 mutant core ở đúng ca đích, gồm 13 mutant từ bảng sẵn có và hai mutant độc lập bỏ `is_error` hoặc 503. Ca cắt thấy `lech=[]` sau khi đổi so toàn khoản thành chuỗi con. Ca bỏ khoản thấy mất `[2]`. Ca schema báo API bị gọi sai. Ca bỏ riêng rc, `is_error` hoặc subtype báo đã nhận envelope lỗi ở sub. Ca settings đòi lại giá trị rỗng. Các ca 503/529, CAP, cờ rỗng và symlink báo đúng điều kiện bị mất. Cả 5 mutant launcher có trong bảng `anthropic_api_*` bị t162 giết do assertion đích. Các lý do lần lượt là phát sinh gọi mạng mặc định, nhầm HTTP 400 hết credit, nhầm thứ tự tên biến, nhận HTTP 200 rỗng và nhầm mất mạng thành lỗi xác thực. Mutant bỏ riêng trường `type` sống như N8.

**Đột biến CLI.** `probe-cli-mutations.py`, rc 0, chạy nguyên thân ca selftest `r380_llm_khai_niem_bien_dau_vao` trên handler từ các bản sao tạm. Đối chứng trả `True`. Năm mutant ghi dù lệch, bỏ config, bỏ profile, bỏ kiểm số Điều và coi thứ tự rỗng như vắng làm ca trả `False`. Mutant bỏ nhánh Unicode gây đúng `UnicodeDecodeError` của fixture legacy. Mutant thay ghi nguyên tử bằng ghi trực tiếp vẫn trả `True`, phù hợp phạm vi ca hiện có chỉ canh bản bị từ chối.

**Retry SDK.** `probe-api-retry.py`, rc 0, giữ số retry mặc định và dùng transport giả. SDK thực hiện ba request cho mỗi 503, 529, 504 và 408 trước khi lõi nhận lỗi cuối. 503/529 ra `ChuyenDuong`, 504/408 thường ra `Dung`. Đây là hành vi nội bộ SDK trên fixture, không đo billing.

## Full selftest đối chiếu base

Cả hai vế dùng `python scripts/tl.py --selftest` từ clone detached riêng, HEAD tree `22e588557bca2b5a88d1e178b35d6c3ab4c1e8ac`, base tree `e55e6855a845e23b6e8a7a45cf3ed5a260926330`. Cùng Python 3.13.18, cấu hình `core.abbrev=7`, môi trường tách HOME/TMP, proxy trỏ loopback, khóa Git transport và dùng lệnh Claude giả bảo vệ trên PATH. Selftest còn bật chốt `TL_SELFTEST_NO_NET`. Model trong các probe dùng đối tượng giả hoặc transport giả. Log đầy đủ và rc lưu trong scratch `logs/selftest-head.*` và `logs/selftest-base.*`.

| Checkout | Kết quả |
|---|---|
| HEAD `ec0722ad128e3439899ba210ee567142f5552b34` | `failed`, rc 1, `1775/1789`; cả ba ca r380, parser snapshot và VERSION có `[OK]`. SHA-256 stdout `fd0ebd9e88a8b22294b784812bc006940eb928362548f1eb29979e7bb86437e0`. |
| Base `168d562b824db709ad88aa14f81d0ce3038cbfcb` | `failed`, rc 1, `1772/1786`. SHA-256 stdout `1876f2eb29975b47932412443188fa6a6c4112a95c3c8aeec32d8866c78db8cf`. |

So tập ID các dòng `[FAIL]` cho đúng 14 ca chung, gồm 8 ca `r973_bootstrap_*`, 5 ca `wp433_*` và `wp727_tl_gws_refresh`. Delta gồm 0 ca mới đỏ và 0 ca hết đỏ. Hai suite giữ trạng thái `failed` trong môi trường này. `git status` ở clone đo ghi nhận các hiện vật ignored `references/golden/fixtures/` và `scripts/.tl_state/` do phép đo để lại trong scratch.

## Không đo được

- `not_run` — Billing hoặc tài khoản chính sách thật, runtime `claude -p` thật, Anthropic API thật, và corpus LIVE. Các ca định tuyến đo từ binary/help và subprocess giả. Ca HTTP dùng transport giả.
- `not_run` — Windows, Cowork và GitHub CI/provenance. Kết quả ở đây là review offline bằng công cụ cục bộ trên Linux.
- `not_measured` — Model/effort thực sự phục vụ reviewer, identity runtime của Executor và receipt terminal của chính lượt review đang ghi. `checkpoint.json` và `run.json` xác nhận provider/surface/transport đã giao, SHA và băm prompt. Review này có phạm vi verdict cục bộ theo prompt.
- `skipped` — Không có ca bỏ qua trong suite core, t162 và các mutant đích đã chọn.

Đọc lại checkout được giao ở cuối lượt cho cùng exact HEAD và tree, diff tracked và diff index có SHA-256 rỗng `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Snapshot ban đầu thấy `.codex/` ignored rỗng. Snapshot cuối thấy cùng thư mục và `.review/VERDICT.md` untracked. Đây là quan sát ở hai mốc.

N1–N4 còn mở ở mức P1. Các phép thử trên cấu trúc nguồn và số Điều đã tái hiện kết quả sai nhưng `ok=true`. Phép thử envelope tái hiện fallback trái hợp đồng và bằng chứng danh tính tính tiền của `sub` còn thiếu.

VERDICT: REQUEST_CHANGES
