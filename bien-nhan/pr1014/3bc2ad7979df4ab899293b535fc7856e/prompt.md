# Cross-review lượt 3 — PR ducthangho/tra-luat#1014 (vá lỗi chỉ-Windows trong test) — reviewer: codex

Bạn là reviewer ĐỘC LẬP, phiên mới. Executor là một phiên Claude. Không tin lời khai của executor; tự đo.

## Đối tượng
- Kho tại `cay-kho/`. `reviewed_sha` = `32bf0e621b42cc33d6b68a8bb2a80f66f4b682f1` (cha `abc8607` = head lượt 2, đã approve 0/0/0/0 —
  `verdict-cu/review-2-VERDICT.md`). Trước mọi việc: `git -C cay-kho rev-parse HEAD` phải bằng `reviewed_sha`.
- Master đối chứng `641b3de`. Diff toàn PR: `git -C cay-kho diff 641b3de 32bf0e6` (2 tệp test). Delta lượt này: `git -C cay-kho diff abc8607 32bf0e6`.
- Bằng chứng mới: `windows-log-run40844300802-gate-ops.txt` (Windows thật, head `abc8607`): `bien_nhan_v2_test` 92/93 — c93, c96 ĐẠT,
  137/137 đột biến CÓ RĂNG; `c91` đỏ ở fixture `cau_hinh_canh_bao`: đòi stderr nêu `fsyncObjectFiles`, được rc=1.
- Lời khai executor (kiểm): Git for Windows (2.55.0.windows.5, đo trên máy local) KHÔNG in cảnh báo cho `core.fsyncObjectFiles=true` ở
  rev-parse/merge-base/cat-file/for-each-ref/--is-shallow-repository; `core.fsync=<thành phần lạ>` in
  "warning: ignoring unknown core.fsync component" ở cả 5 lệnh trên CẢ HAI nền. Bản vá đổi fixture sang `core.fsync=tl-thanh-phan-la`, dấu
  stderr = chính giá trị lạ.

## Nhiệm vụ
(a) Delta `abc8607..32bf0e6` đúng và tối thiểu? Trên Linux, git của sandbox có in cảnh báo cho `core.fsync=tl-thanh-phan-la` ở MỌI lệnh mà cổng
gọi (liệt kê lệnh cổng thực sự chạy trong fixture này, đừng chỉ tin danh sách 5 lệnh)? Cảnh báo có bị git tắt khi đi qua môi trường cổng dựng
(cổng lọc biến `GIT_*`, có thể đặt config riêng) không? Dấu `tl-thanh-phan-la` có thể khớp nhầm nguồn khác không?
(b) Răng: `m114_bo_qua_STDERR_cua_git` phải giết fixture mới (chạy thật trong bản sao tạm, cô lập fixture `cau_hinh_canh_bao`, hai chế độ nợ);
đối chứng c18 xanh. Thử thêm: xoá dòng `config core.fsync` ⇒ fixture phải ĐỎ (cổng rc=1), không xanh giả.
(c) Còn fixture con nào của c91 (17 cái) dựa vào HÀNH VI GIT có thể khác giữa Git for Windows và Linux (thông báo stderr, cảnh báo, grafts
deprecated, partial clone/promisor, symref, dangling) mà chưa được đo trên Windows? Đối chiếu log Windows mới: các fixture đứng TRƯỚC
`cau_hinh_canh_bao` trong vòng lặp đã ĐẠT trên Windows thật chưa (log chỉ báo chỗ đỏ đầu tiên — xác định từ log những gì đã được đo).
(d) Chạy trong bản sao tạm ngoài `cay-kho/`: `python3 ops/bien_nhan_v2_test.py` ở head và master; phân biệt ca đỏ vì kho nông với hồi quy.
Windows: chỉ dùng log đã giao; phần còn lại `not_measured`.

## Quyền
Chỉ đọc `cay-kho/`. Không push, không gọi API ghi GitHub. Ghi tệp tạm dưới thư mục làm việc hiện tại (ngoài `cay-kho/`).

## Đầu ra
Ghi `VERDICT.md` ở thư mục làm việc hiện tại: dòng đầu `verdict: approve|changes_requested`, dòng hai `reviewed_sha: <40 hex>`,
dòng `so_lop: P0 n / P1 n / P2 n / P3 n`, từng finding (id, mức, tệp:dòng, mô tả, tái hiện, đề xuất), mục "Đã đo" với lệnh/rc/kết quả.
`approve` chỉ khi 0 finding P0–P3.
