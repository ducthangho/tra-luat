# wp1463 (PR2) — kết quả đo của SPEC r14, lease `wp1463-r14-g2-claude` (lượt 2)
Đo 2026-11-26 06:13Z–06:59Z, phiên cloud Linux, 4 CPU, Python 3.13.18, có `actionlint` và `shellcheck`, trên MỘT clone cục bộ
(`core.abbrev 7`) của commit mang đúng ba tệp mã của PR; base của lease `1260fa0cba89353911e2f97188b2c04dab8139d7`. Mỗi khối là đầu
ra NGUYÊN VĂN của lệnh ở tiêu đề (bỏ lời nhắc `detached HEAD` mà lệnh clone của git in ra stderr), `rc=` là mã thoát. Giây ở `ab` là giây tường cục bộ, ba lượt chạy NỐI TIẾP (không phải số CI). Dòng `KET_LUAN_REGISTRY: DAT (dau ra doc tu <thư mục nháp ngoài kho>)` của `registry` đứng trước `rc=0`; đường dẫn nháp không chép vào đây. Tệp đã chạy:
- `ops/ci_provenance_test.py` sha256 `295986a1ec9fe7aab8905d8ef68bd02896dd98f140a33efc2ddd1bfca480beec`
- `.claude/dev/ci_dang_ky_test.py` sha256 `92516f3f45fef47bfee810a26f53bd1f36724af0cd0d0e0a95ab629b6cc834d2`
## `do_pr2.py ab 1260fa0cba89353911e2f97188b2c04dab8139d7` (Nghiệm thu 1, 2, 5)
```
AB base=1260fa0cba89353911e2f97188b2c04dab8139d7 blob ops/ci_provenance.py base=2b2b9218892814e94c0ad95fe3bae77d41edd5fe H=2b2b9218892814e94c0ad95fe3bae77d41edd5fe (H = HEAD cua kho do, khong ghi o day)
LUOT base day_du: rc=0 · 646.5 s · TIEN TRINH: 4 · CPU 4
  CA: 77/77 dat · DOT BIEN: 485/485 bi giet dung ly do · TU KIEM PHAN HANG: DAT (2 dot bien) · TONG: DAT
LUOT H day_du: rc=0 · 634.6 s · TIEN TRINH: 4 · CHE DO: day_du · CPU 4
  CA: 86/86 dat · DOT BIEN: 522/522 bi giet dung ly do · TU KIEM PHAN HANG: DAT (2 dot bien) · TONG: DAT
LUOT H nhe: rc=0 · 153.5 s · TIEN TRINH: 4 · CHE DO: nhe · CPU 4
  CA: 86/86 dat · DOT BIEN: 522 muc CHE DO NHE — do khi diff cham vung · TU KIEM PHAN HANG: DAT (2 dot bien) · TONG: DAT
KE HOACH DOT BIEN: base 485 viec · H 522 viec · ten base ⊆ H: True
PHEP ca_bo_day_du: DUNG
PHEP cung_bang: DUNG
PHEP khong_thieu_ten: DUNG
PHEP ast_phan_hang: DUNG
PHEP luoi_phan_hang: DUNG
PHEP cung_blob_san_pham: DUNG
PHEP cong_thuc_cu_dong: DUNG
PHEP tong_hai_chieu: DUNG
PHEP kho_va_ben_doc_cu: DUNG
KET_LUAN_AB: DAT (9/9 phep dung)
rc=0
```
## `do_pr2.py registry --tu <thư mục --luu của lệnh ab>` (Nghiệm thu 3)
```
REGISTRY dau ra nhe / ke hoach nhe: ĐẠT (mong ĐẠT) · CI_DANG_KY ops/ci_provenance_test.py: ĐẠT rc=0
REGISTRY dau ra day_du / ke hoach day_du: ĐẠT (mong ĐẠT) · CI_DANG_KY ops/ci_provenance_test.py: ĐẠT rc=0
REGISTRY dau ra day_du / ke hoach nhe: ĐỎ (mong ĐỎ) · CI_DANG_KY ops/ci_provenance_test.py: chế độ nhẹ mà VẪN in dòng đột biến ĐỦ — cờ nhẹ không có tác dụng | CI_DANG_KY ops/ci_provenance_test.py: ĐỎ rc=0
REGISTRY dau ra nhe / ke hoach day_du: ĐỎ (mong ĐỎ) · CI_DANG_KY ops/ci_provenance_test.py: ĐỎ rc=0
rc=0
```
## `do_pr2.py vung` trên H (Nghiệm thu 4)
```
PHEP bo_day_du: SACH · rc=0 · (1) khac rong=True · (2) nhan chung ops/ci_provenance.py=True · (3) ngoai vung=[] · Python con/dong khoi dong con=608/608
  tap (5): ['.claude/dev/ci_dang_ky_test.py', '.github/workflows/ops-do-workflow-definition.yml', 'ops/bash_nen.py', 'ops/ci_provenance.py', 'ops/ci_provenance_test.py']
  khoi cuoi: ['CA: 86/86 dat', 'DOT BIEN: 522/522 bi giet dung ly do', 'TU KIEM PHAN HANG: DAT (2 dot bien)', 'TONG: DAT']
PHEP phan_chung_nguyen: SACH · rc=0 · (1) khac rong=True · (2) nhan chung .github/workflows/ci.yml=True · (3) ngoai vung=[] · Python con/dong khoi dong con=79/91
  tap (7): ['.claude/dev/ci_dang_ky_test.py', '.github/workflows/ci-dot-bien-du.yml', '.github/workflows/ci.yml', '.github/workflows/launcher-windows.yml', 'ops/bash_nen.py', 'ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json', 'ops/specs/wp1460-r1/hop_dong/fixture.json']
  danh tinh: che_do=nguyen truoc={'NHE': True, 'MAU_DAY_DU': True, 'MAU_NHE': True, 'VUNG_THEM': True, 'so_vung_them': 7} sau={'NHE': True, 'MAU_DAY_DU': True, 'MAU_NHE': True, 'VUNG_THEM': True, 'so_vung_them': 7} phan_chung=True hang=30/30
PHEP phan_chung_go_bon_khoa: SACH · rc=0 · (1) khac rong=True · (2) nhan chung .github/workflows/ci.yml=True · (3) ngoai vung=[] · Python con/dong khoi dong con=79/91
  tap (7): ['.claude/dev/ci_dang_ky_test.py', '.github/workflows/ci-dot-bien-du.yml', '.github/workflows/ci.yml', '.github/workflows/launcher-windows.yml', 'ops/bash_nen.py', 'ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json', 'ops/specs/wp1460-r1/hop_dong/fixture.json']
  danh tinh: che_do=go_bon_khoa truoc={'NHE': True, 'MAU_DAY_DU': True, 'MAU_NHE': True, 'VUNG_THEM': True, 'so_vung_them': 7} sau={'NHE': False, 'MAU_DAY_DU': False, 'MAU_NHE': False, 'VUNG_THEM': False, 'so_vung_them': 0} phan_chung=True hang=30/30
KET_LUAN_VUNG: SACH
rc=0
```
Lần chạy SỚM của lượt 2 (base + bốn thay đổi dữ liệu mục 3 + `vung`; `ops/ci_provenance_test.py` còn blob base `e381a597…`): `KET_LUAN_VUNG: SACH`, rc 0 — `bo_day_du` 5 tệp, 562/562, `DOT BIEN: 485/485`; hai probe mỗi cái đúng 7 tệp như trên, 79/92 và 79/93.
## `do_pr2.py tu-kiem --dot-bien` (gồm trọn các dòng `SO` của `tu-kiem`)
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
TU_KIEM_VUNG: 116/116 dat
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
DOT_BIEN_TU_KIEM: 28/28 bi bat dung cho (15 cua bo so, 13 cua phep do vung)
KET_LUAN_TU_KIEM: DAT
rc=0
```
`do_pr2.py tu-kiem`: `TU_KIEM_SO: 26/26 dat · moi phep co dau vao am: True · TU_KIEM_VUNG: 116/116 dat · KET_LUAN_TU_KIEM: DAT · rc=0`.
## Ngoài năm lệnh con
- `python3 .claude/dev/ci_dang_ky_test.py` (cùng clone): `PHẢN CHỨNG: 1677/1677 đỏ đúng` · `TỔNG: ĐẠT` · `rc=0`. CHƯA ĐO (ngoài quyền executor): CI PR Ubuntu, K7 (`ci-dot-bien-du.yml`), Windows, Nghiệm thu 10 sau merge.
