# KẾT QUẢ thi hành Q-A / Q-B / Q-C (lượt 26) — 31-07-2026

Nguồn việc: `rasoat/PROMPT_TIEP_NLM_2026-07-31b.md` (master `e8b2243`) — 3 mục lượt 25 để lại chờ duyệt.
Sổ nền: `rasoat/KETQUA_US_NLM_QUEUE_2026-07-31.md`.
**Phê duyệt trong phiên:** Q-A = nạp lại NLM · Q-B = re-push canonical rồi gỡ raw (nhánh 45-2019) ·
Q-C = gỡ `9e985570`. Cả 3 đều chọn phương án KHUYẾN NGHỊ.

## 0. Điều kiện tiên quyết (ĐO, không suy)

| Mục | Bằng chứng |
|---|---|
| US-egress | exit IP `160.79.106.25` — Columbus/Ohio/US (AS396982 Google) qua `ipinfo.io` |
| Bootstrap | `tl_fetch.sh --setup` rc=0 · gws 0.22.5 · webapp ping `2.21.2p` · registry 1316 dòng / corpus **696** |
| NLM auth | `nlm-install` → `nlm-auth-load` → `nlm-auth-status` **`alive:true`**, probe LIVE 743ed200 |
| MCP notebooklm | **KHÔNG có** (giống container lượt 25) ⇒ nhánh 2 PDF của Q-B vẫn chặn kỹ thuật |

Client v1.36.16, master `e8b2243`.

## 1. Kiểm chứng lượt 25 TRƯỚC khi ghi (không tin sổ, đo LIVE)

| Kiểm | Kết quả |
|---|---|
| Slot LIVE `slot-audit --all-shards` | 743ed200=**299** · 45739ff7=**292** · 2d8c2fef=**22** · 80742228=**108** — khớp TUYỆT ĐỐI sổ lượt 25 |
| Việc 1 (176/2025) | `1hQedQKZ…` corpus=true on_nlm=true sid `64c5c6a4` · `1auEnrsy…` corpus=false on_nlm=false ✓ |
| `nlm-audit-physical` | rc=1 — đúng 2 finding tồn: `pointer_dead=1` (KL_195) · `dup_physical=1` (Công đoàn) |

⇒ Không hồi quy, không phiên khác chen vào. 3 mục chờ duyệt còn nguyên trạng.

## 2. Q-C — gỡ trùng vật lý `Luat_50-2024-QH15_Cong_doan` (làm TRƯỚC để dôi slot)

**Đo trước khi gỡ (bắt buộc — không gỡ mù):** `nlm-content --no-fallback` cả hai sid, rc=0 cả hai,
**5302 bytes, sha256 GIỐNG HỆT** `2037403a08c2b0544468e8858e8e7c31e32c9cc023ee28c46e3b6361fee5f4de`
⇒ gỡ bản nào cũng không mất nội dung. Registry trỏ `1e9d957b` (đúng bản `nlm-audit-physical` khuyên GIỮ)
⇒ gỡ `9e985570` không tạo con trỏ treo.

`tl nlm-source-remove 9e985570-… --apply --confirm yes` → `deleted:1`, journal `nlm-source-remove_1785462069_11073`.
**Readback `nlm-list` tươi:** 292 → **291**, còn đúng 1 nguồn Công đoàn = `1e9d957b`. ✓

## 3. Q-A — nạp lại `KL_195-2025-KL-TW` (con trỏ chết)

Xác nhận chết bằng listing VẬT LÝ trước: `nlm-list 45739ff7` **không có** mục nào chứa `195` ⇒ sid
`6039b2a5` chết thật, không phải lỗi đọc.

`tl --profile vbqppl nlm-add 45739ff7-… --drive-id 1rpMJpDB… --type doc --row-kind own --no-fallback`
→ sid mới **`52eb0e58-1384-49bf-ad0c-878bc48c4a52`**, `ready:true`; `reg_link` journal `nlm-add-link_1785462221_12155`.

**Readback keyed (`count=1` trước khi tin `rows[0]`):** corpus=`true` · on_nlm=`True` ·
nlm_status=`pushed` · sid=`52eb0e58…` · nb=`45739ff7` · row_kind=`own`. ✓

⇒ Nợ phủ được TRẢ, không phải bị CHE. `--clear-stale` **không cần chạy** và đã KHÔNG chạy.

