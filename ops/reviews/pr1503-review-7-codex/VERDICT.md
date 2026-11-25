# Verdict PR #1503 lượt 7 — Codex

reviewed_sha: b5dc962aa77d9d56acacafda406f9aa1ab202c8d
reviewed_tree: 8f8c1f38f95e164d918ef9c141e29444f9a00951
base_sha: 5259239d763c9ffc1677f033bd9a9cf23ede9299
nang_tran: chủ kho nâng trần lên 7 theo chỉ thị dẫn comment PR 7134111088 (lời gọi thứ 7, cuối cùng)

## Đối chiếu lượt 6 (và các lớp còn mở)

Đối chứng lượt 6 tại `9af35ba16c9c096d6a42330d92c8ae8c2c6a5b1c`. Các phép đo dùng bản sao detached và đồ giả cục bộ trong `/tmp/pr1503-r7.6R2WRc`.

| # | Trạng thái | Bằng chứng |
|---|---|---|
| S1 | ĐÃ ĐÓNG đường chuyển API sau spawn | Probes chạy tiến trình Python thật thay CLI. Sau lỗi đọc bền, lượt 6 gọi API giả, HEAD dừng với 0 lượt API. Sau lỗi dọn thư mục model, lượt 6 gọi API giả, HEAD trả `sub`. Spawn lỗi thật và lỗi chuẩn bị vẫn chuyển. Thu hồi tiến trình sau lỗi đọc còn T2. |
| S2 | ĐÃ ĐÓNG các ca đã báo, CÒN MỞ lớp ranh giới | Ở nguồn mất số, kết quả gộp vì ký tự ngoặc được trích dẫn đổi rc 0 → 5 và giữ tệp cũ. Kết quả đủ hai mục đổi rc 5 → 0. Dòng gãy trước từ nối cũng đổi rc 0 → 5. Phép cắt sai quanh dấu ngoặc đóng được trích dẫn đổi rc 0 → 5, phép cắt đúng đạt. Ca câu đầu `Điều 3 của quy chế…` chỉ đạt khi đủ hai mục và metadata `dieu=null`. Nguồn trộn số với dấu kép thẳng được trích dẫn vẫn lọt, xem T1. |
| S3 | ĐÃ ĐÓNG | Hai chiều quan hệ tổ tiên đều rc 2. Số lần gọi đồ giả đổi 1 → 0 và HEAD không tạo đích. Hai tệp ngang cấp và hai cha mới riêng vẫn rc 0, JSON/JSONL đọc lại được. Cặp hardlink dừng trước model và giữ byte cũ. |
| `ranh-gioi-khoan` | CÒN MỞ · P1 · S2 → T1 | Cùng bộ quét quyết định còn mở trích dẫn và chọn từ nối. Chốt phải nhận tiếp dòng khi trích dẫn thật còn mở và từ chối nuốt dòng độc lập sau một trích dẫn đã khép. |
| `phan-loai-sub` | ĐÃ ĐÓNG lớp chuyển tuyến | Với runner thật, auth không đạt và lỗi trước spawn đi API giả. Timeout, lỗi đọc và lỗi dọn dẹp sau spawn có 0 lượt API. |
| `ghi-tep-local` | ĐÃ ĐÓNG trong phạm vi S3 | Hai chiều tổ tiên và đối chứng ngang cấp, cha riêng, hardlink. |
| `thu-hoi-tien-trinh-sub` | SINH LỖI MỚI · P2 · T2 | Timeout thông thường thu hồi được. Lỗi đọc lặp lại khiến lần thu hồi phụ thuộc vào chính thao tác đọc đã hỏng. |

Hai trong ba lớp mang sang từ lượt 6 đã đóng trong phạm vi đo. Một lớp còn mở và một lớp mới được ghi riêng.

## Findings mới

### T1 [P1] Dấu kép thẳng được trích dẫn làm một dòng mất số lọt vào khoản trước — scripts/tl_core/llm_route.py:502–508,524–546

`ranh-gioi-khoan` · Biểu hiện mới được đo trong chế độ có số, cùng cơ chế với S2. Một định nghĩa có số kết thúc bằng dấu ngoặc kép thẳng được trích nguyên ký tự bên trong một cặp ngoặc kép cong đã khép. Dòng kế là một định nghĩa độc lập bị mất số, rồi đến khoản 2. `_quet` đổi cờ `thang` ngay trong trích dẫn cong và giữ cờ sau khi cặp cong đóng. `_dang_mo` vì thế báo còn mở và cho ghép dòng mất số vào mục 1. Kiểm số liên tục vẫn qua với hai mục, mặc dù nguồn có ba dòng định nghĩa.

