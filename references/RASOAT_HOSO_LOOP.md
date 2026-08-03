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
| **A2** | Nhận vai: `state-get` đọc state từ Drive → **HOÀ GIẢI đơn vị `doing`** (r213, khe hở H8 đo 26-07: phiên trước chết SAU khi ghi master nhưng TRƯỚC khi ghi state — `doing` mà ĐÃ có `master/<unit>.json` ⇒ `done`, không có ⇒ `pending`; `done` KHÔNG BAO GIỜ bị hạ) → ghi `session_claim` (id + giờ + `progress_ptr`) → `state-put`. Claim cũ quá hạn **30′** mà `progress_ptr` KHÔNG nhích → chiếm quyền; còn nhích → phiên sau LÙI | `tl state-get --json` · `tl rasoat-merge --state …` (hoà giải) · `tl state-put --in … --expect-claim <id cũ>` |
| **A3** | Lấy đơn vị `pending` ưu tiên cao nhất: SÂU trước, và **ưu tiên NLM-ready** (nguồn đã `added` trong Q-NLM). Nguồn còn `pending` NLM → chỉ lấy khi hết việc khác, phát hiện tự mang `muc_chac_chan="cho_verify_nlm"` | `scripts/rasoat_worksheet.py` (chấm SÂU/ĐỐI CHIẾU/—) |
| **A4** | Rà 3 tầng: T1 cache tất định → T2 quét thô → T3 đào sâu; mở rộng frontier | `tl extract --dieu N` · `tl tra_cuu --cite --exact` · `tl nlm-query`/`nlm-cross` scoped · `tl frontier-expand --json` |
| **A5** | VERIFY từng phát hiện — **nguyên văn CHỈ từ cache/raw**; fail verify ⇒ KHÔNG ghi | `tl nlm-query --source-id <sid> --strict-scope`; chế độ không-NLM → §4b |
| **A6** | Ghi `master/<unit>.json` (kèm `anchor` + `muc_chac_chan`) → đánh `done` → **cập nhật state NGAY** (không dồn cuối phiên) | ghi NGOÀI cây skill (§7); `tl state-put --in <out-dir>/rasoat_state.json` |
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

> **Mâu thuẫn doctrine đã chốt (r213 — đo 26-07).** Chuỗi khắc phục của `nlm-auth-status` xếp
> `tl nlm-auth-load` ở vị trí **(1)**, ngược hẳn điều cấm ngay trên. Cả hai đều đúng, khác NGỮ CẢNH:
> vị trí (1) là đường **bootstrap Cowork/headless** — ở đó máy chưa có jar nào và `nlm-auth-load` là
> đường duy nhất chạy được không cần browser. Trong **lượt rà** thì ngược lại: jar đang sống hoặc vừa
> chết, nạp bundle đè lên là quay vòng vô ích. ⇒ **Không đảo thứ tự** (đảo là phá đường bootstrap,
> nghiệm thu r208b) và **không nới điều cấm** (nới là mở lại vòng lặp r208c đã đóng); thay vào đó mọi
> thông báo auth nay mang sẵn **câu trừ** trỏ về §4b, vì agent đọc thông báo lỗi thường không đọc
> doctrine. Chốt chặn hạ cấp `_nlm_auth_load_downgrade` (r208c) vẫn giữ — nó chặn bản CŨ hơn nhưng
> KHÔNG chặn được bản mới-hơn-mà-cũng-chết, nên câu trừ là lớp phòng thủ còn thiếu.

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
   "anchor":{"doc_deps":[{"so_hieu":"","text_hash":"sha256:<64hex>","locator":"","dieu":[]}],"cite":"","skill_version":"",
             "verified_at":"","ttl_ngay":90}}],
 "ung_vien_nap": [{"so_hieu":"","ly_do":""}], "dieu_lien_quan_moi": []}

QUY TẮC ĐIỀN:
- `hinh_thuc` CHỈ dùng giá trị trong `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` (`_vocab_hinh_thuc`) —
  từ v1.36.45 (r311) sai chính tả/không dấu/để trống làm `rasoat_phuluc.py` DỪNG (fail-closed, nêu đích
  danh dòng sai) chứ không còn rơi âm thầm vào phụ lục 04.
