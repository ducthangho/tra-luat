**Kết luận: approve.** Không còn finding P0, P1 hay P2, chỉ còn 5 finding P3. SHA đặc tả khớp `50269a88…`.

- **Finding cũ của tôi:** R03, R04 và S01–S07 đều đã đóng. S03 còn một lệch chữ ở mC6, tôi tách thành T01 (P3).
- **Các chốt mới của bản sửa 2:** đo trên bản sao fixture thật đều đúng, không chặn oan dữ liệu thật.
  - `la_landed` so với `kiem_ho_so_land`: 170 hồ sơ, 94 landed, lệch 0.
  - Mỗi đột biến m45, m46, m47, m48 chỉ làm đỏ đúng ca đích của nó.
  - B8 dùng bản sao pr680 dựng được.
  - 66/66 tệp danh-gia có mode 100644 và khớp regex D2b.
  - Hai bản tham chiếu chạy lại ra trùng từng byte: 25/56/39/50, tổng 93 vi phạm.
- **Mục 3 của Issue:** không tìm được lời khai dương nào qua L8 hay D2b mà không có tệp danh-gia khớp provenance của run land thật, ngoài các giới hạn đã khai. Chỉ có một đường `owner_waived` chưa khai: chép một readback thật sang hồ sơ khác (T04).
- **Đáng báo chủ kho (T02):** D2b sẽ chặn hai nếp đóng WP đang dùng mà đặc tả chưa ghi thành hệ quả:
  - ba M8 `passed` của pr1392, pr1406 và pr1415 dựa vào run hậu duệ, vì run trên chính merge commit FAILED 38/39;
  - cả bốn M8 `owner_waived` hiện có chỉ có dòng `mien_gate_packet_loop:`, không có dòng `mien_gate_output:`.
- **Sự cố trong sandbox:** một lệnh `awk` của tôi (`print NF>0`) vô tình tạo tệp `0` ở gốc kho. Tôi đã xoá. `git status` nay rỗng, HEAD vẫn `e9afa78`.

VERDICT cũng đã ghi vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-3-claude/work/VERDICT.md`. Script đo nằm trong `work/r3/` và hai script cũ `work/a213.py`, `work/do_m8.py`.

```
# VERDICT wp1236 r9 vòng 3
spec_sha256: 50269a88976968f60f50f714c882ab88cba6f597ff0249bd19b5ce157342b496
## Finding vòng 1–2 của tôi còn mở
- R03: ĐÓNG — phần C5 đã dựng lại để mỗi vế chỉ một chốt bắt. mC11 làm (b) ra ĐẠT (đo được), mC12 làm (a) mất `duong_dan_sai`. Chữ của mC6 còn lệch, tách thành T01 (P3).
- R04: ĐÓNG — đóng cùng S01.
- S01: ĐÓNG — `la_landed` nhận đủ ba dạng. So với `kiem_ho_so_land._xet_mot_tep`: 170 hồ sơ, 94 landed, lệch 0. A2-12 (a)–(d) và đối chứng ra đúng kỳ vọng; m47 chỉ làm (b) đỏ, m48 chỉ làm (c) đỏ.
- S02: ĐÓNG — D2b nay neo theo OID trên `refs/remotes/origin/*`, không còn đòi `origin/master`. Kho dùng merge commit (40/40 commit first-parent có hai cha), nên sau khi PR lưu trữ merge, OID vẫn tới được.
- S03: ĐÓNG (phần thiết kế) — chốt đường dẫn nay chạy trên chuỗi thô và `git ls-tree`. Riêng chữ của mC6 còn lệch: xem T01.
- S04: ĐÓNG — tên lý do đã thống nhất, luật bắn cả khi hồ sơ đã có vi phạm khác. Đo lại: 36 lần bắn, 93 vi phạm.
- S05: ĐÓNG — `pr680` có băm khớp `MIEN_TRU_CUTOVER`. L8 tham chiếu chạy trên nội dung ấy ra `dinh_dang_loi_khai` (thêm `landed_khong_loi_khai_gate_output`), nên mB8 làm B8 ra rc 1.
- S06: ĐÓNG — đã thêm m45 và m46, đo trên bản sao `T-v3-pass`:
  - biến thể `\r` lẻ trong phần chữ tự do: gốc ra `cr_le`, m45 ra `passed`, m46 vẫn ra `cr_le`;
  - biến thể CRLF nửa số dòng: gốc ra `xuong_dong_tron`, m46 ra `passed`;
  - đối chứng toàn CRLF: `passed` ở cả ba.
