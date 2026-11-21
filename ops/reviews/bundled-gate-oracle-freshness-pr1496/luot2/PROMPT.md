# Codex review mã lượt 2 (XÁC MINH) — PR #1496, packet wp433 r11 (BUNDLED-GATE-ORACLE-FRESHNESS)

Bạn là REVIEWER Codex độc lập, READ-ONLY đối với kho sản phẩm. Thư mục làm việc: thư mục chứa tệp này.
Kho clone đầy đủ ở `./kho`, HEAD detached tại ứng viên. KHÔNG push, KHÔNG gọi mạng, KHÔNG để lại commit trong `./kho`.
Mọi thứ bạn tạo đặt trong thư mục con MỚI (vd `./rv2/`). Không đọc secrets.

## Bối cảnh
Lượt 1 (cùng reviewed_sha) trả `changes_requested`; verdict ở `bang-chung/VERDICT-luot1.md`. Lượt 1 đã đo và kết luận:
A0–A3, A5, A6 đạt; 13 hướng săn không có hồi quy; hai lớp F10/F11 đã vá trong phạm vi Q7; R11-C1..C4 là P3 nợ
`bundled-gate-oracle-to-hop`. Finding chặn DUY NHẤT là **R11-A4 (P2, `a4-runner-git-marker`)**: trong sandbox, selftest
1772/1786, bundle checker 6/20 đỏ, EOL 29/32 — trùng nhau trên base lẫn C, vì `.git` chỉ đọc gắn lên tổ tiên `TMPDIR`.
Phép khoá lại lượt 1 đòi: selftest rc 0 và 1786/1786; bundle checker rc 0, 20 ca, `failed: []`; EOL rc 0, 32/32 —
trên runner KHÔNG có marker `.git` ở tổ tiên thư mục fixture tạm.

## Nhiệm vụ lượt này: XÁC MINH R11-A4 đã đóng — bằng đo, không nhận lời
Định danh: reviewed_sha `4f648e5b784aa4e19f0385eee68cd75e69e1dd18`, tree `33f7b4183f408dafc029ecf860aab9857f244365`.
Bằng chứng do executor cung cấp (lời khai — bạn phải kiểm):
1. Log job CI GitHub trên PR #1496: `bang-chung/job-136949922299.log` (job `gate (ubuntu-latest)`) và
   `bang-chung/job-136950323162.log` (job `gate-nhanh-gop`). Băm ở `bang-chung/BAM.txt`. CI chạy trên merge ref
   `refs/tmp/pr1496-merge` = `bac598d4e4ab9a50242e496405ec7548ba38b807` (có sẵn trong `./kho`).
   Kiểm: (a) `bac598d` có hai cha `e2f28fb…` và `4f648e5…`, và `bac598d^{tree}` == `4f648e5^{tree}` == tree trên;
   (b) log ghi đúng SHA ấy (`HEAD is now at bac598d …`, `PR_HEAD_SHA: 4f648e5…`); (c) trong log có, ở ĐÚNG bước tương ứng,
   `== tl selftest 1786/1786 ==` kèm `[OK] wp433_bundled_tach_manh`; bundle checker `"case_count": 20` và `"failed": []`;
   EOL `32/32 dat`. Đọc ngữ cảnh quanh từng dòng để chắc dòng ấy thuộc đúng lệnh (không phải một lệnh khác in số giống).
   Đối chiếu tên bước với `.github/workflows/ci.yml` trong `./kho`.
2. Đầu ra đo của executor ngoài sandbox (clone đầy đủ trên đĩa, 18:28–18:57Z):
   `git -C kho show bc4fc8e:ops/handoff/wp433/r11-g1/do/sau-selftest.out`, `.../sau-bfc.out`, `.../sau-eol.out`, `.../tong.txt`.
3. Nếu sandbox của bạn cho phép, thử TỰ chạy lại ba cổng trên một clone của C với `TMPDIR` đặt ở nơi không có `.git` ở
   tổ tiên (dò trước bằng `git -C <dir> rev-parse --is-inside-work-tree` phải KHÔNG trả 0, và kiểm không có `.git` ở mọi
   tổ tiên). Không làm được thì ghi KHÔNG ĐO ĐƯỢC kèm lý do — đừng coi đó là lỗi của C.
4. Kiểm không có thay đổi nào khác: `git -C kho diff --name-only e2f28fb HEAD` vẫn ⊆ {RELEASE_MANIFEST.json,
   scripts/test_fragments/wp433_bundled_tach_manh.py, scripts/tl_test_fragments_bundled.py} và HEAD/tree đúng định danh.

Tiêu chí chặn giữ nguyên như lượt 1 (Q7): chỉ hồi quy so với base, lỗi sản phẩm, hoặc A0–A6 đo sai mới là P0–P2.
Không cần chạy lại ma trận 125 đột biến (lượt 1 đã đo, log ở verdict lượt 1).

## Đầu ra — ghi TĂNG DẦN `VERDICT.md` trong thư mục này
```yaml
verdict: approve | changes_requested
reviewed_sha: 4f648e5b784aa4e19f0385eee68cd75e69e1dd18
tree: 33f7b4183f408dafc029ecf860aab9857f244365
packet: BUNDLED-GATE-ORACLE-FRESHNESS
lease: wp433-r11-g1-claude
review_class: sensitive
provider: openai_codex
execution_surface: codex_cli
transport: machine
luot: 2
```
Rồi: bảng phép đo (lệnh, rc, giờ UTC, kết quả); trạng thái R11-A4 theo nhãn §8 (ĐÃ VÁ THẬT / VÁ MỘT PHẦN / …) kèm bằng chứng;
bảng lớp (giữ slug lượt 1); findings mới nếu có. Dòng CUỐI đúng một: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`.
