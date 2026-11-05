verdict: approve
reviewed_sha: 69f48261618a72b9058e88e875ad8de5d52a8860
so_lop: P0 0 / P1 0 / P2 0 / P3 0

Reviewer: `openai_codex`, phiên độc lập với executor; bề mặt thực thi là Codex qua API với shell cục bộ trong sandbox, transport `machine`. Không có chứng thực model/effort phục vụ từng request. Review ngoại tuyến theo `prompt.snapshot` và `VERDICT-luot1.md`, trên hai trục nội dung yêu cầu và standards/security.

Phạm vi: `git -C cay-kho diff 07b773c 69f4826 -- CLAUDE.md`; base đầy đủ `07b773c806bf6a42a4f0e4c88b4e26c6001f35ab`, head đúng SHA yêu cầu, tree `8f615ce4f93fbae90c9a064378142ebd49760426`. Diff thực tế **+10/−5 dòng**, do hai commit `a5fc816` và `69f4826`; hồ sơ land của commit xen giữa `d96716c` nằm ngoài phạm vi này. Mọi neo tệp:dòng dưới đây tính từ `cay-kho/` tại reviewed SHA.

## ĐỐI CHIẾU LƯỢT TRƯỚC — F1: đóng, ĐÃ VÁ THẬT

Đã tìm trên toàn bộ 1.147 dòng của `CLAUDE.md`, bằng các mẫu ngày 30-09/09-30, từng mốc giờ, `rest-kho`, `curl` và các đoạn REST/403/GraphQL; đọc cả đoạn readback/MCP, §Đẩy ref và §Gọi agent đa nền. Không chỉ xét các dòng trong diff.

`CLAUDE.md:738`–`:742` tuyên bố nhãn áp dụng cho **mọi mốc giờ 30-09 trong tệp**, nêu đích danh cả ba vùng và đủ tám dạng mốc giờ; giờ chạy cùng độ phủ client là lời khai của executor, thiếu log gốc, **KHÔNG ĐO ĐƯỢC**. Nhãn phân biệt rõ chúng với trạng thái HTTP được reviewer đo ở giờ khác.

| Mốc/lời khai | Chỗ xuất hiện ngoài danh sách nhãn | Bằng chứng đã sửa cách khai |
|---|---|---|
| Hook `06:29Z`, `rest-kho=OK` | `CLAUDE.md:748` | Câu bắt đầu bằng “Lời khai”; `:749` ghi không có biên nhận, KHÔNG ĐO ĐƯỢC, kể cả vế “từ trước khi mục này được sửa”. |
| `06:30–06:31Z`, `07:10Z` | `CLAUDE.md:726` | Cả hai nằm trong danh sách nhãn `:739`, với phạm vi mục REST được nêu tại `:738`. |
| `06:31Z` | `CLAUDE.md:163`, `CLAUDE.md:627` | Cả hai chỗ đều thêm ngay nhãn “mốc giờ và client: lời khai chưa có biên nhận”, dẫn về nhãn chung. |
| `06:31–06:33Z` | `CLAUDE.md:157` | Thêm nhãn tại chỗ cho mốc giờ và client, dẫn tới §Gọi agent đa nền. |
| `07:10–07:11Z` | `CLAUDE.md:732` | Nhãn `:738`–`:742` phủ mục này và liệt kê đúng mốc tại `:739`. |
| `07:11Z` | `CLAUDE.md:630` | Nhãn chung nêu rõ §Đẩy ref và liệt kê đúng mốc; con trỏ tới nhãn đã có ngay tại `:627` trong cùng đoạn. |
| `07:51–07:57Z`, “`curl` 10” | `CLAUDE.md:728` | Nhãn chung liệt kê đúng mốc, đồng thời nêu chính ví dụ “`curl` 10” là độ phủ client chưa có log gốc. |

Các mốc lặp lại ở `CLAUDE.md:739` thuộc chính nội dung nhãn. Không tìm thấy lần xuất hiện cùng lớp nào còn nằm ngoài phạm vi nhãn. F1 đóng ở lỗi **kể lời khai chưa có biên nhận như phép đo đã kiểm**; việc executor thực sự chạy vào các giờ ấy vẫn chưa được xác minh.

## Đối chiếu neo mới và mâu thuẫn

Đã đọc trực tiếp toàn bộ hai verdict được thêm làm neo:

| Neo | Nội dung kiểm được trong tệp |
|---|---|
| `ops/reviews/pr631-review-3-opus-max/VERDICT.md:78` | Ghi phép đo các đường con bằng `urllib` lúc 07:32 và một tập con bằng `curl` lúc 07:40; bảng từ `:138` ghi kết quả HTTP cho các đường kho/PR/comment và hai loại 403. `:183`–`:185` nói rõ giờ chạy executor và hook thiếu biên nhận. |
| `ops/reviews/pr631-review-4-opus-max/VERDICT.md:39` | Ghi reviewer đo lại đủ 14 đường bằng cả hai client ở 08:04; mục “Phép đo lại” từ `:145` ghi chi tiết trạng thái. `:155`–`:156` phân biệt đếm danh sách, tái lập trạng thái và xác minh lần chạy; `:197`–`:200` tiếp tục ghi không có biên nhận giờ executor và không biết `curl` đã phủ 10 đường nào. |

