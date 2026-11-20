tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# SECRETS-SET-BUNDLE-KIEU r1 — `secrets-set` dùng bundle giải mã mà chưa kiểm kiểu (nợ `wp433-secrets-set-bundle-khong-phai-dict`)

- packet_id: SECRETS-SET-BUNDLE-KIEU; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Nợ ghi ở §2 đặc tả `ops/specs/GWS-CRED-DICH-NGOAI-KHO-N-r2.md` (nhánh `ops/wp433-p2n-spec`): "`secrets-set` (dòng 1014) cũng dùng bundle chưa kiểm kiểu — nợ riêng nếu chủ kho muốn". Chủ kho 2026-11-20 (phiên điều phối #1206): "Mở việc riêng cho Secret Set đi." |
| `phu_thuoc` | Packet N (PR #1441; hồ sơ land PR #1451) đã thêm cùng kiểm cho `cmd_bootstrap` và `cmd_nlm_auth_pull`; P2BW (PR #1453; hồ sơ land PR #1456) đã land. |
| `review_class` | `sensitive`: `scripts/tl_gws.py` `_secrets_set_body` là đường GHI credential (bundle `tl_secrets.enc` và hai tệp public `.enc` trên Drive). |
| `base` | `0f9aa2a2cc697129e1f5be72feddf60986286865` (origin/master lúc soạn; tree `da48b7d3aa2c430499461a35c82f52a96ff5e07f`). Blob `scripts/tl_gws.py` `fbeb9421edd0a7e451534a92c89d090c4de4b3a4`, sha256 `7c31d2b3f37bd1ac93a546eeda50fb07fd17e836414c3ce17b35ab8a7f291941` (bằng bản sau land N, `8048551`). Phiên thi hành đo lại §0 trên base thật của lease và DỪNG nếu lệch. |

Các mục **[ĐÃ CHỐT Qn]** dưới đây là quyết định của chủ kho ngày 2026-11-20 (phiên điều phối #1206); muốn đổi thì phải ra revision mới.

## 0. Hiện trạng (đo trên `0f9aa2a`, chỉ Linux)

Bằng chứng chạy được ở `ops/reviews/wp433-secrets-set-spec-r1/`: `tai_hien.py` (runner), `tai-hien-linux.txt` (base), `nguyen-mau.diff`, `nguyen-mau-linux.txt`.
Runner nạp `scripts/tl_gws.py` vào module MỚI trong bộ nhớ, thay MỌI hàm tải/ghi/mạng bằng đồ giả CÓ ĐẾM (`_secrets_fetch`, `_secrets_upload`,
`_stage_enc_upload`, `_gws_export_cred`, `_refresh_nlm_auth`, `_nlm_auth_files`, `_nlm_files_after_live_canary`, `_gas` ném lỗi, `load_creds` rỗng), bọc
`gws_cred_store.encrypt` để ghi KHOÁ được dùng, HOME/TL_* tạm, `TL_MASTER_KEY` giả. KHÔNG mạng, KHÔNG Drive, KHÔNG secrets thật.

- **Luồng (`scripts/tl_gws.py`, số dòng trên base):** `cmd_secrets_set` (992) bọc thân bằng `_nlm_contained` (913–922): mọi ngoại lệ ⇒ rc 5 và câu
  "Kiểm Drive trước khi coi là chưa upload gì". `_secrets_set_body` (999): khoá ghi → `fid` → `load_creds` → `_secrets_fetch` → giải mã
  `bundle = json.loads(store.decrypt(blob, master)…)` (1014; lỗi giải mã ⇒ rc 3, 1015–1017) → cờ theo thứ tự `--gas-token` (1021) · `--webapp` ·
  `--gws` (gọi `_gws_export_cred`) · `--nlm` (gọi `_refresh_nlm_auth` rồi canary SỐNG `_nlm_files_after_live_canary`) → `if not changed` (rc 1) →
  `_nlm_bundle_guard` → `_secrets_upload` (bundle) → đồng bộ public: khoá `_tok = os.environ.get("TL_TOKEN") or str(bundle.get("token") or "")` (1062),
  mã hoá `gws_cred.enc` / `nlm_cred.enc` bằng `_tok`. `secrets-set` giải mã cùng định dạng bundle với `bootstrap` và `nlm-auth-pull`; `_secrets_fetch` (678) lấy bytes từ
  `--secrets-file` nếu có, không thì thử đường tải (webapp, direct-media). Đồ giả đặt ở ranh giới `_secrets_fetch` nên đo SỐ LẦN tải, không đo I/O nội
  bộ của nó. Đây là chỗ giải mã bundle DUY NHẤT trong `tl_gws.py` còn thiếu kiểm kiểu (1870, 1922 đã có từ packet N).
- **(1) Bundle không phải object** (`[1,2]`, `"chuoi"`, `7`, `null`, `true`) × cờ (`--gas-token`, `--webapp`, `--gws`, `--nlm`, không cờ) = 25 lượt:
  - 20 lượt có cờ: **rc 5**, đúng một dòng `[secrets-set] ✗ dừng vì lỗi TypeError — … Kiểm Drive trước khi coi là chưa upload gì.`; `upload = 0`,
    `stage_enc = 0` (không ghi một phần lên Drive — câu "Kiểm Drive…" chỉ ngược thực tế). Tác dụng phụ TRƯỚC khi vỡ: `--gws` ⇒ `gws_export = 1`;
    `--nlm` ⇒ `nlm_refresh = 1` và **`canary = 1` (canary sống thừa)**.
  - 5 lượt không cờ: rc 1, `⚠ không có trường nào để đổi` (không lộ kiểu sai).
- **(2) Bundle object, `token` không phải str, không `TL_TOKEN`** (`[1]`, `{"a": 1}`, `7`) × (`--gws`, `--nlm`) = 6 lượt: **rc 0**, `upload = 1`,
  `stage_enc = 1`, tệp public mã hoá bằng khoá `'[1]'` / `"{'a': 1}"` / `'7'` (repr của giá trị), KHÔNG cảnh báo nào.
- **(3) Hồi quy, bundle object hợp lệ** (`{"token": "tok-cu", "webappUrl": "u"}`), sáu lượt theo thứ tự `gas_token`, `webapp`, `gws`, `nlm`, `khong_co`,
  `env_token.gws` (lượt cuối: `TL_TOKEN=tok-env`, token `[1]`, `--gws`): `rc = (0, 0, 0, 0, 1, 0)`; mọi lượt `fetch = 1`, `gas = 0`;
  `upload = (1, 1, 1, 1, 0, 1)`; `stage_enc = (0, 0, 1, 1, 0, 1)`; `gws_export = (0, 0, 1, 0, 0, 1)`; `nlm_refresh = canary = (0, 0, 0, 1, 0, 0)`;
  khoá public `([], [], ['tok-cu'], ['tok-cu'], [], ['tok-env'])`. Số lần `encrypt` không chép cứng (runner chỉ in khoá khác khoá master).
- **Nguyên mẫu** (`nguyen-mau.diff`, `tl_gws.py` +5/−1, đo cùng runner): (1) cả 25 lượt rc 3, đúng một dòng `[secrets-set] ✗ dữ liệu không hợp lệ: bundle`,
  `fetch = 1` và MỌI bộ đếm khác 0 (kể cả `canary`); (2) cả 6 lượt rc 0, `upload = 1`, `stage_enc = 0`, không khoá public, một dòng
  `⚠ thiếu webapp token → KHÔNG đồng bộ được đường public …` (cảnh báo SẴN CÓ); (3) y hệt base.

## 1. `write_set`

```
scripts/tl_gws.py
scripts/test_fragments/wp433_secrets_set_bundle.py
scripts/tl_test_fragments_bundled.py
```

`wp433_secrets_set_bundle.py` là tệp MỚI. KHÔNG `RELEASE_MANIFEST.json`. Bundled chỉ sinh bằng `generate_bundled_module_bytes(scripts/test_fragments)`.
**Điều kiện trước khi cấp lease (E2):** comment của chủ kho trên #433 cấp ngoại lệ bundled nêu đúng `packet_id` `SECRETS-SET-BUNDLE-KIEU`, đúng một tệp
`scripts/tl_test_fragments_bundled.py` và sha256 của đặc tả này đã đóng băng; lease trỏ URL comment. Phiên land tái sinh manifest.

## 2. `ngoai_pham_vi`

- Câu "Kiểm Drive trước khi coi là chưa upload gì" của `_nlm_contained` (dùng chung ba lệnh stage): giữ nguyên; sau M1 bundle sai kiểu không còn đi tới đó.
- Ghi đè `token` sai kiểu trong bundle khi KHÔNG có `--gas-token` (bundle tải về được ghi lại nguyên trường `token`): giữ nguyên — Q2 = A chỉ bỏ đồng bộ public.
- `secrets-stage` (gói từ config cục bộ, `bundle = {}` khi đọc lỗi; `json.load` ra không-object thì `bundle.setdefault` ném ⇒ rc 5): không thuộc nợ này;
  ghi chú để chủ kho quyết nếu muốn mở tiếp.
- Không sửa `ops/**`, `.github/**`, `scripts/tl_selftest.py`, fragment khác, `RELEASE_MANIFEST.json`, `changelog.d/*`, `VERSION`, `CHANGELOG.md`, `SKILL.md`.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | **[ĐÃ CHỐT Q1: rc 3, kiểm ngay]** Ngay sau khối `try/except` giải mã (sau dòng 1017 của base), TRƯỚC `changed = []` và mọi cờ: `bundle` không phải `dict` ⇒ in ĐÚNG một dòng stderr `[secrets-set] ✗ dữ liệu không hợp lệ: bundle`, trả **3**; không gọi `_gws_export_cred`, `_refresh_nlm_auth`, canary, `encrypt`, upload nào. Nguyên văn ở `nguyen-mau.diff` (hunk 1; cùng hình dạng dòng 1870/1922). | `scripts/tl_gws.py` |
| M2 | **[ĐÃ CHỐT Q2: A, coi như thiếu]** Ở dòng 1062 của base: khoá public lấy `TL_TOKEN`; không có thì `bundle.get("token")` CHỈ KHI là `str`, ngược lại `""` ⇒ rơi vào nhánh cảnh báo SẴN CÓ "thiếu webapp token → KHÔNG đồng bộ được đường public" (rc giữ nguyên, bundle vẫn upload). Không dùng `str(...)`/`repr` của giá trị khác str làm khoá. Nguyên văn ở `nguyen-mau.diff` (hunk 2). | `scripts/tl_gws.py` |
| M3 | Fragment MỚI `wp433_secrets_set_bundle.py`, `TEST_ID = "wp433_secrets_set_bundle"`, khuôn fragment N/R: bản `tl_gws` nạp TRONG BỘ NHỚ (nguồn thật hoặc đột biến), HOME/TL_* tạm, dữ liệu GIẢ, MỌI hàm tải/ghi/mạng thay bằng đồ giả CÓ ĐẾM như runner §0 (không một lời gọi mạng nào — `_gas` giả ném lỗi), `encrypt` bọc để ghi khoá; `TinHieuChotCa(ca, lượt, nhãn)` riêng; sổ lượt `_LUOT_DU_KIEN` viết riêng khỏi hàm ca; mọi đầu ra ra stderr; `run(tl)` trả True/False. Ba ca theo §4. | fragment mới |
| M4 | Tái sinh bundled; không sửa tay. | bundled |

## 4. `nghiem_thu`

| # | ca | tiêu chí (mỗi lượt một hậu điều đầy đủ, nhãn đỏ ĐẦU TIÊN thành tín hiệu) | phép đo làm nó ĐỎ |
|---|---|---|---|
| N1 | `kieu` — 25 lượt theo thứ tự `list, str, int, null, true` × `gas_token, webapp, gws, nlm, khong_co` | nhãn `rc3`: rc == 3; `dong`: TOÀN BỘ `stderr.splitlines()` bằng đúng danh sách một phần tử `["[secrets-set] ✗ dữ liệu không hợp lệ: bundle"]` (không dòng nào khác, kể cả dòng thường); `khong_goi`: `fetch == 1` và mọi bộ đếm khác (`upload`, `stage_enc`, `gws_export`, `nlm_refresh`, `canary`, `gas`, số lần `encrypt`) == 0 | Base: lượt đầu `kieu.list.gas_token` đỏ ở `rc3` (rc 5, đã đo). |
| N2 | `token_kieu` — 6 lượt: token `[1]`, `{"a": 1}`, `7` × `gws`, `nlm`; không `TL_TOKEN` | `rc0`: rc == 0; `upload1`: `upload == 1`; `khong_public`: `stage_enc == 0` và không khoá nào ngoài `TL_MASTER_KEY` được dùng cho `encrypt`; `canh_bao`: đúng một dòng chứa `thiếu webapp token`, không dòng `✗` | Base: `token_kieu.list.gws` đỏ ở `khong_public` (khoá `'[1]'`, đã đo). |
| N3 | `hoi_quy` — 6 lượt: bundle object hợp lệ × 5 cờ, cộng `TL_TOKEN=tok-env` + token `[1]` + `--gws` | rc, MỌI bộ đếm (`fetch`, `gas`, `upload`, `stage_enc`, `gws_export`, `nlm_refresh`, `canary`) và danh sách khoá public BẰNG bảng §0 (3), chép cứng trong fragment | Bất kỳ lệch nào (base phải ĐẠT ca này). |
| N4 | gate | selftest N/N hai số bằng nhau, N = N_base + 1; `test-fragments-check --json` `ok: true`; `bundle_fragment_check.py --json` `ok: true`, `failed: []`; lane worker `release-manifest` tạm + `release-verify --strict` `ok: true`; `git diff --check` sạch; `doctrine-scan`, `adr-song` rc 0; ruff F delta 0; các fragment #433 đã có (`wp433_*`) `run()` True với bộ đếm BẰNG base. | Bất kỳ vế nào khác. |
| N5 | đo native D1 (§4c) | Hồ sơ PR packet ghi lệnh, shell, exact head/tree base và candidate đã ghim, đầu ra thô, rc và kết luận của D1 (cả hai vế). | Thiếu, sai SHA/tree, không chạy được (`KHÔNG ĐO ĐƯỢC`) hoặc trái kỳ vọng ⇒ không land. |

Phép đo base/head dựng hai clone trong MỘT lệnh (CLAUDE.md). Fragment chạy trên `tl_gws.py` của base phải ĐỎ (`run()` False) đúng ở N1 rồi N2 —
đo bằng cách nạp nguồn base vào fragment của candidate (không sửa base).

### 4b. Đột biến (bảng `_DB` của fragment; mỗi đột biến neo khớp ĐÚNG một lần trên nguồn candidate)

| # | tên | đột biến | ca · lượt đích | nhãn |
|---|---|---|---|---|
| 1 | `db_bo_kiem_kieu` | xoá ba dòng của M1 | `kieu` · `kieu.list.gas_token` | `rc3` |
| 2 | `db_kieu_chi_list` | `isinstance(bundle, dict)` → `isinstance(bundle, (dict, str))` | `kieu` · `kieu.str.gas_token` | `rc3` |
| 3 | `db_kieu_thong_diep` | thông điệp M1 `dữ liệu không hợp lệ: bundle` → `giải mã lỗi: bundle` (rc 3 giữ nguyên) | `kieu` · `kieu.list.gas_token` | `dong` |
| 4 | `db_token_repr` | dòng `_tok` của M2 về `str(bundle.get("token") or "")` | `token_kieu` · `token_kieu.list.gws` | `khong_public` |

Phân hạng như fragment N: GIẾT chỉ khi tín hiệu là `TinHieuChotCa` khớp đúng (ca, lượt, nhãn); chết vì lý do khác là TÍN DỤNG GIẢ; neo không khớp đúng một
lần là HỎNG. Vì `_nlm_contained` biến MỌI ngoại lệ trong thân lệnh thành rc 5 (một lỗi vô can cũng sinh đúng tuple `rc3` của đột biến 1), đột biến 1 và 2
chỉ tính GIẾT khi khớp tuple VÀ lượt đích quan sát được rc 5 kèm đúng một dòng `[secrets-set] ✗ dừng vì lỗi TypeError …` (đúng cơ chế đã đo ở §0);
rc 5 với lớp khác (vd `AttributeError`) ⇒ TÍN DỤNG GIẢ. Đột biến 1 và 2 cùng nhãn `rc3` nhưng khác LƯỢT đích (đột biến 2 để `list` qua đúng, chỉ đỏ ở `str`); đột biến 3 giữ rc 3 nên chỉ nhãn `dong`
bắt được — ba đột biến phân biệt được bằng đầu vào. Dời kiểm M1 xuống sau các cờ KHÔNG phải đột biến riêng: mọi vị trí sau cờ đầu tiên vỡ `TypeError` ở
lượt đầu (`kieu.list.gas_token`, rc 5) y như đột biến 1. Tự kiểm bộ phân hạng ≥ 3 ca: (a) một đột biến giả ném `AttributeError` tại vị trí chốt — bị chính
`_nlm_contained` bắt, cùng ca, lượt `kieu.list.gas_token` và nhãn `rc3` — phải ra TÍN DỤNG GIẢ; (b) một đột biến giả chết vì `AttributeError` qua `except`
đổi kiểu ⇒ TÍN DỤNG GIẢ; (c) một đột biến chú thích vô hại ⇒ SỐNG SÓT.

**Phản chứng bộ đo** (không thuộc `_DB`, chạy trong `run()`; mỗi cái phải ĐỎ đúng chỗ, còn nguồn thật đạt lượt ấy): (PC1) thêm một dòng stderr THƯỜNG
(không `✗`) ngay trước `return 3` của M1 ⇒ đỏ `kieu.list.gas_token` · `dong`; (PC2) khi có `--gws`, gọi `_gws_export_cred()` (giả) ngay TRƯỚC khi từ chối
bundle sai kiểu, rc và stderr vẫn đúng ⇒ đỏ `kieu.list.gws` · `khong_goi` (trong khi `kieu.list.gas_token` vẫn đạt). Phản chứng không đỏ đúng chỗ ⇒ `run()` False.

### 4c. Đo native Windows — **[ĐÃ CHỐT Q3: đo một lượt D1 nhẹ]** (`DESKTOP-T9R33P2`, dự phòng VM)

Ghim exact head/tree; clone `git -c core.longpaths=true`; `python`; rig dùng một lần do phiên thi hành soạn, đăng comment PR (gzip+base64 + sha256, qua REST);
chạy dưới thư mục phiên; dọn đúng thứ mình tạo; offline (fragment không mạng). Ngân sách Windows native của lease ≤ 2.

| # | bắt buộc | dựng / lệnh | kỳ vọng |
|---|---|---|---|
| D1 | có | `run(tl)` fragment `wp433_secrets_set_bundle` của candidate, mỗi vế một tiến trình, mỗi vế MỘT lần: (a) candidate; (b) nguồn `tl_gws.py` của base nạp vào fragment candidate | (a) `True`, bộ đếm `CA 3/3 · LUOT 37/37 · DOT BIEN 4/4 · HONG 0 · TU_KIEM …` BẰNG lượt Linux; (b) `run=False`, đỏ ĐÚNG ca `kieu` lượt `kieu.list.gas_token` nhãn `rc3`; chạy riêng ca `token_kieu` đỏ đúng `token_kieu.list.gws` · `khong_public`; chạy riêng ca `hoi_quy` đạt đủ 6/6 lượt. Rig chạy (a) và (b) thành HAI tiến trình, mỗi cái một lần |
| — | (T3, ngoài §4c) | Theo `docs/PROTOCOL_DA_PHIEN.md` §10.1: T3 đo trên SHA tích hợp đã đóng băng ở `land prepare` (selftest + gate lane LAND, kèm PR tái sinh manifest); bằng chứng ghi ở checkpoint land/hồ sơ land, KHÔNG thuộc N5 của PR packet | xanh |

## 5. `pham_vi_e`

Không chạm E4, E5: chỉ đổi kiểm kiểu và chọn khoá trước các đường ghi; dữ liệu giả, thư mục tạm, không mạng, không LIVE, không đẩy Package, không chạy
`secrets-set` thật.

## 6. `luat_dung`

- Trần lời gọi Codex theo `ADR-0055`; trần kích thước `ADR-0053` (≤ 6 tệp, ≤ 450 dòng thêm) đo bằng numstat thật trước khi công bố; tập đường diff phải
  bằng ĐÚNG ba đường của §1 (write set của packet); vượt hoặc lệch ⇒ DỪNG, nâng trần là **E2**.
- §0 lệch trên base thật (dòng 1014–1017, 1062; hành vi (1)(2)(3)) ⇒ dừng, revision.
- Fragment trên nguồn base không đỏ đúng N1/N2, hoặc `hoi_quy` lệch bảng §0 (3) ⇒ dừng.
- Một fragment #433 đã có đổi bộ đếm so base ⇒ dừng.
- D1 (a) không `True`, hoặc (b) không đỏ đúng đích, hoặc thiếu đầu ra / sai SHA-tree / không khởi chạy được (`KHÔNG ĐO ĐƯỢC`) ⇒ dừng; trái kỳ vọng ⇒ revision.
- Chưa có comment ngoại lệ bundled đúng `packet_id` ⇒ không cấp lease (**E2**). Đặc tả chờ chủ kho duyệt băm theo `ADR-0067` (**E2**).

## 7. `hinh_dang_ke_thua`

Cùng lớp với M3 của packet N (bundle JSON hợp lệ mà không phải object ⇒ từ chối như giải mã lỗi, TRƯỚC mọi tác dụng phụ). Khác N ở chỗ lỗi cũ
đã bị `_nlm_contained` bắt (rc 5, không traceback) nhưng (a) chạy canary SỐNG thừa trước khi vỡ và (b) báo người dùng "kiểm Drive" khi không có gì được ghi.
M2 thuộc họ "khoá suy ra từ dữ liệu chưa kiểm kiểu": `str()` biến một giá trị sai kiểu thành một khoá HỢP LỆ VỀ HÌNH THỨC — lỗi không ồn ào mà âm thầm.

## 8. `chua_do_duoc` và dự toán

- Numstat dự kiến: `tl_gws.py` +5/−1 (đo trên nguyên mẫu) · `wp433_secrets_set_bundle.py` ước 170–240 · `tl_test_fragments_bundled.py` ~+2/−1
  ⇒ **3 tệp, ~180–250 dòng thêm**, dưới trần 450.
- Chưa đo: fragment mới (việc của phiên thi hành); native Windows D1 (§4c); EACCES/khác nền — không liên quan (không chạm hệ tệp).

## 9. Lịch sử và quyết định

- Chủ kho 2026-11-20: mở việc riêng cho nợ `secrets-set` sau khi P2BW land.
- **ĐÃ CHỐT 2026-11-20** (phiên điều phối #1206): Q1 = rc 3, kiểm ngay sau giải mã trước mọi cờ (khuyến nghị); Q2 = A, `token` không phải str ⇒ coi như thiếu
  (khuyến nghị); Q3 = ĐO một lượt D1 nhẹ trên Desktop (khác khuyến nghị "miễn"); chủ kho muốn Codex review đặc tả TRƯỚC khi duyệt băm.
- Bản soạn đầu (`d264d300…`, chưa push) mất khi container của phiên bị thay; bản này soạn lại và đo lại trên `0f9aa2a`.

## 10. Nhật ký revision

- 2026-11-20T12:5xZ (phiên con của điều phối #1206): bản 1 soạn lại, đo §0 trên `0f9aa2a` (Linux), ghi Q1–Q3 đã chốt.
- 2026-11-20T12:4xZ (phiên con của điều phối #1206): Codex lượt 1/10 `request_changes` (3 P2, 2 P3), sửa hết: N1 `dong` so TOÀN BỘ stderr; hai phản chứng
  bộ đo PC1 (dòng stderr thừa) và PC2 (export trước khi từ chối); đột biến 1–2 chỉ GIẾT khi thấy đúng `TypeError` qua `_nlm_contained` + tự kiểm
  `AttributeError` bị wrapper bắt; N5 chỉ D1, T3 chuyển về `land prepare` (§10.1), §6 thêm `KHÔNG ĐO ĐƯỢC`; §0(3) chép đủ bộ đếm; §0 nêu `--secrets-file`;
  §6 trần ADR-0053 đúng là 6 tệp/450 dòng, write set 3 đường.