`run-check head structure-head python /tmp/pr1503-r7.6R2WRc/probe-structure.py` và cùng phép đo trên `prior` đều rc 0. Ca `mixed-numbered straight-quote` trên cả hai SHA cho `scan-open True`, CLI handler rc 0, `ok=true`, chỉ hai mục và ghi đè tệp có sẵn. Trên HEAD, đối chứng dùng dấu ngoặc tròn được trích dẫn cho `scan-open False`, rc 5, giữ byte cũ. Trích dẫn thật mở qua hai dòng vẫn đạt rc 0. Nguồn mất số hoàn toàn chứa dấu kép thẳng tương tự cũng đã được vá và đạt với đúng hai mục.

Sửa tại `_quet` vì `_dang_mo` và `_tu_noi` cùng dùng trạng thái này. Chỉ cho dấu trích dẫn điều khiển loại trong đúng ngữ cảnh đang mở. Khóa ca trộn số ở trên bằng rc 5, byte cũ giữ nguyên, cùng ca mở trích dẫn thật qua hai dòng phải đạt. Giữ cả ca dấu ngoặc tròn nằm trong trích dẫn và từ nối sau ngoặc lồng. Đột biến bật lại phép đổi trạng thái dấu thẳng khi đang nằm trong cặp cong phải làm ca trộn số đỏ. Khi sửa thứ tự mở và đóng, cần đo dấu kép lồng có chủ ý để tránh chặn nhầm tiếp dòng hợp lệ.

### T2 [P2] Runner giết tiến trình khi lỗi đọc kéo dài nhưng có thể chưa thu hồi nó — scripts/tl_core/llm_route.py:99–105

`thu-hoi-tien-trinh-sub` · `communicate()` gặp EIO, runner gọi `kill()` rồi thử lại `communicate()`. Nếu lỗi đọc tiếp diễn, lần hai bị nuốt và runner thoát mà chưa gọi `wait()`. Runner dùng chung cho model và `auth status`.

Probe `read-error` giữ một đối tượng `Popen` thật, chờ tiến trình Python tạo dấu đã chạy rồi tiêm EIO vào lần đọc và lần đọc lại. Trước khi probe thực hiện dọn riêng, Linux `waitid(WEXITED | WNOWAIT)` còn quan sát tiến trình con bị SIGKILL với `returncode=None` trên HEAD. Lượt 6 dùng `subprocess.run` và tiến trình đã được thu hồi tại cùng điểm quan sát. Ca timeout đơn giản trên HEAD có `returncode=-9` và `waitid` báo đã thu hồi. Đường model vẫn dừng với 0 lượt API ở ca EIO trên HEAD.

Đặt phần chờ và đóng pipe độc lập với việc đọc lại trong nhánh lỗi của `_chay_co_moc`. Giữ ngoại lệ ban đầu để ngữ nghĩa timeout và I/O ổn định. Ca kiểm cần giữ đối tượng tiến trình và quan sát từ hệ điều hành trước khi dọn. Đột biến bỏ đợi thu hồi phải đỏ dù vẫn phát ngoại lệ timeout. Chờ hoặc đọc kiểu không giới hạn có thể làm lệnh mắc lại khi một tiến trình khác còn giữ pipe, vì vậy cần đo cả giới hạn thời gian của nhánh dọn dẹp.

## Đã kiểm mà không thấy lỗi

- `cmd_extract` thật, với transport giả, giữ nguyên tiêu đề nguồn sau dòng phân cách. Tiêu đề có `.` và `:` đều cho extract rc 0 và handler rc 0. Tiêu đề không dấu cho extract rc 0, handler HEAD rc 5, giữ tệp cũ. Hành vi này khớp giới hạn chủ kho đã khai. Phép đo dùng fixture, không khẳng định hiện trạng corpus.
- Auth giả qua tiến trình thật với cùng cấu hình argv và env. Auth first-party đúng trả `sub`. Auth dạng API key hoặc timeout chuyển sang API giả trước khi model spawn. Trace `runtime-head-measured` và `runtime-prior-measured` đều rc 0. Hai lần dựng probe đối chứng trước đó có kỳ vọng sai về chữ ký `mkdtemp` và mã thoát của con bị giết, đã sửa trước lần đo dùng trong verdict.

