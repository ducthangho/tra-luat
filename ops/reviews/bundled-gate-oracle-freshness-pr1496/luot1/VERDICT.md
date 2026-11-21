---
verdict: changes_requested
reviewed_sha: 4f648e5b784aa4e19f0385eee68cd75e69e1dd18
tree: 33f7b4183f408dafc029ecf860aab9857f244365
packet: BUNDLED-GATE-ORACLE-FRESHNESS
lease: wp433-r11-g1-claude
review_class: sensitive
provider: openai_codex
execution_surface: codex_cli
transport: machine
---

Rà soát độc lập PR #1496 trên `4f648e5` và continuation base `e2f28fb`, ngày 21-11-2026 UTC. **Kết luận yêu cầu bổ sung bằng chứng A4.** A0–A3, A5 và A6 đạt. A4 đỏ cùng các ca ở hai mốc do môi trường sandbox. A6 và 13 phép thử bổ sung ghi nhận 0 hồi quy từ base sang C. Bốn ca ngoài ma trận cùng sống được ghi P3 theo Q7.

Môi trường Linux x86_64, Python 3.13.18 và Git 2.43.0. `kho/` là checkout giao để review, còn clone, thư mục tạm và log ở `rv/`.

## Phép đo

| Lệnh | RC | Giờ UTC | Kết quả |
|---|---:|---|---|
| `python3 -B rv/preflight.py` | 0 | 19:01:19 | HEAD và tree đúng, detached, clone đầy đủ và có object `358451e8`. Baseline bất biến là tổ tiên của base, base là tổ tiên của C. Các cây runtime khớp giữa hai baseline. |
| `git -C kho show 5bd8463e9:ops/specs/BUNDLED-GATE-ORACLE-FRESHNESS-r5.md \| sha256sum` | 0 | 19:00:30 | `5ae3d269551dd6791aafc33e0c498bda7103fef28e85bf6a79cb4ed4d5f26159`, khớp lease r11/g1, lớp `sensitive`. |
| `python3 -B rv/preflight.py` (hiện vật, write set, W1) | 0 | 19:01:19 | 11 băm khớp README theo độ dài công bố (7 băm đầy đủ, 4 tiền tố 8 hex). Diff khớp lease: 3 tệp, +54/−26, W3 giữ nguyên. Commit cuối chỉ đổi manifest. `va.py` áp 11 thay thế, W1 trùng byte với C. |
| `git -C kho diff --binary e2f28fb HEAD \| cmp - diff.patch` | 0 | 19:01:19 | Diff khớp snapshot. |
| `bash rv/run-matrices.sh` (dựng hai clone trong cùng lần gọi) | 0 ở bước dựng | 19:01:49–19:01:56 | `rv/nen` = `e2f28fb`, tree `242907967208889bed9e2f29459eac9c838bcf27`; `rv/sau` = `4f648e5`, tree `33f7b4183f408dafc029ecf860aab9857f244365`. Cả hai detached, `shallow=false`, có object `358451e8`, `core.abbrev=7`, không hardlink. |
| `python3 -u -B rv/spec/ma_tran_r11.py rv/nen` | 1 (dự kiến) | 19:01:56–19:24:28 | `DON_DICH: 32/32`, `TONG: 125 dot bien + doi chung, sai=55`. A0 khớp đủ năm ca. [Log](rv/log/matrix-nen.out) |
| `python3 -u -B rv/spec/ma_tran_r11.py rv/sau` | 0 | 19:01:56–19:27:24 | A1 `DAT doi_chung run=True so_nhan=32 do= dich=`. A2 `DON_DICH: 32/32`, `TONG: 125 dot bien + doi chung, sai=0`. A3 20/20 ca `a7_`; 13/13 ca nợ `no_` đúng đích rỗng. [Log](rv/log/matrix-sau.out) |
| `python3 -B rv/spec/doi_chieu_don_dieu.py rv/log/matrix-nen.out rv/log/matrix-sau.out` | 0 | 19:27:24 | A6 `DON_DIEU: base giet 72 ca do duoc; C yeu di 0; C thieu 0`. [Log](rv/log/a6.out) |
| `bash rv/check-snapshot.sh \| cmp - rv/log/final-snapshot.out` | 0 | 19:27:27–19:28 | Sau A6, snapshot HEAD/tree, diff/index, trạng thái tệp và băm W1–W4 trùng snapshot sau tái sinh. |

