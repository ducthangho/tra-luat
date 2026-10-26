---
verdict: approve
reviewed_sha: 9d34a8e7e97fdc8ac178fc209219cea067e4c279
spec_sha256: a98d09e86e32ee249668aaa114aed43e8a982e8bd7f9ef81fe61aa6a2a168791
so_p0: 0
so_p1: 0
so_p2: 0
so_p3: 0
---
**Kết luận: approve — 0 P0/P1/P2/P3.** F752-01, F752-02, F752-03 và 4369279124 đều ĐÃ VÁ THẬT trong phạm vi đo; 58/58 mutant suite và 9/9 mutant B3 bị bắt. Hai suite gốc 9/9 và 6/6. Verdict không chứng nhận gate tích hợp hoặc quyền land.

Bản ghi đã được bổ sung tăng dần sau mỗi bước; bản trước khi sắp lại bố cục giữ ở [VERDICT-progress.md](VERDICT-progress.md).

Lệnh preflight đầu tiên: `git rev-parse HEAD` — exit 0, stdout `9d34a8e7e97fdc8ac178fc209219cea067e4c279`, khớp chỉ thị.


Candidate/tree: `9d34a8e7e97fdc8ac178fc209219cea067e4c279` / `29f77cbd6bbad077b8f7e14dcaa067f73d83f243`. Base diff: `1797c32530fba381afd4009340a3fa558b7e37b0`; nền cố định B3: `1d7e642092fb3dda15967be44d095f37bb22ac5f`. Spec r4 đã đọc toàn bộ, băm file khớp. Hai verdict cũ đã đo băm khớp chỉ thị trước khi đọc. Diff đúng bốn tệp mới, +725/−0, dưới trần 4 tệp/1.000 dòng. Worktree ban đầu sạch, kể cả ignored; `core.abbrev=7`.

Reviewer `openai_codex / codex_cli / machine`, họ `openai`, header khai `gpt-6-astra`, effort `xhigh`, CLI `0.164.0`, session `01a17173-016f-7640-b4a3-7e572553b6a6`, run `aedfc579` (nguồn `runs/aedfc579/stderr.log`, dòng 2–13). Header không chứng minh model từng request. Executor Claude theo assignment; runtime receipt Executor chưa có. Class khai routine / hiệu lực sensitive theo spec. Không tìm được lease #752 trong mirror; generation/lease/state server chưa đo, không chứng nhận authority land. Thực hiện chỉ thị review offline exact SHA của người dùng; không chuyển state assurance. Sandbox khai workspace-write; mirror được đối xử read-only.

