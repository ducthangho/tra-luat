# WP748 r7 — Claude Opus 5.5 đo đầy đủ gate Windows với ngoại lệ socket t20zo được duyệt

## Authority và mỏ neo

- Packet/Mission: #748. Chủ kho đổi Executor sang Claude Opus 5.5 tại https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6167748332; ngày 2026-10-14 chấp thuận revision hẹp cho socket Windows trong chat Codex, ghi bền đúng phạm vi tại https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6171400658. Đây là quyền soạn Packet, cấp lease riêng và đo gate; không phải quyền merge, land hay LIVE.
- Revision 7, generation 7. R6/g6 `wp748-r6-g6-claude-windows-20261014` được đánh dấu `da_bi_thay_the: wp748-r7-g7-claude-windows-20261014` trên nhánh `ops/wp748-r6-g6-lease` commit `933defb32f50cfcf51c3d1efdf32e1da237715a3`. G6 chưa commit/push sản phẩm hoặc mở PR. Nguồn bản vá g6 là diff chưa commit đúng một tệp `ops/ci_duong_nhanh_test.py`, 11925 byte, SHA256 `8575738e7121ce7aecb1b6de26b40a72ab409971ce3ad5821f430a61c0eb625f`; file SHA256 `0360d6499142f8130c71b440c4a1cb86187e94fe4a03cfd8558ed4741ac6d6b4`. Bản sao patch immutable nằm ngoài repo tại `C:\Users\admin\.codex\visualizations\2026\10\13\01a137a1-af70-7002-a1a7-89cbed32d176\wp748-g6-diagnostic.patch`. Đây là nguồn mã được phép cho g7 sau khi kiểm lại hash; gate g6 không chuyển thành gate g7.
- Immutable acceptance baseline WP748 là master `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`, tree `eacec93c64bd96926ba26fa6ef6b980f686dd483`. Branch Executor `agent/wp748-g7-claude` bắt đầu tại `397fc2a10c8391e530c5ed8230812422b1d39eff`, tree `7e02ba671f8f135ed4bc23eb5d9039adc66d5012`, nhận diff nguồn g6 sau khi g6 dừng; target PR `mission/748/integration`. Clone độc lập có `.git` thư mục tại `D:\Quốc hội\tra-luat\work\wp748-g5-claude` đã được chủ kho trust; chuyển branch g6→g7 chỉ khi process g6 đã dừng và kiểm patch hash. Không sửa branch WP744/#747, #671/#690, #698, #700 hoặc các generation cũ.
- Nguồn lỗi và ranh giới kỹ thuật ở `ops/specs/wp748-windows-gates-r3.md` commit `1e3454dd6f52cbfe503bb8370823766d1049b756`, SHA256 `04a4f9048c3abc566ada28ed5601041aba6668bdbbd20ba8489914e0a412fa18`. R7 giữ acceptance r6/r5/r3/r4, trừ ngoại lệ socket Windows đúng phạm vi dưới đây.

## Objective và effective write set

Đo đầy đủ những gate còn thiếu trên Windows native và Linux, khép ba lớp G5, lease và registry của r3 trên một exact candidate. Nếu lỗi nằm trong chín đường dưới đây, Claude có thể sửa và đo lại toàn bộ gate bị ảnh hưởng; nếu cần đường khác hoặc đổi nghĩa phép thử ngoài ngoại lệ đã duyệt, dừng để xin revision. Không tăng timeout, hạ mẫu số mutant, bỏ ca hoặc đổi `continue-on-error` để qua gate.

1. `ops/bash_nen.py`
2. `ops/cong_cu_test.py`
3. `ops/lease_publish_test.py`
4. `.claude/dev/ci_dang_ky_test.py`
5. `ops/nhanh_don_duoc_test.py`
6. `.github/workflows/ci.yml`
7. `.github/workflows/ci-dot-bien-du.yml`
8. `ops/ci_duong_nhanh_test.py`
9. `.claude/dev/doc_receipt_thu_hoi_test.py`

Đây là effective write set đóng. Metadata spec/lease nằm trên branch điều phối, ngoài branch Executor. Không sửa `ops/lease_publish.py`, `.claude/hooks/subagent_ghi_detect_test.py`, CI ruleset, manifest/golden/changelog, credential hoặc LIVE. Review class/risk: **sensitive**. Executor: Claude Code trên Windows native, model `claude-opus-5-5`, provider `anthropic_claude`, surface `claude_code`, transport `machine/local`. CLI 2.1.299 từ gói npm chính thức đã probe `MODEL_OK`; dùng executable `C:\Users\admin\.local\bin\claude-2.1.299.exe` và khai model thực từ log. Workspace Executor phải là clone độc lập có `.git` là thư mục để qua `launcher run`; không dùng linked worktree g4. Reviewer: Codex/OpenAI trong **phiên mới độc lập**, checkout exact head read-only; review Spec và Standards/Security, không quá hai lượt trên PR. Claude Executor không tự review/approve/merge/land.

