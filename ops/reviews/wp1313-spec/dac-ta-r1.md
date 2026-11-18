tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# LAUNCHER-5XX-KHONG-PHAI-CHAN r1 — 5xx không header GitHub là `khong_do_duoc`, không phải `chan`

- packet_id: LAUNCHER-5XX-KHONG-PHAI-CHAN; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #1313 |
| `nguon_cap_viec` | Nợ có tên #1313 do chủ kho mở trong phiên điều phối 13-11-2026. Chủ kho 17-11-2026 (phiên điều phối #1206) chọn "#1313 LAUNCHER-5XX" khi hỏi việc độc lập làm được ngay. |
| `review_class` | `sensitive`: `.claude/dev/launcher.py` và `.claude/dev/launcher_test.py` nhận lớp mặc định fail-closed từ `_tinh_lop_tu_write_set` (cùng lý do với #1375). Đối chiếu lại bằng `lease_publish check` khi cấp lease. |
| `base` | `13bf69f6eb797e859619a2062e7c9577e6a9cc0b` lúc soạn; lease ghi OID base thật lúc cấp. |

## 0. Hiện trạng (đo 2026-11-17T16:1xZ trên `13bf69f`, Linux, Python 3.13.18)

- `.claude/dev/launcher.py` có HAI hàm phân loại một phản hồi HTTP theo header `X-GitHub-*`, và cả hai gán mọi `HTTPError`
  KHÔNG có header GitHub thành `chan`, bất kể mã trạng thái:
  - `_do_rest_github` (dòng 4726), nhánh `except urllib.error.HTTPError as e:` (dòng 4760–4768): trả
    `("mo" if co_gh else "chan", …, False)`.
  - `_do_mcp_endpoint` (dòng 4994), nhánh `except urllib.error.HTTPError as e:` (dòng 5085–5090): trả
    `(("mo" if co_gh_ep else "chan"), …, False)`. Hàm này cố ý dùng tên biến `*_ep` khác chữ với `_do_rest_github` để mỗi mẫu
    đột biến khớp đúng một chỗ (`t117_moi_mau_dot_bien_phai_khop_DUNG_MOT_cho`).
- Hậu quả đo được (#1313, 13-11-2026 khoảng 14:10Z, 9 lượt gọi `_do_rest_github`): 502 không header do đường hầm proxy đứt
  (`$HTTPS_PROXY/__agentproxy/status` ghi `ws_closed_mid_exchange` tới `api.github.com:443`) bị in
  `chan HTTP 502 (KHONG header GitHub -> proxy tu sinh)`, y như 403 chặn theo đường dẫn đo ngày 17-08. Vài phút sau REST thông lại.
- Ca hiện có: `t110_rest_github_phan_loai_theo_HEADER_khong_theo_MA_TRANG_THAI` (dòng 3372) và
  `t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec` (dòng 5683). Cả hai phủ 200/403/4xx có header/lỗi
  mạng; không ca nào phủ 5xx. Ca nạp module bằng `_tai_launcher_thu()`, giả `urllib.request.urlopen`, khẳng định bằng `bang(...)`.
- Người gọi: `_do_github` dùng `tt_chung == "mo"` cho `rest-chung` và `ok_kho` cho `rest-kho` (mô tả `"{mt_kho} [{tt_kho}]"`
  khi hỏng); `_do_mcp_endpoint` được gọi ở dòng 5244. Cả hai người gọi đã xử lý `khong_do_duoc` (nhánh lỗi mạng sẵn có trả nó).

## 1. `write_set`

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

## 2. `ngoai_pham_vi`

- Không đổi phân loại 2xx (200 không header vẫn `chan`), 4xx (403 không header vẫn `chan`; 4xx có header vẫn `mo`), 5xx CÓ header
  GitHub (vẫn `mo`, thao tác hỏng), và lỗi mạng (vẫn `khong_do_duoc`).
- Không đổi cờ `ok` của bất kỳ nhánh nào: mọi 5xx vẫn `False`.
- Không đổi cách `_do_github` ánh xạ `khong_do_duoc` của `rest-kho` sang cờ (hiện `False`, in `rest-kho=khong … [khong_do_duoc]`,
  y như nhánh lỗi mạng đang làm). Đưa nó về `None`/`chua-do-duoc` là thay đổi riêng, không thuộc packet này.
- Không retry, không đổi `timeout`.
- Không CI Windows, không đo native Windows: ca thuần giả `urlopen`, chạy mọi nền.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | `_do_rest_github`, nhánh `HTTPError`: không header GitHub và `e.code >= 500` ⇒ trả `("khong_do_duoc", <mô tả>, False)`; mô tả nêu mã (`HTTP <mã>`) và nói rõ là lỗi truyền tải, không phải chặn (ví dụ `HTTP 502 (KHONG header GitHub, 5xx -> loi truyen tai, KHONG DO DUOC)`). Mọi trường hợp khác giữ nguyên hành vi base. | `.claude/dev/launcher.py` |
| M2 | `_do_mcp_endpoint`, nhánh `HTTPError`: cùng quy tắc với M1. Viết KHÁC CHỮ với dòng của M1 (giữ quy ước `*_ep` của hàm) để mẫu đột biến của M1 và M2 mỗi mẫu khớp đúng một chỗ; `t117` phải tiếp tục đạt. | `.claude/dev/launcher.py` |
| M3 | Ca mới `r1313_rest_5xx_khong_header_la_khong_do_duoc` (đăng ký vào `CA`): nạp module qua `_tai_launcher_thu()` trong thân ca, giả `urlopen`; khẳng định bằng `bang(...)`, thông điệp định danh vế: (a) 502 không header ⇒ `khong_do_duoc`, `ok is False`, mô tả chứa `502`; (b) 503 không header ⇒ `khong_do_duoc`; (c) 500 không header ⇒ `khong_do_duoc` (biên dưới); (d) 499 không header ⇒ `chan` (biên trên của 4xx); (e) 403 không header ⇒ `chan`; (f) 502 CÓ header `X-GitHub-Request-Id` ⇒ `mo`, `ok is False`. Khôi phục `urlopen` trong `finally`. | `.claude/dev/launcher_test.py` |
| M4 | Ca mới `r1313_mcp_endpoint_5xx_khong_header_la_khong_do_duoc`: cùng sáu vế (a)–(f) với `_do_mcp_endpoint("https://x/mcp/")`. | `.claude/dev/launcher_test.py` |
| M5 | Hai đột biến mới trong `DOT_BIEN`, mỗi cái nhắm đúng một hàm: `r1313_rest_5xx_ve_chan` (gỡ điều kiện 5xx của M1, đưa nhánh về hành vi base) với ca đích `["r1313_rest_5xx_khong_header_la_khong_do_duoc"]`; `r1313_mcp_5xx_ve_chan` (gỡ điều kiện 5xx của M2) với ca đích `["r1313_mcp_endpoint_5xx_khong_header_la_khong_do_duoc"]`. Mẫu `(tìm, thay)` lấy nguyên văn từ dòng M1/M2 đã viết; mỗi mẫu khớp đúng một chỗ. | `.claude/dev/launcher_test.py` |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Hai ca M3, M4 ĐẠT trên head (Linux, Python 3.13 của gate và 3.11 nếu có); `t110`, `t143`, `t117` vẫn ĐẠT. | Đột biến M5 qua runner `DOT_BIEN` ⇒ ca đích ĐỎ tại `bang(...)` vế (a), runner ghi `giet` (không phải `loi`/`bo_qua`), MỖI đột biến giết đúng ca đích của nó và không giết ca của đường kia. Đối chứng biên: trên bản sao tạm đổi ngưỡng `>= 500` thành `> 500` ở M1 ⇒ vế (c) của M3 ĐỎ; đổi thành `>= 400` ⇒ vế (d)/(e) ĐỎ. |
| N2 | Bộ đột biến của `launcher_test.py` trên CI giết hai đột biến M5 đúng ca đích (bán kính đột biến báo `giet 1/1` cho mỗi cái). | Xoá một ca hoặc bỏ đăng ký ⇒ runner báo thiếu ca đích; gỡ vế (a) của một ca trên bản sao ⇒ đột biến tương ứng SỐNG. |
| N3 | Hành vi ngoài 5xx-không-header không đổi: chạy `t110`, `t143` và toàn bộ ca có tên chứa `rest` hoặc `mcp_endpoint` trên base và head, cùng kết quả. | Bất kỳ ca nào đạt trên base mà đỏ trên head. |
| N4 | Đo trên exact head, ghi lệnh + mã thoát + bằng chứng dương: `ruff --select F` delta 0 trên hai tệp; `doctrine-scan`, `adr-song` rc 0; `git diff --check` sạch; `git diff --numstat base..H` đúng 2 tệp, ≤ 450 dòng thêm (`ADR-0053`). | Phản chứng lint: thêm một tên chưa định nghĩa ⇒ delta ≠ 0; phản chứng phạm vi: thêm đường dẫn thứ ba ⇒ numstat 3 tệp. `doctrine-scan`/`adr-song`: không có phản chứng riêng ở packet này — khai thẳng. |
| N5 | `python .claude/dev/launcher.py doctor` chạy trọn trên head (rc như base) và dòng `github` vẫn in đủ các đường. | rc khác base, hay thiếu một đường trong dòng `github`. |

## 5. `pham_vi_e`

Không chạm E4, không chạm E5.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Cần sửa ngoài write set, hoặc thấy một đường thứ ba cùng phân loại (ngoài hai hàm ở §0) ⇒ dừng triển khai và đi revision đặc tả.
- Đặc tả không thuộc Mission nên chờ chủ kho duyệt băm theo `ADR-0067` — **E2**.

## 7. `hinh_dang_ke_thua`

`khong_ap_dung` — sửa phân loại, không phải packet khắc phục một bản vá cũ.

## 8. `chua_do_duoc`

- Không tái hiện được 502 thật của proxy theo ý muốn; ca dùng `HTTPError` giả. Mô tả 502 thật lấy từ đo đạc ghi trong #1313.
- Kích thước ước lượng tĩnh: ~20 dòng ở `launcher.py`, ~80 dòng ở `launcher_test.py`; đo lại bằng numstat trước khi công bố.
