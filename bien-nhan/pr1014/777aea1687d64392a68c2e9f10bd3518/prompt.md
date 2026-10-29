# Cross-review lượt 1 — PR ducthangho/tra-luat#1014 (vá lỗi chỉ-Windows trong test) — reviewer: codex

Bạn là reviewer ĐỘC LẬP, phiên mới. Executor là một phiên Claude. Không tin lời khai của executor; tự đo.

## Đối tượng
- Kho tại `cay-kho/`. `reviewed_sha` = `ef2c3ff647baf88bad3baf55314fb3a3d2cf14f1` (merge master `641b3de` vào nhánh; commit vá là `8396cf2`).
  Trước mọi việc: `git -C cay-kho rev-parse HEAD` phải bằng `reviewed_sha`.
- Diff thật so master: `git -C cay-kho diff 641b3de ef2c3ff` — 2 tệp: `ops/bien_nhan_v2_test.py`, `ops/lease_publish_test.py`.
- Bằng chứng lỗi gốc (log Windows đã tải): `windows-log-run40833865576-gate-ops.txt` (bien_nhan_v2_test 90/93: c96 ĐỎ, c91/c93 KHÔNG ĐO ĐƯỢC,
  6 đột biến KHÔNG RĂNG) và `windows-log-run40812761896-gate-ops.txt` (lease_publish_test 253/254, t27 ĐỎ).
- Lời khai executor (kiểm từng cái):
  - c96: git giả cũ là script `/bin/sh` tên `git` trước PATH; Windows `CreateProcess` chỉ thêm `.exe` ⇒ git thật chạy ⇒ rc=1. Vá: chặn ở
    `bnv2.subprocess.run` (cửa DUY NHẤT cổng gọi git), mẫu khớp ⇒ rc=3 stderr rỗng; thêm bộ đếm `dung` khi git giả không được gọi.
  - c93/_kho_cau: `write_text`/`text=True` ghi `\r\n` trên Windows ⇒ SHA khác ⇒ ghi bằng byte; Linux byte không đổi.
  - c91 `run_json_ten_qua_dai`: Windows trả ENOENT cho thành phần 300 ký tự ⇒ trên Windows dùng ký tự cấm `<` (WinError 123/EINVAL).
  - t26/t27: `Path.glob` không phân biệt hoa thường trên Windows ⇒ helper `_tep_co_duoi` so `str.endswith`.

## Nhiệm vụ
(a) **Chẩn đoán đúng?** Đối chiếu log + mã. Mỗi ca: gốc lỗi khai có khớp triệu chứng không. Có lỗi chỉ-Windows nào KHÁC trong hai suite này
cùng lớp (git giả qua PATH, `write_text`/`text=True` ảnh hưởng SHA/băm, `glob` hoa thường, phụ thuộc errno/POSIX, symlink, chmod) mà bản vá
bỏ sót? Liệt kê từng chỗ kèm dòng; đánh giá cái nào sẽ đỏ trên Windows.
(b) **c96 có làm yếu ca không?** Bản cũ kiểm cổng qua PATH thật; bản mới chặn trong tiến trình. Chốt mà ca canh (rc lạ + stderr rỗng ⇒ rc=2,
cho `merge-base` và `--is-shallow-repository`) có còn được đo đầy đủ? Shim `types.SimpleNamespace(**vars(subprocess))` có lỗ gì (ví dụ cổng
dùng thuộc tính subprocess khác, đột biến `_dot_bien_tep` thay module `bnv2`, khôi phục khi ngoại lệ)? Đột biến `m125_bo_chot_RC_cua_git` có còn
giết `c96` — chạy thật trong bản sao tạm. Thử thêm: gỡ bộ đếm `dem` / để shim không khớp ⇒ ca có thành KHÔNG ĐO ĐƯỢC thay vì xanh giả?
(c) **t26/t27**: bản vá giữ hành vi Linux không đổi? Chọn "phân biệt hoa thường trên mọi nền" có che mất verdict nào mà lẽ ra mục lục phải có
(`ops/reviews/wp929-g1-codex-luot{1,2}-VERDICT.md`)? Đánh giá đó là nợ có sẵn hay hồi quy do bản vá; đề xuất xử lý nếu cần.
(d) **Chạy.** Trong bản sao tạm ngoài `cay-kho/`: `python3 ops/bien_nhan_v2_test.py` và `python3 ops/lease_publish_test.py --chi-ca=t26_`,
`--chi-ca=t27_` ở head và ở master `641b3de`; ghi dòng tổng. Clone nông sẽ làm vài ca đỏ vì "kho nông" — phân biệt rõ với hồi quy (so head↔master,
hoặc `git fetch --unshallow` nếu mạng cho phép). Windows: `not_measured` ở lượt này.

## Quyền
Chỉ đọc `cay-kho/`. Không push, không gọi API ghi GitHub. Ghi tệp tạm dưới thư mục làm việc hiện tại (ngoài `cay-kho/`).

## Đầu ra
Ghi `VERDICT.md` ở thư mục làm việc hiện tại: dòng đầu `verdict: approve|changes_requested`, dòng hai `reviewed_sha: <40 hex>`,
dòng `so_lop: P0 n / P1 n / P2 n / P3 n`, từng finding (id, mức, tệp:dòng, mô tả, tái hiện, đề xuất), mục "Đã đo" với lệnh/rc/kết quả.
`approve` chỉ khi 0 finding P0–P3.
