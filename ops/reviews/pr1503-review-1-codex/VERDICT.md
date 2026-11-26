# Verdict PR #1503 lượt 1 — Codex
reviewed_sha: 257beee354cf4861c2d2978d195dfebaf81904d0
base_sha: a99a74f75867172fe62f984d7528f5d5bd73dacb
tree: 72c3c876f19cce43b19dc0043143bb33878b5f7a
provider: openai_codex
execution_surface: codex_cli
transport: machine
run_id: 7d2be5a4

Đã đối chiếu HEAD detached, merge-base với ref cục bộ `origin/master`, diff 21 tệp và SHA-256 prompt `097d34e37274742d79b0a191263e75e5a0473af5635b68ed6052e0415f5b3ccd` với receipt cục bộ. Phạm vi là review offline theo prompt được giao. Snapshot thiếu khai báo Review Class nên áp dụng mức thận trọng `sensitive`. Môi trường Linux x86_64, Python 3.13.18, codex-cli 0.172.0, sandbox workspace-write, `core.abbrev=7`. Source và index có diff rỗng qua kiểm tra đầu/cuối. Phép đo này quan sát trạng thái tại hai mốc. Các script đo nằm ngoài checkout tại `/tmp/tra-luat-pr1503.yGc4gw/probe/`.

## Findings

### F1 [P1] Định nghĩa bị cắt và khoản bị bỏ vẫn qua kiểm nguyên văn — scripts/tl_core/llm_route.py:308

**Kịch bản.** Điều giả có hai khoản, khoản 1 là `Hồ sơ là tài liệu do cơ quan có thẩm quyền lập.` Model chỉ trả `tài liệu` cho khoản 1. Phép kiểm chuỗi con nhận đoạn bị cắt và CLI báo `ok=true` với rc 0. Cùng fixture, mảng rỗng, mảng thiếu khoản 2 và hai khoản bị tráo số đều được báo đạt. Người gọi có thể dùng bản thiếu hoặc sai số khoản như bản đã xác minh.

**Bằng chứng.** `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-verbatim.py` (rc 0). Script chạy CLI thật với `--tep --thu-tu sub --json` và executable Claude giả. Cả đối chứng đủ hai khoản lẫn bốn đầu ra sai đều trả `rc=0 ok=True lech=[]`. Ca `truncated` trả khoản 1 với đúng chuỗi bị cắt `tài liệu`. `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-article-meta.py` cũng xác nhận kết quả đúng bị từ chối nếu nguồn xuống dòng giữa `là` và phần định nghĩa (`split_line rc=5 lech=[1]`).

**Đề xuất sửa.** Ở `lech_nguyen_van` và bước xác nhận của `tach_khai_niem`, đối chiếu mỗi mục với trọn thân khoản trong nguồn và kiểm tập số khoản, thứ tự, tính duy nhất. So từ đoạn nguồn đã xác định ranh giới để giữ nguyên dấu câu và từ ngữ. Khóa bằng năm fixture trên và đột biến đổi so khớp toàn khoản thành tìm chuỗi con. Thêm ca nguồn có khoản xuống dòng và ca hợp lệ thiếu số hiển thị để bản vá định nghĩa rõ đầu vào hỗ trợ, tránh bỏ sót phần tiếp dòng.

### F2 [P1] Claude Code cạn lượt sửa schema vẫn kích hoạt đường API — scripts/tl_core/llm_route.py:192

**Kịch bản.** Với thứ tự mặc định `sub,api`, Claude Code đã chạy model và trả envelope `error_max_structured_output_retries`, `is_error=true`, rc 1. Lõi coi mọi lỗi envelope là lỗi đường và gọi tiếp API. Lỗi đầu ra của lần yêu cầu trước có thể làm người dùng tốn thêm credit API, trái quy tắc dừng khi sai schema.

**Bằng chứng.** `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-sub.py` (rc 0) → `schema_retries result= api fallback= ['api']`. Đối chứng lỗi hạn mức cũng gọi API như mong đợi. Cùng script, envelope có subtype lỗi, rc 0 và thiếu `is_error` được nhận như thành công nếu vẫn có structured output. `modelUsage` dạng mảng gây `AttributeError` và record model rỗng được báo 0 token. Executable Claude Code 2.1.331 có nhánh dựng `subtype:"error_max_structured_output_retries"` kèm mảng `errors`. Mã thoát của một phiên Claude Code thật **KHÔNG ĐO ĐƯỢC** vì lượt này chỉ dùng phản hồi giả.

