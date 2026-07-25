# WORKFLOW RÀ SOÁT TỰ ĐỘNG HOÁ CAO — "NHÀ MÁY RÀ SOÁT" (đề xuất, chưa triển khai)

> Trạng thái: ĐỀ XUẤT thiết kế (docs-only). Bổ sung cho `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md`
> (kiến trúc + hiện trạng + hạng mục); tài liệu này mô tả **workflow vận hành** — dòng chảy, hàng đợi,
> sự kiện, và cách đạt tự động hoá cao nhất trong khuôn khổ 3 điểm dừng có chủ đích.
> Yêu cầu gốc (2026-07-25): tự động hoá cao nhất; **giữa chừng nạp thêm nguồn**; **sửa lỗi phát hiện được**;
> **định kỳ rà lại kết quả cũ**.
> ⚠ Kho `claude-code-best-practice` là clone dev-only local, KHÔNG có trong phiên remote này — các
> nguyên lý §1 cần đối chiếu lại kho đó trên máy dev trước khi chốt (CLAUDE.md buộc ưu tiên kho).

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

## §3. STATE — 4 hàng đợi + sổ phát hiện (tất cả là FILE, nằm trong `_meta/` của profile hồ sơ — P1+P7)

| File | Vai trò | Ghi chú |
|---|---|---|
| `_meta/rasoat_state.json` | Q-UNITS + con trỏ chu kỳ + `session_claim` + quota NLM còn lại + note bàn giao | nguồn sự thật resume; nằm trên Drive theo ADR-0003 → bền hơn `~/.tra_luat_cache` (bị reset giữa phiên) |
| `_meta/rasoat_ingest_queue.json` | Q-INGEST: ứng viên từ `frontier-expand` (`missing_in_corpus`) + user bổ sung, kèm trạng thái dry-planned/staged/flipped | mục nào NGOÀI phạm vi kickoff contract → gắn `out_of_scope`, chờ người, không tự nạp |
| `master/<unit>.json` (thư mục) | sổ phát hiện — 1 file/đơn vị rà, schema `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` | append-only ở mức thư mục; `rasoat_phuluc.py --in master/` gộp khi tổng hợp |
| `_meta/rasoat_bugs.md` | Q-BUGS: lỗi skill gặp giữa chừng | mỗi mục: VERSION đo được + lệnh tái hiện + workaround đã dùng + phân loại workaround/blocker |
| `_meta/rasoat_approvals.json` | Q-APPROVALS: các dry-plan (kèm `plan_hash`) đã gom, chờ duyệt lô | người duyệt đọc 1 bảng, chấp thuận → máy chạy chuỗi `--apply --confirm yes --expected-plan-hash` |

**NEO PHỤ THUỘC của mỗi phát hiện** (điều kiện của Loop C — P5), thêm vào mỗi dòng `noi_dung[]`:

```json
"anchor": {
  "doc_deps": [{"so_hieu": "18/VBHN-VPQH 2025", "text_hash": "sha256:…", "dieu": ["54", "125"]}],
  "cite": "cache:18VBHN2025#dieu54",
  "skill_version": "1.35.38",
  "verified_at": "2026-07-25",
  "ttl_ngay": 90
}
```

Ý nghĩa: phát hiện này ĐÚNG chừng nào các `text_hash` kia còn là bản hiện hành. Đổi hash / có VBHN mới
/ TTL cạn (với mức "cần kiểm tra") ⇒ máy TỰ biết phát hiện nào cần rà lại — không cần người nhớ.

---

## §4. BA VÒNG LẶP — mô tả từng bước, ánh xạ lệnh CÓ THẬT

### LOOP A — RÀ (mỗi phiên thức dậy chạy một lượt drain)

| Bước | Việc | Lệnh/cơ chế có thật | Tự động? |
|---|---|---|---|
| A1 | Pha 0 tiền kiểm: ping, cookie, VERSION khớp | `doctor`/`ping`, `nlm-auth-status`, probe 3 kênh NLM (KERNEL_APPENDIX §E) | ✅ — fail chặn đứng thì dừng sớm TRƯỚC khi tiêu NLM |
| A2 | Nhận vai: ghi `session_claim` (id phiên + giờ) vào state | RMW qua GAS (LockService làm lưới) | ✅ |
| A3 | Lấy đơn vị `pending` ưu tiên cao nhất (SÂU trước, theo phân tầng worksheet) | `rasoat_worksheet.py` đã chấm SÂU/ĐỐI CHIẾU/— | ✅ |
| A4 | T1→T2→T3 theo quy trình 3 tầng; mở rộng frontier | `tra_cuu --cite --exact`, `notebook_query` scoped, `frontier-expand --json` | ✅ (ngân sách NLM trừ dần trong state) |
| A5 | VERIFY từng phát hiện | `nlm_qa verify`; nguyên văn CHỈ từ cache/raw | ✅ — phát hiện fail verify KHÔNG được ghi |
| A6 | Ghi `master/<unit>.json` (kèm anchor) + đánh `done` + cập nhật CSV nhật ký NLM | ghi file, ngoài cây skill | ✅ |
| A7 | Ứng viên mới từ A4 → append Q-INGEST; Điều liên quan mới → append Q-UNITS | máy phân loại theo phạm vi kickoff | ✅ |
| A8 | Cạn ngân sách/context → chốt checkpoint + note bàn giao → thoát êm | state đã là file nên "thoát" = không làm gì thêm | ✅ |

