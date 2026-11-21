tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# SECRETS-SET-BUNDLE-KIEU r3 — `secrets-set` dùng bundle giải mã mà chưa kiểm kiểu (nợ `wp433-secrets-set-bundle-khong-phai-dict`)

- packet_id: SECRETS-SET-BUNDLE-KIEU; revision: 3; thay r2 (`22a1be3915168e82b164ed11f43834b595bbafc8223e4c66834f2ce02b852091`) và r1 (`477fb64757d03e9ce34b112ec507283e140d98a88fd16c2eefa3fe61ef88cfc1`).
- r1 CHƯA đóng băng hợp lệ: ba verdict Codex của r1 (`ops/reviews/wp433-secrets-set-spec-r1/rv/`) không có `class_slug` và bảng lớp (§8.3). Theo mục sổ
  https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7046243035 chúng không dùng để approve, nhưng vẫn tính vào trần lời gọi:
  **đã dùng 4/10** theo dòng `tran_loi_goi_codex` ở trên (lượt 4 là lượt §8.3 đầu tiên, trên r2).

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Nợ ghi ở §2 đặc tả `ops/specs/GWS-CRED-DICH-NGOAI-KHO-N-r2.md`. Chủ kho 2026-11-20: "Mở việc riêng cho Secret Set đi." Chủ kho 2026-11-21 (phiên điều phối #1206), sau khi BUNDLED-TACH-MANH land: làm ngay, executor Opus 5.5. |
| `phu_thuoc` | BUNDLED-TACH-MANH đã land (PR #1485, merge `96cd012`; hồ sơ land PR #1486, merge `1e397c8`). Packet N (PR #1441) và P2BW (PR #1453) đã land. |
| `review_class` | `sensitive`: `scripts/tl_gws.py` `_secrets_set_body` là đường GHI credential (bundle `tl_secrets.enc` và hai tệp public `.enc` trên Drive). |
| `base` | `1e397c89d69f451694a2252103ea97ec274ab43f` (origin/master lúc soạn; tree `b1b95b504e4a64cc6470dfed2081da6d778f4499`). Blob `scripts/tl_gws.py` `fbeb9421edd0a7e451534a92c89d090c4de4b3a4`, BẰNG blob ở `0f9aa2a` (base của r1): không commit nào từ `0f9aa2a` tới base chạm tệp này, nên mọi số dòng neo của r1 vẫn đúng. Phiên thi hành đo lại §0 trên base thật của lease; lệch thì DỪNG. |

Các mục **[ĐÃ CHỐT Qn]** là quyết định của chủ kho, giữ nguyên từ r1. Muốn đổi thì phải ra revision mới.

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

**Quy tắc vế** (bài học BUNDLED-TACH-MANH; áp cho MỌI khoá; vá chung lớp `mutation-target-accounting`):
1. **Danh mục khoá đóng.** Mỗi khoá là một bộ `ca.luot.quan_sat` và quan sát ĐÚNG MỘT hành vi trực tiếp (rc, một dòng stderr, MỘT bộ đếm, tập khoá `encrypt`). Không gộp nhiều bộ đếm, không gộp "có cảnh báo" với "vắng dòng lỗi".
2. **Kỳ vọng dựng độc lập:** chép cứng trong fragment, không tính lại từ mã sau sửa.
3. **Kênh bản đồ:** `run(tl)` vẫn trả `True`/`False`; ngoài ra fragment ghi BẢN ĐỒ ĐẦY ĐỦ `{khoa: True|False}` của chính lần chạy ra kênh rig (đường tệp do biến môi trường `WP433_SS_BAN_DO` chỉ định; không có biến thì không ghi). N4 chỉ đọc bản đồ do tiến trình của chính đột biến ấy ghi. Khoá có trong danh mục mà vắng trong bản đồ tính là ĐỎ.
4. **Đơn đích theo loại quan sát:** một đột biến mã sản phẩm thường tác động mọi lượt của một ca, nên "đơn đích" ở đây nghĩa là tập khoá đỏ của nó chỉ chứa MỘT loại quan sát (ví dụ chỉ `*.*.upload0`), có thể trên nhiều lượt. Mỗi loại quan sát trong danh mục là đích của ≥1 đột biến đơn đích như vậy.
5. Mỗi đột biến chạy trong một tiến trình MỚI, trên nguồn đã áp đột biến.

**Danh mục loại quan sát** (26 loại; số khoá = loại × số lượt của ca):

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
| N4 | ma trận đột biến | Executor nộp trong handoff ma trận (đột biến → TẬP KHOÁ ĐÍCH THỰC TẾ, đo trên SHA ứng viên). Bắt buộc: (i) mỗi loại quan sát của danh mục có ≥1 đột biến đơn đích (quy tắc 4); (ii) bốn đột biến của r1 (`db_bo_kiem_kieu`, `db_kieu_chi_list`, `db_kieu_thong_diep`, `db_token_repr`) khai ĐỦ tập khoá đỏ thực tế (không chỉ lỗi đầu), giữ điều kiện GIẾT theo vị trí frame của r1 cho đột biến 1–2; (iii) PC1, PC2 của r1 khai đủ tập đỏ thực tế. Trên SHA ứng viên, mỗi đột biến: `run()` False, không văng, bản đồ đủ khoá, tập khoá False BẰNG tập khai. Bốn tự kiểm (a), (a2), (b), (c) của bộ phân hạng dùng kết quả kỳ vọng riêng; (c) phải SỐNG. | một loại quan sát không có đột biến đơn đích; đột biến sống; chết do ngoại lệ (tín dụng giả); bản đồ thiếu khoá; tập False khác tập khai; tự kiểm sai |
| N5 | gate trên SHA ứng viên (commit cuối là manifest), clone đầy đủ | selftest N/N hai số bằng nhau, N = N_base + 1 (base 1785 ⇒ 1786); `test-fragments-check --json` `ok: true` trên mọi mảnh; `bundle_fragment_check.py --json` `ok: true`, `failed: []`, `case_count` = base + 1; `release-verify RELEASE_MANIFEST.json --strict --json` trên CHÍNH tệp đã commit: `ok: true`, `expected_file_count == checked_file_count == 186`; `workflow-audit --strict --json` rc 0, `py_size.fail == []`, `py_size.warn == []`; `golden-test` ok (`core.abbrev 7`); `.githooks/eol_policy_test.py` N/N; ruff F delta 0 (`python3 -m ruff` bản ghim CI); **`git diff --check <base_sha> <candidate_sha>`** rc 0 và **`git diff --numstat <base_sha> <candidate_sha>`** trong trần §6 (hai OID đầy đủ ghi trong bằng chứng); `doctrine-scan`, `adr-song` rc 0; các fragment `wp433_*` đã có `run()` True. | bất kỳ vế nào |
| N6 | D1 native (§4c) | Đủ mọi vế của D1 ở §4c, với exact SHA/tree của base và ứng viên. | thiếu bất kỳ vế nào, sai SHA/tree, `KHÔNG ĐO ĐƯỢC`, `HONG > 0` ở vế (a), hoặc trái kỳ vọng |

**Phạm vi so sánh** (vá chung lớp `candidate-diff-gate-scope`): MỌI lệnh cổng so sánh hai trạng thái (diff, numstat, delta ruff, delta selftest) ghi rõ hai OID đầy đủ `<base_sha>` và `<candidate_sha>`; không lệnh nào dựa vào worktree hay `HEAD` ngầm định.

Phép đo base và head dựng hai clone trong MỘT lệnh. Fragment chạy với nguồn `tl_gws.py` của base phải ĐỎ ở N1 và N2 (tập đỏ ghi trong bằng chứng) và XANH ở N3. Đo bằng cách nạp nguồn base vào fragment của ứng viên, không sửa base.

### 4c. Đo native Windows — **[ĐÃ CHỐT Q3: đo một lượt D1 nhẹ]** (`DESKTOP-T9R33P2`)

Vá chung lớp `native-gate-evidence`: một điều kiện D1 đầy đủ, không dẫn chiếu bản rút gọn.

- **Dựng:** ghim exact head/tree của ứng viên và base; clone `git -c core.longpaths=true`; `python`; rig dùng một lần do executor soạn, đăng comment PR dạng gzip+base64 kèm sha256 qua REST; chạy dưới thư mục phiên, offline; dọn đúng thứ mình tạo. Ngân sách Windows native ≤ 2.
- **Hai tiến trình, mỗi vế MỘT lần:**
  - **(a) vế ứng viên:** `run(tl)` của fragment ứng viên trên nguồn ứng viên. Kỳ vọng: `True`; bản đồ khoá đủ và BẰNG bản đồ lượt Linux trên cùng SHA; `HONG 0`; ma trận N4 chạy trên nguồn ứng viên cho cùng kết quả phân hạng như Linux.
  - **(b) vế base:** nguồn `tl_gws.py` của base nạp vào fragment ứng viên, cùng bộ đo. Kỳ vọng dương, ghi riêng từng vế: N1 đỏ, có khoá `kieu.list.gas_token.rc3` False; N2 đỏ, có khoá `token_kieu.list.gws.khoa_public_rong` False; N3 XANH đủ 60/60 khoá. Vế âm: `HONG` của bộ đo ở vế (b) phải bằng 0 — `False` do neo đột biến hỏng (`HONG > 0`) KHÔNG được tính là đỏ hành vi.
- **Ghi:** lệnh, shell, phiên bản python, exact SHA/tree hai vế, đầu ra thô, rc, bản đồ khoá của cả hai vế.
- **KHÔNG ĐO ĐƯỢC:** máy offline, thiếu quyền, rig không chạy tới `run()`, hoặc thiếu bất kỳ dữ kiện nào ở trên ⇒ ghi `KHÔNG ĐO ĐƯỢC`, N6 đỏ, dừng theo §6.
- **T3** (ngoài §4c): theo `docs/PROTOCOL_DA_PHIEN.md` §10.1.

## 5. `pham_vi_e`

Không chạm E4, E5. Dùng dữ liệu giả và thư mục tạm. Không mạng, không LIVE, không đẩy Package, không chạy `secrets-set` thật, không đọc hay ghi secrets thật.

## 6. `luat_dung`

- **Trần:**
  - Lời gọi Codex theo ADR-0055, đã dùng 3/10.
  - Kích thước theo ADR-0053 (≤ 6 tệp, ≤ 450 dòng thêm), đo bằng numstat thật.
  - Tập đường trong diff phải nằm trong write set §1.
  - Vượt trần hoặc lệch write set ⇒ DỪNG; nâng trần là E2.
- **Lệch hiện trạng:** §0 lệch trên base thật (blob `tl_gws.py`, các dòng neo, hành vi (1)(2)(3), mảnh chứa fragment) ⇒ DỪNG, ra revision.
- **Fragment sai trên base:** chạy trên nguồn base mà không đỏ đúng N1/N2, hoặc `hoi_quy` lệch bảng ⇒ DỪNG.
- **Fragment #433 khác bị ảnh hưởng:** một fragment `wp433_*` đã có đổi bộ đếm so với base ⇒ DỪNG.
- **D1:** bất kỳ vế nào của §4c không đạt, hoặc `KHÔNG ĐO ĐƯỢC` ⇒ DỪNG (N6).
- **Ngoại lệ chưa có:** chưa có comment ngoại lệ bundled + manifest ⇒ không cấp lease (E2).
- **Mọi stop condition khác:** theo protocol §12.

## 7. `hinh_dang_ke_thua`

Cùng lớp với M3 của packet N: bundle JSON hợp lệ nhưng không phải object thì từ chối NGAY SAU giải mã và trước mọi cờ, export, refresh, canary, mã hoá lại và upload. Ranh giới ấy nằm SAU `load_creds` và `_secrets_fetch` (đọc `--secrets-file` hoặc tải), hai bước vẫn chạy trước giải mã và ngoài phạm vi packet (§0a). M2 thuộc họ "khoá suy ra từ dữ liệu
chưa kiểm kiểu". Mọi packet sau đụng fragment đều phải khai cả nhóm `tl_test_fragments_bundled*.py`, đúng như §7 của BUNDLED-TACH-MANH.

## 8. `chua_do_duoc` và dự toán

- **Numstat:** đo nguyên mẫu được +211/−8 trên 4 tệp (§0b). Fragment còn phải thêm danh mục khoá, kênh bản đồ và đột biến cho 26 loại quan sát (N4); ước thêm 100–200 dòng ⇒ dự toán **≤ 410 dòng thêm**, dưới 450. Vượt thì DỪNG (§6), không cắt vế.
- **Chưa đo:**
  - fragment sau khi mở rộng ma trận (việc của executor);
  - D1 Windows (§4c).

## 9. Lịch sử và quyết định

- Chủ kho 2026-11-20 mở việc riêng cho nợ `secrets-set`. Q1–Q3 chốt như đã ghi ở r1.
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

## 10. Nhật ký revision

- 2026-11-21T07:3xZ (phiên con của điều phối #1206): bản 2 trên base `1e397c8`. Đo §0b (Linux): fragment nằm ở mảnh 2, selftest 1786/1786, `release-verify` 186/186, numstat +211/−8. Thay đổi so với r1:
  - write set thêm `tl_test_fragments_bundled_2.py`, `tl_test_fragments_bundled.py` và `RELEASE_MANIFEST.json` (ngoại lệ kiểu Q7);
  - nghiệm thu theo quy tắc vế;
  - ma trận đột biến phủ mọi nhãn;
  - §3a chỉ trỏ tới protocol.
- 2026-11-21 (phiên con của điều phối #1206): **r3** từ r2 `22a1be39`: vá chung 5 lớp Codex lượt 4 (bảng lớp §9). Không đổi Q1–Q3, write set, trần.
