# WORKFLOW RÀ SOÁT TỰ ĐỘNG HOÁ CAO — "NHÀ MÁY RÀ SOÁT" (đề xuất, chưa triển khai)

> Trạng thái: ĐỀ XUẤT thiết kế (docs-only). Bổ sung cho `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md`
> (kiến trúc + hiện trạng + hạng mục); tài liệu này mô tả **workflow vận hành** — dòng chảy, hàng đợi,
> sự kiện, và cách đạt tự động hoá cao nhất trong khuôn khổ 3 điểm dừng có chủ đích.
> Yêu cầu gốc (2026-07-25): tự động hoá cao nhất; **giữa chừng nạp thêm nguồn**; **sửa lỗi phát hiện được**;
> **định kỳ rà lại kết quả cũ**.
> ✅ **Đối chiếu kho `claude-code-best-practice` ĐÃ LÀM 25-07 trên máy dev** (bản Jul 25 2026 / Claude Code
> v2.1.220, đã pull): **KHÔNG có nguyên lý P1–P7 nào bị kho khuyên ngược.** Ba bổ sung rút từ kho (đã nhập
> vào thân tài liệu, nguồn ghi tại chỗ): **A1** — agent read-only ép cứng bằng frontmatter (`claude-subagents.md`),
> xem KE_HOACH C4; **A2** — wrapper Loop C khai `disallowed-tools: AskUserQuestion` + `disable-model-invocation`
> (`claude-skills.md`), xem §5; **A3** — headless local thêm `--max-turns`/`--max-budget-usd`, chỉ có ở print
> mode (`claude-cli-startup-flags.md`), xem §5.
> **CHỐT 25-07 (grill):** nơi lưu state = LAI (§3) · Loop B thêm B0/uỷ-quyền-nguồn-tải/tách-kênh/chuẩn-bị-trước
> (§4) · worker Q-NLM tuần tự (§4a) · phòng thủ NLM 3 tầng + Q-VERIFY (§4b) · đơn vị "đối chiếu bổ sung" (§4 B.4)
> · ma trận môi trường local/Cowork/Claude-chat (§5b).

---

## §1. NGUYÊN LÝ TỰ ĐỘNG HOÁ (rút từ pattern đã kiểm chứng trong repo + best practice Claude Code)

| # | Nguyên lý | Nguồn gốc trong repo |
|---|---|---|
| P1 | **State là file, không phải context.** Mọi hàng đợi/tiến độ/phát hiện nằm trong file máy-đọc-được; phiên (và context) là VAI TRÒ dùng lại được, kill lúc nào cũng resume | journal/WAL + `--resume`; bài học kế nhiệm phiên |
| P2 | **Điểm chạm người tỷ lệ O(số pha), KHÔNG O(số file).** Không xin duyệt từng lệnh — gom mọi việc cần duyệt thành LÔ tại ranh giới pha; 1 lô = 1 lệnh `--apply` = 1 câu hỏi hook | staged lane r200: nạp `corpus=false` hàng loạt, `verify-staged --apply` flip CẢ LÔ 1 lần, undo cả lô |
| P3 | **Mọi bước tự động phải có cổng máy đứng sau** (dry-run → apply plan-hash → verify/readback), tự động ≠ bỏ cổng | doctrine DETERMINISTIC WORKFLOW GATES trong SKILL.md |
| P4 | **Degrade-and-continue:** gặp lỗi → thử đường fallback có sẵn → không được thì ghi sổ + đánh dấu đơn vị BLOCKED → đi tiếp việc khác; chỉ dừng toàn cục khi không còn việc nào làm được | `--method auto` fallback chuỗi; `BATCH_LINKS` khi cookie chết; PAUSE của `tl loop` |
| P5 | **Phát hiện phải mang NEO PHỤ THUỘC** (nó đúng dựa trên bản nào của văn bản nào) — đây là điều kiện để "rà lại định kỳ" thành phép TÍNH thay vì làm lại từ đầu | ADR-0011 (source revision tách content identity); registry `superseded_by` |
| P6 | **Wake định kỳ im lặng khi không có việc.** Lịch chạy lại không được thành spam; chỉ nổi lên khi có delta thật | pattern Routine/cron; `changes_pull` delta rẻ |
| P7 | **Hồ sơ = PROFILE.** Không phát minh khái niệm "hồ sơ" mới: mỗi hồ sơ dự thảo là 1 profile (folder + registry + notebook + marker `_meta/` riêng) → thừa hưởng single-writer LockService+RMW và độ bền Drive | ADR-0003 (marker là nguồn sự thật), v1.30.0 baseAlso |
| P8 | **(chốt 25-07) Một đường nạp — HAI chế độ điều phối.** Nạp ad-hoc (ngoài rà soát) và nạp trong rà soát dùng CHUNG lõi máy: QT-2 → dry-plan + `plan_hash` → staged → verify-staged → cache; khác nhau CHỈ ở tầng duyệt: người-có-mặt duyệt ngay từng yêu cầu vs kickoff uỷ quyền + gom lô tại điểm chạm ②. Hai nâng cấp áp cho CẢ HAI chế độ: **B0 dò-trùng-tươi** (sự cố nạp chồng 9 tài liệu 24-07 xảy ra ở đường nạp THƯỜNG) và **tách kênh NLM** (văn bản dùng được từ cache ngay, NLM làm giàu sau — kể cả ad-hoc không bắt người ngồi chờ ~86s/lô) | làn staged r200; cổng tiền-nạp QT-2/WEB (SKILL.md:183–184); bài học 24-07 |

