reviewed_sha: 4cd2ba29acdb1fba5eac2267a17d049fa0880a41
verdict: approve
reviewer: codex (OpenAI), codex_cli, read-only

# Packet #1488 r5 · lượt 7

## Findings

Không có finding P0–P3 mới trong delta. Hai P3 của lượt 6 đã đóng.

- `.claude/dev/launcher_test.py:12332` bỏ `GITHUB_PATH` khỏi môi trường của lần gọi shell thực tế. `R-gp-vang` đòi rc 7, đúng cả dòng chẩn đoán và dừng trước hậu kiểm. Đột biến chỉ chốt khi có đích trả rc 3 ở chính ca này.
- `.claude/dev/launcher_test.py:12321` thêm nhãn `DICH_WIN` hợp lệ với NUL hoặc 0x01 trong đường dẫn. Ca đòi rc 7, đúng cả dòng chẩn đoán, tệp đích rỗng và không có log `cygpath`. Đột biến gọi `cygpath -w` sớm vẫn trả rc 7 và in dòng báo riêng, nhưng log làm ca đỏ. Trong fixture này, công thức chỉ ghi kênh và stub chỉ ghi log hoặc in đường dẫn. Bỏ chốt làm ca đỏ ngay cả khi nhánh báo sai dạng vẫn trả rc 7.

## Đối chiếu delta và B2/B5

HEAD khớp `HEAD_SHA.txt`, cây nguồn sạch, SHA-256 của spec khớp băm đã duyệt `c27e7b6d14422d892e28840897340b1181c1315d5a79fb393e7958ad61967580`. Cha trực tiếp là `e9ac35b358379ebebea558c2ec26086d26b26a4e`. Commit chỉ sửa `.claude/dev/launcher_test.py`. Shell giống từng byte với lượt 6. Ca (Q) và nội dung đã nhập từ master nằm ngoài delta lượt 7. Hai đột biến của (Q) vẫn đỏ đúng ca.

Ở `ops/cai_cong_cu.sh:245–249`, `cat` mở kênh một lần, `tr` đọc stdin. `pipefail` giữ lỗi của cả hai vế, kể cả khi đã in đủ dữ liệu. Hai ca K1/K2 đo lỗi `cat`, K3 đo số lần đọc trên đường thành công. Probe lượt này tiêm lỗi `tr` cả khi không in và khi chuyển tiếp đủ dữ liệu, đều nhận rc 7, báo lỗi đọc và tệp đích rỗng. Chốt bắt NUL đã chuyển thành 0x01 và byte 0x01 có sẵn trước dispatch ghi, gọi `cygpath` hoặc đổi PATH. Byte 0x01 là ký tự ASCII độc lập, không thể nằm trong chuỗi byte của một ký tự UTF-8 nhiều byte hợp lệ. `exit 7` trong lượt `source` giữ cùng cơ chế thoát như nhánh kênh sai dạng cũ. Đường này đã được đo ở lượt 6.

## Lệnh và mã thoát

- `cat HEAD_SHA.txt`, `git -C repo rev-parse HEAD`, `git -C repo rev-parse HEAD^`, `git --no-optional-locks -C repo status --porcelain`, phép so HEAD với tệp và `sha256sum -c` đều rc 0.
- `git -C repo diff e9ac35b HEAD`, `git -C repo diff --name-only e9ac35b HEAD`, `git -C repo diff --check e9ac35b HEAD`, `git -C repo diff --exit-code e9ac35b HEAD -- ops/cai_cong_cu.sh` đều rc 0.
- `git -C repo diff --exit-code 210ceff 9390529 -- ops/cai_cong_cu.sh` và hai lệnh `git diff --stat` cho test qua merge và bước (Q) đều rc 0.
- `git clone --no-local -- repo scratch/review7`, `git rev-parse HEAD` trong clone và `bash -n scratch/review7/ops/cai_cong_cu.sh` đều rc 0. Môi trường Linux, Bash 5.2.21, Python 3.13.18.

Các lệnh sau chạy trong `scratch/review7` với `TMPDIR="$PWD/.."`.

