tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# LAUNCHER-5XX-KHONG-PHAI-CHAN r3 — 5xx không header GitHub là `khong_do_duoc`, không phải `chan`

- packet_id: LAUNCHER-5XX-KHONG-PHAI-CHAN; revision: 3;

| trường | giá trị |
|---|---|
| `packet_issue` | #1313 |
| `nguon_cap_viec` | Nợ có tên #1313 do chủ kho mở trong phiên điều phối 13-11-2026. Chủ kho 17-11-2026 (phiên điều phối #1206) chọn "#1313 LAUNCHER-5XX" khi hỏi việc độc lập làm được ngay. |
| `review_class` | `sensitive`: `.claude/dev/launcher.py`, `.claude/dev/launcher_test.py`, `.claude/dev/mcp_github_doc.py`, `.claude/dev/mcp_github_doc_test.py` nhận lớp mặc định fail-closed từ `_tinh_lop_tu_write_set` (cùng lý do với #1375). Đối chiếu lại bằng `lease_publish check` khi cấp lease. |
| `base` | `3d6bfa5361dc30caf1caea9ae2c3ffe1a563902f` lúc soạn r3 (hai tệp launcher không đổi so với `13bf69f`, nơi đo §0 của r1/r2: `git diff` rỗng); lease ghi OID base thật lúc cấp. |

## 0. Hiện trạng (đo 2026-11-17T16:16:56Z trên `13bf69f`, Linux, Python 3.13.18)

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
- Chỗ THỨ BA (executor g1 của lease `wp1313-r2-g1-claude` phát hiện ở preflight, dừng theo §6 r2; đo lại 2026-11-18T00:0xZ trên
  `3d6bfa5`): `.claude/dev/mcp_github_doc.py` (client MCP GitHub tự dựng), hàm `Phien._post`, nhánh `except urllib.error.HTTPError as e:`
  (dòng 130–134): mọi `HTTPError` không header `X-GitHub-*` ném `Hong("HTTP <mã> (KHONG header GitHub -> proxy tu sinh)")`, kể cả 5xx;
  `_main` (dòng 235) in `KHONG_DO_DUOC/CHAN: <mô tả>`. Tệp này không trả trạng thái ba giá trị — bệnh nằm ở MÔ TẢ (cùng suy diễn
  "thất bại ⇒ proxy chặn"). Docstring đầu tệp tự khai "cùng tiêu chí `_do_rest_github` và `_do_mcp_endpoint`".
  `.claude/dev/mcp_github_doc_test.py` không có ca nào cho 5xx (grep rỗng); tệp có runner đột biến riêng (`--dot-bien`, bảng
  `DOT_BIEN` bốn trường `(tên, tìm, thay, ca đích)`, phân hạng `TinHieuChotCa` theo tên ca) và được CI đếm bằng mẫu
  `mcp_github_doc tests: N/N ca QUA` (`.claude/dev/ci_dang_ky_test.py`). Nhánh 2xx không header ở `bat_tay` (dòng 173–174) giữ nguyên
  theo §2 (2xx không header vẫn là chặn).
- Ca hiện có: `t110_rest_github_phan_loai_theo_HEADER_khong_theo_MA_TRANG_THAI` (dòng 3372) và
  `t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec` (dòng 5683). Cả hai phủ 200/403/4xx có header/lỗi
  mạng; không ca nào phủ 5xx. Ca nạp module bằng `_tai_launcher_thu()`, giả `urllib.request.urlopen`, khẳng định bằng `bang(...)`.
- Người gọi: `_do_github` dùng `tt_chung == "mo"` cho `rest-chung` và `ok_kho` cho `rest-kho` (mô tả `"{mt_kho} [{tt_kho}]"`
  khi hỏng); `_do_mcp_endpoint` được gọi ở dòng 5244, kết quả `khong_do_duoc` đổi thành cờ `None` và `_nhan_duong` in
  `chua-do-duoc`. NHƯNG `_do_github` còn một chỗ suy diễn ở đầu ra (dòng 5257–5259): `kho_chan = any(t == "rest-kho" and not ok …)`
  rồi, khi `gh-cli` báo đã xác thực, in `gh BAO da xac thuc nhung duong kho bi chan`. Chỗ này gộp MỌI thất bại của `rest-kho`
  (404 có header, lỗi mạng, cờ `None` khi không đọc được slug, và 5xx sau packet này) thành chữ "bị chặn" — cùng bệnh với
  #1313 ở tầng kết xuất (review độc lập lượt 1, F3).
- Neo đột biến hiện có chạm hai nhánh này (đo `grep` trên `launcher_test.py`, mỗi mẫu khớp đúng một chỗ ở base):
  `rest_phan_loai_theo_ma_trang_thai` (neo dòng `co_gh = any(...)` + chú thích ngay dưới, nhánh `HTTPError` của REST),
  `rest_toi_duoc_la_lam_duoc_viec` (neo `                False)\n    except Exception as e:`, cuối nhánh `HTTPError` của REST),
  `mcp_endpoint_toi_duoc_la_LAM_DUOC_VIEC` và `mcp_endpoint_in_token_vao_mo_ta` (cả hai neo nguyên dòng `return` 5090 của MCP).

## 1. `write_set`

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
.claude/dev/mcp_github_doc.py
.claude/dev/mcp_github_doc_test.py
```

## 2. `ngoai_pham_vi`

- Không đổi phân loại 2xx (200 không header vẫn `chan`), 4xx (mọi 4xx không header vẫn `chan`, kể cả 407 và 429; 4xx có
  header vẫn `mo`), mã ngoài 100–599 (vẫn như base), 5xx CÓ header GitHub (vẫn `mo`, thao tác hỏng), và lỗi mạng (vẫn
  `khong_do_duoc`). 429 không header có thể chỉ là giới hạn tần suất của proxy; giữ `chan` là GIỚI HẠN CỐ Ý của packet này, ghi
  bằng một vế test để ai đổi nó phải đổi có chủ ý.
- "Không header + 5xx ⇒ `khong_do_duoc`" là lựa chọn chẩn đoán BẢO THỦ (chưa đủ bằng chứng kết luận chặn), không phải khẳng định
  chắc chắn là lỗi truyền tải.
- Không đổi cờ `ok` của bất kỳ nhánh nào: mọi 5xx vẫn `False`.
- Không đổi cách `_do_github` ánh xạ `khong_do_duoc` của `rest-kho` sang cờ (hiện `False`, in `rest-kho=khong … [khong_do_duoc]`,
  y như nhánh lỗi mạng đang làm). Đưa nó về `None`/`chua-do-duoc` là thay đổi riêng, không thuộc packet này.
- Không retry, không đổi `timeout`.
- Không CI Windows, không đo native Windows: ca thuần giả `urlopen`, chạy mọi nền.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | `_do_rest_github`, nhánh `HTTPError`: không header GitHub và `500 <= e.code < 600` ⇒ trả `("khong_do_duoc", <mô tả>, False)`. Mô tả chứa `HTTP <mã>` và cụm chuẩn `loi truyen tai`, KHÔNG chứa `proxy tu sinh` (ví dụ `HTTP 502 (KHONG header GitHub, 5xx -> loi truyen tai, KHONG DO DUOC)`). Viết thành nhánh trả sớm THÊM VÀO; các dòng mà neo đột biến hiện có (§0) trỏ tới giữ nguyên từng byte, để mỗi mẫu cũ vẫn khớp đúng một chỗ. Mọi trường hợp khác giữ nguyên hành vi base. | `.claude/dev/launcher.py` |
| M2 | `_do_mcp_endpoint`, nhánh `HTTPError`: cùng quy tắc và cùng cụm chuẩn với M1. Viết KHÁC CHỮ với dòng của M1 (giữ quy ước `*_ep` của hàm) để mẫu đột biến của M1 và M2 mỗi mẫu khớp đúng một chỗ; dòng `return` 5090 mà hai đột biến MCP hiện có neo vào giữ nguyên từng byte; `t117` phải tiếp tục đạt. | `.claude/dev/launcher.py` |
| M6 | `_do_github`: cảnh báo `gh BAO da xac thuc nhung duong kho bi chan` chỉ in khi `rest-kho` ĐÃ ĐO và trạng thái là `chan` (giữ trạng thái `tt_kho` để quyết, không suy từ cờ `ok`). `rest-kho` hỏng vì lý do khác (`khong_do_duoc`, `mo` thiếu quyền, không đọc được slug) thì không in chữ "bị chặn". Không đổi cờ hay kết luận `DUNG_DUOC` nào. | `.claude/dev/launcher.py` |
| M3 | Ca mới `r1313_rest_5xx_khong_header_la_khong_do_duoc` (đăng ký vào `CA`): nạp module qua `_tai_launcher_thu()` trong thân ca, giả `urlopen`; khẳng định bằng `bang(...)`, thông điệp định danh vế. Vế (a) 502, (b) 503, (c) 500 (biên dưới), mỗi vế không header, khẳng định ĐỦ BỐN điều: trạng thái `khong_do_duoc`, `ok is False`, mô tả chứa đúng mã, mô tả chứa `loi truyen tai` và không chứa `proxy tu sinh`. (d) 499 không header ⇒ `chan`; (e) 403 không header ⇒ `chan` và mô tả chứa `proxy`; (f) 502 CÓ header `X-GitHub-Request-Id` ⇒ `mo`, `ok is False`; (g) 600 không header ⇒ `chan` (biên trên của dải 5xx); (h) 429 không header ⇒ `chan` (giới hạn cố ý, §2). Khôi phục `urlopen` trong `finally`. | `.claude/dev/launcher_test.py` |
| M4 | Ca mới `r1313_mcp_endpoint_5xx_khong_header_la_khong_do_duoc`: cùng tám vế (a)–(h) với `_do_mcp_endpoint("https://x/mcp/")`. | `.claude/dev/launcher_test.py` |
| M8 | `mcp_github_doc.py`, `Phien._post`, nhánh `HTTPError`: không header GitHub và `500 <= e.code < 600` ⇒ vẫn ném `Hong`, nhưng mô tả chứa `HTTP <mã>` và cụm chuẩn `loi truyen tai`, KHÔNG chứa `proxy tu sinh`. Mọi trường hợp khác giữ nguyên chữ base. Các mẫu `DOT_BIEN` hiện có của tệp test giữ khớp đúng một chỗ. | `.claude/dev/mcp_github_doc.py` |
| M9 | `mcp_github_doc_test.py`: ca mới `t18_5xx_khong_header_la_loi_truyen_tai_khong_phai_proxy` (đăng ký `@ca`, dùng `_MayChuGia`/`_urlopen_gia`/`_hong` sẵn có): (a) 502 không header ⇒ `Hong`, mô tả chứa `502`, `loi truyen tai`, không chứa `proxy tu sinh`; (b) 503 không header ⇒ như (a); (c) 403 không header ⇒ mô tả chứa `proxy tu sinh`; (d) 502 CÓ header GitHub ⇒ mô tả chứa `thieu quyen`. Một đột biến mới trong `DOT_BIEN` của tệp này, `r1313_mcp_doc_5xx_ve_proxy` (gỡ nhánh 5xx của M8), ca đích `t18_5xx_khong_header_la_loi_truyen_tai_khong_phai_proxy`. | `.claude/dev/mcp_github_doc_test.py` |
| M7 | Ca mới `r1313_canh_gh_chi_noi_chan_khi_kho_chan`: nạp qua `_tai_launcher_thu()`, giả `_git` (origin GitHub), `gh auth status` thành công và `_do_rest_github` theo khuôn `t103`/`t115`; khẳng định: (a) `rest-kho` trả `khong_do_duoc` (502) ⇒ đầu ra KHÔNG chứa `duong kho bi chan`; (b) `rest-kho` trả `mo` thiếu quyền (404 có header) ⇒ không chứa; (c) `rest-kho` trả `chan` (403 không header) ⇒ CÓ chứa. Khôi phục mọi thứ đã giả trong `finally`. | `.claude/dev/launcher_test.py` |
| M5 | Bốn đột biến mới trong `DOT_BIEN`, mỗi cái nhắm đúng một chỗ: `r1313_rest_5xx_ve_chan` (gỡ điều kiện 5xx của M1, đưa nhánh về hành vi base) ca đích `["r1313_rest_5xx_khong_header_la_khong_do_duoc"]`; `r1313_mcp_5xx_ve_chan` (gỡ điều kiện 5xx của M2) ca đích `["r1313_mcp_endpoint_5xx_khong_header_la_khong_do_duoc"]`; `r1313_rest_mo_ta_noi_chan` (giữ trạng thái M1 nhưng đổi riêng mô tả thành câu kết luận proxy chặn) ca đích ca M3; `r1313_canh_kho_gop_moi_that_bai` (đưa điều kiện cảnh báo M6 về suy từ `not ok`) ca đích `["r1313_canh_gh_chi_noi_chan_khi_kho_chan"]`. Mẫu `(tìm, thay)` lấy nguyên văn từ dòng đã viết; mỗi mẫu khớp đúng một chỗ. | `.claude/dev/launcher_test.py` |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Ba ca M3, M4, M7 ĐẠT trên head (Linux, Python 3.13 của gate và 3.11 nếu có); `t103`, `t110`, `t115`, `t143`, `t117` vẫn ĐẠT. | Mỗi đột biến M5 qua runner `DOT_BIEN` ⇒ ca đích ĐỎ tại `bang(...)`, runner ghi `OK giet 1/1` (không phải `loi`/`bo_qua`). Runner chỉ chạy ca đích, nên thêm MA TRẬN CHÉO: trên bản sao mang từng đột biến, chạy cả ba ca mới bằng `--lap-ca`: ca đích ĐỎ bằng `TinHieuChotCa` ở vế mong đợi, hai ca kia ĐẠT; ghi đủ 4 × 3 ô. Đối chứng biên trên bản sao: ngưỡng M1 `500 <=` thành `500 <` ⇒ vế (c) của M3 ĐỎ; thành `400 <=` ⇒ vế (d)/(e)/(h) ĐỎ; bỏ cận `< 600` ⇒ vế (g) ĐỎ. |
| N2 | Bộ đột biến của `launcher_test.py` trên CI giết bốn đột biến M5 đúng ca đích (bán kính đột biến báo `giet 1/1` cho mỗi cái), và các đột biến hiện có ở §0 vẫn `giet`. | Bỏ đăng ký một ca ⇒ runner báo `SAI - ca dich khong tim thay/trung`; trên bản sao, gỡ TOÀN BỘ khẳng định phân loại 5xx-không-header (vế (a)–(c)) của ca M3, giữ các vế còn lại ⇒ `r1313_rest_5xx_ve_chan` SỐNG (gỡ riêng một vế KHÔNG đủ: hai vế 5xx còn lại vẫn giết, đo ở review lượt 1); gỡ riêng các khẳng định mô tả của ca M3 ⇒ `r1313_rest_mo_ta_noi_chan` SỐNG. |
| N3 | Hành vi ngoài phạm vi không đổi trên một TẬP CA ĐÓNG: danh sách các ca ĐÃ CÓ ở base có tên chứa `rest`, `mcp_endpoint`, `github` hoặc là `t103`/`t115` (liệt kê tên trong báo cáo). Chạy tập ấy bằng `launcher_test.py` của base trên cây base, và bằng `launcher_test.py` của head trên cây head; so từng ca đạt/đỏ/bỏ qua. Ba ca r1313 không thuộc tập này; hành vi base của chúng được đo gián tiếp qua các đột biến M5 (đưa mã về hành vi base thì ca ĐỎ). Phép so này KHÔNG chứng minh mọi hành vi ngoài phạm vi được phủ. | Một ca trong tập đạt trên base mà đỏ hay bỏ qua trên head. |
| N6 | `python .claude/dev/mcp_github_doc_test.py` ĐẠT N/N trên head (đủ ca cũ cộng `t18`); `python .claude/dev/mcp_github_doc_test.py --dot-bien` báo mọi đột biến (cũ và `r1313_mcp_doc_5xx_ve_proxy`) giết thật, rc 0. | Đột biến `r1313_mcp_doc_5xx_ve_proxy` ⇒ `t18` ĐỎ bằng `TinHieuChotCa` (runner xếp `giet`, không `tin_dung_gia`); trên bản sao gỡ các khẳng định vế (a)–(b) của `t18` ⇒ đột biến SỐNG, runner rc 1. |
| N4 | Đo trên exact head, ghi lệnh + mã thoát + bằng chứng dương: `ruff --select F` delta 0 trên bốn tệp; `doctrine-scan`, `adr-song` rc 0; `git diff --check` sạch; `git diff --numstat base..H` đúng 4 tệp, ≤ 450 dòng thêm (`ADR-0053`). | Phản chứng lint: thêm một tên chưa định nghĩa ⇒ delta ≠ 0; phản chứng phạm vi: thêm đường dẫn thứ năm ⇒ numstat 5 tệp. `doctrine-scan`/`adr-song`: không có phản chứng riêng ở packet này — khai thẳng. |
| N5 | `python .claude/dev/launcher.py doctor` chạy trọn trên head (rc như base) và dòng `github` vẫn in đủ các đường. | rc khác base, hay thiếu một đường trong dòng `github`. |

## 5. `pham_vi_e`

Không chạm E4, không chạm E5.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Cần sửa ngoài write set, hoặc thấy một chỗ KHÁC cùng phân loại hay cùng suy diễn "thất bại ⇒ bị chặn" ngoài các chỗ đã liệt kê ở §0 (hai hàm và cảnh báo `kho_chan` của `launcher.py`, `Phien._post` của `mcp_github_doc.py`) ⇒ dừng triển khai và đi revision đặc tả. Tầm quét tối thiểu khi preflight: `rg -n 'x-github' --glob '!*.md' --glob '!ops/**'` trên base.
- Đặc tả không thuộc Mission nên chờ chủ kho duyệt băm theo `ADR-0067` — **E2**.

## 7. `hinh_dang_ke_thua`

`khong_ap_dung` — sửa phân loại, không phải packet khắc phục một bản vá cũ.

## 8. `chua_do_duoc`

- Không tái hiện được 502 thật của proxy theo ý muốn; ca dùng `HTTPError` giả. Mô tả 502 thật lấy từ đo đạc ghi trong #1313.
- Kích thước ước lượng tĩnh: 130–220 dòng thêm cho hai tệp launcher (review độc lập lượt 1, 17-11-2026) cộng khoảng 30–50 dòng cho hai tệp `mcp_github_doc*`; 4 tệp, trong trần `ADR-0053`. Đo lại bằng numstat trước khi công bố.

## 9. `lich_su_revision`

- r1 → r2 (review độc lập Codex lượt 1, `request_changes`, 5 P2): F1 phản chứng N2 sửa thành gỡ toàn bộ vế 5xx; F2 thêm ma trận chéo vào N1; F3 thêm M6 + M7 + đột biến cho cảnh báo `kho_chan` ở người gọi; F4 N3 chốt tập ca đóng và tách ba ca mới; F5 khẳng định đủ bốn điều cho vế 5xx, thêm đột biến mô tả. Kèm: dải `500 <= mã < 600`, vế 600 và 429 (giới hạn cố ý), ràng buộc giữ neo các đột biến cũ, mốc giờ đo chính xác.
- r2 → r3 (executor g1 dừng ở preflight theo §6, 18-11-2026; chủ kho chọn "Làm r3 gộp luôn"): thêm chỗ thứ ba `mcp_github_doc.py` `Phien._post` vào §0 và write set (M8, M9, N6); luật dừng §6 liệt kê đủ các chỗ và tầm quét preflight; ghi chú M6 của executor: `tt_kho` phải có giá trị (vd. `None`) ở nhánh không đọc được slug.