---

## §2. SƠ ĐỒ TỔNG — 3 VÒNG LẶP + 1 LÀN LỖI, quay quanh 4 HÀNG ĐỢI

```
                       NGƯỜI ①: kickoff contract (phạm vi hồ sơ + uỷ quyền + ngân sách)
                                             │
                                    PHA 0 TIỀN KIỂM (mỗi lần thức dậy)
                                doctor · precheck · tuổi cookie NLM · VERSION
                                   fail có fallback → ghi Q-BUGS, đi tiếp
                                   fail chặn đứng  → DỪNG SỚM, báo 1 dòng
                                             │
   ┌─────────────────────────────────────────┼──────────────────────────────────────────┐
   │                                         ▼                                          │
   │   Q-UNITS (đơn vị rà)      ◄─── LOOP A: RÀ (mỗi phiên drain) ───►  master/<unit>.json
   │   pending/doing/done/                T1 phân tầng (cache, 0 NLM)        (append-only,
   │   blocked/stale                      T2 quét thô (NLM scoped)            mỗi dòng có
   │        ▲    ▲                        T3 đào sâu + Claude so cache        NEO PHỤ THUỘC)
   │        │    │                        VERIFY (nlm_qa + cache cite)             │
   │        │    │                             │                                   │
   │        │    │            phát hiện văn bản mới (frontier-expand)              │
   │        │    │                             ▼                                   │
   │        │    └──── LOOP B: NẠP ◄── Q-INGEST (missing_in_corpus)                │
   │        │          dry-run plan → nạp STAGED (corpus=false, tự động)           │
   │        │          → gom lô → NGƯỜI ② duyệt LÔ (1 câu hỏi hook/pha)            │
   │        │          → verify-staged flip cả lô → cache → sinh đơn vị mới ───────┤
   │        │                                                                      │
   │        └───────── LOOP C: TÁI RÀ (định kỳ, Routine) ◄─────────────────────────┘
   │                   changes_pull + vb_status + vbhn-check các doc hồ sơ
   │                   delta? → đánh STALE các phát hiện có neo trúng delta
   │                   → re-queue DIFF-AWARE (chỉ Điều đổi) vào Q-UNITS
   │
   │   Q-BUGS (làn lỗi, chạy xuyên suốt): lỗi → workaround/fallback → ghi sổ →
   │   đơn vị BLOCKED nếu bí → gom về cuối; KHÔNG dừng vòng
   │
   └── ĐK DỪNG chu kỳ: Q-UNITS hết pending ∧ Q-INGEST rỗng ∧ dry_rounds ≥ K ──► PHA 4 tổng hợp
                                             │
                       NGƯỜI ③: nghiệm thu (Phiếu A–G + lô --apply còn chờ + Q-BUGS) + KÝ
```

**Điểm chạm người trong một chu kỳ: đúng 3 loại** — ① giao việc, ② duyệt lô nạp (mỗi pha 1 lần, không
phải mỗi file), ③ nghiệm thu + ký. Giữa chúng máy tự chạy, kể cả qua nhiều phiên/kill.

---

## §3. STATE — hàng đợi + sổ phát hiện (tất cả là FILE — P1+P7; nơi lưu **LAI, chốt 25-07**)

State sống-còn trên Drive `_meta/` của profile; sổ nặng ở local `--out-dir`, đẩy Drive theo lô (§B.5 KE_HOACH).