## 4. Q-B nhánh 45-2019 — re-push canonical → gỡ raw

### 4.1 Bẫy phát hiện TRƯỚC khi ghi (nếu không thấy thì hỏng như ca 176 lượt 25)

`nlm-list` cho thấy nguồn docx **thô** `04e51f9c` trên NLM đang mang **ĐÚNG tên canonical**
`BLuat_45-2019-QH14_Bo_luat_lao_dong` (registry ghi tên `…_lao_dong.docx` — sổ và NLM LỆCH TÊN).
⇒ `nlm-add` canonical sẽ bị **cổng dedup-live theo TÊN** chặn `ALREADY_ON_NOTEBOOK`.
Chọn **đổi tên nguồn thô về đúng tên registry** thay vì `--skip-live-check` (không phá cổng an toàn).

`tl --profile vbqppl source-rename 1zsmfCS1… --name Luat_45-2019-QH14_Bo_luat_lao_dong.docx --rename-drive --apply`
→ `nlm_rename.ok=true rc=0`; `drive_rename` oldName == newName (Drive vốn đã đúng, no-op thật);
journal `source-rename_1785462302_13239`.

### 4.2 Add canonical TRƯỚC, gỡ raw SAU (bảo toàn độ phủ tuyệt đối)

`tl --profile vbqppl nlm-add 45739ff7-… --drive-id 1rjx9MLS… --type doc --row-kind own --no-fallback`
→ sid **`6cce35ec-035b-4973-8902-af5813390e01`**, `ready:true`; journal `nlm-add-link_1785462460_13601`.

**Verify độ phủ THẬT trước khi gỡ** (không tin `ready`): `nlm-content 6cce35ec… --no-fallback` rc=0,
5356 bytes, nội dung thật: *"Bộ luật số: 45/2019/QH14 … BỘ LUẬT LAO ĐỘNG … Điều 1. Phạm vi điều chỉnh"*.
Readback keyed canonical `1rjx9MLS…`: corpus=true · on_nlm=True · nlm_status=pushed · sid `6cce35ec…`. ✓

### 4.3 Gỡ raw + đồng bộ sổ

`nlm-source-remove 04e51f9c…` lần đầu **fail-closed đúng thiết kế** (`POINTER_STILL_ATTACHED`, skipped=1).
Chọn `--force` (gỡ vật lý trước, sổ theo sau) — đúng tiền lệ lượt 25 + SKILL #16 "registry chỉ ghi sự
thật ĐÃ xác minh vật lý". → `deleted:1`, journal `nlm-source-remove_1785463123_2984`.

★★ **ĐÍNH CHÍNH (thêm sau khi thấy `5c12dd6`): bước gỡ raw này BỊ TRÙNG với một phiên song song, và
phiên kia làm TRƯỚC.** Xem §4.4.

`tl --profile vbqppl register --drive-id 1zsmfCS1… --nlm-status removed_by_user --no-autofill --apply`
→ trả **`verified:false` + `error:FIELDS_DROPPED_ON_WRITE`**, journal `register_1785463754_2272`.
★ **KHÔNG tin thông báo — đo readback keyed:** `count=1`, on_nlm=`False`, nlm_status=`removed_by_user`,
sid `04e51f9c…` giữ làm lịch sử, row_kind=overflow. **Field đích ĐÃ vào**; `FIELDS_DROPPED_ON_WRITE`
rơi vào field khác. Đây đúng là lý do readback là bằng chứng DUY NHẤT.

### 4.4 ★★ VA CHẠM HAI PHIÊN SONG SONG — đính chính quyền tác giả

Sau khi đẩy sổ, `git fetch` lộ ra master đã nhảy `e8b2243` → **`5c12dd6`** ("lượt 25 vòng 2"): **một
phiên khác cùng lúc cũng được duyệt Q-A/Q-B/Q-C và cùng thao tác trên 45739ff7.**

Phiên kia phát hiện ra phiên NÀY trước (họ ghi ở §8 sổ của họ): `nlm-add` KL_195 của họ bị cổng dedup
chặn `ALREADY_ON_NOTEBOOK` với sid `52eb0e58…` — chính sid phiên này vừa tạo — và ba đổi thay
`+52eb0e58` / `−9e985570` / `+6cce35ec` không có trong `tl journal` của họ. Họ xử ĐÚNG: **dừng mọi lệnh
`add`, không ghi đè, chỉ làm nốt phần còn thiếu.**

