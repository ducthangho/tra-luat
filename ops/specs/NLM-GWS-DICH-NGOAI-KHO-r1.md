tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# NLM-GWS-DICH-NGOAI-KHO r1 — đích ghi credential NLM/GWS/config của `tl_gws.py` phải qua danh sách cho phép, nằm ngoài kho git và không ghi xuyên liên kết

- packet_id: NLM-GWS-DICH-NGOAI-KHO; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #433 |
| `nguon_cap_viec` | Issue #433 (packet khắc phục "keep ephemeral credential destinations outside the repository", tiền nhiệm #431 / PR #432). Kiến trúc cũ của #433 (`session_credentials.py`, `codex_cred.py`, PR #434–#441, #447) đã bỏ; chủ kho duyệt phạm vi mới ngày 18-11-2026: chỉ phần đích ghi credential NLM/GWS của `scripts/tl_gws.py` còn hở sau WP1334 (`8ed3503`, `3b23422`, đã land chốt cho `CODEX_HOME`). |
| `review_class` | `sensitive`: `scripts/tl_gws.py` là đường ghi credential (cookie NLM, `credentials.json` của gws, token GAS trong `~/.tra_luat_config.json`). Các tệp còn lại của write set (fragment test, bundled module) đi theo nó. Đối chiếu lại bằng `lease_publish check` khi cấp lease; không rõ thì giữ `sensitive` (fail-closed). |
| `base` | `641108cb997872b0ef2a277ea9c8faf8b82532bb` (`origin/master` lúc soạn, fetch 2026-11-18T04:47:55Z); lease ghi OID base thật lúc cấp. Blob `scripts/tl_gws.py` ở base: `cddf7d35f6d727214a88d30a51f790001f881cc6` (sha256 `1ca18373768fa6618091bb223ed547b7ea1da6cb4fa793a63dd639bd6c526b9f`). Mọi số dòng ở §0 tính trên blob này. |
| `lich_su_soan` | Hai lượt review Codex và quyết định của chủ kho 18-11-2026 (phương án B, tách packet) — §9. Phần W4/W5 tách sang đặc tả `GWS-CRED-DICH-NGOAI-KHO-r1.md`. H1 và dòng `packet_id` giữ `revision: 1` vì băm chưa được duyệt. |

## 0. Hiện trạng (đo trên base, Linux, Python 3.13.18, bản sao `git archive` trong scratchpad, HOME tạm, dữ liệu GIẢ, không mạng)

Mốc đo: lượt soạn đầu 2026-11-18T04:47:55Z–04:59:28Z; lượt sửa theo review 1 05:13Z–05:21Z; theo review 2 05:31Z–05:40Z; tách packet 05:45Z–05:55Z. Các mốc phút là lời khai
của phiên soạn, chỉ phép đo nào ghi kèm giờ máy (`date -u`) mới có giờ đo được.

### 0.1 Các chỗ ghi tệp credential trong `scripts/tl_gws.py`

Liệt kê đủ bằng `grep -n -E 'open\([^)]*"(w|wb|a)"|write_text|write_bytes|_ghi_nguyen_tu_0600\(|os\.replace|makedirs'`
trên blob base, rồi đọc ngữ cảnh từng hit. Các hit KHÔNG thuộc packet: tải media/tạm (380, 390, 668, 1806),
cài Python/nlm/gws (1423, 1487–1501, 2275), `_ghi_nguyen_tu_0600` (1158–1170) và chỗ gọi nó ở `_bootstrap_agent_creds`
(1271, đã có chốt WP1334 ở 1259). Sáu chỗ ghi credential CHƯA có chốt kho (số dòng đo lại 05:14Z). Packet này xử W1, W2, W3, W6; W4, W5 thuộc packet `GWS-CRED-DICH-NGOAI-KHO` (tách theo quyết định chủ kho 18-11-2026):

| # | hàm | dòng | đích | cách ghi hiện tại |
|---|---|---|---|---|
| W1 | `cmd_nlm_auth_pull` | 1654–1663 | `~/.notebooklm-mcp-cli/<rel>` | `dst = os.path.join(nbase, *str(rel).split("/"))` (1656), `makedirs` (1657), `open("w")` (1658), `chmod` sau |
| W2 | `cmd_bootstrap`, nhánh `bundle.get("nlm_auth")` | 1742–1751 | như W1 | cùng mẫu (1745–1747) |
| W3 | `_nlm_auth_load` | 1966–1974 | như W1 | cùng mẫu (1968–1970) |
| W4 | `cmd_bootstrap`, nhánh `bundle.get("gws_cred")` | 1729–1736 | `$GOOGLE_WORKSPACE_CLI_CONFIG_DIR` hoặc `~/.config/gws` + `/credentials.json` | `makedirs` (1730), `open("wb")` (1732) không nguyên tử, `chmod` sau |
| W5 | `_gws_auth_load` | 1879–1886 | như W4 | cùng mẫu (1880–1882) |
| W6 | `cmd_bootstrap`, nhánh `bundle.get("token")` | 1707–1718 | `~/.tra_luat_config.json` (mang token GAS) | `existing.update({k: v … if k != "gws_cred"})` (1715) chép CẢ `nlm_auth` vào config; `open("w")` (1716) ghi đè tại chỗ, `chmod` sau |