Skill dùng: [cross-review](../mirror/.agents/skills/cross-review/SKILL.md). Mọi cache/temp/output dưới `goi`, Python `-B`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=goi/tmp`, Git `GIT_OPTIONAL_LOCKS=0`, Ruff `--no-cache`.

Lệnh tái lập từ cwd bất kỳ (chỉ ghi trong gói; script evidence có thể cập nhật output):

```bash
G=/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review752cli3/goi
python3 -B "$G/baseline.py"
python3 -B "$G/mutations.py"
python3 -B "$G/probes.py"
python3 -B "$G/independent.py"
python3 -B "$G/additional.py"
```

## ĐỐI CHIẾU LƯỢT TRƯỚC

Hai nguồn đã đo băm trước khi dùng: `VERDICT-luot1.md` = `97b0770b08ec40889c65737163ce7dcfc55cb3740dc1abc5f009d6e529ee53e6`; `VERDICT-luot2.md` = `8410d08121342ee97c2e8f0fc8b1f7819b5f38d576f3ccfaf63d710a30163a28`. Lượt 1 neo `f9b3dc1ec11a5089b06d67a658e0f840742466eb`; lượt 2 neo `fc1bb3add70b7e7a2f17cdf4f940d7ce484b7053`.

| Finding | Đúng một trạng thái | Phép đo trên candidate |
|---|---|---|
| F752-01 | **ĐÃ VÁ THẬT** | h06/h07/h08 sửa byte tệp có sẵn lần lượt ở cả hai mode, riêng JSON, riêng chữ: đều đỏ `ca_glob_va_khong_ghi`, rc 1, 5/6. Bản giao 6/6; cả hai lượt được so nội dung. |
| F752-02 | **ĐÃ VÁ THẬT** | Probe giữ policy thật: POSIX lỗi/vắng API ⇒ đơn ca rc 1, 0/1; Windows mô phỏng lỗi/vắng API ⇒ rc 0, BO QUA, 0/0; tất cả calls=0. Toàn suite POSIX 5/6 rc 1; Windows 5/5 rc 0 kèm BO QUA. t01/t02/t03/t07/t08 đều bị bắt. Lỗi bản vá sinh ở lượt 2 được nối F752-03 bên dưới. |
| F752-03 | **ĐÃ VÁ THẬT** | t04 luôn tha, t05 không tha, t06 đảo nền, t08 return khi API vắng nay đều rc 1 và đỏ `ca_tu_kiem_bo_qua_symlink`. Ma trận 4 ô dùng policy thật; t09 gọi công cụ trước bỏ qua bị assertion GOI_CONG_CU 0 bắt. Symlink thật Linux: gọi đúng 1 lần, rc công cụ 3, KHONG_DOC_DUOC; ép trả rc 0 thì ca đỏ 0/1. |
| 4369279124 | **ĐÃ VÁ THẬT** | Tái dùng bốn fixture scalar có sẵn: thang-13, the-timestamp, the-int, long-sau. Cả bốn bản giao rc 3, JSON LOI + DAT, không traceback; catch hẹp về yaml.YAMLError đều rc 1/traceback. Mutant l01 đỏ ca scalar, 8/9. |

Lệnh: `python3 -B goi/probes.py` (driver rc 0), `python3 -B goi/mutations.py` (driver rc 0). Command subprocess, đầu ra nguyên văn và mã thoát trong [symlink-probes.json](symlink-probes.json), [scalar-probes.json](scalar-probes.json), [mutations.json](mutations.json). N/N của toàn suite bình thường có đúng một dòng; 0/0 chỉ ở đơn ca cố ý skip, không dùng làm bằng chứng B6(c). Ma trận tên nền là mô phỏng trên Linux, không phải Windows thật.

| Slug lớp | Finding nối lịch sử | Trạng thái phạm vi đã đo |
|---|---|---|
| hint-khong-ghi-chi-so-duong-dan | F752-01, lượt 1 → lượt 2 → lượt 3 | Đóng bằng ba mutant ghi byte |
| hint-symlink-skip-tinh-pass | F752-02 lượt 1; lượt 2 sinh F752-03 | Đóng hành vi/accounting và kiểm hồi quy |
| hint-symlink-tu-kiem-thay-chot-can-do | F752-03, sinh từ F752-02 ở lượt 2 | Đóng cả policy thật và nhánh API vắng, đủ 4 ô |

Lớp mở duy nhất cuối lượt 2 được đóng ở lượt 3: 1/1 = 100%; ba finding trước còn lại là kiểm lại, không cộng mẫu số. Không dùng tỷ lệ ấy thay kết quả đo trên candidate.


## Bảng đo lại

| Lệnh (cwd mirror) | rc thật và đầu ra | Đối chiếu |
|---|---|---|
| `git merge-base --is-ancestor 1797c32530fba381afd4009340a3fa558b7e37b0 9d34a8e7e97fdc8ac178fc209219cea067e4c279` | 0 · (rỗng) | đã đo |
| `git diff --check 1797c32530fba381afd4009340a3fa558b7e37b0 9d34a8e7e97fdc8ac178fc209219cea067e4c279` | 0 · (rỗng) | đã đo |
| `python3 -B ops/kiem_ho_so_land_test.py` | 0 · 9/9 | đã đo |
| `python3 -B ops/kiem_nhan_hint_test.py` | 0 · 6/6 | đã đo |
| `python3 -B ops/kiem_ho_so_land.py --root . --json` | 1 · {"n_dat": 15, "n_landed": 16, "n_mien_tru": 0, "phamvi_glob": "ops/land/*-land-evidence.yaml", "rc": 1, "len(tep)": 65} | đã đo |
| `python3 -B ops/kiem_nhan_hint.py --root . --json` | 0 · {"dem": {"CO_NHAN": 26, "KHONG_DU_DIEU_KIEN_PATCH_AS_HINT": 37, "RONG": 2, "KHONG_DOC_DUOC": 0}, "phamvi_glob": "ops/reviews/**/*HINT.patch", "rc": 0, "len(tep)": 65} | đã đo |
| `python3 -B ops/kiem_ho_so_land.py --root .` | 1 · pham vi: ops/land/*-land-evidence.yaml (không đệ quy)<br>TỔNG: 15/16 hồ sơ landed True đạt · 0 miễn trừ · rc=1 | đã đo |
| `python3 -B ops/kiem_nhan_hint.py --root .` | 0 · pham vi: ops/reviews/**/*HINT.patch<br>ĐẾM: CO_NHAN 26 · KHONG_DU_DIEU_KIEN_PATCH_AS_HINT 37 · RONG 2 · KHONG_DOC_DUOC 0 · tổng 65 · rc=0 | đã đo |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | 1 · ĐỎ: test sống chưa đăng ký: ops/kiem_ho_so_land_test.py<br>ĐỎ: test sống chưa đăng ký: ops/kiem_nhan_hint_test.py<br>ĐĂNG KÝ: 26/24<br>TRẠNG THÁI: chan=24 cach_ly=0<br>LAUNCHER WINDOWS: 4/4 hợp đồng<br>RUFF CI: 3/3 hợp đồng<br>TỔNG: ĐỎ | failed có kiểm soát: đăng ký thuộc #763 |
| `python3 -B ops/ci_duong_nhanh_test.py --mot-ca k01_so_dang_ky_nhan_muc_da_noi` | 3 · DO:k01_so_dang_ky_nhan_muc_da_noi:so dang ky phai sach, duoc ['test sống chưa đăng ký: ops/kiem_ho_so_land_test.py', 'test sống chưa đăng ký: ops/kiem_nhan_hint_test.py'] | failed có kiểm soát: đăng ký thuộc #763 |
| `ruff --version` | 0 · ruff 0.16.9 | đã đo |
| `ruff check --no-cache --select F ops/kiem_ho_so_land.py ops/kiem_ho_so_land_test.py ops/kiem_nhan_hint.py ops/kiem_nhan_hint_test.py` | 0 · All checks passed! | đã đo |
| `git remote get-url origin` | 0 · https://github.com/ducthangho/tra-luat | đã đo |
| `git --version` | 0 · git version 2.43.0 | đã đo |

Môi trường: {"platform": "Linux-6.18.44-fc-v153-x86_64-with-glibc2.39", "python": "3.11.17 (main, Oct  1 2026, 15:41:07) [GCC 13.3.0]", "executable": "/usr/local/bin/python3", "pyyaml": "6.0.1"}. Log đầy đủ/command/cwd/rc: [baseline.json](baseline.json).

### Đo độc lập B3/B5 và nghiệm thu B1–B7

`python3 -B goi/independent.py` ⇒ driver rc 0. Oracle không import công cụ packet; L-6 kiểm kiểu/độ dài/tập ký tự SHA độc lập, tiền tố/mảnh URL, trạng thái, lý do cả hai chiều và bộ đếm; L-5 kiểm nguyên văn nhãn. Đầu ra đầy đủ và các lệnh xuất blob lịch sử ở [independent.json](independent.json).

| Cây | Số tệp | DAT / landed / MIEN_TRU | F | rc công cụ | Đối chiếu |
|---|---:|---|---:|---:|---|
| mirror | 65 | 15 / 16 / 0 | 1 | 1 | khớp từng đường dẫn, trạng thái, lý do và bộ đếm |
| base | 65 | 15 / 16 / 0 | 1 | 1 | khớp từng đường dẫn, trạng thái, lý do và bộ đếm |
| base-without-F | 64 | 15 / 15 / 0 | 0 | 0 | khớp từng đường dẫn, trạng thái, lý do và bộ đếm |
| fixed | 51 | 16 / 29 / 1 | 12 | 1 | khớp từng đường dẫn, trạng thái, lý do và bộ đếm |
| fixed-without-F | 39 | 16 / 17 / 1 | 0 | 0 | khớp từng đường dẫn, trạng thái, lý do và bộ đếm |

HINT mirror: 65 tệp, `CO_NHAN=26`, `KHONG_DU_DIEU_KIEN_PATCH_AS_HINT=37`, `RONG=2`, `KHONG_DOC_DUOC=0`, rc 0; từng tệp và `dem` khớp oracle. Hai glob bằng đúng trong JSON và là token riêng ở đầu ra chữ.

Nợ dữ liệu B3 trên mirror/base: **`ops/land/pr881-wp852-land-evidence.yaml`**, trượt `authorization_url` vì thiếu mảnh L-6. Nợ đã có ở base, owner là bên ghi sổ/phiên điều phối, nằm ngoài write set #752; không tính finding mã. Nền cố định có đúng 12 tệp F; danh sách và mệnh đề trượt trong `independent.json`. Trên hai cây loại F, rc 0 và `n_dat + n_mien_tru == n_landed`. Ghim cây cố định khớp 16/29/1 và miễn trừ đúng một `pr672-wp574`.

| Tiêu chí | Phép đo và kết quả | Trạng thái |
|---|---|---|
| B1 | `ca_b1_rang_l6`: 19 fixture, đếm/lý do hai chiều; mutant SHA, khoá lồng, URL/mảnh, boolean và fallback gốc bị bắt. | passed phạm vi đã đo |
| B1b | Fail-close YAML, loại gốc/state, UTF-8/thư mục, import thiếu, cây trộn và thẻ Python có sẵn; scalar đối chứng riêng 4/4; mutant catch/ưu tiên rc bị bắt. | passed |
| B1c | SHA 41/64, repo anh em, landed số 1; mutant `{40,}`, nhận 64, bỏ dấu `/`, `!= True` đều đỏ đúng fixture. | passed |
| B2 | CLI đọc hằng thật: ca A 1 MIEN_TRU có lý do, ca B rc 3. Bỏ tồn tại/gỡ mục/thêm mục/lý do rỗng đều đỏ ca B2. | passed |
| B2b | Chỉ một tệp đúng phạm vi; *.yaml và rglob bị bắt. | passed |
| B3 | Oracle mirror/base/nền cố định, hai bản sao loại F; ghim 16/29/1, glob chữ/JSON, lý do hai chiều; 9 mutant bị oracle bác. | passed trên đầu vào land; giới hạn bản sao bên dưới |
| B4 | Các loại HINT, byte lỗi/thư mục, symlink treo; nhãn ngắn, thiếu commit, replace, OSError thoát, không strip đều bị bắt. | passed |
| B5 | CLI mirror khớp oracle 26/37/2/0, glob đúng; mutant ghi byte cả hai mode/riêng JSON/riêng chữ đỏ đúng ca. | passed |
| B6(a) | Registry rc 1, 26/24; đúng hai lỗi test sống chưa đăng ký. | failed có kiểm soát theo đường A; không finding |
| B6(b) | Ruff 0.16.9, `--no-cache --select F` bốn tệp: rc 0, All checks passed!; bản sao thêm import thừa: rc 1/F401. | passed; delta 0 so cơ sở rỗng |
| B6(c) | Hai suite rc 0, đúng một dòng 9/9 và 6/6; nhánh skip/pass có probe riêng, t01–t08 đều bị bắt. | passed |
| B6(d) | k01 riêng rc 3, chỉ hai lỗi đăng ký được phép. Full suite và Actions chưa đo. | passed đối chiếu nguyên nhân k01; phần còn lại not_run/not_measured |
| B7 | Hai công cụ × ba root sai × chữ/JSON: rc 2, không dòng đếm; bỏ guard root đỏ ca B7. | passed |

`RUFF CI: 3/3 hợp đồng` và `LAUNCHER WINDOWS: 4/4 hợp đồng` của registry là phép kiểm cấu trúc; không phải bare lint hay thực thi Windows. Bare lint được chạy riêng như bảng trên.


## Đột biến

Lệnh: `python3 -B goi/mutations.py` (từ thư mục cha mirror; hoặc dùng đường dẫn tuyệt đối). Mỗi mutant có một bản sao riêng qua `mktemp -d -p goi`; thay đúng một chốt. Mã neo/thay nguyên văn, command/rc/stdout/stderr trong [mutations.json](mutations.json). `t09` là phép đo bổ sung của reviewer, không khẳng định đồng nhất mutant thứ 9 Executor khai.

| Tên | Chốt đổi | rc · N/N · ca đỏ | Giết/sống |
|---|---|---|---|
| t01-skip-counted-pass | `bo_qua += 1` → `dat += 1` | 1 · 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: nt/loi: ['BO QUA ca_symlink_treo: PermissionError: gia lap', '1/1', 'GOI_CONG_CU 0'] | GIẾT |
| t02-skip-in-total | `tong = len(CA) - bo_qua` → `tong = len(CA)` | 1 · 0/1, 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: nt/loi: rc 1 (cần 0); BO QUA ca_symlink_treo: PermissionError: gia lap | GIẾT |
| t03-silent-skip | `print(f"BO QUA {ca.__name__}: {e}")` → `pass` | 1 · 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: nt/loi: thiếu dòng 'BO QUA ca_symlink_treo:': ['0/0', 'GOI_CONG_CU 0'] | GIẾT |
| t04-policy-always-allow | `return os.name == "nt"` → `return True` | 1 · 0/0, 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: posix/loi: rc 0 (cần 1); BO QUA ca_symlink_treo: PermissionError: gia lap | GIẾT |
| t05-policy-never-allow | `return os.name == "nt"` → `return False` | 1 · 0/1, 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: nt/loi: rc 1 (cần 0); DO ca_symlink_treo: AssertionError: nền POSIX không tạo được symlink: PermissionError: gia lap | GIẾT |
| t06-policy-inverted | `return os.name == "nt"` → `return os.name != "nt"` | 1 · 0/1, 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: nt/loi: rc 1 (cần 0); DO ca_symlink_treo: AssertionError: nền POSIX không tạo được symlink: PermissionError: gia lap | GIẾT |
| t07-early-return | `_khong_tao_duoc(f"{type(e).__name__}: {e}")` → `return` | 1 · 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: nt/loi: ['1/1', 'GOI_CONG_CU 0'] | GIẾT |
| t08-absent-symlink-pass | `_khong_tao_duoc("os.symlink vắng")` → `return` | 1 · 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: nt/vang: ['1/1', 'GOI_CONG_CU 0'] | GIẾT |
| t09-call-before-skip | `        if _cho_phep_bo_qua():` → `        _chay(Path(__file__).parent) ⏎         if _cho_phep_bo_qua():` | 1 · 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: nt/loi: công cụ bị gọi dù không tạo được symlink: ['BO QUA ca_symlink_treo: PermissionError: gia lap', '0/0', 'GOI_CONG_CU 1'] | GIẾT |
| l01-yaml-catch | `except Exception as e:` → `except yaml.YAMLError as e:` | 1 · 8/9 · DO ca_b1b_scalar_hong: AssertionError: thang-13: rc 1 (cần 3); hon3/dist-packages/yaml/constructor.py", line 330, in construct_yaml_timestamp | GIẾT |
| l02-fullmatch-to-match | `RE_SHA.fullmatch(sha)` → `RE_SHA.match(sha)` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha-lf: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l03-relax-regex | `RE_SHA = re.compile(r"[0-9a-f]{40}")` → `RE_SHA = re.compile(r"[0-9a-fA-F]{39,40}")` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha39: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l04-coerce-sha | `isinstance(sha, str) and RE_SHA.fullmatch(sha)` → `RE_SHA.fullmatch(str(sha))` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha-so: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l05-nested-keys | `    truot = [] ⏎     sha =` → `    doc = doc.get("candidates", [doc])[0] ⏎     truot = [] ⏎     sha =` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: long: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l06-no-startswith | `url.startswith(TIEN_TO_URL)` → `True` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: url-ngoai: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l07-prefix-in | `url.startswith(TIEN_TO_URL)` → `(TIEN_TO_URL in url)` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: url-nhung: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l08-no-fragment | `any(m in url for m in MANH_URL)` → `True` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: url-thieu-manh: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l09-remove-fragment-0 | `any(m in url for m in MANH_URL)` → `any(m in url for m in MANH_URL if m != '#issuecomment-')` | 1 · 5/9 · DO ca_b1_rang_l6: AssertionError: dat-ic: TRUOT (cần DAT) — trượt L-6 ở authorization_url | GIẾT |
| l09-remove-fragment-1 | `any(m in url for m in MANH_URL)` → `any(m in url for m in MANH_URL if m != '#pullrequestreview-')` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: dat-prr: TRUOT (cần DAT) — trượt L-6 ở authorization_url | GIẾT |
| l09-remove-fragment-2 | `any(m in url for m in MANH_URL)` → `any(m in url for m in MANH_URL if m != '#discussion_r')` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: dat-disc: TRUOT (cần DAT) — trượt L-6 ở authorization_url | GIẾT |
| l10-truthy | `landed is not True` → `not landed` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: boqua-chuoi: TRUOT (cần BO_QUA) — trượt L-6 ở authorized_head_sha, authorization_url | GIẾT |
| l11-equal-landed | `landed is not True` → `landed != True` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: boqua-mot: TRUOT (cần BO_QUA) — trượt L-6 ở authorized_head_sha, authorization_url | GIẾT |
| l12-no-root-landed | `doc.get("landed"), "landed (mức gốc)"` → `None, "landed (mức gốc)"` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: goc-hoa: BO_QUA (cần TRUOT) — landed (mức gốc) = None, không phải True | GIẾT |
| l13-long-sha | `RE_SHA = re.compile(r"[0-9a-f]{40}")` → `RE_SHA = re.compile(r"[0-9a-f]{40,}")` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha41: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l14-sha64 | `RE_SHA = re.compile(r"[0-9a-f]{40}")` → `RE_SHA = re.compile(r"(?:[0-9a-f]{40}\|[0-9a-f]{64})")` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha64: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l15-prefix-no-slash | `url.startswith(TIEN_TO_URL)` → `url.startswith(TIEN_TO_URL.rstrip("/"))` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: url-anh-em: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l16-rc-priority | `3 if co_loi else (1 if co_truot else 0)` → `1 if co_truot else (3 if co_loi else 0)` | 1 · 8/9 · DO ca_b1b_fail_close: AssertionError: tron: rc 1 (cần 3);  | GIẾT |
| l17-no-exemption-existence | `sorted(k for k in mien_tru if not (root / k).is_file())` → `[]` | 1 · 8/9 · DO ca_b2_mien_tru_hang: AssertionError: ca B (không có pr672) rc 0 (cần 3 — miễn trừ vắng) | GIẾT |
| l18-no-exemption | `    "ops/land/pr672-wp574-land-evidence.yaml": "hồ sơ của packet khác, ghi trước luật L-6; sửa ở packet riêng",` → `` | 1 · 8/9 · DO ca_b2_mien_tru_hang: AssertionError: ca A rc 1 (cần 0); pham vi: ops/land/*-land-evidence.yaml (không đệ quy) | GIẾT |
| l19-extra-exemption | `MIEN_TRU = {` → `MIEN_TRU = { ⏎     "ops/land/extra-land-evidence.yaml": "extra",` | 1 · 8/9 · DO ca_b2_mien_tru_hang: AssertionError: ca A rc 3 (cần 0); yaml (không đệ quy) | GIẾT |
| l20-empty-exemption-reason | `"hồ sơ của packet khác, ghi trước luật L-6; sửa ở packet riêng",` → `"",` | 1 · 8/9 · DO ca_b2_mien_tru_hang: AssertionError: ca A lý do rỗng: 'MIEN_TRU ops/land/pr672-wp574-land-evidence.yaml —  (trượt L-6 ở authorized_head_sha, authorization_url)' | GIẾT |
| l21-glob-yaml | `thu_muc.glob("*-land-evidence.yaml")` → `thu_muc.glob("*.yaml")` | 1 · 8/9 · DO ca_b2b_pham_vi: AssertionError: rc 1 (cần 0) | GIẾT |
| l22-recursive-glob | `thu_muc.glob("*-land-evidence.yaml")` → `thu_muc.rglob("*-land-evidence.yaml")` | 1 · 8/9 · DO ca_b2b_pham_vi: AssertionError: rc 1 (cần 0) | GIẾT |
| l23-empty-reason | `"trượt L-6 ở " + ", ".join(truot)` → `""` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha39: ly_do thiếu authorized_head_sha:  | GIẾT |
| l24-both-keys-reason | `"trượt L-6 ở " + ", ".join(truot)` → `"authorized_head_sha authorization_url"` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha39: ly_do nêu thừa authorization_url: authorized_head_sha authorization_url | GIẾT |
| l25-json-glob-suffix | `"phamvi_glob": PHAMVI_GLOB} ⏎  ⏎  ⏎ def main` → `"phamvi_glob": PHAMVI_GLOB + ".bak"} ⏎  ⏎  ⏎ def main` | 1 · 8/9 · DO ca_glob_token: AssertionError: ops/land/*-land-evidence.yaml.bak | GIẾT |
| l26-text-glob-suffix | `print(f"pham vi: {PHAMVI_GLOB}` → `print(f"pham vi: {PHAMVI_GLOB}.bak` | 1 · 8/9 · DO ca_glob_token: AssertionError: không có đúng một dòng mang token glob | GIẾT |
| l27-no-root-check | `if not root.is_dir() or not (root / THU_MUC).is_dir():` → `if False:` | 1 · 8/9 · DO ca_b7_root_sai: AssertionError: khong-ton-tai: rc 3 (cần 2) | GIẾT |
| h25-json-glob-suffix | `"phamvi_glob": PHAMVI_GLOB} ⏎  ⏎  ⏎ def main` → `"phamvi_glob": PHAMVI_GLOB + ".bak"} ⏎  ⏎  ⏎ def main` | 1 · 5/6 · DO ca_glob_va_khong_ghi: AssertionError: ops/reviews/**/*HINT.patch.bak | GIẾT |
| h26-text-glob-suffix | `print(f"pham vi: {PHAMVI_GLOB}` → `print(f"pham vi: {PHAMVI_GLOB}.bak` | 1 · 5/6 · DO ca_glob_va_khong_ghi: AssertionError: không có đúng một dòng mang token glob | GIẾT |
| h27-no-root-check | `if not root.is_dir() or not (root / THU_MUC).is_dir():` → `if False:` | 1 · 5/6 · DO ca_b7_root_sai: AssertionError: khong-ton-tai: rc 0 (cần 2) | GIẾT |
| h01-short-label | `if NHAN in van_ban:` → `if "chưa chạy" in van_ban:` | 1 · 5/6 · DO ca_b4_rang_l5: AssertionError: ops/reviews/b/x-HINT.patch: CO_NHAN (cần KHONG_DU_DIEU_KIEN_PATCH_AS_HINT) | GIẾT |
| h02-no-commit | `if NHAN in van_ban:` → `if NHAN.removesuffix(" commit") in van_ban:` | 1 · 5/6 · DO ca_b4_rang_l5: AssertionError: ops/reviews/c/HINT.patch: CO_NHAN (cần KHONG_DU_DIEU_KIEN_PATCH_AS_HINT) | GIẾT |
| h03-utf8-replace | `.decode("utf-8")` → `.decode("utf-8", errors="replace")` | 1 · 5/6 · DO ca_b4_rang_l5: AssertionError: ops/reviews/f/HINT.patch: KHONG_DU_DIEU_KIEN_PATCH_AS_HINT (cần KHONG_DOC_DUOC) | GIẾT |
| h04-oserror-escape | `except OSError as e:` → `except PermissionError as e:` | 1 · 4/6 · DO ca_b4_rang_l5: JSONDecodeError: Expecting value: line 1 column 1 (char 0) | GIẾT |
| h05-no-strip | `if not van_ban.strip():` → `if not van_ban:` | 1 · 5/6 · DO ca_b4_rang_l5: AssertionError: ops/reviews/e/HINT.patch: KHONG_DU_DIEU_KIEN_PATCH_AS_HINT (cần RONG) | GIẾT |
| h06-write-content | `van_ban = tep.read_bytes().decode("utf-8")` → `van_ban = tep.read_bytes().decode("utf-8") ⏎         if True: ⏎             tep.write_bytes(tep.read_bytes() + b"\n")` | 1 · 5/6 · DO ca_glob_va_khong_ghi: AssertionError: công cụ đã ghi/sửa tệp (lượt đầu ra chữ) | GIẾT |
| h07-write-json | `van_ban = tep.read_bytes().decode("utf-8")` → `van_ban = tep.read_bytes().decode("utf-8") ⏎         if "--json" in sys.argv: ⏎             tep.write_bytes(tep.read_bytes() + b"\n")` | 1 · 5/6 · DO ca_glob_va_khong_ghi: AssertionError: công cụ đã ghi/sửa tệp (lượt --json): ['ops/reviews/a/HINT.patch', 'ops/reviews/b/x-HINT.patch'] | GIẾT |
| h08-write-text | `van_ban = tep.read_bytes().decode("utf-8")` → `van_ban = tep.read_bytes().decode("utf-8") ⏎         if "--json" not in sys.argv: ⏎             tep.write_bytes(tep.read_bytes() + b"\n")` | 1 · 5/6 · DO ca_glob_va_khong_ghi: AssertionError: công cụ đã ghi/sửa tệp (lượt đầu ra chữ) | GIẾT |

Đã hoàn tất 49 mutant suite; giết 49, sống 0.

### B3: phản chứng bằng oracle độc lập

Lệnh `python3 -B goi/independent.py`; từng mutant thay một chốt trên bản sao. “Giết” là oracle bác đúng vi phạm, không phải suy từ rc khác 0. Baseline trên cùng cây đạt; [b3-mutants.json](b3-mutants.json) giữ nguyên command/rc/stdout/stderr và neo/thay.

| Tên | Chốt đổi | rc công cụ · phép kiểm đỏ | Kết quả |
|---|---|---|---|
| b3-no-fragment | `any(m in url for m in MANH_URL)` → `True` | 0 · rc differs; n_dat: 28 != 16 | GIẾT |
| b3-only-pull | `url.startswith(TIEN_TO_URL)` → `url.startswith(TIEN_TO_URL + "pull/")` | 1 · rc differs; n_dat: 14 != 16 | GIẾT |
| b3-glob-yaml | `thu_muc.glob("*-land-evidence.yaml")` → `thu_muc.glob("*.yaml")` | 0 · paths differ ['ops/land/pr666-wp650-provenance.yaml']; len(tep) differs | GIẾT |
| b3-no-exemption | `    "ops/land/pr672-wp574-land-evidence.yaml": "hồ sơ của packet khác, ghi trước luật L-6; sửa ở packet riêng",` → `` | 1 · n_mien_tru: 0 != 1; ops/land/pr672-wp574-land-evidence.yaml: status differs | GIẾT |
| b3-add-F-exemptions | `MIEN_TRU = {` → `MIEN_TRU = { ⏎     'ops/land/pr779-wp775-land-evidence.yaml': "extra", ⏎     'ops/land/pr791-wp782-land-evidence.yaml': "extra", ⏎     'ops/land/pr792-wp484-land-evidence.yaml': "extra", ⏎     'ops/land/pr793-wp784-land-evidence.yaml': "extra", ⏎     'ops/land/pr800-wp794-land-evidence.yaml': "extra", ⏎     'ops/land/pr801-wp795-land-evidence.yaml': "extra", ⏎     'ops/land/pr818-wp788-land-evidence.yaml': "extra", ⏎     'ops/land/pr823-wp802-land-evidence.yaml': "extra", ⏎     'ops/land/pr832-wp831-land-evidence.yaml': "extra", ⏎     'ops/land/pr836-wp812-land-evidence.yaml': "extra", ⏎     'ops/land/pr848-wp744-land-evidence.yaml': "extra", ⏎     'ops/land/pr873-wp868-land-evidence.yaml': "extra", ⏎ ` | 0 · rc differs; n_mien_tru: 13 != 1 | GIẾT |
| b3-undercount | `return rc, {"tep": tep_list, "n_dat": n_dat, "n_landed": n_landed,` → `return rc, {"tep": tep_list, "n_dat": n_dat - 2, "n_landed": n_landed - 2,` | 1 · n_dat: 14 != 16; n_landed: 27 != 29 | GIẾT |
| b3-empty-reason | `"trượt L-6 ở " + ", ".join(truot)` → `""` | 1 · ops/land/pr779-wp775-land-evidence.yaml: wrong reason authorization_url; ops/land/pr791-wp782-land-evidence.yaml: wrong reason authorization_url | GIẾT |
| b3-wrong-reason | `"trượt L-6 ở " + ", ".join(truot)` → `"authorized_head_sha"` | 1 · ops/land/pr779-wp775-land-evidence.yaml: wrong reason authorized_head_sha; ops/land/pr779-wp775-land-evidence.yaml: wrong reason authorization_url | GIẾT |
| b3-both-keys-reason | `"trượt L-6 ở " + ", ".join(truot)` → `"authorized_head_sha authorization_url"` | 1 · ops/land/pr779-wp775-land-evidence.yaml: wrong reason authorized_head_sha; ops/land/pr791-wp782-land-evidence.yaml: wrong reason authorized_head_sha | GIẾT |

### B1/B1b bổ sung và kiểm proxy

`python3 -B goi/additional.py` ⇒ driver rc 0; chín mutant bổ sung đều bị bắt. Chỉ tái dùng fixture của candidate, gồm thẻ Python sẵn có; không soạn tải trọng mới. Đầu ra, neo/thay và command/rc đầy đủ: [additional-mutants.json](additional-mutants.json).

| Tên | Chốt đổi | rc · N/N · ca đỏ | Kết quả |
|---|---|---|---|
| l28-match-dollar | `RE_SHA.fullmatch(sha)` → `re.match(r"[0-9a-f]{40}$", sha)` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha-lf: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l29-in-without-scheme | `url.startswith(TIEN_TO_URL)` → `(TIEN_TO_URL.removeprefix("https://") in url)` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: url-gia: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l30-in-without-host | `url.startswith(TIEN_TO_URL)` → `("ducthangho/tra-luat" in url)` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: url-ngoai: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l31-no-sha-type | `isinstance(sha, str) and RE_SHA.fullmatch(sha)` → `RE_SHA.fullmatch(sha)` | 1 · 6/9 · DO ca_b1_rang_l6: TypeError: 'NoneType' object is not subscriptable | GIẾT |
| l32-swallow-yaml | `return "LOI", f"YAML không đọc được ({type(e).__name__})", False` → `return "BO_QUA", "YAML bỏ qua", False` | 1 · 6/9 · DO ca_b1b_fail_close: AssertionError: yaml-ngoac: rc 0 (cần 3);  | GIẾT |
| l33-unsafe-loader | `doc = yaml.safe_load(van_ban)` → `doc = yaml.unsafe_load(van_ban)` | 1 · 8/9 · DO ca_b1b_the_python: AssertionError: rc 0 (cần 3) | GIẾT |
| l34-root-none-escape | `if not isinstance(doc, dict):` → `if doc is not None and not isinstance(doc, dict):` | 1 · 8/9 · DO ca_b1b_fail_close: AssertionError: rong: rc 1 (cần 3); w752cli3/goi/mut-Sc4aGNem/ops/kiem_ho_so_land.py", line 68, in _xet_mot_tep | GIẾT |
| l35-invalid-state-skip | `return "LOI", f"trang_thai_packet không phải ánh xạ ({type(tp).__name__})", False` → `return "BO_QUA", "state vắng", False` | 1 · 8/9 · DO ca_b1b_fail_close: AssertionError: tp-chuoi: rc 0 (cần 3);  | GIẾT |
| l36-missing-yaml-rc0 | `return 3, {"loi": "thiếu PyYAML"` → `return 0, {"loi": "thiếu PyYAML"` | 1 · 8/9 · DO ca_b1b_thieu_pyyaml: AssertionError: rc 0 (cần 3, tiêm miễn trừ {});  | GIẾT |

Tổng **58/58 mutant suite bị giết**, **9/9 mutant B3 bị oracle bác**, **0 sống** trong tập đã chạy. Riêng t01–t08 tái lập đúng các chốt của lượt 2; t09 là probe bổ sung gọi công cụ trước khi skip. Mutant chết do hồi quy của công cụ làm không có JSON (`h04`, `l31`) được phân biệt với lỗi setup; không mutant nào chết do import/fixture/permission ngoài chốt đã tiêm.

Đã quan sát trực tiếp bốn subprocess THẬT của `ca_tu_kiem_bo_qua_symlink`: đúng 4 ô, thứ tự nt/lỗi, nt/vắng, posix/lỗi, posix/vắng; hai ô POSIX đỏ vì đúng AssertionError từ `_khong_tao_duoc`, không phải proxy thiếu thuộc tính khác. Hai ô Windows mô phỏng báo BO QUA đúng nguyên nhân. Cả bốn có GOI_CONG_CU 0, stderr rỗng; policy vẫn là object hàm ban đầu và os toàn cục không đổi. Evidence [selfcheck-children.json](selfcheck-children.json). Probe độc lập chỉ ghi nhận truy cập `name`/`symlink` ở đường này, không thấy thuộc tính bị proxy che ngoài phạm vi; ca thật Linux vẫn qua `_chay` một lần và đòi rc 3. Không phát hiện biểu hiện mới của lớp “ca tuyên bố đo nhưng không đo” trong phạm vi ấy.


## Findings

Không có finding mới P0/P1/P2/P3 trong phạm vi đã đo. Bốn finding được yêu cầu đối chiếu đều **ĐÃ VÁ THẬT**. Nợ dữ liệu land và lỗi đăng ký test theo đường A đã tách riêng ở bảng nghiệm thu; không tính chúng là lỗi mã #752.

Kết luận nội dung: **approve** trên exact candidate này, **0 P0 · 0 P1 · 0 P2 · 0 P3**. Không tạo authority merge/land hoặc chuyển state `cross_approved`.

## chua_do_duoc

- **not_measured:** Windows thật. Tên nền nt/posix trong probe là mô phỏng nhánh Python trên Linux; không xác nhận quyền symlink hay hành vi pathlib Windows thật. Symlink treo THẬT chỉ được đo trên Linux.
- **not_measured:** remote head, CI GitHub run/attempt/checkout/workflow provenance, generation/hạn lease, runtime receipt Executor, GitHub submitter, approval/land. Chỉ thị cấm mạng; lượt này không chứng nhận các điều kiện ấy. Header CLI chỉ công bố model/effort, không chứng minh từng request. Rc/trạng thái launcher của lượt đang chạy phải được bên vận chuyển đọc sau khi tiến trình kết thúc.
- **not_run:** full `ops/ci_duong_nhanh_test.py` và registry `--chay`. Full suite dựng/thay Git ref; chỉ thị cấm sửa ref nên chỉ đo registry không `--chay` và k01 riêng. Không suy từ k01 rằng mọi ca còn lại đều xanh; B6(d) toàn phần chưa đo. Release/LIVE/deploy không chạy.
- **failed có kiểm soát:** registry rc 1 và k01 riêng rc 3 (mã của chế độ đơn ca), đúng lỗi hai test chưa đăng ký. Không gọi các gate ấy là passed; gate xanh tích hợp thuộc #763. Không có skipped trên hai suite gốc Linux; skip chỉ phát sinh có chủ đích ở probe Windows mô phỏng và được ghi BO QUA, không tính đạt.
- **Giới hạn B3:** cây lịch sử và cây loại F là bản sao đầu vào YAML mức đỉnh `ops/land` (có provenance ngoài glob để phản chứng), không full clone toàn repository. Đã đo toàn bộ đầu vào cần phân loại/đếm, nhưng không chứng nhận mọi tệp ngoài đầu vào bất biến trên một full clone. Oracle không import mã packet; hai script/output được băm bên dưới.
- **Giới hạn phản chứng:** 58 mutant suite + 9 mutant B3 nêu trên, không tuyên bố phủ mọi lỗi có thể có. Theo mục 5 chỉ thị, các hướng cần soạn đường dẫn thoát cây hoặc tải trọng mới chỉ mô tả bằng lời để điều phối tự viết: mục được glob chọn dẫn ra ngoài root; tệp đặc biệt làm đọc bị chặn; đầu vào gây cạn tài nguyên. Lượt này không dựng các hướng ấy.
- **Giới hạn snapshot:** đầu/cuối cùng HEAD/tree, diff/index rỗng, tracked/untracked sạch. Snapshot lúc 05:14:18Z còn khớp toàn bộ mốc đầu; kiểm tra sau khi sắp lại verdict thấy ignored `.codex/` mới xuất hiện. Đã ghi lại snapshot cuối; không đọc nội dung `.codex/`, không có lệnh reviewer ghi vào đó, nguồn tạo **not_measured**. Do đó không khai ignored bất biến. Hash 135 tệp (4 tệp packet, 65 land, 65 HINT, spec) giống nhau. Spec file/blob đều khớp băm đóng băng. Không đọc tệp bí mật, không băm toàn bộ nội dung kho hoặc repo nguồn Executor ngoài mirror. Snapshot chỉ chứng minh không có delta quan sát được ở hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. [final-integrity.json](final-integrity.json) ghi thời điểm/lệnh/rc.

Mọi driver đo kể trên kết thúc rc 0; rc của từng tiến trình con được giữ riêng trong evidence, kể cả rc 1/2/3 được mong đợi. Không dùng rc driver để đổi một phép đo failed/not_run thành pass.


Artifact và SHA-256 (định danh bytes của đúng lượt này):

| Artifact | SHA-256 |
|---|---|
| [reviewlib.py](reviewlib.py) | `5848db32b67e8fae6c64a12ec68f7b2015abff2ef4bb9b911811d1d5e87ce525` |
| [baseline.py](baseline.py) | `6fb9a7b2fbd6e837207e8fadae4d78c3f0fed73ce041d17acb4e8d129eaa969d` |
| [baseline.json](baseline.json) | `e5efba0d25625da65e37632f357a9581278ef942ff82afa864b5f39511402aba` |
| [mutations.py](mutations.py) | `93fde6b5ce61f8c9916d4e34a129a55a517bfd9b21680d869145668c19923f1c` |
| [mutations.json](mutations.json) | `a000281e7396ddad3f7611b98897450f35dff2a5632f0f0eda1406fb6774f54f` |
| [probes.py](probes.py) | `78b5a993d045182e9e4ec6f7911701ee1c5be2f92796b846046447ca6ad98c8f` |
| [symlink-probes.json](symlink-probes.json) | `fde4f3c1d8931e7c2e9b268440ba8c536087a24de04fe5d8af18f41b5d516a4a` |
| [scalar-probes.json](scalar-probes.json) | `46f99e40be23eb1f7d50e6d2abfdf20b8a3a2b83c4559c4c8de23185c4574033` |
| [independent.py](independent.py) | `b1c9269b10f2f2268849c1897fd95b93d7be933d61a36598fd29c19205e1d999` |
| [independent.json](independent.json) | `723f668e20cf5428541ce6a4d76e947df3b83aed72775af4efa8b5f62097bd46` |
| [b3-mutants.json](b3-mutants.json) | `037fc675136791c346953cf0a015b0f4dd503e74cc0e64046667f8ef9ad06a25` |
| [ruff-negative.json](ruff-negative.json) | `4f79ef6a3b1a089a79ffdfac057a01afa3e0a15642f7526e5338fbd5b81e2ad2` |
| [additional.py](additional.py) | `f768434641ada7e96bc61c76d35dfc4fe21560f243bc6dad1733bfeeb0841024` |
| [additional-mutants.json](additional-mutants.json) | `49283ea5bf1ceea49bc86d0d6ed0186ca878d86cbe7fa569ad7b7fa0f966c26c` |
| [selfcheck-children.json](selfcheck-children.json) | `5794d8e84585cdc60d60a9a4dbf2526e78f1e80314f65cc4115a26fef81f3163` |
| [snapshot-before.json](snapshot-before.json) | `1dc80741b322412f938981bd28556d3f21cbc33718820ef30ba2170a4c822c91` |
| [snapshot-after.json](snapshot-after.json) | `1dc80741b322412f938981bd28556d3f21cbc33718820ef30ba2170a4c822c91` |
| [final-integrity.json](final-integrity.json) | `482382d8264a35e16257e5f3303d8dee8765f7f716a5b94ef3bcf2c962582315` |
| [VERDICT-progress.md](VERDICT-progress.md) | `c7439cebefbbfa8768cf17c866d0c3f69262555679397781db671dcb7dcdb510` |
| [snapshot-before-late-ignored.json](snapshot-before-late-ignored.json) | `1dc80741b322412f938981bd28556d3f21cbc33718820ef30ba2170a4c822c91` |