**Phân định thật (theo dấu thời gian journal, epoch trong tên journal):**

| Thao tác | Ai làm THẬT | Bằng chứng |
|---|---|---|
| Q-A add KL_195 `52eb0e58` | **phiên này** | `nlm-add-link_1785462221_12155`; phiên kia bị dedup chặn |
| Q-C gỡ dup `9e985570` | **phiên này** | `nlm-source-remove_1785462069_11073` |
| Q-B rename raw + add canonical `6cce35ec` | **phiên này** | `source-rename_…302_13239` · `nlm-add-link_…460_13601` |
| **Q-B gỡ raw `04e51f9c`** | **PHIÊN KIA — trước 59 giây** | họ `…_1785463064_2269` · tôi `…_1785463123_2984` |
| **register `1zsmfCS1` removed_by_user** | **PHIÊN KIA trước** | họ `…_1785463084_2631` · tôi `…_1785463754_2272` |

⇒ §4.3 ở trên KHÔNG được đọc là "phiên này gỡ raw". Lệnh `--force` của tôi trả `deleted:1` **sau khi**
lệnh của họ đã chạy; hai lệnh cùng đích, cùng giá trị, idempotent nên **kết quả không hỏng**, nhưng công
là của họ. Ghi lại đúng để lượt sau không đếm đôi.

**Kiểm chứng lại sau va chạm** (chạy khi đã thấy `5c12dd6`): `nlm-audit-physical` rc=0 `clean:true`
(4 counter = 0) · 45739ff7 = 292 · 4 dòng then chốt đúng đích (KL_195 `52eb0e58` pushed · canonical
`6cce35ec` pushed · raw `04e51f9c` removed_by_user · Công đoàn còn `1e9d957b`). **Không có hư hại do
ghi đôi.**

★ **Bài học phải giữ:** `nlm-add` có cổng dedup-live nên va chạm `add` bị chặn TỰ ĐỘNG — đó là thứ duy
nhất cứu lượt này. Nhưng `nlm-source-remove --force` và `register` **KHÔNG có cổng nào**: hai phiên cùng
gỡ/cùng ghi thì lệnh sau chạy trên trạng thái đã đổi mà vẫn trả `ok`. Cùng doctrine "hai phiên song song
⇒ DỪNG, đối chiếu" của §Quy ước deploy: **trước lô ghi NLM/registry, `git fetch origin master` và kiểm
xem có phiên khác đang mở cùng đợt không** — chốt này hiện CHƯA có ai cưỡng chế.

## 5. Đối soát chốt toàn cục (sau lượt)

**`nlm-audit-physical` rc=0 `clean:true`** — lần đầu shard SẠCH tuyệt đối:

| counter | trước lượt | sau lượt |
|---|---|---|
| `pointer_dead` | 1 (KL_195) | **0** |
| `dup_physical` | 1 (Công đoàn) | **0** |
| `pointer_mismatch` | 0 | 0 |
| `unregistered_physical` | 0 | 0 |

**Số học slot khớp chính xác từng bước** trên 45739ff7:
292 → −`9e985570` **291** → +`52eb0e58` **292** → +`6cce35ec` **293** → −`04e51f9c` **292**.
743ed200 = 299 · 2d8c2fef = 22 (không đụng).

`nlm-reconcile --all-notebooks` (DRY): **`desync_real` = 0 / 0 / 0** cả ba notebook (nợ KL_195 hết THẬT),
`coverage_gap` = **0** trên 45739ff7, `link_candidates` = 0, `backfill` = 0.

## 6. Phát hiện MỚI trong lúc đối soát — TỒN SẴN, chưa duyệt, KHÔNG tự làm

1. **`CU_ILO-128` trùng CHÉO notebook** — `nlm-reconcile 45739ff7` báo `unregistered_on_nlm=1`:
   sid `c4f16911-f255-4876-9735-ad7c3fa40964` (`CU_ILO-128_Tro_cap_tan_tat_tuoi_gia_tu_tuat_1967`) nằm
   VẬT LÝ trên 45739ff7, trong khi registry chỉ biết bản trên 743ed200 (row `1All5aL5HNRwXSYSsibTLGrZb234xx5gDBjpcUuoKibE`,
   sid `a8e7b4e8…`, corpus=true, on_nlm=true).
   ★ Vì sao `nlm-audit-physical` KHÔNG bắt: nó dedup theo title **trong từng notebook**, còn cặp này
   nằm ở HAI notebook khác nhau ⇒ hai công cụ nhìn hai góc, phải đọc CẢ HAI.
   Đây là mục trồi lên SAU khi gỡ dup Công đoàn (trước đó `unregistered_sample` là `9e985570…`).
   Không do lượt này sinh ra — chưa hề đụng nguồn ILO nào.
