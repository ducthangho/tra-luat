# Đặc tả packet `T191-PY314-INTERPOLATION` r1 — vá khẩn ca t191 cho Python 3.14

Packet Issue: #1195. Nguồn thẩm quyền: thân Issue #1195 (chủ kho chọn "Vá khẩn t191" ngày 05-11-2026).

## Sự cố (đã đo)

- Từ khoảng 00:31Z ngày 05-11-2026 mọi lượt `ops — đăng lease bằng git` ĐỎ ở bước tự kiểm: `lease_publish: 283/284 đạt`,
  ca đỏ duy nhất là `t191_MOI_chot_cua_kiem_deu_duoc_t190_phu_o_nhanh_DA_DANG`.
- Runner: log "Set up job" của run 41950099518 in `Image: ubuntu-26.04`, `Version: 20261101.186.1`; readme của image ấy
  (`actions/runner-images`, tag `ubuntu26/20261101.186`) khai `Python 3.14.4`. Workflow không ghim Python.
- Tái hiện tại chỗ: cùng HEAD `1813bfd4`, chạy riêng t191 — Python 3.13.18 QUA, Python 3.14.6 ĐỎ đúng thông điệp của CI.

## Gốc lỗi (đo trên 3.14.6, bản sao tạm)

Ba lỗi độc lập, lỗi sau bị lỗi trước che:

1. **Vũ trụ khoá có hai lớp mới** `TemplateStr`, `Interpolation` (t-string) mà kho mẫu `_KHO_T191` không có mẫu nào.
   Thông điệp CI cắt ở 5 phần tử nên chỉ thấy `Interpolation`; danh sách thiếu đủ là 12 khoá `goc` của cả hai lớp.
2. **Bộ đọc chữ ký docstring** của `_vu_tru_t191` dùng `(\w+)[*?]? (\w+)`; 3.14 viết `Dict(expr?* keys, …)` và
   `arguments(…, expr?* kw_defaults, …)` nên assert "chữ ký docstring lệch `_fields`" đỏ (bị lỗi 1 che, vì chốt vũ trụ khoá
   chạy trước).
3. **`ast.unparse` của 3.14 in lại trường `str` của `Interpolation`** (văn bản nguồn) thay vì `value`, nên thay `value` bằng
   chốt/cờ bị bỏ qua âm thầm (witness `(False, False)`).

## Việc phải làm

- R1. Thêm một mẫu t-string vào `_KHO_T191`, chỉ vào kho khi Python đang chạy phân tích được (cùng cơ chế
  `_phan_tich_duoc_t191` đang dùng cho `type` 3.12/3.13).
- R2. Bộ đọc chữ ký nhận cả `?*`; trên 3.13 kết quả không đổi.
- R3. Khi thay một con của `Interpolation`, xoá `str` để `unparse` dựng từ `value`; áp ở cả hai chỗ thay (`_thay_t191`,
  `_sinh_goc_t191`). Không đổi hành vi với mọi lớp khác (chỉ `Interpolation` có trường `str`).
- R4. Ô không dựng nổi witness hợp lệ được miễn theo ĐÚNG luật của ca (`_MIEN_SINH_T191`, lý do là thứ máy đo), cùng lý do với
  ô tương ứng của f-string: `TemplateStr.values` ~ `JoinedStr.values`, `Interpolation.format_spec` ~ `FormattedValue.format_spec`,
  gốc `Interpolation` ~ gốc `FormattedValue`; gốc `TemplateStr` trong `F or @` ~ `Lambda`/`GeneratorExp` (giá trị luôn đúng).
  Mục miễn chỉ có khi Python có lớp ấy.
- R5. Một tự kiểm rẻ trong t191, chỉ chạy khi có `ast.Interpolation`: thay `value` qua `_thay_t191` thì văn bản dựng lại phải
  chứa chốt.

## Cấm

- KHÔNG nới chốt chung (mọi chốt của t191 giữ nguyên). KHÔNG sửa `ops/lease_publish.py` hay workflow.
- Không miễn theo lớp chung chung; mỗi mục miễn mang lý do đo được và t191 vẫn đòi MỌI lần xuất hiện hỏng đúng lý do.

## Tiêu chí nhận

- A1. `ops/lease_publish_test.py` N/N trên Python 3.13 và trên Python 3.14 (hai số bằng nhau).
- A2. Đột biến, đo trên 3.14: gỡ từng phần R1, R2, R3, R4 ⇒ t191 ĐỎ.
- A3. Trần: 1 tệp code (`ops/lease_publish_test.py`), ≤ 120 dòng thêm (`git diff --numstat` so merge-base). Đặc tả này và tệp
  lease là tệp điều phối, không tính vào trần.

## Ngoại lệ chủ kho đã duyệt (#1195)

Vì chính workflow đăng lease đang hỏng, lease của packet này chỉ cần nằm trên ref `ops/**` và qua `lease_publish.py check`;
comment lease được đăng bù khi workflow xanh lại. Lượt workflow đỏ ở bước tự kiểm của lease này là đúng dự kiến.

## Ghi chú

PR #1185 và #1181 (WP1176) cũng sửa `ops/lease_publish_test.py`, lease đã hết hạn; packet này không đụng chúng, có thể xung đột
khi chúng merge sau.
