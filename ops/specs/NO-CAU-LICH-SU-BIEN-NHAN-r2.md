# Đặc tả packet — `NO-CAU-LICH-SU-BIEN-NHAN` (revision 2)

- `packet_id`: **NO-CAU-LICH-SU-BIEN-NHAN** · `packet_issue`: **#960** · `revision`: **2** · soạn 27-10-2026 bằng skill `soan-spec`
  (phiên `session_015GtxrbeTfDyFKdj7rb72Uq`, chính là phiên executor r1). Chủ kho chốt Q1–Q9 "theo khuyến nghị" lúc 12:55Z 27-10.
- Executor/reviewer: chủ kho định tuyến lúc cấp lease. Đặc tả giả định reviewer khác họ executor ⇒ `assurance_target: cross_approved`.
- `nguon_cap_viec`: khắc phục — packet cha là r1 của chính #960 (PR #976, merge `20a2e2b`). Nguồn finding:
  `ops/reviews/wp960-review-2-codex-verdict.md` (sha256 `ad6b7d52…`, 7 finding mở) và handoff `ops/handoff/wp960-g1-claude.md` trên
  nhánh `ops/wp960-r1-g1-lease` @ `0cc545e`.
- `review_class`: **systemic** (cổng đọc toàn bộ sổ biên nhận). Cổng lease tính `ops/**` ⇒ `sensitive`; lấy mức cao hơn.
- Base dự kiến: nhánh mặc định lúc cấp lease (đo 12:55Z 27-10: `20a2e2b`). Đo lại khi cấp lease.

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
luat_push_va_dung_va: ADR-0054@7cc384ec9e02ed79b429ac6ee2455d3bfbb75b16

(Q9: ngân sách lời gọi Codex của r2 đếm lại từ 0, trần 8 theo `ADR-0052`. Đo 12:55Z 27-10: `ADR-0054` CHƯA kích hoạt — `rg -l
'kích hoạt \`ADR-0054\`' docs/adr/` chỉ ra chính tệp ADR ⇒ dòng `luat_push_va_dung_va` vô hiệu, giữ để đúng khuôn r1.)

## Vấn đề (một đoạn)

R1 thêm ba luật SỰ THẬT (L-REVIEW, L-ANCESTRY, L-SURFACE) vào `ops/bien_nhan_v2.py`. Hai lượt codex trên r1 đều ra
`changes_requested`; lượt 2 còn **7 finding** (đơn vị: finding, mục `### <slug> [P*]` của verdict). Cả 7 thuộc ba hình dạng đã lặp ở
ba lượt review (bảng `hinh_dang_ke_thua`), nên r1 dừng theo chốt. R2 đóng các hình dạng ấy bằng KIẾN TRÚC chứ không vá từng đường:
bỏ hẳn mốc `dung_tai` (xoá lớp "nguồn gốc câu"), một biên duy nhất cho lỗi đo, và định nghĩa hẹp cho lời tự khai surface.

## `write_set`

`ops/bien_nhan_v2.py` · `ops/bien_nhan_v2_test.py`

(Đo 12:55Z 27-10, `ai-dang-giu` sau khi đồng bộ đủ ref: cả hai ⇒ `NGƯỜI_GIỮ 1: wp960-r1-g1-claude`, lease r1 còn hạn tới
2026-10-29T07:22Z. Lease r2 phải khai `thay_the_cho` và đặt bia mộ `da_bi_thay_the` vào lease r1 nếu r1 còn hạn lúc cấp.)

## `ngoai_pham_vi`

