# KẾT QUẢ XỬ HÀNG ĐỢI NLM từ container US-egress (lượt 25) — 31-07-2026

Nguồn việc: `rasoat/PROMPT_US_NLM_QUEUE_2026-07-31.md` (master `0765e7a`) — 4 việc sau lượt 24.
Sổ nền: `rasoat/KETQUA_GHI_BANGDUYET_CORPUS_AUDIT_2026-07-31.md` (`69b1819`).

★★ **ĐỌC KÈM — hai sổ, một đợt việc.** Vòng 2 của sổ này (§8-§11) chạy SONG SONG với phiên **P15**
trên cùng notebook 45739ff7; sổ phía kia là `rasoat/KETQUA_NLM_QA_QB_QC_2026-07-31.md` (lượt 26,
commit `326c33d`) + bàn giao `rasoat/PROMPT_TIEP_NLM_2026-07-31c.md`. **Phân định quyền tác giả chính
xác: §4.4 sổ lượt 26.** Tóm tắt: Q-A + Q-C + rename/add canonical do P15 làm; **gỡ raw `04e51f9c` +
`register` do phiên này (`5c12dd6`) làm trước 59 giây**, P15 chạy trùng (idempotent, không hư hại).
Trạng thái chốt được HAI phiên đo ĐỘC LẬP và trùng khớp: `nlm-audit-physical` rc=0 (`clean:true`),
`desync_real` 0/0/0, `coverage_gap` 0. Bàn giao còn hiệu lực là bản **`…-31c.md`** (R-1…R-5), bản
`…-31b.md` đã bị nó thay thế.

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

---

# VÒNG 2 (cùng ngày) — người dùng duyệt «theo khuyến nghị»

Phê duyệt nguyên văn: «tôi duyệt theo khuyến nghị. hãy thực hiện» ⇒ thi hành Q-A, Q-B (ưu tiên
45-2019), Q-C của §5.

## 8. ★ PHÁT HIỆN LỚN: có TÁC NHÂN KHÁC ghi song song vào notebook 45739ff7

Khi bắt tay làm Q-A, `nlm-add` bị cổng dedup chặn `ALREADY_ON_NOTEBOOK` với sid `52eb0e58…` — một
nguồn KL_195 mà bản dump LIVE trước đó KHÔNG có. So khớp tập hợp 3 bản dump liên tiếp (v2→v3→v4) lộ ra
notebook đang bị sửa TRONG LÚC đo, không phải do phiên này:

| Đổi | Nguồn | Do ai |
|---|---|---|
| `+52eb0e58` KL_195-2025-KL-TW | xuất hiện | **KHÔNG phải tôi** |
| `−9e985570` Luat_50-2024 Công đoàn (bản trùng) | biến mất | **KHÔNG phải tôi** |
| `+6cce35ec` BLuat_45-2019 canonical (status 1→2) | xuất hiện | **KHÔNG phải tôi** |

Bằng chứng phủ định: `tl journal` liệt kê ĐÚNG 13 run của phiên này (3 `nlm-source-remove`, 1 `nlm-add`
+link, 3 `register`, 5 `source-rename`) — KHÔNG có lệnh nào gỡ `9e985570` hay add `52eb0e58`/`6cce35ec`.
Ba thay đổi đó đúng bằng ba khuyến nghị Q-A/Q-B/Q-C ⇒ nhiều khả năng người dùng đã giao cùng phê duyệt
cho một phiên song song (nếp P15), hoặc tự chạy.

**Ứng xử:** DỪNG mọi lệnh `add` (sẽ tạo trùng — cổng dedup đã chặn đúng 1 lần), chỉ đo lại rồi làm nốt
phần CÒN THIẾU. Không ghi đè việc của phiên kia. Cùng doctrine "hai phiên song song ⇒ dừng, đối chiếu"
của §Quy ước deploy.

## 9. Kết quả vòng 2