A0 trên base đã cho `do=` rỗng ở `r11_size_only`, `r11_one_stale_ok`, `r11_missing_ok_narrow`. `r11_ann_empty` cho V4,V5,V6,V8,V9 và `r11_duplicate` cho V4,V5,V6,V8. [Đầu ra ma trận nền](rv/log/matrix-nen.out)

## Cổng cục bộ A4/A5

Lượt đầu trên base dùng cấu hình Git kế thừa và cho selftest `1770/1786` (rc 1, 19:02:35–19:07:35Z) cùng bundle checker `ok=false`, 6 fragment đỏ trong 20 ca (rc 1, 19:07:36–19:08:49Z). `commit.gpgsign=true` làm ca tạo mini-repo gọi trình ký. Phép dò commit trống xác nhận trình ký thử mở socket loopback và sandbox chặn. Đã dừng lượt đầu (rc 130) và chạy lại bằng `GIT_CONFIG_GLOBAL=rv/offline-git.config` với ký commit tắt cho Git của phép đo. Mini-repo đối chứng tạo được commit với cấu hình đó. Log lượt đầu ở [rv/log/first-gates](rv/log/first-gates).

Sandbox gắn `.git` rỗng chỉ đọc ở thư mục làm việc và `/tmp`. `git rev-parse --is-inside-work-tree` ở thư mục làm việc trả 128. Với một đường giả định trong `rv/tmp`, `_trong_kho_git()` trả chính thư mục làm việc. Với một đường giả định trực tiếp trong `/tmp`, hàm trả `/tmp`. Đây là phép dò trên đường tên, không đọc thông tin xác thực.

