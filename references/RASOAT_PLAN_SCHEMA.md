# RASOAT_PLAN_SCHEMA — `rasoat_plan.v1` (phần BIẾN ĐỘNG của lớp điều phối rà soát hồ sơ)

> Phần TĨNH (vòng lặp, cổng, điều kiện dừng) đã đóng ở thẻ `references/workflows/rasoat_hoso.json`
> (`workflow_card.v1` — được `workflow-audit` kiểm tự động). Tài liệu này đặc tả DUY NHẤT phần biến động:
> file state của TỪNG hồ sơ. Nguồn thiết kế: docs nhánh kiến trúc (KE_HOACH_RASOAT_HOSO_ORCHESTRATION +
> WORKFLOW_RASOAT_TU_DONG, chốt grill 25→26-07). MẪU bảng master đi kèm:
> `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` (bên đọc: `scripts/rasoat_phuluc.py`).

## 1. Nơi lưu (CHỐT LAI — doctrine B.5)

| Thứ | Nơi | Lý do |
|---|---|---|
| `_meta/rasoat_state.json` (file này) | **Drive, trong `_meta/` của profile hồ sơ** | nguồn sự thật resume; sống qua kill/sandbox chat; RMW GAS 2.21.2p nguyên tử |
| `master/<unit>.json`, Q-APPROVALS, Q-BUGS | local `--out-dir` NGOÀI cây skill; đẩy Drive theo lô ở checkpoint (Claude chat: mỗi đơn vị) | sổ nặng, ghi 1 lần khi done |
| MẪU bất biến | trong cây skill (`templates/`, vào zip) | chỉ MẪU rỗng mới được nằm trong cây — state biến động lọt cây = `package_hash` lệch, gate ĐỎ |

## 2. Cấu trúc `rasoat_state.json` (`schema: "rasoat_plan.v1"`)

```json
{
  "schema": "rasoat_plan.v1",
  "ho_so_id": "luat-x-2026",
  "session_claim": {"id": "phien-2026-07-26-a", "ts": "2026-07-26T09:00:00", "progress_ptr": "unit-007"},
  "quota": {"nlm_con_lai": 60, "tvpl_hom_nay": 0},
  "dot": [
    {"dot_id": "dot-01", "ten": "Đợt 1 — chế định A", "trang_thai": "da_dong",
     "mo_luc": "2026-08-20", "dong_luc": "2026-08-24", "gioi_han_da_biet": []}
  ],
  "q_units": [
    {"unit_id": "unit-001", "van_ban": "18-2025-VBHN-VPQH", "dieu": ["54"], "tang": "SAU",
     "trang_thai": "done", "loai": "ra_soat", "dot_id": "dot-01"},
    {"unit_id": "unit-009", "van_ban": "18-2025-VBHN-VPQH", "dieu": ["125"], "tang": "DOI_CHIEU",
     "trang_thai": "pending", "loai": "doi_chieu_bo_sung", "doi_chieu_voi": "145-2026-ND-CP",
     "dot_id": "dot-02", "cong_anh_huong": "dan_chieu"}
  ],
  "q_ingest": [
    {"so_hieu": "145-2026-ND-CP", "trang_thai": "staged", "plan_hash": "…", "nguon": "vbpl.vn",
     "dot_id": "dot-02", "nhom_chinh_sach": false}
  ],
  "q_nlm": [
    {"so_hieu": "145-2026-ND-CP", "trang_thai": "pending"}
  ],
  "q_verify": [
    {"unit_id": "unit-004", "key_phat_hien": "VD-03", "ly_do": "cho_verify_nlm"}
  ],
  "dry_rounds_lien_tiep": 0,
  "note_ban_giao": "đang dở gì · việc kế tiếp · bẫy đang mở",
  "cap_nhat": "2026-07-26T09:41:00"
}
```

## 3. Từ vựng đóng (enum)

- `trang_thai` đơn vị: `pending | doing | done | blocked | stale` — **bất biến: `done` không bao giờ về
  `pending` toàn phần trừ khi anchor vỡ** (văn bản nền đổi `text_hash`).
- `loai` đơn vị: `ra_soat | doi_chieu_bo_sung` (cặp đơn-vị-done × văn-bản-mới, chỉ so phần giao).
- `muc_chac_chan` phát hiện (ghi trong master, không ở đây): `chac_chan | can_kiem_tra | cho_verify_nlm`.
- `q_ingest.trang_thai`: `cho_tai | cho_nguoi_tai | dry_planned | staged | flipped | out_of_scope |
  da_quyet | da_quyet_va_thi_hanh` — hai giá trị cuối cho mục người thẩm tra đã quyết (giữ/không thay,
  hoặc đã thi hành); lời quyết nguyên văn để ở `ghi_chu`, **không nhét vào `trang_thai`**.