| Mục | Trạng thái | Ai làm |
|---|---|---|
| **Q-A** KL_195 | ✅ registry đã trỏ `52eb0e58…`, corpus=true, on_nlm=true, `desync_real`→**0** | phiên khác |
| **Q-C** dup Công đoàn | ✅ chỉ còn `1e9d957b…` LIVE, `dup_physical`→**0** | phiên khác |
| **Q-B** re-push canonical BLLĐ | ✅ `6cce35ec…` ready(status 2), registry đã nối | phiên khác |
| **Q-B** gỡ docx thô 45-2019 | ✅ **PHIÊN NÀY LÀM** — sau khi verify canonical đọc được thật | `nlm-source-remove_1785463064_2269` + `register_1785463084_2631` |

Tiền đề tôi tự đặt đã kiểm ĐỦ trước khi gỡ: canonical `1rjx9MLS…` là **Google Doc** thật (`gws drive
files get`: mimeType `google-apps.document`, `trashed:false`), nguồn `6cce35ec` **status=2**, và
`nlm-content 6cce35ec --no-fallback` rc=0 trả nguyên văn "Bộ luật số: 45/2019/QH14 … Điều 1. Phạm vi
điều chỉnh". Chỉ khi đủ 3 bằng chứng mới gỡ `04e51f9c`.

**Readback keyed** dòng docx thô `1zsmfCS1…`: count=1 · corpus=false · on_nlm=**false** ·
nlm_status=removed_by_user.

★ Ghi chú `FIELDS_DROPPED_ON_WRITE`: lệnh `register` này trả `verified:false` + cờ đó (2 lệnh register
trước trả `verified:true`). Đã đối chiếu TOÀN BỘ 17 trường trước/sau: **chỉ đúng 2 trường mục tiêu đổi**
(`nlm_status`, `on_nlm`), không mất gì. Nguyên nhân: webapp BỎ QUA field RỖNG (`goc`/`hieuluc`/
`sua_doi`/`title_vn` vốn đã rỗng) — đúng hành vi đã biết trong CLAUDE.md, vô hại. **Bài học: cờ này
không đồng nghĩa hỏng ghi — nhưng bắt buộc diff toàn dòng mới được kết luận.**

## 10. Đối soát chốt sau vòng 2

- `nlm-audit-physical` → **rc=0 "SẠCH — pointer khớp vật lý toàn scope"** (trước vòng 2: rc=1 với
  `dup_physical=1` + `pointer_dead=1`).
- `nlm-reconcile --all-notebooks` → `desync_real` = **0/0/0**; `coverage_gap` = **0**.
- LIVE: 743ed200 = 299/300 · 45739ff7 = **292/300** (−docx thô +canonical, +KL195, −dup Công đoàn) ·
  2d8c2fef = 22/300.
- Còn 1 `unregistered_on_nlm` trên 45739ff7 = `c4f16911…` **`CU_ILO-128_Tro_cap_tan_tat_tuoi_gia`** —
  nguồn điều ước nằm VẬT LÝ ở 45739ff7 nhưng registry trỏ 743ed200 (`foreign_skipped`, by title).
  CÓ TRƯỚC lượt 25, ngoài phạm vi ⇒ để lại, có ghi.

## 11. Còn treo sau vòng 2

- **3 nguồn PDF `raw_on_nlm`** (`TL_ILO_2026` — đã xác minh mimeType `application/pdf`;
  `VBT_PL_BC_BHXH_HaNoi_khao_sat_6-2026.pdf`; `VBT_BC_BHXH_HaNoi_thuc_hien_CS_BHXH_2025.pdf`).
  **CHẶN KỸ THUẬT ở container này**: theo memory `nlm-add-pdf-drive-fail` phải download + MCP
  `source_add source_type=file`, mà phiên này KHÔNG có MCP notebooklm. Cần phiên có MCP.
  (Cụm `raw_on_nlm` từ 4 → **1 văn bản đã xong** (45-2019), còn 3 PDF.)
- `c4f16911` CU_ILO-128 lệch notebook (trên).
- `CORPUS_TRUE_NOT_ON_NLM` 53 — nợ CẤU TRÚC (trần 300/notebook), cần shard mới.
- Ngoài phạm vi giữ nguyên: note dup↔bản chuẩn · lô 3b 43 tên · r vá auditor/doc-text · sheet-dup
  `1Qja1Lwp…` Kế toán (CẤM reg-delete) · 43 row_kind overflow · quarantine hẳn `1auEnrsy…` · BC thẩm
  tra mẫu P9. Deploy: nợ 0 (Drive = v1.36.16).
