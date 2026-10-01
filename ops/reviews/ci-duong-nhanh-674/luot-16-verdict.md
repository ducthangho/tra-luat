Reviewed commit: f9f6fb1b746381963070f7673976e0e76998d4f3
verdict: changes_requested
reviewed_sha: f9f6fb1b746381963070f7673976e0e76998d4f3
review_class: advisory_review (reviewer cùng họ executor — Claude Opus)

> Nói thẳng: reviewer là Claude Opus 5.5 (effort max, tự khai, không có receipt runtime ⇒ model/effort thật `KHÔNG ĐO ĐƯỢC`),
> executor cũng là Claude Opus ⇒ CÙNG HỌ ⇒ lượt này là `advisory_review`, KHÔNG phải `cross_approved`. Packet `sensitive`
> vẫn cần Codex `cross_approved` hoặc `human_audited` ở cổng land.

Trạng thái: HOÀN TẤT — **changes_requested** · TONG: P0=0 P1=0 P2=0 P3=1 — 1 lớp mới của #674 (P3, tài liệu); hai lớp lượt 15
ĐÃ VÁ THẬT; lớp đã dừng S3: 0 phát hiện mới; nợ #694: 0 phát hiện tính P (1 số không neo, báo kèm). Ngưỡng chủ kho 0/0/0 ⇒ chưa đạt.

## Đối tượng (đo)
- PROMPT.md sha256 `610474bd252fd81f183f85ee442907dd38b334deb1da3161cf06b539c0ca13b3` (khớp), SPEC-r2.md sha256
  `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57` (khớp).
- `git -C cay rev-parse HEAD` ⇒ `f9f6fb1b746381963070f7673976e0e76998d4f3`; cha `b6104b02d2edddfe89a854f33db908291bec0559`;
  `origin/master` = merge-base = `20ec8d5d0e86cb7dc01f202c7596407a957e5961`.
- `git diff --numstat origin/master...f9f6fb1` ⇒ đúng 4 tệp write set:
  `1 0 .claude/dev/ci_dang_ky_test.py` · `98 8 .github/workflows/ci.yml` · `540 0 ops/ci_duong_nhanh.py` · `3135 0 ops/ci_duong_nhanh_test.py`.
- Bản vá lượt 16 (`git diff --numstat b6104b0 f9f6fb1`): `8 4 .github/workflows/ci.yml` (chỉ chú thích, H7) ·
  `43 70 ops/ci_duong_nhanh.py` · `265 163 ops/ci_duong_nhanh_test.py`. (Bản ghi đầu của dòng này chép SUY từ `--stat` —
  +46/−67, +262/−166 — và sai; đã thay bằng số đo.) Executor KHÔNG áp nguyên hint lượt 15 (hint chạy t82 qua `MA_CHAY_CA`); thay bằng `kiem_ca_chep_cay` gọi runner
  `--chi-ca=` và BỎ `kiem_symlink_treo_ca_cay`.

## Môi trường và số đo nền (HEAD f9f6fb1, chạy trong `cay/`, `TMPDIR=R/tmp`)
- Linux, 4 lõi, Python 3.11.15 (mặc định) + 3.12.3, git 2.43.0, actionlint 1.7.7, **shellcheck 0.9.0 CÓ MẶT** (nền đo mạnh),
  ruff 0.15.8 (CI ghim 0.15.15), PyYAML 6.0.1 (CI 6.0.3), jsonschema VẮNG. Không mạng GitHub, không Actions, không Windows. Chạy root.
- `git -C cay status --short --ignored` trước/sau mỗi lệnh chạy trong `cay/`: RỖNG cả hai (cây không bị chạm).