- S07: ĐÓNG — đã thêm mục *Hệ quả cho biên bản M8*. K3 nay đòi `moc.checkout` khác rỗng, khớp `or [None]` trong bản tham chiếu.
## Findings mới
- id: T01
  severity: P3
  vi_tri: C5, dòng 325 (mC6, mC12)
  van_de: Đọc theo chữ, "mC6 bỏ tiền tố `ops/land/` của regex" sinh ra một regex không fullmatch bất kỳ đường dẫn nào bắt đầu bằng `ops/`, kể cả đường dẫn hợp lệ của C1. Hệ quả: mC6 bị C1 giết chứ không phải C5, còn C5(c) vẫn ra `duong_dan_sai`, tức "chết sai lý do". Ngoài ra câu "(a ra ĐẠT vì git chuẩn hoá đường dẫn)" chỉ đúng với một cách gọi `ls-tree` nhất định.
  bang_chung: |
    `work/r3/gitc`, `re.fullmatch`:
    - regex gốc: C1 True, (c) False;
    - bản bỏ hẳn `ops/land/`: C1 False, (c) False;
    - bản thay bằng `ops/[^/]+/`: C1 True, (c) True.
    Với `..`:
    - `git ls-tree O -- ops/land/pr1440-wp1319-provenance/..` liệt kê nội dung thư mục cha, tên mục khác tiền tố đã hỏi;
    - `git rev-parse O:…/..` bị hiểu thành phạm vi `A..B`;
    - `O:…/../pr1440-wp1319-provenance` ⇒ "Not a valid object name".
    Dù vậy C5 vẫn đỏ dưới mC12, vì ca so đúng tên lý do.
  de_xuat: Ghi mC6 thành "thay `ops/land/` bằng `ops/[^/]+/`". Ghi kết quả mC12 thành "(a) mất `duong_dan_sai`", không hứa ĐẠT.
- id: T02
  severity: P3
  vi_tri: Hệ quả cho biên bản M8, dòng 198–202; ngoai_pham_vi gạch L-7, dòng 224–225
  van_de: Thiếu hai hệ quả đo được của D2b trên nếp M8 thật, và câu về `hau-due` chỉ nói về L8. (i) M8 `passed` dựa vào run hậu duệ sẽ bị chặn bằng `D2b neo_head`. (ii) Mọi M8 `owner_waived` hiện có sẽ trượt `kiem_mien`.
  bang_chung: |
    `work/do_m8.py`: 40 M8 `passed`; 34 khớp run, head và `passed`.
    - pr1392, pr1406, pr1415 (cùng commit 19-11) ghi `ci_master.run_id: 44502045702`. Đó là run trên `4eda94e`, hậu duệ, vì run trên chính merge commit FAILED 38/39.
    `work/r3/do_m8_mien.py`: 4/4 M8 `owner_waived` (pr1340, pr1344, pr1347, pr1352) chỉ có dòng `mien_gate_packet_loop:`, 0 dòng `mien_gate_output:`.
    - pr1347 và pr1352 dùng lại waiver của SHA khác (`b8bc64f`, `aa718cb`), không phải merge commit của chính chúng.
  de_xuat: Thêm Hệ quả M8 số 4 — M8 `passed` phải trỏ run của chính `merge_commit`; run hậu duệ phải đi `owner_waived`. Thêm số 5 — waiver phải là dòng `mien_gate_output: <merge_commit> …`; dòng `mien_gate_packet_loop:` và waiver dùng lại cho SHA khác không được nhận. Ở ngoai_pham_vi ghi rõ: D2b chặn `hau-due`, chỉ L8 không chặn.
- id: T03
  severity: P3
  vi_tri: kiem_mien, dòng 128–134; D2b, dòng 156, 165, 170–171; C4, C6, dòng 324 và 326
  van_de: Đặc tả nói "tên lý do CỐ ĐỊNH; ca C so đúng tên", nhưng còn ba chỗ chưa định.
  bang_chung: |
    (a) Đặc tả không liệt kê tên `<điều kiện>` của `kiem_mien`, nhưng C6 so `D2b mien:tac_gia`. Tên này chỉ có trong `do_loi_khai.py`, nơi `os` và SHA còn gộp thành `os_sha`, trong khi A2-9 tách (g) và (i).
    (b) Khi `kiem_tep` ra `failed` thì K8 không có lý do (bản tham chiếu trả `('failed', [])`), nên `D2b kiem_tep:failed:<lý do đầu>` ở C4 có phần lý do rỗng.
    (c) Gạch `run_attempt` của D2b không đặt điều kiện, còn Hệ quả M8 số 1 nói "BẮT BUỘC khi `passed`". Chưa rõ M8 `owner_waived` có bị đòi không.
  de_xuat: Liệt kê tên điều kiện của `kiem_mien` (url, readback, tac_gia, dong_mien, han, os, sha). Ghi `<lý do đầu>` là rỗng hoặc `-` khi không có lý do. Nói rõ phạm vi của `attempt_kieu`.
