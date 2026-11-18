# WP1404 r1 — kết quả đo (executor: phiên `session_015GtxrazyAyLwN5BiEB52Sq`, Linux, 18-11-2026)

Base `e2c3b82f818bd1739d31261e8129d3ef44915acf`. Mã đo: `3d2035b366a4b157e04d08943e395117d314cd92` (commit chứa tệp này
chỉ thêm RESULTS.md, không đổi mã). Đặc tả `ops/specs/wp1404-r1.md` sha256 `1eb8f442…314d`.

## 1. Căn cứ (spec §1, nhắc lại để đối chiếu)
- Run 44347295196, job `gate-packet-loop-manh (ubuntu-latest, 2)`: `bash ops/cai_cong_cu.sh rg` ⇒
  `E: Unable to locate package ripgrep`, apt rc 100, trước mọi ca test.
- 19 lượt `gate` gần nhất: bước `cài rg…` chạy 343 lần, lỗi 1 lần.

## 2. Thay đổi
- `ops/cai_cong_cu.sh`: lần chạy công thức nằm trong `while :`; lần đầu lỗi **và** `LENH` có `apt-get install` ⇒
  `apt-get update -qq` (thêm `sudo` khi `LENH` bắt đầu `sudo apt-get`), làm rỗng `KENH_KQ`, `continue` chạy lại đúng một
  lần (`LAN_CAI -eq 1`). Update lỗi chỉ in cảnh báo. Mọi xử lý sau vòng (cờ `bat_buoc: false`, `exit "$RC_CAI"`, đọc kênh)
  không đổi.
- `.claude/dev/launcher_test.py`: `_wp831_chay_cai_rg` nhận thêm `apt_get=`/`brew=` để thay thân lệnh giả; ca
  `r1404_cai_apt_update_roi_thu_lai`; ba đột biến `cai_sh` trong `DOT_BIEN_HOOK`.

## 3. Ca `r1404_cai_apt_update_roi_thu_lai` (N1)
Chạy nguyên công thức `rg.cai.<nen>` đọc từ `ops/cong_cu.yaml`; `apt-get`/`brew` giả ghi từng đối số đầu vào nhật ký.

| Kịch bản | Kỳ vọng | Đo |
|---|---|---|
| install lỗi "Unable to locate package" tới khi `update` chạy | rc 0, `DAT`, nhật ký `install update install`, stderr có dòng thử lại | đạt |
| install luôn lỗi | rc 100, nhật ký `install update install` | đạt |
| install được ngay | nhật ký `install` | đạt |
| `macos`, `brew install` lỗi | rc 1, nhật ký apt rỗng | đạt |

`--lap-ca r1404_cai_apt_update_roi_thu_lai --lan 1`: 1/1.

## 4. Đột biến (N2)

| Đột biến | Thay đổi | Ca đích | Kết quả |
|---|---|---|---|
| `wp1404_sh_bo_thu_lai_apt` | `*"apt-get install"*)` → mẫu không bao giờ khớp | r1404 | giết 1/1 (rc 100 sau update) |
| `wp1404_sh_thu_lai_moi_loi` | `*"apt-get install"*)` → `*)` | r1404 | giết 1/1 (brew lỗi mà vẫn gọi `apt-get update`) |
| `wp1404_sh_bo_cai_lai` | bỏ `continue` | r1404 | giết 1/1 (rc 100 sau update) |

## 5. Hồi quy (N3) — hai vế dựng trong một lệnh (clone + checkout + `core.abbrev 7`)
`/tmp/.git` không tồn tại lúc đo.

| Phép đo | base `e2c3b82` | head |
|---|---|---|
| `launcher_test.py` | 424/424 (tổng 426, bỏ qua 2) | 425/425 (tổng 427, bỏ qua 2) — `3d2035b` và `6d52f57` |
| `launcher_test.py --dot-bien` | 720/720 (6 không đo được trên nền này) | `6d52f57`: **721/723** · `3d2035b`: 723/723 (cùng 6) |

Hai ca bỏ qua (`t62_…`, `r484_g4_windows_sid_alias_identity`) và sáu đột biến không đo được (nhánh Windows) giống hệt
nhau ở hai vế. Delta = +1 ca, +3 đột biến, 0 hồi quy trên `3d2035b`.

**Lỗi do chính bản vá, đã sửa:** ở `6d52f57` nhánh thử lại chép lại dòng `( set +e; eval "$LENH" ) > "$TAM_CAI/stdout"`,
nên neo của `wp868_sh_cho_eof_stdout` và `wp868_sh_go_trap_sau_eval` khớp hai chỗ và `--dot-bien` báo `SAI` (721/723).
Bộ ca thường vẫn xanh: chỉ bảng đột biến lộ ra. `3d2035b` chuyển sang vòng `while` để dòng ấy là duy nhất; đột biến
`wp1404_sh_bo_cai_lai` đổi neo sang dòng `continue`.

## 6. Khác
- `python .claude/dev/packet_loop.py doctrine-scan --root .`: sạch (12 tệp), rc 0.
- CI của PR ducthangho/tra-luat#1406 và review Codex (N4, N5): ghi ở `VERDICT.md` khi có.

## 7. Không đo được
- Runner Ubuntu thật thiếu danh sách gói: không tái lập được theo yêu cầu. Bằng chứng hành vi chỉ đến từ `apt-get` giả.
- macOS/Windows: chỉ khẳng định B3 bằng kịch bản `brew` giả trên Linux; không chạy trên nền thật.
