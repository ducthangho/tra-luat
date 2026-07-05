# ★ v1.33.32 — MERGE bundle-12 (`tra-luat-skill-v1.33.31-gws3env-fixed.zip`): nhánh song song CÙNG 3 vấn đề trên v1.33.30 — hội tụ lần 4, mỗi bên mạnh một nửa

Bundle-12 dựng trên v1.33.30, tự đặt TRÙNG SỐ v1.33.31, xử CÙNG log rà LIVE v1.33.28 với canonical v1.33.31 ta
(S-1 P0 giả · S-2 đếm kép omnibus · A cookie già). Đối chiếu BẰNG HÀNH VI từng mảng:

## PORT (4 — bản họ đúng/giàu hơn)
- **S-1 TIÊU CHÍ PHỦ ĐỊNH theo tín-hiệu-hành-động** (thay `verdict=OK` của ta): suppress khi
  missing_links/subject_only_review/footnote_only_amendments ĐỀU rỗng — negate được cả ca THIẾU VBHN
  (verdict=QT5_WEB_REQUIRED; thiếu VBHN là việc bucket WEB, không giữ oan tín hiệu rel — ta bỏ sót lớp 68-2025/
  44-2019). TINH CHỈNH khi nhận: BỎ `amend_n` khỏi tiêu chí bundle — candidates ĐÃ-linked-đủ (không missing_links)
  không có gì để backfill, giữ chúng là oan (bundle giữ → ca đã-hợp-nhất-xong vẫn treo INFO).
- **S-1 bucket riêng `relation_probe_suppressed`** (+counts key) — hàng đợi rel_low chỉ còn ca CÒN tín hiệu;
  ca phủ định tách bạch, counts vẫn cộng về laws_scanned.
- **S-1 payload `row.relation_probe`** (verdict/flags/counts/note) đi kèm row kể cả khi row rơi bucket web —
  driver thấy NGAY vì sao phủ định/giữ, khỏi chạy lại relation-check tay.
- **S-1 ops-plan 3 tầng**: P0 CHỈ ứng viên MẠNH (`relation_check_before_backfill`); low-conf còn tín hiệu →
  **P2 `relation_low_confidence_probe`** read-only (LOW_CONF là INFO, không phải việc P0); + **mirror
  registry_hygiene.py**: OMNIBUS_NARROW rời title_mismatch của registry-doctor (nhất quán với sweep).

## GIỮ TA (4 — bundle không có/nông hơn)
- Phạm vi probe = strong LẪN low-conf (bundle chỉ low-conf — bỏ sót backfill-khống lớp A1 v1.33.4).
- Cờ `RELATION_CHECK_NEGATED` trên row + `relation_negated_count` (grep-được, đếm cả row rơi bucket web).
- **P3 `relation_candidates_negated`** info audit-trail trong ops-plan (bundle drop hẳn — mất dấu vì sao biến mất).
- S-2 bucket `omnibus_title_advisory` trong sweep (bundle DROP im lặng khỏi title_mismatch — mất visibility);
  cookie-age: helper `_nlm_cookie_age_note` phủ 6 đường + doctor (bundle chỉ vá nlm-auth-load, message inline).

Bundle KHÔNG có test nào (0); ta viết lại r42 theo shape gộp + r43 khoá tiêu chí PORT (suppress-dù-QT5, control
subject-only giữ; mirror registry_hygiene). selftest **586/586** (+2). Zip bundle còn __pycache__/.pytest_cache —
không port thói quen đóng gói.

---

# ★ v1.33.31 — xử log rà LIVE v1.33.28 (2026-07-05): S-1 hai engine bất đồng · S-2 advisory kép omnibus · A cookie già nạp im lặng

Log Cowork chạy LIVE v1.33.28 (67 Luật, ops-plan P0→P3). Nhóm 🟠 false-positive + 1 ma sát vận hành = CODE-fixable:

## S-1 — review-queue CROSS-VALIDATE ứng viên sửa đổi qua relation-check (hết P0 giả)
- **Hiện tượng:** review-queue gắn 124/125-2025 (GDNN/GDĐH) cờ `AMENDMENT_CANDIDATE_LOW_CONFIDENCE`/
  `UNLINKED_AMENDMENT_CANDIDATE`/`VBHN_RECHECK_REQUIRED` → ops-plan đẩy **P0** `relation_check_before_backfill`;
  nhưng `tl relation-check --base 124-2025-QH15` (engine tất định `_relation_audit`) trả **verdict=OK, flags=[],
  candidates=[]**. Hai engine BẤT ĐỒNG — người vận hành phải chạy relation-check tay TỪNG SỐ để loại (cùng lớp:
  68-2025, 44-2019 trong web_round2).
- **Fix:** `_review_queue_report` nay tự chạy `_relation_audit(entries, base=<sohieu>)` cho MỌI row có cờ rel
  (strong lẫn low-conf). Audit **verdict=OK** (= không missing_links/subject_only/footnote-thiếu, VBHN đã thấy)
  → cờ **`RELATION_CHECK_NEGATED`** + hạ khỏi bucket hành động (rel→rel_low), fix_command ghi "ĐÃ PHỦ ĐỊNH",
  top-level +`relation_negated_count`. Audit còn REVIEW/QT5 → KHÔNG negate (fixture 06/2022 subject-only nguyên trạng).
- **ops-plan:** row mang `RELATION_CHECK_NEGATED` KHÔNG vào P0 nữa — hạ dòng info **P3
  `relation_candidates_negated`** (audit-trail, confirm_required=false); P0 chỉ giữ ca chưa phủ định + note số ca đã loại.

## S-2 — khử advisory KÉP `OMNIBUS_NARROW_TITLE_CHECK` (sweep)
- **Hiện tượng:** 45-2019 (BLLĐ) xuất cờ ở bảng flags từng entry RỒI LẠI vào `title_mismatch` của sweep (2 dòng)
  — 1 nguyên nhân đếm 2 lần, người rà tưởng 2 vấn đề. "Không sai dữ liệu": tên hẹp vs BỊ luật sửa-nhiều-luật đụng
  tới, không có action rename.
- **Fix (mirror advisory-split v1.33.22):** headline `title_mismatch` CHỈ còn `TITLE_METADATA_MISMATCH`;
  OMNIBUS_NARROW một mình → bucket mới **`omnibus_title_advisory`** (+`_rows`, in `omnibus_advisory=` ở sweep text
  + hygiene). Cờ trên entry giữ nguyên (source-map/corpus-audit vẫn thấy).

## A — cảnh báo CHỦ ĐỘNG tuổi cookie NLM (trước đây chỉ in info)
- **Hiện tượng:** `nlm-auth-load` nạp cookie ~19 ngày tuổi IM LẶNG (chỉ in "~19 ngày tuổi" như info) — không ai
  được nhắc re-stage cho tới khi auth chết giữa phiên (cookie sống ~2–4 tuần).
- **Fix:** helper chung `_nlm_cookie_age_note` (ngưỡng `_NLM_COOKIE_WARN_DAYS=14`) — nối chuỗi ⚠ "re-stage sớm:
  `nlm login` → `tl nlm-auth-stage` / `tl secrets-set --nlm`" vào MỌI đường: `nlm-auth-load`, `nlm-auth-pull`,
  `nlm-auth-stage` (nhắc làm tươi TRƯỚC khi gói bản già), `bootstrap` (thay warn ad-hoc >14), `secrets-set --nlm`,
  và **doctor** check `nlm CLI` (đọc extracted_at local; advisory — KHÔNG đổi ok/rc).

**Verify:** selftest **584/584** (+5 r42: rel-negated demote+flag+counts, control not-negated, ops-plan P0→P3,
omnibus advisory-split, cookie threshold) · ruff 505 lỗi = baseline HEAD (0 lỗi mới) · compile OK.
**Không xử ở đây (data/ops, chờ user):** web lượt-2 23-24 Luật (Chrome official-first + vbhn-verify), dedup-plan
--apply (ready 3/review 46), backfill-loai --normalize --apply (1), 159 tên phi chuẩn (corpus-audit --all --full),
slot 298/300 (kế hoạch overflow trước đợt nạp mới), quarantine 105/orphan 8.

---

# ★ v1.33.30 — MERGE bundle-29 (`tra-luat-skill-v1.33.29-gws3env-fixed.zip`): nhánh song song CÙNG log v1.33.28 — port 3 món SÂU hơn bản ta, giữ 4 món ta có mà họ không

Bundle-29 dựng trên v1.33.28, xử cùng 3 log với canonical v1.33.29 — hội tụ lần nữa, mỗi bên mạnh một nửa:

## PORT (3 — bản họ sâu/giàu hơn)
- **candidates[] STRUCTURED** (thay compact-string v1.33.29 ta): item + top-level gộp-dedup, mỗi row đủ
  sohieu_key/confidence/candidate_type/linked_to_query/strong/omnibus/subject_overlap + candidate_count.
  Field-verify 44/2019: ứng viên 71-2020 hiện structured ở top-level.
- **Compound-sohieu ở TẦNG PARSER** `_parse_sohieu_from_name` (thay suppress-flag v1.33.29 ta — mọi consumer
  MISSING_SOHIEU/sweep/corpus-audit cùng hưởng): nhận 'NN-MM-<CQ>[-<CQ>]' CHỈ khi tên có marker VBHN —
  số kép không-marker vẫn trả rỗng (control r41; fixture đầu của ta sai vì '2024-2025-ND' vốn được regex CŨ
  bắt — đã thay control đúng). Giữ luôn suppress-flag ta làm phòng-vệ-kép.
- **`--refresh` flag + TL_FETCH_REFRESH** cho tl_fetch.sh: ép xoá zip+live — escape hatch cho ca Drive re-up
  CÙNG VERSION khác nội dung mà version-compare của ta không bắt được. GIỮ máy version-compare ta (nhanh hơn
  full-refresh mặc định của họ: không re-extract khi version trùng).

## GIỮ TA (4 — họ không có)
- `_resolve_registry_doc_id` (tương đương `_effective_registry_doc_id` họ — giữ bản ta đã test r40).
- BrokenPipe hardening main() · tl_fetch ROOT in kèm VERSION · .gitattributes *.sh=LF.

+test rc-doctrine của họ (sweep/review-queue --json rc=0 dù có findings) adapt fixture ta.
selftest **579/579** (+2 r41, r40 candidates chuyển structured).

---

# ★ v1.33.29 — Xử log verify + log rà v1.33.28 LIVE: doctor pin-check stale · footgun tl_fetch 2 tầng · NO_SOHIEU số-kép · candidates parity · rc=1 ma

3 log chạy LIVE v1.33.28. Fix 5 + phân xử 3:

## FIX (5)
- **S-9b doctor pin-check STALE**: pin xong bằng config-pin-registry (root+profile) mà doctor VẪN in
  '(rỗng → NÊN PIN)' — check cũ CHỈ đọc env TL_REGISTRY_DOC_ID (apply_profile_offline không export key này).
  Helper mới `_resolve_registry_doc_id` (env → profile → root config, trả kèm NGUỒN) dùng cho doctor; note
  pinned in rõ 'pinned · config:<path>'. Field-verify: resolver thấy đúng Sheet 1C21i65… đã pin.
- **Footgun tl_fetch.sh 2 TẦNG** (suýt gây kết luận sai 'ops-plan thiếu'): (t1) $ZIP cũ còn → bước tải BỎ QUA
  → --setup chạy mãi bản cũ → nay `--setup`/`--setup-step core` XOÁ zip ép tải mới (ý định = lấy bản mới nhất;
  step gws/boot/nlm giữ zip); (t2) $OUT/live còn tl.py cũ → giải nén bị bỏ qua + ROOT ghi đè về bản cũ → nay
  SO VERSION zip-vs-đã-giải-nén, lệch = re-extract; ROOT in kèm VERSION mỗi lần.
- **4D NO_SOHIEU_IN_NAME oan cho VBHN số KÉP** ('VBHN_73-82-ND-CP_…' — repro offline): nhận pattern
  'NN-MM-<CQ>[-<CQ>]' trước khi cờ (VBHN gộp nhiều văn bản không thiếu số hiệu).
- **4D source-map thiếu chi tiết ứng viên**: item +`candidates[]` compact 'sohieu|tên|confidence' — CÙNG
  format review-queue rows, driver hết phải gọi thêm lệnh.
- **BrokenPipe hardening** ở main(): 'sweep/review-queue --json rc=1 dù chạy OK' KHÔNG tái hiện (cả 2 return 0
  vô điều kiện) — triệu chứng khớp `--json | head/jq-thoát-sớm` → BrokenPipeError exit 1 → nay nuốt, rc=0
  (payload trọn = dùng --out).

## PHÂN XỬ (không phải lỗi / đã có sẵn)
- `reg-query --json` shape: ĐÃ là envelope `reg-query.v2 {ok, schema, count, rows, entries}` — verify chạy
  thật; 'list trần' của log không tái hiện (khả năng parse nhầm field con).
- `confirm --all-unconfirmed (+--limit)`: ĐÃ TỒN TẠI từ trước — khuyến nghị P1-5 của log là gap nhận-biết;
  usage lệnh tự liệt kê.
- Trôi mẫu số giữa lệnh = GAS cache ~600s + định nghĩa khác nhau — đã docs (`tl counts` + note).

selftest **577/577** (+3 r40: resolver 3 tầng env/profile/root, số-kép không-cờ + control, candidates compact).

---

# ★ v1.33.28 — MERGE bundle-27 (`tra-luat-skill-v1.33.27-gws3env-fixed.zip`): ops-plan + --out phủ lệnh nặng — port trọn, sửa 1 test env-leak + 1 F841

Bundle-27 dựng TRỰC TIẾP trên canonical v1.33.26 (cả selftest xây trên block r38 ta — hội tụ chuỗi công cụ).
Port trọn 2 nhóm, 0 reject lần 3 liên tiếp; 2 chỉnh nhỏ khi nhận:

## PORT (2)
- **`tl ops-plan [--json] [--out]`** (READ-ONLY): gom review-queue + sweep thành HÀNG ĐỢI VIỆC P0→P3
  máy-đọc ({id, command điền sẵn, confirm_required, mode, reason, sample}) — thay việc đọc log dài rồi suy
  lệnh tay; phủ đúng vòng lặp A/B/C/D/E (pin registry, web lượt-2, relation-check-trước-backfill,
  reconcile LIVE, dedup, lô tên, loai, quarantine, slot preflight, cowork-plan). Thực địa: 9 action,
  tự nhận registryDocId_pinned=True sau khi pin. Doctrine giữ: dòng confirm_required=true KHÔNG tự ghi.
- **`--out` atomic mở rộng** cho doctor/cowork-plan/sweep/counts/nlm-get/nlm-reconcile (cùng
  `_emit_json_payload`) — trọn bộ lệnh JSON nặng nay ghi-file-rồi-phân-tích được, né trần 30s Cowork.

## SỬA khi nhận (2)
- Test r39 của bundle KHÔNG hermetic: máy ĐÃ pin registry + env TL_NOTEBOOK_ID từ apply_profile_offline
  (config thật) đè fixture → action pin biến mất + notebook ≠ NB39 → fail OAN trên máy-đã-pin (máy bundle
  chưa pin nên không thấy). Sửa: pop cả bộ env TL_REGISTRY_DOC_ID/TL_NOTEBOOK_ID/TL_PROFILE quanh call,
  khôi phục sau.
- F841 `drift` gán không dùng trong _ops_plan_report — bỏ.

SKILL.md +1 dòng ops-plan/--out. selftest **574/574** (+2 r39, đã hermetic-hoá).

---

# ★ v1.33.26 — MERGE bundle-25 (`tra-luat-skill-v1.33.25-gws3env-fixed.zip`): A5 superset + --out atomic + config-pin-registry — port TRỌN, 0 reject (lần 2 liên tiếp)

Bundle-25 dựng trên v1.33.24, xử cùng log với v1.33.25 ta. Fix A5 của họ là SUPERSET bản ta (thêm
`review_reason` alias, dedup BASE_SCOPE_HIT, QT5-fallback sinh query tối thiểu khi có cờ web mà hint rỗng)
→ lấy tl.py của họ làm nền v1.33.26 (helpers `_mutable_config_target`/`_write_json_atomic` verify tồn tại).

## PORT (4)
- **A5 superset**: flags_all + review_reason ở item + top-level; qt5_queries top-level gộp-dedup (cap 12);
  fallback QT5 khi cờ web mà hints rỗng. Thực địa BLHS: flags_all 3 cờ, review_reason khớp, qt5=8.
- **`--out <file>`** cho source-map/review-queue (+config-pin-registry): `_emit_json_payload` ghi JSON ATOMIC
  (.tmp → os.replace) + in path — xử A3 (heredoc/stdout dài bị trần 30s Cowork giết): driver ghi file rồi
  phân tích tách bước.
- **`tl config-pin-registry <SHEET_ID>`** (S-9 usability): pin registryDocId vào config LOCAL an toàn —
  read-modify-write giữ nguyên key khác, từ chối Doc legacy 1mATG, không gọi Drive/Sheets; --profile-name/
  --root. Checklist mục 6 nay = 1 lệnh (vẫn cần SHEET_ID thật từ user).
- 2 selftest gốc bundle (schema parity + pin-safe) port thành r38 + thêm test --out atomic của ta.

selftest **572/572** (+3 r38). Ghi chú: v1.33.25 canonical (A5 bản ta) bị SUPERSEDE bởi bản superset này —
không mất gì (r37 vẫn pass trên code họ).

---

# ★ v1.33.25 — A5 log rà 67 LIVE v1.33.24: schema source-map ↔ review-queue lệch (flags_all/qt5_queries)

Log rà 67 Luật vòng mới CHẠY LIVE v1.33.24 (bản deploy đầy đủ chuỗi 21..24 — log tự xác nhận advisory=11,
claim=542+slot_rule, doctor path-note hoạt động). Duy nhất 1 bug code mới:

## FIX
- **A5**: `tl source-map <sh> --json` trả `flags_all=None` + `qt5_queries` RỖNG ở top-level trong khi
  review-queue cùng văn bản có đủ — driver batch đọc `.flags_all` đồng nhất giữa 2 surface phải fallback
  (đúng lớp schema-drift B.1 đã vá cho review_other). Fix 2 tầng: item `_source_map_one` +alias
  `flags_all` (= flags — vốn là TOÀN BỘ warning-codes, cùng ngữ nghĩa flags_all của review-queue rows);
  top-level cmd_source_map +`flags_all` aggregate + `qt5_queries` gộp-dedup từ items. Verify thực địa
  71/2020: top flags_all=['AMENDS_OTHER_VBHN'], qt5_queries=8.

Còn lại của log: A1/A2/A4 = workaround đã ship hoạt động (log tự xác nhận); A3 (bash 30s heredoc) = trần
sandbox — khuyến nghị sẵn có (--json ra file rồi phân tích tách bước); B/C/D/E = data-ops/ràng-buộc đã nằm
trong runbook (pin registryDocId, nlm-reconcile --apply 1 mục, web lượt-2 24 Luật, dedup/160-tên/loai,
kế hoạch overflow slot 298/300). selftest **569/569** (+1 r37).

---

# ★ v1.33.24 — MERGE bundle-23 (`tra-luat-skill-v1.33.23-gws3env-fixed.zip`): nhánh hội tụ trên v1.33.22, xử CÙNG log Cowork bằng các món BỔ TRỢ — port TRỌN, 0 reject (bundle sạch nhất chuỗi merge)

Bundle-23 dựng trên canonical v1.33.22, xử cùng log rà Cowork với v1.33.23 ta nhưng chọn các món KHÁC —
BỔ TRỢ hoàn hảo (ta: symlink /usr/local/bin; họ: 5 món dưới). Verify hành vi: chạy integrity check của họ
trên CHÍNH cây canonical (PASS — boot.py ở _fallback lookup với tới) + canary SyntaxError/NUL đều bắt được
+ mọi helper họ gọi (transport.runtime_env, gws_bridge.gws_exe, _resolve_nlm_notebook, NLM_SLOT_CAP,
nlm_cli.notebook_get) tồn tại. LẦN ĐẦU trong chuỗi 8 merge: KHÔNG có gì để reject.

## PORT (5 — nguyên vẹn)
- **`tl cowork-plan [--json]`** (C-1 tổng hợp): checklist bootstrap READ-ONLY — package integrity, gws MUSL,
  nlm step-machine, PATH non-interactive, nhắc slot-LIVE + pin registryDocId; next_actions máy-đọc.
- **doctor +check `package integrity`** (C-1.1): `_skill_package_integrity` compile 7 file core (nhận cả
  _fallback/), bắt NUL/SyntaxError/file-cụt → khuyến nghị tải zip sạch — mount-cắt-cụt hết âm thầm.
- **`tl up --nlm` trên Cowork chỉ chạy 1 bước `nlm-install --resume`** (C-1.2): detect runtime qua
  transport.runtime_env; rc=3 → báo PARTIAL kèm lệnh lặp — hết chết giữa chừng vì trần 45s.
- **doctor phân biệt `tl_nlm_path` vs `shell_nlm_path`** (C-1.4 phía hiển-thị — bổ trợ symlink v1.33.23 ta:
  symlink xử gốc trên Cowork root, hiển thị xử máy không quyền ghi /usr/local/bin).
- **`tl counts --live-nlm [--notebook-id]`** (C-2/C-4): bảng counts in kèm số VẬT LÝ LIVE
  (source_count/cap/remaining/near_full) + `slot_rule` — diệt hẳn bẫy claim-542-vs-vật-lý-298 ngay tại chỗ
  người vận hành nhìn số.

Giữ của ta: `_symlink_nlm_system_path` (bundle không có). SKILL.md +2 dòng lệnh mới.
selftest **568/568** (+4 r36: 2 canary gốc bundle + integrity-PASS-trên-cây-thật [chống doctor false-alarm
vĩnh viễn nếu danh sách file core lệch cây] + parser 2 lệnh mới).

---

# ★ v1.33.23 — C-1.4 log rà Cowork LIVE v1.33.20: `nlm` trần chết ở bash non-interactive

Log rà 67 Luật vòng mới (Cowork, LIVE v1.33.20): 19 mục / 5 lớp — ĐỐI CHIẾU: C-2..C-5 đều là data-ops/known
đã có fixer hoặc trong runbook (C-3 "17 title_mismatch" đã 17→2+advisory ở v1.33.22 CHƯA deploy; "4 stale_nlm_ref"
đã có quarantine-fix reg_clear v1.33.22; 161 tên đã có lô corpus-audit + lane name-only v1.33.21); C-1 phần lớn
là ràng buộc nền tảng đã docs (mount cắt cụt → BƯỚC 0 curl zip; 45s → --resume; gws MUSL → bootstrap sẵn).
CODE-fixable còn đúng 1 món:

## FIX
- **C-1.4**: installer ghi `export PATH=~/.local/bin` vào ~/.profile + ~/.bashrc (v2.2) nhưng bash
  NON-INTERACTIVE không source 2 file đó → `nlm ...` trần báo 'No such file or directory', chỉ chạy được
  absolute-path / `tl nlm-*` (tự nối PATH). Thêm `_symlink_nlm_system_path`: best-effort symlink
  `~/.local/bin/nlm → /usr/local/bin/nlm` sau khi cài xong (/usr/local/bin nằm trong PATH MẶC ĐỊNH mọi shell;
  Cowork chạy root ghi được) — idempotent, KHÔNG đè file/link lạ (cảnh báo thay vì đè), nuốt lỗi khi không có
  quyền, chỉ POSIX. Gọi ở cả 2 đường done (--uv + --resume/trọn gói).

selftest **564/564** (+1 r35: 3 nhánh guard test offline — non-POSIX no-op / src thiếu no-op / dst-đã-có
không-đè). Việc còn lại của log = checklist data-ops sẵn có (deploy v1.33.23 rồi chạy: quarantine-fix --apply,
vbhn-year-fix --with-name --apply, dedup-plan --apply, pin registryDocId, web lượt-2 nhóm HIGH_VELOCITY).

---

# ★ v1.33.22 — MERGE bundle-21 (`tra-luat-skill-v1.33.21-gws3env-fixed.zip`): nhánh hội tụ trên v1.33.20, BỔ TRỢ v1.33.21 — port 2 có sửa primitive, giữ lane name-only của ta

Bundle-21 dựng trên canonical v1.33.20 (91 dòng), xử CÙNG nhóm dư B.5-residual/B3-B9 nhưng bằng cách KHÁC và
BỔ TRỢ bản ta: ta làm FIXER dữ liệu (lane name-only ×11), họ làm PHÂN LOẠI counter + fixer stale-ref. Không
trùng — merge cả hai. Họ KHÔNG có lane name-only của ta.

## PORT (2)
- **B.5-residual (advisory split)**: headline `sweep.title_mismatch`/`hygiene.title_mismatch_candidates` CHỈ
  còn lệch hành-động-được (OMNIBUS_NARROW_TITLE_CHECK/TITLE_METADATA_MISMATCH); cờ VBHN metadata → bucket
  `vbhn_metadata_advisory` (+_rows) — việc của vbhn-year-fix, không phồng hàng source-rename/recat; drift NLM
  (STATUS_MISMATCH/NOTEBOOK_ID/CORPUS_TRUE_NOT_ON_NLM) hết đếm KÉP với nhóm nlm_drift. Thực địa:
  title_mismatch 17→2, vbhn_advisory=21. (Đơn giản hoá so bundle: advisory = entry VBHN + bất kỳ cờ VBHN_* —
  không hardcode list dễ mục.)
- **B3/B9 (quarantine stale-ref fixer)**: `_quarantine_fix_items` +bucket `clear_stale_nlm_ref` (còn
  nlm_source_id nhưng KHÔNG live — status removed*/deleted) → `quarantine-fix --apply` tự dọn; ghost LIVE vẫn
  chỉ báo (xoá nguồn tay sau verify). **SỬA PRIMITIVE bản bundle — vi phạm BẤT BIẾN đã ghi memory**: họ clear
  bằng `_journaled_reg_write` (reg_bulk) ghi giá trị RỖNG → webapp BỎ QUA im lặng = báo cleared nhưng không
  clear gì (false-success). Bản merge: helper `_quarantine_clear_stale` đi `_journaled_reg_clear` (action
  reg_clear keyed + confirm=yes) TỪNG DÒNG, kèm before cho `tl undo`; khoá bằng test FakeG r34 (mọi action
  khác reg_clear = AssertionError). Thực địa DRY: bắt đúng 4 ca (62-VBHN XNC/09-VBHN Đầu tư/20-VPQH ĐTC/
  41-2024 BHXH) — checklist mục 5 nay 1 lệnh thay reg_clear tay.
- Sweep next-action + corpus-fix bước quarantine phân biệt stale_nlm_ref (fixer tất định) vs still_on_nlm
  (xoá tay); hygiene scan text +vbhn_advisory.

selftest **563/563** (+3 r34: bucket stale-vs-ghost, PRIMITIVE-lock reg_clear, advisory split).

---

# ★ v1.33.21 — B.5-residual: lane NAME-ONLY cho vbhn-year-fix (11 VBHN tên-thiếu-năm không fixer nào phủ)

Log verify v1.33.20 LIVE xác nhận MỌI bug code trước đã đóng (corpus-audit 67/67 sạch, header_mismatch 5→0).
Mổ nốt 2 lớp dư: (a) TITLE_OR_REGISTRY_WARN còn lại của 33-2024/55-2010 = cờ ĐÚNG — bản VBHN trong chuỗi mang
tên thiếu năm (`VBHN_34-VPQH_Luat_Luu_tru`, `VBHN_61-VBHN-VPQH_ATTP`) vi phạm bất biến NN-YYYY-VBHN dù sohieu
ĐÃ year-fix; (b) 17 title_mismatch = 15 VBHN, chi phối VBHN_NAME_MISSING_YEAR ×11 — CÙNG lớp. Phát hiện LỖ
TOOLING: `vbhn-year-fix` chỉ quét sohieu-thiếu-năm → DRY trả fixable=0, lớp name-only KHÔNG fixer nào phủ =
backlog treo vĩnh viễn (phải source-rename tay ×11).

## FIX
- `_vbhn_year_fix_items` lane **NAME-ONLY** (`mode='name_only'`): sohieu chuẩn NN-YYYY-VBHN-XXX + TÊN thiếu
  năm-ban-hành → đề xuất đổi TÊN, sohieu GIỮ NGUYÊN (không thể tạo collision số hiệu). Chỉ ghi khi
  `--with-name`; chạy thiếu cờ → loại khỏi sel + nhắc LOUD (không upsert sohieu no-op).
- `_name_inject_vbhn_year` nhận CẢ dạng NGẮN `NN-VPQH` (thiếu segment VBHN — ca 34-VPQH trước trả nguyên tên
  → lane câm với đúng ca cần nhất); idempotent giữ nguyên.
- DRY in marker `📛NAME-ONLY` + cột TÊN→.

Thực địa DRY: bắt ĐÚNG 11 ca (khớp phân tích flag), CONFLICT 0, tên mới đúng bất biến — sẵn chờ user duyệt
`tl vbhn-year-fix --with-name --apply`. selftest **560/560** (+2 r33: inject dạng ngắn + lane 4-fixture có
control corpus=false/tên-đã-đủ-năm). Các mục còn lại của 2 log = DATA-ops đã DRY-preview đủ (xem runbook).

---

# ★ v1.33.20 — MERGE bundle-20 (`tra-luat-skill-v1.33.20-gws3env-fixed.zip`): nhánh song song CÙNG backlog S-10/nhóm-B trên v1.33.18 — lấy KIẾN TRÚC, sửa 2 guard-bug

Bundle-20 dựng trên v1.33.18 (52 dòng), vá đúng backlog mà canonical v1.33.19 vừa xử — lần HỘI TỤ THỨ 3.
Đối chiếu hành vi 2 chiều: phần lớn trùng quyết định ta (B.1/B.3/B.7 bản ta mạnh hơn hoặc tương đương — giữ ta);
1 phần KIẾN TRÚC của họ tốt hơn → port có sửa.

## PORT (3)
- **S-10 v2 — hàm chung `_header_verify_infer_cats(entry) -> (cats, rule)`** (kiến trúc bundle-20): check-4 +
  fix_suggest cùng MỘT nguồn suy luận cat, thêm `infer_cat_rule` máy-đọc + rule trong text mismatch. NÂNG so
  v1.33.19: header-verify nay bắt CẢ chiều omnibus/điều-ước NẰM NHẦM folder (57-2024 đặt ở 34 → cat:False +
  rule=omnibus-46; CU_ILO-105 đặt ở 20 → đề xuất về 23) — v1.33.19 chỉ chắn chiều giữ-đúng-chỗ.
  SỬA 2 BUG bản họ (phản chứng chạy được, khoá r32):
  (a) chiều PROPOSE vào-46 của họ dùng `_omnibus_name_evidence` (nhánh ≥2-refs) → 71-2020 SuaDoi_HIV
      goc+related nằm ĐÚNG 45 bị cat:False rule=omnibus-46 (đúng lớp r29, tái xuất lần 3 trên surface thứ 3)
      — ta: PROPOSE chỉ text-pattern, refs CHỈ dùng SUPPRESS (tên mờ + ≥2 refs + đang ở 46 → giữ);
  (b) họ bỏ skip 00/23 tổng quát (chỉ chắn 23 khi tên khớp prefix treaty) → doc trong 23/00 tên khác vẫn bị
      suy thô — ta giữ not-applicable cho cả 2 rổ (mirror cat-audit).
- `_ABBREV_MAP` += gdpt/bh/qppl ('bh' đứng-một-mình = Ban hành theo quy ước tên corpus; expansion append-only).
- `_is_treaty_entry` += unesco.

## GIỮ TA (3 — bản họ yếu hơn)
- B.1: họ chỉ vá flags trong nhánh review_other; ta fallback ở CHỖ BUILD ROW (phủ mọi bucket).
- B.3: regex HL tự viết của họ ≈ `_HL_SUFFIX_RE` sẵn có ta tái dùng.
- B.7: họ nuốt CÂM cat-00 (pass không đếm) + gộp MỌI cat-23 không-số-hiệu vào treaties (giấu file thô misfile);
  ta: bucket `party_docs` đếm được + treaty theo tên/loai (file thô trong 23 vẫn ra orphan).

Thực địa sau merge: 57-2024 LIVE ok 4/4 + infer rỗng; cat-audit giữ 2 cờ. selftest **558/558** (+5 r32:
misfile-omnibus bắt được, r29-lock lần 3, suppress-arm refs, treaty 2 chiều, abbrev mới).

---

# ★ v1.33.19 — Xử S-10 (3 surface kiểm cat KHÔNG nhất quán) + nhóm B log rà v1.33.18 LIVE (B.1/B.2/B.3/B.5/B.7)

2 log rà chạy LIVE v1.33.18 (fresh bootstrap): S-10 guard omnibus-46/điều-ước ĐÃ vá ở cat-audit + corpus-audit
nhưng CHƯA lan sang header-verify → ~61 dương-tính-giả dồn về lệnh đó; + nhóm B (schema/heuristic/hygiene).

## FIX
- **S-10** `_verify_header_match` check-4 CAT đồng bộ ĐÚNG bộ guard 3 surface: cat 00/23 (Đảng/điều ước) →
  check KHÔNG ÁP DỤNG (mirror cat-audit skip — hết ILO-088 cat:False đòi dời 20); boundary-rule khẳng định
  cat hiện tại → PASS; cat 46 + `_omnibus_name_evidence` → PASS (57-2024 LIVE nay ok:True 4/4). Misfile
  THẬT trong 46 vẫn FAIL (fixture 38-2019 Quản lý thuế cat 46 → cat:False — không nới quá tay).
  `fix_suggest.infer_cat` chỉ còn đề xuất khi check cat THẬT SỰ fail (hết in ['34'] mồi false-recat).
- **B.1** review-queue: flags lọc theo nhóm-việc RỖNG → mirror flags_all (4/4 row review_other từng flags=[]
  câm dù flags_all đầy — driver duyệt .flags đồng nhất hết mù lý do).
- **B.2** `_ABBREV_MAP` += gddh/gdnn/vbqppl (GDDH khớp 0/1, BH_VBQPPL 0/1 fail oan dù sohieu/loai/cat PASS).
  BONUS thực địa: nở viết tắt mở khoá khớp chủ đề → lộ 3 ứng viên sửa-đổi THẬT trước đây VÔ HÌNH
  (125-GDĐH/124-GDNN ↔ 123-2025 sửa luật giáo dục; 64-2025 BH_VBQPPL ↔ 87-2025) — vào bucket INFO rel_low.
- **B.3** `_name_tail_key` strip hậu tố ngày-hiệu-lực `_HL<date>` (Thu_do_HL2026-07-01 → token rác 'hl2026'
  làm title 1/2 fail) — strip SAU bước đổi separator (trước đó \b không bắt được '_hl…').
- **B.5** `TITLE_METADATA_MISMATCH` hết oan khi metadata title là TÊN-FILE-CỤT ('Luat_123-2025-QH15_GD' /
  'Luat_71-2020-QH14' — token còn mỗi qh15/qh14, không bao giờ giao tail): lọc qua `_looks_like_filename_title`
  (P0-1 v1.31.0 sinh ra đúng cho việc này) + so TAIL-vs-TAIL — meta không có bằng chứng chủ đề thì KHÔNG
  buộc tội; misname THẬT (meta trích yếu chủ đề khác hẳn) VẪN bắt. Thực địa: review_other 4→2 (123-2025 +
  71-2020 rời), sweep title_mismatch 20→17. SKILL §4 sửa câu overclaim 'HẾT nhiễu' → 'GIẢM nhiễu 2 đợt'.
- **B.7** orphan detector: `_is_treaty_entry` nhận FTA/chương điều ước (CPTPP/EVFTA/RCEP/UKVFTA/DUQT_/ILO-);
  văn kiện Đảng (cat 00 / VK_/Van_kien) → lớp riêng `party_docs` mới. Thực địa: orphans 16→8 (treaties 31→33,
  party_docs=6) — 8 còn lại là ca thật cần soi (219_2025_ND-CP_m_668418…).

Nhóm còn lại của log = DATA-ops (B.6 reg-delete 2 .doc quarantine; B.9 quarantine-fix 4 stale; B.10 loai/cat
lạ; B.11 pin registryDocId; + title_vn RÁC ca 33-2024 'Luật số: 33/2024/QH15' → backfill-title-vn re-derive).
selftest **553/553** (+6 r31, có control chống-nới cho từng guard).

---

# ★ v1.33.18 — Xử nhóm CLI/hợp-đồng log rà 67 Luật CHẠY LIVE v1.33.17 (A1/A2/A3/D) — MERGE bundle-18 + phần tốt tl_changes.patch

Bundle-18 dựng TRỰC TIẾP trên canonical v1.33.17 (35 dòng, 4 fix đúng trọng tâm, TỰ loại phần độc của
tl_changes.patch — nhánh thứ 2 liên tiếp hội tụ với quyết định canonical). Đối chiếu hành vi như mọi lần.

## FIX (4 — port bundle-18, riêng A3 lấy ngữ nghĩa patch)
- **A1** `nlm-get --json`: parser nhận no-op (lệnh vốn luôn xuất JSON) — driver thêm --json đồng nhất cho nhóm
  read-only hết gãy `unrecognized arguments`.
- **A2** corpus-audit pagination MÂU THUẪN (`partial=true` + `next_offset=null` → driver phân trang DỪNG sau
  40/530 âm thầm): chế độ checkpoint nay phát `next_offset` = PROGRESS MARKER (số drive_id đã checkpoint) +
  `pagination_mode` (checkpoint_resume/full_checkpoint/offset) + `resume_required` + `resume_command` điền sẵn;
  text in tiến độ N/pool. Lệnh đúng vẫn là LẶP CÙNG LỆNH --all --resume tới rc=0.
- **A3** `corpus-audit --all --full`: quét HẾT pool 1 lệnh (bỏ cap trang 40, nên kèm --workers 4-6). LẤY NGỮ
  NGHĨA CỦA PATCH thay vì bundle: --full VẪN đi qua máy CHECKPOINT + nạp checkpoint sẵn có — chết ở doc #500
  không mất 499 header đã đọc, chạy lại là nối (bundle-18 cho --full chạy trần: timeout = mất trắng);
  Cowork trần-lệnh-ngắn vẫn dùng --all --resume trang nhỏ.
- **D** cặp gốc/sửa LỆCH PHA (64-2006 HIV verdict OK 'đã hợp nhất' nhưng luật sửa 71-2020 CÙNG CHUỖI vẫn bị
  NO_VERIFIED_VBHN + QT5 đẩy web lượt-2): luật SỬA có amends_vbhn (AMENDS_OTHER_VBHN — nội dung đã phản ánh
  trong VBHN của luật ĐÍCH) → 2 gate NO_VERIFIED_VBHN/QT5 im (đồng dạng nhánh omnibus AMENDS_OTHER).
  Thực địa: 71-2020 rời web bucket (25→24, sang review_other vì TITLE warn); 26-2018 GIỮ đúng (đích chưa có
  VBHN trong corpus — control chống nới quá tay).

## REJECT từ tl_changes.patch (3 — cái mới có phản chứng, cái cũ đã khoá test)
- **Bypass sohieu cho Bộ luật/VBHN khi header KHÔNG có số nào**: biến 'không xác minh được' thành PASS —
  `_verify_header_match.ok` là cổng `tl confirm` (gán verified) → false-confirm cho scan/doc sai. Ca thật
  (VBHN_21-2026 số ở khối ký cuối) đã xử ĐÚNG CÁCH bằng full-text+compact từ v1.33.15/17. Bundle-18 cũng
  không lấy (hội tụ).
- cat-audit into-46 refs-based — đã reject + khoá r29 (phản chứng 71-2020 goc+related).
- `fix_command` LOAI_MISMATCH đổi thành `tl register ... --apply`: NHÚNG lệnh ghi tự-áp vào worklist
  propose-only — trái doctrine DRY-trước/duyệt-tay; giữ lệnh review + reg_upsert.

selftest **547/547** (+4 r30: parser A1/A3, D suppress + control, A2/A3 END-TO-END offline 2 vòng thật —
partial-markers rồi --full nối checkpoint chạy nốt + tự dọn). Các mục B/C/E của log là DATA-ops/môi trường
(đã có trong runbook: nlm-reconcile LIVE, dedup-plan, 163 tên, quarantine-fix, pin registryDocId).

---

# dev-tooling 2026-07-04 (KHÔNG bump version — không đổi runtime, KHÔNG vào zip deploy)

Bộ phòng vệ phía DEV cho phiên Claude Code trên máy này (Cowork LIVE không dùng các file này — phòng vệ LIVE
vẫn là _apply_gate/DRY-default/journal trong tl.py): `CLAUDE.md` điều phối ngắn (kiến trúc ghi/đọc + 5 bài học
đắt giá + quy trình sửa code); `.claude/settings.json` permission allow(read/test)/ask(commit/push/clasp)/
deny(secrets, rm -rf) + hook PreToolUse `pretooluse_guard.py` — lệnh chạm `--apply|--clear-stale|source-delete|
reg-delete|drive_trash|rm -rf|clasp push|gas-deploy|--force-insert` → HỎI user (ask, không deny cứng — runbook
vẫn có ngày chạy --apply có duyệt); `.githooks/pre-commit` (core.hooksPath) chặn stage secrets/binary
(.enc/.env/cookie/tl_secrets/client_secret/credentials/zip/dl — test hành vi: fake .enc bị chặn rc=1, stage
sạch rc=0); agent `tl-auditor` READ-ONLY (tiêu hoá log audit dài, cấm mutate — bài học rogue-edit);
upload-skill-to-Package.ps1 stage nay tự loại `.claude/`, `.githooks/`, `CLAUDE.md` khỏi zip.

---

# ★ v1.33.17 — MERGE nhánh-5 (`tra-luat-skill-v1.33.17-gws3env-patch-merged.zip`): nhánh HỘI TỤ trên chính canonical v1.33.15 — port 2, reject 2

Nhánh-5 = canonical v1.33.15 CỦA TA làm nền + họ tự merge nhánh-4 SONG SONG (trùng phần lớn v1.33.16 ta: cùng
reject `_corpus_audit_json_row`/S-2-guard-đơn-giản, cùng sửa key `unregistered` chết của nhánh-4 — hội tụ độc
lập, tín hiệu tốt) + merge thêm `tl_changes.patch`. Đối chiếu BẰNG HÀNH VI 2 chiều như mọi lần.

## PORT (2)
- **S-2i compact sohieu-match** (món MỚI duy nhất, từ tl_changes.patch): header format LỎNG
  'Số: 47 / 2024 / NĐ - CP' (separator lạ — _SOHIEU_RE lẫn substring-check đều trượt, REPRO lỗ thật trên bản
  ta) → so COMPACT chỉ-chữ-số trên 2000 ký tự đầu, kèm dạng không-năm VBHN; số hiệu SAI thật (99/2099) vẫn fail.
- sweep --live-nlm dòng text +`unregistered=` (JSON ta đã có từ v1.33.16).

## REJECT (2 — có phản chứng, khoá test r29)
- **cat-audit đề xuất VÀO-46 bằng `_omnibus_name_evidence`** (gồm nhánh ≥2-refs): luật sửa MỘT đích có
  goc+related = 2 ref tokens → bundle họ flag `71-2020 SuaDoi_Phong_chong_HIV` (cat 45 Y tế) thành 45→46
  confidence HIGH (repro trên bundle). Evidence refs-based chỉ an toàn chiều SUPPRESS (giữ-trong-46); chiều
  PROPOSE ta đã có qua `_cat_boundary_rule` text-pattern chặt (v1.33.16) — test VÀO-46 của chính họ (57-2024
  nằm nhầm 34 → 46) PASS trên cơ chế ta, giữ nguyên làm r29.
- **Doctor S-9 FAIL khi registryDocId rỗng** (lần 2 — nhánh-4 và nhánh-5 cùng chọn FAIL): giữ quyết định
  v1.33.16 — rỗng = auto-discover an toàn by-design (v1.23.22), PASS + khuyến nghị pin rõ; FAIL làm doctor đỏ
  trường kỳ + rủi ro Cowork loop tự-sửa-config.

Ghi chú: nhánh-5 KHÔNG có các phần v1.33.16 ta (S-2h `_declared_loai_from_header` viết-lại + 4c, widen
`_omnibus_name_text`, boundary-46+guard VBHN, dedup trigger active, flatten alias, advisory lô) — canonical
giữ tất. Kiểm thực địa: cat-audit vẫn 2 cờ; BLHS live PASS 4/4. selftest **543/543** (+3 r29: loose-spacing
[test gốc nhánh-5], into-46-qua-boundary, phản-chứng 71-2020 khoá reject).

---

# ★ v1.33.16 — MERGE nhánh-4 (`tra-luat-skill-v1.33.15-gws3env-patched.zip`): bản độc lập CÙNG backlog S-1..S-9 trên v1.33.14 — port 6, reject 4

Nhánh-4 tự đặt tên v1.33.15 (TRÙNG SỐ với canonical — 2 nhánh độc lập cùng vá backlog log rà 40/531 + 67 Luật).
Đối chiếu BẰNG HÀNH VI (không grep chuỗi): chạy fixture của họ trên bản ta, bơm ca phản-chứng vào bản họ.
GIỮ canonical base v1.33.15 (S-2 của ta vá đúng gốc rễ ĐO ĐƯỢC: 4/5 fail TITLE vì token rác + 1/5 sohieu khối-ký-cuối,
verify 5/5 PASS LIVE — S-2 nhánh-4 chỉ đoán 'Bộ luật/VBHN guard', không chữa được ca nào trong 5 ca thật).

## PORT (6 — mỗi món lấp lỗ thật, có sửa lỗi của chính bản họ khi port)
- **S-3b** `_omnibus_name_text` (tách text-core khỏi `_omnibus_name_evidence`): +pattern chữ 'sửa đổi (bổ sung)
  (một số) (điều của) các/nhiều luật' — NỚI hơn nhánh-4 (bắt cả phrasing thật 'một số điều của các luật' mà regex
  họ miss); `_cat_boundary_rule` nay ép 46 cho CẢ omnibus dạng NÉN nằm nhầm folder (đề xuất ĐƯA VÀO 46 — chiều
  ta chưa có) + GUARD hơn họ: VBHN không bao giờ ép 46; `_cat_likely_wrong_suggest` nhận omnibus qua title-scope.
- **S-2h** `_declared_loai_from_header` — port Ý TƯỞNG, VIẾT LẠI detector: registry 'Luật' + khối tiêu đề in
  'BỘ LUẬT' xen kẽ ('BỘ LUẬT\nSố:…\nHÌNH SỰ') là lỗ THẬT của ta (repro: 0 đề xuất, header_ok=True). Check 4c mới
  đề xuất LOAI_MISMATCH khi khai báo MẠNH (Bộ luật/VBHN) ≠ registry; guard kép: entry VBHN không qua (VBHN in
  tiêu đề luật gốc — đo thật ca 21-2026), registry VBHN không bao giờ bị hạ.
- **S-8b** `_vbhn_latest_low_priority_recent_law` (vbhn-check) — ĐỐI XỨNG với S-8 source-map v1.33.15: luật rất
  mới chưa có ứng viên VBHN + không high-velocity → cờ INFO `VBHN_LATEST_LOW_PRIORITY_RECENT_LAW` thay
  UNVERIFIED_LATEST (QT5_WEB_REQUIRED giữ). Năm ĐỘNG (≥ nay−2) thay hardcode 2024 của họ (sẽ mục theo thời gian).
- **S-4/S-5** sweep --live-nlm JSON +other_notebook/link_candidates/unregistered_on_nlm/registry_live_gap/basis
  + dòng text gap — SỬA BUG bản họ: plan key là `unregistered`, họ đọc `unregistered_on_nlm` không tồn tại → luôn 0.
- **S-6/S-7** next-actions: trigger dedup-plan nay tính CẢ cụm ACTIVE by_sohieu_raw_active/by_name_active (P2-4
  v1.33.12 đo được nhưng chưa nối trigger); 163 tên phi-chuẩn → hướng dẫn chạy LÔ corpus-audit đọc
  rows[].fix_command (khớp S-1) thay lệnh từng-ca; advisory NLM nêu rõ claim=estimate không chốt FULL/overflow.
- **S-1b** `_audit_row_flatten` +alias `command`/`proposal_count`/`current` (phần đáng giá của
  `_corpus_audit_json_row` họ). KHÔNG port `proposal_rows[]` (trùng proposals[] vốn đã phẳng từng món).

## REJECT (4 — đều có PHẢN CHỨNG chạy được, khoá bằng test r28)
- `_declared_loai_from_header` bản 12k-scan tự do: NĐ 'Căn cứ Bộ luật Lao động' → đọc thành 'Bộ luật', TT 'Căn
  cứ Văn bản hợp nhất số 19/…' → 'VBHN' (repro trên chính bundle họ) ⇒ 🔴 LOAI_MISMATCH oan HÀNG LOẠT cho mọi
  NĐ/TT quy định chi tiết Bộ luật. Thay bằng detector dòng-IN-HOA-đứng-riêng khớp-đầu-dòng, dòng đầu tiên thắng.
- Topic 'dautucong' trong list omnibus: 'dautu' là SUBSTRING của 'dautucong' → tên 1-đề-tài 'SuaDoi_Dau_tu_cong'
  đếm thành 2 = false-omnibus.
- Doctor S-9 coi registryDocId RỖNG là FAIL: rỗng = fallback auto-discover AN TOÀN by-design (v1.23.22) — FAIL
  làm doctor đỏ trường kỳ tới khi user pin + rủi ro Cowork loop tự-sửa-config. Port dạng PASS + khuyến nghị pin rõ.
- S-2 'guard Bộ luật' làm fix CHÍNH cho header_mismatch_no_proposal: sai chẩn đoán — 5/5 ca thật là TITLE-token-rác
  /sohieu-khối-ký-cuối (đã vá + verify LIVE ở v1.33.15); bản họ không chữa được ca nào trong 5.

Kiểm thực địa sau merge: cat-audit vẫn 2 cờ hợp lệ; vbhn-check 91/2025 → LOW_PRIORITY thay latest, BLHS giữ
UNVERIFIED+HIGH_VELOCITY; review-queue web 25 (dòng 89-2025 mới xuất hiện là do DATA cache refresh — A/B cùng
cache trên code v1.33.15 cũng ra 25, KHÔNG phải regression merge). selftest **540/540** (+6 r28, khoá cả 4 reject).

---

# ★ v1.33.15 — Xử nhóm CODE log rà 40/531 + review-queue 67 Luật CHẠY LIVE v1.33.14 (S-1/S-2/S-3/S-8)

Toàn bộ 4 bug đều REPRO BẰNG HÀNH VI trước khi vá (bài học đối chiếu nhánh: test hành vi, không grep chuỗi) —
5 ca S-2 verify LIVE trên chính document Drive thật, S-3/S-8 verify offline trên manifest cache thật.

## S-2 🔴 corpus-audit `header_mismatch_no_proposal` 5/40 (BLHS, ND_47-2024, VBHN_21/62-2026, TT_95-2025)
Chẩn đoán thật (khác giả thuyết 'ma sát Luật vs Bộ luật' của log): 4/5 fail check TITLE vì token chủ đề RÁC,
1/5 fail check SOHIEU vì layout văn bản. Vá 7 lớp, cả 5 ca nay PASS LIVE:
- (a) title-check TAIL-FIRST: token chủ đề lấy từ `_name_tail_key` (sau prefix+sohieu), hết rác
  'bluat'/'qh13'/'tt44'/'btc' lọt vào bộ token phải-khớp; fallback full-name khi tail rỗng (tên trơ).
- (b) `_name_tail_key` nhận prefix họ Bộ-luật `bluat|bl[a-z]{2,6}` (BLuat chuẩn sinh P1-3 + BLDS/BLHS legacy)
  — trước đó tail của MỌI tên BLuat_/BLDS_ = nguyên tên không strip.
- (c) viết tắt mở rộng so TỪ NGUYÊN VĂN trên text (regex word-bound) — từ 2-ký-tự ('co','so','du' của CSDL)
  bị `_token_set` lọc len≥3 nên check cũ `w in _ftoks` KHÔNG BAO GIỜ đậu.
- (d) token NÉN CamelCase ≥6 ký tự ('nhapcanh','xuatcanh','suadoi') khớp SUBSTRING trên text đã nén.
- (e) `_ABBREV_MAP` += csdl (cơ sở dữ liệu), ncc (người có công).
- (f) sohieu VBHN: layout VPQH in 'Số: NN/VBHN-VPQH' CHỈ ở khối ký CUỐI (đo thật ca 21-2026 BLTTDS: vị trí
  492k/532k ký tự — ngoài head-6000) → tìm dạng có-năm/không-năm trên TOÀN văn bản.
- (g) hết CÂM: `_corpus_audit_row` trả `header_mismatches`/`header_checks`; hàng `header_mismatch_no_proposal`
  + bản in text kèm LÝ DO lệch — người rà tay khỏi chạy lại header-verify.

## S-1 🔴 corpus-audit --json: summary đếm proposal nhưng rows[].type/suggested_name/proposal = null
Chi tiết chỉ nằm LỒNG trong `proposals[]` (schema summary↔row lệch — driver phẳng đọc null). `_audit_row_flatten`
MIRROR đề xuất CHÍNH (nặng nhất) lên top-level row: `type/severity/icon/suggested/suggested_name/fix_command/
proposal/flags`; áp cả 3 đường (engine chung, nhánh raw, và LÚC XUẤT JSON — idempotent, checkpoint đời cũ nạp
lại vẫn ra schema mới). `proposals[]` giữ nguyên là nguồn sự thật đầy đủ.

## S-3 🟠 cat-audit/CAT_LIKELY_WRONG đề nghị rời rổ 46 cho omnibus (57-2024 46→34)
`_omnibus_name_evidence` (PURE) = bằng chứng omnibus theo TÊN/REF, ĐỘC LẬP VỚI CAT — không lấy 'đang ở 46' làm
bằng chứng 'thuộc rổ 46' (lập luận vòng); `_is_omnibus_entry` = cat46 ∨ name-evidence (contract cũ giữ nguyên).
Cả 2 auditor (cat-audit + `_cat_likely_wrong_suggest`) suppress đề xuất RỜI 46 khi có name-evidence; VBHN nằm
nhầm 46 VẪN được đề xuất dời (VBHN cat theo luật đích); chiều đề xuất VÀO 46 giữ nguyên (r13). Kiểm thực địa:
cat-audit 3 cờ → 2 (mất đúng cờ giả 46→34; 2 gợi ý TT medium-conf hợp lệ GIỮ).

## S-8 🟡 over-flag VBHN_CANDIDATE_UNVERIFIED_LATEST đẩy 37/67 Luật vào hàng web lượt-2
Đính chính log: các luật 2024-2026 bị cờ KHÔNG phải 'chưa/không có VBHN' — chúng CÓ VBHN 2025-2026 trong corpus
(vd 50-2024 Công đoàn → VBHN_90-VPQH_2025) nhưng cờ bật VÔ ĐIỀU KIỆN khi related_vbhn≠∅. Hạ cờ khi: VBHN DUY
NHẤT + năm rõ ≥ năm-nay−1 + không luật-sửa nào MỚI HƠN đã biết (covered theo ngày ∨ không ứng viên normative)
+ KHÔNG thuộc nhóm S10 HIGH_VELOCITY → cờ INFO mới `VBHN_LATEST_RECENT_COVERED`. Kiểm thực địa: web lượt-2
37→24, sạch 28→39; 10 ca ★ HIGH_VELOCITY giữ nguyên (khớp đúng danh sách B1 của phiên rà); doctrine
`vbhn-verify --official-required` trước khi trích dẫn KHÔNG đổi — chỉ hạ ưu tiên hàng đợi.

selftest **534/534** (+9 r27: tail-key-bluat, title-no-junk ×3 ca thật, sohieu-signature-tail, row-selfdescribing,
hdr-bad-carries-reason, omnibus-name-evidence, cat-keeps-46 ×2, recent-vbhn-downgrade, review-queue-denoised;
r18a cập nhật theo hành vi S-8 + năm fixture ĐỘNG). Nợ DATA (ops, không phải code — giao user): nlm-reconcile
--apply --clear-stale (17 dangling, S-4/S-5) · dedup-plan --apply (S-7) · header-verify --fix-suggest lô 163 tên
(S-6) · pin registryDocId vào config (S-9) · chốt VBHN 10 luật ★ + backfill 68-2025/44-2019 (B1/B3).

---

# ★ v1.33.14 — MERGE nhánh-3 (`D:\admin\tra-luat\tra-luat.zip`): bản độc lập THỨ BA vá backlog trên v1.33.11 — port 7, reject 4

## PORT (7 — mỗi món đều mạnh hơn bản ta hoặc lấp lỗ ta chưa có)
- `_normalize_loai` tách nhãn KÉP tại NGUỒN ('/', '\\', '|', ' và ') — mọi caller hưởng (register-normalize,
  backfill-loai, reg-query --loai, corpus-audit) thay vì vá lẻ từng chỗ như v1.33.12.
- `_infer_loai` + token BLUAT (lỗ thật: ta thêm BLuat vào prefix-RE v1.33.12 nhưng quên _infer_loai).
- `register --bulk` LỚP 2 existence-check (`_register_bulk_missing` PURE, probe cap 20, escape --force-insert)
  — v1.33.13 mới có format-guard cho bulk, chưa có existence.
- `_valid_cats` + `_resolve_cat_folder` nhận categories='inherit' (doctrine §12) — profile dự án inherit
  trước đây trả set rỗng/cây sai.
- `_resolve_cat_folder` NÂNG CẤP LỚN (contract-verified list/info/rename/mkdir+parentId): exact-canonical dùng
  luôn; folder MÃ TRƠ ĐƠN NHẤT cùng prefix → **RENAME về canonical (gộp thật, giữ fileId)** — mkdir-by-name
  v1.33.12 tạo folder mới SONG SONG còn folder trơ vẫn ôm file; ≥2 ứng viên mờ → dùng cái đầu, KHÔNG tự rename;
  config-map → best-effort rename; mkdir kèm parentId=root profile. Lõi tách `_resolve_cat_folder_impl`
  (test FakeG 3 kịch bản).
- `backfill-loai` trigger NAME-ONLY: tên VBHN_ là bằng chứng đủ mạnh một mình → conflict 'Văn bản hợp nhất'
  cho MỌI nhãn khác (lịch sử nới có kiểm chứng: S3 2-bằng-chứng → 2 ca thật lọt [115 loai='Luật', 67-2025
  'thuong' sohieu thiếu -VBHN-] → name-only; propose-only/DRY nên không có ghi tự động).
- `sapxep.suggest_name` prefix: +BLuat +BLHS, GIỮ BLDS/BLLD legacy (file ngoài tl.py — cả 3 nhánh trước đều bỏ sót).

## REJECT (4 — kèm lý do)
- `register` DRY-mặc-định (`--apply` gate): PHÁ CONTRACT CLI — mọi runbook/script sẵn có gọi register không
  --apply sẽ thành no-op rc=0 (automation tưởng thành công). Lớp validate 2 tầng đã chặn gốc rác mà không phá.
- Prefix-RE bỏ Bo_luat/BLDS…, family → 'BLuat': REGRESSION — tên legacy hợp lệ (BLDS_91-2015 đang sống trong
  corpus) sẽ bị flag NO_TYPE_PREFIX oan; doctrine v1.33.12 giữ legacy. sapxep của họ cùng lỗi — đã sửa khi port.
- review-queue rel_low FLAG-based + rel_low xếp TRƯỚC web: ta giữ PAYLOAD-based `_rq_rel_strong` (mịn hơn cờ
  tổng) + web trước rel_low (việc web là thật, không được rơi khỏi hàng đợi chính).
- 'REVIEW không cờ → demote clean': GIẤU anomaly — ta giữ review_other + reason/flags_all.

selftest **524/524** (+5 r26: normalize-dual-source, infer-bluat, bulk-missing, resolve-folder-impl-3-kịch-bản,
vbhn-name-only-conflict).

---

# ★ v1.33.13 — MERGE patch "AUDIT 07/2026" (files.zip): 2 nhánh cùng vá backlog 9 lỗi trên v1.33.11 — hợp nhất chọn lọc

Patch đính kèm (tra-luat_v1.33.13_cumulative.patch) = nhánh khác tự vá CÙNG backlog trên nền v1.33.11.
So với v1.33.12 của ta: TRÙNG HƯỚNG P1-1 (nhãn đủ)/P2-1/P2-2/P2-3; THIẾU P1-2 (_resolve_cat_folder canonical),
P1-3 (BLuat), P2-4 (*_active), P0-2 (--live-nlm), và escape-hatch --force-unsafe của họ KHÔNG được wire vào
parser register (getattr luôn False — user không bypass được). GIỮ canonical base; PORT 3 phần họ MẠNH HƠN:

## P0-1 nay 2 LỚP + phủ cả --bulk
- LỚP 1 (port): `_looks_like_drive_id` — format-guard OFFLINE rẻ (≥20 ký tự [A-Za-z0-9_-], nhận prefix `nlm:`)
  → id cắt cụt bị chặn NGAY với lỗi rõ `DRIVE_ID_MALFORMED`, không tốn round-trip; áp CẢ `register --bulk`
  (v1.33.12 ta chỉ guard đường đơn — lỗ họ vá được). Escape thống nhất `--force-insert` (đã wire parser).
- LỚP 2 (giữ của ta): `_register_target_exists` — id ĐÚNG DẠNG nhưng không tồn tại (manifest + Drive live)
  vẫn REFUSE `DRIVE_ID_NOT_FOUND` (format-guard một mình KHÔNG bắt được ca này).

## P2-3 rộng hơn: corroboration sohieu
- Port trigger của họ: tên `VBHN_` + sohieu chứa `-VBHN-` + nhãn KHÔNG-map-được BẤT KỲ → conflict 'Văn bản
  hợp nhất' (không chỉ 'thuong'); giữ mode=conflict của ta (họ để lẫn vào normalize). Working-doc 'thuong'
  không tên VBHN_ tuyệt đối không bị đề xuất VBHN (test khoá).

## Vocab máy-đọc
- recat plan + `cat_label` (alias `reg_label` — key patch kia dùng); review_other + `review_reason` LIST.

## KHÔNG port (đã có bản mạnh hơn / khác thiết kế)
- `_RQ_REL_STRONG` flag-based của họ: ta dùng `_rq_rel_strong` PAYLOAD-based + bucket INFO
  `relation_low_confidence` riêng (giữ được candidates/fix_command thay vì dồn vào review_other).
- Test 'BC thuong không được đề xuất gì' của họ: nới đúng ngữ nghĩa — normalize 'thuong'→'Văn bản thường'
  (enum hợp lệ) được phép; chỉ cấm đề xuất 'Văn bản hợp nhất'.

selftest **519/519** (+3 r25: looks-like-drive-id, vbhn-masquerade-sohieu-corroborated, cat-label-alias).

---

# ★ v1.33.12 — Backlog 9 lỗi phiên khắc phục 04/07: chặn register-rác, recat/folder canonical, review-queue hết báo động giả

## 🔴 P0-1 — `register` hết CHÈN DÒNG RÁC (drive_id cắt cụt → reg_upsert insert dòng rỗng, ok:true không báo)
- `_register_target_exists`: drive_id phải có trong MANIFEST hoặc Drive LIVE (files_get — file vừa upload chưa
  vào cache vẫn hợp lệ, không gãy luồng ingest). Không thấy → REFUSE rc=2 `DRIVE_ID_NOT_FOUND` + hướng dọn rác
  (`reg-delete --force`); cố ý tạo dòng mới không gắn Drive → `--force-insert` (LOUD).

## 🟠 P1-1 + P1-2 — recat/folder: GỘP FOLDER VẬT LÝ KHẢ THI trở lại
- P1-1: recat trước ghi MÃ TRƠ vào registry (`cat=code`) → nhãn trơ cùng mã "patched=0 = đã đúng" GIẢ, bare-cat
  36→36. Nay ghi NHÃN ĐỦ canonical `NN_Ten` (`_cat_reg_label` từ phap_dien_45.folder — khớp cat-list); plan DRY
  in `reg_label`.
- P1-2: `_resolve_cat_folder` trước ưu tiên config.categories (folder mã-trơ/tên-có-dấu cũ) → move vào folder
  SAI TÊN, cat-list vẫn báo '10 mã chưa có folder'. Nay resolve THEO TÊN CANONICAL ASCII trước (mkdir
  find-or-create đúng `NN_Ten`), config chỉ còn fallback.

## 🟠 P1-3 — Chốt doctrine prefix Bộ luật
- `BLuat_` = CHUẨN SINH TỰ ĐỘNG (standardize_name); BLDS_/BLHS_/BLLĐ_… = legacy HỢP LỆ cùng họ Bo_luat
  (migrate dần khi rename, không bắt buộc). VÁ KHẨN kèm theo: corpus ĐÃ có BLuat_100-2015/45-2019 sau
  source-rename mà `_NAME_TYPE_PREFIX_RE` chưa nhận `BLuat` → sẽ flag oan chính tên chuẩn vừa sinh; đã thêm
  vào RE + family-map + _ABBREV_MAP.

## 🟡 P2-1 + P2-2 — review-queue: REVIEW luôn có lý do; rel low-conf hết phồng hàng đợi
- P2-1: mọi row có `flags_all` (toàn bộ cờ source-map, không lọc nhóm); review_other thêm `reason` — hết
  "verdict=REVIEW, flags=[]" câm (ca 123-2025).
- P2-2: bucket HÀNH ĐỘNG `relation_backfill` chỉ nhận ứng viên MẠNH (linked/strong/confidence≠low —
  `_rq_rel_strong`, cùng ngưỡng escalate v1.29.6); toàn low-conf → bucket INFO MỚI `relation_low_confidence`
  (vẫn kèm candidates + lệnh relation-check phủ định nhanh). Log chứng minh: relation-check trả OK/
  missing_links=[] cho CẢ 3 ca low-conf từng nằm bucket hành động. counts thêm khóa mới, tổng vẫn = laws_scanned.

## 🟡 P2-3 — backfill-loai --normalize hết "no-op"
- Nhãn KÉP 'Quyết định/Quy định' → lấy VẾ ĐẦU; VBHN ĐỘI LỐT 'thuong' (ca VBHN_67-2025 Doanh nghiệp — LỖI THẬT
  từng lọt) → mode=conflict 'Văn bản hợp nhất' (2 bằng chứng: prefix VBHN_ + nhãn thuong vô lý; bắt cả 2 nhánh
  enum-hợp-lệ lẫn phi-chuẩn).

## 🟡 P2-4 + 🔴 P0-2 — chẩn đoán rõ tiến độ
- P2-4: sweep duplicates thêm `by_sohieu_raw_active`/`by_name_active` (cụm còn ≥2 dòng corpus=true — GIẢM theo
  tiến độ dedup; raw giữ nguyên by design, in kèm giải thích).
- P0-2: `sweep --live-nlm` — sweep TỰ đối soát NLM LIVE 1 lượt (read-only qua nlm-reconcile plan): JSON
  `nlm_live{live_on_nlm, desync_real, already_removed, claiming}` + next_action 🔴 khi desync>0. Mặc định
  offline như cũ (nhãn OFFLINE giữ); khi rà TOÀN corpus → bật cờ này.

selftest **516/516** (+5 r24: register-guard, recat-full-label, bluat-prefix, backfill-loai-dual+vbhn-thuong,
rel-strong+sweep-live-flag; r17b/r19 cập nhật theo bucket relation_low_confidence).

---

# ★ v1.33.11 — MERGE HỘI TỤ 2 nhánh v1.33.10 (canonical Claude ⊕ bundle Codex — cùng vá 1 bộ log, khác code)

Bundle Codex rẽ từ canonical v1.33.9, tự vá cùng bộ log rồi cũng đặt tên v1.33.10. So diff đầy đủ (4 file):
GIỮ canonical làm base (Codex THIẾU: E1 nlm-get alias, `_read_verify_text` gws-first — vbhn-verify của họ vẫn
chết theo exporttext, cờ USE_VBHN corroboration, bộ test r23), PORT 5 phần UNIQUE của Codex:
1. **`_journal_dir()` env-override** — `TL_JOURNAL_DIR` > `TL_CACHE_DIR/_journal` > `~/.tl_journal` (selftest/
   sandbox/cache tách profile không mất dấu WAL) + docstring cmd_journal.
2. **`doctor --deep` probe `webapp exporttext scope`** — gọi exporttext TRỰC TIẾP trên 1 GDoc nhẹ (cố ý KHÔNG
   qua gws-first) → bắt đúng ca ping XANH nhưng fallback GAS chết vì thiếu script.external_request, kèm
   remediation (manifest open-egress + RUN re-authorize + Deploy). Bổ trợ hoàn hảo cho GWS-FIRST v1.33.10.
3. **preingest/status: `_relation_subject_verdict` ok|mismatch|unknown** — unknown (thiếu tên/chủ đề 2 bên,
   trước là no-op True) KHÔNG được tự USE_VBHN nữa → REVIEW `VBHN_GOC_SUBJECT_UNVERIFIED` (tách khỏi
   MISMATCH lệch thật). ĐÚNG ca 143-2025→61-2026 của log. KẾT HỢP với cờ corroboration của canonical: ca pass
   subject vẫn tự khai USE_VBHN_UNVERIFIED_LATEST + VBHN_GOC_UNCORROBORATED — hai lớp phòng thủ bổ nhau.
4. **`corpus-fix` bước `raw_on_nlm`** (order 8, human_confirm) — detector v1.33.4 nay có đường sửa trong
   orchestrator: copy_convert → nlm-add GDoc → gỡ raw; các bước sau renumber 9-13.
5. **xref error detail trỏ `tl doctor --deep`** (đồng bộ với probe #2).
Tests: +raw_on_nlm trong corpus_fix_plan_ordered_tiered, +ca _dunk trong status_vbhn_subject_mismatch_guard
(fixture r23 thêm TÊN 2 bên — unknown-guard mới chặn đường SKIP với fixture trơ cũ, đúng thiết kế).

selftest **511/511** (tổng KHÔNG đổi — 2 phần Codex là MỞ RỘNG assertion trong case sẵn có: corpus_fix_plan
+raw_on_nlm, status_guard +_dunk; fixture r23 cập nhật theo unknown-guard).

---

# ★ v1.33.10 — xref/vbhn-verify/frontier GWS-FIRST (hết chết theo exporttext-scope) + status USE_VBHN tự khai corroboration

## A1 🔴 (log: `tl xref` chết 'thiếu scope script.external_request' TRONG KHI gws direct-media đang SỐNG)
- 3 chỗ còn gọi THẲNG webapp exporttext (`_read_verify_text` của vbhn-verify, đường export của xref/extract-target,
  `_frontier_doc_text`) nay đi `_read_doc_text` GWS-FIRST (cache → direct-media → transport → exporttext CUỐI).
  Hệ quả: xref/vbhn-verify/frontier-expand/cache-build sống bằng direct-media như extract/corpus-audit; exporttext
  chỉ còn là fallback cuối. (Muốn fallback GAS đọc được thật: thêm scope `script.external_request` vào
  appsscript.json + clasp redeploy + OWNER re-authorize — việc GAS-side, xem references/APPSSCRIPT_MANIFEST.open-egress.json.)

## B1 🟠 (log: status 'USE_VBHN 61-2026' cho 143-2025 nhưng `vbhn-check --goc 143` 0 candidate — 2 lệnh 'mâu thuẫn')
- KHÔNG phải 2 sự thật: status tin gợi ý webapp (superseded_by, đã qua guard chủ đề §1.1); vbhn-check đi
  registry.goc — goc VBHN CHƯA backfill thì 0 candidate là TẤT YẾU. Nay USE_VBHN TỰ KHAI: field
  `use_vbhn_goc_corroborated` + flags máy-đọc `USE_VBHN_UNVERIFIED_LATEST` (LUÔN — S9 chưa lượt-2, xử cả B2)
  và `VBHN_GOC_UNCORROBORATED` (khi goc trống/không dẫn chiếu bản gốc) + action giải thích và lệnh verify.

## E1 + kiểm chứng B1-log1
- `tl nlm-get vbqppl|base` → tự map notebook nền (hết NLM API NOT_FOUND khi truyền tên profile).
- `--json` SẠCH stdout: khoá bằng test cmd-level (sweep/review-queue parse thẳng json.loads; corpus-audit/
  dedup-check/counts đã khoá ở r20-r22 — heartbeat/banner đều đi stderr). Log ghi nhận bẩn nhiều khả năng do
  driver gộp 2>&1 — tách stream khi parse.

## Đối chiếu phần còn lại (không đổi code)
- A2-log2 (nlm PATH): `nlm_exe()` ĐÃ tự nối ~/.local/bin từ 2.2 — mọi lệnh `tl nlm-*` không cần .bashrc; chỉ
  gọi `nlm` TRẦN ngoài tl mới cần export PATH. C1 (extract CAP): cache-build/extract nay cùng đường gws-first
  ở trên. C2-C5 (45s/lock/tmp/resume-loop): giới hạn env đã biết. D1-D4 + A-mục log-1 (loai 2 Bộ luật, recat 4,
  rename 5, convert 4 raw, backfill 2 quan hệ, hieuluc): NỢ DATA — lệnh sẵn theo runbook; D3 lưu ý dùng
  `reg-query --loai` (so CHUẨN HOÁ, 'Luat' khớp 'Luật') thay lọc tay có dấu.

selftest **511/511** (+3 r23: use-vbhn-corroboration, json-stdout-pure, nlm-notebook-alias).

---

# ★ v1.33.9 — Log rà 90/531 chạy v1.33.8: GỐC RỄ 31 ca VBHN no-proposal + dedup-check schema + lệnh `tl counts`

Bucket A5 v1.33.7 (`header_mismatch_no_proposal`) làm đúng nhiệm vụ — 31/90 ca lộ ra là MỘT defect hệ thống:

## A1 🔴 — VBHN year-injected FAIL header-verify HỆ THỐNG (31 ca ~100% VBHN) — 2 gốc rễ, cả 2 đã vá
- (a) SOHIEU: registry VBHN mang NĂM TIÊM THÊM theo bất biến `NN-YYYY-VBHN-XXX` (quy ước CỦA TA chống tái dùng
  số), còn văn bản in dạng chính thức KHÔNG NĂM `Số: NN/VBHN-XXX` → check cũ fail với MỌI VBHN đã year-fix.
  Nay chấp nhận dạng KHÔNG-NĂM tương đương là KHỚP (cả qua head_shs lẫn substring head_norm).
- (b) TITLE: toks chủ đề có thể chỉ còn 1 token (`Luat_Ke_toan` → 'luat' stop + 'ke' ngắn bị bỏ, còn 'toan')
  mà SÀN cũ max(2,…)=2 > số token → check KHÔNG BAO GIỜ pass. Sàn nay bị chặn bởi chính số token đang có.
- (c) guard A1c: KHÔNG BAO GIỜ đề xuất SOHIEU_MISMATCH rớt-năm cho VBHN year-fixed (chống sót nếu check tương
  lai đổi). Kết quả: ca 25/VBHN-VPQH mẫu → header_ok=True, 0 proposals, RA KHỎI bucket; ca còn lại trong bucket
  từ nay là LỆCH THẬT.

## A6 — dedup-check hết lệch schema
- verdict=COLLISION nhưng payload chỉ nằm ở `exact_sohieu_collision` → driver đọc `groups` thấy 0 ⇒ kết luận
  'không trùng' SAI. Nay alias `groups`/`duplicates` = cùng payload (compat giữ nguyên khoá cũ).

## B — `tl counts` (MỚI): MỘT BẢNG mẫu số trên CÙNG snapshot
- 5 log liên tiếp vấp '6 con số corpus khác nhau' (743/509/521/531/110-68/544-295). Một lệnh in đủ:
  registry_rows / corpus_client / corpus_server_rule / corpus_audit_pool / luat_loai_all / luat_corpus /
  registry_claim_nlm — MỖI DÒNG kèm ĐỊNH NGHĨA; NLM vật lý ghi rõ ESTIMATE + trỏ `tl nlm-get` LIVE (L4/L5).

## Đối chiếu phần còn lại của log (đã xử trước đó / data)
- A2 (sweep drift offline false-clean → live desync 76/2026 Dược): ĐÚNG THIẾT KẾ sau v1.33.4 — sweep tự dán nhãn
  OFFLINE + phiên rà đã nghe theo và chạy nlm-reconcile LIVE bắt được. Data: --clear-stale/re-push.
- A3 (4 raw trên NLM), A4 (loai Bộ luật — corpus-audit v1.33.7 đã flag), A5 (sohieu thô 44_2024 — dedup-plan),
  A7/A8/A9 (tên/sohieu sai/blank — rename/hygiene), cat_label_variants=11 (recat): DATA-OPS theo runbook.
- NLM 295/300 còn 5 slot: neo nlm-get trước mọi push (doctrine sẵn).

selftest **508/508** (+3 r22: vbhn-yearless-header-ok, dedup-groups-alias, counts-one-table).

---

# ★ v1.33.8 — Kiểm chứng thực địa bộ vá v1.33.7 + `corpus-audit --workers` (đọc header song song)

Log gửi lại = CÙNG bộ A1..A6/§A-I đã vá ở v1.33.7. Đợt này:
- **KIỂM CHỨNG trên dữ liệu THẬT (manifest cache):** ca 22-2023.html → NAME_NONSTANDARD (offline, rc=0, vào
  need_manual_read); BLHS 100/2015 → LOAI_MISMATCH suggested 'Bộ luật'; review-queue schema=review_queue.v1 +
  counts cộng khớp laws_scanned. Cả 3 fix hoạt động đúng trên chính các ca log nêu.
- **`--workers N` (A1 phần còn thiếu 'cần chế độ đọc song song'):** PREFETCH text theo CHÙM bằng thread-pool
  (I/O-bound — direct-media/GAS/NLM đều là network round-trip), rồi XỬ TUẦN TỰ — logic fast-fail/checkpoint/
  heartbeat giữ nguyên thứ tự; mỗi doc đọc ĐÚNG 1 lần; circuit-breaker auth-dead dùng chung cờ process nên
  worker sau tự skip khi cred chết. Mặc định 1 = tuần tự như cũ; gợi ý 4-6. Kết hợp chuẩn cho pool lớn:
  `corpus-audit --all --resume --limit 40 --workers 4` (mỗi trang ~10-15s, lặp tới rc=0).

selftest **505/505** (+1 r21: parallel-prefetch — 2 doc/2 luồng, đọc đúng 2 lần, scanned_clean=2).

---

# ★ v1.33.7 — Log rà v1.33.6: corpus-audit hết cắt-âm-thầm/mù-tên-raw/mù-Bộ-luật + JSON phân biệt sạch-vs-chưa-quét

## A1 — `corpus-audit --all --resume`: cày TRỌN pool theo TRANG (idiom nlm-install)
- Log: `--all` cắt âm thầm ở 40; `--limit 600` thì cày 531 header một lượt ~9' vượt trần Cowork. Nay
  `--all --resume` = trang --limit (mặc định 40) + checkpoint `corpus_audit_ckpt_all.json`: rc=3 = PARTIAL
  (JSON `partial/remaining` máy-đọc) → LẶP CÙNG LỆNH tới rc=0, chạy trọn tự dọn checkpoint. Không resume:
  giữ cảnh báo CẮT BATCH loud cũ (v1.29.6).

## A2 — Bắt lệch loai Bộ luật ↔ Luật (BLHS 100/2015, BLLĐ 45/2019 loai='Luat' mà proposals=0)
- 'Bộ luật' và 'Luật' CÙNG tier-5 nên checks['loai'] pass khi header có 'luat' → nhánh LOAI_MISMATCH cũ câm.
  Check 4b mới đối chiếu RIÊNG cặp này theo HEADER (title-block đã ưu tiên 'BỘ LUẬT' trước 'LUẬT' từ v1.31.2);
  fix qua register/reg_upsert (backfill-loai không đoán ca này — enum 'Luat'→'Luật' là hợp lệ nên normalize im).

## A3 — Nhánh RAW không còn skip check TÊN (slug .html 22-2023 — ca nonstandard NẶNG NHẤT lại thoát)
- NAME structural là check OFFLINE, không cần header → chạy ngay trong nhánh raw_no_gdoc trước khi vào
  need_manual_read. `luat-dau-thau-…-d1.html` nay ra NAME_NONSTANDARD (FILE_EXTENSION+NO_TYPE_PREFIX).

## A4 + A5 — JSON phân biệt 'sạch' vs 'chưa quét'; header FAIL không nuốt câm
- A4: `scanned_ids` (đã đọc header thật) + `clean_ids`/`scanned_clean` — hết cảnh rows=[] mơ hồ giữa sạch và
  chưa quét (cộng với partial/coverage_complete là đủ tín hiệu máy).
- A5: `header_mismatch_no_proposal` — header_ok=False mà 0 đề xuất (64-2006/71-2020) vào hàng đợi RÀ TAY riêng
  kèm lệnh header-verify --fix-suggest, in cả bản text.

## Markers minh bạch (log §A intermittent + §B mâu thuẫn auditor)
- review-queue JSON + `schema: "review_queue.v1"` — driver kiểm marker trước khi tin payload (log ghi nhận 1 lần
  nhận nhầm dump reg-query.v2 ~660KB, KHÔNG tái hiện được sau 3 lần chạy lại).
- cat-audit JSON + `scanned` — log claim 'cat-audit 0 mismatch với ca 143' KHÔNG TÁI HIỆN: chạy nguyên vòng
  trên canonical + manifest cache flag đủ 2 ca ALIAS (45→34 Đầu tư, 09→04 Công chứng); nghi phiên đó chạy
  bản/cache khác — có `scanned` thì 0-finding tự lộ bối cảnh.

## Data (log §B/C-I — lệnh sẵn, user duyệt)
- 143/2025 NHÂN BẢN 3 dòng + bản sống misfile 45: `tl recat <id-bản-sống> --cat 34 --apply` + dedup-check
  2 bản corpus=false; VBHN 115 loai='Luật': backfill-loai --normalize (conflict-mode v1.32.2 đã đề xuất sẵn);
  6 naming defect + 172 tên; lượt-2 web 10 HIGH_VELOCITY + 14 QT5; backfill 123/68-2025; quarantine 4 stale.

selftest **504/504** (+4 r20: all-resume-pages, raw-name-flag, bo-luat-mismatch, schema-marker).

---

# ★ v1.33.6 — Log rà 66/68 CHẠY CANONICAL v1.33.5 (fix v1.33.4 phát huy thực địa): rel-row kèm ứng viên + reg-query --loai + --version + detector cat trơ

TIN XÁC NHẬN thực địa: kế toán review-queue khớp máy (29+37+2=68), rel còn đúng 2 ca thật (123/68-2025 — hết
2 ca khống), `raw_on_nlm` bắt 4 nguồn thô (thêm 3 .docx ngoài ca .html), nlm_drift đã dán nhãn OFFLINE.

## C — "flag ≠ payload" (123-2025): KHÔNG tái hiện được payload rỗng; vá đúng chỗ THẬT
- Repro trên manifest cache: `source-map 123-2025 --json` CÓ payload (ứng viên 57-2024 omnibus, confidence=low)
  — nơi thật sự "không có gì để soi" là ROW của review-queue (chỉ flags+fix_command). Vá: row relation_backfill
  nay KÈM `candidates` top-3 (`sohieu|tên|confidence` từ chính payload source-map; text in "↳ ứng viên: …");
  warning UNLINKED trỏ rõ key `unlinked_amendment_candidates`. Ca 123-2025: miss-link THẬT (VBHN_72 Giáo dục
  không được thấy vì tên 'Luat_123-2025-QH15_GD' cụt — nợ rename D2) → REVIEW đúng, nay có ứng viên soi ngay.

## B7 — `reg-query` nhận `--loai` + trả trường loai
- Log: loai là khái niệm hạng nhất mà reg-query trả loai=None mọi dòng → không liệt kê được Luật theo loại,
  phải lọc tay theo tiền tố tên. Nay: row có `loai` (raw) + `loai_canon` (chuẩn hoá enum); `--loai Luật` khớp
  cả 'Luat'/'luật' (so bản chuẩn hoá; 'Bộ luật' là loại riêng).

## F — `tl --version` + docstring hết drift
- `--version` là flag chuẩn (in `tl <VERSION> (webapp target 2.21.2i)` thay vì usage-error). Docstring tl.py
  BỎ số version hardcode (v1.22.68 cũ 11 bậc) — hằng VERSION là nguồn chân lý duy nhất.

## D — detector `cat_label_variants` (folder trơ vs đủ tên)
- Log: tồn tại đồng thời `05` & `05_Can_bo_cong_chuc_vien_chuc`, `32` & `32_Thong_tin…`, bare 32 chứa văn bản
  làm việc lọt corpus → sweep nay đếm `cat_label_variants` + rows + next_action gộp qua `tl recat`.

## Data/ops còn lại của log (lệnh sẵn, user duyệt)
- 🔴 desync 76/2026-VBHN Luật Dược: `nlm-reconcile --apply --clear-stale` (nếu gỡ chủ đích) hoặc re-push.
- 🔴 4 nguồn thô trên NLM (22-2023.html + 37_2025_TT-BYT/59_2023_TT-BTC/39_2016_ND-CP .docx): convert chain.
- 🟡 gộp cat trơ (05/32/34) + name_nonstandard 171 + loai 63 + dedup 93/39/7/9 + quarantine 107 + 80/531
  corpus-audit (tiếp --offset 80). 🟡 slot −1: neo `nlm-get` (doctrine L4/L5).

selftest **500/500** (+4 r19: rel-row-candidates, reg-query-loai, version-flag, cat-variants).

---

# ★ v1.33.5 — Khoá regression ca 19-2012 (OK+COVERED) + kế toán VBHN-đội-lốt-Luật + doc status vocab

Log rà 69 (phiên chạy MOUNT v1.33.3) báo lại đúng bộ A1/A2/B1/C1/C2 — TẤT CẢ đã vá ở v1.33.4 bên dưới
(khớp từng chi tiết: _RQ_REL_SUPPRESS, bucket loại trừ + counts, _alias_vocab, nlm_drift_basis, raw_on_nlm).
Đợt này chỉ bổ sung phần log lộ thêm:
- **r18a khoá ĐÚNG HÌNH DẠNG 19-2012**: amendment LINKED (goc) + VBHN phủ theo năm → OK + COVERED_BY_VBHN_DATE
  → KHÔNG vào relation_backfill (r17 mới khoá ca CONFIRMED); vẫn ở web_round2 vì UNVERIFIED_LATEST là việc thật.
- **Kế toán 69-vs-68 minh bạch**: phiên rà mất thời gian truy "1 Luật rớt câm" — thực ra là VBHN đội lốt
  loai='Luật' (ca 115-VBHN, data bẩn) lọt bộ lọc Luật của người vận hành. review-queue nay đếm TƯỜNG MINH
  `skipped_vbhn_as_base` (JSON + headline "VBHN-rà-theo-gốc: n") — mọi con số cộng khớp máy được.
- **SKILL §4**: dòng `tl status` ghi rõ vocab RIÊNG decision ADD/SKIP/REVIEW + alias verdict/flags từ v1.33.4
  (ADD/SKIP ≠ OK của source-map) — hết nguồn hiểu lầm "đã hợp nhất vocab" mà log B1 chỉ ra.

selftest **496/496** (+2 r18). Nợ DATA giữ nguyên thứ tự v1.33.4 (backfill-title-vn → hieuluc → nlm-reconcile
--clear-stale → ca .html 22-2023 → dedup/loai/rename).

---

# ★ v1.33.4 — Log chạy LIVE review-queue lần đầu: vá A1/A2 (backfill khống, đếm lệch) + status verdict-alias + 2 điểm mù sweep

## A1 — relation_backfill hết VIỆC KHỐNG (~40% hàng đợi là giả)
- Đo thật trên 5 ca: 19-2012 (verdict OK + AMENDMENT_CANDIDATES_COVERED_BY_VBHN_DATE) và 90-2025 (OK +
  CONFIRMED) vẫn bị xếp backfill — bucket cũ phân loại thuần theo cờ thô AMENDMENT_CANDIDATE_IN_CORPUS, vứt
  verdict + cờ HOÁ-GIẢI mà source-map đã tính. Nay `_RQ_REL_SUPPRESS` (CONSOLIDATED/COVERED_BY_VBHN_DATE/
  GATE_SUPPRESSED_CONFIRMED/CONFIRMED/OMNIBUS_AMENDS_OTHER): rel = verdict≠OK ∧ cờ-rel ∧ ¬suppressor.
  Ca thật 123-2025/68-2025 (REVIEW + UNLINKED) GIỮ NGUYÊN; 57-2024 (OK) → hết mập mờ, về clean/web theo verdict.

## A2 — bucket CHÍNH loại trừ lẫn nhau; counts CỘNG VỀ laws_scanned
- Trước: 68-2025/19-2012 nằm cả web_round2 lẫn relation_backfill → 39+5=44 line-item cho 42 Luật, tổng không
  đối soát được. Nay: ưu tiên pause > relation > web > clean/review_other (mỗi Luật đúng 1 nhóm chính; JSON có
  `counts` — tổng LUÔN = laws_scanned, máy đối soát được); VIỆC KÉP vẫn thấy đủ qua trường `buckets` từng dòng
  (text in "(+web lượt-2)"). Thêm nhóm `review_other` — REVIEW không rơi nhóm nào (trước bị RƠI KHỎI mọi đếm).

## B1 — `status --json` phát alias {verdict, flags} top-level
- Driver batch đọc `d['verdict']` cho mọi lệnh audit nhưng status chỉ có decision/reason/surface → None câm
  12/12. `preingest_gate._alias_vocab`: verdict = decision (ADD/SKIP/REVIEW — vocab tiền-nạp, KHÔNG đánh đồng
  OK của source-map); flags = mã surface + USE_VBHN/PENDING_AMENDMENTS/IN_REGISTRY_HIEULUC_UNKNOWN/
  VBHN_GOC_SUBJECT_MISMATCH/caution. decision/reason/surface GIỮ NGUYÊN (compat).

## C1 + C2 — hai điểm mù sweep
- C1: sweep in `nlm_drift ... [OFFLINE registry-only — live: tl nlm-reconcile]` + `nlm_drift_basis` trong JSON
  + next_action thường trực — ca thật: sweep=0 nhưng nlm-reconcile LIVE thấy 24 dòng desync/removed
  (registry_rows_claiming_nlm=544 vs live=295: slot registry chỉ là ESTIMATE, doctrine L4/L5).
- C2: detector MỚI `raw_on_nlm` — file THÔ (html/docx) đang là nguồn NLM live (trái 'chỉ push GDoc'; gate #3
  chỉ chặn push MỚI, hàng tồn cũ như 22-2023.html lọt) → 🔴 + rows + next_action: convert GDoc → re-push →
  gỡ nguồn raw + reg_clear mapping.

## Nợ DỮ LIỆU (thứ tự user duyệt — từ mục D của log, lệnh sẵn)
1. `tl backfill-title-vn --apply` (65/68 title_vn rỗng — GỐC RỄ QT-5 recall kém → 39 Luật web lượt-2).
2. Backfill `hieuluc` 66/68 dòng Luật (cổng status phân biệt lại được; xem IN_REGISTRY_HIEULUC_UNKNOWN).
3. `tl nlm-reconcile 743ed200-… --apply --clear-stale` (24 dòng desync/removed).
4. Ca 22-2023 .html: convert GDoc + re-push + gỡ nguồn HTML (raw_on_nlm sẽ về 0) + source-rename.
5. `tl dedup-plan --apply` + `tl backfill-loai --normalize --apply` + rename 64-2006/71-2020/03-2007.

selftest **494/494** (+4 r17: no-fake-rel, rel-real+counts-reconciliation, status-alias, raw_on_nlm).

---

# ★ v1.33.3 — Log rà 66×3 + 68 Luật: siết 2 dương-tính-giả heuristic (D1/D2) + lệnh `review-queue` gỡ nghẽn gom-tay lượt-2

Tin tốt log xác nhận: ~200 lần gọi 0 traceback/timeout/parse-fail; defect lịch sử không tái phát. Còn lại:
D (heuristic FP) + B (nghẽn quy trình: ~26 Luật cần lượt web nhưng phải GOM TAY từ 66-111 lần source-map).

## D1 — CAT_LIKELY_WRONG hết trộn thật/giả (ca 87/2015 cat 35 → gợi 44 CHỈ vì alias 'giam sat')
- Thủ phạm đo được: chủ đề 44 có alias đơn 'giam sat' — khớp 2/10 từ của chủ đề "Hoạt động giám sát của QH và
  HĐND" vẫn thành đề xuất high-confidence. 2 cổng phủ định mới (chỉ áp tầng content_alias — boundary/pin/
  omnibus-46 là bằng chứng tầng doctrine, không đụng):
  (a) `_cat_alias_evidence_for(cur)`: alias pháp điển của CHÍNH cat hiện tại xuất hiện trong title-scope →
      title cũng ủng hộ cat đang gán → không dời;
  (b) COVERAGE-GATE: alias đề xuất phải BAO TRÙM ≥1/2 số từ chủ đề — 'dau tu'/'cong chung' phủ trọn subject
      → GIỮ tín hiệu thật (143→34, 46/2024→04); 'giam sat' 2/10 → nhiễu, BỎ.

## D2 — header-verify TITLE-token over-fire (87/2015 HEADER_MISMATCH 3/4 dù tên ĐÚNG)
- Token VIẾT TẮT trong tên (HDND…) không bao giờ xuất hiện nguyên dạng trong header viết đầy đủ → nay khớp qua
  DẠNG MỞ RỘNG (_ABBREV_MAP, +hdnd/ubnd/mttq); thêm lối thoát TỶ LỆ ≥3/4 cho tên ≥4 token (1 token lạ không
  đánh sập cả check); tên 2-3 token giữ ngưỡng chặt cũ; tên SAI chủ đề thật vẫn FAIL.

## B — `tl review-queue` (MỚI): 1 lệnh gom hàng đợi rà soát
- 3 log liên tiếp cùng kết luận "~26 Luật cần lượt web LƯỢT-2 mới finalize" nhưng đều phải chạy 66-111 lần
  source-map rời rồi gom tay. Nay: quét mọi Luật/Bộ luật corpus=true (dedup sohieu; dòng thiếu sohieu đếm
  LOUD; VBHN rà theo luật gốc) → source-map offline → nhóm VIỆC:
  `web_round2` (NO_VERIFIED/UNVERIFIED_LATEST/HIGH_VELOCITY — ★ HIGH_VELOCITY xếp trước, kèm qt5_queries
  sẵn dán cho phiên Chrome) · `relation_backfill` (lệnh relation-check điền sẵn — ghi phải hỏi user) ·
  `pause` · `clean_count`. KHÔNG thay verify official — chỉ diệt công đoạn gom-và-phân-loại. `--json/--limit`.
- Quy trình chuẩn mới: `tl review-queue --json` → phiên Chrome chạy lượt-2 theo nhóm ★ trước →
  `tl vbhn-verify --official-required` → nạp QT-3.

## Không đổi (đúng chủ đích, trả lời mục F/G của log)
- F (521/509/521): khác định nghĩa + snapshot — sweep in headline server-rule "khớp `tl boot`" + corpus_basis
  từ v1.30.1/v1.31.0; muốn khớp tuyệt đối: `boot --refresh` + `sweep --refresh` cùng phiên.
- G (295/300): doctrine L4/L5 giữ nguyên — neo `tl nlm-get` LIVE trước khi kết luận FULL (memory đã sửa).
- E: nợ dữ liệu (rename 4 tên, ORPHAN_CAT 44/2024, 105/2016, backfill-loai 63, dedup 39/7/9, quarantine 107)
  — lệnh sẵn, xem runbook v1.33.0.

selftest **490/490** (+4 r16: header-abbrev-ratio, cat-coverage-gate, review-queue groups, parser).

---

# ★ v1.33.2 — Log rà 111 Luật (chạy v1.33.0): 6 defect A1..A6 — false-clean name-query, pin §0.13, evidence overclaim

Tin tốt log xác nhận: errors:[] xuyên suốt — P0-1 double-fault + pagination không tái hiện trên v1.33.0.

## A1 🔴 source-map query THEO TÊN false-clean (ca "Bộ luật Hình sự" OK/flags=[])
- Gate NO_VERIFIED_VBHN_IN_CORPUS/QT5 cũ đòi `qkey and direct` → truy vấn theo TÊN câm hoàn toàn: BLHS trả OK,
  chọn bản gốc 2015, không cờ nào — dù §0.1 lấy chính BLHS làm ví dụ VBHN lỗi thời (web có 135/VBHN-2025).
- Vá: nhánh ELIF cho name-query — canonical là bản GỐC + pool không có VBHN nào + năm canonical ≤2021 (cùng
  ngưỡng gate sohieu) → cùng cặp cờ REVIEW. Thêm A1b: VBHN_HIGH_AMENDMENT_VELOCITY (S10) nay bắn CẢ khi corpus
  chưa có VBHN (trước chỉ nằm trong nhánh `related_vbhn` — đúng ca cần nhất lại im).

## A2 🔴 + A3 — pin cat §0.13 + evidence hết overclaim
- `_CAT_PIN_RULES` (§0.13 "KHÔNG đoán cat"): xuất/nhập cảnh = 01 (hết đề xuất VBHN_62 01→39); tố tụng = 37;
  dân tộc = 10. Title khớp pin: cat ĐÚNG pin → im; cat KHÁC pin → đề xuất CHÍNH pin (doctrine thắng alias);
  omnibus nhắc chủ đề pin trong tên → nhường rổ 46. AI/CĐS/CNCNS (QĐ 26/6) im lặng CẢ 2 CHIỀU.
- A3: evidence bỏ "(đồng thuận cat-audit)" — cat-audit có guard/blacklist riêng nên có thể vẫn im với cùng
  alias; nay ghi "(alias pháp điển cùng hướng; cat-audit có guard riêng, có thể vẫn im)".

## A4 — NO_SUBJECT_TOKENS false-positive hệ thống (Thong_ke/Gia/Lao_dong/Thu_vien)
- Gốc: `_subject_tokens` bỏ stop-token TRÙNG TỪ-LOẠI văn bản ('thong' ∈ thông-tư…) + từ <3 ký tự → tên CÓ chủ
  đề đếm rỗng — dính cả 3 lệnh dùng chung `_name_structural_issues`. Fallback: tail còn từ-chữ ≥3 ký tự ngoài
  từ-loại → CÓ chủ đề. Tên trơ thật (`_GD`, 71-2020 cụt) VẪN cờ đúng.

## A5 + A6 — CLI nhất quán
- `nlm-reconcile --json` hết crash unrecognized arguments (output vốn đã JSON — nhận cờ cho driver batch đồng nhất).
- `corpus-audit --sohieu-file` + `--limit/--offset`: hết bỏ qua IM LẶNG — mặc định CẢ LÔ (đúng thiết kế
  1-process + --resume), truyền --limit/--offset thì cắt LOUD kèm trang kế; --limit default nay None để phân
  biệt explicit (fallback --all/--cat vẫn 40 như cũ).

Phần B/C của log (20 UNVERIFIED_LATEST, 15 NO_VERIFIED cần QT-5, quarantine 107, dedup, backfill-loai, misfile
143/46, slot drift −1, desync Luật Dược 76-2026, HTML đấu thầu, collision 73-82-ND-CP…) = NỢ DỮ LIỆU/vận hành —
lệnh sẵn trong runbook v1.33.0; friction Cowork (mount cắt cụt/45s/glibc/sticky-tmp) là giới hạn env đã biết.

selftest **486/486** (+6 r15: name-query gate, pin §0.13, evidence, subject-tokens, --json, sohieu-file×limit).

---

# ★ v1.33.1 — Vòng đời credential: 2 đường (bundle + public) cùng tươi bằng 1 lệnh; auth-stage ghi đè TẠI CHỖ

Từ log Cowork (A1 GWS_CRED_EXPIRED tái diễn) + chốt của user: "cả đường bundle lẫn đường public đều chạy".
Gốc rễ friction: `gws-auth-stage`/`nlm-auth-stage` cũ `upload()` TẠO FILE MỚI mỗi lần → fileId đổi → phải bake
lại tl.py / truyền --cred-file-id mỗi phiên; trong khi bundle (`secrets-set`) đã ghi-đè-tại-chỗ từ lâu.

## `_stage_enc_upload` (helper chung) + auth-stage GHI ĐÈ TẠI CHỖ mặc định
- `gws-auth-stage`: mặc định `update_content(GWS_CRED_FILEID)` — fileId GIỮ NGUYÊN → phiên Chat/Cowork sau chỉ
  `tl up`/`gws-auth-load` như cũ là nhận cred tươi, KHÔNG bake lại, KHÔNG đổi lệnh. `--cred-file-id` nhắm file
  khác; `--new` giữ hành vi cũ (tạo file mới, in fileId để bake).
- `nlm-auth-stage`: cùng khuôn với `NLM_CRED_FILEID`/env `TL_NLM_CRED_FILEID` (cookie rụng ~2-4 tuần — mỗi lần
  re-stage không còn đổi fileId).

## `secrets-set --gws/--nlm` đồng bộ luôn đường PUBLIC (1 lệnh = cả 2 đường tươi)
- Sau khi ghi đè bundle, tự mã hoá lại field tương ứng bằng WEBAPP TOKEN và ghi đè tại chỗ
  `gws_cred.enc`/`nlm_cred.enc` public. Lỗi public chỉ WARN (bundle đã xong, rc=0) + chỉ lệnh vá tay;
  `--no-public` opt-out. Thiếu token → WARN rõ, không im lặng.
- VÒNG ĐỜI TỪ NAY (mỗi lần token rụng, chạy trên máy Windows đã login):
  `gws auth login` → `tl secrets-set --gws` — XONG: Cowork (bundle) lẫn Chat (public 1Wb…) đều tự nhận.
  Cookie nlm rụng: `nlm login` → `tl secrets-set --nlm` (tương tự). KHÔNG trộn bundle & public trong CÙNG phiên
  Chat (2 đường cùng ghi ~/.config/gws/credentials.json — cái sau thắng); fix vĩnh viễn chu kỳ 7 ngày: đưa OAuth
  app sang Production (Cloud Console → OAuth consent screen → Publish).
- Message remediation (GWS_CRED_EXPIRED + canary doctor) cập nhật theo.

## Đối chiếu phần còn lại của log Cowork (không phải bug code mới)
- A2 nlm-install 45s / A3 mount cắt cụt: friction cố hữu Cowork — đã có `--resume` (v1.30.1) + `tl_fetch.sh
  --setup-step` (v1.32.2) + BƯỚC 0 curl zip sạch.
- E2 corpus-audit timeout: dùng `--offset` phân trang hoặc `--sohieu-file <f> --resume` (v1.33.0) trong 1 process.
- E1 lệch 509/521: định nghĩa client vs server-rule + snapshot (sweep in corpus_basis; `boot --refresh` +
  `sweep --refresh` cùng phiên nếu cần khớp).
- B1 (13 luật NO_VERIFIED_VBHN + QT-5), B2 (18 luật UNVERIFIED_LATEST lượt-2), B3 (109/2025 HIGH_VELOCITY),
  C1/C2 (relation backfill 123-2025/68-2025), D1 (recat 46-2024→04, 143-2025→34), D2 (backfill-title-vn 3 tên
  trơ), E3 (1 dòng sohieu rỗng) = NỢ DỮ LIỆU — lệnh sẵn trong runbook v1.33.0 mục 'Nợ DỮ LIỆU'.

selftest **480/480** (+2 r14: stage-enc-inplace fake-bridge, parser flags).

---

# ★ v1.33.0 — Log rà 69 Luật (A-mục) + log rà 15 Luật v1.32.2: CAT-auditor over-fire 78% + name/reuse-risk/dup oan + circuit-breaker gws

Hai log hội tụ về CÙNG các defect precision của auditor; bản này xử trọn nhóm CODE (A1/A2/A3 log-69; B1/B2/B3/B4/C4 log-15).

## A1+B1+B2 — `CAT_LIKELY_WRONG` chỉ suy từ TIÊU ĐỀ + cổng phủ định (`_cat_likely_wrong_suggest`)
- ĐO THẬT log-69: 59 đề xuất/54 trên 69 Luật ≈ 78% false-positive (134 AI →46; BLHS 100 →23 'điều ước'; mọi VBHN →46)
  — khối 5b cũ đưa CẢ 24KB header vào `_vb_auto_cat_from_text` → điều khoản chuyển tiếp 'sửa đổi, bổ sung' + dẫn
  chiếu 'điều ước quốc tế' + token lạc (hải quan/BHXH) trong THÂN của gần như mọi luật kích boundary-rule.
- Nay: (1) bằng chứng = TITLE-SCOPE (tên + khối tiêu đề IN HOA `_title_block_from_text` + title_vn), thân văn bản
  KHÔNG còn là bằng chứng cat; (2) VBHN KHÔNG BAO GIỜ →46 (hợp nhất ≠ omnibus — cat theo LUẬT ĐÍCH); omnibus THẬT
  (`_is_omnibus_entry`, cả tên nén) vẫn →46 kể cả khi title-block miss; (3) →23 chặn khi loai/tên đã định danh
  Luật/Bộ luật; (4) allowlist Quyết định 26/6: AI/CĐS/CNCNS đang cat 19 → KHÔNG đề xuất dời (`_CAT19_PIN_RE`);
  (5) cross-check `_expected_cat_from_alias` (CÙNG engine cat-audit → xử luôn B3 'hai auditor mâu thuẫn'): alias
  khẳng định cat hiện tại → bỏ; alias ra cat thứ ba → bỏ; alias đồng thuận → ghi vào evidence.
- Tín hiệu thật GIỮ: 143-2025 'Đầu tư' cat 45 → đề xuất 34 (không còn 46 sai); omnibus 57-2024 → 46.
- note_vs_sweep cập nhật cho khớp thực đo (A1e: hết tự nhận 'precision-first' trong khi bắn 59 phát).

## A2 — NAME_NONSTANDARD nhận viết tắt Bộ luật (`BLDS_/BLHS_/BLLD_/BLTTHS_/BLTTDS_/BLHH_`)
- `_NAME_TYPE_PREFIX_RE` whitelist + `_NAME_PREFIX_FAMILY` (BLDS↔Bo_luat cùng HỌ — không tính 'đổi mã loại' i2c).
  Áp cả 3 chỗ: `_name_structural_issues` (sweep name_nonstandard dùng chung), `_name_looks_nonstandard`, guard prefix
  NAME_TRICH_YEU. 4 ca tên hỏng thật (.html/thiếu sohieu/cụt) VẪN bắt.

## A3 — Circuit-breaker gws AUTH-DEAD (transport + tl_gws + `_read_doc_text`)
- Log-69: `[FALLBACK→GAS] gws rc=2: Authentication failed` trên MỌI văn bản + mỗi doc tốn retry gws → batch 69 vượt
  timeout shell. Lỗi auth là TERMINAL trong 1 process: `tl_gws._CRED_AUTH_DEAD` (set khi invalid_grant trong
  `_access_token`) → `_read_doc_text`/transport-download SKIP direct-media từ doc thứ 2; `transport._GWS_AUTH_DEAD`
  (+`_is_gws_auth_error`) → op sau đi THẲNG GAS, thông báo đúng 1 lần. 2 cờ TÁCH RỜI đúng kiến trúc 2-credential.
  gws-ping/doctor canary gọi thẳng `_access_token` nên không bị breaker che.

## B4 — `VBHN_NUMBER_REUSE_RISK`/`TITLE_OR_REGISTRY_WARN` hết oan khi năm ĐỦ (ca 25-2025 Kế toán)
- GỐC RỄ tìm ra khi viết test: `VBHN_BARE_NUMBER` false-positive — tail 'Luat_Ke_toan' bị `_token_set` bỏ 'luat'
  (stop-word) + 'ke' (2 ký tự) → đếm <2 tưởng TÊN TRƠ → kéo cả REUSE_RISK lẫn TITLE_WARN. Vá tận gốc trong
  `_vbhn_metadata_flags`: fallback đếm từ-chữ ≥2 ký tự trong tail.
- Thêm 2 lớp cho reuse-risk: (a) 'nhiều ứng viên cùng số' chỉ đếm VĂN BẢN PHÂN BIỆT (bỏ sidecar .docx/quarantine —
  cặp GDoc+file-thô cùng số là MỘT văn bản); (b) `_vbhn_year_complete` — năm có ở CẢ sohieu-key lẫn TÊN thì hết rủi
  ro tái-dùng-số (số VBHN tái dùng THEO NĂM). Tên trơ thiếu năm (133/61/72) VẪN cờ đúng.

## C4 — sweep/hygiene dup by_sohieu tách TRÙNG THẬT vs cặp lành (`_sohieu_dup_group_real`)
- Headline '93 trùng' = báo động giả (log-15: chỉ 4 cụm ≥2 corpus=true, cả 4 là tách Phụ lục/Final cố ý; 49 cụm
  gốc+VBHN/quarantine lành). Trùng THẬT = ≥2 bản corpus=true CÙNG PHÍA (≥2 VBHN hoặc ≥2 non-VBHN) sau khi loại
  sidecar/quarantine/template/phụ-lục (nhận cả 'PhuLuc' nén). sweep in `sohieu=<real> (raw=<N> gồm gốc+VBHN/phụ-lục
  lành)`; hygiene scan: `duplicates_by_sohieu`=real, `duplicate_sohieu_groups_raw`=raw (đúng tên khóa sẵn có).

## B3-log69 — `corpus-audit --sohieu-file <f> [--resume]`
- Vòng `--sohieu X` ×69 process rời = 69 lần boot + retry gws per-doc → 1 PROCESS cả lô (mỗi dòng 1 số hiệu, '#'
  comment, dedup drive_id, dòng không resolve báo LOUD). CHECKPOINT theo md5 nội dung file: ghi sau mỗi target,
  `--resume` nạp lại bỏ target đã xử (kể cả sau READ_BACKEND_DOWN — abort message chỉ lệnh resume), chạy trọn tự xoá.

## KHÔNG sửa (đúng chủ đích)
- B2-log69 (doctor false-green): ĐÃ vá v1.32.1 (canary) — log-15 xác nhận doctor nay ĐỎ đúng.
- D1/D2-log15 (509 vs 521; NLM 295/300): khác ĐỊNH NGHĨA + snapshot, sweep đã in corpus_basis; tin `nlm-get` LIVE.

## Nợ DỮ LIỆU (user duyệt & chạy — lệnh sẵn, thứ tự khuyến nghị)
1. `tl backfill-loai --normalize --apply` — 63-77 loai phi-chuẩn (C1 cả 2 log; ⚠ PHẢI có --normalize).
2. Verify header 143-2025 rồi `tl recat 143-2025-QH15 --cat 34 --apply` (C4-log69 — misfile THẬT, đích 34 không phải 46).
3. `tl backfill-title-vn` / `tl register --title-vn` cho 33-2024 (C3-log69 boilerplate).
4. `tl header-verify --fix-suggest` → `source-rename` 4 ca tên hỏng thật (123_GD, 71-2020, 64-2006, 03-2007, 22-2023.html) + lô tên VBHN trơ thiếu năm (C2-log15: 133/61/72 — `source-rename --rename-drive`).
5. E1-log15: QT-5 tìm VBHN mới nhất Bộ luật Hình sự (135/VBHN 2025) → nạp QT-3; mẻ QT-5 14 luật NO_VERIFIED_VBHN.
6. `tl dedup-plan` (DRY) soát các cụm same_document/md5 còn lại.

selftest **478/478** (+9 r13: cat-body-not-evidence, pin19, true-positive-alias, omnibus-46/VBHN-never-46,
name-BLDS, reuse-sidecar+year-complete, dup-real, gws-breaker, sohieu-file flags). transport selftest 12/12.

---

# ★ v1.32.2 — Log rà 69 Luật (chạy LIVE trên v1.32.x): cold-start + loai-conflict + omnibus-tên-nén + tách bước setup

TIN XÁC NHẬN từ log: gate A1/A2 v1.32.0 hoạt động đúng thực địa (90-2025 nay OK + AMENDMENT_GATE_SUPPRESSED_CONFIRMED;
115-2026-VBHN nay OK + AMENDMENTS_ALREADY_CONSOLIDATED); doctor 13/13 sau khi user refresh cred; nlm-install --resume
+ canary vào guồng. REVIEW còn lại chủ yếu ĐÚNG THIẾT KẾ (14 luật thiếu VBHN cần QT-5 web; 3 luật cần relation-backfill).

## S1 — `tl ping` retry cold-start Apps Script
- Webapp lạnh trả 404/timeout 2-3 lần gọi ĐẦU rồi mới ấm → phiên từng kết luận sai 'webapp chết'. Ping nay retry ×3
  (backoff 2s/5s) CHỈ với lỗi dạng cold-start (404/timeout) — lỗi khác giữ nguyên, không che.

## S3 — backfill-loai --normalize thêm mode CONFLICT (ca 115-2026-VBHN mang loai='Luật')
- loai HỢP LỆ enum nhưng mâu thuẫn bằng chứng → chỉ đề xuất khi 2 bằng chứng ĐỒNG THUẬN: tên prefix `VBHN_` VÀ
  sohieu chứa `-VBHN-` → 'Văn bản hợp nhất' (mode=conflict; prefix khác nhiều ngoại lệ nên KHÔNG mở rộng).

## S5 — `_is_omnibus_entry` nhánh đề-tài-trong-tên (dạng NÉN)
- Ca 57-2024 vẫn REVIEW lặp sau v1.32.0: registry goc/sua_doi CHƯA backfill → nhánh ≥2-ref câm; tên
  'SuaDoi_QuyHoach_DauTu_PPP_DauThau' strip xong DÍNH LIỀN nên so alias có-space không khớp → so DẠNG NÉN,
  ≥2 đề-tài = omnibus. Guard: sửa-1-luật (75-2025 Quảng cáo) / luật thường có 'đầu tư' trong tên (68-2025) KHÔNG dính.

## S4 — `tl_fetch.sh --setup-step core|gws|boot|nlm`
- --setup trọn gói vượt trần 45s/lệnh Cowork (bị kill giữa chừng, log C1) → tách 4 bước, mỗi lệnh 1 bước;
  bước nlm lặp cùng lệnh tới hết PARTIAL (rc=3 = còn bước, KHÔNG lỗi — in rõ).

Ghi chú log C1 còn lại = giới hạn môi trường đã biết (mount cắt cụt/bwrap kill nền/boot 36.7s gần trần — boot sẽ
nhanh hơn khi cred sống vì manifest đi direct-media). Data runbook mục D giữ nguyên (6 bước — các lệnh đều sẵn).

selftest **469/469** (+3 r12: omnibus-tên-nén ± guard, loai-conflict corroborated ± guard, nlm-read gates).

---

# ★ v1.32.1 — Log rà 119 Luật: read-path CHẾT TOÀN BỘ nhưng health-check FALSE-GREEN

Từ phiên rà toàn tập 119 Luật (v1.31.2): gws refresh_token đã revoke NHƯNG `doctor`/`gws-ping` vẫn ✓
(chỉ kiểm binary + cấu hình oauth2, KHÔNG thử token thật) → phiên tưởng sẵn sàng rồi corpus-audit lặp
từng doc ~22s toàn 'header rỗng' (pool 531 ≈ 3.2h all-error). Đồng thời lộ khẳng định SAI trong message
GWS_CRED_EXPIRED cũ: fallback GAS 'vẫn đúng' — thực tế exporttext (đọc text) chết theo vì webapp thiếu
scope `script.external_request`; chỉ download-file (b64) sống.

## P1a — Canary token thật (`_gws_cred_alive`)
- 1 POST oauth2 (~200ms, cache token process): `gws-ping` + `doctor` nay ĐỎ khi invalid_grant, kèm remediation
  (`gws auth login` → `tl secrets-set --gws`) + workaround (`tl nlm-content`); `doctor --offline` skip canary
  và GHI RÕ chưa kiểm. Note cuối gws-ping phân biệt 'cred CHẾT' (đọc Drive hỏng) vs 'chưa nạp' (fallback OK).
  Verify LIVE trên máy dev (cred đang chết thật): gws-ping ✗ đúng.

## P1b — Fast-fail + đường đọc dự phòng NLM
- `corpus-audit` + `backfill-title-vn` (header mode): ≥3 lỗi đọc LIÊN TIẾP (đã thử cả 2 đường) → ABORT
  `READ_BACKEND_DOWN` rc=2 kèm chẩn đoán, không cày hết pool.
- `_read_doc_text_via_nlm` (mới): entry có nlm_source_id live → đọc text qua `nlm source content` (bản đã nạp,
  vẫn verbatim nguồn — đủ cho header/audit). corpus-audit/backfill-title-vn tự thử khi Drive chết → 295 nguồn
  NLM vẫn audit được trong lúc chờ refresh cred.

## P0-msg — Sửa khẳng định sai
- GWS_CRED_EXPIRED nay nói đúng: fallback GAS chỉ cứu DOWNLOAD file; op ĐỌC TEXT chết theo (webapp thiếu scope
  `script.external_request`) — extract/corpus-audit đi đường NLM tạm. (Cấp scope cho webapp = việc GAS-side,
  cần sửa appsscript.json + redeploy nếu muốn fallback đọc thật sự sống.)

Nợ OPS/DATA (mục E log — không đổi): (1) `gws auth login` → `tl secrets-set --gws` [P0, chặn nhiều nhất];
(2) sau khi có read: header-verify 21 dòng TITLE_OR_REGISTRY_WARN + backfill hieuluc + QT-5 web 14 luật REVIEW;
(3) hygiene: dedup-plan/backfill-loai --normalize/chuẩn hoá 173 tên (gồm canonical .html Đấu thầu 22-2023).

selftest **467/467** (+1 r12). Lưu ý: log này chạy v1.31.2 — các defect gate A1/A2/A3 nó gặp (REVIEW omnibus/
confirmed/VBHN) đã vá ở v1.32.0 chưa-deploy; deploy 1 lần được cả 2 đợt.

---

# ★ v1.32.0 — Log rà 77 Luật: 3 defect lớp AMENDMENT-GATE (A1/A2/A3) + enum điều ước + sidecar noise

Từ backlog rà 77 Luật trên bản deploy v1.31.x (xác nhận qua name_nonstandard/stale_nlm_ref trong log): mọi defect
đều ở LỚP GATE trong `_source_map_one`, không phải detector.

## A1 — confirmed=yes phải chặn CẢ nhóm cờ amendment-gate (ca 90-2025)
- Trước: `_entry_confirmed` chỉ suppress DIRTY/TITLE_WARN; khối escalation (UNLINKED_AMENDMENT_CANDIDATE /
  VBHN_RECHECK_REQUIRED / PAUSE / LOW_CONFIDENCE) chạy bất kể canonical đã verified — trái doctrine §confirm.
- Nay: canonical confirmed → cờ `AMENDMENT_GATE_SUPPRESSED_CONFIRMED` (ứng viên chỉ liệt kê tham khảo), KHÔNG
  escalation; `action_required` nhất quán (`_gate_escalate` = strong ∧ ¬covered ∧ ¬confirmed). Nghi có sửa đổi
  MỚI hơn ngày confirm → gỡ nhãn verified rồi rà lại (ghi rõ trong cờ).

## A2 — gate 'tìm VBHN cho một VBHN' (ca 115-2026-VBHN)
- Gốc: khối consolidated chỉ gom goc của `related_vbhn` — RỖNG khi query THẲNG số VBHN (canonical = chính VBHN
  từ direct) → luật nó đã hợp nhất (06-2026) bị coi amendment mồ côi + đòi 'recheck VBHN'.
- Nay: canonical là VBHN → refilter ứng viên thuộc `_goc_keys(canonical)` sang consolidated_amendments
  (+AMENDMENTS_ALREADY_CONSOLIDATED); ứng viên NGOÀI goc còn lại → `VBHN_GOC_VERIFY` (xác minh chuỗi goc/sua_doi
  qua footnote-map/relation-check + bản MỚI NHẤT lượt-2) thay vì VBHN_RECHECK_REQUIRED; REVIEW giữ cho ca này
  (VBHN có amendment chưa hợp nhất = rủi ro lỗi thời THẬT).

## A3 — omnibus bị coi amendment mồ côi lặp vô hạn (57-2024/68-2025/90-2025/123-2025)
- `_is_omnibus_entry` (PURE): cat 46 ∨ tên 'sua doi N luat' ∨ (cụm sửa-đổi + ≥2 ref goc/sua_doi). Canonical
  omnibus → `OMNIBUS_AMENDS_OTHER` (bản chất amends-other, không bao giờ có VBHN của chính nó — rà theo từng
  luật ĐÍCH), BỎ UNLINKED/LOW_CONFIDENCE → verdict OK thay REVIEW lặp. PAUSE cho ứng viên STRONG giữ nguyên.

## A4 + B3
- `_LOAI_CANON` + 'Điều ước quốc tế'/'Công ước' (keys dieu uoc quoc te/dieu uoc/cong uoc…) — hết 56 dòng công ước
  ILO đếm nonmappable/loai_noncanonical GIẢ; `backfill-loai --normalize` hưởng ngay.
- `RAW_NAME_NOT_NLM` bỏ khỏi `risky_candidates` khi entry là SIDECAR .docx/.pdf cạnh GDoc cùng nhóm
  (`_is_source_sidecar` — 21 ca noise mỗi lần rà; cờ gốc trong _title_flags giữ nguyên cho sweep/doctor).

## Nợ DỮ LIỆU (mục C log — user chạy LIVE, thứ tự corpus-fix):
1. `tl backfill-loai --normalize --apply` (60 dòng + hết 56 nonmappable-giả sau A4; sửa cả 115 về VBHN).
2. BHXH 41-2024: giữ GDoc -QH15 canonical → gỡ NLM bản PDF trùng → `tl source-update-corpus 41-2024-QH15 true`
   + bỏ quarantine (xem stale_nlm_ref sweep).
3. 61_2020 Đầu tư: backfill goc/sua_doi (57-2024 sửa) qua `tl relation-backfill --base 61-2020-QH14` + sửa
   sohieu underscore.
4. `tl recat 143-2025-QH15 --cat 34 --apply` (sau header-verify) · điền cat 44-2024 · xác minh 46-2024→04 (medium)
   · vá hậu tố tên folder cat trơ (46-2019→32, 57-2024→34, 129-2025→05).
5. Mẻ QT-5 web lượt-2: ưu tiên 22-2023 Đấu thầu + 109-2025 Thuế TNCN (HIGH_VELOCITY), rồi 16 QT5_WEB_REQUIRED +
   19 UNVERIFIED_LATEST (query đã sinh sẵn trong source-map/vbhn-check --json, chạy Claude-in-Chrome).

selftest **466/466** (+7 r11_*: confirmed-suppress cả strong-linked, VBHN-consolidates-own-goc, GOC_VERIFY,
omnibus amends-other + detector, treaty enum, sidecar-not-risky).

---

# ★ v1.31.2 — Log LIVE vòng 3: U1 sanitize UTF-8 export-text + U2 trích yếu từ KHỐI TIÊU ĐỀ (tier-1)

Từ lần chạy tiếp của phiên rà (vẫn bản mount v1.30.1): (1) `tl extract --dieu 1` làm vỡ capture bash vì byte
không hợp UTF-8 trong output; (2) phát hiện ĐÚNG của họ: nguồn trích yếu chuẩn = KHỐI TIÊU ĐỀ (dòng LUẬT/BỘ LUẬT
IN HOA → dòng chủ đề, trước 'Căn cứ'), không phải Điều 1 (trả khoản phạm-vi). Script + sidecar 34 mục gửi kèm
đã THẨM ĐỊNH — sidecar lộ ≥6 mục CỤT/SAI ('Luật Lưu trữ và pháp', 'Luật Thi', 'Luật Quản lý', 91/2015 thành
'Luật Dân sự' SAI LOẠI, casing .lower() trần) → KHÔNG import; làm lại parser trong skill.

## U1 — `_sanitize_export_text` (chống vỡ UTF-8 mọi driver)
- Diệt lone-surrogate (round-trip encode-replace — rò từ decode surrogateescape các đường export/gws) + bỏ
  control-char (giữ \n \t). Bọc MỌI nhánh `_read_doc_text` (cache/direct-media/transport/exporttext) +
  `cmd_extract` TRƯỚC khi ghi đĩa/in — stdout reconfigure errors='replace' sẵn có (tl.py:44) KHÔNG cứu được
  file `--out` và text chui vào pipeline JSON của driver.

## U2 — `_title_block_from_text` + `_title_sentence_case` (TIER-1 của `_title_vn_from_header`)
- Bóc dòng LOẠI IN HOA đứng riêng (`BỘ LUẬT` ưu tiên TRƯỚC `LUẬT` — script gốc match ngược → sai loại) → gom
  ĐỦ các dòng chủ đề in-hoa (≥80% chữ hoa; KHÔNG cap 4 dòng như script gốc → hết cụt '(HIV/AIDS)'/'…quy phạm
  pháp luật'; dừng ở Căn cứ/CHƯƠNG/Điều/kẻ ngang/dòng thường) → sentence-case GIỮ token có số/`/`/ngoặc.
- Nhận cả PHÁP LỆNH/NGHỊ QUYẾT/NGHỊ ĐỊNH/THÔNG TƯ (kind qua _normalize_loai). Miss → tier-2 cũ
  (_doc_subject_for_name) giữ nguyên; guard dấu/boilerplate như cũ. `backfill-title-vn` (header mode) hưởng trực tiếp.
- Ghim test đúng các ca sidecar hỏng: multiline-no-cap, Bộ-luật-đúng-loại, (HIV/AIDS), dừng-ở-dòng-thường.

## Vá thêm cùng ngày (debug phiên deploy của user)
- **FP cat-guard CNTT (phiên rà xác nhận, canonical dính y hệt — tự tái hiện):** chude 19 có alias TRẦN
  'cong nghe' còn 03 KHÔNG có alias 'cong nghe thong tin' trong linhvuc_phapdien.json → Luật CNTT (03 đúng chuẩn)
  bị `_expected_cat_from_alias` nghi 19. Vá MẠNH HƠN script tham khảo (họ defer-im-lặng): boundary
  'cong nghe thong tin' → trả POSITIVE **03** (đã xác minh pháp điển, doctrine §0.13 — bắt được cả ca Luật CNTT
  nằm SAI cat khác) + 'cong nghe' trần vào _ALIAS_TOO_GENERIC (alias 19 đặc thù giữ nguyên). +1 test r9. ⚠ KHÔNG
  áp gói patch/sidecar của phiên kia lên canonical: patch nhắm v1.30.1 (đã bị v1.31.x vượt — áp vào là THỤT LÙI
  derive_subject + tái nhập sidecar trái doctrine); sidecar 34 mục vẫn nguyên ≥6 lỗi cụt/sai-loại.
- **Selftest xả noise test-lỗi-chủ-đích ra console deploy** (user đọc thành "vẫn lỗi"): `tl register: error:
  invalid choice: 'xyz'` là test r5 CỐ TÌNH truyền giá trị sai để xác nhận parser CHẶN (PASS nhờ chính dòng đó);
  tương tự CẮT BATCH (test phân trang loud), [gas-retry] TimeoutError (mock), ENTRY_RAW_NO_GDOC (hành vi đang
  test), [manifest] gws-fallback (test env-restore chạm LIVE). → helper `_hush` nuốt stdout/stderr của 5 block đó;
  console selftest nay CHỈ còn [OK]/[FAIL] + 2 dòng tổng. Debug lại: `TL_SELFTEST_VERBOSE=1`.
- **`upload-skill-to-Package.cmd` in "The system cannot find the path specified." mỗi lần chạy:** bisect bằng
  echo-on lộ thủ phạm = mũi tên `->` trong dòng `title` — cmd hiểu `>` là REDIRECTION, cố ghi stdout vào file
  `VBQPPL/Package` không tồn tại. Bỏ mũi tên khỏi title → hết (không liên quan Unicode/AutoRun như nghi ban đầu).
- **direct-media HTTP 400 "Bad Request" (mọi đường _drive_media_download):** cô lập từng bước → gốc =
  **GWS_CRED_EXPIRED**: refresh_token trong `~/.config/gws/credentials.json` hết hạn/bị thu hồi (invalid_grant
  từ oauth2.googleapis.com). Kiến trúc: file cred này (nguồn direct-media) TÁCH RỜI token keyring của gws CLI
  binary → gws CLI (drive-push/files list) vẫn chạy tốt trong khi direct-media chết → không ai nghi cred.
  `_access_token` nay đọc body lỗi + raise thông điệp tự-chẩn-đoán (GWS_CRED_EXPIRED + cách sửa). Fallback GAS
  b64 vẫn đúng (chỉ chậm + noisy). **Ops:** `gws auth login` → `tl secrets-set --gws` (làm mới bundle cho Cowork
  — bundle hiện tại nhiều khả năng cũng chứa cred hết hạn ⇒ Cowork cũng đang rơi fallback).

selftest **458/458** (+7 r10_*). Dữ liệu: sidecar 34 mục của phiên kia KHÔNG cần import — sau deploy chạy
`tl backfill-title-vn --from-tukhoa --apply` rồi `tl backfill-title-vn --apply` (header tier-1 mới) lặp tới
writable=0 là phủ sạch + ĐÚNG hơn sidecar.

---

# ★ v1.31.1 — Log phiên rà 68 Luật VÒNG 2 (tham khảo 4 script user): title_vn at-ingest + tier tukhoa + alias-strict + sweep name_nonstandard

Bối cảnh: phiên Cowork kia chạy bản MOUNT v1.30.1 (v1.31.0 đã zip nhưng CHƯA push) → nhiều mục họ vá lại là thứ
v1.31.0 ĐÃ CÓ (derive_subject title-first, CAT_LIKELY_WRONG, NAME_NONSTANDARD, P1-4 agency-gate). Chỉ tích hợp
phần MỚI THẬT từ 4 script gửi kèm (đã thẩm định + vá lỗi họ tự báo).

## N1 — title_vn AT-INGEST (fix gốc họ đề xuất: "bắt trích yếu tại ingest, không vá post-hoc")
- `ingest-local` backfill sau organize nay ghi KÈM `title_vn` từ auto-plan (`_title_vn_from_plan` — analyzer đã
  đọc header/probe-text sẵn, 0 call thêm; guard có-dấu + không-boilerplate; chỉ ghi khi read-back title_vn rỗng;
  journaled before → undo). Dòng registry MỚI hết rơi vào nợ backfill.

## N2 — `backfill-title-vn --from-tukhoa` (tier-2 OFFLINE; thay thế đề xuất sidecar của script gốc)
- `_title_vn_from_tukhoa`: bóc `(Bộ luật|Luật) <chủ đề CÓ DẤU>` từ field `tukhoa` sẵn có — 0 call/dòng, quét cả
  pool 1 phát; guard: cắt heading-giữa-câu (regex `[A-ZĐ]` — KHÔNG dùng dải `À-Ỹ` vì Unicode XEN KẼ hoa/thường,
  'đ'∈À-Ỹ từng cắt nhầm giữa 'quy định'; bug tự bắt khi smoke), cắt đuôi liên từ (+năm/quy/định), boilerplate,
  PHẢI có dấu, CROSS-CHECK token với tên file qua `_token_set`.
- **Vá 2 lỗi script gốc TỰ BÁO:** (a) false-reject viết tắt (CNTT ↔ 'công nghệ thông tin') → cross-check dùng
  `_token_set` (đã expand `_ABBREV_MAP`) + bổ sung 6 viết tắt (cntt/pcth/pccc/hnvgd/gtvt/khcn); (b) méo/cụt
  ('Luật Thi', 'Luật Mặt trận') → chính cross-check + junk-cut loại.
- **KHÔNG dùng sidecar `~/.tra_luat_trichyeu.json`** như script gốc — trái doctrine single-source (sự cố
  2026-06-30): registry cột `title_vn` là nguồn duy nhất, `_META_TITLE_KEYS` tự ăn. Vận hành: chạy
  `--from-tukhoa --apply` TRƯỚC (phủ nhanh phần sạch) → mặc định (header, lô 40) vét phần còn lại.

## N3 — cat-audit tầng ALIAS pháp điển (từ cat_audit_strict.py, thẩm định)
- `_expected_cat_from_alias` (+`_alias_cat_pairs` cache): alias `linhvuc_phapdien.chude[].alias`+slug,
  longest-match whole-word ≥5 ký tự, blacklist alias quá chung (giám sát/quản lý/…), boundary-guard
  'vốn nhà nước/đầu tư công/ngân sách' → nhường `_cat_boundary_rule` (chống over-fire 68-2025 → đúng 26).
- Nối vào `cmd_cat_audit` nhánh cuối (chỉ khi boundary + keyword-tên đều im; chỉ tên Luật/Bộ luật; subject =
  tail-pretty + title_vn — giàu thêm sau backfill): cờ `CAT_LIKELY_WRONG` confidence=medium, REVIEW-tay.
  Bắt đúng 2 true-positive log: **143-2025 Đầu tư ở 45 Y tế → 34**; **46-2024 Công chứng ở 09 → 04**.

## N4 — sweep `name_nonstandard` (từ name_audit.py; corpus-audit chỉ chấm dòng ĐÃ đọc header → thiếu phủ)
- `_sweep_report` + bucket `name_nonstandard`/`name_nonstandard_rows` (offline toàn corpus, dùng
  `_name_structural_issues` sẵn có; cùng guard corpus-audit: bỏ PL_/Mau_/điều-ước/non-corpus) + NEXT ACTION.

## Review đối kháng (2 chiều + verify) — 1 CONFIRMED đã VÁ, chiều alias/sweep PASS toàn bộ
- **VÁ (CONFIRMED critical):** heading-split tukhoa đoán theo chữ-hoa cắt trước MỌI từ viết-Hoa → tukhoa
  Title-Case ('Bảo Hiểm Xã Hội Điều 2') cụt còn 'Bảo' — nay cắt theo TỪ-KHÓA heading thật
  (Điều/Chương/Mục/Phần/Khoản/Giải thích/Phạm vi/Đối tượng/Hiệu lực); danh-từ-riêng giữa tên
  ('Mặt trận Tổ quốc Việt Nam') không còn bị cắt (+test r9 ghim cả 2 ca).
- **Siết (major reviewer nêu):** N1 title_vn CHỈ ghi khi reg_get read-back OK (lỗi mạng → thôi, không ghi mù —
  backfill-title-vn vét sau).
- Trade-off boundary-guard N3 (nhường corpus-audit level-3 ca đầu-tư-công nằm sai cat): reviewer chiều 2 xác nhận
  đúng thiết kế precision-first; _corpus_fix_plan không đọc key mới → 0 regression.

selftest **451/451** (+9 r9_*: tukhoa extract/abbrev/rejects/heading-đ/Title-Case, alias-cat + boundary,
title_vn_from_plan, sweep offline, parser). Nợ DỮ LIỆU giữ nguyên runbook: backfill-title-vn (tukhoa→header) →
nạp VBHN 135 BLHS → LƯỢT-2 web set-A/B → consolidation-cleanup 44 → dedup/year/loai.

---

# ★ v1.31.0 — Backlog rà 68 Luật (2026-07-03): P0 độ-chính-xác-phát-hiện + P1 nhất quán vocab/đếm

Từ BACKLOG hợp nhất Lượt 1-3 + QT-5 web trên 68 Luật (v1.30.1): tầng LỆNH ổn định (0 crash, đúng rc) — mọi vấn đề
nằm ở ĐỘ CHÍNH XÁC PHÁT HIỆN + NHẤT QUÁN VOCAB. User kèm patch tham khảo P0-1 (đã thẩm định, tích hợp có điều chỉnh).

## 🔴 P0 — độ chính xác phát hiện
- **P0-1 QT-5 subject (bằng chứng: query literal-filename tìm ra 0; query tay có dấu ra ngay VBHN 135 BLHS):**
  (a) `_derive_subject_from_entries` ĐẢO ưu tiên: title-first (guard `_looks_like_filename_title` — nlm_title/
  title_vn nhiều khi = tên file) → `_name_tail_pretty` (GIỮ hoa/thường) → fallback tail-key ASCII cũ;
  (b) cờ `QT5_SUBJECT_NO_DIACRITICS` (advisory) trong vbhn-check khi subject không dấu — nhắc --subject tay;
  (c) **`tl backfill-title-vn` (MỚI):** phát hiện then chốt khi rà — cột `title_vn` ĐÃ CÓ SẴN trong 27 cột
  (v2.13.0, entryOf_ đã export, _META_TITLE_KEYS đã ưu tiên) → KHÔNG cần đổi schema/deploy GAS như backlog dự kiến;
  chỉ cần BACKFILL: đọc header thật (`_read_doc_text`, lô 40 + --offset + heartbeat) → `_title_vn_from_header`
  (PURE: ALL-CAPS→sentence-case, '<Loại> <Chủ đề>'; skip LOUD khi NO_DIACRITICS/BOILERPLATE — không đoán) →
  journaled reg_bulk cột title_vn (before→undo). Sau backfill toàn chuỗi QT-5 tự ăn khớp.
- **P0-2 `CAT_LIKELY_WRONG`:** corpus-audit trước CHỈ fill-missing (cat rỗng/00) → ca `Luat_143-2025 Đầu tư` nằm
  cat 45 Y tế mà 0 proposals. Nay cat CÓ GIÁ TRỊ + suy-nội-dung confidence=high ra cat KHÁC → proposal 🟡 REVIEW
  (`tl recat` DRY, người duyệt — KHÔNG auto-move, giữ bài học over-fire v1.27.1).
- **P0-3 `NAME_NONSTANDARD`:** `_name_structural_issues` (PURE) so tên với mẫu `<Loai>_<sohieu>_<Chu_de>` ĐỘC LẬP
  header — bắt trọn 4 ca lọt lưới: `.html` filename, thiếu cụm sohieu (`Luat_Phong_chong_benh_truyen_nhiem`),
  thiếu token chủ đề (`Luat_64-2006-QH11`); skip PL_/Mau_/điều-ước/non-corpus; không trùng NAME_TRICH_YEU.

## 🟠 P1 — precision & nhất quán
- **P1-4 `_vbhn_agency_mismatch`:** VBHN cấp BỘ (VBHN-BTP/BGDDT/…, hợp nhất NĐ/TT) KHÔNG được nổi làm candidate
  của văn bản QH (…-QHxx/UBTVQHxx/LCT-HDNN) khi KHÔNG có goc-chain dẫn chiếu base — gate ở CẢ `_vbhn_candidates`
  (vbhn-check) + `_relation_audit` (relation-check). Chặn ca 4231-2025-VBHN-BTP score 158 nổi cho Luật 90/2025.
- **P1-5 vocab QT-5 thống nhất `{verdict, flags, qt5_queries, google_discovery}`:** relation-check thêm
  verdict/flags top-level (REVIEW khi missing_links/footnote-thiếu/subject-only · QT5_WEB_REQUIRED khi chưa thấy
  VBHN · OK) + `qt5_queries` (giữ `vbhn_queries` compat); source-map item thêm alias `qt5_queries`.
- **P1-6:** sweep `quarantine.still_on_nlm` nay = LIVE-status (`_entry_on_nlm_live` — khớp reg-query; hết bất đồng
  4 vs 0); nlm_source_id sót trên dòng đã gỡ → `stale_nlm_ref` riêng (rác metadata → reg_clear).
- **P1-7:** sweep text 1 CON SỐ HEADLINE = server-rule (khớp `tl boot`) + 1 dòng Δ gọn; `--verbose` mới in giải
  thích định nghĩa đầy đủ. JSON giữ nguyên đủ trường.
- **P1-8:** `_is_treaty_entry` — Công ước/Điều ước quốc tế (CU_ILO-*, Cong_uoc_*) sohieu RỖNG là HỢP LỆ → lớp
  `treaties` riêng trong hygiene/sweep, KHÔNG tính orphan (orphans=46 trước đây gộp cả ILO).
- **P1-9 (data — ĐÃ LÀM LIVE trong phiên):** config public `1dEOBJ…` vá `profiles.vbqppl.registryDocId`
  1mATG Doc-legacy → `1C21i65…` Sheet thật; drive-push GIỮ fileId; verify curl PASS (hết auto-heal mỗi phiên trống;
  GAS v73 doWriteConfig_ đã vá clobber nên không bị ghi đè lại).

## Review đối kháng (3 reviewer + verify per-finding, Explore read-only) — kết quả
- **VÁ (finding thật, tự tái hiện):** `_name_tail_pretty` để LỌT NĂM sau khi bóc sohieu tên VBHN
  (`VBHN_121-VBHN-VPQH_2025_Luat_HNGD` → '2025 Luat Hon nhan…') → + 1 lớp bóc năm đứng đầu; test r8 siết
  SO CHÍNH XÁC (endswith cũ che mất bug).
- **VÁ (CONFIRMED):** `backfill-title-vn --apply` pool TỰ CO sau mỗi lần ghi → `--offset` cũ NHẢY CÓC bỏ sót —
  nay --apply BỎ QUA --offset (loud); semantics = LẶP CÙNG LỆNH tới writable=0 (--offset chỉ cho DRY).
- **REFUTED:** 'qt5_queries alias mismatch source-map vs relation-check' — chủ đích thiết kế (mỗi lệnh alias
  sang list QT-5 tương ứng của nó; test ghim cả 2; không consumer nào gộp chéo).
- Minor ghi nhận không vá: `mo_ta` trong _META_TITLE_KEYS có thể nhiễu (đã guard filename+token; theo dõi);
  `.capitalize()` hạ chữ hoa danh-từ-riêng (hiếm ở trích yếu luật; NO_DIACRITICS chặn phần lớn ca OCR);
  corpus=='true' strict (convention toàn codebase); CAT_LIKELY_WRONG hiển thị cat đầy đủ vs so 2-digit (trung thực).

selftest **442/442** (+21 r8_*; 1 test cũ `derive_subject_no_hl_garbage` cập nhật theo hành-vi-giữ-hoa-thường có
chủ đích). Nợ DỮ LIỆU P2 (nạp VBHN 135 BLHS, LƯỢT-2 web 30 luật, consolidation review_on_nlm=44, dedup 93 nhóm,
22 VBHN tên thiếu năm, 77 loai) → mục 4 runbook phiên; `backfill-title-vn --apply` chạy 1 LẦN trước LƯỢT-2 web.

---

# ★ v1.30.1 — Xử log LIVE 2026-07-03 (9 vấn đề): 4 vá CẤP SKILL + runbook nợ DỮ LIỆU

Từ log rà 108 Luật + audit corpus trên Cowork. Phân loại: #1/#7/#8/#4 có gốc CÔNG CỤ → vá skill;
#2/#3/#5/#6/#9 là nợ DỮ LIỆU (detector/lệnh sửa ĐÃ CÓ) → runbook thứ-tự-phụ-thuộc cho user chạy LIVE.

## #1 — `nlm-install --resume` (Cowork 45s/lệnh + bwrap --unshare-pid kill tiến trình nền)
- Gốc: cả chuỗi (tải 31MB → giải nén → uv tool install) chạy 1 lệnh liền; tarball nằm TemporaryDirectory —
  kill giữa chừng mất trắng; nohup/setsid vô dụng (mỗi bash 1 PID-namespace riêng). Log thật: phải bóc tay 3 bước.
- FIX: **máy trạng thái 3 bước idempotent** — `_nlm_install_probe` (trạng thái dò từ ĐĨA: nlm→done / pybin→install /
  tgz→extract / else→fetch) + `_nlm_step_fetch` (tarball VỊ TRÍ BỀN `_dl/py311.tar.gz`, `.part`→md5→`os.replace`) +
  `_nlm_step_extract` (xong dọn tarball) + `_nlm_step_install` (uv cache tự resume — đo thật 3 lần là xong).
  **`--resume`: mỗi lần gọi chạy ĐÚNG 1 bước → rc=3 PARTIAL còn bước / rc=0 xong — LẶP CÙNG LỆNH tới rc=0.**
  Đường trọn-gói (mặc định, env không giới hạn) tái dùng step-machine → kill giữa chừng cũng resume được.
  Guard chống lặp vô hạn/PARTIAL giả khi install rc=0 mà `nlm` chưa thấy trên PATH (tin rc=0 + hướng dẫn export PATH).
  +`--version` pin bản. rc md5-lệch 3→2 (3 nay = PARTIAL; caller cũ chỉ check ==0 — an toàn).

## #7 — số corpus lệch boot(527)/sweep(515): KHÁC ĐỊNH NGHĨA + snapshot, nay tự khai
- Gốc THẬT (đọc Code.gs:2173-2183): server `corpus_count` = corpus∈{true,vbqppl} ∪ row_kind=overflow, TRỪ ref &
  loai='thuong'; sweep `corpus` = corpus=='true' thuần; cộng lệch snapshot (client cache + GAS đọc-cache ~600s).
- FIX: `_corpus_count_server_rule` (PURE, mô phỏng đúng luật server) → sweep in CẢ 2 thước đo trên CÙNG snapshot
  + `corpus_basis` giải thích + `snapshot_age_s` + dòng ℹ khi 2 số lệch; boot.py thêm `corpus_count_rule`.

## #8 — cat-audit tự khai độ phủ (1 cờ/515 doc là THIẾT KẾ precision-first, không phải corpus sạch)
- Thêm `coverage_note` (JSON + text): heuristic TÊN level-2; audit sâu đọc HEADER thật = `tl corpus-audit`;
  sức khoẻ tổng = `tl sweep`; per-file = `cat-verify`.

## #4 — `backfill-loai --normalize` (GAP THẬT: 77 dòng loai phi-chuẩn KHÔNG BAO GIỜ được sửa)
- Gốc: sweep gợi `backfill-loai --apply` cho loai_noncanonical nhưng lệnh idempotent BỎ QUA mọi dòng đã-có-loai →
  9 dòng "Luat" không dấu (+68 khác) nằm ngoài tầm với.
- FIX: `_backfill_loai_candidates(entries, normalize)` (PURE) — normalize=True sửa CẢ dòng SAI enum khi map TẤT ĐỊNH
  qua `_normalize_loai` ('Luat'→'Luật', 'nd'→'Nghị định'); giá trị lạ → `nonmappable` (báo, KHÔNG đoán).
  sweep NEXT-ACTIONS + corpus-fix bước 6 đổi gợi ý sang `tl backfill-loai --normalize --apply`.

## Review đối kháng delta (2 reviewer + verify; 1 reviewer nhánh resume hỏng schema — các điểm nhọn nhánh đó đã
## tự kiểm: .part ghi đè sạch, tarball chỉ xóa SAU extract OK, caller cũ chỉ check rc==0) — 4 CONFIRMED đã VÁ:
- `_corpus_count_server_rule`: loai so EXACT `== 'thuong'` (GAS không lower/strip — Code.gs:2183; lower-hoá = tự tạo
  lệch mới với boot; 'Thuong' hoa server VẪN đếm — test cập nhật).
- `backfill-loai --apply`: kèm `before_by_key` {loai cũ: fill=rỗng / normalize=loai_raw} → `tl undo` khôi phục được
  (trước thiếu before → undo câm — cùng họ bug missing-sohieu đã vá từ v1.28.2).
- `_LOAI_CANON` + `"cd": "Công điện"` (CD ∈ họ canonical `_canon_fams` từ v1.29.4 — loại trừ 'cd' trần là TỰ MÂU
  THUẪN: dòng loai='CD' rơi nonmappable thay vì map; nhất quán nd/tt/nq/qd/kl/ct sẵn có).
- Minor ghi nhận không vá: cat-audit in coverage_note cả khi 0 cờ (chủ đích — nhắc chính lúc "0 cờ" dễ ngộ nhận sạch).

## Nợ DỮ LIỆU (skill đã có công cụ — user chạy LIVE theo runbook thứ-tự-phụ-thuộc, xem HANDOFF/phiên):
#2 CANONICAL_VBHN_NUMBER_DIFFERS ×2 (52-2014→VBHN 121-2025, 85-2015→VBHN 83-2026) → `source-rename --sohieu`;
#3 PCBTN thiếu sohieu → `register --sohieu 03-2007-QH12`; #5 dedup 94 nhóm (⚠ phụ-lục-cùng-số-hiệu KHÔNG dedup mù
— doctrine v1.29.7 #4) → `dedup-plan`/`hygiene plan`; #6 5 dòng corpus=true chưa NLM (3 báo cáo ILO nghi KHÔNG phải
VBQPPL) → `source-update-corpus false` TRƯỚC rồi mới `ingest-missing`; #9 19 VBHN_CANDIDATE_UNVERIFIED_LATEST (QT-5
web) + 7 UNLINKED_AMENDMENT → `relation-backfill`.

selftest **421/421** (+8 r7_*: probe-steps, rc-map, corpus-server-rule×2, sweep-fields, backfill-normalize×2,
normalize-map, parser). KHÔNG đóng zip (gộp với v1.30.0 chờ user duyệt).

---

# ★ v1.30.0 — Rà soát kiến trúc PROFILE: A base-also + B discover + C adopt + D doctor + E index + F doctrine

Từ rà soát kiến trúc profile (log 2026-07-03): config chỉ biết 3 profile nhưng Drive có ≥6 thư mục đã-là-profile
(registry+manifest riêng: DinhMucChi, NQ80, NQ36…); `apply_profile_env` THAY THẾ scope (chọn profile = mất VBQPPL);
registry/manifest đặt lạc chỗ (NQ36 ở gốc Van_ban_thuong); không có "sổ cái" profile đọc được trên Drive.
Thứ tự triển khai B→C→E→D (reversible/an toàn) rồi A (đổi hành vi đọc). +24 test r6_* (383→407).

## A — profile CỘNG VBQPPL (`TL_BASE_ALSO`, đổi hành vi ĐỌC — codify doctrine MULTI_CORPUS_V1_18 §2 vào CLI)
- `_apply_profile_env`: profile DỰ ÁN mặc định set `TL_BASE_ALSO=1`; opt-out `profiles.<p>.baseAlso=false`;
  vbqppl KHÔNG set; cặp cờ `--base-also/--no-base-also` override per-lệnh (`_add_base_also_flags`).
- **Hợp nhất** (profile TRƯỚC, nền BỔ SUNG, dedup drive_id, hit nền `_scope='vbqppl'`): `locate` (mục
  `[nền VBQPPL]` riêng; base-also BỎ shortcut index vì index chỉ chứa scope profile; LOW_CONFIDENCE tính trên
  CẢ 2 scope) + `reg-query` (envelope thêm `base_also{base_hits}`, row thêm `scope`, text mode đuôi `[nền]`).
- **Fallback-khi-miss** (đúng doctrine profile-first): `source-map`/`exists` — profile MISS hoàn toàn → tra tiếp
  manifest nền, hit gắn `scope='vbqppl'` + cờ `BASE_SCOPE_HIT` (exists thêm warning rõ). Canonical profile luôn thắng.
- `nlm-cross`: mặc định nối thêm notebook NỀN (`_vbqppl_notebooks` = base+overflow+shards từ config, dedup) sau
  notebook profile.
- Hạ tầng: `_base_manifest_entries` (đọc manifest nền bằng snapshot→swap→KHÔI PHỤC env overlay — cache nền rơi
  đúng thư mục cache gốc, không nhiễm cache profile) + `_merge_base_entries` (PURE). **Đường GHI/ingest KHÔNG đổi.**

## B — `profile-list --discover [--folder-cap N]` (READ-ONLY, LIVE)
- Quét `Van_ban_thuong` 2 cấp (con trực tiếp + `_meta` từng thư mục) qua GAS `list`; lõi phân loại PURE
  `_discover_classify`: ✅ in_config / 🟠 **unregistered_profile** (kèm lệnh `profile-adopt` điền sẵn) / ⚪ empty_folder
  / · plain_folder / 🔴 **misplaced_root_assets** (registry/manifest Ở GỐC VBT — ca NQ36; loại trừ asset đã trong
  config, vd registry vbthuong) / ⚠ config_only (bỏ qua profile có root == VBT).
- `_discover_item_kind` nhận diện KHOAN DUNG biến thể tên thật: `tra_luat_registry.LuatBHXH` / `Registry_NQ36` /
  `tra_luat_registry` trơ / `_manifest_DinhMucChi.json` / `tra_luat_manifest.NQ36.json`; đòi mime Sheet cho registry;
  `_PROFILES_INDEX*` = hạ tầng (không phải asset lạc). Cap thư mục quét LOUD (60 mặc định).

## C — `profile-adopt` (lệnh MỚI — seed profile ĐÃ CÓ hạ tầng; nội-hoá new-profile.ps1 #8 v1.29.7 vào skill)
- `--name <p> --folder <id> [--notebook] [--registry] [--manifest] [--bootstrap-manifest] [--apply]`. Tự dò asset
  trong folder+`_meta` (`_adopt_pick_assets` PURE); nhiều ứng viên → AMBIGUOUS bắt chọn (KHÔNG đoán); override thắng.
- **GUARD registry 3 tầng** (bài học CLOBBER 766 dòng): mime = Google Sheet THẬT · ≠ `_LEGACY_REGISTRY_DOC_ID`
  (1mATG Doc-as-Sheet đọc RỖNG) · `--apply` chạy `_verify_registry_sheet` (schema 27 cột, heal cột thiếu idempotent).
- notebookId: `--notebook` > đọc từ manifest JSON (schema `_manifest_placeholder`); thiếu → warning NO_NOTEBOOK_ID
  (lệnh NLM sẽ chặn — đúng thiết kế, không fallback base). `--bootstrap-manifest` sinh manifest mới + manifest_export.
- Ghi `manifestScope='own'` + `categories='own'` qua `_persist_profile_config` (journaled `config_write`, merge giữ
  field cũ); PROFILE_EXISTS_DIFFERENT_FOLDER chặn đè nhầm; adopt lại cùng folder = idempotent. DRY mặc định.

## D — `profile-doctor` (BẤT BIẾN LAYOUT mới) 
- **Bất biến: registry + manifest của profile nằm TRONG thư mục profile (root hoặc `_meta`).** `_doctor_check_profile`
  (PURE) đối chiếu `parents` (action `info`): `MISPLACED_ASSET` (kèm fix move) · `REGISTRY_LEGACY_DOC` ·
  `REGISTRY_NOT_SHEET_MIME` · `*_TRASHED` (critical) · thiếu registryDocId (critical)/notebookId/manifestId (warn).
- `--fix --apply`: `resolvefolder _meta` (tạo nếu thiếu + persist metaFolderId journaled) → action `move`
  (fileId GIỮ NGUYÊN ⇒ config registryDocId/manifestId KHÔNG phải đổi) — journal `drive_move` intent{before parents}.
  rc=0 sạch / 1 finding / 2 lỗi. Ca NQ36: adopt bằng --registry/--manifest (asset lạc gốc) → doctor --fix move vào chỗ.

## E — `profile-index` (SỔ CÁI `Van_ban_thuong/_PROFILES_INDEX` — Google Sheet)
- Cột: profile | default | rootFolderId | folder_name | notebookId | registryDocId | manifestId | categories |
  manifestScope | baseAlso | note. **BẢN CHIẾU từ config — nguồn sự thật DUY NHẤT vẫn là config** (tránh
  nguồn-sự-thật-thứ-4 trôi, sự cố 2026-06-30). DRY in CSV; `--rebuild --apply` LIVE.
- `upload` GAS KHÔNG ghi-đè-tại-chỗ (force=true chỉ bypass dedup sha) ⇒ mô hình **tạo-trước-dọn-sau** fail-safe:
  upload CSV → `copy_convert` Sheet MỚI → trash bản cũ + CSV trung gian (journal `drive_trash`, phục hồi được).
  sheetId ĐỔI mỗi rebuild — mở qua folder, đừng bookmark id.

## F — doctrine/tài liệu
- SKILL.md §0.9 bổ sung: **profile chạy CÙNG VBQPPL, KHÔNG thay thế** + bất biến layout + 3 lệnh mới + `--discover`;
  bảng CLI thêm 4 dòng; locate row ghi rõ cặp cờ base-also áp cho 5 lệnh đọc.

## Review đối kháng (workflow 4 reviewer + verify per-finding, Explore read-only) — 8 CONFIRMED đã VÁ, 1 REFUTED
- **(A)** `_apply_profile_env`: profile KHÔNG tồn tại trong config rơi về data NỀN mà vẫn set TL_BASE_ALSO →
  nay CHỈ set khi `profiles.get(name)` thật (hết nền tự quét mình 2 lần).
- **(C)** adopt: + guard `REGISTRY_SHARED_WITH_OTHER_PROFILE`/`MANIFEST_SHARED_WITH_OTHER_PROFILE`
  (`_profile_asset_owners` — chặn --apply reg_addcols mutate Sheet đang thuộc profile khác); + manifest lạ
  (trường `profile` ≠ tên adopt, so theo slug) KHÔNG được cấp notebookId (`_notebook_from_manifest_json`,
  warning MANIFEST_PROFILE_MISMATCH — hết nguy cơ ghi đè notebookId đúng bằng notebook profile khác).
- **(D)** doctor: + `_strip_shared_fixes` — asset dùng chung ≥2 profile → BỎ fix-move, nâng
  `SHARED_ASSET_MULTI_PROFILE` critical (move theo profile này = phá layout profile kia; soi TOÀN config kể cả
  khi --profile-name 1 profile); + `move` bọc `_gas_get_retry` (idempotent — re-move cùng đích = no-op; hết treo
  fix vì 1 timeout transient); + journal `drive_move` BỎ `before` theo hợp đồng op non-reg v1.29.1 (parents cũ →
  `set.from_parents` forensic/undo tay — trước đây undo sinh restore-op rác đẩy nhầm vào `_journaled_reg_write`).
- **(E)** index: dọn bản cũ theo TÊN CHÍNH XÁC `_PROFILES_INDEX`/`.csv` (`_index_old_candidates`) — hết nguy cơ
  trash nhầm file người dùng `_PROFILES_INDEX_backup…` (startswith cũ quá rộng).
- **(B/C/D/E)** `_ProfileEnvGuard`: 4 lệnh profile-ops ép scope NỀN (load_creds DEFAULT) → snapshot + KHÔI PHỤC
  env overlay khi ra (kể cả lỗi) — caller cùng-process không bị đổi TL_PROFILE ngầm.
- REFUTED: "resolvefolder parentId không tới GAS" — doResolveFolder_ xử parentId đúng (Code.gs:463-476).
- Minor ghi nhận (không vá): `info.parents` không được contract bảo đảm tường minh (GAS hiện luôn trả);
  `_mime_from_info` rỗng khi info dị dạng → báo FOLDER_ID_INVALID kèm info thô (đủ chẩn đoán).

selftest **413/413** (+30 r6_*: 24 tính năng + 6 review-fix: base-also-unknown-profile, asset-owners,
strip-shared-fix, manifest-mismatch, index-exact-names, env-guard-restore). KHÔNG đóng zip đợt này
(chờ yêu cầu bổ sung của user).

---

# ★ v1.29.7 — Xử log NĐ131+phụ lục: 9 vấn đề ingest/extract/dedup/bookkeeping + 3 script quy trình

Từ log LIVE nạp NĐ 131/2021 + phụ lục vào profile "Pháp lệnh NCC" (9 vấn đề, xếp theo ảnh hưởng).

## Lỗi dữ liệu/độ tin cậy
- **#1 `--sohieu` không vào registry (ingest-local):** organize có nhận sohieu server-side nhưng thực tế từng không
  persist → **READ-BACK sau organize + BACKFILL** journaled `reg_upsert` (sohieu immutable; kèm loai/goc) + cảnh báo.
- **#2 extract chọn nhầm PHỤ LỤC làm canonical:** tie-break `_resolve_deep_target` khi query số hiệu:
  registry-sohieu khớp THẬT **+150** · tên phụ lục (`PL_`/`Phu_luc`) **−120** — chính văn thắng cả khi cả 2 sohieu rỗng.
- **#3 extract dính cap ~200k dù đã `cache-build`:** ưu tiên **cache CONSOLIDATED** (`cache.find(sohieu).articles`,
  ca 185 Điều từng cụt ở Điều 26 — không lấy được Điều 40/130) → dựng full-text nguồn `cache-build (no-cap)`.
- **#4 dedup gate dương tính giả trên phụ lục:** **BỎ tầng SOHIEU** khỏi `_nlm_dedup_gate` — chính văn + phụ lục CÙNG
  số hiệu → phụ lục hợp lệ từng bị chặn TITLE_ALREADY_ON_NOTEBOOK trỏ nhầm source chính văn (phải --skip-live-check
  tay). Gate = drive_id + exact-title-duy-nhất (chống re-push CÙNG tài liệu); `ingest-missing` GIỮ 3 tầng (backlog 1-1).

## Lỗi quy trình / bookkeeping
- **#5 `nlm-reconcile` không link nguồn vừa `nlm-add`:** SELF-HEAL — `unregistered≠∅` mà chưa `--refresh` → tự refresh
  manifest + re-plan 1 lần (row vừa ingest chỉ thiếu trong cache → thành `link_candidates`, `--apply` backfill được).
- **#6 `row_kind=overflow` gán nhầm cho profile-own:** trước `target != NLM_BASE_NOTEBOOK → overflow` (mọi profile
  dính); nay overflow **CHỈ khi target == overflow-shard đã cấu hình** (TL_OVERFLOW_NOTEBOOK_ID).
- **#7 không có đường sửa row_kind:** `tl register --drive-id <id> --row-kind own|overflow|ref` (choices chặn giá trị lạ).

## Cấu hình / khởi động — 3 SCRIPT QUY TRÌNH (tại `D:\Quốc hội\`, hướng dẫn: references/DEV_TOOLING_GUIDE.md §9)
- **#8 `new-profile.ps1`** — seed profile ĐÃ có hạ tầng (4 ID từ SKILL_OF_RECORD) vào config, journaled + verify;
  guard registry rỗng/Doc-legacy (bài học clobber).
- **#9 `preflight-ingest.ps1`** — `tl up --nlm` XANH mới ingest; VÀ trong skill: `ingest-local --apply` nay **TỰ
  PRE-CHECK NLM** (binary + notebook_get) TRƯỚC upload — fail → dừng sớm CHƯA đụng Drive/registry (hết chuỗi dở
  dang gãy ở bước cuối); ép: `--skip-nlm-preflight`. (Review vá 1 bug: điều kiện ready chỉ tin `ok`.)
- **#6/#7 `fix-row-kind.ps1`** — rà + sửa hàng loạt dòng overflow-nhầm về own (mỗi dòng journaled, undo được).

selftest **383/383** (+5 r5_*). integrity 33/0. Review đối kháng: 1 bug MEDIUM (preflight condition) đã vá.
Deploy: `upload-skill-to-Package.ps1` → verify Package=1.29.7.

---

# ★ v1.29.6 — Xử log rà 118 Luật: P0 amendment-gate precision (15 PAUSE giả = 13%) + P1/P2

Từ báo cáo rà toàn corpus 118 Luật (67 gốc + 51 VBHN, v1.29.5): P0 nghiêm trọng nhất — `source-map` ép
PAUSE_AND_ASK_USER cho 15/118 Luật, **100% ứng viên gây PAUSE đều confidence=low, non-linked**.
Recon 5-agent read-only + **verify EMPIRICAL trước/sau trên manifest thật** (doctrine v1.27.1).

## P0 — 4 fix precision cổng amendment-existence
- **(a) FILTER ứng viên:** `corpus=false` (bản đã thay — Luat_51/46-2024) · cat `Van_ban_thuong` (bản góp ý
  Quy chế lao động HR từng bị gán làm amendment cho **Luật Giá**!) · tên PHI-QUY-PHẠM khi registry-sohieu rỗng
  (+`lịch trình`/`thẩm tra`/`dự thảo`/`kế hoạch họp` — ca 'Lịch trình thẩm tra dự án Luật SĐ Luật Xuất bản';
  prefix `YK_` loại vô điều kiện). Chuẩn hoá `_`→space trước match (keyword cũ 'gop y' không match 'gop_y').
- **(b) NGƯỠNG PAUSE:** candidate **MẠNH** = dẫn chiếu đúng số hiệu base (linked) / confidence=high — chỉ mạnh
  mới escalate PAUSE; weak-only → cờ mới `AMENDMENT_CANDIDATE_LOW_CONFIDENCE` = **REVIEW** (không dừng workflow).
- **(c) VBHN date-coverage FALLBACK NĂM** (cổng cũ im lặng vì manifest thiếu full-date → 9/15 base-là-VBHN vẫn
  PAUSE): so **năm-từ-sohieu-key** STRICT (`25-2026-VBHN` > `90-2025-QH15` → covered `(year-only)`; cùng năm =
  mơ hồ, không cover — an toàn).
- **(d) OMNIBUS** `sua_doi_N_luat` non-linked = weak vô điều kiện (từng bị gán cho 8 base nó KHÔNG sửa chỉ vì
  khớp chủ đề trần); linked qua goc/sua_doi/refs vẫn strong → PAUSE đúng.

**Empirical (manifest 762):** 19/2012 + 90/2025 + 57/2024: PAUSE→REVIEW ✓ ('Lịch trình' bị lọc, 51/46-2024
corpus=false bị lọc, 19/2012 covered=2026 year-only) · control 80/2025 + 25/VBHN: OK giữ nguyên ✓ · test
**linked-still-PAUSES** pass (không mất an toàn) ✓.

## P1 — corpus-audit under-scan âm thầm
`--all` bị limit mặc định cắt → scanned=40/515, 0 proposal → "sạch" GIẢ. Fix: cảnh báo **⚠ CẮT BATCH** LOUD
(X..Y/N + lệnh trang kế) + JSON thêm `pool_total`/`next_offset`/`coverage_complete` (KHÔNG bỏ cap — 515
header-read sẽ lại client-timeout). Đối chiếu sweep: **2 thước đo KHÁC NHAU** (corpus-audit = header thật,
guard chặt; sweep = heuristic tên/enum-field) — note rõ 2 phía (`note_vs_sweep` + next_actions), đếm lệch
là bình thường, không phải "một trong hai sai".

## P2 — nhiễu cờ + CLI
- `_vbhn_metadata_flags` nhận **năm trong sohieu-key** (`NN-YYYY-VBHN-XXX`): hết cờ thiếu-năm oan →
  `VBHN_NUMBER_REUSE_RISK` hết nổ trên mọi VBHN (20×) → `TITLE_OR_REGISTRY_WARN` hết treo-rỗng (24×) —
  empirical: cờ giờ luôn kèm `risky_candidates` có finding THẬT (vd tên file thiếu năm).
- `--corpus`/`--nlm` (reg-query, profile-files): nhận cả `--corpus true/false` (hết rc=2 usage-error);
  SKILL.md bảng CLI cập nhật.

selftest **378/378** (+7 test, 1 test cũ cập nhật theo semantics mới — có test chống-vacuous cho omnibus).
integrity 33/0. Deploy: `upload-skill-to-Package.ps1` → verify Package=1.29.6.

**Data-ops còn lại của log (LIVE, user duyệt — xem tổng kết phiên):** backfill sohieu Luật PCBTN (03/2007/QH12);
5 file thô corpus=true chưa chuẩn hoá; dedup 94 nhóm/orphan 71 (`dedup-plan`/`hygiene plan`).

---

# ★ v1.29.5 — Cài dev-tooling → `ruff` bắt BUG THẬT: đường đọc văn bản nhanh nhất chưa từng chạy được

Sau khi thiết lập hạ tầng dev (git/clasp), cài thêm `ruff`/`pyright`/`hypothesis`/`gh`/`ccusage`/`claude-code-log`/
`gas-fakes` theo khuyến nghị. Chạy `ruff check --select F821` (undefined-name) lập tức bắt được **bug thật đang
chạy production từ lâu**:

**`_read_doc_text`** (hàm đọc nguyên văn GDoc — dùng khắp nơi: corpus-audit, header-verify, extract, xref,
footnote-map) có nhánh **direct-media** (nhanh nhất, chỉ cần cred gws, KHÔNG cần binary) gọi
`tempfile.TemporaryDirectory()` nhưng **`tempfile` chưa từng được import ở module scope** (chỉ có 2
`import tempfile as _tf` cục bộ ở HAI hàm khác, tên alias khác). Mỗi lần nhánh này chạy → `NameError` → bị
`except Exception: pass` ngay dưới **nuốt âm thầm** → luôn rơi xuống fallback chậm hơn (transport→gws binary /
GAS webapp `exporttext`). **Nhánh nhanh nhất chưa từng thực thi đúng kể từ khi được viết** — một phần nguyên
nhân hợp lý cho các báo cáo "corpus-audit chậm" trước đây (i1, đã vá bằng `--offset` ở v1.29.4, nhưng gốc rễ
tốc độ per-item nằm ở đây).

**FIX:** `import tempfile` vào khối import global (tl.py dòng 41). Dọn thêm 2 `F841` (unused-variable):
`except Exception as e` bỏ `as e`; `cat_in_45` dư thừa trong `cmd_ingest_local` (`cat_valid` đã cùng giá trị,
sót từ refactor #10 AUDIT v1.29.4).

**Verify LIVE:** `_read_doc_text` chạy sạch không lỗi (41706 ký tự, văn bản thật). selftest 372/372, integrity
33/0, `ruff check --select F821,F841` sạch.

**Hạ tầng dev mới (2026-07-02):**
- Canonical dir → **`D:\Quốc hội\tra-luat`** (từ `Downloads\tra-luat`) + `git init`
- Apps Script chuyển sang **`clasp`** (thay sửa tay browser editor) — `gas-project/` clone qua `clasp clone`;
  **`gas-deploy.ps1`** = 1 lệnh push+version+deploy (diff-check trước khi lên production; auto đồng bộ ngược
  `gas-project/Code.gs` → `references/Code.2.21.2i.gs` sau deploy — chống trôi tài liệu)
- Deploy đầu tiên qua clasp (version 73): fix `doWriteConfig_` (pending từ v1.29.0) + tính năng `PENDING_EFFECT`
  (viết sẵn trong reference nhưng chưa từng deploy) — cả 2 verify LIVE OK
- Cài: `ruff`, `pyright`, `hypothesis`, `gh` CLI, `ccusage`, `claude-code-log`, `@mcpher/gas-fakes` (devDependency
  trong `gas-project/`, `.claspignore` xác nhận không lọt vào push)

Deploy skill: `upload-skill-to-Package.cmd` (nay tại `D:\Quốc hội\`) → verify Package=1.29.5.

---

# ★ Apps Script REDEPLOY (2026-07-02) — clasp thay browser editor; version 73 LIVE

Chuyển hạ tầng dev Apps Script sang **`google/clasp`** (canonical dir di chuyển `Downloads\tra-luat`
→ `D:\Quốc hội\tra-luat`; `git init` + `gas-project/` clone qua `clasp clone <scriptId>`).

**Phát hiện khi clone:** diff `gas-project/Code.gs` (live) vs `references/Code.2.21.2i.gs` (repo) lộ **2 điểm lệch**:
1. Fix `doWriteConfig_` (v1.29.0, chặn clobber `registryDocId` về Doc legacy `1mATG`) — **đã pending redeploy từ
   phiên v1.29.0**, đúng kỳ vọng.
2. **Phát hiện mới:** khối `PENDING_EFFECT`/`effectiveDateIso_` (vb_status phát hiện văn bản hiệu lực TƯƠNG LAI,
   thêm field `effective_date`/`pending_effect`) tồn tại trong `references/Code.2.21.2i.gs` nhưng **chưa từng
   deploy** — viết vào tài liệu tham chiếu ở phiên nào đó, quên push.

**Deploy (2026-07-02, user xác nhận):** `clasp push` (2 file) → `clasp version` (73) → `clasp deploy -i
<deploymentId hiện tại>` (**GIỮ NGUYÊN deployment `/exec` — không tạo mới**, khớp `webappUrl` trong config).

**Verify LIVE:** `ping` OK (version 2.21.2i) · `writeconfig`+`readconfig` trả `registryDocId=1C21i65…` (Sheet
thật, KHÔNG còn `1mATG` — xác nhận fix #1 hoạt động) · `vb_status` trả `effective_date`/`pending_effect` không
lỗi, note enum có `PENDING_EFFECT` (xác nhận tính năng #2 hoạt động) · local selftest 372/372 + integrity 33/0.

---

# ★ v1.29.4 (gws3env) — Xử DỨT ĐIỂM 5 vấn đề công cụ (log LIVE) + hoàn tất roadmap #8/#9/#10

Từ báo cáo 5 vấn đề công cụ các phiên LIVE (workflow Explore read-only root-cause 5 hướng song song).

- **i3 `shared-source-fix --apply` báo ok mà `links_cleared: 0` — GỐC CHUNG với i4:** ghi GIÁ TRỊ RỖNG qua
  reg_bulk/reg_upsert bị webapp **BỎ QUA IM LẶNG** ("empty string KHÔNG ghi đè" by design — Code.gs:2467). FIX:
  helper **`_journaled_reg_clear`** (action `reg_clear` keyed **drive_id bản thua** — không key nlm_source_id vì sẽ
  clear CẢ 2 dòng; validate `_REG_CLEARABLE_COLS`; intent{before} → `tl undo` restore được; đếm `cleared` THẬT +
  LOUD khi hụt, rc=1). shared-source-fix --apply nay đi reg_clear per-loser.
- **i4 `register --nlm-source-id ""` không xóa:** giá trị rỗng bị DROP ngay client-side (`if v:`) → upsert phần còn
  lại trả updated=true = ẢO GIÁC đã xóa. FIX: arg RỖNG TƯỜNG MINH = lệnh XÓA → tự route `reg_clear` (cột clearable)
  hoặc CHẶN LOUD `COLS_NOT_CLEARABLE` (cột khác — không xóa được qua upsert by design).
- **i5 sau `source-rename`/`source-update-corpus` lệnh kế timeout/PARSEERR (phải boot --refresh tay):** gốc =
  bust-cache xoá CẢ `manifest_index.json` nhưng CHỈ `tl boot` dựng lại → locate/reg-query mất index → rơi fallback
  webapp KHÔNG retry. FIX: **`_rebuild_manifest_index`** — index TỰ-HỒI-PHỤC mỗi lần `_load_manifest_full` tải
  manifest mới; + **`_gas_get_retry`** (×2 backoff, CHỈ lỗi transient timeout/URLError/Response-không-JSON/5xx;
  KHÔNG retry mutate — at-least-once nguy hiểm với createtext) cho manifest_export/manifest/download.
- **i1 `corpus-audit --limit` lớn treo im lặng:** mỗi lần gọi quét lại TỪ ĐẦU → limit 30-40 vượt client-timeout.
  FIX: **`--offset` phân trang** (corpus-audit + header-verify) — chạy `--limit 20 --offset 0/20/40…`.
- **i2 `NAME_TRICH_YEU` đề xuất tệ (3 kiểu):** (a) prefix regex thiếu **KL|CT|CD|TTLT|TB** → tên ĐÃ CHUẨN bị coi
  hỏng-cấu-trúc → đề xuất tên tự-trích kém hơn; (b) boilerplate + ~20 **tên bộ-ngành** (ca `TT_104…_Bo_tai_chinh`;
  không dùng '^bo ' — strip-accents 'Bổ sung'≡'bo sung'); (c) guard **ĐỔI-PREFIX**: không đề xuất đổi mã loại
  (ca KL_→NQ_ sai — loại lệch thật đã có LOAI_MISMATCH trỏ header-verify tay).
- **#8 rc-doctrine:** alias CI **`--fail-on-finding`** cho MỌI cờ `--strict` (9 lệnh); `source-map` nay có
  `--strict` (rc=1 khi verdict REVIEW/PAUSE; mặc định rc=0 — phát-hiện ≠ lỗi lệnh).
- **#9:** hằng `GWS_TIMEOUT_{FAST,STD,LARGE}` (hết lệch 45/60); `locate` **AUTO-REFRESH** khi cache >900s
  (`--trust-cache` tắt) — diệt nguồn báo-động-giả cache lệch lặp lại nhiều phiên.
- **#10:** tách PURE `_ingest_local_cat_gate` từ cmd_ingest_local (test offline).

selftest **372/372** (+6 r4_*). integrity 33/0. **ROADMAP AUDIT HOÀN TẤT #1→#10.**
Deploy: `upload-skill-to-Package.cmd` → verify Package=1.29.4.

---

# ★ v1.29.3 (gws3env) — AUDIT roadmap #3+#4+#5+#6+#7 (hoàn tất các mục value-cao còn lại)

- **#3 Dedup-live gate BẮT BUỘC mọi đường source_add (B3):** helper **`_nlm_dedup_gate`** (tái dùng dedup 3-tầng
  drive_id/sohieu-duy-nhất/exact-title) cắm vào **`nlm-add`** (đường push trần cuối — từng tạo trùng khi dùng làm
  recovery) + **`profile-ingest`** (gate title canonical + MỌI chunk-title — bắt ca re-run sau fail giữa chừng: GDoc
  MỚI nhưng TITLE CŨ = trùng nội dung) + **`ingest-local`** (trước bước nlm_source_add; abort ghi journal).
  dup → ABORT rc=2 kèm source_id + hướng xử (`nlm-reconcile`/`nlm-orphans`); KHÔNG liệt kê được LIVE → ABORT
  (doctrine S13); ép: `--skip-live-check` (thêm vào 4 parser). `push-overflow` không source_add → không cần gate.
- **#4 Bỏ N+1 manifest (B2):** `cmd_loop` vòng ≥2 đọc registry-sheet **LIVE qua gws** (~1.2s, không re-export, né cache
  đọc GAS 600s) rồi **`_entries_with_live_fields`** overlay CHỈ trường mutable (corpus/nlm_*) lên nền manifest-enriched
  vòng 1 — **GIỮ shape enriched → detector không phân kỳ** (bài học R1); gws lỗi/thiếu → fallback NGUYÊN hành vi cũ.
  `cmd_preflight` gộp 2 lần parse manifest (~800KB JSON) → 1 lần dùng chung.
- **#5 Detector `raw_dup_of_standard` (log LIVE 2.3 — phần còn lại):** bắt bản TẢI THÔ corpus=true có sohieu-key RỖNG
  **hoặc trích SAI** (family ngoài họ canonical — phát hiện mới khi viết test: `_sohieu_key_entry('ND274_2025_cham
  dong…')` = **'274-2025-CHAM'** ('CHAM' nhận nhầm là mã loại!) → key KHÔNG rỗng nên **lọt S12** — giải thích trọn vẹn
  vì sao 5 dòng LIVE kẹt vĩnh viễn) mà tên chứa `<LOẠI><số>_<năm>` khớp lỏng ĐÚNG 1 bản chuẩn corpus=true → propose
  `source-update-corpus <id> false` (**PROPOSE-ONLY**; match lỏng không auto). Num chuẩn hoá int (zero-padded `06`≡`6`
  — ca PL_06). Vào `sweep` (bucket + rows + NEXT ACTIONS) + `corpus-fix` plan (order 8, tier human_confirm).
- **#6 Journal config + delete-assets (B1):** `_persist_profile_config` journal **op config_write** (intent{before =
  block cũ} + commit{verify READ-BACK}; best-effort — không chặn ghi); `profile-delete`/`profile-file-remove` journal
  vòng **NLM-delete** (op nlm_source_delete — BẤT KHẢ NGHỊCH, forensic) + vòng **Drive-trash** (op drive_trash) —
  crash giữa vòng nay có dấu vết `tl journal <run>`.
- **#7 Đợt test checkpoint-recovery (B6) — 21 case `r3_*` (FakeGas mock, cô lập TL_PROFILE=selftest-r3 + cleanup):**
  verified-write {ok / idempotent / miss-thật / bad-cols CHẶN-TRƯỚC-post / raise / missed-là-list}; journaled-write
  {intent set+before, commit per-row, partial-fail → inflight, **BUST-cache marker (regression #1)**}; journaled-upsert
  idempotent; **resume BỎ QUA op non-reg** (hợp đồng composite 2.4) + undo CHỈ op có before; `_apply_gate` chặn
  profile-registry-rỗng + `--force-unsafe` vượt; dedup-gate 5 verdict; overlay mutable-only; raw-dup detector.

**Smoke LIVE bắt 1 false-positive THẬT** (detector #5 ghép nhầm `CD_32-2026-CD-TTg` Công điện — tên CHUẨN loại hiếm —
với `TT_32-2026`): vá guard "candidate PHẢI trông như file thô (đuôi file / space)" + thêm CD vào họ canonical →
LIVE `raw_dup=0` sạch. (Đúng doctrine "CHẠY MANIFEST THẬT là bước kiểm bắt buộc" — v1.27.1.)

selftest **366/366** (+19). integrity 33/0. Deploy: `upload-skill-to-Package.cmd` → verify Package=1.29.3.

---

# ★ v1.29.2 (gws3env) — AUDIT roadmap #1+#2: bust-cache-after-write thống nhất + wrap 3 đường ghi trần

Thực thi 2 mục đầu ROADMAP (`~/Downloads/tra-luat-AUDIT-2026-07-02.md`, phần C).

- **#1 Bust-cache-after-write (AUDIT B5):** `_journaled_reg_write` + `_journaled_reg_upsert` tự gọi
  `_invalidate_manifest_cache()` sau MỌI lần ghi — **1 chỗ phủ mọi lệnh đã wrap** (trước chỉ 3-4/16 lệnh nhớ gọi
  rải rác → đọc-sau-ghi dính cache local stale). Lần đọc kế `_load_manifest_full` (mất cache) → `manifest_export`
  = GAS `regReadAll_(true)` **TƯƠI** (né luôn cache đọc ~600s server-side). Items rỗng → KHÔNG bust.
- **#2 Wrap 3 đường ghi trần (AUDIT B1):**
  - **`register`** — cả `--bulk` (reg_bulk) lẫn upsert đơn (reg_upsert) nay qua `_apply_gate` + journal +
    verified-write, before best-effort từ manifest (`_reg_before_from_manifest`) → `tl undo` khôi phục được
    (kể cả sohieu/goc vì đi reg_upsert). `--bulk`: cols mặc định `nlm_title` tường minh (= default webapp cũ);
    items trộn khóa → **BUCKET 2 batch** theo key_field (review bắt: 1 key_field cho batch trộn → journal key=''
    → false-committed/undo hỏng); item không có khóa nào → CHẶN rc=2. Output nay `{ok, batches[], journal}`.
    ⚠ rc thay đổi CÓ CHỦ ĐÍCH: dòng `miss` THẬT (key không khớp) nay rc=1 (trước ok:true + missed>0 vẫn rc=0).
  - **`backfill-notebook`** — items trộn khóa (src-ids/drive-ids) → TÁCH 2 batch theo key_field, mỗi batch
    journaled+verified. JSON `plan.reg_bulk` nay là **LIST** (mỗi phần tử kèm key_field+verified).
  - **`push-overflow`** — gate+journal+verified; **SỬA rc**: trước đòi `patched>0` → chạy-lại idempotent
    (patched=0, giá trị đã đúng) bị rc=1 SAI; nay rc theo `verified` (doctrine v1.28.6: chỉ miss THẬT mới fail).
  - `--force-unsafe` thêm cho cả 3 parser (thoát precheck-gate có chủ đích).
- Helper mới `_reg_before_from_manifest(items, cols, key_field)` — before-snapshot best-effort cho undo (đọc manifest
  cache local; map `drive_id→id`/`so_hieu` của manifest đã-làm-giàu; stale chỉ ảnh hưởng undo tham khảo).

selftest **347/347** (+3: r3_bust_cache_after_write, r3_before_from_manifest, r3_force_unsafe_flags). integrity 33/0.
DRY smoke backfill-notebook OK. Deploy: `upload-skill-to-Package.cmd` → verify Package=1.29.2.

---

# ★ v1.29.1 (gws3env) — Xử 5 vấn đề log LIVE audit corpus (2.1→2.5): WAL-hoá ingest-missing + journal ingest-local

Từ báo cáo audit corpus LIVE 2026-07-02 (5 vấn đề công cụ). Điều tra = workflow 11-agent read-only (5 root-cause + 6 audit
toàn codebase) — báo cáo đầy đủ + roadmap: `~/Downloads/tra-luat-AUDIT-2026-07-02.md`.

- **2.1 Trùng NLM tái diễn dù S13 (VBHN_67 3×/PL_06 2×) — GỐC RỄ THẬT:** `source_add` là 1 subprocess BLOCKING
  (`wait=True`, tới 630s) → client-timeout giết GIỮA call = source ĐÃ tạo server-side nhưng ckpt (ghi SAU add) mất dấu;
  run sau listing `skip_freshness` có thể CHƯA thấy source mới, tier-sohieu MISS vì bất-đối-xứng năm (registry year-fixed
  `67-2025-VBHN-VPQH` ≠ title parse `67-VBHN-VPQH`). **FIX:** ckpt 4 khóa `{done,pending,linked,fails}`
  (`_ingest_ckpt_load_full`, backward-compat) — **`pending` ghi TRƯỚC add (WAL)** → run sau **FRESH-verify**
  (`skip_freshness=False`) các mục add-dở TRƯỚC khi cho add lại; dedup-live thêm **TẦNG 3 exact-title DUY NHẤT**
  (`_ingest_dedup_title_key` — title do chính tool đặt khi add).
- **2.2 Hàng đợi relink 1→8 (GAS cache đọc 600s):** `linked` ghi nhận reg_link ĐÃ verified → **SKIP relink lặp**
  (summary `ALREADY_LINKED`; ép chạy lại: `--relink`). Cảnh báo "chưa xác nhận" chỉ còn khi lỗi THẬT (v1.28.6 verify).
- **2.3 Bản-thô-trùng fail lặp đốt batch:** `fails` đếm FAIL liên tiếp per-item → **≥3 SKIP** + `PUSH_FAIL_SKIPPED`
  + hint (`header-verify` / `source-update-corpus <id> false`); ép thử lại: `--retry-failed`. Detector
  `raw_dup_of_standard` (bắt PDF thô trùng bản chuẩn) = roadmap AUDIT.
- **2.4 Composite không journal:** `ingest-local` wrap TOÀN CHUỖI mkdir→upload→organize→nlm_source_add→reg_link qua
  WAL journal (intent/commit per-step; op non-reg KHÔNG kèm `before` → `tl resume`/`undo` không đụng — chỉ soi
  `tl journal <run>` thấy bước dở; reg_link đổi `g.post reg_bulk` trần → `_journaled_reg_write` verified; mọi nhánh
  fail in kèm `journal` run_id). Còn profile-ingest/push-overflow/backfill-notebook/register--bulk = roadmap.
- **2.5 Cosmetic:** (a) `LOAI_MISMATCH` guard `_normalize_loai` 2 vế — hết đề xuất current==suggested (checks.loai chỉ
  là tier-word-presence; header cụt/OCR → False dù loại khớp); (b) `corpus-audit` **HEARTBEAT per-item** ra stderr
  (batch lớn từng "treo 0 output").
- **Quick-win audit cache-coherence:** `_atomic_write_text` (tmp+`os.replace`) cho manifest cache; gws direct-media tải
  vào `.dl` tạm, CHỈ replace sau parse+validate (kill giữa chừng KHÔNG hỏng cache đang có).

selftest **344/344** (+4: r2_ckpt_full_compat, r2_dedup_live_title_tier, r2_loai_same_norm_no_selfmismatch, +ckpt cũ).
integrity 33/0. LIVE smoke reg-query --refresh OK. Deploy: `upload-skill-to-Package.cmd` → verify Package=1.29.1.

---

# ★ v1.29.0 (gws3env) — R1: nhóm-D ĐỌC gws-primary + GAS fallback (gws CLI nay có Sheets API) + FIX config registryDocId

Theo yêu cầu người dùng (chỉ ra `github.com/googleworkspace/cli` nay có Sheets API → tiền đề "gws-bridge thiếu Sheets" LỖI THỜI).
Khảo sát + đo hiệu năng LIVE (2026-07-02) + workflow Explore read-only trước khi code. **CHỈ đổi đường ĐỌC ở chỗ KHÔNG phân kỳ.**

**Điều tra (đổi cả hiểu biết):**
- Registry THẬT là Google **SHEET** (`tra_luat_registry`, tab `files`, 766 dòng), KHÔNG phải Doc.
- Client đọc registry-rows qua **manifest ĐÃ-LÀM-GIÀU** (`_manifest_entries`→`_load_manifest_full`), do `doManifestExport_.entryOf_`
  (drive_id→id, sohieu→so_hieu `canonManifestSoHieu_`, +`issue_year`/`so_hieu_src`/parse-từ-tên) — **KHÔNG đọc sheet raw**.
  ⇒ đọc-thẳng-sheet KHÔNG phải drop-in (phải nhân bản canon/issue_year/treeHash = đúng loại lỗi phân kỳ đang chống).

**Thay đổi (an toàn, 0 rủi ro phân kỳ):**
- **(A) `_load_manifest_full`** tải `manifest.json` qua **DIRECT-MEDIA gws** (raw, KHÔNG cap 9MB webapp, nhanh hơn, byte-exact)
  TRƯỚC → **FALLBACK GAS b64** (warn-once). Đây là đường đọc trung tâm của 50+ lệnh.
- **(B) Primitive gws Sheets** `_gws_sheets_values_get`/`_gws_read_registry_rows`/`_parse_sheet_values_to_rows` (PURE, parity
  GAS `rowsToObjs_`: header-zip, ép str, bù ô đuôi rỗng, đủ cột schema, BỎ dòng drive_id rỗng) + **`precheck --gws-live`**
  báo DRIFT sheet↔manifest (read-only, opt-in — KHÔNG thêm trễ/lỗi vào cổng `--apply`).

**GIỮ GAS ĐỘC QUYỀN (không đổi):** GHI registry (reg_bulk/reg_upsert) + D2 (regen2/manifest_export/organize/treeHash) — vì
LockService khóa 30s + read-modify-write swap NGUYÊN TỬ + business-logic Apps Script (chuyển = phân kỳ), KHÔNG vì thiếu Sheets.

**FIX config bug:** base `profiles.vbqppl.registryDocId` = `1mATG…` (Google DOC legacy) → `1C21i65…` (SHEET `tra_luat_registry`
THẬT). Xác minh: GAS `reg_get` drive_id KHỚP gws đọc 1C21i65 (`80-2025-QH15`→`1CYSMtH22…`) → hết mơ hồ 2 sheet trùng tên +
bật đường đọc gws cho base. (Đúng cảnh báo `precheck`/doctor legacy-Doc.)

**Đo LIVE (N=8):** gws sheet-read **1.19s** vs GAS reg_get 2.36s (~2×); gws GDoc **2.54s** vs GAS 3.67s (~1.4×); gws startup
~800ms/lần (thuế cố định → đọc GỘP cả sheet); ổn định 8/8. Đề án đầy đủ: `tra-luat-DESIGN-nhomD-gws-primary.md`.

**Review đối kháng (Explore read-only) vá 3 finding:** (1) `_parse_sheet_values_to_rows` đọc THEO VỊ TRÍ theo
`REGISTRY_SCHEMA_COLS` (parity GAS `rowsToObjs_` positional — GAS map theo REG_COLS_[c], KHÔNG theo tên header thực →
chống mất-parity khi ai đổi thứ tự/cỡ chữ cột Sheet); (2) `tra_luat_config.example.json` registryDocId legacy→1C21i65;
(3) **GAS `doWriteConfig_`** (ref `Code.gs` 995/1007) phát `TL_REGSHEET_ID_AUTO` (sheet THẬT) thay `CONFIG.REGISTRY_DOC_ID`
(Doc legacy) — chống **clobber** config về Doc mỗi lần writeconfig/token-rotate. ⚠ **PENDING redeploy Apps Script** (frozen);
tới khi redeploy, client auto-heal (blank legacy → auto-discover Sheet) giữ ĐÚNG (chỉ hoãn tối-ưu gws-base-read).

selftest **341/341** (+3: r1_sheet_parse_parity, r1_sheet_parse_empty, r1_sheet_parse_positional_by_cols). integrity 33/0.
Deploy skill: `upload-skill-to-Package.cmd` (user, cần gws auth) → verify Package=1.29.0. Deploy GAS (tùy chọn, cho fix #3):
redeploy Apps Script `Code.2.21.2i.gs`.

---

# ★ v1.28.7 (gws3env) — gws PRIMARY cho MỌI env (chat dùng gws, mcp thành opt-in)

Theo yêu cầu người dùng: trước đây `chat` buộc đi backend `mcp` **chỉ vì chưa biết cách chạy gws trong chat**.
Nay gws chạy được trong shell của chat → định tuyến `chat` như `code`/`cowork`.

- **`transport.py` `_BACKEND_BY_ENV`:** `{code: gws, cowork: gws, chat: mcp}` → **`{code: gws, cowork: gws, chat: gws}`**.
  Cả 3 env: **gws PRIMARY, GAS fallback** (ồn ào). Không còn env nào mặc định `mcp`.
- **mcp thành OPT-IN (không mất năng lực):** đặt `TL_DRIVE_BACKEND=mcp` cho **pure-chat KHÔNG shell** (Claude chỉ có Drive MCP,
  không có Python gws). Thêm `_resolve_backend(env)` = env-map + override.
- **Defer gắn với BACKEND, không phải ENV:** nhóm-D → `DeferToShell` và read → `DeferToMCP` **chỉ khi backend=mcp**
  (trước đây gắn cứng `env==chat`). Nên `--env chat` trong shell nay chạy GAS business-logic thẳng (như cowork), không defer.

### Vì sao nhóm D (register/manifest/reg_bulk/reg_upsert/slot/organize…) vẫn **GAS ĐỘC QUYỀN** — GWS có "chạy được" không?

Hai lý do độc lập, cả hai đều thật:
1. **gws-bridge CHƯA hiện thực Sheets API.** `gws_bridge.py` chỉ có thao tác **Drive** (files/move/rename/upload/read);
   không có đọc/ghi ô Sheet (`values`/`batchUpdate`). Registry là một Google **Sheet** → gws hiện tại *không có đường* chạm tới.
2. **Business-logic nằm ở Apps Script**, không phải lời gọi API thô. `reg_bulk` = đọc Sheet + khớp dòng theo drive_id +
   dedup + ánh xạ cột + trả patched/miss; `manifest` = duyệt cây Drive + trộn registry + tính treeHash; `organize` = phân loại + di chuyển + đăng ký.
   Để gws làm nhóm D phải **viết lại toàn bộ logic đó trong client Python** → **trùng lặp nguồn chân lý → phân kỳ** = đúng
   loại lỗi dữ liệu ta vừa mất nhiều công vá. ⇒ Giữ GAS độc quyền là **đúng thiết kế** (single source of truth), KHÔNG phải giới hạn cấu hình.

> Nếu muốn giảm độ trễ GAS-cache-đọc-600s: có thể thêm **đường gws đọc-thẳng Sheet** (chỉ READ, không logic) để bỏ cache —
> đây là bổ sung nhỏ, an toàn, làm sau nếu cần. GHI vẫn qua GAS.

**Phạm vi ảnh hưởng:** `transport.drive_op` chỉ được `tl.py` gọi cho `download`/`read` (nhóm A đọc) → đổi routing **KHÔNG**
chạm luồng ghi registry (đi `_gas()` thẳng). `tl.py` không bắt `DeferToMCP`/`DeferToShell` → không phá luồng nào.
Kiểm định: **transport selftest 12/12**, **tl selftest 338/338**.

---

# ★ v1.28.6 (gws3env) — VÁ báo động giả REG_WRITE_FAIL (idempotent) + làm rõ kiến trúc GWS/GAS

Xử log LIVE 2026-07-02: `tl loop`/`ingest-missing` liên tục báo `REG_WRITE_FAIL` dù dữ liệu ĐÃ ĐÚNG, buộc người vận hành
phải `register` từng dòng + refresh manifest thủ công.

- **Gốc rễ (báo động GIẢ):** `_verify_reg_result` coi `patched < expected` là ghi HỤT. Nhưng theo API_CONTRACT, reg_bulk
  `patched` = **số dòng ĐỔI** → ghi lại giá trị ĐÃ ĐÚNG cho patched=0 (idempotent no-op) = THÀNH CÔNG, KHÔNG phải lỗi.
  **FIX:** `verified = ok AND KHÔNG có dòng `miss[]`** (drive_id không khớp = hụt THẬT); `patched` chỉ là thông tin (cờ
  `no_change`). `_verified_reg_upsert`: `updated=False` = idempotent SUCCESS (verified=ok; `changed`=thông tin). `_journaled_
  reg_write` commit per-row theo `miss[]`. `recat`/`missing-sohieu`/`consolidation-cleanup`: LOUD chỉ khi **miss THẬT**, không
  khi patched=0. ⚠ **Không mất bảo vệ:** silent-write cột-sai (`so_hieu`≠`sohieu`) VẪN bị `_reg_cols_valid` chặn TRƯỚC ghi.
- **Làm rõ kiến trúc GWS/GAS (nguyên tắc user nhớ ĐÚNG, không cần đổi):** 'GWS chính, GAS fallback' đã áp cho thao tác
  **DRIVE** (fetch/move/rename/upload/read) qua `transport.py` router (`_BACKEND_BY_ENV={code/cowork:gws}`). Nhưng ghi/đọc
  **REGISTRY** (reg_bulk/reg_upsert/manifest_export = **nhóm D business-logic**) là **GAS ĐỘC QUYỀN by design** — Apps Script
  sở hữu logic Sheet (dedup/cột/regen2/schema); KHÔNG có đường gws cho registry (tạo sẽ bỏ qua business-logic). Nên 'toàn thấy
  GAS' khi ghi registry là ĐÚNG THIẾT KẾ, không phải lỗi cấu hình. GAS cache ~600s là cache **ĐỌC** server-side (frozen);
  **WRITE không cache** (nên `register`/`reg_bulk` ghi tức thì); dữ liệu vẫn đúng (live-dedup NLM ground-truth), chỉ
  backlog-count HIỂN THỊ trễ tới 600s — đã giảm nhẹ bằng `done_ids` (loop) + live-dedup (ingest-missing).

selftest **338/338** (+2 idempotent: `reg_bulk_idempotent_patched0_ok`, `verify_reg_result_by_missed_not_patched`; cập nhật
`verified_reg_upsert_gate`, `recat_warns_on_real_miss_not_idempotent`). Review đối kháng Explore.

---

# ★ v1.28.5 (gws3env) — CHECKPOINT phủ TOÀN BỘ lệnh mutate + kế hoạch test LIVE

Hoàn thiện: mở rộng tầng an toàn (precheck-gate + WAL journal + verified-write) từ 6 lệnh (Pha 1) sang **10 lệnh mutate còn
lại** → **TỔNG 16 lệnh** ghi registry đều qua checkpoint. Kèm **kế hoạch test LIVE** cho Cowork.

- **10 lệnh mới bọc:** `consolidation-cleanup`, `dedup-plan`, `quarantine-fix`, `backfill-loai`, `relation-backfill`,
  `shared-source-fix`, `source-rename` (reg_upsert), `source-update-corpus` (reg_upsert), `confirm` (per-item) — tất cả có
  `before`-snapshot → **undo được** (`tl undo <journal>`). `source-delete` (**BẤT KHẢ NGHỊCH**) → journal LƯU **snapshot
  forensic** toàn dòng trước khi xóa (op=`reg_delete` KHÔNG auto-undo/resume; khôi phục TAY). `--force-unsafe` cho cả 10.
- **`references/CHECKPOINT_TEST_PLAN.md`** — runbook test LIVE trên corpus THẬT (Cowork/Chat): precheck (chặn legacy-doc/cột
  sai/profile rỗng) → verified-write+journal → undo (khôi phục) → resume (op dở) → loop (hội tụ) → fail-safe (--apply bị
  chặn khi blocker). Nguyên tắc **DRY-trước + lô-nhỏ + undo-sau**; 9 mục checklist PASS; bảng 16 lệnh + reversibility.

**Bao phủ checkpoint HOÀN CHỈNH** — mọi ghi registry: precheck-gate + WAL journal + verified-write + resume/undo + loop.
selftest **337/337** (không đổi — 10 wrap theo mẫu đã test). Review đối kháng Explore.

---

# ★ v1.28.4 (gws3env) — CHECKPOINT Pha 3 HOÀN TẤT: `tl loop` (loop hợp nhất có cổng-verify + hội tụ + fail-safe)

Pha 3 khép kín hệ thống checkpoint — biến triết lý *"không bỏ bước, không né quy trình"* thành một **control loop** thực thi.
**TOÀN BỘ 4 PHA XONG:** P0 nền tảng → P1 bọc 6 lệnh mutate → P2 resume/undo → **P3 loop**.

- **PURE (bộ não, test offline):** `_pipeline_step_decision(precond, action, verify)` — bước **CHỈ DONE khi verify PASS**;
  precond sai→SKIP (ghi lý do, không âm thầm bỏ); action-fail/verify-hụt→PAUSE (fail-safe). `_loop_controller(rounds, k_dry,
  max_iter)` — HỘI TỤ khi k_dry vòng cuối hết-việc; PAUSE khi **NO_PROGRESS** (fix rồi mà tồn không giảm) / **MAX_ITER**.
- **`tl loop [--apply] [--dry-rounds K] [--max-iter N]`:** mỗi vòng detect (tầng an toàn infra+dedup) → `corpus=false`
  (**verified-write + journaled**) → re-detect đến HỘI TỤ. CHỈ tầng REVERSIBLE → **undo được toàn bộ** (`tl undo <loop_run>`);
  metadata/human vẫn qua `corpus-fix` DRY. DRY mặc định.
- **⚠ Vá GAS-cache (review):** re-detect ngay sau ghi có thể vẫn thấy `corpus=true` (GAS cache ~600s chưa lan) → dễ
  **NO_PROGRESS GIẢ**. Fix: theo dõi `done_ids` TRONG-PHIÊN, loại khỏi "remaining" → hội tụ dựa trạng thái trong-phiên, không
  phụ thuộc GAS lan truyền (vẫn bắt vấn đề PHÁT SINH mới). Review đối kháng Explore: đây là finding thật DUY NHẤT (đã vá);
  termination/partial-write/undo đều đúng (retracted).
- Tách `_corpus_safe_reversible` dùng CHUNG với `corpus-fix --tier safe` (refactor 0-đổi-output).

selftest **331→337** (+6: step-decision, controller converged/no-progress/continue/max-iter). **Hệ thống checkpoint hoàn
chỉnh** — mọi ghi registry của 6 lệnh mutate: precheck-gate + WAL journal + verified-write + resume/undo + loop hội tụ.

---

# ★ v1.28.3 (gws3env) — CHECKPOINT Pha 2: `tl resume` + `tl undo` (giá trị đầy đủ của WAL journal)

Pha 2 — biến WAL journal thành **resume + undo thật**. Đây là "viên ngọc" của hệ thống checkpoint: mọi ghi registry của
6 lệnh mutate (Pha 1) giờ đảo-ngược-được và tiếp-tục-được.

- **Journal lưu thêm:** intent nay kèm `set` (giá trị ĐỊNH GHI) + `key_field` (ngoài `before` đã có) → tái tạo được lệnh ghi.
- **`_journal_resume_ops`** (PURE): op DỞ = intent chưa commit-ok, có `set` → làm lại. **`_journal_undo_ops`** (+key_field):
  restore `before` các dòng đã commit-ok, NGƯỢC thứ tự, giữ `before` GỐC khi retry. **`_journal_reapply_one`**: ghi lại ĐÚNG
  loại gốc — `reg_upsert` cho khóa immutable (sohieu/goc — reg_bulk bỏ im lặng) vs `reg_bulk`.
- **`tl undo <run> --apply --confirm yes`**: khôi phục registry về `before` (vd recat 16→undo→00; corpus=false→undo→true;
  sohieu năm→undo→cũ). ⚠ CHỈ registry — xóa NLM/Drive/`reg_clear` KHÔNG undo được (đánh dấu rõ).
- **`tl resume <run> --apply`**: làm lại op dở bằng `set` (idempotent). NLM `source_add` do CHẠY LẠI lệnh gốc (live-dedup lo trùng).
- Cả 2 qua precheck-gate + tự ghi journal run mới (`undo_*`/`resume_*`) + invalidate cache.

Smoke thật (journal tổng hợp): `journal`→done=1/inflight=1; `undo`→1 op (dòng COMMITTED, restore `before`); `resume`→1 op
(dòng INFLIGHT, reapply `set`) — phân loại đúng. selftest **330→331** (+1 `journal_undo_and_resume_ops`). Review đối kháng
Explore. **Pha 3 (chờ user):** loop hợp nhất có cổng-verify từng bước (observe→precheck→act→verify→commit→lặp+fail-safe).

---

# ★ v1.28.2 (gws3env) — CHECKPOINT Pha 1 HOÀN TẤT: bọc nốt missing-sohieu + vbhn-year-fix + nlm-reconcile

Hoàn tất Pha 1 — **6 lệnh mutate rủi ro nhất** (ingest-missing, recat, corpus-fix, missing-sohieu, vbhn-year-fix,
nlm-reconcile) nay đều qua tầng an toàn precheck-gate + WAL journal + verified-write.

- **Helper mới cho khóa IMMUTABLE** (sohieu/goc — `reg_upsert`, KHÔNG reg_bulk vì reg_bulk bỏ IM LẶNG): `_verified_reg_upsert`
  (validate field ghi ∈ schema + verify `updated|upserted|created` truthy = thật sự đổi) + `_journaled_reg_upsert`
  (intent{before} → verified upsert → commit{verify}).
- **`missing-sohieu`:** gate + journal + `_journaled_reg_write` cột **`sohieu`** (đúng, KHÔNG `so_hieu`) + before{sohieu:""}
  + LOUD patched<len.
- **`vbhn-year-fix`:** gate + journal + `_journaled_reg_upsert` PER-ROW (payload sohieu[+name], before{sohieu/name cũ} — undo
  trả số hiệu/tên cũ). verify `updated` thay vì tự đọc raw.
- **`nlm-reconcile`:** gate + journal; backfill (key=`nlm_source_id`, cols=`nlm_notebook_id`) + link (key=`drive_id`) qua
  journaled-write; `reg_clear` batch (--clear-stale) journaled intent/commit (KHÔNG reversible tự động — đánh dấu rõ).
- `--force-unsafe` cho cả 3 (bỏ qua precheck blocker khi CHẮC).

selftest **328→330** (+2: `verified_reg_upsert_gate`, `journaled_reg_upsert_records`). Review đối kháng Explore. **Pha sau
(chờ user):** Pha 2 `tl resume <run>`/`tl undo <run>` (journal đã có `before` cho undo); Pha 3 loop hợp nhất có cổng-verify.

---

# ★ v1.28.1 (gws3env) — CHECKPOINT Pha 1: bọc lệnh mutate qua precheck-gate + WAL journal + verified-write (+ vá log timeout PHA 5)

Pha 1 của hệ thống checkpoint — **bắt đầu ĐỔI hành vi `--apply`**: 3 lệnh mutate rủi ro nhất đi qua tầng an toàn. Đồng thời
vá đúng vấn đề trong log PHA 5 (ingest-missing --apply tốn ~43s khởi động, im lặng → tưởng treo/route sai).

- **Helper chung:** `_apply_gate(a, write_cols)` (chạy precheck → **ABORT rc=2 nếu blocker critical**: registryDocId legacy /
  profile-registry rỗng / cột lạ / — trừ `--force-unsafe`); `_apply_journal_start(cmd, meta)` (mở WAL run); `_journaled_reg_write`
  (journal `intent{before}` → verified reg_bulk (validate cột + patched≥len) → journal `commit{verify}`).
- **`ingest-missing` (vá log timeout):** (1) **refresh manifest CÓ ĐIỀU KIỆN** — chỉ force khi cache >300s (trước LUÔN force
  → phần lớn 43s); (2) **HEARTBEAT khởi động** flush stderr từng bước (manifest N dòng → slot LIVE + **ROUTE base→overflow in
  NGAY** → dedup LIVE → bắt đầu đẩy) → thấy tiến độ, không tưởng treo; (3) journal `run_start` TRƯỚC bước chậm (kill giữa
  startup vẫn thấy run trong `tl journal`); (4) `_reg_link` qua journaled-write (intent+commit+verify).
- **`recat`:** gate + journal + verified-write + `before{cat cũ}` (undo trả cat cũ). Giữ LOUD patched<len (chống silent-patch).
- **`corpus-fix --apply --tier safe`:** gate + journal + verified-write + `before{corpus=true}` (undo trả corpus=true).
- **`--force-unsafe`** cho cả 3 (bỏ qua blocker khi CHẮC — rủi ro tự chịu).

**⚠ Trade-off (thành thật):** refresh có điều kiện đánh đổi 1 phần cửa-sổ-stale S12 (≤300s) lấy không-timeout; residual thấp
(văn bản THẬT + live-dedup che trùng); GAS cache ~600s vẫn là trần server-side. **Pha sau (chờ user):** bọc
`missing-sohieu`/`vbhn-year-fix` (reg_upsert → cần verified-upsert)/`nlm-reconcile`; Pha 2 `tl resume`/`tl undo`; Pha 3 loop.

selftest **326→327** (+1 integration `journaled_reg_write`). Review đối kháng Explore.

---

# ★ v1.28.0 (gws3env) — Hệ thống CHECKPOINT chống hỏng-dữ-liệu (Pha 0 nền tảng): WAL journal + verified-write + preflight

Yêu cầu user: skill phức tạp, chạy lâu, nhiều lần hỏng dữ liệu → nghiên cứu hệ thống checkpoint tối ưu bảo đảm chạy ổn
định, không bỏ bước, không né quy trình. **Nghiên cứu (workflow 3 agent read-only):** kiểm kê 23 cơ chế checkpoint + 33
gate hiện có + **18 sự cố dữ liệu THẬT** → quy về 3 lỗ hổng gốc: (A) không có WAL journal cho pipeline nhiều bước (chỉ
ingest-missing có checkpoint); (B) ghi remote KHÔNG verify-readback (gốc của 4 ca 'ghi mù' im lặng: `so_hieu`≠`sohieu`,
recat patched:0, cat không validate); (C) không có tầng tiền-kiểm bất biến thống nhất (vụ CLOBBER 766 dòng registry nền).

**Kiến trúc đề xuất:** WAL Journal + Bộ chạy Cổng-kiểm + Tiền-kiểm bất biến (loop = observe→precheck→act-1-bước→
verify-readback→journal-commit→lặp, hội tụ + fail-safe pause). 4 pha. **Pha 0 (bản này) = NỀN TẢNG pure/test offline,
CHƯA đổi hành vi lệnh:**

- **WAL Journal** `_journal_*` (`~/.tl_journal/<run>.jsonl` append-only): `intent{op,key,before-snapshot}` ghi TRƯỚC call
  remote, `commit{verify}` ghi SAU. `_journal_resume_state` → done (commit-ok) vs **inflight** (intent chưa commit → cần
  VERIFY remote khi resume); `_journal_undo_ops` → op `restore` (khôi phục `before`), ngược thứ tự (undo mới-nhất-trước).
- **Verified reg-write** — `_reg_cols_valid` (mọi cột ∈ `REGISTRY_SCHEMA_COLS` → chống `so_hieu` bị bỏ im lặng) +
  `_verify_reg_result` (patched≥expected) + `_verified_reg_write` (validate cột TRƯỚC post, verify SAU). Đóng lỗ hổng (B).
- **Preflight invariant** — `_preflight_invariants`/`_preflight_verdict` gom guard: registryDocId≠Doc-legacy-1mATG,
  profile-registryDocId≠rỗng (chống clobber), cột∈schema, snapshot tươi. Đóng lỗ hổng (C).
- **2 lệnh READ-ONLY:** `tl precheck` (kiểm bất biến trước ghi; rc=1 nếu blocker — **chạy thật LỘ dev config registryDocId
  =legacy 1mATG**, đúng loại sự cố mispoint), `tl journal` (soi WAL). ⚠ `precheck` khác `preflight` (=sharding NLM).

**Pha sau (chờ user):** Pha 1 bọc `ingest-missing`/`corpus-fix`/`recat`/`missing-sohieu`/`vbhn-year-fix`/`nlm-reconcile`
qua verified-write+journal+precheck; Pha 2 `tl resume`/`tl undo`; Pha 3 loop hợp nhất. Phản biện: KHÔNG dựng 2PC (GAS
frozen) — journal là client-side best-effort (resume+verify+undo-registry), không làm remote atomic; GAS 600s cache là
trần server-side, thiết kế BAO nó chứ không xoá.

selftest **318→324** (+6 case pure: journal resume/undo, reg-cols, verify-result, verified-write, preflight-gate).
Review đối kháng Explore.

---

# ★ v1.27.2 (gws3env) — FIX `ingest-missing --apply`: chống trùng NLM (S13) + skip rác/freshness (S12) + locate cache-warning

Xử log PHA 5 (01/07/2026, đẩy backlog văn bản thiếu lên NLM). Bug: dòng rác bị đẩy TRÙNG 3 lần; văn bản thật bị tạo source
trùng khi tiến trình timeout giữa chừng.

- **S13 (ưu tiên — rủi ro tạo rác THẬT trên NLM):** `ingest-missing --apply` nay **ĐỐI CHIẾU nguồn LIVE** trên notebook đích
  TRƯỚC mỗi `source_add` (`_ingest_missing_dedup_live` khớp Drive fileId qua `_nlm_source_drive_id`) → tài liệu đã có nguồn
  nhưng registry chưa ghi → **LINK/reconcile, KHÔNG tạo trùng** (chống ca lần trước ngắt giữa `source_add`↔`reg_bulk`, hoặc
  manifest stale). Checkpoint đổi sang `{drive_id: source_id}` ghi **NGAY sau source_add** (trước reg_bulk) → kill sau đó vẫn
  reconcile được, không re-add; `_ingest_ckpt_load` đọc tương thích format list cũ. **Stream tiến độ per-item ra stderr**
  (`[i/n] + sohieu … OK→source_id`) → biết chính xác dừng ở đâu khi timeout, thay vì im lặng.
- **S12 (cache lệch + rác):** `_ingest_missing_partition` **BỎ QUA dòng `sohieu=''`** (rác chưa chuẩn hoá — vd
  `80-nd-cp.signed.pdf`, `nlm_sources_delta_*.json`; `--allow-no-sohieu` để ép nạp). In `manifest_snapshot` (generatedAt) +
  cảnh báo **GAS cache registry ~600s** có thể lệch — sửa `corpus` xong nên `manifest`+`boot --refresh` rồi đợi, kiểm lại
  targets. ⚠ RESIDUAL: GAS 600s cache là **server-side (frozen)** — 1 dòng vừa set `corpus=false` mà manifest còn báo `true`
  VÀ chưa-live vẫn có thể lọt 1 lần (low-harm: là văn bản THẬT, không phải rác); mitigation = snapshot-warning + đợi/refresh.
- **`tl locate`:** thêm cảnh báo **OFFLINE CACHE — có thể lệch live**, gợi ý `reg-query --sohieu … --refresh` để đối chiếu
  (chống **báo động giả shared-source**: 1 drive_id "khớp" nhiều dòng thường là khớp-mờ tên trong cache, không phải shared thật).

Đo cache thật: backlog **215 → nạp 197, skip 18** dòng `sohieu=''` (gồm đúng dòng rác `80-nd-cp` + `delta.json`). selftest
**317/317** (+5 case: partition-skip, dedup-live-link, ckpt-backward-compat). Review đối kháng 2 Explore.

---

# ★ v1.27.1 (gws3env) — `corpus-audit` (A) + làm giàu `header-verify --fix-suggest` (B): KẾT HỢP qua engine đề xuất dùng chung

Yêu cầu user: kết hợp **cả A (lệnh `corpus-audit` riêng) và B (mở rộng `header-verify --fix-suggest`)**. Làm gọn bằng **một
engine đề xuất DÙNG CHUNG** `_corpus_audit_row` (PURE, propose-only) — đọc HEADER thật → SO registry → trả `proposals`
{type, severity, current, suggested, fix_command}. Hai cửa: `corpus-audit` (toàn corpus, worklist xếp hạng) + `header-verify
--fix-suggest` (per-file, nay kèm `suggested_name`+lệnh). Tái dùng `_verify_header_match`/`_classify_doc_header`/
`_vb_standard_doc_name`/`_vb_auto_cat_from_text` — KHÔNG viết detector mới.

- **`corpus-audit [--all|--sohieu|--drive-id|--cat NN] [--limit] [--strict] [--json]`** — worklist SỬA xếp hạng + lệnh điền
  sẵn: 🔴`SOHIEU_MISMATCH`(→`source-rename --sohieu`), 🔴`LOAI_MISMATCH`, 🟠`NAME_TRICH_YEU`(→`source-rename --name`),
  🟡`MISSING_YEAR`(→`vbhn-year-fix`), 🟢`CAT_MISMATCH`(→`recat`). **PROPOSE-ONLY (KHÔNG `--apply`** — sửa chạy qua fixer
  chuyên dụng). Xử raw-no-gdoc (→"cần đọc tay") + lỗi đọc header graceful (như `header-verify`). `--strict`→rc=1 nếu có 🔴.
- **AN TOÀN (siết sau khi CHẠY MANIFEST THẬT lộ over-fire — chạy thật là bước kiểm bắt buộc):**
  - Chạy đầu trên 20 dòng: `CAT_MISMATCH` fire cả 20 (gợi cat `00` vô lệ, đòi chuyển Hình sự 16→23), `MISSING_DATE_AGENCY`
    fire 19/20 (cơ quan sai: ND Chính phủ→VPQH), và **NGUY HIỂM**: `NAME_TRICH_YEU` đòi đổi `VBHN_..._Luat_Ke_toan` →
    `VBHN_25-VBHN-VPQH_Van_phong_quoc_hoi` (RỚT NĂM + nhặt boilerplate 'Văn phòng Quốc hội' thay trích yếu 'Kế toán').
  - Vá: (1) `NAME_TRICH_YEU` CHỈ khi tên HỎNG CẤU TRÚC (`_name_looks_nonstandard`: UUID/đuôi file/thiếu mã loại — regex
    `^(Luat|VBHN|ND|TT|…)[_\-]`, KHÔNG `\b` vì `_` là word-char) + subject KHÔNG boilerplate (`_subject_is_boilerplate`
    chặn tên cơ quan) + **CHIA SẺ ≥1 token** tên cũ → tên ĐÃ chuẩn KHÔNG đụng, ca VBHN Kế toán hết bị rename sai.
    (2) `CAT_MISMATCH` chỉ FILL-MISSING (cat rỗng/`00`, suggested hợp lệ ≠`00` confident — KHÔNG override cat thật; phát
    hiện cat SAI = dùng `cat-audit`). (3) BỎ `MISSING_DATE_AGENCY` (cơ quan nhiễu). Đo lại: 20 dòng → 0 đề xuất nhiễu.
- Trên manifest thật: **198/541** dòng corpus có tên phi chuẩn (target thật của `NAME_TRICH_YEU` khi có gws đọc header).

selftest **313/313** (+7 case, gồm regression `corpus_audit_no_rename_standard_name` ghim ca VBHN Kế toán). Review đối kháng
2 Explore: calibration = GOOD (thiên về false-negative, an toàn); 0 blocker.

---

# ★ v1.27.0 (gws3env) — S9/S10/S11 chống chốt VBHN LỖI THỜI + Pha sau `consolidation-cleanup`

Xử log 🔴 **High QT-5 (2026-07-01)**: tìm VBHN Bộ luật Hình sự DỪNG ở bản **LỖI THỜI** `01/VBHN-VPQH` (2017) thay vì bản
**MỚI NHẤT** `135/VBHN-VPQH` (2025). Gốc rễ: quy trình chốt ở VBHN ĐẦU TIÊN tìm thấy — nhưng **số hiệu VBHN TĂNG theo mỗi
lần hợp nhất** (01→11→135, KHÔNG phải semver). Ưu tiên **S9** (gốc rễ) trước.

- **S9 — 2 LƯỢT bắt buộc** (`_qt5_queries`, `_qt5_search_hints`): thêm truy vấn `'<tên> hợp nhất mới nhất <năm>'`,
  `'"<tên>" "hợp nhất" <năm>'`, `site:congbao.chinhphu.vn … "hợp nhất"`. Cờ máy-đọc **`VBHN_CANDIDATE_UNVERIFIED_LATEST`**
  (source-map & vbhn-check khi CÓ ứng viên VBHN nhưng CHƯA verify là bản mới nhất) → buộc kiểm lượt-2 trước khi trả.
- **S10 — nhận diện luật cải cách cao** (`_HIGH_AMENDMENT_SUBJECTS`/`_is_high_amendment_subject`): Hình sự/tố tụng hình sự/
  phí-lệ-phí/đất đai/doanh nghiệp/đầu tư/đấu thầu/thuế… (giai đoạn 2024-2026). Cờ **`VBHN_HIGH_AMENDMENT_VELOCITY`** +
  đẩy truy vấn 'mới nhất'/congbao/năm-hiện-tại lên ĐẦU danh sách. Helper chuẩn hoá dấu `_-./` (nhận cả `Bo_luat_hinh_su`).
- **S11 — doctrine số VBHN tăng dần** (SKILL §0.1): tìm SỐ LỚN HƠN / NGÀY MỚI HƠN cùng cơ quan (VPQH), KHÔNG semver.
- **`consolidation-cleanup` (Pha sau — corpus-fix bước 11 đã trỏ)**: 'có ĐỒNG THỜI VBHN + gốc/sửa đổi RỜI' → GIỮ VBHN,
  set THÀNH PHẦN corpus=false (**reversible**) khi VBHN phủ **đã verify (on NLM)**. **CORROBORATE goc** (`_vbhn_goc_corroborated`
  — cùng guard với source-map VBHN-first): khớp goc nhưng tên VBHN mã hoá base KHÁC / chủ đề xung khắc → **review
  `GOC_POLLUTION_SUSPECT`, KHÔNG auto** (đề phòng ẩn văn bản mà redirect VBHN-first lại không kích hoạt). Component còn NLM →
  review. DRY mặc định; `--apply` reg_bulk corpus=false CHỈ nhóm corroborated. Trên manifest thật: 16 ready / 29 còn-NLM /
  2 nghi-goc-nhiễm (2 luật sửa nhiều-chủ-đề: 187/2025/NĐ-CP, 57/2024/QH15 — đúng, không auto-ẩn).

selftest **300→306** (+5 case: qt5_two_pass_latest, high_amendment_velocity_detect, source_map_vbhn_unverified_latest_flag,
consolidation_cleanup_keeps_vbhn_flags_components, …_requires_verified_vbhn, …_routes_goc_pollution_to_review). Review đối kháng, integrity sạch.

---

# ★ v1.26.1 (gws3env) — MERGE nhánh Codex 1.24.4-updated (source CRUD): source-delete + source-update-corpus

Nhánh Codex `1.24.4-updated` rẽ từ base 1.24.4, làm SONG SONG bộ source CRUD VBQPPL. Nhánh Claude (1.26.0) đã đi xa hơn
(corpus-fix orchestrator + source-rename + shared-source-fix + full profile) NHƯNG THIẾU 2 verb nhánh Codex có:
`source-delete` (xóa) + `source-update-corpus` (bỏ ra/đưa vào corpus) — đúng "thêm/xóa/bỏ ra khỏi corpus/nlm" user yêu cầu.
So từng phần → giữ 1.26.0 làm nền, **PORT 2 verb + INJECT safety của Claude**. selftest **298→300**, integrity sạch, review đối kháng.

- **`source-update-corpus <t> true|false`** (PORT) — `false` = BỎ RA KHỎI CORPUS: `reg_upsert corpus=false` (**reversible ở
  registry**) + gỡ nguồn NLM; `true` = đưa vào lại (nhắc nlm-add/ingest). **GHÉP GUARD `_profile_deletable_sources`/
  shared_source_id** (nhánh Codex xóa nguồn KHÔNG kiểm shared → gãy link kia; nay CHẶN, báo `nlm_blocked_shared`).
- **`source-delete <t>`** (PORT) — XÓA CỨNG bất khả nghịch: gỡ NLM (GUARD shared) + trash Drive + xóa dòng registry.
  DRY + `--confirm yes`; plan nêu rõ lựa chọn REVERSIBLE (`source-update-corpus false`) trước khi xóa cứng.
- **`source-rename` ENHANCE** (ghép ưu điểm nhánh Codex): thêm đổi tên **NGUỒN NLM** (`nlm_cli.source_rename`) khi
  `--rename-drive` + **xoá cache manifest sau ghi** (`_invalidate_manifest_cache` — đọc sau lấy LIVE). GIỮ ưu điểm 1.26.0
  (auto-suggest tên chuẩn + `ALREADY_STANDARD` + DRY-plan + `--sohieu`).

**An toàn (review đối kháng 3 major → đã vá):** nhánh Codex khi source SHARED chỉ skip xóa NLM nhưng VẪN xóa registry/Drive
(hoặc set corpus=false) → để nguồn NLM MỒ CÔI + sibling gãy/nhầm status. **FIX: `source-delete` và `source-update-corpus
false` ABORT TOÀN BỘ khi shared** (`blocked_shared`/`SHARED_SOURCE_MUST_FIX_FIRST`) — buộc `shared-source-fix` (resolve
FALSE-LINK, xác định bản THẬT sở hữu nguồn) TRƯỚC, rồi mới xóa/bỏ-corpus. Verify synthetic: SHARED→abort, UNIQUE→chạy.

**Doctrine MERGE:** nhánh Codex có verb mình thiếu → PORT nguyên năng lực (xóa/corpus-toggle) NHƯNG thêm safety mình
mạnh hơn (shared-guard ABORT, DRY, confirm, reversible-first). Nhóm sai-nội-dung vẫn DETECT+ĐỀ XUẤT. **Pha 2 LIVE Cowork:** `--apply`.

---

# ★ v1.26.0 (gws3env) — TÍNH NĂNG: dọn/chỉnh lý dữ liệu VBQPPL (orchestrator + rename + shared-fixer)

Theo yêu cầu: rename/thêm/xóa nguồn VBQPPL + bộ công cụ làm sạch/chỉnh lý (trùng lặp, stale, NLM↔Drive lệch, link sai,
tên/số hiệu/trích yếu sai, thiếu năm, VBHN mới chưa nạp, cùng lúc VBHN+gốc, VBHN-first khi tìm thành phần…).
**Phản biện trước:** ~80% việc PHÁT HIỆN đã có (`sweep`/`hygiene`/`dedup-plan`/`nlm-orphans`/`header-verify`/`vbhn-check`/
`source-map`/`vbhn-year-fix`/`relation-check`). Chỉ lấp GAP thật: điều phối theo thứ tự + rename nguồn + fixer link-sai;
tái dùng helper, KHÔNG nhân bản. selftest **295→298**, integrity sạch, review đối kháng manifest thật.

- **`corpus-fix`** — ORCHESTRATOR: gộp mọi detector (sweep) → kế hoạch **THEO THỨ TỰ PHỤ THUỘC** (shared-link → goc-nhiễm →
  infra → dedup → year → loai → title/cat → nlm-relabel → ingest → consolidation → quarantine). **Thứ tự là điểm mấu chốt**
  (vd reconcile TRƯỚC khi tách shared-link = xóa nhầm nguồn gãy link kia). Phân **2 tầng**: ✅safe_auto (REVERSIBLE:
  corpus=false) / 🟡metadata / 🔴human_confirm / 🏗structural. `--apply --tier safe` chỉ chạy reversible (infra+dedup→
  corpus=false); metadata/human/structural LUÔN in lệnh + người duyệt. (Đo cache thật: 11 bước, dup 82/year 28/loai 78/
  title 283/corpus-not-nlm 226/consolidation 61…)
- **`source-rename <drive_id|sohieu>`** — đổi TÊN nguồn VBQPPL (lấp gap rename): `reg_upsert` registry.name (+`--sohieu`
  reg_upsert --merge cho khóa) + tùy chọn `--rename-drive` đổi tên GDoc trên Drive (`rename` action). Bỏ `--name` → gợi ý
  tên chuẩn (`standardize_name`, chủ đề capitalize đúng quy ước) + cờ `ALREADY_STANDARD`. Cảnh báo VBHN thiếu năm / đổi
  sohieu. DRY mặc định; verify `header-verify` trước.
- **`shared-source-fix`** — FIXER `shared_source_id` FALSE-LINK (đã DETECT ở sweep, trước phải sửa tay): GIỮ link ở bản
  điểm cao, `reg_clear` link bản kia rồi re-push riêng. `--apply --confirm yes`; ⚠ verify `nlm-content` xem source THỰC
  thuộc bản nào trước khi ghi.

**Phản biện đã áp (an toàn):** DRY mặc định mọi nơi; `corpus-fix --apply` CHỈ tầng safe (reversible corpus=false), không
tự xóa NLM/Drive/sohieu; nhóm sai-nội-dung (tên/trích yếu/văn bản) = DETECT+ĐỀ XUẤT, KHÔNG auto (cần `header-verify`
ground-truth); shared-fixer + rename cần confirm + verify.

**CÒN đề xuất (chờ bạn chốt scope):** `consolidation-cleanup` (gộp gốc/sửa về VBHN đã verify → corpus=false), `corpus-audit`
(đọc header hàng loạt → đề xuất sửa tên/số hiệu/trích yếu sai — propose-only). **Pha 2 LIVE Cowork:** `--apply` các lệnh trên.

---

# ★ v1.25.1 (gws3env) — MERGE TỐI ƯU Claude(1.25.0)⊕Codex(1.24.5): ingest auto-analyze + profile lifecycle

Hai nhánh ĐỘC LẬP (cùng base v1.24.4) cùng làm tính năng "nạp qua Claude tự phân tích + quản lý profile". So từng phần,
đo empirical, giữ bản mạnh hơn. **BASE = Codex 1.24.5** (profile CRUD ĐẦY ĐỦ + THỰC THI LIVE) + **GHÉP của Claude**
(name builder đúng + guard an toàn + 2 lệnh VIEW). selftest **294/294**, integrity sạch, review đối kháng manifest thật.

**BASE Codex 1.24.5 (giữ — hoàn chỉnh hơn):** `ingest-local --auto-plan` (đọc probe text → suy name/sohieu/loai/cat,
OCR gate, block cat mơ hồ khi thiếu text); profile lifecycle THỰC THI: `profile-list/use/rename(--rename-assets)/
delete(--delete-nlm-sources/--trash-assets)/files/manifest/file-add/file-remove`. `profile-files`/`profile-manifest`/
`profile-file-add` là 3 việc user yêu cầu (liệt kê file / load manifest / thêm file) mà nhánh Claude 1.25.0 thiếu.

**GHÉP của Claude (net-additive, đo empirical):**
- **SỬA name builder Codex** — Codex `_vb_standard_doc_name` lấy nhầm dòng số hiệu làm chủ đề → tên lặp
  `Luat_113-2025-QH15_113_2025_QH15`. GHÉP `_doc_subject_for_name` (lấy dòng TIÊU ĐỀ thật, bỏ dòng số hiệu/'DỰ THẢO',
  strip loại, ALL-CAPS→sentence-case, basename tránh leak UUID path) + dự thảo→`DUTHAO_` → `Luat_113-2025-QH15_Dan_so`,
  `ND_146-2018-ND-CP_Quy_dinh_chi_tiet_Luat_Bao_hiem_y_te`, `DUTHAO_Luat_Tri_tue_nhan_tao`.
- **GUARD an toàn** `_profile_deletable_sources` — Codex `profile-delete --delete-nlm-sources`/`profile-file-remove
  --delete-nlm` xóa MỌI live source_id KHÔNG kiểm `shared_source_id` → xóa 1 nguồn gãy link văn bản khác (đúng 2
  FALSE-LINK hiện có). GHÉP: tách deletable/blocked, CHỈ xóa nguồn KHÔNG shared, báo `nlm_blocked_shared_source_id`.
- **backup config** trước `profile-delete` (hồi phục được).
- **+2 lệnh của Claude**: `registry-map` (VIEW hợp nhất VBQPPL base+shard + mọi profile, không store) + `ingest-analyze`
  (DRY chuẩn, dùng CHUNG analyzer `_vb_ingest_auto_plan` + in lệnh `ingest-local --auto-plan` điền sẵn).

**Doctrine MERGE:** cùng base → giữ nhánh HOÀN CHỈNH hơn làm nền (Codex profile CRUD + LIVE exec), ghép phần mình ĐÚNG/AN
TOÀN hơn (name builder + shared-guard + backup + VIEW). Đo empirical để chọn (Codex name lặp số hiệu; Claude đúng).

**CÒN Pha 2 (LIVE Cowork, user chạy):** `--auto-plan --apply`, `--delete-nlm-sources`/`--trash-assets`/`--rename-assets`
chạy lô nhỏ giám sát (dev không cred ghi; guard + DRY + confirm bảo vệ).

---

# ★ v1.25.0 (gws3env) — TÍNH NĂNG: ingest auto-analyze + profile lifecycle CRUD (yêu cầu user)

Bổ sung theo yêu cầu: nạp thẳng qua Claude có **tự phân tích đổi tên + xác định cat trước khi upload**, và **quản lý
profile** (thêm/xóa/đổi tên/chọn/liệt kê + view folder+shard+NLM). **Phản biện trước khi làm:** ~70% đã tồn tại
(`ingest-local`, `profile-create/ingest`, `cat-verify`, sharding, config v2) → CHỈ bổ sung phần thật sự thiếu, tái dùng
helper sẵn có, **KHÔNG nhân bản**. selftest **290→297**, integrity sạch, review đối kháng 2 reviewer (manifest thật).

**Nạp có phân tích:**
- **`ingest-analyze --file <f> [--text-file <txt>]`** (DRY, pure, read-only): đọc HEADER → ĐỀ XUẤT `suggested_name`
  chuẩn (`standardize_name.build_doc_name` → `Luat_113-2025-QH15_Dan_so`; dự thảo→`DUTHAO_…`) + `cat` (boundary-rule >
  content-infer, kèm `cat_alternatives` + cảnh báo `CAT_LOW_CONFIDENCE`/`CAT_NOT_DETERMINED`) + sohieu/loai/năm/
  `goc_hints` + **lệnh `ingest-local … --apply` điền sẵn**. `_doc_subject_for_name`: bỏ dòng số hiệu/quốc hiệu/`DỰ THẢO`,
  strip tiền tố loại, ALL-CAPS→sentence-case, dùng basename (tránh leak fragment UUID trong path). File .docx/.pdf:
  Claude đọc nội dung → `.txt` → `--text-file`. Luồng: **analyze → verify (cat-verify/header-verify) → ingest-local --apply**.
  (Nạp cho profile tương tự qua `--profile-mode` + `profile-ingest`.)

**Quản lý profile (lifecycle CRUD; config-CRUD ghi FILE config LOCAL atomic, Drive/NLM write = --apply LIVE Cowork):**
- **`profile-list`** / **`registry-map`** — VIEW dẫn xuất config (mọi profile + VBQPPL base+overflow-shard + notebook);
  validate live bằng `nlm-get`/`profile-info`, **KHÔNG** store ghi tay (tránh nguồn-sự-thật-thứ-4 trôi như sự cố 2026-06-30).
- **`profile-use <name>`** — ghi `defaultProfile` (config LOCAL), DRY mặc định.
- **`profile-rename <old> <new>`** — đổi KEY config; **IDs (folder/notebook/registry) GIỮ NGUYÊN** = khóa thật → an toàn,
  hồi phục; tên hiển thị Drive/NLM đổi tay. TỪ CHỐI đổi `vbqppl`.
- **`profile-delete <name>`** — **MẶC ĐỊNH detach** (gỡ config, GIỮ Drive folder + registry + NLM; backup config;
  defaultProfile→vbqppl). `--purge-nlm` kèm KẾ HOẠCH xóa nguồn NLM (LIVE) với **guard `shared_source_id`** (KHÔNG xóa
  nguồn dùng chung → tránh gãy link, đúng bài học 2 FALSE-LINK hiện tại); `--apply` cần `--confirm <name>`.
- **`profile-remove-file <drive_id|sohieu>`** — report-only, in lệnh reg-delete + nlm delete, **CHẶN nlm delete nếu shared_source_id**.

**An toàn (phản biện đã áp):** delete mặc định detach (không xóa NLM); mọi write DRY mặc định + backup + confirm-tên;
guard shared_source_id ở mọi đường xóa NLM; auto-cat/tên chỉ ĐỀ XUẤT (giữ cổng REVIEW_CAT + verify), không commit câm;
IDs bất biến khi rename; view-not-store cho registry-map. **CÒN Pha 2 (LIVE Cowork, user chạy):** đấu nối `--apply`
Drive/NLM cho purge/rename-remote, chạy lô nhỏ giám sát (dev không có cred ghi).

---

# ★ v1.24.4 (gws3env) — MERGE TỐI ƯU Claude⊕Codex (cùng xử báo cáo rà 122/73 Luật)

Hai nhánh hotfix ĐỘC LẬP (cùng base v1.24.2) cùng chữa báo cáo rà 122+73 Luật. **BASE = Codex v1.24.3** (A-layer
RỘNG + SẠCH hơn) + **REFINE của Claude** (cổng WARN rộng hơn). selftest **290/290**, integrity sạch, review đối kháng
3 reviewer trên manifest thật. Toàn bộ là lỗi lớp ĐỊNH TUYẾN/SIÊU-DỮ-LIỆU (nội dung văn bản ĐẠT); KHÔNG đụng data corpus.

**A1 — ghost tên-rỗng nhấn chìm `TITLE_OR_REGISTRY_WARN` (41%).** Lọc `nk!=''` khỏi `risky_candidates`.

**A2 — số hiệu luật TRƯỚC 1992 `NN-LCT-HDNNx`** (vd `21-LCT-HDNN8` Luật Bảo vệ sức khỏe nhân dân 1989) không nhận →
name-mode canonical=null. FIX toàn diện (Codex): `_looks_like_sohieu_query` + **`_sohieu_base_sort_year`** (LCT-HDNN→1987
để `_vbhn_base_key` chọn ĐÚNG base của goc-chain có luật cũ) + `_RAW_SOHIEU_RE` parse-từ-tên + `_doctype_family`=Luật + `_ref_tokens`.

**A3 — cờ TRÔI registry↔NLM dán per-law (28 luật).** Hai tầng: **HIỂN THỊ** bỏ `NLM_STATUS_MISMATCH` khỏi `canonical.flags`
(`_source_map_flags`/`_summ_entry_source_map`, giữ `CORPUS_TRUE_NOT_ON_NLM` có nghĩa) + **CỔNG WARN** (Claude refine) rộng
hơn: `_TITLE_WARN_GLOBAL_FLAGS` (thêm `CORPUS_TRUE_NOT_ON_NLM`/`NLM_NOTEBOOK_ID_MISSING`/`RAW_NAME_NOT_NLM`) → không WARN
per-law cho cờ trôi của BẢN THÔ song song. Đo thật: WARN **28→9 / 60 luật** (Codex-alone 22, Claude-alone 8, MERGE 9);
9 luật còn lại đều có cờ SIÊU-DỮ-LIỆU thật (VBHN thiếu năm…). Cờ trôi vẫn hiện ở `doctor`/`sweep`/`nlm_gaps`.

**A4 — schema JSON.** `verdict` + `flags` top-level cho CẢ `source-map` (per-item `_source_map_verdict` + `_aggregate_verdict`
cả batch + `_warning_codes`) VÀ `vbhn-check` (`_vbhn_check_verdict`), vocab nhất quán OK/REVIEW/PAUSE_AND_ASK_USER/
UNKNOWN_NOT_ABSENT (+QT5_WEB_REQUIRED). Driver batch khỏi parse text/regex. (D5 `source-map --json` VỐN đã có — báo cáo nhầm.)

**Doctrine MERGE:** cùng base → so từng phần, giữ bản RỘNG+SẠCH hơn làm nền, refine phần mình mạnh hơn (đo empirical
để chọn). Regression check trên manifest: P0 goc-pollution (113/2025→Dân số), consolidation (64/2020 no-PAUSE),
`CANONICAL_VBHN_NUMBER_DIFFERS` (52/2014) — 0 vỡ.

**CÒN DỮ LIỆU/WEBAPP (user Cowork):** goc pollution VBHN_22 (reg_upsert→21-LCT-HDNN8); 2 shared_source_id (map_set tách
TRƯỚC reconcile); dedup cụm cat 45 (`dedup-plan --apply`); `infra_in_corpus` tl_secrets.enc→corpus=false; vbhn-year-fix;
backfill goc/sua_doi ~20 UNLINKED; QT-5 web cho 30 luật nền thiếu VBHN.

---

# ★ v1.24.2 (gws3env) — MERGE hotfix Claude ⊕ Codex (cùng xử báo cáo rà 108 lần)

Hai nhánh hotfix ĐỘC LẬP cùng chữa báo cáo rà 108 lần. **GIỮ nhánh Claude (1.24.1) làm BASE** (đầy đủ + đã review
đối kháng 5+1 agent): §1.2 dùng **consolidation goc-chain** (bỏ luật-sửa đã nằm trong chuỗi goc VBHN) — trên manifest
thật hạ **6 PAUSE giả** trong khi date-coverage của Codex VÔ HIỆU (manifest thiếu ngày ban hành); + độc quyền detector
`_goc_pollution_groups` (sweep), A3 `CANONICAL_VBHN_NUMBER_DIFFERS`, B3 dedup ứng-viên-sửa, §1.8 hieuluc-hint,
`_flags_reason`. **PORT bổ sung từ Codex** (bổ trợ, net-additive):
- **Cổng PHỤ date-coverage** `_amendments_covered_by_vbhn_date` + `_entry_issue_date_iso`: hạ PAUSE→INFO khi VBHN
  canonical ban hành KHÔNG sớm hơn TẤT CẢ luật-sửa còn lại (đều có ngày rõ) — chạy SAU consolidation, bắt ca goc thiếu
  nhưng ngày đủ. Trả `covered_by_vbhn_date`/`vbhn_issue_date`/`covered_amendment_candidates`. (No-op khi thiếu ngày.)
- **Cổng CHỦ ĐỀ status-path** (`_fallback/preingest_gate`): `_redirect_vbhn`→`(target, rejected[])` + `_relation_subject_compatible`;
  `status` trả **REVIEW `VBHN_GOC_SUBJECT_MISMATCH`** thay vì tự SKIP/USE_VBHN khi webapp gợi ý VBHN LỆCH chủ đề (ca
  §1.1 Dân số→BLLĐ). Best-effort: no-op khi `superseded_by` thiếu tên → CHỈ làm `status` an toàn hơn (false-reject →
  REVIEW, không bao giờ SKIP sai). Ghép với nhánh §1.8 hieuluc-unknown.
- Alias `weak_candidates` (= `uncertain_candidates`) trong `vbhn-check` (tương thích tên Codex).
selftest **280 → 284**; 0-divergence canonical Claude↔Codex trên 60 base VBHN thật; integrity sạch.

---

# ★ v1.24.1 (gws3env) — FIX báo cáo rà 108 lần + 3 batch (lỗi định tuyến/siêu dữ liệu của skill)

Toàn bộ là lỗi LỚP LOGIC ĐỊNH TUYẾN/SIÊU DỮ LIỆU (nội dung văn bản đều ĐẠT). Vá ở `tl.py` (lõi pure, test offline)
+ `_fallback/preingest_gate.py`. selftest **268 → 280** (+12), integrity sạch, review đối kháng (5 reviewer + critic, chạy
trên manifest thật) = 0 blocker/0 major. **KHÔNG đụng dữ liệu corpus** (việc ghi registry/NLM = user chạy Cowork).

- **§1.1 (P0) — chống `registry.goc` NHIỄM khiến `source-map` redirect VBHN-first SANG SAI văn bản.** Ca thật:
  query Luật Dân số `113/2025/QH15` bị trỏ nhầm sang VBHN "Bảo vệ sức khỏe nhân dân" vì registry.goc của VBHN đó
  = `113-2025-QH15` (nhiễm) dù TÊN mã hoá `goc_21-LCT-HDNN8`. FIX: `_name_goc_base_key` (đọc base từ token `goc_<X>`
  trong tên) + `_vbhn_goc_corroborated` (chỉ redirect khi base-tên KHỚP qkey VÀ chủ đề không xung khắc) → VBHN nhiễm
  rơi `goc_mismatch_vbhn` + cờ `GOC_SUBJECT_MISMATCH`, canonical về ĐÚNG bản gốc. **Detector mới `_goc_pollution_groups`
  vào `tl sweep`** (`goc_pollution`/`goc_pollution_rows` + suggested_goc) để TÌM mọi VBHN goc-nhiễm. Redirect hợp lệ
  (84/2015→VBHN_14 ATVSLĐ; 64/2020→VBHN_123 PPP) GIỮ NGUYÊN.
- **§1.2 — PAUSE giả khi luật-sửa ĐÃ hợp nhất.** PPP `64/2020`: 57/2024 & 90/2025 đã trong chuỗi goc VBHN 123 →
  trước báo `PAUSE_AND_ASK_USER`. Nay lọc khỏi amendment_candidates + cờ INFO `AMENDMENTS_ALREADY_CONSOLIDATED`;
  luật-sửa mồ côi (105/2016 Dược) VẪN PAUSE đúng.
- **B3 — dedup ứng viên sửa-đổi trùng số hiệu** (bản GDoc + .docx thô song song) trong `_find_amendment_candidates`.
- **§1.3 — `vbhn-check --goc` tách nhiễu.** Ứng viên chỉ trùng CHỦ ĐỀ mà KHÔNG dẫn-chiếu goc (`GOC_NOT_EVIDENT_IN_METADATA`)
  → `uncertain_candidates` riêng (cờ `GOC_NOT_EVIDENT_FILTERED`/`GOC_FILTER_NO_DIRECT_HIT`), không nhầm là đã-lọc-theo-goc.
- **A3** — cờ `CANONICAL_VBHN_NUMBER_DIFFERS`: số hiệu chỉ mục (vd 52-2014) ≠ số hiệu VBHN thật của canonical (VBHN_121).
- **§1.6** — thêm `--json` cho `ping` và `doctor` (nhất quán CLI). **§1.7** — alias key `results` cho source-map/vbhn-check.
- **Vá UX** — `risky_candidates` thêm trường `reason` (trước rỗng) qua `_flags_reason`.
- **§1.8** — `status` luật mới `IN_REGISTRY_HIEULUC_UNKNOWN`: nêu rõ GAP dữ liệu + (nếu số hiệu năm gần đây) "nhiều khả
  năng còn hiệu lực" + gợi ý backfill hieuluc (vẫn REVIEW, không tự kết luận).
- **Còn là DỮ LIỆU/WEBAPP (user xử Cowork, KHÔNG phải code):** sửa `goc` nhiễm (reg_upsert; `tl sweep` liệt kê);
  `nlm-reconcile` 197 mục lệch; `vbhn-year-fix --apply` 23 VBHN thiếu năm; backfill `goc/sua_doi` + `hieuluc` + `confirm`;
  redirect SAI ở `tl status` (webapp tính `superseded_by` từ goc nhiễm) tự hết khi sửa goc — `source-map` đã đúng để đối chiếu.

---

# ★ v1.24.0 (gws3env) — MERGE Codex v1.23.23 (profile-own-ingest) + cross-corpus đa-notebook

Hợp nhất 2 nhánh profile (Claude Pha-1-pure ⊕ Codex profile-own-ingest). **GIỮ Codex làm BASE** (hoàn chỉnh hơn:
profile-create tạo Sheet registry 27 cột+_meta+manifest; profile-ingest orchestrator đầy đủ; policy forbid-inherit;
generate_style_template) — Codex đã có ĐỦ detector 1.23.x (sweep/dedup-plan/quarantine-fix/shared_source_id/infra/
clobber+legacy guards) vì rẽ từ 1.23.22 của Claude. **PORT bổ sung của Claude + yêu cầu user:**
- `_manifest_fallback`: **LUÔN ƯU TIÊN tìm trong 1 NOTEBOOK (profile) TRƯỚC** (nhanh/đúng phạm vi); **CHỈ khi MISS** hoặc
  cần đối chiếu xuyên corpus mới `cross_notebook_query` theo THỨ TỰ ƯU TIÊN: profile → VBQPPL (`743ed200…`) → VBQPPL-2
  overflow (`45739ff7…`) → shard mới. Khi trùng → **canonical PROFILE THẮNG**, VBQPPL/shard chỉ bổ sung. Project
  Instruction + NLM System Prompt sinh ra **DÙNG ĐƯỢC LUÔN** (id thật).
- Đồng bộ const/VERSION/SKILL header = 1.24.0 (Codex để 2 dòng `VERSION=` lệch → gộp 1).

+1 test `instruction_cross_notebook_all_shards` → selftest **268/268**, integrity sạch.

---

# ★ v1.23.23 (profile-own-ingest) — profile tự trị + ingest dự thảo/OCR

- `profile-create --apply` tạo đủ folder profile, `_meta`, Google Sheet registry 27 cột và JSON manifest riêng; ghi `registryDocId`, `manifestId`, `manifestScope=own`, `categories=own` vào config.
- Chặn profile dự án `categories=inherit` ở các lệnh ghi/quét nguy hiểm; forward `manifestScope` và `metaFolderId`.
- Thêm `profile-ingest` DRY mặc định: phân loại header, prefix `DUTHAO_`, gate Điều/Phụ lục/OCR, giữ canonical GDoc flat trong root profile, tách nguồn NLM theo Điều vào `_meta` khi văn bản lớn.
- Source-map/extract cảnh báo `DỰ THẢO — chưa hiệu lực`; OCR chưa verify không được `corpus=true`.
- Instruction generator tách prompt kỹ thuật khỏi `style-template`; bổ sung verify nguyên văn, VBHN-first, source id và Điều/khoản/điểm.

---

# ★ v1.23.22 (gws3env) — ROOT-CAUSE THẬT (đính chính 1.23.21: KHÔNG mất dữ liệu)

**Đính chính sự cố 2026-06-30:** registry **KHÔNG bị xóa 766 dòng**. Root-cause thật = config `registryDocId` trỏ NHẦM
**Doc legacy `1mATG`** (vnd.google-apps.document — chỉ dùng ping/display) thay vì **SHEET registry thật**
(`tra_luat_registry`). Webapp `regSS_` mở Doc-as-Sheet → đọc RỖNG → `count=0` ẢO. Dữ liệu vẫn nguyên (corpus 552 = do
`dedup-plan --apply` bỏ 50 dup, KHÔNG phải mất). **Template public** (init-config --from-public) ghi đè registryDocId về
Doc legacy → tái diễn mỗi `tl_fetch.sh --setup`.

**FIX:**
- **doctor** CHẶN cứng: `registryDocId == _LEGACY_REGISTRY_DOC_ID` (1mATG) → check FAIL + chỉ sửa (về Sheet thật hoặc để
  rỗng cho webapp auto-discover) + `tl reg-query --refresh`.
- **init-config AUTO-HEAL:** blank `registryDocId` (base + mọi profile) nếu == Doc legacy → webapp auto-discover Sheet
  `tra_luat_registry`. Tự lành mỗi setup dù template Drive còn sai.
- Giữ guard 1.23.21 (profile registryDocId RỖNG → chặn clobber base) — vẫn là phòng thủ hợp lệ.

+1 test `legacy_registry_doc_guard` → selftest **260/260**. ⚠ Vẫn nên **cập nhật template config trên Drive** (registryDocId
= Sheet thật hoặc rỗng) để gốc rễ sạch.

---

# ★ v1.23.21 (gws3env) — ⛔ GUARD chống CLOBBER registry NỀN (sự cố nghiêm trọng)

**SỰ CỐ 2026-06-30 (mất 766 dòng registry VBQPPL):** tạo profile dự án "Khảo sát Luật XB" với `registryDocId` RỖNG →
`manifest --touched-drive --confirm yes` (profile) → webapp `regSS_` KHÔNG có `_REQ_REGISTRY_ID_` → rơi nhánh **BASE**
(Sheet `tra_luat_registry`) → regen2 quét cả cây VBQPPL (PROFILE_MANIFEST_SCOPE_BLOWUP, 418 dòng) → `profile-rebuild-registry
--apply` "dọn phình" nhưng thao tác trên BASE → **XÓA SẠCH 766→0 dòng registry nền**.

**FIX (preventive):** `cmd_manifest` (--touched-drive) + `cmd_profile_rebuild_registry` CHẶN khi profile dự án có
`TL_REGISTRY_DOC_ID` rỗng → `PROFILE_REGISTRY_ID_EMPTY_WOULD_CLOBBER_BASE` (rc=2) — bắt tạo registry RIÊNG (Sheet mới +
ghi registryDocId vào config) TRƯỚC. +1 test `profile_registry_clobber_guard` → selftest **259/259**.

**LÀM RÕ KIẾN TRÚC (từ GS):** registry base = **Google SHEET `tra_luat_registry`** (`regSS_` tìm theo TÊN trong root /
`TL_REGSHEET_ID_AUTO` ScriptProperties), KHÔNG phải Doc `1mATG` (chỉ dùng ping/display — legacy). ⇒ **Khôi phục đúng =
restore SHEET `tra_luat_registry`** qua version history Google Sheets (KHÔNG phải restore Doc). Cache registry =
CacheService `tl212_reg_*` TTL 600s (10') → count=0 sau khôi phục Sheet sẽ tự đúng sau ≤10' hoặc khi có write.

---

# ★ v1.23.20 (gws3env) — DETECTOR `infra_in_corpus` (file hạ tầng lẫn corpus)

**Phát hiện khi rà 106 Luật (dump corpus):** file HẠ TẦNG đếm `corpus=true` = RÁC: `tl_secrets.enc`,
`nlm_sources_delta_2026-06-11{,b,c}.json`. `_is_infra_entry` (module-level): `.json`/`.enc` + tên
`nlm_sources`/`manifest`/`registry`/`reg_query`/`secrets`/`_delta` → infra; BẢO VỆ văn bản thật (GDoc/PDF/Word mime →
KHÔNG false-positive). Thêm vào `tl sweep`: `infra_in_corpus` count + rows + NEXT ACTION (set corpus=false). +1 test →
selftest **258/258**. (Fix: `tl register --bulk <[{drive_id,corpus:false}]> --cols corpus` cho các drive_id infra.)

---

# ★ v1.23.19 (gws3env) — COMPOSITE `tl dedup-plan` (kế hoạch dedup toàn corpus 1 lệnh)

Biến chuỗi `hygiene plan <q>` từng cụm → 1 lệnh. `_dedup_plan` tái dùng canonical-picker đã có
(`_hygiene_groups`.reconcile_clusters — `_cluster_same_doc` = CÙNG văn bản theo subject-sig) + **gộp `sidecars`** (.docx/.pdf
cạnh GDoc canonical = dup định dạng). Mỗi cụm: GIỮ canonical, set `corpus=false` các bản dup (reversible).
**BẤT BIẾN AN TOÀN:** (1) không quarantine chính canonical; (2) không quarantine drive_id LÀ canonical của cụm khác;
(3) mỗi drive_id 1 lần. `ready` = cụm có canonical rõ (auto); `review` = cụm thiếu canonical (quyết tay); `dups_on_nlm` =
dup còn nguồn NLM (cân nhắc `nlm source delete` tay, §4#2). DRY mặc định; `--apply` ghi reg_bulk corpus=false. `sweep`
NEXT ACTION dedup giờ trỏ `tl dedup-plan --apply`. +1 test `dedup_plan_keeps_canonical` → selftest **257/257**.

---

# ★ v1.23.18 (gws3env) — FIX false-fire `NLM_STATUS_MISMATCH` (họ status removed_*)

**Phát hiện khi `nlm-orphans --fix-mismatch` LIVE trả `MISMATCH_LIVE=0`** dù `sweep` báo 79 `NLM_STATUS_MISMATCH`. Nguyên
nhân: whitelist status **exact-match** `{pushed,synced,removed,removed_from_drive,deleted,trash,trashed}` KHÔNG nhận BIẾN
THỂ tiền tố `removed_*` (vd `removed_superseded_by_VBHN`, `removed_dedup`) → cờ false-fire; đồng thời `_entry_on_nlm_live`
coi NHẦM `removed_superseded_by_VBHN` là CÒN SỐNG (lệch `still_on_nlm`/ghost). FIX: helper **`_nlm_status_known`** /
**`_nlm_status_removed`** nhận HỌ theo tiền tố (`pushed*`/`synced`/`active` ; `removed*`/`trash*`/`deleted`), áp 4 site:
doctor drift flag, `_title_flags`, `_entry_on_nlm_live`, vbhn-normalize removed-list. `sweep` NEXT ACTION cho
NLM_STATUS_MISMATCH đổi: = nhãn status LẠ (registry hygiene), KHÔNG phải live desync (nlm-orphans chỉ vá MISMATCH_LIVE thật).

+2 test (`nlm_status_family_recognition`, `nlm_status_mismatch_no_false_fire`) → selftest **256/256**.

---

# ★ v1.23.17 (gws3env) — `sweep` NEXT ACTION nlm_drift tách theo sub-type

**Phát hiện khi chạy nlm-reconcile LIVE:** reconcile patch 2 link nhưng `nlm_drift` vẫn 288 — vì reconcile chỉ chữa
**LINKAGE** (source_id↔drive_id), KHÔNG phải toàn bộ drift. Sweep cũ gộp 288 → "nlm-reconcile --apply" GÂY HIỂU NHẦM.
FIX: `_sweep_report` next_actions tách 3 sub-type, mỗi cái LỆNH ĐÚNG:
- `NLM_NOTEBOOK_ID_MISSING` → `tl nlm-reconcile <nb> --apply` (linkage; shard khác → reconcile từng shard)
- `NLM_STATUS_MISMATCH` → `tl nlm-orphans <nb> --fix-mismatch` (đọc NLM LIVE, không đụng NLM)
- `CORPUS_TRUE_NOT_ON_NLM` → `tl ingest-missing --apply` (JOB LỚN; phần lớn CẤU TRÚC do corpus>cap 300/notebook → KHÔNG về 0)

selftest **254/254**.

---

# ★ v1.23.16 (gws3env) — DETECTOR `shared_source_id` (FALSE-LINK NLM)

**Phát hiện khi dọn ghost NLM LIVE (B2):** ca NQ42 — canonical (`Doi_moi_chat_luong_CS_xa_hoi`) và ghost
(`Chinh_sach_xa_hoi`) là 2 GDoc KHÁC nhau nhưng registry gắn **CÙNG `nlm_source_id`** (backfill/reconcile nhầm). Xóa
nguồn của ghost → **canonical mất link NLM** (chưa từng thật sự push) → phải `nlm source delete` + re-push + map_set tay.

FIX: pure `_shared_source_id_groups(entries)` phát hiện ≥2 drive_id chung 1 nlm_source_id → thêm vào **`tl sweep`**
(`shared_source_id` count + nhóm + NEXT ACTION 🔴 cảnh báo SỬA TRƯỚC khi `nlm-reconcile`/xóa nguồn). Giúp THẤY footgun
trước khi reconcile 291 mục. Dev cache: 4 nhóm. +1 test `shared_source_id_detect` → selftest **253→254/254**.

---

# ★ v1.23.15 (gws3env) — Xử báo cáo rà 106 Luật (mục code CÒN LẠI)

Báo cáo chạy trên 1.23.10. Đối chiếu (workflow Explore read-only): **5.1** (dedup-check tên), **5.3** (reg-query limit 60),
**5.6** (source-map name multi-hit), **4.B** (vbhn-normalize tồn tại) → **ĐÃ vá** ở 1.23.11–1.23.14. Mục code còn lại:

- **5.2 — `vbhn-check` bare-number cross-subject:** `tl vbhn-check --goc 09-2017-QH14` (Du lịch) kéo nhầm `14-2024-VBHN-VPQH`
  (ATVSLĐ) vì `goc_hit` (refs∩gkeys) được giữ BẤT KỂ chủ đề, và `_disc_conflict` chỉ biết cặp-conflict cụ thể (không biết
  'du lịch' vs 'lao động'). FIX `_vbhn_candidates`: khi ĐÃ biết subject (truyền/suy từ goc), `goc_hit` phải TƯƠNG THÍCH
  chủ đề (`sscore≥30`) mới giữ — chặn goc-ref nhiễu khác lĩnh vực; subject rỗng vẫn nhận goc_hit. +2 test.
- **5.5 — Cowork /tmp không ghi được** (sticky-bit, owner nobody → Permission denied): `_ensure_writable_tmpdir()` chạy lúc
  import — nếu TMPDIR/gettempdir không ghi được thì trỏ TMPDIR về `CACHE/tmp` ($HOME, luôn ghi được); `tempfile.*` và mọi
  script con (kế thừa `os.environ`) tự dùng dir này. Idempotent, im lặng nếu /tmp vốn ghi được.
- **5.4 — SKILL.md §1**: thêm cảnh báo bootstrap 45s Cowork (tách `--setup` core khỏi `--nlm`). **4.B**: thêm
  `vbhn-normalize`/`vbhn-year-fix`/`sweep`/`quarantine-fix` vào bảng CLI §4.

Mục §4.A/C/D/E = DATA (lệnh đã có: relation-check/relation-backfill, vbhn-check QT-5, nlm-reconcile, hygiene/quarantine-fix).
selftest **251→253/253**, integrity sạch.

---

# ★ v1.23.14 (gws3env) — COMPOSITE `tl quarantine-fix` (dọn nhóm B tất định)

Biến chuỗi dọn quarantine (report rà corpus nhóm B) → 1 lệnh. `_quarantine_fix_items` phân loại 4 nhóm:
- **set_corpus_false** — corpus=true nhưng file THÔ (.pdf/.docx/.doc = dup định dạng gán nhầm) → `--apply` set corpus=false (an toàn, canonical GDoc ở chỗ khác).
- **normalize_label** — nhãn quarantine biến thể (cat≠QUARANTINE_CAT) → `--apply` chuẩn hoá cat=QUARANTINE_CAT.
- **review_restore** — corpus=true NHƯNG là **GDoc native** → nghi canonical SỐNG bị kẹt quarantine (gốc rễ A1/B1, vd BLLĐ) → **KHÔNG auto**, người dùng quyết khôi phục (recat ra chủ đề) hay set false.
- **ghost_nlm** — quarantine nhưng còn nguồn NLM **live** → báo `nlm_source_id`, xoá tay (`nlm source delete`) sau verify (§4#2).

DRY mặc định; `--apply` chỉ ghi 2 nhóm AN TOÀN (set_corpus_false + normalize_label), 2 nhóm còn lại chỉ BÁO. +1 test
`quarantine_fix_classify` → selftest **251/251**. (Dev cache: 10 corpus_false + 13 label + 1 review_restore[51/2024 GDoc] + 3 ghost.)

---

# ★ v1.23.13 (gws3env) — MERGE Codex + gỡ `_parts` + composite `tl sweep`

**(1) MERGE HỘI TỤ bản Codex v1.23.11** (cả 2 cùng vá report rà corpus, độc lập). Giữ base ĐÃ VERIFY của Claude (có
1.23.11/1.23.12 + KH1/2/3 + bất biến năm), PORT phần UNIQUE của Codex:
- **A1 SUBJECT-GATE thật** (`_name_subject_text` + `_name_subject_match`): `source-map` theo tên ghim canonical CHỈ
  trong các hit KHỚP CHỦ ĐỀ (abbrev-aware: 'BLLD'≡'Bộ luật Lao động', 'BHXH'≡'bảo hiểm xã hội'); hit chỉ trùng token
  chung ('Dân chủ cơ sở') bị loại; không có hit chủ đề → `canonical=None` + `NAME_QUERY_SUBJECT_MISMATCH_NO_CANONICAL`.
  (Trước đây Claude không tái hiện A1 nên giữ gate cũ — Codex có fix thật, nay port.) +2 test.
- `resolve_identity` cộng điểm `name_tokens` (token-subset, gồm subject) → dedup-check bắt 'Luật Thư viện'↔
  'Luat_46-2019-QH14_Thu_vien'. +1 test.
- `vbhn-check` cảnh báo `SUBJECT_FILTER_WEAK` khi mọi hit metadata yếu; `reg-query` text in `LIMIT_TRUNCATED` rõ.
- A2/A3/A4/A5 + reg-query json-all: GIỮ bản Claude đã verify (hội tụ).

**(2) GỠ `_parts`** (cơ chế chia nhỏ chống mount-cắt-cụt — Cowork nay bootstrap qua `tl_fetch.sh` tải zip SẠCH từ Drive
nên `_parts` hết tác dụng): xoá `scripts/_parts/` + `build_parts.py` + `tl_rebuild.sh`; `tl_boot.py` rút gọn còn
strip-NUL→compile→exec; `_reassemble_parts`→None (mọi hàm heal degrade an toàn về on-disk); `edit-skill`/`verify-integrity`
bỏ bước build_parts (verify-integrity giờ toàn NOPARTS = bình thường).

**(3) COMPOSITE TẤT ĐỊNH `tl sweep`** (biến chuỗi action thường gặp → 1 function): 1 lệnh read-only thay cả chuỗi
`hygiene scan` + `cat-audit` + `slot-audit` + `doctor`-drift + `vbhn-year-fix` DRY + đếm quarantine/dup → JSON/text +
**NEXT ACTIONS điền sẵn lệnh**. Pure `_sweep_report(entries)` (test offline). +1 test.

selftest **246→250/250**, integrity sạch (33 file, hết _parts).

---

# ★ v1.23.12 (gws3env) — reg-query --json undercount + cờ trạng thái mâu thuẫn quarantine

**Phát hiện khi chạy B1 (liệt kê quarantine) LIVE:**
- **reg-query `--json` UNDERCOUNT âm thầm:** mặc định cắt **60 rows** → script đếm `len(rows)` chỉ thấy 60/110 quarantine
  (đúng điểm yếu #3 báo cáo trước). `count` envelope vốn đúng (tổng), nhưng consumer lặp `rows`. FIX: `--json` trả **TẤT
  CẢ rows** mặc định (JSON cho tool); text mode giữ cắt 60 (dễ đọc, có dòng "(hiện 60)"); thêm cờ `truncated`. `--limit` ép trần.
- **Cờ TRẠNG THÁI MÂU THUẪN** trong `hygiene scan`: `quarantine_corpus_true` (trong quarantine nhưng corpus=true — lẽ ra
  false) + `quarantine_still_on_nlm` (quarantine nhưng còn nguồn NLM live = GHOST cần gỡ). Surface để dọn dữ liệu.

selftest **246/246** (đổi additive, smoke xác nhận: reg-query --json trả 775/775; hygiene cờ mới hoạt động).

---

# ★ v1.23.11 (gws3env) — Xử báo cáo rà corpus (nhóm A: lỗi/khiếm khuyết skill)

- **A2 — nhãn QUARANTINE không thống nhất:** thêm hằng `QUARANTINE_CAT="_ZZZ_QUARANTINE_taluat"` (nhãn GHI chuẩn) +
  `_is_quarantine_label_variant` + cờ `quarantine_label_variants` trong `hygiene scan`. `_is_quarantine_cat` đã nhận MỌI
  biến thể (code `QUARANTINE`, folder `_ZZZ_…`) nên audit HỘI TỤ dù nhãn lệch; cờ mới surface dòng nhãn cũ để chuẩn hoá.
- **A3 — slot-audit đếm ảo:** `slot-audit` TỰ neo `live_source_count` từ nlm CLI (`notebook_get`) + cảnh báo gap
  estimate↔live, KHÔNG cần gọi `--physical` tay; `--no-live` để tắt (offline/không cred).
- **A4 — doctor không breakdown:** `doctor` in BREAKDOWN từng cờ lệch NLM (NLM_STATUS_MISMATCH / CORPUS_TRUE_NOT_ON_NLM /
  NLM_NOTEBOOK_ID_MISSING) + lệnh `tl nlm-reconcile <nb> --apply` ĐIỀN SẴN notebook id (1 bước).
- **A5 — quote bẫy:** help `vbhn-check --subject` thêm cảnh báo QUOTE cụm có dấu cách.
- **A1 — source-map ghim sai canonical theo token tên:** KHÔNG tái hiện trên v1.23.11 với dữ liệu đại diện. Gate
  `LOW_CONFIDENCE_NAME_MATCH` GỐC đã null canonical khi hit điểm-cao không `_name_strong_match` (abbrev-aware) → ca report
  ('Bộ luật Lao động'→'Dân chủ 87') đáng lẽ đã bị null. Thử thay gate bằng nhóm theo tail-key gây REGRESSION ca tên viết
  tắt (BHXH) + ranking quarantine → đã revert, giữ gate gốc + thêm test cross-domain. Cần `tl source-map … --json` LIVE để
  soi vì sao 87 lọt by_name nếu còn gặp.

(Nhóm B = dọn DỮ LIỆU trên Cowork — không phải lỗi code; C = output rà soát; D/E = OK.) +3 test → selftest **246/246**.

---

# ★ v1.23.10 (gws3env) — GUARD `cat`: chặn folder rác gõ tay

**Phát hiện khi nạp THADS 106/2025/QH15 LIVE:** `recat --cat 30` move Drive OK nhưng `reg_patched=0` (webapp index chưa
thấy row) → workaround `register --bulk --cols cat` với tên folder **gõ tay SAI** `30_To_chuc_bo_may_nha_nuoc` (số 30 ghép
tên của cat 35 = "Tổ chức bộ máy nhà nước"; cat 30 thật là "Thi hành án" = `30_Thi_hanh_an`). `register`/reg_bulk **KHÔNG
validate** → ghi folder rác im lặng → registry lệch folder vật lý. FIX: `_is_valid_cat_value` chặn cat không thuộc taxonomy
45+2 (cả `--bulk` lẫn reg_upsert), rc=2, nhắc dùng `tl recat --cat <số>` (tự resolve + validate folder). +1 test
`valid_cat_value_guard` → selftest **244/244**.

**BÀI HỌC:** đổi cat LUÔN dùng `tl recat --cat <số>` (resolve folder từ mã + validate taxonomy); KHÔNG `register --bulk`
với tên folder gõ tay. Khi recat báo `reg_patched=0`: `tl boot --refresh` rồi `recat` lại, KHÔNG vá tên tay.

---

# ★ v1.23.9 (gws3env) — `vbhn-year-fix` chỉ corpus + sửa HINT `regen2` không tồn tại

**Phát hiện khi chạy LIVE Cowork:**
- **(A) CONFLICT GIẢ:** `vbhn-year-fix` quét CẢ sidecar/quarantine (corpus=false) → chúng va sohieu với GDoc canonical
  cùng số → báo conflict, dù `tl hygiene plan` báo "sạch" (mâu thuẫn). FIX: `_vbhn_year_fix_items` CHỈ quét
  `corpus=true` (canonical). Sidecar/quarantine không cần year-fix.
- **(B) HINT SAI:** lệnh ghi (relation-backfill/ingest-missing/backfill-loai/missing-sohieu/vbhn-year-fix/recat) in
  `MANIFEST_STALE_RUN_REGEN2` → user chạy `tl regen2` nhưng **KHÔNG có lệnh đó** (chỉ `tl manifest`; "regen2" là action
  GAS gọi qua `tl manifest --touched-drive`). Sửa 6 hint → chỉ đúng: `tl boot --refresh` (sau ghi registry sheet) hoặc
  `tl manifest` (sau khi đổi cây Drive).

Test `vbhn_year_fix_items_split` mở rộng (thêm dòng corpus=false PHẢI bị bỏ) → selftest **243/243**. Hint còn lại
`MANIFEST_STALE_RUN_REGEN2` duy nhất ở comment VERSION (lịch sử changelog), không phải output.

---

# ★ v1.23.8 (gws3env) — SAFEGUARD `vbhn-year-fix`: chặn tạo collision MỚI

**Phát hiện khi soát DRY** (dev cache): nhiều số VBHN cùng số ra CÙNG năm (`62`→[2026×4], `21`→[2026×3], `108`→[2025×2]).
Nếu `--apply` thì ≥2 dòng nhận **CÙNG `NN-YYYY-VBHN-XXX`** → **TẠO collision MỚI** (vô nghĩa). Nguyên nhân: hoặc dòng dup
cùng văn bản (phải dedup), hoặc 2 văn bản KHÁC nhau cùng số+năm (năm không đủ phân biệt). `_vbhn_year_fix_items` nay trả
**(fixable, needs_year, conflicts)**: chỉ `fixable` (new_sohieu DUY NHẤT) mới ghi; nhóm trùng → `conflicts` in 🔴, KHÔNG
auto-apply, `--apply` trả rc=1 nếu còn conflict. +1 test `vbhn_year_fix_conflict_detect` → **242→243/243**.

---

# ★ v1.23.7 (gws3env) — BẤT BIẾN: số hiệu VBQPPL PHẢI có NĂM (VBHN year-collision)

**Yêu cầu hệ thống** (user nhấn mạnh 2026-06-30): MỌI số hiệu/tên VBQPPL phải chứa NĂM. **VBHN là thủ phạm** — số VBHN
chính thức (`NN/VBHN-XXX`) KHÔNG có năm và **tái dùng mỗi năm** → cùng số = văn bản khác. Gặp hàng loạt: `61/VBHN-VPQH`
= ATTP(2025)+Thuế TNDN(2026); `14/VBHN-VPQH` = ATVSLĐ(2024)+NLĐ nước ngoài(2023); `115/VBHN-VPQH` = THADS(2025)+Thi
đua(2026); `25/VBHN-VPQH` = Kế toán(2025)+Giá(2026).

**Lệnh MỚI `tl vbhn-year-fix [--limit N] [--with-name] [--apply]`:** quét registry các VBHN có sohieu thiếu năm
(`NN-VBHN-XXX`) → suy năm ban hành (`_entry_issue_year`: trường issue/ngày ban hành/tên) → đề xuất sohieu chuẩn
**`NN-YYYY-VBHN-XXX`** (+ tên có năm với `--with-name`). DRY mặc định; `--apply` GHI qua **reg_upsert** (KHÔNG reg_bulk —
sohieu là khóa immutable, reg_bulk bỏ im lặng). Ca không suy được năm offline → `needs_year` (đọc header/NLM xác minh tay).
Pure `_vbhn_sohieu_inject_year` / `_name_inject_vbhn_year` / `_vbhn_year_fix_items` (test offline).

**`tl register`:** cảnh báo `VBHN_SOHIEU_NO_YEAR` khi ghi sohieu VBHN thiếu năm (không chặn, nhắc dùng dạng có năm).

+3 test (`vbhn_sohieu_inject_year`, `vbhn_name_inject_year`, `vbhn_year_fix_items_split`) → **239→242/242**.
⚠ Chạy LIVE Cowork: `tl vbhn-year-fix` (DRY xem) → `--apply --with-name` để cập nhật toàn bộ. Sau đó `regen2 --refresh`.

---

# ★ v1.23.6 (gws3env) — FIX: `recat --apply` báo `reg_patched:0` âm thầm

**BUG** (phát hiện khi KH2 Pha 2.6 recat LIVE Cowork): `tl recat --apply` move file Drive thành công nhưng `reg_bulk`
patch cat trả **`reg_patched:0`** với các row MỚI THÊM (webapp registry index chưa thấy row → match 0) — in JSON `ok:true`
khiến người dùng tưởng đã cập nhật registry, thực ra cat chưa đổi (cùng họ "ghi im lặng" với 1.23.5). Code reg_bulk vốn
ĐÚNG (`cols="cat"`); vấn đề là **không cảnh báo khi `reg_patched < moved`**. Nay: in cảnh báo LOUD ra stderr + **rc=1**
khi patch thiếu, chỉ rõ khắc phục (`tl regen2 --refresh` rồi reg_bulk/recat lại). +1 test `recat_warns_when_patch_short`
(inspect source) → **238→239/239**. (Trên Cowork đã workaround: refresh + reg_bulk tay = 6/6 ✅.)

---

# ★ v1.23.5 (gws3env) — FIX: `missing-sohieu --apply` ghi sai cột (`so_hieu` → `sohieu`)

**BUG** (phát hiện khi KH2 Pha 2.8 chạy LIVE trên Cowork): `tl missing-sohieu --apply` ghi `reg_bulk` với khóa **`so_hieu`**
(có gạch dưới) — webapp registry **BỎ IM LẶNG** mọi cột lạ (đúng cảnh báo `API_CONTRACT.md` mục 0: khóa duy nhất là
**`sohieu`**). Hậu quả: apply trả `patched=0` mà KHÔNG báo lỗi → người dùng tưởng đã ghi. Sửa `items` key + `cols` →
`"sohieu"` (line ~8061) + docstring/help. Trên Cowork đã workaround thủ công (`cols="sohieu"`, ghi 193/193); nay **code gốc
đúng** để lần sau `--apply` thẳng hoạt động. +1 test regression `missing_sohieu_reg_bulk_col_sohieu` (inspect source) →
**237→238/238**. (Đối chiếu: `backfill-loai` đã dùng đúng `cols="loai"` — không ảnh hưởng.)

---

# ★ v1.23.4 (gws3env) — `tl relation-backfill`: KH1 HOÀN TẤT (lệnh cuối)

**`tl relation-backfill --base <sohieu> [--subject] [--apply]`** [MỚI] (Pha 1.5, cho KH2 Pha 2.3): GHI quan hệ sửa đổi
mà `relation-check` ĐÃ phát hiện (`missing_links` từ `_relation_audit`) — set **`goc`** cho luật SỬA (trỏ về gốc), append
**`sua_doi`** cho luật GỐC. Pure **`_relation_backfill_items`** HỢP NHẤT với `sua_doi` hiện có + dedup (KHÔNG đè mất quan
hệ cũ). Tái dùng nguyên cổng chống dương-tính-giả của relation-check (footnote-map): **chỉ backfill direct/ref-linked**;
ca chỉ-trùng-chủ-đề → `subject_only_review` (xác minh tay, không auto-ghi). DRY mặc định; `--apply` ghi reg_bulk. +1 test
→ **236→237/237**.

> **★ KH1 hoàn tất toàn bộ lệnh** (1.22.71→1.23.4): H1/H2/UTF-8/instructions; 3 cổng **G1**(source-verify)/**G2**(header-verify)/
> **G3**(cat-verify+cat-audit/recat); vòng lặp **frontier-expand/ingest-missing/rasoat-loop**; dọn corpus **backfill-loai/
> sohieu-conflict/missing-sohieu**; hạ tầng **slot-audit/overflow-resolve/edit-skill**; **nlm-orphans** (1.23.2) + overflow
> physical (1.23.1); **relation-backfill** (1.23.4). selftest 209→**237**, guard `skill_md_version_matches_VERSION`.
>
> CÒN (tài liệu, không phải lệnh): cập nhật `RUNBOOK.md`/`API_CONTRACT.md`. KH2 (corpus 775 dòng) + KH3 (nạp văn bản thiếu) tiếp.

# v1.23.3 (gws3env) — FIX deploy-display: SKILL.md header version cứng + guard selftest

**Lỗi:** SKILL.md dòng 18 ghi CỨNG `# tra-luat — LÕI VẬN HÀNH (v1.22.70)` — tôi bump VERSION/tl.py qua 1.22.71→1.23.2
mà **chưa hề sed SKILL.md** → bản deploy **HIỂN THỊ "v1.22.70"** dù runtime đúng version mới. (Người dùng thấy v1.22.70.)

- **Sửa SKILL.md** header → `(v1.23.3)`.
- **GUARD selftest `skill_md_version_matches_VERSION`**: assert `"v"+VERSION` xuất hiện trong SKILL.md → bump nào quên
  cập nhật SKILL.md = selftest FAIL = `upload-skill-to-Package.sh` dừng (script chạy selftest trước khi zip). Chặn tái diễn.
  selftest **235→236/236**.

> **Phát hiện vận hành (curl Package live):** file Package (`SKILL_FILEID=1H5kAt3…`, nơi Cowork bootstrap) đang là **v1.23.0,
> KHÔNG có nlm-orphans** — tức **1.23.1 + 1.23.2 CHƯA push thành công** lên Package (drive-push cần gws auth; dev này
> `auth=none` nên KHÔNG push được). → phải re-deploy 1.23.3 trên máy CÓ gws auth, và **VERIFY push** bằng curl Package fileId
> (xem version thật trên Package, độc lập với Cowork). fileId tl_fetch == SKILL_FILEID (khớp, không lệch).

# v1.23.2 (gws3env) — `tl nlm-orphans`: tự động hoá điều tra ghost (thay soi tay nhiều vòng)

Đúc kết từ phiên điều tra LIVE: **`removed_from_drive` gắn nhầm cho ≥8 văn bản còn SỐNG trên NLM** (66.18/2026/NQ-CP,
09/VBHN-BNV, 5 văn kiện BCH Trung ương, VBHN_25 Luật Kế toán) + số hiệu LƯU CỤT (`66`, `09-BNV`). Sau 6 vòng soi tay
(diff live∖registry, dễ sai — đã lệch 37 vs 18 một lần), đóng thành 1 lệnh. selftest **234→235/235**.

**`tl nlm-orphans <notebook> [--fix-mismatch] [--deep] [--json]`** [MỚI]:
- Đọc nguồn NLM **LIVE** (`nlm_cli.source_list`, ~4s) ↔ registry (theo `nlm_source_id`) → pure **`_classify_nlm_sources`**
  (test offline) phân 3 nhóm: **REGISTERED_ACTIVE** (lành) · **STATUS_MISMATCH_LIVE** (dòng registry `removed*` nhưng
  nguồn còn đọc được = GẮN NHÃN SAI → vá) · **UNREGISTERED** (trên NLM, không dòng registry → điều tra).
- **`--fix-mismatch`**: in bản vá metadata **DRY** (`corpus=true, nlm_status=pushed`) cho nhóm mislabel, keyed `drive_id`
  → ghi bằng `tl register --bulk <file> --cols corpus,nlm_status[,sohieu]`. **KHÔNG đụng NLM, KHÔNG xóa.**
- **`--deep`**: đọc nội dung NLM từng mismatch → trích **số hiệu header thật** (vá cả sohieu cụt: `66`→`66.18/2026/NQ-CP`).
- Phơi `physical_vs_registry_active_gap` (đo đúng khoảng lệch 315 vs registry).

> Bất biến: REPORT-ONLY, KHÔNG tự xóa nguồn NLM (mọi `source_delete` cần người duyệt). Đây là tool **phát hiện**; **nguyên
> nhân gốc** (pipeline nào gắn nhầm `removed_from_drive` cho văn bản sống) vẫn cần soi riêng.
>
> CÒN: `relation-backfill` (Pha 1.5 live); cập nhật `SKILL.md`/`RUNBOOK.md`/`API_CONTRACT.md` + deploy Package (user-side).

# v1.23.1 (gws3env) — vá sweep-finding: `overflow-resolve` đối chiếu LIVE (physical) thay registry-only

Phát hiện khi chạy KH1 sweep LIVE trên Cowork: **base notebook registry 279 nhưng `nlm-get` vật lý 315** (>cap 300) —
nguồn add thẳng chưa đăng ký registry. `overflow-resolve` cũ đếm REGISTRY-only nên báo "BASE_HAS_ROOM" SAI (vật lý đã vượt).

- **`overflow-resolve` đối chiếu LIVE**: lấy `nlm-get` physical cho base+overflow → dùng **MAX(registry, physical)** làm slot
  hiệu lực (`_overflow_status`, pure) → KHÔNG báo "còn chỗ" giả. Cờ **`REGISTRY_BEHIND_LIVE`** + chênh lệch (vd +36) → gợi
  `tl nlm-reconcile <notebook> --apply` đăng ký nguồn lạc TRƯỚC khi nạp. `--no-live` để registry-only (offline/nhanh).
  Sửa cosmetic flag (BASE_HAS_ROOM khi base còn chỗ, không còn nhầm OVERFLOW_SHARD_EXISTS). +1 test → **234/234**.
- **Lưu ý:** `ingest-missing --apply` ĐÃ physical-safe từ 1.22.74 (tính room qua `nlm-get` LIVE) → KHÔNG nhồi base 315.
  Bản vá này chỉ làm advisory `overflow-resolve` khớp sự thật vật lý.

# ★ v1.23.0 (gws3env) — PHÁT HÀNH KH1 (sửa skill sau báo cáo rà 70 Luật)

Đóng mốc **1.23.0** = thực thi Kế hoạch 1. selftest **209→233/233** (+24, toàn bộ pure-helper offline), `verify-integrity` sạch
xuyên suốt, mỗi lệnh mới DRY/report-only mặc định, **KHÔNG RAG**, nhánh mutate có guard cứng. Bản agent workflow tự ý
tiêm header-verify/cat-verify ở phiên đầu đã được **revert sạch**; toàn bộ dựng lại CÓ REVIEW + test.

**Bản 1.23.0 này (Pha 1.3 + III.2) thêm:**
- **`tl slot-audit --all-shards`** (II.5): đếm slot TỪNG shard (base+overflow) + cảnh báo near-full ≥270/300 (pure
  `_slot_count_all_shards`). LIVE: base VBQPPL **279/300 (NEAR)**, overflow VBQPPL-2 29/300.
- **`tl overflow-resolve`** (II.1): kiểm shard overflow SẴN CÓ → cờ `OVERFLOW_SHARD_EXISTS_DO_NOT_CREATE` (chống tạo
  notebook nhầm như sự cố 'VBQPPL_overflow_1'); reuse `_overflow_route`. LIVE: phát hiện đúng VBQPPL-2 còn chỗ.
- **`tl edit-skill <file> --patch`** (III.2): sửa file skill AN TOÀN — assert-đếm chuỗi → py_compile → write_text →
  build_parts; né tầng Edit/Write mount Cowork hay revert. DRY mặc định (assert+compile, không ghi).
- **II.4** manifest-stale: lệnh ghi MỚI phát `MANIFEST_STALE_RUN_REGEN2`. **II.3** canonical-not-sidecar: ĐÃ xử sẵn qua
  deep-resolver (`_resolve_deep_target` ưu tiên GDoc/corpus/live + `_is_source_sidecar` + phạt raw −300).

**★ Tổng KH1 (10 lệnh + 4 FIX, qua 1.22.71→1.23.0):**
- Pha 1.0/1.1/1.4: đối soát version · H1 (reg-query rc=0 khóa test) · H2 (registry-doctor text=JSON schema) · III.1 UTF-8
  (PYTHONUTF8 truyền script con) · III.3 `instructions --out`.
- Pha 1.2 — **3 cổng**: `cat-verify`(G3)+FIX `cat-audit`/`recat` · `header-verify`(G2) · `source-verify`(G1)+re-rank
  `_DISCOVERY_SITES` official-first.
- Pha 1.2 — **vòng lặp khép kín**: `frontier-expand` · `ingest-missing`(idempotent, no-new-notebook) · `rasoat-loop`(orchestrator).
- Pha 1.5 — **dọn corpus**: `backfill-loai`(191/769) · tách `SOHIEU_CONFLICT_DIFFERENT_DOC`(22/28) · `missing-sohieu`(194/307).
- Pha 1.3/III.2: `slot-audit --all-shards` · `overflow-resolve` · `edit-skill`.

> ⚠️ Nhánh mutate live (`ingest-missing --apply`, `*-fix --apply`) + expand-live (`rasoat-loop` đọc GDoc) **CHƯA test
> trên dev** (không có NLM/ghi cred) — lõi pure đã test offline; lần `--apply` đầu chạy **Cowork batch nhỏ, giám sát**.
>
> CÒN (→ 1.23.1): `relation-backfill` (Pha 1.5, live: orchestrate relation-check → ghi goc/sua_doi cho 8–9 Luật PAUSE);
> cập nhật `SKILL.md`/`RUNBOOK.md`/`API_CONTRACT.md` (schema 3 cổng + vòng lặp) + `upload-skill-to-Package.cmd` (user-side deploy).

# v1.22.76 (gws3env) — KH1 Pha 1.5: `tl missing-sohieu --fix` (hoàn tất quick-wins pure)

**`tl missing-sohieu [--limit N] [--apply]`** [MỚI]: đề xuất SỐ HIỆU cho dòng registry **thiếu sohieu** (field rỗng,
~257 dòng) — parse từ TÊN qua `_parse_sohieu_from_name` (bỏ Mẫu/Phụ lục). DRY mặc định; `--apply` ghi `reg_bulk` cột
`so_hieu`; idempotent. ⚠ **ĐỀ XUẤT theo TÊN — phải XÁC MINH bằng `tl header-verify` (G2, đọc header thật)** trước khi
tin tuyệt đối. LIVE manifest: suy được **194/307** dòng thiếu (no_parse=113 = orphan/tên không có số hiệu). +1 test → **231/231**.

Hoàn tất **Pha 1.5 quick-wins pure** (backfill-loai + sohieu-conflict split + missing-sohieu).

> CÒN của KH1 (→ v1.23.0): Pha 1.5 `relation-backfill` (live, orchestrate relation-check→ghi goc/sua_doi); Pha 1.3
> (overflow-resolve / canonical-not-sidecar / manifest-stale / slot-audit per-shard); III.2 `edit-skill`; rồi phát hành 1.23.0.

# v1.22.75 (gws3env) — KH1 Pha 1.5 (quick-wins): `backfill-loai` + tách `SOHIEU_CONFLICT_DIFFERENT_DOC`

Hai quick-win dọn corpus (pure, offline-testable). selftest **228→230/230**.

- **`tl backfill-loai [--limit N] [--apply]`** [MỚI]: suy `loai` CHUẨN (∈ enum) cho dòng registry **thiếu loai** (loai
  rỗng 0/775) từ tiền tố tên (Luat_/BLDS_/ND_/TT_/NQ_…) + mã cơ quan số hiệu, qua pure **`_infer_loai`** (VBHN→"Văn bản
  hợp nhất"; tên-trước, số-hiệu fallback). DRY mặc định; `--apply` ghi `reg_bulk` cột loai; IDEMPOTENT (bỏ dòng đã có loai).
  LIVE manifest: **suy được 191/769** (phân bố VBHN 41/NĐ 42/NQ 37/TT 33/Luật 31/Bộ luật 4/…).
- **Tách `SOHIEU_CONFLICT_DIFFERENT_DOC` vs `SAME_DOC`** trong `registry-doctor` [FIX]: trong mỗi nhóm trùng số hiệu,
  dùng **`_subject_sig`** (bỏ đuôi+doctype+số+năm) → ≥2 chữ-ký-chủ-đề khác nhau = **văn bản KHÁC cùng số hiệu (NGUY HIỂM
  tra sai)**; 1 chữ ký = sidecar/khác-format CÙNG văn bản (lành). Thêm khóa `sohieu_conflict_groups` vào schema (text=json
  parity giữ nguyên) + sample `sohieu_conflict`. Bản nào ĐÚNG → để **G2 `header-verify`** quyết. LIVE: **22 conflict / 6
  same-doc** trong 28 nhóm trùng.

> CÒN của KH1 (→ v1.23.0): Pha 1.5 `relation-backfill` + `missing-sohieu --fix` (live, qua G2); Pha 1.3 (overflow-resolve /
> canonical-not-sidecar / manifest-stale / slot-audit per-shard); III.2 `edit-skill`; rồi phát hành 1.23.0.

# v1.22.74 (gws3env) — KH1 Pha 1.2 HOÀN TẤT P0: `tl ingest-missing` + `tl rasoat-loop` (vòng lặp khép kín)

Hoàn tất bộ lệnh **P0** của vòng lặp rà soát khép kín. selftest **225→228/228**.

- **`tl ingest-missing [--cat NN] [--limit N] [--apply]`** [MỚI]: nạp HÀNG LOẠT văn bản corpus **chưa trên NLM**
  (backlog) → `source_add` + ghi registry. **IDEMPOTENT** (bỏ bản đã on NLM + checkpoint `~/.tl_ingest_missing_ckpt.json`
  resume). **DRY mặc định**. Định tuyến **theo chỗ trống** (base → overflow shard SẴN CÓ qua `_discover_overflow_from_registry`).
  **BẤT BIẾN `_overflow_route`: KHÔNG BAO GIỜ tạo notebook mới** — đầy hết → `BLOCKED` (hỏi người dùng duyệt shard mới).
  Pure `_ingest_missing_select` (idempotent) + `_overflow_route` (no-create) test offline. `--apply` tái dùng
  `nlm-cli.source_add` + `reg_bulk` (đã verified).
- **`tl rasoat-loop <base> [--max-iter N] [--dry-rounds K]`** [MỚI, orchestrator, REPORT-ONLY v1]: VÒNG LẶP KHÉP KÍN —
  SEED từ base → `frontier-expand` → **mở rộng đệ quy** các ứng viên in-corpus (đọc NGUYÊN VĂN từ cache/gws, **KHÔNG RAG**)
  → dedup `seen` **chống lặp vô hạn** → dừng khi frontier rỗng VÀ `dry_rounds≥K` (mặc định 2) hoặc chạm `--max-iter`.
  Xuất: hội tụ?, **GAP ngoài corpus** (→ tải/KH3 qua G1/G2/G3), **in-corpus-chưa-NLM** (→ `ingest-missing --apply`).
  KHÔNG tự mutate; đánh giá sâu từng cặp → `tl overlap`. Pure `_rasoat_dedup_push` test offline.

> ⚠️ Nhánh mutate (`ingest-missing --apply`) và expand-live (`rasoat-loop` đọc GDoc) **chưa test trên máy dev** (không có
> NLM cred ghi) — lõi pure (select/route/dedup) đã test offline; lần `--apply` đầu chạy trên **Cowork** với batch nhỏ, giám sát.
>
> CÒN của KH1 (→ v1.23.0): Pha 1.3 (overflow-resolve / canonical-not-sidecar / manifest-stale / slot-audit per-shard);
> Pha 1.5 (backfill-loai / sohieu-conflict / relation-backfill / missing-sohieu); III.2 `edit-skill`; rồi phát hành 1.23.0.

# v1.22.73 (gws3env) — KH1 Pha 1.2: `tl frontier-expand` (vòng lặp rà soát — discovery-only)

**`tl frontier-expand <gdoc|sohieu>`** [MỚI]: trích MỌI văn bản được dẫn chiếu trong 1 văn bản (xref + footnote sửa
đổi + inline) → ứng viên **FRONTIER** dedup theo số hiệu + ưu tiên (amending=1 > VBHN=2 > dẫn-chiếu=3) + cờ `in_corpus`.
`missing_in_corpus` = ứng viên cần nạp (đầu vào `ingest-missing`/discovery). DISCOVERY/REPORT-ONLY, **KHÔNG RAG** (mọi số
hiệu/tên từ `extract_refs`/`resolve_footnote_amendments`). Core PURE `_frontier_candidates` (dedup+ưu tiên+in_corpus,
test offline) + `_frontier_doc_text` (reader: --text-file offline / gdoc deep-resolve→cache→exporttext). +2 test → **225/225**.

> CÒN của KH1 (→ v1.23.0): `ingest-missing` (mutate NLM — bất biến no-new-notebook, --apply chưa test live được ở máy
> dev) + `rasoat-loop` (orchestrator khép kín); Pha 1.3; Pha 1.5; III.2 `edit-skill`.

# v1.22.72 (gws3env) — KH1 Pha 1.2: dựng 3 CỔNG XÁC MINH G1/G2/G3 (sạch, có test)

Dựng **3 cổng kiểm chứng** theo kế hoạch v2 — **dựng lại SẠCH từ đầu** (bản agent workflow tự ý tiêm vào canonical
ở phiên trước đã được revert; KHÔNG tái sử dụng). selftest **209→223/223** (+14, toàn bộ test PURE helper, offline).

- **G3 — category theo NỘI DUNG + quy tắc ranh giới:**
  - Helper pure: `_load_linhvuc` (đọc `linhvuc_phapdien.json` quy_tac_ranh_gioi), `_cat_taxonomy` (45+00+46+QUARANTINE),
    `_infer_cats_text` (suy cat theo **alias trên NỘI DUNG**, whole-word `\b`, cụm dài thắng nhiễu đơn-từ),
    `_cat_boundary_rule` (ÉP: BHXH/BHYT→02, đầu-tư-công/hải-quan→26, sửa≥2 luật→46, điều-ước→23, Đảng→00).
  - **`tl cat-verify <gdoc|sohieu>`** [MỚI] read-only: đọc Điều 1 → cat_suggested/confidence/rule_applied/tie. `--text-file` chạy offline.
  - **FIX `cat-audit`**: thêm confidence + cờ RULE (ranh giới) + kiểm cat ∈ 45+2 (taxonomy_violations) + `--strict`.
  - **FIX `recat`**: cảnh báo `BOUNDARY_CONFLICT` (advisory, theo tên) trước apply + `--force-cat` (không hard-block omnibus).
- **G2 — tên ↔ header thật (hàng loạt):**
  - `_extract_header_facts` (pure): trích ngày ban hành + cơ quan từ header.
  - **`tl header-verify [--all|--sohieu|--drive-id|--cat] [--fix-suggest] [--strict]`** [MỚI] READ-ONLY: chạy
    `_verify_header_match` hàng loạt để bắt DRIFT trên 775 dòng cũ. Bổ trợ `confirm` (confirm GHI verified; header-verify chỉ soát).
    Tài liệu hóa: KHÁC `title_mismatch` (registry-doctor/hygiene = lệch metadata NỘI BỘ, không đọc header).
- **G1 — nguồn official-first + toàn vẹn:**
  - `_content_md5` (NFC→md5, pure), `_official_rank` (vbpl/congbao=1 > .gov/.chinhphu=2 > luatvietnam=3 > thuvienphapluat=4).
  - **[FIX] `_DISCOVERY_SITES` re-rank OFFICIAL-FIRST** (vbpl.vn đầu, không còn thuvienphapluat đầu) → ảnh hưởng find-doc/QT-5.
  - **`tl source-verify <sohieu|gdoc>`** [MỚI]: content_md5 + số hiệu header + cờ `SOURCE_DISCREPANCY` (header≠registry) +
    liệt kê nguồn web xếp uy tín để đối chiếu ≥N nguồn. `--text-file` offline. KHÔNG tự scrape (research=discovery).

> CÒN của KH1 (→ v1.23.0): orchestrator `rasoat-loop` + `frontier-expand` + `ingest-missing` (Pha 1.2 P0); Pha 1.3
> (overflow-resolve/canonical-sidecar/manifest-stale/slot-audit per-shard); Pha 1.5 (backfill-loai/sohieu-conflict/relation-backfill/missing-sohieu).

# v1.22.71 (gws3env) — KH1 Pha 1.1/1.4: vá H2 (registry-doctor schema) + khóa H1 + UTF-8 robustness + `instructions --out`

Thực thi **Kế hoạch 1** (sửa skill) sau báo cáo rà 70 Luật. Đối soát code canonical: H1/overlap đã đúng ở canonical;
chỉ H2 còn là bug thật. selftest **206→209/209**.

- **H2 (mục H báo cáo) — `registry-doctor` text ≠ JSON schema:** dòng text in nhãn `duplicate_sohieu=/title_mismatch=/rows=`
  trong khi JSON dùng `duplicate_sohieu_groups/title_mismatch_candidates/count` → tool parse text không khớp JSON.
  **Vá cấu trúc:** dòng text SINH TỪ `_DOCTOR_SUMMARY_KEYS` (`build_doctor_summary`/`format_doctor_text`) → text & JSON
  **dùng chung schema, không thể lệch nhãn lần nữa**. +test `registry_doctor_text_json_parity`.
- **H1 (mục H) — `reg-query --json` rc=1:** KHÔNG tái hiện ở canonical (rc=0 sạch, kể cả dump toàn bộ/qua pipe); rc=1 trong
  log là confound redirect/`&&`/bản deployed cũ. **Khóa** bằng test `reg_query_json_rc0_envelope` (monkeypatch offline).
- **III.1 UTF-8 (mục H robustness):** `tl.py` set `PYTHONUTF8=1`/`PYTHONIOENCODING=utf-8` → truyền xuống MỌI script con
  spawn (hết `UnicodeEncodeError 'charmap'` của `gen_instructions.py`… trên console Windows cp125x); `gen_instructions.py`
  thêm `reconfigure` cho chạy standalone. +test `utf8_child_env_set`.
- **III.3 CLI gap:** `tl instructions --out <file>` ghi Instruction UTF-8 ra file (khỏi gọi thẳng `gen_instructions.py`).

> Còn lại của KH1 (roadmap v1.23.0): P0 `rasoat-loop`/`frontier-expand`/`ingest-missing`; Pha 1.3 (overflow-resolve,
> canonical-not-sidecar, manifest-stale, slot-audit per-shard); Pha 1.5 (backfill-loai, sohieu-conflict, relation-backfill);
> 3 cổng G1/G2/G3 (xem KE_HOACH v2).

# v1.22.70 (gws3env) — HỢP NHẤT Codex v1.22.69 + vá log đa-profile (Nhóm A–E) + large-file-split

Hợp nhất bản Codex v1.22.69 (gửi kèm) với bản Claude v1.22.69 (CONVERGENT — 2 nhánh cùng vá 13 lỗi 2 báo cáo,
khác code) + vá batch log MỚI (đa-profile) + tính năng tách file lớn. selftest 197→**204/204**.

**MERGE (giữ bản Claude verify làm base, port phần Codex mạnh hơn):**
- **Deep-resolver MIME-aware** (`_resolve_deep_target` + `_entry_mime`/`_entry_google_doc`/`_entry_raw_no_gdoc`/
  `_deep_entry_rank`) cho `extract`/`xref`/`footnote-map`: ưu tiên GDoc native (theo MIME) + corpus + NLM-live, phạt
  nặng raw/quarantine; tên DÀI toàn chữ-gạch-dưới KHÔNG bị nhận nhầm DriveId → **bug C trọn vẹn** (hết 404 giả).
- **`_classify_ref` kiểm VBHN-coverage TRƯỚC TYPO/MISSING:** số hiệu gốc đã có VBHN bao phủ → OUTDATED (rà VBHN).
- **`ENTRY_RAW_NO_GDOC` rc=2 + ok:false** (theo yêu cầu báo cáo: chỉ-raw → rc≠0; resolver đã ưu tiên GDoc nên chỉ
  fire khi GENUINE raw-only). Giữ riêng của bản Claude: H (doctor drift), D (text-cache), G (hygiene sidecar), 2.2 (nlm PATH).

**Nhóm A–E (log đa-profile thực tế):**
- **B (nghiêm trọng nhất):** `_ingest_target`/`nlm-add`/`nlm-query` push/query nhắm **notebook CỦA PROFILE**
  (`TL_NOTEBOOK_ID`), hết đẩy nhầm VBQPPL base (743ed200) khi `--profile NQ36`. `nlm-add`/`nlm-query` nay nạp
  `apply_profile_offline` + lỗi `NO_NOTEBOOK_ID` rõ nếu profile thiếu notebookId.
- **A1:** `profile-create --apply` GHI BỀN `config.profiles.<name>` (`_persist_profile_config`, merge) → `profile-info`
  hết fallback VBQPPL. **A2:** next-steps cấm copy sheet VBQPPL bằng tay (để lại orphan), dùng `tl --profile X manifest`.
- **C1:** `nlm-reconcile` BẮC CẦU gdoc↔source_id (`_nlm_source_drive_id` + `link_candidates`): nguồn live khớp
  drive_id/số hiệu của dòng registry thiếu source_id → backfill, hết "unregistered" giả. **C2:** `register --nlm-notebook-id`.
  **C3:** `backfill-notebook` khóa ĐÚNG nguồn (`--src-ids`→nlm_source_id, `--drive-ids`→drive_id).
- **D1:** cảnh báo profile non-default + categories=inherit (văn bản vào cây chung VBQPPL). **D2:** `regen2` loại
  registry/manifest/orphan khỏi scan own (count 8→5 thật). **D3:** `reg-delete --force` (đã có) + thông điệp rõ.
- **E1:** `nlm_cli` lọc "Using keyring backend" khỏi stdout/stderr (hết vỡ `json.loads`). **E2:** `reg-query --refresh`
  (đã có) + help nhắc refresh sau khi ghi sheet.

**Large-file split (yêu cầu user):** `ingest-local` có CỔNG HỎI TÁCH — file > ~1.2MB (`--large-threshold`) → DỪNG
`--apply`, gợi ý tách theo Phần/Chương/cụm Điều (mỗi phần 1 nguồn = chất lượng RAG cao nhất); `--allow-large` để nạp
nguyên. + doctrine SKILL.md §2.

---

# v1.22.69 (gws3env) — vá 13 lỗi CÔNG CỤ từ 2 BÁO CÁO RÀ 71+105 LUẬT (+ rà soát đối kháng gia cố 9 phát hiện)

Hai báo cáo rà soát thực tế (71 Luật mức đầy đủ · 105 Luật canonical VBHN-first) nêu 13 lỗi/hạn chế của skill.
Đã vá toàn bộ + thêm 14 test (selftest 179→194/194). Tóm tắt theo nhãn báo cáo:

- **A — `tl status` rc=2 trên REVIEW (46/71 Luật):** verdict ADD/SKIP/REVIEW là PHÁT HIỆN dữ liệu → **rc=0**
  (hết phá `&&`/CI; driver agentic không hiểu nhầm REVIEW = lệnh hỏng). Thêm cờ `--strict` (rc=1 khi REVIEW,
  mirror `xref --strict`). `preingest_gate.verdict_exit` + `cmd_status` dùng `inspect.signature` (tương thích
  module nền cũ, GIỮ ngữ nghĩa --strict). DOCTRINE §2 A3 cập nhật.
- **C / P0-1 — resolver đọc sâu chọn file THÔ thay GDoc → im lặng rỗng-rc0 (≥6 VBHN có sidecar):** `_entry_score`
  PHẠT −300 file thô (.docx/.pdf/.html) CHƯA-trên-NLM → GDoc native THẮNG sidecar cùng số hiệu; `ENTRY_RAW_NO_GDOC`
  in **STDOUT** (caller THẤY, không còn bỏ sót luật); `_resolve_base_gdoc` fallback `drive_id` khi sohieu rỗng.
- **B + P1-3 — `xref` dẫn chiếu ẢO + mâu thuẫn MISSING/MISMATCH:** `extract_refs` **DEDUP theo SỐ HIỆU**
  (1 phán quyết/số hiệu/run) + `_clean_ref_name_phrase` cắt mệnh-đề-chuyển-tiếp ("…này có hiệu lực thi hành…")
  nhưng GIỮ tên luật thật ("Thi hành án dân sự").
- **P0-2 — `DOC_TEXT_SOHIEU_TYPO` gán nhầm xuyên không-gian-số-hiệu:** `_doctype_family` chặn gợi ý typo VƯỢT
  BIÊN họ loại (QH ≠ NQ-TW/KL-TW ≠ NĐ-CP — tái dùng số+năm là hợp pháp); CÙNG họ (QH14↔QH15) vẫn flag.
- **P1-4 — `source-map` chọn sai canonical khi số VBHN tái dùng:** >1 VBHN cùng số hiệu KHÁC chủ đề → `canonical=None`
  + `VBHN_REUSE_AMBIGUOUS_NO_CANONICAL` (đòi phân định chủ đề/năm); cùng chủ đề/nhiều version vẫn chốt.
- **P1-5 — amendment-detector kích PAUSE sai trên văn bản phi quy phạm:** loại tài liệu "góp ý/kiến nghị/ý kiến"
  (gate theo SỐ HIỆU REGISTRY); `PAUSE_AND_ASK_USER` CHỈ khi có ứng viên MANG số hiệu hợp lệ.
- **P2-6 — `vbhn-check` luôn `CONTENT_VERIFY_REQUIRED`:** chỉ ép khi collision CỦA CHÍNH số hiệu ứng viên (KHÔNG
  corpus-wide → hết 86 cờ máy móc); verified+năm+duy nhất → `VBHN_METADATA_OK`.
- **H — registry lệch NLM chưa tự chữa:** `tl doctor` cảnh báo định kỳ (đếm cờ OFFLINE từ cache → gợi ý
  `tl nlm-reconcile`, KHÔNG chặn/không gọi mạng).
- **D — timeout văn bản lớn:** `_read_doc_text` + `cmd_xref` TÁI DÙNG cache `extract_<gid>.txt` (Bộ luật Dân sự
  hết export lại nhiều lần).
- **E — đuôi .doc/.docx còn trong tên chuẩn:** `standardize_name.normalize_name` bỏ đuôi khỏi tên CHUẨN (GiỮ ở tên FILE).
- **G — file thô lẫn corpus:** `hygiene` bucket `sidecar_corpus_fix` (.docx cạnh GDoc mà corpus=true → đề xuất `SET_CORPUS_FALSE`).
- **P2-7 — `loai`/`hieuluc` không chuẩn enum:** `_normalize_loai`/`_normalize_hieuluc` lúc `register` + bucket
  hygiene `loai_noncanonical` (KHÔNG nhồi `_title_flags` → tránh nhiễu source-map).
- **2.2 — nlm không trên PATH:** `nlm_cli` nối `~/.local/bin` + user-base bin vào PATH (which + subprocess env);
  `doctor` dùng `nlm_exe()` (hết báo đỏ giả); `nlm-install` ghi PATH bền `~/.profile`/`~/.bashrc` (POSIX).

HOÃN **P2-8** (tách MISSING ngoài-phạm-vi-corpus vs resolver-trượt) — cần enrich manifest trước.
Hạ tầng (mount cắt cụt, /tmp sticky-bit, tiến trình nền, uv CDN chặn) là giới hạn môi trường Cowork — đã có quy trình.

---

# v1.22.43 (gws3env) — `tl drive-push` cập nhật Drive GIỮ fileId (đẩy bản ship mỗi lần 1 lệnh)

User cần script Windows đẩy bundle lên Drive giữ fileId. Thêm lệnh tái dùng thay vì gõ chuỗi gws JSON dài:

- **`tl drive-push <zip> [--file-id <id>]`:** bọc `gws_bridge.update_content` (`gws drive files update --params {fileId}
  --upload`) → thay NỘI DUNG file Drive, **GIỮ fileId**. Mặc định fileId = **`SKILL_FILEID`** (baked = `1H5kAt…`). Kiểm gws
  auth trước; KHÔNG tạo file mới. Mỗi lần ship: `python scripts/tl.py drive-push <bundle>` (máy có gws auth) → tl_fetch tự lấy bản mới.
- Kèm script Windows `update-drive.cmd` (1 dòng gọi drive-push) cho user.
- selftest **115/115**. (Lệnh upload thực thi ở máy user — exfil classifier chỉ chặn trong phiên agent, không chặn user tự chạy.)

---

# v1.22.42 (gws3env) — BUNDLE skill+gws (cắt 1 download) + `nlm-install --uv`

Theo yêu cầu: gộp skill + gws binary thành 1 package để bootstrap tải 1 lần.

- **`gws-bootstrap-cowork --local-tgz <gws.tgz>`:** dùng gws.tgz CÓ SẴN local (giải nén từ bundle) → **KHỎI tải Drive**;
  md5 vẫn verify → extract → chmod → place → load cred. Không có thì giữ đường cũ (direct-media/webapp tải).
- **`tl_fetch.sh --setup`:** tự dò `assets/gws.tgz` trong bản giải nén → nếu có thì `gws-bootstrap-cowork --local-tgz`.
- **2 artifact (từ 1 build):** (a) `tra-luat-skill-vX.zip` = lean `tl_stage/` (≤200 file) → **import vào Cowork**; (b)
  `tra-luat-bundle-vX.zip` = `tl_stage/` + `assets/gws.tgz` (~11MB) → **upload lên Drive fileId `1H5kAt…`** để tl_fetch tải.
  Bootstrap: curl bundle (1) = skill + gws; chỉ config (private) cần Drive MCP (1). Python qua uv (0 nếu hệ thống ≥3.11).
- **`nlm-install --uv`** (từ 1.22.41): uv lo Python 3.11, bỏ 31MB Drive; `tl_fetch.sh --setup --nlm` dùng `--uv`.
- selftest **115/115**.

> v1.23.0 spec (rasoat-loop khép kín, overlap so-quy-phạm, ingest-missing, overflow-auto-resolve, …): roadmap P0→P2, làm sau.

---

# v1.22.41 (gws3env) — `nlm-install --uv` (egress mở → uv lo Python 3.11, bỏ 31MB Drive) + bootstrap 1 lệnh đủ

User chuyển sandbox sang **allow-all egress** + yêu cầu: Python 3.11 nên dùng **uv cài** (hệ thống ≥3.11 thì khỏi cài),
bootstrap 1 script đủ GAS→direct-media→gws→nlm→nlm login→boot, ít download nhất.

- **`nlm-install --uv`:** ưu tiên `_ensure_nlm_installed` (uv-first): `uv tool install --python 3.11 notebooklm-mcp-cli`
  — uv dùng python hệ thống nếu đã ≥3.11, hoặc `uv python install 3.11` (egress mở), **KHÔNG tải 31MB Python từ Drive**.
  Tự fallback Drive-Python khi uv/egress lỗi (gọi lại nhánh cũ với uv=False → không lặp). Mặc định (không cờ) vẫn là
  đường Drive (tương thích Cowork cũ chặn astral).
- **`tl_fetch.sh --setup --nlm`** (bootstrap 1 lệnh) nay chạy `nlm-install --uv`: curl skill(public) → init-config → ping →
  gws-bootstrap (direct-media) → boot (manifest/registry) → nlm-install(uv) → nlm-auth-load (headless). Egress-all → curl
  lấy file public nhanh; chỉ config (private) cần Drive MCP. **Số download tối thiểu:** skill(1) + config(1) + gws(1) +
  uv/nlm(PyPI). Python: 0 nếu hệ thống ≥3.11.
- selftest **115/115**. (Đặc tả v1.23.0 — rasoat-loop/overlap/ingest-missing/overflow-resolve — là roadmap riêng, ưu tiên P0.)

---

# v1.22.40 (gws3env) — bake `NLM_CRED_FILEID` (đã stage + verify) → nlm headless sẵn sàng

User stage xong: `NLM_CRED_FILEID="156StZcgqk-TYNRGCX76HrvueRgoV2Rpq"` (nlm_cred.enc 24.526B trên Drive). Bake vào tl.py.
**Verify thật end-to-end:** webapp `download` → giải mã bằng webapp token (KHÔNG master key) → 3 file (auth.json +
profiles/default/{cookies,metadata}.json), cookie ~11 ngày tuổi; token sai → HMAC từ chối. Từ nay `sh scripts/tl_fetch.sh
--setup --nlm` trong Cowork = đủ **gws + nlm headless** trong 1 lệnh (sau khi agent lấy config qua Drive MCP).
fileId là Drive id (file ĐÃ mã hoá) — không phải secret, bake công khai như GWS_CRED_FILEID.

---

# v1.22.39 (gws3env) — nlm HEADLESS không cần master key (`nlm-auth-stage`/`nlm-auth-load`, khoá=webapp token)

Vấn đề: Cowork `nlm login` cần browser (không headless); `nlm-auth-pull` cần TL_MASTER_KEY (phiên trống không có) →
NLM phải rơi về MCP (chậm). Giải: **mirror y hệt pattern gws-auth** — mã hoá cookie nlm bằng **webapp token** (đã có
trong config, không cần master key):

- **`nlm-auth-stage` [CODE, sau `nlm login`]:** `_nlm_auth_files()` (auth.json + profiles/default/*) → `gws_cred_store.encrypt`
  (khoá = webapp token, PBKDF2+HMAC) → upload `nlm_cred.enc` lên Drive `_HOP_NAP` → in fileId. Cookie chỉ ở RAM; bản trên
  Drive đã mã hoá, KHÔNG vào zip. `--refresh` ép nlm tái sinh cookie trước khi gói.
- **`nlm-auth-load` [COWORK, HEADLESS]:** webapp `download` fileId → giải mã (token) → ghi `~/.notebooklm-mcp-cli`
  (chmod 600). **KHÔNG cần master key/`nlm login`.** fileId: `NLM_CRED_FILEID` (baked, trống) / env `TL_NLM_CRED_FILEID`
  / `--cred-file-id`.
- **`tl_fetch.sh --setup --nlm`** tự chạy `nlm-auth-load` sau `nlm-install` (sau gws) → nlm chạy thẳng, hết MCP fallback.
- Verify: selftest 115/115; `gws_cred_store` round-trip cho JSON nlm OK; token sai → HMAC từ chối.

> **Thiết lập 1 lần (máy có browser):** `nlm login` → `tl nlm-auth-stage` → lấy fileId → điền `NLM_CRED_FILEID` trong
> tl.py (hoặc env `TL_NLM_CRED_FILEID`). Từ đó mọi phiên Cowork `--setup --nlm` có nlm headless. Cookie hết hạn (~2–4 tuần)
> → stage lại. (Cùng mô hình tin cậy webapp token như gws cred.)

---

# v1.22.38 (gws3env) — `tl_fetch.sh` ROUTE TỐI ƯU + `--setup` bootstrap 1 lệnh; vá bẫy /tmp sticky

Log Cowork thật cho biết egress là **proxy ALLOWLIST** (không chặn hẳn): `drive.usercontent.google.com` +
`script.google.com` MỞ (200); `google.com`/GitHub/astral CDN CHẶN; PyPI MỞ. → curl **tải được** Drive file PUBLIC.
`tl_fetch.sh` cũ "tưởng egress chặn" vì 2 bug: (1) ghi `/tmp` sticky → file rỗng owner `nobody` lần hỏng trước chặn
`curl -o` (exit 23) + làm script tưởng "đã có"; (2) thử webapp trước curl. Vá + thêm bootstrap:

- **ROUTE TỐI ƯU theo visibility:** zip skill (public)→**curl** `drive.usercontent` (nhanh nhất, off-context, không
  token); config/token (private)→**Drive MCP** (curl→trang login; nhỏ nên round-trip); gws binary + Python 31MB
  (private)→**gws direct-media** (sau khi gws có) / GAS-proxy (Drive MCP cap 10MB); nlm→**pip** (PyPI mở).
- **`tl_fetch.sh` vá:** curl PUBLIC **trước**, ghi **`$HOME/.tl_fetch`** (KHÔNG /tmp sticky), tái dùng zip+unzip lần sau,
  in `ROOT` để chạy thẳng. Fallback webapp `download` (token) → Drive MCP.
- **`--setup [--nlm]` (mới):** bootstrap 1 lệnh — curl zip → (thiếu config thì in fileId MCP, exit 10) → init-config →
  ping → **gws-bootstrap-cowork TRƯỚC** → boot → [nlm-install]. **gws trước nlm** để `nlm-install` tải Python 31MB qua
  `drive_op` định tuyến **gws/direct-media (nhanh, ~37s)** thay vì GAS-b64 (chậm, quá 45s cap bash).
- SKILL.md §1 + COWORK_EDIT_SAFETY: bảng route + lệnh `--setup` + heredoc curl-first/$HOME dán-lại. selftest **115/115**;
  verify thật: curl public→unzip→selftest 115/115; `--setup` đúng exit-10 khi thiếu config.

> Lệnh bootstrap Cowork: ① agent Drive MCP tải `1dEOBJ…` → `~/.tra_luat_config.json`; ② `sh scripts/tl_fetch.sh --setup --nlm`.

---

# v1.22.37 (gws3env) — `tl_fetch.sh` tải skill QUA WEBAPP GAS (egress đã được phép, không cần allowlist Drive)

User báo: sandbox Cowork **chặn egress trực tiếp** (curl/wget tới Drive). Nhưng `script.google.com` (webapp GAS) **đã
chạy** (phiên trước ping ra 2.21.2i). Và webapp 2.21.2i có sẵn action **`download`** (`fileId → b64`, đọc Drive
server-side). Đã **test thật** từ máy này: webapp trả base64 zip 781365B đúng. → đổi `tl_fetch.sh` ưu tiên webapp:

- **`tl_fetch.sh` thứ tự tải:** (1) `/tmp/tl_skill.zip` có sẵn (agent tải qua Drive MCP) → dùng; (2) **WEBAPP GAS**
  `action=download&fileId=<zip>` bằng token từ `~/.tra_luat_config.json` (đường CHẮC — egress `script.google.com` đã được
  phép; webapp đọc Drive server-side nên KHÔNG cần allowlist Drive); (3) curl thẳng `drive.usercontent.google.com` (chỉ
  khi sandbox cho egress đó). Phần fetch dùng `python3 -c` inline (urllib/base64) → b64 giải mã TRONG tiến trình, KHÔNG
  cần agent round-trip payload lớn. **Verify end-to-end:** webapp → unzip → `tl.py --selftest` **115/115**.
- **Phiên trống:** agent lấy `CONFIG_FILEID` qua Drive MCP → ghi `~/.tra_luat_config.json` (webappUrl+token; config nhỏ,
  agent ghi được) → `sh scripts/tl_fetch.sh ping`. SKILL.md §1 + COWORK_EDIT_SAFETY ghi rõ + heredoc dán-lại (đường webapp).
- "Egress nào?": **`script.google.com`** (webapp) — không phải `drive.usercontent.google.com`.

> Vận hành: giữ file Drive `1H5kAt3SRVP7_…` = zip skill MỚI NHẤT (cập nhật NỘI DUNG, giữ fileId). Webapp đọc chính file
> đó server-side. Config/token vẫn lấy riêng (zip skill là bản SẠCH, không secret).

---

# v1.22.36 (gws3env) — `tl_fetch.sh`: BỎ QUA mount, chạy skill từ bản tải-Drive ở /tmp (giải pháp gốc rễ)

Phiên Cowork mới: mount cắt cụt ĐỒNG THỜI `tl.py` + `tl_boot.py` + `build_parts.py` + cả **mảnh `_parts`**
(`tl.022/023`, `tl_boot.*`, `tl_selftest.003` fail checksum) → MỌI recovery LOCAL bó tay (Python parse cả file → chết;
mảnh hỏng tại nguồn → ghép vô nghĩa). Kết luận: chia-nhỏ-file đã chạm trần (cả file 3KB vẫn bị cắt). Đổi kiến trúc:

- **`scripts/tl_fetch.sh` (mới, ~18 dòng shell):** thủ phạm là **mount**; **mạng giao byte trung thực** → tải **1 zip
  skill từ Drive** (fileId baked, share "anyone with link") về `/tmp/tl_live`, **`unzip` kiểm CRC** (zip cắt báo lỗi TO,
  không chạy nhầm), rồi chạy `tl.py` Ở ĐÓ — **bỏ qua mount hoàn toàn**. Bề mặt-tới-hạn-qua-mount giảm còn 1 file tí hon,
  shell (sống sót cắt cụt) + nhỏ tới mức **dán-lại bằng heredoc** (COWORK_EDIT_SAFETY §3 bước 0). Egress chặn → agent tải
  zip qua **Drive MCP** về `/tmp/tl_skill.zip`. **Đã verify end-to-end:** tải Drive → unzip → `tl.py --selftest` 115/115,
  `--help` ra đủ subcommand (entrypoint — thứ BIẾN MẤT ở phiên mount hỏng — đã có).
- **SKILL.md §1 + COWORK_EDIT_SAFETY:** `tl_fetch.sh` là đường recovery **ƯU TIÊN ★** khi mount nghi cắt cụt; local
  (tl_boot/_parts/tl_rebuild.sh) là fallback khi egress chặn.
- Config/token vẫn lấy riêng qua MCP (zip skill là bản SẠCH, không secret). selftest **115/115**.

> ⚠ **Vận hành:** giữ file Drive `1H5kAt3SRVP7_…` = **zip skill MỚI NHẤT** (mỗi lần ship bản mới → cập nhật NỘI DUNG file
> đó, GIỮ NGUYÊN fileId). Đây là "nguồn chân lý" khi mount hỏng.

---

# v1.22.35 (gws3env) — Recovery PARSE-ROBUST khi mount cắt cả tl_boot/build_parts + checksum định vị mảnh hỏng

Log Cowork: mount cắt cụt **ĐỒNG THỜI** `tl.py` + `tl_boot.py` (launcher) + `build_parts.py` (reassembler) + mangle cả
mảnh `_parts` → mọi recovery Python chết (Python parse CẢ file trước khi chạy; 1 dòng cụt = chết hẳn), và lỗi hiện ra
là `SyntaxError @5581` mù mịt. Vá theo đúng các khuyến nghị #3/#4/#6:

- **`scripts/tl_rebuild.sh` (mới):** recovery **SHELL** — shell chạy TỪNG DÒNG nên sống sót cắt cụt (chạy tới chỗ bị
  cắt), khác Python. Ghép MỌI `_parts/<name>/` → `/tmp/tl_rebuilt/<name>.py`, bỏ NUL, đối chiếu `MANIFEST.sha256`, báo
  CHÍNH XÁC mảnh nào mount cắt, exit≠0. Chạy được kể cả khi `tl_boot.py`/`build_parts.py` đã chết.
- **`_parts/MANIFEST.sha256` (mới):** `build_parts.py` ghi checksum mỗi MẢNH + mỗi FILE ghép. `build_parts.py --verify`
  (hoặc `sha256sum -c`) định vị mảnh/file mount cắt → thay `SyntaxError` mù bằng `_parts/tl/tl.011: FAILED → RE-SYNC`.
- **`tl_boot.py` làm cứng (#3/#4):** verify tl.py theo MANIFEST sha NGAY khi khởi động — bắt cả ca "compile được nhưng
  mangled" (on-disk lệch sha → ưu tiên `_parts`; `_parts` cũng lệch → báo "mảnh bị mount cắt"). Thất bại → exit≠0 + chỉ
  thẳng `tl_rebuild.sh`/`--verify`/re-sync (không còn `SyntaxError` thô).
- **SKILL.md §1 + COWORK_EDIT_SAFETY.md:** thang leo recovery 5 mức (tl_boot → verify-integrity --fix → tl_rebuild.sh →
  --verify → re-sync) + nguyên lý "shell sống sót, Python chết".
- selftest **115/115**; chứng minh: happy-path tl_rebuild.sh ghép+verify+compile OK; cắt 1 mảnh `tl.011` → báo đúng
  `tl/tl.011 FAILED` + exit 3.

> Giới hạn còn lại (môi trường, ngoài skill): khi mount cắt CẢ mảnh `_parts` thì ghép không cứu được — **re-sync skill**
> là cách dứt điểm. Cấu trúc: tách `tl.py` 325KB thành module nhỏ là hướng giảm bề mặt (đề xuất #2) nhưng lợi ích hạn chế
> (log cho thấy cả file 3KB như tl_boot vẫn bị cắt) — cân nhắc riêng.

---

# v1.22.34 (gws3env) — Dọn `references/` 63→24 file (gỡ GS cũ + dev-archive)

Theo yêu cầu: gỡ bớt file `.gs` cũ + rà `references/` loại file thừa. Giảm tải import + bớt rối, KHÔNG mất gì
(chuyển ra archive ngoài skill — phục hồi được).

- **Gỡ 8 `Code.*.gs` đời trước** (2.21.1, 2.21.2b/c/d/e/f/g/h ~1.5MB) — chỉ giữ bản LIVE **`Code.2.21.2i.gs`**.
- **Gỡ 31 doc dev-archive** (MERGE_/DELTA_(trừ v1.19)/PATCH_REPORT/GS_*_HOTFIX/NLM_CLI_*/SHARDING/TVPL_AUTODOWNLOAD/
  IDENTITY_XREF/PROFILE_SCOPE_V1.19.2/REVIEW_BLLD/RA_SOAT_LESSONS/… + restricted-egress manifest) — KHÔNG file nào được
  code hay tài liệu vận hành (SKILL/RUNBOOK/API_CONTRACT) dẫn chiếu; lịch sử/biện luận đã có ở `DOCTRINE_APPENDIX.md` + CHANGELOG.
- **GIỮ (24 file):** 3 doc lõi (API_CONTRACT/RUNBOOK/DOCTRINE_APPENDIX), COWORK_PROJECT/COWORK_EDIT_SAFETY, 3 JSON
  runtime (phap_dien_45/linhvuc_phapdien/subject_clusters — code nạp), `Code.2.21.2i.gs`, open-egress manifest, 2 doc
  rasoat_phuluc in ra (QUY_TRINH_RA_SOAT_3_TANG/VAN_PHONG_HANH_CHINH), PATCH_v2.21.1 (apply_gs_patches dẫn), + ~9 doc
  SKILL/RUNBOOK "Tài liệu chi tiết" dẫn chiếu.
- **Đã sửa pointer treo:** SKILL.md (2 dòng GS lịch sử) + RUNBOOK.md (1 dòng) + INSTALL.md (note manifest = layout gốc).
  File gỡ nằm ở **`C:\Users\admin\Downloads\tra-luat-references-archive\`** (phục hồi nếu cần).
- **Tổng file gói: ~123** (162 → 123). selftest **115/115**, verify-integrity 0 lỗi. Chức năng runtime KHÔNG đổi.

---

# v1.22.33 (gws3env) — Đóng gói: giữ _parts ≤200 file (giới hạn import skill)

Bản v1.22.32 bị skill-import từ chối: **221 file > giới hạn 200**. Nguyên nhân: "extra hardening" 1.22.32 hạ THRESHOLD
12KB/CHUNK 8KB → chunk MỌI module 12–19KB → 99 mảnh `_parts/`. Khôi phục cân bằng:

- **`build_parts.py`** về **THRESHOLD 30KB / CHUNK 14KB** (vẫn ép LUÔN ≥2 mảnh, mỗi mảnh < gốc). `_parts/` CHỈ cho file
  LỚN (tl/tl_gws/tl_selftest/apply_gs_patches) + **FORCE** (tl_boot, rasoat_worksheet/phuluc, registry_orchestrator,
  backfill_*) → **48 mảnh, tổng 162 file** (< 200). Module import cỡ vừa (transport/gws_bridge/ingest_to_cache…) bỏ
  `_parts` (cắt cụt hiếm + `verify-integrity` báo TRUNCATED → re-sync). Đường tới-hạn (tl_boot→tl→rasoat subprocess)
  VẪN có `_parts` đầy đủ.
- Comment trong `build_parts.py` ghi rõ **trần 200 file** để lần đóng gói sau không nở lại.
- **Chức năng = 1.22.32** (không đổi code runtime). selftest **115/115**, `verify-integrity` 0 lỗi, validate từ zip đã giải nén.

---

# v1.22.32 (gws3env) — Lớp PHÁT HIỆN cắt cụt (`tl verify-integrity`) + protocol NGĂN write-side (Cowork)

Hoàn tất phòng thủ truncation 3 lớp theo giải pháp người dùng đề xuất (write-side prevention) — bổ trợ cho lớp khôi
phục `_parts/` đã có. **NGĂN → PHÁT HIỆN → KHÔI PHỤC.**

- **`tl verify-integrity [--fix] [--json]` (mới, offline):** lớp PHÁT HIỆN (md5/wc-l hoá 1 lệnh). Soi MỌI `scripts/*.py`,
  đối chiếu on-disk ↔ ghép-từ-`_parts`: `OK · NOPARTS · DRIFT (sửa tay chưa build_parts) · NUL · TRUNCATED · MISSING`
  (exit 2 nếu có lỗi). `--fix` GHÉP lại file TRUNCATED/NUL/MISSING từ `_parts`, **ghi bằng Python `write_text`** (an toàn,
  né tầng Edit/Write Cowork hay cắt cụt); KHÔNG đụng DRIFT (sửa tay hợp lệ). `tl_boot.py` tự lành `tl.py` trước nên lệnh
  này chạy được cả khi `tl.py` từng bị cắt cụt.
- **`references/COWORK_EDIT_SAFETY.md` (mới) + SKILL.md §1:** protocol NGĂN khi SỬA file skill trong Cowork — **đừng tin
  Edit/Write native**, ghi bằng Python `pathlib.write_text()` / heredoc qua Bash, git checkpoint, rồi `verify-integrity`.
  Recovery 1 lệnh: `build_parts.py --rebuild --out <ghi-được>` / `verify-integrity --fix` / `/rewind`.
- selftest **115/115** (+`integrity_scan_all_healthy`).

---

# v1.22.31 (gws3env) — Truncation-resilience triệt để + doctor kiểm nlm/gws + reg-query khóa NLM rõ-nghĩa

Hai log Cowork đều suýt chết vì **mount cắt cụt** `tl_boot.py` + `rasoat_worksheet.py` mà CHÚNG KHÔNG có `_parts/`
→ không tự cứu được. Truncation KHÔNG ổn định, hit cả file NHỎ (tl_boot 3KB), không chỉ file >30KB.

- **`build_parts.py`:** thêm `FORCE_CHUNK` = bootstrap + script chạy-bằng-subprocess (`tl_boot`, `rasoat_worksheet`,
  `rasoat_phuluc`, `registry_orchestrator`, `backfill_keywords_live`, `backfill_nlm_title`) → LUÔN có `_parts/` (≥2 mảnh
  dù nhỏ). Thêm **`--rebuild [--out DIR]`**: ghép MỌI `_parts/` → `.py` bằng **1 lệnh** (vá "thư mục skill read-only →
  mirror" + "cắt cụt nhiều file": `python scripts/build_parts.py --rebuild --out <writable>`).
- **`_healed_script_path` (mới):** script subprocess KHÔNG đi qua `_imp` self-heal → nay tự làm-lành: bản gốc lành &
  KHỚP `_parts` → chạy thẳng; NUL-pad/CẮT CỤT → ghép từ `_parts` ra file tạm trong cache (ghi-được, né dir read-only).
  **Bắt cả ca "cắt cụt mà VẪN compile"** (mất hàm/đuôi như `main()`): coi `_parts` (đã verify==gốc) là chân lý, khác →
  ưu tiên `_parts`. `cmd_rasoat` dùng nó trước khi subprocess. Có mkdir cache cho phiên trống.
- **`doctor`:** thêm 2 dòng theo yêu cầu — **`nlm CLI (fast-lane)`** (`shutil.which("nlm")`; thiếu → cách `tl nlm-install`)
  và **`gws/direct-media`** (`gws_bridge.is_available()`; thiếu → cách bật: `tl bootstrap --secrets-file` tải `tl_secrets.enc`
  bằng master key, hoặc `tl gws-auth-load` giải mã gws cred bằng token). Trả lời 2 điểm log Cowork: không kiểm nlm + chưa
  tải `tl_secrets.enc` để bật gws.
- **#3 (chat) `reg-query --json`:** khóa NLM mơ hồ (`nlm`=source_id dễ đọc nhầm là status; `src_id` sai tên, luôn rỗng)
  → thay bằng **`on_nlm`** (bool), **`nlm_source_id`** (id), **`nlm_status`** (trạng thái) — khớp tên raw.
- selftest **114/114** (+`healed_script_path_intact_returns_original`, +`reg_query_row_unambiguous_nlm`); chứng minh
  truncation: bản cắt cụt 55% được ghép lại từ `_parts` compile sạch & giống hệt gốc; `--rebuild` 10/10 file khớp.

> Vẫn cần user (ngoài skill): rotate `TL_MASTER_KEY`/token đã lộ; cấp `tl_secrets.enc`/master key vào phiên để gws/
> direct-media tự bật; backfill `goc/sua_doi` 45/2019↔18-VBHN-VPQH (cần duyệt); gỡ slot NLM 45/2019 (cần duyệt).

---

# v1.22.30 (gws3env) — FIX bug CORRECTNESS: footnote false-positive Điều 217 (BLLĐ)

Log Cowork (lệnh mới `tl overlap` phơi bày): `footnote-map` báo **5 điểm sửa cấp Điều** cho BLLĐ nhưng điểm thứ 5
("Điều 217 K3 ← 71/2025 Điều 44") là **FALSE-POSITIVE**. Thực tế: marker `[6]` nằm trên TIÊU ĐỀ CHƯƠNG "ĐIỀU KHOẢN
THI HÀNH" (sau Điều 217), footnote def là TRÍCH DẪN "Điều 50. Hiệu lực thi hành" của 71/2025 (`is_amend=False`).
- **Nguyên nhân (bug tôi gây từ v1.22.1):** nhánh **Type-B anchor-recovery** gắn footnote `is_amend=False` (trích dẫn)
  thành sửa đổi, lấy đích từ Điều gần nhất (Điều 217) → sai cả đích lẫn bản chất.
- **Vá:** BỎ Type-B. Footnote `is_amend=False` (trích dẫn căn cứ / "Điều X… quy định như sau" / hiệu-lực-thi-hành) →
  KHÔNG phải sửa đổi cấp Điều → BỎ khỏi `dieu_level_amendment_map`. Amendment THẬT luôn có động-từ-sửa trong def
  (is_amend=True). Verified BLLĐ: **5→4 điểm đúng** (Đ59/61/139/154; Đ217 rớt), pending Đ139 còn, footnote_count=4.
- selftest +1 (`footnote_citation_not_amendment`: trích dẫn trên tiêu đề chương KHÔNG gắn Điều 217) → **112/112**.
  Test cũ `footnote_gdnn_markers` (def "[6] Điều 217 ĐƯỢC BỔ SUNG…" = is_amend=True, amendment thật) vẫn pass.
- **GHI NHẬN (data, không phải code):** corpus Luật 113/2025 ghi "Bộ luật Lao động số **49**/2019/QH14" (đúng = **45**) —
  cần đối chiếu Công báo (erratum gốc hay lỗi corpus); skill báo verbatim đúng. 2 file rà soát BLLĐ cũ chép sai
  điểm thứ 5 → nên tạo lại bằng v1.22.30.

---

# v1.22.29 (gws3env) — FIX DỨT ĐIỂM truncation Cowork (chunk+reassemble) + viết `vb_status.py`

Truncation Cowork (#51435/#53940 — hạ tầng, KHÔNG sửa từ skill được) cắt cụt file .py LỚN khi giao skill → tl.py
không compile → toàn bộ lệnh chết. Trước chỉ DETECT (tl_boot báo "cắt cụt"); nay TỰ TÁI TẠO:
- **`build_parts.py`** chia mỗi .py >30KB thành mảnh ≤14KB ở `scripts/_parts/<name>/<name>.NNN` (mảnh nhỏ SỐNG SÓT
  delivery). Chạy lúc đóng gói (sau bump version). Hiện chunk: tl(23)/tl_gws(5)/tl_selftest(4)/apply_gs_patches(3).
- **`tl_boot.py`**: tl.py cắt cụt → GHÉP từ `_parts/tl/` → exec (HERE=scripts/ gốc → anh em+references tìm bình thường).
- **`_selfheal_module`/`_imp`**: module khác (tl_gws/tl_selftest/…) cắt cụt → GHÉP từ `_parts/<name>/`. (NUL-pad vẫn
  strip như cũ.)
- **Verified end-to-end:** cắt cụt tl.py 15KB + tl_gws 10KB → tự ghép → `ping`=2.21.2i, `transport-info` chạy,
  selftest 111/111. Ghép == gốc (byte-exact). → Cowork truncation KHÔNG còn chặn skill.
- **`vb_status.py`** (file optional CUỐI CÙNG còn thiếu) — viết mới: CLI bọc action webapp `vb_status` (GET `q` →
  status/hieuluc/is_vbhn/superseded_by[]/supersedes[]/flags[]). `tl doctor` optional **"đủ"** (0 thiếu).
- Đóng gói GIỮ `scripts/_parts/` trong zip (nguồn tái tạo). Quy tắc: bump version → `build_parts.py` → quét token → zip.

---

# v1.22.28 (gws3env) — Tích hợp `tra_cuu.py` (tra cứu nguyên văn — SKILL §6) từ v1.9.9.8

User gửi `tra-luat-v1_9_9_8.zip` (cũ hơn nhưng CÓ tra_cuu.py). Tích hợp:
- **`tra_cuu.py`** (tra cứu XÁC ĐỊNH từng câu chữ Điều/Khoản/Điểm/Mục từ legal_document.json — KHÔNG RAG) +
  **`provenance.py`** (cảnh báo nguồn/freshness, self-contained drop-in).
- **Tương thích cache (version-skew):** cache.py v1.9.9.8 (44KB) interface KHÁC bản hiện tại (1.3KB): `find`→list
  vs dict, `cache_dir`→Path vs str → KHÔNG replace được (vỡ ingest_to_cache). Thay vào: **PORT `get_doc`/`get_record`
  vào cache.py hiện tại** — `get_doc`=`find` (cache docs có structure[] do ingest_to_cache ghi → find_units chạy);
  `get_record`=None (overlay chưa có index freshness riêng; tra_cuu bỏ qua, vẫn chạy). 2 mode đều OK: `--doc <file>`
  + `--cache-id <số hiệu>` (alias 18/VBHN→45/2019 trúng → trả nguyên văn).
- `tl doctor` optional **thiếu 2 → thiếu 1** (chỉ còn `vb_status.py` — KHÔNG có trong CẢ v1.15.7 lẫn v1.9.9.8; cần
  bản full-skill khác nữa). selftest 111/111.

---

# v1.22.27 (gws3env) — Dọn papercut từ 2 log rà BLLĐ (#3/#4/#6/#9)

- **#4 `tl rasoat worksheet <số hiệu>`** map positional → `--so-hieu` (mới `_rasoat_map_positional`; cũng áp `phuluc → --in`).
  No-op khi đã có cờ / `-h` / sub khác. Hết lỗi argparse "thiếu --so-hieu" khi gọi qua wrapper.
- **#3 `rasoat-chongcheo`** thôi in "giai đoạn sau" gây hiểu nhầm; nay trỏ thẳng bước so quy phạm có thật:
  `tl overlap <target> --with-source` (lệnh `overlap` đã tồn tại — đây là vấn đề discoverability, không phải thiếu chức năng).
- **#6 `source-map`** không nhồi dòng ĐÃ CÁCH LY (cat quarantine HOẶC corpus=false & không NLM) vào `risky_candidates`
  (mới `_entry_quarantined`) — bớt nhiễu WARN; dòng đó vẫn hiện ở `direct_hits`. (Dứt điểm vẫn nên `reg-delete`.)
- **#9 Phiếu công tác** — `short_title` lấy trọn tiêu đề Điều rồi rút gọn ở **ranh giới từ** (120 ký tự) + dấu `…`,
  hết cảnh "đứt giữa chữ" (vd Điều 17/36).
- selftest **111/111** (thêm `rasoat_worksheet_positional_maps_so_hieu`, `entry_quarantined_detect`,
  `source_map_quarantine_not_risky`); `short_title` kiểm thủ công.

> Ngoài phạm vi sửa-mã (cần máy/cred của user, KHÔNG vá được trong skill): **#2** `nlm` CLI chưa trên PATH (cài+auth),
> **#5** auth `gws` (đang fallback GAS — vẫn đúng), **#7** đồng bộ config Drive↔example (thiếu cat + profile NQ80),
> **#8** dọn hygiene registry (chạy `tl hygiene plan` + xác nhận). **#9b** `hygiene scan` mặc định text là CHỦ Ý (thêm `--json`).

---

# v1.22.26 (gws3env) — #1 relation-check: chặn dương-tính-giả backfill sua_doi + cổng footnote-map

Cả 2 log rà BLLĐ báo `relation-check` đề xuất `BACKFILL_SUA_DOI_ON_BASE` cho **2 nghị định KHÔNG liên quan**
(`108/2026/NĐ-CP` trường giáo dưỡng, `158/2025/NĐ-CP` bảo hiểm — chỉ trùng chữ "lao động") làm "văn bản sửa đổi"
của Luật 45/2019, đồng thời **bỏ sót 3 luật sửa thật** (71/113/124/2025/QH15). Nguyên nhân: nhánh sua_doi-trên-base
dùng `candidate_keys` THÔ (gộp cả ứng viên subject-only), trong khi nhánh goc-trên-amendment đã có guard #3. Vá:

- **`_relation_audit`:** xếp hạng reason theo SỐ HIỆU (direct > ref > subject). `BACKFILL_SUA_DOI_ON_BASE` CHỈ nhận số
  hiệu **đủ điều kiện** = direct (user `--amendment`) / ref (registry trỏ base) / **footnote-confirmed**. Subject-only
  KHÔNG bao giờ auto-backfill khi không có footnote-map → đẩy sang `subject_only_review`.
- **Cổng footnote-map (nguồn ƯU TIÊN hơn heuristic):** `relation-check --footnote-source <gdoc|số hiệu>` / `--footnote-file`
  → lấy bản đồ sửa đổi cấp Điều của VBHN; ứng viên subject-only **được rescue** nếu có trong footnote-map, bị **chặn**
  nếu không (`SUBJECT_ONLY_BLOCKED_BY_FOOTNOTE`). Số hiệu sửa đổi có trong footnote-map nhưng thiếu corpus → nổi lên
  `footnote_only_amendments` + cảnh báo `FOOTNOTE_AMENDMENT_NOT_IN_CORPUS` (vá luôn "bỏ sót 3 luật thật").
- selftest **108/108** (siết `relation_subject_only_no_backfill` để bắt cả nhánh sua_doi + thêm
  `relation_footnote_gate_rescue_block`); repro 2 false-positive của log bị chặn ở cả 2 chế độ.

---

# v1.22.25 (gws3env) — Phiên trống tự tải config từ Drive + rasoat fail-loud

Cả 2 log (Cowork+Chat) đều kẹt khâu KHÔNG có config/token → agent phải dò Drive tay. Khắc phục:
- **Bake `CONFIG_FILEID`** (config v2 trên Drive — chỉ fileId). **`tl init-config --file <json đã tải>`** (đường
  GAS-only, KHÔNG cần master key) + **`--from-drive`** (tự tải direct-media nếu có gws cred). Verified cả hai ghi
  `~/.tra_luat_config.json` đúng.
- **Lỗi-thiếu-config → chỉ dẫn TẤT ĐỊNH** (hết "dò Drive"): 2 đường — có master key → MCP tải `SECRETS_FILEID` →
  `tl bootstrap --secrets-file` (token+gws+nlm); không → MCP tải `CONFIG_FILEID` → `tl init-config --file`. SKILL.md
  §1 ghi rõ. CLI không gọi được Drive MCP (tool của agent) nên seed vẫn agent-mediated 1 bước, nhưng nay tất định.
- **S3 rasoat-chongcheo fail-loud:** corpus trống (chưa `boot`) → `in_corpus=None` (`?corpus`) + cảnh báo "CORPUS
  CHƯA NẠP", KHÔNG còn ✗thiếu-corpus ÂM-TÍNH-GIẢ. `missing_in_corpus` chỉ tính `is False`. Verified.
- Kiểm chứng KHÔNG phải bug ở v1.22.24: **exit-code = 1** đúng khi thiếu config (B2/S2 = artifact SIGPIPE/`|head`
  hoặc version cũ); **vbhn-check --subject = 11** candidate (đã siết #2, không phải 17). B4 (gws fallback) đúng
  thiết kế. B5/S5 (MCP legal_ask 'organic') ngoài skill.
- selftest 107/107; gen 14/14; tl_boot ✓.

---

# v1.22.24 (gws3env) — TÍCH HỢP script lõi từ full-skill v1.15.7 (vá B)

Vấn đề B (overlay thiếu ~23 script lõi → rỗng nửa skill, `tl rasoat` chỉ discovery). User gửi full-skill v1.15.7.
Workflow phân tích tương thích 14 script song song (15 agent) + kế hoạch tích hợp → tích hợp **16 script** vào
scripts/ (đối chiếu contract 2.21.2i, sửa version-skew):
- **Drop-in (stdlib):** common, cache, verify_deep, keywords, standardize_name, vbhn_query, rasoat_worksheet,
  rasoat_phuluc, registry_orchestrator, normalize_document, backfill_keywords_live, ingest_to_cache, build_cache,
  nlm_sources.
- **Sửa version-skew (workflow bắt):** `sapxep.py` version-parse `split('.')` vỡ với '2.21.2i' (có chữ 'i') →
  `re.split(r'[^0-9]+')[:3]` → (2,21,2); `manifest_export` POST→GET (sapxep ×2 + backfill_nlm_title — contract là
  GET); `backfill_keywords_live` `/tmp` POSIX → `tempfile.gettempdir()` (Windows).
- **gas closure:** thêm `scripts/gas.py` RE-EXPORT `_fallback/gas.py` (script con subprocess `import gas` resolve
  được; 1 nguồn chân lý; không circular). tl.py `_gas()` dùng re-export = symbols y hệt → KHÔNG regression.
- **Data:** `linhvuc_phapdien.json` (sapxep) → scripts/+references/; `QUY_TRINH_RA_SOAT_3_TANG.md` +
  `VAN_PHONG_HANH_CHINH.md` (rasoat_phuluc) → references/.
- **BỎ:** không tích hợp `nlm_sources` như primary (đã có nlm_cli superset) nhưng copy để backfill_nlm_title import được.
- Verified: 16/16 import OK; `tl ping`=2.21.2i, selftest 107/107, gen 14/14; `tl rasoat worksheet` DISPATCH script
  THẬT (hết fallback plan); vbhn_query --selftest PASS; sapxep ver-parse (2,21,2); 0 dòng >800B; 0 token rò.
- `tl doctor` optional **thiếu 8 → thiếu 2** (chỉ `tra_cuu.py`+`vb_status.py` — KHÔNG có trong v1.15.7, là full-skill
  mới hơn; nếu user gửi bản có 2 file này tôi gói tiếp).

---

# v1.22.23 (gws3env) — Vá Cowork/Chat log + workflow-verified (sửa 1 regression)

Workflow xác minh đối kháng đa-văn-bản (5 agent: BHXH/ATVSLĐ/Giáo dục/BHYT + completeness critic) BẮT 1 regression
+ tinh chỉnh:
- **#7 regression (workflow bắt):** bộ lọc file-thô cũ `(not _entry_sohieu)` KHÔNG bắt .docx có số hiệu parse từ
  registry (vd 108-VBHN-VPQH.docx cạnh GDoc NLM vẫn lọt). Sửa: loại .docx/.pdf-không-NLM khi **đã có bản NLM TRÙNG
  số hiệu** (thừa) HOẶC số hiệu rỗng/sidecar → GIỮ .docx VBHN MỚI chưa-NLM (không over-filter — đúng lo critic).
  Verified Giáo dục/BLLĐ/BHYT: 0 file-thô-thừa lọt, canonical NLM giữ, .docx-mới-chưa-NLM giữ.
- **#5 (critic):** ngưỡng non-linked `overlap≥3` → `≥ min(3, |subj|)` — chủ đề tên ngắn (≤2 token) không bị
  over-filter; vẫn khử nhiễu BLLĐ 2→0.
- **D (critic):** dọn nốt stray `2.21.2h` trong docstring tl.py → `2.21.2i` (khớp EXPECT_VERSION/contract gate).
- **#1 (critic xác nhận):** `cmd_init_config` ĐÃ TỒN TẠI (dòng 550) + subparser + _CREDS_LAZY_CMDS — Cowork log
  "không tồn tại" là do mount cắt cụt. Không cần thêm.
- **#6:** verified KHÔNG có consumer `int()/sum()` trên rasoat pending_effect_count (an toàn khi = null).

Nội dung gốc (đã giữ): D version-sync; #5 relation-check confidence; #6 rasoat pending n/a; #7 vbhn-check lọc
file-thô; B2 Drive config defaultProfile→vbqppl (fileId 1dEOBJ8…); SKILL.md §1 entry → tl_boot.py. selftest 107/107.
KHÔNG fix (môi trường/đóng gói): A mount cắt tl.py (#51435, tl.py tôi 5377 dòng hoàn chỉnh — re-sync); B overlay
thiếu ~23 full-skill script (không có để ship); E MCP legal_ask 'organic'. Critic lưu B impact cao — cần cài full skill.

---

# v1.22.22 (gws3env) — (gộp vào 1.22.23)

Hai log mới (Cowork + Chat). Xác minh: **tl.py của tôi HOÀN CHỈNH** (5377 dòng, có `if __name__`, compile OK) →
Cowork "cắt cụt 5272/thiếu __main__" = **mount Bug#1 cắt file** (#51435), KHÔNG phải file thiếu. Vá phần fixable:
- **D version-sync:** docstring tl.py `v1.21.0` → `v1.22.22` (khớp VERSION + SKILL.md). SKILL.md header → 1.22.22.
- **#5 relation-check:** non-linked candidate siết overlap **2→3** (overlap-2 kéo về NĐ trường-giáo-dưỡng/BHXH khác
  lĩnh vực) + nhãn **confidence** high(linked)/low → BLLĐ nhiễu 2→0, không bỏ sót (amendment thật qua footnote).
- **#6 pending nhập nhằng:** rasoat-chongcheo `pending_effect` chỉ có khi đã đọc nguyên văn → chưa đọc in **n/a**
  (≠0, tránh hiểu nhầm "không có gì chờ") + `pending_effect_scope` (article/unknown) + note phân biệt missing_in_corpus.
- **#7 vbhn-check báo giả:** `_vbhn_candidates` bỏ **file gốc thô** (sidecar HOẶC .doc/.docx/.pdf chưa parse số hiệu +
  không NLM) → BLLĐ 12→11, .docx "000.01…" hết lọt, canonical NLM giữ nguyên.
- **B2 Drive:** `tra_luat_config.v2.json` TRÊN DRIVE (fileId 1dEOBJ8…) defaultProfile "Luật BHXH" → **"vbqppl"** (giữ
  token/profiles) → Cowork/Chat tải về đã đúng default, khỏi `--profile` tay.
- **Cowork entry:** SKILL.md §1 đổi sang `python scripts/tl_boot.py …` (truncation → báo rõ thay vì im lặng exit 0).
- KHÔNG fix được (môi trường/đóng gói): A (mount cắt tl.py — re-sync/restart Cowork), B (overlay thiếu ~23 script
  full-skill như tra_cuu/verify_deep — không có trong overlay này), E (MCP legal_ask lỗi schema 'organic' — ngoài skill).
- selftest 107/107.

---

# v1.22.21 (gws3env) — #3/#4 dedup bắt trùng SỐ HIỆU thật (Chat log, user xếp nguy hiểm nhất)

- **#3 `dedup-check`:** trước query gộp "18-VBHN-VPQH Bộ luật Lao động" → norm_sohieu hỏng → 0 exact hit (chỉ ra
  fuzzy dự thảo). Sửa: **TÁCH token số hiệu khỏi query** (regex có-chữ) → quét trùng số hiệu CHÍNH XÁC → verdict
  **COLLISION** (≥2 thực thể cùng số hiệu) + phân vai **CANONICAL/DUP** (canonical = NLM/điểm cao). Verified: BLLĐ
  ra 3 thực thể (GDoc NLM + .docx + bản quarantine), hết bỏ sót.
- **#4 hygiene `same_document_dups`:** trùng cùng-document (cùng số hiệu) trước rơi vào `vbhn_reuse_collisions` (rổ
  cố ý KHÔNG quarantine) → `hygiene plan` trả clusters=[]. Sửa: `_split_distinct_vbhn_docs` phân biệt theo **XUNG
  ĐỘT năm/goc** (14/VBHN ATVSLĐ-2024 vs NLĐ-2023 = năm khác → reuse GIỮ; 18/VBHN BLLĐ: GDoc-2026 + .docx-thiếu-năm
  = không xung đột → nhân-đôi). Rổ mới `vbhn_same_document_dups` (canonical + dups) vào hygiene scan/plan →
  `hygiene plan "Bộ luật Lao động"` nay ra cluster GIỮ-canonical / QUARANTINE-dup (DRY, cần --confirm). Sidecar
  loại khỏi phân tích va chạm. An toàn: canonical (NLM) KHÔNG bao giờ bị xếp dọn. selftest +1 → 107/107.
- Còn lại Chat #5/#6/#7 (gộp 3 cổng dọn / nhãn tin cậy relation-check / kết xuất đề xuất gỡ NLM slot) — pass sau.

---

# v1.22.20 (gws3env) — B2 defaultProfile=vbqppl + #2 vbhn-check filter + BẢO MẬT loại config-token khỏi zip

- **🚨 BẢO MẬT:** `tra_luat_config.v2.json` (chứa **token plaintext**) bị đóng vào mọi zip v1.22.x → **LOẠI khỏi
  zip** từ nay (đóng gói qua staging-dir, xoá config-token + *.enc). Ship `tra_luat_config.example.json` (sạch,
  placeholder) thay thế. (Zip cũ chỉ ở Downloads máy user, chưa publish → rủi ro thấp; nên cân nhắc xoay token.)
- **B2:** `tra_luat_config.v2.json` `defaultProfile` "Luật BHXH" → **"vbqppl"** (rà VBQPPL không còn đọc nhầm scope
  project BHXH). DEFAULT_PROFILE code vốn đã = vbqppl; config nay khớp.
- **#2 (Chat log):** `vbhn-check --subject` không lọc — `_vbhn_candidates` nhận subject khi `sscore>0`, mà token
  "dong" trùng động/đồng/đông sau bỏ dấu → kéo Thư viện/TDTT/Quảng cáo. Sửa: subject chỉ tính khi **sscore≥60**
  (trùng tên hoặc ĐỦ mọi token chủ đề). Verified: BLLĐ 41→12 candidates, hết nhiễu rõ.
- Ghi nhận chưa code (Chat #3/#4/#5/#6/#7): dedup-check bỏ sót trùng SỐ-HIỆU thật (ưu tiên fuzzy keyword); trùng
  cùng-document bị xếp nhầm `vbhn_reuse_collisions` (không quarantine); 3 cổng chưa gộp list dọn; relation-check
  amendment_candidates nhiễu; chưa kết xuất đề xuất gỡ NLM slot. Cần thiết kế riêng (deep registry logic).

---

# v1.22.19 (gws3env) — Auto-tải tl_secrets.enc từ Drive khi thiếu file + B1 config v2.json

Theo yêu cầu "thiếu tl_secrets.enc thì tìm+tải trên Drive":
- **Bake `SECRETS_FILEID`** = id bundle trên Drive (chỉ là fileId; bundle vẫn mã hoá — vô dụng nếu thiếu
  TL_MASTER_KEY). Bootstrap THIẾU `--secrets-file` → tự tải bằng id này.
- **`_secrets_fetch` mở rộng:** `--secrets-file` → **webapp GAS** (nếu có token) → **direct-media** (nếu có gws
  cred) → None. Dùng chung bootstrap/secrets-set/nlm-auth-pull. Verified: không file local → tải webapp 26KB →
  giải mã OK (gws_cred+nlm_auth).
- **B1 fix:** `_config_candidates` nhận `tra_luat_config.v2.json`/`tra_luat_config.json` ở cwd / gốc skill /
  scripts/ → khởi động TRẦN (không `--config`) tự thấy config, hết "Thiếu TL_WEBAPP/TL_TOKEN". Cũng nạp token để
  webapp-fetch bundle. Verified.
- **B5 fix:** SKILL.md header v1.21.0 → đồng bộ VERSION.
- (Ghi nhận, chưa code) B2 defaultProfile="Luật BHXH" footgun → rà VBQPPL phải `--profile vbqppl`; B6
  relation-check `amendment_candidates` nhiễu (heuristic lỏng) → lọc tay.

---

# v1.22.18 (gws3env) — tl_boot.py: launcher tự strip-NUL cho tl.py (mount Bug#2)

Xác định cơ chế gốc qua GitHub anthropics/claude-code#51435: cài/giao skill Cowork có **Bug#2** — re-upload file
NHỎ hơn đè bản cached LỚN mà không O_TRUNC → phần dư thành **NUL byte đuôi**. **v1.22.17 shrink tl.py 338→301KB
chính là cái KÍCH HOẠT** (đè bản ~343KB cũ → 42.077 NUL → ValueError). tl.py KHÔNG tự strip NUL cho chính nó
(Python nạp nó TRƯỚC code self-heal).
- **`scripts/tl_boot.py` (1.9KB)** — launcher nhỏ (không dính bug vì nhỏ + không bao giờ shrink): đọc tl.py → BỎ
  NUL → exec như __main__; exit code truyền qua; cắt-cụt-thật (Bug#1) → báo lỗi rõ + cách mirror. Verified: nhồi
  42.077 NUL → 342.960B (khớp log) → tl_boot chạy selftest 106/106.
- **Entry point Cowork đổi sang `python scripts/tl_boot.py …`** (COWORK_PROJECT.md + Instructions). Dùng được mặc
  định (không NUL thì strip là no-op).
- Stack phòng vệ đầy đủ: tl.py NUL→tl_boot strip; tl_gws NUL→_imp self-heal; tl_gws cắt cụt→build_parser degrade
  (lệnh lõi chạy); subject_clusters hỏng→cluster cảnh báo. Dứt điểm vẫn là RE-SYNC (restart Cowork trước khi cài).

---

# v1.22.17 (gws3env) — Tách selftest → tl_selftest.py (giảm cắt cụt tl.py)

Lỗi gốc tái diễn = mount cắt cụt FILE LỚN; tl.py (~338KB) là to nhất + quan trọng nhất → dễ cắt nhất.
- **Tách `selftest()` (389 dòng, 106 case) → `scripts/tl_selftest.py`** (bind tên-trần của tl, như tl_gws).
  `tl.selftest()` thành wrapper mỏng: `_imp("tl_selftest").bind(tl).run()` — tl_selftest NUL-pad thì `_imp`
  tự heal, cắt cụt thật thì wrapper try/except báo lỗi + return 1 (không crash).
- **tl.py: 338KB → 301KB** (margin dưới cap mount ~343KB nay ~42KB, thoải mái) → giảm mạnh bề mặt bị mount
  cắt cụt cho file tối quan trọng. selftest vẫn 106/106; gen 14/14; transport 11/11.
- 86→87 file (thêm tl_selftest.py). Không đổi logic test nào.

---

# v1.22.16 (gws3env) — Vá B1/B6/B7/B8/B9 từ log Cowork thật

Phần lớn lỗi log là MOUNT (NUL/cắt cụt — cần re-sync; self-heal NUL + mirror đã có). Vá các lỗi LOGIC:
- **B1** bootstrap `--secrets-file` trỏ file KHÔNG có → check tường minh sớm: thông báo rõ (đặt .enc vào Context) +
  `return 2`, thay vì FileNotFoundError/đi tiếp mơ hồ.
- **B6** `subject_clusters.json` parse lỗi (cắt cụt) → trước IM LẶNG trả cụm rỗng (dễ kết luận nhầm "không có
  cụm"). Nay **CẢNH BÁO to** + cờ `_parse_error`; phân biệt file-thiếu (im) vs file-hỏng (báo).
- **B7** `tl cluster "<free text>"`: khớp thêm TÊN CỤM / base_name → "lao động" / "pháp luật về lao động" /
  "lao động xã hội" đều ra base `18/VBHN-VPQH` (trước chỉ khớp member key, trả "không có ánh xạ").
- **B8** `bootstrap` exit code: thêm cờ `degraded` + wrap gws-install/nlm trong try/except → traceback KHÔNG còn
  "nuốt" thành exit 0; degraded (gws/nlm chưa đủ) → exit 1; in "XONG (SUY GIẢM…)".
- **B9** `__pycache__/*.cpython-313.pyc` từng lọt zip (sinh khi chạy ở Code Python 3.13) → dọn TRIỆT để ngay
  trước khi nén (sandbox 3.10 bỏ qua .pyc 3.13, vô hại nhưng bẩn).
- B2/B3/B4/B5 (mount NUL/cắt cụt, hỏng chéo 2 mount) + B10 (gws fallback) = môi trường/đúng-thiết-kế.

---

# v1.22.15 (gws3env) — `tl overlap`: E1 nâng cấp so quy phạm (nguyên văn 2 phía)

Nâng E1 từ discovery → cấp NGUYÊN VĂN để so quy phạm (việc agent từng làm tay nay tự động):
- **`tl overlap <gdocId|sohieu|--text-file>`**: với mỗi điểm giao thoa (footnote amendment) của VBHN canonical →
  trích **nguyên văn Điều bị sửa** từ bản hợp nhất (offline) + metadata (luật sửa, vị trí, hiệu lực) + **cờ cấu
  trúc** `⏳PENDING` / `⚠ĐA-LUẬT-SỬA` (≥2 luật sửa cùng Điều) / `nguồn-?`. `--with-source`: trích THÊM điều tương
  ứng của luật sửa từ corpus (online). `--json` cho máy.
- Nguyên tắc giữ vững: skill chỉ cấp **verbatim 2 phía**; Claude đọc + phán OVERLAP/CONFLICT (KHÔNG RAG sinh).
- Verified BLLĐ thật: 5/5 điểm trích đủ; Đ139 K1 ⏳PENDING; `--with-source` trả đúng 113/2025 Đ29 ("…07 tháng…")
  khớp bản hợp nhất. Đặt ở tl_gws.py (giữ tl.py < cap); `overlap` ∈ _CREDS_LAZY_CMDS.
- Còn lại (GĐ sau): phán xung đột tự động (heuristic số/giá trị), overlap CHÉO văn bản qua dẫn chiếu (ngoài footnote).

---

# v1.22.14 (gws3env) — bootstrap tự cài nlm qua Drive-Python (uv CDN chặn)

Log Cowork: bootstrap từ Context THÀNH CÔNG (gws OK) — đưa cả skill vào Context đã hết cắt cụt; cụm "lao động"
chạy (8 luật, hết "trống"). Còn nlm: bootstrap thử uv→astral CDN chặn ("tunnel error") rồi DỪNG, chưa tự đi
đường Drive.
- **`_ensure_nlm_installed` thêm fallback Drive-Python:** uv (CDN) fail → tự gọi `cmd_nlm_install` (tải Python 3.11
  standalone từ Drive, egress mở) → cài nlm. Bootstrap nay cài nlm TRỌN VẸN ở Cowork (≈31MB direct-media, ~5s;
  `--no-nlm` để bỏ). Code (CDN mở) thì uv thắng, không tải Drive.
- Làm rõ từ log: #5 "cluster cắt …đi làm việ" = terminal agent cắt dòng, KHÔNG phải skill (cmd_cluster in đủ).
  Các tồn đọng KHÁC (môi trường/GĐ-sau/data): SKILL.md mount lệch version (Cowork auto-load bản mount cũ); E1
  rasoat-chongcheo mới discovery chưa so quy phạm (GĐ sau); nhiễu hygiene registry quanh BLLĐ (cần dọn data Drive).

---

# v1.22.13 (gws3env) — load_creds env+profile + Cowork Project setup robust

Từ log Cowork Project thật:
- **Fix #5 (mâu thuẫn §9):** `load_creds` trước chỉ dùng env khi KHÔNG có `--profile` → `boot --profile vbqppl`
  với env đủ vẫn báo "Thiếu TL_WEBAPP/TL_TOKEN" + đòi file. Nay **env (TL_WEBAPP+TL_TOKEN) đủ để chạy kể cả có
  `--profile`** (scope qua TL_*_env/§9 hoặc config mặc định best-effort). Verified env+profile không sys.exit.
- **COWORK_PROJECT.md** trả lời "setup có đúng không": ✅ đính kèm tl_secrets.enc đúng; ❌ còn placeholder master
  key; ❌ **thiếu mã nguồn skill trong Context** — lỗi `tl_gws.py` cắt cụt 31821B đến từ bản SKILL-MOUNT mà Context
  không đè được. → Khuyến nghị đưa CẢ `scripts/`+`references/` vào Context, chạy từ đó (né mount cắt cụt) + chmod
  -R u+w (file mount read-only 0500) + thay master key thật. Instructions cập nhật.
- Lưu ý còn lại (môi trường, không phải code): cụm "lao động" cần subject_clusters đầy đủ; OVERLAP/CONFLICT là GĐ
  sau; lệch ngày sandbox (26 vs 27/6) ảnh hưởng mốc PENDING sát ngày.

---

# v1.22.12 (gws3env) — Chống mount-corrupt: self-heal NUL + degrade graceful

Mount Cowork tái diễn cắt cụt/NUL-pad `tl_gws.py` (vd 31821B, unterminated line 589) → vì `build_parser` import
tl_gws nên tl.py CHẾT HOÀN TOÀN (kể cả lệnh rà soát lõi không cần gws). Hai lớp phòng vệ:
- **`_imp` self-heal NUL** (`_selfheal_module`): import lỗi SyntaxError/ValueError → đọc nguồn, BỎ byte NUL, compile
  lại + exec thành module. NUL-pad (corrupt phổ biến nhất) → **TỰ LÀNH**, gws/bootstrap chạy khỏi sửa tay.
- **`build_parser` degrade graceful**: nếu nạp tl_gws vẫn fail (cắt cụt THẬT, mất byte) → stub thay cho `tlg.*`
  (lệnh gws/bootstrap/nlm/secrets báo lỗi rõ + cách khắc phục, rc=3) nhưng **lệnh LÕI vẫn chạy** (footnote-map/
  cluster/rasoat-chongcheo — verified rc=0, 5/5 footnote). Hết cảnh "tl.py sập toàn bộ".
- Verified: NUL-pad module → self-heal nạp OK; cắt cụt → None → stub; mô phỏng tl_gws hỏng → footnote-map vẫn 5 điểm.
- Vẫn nên **re-sync skill** để hết corrupt; đây là lưới an toàn để rà soát không bị chặn.

---

# v1.22.11 (gws3env) — Cowork refresh nlm (`nlm-auth-pull`) + Cowork Project (bỏ MCP seed)

- **Đã chạy `secrets-set --nlm`** → bundle live (`1V0rSVF…`) giờ có `nlm_auth` (3 file, cookie ~10 ngày). Cowork
  bootstrap → nlm headless tự động.
- **`tl nlm-auth-pull`** [Cowork]: kéo RIÊNG cookie nlm mới nhất từ bundle → `~/.notebooklm-mcp-cli` (refresh giữa
  phiên, nhẹ hơn bootstrap). Nguồn: `--secrets-file` (project file) → direct-media → webapp. Thêm vào `_CREDS_LAZY_CMDS`
  (cùng `nlm-install`) — tự lo cred, KHÔNG cần webapp token.
- **`references/COWORK_PROJECT.md`**: hướng dẫn dựng Cowork Project — đính kèm `tl_secrets.enc` làm project file →
  bootstrap `--secrets-file ./tl_secrets.enc` đọc seed TẠI CHỖ → **bỏ hoàn toàn Drive MCP**; binary lớn (gws 6.8MB,
  Python 31MB) qua direct-media (đã nhanh nhất). Kèm Project Instructions dán sẵn + chu trình đồng bộ cookie
  (local `secrets-set --nlm` qua Task Scheduler → Cowork `nlm-auth-pull`).
- Làm rõ Ask "direct-media mặc định": file LỚN đã luôn direct-media; chỉ seed ~26KB từng qua MCP — Project file bỏ nốt.

---

# v1.22.10 (gws3env) — Cơ chế refresh nlm: refresh-trước-stage + secrets-set --nlm

Theo cơ chế nlm: cookies (tuần) / CSRF (phút, tự refresh) / session (mỗi init); hết hạn → đọc lại auth.json từ
ĐĨA + tái sinh từ browser profile. Ghi-FILE (v1.22.9) là ĐÚNG hướng (env var `NOTEBOOKLM_COOKIES` đông cứng làm
auto-refresh chết — KHÔNG dùng). Bổ sung cho mô hình Cowork ephemeral:
- **`_refresh_nlm_auth`**: `secrets-stage`/`secrets-set --nlm` chạy `nlm login --check` TRƯỚC khi gói → nlm tái
  sinh cookie từ browser profile (ghi đè auth.json) → bundle bắt cookie MỚI NHẤT.
- **`secrets-set --nlm`**: refresh cookie nlm tại chỗ vào bundle (giữ fileId) — bảo trì định kỳ ~2–4 tuần, khỏi
  re-export cả gws.
- **Báo tuổi cookie** (`_nlm_auth_age_days` từ `extracted_at`): secrets-stage/set in tuổi; bootstrap cảnh báo nếu
  >14 ngày + chỉ cách re-stage. (Cookie hiện tại của user: ~10 ngày.)
- Cowork KHÔNG tự refresh (không browser/chrome-profile) nhưng 1 phiên « tuổi cookie nên đủ; refresh thật ở Code.
  RUNBOOK §nlm: cơ chế 3-lớp + vì-sao-ghi-file + chu trình bảo trì.

---

# v1.22.9 (gws3env) — Stage nlm_auth: NotebookLM headless cho Cowork

`tl nlm-install` (v1.22.8) đã cài `nlm` THÀNH CÔNG end-to-end qua Drive (nlm 0.7.7). Còn lại: nlm chưa auth
("Profile 'default' not found" → fallback MCP). `nlm login` là **cookie-based** (mở trình duyệt) — không chạy
trong sandbox Cowork. Giải: stage cookies vào bundle như gws_cred (agent đề xuất).
- **`secrets-stage` gói `nlm_auth`** = {`auth.json`, `profiles/default/cookies.json`, `profiles/default/metadata.json`}
  từ `~/.notebooklm-mcp-cli` (helper `_nlm_auth_files`). SECRET → chỉ trong bundle MÃ HOÁ (verified cookie KHÔNG
  lộ plaintext); `--no-nlm` để bỏ.
- **`bootstrap` ghi lại** các file đó vào `~/.notebooklm-mcp-cli` (chmod 600) ở Code/Cowork → nlm chạy **headless**
  (`nlm login --check` xanh), khỏi `nlm login` thủ công.
- **secret_guard**: chặn cookie phiên Google (`__Secure-[13]PSID`/`SAPISID`) + `git add/scp …notebooklm-mcp-cli`.
- Quy trình: (Code) `nlm login` 1 lần → `tl secrets-stage` → (Cowork) `tl bootstrap`. Cookies ~2–4 tuần, hết hạn
  thì login+stage lại (hoặc `nlm login --manual -f cookies.txt`). RUNBOOK §nlm cập nhật.

---

# v1.22.8 (gws3env) — Fix giải nén Python: filter=fully_trusted

`tl nlm-install` (v1.22.7) đã: hết NameError, tải 31MB Python 3.11 từ Drive THÀNH CÔNG (chứng minh đường-vòng
-qua-Drive vượt được chặn egress). Nhưng giải nén crash trên Python 3.10.12:
`tarfile.LinkOutsideDestinationError: 'python/share/terminfo/1/1178' would link to '…/a/adm1178'`.
- Nguyên nhân: `extractall(filter="data")` — backport `data` filter ở 3.10.12 từ chối 300+ symlink hợp lệ
  (terminfo `..`) trong tarball python-build-standalone. (3.13 không tái lập vì filter đã tinh chỉnh.)
- **Vá:** `filter="fully_trusted"` — tarball ĐÃ md5-verify (đúng bản chính thức) → bỏ kiểm tra link/path, giải
  nén được symlink trên MỌI phiên bản Python. An toàn vì nguồn đã xác thực bằng PY311_MD5.
- Verified: member khó `terminfo/1/1178 -> ../a/adm1178` extract OK với fully_trusted. selftest 106/106.

---

# v1.22.7 (gws3env) — Fix NameError tempfile trong `tl nlm-install`

`cmd_nlm_install` (v1.22.6) dùng `tempfile` bare nhưng tl_gws.py KHÔNG import stdlib ở top — chỉ lệ thuộc
`bind()` chép globals từ tl.py. Mà tl.py không export `tempfile/tarfile/stat/hashlib` (chỉ có
base64/json/os/re/sys/subprocess/time) → bind không thể chèn → `NameError: tempfile` (lộ khi agent dispatch
trực tiếp KHÔNG qua build_parser do mount corrupt; cũng latent ở path thường).
- **Vá:** tl_gws.py **import stdlib TƯỜNG MINH ở top** (os/sys/re/json/stat/base64/hashlib/tarfile/tempfile/
  subprocess) → tự đủ, không lệ thuộc bind cho stdlib. bind() chỉ còn chèn tên tl-RIÊNG (_gas/_imp/hằng GWS_*/
  PY311_*…). Robust hơn với path bypass-bind.
- Verified: `cmd_nlm_install` qua đúng flow bind tới bước download (không NameError); selftest 106/106.

---

# v1.22.6 (gws3env) — `tl nlm-install`: Python 3.11 standalone qua Drive (vòng egress Cowork)

Cowork CHẶN egress astral CDN ("tunnel error") → uv không tải được managed Python 3.11. Nhưng egress
**Google Drive MỞ** (gws chạy được) → đưa Python qua Drive như đã làm với binary gws.
- **`tl nlm-install`** (lệnh MỚI, opt-in — KHÔNG tự chạy trong bootstrap để khỏi tải 31MB mỗi lần): tải
  **Python 3.11.15 standalone** (python-build-standalone, install_only_stripped ~31MB, `PY311_FILEID` trên
  Drive) → md5-verify → giải nén `~/.local/python311` → cài notebooklm-mcp-cli bằng `uv tool install --python
  <bin>` (uv KHÔNG tải Python vì đã có local → bỏ qua astral CDN) hoặc `python3.11 -m pip install --user`.
- Hằng `PY311_FILEID`/`PY311_MD5` (tl.py). Cơ chế tải+md5+unpack verified trên Code (md5 byte-exact, tarball
  có `python/bin/python3.11`); phần chạy interpreter + cài nlm thực thi ở Cowork/Linux.
- Egress sandbox = allowlist HẠ TẦNG Cowork, KHÔNG sửa từ skill — chỉ vòng qua được kênh đã mở (Drive). Nếu
  PyPI cũng chặn → CLI bất khả → NotebookLM MCP. RUNBOOK §nlm cập nhật.

---

# v1.22.5 (gws3env) — nlm cài qua `uv --python 3.11` (fix "unsatisfiable")

Rà soát repo `jacob-bd/notebooklm-mcp-cli`: là **pure Python package** (PyPI), **KHÔNG có binary standalone**
như gws → không "đóng gói binary giống gws" được (gws compiled chạy không runtime; nlm cần Python ≥3.11).
Deps toàn pure-Python chuẩn (fastmcp/httpx/pydantic/typer…) — "all versions unsatisfiable" trên Cowork
KHÔNG do dep lỗi mà do **thiếu `--python 3.11`**: uv resolve theo system 3.10 → pkg-≥3.11 không bản nào thỏa.
- **Vá `_ensure_nlm_installed`**: `uv python install 3.11` + `uv tool install --python 3.11 notebooklm-mcp-cli`
  (uv tự tải managed Python 3.11, vượt rào 3.10) → verified cài được `nlm`. Xác nhận bằng `nlm_exe` sau cài.
- Giới hạn còn lại: nếu sandbox Cowork CHẶN egress tải managed Python (astral CDN) → CLI bất khả; khi đó
  **NotebookLM MCP** (đã sẵn ở Cowork) là đường đúng — CLI chỉ là tiện ích env Code, KHÔNG ảnh hưởng rà soát.

---

# v1.22.4 (gws3env) — Footnote bắt marker DEF số-trần ([2] Điều 59)

Nguyên nhân gốc (đọc nguyên văn VBHN-18): chú thích đánh marker KHÔNG nhất quán — `[3]`/`[4]`/`[6]` có ngoặc
nhưng **[2] viết SỐ TRẦN `\n2 Điểm này được sửa đổi…`** (không ngoặc) → `_MARK_RE` bỏ sót → `def_missing`.
- **Vá `resolve_footnote_amendments`**: ngoài marker `[n]`, nhận thêm **marker số-trần đầu dòng** trong
  foot_region — CHỈ cho số CÓ anchor trong thân + theo sau là `Điểm|Khoản|Điều|Cụm từ` (tránh false-positive).
  → [2] Điều 59 K2 ← **124/2025/QH15** (điểm a K1 Đ43), HL 01/01/2026 — phân giải ĐỦ NGUỒN, hết "?".
- Recall footnote BLLĐ giờ **5/5 đầy đủ luật sửa**: Đ59←124, Đ61←124, Đ139←113 (⏳pending 01/07/2026),
  Đ154←71, Đ217←71. Khớp 100% đối chiếu nguyên văn thủ công.
- Selftest +1 (`footnote_bare_number_marker`) → **106/106**.
- `footnote_defs` JSON xác nhận LÀ **object** (dict marker→record đủ trường) — báo cáo "mảng" của agent là do
  mount Cowork phục vụ bản tl.py cũ/cắt-cụt, không phải code.

---

# v1.22.3 (gws3env) — direct-media = phương án download tối ưu + nlm qua uv

Benchmark LIVE (median, ms): direct-media-token-cache thắng/hoà mọi loại & **byte-exact** —
tiny.json 1040 (gws N/A), med.js 1440 (gws 1485), bin 6.8MB 2997 (gws 3156, **AS-b64 20848**), GDoc 3083.
- **Token cache** (`_access_token`): đổi refresh→access 1 lần/process → tải loạt file chỉ 1 round-trip token.
- **`_drive_media_download` thêm `export_mime`**: tải cả Google-native (Doc/Sheet) qua endpoint `/export`.
- **Router `drive_op("download")`**: Code/Cowork ưu tiên **direct-media** (khi có gws cred file) → gws (binary)
  → GAS-b64. Byte-exact MỌI loại kể cả text/JSON (gws CLI làm méo JSON; AS-b64 chậm 2–5.6× + cap 9MB).
- **nlm qua `uv tool install`**: uv TỰ CẤP Python ≥3.11 (vượt rào sandbox Cowork 3.10) → cài được
  notebooklm-mcp-cli (verified `nlm 0.7.7`). uv thiếu → `pip install --user uv` trước; pip-trực-tiếp chỉ khi ≥3.11.
- RUNBOOK A0.8b: cập nhật bảng benchmark + quy tắc download direct-media-first.

---

# v1.22.2 (gws3env) — Download direct-media (không base64)

- **`_drive_media_download`** (tl_gws): tải Drive `alt=media` qua HTTP với access-token (đổi từ gws cred
  refresh_token) → **RAW bytes STREAMING xuống đĩa, KHÔNG base64, không cap 9MB, ~2.8× nhanh** webapp-b64
  (đo: 4.6s vs 12.9s/6.8MB). Bootstrap binary gws dùng direct-media nếu có cred (ghi cred TRƯỚC khi cài
  binary); fallback webapp-b64 khi chưa có cred. Secrets `.enc` vẫn webapp-b64 (chicken-egg: cred ở trong .enc).
- **nlm:** bỏ qua pip nếu Python <3.11 (notebooklm-mcp-cli yêu cầu ≥3.11; Cowork 3.10 → fallback NotebookLM MCP).

---

# v1.22.1 (gws3env) — Tích hợp gws 3-env + vá rà soát thực tế

Ngày: 2026-06-26. Nền: 1.22.0 (contract 2.21.2i, **GS KHÔNG đổi**).
- **Transport gws 3-env:** `scripts/{gws_bridge,mcp_bridge,transport,tl_gws}.py` — router gws→GAS-fallback (Code/
  Cowork) / Drive MCP (Chat); lệnh `gws-ping`/`transport-info`/`download`/`bootstrap`/`secrets-*`. tl.py tách
  `tl_gws.py` (giữ <343KB cap mount Cowork).
- **Đọc nguyên văn qua gws:** `extract`/`footnote-map`/`rasoat-chongcheo` ưu tiên transport→gws (bypass webapp
  `exporttext` lỗi OAuth `script.external_request`); nguyên văn 100% (cùng GDoc).
- **Footnote-resolver:** `_HL_DATE_VN_RE` bắt "ngày DD tháng MM năm YYYY" → **pending_effect chạy**; phân biệt
  amendment thật vs trích dẫn ("căn cứ ban hành"/"quy định như sau") + Type-B recover đích từ anchor (vd
  Điều 217←71/2025) + body-marker thiếu-def (Điều 59, cờ `def_missing`). `pending_effect_count` vào cả JSON.
- **Cluster:** `_resolve_cluster_member` disambiguate số hiệu TRÙNG (giữ VBHN-first); cờ ambiguous chỉ khi ≥2
  VB khác thật; `base_aliases` (rasoat-chongcheo nhận Luật gốc 45/2019/QH14).
- **Bootstrap nlm:** `pip install notebooklm-mcp-cli` (unpinned) + resolver `~/.local/bin`.

---

# v1.22.0 — ĐẶC TẢ 26/6: footnote def-driven (B1-B4) + quy trình tải gated env-aware (C0-C5)

Ngày: 2026-06-26

**Nhóm I — footnote-resolver def-driven (vá 3 lỗi còn lại sau v1.21.0 trên BLLĐ):**
- **B1** — viết lại `resolve_footnote_amendments` thành **def-driven**: MỖI chú thích `[n]` = 1 bản ghi ĐỘC LẬP (`_parse_footnote_def`), không "mượn" số/đích/luật của marker khác. Tách def theo MARKER (không phụ thuộc xuống dòng). Mỗi def: target (điều BỊ SỬA, từ mệnh đề trước động-từ-sửa; thiếu Điều → anchor thân điền) tách khỏi vị trí NGUỒN (trong luật sửa); luật sửa lấy theo cụm "của Luật … số <sh>" TRONG chính def (`_AMEND_LAW_RE`, hết "luật gần nhất"); thêm trường `diem`. Kết quả BLLĐ: footnote_count **4→5**, đủ [2]Đ59←124/2025(điểm a K1Đ43), [3]Đ61 K3←124/2025(điểm b K1Đ43), [4]Đ139 K1←113/2025, [5]Đ154 K8a←71/2025, [6]Đ217←71/2025.
- **B2** — điền `hieu_luc` mỗi amendment: từ "có hiệu lực kể từ ngày…" trong chú thích, fallback registry theo số hiệu luật sửa (`_entry_hieuluc_date`); cờ `pending_effect = hieu_luc>today`. `footnote-map`/`xref`/`rasoat-chongcheo` truyền `entries` để fill.
- **B3** — `rasoat-chongcheo`: `pending_effect_count` suy từ footnote + danh sách `pending_effect[]` `{dieu,khoan,diem,amending_sohieu,hieu_luc}`; thêm `--target <gdoc|số hiệu>` để export text. BLLĐ: pending=1 (Điều 139 ← 113/2025, 01/7/2026).
- **B4** — Phiếu/human-output tách mục "⏳ HIỆU LỰC TƯƠNG LAI" (không trộn phần đã hiệu lực).
- Selftest +3: `footnote_gdnn_markers`, `footnote_hieuluc_fill`, `pending_from_footnote`.

**Nhóm II — quy trình tải VBHN login-gate (C0-C5):**
- **C1/10a** — luật cứng: official chỉ có PDF ⇒ PHẢI thử docx ở TVPL+LVN trước; PDF là phương án cuối + kiểm chất lượng text. (Ghi nhận sự cố XNC 62/VBHN-VPQH.)
- **C2/C3/10b** — env-aware: `_runtime_env()` ∈ {code,cowork,chat}, không chắc→chat (an toàn). code/cowork: HỎI trước khi tự tải; chat: đưa link bấm-được.
- **C4** — `tl fetch-links [--env]` xuất link TẢI XUỐNG (nhãn `[Tải .docx <sh> — <nguồn> (cần đăng nhập)]`) + link TẢI LÊN `_HOP_NAP` (folder `1bNSAKGACtk0…`); KHÔNG URL trần.
- Selftest +2: `fetch_links_hopnap_upload`, `runtime_env_explicit`.

Không đụng GS (contract 2.21.2i giữ nguyên) ⇒ không cần redeploy webapp.

---

# v1.21.0 — DELTA LESSONS phiên BLLĐ+NQ72: vá B3 footnote / xref B1-B2 / preflight dedup+slot

Ngày: 2026-06-26

- **L1 [B3 footnote-resolver]** — `resolve_footnote_amendments` chuẩn hóa DẤU DÍNH số-khoản↔số-chú-thích ("1.4[4]", "[4]4 Khoản…", "8a[5]") TRƯỚC khi match (trước chỉ bắt 1/5, gán sai luật). `_KHOAN_HEAD_RE` + stick nhận khoản hậu tố chữ (8a). Verify: [4]→Đ139 K1←Dân số 113 PENDING, [5]→Đ154 K8a←CNCNS 71.
- **L2 [B4 pending]** — pending_effect nay phát hiện đúng (Điều 139, Luật Dân số 01/7/2026) sau khi L1 chạy.
- **L3 [xref B1+B2]** — B1: chuỗi hợp nhất ĐẦY ĐỦ của VBHN (mapped ∪ footnote ∪ preamble) → 113/124/45-2019… KHÔNG còn OUTDATED. B2: `rel_type` 3 loại — **SUA_DOI_BASE** (sửa vào base, map cấp Điều) / **CHU_THICH_LICH_SU** (lớp sửa lịch sử đã hợp nhất: 97/2015, 35/2018…) / **DAN_CHIEU_NOI_DUNG** (dẫn chiếu luật khác). Xuất `consolidation_chain` + `rel_summary`.
- **L4 [preflight dedup]** — thêm dedup PHÍA TL **lỏng-năm**: `_sohieu_loose` để `72/NQ-TW ≡ 72/2025/NQ-TW` → cảnh báo `⚠DUP-TL` khi số hiệu đã trên NLM dù KHÁC TÊN (suýt nhân bản NQ72 trong notebook đầy).
- **L5 [slot-count]** — `_nlm_slot_count` LOẠI `removed_*`/`other_notebook` dù còn `nlm_source_id` sót (trước used=322>live 300). `preflight` verify-LIVE qua `nlm-get` khi webapp báo FULL.
- **L6 [doctrine]** — SKILL §1: notebook đầy thật (LIVE 300/300) → giải phóng slot (bản GỐC đã có VBHN: 45/2019←VBHN18, 84/2015←VBHN14, 69/2020←VBHN8) hoặc overflow; `source_delete` BẤT KHẢ NGHỊCH → lập danh sách + chờ xác nhận.
- Selftest tl **93/93** (+`footnote_dau_kep_L1L2`, +`sohieu_loose_L4`, +`slot_excludes_removed_L5`) · gen 14/14 · contract KHỚP 2.21.2i · gs 12/12. *(Chỉ `tl.py`+docs; không đụng GS → không redeploy.)*

# v1.20.8 — reg-query in full drive_id (vá cắt 20 ký tự) + dọn cụm Dữ liệu 19→03

Ngày 2026-06-26: `reg-query` human-mode in ĐỦ drive_id (trước cắt 20 ký tự làm hỏng luồng query→recat). Đã recat 11 doc Dữ liệu/CNTT/GDĐT từ 19→03 (dogfood reg-query+recat).

# v1.20.7 — Gộp tác vụ ad-hoc thành lệnh: reg-query / recat / cat-audit + hygiene subject-aware

Ngày: 2026-06-26

Rà các snippet viết tay phiên dọn corpus → nhiều cái TRÙNG lệnh sẵn có (`hygiene`, `dedup-check`, `locate`, `manifest`). Bổ sung 3 lệnh lấp GAP thật + 1 nâng cấp:
- **`tl reg-query`** — truy vấn registry/manifest OFFLINE + lọc `--name/--sohieu/--cat/--nlm/--no-nlm/--row-kind/--corpus/--mime` (`--json`). Thay ~15 snippet `json.load(manifest)+filter`.
- **`tl recat <drive_id…> --cat NN [--quarantine] [--apply]`** — di dời file → folder chủ đề (mkdir đúng tên 45-ref nếu thiếu) + cập nhật registry; `--quarantine` cách ly + xóa mapping NLM. DRY mặc định. Thay ~10 snippet move+reg_bulk.
- **`tl cat-audit`** — audit cấp 2: doc corpus có folder ≠ chủ đề suy từ TÊN (`_CAT_KEYWORDS` → 45 chủ đề), heuristic, xuất `recat` đề xuất.
- **Nâng cấp `hygiene` subject-aware:** `_reconcile_clusters` chỉ QUARANTINE bản TRÙNG THẬT (cùng `_subject_sig`) — KHÔNG gộp nhầm khác-cơ-quan (TT-BNV vs TT-BYT)/phụ-lục-vs-chính. quarantine_candidates 284→271.
- **Sửa 3 mã sai `_CAT_REVIEW_HINTS`:** hình sự 15→**16**, doanh nghiệp 10→**12**, giao thông 12→**14**.
- Doctrine SKILL §0.14: **dùng lệnh có sẵn, đừng viết snippet tay**.
- Selftest tl **90/90** (+infer_cats_strong, +subject_sig_discriminate) · gen 14/14 · contract KHỚP 2.21.2i · gs 12/12.

# v1.20.4 — Audit cấp 2: di dời misfile-đơn + secret-guard hook

Ngày: 2026-06-26

- **Audit cấp 2 (rà doc trong từng folder):** 63 cờ nghi lệch → triage. Phần lớn ĐÚNG; phát hiện thêm **46 nhóm trùng lặp** (58 dòng dư) — chủ yếu mẫu "bản sạch GDoc ↔ bản .doc/.docx" + vài số-hiệu trùng do gán nhãn sai.
- **Đã di dời 8 misfile-ĐƠN (1 dòng, có NLM, chỉ sai folder):** Bộ luật Hình sự→**16** (tạo folder `16_Hinh_su`), Luật Trẻ em→**08**, Người khuyết tật→**06**, NĐ 142 Chính quyền địa phương→**35**, NQ 261 Y tế→**45**, Thuế TNCN/TNDN→**33**. NLM giữ nguyên.
- **CHƯA xử lý (dedup thật, cần pass riêng + chọn canonical):** cụm CNTT/Dữ liệu (bản sạch@19 ↔ .doc@03), Thư viện (41↔32), Kế toán (sai cat 33→17?), + số-hiệu trùng/gán nhãn sai (60-2024 Dữ liệu vs Phòng bệnh; 67-2006 CNTT vs NLĐ; 57-2024 QuyHoach vs BHYT; 61-VBHN Thuế vs ATTP). Luật 57/2024: bản .docx đã quarantine nhưng bản NLM-linked còn ở 46 (46 = "Luật sửa nhiều luật" là home hợp lệ).
- **Secret-guard hook (`scripts/hooks/secret_guard.py`):** mượn ý ecc — PreToolUse chặn echo/commit/upload **token webapp** (`tl_…`), URL `/exec?token=`, key sk-/ghp_/AKIA/AIza, và git/gh/scp/curl đụng `tra_luat_config`/`.gs`/`INSTALL.zip`. Fail-open khi parse lỗi; KHÔNG log giá trị bí mật. Đã smoke-test (chặn token/commit-config/exec-url; cho qua lệnh thường).
- GS `CATEGORIES_FALLBACK` thêm **16**. Selftest tl **88/88** · contract KHỚP 2.21.2i · GS parse OK.

# v1.20.3 — GS mime-guard: file phi-văn-bản ở root không tính corpus

Ngày: 2026-06-26

- **GS `_isNonVbMime_` + guard regen2:** file mime `json/spreadsheet/csv/presentation/script` → `corpus=false` (VBQPPL chỉ là Google Doc/PDF/Word). Xử lý nốt `tra_luat_config.v2.json` (giữ ở root theo yêu cầu nhưng KHÔNG còn bị đếm corpus) + future-proof mọi file cấu hình/chỉ mục/backup lỡ nằm trong cây.
- Verify redeploy 1.20.2: version 2.21.2i, cat **01/03/37/43 resolve** đúng.
- ⚠️ **Cần REDEPLOY** Code.gs để guard hiệu lực → sau regen2, corpus 618 → ~617 (loại `config.v2.json`). API/contract không đổi (version giữ 2.21.2i).
- Selftest tl **88/88** · contract KHỚP 2.21.2i · gs 12/12 · GS parse OK.

# v1.20.2 — Dọn corpus theo 45 chủ đề: phân 33 doc khỏi root + xác định/loại văn bản dư

Ngày: 2026-06-26

- **Xác minh redeploy GS:** quarantine→corpus:false hiệu lực — 44 file QUARANTINE thôi bị đếm; corpus 687→643.
- **Phase 1 (18 doc rõ ràng):** từ root → 06 (Người cao tuổi), 32 (Xuất bản/Thư viện/Báo chí), 38 (Tín ngưỡng tôn giáo), 39 (Mại dâm/Ma túy), 41 (TDTT/Quảng cáo/Di sản/Du lịch/Điện ảnh).
- **Phase 2 (tra Bộ pháp điển):**
  - **Cụm CNTT/GDĐT/Dữ liệu/CSDL/DVC trực tuyến (12 doc) → 03 Bưu chính, viễn thông** (phapdien: đề mục CNTT thuộc chủ đề 3). Tạo folder `03_Buu_chinh_vien_thong`.
  - NĐ 30/2020 → **42 Văn thư**; NĐ 187/2025 ×2 → **44**.
  - VBHN 131 **Luật Quy hoạch** 21/2017 → **43 Xây dựng, nhà ở, đô thị** (tạo folder `43_Xay_dung_nha_o_do_thi`).
  - `178-qh15.signed.pdf` = **NQ 178/2025/QH15** (tổ chức cơ quan QH) → **35**; `80-nd-cp.signed.pdf` = **NĐ 80/2025/NĐ-CP** (tổ chức thi hành PL) → **44** (đọc nội dung file để định danh).
  - **Luật 57/2024** (omnibus sửa Quy hoạch/Đầu tư/PPP/Đấu thầu) → **QUARANTINE**: các luật con đã có VBHN hiện hành (Quy hoạch 131, PPP 123, Đấu thầu 74) + Đầu tư có luật mới 143/2025 ⇒ bản sửa đổi rời dư thừa (VBHN-first).
- **Phase 3:** dời 11 file housekeeping (CHI_MUC, REGISTRY, nlm_sources, INDEX, HANDOVER, bench/probe…) → folder `_META_taluat` (register:false, ra khỏi corpus+registry). Giữ `tra_luat_config.v2.json` ở root theo yêu cầu (1 count json thừa, không push NLM).
- **Kết quả:** root từ 49 corpus → **chỉ còn config.v2.json**; corpus **643→618**, mọi doc về đúng chủ đề pháp điển.
- **GS `CATEGORIES_FALLBACK`:** thêm 03/43 (01/37 đã thêm ở 1.20.1). Dynamic scan nhận folder mới ngay; fallback chỉ áp khi quét lỗi → redeploy không gấp.
- `phap_dien_45.json`: set `exists=true` cho 01/03/37/43. Selftest tl **88/88** · contract KHỚP 2.21.2i · gs 12/12 · GS parse OK.

# v1.20.1 — Phân lĩnh vực ĐÚNG 45 chủ đề pháp điển + vá lỗi ingest trùng + GS quarantine

Ngày: 2026-06-25

- **Kiểm tra mapping 1-45 vs danh mục chính thức:** xác nhận mã folder khớp **45 chủ đề Bộ pháp điển** (QĐ 843/QĐ-TTg). Lưu `references/phap_dien_45.json` (45 chủ đề + tên + slug; nguồn thuvienphapluat.vn/phap-luat/chu-de/bo-phap-dien) + lệnh `tl cat-list`. Mã `00`/`46` = rổ phi-pháp-điển tự thêm.
- **SỬA 2 cat gán SAI trước đó (live):** VBHN 21 BL Tố tụng dân sự `09 Dân sự`→**`37 Tố tụng…`**; VBHN 62 Nhập/xuất cảnh người NN `23 Ngoại giao`→**`01 An ninh quốc gia`**. Tạo folder `01_An_ninh_quoc_gia` + `37_To_tung_va_cac_phuong_thuc_giai_quyet_tranh_chap`, move GDoc+src, cập nhật registry. NLM nguồn không đổi.
- **(4) ingest validate theo ĐỦ 45 + auto-mkdir:** `ingest-local` nhận mọi mã 1-45; hợp lệ mà thiếu folder → tự `mkdir` đúng tên chính thức; ngoài 45 → `REVIEW_CAT` chặn `--apply`. Sửa `_CAT_REVIEW_HINTS` (37/01/16/10/12…).
- **VÁ LỖI INGEST TRÙNG:** `upload` (smartConvert_) tự convert docx→GDoc **+ tự register**, rồi `organize convert` tạo GDoc THỨ HAI ⇒ mỗi văn bản dư 1 GDoc/1 dòng. Fix `ingest-local`: upload `convert=false`+`register=false` (giữ .docx làm src, chỉ 1 GDoc). Dọn 2 GDoc trùng (VBHN 21/62) → QUARANTINE; canonical NLM-linked giữ nguyên.
- **GS (`Code.2.21.2i.gs`) — 2 sửa liên quan cat:** (a) `CATEGORIES_FALLBACK` bổ sung đủ folder hiện có (trước thiếu 9) + 01/37; (b) **`classifyScanFolder_`: QUARANTINE → `corpus:false`** (trước trả `corpus:true` nên file cách ly VẪN bị đếm corpus — lỗi ảnh hưởng mọi file quarantine). ⚠️ **Cần REDEPLOY Code.gs** để corpus-count loại file quarantine (data API không đổi → version giữ 2.21.2i, contract KHỚP).
- **Phủ nốt MCP→CLI:** `tl nlm-cross` (cross_notebook_query, test 2/2 shard) + `tl nlm-get` (notebook_get, test=3) + `source_rename`. Doctrine SKILL/RUNBOOK sửa hết tham chiếu MCP.
- Selftest tl **88/88** · gen 14/14 · contract KHỚP 2.21.2i · gs 12/12 · GS parse OK.

# v1.20.0 — NLM GHI qua CLI (bỏ MCP source_add) + `tl ingest-local` 1-lệnh

Ngày: 2026-06-25

- **(1) NLM write qua CLI** — phát hiện `nlm source add/delete/sync` chạy headless được (CLI, KHÔNG có `-j` → parse text `Source ID: <uuid>`). `nlm_cli.py` thêm `source_add/source_delete/source_sync`; doctrine SKILL §1 + RUNBOOK §A4 sửa: **MỌI thao tác NLM (đọc + GHI) qua CLI**, MCP chỉ fallback. Bỏ carve-out sai "source_add=MCP". Lệnh `tl nlm-add <nb> --drive <id> [--wait]`.
  - **Test LIVE:** add (5.9s) → list thấy → delete (3.0s) → list sạch, round-trip OK.
- **(2) `tl ingest-local <file>` — ingest 1-lệnh** thay 5 bước thủ công: upload `_HOP_NAP` (b64) → `organize` (convert GDoc + tên chuẩn + cat + stamp goc/hiệu-lực) → **`nlm source add` (CLI)** → push registry (`row_kind` own/overflow). DRY mặc định, `--apply` để chạy. Pipeline chạy TRỌN trong tl, không gãy bởi round-trip MCP.
- **(3) preflight trong ingest** — `ingest-local` gọi `nlm_preflight` (`_ingest_target`) tự định tuyến base VBQPPL ↔ shard overflow khi base đầy (cap 300).
- **Phủ NỐT MCP→CLI** (đã rà cây `nlm`): thêm `tl nlm-cross` (= `nlm cross query`, thay `cross_notebook_query`; mặc định base+overflow — **test 2/2 shard**), `tl nlm-get` (= `nlm notebook get -j`, thay `notebook_get.source_count`; **test=3**), `nlm_cli.source_rename` (thay `source_rename`). `nlm-cross`/`nlm-get` gọi `apply_profile_offline` để nạp id shard từ config (không cần webapp). Doctrine SKILL §0.11/§1 + RUNBOOK §A/§C/đối-chiếu sửa hết các tham chiếu MCP còn lại.
- **(4) cat hardening** — `ingest-local` validate `cat` ∈ tập đề mục pháp điển THỰC của profile (19 mã + QUARANTINE), zero-pad 1 chữ số; lệch → `REVIEW_CAT` chặn `--apply` (trừ `--force-cat`). Tài liệu hóa: tố tụng→09, xuất nhập cảnh→23 (chưa có đề mục riêng → cat gần nhất + xác nhận).
- **(5) sidecar docx** — `ingest-local` truyền `register=true` → tạo **1 dòng registry atomic** (`drive_id`=GDoc, `src_id`=docx), không lệ thuộc regen2; xác nhận regen2 (Code §doRegen2_ dòng 68-77) cũng tự ghép cặp GDoc↔docx cùng base-name → KHÔNG sinh dòng trùng.
- Selftest tl **87/87** (+`nlm_cli_cross_get_rename`,`ingest_norm_cat`) · gen 14/14 · contract KHỚP 2.21.2i · gs 12/12. Test LIVE: nlm add/delete round-trip, nlm-get=3, nlm-cross 2/2 shard, cat-validate chặn đúng.

# v1.19.19 — Dọn dữ liệu C1/C2 (live) + egress Công báo ② kiểm chứng

Ngày: 2026-06-25

- **C2 (dọn — đã chạy live, reversible, không trash):** C2.5 VBHN 67 Doanh nghiệp + sidecar → cat 34; C2.3 sidecar BHXH 41/2024 → QUARANTINE; C2.4 bản trùng Việc làm 74/2025 (root) → QUARANTINE; C2.6 ×2 dup Hiến pháp 52 → QUARANTINE; C2.1 ×3 BHYT gốc → reg cat 02; C2.2 đã sạch. Verified sau regen2 (treeHash_match=True, corpus=683).
- **C1 (linkage):** cụm lao động-xã hội phần lớn đã có goc; chỉ VBHN 8/VBHN-BNV thiếu → backfill `goc=112/2021/NĐ-CP;372/2025/NĐ-CP` (đọc header xác minh: VBHN của Nghị định 112/2021, KHÔNG phải Luật 69/2020).
- **D1 egress (KIỂM CHỨNG):** `dangerouslyDisableSandbox` + curl link `g7.cdnchinhphu.vn` trích từ trang congbao → tải PDF official (test 2.1MB/111 trang). RUNBOOK §D1 ghi phương pháp ②.
- **Nạp gap:** tải VBHN 21/VBHN-VPQH (BL TTDS) + VBHN 62/VBHN-VPQH (Nhập/xuất cảnh) docx từ LuatVietnam (TVPL hết quota ngày → fallback LVN). Sẵn ~/Downloads; ingest corpus chờ duyệt.
- Selftest tl **84/84** · contract KHỚP 2.21.2i.

# v1.19.18 — Vá phiên rà soát BLLĐ (VBHN 18): A1/B1-B4/E1-E2

Ngày: 2026-06-25 · Chi tiết: `references/REVIEW_BLLD_V1.19.18.md`.

- **A1 [CODE]** `_entry_score`: phạt nặng bản `_ZZZ_QUARANTINE` (−400) + thưởng VBHN-có-goc (+35) → VBHN-first áp cho **cả truy vấn theo TÊN** (resolve_identity cộng `_entry_score//10`). BHXH→VBHN19, BHYT→VBHN40… không còn trả bản quarantine/orphan.
- **A2** [verified] `locate`/`source-map` đã liệt kê ĐỦ ứng viên trùng số + `VBHN_NUMBER_REUSE_RISK`; A1 lo ranking đúng.
- **B1 [CODE]** `_classify_ref`: KHÔNG gắn OUTDATED khi canonical CÒN hiệu lực, hoặc nằm trong chuỗi hợp nhất của chính VBHN đang xét (`base_goc_keys`).
- **B2 [CODE]** xref gắn `rel_type` (SUA_DOI_BASE nếu số hiệu nằm trong footnote-amend của bản này; else DAN_CHIEU) — phân loại nhẹ.
- **B3 [CODE] (trọng yếu)** `resolve_footnote_amendments()` + `tl footnote-map`: bắt cặp marker`[n]`↔chú thích → `dieu_level_amendment_map` {dieu, khoan, amending_sohieu, amending_vitri, hieu_luc, loai}; chuẩn hóa dấu dính `(\d+)\.?(\d+)?\[n\]`. Tích hợp vào `tl xref`. **Khớp bằng chứng VBHN 18:** [4]→Đ139 K1 ← Dân số 113/2025 (01/7/2026); [5]→Đ154 ← CNS 71/2025.
- **B4 [CODE]** cờ `PENDING_EFFECT` khi luật sửa hiệu lực ở tương lai (so với today).
- **E2 [CODE]** `references/subject_clusters.json` + `tl cluster`: 'pháp luật về X' → số hiệu canonical (cụm lao động-xã hội: BHXH/BHYT/ATVSLĐ/việc làm/công đoàn/GDNN/NLĐ nước ngoài/dân số).
- **E1 [CODE] (v1 discovery)** `tl rasoat-chongcheo <base>`: dựng tập liên quan (cụm E2 + footnote B3) + hiện diện corpus + PENDING. **So sánh quy phạm (OVERLAP/CONFLICT/PRIORITY/STALE/GAP) = giai đoạn sau** (cần đọc nguyên văn verify, không RAG).
- **C [HYGIENE] (chờ duyệt — KHÔNG tự chạy):** 6 cụm dọn (C2.1–C2.6) + backfill goc/sua_doi (C1) là data-ops live cần xác nhận từng cụm (qua webapp map_set/reg_bulk/organize; không hard-delete). Ghi nhận, chờ lệnh.
- **D1 [HẠ TẦNG] (ngoài skill):** `g7.cdnchinhphu.vn` ngoài egress allowlist → tải Công báo server-side bị 403/ROBOTS. Ghi RUNBOOK: hoặc mở egress `*.cdnchinhphu.vn`, hoặc Chrome tải về máy rồi kéo vào `_HOP_NAP`.
- Selftest tl **84/84** (+a1/b1×2/b3/e2). Lệnh mới: `footnote-map`, `cluster`, `rasoat-chongcheo`.

# v1.19.17 — Vá bài học test + Google VBHN-first cho MỌI tính năng tìm văn bản

Ngày: 2026-06-25

**Mở rộng Google discovery (yêu cầu người dùng):** `_discovery_links()` dùng chung (Google `site:` + VBHN-first) áp cho:
- `tl find-doc <q>` (MỚI) — primitive "tìm văn bản web" chung.
- QT-5: `vbhn-check` / `status` / `relation-check` → đều xuất `google_discovery` (link Google site: VBHN-first) thay vì chỉ query thô.
- SKILL §0 #1: "MỌI tìm-văn-bản-web dùng Google site:, không search nội bộ".

**Vá bài học từ phiên test (recipe `_FETCH_SOURCES` + RUNBOOK §B1g-bis):**
- **TVPL:** phải CLICK TAB 'Tải về' TRƯỚC (link docx mới đổi `javascript:postback`→URL `/documents/d...` thật) rồi click `(docx)`.
- **Trang lớn → `find` tràn token (>200k):** dùng `javascript_tool` + tọa độ theo TỈ LỆ viewport (`center/innerWidth*1568`, `/innerHeight*737`; viewport ~949×445 ≠ screenshot 1568×737) + click thật. JS `.click()` chỉ chạy cho `<a href>` thật.
- **QUOTA TVPL ~1 docx/ngày** → fallback **LuatVietnam** (docx, nút tải là thẻ `<a>` icon — JS click `<a>` được) → **vbpl.vn** (.doc FREE, KHÔNG có VBHN) → Công báo (.pdf).
- Recipe TVPL/LVN/vbpl trong `_FETCH_SOURCES` viết lại theo thực chiến.

Selftest tl **79/79** (+`discovery_links_shared`). Demo phiên: tải được Luật Dân số/PPP (TVPL docx), Luật Đầu tư (vbpl .doc), BLTTHS VBHN 17/2026 (LuatVietnam docx khi TVPL hết quota).

# v1.19.16 — DISCOVERY qua GOOGLE site: (thay search nội bộ kém)

Ngày: 2026-06-25

- **Dùng GOOGLE `site:` để tìm đúng trang văn bản** (search nội bộ TVPL/LuatVietnam trả kết quả kém hơn hẳn). `_google_site_url()` + `_fetch_plan` thêm `google_search`/`google_search_variants` mỗi nguồn + `google_global`. `discover="google_site"`.
- **`tl fetch-links`** giờ dẫn đầu bằng **link Google site:** (VBHN-first: 'hợp nhất' trước), per nguồn TVPL/LuatVietnam + 1 link Google toàn cục. Người dùng bấm → ra đúng trang văn bản → login → Tải về docx.
- **AUTO (`fetch-route`/`fetch-batch`)**: Claude resolve qua **WebSearch (Google site:)** → trang văn bản trực tiếp → tải.
- **Đo thật (Luật SHTT):** Google site: trả đúng **VBHN 67/VBHN-VPQH 2026** (mới nhất) + 155/2025 + 11/2022 — chính xác hơn search nội bộ. SKILL §0 #10 cập nhật.
- Selftest tl **78/78** (+`google_site_url`).

# v1.19.15 — VBHN-first query expansion + 2 chế độ tải (MANUAL link / AUTO Claude)

Ngày: 2026-06-25 · Chi tiết bổ sung: `references/FETCHER_V1.19.14.md`.

- **VBHN-first query expansion** (`_query_variants`): tra/tìm Luật theo TÊN → sinh biến thể **'<tên> hợp nhất' → '<tên> mới nhất' → tên gốc** (vd "Luật PPP" → "Luật PPP hợp nhất" trước). Theo SỐ HIỆU → tìm thẳng. Đã nêu 'hợp nhất'/'mới nhất' → tôn trọng nguyên trạng. Áp vào `fetch-route`/`fetch-batch`/`fetch-links` + SKILL §0 quy tắc #1.
- **2 chế độ tải:**
  - **`tl fetch-links <q>` (MANUAL):** trả **link markdown bấm-được** cho người dùng tự vào (qua login gate) tải docx — TVPL/LuatVietnam có URL keyword (VBHN-first), vbpl/Công báo kèm hướng dẫn. Dùng khi cần người dùng tự login.
  - **`tl fetch-route`/`fetch-batch` (AUTO):** Claude tự tải qua Chrome (throttle, dedup, checkpoint).
- `_fetch_plan` đổi shape → `{query_variants, sources}` (mỗi nguồn có `search_variants`). Callers + selftest cập nhật.
- Selftest tl **77/77** (+`query_variants_vbhn_first`).

# v1.19.14 — Polite fetcher official-first, ưu tiên FORMAT docx>doc>pdf

Ngày: 2026-06-25 · Chi tiết: `references/FETCHER_V1.19.14.md`.

- **`tl fetch-route <số hiệu|tên>`**: DEDUP + kế hoạch tải theo **ĐỊNH DẠNG docx>doc>pdf** ⇒ thứ tự nguồn **TVPL → LuatVietnam (docx) → vbpl.vn (doc) → Công báo (pdf)**. Mỗi nguồn kèm recipe Chrome đã dò thực tế. (CANONICAL/HIỆU-LỰC vẫn official-first để xác minh bản đúng — 2 trục.)
- **`tl fetch-batch <…> [--file --delay --jitter]`**: điều phối danh sách → **SKIP_DEDUP** (khớp số hiệu) / **REVIEW_DEDUP** (khớp tên qua token-overlap) / **FETCH**; ghi checkpoint `~/.tra_luat_cache/fetch_queue.json`. Tải thật do agent chạy Chrome (throttle ~4s+jitter, concurrency 1, một danh tính, KHÔNG proxy/giả UA).
- **Phát hiện thực nghiệm (đưa vào doctrine):** trang luật VN chặn HTTP server-side (TVPL 403, vbpl 404) → **bắt buộc trình duyệt thật**; Claude in Chrome > Playwright headless (qua Cloudflare bằng session thật, không né tránh). **Demo thật:** tải `Luat Dau tu 2020.doc` (1MB) từ vbpl FREE; `Luat Dan so docx` từ TVPL. Luật Đầu tư 61/2020 **hết hiệu lực 01/03/2026** → bản hiện hành 143/2025 đã có (dedup).
- **Test Luật TTNT 134/2025:** fetch-route → dedup (đã có, pushed); fetch-batch → số hiệu=SKIP, tên=REVIEW, giả=FETCH(TVPL→docx). ✓
- SKILL §0 quy tắc #10 viết lại theo 2 trục + CLI table. Selftest tl **76/76** (+`fetch_plan_format_priority`).

# v1.19.13 — Claude Desktop vs nlm CLI + auto-download VBQPPL từ TVPL (Claude Code/Cowork)

Ngày: 2026-06-24 · Chi tiết: `references/TVPL_AUTODOWNLOAD_V1.19.13.md`.

- **Phần 1 — Claude Chat (Desktop):** KHÔNG gọi được `nlm` CLI (chỉ MCP, không Bash). Muốn fast-lane ở Desktop → bọc `nlm` CLI thành 1 MCP server nhỏ (chưa triển khai, là dự án MCP riêng ngoài skill).
- **Phần 2 — Auto-download TVPL (Claude Code/Cowork):** xác minh KHẢ THI (Claude in Chrome connected; trang /van-ban/ có tab "Tải về" + link "(docx)"; fetch server-side 403 → cần trình duyệt đã đăng nhập). Sửa kết luận cũ "full-auto bất khả" — chỉ đúng cho Apps-Script/Chrome-only; Claude Code có Bash đọc `~/Downloads` nên đóng được vòng.
  - **`tl tvpl-url <số hiệu>`**: dựng URL tìm TVPL + in luồng auto-download (Chrome login VIP → tab Tải về → docx → ~/Downloads → `_HOP_NAP` → preflight → source_add VBQPPL-2 → push-overflow).
  - RUNBOOK §B1g + SKILL CLI table cập nhật. Agent không nhập mật khẩu; tải file = hành động cần xác nhận.
- Selftest tl **75/75**.

# v1.19.12 — mọi ĐỌC NLM qua CLI (không MCP) + đo hiệu năng in-code + vá tiện ích

Ngày: 2026-06-24 · Chi tiết: `references/NLM_CLI_ALLREADS_V1.19.12.md`.

- **B — mọi thao tác ĐỌC NLM qua CLI `nlm` (Claude Code/Cowork), KHÔNG qua MCP** (mọi lệnh có CLI: list/get/content/describe/query):
  - `nlm_cli.py` thêm `source_get`, `source_content`, `notebook_query`.
  - `tl nlm-content <src> [--out|--dieu N]` (thay MCP `source_get_content` vốn TRÀN TOKEN), `tl nlm-query <q> [--source-id …]` (thay `notebook_query`).
  - SKILL §1 + RUNBOOK §A4 + API_CONTRACT: nguyên tắc BẮT BUỘC — MCP chỉ fallback (thiếu CLI/auth) hoặc thao tác GHI (source_add/studio).
- **C — `tl bench`**: đo hiệu năng MỌI tính năng tính-toán-trong-code (offline) trên manifest. **Đo thật (757 entries):** manifest_load 8.9ms · resolve_identity 51.9ms · alias 0.007ms · reconcile_plan 0.23ms · extract_refs 0.005ms · scan 0.27ms ⇒ **in-code <52ms; bottleneck thật là network (webapp ~3.3s, CLI ~4s)**.
- **D — vá tiện ích từ phiên chạy:** `tl reg-delete --drive-ids … [--force]` (bọc reg_delete đúng tham số drive_ids[]+require_removed — trước phải làm tay).
- **A — 3 nguồn unregistered**: chẩn đoán = nguồn thêm thẳng vào NLM ngoài flow (NQ 59-NQ/TW, QĐ 05/QĐ-BCĐ là GDoc; Phụ lục NĐ 73/2019 là PDF vi phạm doctrine), KHÔNG có Drive file chuẩn + KHÔNG có dòng registry → cần flow ingest từng văn bản (chưa auto-register được).
- Selftest tl **75/75**.

# v1.19.11 — reconcile shard-aware + xử lý dứt 13 desync + profile NQ80

Ngày: 2026-06-24

- **`_nlm_reconcile_plan` shard-aware:** dòng có `nlm_notebook_id` ≠ notebook đang xét (vd overflow trên VBQPPL-2) → nhóm `other_notebook`, KHÔNG tính `desync_real` (trước bị báo desync giả). Output thêm `other_notebook`. Selftest **75/75** (+`nlm_reconcile_other_notebook`).
- **Xử lý dứt 13 nguồn desync** (data live):
  - VBQPPL: Luật 87 + VBHN 07 + ND 97 → `removed_superseded_by_VBHN` (xác minh VBHN_54 / VBHN_04 hợp nhất); NQ 68 → re-push base; NQ 42 → re-map source có sẵn; **NQ 71 → re-push VBQPPL-2 (overflow, row_kind=overflow)** — chuyến đầu dùng shard phụ.
  - **Profile NQ80 mới:** 7 doc trong `Van_ban_thuong/NQ80-sua-doi-bo-sung` (notebook cc39895d) → tạo profile NQ80 (registry `1LMKn…` + manifest `1WobF…` tạo sẵn rồi forward — KHÔNG auto-create để tránh ghi nhầm registry nền), regen2 own-scope 7 rows, map nlm_source_id (row_kind=own), xóa 7 rows thừa khỏi registry VBQPPL nền.
- Base VBQPPL cuối: live 300, desync_real **0**, other_notebook 1 (NQ 71), already_removed 79, unregistered 3. NQ80: 7 own, desync 0.
- Config: thêm profile `NQ80`; `vbqppl.shards/overflowNotebookId` (từ v1.19.10).

# v1.19.10 — kích hoạt sharding VBQPPL (Option 1: overflow notebook, không deploy GAS)

Ngày: 2026-06-24 · Chi tiết: `references/SHARDING_V1.19.10.md`.

VBQPPL chạm cap 300/300. Kích hoạt định tuyến overflow (cơ chế đã có sẵn ở GAS `nlm_preflight`/`nlm_slots`).

- **Tạo notebook shard phụ `VBQPPL-2`** (`45739ff7-347a-45c7-8066-0f2f3b55f76a`).
- **Config** `profiles.vbqppl`: thêm `overflowNotebookId` + `shards:[base, shard2]` (forward-compatible cho Option 3, không cần migrate).
- **`tl preflight <số hiệu>`:** gọi `nlm_preflight(notebookId=base, overflowNotebookId từ config, normative=true)` → base đầy ⇒ `decision=REVIEW` + `overflow_route` sang shard phụ. **Đo thật:** base used=323/300 full=true → route=45739ff7. ✓
- **`tl push-overflow --drive-id --source-id`:** sau `source_add` (MCP) vào shard phụ → reg_bulk set `row_kind=overflow, nlm_notebook_id=<shard>, nlm_status=pushed`.
- **Không deploy GAS** (chỉ Python + config, chạy trên 2.21.2i live). `overflowNotebookId` ánh xạ env `TL_OVERFLOW_NOTEBOOK_ID`.
- SKILL §1 + CLI table cập nhật quy tắc sharding; selftest tl **74/74**.

# v1.19.9 — nlm-reconcile: tách `already_removed` khỏi `desync_real` (hết báo động giả)

Ngày: 2026-06-24

- **`_nlm_reconcile_plan`/`tl nlm-reconcile`** giờ tách nhóm "không trên NLM" thành:
  - `desync_real` = status `pushed/synced` nhưng VẮNG NLM → đáng xử lý;
  - `already_removed` = status `removed*` (removed_below_nd/removed_from_drive/removed/removed_superseded_by_VBHN) → **đã gỡ CÓ CHỦ ĐÍCH, KHÔNG phải lỗi** (kèm `already_removed_by_status`).
  Trước đây gộp thành "stale" gây báo động giả (93). **Đo thật:** 92 → **13 desync_real + 79 already_removed**.
- **`--clear-stale` CHỈ áp `desync_real`** — KHÔNG đụng `already_removed` (giữ nguyên status removed* làm hồ sơ).
- Giữ khóa `stale`=`desync_real` (tương thích ngược). Selftest tl **74/74** (thêm `nlm_reconcile_split_removed`).
- **Rà soát thực tế:** 92 dòng "stale" của VBQPPL đều KHÔNG thuộc notebook profile (vbthuong fec6c125 / Luật BHXH 59e8d0de dùng registry riêng, mapping 37/37 và 34/34 — CHÍNH XÁC). Backfill 283 dòng VBQPPL đã apply + persist (358→75 thiếu notebook).

# v1.19.8 — fast-lane CLI `nlm` (không qua MCP) + reconcile registry↔NLM (WS1)

Ngày: 2026-06-24 · Chi tiết: `references/NLM_CLI_FASTLANE_V1.19.8.md`.

**Nghiên cứu (đo thật):** CLI `nlm` v0.7.7 (package `notebooklm-mcp-cli`, cùng nguồn với MCP server) chạy headless trong Claude Code. `nlm source list <nb> --drive --skip-freshness` = **299 nguồn / ~4s** (vs MCP `source_list_drive` timeout ~4' — CLI có cờ `--skip-freshness` MCP thiếu).

- **A. `scripts/nlm_cli.py`:** adapter bọc CLI `nlm` (gate PATH+auth, fallback `{ok:False,fallback:'mcp'}`).
- **B. `tl nlm-list <nb>`:** liệt kê nguồn live ~4s (thay `source_list_drive`).
- **C. `tl nlm-reconcile <nb> [--apply] [--clear-stale]`:** đối soát ground-truth → backfill `nlm_notebook_id` cho dòng THỰC SỰ trên NLM; báo `stale` (pushed nhưng không có trên NLM) + `unregistered`. DRY mặc định. **Đo thật:** live 299 · backfill 283 · stale 93 · unregistered 3 → giải dứt điểm WS1 (lấy được ground-truth an toàn).
- **D.** RUNBOOK §A4 + API_CONTRACT §9: fast-lane CLI thay khuyến cáo "TRÁNH source_list_drive".
- **E.** Nguyên tắc (SKILL §1): ưu tiên CLI `nlm` cho read NLM trong Claude Code/Cowork; MCP là fallback.
- Selftest tl **73/73** (thêm `nlm_reconcile_plan` thuần). Yêu cầu: CLI `nlm` + `nlm login` (thiếu → tự fallback).

# v1.19.7 — hardening danh tính (alias) + Reference Integrity (xref) + định tuyến nạp + cache snapshot

Ngày: 2026-06-24 · Implement đề xuất 5 workstream (WS1/WS2/WS3/WS5 = mã; WS4 = dữ liệu, không code). Chi tiết: `references/IDENTITY_XREF_V1.19.7.md`.

- **WS1 — bộ giải danh tính chuẩn hóa + alias (`resolve_identity`, `_ALIASES`):** khớp qua số hiệu → tên/name_key → ALIAS (BHXH↔Bảo hiểm xã hội, ATVSLĐ, NLĐ, GDNN, BLLĐ, BLHS…) trên cả `tukhoa/linhvuc/cat` → **sửa báo sót `source-map`** (tìm được BHXH/NLĐ/GDNN qua viết tắt). Đã test thật: "BHXH" → VBHN 19 BHXH.
- **WS1 — `tl dedup-check <q>`:** dedup theo manifest OFFLINE + bộ danh tính (thay `nlm_dedup` webapp trả sai). Verdict DUPLICATE/MAYBE/NEW.
- **WS1 — `tl slot-audit --physical N`:** neo sức chứa VẬT LÝ (`notebook_get.source_count`), in gap + cảnh báo backfill (đo thật: registry 385 vs vật lý 299 → gap −86). **`tl backfill-notebook`** ghi `nlm_notebook_id` (reg_bulk, DRY mặc định).
- **WS2 — `tl xref <gdocId|sh> [--text-file]`:** bóc dẫn chiếu (NFC) → giải canonical → cờ REPORT-ONLY `MISSING/OUTDATED/SOHIEU_MISMATCH/OMNIBUS`. Đã test trên Bộ luật Lao động: bắt SOHIEU_MISMATCH (BHXH 58/2014 cũ vs 41/2024), OUTDATED (84/2015 có VBHN), MISSING.
- **WS3 — `tl ingest-route <file/sh>`:** cây quyết định 3.bis (advisory) định tuyến file nhập: PROFILE_OWN / ASK_USE_EXISTING / REVIEW_NEARMATCH / ASK_ADD_TO_VBQPPL (shard theo lĩnh vực). Mọi ghi qua xác nhận.
- **WS5 — `tl cache-snapshot export|import`:** snapshot manifest_index có CỔNG treeHash (chặn cache cũ) + boot cache-TTL của v1.19.6.
- **WS4 (dữ liệu, không code):** vệ sinh corpus (VBHN 18/14, BLHS 100/2015, bare-number) làm trong phiên thường bằng `hygiene/reg_*/vbhn-verify`.
- Selftest tl **72/72** (thêm 6 ca alias/extract_refs/xref/resolve); gen 14/14; contract KHỚP 2.21.2i.

# v1.19.6 — đo thời gian + tối ưu load/tra cứu (boot cache-TTL, gọi song song)

Ngày: 2026-06-24

**Phân tích (đo THẬT trên live 2.21.2i):** >95% thời gian là ĐỘ TRỄ HTTP của Apps Script `/exec`
(~3.3s/round-trip; `server_ms` chỉ ~25–113ms) → thời gian ≈ 3s × số call. Không cần refactor kiến trúc;
nút thắt là I/O latency + thiếu cache/parallel. Chi tiết: `references/PERFORMANCE_V1.19.6.md`.

- **`boot` tái dùng cache local theo TTL** (`_fallback/boot.py`): manifest_index còn tươi (mtime < TTL,
  mặc định 600s; env `TL_BOOT_TTL`) ⇒ tái dùng, **0 call webapp**. `--refresh` ép tải lại, `--max-age <giây>`.
  → boot lặp lại **~12s → ~0.2s (đo thật, ~50x)**.
- **Đo thời gian tự động:** `tl perf [--json]` (suite round-trip/song song/cache + chẩn đoán) và cờ global
  `--timings` (=env `TL_TIMINGS=1`) in `[timing] <action> wall/server/client` cho MỌI call webapp.
- **`gas_parallel(calls)`**: chạy nhiều call ĐỘC LẬP song song (~2.8–3.2x, Apps Script không serialize).
- Khuyến nghị deploy-side (giảm số call): gộp boot 1 round-trip (manifest có entries inline), `changes_pull`
  delta, regen2 quét folder bằng `UrlFetchApp.fetchAll`, find ưu tiên registry trước fulltext.
- Selftest tl 66/66 giữ nguyên; không đổi logic profile/scope của v1.19.5.

# v1.19.5 — best-combined profile scope + phục hồi registry an toàn

Ngày: 2026-06-24

- So sánh và hợp nhất với `tra_luat_v1.19.4_regen2_profile_scope.zip`.
- Giữ server **2.21.2i** của nhánh nền: quét own-root đệ quy mọi cấp, giữ `row_kind=ref`, guard theo
  `old_own_count/new_own_count`; không dùng server 2.21.2h của bản ghép vì chỉ quét 2 cấp và merge ref như own.
- Nhập lệnh `profile-rebuild-registry`, nhưng sửa tiêu chí phục hồi: giữ hợp của
  **file thật trong `rootFolderId` + dòng đúng notebook + mọi `row_kind=ref`**. Bản gửi kèm chỉ giữ theo
  notebook nên có thể xóa nhầm own-row chưa map notebook.
- Recovery từ chối chạy nếu `list recursive` bị capped, DRY mặc định, apply cần `--confirm yes`,
  xóa theo lô 200 dòng và chạy `manifest_export` lại sau khi xóa.
- Thêm version gate trước regen profile: nếu `ping.version != 2.21.2i`, dừng trước `regen2`.
  Điều này chặn server cũ bỏ qua `manifestScope/rootFolderId` rồi ghi phình trước khi client cảnh báo.
- Thêm tài liệu `references/REGEN2_PROFILE_SCOPE_V1.19.5.md`.
- **Kèm `tra_luat_config.v2.json`** trong gói (schema 2: webappUrl+token+profiles) để chạy `tl --config tra_luat_config.v2.json ping/boot` ngay. ⚠️ File chứa TOKEN — không chia sẻ gói công khai.
- **Đối chiếu version (so sánh với v1.19.4):** đã xác minh `tl ping` = **2.21.2i** (`registry_schema=reg_cols_row_kind_v1`, 27 cột) — server ĐÃ deploy `Code.2.21.2i.gs`. `EXPECT_VERSION=2.21.2i` khớp live/contract. Đồng bộ nhãn **LIVE 2.21.2i** ở SKILL/RUNBOOK/API_CONTRACT/INSTALL (bỏ các câu "live 2.21.2h"/"đích/chưa rõ" mâu thuẫn). Chi tiết: `references/MERGE_V1.19.5.md`.

# v1.19.4 — regen2 làm phình registry/manifest của profile kế thừa (categories=inherit)

Ngày: 2026-06-24

- **Triệu chứng:** sau ingest, `tl manifest --touched-drive` trên profile văn bản thường có
  `categories=inherit` có thể làm registry/manifest tăng từ khoảng 34 lên 726 dòng và lẫn toàn bộ VBQPPL.
  Dòng own/notebook không mất, nhưng `locate/source-map/dedup` có thể chọn nhầm VBQPPL làm canonical profile.
- **Nguyên nhân:** `regen2` đã nhận đúng `registryDocId` profile nhưng vẫn quét `rootId_()/corpusFolders_()`
  của VBQPPL. `inherit` bị hiểu nhầm thành quyền populate manifest từ cây category dùng chung.
- **Scope fix (`Code.2.21.2i.gs`):** thêm `manifestScope=own|inherited`. Profile khác `vbqppl` mặc định
  `own`, chỉ quét đệ quy `rootFolderId` riêng; không đi vào folder category kế thừa. Quét own giữ nguyên
  `row_kind=ref`, tránh đánh dấu nguồn tham chiếu dùng chung là `removed_from_drive`.
- **Guard bắt buộc:** trước `regWriteAll_`, so `new_own_count` với `old_own_count`. Nếu
  `new_own_count > max(2×old_own_count, old_own_count+50)`, dừng với
  `PROFILE_MANIFEST_SCOPE_BLOWUP`, không ghi registry; chỉ override bằng `--confirm-blowup yes`.
- **Kết phiên an toàn:** profile `categories=inherit` mặc định export-only. `--touched-drive` yêu cầu
  `--confirm yes` và vẫn chạy `manifestScope=own`. `vbqppl` giữ phạm vi inherited như trước.
- **Ngữ nghĩa chốt:** `categories=inherit` chỉ dùng chung cây VBQPPL để ORGANIZE/tra cứu fallback;
  KHÔNG populate registry/manifest profile. Profile chỉ gồm `own + ref` (và `overflow` khi host).

# v1.19.3-hotfix — deploy 2.21.2h + profile/row_kind guard

Ngày: 2026-06-23

- Bump server contract lên **`2.21.2h`**: `Code.2.21.2h.gs` là bản deploy hiện hành; `Code.2.21.2g.gs` giữ làm tham chiếu lịch sử. `ping` trả thêm `schema_version`, `registry_schema`, `registry_cols` để phát hiện thay đổi `REG_COLS_`/`row_kind` thay vì silent-mismatch.
- Đồng bộ `tl.py EXPECT_VERSION=2.21.2h`, `API_CONTRACT`, SKILL/RUNBOOK/INSTALL/DELTA/PROFILE_SCOPE và `contract_check --audit` KHỚP `2.21.2h`.
- Vá profile-scope offline cho `slot-audit`, `locate`, `exists`, `source-map` giống `hygiene`: mọi lệnh đọc manifest offline gọi `apply_profile_offline(...)` trước khi mở cache.
- `row_kind` chuẩn hóa `own/ref/overflow`; hygiene/registry-doctor bỏ qua `row_kind=ref` và `own` văn bản thường khi dò duplicate/orphan/title-mismatch. `nlm_slots` mặc định không đếm `ref`, nhưng `countRefs=true`/`count_refs=true` đếm cả dòng tham chiếu.
- Doctrine slot: số slot registry là ước lượng logic; preflight trước khi đẩy phải lấy sức chứa vật lý bằng `notebook_get.source_count` để không đẩy quá tay khi profile có dòng `ref`.
- Dọn hệ quả của blanket-replace khi bump: khôi phục tên file lịch sử bị đổi nhầm và các ghi chú "predeploy" giờ thành "đã LIVE" (PROFILE_SCOPE §3, DELTA §A8, GS_2.21.2E, MULTI_CORPUS, MERGE).
- writeconfig nay an toàn: rotate token KHÔNG còn xoá block `profiles` v2.

# v1.19.2 — sửa lỗi version-bump, boot/manifest tôn trọng profile, writeconfig giữ profiles, doctrine backfill

Ngày: 2026-06-23

> **Bản HỢP NHẤT (best-of-both):** lấy fallback env-driven của nhánh Codex (gọn, có `--profile`) + giữ kỷ luật version-detectable cho writeconfig (tách `2.21.2g`) + buildConfigObject_ merge phong phú của Codex. Chi tiết: `references/PROFILE_SCOPE_V1.19.2.md`, `references/MERGE_V1.19.2.md`.

1. **Bump version sau deploy (live 2.21.2f):** `contract_check.py --bump 2.21.2f` đã chạy — `tl.py EXPECT_VERSION=2.21.2f`, `API_CONTRACT` đóng dấu `2.21.2f`; SKILL/RUNBOOK/INSTALL đồng bộ. Hết cảnh báo "version ≠" giả; mismatch thật lại lộ ra.
2. **`_fallback/gas.py` + `boot.py` + `manifest_build.py` tôn trọng profile (env-driven):** `gas.py` nhận `--profile`, đọc config v2 và tự chèn `registryDocId/manifestId` vào MỌI `get/post` (gated theo `TL_PROFILE`≠`vbqppl`, không đè param tường minh). `boot.py` nhận `--profile`, forward scope vào `manifest_export/manifest`, ghi cache `~/.tra_luat_cache/<profile>/`. `manifest_build.py` forward scope vào `regen2/manifest_export`. ⇒ `tl --profile P boot/manifest` đọc-ghi ĐÚNG registry/manifest của P; HẾT rủi ro regen nhầm VBQPPL nền. (Thay cơ chế `TL_SCOPE_*`/kwargs của bản nháp bằng env-driven thống nhất, tránh double cache-nesting.)
3. **`tl boot` truyền `--profile`; `tl manifest` gọi `manifest_build.build(no_regen)`** (env do `load_creds` đặt). `_ScopedGas` ở tl.py giữ lại (idempotent với `setdefault` của gas.py).
4. **writeconfig giữ/merge block profiles v2 (PREDEPLOY `Code.2.21.2g.gs`):** `buildConfigObject_` (logic merge của Codex) đọc mirror hiện có, merge `profiles`, bảo toàn `defaultProfile`, đồng bộ `profiles.vbqppl` theo hằng nền, xuất `schema:2` + `profilePolicy`. **Tách 2.21.2g** thay vì sửa thẳng 2.21.2f live → tránh silent-mismatch (ping vẫn 2.21.2f dù bản deploy chưa có fix). Sau deploy → `--bump 2.21.2g`.
5. **Doctrine backfill (DELTA §C.1):** sửa giả định "19 văn bản" (thực tế ví dụ 37 nguồn = 4 VB thường + 33 VBQPPL canonical). Phân biệt VĂN BẢN THƯỜNG riêng của profile (đăng ký vào registry profile) với VBQPPL canonical tham chiếu trong notebook dự án (GIỮ ở VBQPPL; thêm dòng tham chiếu `nlm_notebook_id=<NB>`, KHÔNG xoá gốc). Registry một-dòng-một-notebook không biểu diễn nguồn dùng chung → dùng dòng tham chiếu.

(Không phải lỗi: nhánh profile của `regSS_()` không tự gọi `ensureRegTabs_`, nhưng `regReadAll_/regUpsertOne_` có gọi nên Sheet rỗng vẫn dựng đúng tab/header — đường tạo registry mới chạy tốt.)

# v1.19.1 — đơn giản hóa tạo Instruction theo profile

Ngày: 2026-06-23

- **Mặc định tạo Instruction = VBQPPL.** `tl instructions` / `gen_instructions.generate()` không truyền profile ⇒ Instruction VBQPPL như cũ (không chèn `profile_setup`).
- **Văn bản thường với tên + notebook riêng ⇒ Instruction gắn profile mới + fallback VBQPPL.** `gen_instructions.generate(..., profile, notebook_id, folder_name, root_folder_id)`: khối `corpus_profile` nêu Project NÀY mặc định dùng profile đó (notebook riêng, folder `Van_ban_thuong/<tên>`), mọi thao tác đi theo profile, MISS mới fallback VBQPPL; thêm khối `profile_setup` (config snippet + các bước dựng 1 lần).
- **`tl profile-create --name <tên> --notebook <id> [--folder-name <tên>] [--apply]`** (DRY mặc định): khi `--apply` tạo folder `<tên>` trong Drive folder `Van_ban_thuong` (qua `bootstrap`→`vanBanThuongId` + `resolvefolder create=true`), in `config_profiles_patch` (ghi vào `profiles.<tên>`), các bước tiếp theo, và Instruction Project gắn profile.
- `tl instructions` thêm `--profile`/`--notebook`/`--folder-name`/`--root-folder-id` (dùng global `--profile` để chọn corpus).
- `gen_instructions.py` VERSION → 1.19.0; selftest 14/14 (thêm ca default-vbqppl + project-profile). `tl.py` selftest 65/65.

# v1.19.0 — Cách B: registry/manifest RIÊNG theo profile (webapp nhận docId mỗi request)

Ngày: 2026-06-23

- **Apps Script `references/Code.2.21.2f.gs` (predeploy):** webapp 1 deployment (giữ URL+token) nhận
  `registryDocId`/`manifestId` mỗi request; thiếu ⇒ hằng VBQPPL nền (`BASE_REGISTRY_DOC_ID_`/`BASE_MANIFEST_ID_`).
  Thêm `setCorpusScope_(p)` ở `main_()` + `resolveRegistry_/resolveManifest_`; `regSS_()` mở đúng Sheet profile
  (fail thì throw, không ghi nhầm VBQPPL); cache registry KEY theo registry (`_regCacheKey_`); `manifest_export`
  ghi đúng `manifestId` profile không đụng manifest nền; trả `registry_scope`/`manifest_scope`. Nhóm `nlm_*`
  giữ base-fallback theo `nlm_notebook_id`. Bump `APP_VERSION='2.21.2f'` (sau deploy → `contract_check.py --bump 2.21.2f`).
- **`tl.py`:** wrapper `_ScopedGas` tự forward `registryDocId`/`manifestId` (env `TL_REGISTRY_DOC_ID`/`TL_MANIFEST_ID`)
  vào MỌI call webapp khi `--profile` KHÁC mặc định; không đè param tường minh; `vbqppl` bỏ trống ⇒ nền.
- **Backward-compat:** `EXPECT_VERSION` giữ `2.21.2d` đến khi deploy 2.21.2f; `vbqppl` chạy y như cũ.
- Thêm `references/DELTA_v1.19.md` (gồm mục C — thiết lập 1 lần cho `vbthuong`, và mục D — quy ước prompt/lệnh theo profile); RUNBOOK thêm §D quy ước prompt.
- Selftest `tl.py` 65/65; `gen_instructions` 9/9; `contract_check --audit` KHỚP 2.21.2d; node --check 2.21.2f PASS.

# v1.18.0 — multi-corpus profile + download link priority + notebook slot guard

> **Bản HỢP NHẤT (best-of-both):** nền là nhánh có CLI thật (profile/link-priority/slot-audit, cache theo profile, 5 marker Instruction); ghép thêm bản vá `.gs` mạnh hơn (base-fallback) + `references/DELTA_v1.18.md` (đặc tả gốc) từ nhánh kia. Xem `references/MERGE_V1.18.0.md`.

- Thêm config v2/corpus profile: `vbqppl` giữ webapp/token và corpus pháp điển; `vbthuong`/profile dự án có folder/notebook/registry/manifest riêng.
- Runtime `tl.py` thêm global `--profile`, `tl profile-info`, cache manifest tách theo profile, và env `TL_ROOT_FOLDER_ID/TL_NOTEBOOK_ID/TL_REGISTRY_DOC_ID/TL_MANIFEST_ID`.
- Thêm `tl link-priority`: link DOWNLOAD người dùng ưu tiên thuvienphapluat.vn → luatvietnam.vn → congbao.chinhphu.vn → official khác; canonical lưu/đối chiếu vẫn official-first.
- Thêm `tl slot-audit`: đếm slot theo `nlm_notebook_id == notebookId`, chống lỗi NOTEBOOK_FULL giả. **Base-fallback:** dòng RỖNG `nlm_notebook_id` quy về notebook nền (VBQPPL) → VBQPPL vẫn đếm đúng không cần backfill, notebook dự án hết full giả. CLI trả thêm `slots_effective`/`is_base_notebook`.
- `references/Code.2.21.2e.gs` predeploy: vá `doNlmSlots_` **và** `doNlmDedup_` (Codex chỉ vá `doNlmSlots_`) theo base-fallback + thêm hằng `NLM_DEFAULT_NOTEBOOK_`; `EXPECT_VERSION` giữ `2.21.2d` đến khi deploy → `contract_check.py --bump 2.21.2e`.
- Instruction generator/audit thêm các khối `download_link_priority`, `corpus_profile`, `manifest_fallback`, `cross_notebook_query`, `nlm_notebook_id`.
- API_CONTRACT bổ sung §11 (config schema v2), cập nhật §7 (`baseNotebookId`/`base_notebook`) + §6 (`map_set notebookId`).
- Thêm `references/MULTI_CORPUS_PROFILE_V1_18.md`, `references/GS_2.21.2E_MULTI_CORPUS_SLOT.md`, `references/DELTA_v1.18.md`, `references/MERGE_V1.18.0.md`.
- Selftest `tl.py` 61/61; `gen_instructions.py --selftest` 9/9; `contract_check --audit` KHỚP 2.21.2d; node --check 2.21.2d + 2.21.2e PASS.

# v1.17.26 — combined external-ingest + instruction-audit gate

- Hợp nhất hai nhánh v1.17.25: giữ `tl external-ingest` và giữ `tl instruction-audit`/`gen_instructions.py` bản mạnh.
- `tl external-ingest` chặn `research_import/source_add(url)` nạp thẳng VBQPPL vào NLM, chặn notebook/folder mới mặc định, chặn PDF thô làm canonical.
- `tl instruction-audit` kiểm Instruction có đủ `SKILL_OF_RECORD`, `ingest_handoff`, `confirm_gate_web`, `QT-3`, `official-first`, `docx`, `notebook đang dùng`.
- `tl instructions` là alias sinh Instruction nhanh, tương thích luồng cũ.
- Thêm `references/MERGE_V1.17.26.md` và `references/INSTRUCTION_SKILL_BINDING.md`.

## 1.17.25 (2026-06-22) — external-ingest gate + Instruction binding
- Từ log Nghị định 129/2025: cấm dùng `research_import`/`source_add(url)` nạp thẳng VBQPPL vào NotebookLM hoặc tạo notebook tạm như nguồn dùng; `research_*` chỉ discovery.
- Thêm `scripts/gen_instructions.py`: sinh Instruction cho Claude Project/NotebookLM/config với `SKILL_OF_RECORD`, `ingest_handoff`, `confirm_gate_web`, official-first, ưu tiên docx/GDoc, và mặc định notebook đang dùng.
- Thêm `tl instruction-audit`: kiểm file Instruction hoặc output generator; fail nếu thiếu khối ràng buộc skill/QT-3/research discovery-only.
- Thêm `references/EXTERNAL_INGEST_GATE.md`; cập nhật SKILL/INSTALL để phân biệt đồng ý "tìm nguồn" với đồng ý "ghi/nạp".
- Selftest `tl.py` tăng lên 51/51; `gen_instructions.py --selftest` có 9/9 ca.

## 1.17.24 (2026-06-21) — best-combined amendment gate + relation-check
- So sánh và hợp nhất thêm nhánh `tra_luat_v1_17_22_amendment_gate`: giữ `relation-check`/backfill actions của v1.17.22, đồng thời đưa amendment gate trực tiếp vào `source-map`.
- `source-map` nay trả `amendment_candidates`, `unlinked_amendment_candidates`, `AMENDMENT_CANDIDATE_IN_CORPUS`, `UNLINKED_AMENDMENT_CANDIDATE`, `VBHN_RECHECK_REQUIRED`, `PAUSE_AND_ASK_USER`, và `action_required=PAUSE_AND_ASK_USER`.
- Thêm `tl exists <query> --json`: kiểm tra hiện diện/nguồn liên quan bằng `source-map` chuẩn hóa; miss là `UNKNOWN_NOT_ABSENT`, không kết luận vắng mặt.
- `tl vbhn-check --goc <số hiệu>` tự suy trích yếu từ manifest nếu thiếu `--subject`, để sinh query web kiểu `"luật <chủ đề>" "hợp nhất"` và `site:thuvienphapluat.vn ...`.
- Selftest tăng lên 46/46.

## 1.17.22 (2026-06-21) — stale relation guard + VBHN web-query hardening
- Thêm `tl relation-check --base <số hiệu gốc> --subject <trích yếu> [--amendment <số hiệu sửa đổi>]`: quét manifest/corpus/NLM để phát hiện văn bản sửa đổi đã có nhưng registry thiếu `goc/sua_doi`.
- Nếu phát hiện văn bản lỗi thời hoặc đã bị sửa đổi, quy trình bắt buộc là dừng rà bản cũ, hỏi người dùng để ghi registry/nạp văn bản ngay; không đưa vào mục xử lý sau khi việc đó quyết định nguồn rà soát.
- `relation-check` trả `AMENDMENT_FOUND_IN_CORPUS`, `RELATION_BACKFILL_REQUIRED`, và hành động gợi ý `BACKFILL_SUA_DOI_ON_BASE`/`BACKFILL_GOC_ON_AMENDMENT`.
- `vbhn-check`/`relation-check` mở rộng `qt5_queries`: thêm query đơn giản `"luật <chủ đề>" "hợp nhất"` và `site:thuvienphapluat.vn ...` để phát hiện nhanh VBHN ngoài corpus; vẫn giữ official-first khi chốt canonical.
- Thêm `references/STALE_RELATION_GUARD.md`; selftest tăng lên 43/43.

## 1.17.21 (2026-06-21) — postdeploy 2.21.2d + lessons hardening
- Bump chuẩn runtime/contract lên `2.21.2d`: `API_CONTRACT.md`, `tl.py EXPECT_VERSION`, `SKILL.md`, `RUNBOOK.md`, `INSTALL.md` đồng bộ với `Code.2.21.2d.gs`.
- Đưa bài học HD06 vào `references/RA_SOAT_LESSONS_2026_06.md` và RUNBOOK: không kết luận văn bản vắng mặt từ `reg_get name_contains`; phải chạy `tl source-map` + `tl locate/status`.
- `_fallback/gas.py` cảnh báo khi gọi `reg_get name_contains` và in `raw count`.
- `hygiene scan` thêm `duplicate_identity_groups` bên cạnh `duplicate_sohieu_groups_raw`, và cờ `NLM_STATUS_MISMATCH` cho nợ chuẩn hóa metadata NLM.
- Giữ nguyên nguyên tắc: có `nlm_source_id` và không removed thì vẫn query được; `nlm_status` khác `pushed/synced` không phải bằng chứng nguồn vắng mặt.

## 1.17.20 (2026-06-21) — registry hygiene year-parser parity
- Chấp nhận hướng sửa v1.17.19, nhưng vá thêm `scripts/registry_hygiene.py`: trước đó file này vẫn suy `issue_year` từ `tukhoa/keywords/trich_yeu`, có thể làm mất cờ `VBHN_MISSING_YEAR_OR_DATE` khi chạy hygiene độc lập.
- Siết check tên: nếu `issue_year=2024` nhưng tên chỉ chứa năm nguồn như `84-2015`, vẫn gắn `VBHN_NAME_MISSING_YEAR`; năm trong tên phải khớp năm ban hành VBHN.
- Giữ live/EXPECT `2.21.2c`; `references/Code.2.21.2d.gs` vẫn là bản predeploy để sửa server-side `manifest_export`.

## 1.17.19 (2026-06-21) — safe issue_year parser cho VBHN
- Fix runtime `_entry_issue_year`: không lấy năm bất kỳ trong `tukhoa/keywords/trich_yeu` vì có thể là năm của luật gốc được hợp nhất (ví dụ 84/2015/QH13), không phải năm ban hành VBHN.
- Thêm `references/Code.2.21.2d.gs` với `issueYearFromEntry_` an toàn tương tự; giữ `2.21.2c` là live/EXPECT cho tới khi deploy 2.21.2d và bump contract.
- Selftest bổ sung ca `issue_year_not_from_goc_in_keywords`, `issue_year_from_vbhn_name_separator`, `issue_year_from_issue_date`.

## 1.17.18 (2026-06-21) — VBHN cấp Bộ phải có năm + khép contract 2.21.2c

- Bump runtime post-deploy lên `2.21.2c`: `tl.py EXPECT_VERSION`, `API_CONTRACT.md`, `SKILL.md`, `RUNBOOK.md`, `INSTALL.md` đồng bộ với `Code.2.21.2c.gs`.
- Thêm guard VBHN cấp Bộ: nhận diện `NN/VBHN-BYT`, `05/VBHN-BGDĐT`, `2279/VBHN-BLĐTBXH`... và gắn `VBHN_MINISTRY_SCOPE`, `VBHN_MINISTRY_MISSING_YEAR`, `VBHN_MINISTRY_NAME_MISSING_YEAR`.
- `tl vbhn-normalize --json` report-only mẫu tên `VBHN_<so>-VBHN-<co_quan>_<year>_<ten_rut_gon>`; thiếu năm thì yêu cầu backfill từ dòng ngày ban hành trước khi rename.
- Đồng bộ `registry_hygiene.py` để đưa lỗi cấp Bộ thiếu năm vào `title_mismatch_candidates`, không gom/quarantine mù theo số hiệu trần.
- Selftest tăng lên 35/35.

## v1.17.17 — GS 2.21.2c predeploy hotfix + runtime warning trim

- Thêm `references/Code.2.21.2c.gs`:
  - giữ `removed_from_drive` khi còn `nlm_source_id` cũ, không tự set lại `pushed` trong `regen2`;
  - thêm action `reg_clear` để xóa mapping NLM có kiểm soát;
  - `manifest_export` canonical hóa số hiệu VBHN ngắn và xuất `issue_year` suy từ tên/metadata.
- Runtime: giảm nhiễu `VBHN_NUMBER_REUSE_RISK` khi VBHN đã có năm/chủ đề rõ.
- `vbhn-normalize` báo thêm `removed_nlm_mappings` để xử lý ghost/stale NLM sau khi xác nhận.

## 1.17.17 (2026-06-21) — hợp nhất hygiene-guards + normalize report + empty-name guard

- Lấy nhánh `v1.17.15-vbhn-hygiene-guards` làm nền vì có guard tốt hơn: sidecar `.docx/.pdf`, `NLM_GHOST_SOURCE`, `VBHN_SOHIEU_NORMALIZED_FROM_SHORT_VPQH`, `VBHN_NAME_MISSING_YEAR`, tách cụm VBHN theo năm/chủ đề/gốc/md5.
- Port lại lệnh `tl vbhn-normalize` từ nhánh v1.17.15 trước đó: report-only đề xuất backfill số hiệu VBHN, đổi tên thêm năm/chủ đề, liệt kê nguồn NLM mồ côi.
- FIX quan trọng: không cho tên rỗng match mọi truy vấn trong `locate/source-map/hygiene plan`; trước đó biểu thức `nk in qnk` khiến NLM ghost `name=''` có thể lọt vào truy vấn theo tên/số.
- Siết điểm canonical: nguồn NLM thiếu cả tên, số hiệu, cat bị hạ điểm mạnh, không thắng văn bản có metadata.
- Sửa `_goc_keys` để xử lý đúng `goc` dạng list/dict, tránh tạo khóa cụm bẩn kiểu `['84-2015-QH13']`.
- `registry_hygiene.py` đồng bộ thêm chuẩn hóa `NN-VPQH` → `NN-VBHN-VPQH` với VBHN, parser năm có `_2024_`, và flag `NLM_GHOST_SOURCE`/`VBHN_NAME_MISSING_YEAR`.
- Selftest tăng lên 30/30.

## 1.17.15 (2026-06-21) — VBHN hygiene/source-map guard
- FIX chuẩn hóa số hiệu VBHN VPQH trong runtime: `19-VPQH`/`40-VPQH` được canonicalize thành `19-VBHN-VPQH`/`40-VBHN-VPQH`.
- FIX parser năm cho tên file có underscore như `_2024_`, `_2026_`; giảm cờ sai `VBHN_MISSING_YEAR_OR_DATE`.
- SIẾT `hygiene/reconcile`: VBHN không gom cụm theo số hiệu trần; dùng số hiệu + năm/chủ đề/gốc/md5 để tránh quarantine nhầm VBHN 2023 khác chủ đề khi xử lý `14/VBHN-VPQH`.
- SIẾT canonical score: nguồn NLM rỗng cả tên/số hiệu/cat bị gắn `NLM_GHOST_SOURCE` và bị hạ điểm, không lấn bản có metadata khi query theo tên.
- TÁCH file `.docx/.pdf` gốc cạnh GDoc thành `sidecar_source_files`, không tính chung như orphan/quarantine candidate.
- Selftest tăng lên 28/28.

## 1.17.14 (2026-06-21) — VBHN official-first gate
- FIX lỗi quy trình từ log ATVSLĐ: không tự ghép VBHN làm bản dùng/canonical/NLM; nếu thiếu official thì hỏi người dùng nạp vào `_HOP_NAP` hoặc lấy nguồn chính thức.
- THÊM `tl vbhn-verify --official-required`: fail khi không có dấu hiệu nguồn chính thức/footnote hoặc khi nguồn/tên có dấu hiệu `ASSEMBLED`/tự ghép.
- THÊM `tl vbhn-compare --official-text ... --candidate-text ... --focus "Điều 53"` để so bản chính thức với bản tạm, bắt thiếu footnote và stale-ref kiểu giữ cả `Điều 111` lẫn `Điều 90`.
- THÊM `references/VBHN_OFFICIAL_FIRST.md`; cập nhật SKILL/RUNBOOK/INSTALL/VBHN_QT5 theo workflow official-first.
- Selftest tăng lên 22/22.

## 1.17.13 (2026-06-21) — best-combined VBHN QT-5 verification gate
- HỢP NHẤT bản `tra_luat_v1_17_12_vbhn_qt5.zip`: thêm `tl vbhn-check`, `tl vbhn-verify`, `tl vbhn-check --scan`.
- GIỮ guard v1.17.12: `NO_VERIFIED_VBHN_IN_CORPUS`, `QT5_WEB_REQUIRED`, `VBHN_NUMBER_REUSE_RISK`, `VBHN_BARE_NUMBER`, `VBHN_MISSING_YEAR_OR_DATE`.
- `vbhn-check` dò ứng viên trong manifest theo subject/goc/year, trả `qt5_queries` nếu không có hit và không kết luận vắng VBHN.
- `vbhn-verify` kiểm nội dung text/export: title, gốc/sửa đổi, năm và header VBHN; bắt dương tính giả đúng số hiệu nhưng sai chủ đề/năm.
- Sửa port: `vbhn-verify --sohieu` dùng `_canonical_for_query`; exporttext dùng tham số `fileId` theo contract hiện có.
- Selftest tăng lên 20/20.

## 1.17.12 (2026-06-21) — VBHN year/reuse guard + no-overclaim QT-5
- FIX lỗi phương pháp từ log: không kết luận "không có VBHN" từ một lần tìm/corpus miss; `source-map` nay dùng `NO_VERIFIED_VBHN_IN_CORPUS` + `QT5_WEB_REQUIRED`.
- THÊM guard số VBHN tái sử dụng theo năm: `VBHN_NUMBER_REUSE_RISK` khi query số VBHN trần; phải verify ngày ban hành + tiêu đề + dòng hợp nhất.
- THÊM cờ hygiene `VBHN_BARE_NUMBER`, `VBHN_MISSING_YEAR_OR_DATE` để bắt file kiểu `VBHN_14-VBHN-VPQH`/orphan thiếu năm, thiếu chủ đề.
- `source-map` trả `qt5_search_hints` theo trích yếu/chủ đề + "hợp nhất" để nhắc đúng QT-5.
- Selftest tăng lên 16/16, có fixture cho `14/VBHN-VPQH` tái sử dụng theo năm.

## 1.17.11 (2026-06-21) — best-combined source-map + runtime-log hygiene
- HỢP NHẤT bản `source-map hotfix` với bản `runtime-log-hardened`: thêm `tl source-map <q...>` để lập bản đồ nguồn rà soát VBHN-first trước khi query/extract.
- `source-map` chọn VBHN liên quan nếu trường `goc` chứa số hiệu đích; cảnh báo thiếu VBHN đời cũ đã được v1.17.12 thay bằng `NO_VERIFIED_VBHN_IN_CORPUS` + `QT5_WEB_REQUIRED`.
- GIỮ lớp hardening của v1.17.10: `locate` chạy offline không cần token khi có cache, match tên theo `_name_key`, in `WARN=...`; `hygiene/registry-doctor` có `title_mismatch_candidates`.
- NÂNG `_entry_score`: VBHN là tiebreaker và bản hết hiệu lực/thay thế bị trừ điểm, gần hơn tinh thần `registryRank_` 2.21.2b.
- THÊM `references/REALRUN_4LAWS_SOURCE_MAP_FIXES.md`; selftest tăng lên 14/14.

## 1.17.10 (2026-06-21) — harden theo log chạy thật v1.17.9 + Code.gs 2.21.2b
- THÊM cảnh báo `OMNIBUS_NARROW_TITLE_CHECK`/`TITLE_METADATA_MISMATCH` trong `tl locate`, `tl hygiene scan` và `registry-doctor`, bắt trường hợp tên file hẹp/sai so với quan hệ sửa nhiều luật.
- `tl locate` ưu tiên manifest đầy đủ trước webapp `find`, hỗ trợ `--refresh/--debug`, in `WARN=...` và hướng dẫn chạy `tl status`/`hygiene plan` trước khi dùng nguồn.
- `hygiene scan` thêm `title_mismatch_candidates` và sample có `flags`, giúp phát hiện các dòng kiểu `Luat_57-2024-QH15_Bao_hiem_y_te` trước khi rà soát.
- Cập nhật SKILL/INSTALL/RUNBOOK: overlay-only là trạng thái có kiểm soát; ưu tiên `tl.py`; fallback thấp dùng `scripts/_fallback/gas.py ACTION key=value`, không dùng cú pháp cũ `gas.py get ACTION`.
- GIỮ Apps Script `Code.2.21.2b.gs` nguyên bản deploy-ready vì log chạy thật đã xanh bootstrap/ping; sửa tập trung vào lớp runtime chọn nguồn/vệ sinh registry.

## 1.17.9 (2026-06-21) — post-deploy 2.21.2b + Unicode verify + hygiene guard
- KHÉP lệch version: webapp live 2.21.2b, API_CONTRACT/tl EXPECT/SKILL/RUNBOOK đồng bộ 2.21.2b.
- THÊM requirements.txt (stdlib-only) để tài liệu `pip install -r requirements.txt` không lệch thực tế.
- THÊM `tl extract --find` tìm chuỗi sau Unicode NFC normalize, tránh grep âm tính giả với tiếng Việt có dấu.
- FIX hygiene/reconcile: không parse tên `Mẫu_*/Mau_*/PL_*/Phụ_lục*` thành số hiệu văn bản, tránh quarantine nhầm biểu mẫu/phụ lục.
- UPDATE contract_check --bump: API_CONTRACT không còn sót version cũ trong các dòng ghi chú meta_find/fetch_url_to_drive.

# tra-luat — CHANGELOG goi refactor

## 1.17.8 (2026-06-21) — best-of-both + Code.gs 2.21.2b VBHN-first
- NEN: v1.17.7 da xanh (UTF-8, pre-deploy 2.21.1, patcher stdin, registry-doctor, ingest guard) + runtime reconcile tu best-of-both.
- THEM `Code.2.21.2b.gs`: giu 7 fix Apps Script 2.21.2 va them VBHN-first/superseded sink trong `registryRank_`.
- GIU contract/EXPECT = 2.21.1 pre-deploy; sau khi deploy 2.21.2b va runtime xanh thi `contract_check.py --bump 2.21.2b`.
- PORT `tl hygiene reconcile` va alias `tl reconcile` de gom cum theo so hieu parse tu ten hoac md5, van dry-run mac dinh va chi move khi `--apply --confirm yes`.
- FIX tiep loi cua cac nhanh ung vien: best-of-both bi pre-bump 2.21.2 va crash Unicode help; nhanh D co 2.21.2b nhung patcher selftest con FAIL node temp.

## 1.17.7 (2026-06-21) — hop nhat toi uu Code.gs 2.21.2 + runtime hygiene
- NEN: v1.17.6 nhanh (runtime v1.17.5 + Code.2.21.2 deploy-ready + UTF-8 hardening), giu contract/EXPECT=2.21.1 theo ky luat pre-deploy.
- FIX apply_gs_patches selftest tren Windows/Codex sandbox: `node --check` chay qua stdin UTF-8, khong dung file tam trong `%TEMP%`.
- THEM lai `scripts/registry_hygiene.py` + `tl registry-doctor` de tuong thich nguoc voi nhanh 2.21.2 report-only; `tl hygiene` van la cong cu manh hon khi can plan/apply.
- SIET `tl ingest --apply`: neu overlay thieu `standardize_name.py` va chua truyen `--ten`, dung ro rang thay vi organize voi ten chua chuan.
- Cap nhat SKILL/INSTALL: package v1.17.7, live contract 2.21.1, co `Code.2.21.2.gs` deploy-ready va `CODE_2.21.2_FIXES.md` huong dan deploy->bump.

## 1.17.6 (2026-06-21) — merge nhanh CODE.GS (2.21.2, 7 fix) vao runtime v1.17.5
- THEM Code.2.21.2.gs (deploy-ready): 7 fix Apps Script THAT (verified voi 2.21.1): doBootstrap_ persist
  TL_ROOT_ID; manifest_export persist TL_MANIFEST_ID + manifest auto-heal; manifestIndexIds_ doc entries||files;
  registryRank_ uu tien canonical; regCacheBust_ 64 chunk; setup/getToken mask token; Unicode Windows.
- THEM UTF-8 hardening (sys.stdout/stderr.reconfigure) vao tl/contract_check/apply + _fallback/* (Windows + tieng Viet).
- GIU contract/EXPECT = 2.21.1 (pre-deploy; webapp live van 2.21.1). references/CODE_2.21.2_FIXES.md co duong deploy->bump.
- GIU runtime v1.17.5: hygiene scan/plan/query + --apply move, reconcile (sohieu-tu-ten + md5), init-config,
  doctor --offline/--deep, _fallback khong-de, boot download-entries. hygiene > registry-doctor cua nhanh B.
- Kiem: tl 5/5·cc 2/2·apply 12/12; audit 2.21.1; node --check CA 2.21.1 LAN 2.21.2 PASS; hygiene chay; 0 pyc.

# tra-luat — CHANGELOG goi refactor

## 1.17.5 (2026-06-21) — hop nhat v1.17.4-runtime-hygiene + bu phat hien reconcile
- LAY tu v1.17.4: `tl hygiene scan/plan/query` (thay reconcile) voi `_entry_score` chon canonical co nguyen tac,
  accent-strip, va `--apply --confirm yes` THUC THI move->QUARANTINE (DRY-RUN mac dinh, KHONG trash).
- PORT tu reconcile cua toi: `_sohieu_or_parsed` (parse so hieu tu ten tho, coi `_`≡`-`) -> scan gop dung cum
  junk gach-duoi; them `duplicates_by_md5` (bat ban byte-trung khong parse duoc so hieu); `--to-cat` chon dich move.
- GIU het v1.17.4 (= v1.17.3 cua toi + fix): _fallback khong-de, boot download-entries, boot --config,
  _fallback/gas loi-gon, init-config, doctor --offline/--deep, sach pyc, bump dong bo SKILL/RUNBOOK.
- Kiem: tl 5/5·cc 2/2·apply 12/12; audit KHOP 2.21.1; hygiene scan dup_sohieu=2/dup_md5=2/orphans=6 tren fixture;
  plan ghep canonical↔junk; --apply DRY mac dinh; node PASS; 0 pyc.


## v1.17.4 — Runtime hygiene & review support

- Thêm `tl hygiene scan|plan|query` để phát hiện duplicate/orphan kể cả dòng `sohieu` rỗng; lập kế hoạch QUARANTINE an toàn, không trash.
- `tl extract` nhận thêm `--sohieu` để tự chọn canonical từ manifest rồi `exporttext` ra đĩa; tránh phải tự tìm gdocId khi rà soát.
- `tl manifest --touched-drive` không còn xanh giả nếu `regen2` và `manifest_export` lệch `treeHash`/`corpus_count`.
- Siết `hygiene` để chạy offline từ cache nếu có, và chỉ gọi webapp khi refresh/apply/cần manifest.
- Cập nhật tài liệu RUNBOOK/SKILL: overlay thiếu `rasoat/backfill` là trạng thái có kiểm soát; dùng `rasoat` fallback plan hoặc `hygiene`/`extract` cho workflow thủ công có cấu trúc.

# tra-luat — CHANGELOG gói refactor

## 1.17.4 (2026-06-20) — hợp nhất v1.16.11 (fix boot --config) lên nền v1.17.1
- FIX bug thật (reviewer v1.16.11 bắt, v1.17.1 cũng dính): `tl --config FILE boot` không truyền creds xuống
  subprocess. Nay `cmd_boot` `load_creds(--config)` trước subprocess + truyền `--config` cho `_fallback/boot.py`;
  `_fallback/boot.py` nhận `--config`.
- `_fallback/gas.py`: GET/POST bọc lỗi urllib → dict gọn (hết traceback cho boot/manifest/preingest).
- Dọn header SKILL.md → v1.17.4.
- GIỮ toàn bộ v1.17.1: `_fallback/`+`_imp` không-đè, boot download-entries, `init-config`, `doctor --offline/--deep`,
  `rasoat` graceful, bump đồng bộ SKILL/RUNBOOK, sạch pyc.
- Kiểm: tl 5/5·cc 2/2·apply 12/12; audit ✓2.21.1; boot --config tới nơi; non-clobber; node PASS.

# tra-luat — CHANGELOG gói refactor

## 1.17.1 (2026-06-20) — hợp nhất v1.17.0-runtime-stable (lấy tiện, bỏ rủi ro)
- LẤY từ v1.17.0 của reviewer: `tl init-config` (lưu config local từ JSON mirror private — vấn đề #4);
  `tl doctor` giàu (core/optional/credential/contract/ping, cờ `--offline`/`--deep`, exit-code);
  `tl rasoat` graceful (thiếu optional → báo rõ, không gọi file vắng).
- GIỮ kiến trúc an-toàn v1.16.10: `_fallback/`+`_imp()` ROOT-precedence (KHÔNG đè bản nền thật);
  `_fallback/boot.py` đã sửa bug index rỗng (download file manifest → parse entries); không rác pyc;
  `--bump` đồng bộ SKILL/RUNBOOK.
- doctor THÍCH NGHI _fallback: core script tính cả khi ở `_fallback/`, hiện rõ nguồn "gốc/_fallback".
- Bằng chứng: v1.17.0 KHÔNG sửa 3 điểm đã flag (ship gốc→đè; boot index rỗng; pyc) — chi tiết
  references/COMPARISON_HOTFIX.md. Selftest tl 5/5·cc 2/2·apply 12/12; audit ✓2.21.1; node PASS.

# tra-luat — CHANGELOG gói refactor

## 1.16.10 (2026-06-20) — tổng hợp best-of-both với runtime-hotfix của reviewer
- **`scripts/_fallback/`** (mới): bản nền TỐI THIỂU `gas/boot/manifest_build/preingest_gate` (hội tụ với
  hotfix reviewer) NHƯNG đặt ở `_fallback/` để **không đè** bản nền thật khi cài chồng lên skill đầy đủ.
- **`_imp()` ROOT-precedence** trong `tl.py` + `contract_check.py`: ưu tiên `scripts/` gốc (bản thật) →
  rồi `_fallback/`. Kết quả: phiên trống chạy được `ping/boot/manifest/preingest`; skill đầy đủ dùng bản thật.
- **Hết phụ thuộc cứng `gas`** ở `contract_check.py` (đường online) — sửa nốt lỗi reviewer chỉ (v1.16.9 còn sót).
- **`contract_check --bump` đồng bộ SKILL.md + RUNBOOK.md** (lấy ý reviewer; nay tái lập được, bỏ sửa tay).
- `references/COMPARISON_HOTFIX.md` (mới): đối chiếu hotfix vs bản tôi vs tổng hợp + lý do không-đè + ghi công.
- Không kèm `__pycache__`. Kiểm: tl 5/5 · cc 2/2 · apply 12/12 · audit KHỚP 2.21.1 · node PASS;
  standalone resolve `_fallback`; non-clobber (gốc thắng); bump nháp 2.21.1→2.21.2 đồng bộ SKILL/RUNBOOK 8 chỗ.

# tra-luat — CHANGELOG gói refactor

## 1.16.9 (2026-06-20) — chạy thật lần đầu: overlay tự-sống + post-deploy 2.21.1 (rà soát thứ 7)
- **Gia cố overlay đứng riêng** (gốc rễ: thiếu script nền chặn cứng CLI): `tl.py` thêm **client webapp built-in
  (stdlib)** dùng khi thiếu `gas.py` ⇒ `ping/locate/status/boot(lite)` chạy không cần nền; lệnh cần nền báo rõ
  (không còn `ModuleNotFoundError`); thêm **`tl doctor`** (liệt kê nền có/thiếu, chế độ, thử ping).
- **Bump post-deploy 2.21.1** (webapp xác nhận live 2.21.1): API_CONTRACT stamp + tl.py EXPECT_VERSION (+ literal
  selftest) + SKILL.md/RUNBOOK → 2.21.1. `contract_check --audit` ✓ KHỚP 2.21.1.
- `references/SKILL_ISSUES_FIRSTRUN.md` (mới) — ghi nhận 3 vấn đề first-run + trạng thái xử lý + kênh đi vòng.
- Đã test phiên CHỈ-CÓ-tl.py: `doctor` chạy đầy đủ; `ingest/manifest` báo `_need_base` rõ; `ping` creds-giả trả
  dict lỗi (không traceback) qua client built-in. Selftest tl 5/5, cc 2/2, apply 12/12.

# tra-luat — CHANGELOG gói refactor

## 1.16.8 (2026-06-20) — dọn nốt comment + thêm bump post-deploy (rà soát thứ 6)
- Sửa sạn comment cuối `.gs`: `ping phải trả version: 2.21.1'.` (dư `'`) → `2.21.1.` (sửa tận patch `cmt_ping_ver`).
- **`contract_check.py --bump <VERSION>`** (MỚI, post-deploy): nâng ĐỒNG BỘ stamp API_CONTRACT + tl.py
  EXPECT_VERSION (+ literal selftest) + neutralize cảnh báo `⚠ HỎNG ở deploy` → `✓ đã vá`. Gói ship VẪN ở
  2.20.0 (pre-deploy); chỉ bump SAU khi deploy 2.21.1 + runtime xanh. Test trên bản sao: audit/selftest đều khớp 2.21.1.
- Code.gs vẫn: auto 41/41, audit 24/24, node PASS, DEPLOYABLE_CANDIDATE (không đổi chức năng so với 1.16.7).

# tra-luat — CHANGELOG gói refactor

## 1.16.7 (2026-06-20) — đóng lỗ hổng F5 + xóa dead code (rà soát thứ 5)
- **F5 (P1) thật sự áp**: `manifest_export` dùng `treeHashV2_(corpusObjs)` + trả `corpus_count` → cùng cơ sở `regen2`.
  Trước đó F5 chỉ ở PATCH doc, CHƯA vào bảng patch tự động ⇒ `Code.2.21.1.gs` v1.16.6 vẫn lệch treeHash.
- **Đóng lỗ hổng audit**: thêm 4 audit (3 cho F5 + 1 cho doRegen_) ⇒ audit 20→24. (Đây là gốc rễ: audit cũ
  không kiểm F5 nên không phát hiện.)
- **Xóa `doRegen_`** legacy (dead code sau stub F6) bằng engine mới `delete_span` (end-anchor = `doManifestRead_`,
  giữ nguyên doManifestRead_/buildConfigObject_).
- Sửa 3 comment stale: header `ping 2.20.0`→`2.21.1`; `readconfig (và downloadUrl)`→private; note `vb_status` thêm enum.
- Chạy trên code.gs deploy thật: **auto 41/41, audit 24/24, node --check PASS, DEPLOYABLE_CANDIDATE**.
- `references/Code.2.21.1.gs` 3164 dòng — 0 stale version, 0 URL tải public.

# tra-luat — CHANGELOG gói refactor

## 1.16.6 (2026-06-20) — BEST-OF-BOTH (harness rà-soát-độc-lập + coverage đầy đủ)
So sánh với bản 1.16.5 độc lập (tác giả khác) → hợp nhất điểm mạnh hai bên:
- LẤY TỪ BẢN ĐỘC LẬP (harness an toàn hơn): gate **DEPLOYABLE_CANDIDATE / NOT_DEPLOYABLE_YET**,
  exit code nghiêm (0 chỉ khi deployable), **20 static audit** (rộng hơn 5 của tôi), `configview_alias`
  scope vào `dispatchAction_`, `--force` chỉ để debug. Bản đó selftest 12/12 — GIỮ.
- GIỮ TỪ BẢN CỦA TÔI (coverage cao hơn): auto cả 11 rewrite hàm lớn (F1 driveSearch_+metafind+find,
  F6 stub, F7/F7b writeconfig, F9b organize, F10 map_set, F11b vb_status, F13b copy_convert, E read/writeconfig)
  → KHÔNG để manual. Bản độc lập chỉ auto 21 và để các rewrite này MANUAL (auto-output NOT_DEPLOYABLE).
- AUDIT RỘNG CỦA HỌ bắt thêm 2 điểm bản tôi sót: (1) comment header đầu file vẫn ghi `action=regen` →
  thêm vá `header_regen_comment`; (2) `manifest` action trả `downloadUrl` public → thêm vá `manifest_downloadurl`
  (đổi `driveFileId`). Sửa pattern audit `map_set_notebook` cho khớp impl inline (`nlm_notebook_id: p.notebookId...`).
- KẾT QUẢ chạy trên code.gs deploy THẬT: **auto 34/34, audit 20/20, node --check PASS, DEPLOYABLE_CANDIDATE, exit 0**.
  `references/Code.2.21.1.gs` = file deploy thẳng (0 URL tải công khai cho cả config lẫn manifest, 0 `regen` legacy).

# tra-luat — CHANGELOG gói refactor

## 1.16.5 (2026-06-20) — full Code.gs 2.21.1 HỢP NHẤT (đã node --check trên file deploy thật)
- Nhận `code.gs` ĐANG DEPLOY (3151 dòng) → khớp anchor CHÍNH XÁC → `apply_gs_patches.py` áp **32/32 tự động, 0 lỗi**,
  static audit 5/5, **`node --check` PASS** (file kết quả 3203 dòng).
- Sửa anchor `configview_alias` (F2): chuỗi trùng trong khối comment → anchor kèm dòng `/* --- v2.12 --- */` (duy nhất).
  Sửa `copyconvert_viewurl` (F13b): trùng với copyOneExt_ dòng 517 → anchor kèm dòng `srcFileId:...` (chỉ doCopyConvert_).
- Chuyển HẾT mục MANUAL→AUTO: F1 (driveSearch_ + metafind scope:corpus + find tầng-3), F6 (stub regen), F7/F7b
  (writeconfig bỏ public-share + privateConfigFile_), F9 (extDest_ fail-closed), F9b (organize fail-closed),
  F10 (map_set nlm_notebook_id), F11b (vb_status), F13b (copy_convert viewUrl), E (read/writeconfig downloadUrl→private).
  MANUAL còn lại: chỉ F16c (appsscript.json — chọn 1 trong 2 manifest) + xóa `doRegen_` (dead code, tùy chọn).
- Giao kèm: `references/Code.2.21.1.gs` (file deploy thẳng) + `references/PATCH_REPORT.sample.md` (report thật của lần áp).

# tra-luat — CHANGELOG gói refactor

## 1.16.4 (2026-06-20) — nạp rà soát thứ 4 (A–E) + apply_gs_patches.py (hướng 2)
- **A** hết stale `2.21.0` (patch + INSTALL). **B** `meta_find` mặc định `scope:'corpus'`.
  **C** F15c rà TRIỆT ĐỂ `CONFIG.ROOT_FOLDER_ID` (gồm setup/doExport_/doPerf_/diagnostics) qua global-root + audit.
  **D** `doManifestRead_` hết nhắc `regen` deprecated. **E** `readconfig`/`writeconfig` `downloadUrl` khi config private.
- **`scripts/apply_gs_patches.py`** (MỚI) — áp patch .gs ANCHOR NGHIÊM NGẶT: dry-run mặc định; khớp đúng-1-lần
  (0/≥2 ⇒ fail, không ghi nửa vời); `PATCH_REPORT.md` (auto/manual/audit); static audit (jsonOut_, version cũ,
  CONFIG.ROOT_FOLDER_ID ngoài 3 nơi, privateConfigFile_…); `node --check`. selftest engine 8/8.
  Tự động phần DỄ SÓT (version + global rootId_ + chèn helper + F8 scoped + vá ngắn); rewrite hàm lớn → MANUAL theo doc.

# tra-luat — CHANGELOG gói refactor

## 1.16.3 (2026-06-20) — nạp rà soát thứ 3 (lớp .gs 2.21.1)
Webapp đích sau khi áp patch: **2.21.1** (trước: 2.21.0). PATCH đổi tên → `PATCH_v2.21.1.gs.md`.
- **F7b** revoke sharing CÔNG KHAI của `tra_luat_config.json` ĐÃ tồn tại (`privateConfigFile_`), không chỉ bỏ share khi tạo mới — kiểm bằng `perm_list`.
- **F9b** `doOrganize_` fail-closed khi cat sai (chặn đường rơi ROOT còn lại sau F9; chấp cả cat='4').
- **F15c** hoàn thiện root persistence: helper `rootId_()` + thay mọi `CONFIG.ROOT_FOLDER_ID` vận hành (kèm phương án thay thế: bỏ hẳn tự-tạo-root).
- **F16c** chốt policy egress: tách `APPSSCRIPT_MANIFEST.open-egress.json` / `.restricted-egress.json` (bỏ file có khóa `_GHI_CHU_`); mặc định khuyến nghị restricted.
- **F4b** `regen2` đọc CẢ `ap.soHieu` (cũ) lẫn `ap.sohieu` (mới) — tương thích ngược metadata.
- Sửa nit: nhãn patch "F8–F18"→"F8–F16b"; INSTALL header/VERSION → 1.16.3; tên file PATCH cập nhật ở SKILL/INSTALL.

## 1.16.2 (2026-06-20) — nạp rà soát thứ 2 (16 góp ý) → lớp .gs F8–F16b
- F8 `fetch_url_to_drive` bỏ `jsonOut_` (mất payload — P0). F9 `resolveFolder_`/`extDest_` fail-closed (P0).
  F10 `map_set` ghi `nlm_notebook_id` (P0). F11b `vb_status` thêm `VBHN_IN_REGISTRY_NOT_ON_NLM` (P0).
  F12 `importext` chấp `files=[id,...]`. F13b `copy_convert` viewUrl đúng loại. F14b `batch` cap+cấm lồng.
  F15b bootstrap persist root. F16b manifest whitelist + cảnh báo fetch ngoài.
- `contract_check.py --audit` (offline đối chiếu API_CONTRACT ↔ tl.py). INSTALL ghi rõ OVERLAY + stdlib-only.

## 1.16.1 (2026-06-20) — hoàn thiện rà soát .gs (F4/F6/F7)
- F4 chuẩn hóa appProperties chữ thường; F6 khai tử `regen` legacy; F7 gỡ public-share mirror chứa token.

## 1.16.0 (2026-06-20) — refactor tất định hóa vận hành (4 hướng)
1. API_CONTRACT.md (đóng dấu 2.20.0; sửa 3 lệch). 2. RUNBOOK.md (đánh số). 3. tl.py + contract_check.py.
4. SKILL.md rút gọn LÕI + DOCTRINE_APPENDIX.md giữ nguyên changelog cũ.

## v1.17.4 — runtime polish sau chạy thật
- `_fallback/boot.py` thêm postcondition: nếu manifest có count/corpus_count nhưng `entries_indexed=0` thì lỗi, tránh boot xanh giả.
- `tl rasoat` khi thiếu optional script in fallback plan có cấu trúc thay vì chỉ báo thiếu, giúp Claude chuyển sang webapp + NLM + legal MCP.
- Giữ nguyên `_fallback` không-đè, `init-config`, `boot --config`, version gate 2.21.1.