<!-- ket-qua-cong -->
| Lệnh | RC | Giờ UTC | Kết quả |
|---|---:|---|---|
| `sau` · `python3 scripts/tl.py --selftest` | 1 | 19:09:41–19:14:27 | Đỏ · `== tl selftest 1772/1786 ==` · [log](rv/log/sau-selftest.out) |
| `nen` · `python3 scripts/tl.py --selftest` | 1 | 19:09:41–19:14:28 | Đỏ · `== tl selftest 1772/1786 ==` · [log](rv/log/nen-selftest.out) |
| `sau` · `python3 scripts/tl.py test-fragments-check --json` | 0 | 19:14:27–19:14:28 | Đạt · `ok=True, status=current, expected/actual bytes 315296/315296` · [log](rv/log/sau-fragments.out) |
| `nen` · `python3 scripts/tl.py test-fragments-check --json` | 0 | 19:14:28–19:14:29 | Đạt · `ok=True, status=current, expected/actual bytes 312974/312974` · [log](rv/log/nen-fragments.out) |
| `nen` · `python3 .github/checks/bundle_fragment_check.py --json` | 1 | 19:14:29–19:15:39 | Đỏ · `ok=False, failed=6, case_count=20` · [log](rv/log/nen-bundle.out) |
| `sau` · `python3 .github/checks/bundle_fragment_check.py --json` | 1 | 19:14:28–19:15:39 | Đỏ · `ok=False, failed=6, case_count=20` · [log](rv/log/sau-bundle.out) |
| `nen` · `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | 19:15:39–19:15:41 | Đạt · `ok=True, expected_file_count=186, checked_file_count=186` · [log](rv/log/nen-verify.out) |
| `sau` · `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | 19:15:39–19:15:41 | Đạt · `ok=True, expected_file_count=186, checked_file_count=186` · [log](rv/log/sau-verify.out) |
| `nen` · `python3 scripts/tl.py workflow-audit --strict --json` | 0 | 19:15:41–19:15:41 | Đạt · `ok=True, py_size.fail=[], py_size.warn=[], files_scanned=74` · [log](rv/log/nen-workflow.out) |
| `sau` · `python3 scripts/tl.py workflow-audit --strict --json` | 0 | 19:15:41–19:15:41 | Đạt · `ok=True, py_size.fail=[], py_size.warn=[], files_scanned=74` · [log](rv/log/sau-workflow.out) |
| `nen` · `python3 scripts/tl.py golden-test --json` | 0 | 19:15:41–19:16:06 | Đạt · `ok=True, case_count=20` · [log](rv/log/nen-golden.out) |
| `sau` · `python3 scripts/tl.py golden-test --json` | 0 | 19:15:42–19:16:06 | Đạt · `ok=True, case_count=20` · [log](rv/log/sau-golden.out) |
| `nen` · `python3 .githooks/eol_policy_test.py` | 1 | 19:16:06–19:20:41 | Đỏ · `29/32 dat` · [log](rv/log/nen-eol.out) |
| `nen` · `python3 -m ruff --version` | 0 | 19:20:41–19:20:41 | Đạt · `ruff 0.15.15` · [log](rv/log/nen-ruff-version.out) |
| `nen` · `python3 -m ruff check --no-cache --select F scripts/test_fragments/wp433_bundled_tach_manh.py` | 0 | 19:20:41–19:20:41 | Đạt · `All checks passed!` · [log](rv/log/nen-ruff.out) |
| `nen` · `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | 19:20:41–19:20:41 | Đạt · `doctrine-scan: sạch — đã quét 12 tệp, 0 chỗ chép doctrine` · [log](rv/log/nen-doctrine.out) |
| `nen` · `python3 .claude/dev/packet_loop.py adr-song --root .` | 0 | 19:20:41–19:20:41 | Đạt · `adr-song: sạch — 66 ADR trên đĩa, 66 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` · [log](rv/log/nen-adr.out) |
| `sau` · `python3 .githooks/eol_policy_test.py` | 1 | 19:16:06–19:20:43 | Đỏ · `29/32 dat` · [log](rv/log/sau-eol.out) |
| `sau` · `python3 -m ruff --version` | 0 | 19:20:43–19:20:43 | Đạt · `ruff 0.15.15` · [log](rv/log/sau-ruff-version.out) |
| `sau` · `python3 -m ruff check --no-cache --select F scripts/test_fragments/wp433_bundled_tach_manh.py` | 0 | 19:20:43–19:20:43 | Đạt · `All checks passed!` · [log](rv/log/sau-ruff.out) |
| `sau` · `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | 19:20:43–19:20:43 | Đạt · `doctrine-scan: sạch — đã quét 12 tệp, 0 chỗ chép doctrine` · [log](rv/log/sau-doctrine.out) |
| `sau` · `python3 .claude/dev/packet_loop.py adr-song --root .` | 0 | 19:20:43–19:20:43 | Đạt · `adr-song: sạch — 66 ADR trên đĩa, 66 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` · [log](rv/log/sau-adr.out) |
| `sau` · `git diff --check e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8 HEAD` | 0 | 19:20:43–19:20:43 | Đạt · `stdout/stderr rỗng` · [log](rv/log/sau-diffcheck.out) |
| `sau` · `git diff --name-only e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8 HEAD` | 0 | 19:20:43–19:20:43 | Đạt · `RELEASE_MANIFEST.json · scripts/test_fragments/wp433_bundled_tach_manh.py · scripts/tl_test_fragments_bundled.py` · [log](rv/log/sau-names.out) |
| `sau` · `python3 -c "import sys; sys.path.insert(0,'scripts'); from tl_core import test_fragments as tf; tf.write_bundled_modules('scripts/test_fragments', 'scripts')"` | 0 | 19:20:43–19:20:44 | Đạt · `stdout/stderr rỗng` · [log](rv/log/sau-regen-bundle.out) |
| `sau` · `git diff --exit-code -- scripts/tl_test_fragments_bundled.py scripts/tl_test_fragments_bundled_2.py` | 0 | 19:20:44–19:20:44 | Đạt · `stdout/stderr rỗng` · [log](rv/log/sau-regen-bundle-diff.out) |
| `sau` · `python3 scripts/tl.py release-manifest --out RELEASE_MANIFEST.json` | 0 | 19:20:44–19:20:45 | Đạt · `package_hash=7432c98d26749f1886443bc290a5db73735bf9f8a2534cd7f87c8568e694c539` · [log](rv/log/sau-regen-manifest.out) |
| `sau` · `git status --porcelain=v1 --untracked-files=all --ignored` | 0 | 19:20:45–19:20:45 | Snapshot trước dọn · `20 tệp ignored do phép đo tạo, tracked và untracked sạch` · [log](rv/log/sau-status.out) |
<!-- het-ket-qua-cong -->

