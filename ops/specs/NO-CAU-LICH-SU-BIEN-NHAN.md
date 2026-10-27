# Đặc tả packet — `NO-CAU-LICH-SU-BIEN-NHAN` (revision 1)

- `packet_id`: **NO-CAU-LICH-SU-BIEN-NHAN** · `packet_issue`: **#960** · `revision`: **1** · soạn 27-10-2026 bằng skill `soan-spec`
  (phiên `session_01WZT2MvvoQV8QGF1vX9STrJ`; chủ kho chốt Q1–Q12 "theo khuyến nghị" và xác nhận đã hiểu giống nhau, đóng băng 27-10-2026) · executor/reviewer: **chưa định tuyến**,
  do chủ kho chọn lúc cấp lease. Reviewer khác họ executor ⇒ `assurance_target: cross_approved`.
- `nguon_cap_viec`: khắc phục — nợ `NO-CAU-LICH-SU-BIEN-NHAN` ghi ở khối `no_con_mo_20261027` của
  `ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml` (master `597a6cb`, merge #959); đề xuất ở Issue #960.
- `review_class`: **systemic** — cổng mới chạm cách đọc toàn bộ sổ biên nhận, không chạm `ci.yml`, credential, hay gói phát hành.
- Base dự kiến: nhánh mặc định lúc cấp lease (đo lại 06:35Z 27-10: `7129f7d`; gate trên `a195b95` run 40454280949 xanh 23/23).

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
luat_push_va_dung_va: ADR-0054@7cc384ec9e02ed79b429ac6ee2455d3bfbb75b16

## Vấn đề (một đoạn)

Biên nhận review và caveat chứa câu **phụ thuộc trạng thái** — "chưa review lại", "chỉ là một nhánh / không phải tổ tiên
master", "surface `codex_service`" — đúng lúc ghi nhưng sai sau đó. Không cổng nào bắt: `bien_nhan_v2`,
`land_evidence_nguon`, `t26`/`t27`/`t138` đều xanh khi câu ấy sai. Chuỗi review #896 tốn **8 lượt** codex (lượt 2–8) và
**6 lần áp HINT** để vá tay; mỗi lượt quét rộng hơn lại tìm thêm thể hiện mới. Packet này đổi việc VÁ TAY thành một
PHÉP ĐO trong cổng sẵn có.

## `write_set`

`ops/bien_nhan_v2.py` · `ops/bien_nhan_v2_test.py`

(Đo lại 06:35Z 27-10: `ai-dang-giu` cả hai ⇒ `NGƯỜI_GIỮ 0`. Đo lại trước khi cấp lease.)

## `ngoai_pham_vi`

| thứ | vì sao |
|---|---|
| `ops/land/*-land-evidence.yaml` | YAML tự do, mỗi hồ sơ một khuôn; `ops/land_evidence_nguon.py` đang bị lease `land-evidence-l7-r1-g1-claude-remote-20261027` giữ (đo lại 06:35Z 27-10). Ghi thành nợ con `NO-CAU-LICH-SU-LAND-EVIDENCE` (Q1). |
| `.github/workflows/ci.yml` | `bien_nhan_v2` đã chạy trong CI (ci.yml dòng 666, 712); không thêm bước (Q2). |
| `_TRANSPORT_CONTRACTS`, hợp đồng surface | thuộc #461 (Q5). |
| Sửa byte của verdict/biên nhận lịch sử | hiện vật neo băm; nợ tồn đi qua danh sách đóng băng (Q4). |
| Biên nhận không có `run_json` trỏ tệp trong kho | không có nguồn để phân xử surface (Q11) — xem `chua_do_duoc`. |

## Định nghĩa dùng chung

- **Mốc** (Q7): trường có cấu trúc `dung_tai: <oid40>` đặt trong CÙNG mapping YAML chứa câu (caveat, `anchor`, hoặc mapping
  cha của trường văn bản). Hợp lệ khi `<oid40>` là object commit có trong kho VÀ là tổ tiên của commit đầu tiên thêm câu ấy
  (đo bằng `git log --diff-filter=A`/blame trên tệp). Mốc chỉ miễn cho câu của mapping đó.
- **Ba trạng thái** của cổng giữ nguyên: `0` sạch · `1` vi phạm · `2` KHÔNG ĐO ĐƯỢC (`RC_KHONG_DO_DUOC`).

## `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| M1 | Luật **L-REVIEW**: trong một biên nhận, câu khẳng định head `H` (OID 40 ký tự trong cùng câu) "chưa/không được review (lại)" là **vi phạm** khi tồn tại biên nhận khác trong `ops/reviews/` có `reviewed_sha == H` (khớp đúng 40 ký tự, không suy hậu duệ) và `luot` lớn hơn — trừ khi mapping có mốc hợp lệ (Q8). | `ops/bien_nhan_v2.py` |
| M2 | Luật **L-ANCESTRY**: câu dạng ancestry ("chỉ là một nhánh", "không phải tổ tiên", "chưa ở/tới master", "canonical inclusion pending" và các biến thể không dấu) chứa OID `X` là **vi phạm** khi `git merge-base --is-ancestor X <nhánh mặc định>` rc=0 và mapping không có mốc. OID không tra được ⇒ **KHÔNG ĐO ĐƯỢC** (`rc=2`) (Q9). | `ops/bien_nhan_v2.py` |
| M3 | Luật **L-SURFACE**: biên nhận có `model_reviewer_identity.run_json` trỏ tệp có trong kho và tệp ấy có `execution_surface = S`; verdict (`verdict_path`) có dòng khớp `execution[_ ]surface` kèm giá trị surface `S' ≠ S` ⇒ biên nhận phải có caveat id `VERDICT-KHAI-SAI-EXECUTION-SURFACE`; thiếu ⇒ **vi phạm** (Q11). | `ops/bien_nhan_v2.py` |
| M4 | **Danh sách nợ đóng băng** (Q10): executor chạy M1–M3 trên base SHA của packet, ghi mọi vi phạm hiện có (tệp + đường dẫn trường + luật) thành hằng trong `bien_nhan_v2.py`, cùng cơ chế `NO_DA_DO`. Bất biến: danh sách CHỈ được giảm; mục nợ mà câu đã hết vi phạm ⇒ **vi phạm** (nợ chết phải xoá); mục mới ngoài danh sách ⇒ **vi phạm**. Dòng tổng kết CLI in thêm số nợ của luật mới. | `ops/bien_nhan_v2.py` |
| M5 | Ca test cho M1–M4 và đột biến cho từng chốt. | `ops/bien_nhan_v2_test.py` |

## `nghiem_thu`

Mỗi ca dựng fixture dương đầy đủ trong thư mục tạm (kho git tạm có lịch sử thật), rồi đổi đúng MỘT yếu tố. Mỗi ca có một
đột biến (trên bản sao ngoài kho) gỡ đúng chốt ấy làm ca **ĐỎ**; tiêm danh sách nợ qua tham số `kiem(…)` sẵn có.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| A1 (M1) | Câu "chưa review lại" + có biên nhận sau cùng `reviewed_sha`, `luot` lớn hơn ⇒ `rc=1`; cùng câu mà biên nhận sau có `reviewed_sha` KHÁC một ký tự ⇒ `rc=0`; cùng câu + `dung_tai` hợp lệ ⇒ `rc=0`. | Đột biến bỏ phép so `reviewed_sha` ⇒ ca thứ nhất xanh (ĐỎ). Đột biến so bằng tiền tố 7 ký tự ⇒ ca thứ hai đỏ sai (ĐỎ). |
| A2 (M2) | Câu ancestry chứa OID đã là tổ tiên ⇒ `rc=1`; OID chưa là tổ tiên ⇒ `rc=0`; OID không tồn tại ⇒ `rc=2`; + `dung_tai` hợp lệ ⇒ `rc=0`; `dung_tai` trỏ OID KHÔNG là tổ tiên của commit thêm câu ⇒ `rc=1`. | Đột biến coi OID thiếu là "không tổ tiên" ⇒ ca `rc=2` thành `rc=0` (ĐỎ). Đột biến bỏ kiểm tổ tiên của mốc ⇒ ca cuối xanh (ĐỎ). |
| A3 (M2, L6-b/d) | Biến thể có dấu / không dấu / xuống dòng trong scalar folded `>-` đều bị nhận; câu chỉ NHẮC cụm từ trong ngoặc trích của finding mà không chứa OID ⇒ không phải vi phạm. | Đột biến khớp theo từng dòng thay vì scalar đã nối ⇒ ca xuống dòng xanh (ĐỎ). |
| A4 (M3) | Run.json `codex_cli` + verdict khai `codex_service` + thiếu caveat ⇒ `rc=1`; có caveat ⇒ `rc=0`; verdict khai đúng `codex_cli` ⇒ `rc=0`; `run_json` trỏ tệp không có ⇒ luật không áp (không vi phạm, đếm vào `chua_do_duoc` của dòng tổng kết). | Đột biến bỏ phép đọc run.json (luôn coi khác) ⇒ ca khai đúng đỏ sai (ĐỎ). |
| A5 (M4) | Fixture có một vi phạm nằm trong danh sách nợ ⇒ `rc=0`; xoá mục nợ ⇒ `rc=1`; vá câu nhưng giữ mục nợ ⇒ `rc=1` (nợ chết). | Đột biến bỏ chốt nợ chết ⇒ ca thứ ba xanh (ĐỎ). |
| A6 (cả packet) | Trên đúng base SHA và trên head packet: `python3 ops/bien_nhan_v2.py --root .` rc=0, `TỔNG: ĐẠT`; `python ops/bien_nhan_v2_test.py` N/N với hai số BẰNG NHAU. | Chạy trên base SHA với danh sách nợ RỖNG phải ra `rc=1` (bằng chứng luật có răng trên dữ liệu thật). Không ra `rc=1` ⇒ luật mù, ĐỎ. |
| A7 (nền, L6) | Trước khi bắt tay: A1–A5 trên base phải ra "chưa làm" (ca chưa tồn tại / luật chưa có). | — (tiêu chí canh nền; răng đến từ A1–A5). |

## `hinh_dang_ke_thua`

Chép từ chuỗi biên nhận `ops/reviews/pr896-review-{2..8}-codex-verdict.receipt.yaml` (đơn vị: **finding** theo dòng `Kết quả` của
verdict; "lớp" = hình dạng lỗi).

| lượt | reviewed_sha | P1/P2 | lớp |
|---|---|---|---|
| 2 | `8d56009` | 1/0 | surface tự khai |
| 3 | `82359c4` | 2/1 | surface tự khai · trạng thái cũ (HINT chưa áp) |
| 4 | `2e4183b` | 3/1 | trạng thái cũ ×2 (chưa review, ancestry) · surface |
| 5 | `1a276a1` | 2/0 | trạng thái cũ ×2 |
| 6 | `22382d8` | 2/0 | ancestry · surface (provenance land) |
| 7 | `05bc12e` | 2/1 | trạng thái cũ ("#490 chưa merge") · mô tả hiện vật sai · surface |
| 8 | `fb87110` | 0/0 | — |

Bộ đếm hình dạng: **trạng thái phụ thuộc thời điểm** lặp ở lượt 3, 4, 5, 6, 7 (5 lần); **surface tự khai** ở lượt 2, 3, 4, 6, 7
(5 lần). Cả hai đã vượt chốt "lặp ba lần" — lý do packet này tồn tại. Nếu packet này lại lặp một hình dạng ≥ 3 lần qua các lượt
review thì DỪNG hỏi chủ kho "có nên làm tiếp không".

## Kích thước dự kiến

250–400 dòng thêm trên 2 tệp (đối chiếu: `8f5b8a2` #551 = 124+/3- trên cùng hai tệp, ba vòng vá sau 267+/153-; đo 06:33Z 27-10).
So ngưỡng theo `docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md` lúc cấp lease; vượt thì khai theo đúng dạng ADR ấy.

## `chua_do_duoc`

- **Số vi phạm thật trên master** chưa đo: con số khớp mẫu thô (06:26Z 27-10, receipt: "chưa review" 14 tệp/16 dòng; ancestry
  36 tệp/55 dòng; `codex_service` 16 tệp/27 dòng) GỒM cả câu đã có mốc văn xuôi và câu chỉ trích; số vi phạm theo M1–M3 chỉ có
  khi luật chạy (M4 ghi nó).
- **Mốc văn xuôi** viết ở #947 ("tai moc ghi so …") KHÔNG được M1–M3 công nhận (Q7) — các câu ấy có thể rơi vào danh sách nợ.
- **Biên nhận không có `run_json` trong kho** (vd 13 receipt pr455/phan-bien/…): L-SURFACE không phân xử được; giữ caveat
  `SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC` hiện có.
- **`ADR-0054` chưa kích hoạt** (đo 06:33Z 27-10: `rg -l 'kích hoạt \`ADR-0054\`' docs/adr/` chỉ ra chính tệp ADR) ⇒ dòng khai
  `luat_push_va_dung_va` hiện **vô hiệu**, packet chịu luật cũ. Với `systemic` luật cũ cũng đòi hết P0/P1/P2, nên ngưỡng dừng
  không đổi.
- Hành vi của regex M2 trên mọi biến thể chữ viết tay KHÔNG chứng minh được đầy đủ (L6 "danh sách cấm"); răng thật của packet
  là phép đo SỰ THẬT (merge-base, `reviewed_sha`, run.json), regex chỉ chọn ứng viên.
