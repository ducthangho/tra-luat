# VERDICT wp1236 r9 vòng 3
spec_sha256: 50269a88976968f60f50f714c882ab88cba6f597ff0249bd19b5ce157342b496

## Finding vòng 1–2 của tôi còn mở

- R01: ĐÓNG — Hai fixture CRLF thật vẫn đạt trong phép quét 66 tệp; LF/CRLF đồng nhất đạt, CR lẻ/trộn bị bắt đúng lý do (`audit_round3.py`, rc 0).
- R02 / S01: ĐÓNG — C3–C5 nay so lý do D2b riêng, C4 neo đúng header T-fail; phép đo Git và điều kiện đặc tả xác nhận bỏ chốt làm mất lý do đích, không còn lấy rc của D3 hay chốt khác làm bằng chứng thay (`audit_d2b_round3.py`, rc 0).
- R03: ĐÓNG — `nang_tran` đủ bốn trường, đề nghị đợt A 3 tệp/800 dòng được ghi rõ chưa được duyệt; hai OID ADR vượt đủ ba phép kiểm trên lịch sử/ref được cấp (`audit_round3.py`, rc 0).
- R04: ĐÓNG — D2b neo attempt và đòi int dương; C3 phân biệt attempt lệch, thiếu và bool bằng lý do riêng (`audit_d2b_round3.py`, rc 0).
- R05 / S02: ĐÓNG — Census 25/56/39/50, 50 script = 20/28/2, 28 ca A và 49 ID đột biến khớp; các số cũ trong bảng phản biện đã được gắn rõ với vòng lịch sử.
- S03: ĐÓNG — B8 dùng pr680 nguyên byte, băm `964742fef636a70587b2247c094ac4f38aea540a01abdce8b6319c8f74b447bf`; cổng hiện hành rc 0, `1/1 miễn trừ`, còn áp L8 trước cutover sinh `dinh_dang_loi_khai` (`audit_round3.py`, rc 0).

## Findings mới

- id: T01
  severity: P3
  vi_tri: SPEC.md:86–87,283,421 — K3 và A1-14
  van_de: Điều kiện mới `moc.checkout` khác rỗng chưa có vế âm và đột biến riêng trong nghiệm thu.
  bang_chung: `python3 -B ../work/audit_new_guards.py` rc 0; trên bản sao T-v3-pass, `checkout: []` cho `not_measured/provenance_chua_du`, còn đột biến bỏ riêng chốt rỗng cho `passed`; đối chứng dương và cả ba vế A1-14(a–c) giữ nguyên kết quả giữa bản gốc và đột biến.
  de_xuat: Thêm A1-14(d) với `checkout: []`, đòi đúng `provenance_chua_du`, kèm đột biến chỉ bỏ điều kiện khác rỗng; giữ đối chứng đầy đủ vẫn passed và cập nhật tổng đột biến. Không nới luật checkout để làm ca xanh.

- id: T02
  severity: P3
  vi_tri: SPEC.md:98,165,324 — K8, đầu ra D2b và C4
  van_de: Chuỗi lỗi D2b đòi `<lý do đầu>` nhưng chưa định nghĩa cách in khi `kiem_tep` trả `failed` với danh sách lý do rỗng.
  bang_chung: `python3 -B ../work/audit_d2b_round3.py` rc 0; T-fail nguyên byte sau `git archive` trả `("failed", [])`, header run `44711337223`, attempt `1`, head `00ee83998487d289324566f230b67b5923a9a9d9`; không có phần tử lý do đầu tiên để dùng cho mẫu dòng 165.
  de_xuat: Chốt cách biểu diễn khi danh sách rỗng, chẳng hạn `D2b kiem_tep:failed`, và để C4 so đúng chuỗi đó, rc 12, không traceback; giữ nguyên ý nghĩa `failed`, không đổi thành `not_measured` chỉ để có lý do.

## Đã đo lại, khớp

