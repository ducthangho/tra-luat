Kết luận: **changes_requested**, còn 3 finding P2 và 4 finding P3. Kho không bị sửa: HEAD vẫn `951b717`, `git status` rỗng. Công cụ Write lại bị từ chối quyền, nên tôi ghi `work/VERDICT.md` bằng Bash, chỉ trong `work/`.

- **Finding vòng 1 của tôi:** 10/12 đã đóng. Hai finding còn mở:
  - R03: phần C5 vẫn chưa đóng, và lỗi lan sang thêm hai đột biến.
  - R04: luật `landed` mới chỉ chặn được một trong ba dạng khai landed.
- **Mục 3 (có lời khai dương nào lọt không):** có. `ops/kiem_ho_so_land.py` công nhận ba dạng landed, nhưng luật mới chỉ đọc `trang_thai_packet.landed`. Tôi chép pr1378 thành một hồ sơ mới, giữ `landed: true` ở mức gốc, chỉ khai gate output bằng văn xuôi `0 dong ##[error]`, không có tệp danh-gia. Kết quả: L8 không thấy vi phạm nào, `land_evidence_nguon` ĐẠT, `kiem_ho_so_land` vẫn tính là landed. Năm hồ sơ thật (pr1055, pr924, pr950, pr963, pr1137) cũng land theo khối `landed_<ngày>` mà luật không thấy (S01).
- **Chốt mới chặn oan dữ liệu thật:** D2b bắt tệp danh-gia phải nằm trên `origin/master`. Điều này trái ADR-0060 ("PR lưu trữ … không chặn việc đóng WP"). Ca thật: pr1312 đóng WP lúc 14-11 02:36Z, còn tệp danh-gia tới master khoảng 26 giờ sau (S02).
- **Nghiệm thu C5:** hai biến thể (b) và (c) bị chốt "thành phần thứ ba" bắt trước. Vì thế mC11 và mC12 không thể làm C5 đỏ, còn mC6 cũng sống nếu thi công tự nhiên (S03).
- **Các chốt mới còn lại** đo đúng trên bản sao fixture thật: CRLF, `provenance_chua_du`, `ket_luan_lech`, A1-13 đến A1-15. Hai bản tham chiếu chạy lại ra trùng từng byte.

