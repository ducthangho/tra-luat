# WP1404 r1 — kết quả đo (executor: phiên `session_015GtxrazyAyLwN5BiEB52Sq`, Linux, 18-11-2026)

Base `e2c3b82f818bd1739d31261e8129d3ef44915acf`. Đặc tả `ops/specs/wp1404-r1.md` sha256 `1eb8f442…314d`.
Mã đo lượt 1: `3d2035b`. Sau Codex lượt 1: `921cbb6`. Sau Codex lượt 2: `6b0e375`. Sau Codex lượt 3:
`b0e9866a8e20924f380e602719165140fdbc41eb`; các commit sau nó chỉ đổi tệp hồ sơ (RESULTS, VERDICT, lease).

## 1. Căn cứ (spec §1, nhắc lại để đối chiếu)
- Run 44347295196, job `gate-packet-loop-manh (ubuntu-latest, 2)`: `bash ops/cai_cong_cu.sh rg` ⇒
  `E: Unable to locate package ripgrep`, apt rc 100, trước mọi ca test.
- 19 lượt `gate` gần nhất: bước `cài rg…` chạy 343 lần, lỗi 1 lần.

## 2. Thay đổi
- `ops/cai_cong_cu.sh`: lần chạy công thức nằm trong hàm `_wp1404_chay_cong_thuc` (dòng `eval` duy nhất, thân không thụt
  lề); lần đầu lỗi **và** `LENH` có `apt-get install` ⇒ `apt-get update -qq` (thêm `sudo` khi `LENH` bắt đầu
  `sudo apt-get`), chuyển sang kênh MỚI `$TAM_CAI/kq-thu-lai` (`export -n`), xoá `$TAM_CAI/stdout` để lần sau mở inode
  mới, rồi gọi hàm đúng một lần nữa. Cả hai lời gọi truyền `"$@"` (công thức thấy tham số vị trí như khi `eval` nằm ngoài
  hàm). Không có biến đếm. Stdout của `update` đi sang stderr (stdout
  của script là JSON của `kiem-tra`). Update lỗi chỉ in cảnh báo. Mọi xử lý sau vòng (cờ `bat_buoc: false`,
  `exit "$RC_CAI"`, đọc kênh) không đổi.
- `.claude/dev/launcher_test.py`: `_wp831_chay_cai_rg` nhận thêm `apt_get=`/`brew=` để thay thân lệnh giả; ca
  `r1404_cai_apt_update_roi_thu_lai` và `r1404_thu_lai_chot_chi_tiet` (thêm sau Codex lượt 1, qua `_wp868_chay`);
  19 đột biến `cai_sh` trong `DOT_BIEN_HOOK`.

## 3. Ca `r1404_cai_apt_update_roi_thu_lai` (N1)
Chạy nguyên công thức `rg.cai.<nen>` đọc từ `ops/cong_cu.yaml`. `apt-get` giả ghi đối số ĐẦU (`$1`) vào nhật ký; `brew` giả
không ghi gì (ca chỉ kiểm rc và nhật ký apt rỗng). Nhật ký toàn argv và tách `sudo` nằm ở §3b.

| Kịch bản | Kỳ vọng | Đo |
|---|---|---|
| install lỗi "Unable to locate package" tới khi `update` chạy | rc 0, `DAT`, nhật ký `install update install`, stderr có dòng thử lại | đạt |
| install luôn lỗi | rc 100, nhật ký `install update install` | đạt |
| install được ngay | nhật ký `install` | đạt |
| `macos`, `brew install` lỗi | rc 1, nhật ký apt rỗng | đạt |

`--lap-ca r1404_cai_apt_update_roi_thu_lai --lan 2`: 2/2.

## 3b. Ca `r1404_thu_lai_chot_chi_tiet` (sau Codex lượt 1)