| Lệnh xác nhận A5 | RC | Giờ UTC | Kết quả |
|---|---:|---|---|
| `python3 -B rv/clean-probe-output.py` | 0 | 19:21:25 | Dọn 20 tệp ignored do phép đo sinh trong mỗi clone, ở `references/golden/fixtures/` và `scripts/.tl_state/`. [Danh sách](rv/log/cleanup.out) |
| `bash rv/verify-regeneration.sh` | 0 | 19:21:25–19:21:26 | Tái sinh W2/W3 bằng writer và W4 bằng `release-manifest`. `git diff --exit-code` trên bundle/manifest và `git status --porcelain=v1` sạch. Snapshot `kho`, base và C kiểm HEAD/tree, index, tracked, untracked, ignored và SHA256 W1–W4. W1–W4 của C trùng byte với `kho`. [Snapshot](rv/log/final-snapshot.out) |

A5 đạt. Snapshot chỉ xác nhận trạng thái quan sát được tại các mốc kiểm. Ruff F chạy cục bộ trên W1 với bản 0.15.15. CI GitHub chưa được đo trong lượt offline, Windows native được miễn trong đặc tả.

## Săn hồi quy

Hai lượt `python3 -B rv/hunt.py nen` và `python3 -B rv/hunt.py sau` dùng nguyên văn runner `RUN` của ma trận, chép tệp tracked vào cây tạm riêng cho từng ca. Lượt đầu trả rc 1 trên cả hai mốc vì neo `absent_shard_empty_field` thừa khoảng trắng. Sau khi sửa neo, ca này áp đúng một lần và trả rc 0 ở cả hai mốc (19:07:57–19:08:23Z). Có 13 hướng ngoài đối chứng. Cột `rc` trong output là mã thoát của tiến trình fragment. `run` và `do` là kết quả oracle. [Log nền](rv/log/hunt-nen.out) · [Log C](rv/log/hunt-sau.out) · [Nền, chạy lại](rv/log/hunt-nen-retry.out) · [C, chạy lại](rv/log/hunt-sau-retry.out)

