# Handoff wp1021 g1 — executor `claude` (phiên cloud), 30-10-2026

- Packet #1021 `BIEN-NHAN-V2-GLOB-HOA-THUONG` r2 · lease `ops/leases/wp1021-r2-g1-claude.yaml` @ `c91c1c1` (nhánh
  `ops/wp1021-r2-g1-lease`) · đặc tả `ops/specs/BIEN-NHAN-V2-GLOB-HOA-THUONG-r2.md` sha256
  `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`.
- Nhánh code `agent/wp1021-g1-claude`, head cuối **`e9e0048b48ab610fee1246368b4f134c1ac4ae76`** (base `757bde5`). PR draft #1040.
- Không merge/land/deploy (`uy_quyen_merge: false`). Không force-push, không rebase, không xoá ref.
- Tệp này nằm trên nhánh lease, KHÔNG trên nhánh code, để head mà Codex đã duyệt không đổi.

## Lịch sử nhánh code
| commit | nội dung |
|---|---|
| `99c463d` | M1/M2: helper `_chon_bien_nhan` (iterdir + so đuôi `.lower()`, không lọc `is_file`) thay hai chỗ glob ở `kiem()`/`_sinh_no()`; ca `c98`; đột biến `m142`, `m143` |
| `5efa311` | vá Codex lượt 1: lỗi liệt kê ⇒ `KhongDoDuoc` (rc=2); ca `c99`; đột biến `m144`–`m147` |
| `8d9e3e3` | vá Codex lượt 2: `_hoi_trang_thai` (lỗi `stat` của `is_dir`/`.git exists` ⇒ rc=2, chỉ `OSError`); ca `c100`; đột biến `m148`–`m153` |
| `e9e0048` | vá Codex lượt 3 (chỉ tệp test): tiêm thêm `OSError(EIO)` cạnh `PermissionError`; đột biến `m154`, `m155` |

Diff so base: `ops/bien_nhan_v2.py` +40/−5 · `ops/bien_nhan_v2_test.py` +283/−0. Đúng hai tệp write set.

## Tiêu chí — đo trên đúng `e9e0048`
- **Suite Linux (phiên này)** `python ops/bien_nhan_v2_test.py`: `97/97 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM
  đạt` · `TỔNG: ĐẠT` · rc=0.
- **C6** `python ops/bien_nhan_v2.py --root .`: `tổng 306` · `TỔNG: ĐẠT` (nền lease = 306). `--sinh-no`: `# 42 tệp`.
- **C1a/C1b/C2/C3/C9**: Codex lượt 4 đo độc lập, ĐẠT (C3 = hoàn nguyên glob ⇒ `c98` giết thật trên Linux; không vào bảng thường vì
  sống trên Windows). `rg 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` ⇒ 0 dòng. ruff `--select F` delta 0 (F541 sẵn có ở
  test, dời 1677 → 1678 vì thêm một dòng import). `doctrine-scan` sạch. `git diff --check` rc0.