- Reviewed SHA `e7e72db6b67a0102a6d3d553b75a901305dd1e96`; tree `0dc009107fea755b1a1bb938c3e7ad1f11a541c2`; base `8048551a9b1eb886c126d2a1a4df0f95fb285964`. SPEC trong/ngoài kho cùng băm được giao; branch `sandbox`, lịch sử không shallow, `core.abbrev=7`.
- `python3 -B ops/reviews/wp1236-r9-soan/thamchieu.py .` rc 0: **66 = 47 passed + 10 failed + 9 not_measured**. Cả 66 tệp có Git mode `100644`.
- `python3 -B ops/reviews/wp1236-r9-soan/do_loi_khai.py .` rc 0: **170 = 25 cutover + 56 đỏ + 39 đạt + 50 không lời khai**; **93 vi phạm**, phân rã **39/36/12/2/2/2** đúng đặc tả.
- `python3 -B ../work/audit_round3.py` rc 0: **170 hồ sơ, 94 landed, 0 lệch** với `kiem_ho_so_land`; A2-12 ba dạng, lời khai dương vi phạm và đối chứng false đúng; m44/m47–m49 mất đúng lý do đích; m45/m46 làm ca CR lẻ/trộn chuyển sang passed. B8 và các số đếm khớp.
- `python3 -B ../work/audit_d2b_round3.py` rc 0: O nằm trên `origin/ops/x` nhưng chưa trên master vẫn được chọn; archive giữ nguyên byte và T-v3-pass đạt. Symlink tệp có mode `120000`; bỏ chốt mode thì bản archive đọc được và đạt. C5(c) chỉ qua khi bỏ tiền tố; C9 loại O chỉ cục bộ và loại blob. Sửa cây làm việc không đổi archive tại O. C3 kiểm riêng năm biến thể neo/kiểu. Đây là phép đo Git và điều kiện đặc tả, không phải CLI D2b tương lai.
- `python3 -B ../work/audit_new_guards.py` rc 0: ngoài T01, fixture waiver sửa từ readback thật đạt khi hợp lệ, đổi riêng `author_association` sang MEMBER bị `tac_gia`. `python3 -B ../work/audit_c8_baseline.py` rc 0: **6/6** ca hiện hành gồm đối chứng đóng WP và D1/D3/D4 đạt.
- Chưa tìm thấy lời khai dương mới lọt L8/D2b mà thiếu tệp đánh giá khớp provenance trong phạm vi đã kiểm, ngoài các giới hạn giả mạo tệp/provenance, không đọc log và không neo head hồ sơ đã khai. Cách lấy dữ liệu từ OID trên nhánh remote phù hợp làn lưu trữ ADR-0060; `pham_vi_e`, `nang_tran`, `luat_dung` không có finding mới.
- `passed`: sáu lệnh đo hoàn chỉnh nêu trên; receipt và hash output ở `run2_receipts.json`. `failed/setup`: lần dựng kho tạm đầu rc 1 vì cấu hình ký commit thừa kế gọi dịch vụ cục bộ bị sandbox chặn; đã lưu lỗi, lượt hoàn chỉnh cấu hình riêng kho tạm. `skipped`: 0. `not_run`: mã triển khai r9 và toàn bộ suite/đột biến tương lai, full CI, Windows, Ruff. Hai P3 không chặn theo quy tắc của assignment.
- Provider `openai_codex`, execution surface `codex_cli`, transport `machine`, run `076d2a658ea34c0fa9cfa5598e0efce6` theo `run.json`; model/effort phục vụ `KHONG_DO_DUOC`. Linux, Python 3.13.18, PyYAML 6.0.3, Git 2.43.0; sandbox `workspace-write`, reviewer giữ repository chỉ đọc. Không gọi GitHub. Snapshot trước/sau **17.340 tệp không đổi băm**, HEAD/tree/diff/index/status không đổi; đây là đối chiếu hai mốc quan sát. Chỉ ghi hiện vật trong `work/`.

KET_LUAN: approve