| thứ | vì sao |
|---|---|
| Sửa biên nhận `ops/reviews/*.receipt.yaml`, kể cả caveat dương tính giả trên `wp960-review-{1,2}` | Q6: caveat ghi đúng sự thật lúc ghi sổ; sửa biên nhận phải mở write set. |
| `ops/land/*`, `ops/land_evidence_nguon.py` | như r1 (nợ `NO-CAU-LICH-SU-LAND-EVIDENCE`). |
| `.github/workflows/ci.yml` | cổng đã chạy trong CI; không thêm bước. |
| Theo dõi đổi tên / lịch sử tệp | mốc bị bỏ (M1) ⇒ không còn phép đo nào cần lịch sử tệp. |
| Đột biến riêng cho khối `>-` | Q7: thư viện YAML gấp dòng trước khi cổng thấy; cổng không có chốt cho nó. |

## `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| M1 | **Bỏ mốc `dung_tai`** (Q2): L-REVIEW và L-ANCESTRY không còn ngoại lệ nào; xoá mã đọc mốc và truy lịch sử tệp. | `ops/bien_nhan_v2.py` |
| M2 | **Một biên lỗi đo** (Q3): mọi lỗi đọc / phân tích / gọi git trong ba luật VÀ khi băm-đọc receipt ⇒ KHÔNG ĐO ĐƯỢC (rc=2), không traceback; mục nợ đang KHÔNG ĐO ĐƯỢC không được kết luận là nợ chết. | `ops/bien_nhan_v2.py` |
| M3 | **OID theo ngữ cảnh** (Q4): token không tra được commit ⇒ KHÔNG ĐO ĐƯỢC khi token đủ 40 hex, HOẶC trộn chữ số và chữ cái, HOẶC nằm trong backtick, HOẶC đứng ngay sau từ `commit`; còn lại (thuần số / thuần chữ, không ngữ cảnh) bỏ qua. Token tra ra commit luôn là ứng viên. | `ops/bien_nhan_v2.py` |
| M4 | **Lời tự khai surface** (Q5, phương án a): một khai báo `execution[_ ]surface` chỉ là lời TỰ KHAI khi trong cửa sổ {dòng trước, dòng ấy, dòng sau} có từ `provider` VÀ không có trích dẫn dạng `đường/dẫn.ext:N`. L-SURFACE chỉ so lời tự khai với `run.json`. | `ops/bien_nhan_v2.py` |
| M5 | **Sinh lại `NO_CAU_LICH_SU`** trên base của lease r2 (cả hằng trong cổng lẫn bản đóng băng trong test); bánh cóc chỉ co giữ nguyên. | `ops/bien_nhan_v2.py` · `ops/bien_nhan_v2_test.py` |
| M6 | Ca test cho M1–M5, đột biến cho từng chốt, gỡ các ca/đột biến của mốc. | `ops/bien_nhan_v2_test.py` |

## `nghiem_thu`

Mọi ca dựng kho git THẬT có lịch sử (`_kho_cau` / `_kho_surface`, ngày commit ghim) rồi đổi đúng MỘT yếu tố. Đột biến chạy trên
bản sao ngoài kho; phải giết ĐÚNG ca đích bằng `TinHieuChotCa` (không lĩnh tín dụng từ lỗi vô can). Cột "nền" là kết quả chạy
thử trên `20a2e2b` lúc 12:55Z 27-10 bằng script dựng từ fixture có sẵn.

