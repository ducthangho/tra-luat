# RASOAT_HOSO_LOOP — kịch bản VÒNG LẶP rà soát hồ sơ dự thảo luật (lớp điều phối)

> Phần TĨNH có cổng máy: `references/workflows/rasoat_hoso.json` (`workflow_card.v1`).
> Phần BIẾN ĐỘNG (state, hàng đợi, hằng số): `references/RASOAT_PLAN_SCHEMA.md` (`rasoat_plan.v1`).
> Quy trình rà 3 tầng: `references/QUY_TRINH_RA_SOAT_3_TANG.md`. Mẫu sổ phát hiện:
> `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json`.
> Tài liệu này = KỊCH BẢN vận hành: ai làm gì, theo thứ tự nào, bằng lệnh CÓ THẬT nào.
> **KHÔNG xây engine mới** — vòng lặp BỌC `tl rasoat-loop` + `tl frontier-expand` sẵn có và dùng nguyên
> bộ từ vựng hội tụ của chúng: `dry_rounds` / `max_iter` / `PAUSE`.

## §0. VAI TRÒ & RANH GIỚI (vi phạm = hỏng dữ liệu, không phải hỏng việc)

| Vai | Được làm | Cấm |
|---|---|---|
| **phiên chính** (đang cầm `session_claim`) | BÊN GHI DUY NHẤT: cập nhật state, ghi `master/<unit>.json`, chạy lệnh ghi registry qua cổng (`--apply --confirm yes --expected-plan-hash`), đẩy Drive | tự `--apply` khi người chưa duyệt lô; ghi khi KHÔNG cầm claim |
| **agent rà** (`tl-rasoat`, §6) | đọc cache/registry/NLM, trả JSON phát hiện | ghi BẤT KỲ file nào; mọi lệnh `--apply`/`register`/`ingest*`; sửa `scripts/tl.py` |
| **worker Q-NLM** (§3.5) | gọi NLM nạp nguồn TUẦN TỰ, trả JSON kết quả | ghi registry, ghi state, ghi file trong cây skill |
| **người** | duyệt lô nạp (điểm chạm ②), duyệt `--apply`, nghiệm thu + ký | — |

Lưới dưới cùng: registry ghi qua GAS có LockService + RMW nguyên tử (2.21.2p) — nhưng đó là lưới, KHÔNG
phải giấy phép cho hai phiên cùng ghi.

## §1. HỢP ĐỒNG GIAO VIỆC (kickoff) — người giao việc MỘT lần, đủ 8 mục

Thiếu mục nào ⇒ **hỏi TRƯỚC khi chạy vòng lặp**, không tự đoán (đoán sai = rà nhầm phạm vi, tiêu ngân sách
nhầm chỗ, hoặc nạp văn bản người ta không muốn). Mục có mặc định thì im lặng = nhận mặc định — mặc định
lấy từ `references/RASOAT_PLAN_SCHEMA.md` §4, kickoff override được từng hồ sơ.

| # | Mục | Người giao phải nêu | Im lặng = mặc định |
|---|---|---|---|
| 1 | **Phạm vi hồ sơ** | danh sách văn bản + profile đích (`--profile <P>`); hồ sơ = PROFILE, không đẻ khái niệm mới | **KHÔNG có mặc định — bắt buộc hỏi** |
| 2 | **Uỷ quyền nạp** | được tự nạp văn bản THUỘC hồ sơ theo làn staged hay không | có: làn staged `corpus=false`, người duyệt LÔ tại ② |
| 3 | **Uỷ quyền nguồn tải** | domain được tự tải; nguồn gated đi kênh Chrome đăng-nhập-sẵn | `vbpl.vn` · `congbao.chinhphu.vn` · `*.chinhphu.vn` · `*.gov.vn` · `quochoi.vn` · `dangcongsan.vn`; gated TVPL→LVN (§3.2) |
| 4 | **Ngân sách** | NLM call/hồ sơ · `quota_tvpl`/ngày | 60 · 100 (sổ đếm + phản ứng, không chặn sớm) |
| 5 | **Chính sách lỗi** | degrade-and-continue hay dừng sớm | degrade-and-continue (§5) — chỉ dừng khi mọi đơn vị còn lại cùng blocked |
| 6 | **Biến thể tự trị Loop B** | bật/tắt; bật thì ghi rõ điều kiện hẹp | TẮT (§3.4) |
| 7 | **Môi trường & đường ghi** | nơi chạy (local/Cowork/Claude chat) + `--out-dir` cho sổ nặng | local: `--out-dir` NGOÀI cây skill, đẩy Drive theo lô; chat: đẩy sau MỖI đơn vị (§7) |
| 8 | **Nghiệm thu & điểm dừng** | ai nghiệm thu/ký; cần dự thảo Phiếu A–G hay chỉ bảng master | Phiếu A–G nháp + bảng master + Q-APPROVALS + sổ lỗi; ba điểm chạm ①②③ giữ nguyên |