```
# VERDICT wp1236 r9 vòng 2
spec_sha256: 18da18c417a446284e7c40bf6c60070206891be88837bc4d88ad81d49c2c2e65
## Finding vòng 1 của tôi
- R01: ĐÓNG — đặc tả nhận CRLF đồng nhất. pr1312 và pr1317 ra `passed`. Trên bản sao T-v3-pass, `cr_le` (cả ở phần chữ tự do lẫn trong sha), `xuong_dong_tron` và đối chứng toàn CRLF ⇒ `passed` đều đúng; m38 làm đối chứng đỏ (`work/bien_the.py`).
- R02: ĐÓNG — A1-13 ra `not_measured ket_luan_lech:136203672900`, dưới m40 ra `passed`. Thêm chốt K5 mà corpus vẫn 47/10/9, trùng byte `do_tep.txt`.
- R03: CÒN MỞ — m13 (float/bool), m20 (`measured1`), m22, m23 (A2-4 dựng lại) và mC1 (dòng `D2b ĐẠT`) đã đóng. Phần C5 (mC6) chưa đóng và nay lan sang mC11, mC12: xem S03.
- R04: CÒN MỞ — luật `landed_khong_loi_khai_gate_output` chỉ đọc `trang_thai_packet.landed`. Hai dạng landed mà `ops/kiem_ho_so_land.py` công nhận (`landed` ở mức gốc, và khối `landed_<8 số>`) vẫn lọt bằng văn xuôi: xem S01.
- R05: ĐÓNG — 20/28/2 = 50 script, 39 vi phạm dương-không-tệp, m37 4/6, m1…m44 mỗi số đúng một lần, 27 ca A. Có lệch số mới ở phân rã luật landed: xem S04.
- R06: ĐÓNG — A1-15 dựng trên bản sao T-v2-pass ra `not_measured co_job_skipped`; dưới m1 ra `passed`. Đối chứng không sửa ra `passed`.
- R07: ĐÓNG — L8 chạy sau cutover. `MIEN_TRU_L8` 51 mục, không chứa mục cutover; có B1 và B8. Cách viết B8 xem S05.
- R08: ĐÓNG — A1-14 (a)(b)(c) đều ra `provenance_chua_du`; m41 chỉ làm (a) ra `passed`, m42 chỉ làm (b) ra `passed`.
- R09: ĐÓNG — đã đặt tên lý do, ghi base `thu_muc`, định rc CLI, thư mục D2b, B4 chép script. Cách `eval(compile(ast.Expression(nút.value)…), {"__builtins__": {"tuple": tuple}})` ra đúng 5 tên, khớp `CHECK_BAT_BUOC_TEN`.
- R10: ĐÓNG — đã thêm Hệ quả 5–8, và khai độ lệch so với mục 3 của Issue ở `ngoai_pham_vi`.
- R11: ĐÓNG — `nang_tran` đã có `ai_nang`, `tran_cu`, `tran_moi`.
- R12: ĐÓNG — (a) API đổi thành `kiem_ho_so(du_lieu, thu_muc)`; (b) D2b đọc từ `origin/master`. Nhưng cách sửa (b) đụng ADR-0060: xem S02.
## Findings mới
- id: S01
  severity: P2
  vi_tri: Thiết kế › `kiem_ho_so` gạch cuối (dòng 121–124); Hệ quả 7 (dòng 162); ngoai_pham_vi gạch cuối (dòng 192–193); A2-12 (dòng 255), B7 (dòng 271); MIEN_TRU_L8 (dòng 144–151)
  van_de: Luật landed chỉ coi là landed khi `trang_thai_packet.landed is True`, trong khi chính cổng `ops/kiem_ho_so_land.py` (dòng 4–15, 97–106) còn coi là landed hai dạng nữa: `landed` ở MỨC GỐC khi không có `trang_thai_packet` (kiểu a), và khối gốc `landed_<8 số>` có `landed: true` (kiểu b, wp981). Một hồ sơ MỚI land theo hai dạng này, chỉ khai gate output bằng văn xuôi, vẫn qua L8. Câu "chặn đường lọt chính" ở ngoai_pham_vi vì thế sai với 2/3 dạng landed, và đây là câu trả lời cho mục 3.
  bang_chung: `work/do_landed.py`: 24/170 hồ sơ có khối `landed_<8 số>`; pr1155 và pr1378 (19-11, không thuộc cutover) dùng `landed: True` mức gốc. Năm hồ sơ thật (pr1055, pr924, pr950, pr963, pr1137) có `trang_thai_packet.landed: false` nhưng landed qua khối kiểu b (`kiem_ho_so_land` ghi "landed đọc từ landed_2026…"); bản tham chiếu xếp bốn hồ sơ đầu vào KHONG_LOI_KHAI và pr1137 vào DAT. Dựng `work/landed/a2`: chép pr1378 thành `pr9001-moi`, đổi tên khoá `gate_output` duy nhất, đặt `landed_dieu_kien: '… DAT — Gate output (0 dong ##[error] tren 39 log)'` (dạng pr1065), không có tệp danh-gia ⇒ `do_loi_khai.py` cho `KHONG_LOI_KHAI` (0 vi phạm), `land_evidence_nguon.py` ĐẠT, `kiem_ho_so_land._xet_mot_tep` ra `('DAT', '… landed đọc từ landed (mức gốc)', True)`. Dùng định nghĩa landed của `kiem_ho_so_land` (`work/rong/`) ⇒ 25 / **56 ĐỎ** / 39 ĐẠT / 50 không lời khai, luật landed bắn 11 lần thay vì 6.
  de_xuat: Dùng đúng định nghĩa landed của `kiem_ho_so_land.py`: `trang_thai_packet.landed` nếu có khoá `trang_thai_packet`, không thì `landed` mức gốc; HOẶC có khối gốc `landed_\d{8}` mang `landed is True`. Có thể tách thành một hàm dùng chung, hoặc chép kèm test so hai cài đặt. Thêm vào A2-12 và B7 hai biến thể (mức gốc, kiểu b), mỗi biến thể một đột biến gỡ đúng dạng ấy. Đo lại `MIEN_TRU_L8` (bản tham chiếu: 56), sửa Hệ quả 7 và câu ở ngoai_pham_vi.
- id: S02
  severity: P2
  vi_tri: Luật mới › D2b (dòng 142: "đọc từ `refs/remotes/origin/master` … chưa có trên master ⇒ `D2b nguon_chua_tren_master`"); C9 (dòng 288); pham_vi_e, Hệ quả
  van_de: D2b buộc tệp danh-gia và provenance phải nằm trên `origin/master` thì mới đóng được WP. Điều này trái ADR-0060 (Accepted): ADR cho phần `ops/land/**` đi làn lưu trữ và nói làn ấy "không chặn việc đóng WP" (dòng 116–118), còn M8 là "điểm cuối" (dòng 113). Nếp đóng WP thật đang theo đúng ADR, nên D2b sẽ chặn oan, mà đặc tả không khai độ lệch ADR này ở đâu.
  bang_chung: pr1312 có M8 `moc_10_2_2.gate_output: passed`. Biên bản M8 đăng lúc `2026-11-14T02:36:12Z` (`readback-comment-6870309468.json`), và `kiem-dong-wp-m8.txt` ghi "ĐÓNG ĐƯỢC WP … rc=0". Tệp `danh-gia-gate-output-43466453500.txt` thì tới master qua PR #1324 (`116d776`, `2026-11-15T11:09:42+07:00`), tức khoảng 26 giờ sau. pr1394 cũng thêm `bien-ban-m8.yaml`, `kiem-dong-wp-m8.txt` và tệp danh-gia trong CÙNG commit `1cecd03`. Ngoài ra, PR lưu trữ "không cross-review bằng model", nên đọc từ master không cho thêm độ tin cậy về nội dung `ops/land/**`.
  de_xuat: Chọn một cách. (a) Biên bản M8 ghi `gate_output_nguon_oid` (40 hex). D2b đòi OID ấy đến được từ một ref `refs/remotes/origin/*` đã fetch, rồi `git archive <oid>`; C9 đổi thành "OID không có trên remote". (b) Đọc cây làm việc, đòi tệp được track và khớp `HEAD`, rồi khai giới hạn ở chua_do_duoc. (c) Giữ `origin/master` nhưng khai độ lệch ADR-0060 ở pham_vi_e và luat_dung, kèm mã câu hỏi cho chủ kho, và thêm hệ quả "đóng WP sau khi PR hồ sơ merge". Cho `readback_thu_muc` của nhánh owner_waived đọc cùng nguồn với `gate_output_nguon` (hiện chưa định).
- id: S03
  severity: P2
  vi_tri: C5 (dòng 284); D2b, câu "thành phần thứ ba … tận cùng `-provenance`" và "sau `resolve()` nằm dưới `<root>/ops/land/`, không symlink" (dòng 142)
  van_de: Cả ba đột biến của C5 không thể làm ca của chúng đỏ nếu thi công đúng chữ đặc tả, vì mỗi biến thể đã bị một chốt khác bắt và C5 chỉ so rc 12. Thêm nữa, chốt `resolve()`/symlink chạy trên cây làm việc, còn dữ liệu đọc từ `git archive` của `origin/master`, nên hai chốt ấy không đo đúng nguồn được đọc. Đây cùng lớp với R03 vòng 1.
  bang_chung: `PurePosixPath(p).parts`: (b) `ops/land/lk/…` có thành phần thứ ba `lk`; (c) `ops/land/x/../pr1440-wp1319-provenance/…` có thành phần thứ ba `x`. Cả hai không tận cùng `-provenance`, nên rc 12 do chốt (d) bất kể mC11/mC12. (a) `ops/khac/…` có `parts[:2] = ('ops','khac')`: bị chốt "dạng `ops/land/<X>-provenance/…`" bắt, hoặc nằm ngoài thư mục được archive (`ops/land/<X>-provenance`), nên mC6 sống. Đo trong kho git tạm `work/gitc`: `git archive origin/master ops/land/x/../pr1440-wp1319-provenance` âm thầm chuẩn hoá ra `ops/land/pr1440-wp1319-provenance/`; `ops/land/lk` (symlink đã commit) ra một mục `lrwxrwxrwx … lk -> pr1440-wp1319-provenance`; `ops/land/lk/<tệp>` ⇒ "not a tar archive".
  de_xuat: Định nghĩa chốt đường dẫn trên CHUỖI THÔ và CÂY GIT của nguồn đọc, không trên cây làm việc: `re.fullmatch(r"ops/land/[^/]+-provenance/(?:[^/]+/)*danh-gia-gate-output-\d+\.txt", p)`, cấm thành phần `.`/`..`, và mọi tiền tố của `p` trong `git ls-tree <ref>` phải có mode 040000/100644 (120000 ⇒ symlink). Dựng lại C5 để mỗi vế chỉ một chốt bắt: (a) `ops/land/pr1440-wp1319-provenance/../pr1440-wp1319-provenance/danh-gia…` (chỉ chốt `..`; đột biến nhận `..` ⇒ git chuẩn hoá ⇒ ĐẠT); (b) tệp danh-gia commit dạng symlink (mode 120000) trỏ tệp thật cùng thư mục (chỉ chốt mode); (c) `ops/khac/…` khi tệp và provenance cũng có trên ref (chỉ chốt regex). Hoặc cho C5 so cả tên lý do, không chỉ rc.
- id: S04
  severity: P3
  vi_tri: MIEN_TRU_L8, phân rã vi phạm (dòng 147–150)
  van_de: Theo chữ đặc tả ("KHÔNG có lời khai dương HỢP LỆ"), luật landed bắn 20 lần và tổng vi phạm là 77, không phải 6 và 63. Bản tham chiếu đặt `co_duong = True` cho mọi token dương kể cả khi tệp trượt, và chỉ thêm vi phạm landed khi hồ sơ chưa có vi phạm nào. Tên lý do trong bản tham chiếu là `landed_khong_loi_khai_gate_output_duong`, khác tên trong đặc tả.
  bang_chung: `work/dem/theo_chu.py` (chỉ `co_duong` khi lời khai không sinh vi phạm, bỏ điều kiện `not vp`) ⇒ `landed_khong_loi_khai_gate_output_duong: 20`; số hồ sơ vẫn 51/40/54.
  de_xuat: Ghi số theo đúng định nghĩa (20/77), hoặc đổi định nghĩa cho khớp bản tham chiếu. Thống nhất tên lý do. Số hồ sơ và `MIEN_TRU_L8` không đổi vì điểm này (S01 thì có đổi).
- id: S05
  severity: P3
  vi_tri: B8 (dòng 272)
  van_de: "Hồ sơ tạm mang tên và băm của một mục `MIEN_TRU_CUTOVER`, nội dung có lời khai dương không tệp" là không dựng được. Băm ghim nội dung, mà không hồ sơ cutover nào có lời khai dương thiếu tệp.
  bang_chung: `work/b8/chi_cutover.py` chạy L8 tham chiếu chỉ trên 25 hồ sơ cutover có băm khớp ⇒ 15 ĐỎ, trong đó 8 do `dinh_dang_loi_khai` (pr594, pr680, pr684, pr689, pr696, pr701, pr703, pr707) và 7 do luật landed; 0 `duong_khong_tep_danh_gia`.
  de_xuat: Ghim tệp cụ thể, ví dụ "bản sao byte-nguyên `pr680-wp676-land-evidence.yaml` (L8 trên nội dung ấy ⇒ `dinh_dang_loi_khai`)".
- id: S06
  severity: P3
  vi_tri: A1-3 (dòng 232); doc_danh_gia (dòng 66–67)
  van_de: Hai chốt mới `cr_le` và `xuong_dong_tron` có tác dụng thật nhưng chưa có đột biến nào nhắm vào chúng. A1-3 chỉ có m3, m4, m5, m38.
  bang_chung: Bản sao tham chiếu bỏ `cr_le`: `\r` đặt ở phần chữ tự do `(.*)` của dòng job ⇒ `('passed', [])` (`.` khớp `\r`). Bản sao chấp nhận tệp trộn (chỉ bỏ `\r` ở dòng có nó) ⇒ biến thể CRLF nửa số dòng ra `('passed', [])`.
  de_xuat: Thêm m45 "bỏ chốt `cr_le`" (đích: `\r` trong phần chữ tự do của dòng job) và m46 "nhận xuống dòng trộn". Ghim vị trí `\r` lẻ của A1-3 vào phần chữ tự do. Cập nhật tổng số đột biến và ước `kich_thuoc`.
- id: S07
  severity: P3
  vi_tri: Hệ quả (dòng 153–163); D2b (dòng 142); K3 (dòng 85–87)
  van_de: (1) Chưa có hệ quả cho biên bản M8: các khoá gốc mới `gate_output_nguon`/`gate_output_mien`, và `ci_master.run_attempt` bắt buộc. (2) K3 viết "mọi phần tử `moc.checkout[*]`", nên danh sách rỗng hoặc thiếu khoá thì đúng một cách trống rỗng; bản tham chiếu (`or [None]`) lại cho trượt.
  bang_chung: 48 tệp `ops/land/*/bien-ban-m8*.yaml`, 0 tệp có `run_attempt` (`grep -l run_attempt`). `thamchieu.py` dòng 58: `for c in y["moc"].get("checkout") or [None]`.
  de_xuat: Thêm mục "Hệ quả cho biên bản M8" (ba khoá trên, và thứ tự đóng WP theo S02). Ghi K3 "`moc.checkout` là list KHÁC RỖNG …" cho khớp bản tham chiếu.
## Đã đo lại, khớp
- sha256 SPEC.md và `ops/specs/wp1236-r9.md` đều `18da18c4…2e65`. HEAD `951b717`; `git status` rỗng trước và sau; không sinh `__pycache__`.
- `thamchieu.py` chạy lại, trùng byte `do_tep.txt`: 47/10/9. `do_loi_khai.py` trùng byte `do_loi_khai.txt`: 25/51/40/54, vi phạm 39/12/6/2/2/2.
- Script `danh_gia_gate.py`: 20 `b87f9697` · 28 `539fed68` · 2 `0ea9a5e9`. Hai tệp CRLF có `i/crlf w/crlf attr/-text`, ra `passed`.
- A1-3, cả chín biến thể và đối chứng: đúng lý do của từng biến thể. A1-13, A1-14 (a/b/c), A1-15 khớp bảng; m1, m38, m40, m41, m42 giết đúng đích.
- `CHECK_BAT_BUOC` đọc bằng `ast` + `eval` giới hạn builtins ⇒ 5 tên, bằng `CHECK_BAT_BUOC_TEN`.
- m1…m44 mỗi số đúng một lần (m28–m35 viết dạng khoảng); 27 ca A, 8 ca B, 9 ca C; mB1–mB8, mC1–mC13 không trùng.
- 156/170 hồ sơ có khoá `trang_thai_packet.landed` (81 false + 1 + 61 true + 13).
- `cmd_kiem_dong_wp`: D1 đòi `moc_10_2_2` đủ đúng bộ khoá ⇒ `gate_output` luôn có mặt; `DAT_MOC` = (passed, owner_waived); D3 đã neo `merge_commit` vào first-parent `origin/master`.
KET_LUAN: changes_requested
```