| # | tiêu chí | phép đo làm nó ĐỎ | nền |
|---|---|---|---|
| B1 (M1) | Câu ancestry có OID đã là tổ tiên + `dung_tai: <B0>` hợp lệ ⇒ **rc=1**. Câu "chưa review lại" + `dung_tai` hợp lệ + biên nhận sau cùng SHA ⇒ **rc=1**. `rg -n '"dung_tai"\|def _moc_\|def _commit_them_cau\|def _co_cau' ops/bien_nhan_v2.py` ⇒ **0 dòng** (vế âm; chú thích nhắc tên mốc để giải thích việc bỏ thì được phép) — vế dương là hai ca rc=1 ở trên. | Đột biến chèn lại phép miễn khi mapping có `dung_tai` ⇒ hai ca xanh (ĐỎ). | rc=0 (chưa làm) |
| B2 (M2) | Bốn nguồn hỏng, mỗi nguồn một fixture, mỗi fixture chạy CẢ khi có lẫn khi không có mục nợ tương ứng: receipt là THƯ MỤC tên `*.receipt.yaml` (I/O khi băm); run.json có mà JSON lỗi; nhánh mặc định là một tree (`merge-base` rc ngoài 0/1); alias YAML vòng ⇒ đều **rc=2**, stderr không chứa `Traceback`, không dòng `NỢ CHẾT`. | Đột biến gỡ biên (cho ngoại lệ lọt ra / trả rc=1) ⇒ ca đỏ. | receipt-thư-mục ⇒ chết `IsADirectoryError` (chưa làm) |
| B3 (M3) | OID thiếu: `aaaa…a` (40) ⇒ rc=2 · `` `abcdefa` `` ⇒ rc=2 · `commit 1234567` ⇒ rc=2 · `12ab34c` (trộn) ⇒ rc=2. Đối chứng bỏ qua: `deadbeef` và số run `40268583940` không ngữ cảnh ⇒ rc=0. Giữ ca OID thật toàn số / toàn chữ (tiền tố tất định) ⇒ rc=1. | Đột biến bỏ luật ngữ cảnh (mọi token thuần bị bỏ qua) ⇒ ca backtick xanh (ĐỎ); đột biến coi mọi token thuần là bắt buộc ⇒ ca `deadbeef` rc=2 (ĐỎ). | 40-hex ⇒ 0, backtick ⇒ 0 (chưa làm); `deadbeef` ⇒ 0 (đối chứng đã đúng) |
| B4 (M4) | run.json `codex_cli`: (i) `provider: openai_codex` + dòng sau `execution_surface: codex_service`, thiếu caveat ⇒ rc=1; (ii) dòng trước là `ops/x/v.md:6`, dòng sau khai `provider … execution surface codex_service` ⇒ rc=0; (iii) `execution_surface: codex_service` không có `provider` trong cửa sổ ⇒ rc=0; (iv) hai khai báo cùng dòng có `provider` (cả hai thứ tự) ⇒ rc=1. | Đột biến bỏ điều kiện `provider` ⇒ (iii) đỏ; bỏ điều kiện trích dẫn ⇒ (ii) đỏ; chỉ xét khai báo đầu dòng ⇒ (iv) đỏ. | (i) 1 · (ii) 1 · (iii) 1 (hai ca sau: chưa làm) |
| B5 (M5) | Trên base và trên head: `python3 ops/bien_nhan_v2.py --root .` rc=0 `TỔNG: ĐẠT`; nợ rỗng ⇒ rc=1 với đúng `len(NO_CAU_LICH_SU)` dòng ba luật (giữ ca kiểu `c76`); dòng tổng kết in số nợ từng luật. Nợ L-SURFACE kỳ vọng **0** (đo 12:55Z 27-10: quy tắc M4 bắt 7 lời tự khai trong 20 verdict có run.json, 6 khác `codex_cli` đều đã có caveat). Mọi mục nợ trỏ tệp có thật; danh sách ⊆ bản đóng băng trong test. | Danh sách nợ rỗng không ra rc=1 ⇒ luật mù (ĐỎ). Đột biến nở thêm một mục ⇒ ca bánh cóc đỏ. | — (hằng sinh lúc thi hành) |
| B6 (A3 r1, Q7) | Khối `\|` gãy dòng bị nhận và có đột biến `m78` (khớp từng dòng) làm đúng trường ấy đỏ; khối `>-` là ca hồi quy, docstring khai thẳng không có chốt trong cổng. | `m78` không còn giết trường `\|` ⇒ ĐỎ. | đã có từ r1 |
| B7 (cả packet) | `python ops/bien_nhan_v2_test.py` N/N với hai số BẰNG NHAU, mọi đột biến thường CÓ RĂNG; ruff `--select F` delta 0 so base; `doctrine-scan` rc=0; `git diff --check` rc=0; `git diff --numstat` base..head ghi vào PR và đối chiếu ADR-0044. | Bất kỳ ô nào khác ⇒ ĐỎ. | 85/85 · 95/95 trên `20a2e2b` |
| B8 (nền) | Trước khi bắt tay: B1–B4 trên base phải ra đúng cột "nền" ở trên. | — (canh nền; răng từ B1–B5). | đã chạy 12:55Z 27-10 |

