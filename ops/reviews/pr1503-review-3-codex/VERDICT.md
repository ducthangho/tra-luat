# Verdict PR #1503 lượt 3 — Codex

reviewed_sha: 254d4e2d3c789c32a29d6769170e2c0615a32502
base_sha: 2cbb552876c2f0dd6e957db7c2408112c7527127
tree: 17b70f78c88109c10931bc6641d2339b96761f06
nang_tran: chủ kho đồng ý trong phiên điều phối (lượt thứ 3 > trần 2), theo chỉ thị ngày 24-11-2026
provider: openai_codex
execution_surface: codex_cli
transport: machine
run_id: 1d9a975a954c41a9b1b86e78a997b33e

HEAD detached khớp snapshot. Merge-base với ref master cục bộ khớp base được giao. Băm SHA-256 của prompt khớp checkpoint và run, `f4dc2a3a4ec5d2ca55a8508e935857883265ee2ac730c510408506bab4542382`. Phạm vi ghi trong checkout là `.review/VERDICT.md`. Worktree và index sạch với tệp tracked ở mốc đầu. Review offline theo chỉ thị điều phối, áp lớp `sensitive` khi thiếu khai báo Review Class chính thức. Scratch ngoài checkout để tái lập số đo là `/tmp/pr1503-r3.tRwgmC`.

## Đối chiếu lượt 2 (và các mục lượt 1 còn mở)

Nguồn lượt 2 là `ops/reviews/pr1503-review-2-codex/VERDICT.md`, SHA `ec0722ad128e3439899ba210ee567142f5552b34`. Nguồn lượt 1 là `ops/reviews/pr1503-review-1-codex/VERDICT.md`, SHA `257beee354cf4861c2d2978d195dfebaf81904d0`. Các phép đo `probe-*.py` và log ở scratch ghi trên. Mọi lượt model dưới đây đều dùng đồ giả.

| # | Trạng thái | Bằng chứng |
|---|---|---|
| N1 [P1], F1 [P1] | VÁ SINH LỖI MỚI | `probe-cli` và `probe-sources`, rc 0. Có số và xuống dòng đạt. Nguồn số 1, 4 giữ được số 4, đổi sang 2 thì rc 5. Ca cũ nuốt đoạn mở đầu trả rc 5, lệch [0]. Kiểm tách chữ “là” đầu tiên chặn cách tách sai cũ nhưng chấp nhận cách tách sai trong ngoặc gọi tắt, xem M1. Hỗn hợp có số và mất số vẫn có thể mất khoản. |
| N2 [P1], F2 [P1] | VÁ MỘT PHẦN | `probe-core`, rc 0. Từ chối và cắt đầu ra dừng cả khi envelope khai success, với 0 lượt API. `subtype=[]` và usage dạng mảng/null/rỗng ở kết quả thành công không còn gây ngoại lệ hoặc được nhận. Envelope lỗi có input/output dương dừng. Hạn mức với usage 0 chuyển. Ca đã có token ở trường khác hoặc hỏng một chỉ số còn chuyển, xem M2. |
| N3 [P1], F11 [P2] | ĐÃ VÁ THẬT | `probe-cli`, rc 0. UTF-8 BOM có tiêu đề Điều 15 trả rc 0, `dieu="15"`; ghép `--dieu 7` trả rc 2 và 0 lượt model. |
| N4 [P1], F3 [P1] | VÁ SINH LỖI MỚI | `probe-core`, rc 0. Preflight nhận `claude.ai` và `oauth_token` khi `loggedIn=true`, `firstParty`; từ chối API key/helper, bên thứ ba, đăng xuất, rc khác 0 và timeout trước `-p`. `probe-auth-live`: CLI 2.1.331 hỗ trợ đúng cú pháp và phiên này khai `oauth_token/firstParty`. Cùng env đó có thể trả provider khác theo setting sources vì preflight và lượt model dùng hai cấu hình, xem M3. |
| N5 [P2] | ĐÃ VÁ THẬT | `probe-cli`, rc 0. Đích thường giữ mode 0640, thư mục bị từ chối trước model, lỗi replace trả rc 2, giữ byte và dọn tệp tạm. Hai ca đặt/xóa thứ tự với đích thư mục trả rc 2 và báo `IsADirectoryError` có kiểm soát. Quan sát mới về đích nhật ký là M5. |
| N6 [P2], F6 [P1] | VÁ SINH LỖI MỚI | `probe-core`, rc 0. Điều 3 và Điều 4 có trong cùng nguồn CAP thì đạt, Điều cuối thiếu ranh giới bị từ chối. Điều 3 trọn với Điều 3a ngay sau vẫn bị từ chối. Hai lần đọc hai phiên bản có thể cấp nhầm bằng chứng cho bản bị cắt, xem M4. `--config`/ `--profile` được giữ trên cả hai lần đọc. |
| N7 [P2], F7 [P2] | ĐÃ VÁ THẬT | `probe-core` và `probe-api`. Mã 504/500/408 thắng body ngay cả khi type gợi ý chuyển. 503/529/429 giữ chuyển, thiếu status dùng type. SDK 2.13.0 qua mock transport cho 504 `GatewayTimeoutError → Dung`. Retry mặc định trong SDK vẫn đọc ba lần trước khi bộ phân loại chạy, đã thấy từ lượt 2. |
| N8 [P2], F8 [P2] | VÁ MỘT PHẦN | `probe-api`, t162 và đột biến đích. Thiếu type, model khác và số âm trả `KHONG_DO_DUOC`; Message đối chứng có usage dương trả `DUNG_DUOC`. Đường 200 vẫn nhận object có đúng ba trường đang kiểm, 0+0 token và thiếu payload Message, xem M6. |

