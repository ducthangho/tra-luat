# Đặc tả packet — `CLOUD-SETUP-P3-WRITEBACK` (revision 2 — errata)

- `packet_id`: **CLOUD-SETUP-P3-WRITEBACK** · `packet_issue`: **#1089** (Issue cha #1008) · `revision`: **2 (errata)** · trạng thái:
  r1 **ĐÓNG BĂNG** 01-11-2026 ~00:25Z (`ops/specs/cloud-setup-p3-writeback-r1.md`, blob `b5bb73e8`, sha256 `e4b0800a…`,
  issuecomment-6551147799). r2 là **errata** của r1, soạn 01-11-2026 bởi phiên điều phối `session_015GtxraXfMD1t2FJLzzGDr4`;
  chỉ sửa MỘT chỗ — phép đo A12 — do finding P2 của Codex connector trên PR #1095 chỉ ra (mục `errata_r2` cuối tệp). Mọi chỗ
  khác giữ nguyên từng byte so với r1. Băm `sha256` của r2 ghi trên Issue #1089 và PR #1095, không ghi trong tệp. r1 soạn
  31-10 → 01-11-2026, phiên `session_015GtxrcPNaayykBErdfcNUB`.
- `nguon_cap_viec`: chỉ thị của chủ kho mở P3 (31-10-2026 ~16:55Z, qua phiên điều phối `session_015GtxraXfMD1t2FJLzzGDr4`),
  dòng P3 trong bảng chuỗi của Issue #1008. Phạm vi chốt trong phiên soạn này: vòng 1 Q1–Q10 và vòng 2 Q11–Q20, chủ kho
  trả lời cả hai vòng "đồng ý tất cả" (khuyến nghị). Không có dòng kế hoạch nào trong `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`.
