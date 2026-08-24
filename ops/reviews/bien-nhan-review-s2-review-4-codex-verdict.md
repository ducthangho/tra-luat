verdict: changes_requested
reviewed_sha: 8b627e843a3be87f2ceac97f2f147bbadcaa3cdc

## DOI CHIEU BON FINDING DA VA
- bn-verdict-path-ngoai-cay: ĐÃ VÁ THẬT — đột biến bỏ chốt đường tuyệt đối và phép neo đích đã làm cả `bien_nhan_verdict_path_TUYET_DOI_khong_duoc_dem` lẫn `bien_nhan_verdict_path_SYMLINK_ra_ngoai_khong_duoc_dem` ĐỎ (rc thực 0, kỳ vọng 11); các đối chứng verdict mồ côi và packet slug vẫn XANH trong phép đo tách lớp.
- bn-thieu-sha-dem-theo-tep: ĐÃ VÁ THẬT — đột biến cho nhánh thiếu SHA dùng tên tệp làm khóa khiến `bien_nhan_thieu_sha_nhieu_ban_van_dem_MOT` ĐỎ (rc thực 0, kỳ vọng 11).
- bn-sha-rac-dem-theo-gia-tri: ĐÃ VÁ THẬT — đột biến cho `_la_dang_commit` luôn trả `True` khiến `bien_nhan_sha_RAC_khong_duoc_lam_khoa_vong` ĐỎ (rc thực 0, kỳ vọng 11), trong khi ca hai SHA hợp dạng khác nhau vẫn XANH.
- bn-nguong-tu-tat-duoc: ĐÃ VÁ THẬT — đột biến hạ sàn để nhận 0 khiến `bien_nhan_nguong_0_hoac_am_bi_CHAN` ĐỎ (0 được nhận với rc=0, kỳ vọng rc=2).

## CHIEU BAT OAN
| ca | kỳ vọng | đo được | khớp? |
|---|---|---|---|
| sha THẬT khác nhau vẫn đếm RIÊNG | qua | ca `bien_nhan_sha_that_van_dem_RIENG` XANH; suite nền rc=0 | có |
| sha rác vẫn tính MỘT vòng hợp lệ | một vòng | vế chiều dương trong `bien_nhan_sha_RAC_khong_duoc_lam_khoa_vong` XANH; suite nền rc=0 | có |
| thiếu sha vẫn tính MỘT vòng | một vòng | vế chiều dương trong `bien_nhan_thieu_sha_nhieu_ban_van_dem_MOT` XANH; suite nền rc=0 | có |
| verdict_path hợp lệ vẫn QUA | qua | `bien_nhan_co_reviewer_thi_QUA` và các fixture `_kho_gia_co_verdict` XANH; suite nền rc=0 | có |

## BANG DO
| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| head được review | 8b627e843a3be87f2ceac97f2f147bbadcaa3cdc | `git -C cay-kho rev-parse HEAD` đúng SHA đầy đủ | có |
| suite clone rời | 253/253 đạt, rc=0 | `nền: 253/253 đạt`, `TỔNG: ĐẠT`, tiến trình rc=0 | có |
| thống kê suite | 63 đột biến, 78 lớp lách, 35 ca bắt-oan, 0 ngoại lệ AC18 | suite tự in đúng 63/78/35/0 | có |
| quy mô diff | 2 tệp, +509/-0 | `git diff --numstat base..HEAD`: 190+319 dòng thêm, 0 xóa, đúng 2 tệp | có |
| bien-nhan packet 298 | rc=11, 0 vòng | chạy trực tiếp cho 0 vòng và rc=11 | có |
| CI tham chiếu packet_loop_test.py | 0 workflow | `rg` trong `.github` không có kết quả | có |
| trạng thái GitHub trực tiếp | KHÔNG ĐO ĐƯỢC | KHÔNG ĐO ĐƯỢC — sandbox chỉ có origin mirror cục bộ; không tái thử REST | KHÔNG ĐO ĐƯỢC |

## HUONG_THU_TOI_KHONG_TU_VIET
- Dựng hai biên nhận hợp lệ cùng trỏ một commit: một biên nhận ghi object ID đầy đủ, biên nhận kia ghi dạng rút gọn của chính object ID đó; yêu cầu `--toi-thieu 2` phải ĐỎ vì chỉ có một vòng. Tôi không tự viết fixture này theo ràng buộc của lượt 4.

### bn-sha-viet-tat-nhan-doi-vong  [P1]  Một commit có thể được đếm thành hai vòng bằng hai cách biểu diễn SHA
TỆP/DÒNG: `cay-kho/.claude/dev/packet_loop.py:1510`, `cay-kho/.claude/dev/packet_loop.py:1663` · VẤN ĐỀ: `_la_dang_commit` chấp mọi hex dài 7..64, còn khóa vòng là nguyên chuỗi đã hạ chữ. Vì vậy object ID đầy đủ và bản rút gọn hợp lệ của chính nó là hai khóa khác nhau dù cùng neo một commit; ngưỡng vòng có thể được thỏa bằng hai cách viết của một vòng. Suite chỉ thử hai SHA hợp dạng nhưng thực sự khác nhau, chưa thử quan hệ đầy đủ/rút gọn. · ĐÃ THỬ NGHIỆM: đọc đường dữ liệu và rà danh sách ca; không dựng fixture theo lệnh cấm tự soạn chuỗi tấn công. Hướng thử cụ thể đã ghi ở trên; kết quả động: KHÔNG ĐO ĐƯỢC. · ĐỘ TIN: cao về lỗi logic, trung bình về tái hiện động cho đến khi điều phối thêm ca.