| File | Nơi lưu | Vai trò | Ghi chú |
|---|---|---|---|
| `_meta/rasoat_state.json` | **Drive** | Q-UNITS + Q-INGEST + **Q-NLM** + con trỏ chu kỳ + `session_claim` + quota NLM còn lại + **quota TVPL** + note bàn giao | nguồn sự thật resume; Drive theo ADR-0003 — `~/.tra_luat_cache` không đủ bền (Claude chat xoá trắng sandbox mỗi phiên); RMW đã ATOMIC (GAS 2.21.2p). Gộp Q-INGEST/Q-NLM vào MỘT file = 1 lần RMW, 1 claim |
| — Q-INGEST (trong state) | Drive | ứng viên từ `frontier-expand` (`missing_in_corpus`) + user bổ sung, trạng thái dry-planned/staged/flipped | mục NGOÀI phạm vi kickoff contract → gắn `out_of_scope`, chờ người, không tự nạp |
| — Q-NLM (trong state) | Drive | nguồn chờ nạp NotebookLM: `pending/added/failed` — worker §4a drain tuần tự | nạp NLM là LÀM GIÀU về sau, không chặn rà (đơn vị rà được ngay khi cache xong) |
| `master/<unit>.json` (thư mục) | **local `--out-dir`**, đẩy Drive ở checkpoint/Pha 4 (chat: mỗi đơn vị/lô nhỏ) | sổ phát hiện — 1 file/đơn vị rà, schema `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` | append-only ở mức thư mục; `rasoat_phuluc.py --in master/` gộp khi tổng hợp; mỗi `noi_dung[]` mang `anchor` + `muc_chac_chan` (H1b) |
| `_meta/rasoat_bugs.md` | local, đẩy cùng checkpoint | Q-BUGS: lỗi skill gặp giữa chừng | mỗi mục: VERSION đo được + lệnh tái hiện + workaround đã dùng + phân loại workaround/blocker |
| `_meta/rasoat_approvals.json` | local, đẩy cùng checkpoint | Q-APPROVALS: các dry-plan (kèm `plan_hash`) đã gom, chờ duyệt lô | người duyệt đọc 1 bảng, chấp thuận → máy chạy chuỗi `--apply --confirm yes --expected-plan-hash` |
| — Q-VERIFY (trong state) | Drive | phát hiện ghi trong chế độ không-NLM (`muc_chac_chan="cho_verify_nlm"`) chờ trả nợ kiểm chéo `nlm_qa` | cookie sống lại → một lượt trả nợ tuần tự, đạt thì nâng hạng (§4b) |

**NEO PHỤ THUỘC của mỗi phát hiện** (điều kiện của Loop C — P5), thêm vào mỗi dòng `noi_dung[]`:

```json
"anchor": {
  "doc_deps": [{"so_hieu": "18-2025-VBHN-VPQH", "text_hash": "sha256:…", "dieu": ["54", "125"]}],
  "cite": "cache:18VBHN2025#dieu54",
  "skill_version": "1.35.38",
  "verified_at": "2026-07-25",
  "ttl_ngay": 90
}
```

Ý nghĩa: phát hiện này ĐÚNG chừng nào các `text_hash` kia còn là bản hiện hành. Đổi hash / có VBHN mới
/ TTL cạn (với mức "cần kiểm tra") ⇒ máy TỰ biết phát hiện nào cần rà lại — không cần người nhớ.

> `so_hieu` trong anchor PHẢI theo chuẩn bất biến `NN-YYYY-VBHN-XXX` (mọi số hiệu có NĂM). Kèm anchor, mỗi
> dòng `noi_dung[]` mang `muc_chac_chan` (`chac_chan | can_kiem_tra | cho_verify_nlm` — H1b KE_HOACH); TTL
> chỉ áp mức `can_kiem_tra`, còn `cho_verify_nlm` do Q-VERIFY xử lý (§4b).

---

## §4. BA VÒNG LẶP — mô tả từng bước, ánh xạ lệnh CÓ THẬT

### LOOP A — RÀ (mỗi phiên thức dậy chạy một lượt drain)

| Bước | Việc | Lệnh/cơ chế có thật | Tự động? |
|---|---|---|---|
| A1 | Pha 0 tiền kiểm: ping, cookie, VERSION khớp | `doctor`/`ping`, `nlm-auth-status`, probe 3 kênh NLM (KERNEL_APPENDIX §E) | ✅ — fail chặn đứng thì dừng sớm TRƯỚC khi tiêu NLM |
| A2 | Nhận vai: ghi `session_claim` (id phiên + giờ) vào state | RMW qua GAS (LockService làm lưới) | ✅ |
| A3 | Lấy đơn vị `pending` ưu tiên cao nhất (SÂU trước, theo phân tầng worksheet). **Ưu tiên NLM-ready (chốt 25-07):** lấy đơn vị có nguồn liên quan đã `added` trong Q-NLM trước; đơn vị mà nguồn còn `pending` NLM chỉ lấy khi KHÔNG còn việc khác — khi đó phát hiện tự mang `muc_chac_chan="cho_verify_nlm"` + vào Q-VERIFY (cơ chế §4b áp theo TỪNG NGUỒN). Không có "rà thiếu mà ghi là chắc chắn" | `rasoat_worksheet.py` đã chấm SÂU/ĐỐI CHIẾU/— | ✅ |
| A4 | T1→T2→T3 theo quy trình 3 tầng; mở rộng frontier | `tra_cuu --cite --exact`, `notebook_query` scoped, `frontier-expand --json` | ✅ (ngân sách NLM trừ dần trong state). **NLM chết → KHÔNG dừng**: T2 chuyển quét cache/Drive trực tiếp (chế độ không-NLM §4b) |
| A5 | VERIFY từng phát hiện | `nlm_qa verify`; nguyên văn CHỈ từ cache/raw | ✅ — phát hiện fail verify KHÔNG được ghi. Chế độ không-NLM: ghi với `muc_chac_chan="cho_verify_nlm"` + vào Q-VERIFY, trả nợ khi cookie sống (§4b) |
| A6 | Ghi `master/<unit>.json` (kèm anchor) + đánh `done` + cập nhật CSV nhật ký NLM | ghi file, ngoài cây skill | ✅ |
| A7 | Ứng viên mới từ A4 → append Q-INGEST; Điều liên quan mới → append Q-UNITS | máy phân loại theo phạm vi kickoff | ✅ |
| A8 | Cạn ngân sách/context → chốt checkpoint + note bàn giao → thoát êm | state đã là file nên "thoát" = không làm gì thêm | ✅ |