| Lệnh | Output thật |
|---|---|
| `python3 -B ops/ci_duong_nhanh_test.py` | `CA: 101/101 dat · 0 do · 0 hong` · `DOT BIEN: 301/301 bi giet dung ly do` · `KIEM KE: ca hanh_vi=73 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=9 = 101 · dot bien .claude/dev/ci_dang_ky_test.py=2 + .github/workflows/ci.yml=78 + ops/ci_duong_nhanh.py=178 + ops/ci_duong_nhanh_test.py=43 = 301` · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` · rc=0 · 90,6 s |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0 · 7,2 s |
| `actionlint .github/workflows/ci.yml` | rc=0, không finding (shellcheck có mặt) |
| `python3 -m ruff check --no-cache --select F ops/ci_duong_nhanh.py ops/ci_duong_nhanh_test.py` | `All checks passed!` rc=0 · `scripts/tl.py`: 12 lỗi F ở HEAD và 12 ở `origin/master` (tệp không đổi) ⇒ delta 0 |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | `sạch — đã quét 10 tệp, 0 chỗ chép doctrine` rc=0 |
| `git diff --numstat origin/master -- .claude/dev/ci_dang_ky_test.py` | `1 0` |
| `python3 -B ../goi/kiem_ke.py` | `CA tong: 101` (73+16+3+9) · `DOT_BIEN tong: 301` (ci_duong_nhanh.py 178 · test 43 · ci.yml 78 · ci_dang_ky_test 2) · `BO_QUA {'gate': 5, 'gate-ops': 3, 'gate-packet-loop': 1}` · ba ca dữ liệu trên kho thật `loi = [] | 5.4s` (công cụ kiểm kê chưa biết `CA_CHEP_CAY_CHUAN`, nên không đo `t82`) |

Khớp lời khai commit lượt 16 (`CA 101/101, DOT BIEN 301/301, TU KIEM DAT, TONG DAT; ci_dang_ky_test 23/23 + 1025/1025;
actionlint rc=0; ruff F sach; doctrine-scan rc=0; +1/-0`). Kiểm kê tay: đột biến 305 (g4) − 18 (bỏ `kiem_symlink_treo_ca_cay`)
+ 14 (mới, đều `_ma`) = 301 ✓ (`ops/ci_duong_nhanh.py` 182 − 18 + 14 = 178 ✓); ca 97 − 3 (`t20zi` cũ, `t20zj`, `t20zk`) + 7
(`t20zi` mới, `t20zl`, `t20zm`, `t20zn`, `t20zo`, `t20zp`, `t22c`) = 101 ✓.

## ĐỐI CHIẾU LƯỢT TRƯỚC (đột biến TỰ VIẾT, khác chữ harness; kết luận theo CA, không theo vòng đột biến của harness)
Rig: `R/tmp/mut/mut.py` + `ds_doi_chieu.py` + `chay_ca.py`. Mỗi đột biến một bản sao `copytree` riêng của clone `R/tmp/w` @
HEAD (không `.git`), neo `count == 1`, chạy MỌI 101 ca trong tiến trình (`chay_ca_trong_tien_trinh` của chính bộ test), ghi ca
ĐỎ + lý do (`[DO]` = `TinHieuChotCa` do `bang()` ném; `[HONG]` = lỗi vô can — không có cái nào). Log `R/out/mut-doi-chieu.log`.

| Lớp lượt 15 | Đột biến của tôi ⇒ CA · ca đỏ · thông điệp | Trạng thái |
|---|---|---|
| **F1** `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (cây sâu ≥ ~500 tầng) | `R3` miễn `RecursionError` sau khi chạy ⇒ 98/101, `t20zl` "cay sau 600 tang: kiem-re phai chay CHINH t82 va DO vi RecursionError, duoc []" (+ `t20zo`, `t22c` "loi phai neu dong DO cua runner") · `R6` gọi `t82` qua `-c runpy` (NÔNG hơn MỘT khung) ⇒ 97/101, `t20zn` "CI ['t01_…', 'main', '<module>'], kiem-re ['t82_…', '<module>']" (+ `t22c` argv, `t20a`, `t23`) · `R1` chạy rồi bỏ kết quả ⇒ 95/101, `t20zi` "thieu ['docs/a.md',…]" · `t20zl` · `t20zm` · `t20zp` · `t20zo` · `t22c` | **ĐÃ VÁ THẬT** — và vá RỘNG hơn hint: hai vế trên cây thật xem H5 (`sau600`) |
| F1 — đường vào mới executor tự liệt kê (`ops/leases/` biến mất) | `R4` miễn `FileNotFoundError` ⇒ 100/101, đúng MỘT ca `t20zm` "ops/leases/ bien mat: kiem-re phai chay CHINH t82 va DO vi FileNotFoundError (hong.yaml), duoc []" | có răng, đúng ca |
| F1 — symlink treo (lớp lượt 8, nay đo bằng `t82` thật) | `R5` miễn `Error: [(` (dạng `shutil.Error`) ⇒ 99/101, `t20zi` "thieu ['docs/a.md','docs/b.md','docs/lien-ket.md','docs/thu-muc','ops/reviews/l.md']" (+ `t20zp` fixture) | có răng, đúng ca |
| F1 — bằng chứng DƯƠNG của runner | `R7` coi `bỏ qua=1` là đạt ⇒ 100/101, `t22c` "rc=0 nhung 0/0 bo qua 1: phai DO" · `R8` nhận MỌI dòng `lease_publish: …` ⇒ 100/101, `t22c` (cùng thông điệp) · `R2` gọi ca KHÁC (`t23`) qua runner ⇒ 92/101, `t22c` "ca chep cay sai: 't23_…'" + `t20zi/zl/zm/zn/zp` | có răng, đúng ca |
| **F2** `chu-thich-co-san-khai-hanh-vi-cu` | Không có cổng nào canh chú thích ⇒ đột biến không áp dụng (nói thẳng: lớp này là kỷ luật đọc). Thay bằng phép đo CẤU TRÚC trên YAML/mã thật cho TỪNG mệnh đề của năm câu đã sửa (`R/tmp/f2/kiem_chu_thich.py`, log `R/out/f2-kiem-chu-thich.log`): 14/14 `DUNG` — checkout `chuan-bi` đúng một, `if` chỉ `pull_request`, không ghi đè `ref` (⇒ `github.sha`), phân loại chạy sau nó · `tl selftest (luot PR…)` mang `che_do != 'duong_nhanh'`, bước liệt kê in đúng tên nó và đứng trước MỌI bước bị bỏ (idx 9 / 34) · `gate-ops` có ĐÚNG ba bước mang `che_do` và đúng là lease-publish, cgroup, lifecycle nền · `gate-packet-loop`: bước NGAY TRÊN `packet-loop selftest` là bước liệt kê in lý do của nó · `lenh_kiem_re` gọi `kiem_mode_git`, `kiem_loai_tep`, `kiem_ca_chep_cay`; `kiem_symlink_treo_ca_cay` không còn | **ĐÃ VÁ THẬT** (5 câu: 3 câu lượt 15 + 2 câu "KHÔNG bỏ/thêm" của `gate-ops`/`gate-packet-loop` executor tự tìm) |

Tổng: 8/8 đột biến của reviewer chết ĐÚNG ca đích với thông điệp nói đúng thuộc tính bị đột biến; 0 `[HONG]` (không tín dụng giả).
Số đo ngưỡng mà docstring/ca khai, đo lại độc lập (`R/tmp/nguong/nguong.py`, bố cục `ops/reviews/zz-sau/a^N/f.md`, N=484..501,
`R/out/nguong.log`): `python3.11 runner` ĐỎ từ N=492 · `python3.11 -c MA_CHAY_CA` ĐỎ từ 492 · `python3.12 runner` ĐỎ từ 494 ·
`python3.12 -c MA_CHAY_CA` ĐỎ từ 494 (mọi ĐỎ đều `RecursionError`) ⇒ khớp "492 với 3.11.15, 494 với 3.12.3" và "hai cách gọi
TRÙNG nhau". `t82` qua runner chạy được khi PATH KHÔNG có actionlint (đúng điều kiện của bước `kiem-re` ở `gate-ops`, nơi wrapper
cài actionlint không chạy): 3.11 `[]` 1,46 s · 3.12 `[]` 1,78 s.

## BẢNG LỚP

| Slug | Gốc lớp | Biểu hiện trên f9f6fb1 | Hạng | Của ai |
|---|---|---|---|---|
| `docstring-moi-khai-rong-hon-ma` | Câu tổng quát hoá ("mọi/mỗi") MỚI viết ở lượt 16 không kiểm trên chính mã nó mô tả. Cùng HỌ với F2 lượt 15 (`chu-thich-co-san-khai-hanh-vi-cu`) nhưng khác gốc: đó là câu CŨ trôi sau khi hành vi đổi, đây là câu MỚI viết rộng hơn mã ngay lúc viết (một trong hai câu chính là câu F2 lượt 15 được viết lại). | docstring `cay_t82` (sai cho 2/5 ca dùng nó) · docstring `kiem_loai_tep` "symlink TREO ở mọi đâu trong cây" (sai cho ba lớp tên `copytree` của `t82` bỏ qua) — F1 | **P3** | **#674** |
| `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` | (F1 lượt 15) bước bù MÔ PHỎNG một phần bất biến của bước bị bỏ | **ĐÃ VÁ THẬT**: `kiem-re` chạy CHÍNH `t82` qua runner; 8/8 đột biến tự viết chết đúng ca; H2a/H2b: `t82` một mình = `t82` trong suite (0 ghi vào cây, cùng chuỗi khung, cùng ngưỡng, không phụ thuộc actionlint/actor); H5: 7 vế × mọi bước bị bỏ, tập ĐỎ của bước bị bỏ ⊆ tập lỗi `kiem-re`; 0 đường vào mới | — | #674 (đóng) |
| `chu-thich-co-san-khai-hanh-vi-cu` | (F2 lượt 15) | **ĐÃ VÁ THẬT** cho cả 5 câu (14/14 mệnh đề cấu trúc đúng); câu `kiem_loai_tep` viết lại mang một khai rộng MỚI nhỏ hơn → ghi ở lớp trên, không tính trùng | — | #674 (đóng) |
| `kiem-mode-git-chot-khong-rang` | lớp đã DỪNG theo S3 lease g4 | 0 phát hiện mới (lượt 16 không chạm `kiem_mode_git`; `t20zh` vẫn trong 101/101) | — | lớp đã dừng |
| `chot-yaml-chi-do-su-hien-dien` | nợ #694 | 0 phát hiện mới: `ci.yml` lượt 16 có cấu trúc YAML (đã parse) BẰNG HỆT g4, 12 dòng khác đều là chú thích | — | nợ #694 |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | nợ #694 | "16/16 kich ban" (docstring `t20zp` + commit) không có rig trong cây ⇒ không tái lập; "4,1 giay moi lan" là số thời gian không ghi điều kiện đo (ở đây 1,10 s) — báo, không tính P | — | nợ #694 |
| QUAN SÁT `fixture-lease-phu-thuoc-du-lieu-ho-so` | fixture "lease thật hết hạn hợp lệ" chọn từ dữ liệu hồ sơ THẬT (cùng họ `fixture-lease-phu-thuoc-actor-ci` lượt 3, nay ở chiều DỮ LIỆU) | chỉ 3/119 lease đủ điều kiện; PR làm cả 3 mất điều kiện ⇒ `ci-duong-nhanh selftest` ĐỎ ở MỌI đường (đo: `t20a`,`t20d` `KhongCoFixture`, `t23` ĐỎ). Fail-close, thông điệp rõ; lịch sử master: 0 lần xoá lease, 3 lease ấy chưa từng bị sửa, CLAUDE.md cấm viết bia mộ vào lease hết hạn ⇒ không tính P | quan sát | #674 |

