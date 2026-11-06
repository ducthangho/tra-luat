# Đặc tả packet — `THU-HOI-ADMISSION-MERGE-BASE-B` (revision 1)

- `packet_id`: **THU-HOI-ADMISSION-MERGE-BASE-B** · `revision`: **1** · trạng thái: nháp, chờ chủ kho duyệt băm.
- `packet_issue`: **#1266** (sub-issue của Mission #1264). Issue không tự cấp việc (protocol §3.2, §4).
- **Phụ thuộc:** packet `THU-HOI-ADMISSION-MERGE-BASE-A` #1265 (ADR-0066 và dòng §20, đặc tả
  `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-A-r1.md`) đã land. Base của B phải chứa commit land của A; đo bằng
  `git merge-base --is-ancestor <land A> <base B>` ⇒ rc 0, không đo được ⇒ chưa cấp lease.
- `nguon_cap_viec`: như packet A — quyết định chủ kho trong phiên soạn spec 06-11-2026, vòng 1 Q1–Q7 và vòng 2
  Q8–Q13, cả hai *"Theo khuyến nghị"*; căn cứ tài liệu https://claude.ai/artifact/Au5vgKvAZWdqGDHMvkU4cW. Bản ghi
  bền ở thân Mission #1264 (phiên soạn spec đăng theo yêu cầu chủ kho); thẩm quyền ràng buộc là comment duyệt băm
  đặc tả này do chính chủ kho đăng trên #1266.
