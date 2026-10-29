# Đặc tả packet — `CLOUD-SETUP-P1-BUNDLE` (revision 1)

- `packet_id`: **CLOUD-SETUP-P1-BUNDLE** · `packet_issue`: **#1009** (Issue cha #1008) · `revision`: **1** · trạng thái: **ĐÓNG BĂNG**
  lúc 07:10Z 29-10-2026 sau khi chủ kho duyệt (băm `sha256` ghi trên Issue #1009 và PR #1004, không ghi trong tệp) · soạn 29-10-2026 bằng skill `soan-spec`,
  phiên `session_015GtxraXfMD1t2FJLzzGDr4`. Chủ kho chốt Q1–Q18 "theo khuyến nghị" trong cùng phiên, rồi chọn
  phương án (A) ở Q19: thêm khoá Gemini cho CLI `agy` (Antigravity) vào cùng tệp, chuyển phần `RUNBOOK.md` sang P2.
- `nguon_cap_viec`: chỉ thị trực tiếp của chủ kho trong phiên nói trên (không có dòng kế hoạch nào trong
  `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`). Packet đầu của chuỗi ba packet `cloud-setup` (Q1): P1 bundle · P2 script ·
  P3 ghi ngược + NLM. P2 và P3 soạn đặc tả riêng SAU khi P1 land.
- `review_class`: **sensitive** — chạm ranh giới credential (protocol §8, dòng `sensitive`).
- Base dự kiến: nhánh mặc định lúc cấp lease. Đo 07:10Z 29-10: `0a8f4d78d30854247a7147e45f5586bf856925da`
  (tree `4f8af6635d9ce0a60de26b22da45b280119ee09c`). Đo lại khi cấp lease.

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

(OID trên là commit LAND của cả `ADR-0052` lẫn `ADR-0053` trên nhánh mặc định, đo bằng
`git log origin/master --first-parent --diff-filter=A` lúc 04:19Z và đo lại 07:10Z 29-10: không đổi.)

## Vấn đề (một đoạn)

Chủ kho muốn mọi nền cloud (Claude Code web, Codex cloud) dựng đủ credential từ **đúng một** secret ở giao diện:
`TL_MASTER_KEY`. Bundle hiện có `tl_secrets.enc` mang 4 khoá (`webappUrl`, `token`, `gws_cred`, `nlm_auth` — đo
`scripts/tl_gws.py:986` lúc 04:19Z 29-10) nhưng không mang credential của agent (`auth.json` của Codex gói ChatGPT,
token dài hạn của Claude, khoá `GEMINI_API_KEY` cho CLI `agy` của Antigravity). Không thể nhét chúng vào `tl_secrets.enc`: chốt WP714 (`_nlm_bundle_guard`,
`scripts/tl_gws.py:896`) bắt mọi lần `secrets-set` trên bundle có `nlm_auth` phải kèm jar NLM vừa qua canary tại chỗ,
nên một phiên cloud không bao giờ ghi được vào đó — và P3 cần phiên cloud ghi ngược `auth.json` sau khi Codex xoay
refresh token. P1 dựng một tệp mã hoá RIÊNG cho credential agent, cùng khoá gốc, cùng kiểu link công khai.

## `write_set`

1. `scripts/tl_gws.py`
2. `scripts/tl_core/cli.py`
3. `scripts/tl_selftest.py`
4. `changelog.d/wp-1009.md`
5. `RELEASE_MANIFEST.json`

Năm tệp, dưới trần `ADR-0053` (≤ 6 tệp). Ba tệp đầu nằm trong `RELEASE_MANIFEST.json` (đo 04:19Z, đo lại 07:10Z 29-10: manifest có 192
tệp, gồm cả `scripts/tl_core/cli.py`, `scripts/tl_gws.py`, `scripts/tl_selftest.py`), nên manifest phải tái sinh
(tiền lệ commit `685bc187`). `changelog.d/` bị release filter loại (protocol, mục fragment). `references/RUNBOOK.md`
chuyển sang P2 theo Q19 (A) để giữ dư địa dòng cho khoá Gemini.

`ai-dang-giu` lúc 07:10Z 29-10, sau khi fetch đủ `refs/heads/*`: cả năm đường dẫn ⇒ `NGƯỜI_GIỮ 0`, rc 0 (lần đo
04:19Z chỉ thấy lease **HẾT_HẠN** `wp710-*`, `r378-*` trên `scripts/tl_gws.py`, `scripts/tl_selftest.py`). Đo lại cả
năm khi cấp lease.

## `ngoai_pham_vi`

| thứ | vì sao |
|---|---|
| Script setup chung `scripts/cloud-setup.sh`, hook `.claude/hooks/session-start.sh`, `ops/codex_cloud_setup.sh` | P2 (Q1). |
| Ghi ngược `auth.json` có khoá + CAS, action mới trong `Code.gs`, tải lại jar NLM khi gặp 401 | P3 (Q1, Q6). |
| Chống ghi đồng thời cho `agent-creds-set` | P1 chỉ ghi `rev` đúng; người ghi duy nhất là chủ kho chạy tay (Q18). |
| Đổi `TL_MASTER_KEY`, mã hoá lại `tl_secrets.enc`, tạo tệp `tl_agent_creds.enc` thật, bật anyone-with-link | Thao tác LIVE trên Drive — bước vận hành của chủ kho SAU land (Q3). Mã không có hàm đổi quyền chia sẻ Drive (đo 04:19Z 29-10: không có `permission`/`anyone` trong `scripts/tl_gws.py`), và packet KHÔNG thêm. |
| Ghi fileId thật vào hằng `AGENT_CREDS_FILEID` | Tệp chưa tồn tại lúc land; ghi ở P2 (Q15). |
| Export `CLAUDE_CODE_OAUTH_TOKEN`, `GEMINI_API_KEY` vào môi trường của từng nền; ghi `modelProvider: gemini` vào `~/.gemini/antigravity-cli/settings.json` | Mỗi nền một cơ chế — P2 (Q5, Q19). P1 không ghi gì vào `~/.gemini`. |
| `references/RUNBOOK.md` (hướng dẫn sinh khoá, tạo tệp, đổi khoá) | Chuyển sang P2 (Q19 A). Tới lúc P2 land, hướng dẫn vận hành nằm ở mục "Bước vận hành SAU land" của đặc tả này. |
| Cloud agent của Antigravity; đăng nhập OAuth và ADC của `agy` | Không có tài liệu chính thức về setup script/secret cho cloud agent (Q4); OAuth của `agy` có báo cáo không lưu được token khi thiếu keyring trên Linux. P1 chỉ lo khoá API tĩnh. |
| Sửa `tl_secrets.enc`, nới chốt WP714 | Q8: tách tệp chính là để không đụng chốt ấy. |
| `SKILL.md` | Không liệt kê cờ của `secrets-set` (đo 04:19Z 29-10), nên lệnh mới không buộc đổi vocab ở đó. |
| Hằng trong `scripts/tl.py` | Đặt hằng ở `tl.py` thành tệp thứ 7, vượt trần; hằng ở `tl_gws.py` (Q15). |

## `muc_tieu`

Mỗi dòng chiếu vào đúng một đường dẫn ở `write_set` (L2).

1. `scripts/tl_gws.py` — lệnh `agent-creds-set`: dựng payload JSON `{schema: 1, rev, updated_at, codex_auth?,
   claude_oauth_token?, antigravity_api_key?}`, mã hoá bằng `gws_cred_store.encrypt(…, TL_MASTER_KEY)`, upload qua `_stage_enc_upload`
   (`--new` tạo tệp mới và in fileId; `--file-id`/env/hằng ghi đè tại chỗ). `--codex` đọc `<CODEX_HOME>/auth.json`
   (thiếu/rỗng ⇒ `~/.codex/auth.json`) và từ chối nếu `tokens` không phải object; `--claude-token-env VAR` (mặc định
   `CLAUDE_CODE_OAUTH_TOKEN`) và `--antigravity-key-env VAR` (mặc định `GEMINI_API_KEY`) đọc giá trị từ biến, không
   bao giờ từ argv; biến được nêu mà rỗng ⇒ từ chối (rc khác 0, 0 upload), không ghi chuỗi rỗng. Ghi tại chỗ: tải bản cũ, giải mã, giữ các khoá
   không bị thay, `rev` = cũ + 1; KHÔNG giải mã được bản cũ ⇒ từ chối (rc khác 0, 0 upload), không reset `rev` ngầm.
   Không in giá trị credential ở bất kỳ nhánh nào, chỉ tên khoá đã thay.
2. `scripts/tl_gws.py` — kiểm độ mạnh `TL_MASTER_KEY` ở đường GHI (`secrets-stage`, `secrets-set`,
   `agent-creds-set`): dưới 32 ký tự HOẶC dưới 12 ký tự khác nhau ⇒ rc 2, 0 lời gọi upload. Đường ĐỌC (`bootstrap`)
   không kiểm (Q11).
3. `scripts/tl_gws.py` — lệnh `secrets-keygen`: in một khoá `secrets.token_urlsafe(32)` (43 ký tự), không ghi đĩa.
4. `scripts/tl_gws.py` — `bootstrap` nạp credential agent: fileId theo thứ tự `TL_AGENT_CREDS_FILEID` > hằng
   `AGENT_CREDS_FILEID` (rỗng lúc land). Ghi `auth.json` vào `<CODEX_HOME>` hoặc `~/.codex`: nguyên tử (tệp tạm cùng thư
   mục + `os.replace`), quyền 0600; bản trên đĩa có `last_refresh` MỚI HƠN hoặc BẰNG ⇒ giữ nguyên (Q12). Claude token và
   khoá Gemini: không export, không ghi tệp, chỉ báo TÊN khoá có mặt. In ĐÚNG MỘT dòng trạng thái: `agent_creds: ĐÃ NẠP` · `agent_creds: KHÔNG CẤU HÌNH` ·
   `agent_creds: KHÔNG ĐO ĐƯỢC`. Không làm hỏng đường chính của `bootstrap` trừ khi có `--require-agent-creds` (Q17).
5. `scripts/tl_core/cli.py` — parser cho `agent-creds-set` (`--codex`, `--claude-token-env`, `--antigravity-key-env`,
   `--new`, `--file-id`, `--folder`), `secrets-keygen`, và cờ `--require-agent-creds` của `bootstrap`.
6. `scripts/tl_selftest.py` — các ca ở mục `nghiem_thu`, hermetic: không mạng, không Drive, `_stage_enc_upload` và
   tải công khai bị thay bằng đồ giả GIỮ TRẠNG THÁI có đếm lời gọi.
7. `changelog.d/wp-1009.md` — fragment changelog của packet.
8. `RELEASE_MANIFEST.json` — tái sinh sau khi ba tệp thuộc manifest đổi nội dung.

Luật dự phòng kích thước (thay luật Q14 cũ, vì `RUNBOOK.md` đã ra khỏi P1): nếu tổng dòng thêm vượt 450 thì chuyển
mục tiêu 3 (`secrets-keygen`) cùng ca C1 sang P2, không xin nâng trần.

## `nghiem_thu`

Tên ca dùng tiền tố `r973_` … (đo 04:19Z, đo lại 07:10Z 29-10: số `r` lớn nhất trong `scripts/tl_selftest.py` là `r972`; nếu đã có
`r973` lúc thi hành thì lấy số kế tiếp còn trống và ghi lại trong handoff). Mỗi ca kèm đột biến làm nó đổi màu (L3);
đột biến chạy trên BẢN SAO TẠM, không trên tệp thật.

| # | mục tiêu | tiêu chí | phép đo làm ĐỎ (đột biến) |
|---|---|---|---|
| A1 | 1 | `r973_agent_creds_set_ma_hoa_va_rev`: tạo mới ⇒ đồ giả upload nhận đúng 1 blob; giải mã bằng khoá đúng ra JSON có `schema == 1`, `rev == 1`, có `codex_auth`; ghi tại chỗ lần hai ⇒ `rev == 2` và khoá không bị thay vẫn còn | bỏ dòng tăng `rev` ⇒ ĐỎ; ghi `codex_auth` dạng plaintext (bỏ `encrypt`) ⇒ ĐỎ |
| A2 | 1 | `r973_agent_creds_tu_choi_ban_cu_khong_giai_ma_duoc`: bản cũ mã hoá bằng khoá KHÁC ⇒ rc khác 0, đồ giả upload đếm **0** lời gọi | đổi nhánh lỗi giải mã thành "coi như tệp rỗng" ⇒ ĐỎ (upload 1 lần, `rev == 1`) |
| A3 | 1 | `r973_agent_creds_khong_in_gia_tri`: sentinel RIÊNG đặt trong `auth.json`, trong biến token Claude và trong biến khoá Gemini; stdout + stderr của MỌI nhánh (thành công, lỗi giải mã, lỗi upload) không chứa sentinel nào trong ba (đo từng sentinel riêng — L6c) | thêm `print` giá trị khoá Gemini ở một nhánh lỗi ⇒ ĐỎ |
| A6 | 1 | `r973_agent_creds_khoa_gemini_tu_bien`: `--antigravity-key-env MY_KEY` với `MY_KEY` có giá trị ⇒ payload giải mã có `antigravity_api_key` đúng giá trị ấy; không nêu cờ ⇒ payload không có khoá ấy; biến rỗng ⇒ rc khác 0 và upload **0** lời gọi | đọc cứng `GEMINI_API_KEY` bỏ qua tên biến được nêu ⇒ ĐỎ; ghi chuỗi rỗng thay vì từ chối ⇒ ĐỎ |
| A4 | 1 | `r973_agent_creds_tokens_phai_la_object`: `auth.json` có `"tokens": "chuoi"` ⇒ rc khác 0, 0 upload | đổi kiểm `isinstance(…, dict)` thành `"tokens" in d` ⇒ ĐỎ |
| A5 | 1 | `r973_agent_creds_ton_trong_CODEX_HOME`: `CODEX_HOME` trỏ thư mục tạm có `auth.json` riêng ⇒ payload mang đúng tệp ấy, không phải `~/.codex` | cứng hoá `~/.codex` ⇒ ĐỎ |
| B1 | 2 | `r973_khoa_yeu_bi_tu_choi_o_duong_ghi`: khoá 31 ký tự ⇒ cả ba lệnh ghi trả rc 2, upload **0** lời gọi mỗi lệnh (đếm riêng TỪNG lệnh, không đếm gộp — L6c); khoá 32 ký tự nhưng 11 ký tự khác nhau ⇒ rc 2; khoá `secrets.token_urlsafe(32)` ⇒ qua | đổi ngưỡng 32 thành 31 ⇒ ĐỎ; bỏ kiểm ở riêng `secrets-set` ⇒ ĐỎ (vì đếm từng lệnh) |
| B2 | 2 | `r973_bootstrap_khong_kiem_khoa`: bundle mã hoá bằng khoá 8 ký tự vẫn giải mã được qua `bootstrap` | thêm kiểm độ mạnh vào `bootstrap` ⇒ ĐỎ |
| C1 | 3 | `r973_secrets_keygen`: stdout đúng một dòng dài 43, khớp `^[A-Za-z0-9_-]{43}$`, hai lần gọi khác nhau; thư mục làm việc và HOME tạm không có tệp mới | in hằng cố định ⇒ ĐỎ (hai lần gọi trùng); ghi khoá ra tệp ⇒ ĐỎ |
| D1 | 4 | `r973_bootstrap_ba_trang_thai`: fileId rỗng ⇒ đúng một dòng `agent_creds: KHÔNG CẤU HÌNH`, rc đường chính không đổi; tải lỗi ⇒ `KHÔNG ĐO ĐƯỢC`; thành công ⇒ `ĐÃ NẠP` | gộp `KHÔNG ĐO ĐƯỢC` vào `KHÔNG CẤU HÌNH` ⇒ ĐỎ |
| D2 | 4,5 | `r973_bootstrap_require_agent_creds`: có cờ ⇒ hai trạng thái xấu cho rc khác 0; không cờ ⇒ rc như cũ | bỏ nhánh rc của cờ ⇒ ĐỎ |
| D3 | 4 | `r973_bootstrap_giu_auth_json_moi_hon`: đĩa có `last_refresh` mới hơn ⇒ tệp trên đĩa giữ nguyên byte; bằng nhau ⇒ không ghi (mtime không đổi); cũ hơn ⇒ ghi, quyền 0600 (bỏ kiểm quyền trên Windows, ghi lý do trong ca) | đổi `>=` thành `>` ⇒ ĐỎ ở vế bằng nhau; bỏ so `last_refresh` ⇒ ĐỎ |
| D4 | 4 | `r973_bootstrap_env_thang_hang`: `TL_AGENT_CREDS_FILEID` đặt ⇒ đồ giả tải nhận đúng fileId của biến dù hằng khác rỗng | đảo thứ tự ưu tiên ⇒ ĐỎ |
| D5 | 4 | `r973_bootstrap_khong_export_khong_ghi_gemini`: payload có `claude_oauth_token` và `antigravity_api_key` ⇒ sau `bootstrap`, `os.environ` của tiến trình KHÔNG có `CLAUDE_CODE_OAUTH_TOKEN`, `GEMINI_API_KEY` (nếu trước đó vắng), HOME tạm KHÔNG có thư mục `.gemini`; stdout chứa TÊN hai khoá, không chứa giá trị | thêm `os.environ["GEMINI_API_KEY"] = …` ⇒ ĐỎ; ghi `settings.json` vào `~/.gemini` ⇒ ĐỎ |
| E1 | 5 | các lệnh mới có trong parser: `tl agent-creds-set --help` chứa cả `--antigravity-key-env`, `tl secrets-keygen --help`, `tl bootstrap --help` chứa `--require-agent-creds` (rc 0, khớp chuỗi cờ nguyên văn — vế dương; vế âm L6a: trên base cả ba chưa có, đo 04:19Z 29-10) | xoá dòng `add_parser("agent-creds-set"…)` ⇒ ĐỎ |
| G1 | 6 | `python scripts/tl.py --selftest`: **delta so base = 0 ca đỏ mới**, và mọi ca `r973_*` ĐẠT. Nền đo 04:19Z và đo lại 07:10Z 29-10 trong container cloud (cây = nhánh mặc định + đúng tệp đặc tả này): **1736/1738** (đơn vị: ca selftest), hai ca đỏ sẵn `r218_docclaims_l2_sha_khong_ton_tai`, `r264_doc_claims_phu_docs` | một ca `r973_*` đỏ, hoặc bất kỳ ca nào đạt trên base mà đỏ trên head ⇒ ĐỎ |
| J1 | 8 | `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true` và `expected == checked` (lane LAND, CLAUDE.md mục deploy 5) | sửa một byte của `scripts/tl_gws.py` sau khi tái sinh ⇒ ĐỎ |
| K1 | — | `python -m ruff check --select F scripts/tl_gws.py scripts/tl_core/cli.py`: delta F so base = 0 | thêm một tên chưa định nghĩa ⇒ ĐỎ |
| K2 | — | kích thước: `git diff --numstat <base>..<head>` ⇒ ≤ 6 tệp và ≤ 450 dòng thêm (đơn vị: dòng thêm, tổng trên mọi tệp của diff) | vượt ⇒ ĐỎ; luật dự phòng: chuyển mục tiêu 3 sang P2 |

Tiêu chí E1 là khớp chuỗi: vế dương trên head, vế âm trên base đã ghi (L6a); E1 đo trên đầu ra `--help`, không phải
Markdown, nên L6b không áp dụng; A3 đo từng sentinel riêng, không tiêu chí nào đếm gộp nhiều vị trí (L6c); không có lời
khai bằng chữ số dạng "N lời gọi" cần bắt hai dạng (L6d); không có lời khai "không cổng nào cưỡng chế" (L6e).

## Kích thước dự kiến

**Ước tính, CHƯA đo** (chưa có mã): khoảng 425 dòng thêm trên 5 tệp — `tl_gws.py` ~165, `tl_core/cli.py` ~17,
`tl_selftest.py` ~230, `changelog.d` ~15, manifest vài dòng băm. Trần `ADR-0053`: 6 tệp / 450 dòng thêm. Lời gọi Codex review: theo trần `ADR-0052` của dòng `tran_loi_goi_codex` ở đầu đặc tả.

## Bước vận hành SAU land (chủ kho, không thuộc packet)

1. `tl secrets-keygen` ⇒ khoá mới; đặt `TL_MASTER_KEY` mới vào giao diện các nền.
2. Mã hoá lại `tl_secrets.enc` bằng khoá mới (`tl secrets-stage`, trên laptop có jar NLM).
3. `tl agent-creds-set --new --codex --claude-token-env CLAUDE_CODE_OAUTH_TOKEN --antigravity-key-env GEMINI_API_KEY`
   ⇒ ghi lại fileId; bật anyone-with-link trên Drive; đặt `TL_AGENT_CREDS_FILEID` tạm thời. (Token Claude lấy bằng
   `claude setup-token`; khoá Gemini tạo ở Google AI Studio.)
4. Kiểm trên một phiên mới: `tl bootstrap --require-agent-creds` ⇒ `agent_creds: ĐÃ NẠP`.

## `hinh_dang_ke_thua`

`khong_ap_dung` — packet mới, không khắc phục packet nào; không có biên nhận tiền nhiệm.

## `chua_do_duoc`

- Hành vi thật của `_stage_enc_upload` và tải công khai với Drive: ca selftest dùng đồ giả; LIVE chỉ đo ở bước vận hành 3–4.
- `last_refresh` trong `auth.json` thật của Codex có luôn mặt và cùng định dạng ISO không: đo trên tệp container ngày 29-10
  thì có (`2026-10-27T11:35:54.511153200Z`, chín chữ số phần giây). Mã phải so được chuỗi có độ chính xác khác nhau;
  tệp không có `last_refresh` thì coi là CŨ HƠN mọi bản có (ghi vào handoff nếu chọn khác).
- Quyền 0600 trên Windows: không đo được bằng `stat`; ca D3 bỏ vế quyền trên Windows và ghi lý do.
- CLI `agy` chưa được đo ở bất kỳ máy nào trong phiên soạn (container không cài, laptop chưa kiểm). Việc `agy` nhận
  `GEMINI_API_KEY` khi `modelProvider: gemini` lấy từ tài liệu cài đặt chính thức của Antigravity, chưa chạy thật.
  P1 chỉ lưu và giải mã khoá, nên điều này không chặn P1; P2 phải đo trước khi dựa vào.
- Số dòng thêm thật (mục Kích thước dự kiến): đo lúc thi hành.