## BẢNG SĂN (H1 = phần ĐỐI CHIẾU ở trên; mục ghi theo thứ tự chạy; mỗi hướng: giả thuyết / lệnh / output thật / kết luận)

### H2a — `t82` một mình (kiem-re) có thấy CÙNG cây với `t82` trong suite đầy đủ không (trạng thái do ca/bước TRƯỚC để lại)
- **Giả thuyết:** ở đường đầy đủ của `gate-ops`, `t82` chạy SAU `ci-duong-nhanh selftest`, `bien-nhan v2 selftest` và sau ~81 ca
  khác trong cùng tiến trình runner; nếu chúng GHI vào cây thật (vd tạo lại `ops/leases/`, để lại tệp/symlink), `t82` một
  mình (kiem-re) và `t82` trong suite phán trên hai cây khác nhau.
- **Lệnh:** `R/tmp/hookw/chay_audit.sh` trên clone sạch `R/tmp/w` @ HEAD, env CI (`PYTHONIOENCODING/PYTHONUTF8/
  PYTHONDONTWRITEBYTECODE`): audit hook `sitecustomize.py` (qua `PYTHONPATH`, cha + mọi con python) ghi MỌI thao tác ghi dưới
  gốc cây (`open` ghi, `os.remove/rmdir/mkdir/rename/symlink/link/chmod/utime`, `shutil.*`; `dir_fd` phân giải qua
  `/proc/self/fd`), cộng ẢNH CHỤP cây (`find -printf '%P %s %T@ %y'`, kể cả tệp ẩn, trừ `.git`) trước/sau mỗi bộ — bắt cả
  tiến trình không phải python. Đối chứng của hook: dương (cha ghi+xoá `ZZ_audit_probe`, mkdir/rmdir; con python mkdir/rmdir)
  ⇒ 6 dòng; âm (`shutil.rmtree` trong thư mục tạm có `ops/leases/x.yaml`) ⇒ 0 dòng.
- **Lỗi rig (khai):** bản hook đầu phân giải đường dẫn tương đối theo cwd trong khi `rmtree` dùng `dir_fd` ⇒ hàng nghìn dương
  tính giả (vd "`lease_publish_test.py` bị xoá ở gốc cây"); bản sửa đầu coi `dir_fd=-1` là fd thật ⇒ mất `os.remove`. Cả hai
  bị đối chứng dương bắt, đã sửa trước khi đo. Một `pkill -f` của tôi khớp chính dòng lệnh shell của tôi và giết nó (rc=144) —
  lỗi rig, không chạm cây.
- **Output thật** (`R/out/audit-ghi-tong.txt`):
```
ci_duong_nhanh_test rc=0 93s ghi_hook=0 lech_anh_chup=0
bien_nhan_v2_test   rc=0 133s ghi_hook=0 lech_anh_chup=0
lease_publish_test  rc=0 347s ghi_hook=0 lech_anh_chup=0      (lease_publish: 195/195 đạt; đã chạy=195, bỏ qua=0)
```
- **Kết luận: KHÔNG PHẢI LỖI.** Không bước/ca nào chạy trước `t82` (ở cả hai đường) ghi vào cây ⇒ `t82` một mình thấy đúng cây
  `t82` trong suite thấy. Giới hạn: tệp TẠM do tiến trình không-python tạo rồi xoá trước khi `t82` chạy thì ảnh chụp không
  thấy (hook thì thấy nếu là python).

### H2b — Tương đương MÔI TRƯỜNG giữa `t82` trong `kiem-re` và `t82` trong bước `lease-publish selftest` (độ sâu khung, trình thông dịch, env, cwd, actor)
- **Giả thuyết:** hai lời gọi khác nhau ở thứ gì đó ngoài mã — trình thông dịch, PATH, biến môi trường, cwd, độ sâu khung — nên
  một cây có thể DAT ở một đường và ĐỎ ở đường kia.
- **Lệnh + output thật:**
  · đọc `ops/chay_lease_publish_test.sh` (HEAD): `exec "${PYTHON_LEASE[@]}" "$GOC/ops/lease_publish_test.py"` với `PYTHON_LEASE`
    = `python` đầu tiên trên PATH (= `actions/setup-python` 3.12, cùng `python` mà bước `kiem-re` dùng ⇒ cùng `sys.executable`);
    wrapper thêm `PYTHONUNBUFFERED=1`, `AL_VER/AL_DICH` và actionlint vào PATH; env cấp job (`PYTHONIOENCODING`, `PYTHONUTF8`,
    `PYTHONDONTWRITEBYTECODE`) chung cho cả hai bước; cả hai thừa kế `GITHUB_ACTOR` của runner.
  · độ sâu khung: ngưỡng `RecursionError` hai cách gọi TRÙNG nhau trên cả 3.11/3.12 (bảng ở ĐỐI CHIẾU); `t20zn` ĐẠT ở nền
    (101/101) tức chuỗi khung `kiem-re` = chuỗi CI trừ tên ca; chuỗi CI thật `['t01_…', 'main', '<module>']` in ra ở đột biến `R6`.
  · PATH KHÔNG có actionlint (điều kiện thật của bước `kiem-re` ở `gate-ops`): `kiem_ca_chep_cay()` ⇒ 3.11 `[]` · 3.12 `[]`.
  · `GITHUB_ACTOR` ∈ {vắng, `ducthangho`, `notebyme88`, `github-actions[bot]`}: `chep_cay: [] | du_lieu: []` ở cả bốn.
  · trạng thái do bước/ca TRƯỚC để lại: 0 thao tác ghi dưới cây (H2a).
  · module-level của `lease_publish_test.py`: không `setrecursionlimit`, không gán `os.environ`, chỉ `t82` tự `chdir` có khôi phục
    (`grep` dòng 3198/3206).
