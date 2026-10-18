# Kế nhiệm WP710 — hướng dẫn NLM cũ ngoài write set + phép đo Linux độc lập (BẢN NHÁP, CHƯA ĐÓNG BĂNG)

> **ĐÃ BỊ THAY THẾ** bởi bốn đặc tả r1: `ops/specs/wp725-…`, `wp726-…`, `wp727-…`, `wp728-…` (Issue #725–#728), sau khi chủ kho đồng ý mọi khuyến nghị Q1–Q10. Tệp này giữ làm hồ sơ quyết định.
>
> **TRẠNG THÁI: NHÁP r0.** Băm của tệp này KHÔNG dùng cho lease. Các ô `CHỜ Qn` là quyết định của
> chủ kho (xem phần "Quyết định chờ" cuối tệp). Khi đóng băng: đổi tên thành `ops/specs/wp<issue>-<slug>-r1.md`
> theo số Issue thật, xoá mọi ô `CHỜ`, rồi mới tính `sha256`.
> Mọi số đo dưới đây đo lúc **2026-10-09T16:58Z** trên `origin/master` `353da6b30f7e2f54a7bed92db97c0fe9ea70a21d`
> (tree `786902b6da7740c47654cc781faa244312736498`), clone đã `--unshallow`, tập nhánh máy chủ = tập cục bộ
> (492 tên, `comm -23` rỗng). Đo lại trước khi đăng băm/cấp lease (L5).

## packet_id · packet_issue

- `packet_id`: **CHỜ Q1** (`wp<issue>` sau khi có Issue). Đề xuất tách HAI packet code + MỘT lượt đo — xem Q1.
- `packet_issue`: CHƯA CÓ. Đã kiểm 16:50Z: không Issue mở nào từ 2026-10-01 nhắc hai lớp này
  (`list_issues` since 2026-10-01: 15 Issue, không cái nào); `search_issues` theo chủ đề: 0 kết quả;
  `ops/specs/`, `ops/leases/` chỉ có hồ sơ của chính WP710.

## nguon_cap_viec

Packet khắc phục, cha là WP710 (Issue #710, Spec r4 sha256
`a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b`), đã land bằng
`8b59185975a938504de5963d2310e574dd4858b2` (là tổ tiên của `origin/master`, đo bằng `merge-base --is-ancestor`).
Nguồn finding: `ops/reviews/wp710-g5-luot-9/VERDICT.md` trên nhánh `ops/wp710-g5-hien-vat-review`
(commit `2e53b19a9c86a06f8f67247f9d68d8933d780de0`; định danh là BĂM commit, không phải tên nhánh — tìm ở
`master` trước, chưa thấy thì fetch nhánh ấy), dòng 20 và 22 (bảng lớp) cùng mục "FINDING THEO LỚP".

## hinh_dang_ke_thua (L4)

Đếm theo **lượt review** (đơn vị: một lượt Codex cross-review của WP710 có VERDICT trong hồ sơ):

| lớp | số lượt nêu | trạng thái ở lượt 9 | ghi chú |
|---|---|---|---|
| `huong-dan-cu-con-lech-sau-va-ngoai-write-set` | 7 (lượt 3→9), theo lời khai của chỉ thị; lượt 4–9 đối chiếu được trong hồ sơ g5, lượt 3 CHƯA đối chiếu ở phiên này | CHƯA VÁ, P3 | ngoài write set nên không vá được — lặp không phải vì vá hờ |
| `linux-subreaper-khong-thu-hoi-zombie` | lượt 9 ghi "P2 lịch sử thiếu đo" | mã có; việc đóng KHÔNG ĐO ĐƯỢC độc lập | bên duy nhất đã đo là Executor |

Hình dạng đáng chép sang: **phạm vi lời khai của reviewer hẹp hơn phạm vi lỗi thật.** Verdict nêu 4 tệp;
quét toàn kho lúc 16:55Z (agent đọc-thôi, rồi kiểm tay từng dòng) ra thêm **4 tệp có hướng dẫn trái quy trình
mới** và **1 tệp nêu trong verdict mà thực ra không lệch** — bảng ở mục `write_set`. Đúng hình dạng
"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA" của CLAUDE.md: Executor phải tự quét lại, không vá theo danh sách.

## review_class

**CHỜ Q1/Q6.** Đề xuất: packet A (tài liệu + chuỗi trợ giúp) `systemic` — chạm 3 tệp trong
`RELEASE_MANIFEST.json` và một golden; packet B (đường quyết định sống/chết và đường stage trong mã) `sensitive`
— đổi hành vi của Routine bảo trì đang chạy và đường dẫn credential. Thiếu quyết định ⇒ cả hai xử như `sensitive`.
`.github/coordination/change-impact.v1.json` VẮNG (đo 16:52Z: thư mục chỉ có 3 tệp `.md` và `schemas/`), nên
effective write set không tính được bằng máy — cần ngoại lệ thủ công có giới hạn như WP710 (nợ #473).

## write_set (đề xuất, mọi đường dẫn `exact`)

Bảng phân loại MỌI hit của `rg -n 'nlm login|login --check|nlm-auth-stage'` ngoài `ops/**`, `CHANGELOG.md`,
`references/changelog_archive/**` (đo 16:55Z):

| tệp | dòng (đo lại) | trong manifest | vì sao lệch / không lệch | đề xuất |
|---|---|---|---|---|
| `scripts/tl_core/cli.py` | 145 help `[CODE, sau \`nlm login\`]`; 147 `--refresh` "tái sinh cookie từ browser profile"; 150 `--force` "bỏ qua cổng verify-LIVE — ép stage DÙ cookie đang chết" | có | 150 nói NGƯỢC sự thật: từ WP710 `--force` KHÔNG qua được cổng canary (RUNBOOK:176) | A |
| `references/golden/parser_surface.json` | 91 (băm `nlm-auth-stage`) | có | băm phủ help của lệnh và mọi cờ (`tl_selftest.py:6602–6631`); sửa cli.py ⇒ `r77a_parser_surface_matches_snapshot` ĐỎ | A (**CHỜ Q5**) |
| `references/COWORK_PROJECT.md` | 83 (`secrets-set --nlm` "tự `nlm login --check` refresh"), 84–88 (Task Scheduler hằng ngày, `TL_MASTER_KEY` trong dòng lệnh task), 94 | có | trái chuỗi refresh→canary→stage; Scheduled Task trái giới hạn WP710 | A (**CHỜ Q7**) |
| `references/RUNBOOK.md` | 195 "`nlm login --check` xanh" làm tín hiệu thành công | có | trái chính RUNBOOK:209/718 | A |
| `scripts/nlm-auto-refresh.sh` | 76 phán sống bằng `login --check`; 78 `nlm-auth-stage >/dev/null 2>&1 \|\| true`; 85 `nlm login && nlm-auth-stage` | có | false-green + nuốt rc; chạy bởi Routine bảo trì (CHANGELOG v1.35.87: `trig_01ReWux8`) | B (**CHỜ Q3**) |
| `scripts/env-reimport.sh` | 129–130 phán sống bằng `login --check`; 137 `nlm login && nlm-auth-stage` | có | cùng lỗi | B |
| `scripts/nlm-auth-import.sh` | 195 phán sống bằng `login --check`, gate cho bước 5; 208–211 mọi lỗi stage (kể cả rc 4 canary từ chối) in "cookie ở ĐÂY vẫn dùng được" | có | rc KHÔNG bị nuốt (`pipefail` ở :37) nhưng diễn giải sai rc 4 | B |
| `scripts/tl_gws.py` | 756–765 `_refresh_nlm_auth` gọi `nlm login --check` (sau cờ `--refresh`, gọi ở 954/1021/1746, giá trị trả về bị bỏ qua — cổng canary vẫn chạy sau nên KHÔNG phải lỗ sống/chết); 1405, 1787 "Kiểm: nlm login --check"; 839/1672/1695/1718/1727/1769 thứ tự cũ `nlm login → nlm-auth-stage` | có | bước refresh là quy trình cũ; chuỗi gợi ý dạy phép kiểm false-green | B (**CHỜ Q4**) |
| `docs/WORKFLOW_RASOAT_TU_DONG.md` | 274, 362 | KHÔNG | dòng 3: "⛔ TÀI LIỆU LƯU TRỮ … KHÔNG PHẢI CHỈ DẪN VẬN HÀNH"; nằm trong `_DOC_CLAIMS_HISTORICAL` (`scripts/tl_core/workflow.py:841`); dòng 274 đã nói "KHÔNG tin `nlm login --check`… xác nhận CHỈ bằng probe live" | **loại** (**CHỜ Q2**) |
| `scripts/tl.py` | 122–123 chú thích "Stage 1 lần ở Code (sau `nlm login`)" | có | chỉ là chú thích; `tl.py` là tệp nóng phải chạy tuần tự (§5) | **loại**, ghi nợ có tên |
| `tl-setup.ps1`, `tl-setup.cmd` | — | — | 0 hit `nlm` (không phân biệt hoa/thường) — khớp đo lượt 4, bác lượt 3 | loại |

Cộng mỗi packet: `changelog.d/wp-<issue>.md` và `scripts/test_fragments/wp<issue>_<slug>.py` (§5: test mới vào
fragment, KHÔNG vào `tl_selftest.py`). Kích thước theo ADR-0044: A = 4 tệp sản phẩm + 2 = **6 tệp** (trần
thường 6); B = 4 + 2 = **6 tệp** — vượt trần `sensitive chạm authority` (≤3 tệp, ≤300 dòng) nếu B bị xếp
chạm authority ⇒ có thể phải tách B thành B1 (ba script shell) và B2 (`tl_gws.py`). **CHỜ Q1.**

Tệp hiện vật land-only, KHÔNG thuộc write set Executor: `RELEASE_MANIFEST.json`.

## ngoai_pham_vi

- `docs/WORKFLOW_RASOAT_TU_DONG.md` (tài liệu lưu trữ, đã nhất quán — nếu Q2 chọn loại).
- `scripts/tl.py:122–123` — nợ có tên `tl-py-chu-thich-thu-tu-stage-cu`.
- `scripts/nlm-credential-refresh.ps1`, `.Tests.ps1` — không sửa; đồng hồ WSL trôi (2,9 s/130 s, 7,0 s/256 s so
  dung sai 1 s, lời khai Executor WP710, chưa ai đo độc lập) giữ là giới hạn đã ghi ở RUNBOOK (**CHỜ Q8**).
- Các hit HISTORICAL (`rasoat/**`, `changelog.d/wp-710.md`, `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md:263`,
  chú thích có ngày trong `tl_gws.py`/`nlm_ops.py`) và ~60 hit đã nhất quán (dùng `nlm login` làm bước PHỤC HỒI
  hoặc cài đặt lần đầu — RUNBOOK cho phép).
- LIVE, credential thật, Drive, deploy, merge/land.

## muc_tieu

Packet A:
1. `scripts/tl_core/cli.py` — help của `nlm-auth-stage`, `--refresh`, `--force` nói đúng hành vi hiện tại.
2. `references/golden/parser_surface.json` — chỉ băm `nlm-auth-stage` đổi, sinh bằng `TL_WRITE_PARSER_SURFACE=1`.
3. `references/COWORK_PROJECT.md` — mục 3 trỏ quy trình WP710 (RUNBOOK mục "WP710 — làm tươi credential NLM"), bỏ `login --check` làm phép refresh/xác nhận.
4. `references/RUNBOOK.md` — dòng 195 bỏ `login --check` làm tín hiệu thành công.
5. `changelog.d/wp-<issue>.md` — mảnh changelog, không bump version.
6. `scripts/test_fragments/wp<issue>_<slug>.py` — ca khoá.

Packet B:
1. `scripts/nlm-auto-refresh.sh` — phán sống bằng canary dương (đường đề xuất: rc của `tl nlm-auth-stage`, vốn tự chạy canary — rc 0 sống+đã stage, rc 4 canary không dương ⇒ chết, rc khác ⇒ hạ tầng), KHÔNG nuốt rc.
2. `scripts/env-reimport.sh` — như trên, không stage (script này chỉ báo).
3. `scripts/nlm-auth-import.sh` — phán sống bằng canary; phân biệt rc 4 với lỗi khác khi báo.
4. `scripts/tl_gws.py` — `_refresh_nlm_auth` và các chuỗi gợi ý theo quy trình mới.
5–6. changelog fragment + test fragment.

## nghiem_thu (mỗi tiêu chí nêu phép đo làm nó ĐỎ — L3)

- **N1 (cả hai).** `rg -n 'login --check'` trên các tệp write set chỉ còn hit ở câu phủ định có chủ đích
  (danh sách CHO PHÉP các dòng, ghi cứng trong test fragment, không danh sách cấm). ĐỎ: thêm lại một dòng
  `nlm login --check` khẳng định vào bất kỳ tệp nào trong write set ⇒ ca fragment đỏ.
- **N2 (A).** Help `--force` không còn khẳng định bỏ qua được cổng. ĐỎ: ca fragment đọc `build_parser()` và
  đòi help `--force` khớp câu mới; đột biến trả câu cũ ⇒ đỏ.
- **N3 (A).** `r77a_parser_surface_matches_snapshot` xanh; `git diff -- references/golden/` đúng 1 dòng (băm
  `nlm-auth-stage`). ĐỎ: sửa help mà không sinh lại golden ⇒ r77a đỏ (đã có sẵn).
- **N4 (A).** Ca r228 (`tl_selftest.py:26401`, con trỏ RUNBOOK→COWORK_PROJECT) vẫn xanh.
- **N5 (B).** Với `nlm`/`tl` giả GIỮ TRẠNG THÁI (không diễn kịch bản): `nlm login --check` trả "valid" nhưng
  canary âm ⇒ script báo CHẾT và thoát mã chết; canary dương ⇒ SỐNG. ĐỎ: đột biến khôi phục phán quyết bằng
  `login --check` ⇒ ca false-green đỏ. Nhật ký lời gọi phải chứng minh 0 lời gọi `login --check`.
- **N6 (B).** `nlm-auto-refresh.sh`: stage rc ≠ 0 lan ra mã thoát. ĐỎ: đột biến thêm lại `|| true` ⇒ đỏ.
- **N7 (B).** `nlm-auth-import.sh`: rc 4 của stage in thông điệp "canary không dương", khác lỗi hạ tầng. ĐỎ:
  đột biến gộp hai nhánh ⇒ đỏ.
- **N8 (B).** `_refresh_nlm_auth` không gọi `login --check`. ĐỎ: ca fragment chặn subprocess, ghi argv; đột biến
  trả lệnh cũ ⇒ đỏ. (Hành vi thay thế CHỜ Q4.)
- **N9 (cả hai, nghĩa vụ LAND).** Sau merge, lane LAND trên `master` chạy
  `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ phải `ok=true`, `expected == checked`.
  Vì sửa NỘI DUNG tệp trong manifest làm sha lệch mà `file_count` không đổi, và lane PR (manifest tạm) KHÔNG bắt
  được: hồ sơ land phải tái sinh `RELEASE_MANIFEST.json` (`tl release-manifest --out RELEASE_MANIFEST.json --json`)
  và chạy lệnh trên TẠI CHỖ trước khi merge. ĐỎ: bỏ bước tái sinh ⇒ lệnh trả `ok=false`.
- **N10.** Gate theo CLAUDE.md: ruff F delta = 0 so master; selftest N/N với hai số bằng nhau; worker gate xanh.

## Tồn 2 — yêu cầu PHÉP ĐO ĐỘC LẬP (không phải packet code)

Đối tượng: lớp `linux-subreaper-khong-thu-hoi-zombie` và hai phép so parity 101 dạng / 168 chuỗi byte, trên
mã đã land (`scripts/nlm-credential-refresh.ps1`, `.Tests.ps1` tại `origin/master` `353da6b`).

Ai đo: **bên KHÁC Executor**. Executor g5 của WP710 là `claude` (lease `ops/leases/wp710-r4-g5-claude-windows.yaml`:
`provider: anthropic_claude`), nên phiên Claude nào (kể cả phiên soạn đặc tả này) đo cũng chỉ là
`same_provider`, KHÔNG đóng được lớp. Đề xuất: **Codex trên phiên cloud Linux** (`cross_approved`), hoặc human
audit. **CHỜ Q9.**

Nội dung đo, mỗi mục ghi lệnh, rc, đầu ra nguyên văn, phiên bản pwsh/Python/nhân:
- M1. `pwsh -NoProfile -File scripts/nlm-credential-refresh.Tests.ps1` ⇒ đòi `passed=N failed=0` với N bằng số ca
  bộ test đếm được trên Linux (lời khai Executor: 34). ĐỎ: bất kỳ `failed>0`, hoặc N khác số `$cases++` thực chạy.
- M2. Zombie qua NHIỀU chu kỳ: ca `v` hiện chỉ kiểm SAU CHU KỲ ĐẦU (`-MaxCycles 2`, `Tests.ps1:991–1027`), còn
  con số "4 chu kỳ, 0 zombie" của changelog đến từ rig KHÔNG có trong kho. Bên đo dựng rig ở scratch: wrapper với
  `-EnableKeepalive -MaxCycles ≥4`, sau MỖI khoảng nghỉ đếm con trạng thái `Z` của wrapper qua `/proc/*/stat`.
  Đòi 0 ở mọi khoảng. Phản chứng bắt buộc: bản sao tạm của wrapper đã gỡ lời gọi `Invoke-ReapAdopted` phải cho
  số zombie TĂNG (changelog khai đầu cũ: 1, 2, 3) — không có phản chứng thì phép đo không có răng.
- M3. Parity 101/168: script so của Executor KHÔNG nằm trong kho (đã tìm 16:57Z) ⇒ không tái lập nguyên văn
  được. **CHỜ Q10.**
- Bẫy rig đã biết: thiếu `python` (chỉ có `python3`) — `Tests.ps1:213` gọi `Get-Command python`; đồng hồ trôi
  trong pwsh sống lâu (WSL). Trên cloud Linux có thể không gặp, nhưng phải ghi `python --version` và lệch đồng hồ.
- Đầu ra: biên nhận trong `ops/reviews/<id>/` (VERDICT + run.json + SHA256SUMS), neo `reviewed_sha`.

## chua_do_duoc (từ phiên này)

- Codex trong container này: `doctor` 16:53Z báo `CHUA_XAC_THUC` — `access_token` hết hạn −135,1 h,
  `last_refresh=2026-09-24T01:47:47Z` ⇒ `CODEX_AUTH_JSON` của môi trường đã chết; lượt Codex cloud cần chủ kho
  làm mới nó (chép base64 NGAY sau `codex login`, xem CLAUDE.md "Refresh token của codex XOAY VÒNG").
- Hành vi thật của Routine `trig_01ReWux8` sau khi đổi mã thoát của `nlm-auto-refresh.sh` (B) — chưa đo ai/cái gì
  đọc mã thoát ấy.
- `nlm` CLI thật: `nlm auth refresh` có thay được `nlm login --check` trong `_refresh_nlm_auth` không (Q4) — không
  đo được offline.
- Lượt 3 có nêu `tl-setup.ps1` hay không: không đọc VERDICT lượt 3 trong phiên này (hồ sơ g5 chỉ có lượt 4–9).

## Quyết định chờ (tóm tắt — câu hỏi đầy đủ ở tin nhắn trình chủ kho)

Q1 tách packet · Q2 loại WORKFLOW_RASOAT · Q3 phán quyết của `nlm-auto-refresh.sh` · Q4 `_refresh_nlm_auth` ·
Q5 golden trong write set · Q6 executor/reviewer · Q7 Task Scheduler ở COWORK_PROJECT · Q8 đồng hồ WSL ·
Q9 ai đo Tồn 2 · Q10 parity 101/168.
