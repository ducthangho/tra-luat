# wp1463 (PR2) — kết quả đo của SPEC r15, lease `wp1463-r15-g3-claude` (lượt 3)
Đo 2026-11-26 08:00Z–08:53Z, phiên cloud Linux, 4 CPU, Python 3.13.18, có `actionlint` và `shellcheck`, trên clone cục bộ của lease (`core.abbrev 7`) tại
commit mang đúng ba tệp mã của PR; base của lease `1260fa0cba89353911e2f97188b2c04dab8139d7`. Mỗi khối là đầu ra NGUYÊN VĂN (stdout) của lệnh ở tiêu đề, `rc=` là mã
thoát. Các lệnh chạy NỐI TIẾP, không lệnh nặng nào chạy song song; giây ở `ab` là giây tường cục bộ (không phải số CI). `ab` dựng hai clone tạm từ clone ấy; `<luu>` trong tiêu đề là thư mục nháp ngoài kho (`/tmp/wp1463-g3/luu2` trong khối `registry`). Tệp đã chạy:
- `ops/ci_provenance_test.py` sha256 `8eaa12ea2bc7076f6d3f3db75b5208e0e47f12a4462d7b6a0dc223c9714db81f`
- `.claude/dev/ci_dang_ky_test.py` sha256 `92516f3f45fef47bfee810a26f53bd1f36724af0cd0d0e0a95ab629b6cc834d2`
- script đo `ops/specs/wp1463-r1/do/do_pr2.py` sha256 `093dccfb996abb8f97505b7170951b1188bc6c5162fa2a23f376762e107d5d78`
## `do_pr2.py ab 1260fa0cba89353911e2f97188b2c04dab8139d7 --luu <luu>` (Nghiệm thu 1, 2, 5; R15-1)
```
SHA256 ops/ci_provenance_test.py: 8eaa12ea2bc7076f6d3f3db75b5208e0e47f12a4462d7b6a0dc223c9714db81f
SHA256 .claude/dev/ci_dang_ky_test.py: 92516f3f45fef47bfee810a26f53bd1f36724af0cd0d0e0a95ab629b6cc834d2
AB base=1260fa0cba89353911e2f97188b2c04dab8139d7 blob ops/ci_provenance.py base=2b2b9218892814e94c0ad95fe3bae77d41edd5fe H=2b2b9218892814e94c0ad95fe3bae77d41edd5fe (H = HEAD cua kho do, khong ghi o day)
LUOT base day_du: rc=0 · 626.4 s · TIEN TRINH: 4 · CPU 4
  CA: 77/77 dat · DOT BIEN: 485/485 bi giet dung ly do · TU KIEM PHAN HANG: DAT (2 dot bien) · TONG: DAT
LUOT H day_du: rc=0 · 657.9 s · TIEN TRINH: 4 · CHE DO: day_du · CPU 4
  CA: 86/86 dat · DOT BIEN: 524/524 bi giet dung ly do · TU KIEM PHAN HANG: DAT (2 dot bien) · TONG: DAT
LUOT H nhe: rc=0 · 150.4 s · TIEN TRINH: 4 · CHE DO: nhe · CPU 4
  CA: 86/86 dat · DOT BIEN: 524 muc CHE DO NHE — do khi diff cham vung · TU KIEM PHAN HANG: DAT (2 dot bien) · TONG: DAT
KE HOACH DOT BIEN: base 485 viec · H 524 viec · ten base ⊆ H: True
PHEP ca_bo_day_du: DUNG
PHEP cung_bang: DUNG
PHEP khong_thieu_ten: DUNG
PHEP ast_phan_hang: DUNG
PHEP luoi_phan_hang: DUNG
PHEP cung_blob_san_pham: DUNG
PHEP cong_thuc_cu_dong: DUNG
PHEP tong_hai_chieu: DUNG
PHEP kho_va_ben_doc_cu: DUNG
RC_LUOT: base/day_du=0 · H/day_du=0 · H/nhe=0 (ca ba phai bang 0)
KET_LUAN_AB: DAT (9/9 phep dung)
rc=0
```
## `do_pr2.py registry --tu <luu>` (Nghiệm thu 3)
```
REGISTRY dau ra nhe / ke hoach nhe: ĐẠT (mong ĐẠT) · CI_DANG_KY ops/ci_provenance_test.py: ĐẠT rc=0
REGISTRY dau ra day_du / ke hoach day_du: ĐẠT (mong ĐẠT) · CI_DANG_KY ops/ci_provenance_test.py: ĐẠT rc=0
REGISTRY dau ra day_du / ke hoach nhe: ĐỎ (mong ĐỎ) · CI_DANG_KY ops/ci_provenance_test.py: chế độ nhẹ mà VẪN in dòng đột biến ĐỦ — cờ nhẹ không có tác dụng | CI_DANG_KY ops/ci_provenance_test.py: ĐỎ rc=0
REGISTRY dau ra nhe / ke hoach day_du: ĐỎ (mong ĐỎ) · CI_DANG_KY ops/ci_provenance_test.py: ĐỎ rc=0
KET_LUAN_REGISTRY: DAT (dau ra doc tu /tmp/wp1463-g3/luu2)
rc=0
```
## `do_pr2.py vung --luu <thư mục nháp khác>` trên H (Nghiệm thu 4; R15-3, R15-4)
```
SHA256 ops/ci_provenance_test.py: 8eaa12ea2bc7076f6d3f3db75b5208e0e47f12a4462d7b6a0dc223c9714db81f
SHA256 .claude/dev/ci_dang_ky_test.py: 92516f3f45fef47bfee810a26f53bd1f36724af0cd0d0e0a95ab629b6cc834d2
PHEP bo_day_du: SACH · rc=0 · (1) khac rong=True · (2) nhan chung ops/ci_provenance.py=True · (3) ngoai vung=[] · Python con/dong khoi dong con=610/610
  tap (5): ['.claude/dev/ci_dang_ky_test.py', '.github/workflows/ops-do-workflow-definition.yml', 'ops/bash_nen.py', 'ops/ci_provenance.py', 'ops/ci_provenance_test.py']
  khoi cuoi: ['CA: 86/86 dat', 'DOT BIEN: 524/524 bi giet dung ly do', 'TU KIEM PHAN HANG: DAT (2 dot bien)', 'TONG: DAT']
PHEP phan_chung_nguyen: SACH · rc=0 · (1) khac rong=True · (2) nhan chung .github/workflows/ci.yml=True · (3) ngoai vung=[] · Python con/dong khoi dong con=79/91
  tap (7): ['.claude/dev/ci_dang_ky_test.py', '.github/workflows/ci-dot-bien-du.yml', '.github/workflows/ci.yml', '.github/workflows/launcher-windows.yml', 'ops/bash_nen.py', 'ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json', 'ops/specs/wp1460-r1/hop_dong/fixture.json']
  danh tinh: che_do=nguyen truoc={'NHE': True, 'MAU_DAY_DU': True, 'MAU_NHE': True, 'VUNG_THEM': True, 'so_vung_them': 7} sau={'NHE': True, 'MAU_DAY_DU': True, 'MAU_NHE': True, 'VUNG_THEM': True, 'so_vung_them': 7} phan_chung=True hang=30/30
PHEP phan_chung_go_bon_khoa: SACH · rc=0 · (1) khac rong=True · (2) nhan chung .github/workflows/ci.yml=True · (3) ngoai vung=[] · Python con/dong khoi dong con=79/91
  tap (7): ['.claude/dev/ci_dang_ky_test.py', '.github/workflows/ci-dot-bien-du.yml', '.github/workflows/ci.yml', '.github/workflows/launcher-windows.yml', 'ops/bash_nen.py', 'ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json', 'ops/specs/wp1460-r1/hop_dong/fixture.json']
  danh tinh: che_do=go_bon_khoa truoc={'NHE': True, 'MAU_DAY_DU': True, 'MAU_NHE': True, 'VUNG_THEM': True, 'so_vung_them': 7} sau={'NHE': False, 'MAU_DAY_DU': False, 'MAU_NHE': False, 'VUNG_THEM': False, 'so_vung_them': 0} phan_chung=True hang=30/30
GIOI_HAN_VUNG (SPEC r15 R15-4, bao dam GIAM, chu kho chap nhan): Python con chi duoc DEM khi NHAN RA DUOC — exe/argv[0] co ten co so khop python[0-9.]*(\.exe)?$ hoac realpath trung trinh thong dich dang chay; ban sao/ban doi ten cua trinh thong dich chay KHONG hook thi KHONG bi do (PR2-C04, giao packet NO-PR2-VUNG-CAP-HDH).
KET_LUAN_VUNG: SACH
rc=0
```
**Giới hạn của kết luận `vung` (SPEC r15 R15-4, PR2-C04 — bảo đảm GIẢM, chủ kho chấp nhận; lớp `zone-audit-open-coverage-incomplete` KHÔNG ghi `ĐÃ VÁ THẬT`).**
`SACH` chỉ nói: mọi tệp được theo dõi mà hook ĐÃ GHI đều thoả `oracle({x}) == "day_du"`, và số Python con NHẬN RA ĐƯỢC (đúng hàm `la_python`: `exe`
hoặc `argv[0]` có tên cơ sở khớp `python[0-9.]*(\.exe)?$`, hoặc realpath trùng trình thông dịch đang chạy `vung`) không vượt số lần hook khởi động.
CÒN HỞ: Python con chạy từ BẢN SAO/BẢN ĐỔI TÊN của trình thông dịch mà không hook (`-I`/`-S`/`-E`, môi trường bị xoá) KHÔNG được đếm và KHÔNG bị đo —
review mã lượt 1 dựng được `SACH` với 0 con / 0 dòng khởi động; mã KHÔNG mở rộng biểu thức tên (mở rộng tạo cảm giác an toàn giả); việc đo vùng ở cấp
hệ điều hành giao packet `NO-PR2-VUNG-CAP-HDH`. Các giới hạn cũ giữ nguyên: tiến trình không phải Python, Python gọi qua shell, lần đọc không phát sự
kiện audit `open`, Python con không hook bị che bởi dòng khởi động thừa. Thêm giới hạn của bước dọn R15-3: hậu duệ tự rời nhóm tiến trình
(`setsid`/`setpgid`) không bị tín hiệu dọn chạm tới; nếu nó còn giữ ống đầu ra thì hàm báo `DON KHONG HET`, nếu nó đã đóng ống thì hàm KHÔNG phát hiện được.
## `do_pr2.py tu-kiem --dot-bien` (gồm trọn các dòng `SO`, `CHAY` của `tu-kiem`)
Véc-tơ theo thứ tự `ca_bo_day_du cung_bang khong_thieu_ten ast_phan_hang luoi_phan_hang cung_blob_san_pham cong_thuc_cu_dong tong_hai_chieu kho_va_ben_doc_cu` (1 = đúng).
```
SO nen_khoe: khai sai [] · vec-to 111111111
SO a_doi_thay_the: khai sai ['ca_bo_day_du'] · vec-to 011111111
SO a_doi_neo: khai sai ['ca_bo_day_du'] · vec-to 011111111
SO a_doi_tien_to_ca_dich: khai sai ['ca_bo_day_du'] · vec-to 011111111
SO a_doi_hang_mong_tu_kiem: khai sai ['ca_bo_day_du'] · vec-to 011111111
SO a_chuyen_bang: khai sai ['cung_bang'] · vec-to 101111111
SO a_thieu_ten_base: khai sai ['kho_va_ben_doc_cu', 'khong_thieu_ten'] · vec-to 110111110
SO b_phan_hang_rc4_HONG: khai sai ['ast_phan_hang', 'luoi_phan_hang'] · vec-to 111001111
SO c_oid_khac: khai sai ['cung_blob_san_pham'] · vec-to 111110111
SO d_dong_dot_bien_tu_so_M_tru_1: khai sai ['cong_thuc_cu_dong', 'kho_va_ben_doc_cu'] · vec-to 111111010
SO d_cu_dot_bien_doi_cho: khai sai ['cong_thuc_cu_dong', 'tong_hai_chieu'] · vec-to 111111001
SO d_bo_tu_kiem_khoi_cu: khai sai ['cong_thuc_cu_dong', 'tong_hai_chieu'] · vec-to 111111001
SO d_cu_tu_kiem_lech_hang_ma_TONG_DAT: khai sai ['kho_va_ben_doc_cu', 'tong_hai_chieu'] · vec-to 111111100
SO d_TONG_DO_tren_nen_khoe: khai sai ['kho_va_ben_doc_cu', 'tong_hai_chieu'] · vec-to 111111100
SO e_them_dong_sau_TONG: khai sai ['kho_va_ben_doc_cu'] · vec-to 111111110
SO e_hang_A3_cua_ten_base_thanh_song: khai sai ['kho_va_ben_doc_cu'] · vec-to 111111110
SO e_dau_ra_nhe_khop_MOI_base: khai sai ['kho_va_ben_doc_cu'] · vec-to 111111110
SO duong_them_muc_moi: khai sai [] · vec-to 111111111
SO duong_phan_hang_doi_khoang_trang_chu_thich: khai sai [] · vec-to 111111111
SO doi_chung_d_phan_tu_ha_tang_cu_GIET: khai sai ['kho_va_ben_doc_cu'] · vec-to 111111110
SO doi_chung_d_phan_tu_ha_tang_cu_TIN_DUNG_GIA: khai sai ['kho_va_ben_doc_cu'] · vec-to 111111110
SO doi_chung_d_phan_tu_ha_tang_cu_SONG_SOT: khai sai ['kho_va_ben_doc_cu'] · vec-to 111111110
SO doi_chung_d_tu_kiem_het_han_trong_ca: khai sai ['kho_va_ben_doc_cu'] · vec-to 111111110
SO doi_chung_d_thieu_ket_qua_dot_bien: khai sai ['kho_va_ben_doc_cu'] · vec-to 111111110
SO doi_chung_d_E_khac_rong_XANH: khai sai ['kho_va_ben_doc_cu'] · vec-to 111111110
SO doi_chung_d_thieu_tu_kiem_TONG_DO: khai sai ['cong_thuc_cu_dong', 'kho_va_ben_doc_cu'] · vec-to 111111010
TU_KIEM_SO: 26/26 dat · moi phep co dau vao am: True
TU_KIEM_VUNG: 130/130 dat
CHAY ab_rc0_doi_chung: mong (0, 'KET_LUAN_AB: DAT', '9/9') · duoc (0, 'KET_LUAN_AB: DAT', '9/9')
CHAY ab_rc42_base_day_du: mong (1, 'KET_LUAN_AB: DO', '9/9') · duoc (1, 'KET_LUAN_AB: DO', '9/9')
CHAY ab_rc42_H_day_du: mong (1, 'KET_LUAN_AB: DO', '9/9') · duoc (1, 'KET_LUAN_AB: DO', '9/9')
CHAY ab_rc42_H_nhe: mong (1, 'KET_LUAN_AB: DO', '9/9') · duoc (1, 'KET_LUAN_AB: DO', '9/9')
CHAY registry_tu_rc0_doi_chung: mong 0 · duoc 0
CHAY registry_tu_rc42_luot_nhe: mong 1 · duoc 1
CHAY quan_sat_khoe_doi_chung: mong (0, False, ['DA_CHAY chau', 'DA_CHAY con'], ['dau_chau', 'dau_con']) · duoc (0, False, ['DA_CHAY chau', 'DA_CHAY con'], ['dau_chau', 'dau_con'])
CHAY quan_sat_qua_han_con_va_chau_khong_de_dau: mong (None, True, ['DA_CHAY chau', 'DA_CHAY con'], []) · duoc (None, True, ['DA_CHAY chau', 'DA_CHAY con'], [])
TU_KIEM_CHAY: 8/8 dat
DB_SO go_ca_bo_day_du: BAT · a_doi_thay_the: ca_bo_day_du SAI→DUNG; a_doi_neo: ca_bo_day_du SAI→DUNG; a_doi_tien_to_ca_dich: ca_bo_day_du SAI→DUNG; a_doi_hang_mong_tu_kiem: ca_bo_day_du SAI→DUNG
DB_SO go_cung_bang: BAT · a_chuyen_bang: cung_bang SAI→DUNG
DB_SO go_khong_thieu_ten: BAT · a_thieu_ten_base: khong_thieu_ten SAI→DUNG
DB_SO go_ast_phan_hang: BAT · b_phan_hang_rc4_HONG: ast_phan_hang SAI→DUNG
DB_SO go_luoi_phan_hang: BAT · b_phan_hang_rc4_HONG: luoi_phan_hang SAI→DUNG
DB_SO go_cung_blob_san_pham: BAT · c_oid_khac: cung_blob_san_pham SAI→DUNG
DB_SO go_cong_thuc_cu_dong: BAT · d_dong_dot_bien_tu_so_M_tru_1: cong_thuc_cu_dong SAI→DUNG; d_cu_dot_bien_doi_cho: cong_thuc_cu_dong SAI→DUNG; d_bo_tu_kiem_khoi_cu: cong_thuc_cu_dong SAI→DUNG; doi_chung_d_thieu_tu_kiem_TONG_DO: cong_thuc_cu_dong SAI→DUNG
DB_SO go_tong_hai_chieu: BAT · d_cu_dot_bien_doi_cho: tong_hai_chieu SAI→DUNG; d_bo_tu_kiem_khoi_cu: tong_hai_chieu SAI→DUNG; d_cu_tu_kiem_lech_hang_ma_TONG_DAT: tong_hai_chieu SAI→DUNG; d_TONG_DO_tren_nen_khoe: tong_hai_chieu SAI→DUNG
DB_SO go_kho_va_ben_doc_cu: BAT · a_thieu_ten_base: kho_va_ben_doc_cu SAI→DUNG; d_dong_dot_bien_tu_so_M_tru_1: kho_va_ben_doc_cu SAI→DUNG; d_cu_tu_kiem_lech_hang_ma_TONG_DAT: kho_va_ben_doc_cu SAI→DUNG; d_TONG_DO_tren_nen_khoe: kho_va_ben_doc_cu SAI→DUNG
DB_SO d_tinh_cong_thuc_cu_tu_tang_A3: BAT · d_cu_dot_bien_doi_cho: cong_thuc_cu_dong SAI→DUNG; d_cu_dot_bien_doi_cho: tong_hai_chieu SAI→DUNG; e_hang_A3_cua_ten_base_thanh_song: cong_thuc_cu_dong DUNG→SAI; e_hang_A3_cua_ten_base_thanh_song: tong_hai_chieu DUNG→SAI
DB_SO d_so_TONG_bang_dang_thuc_voi_ok_cu: BAT · doi_chung_d_phan_tu_ha_tang_cu_GIET: tong_hai_chieu DUNG→SAI; doi_chung_d_tu_kiem_het_han_trong_ca: tong_hai_chieu DUNG→SAI; doi_chung_d_E_khac_rong_XANH: tong_hai_chieu DUNG→SAI
DB_SO d_du_cu_tren_cu_da_can_theo_ke_hoach: BAT · d_cu_dot_bien_doi_cho: cong_thuc_cu_dong SAI→DUNG; d_cu_dot_bien_doi_cho: tong_hai_chieu SAI→DUNG
DB_SO d_luat_thuan_dung_ok_cu_thay_ok_cu_E: BAT · doi_chung_d_E_khac_rong_XANH: tong_hai_chieu DUNG→SAI
DB_SO d_ok_cu_khong_tinh_duoc_coi_la_True: BAT · d_bo_tu_kiem_khoi_cu: tong_hai_chieu SAI→DUNG
DB_SO d_E_khac_rong_ep_khong_xanh: BAT · doi_chung_d_E_khac_rong_XANH: tong_hai_chieu DUNG→SAI
DB_VUNG probe_dung_rieng_dung_nhan_chung_cua_bo: BAT · thuan_khoe_tap_probe_da_do: mong ('SACH', ('SACH', 'SACH', 'SACH')) duoc ('KHONG_DO_DUOC', ('SACH', 'KHONG_DO_DUOC', 'KHONG_DO_DUOC'))
DB_VUNG hop_tap_luot_du_vao_quan_sat_rong_cua_probe: BAT · thuan_tap_rong_phan_chung_nguyen: mong ('KHONG_DO_DUOC', ('SACH', 'KHONG_DO_DUOC', 'SACH')) duoc ('SACH', ('SACH', 'SACH', 'SACH'))
DB_VUNG bo_chot_song: BAT · thuan_tap_rong_bo_day_du: mong ('KHONG_DO_DUOC', ('KHONG_DO_DUOC', 'SACH', 'SACH')) duoc ('SACH', ('SACH', 'SACH', 'SACH'))
DB_VUNG khong_lan_truyen_hook_sang_tien_trinh_con: BAT · that_doc_con_bo_day_du: mong ('NGOAI_VUNG', ('NGOAI_VUNG', 'SACH', 'SACH')) duoc ('KHONG_DO_DUOC', ('KHONG_DO_DUOC', 'SACH', 'SACH'))
DB_VUNG giai_dir_fd_theo_cwd: BAT · that_doc_dirfd_bo_day_du: mong ('NGOAI_VUNG', ('NGOAI_VUNG', 'SACH', 'SACH')) duoc ('SACH', ('SACH', 'SACH', 'SACH'))
DB_VUNG chi_khop_duong_dan_theo_chu: BAT · that_doc_symlink_bo_day_du: mong ('NGOAI_VUNG', ('NGOAI_VUNG', 'SACH', 'SACH')) duoc ('SACH', ('SACH', 'SACH', 'SACH'))
DB_VUNG bo_dem_python_con: BAT · that_con_I_bo_day_du: mong ('KHONG_DO_DUOC', ('KHONG_DO_DUOC', 'SACH', 'SACH')) duoc ('SACH', ('SACH', 'SACH', 'SACH'))
DB_VUNG bo_rc: BAT · that_rc_sau_bo_day_du: mong ('KHONG_DO_DUOC', ('KHONG_DO_DUOC', 'SACH', 'SACH')) duoc ('SACH', ('SACH', 'SACH', 'SACH'))
DB_VUNG tap_phep_chi_so_so_luong: BAT · thuan_tap_phep_lap: mong KHONG_DO_DUOC duoc SACH
DB_VUNG chay_mot_phep_hai_lan_thay_cho_phep_khac: BAT · that_khoe: mong ('SACH', ('SACH', 'SACH', 'SACH')) duoc ('KHONG_DO_DUOC', ('SACH', 'SACH', 'KHONG_DO_DUOC'))
DB_VUNG bo_so_mot_hang_nhung_van_dem: BAT · thuan_hang_lech_phan_chung_nguyen_wf_wd: mong ('KHONG_DO_DUOC', ('SACH', 'KHONG_DO_DUOC', 'SACH')) duoc ('SACH', ('SACH', 'SACH', 'SACH'))
DB_VUNG phep_go_chay_ban_nap_cua_phep_khac: BAT · that_khoe: mong ('SACH', ('SACH', 'SACH', 'SACH')) duoc ('KHONG_DO_DUOC', ('SACH', 'SACH', 'KHONG_DO_DUOC'))
DB_VUNG go_khong_go_khoa: BAT · that_khoe: mong ('SACH', ('SACH', 'SACH', 'SACH')) duoc ('KHONG_DO_DUOC', ('SACH', 'SACH', 'KHONG_DO_DUOC'))
DB_VUNG phan_loai_bo_realpath: BAT · that_la_python_realpath_trung: mong True duoc False
DB_VUNG phan_loai_nhan_moi_ten: BAT · that_la_python_ban_sao_doi_ten_KHONG_nhan_ra: mong False duoc True
DB_VUNG hook_chi_cai_theo_ten_trinh_thong_dich: BAT · that_doc_con_doi_ten_bo_day_du: mong ('NGOAI_VUNG', ('NGOAI_VUNG', 'SACH', 'SACH')) duoc ('SACH', ('SACH', 'SACH', 'SACH'))
DB_CHAY ab_bo_chot_rc_luot_base_day_du: BAT · ab_rc42_base_day_du: mong (1, 'KET_LUAN_AB: DO', '9/9') duoc (0, 'KET_LUAN_AB: DAT', '9/9')
DB_CHAY ab_bo_chot_rc_luot_H_day_du: BAT · ab_rc42_H_day_du: mong (1, 'KET_LUAN_AB: DO', '9/9') duoc (0, 'KET_LUAN_AB: DAT', '9/9')
DB_CHAY ab_bo_chot_rc_luot_H_nhe: BAT · ab_rc42_H_nhe: mong (1, 'KET_LUAN_AB: DO', '9/9') duoc (0, 'KET_LUAN_AB: DAT', '9/9')
DB_CHAY registry_tu_mac_dinh_rc_0: BAT · registry_tu_rc42_luot_nhe: mong 1 duoc 0
DB_CHAY quan_sat_bo_buoc_don: BAT · quan_sat_qua_han_con_va_chau_khong_de_dau: mong (None, True, ['DA_CHAY chau', 'DA_CHAY con'], []) duoc (None, True, ['DA_CHAY chau', 'DA_CHAY con'], ['dau_chau', 'dau_con'])
DB_CHAY quan_sat_chi_ket_thuc_con_khong_ket_thuc_nhom: BAT · quan_sat_qua_han_con_va_chau_khong_de_dau: mong (None, True, ['DA_CHAY chau', 'DA_CHAY con'], []) duoc (None, True, ['DA_CHAY chau', 'DA_CHAY con'], ['dau_chau'])
DOT_BIEN_TU_KIEM: 37/37 bi bat dung cho (15 cua bo so, 16 cua phep do vung, 6 cua bo chay)
KET_LUAN_TU_KIEM: DAT
rc=0
```
`do_pr2.py tu-kiem`: `TU_KIEM_SO: 26/26 dat · moi phep co dau vao am: True · TU_KIEM_VUNG: 130/130 dat · TU_KIEM_CHAY: 8/8 dat · KET_LUAN_TU_KIEM: DAT · rc=0`.
## R15-1 … R15-4: ca khoá, đột biến riêng, kết quả đo
- **R15-1** (`ab` đòi rc 0 ở cả ba lượt). Ca khoá (`tu-kiem`, nhóm `CHAY`, gọi `do_ab` THẬT với bộ chạy giả trả đầu ra KHOẺ kèm rc 42 ở đúng một ranh giới):
  `ab_rc42_base_day_du`, `ab_rc42_H_day_du`, `ab_rc42_H_nhe` ⇒ lệnh rc 1, `KET_LUAN_AB: DO`, chín phép vẫn 9/9; đối chứng `ab_rc0_doi_chung` ⇒ rc 0, `DAT`.
  Đột biến `ab_bo_chot_rc_luot_base_day_du`, `…_H_day_du`, `…_H_nhe`: mỗi cái `BAT` ở đúng ca của lượt ấy (`DO`→`DAT`). Quét cùng lớp: `registry --tu` đọc rc
  ĐÃ LƯU (`<luu>/H.<chế độ>.rc`) thay vì mặc định 0 — ca `registry_tu_rc42_luot_nhe` (đối chứng `registry_tu_rc0_doi_chung`), đột biến `registry_tu_mac_dinh_rc_0` `BAT`.
  Lượt thật ở khối `ab`: dòng `RC_LUOT` in rc của cả ba lượt.