**Đề xuất sửa.** Phân loại envelope ở `duong_sub` trước khi xét fallback. Các subtype lỗi yêu cầu có nghĩa rõ phải phát `Dung` kể cả khi rc khác 0. Chỉ nhận thành công khi loại envelope và kiểu của các trường cần thiết hợp lệ. Tách thiếu số đo token khỏi số token thực tế bằng 0. Khóa bằng fixture cạn lượt sửa schema với đường API giả bị cấm và đột biến bỏ chốt subtype. Giữ ca hạn mức và mất CLI để việc siết envelope không vô hiệu hóa fallback hợp lệ.

### F3 [P1] Tuyến sub kế thừa cấu hình Claude Code dùng Bedrock — scripts/tl_core/llm_route.py:44

**Kịch bản.** Máy đã bật Bedrock bằng `CLAUDE_CODE_USE_BEDROCK=1`. Khi chọn `sub`, subprocess Claude Code giữ nguyên biến chọn provider đó. Nếu Bedrock đã xác thực và trả đúng model, CLI vẫn ghi `DUONG: sub (subscription — tinh vao han muc goi)`, dù lần gọi đi qua provider do người dùng cấu hình. Cùng rủi ro với các biến chọn Vertex, Foundry hoặc gateway.

**Bằng chứng.** `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-sub.py` (rc 0) → `sub-env flags = ['CLAUDE_CODE_SKIP_BEDROCK_AUTH', 'CLAUDE_CODE_USE_BEDROCK']`, `third_party result= sub fallback= []`. `claude --help` (rc 0) xác nhận CLI hỗ trợ thông tin xác thực riêng cho Bedrock, Vertex và Foundry. `LC_ALL=C rg -ao --no-filename 'CLAUDE_CODE_USE_(BEDROCK|VERTEX|FOUNDRY|GATEWAY)' "$(command -v claude)" | sort | uniq -c` → tìm thấy cả bốn biến. Chuỗi hướng dẫn đi kèm executable xác nhận `Amazon Bedrock: set CLAUDE_CODE_USE_BEDROCK=1 with AWS credentials`. **KHÔNG ĐO ĐƯỢC** tài khoản thực tế bị tính tiền, do không gọi dịch vụ thật.

**Đề xuất sửa.** Đặt chốt kiểm provider ở `env_cho_sub` hoặc ngay đầu `duong_sub`. Từ chối môi trường có cấu hình định tuyến khác khi chưa xác nhận được subscription, hoặc cô lập các nguồn cấu hình đó mà vẫn giữ được login subscription. Kiểm cả cấu hình ngoài env có thể tác động đến danh tính. Khóa bằng đồ giả bắt env child, với đột biến giữ lại từng cờ provider. Giữ đối chứng login subscription để tránh bản vá vô tình loại đường chính của người dùng.

### F4 [P1] `--out` ghi đè bản đã xác minh bằng kết quả bị từ chối — scripts/tl_core/ops_misc.py:3029

**Kịch bản.** Tệp đích chứa kết quả từ lần chạy trước. Lần chạy mới trả định nghĩa diễn giải, bị chốt nguyên văn bắt và kết thúc rc 5. Handler đã ghi đè tệp đích trước khi kiểm `kq["lech"]`. JSON trên đĩa chứa chuỗi sai và thiếu cả `ok` lẫn `lech_nguyen_van`, nên tiến trình đọc riêng tệp có thể nhận nhầm thành kết quả hợp lệ.

**Bằng chứng.** `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-cli.py` (rc 0) → `out_rejected rc=5 stdout_ok=False saved_keys=['dieu', 'khai_niem', 'nguon', 'so_hieu'] saved_definition=bản diễn giải. previous_present=False`. Phép đo đi qua parser và handler thật với model giả.

**Đề xuất sửa.** Trong `cmd_llm_khai_niem`, xuất `--out` chỉ sau khi toàn bộ kết quả qua kiểm và dùng ghi nguyên tử. Giữ thông tin chẩn đoán ở stderr hoặc envelope stdout. Khóa bằng ca rc 5 với tệp đích có sẵn và ca với tệp chưa tồn tại. Đột biến đưa thao tác ghi lên trước phép kiểm phải làm đỏ cả hai. Giữ đối chứng rc 0 có tệp dùng được và nhật ký đo chi phí vẫn có ích khi model trả sai.