### Preflight và môi trường

Checkout rời, detached. Ref `origin/master` cục bộ và `git merge-base HEAD origin/master` cùng trỏ base đã giao. Prompt SHA-256 `7d13011b1b4b9632f56d1bc57869adf0c6909897b83dc1ee84bf1ff8d62eb3c3` khớp `checkpoint.json` và `run.json` của run `e961165586ef45f0bb94405a972f2953`. Cả hai neo đúng HEAD. Phạm vi ghi là `.review/VERDICT.md` và vùng tạm ngoài checkout. Review Class đánh giá theo diff là `sensitive` vì có launcher và đường credential. Đã kiểm trục đặc tả và standards/security.

`provider=openai_codex`, `execution_surface=codex_cli`, `transport=machine` theo run cục bộ. Sandbox `workspace-write`, Linux x86_64, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, Bash. Các gate chạy trên bản sao detached với `core.abbrev=7`, HOME/cache/tmp riêng, môi trường tối giản, proxy loopback, Git transport file và stub chặn CLI bên ngoài. `run-check` ghi OID/tree, argv, rc, stdout/stderr và SHA-256 mỗi luồng tại `/tmp/pr1503-r7.6R2WRc/logs/`.

Diff toàn PR có SHA-256 `cee77903d66c0bbc8f953fdf71137ad69516fb9b4199ebd857ec08a7ee2ac13f`. Diff từ lượt 6 có SHA-256 `44b4b1c5f5cdbf17202dd6cafc1aeb34b6f55bb0553abb4fe0420914d137ffe5`. `git diff --check` rc 2 cho mỗi phạm vi vì ba dấu ngắt dòng Markdown bằng hai khoảng trắng trong verdict lượt 6 đã lưu. Cùng phép đo với `git -c core.whitespace=-blank-at-eol diff --check` rc 0.

### Gate cục bộ

