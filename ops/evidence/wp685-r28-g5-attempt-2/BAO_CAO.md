# wp685 r28 g5 attempt 2: báo cáo executor subagent

- Packet #685 `wp685` (`LAUNCHER-CON-SONG-ESRCH`), Mission #686, revision 28, generation 5, **attempt 2**
  (event #686 `6098517954`, hạn 2026-10-10T15:48:45Z). Bắt đầu 14:28Z; mọi phép đo xong 14:47:20Z.
- **Ứng viên KHÔNG đổi**: `3089b54455a44b8cfcf2fd27b01894bc2a5d764d`, tree `952d7c3092e02886150bb9c936dec7b5fc779aec`,
  parent `ab457c651eb4428705f0492163080b661c858b72` (tree `8649be372de2c824268682c3f80fa086ee750ef7`). Attempt này chỉ
  sửa GÓI BẰNG CHỨNG theo VERDICT lượt 1 (`3c06c0fe…dd43`): 0 P1 / 3 P2, cả ba ở phía bằng chứng. Không lệnh nào
  dưới đây cho thấy lỗi mã, nên không có commit mới. Không push, không đăng GitHub, không gọi reviewer.
- Đặc tả `ops/specs/launcher-con-song-esrch-r28.md` @ `origin/claude/wp685-r24-doi-executor`: sha256 `8007edf4…e156`,
  khớp. Script kiểm lại băm ở cả `trich_chot_tinh.py` lẫn `bang_chung_aw_d.py`.
- Môi trường (khối (a)–(d) ở đầu MỌI log): Linux `6.18.44-fc-v114` x86_64, `ID=ubuntu`, `VERSION_ID="24.04"`,
  `Python 3.11.15`, `Python 3.12.3`, ruff 0.15.8. Reviewer lượt 1 dùng 3.11.17, nên mỏ neo (iii) không cho tái dùng
  chéo. Vì vậy mọi số dưới đây là số đo lại trong attempt này.

## Rig: cây SẠCH ở exact SHA
Một lệnh dựng cả hai vế, cùng các bước:
`for p in cay:3089b54… nen:ab457c6…; do git worktree add --detach $A/$d $s; git -C $A/$d config core.abbrev 7; done`.
Kết quả: `cay` = `3089b54…` / `952d7c3…`, status rỗng; `nen` = `ab457c6…` / `8649be3…`, status rỗng.
Vế thứ ba `nen_testuv` là worktree ở `ab457c6` cộng `launcher_test.py` của ứng viên (`git show 3089b54:…`). Status của
nó là ` M .claude/dev/launcher_test.py`, và vế này CHỈ dùng cho phản chứng "test mới đỏ trên nền".
`chay_log.sh` ghi vào đầu mỗi log: khối môi trường; `git rev-parse HEAD HEAD^{tree}` và `git status --porcelain` của
CHÍNH cây đo; sha256 hai tệp write set; lệnh nguyên văn; runtime; giờ UTC. Sau lệnh nó ghi thêm rc, rồi HEAD/tree và
status lần nữa. Mọi log `cay` đều mang `3089b54…`/`952d7c3…` và status `[]` ở **cả trước lẫn sau** lệnh. Mọi log
`nen` đều mang `ab457c6…`/`8649be3…` và status `[]`.

## Bảng B1–B8 (exact SHA; log ở `log/`)
| tiêu chí | cây | lệnh (cwd = cây) | rc | kết quả |
|---|---|---|---|---|
| B1–B4, B8 | `cay` 3089b54 | `sau_ca.sh python3.1x` (`--lap-ca tNNN --lan 1`, t156–t161) · `B1-B4_B8_cay_python3.1{1,2}.log` | 0 / 0 | 6/6 qua × 2 Python, `### TONG rc=0` |
| B1–B4, B8 phản chứng | `nen_testuv` (ab457c6 + test ứng viên) | cùng lệnh · `B1-B4_B8_nen_testuv_python3.1{1,2}.log` | 1 / 1 | 6/6 ĐỎ đúng loại, cả 2 Python: `B1 seam escaped` (ProcessLookupError), `B3b-giet-cay seam escaped` (PermissionError), `B8-sau-sinh 124 noi doi`, `B8-luc-sinh qua han khong giet duoc` rc=10, `B8-setsid 124 noi doi`, `B8-me-thoat 124 noi doi` |
| B2 chốt tĩnh | `cay` | `python3.1x -B chot_tinh_r12.py $A/nen/.claude/dev/launcher.py .claude/dev/launcher.py .claude/dev/launcher_test.py` · `B2_chot_tinh_python3.1{1,2}.log` | 0 / 0 | `UNG VIEN: DAT`, 13 đối chứng `DO DUNG LUAT`, `KET LUAN: DAT \| rc=0` ở cả 3.11 và 3.12 |
| B4 sàn Windows (tĩnh) | `cay` (+ test của `nen`) | `san_windows.py` ×2 · `B4_san_windows.log` | 0 | nền 11/177 không đo được (93.79 %, biên 42); ứng viên 65/231 (71.86 %, biên 4). Đây là ước lượng tĩnh, không phải một lượt chạy Windows |
| B5 A/W | `cay` | `bang_chung_aw_d.py .claude/dev <tam> all <spec>` · `B5_AW_D_python3.1{1,2}.log` | 0 / 0 | **55/55 cặp đạt** × 2 Python |
| B5 D | `cay` | cùng lệnh; bảng máy đọc `log/bang_D_python3.1{1,2}.json` (cùng sha256 `6dcbd999…7b14`) | 0 / 0 | danh mục: 65 khoá = đặc tả (trích bằng máy) = viết cứng; bảng control 65 dòng / 65 khoá, 0 lặp/thiếu/thừa. Bản đúng XANH (t156 56 đơn vị, t157 1, `thieu=[] thua=[]`, đúng thứ tự). **65/65 control đỏ đúng**: tập thiếu BẰNG kỳ vọng VÀ `thua=[]`. **6/6 phép đảo** `missing=[] thua=[] order=False` |
| B5 D phản chứng | `cay` | `phan_chung_d.py` · `B5_D_phan_chung_python3.1{1,2}.log` | 0 / 0 | **9/9** × 2 Python: bản sạch rc=0, và 8 phản chứng đều rc=1, mỗi cái in đúng dấu lý do (xem dưới) |
| B5 (E) | `cay` | `bang_chung_e.py .claude/dev <tam> <spec> log/bang_E_python3.1x.json` · `B5_E_python3.1{1,2}.log` | 0 / 0 | **118/118** (83 + 35; `DS-E-C3` không áp dụng), tập tên khớp danh sách ĐÓNG (thiếu=[], thừa=[]). Bảng `b945c96c…2ce0` (hai Python cùng băm, trùng attempt 1) |
| B6 suite (song song ×4) | `nen` / `cay` | `python3.1x -B .claude/dev/launcher_test.py` · `B6_suite_{nen,cay}_python3.1{1,2}.log` | 1 cả 4 | 3.11: nền 187/188, ứng viên 193/194. 3.12: nền 186/188, ứng viên 192/194. Ca đỏ: `t72_bi_ngat…` ở CẢ 4 log, cộng `r351_…` ở 3.12 cả hai vế. Tập ca đỏ hai vế BẰNG nhau ⇒ **delta = 0** |
| B6 suite (tuần tự) | `nen` / `cay` | cùng lệnh, mỗi lúc một tiến trình · `B6_suite_tuan_tu_*` | 0,0 / 1,1 | 3.11: nền 188/188, ứng viên **194/194**. 3.12: nền 187/188, ứng viên 193/194; ca đỏ duy nhất là `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` ở CẢ HAI vế, đỏ sẵn và phụ thuộc môi trường. **Delta = 0**. `t72` chạy riêng 3 lần × 4 tổ hợp (`B6_t72_lap_*`): 12/12 qua ⇒ đỏ ở lượt song song là do tải/đồng thời, có ở nền như ở ứng viên, không phải hồi quy |
| B6 `--dot-bien` | `nen` / `cay` | `… --dot-bien` · `B6_dotbien_*` | 0 cả 4 | nền `176/176 dat (1 khong do duoc)`; ứng viên `230/230 dat (1 khong do duoc)` × 2 Python; 54/54 mục `wp685_*` `OK`. Mục không đo được là `124_khi_chau_con_song` (đích `t62`, chỉ Windows), có ở cả hai vế |
| B6 ruff F | `nen` / `cay` | `ruff check --no-cache --select F --target-version py311 …` · `B6_ruff_{nen,cay}.log` | 1 / 1 | cả hai vế cùng 5 F841, chỉ lệch số dòng +2 ⇒ **delta multiset = ∅**. Đây không phải lint pass |
| B6 diff/write set | `cay` | `B6_git_numstat_grep.log` | 0 | numstat `33/5 launcher.py`, `1096/2 launcher_test.py` (+1129/−7); đúng 2 tệp; `git diff --check` rc=0; `linux:` chỉ có ở `:365`, `:499`; write set ở `423b4ba` = `ab457c6` (rc=0) |
| B7 | — | — | — | KHÔNG CHẠY: bằng chứng tuỳ chọn, không phải cổng. Windows thật, Python 3.13 và CI cũng không chạy |
| B8 | — | gộp vào hàng B1–B4, B8 (t158–t161) | — | — |

## Đóng từng P2 của VERDICT lượt 1
**1. `D65-control-catalog-not-validated`**, ở `bang_chung_aw_d.py`. Phần A/W giữ nguyên từng dòng; phần D viết lại.
- `khoa_tu_dac_ta` trích bằng máy hai thứ từ "Bảng tiểu nhãn" của đặc tả: 8 nhãn có tiểu nhãn kèm 48 tiểu nhãn
  (đếm khớp cột "số đơn vị"), và 9 nhãn không tiểu nhãn (lấy từ câu "Nhãn không liệt kê ở đây (…)"). Kết quả phải
  BẰNG bảng viết cứng (`TIEU`, 17 nhãn). 65 khoá có dạng `nhan:<nhãn>` và `tieu:<nhãn>/<tiểu nhãn>` đúng §7
  B5(D).6, và 57 đơn vị là duy nhất.
- `kiem_danh_muc` chạy TRƯỚC mọi control. Bảng control phải có đúng 65 dòng, mỗi khoá đúng một dòng. Thiếu, thừa,
  lặp hay sai tiền tố ⇒ `D DANH MUC DO` và rc=1. Phép đổi của mỗi dòng (`tach_khoa`) được DẪN XUẤT từ chính khoá, nên
  khoá và thứ bị đổi không thể lệch nhau.
- `doi_chieu` trả `(thiếu, thừa, sai thứ tự)`. Bản đúng chỉ xanh khi cả ba rỗng. Một control chỉ đạt khi tập thiếu
  BẰNG tập kỳ vọng và `thua=[]`. Quan sát lặp lại của CÙNG một đơn vị hợp lệ vẫn được chấp nhận, vì một đơn vị có
  nhiều assertion. Nhãn lạ bị ghi thành `('?', msg)`, tức là thừa.
- `bang_chung_e.py` đổi đúng một chỗ: lời gọi `AW.doi_chieu` nay nhận bộ ba, nên đối chứng sống cũng phải không có
  phần thừa.
- Phản chứng `phan_chung_d.py` (biến `D_PHAN_CHUNG`, mỗi ca phải rc≠0 VÀ in đúng dấu lý do). Kết quả 9/9 ở cả
  3.11 và 3.12:

| ca | thứ bị bơm | kết quả đo |
|---|---|---|
| `lap` (phản chứng của reviewer) | thay control cuối bằng control đầu | rc=1 · `so dong=65 so khoa=64 lap=['nhan:B1'] thieu=['tieu:B2-nhanh-cu/vang-decode']` |
| `thua` | thêm `tieu:B2-parse/p9` | rc=1 · `so dong=66 … thua=['tieu:B2-parse/p9']` |
| `thua_trung` | thêm một dòng trùng khoá | rc=1 · `so dong=66 so khoa=65 lap=['nhan:B1']` |
| `thieu` | bỏ control cuối | rc=1 · `so dong=64 … thieu=['tieu:B2-nhanh-cu/vang-decode']` |
| `khoa_cu` | khoá kiểu attempt 1 (`noi_mac_dinh:*`) | rc=1 · 17 khoá `nhan:*` thiếu, 17 khoá `noi_mac_dinh:*` thừa |
| `quan_sat_tieu_la` | một lời gọi `bang` đúng thêm, `B2-parse p9`, đi qua chính observer | rc=1 · `D ban dung: DO … thua=[('B2-parse', None)]` |
| `quan_sat_nhan_la` | thêm nhãn lạ `B9-la` | rc=1 · `thua=[('?', 'B9-la ngoai spec')]` |
| `quan_sat_tieu_thieu` | thêm `B2-doc-hong` không kèm tiểu nhãn | rc=1 · `thua=[('B2-doc-hong', None)]` |
| bản sạch | — | rc=0 · `65/65`, `6/6`, `hong=0` |

Ở ba ca `quan_sat_*`, mọi control và phép đảo cũng ĐỎ (`control 0/65`). Nguyên nhân: một đơn vị thừa làm mọi phép
so tập đỏ. Điều này đúng với hợp đồng, vì quan sát thừa không được che đi.

**2. `ED-immutable-artifact-missing`.** Gói này chứa `chot_tinh_r12.py`, là đúng tệp đã chạy ở hàng B2. Tệp được
trích lại bằng máy bằng `trich_chot_tinh.py`, script này đòi ba điều: đặc tả đúng `8007edf4…`, đúng MỘT khối khớp, và
khối có 412 dòng với sha256 `add42b31beeaece6e3cf546d3915a153099bfe7a232995b0e1546bbd4a5735b6`. Kết quả trích trùng
từng byte bản attempt 1. Mọi script khác trong chuỗi chạy cũng nằm trong gói, gồm wrapper `chay_*.sh` và `sau_ca.sh`.
`sau_ca.sh` attempt 2 trả rc=1 khi bất kỳ ca nào đỏ; bản attempt 1 trả rc của `echo`. `sinh_dot_bien.py` không có ở
đây, vì attempt này không chạy nó (mục `DOT_BIEN` đã nằm trong commit).
`kiem_goi.py` đỏ khi thiếu một tệp bắt buộc, khi `SHA256SUMS.txt` thiếu hay thừa dòng so với tệp thật, khi băm lệch,
hoặc khi `chot_tinh_r12.py` khác băm khối. Cờ `--tu-kiem` chép gói ra chỗ tạm, xoá `chot_tinh_r12.py` theo hai cách
(giữ dòng manifest / bỏ cả dòng manifest), và cả hai phải ĐỎ. Kết quả ở `log/kiem_goi.log`.
Phía đến (readback từ OID đã công bố) nằm NGOÀI quyền của subagent: phiên điều phối commit gói, đọc ngược tệp từ
commit ấy, rồi chạy lại `kiem_goi.py` trên bản đọc ngược.

**3. `exact-head-gates-incomplete`.** Mọi log B1–B6/B8 ở trên đo trên worktree SẠCH tách tại `3089b54`. Không có log
nào đo trên cây làm việc chưa commit. Log nền đo trên worktree sạch tại `ab457c6`. Vế `nen_testuv` khai rõ là nền cộng
test ứng viên, và status bẩn được ghi ngay trong log. Log cũ của attempt 1 không được sửa và không được dùng lại.

## Điểm cần phiên điều phối biết
- `t72_bi_ngat_KHONG_duoc_ghi_thanh_xong` đỏ ở lượt suite chạy song song 4 tiến trình, và đỏ ở CẢ nền lẫn ứng viên.
  Ca này qua khi chạy tuần tự, và qua 12/12 khi chạy riêng. Ca nhạy tải, delta = 0. Đây không phải ca của write set.
- `copyable_prompt.md` của attempt 1 không được sao sang gói này.
- Mọi tiến trình con đều được `wait`. Tối đa 4 tiến trình song song. Các worktree `cay`, `nen`, `nen_testuv` vẫn còn
  dưới `$SP/x685g5a2/`, để tái lập.