### LOOP B — NẠP GIỮA CHỪNG (chìa khoá: làn STAGED r200 — P2)

Vấn đề gốc: nạp văn bản là đường GHI rủi ro cao (hook hỏi từng `--apply`) ⇒ nạp giữa chừng kiểu cũ
= chạm người O(số file). Làn staged đảo lại:

1. **Tự động, không cần duyệt nội dung:** mỗi ứng viên trong Q-INGEST (thuộc phạm vi hồ sơ) chạy
   `ingest-route`/`profile-ingest … --json` DRY → plan + `plan_hash` → append Q-APPROVALS. Văn bản
   vào ở trạng thái **staged `corpus=false`** — có mặt để rà tiếp, chưa được tin là corpus.
2. **Điểm chạm ② (1 lần/pha):** người mở bảng Q-APPROVALS — mỗi dòng: tên chuẩn, đích, plan_hash —
   duyệt cả lô. Máy chạy chuỗi apply với `--expected-plan-hash` (lệch plan = tự chặn).
3. **Cổng máy đóng lô:** `verify-staged` (DRY báo cáo → `--apply --confirm yes`) — PASS flip
   `corpus=true` cả lô (1 `reg_bulk` journaled, **undo được cả lô**), FAIL ở lại staged kèm cờ.
   NLM nạp sau qua `nlm-links`/`ingest-missing` (cũng DRY-first, cũng vào Q-APPROVALS).
4. Văn bản mới flip xong → `ingest_to_cache` → `rasoat_worksheet` chấm phân tầng → **sinh đơn vị
   mới vào Q-UNITS** → Loop A rà tiếp. Vòng khép kín.

> Biến thể tự trị hơn (tuỳ khẩu vị rủi ro, ghi trong kickoff contract): người có thể **uỷ quyền trước**
> cho bước 2 với điều kiện hẹp — "văn bản được ≥1 phát hiện đã-verify dẫn chiếu đích danh, đúng loại
> VBQPPL, đi làn staged" ⇒ máy tự apply lô staged, người chỉ còn duyệt bước 3 (flip). Điểm dừng có
> chủ đích vẫn còn — nhưng lùi về nơi rẻ nhất.

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

## §5. LỊCH THỨC DẬY (tự động hoá theo thời gian)

| Lịch | Việc | Cơ chế |
|---|---|---|
| Mỗi phiên làm việc | Loop A drain + Loop B gom lô | người mở phiên hoặc Routine hằng ngày |
| Tuần 1 lần | Loop C tái rà | Routine phiên-mới, prompt cố định "chạy tái rà hồ sơ X"; thoát im lặng nếu không delta |
| Ngày 1 lần (phía LOCAL) | refresh cookie NLM (`secrets-set --nlm`) | cron máy local (COWORK_PROJECT.md §3) — Cowork không tự refresh được |
| Trước mỗi lượt bất kỳ | Pha 0 tiền kiểm | luôn luôn — rẻ, chặn sớm |

---

## §6. CÁI PHẢI XÂY THÊM (tối thiểu, đối chiếu kế hoạch hạng mục)

Workflow trên chạy được ~70% bằng lệnh đã có. Phần thiếu, xếp theo giá trị/công sức:

1. **Anchor trong schema master** (sửa `templates/…json` + quy ước ghi) — không cần code mới, `rasoat_phuluc.py`
   bỏ qua field lạ. Điều kiện của Loop C. *(≈ H1 mở rộng)*
2. **`rasoat_state.json` + quy ước claim/checkpoint** trong `_meta/` profile — schema + kịch bản, không code lõi. *(≈ H2, chuyển nơi lưu theo P7)*
3. **Kịch bản vòng lặp** (`references/RASOAT_HOSO_LOOP.md`) bọc A1–A8/B1–B4/C1–C6 bằng từ vựng
   `dry_rounds`/`max_iter`/PAUSE — prose mỏng vì mọi bước đều trỏ lệnh thật. *(≈ H3)*
4. **Staleness scanner** — phần code MỚI duy nhất đáng viết: đọc master + registry, so hash, in danh sách
   stale + lệnh re-queue. Read-only, JSON, tất định → dễ test golden. *(mới — phục vụ Loop C)*
5. Routine wrapper cho Loop C (prompt cố định + điều kiện thoát im lặng). *(mới, nhỏ)*
6. Agent con cách ly context cho T3 (tuỳ chọn, Đợt sau — không phải nền tảng).

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

*Đối chiếu bắt buộc trên máy dev trước khi chốt: (1) kho `claude-code-best-practice` (P1–P7 có mục nào
kho khuyên khác không); (2) `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` local có sẵn chưa (nếu có thì
schema anchor phải merge vào bản đó, không tạo bản thứ hai).*
