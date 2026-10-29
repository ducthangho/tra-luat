# Đặc tả packet — `CLOUD-SETUP-P1-BUNDLE` (revision 4)

- `packet_id`: **CLOUD-SETUP-P1-BUNDLE** · `packet_issue`: **#1009** (Issue cha #1008) · `revision`: **4** · trạng thái: **ĐÓNG BĂNG**
  khi PR của revision này mở (băm `sha256` ghi trên Issue #1009 và PR, không ghi trong tệp). **Thay thế revision 3**
  (`ops/specs/cloud-setup-p1-bundle-r3.md`, blob `cbe6cb84`, sha256 `b16da4b1…`, land ở `8dd3396a`). Lý do: PR #1023 (head
  `ea0903a7` = `fa04437` lượt 4 approve + merge `origin/master`) ĐỎ CI do chính packet, ở BỐN tệp ngoài write set r3 — đo của
  phiên điều phối và executor 29-10 ~11:20–12:05Z, base `1cc847de` xanh ở cả bốn chỗ:
  · `gate` (Ubuntu job 123414010801 + Windows run 40866904091 job 123423901868): `python scripts/tl_core/command_registry_test.py`
    2 ca đỏ (`total_nodes 200 != 198`, `198 != 196`) — tệp ghim cứng 196 lệnh lá;
  · bước sau đó (chưa chạy trên CI vì job dừng, đo TẠI CHỖ trên `ea0903a7`): `golden-test` rc 2 đúng 2/20 case
    (`references/golden/workflow_audit.json` `checked_commands 196→198`; `references/golden/tool_inventory_inventory_decision.json`
    thêm `agent-creds-set`…) và `determinism-audit --strict` rc 2 CHỈ do hai golden ấy;
  · `gate-registry` (Ubuntu job 123414873474): `.claude/hooks/pretooluse_guard_test.py` 39/41 —
    `python .claude/hooks/pretooluse_guard.py --kiem-bang` head rc 4 `CHAN: _TL_LENH_GHI THIEU 1 lenh read_only=False:
    agent-creds-set`, base rc 0.
  · `gate-registry` (Windows run 40866904091 job 123425366775): CÙNG chỗ — `pretooluse_guard_test.py` 39/41 (t15, t33).
  Lúc đóng băng (~13:05Z) còn `gate-packet-loop (windows-latest)` (job 123423901974) CHƯA xong; bản Ubuntu của job ấy đã xanh trên
  `ea0903a7`. Nếu nó đỏ do packet ở tệp ngoài write set ⇒ S1, revision mới.
  Lỗi Windows CÓ SẴN, KHÔNG do packet: `gate-ops (windows-latest)` `ops/bien_nhan_v2_test.py` c96 (90/93) — đã đỏ y hệt ở run
  40833865576 của nhánh khác; packet #1017 (PR #1018) đang vá. Không vào write set; packet hấp thụ bằng merge `origin/master`
  sau khi bản vá ấy land.
  Sửa đổi so với r3: write set 13 tệp, trần đổi, mục tiêu 12–15, tiêu chí H3–H5 và L1, K2 đo so merge-base. Mọi mục tiêu/tiêu chí
  khác GIỮ NGUYÊN · soạn 29-10-2026, phiên `session_015GtxraXfMD1t2FJLzzGDr4`.
- `nang_tran`: chủ kho, nguyên văn **"Vá hết các lỗi cho tôi, cả trên Windows và Ubuntu, lặp vá cho đến hết P1, P2, P3 và
  không còn lỗi trên Windows."** — https://github.com/ducthangho/tra-luat/issues/1009#issuecomment-6495628501 — cộng trần dòng
  **800** của issuecomment-6493446162. Trần của packet này: **≤ 13 tệp / ≤ 800 dòng thêm** (thay r3 và `ADR-0053`, CHỈ cho packet này).
- `nguon_cap_viec`: chỉ thị trực tiếp của chủ kho trong phiên nói trên (không có dòng kế hoạch nào trong
  `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`). Packet đầu của chuỗi ba packet `cloud-setup` (Q1): P1 bundle · P2 script ·
  P3 ghi ngược + NLM. P2 và P3 soạn đặc tả riêng SAU khi P1 land.