- `q_nlm.trang_thai`: `pending | added | failed`.
- `q_verify.trang_thai`: `cho_tra_no | dat | khong_dat | no_treo`. (`no_treo` = nợ được **khai là giới hạn**
  khi đóng hồ sơ, không phải nợ đang chờ xử.) Trước r300 hàng đợi này **không có enum nào được khai** —
  hồ sơ thật đã tự dùng khoá `ly_do` với từ vựng riêng; giữ `ly_do` làm ghi chú, `trang_thai` là trường máy đọc.
- `q_approvals.trang_thai`: `cho_duyet | da_duyet_va_da_chay | da_quyet`.
- `vong_doi.trang_thai` (mục 7): `dang_ra | tam_ngung | da_dong | da_dong_co_gioi_han`.
- `dot.trang_thai` (mục 8): `chua_mo | dang_ra | da_dong | da_dong_co_gioi_han` — cùng từ vựng `vong_doi`
  một tầng dưới (Đợt ⊂ hồ sơ), để điều kiện đóng dùng chung một khuôn kiểm.
- `q_units[].cong_anh_huong` (chỉ đơn vị `loai="doi_chieu_bo_sung"`): `dan_chieu | chong_cheo |
  tac_dong_chinh_sach` — GHI cổng nào đã sinh đơn vị này (`references/RASOAT_HOSO_LOOP.md` §3bis). Thiếu
  trường ⇒ không truy nguyên được vì sao một đơn vị `done` bị mở lại.

> **Luật chung cho MỌI hàng đợi:** `trang_thai` chỉ nhận token trong enum. Diễn giải đi kèm ⇒ `ghi_chu`;
> giá trị cũ trước khi chuẩn hoá ⇒ `trang_thai_goc`. Đo 01-08 trên hồ sơ `h7-3nd-bhxh-2025`: 7 mục đã trôi
> thành **câu văn xuôi** (`"DA_QUYET_VA_DA_THI_HANH: lua chon (b) — nap lai CHI VAO CACHE"`) ⇒ máy không tự
> kiểm được điều kiện đóng. Enum không cưỡng chế thì sổ sẽ tự chế thêm từ vựng.

## 4. Hằng số vận hành (chốt 26-07 — kickoff từng hồ sơ override được)

| Hằng | Giá trị | Ý nghĩa |
|---|---|---|
| stale-claim takeover `X` | **30 phút** | claim quá hạn + `progress_ptr` không nhích → phiên mới ghi claim đè (RMW); còn nhích → phiên sau LÙI |
| `max_units_per_session` (chat) | **6** | ngưỡng ĐẾM thay ngưỡng % context; hồ sơ toàn đơn vị SÂU → 4 |
| ngưỡng context (local) | **40% mềm / 60% cứng** | đo tại RANH GIỚI đơn vị; chạm auto-compact ~95% = SỰ CỐ quy trình |
| `dry_rounds` K | **2** | hội tụ — khớp `tl rasoat-loop` |
| ngân sách NLM / hồ sơ | **60 call** | trừ dần trong `quota.nlm_con_lai` |
| `quota_tvpl` / ngày | **100** | SỔ ĐẾM + phản ứng (tụt bậc khi TVPL báo hết thật, không chặn sớm) |
| `ttl_ngay` anchor | **90** | chỉ áp mức `can_kiem_tra`; `cho_verify_nlm` do Q-VERIFY xử lý |

## 5. Nghi thức đóng gói (A8) — thứ tự cố định

1. Rà XONG HẲN đơn vị đang cầm, hoặc trả về `pending` — không giả `done`.
2. Đẩy `master/` + Q-APPROVALS/Q-BUGS lên Drive theo luật môi trường.
3. Cập nhật state lần cuối: hàng đợi + quota + `note_ban_giao` → **NHẢ `session_claim`**.
4. Kết sổ registry nếu phiên có ghi: `tl manifest` (+ `ops-plan` đổ việc vệ sinh vào Q-APPROVALS chờ duyệt).

Phiên kế nhiệm: Pha 0 → đọc state từ Drive → ghi claim MỚI → rà tiếp. Kill-ngang = bàn giao không nghi thức:
state cập nhật sau MỖI đơn vị nên mất tối đa 1 đơn vị dở.

## 6. Sinh worksheet/đơn vị & tổng hợp