<!-- ket-qua-san -->
| Hướng | Giả thuyết | Lệnh | Output thật | Kết luận |
|---|---|---|---|---|
| Đối chứng | Fragment nguyên bản trả 32 khoá xanh. | `python3 -B rv/hunt.py nen control` và `python3 -B rv/hunt.py sau control` | base `rc=0 run=True so_nhan=32 do=`, C `rc=0 run=True so_nhan=32 do=` | KHÔNG PHẢI LỖI |
| Hình dạng gói hai fragment | Thay gán một đích bằng gán unpack trên `hai`. V3 phải đỏ dù C đọc dữ liệu rỗng. | `python3 -B rv/hunt.py nen hai_swapped_ast` và `python3 -B rv/hunt.py sau hai_swapped_ast` | base `rc=0 run=False so_nhan=32 do=V3 ly_do=V3:KeyError`, C `rc=0 run=False so_nhan=32 do=V3` | KHÔNG PHẢI LỖI |
| Bảo toàn nguồn trong bundle | Một mục trên `deu` giữ nguyên tên và kích thước nhưng đổi thân `run()`. Các phép so tên và sao bundle có bắt được nội dung sai. | `python3 -B rv/hunt.py nen deu_source_content` và `python3 -B rv/hunt.py sau deu_source_content` | base `rc=0 run=True so_nhan=32 do=`, C `rc=0 run=True so_nhan=32 do=` | KHÔNG PHẢI LỖI hồi quy. Cùng sống, P3 theo Q7. |
| Thân mảnh phụ ở ranh UTF-8 | Một mảnh phụ của `lech` có thêm `assert True`. V8 phải đọc cả mảnh đó. | `python3 -B rv/hunt.py nen lech_assert` và `python3 -B rv/hunt.py sau lech_assert` | base `rc=0 run=True so_nhan=32 do=`, C `rc=0 run=False so_nhan=32 do=V8` | KHÔNG PHẢI LỖI |
| Giá trị chuẩn ở mảnh quá cỡ | `SOURCES` của fixture `lon` chuyển sang lời gọi `tuple`. Ngoại lệ đọc literal phải làm đỏ khoá. | `python3 -B rv/hunt.py nen lon_nonliteral` và `python3 -B rv/hunt.py sau lon_nonliteral` | base `rc=0 run=False so_nhan=32 do=V6 ly_do=V6:ValueError`, C `rc=0 run=False so_nhan=32 do=V6,V8 ly_do=V6:ValueError,V8:ValueError` | KHÔNG PHẢI LỖI |
| Thứ tự metadata mảnh | Đảo thứ tự `SHARDS` trên `deu` mà giữ nguyên các mục nguồn. V9 phải đỏ. | `python3 -B rv/hunt.py nen deu_manifest_reverse` và `python3 -B rv/hunt.py sau deu_manifest_reverse` | base `rc=0 run=False so_nhan=32 do=V9`, C `rc=0 run=False so_nhan=32 do=V9` | KHÔNG PHẢI LỖI |
| Kiểu dữ liệu ở loader | Loader nới kiểu container `SOURCES` từ tuple sang tuple/list. Các fixture loader phải phân biệt hai kiểu. | `python3 -B rv/hunt.py nen loader_relaxes_sources_type` và `python3 -B rv/hunt.py sau loader_relaxes_sources_type` | base `rc=0 run=True so_nhan=32 do=`, C `rc=0 run=True so_nhan=32 do=` | KHÔNG PHẢI LỖI hồi quy. Cùng sống, P3 theo Q7. |
| Ranh generator/writer | Writer cắt LF ở cuối mảnh chính trong khi byte generator giữ nguyên. V11 phải đỏ. | `python3 -B rv/hunt.py nen writer_primary_eol` và `python3 -B rv/hunt.py sau writer_primary_eol` | base `rc=0 run=False so_nhan=32 do=V11`, C `rc=0 run=False so_nhan=32 do=V11` | KHÔNG PHẢI LỖI |
| V23 đối chiếu danh sách mảnh lạc | Cổng trả mỗi tên mảnh lạc hai lần dù quyết định stale đúng. | `python3 -B rv/hunt.py nen extra_duplicate_names` và `python3 -B rv/hunt.py sau extra_duplicate_names` | base `rc=0 run=False so_nhan=32 do=V23`, C `rc=0 run=False so_nhan=32 do=V23` | KHÔNG PHẢI LỖI |
| Mã thoát CLI | Nhánh thất bại trả rc 1 thay cho rc 2 và giữ nguyên payload. | `python3 -B rv/hunt.py nen stale_rc_wrong` và `python3 -B rv/hunt.py sau stale_rc_wrong` | base `rc=0 run=True so_nhan=32 do=`, C `rc=0 run=False so_nhan=32 do=V23,V24,V25,V26,V27` | KHÔNG PHẢI LỖI |
| V25 phân biệt thiếu mảnh | Cổng báo `actual_bytes=-1` cho mảnh vắng. Khoá phải đòi `None`. | `python3 -B rv/hunt.py nen absent_shard_empty_field` và `python3 -B rv/hunt.py sau absent_shard_empty_field` | base `rc=0 run=False so_nhan=32 do=V25`, C `rc=0 run=False so_nhan=32 do=V25` | KHÔNG PHẢI LỖI |
| V26 kiểm kiểu JSON | Cổng trả số `0` ở `ok` trên nhánh missing, giữ rc 2, status và error. | `python3 -B rv/hunt.py nen missing_numeric_ok` và `python3 -B rv/hunt.py sau missing_numeric_ok` | base `rc=0 run=True so_nhan=32 do=`, C `rc=0 run=True so_nhan=32 do=` | KHÔNG PHẢI LỖI hồi quy. Cùng sống, P3 theo Q7. |
| V27 trạng thái current tự mâu thuẫn | Cổng giữ rc 0 và `ok=true` nhưng thêm mã lỗi stale vào JSON current. | `python3 -B rv/hunt.py nen current_has_error` và `python3 -B rv/hunt.py sau current_has_error` | base `rc=0 run=True so_nhan=32 do=`, C `rc=0 run=False so_nhan=32 do=V27` | KHÔNG PHẢI LỖI |
| Kích thước từng mảnh khi stale | Nhánh stale ghi kích thước kỳ vọng đè số byte thực tế của từng mảnh có mặt trong khi số tổng hợp vẫn đúng. | `python3 -B rv/hunt.py nen stale_wrong_size` và `python3 -B rv/hunt.py sau stale_wrong_size` | base `rc=0 run=True so_nhan=32 do=`, C `rc=0 run=True so_nhan=32 do=` | KHÔNG PHẢI LỖI hồi quy. Cùng sống, P3 theo Q7. |
<!-- het-ket-qua-san -->