- **Kết luận: KHÔNG PHẢI LỖI.** Trên mọi trục đo được, `t82` qua runner trong `kiem-re` phán đúng như `t82` trong suite đầy đủ.
  KHÔNG ĐO ĐƯỢC: Windows (`gate-ops` có nhãn `windows` cũng chạy `kiem-re`, mà `ci-duong-nhanh selftest` chỉ chạy Linux — xem
  KHÔNG ĐO ĐƯỢC), Python 3.12 bản vá của runner Actions (máy này 3.12.3).

### H3 — Fail-open khi đầu ra runner bị giả / bị cắt
- **Giả thuyết:** bằng chứng dương `rc == 0 and DONG_TONG_KET_MOT_CA in (x.strip() for x in dong)` có thể bị thoả mà `t82` không
  thật sự đạt.
- **Lệnh (đọc mã runner, HEAD):** `main()` của `ops/lease_publish_test.py` (dòng 11037–11083): `return 1 if hong else 0`; ca ném
  `BoQuaNen` mới vào `bo_qua` (⇒ `0/0 … bỏ qua=1`, `t22c` + đột biến `R7` của tôi đã chặn); `--chi-ca=` khớp TIỀN TỐ, không khớp
  ⇒ `RC_CHON_CA_SAI = 3`; khớp hai ca ⇒ `2/2` (`t22c`, `R8`). `t82` không ném `BoQuaNen`, không in nội dung tệp nào của cây.
  Đường dẫn trong thông điệp lỗi chỉ xuất hiện khi `t82` ĐỎ (rc=1), và tên có ký tự điều khiển đã bị bộ phân loại đẩy về `day_du`.
  Đầu ra bị cắt (mất dòng tổng kết) ⇒ ĐỎ; tiến trình bị giết ⇒ rc≠0 ⇒ ĐỎ.
- **Kết luận: KHÔNG PHẢI LỖI.** Không có đường nào để dữ liệu hồ sơ tạo `rc=0` + dòng `1/1` khi `t82` thật sự ĐỎ: `rc=0` đòi `hong`
  rỗng, và nội dung đầu ra do mã runner (ngoài allowlist) quyết định.

### H6 — Chú thích / docstring lượt 16: câu nào còn sai hoặc khai rộng hơn phép đo ⇒ **LỖI tài liệu (F1 dưới)**
- **Giả thuyết:** lượt 16 viết lại nhiều câu khai (ci.yml ×4, module, `kiem_loai_tep`, `kiem_ca_du_lieu`, `kiem_ca_chep_cay`, 8
  docstring ca mới); câu mới có thể lặp đúng lớp lượt 15 vừa sửa (khai hành vi không kiểm trên chính tệp).
- **Lệnh:** (a) năm câu ci.yml/`kiem_loai_tep` đã sửa — phép đo cấu trúc `R/tmp/f2/kiem_chu_thich.py` (14/14 `DUNG`, ở ĐỐI CHIẾU);
  (b) mọi con số mới: ngưỡng 492/494 (`nguong.py` ✓), "3 khung / 2 khung" (chuỗi khung in bởi đột biến `R6` ✓), "123 tep doi"
  (`git ls-files ops/leases | wc -l` ⇒ `123` ✓), "~120 MB" (copytree cả cây bỏ `.git` ⇒ `120.8 MB` ✓), "~6 giay" (đo 5,4 s · 5,69 s ở 3.11; 6,56 s · 6,74 s ở 3.12 ✓),
  "4,1 giay moi lan" (máy này 1,10 s cho riêng copytree — số thời gian phụ thuộc máy, không phải lời khai hành vi);
  (c) mọi câu tổng quát hoá ("mọi/mỗi/MOI") trong dòng `+` của lượt 16: `grep` rồi dựng phản chứng chạy được
  `R/tmp/f3/phan_chung_docstring.py` (log `R/out/f3-phan-chung-docstring.log`).