2. **`removed_family_still_live = 7`** trên 45739ff7 — chưa điều tra, ngoài phạm vi duyệt.
3. **Registry row Công đoàn `1MogfQLK…` SAI so với vật lý**: sổ ghi `on_nlm=False` +
   `nlm_status=removed_by_user`, trong khi sid `1e9d957b` **SỐNG thật** trên 45739ff7 (đã đọc bằng
   `nlm-list` và `nlm-content` rc=0). Đây là dòng corpus=true ⇒ nhiều khả năng đang bị đếm oan vào
   `CORPUS_TRUE_NOT_ON_NLM` (53 → có thể 52). `nlm-audit-physical` KHÔNG bắt vì `pointer_mismatch` chỉ
   soi dòng tự nhận `on_nlm=true` — sai theo chiều "sổ nói đã gỡ mà vật lý còn" thì lọt lưới.
   Chưa sửa (không được duyệt ghi field này). Sửa = `register --drive-id 1MogfQLK… --nlm-status pushed`.

## 7. Còn treo sau lượt 26

- **Q-B phần còn lại — 3 nguồn `raw_on_nlm`** (duyệt lượt này chỉ phủ nhánh 45-2019):
  `1PWj5iUJb1pcd5Q1TItAeDhuZvqrdgdK2` (TL_ILO, sid `9c0611ad…`) ·
  `19_6Mp_8e1NQerD5ed42A5TRlO7W14VWt` (PDF, `c0d3c268…`) ·
  `1h0kl-G4-8l7r_rvOMSlVlXu3su1IwSvU` (PDF, `52f8ac58…`).
  2 PDF cần phiên **có MCP notebooklm** (memory `nlm-add-pdf-drive-fail`).
- 3 phát hiện §6.
- `CORPUS_TRUE_NOT_ON_NLM` 53 — nợ CẤU TRÚC do trần 300/notebook (nay 45739ff7 còn 8 slot, 743ed200 còn 1).
- **Memory topic `rasoat-hoso-orchestration-plan` CHƯA cập nhật** — phiên này không có công cụ memory;
  người/phiên có memory cần chép §5-§7 vào đầu topic.
- Ngoài phạm vi (giữ nguyên): note dup↔bản chuẩn · lô 3b 43 tên thiếu chủ đề · r vá auditor/doc-text ·
  sheet-dup `1Qja1Lwp…` Kế toán (CẤM reg-delete) · 43 row_kind overflow · quarantine hẳn `1auEnrsy…` ·
  BC thẩm tra mẫu P9. Deploy: nợ 0 (Drive = v1.36.16) — lượt này KHÔNG đụng code/deploy.

## 8. Nếp mới rút ra (bổ sung cho lượt sau)

- **Cổng dedup-live theo TÊN bắt cả trường hợp NLM và registry LỆCH TÊN.** Trước khi `nlm-add`, đọc
  `nlm-list` xem tên VẬT LÝ đang là gì — đừng suy từ tên registry. Cách gỡ đúng là **đổi tên cho khớp
  sổ**, không phải `--skip-live-check`.
- **`register` có thể trả `verified:false` + `FIELDS_DROPPED_ON_WRITE` mà field đích VẪN VÀO.** Đọc
  readback keyed rồi mới kết luận — cả hai chiều (đừng vội chạy lại, dễ ghi đè lần hai).
- **`nlm-audit-physical` và `nlm-reconcile` KHÔNG thay thế nhau**: cái đầu dedup trong-notebook, cái sau
  bắt trùng chéo-notebook. `clean:true` của cái đầu KHÔNG có nghĩa sạch toàn cục (§6 mục 1 là bằng chứng).
- Gỡ nguồn trùng: **đo `nlm-content --no-fallback` + so sha256 hai bản** trước khi gỡ, đừng tin tên giống.
