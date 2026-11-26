# Verdict PR #1503 lượt 8 — Codex

reviewed_sha: a93b8f3069cd845468545fa79c501a2a6a1782f0
reviewed_tree: 2f2487f4c735ec243e66aa469424eb1614b36b07
base_sha: a03a28ef076503c7fe93c208a4998c32590a977f
nang_tran: chủ kho nâng trần lên 8 (lời gọi thứ 8, cuối cùng)

## Đối chiếu lượt 7 (và các lớp còn mở)

Phép đo A/B dùng HEAD và commit lượt 7 `b5dc962aa77d9d56acacafda406f9aa1ab202c8d` (tree `8f8c1f38f95e164d918ef9c141e29444f9a00951`). Các lệnh chạy trên bản sao tạm trong `/tmp/pr1503-r8.ZmmDyD`. Các phép đo dưới đây có rc 0 ở hai mốc.

| # | Trạng thái | Bằng chứng |
|---|---|---|
| T1 | ĐÃ ĐÓNG ca gốc | `probe-structure.py`: dòng mất số sau dấu kép thẳng nằm trong trích dẫn cong đổi từ rc 0, `ok=true`, ghi đè tệp, sang rc 5, `ok=false`, giữ byte cũ. Đối chứng bỏ dòng mất số giữ rc 0. Ngoặc tròn trải dòng với dòng kế không thuộc hai dạng được phép đổi rc 0 → 5. |
| T2 | ĐÃ ĐÓNG ca EIO gốc trên Linux | `probe-runtime.py` tiêm EIO sau khi con Python đã tạo marker. Lượt 7 đọc hai lần, `waitid(WNOWAIT)` còn thấy con chết chưa được thu hồi và cả hai pipe mở. HEAD đọc một lần, `waitid` báo đã thu hồi, `returncode=-9`, cả hai pipe đóng. Hai mốc đều dừng với 0 lượt API giả. |
| `ranh-gioi-khoan` | CÒN MỞ và SINH LỖI MỚI · P1 | Nhận sai số khoản trong trích dẫn nhiều dòng còn ở hai mốc (U3). HEAD phát sinh cắt sai từ nối trong trích dẫn lồng cùng kiểu dấu trên một dòng (U1). Phép đóng lớp phải từ chối ranh giới mơ hồ và vẫn giữ các đối chứng cấu trúc hợp lệ. |
| `thu-hoi-tien-trinh-sub` | SINH LỖI MỚI · P2 | Đã thu hồi được con trực tiếp sau EIO và timeout thông thường trên Linux. Phép đo dùng cơ chế đọc có luồng của CPython cho thấy `close()` có thể chờ EOF trước khi tới `wait(timeout=5)` (U2). Cần chạy ca giữ đầu ghi trên Windows để đóng lớp. |

## Findings mới

### U1 [P1] Dấu đóng của trích dẫn lồng làm bộ kiểm nhận nhầm từ nối trong trích dẫn — scripts/tl_core/llm_route.py:531–549,563–569

Lớp `ranh-gioi-khoan`. Một thuật ngữ trên **một dòng** chứa đoạn trích kép cong, trong đó có một cụm con cũng dùng cặp kép cong. Cả cụm con và đoạn trích ngoài đều có dấu đóng. Có chữ “là” sau dấu đóng của cụm con, vẫn nằm trong đoạn trích ngoài, rồi mới đến từ nối thật của khoản. `_quet` khép trạng thái tại dấu đóng đầu tiên. `_tu_noi` chọn chữ “là” bên trong đoạn trích. Hai trường sau khi cắt vẫn chứa đủ chữ của nguồn, nên phép so trọn khoản xác nhận nhầm ranh giới.