### LOOP B — NẠP GIỮA CHỪNG (chìa khoá: làn STAGED r200 — P2; **đơn vị tối ưu là LÔ, không phải file**)

Vấn đề gốc: nạp văn bản là đường GHI rủi ro cao (hook hỏi từng `--apply`) ⇒ nạp giữa chừng kiểu cũ
= chạm người O(số file). Làn staged đảo lại. Số đo ủng hộ lô: bulk-flip nhanh **×3,9** so với từng file;
NLM lô 8 nguồn wall 86,5s + reconcile 27,8s (khuôn lô r192). KHÔNG đưa việc gộp thêm GAS call vào kế
hoạch — r207 đã đo bỏ 1 call chỉ −0,6s (trong nhiễu), và nửa gộp `reg_get` CỐ Ý không làm (race đã trả giá).

0. **B0 — dò trùng trên dữ liệu TƯƠI (bắt buộc, bài học 24-07):** trước khi lập kế hoạch lô,
   `reg-query --refresh` — dò trùng bằng cache nguội đã từng nạp chồng 9 tài liệu vào ATVSLĐ.
1. **Tự động, không cần duyệt nội dung:** mỗi ứng viên trong Q-INGEST (thuộc phạm vi hồ sơ) chạy
   `ingest-route`/`profile-ingest … --json` DRY → plan + `plan_hash` → append Q-APPROVALS. Văn bản
   vào ở trạng thái **staged `corpus=false`** — có mặt để rà tiếp, chưa được tin là corpus.
   **Nguồn tải (uỷ quyền trong kickoff — chống hỏi-người rời rạc):** văn bản lấy được từ danh sách
   nguồn tin cậy đã khai (vbpl.vn, Công báo, cổng .gov.vn/.chinhphu.vn…) → máy TỰ tải vào khu tập kết;
   KHÔNG tự lấy được → gắn `cho_nguoi_tai` (kèm link TVPL nếu có) và **gom hỏi chung tại điểm chạm ②**,
   không hỏi lẻ từng file giữa chừng.
   **Bậc thang TVPL (chốt 25-07 — docx TVPL chất lượng file tốt nhất, user có account):**
   - Local/Cowork có Chrome đăng nhập TVPL sẵn → kênh **`tl tvpl-url` auto-download docx TUẦN TỰ** cho cả
     lô (uỷ quyền trong kickoff; recipe thực chiến: click tab "Tải về" trước rồi mới `(docx)`).
     **Ranh giới an toàn TUYỆT ĐỐI:** chỉ dùng phiên ĐÃ đăng nhập — máy không bao giờ nhập mật khẩu hộ;
     gặp login hết hạn/CAPTCHA → DỪNG kênh, tụt bậc, gom hỏi người tại ②.
   - **Quota guard:** đếm `quota_tvpl` trong state như quota NLM (ngưỡng thật CẦN NGƯỜI XÁC NHẬN — ghi cũ
     "~1 docx/ngày" có thể lỗi thời với account hiện tại); chạm ngưỡng → tụt bậc **LuatVietnam (docx) →
     vbpl.vn (.doc) → Công báo (PDF = hạ sách cuối, kiểm chất lượng text theo luật cứng C1/10a)**.
   - Claude chat: không lái Chrome được → link TVPL bấm-được cho người tự tải, gom MỘT lần tại ②.
   - **KHÔNG đổi canonical:** mọi bản tải về vẫn qua QT-2 + xác minh official-first (`_official_rank`
     vbpl/Công báo=1 … TVPL=4 giữ nguyên — TVPL cho FILE đẹp, official để CHỐT bản đúng).
   **Chuẩn-bị-trước, duyệt-sau:** mọi việc nặng (tải, bóc tách, cache, dry-run) làm XONG TRƯỚC khi hỏi
   người — lúc duyệt, việc còn lại chỉ là ghi registry vài giây/lô; thời gian người vắng mặt không thành
   thời gian máy chết (vòng RÀ vẫn chạy trên đơn vị đã có).
2. **Điểm chạm ② (1 lần/pha):** người mở bảng Q-APPROVALS — mỗi dòng: tên chuẩn, đích, plan_hash —
   duyệt cả lô. Máy chạy chuỗi apply với `--expected-plan-hash` (lệch plan = tự chặn).
3. **Cổng máy đóng lô:** `verify-staged` (DRY báo cáo → `--apply --confirm yes`) — PASS flip
   `corpus=true` cả lô (1 `reg_bulk` journaled, **undo được cả lô**), FAIL ở lại staged kèm cờ.
   **Tách kênh:** kênh kho/cache (không cần NLM) dừng ở đây — đơn vị RÀ ĐƯỢC NGAY; kênh NLM đi riêng:
   nguồn flip xong append **Q-NLM**, worker §4a nạp tuần tự sau, không chặn ai.