| Lệnh | rc | Kết quả |
|---|---:|---|
| `python .claude/dev/launcher_test.py --lap-ca r1488_github_path_chi_ghi_khi_thanh_cong --lan 2` | 0 | 2/2 |
| `python .claude/dev/launcher_test.py --lap-ca r858_hinh_dang_cong_thuc_cai --lan 1` | 0 | 1/1 |
| `python .claude/dev/launcher_test.py --lap-ca r868_hinh_dang_kenh_ket_qua --lan 1` | 0 | 1/1 |
| `python .claude/dev/launcher_test.py --lap-ca r868_doc_kenh_hong_thi_dung --lan 1` | 0 | 1/1 |
| `python .claude/dev/launcher_test.py --lap-ca r868_ghi_kenh_hong_thi_dung --lan 1` | 0 | 1/1 |
| `python .claude/dev/launcher_test.py --lap-ca r858_cai_windows_chon_ban_chay_duoc --lan 1` | 0 | 1/1 |
| `python -B ../review7-tr.py` | 0 | Hai probe, shell rc 7 ở cả hai |
| `python -B ../review7-mutants.py` | 0 | 12 đột biến trong bảng và một đột biến riêng đều bị bắt |

Runner áp từng đột biến trên một tệp shell riêng trong `scratch/`, kiểm neo khớp đúng một lần và chạy các ca đích. Mã 0 là của runner. Điểm đỏ ghi dưới đây là assertion đầu tiên (`TinHieuChotCa`), không phải lỗi chạy harness. Tất cả các hàng trừ `wp868_sh_doc_kenh_nuot_loi` dùng ca r1488.

| Đột biến | Điểm đỏ đầu tiên |
|---|---|
| `wp1488_sh_doc_kenh_cu_ghi_muon` | C, ghi đường dẫn của lượt cũ |
| `wp1488_sh_doc_kenh_rieng_truoc` | L-LF, ghi đường dẫn dù payload có LF |
| `wp1488_sh_doc_kenh_hai_lan` | K3, đếm hai lần đọc |
| `wp1488_sh_path_nhan_hau_to` | Q-win-hau-to, rc 3 |
| `wp1488_sh_ghi_nhan_long` | Q-win-hau-to, rc 1 và có log `cygpath` |
| `wp1488_sh_bo_tr_nul` | R-dich-nul, rc 0 và có dòng ghi |
| `wp1488_sh_bo_chot_nul` | R-dich-nul, rc 7 nhưng thiếu chẩn đoán riêng |
| `wp1488_sh_pipeline_nuot_loi_cat` | K1, rc 0 sau lỗi đọc |
| `wp1488_sh_chot_nul_chi_khi_co_dich` | **R-gp-vang**, rc 3 ở hậu kiểm |
| `wp1488_sh_cygpath_truoc_chot_nul` | **R-win-nul-giua**, rc 7 và tệp đích rỗng nhưng có log `cygpath` |
| `wp1488_sh_chot_nul_sau_ghi` | R-nul-giua, tệp đích đã bị ghi |
| `wp868_sh_doc_kenh_nuot_loi` | `r868_doc_kenh_hong_thi_dung`, rc 0 và đã chạy probe sau đọc. `r868_hinh_dang_kenh_ket_qua` cũng đỏ. |
| `review7_cygpath_chi_khi_duong_dan_win_co_byte_hong` | R-win-nul-giua. Đột biến riêng chỉ gọi sớm khi nhãn Windows hợp lệ và payload chứa sentinel. Log bắt được lời gọi. |

## Chưa đo

Trong tập đột biến có sẵn đã chọn, chưa có đột biến chuyên biệt cho lỗi vế `tr`, đổi PATH nội bộ trước chốt mà vẫn trả 7, hoặc truyền rc 7 qua lượt `source`. Probe riêng ở lượt này đo lỗi `tr`. Đối chiếu lượt 6 bao gồm phép thử `source` và UTF-8 dưới `C` và `C.UTF-8`. Lượt 7 không chạy lại toàn bộ suite, CI, doctrine-scan, hoặc Windows/Git Bash thật. Các ca Windows chạy bằng stub trên Linux.