### F5 [P1] `--config` bị bỏ khi lệnh tìm nguồn — scripts/tl_core/ops_misc.py:3001

**Kịch bản.** Gọi `tl --config requested.json --profile Demo llm-khai-niem 94/2099/QH99 --dieu 3`. Lệnh thuộc nhóm nạp creds muộn và chỉ chuyển tiếp `--profile` cho `extract`. Nếu config mặc định cũng có profile `Demo` nhưng khác registry hoặc manifest, tiến trình con có thể lấy nguồn khác mà đầu ra vẫn mang số hiệu người dùng đã nhập. Nếu config mặc định thiếu profile, người dùng có thể nhận lỗi dù đã chỉ đúng config.

**Bằng chứng.** `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-cli.py` (rc 0) → `config_child ['extract', '94/2099/QH99', '--dieu', '3', '--profile', 'Demo'] rc=0 term=tài liệu lưu.`. Stub con phân biệt hai nguồn theo việc nhận được `--config`. Trên parser thật, `--config` là cờ gốc ở `scripts/tl_core/cli.py:39`, còn `tl.main` bỏ nạp creds cho lệnh này ở `scripts/tl.py:1337`.

**Đề xuất sửa.** Chuyển tiếp các cờ gốc quyết định nguồn ở chỗ xây argv cho `extract`. Dùng vị trí đã được parser `extract` hỗ trợ cho cả `--config` và `--profile`. Khóa bằng fixture hai config với cùng tên profile nhưng nội dung khác và đột biến bỏ truyền config. Giữ ca `--tep` độc lập với creds và ca lấy nguồn bằng config mặc định.

### F6 [P1] Cảnh báo nguồn chạm trần bị bỏ trước khi gọi model — scripts/tl_core/ops_misc.py:3009

**Kịch bản.** Nguồn export chạm trần khi đang ở thân Điều cần tách, ngay sau khoản 1. `tl extract` in Điều thấy được, rc 0 và cảnh báo CAP trên stderr (`scripts/tl_core/extract_cache.py:317`). Handler bỏ dòng cảnh báo, gửi phần Điều có thể bị cắt cho model, rồi trả `ok=true` khi các mục khớp phần còn lại. Kể cả phép đối chiếu đủ khoản so với chuỗi nguồn nhận được cũng không thể nhận biết khoản đã mất trước đó.

**Bằng chứng.** `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-cli.py` (rc 0) → `capped_extract model_calls=1 rc=0 ok=True cap_forwarded=False` với subprocess giả trả đúng dạng marker Điều và cảnh báo CAP.

**Đề xuất sửa.** Truyền trạng thái đầy đủ của Điều từ lớp `extract` sang handler bằng dữ liệu có cấu trúc. Dừng trước model nếu Điều chạm cuối phần export và chưa xác minh trọn Điều, kèm hướng dùng nguồn no-cap. Ca giả cuối Điều bị cắt phải có 0 lượt model. Đột biến bỏ chốt phải làm ca đó đỏ. Giữ ca Điều đã kết thúc trước điểm cắt để tránh từ chối oan văn bản dài.

### F7 [P2] SDK báo dịch vụ API quá tải nhưng không thử tuyến sub — scripts/tl_core/llm_route.py:87

**Kịch bản.** Người dùng đặt `api,sub`. Dịch vụ API tiếp tục trả HTTP 529 sau khi hết retry của SDK. Đây là lỗi quá tải ở dịch vụ, nhưng lõi phát `Dung` và handler trả rc 4. Nhánh sub không được thử. HTTP 503 và HTTP 408 cũng bị coi là lỗi yêu cầu.

**Bằng chứng.** `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-sdk.py` (rc 0) dùng Anthropic SDK 2.13.0 thật và `httpx2.MockTransport`, với retry tắt để đo lỗi cuối mà lớp gọi nhận. Kết quả `529 overloaded_error Dung ['api'] OverloadedError overloaded_error` và `503 api_error Dung ['api'] ServiceUnavailableError api_error`. Hai đối chứng HTTP 400 thường và HTTP 429 lần lượt cho `Dung ['api']` và `sub ['api', 'sub']`.