- **Output thật (c):**
```
(i) t20zi … chuoi ket qua kiem_ca_chep_cay = ['DAT', 'DO(1)'] | lan dau = DAT
(i) t20zl … ['DAT', 'DO(1)'] | lan dau = DAT          (i) t20zm … ['DAT', 'DO(1)'] | lan dau = DAT
(i) t20zn_ca_chep_cay_chay_cung_chuoi_khung_voi_ci: ['DO(1)'] | lan dau = DO(1)
(i) t20zp_ca_chep_cay_di_theo_buoc_bi_bo_khi_no_doi: ['DO(1)', 'DAT'] | lan dau = DO(1)
(ii) doi chung: ten thuong    docs/treo.md              treo=True -> kiem_ca_chep_cay DO
(ii) duoi __pycache__         docs/__pycache__/treo.md  treo=True -> kiem_ca_chep_cay DAT (KHONG bat)
(ii) ten *.pyc                docs/zz-treo.pyc          treo=True -> kiem_ca_chep_cay DAT (KHONG bat)
(ii) duoi .git                .git/zz-treo              treo=True -> kiem_ca_chep_cay DAT (KHONG bat)
```
- **Kết luận: LỖI tài liệu, hai câu MỚI của lượt 16** — docstring `cay_t82` khai "MOI ca dung cay nay doi doi chung DAT tren
  CHINH cay ay truoc khi them dau vao" (sai cho 2/5 ca); docstring `kiem_loai_tep` khai `t82` bắt "symlink TREO ở MỌI ĐÂU trong
  cây" (sai cho ba lớp tên mà `copytree` của `t82` bỏ qua — HÀNH VI đúng, vì đúng là thứ `t82` làm; CÂU KHAI sai). Không câu ci.yml
  nào sai. Ngoài ra (nợ #694, không tính P): "16/16 kich ban" (`t20zp`, commit) không có rig trong cây ⇒ không tái lập được.

### H4 — Đường nhanh trên LỊCH SỬ THẬT: ĐỎ oan do `t82` mới? đúng đắn phân loại? chi phí (hai vế HEAD / g4 trong CÙNG vòng lặp)
- **Giả thuyết:** `kiem_ca_chep_cay` (mới) làm ĐỎ oan PR hồ sơ hợp lệ; hoặc phân loại sai trên PR thật.
- **Lệnh:** `R/tmp/h4/h4.py` (python3.12, env CI): 60 merge first-parent gần nhất của master tính từ `20ec8d5`; với mỗi merge `M`
  (cha1 = gốc, cha2 = đầu, `M` đóng vai `github.sha`): phân loại bằng module HEAD; nếu `duong_nhanh` thì checkout `M` và chạy
  `lenh_kiem_re` của **HEAD f9f6fb1** và của **g4 b6104b0** (module trích bằng `git show`) trên CÙNG checkout, trong CÙNG vòng lặp,
  đo thời gian từng lần. Thêm ba ca KHÔNG ĐO ĐƯỢC + `push`. Log `R/out/h4-lich-su.log`.
- **Output thật:**
```
60 merge: 25 day_du (mọi PR có tệp ngoài allowlist: .github/workflows/ci.yml, ops/lease_publish*.py, scripts/tl_selftest.py, …)
          35 duong_nhanh: 25 × "HEAD rc=0 | g4 rc=0" · 10 × "HEAD rc=1 | g4 rc=1" (cả 10: kiem lease (het han) …
             TypeError: kiem() got an unexpected keyword argument 'bo_qua_han')
grep 'ca chep CA cay' (lỗi t82) = 0 dòng · grep 'ca du lieu cua lease_publish_test' = 0 dòng
kiem-re HEAD: n=35 trung vi 6.90s · g4: n=35 trung vi 5.73s · delta trung vi +1.17s   (máy đang chạy H5 song song)
thieu merge ref / merge ref khong co object / goc toan 0 -> ('day_du', 'DUONG_NHANH: KHONG DO DUOC diff … fail-close ve DAY_DU')
push -> ('day_du', "… su_kien='push' khong phai pull_request, luon DAY_DU")
```
- **Lỗi rig (khai):** 10 vế ĐỎ ở CẢ HAI module là do tôi chạy module HEAD trên CÂY CŨ: `lease_publish.py` của cây ấy chưa có tham số
  `bo_qua_han`, còn lease trong PR nay đã hết hạn nên `kiem_lease` rẽ nhánh `MA_KIEM_HET_HAN`. Trong CI thật, cây merge luôn mang
  `lease_publish.py` cùng thời với module, và lease khi ấy còn hạn (nhánh `check`). Không phải lỗi sản phẩm, không liên quan lượt 16.
- **Kết luận: KHÔNG PHẢI LỖI.** Trên 35 PR hồ sơ thật, `t82` mới KHÔNG làm đỏ thêm vế nào (rc HEAD == rc g4 ở 35/35; 0 dòng lỗi
  `t82`); 25/25 PR mã ⇒ `day_du`; KHÔNG ĐO ĐƯỢC ⇒ `day_du`. Chi phí đo được +1,17 s trung vị (khai +1,59 s: 5,54 → 7,13 s) — cùng
  bậc, sai khác nằm trong nhiễu tải; đo lại lúc máy rảnh ở H9.

### H8 — 14 đột biến MỚI của harness lượt 16: chết ĐÚNG lý do không (tín dụng giả mức 2: chết ở `bang` fixture/đối chứng thay vì `bang` thuộc tính)
- **Giả thuyết:** harness phân hạng theo TÊN ca đích (`DO:<ca>:`); một đột biến có thể làm ca đích đỏ ở `bang` đối chứng mà vẫn được
  đếm GIẾT.
- **Lệnh:** `R/tmp/mut/mut_harness.py` — lấy NGUYÊN `(tệp, hàm)` của 14 mục `DOT_BIEN` mới (tên trích từ diff `b6104b0..f9f6fb1`),
  áp lên bản sao riêng của `R/tmp/w`, chạy MỌI 101 ca, đọc thông điệp ca đích (log `R/out/mut-harness-luot16.log`); riêng mục có ca
  đích ĐẠT trong rig của tôi thì chạy lại TRONG khung harness thật (`chay_mot_dot_bien` + `chay_con`).
- **Output thật (ca đích · thông điệp):** `kiem_re_bo_ca_chep_cay` ⇒ `t20a` "phai goi lease_publish_test DUNG HAI lan" ·
  `kiem_re_nuot_loi_ca_chep_cay` / `…_ca_du_lieu` ⇒ `t20zo` "t82 DO / ca du lieu DO: kiem-re phai DO va neu dong loi ay: rc=0" ·
  `ca_chep_cay_nang_tran_de_quy` ⇒ `t20zl` "…DO vi RecursionError, duoc []" · `…_dung_lai_leases` ⇒ `t20zm` "…FileNotFoundError
  (hong.yaml), duoc []" · `…_don_symlink_treo` ⇒ `t20zi` "thieu ['docs/a.md',…]: []" · `…_them_mo_phong_symlink_treo` ⇒ `t20zp`
  "…phai DI THEO no, khong DO oan, duoc ['symlink TREO (mo phong copytree)']" · `…_qua_ma_chay_ca` / `…_qua_runpy_sau_hon` ⇒ `t20zn`
  "CI ['t01_…','main','<module>'], kiem-re ['t82_…','<module>']" / "['t82_…','main','<module>','_run_code','_run_module_code',
  'run_path','<module>']" · `…_chi_tin_rc` / `…_chi_tin_tong_ket` / `…_nuot_ngoai_le` / `…_bo_dong_do` ⇒ `t22c` đúng từng vế
  ("rc=0 dau ra rong", "rc=1 du co tong ket 1/1", "ngoai le … KHONG DO DUOC", "loi phai neu dong DO cua runner") ·
  `ca_chep_cay_cwd_sai` ⇒ rig tôi: `t22c` ĐẠT (module nạp từ chính cây test ⇒ `ROOT == ROOT_THAT`); khung harness: `GIET`, `t22c` đỏ
  ở `bang` "t82 that phai DAT tren kho that: ['… rc=0, KHONG co dong tong ket 1/1: ']" (cây tối thiểu của harness chỉ có
  `ops/lease_publish_test.py` giữ chỗ `# cho`). 0 `[HONG]` ở cả 14.
- **Kết luận: KHÔNG PHẢI LỖI.** 13/14 chết ở `bang` thuộc tính; 1/14 (`cwd_sai`) chết vì hậu quả thật của chính đột biến (chạy sai
  tệp) — và đột biến ấy TƯƠNG ĐƯƠNG trong production (`main` luôn gọi `lenh_kiem_re` với `kho=ROOT`), nên không có lỗ sản phẩm.

### H5 — Lớp `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`: bước bị bỏ KHÁC còn phán dữ liệu cây mà `kiem-re` chưa phán? (mọi vế dựng trong MỘT lệnh)
- **Giả thuyết:** các lượt trước kiểm kê bằng audit hook Python (`open/listdir/scandir`) — MÙ với phép thử TỒN TẠI (`stat`) và với
  dữ liệu đọc qua tiến trình `git`. Loại đầu vào chưa đo: PR hồ sơ XOÁ SẠCH một thư mục hồ sơ (thư mục biến mất), PR đặt MÃ vào
  hồ sơ (`.py` lỗi cú pháp, `*_test.py` hỏng, JSON hỏng, `.sh`), cây sâu 600 tầng trên CÂY THẬT với python 3.12.
