tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# SECRETS-SET-BUNDLE-KIEU r2 — `secrets-set` dùng bundle giải mã mà chưa kiểm kiểu (nợ `wp433-secrets-set-bundle-khong-phai-dict`)

- packet_id: SECRETS-SET-BUNDLE-KIEU; revision: 2; thay r1 (`477fb64757d03e9ce34b112ec507283e140d98a88fd16c2eefa3fe61ef88cfc1`).
- r1 CHƯA đóng băng hợp lệ: ba verdict Codex của r1 (`ops/reviews/wp433-secrets-set-spec-r1/rv/`) không có `class_slug` và bảng lớp (§8.3). Theo mục sổ
  https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7046243035 chúng không dùng để approve, nhưng vẫn tính vào trần lời gọi:
  **đã dùng 3/10** theo dòng `tran_loi_goi_codex` ở trên.

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
  - `_secrets_set_body` (999) giải mã ở dòng 1014 (lỗi thì rc 3, dòng 1015–1017).
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
- chạy `tl.py release-manifest --out RELEASE_MANIFEST.json`, rồi commit cục bộ thành `0a3f3edc`, tree `8d23a5ea`.

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

**Numstat `base..0a3f3edc`:** 4 tệp, **+211/−8**.

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

**Quy tắc vế** (bài học của BUNDLED-TACH-MANH, áp cho mọi khoá):
1. Mỗi nhãn chỉ quan sát MỘT hành vi.
2. Nhãn quan sát trực tiếp: rc, stderr, bộ đếm, khoá `encrypt`. Không suy ra qua thành phần khác.
3. Mỗi nhãn là đích của ít nhất một đột biến chỉ phá đúng nó.
4. Mỗi đột biến chạy trong một tiến trình MỚI, trên nguồn đã áp đột biến, và đọc kết quả của chính lần chạy đó.
5. Nhãn vắng mặt trong kết quả tính là ĐỎ.

| # | ca | tiêu chí | đỏ khi |
|---|---|---|---|
| N1 | `kieu`: 25 lượt, kiểu `list, str, int, null, true` × cờ `gas_token, webapp, gws, nlm, khong_co` | Mỗi lượt có ba nhãn: `rc3` (rc == 3); `dong` (TOÀN BỘ `stderr.splitlines()` bằng đúng `["[secrets-set] ✗ dữ liệu không hợp lệ: bundle"]`); `khong_goi` (`fetch == 1`, và `upload`, `stage_enc`, `gws_export`, `nlm_refresh`, `canary`, `gas`, số lần `encrypt` đều == 0). | có lượt mà nhãn nào không thoả, hoặc nhãn vắng |
| N2 | `token_kieu`: 6 lượt, token `[1]`, `{"a": 1}`, `7` × cờ `gws`, `nlm`, không có `TL_TOKEN` | `rc0` (rc == 0); `upload1` (`upload == 1`); `khong_public` (`stage_enc == 0` và `encrypt` không dùng khoá nào ngoài `TL_MASTER_KEY`); `canh_bao` (đúng một dòng chứa `thiếu webapp token`, không dòng nào có `✗`). | như N1 |
| N3 | `hoi_quy`: 6 lượt như §0(3) của r1 | rc, MỌI bộ đếm và danh sách khoá public BẰNG bảng §0(3) của r1, chép cứng trong fragment. | bất kỳ lệch nào, hoặc nhãn vắng |
| N4 | ma trận đột biến | Executor nộp ma trận (đột biến → tập ca·lượt·nhãn đích) trong handoff. **Mỗi** nhãn của N1–N3 là đích của ít nhất một đột biến đơn đích. Tối thiểu có bốn đột biến của r1 (`db_bo_kiem_kieu`, `db_kieu_chi_list`, `db_kieu_thong_diep`, `db_token_repr`), cùng điều kiện GIẾT theo vị trí frame của r1 cho đột biến 1–2. Hai phản chứng bộ đo PC1, PC2 của r1 cũng phải đỏ đúng chỗ. Trên SHA ứng viên: mỗi đột biến làm `run()` False, không văng, và tập đỏ BẰNG đúng tập đích đã khai. Bốn tự kiểm (a), (a2), (b), (c) của bộ phân hạng r1 phải đạt. | một nhãn không có đột biến đích; đột biến sống; chết do ngoại lệ (tín dụng giả); tập đỏ khác tập đích; tự kiểm hoặc phản chứng không đạt |
| N5 | gate trên SHA ứng viên (commit cuối là manifest), clone đầy đủ | selftest N/N hai số bằng nhau, N = N_base + 1 (base 1785 ⇒ 1786); `test-fragments-check --json` `ok: true` trên mọi mảnh; `bundle_fragment_check.py --json` `ok: true`, `failed: []`, `case_count` = base + 1; `release-verify RELEASE_MANIFEST.json --strict --json` trên CHÍNH tệp đã commit: `ok: true`, `expected_file_count == checked_file_count == 186`; `workflow-audit --strict --json` rc 0, `py_size.fail == []`, `py_size.warn == []`; `golden-test` ok (`core.abbrev 7`); `.githooks/eol_policy_test.py` N/N; ruff F delta 0; `git diff --check`, `doctrine-scan`, `adr-song` rc 0; các fragment `wp433_*` đã có `run()` True. | bất kỳ vế nào |
| N6 | đo native D1 (§4c) | Hồ sơ ghi lệnh, shell, exact head/tree của base và ứng viên, đầu ra thô, rc và kết luận của cả hai vế D1. | thiếu, sai SHA/tree, `KHÔNG ĐO ĐƯỢC`, hoặc trái kỳ vọng |

