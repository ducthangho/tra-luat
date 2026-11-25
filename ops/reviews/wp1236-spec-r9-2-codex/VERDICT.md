# VERDICT wp1236 r9 vòng 2
spec_sha256: 18da18c417a446284e7c40bf6c60070206891be88837bc4d88ad81d49c2c2e65

## Finding vòng 1 của tôi

- R01: ĐÓNG — Hai fixture CRLF thật đều passed; LF/CRLF đồng nhất đạt, CR trộn và CR lẻ bị từ chối đúng lý do; m38 làm đỏ đối chứng CRLF (`audit_round2.py`, rc 0).
- R02: CÒN MỞ — m13, m22 và mC1 đã sửa, nhưng lớp “ca bị chốt khác bắt thay” còn ở C3–C5, xem S01.
- R03: ĐÓNG — `nang_tran` đủ bốn trường, phân biệt đề nghị 3 tệp/750 dòng với quyền đã duyệt; hai OID ADR qua đủ phép kiểm trên refs được cấp (`audit_round2.py`, rc 0).
- R04: ĐÓNG — D2b đã neo attempt và đòi int dương; phép đo điều kiện nhận 1, loại 2, thiếu, bool và float (`audit_round2.py`, rc 0); chưa chạy mã D2b tương lai.
- R05: CÒN MỞ — 50 script, 27 ca và 44 ID đột biến đã khớp; còn hai chỗ giữ census cũ, xem S02.

## Findings mới

- id: S01
  severity: P2
  vi_tri: SPEC.md:142,282–284 — C3–C5; tiếp lớp R02
  van_de: Các ca chỉ đòi rc 12 chưa cô lập chốt đích, nên bỏ chốt được chỉ định vẫn có thể giữ nguyên kết quả nghiệm thu.
  bang_chung: `python3 -B ../work/audit_round2.py` và `python3 -B ../work/audit_d2_targets.py` đều rc 0. C5(b)/(c) có thành phần thứ ba `lk`/`x`, không tận cùng `-provenance`: bỏ chốt symlink/`..` vẫn bị điều kiện dòng 142 từ chối. Bản sao M8 hợp lệ qua CLI D1–D4 hiện hành rc 0; chỉ đổi `merge_commit` theo C3 thì rc 12 vì D3, ngay khi chưa có D2b. T-fail của C4 khác run/head với C1; nếu giữ M8 của C1, bỏ riêng chốt trạng thái vẫn bị neo run/head chặn. Đây là phép đo mã hiện hành và điều kiện đặc tả, không phải D2b tương lai. Chi tiết: [audit_round2.json](audit_round2.json), [audit_d2_targets.json](audit_d2_targets.json).
  de_xuat: C3 kiểm lý do D2b cụ thể; C4 ghi rõ M8 khớp header T-fail và D1/D3/D4 đạt; C5 đặt symlink/`x/..` bên trong thư mục có thành phần thứ ba hợp lệ, kiểm riêng lý do chốt đích. Đo lại đối chứng nguyên bản/đột biến và `TinHieuChotCa` đúng ca; giữ D3 và yêu cầu nguồn trên master để tránh làm yếu cổng khi sửa test.

- id: S02
  severity: P3
  vi_tri: SPEC.md:331,345 — tiếp lớp R05
  van_de: Hai đoạn vẫn khai `53 hồ sơ ĐỎ` và `53/40/77`, trái bảng census cập nhật ở dòng 145–150.
  bang_chung: `python3 -B ops/reviews/wp1236-r9-soan/do_loi_khai.py .` rc 0: `MIEN_CUTOVER=25, DO=51, DAT=40, KHONG_LOI_KHAI=54`; `audit_round2.py` xác nhận hai chỗ còn số cũ.
  de_xuat: Đồng bộ số; nếu giữ lịch sử thì ghi rõ băm/bản vòng 1 và phạm vi chưa áp cutover. So mọi chỗ dẫn census trên cùng bản đặc tả để tránh trộn phạm vi đếm.

- id: S03
  severity: P3
  vi_tri: SPEC.md:272 — B8
  van_de: B8 chưa phân biệt mục cutover thật với mục tiêm riêng trong test, trong khi dạng fixture “dương không tệp” không có trong 25 hồ sơ còn khớp băm.
  bang_chung: `python3 -B ../work/audit_claims.py` rc 0: 25 hồ sơ khớp băm, 0 fixture dương không tệp, 15 fixture bị L8 từ chối vì lý do khác. pr594 qua cổng hiện hành rc 0, `1/1 miễn trừ`; áp logic L8 trước cutover cho bốn lỗi `dinh_dang_loi_khai`. Chi tiết: [audit_claims.json](audit_claims.json).
  de_xuat: Dùng nguyên byte pr594 và đổi đầu vào B8 thành “lời khai sai định dạng”; mB8 vẫn phải làm ca đỏ. Hoặc ghi rõ tiêm mục chỉ vào instance module test như c09 hiện có, giữ phép kiểm bảng cutover sản phẩm để tránh nới miễn trừ.

## Đã đo lại, khớp

- Reviewed SHA `026e35fab50887a6b7b09091ce0ba2200c3db307`; tree `a5343922a6ddb862b819fc573a03d2c975877911`; base `8048551a9b1eb886c126d2a1a4df0f95fb285964`. Hai bản SPEC trong/ngoài kho cùng băm được giao.
- Hai script tham chiếu rc 0: 66 tệp = 47 passed/10 failed/9 not_measured; 170 hồ sơ = 25 cutover + 51 đỏ + 40 đạt + 54 không lời khai. Bộ sinh: 50 script = 20/28/2; header = 29/35/2.
- Trên bản sao fixture và tham chiếu: A1-13/m40, A1-14/m41–m43, A1-15/m1 đổi màu đúng chốt; CRLF không chặn oan dữ liệu thật. A2-12/B7 bắt landed thiếu lời khai; đối chứng landed false đạt.
- `git archive` nguồn master rc 0, fixture vẫn passed và khớp byte; tệp chỉ có ở cây tạm không đọc được từ master (rc 128), phù hợp C9. Hai bản lịch sử #1127 đều bị từ chối đúng `duong_khong_tep_danh_gia`.
- Chưa tìm thấy lời khai dương lọt ngoài giới hạn đã khai trong phạm vi đã kiểm; đây không phải chứng nhận mã triển khai chưa tồn tại.
- `passed`: hai phép quét và ba script đo hoàn chỉnh. Lần dò B8 đầu rc 1 vì không tìm được fixture; bản đo tiếp ghi rõ kết quả đó. `failed`: yêu cầu chết đúng ca đích ở S01. `not_run`: mã triển khai r9, full CI, Windows, Ruff; không phép đo nào bị skipped.
- Provider `openai_codex`, surface `codex_cli`, transport `machine`, run `f16313512cbf477eada2d9eeb57b79bc`; model/effort thực phục vụ `KHONG_DO_DUOC`. Linux, Python 3.13.18, PyYAML 6.0.3; sandbox `workspace-write`, reviewer giữ repository chỉ đọc. Không gọi mạng; snapshot đầu/cuối 17.337 tệp không đổi băm, HEAD/tree và diff/index không đổi. Hiện vật trong `work/`.

KET_LUAN: changes_requested