## Lớp finding

| Slug | Finding IDs | Mức cao nhất | Cách vá chung | Phép kiểm đóng lớp |
|---|---|---|---|---|

| `bundle-gate-fixture-oracle` | F10, hai biểu hiện · verdict `5293a85` @ `3f5641c8` và lịch sử §7 | P2 lịch sử | Dùng một fixture cho mỗi nhiễu loạn. Đối chiếu quyết định đủ bốn trường và băm/số byte tính độc lập. | `r11_size_only`, `r11_one_stale_ok`, `r11_missing_ok_narrow`, cặp `a7_` tương ứng và A6. Đã vá trong phạm vi Q7. Ba ca trên đỏ lần lượt V24/V27, V27, V26 trên C. Đối chứng xanh, không mất ca nền theo A6. |
| `shard-ast-shape-oracle` | F11, hai biểu hiện · verdict `5293a85` @ `3f5641c8` và lịch sử §7 | P3 lịch sử | Giới hạn nguồn literal vào phép gán chuẩn đầu tiên và kiểm hình dạng trên cả ba topology nhiều mảnh. | `r11_ann_empty`, `r11_duplicate`, bảy ca `r11_rv4_s*` và đối chứng V3/V8/V9. Đã vá trong phạm vi Q7. Cả hai ca F11 và bảy ca `r11_rv4_s*` đều chỉ đỏ V8 và không có lý do ngoại lệ. Probe ở `hai`, `deu`, `lech`, `lon` và A6 xác nhận giữ các ca base bắt. |
| `bundled-gate-oracle-to-hop` | R11-C1–C4 · probe ngoài ma trận trên `e2f28fb` và `4f648e5`. Kế thừa 13 ca `no_` và các ca RV5-F1 đã ghi. | P3 theo Q7 | Mô hình tham chiếu đọc nguồn, hình dạng và toàn bộ payload theo từng topology. Khoá kiểu dữ liệu và đối chiếu dữ liệu nguồn, quyết định, byte tổng và byte từng mảnh. | Cả hai mốc cho 32 khoá xanh với bốn đột biến mới. Khi đóng lớp, giữ đối chứng xanh và yêu cầu đúng khoá đỏ theo từng phép dưới đây. |
| `a4-runner-git-marker` | R11-A4 · exact C và base trong sandbox | P2 về nghiệm thu | Chạy cặp kiểm tra trên runner có đường fixture tạm độc lập với marker `.git`. | Selftest 1786/1786, bundle checker 20/20 với `failed: []` và EOL 32/32. Ba lệnh rc 0. |

