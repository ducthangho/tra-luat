# BIÊN BẢN — chạy lại workflow đăng lease g2 sau khi cổng tự kiểm ĐỎ vì `t125`

| | |
|---|---|
| ai yêu cầu | chủ kho, phiên điều phối `18-09-2026`: *"chạy lại workflow đăng lease g2 đi"* |
| ai thực hiện | phiên claude (điều phối), bằng `POST /actions/runs/35365260980/rerun-failed-jobs` |
| thời điểm | `2026-09-18T16:1xZ` · `HTTP 201` |
| run | <https://github.com/ducthangho/tra-luat/actions/runs/35365260980> |

## Vì sao biên bản này tồn tại

**Chạy lại một cổng vừa đỏ để lấy màu xanh là hành vi phải để lại dấu vết.** Không có tệp này thì
lịch sử chỉ còn một lượt XANH, và không ai biết lượt trước đã ĐỎ, đỏ vì gì, hay ai quyết định chạy
lại. Đó đúng là cách một cổng biến thành nghi lễ.

## Cái đã ĐỎ, nguyên văn

Lượt đầu (`attempt 1`, `15:54:30Z`) hỏng ở bước **`tự kiểm cổng trước khi tin nó`**; bước `đăng`
bị `skipped`, nên **không comment nào được đăng**. Fail-close đúng thiết kế.

```
[A] khong-actor : lease_publish: 157/157 đạt   rc=0
[B] co-actor    : lease_publish: 156/157 đạt   rc=1
!!! do t125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor
    LỆCH_CHƯA_RÕ_NGUYÊN_NHÂN … ca lệch ĐỎ=['t139_A12_catalog_mutant_A0_giet_dung_ly_do_va_ghi_SONG_kem_seam']
  ĐỎ  t139…: catalog lệch: ['S8-bo-deadline: kỳ vọng GIET, thực SONG (seam: KhoObject._con_thoi_gian)']
```

## Vì sao chạy lại là hợp lệ — phép đo tách nguyên nhân

Không dựa vào cảm giác "chắc là flake". Hai lượt đăng lease chạy **cách nhau 34 giây**:

| nhánh | thời điểm | kết quả |
|---|---|---|
| `ops/cap-lease-541-g2` | `15:54:30Z` | **failure** |
| `ops/cap-lease-541` | `15:55:04Z` | **success** |

Mã cổng trên hai nhánh **giống từng byte**: `ops/lease_publish.py` blob `8a58066385`,
`ops/lease_publish_test.py` blob `06701deb6e`. Hai nhánh chỉ khác nhau đúng hai tệp vừa thêm — một
lease YAML và spec r3 — không tệp nào cổng chạy. **Cùng mã, cùng phút, kết quả ngược nhau.**

Khớp với lần trước: trên Windows của chủ kho sáng `18-09`, `t125` cũng ĐỎ với đúng chữ
`LỆCH_CHƯA_RÕ_NGUYÊN_NHÂN`, chỉ khác ca lệch (`t156`).

**Không chạm một byte mã nào.** `rerun-failed-jobs` chạy lại đúng job đã hỏng trên đúng commit ấy.

## Cái KHÔNG được đọc ra từ biên bản này

- **KHÔNG khai `t125` đã được chẩn đoán.** Chính ca ấy in `LỆCH_CHƯA_RÕ_NGUYÊN_NHÂN` và từ chối kết
  luận; biên bản này cũng không kết luận. `S8-bo-deadline` + seam `_con_thoi_gian` là **manh mối**
  (đột biến hạn chót ⇒ nhạy thời gian/tải), không phải nguyên nhân.
- **KHÔNG khai chạy lại là cách chữa.** Nó là cách **đi tiếp**. Khuyết tật còn nguyên.
- **KHÔNG khai lượt xanh chứng minh bản vá đúng.** Nó chỉ chứng minh lượt ấy xanh.

## Nợ mở ra từ đây

`t125` nay đã chặn **hai** phép đo khác nhau trong **một** ngày (Windows sáng, CI chiều). Theo
doctrine *"đếm HÌNH DẠNG lỗi, đừng chỉ đếm lỗi"* của kho: hai lần là **tín hiệu**, ba lần là bẫy.
Đề xuất mở packet riêng cho `t125` trước khi nó chặn lần thứ ba — và **không** gộp vào #541, vì
#541 đã khai `t125` là `ngoai_pham_vi` ở spec r3 và đang sát trần kích thước.