- `review_class`: **sensitive** — `ops/lease_publish.py` là cổng đọc lease (`ADR-0047`); chạm `.github/workflows/**`
  và `.claude/dev/**` (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease, sau khi A land (đo 08:25Z 06-11-2026: master `08bcb51f`, A chưa land).
- Executor **Claude**; reviewer **Codex** độc lập; `human_audited` trên exact head trước merge (vòng 1 Q6). Điều
  kiện merge theo `ADR-0060`.
- Windows: `required` theo `ADR-0060` M3, vì diff chạm `.github/workflows/**` và `.claude/dev/**` (mục 6).
- `full_mutant_audit`: bắt buộc theo M9/K7, vì diff chạm `ops/**/*.py`, `.claude/dev/**` và `.github/workflows/**`.
- Ngân sách đóng của packet (CI, M9, Windows, lời gọi model): mục 8.

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

```yaml
nang_tran:
  ai_nang: chủ kho ducthangho — vòng 1 Q7 của phiên soạn spec 06-11-2026 ("Theo khuyến nghị"); phải ghi lại trên Issue
  can_cu: >-
    Ước lượng 440–590 dòng thêm (mã bộ kiểm ~90–140, test bộ kiểm ~250–350, validator C1a1a và test ~90), chưa đo;
    so sánh gần nhất PR #620 (+204 dòng, 2 tệp). Receipt v2 và validator chấp nhận v2 là một thay đổi hợp đồng,
    land cùng nhau để không có khoảng nào bên này nói v2 mà bên kia chỉ hiểu v1.
  tran_cu: "≤ 6 tệp / ≤ 450 dòng thêm (ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab)"
  tran_moi: "≤ 6 tệp / ≤ 600 dòng thêm, đo bằng git diff --numstat origin/master...HEAD; vượt thì bỏ bớt ca phụ, không xin nâng thêm"
```

## 0. Vấn đề

Như mục 0 của packet A. Tóm lại: `lenh_kiem_thu_hoi_github` gọi `kho.to_tien(S, H)` và trả 12 khi S không phải tổ
tiên của H. Từ khi A land, `ADR-0066` thay luật ấy bằng cổng vùng bằng nhau ở mọi merge-base; packet này thi hành
nó trong mã.

## 1. write_set

- `ops/lease_publish.py`
- `ops/lease_publish_test.py`
- `.github/workflows/ops-thu-hoi-admission.yml` — chỉ khối chú thích ở đầu tệp; không đổi bước nào.
- `.claude/dev/doc_receipt_thu_hoi.py`
- `.claude/dev/doc_receipt_thu_hoi_test.py`

Điều kiện cấp lease: không lease nào còn hiệu lực giữ một đường dẫn trên (đo như packet A). Đo 06-11-2026 trên kho
có `refs/heads/*` khớp máy chủ: `ops/lease_publish.py`, `ops/lease_publish_test.py` và
`.github/workflows/ops-thu-hoi-admission.yml` ⇒ `NGƯỜI_GIỮ 0`. `.claude/dev/doc_receipt_thu_hoi.py` và
`.claude/dev/doc_receipt_thu_hoi_test.py` ⇒ `CHAN [12]` vì máy chủ thêm nhánh giữa lượt quét (`claude/ghi-so-land-1258`,
`ops/wp1239-r4-g3-lease`; chốt fail-close đúng thiết kế). Người cấp lease đo lại cả năm đường dẫn ngay trước khi cấp (L5).

## 2. ngoai_pham_vi

- Luật theo ID lease (R3/R4) và việc kiểm lại lúc land (R5): thuộc A1b (#656) và bên kiểm lúc land (#499 C1,
  #1179), vòng 1 Q5. Packet này chỉ ghi vào receipt dữ kiện để R5 dùng.
- `SO_THU_HOI_KICH_HOAT` giữ `False`; luật "chế độ chưa kích hoạt đòi tập revocation rỗng ở S và T" giữ nguyên.
- Chuyển tiếp Q13 (marker mới đòi `base_sha_before_add == S`) giữ nguyên. PR thêm tệp policy và marker vẫn cần S
  đúng bằng base của sự kiện; đó là việc của A1, rất hiếm, không phải nguồn sync hằng ngày.
- Các lệnh khác của `ops/lease_publish.py` (`check`, `body`, `kiem-github`, `ai-dang-giu`) và các bước của workflow.
- Vùng so sánh **không** gồm `ops/leases/**` (vòng 2 Q8). A1b phải mở rộng vùng khi bộ kiểm bắt đầu đọc lease.
- Đặc tả đã đóng băng (r9 của `THU-HOI-LEASE-VA-CAP-LAI`, r5 của `LAND-DOC-RECEIPT-THU-HOI-C1a1a`) và đặc tả #1179.
- WP1174 (#1174, bộ duyệt C6 chờ chủ kho, đo 15:0xZ 06-11-2026: chưa cấp lease) sửa `kiem-merge` trong
  `.claude/dev/packet_loop.py`. Packet này không thích nghi trước với thay đổi ấy: nếu WP1174 land trước khi B merge,
  điều kiện merge của B được đánh giá bằng mã canonical tại thời điểm merge.
- Ngoại lệ closure `ADR-0032` kiểu WP1174: không xin. Đo 06-11-2026: 0/179 lease trên master có ngoại lệ closure;
  các lease gần đây bỏ trống hoặc để `null` trường `change_policy_sha`.

## 3. Bảng ba trạng thái — đóng, mọi bước mới phải theo

Bài học của lớp `phan-loai-vang-va-khong-do-duoc` (mục 7): "không thấy" và "không đo được" phải là hai nhánh khác
nhau trong mã, mỗi nhánh có ca test riêng.

| bước | kết quả "có" | kết quả "không" (đo được) | không đo được ⇒ rc 12 |
|---|---|---|---|
| quan hệ S→H | đi parent từ H gặp S ⇒ `to_tien`, ghi số cạnh | duyệt hết tổ tiên của H trong ngân sách mà không gặp S ⇒ sang bước merge-base | vượt ngân sách, thiếu object, object băm không khớp tên, graft hoặc `refs/replace` |
| tập merge-base | ≥ 1 merge-base, tính trọn trong ngân sách | 0 merge-base (lịch sử không chung gốc) ⇒ rc 12 | vượt `max_commits_merge_base`, thiếu object, object hỏng |
| so vùng | mọi merge-base có vùng bằng vùng tại S ⇒ đi tiếp các phép kiểm cũ trên T | một merge-base lệch ⇒ rc 12, thông báo có `VUNG_LECH`, SHA của merge-base, đường dẫn lệch đầu tiên | `tim` gặp tổ tiên không phải thư mục, đọc object lỗi |

Không bước mới nào được trả 0 khi một phép đo của nó không đo được.

## 4. muc_tieu

1. `ops/lease_publish.py` — hàm ba trạng thái cho quan hệ S→H (trả số cạnh, hoặc "không phải tổ tiên", hoặc ném
   rc 12 khi không đo được) dùng chung bộ đọc có băm của `KhoObject`. `KhoObject.to_tien` giữ nguyên hành vi bên
   ngoài (ném 12 khi không phải tổ tiên) cho mọi chỗ gọi hiện có.
2. `ops/lease_publish.py` — tính **mọi** merge-base của (S, H) bằng bộ đọc có băm: giao tập tổ tiên của hai phía,
   lấy các phần tử cực đại. Khoá ngân sách mới `max_commits_merge_base` = **50.000** commit đã đọc cho một lần tính
   (cả hai phía) trong `NGAN_SACH_MAC_DINH`. Căn cứ: #1179 đo toàn lịch sử master **5.444** commit, 8.480.418 byte,
   0,34 giây (07:23Z 06-11-2026), tức trần dư khoảng 9 lần. Không gọi `git merge-base` hay Git plumbing nào khác.
3. `ops/lease_publish.py` — hàm vùng của một commit: bản đồ `ops/thu-hoi/**` qua `KhoObject.namespace`, cộng mục
   `PATH_POLICY_CLOSURE` qua `KhoObject.tim` (vắng ⇒ không có khoá; tổ tiên không phải thư mục ⇒ 12, như hành vi
   hiện có). So từng merge-base với S theo bảng mục 3.
4. `ops/lease_publish.py` — `lenh_kiem_thu_hoi_github` dùng mục tiêu 1–3 thay cho `kho.to_tien(S, H)`; mọi phép
   kiểm còn lại (append-only S→T, validator namespace T, Q13, chế độ chưa kích hoạt) giữ nguyên thứ tự và mã thoát.
   Receipt lên `schema_version` **2** với ba khoá mới:
   - `quan_he_S_H`: `"to_tien"` hoặc `"merge_base"`;
   - `merge_bases`: danh sách SHA40 không trùng, sắp tăng; chế độ `to_tien` ⇒ đúng `[S]`;
   - `vung_tai_S`: bản đồ vùng đã so, khoá là đường dẫn, giá trị `[mode, kiểu, OID]`.

   `canh_ancestry`: số nguyên ở chế độ `to_tien`, `null` ở chế độ `merge_base`. Dòng in `THU_HOI_ADMISSION …` thêm
   `quan_he=<giá trị>`.
5. `ops/lease_publish_test.py` — sửa ca con của t133 đang khẳng định *"S không tổ tiên H phải 12"* (đo 06-11: dòng
   6580 trên `08bcb51f`): ca ấy thành "S không tổ tiên H, vùng bằng nhau ⇒ rc 0, `merge_base`", và thêm một ca
   vùng lệch ⇒ 12. Thêm các ca B1–B9 ở mục 5, mỗi đột biến đăng ký vào bảng đột biến sẵn có của tệp (cùng khuôn với
   mục `C1-tim-to-tien-non-tree-la-vang`). Cập nhật phép kiểm tĩnh của workflow (t137) cho B10.
6. `.github/workflows/ops-thu-hoi-admission.yml` — thay câu chú thích *"Bộ kiểm còn đòi S là tổ tiên của H — đó là
   thiết kế fail-close giữ nguyên theo quyết định chủ kho cho #618 (đường (a)), không phải dương tính giả."* bằng
   câu nói luật mới, có chữ `ADR-0066`. Không đổi dòng nào ngoài khối chú thích.
7. `.claude/dev/doc_receipt_thu_hoi.py` — nhận receipt v1 (đúng 38 khoá như hiện nay) **và** v2 (đúng 41 khoá),
   mỗi phiên bản là một tập khoá đóng riêng. Luật riêng của v2: `quan_he_S_H` thuộc hai giá trị trên; `merge_bases`
   là danh sách SHA40 không rỗng, không trùng, sắp tăng; `to_tien` ⇒ `merge_bases == [S]` và `canh_ancestry` là số
   nguyên ≥ 0; `merge_base` ⇒ `canh_ancestry` là `null` và S không nằm trong `merge_bases`; `vung_tai_S` là dict
   khoá chuỗi, giá trị danh sách 3 phần tử. Module giữ thuần JSON: không git, không mạng.
8. `.claude/dev/doc_receipt_thu_hoi_test.py` — các ca B11 ở mục 5.

## 5. nghiem_thu

Mọi ca "đỏ" kèm một đột biến làm ca đổi màu (L3). Fixture dựng đồ thị Git thật trong thư mục tạm, như t133.

| # | ca | kỳ vọng | đột biến phải làm ca đổi màu |
|---|---|---|---|
| B1 | S là tổ tiên H | rc 0; receipt v2, `quan_he_S_H = to_tien`, `merge_bases = [S]`, `canh_ancestry` số nguyên | luôn đi nhánh merge-base ⇒ `quan_he_S_H` khác ⇒ ca đỏ |
| B2 | H rẽ từ B, master đi tiếp và đổi tệp ngoài vùng | rc 0; `merge_base`, `merge_bases = [B]`, `canh_ancestry = null` | bắt lại `to_tien` ⇒ rc 12 ⇒ ca đỏ |
| B3 | Master thêm `.github/coordination/change-impact.v1.json` sau B | rc 12, thông báo có `VUNG_LECH` | bỏ cổng so vùng ⇒ rc 0 ⇒ ca đỏ |
| B3b | Master thêm một bản ghi thu hồi sau B | rc 12 | **không có đột biến đơn lẻ nào lật được**: khi cờ tắt, luật "sổ phải rỗng" cũng trả 12. Ghi thẳng như vậy; răng của cổng nằm ở B3 |
| B4 | B và S có cùng một bản ghi; H xoá (hoặc sửa) bản ghi ấy; S không là tổ tiên H | rc 8 (append-only) | bỏ phép append-only ⇒ rc đổi (sang 12 vì sổ không rỗng) ⇒ ca đỏ |
| B5 | Criss-cross: hai merge-base, merge-base đứng đầu theo thứ tự sắp có vùng bằng S, cái còn lại lệch | rc 12, `VUNG_LECH` | chỉ so merge-base đầu ⇒ rc 0 ⇒ ca đỏ |
| B6 | S và H không chung gốc | rc 12 | coi "0 merge-base" là đạt ⇒ rc 0 ⇒ ca đỏ |
| B7 | Ngân sách `max_commits_merge_base` nhỏ hơn số commit phải đọc (truyền qua tham số `ngan_sach` nội bộ) | rc 12, không phải 0 | nuốt lỗi vượt ngân sách ⇒ rc 0 ⇒ ca đỏ |
| B8 | Đường duyệt đi qua object có nội dung không băm ra đúng tên, hoặc có `refs/replace` | rc 12 | tính merge-base bằng `git merge-base --all` thay bộ đọc có băm ⇒ rc 0 ⇒ ca đỏ |
| B9 | Vượt ngân sách **trong lúc** xét S→H (trước bước merge-base) | rc 12 | xếp "vượt ngân sách" vào nhánh "không phải tổ tiên" ⇒ đi tiếp merge-base ⇒ rc 0 ⇒ ca đỏ |
| B10 | Chú thích workflow, đo trên văn bản đã nối dòng từng đoạn (L6 b): có nguyên câu mới nhắc `ADR-0066` (vế dương); không còn câu cũ ở mục tiêu 6 (vế âm) | cả hai vế đạt | ghi lại câu cũ ⇒ vế âm đỏ; xoá câu mới ⇒ vế dương đỏ; ngắt dòng lại giữ nguyên chữ ⇒ vẫn đạt |
| B11 | `doc_receipt_thu_hoi`: v1 hiện có ⇒ `ok`; v2 `to_tien` ⇒ `ok`; v2 `merge_base` ⇒ `ok`; v2 thiếu `merge_bases`, thừa một khoá, `to_tien` với `merge_bases ≠ [S]`, `merge_base` với `canh_ancestry` số, `schema_version = 3` ⇒ mỗi ca `do` | như cột trái | bỏ kiểm tập khoá v2 ⇒ ca thiếu/thừa khoá thành `ok` ⇒ ca đỏ |
| B12 | `doc_receipt_thu_hoi.py` giữ thuần JSON: đếm nguyên từ `subprocess`, `socket`, `urllib` trong tệp ⇒ 0 mỗi từ (đếm từng từ, không gộp — L6 c) | mỗi từ 0 | thêm `import subprocess` ⇒ đỏ |
| B13 | Toàn bộ `ops/lease_publish_test.py` và `.claude/dev/doc_receipt_thu_hoi_test.py` trên CI Linux của exact head báo `N/N` với hai số bằng nhau | lệch | — (bằng chứng dương, không tin `rc=0` một mình) |
| B14 | Windows, mục 6 | xanh theo `ADR-0060` M3 (a)–(c) | — |
| B15 | `ci-dot-bien-du.yml` thành công trên exact head, mọi job `success` (K7) | thiếu hoặc đỏ | — |
| B16 | Kích thước theo `nang_tran`: ≤ 6 tệp, ≤ 600 dòng thêm; không tệp ngoài `write_set` | vượt hoặc tệp lạ | thêm một tệp ⇒ đỏ |
| B17 | Hiệu năng trên kho thật: chạy bộ kiểm với S = tip master và H = head của một PR thật đang tụt sau master | rc 0, `merge_base`, ghi thời gian, `so_object_da_doc`, `tong_bytes`, không chạm trần | rc 12 vì ngân sách ⇒ đỏ |
| B18 | Canary sau land: PR thật đầu tiên có head không chứa tip master | check `thu-hoi` success; receipt đọc lại có `quan_he_S_H = merge_base` | **chưa đo được** tới khi có PR ấy; người land ghi run ID và receipt đã đọc lại |

Chạy thử trên nền (worktree tách ở `origin/master` `08bcb51f`, 08:3xZ 06-11-2026):

- B10: trên văn bản chú thích đã nối dòng từng đoạn, câu cũ ở mục tiêu 6 có mặt **1** lần, `ADR-0066` **0** lần —
  cả hai vế đỏ, đúng màu "chưa làm".
- B12: đếm nguyên từ trong `.claude/dev/doc_receipt_thu_hoi.py`: `subprocess` 0, `socket` 0, `urllib` 0 — bất
  biến, xanh sẵn; răng nằm ở đột biến.
- B1–B9, B11: các ca chưa tồn tại trên nền; ca t133 hiện có khẳng định *"S không tổ tiên H phải 12"*, tức màu của
  B2 trên nền là 12 (đọc từ mã, chưa chạy). Phải chạy B2, B5, B6 trên mã nền ngay sau khi viết fixture để xác nhận
  chúng đỏ đúng chỗ, trước khi sửa bộ kiểm.
- B13: chưa chạy toàn bộ suite trên nền ở phiên này; số ca nền lấy từ CI của base khi cấp lease.

### 5.1 Kho ID đóng băng

Danh tính của một ca là **hậu tố tên** dưới đây, không phải số thứ tự. Trong `ops/lease_publish_test.py` mọi ca tên
`t<số>_…` và đăng ký qua `CA.append` (đo 06-11-2026 trên `origin/master`: 280 ca, số lớn nhất `t237`). Executor chọn
số kế tiếp còn trống trên base của lease, giữ nguyên hậu tố. Mỗi hậu tố phải khớp **đúng một** hàm; không khớp hoặc
khớp hai ⇒ runner đỏ. Mỗi đột biến có ID riêng, đăng ký vào bảng đột biến sẵn có của tệp test tương ứng; tệp nào
chưa có bảng thì executor chạy đột biến bằng tay trên bản sao tạm và ghi ID, lệnh, kết quả vào handoff.

| ca | tệp | hậu tố / tên ca | ID đột biến | nền |
|---|---|---|---|---|
| B1 | `ops/lease_publish_test.py` | `_amb01_to_tien_giu_nguyen` | `amb-m01-luon-di-merge-base` | cả hai |
| B2 | `ops/lease_publish_test.py` | `_amb02_merge_base_vung_bang_nhau` | `amb-m02-bat-lai-to-tien` | cả hai |
| B3 | `ops/lease_publish_test.py` | `_amb03_policy_lech_sau_merge_base` | `amb-m03-bo-cong-so-vung` | cả hai |
| B3b | `ops/lease_publish_test.py` | `_amb03b_thu_hoi_moi_tren_master` | — (mục 5, hàng B3b) | cả hai |
| B4 | `ops/lease_publish_test.py` | `_amb04_append_only_qua_merge_base` | `amb-m04-bo-append-only` | cả hai |
| B5 | `ops/lease_publish_test.py` | `_amb05_criss_cross_mot_base_lech` | `amb-m05-chi-so-base-dau` | cả hai |
| B6 | `ops/lease_publish_test.py` | `_amb06_khong_chung_goc` | `amb-m06-rong-la-dat` | cả hai |
| B7 | `ops/lease_publish_test.py` | `_amb07_vuot_ngan_sach_merge_base` | `amb-m07-nuot-vuot-ngan-sach` | cả hai |
| B8 | `ops/lease_publish_test.py` | `_amb08_object_gia_tren_duong_duyet` | `amb-m08-git-merge-base-thay-bo-doc` | cả hai |
| B9 | `ops/lease_publish_test.py` | `_amb09_vuot_ngan_sach_khi_xet_to_tien` | `amb-m09-vuot-ngan-sach-thanh-khong-to-tien` | cả hai |
| B10 | `ops/lease_publish_test.py` | `_amb10_chu_thich_workflow_adr0066` | `amb-m10-ghi-lai-cau-cu` | cả hai |
| t133 | `ops/lease_publish_test.py` | tên hiện có, ca con "S không tổ tiên H" đổi kỳ vọng (mục tiêu 5) | `amb-m02-bat-lai-to-tien` | cả hai |
| B11 | `.claude/dev/doc_receipt_thu_hoi_test.py` | ca bảng `v2_to_tien`, `v2_merge_base`, `v2_thieu_merge_bases`, `v2_thua_khoa`, `v2_to_tien_base_khac_S`, `v2_merge_base_canh_so`, `schema_3`; ca v1 hiện có giữ nguyên | `amb-m11-bo-tap-khoa-v2` | cả hai |
| B12 | `.claude/dev/doc_receipt_thu_hoi_test.py` | ca `thuan_json_khong_subprocess_socket_urllib` | `amb-m12-them-subprocess` | cả hai |

Cột "nền" là ý định; nền thật của từng ca do bước đo nền ở mục 6 quyết. Ca đã ghi "cả hai" mà không chạy được trên
Windows native phải khai lý do trên #1266 trước lượt ứng viên (mục 6 bước 2), không lặng lẽ bỏ.

## 6. Windows (vòng 2 Q12)

Máy: `tra-luat-win`, Desktop Commander device `f7281f27-f79f-40a2-a2f5-b454b58a166a`, tài khoản `tlcommander`.
Không dùng device khác của cùng VM chạy dưới tài khoản quản trị để lấy quyền cao hơn. Clone thường, có thư mục `.git`
riêng; H chưa lên GitHub thì đưa sang bằng git bundle và kiểm commit, tree, cha khớp từng hash (`ADR-0060` M4).
Output, cache, thư mục tạm đặt ngoài checkout. Giữ `KHOA.txt` theo `ADR-0057`–`0059`; không đụng tiến trình hay khoá
của packet khác.

1. **Đo nền**, trước khi sửa mã: chạy trên base tập ứng viên gồm toàn bộ `.claude/dev/doc_receipt_thu_hoi_test.py`,
   cùng các ca t133, t151, t137 của `ops/lease_publish_test.py`. Ghi ca nào chạy native được.
2. **Đóng băng tập bắt buộc** và đăng lên #1266 **trước** lượt ứng viên. Tập ấy gồm:
   - **luôn có**: toàn bộ `doc_receipt_thu_hoi_test.py` (gồm B11, B12) và `_amb10_chu_thich_workflow_adr0066`;
   - **có điều kiện**: t133 và các ca `_amb01`…`_amb09` — vào tập bắt buộc nếu t133 chạy native được ở bước 1;
     nếu không, mỗi ca loại ra phải kèm lý do (protocol ghi bộ giải Git của admission dùng PATH `/usr/bin:/bin`,
     chưa hỗ trợ Windows native).

   Sau khi đã đăng, tập bắt buộc chỉ được **thêm** ca, không được bớt.
3. **Runner tập trung** nằm ngoài checkout (không thuộc write set). Nó gọi `main(chon=[...])` của
   `ops/lease_publish_test.py` với các hàm tìm theo hậu tố ở mục 5.1, và `chay_ca(..., chi=...)` (hoặc toàn tệp)
   của `doc_receipt_thu_hoi_test.py`. Không gọi `main()` không đối số, vì nó chạy cả 280 ca cũ. Runner phải:
   - kiểm `git rev-parse HEAD` bằng H và `git status --porcelain` rỗng, trước và sau lượt chạy;
   - kiểm nền thật (`platform.system()`), phiên bản Python và Git;
   - đỏ khi một ID không khớp đúng một hàm; coi `BỎ QUA`, skip, timeout, lỗi hạ tầng là **không đạt**;
   - ghi JSON gồm H, tree, nền, danh sách ID, kết quả từng ID, rc, kèm sha256 của tệp JSON.

   Cùng runner ấy chạy trên Linux trước full gate, để có kết quả tập trung nhanh.
4. Lượt nền và lượt ứng viên dựng trong **cùng một lệnh**, cùng máy, có danh sách ID ca và kết quả (M3 a). Ca bắt
   buộc bị `skipped`/`not_run` ⇒ không xanh.
5. Tiến trình test không được thấy credential LIVE: `TL_TOKEN`, `TL_WEBAPP`, `TL_MASTER_KEY`,
   `TL_AGENT_CREDS_FILEID` và các biến Drive/GAS/NLM khác phải vắng. Runner kiểm sự vắng mặt bằng giá trị đúng/sai,
   không in giá trị.

## 7. hinh_dang_ke_thua

Chép từ đặc tả #1179 r1 §7 (nhánh `claude/spec-1179-c1a1b`, commit `7cfb4d7`) và quyết định chủ kho ở #1179 lúc
07:58Z 06-11-2026:

| lớp | số đếm | nguồn | chốt ở packet này |
|---|---|---|---|
| `phan-loai-vang-va-khong-do-duoc` | **4** (đã chạm chốt dừng ở #1179) | #1179 r1 lượt 1 F4 | bảng đóng ở mục 3; ca B6, B7, B9 |
| `mo-rong-module-pha-hop-dong-json-thuan` | 3 | #1179 review draft0–2 | mục tiêu 7 giữ thuần JSON; ca B12 |
| `nguon-duoc-tin-ma-chua-xac-minh` | 7 (chuỗi thu hồi) | spec C1a1a r5 §6 | merge-base chỉ tính bằng bộ đọc có băm; ca B8 |

Một biểu hiện mới của **bất kỳ** lớp nào trên ở bất kỳ lượt review nào (đặc tả hay PR thi công) ⇒ DỪNG, Review
Rescue Checkpoint (`ADR-0037`), báo chủ kho; không vá tiếp theo chỗ bị chỉ.

## 8. Review và ngân sách đóng

**Review đặc tả, trước khi chủ kho duyệt băm:** một lượt review độc lập của chính đặc tả này (Codex, ≤ 2 lời gọi,
tính trên PR đưa đặc tả vào kho). Finding P0–P2 ⇒ sửa đặc tả và tính băm mới trước khi duyệt.

**Review mã:** reviewer Codex độc lập, phiên riêng; trần 10 lời gọi theo dòng khai `ADR-0055` ở đầu tệp, đếm
**trước** mỗi lời gọi. Ngân sách mềm 4 lời gọi; hai lượt liên tiếp chưa approve ⇒ Review Rescue Checkpoint.
Reviewer **chạy** các ca và **đột biến bản vá** để đo răng; hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời
cho phiên điều phối viết. Human audit theo `human_exact_head_audit.v1` (`ADR-0063`) trên exact head trước merge.

**Ngân sách đóng của PR mã** (đề xuất trong đặc tả; chủ kho chốt khi duyệt băm):

| hạng mục | trần | ghi chú |
|---|---|---|
| Lượt CI Ubuntu trên PR (head hoặc attempt) | 2 | rerun cũng tính; khớp `ADR-0060` M5 (một lần push chính) |
| Lượt `ci-dot-bien-du.yml` đầy đủ | 1 | lượt thứ 2 chỉ khi head đổi sau rework, cần checkpoint chủ kho |
| Lượt Windows native tập trung | 2 | mỗi lượt gồm nền và ứng viên trong một lệnh; tổng ≤ 60 phút |
| Phiên executor | 2 | checkpoint chủ kho nếu một phiên chạy quá 120 phút chủ động mà chưa có H |
| Lời gọi Codex review mã | 10 | mềm 4, như trên |

Không trong packet này: gắn nhãn `windows` lên PR; gọi tay `ci.yml` (cả hai `runner_set` đều có Windows); Windows
CI; full mutant trên Windows; mua credits. Hết một trần, hoặc không biết mức đã dùng ⇒ dừng ở checkpoint chủ kho;
không vay ngân sách của packet khác.

## 9. chua_do_duoc

- Kết quả `ai-dang-giu` cho `.claude/dev/doc_receipt_thu_hoi.py` và `.claude/dev/doc_receipt_thu_hoi_test.py`: cả hai
  bị chốt fail-close chặn vì máy chủ thêm nhánh giữa lượt quét.
- Ca nào của t133/t151/t137 chạy được trên Windows native: chưa đo (mục 6 bước 1).
- Runner tập trung (mục 6 bước 3): chưa dựng, chưa chạy lần nào.
- Các trần ở mục 8 là đề xuất; chưa có số đo mức dùng thực của một packet cỡ này để biện hộ từng con số.
- Hiệu năng thật của phép tính merge-base trên kho này (B17): mới có số đo duyệt toàn lịch sử master của #1179,
  chưa đo phép giao hai phía.
- Canary B18: chỉ đo được sau land.
- Số dòng thực tế: mới là ước lượng (khối `nang_tran`).