- **Lệnh:** `R/tmp/h5/h5.py` — mỗi vế: clone mirror @ HEAD → nhánh `pr` áp thay đổi → commit → merge ref (`merge-tree --write-tree`
  + `commit-tree`, cha1 = gốc, cha2 = đầu) → checkout merge ref → CÙNG lệnh, CÙNG env CI (python3.12 qua shim, `core.abbrev 7`):
  phân loại · `doctrine-scan && ci_duong_nhanh.py kiem-re` · **mọi bước bị bỏ**: `tl.py --selftest` · `golden-test` ·
  `determinism-audit --strict` · `release-check --full` · `release-bundle` ×2 + so SHA-256 · `lease_publish_test.py` (suite ĐẦY ĐỦ,
  `PYTHONUNBUFFERED=1`) · `packet_loop_test.py` · rồi `gate_lifecycle_test.py` tuần tự. Log `R/out/h5/<vế>.log`.
- **Output thật (7 vế):**

| vế | phân loại | kiem-re HEAD | tl selftest | golden | determinism | release-check | bundle×2 | lease_publish (suite) | packet_loop |
|---|---|---|---|---|---|---|---|---|---|
| `nen` (+1 `ops/specs/ZZ-NEN.md`) | nhanh (1) | rc=0 DAT | rc=0 | rc=0 | rc=0 | rc=0 | rc=0 | `195/195` | rc=0 |
| `xoa_land` (xoá 59 tệp) | nhanh (59) | rc=0 DAT | rc=0 | rc=0 | rc=0 | rc=0 | rc=0 | `195/195` | rc=0 |
| `xoa_specs` (182) | nhanh | rc=1 `t23` "trỏ vào tệp không có: ops/specs/…" | rc=0 | rc=0 | rc=0 | rc=0 | rc=0 | `194/195` ĐỎ `t23` (cùng lý do) | rc=0 |
| `xoa_reviews` (1627) | nhanh | rc=1 `t26` "thiếu hẳn …/ops/reviews" | rc=0 | rc=0 | rc=0 | rc=0 | rc=0 | `193/195` ĐỎ `t26`,`t27` | rc=0 |
| `xoa_leases` (123) | nhanh | rc=1 `t82` "FileNotFoundError … ops/leases/hong.yaml" | rc=0 | rc=0 | rc=0 | rc=0 | rc=0 | `194/195` ĐỎ `t82` (cùng lý do) | rc=0 |
| `ma_trong_ho_so` (4) | nhanh | rc=0 DAT | rc=0 | rc=0 | rc=0 | rc=0 | rc=0 | `195/195` | rc=0 |
| `sau600` (cây THẬT, 600 tầng, python3.12) | nhanh (1) | rc=1 `t82` "RecursionError: maximum recursion depth exceeded" | rc=0 | rc=0 | rc=0 | rc=0 | rc=0 | `194/195` ĐỎ `t82` (cùng lý do) | rc=0 |

  Hai vế HEAD/g4 cho đường vào `xoa_leases` (MỘT lệnh, cùng checkout): `kiem-re HEAD f9f6fb1: rc=1 … t82 … FileNotFoundError` ·
  `kiem-re g4 b6104b0: rc=0 … DAT (123 tep doi, 0 loi)` ⇒ khớp lời khai `t20zm`; và `t23` KHÔNG đỏ ⇒ khớp "t23 `return` sớm".
  Bằng chứng DƯƠNG ở cả 7 vế (không tin rc): `== tl selftest 1715/1715 ==` + 0 `[FAIL]` · golden/determinism/release-check `"ok": true` ·
  bundle ×2 cùng SHA-256 (`4761688a720b…`, giống hệt ở 7 vế vì gói loại `ops/`) · `packet_loop_test` `nền: 291/291 đạt · BỎ QUA: 1` +
  `TỔNG: ĐẠT` · `gate_lifecycle_test.py` (tuần tự): `26/28 ca QUA (hong 2)` ở CẢ 7 vế, tập FAIL md5 `dddd0759` giống hệt
  (`case_interrupt_kills_tree_before_releasing_lock`, `case_ke_de_lai_lien_tuc_khong_thoat_duoc`, đều `TimeoutExpired` giết cây tiến
  trình) ⇒ đỏ NỀN của rig, delta 0. Tổng thời gian 4865 s.
- **Kết luận: KHÔNG PHẢI LỖI.** Ở mọi vế, tập bước bị bỏ ĐỎ ⊆ tập lỗi `kiem-re` (cùng ca, cùng lý do); vế nào `kiem-re` DAT thì MỌI
  bước bị bỏ đều xanh (`nen`, `xoa_land`, `ma_trong_ho_so`). F1 lượt 15 vá thật trên CÂY THẬT với 3.12 (`sau600`: `kiem-re` ĐỎ đúng
  `t82`, suite đầy đủ ĐỎ đúng `t82`). Không có đường vào mới của lớp. Giới hạn: bảy loại đầu vào, không phải mọi đầu vào.

### H9 — Chi phí khai "+1,6 s" (commit: "trung vi 5,54 s -> 7,13 s"), đo lúc máy rỗi, hai vế trong MỘT lệnh
- **Lệnh:** `R/tmp/h4/chi_phi.py 7` (python3.12, env CI) — `lenh_kiem_re` của HEAD và của g4 trên CÙNG checkout merge ref (vế `nen`
  của H5), xen kẽ thứ tự, 7 lần mỗi bên; rồi đo riêng `kiem_ca_chep_cay` và `kiem_ca_du_lieu` của HEAD. Load average lúc đo 0,10.
- **Output thật** (`R/out/chi-phi.log`):
```
kiem-re HEAD: n=7 trung vi 8.14s (min 7.86, max 8.63)
kiem-re g4  : n=7 trung vi 6.32s (min 6.12, max 6.62)
delta trung vi HEAD - g4 = +1.82s
rieng kiem_ca_chep_cay (t82 qua runner): trung vi 1.98s · kiem_ca_du_lieu: trung vi 6.74s
```
- **Kết luận: KHÔNG PHẢI LỖI.** Chi phí thêm ≈ đúng thời gian của `t82` qua runner (≈ 2 s); con số khai +1,59 s (máy/phiên bản khác:
  g4 5,54 s ở đó, 6,32 s ở đây với 3.12) cùng bậc. Lần đo dưới tải (H4) cho +1,17 s — số thời gian, không phải lời khai hành vi.

### H7 — `ci.yml` lượt 16 có thật "không đổi hành vi" không; nghiệm thu 8 (actionlint có răng) trên HEAD
- **Lệnh:** parse `ci.yml` của `b6104b0` và HEAD bằng PyYAML rồi so `==`; tập dòng khác nhau; `actionlint` trên bản sao HEAD có/không
  chèn `# chu thich co ${{ }} rong` vào thân `run:` của bước `kiem-re` (`R/tmp/al/`, log `R/out/al-dot-bien.log`).
