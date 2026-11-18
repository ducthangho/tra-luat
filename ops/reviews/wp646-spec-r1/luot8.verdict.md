## Review độc lập lượt 8 · Issue #646

Đặc tả r1, SHA-256 `0c9c005b9e044dbea41463ebf6754f3dd8bdcb650f8d73999192150f5b80c27c`. Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout ở detached HEAD, trùng OID của `master`. Đặc tả và các bản lịch sử là tệp untracked được giao để review.

Reviewer thuộc họ OpenAI, chạy Codex với shell cục bộ và trả verdict qua stdout. Model và effort phục vụ chưa đo được. Rig chạy trong `/dev/shm` với Git 2.43.0 và Python 3.13.18. Một lần dựng rig kế thừa cấu hình ký commit và bị sandbox chặn kết nối loopback. Các phép đo Git sau đó dùng cấu hình cô lập và tắt ký commit. Worktree giữ nguyên.

## Finding lượt 7

| Finding | Trạng thái | Bằng chứng lượt 8 |
|---|---|---|
| P2 · Gitlink ngoài write set lọt dưới `diff.ignoreSubmodules=all` | Đóng | Cùng fixture, N1 bản 7 `rc=0`, N1 hiện tại `rc=1` tại (a), raw diff hiện `000000 → 160000`. N5 `rc=0` vì blob tài liệu đúng. |
| P3 · `* -diff` làm H đúng đỏ oan | Đóng | Với `.git/info/attributes` chứa `* -diff`, N1 bản 7 `rc=1`, N1 hiện tại `rc=0`, báo `14 0`. N5 `rc=0`. |
| P3 · §6 ghi số lượt | Đóng | §6 ghi mốc đến hết lượt 7, bảy `request_changes`, và yêu cầu lấy lại số từ biên nhận tại thời điểm hỏi E2. Lượt hiện tại là lượt 8. |

## Finding mới

| Mức | Finding | Phản chứng đã chạy |
|---|---|---|
| **P2** | **N1 chấp nhận sai cây của exact OID khi có commit replacement.** [N1, dòng 249](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP3/ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md:249) | Dựng `H_bad` chứa khối đúng và tệp `extra` ngoài write set. `git --no-replace-objects diff-tree -r --raw B H_bad` hiện hai dòng, gồm `A extra`. Chạy `git replace H_bad H_good`, rồi `bash n1.sh B H_bad n5.py` trả **`rc=0`, `N1 DAT`, `14 0`**. N5 cũng `rc=0` trên blob tài liệu. Giữ nguyên hai OID và chạy lại với `GIT_NO_REPLACE_OBJECTS=1` thì N1 trả `rc=1` và hiện `A extra`. Cần vô hiệu hóa replacement trên toàn bộ đường đọc Git của N1 và đường trích blob cho N5. |
| P3 | **Cam kết độc lập với môi trường Git rộng hơn hành vi đã đo.** [N1, dòng 185](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP3/ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md:185) | H đúng cho N1 `rc=0` ở đối chứng. Đặt `GIT_DIR` trỏ tới thư mục không tồn tại, hoặc đặt repo-local `core.abbrev=bogus`, thì cùng B/H cho `rc=1`. Cả hai bị báo là base thiếu tệp dù stderr lần lượt chỉ ra lỗi định vị repo và lỗi cấu hình. Cần xác định nguồn repo được ghim và báo đúng lỗi môi trường. |

Không phát hiện P0 hoặc P1.

## Đột biến và hồi quy

| Bỏ chốt | Ca phân biệt | N1 gốc → đột biến | N5 |
|---|---|---|---|
| (a) So một dòng raw diff | Khối đúng kèm gitlink ngoài write set, dưới `diff.ignoreSubmodules=all` | `1 → 0` | `0` |
| (b) Đòi `14 0` | `git replace` blob H bằng blob có thêm hai dòng ở §5. OID trong tree vẫn là OID kỳ vọng, `cat-file` đọc `16 0` | `1 → 0` | `0` |
| (c) So OID blob kỳ vọng | Chèn đủ 14 dòng ngay trước `## 5.` | `1 → 0` | `1` |

Ca (b) cần blob replacement để phân biệt hai chốt. Với cùng nội dung thêm ở §5 được commit bình thường, bỏ (b) vẫn đỏ nhờ (c). Ca (c) đổi màu riêng N1, còn N5 bắt sai vị trí.

