reviewed_sha: e9ac35b358379ebebea558c2ec26086d26b26a4e
verdict: approve
reviewer: codex (OpenAI), codex_cli, read-only

# Packet #1488 r5 · lượt 6

Delta sau lượt 5 không có P0–P2. Hai P3 dưới đây là khoảng trống kiểm thử. HEAD khớp `HEAD_SHA.txt`, cây nguồn sạch trước và sau review. SHA-256 của `wp1488-r5.md` khớp băm đã duyệt `c27e7b6d14422d892e28840897340b1181c1315d5a79fb393e7958ad61967580`.

## Findings

- **P3 — Ca (R) chưa đo việc từ chối kênh khi vắng `GITHUB_PATH`.** `.claude/dev/launcher_test.py:12323` luôn nhận tệp đích do fixture đặt. Đột biến riêng chỉ chạy chốt NUL khi `GITHUB_PATH` khác rỗng vẫn qua ca r1488. Probe dùng kênh `DICH` với NUL ở cuối đường dẫn và bỏ biến đích cho thấy H trả 7, còn bản đột biến lọt tới hậu kiểm và trả 3. Thêm biến thể (R) bỏ biến đích, đòi rc 7, dòng báo riêng và dừng trước hậu kiểm. Biến thể này bắt được đột biến trên.
- **P3 — Ca (R) thiếu payload Windows sai byte nhưng có nhãn hợp lệ.** `.claude/dev/launcher_test.py:12316` đặt NUL trong nhãn Windows. Hai payload sai byte hiện có dùng nhãn POSIX. Đột biến riêng gọi `cygpath -w` trước chốt chỉ khi nhãn Windows hợp lệ và payload chứa sentinel vẫn qua ca r1488. Với `DICH_WIN` + LF + đường dẫn chứa NUL, H trả 7 và không gọi stub. Bản đột biến cũng trả 7, in đúng dòng báo, giữ tệp đích rỗng nhưng có log gọi stub. Thêm payload Windows có NUL hoặc 0x01 vào (R), giữ assertion log. Probe đã bắt được đột biến này.

## Đối chiếu B2/B5

- `ops/cai_cong_cu.sh:245–249` đọc kênh sau retry và chỉ khi `RC_CAI=0`. `cat` mở kênh một lần, `tr` chỉ đọc stdin. Với `pipefail`, lỗi của bất kỳ vế nào bỏ qua `printf x`, làm phép gán thất bại và trả 7. K1 và K2 đo `cat` in đủ rồi lỗi và lỗi không in gì. Probe cho `tr` trả 19 trong cả hai tình huống đều nhận rc 7, dòng báo lỗi đọc và tệp đích rỗng. K3 đếm đúng một lần đọc kênh trên đường thành công.
- Byte NUL trở thành 0x01 trước command substitution. 0x01 vốn có được giữ nguyên. Sentinel `x` giữ LF cuối, rồi chỉ `x` được bỏ. Chốt tại dòng 249 đứng trước dispatch ghi, đổi qua `cygpath -w`, dispatch PATH và hậu kiểm. 0x01 là một ký tự điều khiển ASCII độc lập, không thể là byte đầu hoặc byte tiếp nối của một ký tự UTF-8 nhiều byte hợp lệ. Đường dẫn thử có chữ `đường` qua nguyên văn dưới `C` và `C.UTF-8`.
- Probe `--bat-buoc` qua lượt `source` của công cụ tùy chọn có `chuan_bi: true`: cả nhãn sai dạng theo cách cũ và payload chứa NUL đều trả 7, tệp đích rỗng, không chạy công cụ kế tiếp. B2/B5 quy định rc 7 cho kênh hỏng. Nhánh đi tiếp của công cụ tùy chọn nằm sau đó và áp dụng cho lỗi cài đặt đi qua `RC_CAI`.
- (Q) chỉ bổ sung test, với bốn đầu vào sai dạng và stub ghi dấu nếu bị gọi. Hai đột biến (Q) chết ở đầu vào đầu tiên, khớp §9. §9 cũng đã sửa hai mục r4 sang (I-win). Merge `9390529` có đúng hai cha đã nêu, diff shell so với cha thứ nhất rỗng. Merge ba chiều `launcher_test.py` từ hai cha và merge-base khớp từng byte với blob của merge. Diff theo cha master chỉ có các hunk #1488.
- (R) đo rc, thông báo riêng, byte trong tệp đích và log stub. Trong fixture hiện tại, công thức chỉ ghi kênh, stub chỉ ghi log hoặc in đường dẫn, và nhánh báo kênh hỏng thông thường không có cụm `byte NUL hoac 0x01`. Bỏ chốt cho thấy `R-dich-nul` vẫn trả 7 nhưng đỏ vì thiếu chẩn đoán riêng. Assertion tìm chuỗi con trên stderr tổng hợp nên một đường khác in đúng cụm vẫn có thể thỏa riêng điều kiện này. Không có đường như vậy trong fixture hiện tại. So sánh với dòng chẩn đoán đầy đủ sẽ siết phép đo.
- Bốn đột biến N2 mới phủ chuyển NUL, chốt sentinel, lỗi vế `cat` và thứ tự trước ghi. Chưa có đột biến chuyên biệt cho lỗi vế `tr`, chốt trước PATH khi vắng đích, thứ tự với `cygpath` khi nhãn Windows hợp lệ, hoặc truyền rc 7 qua `source`. Đột biến `wp868_sh_doc_kenh_nuot_loi` có thể nuốt lỗi cả hai vế, nhưng ca đích đỏ hiện tại tiêm lỗi vào `cat`. Các probe riêng đo các đường này trên H.