Vì vậy câu mới “trạng thái HTTP do reviewer đo lại ở giờ khác” có neo đúng nội dung. Nó không nhận reviewer đã xác minh hook, giờ executor hay tập 10 đường của executor. Phần readback cũng phù hợp với các số đếm và đối chiếu hai client được ghi trong verdict lượt 4 tại `:51`–`:54`, `:168`.

Không phát hiện finding mới P0/P1/P2/P3. Các giới hạn về phiên đã đo, đường chưa đo, REST DELETE/phương thức ghi, khả năng `gh`/GraphQL và nguyên nhân thay đổi hạ tầng vẫn nhất quán với nhãn mới. Bản vá không nhận đã đóng những khả năng vận hành còn chưa đo.

Quét đúng **10 dòng thêm** bằng 20 mẫu bí mật (hai bảng mẫu trong `scripts/pkg_secret_scan.py`, `scripts/hooks/secret_guard.py`, bổ sung mẫu PAT GitHub): **0 hit**. Kiểm các chuỗi bỏ qua CI, trailer bỏ qua kiểm tra và cú pháp mở biểu thức Actions: **0 hit trong phần thêm**; không chép các chuỗi ấy vào verdict. `git diff --check 07b773c 69f4826 -- CLAUDE.md`: **rc=0**. Ba dòng chứa chuỗi thoát ASCII cho U+0308 giữ nguyên so base; U+0308 thật vẫn bằng 0.

## Cổng

Chạy mới tại reviewed SHA trong `cay-kho`, với `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`; mọi Python dùng `-B`. `TMPDIR` và `TL_CACHE_DIR` trỏ tới đường dẫn tuyệt đối của `out/`, để cả phép thử tệp tạm của `tl.py` nằm ngoài checkout. Không dùng kết quả cổng lịch sử thay cho lần chạy này.

| Lệnh | rc | Trạng thái và marker dương |
|---|---:|---|
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | **passed** — `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 -B .claude/dev/packet_loop.py adr-song --root .` | 0 | **passed** — `adr-song: sạch — 62 ADR trên đĩa, 62 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` |
| `python3 -B scripts/tl.py doc-claims-check --json` | 0 | **passed** — `ok: true`, `schema: doc_claims_check.v1`, `files_scanned: 124`, `flags: []`, `layers_skipped: {}`, có `CLAUDE.md` trong `roots`; stderr rỗng. |

JSON cổng cuối có `advisory_count: 381`, `claims_flagged: 381`, mọi giá trị `by_layer` đều 0, `strict: false`. Các advisory không phải lỗi chặn. Cả ba cổng yêu cầu đều chạy và đạt; không có cổng bị skipped hoặc not_run. Đây là cổng hình thức, không xác minh các phép đo mạng lịch sử.

## KHÔNG ĐO ĐƯỢC

- Không gọi mạng. Mã HTTP, header, nội dung comment, số đếm ký tự và kết quả hai client lịch sử được đối chiếu với verdict lưu trong kho; tôi không đo lại chúng từ GitHub và không coi đường dẫn log `scratch/` được kể trong verdict là log thô hiện có trong checkout.
- Giờ chạy, hook và độ phủ client của executor vẫn chưa có biên nhận gốc được xác minh. Việc đóng F1 là chấp nhận cách khai đã giới hạn đúng bằng chứng.
- Không thử `doctor`, hook phiên, MCP, `gh`, GraphQL POST, REST DELETE hay phương thức ghi; không kiểm trạng thái GitHub/CI hiện tại, điều kiện merge/land hoặc commit hồ sơ land ngoài phạm vi.
- Không xác định tầng thay Authorization hay nguyên nhân chuyển 403 sang 200. Không dùng số đo của phiên khác để xác nhận thời điểm executor hoặc trạng thái chung của hạ tầng.

Tôi không sửa, tạo hay xoá bất kỳ tệp nào trong `./cay-kho`. Snapshot trước/sau các phép kiểm gồm **14.002 tệp và 1.033 thư mục**, không symlink; băm tổng hợp đường dẫn, nội dung và mode cùng bằng `f8b82822d19a75f7b55444250e2d46edfd2c3eba325e32f47bcaee1cd27a8885`, gồm cả `.git`. HEAD/tree giữ nguyên; status cuối rỗng kể cả ignored/untracked. Snapshot chứng minh không có delta quan sát được giữa hai mốc. Đầu ra giao nộp duy nhất là `./out/VERDICT.md`.