Bằng chứng A/B bằng `run-check {head,prior} structure-{head,prior} python <scratch>/probe-structure.py`, dùng handler thật, nguồn văn bản giả và model giả. Trên HEAD, cả nguồn có số và nguồn mất số đều nhận kết quả bị cắt sai với `lech=[]`, rc 0, `ok=true`, và ghi đè `--out`. Kết quả cắt đúng nhận `lech=[1]`, rc 5, `ok=false`, và giữ tệp cũ. Trên lượt 7, hai kết quả đảo lại ở cả hai dạng nguồn. Đối chứng dùng kiểu dấu khác cho trích dẫn bên trong vẫn nhận đúng và từ chối kết quả cắt sai trên cả hai mốc.

Đề xuất xử lý tại bộ quét chọn từ nối trong một khoản. Giữ mô hình một cụm đang mở và trả trạng thái mơ hồ khi gặp dấu mở kép cong cùng loại trong cụm đó. Truyền trạng thái mơ hồ tới phép kiểm khoản để từ chối cả hai cách cắt trong trường hợp này. Khóa bằng hai dạng nguồn đã đo, đòi rc 5 và giữ byte đích khi model trả cách cắt sai. Giữ các đối chứng cho cặp cong chứa dấu kép thẳng và trích dẫn dùng hai kiểu dấu. Đột biến bỏ chốt mơ hồ phải làm ca cắt sai đỏ. Cách vá bảo thủ có thể chặn một thuật ngữ dùng ký tự mở cong như nội dung theo quy ước riêng. Phân tích trích dẫn lồng đầy đủ có thể nhận thêm nguồn hợp lệ và cần tiêu chí riêng.

### U2 [P2] Đóng pipe có luồng đọc đang chờ có thể giữ runner trước lệnh `wait` — scripts/tl_core/llm_route.py:104–109

Lớp `thu-hoi-tien-trinh-sub`. Nhánh Windows của CPython dùng luồng nền gọi `fh.read()` trên mỗi pipe. Sau timeout, runner giết con trực tiếp rồi gọi `close()` trên cùng đối tượng đọc. Nếu một bên khác vẫn giữ đầu ghi, luồng đọc có thể giữ khóa của bộ đệm và lời gọi `close()` chờ khóa. Giới hạn năm giây nằm sau lời gọi này.

`run-check {head,prior} threaded-{head,prior} python <scratch>/probe-threaded-pipes.py` dùng nguyên các hàm đọc và chờ luồng của nhánh Windows trong thư viện chuẩn CPython 3.13.18, với pipe và tiến trình con thật trên Linux. Đầu ghi phụ được đóng sau 6 giây. Cả hai phép đo rc 0. HEAD mới trả timeout ở 6,001 giây, sau khi đầu ghi phụ đã đóng, rồi thu hồi con với `returncode=-9`. Lượt 7 trả timeout ở 5,102 giây khi đầu ghi phụ còn mở, con chưa được thu hồi. Cùng thiết lập, đối chứng HEAD với `communicate` bản địa Linux và bản tạm chỉ bỏ đoạn đóng pipe khi dùng cách đọc có luồng đều trả timeout ở 0,103 giây, khi đầu ghi phụ còn mở và con đã được thu hồi. Hai phép `probe-threaded-controls.py native|skip_close` rc 0. Bản bỏ đóng pipe dùng để định vị điểm chờ. Windows bản địa còn thiếu phép đo.

Đề xuất tại `_chay_co_moc`: dùng đường thu stdout/stderr trên Windows không cần đóng đồng bộ một pipe có luồng đọc đang chờ, ví dụ chuyển hướng sang tệp tạm và chỉ đọc sau khi tiến trình kết thúc thành công. Giữ đợi thu hồi có hạn và giữ ngoại lệ ban đầu. Thêm ca Windows giữ đầu ghi qua timeout, đòi runner trả trong hạn và con trực tiếp được thu hồi. Đột biến phục hồi đóng pipe đồng bộ phải làm ca vượt hạn. Nếu dùng tệp tạm, cần đo phần đĩa phát sinh khi output lớn, dọn tệp khi còn handle và tính đầy đủ của output thành công.