- **M-2 Ubuntu** — run PR [41053943431](https://github.com/ducthangho/tra-luat/actions/runs/41053943431) `success`, mọi job nhãn
  `ubuntu-latest`, runner_id ≠ 0. Job `gate-ops (ubuntu-latest)` 124056817696: `bien_nhan_v2_test: 97/97 ca đạt · 151/151 đột biến
  thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt` · `TỔNG: ĐẠT`; `lease_publish: 268/268 đạt; đã chạy=268, bỏ qua=0`.
- **M-2 Windows** — dispatch `runner_set=windows-only` [41053942887](https://github.com/ducthangho/tra-luat/actions/runs/41053942887)
  `success`. Job `gate-ops (windows-latest)` 124057167797 (nhãn `windows-latest`, runner_id 1000026012): `bien_nhan_v2_test: 97/97
  ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt` · `TỔNG: ĐẠT`; `lease_publish: 255/255 đạt; đã chạy=255, bỏ
  qua=13` (13 ca bỏ qua có khai báo, giống run Windows trên `dbbabf9` trước packet).
- **M-4 / C7 (Windows local)**: KHÔNG chạy trong phiên này ⇒ không có lỗi local nào cần vá. Ghi rõ: C7 chưa đo.

## Cross-review Codex — 4/4 lời gọi (trần spec r2 / lease M-1)
Qua `.claude/dev/launcher.py run --require-clean --expected-head …`, lệnh `codex exec -m gpt-6-astra -c
model_reasoning_effort="xhigh" --sandbox workspace-write`. `stderr.log` của cả bốn lượt KHÔNG in header model/effort, nên model và
cường độ ở đây là GIÁ TRỊ YÊU CẦU, chưa có xác nhận từ phía chạy. Sandbox: clone thường detached + SPEC + diff + verdict lượt trước.

| lượt | run_id | prompt sha256 | head | thời lượng | verdict | VERDICT.md sha256 |
|---|---|---|---|---|---|---|
| 1 | `fe55b319aa1843f0a671fccdabc58f91` | `f333893e…4c093c` | `99c463d` | 1216,3 s, rc0 | request_changes (2 P2) | `2b624947…20fdf4` |
| 2 | `8032f63d163a457192419ffea4cdb81a` | `16e81a25…924d13` | `5efa311` | 831,5 s, rc0 | request_changes (1 P2, 1 P3) | `68b2cbe6…3827fd` |
| 3 | `af505919a7a94adba8804d9589b0339d` | `d7f60694…659e2e` | `8d9e3e3` | 899,0 s, rc0 | request_changes (1 P3) | `4c786b0d…b388b` |
| 4 | `970e84dbe41d44b2ab346259c53bc519` | `1006b62e…78ce159` | `e9e0048` | 602,5 s, rc0 | **approve**, 0 P0–P3 mở | `076ef6c8…af78482` |

Finding và cách xử lý (mọi finding mang HÌNH DẠNG `loi-do`; KHÔNG có finding `bo-chon-ung-vien` nào sau lượt 1):
- L1 P2 `loi-do-liet-ke-thu-muc-thoat-traceback`: `iterdir()` ném `EACCES` ⇒ rc=1 + traceback (glob cũ nuốt lỗi). Vá ở `5efa311`.
- L1 P2 `bo-chon-ung-vien-thieu-rang-hai-duong-goi`: ba đột biến (lọc đuôi chính xác ở `--sinh-no`, bỏ `sorted`, bỏ nhánh thư mục
  vắng) sống qua suite. Đây là hình dạng chốt dừng của spec ⇒ DỪNG hỏi chủ kho; chủ kho duyệt làm tiếp 30-10-2026. Vá ở `5efa311`.
- L2 P2 cùng slug, biểu hiện thứ hai: `Path.is_dir()` chỉ nuốt ENOENT/ENOTDIR, `EACCES` ở `stat` vẫn ném ⇒ `--sinh-no` rc=1 +
  traceback (base rc=0, tức hồi quy của packet). Vá ở `8d9e3e3`; Codex lượt 3 kiểm thêm toàn bộ bảng lời gọi hệ tệp trên hai đường.
- L2 P3 `loi-do-thieu-chot-ngoai-le-lap-trinh`: chưa ca nào đòi lỗi lập trình đi thẳng ra. Vá ở `8d9e3e3` (`c100` chốt 7).
- L3 P3 `loi-do-thieu-chot-oserror-ngoai-permissionerror`: thu hẹp phép bắt về `PermissionError` sống. Vá ở `e9e0048`.
- L4: cả ba lớp đóng; không finding mới. Hai đột biến sống mà Codex tự dựng ở lượt 4 được nó phân loại tương đương (đảo thứ tự
  factory) hoặc bị bảng đột biến bắt (đổi EIO → EACCES làm `m154`/`m155` mất răng).

**Nơi lưu verdict**: bốn tệp `VERDICT.md` và bằng chứng của reviewer CHỈ nằm trong scratchpad của phiên này (tạm, mất khi container
bị thu hồi). `ops/reviews/**` không thuộc write set nên executor KHÔNG ghi biên nhận vào kho. Bản chiếu verdict lượt 4 đăng lên PR
#1040; nếu cổng land cần biên nhận trong `ops/reviews/`, việc ấy cần lease/thẩm quyền riêng.

## Quan sát khác (ghi, KHÔNG vá)
- Clone của container mở ra nông; phải `fetch --unshallow` trước khi chạy `bien_nhan_v2.py --root .` (nông ⇒ rc=2).
- Codex lượt 3 liệt kê hai lỗi `resolve` (đường dẫn module provider; `--root` trong `main`) thoát traceback khi tiêm `OSError` — có
  sẵn ở base, ngoài write set, không tính finding của packet.
- `gate lifecycle tests` trên Windows in `16/28 ca QUA (bo qua 12, hong 0) - KHONG DU` trong bước "nền không có cgroup"; job vẫn
  `success`. Không thuộc packet này, chưa đối chiếu với master.

## Việc còn lại (không phải của executor)
- Merge/land: chủ kho.
- Biên nhận review trong `ops/reviews/` (nếu cổng land đòi): ngoài write set.