| Kịch bản | Chốt |
|---|---|
| (a) NGUYÊN `rg.cai.linux`, `sudo` giả ghi nhật ký, `update` in rác ra stdout | nhật ký đúng `sudo apt-get install -y ripgrep` · `install -y ripgrep` · `sudo apt-get update -qq` · `update -qq` · `sudo apt-get install -y ripgrep` · `install -y ripgrep`; stdout `json.loads` được; đúng MỘT dòng báo thử lại có `'rg'` và `rc=100` |
| (b) `update` rc 78, install rc 100 rồi 42 | script thoát 42; nhật ký `install update install` |
| (c1) công thức `apt-get install …` không `sudo`, update in rác | nhật ký đúng `install -y ripgrep` · `update -qq` · `install -y ripgrep`, không `sudo`; stdout `json.loads` được |
| (c2) như (c1), update rc 78, install rc 100 rồi 42 | script thoát 42; nhật ký `install update install` |
| (d) lần đầu: bộ chọn ghi kênh tới `tot2/` rồi `&& false`; sau update `tot2/rg` hỏng, lần cài lại in thư mục tốt ra stdout | `DAT` (kênh cũ không được dùng) |
| (e) probe writer muộn của Codex lượt 1 (hai tệp dấu đồng bộ; writer chỉ ghi khi đã được phép) | fixture chốt writer ĐÃ ghi; `DAT` |
| (f) probe `late_channel` của Codex lượt 2: tiến trình nền của lần đầu gọi bộ chọn, ghi KÊNH cũ sau khi lần cài lại xong | fixture chốt bộ chọn nền ĐÃ ghi; `DAT` |
| (g) probe `readonly` của Codex lượt 2: shell gọi có `readonly LAN_CAI=42`, `source` hai lượt, mỗi lượt buộc cài lại | rc 0; cả hai lượt vòng ngoài in `LAN_CAI=42`; đúng hai dòng báo thử lại |
| (h) `bash -a` (allexport), cài lại | trình cài thấy `KENH_KQ` và `TAM_CAI` VẮNG ở cả ba lời gọi |
| (i) Codex lượt 3: công thức `test "${1-}" = rg && apt-get install …`, hai stub (cài được ngay · cần update) | rc 0, `DAT`, `GITHUB_PATH` là thư mục tốt; nhật ký đúng `install` / `install update install` |

`--lap-ca r1404_thu_lai_chot_chi_tiet --lan 2`: 2/2. Phản chứng: với `ops/cai_cong_cu.sh` của `3d2035b` ca ĐỎ ở (a)
(`stdout khong con la MOT tai lieu JSON … 'update-…'`); với script của `921cbb6` ĐỎ ở (f) (rc 3); với script của `6b0e375` ĐỎ ở (i) (cài được ngay ⇒ rc 1, nhật ký
chỉ `update`).

## 4. Đột biến (N2)

| Đột biến | Thay đổi | Ca đích | Kết quả |
|---|---|---|---|
| `wp1404_sh_bo_thu_lai_apt` | `*"apt-get install"*)` → mẫu không bao giờ khớp | r1404_cai… | giết 1/1 (rc 100; update KHÔNG chạy) |
| `wp1404_sh_thu_lai_moi_loi` | `*"apt-get install"*)` → `*)` | r1404_cai… | giết 1/1 (brew lỗi mà vẫn gọi `apt-get update`) |
| `wp1404_sh_bo_cai_lai` | bỏ lời gọi hàm lần hai | r1404_cai… | giết 1/1 (rc 100 sau update) |
| `wp1404_sh_thu_lai_hai_lan` | gọi hàm hai lần ở nhánh thử lại | r1404_cai… | giết 1/1 |
| `wp1404_sh_update_vao_stdout` | bỏ `>&2` ở nhánh sudo | r1404_thu_lai… | giết 1/1, (a) JSON |
| `wp1404_sh_bo_sudo_update` | nhánh sudo gọi `apt-get update` trần | r1404_thu_lai… | giết 1/1, (a) nhật ký argv |
| `wp1404_sh_nhanh_tran_dung_sudo` | nhánh không sudo gọi `sudo` | r1404_thu_lai… | giết 1/1, (c1) |
| `wp1404_sh_update_loi_dung` | bỏ `\|\| echo …` ở nhánh sudo | r1404_thu_lai… | giết 1/1, (b) rc 78 |
| `wp1404_sh_bo_ten_rc_dong_bao` | dòng báo bỏ tên và rc | r1404_thu_lai… | giết 1/1, (a) |
| `wp1404_sh_giu_kenh_lan_dau` | giữ đường dẫn kênh cũ (chỉ làm rỗng) | r1404_thu_lai… | giết 1/1, (f) rc 3 |
| `wp1404_sh_dung_lai_inode_stdout` | bỏ `rm -f -- "$TAM_CAI/stdout"` | r1404_thu_lai… | giết 1/1, (e) rc 3 |
| `wp1404_sh_kenh_moi_khong_tao` | bỏ `: > "$KENH_KQ"` của kênh mới | r1404_thu_lai… | giết 1/1, chết ở (d) rc 7 (đọc kênh lỗi) |
| `wp1404_sh_kenh_moi_lo_export` | bỏ `export -n KENH_KQ` | r1404_thu_lai… | giết 1/1, (h) |
| `wp1404_sh_bien_dem_toan_cuc` | thêm lại `LAN_CAI=0` toàn cục | r1404_thu_lai… | giết 1/1, (g) rc 1 |
| `wp1404_sh_tran_update_vao_stdout` | nhánh gọi thẳng bỏ `>&2` | r1404_thu_lai… | giết 1/1, (c1) JSON |
| `wp1404_sh_tran_bo_qq` | nhánh gọi thẳng bỏ `-qq` | r1404_thu_lai… | giết 1/1, (c1) argv |
| `wp1404_sh_tran_update_loi_dung` | nhánh gọi thẳng bỏ `\|\| echo …` | r1404_thu_lai… | giết 1/1, (c2) rc 78 |
| `wp1404_sh_mat_tham_so_lan_dau` | lời gọi đầu bỏ `"$@"` | r1404_thu_lai… | giết 1/1, (i) cài được ngay |
| `wp1404_sh_mat_tham_so_cai_lai` | lời gọi lại bỏ `"$@"` | r1404_thu_lai… | giết 1/1, (i) cần update, rc 1 |