| Lệnh trên HEAD, trừ nơi ghi riêng | Trạng thái và bằng chứng |
|---|---|
| `python scripts/tl_core/llm_route_test.py` | `passed`, rc 0, 47/47 ca, 71/71 mục đột biến, 70 ID khác nhau. |
| `python .claude/dev/launcher_test.py --lap-ca t162 --lan 1` | `passed`, rc 0, 1/1, 0 bỏ qua, 0 hỏng. |
| `python .claude/hooks/pretooluse_guard.py --kiem-bang` | `passed`, rc 0, 108 writer, 93 lệnh đọc, help 26/26 chương trình và 425 cờ xác nhận. |
| `python scripts/tl_core/command_registry_test.py` | `passed`, rc 0, 10 test, `OK`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed`, rc 0, `ok=true`, 26 cards, 0 lỗi, 0 cảnh báo. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed`, rc 0, `ok=true`, 20/20. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed`, rc 0, `ok=true`, 187/187, package hash khớp. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed`, rc 0, `ok=true`, 15 checks. |
| `python scripts/gen_instructions.py --selftest` | `passed`, rc 0, 44/44. |
| `python .claude/dev/ci_dang_ky_test.py` và probe riêng `loi_ruff_ci()` | `passed`, rc 0 từng phép, đăng ký 32/32, Ruff contract 3/3, phản chứng 1226/1226. Probe in `RUFF_CONTRACT 3 []`. |
| `python -m ruff check --no-cache --select F --output-format json scripts/tl.py` | `failed`, rc 1 cả HEAD và base với Ruff 0.15.15, cùng 12 F821 và cùng đa tập thông báo. Delta bằng 0. |
| `python scripts/tl.py release-bundle --out <scratch>/bundle{1,2}.zip --json`, mỗi tệp một lệnh, rồi `cmp` | `passed`, rc 0 từng lệnh. Cả hai bản có 187 tệp, `reproducible=true`, SHA-256 `53ca1b75720a74976ba89372aa5ecd55630a8e21a4ef946b47e14f903bed4407`. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --archive <scratch>/bundle1.zip --json` | `passed`, rc 0, `ok=true`, 187/187, archive hợp lệ. |

### Đột biến trên bản sao tạm

- `run-check head mutants python <scratch>/probe-mutants.py` rc 0. Hai ca đích stock đạt. 8/8 đột biến làm đỏ đúng assertion, gồm bốn về phân đoạn và tiêu đề, bốn về mốc spawn và phân loại lỗi. Các assertion quan sát được gồm từ chối gộp dòng gãy ở nguồn mất số, không coi dấu ngoặc tròn được trích dẫn là cú pháp, không nuốt câu tham chiếu Điều làm tiêu đề, chặn API sau EIO và giữ fallback khi spawn thật thất bại.
- `run-check head destinations-head python <scratch>/probe-destinations.py` rc 0. Lấy nguyên thân ca `r380_llm_khai_niem_bien_dau_vao` từ selftest. Ca gốc trả `True`. Bỏ riêng mỗi chiều quan hệ tổ tiên trong hai bản sao của `ops_misc.py` lần lượt làm ca trả `False`. Đối chứng trên lượt 6 xác nhận khi thiếu chốt thì model bị gọi, JSON đầu ra đã được ghi và nhật ký chưa được tạo.
- Đột biến giữ `kill()` nhưng bỏ bước thử thu hồi vẫn qua ca stock `ca_sau_khoi_chay_khong_chuyen`. Ca này khóa phân loại timeout. T2 dùng `waitid` để quan sát thu hồi trực tiếp. Suite lõi tiếp tục đếm hai mục đột biến trùng ID `bo_hai_ve_khac_rong` như lượt 6.

### Full selftest đối chiếu base

Chạy `python scripts/tl.py --selftest` với cùng cấu hình cô lập trên hai mốc.

| Mốc | Trạng thái | Bằng chứng |
|---|---|---|
| HEAD `b5dc962aa77d9d56acacafda406f9aa1ab202c8d` | `failed`, rc 1 | 1774/1789, cả ba ca `r380_*` đạt. SHA-256 stdout `0a8a67679776e924b32a50d31af5c2e0b2fb523f5a5a26b62559ed34726b2998`. |
| Base `5259239d763c9ffc1677f033bd9a9cf23ede9299`, tree `f51dd6a68bd96bcf71a1fb351e652a3eee318a1b` | `failed`, rc 1 | 1771/1786. SHA-256 stdout `139183a692e6d900ff7e95b3a5c925ec316136dd51e8e4229e9e0d392f78aa85`. |

So đa tập ID `[FAIL]` thu được đúng 15 ca chung, 0 ca đỏ mới và 0 ca hết đỏ. Tập chung gồm tám ca `r973_bootstrap_*`, năm ca `wp433_*`, `wp727_tl_gws_refresh` và `wp1099_nlm_nap_lai`. Kết quả selftest đầy đủ ở cả hai mốc vẫn là `failed` trong môi trường này.

Giải nén bằng `python -m zipfile -e <scratch>/bundle1.zip <scratch>/unpacked`, rc 0. Tại gốc gói giải nén, `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` rc 0, `ok=true`, 187/187 và package hash khớp. Nguồn neo của gói là SHA-256 ZIP ở bảng trên.

## Không đo được

- `not_run` — Claude/Anthropic thật, `claude auth status` thật, billing, corpus LIVE, nguồn Google Doc thật, toàn bộ launcher suite, GitHub và CI từ xa.
- `not_measured` — Windows/Cowork, race filesystem, thu hồi cây tiến trình nhiều cấp, model/effort phục vụ thực tế, revision/spec hash/generation chính thức, danh tính Executor qua receipt độc lập và head PR từ xa. Lần đọc cuối `run.json` vẫn là `dang_chay`, mã thoát con chưa có. Verdict này là bằng chứng review cục bộ trên exact SHA đã giao.
- `skipped` — Core và t162 có 0 ca bỏ qua.
- `not_measured` — Phép kiểm bảng hook báo 35 cờ help chưa đo được ngoài 425 cờ đã xác nhận.

Đọc lại checkout cuối phiên cho đúng HEAD và tree đầu tệp. Diff tracked của worktree và index đều rỗng ở hai mốc. Mỗi hash diff rỗng là `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Mục ignored `.codex/` giữ nguyên và rỗng trong phạm vi nhìn thấy. Tệp untracked duy nhất được thêm là `.review/VERDICT.md`. Kết luận sạch giới hạn ở hai ảnh chụp cục bộ.

T1 còn P1 vì có thể ghi kết quả thiếu một khoản dưới trạng thái `ok=true`.

VERDICT: REQUEST_CHANGES