- **R15-2** (chốt 65 536 BYTE của bộ kiểm kết quả con). Ca khoá `c82_tang_thuc_thi_ca_va_con`: véc-tơ 29 = kết quả HỢP LỆ đệm khoảng trắng cuối tới đúng 65 537
  byte ⇒ `infrastructure_error`; đối chứng véc-tơ 5 = cùng kết quả đúng 65 536 byte ⇒ `hoan_tat`; ca tự khẳng định độ dài byte của hai véc-tơ; qua CẢ HAI bộ
  chạy cha. Đột biến `T47_R15_2_bo_kiem_bo_chot_kich_thuoc` và `T48_R15_2_bo_kiem_doc_65536_thay_65537`: trong lượt đủ THẬT trên H (khối `ab`) cả hai
  `trang_thai_thuc_thi` = `hoan_tat`, `phan_hang_dot_bien` = `giet` (đọc từ dòng `KET_CUC_A3` của `<luu>/H.day_du.out`). Chi tiết lý do chết, đo riêng bằng
  script nháp ngoài kho gọi `chay_dot_bien_test` của chính tệp test (in `tên => (hạng, đuôi đầu ra con, trạng thái)`):
```
T47_R15_2_bo_kiem_bo_chot_kich_thuoc => ('GIET', 'DO:c82_tang_thuc_thi_ca_va_con:chay_con véc-tơ 29: mong infrastructure_error, được hoan_tat (rc 0)', 'hoan_tat')
T48_R15_2_bo_kiem_doc_65536_thay_65537 => ('GIET', 'DO:c82_tang_thuc_thi_ca_va_con:chay_con véc-tơ 29: mong infrastructure_error, được hoan_tat (rc 0)', 'hoan_tat')
```
- **R15-3** (`chay_quan_sat` sở hữu và dọn nhóm tiến trình nó sinh). Ca khoá `quan_sat_qua_han_con_va_chau_khong_de_dau` (con THẬT và cháu THẬT cùng hẹn ghi dấu
  2 s sau khi khởi động, hạn 2 s): hàm trả `(None, None, "LOI_CHAY: TimeoutExpired…")`, đầu ra đã bắt còn đủ hai dòng `DA_CHAY`, và 4,5 s sau khi khởi động KHÔNG có dấu nào;
  đối chứng `quan_sat_khoe_doi_chung` ⇒ rc 0 và đủ hai dấu. Đột biến `quan_sat_bo_buoc_don` ⇒ hai dấu `dau_chau`, `dau_con` xuất hiện (`BAT`);
  `quan_sat_chi_ket_thuc_con_khong_ket_thuc_nhom` ⇒ dấu `dau_chau` xuất hiện (`BAT`). Nền không có nhóm tiến trình kiểu POSIX: ca ghi `KHONG_DO_DUOC` (lệch kỳ vọng ⇒ `tu-kiem` ĐỎ), không giả ĐẠT.