## Findings mới

### M1 [P1] Có thể xác nhận nguyên văn với thiếu khoản hoặc ranh giới thuật ngữ sai — scripts/tl_core/llm_route.py:442–506

**Kịch bản và bằng chứng.** `probe-sources`, rc 0, dùng text từ bản công bố. Điều 3 Luật 134/2025/QH15 có 8 khoản. Dạng có số (giữ xuống dòng) và dạng bỏ số với mỗi khoản một dòng đều cho `lech=[]`. Bỏ số và giữ xuống dòng giữa khoản 4 trả `[0]` với cả 8 kết quả đúng. Chỉ mất số khoản 4 thì bản gộp 4 vào 3 được `lech=[]` với 7 mục. Trong `probe-cli`, ca gộp tương đương qua `tl.main` trả rc 0, `ok=true` và ghi `--out`. Ranh giới cũng có thể sai ngay trên văn bản có số. Khoản 2 Điều 3 Nghị định 69/2014/NĐ-CP có chữ “là” trong ngoặc gọi tắt rồi mới đến chữ nối định nghĩa. Tách đúng ở ngoài ngoặc cho `[2]`; tách ở trong ngoặc cho `[]`. Khoản 5 của cùng Điều có các điểm a), b) nhưng dùng “bao gồm”, tương tự khoản 1 Điều 3 Nghị định 24/2021/NĐ-CP. Hai mục thực được bộ tách nhận diện đúng số nhưng kết quả giữ từ nối nguồn không thể qua phép ghép cố định bằng “là”. Đối chứng hai điểm a), b) với từ nối “là” đạt trên cả dạng có và không có số. [Luật 134/2025/QH15, Điều 3](https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/12/134-luat-qh.pdf), [Nghị định 69/2014/NĐ-CP, Điều 3](https://vbpl.vn/FileData/TW/Lists/vbpq/Attachments/36825/VanBanGoc_69.2014.N%C4%90-CP.pdf), [Nghị định 24/2021/NĐ-CP, Điều 3](https://vbpl.vn/FileData/TW/Lists/vbpq/Attachments/150076/VanBanGoc_24-2021-N%C4%90-CP.pdf).

**Đề xuất.** Lấy ranh giới và số khoản từ cấu trúc đoạn/điểm đã có ở tầng đọc nguồn. Nếu chỉ có text và không phân giải được ranh giới, báo rõ trước khi gọi model. Xác định vị trí từ nối ở cấp chính và so từng trường theo span gốc. Khóa ca khoản mất một số, xuống dòng và ngoặc gọi tắt bằng cả đầu ra đúng và đầu ra gộp/tách sai. Khi mở rộng từ nối, kiểm cả nội dung liệt kê và ngoặc để tránh nhận “bao gồm” nằm bên trong định nghĩa làm ranh giới mới.

### M2 [P1] Fallback nhìn thiếu bằng chứng token đã chạy — scripts/tl_core/llm_route.py:241–254, 308–328

**Kịch bản và bằng chứng.** `probe-core`, rc 0. Với `error_during_execution`, usage input/output dương dừng sau `auth, -p`. Cùng envelope chỉ có `cacheReadInputTokens=1200` gọi tiếp API giả. Nếu tổng `usage` đã báo 9 input và 2 output nhưng `modelUsage={}`, hoặc `modelUsage` có input/output dương và một trường cache sai kiểu, cũng gọi tiếp API giả. `_usage_sub` còn trả bốn số 0 cho một mục rỗng và bù 0 cho output bị thiếu. Các ca này đo quyết định trên envelope giả. Tài liệu provider tính cả token đọc/ghi cache vào input, và binary CLI có các trường usage riêng cho cache. [Claude Platform Docs, Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching).

**Đề xuất.** Tại bộ phân loại lỗi, xét dấu token dương từ cả cache và usage tổng, độc lập với bước kiểm tính đầy đủ để công bố số đo cuối. Cho phép đổi đường khi có dấu lỗi trước khi chạy hoặc hạn mức đã xác định. Khóa ca thiếu dữ liệu, cache-only và usage tổng dương với 0 lượt API. Giữ đối chứng hạn mức trước khi chạy được chuyển để tránh từ chối mọi lỗi khởi động.

### M3 [P1] Preflight và lượt model nạp khác nguồn settings — scripts/tl_core/llm_route.py:198–203, 257–275

**Kịch bản và bằng chứng.** Trên Claude Code 2.1.331, `probe-auth-live` chạy đúng lệnh local `auth status --json`. Với cấu hình trống và token OAuth giả, status khai `oauth_token/firstParty`. Thêm cấu hình người dùng định tuyến Bedrock trong HOME tạm làm cùng lệnh khai `third_party/bedrock`. Ghim `claude --setting-sources "" auth status --json` trả lại `oauth_token/firstParty` với cùng env và thư mục chạy. `-p` của code đã có `--setting-sources ""`; preflight thì thiếu. Thay status Bedrock đã đo vào `probe-core` cho chuỗi `auth, api`, bỏ qua sub vì thông tin từ cấu hình mà lượt model dự kiến tắt. CLI cũng trả `oauth_token` khi chỉ thấy token giả, nên đây là phân loại nguồn credential tại chỗ. Riêng `authMethod=[]` làm phép tra tập ném `TypeError` thay vì phân loại lỗi của tuyến. Ca giả CLI cũ không có `auth status` và ca timeout đều chuyển sang API giả, với 0 lượt `-p`.

**Đề xuất.** Dùng cùng lựa chọn settings và kiểm kiểu trường JSON trong `kiem_xac_thuc_sub`. Đo lại chính sách quản trị trên hai đường để giữ chặn thứ ba còn hiệu lực. Khóa bằng ca thay settings người dùng ở trên, JSON sai kiểu và đối chứng CLI cũ. Đồng bộ nhãn kết quả với mức chứng minh của preflight, vì `extra usage` và billing của tài khoản nằm ngoài tín hiệu đã đo.

### M4 [P1] Bằng chứng hết Điều lúc chạm CAP đến từ lần đọc khác — scripts/tl_core/llm_route.py:581–611

**Kịch bản và bằng chứng.** `probe-core`, rc 0, dùng `tl.extract_dieu` thật trên hai bản văn bản mẫu và mô phỏng I/O của tiến trình con. Lần đầu trả Điều 3 chạm CAP với một khoản ở cuối phần đọc được. Lần sau có thể resolve/cập nhật nguồn và tìm được Điều 4. `_co_dieu` chỉ kiểm rc và marker nên cho qua 47 ký tự của lần đọc đầu. Kết quả một khoản được `lech=[]` dù quan sát đầu chưa có ranh giới cuối Điều. Đối chứng giữ nguyên bản CAP thiếu ranh giới trả lỗi, giữ nguyên bản có cả Điều 3 và 4 thì đạt. Nếu Điều tiếp theo là 3a, `extract_dieu` đã cắt đúng Điều 3 nhưng code tìm 4 nên chặn oan. `probe-cli` cũng xác nhận đường `--dieu 3a` qua parse thật của `extract` bị rc 2 do cờ nhận int.

**Đề xuất.** Tại `cmd_extract`, trả thông tin CAP và ranh giới thực từ chính snapshot tạo ra Điều đích, sau khi tách trên cùng chuỗi. Tái dùng biên của trình tách, bao gồm Điều kế tiếp có hậu tố hoặc số nhảy. Ca đóng cần chứng minh không lấy bằng chứng giữa hai bản khác nhau, nhận đúng Điều có ranh giới và từ chối phần đuôi CAP. Khi thêm định dạng metadata, kiểm tương thích với người gọi `extract` dùng stdout hiện hành.

### M5 [P1] Nhật ký dùng chung đích với `--out` làm hỏng JSON đã xác minh — scripts/tl_core/ops_misc.py:3073–3083

**Kịch bản và bằng chứng.** `probe-cli`, rc 0. Dùng cùng một đường dẫn tệp thường cho `--out` và `--nhat-ky`. Trên kết quả sai, lệnh trả rc 5 nhưng byte tệp đã xác minh đổi vì bị nối thêm một dòng JSONL. Trên kết quả đúng, lệnh trả rc 0 và `ok=true` nhưng tệp mới cũng không đọc được bằng `json.loads`. Hai ca đều báo `Extra data`. Đối chứng chỉ dùng `--out` giữ nguyên byte ở rc 5 và ghi JSON đọc được ở rc 0. Lỗi có từ khi PR kết hợp hai đầu ra, vẫn còn sau vá N5.

**Đề xuất.** Kiểm đích trùng trước model ở handler, kể cả tên khác cùng định danh tệp. Khóa bằng ca hai đường dẫn giống nhau, hai cách trỏ cùng đích và hai đích độc lập. Ca từ chối phải kiểm 0 lượt model, byte đích cũ và mã thoát. Giữ nhật ký JSONL nối tiếp cho trường hợp đích độc lập. Khi mở kiểm đích, giữ đường dẫn hợp lệ cho tệp chưa tạo.

### M6 [P2] Doctor xác nhận được cách dùng API từ một object rỗng về nghiệp vụ — .claude/dev/launcher.py:4814–4833

**Kịch bản và bằng chứng.** `probe-api`, rc 0. Một HTTP 200 giả chỉ mang `type`, đúng tên model và `usage={input_tokens:0, output_tokens:0}` được `DUNG_DUOC`. Mẫu thiếu cả định danh, vai trò và nội dung mà Message đối chứng có. `t162` khóa riêng type/model/token âm và hiện dùng mẫu dương thiếu các trường Message khác. Lượt này đã giết lại cả ba đột biến đó.

**Đề xuất.** Xác nhận các trường bắt buộc của Message và dấu dương phù hợp với probe một lượt đơn giản. Thêm mẫu 0+0/thiếu payload và đối chứng Message thật về cấu trúc. Khi xác nhận model, thử alias chính thức được hỗ trợ để giữ đường kiểm hợp lệ, với mock transport.

### M7 [P1] Gate kiểm bảng writer vẫn có assertion ghim số cũ — .claude/hooks/pretooluse_guard_test.py:635–641

**Kịch bản và bằng chứng.** Hai lệnh mới có `read_only=False`; bảng hook và golden cùng ghi đúng. Với Ruff ghim 0.15.15, `probe-hook.py` chạy nguyên thân t15/t33. Base trả rc 0, t15 và t33 đều đạt với 106 writer. HEAD có t15 đạt và hook trả rc 0 với `101 writer top-level + 7 writer LONG = 108`, nhưng t33 đỏ vì còn đòi `= 106`; probe trả rc 1. Hook thực tế trả `deny` đúng lớp writer cho cả `llm-order` và `llm-khai-niem` trong ngữ cảnh `tl-auditor`. Đây là lỗi gate ở chính HEAD dù lệnh trực tiếp `--kiem-bang` xanh.

**Đề xuất.** Cập nhật số kỳ vọng của t33 theo 108 và giữ kiểm nguồn runtime. Khóa hai tên mới bằng đối chứng tên có mặt trong bảng writer và hook trả deny do `read_only=False`. Việc chỉ nới assertion số đếm có thể che drift sau này, nên giữ ca t15 đối chiếu đủ tập và các đột biến bỏ từng tên.

### Bảng lớp nguyên nhân

| Lớp | Nguồn và biểu hiện | Mức còn mở | Ca đóng |
|---|---|---|---|
| `ranh-gioi-khoan` | F1 → N1 → M1 | P1 | Nguồn thực có số/mất số, ô xuống dòng và ngoặc gọi tắt, đối chứng đúng lẫn sai. |
| `phan-loai-sub` | F2 → N2 → M2 | P1 | Đếm fallback khi token cache/tổng dương và khi có lỗi xác định trước model. |
| `dinh-tuyen-sub` | F3 → N4 → M3 | P1 | Cùng provider/settings tại preflight và lượt model, kiểm kiểu và CLI cũ. |
| `ghi-tep-local` | F4 → N5, M5 | P1 | Hai đích trùng bị chặn trước model, tệp cũ giữ nguyên khi kết quả bị từ chối. |
| `chon-config-profile` | F5 | Đã đóng ở lượt 2, kiểm lại đường CAP | Hai lời gọi con giữ cùng `--config` và `--profile`. |
| `day-du-dieu` | F6 → N6 → M4 | P1 | Biên từ chính snapshot, gồm Điều sau có hậu tố và đuôi CAP. |
| `phan-loai-http-api` | F7 → N7 | Đã đóng cho ưu tiên status/type | SDK giả kiểm 504/body chồng, 503/529/429 và lỗi không có status. |
| `bang-chung-doctor` | F8 → N8 → M6 | P2 | Fixture đủ Message đối chiếu HTTP 200 thiếu payload và 0+0. |
| `thu-tu-duong` | F9 | Đã đóng ở lượt 2 | Cờ rỗng và symlink đứt giữ pass trong core suite. |
| `tin-hieu-subprocess` | F10 | Đã đóng ở lượt 2 | Đột biến bỏ rc, is_error hoặc settings vẫn bị core suite giết. |
| `so-dieu-tu-tep` | F11 → N3 | Đã đóng | UTF-8 BOM, không BOM, và số Điều xung đột. |
| `giai-ma-utf8` | F12 | Đã đóng ở lượt 2 | Ca byte mã cũ trong selftest r380 vẫn đạt. |
| `dong-bo-hook-registry` | M7, xuất hiện sau khi thêm hai writer | P1 | t15/t33 cùng đạt, bỏ riêng từng writer làm t15 đỏ đúng lý do. |

13 lớp đã rà, 7 lớp còn mở gồm 6 P1 và 1 P2. 7 mục M là các biểu hiện tại SHA lượt này. Các mục M1–M6 tiếp nối lớp đã có hoặc cho thấy cách vào khác của lớp đó. M7 là lớp mới.

## Đã kiểm mà không thấy lỗi

Môi trường Linux x86_64, Bash, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, sandbox `workspace-write`. Đo trên hai clone detached ngoài checkout được giao. Các test chạy với HOME/TMP tách riêng, proxy loopback, chỉ cho Git transport file và executable Claude giả bảo vệ PATH. Phép kiểm Claude thật giới hạn ở version/help và auth status cục bộ, với output xác thực lọc còn trạng thái và tên các trường. `run-check TÊN CHECKOUT LỆNH…` tại scratch lưu command, stdout, stderr và rc trong `logs/`.

| Lệnh trên HEAD | Trạng thái và bằng chứng |
|---|---|
| `python scripts/tl_core/llm_route_test.py` | `passed`, rc 0, 40/40 ca và 47/47 đột biến. |
| `python .claude/dev/launcher_test.py --lap-ca t162 --lan 1` | `passed`, rc 0, 1/1 ca, 0 bỏ qua, 0 hỏng. |
| `python .claude/hooks/pretooluse_guard.py --kiem-bang` | `passed`, rc 0 với Ruff 0.15.15. Đối chiếu 108 writer và 93 lệnh đọc từ runtime, đo help 26/26 chương trình. 35 cờ riêng ở tầng 2 ghi “KHONG DO DUOC”. Ca t33 của test suite được báo riêng ở M7. |
| `python scripts/tl_core/command_registry_test.py` | `passed`, rc 0, 10 tests, `OK`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed`, rc 0, `ok=true`, 194 lệnh, 26 cards, 0 lỗi, 0 cảnh báo. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed`, rc 0, `ok=true`, 20/20. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed`, rc 0, `ok=true`, 187/187, `package_hash_match=true`. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed`, rc 0, `ok=true`, 15 checks. |
| `python scripts/gen_instructions.py --selftest` | `passed`, rc 0, 44/44. |
| `python .claude/dev/ci_dang_ky_test.py` | `passed`, rc 0, 32/32 đăng ký và Ruff CI 3/3 hợp đồng. |
| `loi_ruff_ci()` qua `runpy.run_path(".claude/dev/ci_dang_ky_test.py")` | `passed`, rc 0, `RUFF_CONTRACT 3 []`. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | `failed`, rc 1 ở HEAD và base. Ruff 0.15.15 báo cùng 12 F821 theo mã/thông điệp. Hai vị trí dịch một dòng, delta chẩn đoán 0. |
| `python scripts/tl.py release-bundle --out <scratch>/release{1,2}.zip --json` (hai lần) | `passed`, cả hai rc 0, `ok=true`, 187 tệp. SHA-256 hai archive đều `9d13cbc68b6a1a30cd9856d7f25cb1ee50829df993cc8259efcf1b9ffa0b1998`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --archive <scratch>/release1.zip --json`, rồi verify strict từ cây giải nén | `passed`, mỗi lần rc 0. `archive_ok=true` và lần verify cây giải nén đạt 187/187 với package hash khớp. |
| `python <scratch>/probe-hook.py` với Ruff ghim | HEAD `failed`, rc 1, t15 đạt, t33 đỏ do 108 so với 106. Base `passed`, rc 0, t15/t33 đạt. Lần đầu dùng executable Ruff 0.16.9 trên PATH nên hai ca fail-closed rc 4 trên cả hai vế. Phép đo quyết định lặp bằng 0.15.15. |

### Đột biến trên bản sao tạm

- `probe-mutations.py`, rc 0. Đối chứng HEAD xanh trước khi đổi. 12/12 mutant core làm đúng ca đích đỏ với `TinHieuChotCa`. Ca số khoản bắt đánh theo vị trí; ca mơ hồ bắt nuốt dòng trước khoản đầu; ca chữ “là” bắt tách ở vị trí thứ hai trong mẫu đơn giản; ca BOM bắt mất tiêu đề. Các ca sub lần lượt bắt nhận kết quả từ chối, nhận kết quả 0 token, gọi API sau lượt đã chạy, nhận API key và nhận provider sai. Ca CAP mất lần kiểm Điều 4 bật assertion vì thiếu chứng cứ ranh giới. Ca 504 đỏ khi type thắng status.
- Cùng script giết 8/8 mutant launcher ở t162. Ba mutant mới bỏ riêng type, bỏ model và nhận số âm làm từng payload đích được gắn nhầm `DUNG_DUOC`. Năm ca còn lại bắt gọi mạng mặc định, phân loại sai 400 hết credit, thứ tự tên biến sai, nhận HTTP 200 rỗng và nhầm mất mạng thành lỗi xác thực.
- `run-cli-mutations.py`, rc 0. Chạy nguyên thân `r380_llm_khai_niem_bien_dau_vao` trên cây tạm. Đối chứng rc 0. Bỏ giữ mode hoặc bỏ kiểm thư mục trước model làm ca rc 1. Bỏ riêng `utf-8-sig` vẫn rc 0 vì hàm nhận tiêu đề tự gỡ BOM. Bỏ cả hai chốt làm rc 1. Writer ghi thẳng vẫn qua ca r380, phù hợp vì ca hiện tại chưa tiêm lỗi giữa lần ghi.
- `probe-hook-mutations.py --metadata`, rc 0. Bỏ riêng mỗi tên writer làm t15 đỏ với hook rc 4 và thông báo thiếu đúng tên. Đổi metadata `llm-khai-niem` sang `read_only=True` làm hook rc 4 và golden rc 2. Ca golden đỏ là `tool_inventory_inventory_decision`.

### Full selftest đối chiếu base

Cả hai vế chạy `python scripts/tl.py --selftest` với `TL_SELFTEST_NO_NET=1` và cùng cấu hình cô lập đã ghi. Base tree là `f78a9c73b33de71d25116181554f0958b52c1510`. Log `selftest-head.*` và `selftest-base.*` giữ rc và stdout/stderr thật.

| Checkout | Trạng thái | Bằng chứng |
|---|---|---|
| HEAD | `failed`, rc 1 | 1774/1789. Cả 3 ca r380 đạt. SHA-256 stdout `69145017927989257ec3c18cf083e936acb629d2296261bb4b9c392fb1da3d2a`. |
| Base | `failed`, rc 1 | 1771/1786. SHA-256 stdout `f1a72762293c781af0e7f0006a820f385d15402bf1701d5f69e11ad4dfd333e7`. |

`probe-selftest-delta.py`, rc 0, so theo ID của [FAIL]: 15 ca chung, 0 ca đỏ mới, 0 ca hết đỏ. Các ca chung gồm 8 `r973_bootstrap_*`, 5 `wp433_*`, `wp727_tl_gws_refresh` và `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`. Riêng r226 bị chính cách ghim `core.abbrev=7` qua môi trường của runner lấn cấu hình tạm 8 của ca. `probe-selftest-r226.py` chạy nguyên thân ca trên mỗi SHA, rc 0 cho phép đối chiếu, xác nhận cả hai vế False với override cấp lệnh và True với ghim repo-local. Hai báo cáo full selftest ở bảng vẫn là `failed`. Các thư mục ignored do full suite sinh nằm trong clone đo.

## Không đo được

- `not_run` — Model Claude thật, Anthropic Messages thật, hóa đơn/hạn mức/extra usage của tài khoản, corpus LIVE, CI hoặc provenance GitHub, Windows/Cowork, toàn bộ bộ test hook. Ca URL/token dùng fixture và transport giả. Ca t15/t33 chạy đúng hai thân hàm stock.
- `not_measured` — Model/effort phục vụ của reviewer theo receipt terminal, provider/model của Executor theo receipt và revision/spec hash/generation chính thức. Review scope và authority của lượt này lấy từ chỉ thị điều phối exact SHA. `run.json` quan sát trong lúc thực thi neo provider/surface/transport và SHA. Model/effort của run chưa có số đo terminal quan sát được.
- `skipped` — Không có ca skip ở core hoặc t162. Các mục help ghi "KHONG DO DUOC" được giữ riêng và không tính là đã xác nhận.

Readback cuối của checkout được giao cho cùng HEAD và tree. Diff tracked và index đều rỗng với SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Snapshot đầu có `.codex/` ignored, snapshot cuối có thêm đúng `.review/VERDICT.md` untracked. Đây là quan sát ở hai mốc. Diff PR có 28 tệp và `git diff --check <base> HEAD` rc 0.

VERDICT: REQUEST_CHANGES