## Ngoại lệ socket Windows được chủ kho duyệt

- Chỉ trong nhánh `socket` của `t20zo_la_khong_phai_tep_thuong_do` trên Windows native: vì WinSock bind tạo đường đĩa mà `os.stat` báo `S_IFREG`, được dùng một named pipe thật để kiểm đường đi và mock `os.stat` có phạm vi đúng một leaf nhằm kiểm logic từ chối `S_IFSOCK`. Đây là phép đo **logic của bộ kiểm**, không phải bằng chứng đã tạo hay từ chối socket thật trên Windows.
- Trên Linux, `t20zo` phải tiếp tục dùng FIFO và AF_UNIX socket thật, không mock; full suite Linux phải đo lại. FIFO Windows phải giữ tiền đề `t82` VAP đúng lý do special file, không dựa vào cạn instance. Không bỏ ca, giảm mẫu số mutant, đổi matcher hoặc đổi hành vi sản phẩm để qua gate.
- Reviewer độc lập phải kiểm việc mock chỉ áp dụng cho đúng leaf/đúng nhánh Windows và không làm xanh giả các nhánh FIFO, symlink hay Linux; nếu không chứng minh được, verdict P1/P2 và dừng.

## Acceptance và bằng chứng

1. Trước ghi: remote refs/base, spec hash/commit, lease và hạn, write set, provider/surface, holder scan cả chín đường cho thấy g6 đã bị thay thế và đúng một g7 sau cấp; clone đúng start SHA, đúng một diff nguồn g6 trong write set với hash nêu trên. Chạy `lease_publish.py check` và `kiem-github` rc0 trước bản chiếu tự động; đối chiếu ID/body comment. Không tính bất kỳ gate g6 nào cho g7.
2. Windows native trên exact head g7: ca symlink của `ops/ci_duong_nhanh_test.py` đạt 10/10 **và full suite** N/N với mutant denominator giữ nguyên. Trong t20zo, FIFO Windows phải là named pipe thật và t82 phải VAP do loại tệp; nhánh socket Windows chỉ được khai là logic allow-list bằng mock `os.stat` cục bộ theo ngoại lệ dưới đây. Linux dùng FIFO/socket thật. G5 `CONG_CU_TEST_BAN_KINH=manh` full suite N/N, lease-publish full suite N/N, doc receipt 156/156 và 162/162 mutant. Các ca đỏ gốc t23/t49/t217 và M1s9 xanh đúng lý do; phản chứng bản sao tạm đỏ. Không tăng skipped/not_measured.
3. Registry Windows full suite kết thúc dưới trần 105 phút với positive marker, đúng số ca, log thời gian từng bộ; `subagent_ghi_detect_test.py` không bị cancelled/time-out. Nếu full suite chỉ chạy light mode thì ghi `not_measured`, không khai pass. Linux regressions của các suite liên quan xanh.
4. `python scripts/tl.py --selftest` full N/N, rc0 và marker dương trên exact head. `git diff --check` rc0; `scripts/pkg_secret_scan.py` trên bản sao đúng write set rc0; ruff F delta 0 so immutable baseline theo tập `(code,message)`. Ghi riêng passed, failed, skipped, not_run, not_measured và artifact hash.
5. Chỉ sau local gates/handoff sạch mới push branch g7 và mở **draft PR** vào `mission/748/integration`. Full CI matrix trên exact candidate: mọi required check success, Windows và Ubuntu full selftest artifact JSON + output SHA256 khớp head/tree; registry Windows không cancelled/time-out; G5 và gate-ops Windows success. CI trên SHA khác không tính.
6. Codex cross-review exact SHA 0 P1/P2, có verdict/identity/evidence URL. Handoff ghi exact head/tree, command+rc, positive marker, artifact hashes, model/provider/surface/transport, giới hạn phép đo. Không suy quyền land từ CI/review; land cần quyền riêng trên exact SHA.

## Stop conditions

Thiếu/stale lease, drift base/ref, holder chồng, provider/surface khác khai, cần ghi ngoài chín tệp, đổi nghĩa test ngoài ngoại lệ socket Windows được duyệt, positive evidence thiếu hoặc cùng finding lặp tới trần protocol ⇒ dừng. Lease hết hạn giữa chừng ⇒ ngừng ghi và báo; không force-push. Không dùng credential thật, merge, land hoặc LIVE.