Mỗi đột biến của ca `r1404_thu_lai…` được chạy riêng để đọc assertion. Từng đột biến chết đúng kịch bản ghi ở cột cuối,
bằng `TinHieuChotCa`, không phải lỗi giàn. Riêng bảng `cai_sh` (mọi packet) chạy lại: `6b0e375` 65/65 · `b0e9866` 67/67.

## 5. Hồi quy (N3) — các vế dựng cùng cách (clone + checkout + `core.abbrev 7`)
`/tmp/.git` không tồn tại lúc đo.

| Phép đo | base `e2c3b82` | head |
|---|---|---|
| `launcher_test.py` | 424/424 (tổng 426, bỏ qua 2) | `6d52f57`, `3d2035b`: 425/425 (tổng 427) · `921cbb6`, `6b0e375`, `b0e9866`: 426/426 (tổng 428, bỏ qua 2) |
| `launcher_test.py --dot-bien` | 720/720 (6 không đo được trên nền này) | `6d52f57`: **721/723** · `3d2035b`: 723/723 · `921cbb6`: 731/731 · `6b0e375`: 737/737 · `b0e9866`: 739/739 (cùng 6) |

Hai ca bỏ qua (`t62_…`, `r484_g4_windows_sid_alias_identity`) và sáu đột biến không đo được (nhánh Windows) giống hệt
nhau ở mọi vế. Delta trên `b0e9866` = +2 ca, +19 đột biến, 0 hồi quy.

**Lỗi do chính bản vá, đã sửa:** ở `6d52f57` nhánh thử lại chép lại dòng `( set +e; eval "$LENH" ) > "$TAM_CAI/stdout"`,
nên neo của `wp868_sh_cho_eof_stdout` và `wp868_sh_go_trap_sau_eval` khớp hai chỗ và `--dot-bien` báo `SAI` (721/723).
Bộ ca thường vẫn xanh: chỉ bảng đột biến lộ ra. `3d2035b` chuyển sang vòng `while` để dòng ấy là duy nhất; đột biến
`wp1404_sh_bo_cai_lai` đổi neo sang dòng `continue`.

## 6. Khác
- `python .claude/dev/packet_loop.py doctrine-scan --root .`: sạch (12 tệp), rc 0.
- CI của PR ducthangho/tra-luat#1406: `gate (ubuntu-latest)` ĐỎ trên `3d2035b`, `141a3a7`, `5505f7a`. Nguyên nhân là cổng
  cây thật của `cong_cu_test` thấy hai lời gọi `bash` trần ở `ops/land/pr1386-wp646-provenance/linux/n1env_1386.py:30`
  và `n1rig_1386.py:25`. Hai tệp ấy có sẵn trên master `e2c3b82`: `python ops/bash_nen.py quet --root .` cho rc=2 với báo
  cáo giống hệt nhau trên base và head (delta 0). Lượt push master `e2c3b82` không chạy `cong_cu_test`. Hai tệp nằm ngoài
  write set; đã nêu ở comment PR. Vì vậy N4 CHƯA đạt cho tới khi master được sửa.
- Review Codex (N5): `VERDICT.md`.

## 7. Không đo được
- Nợ có tên `WP1404-GITHUB-PATH-LAN-LOI` (Codex lượt 2 P3, chủ kho chọn ghi nợ): công thức mà bộ chọn chạy xong rồi một
  bước sau lỗi để lại thư mục của lần cài lỗi trong `GITHUB_PATH`. Ca (d) dựng đúng hình dạng ấy nhưng chỉ chốt `DAT`,
  không chốt nội dung `GITHUB_PATH`. Mọi công thức apt hiện có kết thúc bằng bộ chọn.
- Runner Ubuntu thật thiếu danh sách gói: không tái lập được theo yêu cầu. Bằng chứng hành vi chỉ đến từ `apt-get` giả.
- macOS/Windows: chỉ khẳng định B3 bằng kịch bản `brew` giả trên Linux; không chạy trên nền thật.