<!-- KICKOFF_CONTRACT_v1
muc_bat_buoc: pham_vi_ho_so | uy_quyen_nap | uy_quyen_nguon_tai | ngan_sach | chinh_sach_loi | bien_the_tu_tri | moi_truong_va_duong_ghi | nghiem_thu_va_diem_dung
khong_co_mac_dinh: pham_vi_ho_so
mac_dinh: nlm=60 | tvpl=100 | dry_rounds=2 | max_units_per_session=6 | takeover_phut=30 | ttl_ngay=90
thieu_muc: HOI truoc khi chay vong lap - CAM doan
tien_kiem: PHA0_GATE_v1 (references/QUY_TRINH_RA_SOAT_3_TANG.md - PHA 0)
-->

**Tiền kiểm khi nhận việc:** chạy `PHA0_GATE_v1` (`references/QUY_TRINH_RA_SOAT_3_TANG.md`, PHA 0) NGAY tại
kickoff, trước khi hứa gì. Hỏng loại **chặn đứng** ⇒ báo người 1 dòng tại chỗ, **chưa tiêu call truy vấn NLM
nào**; **chặn làn ghi** ⇒ nhận việc nhưng khai rõ Loop B đứng (chỉ rà được trên cái đã có trong corpus);
**có fallback** ⇒ nhận việc, chạy chế độ suy giảm và ghi vào note bàn giao.

## §2. LOOP A — RÀ (mỗi phiên chạy MỘT lượt drain)

| Bước | Việc | Lệnh/cơ chế CÓ THẬT |
|---|---|---|
| **A1** | Pha 0 tiền kiểm — chạy ĐỦ `PHA0_GATE_v1` b1–b6 (`references/QUY_TRINH_RA_SOAT_3_TANG.md`): b1 `doctor` · b2 `ping`/contract · b3 `precheck` · b4 `profile-doctor` · b5 auth · b6 canary. **Không tin mô hình tuổi cookie** — lượt nào cần NLM thì canary probe LIVE trước (van F7 r208d đã chuyển sang verdict LIVE). Chặn đứng ⇒ dừng SỚM khi chưa tiêu call truy vấn NLM nào | `tl doctor --json` · `tl ping --json` · `tl precheck --json` · `tl profile-doctor --json` · `tl nlm-auth-status --json` (schema v2, đọc `rotation_token_expired`) · `registry_orchestrator boot` |
| **A2** | Nhận vai: ghi `session_claim` (id + giờ + `progress_ptr`) vào state. Claim cũ quá hạn **30′** mà `progress_ptr` KHÔNG nhích → chiếm quyền; còn nhích → phiên sau LÙI | RMW qua GAS |
| **A3** | Lấy đơn vị `pending` ưu tiên cao nhất: SÂU trước, và **ưu tiên NLM-ready** (nguồn đã `added` trong Q-NLM). Nguồn còn `pending` NLM → chỉ lấy khi hết việc khác, phát hiện tự mang `muc_chac_chan="cho_verify_nlm"` | `scripts/rasoat_worksheet.py` (chấm SÂU/ĐỐI CHIẾU/—) |
| **A4** | Rà 3 tầng: T1 cache tất định → T2 quét thô → T3 đào sâu; mở rộng frontier | `tl extract --dieu N` · `tl tra_cuu --cite --exact` · `tl nlm-query`/`nlm-cross` scoped · `tl frontier-expand --json` |
| **A5** | VERIFY từng phát hiện — **nguyên văn CHỈ từ cache/raw**; fail verify ⇒ KHÔNG ghi | `nlm_qa verify` (đường `tl`); chế độ không-NLM → §4b |
| **A6** | Ghi `master/<unit>.json` (kèm `anchor` + `muc_chac_chan`) → đánh `done` → **cập nhật state NGAY** (không dồn cuối phiên) | ghi NGOÀI cây skill (§7) |
| **A7** | Ứng viên mới → Q-INGEST (§3); Điều liên quan mới → Q-UNITS; văn bản mới flip corpus → sinh đơn vị `doi_chieu_bo_sung` (§3.6) | phân loại theo phạm vi kickoff |
| **A8** | **Đóng gói chủ động** (§8) → note bàn giao → NHẢ claim → thoát êm | state là file nên "thoát" = không làm gì thêm |