**Đề xuất sửa.** Bổ sung các mã lỗi khả dụng của provider có nghĩa rõ ở `phan_loai_loi_api`, bắt đầu bằng 503 và 529. Xác định cùng người giữ hợp đồng khi mạng đã gửi request nhưng không xác định được kết quả, như 504. Khóa bằng transport giả với đúng lớp lỗi SDK, ca 4xx lỗi yêu cầu và đột biến bỏ 529 khỏi tập chuyển đường. Tránh mở rộng mù sang mọi 5xx có thể phản ánh tính năng chưa hỗ trợ.

### F8 [P2] Doctor xác nhận key dùng được với HTTP 200 rỗng — .claude/dev/launcher.py:4813

**Kịch bản.** Một gateway ở endpoint cấu hình trả HTTP 200 rỗng hoặc `{"status":"ok"}`. Probe trả `DUNG_DUOC` và token `?+?` dù chưa thấy phản hồi Messages. Nếu proxy trả JSON dạng mảng, `.get()` gây `AttributeError` trên cả đường 200 và đường xử lý HTTPError.

**Bằng chứng.** `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-launcher.py probe` (rc 0) → `empty_200 DUNG_DUOC … ?+? token`, `wrong_200 DUNG_DUOC … ?+? token`, `non_object_401 AttributeError`, `non_object_200 AttributeError`. Phản hồi Messages giả có usage cho `DUNG_DUOC … 2+4 token`.

**Đề xuất sửa.** Kiểm cấu trúc phản hồi ngay trong `_do_anthropic_api`; chỉ tuyên bố `DUNG_DUOC` khi có dữ liệu Message tối thiểu và usage hợp lệ. Với JSON lạ ở đường lỗi, giữ mã HTTP để xác định trạng thái và chỉ in nhãn lỗi thuộc tập đã biết. Mở rộng t162 với HTTP 200 rỗng, body sai kiểu và Message hợp lệ. Đột biến chấp nhận mọi 2xx phải chết bằng ca thiếu bằng chứng dương. Kiểm tương thích với phản hồi Messages thực của API và proxy hỗ trợ.

### F9 [P2] Thứ tự không hợp lệ có thể rơi xuống cấu hình tính tiền khác — scripts/tl_core/llm_route.py:328

**Kịch bản.** Script truyền `--thu-tu ""` vì biến dùng để dựng cờ bị rỗng. `if cli` bỏ qua cờ đã truyền và dùng `TL_LLM_ORDER=api`. Trường hợp khác, tệp thứ tự là symlink cục bộ đến cấu hình đã bị chuyển đi. `Path.exists()` coi như không có tệp và cũng dùng API. `--reset` báo không có tệp trong khi symlink vẫn còn.

**Bằng chứng.** `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-order.py` (rc 0) → `explicit (('sub',), 'co --thu-tu')`, `explicit_empty (('api',), 'bien TL_LLM_ORDER')`, `dangling_order_link True (('api',), 'bien TL_LLM_ORDER')`, `reset_dangling False link_remains True`. Phản chứng ghi nguyên tử đạt `replace_failed ('sub',) files ['order.json']` khi chặn `os.replace`.

**Đề xuất sửa.** Ở `thu_tu_hieu_luc`, phân biệt cờ vắng với giá trị rỗng và phân biệt không có tệp cấu hình với đường dẫn đã tồn tại nhưng không đọc được. Ở `xoa_thu_tu`, unlink chính phần tử cấu hình và xử lý trường hợp đã bị xóa. Khóa bằng ca cờ rỗng và symlink đứt cùng các đột biến trả lại điều kiện truthiness hoặc `exists()`. Giữ ca thiếu tệp thật để xác nhận thứ tự env và mặc định vẫn hoạt động.

### F10 [P2] Suite core không bắt mất riêng từng tín hiệu lỗi subprocess — scripts/tl_core/llm_route_test.py:167

**Kịch bản.** Ca fallback sub duy nhất dùng đồng thời rc khác 0 và `is_error=true`. Xóa một trong hai chốt đều không làm ca đỏ. Ca env cũng chỉ đòi có mặt `--setting-sources`, nên đổi giá trị rỗng thành `user` vẫn xanh dù đã yêu cầu Claude đọc thêm cấu hình người dùng.

**Bằng chứng.** `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-core-mutants.py` (rc 0) → `drop_rc_check 21/21 []`, `drop_is_error_check 21/21 []`, `restore_user_settings 21/21 []`. Mỗi thay đổi được áp vào một tệp core riêng trong thư mục tạm, rồi chạy toàn bộ 21 ca gốc.