## Luật viết đi kèm (Q2)

Biên nhận KHÔNG viết câu trạng thái kèm OID ("X chưa vào master", "head H chưa được review lại"). Lịch sử ghi ở thì quá khứ và không
gắn OID vào chính câu trạng thái. Lý do: bỏ mốc ⇒ một câu như vậy thành vi phạm ngay khi trạng thái đổi, và CI đỏ trên một biên nhận
không ai đụng. Luật này chỉ ghi ở đây và trong docstring cổng; KHÔNG có cổng riêng ép viết (chính L-REVIEW/L-ANCESTRY là cổng).

## `hinh_dang_ke_thua`

Chép từ handoff r1 và `ops/reviews/wp960-review-{1,2}-codex-verdict.md` (đơn vị: finding; "lượt" = một lượt review):

| hình dạng | connector `7ae7fc1` | codex lượt 1 `7ae7fc1` | codex lượt 2 `916a60a` |
|---|---|---|---|
| lỗi ĐO thành sạch/vi phạm | run.json hỏng | surface hỏng · alias vòng | lịch sử hỏng · I/O khi băm · OID thiếu |
| bộ chọn ứng viên (regex) bỏ sót/bắt nhầm | OID toàn số · dòng trích dẫn | OID toàn chữ · khai báo thứ hai | tham chiếu miễn nhầm · ba nợ trích dẫn |
| nguồn gốc câu cho mốc `dung_tai` | blame cả scalar | đổi khoảng trắng | đổi tên tệp |

Mỗi hình dạng đã có **3** lượt. Q8: nếu một hình dạng xuất hiện ở BẤT KỲ lượt review nào của r2 (lần thứ 4) ⇒ DỪNG và hỏi chủ kho.
Hình dạng thứ ba bị xoá theo kiến trúc (M1); xuất hiện lại dưới dạng khác cũng tính.

## Kích thước dự kiến

Ước (chưa đo): +250/−250 trên 2 tệp so base. Căn cứ đo 12:55Z 27-10: phần mốc ≈ 57 dòng sản phẩm + ≈ 53 dòng ba ca `c80`/`c81`/`c85`
(chưa kể ca mốc trong `c69`/`c71` và đột biến m86/m87/m90/m93) sẽ bị gỡ. Đối chiếu ngưỡng ADR-0044 cho packet không chạm authority
(≤ 6 tệp, ≤ 1.000 dòng thêm cộng xoá); vượt thì khai theo đúng ADR ấy trong PR.

## `chua_do_duoc`

- **Số nợ L-REVIEW / L-ANCESTRY sau khi bỏ mốc**: chưa đo; trên `20a2e2b` không biên nhận nào mang `dung_tai` (r1 mới có cơ chế), nên
  dự kiến giữ 1 / 60 — chỉ có khi luật chạy trên base của lease.
- **M4 là heuristic**: lời tự khai không có từ `provider` trong cửa sổ ba dòng sẽ không bị đối chiếu. Đo 12:55Z 27-10 trên 20 verdict:
  7/7 lời tự khai đã biết đều bắt được, 0 bắt nhầm; tập ngoài 20 verdict ấy chưa đo.
- **M3 trên dữ liệu thật**: 3 token thuần không tra được trong câu ứng viên, không token nào có ngữ cảnh ⇒ 0 mục rc=2 mới (đo
  12:55Z 27-10). Văn xuôi viết sau này chưa đo.
- **Regex chọn ứng viên** vẫn không chứng minh phủ mọi cách viết tay (như r1).