### U3 [P1] Số thứ tự trong trích dẫn nhiều dòng bị nhận là số khoản — scripts/tl_core/llm_route.py:498–506,522–524,563–569

Lớp `ranh-gioi-khoan`. Biểu hiện đã có ở lượt 7 và còn mở trên HEAD. Khoản duy nhất chứa trích dẫn hai dòng gồm hai mục đánh số. Số thứ nhất của đoạn trích nằm giữa dòng khoản. Số thứ hai của đoạn trích nằm đầu dòng kế và tình cờ nối tiếp số khoản thật. `tach_khoan` nhận dấu số ấy ngay trước khi xử lý các dòng tiếp. Mỗi phần vẫn có một từ “là”, nên bộ kiểm chấp nhận hai mục, cắt mất dấu số nằm trong nguyên văn định nghĩa và chia một khoản thành hai.

`run-check {head,prior} numbering-{head,prior} python <scratch>/probe-numbering-in-quote.py` đo handler thật với model giả. Trên cả hai mốc, kết quả hai mục sai có `lech=[]`, rc 0, `ok=true`, đè tệp cũ. Kết quả một mục giữ đủ đoạn trích nhận `lech=[1,2]`, rc 5 và giữ tệp. Đổi cặp dấu trích dẫn thành cặp ngoặc tròn giữ nguyên cả hai kết quả trên hai mốc. Hai đối chứng bổ sung trong `probe-structure.py` cho thấy HEAD cũng nhận trích dẫn nhiều dòng khi dòng hai mở bằng “là” hoặc là dòng điểm. Văn bản của hai đối chứng ấy được giữ đủ, còn ca mang số đầu dòng làm sai số lượng và nội dung khoản.

Đề xuất tại `tach_khoan`: kiểm tra mơ hồ về dấu phân cách qua ranh giới dòng trước khi nhận số khoản hoặc một dòng tiếp được phép. Dùng trạng thái này để từ chối nguồn có dấu mở qua dòng theo giới hạn đã chốt. Khóa ca có số trong đoạn trích bằng rc 5, giữ byte tệp đích và kiểm cả hai hình dạng tiếp dòng đã đo. Đột biến bỏ kiểm ở dòng có số phải làm ca tách nhầm đỏ. Giữ đối chứng dấu ngoặc tròn được trích như ký tự, điểm hợp lệ và xuống dòng trước từ nối thật. Bộ kiểm quá rộng có thể chặn oan các ký hiệu được trích hoặc dấu lẻ có nghĩa trong một dòng.

## Đã kiểm mà không thấy lỗi

- `probe-runtime.py` chạy tiến trình Python thật thay CLI. Auth first-party hợp lệ giữ đường `sub`. Auth API-key, auth timeout, lỗi tạo thư mục tạm và lỗi spawn thật đều đến API giả đúng một lần, marker model chưa tồn tại. Sau marker, timeout, EIO, hết hạn mức và mất envelope đều dừng với 0 lượt API giả. Lỗi dọn thư mục model theo chế độ bỏ qua lỗi giữ kết quả `sub`. Các probe chạy trên HEAD và lượt 7, rc 0.
- `probe-structure.py` đo đối chứng đúng qua handler. Trích dẫn cong chứa dấu kép thẳng, dòng “là” tiếp một thuật ngữ chưa có từ nối, dòng điểm hợp lệ và nguồn mất số với một khoản mỗi dòng đều rc 0, `ok=true`, và ghi hai mục trên cả hai mốc.

### Đột biến trên bản sao tạm

`run-check head mutants python <scratch>/probe-mutants.py`, rc 0, stdout SHA-256 `cca8b99369b5330a3576766f3a5b7a737a12bce7551826bf24b17ad032e238f5`. Cả hai ca đích nguyên trạng đều xanh. Tám đột biến làm đỏ đúng assertion.