N1 đạt **13/13** ca hồi quy theo §0. N5 đạt **31/31** ca dựng lại. Đổi phép so vùng từ bằng byte sang chứa khối làm đúng năm ca âm chuyển `1 → 0`, còn **26/31**.

## L1–L7

| Luật | Kết quả |
|---|---|
| L1 | Số đếm có đơn vị: dòng, byte, tệp lease, hit và lượt review. |
| L2 | M1–M3 cùng chiếu vào `docs/PROTOCOL_DA_PHIEN.md`, đường dẫn duy nhất trong write set. |
| L3 | N1–N5 có ca làm đỏ. N1 còn phản chứng xanh giả P2 ở trên. |
| L4 | Không áp dụng cho packet này theo §7. §9 lưu lịch sử các vòng sửa đặc tả. |
| L5 | §0 ghi mốc đo, văn bản chèn dẫn tên hàm và tệp. §6 yêu cầu đọc lại số lượt tại điểm hỏi và đo lại §0 trên exact base trước khi viết. |
| L6 | So byte phù hợp với khối đã chốt và bắt cả biến thể xuống dòng. Đo lại `git grep -n -Fw heartbeat_at 641108c -- <tệp>` cho `rc=1` trên từng vị trí trong sáu vị trí §20, và đúng một hit fixture trong hai glob. Bảo đảm exact OID của N1 còn vướng P2. |
| L7 | §6 viện dẫn trần ADR-0055, không đặt trần mềm. Điểm chờ duyệt băm mang mã E2, có mức đã dùng, quyền còn thiếu và mục đích. §5 khai phạm vi E4/E5. |

Trên base, `doctrine-scan` và `adr-song` đều `rc=0` với bằng chứng dương 12 adapter sạch và 66/66 ADR. `doc-claims-check --strict --json` chạy lại với `TMPDIR` trong `/dev/shm` cho `rc=0`, `ok=true` và đúng hai advisory `PATH_MISSING_MIEN_TRU` của protocol. Các đột biến N2/N3 và toàn bộ ma trận N4 chưa được chạy lại trong lượt này. Tình trạng lease và ref từ xa chưa đo.

KET_LUAN: request_changes
tokens used
78,117
## Review độc lập lượt 8 · Issue #646

Đặc tả r1, SHA-256 `0c9c005b9e044dbea41463ebf6754f3dd8bdcb650f8d73999192150f5b80c27c`. Base `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Checkout ở detached HEAD, trùng OID của `master`. Đặc tả và các bản lịch sử là tệp untracked được giao để review.

Reviewer thuộc họ OpenAI, chạy Codex với shell cục bộ và trả verdict qua stdout. Model và effort phục vụ chưa đo được. Rig chạy trong `/dev/shm` với Git 2.43.0 và Python 3.13.18. Một lần dựng rig kế thừa cấu hình ký commit và bị sandbox chặn kết nối loopback. Các phép đo Git sau đó dùng cấu hình cô lập và tắt ký commit. Worktree giữ nguyên.

## Finding lượt 7

| Finding | Trạng thái | Bằng chứng lượt 8 |
|---|---|---|
| P2 · Gitlink ngoài write set lọt dưới `diff.ignoreSubmodules=all` | Đóng | Cùng fixture, N1 bản 7 `rc=0`, N1 hiện tại `rc=1` tại (a), raw diff hiện `000000 → 160000`. N5 `rc=0` vì blob tài liệu đúng. |
| P3 · `* -diff` làm H đúng đỏ oan | Đóng | Với `.git/info/attributes` chứa `* -diff`, N1 bản 7 `rc=1`, N1 hiện tại `rc=0`, báo `14 0`. N5 `rc=0`. |
| P3 · §6 ghi số lượt | Đóng | §6 ghi mốc đến hết lượt 7, bảy `request_changes`, và yêu cầu lấy lại số từ biên nhận tại thời điểm hỏi E2. Lượt hiện tại là lượt 8. |

## Finding mới

| Mức | Finding | Phản chứng đã chạy |
|---|---|---|
| **P2** | **N1 chấp nhận sai cây của exact OID khi có commit replacement.** [N1, dòng 249](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP3/ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md:249) | Dựng `H_bad` chứa khối đúng và tệp `extra` ngoài write set. `git --no-replace-objects diff-tree -r --raw B H_bad` hiện hai dòng, gồm `A extra`. Chạy `git replace H_bad H_good`, rồi `bash n1.sh B H_bad n5.py` trả **`rc=0`, `N1 DAT`, `14 0`**. N5 cũng `rc=0` trên blob tài liệu. Giữ nguyên hai OID và chạy lại với `GIT_NO_REPLACE_OBJECTS=1` thì N1 trả `rc=1` và hiện `A extra`. Cần vô hiệu hóa replacement trên toàn bộ đường đọc Git của N1 và đường trích blob cho N5. |
| P3 | **Cam kết độc lập với môi trường Git rộng hơn hành vi đã đo.** [N1, dòng 185](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP3/ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md:185) | H đúng cho N1 `rc=0` ở đối chứng. Đặt `GIT_DIR` trỏ tới thư mục không tồn tại, hoặc đặt repo-local `core.abbrev=bogus`, thì cùng B/H cho `rc=1`. Cả hai bị báo là base thiếu tệp dù stderr lần lượt chỉ ra lỗi định vị repo và lỗi cấu hình. Cần xác định nguồn repo được ghim và báo đúng lỗi môi trường. |

Không phát hiện P0 hoặc P1.

## Đột biến và hồi quy

| Bỏ chốt | Ca phân biệt | N1 gốc → đột biến | N5 |
|---|---|---|---|
| (a) So một dòng raw diff | Khối đúng kèm gitlink ngoài write set, dưới `diff.ignoreSubmodules=all` | `1 → 0` | `0` |
| (b) Đòi `14 0` | `git replace` blob H bằng blob có thêm hai dòng ở §5. OID trong tree vẫn là OID kỳ vọng, `cat-file` đọc `16 0` | `1 → 0` | `0` |
| (c) So OID blob kỳ vọng | Chèn đủ 14 dòng ngay trước `## 5.` | `1 → 0` | `1` |