- `review_class`: **sensitive** — chạm ranh giới credential (protocol §8, dòng `sensitive`).
- Base: `1cc847defbe646c68f4126144dbc80e02eafd61b` (tree `5cccb599cff4500ccad69858740b9c6e5dd7a2d2`, merge PR #1004) là điểm rẽ
  của nhánh `claude/wp1009-cloud-setup-p1-g1`, đã merge `origin/master` một lần (`ea0903a7`). Executor đi tiếp từ head nhánh ấy,
  được merge `origin/master` thêm (merge commit, không rebase/force-push). Mọi phép đo KÍCH THƯỚC và DELTA của packet đo so
  **merge-base với `origin/master`** (`git diff origin/master...HEAD`), không so `1cc847de` — merge master làm diff so `1cc847de`
  mang cả thay đổi của người khác. Đo lại khi cấp lease.

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: nang_tran issuecomment-6495628501 + issuecomment-6493446162 (≤ 13 tệp / ≤ 800 dòng thêm; thay ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab)

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
6. `scripts/tl.py` (r2 — chỉ sửa tập `_CREDS_LAZY_CMDS`)
7. `scripts/tl_core/command_registry.py` (r3 — chỉ thêm metadata cho hai lệnh mới)
8. `references/golden/parser_surface.json` (r3 — chỉ tái sinh snapshot)
9. `scripts/tl_core/command_registry_test.py` (r4 — chỉ sửa số đếm ratchet)
10. `references/golden/workflow_audit.json` (r4 — chỉ tái sinh)
11. `references/golden/tool_inventory_inventory_decision.json` (r4 — chỉ tái sinh)
12. `.claude/hooks/pretooluse_guard.py` (r4 — chỉ thêm `agent-creds-set` vào `_TL_LENH_GHI`)
13. `.claude/hooks/pretooluse_guard_test.py` (r4 — CHỈ khi ca của nó ghim số đếm/tên lệnh; không cần thì không sửa)

Mười ba tệp = trần đã nâng (`nang_tran`). Đo 12:05Z 29-10: hai golden r4 CÓ trong `RELEASE_MANIFEST.json`;
`scripts/tl_core/command_registry_test.py` và hai tệp `.claude/hooks/` KHÔNG có (bị release filter loại). (r3:) Cả hai tệp r3 nằm trong `RELEASE_MANIFEST.json` (đo 08:40Z 29-10: manifest 192 tệp, có
`references/golden/parser_surface.json` và `scripts/tl_core/command_registry.py`). Ba tệp đầu và `scripts/tl.py` nằm trong `RELEASE_MANIFEST.json` (đo 04:19Z, đo lại 07:10Z 29-10: manifest có 192
tệp, gồm cả `scripts/tl_core/cli.py`, `scripts/tl_gws.py`, `scripts/tl_selftest.py`), nên manifest phải tái sinh
(tiền lệ commit `685bc187`). `changelog.d/` bị release filter loại (protocol, mục fragment). `references/RUNBOOK.md`
chuyển sang P2 theo Q19 (A) để giữ dư địa dòng cho khoá Gemini.

`ai-dang-giu` lúc 08:34Z 29-10, sau khi fetch đủ `refs/heads/*` (`ls-remote` 689 = cục bộ 689, `comm -23` = 0, `comm -13` = 0):
hai đường dẫn r3 (`scripts/tl_core/command_registry.py`, `references/golden/parser_surface.json`) ⇒ `NGƯỜI_GIỮ 0`. Sáu đường
dẫn r2 đang do lease `wp1009-cloud-setup-p1-r2-g1-claude` (chính packet này) giữ — lease cho r3 phải KHAI `thay_the_cho` g1 và
đặt bia mộ `da_bi_thay_the` lên tệp g1 (g1 còn hạn tới 2026-10-30T08:10:00Z). `origin/master` đã tiến 10 commit so base
(tới `e9967f07`, đo 08:34Z): `git diff --stat 1cc847de origin/master` trên cả 8 đường dẫn ⇒ rỗng. Đo lại cả tám khi cấp lease.

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
| Hằng trong `scripts/tl.py` | Hằng đặt ở `tl_gws.py` (Q15); `tl.py` chỉ sửa `_CREDS_LAZY_CMDS`. |
| Metadata/snapshot cho lệnh KHÁC ngoài `agent-creds-set`, `secrets-keygen`, cờ `--require-agent-creds` | r3 chỉ mở hai tệp cho đúng ba thay đổi parser này. |

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
8. `RELEASE_MANIFEST.json` — tái sinh sau khi sáu tệp thuộc manifest đổi nội dung.
9. `scripts/tl.py` — thêm `secrets-keygen` và `agent-creds-set` vào `_CREDS_LAZY_CMDS`, để hai lệnh chạy được trên máy chưa
   có config webapp (`secrets-keygen` không cần credential nào; `agent-creds-set` chỉ cần `TL_MASTER_KEY` và đường upload
   gws của chính nó). Không thêm, không bớt lệnh nào khác trong tập; `secrets-stage`, `secrets-set` vẫn đi qua `load_creds`.

10. `scripts/tl_core/command_registry.py` — thêm metadata `COMMAND_META` cho `agent-creds-set` và `secrets-keygen`, theo khuôn
   dòng `secrets-stage`/`secrets-set` đang có: `agent-creds-set` ghi Drive ⇒ `write_scope` chứa `drive` và PHẢI có gate
   (`builtin_gate="secrets_master_key_gate"`, như hai lệnh ghi bundle hiện có — nếu không thì `validate_registry` trả
   `WRITE_CMD_NO_GATE`); `secrets-keygen` không ghi gì ngoài stdout ⇒ `read_only=True`, `write_scope` `none`. Không sửa
   metadata lệnh nào khác.
11. `references/golden/parser_surface.json` — tái sinh bằng `TL_WRITE_PARSER_SURFACE=1 python scripts/tl.py --selftest`
   (cơ chế có sẵn, `scripts/tl_selftest.py:6642`), rồi kiểm `git diff -- references/golden/parser_surface.json` CHỈ mang
   `agent-creds-set`, `secrets-keygen` và cờ `--require-agent-creds` của `bootstrap`; diff có thứ gì khác ⇒ DỪNG.

Luật kích thước (thay luật dự phòng của r2 — chuyển `secrets-keygen` sang P2 không bớt được tệp nào, vì `agent-creds-set` và
`--require-agent-creds` vẫn đổi parser): vượt 13 tệp hoặc 800 dòng thêm (đo so merge-base) ⇒ DỪNG, hỏi chủ kho; không tự tách packet.

12. `scripts/tl_core/command_registry_test.py` — cập nhật số đếm ratchet (lệnh lá 196→198, node 198→200, kể cả dòng mô tả)
   đúng bằng số `compute_parser_coverage` đo được trên head; không đổi logic ca nào.
13. `references/golden/workflow_audit.json`, `references/golden/tool_inventory_inventory_decision.json` — tái sinh bằng
   `python scripts/tl.py golden-test --write`, rồi `git diff -- references/golden/` CHỈ được mang hai lệnh mới và số đếm
   tương ứng (CLAUDE.md mục deploy 5); diff có golden khác hoặc khoá khác ⇒ DỪNG.
14. `.claude/hooks/pretooluse_guard.py` — thêm `agent-creds-set` vào `_TL_LENH_GHI` (lệnh ghi Drive — subagent PHẢI bị chặn chạy
   nó); KHÔNG thêm `secrets-keygen` (read_only). Không sửa logic guard; nếu chú thích ghi số lệnh thì cập nhật số. Tệp test chỉ
   sửa khi một ca ghim số/tên phải đổi theo.
15. CI hai nền: mọi context BẮT BUỘC liệt kê ở tiêu chí L1 xanh trên Ubuntu (lượt PR) VÀ Windows (`workflow_dispatch`
   `runner_set=windows-only` trên nhánh packet — được phép theo chỉ thị chủ kho), trừ lỗi CÓ SẴN đã chứng minh đỏ y hệt trên
   một ref không chứa packet; lỗi có sẵn ấy hấp thụ bằng merge `origin/master` khi bản vá của nó đã land, không sửa trong packet.

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
| E2 | 9 | `r973_lenh_moi_khong_can_creds_webapp` (mức CLI, tiến trình con thật `python scripts/tl.py …`, HOME tạm KHÔNG có `.tra_luat_config.json`, môi trường KHÔNG có `TL_WEBAPP`/`TL_TOKEN`): `secrets-keygen` ⇒ rc 0 và đúng một dòng khoá; `agent-creds-set --codex` không đặt `TL_MASTER_KEY` ⇒ thông báo lỗi CỦA CHÍNH lệnh về `TL_MASTER_KEY` (rc 2), KHÔNG phải thông báo thiếu credential webapp của `load_creds`. Vế âm giữ hành vi cũ: `secrets-set` cùng điều kiện vẫn chết ở `load_creds` (thông báo thiếu `TL_WEBAPP`). Trên base cả hai lệnh mới chưa tồn tại (đo 07:22Z 29-10: `_CREDS_LAZY_CMDS` không chứa chúng) | bỏ `secrets-keygen` khỏi tập ⇒ ĐỎ; bỏ `agent-creds-set` khỏi tập ⇒ ĐỎ; thêm `secrets-set` vào tập ⇒ ĐỎ (vế âm) |
| G1 | 6 | `python scripts/tl.py --selftest` (trên Ubuntu VÀ Windows — L1) với `core.abbrev=7` (CLAUDE.md, mục deploy 6): **delta so base = 0 ca đỏ mới**, và mọi ca `r973_*` ĐẠT. Nền: **1738/1738** (đơn vị: ca selftest) trên `1cc847de` — đo của executor 29-10 ~08:25Z, và NỀN_ĐO_ĐIỀU_PHỐI ở mục `chua_do_duoc`. Số `1736/1738` của r2 đo KHÔNG ghim `core.abbrev`, hai ca đỏ khi ấy (`r218`, `r264`) là đỏ giả theo nền đo | một ca `r973_*` đỏ, hoặc bất kỳ ca nào đạt trên base mà đỏ trên head ⇒ ĐỎ |
| J1 | 8 | `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true` và `expected == checked` (lane LAND, CLAUDE.md mục deploy 5) | sửa một byte của `scripts/tl_gws.py` sau khi tái sinh ⇒ ĐỎ |
| K1 | — | `python -m ruff check --select F scripts/tl_gws.py scripts/tl_core/cli.py scripts/tl_core/command_registry.py scripts/tl.py`: delta F so base = 0 | thêm một tên chưa định nghĩa ⇒ ĐỎ |
| H1 | 10 | `python scripts/tl.py workflow-audit --strict --json` ⇒ rc 0, `ok == true`, `registry.issues == []` (vế dương trên head; vế âm L6a: cây base + chỉ hai lệnh trong parser ⇒ rc 2 với hai `UNREGISTERED_PARSER_CMD`, đo 08:25Z 29-10) | xoá dòng metadata `agent-creds-set` ⇒ ĐỎ (`UNREGISTERED_PARSER_CMD`); bỏ `builtin_gate` của `agent-creds-set` ⇒ ĐỎ (`WRITE_CMD_NO_GATE`) |
| H2 | 11 | `r77a_parser_surface_matches_snapshot` ĐẠT trên head KHÔNG đặt `TL_WRITE_PARSER_SURFACE`; `git diff 1cc847de -- references/golden/parser_surface.json` chỉ có các khoá/cờ của ba thay đổi parser | khôi phục snapshot về bản base ⇒ ĐỎ |
| H3 | 12 | `python scripts/tl_core/command_registry_test.py` rc 0 trên head (vế âm: head `ea0903a7` đỏ 2/10, đo 11:21Z 29-10) | trả số về 196 ⇒ ĐỎ |
| H4 | 13 | `python scripts/tl.py golden-test --json` rc 0 `ok: true` và `determinism-audit --strict --json` rc 0 (vế âm: `ea0903a7` rc 2 cả hai) | khôi phục một golden về bản base ⇒ ĐỎ |
| H5 | 14 | `python .claude/hooks/pretooluse_guard.py --kiem-bang` rc 0 và `python .claude/hooks/pretooluse_guard_test.py` đạt hết (vế âm: `ea0903a7` rc 4, 39/41) | gỡ `agent-creds-set` khỏi `_TL_LENH_GHI` ⇒ ĐỎ |
| L1 | 15 | Danh sách context BẮT BUỘC theo từng nền (đối chiếu ma trận + `if:` của `.github/workflows/ci.yml` tại `origin/master` ~13:05Z 29-10; đọc lại lúc nghiệm thu, lệch thì theo `ci.yml`). **Ubuntu — lượt PR trên head H:** `success` cho `chuan-bi`, `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-nhanh-manh (ubuntu-latest, 0…7)` (8 job), `gate-nhanh-gop (ubuntu-latest)`, `gate-registry (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)`, `gate-cong-cu-gop (ubuntu-latest)`, `gate-cong-cu (ubuntu-latest, 0…7)` (8 job), và `thu-hoi`. Riêng `gate-cong-cu` được `skipped` CHỈ khi output `che_do` của `chuan-bi` trên chính lượt ấy là `duong_nhanh` (ghi giá trị đọc được vào handoff). **Windows — `workflow_dispatch` `runner_set=windows-only` trên CÙNG H** (dispatch luôn `day_du`): `success` cho `chuan-bi`, `gate (windows-latest)`, `gate-ops (windows-latest)`, `gate-nhanh-manh (windows-latest, 0…7)`, `gate-nhanh-gop (windows-latest)`, `gate-registry (windows-latest)`, `gate-packet-loop (windows-latest)`, `gate-cong-cu (windows-latest, 0)`. KHÔNG ÁP DỤNG trên Windows (ghi riêng, không tính đạt/rớt): `gate-cong-cu-gop` (`if:` đòi ma trận có `ubuntu-latest` + `exclude: windows-latest`) và `gate-cong-cu (windows-latest, 1…7)` (`exclude`) — bằng chứng thay thế là job gom/mảnh tương ứng `success` trên lượt PR Ubuntu của cùng H. Mọi context bắt buộc khác `success` (`skipped`, `cancelled`, vắng) ⇒ ĐỎ — KHÔNG có ngoại lệ chung cho `skipped`. Ngoại lệ duy nhất: job đỏ do lỗi CÓ SẴN đã chứng minh (run id đỏ y hệt trên ref không chứa packet), ghi vào handoff | một context bắt buộc đỏ do packet, hoặc `skipped`/vắng ngoài hai trường hợp nêu trên ⇒ ĐỎ |
| K2 | — | kích thước: `git diff --numstat origin/master...HEAD` ⇒ ≤ 13 tệp và ≤ 800 dòng thêm (đơn vị: dòng thêm, tổng trên mọi tệp của diff) | vượt ⇒ ĐỎ; DỪNG hỏi chủ kho |

Tiêu chí E1 là khớp chuỗi: vế dương trên head, vế âm trên base đã ghi (L6a); E1 đo trên đầu ra `--help`, không phải
Markdown, nên L6b không áp dụng; A3 đo từng sentinel riêng, không tiêu chí nào đếm gộp nhiều vị trí (L6c); không có lời
khai bằng chữ số dạng "N lời gọi" cần bắt hai dạng (L6d); không có lời khai "không cổng nào cưỡng chế" (L6e).

## Kích thước dự kiến

**Đo** trên head nhánh `ea0903a7` (`git diff --numstat origin/master...ea0903a7`, 29-10 ~12:30Z): **650 dòng thêm trên 8 tệp**.
Phần r4 **ước tính**: `command_registry_test.py` ~5, hai golden ~20–40 (snapshot JSON), `pretooluse_guard.py` ~1–2, test guard 0–3,
manifest vài dòng băm ⇒ khoảng 680–700 dòng trên 12–13 tệp; dư ~100 dòng cho vá theo review và lỗi riêng Windows (nếu có, gần như
chắc nằm trong `tl_gws.py`/`tl_selftest.py` đã có trong write set). Trần: 13 tệp / 800 dòng thêm. Lời gọi Codex: đã dùng 4/8 (L1–L4 trên
r3); hết 8 chưa sạch ⇒ Review Rescue Checkpoint (`ADR-0037`).

Luật review cho phần còn lại (chủ kho, issuecomment-6494782891 + issuecomment-6495628501): mỗi lượt kiểm (i) finding lượt trước
đã đóng thật chưa, (ii) lỗi hành vi mức P0–P2, (iii) P3. Đột biến sống ngoài bảng tiêu chí được ghi P3 — và theo chỉ thị "hết
P1, P2, P3" P3 cũng phải vá trước khi xin land. Reviewer KHÔNG săn đột biến mới ngoài các nhánh mã r4 thêm.

(Trần lời gọi: dòng `tran_loi_goi_codex` ở đầu đặc tả.)

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
- Số dòng thêm thật của bốn tệp còn lại (mục Kích thước dự kiến): đo lúc thi hành.
- NỀN_ĐO_ĐIỀU_PHỐI: selftest trên `1cc847de` với `core.abbrev=7` do phiên điều phối chạy lại song song lúc soạn r3; kết quả ghi trên
  Issue #1009 khi có. Lệch `1738/1738` của executor ⇒ lấy nền NHỎ hơn làm sàn và ghi lại trong handoff.