| Đột biến | Dấu hiệu ca đích đỏ |
|---|---|
| Nối dòng “là” cả ở nguồn mất số | Dòng gãy bị nhận thay vì chặn. |
| Nối dòng “là” sau khoản đã có từ nối | Dòng bị gộp vào khoản trước. |
| Bỏ lần lượt bộ nhận dấu kép thẳng và cong | Cách cắt sai bên trong trích dẫn được nhận trong từng biến thể. |
| Dấu đóng khác loại cũng kết thúc trích dẫn | Đối chứng kép thẳng trong kép cong bị chặn oan. |
| Dấu ngoặc tròn đóng trong trích dẫn vẫn đổi độ sâu | Cách cắt đúng bị chặn. |
| Hồi phục tiếp dòng theo dấu còn mở và giữ bộ quét mới | Ngoặc tròn qua dòng lại được nối. |
| Bỏ `wait` sau EIO | `returncode=None`, con chưa được thu hồi. |

Hai đột biến bỏ đóng pipe và bỏ riêng tham số timeout của `wait` vẫn qua ca stock T2. Phép kiểm bổ sung với tiến trình giả bắt được cả hai và xác nhận thứ tự HEAD là đọc một lần, kill, đóng stdout/stderr, `wait(timeout=5)`, rồi trả lại EIO gốc. Suite báo 71 mục đột biến, trong đó có 70 ID khác nhau do `bo_hai_ve_khac_rong` lặp hai lần.

### Gate cục bộ trên HEAD

