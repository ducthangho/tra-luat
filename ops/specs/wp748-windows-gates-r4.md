# WP748 r4 — đo đủ gate Windows trên candidate g3

## Authority và mỏ neo

- Packet/Mission: #748. Chủ kho chỉ thị trong phiên Codex ngày 2026-10-14: “Đồng ý, cấp lease rồi đo lại các gate còn thiếu”; trước đó chỉ thị tiếp tục với `agy` và model đang sử dụng. Dispatcher phải ghi nguồn chỉ thị bền lên Issue #748 trước khi phát hành lease. Đây chỉ là quyền Executor/gate, không phải quyền merge, land hay LIVE.
- Revision 4, generation 4. Lease r3/g3 `wp748-r3-g3-antigravity-windows-20261014` hết hạn 2026-10-14T10:17:53Z. Candidate local g3 sạch tại `397fc2a10c8391e530c5ed8230812422b1d39eff`, tree `7e02ba671f8f135ed4bc23eb5d9039adc66d5012`, chưa push/PR; remote g3 vẫn ở `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`. Đây là nguồn mã cho g4, phải kiểm OID/tree rồi mới tạo branch/worktree g4. Không coi gate g3 là gate exact head g4 nếu head đổi.
- Immutable acceptance baseline của WP748 là master `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`, tree `eacec93c64bd96926ba26fa6ef6b980f686dd483`. Branch Executor `agent/wp748-g4-antigravity` bắt đầu tại candidate `397fc2a10c8391e530c5ed8230812422b1d39eff`; target PR `mission/748/integration`. G3 được đánh dấu `da_bi_thay_the` và g4 `thay_the_cho` hai chiều. Không sửa branch WP744/#747, #671/#690, #698, #700 hay g3.
- Nguồn lỗi ban đầu, ranh giới kỹ thuật và các ca phản chứng nằm tại `ops/specs/wp748-windows-gates-r3.md` commit `1e3454dd6f52cbfe503bb8370823766d1049b756`, SHA256 `04a4f9048c3abc566ada28ed5601041aba6668bdbbd20ba8489914e0a412fa18`. R4 chỉ thay mỏ neo, thế hệ và yêu cầu đo lại; không giảm acceptance của r3.

## Objective và effective write set

Đo đầy đủ những gate còn thiếu trên Windows native và Linux, khép ba lớp G5, lease và registry của r3 trên một exact candidate. Nếu lỗi nằm trong chín đường dưới đây, Antigravity có thể sửa và đo lại toàn bộ gate bị ảnh hưởng; nếu cần đường khác hoặc đổi nghĩa phép thử, dừng để xin revision. Không tăng timeout, hạ mẫu số mutant, bỏ ca hoặc đổi `continue-on-error` để qua gate.

1. `ops/bash_nen.py`
2. `ops/cong_cu_test.py`
3. `ops/lease_publish_test.py`
4. `.claude/dev/ci_dang_ky_test.py`
5. `ops/nhanh_don_duoc_test.py`
6. `.github/workflows/ci.yml`
7. `.github/workflows/ci-dot-bien-du.yml`
8. `ops/ci_duong_nhanh_test.py`
9. `.claude/dev/doc_receipt_thu_hoi_test.py`

Đây là effective write set đóng. Metadata spec/lease nằm trên branch điều phối, ngoài branch Executor. Không sửa `ops/lease_publish.py`, `.claude/hooks/subagent_ghi_detect_test.py`, CI ruleset, manifest/golden/changelog, credential hoặc LIVE. Review class/risk: **sensitive**. Executor: Google Antigravity, Windows native, model `gemini-3.8-flash-high` nếu CLI tiếp tục hỗ trợ, provider `google_antigravity`, surface `antigravity`, transport `machine/local`. Khai model thực từ log. Reviewer: Codex/OpenAI trong **phiên mới độc lập**, checkout exact head read-only; review Spec và Standards/Security, không quá hai lượt trên PR. AG không tự review/approve/merge/land.

## Acceptance và bằng chứng

1. Trước ghi: remote refs/base, spec hash/commit, lease và hạn, write set, provider/surface, holder scan cả chín đường = 0 trước cấp và đúng một g4 sau cấp; worktree g4 sạch ở start SHA. Chạy `lease_publish.py check` và `kiem-github` rc0 trước bản chiếu tự động; đối chiếu ID/body comment.
2. Windows native exact head: ca symlink của `ops/ci_duong_nhanh_test.py` đạt 10/10 **và full suite** đạt N/N với mutant denominator giữ nguyên; phép thử đơn lẻ không thay full suite. G5 `CONG_CU_TEST_BAN_KINH=manh` full suite N/N, lease-publish full suite N/N, doc receipt 156/156 và 162/162 mutant. Các ca đỏ gốc t23/t49/t217 và M1s9 xanh đúng lý do; ca phản chứng trên bản sao tạm đỏ. Không tăng skipped/not_measured.
3. Registry Windows full suite kết thúc dưới trần 105 phút với positive marker, đúng số ca, log thời gian từng bộ; `subagent_ghi_detect_test.py` không bị cancelled/time-out. Nếu full suite chỉ chạy light mode thì ghi `not_measured`, không khai pass. Linux regressions của các suite liên quan xanh.
4. `python scripts/tl.py --selftest` full N/N, rc0 và marker dương trên exact head. `git diff --check` rc0; `scripts/pkg_secret_scan.py` trên bản sao đúng write set rc0; ruff F delta 0 so immutable baseline theo tập `(code,message)`. Ghi riêng passed, failed, skipped, not_run, not_measured và artifact hash.
5. Chỉ sau local gates/handoff sạch mới push branch g4 và mở **draft PR** vào `mission/748/integration`. Full CI matrix trên exact candidate: mọi required check success, Windows và Ubuntu full selftest artifact JSON + output SHA256 khớp head/tree; registry Windows không cancelled/time-out; G5 và gate-ops Windows success. CI trên SHA khác không tính.
6. Codex cross-review exact SHA 0 P1/P2, có verdict/identity/evidence URL. Handoff ghi exact head/tree, command+rc, positive marker, artifact hashes, model/provider/surface/transport, giới hạn phép đo. Không suy quyền land từ CI/review; land cần quyền riêng trên exact SHA.

## Stop conditions

Thiếu/stale lease, drift base/ref, holder chồng, provider/surface khác khai, cần ghi ngoài chín tệp, test đổi nghĩa, positive evidence thiếu hoặc cùng finding lặp tới trần protocol ⇒ dừng. Lease hết hạn giữa chừng ⇒ ngừng ghi và báo; không force-push. Không dùng credential thật, merge, land hoặc LIVE.