## Soi mã W1

- `scripts/test_fragments/wp433_bundled_tach_manh.py:67` dựng hình dạng từ AST sau docstring đầu. Nhánh đọc literal chỉ nhận `Assign` chuẩn cho `SOURCES`/`SHARDS`. `AnnAssign` và gán nhiều đích còn trong hình dạng, nên V3/V8 có thể làm đỏ dù đường dữ liệu bỏ qua chúng. V8 chạy generator trên `deu`, `lech` với hạn `2*s5`, và `lon` với hạn mặc định. Phần hình dạng của `deu` đòi đúng ba mảnh, phần ranh và nội dung tên của `lech`/`lon` do V5/V6 kiểm. `setdefault` vẫn đánh giá giá trị trước khi gọi, là RV5-F2 đã ghi.
- `scripts/test_fragments/wp433_bundled_tach_manh.py:195` đọc bốn trường quyết định. `hong()` phục hồi fixture ở mỗi lượt bằng `cong()`, lấy dữ liệu kỳ vọng từ bản dựng độc lập và lấy dữ liệu đĩa sau cổng. Nó giữ ca nối nguyên dòng của nền, thêm sáu ca riêng, rồi so băm và số byte ở dòng 211. `all([...])` thử cả bảy ca khi các ca trả boolean. V24 thử mảnh chính và mảnh phụ, V23 thử riêng từng tên mảnh lạc.
- `scripts/test_fragments/wp433_bundled_tach_manh.py:221` kiểm khoá V25 với cả quyết định và `actual_bytes=None`. V26 kiểm quyết định thiếu mảnh chính. V27 dừng sớm khi vế current sai, làm đỏ chính V27. JSON lỗi từ `_check()` trở thành dict rỗng nên không thể thoả tuple quyết định. Ngoại lệ của phép đo từng khoá được `run()` ghi False và giữ các khoá sau ở dòng 310.

## Findings

### Điều kiện nghiệm thu A4

**R11-A4 · P2 · `a4-runner-git-marker` · `scripts/tl_gws.py:1124`, `scripts/tl_selftest.py:21572`.** Sau khi tắt ký commit trong cấu hình Git của phép đo, cả hai clone chạy đúng lệnh `python3 scripts/tl.py --selftest` và cùng dừng ở `1772/1786`, rc 1. Hai danh sách đỏ trùng byte, gồm tám ca `r973_bootstrap_*` và sáu fragment GWS/NLM. Bundle checker cũng trả rc 1 với đúng sáu fragment đó trong 20 ca trên cả hai mốc. EOL trả rc 1, 29/32 ở cả hai mốc, với cùng ba ca tích hợp phụ thuộc bundle checker. `wp433_bundled_tach_manh` xanh trong cả selftest lẫn bundle checker. Thư mục `.git` chỉ đọc do sandbox gắn vào tổ tiên của `TMPDIR` làm fixture được xem là nằm trong kho. Điều kiện A4 đòi `1786/1786` trên C, nên lượt này chưa có bằng chứng đạt. Hướng xử lý là chạy lại ba cổng bị ảnh hưởng trên cặp clone exact SHA trong runner có thư mục fixture tạm ngoài các cây có marker `.git`. Phép khoá lại là selftest rc 0 và 1786/1786 cùng bundle checker rc 0 với 20 ca, `failed: []` và EOL rc 0, 32/32. Giữ nguyên ca thử chặn đường trong kho để tránh hồi quy ở ranh ghi dữ liệu xác thực. [Ca đỏ nền](rv/log/nen-selftest.failures) · [Ca đỏ C](rv/log/sau-selftest.failures) · [Bundle checker C](rv/log/sau-bundle.out) · [EOL C](rv/log/sau-eol.out)