- Phân tầng đơn vị: `scripts/rasoat_worksheet.py` (chấm SÂU/ĐỐI CHIẾU/—; sinh `NHAT_KY_NLM_<sh>.csv`).
- Tổng hợp cuối: `scripts/rasoat_phuluc.py --in master/` (Pha 4 — hàm thuần từ thư mục master, chạy lại
  bao nhiêu lần cũng được). Quy trình nền: `references/QUY_TRINH_RA_SOAT_3_TANG.md`.

## 7. Vòng đời HỒ SƠ (r300) — đóng, và mở hồ sơ kế tiếp

`rasoat_plan.v1` vốn có trạng thái cho **đơn vị rà**, **không có** cho **hồ sơ**. Hệ quả đo được trên
`h7-3nd-bhxh-2025`: người thẩm tra chốt "đã đóng" mà **không có gì trong file nói nó đóng**, trong khi còn
5 đầu mối treo (claim chưa nhả · 1 duyệt `cho_duyet` · 3 nợ kiểm chéo · 5 văn bản chưa lấy được · 7 trạng
thái văn xuôi). Khối `vong_doi` biến "đóng" thành trạng thái máy đọc được, và buộc mọi đầu mối phải được
**định đoạt tường minh** — xử, hoặc khai là giới hạn.

```json
"vong_doi": {
  "trang_thai": "da_dong_co_gioi_han",
  "mo_luc": "…", "dong_luc": "…", "dong_boi": "…",
  "san_pham_cuoi": ["BAO_CAO_RA_SOAT.md", "BANG_MASTER.json", "phuluc/"],
  "gioi_han_da_biet": [{"loai": "…", "so_luong": 0, "chi_tiet": []}],
  "dinh_doat": {"q_units": "…", "q_ingest": "…", "q_nlm": "…", "q_verify": "…", "q_approvals": "…"},
  "anchor_con_hieu_luc": false, "ly_do_anchor": "…",
  "skill_version_luc_dong": "…"
}
```

### 7.1 Điều kiện đóng — 6 vế

Đủ **cả 6** ⇒ `da_dong`. Thiếu vế nào mà vẫn đóng ⇒ **`da_dong_co_gioi_han`** kèm mục tương ứng trong
`gioi_han_da_biet` (bắt buộc; không có mục = không được đóng).

1. `q_units`: 0 mục `pending`/`doing` (`blocked` ⇒ khai giới hạn).
2. `q_approvals`: 0 mục `cho_duyet`; mỗi mục còn lại có kết cục tường minh.
3. `q_verify`: mọi mục có `trang_thai` thuộc enum; còn `cho_tra_no` ⇒ chuyển `no_treo` **và** khai giới hạn.
4. `q_ingest`: mọi mục thuộc enum; `cho_tai`/`cho_nguoi_tai` còn lại ⇒ khai giới hạn.
5. `session_claim` **đã nhả** (`id: null` + `released_at`).
6. Sản phẩm cuối gộp/kết xuất được: `tl rasoat-merge --check` rc=0 · `rasoat_phuluc.py --in <master/>` rc=0.

> **Bất biến:** đóng hồ sơ là **ĐÓNG BĂNG, không phải dọn** — KHÔNG xoá `master/`, `rasoat_bugs.md`,
> `rasoat_approvals.json`, các `BIEN_BAN_*`.

### 7.2 Sau khi đóng — Loop C được phép gì

Hồ sơ đóng KHÔNG làm phát hiện hết giá trị (luật có thể sửa sau khi trình ⇒ `resolved_by_amendment`).
Nhưng Loop C **chỉ được chạy khi `anchor_con_hieu_luc: true`**; `false` ⇒ **BỎ QUA hồ sơ và NÓI RA lý do**
(`ly_do_anchor`), không im lặng thoát.

Đo 01-08: `anchor.text_hash` của hồ sơ BHXH là **địa chỉ định vị, không phải hash** — 40 phát hiện ·
82 `doc_deps` · **82/82 điền · 0/82 khớp `sha256:<64hex>`**; registry/manifest không có trường `text_hash`.
⇒ chạy Loop C theo đặc tả hiện hành sẽ ra **STALE giả 100%**. Chỉ bật `true` sau khi anchor được di trú
(tách `locator` khỏi `text_hash`, tính lại bằng `doc_identity._content_hash`).

**Đo lại 02-08 (r321) — phân rã 82 ô, vì "di trú" KHÔNG phải một việc đồng nhất:**

