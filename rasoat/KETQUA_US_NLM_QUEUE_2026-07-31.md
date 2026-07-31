# KẾT QUẢ XỬ HÀNG ĐỢI NLM từ container US-egress (lượt 25) — 31-07-2026

Nguồn việc: `rasoat/PROMPT_US_NLM_QUEUE_2026-07-31.md` (master `0765e7a`) — 4 việc sau lượt 24.
Sổ nền: `rasoat/KETQUA_GHI_BANGDUYET_CORPUS_AUDIT_2026-07-31.md` (`69b1819`).

## 0. Điều kiện tiên quyết (ĐO, không suy)

| Mục | Bằng chứng |
|---|---|
| US-egress | exit IP `160.79.106.107` — Columbus/Ohio/US (AS396982 Google) qua `ipinfo.io` |
| Bootstrap | `tl_fetch.sh --setup` rc=0 · gws 0.22.5 · webapp ping `2.21.2p` · registry 1316 dòng / corpus 695 |
| NLM auth | `nlm-auth-load` (cookie ~0 ngày) → **`nlm-auth-status` `alive:true`**, probe LIVE notebook 743ed200, `age_min 39.7` |

Client v1.36.16, master `0765e7a` (không tụt sau origin/master).

## 1. Kết quả từng việc

| Việc | Kết quả | Journal / bằng chứng |
|---|---|---|
| **1** chuỗi 176/2025 | ✅ TRỌN. Bản mới `1hQedQKZ…` **corpus=true + on_nlm=true** (sid `64c5c6a4-bca4-4289-8958-67c6213b5b7f`, nb 45739ff7, `ready`); bản khuyết `1auEnrsy…` **sạch NLM vật lý** + corpus=false | `nlm-source-remove_1785459691_17187` · `nlm-add-link_1785459850_17549` · `register_1785460139_19001` (verified=true) |
| **2** 9 nguồn tên cũ | ✅ **9/9 khớp LIVE** — nhưng chỉ **5** cần chạy: 4 nguồn (QD_127 · QD_33 · ND_356 · QD_804) ĐÃ mang tên mới sẵn ⇒ bỏ qua đúng chỉ thị | 5× `source-rename_1785460301…460471`, mỗi lệnh `nlm_rename.ok=true rc=0`, verify lại bằng `nlm-list` tươi |
| **3** 2 dòng nlm-only | ✅ ĐO XONG — **cả hai SỐNG**, không phải nguồn chết ⇒ chỉ ghi nhận, KHÔNG ghi gì | `nlm-content --no-fallback` rc=0, nội dung thật (xem §3) |
| **4** tồn cũ | ◑ MỘT PHẦN — 2 ghost đã gỡ; cụm `raw_on_nlm` (gồm docx 45-2019) **HOÃN có lý do** (§4) | `nlm-source-remove_1785460809_26616` · `register_1785460988_26982` · `register_1785461015_26985` |

## 2. Việc 1 — chi tiết + 2 lệch so với kế hoạch (có lý do)

**Lệch 1 — notebook đích: 45739ff7 chứ KHÔNG phải 743ed200 gợi ý.**
`slot-audit --all-shards` LIVE: 743ed200 = **300/300 FULL**. Prompt đã dặn "notebook do routing quyết
nếu gợi ý không hợp — đừng ép". Chọn shard VBQPPL-2 `45739ff7` (293/300, còn 7 slot) vì (a) đúng
topology corpus VBQPPL, (b) chính là nơi nguồn 176-khuyết đang nằm ⇒ gỡ 1 + thêm 1 = **hoà slot**.

**Lệch 2 — ĐẢO thứ tự: gỡ TRƯỚC, add SAU.**
Đo LIVE cho thấy nguồn 176-khuyết `16e6a29f` **VẪN SỐNG** trên 45739ff7 dù registry ghi
`nlm_status=removed_by_user` (sổ tin sai — đúng họ lỗi "registry nói đã gỡ mà vật lý còn"). Nó mang
**tên trùng khít** với GDoc mới ⇒ chạy `nlm-add` trước sẽ bị cổng dedup-live chặn `ALREADY_ON_NOTEBOOK`.
Ép qua bằng `--skip-live-check` là phá cổng an toàn ⇒ đảo thứ tự thay vì phá cổng.

`nlm-source-remove` fail-closed đúng thiết kế lần đầu (`POINTER_STILL_ATTACHED`, rc=2). Chọn `--force`
(gỡ vật lý trước, sổ theo sau) thay vì xoá con trỏ registry trước — đúng nguyên tắc SKILL #16
"registry chỉ ghi sự thật ĐÃ xác minh vật lý".