- id: T04
  severity: P3
  vi_tri: chua_do_duoc, gạch readback, dòng 383–384; ngoai_pham_vi gạch L-7, dòng 224–225
  van_de: Câu "readback chứng minh có comment đúng dòng" rộng hơn thực tế, vì readback JSON là tệp trong hồ sơ, sửa tay được như provenance. Ở hồ sơ (`head = None`), SHA của waiver cũng không neo vào merge commit. Vì vậy một waiver `mien_gate_output` thật có thể được dùng lại cho hồ sơ landed khác chỉ bằng cách chép tệp readback, và qua luật landed mà không cần tệp danh-gia nào.
  bang_chung: Mục `kiem_mien`, dòng 133–134 ("ở hồ sơ land … SHA ấy phải xuất hiện nguyên văn trong chuỗi lời khai"). `han` chỉ kiểm dạng (Q10). Câu L-7 ở ngoai_pham_vi chỉ nói về "lời khai dương".
  de_xuat: Ở chua_do_duoc ghi "readback JSON sửa tay được, như provenance". Mở câu L-7 ra cho cả `owner_waived`: ở hồ sơ, SHA của waiver không neo vào commit land.
- id: T05
  severity: P3
  vi_tri: Thiết kế › `kiem_ho_so`, dòng 112 ("đo: 122/122 trích dẫn thật theo dạng này")
  van_de: Không tái lập được số 122/122. Số này cũng trái với chính phân rã ở dòng 182 ("2 tệp trích ngoài thư mục provenance").
  bang_chung: |
    Trên 170 hồ sơ:
    - đếm token danh-gia trên byte thô: 148 token, 144 phân giải dưới `thu_muc`;
    - đếm theo cặp (hồ sơ, token): 67 / 65;
    - chỉ đếm dưới khoá `gateoutput`: 62 / 60.
    Phần lệch là pr1392 và pr1406, trích `pr1415-wp433-provenance/hau-due-4eda94e/…`, tức tương đối `ops/land/`, không tương đối `thu_muc`.
  de_xuat: Ghi số đo lại kèm đơn vị (L1) và thời điểm, ví dụ "60/62 trích dẫn dưới khoá gateoutput; 2 trích tương đối `ops/land/` ⇒ `tep_danh_gia_khong_hop_le`".
## Đã đo lại, khớp
- sha256 của SPEC.md bằng `ops/specs/wp1236-r9.md` tại HEAD `e9afa78`. Diff giữa `d81f359` và `9e05aac` chỉ chạm đặc tả, `do_loi_khai.py`, README và các VERDICT vòng 2. `ops/land` không đổi so với `8048551`.
- `thamchieu.py` và `do_loi_khai.py` chạy lại trùng từng byte với `do_tep.txt` / `do_loi_khai.txt`:
  - 47 / 10 / 9;
  - 25 / 56 / 39 / 50;
  - vi phạm 39 / 36 / 12 / 2 / 2 / 2 = 93.
- `la_landed` so với `kiem_ho_so_land`: 170 / 94 / lệch 0. Hình dạng thật: pr1378 có `landed: True` ở mức gốc, không `trang_thai_packet`; pr1055 có `trang_thai_packet.landed: false` cộng khối `landed_20261102`.
- A2-12 (a)–(d) và đối chứng, m47, m48: đúng đích (`work/r3/a212_test.py`).
- A1-3 với m45, m46: đúng đích (`work/r3/a13_test.py`).
- B8: băm pr680 = `964742fe…`, khớp `MIEN_TRU_CUTOVER`.
- D2b trên dữ liệu thật: 66/66 tệp danh-gia có mode 100644 và khớp regex `tep`. Trong `ops/land` không có mode 120000.
- `git branch -r --contains O --format=%(refname)` liệt kê đủ `refs/remotes/origin/*`.
- C5(b): `git archive` giữ symlink; `kiem_tep` đọc xuyên symlink ra `passed`, nên mC11 làm (b) ra ĐẠT.
- Header của sáu fixture khớp C3/C4. T-fail có head `00ee839…` và attempt 1.
- 48 tệp M8, 0 tệp có `run_attempt`.
- m1…m49 mỗi số đúng một lần; 28 ca A, 8 ca B, 9 ca C; mB1–mB8 và mC1–mC13 không trùng.
- Dòng khai ADR-0053 và ADR-0055 trỏ commit có tệp ADR. Trần 6 tệp / 450 dòng khớp ADR-0053.
- Mục 3: không tìm được lời khai dương nào qua L8 hay D2b mà không có tệp danh-gia khớp provenance của run land thật, ngoài các giới hạn đã khai. Đã thử:
  - ba dạng landed;
  - đường dẫn `..`, symlink, `ops/khac`;
  - run hậu duệ, bị D2b chặn bằng `neo_head`;
  - YAML khoá trùng, bị L4 chặn.
  Chỉ lọt biến thể `owner_waived` (T04).
KET_LUAN: approve
```