Ca (b) cần blob replacement để phân biệt hai chốt. Với cùng nội dung thêm ở §5 được commit bình thường, bỏ (b) vẫn đỏ nhờ (c). Ca (c) đổi màu riêng N1, còn N5 bắt sai vị trí.

N1 đạt **13/13** ca hồi quy theo §0. N5 đạt **31/31** ca dựng lại. Đổi phép so vùng từ bằng byte sang chứa khối làm đúng năm ca âm chuyển `1 → 0`, còn **26/31**.

## L1–L7

| Luật | Kết quả |
|---|---|
| L1 | Số đếm có đơn vị: dòng, byte, tệp lease, hit và lượt review. |
| L2 | M1–M3 cùng chiếu vào `docs/PROTOCOL_DA_PHIEN.md`, đường dẫn duy nhất trong write set. |
| L3 | N1–N5 có ca làm đỏ. N1 còn phản chứng xanh giả P2 ở trên. |
| L4 | Không áp dụng cho packet này theo §7. §9 lưu lịch sử các vòng sửa đặc tả. |
| L5 | §0 ghi mốc đo, văn bản chèn dẫn tên hàm và tệp. §6 yêu cầu đọc lại số lượt tại điểm hỏi và đo lại §0 trên exact base trước khi viết. |
| L6 | So byte phù hợp với khối đã chốt và bắt cả biến thể xuống dòng. Đo lại `git grep -n -Fw heartbeat_at 641108c -- <tệp>` cho `rc=1` trên từng vị trí trong sáu vị trí §20, và đúng một hit fixture trong hai glob. Bảo đảm exact OID của N1 còn vướng P2. |
| L7 | §6 viện dẫn trần ADR-0055, không đặt trần mềm. Điểm chờ duyệt băm mang mã E2, có mức đã dùng, quyền còn thiếu và mục đích. §5 khai phạm vi E4/E5. |

Trên base, `doctrine-scan` và `adr-song` đều `rc=0` với bằng chứng dương 12 adapter sạch và 66/66 ADR. `doc-claims-check --strict --json` chạy lại với `TMPDIR` trong `/dev/shm` cho `rc=0`, `ok=true` và đúng hai advisory `PATH_MISSING_MIEN_TRU` của protocol. Các đột biến N2/N3 và toàn bộ ma trận N4 chưa được chạy lại trong lượt này. Tình trạng lease và ref từ xa chưa đo.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T08:57:22Z
