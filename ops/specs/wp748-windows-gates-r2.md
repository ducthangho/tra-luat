# WP748 r2 — khôi phục gate Windows của full matrix

## Authority và mỏ neo

- Packet/Mission Issue: #748. Chỉ thị chủ kho trong phiên Codex ngày 2026-10-13: “Cấp lease và packet mới để sửa các lỗi gate Windows”, sau đó “Đồng ý” với revision kế nhiệm khi r1/g1 gặp stop condition; quyết định được ghi hộ tại issue comment 6139285921. Đây là authority r2/g2, không phải quyền land.
- Nguồn đo: run `38322344390` trên PR #747 head `fffd14f4546f5eb44b3fe1138bc49c9703c7ed97`, tree `72785c6c1e884bc0b5c1771df644622d590223b4`. Run hoàn tất `failure` lúc 2026-10-13T01:14:14Z.
- Immutable acceptance baseline và start SHA: canonical master `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`, tree `eacec93c64bd96926ba26fa6ef6b980f686dd483`. Lệch base trước khi bắt đầu ⇒ dừng và xin revision mới.
- Revision 2, generation 2. Branch Executor `agent/wp748-g2-antigravity`; target PR `mission/748/integration` do dispatcher dựng từ đúng base. r1/g1 dừng sạch ở base vì thiếu một test trong write set; lease cũ được đánh dấu `da_bi_thay_the` trên `ops/wp748-r1-g1-lease` và lease g2 phải ghi `thay_the_cho` đúng ID cũ. Không sửa nhánh WP744/#747, #671/#690, #698 hoặc #700.

## Objective

Đóng theo lớp ba cổng Windows đỏ của run nguồn, giữ nguyên các biên an toàn và có bằng chứng dương từ Windows thật. Đây là một Packet vì full matrix chỉ trở lại xanh khi cả ba lớp cùng đóng trên một exact candidate; Executor phải hoàn thành đủ trong write set. Nếu chẩn đoán đòi đường dẫn khác, dừng và tạo revision/generation mới; không âm thầm mở rộng.

1. **G5:** `gate (windows-latest)` và 8 shard `gate-cong-cu` đỏ ở `ops/cong_cu_test.py`: 52/54 đạt, 2 failed (`t23_batch_chiu_duoc_stdout_CRLF_cua_python_windows`, `t49_duong_XAU_ra_JSON_HOP_LE_va_NGAY_GO_phai_duoc_DOC`), 2 skipped. Đo riêng cảnh báo `SyntaxWarning: invalid escape sequence '\('` từ `ops/bash_nen.py:900`, việc đọc CRLF và đường Unicode thường/byte xấu. Giữ nguyên ý nghĩa ca test và mutant; không skip hoặc sửa điều kiện để lấy xanh. Draft PR #690 có bản thử cũ, chỉ dùng làm hint sau khi đối chiếu base và chạy phản chứng.
2. **Lease gate:** `gate-ops (windows-latest)` đỏ ở `ops/lease_publish_test.py:t217_a9_object_store_thieu_blob_la_2`: `PermissionError [WinError 5]` khi unlink Git object. Phân biệt object read-only của Git for Windows với lỗi sản phẩm. Trong revision này chỉ được sửa test/harness; nếu chứng minh `ops/lease_publish.py` phải đổi thì dừng và xin revision. Bảo toàn kiểm object-store, ancestry, OID và fail-closed; không biến ca thiếu blob thành skipped.
3. **Registry:** `gate-registry (windows-latest)` bị GitHub hủy khi chạm trần job 105 phút ở bước `test registry (phạm vi + các bộ chưa được nối)` (23:30:20Z→01:14:07Z); verdict toàn suite là **not_measured**, nhưng log trước hủy có hai bằng chứng riêng. `.claude/dev/doc_receipt_thu_hoi_test.py` **failed rc=1**: 156/156 ca nền, 161/162 mutant bị giết; mutant M1s9 dùng `os.posix_spawn` trên Windows. Dispatcher tái hiện trên Windows native cùng base/PyYAML: Python rc=1, 161/162; Ubuntu run nguồn đạt 162/162 rc=0. Sửa test/mutant của bộ này để giữ ràng buộc không spawn trên cả hai nền, không bỏ mutant hay hạ denominator. `.claude/hooks/subagent_ghi_detect_test.py` còn chạy khi job bị hủy; cleanup thư mục tạm thất bại do hủy, không suy verdict của bộ. Đọc log/đo thời gian từng bộ, xác định phần làm chậm rồi giảm thời gian bằng phân chia hoặc thuật toán trong write set. Chỉ nâng timeout, tắt test, hạ số ca/đột biến hoặc đổi `continue-on-error` không đáp ứng. Mọi thay đổi workflow phải giữ classifier, catalog và `ci-dot-bien-du` đồng bộ, với ca phản chứng cho cấu hình lệch.

## Effective write set đóng