**HỘI TỤ (điều kiện dừng chu kỳ, dùng đúng từ vựng `rasoat-loop`):** hết `pending` ∧ Q-INGEST rỗng ∧
`dry_rounds ≥ 2` (2 vòng liên tiếp không sinh việc mới). Fail-safe: `max_iter`. Không tiến mà chưa hội tụ
⇒ **PAUSE** + báo người 1 dòng, KHÔNG lặp mù.

```bash
tl --profile "<hồ sơ>" rasoat-loop --dry-rounds 2 --json     # lớp phát hiện, report-only
tl --profile "<hồ sơ>" frontier-expand --json                # missing_in_corpus = hàng đợi nạp
```

## §3. LOOP B — NẠP GIỮA CHỪNG (đơn vị tối ưu là **LÔ**, không phải file)

**B0. Dò trùng trên dữ liệu TƯƠI (bắt buộc):** `tl reg-query --refresh …` trước khi lập kế hoạch lô —
dò trùng bằng cache nguội đã từng nạp chồng 9 tài liệu (24-07).

**B1. Chuẩn bị TRƯỚC, duyệt SAU:** mỗi ứng viên chạy DRY → `plan_hash` → Q-APPROVALS; văn bản vào trạng
thái **staged `corpus=false`**. Mọi việc nặng (tải, bóc tách, cache, dry-run) làm XONG trước khi hỏi người.

```bash
tl --profile "<hồ sơ>" reg-query --refresh --sohieu <số hiệu>        # B0: dò trùng trên dữ liệu TƯƠI
tl --profile "<hồ sơ>" profile-ingest --staged <file> --json         # DRY → plan_hash (corpus=false)
tl --profile "<hồ sơ>" verify-staged --json                          # DRY báo cáo trước khi flip cả lô
```

**B2. Nguồn tải — bậc thang:** official tự tải → gated qua Chrome đã đăng nhập (`tl tvpl-url`, TUẦN TỰ;
**không bao giờ nhập mật khẩu hộ**; CAPTCHA/login hết hạn ⇒ dừng kênh, tụt bậc) → LuatVietnam → `vbpl.vn`
→ Công báo PDF (hạ sách cuối, kiểm chất lượng text). Không tự lấy được ⇒ `cho_nguoi_tai`, gom hỏi tại ②.

**B3. Điểm chạm ② (1 lần/pha):** người duyệt CẢ LÔ trên một bảng; máy chạy chuỗi
`--apply --confirm yes --expected-plan-hash <hash>` (lệch plan = tự chặn).

**B4. Cổng máy đóng lô:** `tl verify-staged` DRY → `--apply --confirm yes` flip `corpus=true` cả lô
(1 `reg_bulk` journaled, undo được cả lô); FAIL ở lại staged kèm cờ.

**B5. Tách kênh:** cache xong = **đơn vị RÀ ĐƯỢC NGAY**. Nạp NLM đi riêng: nguồn flip xong → Q-NLM,
**worker tuần tự** drain tới hết (`tl nlm-add` / `ingest-missing`), cuối lô MỘT lần
`tl nlm-reconcile <nb> --all-notebooks`; sau lô chạy `tl backfill-title-vn` cho dòng MỚI.
⚠ PDF: `nlm-add --drive-id` HỎNG với PDF → đi đường tải file + `source_add source_type=file`; hỏng nữa ⇒
đánh `failed` + ghi làn lỗi, KHÔNG retry vô hạn.

**B6. Đơn vị `doi_chieu_bo_sung`:** văn bản mới D flip corpus ⇒ `tl relation-check` 2 CHIỀU: đơn vị `done`
nào dẫn chiếu tới/bị D dẫn chiếu → sinh đơn vị cặp (đơn-vị-cũ × D), **chỉ so phần giao**.
**Bất biến:** đơn vị `done` KHÔNG BAO GIỜ reset về `pending` toàn phần trừ khi anchor vỡ.

## §4. LOOP C — TÁI RÀ ĐỊNH KỲ (tuần 1 lần, phiên mới, context sạch)

`changes_pull` delta → `vb_status`/`relation-check`/`vbhn-check` → so `anchor.doc_deps.text_hash`:
hash đổi / bị supersede / TTL 90 ngày cạn (chỉ mức `can_kiem_tra`) ⇒ đánh STALE, re-queue **diff-aware**
(chỉ Điều đổi). Không delta ⇒ **thoát im lặng**. Wrapper chạy nền KHÔNG được hỏi người
(`disallowed-tools: AskUserQuestion`).