- `so_hieu` PHẢI có NĂM (chuẩn `NN-YYYY-VBHN-XXX`).
- Phát hiện chưa qua kiểm chéo NLM ⇒ `muc_chac_chan="cho_verify_nlm"` (phiên chính sẽ xếp vào Q-VERIFY).
- Không chắc ⇒ nói KHÔNG CÓ / để `can_kiem_tra`; cấm bịa số hiệu, ngày, nội dung.
```

Phiên chính nhận JSON → validate schema → ghi `master/<unit>.json` → cập nhật state. JSON sai schema:
KHÔNG ghi, đánh `blocked` + ghi Q-BUGS.

### §6b. PHA 4 — DỒN N PHIẾU ĐƠN VỊ → BẢNG MASTER → PHỤ LỤC

Khuôn `master/<unit>.json` (trên) và khuôn bảng master (`templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json`)
khớp ở tầng **item** nhưng lệch ở tầng **container**: §6 để `van_ban` là CHUỖI số hiệu và phát hiện dưới
`phat_hien`; bảng cần `van_ban` là DANH SÁCH metadata (cho Phụ lục 03) và `noi_dung` phẳng. Bước "dồn"
này Đợt 1–3 chỉ tả bằng lời nên **không ai cài — PHA 4 sập thật ngày 26-07**. Từ r213 nó là lệnh:

```bash
tl rasoat-merge --in <out-dir>/master --out <out-dir>/BANG_MASTER.json \
                --state <out-dir>/rasoat_state.json --json      # --state = kèm hoà giải đơn vị doing
