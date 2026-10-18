# Handoff wp831 g1 — RG-NO-SAU-802 (executor `wp831-r1-g1-claude`)

Packet #831 · spec `ops/specs/wp831.md` sha256 `92d179bc…9888` (ref `ops/wp831-spec@9eaea9b`) · lease
`ops/leases/wp831-r1-g1-claude.yaml` (nhánh `ops/wp831-r1-g1-lease@c0fb50f`, đăng bởi run `39113916942` success).
Nhánh `agent/wp831-g1-claude`, base `dfe5437`, đã merge `origin/master@1e69d2a` (không rebase). PR #832 (DRAFT).
KHÔNG merge/land/deploy — việc của chủ kho.

## Đã làm
| tệp | việc |
|---|---|
| `ops/cong_cu.yaml` | L1: `rg.cai.linux`/`macos` chọn thư mục ĐẦU TIÊN có `rg` tồn tại, thực thi được (`-x`, F01) và được `cong_cu.py kiem-tra --chi rg` nhận `DAT`; không ứng viên nào ⇒ thoát ≠ 0. Ứng viên: Linux `${CONG_CU_GOC:-}/usr/bin` (Q1) → `command -v`; macOS `$(brew --prefix)/bin` → `command -v`. Ghi `$GITHUB_PATH` CHỈ khi `rg` tên trần vẫn chưa `DAT`. Phần trước ` && ` đầu tiên giữ nguyên. |
| `.claude/dev/launcher_test.py` | `r831_cai_rg_linux_chon_ban_chay_duoc`, `r831_cai_rg_macos_chon_ban_chay_duoc`: 2 chiều dương + 3 chiều âm + "tên trần đã tốt ⇒ không ghi `$GITHUB_PATH`" + F01 (ứng viên không thực thi). 5 đột biến `wp831_yaml_*`. Neo `wp802_yaml_chon_ung_vien_chi_theo_ma_thoat` dài thêm để vẫn khớp đúng một chỗ. |
| `docs/GOI_AGENT_DA_NEN.md` | L2: bảng bắt buộc THEO NỀN (đo từ `_bat_buoc`), mã 12 gồm `xac_thuc` SAI và `BI_CHE`. |
| `changelog.d/wp-831.md` | fragment. |
| `RELEASE_MANIFEST.json` | L3: sinh lại (commit cuối có đổi tệp trong manifest). |

## Lệch chữ spec — trạng thái
- **Q1: ĐÃ RÚT lệch.** Bản đầu thay `/usr/bin` bằng thư mục `dpkg -L` khai; Codex lượt 1 F02 (P2) chứng minh nó có
  thể bỏ mất một `/usr/bin/rg` tốt. Nay ứng viên đúng Q1 (`/usr/bin` rồi `command -v`); `CONG_CU_GOC` (mặc định rỗng)
  chỉ là seam để test cô lập `/usr/bin` — không có nó nửa âm của N1 không thể đỏ trên máy có `/usr/bin/rg` tốt (Codex
  đo lại: q1_hard_usrbin). Báo ở https://github.com/ducthangho/tra-luat/issues/831#issuecomment-6248148183.
- **N4: giữ.** Tập bắt buộc theo nền (git/python/rg/bash luôn; claude/codex trừ CI; gh chỉ máy người dùng). Codex
  lượt 1 đối chiếu `_bat_buoc` và CHẤP NHẬN.

## Lỗi do chính packet gây ra rồi đã sửa (ghi cho người sau)
- `ci.yml` run `39115659366` @`c3c790e` ĐỎ: công thức ghi `/usr/bin` vào `$GITHUB_PATH` vô điều kiện ⇒ bước sau
  `python` thành python hệ thống 3.12.3 (`jsonschema` 4.10.3 thay 4.26.0). Sửa ở `720ee87`.
- `launcher-windows.yml` run `39115887003` @`720ee87`: 197/197 đạt nhưng 88 không đo được ⇒ 69,1% < sàn 70%. 9 đột biến
  wp831 đều chỉ đo được trên POSIX. Giữ 5 (một cho mỗi chốt) ⇒ 197/281 = 70,1%. **Sàn Windows gần cạn**: packet sau
  thêm đột biến chỉ-POSIX sẽ đụng sàn — nợ chung, không riêng packet này.

## Cổng (hai vế dựng trong MỘT lệnh: clone `--no-hardlinks`, `core.abbrev 7`, `PYTHONDONTWRITEBYTECODE=1`)
- `launcher_test.py` @`720ee87`: nền `1e69d2a` 232/232 (có auth giả) · 231/232 (không) — head 234/234 · 233/234.
  Ca hỏng ở CẢ HAI vế là `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac`, chỉ khi hai suite chạy SONG SONG;
  chạy riêng 10/10 qua ở cả hai vế ⇒ delta 0, không do packet. Nợ cách ly của `t86` (không vá).
- `--dot-bien` @`720ee87`: 281/281 (4 không đo được trên Linux, có sẵn).
- Đo lại trên head cuối: xem "Kết quả cuối".
- `ruff check --select F .claude/dev/launcher_test.py`: 5 F841 = 5 trên nền ⇒ delta 0.
- `doctrine-scan --root .` rc 0 · `tl.py doc-claims-check --strict` `ok: true` · `golden-test` ok.

## Review
- Codex lượt 1 (`gpt-6.1-sol`, `xhigh`, launcher run `ce422f79`, 825,7s, rc 0) @`c3c790e`: `changes_requested`,
  F01 `chooser-checker-path-fallthrough` P2, F02 `linux-candidate-set-drops-usrbin` P2; N4 chấp nhận. Verdict:
  `ops/reviews/wp831-g1-luot1-codex-verdict.md` trên nhánh `ops/wp831-r1-g1-lease`. Cả hai đã vá (xem trên).

## Kết quả cuối
(điền sau: run `ci.yml`, run `launcher-windows.yml` + số ca bỏ qua, verdict Codex lượt cuối, `release-verify`)

## Nợ còn lại (KHÔNG vá — spec "Ngoài phạm vi"/Q6/Q8)
- Công thức cài của `git`, `python`, `shellcheck`, `bash` vẫn `dirname "$(command -v …)"` — cùng hình dạng L1.
- Đột biến survival Codex lượt 1 nêu (không phải lỗi sản phẩm): tiền tố install macOS không ca nào canh (r802 parity
  bỏ mục macOS; stub brew nhận mọi lệnh); init/guard cuối/fallback `command -v`/thứ tự ứng viên không có ca riêng.
- `ops/bash_nen.py:900` `SyntaxWarning: invalid escape sequence '\('` mỗi lần nạp — lease `wp748-r18-g18`, #748.
- `t86` không cách ly khi hai suite chạy song song (xem Cổng).
- Sàn đột biến Windows còn ~0,1% dư.
