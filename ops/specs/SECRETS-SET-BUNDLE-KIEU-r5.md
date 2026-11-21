tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# SECRETS-SET-BUNDLE-KIEU r5 — `secrets-set` dùng bundle giải mã mà chưa kiểm kiểu (nợ `wp433-secrets-set-bundle-khong-phai-dict`)

- packet_id: SECRETS-SET-BUNDLE-KIEU; revision: 5; thay r4 (`be0974f908ef9f45ece2055c6b113e9a7b837260404b5c83b1d94ccaf438f814`), r3 (`593b82a7ba2abb3b24159176a37445e41dc723efce9dfdaa009ff6f828257a18`), r2 (`22a1be3915168e82b164ed11f43834b595bbafc8223e4c66834f2ce02b852091`) và r1 (`477fb64757d03e9ce34b112ec507283e140d98a88fd16c2eefa3fe61ef88cfc1`).
- r1 CHƯA đóng băng hợp lệ: ba verdict Codex của r1 (`ops/reviews/wp433-secrets-set-spec-r1/rv/`) không có `class_slug` và bảng lớp (§8.3). Theo mục sổ
  https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7046243035 chúng không dùng để approve, nhưng vẫn tính vào trần lời gọi:
  **đã dùng 6/10** theo dòng `tran_loi_goi_codex` ở trên (lượt 4 là lượt §8.3 đầu tiên, trên r2; lượt 5 trên r3; lượt 6 trên r4).

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Nợ ghi ở §2 đặc tả `ops/specs/GWS-CRED-DICH-NGOAI-KHO-N-r2.md`. Chủ kho 2026-11-20: "Mở việc riêng cho Secret Set đi." Chủ kho 2026-11-21 (phiên điều phối #1206), sau khi BUNDLED-TACH-MANH land: làm ngay, executor Opus 5.5. |
| `phu_thuoc` | BUNDLED-TACH-MANH đã land (PR #1485, merge `96cd012`; hồ sơ land PR #1486, merge `1e397c8`). Packet N (PR #1441) và P2BW (PR #1453) đã land. |
| `review_class` | `sensitive`: `scripts/tl_gws.py` `_secrets_set_body` là đường GHI credential (bundle `tl_secrets.enc` và hai tệp public `.enc` trên Drive). |
| `base` | `1e397c89d69f451694a2252103ea97ec274ab43f` (origin/master lúc soạn; tree `b1b95b504e4a64cc6470dfed2081da6d778f4499`). Blob `scripts/tl_gws.py` `fbeb9421edd0a7e451534a92c89d090c4de4b3a4`, BẰNG blob ở `0f9aa2a` (base của r1): không commit nào từ `0f9aa2a` tới base chạm tệp này, nên mọi số dòng neo của r1 vẫn đúng. Phiên thi hành đo lại §0 trên base thật của lease; lệch thì DỪNG. |

Các mục **[ĐÃ CHỐT Qn]** là quyết định của chủ kho. Q1–Q2 giữ nguyên từ r1. Q3 (đo D1 Windows) được chủ kho THAY bằng **Q4'** (miễn D1) và thêm **Q5'** (chốt độ mịn) ngày 2026-11-21 theo E1 (§9). Muốn đổi thì phải ra revision mới.

## 0. Hiện trạng

### 0a. Hành vi `secrets-set` — giữ nguyên số đo r1

`tl_gws.py` trên base bằng từng byte bản r1 đã đo, nên số đo §0 của r1 vẫn đúng nguyên văn. Bằng chứng chạy được:
`ops/reviews/wp433-secrets-set-spec-r1/` (`tai_hien.py`, `tai-hien-linux.txt`, `nguyen-mau.diff`, `nguyen-mau-linux.txt`). Tóm tắt:

- **Luồng** (số dòng trên base):
  - `cmd_secrets_set` (992) bọc thân bằng `_nlm_contained` (913–922). Mọi ngoại lệ trong thân thành rc 5 kèm câu "Kiểm Drive trước khi coi là chưa upload gì".
  - `_secrets_set_body` (999) chạy `load_creds` rồi `_secrets_fetch` TRƯỚC khi giải mã (dòng 1007–1013). Nguồn bundle là `--secrets-file` (đọc tệp cục bộ) hoặc đường tải (dòng 678–694). Hai bước này KHÔNG thuộc phạm vi M1: bộ đếm `fetch` đo lời gọi tại ranh giới stub và bằng 1 ở mọi lượt.
  - Giải mã ở dòng 1014 (lỗi thì rc 3, dòng 1015–1017).
  - Sau đó lần lượt xử lý các cờ `--gas-token`, `--webapp`, `--gws`, `--nlm`. Riêng `--nlm` gọi `_refresh_nlm_auth` rồi chạy canary SỐNG.
  - Tiếp theo là upload, rồi đồng bộ public bằng khoá `_tok = os.environ.get("TL_TOKEN") or str(bundle.get("token") or "")` (1062).
- **(1) Bundle không phải object**, 25 lượt:
  - Có cờ: rc 5 kèm `✗ dừng vì lỗi TypeError …`. Upload 0, nhưng có tác dụng phụ trước khi vỡ: `--gws` chạy export; `--nlm` chạy refresh và **canary sống thừa**.
  - Không cờ: rc 1.
- **(2) Token không phải str, không có `TL_TOKEN`**, 6 lượt: rc 0, upload 1, và tệp public mã hoá bằng `repr` của giá trị làm khoá. Không có cảnh báo nào.
- **(3) Hồi quy**: bảng bộ đếm 6 lượt, chép nguyên ở §0(3) của r1.

### 0b. Đo trên base mới (2026-11-21T07:2x–07:3xZ, Linux)

Bằng chứng ở `ops/reviews/wp433-secrets-set-spec-r2/`.

**Cách dựng.** Một lệnh dựng hai clone đầy đủ (không shallow, có object `358451e8`) dưới `/dev/shm`, `core.abbrev 7`. Vế sau làm ba việc:
- áp hai tệp ghim `git show a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c:scripts/tl_gws.py` và `:scripts/test_fragments/wp433_secrets_set_bundle.py` (nhánh `agent/wp433-r8-g1-claude`);
- chạy `write_bundled_modules(scripts/test_fragments, scripts)`;
- chạy `tl.py release-manifest --out RELEASE_MANIFEST.json`. Cây kết quả có tree `8d23a5eabc6c0d419298a249a84c133bdc9afff2`. Commit cục bộ của lượt dựng KHÔNG được push, nên không dẫn chiếu OID commit; nguồn tái lập là diff nguyên mẫu `ops/reviews/wp433-secrets-set-spec-r2/nguyen-mau-tl_gws.diff` cộng hai tệp ghim. Codex lượt 4 dựng lại độc lập ra cùng tree (commit `1f2a969`, cũng không push).

| phép đo | base `1e397c8` | sau khi áp |
|---|---|---|
| mảnh (`test-fragments-check`) | 2 mảnh: 170.024 / 130.941 B, `ok: true` | 2 mảnh: 170.024 / **146.627** B, `ok: true`; fragment secrets-set rơi vào **mảnh 2**; mảnh 1 không đổi byte |
| `--selftest` | rc 0, 1785/1785 | rc 0, **1786/1786** |
| `bundle_fragment_check.py --json` | `ok: true`, `failed: []`, 19 ca | `ok: true`, `failed: []`, **20** ca |
| `release-verify RELEASE_MANIFEST.json --strict --json` (manifest đã commit) | `ok: true`, 186 == 186 | `ok: true`, 186 == 186 |
| `workflow-audit --strict --json` | `ok: true`, `py_size.fail []`, `py_size.warn []`, `files_scanned` 74 | như base |
| `golden-test --json` | rc 0 | rc 0 |
| ruff F (4 tệp `scripts/`) | 0 | 0; fragment: All checks passed |
| `doctrine-scan` | rc 0 | rc 0 |
| `.githooks/eol_policy_test.py` | 32/32 | 32/32 |

Thêm fragment không làm đổi số tệp trong manifest (186), vì gói loại `scripts/test_fragments/`. Do đó KHÔNG phải sửa hai ca ghim số tệp
(`r291_docs_ngoai_goi`, `r357_agents_ngoai_goi`) trong `tl_selftest.py`.

**Numstat `git diff --numstat 1e397c8 <commit cây 8d23a5ea>`:** 4 tệp, **+211/−8**.

| tệp | thêm/xoá |
|---|---|
| `RELEASE_MANIFEST.json` | 7/7 |
| fragment | 198/0 |
| `tl_gws.py` | 5/1 |
| `tl_test_fragments_bundled_2.py` | 1/0 |

## 1. `write_set`

```
RELEASE_MANIFEST.json
scripts/test_fragments/wp433_secrets_set_bundle.py
scripts/tl_gws.py
scripts/tl_test_fragments_bundled.py
scripts/tl_test_fragments_bundled_2.py
```

5 tệp, dưới trần 6 của ADR-0053. Dự toán ≤ 450 dòng thêm (§8), nên không cần `nang_tran`.

- **`tl_test_fragments_bundled.py`** trên số đo hiện KHÔNG đổi, nhưng vẫn phải khai. Theo §7 của đặc tả BUNDLED-TACH-MANH đã land, ranh mảnh có thể trôi, nên mọi packet đụng fragment khai cả nhóm `tl_test_fragments_bundled*.py`.
- **Hai tệp bundled** CHỈ được sinh bằng `write_bundled_modules(scripts/test_fragments, scripts)`. Không sửa tay. Không dùng `generate_bundled_module_bytes` để ghi tệp.
- **`RELEASE_MANIFEST.json`** được executor commit, theo ngoại lệ của chủ kho cùng hình thức Q7 của BUNDLED-TACH-MANH. Tệp CHỈ được sinh bằng `python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json` và là commit CUỐI của mỗi SHA ứng viên.

**Điều kiện cấp lease (E2):** chủ kho đăng comment trên #433 cấp ngoại lệ, nêu đúng:
- `packet_id` `SECRETS-SET-BUNDLE-KIEU`;
- hai tệp bundled và `RELEASE_MANIFEST.json` kèm điều kiện sinh;
- sha256 của đặc tả đã đóng băng.

Lease trỏ URL của comment đó.

## 2. `ngoai_pham_vi`

- **Câu "Kiểm Drive trước khi coi là chưa upload gì"** của `_nlm_contained` (dùng chung cho ba lệnh stage): giữ nguyên.
- **Ghi đè `token` sai kiểu** khi KHÔNG có `--gas-token`: giữ nguyên. Q2 = A chỉ bỏ phần đồng bộ public.
- **`secrets-stage`:** không thuộc nợ này.
- **Không sửa:** `ops/**`, `.github/**`, `scripts/tl_selftest.py`, fragment khác, `scripts/tl_core/**`, `changelog.d/*`, `VERSION`, `CHANGELOG.md`, `SKILL.md`.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | **[ĐÃ CHỐT Q1: rc 3, kiểm ngay]** Ngay sau khối `try/except` giải mã (sau dòng 1017 của base), TRƯỚC `changed = []` và trước mọi cờ: nếu `bundle` không phải `dict` thì in ĐÚNG một dòng stderr `[secrets-set] ✗ dữ liệu không hợp lệ: bundle` và trả **3**. Không gọi `_gws_export_cred`, `_refresh_nlm_auth`, canary, `encrypt` hay upload nào. Nguyên văn ở `ops/reviews/wp433-secrets-set-spec-r2/nguyen-mau-tl_gws.diff` (hunk 1). | `scripts/tl_gws.py` |
| M2 | **[ĐÃ CHỐT Q2: A, coi như thiếu]** Khoá public lấy `TL_TOKEN`. Nếu không có thì lấy `bundle.get("token")` CHỈ KHI giá trị là `str`, ngược lại dùng `""`. Khi đó luồng rơi vào nhánh cảnh báo SẴN CÓ "thiếu webapp token → KHÔNG đồng bộ được đường public": rc giữ nguyên, bundle vẫn upload. Nguyên văn ở cùng diff (hunk 2). | `scripts/tl_gws.py` |
| M3 | Fragment `wp433_secrets_set_bundle.py`, `TEST_ID = "wp433_secrets_set_bundle"`. Được phép bắt đầu từ bản ghim `a8a3b3ca…` nhưng phải thoả §4. Ràng buộc: nạp `tl_gws` trong bộ nhớ; HOME/TL_* tạm; dữ liệu giả; MỌI hàm tải/ghi/mạng thay bằng đồ giả có đếm (`_gas` giả ném lỗi); `encrypt` được bọc để ghi lại khoá; mọi đầu ra ra stderr; `run(tl)` trả True/False. | fragment |
| M4 | Tái sinh bundled bằng `write_bundled_modules`. | hai tệp bundled |
| M5 | Tái sinh `RELEASE_MANIFEST.json` thành commit CUỐI (§1). | manifest |

## 3a. Luồng thi công

Thi công theo đúng protocol §13 `work-packet`, ADR-0060 M5/M12 và §12. Đặc tả này không diễn đạt lại các luật đó; chỗ nào lệch thì đặc tả sai.
Phần riêng của packet chỉ có hai điểm:
- commit cuối của mỗi SHA ứng viên là commit tái sinh manifest (M5);
- mỗi lần vá cũng phải kết thúc bằng một commit tái sinh manifest.

## 4. `nghiem_thu`

**Độ mịn nghiệm thu — [ĐÃ CHỐT Q5'] (chủ kho 2026-11-21, E1; cùng tinh thần Q9 của BUNDLED-TACH-MANH):** với N4, bộ ba (1) tập đích của mỗi đột biến khai ĐỘC LẬP trước khi chạy, (2) so CHÍNH XÁC tập khoá False == tập khai trên danh mục khoá đóng, (3) tự kiểm (d) "ép xanh" là TẬP NGHIỆM THU ĐỦ. Phản chứng ĐƠN KHOÁ cho từng khoá (finding F01 Codex lượt 6) KHÔNG phải điều kiện merge; reviewer trên SHA ứng viên nêu được thì ghi vào nợ có tên `secrets-set-do-min-ve` (mức P3). Chỉ hành vi SAI của mã sản phẩm hoặc một phép đo XANH GIẢ mới là P0–P2. Cặp khoá phụ thuộc tất yếu (`hoi_quy.*.khoa_public` ↔ `hoi_quy.*.encrypt`: đổi khoá public kéo theo đổi tập khoá truyền cho `encrypt`) được phép khai CHUNG trong một tập đích; không đòi đột biến tách riêng từng khoá của cặp.

**Quy tắc vế** (bài học BUNDLED-TACH-MANH; áp cho MỌI khoá; vá chung lớp `mutation-target-accounting`):
1. **Danh mục khoá đóng.** Mỗi khoá là một bộ `ca.luot.quan_sat` và quan sát ĐÚNG MỘT hành vi trực tiếp (rc, một dòng stderr, MỘT bộ đếm, tập khoá `encrypt`). Không gộp nhiều bộ đếm, không gộp "có cảnh báo" với "vắng dòng lỗi".
2. **Kỳ vọng dựng độc lập:** chép cứng trong fragment, không tính lại từ mã sau sửa.
3. **Kênh bản đồ:** `run(tl)` vẫn trả `True`/`False`; ngoài ra fragment ghi BẢN ĐỒ ĐẦY ĐỦ `{khoa: True|False}` của chính lần chạy ra kênh rig (đường tệp do biến môi trường `WP433_SS_BAN_DO` chỉ định; không có biến thì không ghi). N4 chỉ đọc bản đồ do tiến trình của chính đột biến ấy ghi. Khoá có trong danh mục mà vắng trong bản đồ tính là ĐỎ.
4. **Tập đích khai độc lập, so chính xác theo KHOÁ** (r4, sau checkpoint §12): mỗi đột biến có tập khoá đích ĐẦY ĐỦ (liệt kê từng khoá `ca.luot.quan_sat`) ghi trong tệp ma trận TRƯỚC khi chạy, dựng từ cơ chế của đột biến chứ KHÔNG suy từ bản đồ lỗi đo được. N4 so CHÍNH XÁC: tập khoá của bản đồ == danh mục đóng 346 khoá, và tập khoá False == tập đích đã khai. "Đơn đích" định nghĩa theo khoá: một đột biến được tính là phủ khoá k khi k thuộc tập đích khai của nó và tập ấy khớp chính xác. Mỗi khoá trong danh mục phải thuộc tập đích của ≥1 đột biến. Một đột biến mã sản phẩm tác động nhiều lượt của một ca được phép khai tập đích gồm mọi lượt ấy; khi đó bằng chứng phải có số đo (bản đồ của chính tiến trình) cho thấy MỌI khoá khai đều False — một lượt mù (khoá khai mà True) làm đột biến ĐỎ ở so tập. Tự kiểm bắt buộc **(d) ép xanh**: một đột biến FRAGMENT ép đúng một khoá đang đỏ thành True (ví dụ `kieu.list.gws.gws_export0`) dưới một đột biến mã sản phẩm phải làm N4 ĐỎ ở so tập.
5. Mỗi đột biến chạy trong một tiến trình MỚI, trên nguồn đã áp đột biến.

**Danh mục loại quan sát** (26 cặp `(ca, quan_sat)` trên 25 tên quan sát — `stage_enc0` dùng ở cả `kieu` lẫn `token_kieu`; khoá luôn mang tiền tố ca nên không trùng; số khoá = số cặp × số lượt của ca = 250 + 36 + 60 = 346):

| ca | lượt | loại quan sát (kỳ vọng) |
|---|---|---|
| `kieu` | 25: kiểu `list, str, int, null, true` × cờ `gas_token, webapp, gws, nlm, khong_co` | `rc3` (rc == 3); `dong` (TOÀN BỘ `stderr.splitlines()` == `["[secrets-set] ✗ dữ liệu không hợp lệ: bundle"]`); `fetch1`; `upload0`; `stage_enc0`; `gws_export0`; `nlm_refresh0`; `canary0`; `gas0`; `encrypt0` (số lần gọi `encrypt` == 0) — 10 loại |
| `token_kieu` | 6: token `[1]`, `{"a": 1}`, `7` × cờ `gws`, `nlm`, không `TL_TOKEN` | `rc0`; `upload1`; `stage_enc0`; `khoa_public_rong` (`encrypt` không dùng khoá nào ngoài `TL_MASTER_KEY`); `canh_bao_co` (đúng một dòng chứa `thiếu webapp token`); `khong_dong_loi` (không dòng nào chứa `✗`) — 6 loại |
| `hoi_quy` | 6 lượt như §0(3) của r1 | `rc`; `fetch`; `gas`; `upload`; `stage_enc`; `gws_export`; `nlm_refresh`; `canary`; `encrypt`; `khoa_public` — 10 loại, mỗi loại so bằng giá trị chép cứng ở bảng dưới |

**Bảng kỳ vọng `hoi_quy`** (vá chung lớp `regression-oracle-baseline`: MỌI bộ đếm có kỳ vọng chép cứng; thứ tự lượt `gas_token, webapp, gws, nlm, khong_co, env_token.gws`; đo trên base `1e397c8` và nguyên mẫu, cả hai như nhau):

| loại | giá trị theo lượt |
|---|---|
| `rc` | (0, 0, 0, 0, 1, 0) |
| `fetch` | (1, 1, 1, 1, 1, 1) |
| `gas` | (0, 0, 0, 0, 0, 0) |
| `upload` | (1, 1, 1, 1, 0, 1) |
| `stage_enc` | (0, 0, 1, 1, 0, 1) |
| `gws_export` | (0, 0, 1, 0, 0, 1) |
| `nlm_refresh` | (0, 0, 0, 1, 0, 0) |
| `canary` | (0, 0, 0, 1, 0, 0) |
| `encrypt` | (1, 1, 2, 2, 0, 2) |
| `khoa_public` | ([], [], ['tok-cu'], ['tok-cu'], [], ['tok-env']) |

| # | ca | tiêu chí | đỏ khi |
|---|---|---|---|
| N1 | `kieu` | mọi khoá `kieu.*.*` (250) đúng kỳ vọng | có khoá sai hoặc vắng |
| N2 | `token_kieu` | mọi khoá `token_kieu.*.*` (36) đúng kỳ vọng | có khoá sai hoặc vắng |
| N3 | `hoi_quy` | mọi khoá `hoi_quy.*.*` (60) bằng bảng kỳ vọng | có khoá sai hoặc vắng |
| N4 | ma trận đột biến | Executor nộp trong handoff tệp ma trận (đột biến → TẬP KHOÁ ĐÍCH khai độc lập theo quy tắc 4, ghi trước khi chạy; băm tệp ghi trong handoff). Bắt buộc: (i) mỗi khoá của danh mục 346 khoá thuộc tập đích của ≥1 đột biến; (ii) bốn đột biến của r1 (`db_bo_kiem_kieu`, `db_kieu_chi_list`, `db_kieu_thong_diep`, `db_token_repr`) khai ĐỦ tập đích, giữ điều kiện GIẾT theo vị trí frame của r1 cho đột biến 1–2; (iii) PC1, PC2 của r1 khai đủ tập đích. Trên SHA ứng viên, mỗi đột biến chạy một tiến trình MỚI: `run()` False, không văng, tập khoá bản đồ == danh mục, tập khoá False == tập đích khai. Năm tự kiểm (a), (a2), (b), (c), (d) của bộ phân hạng dùng kết quả kỳ vọng riêng; (c) phải SỐNG; (d) phải làm so tập ĐỎ. | một khoá không thuộc tập đích nào; đột biến sống; chết do ngoại lệ (tín dụng giả); bản đồ thiếu hoặc thừa khoá; tập False khác tập khai; tập khai suy từ bản đồ lỗi; tự kiểm sai |
| N5 | gate trên SHA ứng viên (commit cuối là manifest), clone đầy đủ | selftest N/N hai số bằng nhau, N = N_base + 1 (base 1785 ⇒ 1786); `test-fragments-check --json` `ok: true` trên mọi mảnh; `bundle_fragment_check.py --json` `ok: true`, `failed: []`, `case_count` = base + 1; `release-verify RELEASE_MANIFEST.json --strict --json` trên CHÍNH tệp đã commit: `ok: true`, `expected_file_count == checked_file_count == 186`; `workflow-audit --strict --json` rc 0, `py_size.fail == []`, `py_size.warn == []`; `golden-test` ok (`core.abbrev 7`); `.githooks/eol_policy_test.py` N/N; ruff F delta 0 (`python3 -m ruff` bản ghim CI); **`git diff --check <base_sha> <candidate_sha>`** rc 0 và **`git diff --numstat <base_sha> <candidate_sha>`** trong trần §6 (hai OID đầy đủ ghi trong bằng chứng); `doctrine-scan`, `adr-song` rc 0; các fragment `wp433_*` đã có `run()` True. | bất kỳ vế nào |
| N6 | — | **Miễn theo Q4'** (§4c). Không phải điều kiện merge. | — |

**Phạm vi so sánh** (vá chung lớp `candidate-diff-gate-scope`): MỌI lệnh cổng so sánh hai trạng thái (diff, numstat, delta ruff, delta selftest) ghi rõ hai OID đầy đủ `<base_sha>` và `<candidate_sha>`; không lệnh nào dựa vào worktree hay `HEAD` ngầm định.

Phép đo base và head dựng hai clone trong MỘT lệnh. Fragment chạy với nguồn `tl_gws.py` của base phải ĐỎ ở N1 và N2 (tập đỏ ghi trong bằng chứng) và XANH ở N3. Đo bằng cách nạp nguồn base vào fragment của ứng viên, không sửa base.

### 4c. Đo native Windows — **MIỄN [ĐÃ CHỐT Q4']** (chủ kho 2026-11-21, E1; thay Q3)

Không có lượt đo native Windows (D1). Lý do: mã sản phẩm của packet là Python thuần (so sánh kiểu bundle và token sau giải mã), không gọi API riêng nền, không đụng đường dẫn hay tiến trình; fragment chạy trong selftest trên CI Linux. Ngân sách Windows native của lease = **0**. T3 (ngoài phạm vi đặc tả này) theo `docs/PROTOCOL_DA_PHIEN.md` §10.1.

## 5. `pham_vi_e`

Không chạm E4, E5. Dùng dữ liệu giả và thư mục tạm. Không mạng, không LIVE, không đẩy Package, không chạy `secrets-set` thật, không đọc hay ghi secrets thật.

## 6. `luat_dung`

- **Trần:**
  - Lời gọi Codex theo ADR-0055, đã dùng 6/10.
  - Kích thước theo ADR-0053 (≤ 6 tệp, ≤ 450 dòng thêm), đo bằng numstat thật.
  - Tập đường trong diff phải nằm trong write set §1.
  - Vượt trần hoặc lệch write set ⇒ DỪNG; nâng trần là E2.
- **Lệch hiện trạng:** §0 lệch trên base thật (blob `tl_gws.py`, các dòng neo, hành vi (1)(2)(3), mảnh chứa fragment) ⇒ DỪNG, ra revision.
- **Fragment sai trên base:** chạy trên nguồn base mà không đỏ đúng N1/N2, hoặc `hoi_quy` lệch bảng ⇒ DỪNG.
- **Fragment #433 khác bị ảnh hưởng:** một fragment `wp433_*` đã có đổi bộ đếm so với base ⇒ DỪNG.
- **Ngoại lệ chưa có:** chưa có comment ngoại lệ bundled + manifest ⇒ không cấp lease (E2).
- **Mọi stop condition khác:** theo protocol §12.

## 7. `hinh_dang_ke_thua`

Cùng lớp với M3 của packet N: bundle JSON hợp lệ nhưng không phải object thì từ chối NGAY SAU giải mã và trước mọi cờ, export, refresh, canary, mã hoá lại và upload. Ranh giới ấy nằm SAU `load_creds` và `_secrets_fetch` (đọc `--secrets-file` hoặc tải), hai bước vẫn chạy trước giải mã và ngoài phạm vi packet (§0a). M2 thuộc họ "khoá suy ra từ dữ liệu
chưa kiểm kiểu". Mọi packet sau đụng fragment đều phải khai cả nhóm `tl_test_fragments_bundled*.py`, đúng như §7 của BUNDLED-TACH-MANH.

## 8. `chua_do_duoc` và dự toán

- **Numstat:** đo nguyên mẫu được +211/−8 trên 4 tệp (§0b). Fragment còn phải thêm danh mục khoá, kênh bản đồ, tệp ma trận tập đích và đột biến (N4); ước thêm 100–200 dòng ⇒ dự toán **≤ 415 dòng thêm** (211 + 200 = 411), dưới 450. Reviewer lượt 5 đo: bản đồ 346 khoá được 11.815 B; mảnh 2 với đệm 239 dòng là 165.030 B, dưới hạn mảnh 192 KiB. Vượt thì DỪNG (§6), không cắt vế.
- **Chưa đo:**
  - fragment sau khi mở rộng ma trận (việc của executor);
  - Windows native: miễn theo Q4' (§4c), không đo.

## 9. Lịch sử và quyết định

- Chủ kho 2026-11-20 mở việc riêng cho nợ `secrets-set`. Q1–Q3 chốt như đã ghi ở r1 (Q3 được thay bằng Q4' ngày 2026-11-21, xem dưới).
- r1 (`477fb647`): Codex review 3/10 lượt, lượt 3 approve, nhưng cả ba verdict thiếu bảng lớp §8.3, nên r1 không đóng băng hợp lệ (mục sổ 7046243035).
- **Thi công trên r1 bị dừng:**
  - Fragment secrets-set làm tệp bundled một mảnh vượt WARN (300.798 B).
  - Chủ kho chọn "Tách bundled trước", và packet BUNDLED-TACH-MANH đã land.
- **Sự cố trên nhánh `agent/wp433-r8-g1-claude`** (lease `wp433-r8-g1-claude`, đã ghi bia mộ):
  - Executor push 3 lần: `a8a3b3c` (code), `5eab294` (waiver `py_size` cho tệp bundled, ngoài write set, KHÔNG được duyệt), `de341ed` (revert `5eab294`, cây về đúng `a8a3b3c`).
  - Cả ba lần push đều chưa qua review offline approve và chưa đạt bất biến (a) §12. Biên nhận của packet này phải ghi lại ba lần push đó.
  - r2 chạy trên generation và nhánh MỚI, không tiếp nhánh cũ. Mã của nhánh cũ chỉ được dùng làm nguồn ghim (`a8a3b3ca…`).
- **Chủ kho 2026-11-21:**
  - Làm secrets-set ngay sau khi tách bundled land.
  - Executor dùng Opus 5.5 vì Fable đã hết hạn mức tới 25-11.

- Codex lượt 4/10 (run `44a7c54b`, r2, §8.3 đầu tiên, request_changes; verdict `ops/reviews/wp433-secrets-set-spec-r2/codex/luot4.txt` @ `a6f3c8e`): 5 lớp mở, 8 biểu hiện. Tỷ lệ 3→4 N/A (r1 kết thúc U=∅). r3 vá chung theo lớp.

### Bảng lớp r3 (vá chung)

| class_slug | biểu hiện lượt 4 | cách vá chung ở r3 | phép kiểm đóng lớp |
|---|---|---|---|
| `mutation-target-accounting` (P2) | F01: nhãn gộp (`khong_goi`, `khong_public`, `canh_bao`), đích dừng ở lỗi đầu, `run()` chỉ trả boolean | quy tắc vế 1–5: danh mục khoá `ca.luot.quan_sat` một hành vi; kênh bản đồ `WP433_SS_BAN_DO`, khoá vắng là đỏ; đơn đích theo loại quan sát; bốn đột biến r1 và PC1/PC2 khai tập đỏ thực tế | đếm: mọi loại quan sát của danh mục có ≥1 đột biến đơn đích; không khoá nào quan sát >1 hành vi; N4 so tập False với tập khai trên bản đồ của chính tiến trình |
| `native-gate-evidence` (P2) | F03: D1 rút gọn, không đòi N2/N3, không loại `False` do neo `HONG` | §4c viết lại một điều kiện D1 đầy đủ: (a) ứng viên True + bản đồ bằng Linux + HONG 0 + ma trận; (b) base đỏ N1, N2 ở khoá ghi rõ, N3 xanh 60/60, HONG 0; nhánh KHÔNG ĐO ĐƯỢC; N6 và §6 trỏ đúng §4c | đọc N6, §4c, §6: không chỗ nào dẫn bản rút gọn; hồ sơ chỉ có `False`/`rc3` làm N6 đỏ |
| `candidate-diff-gate-scope` (P2) | F04: `git diff --check` không ghim phạm vi | mọi lệnh so sánh ghim `<base_sha> <candidate_sha>` (diff --check, numstat, delta ruff/selftest) | rà toàn đặc tả: không lệnh so sánh nào dựa vào worktree/HEAD ngầm định |
| `regression-oracle-baseline` (P3) | F02: thiếu kỳ vọng `encrypt` | bảng kỳ vọng `hoi_quy` đủ 10 loại, gồm `encrypt = (1,1,2,2,0,2)` và `fetch`/`gas` tường minh | mọi loại quan sát của `hoi_quy` có một hàng kỳ vọng chép cứng |
| `prevalidation-io-boundary` (P3) | F05: §7 nói chặn "trước mọi tác dụng phụ" | §0a và §7 nêu đúng ranh giới: `load_creds`, `_secrets_fetch` chạy trước giải mã, ngoài phạm vi; M1 chặn ngay sau giải mã trước mọi cờ/ghi/mạng còn lại | không câu nào trong đặc tả tuyên bố chặn trước `fetch`; kỳ vọng `fetch1` ở N1 |

Cùng lượt: bỏ dẫn chiếu commit cục bộ `0a3f3edc…` không có trên GitHub (§0b), trỏ diff nguyên mẫu và tree `8d23a5ea`.

- Codex lượt 5/10 (run `54cec641`, r3, request_changes; verdict `ops/reviews/wp433-secrets-set-spec-r2/codex/luot5.txt` @ `dd82136`): tỷ lệ 4→5 = 3/5 (60%); `candidate-diff-gate-scope`, `regression-oracle-baseline`, `prevalidation-io-boundary` ĐÃ VÁ THẬT; `mutation-target-accounting` và `native-gate-evidence` VÁ MỘT PHẦN; hai lớp mới P3 `implementation-size-estimate`, `review-budget-accounting`. Lớp `native-gate-evidence` xuất hiện lần thứ ba (lượt 1, 4, 5) ⇒ **checkpoint §12**: dừng vá thêm vế, xét lại cách làm.
- **Hướng mới (r4):** (1) D1 = oracle BẰNG NHAU với bản Linux nộp trong handoff (cùng script, cùng ma trận, cùng hai nguồn; so từng tiến trình và từng khoá) thay cho danh sách điều kiện riêng của Windows — cách cũ lặp lại một hình dạng lỗi: mỗi lượt lộ một vế Windows viết thiếu so với Linux. (2) Tập đích N4 khai độc lập trước khi chạy và so chính xác theo khoá, thêm tự kiểm (d) ép xanh — cách cũ ("đơn đích theo loại", tập đích lấy từ bản đồ lỗi) tự xác nhận được một lượt mù.

### Bảng lớp r4 (vá chung)

| class_slug | biểu hiện lượt 5 | cách vá chung ở r4 | phép kiểm đóng lớp |
|---|---|---|---|
| `mutation-target-accounting` (P2) | F01: đơn đích theo loại che lượt mù; tập đích suy từ bản đồ lỗi; đếm 25/26 | quy tắc 4 viết lại: tập đích khai độc lập trước khi chạy, so chính xác theo khoá trên danh mục 346 khoá; tự kiểm (d) ép xanh; nêu rõ 26 cặp / 25 tên | ép một khoá đỏ thành True dưới một đột biến mã sản phẩm làm N4 ĐỎ; không chỗ nào cho tập đích lấy từ bản đồ đo được |
| `native-gate-evidence` (P2, lần 3) | F02: vế base thiếu `run=False`; nguồn ma trận lẫn nguồn đo; "hai tiến trình" mơ hồ | D1 = `d1-windows.json` BẰNG `d1-linux.json`, tách nguồn fragment / nguồn mã sản phẩm, số tiến trình lấy từ bản Linux; bỏ mọi điều kiện riêng Windows | §4c, N6, §6 không còn điều kiện Windows nào ngoài so bằng; mọi giá trị `run()`, `HONG`, khoá của vế base đều nằm trong `d1-linux.json` |
| `implementation-size-estimate` (P3) | F03: 211 + 200 = 411 > 410 | dự toán ≤ 415, kèm số đo kích thước của reviewer | phép cộng trong §8 khớp cận |
| `review-budget-accounting` (P3) | F04: §6 ghi 3/10 trong khi đầu và §9 ghi 4/10 | mọi chỗ ghi số lượt Codex dùng 5/10 | rg `/10` trong đặc tả chỉ ra một số hiện hành |

- Codex lượt 6/10 (run `bf71cd53`, r4, request_changes; verdict `ops/reviews/wp433-secrets-set-spec-r2/codex/luot6.txt` @ `c7dc360`): tỷ lệ 5→6 = 2/4 (50%); `implementation-size-estimate` và `review-budget-accounting` ĐÃ VÁ THẬT; `mutation-target-accounting` VÁ MỘT PHẦN (F01: "đơn đích" cho phép tập nhiều khoá, đòi phản chứng đơn khoá); `native-gate-evidence` VÁ MỘT PHẦN, **lần xuất hiện thứ tư** (F02: oracle bằng nhau chưa buộc bản Linux đạt N1–N4 trước); lớp mới `native-rig-handoff-order` (F03: rig đăng qua comment PR trong khi D1 phải xong trước push).
- **Chủ kho 2026-11-21 (E1, AskUserQuestion phiên #1206): "Miễn D1 + chốt độ mịn".** Gốc rễ: mã sản phẩm Python thuần, khó khăn nằm ở việc đặc tả hoá một phép đo chéo nền, không nằm ở mã; lớp D1 tái phát sau khi đã đổi cách làm (r4). Hai quyết định:
  - **Q4'** (thay Q3): miễn đo native Windows D1; ngân sách Windows = 0.
  - **Q5'**: tập đích khai độc lập + so chính xác + tự kiểm (d) là đủ cho N4; phản chứng đơn khoá là nợ P3 `secrets-set-do-min-ve`; cặp `khoa_public` ↔ `encrypt` khai chung.

### Bảng lớp r5

| class_slug | trạng thái sau r5 | cách đóng | phép kiểm đóng lớp |
|---|---|---|---|
| `native-gate-evidence` (P2, lần 4) | ĐÓNG bằng QUYẾT ĐỊNH PHẠM VI của chủ kho (Q4'), không phải bằng vá | §4c thành MIỄN; N6 miễn; §6 bỏ điều kiện D1; ngân sách Windows 0 | phần hiệu lực §0–§8 không còn điều kiện, tệp hay rig nào cho D1 |
| `native-rig-handoff-order` (P2, mới lượt 6) | ĐÓNG bằng QUYẾT ĐỊNH PHẠM VI (Q4'): không còn rig Windows | bỏ mọi bước giao rig | phần hiệu lực không còn bước đăng rig |
| `mutation-target-accounting` (P2) | phần đòi phản chứng đơn khoá chuyển thành NỢ P3 theo Q5'; phần còn lại (khai độc lập, so chính xác, ép xanh) giữ nguyên từ r4 | ghi Q5' ở §4, nợ `secrets-set-do-min-ve`, cặp phụ thuộc khai chung | §4 nêu Q5'; N4 không đòi phản chứng đơn khoá |
| `review-budget-accounting` (P3) | đã đóng ở lượt 6 | mọi chỗ ghi 6/10 | rg `/10` trong đặc tả chỉ ra 6/10 ở phần hiệu lực |

## 10. Nhật ký revision

- 2026-11-21T07:3xZ (phiên con của điều phối #1206): bản 2 trên base `1e397c8`. Đo §0b (Linux): fragment nằm ở mảnh 2, selftest 1786/1786, `release-verify` 186/186, numstat +211/−8. Thay đổi so với r1:
  - write set thêm `tl_test_fragments_bundled_2.py`, `tl_test_fragments_bundled.py` và `RELEASE_MANIFEST.json` (ngoại lệ kiểu Q7);
  - nghiệm thu theo quy tắc vế;
  - ma trận đột biến phủ mọi nhãn;
  - §3a chỉ trỏ tới protocol.
- 2026-11-21 (phiên con của điều phối #1206): **r3** từ r2 `22a1be39`: vá chung 5 lớp Codex lượt 4 (bảng lớp §9). Không đổi Q1–Q3, write set, trần.
- 2026-11-21 (phiên con của điều phối #1206): **r4** từ r3 `593b82a7` sau checkpoint §12 lượt 5: D1 oracle bằng nhau, tập đích N4 khai độc lập so chính xác theo khoá + tự kiểm (d), sửa đếm 26/25, dự toán ≤ 415, số lượt Codex 5/10. Không đổi Q1–Q3, write set, trần.
- Mục sổ `xet_lai_cach_lam` cho checkpoint lượt 5: https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7059747094
- 2026-11-21 (phiên con của điều phối #1206): **r5** từ r4 `be0974f9` theo quyết định chủ kho (E1) sau Codex lượt 6: Q4' miễn D1 Windows, Q5' chốt độ mịn N4 (nợ `secrets-set-do-min-ve`), đã dùng 6/10. Không đổi Q1–Q2, write set (5 tệp), trần.
