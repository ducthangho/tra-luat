tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# GWS-CRED-DICH-NGOAI-KHO-B r1 — dữ liệu ghi qua W6 (`token`/`webappUrl` vào env, `~/.tra_luat_config.json`) phải được kiểm TRƯỚC khi gán env và trước khi ghi; không ngoại lệ nào thoát khỏi `cmd_bootstrap`

- packet_id: GWS-CRED-DICH-NGOAI-KHO-B; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Issue #433. Chủ kho 2026-11-19 (phiên điều phối #1206, AskUserQuestion, Q1 tầng một của đặc tả P2a) tách kiểm DỮ LIỆU W6 khỏi `GWS-CRED-DICH-NGOAI-KHO` thành **P2b** `GWS-CRED-DICH-NGOAI-KHO-B`; đường Windows/UNC là **P2c** (packet khác). Nội dung chuyển sang đây, theo §2 của đặc tả P2a (`ops/specs/GWS-CRED-DICH-NGOAI-KHO-A-r1.md`, nhánh `ops/wp433-p2a-spec`, sha256 `b0065947…`): M7 cũ (kiểm dữ liệu W6), ca `w6_du_lieu` (N9w6 cũ), ca hồi quy `jar_rong_base` (N3d cũ), đột biến dòng 24–29 cũ. Nguồn của các mục cũ: bản lưu `ops/reviews/wp433p2a-spec-r1/dac-ta-ban0-truoc-tach.md` trên cùng nhánh. |
| `phu_thuoc` | Packet 1 `NLM-GWS-DICH-NGOAI-KHO` (PR #1394, merge `700fbca`) và P2a `GWS-CRED-DICH-NGOAI-KHO-A` (PR #1415, merge `417b593`) ĐÃ LAND. P2b sửa thân `cmd_bootstrap` ở đoạn W6 do packet 1 viết; giữ nguyên `_kiem_dich_ghi`, `_ghi_nguyen_tu_0600`, `_kiem_jar_nlm`, `_dich_cred_gws` và hợp đồng lỗi (M4 packet 1, M3 P2a: một dòng `[thẻ] ✗ <cụm>: <chi tiết>`, `degraded`). |
| `review_class` | `sensitive`: `scripts/tl_gws.py` là đường ghi credential (`TL_TOKEN` và `~/.tra_luat_config.json` mang token GAS). Đối chiếu bằng `lease_publish check` khi cấp lease. |
| `base` | `11bd0336d00b4a9544e70dcbbe049d372053a3ec` lúc soạn (`origin/master`, 2026-11-19T10:0xZ, đã chứa `417b593`); blob `scripts/tl_gws.py` `9ec027c2808868a05b67adc3d93ea68a574d6ec0`, 2649 dòng. Lease ghi OID base thật lúc cấp; phiên thi hành đo lại §0 trên base ấy trước khi sửa. |

## 0. Hiện trạng (đo trên `11bd033`, Linux, Python 3.13.18 trừ chỗ ghi khác, dữ liệu GIẢ, không mạng; giờ là giờ máy)

### 0.1 Chỗ ghi thuộc packet

W6 nằm trong `cmd_bootstrap` (định nghĩa 1740): giải mã bundle (1766), `degraded = False` (1771), kiểm jar (1772–1775), rồi
`if bundle.get("token"):` (1777) ⇒ `os.environ["TL_TOKEN"] = bundle["token"]` (1778), `os.environ["TL_WEBAPP"] = bundle["webappUrl"]` khi
truthy (1779–1780), chốt đích `_kiem_dich_ghi(cfgp, cfgp, ())` (1784), đọc `existing` (1787, `except Exception` ⇒ `{}`), `existing.update(…)`
(1791), `_ghi_nguyen_tu_0600(cfgp, json.dumps(existing, ensure_ascii=False).encode("utf-8"))` (1792), `except OSError` (1794); nhánh thiếu
token in `[bootstrap] ⚠ bundle thiếu GAS token.` (1799) và KHÔNG đặt `degraded`. Không có kiểm kiểu/NUL/encode nào trước 1778, 1780, 1791, 1792.

Hai nhánh định dạng jar KHÔNG đổi của packet 1 (đo hồi quy ở N2): W1 `cmd_nlm_auth_pull` `if not nlm:` (1722) ⇒ dòng `⚠ bundle chưa có
nlm_auth …`, rc 1; W3 `_nlm_auth_load` `if not isinstance(nlm, dict) or not nlm:` (2035) ⇒ `(False, "nlm_cred rỗng/sai định dạng.")`;
W2 `ly_jar = _kiem_jar_nlm(jar) if jar else None` (1773).

### 0.2 Phép đo hành vi base (`do_w6.py` B*, 2026-11-19T10:04:21Z; `do_locale.py` L*; `cmd_bootstrap --env chat`, HOME tạm, config cũ `{"token": "CU"}`)

| phép | bundle / config cũ | base `11bd033` |
|---|---|---|
| B0 | `token`, `webappUrl`, `rootFolderId` hợp lệ | rc 0, hai biến đặt, config merge, đúng một dòng `agent_creds:` |
| B1, B18 | `token` = `5`, `["a"]` | `TypeError: str expected, not int/list` THOÁT; không biến, config giữ byte, 0 dòng `agent_creds:` |
| B2 | `token` = `"a\ud800"` (chuỗi thoát JSON) | `UnicodeEncodeError … surrogates not allowed` THOÁT ở phép gán env |
| B3 | `token` = `"a\udc80"` | phép gán env THÀNH CÔNG (surrogateescape), rồi `UnicodeEncodeError` THOÁT ở 1792: `TL_TOKEN` đã đổi, config giữ byte |
| B4 | `token` chứa `\u0000` | `ValueError: embedded null byte` THOÁT |
| B5, B6, B7 | `webappUrl` chứa NUL / `7` / `\ud800`; env có sẵn `TL_TOKEN`, `TL_WEBAPP` | THOÁT (`ValueError` / `TypeError` / `UnicodeEncodeError`) SAU khi `TL_TOKEN` đã bị ghi đè; `TL_WEBAPP` giữ |
| B8, B17 | `rootFolderId` = `"\ud800"`; khoá `"\ud800"` | `TL_TOKEN` đặt, `UnicodeEncodeError` THOÁT ở 1792, config giữ byte |
| B12 | config cũ `{"x": "\ud800"}` | như B8 |
| B9, B10, B11 | config cũ `[]`, `null`, `"s"` | `AttributeError: '<kiểu>' object has no attribute 'update'` THOÁT ở 1791; `TL_TOKEN` đặt; config giữ byte |
| B19 | config cũ không parse được | rc 0, config ghi lại `{"token": …}` (nhánh `except Exception` ⇒ `{}`) |
| B13, B14, B15 | `token` = `0`, `null`, `""` | rc 0, dòng `⚠ bundle thiếu GAS token.`, không biến, config giữ |
| B16 | `webappUrl` = `0` | rc 0, `TL_WEBAPP` KHÔNG đặt, config mang `"webappUrl": 0` |
| B20 | bundle là `[1]` | `AttributeError … 'get'` THOÁT ở 1772 (TRƯỚC W6 — ngoài phạm vi, §2) |
| L1 (10:42:08Z) | `webappUrl` = `"https://x/é"`, tiến trình chạy `LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0` (KHÔNG `-I`; `sys.getfilesystemencoding()` = `ascii`) | `UnicodeEncodeError … 'ascii' codec` THOÁT ở phép gán `TL_WEBAPP`, SAU khi `TL_TOKEN` đã đổi. Cùng giá trị dưới locale UTF-8: rc 0 |
| L2, L3 (10:42:00Z) | bundle mang `"extra": 1e999`; config cũ `{"x": NaN}` | rc 0, config ghi `Infinity` / giữ `NaN` — JSON ngoài chuẩn, không dòng lỗi |

Mọi ca THOÁT: không dòng `[bootstrap] ✗`, không dòng `agent_creds:`, không mã thoát (traceback). Bộ ba Python 3.11.18 / 3.12.3 / 3.13.18
(cùng lúc): `os.environ[k] = 7` ⇒ `TypeError: str expected, not int`; `"\udc80"` ⇒ thành công; `"a\x00b"` ⇒ `ValueError: embedded null byte`;
`"\ud800"` ⇒ `UnicodeEncodeError … surrogates not allowed`; `"\x00" in 7` ⇒ `TypeError: argument of type 'int' is not iterable`. Thông điệp
`str expected, not <kiểu>` do `os._createenviron` dựng, CÙNG chuỗi trên nhánh `nt` (đọc nguồn `os.py` 3.13, không đo trên Windows).

### 0.3 Ràng buộc kề bên (đo trên NGUỒN ỨNG VIÊN prototype của M1–M3, dựng ngoài kho bằng `va_ung_vien.py`, không commit; bản prototype hiện hành sha256 `22baf3fd…`, đo 10:43Z–10:47Z)

- Prototype: `tl_gws.py` **+29/−2** (`git diff --no-index --numstat`); `ruff check --select F --output-format concise` trên `tl_gws.py`:
  95 chẩn đoán ở base và ở prototype (delta 0; đo trên bản prototype đầu, 10:1xZ, phần thêm sau không thêm tên mới).
- **Bẫy neo đã đo:** P2a neo đột biến `db_w4_bo_kiem_encode` vào chuỗi `"            except UnicodeEncodeError:\n"` (12 dấu cách). Một
  `except UnicodeEncodeError:` thụt 16 dấu cách CHỨA chuỗi ấy ⇒ fragment P2a báo `ĐỘT BIẾN db_w4_bo_kiem_encode: HONG`, `run` False
  (đo 10:10Z trên prototype đầu). Prototype hiện hành bắt `ValueError` (M3) và mang chú thích cùng dòng: fragment P2a `giết_đúng=37`,
  `TU_KIEM 3/3`, `run` True; fragment packet 1 `giết_đúng=30`, `run` True (10:46:30Z). Neo packet 1 nằm trong đoạn W6:
  `ly_cfg = _kiem_dich_ghi(cfgp, cfgp, ())`, `' and not (k == "nlm_auth" and ly_jar)'`, dòng in `✗ {ly_cfg}` kèm `degraded = True`,
  `ly_cfg = f"ghi lỗi: …"`, chú thích `# 2) gws …`, dòng `--require-agent-creds`; `ly_jar = _kiem_jar_nlm(jar) if jar else None`.
- Neo PD của `ops/cloud_agent_creds_test.py` (bảng 796–806) nằm ngoài đoạn W6. `CAC_TLGWS=<tệp>`: base và prototype đầu đều `TONG: DAT`,
  `DOT BIEN: 91/91`, tự kiểm phân hạng `DAT (4 dot bien)` (10:15:43Z–10:26Z); prototype hiện hành: cùng kết quả (10:53:07Z).
- Không tệp nào khác trong kho neo chuỗi của đoạn W6 (`grep` `bundle thiếu GAS token`, `config (token +`, phép gán `TL_TOKEN`, 10:22Z).
- Bước CI `bundled-fragment check` kiểm bundled committed trên PR; manifest committed chỉ bị kiểm trên master. Driver
  `bundle_fragment_check.py` đọc stdout tiến trình con làm JSON: fragment in ra stderr. `chay_frag.py`/driver trả rc 0 kể cả khi `run`
  False — mọi phép đo fragment đọc giá trị `run`, không đọc rc (review lượt 1).

## 1. `write_set`

```
scripts/tl_gws.py
scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho_b.py
scripts/tl_test_fragments_bundled.py
```

`scripts/tl_test_fragments_bundled.py`: worker mang riêng tệp ấy, chỉ sinh bằng `generate_bundled_module_bytes(scripts/test_fragments)`,
KHÔNG mang `RELEASE_MANIFEST.json` — ngoại lệ so với `docs/PROTOCOL_DA_PHIEN.md` (879–882 ở `11bd033`), cùng phương án B chủ kho chọn
18-11-2026 cho packet 1 và P2a. **Điều kiện trước khi cấp lease (E2, §9 Q1):** comment của chủ kho trên Issue #433 nêu đúng `packet_id`
`GWS-CRED-DICH-NGOAI-KHO-B`, đúng một tệp `scripts/tl_test_fragments_bundled.py` và sha256 của đặc tả này đã đóng băng; lease trỏ URL
comment. Comment `6973856830` (packet 1) và `7002145681` (P2a) không phủ packet này. Phiên land tái sinh `RELEASE_MANIFEST.json`.

## 2. `ngoai_pham_vi`

- Mọi thứ Windows/UNC: P2c. Mã của P2b không rẽ nhánh theo nền; khẳng định đo chỉ trên POSIX (§8).
- Chốt TỔ TIÊN cho đích W6: W6 vẫn gọi `_kiem_dich_ghi(cfgp, cfgp, ())`, chỉ kiểm lá config và luật kho — không sửa ở đây (§9 Q2).
- Bundle KHÔNG phải `dict` (B20): ném ở 1772, trước W6, trong mã kiểm jar của packet 1 — không sửa ở đây (§9 Q3).
- Không kiểm định dạng `webappUrl` (URL hợp lệ hay không), không kiểm kiểu các khoá khác của bundle (`rootFolderId`, …): chúng chỉ đi
  vào config, nơi duy nhất làm hỏng là tuần tự hoá (M3).
- Điều kiện vào nhánh token GIỮ của base (`bundle.get("token")` truthy): `token` falsy (`0`, `null`, `""`) đi nhánh `⚠ bundle thiếu GAS
  token.` như B13–B15 — không gán env, không ghi, nên không có rủi ro dữ liệu. `webappUrl` falsy giữ base (B16: không gán env, merge vào
  config như mọi khoá khác). Hai lựa chọn này có lượt đo và đột biến riêng (N1 `token_falsy`, `web_falsy`).
- Không sửa THÂN `_kiem_dich_ghi`, `_trong_kho_git`, `_ghi_nguyen_tu_0600`, `_kiem_jar_nlm`, `_dich_cred_gws`, `_duong_dich_chuan`, các nhánh
  định dạng jar W1/W2/W3 (§0.1); không sửa `ops/**`, `.github/**`, `scripts/tl_selftest.py`, `RELEASE_MANIFEST.json`, `changelog.d/*`,
  `VERSION`, `CHANGELOG.md`, `SKILL.md`, fragment của packet 1 và P2a.
- TOCTOU: như §2 P2a — chốt và ghi theo TÊN; không chống đối thủ đồng thời. Không đo.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Hàm `_kiem_env_w6(bundle)` trả `None` hoặc `dữ liệu không hợp lệ: <tên trường>`. Duyệt `token` rồi `webappUrl`; `token` luôn được kiểm (người gọi chỉ gọi khi `bundle.get("token")` truthy), `webappUrl` chỉ khi truthy (cùng điều kiện gán env của base, 1779). Giá trị hợp lệ khi, theo thứ tự: là `str`; không chứa `"\x00"`; `.encode("utf-8")` thành công (từ chối cả `\udc80` mà env POSIX vẫn nhận — B3); và khi `os.name == "posix"`, `.encode(sys.getfilesystemencoding(), "surrogateescape")` thành công — đúng phép mã hoá `os.environ` POSIX dùng (`os._createenviron`), nên locale ASCII từ chối thay vì ném ở phép gán (L1). Bắt `ValueError` (gồm `UnicodeEncodeError`). MỘT hàm dùng chung cho cả hai trường (bảng §4b neo vào hình dạng này). Lý do CHỈ nêu tên trường, không nội suy giá trị (token là bí mật). | `scripts/tl_gws.py` |
| M2 | W6 trong `cmd_bootstrap`: gọi M1 khi `bundle.get("token")` truthy, TRƯỚC mọi phép gán `os.environ` của W6. Có lý do ⇒ ĐÚNG MỘT dòng `[bootstrap] ✗ <lý do>` ra stderr, `degraded = True`; KHÔNG gán `TL_TOKEN`/`TL_WEBAPP` (giữ đúng giá trị TẠI ĐẦU W6, tức sau `load_creds` dùng để tải bundle); KHÔNG gọi chốt đích, KHÔNG đọc, KHÔNG gọi writer cho `~/.tra_luat_config.json`; KHÔNG dừng lệnh: các nhánh sau (gws, nlm, agent) chạy như khi W6 thành công, tới đúng một dòng `agent_creds:`. Mã thoát theo luật sẵn có: rc 1 vì `degraded`, trừ `--require-agent-creds` với agent chưa `ĐÃ NẠP` thì rc 4 kèm dòng riêng của cờ (§0.1 P2a). Dòng lỗi jar (packet 1, in TRƯỚC W6) và dòng của cờ được đếm riêng, W6 không nuốt hay gộp chúng. Không lý do ⇒ đường base (gán env, chốt đích, đọc, merge, ghi) cộng M3. Token falsy ⇒ nhánh `⚠` của base, không đổi. | `scripts/tl_gws.py` |
| M3 | Hai kiểm dữ liệu ở bước config (chỉ khi `ly_cfg is None` sau chốt đích của packet 1): (b) `existing` đọc được mà không phải `dict` ⇒ coi như không parse được: `existing = {}`, không dòng lỗi, rc không đổi (như B19); (c) `json.dumps(existing, ensure_ascii=False, allow_nan=False).encode("utf-8")` chạy TRƯỚC writer trong một `try` CHỈ bọc đúng bước ấy, bắt CHỈ `ValueError` (NaN/±Infinity — L2, L3 — và `UnicodeEncodeError` — B8, B12, B17) ⇒ lý do `dữ liệu không hợp lệ: config`, không gọi writer, config giữ byte, `TL_TOKEN`/`TL_WEBAPP` đã gán ở M2 GIỮ, dòng `✓ config` không in. Lý do (c) đi qua đúng dòng in `✗ {ly_cfg}` sẵn có của packet 1 (một dòng, `degraded = True`). Không dòng mới nào được chứa chuỗi neo của fragment packet 1/P2a (§0.3; ví dụ đã đo: `"            except UnicodeEncodeError:\n"`). | `scripts/tl_gws.py` |
| M4 | Fragment `scripts/test_fragments/wp433_gws_cred_dich_ngoai_kho_b.py`, `TEST_ID = "wp433_gws_cred_dich_ngoai_kho_b"` (khớp `_PACKET_TEST_ID_PATTERN`, `scripts/tl_core/test_fragments.py:23`), `run(tl_module)`, cùng khuôn fragment P2a nhưng tự chứa: nạp `tl_gws` trong bộ nhớ (nguồn thật hoặc đột biến), `bind`; rig HOME/`USERPROFILE`/`CODEX_HOME`/`GOOGLE_WORKSPACE_CLI_CONFIG_DIR`/`TL_*`/cwd tạm dưới `realpath(mkdtemp())`, khôi phục trong `finally`; đồ giả có đếm cho `_secrets_fetch`, `_public_curl_bytes`, `load_creds`, `_gas` (`MANG_BI_CHAN`), `_ensure_nlm_installed`, `cmd_gws_bootstrap_cowork`, `gws_exe`; `AGENT_CREDS_FILEID = ""`. Trong cửa sổ MỖI lượt: chặn `subprocess`/`urlopen`; bộ quan sát đếm lời gọi `_kiem_dich_ghi` có `dich` = đường config, lần mở ĐỌC đường config qua `builtins.open`, lời gọi `_ghi_nguyen_tu_0600` có đích = đường config; lượt có cột "giả lập" thay `sys.getfilesystemencoding` hoặc `_bootstrap_agent_creds` trên module; mọi thứ khôi phục trong `finally`. Mọi đầu ra ra STDERR; đột biến trên bản sao trong bộ nhớ, neo khớp đúng 1 lần, phân hạng bằng `TinHieuChotCa(AssertionError)` theo (ca, lượt, nhãn); `_LUOT_DU_KIEN` và `_DU_KIEN` viết RIÊNG khỏi hàm ca và `_DB`. | fragment |
| M5 | Tái sinh `scripts/tl_test_fragments_bundled.py` bằng `generate_bundled_module_bytes(scripts/test_fragments)`; không sửa tay; không đụng `RELEASE_MANIFEST.json`. | bundled |

## 4. `nghiem_thu`

Ký hiệu: TOK, WEB = token/URL giả hợp lệ; SENT = `SENTINEL-wp433b-…` (nằm trong MỌI giá trị sai dạng chuỗi); CU = byte config cũ
`{"token": "CU-wp433b"}`; "trước" = cặp (`TL_TOKEN`, `TL_WEBAPP`) tại đầu W6 — rig thay `load_creds` bằng đồ giả không làm gì và đặt sẵn
cặp giá trị riêng ngay trước lời gọi, nên "trước" = cặp ấy. "Fixture W6" = `cmd_bootstrap --env chat`, HOME tạm ngoài mọi kho có config CU,
agent giả `KHÔNG CẤU HÌNH` — env `chat` chỉ chạy W6 và dòng agent, nên rc của lượt chỉ đến từ W6 (B0: rc 0). Mỗi lượt THU ĐỦ hậu điều rồi so
nhãn theo thứ tự ghi; nhãn đỏ ĐẦU TIÊN là nhãn của tín hiệu; lượt chạy theo thứ tự ghi. Ngoại lệ thoát khỏi lời gọi: khớp (loại, dấu)
trong tập khai CỦA LƯỢT (§4b) ⇒ nhãn khai; ngoài tập ⇒ `ngoai_le_la`. "Dòng W6(t)" = nguyên văn `[bootstrap] ✗ dữ liệu không hợp lệ: t`.

**Bộ nhãn TỪ CHỐI M2**, theo thứ tự: [`env`] cặp env = "trước"; [`cfg`] config = byte cũ, không tệp `.auth.json.*` trong HOME; [`khong_chot`]
0 lời gọi chốt cho đường config; [`khong_ghi`] 0 lời gọi writer cho đường config; [`khong_doc`] 0 lần mở đọc đường config; [`khong_lo`] cả TOK
lẫn SENT đều không có trong stdout, stderr; [`dong_loi`] các dòng stderr bắt đầu `[bootstrap] ✗ ` BẰNG ĐÚNG `[Dòng W6(<trường>)]`; [`agent`] đúng
một dòng `[bootstrap] agent_creds:`; [`ma`] rc 1, không `✓ config`. **Bộ nhãn TỪ CHỐI M3(c)**: [`env`] cặp env = (TOK, `TL_WEBAPP` trước); [`cfg`];
[`khong_ghi`]; [`khong_lo`]; [`dong_loi`] với trường `config`; [`agent`]; [`ma`] (lần chốt và lần đọc là của đường thành công, không đếm).

| # | ca (nền) · lượt | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|---|
| N1 | `w6_du_lieu` (mọi), fixture W6. Lượt theo thứ tự: `W6.hop_le`, `W6.web_kieu`, `W6.web_nul`, `W6.web_dc80`, `W6.token_kieu`, `W6.token_nul`, `W6.token_dc80`, `W6.token_d800`, `W6.jar_va_token`, `W6.require`, `W6.require_da_nap`, `W6.code`, `W6.encode`, `W6.encode_cu`, `W6.nan`, `W6.nan_cu`, `W6.dict_list`, `W6.dict_null`, `W6.dict_str`, `W6.token_falsy`, `W6.web_falsy` (21) | `hop_le` (TOK, WEB, `rootFolderId` `"r"`; config cũ `{"token": "CU-wp433b", "giu": "x"}`) ⇒ [`duong`] rc 0, stderr rỗng, env = (TOK, WEB), có `✓ config`, một `agent_creds:`; [`merge`] config parse ra đúng `{"token": TOK, "giu": "x", "webappUrl": WEB, "rootFolderId": "r"}`. `web_*` (token TOK; `webappUrl` = `7` / SENT+NUL / SENT+`\udc80`) và `token_*` (`webappUrl` WEB; `token` = `5` / SENT+NUL / SENT+`\udc80` / SENT+`\ud800`) ⇒ bộ nhãn M2 với trường tương ứng. `jar_va_token` (`nlm_auth` = `[1]`, `token` = `5`) ⇒ [`hai_dong`] rc 1, dòng `✗` bằng đúng [dòng jar nguyên văn `[bootstrap] ✗ dữ liệu không hợp lệ: nlm_auth phải là dict khác rỗng`, Dòng W6(token)], env = trước, một `agent_creds:`. `require` (`webappUrl` = `7`, `--require-agent-creds`, agent `KHÔNG CẤU HÌNH`) ⇒ [`require`] rc 4, dòng `✗` bằng đúng [Dòng W6(webappUrl), dòng §0.1 của P2a], một `agent_creds:`. `require_da_nap` (cùng bundle và cờ, `_bootstrap_agent_creds` giả trả `ĐÃ NẠP`) ⇒ [`require`] rc 1, dòng `✗` bằng đúng [Dòng W6(webappUrl)], một `agent_creds:`. `code` (`--env code --no-nlm --no-gws`, `webappUrl` = `7`, `gws_cred` hợp lệ, `cfgdir` tạm ngoài kho) ⇒ [`tiep_tuc`] rc 1, dòng `✗` bằng đúng [Dòng W6(webappUrl)], `credentials.json` đúng byte, có `✓ gws cred → `, một `agent_creds:`, env = trước. `encode` (`rootFolderId` = SENT+`\ud800`), `encode_cu` (bundle chỉ `token`; config cũ `{"x": SENT+"\ud800"}`), `nan` (bundle thêm `"extra": 1e999`), `nan_cu` (config cũ `{"x": NaN}`) ⇒ bộ nhãn M3(c); byte cũ là chính tệp config cũ của lượt. `dict_list`/`_null`/`_str` (config cũ `[]`/`null`/`"s"`, bundle chỉ `token`) ⇒ [`duong_dict`] rc 0, stderr rỗng, config parse ra `{"token": TOK}`, có `✓ config`. `token_falsy` (`token` = `0`) ⇒ [`thieu`] rc 0, stderr đúng `["[bootstrap] ⚠ bundle thiếu GAS token."]`, env = trước, config = CU. `web_falsy` (`webappUrl` = `0`) ⇒ [`web_falsy`] rc 0, stderr rỗng, env = (TOK, `TL_WEBAPP` trước), config parse ra `{"token": TOK, "webappUrl": 0}`. Vế âm base: §0.2; trên base lượt đầu đỏ là `W6.web_kieu` (`nem_env`, đo 10:44:24Z). | §4b dòng 1–18, 22–27, 29–34. |
| N1b | `w6_locale` (posix), fixture W6, MỘT lượt `W6.web_locale`, giả lập: `sys.getfilesystemencoding` trả `"ascii"` trong cửa sổ lượt | `webappUrl` = `"https://…/é"` ⇒ [`env`] env = trước; [`dong_loi`] rc 1, dòng `✗` bằng đúng [Dòng W6(webappUrl)], một `agent_creds:`. Giả lập chỉ đổi hàm M1 đọc; phép gán env thật vẫn mã hoá UTF-8 nên đột biến 28 lộ ra ở `env` (H). Vế âm base thật (không giả lập): §0.2 L1. Trên nền khác POSIX lượt này `chỉ_posix` (M1 không áp vế ấy khi `os.name != "posix"`). | §4b dòng 28. |
| N2 | `jar_rong_base` (mọi) — hồi quy cho nhánh MÃ KHÔNG ĐỔI của packet 1. Lượt `W1.rong`, `W1.vang`, `W3.rong`, `W3.list_rong`, `W3.list`, `W2.rong` | `W1.*` (`cmd_nlm_auth_pull`, bundle `{"nlm_auth": {}}` / không khoá) ⇒ [`base_w1`] rc 1, stderr đúng `["[nlm-auth-pull] ⚠ bundle chưa có nlm_auth — ở Code chạy `tl secrets-set --nlm` trước."]`, không `~/.notebooklm-mcp-cli`. `W3.*` (`_nlm_auth_load`, jar `{}` / `[]` / `[["auth.json", "x"]]`) ⇒ [`base_w3`] trả đúng `(False, "nlm_cred rỗng/sai định dạng.")`, không thư mục NLM. `W2.rong` (`cmd_bootstrap --env code --no-nlm --no-gws`, bundle có TOK, `gws_cred` hợp lệ, `nlm_auth` = `{}`; `cfgdir` tạm ngoài kho) ⇒ [`base_w2`] rc 0, stderr rỗng, không thư mục NLM. Base `11bd033`: cả 6 lượt đạt (đo 10:44:24Z). | §4b dòng 19–21. |
| N3 | Tự kiểm của fragment | (a) mỗi ID trong `_DU_KIEN` có đúng một mục `_DB` và ngược lại (so TẬP); mỗi mục giết đúng (ca, lượt, nhãn) đã khai; (b) SỔ LƯỢT: `_LUOT_DU_KIEN` = 3 ca, 28 lượt (21 + 1 + 6); DÃY (ca, lượt) đã ghi trạng thái phải BẰNG dãy nối các bộ của `_LUOT_DU_KIEN` theo thứ tự ca của bảng ca (thiếu, thừa, lặp hay đảo thứ tự ⇒ False); mỗi lượt đúng một trạng thái `đạt` · `đỏ` · `chỉ_posix`; trạng thái `bỏ_qua` không được phép trên mọi nền; (c) MỘT dòng tổng kết RA STDERR `[wp433_gws_cred_dich_ngoai_kho_b] CA: dự_kiến=a chạy=b đạt=c chỉ_posix=w · LUOT: dự_kiến=x chạy=y đạt=z chỉ_posix=t · DOT BIEN: dự_kiến=e chạy=f giết_đúng=g chỉ_posix=v · HONG: i · TU_KIEM: k/3`; `run` True chỉ khi `a == 3`, `b == c`, `a == b + w`, `x == 28`, `y == z`, `x == y + t`, `e == len(_DU_KIEN) == 34`, `f == g`, `e == f + v`, `i == 0`, `k == 3`; trên POSIX `w == t == v == 0`; trên nền khác `w == 1`, `t == 1`, `v == 3` (dòng 3, 4 theo cột nền; dòng 28 theo nền của ca đích); (d) tự kiểm phân hạng (đột biến, ca, lượt, nhãn, hạng mong đợi): `tu_kiem_doi_kieu` — chèn vào đầu thân M1 `try: raise AttributeError("wp433b-tu-kiem") except Exception as e: raise AssertionError(f"wp433b-tu-kiem {type(e).__name__}")`, nhắm (`w6_du_lieu`, `W6.hop_le`, `duong`) ⇒ `TIN_DUNG_GIA` VÀ ngoại lệ bắt được có `__cause__.__context__` kiểu `AttributeError`; `tu_kiem_chu_thich` — chỉ thêm chú thích ⇒ `SONG_SOT`; `tu_kiem_sai_luot` — CHÍNH đột biến dòng 6 (`db_w6_bo_kiem_token`), cùng ca, cùng nhãn `nem_env`, CHỈ khai lượt `W6.web_kieu` thay `W6.token_kieu` (lượt khai có cùng (loại, dấu) trong tập) ⇒ `TIN_DUNG_GIA`; (e) neo 0/2 lần hoặc không `compile` ⇒ `HONG`; (f) stdout của `run` rỗng. | Trên cây tạm: thêm một ID vào `_DU_KIEN` không có mục `_DB` ⇒ (a) False; đổi lượt đích của dòng 1 sang `W6.web_nul` ⇒ False; neo khớp 2 lần ⇒ `HONG: 1`, False; bộ phân hạng bỏ so lượt ⇒ `tu_kiem_sai_luot` ra `GIET` ⇒ False; in tổng kết ra stdout ⇒ (f) đỏ. Phản chứng BỘ ĐO (trên bản sao fragment, không phải mục `_DB`): `pc_bo_luot` — hàm ca bỏ chạy lượt `W6.encode_cu` (ca vẫn báo đạt) ⇒ False; `pc_dao_luot` — hàm ca đổi chỗ `W3.rong` và `W3.list_rong` (tập không đổi) ⇒ False; `pc_bo_ca` — gỡ ca `jar_rong_base` khỏi bảng ca, giữ `_LUOT_DU_KIEN` ⇒ False; `pc_bo_khai` — xoá tập khai của lượt `W6.web_kieu` ⇒ dòng 1, 2 thành `TIN_DUNG_GIA` ⇒ False; `pc_mu_quan_sat` — bộ quan sát đọc config không đếm (luôn 0) ⇒ dòng 23 `SONG_SOT` ⇒ False. Mỗi phép phải cho `run` False với dòng lỗi nêu đúng vế. |
| N4 | Không làm vỡ fragment kề bên và gate PD | Trên head: fragment packet 1 `wp433_nlm_gws_dich_ngoai_kho` và fragment P2a `wp433_gws_cred_dich_ngoai_kho` vẫn `run` True (đọc giá trị `run`, không đọc rc), `HONG: 0`; `python3 ops/cloud_agent_creds_test.py` `TONG: DAT`, `PD*` vẫn `GIET`, từng ca bằng base. | Đo được (§0.3): một `except UnicodeEncodeError:` thụt 16 dấu cách không chú thích ⇒ fragment P2a `HONG: 1`, `run` False. Trên cây tạm sửa một ký tự trong một chuỗi neo PD của `tl_gws.py` ⇒ `cloud_agent_creds_test` không `TONG: DAT` (review lượt 1 đo: neo khớp 0 lần ⇒ `HONG`). |
| N5 | Exact head: `--selftest` ĐẠT N/N hai số bằng nhau trên clone thật, N = N_base + 1, DELTA = 0 ca đỏ mới (base và head dựng trong CÙNG một lệnh); `test-fragments-check --json` ⇒ `ok: true`; `bundle_fragment_check.py --json` ⇒ `ok: true`, `failed: []`. Chạy trên clone sạch `__pycache__` (review lượt 1: cache có sẵn làm `test-fragments-check` báo `INVALID_FRAGMENT_PATH`). | Không tái sinh bundled ⇒ `TEST_ID_SET_MISMATCH`; sửa tay bundled ⇒ `GENERATED_BUNDLE_STALE` (review lượt 1 đo trên base: rc 2). Trên BẢN SAO clone: chuyển riêng fragment P2b ra khỏi `scripts/test_fragments` ⇒ selftest N = N_base ⇒ đỏ vế `N_base + 1`; đổi `run` của fragment dev thành `return False` ⇒ `N−1/N`. |
| N6 | Lane worker `ci.yml` tại chỗ: `release-manifest --root . --out <tạm>` rồi `release-verify <tạm> --root . --strict` ⇒ `ok: true`, `expected_file_count == checked_file_count`. Phiên land tái sinh manifest trong commit land, hồ sơ land ghi `release-verify RELEASE_MANIFEST.json --strict` `ok: true` trên commit ấy. | Trên bản sao: sửa một byte của một tệp trong gói sau khi sinh manifest tạm ⇒ `ok: false`; xoá một tệp ⇒ `ok: false` hoặc `checked < expected`. |
| N7 | Exact head, lệnh + rc + bằng chứng dương: `ruff check --select F` delta = 0 trên `scripts/tl_gws.py` (base 95 chẩn đoán), 0 trên fragment và bundled; `git diff --check <base>..<head>` rc 0; `doctrine-scan`, `adr-song` rc 0; dưới `set -o pipefail`: `git diff --numstat <base>..<head> > numstat.txt` (rc ≠ 0 ⇒ đỏ), (i) đúng 3 dòng, (ii) mỗi dòng khớp `^[0-9]+\t[0-9]+\t<đường>$`, tập đường == §1, (iii) tổng cột thêm ≤ 450. | Tên chưa định nghĩa ⇒ delta ≠ 0. Thêm khoảng trắng cuối dòng ⇒ `git diff --check` rc ≠ 0. Numstat dựng tay: đúng 3 dòng, đúng tập đường, tổng 450 ⇒ XANH; tổng 451 ⇒ (iii) ĐỎ; đổi một đường thành đường ngoài §1 ⇒ (ii) ĐỎ; cột `-` ⇒ (ii) ĐỎ; rỗng ⇒ (i); `<base>` không tồn tại ⇒ rc 128. `doctrine-scan`/`adr-song`: gate kế thừa, phản chứng thuộc `.claude/dev/packet_loop_test.py`. |

### 4b. Bảng đột biến — NGUỒN DUY NHẤT (thắng mọi mô tả đột biến rải trong §4)

Luật LƯỢT GỌI như §4b P2a. Đột biến neo trên NGUỒN CANDIDATE (đã áp M1–M3); mỗi đột biến chỉ chạy CA ĐÍCH của nó. Cột "nền": `posix` ⇒
đếm `chỉ_posix` trên nền khác — dòng 3, 4 vì cơ chế giết dựa vào ngữ nghĩa `os.environ` POSIX mà Windows chưa đo; dòng 28 vì ca đích
`w6_locale` là ca `posix`. Đích (ca, lượt, nhãn) của cả 34 dòng đã ĐO trên nguồn ứng viên prototype (`22baf3fd…`) bằng bộ chạy tạm
`do_dot_bien2.py`, cùng kết quả trên Python 3.11.18 / 3.12.3 / 3.13.18 (2026-11-19T10:44:24Z), 0 neo `HONG`, 34 bộ ba khác nhau — phiên
thi hành đo lại trên mã thật (N3(a)).

| # | đột biến | ca · lượt | nhãn | cơ chế | ngoại lệ khai ở biên lượt | nền |
|---|---|---|---|---|---|---|
| 1 | `db_w6_bo_kiem_web` (M1 không kiểm `webappUrl`) | `w6_du_lieu` · `W6.web_kieu` | `nem_env` | E — gán env `7` | `TypeError` chứa `str expected, not int` | mọi |
| 2 | `db_w6_bo_kiem_kieu` (M1 bỏ vế `isinstance`) | `w6_du_lieu` · `W6.web_kieu` | `nem_kiem` | E — `"\x00" in 7` | `TypeError` chứa `iterable` | mọi |
| 3 | `db_w6_bo_kiem_nul` (M1 bỏ vế NUL) | `w6_du_lieu` · `W6.web_nul` | `nem_env` | E — gán env có NUL | `ValueError` chứa `embedded null` | posix |
| 4 | `db_w6_bo_kiem_encode` (M1 bỏ `.encode("utf-8")`) | `w6_du_lieu` · `W6.web_dc80` | `env` | H — env POSIX nhận `\udc80`, M3(c) chặn config | — | posix |
| 5 | `db_w6_gan_token_truoc` (gán `TL_TOKEN` TRƯỚC lời gọi M1) | `w6_du_lieu` · `W6.web_kieu` | `env` | H | — | mọi |
| 6 | `db_w6_bo_kiem_token` (M1 không kiểm `token`) | `w6_du_lieu` · `W6.token_kieu` | `nem_env` | E — gán env `5` | `TypeError` chứa `str expected, not int` | mọi |
| 7 | `db_w6_bo_bat_encode` (`except` của M3(c) đổi sang lớp không liên quan) | `w6_du_lieu` · `W6.encode` | `nem_encode` | E | `UnicodeEncodeError` chứa `surrogates not allowed` | mọi |
| 8 | `db_w6_kiem_bundle_thay_existing` (thử tuần tự hoá `bundle` trong `try`, writer tự tuần tự hoá `existing` ngoài `try`) | `w6_du_lieu` · `W6.encode_cu` | `nem_encode` | E | như dòng 7 | mọi |
| 9 | `db_w6_encode_go_env` (nhánh `except` của M3(c) thêm `os.environ.pop("TL_TOKEN", None)`) | `w6_du_lieu` · `W6.encode` | `env` | H | — | mọi |
| 10 | `db_w6_encode_ghi_rong` (nhánh `except` của M3(c) đặt dữ liệu `b"{}"`, không đặt lý do) | `w6_du_lieu` · `W6.encode` | `cfg` | H | — | mọi |
| 11 | `db_w6_bo_kiem_dict` (bỏ M3(b)) | `w6_du_lieu` · `W6.dict_list` | `nem_dict` | E | `AttributeError` chứa `object has no attribute 'update'` | mọi |
| 12 | `db_w6_dict_thanh_loi` (M3(b) đặt lý do `dữ liệu không hợp lệ: config` thay vì `{}`) | `w6_du_lieu` · `W6.dict_list` | `duong_dict` | H | — | mọi |
| 13 | `db_w6_token_co_mat` (điều kiện gọi M1 thành `"token" in bundle`) | `w6_du_lieu` · `W6.token_falsy` | `thieu` | H | — | mọi |
| 14 | `db_w6_web_co_mat` (M1 kiểm `webappUrl` khi khoá CÓ MẶT thay vì truthy) | `w6_du_lieu` · `W6.web_falsy` | `web_falsy` | H | — | mọi |
| 15 | `db_w6_lo_gia_tri` (nhánh từ chối M2 in thêm MỘT dòng stdout `[bootstrap] w6=<repr token[:80]><repr webappUrl[:80]>`; stderr, rc giữ) | `w6_du_lieu` · `W6.web_kieu` | `khong_lo` | H — lộ TOK hợp lệ | — | mọi |
| 16 | `db_w6_tu_choi_hop_le` (M1 luôn trả `dữ liệu không hợp lệ: token`) | `w6_du_lieu` · `W6.hop_le` | `duong` | H | — | mọi |
| 17 | `db_w6_quen_degraded` (nhánh từ chối M2 không đặt `degraded`) | `w6_du_lieu` · `W6.web_kieu` | `ma` | H | — | mọi |
| 18 | `db_w6_ghi_khi_tu_choi` (nhánh từ chối M2 gọi writer với `b"{}"` cho config) | `w6_du_lieu` · `W6.web_kieu` | `cfg` | H | — | mọi |
| 19 | `db_w1_jar_rong_moi` (W1 `if not nlm:` ⇒ `if nlm is None:`) | `jar_rong_base` · `W1.rong` | `base_w1` | H | — | mọi |
| 20 | `db_w3_dinh_dang_moi` (W3 bỏ vế `not isinstance(nlm, dict)`) | `jar_rong_base` · `W3.list` | `base_w3` | H | — | mọi |
| 21 | `db_w2_jar_rong_moi` (W2 `if jar` ⇒ `if jar is not None`) | `jar_rong_base` · `W2.rong` | `base_w2` | H | — | mọi |
| 22 | `db_w6_tu_choi_van_chot` (nhánh từ chối M2 gọi `_kiem_dich_ghi` cho đường config) | `w6_du_lieu` · `W6.web_kieu` | `khong_chot` | H | — | mọi |
| 23 | `db_w6_tu_choi_van_doc` (nhánh từ chối M2 mở đọc đường config) | `w6_du_lieu` · `W6.web_kieu` | `khong_doc` | H | — | mọi |
| 24 | `db_w6_tu_choi_ghi_lai` (nhánh từ chối M2 gọi writer với ĐÚNG byte cũ của config — `cfg` vẫn đạt) | `w6_du_lieu` · `W6.web_kieu` | `khong_ghi` | H | — | mọi |
| 25 | `db_w6_encode_ghi_cu` (nhánh `except` của M3(c) gọi writer với đúng byte cũ, giữ lý do) | `w6_du_lieu` · `W6.encode` | `khong_ghi` | H | — | mọi |
| 26 | `db_w6_khong_merge` (đặt `existing = {}` ngay trước `update`) | `w6_du_lieu` · `W6.hop_le` | `merge` | H | — | mọi |
| 27 | `db_w6_cho_nan` (M3(c) bỏ `allow_nan=False`) | `w6_du_lieu` · `W6.nan` | `cfg` | H — ghi `Infinity` | — | mọi |
| 28 | `db_w6_bo_kiem_locale` (M1 bỏ vế mã hoá theo `sys.getfilesystemencoding()`) | `w6_locale` · `W6.web_locale` | `env` | H | — | posix (ca) |
| 29 | `db_w6_dung_som` (nhánh từ chối M2 `return 1` ngay sau dòng lỗi) | `w6_du_lieu` · `W6.web_kieu` | `agent` | H | — | mọi |
| 30 | `db_w6_bo_nhanh_sau` (nhánh từ chối M2 đặt `env = "chat"`) | `w6_du_lieu` · `W6.code` | `tiep_tuc` | H | — | mọi |
| 31 | `db_w6_require_thua_rc1` (chèn `if degraded: return 1` ngay trước nhánh `--require-agent-creds`) | `w6_du_lieu` · `W6.require` | `require` | H | — | mọi |
| 32 | `db_w6_require_luon_4` (nhánh `--require-agent-creds` bỏ vế `ac != "ĐÃ NẠP"`) | `w6_du_lieu` · `W6.require_da_nap` | `require` | H | — | mọi |
| 33 | `db_w6_dung_ly_jar` (gọi M1 chỉ khi `not ly_jar`) | `w6_du_lieu` · `W6.jar_va_token` | `nem_env` | E — gán env `5` | `TypeError` chứa `str expected, not int` | mọi |
| 34 | `db_w6_lap_dong` (in Dòng W6 hai lần) | `w6_du_lieu` · `W6.web_kieu` | `dong_loi` | H | — | mọi |

Tập khai theo lượt (gộp cột 6): `W6.web_kieu` {(`TypeError`, `str expected, not int`) ⇒ `nem_env`; (`TypeError`, `iterable`) ⇒ `nem_kiem`};
`W6.web_nul` {(`ValueError`, `embedded null`) ⇒ `nem_env`}; `W6.token_kieu` và `W6.jar_va_token` {(`TypeError`, `str expected, not int`) ⇒
`nem_env`}; `W6.encode`, `W6.encode_cu` {(`UnicodeEncodeError`, `surrogates not allowed`) ⇒ `nem_encode`}; `W6.dict_list` {(`AttributeError`,
`object has no attribute 'update'`) ⇒ `nem_dict`}; mọi lượt khác: tập rỗng. Hai phần tử của `W6.web_kieu` cùng loại, khác dấu, khác nhãn.
Cùng lượt khác nhãn: `W6.web_kieu` (1, 2, 5, 15, 17, 18, 22, 23, 24, 29, 34 — nhãn `nem_env`, `nem_kiem`, `env`, `khong_lo`, `ma`, `cfg`,
`khong_chot`, `khong_doc`, `khong_ghi`, `agent`, `dong_loi`), `W6.encode` (7, 9, 10, 25), `W6.dict_list` (11, 12), `W6.hop_le` (16, 26).
Lượt không là đích đột biến nào — `W6.token_nul`, `W6.token_dc80`, `W6.token_d800`, `W6.nan_cu`, `W6.dict_null`, `W6.dict_str`, `W1.vang`,
`W3.rong`, `W3.list_rong` — đo HÀNH VI (giá trị khác cùng nhánh); review lượt 1 đã đo: đổi riêng kết quả của từng lượt ấy làm đỏ đúng lượt.
Tổng: **34** đột biến; E **8** (1, 2, 3, 6, 7, 8, 11, 33), H **26**; nền `posix` **3** (3, 4, 28), `mọi` **31**. Tự kiểm phân hạng 3 (N3(d)).
Phản chứng BỘ ĐO 5 (N3, trên bản sao fragment, không vào tổng 34).

## 5. `pham_vi_e`

Không chạm E4, không chạm E5: chỉ sửa mã đường ghi, dữ liệu giả, HOME tạm, đồ giả thay tải Drive (rig xoá cả hằng baked), không LIVE,
không đẩy Package. Ngoại lệ bundled ở §1 chờ chủ kho (§9 Q1).

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Trần kích thước `ADR-0053` (dòng khai đầu tệp, ≤ 6 tệp / ≤ 450 dòng thêm): executor đo `git diff --numstat <base>..H` (N7, không lọc
  đường) TRƯỚC khi công bố; vượt 450 ⇒ DỪNG, không push, báo điều phối. Không cắt ca/phép đo để lọt trần. Nâng trần hay tách là quyết
  định của chủ kho — **E2**.
- `_kiem_dich_ghi`, `_ghi_nguyen_tu_0600` hoặc đoạn W6 trên base thật khác §0.1 (thứ tự gán env → chốt → đọc → merge → ghi), hoặc cần sửa
  thân một hàm liệt kê ở §2 ⇒ dừng, đi revision.
- Chưa có comment cấp ngoại lệ bundled cho packet này trên Issue #433 (§1) ⇒ không cấp lease.
- Cần sửa ngoài write set, hoặc preflight (quét §0.1 của đặc tả packet 1 trên base thật) thấy chỗ ghi credential từ bundle khác W1–W6 ⇒
  dừng, đi revision.
- Neo PD, chuỗi khoá `wp727`, neo đột biến của fragment packet 1 hoặc P2a không giữ được nguyên văn ĐÚNG MỘT lần ⇒ dừng, đi revision.
- Đặc tả không thuộc Mission nên chờ chủ kho duyệt băm theo `ADR-0067` — **E2**.

## 7. `hinh_dang_ke_thua`

Bộ đếm hình dạng lỗi DÙNG CHUNG với packet 1 và P2a, không reset khi tách: lúc P2a đóng băng là mức đặc tả 3, mức mã 0 (§7 P2a); review
mã P2a trên PR #1415 (`6e49b68`) không có finding (connector: "Didn't find any major issues", comment `7003304434`) ⇒ mức mã giữ 0. Hình
dạng của P2b là MỚI so với ba lớp "chốt nhìn thiếu một phần của đường": "kiểm theo một ngữ nghĩa GẦN đúng của sink thay vì đúng ngữ nghĩa
sink". Ba lần trong cùng packet: env POSIX nhận `\udc80` (B3) nên chốt dựa vào phép gán env lọt; bản 1 kiểm UTF-8 trong khi env mã hoá theo
`sys.getfilesystemencoding()` (L1, review lượt 1); bản 1 bắt lỗi encode trong khi `json.dumps` mặc định cho NaN (L2, L3, review lượt 1). Đủ
ba lần ⇒ theo luật đếm, câu hỏi "có nên làm tiếp" đã được hỏi: M1 nay kiểm ĐÚNG phép mã hoá của sink (UTF-8 cho config, mã hoá fs cho env),
M3(c) bắt cả lớp `ValueError` của tuần tự hoá. Hình dạng thứ hai, đã ĐO: neo đột biến theo chuỗi con của fragment khác bị mã mới khớp lần
hai (§0.3) — N4 khoá bằng cách chạy lại hai fragment kề bên.

## 8. `chua_do_duoc`

- Mọi phép đo trên prototype (§0.3, cột đo §4b) là trên mã DỰNG NGOÀI KHO, không phải head; phiên thi hành đo lại trên head (N3, N4).
  `ops/cloud_agent_creds_test.py` trên prototype hiện hành: `TONG: DAT`, `DOT BIEN: 91/91`, tự kiểm `DAT (4 dot bien)`, rc 0 (10:47Z–10:53:07Z).
- Windows: mã M1 rẽ nhánh `os.name == "posix"` cho vế mã hoá fs; hai ca `mọi` chưa chạy trên Windows; dòng 3, 4 đếm `chỉ_posix` vì thông
  điệp NUL và việc env nhận surrogate trên Windows chưa đo. Không có CI Windows bắt buộc.
- Locale ASCII đo bằng tiến trình con thật (L1) cho base và prototype; trong fragment là GIẢ LẬP `sys.getfilesystemencoding` (N1b) — không
  đo được phép gán env thật dưới locale ASCII trong cùng tiến trình.
- Thông điệp `TypeError` của `"\x00" in 7` (dấu `iterable`) đo trên 3.11–3.13; bản Python sau có thể đổi câu (chưa đo).
- Kích thước P2b (ước lượng tĩnh, chưa đo; neo vào fragment P2a đã land: 389 dòng cho 11 ca / 46 lượt / 37 đột biến; numstat P2a `389/0`,
  `48/19`, `1/0` = **438** dòng thêm, review lượt 1 đo): `tl_gws.py` **+27–37** (prototype đo +29/−2); fragment theo hạng mục: khung, nạp,
  đồ giả, `TinHieuChotCa`, phân hạng, tổng kết, tự kiểm ~110–130; rig với ba bộ quan sát và hai giả lập ~50–60; ba hàm ca viết dạng bảng
  lượt (28 lượt) ~55–75; `_LUOT_DU_KIEN`, tập khai, `_DU_KIEN` ~22–28; hằng neo + `_DB` 34 mục ~45–55 ⇒ hạng mục **282–348**, cộng dự
  phòng RIÊNG ≤ 15; bundled **+1** ⇒ hạng mục cộng **310–386**, kèm dự phòng **310–401 dòng thêm, 3 tệp, giữa ~355**, dưới trần 450 với
  biên ≥ 49. Năm phản chứng bộ đo chạy trên bản sao, ngoài numstat. Trần CƯỠNG CHẾ trên numstat thật (N7 (iii), §6).
- `review_class`, lease ba đường, nền selftest: đo khi cấp lease trên base thật.

## 9. Câu hỏi cho chủ kho và lịch sử review

Câu hỏi (E2 theo `ADR-0067`; không chặn review):
- **Q1 — Ngoại lệ bundled (E2, chặn cấp lease):** cần comment mới trên #433 nêu `packet_id` `GWS-CRED-DICH-NGOAI-KHO-B`, tệp
  `scripts/tl_test_fragments_bundled.py` và sha256 đặc tả đóng băng — cùng phương án B như packet 1/P2a. ➡️ Khuyến nghị: cấp, vì phương án
  khác (mang `RELEASE_MANIFEST.json`) đổi quy trình land cho đúng một packet.
- **Q2 — Chốt tổ tiên cho W6** (`~/.tra_luat_config.json`, hiện `_kiem_dich_ghi(cfgp, cfgp, ())`): ngoài phạm vi P2b do chủ kho giao. ➡️
  Khuyến nghị: để packet riêng nếu muốn; chú ý hệ quả §8 của P2a (HOME có tổ tiên là symlink, ví dụ `/home` liên kết, sẽ bị từ chối).
- **Q3 — Bundle không phải `dict`** (B20, ném ở 1772 trước W6): ➡️ Khuyến nghị: để nợ, không mở rộng P2b (thuộc mã jar của packet 1).

**Review Codex lượt 1** (2026-11-19T10:26:52Z–10:40:22Z, bản `cd88fbe9…`, `rv/luot1.verdict.txt`): request_changes, 4 P2, 3 P3; xác nhận
§0.1, B0–B20, bẫy neo, 21 bộ ba của §4b trên ba bản Python, tự kiểm và phản chứng bộ đo trên bộ chạy tạm. Xử lý trong bản này:
- P2 locale env — ĐÃ SỬA: M1 thêm vế mã hoá theo `sys.getfilesystemencoding()` trên POSIX; §0.2 L1 (tiến trình con thật, base ném, prototype
  từ chối); ca `w6_locale` (posix, giả lập) + đột biến 28.
- P2 NaN/Infinity — ĐÃ SỬA: M3(c) `allow_nan=False`, bắt `ValueError`; §0.2 L2, L3; lượt `nan`, `nan_cu`; đột biến 27.
- P2 mốc env và hợp đồng ghép — ĐÃ SỬA: "trước" = tại đầu W6 (sau `load_creds`); M2 nói rõ không dừng nhánh sau, rc 1/4, dòng jar và dòng cờ
  đếm riêng; lượt `jar_va_token`, `require`, `require_da_nap`, `code`; đột biến 29–33.
- P2 không chạm config / không lộ TOK — ĐÃ SỬA: bộ quan sát chốt/đọc/ghi (M4), nhãn `khong_chot`, `khong_ghi`, `khong_doc`; `khong_lo` cấm cả
  TOK; `hop_le` mang khoá cũ `giu` với nhãn `merge`; đột biến 22–26, 34; tách `hop_dong` cũ thành `dong_loi`, `agent`, `ma`.
- P3 biên nhận `w6-ungvien.txt` lệch — ĐÃ SỬA: tái sinh từ prototype hiện hành (10:46:30Z), sha256 nguồn dựng ở §0.3.
- P3 sổ lượt so tập — ĐÃ SỬA: N3(b) so DÃY; phản chứng `pc_dao_luot`.
- P3 §8 cộng thiếu dự phòng — ĐÃ SỬA: tách hạng mục và dự phòng.

## 10. Nhật ký revision

- 2026-11-19T10:2xZ (phiên con của điều phối, soạn r1 bản 1): đo §0 trên `11bd033`; prototype ngoài kho để đo §0.3 và §4b. Bản 1 sha256
  `cd88fbe9…` (`rv/dac-ta-ban1.md`).
- 2026-11-19T10:5xZ (bản 2, sau review lượt 1): §9; prototype +29/−2 (`22baf3fd…`); 3 ca / 28 lượt / 34 đột biến; §8 310–401.