## Lệnh và mã thoát

- `cat HEAD_SHA.txt`, `git -C repo rev-parse HEAD`, `git --no-optional-locks -C repo status --porcelain`, `sha256sum wp1488-r5.md`, `git clone --no-local -- repo scratch/repo` và `git rev-parse HEAD` trong clone đều rc 0.
- Các `git diff` đọc delta đã nêu, `git show` đọc bốn blob, `git merge-base 210ceff d0868db`, `git merge-file -p` trên bản sao và `cmp` với blob merge đều rc 0. `git diff --exit-code` cho shell qua merge rc 0. `git diff --check 9390529 e9ac35b` và kiểm tra cùng loại cho shell, test và RESULTS ở bước Q đều rc 0. Kiểm tra whitespace rộng hơn từ lượt 5 tới H trả 2 do dòng trống cuối bản lưu VERDICT và whitespace trong tài liệu nhập từ master. Lần đối chiếu merge đầu dùng process substitution cho `merge-file` tạo đầu ra rỗng nên `cmp` trả 1. Phép đối chiếu đã được chạy lại với tệp thường.
- `bash -n scratch/repo/ops/cai_cong_cu.sh` rc 0. Môi trường Linux, Bash 5.2.21, Python 3.13.18.

| Lệnh trong `scratch/repo` | rc | Kết quả |
|---|---:|---|
| `python .claude/dev/launcher_test.py --lap-ca r1488_github_path_chi_ghi_khi_thanh_cong --lan 2` | 0 | 2/2 |
| `python .claude/dev/launcher_test.py --lap-ca r858_hinh_dang_cong_thuc_cai --lan 1` | 0 | 1/1 |
| `python .claude/dev/launcher_test.py --lap-ca r868_hinh_dang_kenh_ket_qua --lan 1` | 0 | 1/1 |
| `python .claude/dev/launcher_test.py --lap-ca r868_doc_kenh_hong_thi_dung --lan 1` | 0 | 1/1 |
| `python .claude/dev/launcher_test.py --lap-ca r868_ghi_kenh_hong_thi_dung --lan 1` | 0 | 1/1 |
| `python .claude/dev/launcher_test.py --lap-ca r858_cai_windows_chon_ban_chay_duoc --lan 1` | 0 | 1/1 |
| `TMPDIR="$PWD/.." python -B ../mutants.py` | 0 | Runner ghi kết quả từng bản sao. Mã 0 là của runner, kết quả đỏ là ngoại lệ `TinHieuChotCa`. |
| `TMPDIR="$PWD/.." python -B ../probes.py` | 0 | Sáu probe trên H đạt. |
| `TMPDIR="$PWD/.." python -B ../source_probe.py` | 0 | Hai ca qua lượt source đạt. |
| `TMPDIR="$PWD/.." python -B ../probes.py review_bo_chot_khi_thieu_github_path nul_gp_vang` | 1 | Đỏ vì rc 3 thay vì 7. |
| `TMPDIR="$PWD/.." python -B ../probes.py review_goi_cygpath_truoc_chot_neu_nul_trong_duong_dan_win nul_win_dans_chemin` | 1 | Đỏ vì có log `cygpath`. |

Mỗi đột biến dưới đây được áp riêng, với đúng một vị trí khớp neo trong script nguồn. Các tên trong cột phải là assertion đầu tiên của ca r1488, trừ hàng cuối.

| Đột biến | Điểm đỏ đầu tiên |
|---|---|
| `wp1488_sh_bo_tr_nul` | R-dich-nul, rc 0 và có dòng ghi |
| `wp1488_sh_bo_chot_nul` | R-dich-nul, rc 7 nhưng thiếu dòng báo riêng |
| `wp1488_sh_pipeline_nuot_loi_cat` | K1, rc 0 sau lỗi đọc |
| `wp1488_sh_chot_nul_sau_ghi` | R-nul-giua, tệp đích đã bị ghi |
| `wp1488_sh_path_nhan_hau_to` | Q-win-hau-to, rc 3 |
| `wp1488_sh_ghi_nhan_long` | Q-win-hau-to, rc 1 và có gọi `cygpath` |
| `wp1488_sh_doc_kenh_cu_ghi_muon` | C, ghi đường dẫn từ lượt cũ |
| `wp1488_sh_doc_kenh_rieng_truoc` | L-LF, ghi đường dẫn dù payload có LF |
| `wp1488_sh_doc_kenh_hai_lan` | K3, đếm hai lần đọc |
| `wp868_sh_doc_kenh_nuot_loi` | `r868_doc_kenh_hong_thi_dung`, rc 0 và probe sau đọc đã chạy. Ca hình dạng cũng đỏ. |

## Chưa đo

Chưa chạy toàn bộ suite và toàn bộ mutation trên hai vế N3, CI PR của H cục bộ, hay doctrine-scan N4. Ca Windows dùng stub trên Linux, chưa đo Git Bash/Windows thật hoặc các locale khác ngoài hai locale trên. Các kết quả và bản sao làm việc nằm trong `scratch/`. Lượt chạy baseline đầu tiên dùng thư mục tạm mặc định của harness, được harness tự dọn. Lượt xác nhận lại đặt `TMPDIR` dưới `scratch/`.