**Đề xuất sửa.** Tách fixture lỗi tiến trình và lỗi envelope để từng tín hiệu độc lập phải dẫn đến trạng thái đúng theo hợp đồng đã sửa ở F2. Ở ca môi trường, so cặp option và giá trị rỗng. Thêm cả ba đột biến vào suite, giữ đối chứng lệnh thành công đúng envelope để tránh siết tay quá mức.

### F11 [P2] Đầu ra từ `--tep` tự gán sai số Điều — scripts/tl_core/ops_misc.py:3027

**Kịch bản.** Tệp local bắt đầu bằng `Điều 15. Giải thích từ ngữ`. `llm-khai-niem --tep article-15.txt --json` trả `ok=true` và `"dieu":"3"` do mặc định parser. Nếu người gọi đưa thêm số hiệu và `--dieu 7`, lệnh vẫn tách toàn tệp của Điều 15 nhưng gắn số hiệu truyền vào và Điều 7.

**Bằng chứng.** `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-article-meta.py` (rc 0) chạy CLI thật với Claude giả → `file_article=15 rc=0 json_dieu=3` và `file_article=15 rc=0 json_dieu=7 json_so_hieu=94/2099/QH99`.

**Đề xuất sửa.** Áp mặc định Điều 3 riêng cho chế độ lấy theo số hiệu. Ở chế độ tệp, trường Điều lấy từ tiêu đề xác minh được hoặc để rỗng; kiểm và báo xung đột nếu cho phép người dùng truyền thêm metadata. Khóa bằng tệp Điều 15, tệp không có tiêu đề và ca số Điều truyền vào mâu thuẫn, kèm đột biến đưa mặc định 3 trở lại nhánh tệp. Giữ đối chứng gọi theo số hiệu mà bỏ `--dieu`.

### F12 [P3] Tệp không phải UTF-8 làm thoát khỏi contract mã lỗi — scripts/tl_core/ops_misc.py:2992

**Kịch bản.** Người dùng chọn tệp văn bản mã legacy. `Path.read_text(encoding="utf-8")` ném `UnicodeDecodeError`, đi qua handler do nhánh này chỉ bắt `OSError`. Script chạy lệnh nhận traceback và rc 1 của Python, trong khi CLI khai rc 2 cho đầu vào lỗi.

**Bằng chứng.** `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-cli.py` (rc 0) → `non_utf8 result=UnicodeDecodeError model_calls=0`. Chạy CLI trực tiếp với cùng byte lỗi và executable Claude giả cho rc 1 và traceback `UnicodeDecodeError`.

**Đề xuất sửa.** Bắt `UnicodeError` ở nhánh đọc tệp, in thông báo yêu cầu UTF-8 và trả rc 2 trước khi gọi model. Khóa bằng một tệp legacy và một tệp UTF-8 có dấu. Đột biến bỏ `UnicodeError` khỏi handler phải làm ca đầu đỏ. Tránh thay ký tự lỗi âm thầm trong văn bản làm nguồn.

## Đã kiểm mà không thấy lỗi