4. Văn bản mới flip xong → `ingest_to_cache` → `rasoat_worksheet` chấm phân tầng → **sinh đơn vị
   mới vào Q-UNITS** → Loop A rà tiếp. Vòng khép kín.
   **Đơn vị "đối chiếu bổ sung" (chốt 25-07 — bịt lỗ hổng file-mới-liên-quan-đơn-vị-đã-done):** khi văn
   bản mới D flip vào corpus, chạy `relation-check`/frontier 2 CHIỀU: đơn vị `done` nào dẫn chiếu tới/bị
   D dẫn chiếu → sinh đơn vị loại `doi_chieu_bo_sung` (cặp đơn-vị-cũ × D) — CHỈ so phần giao với D,
   không rà lại toàn đơn vị. **Bất biến (test khoá):** đơn vị `done` không bao giờ reset về `pending`
   toàn phần trừ khi anchor vỡ. Chi phí O(delta) — "rà lại là phép tính, không phải làm lại".

> Biến thể tự trị hơn (tuỳ khẩu vị rủi ro, ghi trong kickoff contract): người có thể **uỷ quyền trước**
> cho bước 2 với điều kiện hẹp — "văn bản được ≥1 phát hiện đã-verify dẫn chiếu đích danh, đúng loại
> VBQPPL, đi làn staged" ⇒ máy tự apply lô staged, người chỉ còn duyệt bước 3 (flip). Điểm dừng có
> chủ đích vẫn còn — nhưng lùi về nơi rẻ nhất.

### §4a. WORKER Q-NLM — nạp NotebookLM TUẦN TỰ, tách khỏi đường găng (chốt 25-07)

Nạp NLM chậm (lô 8 nguồn ≈ 86,5s + reconcile 27,8s) trong khi đơn vị rà chỉ cần CACHE. Ghép nạp NLM vào
vòng RÀ là tự chuốc nghẽn — tách thành worker riêng:

- **MỘT worker duy nhất, drain Q-NLM tuần tự tới hết** (tuần tự là chủ đích: cookie mong manh, có
  reconcile sau lô, tránh dồn dập). KHÔNG chạy nhiều worker song song.
- **Phạm vi ghi = NLM + JSON trả về, KHÔNG hơn:** worker không ghi registry, không ghi file trong cây;
  kết quả trả JSON về phiên chính — phiên chính mới cập nhật Q-NLM trong state (giữ một-người-ghi +
  bài học rogue-edit).
- **Idempotent qua reconcile (khuôn r192):** worker chết giữa chừng → chạy lại tự bỏ qua nguồn đã có.
- **Bẫy PDF ghi thẳng vào đặc tả:** `nlm-add --drive-id` HỎNG với PDF → đi đường tải file + `source_add
  source_type=file`; hỏng nữa → đánh `failed` + ghi làn lỗi, KHÔNG retry vô hạn.
- **Theo môi trường (§5b):** local = background task thật của phiên chính; Claude chat = worker là VAI,
  mỗi phiên thức dậy drain một đoạn, hàng đợi nằm trên Drive chờ phiên sau. Chậm hơn, không sai hơn.

### §4b. PHÒNG THỦ NLM 3 TẦNG — cookie chắc chắn chết khi chạy lâu (chốt 25-07)

Điểm neo doctrine: NLM chỉ giữ vai **ĐỊNH VỊ + KIỂM CHÉO** — nguyên văn CHỈ từ cache/raw. Mất NLM =
mất tiện, KHÔNG mất đúng.

| Tầng | Cơ chế | Môi trường |
|---|---|---|
| 1. Tiền kiểm | Pha 0 đo tuổi cookie mỗi lần thức dậy + cron `secrets-set --nlm` ngày 1 lần phía local | mọi nơi |
| 2. Tự refresh | gặp lỗi xác thực giữa chừng → tự chạy `nlm login`/`refresh_auth` MỘT lần trước khi bỏ cuộc | CHỈ local (Cowork/chat không tự refresh được → nhảy thẳng tầng 3) |
| 3. Chế độ chạy-không-NLM | T2 thay bằng quét cache/Drive trực tiếp (chậm hơn, tốn context hơn, tất định); phát hiện vẫn ghi nhưng `muc_chac_chan="cho_verify_nlm"` + vào **Q-VERIFY**; cookie sống lại → MỘT lượt trả nợ kiểm chéo tuần tự, đạt thì nâng hạng | mọi nơi — vòng RÀ **không bao giờ dừng vì cookie** |

### LOOP C — TÁI RÀ ĐỊNH KỲ (mới hoàn toàn so với kế hoạch trước; P5+P6)

Chạy theo **Routine/cron** (tuần 1 lần, hoặc sau mỗi đợt nạp lớn), phiên mới, context sạch:

| Bước | Việc | Lệnh/cơ chế | Kết quả |
|---|---|---|---|
| C1 | Kéo delta rẻ | `registry_orchestrator.py boot` (`changes_pull` — delta token, không quét toàn bộ) | danh sách doc đổi |
| C2 | Soi hiệu lực từng doc hồ sơ | `vb_status`, `relation-check`, `vbhn-check` (QT-5, VBHN-first lượt-2) | phát hiện VBHN mới hơn / luật sửa đổi / hết hiệu lực |
| C3 | Đối chiếu **anchor**: phát hiện nào có `doc_deps.text_hash` ≠ bản hiện hành, hoặc doc bị supersede, hoặc TTL cạn | so hash trong registry/cache | tập phát hiện STALE (thường NHỎ) |
| C4 | **Diff-aware re-queue:** với doc đổi → `footnote-map` + so cache bản cũ/bản mới → chỉ Điều THAY ĐỔI mới sinh lại đơn vị rà; Điều không đổi → phát hiện cũ **tự gia hạn** (cập nhật `verified_at`, không tốn NLM) | footnote-map + diff cache | Q-UNITS nhận vài đơn vị `stale`, không phải cả hồ sơ |
| C5 | Có việc → chạy Loop A như thường; **không có delta → thoát im lặng** (P6) | — | không spam người |
| C6 | Phát hiện bị VÔ HIỆU bởi bản mới (điều khoản đã được sửa đúng như đề xuất) → chuyển `resolved_by_amendment`, giữ trong sổ làm vết | ghi state | phiếu lần sau tự sạch |

Đây là điểm ăn tiền của anchor: **"rà lại định kỳ" không phải rà lại — là phép so hash + rà phần diff.**
Chi phí mỗi kỳ ≈ 0 khi corpus đứng yên, và tỷ lệ thuận với mức thay đổi thật khi có biến động.

### LÀN LỖI (xuyên suốt — P4)

1. Lỗi lệnh → thử fallback CÓ SẴN theo thứ tự đã biết (`--method auto`; cookie chết → `BATCH_LINKS`;
   GAS cache 600s → đợi/`--refresh`; server cũ → guard SERVER_TOO_OLD đã fail-closed sẵn).
2. Vẫn bí → ghi `rasoat_bugs.md` (VERSION + lệnh tái hiện + hậu quả) → đơn vị hiện tại đánh `blocked`
   (KHÔNG mất, không giả done) → lấy đơn vị pending kế tiếp.
3. Chỉ dừng toàn cục khi: mọi đơn vị còn lại đều blocked bởi CÙNG một lỗi (= chặn đứng thật). Khi đó
   báo người đúng 1 dòng + trạng thái đã checkpoint.
4. Sửa nóng tại LIVE: KHÔNG (deploy là bước tay, LIVE drift). Fix làm ở canonical theo đúng quy trình
   (test `rXX_`), deploy đợt sau; Loop C lần kế tự phát hiện `skill_version` mới và **re-queue các đơn
   vị blocked** — vòng tự lành mà không ai phải nhớ.

---

## §4c. NHỊP REGISTRY / MANIFEST / BACKFILL — 4 nhịp, CẤM chen ngang (chốt 25-07)

(manifest ở đây = manifest PROFILE — ảnh chụp Sheet registry; KHÔNG phải `RELEASE_MANIFEST.json` đóng gói.)
Phần máy đã tối ưu sẵn trong `registry_orchestrator.py` («kiểm RẺ chạy LUÔN, kiểm ĐẮT chỉ khi nghi vấn»);
mục này chỉ chốt các việc đó ĐỨNG Ở NHỊP NÀO của 3 vòng lặp:

| Nhịp | Việc | Ghi chú |
|---|---|---|
| 1. BOOT (mỗi phiên) | `registry_orchestrator boot` = `changes_pull` delta token — ghép vào lô warm-up NỀN §5a | KHÔNG regen2 ở boot trừ khi orchestrator tự leo thang (delta > ngưỡng 40) |
| 2. TRONG vòng RÀ (Loop A) | registry **CHỈ ĐỌC, và đọc OFFLINE** (`reg-query` trên manifest cache; `--live` chỉ readback hẹp ngay sau ghi) | **CẤM mọi backfill/hygiene giữa vòng rà** — gom về ranh giới pha (P2). Chỗ dễ vi phạm nhất |
| 3. CUỐI LÔ NẠP (Loop B.4) | `nlm-reconcile --all-notebooks` MỘT lần/lô + readback 1 lần (nếp PERF v1.34.73). **Sau-lô:** `backfill-title-vn` cho dòng MỚI (lô 40, xếp vào ĐUÔI worker Q-NLM sau khi add xong) — `title_vn` có dấu nuôi QT-5/tra cứu mà vòng rà dùng NGAY, không dồn cuối hồ sơ | `backfill-loai`/`recat` HẾT cần sau ingest (v1.33.44 ghi sạch ngay) — chỉ còn cho dòng cũ, xếp nhịp 4 |
| 4. CHECKPOINT/KẾT PHIÊN + Loop C | kết phiên = `tl manifest` (orchestrator `end`: export luôn, regen2 CHỈ khi `--touched-drive`) → manifest tươi làm sẵn cache cho warm-up phiên sau — hai nhịp tự nuôi nhau. `ops-plan` cuối phiên rà → kết quả đổ vào **Q-APPROVALS chờ duyệt**, KHÔNG tự `--apply`. Vệ sinh định kỳ (`hygiene scan`/`sweep`/`tl loop`) ghép cùng nhịp **Loop C hằng tuần** — cùng phiên-mới, cùng thoát-im-lặng | backfill one-shot sau deploy (`backfill-nlm-status`, `profile-backfill-markers`) KHÔNG thuộc vòng lặp nào |