- **Output thật:** `cau truc YAML (da parse, bo chu thich) bang nhau: True` · `so dong khac: 12 | dong khac KHONG phai chu thich: []` ·
  actionlint nền `rc=0` · đột biến `rc=1` "ci.yml:657:51: unexpected end of input while parsing variable access … [expression]".
- **Kết luận: KHÔNG PHẢI LỖI.** Lời khai commit "Khong doi hanh vi ci.yml" đúng bằng phép đo; nghiệm thu 8 giữ răng.

### H10 — Bộ test của packet có phụ thuộc DỮ LIỆU hồ sơ thật theo cách làm PR hồ sơ hợp lệ ĐỎ không ⇒ QUAN SÁT (không tính P)
- **Giả thuyết:** `lease_that_het_han_hop_le()` (từ lượt 2) chọn fixture từ `ops/leases/*.yaml` THẬT; lượt 3 đã bắt chiều ACTOR của nó
  (`fixture-lease-phu-thuoc-actor-ci`, P2, đã vá) nhưng chưa ai đo chiều DỮ LIỆU — mà dữ liệu ấy chính là thứ đường nhanh cho đổi.
- **Lệnh:** đếm lease đủ điều kiện bằng đúng vị từ của hàm (env không actor) · `R/tmp/fx/fx.py`: hai vế MỘT lệnh (`nen` / `bia_mo` =
  thêm `da_bi_thay_the` vào đúng 3 lease ấy), chạy `t20a t20d t23 t22 t22c` · lịch sử master: `git log --first-parent --diff-filter=D`
  và `-m --diff-filter=M` trên `ops/leases/*.yaml`, số commit chạm từng lease đủ điều kiện.
- **Output thật:** `so lease du dieu kien fixture: 3` · `[nen] CA: 5/5 dat` · `[bia_mo] [HONG] t20a … KhongCoFixture` · `[HONG] t20d …
  KhongCoFixture` · `[DO] t23_fixture_sach_khong_phu_thuoc_actor_ci … khong chon duoc fixture sach` · `CA: 2/5` · lịch sử: xoá lease
  `0` lần; sửa lease `8` lần (mọi lease); mỗi lease trong 3 lease ấy `1 commit` (chỉ lúc tạo).
- **Kết luận: QUAN SÁT, không tính P.** Có đường làm `ci-duong-nhanh selftest` ĐỎ ở MỌI đường (fail-close, thông điệp nói rõ), nhưng
  cần cả 3 lease mất điều kiện cùng lúc — chưa từng xảy ra, và CLAUDE.md cấm viết bia mộ vào lease đã hết hạn. Ghi để người giữ biết
  bộ test gắn vào 3 tệp hồ sơ cụ thể.

## FINDINGS

### docstring-moi-khai-rong-hon-ma [P3] (F1) Hai câu MỚI của lượt 16 khai rộng hơn mã chúng mô tả
**TỆP/DÒNG:** `ops/ci_duong_nhanh_test.py:1321-1322` (docstring `cay_t82`) · `ops/ci_duong_nhanh.py:279` (docstring `kiem_loai_tep`).

**VẤN ĐỀ:** (i) `cay_t82` khai "Moi ca dung cay nay doi doi chung DAT tren CHINH cay ay truoc khi them dau vao, nen DO chi quy duoc
cho dau vao" — đúng cho `t20zi`, `t20zl`, `t20zm` (ba ca MONG ĐỎ), SAI cho `t20zn` (đo chuỗi khung) và `t20zp` (fixture: `t82` nguyên
bản phải ĐỎ trước): lần gọi `kiem_ca_chep_cay` đầu tiên của hai ca ấy ra `DO(1)`, không có đối chứng DAT nào. (ii) `kiem_loai_tep`
(chính câu F2 lượt 15, viết lại ở lượt 16) khai `t82` trong `kiem-re` bắt "symlink TREO ở mọi đâu trong cây" — `copytree` của `t82`
bỏ qua `.git`, `__pycache__`, `*.pyc`, nên symlink treo dưới ba lớp tên ấy KHÔNG bị bắt. HÀNH VI là đúng (đi theo đúng bước bị bỏ —
mục đích của bản vá, `t20zp` khoá nó); CÂU KHAI thì sai. Bản g4 từng ghi đúng tập bỏ qua ấy (`MAU_BO_QUA_CAY` + lý do); bỏ chốt mô
phỏng thì mất luôn câu chính xác. Không đổi hành vi; không cổng nào canh docstring. Hạng P3 theo đúng thước lượt 15 (F2: câu khai sai
về hành vi trong write set); chủ kho có thể hạ thành quan sát.

**PHẢN CHỨNG** (H6 (c), `R/tmp/f3/phan_chung_docstring.py`, chạy được, chỉ đọc cây):
```
(i)  t20zn_ca_chep_cay_chay_cung_chuoi_khung_voi_ci: chuoi ket qua kiem_ca_chep_cay = ['DO(1)'] | lan dau = DO(1)
(i)  t20zp_ca_chep_cay_di_theo_buoc_bi_bo_khi_no_doi: chuoi ket qua kiem_ca_chep_cay = ['DO(1)', 'DAT'] | lan dau = DO(1)
(ii) duoi __pycache__  docs/__pycache__/treo.md  treo=True -> kiem_ca_chep_cay DAT (KHONG bat)
(ii) ten *.pyc         docs/zz-treo.pyc          treo=True -> kiem_ca_chep_cay DAT (KHONG bat)
(ii) duoi .git         .git/zz-treo              treo=True -> kiem_ca_chep_cay DAT (KHONG bat)
     doi chung         docs/treo.md              treo=True -> kiem_ca_chep_cay DO
```

**HINT** (`HINT.patch`, 2 tệp trong write set, chỉ docstring): (i) "Moi ca dung cay nay ma MONG DO doi doi chung DAT … Ca do chuoi
khung va ca doi chinh `t82` KHONG mong DO nen khong co doi chung ay (fixture cua chung la dieu kien khac)." (ii) "symlink TREO ở mọi
chỗ `copytree` của `t82` đi qua, tức TRỪ đúng các tên nó bỏ qua — `.git`, `__pycache__`, `*.pyc`".

**ĐỘT BIẾN đo răng:** không áp dụng (tài liệu; không cổng nào canh nội dung docstring — nói thẳng: lớp này là kỷ luật đọc, máy không
canh). Đo hint không làm đỏ gì (mục ĐO HINT).

**ĐỘ TIN:** cao (đo được); tác động thấp.

