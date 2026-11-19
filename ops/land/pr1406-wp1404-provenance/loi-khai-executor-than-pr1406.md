<!-- Sao nguyen van truong body cua readback-pr-1406.json (PR #1406, head c245a59). Nhan: loi_khai_co_neo. -->

Packet #1404 (r1 g1). Đặc tả đóng băng `ops/specs/wp1404-r1.md` (sha256 `1eb8f442…`, chủ kho duyệt). Lease `ops/leases/wp1404-r1-g1-claude.yaml` (`sensitive`). Trần Codex lúc đầu là 2; chủ kho nâng lên 3 rồi 4 qua hai lần Review Rescue Checkpoint.

## Vì sao
Job `gate-packet-loop-manh (ubuntu-latest, 2)` của run 44347295196 đỏ trước mọi ca test: `bash ops/cai_cong_cu.sh rg` báo `E: Unable to locate package ripgrep`. Công thức `rg.cai.linux` gọi `apt-get install` mà không chạy `apt-get update`. Trong 19 lượt `gate` gần nhất, bước cài `rg` chạy 343 lần và lỗi 1 lần.

## Thay đổi
`ops/cai_cong_cu.sh`:
- Lần chạy công thức nằm trong hàm `_wp1404_chay_cong_thuc "$@"`.
- Lần đầu lỗi **và** công thức có `apt-get install`: chạy `apt-get update -qq` một lần (có `sudo` nếu công thức có). Stdout của lệnh này đi sang stderr.
- Lần cài lại dùng kênh kết quả mới (`export -n`) và tệp stdout mới, rồi gọi hàm đúng một lần nữa.
- Nếu `update` lỗi, script vẫn cài lại; mã thoát cuối là mã của lần cài lại.
- Không đổi `ops/cong_cu.yaml`, launcher, hook phiên hay workflow.

`.claude/dev/launcher_test.py`:
- Ca `r1404_cai_apt_update_roi_thu_lai`: bốn kịch bản trên nguyên công thức YAML.
- Ca `r1404_thu_lai_chot_chi_tiet`: kịch bản (a)–(i), gồm toàn argv kèm sudo/`-qq`, stdout JSON, update lỗi, writer muộn ghi vào stdout và vào kênh, `source` từ shell gọi, allexport, tham số vị trí.
- 19 đột biến `cai_sh`.

## Đo (Linux, các vế dựng cùng cách)

| Phép đo | Base `e2c3b82` | Head `b0e9866` |
|---|---|---|
| `launcher_test.py` | 424/424 | 426/426 |
| `--dot-bien` | 720/720 | 739/739 |
| Bảng đột biến `cai_sh` | — | 67/67 |

Hai ca bỏ qua và sáu đột biến không đo được (nhánh Windows) giống nhau ở cả hai vế. `doctrine-scan` sạch. Chi tiết ở `ops/acceptance/wp1404/RESULTS.md`.

## Review
Codex qua 4 lượt, nguyên văn ở `ops/acceptance/wp1404/VERDICT.md`:
- Lượt 1–3: `request_changes`, đã xử lý từng finding.
- Lượt 4, chỉ xét delta: **`approve`** trên `0bd8edc`. Các commit sau `0bd8edc` chỉ đổi tệp hồ sơ.

## Còn mở
- **Nợ có tên `WP1404-GITHUB-PATH-LAN-LOI`** (chủ kho chọn ghi nợ): một công thức mà bộ chọn chạy xong rồi bước sau lỗi sẽ để lại thư mục của lần cài lỗi trong `GITHUB_PATH`. Mọi công thức apt hiện có đều kết thúc bằng bộ chọn, nên hiện không xảy ra.
- **CI: `gate (ubuntu-latest)` đỏ do lỗi có sẵn trên master**, không do PR này. Hai tệp `ops/land/pr1386-wp646-provenance/linux/n1env_1386.py` và `n1rig_1386.py` gọi `bash` trần. `python ops/bash_nen.py quet --root .` cho rc 2 giống hệt trên base và head. Chi tiết ở comment trên PR.

Executor không merge; chủ kho duyệt merge trên đúng SHA.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_015GtxrazyAyLwN5BiEB52Sq
