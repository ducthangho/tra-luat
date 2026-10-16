# EVIDENCE lượt 3 — lời khai của phiên soạn, KHÔNG phải phép đo của reviewer

Lời khai lượt 1–2 vẫn ở `VERDICT.luot1.md`/`VERDICT.luot2.md` (của bạn) và trong kho `cay-kho/ops/reviews/thu-hoi-lease-a1a-r2/luot{1,2}-EVIDENCE.md`.

## E12. Xử lý lượt 2 (bản nháp 3, commit `79b8ec7b`)
- Áp `HINT.luot2.patch` của bạn nguyên hunk (F8, F9, F10, và phần thuật toán §8.2 của F11), rồi sửa thêm:
  §8.2 thay đoạn "trước khi dùng script… sửa script" bằng **bằng chứng script đã sửa**; thay thuật ngữ chưa định nghĩa
  "miền LEASE_ID" bằng luật cụ thể; "regular blob" → "blob (không kiểm mode — khớp bộ quét của cổng)".
- `do_q6.py` viết lại (diff trong `DIFF.nhap2-nhap3.patch`). Bản in phiên soạn (23:2xZ, không ghi giờ chính xác từng lệnh):
  - `python3 -B do_q6.py --tu-kiem` ⇒ `TU_KIEM: 13/13 dat`, rc=0.
  - 7 đột biến trên bản sao tạm (bỏ kiểm tên · bỏ kiểm mapping · bỏ kiểm trùng · bỏ kiểm kiểu thay_the_cho · bỏ rc3 cho KXĐ ·
    đọc HEAD thay cây mốc · bỏ lọc hạn) ⇒ mỗi cái rc=1 với đúng một ca `HONG` đích, không Traceback. Lần đo đầu, mutant
    "bỏ kiểm kiểu thay_the_cho" chết TypeError (tín dụng giả) ⇒ vòng lặp cặp đổi sang `or []`.
  - Kho thật: mien_lease 89, hợp lệ 89, vi_pham [], ngoai_mien 3 (.yaml.nhap), 11 cặp, digest `8f372ccd…`, KXĐ 0, (b) [] — rc=0.

## E13. Master đã tiến sau các phép đo của bản nháp 2
`origin/master` = `68b552d0` (merge PR #653 lúc `2026-09-26T23:11:08Z`). `git diff --name-only 24c48e28 68b552d0` **không** chạm
`ops/lease_publish.py`, `ops/lease_publish_test.py`, `.github/workflows/ops-thu-hoi-admission.yml`, `.github/workflows/ci.yml`,
`ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md`. Số đo của SPEC §1 vẫn neo `24c48e28` kèm giờ. PR #589 vẫn mở, head `23e16979`.

## E14. Mirror
`cay-kho/` detached tại `79b8ec7b71b04f7b9bdaffebe930fbb9965cd118`. `origin` là bare CỤC BỘ `kho.git`. Tập tên head của mirror
bằng `git ls-remote --heads origin` máy chủ lúc 23:23:57Z (435 head, `comm -3` rỗng); OID là của cache kho thật.