**§4b. Chế độ CHẠY-KHÔNG-NLM (cookie chết là chuyện chắc chắn xảy ra):** T2 chuyển quét cache/Drive trực
tiếp; phát hiện vẫn ghi nhưng `muc_chac_chan="cho_verify_nlm"` + vào **Q-VERIFY**; cookie sống lại → MỘT
lượt trả nợ kiểm chéo tuần tự, đạt thì nâng hạng. Sửa auth: **CHỈ `nlm login` thay phiên mới** — CẤM tự
`nlm-auth-load` (ghi đè jar bằng bản cũ/cũng chết); không tin `nlm login --check` (FALSE-GREEN), chốt
duy nhất là probe LIVE. **Vòng RÀ không bao giờ dừng vì cookie.**

## §5. LÀN LỖI — degrade-and-continue

> Đặc tả đầy đủ (4 bước, phân hạng, khuôn sổ `BUG_LEDGER_v1`, luật sửa nóng):
> `references/QUY_TRINH_RA_SOAT_3_TANG.md` — mục LÀN LỖI. Dưới đây là bản vận hành cho vòng lặp.

1. Lỗi lệnh → fallback CÓ SẴN (`--method auto`; cookie chết → chế độ không-NLM/`tl nlm-links`; GAS cache
   600s → `--refresh`). Đi vòng được ⇒ hạng **`workaround`**, đơn vị vẫn chạy tới `done`.
2. Vẫn bí ⇒ hạng **`blocker`**: ghi Q-BUGS (sổ `rasoat_bugs.md`, **đủ 8 trường** — `ma` · `thoi_diem` ·
   `version_do_duoc` · `lenh_tai_hien` · `hau_qua` · `phan_loai` · `duong_vong` · `don_vi`; thiếu trường =
   coi như chưa ghi sổ) → đơn vị đánh `blocked` (KHÔNG giả `done`) → lấy đơn vị kế tiếp. **PLAN vẫn tiến.**
3. Dừng toàn cục CHỈ khi mọi đơn vị còn lại blocked bởi CÙNG một `ma` → báo người đúng 1 dòng + checkpoint.
   Một `blocker` lẻ KHÔNG BAO GIỜ được đọc thành lý do dừng.
4. Sửa nóng: **CHỈ khi chặn đứng toàn cục**, và vẫn KHÔNG vá tại LIVE (deploy là bước tay ⇒ vá tại chỗ bị đè
   ở lần deploy sau). Fix ở canonical theo quy trình (ruff → selftest N/N + test `rXX_` → CHANGELOG → bump),
   lỗi lẻ thì **gom vá sau lượt rà**; đợt sau Loop C thấy `skill_version` mới sẽ tự re-queue đơn vị blocked.

## §6. AGENT RÀ ĐƠN VỊ `tl-rasoat` — PROMPT MẪU (dán khi spawn; LIVE không có file agent riêng)

> Dev-side có wrapper ép cứng bằng frontmatter (`.claude/agents/tl-rasoat.md`: `tools` không có Write/Edit,
> `disallowedTools`, `maxTurns`). Ở LIVE, ranh giới chỉ còn prompt ⇒ phiên chính PHẢI hậu kiểm
> `tl verify-integrity` + `git status` sau mỗi lượt spawn (bài học rogue-edit).

```text
Bạn là agent RÀ MỘT ĐƠN VỊ cho hồ sơ <ho_so_id>, profile <P>. READ-ONLY tuyệt đối.

RANH GIỚI CỨNG (vi phạm = hỏng việc):
- KHÔNG ghi/sửa/xoá bất kỳ file nào; không lách qua Bash (`>`, `tee`, `sed -i`).
- CẤM mọi lệnh: --apply · --confirm · register · recat · source-* · reg-delete · ingest* · drive-push · clasp.
- Nguyên văn điều luật CHỈ lấy từ cache/raw đã verify; TUYỆT ĐỐI không lấy từ RAG/NLM.
- Ngân sách NLM của bạn: <N> call. Hết ngân sách → dừng, trả phần đã có.

VIỆC: đơn vị <unit_id> = <văn bản> Điều <…>. Chạy T1 (cache tất định) → T2 (quét thô, NLM scoped)
→ T3 (đào sâu) → VERIFY từng phát hiện. NLM chết → chuyển quét cache trực tiếp và đánh dấu (xem dưới).

TRẢ VỀ (final message = JSON THUẦN, không văn xuôi, không bọc ```):
{"unit_id": "...", "trang_thai": "done|blocked", "ly_do_blocked": "",
 "nlm_calls_da_dung": 0,
 "phat_hien": [{"key":"","linh_vuc":"","van_ban":"","can_cu":"","phan_tich":"",
   "hinh_thuc":"","lo_trinh":"","tieu_chi":"","ghi_chu":"",
   "muc_chac_chan":"chac_chan|can_kiem_tra|cho_verify_nlm",
   "anchor":{"doc_deps":[{"so_hieu":"","text_hash":"","dieu":[]}],"cite":"","skill_version":"",
             "verified_at":"","ttl_ngay":90}}],
 "ung_vien_nap": [{"so_hieu":"","ly_do":""}], "dieu_lien_quan_moi": []}