Phép đo base và head dựng hai clone trong MỘT lệnh. Fragment chạy với nguồn `tl_gws.py` của base phải ĐỎ đúng ở N1 rồi đến N2. Đo bằng cách nạp nguồn base
vào fragment của ứng viên, không sửa base.

### 4c. Đo native Windows — **[ĐÃ CHỐT Q3: đo một lượt D1 nhẹ]** (`DESKTOP-T9R33P2`)

Giữ nguyên §4c của r1, chỉ đổi số liệu và nguồn ghim:
- Ghim exact head/tree. Clone bằng `git -c core.longpaths=true`.
- Rig dùng một lần; đăng thành comment PR dạng gzip+base64 kèm sha256, qua REST.
- Chạy dưới thư mục phiên, offline. Ngân sách Windows native ≤ 2.
- D1: (a) fragment của ứng viên ra `True`, bộ đếm bằng lượt Linux; (b) nạp nguồn base vào fragment của ứng viên thì đỏ đúng `kieu.list.gas_token` · `rc3`.

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
- **D1:** (a) không `True`, hoặc (b) không đỏ đúng đích ⇒ DỪNG.
- **Ngoại lệ chưa có:** chưa có comment ngoại lệ bundled + manifest ⇒ không cấp lease (E2).
- **Mọi stop condition khác:** theo protocol §12.

## 7. `hinh_dang_ke_thua`

Cùng lớp với M3 của packet N: bundle JSON hợp lệ nhưng không phải object thì từ chối TRƯỚC mọi tác dụng phụ. M2 thuộc họ "khoá suy ra từ dữ liệu
chưa kiểm kiểu". Mọi packet sau đụng fragment đều phải khai cả nhóm `tl_test_fragments_bundled*.py`, đúng như §7 của BUNDLED-TACH-MANH.

## 8. `chua_do_duoc` và dự toán

- **Numstat:** đo nguyên mẫu được +211/−8 trên 4 tệp (§0b). Fragment còn phải thêm đột biến cho mọi nhãn (N4); ước thêm 60–150 dòng ⇒ dự toán **≤ 360 dòng thêm**, dưới 450.
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

## 10. Nhật ký revision

- 2026-11-21T07:3xZ (phiên con của điều phối #1206): bản 2 trên base `1e397c8`. Đo §0b (Linux): fragment nằm ở mảnh 2, selftest 1786/1786, `release-verify` 186/186, numstat +211/−8. Thay đổi so với r1:
  - write set thêm `tl_test_fragments_bundled_2.py`, `tl_test_fragments_bundled.py` và `RELEASE_MANIFEST.json` (ngoại lệ kiểu Q7);
  - nghiệm thu theo quy tắc vế;
  - ma trận đột biến phủ mọi nhãn;
  - §3a chỉ trỏ tới protocol.