`rel` ở W1–W3 lấy thẳng từ khoá của `nlm_auth` trong bundle đã giải mã; không kiểm `..`, đường tuyệt đối, dấu `\` hay kho.
Nhánh W2 nằm NGOÀI cổng `--no-nlm` (cổng ở dòng 1770 chỉ chặn `_ensure_nlm_installed`), nên chạy cả khi hook gọi
`bootstrap --env code --no-nlm` (`ops/cloud_agent_creds.py`, neo đột biến `A6_bo_no_nlm` của `ops/cloud_agent_creds_test.py`).
`degraded = False` được khởi tạo ở dòng 1725, SAU W6; mọi lần từ chối đặt cờ ấy trước dòng 1725 sẽ bị ghi đè (ràng buộc cho M3).

**W6 là phát hiện của lượt soạn này, ngoài danh sách đã nêu khi chủ kho duyệt hướng (18-11-2026).** Nó lộ ra ở phép đo
F dưới đây: HOME nằm trong kho thì `bootstrap` để lại `home/.tra_luat_config.json` trong cây kho. Không chốt W6 thì tiêu
chí "HOME trong kho ⇒ cây kho sạch" (N7) không đạt được, nên theo L2 nó được đưa vào write set ở đây (M5) chứ không để
phiên thi hành tự gặp. Chủ kho thấy mục này khi duyệt băm (§6, E2).

**Phạm vi rà ngoài `tl_gws.py`** (bảng sự thật của review lượt 1, chưa đo lại ở lượt sửa): `cmd_gws_bootstrap_cowork`
(2265, 2322) và `tl_core/ops_misc.py` (592, 620) chỉ GỌI lại W5/W3, không ghi riêng. Các hit ghi/copy trong `scripts/tl.py`
là probe thư mục tạm, mã tự phục hồi, PDF tạm. Trong `ops/cloud_agent_creds.py`, `_ghi_dau` có chốt kho và chỉ ghi metadata;
`gop_settings` và `dat_env_file` có thể ghi lại nội dung ĐÃ CÓ vào đường dẫn trong kho (`dat_env_file` ghi vào đích do
`CLAUDE_ENV_FILE` chỉ định) nhưng không nhận credential từ bundle. Ba đường ấy ngoài packet; packet này chỉ chốt đích của
credential đến từ bundle/tải Drive.

### 0.2 Phép đo hành vi trên base

Lượt soạn đầu (04:51:21Z, script đo chạy từ thư mục riêng, `python3 -I`):

| phép | dựng | kết quả trên base |
|---|---|---|
| A | `cmd_nlm_auth_pull`, bundle `nlm_auth = {"auth.json": …, "../thoat.json": SENTINEL}` | rc 0; `thoat.json` ghi ở `HOME/thoat.json` (NGOÀI `~/.notebooklm-mcp-cli`) |
| B | `cmd_bootstrap --env code --no-nlm --no-gws`, cùng `nlm_auth` | rc 1 (degraded vì thiếu `gws_cred`); `HOME/thoat.json` vẫn được ghi ⇒ `--no-nlm` không chặn W2 |
| C | `_nlm_auth_load(force=True)`, cùng `nlm_auth` | trả `True`; `HOME/thoat.json` được ghi |
| D | `cmd_nlm_auth_pull`, `nlm_auth = {"profiles/x/la.json": …}` (không `..`, ngoài `_NLM_AUTH_RELS`) | rc 0; tạo `~/.notebooklm-mcp-cli/profiles/x/la.json` |
| E1 | `_gws_auth_load`, `GOOGLE_WORKSPACE_CLI_CONFIG_DIR=<kho git tạm>/gwscfg` | `(True, …/kho/gwscfg/credentials.json)`; `git status --porcelain` = `?? gwscfg/credentials.json` |
| E2 | `cmd_bootstrap --env code`, bundle có `gws_cred`, cùng biến | rc 0; porcelain = `?? gwscfg/credentials.json` |
| F | `cmd_bootstrap --env code --no-nlm --no-gws`, HOME = `<kho git tạm>/home`, bundle có `token` + `nlm_auth` hợp lệ | rc 1; porcelain = `?? home/.notebooklm-mcp-cli/auth.json`, `?? home/.tra_luat_config.json` |
| G | `cmd_bootstrap --env chat` (khuôn của `r973_bootstrap_khong_export_khong_ghi_gemini`), HOME tạm | rc 0; HOME chỉ có `.tra_luat_config.json`; `HOME/.claude` KHÔNG tồn tại |

Lượt sửa (2026-11-18T05:17:57Z, `python3 -I scratchpad/rig433/do_symlink.py <bản sao base>`, tệp thật trong thư mục tạm,
K = thư mục có `.git`), đo các đường mà một chốt chỉ đặt ở THƯ MỤC CHA để lọt:

| phép | dựng | kết quả |
|---|---|---|
| S1 | `~/.notebooklm-mcp-cli/auth.json` là symlink tới `K/dich.json`; HOME ngoài kho; `cmd_nlm_auth_pull` | `_trong_kho_git(thư mục cha)` = `None`; rc 0; `K/dich.json` mang SENTINEL ⇒ ghi xuyên symlink vào kho |
| S2 | `~/.notebooklm-mcp-cli/profiles/default` là symlink tới thư mục NGOÀI mọi kho | chốt cha = `None`; rc 0; `cookies.json` nằm ở thư mục ngoài NLM root |
| S3 | `auth.json` là hardlink của một tệp khác | rc 0; tệp kia mang SENTINEL, `st_nlink` 2 ⇒ `open("w")` sửa inode dùng chung |
| S4 | `_ghi_nguyen_tu_0600` trên đích là symlink vào kho; trên đích là hardlink | đích trong kho giữ `CU`, `a.json` thành tệp thường; tệp kia giữ `CU`, `st_nlink` 1 ⇒ thay tệp nguyên tử không ghi xuyên tệp cuối |
| S5 | `_ghi_nguyen_tu_0600` với thư mục cha là symlink ra ngoài | tệp được tạo ở thư mục đích của symlink ⇒ thay nguyên tử KHÔNG chặn được thành phần thư mục là symlink |
| S6 | `TL_AGENT_CREDS_FILEID=""` | `os.environ.get(...) or AGENT_CREDS_FILEID` (1244) rơi về hằng baked (1089) ⇒ rig để biến rỗng vẫn gọi tải thật |

Kết luận cho thiết kế (M1, M2, M5): cần ba lớp riêng — chốt kho trên thư mục cha (WP1334), từ chối symlink ở mọi thành
phần từ gốc đích trở xuống gồm chính tệp đích (S1, S2, S5), và thay tệp nguyên tử (S3, S4).

### 0.3 Tập khoá `rel` mà phía stage sinh ra — tiền đề của danh sách cho phép (đọc mã base, `git grep`/`git log -S` trên `origin/master`)

- Mọi đường đưa `nlm_auth` lên Drive đi qua MỘT cổng `_nlm_files_after_live_canary` (định nghĩa 867), được gọi ở ba chỗ (đo
  05:33Z): `secrets-stage` trong `_secrets_stage_body` (định nghĩa 931, lời gọi canary 972), `secrets-set --nlm` trong
  `_secrets_set_body` (định nghĩa 998, lời gọi canary 1037, kèm `nlm_cred.enc` ở 1076) và `nlm-auth-stage` trong
  `_nlm_auth_stage_body` (định nghĩa 2004, lời gọi canary 2026). Cổng ấy trả `_nlm_auth_files()` (737), hàm này chỉ lặp
  `_NLM_AUTH_RELS` (704) và có thể ghi đè `out["auth.json"]` (749) — khoá ấy thuộc `_NLM_AUTH_RELS`.
- Nguồn `nlm_auth` khác (config cũ, bundle Drive mang sẵn) bị `_nlm_bundle_guard` (897) từ chối ở cả `secrets-stage` (979)
  lẫn `secrets-set` (1050) theo phép so `is`. Các hit `nlm_auth` trong `tl_core/ops_misc.py` và `tl_core/profile_env.py`
  là cờ trạng thái, không sinh bundle (review lượt 1 xác nhận).
- `git grep '"nlm_auth"'` trên `scripts/**` (trừ test) ra đúng các chỗ trên; không script `.sh`/`.ps1` nào dựng `nlm_auth`.
- Provenance (đo 05:19Z): `git log -S '_NLM_AUTH_RELS =' HEAD -- scripts` ⇒ `394e934` (2026-07-02, baseline v1.29.4),
  `47310dc` (2026-07-11), `bf5ca78` (2026-07-11). `git grep '^_NLM_AUTH_RELS ='` tại cả ba commit cho cùng giá trị
  `("auth.json", "profiles/default/cookies.json", "profiles/default/metadata.json")`, và base có đúng một định nghĩa (dòng 704).
- Kết luận: tập khoá stage sinh ra ⊆ `_NLM_AUTH_RELS`. Danh sách cho phép = đúng `_NLM_AUTH_RELS`, không mở rộng.
  Bundle sinh trước baseline v1.29.4 không đo được (§8).

### 0.4 Hạ tầng có sẵn và ràng buộc kề bên

- `_trong_kho_git(path)` (1119–1138, WP1334): đi lên tổ tiên trên hai chuỗi (từ vựng `abspath` và `realpath` của đường
  gốc), `lstat` mục `.git`. `_ghi_nguyen_tu_0600(path, data)` (1158–1170): `makedirs(0o700)`, `mkstemp` cùng thư mục,
  `fsync`, `chmod 0600`, `os.replace`; lỗi thì xoá tệp tạm rồi ném lại (có thể ném `OSError`).
- **`lstat` không thấy symlink khi đường có hậu tố** (đo 05:31:18Z, `python3 -I scratchpad/rig433/do_luot2.py`, `alias` là
  symlink tới thư mục): `lstat` báo symlink cho `alias` (tuyệt đối và tương đối), báo thư mục THƯỜNG cho `alias/`, `alias/.`,
  `alias/./`, `alias//` (tuyệt đối) và `alias/`, `alias/.` (tương đối). `os.path.normpath("T/alias/../x")` = `T/x`, tức
  gộp `..` theo từ vựng, khác đường kernel đi khi `alias` là symlink. ⇒ M1 phải tách thành phần và kiểm từng tiền tố, không
  `lstat` chuỗi thô và không `normpath`/`abspath` trước khi kiểm.
- **`load_creds` đọc `~/.tra_luat_config.json` TRƯỚC W6** (đo 05:31:28Z, cùng script): HOME tạm có config giả, `TL_*` xoá,
  `tl.load_creds(None, None)` ⇒ `TL_TOKEN` = giá trị trong tệp. Loader đọc bằng `Path(p).read_text` (`tl_core/profile_env.py:43`,
  ứng viên ở `_config_candidates`, 60–73, gồm `Path.home() / ".tra_luat_config.json"`), nên bộ quan sát thay `builtins.open`
  KHÔNG thấy lần đọc ấy (đo: quan sát `open` báo không mở, trong khi token đã được đặt). `cmd_bootstrap` gọi loader (1687) trước
  `_secrets_fetch` (1691) để có `TL_TOKEN` cho đường tải webapp.
- Windows: `stat.FILE_ATTRIBUTE_REPARSE_POINT` có trong module `stat` và `os.lstat(...).st_file_attributes` có trên Windows từ
  Python 3.5; `os.path.isjunction` chỉ có từ 3.12, trong khi tài liệu kho khai Python ≥ 3.11 (`SKILL.md:161`,
  `references/RUNBOOK.md:181`). CI ghim `python-version: "3.12"` (`ci.yml:164` …). Chưa đo trên Windows thật.
- `ops/cloud_agent_creds_test.py` (NGOÀI write set) mang các đột biến `PD*` neo vào CHUỖI CON của `tl_gws.py` (loại tệp
  `tlgws`, bảng ở dòng 796–806); mỗi neo phải khớp đúng một lần, không thì runner báo `HONG`. Các neo:
  `        if (kho := _trong_kho_git(os.path.dirname(dst))) is not None:` (PD1, PD5),
  `    return None   # không tổ tiên nào có \`.git\`` (PD2), `                os.lstat(g)\n` (PD3, PD4),
  `            if os.path.dirname(d) == d:\n                break\n` (PD5), `    for d in dict.fromkeys((os.path.abspath(path), os.path.realpath(path))):`
  (PD7 ×2) và `os.path.abspath(path), os.path.realpath(path))):` (PD8). Mã mới KHÔNG được chứa nguyên văn chuỗi nào
  trong số này. Bẫy cụ thể: cách viết tự nhiên `if (kho := _trong_kho_git(os.path.dirname(dst))) is not None:` ở thụt lề
  8 trùng neo PD1 — đặt tên biến khác.
- Fragment `wp727_tl_gws_refresh` (đang có) khoá NGUYÊN VĂN và sha256 các chuỗi thông báo thành công của `nlm-auth-pull`
  và `nlm-auth-load` (`_CHO_PHEP`, `_CHUOI_CHO_PHEP`) và chạy `cmd_nlm_auth_pull`/`_nlm_auth_load` với jar
  `{"auth.json", "profiles/default/cookies.json"}` trong HOME tạm. Mã mới không đổi hai dòng `print(f"[nlm-auth-pull] ✓ …")`
  (1666–1667) và thông báo `[nlm-auth-load] ✓` của `cmd_nlm_auth_load`.
- Driver của `bundle_fragment_check.py` (`_DRIVER`, từ dòng 52) đọc stdout của tiến trình con làm JSON; fragment hiện có in
  tổng kết ra stderr (`wp1099_nlm_nap_lai.py:372–373`, `file=sys.stderr`).
- Hook phiên gọi `bootstrap` qua `ops/cloud_agent_creds.py nap`, lọc dòng `agent_creds:` và luôn trả 0 (`A8_tra_rc_bootstrap`);
  rc 1 của bootstrap không gãy hook, nhưng một ngoại lệ ném ra khỏi `cmd_bootstrap` trước dòng `agent_creds:` thì làm mất dòng ấy.
- **Quy ước test** (`docs/PROTOCOL_DA_PHIEN.md` ở base, dòng 359–363): regression test mới nằm ở
  `scripts/test_fragments/wp<issue>_<slug>.py`; `scripts/tl_selftest.py` là harness cũ, "mặc định không thuộc packet
  thường". Đặc tả này KHÔNG chạm `tl_selftest.py` (điều kiện `.claude` chuyển vào fragment, M6 — xem §6 E2).
- **Artifact land-only** (`docs/PROTOCOL_DA_PHIEN.md` ở base, dòng 864–868, nguyên văn): "Worker không sửa `VERSION`, hằng
  version trong `tl.py`, header `SKILL.md`, `CHANGELOG.md` hoặc `RELEASE_MANIFEST.json`. … phiên land sinh tất định bundled
  test module `scripts/tl_test_fragments_bundled.py` từ các fragment, rồi mới gán release, bump ba chỗ, hợp nhất changelog
  fragment và tái sinh manifest." Dòng 1007–1008 (§10.2.4): "Worker dùng đúng land generator để sinh bundled candidate trong
  thư mục tạm ngoài repo, kiểm byte/topology nhưng không sửa module land-only trong diff." Docstring của
  `_test_fragments_check` (`tl_core/release.py:207`) gọi module ấy là "land-only bundled module", và `cmd_test_fragments_check`
  là "Opt-in land gate".
- **Thực hành, đo 05:34Z.** Mẫu: TOÀN BỘ 12 tệp `scripts/test_fragments/*.py` trên base; với mỗi tệp lấy commit THÊM nó
  (`git log --diff-filter=A … | tail -1`, cả 12 đều là commit một cha) rồi đếm hai tệp artifact trong commit ấy. Kết quả: 5/12
  mang CẢ bundled lẫn manifest (`a1bbb44` wp1030, `32ba025` wp1099, `f9e4342` wp1121, `232ac54` wp1134, `c46f728` wp1326);
  7/12 không mang tệp nào (`b303a73` wp45, `6f24f90` wp47, `b53b466` wp49, `90e8579` wp88, `96e44d9` wp725, `39f52bd` wp726,
  `c69bff1` wp727). Trong 7 tệp ấy, ít nhất wp725–727 được land bù sau: chú thích `tl_selftest.py` 22737–22742 ghi master đỏ
  `release-verify --strict` giữa chừng "đúng lý do protocol §9 để manifest cho phiên land"; ba tệp wp45/47/49 thuộc giai đoạn
  dựng chính cơ chế fragment, chưa đo vai trò. Ngoài mẫu: `f48a5b2` (wp1325, SỬA fragment có sẵn) không mang, và commit land
  `85c1974` tái sinh cả hai. Không có tỉ lệ "đa số" nào làm căn cứ ở đây; đặc tả theo nguyên văn protocol.
- **Hệ quả đo được cho CI của PR** (bản sao base + một fragment rỗng `wp433_thu_rong`):
  · 05:16:04Z, KHÔNG tái sinh bundled: `python3 .github/checks/bundle_fragment_check.py --json` ⇒ rc 1,
  `problems: ["TEST_ID_SET_MISMATCH"]`, `failed: []`, `case_count` 12.
  · 05:31:35Z–05:31:48Z, cùng bản sao, CHỈ tái sinh `scripts/tl_test_fragments_bundled.py` bằng `generate_bundled_module_bytes`
  (không đụng manifest): cùng lệnh ⇒ rc 0, `ok: true`, `failed: []`, `case_count` 13; `release-verify RELEASE_MANIFEST.json
  --strict --json` ⇒ rc 2, `ok: false`, `expected_file_count 185 == checked_file_count 185` (sha của bundled lệch manifest committed).
  · Lane nào kiểm gì (`ci.yml` ở base): bước `bundled-fragment check (topology gói)` (294–296) chỉ gác bởi `che_do != 'duong_nhanh'`,
  tức chạy trên PR; `release-verify strict (lane LAND — manifest committed)` (501–503) gác bởi `github.ref == 'refs/heads/master'`;
  `release-verify strict (lane WORKER — manifest TẠM ngoài repo)` (521–532) gác bởi `github.ref != 'refs/heads/master'` và sinh
  manifest tạm từ chính cây. ⇒ Trên PR: bundled committed bị kiểm, manifest committed KHÔNG bị kiểm; trên master: cả hai.
  · Review lượt 2 đo độc lập cùng kết quả hai vế (rc 1 / rc 0, 12 / 13 ca).
  · Chưa đo: branch protection của `master` (bước ấy có thuộc required check không). Khe này được xử bằng quyết định của chủ kho 18-11-2026: worker mang riêng bundled (§1).
- CI chạy fragment ở hai topology: cây dev (`--selftest`) và gói giải nén (`bundle_fragment_check.py`, không `.git`, không `ops/`).
- Nền đo (base, lượt soạn đầu): `release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok: true`,
  `expected_file_count 185 == checked_file_count 185` (04:52:44Z). `ruff check --select F` (ruff 0.17.5, 04:52:40Z):
  `scripts/tl_gws.py` 91 F821 + 4 F401 + 2 F811. Tiêu chí là DELTA = 0, không phải 0 tuyệt đối.
- Lease đang giữ (đo 04:53:15Z, `ops/lease_publish.py ai-dang-giu <đường>` sau khi so tập ref `ls-remote` với
  `for-each-ref`: 306 trên máy chủ, 307 cục bộ, 0 thiếu): `scripts/tl_gws.py` và đường fragment ⇒ `NGƯỜI_GIỮ 0`.
  `scripts/tl_test_fragments_bundled.py` (thuộc write set §1) CHƯA đo. Đo lại khi cấp lease.

### 0.5 Nền đo của bộ test (base)

- `python3 scripts/tl.py --selftest` trên bản sao base (04:52:53Z–04:56:03Z): `== tl selftest 1772/1778 ==`, rc 1. Sáu ca ĐỎ:
  `r328_deploy_ep_utf8_hai_chieu`, `r218_docclaims_sach_khong_bao_gia`, `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`,
  `r244_script_deploy_khong_vao_goi`, `r249_bao_cao_rasoat_ngoai_goi`, `r251_deploy_guard_chiu_duoc_banner_gws`. Bản sao là
  `git archive` không `.git` và không ghim `core.abbrev`; nguyên nhân sáu ca CHƯA phân tích, nên đây là nền của RIG này,
  không phải của clone. Các ca liên quan ĐẠT trên cùng lượt: `r973_bootstrap_khong_export_khong_ghi_gemini`,
  `r973_bootstrap_auth_json_nguyen_tu` (gọi thẳng `_bootstrap_agent_creds`, không qua W1–W6), `wp727_tl_gws_refresh`,
  `wp1099_nlm_nap_lai` (`CA A: 12/12 · DOT BIEN: 25/25`). Phiên thi hành đo lại nền trên clone thật, dựng base và head trong
  CÙNG một lệnh (bài học delta hai vế của `CLAUDE.md`), và so DELTA.
- `python3 ops/cloud_agent_creds_test.py` trên bản sao base (04:54:22Z–04:59:20Z, không `.git` ⇒ 5 ca `_git_base` BỎ QUA đúng
  luật, gồm `pd1`, `pd7`): `CA: 55/55 dat` · `DOT BIEN: 84/84 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (4 dot bien)` ·
  `TONG: DAT`, rc 0. Trên clone có `.git` thì năm ca ấy chạy; phiên thi hành đo lại nền ở đó.

## 1. `write_set`

```
scripts/tl_gws.py
scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py
scripts/tl_test_fragments_bundled.py
```

`scripts/tl_test_fragments_bundled.py` vào write set theo **quyết định của chủ kho ngày 18-11-2026** (phương án B của bản
`188c55bf…`): worker mang riêng tệp ấy, chỉ sinh bằng `generate_bundled_module_bytes(scripts/test_fragments)`, KHÔNG mang
`RELEASE_MANIFEST.json`. Đây là ngoại lệ so với nguyên văn `docs/PROTOCOL_DA_PHIEN.md` dòng 864–868 ("phiên land sinh … bundled").
**Điều kiện trước khi cấp lease (E2 — chờ chủ kho):** có comment của chủ kho trên Issue #433 cấp ngoại lệ ấy, nêu đúng `packet_id`
`NLM-GWS-DICH-NGOAI-KHO`, đúng một tệp `scripts/tl_test_fragments_bundled.py` và sha256 của đặc tả đã đóng băng; lease trỏ tới
URL comment ấy. Không có comment ⇒ không cấp lease. Ngoại lệ không lan sang packet khác (packet
`GWS-CRED-DICH-NGOAI-KHO` cần dòng của riêng nó). Phiên land tái sinh `RELEASE_MANIFEST.json` trong commit land (N12).

## 2. `ngoai_pham_vi`

- **W4, W5** (`credentials.json` của gws) và chuẩn hoá `GOOGLE_WORKSPACE_CLI_CONFIG_DIR`: thuộc packet tách riêng
  `GWS-CRED-DICH-NGOAI-KHO` (đặc tả `GWS-CRED-DICH-NGOAI-KHO-r1.md`, quyết định tách của chủ kho 18-11-2026), packet ấy phụ thuộc
  packet này đã land. Packet này không sửa dòng nào của W4 (1729–1736) hay `_gws_auth_load` (1860–1889).
- Mục 3 của #433 (`GITHUB_PAT` → `GH_TOKEN` cho tiến trình con) và mục 8 (bắt buộc `--secrets-file` cho `tl-bootstrap`):
  chủ kho quyết định 18-11-2026 là lỗi thời / đúng theo thiết kế. Không làm.
- Các finding `SPEC-043…` của PR #447 và mọi tệp của kiến trúc cũ: bỏ cùng kiến trúc cũ.
- Không đổi ngữ nghĩa `--no-nlm`: W2 vẫn ghi jar NLM khi bundle mang `nlm_auth`, kể cả có `--no-nlm` (`ADR-0064`).
- Không chốt đích của `_ensure_nlm_installed`, `cmd_gws_bootstrap_cowork` (binary), `_persist_local_bin_on_path`, tải media,
  tệp tạm upload, `gop_settings`/`dat_env_file` của `ops/cloud_agent_creds.py` (§0.1).
- Không chặn LẦN ĐỌC config của `load_creds` (§0.4): đọc qua liên kết không ghi gì vào kho, và chặn nó làm hỏng đường lấy
  `TL_TOKEN` từ config mà `cmd_bootstrap` cần để tải bundle qua webapp. Lời hứa của M3 chỉ áp cho lần đọc PHỤC VỤ MERGE W6.
- Không chặn junction/reparse point trên Windows: `_kiem_dich_ghi` ở packet này chỉ dùng `S_ISLNK`. Vế reparse do packet
  `GWS-CRED-DICH-NGOAI-KHO` thêm vào thân hàm, kèm ca giả lập và junction thật. Trước khi packet ấy land, một junction ở
  `~/.notebooklm-mcp-cli` hay thành phần dưới nó KHÔNG bị chặn trên Windows (luật (a) kho vẫn áp qua `realpath`).
- Không đổi MÃ nhánh định dạng sẵn có cho jar rỗng/vắng (W1 `if not nlm:`, W3 `if not isinstance(nlm, dict) or not nlm:`, điều
  kiện truthy của W2): giữ nguyên base. Ca hồi quy `jar_rong_base` cho các nhánh ấy nằm ở packet `GWS-CRED-DICH-NGOAI-KHO` (N3d).
- Không kiểm DỮ LIỆU của W6 (chuyển 2026-11-18T06:53:23Z theo yêu cầu giữ trần): `token`/`webappUrl` encode được và không chứa NUL
  trước khi gán env, config cũ không phải `dict`, surrogate ở bước tuần tự hoá config. Ở packet này các trường hợp ấy giữ hành vi
  base (có thể ném `UnicodeEncodeError`/`ValueError`/`AttributeError` như base). Khác biệt duy nhất so với base: khi tuần tự hoá lỗi,
  ngoại lệ vẫn lan ra nhưng config cũ giữ nguyên byte (dữ liệu dựng xong mới gọi writer nguyên tử; base truncate rồi ghi dở — đo
  08:52:10Z, M3(3)). Mã, ca và đột biến của chúng là M7/N9w6 của packet
  `GWS-CRED-DICH-NGOAI-KHO`. Không mã nào của phần ấy land ở đây mà thiếu phép đo.
- Không đổi phía stage, `_NLM_AUTH_RELS`, `_nlm_bundle_guard`, chốt chống hạ cấp của `_nlm_auth_load`, THÂN `_trong_kho_git`/
  `_ghi_nguyen_tu_0600` (cổng PD của WP1334 canh); packet chỉ GỌI hai hàm ấy.
- Không sửa `ops/cloud_agent_creds*.py`, hook phiên, `.github/**`, `scripts/tl_selftest.py`, `RELEASE_MANIFEST.json`,
  `changelog.d/*`, `VERSION`, `CHANGELOG.md`, `SKILL.md`.
- Không chống đối thủ ĐỒNG THỜI cùng uid (đổi thư mục/tệp giữa lúc kiểm và lúc ghi). Chốt nhắm cấu hình tĩnh hoặc vô ý.
- Windows: không có CI Windows bắt buộc; quyền 0600 không đo bằng `stat` trên Windows.

## 3. `muc_tieu`

**Liên kết.** Ở packet này một đường là "liên kết" CHỈ khi `os.lstat(...)` cho `stat.S_ISLNK(st_mode)`. Packet này KHÔNG chặn
junction hay reparse point khác trên Windows và không hứa điều đó (§2); vế `FILE_ATTRIBUTE_REPARSE_POINT` cùng phép đo của nó
(giả lập + junction thật) thuộc packet `GWS-CRED-DICH-NGOAI-KHO`, để không có mã nào land mà thiếu phép đo (điều review lượt 3 đã bác).

**`goc`** — NLM: `os.path.expanduser("~/.notebooklm-mcp-cli")` (dựng bằng `join` nên không có hậu tố `/` hay `/.`); config:
chính tệp `os.path.expanduser("~/.tra_luat_config.json")`. HOME và mọi thành phần phía trên `goc` KHÔNG thuộc phần kiểm liên
kết (HOME là symlink là cấu hình hợp lệ); kho nằm sau symlink phía trên vẫn do hai chuỗi từ vựng/`realpath` của `_trong_kho_git` canh. HOME có thể mang thành phần đặc biệt (`/x/.`, `..`, tương đối — review lượt 3 đo trong RAM): chúng nằm PHÍA TRÊN `goc` và chỉ đi qua `_trong_kho_git`, không qua luật (b); packet này không chuẩn hoá HOME (khai thẳng).
Thành phần phía dưới `goc` chỉ đến từ khoá đã qua danh sách cho phép, nên không có `.`, `..`, rỗng.

| # | mục tiêu | tệp |
|---|---|---|
| M1 | `_kiem_dich_ghi(dich, goc, thanh_phan)` — `thanh_phan` là tuple thành phần từ `goc` xuống `dich` (rỗng khi `dich == goc`) — trả `None` (được ghi) hoặc lý do, KHÔNG tạo/ghi gì. Luật theo thứ tự: (a) `_trong_kho_git(os.path.dirname(dich)) is None`, sai ⇒ cụm `nằm trong kho git` + đường kho; (b) `goc` và mọi tiền tố `os.path.join(goc, *thanh_phan[:i])` tới `dich` (kể cả) — dựng từ thành phần, không `lstat` chuỗi do người dùng cấp — nếu ĐANG TỒN TẠI thì không phải liên kết; sai ⇒ `là liên kết tượng trưng` + tiền tố ấy. Tiền điều kiện (hợp đồng với packet `GWS-CRED-DICH-NGOAI-KHO`, gọi lại nguyên thân hàm): `goc` đã ở dạng `lstat` trực tiếp được (không hậu tố `/`, `/.`; chuẩn hoá là việc của caller), `dich == os.path.join(goc, *thanh_phan)`, mỗi phần tử là MỘT tên thành phần, caller ghi đúng `dich` đã kiểm. Hàm chỉ bỏ qua `FileNotFoundError`/`NotADirectoryError` (tiền tố chưa tồn tại); lỗi `lstat` khác thành lý do `ghi lỗi` của caller. Mã mới không chứa nguyên văn chuỗi neo PD nào (§0.4); bẫy: viết `if (kho := _trong_kho_git(os.path.dirname(dst))) is not None:` ở thụt lề 8 trùng neo PD1. | `scripts/tl_gws.py` |
| M2 | `_kiem_jar_nlm(nlm)` trả lý do hoặc `None`: `nlm` là `dict` khác rỗng, sai ⇒ `dữ liệu không hợp lệ`. Nhánh định dạng SẴN CÓ giữ nguyên và chạy TRƯỚC: W1 `if not nlm:` (1650–1653, `⚠ bundle chưa có nlm_auth`, rc 1) — `_kiem_jar_nlm` chỉ thấy jar truthy, nên `list`/chuỗi truthy ra `dữ liệu không hợp lệ`; W3 `if not isinstance(nlm, dict) or not nlm:` (1955–1956, `nlm_cred rỗng/sai định dạng.`) — mọi jar rỗng/sai kiểu dừng ở đó, `_kiem_jar_nlm` chỉ còn bắt khoá và giá trị; W2/M3(1) chỉ chạy khi `bundle.get("nlm_auth")` truthy (như điều kiện W2 của base), jar falsy coi như không có jar; mỗi khoá là `str` BẰNG NGUYÊN VĂN một phần tử `_NLM_AUTH_RELS` (so `in` trên tuple; không lọc `..`, không chuẩn hoá trước), sai ⇒ `ngoài danh sách cho phép` + `repr(khoá)` cắt ≤ 80 ký tự; mỗi giá trị là `str` và `encode("utf-8")` thành công (JSON giải mã được surrogate đơn), sai ⇒ `dữ liệu không hợp lệ`, không in giá trị. W1, W3: `_kiem_jar_nlm` rồi `_kiem_dich_ghi` cho TOÀN BỘ khoá TRƯỚC mọi `makedirs`/ghi; W2: kiểm jar DUY NHẤT ở M3(1), vòng ghi W2 chỉ `_kiem_dich_ghi`; một lý do ⇒ không ghi tệp nào. Ghi bằng `_ghi_nguyen_tu_0600(dst, giá_trị.encode("utf-8"))` thay `open("w")` + `chmod` (không ghi xuyên symlink/hardlink tệp cuối, §0.2 S3–S4). `OSError` ở tệp thứ i: dừng, tệp 1..i-1 đã được thay (nguyên tử từng tệp, KHÔNG cả lượt), không sót tệp tạm. | `scripts/tl_gws.py` |
| M3 | W6, theo thứ tự: (0) `degraded = False` dời lên TRƯỚC W6 (base khởi tạo ở 1725, sau W6). (1) NGAY sau giải mã bundle, mọi `env`, nếu `bundle.get("nlm_auth")` truthy thì `_kiem_jar_nlm`; có lý do ⇒ một dòng, `degraded = True`, lượt này không ghi jar (W2 bỏ qua, không in dòng thứ hai). (2) `_kiem_dich_ghi(cfgp, cfgp, ())` TRƯỚC lần đọc `existing` phục vụ merge; bị từ chối ⇒ token vẫn nạp `TL_TOKEN`/`TL_WEBAPP` như base, không đọc-để-merge, không ghi, một dòng, `degraded = True`. (3) Lần đọc phục vụ merge đi qua `open(` builtin. Được phép thì merge như base nhưng bỏ khoá `nlm_auth` khỏi phần merge khi (1) từ chối (giá trị đã có trong config giữ nguyên); rồi `_ghi_nguyen_tu_0600(cfgp, json.dumps(existing, ensure_ascii=False).encode("utf-8"))`. Kiểm DỮ LIỆU của W6 (token/`webappUrl` encode được và không NUL trước khi gán env; config cũ không phải `dict`; surrogate ở bước tuần tự hoá) KHÔNG thuộc packet này — giữ hành vi base (có thể ném như base; riêng lỗi tuần tự hoá: ngoại lệ vẫn lan ra như base, nhưng config cũ GIỮ NGUYÊN byte vì `json.dumps(...).encode("utf-8")` chạy TRƯỚC writer, khác base vốn mở `"w"` rồi ghi dở mới ném — đo 08:52:10Z: base để lại `'{"token": "moi", "rootFolderId": '`, thứ tự mới giữ `'{"token":"CU"}'`) — mà là M7 của packet `GWS-CRED-DICH-NGOAI-KHO` (§2). (4) `OSError` ⇒ M4; thông báo base `✓ token nạp env (ghi config lỗi: …)` (1720–1721) BỎ. | `scripts/tl_gws.py` |
| M4 | Hợp đồng lỗi cho W1, W2, W3, W6. Mỗi lần từ chối hoặc lỗi ghi in ĐÚNG MỘT dòng stderr: thẻ lệnh (`[nlm-auth-pull]`, `[bootstrap]`) rồi `✗`, TRƯỜNG PHÂN LOẠI (phần cố định ngay sau `✗ `, trước `: `) là đúng một trong năm cụm (phần chi tiết sau `: ` có thể chứa chuỗi trùng một cụm khác, ví dụ khoá lạ `'x là liên kết tượng trưng'` — không tính) `nằm trong kho git` · `là liên kết tượng trưng` · `ngoài danh sách cho phép` · `dữ liệu không hợp lệ` · `ghi lỗi` (kèm `_safe_exc(e)`), không chứa giá trị credential. Định dạng dòng CỐ ĐỊNH: `[<thẻ>] ✗ <cụm>: <chi tiết>` — cụm đứng NGAY sau `✗ ` và trước `: `; mọi đường và khoá nội suy vào `<chi tiết>` đi qua `repr(...)` (thoát `\n`, `\r`, ký tự điều khiển và dấu nháy, nên không bao giờ sinh dòng thứ hai), đường cắt ≤ 200, khoá cắt ≤ 80 ký tự sau `repr`. Loại lỗi nhận diện bằng `fullmatch` của PHẦN CỐ ĐỊNH đầu dòng, không bằng tìm chuỗi con (khoá lạ có thể chứa nguyên văn cụm khác). `_nlm_auth_load` trả `(False, <lý do>)` với lý do = `<cụm>: <chi tiết repr>` (đúng phần sau `✗ ` của định dạng dòng, một dòng), và chỉ biên CLI `cmd_nlm_auth_load` in ra stderr (một dòng `✗`), `cmd_nlm_auth_load` và `ops_misc` giữ nhánh lỗi sẵn có (một dòng `✗`, rc 2). Không ngoại lệ thoát ra TRONG PHẠM VI LỖI packet này xử lý: từ chối của `_kiem_jar_nlm`/`_kiem_dich_ghi`, và `OSError` ở lời ghi W1–W3, W6 (vòng ghi chỉ bắt `OSError`; kiểu và encode của jar kiểm TRƯỚC ở `_kiem_jar_nlm`). Lỗi DỮ LIỆU của W6 (token/`webappUrl`, config không phải `dict`, surrogate khi tuần tự hoá) ngoài phạm vi, giữ hành vi base (§2). Mã thoát: `cmd_nlm_auth_pull` 1; `cmd_bootstrap` đặt `degraded = True` (KỂ CẢ `OSError` ở W6 — đổi có chủ ý so với base), chạy tới đúng một dòng `agent_creds:`, trả 1 — trừ `--require-agent-creds` với agent chưa `ĐÃ NẠP` thì 4 như base (dòng từ chối vẫn in). W3: kiểm NGAY sau giải mã/kiểm định dạng sẵn có, TRƯỚC chốt chống hạ cấp. Hai dòng thông báo thành công mà `wp727_tl_gws_refresh` khoá (§0.4) giữ nguyên văn. | `scripts/tl_gws.py` |
| M5 | Fragment `scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py`, `TEST_ID = "wp433_nlm_gws_dich_ngoai_kho"`, `run(tl_module)`. Ca và đột biến viết dạng BẢNG (một dòng mỗi đột biến: tên, neo, thay thế, ca đích, nhãn đích) để giữ trần. **Rig**: HOME, `USERPROFILE`, `CODEX_HOME`, `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` (luôn ngoài mọi kho), `TL_*`, cwd đặt tạm, khôi phục trong `finally`; trên module thay `AGENT_CREDS_FILEID`/`TL_AGENT_CREDS_FILEID` (§0.2 S6), `_public_curl_bytes`, `_gas`, `_secrets_fetch`, `load_creds`, `_ensure_nlm_installed`, `cmd_gws_bootstrap_cowork`, `_imp("gws_bridge").gws_exe` bằng đồ giả có ĐẾM lời gọi; lớp chặn `subprocess.run`/`Popen`/`urllib.request.urlopen` (dấu `MANG_BI_CHAN`) chỉ cài TRONG cửa sổ gọi hàm `tl_gws`; `git init`/`git status` của fixture chạy ngoài cửa sổ, argv cố định. stdout/stderr bắt RIÊNG. Giá trị credential là `SENTINEL-wp433-…`. Kho tạm = thư mục có `.git` (`git init`, không có `git` thì `mkdir .git`). Fragment in mọi thứ ra STDERR (driver `bundle_fragment_check.py` đọc stdout làm JSON). **Đột biến** áp lên bản sao TRONG BỘ NHỚ của nguồn `tl_gws.py` (`compile`+`exec` vào namespace mới rồi `bind`), không ghi tệp; neo có ngữ cảnh riêng từng chỗ gọi, khớp ĐÚNG MỘT lần, `compile`/`bind` thành công — sai ⇒ `HONG`. **Phân hạng**: ca thu TẬP nhãn hậu điều hỏng, ném `TinHieuChotCa(AssertionError)` mang (tên ca, tập nhãn); đột biến chỉ tính GIẾT khi đúng lớp, đúng ca, nhãn đích thuộc tập. **Ngoại lệ dự kiến**: hậu điều "không ngoại lệ" được đo bằng cách bắt ở BIÊN của TỪNG LƯỢT GỌI một TẬP ĐÓNG (loại, dấu thông điệp) khai cho đúng lượt ấy, rồi đổi thành nhãn hỏng của (ca, lượt); ngoại lệ ngoài tập của lượt đang chạy ⇒ ca dừng với nhãn `ngoai_le_la` (không bao giờ là nhãn đích) — luật đầy đủ ở §4b; giữ đúng tự kiểm N10(c). Tập khai của MỖI LƯỢT = cột "ngoại lệ khai" của các dòng E ghi lượt ấy trong bảng §4b (nguồn duy nhất; lượt không có dòng E thì tập khai rỗng). | fragment |
| M6 | Điều kiện "bootstrap không tạo `~/.claude`" là ca `d5_khong_claude` trong fragment (thay cho sửa `_xem` của `r973_bootstrap_khong_export_khong_ghi_gemini`): bundle agent giả có `codex_auth`, `claude_oauth_token`, `antigravity_api_key`; `cmd_bootstrap --env chat` thật với `_public_curl_bytes` giả; nhãn `codex_da_nap` (trạng thái `ĐÃ NẠP`, `CODEX_HOME/auth.json` là tệp), `khong_claude`, cùng không `HOME/.gemini`, không `CLAUDE_CODE_OAUTH_TOKEN`/`GEMINI_API_KEY`. | fragment |
| M7 | Tái sinh `scripts/tl_test_fragments_bundled.py` bằng `generate_bundled_module_bytes(scripts/test_fragments)`; không sửa tay; không đụng `RELEASE_MANIFEST.json`. | bundled |

## 4. `nghiem_thu`

Ký hiệu: K = thư mục có `.git`; SENT = `SENTINEL-wp433-…`; "sạch(K)" = không tệp/thư mục mới dưới K ngoài `.git` và nội dung
tệp có sẵn không đổi, VÀ khi có `git`, `git -C K status --porcelain --untracked-files=all` rỗng. "stderr đúng" = số dòng stderr
(bỏ dòng rỗng) bằng số dự kiến, mỗi dòng `fullmatch` một mẫu trong danh sách đóng của ca (thẻ + `✗` + cụm M4 + phần đường/khoá),
stdout không chứa SENT. "Fixture bootstrap chuẩn" = `cmd_bootstrap --env code --no-nlm --no-gws`, bundle có `token` và `gws_cred`
hợp lệ (`GOOGLE_WORKSPACE_CLI_CONFIG_DIR` ngoài kho), agent giả `KHÔNG CẤU HÌNH`, `gws_exe` giả trả có; với HOME ngoài mọi kho
và `nlm_auth` hợp lệ (nếu có) nó trả rc 0. Nhãn hậu điều trong ngoặc vuông. Mã LƯỢT GỌI (§4b): `N<k>.<vế>` theo số vế trong ô; vế gọi nhiều lệnh thêm hậu tố lệnh (`-W1`, `-W2`, `-W6`); N2 đánh `N2.0`…`N2.3` theo thứ tự khoá; N8(1) sinh sáu lượt `N8.1-<W1|W2>-<kho|lien_ket|danh_sach>`; ca khoá lạ một thành phần có `N1k-W1`/`-W2`/`-W3`; vế khoá mang cụm của N8(2b) là `N8.2b-khoa`.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | `w1_pull_rel_thoat`, `w2_bootstrap_rel_thoat`, `w3_load_rel_thoat`: `nlm_auth = {"auth.json": <hợp lệ>, "../thoat.json": SENT}` ⇒ [`khong_thoat`] không `thoat.json` nào trong thư mục tạm; [`khong_jar`] NLM root không có tệp; [`ma`] W1 rc 1, W3 `ok is False`; [`stderr`] W1, W2: stderr đúng một dòng `ngoài danh sách cho phép`; W3 (trả tuple, không in): [`ly_do`] lý do trả về là MỘT dòng (không `\n`) và `fullmatch` `ngoài danh sách cho phép: .*` — W3 không đòi stderr. W2 dùng fixture bootstrap chuẩn, config có sẵn mang `nlm_auth = {"auth.json": "CU-wp433"}`: [`token_env`] `TL_TOKEN` đặt; [`config_khong_nlm`] config giữ đúng `nlm_auth` cũ và có `token` mới; [`ma`] rc 1, một dòng `agent_creds:`. Ca khoá lạ của W2 chỉ đo chốt dữ liệu CHUNG (M3(1)) và việc W6 không lưu jar sai — W2 không chạy ở ca ấy. Ca riêng W2 `w2_jar_hop_le_dich_bi_chan`: fixture bootstrap chuẩn, HOME ngoài kho, jar HỢP LỆ, `~/.notebooklm-mcp-cli` là symlink tới T ngoài kho ⇒ [`khong_ra_ngoai`] T rỗng; [`ma`] rc 1; [`stderr`] một dòng `là liên kết tượng trưng`; config vẫn được ghi. Ca riêng W3 `w3_jar_hop_le_dich_bi_chan`: `_nlm_auth_load` với jar HỢP LỆ (ba khoá), `~/.notebooklm-mcp-cli` là symlink tới T ngoài kho ⇒ [`khong_ra_ngoai`] T rỗng; [`ma`] `ok is False`, lý do một dòng `fullmatch` `là liên kết tượng trưng: .*` (không đòi stderr). | Ca `chung_khoa_la_mot_thanh_phan`, ba lượt `N1k-W1`/`N1k-W2`/`N1k-W3` (W2 qua fixture bootstrap chuẩn): jar = `{"auth.json": <hợp lệ>, "khac.json": SENT}` — khoá MỘT thành phần ngoài allowlist, nên khi kiểm jar bị bỏ, `_kiem_dich_ghi` vẫn được gọi đúng tiền điều kiện M1 ⇒ [`khong_khoa_la`] không tệp `khac.json` dưới NLM root, W1/W2 rc 1 với stderr đúng một dòng `ngoài danh sách cho phép`; lượt `N1k-W3`: `ok is False`, lý do một dòng `fullmatch` `ngoài danh sách cho phép: .*`, không đòi stderr. `db_w1_bo_kiem_jar`, `db_w2_bo_kiem_jar`, `db_w3_bo_kiem_jar` (bỏ lời gọi `_kiem_jar_nlm` ở đúng một caller, giữ kiểm đích + writer) ⇒ lượt của caller ấy, nhãn `khong_khoa_la`. Ca `*_rel_thoat` đo hậu điều chung, không mang đột biến riêng. `db_w3_bo_kiem_dich` (W3 chỉ bỏ `_kiem_dich_ghi`) ⇒ `w3_jar_hop_le_dich_bi_chan`, `khong_ra_ngoai`; `db_w1_bo_kiem_dich` ⇒ N6(3) (§4b dòng 5). `db_w2_bo_kiem_dich` (W2 chỉ bỏ `_kiem_dich_ghi`, giữ writer) ⇒ `w2_jar_hop_le_dich_bi_chan`, nhãn `khong_ra_ngoai`. `db_w6_luu_nlm_bi_tu_choi` ⇒ `w2_bootstrap_rel_thoat`, nhãn `config_khong_nlm`. Vế âm base: §0.2 A–C. |
| N2 | `chung_allowlist`: W1, từng khoá `"profiles/default/khac.json"`, `"./auth.json"`, `"profiles\\default\\cookies.json"`, `"/tmp/x.json"` ⇒ [`tu_choi_<i>`] bị từ chối, không tệp nào; [`du_ba`] đúng ba khoá `_NLM_AUTH_RELS` ⇒ ghi đủ, đúng byte UTF-8, 0600 (bỏ vế quyền trên Windows). | `db_blocklist` ("từ chối khi có `..`") ⇒ `tu_choi_0`. `db_chuan_hoa_truoc` (so `normpath(rel)`) ⇒ `tu_choi_1`. Vế âm base: §0.2 D. |
| N3 | `chung_du_lieu_sai_dang`: (1) `nlm_auth` là `[1]` (list khác rỗng) ở W1 và W2 (fixture chuẩn) ⇒ [`kieu_jar`] W1 rc 1, W2 rc 1 + một `agent_creds:`, mỗi lệnh một dòng `dữ liệu không hợp lệ`, không ngoại lệ, không tệp jar; (2) giá trị kiểu số ⇒ [`kieu_gia_tri`] như trên; (3) bundle mang `"auth.json": "\ud800"` (chuỗi thoát JSON dựng trong bytes rồi mã hoá bằng `gws_cred_store`) ⇒ [`surrogate_jar`] W1 rc 1, `dữ liệu không hợp lệ`, không tệp jar, không tệp tạm. Vế (4)–(7) cũ (token/`webappUrl`, tuần tự hoá, config không phải `dict`, NUL) CHUYỂN sang packet `GWS-CRED-DICH-NGOAI-KHO` cùng mã của chúng. Ca (8) `jar_rong_base` (nhánh định dạng sẵn có của W1/W2/W3) CHUYỂN sang packet `GWS-CRED-DICH-NGOAI-KHO` để giữ trần | `db_bo_kiem_kieu_jar` ⇒ `kieu_jar`. `db_bo_kiem_encode` ⇒ `surrogate_jar`.  |
| N4 | `chung_kiem_truoc_ghi`: HOME = K/home, W1 ba khoá hợp lệ ⇒ [`ma`] rc 1; [`khong_tao_thu_muc`] `K/home/.notebooklm-mcp-cli` không tồn tại; [`sach`] sạch(K). Vế dương: HOME ngoài kho ⇒ rc 0, ba tệp. | `db_makedirs_truoc` ⇒ `khong_tao_thu_muc`. `db_bo_kho` (bỏ luật (a)) ⇒ `sach`. |
| N5 | Hai chuỗi của `_trong_kho_git` (symlink NGOÀI kho trỏ vào kho; symlink TRONG kho trỏ ra ngoài) và hai đột biến `db_chi_tu_vung`/`db_chi_realpath` CHUYỂN sang packet `GWS-CRED-DICH-NGOAI-KHO` (đi qua cùng `_kiem_dich_ghi`) để giữ trần. Ở packet này luật (a) có răng qua `db_bo_kho` (N4) và các ca HOME trong kho; hàm `_trong_kho_git` có PD7/PD8 canh. | — (khai thẳng: không có phép đỏ riêng cho hai chuỗi ở packet này) |
| N6 | Liên kết ở đích: (1) `w1_la_symlink` — ca TỐI THIỂU cho LÁ jar (review lượt 5: (2) chỉ phủ `dich == goc`, (3) chỉ thư mục trung gian, và ghi nguyên tử có thể thay symlink bằng tệp thường rồi báo thành công): HOME ngoài kho, `~/.notebooklm-mcp-cli/profiles/default/cookies.json` là symlink tới `T/dich.json` (`CU`), W1 với ba khoá hợp lệ ⇒ [`la_tu_choi`] rc 1, đúng một dòng `là liên kết tượng trưng`, `os.path.islink` của lá vẫn đúng, `T/dich.json` giữ byte, không tệp jar nào mới. Đột biến đầy đủ của lớp này (`db_bo_symlink_cuoi`) ở packet `GWS-CRED-DICH-NGOAI-KHO`; (2) `w6_symlink_config`: `~/.tra_luat_config.json` symlink vào K ⇒ fixture chuẩn rc 1, tệp đích giữ byte, [`stderr`]; với `load_creds` giả, bộ quan sát bọc `builtins.open`, `io.open`, `pathlib.Path.read_text`/`read_bytes` ghi lại mọi lần mở `cfgp` trong cửa sổ gọi ⇒ [`khong_doc_merge`] 0 lần; (3) `chung_symlink_thu_muc` (S2): `profiles/default` symlink ra T ⇒ W1 rc 1, [`khong_ra_ngoai`] T rỗng, [`khong_jar`]; (4) `chung_hardlink` (S3): `auth.json` hardlink của H (`CU`) ⇒ rc 0, [`ban_kia_giu`] H còn `CU`.  | `db_w6_bo_symlink` (chỉ bỏ kiểm symlink ở LÁ config của W6, giữ nguyên đầu vào luật (a); §4b dòng 14) ⇒ (2) `stderr`: fixture N6(2) — HOME ngoài kho, lá config là symlink vào K — luật (a) qua, lá không bị kiểm, writer thay symlink bằng tệp thường, rc 0, không dòng từ chối ⇒ đỏ đúng nhãn `stderr`. `db_w6_doc_truoc_chot` (đọc `existing` rồi mới kiểm) ⇒ (2) `khong_doc_merge`. `db_bo_tien_to_cuoi` (vòng tiền tố của luật (b) dừng trước tiền tố cuối) ⇒ (1) `la_tu_choi`. `db_bo_symlink_thanh_phan` ⇒ (3) `khong_ra_ngoai`. `db_w1_khong_nguyen_tu` (W1 về `open("w")`) ⇒ (4) `ban_kia_giu`. |
| N7 | W6, fixture chuẩn, KHÔNG `nlm_auth`: `w6_chi_config_trong_kho` — HOME = K/home (CODEX_HOME ngoài) ⇒ [`ma`] rc 1; [`sach`]; [`token_env`]; [`stdout`] một `agent_creds:`; [`stderr`] đúng MỘT dòng `nằm trong kho git`. `w6_chi_config_ngoai_kho` — HOME ngoài kho ⇒ [`duong`] rc 0, config ghi, stderr rỗng. `w6_tich_hop` — thêm `nlm_auth` hợp lệ, HOME = K/home ⇒ rc 1, sạch(K), HAI dòng `nằm trong kho git`. Vế âm base: §0.2 F. | `db_w6_bo_chot` (bỏ lời gọi `_kiem_dich_ghi` ở W6) ⇒ `w6_chi_config_trong_kho`, `sach`. `db_quen_degraded`, `db_degraded_khoi_tao_muon` ⇒ `w6_chi_config_trong_kho`, `ma` (không còn W2 nào đặt cờ thay). |
| N8 | `chung_hop_dong_loi`: (1) mỗi lý do kho/liên kết/danh sách ở W1 và W2 ⇒ [`stderr`], [`khong_nem`], [`agent_creds`] một dòng; (2) [`require`] chạy lại fixture của `w2_jar_hop_le_dich_bi_chan` kèm `--require-agent-creds` (một dòng trong bảng ca, agent `KHÔNG CẤU HÌNH`) ⇒ rc 4, stderr đúng HAI dòng (từ chối W2 `là liên kết tượng trưng` + `[bootstrap] ✗ --require-agent-creds …` của base), stdout đúng một dòng `agent_creds:`; (2b) [`mot_dong`] ký tự xuống dòng nằm trong CHÍNH đường được in: chi tiết của lý do kho là đường KHO do `_trong_kho_git` trả về, không phải đường đích, nên kho là thư mục `k\nho` (có `.git`) và HOME = `k\nho/home` ⇒ W1 rc 1, stderr ĐÚNG một dòng, `fullmatch` `\[nlm-auth-pull\] ✗ nằm trong kho git: .*`, và phần chi tiết bằng `repr(<đường kho>)` (đo 06:33:10Z trong thư mục tạm thật, `python3 -I` trên bản sao base: thư mục kho tên `k\nho` tạo được, `_trong_kho_git` trả đường kho CHỨA `\n`, dòng dựng không `repr` tách thành 2 dòng, có `repr` 1 dòng); Điều kiện nền: POSIX dựng kho THẬT `k\nho`; Windows không dựng được tên ấy (review lượt 7: `ntpath.isreserved('k\nho')` đúng) nên trong cửa sổ gọi thay `_trong_kho_git` trên module bằng đồ giả trả đường kho THẬT của ca nối thêm `\nx` cho đúng đường đích của ca (đường khác đi hàm thật), với CÙNG hậu điều. Ca chạy trên MỌI nền, không vào `bỏ_qua` hay `chỉ_windows`. [`cum_trong_khoa`] khoá lạ `"x là liên kết tượng trưng"` ⇒ một dòng, phần cố định nhận diện là `ngoài danh sách cho phép`, không phải `là liên kết tượng trưng`; (3) [`thu_tu_w3`] W3, khoá lạ + `_nlm_auth_load_downgrade` giả báo cũ hơn ⇒ lý do `ngoài danh sách cho phép`, không `HẠ CẤP`; (4) `os.replace` giả ném `OSError` CHỈ khi ĐÍCH thoả điều kiện đường: [`oserror_w1`] đích `profiles/default/cookies.json` ⇒ rc 1, một dòng `ghi lỗi`, không `.auth.json.*` sót, `auth.json` mới, hai tệp kia không tồn tại; [`oserror_w2`] đích dưới NLM root, fixture chuẩn + `nlm_auth` hợp lệ ⇒ rc 1, một `ghi lỗi`, một `agent_creds:`, config vẫn ghi; [`oserror_w6`] đích = config ⇒ rc 1, một dòng `[bootstrap] ✗ … ghi lỗi`, không dòng `✓ token nạp env (ghi config lỗi`, `TL_TOKEN` đặt, config cũ giữ byte. Thêm: `python3 ops/cloud_agent_creds_test.py` trên head `TONG: DAT`, `PD*` vẫn `GIET`, từng ca bằng base (§0.5). | `db_nem_thay_vi_tu_choi` (từ chối bằng `raise ValueError("wp433-nem")`) ⇒ `khong_nem` (bắt ở biên theo tập khai ở M5). `db_in_hai_dong` (thêm dòng stderr KHÔNG chứa cụm) ⇒ `stderr`. `db_oserror_lan` ⇒ `oserror_w1`. `db_w6_oserror_kieu_cu` ⇒ `oserror_w6`. `db_kiem_sau_ha_cap` ⇒ `thu_tu_w3`. `db_khong_repr` (nội suy đường thô, không `repr`) ⇒ `mot_dong`. `db_cum_cuoi_dong` (đưa cụm ra sau phần chi tiết) ⇒ `cum_trong_khoa`. `db_require_thua_rc1` (trả 1 trước nhánh `--require-agent-creds`) ⇒ `require`. Neo PD lặp ⇒ `cloud_agent_creds_test` báo `HONG`. |
| N9 | M6: `d5_khong_claude` ĐẠT trên head (base đã không tạo `.claude`, §0.2 G — răng từ đột biến). | `db_tao_claude`: chèn `os.makedirs(os.path.expanduser("~/.claude"), exist_ok=True)` ngay trước `    co = [k for k in ("claude_oauth_token", "antigravity_api_key") if p.get(k)]` (khớp 1 lần ở base) ⇒ nhãn `khong_claude`, nhãn `codex_da_nap` KHÔNG hỏng. |
| N10 | Tự kiểm. (a) Mỗi đột biến GIẾT đúng (ca, nhãn); mỗi chỗ ghi W1, W2, W3, W6 có ca đích riêng. (b) MỘT dòng tổng kết RA STDERR `[wp433_nlm_gws_dich_ngoai_kho] CA: dự_kiến=a chạy=b đạt=c bỏ_qua=d · DOT BIEN: dự_kiến=e chạy=f giết_đúng=g bỏ_qua=h · HONG: i`; `run` trả `True` chỉ khi `b == c`, `f == g`, `i == 0`, `a == b + d`, `e == f + h`. Ca/đột biến phụ thuộc symlink/hardlink bỏ qua CÙNG NHAU kèm lý do, chỉ khi không tạo được liên kết; trên POSIX `d == h == 0`. Ca `mot_dong` (N8(2b)) chạy trên mọi nền (Windows dùng giả lập `_trong_kho_git`) nên không bao giờ vào `bỏ_qua`. (c) Đột biến tự kiểm của bộ phân hạng (khuôn `TU_KIEM` của `ops/cloud_agent_creds_test.py`): chết vì `AttributeError` qua một `except` đổi kiểu ⇒ TÍN DỤNG GIẢ; chỉ thêm chú thích ⇒ SỐNG SÓT. (d) Neo khớp 0/2 lần hoặc không `compile` ⇒ `HONG`. (e) stdout của `run` rỗng. | Trên cây tạm: (1) đổi lượt đích của `db_w3_bo_kiem_jar` sang `N1k-W1` ⇒ `run` False. (2) TẮT nhãn `khong_khoa_la` của lượt `N1k-W1` ⇒ `db_w1_bo_kiem_jar` không giết đúng nhãn ⇒ False. (3) Neo khớp 2 lần ⇒ `HONG: 1`, False. (4) Ép bỏ qua một ca symlink trên POSIX ⇒ False. (5) In tổng kết ra stdout ⇒ (e) đỏ và `bundle_fragment_check.py` trên cây tạm `ok: false`. (7) Đối chứng cho §4b dòng 14 (đo phụ trên cây tạm, ghi kết quả): dưới `db_w6_bo_symlink`, `w6_chi_config_trong_kho` (HOME = `K/home`) và cùng fixture với HOME = `K` (gốc kho) KHÔNG đổi màu — luật (a) trên `dirname(cfgp)` vẫn từ chối; chỉ `w6_symlink_config` đỏ. (6) `tu_kiem_sai_luot` (§4b): khai lượt đích của dòng 11 là `N3.1-W1` thay `N3.3` ⇒ ngoại lệ khớp loại + dấu nhưng ở lượt khác ⇒ không giết đúng ⇒ False. |
| N11 | Exact head: `python3 scripts/tl.py --selftest` ĐẠT N/N hai số bằng nhau trên clone thật, N = N_base + 1, DELTA so base = 0 ca đỏ mới (base và head dựng trong CÙNG một lệnh). `python3 scripts/tl.py test-fragments-check --json` ⇒ `ok: true`. `python3 .github/checks/bundle_fragment_check.py --json` ⇒ `ok: true`, `failed: []` (cũng là bước CI `bundled-fragment check` trên PR, §0.4). | Không tái sinh bundled ⇒ `TEST_ID_SET_MISMATCH` (đo §0.4). Sửa tay bundled ⇒ `GENERATED_BUNDLE_STALE`. Fragment đọc tệp ngoài gói ⇒ `BUNDLED_FRAGMENT_FAILED`. |
| N12 | Lane worker `ci.yml` 521–532 tại chỗ: `release-manifest --root . --out <tạm ngoài repo>` rồi `release-verify <tạm> --root . --strict` ⇒ `ok: true`, `expected_file_count == checked_file_count` (= 185). `RELEASE_MANIFEST.json` committed LỆCH bundled trên PR head (đo §0.4: rc 2) — lane LAND chỉ chạy trên master, nên phiên land PHẢI tái sinh manifest trong commit land trước khi master nhận diff; hồ sơ land ghi `release-verify RELEASE_MANIFEST.json --strict` `ok: true` trên commit land. | Sửa tay một tệp trong gói sau khi sinh manifest tạm ⇒ `ok: false`. |
| N13 | Exact head, lệnh + rc + bằng chứng dương: `ruff check --select F` delta = 0 trên `scripts/tl_gws.py` (nền §0.4), 0 trên fragment và bundled; `git diff --check` sạch; `doctrine-scan`, `adr-song` rc 0; dưới `set -o pipefail`: `git diff --numstat <base>..<head> > numstat.txt` (rc ≠ 0 ⇒ đỏ), rồi (i) đúng 3 dòng, (ii) mỗi dòng khớp `^[0-9]+\t[0-9]+\t<đường>$` và tập đường == §1, (iii) tổng cột thêm ≤ 450. | Tên chưa định nghĩa ⇒ delta ≠ 0. Tệp ngoài §1 ⇒ (i)/(ii). Trần: cùng lệnh trên `numstat.txt` dựng tay đúng 3 dòng, đúng tập đường §1, cột thêm tổng 450 ⇒ (iii) XANH; đổi một cột cho tổng 451 ⇒ (iii) ĐỎ (cô lập điều kiện tổng khỏi (i)/(ii)). `<base>` không tồn tại ⇒ rc 128 ⇒ đỏ, không phải tổng 0. Đầu vào rỗng ⇒ (i). Dòng `-\t-\t…` ⇒ (ii). `doctrine-scan`/`adr-song`: gate kế thừa, chưa có phép đỏ riêng ở packet này (L3). |


### 4b. Bảng đột biến — NGUỒN DUY NHẤT (thắng mọi mô tả đột biến rải trong §4)

**Lượt gọi.** Mỗi ca gồm một hay nhiều LƯỢT GỌI (một lời gọi hàm `tl_gws` với fixture riêng), mang mã lượt ghi ở cột "lượt" (vd
`N3.4` là vế (4) của N3; `—` = ca chỉ có một lượt). Nhãn hậu điều thuộc về (ca, lượt). Tập ngoại lệ khai gắn với TỪNG LƯỢT, không
với ca: bộ bắt ở biên của lượt L chỉ đổi thành nhãn những ngoại lệ khớp (loại + dấu thông điệp) của chính các dòng E có lượt L.
Ngoại lệ ngoài tập khai của lượt đang chạy ⇒ ca DỪNG và ném `TinHieuChotCa(tên ca, nhãn đã thu ∪ {"ngoai_le_la"})`; `ngoai_le_la`
không bao giờ là nhãn đích, nên đột biến chết kiểu ấy chỉ được tín dụng nếu nhãn đích đã được thu ĐÚNG lượt trước đó. Đột biến
khai (ca, lượt, nhãn) và chỉ GIẾT khi tín hiệu mang đúng bộ ba ấy (`TinHieuChotCa` mang tập (lượt, nhãn)).

Cơ chế chết: **H** = hậu điều đổi màu, không ngoại lệ; **E** = ngoại lệ lan ra khỏi lời gọi, bắt ở biên của đúng lượt theo cột
khai. Cột "tự kiểm": phép đo đã chạy cho phép toán nguyên tố quyết định cơ chế (06:42:22Z, `python3 -I`, Python 3.13.18, thư mục
tạm thật; chưa có mã) hoặc "lập luận" (mã base + hợp đồng M1–M4).

Ràng buộc cài đặt để cơ chế tất định: `_kiem_jar_nlm` và vòng ghi W1–W3 duyệt bằng `nlm.items()`; kiểm kiểu/encode của jar làm
TRƯỚC khi ghi; vòng ghi W1–W3 và W6 chỉ bắt `OSError`; đồ giả `os.replace` ném
`OSError("wp433-oserror")`; đột biến tự kiểm N10(c) ném `AttributeError("wp433-tu-kiem")`, nhắm `w1_pull_rel_thoat` (không lượt nào
khai dấu ấy). Fixture N3.1 là `nlm_auth = [1]` (khác rỗng, nên qua nhánh
`if not nlm` của base và tới `_kiem_jar_nlm`).

| # | đột biến | ca đích | lượt | nhãn | cơ chế | ngoại lệ khai ở biên lượt (loại + dấu) | tự kiểm |
|---|---|---|---|---|---|---|---|
| 1 | `db_w1_bo_kiem_jar` (W1 bỏ lời gọi `_kiem_jar_nlm`, GIỮ `_kiem_dich_ghi` và writer nguyên tử) | `chung_khoa_la_mot_thanh_phan` | `N1k-W1` | `khong_khoa_la` | H — `khac.json` được ghi | — | lập luận |
| 2 | `db_w3_bo_kiem_jar` (W3 bỏ lời gọi `_kiem_jar_nlm`, giữ kiểm đích + writer) | `chung_khoa_la_mot_thanh_phan` | `N1k-W3` | `khong_khoa_la` | H | — | lập luận |
| 3 | `db_w2_bo_kiem_jar` (bỏ lời gọi `_kiem_jar_nlm` của W2 ở M3(1) — chỗ kiểm jar DUY NHẤT của W2; vòng ghi W2 giữ kiểm đích + writer) | `chung_khoa_la_mot_thanh_phan` | `N1k-W2` | `khong_khoa_la` | H | — | lập luận |
| 4 | `db_w2_bo_kiem_dich` (W2 bỏ lời gọi `_kiem_dich_ghi`; GIỮ kiểm jar M3(1), writer nguyên tử và xử lý `OSError`) | `w2_jar_hop_le_dich_bi_chan` | — | `khong_ra_ngoai` | H | — | lập luận (§0.2 S2) |
| 5 | `db_w1_bo_kiem_dich` (W1 gọi `_kiem_jar_nlm`, bỏ `_kiem_dich_ghi`) | `chung_symlink_thu_muc` | — | `khong_ra_ngoai` | H | — | lập luận (§0.2 S5) |
| 6 | `db_w3_bo_kiem_dich` (W3 gọi `_kiem_jar_nlm`, bỏ `_kiem_dich_ghi`) | `w3_jar_hop_le_dich_bi_chan` | — | `khong_ra_ngoai` | H | — | lập luận (§0.2 S5) |
| 7 | `db_w6_luu_nlm_bi_tu_choi` | `w2_bootstrap_rel_thoat` | — | `config_khong_nlm` | H | — | lập luận |
| 8 | `db_blocklist` | `chung_allowlist` | `N2.0` | `tu_choi_0` | H | — | lập luận (§0.2 D) |
| 9 | `db_chuan_hoa_truoc` | `chung_allowlist` | `N2.1` | `tu_choi_1` | H | — | lập luận |
| 10 | `db_bo_kiem_kieu_jar` | `chung_du_lieu_sai_dang` | `N3.1-W1` | `kieu_jar` | E | `N3.1-W1` và `N3.1-W2`: `AttributeError` chứa `'list' object has no attribute 'items'` | đo: `[[…]].items()` ⇒ đúng thông điệp (cùng thông điệp với `[1]`) |
| 11 | `db_bo_kiem_encode` | `chung_du_lieu_sai_dang` | `N3.3` | `surrogate_jar` | E — `encode` trong vòng ghi | `N3.3`: `UnicodeEncodeError` chứa `surrogates not allowed` | đo: đúng thông điệp |
| 12 | `db_makedirs_truoc` | `chung_kiem_truoc_ghi` | — | `khong_tao_thu_muc` | H | — | lập luận |
| 13 | `db_bo_kho` | `chung_kiem_truoc_ghi` | — | `sach` | H | — | lập luận (§0.2 F) |
| 14 | `db_w6_bo_symlink` (W6 thay lời gọi `_kiem_dich_ghi(cfgp, cfgp, ())` bằng phép kiểm CHỈ luật (a) trên CÙNG đầu vào `os.path.dirname(cfgp)` — `_trong_kho_git(os.path.dirname(cfgp))` khác `None` ⇒ từ chối `nằm trong kho git` như cũ (viết với tên biến KHÁC neo PD1) — tức chỉ bỏ luật (b), mà ở W6 (`thanh_phan` rỗng, `dich == goc`) luật (b) chỉ kiểm đúng LÁ config; giữ writer, merge, xử lý `OSError`) | `w6_symlink_config` | — | `stderr` | H | — | lập luận (§0.2 S4) |
| 15 | `db_w6_doc_truoc_chot` | `w6_symlink_config` | — | `khong_doc_merge` | H | — | lập luận |
| 16 | `db_bo_tien_to_cuoi` | `w1_la_symlink` | — | `la_tu_choi` | H | — | lập luận (§0.2 S4) |
| 17 | `db_bo_symlink_thanh_phan` | `chung_symlink_thu_muc` | — | `khong_ra_ngoai` | H | — | lập luận (§0.2 S5) |
| 18 | `db_w1_khong_nguyen_tu` (CHỈ writer W1 về `open("w")` + `chmod`; giữ mọi phép kiểm) | `chung_hardlink` | — | `ban_kia_giu` | H | — | lập luận (§0.2 S3) |
| 19 | `db_w6_bo_chot` (W6 bỏ lời gọi `_kiem_dich_ghi`; giữ writer, merge, xử lý `OSError`) | `w6_chi_config_trong_kho` | — | `sach` | H | — | lập luận |
| 20 | `db_quen_degraded` | `w6_chi_config_trong_kho` | — | `ma` | H | — | lập luận |
| 21 | `db_degraded_khoi_tao_muon` | `w6_chi_config_trong_kho` | — | `ma` | H | — | lập luận |
| 22 | `db_nem_thay_vi_tu_choi` | `chung_hop_dong_loi` | `N8.1-W1-kho` | `khong_nem` | E | mọi lượt `N8.1-*` (ba lý do × W1, W2): `ValueError` chứa `wp433-nem` | lập luận (đột biến tự đặt dấu) |
| 23 | `db_in_hai_dong` | `chung_hop_dong_loi` | `N8.1-W1-kho` | `stderr` | H | — | lập luận |
| 24 | `db_oserror_lan` | `chung_hop_dong_loi` | `N8.4-W1` | `oserror_w1` | E | `N8.4-W1`: `OSError` chứa `wp433-oserror` | lập luận (rig tự đặt dấu) |
| 25 | `db_w6_oserror_kieu_cu` | `chung_hop_dong_loi` | `N8.4-W6` | `oserror_w6` | H | — | lập luận |
| 26 | `db_kiem_sau_ha_cap` | `chung_hop_dong_loi` | `N8.3` | `thu_tu_w3` | H | — | lập luận |
| 27 | `db_khong_repr` | `chung_hop_dong_loi` | `N8.2b` | `mot_dong` | H | — | đo 06:33:10Z: không `repr` ⇒ 2 dòng |
| 28 | `db_cum_cuoi_dong` | `chung_hop_dong_loi` | `N8.2b-khoa` | `cum_trong_khoa` | H | — | lập luận |
| 29 | `db_require_thua_rc1` | `chung_hop_dong_loi` | `N8.2` | `require` | H | — | lập luận |
| 30 | `db_tao_claude` | `d5_khong_claude` | — | `khong_claude` | H | — | lập luận (neo khớp 1 lần, 05:20Z) |

Rà cùng hình dạng (lượt 11 — mỗi đột biến chỉ đổi MỘT cơ chế): không còn dòng nào "quay về vòng ghi base"; kiểm đích ở W1/W2/W3/W6 là dòng 5/4/6/19 (bỏ đúng lời gọi `_kiem_dich_ghi`, giữ writer); writer nguyên tử chỉ đổi ở dòng 18 (W1, giữ mọi phép kiểm); xử lý `OSError` chỉ đổi ở dòng 24 (W1) và 25 (W6); liên kết của W6 chỉ bỏ luật (b) ở lá config, giữ nguyên đầu vào luật (a) (dòng 14), khác dòng 19 (bỏ cả lời gọi). Đột biến TRONG thân hàm chung (`db_bo_kho`, `db_bo_tien_to_cuoi`, `db_bo_symlink_thanh_phan`, `db_makedirs_truoc`, `db_bo_kiem_kieu_jar`, `db_bo_kiem_encode`) mỗi dòng đổi một luật. Rà cùng hình dạng (lượt 10): mỗi caller W1, W2, W3 có MỘT đột biến chỉ bỏ kiểm jar (dòng 1–3, khoá một thành phần `khac.json` ngoài allowlist để giữ tiền điều kiện M1 của `_kiem_dich_ghi`) và MỘT đột biến chỉ bỏ kiểm đích (W1: dòng 5; W2: dòng 4; W3: dòng 6); hai đột biến cũ quay về vòng ghi base (bỏ cả hai chốt) bị THAY vì đã được hai đột biến tách phủ. W6: kiểm jar dùng chung M3(1) với W2 (dòng 3 phủ), kiểm đích riêng (`db_w6_bo_chot`), liên kết riêng (`db_w6_bo_symlink`). Lượt 9: các dòng E còn lại — 10 (`N3.1-W1`/`-W2`),
11 (`N3.3`), 22 (`N8.1-*`), 24 (`N8.4-W1`) — mỗi dòng một (loại, dấu) riêng trong ca của nó; dòng 10 và 22 cùng dấu trên nhiều lượt
mà CÙNG nhãn đích, nên khai trên mọi lượt đột biến chạm tới. Đột biến gộp hai chốt ở một chỗ gọi: xem đoạn lượt 10 ở trên (jar: 1–3; đích: 4–6; W6 jar-merge: 7; W6 đích: 19; W6 liên kết: 14).

Tự kiểm phân hạng (không thuộc bảng giết, N10(c)): `tu_kiem_attributeerror` — `AttributeError("wp433-tu-kiem")` qua một `except`
đổi kiểu ⇒ TÍN DỤNG GIẢ; `tu_kiem_chu_thich` ⇒ SỐNG SÓT; `tu_kiem_sai_luot` — dòng 11 khai lượt đích `N3.1-W1` thay `N3.3` ⇒ ngoại lệ
khớp loại + dấu nhưng phát sinh ở lượt `N3.3`, nhãn thu được là (`N3.3`, `surrogate_jar`) ⇒ KHÔNG giết đúng ⇒ `run` trả `False`.
Tổng: **30** đột biến giết, 4 dòng E (10, 11 đo được thông điệp; 22, 24 dấu do đột biến/rig đặt), 26 dòng H. Tự kiểm bằng phép đo:
**3** dòng (10, 11, 27); 27 dòng lập luận, xác nhận khi chạy bảng trên mã thật (N10(a)).

## 5. `pham_vi_e`

Không chạm E4, không chạm E5. E4 (`ADR-0067`: "đọc hay ghi secrets"): packet sửa MÃ của đường ghi credential nhưng không đọc
hay ghi credential thật nào; mọi ca dùng giá trị giả, HOME tạm, đồ giả thay tải Drive (rig chặn cả hằng baked, M5), không gọi
LIVE, không đẩy Package. Phép xác minh cần đọc bundle thật thuộc E4, ngoài packet (§8). Không đổi danh sách thẩm quyền, cổng
lease hay cổng merge (E5); ngoại lệ bundled ở §1 là quyết định của chủ kho cho đúng packet này, không phải thay đổi protocol.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**. **Quyết định đã có:** trần lời gọi Codex nâng 10→12 cho packet này, chủ kho duyệt 18-11-2026 (Review Rescue Checkpoint); nâng tiếp 12→13 (một lượt xác nhận), chủ kho duyệt 18-11-2026; không áp cho `GWS-CRED-DICH-NGOAI-KHO`.
- Trần kích thước `ADR-0053` (dòng khai đầu tệp). numstat (N13) vượt 450 ⇒ dừng TRƯỚC review và đi revision đặc tả để tách
  tiếp (chủ kho đã chọn tách thay vì nâng trần, 18-11-2026); xin `nang_tran` chỉ khi chủ kho đổi quyết định đó — **E2**.
- Chưa có comment cấp ngoại lệ bundled của chủ kho trên Issue #433 (§1) ⇒ không cấp lease.
- Cần sửa ngoài write set, hoặc preflight thấy chỗ ghi credential từ bundle KHÁC W1–W6 trong `scripts/tl_gws.py` (lệnh quét
  §0.1, chạy lại trên exact base) ⇒ dừng, đi revision.
- Neo PD của `ops/cloud_agent_creds_test.py` hoặc chuỗi khoá của `wp727_tl_gws_refresh` (§0.4) không giữ được nguyên văn ⇒
  dừng, đi revision.
- Đặc tả không thuộc Mission nên chờ chủ kho duyệt băm theo `ADR-0067` — **E2**. Kèm khi hỏi hai mục còn mở:
  1. **W6/M3** (phát hiện của lượt soạn, ngoài danh sách đã duyệt hướng): W6 ghi nguyên tử; từ chối config là liên kết;
     `OSError` khi ghi config đổi từ `✓ … (ghi config lỗi)` rc 0 sang `✗ … ghi lỗi` rc 1; `--env chat` trả rc 1 khi `nlm_auth`
     sai dạng/khoá lạ; lần đọc của `load_creds` KHÔNG bị chặn (§2).
  2. **Điều kiện `.claude`** chuyển từ ca `r973_bootstrap_khong_export_khong_ghi_gemini` sang fragment (M6) — đảo lựa chọn "thêm
     vào ca d5 hiện có" của chủ kho, để `tl_selftest.py` ra khỏi write set; phương án cũ (sửa `_xem` của d5, chạy tuần tự với
     packet chạm `tl_selftest.py`) vẫn dùng được nếu chủ kho giữ.

**Quyết định đã có (chủ kho, 18-11-2026, qua phiên điều phối):** (a) phương án B — worker mang riêng bundled, không manifest,
quyền ghi bằng comment trên Issue #433 (§1); (b) tách packet: W4/W5 sang `GWS-CRED-DICH-NGOAI-KHO`, không nâng trần.

## 7. `hinh_dang_ke_thua`

Tiền nhiệm #431/#432 và chuỗi PR #434, #437, #438, #440, #441 của #433 đều đóng không merge (kiến trúc cũ, chủ kho bỏ).
Biên nhận của chúng không được chép vào kho, nên số đếm hình dạng lỗi theo L4: **KHÔNG ĐO ĐƯỢC**. Tiêu đề PR (đọc Issue #433 qua
MCP github khoảng 04:50Z; lời khai, không biên nhận) — `… at the actual write capability`, `Close final credential-root …`,
`Close final credential boundary gaps` — được đọc thành MỘT hình dạng "vá biên ghi credential, reviewer tìm ra đường ghi khác";
đó là SUY LUẬN từ tiêu đề, không phải bộ đếm. **Bộ đếm hiện tại là bộ đếm CÓ CHỨNG CỨ**, dùng CHUNG cho hai packet tách từ
đặc tả gốc (`NLM-GWS-DICH-NGOAI-KHO`, `GWS-CRED-DICH-NGOAI-KHO`; lớp và số đếm đi theo đường ghi, không reset khi tách). Chứng cứ: stdout
năm lượt review Codex của đặc tả (hiện ở scratchpad phiên điều phối `rvP1/luot1..5.stdout.txt`; phải chép vào `ops/reviews/` khi công
bố băm, chưa chép thì là lời khai). Đếm hình dạng "vá đúng chỗ được chỉ rồi bỏ sót đường khác" ở mức ĐẶC TẢ: **3** (lượt 1 — symlink
tệp cuối/thành phần/hardlink sau chốt thư mục cha; lượt 2 — `goc` dạng `alias/`, `alias/.`; lượt 5 — lá symlink jar không có ca sau
khi dời ca sang packet 2). Mức MÃ: 0 (chưa có mã).
Hai lượt review đặc tả lặp lại đúng hình dạng ấy ở mức đặc tả: lượt 1 — chốt ở thư mục cha lọt ghi xuyên symlink tệp cuối,
symlink thành phần, hardlink (§0.2 S1–S5); lượt 2 — `lstat` trên chuỗi `goc` thô không thấy `alias/`, `alias/.` (§0.4). Đáp lại:
chốt trên CHÍNH đường đích dựng từ thành phần (M1), liệt kê đủ chỗ ghi TRƯỚC (§0.1, gồm W6 tự tìm), luật dừng khi preflight thấy
chỗ thứ bảy. Độ phủ đột biến THEO LỚP, nói đúng phạm vi: danh sách cho phép — N1, N2; dữ liệu jar — N3 (dữ liệu W6: packet 2 M7/N9w6); luật (a) kho — CHỈ biến thể bỏ cả
luật ở caller (`db_bo_kho`, N4), hai biến thể dùng riêng một chuỗi CHỜ packet 2 N3b, thân `_trong_kho_git` do PD7/PD8 canh; luật (b)
tệp cuối — `w6_symlink_config` (N6(2)), đột biến `db_bo_symlink_cuoi` CHỜ packet 2; thành phần thư mục — N6(3); reparse — packet này KHÔNG có mã
lẫn ca (cả hai ở packet 2: N3c giả lập, N4 junction thật); nhánh jar rỗng của base — mã không đổi, ca hồi quy ở packet 2 N3d; ghi nguyên tử — hardlink W1 N6(4); thứ tự đọc merge — N6(2); chỗ gọi riêng — N1 (W1, W2, W3: kiểm jar và kiểm đích, mỗi chốt một đột biến), N7 (W6).
WP1334 (`8ed3503`, `3b23422`) là tiền lệ cùng hướng đã land: một vòng review bắt thêm đường `..` sau symlink (PD8).

## 8. `chua_do_duoc`

- Khoá thật của `nlm_auth` trong bundle trên Drive (`tl_secrets.enc`, `nlm_cred.enc`): không đọc được (E4). Bundle cũ mang khoá
  ngoài `_NLM_AUTH_RELS` ⇒ W1–W3 từ chối cả lượt cho tới khi stage lại; stage lại chỉ sinh khoá thuộc danh sách (§0.3). Bundle
  sinh trước baseline v1.29.4 (2026-07-02) không có lịch sử git để đo.
- Máy thật có thể để `~/.notebooklm-mcp-cli` hay `~/.tra_luat_config.json` là liên kết (dotfile manager): sau packet, lượt nạp vào
  đó bị từ chối với một dòng lý do. Chưa đo trên máy nào.
- Windows: packet này không chặn junction/reparse point (chỉ `S_ISLNK`; §2, §3). Mã và phép đo của vế reparse đều ở packet
  `GWS-CRED-DICH-NGOAI-KHO`. Byte của jar: base ghi chế
  độ văn bản (`\n` → `\r\n` trên Windows), mã mới ghi byte UTF-8 nguyên văn (JSON đọc được cả hai). Chưa chạy trên Windows thật.
- Kích thước (ước lượng tĩnh, chưa đo; tính lại 2026-11-18T08:12:33Z theo `date -u`): `tl_gws.py` +98–121;
  fragment +270–298 (bớt bốn vế N3(4)–(7) và năm dòng đột biến ~20–22; lượt 10 thêm ca khoá lạ một thành phần ba lượt ~3 và
  thay hai đột biến bằng ba ~1); bundled +1 ⇒ **369–420 dòng thêm, 3 tệp**, biên 30.
  Đã chuyển sang packet 2 qua các lượt: N5 cũ (hai chuỗi), symlink tệp cuối của jar + `db_bo_symlink_cuoi` (giữ ca tối thiểu
  `w1_la_symlink`), MÃ và ca của vế reparse, ca `jar_rong_base` + `db_w1_jar_rong_moi` (mã nhánh ấy không đổi ở đây), và (lượt này)
  MÃ + ca + đột biến kiểm dữ liệu W6. N13 đo trên exact head trước review; vượt ⇒ §6.
- `review_class` chưa đối chiếu bằng `lease_publish check`; `ai-dang-giu` cho `scripts/tl_test_fragments_bundled.py` CHƯA đo.
- Branch protection của `master` chưa đo (không ảnh hưởng: với bundled trong diff, bước `bundled-fragment check` dự kiến xanh).
- Các số dòng §0.1 phần "phạm vi rà ngoài `tl_gws.py`" chép từ bảng sự thật của review lượt 1, chưa đo lại.

## 9. Lịch sử review đặc tả

| lượt | bản | kết luận | xử lý |
|---|---|---|---|
| Codex 1 (05:12:16Z) | `f6b536fc…` | `request_changes` (2 P1, 4 P2, 2 P3) | Chốt trên chính đích + ghi nguyên tử; artifact land-only; W6 không lưu `nlm_auth` bị từ chối; rig chặn hằng baked; hợp đồng lỗi; phản chứng theo (ca, nhãn); d5 sang fragment; provenance. Bảng chi tiết ở bản `ded9b932…` §9. |
| Codex 2 (05:30:13Z) | `ded9b932…` | `request_changes` (1 P1, 4 P2, 2 P3 còn mở) | `goc` dựng từ thành phần (phần GWS sang packet 2); reparse point thay `isjunction`; khe protocol–CI ⇒ chủ kho chọn B; N7 tách ca chỉ-W6 cho đột biến `degraded`; một hợp đồng lỗi W6, kiểm dict/encode; thu hẹp lời hứa đọc config (`load_creds`); tổng kết ra stderr, lớp chặn subprocess theo cửa sổ, N13 `pipefail` + đúng số dòng; neo dòng 1244/972/1037/2026, mẫu 12 fragment. Bảng chi tiết ở bản `188c55bf…` §10. |
| Quyết định chủ kho (18-11-2026) | `188c55bf…` | phương án B; tách packet | Bản này: write set 3 tệp, W4/W5 sang `GWS-CRED-DICH-NGOAI-KHO`, bỏ điểm hỏi A/B và nâng trần. |
| Codex 3 (lượt 3) | `d863a253…` | `request_changes` (0 P1, 4 P2, 2 P3; một P2 thuộc packet 2) | W6 kiểm token/webappUrl trước khi gán env (đo 06:13:09Z: surrogate ⇒ `UnicodeEncodeError` ở `os.environ`), tách ca token hỏng / tuần tự hoá hỏng / config cũ không phải `dict` (đo: `.update` ⇒ `AttributeError`); ca W2 jar hợp lệ đích bị chặn cho `db_w2_bo_chot`; ca giả lập bit reparse + đối chứng + `db_bo_reparse`; quan sát lần đọc merge (`khong_doc_merge`); phản chứng trần 450/451 với đúng 3 dòng; tiền điều kiện `_kiem_dich_ghi`; E2 tại điều kiện comment; HOME đặc biệt khai thẳng. Chuyển N5 cũ và ca rc 4 sang packet 2 để giữ trần. |
| Codex 4 (lượt 4) | `d8c961e9…` | `request_changes` (5 P2, 1 P3; 6 finding lượt 3 đóng) | M3(0b) kiểm NUL cho cả hai trường trước mọi phép gán (đo 06:20:01Z), ca `env_nul`; đối chứng reparse dùng `FILE_ATTRIBUTE_DIRECTORY` (16) để `db_reparse_moi_thu` có răng; M2 ghi rõ nhánh định dạng sẵn có của W1/W2/W3 và ca `jar_rong_base`; ca `require` chạy lại fixture W2; §7 thu hẹp lời khai độ phủ theo lớp. Chuyển ca symlink tệp cuối của jar sang packet 2 để giữ trần. |
| Codex 5 (lượt 5) | `3efaba5e…` | `request_changes` (3 P2, 1 P3) | Ca tối thiểu `w1_la_symlink` + `db_bo_tien_to_cuoi`; định dạng dòng cố định `[thẻ] ✗ <cụm>: <repr…>`, nhận diện bằng `fullmatch` đầu dòng, ca `mot_dong`/`cum_trong_khoa`; §7 bộ đếm có chứng cứ dùng chung hai packet. Chuyển reparse giả lập và `jar_rong_base` sang packet 2 để giữ trần. |
| Điều chỉnh của phiên điều phối (trước lượt 6) | `619d9717…` | — | Chuyển LUÔN mã vế reparse sang packet 2 (packet này chỉ `S_ISLNK`, khai không chặn junction); ghi rõ packet này không đổi mã nhánh jar rỗng nên ca `jar_rong_base` ở packet 2 hợp lệ. |
| Codex 6 (lượt 6) | `adfbe103…` | `request_changes` (3 P2, 1 P3) | Ca `mot_dong` đặt `\n` vào đường KHO được in (đo 06:33:10Z: bỏ `repr` ⇒ 2 dòng); "đúng một cụm" giới hạn vào trường phân loại; mốc §8 ghi theo `date -u` (2026-11-18T06:33:42Z). |
| Codex 7 (lượt 7) | `cc70d9e6…` | `request_changes` (2 P2) | `mot_dong`: POSIX kho thật, Windows giả lập giá trị trả về của `_trong_kho_git`, cùng hậu điều, không vào `bỏ_qua`; M5 thêm luật "ngoại lệ dự kiến": bắt TẬP ĐÓNG ở biên lời gọi, đổi thành nhãn qua `TinHieuChotCa`, ngoài tập thì lan ra (không tín dụng). |
| Codex 8 (lượt 8) | `b9f73158…` | `request_changes` (2 P2, 1 P3; lượt thứ hai liên tiếp cùng hình dạng "đột biến chết bằng ngoại lệ chưa khai") | Không vá riêng ba dòng được chỉ: lập §4b — bảng ĐẦY ĐỦ 32 đột biến, mỗi dòng ghi cơ chế chết (H/E) và ngoại lệ khai; tập khai của mỗi ca lấy từ bảng; ràng buộc cài đặt để cơ chế tất định (`nlm_auth.items()`, chỉ bắt `OSError` ở vòng ghi, dấu `wp433-oserror`, `wp433-tu-kiem`). Tự kiểm: 7 dòng bằng phép đo nguyên tố (06:42:22Z, 06:33:10Z), 25 dòng lập luận. Rà toàn bảng tìm thêm `db_bo_kiem_kieu_jar`, `db_bo_kiem_encode`, `db_w6_bo_kiem_encode` cũng chết bằng ngoại lệ chưa khai — đã khai. |
| Codex 9 (lượt 9) | `e415e6ae…` | `request_changes` (4 P2/P3 cho packet 1) | Khai ngoại lệ theo LƯỢT GỌI, không theo ca, kèm nhãn `ngoai_le_la` và tự kiểm `tu_kiem_sai_luot`; rà toàn §4b (dòng 10–12 tách lượt; 9, 13, 26 khai mọi lượt cùng nhãn); tách đột biến gộp hai chốt ở W1/W3 (`db_w1_bo_kiem_dich`, `db_w3_bo_kiem_dich`) + ca `w3_jar_hop_le_dich_bi_chan`; fixture N3.1 = `[1]`. Ước lượng 395–450, biên 0. |
| Điều chỉnh trước lượt 10 (2026-11-18T06:53:23Z) | `8c493e58…` | — | Chuyển khối kiểm DỮ LIỆU W6 (mã M3(0b) + phần dữ liệu của M3(3), ca N3(4)–(7), năm đột biến) sang packet 2 (M7/N9) để biên packet 1 từ 0 lên 34; tự kiểm `tu_kiem_sai_luot` nhắm lại dòng surrogate jar. |
| Codex 10 (lượt 10) | `2b6b7260…` | `request_changes` (packet 1: 1 P2, 1 P3) | Thay hai đột biến "quay về vòng ghi base" bằng ba đột biến chỉ bỏ kiểm jar ở từng caller (W2: M3(1)) + ca `chung_khoa_la_mot_thanh_phan` (khoá một thành phần `khac.json`); M4 giới hạn "không ngoại lệ" vào phạm vi lỗi packet này, bỏ tham chiếu M3(0b). Quyết định chủ kho 18-11-2026: trần lời gọi Codex 10→12 cho packet này; packet 2 hoãn. |
| Codex 11 (lượt 11, sửa 2026-11-18T08:17:06Z) | `1818a859…` | `request_changes` (2 P2, 1 P3) | `db_w2_bo_chot` → `db_w2_bo_kiem_dich` (chỉ bỏ `_kiem_dich_ghi`, giữ writer); rà toàn §4b để mỗi đột biến đổi đúng một cơ chế (dòng 14, 18, 19 ghi rõ phạm vi; `db_w6_bo_symlink` đổi thành đích kiểm lệch một cấp vì bỏ lời gọi đã là dòng 19); các lượt W3 đo LÝ DO trả về bằng `fullmatch` đầu chuỗi, không đòi stderr; `M7/N9` → `M7/N9w6`. |
| Codex 12 (lượt 12, sửa 2026-11-18T08:52:38Z) | `eb7c6040…` | `request_changes` (1 P2, 1 P3) | `db_w6_bo_symlink` định nghĩa lại: chỉ bỏ luật (b) ở lá config W6, giữ nguyên đầu vào luật (a); đối chứng HOME = `K/home` và HOME = `K` không đổi màu (N10(7)); §2/M3 ghi lỗi tuần tự hoá vẫn lan ra nhưng config cũ giữ byte (đo 08:52:10Z). Quyết định chủ kho 18-11-2026: trần lời gọi Codex 12→13 cho packet này. |