## ĐO HINT (`R/HINT.patch`, sha256 `56ecf4a412d88034e31b1319ac1e6959d64c6af52acb89bac689bf9cdb024fb6`, 2 tệp — đều trong write set, chỉ docstring)
| Cây | Kết quả |
|---|---|
| clone MỚI `R/tmp/ap2` từ mirror, checkout `f9f6fb1b746381963070f7673976e0e76998d4f3` | `git apply --check HINT.patch` ⇒ `APPLY_CHECK_OK`; áp xong `cmp` giống hệt bản soạn (`R/tmp/ap`); `git diff --numstat`: `2 1 ops/ci_duong_nhanh.py` · `3 2 ops/ci_duong_nhanh_test.py` |
| `python3 -B ops/ci_duong_nhanh_test.py` (đã áp) | `CA: 101/101 dat · 0 do · 0 hong` · `DOT BIEN: 301/301 bi giet dung ly do` · `KIEM KE: … = 101 · … = 301` (không đổi) · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` · rc=0 · 120 s |
| `python3 -B .claude/dev/ci_dang_ky_test.py` (đã áp) | `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0 |
| `actionlint .github/workflows/ci.yml` (shellcheck có mặt) · `ruff --select F` hai tệp · `doctrine-scan` | rc=0 · `All checks passed!` · `sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `git diff --numstat origin/master -- .claude/dev/ci_dang_ky_test.py` (đã áp) | `1 0` (hint không chạm tệp này) |
| `git status --short --ignored` sau khi chạy | chỉ 2 tệp `M` của hint, không tệp rác |
Không neo đột biến nào chứa văn bản được sửa (`grep`: hai lần khớp đều là chính docstring `cay_t82`). Hint mới chạy trên BẢN SAO;
executor phải tự áp, tự đo, tự commit.

## KHÔNG ĐO ĐƯỢC (nói thẳng)
- Chạy trên Actions thật: PR thật (nghiệm thu 11), merge ref/`github.sha` thật, bản vá Python 3.12 của runner (máy này 3.12.3),
  `timeout-minutes`, actor thật. Merge ref ở đây dựng bằng `merge-tree --write-tree` + `commit-tree`.
- **Windows:** `gate-ops` có nhãn `windows` chạy bước `kiem-re` (kể cả `kiem_ca_chep_cay`) trên Windows, mà bước
  `ci-duong-nhanh selftest` chỉ chạy Linux ⇒ hành vi `kiem_ca_chep_cay` trên Windows chưa phép đo nào chạm. Lập luận tương đương (cùng
  `t82`, cùng job, cùng env `PYTHONUTF8`) đứng được nhưng là suy luận, không phải phép đo.
- Bước cgroup thật của `gate-ops` (cần uỷ quyền cgroup + `sudo`): chỉ chạy `gate_lifecycle_test.py` không cgroup (đỏ nền 2 ca
  `TimeoutExpired` ở MỌI vế, kể cả nền — xem H5).
- G5 `cong_cu_test` / 8 mảnh `gate-cong-cu` không bị bỏ ở đường nhanh nên ngoài lớp này; không chạy. `jsonschema` vắng.
- `PYTHONPATH`/cache: không đo riêng ngoài H2b — cả hai đường thừa kế cùng env job (không `PYTHONPATH`), `-B` +
  `PYTHONDONTWRITEBYTECODE=1`, `copytree` của `t82` bỏ `__pycache__`/`*.pyc`.
- Model/effort thật của lượt review này (tự khai Opus 5.5 / max, không receipt runtime).

## TÁC ĐỘNG NGOÀI SANDBOX (khai)
- `R/cay` không bị chạm: `git -C cay status --short --ignored` RỖNG trước/sau mọi lệnh chạy trong đó. Mọi phép đo khác chạy trên
  clone/bản sao trong `R/tmp/`.
- Không lệnh nào chạy với cwd `/home/user/tra-luat`; không commit, không push, không đăng GitHub, không chạy CI.
- **Một lệnh rig có thể đã chạm tiến trình ngoài sandbox:** để dừng lượt audit hỏng đầu tiên tôi chạy `pkill -f` với mẫu
  `ops/lease_publish_test.py` — mẫu ấy khớp mọi tiến trình trên container có chuỗi đó trong dòng lệnh, kể cả ngoài `R`. Nó giết chính
  shell của tôi (rc=144). `ps` ngay sau đó chỉ còn tiến trình audit của tôi (đã dừng bằng PID); tôi KHÔNG ĐO ĐƯỢC liệu lúc ấy có tiến
  trình của phiên khác mang chuỗi ấy hay không. Từ đó chỉ dừng tiến trình theo PID.
- Một lệnh có `rm -rf` bị hệ phân quyền từ chối; làm lại bằng thư mục mới, không xoá đệ quy.

## KẾT LUẬN
`changes_requested` (ngưỡng chủ kho 0 P1 / 0 P2 / 0 P3; mức bảo đảm tối đa của lượt này là `advisory_review` vì cùng họ model —
packet `sensitive` vẫn cần Codex `cross_approved` hoặc `human_audited` ở cổng land).
- Bản vá lượt 16 ĐÃ VÁ THẬT cả hai P3 lượt 15: F1 `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (8/8 đột biến tự viết chết đúng ca; `kiem-re`
  chạy CHÍNH `t82` qua runner và — đo được — phán y hệt `t82` trong suite đầy đủ: 0 ghi vào cây trước `t82`, cùng chuỗi khung, cùng
  ngưỡng 492/494, không phụ thuộc actionlint/actor; cây thật `sau600`/`xoa_leases` ĐỎ đúng `t82` ở cả hai đường; 7 vế × mọi bước bị bỏ:
  không đường vào mới) và F2 `chu-thich-co-san-khai-hanh-vi-cu` (14/14 mệnh đề cấu trúc đúng; `ci.yml` cấu trúc không đổi).
- Đường nhanh đúng trên lịch sử thật: 35 PR hồ sơ ⇒ nhanh, `t82` mới không làm đỏ thêm vế nào (rc HEAD == rc g4 ở 35/35); 25 PR mã ⇒
  đầy đủ; KHÔNG ĐO ĐƯỢC + `push` ⇒ đầy đủ. Không fail-open khi đầu ra runner bị giả/cắt. Chi phí +1,82 s (máy rỗi, 3.12).
- 14/14 đột biến mới của harness chết ở `bang` của ca đích, 0 `[HONG]`; một mục (`ca_chep_cay_cwd_sai`) là đột biến tương đương
  trong production.
- Còn lại MỘT P3 của #674: **F1** `docstring-moi-khai-rong-hon-ma` — hai câu mới viết rộng hơn mã (docstring `cay_t82`;
  `kiem_loai_tep` "symlink TREO ở mọi đâu trong cây"); không đổi hành vi; chủ kho có thể hạ thành quan sát. `HINT.patch` sửa cả hai,
  áp sạch trên `f9f6fb1`, đã chạy: `CA 101/101 · DOT BIEN 301/301 · TONG: DAT`, registry `23/23 + 1025/1025`.
- Quan sát không tính P: fixture của bộ test gắn vào 3 lease thật (H10); "16/16 kich ban" không tái lập (nợ #694).

TONG: P0=0 P1=0 P2=0 P3=1