### P3 theo Q7 · `bundled-gate-oracle-to-hop`

Cả bốn đột biến dưới đây sống trên base và C với `rc=0 run=True so_nhan=32 do=`. Phép dò trực tiếp `python3 -B rv/witness.py` rc 0, 19:07:24–19:07:29Z, xác nhận từng đột biến thực sự đổi hành vi fixture. [Đầu ra phép dò](rv/log/witness.out)

- **R11-C1 · P3 · `bundled-gate-oracle-to-hop` · `scripts/test_fragments/wp433_bundled_tach_manh.py:279`.** `deu_source_content` đổi thân ca nguồn từ `return True` thành `return None` và giữ cùng tên, cùng 82.340 byte cho mảnh chính. V4 chỉ lấy tên và V11 so writer với chính đầu ra đã bị đổi. Có thể khoá lại bằng cách so các cặp tên và nội dung nguồn với fixture viết tay đã chuẩn hoá EOL. Rủi ro khi vá là chấm đỏ thay đổi hợp lệ ở biểu diễn chuỗi hoặc xuống dòng.
- **R11-C2 · P3 · `bundled-gate-oracle-to-hop` · `scripts/test_fragments/wp433_bundled_tach_manh.py:291`.** `loader_relaxes_sources_type` cho loader nhận list ở chỗ hợp đồng đòi tuple. Loader nguyên bản trả `BUNDLED_MODULE_CONTRACT` trên mẫu list và mutant trả ID `wp9001_a`. Thêm fixture loader dùng list làm đối chứng âm với tuple dương. Rủi ro khi vá là trộn kiểm kiểu container với kiểm thứ tự hoặc kiểm entry.
- **R11-C3 · P3 · `bundled-gate-oracle-to-hop` · `scripts/test_fragments/wp433_bundled_tach_manh.py:195`.** `missing_numeric_ok` trả `ok=0` kiểu int, giữ rc 2 và mã thiếu đúng. So tuple trong Python coi `0 == False`, nên V26 xanh. So boolean theo kiểu/định danh và khoá bằng ca JSON số 0 trên nhánh thiếu có đối chứng boolean. Rủi ro khi vá là thay đổi kiểm soát giá trị hợp lệ ở các nhánh khác của `quyet()`.
- **R11-C4 · P3 · `bundled-gate-oracle-to-hop` · `scripts/test_fragments/wp433_bundled_tach_manh.py:211`.** `stale_wrong_size` ghi kích thước kỳ vọng vào trường thực tế từng mảnh khi tất cả mảnh còn có mặt. Phép dò một mảnh cho đĩa và tổng đều 217 byte, nhưng phần tử `shards` báo 216. V24/V27 kiểm bốn trường tổng, V29 chỉ đo current. So kích thước từng mảnh với fixture độc lập ngay ở stale và khoá bằng mutant này. Rủi ro khi vá là xử lý nhầm giá trị `None` của mảnh vắng.

### Ghi nhận từ handoff

RV5-F1 gồm bốn ca nợ có sẵn m07/m09/m10/m15. RV5-F2 ghi việc `setdefault` đánh giá literal trước khi gọi. RV5-F3 ghi §7 nói chín chốt trong khi A3 có mười. Ba mục này được giữ theo hồ sơ cũ. Chính sách Q7 ghi nợ `bundled-gate-oracle-to-hop` và đặt các ca cùng sống ở P3 trong packet này. Hai lớp sửa trong phạm vi đã có bằng chứng đóng các biểu hiện được giao. Một lớp điều kiện nghiệm thu A4 còn mở, với ba cổng đỏ. Một lớp nợ P3 ghi bốn biểu hiện được đo thêm.

KET_LUAN: request_changes
