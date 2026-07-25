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
  "q_units": [
    {"unit_id": "unit-001", "van_ban": "18-2025-VBHN-VPQH", "dieu": ["54"], "tang": "SAU",
     "trang_thai": "done", "loai": "ra_soat"},
    {"unit_id": "unit-009", "van_ban": "18-2025-VBHN-VPQH", "dieu": ["125"], "tang": "DOI_CHIEU",
     "trang_thai": "pending", "loai": "doi_chieu_bo_sung", "doi_chieu_voi": "145-2026-ND-CP"}
  ],
  "q_ingest": [
    {"so_hieu": "145-2026-ND-CP", "trang_thai": "staged", "plan_hash": "…", "nguon": "vbpl.vn"}
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
- `q_ingest.trang_thai`: `cho_tai | cho_nguoi_tai | dry_planned | staged | flipped | out_of_scope`.
- `q_nlm.trang_thai`: `pending | added | failed`.

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