Chỉ chín tệp sản phẩm/test sau; không có companion ngoài tập này trong r2:

1. `ops/bash_nen.py`
2. `ops/cong_cu_test.py`
3. `ops/lease_publish_test.py`
4. `.claude/dev/ci_dang_ky_test.py`
5. `ops/nhanh_don_duoc_test.py`
6. `.github/workflows/ci.yml`
7. `.github/workflows/ci-dot-bien-du.yml`
8. `ops/ci_duong_nhanh_test.py`
9. `.claude/dev/doc_receipt_thu_hoi_test.py`

Spec và lease là metadata điều phối trên nhánh `ops/wp748-r2-g2-lease`, ngoài nhánh Executor. Không sửa `ops/lease_publish.py`, `.claude/hooks/subagent_ghi_detect_test.py`, CI ruleset, release manifest/golden/changelog, runtime khác, credential, Drive hoặc LIVE. Nếu phép đo chứng minh cần sửa bộ subagent hoặc closure/classifier yêu cầu thêm tệp, dừng và xin revision. Giữ `git diff --check` sạch, ruff F delta = 0 theo tập `(code,message)` so immutable baseline.

## Vai trò và rủi ro

- `risk`, `review_class`, `effective_review_class`: **sensitive** do chạm CI/gate và phép kiểm lease.
- Executor: Google Antigravity trên Windows native, provider `google_antigravity`, model family Gemini, execution surface `antigravity`, transport `machine/local`. Khai model thực từ log lượt chạy; không suy từ model yêu cầu.
- Reviewer: Codex/OpenAI, session mới độc lập và checkout exact head read-only; review hai trục Spec và Standards/Security **theo lớp**, mỗi finding có hint patch/test/đột biến/rủi ro sinh mới. Không quá hai lượt Codex cho PR; chưa đạt thì checkpoint.
- Executor không tự review, approve, merge, land, deploy hoặc dùng credential thật. Land cần quyền riêng trên exact SHA và cổng integration/canonical riêng.

## Acceptance và bằng chứng

1. Trước ghi: refs remote đủ và exact, lease r1/g1 được thay bằng bia mộ hai chiều, holder scan cả chín đường = đúng một lease r2/g2, spec SHA256/commit/lease/generation/base/write-set đúng, worktree Executor sạch; chạy `lease_publish.py check` và `kiem-github` rc0 trước khi đăng bản chiếu tự động (sau đó mã trùng comment phải đối chiếu ID/body). Nếu bất kỳ mục nào lệch ⇒ dừng.
2. Windows native: tái hiện ca đỏ trên baseline, rồi t23/t49/t217 xanh đúng lý do; phản chứng trên **bản sao tạm** làm từng ca đích đỏ. G5 full suite N/N, 0 failed, không tăng skipped hoặc not_measured do bản vá. Lease-publish full suite và các ca object-store liên quan xanh, không giảm lực kiểm.
3. Registry: `doc_receipt_thu_hoi_test.py` trên Windows đạt 156/156 và 162/162 mutant, M1s9 vẫn đỏ khi cố spawn; Linux giữ 162/162. Log định danh bộ chậm, elapsed từng bộ; full suite kết thúc trước trần bằng positive marker và đúng tập ca. Mutant đổi/bỏ cấu hình hoặc bỏ một mảnh phải đỏ. Đo trên Windows thật, không lấy ước lượng Linux làm pass Windows.
4. Linux regressions của các suite liên quan xanh; `python scripts/tl.py --selftest` N/N; `git diff --check` rc0; `python scripts/pkg_secret_scan.py` trên bản sao đúng write set rc0; ruff F delta 0 theo tập. Tách passed, failed, skipped, not_run, not_measured.
5. Sau local gate/handoff sạch mới push. Full CI matrix trên exact candidate: mọi required check success, Windows và Ubuntu full selftest artifact JSON+output SHA256 khớp head/tree; registry Windows không cancelled/time-out; G5 và gate-ops Windows success. PR mới trỏ mission integration, giữ draft tới khi review và land authority riêng. CI trên SHA khác không tính.
6. Codex cross-review exact SHA 0 P1/P2, có verdict/identity/evidence URL. Handoff ghi exact head/tree, command+rc, positive marker, artifact hashes, model/provider/surface/transport, giới hạn phép đo. Không khai runtime NLM audit/canary của WP744 đã đóng từ Packet này.

## Stop conditions

Thiếu/stale lease, drift base/ref, overlapping holder, mô hình/surface khác khai, cần ghi ngoài chín tệp, không tái hiện được ca gốc, test đổi nghĩa hoặc cùng finding lặp theo trần protocol ⇒ ngừng ghi và báo dispatcher. Registry chưa có nguyên nhân trong write set ⇒ successor Packet, không tăng timeout để qua cổng. Hạn lease hết giữa chừng ⇒ ngừng ghi; chỉ commit cục bộ và báo. Không force-push.