python scripts/rasoat_phuluc.py --in <out-dir>/BANG_MASTER.json --out-dir <out-dir>/phuluc
```

`rasoat_phuluc.py` nay **tự nhận khuôn §6** (dùng chung đúng hàm quy đổi), nên `--in <out-dir>/master`
cũng chạy thẳng. Khuôn KHÔNG nhận ra ⇒ **rc≠0 nói rõ file nào**, không nuốt im lặng (bản cũ gặp
`van_ban` là chuỗi thì `+=` trải CHUỖI thành TỪNG KÝ TỰ rồi mới chết sai chỗ).

**KHÔNG BỊA metadata:** đơn vị rà chỉ biết số hiệu + tên; `ngay`/`hieu_luc_tu`/`tinh_trang` nằm ở
registry chứ không nằm trong phiếu rà ⇒ để **RỖNG** và nổi lên `_thieu_o_metadata` để người điền. Đơn
vị nào muốn đủ ô thì mang sẵn `van_ban_meta` (dict, tuỳ chọn) trong `master/<unit>.json`.

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

**LỆNH GHI/ĐỌC STATE (r213 — trước đó doc bắt state ở Drive mà KHÔNG lệnh nào ghi được; lượt rà 26-07
phải giữ state local, không sống nổi ca §7 sandbox xoá trắng):**

```bash
tl --profile "<hồ sơ>" state-get --out <out-dir>/rasoat_state.json --json    # rc=3 = chưa có (lượt đầu)
tl --profile "<hồ sơ>" state-put --in <out-dir>/rasoat_state.json --expect-claim <id> --json
```

`state-put` **KHÔNG có `--confirm`** — và đó là chủ đích: mượn cổng duyệt (`profile-file-add --apply`)
là bắt người xen MỖI lần chốt state, phá nghiệm thu ≤2 lần xen của H7. Đổi lại nó bị khoá bằng ba chốt
máy: (1) danh sách tên ĐÓNG chỉ `rasoat_state.json`, fail-CLOSED với mọi tên khác
hoặc có đường dẫn; (2) folder đích BẮT BUỘC là `_meta/` (`--folder-id`/`TL_META_FOLDER_ID`, không có
mặc định root); (3) `--expect-claim` từ chối ghi khi `session_claim.id` trên Drive đã khác (single-writer
§9). File ghi lên `register="false" share="false"` ⇒ KHÔNG vào registry, KHÔNG mở link công khai.
Thứ tự an toàn: tạo bản MỚI trước, dọn bản cũ sau — chết giữa chừng thì `state-get` vẫn lấy bản mới nhất.

`metaFolderId` rỗng trong config? Đọc marker KHÔNG cần `--apply`: `tl --profile <P> profile-sync --json`
→ `rows[].diffs[].marker`.

## §8. ĐÓNG GÓI & BÀN GIAO (A8)

Đo tại **RANH GIỚI ĐƠN VỊ**, không bao giờ giữa chừng: **40% context = ngưỡng mềm** (không nhận đơn vị SÂU
mới, viết dần note bàn giao) · **60% = ngưỡng cứng** (đóng gói ngay sau đơn vị hiện tại). Claude chat không
có số đo tin cậy → dùng ngưỡng ĐẾM `max_units_per_session` = 6. Chạm auto-compact (~95%) = **SỰ CỐ quy
trình**. **KHÔNG `/compact` giữa phiên rà** — bàn giao qua file trung thực hơn tóm tắt có mất mát.

Nghi thức: xong/trả đơn vị đang cầm → đẩy sổ → cập nhật state + note bàn giao → NHẢ claim → kết sổ registry
(`tl manifest`; `tl ops-plan` đổ việc vệ sinh vào Q-APPROVALS chờ duyệt, KHÔNG tự `--apply`).

**§8b. ĐÓNG HỒ SƠ (khác đóng gói phiên) — r300.** Đóng gói = kết thúc MỘT LƯỢT; đóng hồ sơ = kết thúc CẢ
HỒ SƠ. Đặc tả đầy đủ: `references/RASOAT_PLAN_SCHEMA.md` §7 (khối `vong_doi` + 6 điều kiện đóng + 6 điều
kiện mở hồ sơ kế tiếp). Ba điều dễ sai nhất:

- **"Đóng" phải nằm TRONG FILE.** Đo 01-08 trên hồ sơ thật: người thẩm tra chốt đã đóng mà state không có
  khoá nào nói thế, còn treo 5 đầu mối (claim chưa nhả · 1 `cho_duyet` · nợ kiểm chéo · văn bản chưa lấy
  được · trạng thái văn xuôi). Thiếu vế nào ⇒ **`da_dong_co_gioi_han`** + khai vào `gioi_han_da_biet`;
  **cấm đóng im lặng**.
- **Đóng là ĐÓNG BĂNG, không phải dọn** — không xoá `master/`, `rasoat_bugs.md`, `rasoat_approvals.json`,
  `BIEN_BAN_*`.
- **Loop C chỉ chạy khi `vong_doi.anchor_con_hieu_luc: true`.** `false` ⇒ BỎ QUA hồ sơ và **nói ra lý do**;
  chạy bừa trên anchor chưa di trú sẽ ra STALE giả 100% (§4 cảnh báo cùng chuyện).

Mở hồ sơ kế tiếp: **`--out-dir` MỚI** (dùng lại thư mục cũ = bảng master phồng — `rasoat_phuluc.py --in`
gộp CẢ thư mục), claim cũ đã nhả, kickoff khai lại quota, ghi `skill_version_toi_thieu`.

## §9bis. QUY ƯỚC GHI (r218)

**Một bài học — một lượt ghi.** Không gộp nhiều phát hiện vào một lần ghi tài liệu: cách đánh số lúc nháp
("phát hiện 3", "mục trên", "bảng dưới") rò rỉ vào bản đã ghi và biến thành **trích dẫn chết** — người đọc
sau đi theo con trỏ và lạc. Ghi xong MỘT mục, neo lại vào cây, rồi mới sang mục sau.

Cùng họ với bẫy đã mắc lượt 7 (để bản sao lưu **trong** `master/` ⇒ `rasoat-merge` nuốt, 40→53 phát hiện):
**mọi `*.bak.*.json` để Ở GỐC out-dir, KHÔNG để trong `master/`.**

Kiểm được bằng máy: `tl doc-claims-check --strict` bắt con trỏ chết dạng đường dẫn/link/`file.py:dòng`/
version/số hiệu đợt. Nó KHÔNG bắt được "mục trên" — nên vế đó vẫn là kỷ luật lúc ghi.

## §9. NHỊP REGISTRY (cấm chen ngang)

BOOT `changes_pull` (nền, cùng warm-up) · **trong vòng rà: registry CHỈ ĐỌC, đọc OFFLINE** (`reg-query` trên
manifest cache; `--live` chỉ readback hẹp sau khi ghi) · cuối lô: `nlm-reconcile` 1 lần + `backfill-title-vn`
· kết phiên/Loop C: `tl manifest`, `hygiene scan`/`sweep`/`tl loop`. `regen2` là lệnh ĐẮT — chỉ chạy qua
orchestrator (ngưỡng/`--touched-drive`), không chạy tay giữa hồ sơ.
