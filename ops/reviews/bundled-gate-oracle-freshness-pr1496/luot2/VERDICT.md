---
verdict: approve
reviewed_sha: 4f648e5b784aa4e19f0385eee68cd75e69e1dd18
tree: 33f7b4183f408dafc029ecf860aab9857f244365
packet: BUNDLED-GATE-ORACLE-FRESHNESS
lease: wp433-r11-g1-claude
review_class: sensitive
provider: openai_codex
execution_surface: codex_cli
transport: machine
luot: 2
---

# Xác minh PR #1496, lượt 2

Đối chiếu ứng viên `4f648e5b784aa4e19f0385eee68cd75e69e1dd18` và bằng chứng đóng R11-A4 cho packet `BUNDLED-GATE-ORACLE-FRESHNESS`.

## Bảng phép đo

Ngày 21-11-2026. Giờ trong các hàng CI và executor lấy từ log gốc. Giờ các lệnh đối chiếu lấy từ phiên reviewer.

| Lệnh | RC | Giờ UTC | Kết quả |
| --- | ---: | --- | --- |
| `cmp PROMPT.md ../runs/873e0a10/prompt.snapshot` | 0 | 19:30:45 | Bản chỉ thị trong thư mục làm việc trùng byte với snapshot được giao. |
| `sha256sum -c bang-chung/BAM.txt` | 0 | 19:30:45 | Khớp cả ba băm SHA-256 của verdict lượt 1 và hai log CI. |
| `git -C kho rev-parse HEAD 'HEAD^{tree}' refs/tmp/pr1496-merge 'refs/tmp/pr1496-merge^{tree}' 'refs/tmp/pr1496-merge^1' 'refs/tmp/pr1496-merge^2'` và `git -C kho show -s --format='%H %P %T' refs/tmp/pr1496-merge` | 0, 0 | 19:30:45 | HEAD đúng C. Merge `bac598d4e4ab9a50242e496405ec7548ba38b807` có đúng hai cha theo thứ tự `e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8` và `4f648e5b784aa4e19f0385eee68cd75e69e1dd18`. C và merge cùng tree `33f7b4183f408dafc029ecf860aab9857f244365`. |
| `git -C kho diff --name-only e2f28fb HEAD` | 0 | 19:30:45 | Đúng ba tệp trong write set là `RELEASE_MANIFEST.json`, `scripts/test_fragments/wp433_bundled_tach_manh.py` và `scripts/tl_test_fragments_bundled.py`. |
| `git -C kho show 5bd8463e9:ops/specs/BUNDLED-GATE-ORACLE-FRESHNESS-r5.md \| sha256sum` và `git -C kho rev-parse` trên cùng blob | 0, 0 | 19:33:58 | SHA-256 `5ae3d269551dd6791aafc33e0c498bda7103fef28e85bf6a79cb4ed4d5f26159`, blob `f1621b9ed2e6b9d4dc91cf2562f9f44b7b419ec1`. Cả hai khớp lease `wp433-r11-g1-claude` tại `bc4fc8e`, revision 11, generation 1, `sensitive`. |
| CI `gate (ubuntu-latest)` · `git checkout --progress --force refs/remotes/pull/1496/merge`, `git log -1 --format=%H` | 0† | 18:58:20–18:58:22 | Checkout báo `HEAD is now at bac598d Merge 4f648e5… into e2f28fb…`, rồi trả full SHA `bac598d4e4ab9a50242e496405ec7548ba38b807`. [Log dòng 1192](bang-chung/job-136949922299.log#L1192) · [SHA đầy đủ](bang-chung/job-136949922299.log#L1219) |
| CI `gate (ubuntu-latest)` · `PR head contains required EOL base` | 0† | 19:03:46 | `PR_HEAD_SHA: 4f648e5b784aa4e19f0385eee68cd75e69e1dd18` cùng lệnh kiểm tổ tiên EOL. [Workflow](kho/.github/workflows/ci.yml#L232) · [Log dòng 1533](bang-chung/job-136949922299.log#L1533) |
| CI `gate (ubuntu-latest)` · `python .githooks/eol_policy_test.py` | 0† | 19:04:00–19:09:10 | Bước `eol-policy selftest` có 32 dòng `PASS`, kết thúc `32/32 dat` liền trước `pre_push_test.py`. [Workflow](kho/.github/workflows/ci.yml#L268) · [Lệnh dòng 1625](bang-chung/job-136949922299.log#L1625) · [Kết quả dòng 1672](bang-chung/job-136949922299.log#L1672) |
| CI `gate (ubuntu-latest)` · `python .github/checks/bundle_fragment_check.py --json` | 0† | 19:09:19–19:10:56 | Bước `bundled-fragment check (topology gói)` trả JSON `bundle_fragment_check.v1`, `ok: true`, `case_count: 20`, `failed: []`. Cả 20 mục `cases` đều `ok: true`, gồm `wp433_bundled_tach_manh`. JSON kết thúc trước bước `gen_instructions`. [Workflow](kho/.github/workflows/ci.yml#L294) · [Lệnh dòng 1721](bang-chung/job-136949922299.log#L1721) · [JSON dòng 1735–1914](bang-chung/job-136949922299.log#L1735) |
| CI `gate (ubuntu-latest)` · `python scripts/tl.py --selftest` | 0† | 19:10:56–19:16:17 | Bước `tl selftest (luot PR — khong sinh bang chung)` có khối cuối 1786 dòng `[OK]`, gồm `[OK] wp433_bundled_tach_manh` ở dòng 3816, và `== tl selftest 1786/1786 ==` ở dòng 3849. [Workflow](kho/.github/workflows/ci.yml#L339) · [Lệnh dòng 1993](bang-chung/job-136949922299.log#L1993) · [Kết quả](bang-chung/job-136949922299.log#L3849) |
| CI `gate-nhanh-gop` · `git checkout --progress --force refs/remotes/pull/1496/merge`, `git log -1 --format=%H` | 0† | 18:59:52–18:59:53 | Cùng checkout merge PR #1496. Dòng 1212 ghi đủ SHA hai cha và dòng 1215 ghi full merge SHA. [Log dòng 1212](bang-chung/job-136950323162.log#L1212) |
| CI `gate-nhanh-gop` · `python ops/nhanh_don_duoc_test.py --gop-dich manh` | 0† | 18:59:54–18:59:55 | Bước `gộp mảnh nhanh_don_duoc (targeted_mutant_gate)` báo `GOP 8/8 manh` trên full merge SHA và `DAT`. [Workflow](kho/.github/workflows/ci.yml#L1022) · [Log dòng 1300](bang-chung/job-136950323162.log#L1300) |
| Executor base · `python3 scripts/tl.py --selftest` | 0 | 18:28:15–18:34:06 | `nen-selftest.out` dòng 1809 ghi 1786/1786, dòng 1776 ghi `[OK] wp433_bundled_tach_manh`. `tong.txt` dòng 1. |
| Executor base · `python3 .github/checks/bundle_fragment_check.py --json` | 0 | 18:34:07–18:36:04 | `nen-bfc.out` báo `ok: true`, `case_count: 20`, `failed: []`, fragment WP433 đạt. `tong.txt` dòng 3. |
| Executor base · `python3 .githooks/eol_policy_test.py` | 0 | 18:36:31–18:43:10 | `nen-eol.out` có 32 dòng `PASS`, dòng 34 ghi `32/32 dat`. `tong.txt` dòng 7. |
| Executor C · `python3 scripts/tl.py --selftest` | 0 | 18:43:11–18:48:45 | `sau-selftest.out` dòng 1809 ghi `== tl selftest 1786/1786 ==`, dòng 1776 ghi `[OK] wp433_bundled_tach_manh`. `tong.txt` dòng 11. |
| Executor C · `python3 .github/checks/bundle_fragment_check.py --json` | 0 | 18:48:46–18:50:39 | `sau-bfc.out` một khối JSON schema `bundle_fragment_check.v1`, dòng 24 `case_count: 20`, dòng 170 `failed: []`, dòng 172 `ok: true`. `tong.txt` dòng 14. |
| Executor C · `python3 .githooks/eol_policy_test.py` | 0 | 18:51:05–18:57:03 | `sau-eol.out` có 32 dòng `PASS`, dòng 34 ghi `32/32 dat`. `tong.txt` dòng 19. |
| Reviewer · `python3 -B rv2/doi-chieu.py` | 0 | 19:33:58 | Kiểm các ranh bước trong hai log CI, đọc sáu đầu ra qua `git -C kho show bc4fc8e:ops/handoff/wp433/r11-g1/do/<tên-tệp>` và đối chiếu `tong.txt`. `dinh-danh.txt` gắn `nen` với base và `sau` với C, cả hai `shallow=false`. [Đầu ra](rv2/doi-chieu.out) · [Lệnh đối chiếu](rv2/doi-chieu.py) |
| Reviewer · `git -C rv2/fixture-tmp rev-parse --is-inside-work-tree`, dò `.git` trên đường dẫn thực, `findmnt --mountpoint` | Git 128, findmnt 0 cho mỗi marker | 19:31:34–19:32:56 | `TMPDIR` mặc định là `/tmp`. `rv2/fixture-tmp` nằm dưới hai marker tại `codex-pr-2/.git` và `/tmp/.git`, cả hai là mount chỉ đọc. `/tmp` cũng trả Git 128 và vẫn có `.git`. |
| Reviewer · Chạy lại ba lệnh trên clone C với `TMPDIR` đạt điều kiện tiền kiểm | — | — | **KHÔNG ĐO ĐƯỢC**. Mọi đường ghi được phép nằm dưới `/tmp/.git`. `/var/tmp` không có marker nhưng thao tác tạo thư mục trả `EROFS`. `/dev/shm` không có marker và phép dò tạo thư mục tạm thành công, nhưng đường này nằm ngoài các gốc ghi được cấp cho phiên. |
| `git -C kho diff --check e2f28fb HEAD`, `git -C kho diff --exit-code HEAD -- .github/workflows/ci.yml`, `git --no-optional-locks -C kho status --porcelain=v1 --untracked-files=all --ignored=matching` | 0, 0, 0 | 19:33:58 | Cả ba đầu ra rỗng. HEAD và tree cuối phiên vẫn khớp định danh. |

† Log GitHub Actions ghi đầu ra và việc chuyển sang bước kế tiếp hoặc cleanup. Mã 0 của bước CI được suy từ đầu ra dương, hợp đồng mã thoát của lệnh và sự vắng mặt của dòng lỗi bước trong log. `tong.txt` ghi trực tiếp mã thoát của executor. Cảnh báo thiếu tệp upload `gate-evidence` ở job `gate` khớp cấu hình bước PR tại workflow dòng 376–383. [Log cảnh báo](bang-chung/job-136949922299.log#L3871)

## R11-A4 · ĐÃ VÁ THẬT

Điều kiện nghiệm thu P2 của lượt 1 đã đóng. Job Ubuntu chạy cả ba lệnh trên merge có cùng tree với C và cho selftest `1786/1786`, bundle checker 20 ca với `failed: []`, EOL `32/32 dat`. Các bước thực thi đúng lệnh trong workflow. Log selftest còn ghi đường fixture dưới `/tmp/tra-luat-selftest-l6242gfz`, ngoài checkout CI tại `/home/runner/work/tra-luat/tra-luat`. Đầu ra runner ngoài sandbox xác nhận cả ba lệnh trả 0 trên hai clone đầy đủ của base và C. [Kết quả đối chiếu](rv2/doi-chieu.out) · [Đường fixture trong CI](bang-chung/job-136949922299.log#L2038)

Reviewer kiểm độc lập log và Git objects tại chỗ. Phép chạy lại trong sandbox được ghi **KHÔNG ĐO ĐƯỢC** do marker ở tổ tiên của `TMPDIR` được phép ghi. Log CI và handoff cung cấp bằng chứng chạy và kết quả dương. Việc rà toàn bộ tổ tiên fixture bằng `lstat` chỉ thực hiện được trên sandbox của reviewer. Kết quả xác minh đóng điều kiện môi trường của R11-A4 trên cùng ứng viên, với ba cổng đạt ở môi trường chạy ngoài sandbox này. [Finding và phép khóa lượt 1](bang-chung/VERDICT-luot1.md#điều-kiện-nghiệm-thu-a4)

## Bảng lớp finding

| Slug lượt 1 | Finding, nguồn và mức | Trạng thái | Cách xử lý và phép kiểm đóng lớp |
| --- | --- | --- | --- |
| `bundle-gate-fixture-oracle` | F10, hai biểu hiện. Lịch sử `5293a85` @ `3f5641c8`, P2 lịch sử. | **ĐÃ VÁ THẬT** trong phạm vi Q7, bằng chứng lượt 1 trên cùng C. | Fixture riêng theo nhiễu loạn, đối chiếu quyết định và số byte/băm độc lập. `r11_size_only`, `r11_one_stale_ok`, `r11_missing_ok_narrow` cho V24/V27, V27, V26 theo thứ tự. Đối chứng, `a7_` tương ứng và A6 đạt. |
| `shard-ast-shape-oracle` | F11, hai biểu hiện. Lịch sử `5293a85` @ `3f5641c8`, P3 lịch sử. | **ĐÃ VÁ THẬT** trong phạm vi Q7, bằng chứng lượt 1 trên cùng C. | Neo phép gán chuẩn đầu tiên và kiểm hình dạng trên mọi topology nhiều mảnh. `r11_ann_empty`, `r11_duplicate` và bảy ca `r11_rv4_s*` đều chỉ đỏ V8. Đối chứng và A6 đạt. |
| `bundled-gate-oracle-to-hop` | R11-C1–C4, P3 theo Q7. Probe lượt 1 trên base `e2f28fb` và C `4f648e5`. | **CHƯA VÁ**, nợ đã ghi theo Q7. | Bốn đột biến về nội dung nguồn, kiểu `sources`, kiểu `ok` và số byte riêng từng mảnh sống ở cả hai mốc. Phép đóng nợ dùng fixture độc lập kiểm nội dung, hình dạng, kiểu, quyết định và số byte từng mảnh, giữ đối chứng xanh. |
| `a4-runner-git-marker` | R11-A4, P2 lượt 1 trên base và C. | **ĐÃ VÁ THẬT** về điều kiện nghiệm thu, không còn P2 mở. | Chạy ba cổng trên runner có fixture tạm ngoài cây Git. Log CI đúng tree và đầu ra ngoài sandbox đúng SHA cho đủ ba kết quả dương. |

Lượt 1 đã đo A0–A3, A5, A6 đạt, cùng 13 hướng săn không thấy hồi quy trên cặp base/C. Lượt 2 dùng lại kết quả ma trận 125 đột biến của cùng cặp và đối chiếu bằng chứng bổ sung của A4. [Verdict lượt 1](bang-chung/VERDICT-luot1.md)

## Findings mới

Không có finding mới. R11-A4 đã đóng và R11-C1–C4 được giữ là P3 theo Q7. Số P0–P2 còn mở trong phạm vi review là 0.

KET_LUAN: approve
