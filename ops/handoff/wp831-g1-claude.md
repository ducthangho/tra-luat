# Handoff wp831 g1 — RG-NO-SAU-802 (executor `wp831-r1-g1-claude`)

Packet #831 · spec `ops/specs/wp831.md` sha256 `92d179bc…9888` (ref `ops/wp831-spec@9eaea9b`) · lease
`ops/leases/wp831-r1-g1-claude.yaml` (nhánh `ops/wp831-r1-g1-lease@c0fb50f`, đăng bởi run `39113916942` success).
Nhánh `agent/wp831-g1-claude`, base `dfe5437`, đã merge `origin/master@1e69d2a` (không rebase).
KHÔNG merge/land/deploy — việc của chủ kho.

## Đã làm
| tệp | việc |
|---|---|
| `ops/cong_cu.yaml` | L1: `rg.cai.linux`/`macos` chọn thư mục ĐẦU TIÊN mà `cong_cu.py kiem-tra --chi rg` nhận `DAT`, ghi `$GITHUB_PATH` khi có; không ứng viên nào ⇒ thoát ≠ 0. Phần trước ` && ` đầu tiên giữ nguyên. |
| `.claude/dev/launcher_test.py` | `r831_cai_rg_linux_chon_ban_chay_duoc`, `r831_cai_rg_macos_chon_ban_chay_duoc` (mỗi ca 2 chiều dương + 3 chiều âm) · 7 đột biến `wp831_yaml_*` · neo `wp802_yaml_chon_ung_vien_chi_theo_ma_thoat` dài thêm để vẫn khớp đúng một chỗ. |
| `docs/GOI_AGENT_DA_NEN.md` | L2: bảng bắt buộc THEO NỀN (đo từ `_bat_buoc`), mã 12 gồm `xac_thuc` SAI và `BI_CHE`. |
| `changelog.d/wp-831.md` | fragment. |
| `RELEASE_MANIFEST.json` | L3: sinh lại sau cùng (xem "Cổng"). |

Kích thước (so `origin/master`): xem `git diff --numstat origin/master` trên head cuối; trần ADR-0053 ≤ 6 tệp / ≤ 450 dòng thêm.

## Hai chỗ lệch chữ của spec (đã báo, chờ chủ kho): https://github.com/ducthangho/tra-luat/issues/831#issuecomment-6248148183
1. **Q1:** ứng viên Linux đầu là thư mục `dpkg -L ripgrep` khai (không đọc được ⇒ `/usr/bin`), không phải chuỗi `/usr/bin`
   cứng. Lý do đo được: container và runner CI đều có `/usr/bin/rg` chạy được, test không ghi được `/usr/bin`, nên với
   chuỗi cứng nửa âm của N1 không thể đỏ và nửa dương chọn nhầm `/usr/bin`.
2. **N4:** tập bắt buộc không phải "git, python, rg" mà theo nền: git/python/rg/bash luôn; claude/codex trừ CI; gh chỉ
   máy người dùng. Tài liệu theo mã.

## Cổng (đo tại chỗ, hai vế dựng trong MỘT lệnh: clone `--no-hardlinks`, `core.abbrev 7`, `PYTHONDONTWRITEBYTECODE=1`)
- `launcher_test.py`: nền `1e69d2a` **232/232** (2 bỏ qua) · head `5c303c9` **234/234** (2 bỏ qua), CÓ và KHÔNG
  `CODEX_AUTH_JSON` giả — delta 0 ca đỏ, +2 ca mới.
- `--dot-bien` @`5c303c9`: 278/279 — `wp831_yaml_linux_chi_theo_ma_thoat` SAI vì neo dùng `'` đơn trong khi đột biến
  YAML so trên văn bản tệp (`''`). Vá ở `506f448`; số đo lại trên head cuối: xem mục "Kết quả cuối".
  4 "không đo được trên nền này" là đột biến Windows-native/ca đích bỏ qua, có sẵn từ trước.
- `ruff check --select F .claude/dev/launcher_test.py`: 5 F841 = 5 trên nền ⇒ delta 0.
- `doctrine-scan --root .` rc 0 · `tl.py doc-claims-check --strict` `ok: true`.

## Kết quả cuối
(điền sau push: run CI `ci.yml`, run `launcher-windows.yml` + số ca bỏ qua, verdict Codex, `release-verify` trên head cuối)

## Nợ còn lại (KHÔNG vá trong packet này — spec "Ngoài phạm vi"/Q6/Q8)
- Công thức cài của `git`, `python`, `shellcheck`, `bash` trong `ops/cong_cu.yaml` vẫn `dirname "$(command -v …)"` —
  cùng hình dạng L1 (bản hỏng đầu PATH được in làm thư mục cài).
- `ops/bash_nen.py:900` in `SyntaxWarning: invalid escape sequence '\('` mỗi lần nạp (thấy trong log `--dot-bien`); thuộc
  lease `wp748-r18-g18`, chẩn đoán ở #748.
- Spec N4 khai thiếu tập bắt buộc (xem trên) — soạn spec sau nên đo `_bat_buoc` thay vì chép.
