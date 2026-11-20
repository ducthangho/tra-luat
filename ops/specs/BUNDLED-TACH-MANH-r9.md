tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

```yaml
nang_tran_loi_goi_codex_dac_ta:
  truc: codex_review_calls_dac_ta
  ai_nang: ducthangho
  tran_cu: 10
  tran_moi: 14
  can_cu: 'Chu kho 2026-11-20 (phien dieu phoi #1206, E2 sau luot 10/10 request_changes con 6 bieu hien P2 lop tieu-chi-khong-the-do): "Cap them luot Codex", "+4 luot" (Q8). Khong ap cho ngan sach Codex review PR (10, rieng).'
```

# BUNDLED-TACH-MANH r9 — tách `scripts/tl_test_fragments_bundled.py` thành nhiều mảnh dưới ngưỡng WARN, GIỮ NGUYÊN bộ canh kích thước

- packet_id: BUNDLED-TACH-MANH; revision: 9; thay r8 (`9fb283ce`), r7 (`07a9123c`), r6 (`e82c1197`), r5 (`291a17c6`), r4 (`324bf4ac`), r3 (`305e04fc`), r2 (`420b125f`) và r1 (`e38cc986`, chưa đóng băng hợp lệ — mục sổ https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7046243035).

| trường | giá trị |
|---|---|
| `packet_issue` | **#433** (Q1, chủ kho chốt 2026-11-20). Packet này mở để gỡ chặn packet SECRETS-SET-BUNDLE-KIEU của #433; TEST_ID fragment mới mang tiền tố `wp433_`. |
| `nguon_cap_viec` | Chủ kho 2026-11-20 (phiên điều phối #1206): "Tách bundled trước" — packet riêng, làm TRƯỚC secrets-set, giữ nguyên bộ canh (không nâng ngưỡng, không waiver). |
| `phu_thuoc` | Không. Chặn: SECRETS-SET-BUNDLE-KIEU (nội dung ghim tại commit `a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c`, đang giữ). |
| `review_class` | `sensitive`: chạm `scripts/tl_core/test_fragments.py` (hợp đồng nạp fragment, chạy trong gói phát hành) và `scripts/tl_core/release.py` (cổng `test-fragments-check` lane LAND). |
| `base` | `0f9aa2a2cc697129e1f5be72feddf60986286865`. Phiên thi hành đo lại §0 trên base thật của lease và DỪNG nếu lệch. Đo trên clone ĐẦY ĐỦ: clone nông làm `wp1099_nlm_nap_lai` đỏ giả (thiếu object `358451e8`). |

Các quyết định Q1–Q9 đã được chủ kho chốt 2026-11-20 (xem §9); mỗi chỗ ghi kèm nhãn Qn.

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
  - `RELEASE_MANIFEST.json` băm nội dung từng tệp gói: candidate đổi 5 tệp đã có trong manifest (`release.py`, `test_fragments.py`, `tl_selftest.py`, bundled mảnh 1, golden) và thêm mảnh 2; Executor tái sinh và commit manifest theo M8 làm commit cuối của SHA ứng viên (Q7) ⇒ nếu không tái sinh trong chính packet thì job `gate` (lane LAND `release-verify --strict`) trên master ĐỎ từ lúc merge tới lúc merge PR manifest. Đây là nếp các packet trước (đo: merge #1453 `00ee839` ⇒ run 44711337223 job `gate` failure, xanh lại sau #1454). Reviewer đo trên nguyên mẫu: `release-verify RELEASE_MANIFEST.json --strict` rc 2.

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
RELEASE_MANIFEST.json
```

`RELEASE_MANIFEST.json` nằm trong write set của EXECUTOR theo **ngoại lệ chủ kho Q7** (đối với protocol §9 "Worker không sửa
`RELEASE_MANIFEST.json`"), cùng hình thức ngoại lệ bundled: chỉ sinh bằng `python scripts/tl.py release-manifest --out
RELEASE_MANIFEST.json`, không sửa tay. Ngoại lệ chỉ áp cho packet này.

**Candidate 9 đường > trần 6 của ADR-0053 ⇒ nâng trần (Q2 + Q5 + Q6, chủ kho; E2), khối dưới chép nguyên vào lease.**
Không gộp được: golden phải đổi vì `files_scanned`; `eol_policy_test` phải đổi vì hai ca ghi bundled từ fragment thật; manifest phải đổi để master không đỏ
(Q5); `tl_selftest.py` phải đổi vì hai ca ghim số tệp manifest (Q6). Hai tệp bundled CHỈ sinh bằng `write_bundled_modules(scripts/test_fragments, scripts)`
(M1); `RELEASE_MANIFEST.json` CHỈ sinh bằng `python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json` (M8) — không sửa tay.

```yaml
nang_tran:
  truc: kich_thuoc_packet
  ai_nang: ducthangho
  tran_cu: '<= 6 tep, <= 450 dong them (ADR-0053, packet sensitive)'
  tran_moi: '<= 9 tep (gom RELEASE_MANIFEST.json theo ngoai le Q7), <= 450 dong them'
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
| M6 | Fragment `wp433_bundled_tach_manh.py`, 32 khoá V1–V32 (§4), tính đủ trên mọi đường. Fragment KHÔNG được văng ngoại lệ dưới đột biến: mọi chỉ số/độ dài phải chốt trước khi dùng (đột biến c lần đầu văng `IndexError` ⇒ tín dụng giả; đã thêm chốt). | fragment |
| M7 | Tái sinh bằng `write_bundled_modules`; ra đúng hai mảnh trên base (mảnh 1 ≈ 189 KB, mảnh 2 ≈ 102 KB). | bundled |
| M8 | **Executor** tái sinh `RELEASE_MANIFEST.json` bằng `python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json` thành commit cuối của SHA ứng viên (Q5, Q7; §3a). | manifest |
| M9 | `scripts/tl_selftest.py`: hai ca ghim số tệp manifest đổi `185` → `186` và thêm dòng `# KÊ KHAI SLOT (BUNDLED-TACH-MANH): 185 → **186** = + scripts/tl_test_fragments_bundled_2.py. Trần Package 200 (ZIP 187 entry).` cho mỗi ca (Q6). | `tl_selftest.py` |

## 3a. Luồng thi công

Theo đúng protocol §13 `work-packet`, ADR-0060 M5/M12 và §12; đặc tả không diễn đạt lại. Phần riêng duy nhất của packet
(Q7): commit CUỐI của mỗi SHA ứng viên là commit tái sinh `RELEASE_MANIFEST.json`, do chính Executor tạo bằng lệnh ở §1; mọi
commit vá về sau cũng kết thúc bằng một commit tái sinh manifest trước khi chạy bất biến (a). Không có vai Land Operator nào
trong thi công.

## 4. `nghiem_thu`

Đặc tả quy định các VẾ phải đo (V1–V32) và HÌNH DẠNG phép đo; fixture cụ thể và danh sách đột biến là sản phẩm của executor,
được review trên SHA ứng viên (nơi chạy được), không đóng băng bằng văn xuôi ở đây (lý do: §9, checkpoint lượt 9).

**Độ mịn nghiệm thu (Q9, chủ kho chốt 2026-11-20 theo E1):** V1–V32 dưới đây là TẬP NGHIỆM THU ĐỦ của packet. Chia mịn thêm (tách khoá gộp, thêm biên, thêm trường JSON) không phải điều kiện merge; reviewer trên SHA ứng viên nêu được thì ghi vào nợ có tên `bundled-tach-manh-do-min-ve` (mức P3), trừ khi nó chỉ ra một hành vi SAI của mã sản phẩm hay một phép đo XANH GIẢ — hai loại ấy vẫn là P0–P2.

**Quy tắc vế (từ r6):** (1) mỗi khoá V quan sát ĐÚNG MỘT hành vi — không khoá gộp;
(2) khoá quan sát đầu ra TRỰC TIẾP của chính thành phần (tên/bytes trả về của generator, tệp trên đĩa sau writer, mã lỗi của
loader, trường JSON của cổng), không suy qua thành phần khác; (3) fixture của loader và cổng dựng TAY, độc lập generator;
(4) mỗi khoá là đích của ≥1 đột biến chỉ phá đúng nó (N2).

**Vế kiểm V1–V32** — liệt kê đủ mọi vế hành vi của M1–M3 theo quy tắc trên; mỗi vế là một khoá của fragment:

| # | thành phần | vế |
|---|---|---|
| V1 | generator | Một mảnh: bytes `generate_bundled_modules` có sha256 bằng hằng ghim (đo bằng `generate_bundled_module_bytes` trên base `0f9aa2a` cho CÙNG fixture). |
| V2 | generator | Một mảnh: bytes `generate_bundled_module_bytes` có sha256 bằng cùng hằng ghim. |
| V3 | generator | Một mảnh: không có phép gán `BUNDLED_FRAGMENT_SHARDS` (AST). |
| V4 | generator | Đều: hạn 100 KiB, 6 fragment × 40 KiB ⇒ danh sách tên fragment theo mảnh đúng `[[1,2],[3,4],[5,6]]`. |
| V5 | generator | Đơn vị byte khi cắt mảnh: `len(dòng_tuple_đã_render.encode("utf-8")) + 1` (LF), cộng dồn theo thứ tự; KHÔNG tính header hay dòng khai SHARDS; mở mảnh mới khi `đã_dùng + size > hạn` và mảnh hiện tại không rỗng. Không đều: fixture kích thước khác nhau, có một vị trí tổng ĐÚNG BẰNG hạn (không mở mảnh mới) và một vị trí vượt hạn đúng 1 B (mở mảnh mới) ⇒ danh sách nhóm đúng kỳ vọng tính tay. |
| V6 | generator | Fragment đơn lớn hơn hạn đứng giữa hai fragment nhỏ ⇒ nó một mảnh riêng, hai hàng xóm không ghép vào. |
| V7 | generator | Tên tệp trả về của từng mảnh đúng `tl_test_fragments_bundled.py`, `…_2.py`, `…_3.py` theo thứ tự. |
| V8 | generator | Mảnh 1 (nhiều mảnh): thân module gồm ĐÚNG hai phép gán theo thứ tự `BUNDLED_FRAGMENT_SOURCES` rồi `BUNDLED_FRAGMENT_SHARDS` (AST). |
| V9 | generator | Giá trị tuple `BUNDLED_FRAGMENT_SHARDS` = `("tl_test_fragments_bundled_2.py", "tl_test_fragments_bundled_3.py")` (so GIÁ TRỊ). |
| V10 | generator | Nhiều mảnh: `generate_bundled_module_bytes` trả đúng bytes mảnh 1 của `generate_bundled_modules`. |
| V11 | writer | `write_bundled_modules` ghi đủ ba tệp với đúng tên và bytes bằng đầu ra generator (đọc lại từ đĩa). |
| V12 | writer | `write_bundled_modules` xoá tệp đánh số lạc (`_9`). |
| V13 | loader | Chỉ nạp mảnh được khai; tệp đánh số không khai bị bỏ qua. |
| V14 | loader | Mảnh khai mà thiếu ⇒ `BUNDLED_MODULE_MISSING`. |
| V15 | loader | Thông báo của V14 chứa đường của CHÍNH mảnh thiếu. |
| V16 | loader | Thứ tự xuyên mảnh (không tên trùng, đổi chỗ hai mảnh) ⇒ `BUNDLED_MODULE_CONTRACT`. |
| V17 | loader | Trùng xuyên mảnh: cùng tên NGUYÊN VĂN cuối mảnh k và đầu mảnh k+1, thứ tự không giảm ⇒ `BUNDLED_MODULE_CONTRACT`. |
| V18 | loader | Mảnh k≥2 mang `BUNDLED_FRAGMENT_SHARDS` ⇒ `BUNDLED_MODULE_CONTRACT`. |
| V19 | loader | `BUNDLED_FRAGMENT_SHARDS` rỗng ⇒ `BUNDLED_MODULE_CONTRACT`. |
| V20 | loader | `BUNDLED_FRAGMENT_SHARDS` không liên tục (`("…_3.py",)`) ⇒ `BUNDLED_MODULE_CONTRACT`. |
| V21 | loader | Mảnh 1 có thêm một câu lệnh/phép gán ngoài hai phép gán cho phép ⇒ `BUNDLED_MODULE_CONTRACT`. |
| V22 | loader | Mảnh k≥2 có thêm một câu lệnh/phép gán ngoài `BUNDLED_FRAGMENT_SOURCES` ⇒ `BUNDLED_MODULE_CONTRACT`. |
| V23 | cổng | Tệp đánh số lạc ⇒ `GENERATED_BUNDLE_STALE`, `extra_shards` đúng danh sách. |
| V24 | cổng | Sửa bytes một mảnh phụ ⇒ `GENERATED_BUNDLE_STALE`. |
| V25 | cổng | Thiếu mảnh phụ trên đĩa ⇒ `GENERATED_BUNDLE_STALE`, mục `shards` tương ứng `actual_bytes: null`. |
| V26 | cổng | Thiếu mảnh 1 ⇒ `BUNDLED_MODULE_MISSING`. |
| V27 | cổng | Một mảnh: `expected_sha256`/`actual_sha256`/`expected_bytes`/`actual_bytes` là băm và độ dài của TỆP mảnh 1 (tính độc lập trong fragment). |
| V28 | cổng | Nhiều mảnh: `expected_sha256` và `actual_sha256` = sha256 chuỗi `tên\0bytes` nối theo thứ tự (tính độc lập); `expected_bytes`/`actual_bytes` = độ dài CỦA CHÍNH chuỗi ấy (gồm tên UTF-8 và byte NUL), khớp `nguyen-mau.diff` dòng 215–216. |
| V29 | cổng | Nhiều mảnh: `shards` liệt kê đúng tên theo thứ tự, mỗi mục `expected_bytes`/`actual_bytes` đúng độ dài từng mảnh. |
| V30 | kho thật | `_BUNDLED_SHARD_LIMIT == 196608`. |
| V31 | kho thật | Mọi mảnh thật ≤ 0,7·WARN (200.704 B). Topology DEV (có `scripts/test_fragments/`): đo trên bytes `generate_bundled_modules` sinh từ thư mục fragment thật VÀ trên các tệp mảnh trên đĩa. Topology BUNDLE (gói giải nén, không có `scripts/test_fragments/` theo thiết kế): đo trên các tệp mảnh trên đĩa của gói (mảnh 1 và mọi mảnh nó khai). Ở cả hai topology, tệp mảnh cần đo mà thiếu hay không đọc được ⇒ khoá False. |
| V32 | loader, cổng, writer | Tên mảnh (mảnh 1 và mọi mảnh khai/đánh số) là symlink ⇒ loader trả `BUNDLED_MODULE_CONTRACT`, cổng không `ok` (không đọc qua symlink), writer không ghi xuyên symlink (đích symlink giữ nguyên bytes) — nhất quán với chốt từ chối symlink sẵn có của thư mục fragment (`test_fragments.py` base dòng 194). Fixture dựng symlink trong thư mục tạm; nền không tạo được symlink ⇒ khoá False kèm lý do, không xanh. |

| # | ca | tiêu chí | đỏ khi |
|---|---|---|---|
| N1 | fragment mới | Fragment có đúng một khoá cho mỗi V1–V32 và TÍNH ĐỦ 32 khoá trên mọi đường (hàm đo của một vế văng ⇒ khoá ấy False, các khoá sau vẫn tính; không return sớm); `run()` True khi và chỉ khi đủ 32 khoá và cả 32 True. Trên SHA ứng viên: `run()` True. | `run()` không True; HOẶC có khoá không True; HOẶC số khoá ≠ 32; HOẶC có đường return trước khi tính đủ khoá |
| N2 | ma trận đột biến | Mỗi đột biến chạy trong một tiến trình MỚI trên bản sao cây đã áp đột biến, đọc ĐÚNG bản đồ khoá do lời gọi `run()` của chính tiến trình ấy trả (không dùng kết quả lần gọi trước). Đột biến phá nhiều vế (vd c) khai ĐỦ tập đích; đột biến đích của một vế phải giữ nguyên tiền điều kiện của các khoá ngoài tập đích. Executor nộp ma trận (đột biến → tập khoá đích) trong handoff; mỗi V1–V32 là đích của ≥1 đột biến chỉ phá đúng vế ấy. Trên SHA ứng viên: mỗi đột biến làm `run()` False, không văng, trả ĐỦ 32 khoá, và tập khoá False BẰNG đúng tập đích đã khai. Reviewer được thêm đột biến; đột biến thêm cũng phải thoả. | một vế không có đột biến đích; HOẶC đột biến sống; HOẶC chết do ngoại lệ; HOẶC thiếu khoá trong kết quả; HOẶC tập False ≠ tập đích khai |
| N3 | gate trên SHA ứng viên (commit cuối là manifest, §3a), clone đầy đủ | selftest N/N hai số bằng nhau, N = N_base + 1 (base 1784, nguyên mẫu 1785); `test-fragments-check` `ok: true` hai mảnh; `bundle_fragment_check` `ok: true`, `failed: []`, `case_count` 19; `release-verify RELEASE_MANIFEST.json --strict --json` trên CHÍNH tệp đã commit: `ok: true`, `expected_file_count == checked_file_count == 186` (lane LAND; chốt land chỉ trên SHA thoả vế này); `workflow-audit --strict --json` rc 0, `ok: true`, `py_size.fail == []`, `py_size.warn == []`, `py_size.files_scanned == 74`; `golden-test` ok; `.githooks/eol_policy_test.py` 32/32 (trên cây ĐÃ commit); ruff F delta 0; `git diff --check`, `doctrine-scan`, `adr-song` rc 0. | bất kỳ vế nào |
| N4 | phản chứng mục đích | Trên BẢN SAO của SHA ứng viên, áp `scripts/test_fragments/wp433_secrets_set_bundle.py` + `scripts/tl_gws.py` lấy bằng `git show a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c:<đường>` (ghim OID, không dùng ref động) (không áp lên SHA ứng viên), `write_bundled_modules`: `py_size.warn == []`, `test-fragments-check` ok, selftest N/N (đo nguyên mẫu: 1786/1786, mảnh 189.328 / 117.343 B). Không commit phần áp. | còn WARN; HOẶC `test-fragments-check` không phải rc 0 kèm `ok: true`; HOẶC selftest không phải rc 0 với số đạt = tổng |

### 4b. Đột biến tham khảo (KHÔNG phải tiêu chí; executor tự chốt ma trận ở N2)

Nguyên mẫu đã đo a–f (`dot-bien.txt`), Codex lượt 6 đo g, executor đo h, i. Dùng làm điểm xuất phát cho ma trận N2: a loader nạp mọi
tệp đánh số · b bỏ kiểm thứ tự xuyên mảnh · c generator bỏ hạn mảnh · d cổng bỏ `extra_shards` · e không xoá mảnh lạc · f mảnh k≥2
được phép mang SHARDS · g đổi một dòng chú thích đầu tệp sinh ra · h bỏ hẳn phép kiểm trùng TEST_ID ở loader · i
`_BUNDLED_SHARD_LIMIT` = 200000. Lưu ý: c phá các vế nhiều mảnh (V4–V10) lẫn V31 (kho thật dồn một mảnh ~291 KB), nên tập đích của c phải khai cả hai.

### 4c. Đo native Windows

**MIỄN (Q4, chủ kho chốt 2026-11-20).** Mã chỉ là `pathlib` iterdir/write/unlink và AST/JSON; không API riêng nền, không ký tự đường đặc biệt. Không có lượt D1; ngân sách Windows của lease = 0.

## 5. `pham_vi_e`

Không chạm E4/E5: thư mục tạm, không mạng, không LIVE, không đẩy Package.

## 6. `luat_dung`

- Trần lời gọi Codex đặc tả theo khối Q8 (14); trần Codex review PR theo ADR-0055 (10, riêng); sau khi chủ kho xác nhận ở E2, trần kích thước theo khối `nang_tran` §1 — tối đa 9 tệp, 450 dòng thêm theo numstat thật; vượt ⇒ DỪNG và hỏi chủ kho (E2) — không tự bớt vế V1–V32 (executor ước 32 khoá ≈ 480 dòng, CHƯA đo).
- `release-verify RELEASE_MANIFEST.json --strict` trên SHA ứng viên không `ok: true` ⇒ không trình land.
- §0 lệch trên base thật (kích thước bundled, `files_scanned`, các điểm chạm) ⇒ DỪNG, revision.
- Trên SHA ứng viên (chưa áp N4): một mảnh bất kỳ > 0,7·WARN, hoặc `write_bundled_modules` sinh số mảnh ≠ 2 ⇒ DỪNG, báo (Q3 sai giả định).
- N3 trên SHA ứng viên: bất kỳ ca selftest nào khác ngoài +1 ca mới đổi trạng thái ⇒ DỪNG. Mọi stop condition khác theo protocol §12.
- Đo trên clone nông ⇒ KHÔNG ĐO ĐƯỢC cho N3, không được báo đạt.
- Chưa có comment ngoại lệ bundled đúng `packet_id` + trần nâng ⇒ không cấp lease (**E2**). Đặc tả chờ chủ kho duyệt băm (ADR-0067, **E2**).

## 7. `hinh_dang_ke_thua` và hệ quả cho packet khác

- **Ranh mảnh trôi:** gom tham lam theo thứ tự tên ⇒ thêm một fragment ở giữa thứ tự có thể đẩy fragment sang mảnh sau, đổi CẢ HAI tệp. Vì vậy từ packet này,
  mọi packet thêm/sửa fragment phải khai write set gồm MỌI tệp `scripts/tl_test_fragments_bundled*.py` (kể cả mảnh mới có thể sinh), và ngoại lệ bundled phải
  nêu cả nhóm tệp, sinh bằng `write_bundled_modules` (không còn `generate_bundled_module_bytes`).
- **SECRETS-SET-BUNDLE-KIEU cần revision r2 sau khi packet này land:** fragment `wp433_secrets_set_bundle.py` rơi vào mảnh 2 (đo N4) ⇒ write set thêm
  `scripts/tl_test_fragments_bundled_2.py` (4 tệp worker) cộng `RELEASE_MANIFEST.json` (5 đường; cần ngoại lệ manifest riêng như Q7 hoặc luật chung, vì protocol §9; thiếu ⇒ strict verify rc 2, reviewer lượt 2 đo), ngoại lệ bundled mới, lease mới; nội dung ghim tại `a8a3b3c` phải đặt lên master mới rồi tái sinh bằng
  `write_bundled_modules`, theo cùng luồng §3a. Mã `tl_gws.py` và fragment của nó (ghim `a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c`) không đổi.

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

- Codex lượt 9 (run `b582efd8`, r4, request_changes): tỷ lệ 9→10 = 1/3; `so-do-loi-thoi` ĐÃ VÁ THẬT; hai lớp còn mở tái phát sau đổi cách làm ⇒ E1 + E2 (còn 1/10 lượt). Chủ kho 2026-11-20 chọn **Q7: ngoại lệ manifest cho executor** — gốc lớp `manifest-gan-candidate` là xung đột giữa protocol §9 (worker không sửa manifest) và Q5 (manifest trong candidate); mọi cách chia vai r1–r4 vấp §7/§12. Q7 bỏ vai Land Operator khỏi thi công, luồng về work-packet chuẩn. Lớp `tieu-chi-khong-the-do`: r5 liệt kê đủ từng vế M1–M3 thành V1–V17 (gồm L10-02a–d), N2 đòi đủ khoá; N3 sửa khoá `expected_file_count`/`checked_file_count` (L10-02e). Lượt Codex 10/10 cho r5; chưa approve thì chủ kho duyệt băm trực tiếp.

### Bảng lớp r5 (vá chung)

| class_slug | biểu hiện lượt 9 Codex | cách vá chung ở r5 | phép kiểm đóng lớp |
|---|---|---|---|
| `manifest-gan-candidate` | L10-01a/b | Q7: manifest vào write set executor; bỏ vai LO; §3a chỉ còn một câu riêng (commit cuối là manifest) | không câu nào giao hành động trên SHA ứng viên cho ai ngoài Executor/Reviewer theo protocol; không còn "Land Operator" trong phần hiệu lực |
| `tieu-chi-khong-the-do` | L10-02a–e | mỗi vế hành vi của M1–M3 thành một khoá V; N2 đòi đủ 17 khoá + đột biến chỉ phá đúng vế; khoá JSON N3 đúng tên mã | mỗi câu hành vi trong M1–M3 ánh xạ tới ≥1 V; mỗi khoá JSON trong N3 có trong mã (`release.py` dòng 940–941) |

- Codex lượt 10 (run `60f4ea0e`, r5, request_changes): tỷ lệ 9→10 = 1/2; `manifest-gan-candidate` ĐÃ VÁ THẬT (Q7). `tieu-chi-khong-the-do` VÁ MỘT PHẦN, 6 biểu hiện R5-01..06. Chủ kho (E2) cấp thêm 4 lượt Codex đặc tả (Q8, trần 10 → 14). Phân tích gốc lớp: danh sách vế viết theo "tính chất" nên mỗi lượt reviewer tìm được một hành vi con nằm trong khoá gộp hoặc quan sát qua thành phần khác. Vá chung r6: QUY TẮC VẾ (một khoá một hành vi, quan sát trực tiếp đầu ra của thành phần, fixture loader/cổng dựng tay) + liệt kê lại V1–V31 theo quy tắc ấy.

### Bảng lớp r6 (vá chung)

| class_slug | biểu hiện Codex lượt 10 | cách vá chung ở r6 | phép kiểm đóng lớp |
|---|---|---|---|
| `tieu-chi-khong-the-do` | R5-01 (V5, V6) · R5-02 (V7, V8) · R5-03 (V11) · R5-04 (V21, V22) · R5-05 (V25, V27–V29) · R5-06 (tách V1/V2, V14/V15, V26, V30/V31) | quy tắc vế bốn điểm áp cho MỌI khoá, không riêng sáu biểu hiện | mỗi khoá V có đúng một hành vi; mỗi câu hành vi M1–M3 ánh xạ ≥1 V quan sát trực tiếp; không khoá nào quan sát qua thành phần khác |

- Codex lượt 11 (run `54d28b05`, r6, request_changes): tỷ lệ 10→11 = 0/1; lớp `tieu-chi-khong-the-do` còn 7 biểu hiện R6-01..07, mỗi lượt đòi chia mịn thêm (10 → 17 → 31 → ~45 khoá) sau ba lần đổi cách làm (r4, r5, r6) ⇒ E1. Chủ kho 2026-11-20 chọn **Q9: chốt độ mịn** — V1–V31 là tập nghiệm thu đủ; r7 chỉ vá ba lỗ đúng-sai: R6-07 (V31 thiếu đầu vào phải đỏ, không xanh giả), R6-01 (định nghĩa đơn vị byte cắt mảnh ở V5, khớp `nguyen-mau.diff` dòng 373–374), R6-06 (N2 đọc bản đồ của chính lần chạy, đột biến đa đích khai đủ, giữ tiền điều kiện). Phần còn lại R6-02..05 và các phần chia mịn của R6-01/R6-06 ghi thành nợ `bundled-tach-manh-do-min-ve` (P3). Chủ kho duyệt băm r7 trực tiếp, không thêm lượt Codex.

- Executor (lease g2, 18:46Z) đo được mâu thuẫn trong r7: V31 "thiếu thư mục fragment ⇒ False" làm `bundle_fragment_check` (N3) đỏ trên gói giải nén, vì gói loại `scripts/test_fragments/` theo thiết kế (bản sao dec3931: rc 1, failed [wp433_bundled_tach_manh]). Lỗi do chính bản vá R6-07 của r7 đưa vào (lớp `tieu-chi-khong-the-do`). r8 tách V31 theo topology: DEV đo generator + đĩa, BUNDLE đo tệp mảnh có trong gói; thiếu tệp mảnh cần đo vẫn False. Cùng lượt, V28 "tổng độ dài" mơ hồ: chốt theo nguyên mẫu (độ dài chuỗi `tên\0bytes`), không đổi mã `release.py`.

- Review offline lượt 1 trên SHA ứng viên `4e74fe1` (Codex, run `5ec3b197`, changes_requested; verdict `ops/reviews/bundled-tach-manh-cr/luot1-codex-4e74fe1.txt` @ `ba824e15`): bốn lớp P2. F01–F03 vá trong khoá hiện có. F04 `shard-symlink-follow` (loader/cổng/writer đi theo symlink tại tên mảnh; base đã có cho tệp bundled chính) — chủ kho 2026-11-21 chọn **vá luôn**: r9 thêm V32.

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
- 2026-11-20 (điều phối #1206): **r5** từ r4 `324bf4ac` theo Q7 của chủ kho (E1): ngoại lệ manifest cho executor, V1–V17, sửa khoá N3. Write set 9 tệp, trần không đổi.
- 2026-11-20 (điều phối #1206): **r6** từ r5 `291a17c6`: quy tắc vế + V1–V31 (R5-01..06), khối nâng trần lời gọi Codex đặc tả 10 → 14 (Q8). Write set, trần kích thước không đổi.
- 2026-11-20 (điều phối #1206): **r7** từ r6 `e82c1197` theo Q9 (E1): chốt độ mịn V1–V31, vá R6-07/R6-01/R6-06, nợ `bundled-tach-manh-do-min-ve`. Write set, trần kích thước không đổi.
- 2026-11-20 (điều phối #1206): **r8** từ r7 `07a9123c`: V31 tách topology DEV/BUNDLE (mâu thuẫn với N3 do executor đo), V28 chốt nghĩa độ dài theo nguyên mẫu. Không đổi gì khác.
- 2026-11-21 (điều phối #1206): **r9** từ r8 `9fb283ce`: thêm V32 (từ chối symlink tại tên mảnh ở loader/cổng/writer) theo chủ kho, sau F04 review offline lượt 1. Không đổi gì khác.