| Phép đo | Trạng thái và bằng chứng |
|---|---|
| `python scripts/tl_core/llm_route_test.py` | `passed`, rc 0, 21/21 ca qua và 16/16 đột biến được giết. Các đột biến độc lập ngoài bảng có kết quả ở F10. |
| `python .claude/dev/launcher_test.py --lap-ca t162 --lan 1` | `passed`, rc 0, 1/1 qua, 0 bỏ qua. Đồ giả xác nhận mặc định không gọi mạng, ưu tiên tên key, các trạng thái hết credit/từ chối và không in giá trị key trong các phản hồi đã thử. |
| `python -B /tmp/tra-luat-pr1503.yGc4gw/probe/check-launcher.py mutants` | `passed`, rc 0. Cả 4 đột biến `anthropic_api_*` đều làm đúng t162 đỏ, `TARGETED_MUTANTS 4/4 killed; failed=0; skipped=0`. Runner chỉ chọn 4 đột biến, dùng bản sao tạm của launcher và kiểm tín hiệu assertion của ca đích. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed`, rc 0, `ok=true`, 194 lệnh, 26 cards, 0 lỗi, 0 cảnh báo. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed`, rc 0, `ok=true`, 20/20 cases qua. Fixture `hygiene_sweep_fixture` báo `projection_stable=true` và `raw_stable=false`; đây là trường output đã quan sát, không tính như bằng chứng ổn định raw. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed`, rc 0, `ok=true`, 15 checks. |
| `python scripts/gen_instructions.py --selftest` | `passed`, rc 0, 44/44. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed`, rc 0, `ok=true`, `expected=checked=187`, 0 tệp thiếu/thừa, `package_hash_match=true`. Manifest base có 186 tệp. |
| `python scripts/tl.py --deterministic release-bundle --out <zip> --json` ×2 và `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --archive <zip> --json` | `passed`, rc 0 cả ba lần. Hai ZIP cùng SHA-256 `224496b77daf8434270a2900f9f082de3878dedc72020057436f58aa363bd579`. Archive có lõi `scripts/tl_core/llm_route.py`, bộ unit test dev-side vắng, 187 tệp khớp. Chạy `release-verify --strict --json` từ ZIP đã giải nén cũng cho rc 0, `ok=true` và 187/187. |
| `TL_LLM_ORDER_FILE=<tệp mới> python scripts/tl.py llm-order --json` | `passed`, rc 0, `ok=true`, `thu_tu=["sub","api"]`, `nguon="mac dinh"`. Tệp hỏng thường bị chặn trong suite. Phép thử lỗi `os.replace` giữ nguyên tệp cũ và dọn tệp tạm. |
| `claude --version` và `claude --help` | `passed`, rc 0, Claude Code 2.1.331. Help có toàn bộ cờ mà `lenh_sub` thêm, gồm `-p --model --output-format --no-session-persistence --tools --strict-mcp-config --setting-sources --disable-slash-commands --system-prompt --json-schema`. Kiểm này đo bề mặt cờ được công bố. |
| `loi_ruff_ci()` từ `.claude/dev/ci_dang_ky_test.py` qua `python -B` và `runpy.run_path` | `passed`, rc 0, `RUFF_CONTRACT 3 []`. Ruff 0.15.15. |
| Hai ca tích hợp r380, parser snapshot và VERSION trong `python scripts/tl.py --selftest` | `passed` ở cấp ca. Log có `[OK]` cho `r380_llm_order_luu_doi_xoa`, `r380_llm_khai_niem_tu_tep_qua_sub`, `r77a_parser_surface_matches_snapshot` và `skill_md_version_matches_VERSION`. Cả ba vị trí VERSION ghi 1.36.71. Tổng suite rc 1 như dưới. |

## Phép kiểm còn đỏ

- `python -m ruff check --no-cache --select F scripts/tl.py` trên head và cùng tệp từ base. `failed` theo mã thoát, rc 1 mỗi vế, 12 chẩn đoán cùng code/message mỗi vế, delta 0 theo tiêu chí repo.
- `python scripts/tl.py --selftest` trên hai checkout tạm. Head `failed`, rc 1, 1774/1788. Base `failed`, rc 1, 1772/1786. So tập ID trong các dòng `[FAIL]` cho đúng 14 ca chung và delta 0. Tám ca `r973_bootstrap_*`, năm ca `wp433_*` và `wp727_tl_gws_refresh` đỏ ở cả hai vế trong môi trường sandbox này. Log tại `/tmp/tra-luat-pr1503.yGc4gw/selftest/stdout` và `/tmp/tra-luat-pr1503.yGc4gw/baseline/stdout`.

## Không đo được

- `not_run` — Billing thật, xác thực subscription/API, ID model thật và hành vi runtime của `claude -p`. Phép đo được giao dùng đồ giả và help CLI.
- `not_run` — Windows, Cowork và check CI từ GitHub. Phép đo cục bộ thực hiện trên Linux. Phiên này không có bằng chứng mô hình/effort đã phục vụ hoặc identity Executor để chứng nhận cặp provider. Prompt được neo bằng SHA-256, workspace và commit. Packet revision, spec hash và generation chính thức không có trong snapshot được giao.
- `not_run` — Corpus thật. Ca lấy Điều dùng fixture của tiến trình con, với CAP và canonical như `tl extract` công bố.
- `skipped` — Không ghi nhận bỏ qua ở core hoặc đột biến t162 đã chọn. Windows, CI, LIVE và khoản billing là các phạm vi không thực hiện, như trên.

VERDICT: REQUEST_CHANGES