**Hai bẫy:** (a) GAS cache ~600s — dò trùng phải `--refresh` (B0), ghi xong readback `--live` hẹp, không tin
cache; (b) `regen2` là lệnh ĐẮT duy nhất nhóm này — chỉ chạy qua orchestrator (ngưỡng/`--touched-drive`),
không bao giờ chạy tay giữa hồ sơ.

---

## §5. LỊCH THỨC DẬY (tự động hoá theo thời gian)

| Lịch | Việc | Cơ chế |
|---|---|---|
| Mỗi phiên làm việc | Loop A drain + Loop B gom lô | người mở phiên hoặc Routine hằng ngày |
| Tuần 1 lần | Loop C tái rà | Routine phiên-mới, prompt cố định "chạy tái rà hồ sơ X"; thoát im lặng nếu không delta. **(A2)** wrapper khai `disallowed-tools: AskUserQuestion` (kho nêu đích danh use case background loop) + `disable-model-invocation: true` — tái-rà chỉ chạy theo lịch/lệnh tường minh (nguồn: `claude-skills.md`). **(A3)** chạy headless local (`claude -p`): thêm `--max-turns` + `--max-budget-usd` làm fail-safe ngoài `max_iter` — cả hai CHỈ có ở print mode, Routine cloud phải dựa `max_iter` trong state (nguồn: `claude-cli-startup-flags.md` §Budget & Limits) |
| Ngày 1 lần (phía LOCAL) | refresh cookie NLM (`secrets-set --nlm`) | cron máy local (COWORK_PROJECT.md §3) — Cowork/chat không tự refresh được (tầng 2 §4b chỉ có ở local) |
| Trước mỗi lượt bất kỳ | Pha 0 tiền kiểm | luôn luôn — rẻ, chặn sớm |

### §5a. WARM-UP TOOLS lúc khởi động (chốt 25-07) — làm nóng, KHÔNG thay cổng

| Môi trường | Cách làm |
|---|---|
| Cowork / Claude Code | **Warm-up NỀN** ngay khi phiên bắt đầu: `tl ping --json` + `nlm-auth-status` + tuổi cookie + `registry_orchestrator boot` (changes_pull delta — nhịp 1 §4c) chạy background task (read-only), kết quả ghi file nhỏ; Pha 0 **đọc lại** kết quả thay vì chờ gọi mới — phiên chính trong lúc đó đọc PLAN/worksheet. Gắn: bước nền trong RUNBOOK boot hoặc SessionStart hook dev-side (`.claude/settings.json` — không vào zip). Tool MCP load MỘT lần theo lô (ToolSearch batch / `alwaysLoad` cho server NLM — kho best-practice `claude-settings.md` §Per-Server Tool Loading) |
| Claude chat | Không có background thật → **Pha 0 phân tầng LƯỜI**: (a) boot chỉ `ping` GAS (1 call, rẻ, đằng nào cũng cần); (b) probe NLM HOÃN đến ngay trước lần dùng NLM đầu — lượt chạy chế độ không-NLM thì khỏi probe; (c) không chặn việc đọc/lập kế hoạch sau lưng probe chưa cần |

**Hai ranh giới:** (1) warm-up CHỈ dùng lệnh read-only (ping/status/probe) — không "làm nóng" bằng lệnh ghi;
(2) kết quả warm-up có **TTL** — cookie đo lúc boot có thể chết sau 3 giờ; warm-up là làm nóng, "Pha 0 trước
mỗi lượt" vẫn là cổng thật (chỉ được đọc lại kết quả nền khi còn tươi).

---

## §5b. MA TRẬN MÔI TRƯỜNG — cùng một bộ state, ba môi trường thay nhau cầm việc (chốt 25-07)

Các cổng mạnh nhất (`--expected-plan-hash`, `--confirm yes`, fail-closed) là code trong `tl.py` — chạy đâu
cũng ép được. Cái khác nhau giữa môi trường là hạ tầng quanh vòng lặp:

| Cơ chế | Claude Code/Cowork local | Claude chat (LIVE Package) | Hệ quả thiết kế |
|---|---|---|---|
| Lưu trữ giữa phiên | `~/.tra_luat_cache` sống lâu | sandbox **xoá trắng mỗi phiên** | state sống-còn trên Drive (§3) nên kế nhiệm vẹn; riêng chat: đẩy `master/` sau MỖI đơn vị/lô nhỏ |
| Worker Q-NLM | background task thật | không có tiến trình nền bền | worker là **VAI**: mỗi phiên drain một đoạn, hàng đợi chờ trên Drive (§4a) |
| Tự refresh cookie (tầng 2 §4b) | `nlm login` CLI có thật | không có | chat nhảy thẳng tầng 3 (chạy-không-NLM + Q-VERIFY) |
| Lịch Loop C | cron/Routine | không có cron tin cậy | chat: MỘT câu gõ tay tuần 1 lần, hoặc uỷ máy local chạy — state chung trên Drive, ai chạy cũng được |
| Hook duyệt `--apply` | PreToolUse ép cứng | không có hook | còn (a) cổng code `tl.py` (mạnh, giữ nguyên) + (b) doctrine SKILL.md "HỎI trước `--apply`" (mức nhắc) |
| Agent con cách ly context | spawn được (frontmatter ép read-only — A1) | **không spawn gì cả** | vòng lặp chạy trong chính phiên; ngân sách context hẹp hơn → checkpoint sớm + bàn giao qua file càng quan trọng |

---

## §6. CÁI PHẢI XÂY THÊM (tối thiểu, đối chiếu kế hoạch hạng mục)

Workflow trên chạy được ~70% bằng lệnh đã có. Phần thiếu, xếp theo giá trị/công sức:

1. **Template master TẠO MỚI có anchor + `muc_chac_chan` ngay từ đầu** — local KHÔNG có
   `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` (đã kiểm 25-07), tạo theo H1, KHÔNG có bước merge;
   `rasoat_phuluc.py` bỏ qua field lạ + mở rộng tối thiểu để phụ lục xuất kèm (H1b). Điều kiện của Loop C.
2. **`rasoat_state.json` (gồm Q-INGEST/Q-NLM/Q-VERIFY) + quy ước claim/checkpoint** trong `_meta/` profile
   trên Drive — schema + kịch bản, không code lõi. *(≈ H2, nơi lưu LAI §3)*
3. **Kịch bản vòng lặp** (`references/RASOAT_HOSO_LOOP.md`) bọc A1–A8/B0–B4/C1–C6 bằng từ vựng
   `dry_rounds`/`max_iter`/PAUSE — prose mỏng vì mọi bước đều trỏ lệnh thật. Gồm cả đặc tả worker Q-NLM
   (§4a), chế độ không-NLM (§4b), đơn vị `doi_chieu_bo_sung` (B.4) và 2 luật riêng cho chat (§5b). *(≈ H3)*
4. **Staleness scanner** — phần code MỚI duy nhất đáng viết: đọc master + registry, so hash, in danh sách
   stale + lệnh re-queue. Read-only, JSON, tất định → dễ test golden. *(mới — phục vụ Loop C)*
5. Routine wrapper cho Loop C (prompt cố định + thoát im lặng + frontmatter A2). *(mới, nhỏ)*
6. Agent con cách ly context cho T3 (tuỳ chọn, Đợt sau — không phải nền tảng; khi làm thì ép cứng theo A1).

## §7. VÍ DỤ MỘT CHU KỲ (hồ sơ 3 văn bản, minh hoạ điểm chạm)

```
Ngày 1  NGƯỜI①: "rà hồ sơ dự thảo Luật X: [3 văn bản], ngân sách 60 call NLM, uỷ quyền nạp staged"
        máy: Pha 0 ✓ → nạp 3 VB (lô staged) → NGƯỜI② duyệt lô #1 (1 câu hỏi) → flip ✓
             → worksheet → 14 đơn vị → rà 6 đơn vị, phát hiện NĐ 145 được dẫn 9 lần → Q-INGEST
Ngày 2  máy (Routine): rà tiếp 5 đơn vị; lô staged #2 (NĐ 145 + 2 TT) chờ
        NGƯỜI② duyệt lô #2 (1 câu hỏi) → +5 đơn vị mới từ NĐ/TT
Ngày 3  máy: rà nốt 8 đơn vị; 1 lỗi extract PDF → workaround OCR route, ghi bugs; dry_rounds=2 đạt
             → Pha 4 tổng hợp → phiếu nháp + bảng master + Q-APPROVALS (2 đề xuất reg) + bugs(1)
        NGƯỜI③: nghiệm thu, ký. — Tổng chạm giữa chừng: 2 (đều là duyệt lô).
Tuần 3  máy (Routine C): changes_pull thấy VBHN mới của Luật Y → 4/31 phát hiện stale
             → diff 3 Điều đổi → rà lại 2 đơn vị → 1 phát hiện resolved_by_amendment, 1 giữ nguyên
             → đẩy bản phiếu delta chờ người xem. Các tuần không delta: im lặng.
```

---

*Đối chiếu trên máy dev ĐÃ LÀM 25-07 — kết quả: (1) kho `claude-code-best-practice` KHÔNG khuyên ngược
P1–P7; 3 bổ sung A1–A3 đã nhập vào thân (đầu file + §5 + KE_HOACH C4). (2) `templates/…json` local KHÔNG
tồn tại → tạo mới theo H1, schema anchor + `muc_chac_chan` nhập ngay từ đầu, không có bước merge.*