QUY TẮC ĐIỀN:
- `hinh_thuc` CHỈ dùng giá trị trong `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` (`_vocab_hinh_thuc`) —
  sai chính tả/không dấu sẽ rơi ÂM THẦM vào phụ lục 04.
- `so_hieu` PHẢI có NĂM (chuẩn `NN-YYYY-VBHN-XXX`).
- Phát hiện chưa qua kiểm chéo NLM ⇒ `muc_chac_chan="cho_verify_nlm"` (phiên chính sẽ xếp vào Q-VERIFY).
- Không chắc ⇒ nói KHÔNG CÓ / để `can_kiem_tra`; cấm bịa số hiệu, ngày, nội dung.
```

Phiên chính nhận JSON → validate schema → ghi `master/<unit>.json` → cập nhật state. JSON sai schema:
KHÔNG ghi, đánh `blocked` + ghi Q-BUGS.

## §7. ĐƯỜNG GHI LÚC CHẠY (bất biến §B.5: state biến động NGOÀI cây skill)

Cây skill được hash toàn bộ vào `package_hash`; mọi file đổi theo lượt rà mà nằm trong cây sẽ làm
`release-verify`/golden ĐỎ. Đường ghi hợp lệ — máy đọc được, guard `r210_loop_khong_ghi_trong_cay` khoá:

<!-- WRITE_PATHS_v1
_meta/rasoat_state.json
<out-dir>/master/<unit>.json
<out-dir>/rasoat_approvals.json
<out-dir>/rasoat_bugs.md
-->

`_meta/…` = trên Drive trong profile hồ sơ (bền, sống qua kill/sandbox). `<out-dir>` = thư mục local
NGOÀI cây skill (`--out-dir`), đẩy Drive theo lô ở checkpoint; Claude chat đẩy sau MỖI đơn vị vì sandbox
xoá trắng mỗi phiên. Chỉ **MẪU rỗng** (`templates/`) được nằm trong cây và vào zip.

## §8. ĐÓNG GÓI & BÀN GIAO (A8)

Đo tại **RANH GIỚI ĐƠN VỊ**, không bao giờ giữa chừng: **40% context = ngưỡng mềm** (không nhận đơn vị SÂU
mới, viết dần note bàn giao) · **60% = ngưỡng cứng** (đóng gói ngay sau đơn vị hiện tại). Claude chat không
có số đo tin cậy → dùng ngưỡng ĐẾM `max_units_per_session` = 6. Chạm auto-compact (~95%) = **SỰ CỐ quy
trình**. **KHÔNG `/compact` giữa phiên rà** — bàn giao qua file trung thực hơn tóm tắt có mất mát.

Nghi thức: xong/trả đơn vị đang cầm → đẩy sổ → cập nhật state + note bàn giao → NHẢ claim → kết sổ registry
(`tl manifest`; `tl ops-plan` đổ việc vệ sinh vào Q-APPROVALS chờ duyệt, KHÔNG tự `--apply`).

## §9. NHỊP REGISTRY (cấm chen ngang)

BOOT `changes_pull` (nền, cùng warm-up) · **trong vòng rà: registry CHỈ ĐỌC, đọc OFFLINE** (`reg-query` trên
manifest cache; `--live` chỉ readback hẹp sau khi ghi) · cuối lô: `nlm-reconcile` 1 lần + `backfill-title-vn`
· kết phiên/Loop C: `tl manifest`, `hygiene scan`/`sweep`/`tl loop`. `regen2` là lệnh ĐẮT — chỉ chạy qua
orchestrator (ngưỡng/`--touched-drive`), không chạy tay giữa hồ sơ.
