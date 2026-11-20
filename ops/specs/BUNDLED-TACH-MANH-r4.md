tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# BUNDLED-TACH-MANH r4 — tách `scripts/tl_test_fragments_bundled.py` thành nhiều mảnh dưới ngưỡng WARN, GIỮ NGUYÊN bộ canh kích thước

- packet_id: BUNDLED-TACH-MANH; revision: 4; thay r3 (`305e04fc`), r2 (`420b125f`) và r1 (`e38cc986`, chưa đóng băng hợp lệ — mục sổ https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7046243035).

| trường | giá trị |
|---|---|
| `packet_issue` | **#433** (Q1, chủ kho chốt 2026-11-20). Packet này mở để gỡ chặn packet SECRETS-SET-BUNDLE-KIEU của #433; TEST_ID fragment mới mang tiền tố `wp433_`. |
| `nguon_cap_viec` | Chủ kho 2026-11-20 (phiên điều phối #1206): "Tách bundled trước" — packet riêng, làm TRƯỚC secrets-set, giữ nguyên bộ canh (không nâng ngưỡng, không waiver). |
| `phu_thuoc` | Không. Chặn: SECRETS-SET-BUNDLE-KIEU (nội dung ghim tại commit `a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c`, đang giữ). |
| `review_class` | `sensitive`: chạm `scripts/tl_core/test_fragments.py` (hợp đồng nạp fragment, chạy trong gói phát hành) và `scripts/tl_core/release.py` (cổng `test-fragments-check` lane LAND). |
| `base` | `0f9aa2a2cc697129e1f5be72feddf60986286865`. Phiên thi hành đo lại §0 trên base thật của lease và DỪNG nếu lệch. Đo trên clone ĐẦY ĐỦ: clone nông làm `wp1099_nlm_nap_lai` đỏ giả (thiếu object `358451e8`). |

Các quyết định Q1–Q6 đã được chủ kho chốt 2026-11-20 (xem §9); mỗi chỗ ghi kèm nhãn Qn.

## 0. Hiện trạng (đo trên `0f9aa2a`)

Bằng chứng ở `ops/reviews/bundled-tach-manh-spec-r1/` (README nêu từng tệp).

- **Bộ canh:** `_py_size_findings` (`scripts/tl_core/workflow.py:732`) WARN > 280 KiB = 286.720 B, FAIL > 320 KiB = 327.680 B; mục đích: trần mount Cowork ~343 KB/tệp
  (cắt cụt). Ca `r125_py_size_guard_wired_in_audit` (`scripts/tl_selftest.py:14716–14735`) đòi `py_size.warn == []`. Bundled là tệp RUNTIME: nằm trong
  `_RELEASE_REQUIRED_FILES` (`scripts/tl_core/release.py:486`) và được `load_runtime_fragment_cases` đọc trong gói ⇒ lý do của bộ canh áp đúng cho nó.
- **Kích thước:** bundled 285.112 B (18 fragment, 285.000 B dòng nguồn); dư 1.608 B trước WARN. Lớn nhất: `wp433_gws_cred_dich_ngoai_kho.py` 35.219 B,
  nhỏ nhất `wp45_fragment_canary.py` 245 B. Fragment secrets-set thêm 15.686 B ⇒ 300.798 B ⇒ WARN ⇒ r125 đỏ. Một fragment nhỏ (≤ 1.608 B) vẫn lọt dưới WARN (reviewer đo: fixture nhỏ ⇒ 285.236 B), nhưng mọi fragment cỡ thường thì vượt.
- **Điểm chạm** (rg toàn kho, trừ `ops/land`, `ops/reviews`):
  - `scripts/tl_core/test_fragments.py`: `_BUNDLED_MODULE_NAME` (31), `_read_bundled_sources` (353–400, hợp đồng data-only MỘT phép gán
    `BUNDLED_FRAGMENT_SOURCES`), `_compile_bundled_entries`, `discover_bundled_test_ids`, `load_bundled_fragment_cases`, `_runtime_fragment_topology` (dev nếu có
    `scripts/test_fragments/` không rỗng, ngược lại bundle), `generate_bundled_module_bytes` (464).
  - `scripts/tl_core/release.py`: `_test_fragments_check` (206–255, so byte MỘT tệp), `_RELEASE_REQUIRED_FILES` (486).
  - `.github/checks/bundle_fragment_check.py`: chỉ gọi `load_runtime_fragment_cases` trong gói giải nén + `has_bundled_module` (tệp chính) — không đổi.
  - `.githooks/eol_policy_test.py`: `_tai_sinh_bundled` (884–887) và `case_…driver` (976–979) ghi bundled từ fragment THẬT bằng
    `generate_bundled_module_bytes` ⇒ phải ghi đủ mảnh. Các ca khác (934, selftest 31884–32090, `wp47`) dùng thư mục fixture nhỏ ⇒ một mảnh, byte y hệt nay.
  - `references/golden/workflow_audit.json:1196` `files_scanned: 73` ⇒ thêm một tệp `.py` thành 74.
  - `.claude/dev/gate_lifecycle.py:73` `_CATALOG_POLICY_PATHS` chứa đường bundled (dev-side, chỉ băm chính sách) — xem §2.
  - Tài liệu: `references/COMMANDS.md:60`, `docs/PROTOCOL_DA_PHIEN.md`, ADR-0031, nhiều `ops/specs/*` nhắc tên tệp — xem §2.
  - `scripts/tl_selftest.py`: hai ca `r291_docs_ngoai_goi` (~22775) và `r357_agents_ngoai_goi` (~22836) đọc `RELEASE_MANIFEST.json` trên CÂY LÀM VIỆC (`root / "RELEASE_MANIFEST.json"`, không qua Git) và ghim `len(paths) == 185` kèm dòng KÊ KHAI SLOT ⇒ thêm mảnh 2 phải đổi thành 186 cùng lúc với manifest (reviewer lượt 2 đo: manifest 186 + ghim 185 ⇒ selftest 1783/1785).
  - Trần gói 200 tệp: `RELEASE_MANIFEST.json` liệt kê 185 tệp ⇒ 186; ZIP phát hành có thêm chính manifest nên 186 ⇒ 187 entry. Trần 200 đếm theo entry ZIP.
  - `RELEASE_MANIFEST.json` băm nội dung từng tệp gói: candidate đổi 5 tệp đã có trong manifest (`release.py`, `test_fragments.py`, `tl_selftest.py`, bundled mảnh 1, golden) và thêm mảnh 2; Land Operator tái sinh và commit manifest theo M8 trước khi đóng băng candidate ⇒ nếu không tái sinh trong chính packet thì job `gate` (lane LAND `release-verify --strict`) trên master ĐỎ từ lúc merge tới lúc merge PR manifest. Đây là nếp các packet trước (đo: merge #1453 `00ee839` ⇒ run 44711337223 job `gate` failure, xanh lại sau #1454). Reviewer đo trên nguyên mẫu: `release-verify RELEASE_MANIFEST.json --strict` rc 2.

## 1. `write_set`

```
.githooks/eol_policy_test.py
references/golden/workflow_audit.json
scripts/test_fragments/wp433_bundled_tach_manh.py
scripts/tl_core/release.py
scripts/tl_core/test_fragments.py
scripts/tl_selftest.py
scripts/tl_test_fragments_bundled.py
scripts/tl_test_fragments_bundled_2.py
```

Ngoài write set của WORKER, candidate có thêm đúng MỘT đường do **Land Operator** (phiên điều phối) ghi — protocol §9 cấm worker sửa manifest:

```
RELEASE_MANIFEST.json
```

**Candidate 9 đường (worker 8 + Land Operator 1) > trần 6 của ADR-0053 ⇒ nâng trần (Q2 + Q5 + Q6, chủ kho; E2), khối dưới chép nguyên vào lease.**
Không gộp được: golden phải đổi vì `files_scanned`; `eol_policy_test` phải đổi vì hai ca ghi bundled từ fragment thật; manifest phải đổi để master không đỏ
(Q5); `tl_selftest.py` phải đổi vì hai ca ghim số tệp manifest (Q6). Hai tệp bundled CHỈ sinh bằng `write_bundled_modules(scripts/test_fragments, scripts)`
(M1); `RELEASE_MANIFEST.json` CHỈ sinh bằng `python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json` (M8) — không sửa tay.

```yaml
nang_tran:
  truc: kich_thuoc_packet
  ai_nang: ducthangho
  tran_cu: '<= 6 tep, <= 450 dong them (ADR-0053, packet sensitive)'
  tran_moi: '<= 9 duong dan trong candidate (worker 8 + Land Operator 1: RELEASE_MANIFEST.json), <= 450 dong them'
  can_cu: 'Chu kho 2026-11-20 trong phien dieu phoi #1206: Q2 nang len 7 tep, Q5 dua RELEASE_MANIFEST.json vao candidate, Q6 them scripts/tl_selftest.py (2 ca ghim 185 -> 186) => 9 duong dan. Numstat nguyen mau base 0f9aa2a, 7 tep khong ke manifest: eol_policy_test 2/4, golden 1/1, fragment 130/0, release.py 22/5, test_fragments.py 90/26, bundled 2/9, bundled_2 14/0 = +261/-45; do o review luot 3 (base 0f9aa2a): 7 duong nguyen mau +261/-45, M9 tl_selftest +4/-2, manifest +18/-13 => tong 9 duong +283/-60.'
```

**Điều kiện cấp lease (E2):** comment chủ kho trên #433 cấp ngoại lệ
bundled nêu đúng `packet_id` `BUNDLED-TACH-MANH`, hai tệp bundled, sha256 đặc tả đã đóng băng, và trần đã nâng.

## 2. `ngoai_pham_vi`

- Không đổi ngưỡng, waiver hay vị từ của `_py_size_findings`; không sửa `r125_*`. Trong `scripts/tl_selftest.py` CHỈ được đổi hai chỗ ghim `== 185` → `== 186` của `r291_docs_ngoai_goi` / `r357_agents_ngoai_goi` và thêm một dòng KÊ KHAI SLOT cho mỗi ca (M9); không chạm ca nào khác.
- Không sửa `.github/checks/bundle_fragment_check.py`, `scripts/tl.py`, `_RELEASE_REQUIRED_FILES` (chỉ tệp chính là bắt buộc; mảnh được `test-fragments-check`
  canh), `.claude/dev/gate_lifecycle.py` (đề xuất nợ riêng nếu muốn băm cả mảnh), tài liệu `references/COMMANDS.md` / `docs/**` / ADR (nợ tài liệu riêng:
  `bundled-tach-manh-tai-lieu`).
- Không đổi thứ tự, nội dung hay số fragment hiện có.

## 3. `muc_tieu` (nguyên văn nguyên mẫu ở `ops/reviews/bundled-tach-manh-spec-r1/nguyen-mau.diff`)

| # | mục tiêu | tệp |
|---|---|---|
| M1 | **Sinh mảnh.** `generate_bundled_modules(root) -> tuple[(tên, bytes), …]`: xếp fragment theo thứ tự ổn định hiện có, gom tham lam, mảnh mới khi tổng byte dòng nguồn vượt `_BUNDLED_SHARD_LIMIT` **192 KiB = 196.608 B ≈ 68,6% WARN (Q3, chủ kho chốt 2026-11-20)** (một fragment đơn lớn hơn hạn vẫn đứng riêng một mảnh). Mảnh 1 tên `tl_test_fragments_bundled.py`; mảnh k≥2 tên `tl_test_fragments_bundled_<k>.py`. Khi >1 mảnh, mảnh 1 thêm đúng MỘT phép gán `BUNDLED_FRAGMENT_SHARDS = ("tl_test_fragments_bundled_2.py", …)` sau `BUNDLED_FRAGMENT_SOURCES`; khi 1 mảnh, byte Y HỆT `generate_bundled_module_bytes` hiện nay. `generate_bundled_module_bytes(root)` giữ chữ ký, trả bytes mảnh 1. `write_bundled_modules(root, scripts_dir)` ghi mọi mảnh và XOÁ mảnh đánh số lạc; là đường tái sinh duy nhất được phép. | `test_fragments.py` |
| M2 | **Nạp mảnh.** `_read_bundled_sources(primary)` đọc mảnh 1 rồi ĐÚNG các mảnh mảnh 1 khai trong `BUNDLED_FRAGMENT_SHARDS`, theo thứ tự khai; tệp đánh số không khai thì KHÔNG nạp. Hợp đồng mỗi mảnh vẫn data-only: mảnh 1 cho phép `[SOURCES]` hoặc `[SOURCES, SHARDS]`; mảnh k≥2 chỉ `[SOURCES]`. Danh sách khai phải là `("…_2.py", …, "…_N.py")` liên tục, không rỗng. Thứ tự và tính duy nhất (NFC+casefold) kiểm XUYÊN mảnh. Mảnh khai mà thiếu ⇒ `BUNDLED_MODULE_MISSING` (mã lỗi giữ nguyên, kèm đường mảnh). | `test_fragments.py` |
| M3 | **Cổng `test-fragments-check`.** So từng mảnh kỳ vọng theo byte, cộng phát hiện tệp `tl_test_fragments_bundled_<k>.py` lạc trên đĩa (`extra_shards`) ⇒ `GENERATED_BUNDLE_STALE`. Thiếu mảnh 1 ⇒ `BUNDLED_MODULE_MISSING` như nay. Một mảnh: `expected_sha256`/`actual_sha256`/`*_bytes` giữ nguyên nghĩa (băm tệp). Nhiều mảnh: băm trên chuỗi `tên\0bytes` nối theo thứ tự. Thêm khoá `shards`. | `release.py` |
| M4 | `eol_policy_test.py`: hai chỗ ghi bundled từ fragment thật (`_tai_sinh_bundled`, ca driver) đổi sang `write_bundled_modules`. | `.githooks/eol_policy_test.py` |
| M5 | Golden `workflow_audit.json`: `files_scanned` 73 → 74; không khoá nào khác đổi (`golden-test` ok). | golden |
| M6 | Fragment `wp433_bundled_tach_manh.py`, 10 nhãn P1–P10 (§4), tính đủ trên mọi đường. Fragment KHÔNG được văng ngoại lệ dưới đột biến: mọi chỉ số/độ dài phải chốt trước khi dùng (đột biến c lần đầu văng `IndexError` ⇒ tín dụng giả; đã thêm chốt). | fragment |
| M7 | Tái sinh bằng `write_bundled_modules`; ra đúng hai mảnh trên base (mảnh 1 ≈ 189 KB, mảnh 2 ≈ 102 KB). | bundled |
| M8 | **Land Operator** (không phải worker — protocol §9) tái sinh `RELEASE_MANIFEST.json` bằng `python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json` thành commit riêng, tạo C theo §3a điểm 2 (Q5). | manifest |
| M9 | `scripts/tl_selftest.py`: hai ca ghim số tệp manifest đổi `185` → `186` và thêm dòng `# KÊ KHAI SLOT (BUNDLED-TACH-MANH): 185 → **186** = + scripts/tl_test_fragments_bundled_2.py. Trần Package 200 (ZIP 187 entry).` cho mỗi ca (Q6). | `tl_selftest.py` |

## 3a. Luồng candidate — KHÔNG chép lại protocol, chỉ ghi phần riêng của packet

Thứ tự, handoff, review offline, push, PR, push thêm và stop condition theo đúng protocol §13 `work-packet`, ADR-0060 M5/M12
và §12 (bất biến (a)/(b), tín hiệu không hội tụ, checkpoint). Đặc tả này không diễn đạt lại các luật ấy; chỗ nào lệch là đặc
tả sai. Phần RIÊNG của packet này chỉ gồm ba điểm, vì protocol §9 cấm worker sửa manifest:

1. Worker commit 8 tệp write set CỤC BỘ, không push, và giao cho Land Operator bằng `git format-patch` các tệp không sinh tự
   động + lệnh tái sinh + tree worker + số đo chuẩn bị (đo trên cây worker với manifest tái sinh không commit). Đây là đầu
   vào của Land Operator, chưa phải handoff M12.
2. Land Operator dựng lại commit worker trên base (giữ author), đối chiếu tree với tree worker đã khai (lệch ⇒ DỪNG), rồi
   thêm commit M8. SHA kết quả là SHA ứng viên cục bộ C của ADR-0060 M12; MỌI phép đo nghiệm thu chính thức (N1–N4) chạy
   trên C hoặc bản sao của C, và handoff M12 neo C.
3. **Land Operator giữ C** từ điểm 2 tới khi PR draft mở: LO chạy bất biến (a) và N1–N4 trên C, dựng bundle C, đăng handoff
   §7 lên #433 với `head_sha == tested_sha == C`, nhận verdict, rồi đẩy C đúng một lần và đối chiếu PR head theo ADR-0060
   M5/M12. Worker không push và không giữ vai nào trên C.
4. Vá sau review: tệp write set do worker vá (lại qua điểm 1), Land Operator tái sinh M8 ⇒ C mới, đo lại N1–N4 trên C mới.

## 4. `nghiem_thu`

Từ r4, đặc tả quy định TÍNH CHẤT phải đo và HÌNH DẠNG phép đo; fixture, tên nhãn cụ thể và danh sách đột biến là sản phẩm
của worker, được review trên C (nơi chạy được), không đóng băng bằng văn xuôi ở đây (lý do: §9, checkpoint lượt 9).

**Tính chất P1–P10** (mỗi tính chất là một nhãn của fragment):

| # | tính chất |
|---|---|
| P1 | Một mảnh: fixture nhỏ ⇒ đúng 1 mảnh, không phép gán `BUNDLED_FRAGMENT_SHARDS`; bytes của `generate_bundled_modules` lẫn `generate_bundled_module_bytes` có sha256 bằng hằng ghim trong fragment, hằng đo bằng `generate_bundled_module_bytes` trên base `0f9aa2a` cho CÙNG fixture. |
| P2 | Nhiều mảnh: hạn 100 KiB, 6 fragment × 40 KiB ⇒ đúng 3 mảnh nhóm `2+2+2`; giá trị tuple `BUNDLED_FRAGMENT_SHARDS` bằng `("tl_test_fragments_bundled_2.py", "tl_test_fragments_bundled_3.py")` (so GIÁ TRỊ, không so byte); nạp lại đủ, đúng thứ tự. |
| P3 | Loader chỉ nạp mảnh được khai; tệp đánh số không khai bị bỏ qua. |
| P4 | Cổng `test-fragments-check` báo tệp đánh số lạc: `GENERATED_BUNDLE_STALE`, `extra_shards` đúng danh sách. |
| P5 | `write_bundled_modules` xoá mảnh đánh số lạc. |
| P6 | Mảnh khai mà thiếu ⇒ `BUNDLED_MODULE_MISSING` và thông báo chứa đường của chính mảnh thiếu. |
| P7 | Thứ tự xuyên mảnh: fixture KHÔNG có tên trùng, đổi chỗ hai mảnh ⇒ `BUNDLED_MODULE_CONTRACT`. |
| P8 | Trùng xuyên mảnh: cùng một tên fragment (trùng NGUYÊN VĂN — hợp đồng tên `_FRAGMENT_NAME_RE` chỉ nhận ASCII thường nên đây là dạng trùng duy nhất tới được phép kiểm NFC+casefold) là phần tử cuối mảnh k và đầu mảnh k+1, thứ tự toàn chuỗi không giảm ⇒ `BUNDLED_MODULE_CONTRACT`. |
| P9 | Mảnh k≥2 mang `BUNDLED_FRAGMENT_SHARDS` ⇒ `BUNDLED_MODULE_CONTRACT`. |
| P10 | Kho thật: `_BUNDLED_SHARD_LIMIT == 196608`; mọi mảnh thật ≤ 0,7·WARN (200.704 B). |

| # | ca | tiêu chí | đỏ khi |
|---|---|---|---|
| N1 | fragment mới | Fragment có đúng một nhãn cho mỗi P1–P10 và TÍNH ĐỦ 10 nhãn trên mọi đường (dữ liệu chưa đủ ⇒ nhãn ấy False, không return sớm, không văng); `run()` True khi và chỉ khi cả 10 True. Trên C: `run()` True. | `run()` không True; HOẶC có nhãn không True; HOẶC số nhãn ≠ 10; HOẶC fragment có đường return trước khi tính đủ nhãn |
| N2 | ma trận đột biến | Worker nộp ma trận (đột biến → tập nhãn đích) cùng bàn giao, mỗi P1–P10 là đích của ≥1 đột biến chỉ phá đúng tính chất ấy. Trên C: mỗi đột biến làm `run()` False, không văng, và tập nhãn đỏ (trên đủ 10 khoá; khoá vắng tính là đỏ) BẰNG đúng tập đích đã khai. Reviewer trên C được thêm đột biến; đột biến thêm cũng phải thoả. | một tính chất không có đột biến đích; HOẶC đột biến sống; HOẶC chết do ngoại lệ; HOẶC tập đỏ ≠ tập đích khai |
| N3 | gate trên C (§3a điểm 2), clone đầy đủ | selftest N/N hai số bằng nhau, N = N_base + 1 (base 1784, nguyên mẫu 1785); `test-fragments-check` `ok: true` hai mảnh; `bundle_fragment_check` `ok: true`, `failed: []`, `case_count` 19; `release-verify RELEASE_MANIFEST.json --strict --json` trên CHÍNH tệp đã commit: `ok: true`, `expected == checked` = 186 (lane LAND; chốt land chỉ trên SHA thoả vế này); `workflow-audit --strict --json` rc 0, `ok: true`, `py_size.fail == []`, `py_size.warn == []`, `py_size.files_scanned == 74`; `golden-test` ok; `.githooks/eol_policy_test.py` 32/32 (trên cây ĐÃ commit); ruff F delta 0; `git diff --check`, `doctrine-scan`, `adr-song` rc 0. | bất kỳ vế nào |
| N4 | phản chứng mục đích | Trên BẢN SAO của C, áp `scripts/test_fragments/wp433_secrets_set_bundle.py` + `scripts/tl_gws.py` lấy bằng `git show a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c:<đường>` (ghim OID, không dùng ref động) (không áp lên C), `write_bundled_modules`: `py_size.warn == []`, `test-fragments-check` ok, selftest N/N (đo nguyên mẫu: 1786/1786, mảnh 189.328 / 117.343 B). Không commit phần áp. | còn WARN; HOẶC `test-fragments-check` không phải rc 0 kèm `ok: true`; HOẶC selftest không phải rc 0 với số đạt = tổng |

### 4b. Đột biến tham khảo (KHÔNG phải tiêu chí; worker tự chốt ma trận ở N2)

Nguyên mẫu đã đo a–f (`dot-bien.txt`), Codex lượt 6 đo g, executor đo h, i. Dùng làm điểm xuất phát cho ma trận N2: a loader nạp mọi
tệp đánh số · b bỏ kiểm thứ tự xuyên mảnh · c generator bỏ hạn mảnh · d cổng bỏ `extra_shards` · e không xoá mảnh lạc · f mảnh k≥2
được phép mang SHARDS · g đổi một dòng chú thích đầu tệp sinh ra · h bỏ hẳn phép kiểm trùng TEST_ID ở loader · i
`_BUNDLED_SHARD_LIMIT` = 200000. Lưu ý: c phá cả P2 lẫn P10 (kho thật dồn một mảnh ~291 KB), nên tập đích của c phải khai cả hai.

### 4c. Đo native Windows

**MIỄN (Q4, chủ kho chốt 2026-11-20).** Mã chỉ là `pathlib` iterdir/write/unlink và AST/JSON; không API riêng nền, không ký tự đường đặc biệt. Không có lượt D1; ngân sách Windows của lease = 0.

## 5. `pham_vi_e`

Không chạm E4/E5: thư mục tạm, không mạng, không LIVE, không đẩy Package.

## 6. `luat_dung`

- Trần lời gọi Codex theo ADR-0055; sau khi chủ kho xác nhận ở E2, trần kích thước theo khối `nang_tran` §1 — tối đa 9 đường (worker 8 + Land Operator 1), 450 dòng thêm theo numstat thật; vượt ⇒ DỪNG.
- `release-verify RELEASE_MANIFEST.json --strict` trên SHA ứng viên không `ok: true` ⇒ không trình land.
- §0 lệch trên base thật (kích thước bundled, `files_scanned`, các điểm chạm) ⇒ DỪNG, revision.
- Trên C (chưa áp N4): một mảnh bất kỳ > 0,7·WARN, hoặc `write_bundled_modules` sinh số mảnh ≠ 2 ⇒ DỪNG, báo (Q3 sai giả định).
- Số đo chuẩn bị của worker và N3 trên C: bất kỳ ca selftest nào khác ngoài +1 ca mới đổi trạng thái ⇒ DỪNG. Mọi stop condition khác theo protocol §12.
- Đo trên clone nông ⇒ KHÔNG ĐO ĐƯỢC cho N3, không được báo đạt.
- Chưa có comment ngoại lệ bundled đúng `packet_id` + trần nâng ⇒ không cấp lease (**E2**). Đặc tả chờ chủ kho duyệt băm (ADR-0067, **E2**).

## 7. `hinh_dang_ke_thua` và hệ quả cho packet khác

- **Ranh mảnh trôi:** gom tham lam theo thứ tự tên ⇒ thêm một fragment ở giữa thứ tự có thể đẩy fragment sang mảnh sau, đổi CẢ HAI tệp. Vì vậy từ packet này,
  mọi packet thêm/sửa fragment phải khai write set gồm MỌI tệp `scripts/tl_test_fragments_bundled*.py` (kể cả mảnh mới có thể sinh), và ngoại lệ bundled phải
  nêu cả nhóm tệp, sinh bằng `write_bundled_modules` (không còn `generate_bundled_module_bytes`).
- **SECRETS-SET-BUNDLE-KIEU cần revision r2 sau khi packet này land:** fragment `wp433_secrets_set_bundle.py` rơi vào mảnh 2 (đo N4) ⇒ write set thêm
  `scripts/tl_test_fragments_bundled_2.py` (4 tệp worker) cộng `RELEASE_MANIFEST.json` do Land Operator tái sinh trong candidate (5 đường; thiếu ⇒ strict verify rc 2, reviewer lượt 2 đo), ngoại lệ bundled mới, lease mới; nội dung ghim tại `a8a3b3c` phải đặt lên master mới rồi tái sinh bằng
  `write_bundled_modules`, theo cùng luồng candidate §3a. Mã `tl_gws.py` và fragment của nó (ghim `a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c`) không đổi.

## 8. `chua_do_duoc` và dự toán

- Numstat nguyên mẫu (đo, base `0f9aa2a`, bundled tái sinh bằng `write_bundled_modules`): `eol_policy_test.py` 2/4 · golden 1/1 · fragment mới 130/0 ·
  `release.py` 22/5 · `test_fragments.py` 90/26 · `tl_test_fragments_bundled.py` 2/9 · `tl_test_fragments_bundled_2.py` 14/0 ⇒ **7 tệp, 261 dòng thêm, 45 xoá**.
- Chưa đo: Windows (miễn theo Q4); CI GitHub thật. Đã đo (review lượt 3, base `0f9aa2a`): 7 đường nguyên mẫu +261/−45 · M9 `tl_selftest.py` +4/−2 · manifest +18/−13 ⇒ **9 đường +283/−60** (trần 450).

## 9. Lịch sử và quyết định

- Chủ kho 2026-11-20: secrets-set bị chặn bởi WARN bundled ⇒ chọn "Tách bundled trước" (không nâng ngưỡng, không waiver, không đưa test ra ngoài bundle).
- Chủ kho 2026-11-20 chốt Q1–Q4 theo khuyến nghị: #433 · nâng trần ADR-0053 lên 7 tệp/450 dòng · hạn mảnh 192 KiB · miễn đo Windows. Yêu cầu Codex review đặc tả trước khi duyệt băm.
- Chủ kho 2026-11-20, sau Codex lượt 1 (P1 manifest): Q5 — đưa `RELEASE_MANIFEST.json` vào packet, trần 8 tệp / 450 dòng; bỏ PR manifest riêng sau land.
- Sau Codex lượt 2 (P1 hai ca selftest ghim 185): Q6 — thêm `scripts/tl_selftest.py` vào write set worker (M9); manifest do Land Operator commit (M8, protocol §9). Candidate 9 đường / 450 dòng: CHỜ chủ kho xác nhận khi duyệt băm.

- 2026-11-20 (điều phối #1206, §12 checkpoint, mục sổ 7046243035): 6 verdict lượt 1–6 thiếu `class_slug`/bảng lớp ⇒ không dùng để approve; r1 không đóng băng hợp lệ. Lượt 7 theo §8.3 (run `090feb0c`, request_changes) xác định 3 lớp còn mở. Hướng mới: r2 vá CHUNG theo lớp thay vì từng finding.

### Bảng lớp r2 (vá chung) — giữ làm lịch sử

| class_slug | biểu hiện lượt 7 | cách vá chung ở r2 | phép kiểm đóng lớp |
|---|---|---|---|
| `manifest-gan-candidate` | L7-01a/b | một mục §3a duy nhất quy định thứ tự worker → candidate cục bộ → bất biến (a) → review offline → push một lần; M8, N3, §6, §7 chỉ trỏ về §3a | đọc toàn đặc tả: không còn câu nào cho push/PR/review trước bước 5 §3a hay cho worker head đỏ lên GitHub |
| `tieu-chi-khong-the-do` | L7-02a–e | mọi hàng N có cột "đỏ khi" liệt kê MỌI vế của cột tiêu chí; thêm nhãn `trung_xuyen_manh` + đột biến h; ghim `2+2+2`, hằng 196608, đường mảnh thiếu; N3 thêm `workflow-audit --strict` | với từng hàng N: mỗi vế tiêu chí có một vế "đỏ khi" tương ứng; mỗi nhãn N1 có ≥1 đột biến đích |
| `dau-vao-phan-chung-khong-ghim` | L7-03 | mọi đầu vào ngoài cây (N4, §7, README) ghim OID `a8a3b3ca…`, không ref động | ngoài chính dòng này, đặc tả + README không còn tham chiếu nào tới ref nhánh `agent/…` của secrets-set; mọi chỗ dùng OID |

- Codex lượt 8 (run `cd8375fc`, request_changes): tỷ lệ 7→8 = 1/3; `dau-vao-phan-chung-khong-ghim` ĐÃ VÁ THẬT; hai lớp VÁ MỘT PHẦN. Xét lại cách làm (§12, lớp `manifest-gan-candidate` chạm lần ba): nguyên nhân là đặc tả DIỄN ĐẠT LẠI luồng protocol nên mỗi lượt lộ một chỗ lệch mới (M12 handoff, stop condition). r3 bỏ diễn đạt lại, §3a chỉ trỏ protocol và giữ ba điểm riêng. Lượt 9 nếu tỷ lệ 8→9 < 50% ⇒ dừng vòng vá (hai chuyển tiếp liền), đưa về Review Rescue Checkpoint.

### Bảng lớp r3 (vá chung)

| class_slug | biểu hiện lượt 8 | cách vá chung ở r3 | phép kiểm đóng lớp |
|---|---|---|---|
| `manifest-gan-candidate` | L8-01a/b/c | §3a không diễn đạt lại protocol; trỏ §13 `work-packet`, ADR-0060 M5/M12, §12; chỉ giữ 3 điểm riêng (đầu vào LO, C là SHA ứng viên M12 và mọi N đo trên C, vá ⇒ C mới) | đọc toàn đặc tả: không câu nào quy định handoff/push/PR/review/stop khác hoặc thay protocol; mọi phép đo nghiệm thu chính thức neo C |
| `tieu-chi-khong-the-do` | L8-02a–d | mỗi nhãn N1 có ≥1 đột biến đích riêng (thêm i cho `kho_that`); fixture thứ tự và fixture trùng tách nhau; khoá JSON N3 viết đúng đường `py_size.*`; điều kiện dừng số mảnh đo trên C | bảng ánh xạ nhãn→đột biến phủ 9/9; mỗi khoá JSON trong N3 tồn tại ở đúng đường trong `references/golden/workflow_audit.json`; không điều kiện dừng nào đúng trên base theo nghĩa đen |

- Lượt 9 (reviewer Claude độc lập, cùng họ, không tính vào trần Codex; theo §8.3; request_changes): tỷ lệ 8→9 = 0/2 ⇒ **hai chuyển tiếp liền < 50%** ⇒ dừng vòng vá, Review Rescue Checkpoint (§12, ADR-0037). Phân tích: lớp `tieu-chi-khong-the-do` tái phát vì đặc tả đóng băng bằng VĂN XUÔI những thứ chỉ đo được trên mã (fixture, nhãn, ma trận đột biến), nên reviewer đặc tả chỉ đọc chữ và mỗi lượt lộ một khe mới (L9-02 fixture không dựng được — executor đo xác nhận; L9-03 return sớm; L9-04 vế chưa có đột biến). Lớp `manifest-gan-candidate` còn đúng một khe: chưa giao vai giữ C (L9-01). Không phải E1: có hướng mới có phép đo chống đỡ (executor đã chạy ma trận 9/9 trên cây cục bộ). Hướng mới (r4): đặc tả chỉ quy định tính chất P1–P10 + hình dạng N1/N2 (tính đủ nhãn, ma trận đích khai trước, khoá vắng là đỏ); chi tiết fixture/đột biến review trên C. LO giữ C (§3a điểm 3). Ghi sổ `xet_lai_cach_lam`.

### Bảng lớp r4 (vá chung)

| class_slug | biểu hiện lượt 9 | cách vá chung ở r4 | phép kiểm đóng lớp |
|---|---|---|---|
| `manifest-gan-candidate` | L9-01 | §3a điểm 3: một vai (LO) giữ C cho mọi hành động §13 `work-packet` trên C | mỗi hành động trên C (cổng (a), handoff, review, push, đối chiếu PR head) có đúng một chủ thể |
| `tieu-chi-khong-the-do` | L9-02, L9-03, L9-04 | chuyển từ đóng băng fixture/đột biến bằng văn xuôi sang tính chất P1–P10 + ma trận đột biến khai trước đo trên C; N1 đòi tính đủ nhãn; P8 dùng trùng nguyên văn | mỗi P có ≥1 đột biến chỉ phá P đó, đo trên C với khoá vắng là đỏ; không tiêu chí nào đòi fixture không dựng được với regex hiện hành |
| `so-do-loi-thoi` (tái mở) | L9-05 | §0 sửa: hai ca đọc manifest trên cây làm việc | câu §0 khớp `mf = root / "RELEASE_MANIFEST.json"` |

## 10. Nhật ký revision

- 2026-11-20T15:1xZ (phiên con của điều phối #1206): bản 1, đo §0 và nguyên mẫu trên clone đầy đủ `0f9aa2a` (Linux).
- 2026-11-20 (điều phối #1206): ghi quyết định Q1–Q4 của chủ kho; chưa đổi nội dung kỹ thuật.
- 2026-11-20 (điều phối #1206): sửa theo Codex lượt 1 (run `402df797`, request_changes): P1 manifest vào packet (Q5, M8, N3) · P2 khối `nang_tran` · P2 N4 đỏ đủ ba vế · P3 đếm entry ZIP 186→187 · P3 số đo §0/N4.
- 2026-11-20 (điều phối #1206): sửa theo Codex lượt 2 (run `1e18f41a`, request_changes): P1 `tl_selftest.py` vào write set (Q6, M9) · P2 manifest do Land Operator (M8) · P2 §7 secrets-set 5 đường · P3 README.
- 2026-11-20 (điều phối #1206): sửa theo Codex lượt 3 (run `c2cd2a0c`, request_changes): P1 commit manifest TRƯỚC đóng băng candidate (M8) · P2 §6 trần 9 đường · P3 numstat đo lại +283/−60.
- 2026-11-20 (điều phối #1206): sửa theo Codex lượt 4 (run `5d47c36d`, request_changes): P2 §6 ngoại lệ hai ca M9 trước M8 · P3 §0 năm tệp trong manifest.
- 2026-11-20 (điều phối #1206): sửa theo Codex lượt 5 (run `ee85d37a`, request_changes): P2 `mot_manh` neo sha256 ghim từ base, thêm đột biến g (N2 7/7). Đột biến g chưa đo trên nguyên mẫu — executor đo.
- 2026-11-20 (điều phối #1206): Codex lượt 6 (run `c19b4c3d`) **approve** trên sha256 `9fb430e2…`; sửa P3 duy nhất (tiêu đề §4b). Hằng ghim đo được cho fixture `wp9001_a.py` (216 B) trên base: `73ad44659b63aea9b2f66fb1104c4c82deaa1ad1218e94adb80dcf38384441d7`.
- 2026-11-20 (điều phối #1206): **r2** từ r1 `e38cc986`: vá chung ba lớp của Codex lượt 7 (bảng lớp §9). Không đổi Q1–Q6, write set, trần.
- 2026-11-20 (điều phối #1206): **r3** từ r2 `420b125f`: vá chung hai lớp còn mở của Codex lượt 8 (bảng lớp r3 §9). Không đổi Q1–Q6, write set, trần.
- 2026-11-20 (điều phối #1206): **r4** từ r3 `305e04fc` sau Review Rescue Checkpoint lượt 9: đổi cách đặc tả nghiệm thu (tính chất + ma trận đột biến trên C), LO giữ C, sửa §0. Không đổi Q1–Q6, write set, trần.