- **R15-4** (bảo đảm giảm; không mở rộng biểu thức tên). Ca khoá: (a) `thuan_la_python_exe_*`, `thuan_la_python_argv0_*` cho `python`, `python3`, `python3.13`,
  `python.exe` ⇒ nhận; `that_la_python_realpath_trung` (symlink tên khác trỏ trình thông dịch đang chạy) ⇒ nhận; `thuan_la_python_tu_choi_ten_khac`,
  `that_la_python_ban_sao_doi_ten_KHONG_nhan_ra` ⇒ từ chối. (b) `that_doc_con_doi_ten_<phép>` ở cả ba phép: bản sao đổi tên CÓ hook đọc tệp được theo dõi ngoài vùng
  ⇒ `NGOAI_VUNG` ở đúng phép bị nhắm. (c) `that_con_I_<phép>` (đã có; cùng `-S`, `-E`) ⇒ `KHONG_DO_DUOC`. Đột biến: `phan_loai_bo_realpath`,
  `phan_loai_nhan_moi_ten`, `hook_chi_cai_theo_ten_trinh_thong_dich` (mới) và `bo_dem_python_con` (đã có) — mỗi cái `BAT` ở đúng ca nêu trong khối `tu-kiem --dot-bien`.
## Ngoài năm lệnh con
- `python3 .claude/dev/ci_dang_ky_test.py` (cùng clone, cùng commit mã): `PHẢN CHỨNG: 1677/1677 đỏ đúng` · `TỔNG: ĐẠT` · `rc=0`.
- `python3 -m ruff check --no-cache --select F` (ruff 0.15.15) trên ba tệp `.py` của PR: 0 lỗi; hai tệp có ở base: 0 lỗi ⇒ delta 0.
- CHƯA ĐO (ngoài quyền executor, H chưa đẩy): CI PR Ubuntu, K7 (`ci-dot-bien-du.yml`), Windows, Nghiệm thu 10 sau merge.
