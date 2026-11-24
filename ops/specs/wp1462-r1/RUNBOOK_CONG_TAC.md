# Runbook công tắc giảm G5 (wp1462, B4 của Mission #1172)

Tài liệu dev-side. Mọi mục dưới đây là QUY TRÌNH của người; không cổng nào kiểm. Nguồn hợp đồng: `ops/specs/wp1462-r1/SPEC.md` (mục 2–9) và kế hoạch nguồn r4 §4 A+1, §10 Q9. Hai công tắc (biến Actions mức kho của `ducthangho/tra-luat`), mặc định ĐÓNG:

| Lớp giảm | Biến | Chuỗi cho phép (so từng byte) |
|---|---|---|
| `bo_moi` (PR3) | `TL_GIAM_G5_BO_MOI` | `cho-phep-bo-moi-pr3` |
| `che_do_dich` (PR6) | `TL_GIAM_G5_CHE_DO_DICH` | `cho-phep-che-do-dich-pr6` |

Đóng một lớp = xoá biến của lớp ấy hoặc đặt bất kỳ giá trị nào khác chuỗi cho phép; có hiệu lực ở lượt CI kế tiếp và ở lần `kiem-merge` kế tiếp, không cần merge gì.

1. **Phải đóng ngay khi:** lỗi P0/P1 lọt qua một lượt giảm; bộ phân loại hoặc job gom kết luận sai; release dùng sai H; watchdog B2 báo `stale_or_missing`; audit đỏ chưa khoanh được vùng. Không khoanh được sự cố thuộc lớp nào thì đóng MỌI lớp.
2. **Sau khi đóng:** đọc lại giá trị (readback REST của đúng biến) và ghi vào Issue sự cố, kèm thời điểm đọc.
3. **Điều kiện bật lại** (chép đúng §4 A+1): điều tra có kết luận ghi trong Issue sự cố; full audit (`ci-dot-bien-du.yml`) `success` trên các H bị ảnh hưởng đã khoanh trong Issue ấy và trên đầu `master` lúc bật lại — khi full audit chưa mang G5 (trước PR5) thì kèm G5 đủ `success` trên chính các H ấy; và quyết định mới bằng văn bản của chủ kho. "Chính các H ấy" gồm TỪNG H bị ảnh hưởng VÀ đầu `master` lúc bật lại. Điều khoản G5 đủ còn hiệu lực cho tới khi `ci-dot-bien-du.yml` thật sự chạy G5 (tại nền của đặc tả, workflow ấy không có bước nào chạy `ops/cong_cu_test.py`). Lấy bằng chứng ấy không được phá trần: lượt `ci.yml` đủ trên một H không có sẵn chỉ tạo được bằng đường ở mục 8, mỗi lượt cần chủ kho cho phép riêng và tính vào ngân sách CI/Windows hiện hành.
4. **Phiên AI không ghi biến công tắc** — không tạo, không sửa, không xoá, ở bất kỳ giá trị nào. Mã B4 chỉ gửi GET.
5. **`kiem-merge` là bước cuối trước khi đề nghị merge.** Phán quyết (β) — dòng `CONG_TAC … trang_thai=khop` kèm `HIEU_LUC den=…` — dùng trong 30 phút kể từ `doc_luc`; quá thì chạy lại. Ai đổi công tắc thì mọi phán quyết xanh đang chờ merge hết hiệu lực. Máy không cưỡng chế cửa sổ này.
6. **Siết (không cần quyền ghi biến).** `kiem-merge … --siet-g5-du`: đòi G5 đủ `success` trên đúng H, tắt cả (α) lẫn (β); ai chạy `kiem-merge` cũng dùng được. Biến môi trường `PACKET_LOOP_CAM_DOC_CONG_TAC` khác rỗng: không gửi yêu cầu, công tắc ở `khong_doc_duoc` (mọi PR thuộc (β) bị đòi G5 đủ). Không có cờ hay biến nào theo chiều ngược lại.
7. **Bảng W và bảng máy** lấy từ bản ghi phép đo Q9(a) `ops/specs/wp1462-r1/do/DO_Q9A.yaml` (nhánh `ops/wp1462-r1`); bản ghi ấy phải có trước khi BẤT KỲ ai đặt chuỗi cho phép. Trạng thái lúc viết runbook (20-11-2026):

   | Hàng | Kết quả |
   |---|---|
   | Tập W (cộng tác viên, GitHub App, token, `GITHUB_TOKEN` của workflow) | `khong_do_duoc` — chưa có bản ghi ⇒ mọi hàng tính là THUỘC W |
   | Phiên cloud Linux — đọc công tắc | không đọc được (403 do proxy, 0 header `x-github-`; đo 16:19:34Z 20-11-2026) ⇒ `khong_doc_duoc` |
   | Phiên cloud Linux — chạy bộ phân loại của `master` | đạt (60/60 khớp bảng kỳ vọng) |
   | Máy bàn Windows của chủ kho (máy được chỉ định cho phán quyết (β)) | `khong_do_duoc` — chưa đo |

   Luật: W chưa đo xong hoặc còn thành viên chủ kho không chấp nhận ⇒ không đặt chuỗi cho phép. Máy chưa đo, đo thấy đọc phải bản cũ, hoặc (với máy Windows) chưa chạy các ca `cong_b4_*` ⇒ không dùng cho phán quyết (β).
8. **Tạo một lượt G5 đủ trên H.** Với PR `duong_nhanh` hôm nay chỉ có dispatch `ci.yml` với `che_do=day_du`, kéo theo job Windows ⇒ mỗi lần dùng cần chủ kho cho phép riêng.
9. **Đầu vào của `kiem-merge`.** Readback `--workflow-jobs` phải là REST thô có trường `steps` (thiếu `steps` ⇒ không có bằng chứng G5 đủ). `kiem-merge` phải chạy từ cây trùng `origin/master` vừa fetch (`git fetch origin master`): nó tự kiểm `ls-remote` và blob của chính `packet_loop.py`, lệch thì từ chối; nó KHÔNG tự fetch.
10. **Rủi ro tồn dư Q9(d)** (chép đúng §10): (i) Máy không chứng minh được lần đặt `CHO_PHEP` là quyết định của chủ kho: mọi thành viên của W đều đặt được. (ii) Điều kiện bật lại sau sự cố của r2 §5.5 (điều tra, bằng chứng đủ trên H bị ảnh hưởng, quyết định mới) là runbook; không cổng nào kiểm. (iii) Giữa lúc `kiem-merge` đọc công tắc và lúc bấm merge có một khoảng máy không canh; lớp bù là lượt push `day_du` sau merge, tức phát hiện sau. (iv) "Phiên AI không ghi biến công tắc" là cấm theo quy trình.