| Lệnh | Trạng thái | Bằng chứng dương |
|---|---|---|
| `python scripts/tl_core/llm_route_test.py` | `passed`, rc 0 | 47/47 ca, 71/71 mục đột biến. |
| `python .claude/dev/launcher_test.py --lap-ca t162 --lan 1` | `passed`, rc 0 | 1/1, 0 bỏ qua, 0 hỏng. |
| `python .claude/hooks/pretooluse_guard.py --kiem-bang` | `passed`, rc 0 | 108 writer, 93 lệnh đọc, help 26/26 chương trình, 425 cờ xác nhận. |
| `python scripts/tl_core/command_registry_test.py` | `passed`, rc 0 | 10 test, `OK`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed`, rc 0 | `ok=true`, 26 cards, 0 lỗi, 0 cảnh báo. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed`, rc 0 | `ok=true`, 20/20. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed`, rc 0 | `ok=true`, 187/187, package hash khớp `e4aaa8e697ff4c815f1e2bedb45335913daafb423be69b4db242cd51374808e1`. |

### Neo review và môi trường

- Checkout độc lập, detached, remote cục bộ nhận diện đúng `ducthangho/tra-luat`. Base được giao là cha thứ hai của HEAD và `git merge-base HEAD <base_sha>` trả đúng base. Ref `origin/master` lưu trong bản sao còn ở `5259239d763c9ffc1677f033bd9a9cf23ede9299`. Phép đo dùng exact base trong prompt. Hai tệp launcher thay đổi giữa bản vá và HEAD là phần ghép master đã nêu trong prompt.
- Chỉ thị điều phối là prompt lượt 8 do người dùng giao, dẫn quyết định nâng trần ở comment PR 7134926594. SHA-256 prompt `141c504f54d272402f009f79e2c4a9a74fcd6959d0ca13643d2df0e4dd9872ea` khớp cả checkpoint và run, cùng neo exact HEAD. SHA-256 của checkpoint `8acfb7c85caf2382d687c1292d704bdf3dbd29685870686337e11a6ca4a7b78c` khớp run. Phạm vi ghi là `.review/VERDICT.md` và bản sao tạm bên ngoài checkout. Review Class theo phạm vi thực tế là `sensitive` vì cả PR đi qua launcher và xác thực. Đã kiểm hai trục đặc tả và standards/security.
- `provider=openai_codex`, `execution_surface=codex_cli`, `transport=machine`, `run_id=6bc0aefdd1084c30b6bc208e311e501f` theo hồ sơ run hiện hành. Linux x86_64, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, Bash, sandbox `workspace-write`. Các phép chạy dùng bản sao detached, `core.abbrev=7`, HOME/cache/tmp và môi trường tối giản riêng, Git transport file, proxy loopback và stub CLI ngoài. Mỗi lệnh có exact SHA/tree, argv, rc và SHA-256 stdout/stderr tại `/tmp/pr1503-r8.ZmmDyD/logs/`.
- SHA-256 diff toàn PR `8eb70ecc09e052343cc3d3efcf00bfb13f2492d600d5f4c990e428f47034b4e2`. SHA-256 diff `b5dc962..fcd8e08` là `1e421c61ea7f25eab51a840eecacff217b105c5eaf59748fe0f054b49c6f1bab`. `git diff --check a03a28e a93b8f3` rc 2 vì ba dòng Markdown có hai khoảng trắng cuối dòng trong hồ sơ lượt 6. `git diff --check b5dc962 fcd8e08` rc 0. Phép kiểm toàn PR với `core.whitespace=-blank-at-eol` rc 0.

### Full selftest đối chiếu base

Chạy `python scripts/tl.py --selftest` tuần tự với cùng cấu hình cô lập.

| Mốc | Trạng thái | Bằng chứng |
|---|---|---|
| HEAD `a93b8f3069cd845468545fa79c501a2a6a1782f0` | `failed`, rc 1 | 1775/1789. Cả ba ca `r380_*` đạt. SHA-256 stdout `fd0ebd9e88a8b22294b784812bc006940eb928362548f1eb29979e7bb86437e0`. |
| Base `a03a28ef076503c7fe93c208a4998c32590a977f`, tree `1c3dfd0b5363745cb27ca976cb37ae865aeb2ebe` | `failed`, rc 1 | 1772/1786. SHA-256 stdout `1876f2eb29975b47932412443188fa6a6c4112a95c3c8aeec32d8866c78db8cf`. |

Đối chiếu đa tập ID `[FAIL]` cho đúng 14 ca chung, 0 ca mới đỏ và 0 ca hết đỏ. Tập chung gồm tám ca `r973_bootstrap_*`, năm ca `wp433_*` và `wp727_tl_gws_refresh`. Full selftest vẫn có trạng thái `failed` trên hai mốc trong môi trường cô lập này.

## Không đo được

- `not_run` — Claude/Anthropic thật, `claude auth status` thật, corpus LIVE, billing, GitHub, CI từ xa và toàn bộ launcher suite.
- `not_measured` — Windows/Cowork bản địa, thu hồi cây tiến trình nhiều cấp, model/effort thực tế của reviewer, danh tính Executor qua receipt độc lập, revision/spec hash/generation chính thức và trạng thái PR từ xa. Hồ sơ run tại lúc đọc cuối vẫn đang chạy và chưa có mã thoát terminal. Đây là verdict review cục bộ neo vào SHA được giao.
- `not_measured` — 35 cờ help ngoài 425 cờ đã xác nhận trong phép kiểm bảng hook.
- `skipped` — ca t162 có 0 ca bỏ qua. Core tổng kết 47/47 ca.

Đọc lại cuối phiên xác nhận đúng HEAD/tree, diff tracked và index đều rỗng, mỗi SHA-256 diff là `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Thư mục ignored `.codex/` rỗng ở cả hai mốc trong phạm vi quan sát. Tệp untracked duy nhất được thêm là `.review/VERDICT.md`. Phép so chỉ chứng minh trạng thái tại hai thời điểm chụp.

Hai lớp có ba biểu hiện còn mở. U1 là hồi quy P1 của bản vá, U3 là biểu hiện P1 còn tồn tại và U2 là P2 cần đo thêm trên Windows. Cả hai P1 đều có thể ghi kết quả sai vào `--out` dưới trạng thái `ok=true`.

VERDICT: REQUEST_CHANGES