**Readback keyed cuối (đều `count=1` trước khi tin `rows[0]`):**
- `1hQedQKZ…` → corpus=`true` · row_kind=own · on_nlm=true · sid `64c5c6a4…` · nlm_status=pushed
- `1auEnrsy…` → corpus=`false` · on_nlm=false · nlm_status=removed_by_user

★ **`nlm-reconcile --clear-stale` — CỐ Ý KHÔNG CHẠY.** DRY cho thấy `desync_real` **duy nhất** trên
45739ff7 là **`KL_195-2025-KL-TW`** — một dòng khác, ngoài phạm vi, chưa từng điều tra; nó đồng thời
nằm trong `coverage_gap` ⇒ cách chữa đúng nhiều khả năng là **nạp lại NLM**, không phải xoá mapping
(xoá sẽ CHE mất nợ phủ của một văn bản corpus=true). Dòng 176-khuyết rơi vào nhóm `already_removed`
mà `--clear-stale` cố ý không đụng, nên chốt này KHÔNG cần cho chuỗi 176. Xem §5 mục 1.

## 3. Việc 3 — hai nguồn nlm-only đều SỐNG (bác giả thiết "chết")

Đo bằng `nlm-content <sid> --no-fallback` (bắt buộc `--no-fallback`: mặc định có fallback CORPUS,
đọc được sẽ tưởng nhầm nguồn NLM còn sống).

| sid | rc | Nội dung thật đọc được |
|---|---|---|
| `398d50d7-a639-4528-8820-56644b12fb3e` | 0 | "Số 59-NQ/TW — Hà Nội, ngày 24 tháng 01 năm 2025 · NGHỊ QUYẾT CỦA BỘ CHÍNH TRỊ VỀ HỘI NHẬP QUỐC TẾ TRONG TÌNH HÌNH MỚI" |
| `e583ebea-db66-4cdd-94d9-df663cfc5f54` | 0 | "Phụ lục I — MẪU TỜ TRÌNH THẨM ĐỊNH, PHÊ DUYỆT DỰ ÁN (Kèm theo Nghị định số /2019/NĐ-CP)" |

⇒ Theo chỉ thị "nguồn SỐNG → chỉ ghi nhận", KHÔNG hạ corpus, KHÔNG nạp lại. Cờ audit header để auditor.

## 4. Việc 4 — làm 2, HOÃN 2 (nêu rõ lý do, không giấu)

**ĐÃ LÀM (an toàn, độ phủ canonical còn nguyên):**

| Mục | sid | Sau khi gỡ |
|---|---|---|
| ghost `CD_32-2026-CD-TTg` (row `1reK6yi4…`, corpus=false) | `5ec30323-6dc6-4fcc-9934-76fdab011b28` | on_nlm=false · nlm_status=removed_by_user (readback keyed count=1) |
| bản THIẾU 131-2021 (row `1831ZvZ1…`, corpus=false) | `a37de447-c505-4925-8b7f-15d7604bb3a8` | on_nlm=false · nlm_status=removed_by_user (readback keyed count=1) |

Đã kiểm TRƯỚC khi gỡ: 131-2021 vẫn còn **chính văn** `de667acd` + **phụ lục** `8d9692e0` sống trên
743ed200 ⇒ gỡ bản thiếu không mất độ phủ. Registry đồng bộ bằng `register --nlm-status removed_by_user`
theo đúng quy ước đã có ở dòng 176-khuyết (giữ sid làm lịch sử).

**HOÃN — cụm `raw_on_nlm` 4 nguồn, GỒM CẢ docx 45-2019:**

```
1PWj5iUJb1pcd5Q1TItAeDhuZvqrdgdK2              TL_ILO_2026_AI_tao_sinh_va_viec_lam_VN     9c0611ad…
1zsmfCS1IjtwIaeuftBx5H0h6iInGzIsU              Luat_45-2019-QH14_Bo_luat_lao_dong.docx    04e51f9c…
19_6Mp_8e1NQerD5ed42A5TRlO7W14VWt              VBT_PL_BC_BHXH_HaNoi_khao_sat_6-2026.pdf   c0d3c268…
1h0kl-G4-8l7r_rvOMSlVlXu3su1IwSvU              VBT_BC_BHXH_HaNoi_thuc_hien_CS_BHXH_2025.pdf 52f8ac58…
```