| lớp | n | tự động di trú được? |
|---|---|---|
| `cache:<slug>` (± `#<8hex>`) | 47 | **ĐƯỢC** — `~/.tra_luat_cache/docs/<slug>.json` giữ `text_hash` 64hex thật; hai ô có `#<8hex>` đều KHỚP tiền tố bản cache hiện hành |
| hex 16 ký tự (2 giá trị, `158-2025-ND-CP` + `41-2024-QH15`) | 17 | **KHÔNG** — dò cả `~/.tra_luat_cache/docs` lẫn mọi `cache_bak_*`: khớp **0** bản, kể cả bản lưu ⇒ không truy nguyên được |
| `congbao:<số>#pdf`/`#meta` | 17 | **KHÔNG** — không có record cache; phải lấy lại từ Công báo |
| `gdoc:<id>` | 1 | **KHÔNG** — phải lấy lại từ Drive |

⚠ Vì 17 ô **không truy nguyên được**, câu "tính lại bằng `_content_hash`" ở trên chỉ đúng cho lớp
`cache:`. Áp cho cả 82 là SAI: nó thay một giá trị không rõ nguồn bằng một giá trị TƯƠI, tức khẳng
định một độ tươi **chưa hề kiểm** — đúng thứ mà `anchor_con_hieu_luc` sinh ra để chặn. Ô nào không
truy nguyên được thì **để trống** và giữ `anchor_con_hieu_luc:false` + `ly_do_anchor`.
(Ghi chú: bản đo 01-08 nói "cache `docs/*.json` = 0 record" là đo trong **container rỗng**; trên máy
giữ hồ sơ, `~/.tra_luat_cache/docs/` có đủ 11 bản consolidated.)

Cưỡng chế phía `rasoat-merge` (r321): `tl rasoat-merge` khai `so_anchor_hong` + `anchor_hong`
(đích danh `nguon`/`key`/`so_hieu`) ở **MỌI** chế độ, kể cả `--check`; `--anchor-strict` ⇒ rc=2 và
**KHÔNG ghi** bảng master (cùng khuôn fail-closed r216/r290). KHÔNG bật mặc định — hồ sơ cũ giữ
82/82 ô sai khuôn, chặn đứng chúng vì một lỗi lượt rà không gây ra là đổi một báo cáo sai lấy một
công cụ không dùng được.

### 7.3 Điều kiện mở hồ sơ kế tiếp

1. Hồ sơ trước ở trạng thái terminal (`da_dong` / `da_dong_co_gioi_han` / `tam_ngung` có lý do).
2. **`--out-dir` MỚI** — `rasoat_phuluc.py --in` gộp CẢ THƯ MỤC; trộn hai hồ sơ = bảng master phồng
   (tiền lệ r216: bản sao lẫn trong `master/` làm 40 → 53 phát hiện).
3. `session_claim` hồ sơ trước đã nhả (tránh stale-takeover 30′ đánh thức nhầm).
4. Kickoff khai lại `quota` (NLM/TVPL) và `max_units_per_session` — quota là của LƯỢT, không kế thừa.
5. Khai `skill_version_toi_thieu`: nhiều bất biến đường ghi chỉ được cưỡng chế từ **v1.36.20** (r281/r282).
6. Nợ `no_treo` của hồ sơ trước phải được **nêu lại** trong kickoff mới nếu cùng phạm vi văn bản.

## 8. ĐỢT (`dot`) — ánh xạ Kế hoạch rà soát của cơ quan vào state

Kế hoạch của cơ quan chia việc theo **Đợt**; state KHÔNG mọc thêm hàng đợi cho việc đó. **Một Đợt = tập con
`q_units` cùng `dot_id`**, mô tả Đợt nằm ở mảng `dot` (trên). Kịch bản vận hành + điều kiện đóng Đợt:
`references/RASOAT_HOSO_LOOP.md` §1bis.

| Trường | Bắt buộc | Ý nghĩa |
|---|---|---|
| `dot_id` | có | khoá ngắn (`dot-01`), dùng ở `q_units[].dot_id` và `q_ingest[].dot_id` |
| `ten` | có | tên Đợt ĐÚNG như Kế hoạch của cơ quan gọi — không đặt tên riêng |
| `trang_thai` | có | enum mục 3 |
| `mo_luc` / `dong_luc` | có khi đã mở/đóng | mốc thời gian |
| `gioi_han_da_biet` | bắt buộc khi `da_dong_co_gioi_han` | cùng khuôn §7.1 — không có mục = không được đóng |

**Bất biến Đợt:**

1. **Tuần tự** — tối đa MỘT Đợt ở `dang_ra`. Hai Đợt chồng nhau thì `dry_rounds_lien_tiep` và Q-INGEST
   không quy được về Đợt nào.
2. Đơn vị `doi_chieu_bo_sung` sinh do nguồn nạp giữa chừng thuộc **Đợt đang mở**, KHÔNG mở lại Đợt cũ.
3. `dot_id` là **nhãn**, không phải trạng thái: đổi `dot_id` của một đơn vị `done` không hạ nó về `pending`.