- `review_class`: **sensitive** — đường GHI credential (`tl_agent_creds.enc`), điểm cuối webapp GAS mới, và cấu hình hook
  `.claude/settings.json` (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease (đo 00:22Z 01-11: `4952cff3`, merge PR #1090). Mọi phép đo kích thước/delta
  đo so merge-base (`git diff origin/master...HEAD`).
- **Điều kiện cấp lease (vòng 2 Q12):** `RELEASE_MANIFEST.json` đang bị lease `wp1052-r5-g5-claude` giữ, `lease_expires_at_utc`
  **2026-11-01T15:00:00Z** (đo 00:1xZ 01-11 bằng `ops/lease_publish.py ai-dang-giu`). Chỉ cấp lease cho packet này sau mốc ấy,
  hoặc sớm hơn nếu `wp1052` land hay lease ấy bị thu hồi. Đo lại `ai-dang-giu` trên cả năm đường dẫn của `write_set` ngay
  trước khi cấp (L5); bốn đường dẫn còn lại đo 00:1xZ 01-11 ⇒ `NGƯỜI_GIỮ 0`.
- `nang_tran`: chủ kho đồng ý vòng 2 Q13. Trần packet này: **≤ 5 tệp / ≤ 600 dòng thêm** (thay `ADR-0053` CHỈ cho packet
  này), với cách đếm ở mục *Kích thước*. Vượt ⇒ bỏ bớt ca phụ, KHÔNG xin nâng thêm.

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: nang_tran vòng 2 Q13 (≤ 5 tệp / ≤ 600 dòng thêm; tệp .gs đếm theo diff so 2p, ≤ 120; thay ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab)

(OID là commit LAND của `ADR-0052` và `ADR-0053` — merge PR #791; cùng giá trị đặc tả P1 r4, P2a, P2b. Đo lại 00:2xZ 01-11:
`git show --stat 8ab1007` có cả hai tệp ADR.)

## Vấn đề (một đoạn)

Refresh token Codex (gói ChatGPT) xoay vòng: mỗi lần `codex` làm mới, bản cũ bị vô hiệu. P1/P2 đã cho phiên cloud ĐỌC
`tl_agent_creds.enc` (`bootstrap` → `~/.codex/auth.json`, `scripts/tl_gws.py:1217`), nhưng chưa có đường đưa bản mới NGƯỢC
về, nên bản trong `.enc` mau chết (đo 00:19Z 01-11 trong phiên soạn: `doctor` báo ảnh chụp cũ 108,7h, `SAP_HET_HAN`). Đường
ghi `.enc` duy nhất hiện có là `agent-creds-set` → `_stage_enc_upload` → gws `update_content` (`tl_gws.py:1771`): đọc `rev`,
cộng 1, ghi đè — **không CAS**, hai phiên ghi cùng lúc thì bản sau thắng im lặng. Webapp LIVE `2.21.2p`
(`references/Code.2.21.2p.gs`, 4083 dòng) **không có** action nào ghi đè nội dung một tệp có sẵn (`upload`/`createtext` tạo tệp
mới). Webapp lại KHÔNG có `TL_MASTER_KEY`, nên không đọc được `rev`; thứ duy nhất server so được là `md5Checksum` của blob.
Packet này thêm action `agent_creds_put` (CAS theo md5, trong `LockService`, chỉ cho đúng một fileId) vào bản webapp mới
`2.21.2q`, thêm lệnh con `ghi-nguoc` vào helper P2b `ops/cloud_agent_creds.py`, và gọi nó từ hook `Stop` của Claude Code.

## `write_set`

Đúng 5 đường dẫn (vòng 2 Q12). Không ký tự đại diện.

1. `references/Code.2.21.2q.gs` — **mới**: chép nguyên `references/Code.2.21.2p.gs`, thêm action `agent_creds_put`, đổi `APP_VERSION`
2. `ops/cloud_agent_creds.py` — lệnh con `ghi-nguoc`; `nap` ghi tệp dấu
3. `ops/cloud_agent_creds_test.py` — ca + đột biến (đã đăng ký ở `.claude/dev/ci_dang_ky_test.py:59`; mẫu tổng kết KHÔNG đổi)
4. `.claude/settings.json` — thêm sự kiện `Stop`
5. `RELEASE_MANIFEST.json` — tái sinh vì (1) nằm trong gói phát hành (manifest đo 00:1xZ 01-11: 195 tệp, có `Code.2.21.2o.gs` và
   `Code.2.21.2p.gs`; thêm ⇒ 196, dưới trần 200)

Không tệp nào khác. Cần sửa một tệp ngoài danh sách ⇒ DỪNG, hỏi chủ kho (L2). Cụ thể **KHÔNG** sửa `references/Code.2.21.2p.gs`,
`scripts/tl_gws.py`, `scripts/gws_cred_store.py`, `scripts/gas.py`, `scripts/_fallback/gas.py`, `scripts/tl.py` (giữ
`EXPECT_VERSION = "2.21.2p"`), `scripts/tl_selftest.py`, `scripts/tl_core/**`, `references/API_CONTRACT.md`, `references/RUNBOOK.md`,
`SKILL.md`, `.claude/hooks/**`, `.claude/dev/ci_dang_ky_test.py`, golden, CHANGELOG, VERSION.

## `ngoai_pham_vi`

- **Lệnh `tl agent-creds-writeback`** (vòng 2 Q11 đảo vòng 1 Q7 phần lệnh): một lệnh `tl` mới kéo theo ~13 tệp (tiền lệ P2a
  PR #1063: `tl_gws.py`, `tl_core/cli.py`, `tl.py`, `command_registry*`, 3 golden, `tl_selftest.py`, changelog, manifest…).
  Laptop không cần ghi ngược (laptop dùng `agent-creds-set` bằng tay), còn `ops/` không vào gói phát hành.
- **Ca "khoá cũ → khoá mới"** (vòng 2 Q11 đảo vòng 1 Q9): cần sửa `tl_gws.py` ⇒ sang packet `CLOUD-SETUP-P3C-CONTRACT`.
- **Bump `EXPECT_VERSION`, `API_CONTRACT.md`, SKILL/RUNBOOK** (vòng 1 Q10, vòng 2 Q19): packet `CLOUD-SETUP-P3C-CONTRACT`, mở
  ngay sau M1. Giữa lúc deploy `2.21.2q` và lúc bump, `tl ping` in cảnh báo lệch (`scripts/tl_core/ops_misc.py:312`) — chủ kho
  chấp nhận (Q19). Không guard nào chặn cứng vì lệch này (các guard thật dạng `>=`, vd `ingest_commit` `>=2.21.2o`).
- **Deploy webapp**: bước LIVE `clasp` của chủ kho, giữ deployment ID (vòng 1 Q10). Executor không deploy.
- **NLM tải lại cookie khi gặp 401** (vòng 1 Q1): packet riêng `CLOUD-SETUP-P3B-NLM-401`, Issue và đặc tả riêng.
- **`launcher.py doctor` gọi `agy` thật** (vòng 1 Q9): lane launcher, packet riêng.
- **Lùi sang đường gws khi webapp lỗi/cũ** (vòng 1 Q6, Q10): cấm. Không có đường ghi thứ ba (CLAUDE.md "Nguồn sự thật").
- **Đổi `agent-creds-set`** (vòng 1 Q2): đường tay trên laptop giữ nguyên gws.
- **Codex Cloud, laptop/Windows** (vòng 2 Q20): không hook `Stop`; secret Codex Cloud bị gỡ trước giai đoạn agent; `ghi-nguoc`
  chỉ chạy khi `CLAUDE_CODE_REMOTE=true`.
- **Hai phiên cùng một chuỗi refresh token xoay đồng thời** (vòng 2 Q20): CAS chặn ghi đè mất dữ liệu, KHÔNG cứu token đã bị
  vô hiệu ở phía OpenAI — xem `chua_do_duoc`.

## Hợp đồng `agent_creds_put` (Code.2.21.2q.gs)

POST (qua `doPost`, cùng đường token với mọi action khác). Tham số: `fileId`, `expect_md5`, `b64`.
Thứ tự kiểm, mỗi lỗi trả `{ok:false, error:<MÃ>}` và **không ghi gì**:

1. Script Property `TL_AGENT_CREDS_FILEID` vắng/rỗng ⇒ `AGENT_CREDS_NOT_CONFIGURED`. Không có hằng dự phòng trong mã.
2. `fileId` khác giá trị ấy ⇒ `AGENT_CREDS_FILEID_MISMATCH` (vòng 1 Q4).
3. `expect_md5` không khớp `^[0-9a-f]{32}$` ⇒ `EXPECT_MD5_REQUIRED`. Không có chế độ ghi mù.
4. `b64` giải ra 0 byte hoặc > 65536 byte ⇒ `BLOB_SIZE`.
5. `LockService.getScriptLock().tryLock(10000)` thất bại ⇒ `LOCK_BUSY` (vòng 2 Q15; lock chung với `withRegLock_`,
   `Code.2.21.2p.gs:2363`).
6. **Trong lock**: đọc `md5Checksum` hiện tại của `fileId`. Khác `expect_md5` ⇒ `{ok:false, error:'CAS_CONFLICT', md5:<hiện tại>}`.
7. Khớp ⇒ ghi đè **nội dung** (MIME `application/octet-stream`), không đổi tên/thư mục/chia sẻ; đọc lại `md5Checksum` SAU khi
   ghi ⇒ `{ok:true, md5:<đọc lại>, size:<byte>}`. Nhả lock trong `finally`.

`APP_VERSION = '2.21.2q'`. Mọi phần khác của tệp giữ nguyên byte so `2p` (đo bằng diff ở K2).

## `muc_tieu`

Mỗi dòng chiếu vào đúng một đường dẫn ở `write_set` (L2).

1. → `references/Code.2.21.2q.gs`: action `agent_creds_put` đúng mục *Hợp đồng* ở trên (vòng 1 Q2–Q4, vòng 2 Q15–Q16);
   nhánh `case 'agent_creds_put'` trong bảng điều phối; `APP_VERSION = '2.21.2q'`.
2. → `ops/cloud_agent_creds.py`: lệnh con **`ghi-nguoc [--neu-doi]`** (vòng 1 Q6–Q8, vòng 2 Q11, Q16–Q17).
   - Chỉ chạy khi `CLAUDE_CODE_REMOTE == "true"`; khác ⇒ `BỎ QUA — không phải phiên cloud`, 0 lời gọi mạng.
   - Dùng NGUYÊN các tên của `scripts/tl_gws.py` bằng import thuần từ `scripts/` (đo 00:2xZ 01-11: `python -I` import được
     `tl_gws` và `gws_cred_store` không cần bind): `AGENT_CREDS_FILEID`, `_AGENT_CREDS_KEYS`, `_MASTER_KEY_MIN_LEN`,
     `_MASTER_KEY_MIN_DISTINCT`, `_last_refresh_key`, `_public_curl_bytes`; mã hoá/giải mã bằng `gws_cred_store`; gọi webapp
     bằng `scripts/gas.py` (`gas.get('ping')`, `gas.post('agent_creds_put', …)`). Không định nghĩa lại các tên ấy.
   - Điều kiện chịu ghi (Q8): `TL_MASTER_KEY` có và qua luật độ mạnh (≥ `_MASTER_KEY_MIN_LEN` ký tự VÀ ≥
     `_MASTER_KEY_MIN_DISTINCT` ký tự khác nhau); `<CODEX_HOME hoặc ~/.codex>/auth.json` đọc được, là object, `tokens` là object.
     Thiếu/yếu khoá ⇒ `BỎ QUA — <lý do>`; `auth.json` hỏng ⇒ `KHÔNG ĐO ĐƯỢC — auth.json không hợp lệ`.
   - `--neu-doi` (Q17): tệp dấu có và `_last_refresh_key(đĩa) <= _last_refresh_key(dấu)` ⇒ **im lặng**, rc 0, 0 lời gọi mạng.
     Tệp dấu vắng/hỏng ⇒ đi tiếp như không có cờ.
   - Cổng phiên bản (Q10): `ping.version` khớp `^(\d+)\.(\d+)\.(\d+)([a-z]?)$` và ≥ `2.21.2q` theo bộ (số, số, số, chữ);
     không khớp, nhỏ hơn hay ping lỗi ⇒ `KHÔNG HỖ TRỢ — webapp <v>` (ping lỗi: `<v>` = `không đo được`), không ghi.
   - Vòng CAS (Q6), **tối đa 3 lần**: tải blob qua `_public_curl_bytes(AGENT_CREDS_FILEID)`, tính md5, giải mã, kiểm `schema == 1`
     và `rev` là `int`. `_last_refresh_key(bundle.codex_auth) >= _last_refresh_key(đĩa)` ⇒ `ĐÃ CŨ — bỏ ghi`, cập nhật tệp dấu
     theo bản bundle, dừng. Ngược lại dựng payload mới: mọi khoá của `_AGENT_CREDS_KEYS` có trong bản vừa giải mã chép nguyên,
     chỉ thay `codex_auth` bằng bản đĩa, `schema: 1`, `rev: rev_bundle + 1`, `updated_at` UTC; mã hoá, gửi
     `agent_creds_put(fileId, expect_md5=<md5 vừa tính>, b64)`. `CAS_CONFLICT`/`LOCK_BUSY` ⇒ lặp. Hết 3 lần ⇒
     `KHÔNG ĐO ĐƯỢC — xung đột CAS lặp`. Mã lỗi khác ⇒ `KHÔNG ĐO ĐƯỢC — webapp <MÃ>`. Không bao giờ đọc `claude_oauth_token`
     hay `antigravity_api_key` từ môi trường; không bao giờ lùi sang gws.
   - Readback (Q16): `ok:true` ⇒ đòi `md5` trả về == md5 của blob đã gửi; tải lại công khai, giải mã, đòi `rev == rev mới` và
     `codex_auth.last_refresh == last_refresh đĩa`. Cả ba khớp ⇒ `ĐÃ GHI — rev=<N>`, cập nhật tệp dấu. Lệch ⇒
     `KHÔNG ĐO ĐƯỢC — readback lệch`, KHÔNG cập nhật dấu.
   - Hạn chót nội bộ 25 s cho cả lệnh; quá ⇒ `KHÔNG ĐO ĐƯỢC — quá 25 s`.
   - Đầu ra: **đúng một** dòng `agent_creds_ghi_nguoc: <TRẠNG THÁI> — <chi tiết>` với
     `TRẠNG THÁI ∈ {ĐÃ GHI, ĐÃ CŨ, BỎ QUA, KHÔNG HỖ TRỢ, KHÔNG ĐO ĐƯỢC}`, trừ ca im lặng của `--neu-doi`. Chi tiết không bao
     giờ chứa token, khoá hay base64 của blob; giá trị `TL_MASTER_KEY` bị thay `***` nếu lọt vào thông điệp lỗi.
   - `ghi-nguoc` **luôn rc 0**; chỉ sai cú pháp mới rc 2. Không ghi `auth.json`.
3. → `ops/cloud_agent_creds.py`: **tệp dấu** `<CODEX_HOME hoặc ~/.codex>/.tra-luat-agent-creds-dau.json`, quyền 0600, ghi
   nguyên tử (dùng `_ghi_nguyen_tu` sẵn có của helper), chỉ chứa `{"last_refresh": <chuỗi>, "md5": <32 hex hoặc null>}`.
   - `nap` ghi dấu CHỈ KHI dòng `agent_creds:` kết luận là `ĐÃ NẠP` VÀ chi tiết chứa `codex auth.json → ` (bootstrap đã đè
     đĩa bằng bản bundle, nên đĩa == bundle): `last_refresh` đọc từ `auth.json` trên đĩa, `md5: null`. Mọi kết luận khác
     (kể cả `giữ bản đĩa`) ⇒ `nap` XOÁ dấu cũ nếu có, để lượt `Stop` đầu tiên đi mạng một lần.
   - `ghi-nguoc` ghi dấu sau `ĐÃ GHI` (bản đĩa, md5 đã readback) và sau `ĐÃ CŨ` (bản bundle, md5 vừa tải).
4. → `.claude/settings.json`: sự kiện mới `"Stop"`, đúng một hook dạng các hook `SubagentStart`/`SubagentStop` sẵn có (tìm
   gốc kho qua `CLAUDE_PROJECT_DIR` → `git rev-parse` → `$PWD`, tìm `python3`/`python`/`py`), chạy
   `"$PY" "$D/ops/cloud_agent_creds.py" ghi-nguoc --neu-doi || true`, `"timeout": 30`. Mọi khoá/hook cũ giữ nguyên.
5. → `ops/cloud_agent_creds_test.py`: các ca ở `nghiem_thu` A/B/C/S + đột biến trên bản sao tạm, theo khung sẵn có
   (`TinHieuChotCa`, `phan_hang`, `TU_KIEM`). Dòng tổng kết giữ đúng mẫu đã đăng ký ở `.claude/dev/ci_dang_ky_test.py:59`.
6. → `RELEASE_MANIFEST.json`: tái sinh sau mục 1 (CLAUDE.md, Quy ước deploy mục 5).

## `nghiem_thu`

Ca của A, C, S chạy in-process hoặc trên cây tạm: import helper, thay `_public_curl_bytes`, `gas.get`, `gas.post` bằng một
**Drive giả GIỮ TRẠNG THÁI** (byte + md5 của tệp đổi thật sau mỗi lần ghi thành công, đếm lời gọi), đặt `HOME`/`CODEX_HOME` tạm,
`TL_MASTER_KEY` là sentinel mạnh. Ca B trích **nguyên văn** từ `references/Code.2.21.2q.gs` (không chép lại) hàm của action và
nhánh `case`, chạy bằng `node` với `LockService`, `Drive`/`DriveApp`, `PropertiesService`, `Utilities` giả giữ trạng thái.
Thiếu `node` khi cây có `.git` ⇒ ca **ĐỎ** (`TinHieuChotCa`), không `BoQua` (CLAUDE.md, bài học "ca có MẶT khác ca có ĐO").
Mỗi tiêu chí kèm đột biến làm nó đổi màu (L3); đột biến chạy trên bản sao tạm, không ghi tệp thật.

| # | mục tiêu | tiêu chí | phép đo làm ĐỎ (đột biến) |
|---|---|---|---|
| B1 | 1 | md5 hiện tại == `expect_md5` ⇒ `ok:true`, byte của tệp giả == blob gửi, `md5` trả về == md5 đọc lại sau ghi | không ghi ⇒ ĐỎ |
| B2 | 1 | md5 lệch ⇒ `CAS_CONFLICT`, `md5` = md5 hiện tại, byte KHÔNG đổi (so sha256 trước/sau), số lần gọi ghi = 0 | bỏ phép so ⇒ ĐỎ |
| B3 | 1 | bốn ca riêng, mỗi ca 0 lần ghi và đúng mã: `expect_md5` vắng · `expect_md5` = `"abc"` ⇒ `EXPECT_MD5_REQUIRED`; Script Property vắng ⇒ `AGENT_CREDS_NOT_CONFIGURED`; `fileId` khác ⇒ `AGENT_CREDS_FILEID_MISMATCH` | bỏ kiểm `fileId` ⇒ ĐỎ |
| B4 | 1 | blob 65537 byte và blob 0 byte ⇒ `BLOB_SIZE`, 0 lần ghi (hai ca riêng); 65536 byte ⇒ ghi được | đổi ngưỡng thành `>=` 65536 ⇒ ĐỎ |
| B5 | 1 | `tryLock` giả trả `false` ⇒ `LOCK_BUSY`, 0 lần đọc md5, 0 lần ghi | đọc md5 trước khi lấy lock ⇒ ĐỎ (đếm đọc = 1) |
| B6 | 1 | nhật ký đồ giả: thứ tự `tryLock` → đọc md5 → ghi → đọc md5 → `releaseLock`; ném lỗi ở bước ghi vẫn có `releaseLock` | bỏ `finally` ⇒ ĐỎ |
| B7 | 1 | trong `Code.2.21.2q.gs`: `APP_VERSION = '2.21.2q'` đúng 1 lần; `case 'agent_creds_put'` đúng 1 lần (vế âm trên `2p`: 0 lần — đo 00:2xZ 01-11); `node --check` trên tệp ⇒ rc 0 | xoá nhánh `case` ⇒ ĐỎ |
| A1 | 2 | `CLAUDE_CODE_REMOTE` vắng hoặc `false` (hai ca) ⇒ `BỎ QUA — không phải phiên cloud`, 0 lời gọi tải/ping/post | bỏ kiểm biến ⇒ ĐỎ (đếm > 0) |
| A2 | 2 | khoá vắng · khoá 31 ký tự · khoá 40 ký tự gồm 11 ký tự khác nhau (ba ca riêng) ⇒ `BỎ QUA`, 0 lời gọi mạng; khoá 32 ký tự / 12 ký tự khác nhau ⇒ đi tiếp | dùng `< 31` ⇒ ĐỎ ở ca 31 |
| A3 | 2 | ping `2.21.2p` · `2.21.2` · `abc` · ping lỗi (bốn ca) ⇒ `KHÔNG HỖ TRỢ`, 0 lời gọi `post`; `2.21.2q` và `2.22.0` ⇒ đi tiếp | so chuỗi thô (`"2.21.10" < "2.21.2q"`) ⇒ ĐỎ ở ca bổ sung `2.21.10` (phải đi tiếp) |
| A4 | 2 | bundle `last_refresh` == đĩa, và bundle mới hơn đĩa (hai ca) ⇒ `ĐÃ CŨ — bỏ ghi`, 0 lời gọi `post`, `auth.json` byte không đổi | dùng `>` thay `>=` ⇒ ĐỎ ở ca bằng |
| A5 | 2 | đĩa mới hơn ⇒ `ĐÃ GHI — rev=<rev_cũ+1>`; giải mã byte của Drive giả: `codex_auth` == bản đĩa, `claude_oauth_token`/`antigravity_api_key` == bản cũ (so từng khoá), `schema == 1`; môi trường có `CLAUDE_CODE_OAUTH_TOKEN`/`GEMINI_API_KEY` = sentinel khác ⇒ sentinel ấy KHÔNG có trong payload | đọc khoá Claude từ môi trường ⇒ ĐỎ; rơi khoá cũ ⇒ ĐỎ |
| A6 | 2 | Drive giả đổi blob (một phiên khác ghi) giữa lúc tải và lúc `post` ⇒ lần 1 `CAS_CONFLICT`, helper tải lại; bản mới vẫn cũ hơn đĩa ⇒ lần 2 ghi, `rev` = rev của bản phiên khác + 1, và khoá Claude là của bản phiên khác | dựng payload lần 2 trên bản tải lần 1 ⇒ ĐỎ |
| A7 | 2 | Drive giả luôn `CAS_CONFLICT` ⇒ đúng **3** lời gọi `post`, `KHÔNG ĐO ĐƯỢC — xung đột CAS lặp`; luôn `LOCK_BUSY` ⇒ cũng 3; rc 0 | lặp vô hạn hoặc 1 lần ⇒ ĐỎ (đếm ≠ 3) |
| A8 | 2 | Drive giả trả `ok:true` nhưng `md5` khác md5 blob gửi ⇒ `KHÔNG ĐO ĐƯỢC — readback lệch`, tệp dấu KHÔNG đổi; ca thứ hai: md5 đúng nhưng blob tải lại mang `rev` khác ⇒ cũng lệch | bỏ phép tải lại ⇒ ĐỎ ở ca thứ hai |
| A9 | 2 | trong mọi ca A1–A8: stdout+stderr có đúng 1 dòng bắt đầu `agent_creds_ghi_nguoc: ` (ca im lặng của C2 là 0), không chứa sentinel `TL_MASTER_KEY`, sentinel `refresh_token` trong `auth.json` giả, hay base64 của blob gửi (đo cả hai kênh) | in payload lỗi ⇒ ĐỎ |
| A10 | 2 | `ghi-nguoc` rc 0 ở mọi ca A1–A8; `ghi-nguoc --la` ⇒ rc 2, 0 lời gọi mạng | trả rc khác 0 khi CAS thua ⇒ ĐỎ |
| A11 | 2 | `post` giả treo quá hạn (hạn nội bộ đặt nhỏ qua tham số test) ⇒ `KHÔNG ĐO ĐƯỢC — quá …`, lệnh xong trong < 3 lần hạn | bỏ hạn chót ⇒ ĐỎ |
| A12 | 2 | helper không định nghĩa lại sáu tên của `tl_gws` ở mục tiêu 2, đo HAI vế: **(a) AST** — `ast.parse` CHÍNH `ops/cloud_agent_creds.py`, `ast.walk` mọi cấp: không nút nào gắn một trong sáu tên (`ast.Name` với `ctx` `Store`/`Del`, tên của `FunctionDef`/`AsyncFunctionDef`/`ClassDef`, tên gắn bởi `alias` của `Import` hoặc của `ImportFrom` có `module != "tl_gws"`), và mỗi tên mà helper dùng như tên trần thì có trong đúng một `ImportFrom` với `module == "tl_gws"` (dùng qua thuộc tính `tl_gws.<tên>` thì không cần); **(b) đối tượng** — với hai hàm `_last_refresh_key`, `_public_curl_bytes`: nếu module helper có thuộc tính trùng tên thì nó `is` đối tượng của `tl_gws`. Vế (b) KHÔNG áp cho bốn hằng, vì CPython dùng chung đối tượng số nguyên nhỏ và chuỗi được intern nên `is` vẫn đúng với hằng chép lại (finding P2 PR #1095, đo lại: `_MASTER_KEY_MIN_LEN = 32` chép vào vẫn `is` ⇒ `True`) | vế dương: bản import nguyên trạng ⇒ ĐẠT. Ba đột biến riêng, mỗi cái ⇒ ĐỎ: (1) chép `_MASTER_KEY_MIN_LEN = 32` — ĐÚNG giá trị thật, năm tên kia vẫn import — ĐỎ ở vế (a); (2) chép `AGENT_CREDS_FILEID = "<đúng fileId>"` — ĐỎ ở vế (a); (3) định nghĩa lại `def _last_refresh_key(...)` y hệt thân gốc — ĐỎ ở cả (a) lẫn (b). Không được thay đột biến (1) bằng một giá trị KHÁC 32 |
| C1 | 3 | `nap` với `tl.py` giả in `agent_creds: ĐÃ NẠP — rev=3; codex auth.json → /x (0600)` ⇒ tệp dấu tồn tại, quyền 0600 (POSIX), đúng hai khoá `last_refresh` (== đĩa) và `md5` (null); `tl.py` giả in `… giữ bản đĩa …` với dấu cũ có sẵn ⇒ dấu bị xoá; `KHÔNG ĐO ĐƯỢC` ⇒ dấu bị xoá | ghi dấu bất kể chi tiết ⇒ ĐỎ ở ca `giữ bản đĩa` |
| C2 | 3 | `--neu-doi` với dấu có `last_refresh` == đĩa ⇒ 0 dòng đầu ra, 0 lời gọi mạng; đĩa mới hơn dấu ⇒ đi mạng (đếm tải ≥ 1); dấu vắng ⇒ đi mạng; dấu là `[1]` ⇒ đi mạng | so `!=` thay `<=` hoặc bỏ đọc dấu ⇒ ĐỎ |
| C3 | 3 | sau `ĐÃ GHI` dấu = bản đĩa + md5 readback; sau `ĐÃ CŨ` dấu = bản bundle + md5 vừa tải; tệp dấu không chứa sentinel token | không cập nhật dấu sau `ĐÃ CŨ` ⇒ ĐỎ (lượt `--neu-doi` kế đi mạng lại) |
| S1 | 4 | `json.load(.claude/settings.json)`: `hooks.Stop` có đúng 1 hook, lệnh chứa nguyên chuỗi `ops/cloud_agent_creds.py" ghi-nguoc --neu-doi`, có `|| true`, `timeout == 30`; mọi khoá cũ của `hooks` và giá trị của chúng bằng base (so dict từng khoá). Vế âm trên base: `Stop` vắng — đo 00:1xZ 01-11 | đổi lệnh `SubagentStop` ⇒ ĐỎ |
| S2 | 4 | trích chuỗi lệnh `Stop` từ CHÍNH `settings.json`, chạy bằng `bash -c` với `CLAUDE_PROJECT_DIR` trỏ cây tạm có `ops/cloud_agent_creds.py` giả thoát rc 3 ⇒ bash rc 0, và nhật ký của giả ghi đúng argv `["ghi-nguoc", "--neu-doi"]` (POSIX; Windows bỏ qua có lý do) | bỏ `|| true` ⇒ ĐỎ |
| F1 | 5 | `python ops/cloud_agent_creds_test.py` rc 0 và đầu ra khớp mẫu `.claude/dev/ci_dang_ky_test.py:59` (số ca đạt = tổng > 0, đột biến bị giết đúng lý do = tổng > 0, `TU KIEM PHAN HANG: DAT`) — bằng chứng dương, không tin rc (CLAUDE.md r244) | một mutant sống ⇒ ĐỎ |
| F2 | 5 | mọi ca cũ của P2b vẫn đạt (tập tên ca của base ⊆ tập tên ca của head, và không ca nào đổi thân trừ ca phải đổi vì `nap` ghi/xoá dấu — liệt kê trong handoff) | xoá một ca cũ ⇒ ĐỎ |
| J1 | 6 | `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true`, `expected == checked`, `file_count` = base + 1 | sửa một byte `.gs` sau tái sinh ⇒ ĐỎ |
| G1 | — | `python scripts/tl.py --selftest` (Ubuntu, `core.abbrev=7`): delta so base = 0 ca đỏ mới (đơn vị: ca selftest; nền đo lại trên base lúc cấp lease) | một ca đạt trên base mà đỏ trên head ⇒ ĐỎ |
| G2 | — | `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0 | — (canh bất biến; xanh sẵn trên nền) |
| K1 | — | `ruff check --select F ops/cloud_agent_creds.py ops/cloud_agent_creds_test.py` ⇒ 0 | thêm tên chưa định nghĩa ⇒ ĐỎ |
| K2 | — | (a) `git diff --numstat origin/master...HEAD` ⇒ đúng các tệp của `write_set`, ≤ 5 tệp; (b) `git diff --no-index --numstat references/Code.2.21.2p.gs references/Code.2.21.2q.gs` ⇒ ≤ 120 dòng thêm; (c) tổng dòng thêm của bốn tệp còn lại (theo (a)) + số ở (b) ≤ 600 | vượt hoặc có tệp lạ ⇒ ĐỎ; DỪNG hỏi chủ kho |
| L1 | — | lượt CI PR (Ubuntu) trên head ứng viên: mọi job bắt buộc theo `ci.yml` lúc nghiệm thu `success`; đọc nhãn job (CLAUDE.md, bài học (c)). Không đòi lượt Windows | một job bắt buộc đỏ do packet ⇒ ĐỎ |
| M1 | 1, 2 (LIVE, sau land) | chủ kho deploy `Code.2.21.2q.gs` qua `clasp` giữ deployment ID và đặt Script Property `TL_AGENT_CREDS_FILEID`; chủ kho duyệt riêng trước từng vế. (i) `gas.get('ping').version == "2.21.2q"`; (ii) gọi `agent_creds_put` với `expect_md5` = 32 số `0` ⇒ `CAS_CONFLICT`, và `md5Checksum` của tệp trên Drive trước/sau bằng nhau; (iii) phiên Claude Code web có `auth.json` mới hơn bundle (sau một lượt `codex` thật) ⇒ `ghi-nguoc` in `ĐÃ GHI — rev=N+1`; một phiên **mới** ⇒ log hook có `agent_creds: ĐÃ NẠP — rev=N+1`. Biên nhận chỉ ghi rc, mã, rev, md5; không ghi token | `chưa đo được` cho tới khi chạy thật. Vế (ii) là phép đo DUY NHẤT xác nhận CAS LIVE; vế (iii) là phép đo DUY NHẤT xác nhận đường ghi tới đích. Không thay bằng phép đo khác. Ai đo: chủ kho (deploy, (i), (ii)) và phiên điều phối hoặc executor ((iii)), sau khi chủ kho duyệt |

Ghi chú L6. B7, S1 có vế dương trên head và vế âm trên base (L6a). S1 so dict/chuỗi trên JSON đã parse, không khớp dòng (L6b
không áp dụng); B7 khớp `case 'agent_creds_put'` — là toàn bộ lời khẳng định, trên một dòng của tệp mã, không phải Markdown.
B3, B4, A1–A4, C1, C2 đếm từng ca riêng (L6c). Không có lời khai số lượng dạng chữ (L6d). Không có lời khai "không cổng nào
cưỡng chế" (L6e).

Chạy thử trên nền (00:2xZ 01-11, `4952cff3`): `references/Code.2.21.2q.gs` chưa có (B1–B7 chưa chạy được), `ghi-nguoc` 0 lần
trong `ops/cloud_agent_creds.py` (`main` chỉ nhận `nap`/`cai-agy`, dòng 190), `.claude/settings.json` có bốn sự kiện
`SessionStart`, `PreToolUse`, `SubagentStart`, `SubagentStop` — không có `Stop` (S1 vế dương "chưa làm"). G2 xanh sẵn vì canh
bất biến.

## Kích thước

**Ước tính, chưa đo** (00:2xZ 01-11). `.gs` diff so `2p` ~70 · helper ~160 · test ~320 · `settings.json` ~12 · manifest ~3 ⇒
**~565 dòng thêm** theo cách đếm K2. Riêng `git diff --numstat` thô sẽ báo `Code.2.21.2q.gs` ~4150 dòng thêm (chép nguyên
4083 dòng của `2p`, tiền lệ mọi bản webapp); con số thô ấy KHÔNG tính vào trần (vòng 1 Q5, vòng 2 Q13). Đối chiếu: P2a +524 /
13 tệp (PR #1063), P2b +700 / 8 tệp (PR #1073). Lời gọi Codex theo `ADR-0052`: **8** (vòng 2 Q18). Lời gọi thứ 8 chưa approve
⇒ Review Rescue Checkpoint (`ADR-0037`). Trước MỖI lời gọi Codex, đếm số đã dùng (CLAUDE.md, bài học trần lời gọi Codex).

## `hinh_dang_ke_thua`

`khong_ap_dung` — packet này không khắc phục packet nào. Ghi chú từ chuỗi cloud-setup cho người thi hành:
- P2a dùng hết 8/8 lời gọi Codex; bốn finding cùng hình dạng buộc chủ kho đảo cấu trúc. P2b tốn 7 lời gọi; một finding P2 thật
  là công thức chép sai từ spec r1 mục 10 sang RUNBOOK. Ở packet này hai lớp dễ tái phát nhất là **CAS không nguyên tử** (đọc
  md5 ngoài lock, payload dựng trên bản cũ — A6, B5, B6) và **rò credential qua thông điệp lỗi** (A9). Một finding cùng hình
  dạng lần thứ ba ⇒ dừng, hỏi chủ kho có nên đổi cấu trúc không, đừng vá tiếp.
- P1 vượt trần ba lần vì write set thiếu tệp cơ học. Ở packet này manifest đã nằm sẵn trong write set; dòng đăng ký CI không
  phải đổi vì mẫu tổng kết giữ nguyên.

## `chua_do_duoc`

- **Drive Advanced Service ghi đè nội dung trong GAS giữ nguyên `md5Checksum` đọc lại ngay sau ghi**: chưa đo trên webapp LIVE.
  Nếu đọc lại trả md5 cũ (trễ nhất quán), vế readback của client sẽ báo `readback lệch` thay vì ghi sai — fail-close; đo ở M1.
- **Chi phí lock chung với registry**: `ghi-nguoc` giữ script lock vài trăm ms; chưa đo ảnh hưởng tới `withRegLock_`
  (`tryLock(30000)`) khi ingest đang chạy.
- **Hook `Stop` chạy bao lâu một lần và có bị cắt khi container thu hồi không**: theo tài liệu Claude Code chạy sau mỗi lượt
  trả lời; chưa đo trong phiên remote của kho.
- **Hai phiên cùng một chuỗi refresh token**: nếu phiên A xoay token, phiên B (cùng xuất phát) sẽ không làm mới được nữa; CAS
  chỉ bảo đảm bản ghi lên `.enc` là bản có `last_refresh` mới nhất, không bảo đảm token của B còn sống.
- **Webapp nhận POST base64 ≤ 64 KB qua đường hai bước urllib (KI-01)**: blob thực đo được vài KB (`tl_agent_creds.enc` P1);
  chưa đo trần thực của đường POST.
- **`CLAUDE_CODE_REMOTE` có được đặt trong tiến trình hook `Stop`**: đã đo có ở hook SessionStart (P2b); chưa đo ở `Stop`.
- **Windows**: không đo; hook `ghi-nguoc` tự `BỎ QUA` khi không phải phiên cloud.

## `errata_r2`

- **Chỗ sửa duy nhất: dòng A12 của bảng tiêu chí.** Phép đo r1 (`thuộc tính helper is đối tượng tl_gws`) không phân biệt được
  import với hằng chép lại: trên CPython số nguyên nhỏ (−5…256) dùng chung đối tượng, nên `_MASTER_KEY_MIN_LEN = 32` định nghĩa
  lại trong helper vẫn cho `is` ⇒ `True` — đúng đột biến mà dòng A12 của r1 khai phải ĐỎ, và F1 đòi mọi đột biến bị giết.
  Nguồn: finding P2 của Codex connector trên PR #1095 (review comment 4433878395, head `9440278a`); phiên điều phối đo lại tại chỗ
  01-11-2026 ~00:43Z (`exec('_MASTER_KEY_MIN_LEN = 32')` rồi so `is` với `32` ⇒ `True`).
- **Sửa thế nào:** thêm vế (a) đo bằng AST trên CHÍNH tệp helper (không phụ thuộc cache đối tượng), giữ vế `is` chỉ cho hai hàm
  (đối tượng hàm không được dùng chung), và khai ba đột biến riêng kèm vế dương. Đột biến (1) giữ ĐÚNG giá trị `32` — làm đúng
  điều reviewer cảnh báo: đổi mutant sang giá trị khác sẽ bỏ lọt chính ca chép `32`.
- **Không đổi:** `write_set`, `nang_tran`, `tran_loi_goi_codex`, mọi tiêu chí khác, `hinh_dang_ke_thua`, `chua_do_duoc`. Số
  dòng helper thêm do A12 mới nằm trong trần 600 dòng của r1 (một hàm kiểm AST cỡ 20–30 dòng trong tệp test).