★ **Vì sao KHÔNG gỡ docx 45-2019 dù prompt bảo "gỡ":** đo LIVE thấy nguồn **canonical**
`BLuat_45-2019-QH14_Bo_luat_lao_dong` (`1rjx9MLS…`, corpus=true) có sid `be17c942…` nhưng
**VẮNG khỏi NLM** (`nlm_status=removed_by_user`). Nguồn NLM **duy nhất** của Bộ luật Lao động 45/2019
hiện chính là file docx thô đó. Gỡ trần ⇒ **BLLĐ 2019 biến mất hoàn toàn khỏi NLM** — đó là mất độ phủ
một bộ luật lõi, không phải hygiene. Phác đồ đúng đã ghi trong sổ lượt trước
(`KETQUA_GHI_KHO_NEN_2026-07-31.md` dòng 56 + `sweep` NEXT ACTION) là **convert GDoc → re-push → gỡ raw
+ reg_clear mapping**, và cụm này nằm ở mục **"Còn treo — KHÔNG thuộc phạm vi duyệt lượt này"** ⇒ theo
đúng chỉ thị "chưa duyệt thì TRÌNH". Đề xuất ở §5 mục 2.

Ghi chú: 2/4 là **PDF** ⇒ theo memory `nlm-add-pdf-drive-fail`, không add được bằng `--drive-id`, phải
download + MCP `source_add source_type=file`. **Phiên này KHÔNG có MCP notebooklm** ⇒ nhánh PDF chặn kỹ
thuật ở đây, cần phiên có MCP.

## 5. Việc TRÌNH — chờ người dùng duyệt (không tự làm)

1. **`KL_195-2025-KL-TW` (`1rpMJpDB…`, corpus=true) — con trỏ CHẾT.** `nlm-audit-physical` báo
   `pointer_dead=1`: sid `6039b2a5-6416-4fd2-8161-b14c514bc948` không còn trên NLM. Hai đường: (a) **nạp
   lại** NLM (đúng hơn — đây là văn bản corpus=true, đang là nợ phủ), hay (b) `--clear-stale` xoá mapping
   (che nợ). Đề xuất (a).
2. **Cụm `raw_on_nlm`** — duyệt phác đồ convert→re-push→gỡ cho từng nguồn? Riêng 45-2019 khuyến nghị
   làm SỚM (đang là văn bản lõi mà chỉ có nguồn thô): re-push canonical `1rjx9MLS…` vào 45739ff7 (còn
   8 slot) rồi mới gỡ `04e51f9c`. Nhánh 2 PDF cần phiên có MCP notebooklm.
3. **Trùng vật lý `Luat_50-2024-QH15_Cong_doan`** — `dup_physical=1`: hai nguồn `9e985570…` và
   `1e9d957b…` cùng tên trên 45739ff7. `nlm-audit-physical` gợi ý gỡ `9e985570…`, giữ `1e9d957b…`.
   Chưa duyệt ⇒ chưa gỡ.

★ Cả 3 phát hiện đều **CÓ TRƯỚC lượt này** — chúng đã nằm trong bản DRY `nlm-reconcile` chụp TRƯỚC lệnh
ghi đầu tiên (`unregistered_sample` = `9e985570…`; `desync_real_sample` = `195-2025-KL-TW`). Không phải
hệ quả của lượt 25.

## 6. Đối soát chốt toàn cục (sau lượt)

`nlm-reconcile --all-notebooks` (DRY) — số học khớp **tuyệt đối** với thao tác đã làm:

| notebook | LIVE trước | LIVE sau | Giải thích |
|---|---|---|---|
| 743ed200 (nền) | 300/300 FULL | **299** | −1 ghost CD_32 ⇒ hết FULL, còn 1 slot |
| 45739ff7 (VBQPPL-2) | 293 | **292** | −176 khuyết −131 thiếu +176 mới ⇒ còn 8 slot |
| 2d8c2fef (ILO/điều ước) | 22 | 22 | chỉ đổi tên, không thêm/bớt |

`desync_real`: 743ed200 = 0 · 45739ff7 = 1 (KL_195, có sẵn) · 2d8c2fef = 0.
`nlm-audit-physical` rc=1 với đúng 2 finding tồn đọng ở §5 (mục 1 và 3).

## 7. Còn treo sau lượt 25

- 3 mục §5 (chờ duyệt).
- `CORPUS_TRUE_NOT_ON_NLM` 53 — nợ CẤU TRÚC do trần 300/notebook; nay đã dôi 9 slot (1 + 8) nhưng
  không đủ, cần shard mới nếu muốn kéo về 0.
- Ngoài phạm vi (giữ nguyên): note dup↔bản chuẩn (cần đường đọc cột note GAS) · lô 3b 43 tên thiếu
  chủ đề · r vá auditor/doc-text · sheet-dup `1Qja1Lwp…` Kế toán (CẤM reg-delete) · 43 row_kind
  overflow · quarantine hẳn bản khuyết 176 (`1auEnrsy…`) · BC thẩm tra mẫu P9.
- Deploy: nợ 0 (Drive = v1.36.16). Lượt này KHÔNG đụng code/deploy.
