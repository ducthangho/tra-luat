Reviewed commit: b6104b02d2edddfe89a854f33db908291bec0559
verdict: changes_requested
reviewed_sha: b6104b02d2edddfe89a854f33db908291bec0559
review_class: advisory_review (reviewer cùng họ executor — Claude Opus)

> Nói thẳng: reviewer là Claude Opus 5.5 (effort max, tự khai, không có receipt runtime ⇒ model/effort thật `KHÔNG ĐO ĐƯỢC`),
> executor cũng là Claude Opus ⇒ CÙNG HỌ ⇒ lượt này là `advisory_review`, KHÔNG phải `cross_approved`. Packet `sensitive`
> vẫn cần Codex `cross_approved` hoặc `human_audited` ở cổng land.

Trạng thái: HOÀN TẤT — **changes_requested** · TONG: P0=0 P1=0 P2=0 P3=2 — 2 lớp mới của #674 (cả hai P3); lớp đã dừng S3: 0 phát
hiện mới; nợ #694: 0 phát hiện tính P (1 trôi số báo kèm, H6). Ngưỡng chủ kho 0/0/0 ⇒ chưa đạt.

## Đối tượng (đo)
- `git -C cay rev-parse HEAD` ⇒ `b6104b02d2edddfe89a854f33db908291bec0559`; cha `a78a82a` (merge master `20ec8d5`); `git status --short` rỗng.
- `git diff --numstat origin/master...b6104b0` ⇒ đúng 4 tệp write set:
  `1 0 .claude/dev/ci_dang_ky_test.py` · `90 4 .github/workflows/ci.yml` · `567 0 ops/ci_duong_nhanh.py` · `3033 0 ops/ci_duong_nhanh_test.py`.
- Bản vá g4 (`a78a82a..b6104b0`): chỉ `ops/ci_duong_nhanh.py` (+66/−2) và `ops/ci_duong_nhanh_test.py` (+275/−13).
- PROMPT.md sha256 `e8d68e36…5cab` (khớp), SPEC-r2.md sha256 `b6e719c9…da57` (khớp).

## Môi trường và số đo nền (HEAD b6104b0, chạy trong `cay/`, `TMPDIR=R/tmp`)
- Linux, Python 3.11.15, git 2.43.0, actionlint 1.7.7, **shellcheck 0.9.0 CÓ MẶT** (nền đo mạnh), ruff 0.15.15, PyYAML 6.0.1
  (CI ghim 6.0.3), jsonschema VẮNG. Không mạng GitHub, không Actions, không Windows. Chạy root (nhánh lỗi-quyền thật không đo được).
- Sau mỗi lệnh chạy trong `cay/`: `git -C cay status --short --ignored` ⇒ RỖNG (cây không bị chạm).

| Lệnh | Output thật |
|---|---|
| `python3 -B ops/ci_duong_nhanh_test.py` | `CA: 97/97 dat · 0 do · 0 hong` · `DOT BIEN: 305/305 bi giet dung ly do` · `KIEM KE: ca hanh_vi=69 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=9 = 97 · dot bien .claude/dev/ci_dang_ky_test.py=2 + .github/workflows/ci.yml=78 + ops/ci_duong_nhanh.py=182 + ops/ci_duong_nhanh_test.py=43 = 305` · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` · rc=0 · 1m28s |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0 · 7,1s |
| `actionlint .github/workflows/ci.yml` | rc=0, không finding (shellcheck có mặt) |
| `python3 -m ruff check --no-cache --select F ops/ci_duong_nhanh.py ops/ci_duong_nhanh_test.py` | `All checks passed!` rc=0 · (`scripts/tl.py` 12 lỗi F = nền, packet không chạm tl.py) |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | `sạch — đã quét 10 tệp, 0 chỗ chép doctrine` rc=0 |
| chi phí `kiem_symlink_treo_ca_cay(cay)` (đếm `os.scandir`, `R/tmp/do_chi_phi.py`) | `loi=[]` · 147 lần scandir · 0,013 s |
| `git ls-files -s` trên head: mode 120000/160000 | 0 mục |

Khớp lời khai của commit g4 (`CA 97/97, DOT BIEN 305/305, TU KIEM DAT, TONG DAT; ci_dang_ky_test 23/23 + 1025/1025; actionlint rc=0;
ruff F sach; doctrine-scan rc=0`). Kiểm kê số đột biến g4 thêm (đếm tay từ diff): lớp #668 = 11, lớp symlink-cả-cây = 18,
lớp mode-git = 3, F-B = 4 ⇒ 36; 269 + 36 = 305 ✓; ca 93 + 4 (`t20zh/zi/zj/zk`) = 97 ✓.

## ĐỐI CHIẾU LƯỢT TRƯỚC (đột biến TỰ VIẾT, khác chữ harness; kết luận theo CA, không theo vòng đột biến của harness)
Rig: `R/tmp/mut/mut.py` + `ds_dot_bien.py` + `chay_ca.py`. Mỗi đột biến một bản sao `cp` riêng của clone `R/tmp/w` @ b6104b0
(không `.git`), neo `count == 1`, chạy MỌI 97 ca trong tiến trình (`chay_ca_trong_tien_trinh` của chính bộ test), ghi ca
ĐỎ + lý do (`[DO]` = `TinHieuChotCa` do `bang()` ném; `[HONG]` = lỗi vô can — không có cái nào). Log: `R/out/mut-doi-chieu.log`.
"Chết đúng ca đích" = ca đích ra `[DO]` với thông điệp nói ĐÚNG thuộc tính bị đột biến (đọc từng dòng dưới).

| Lớp lượt trước | Đột biến của tôi ⇒ kết quả (CA) · ca đỏ · thông điệp | Trạng thái |
|---|---|---|
| **P2 lượt 8** `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (symlink TREO ngoài diff) | `R1` `exists`→`lexists` ⇒ 95/97, `t20zi` "thieu ['docs/a.md',…,'ops/reviews/l.md']: rc=0" + `t20zj` "doi chung treo … duoc []" · `R2` thêm `"docs"` vào `MAU_BO_QUA_CAY` ⇒ 94/97, `t20zi` (thiếu 4 đường `docs/`) + `t20zj` + `t20zk` · `R3` `is_dir() and not is_symlink()` ⇒ 96/97, `t20zj` "symlink thu muc vao __pycache__ … duoc []" · `R4` vòng chỉ so gốc ⇒ 96/97, `t20zj` "vong ve to tien khong phai goc … duoc ['symlink TREO … docs/con/len/con/len/…']" · `R6` `[] if True else …` ⇒ 96/97, `t20zi` rc=0 | **ĐÃ VÁ THẬT** (5/5 đột biến chết đúng ca đích; xem thêm H2 hai vế với t82 THẬT) |
| **F-B lượt 8** `kiem-re-cua-fail-close-chua-co-ca` ở cửa `kiem_loai_tep` (6 đột biến sống ở lượt 8) | `N1` chỉ chặn symlink treo · `N3` chỉ `.md` · `N5` bỏ `ops/reviews/` · `N7` bỏ tên không đuôi · `N8` bỏ `/leases/` ⇒ mỗi cái 96/97, đỏ đúng `t20q` với dòng "kiem_loai_tep phai neu '<đường dẫn>'" của TỪNG hình dạng (`hop le .md`, `hop le .yaml`, `toi thu muc`, `duoi ops/leases`) · `N4` chặn oan tệp xoá ⇒ 95/97, đỏ `t20zc` "PR doi ten tep ho so phai DAT … LOI - tep da xoa" (+ `t20u` fixture) | **ĐÃ VÁ THẬT** (6/6 chết; lượt 8 cả 6 sống) |
| **P3 lượt 14** `kiem-mode-git-chot-khong-rang` (miễn kiểm `M`) | `K1` miễn M/120000 CHỈ ở cặp merge ref ⇒ `t20zh` "M/120000 phai TU CHOI o ca ba cap, duoc [2 loi]" · `K2` nhận T/160000 ⇒ `t20zh` + `t20w` + `t20za` · `K3` nhận D mọi mode ⇒ `t20zh` "D/100644 … D/160000" + `t20zb` · `K4` `MODE_THUONG` thêm 120000 ⇒ `t20zh` (A/M/T 120000) + `t20x` · `K5` miễn A/120000 chỉ cặp ba chấm ⇒ `t20zh` | **ĐÃ VÁ THẬT** (5/5; ca bảng `t20zh` bắt cả miễn kiểm MỘT cặp) — lớp đã dừng theo S3, không mở lại |
| **Tích hợp #668** (`gate-cong-cu`, `gate-cong-cu-gop`) | `Y1` `!cancelled()`→`always()` ⇒ `y11` "thua/doi [('gate-cong-cu-gop','always()')]" + `y13` · `Y2` `if: false` vào upload mảnh ⇒ `y12` + `y13` · `Y3` bỏ mảnh 7 ⇒ `y13` "khac ['strategy']" · `Y4` `continue-on-error` cấp job gom ⇒ `y10` + `y13` · `Y5` `continue-on-error` bước gom ⇒ `y10` + `y13` · `Y6` `needs: [chuan-bi, gate]` ⇒ `y13` "khac ['needs']" | **ĐÃ VÁ THẬT** (6/6). `JOB_G5` (registry) = `('gate','gate-registry','gate-packet-loop','gate-cong-cu','gate-cong-cu-gop')` — không có `gate-ops`, khớp docstring test |

Tổng: 22/22 đột biến của reviewer chết đúng ca đích, 0 `[HONG]` (không tín dụng giả). Không có VÁ HỜ / VÁ SINH LỖI MỚI trong bốn mục.

## BẢNG SĂN (ghi theo thứ tự chạy; mỗi hướng: giả thuyết / lệnh / output thật / kết luận)

### H1 — Đúng đắn thật của đường nhanh trên head này, với LỊCH SỬ THẬT của kho (sau merge master)
- **Giả thuyết:** sau merge master (#668, #677…) bộ phân loại + `kiem-re` của HEAD có thể ĐỎ oan một PR hồ sơ thật, hoặc cho
  đường nhanh một PR mã thật.
- **Lệnh:** `R/tmp/e/e_chay.py` — module lấy từ HEAD, cây làm việc = checkout commit merge THẬT (đóng vai `github.sha`), gốc =
  cha 1, đầu = cha 2; mười merge first-parent gần nhất của master. Thêm: PR CHÍNH packet này (gốc `20ec8d5`, đầu `b6104b0`,
  merge ref dựng bằng `merge-tree`+`commit-tree`), chạy `python3 -B ops/ci_duong_nhanh.py` TRONG checkout merge ref; ba ca
  KHÔNG ĐO ĐƯỢC (thiếu merge ref, merge ref không có object, gốc toàn 0) và `push`.
- **Output thật** (`R/out/e-lich-su.log`):
```
merge fc852ff #697  duong_nhanh (66 tep) · kiem-re rc=0 DAT (66 tep doi, 0 loi)
merge a54b825 #691  duong_nhanh (20 tep) · kiem-re rc=0 DAT
merge 91eb8fb #692  duong_nhanh (1 tep)  · kiem-re rc=0 DAT
merge 1741e0a #673  duong_nhanh (2 tep, lease thu hoi) · kiem-re rc=0 DAT
merge c16bec6 #693  duong_nhanh (17 tep) · kiem-re rc=0 DAT
merge 44620e8 #684  duong_nhanh (7 tep)  · kiem-re rc=0 DAT
merge 423b4ba #696  day_du (5 tep ngoai allowlist: .claude/dev/ci_dang_ky_test.py, ...)
merge 7b308bc #681  day_du (5 tep ngoai: ops/cai_actionlint.sh, ...)
merge 20ec8d5 #689  day_du (1 tep ngoai: ops/lease_publish_test.py)
merge 89fc4fa #680  day_du (1 tep ngoai: ops/lease_publish_test.py)
PR #674 (20ec8d5...b6104b0, merge ref 5c0e5ea): DAY_DU vi diff co 4 tep ngoai allowlist (ci_dang_ky_test.py, ci.yml, ci_duong_nhanh.py, ci_duong_nhanh_test.py)
thieu merge ref / merge ref 1234567… khong co object / goc toan 0: "KHONG DO DUOC diff … fail-close ve DAY_DU" (ca ba)
push: "khong phan loai - su_kien='push' … luon DAY_DU"
```
- **Lỗi rig (khai):** lần chạy đầu tôi gọi script của clone `w` với cây merge ref ở clone `e` ⇒ `ROOT` (theo `__file__`) không
  có object ⇒ `KHONG DO DUOC` cho cả PR #674. Chạy lại đúng như CI (script TRONG checkout merge ref) ⇒ như bảng trên.
- **Kết luận: KHÔNG PHẢI LỖI.** 6/6 PR hồ sơ thật ⇒ nhanh + kiem-re DAT (không ĐỎ oan); 4/4 PR mã thật + PR của chính packet ⇒
  đầy đủ; KHÔNG ĐO ĐƯỢC ⇒ đầy đủ. Chạy trên Actions thật: `KHÔNG ĐO ĐƯỢC` (nghiệm thu 11).

### H2 — P2 lượt 8 đo bằng `t82` THẬT, hai vế dựng trong MỘT lệnh (cùng bước, cùng vòng lặp)
- **Giả thuyết:** chốt mới chỉ khớp `t82` trên đồ giả của chính bộ test; trên cây thật có thể còn lệch.
- **Lệnh:** `R/tmp/e2/e2.py` — với mỗi vế `nen`/`dot`: clone `kho.git` @ HEAD; PR1 (đường đầy đủ, coi như đã land) thêm 5 symlink
  HỢP LỆ (`docs/zz-lien-ket.md`, `references/zz-thu` → thư mục, `ops/reviews/zz-l.md`, chuỗi `docs/zz-a.md → zz-b.md → …`);
  PR2 hồ sơ: `nen` thêm `ops/specs/ZZ-KHAC.md`, `dot` XOÁ hai đích; dựng merge ref; chạy phân loại, `kiem-re` của HEAD **và**
  của bản TRƯỚC g4 (`5ec951c`), rồi `python3 -B ops/lease_publish_test.py --chi-ca=t82_` (t82 THẬT) trên cùng checkout.
- **Output thật** (`R/out/e2-hai-ve.log`):
```
[nen] phan-loai HEAD: duong_nhanh
[nen] kiem-re HEAD b6104b0: rc=0 | DUONG_NHANH: kiem-re DAT (1 tep doi, 0 loi)
[nen] kiem-re TRUOC g4 5ec951c: rc=0 | DUONG_NHANH: kiem-re DAT (1 tep doi, 0 loi)
[nen] t82 THAT: rc=0 | lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
[dot] phan-loai HEAD: duong_nhanh
[dot] kiem-re HEAD b6104b0: rc=1 | DUONG_NHANH: kiem-re DO (2 tep doi, 5 loi) | symlink-loi=5 ['docs/zz-a.md','docs/zz-b.md','docs/zz-lien-ket.md','ops/reviews/zz-l.md','references/zz-thu']
[dot] kiem-re TRUOC g4 5ec951c: rc=0 | DUONG_NHANH: kiem-re DAT (2 tep doi, 0 loi)
[dot] t82 THAT: rc=1 | ĐỎ t82_A10_…: Error: [('…/e2/dot/references/zz-thu', …)] || lease_publish: 0/1 đạt
```
- **Kết luận:** P2 lượt 8 **ĐÃ VÁ THẬT** trên cây thật: rc `kiem-re` HEAD == rc `t82` ở cả hai vế (0/0 và 1/1), bản trước g4 lệch
  đúng ở vế `dot` (0 vs 1). Không chặn oan symlink hợp lệ (vế `nen`).

### H3 — Bước bị bỏ KHÁC có đọc dữ liệu cây mà `kiem-re` chưa phán không — kiểm kê LẠI sau merge master (audit hook, không grep)
- **Giả thuyết:** merge master đưa +615 dòng vào `ops/lease_publish_test.py` (ca `t195`–`t202`, bước bị bỏ `lease-publish
  selftest`); một ca mới có thể đọc `ops/{land,leases,reviews,specs}` thật mà `kiem-re` không chạy. (Các bước bị bỏ khác —
  `scripts/tl.py`, `packet_loop*`, `gate_lifecycle*` — KHÔNG đổi trong khoảng merge: `git diff --stat 89fc4fa 20ec8d5` chỉ có 11
  tệp ngoài hồ sơ, không tệp nào trong số đó; kiểm kê của lượt 8 cho chúng còn nguyên giá trị.)
- **Lệnh:** `R/tmp/hook/hook_lp.py` + `sitecustomize.py` (gắn `sys.addaudithook` cho tiến trình cha VÀ mọi tiến trình con python qua
  `PYTHONPATH`), chạy MỌI ca của `lease_publish_test.py` trên clone `R/tmp/w` @ HEAD, ghi `open/os.listdir/os.scandir` dưới 4 thư mục.
- **Output thật** (`R/out/audit-lp.log`, `R/out/audit-lp.jsonl`, 5m56s): `TONG 195 {'QUA': 192, 'KeyError': 3}`; ba `KeyError
  'lp_test_hook'` (`t199`, `t200`, `t202`) là lỗi RIG (các ca tra `sys.modules[__name__]`); sửa rig (đăng ký module) chạy lại riêng
  ba ca ⇒ `{'QUA': 3}`, **0** lần đọc dưới 4 thư mục. Ca đọc dữ liệu hồ sơ:
```
t23 {cha ops/leases: 120, ops/specs: 27} · t26 {cha ops/reviews: 433} · t27 {cha ops/reviews: 435}
t82 {cha ops/land: 63, ops/leases: 124, ops/reviews: 1713, ops/specs: 183}   (copytree CẢ cây)
t125 {con: ops/land 126, ops/leases 488, ops/reviews 5162, ops/specs 420}    (A/B chạy LẠI toàn suite hai lượt con)
```
- **Kết luận: KHÔNG có bộ đọc mới.** `t125` chỉ chạy lại chính suite (so TẬP ca đỏ giữa hai lượt con) nên bề mặt đọc của nó =
  `t23/t26/t27/t82`. `kiem-re` phủ `t23/t26/t27` (`kiem_ca_du_lieu`, chạy thật: `loi=[] | 5.5s`) và `t82` bằng chốt symlink cả cây
  (H2) — trừ một đường KHÔNG phải symlink, xem H4.

### H4 — `kiem_symlink_treo_ca_cay` có TƯƠNG ĐƯƠNG `t82` không, ngoài lớp symlink (chiều DAT oan / ĐỎ oan) ⇒ **LỖI (F1)**
- **Giả thuyết:** chốt mới chỉ mô phỏng phần SYMLINK của `copytree`; `t82` còn hỏng vì lý do khác mà PR hồ sơ tạo được. Liệt kê
  những gì một PR hồ sơ đổi được trên cây (chỉ thêm/sửa/xoá tệp mode 100644/100755 dưới 4 tiền tố — `kiem_mode_git` chặn mọi
  120000/160000): (a) xoá/đổi kiểu đích của symlink có sẵn ⇒ đã phủ (H2); (b) tạo vòng ⇒ không thể (cần symlink mới);
  (c) tệp không đọc được/tệp đặc biệt ⇒ git không tạo; (d) đường dẫn đích dài hơn nguồn ⇒ không (tiền tố San ngắn hơn gốc
  checkout); (e) **ĐỘ SÂU thư mục**: `copytree` đệ quy HAI khung/tầng (`copytree`→`_copytree`), còn `duyet` đệ quy MỘT khung/tầng.
- **Lệnh 1 (hai vế, MỘT lệnh):** `R/tmp/sau/sau.py` — mỗi vế clone @ HEAD, PR hồ sơ thêm `ops/reviews/zz-sau/a/…/a/f.md`
  (vế `nen` N=40, vế `dot` N=600; không symlink, không thoát cây), dựng merge ref, chạy phân loại, `kiem-re` HEAD, `t82` THẬT.
```
[nen N=40]  phan-loai: che_do=duong_nhanh · kiem-re HEAD: rc=0 DAT (1 tep doi, 0 loi) · t82 THAT: rc=0 (1/1 đạt)
[dot N=600] phan-loai: che_do=duong_nhanh · kiem-re HEAD: rc=0 DAT (1 tep doi, 0 loi) · t82 THAT: rc=1
            ĐỎ t82_A10_…: RecursionError: maximum recursion depth exceeded in comparison || lease_publish: 0/1 đạt
```
- **Lệnh 2 (ngưỡng, cùng một cây):** `R/tmp/sau/nguong.py` ⇒ `t82` THẬT `DAT` tới N=490, `RecursionError` từ N=500; chốt cả cây
  `LOI 0` tới N=990 (N=1000 thì chính `os.makedirs` của fixture chạm trần — dừng đo ở đó). Cửa sổ fail-open: **~500 ≤ N < ~995**.
- **Lệnh 3 (bước KHÔNG bị bỏ có chặn thay không):** trên checkout `dot` (N=600): `eol_policy.py --all --json` rc=0 `"ok": true` ·
  `ci_dang_ky_test.py` rc=0 `ĐĂNG KÝ: 23/23 · TỔNG: ĐẠT` · `workflow-audit` rc=0 · `doc-claims-check` rc=0 · `bundle_fragment_check`
  rc=0 · `ci_phamvi --kiem-bam` rc=0 ⇒ không bước giữ lại nào ĐỎ thay. (Python 3.11 cục bộ; CI 3.12: `KHÔNG ĐO ĐƯỢC`.)
- **Lệnh 4 (MỌI bước bị bỏ khác, hai vế N=40/N=600 trong MỘT lệnh, `R/tmp/sau/buoc_bo.sh`, 21m59s):** golden-test · determinism-audit
  strict · release-check full · release-bundle · packet_loop_test · gate_lifecycle_test · tl selftest ⇒ CẢ HAI vế rc=0 (`"ok": true`,
  `291/291 đạt`, `== tl selftest 1715/1715 ==` ở cả hai) ⇒ trong cửa sổ ấy `t82` là bước bị bỏ DUY NHẤT đỏ, nên chạy chính `t82` là đủ.
- **Lệnh 5 (mọi bước GIỮ LẠI còn lại của ba job bắt buộc, vế N=600, `R/tmp/sau/buoc_giu.sh`, 5m26s):** py_compile · codex_cred_test
  `13/13` · idiom_py_test `7/7` (quét `rglob("*.md")` cả cây) · eol_policy_test `30/30` · pre_push_test `9/9` · gen_instructions ·
  command_registry_test · ci_phamvi_test · release-manifest/verify lane WORKER `"ok": true` · tl_boot · bien_nhan_v2_test `TỔNG: ĐẠT` ·
  **ci_duong_nhanh_test `CA: 97/97 · DOT BIEN: 305/305 · TONG: DAT`** ⇒ rc=0 hết. Riêng `cong_cu.py kiem-tra` rc=2 — đo nền cùng lệnh: rc=2
  y hệt ở vế N=40 và ở HEAD (`jsonschema` vắng trong container; CI có cài) ⇒ delta 0. G5 `cong_cu_test` + 8 mảnh `gate-cong-cu`: KHÔNG
  chạy (nặng); đọc mã: chỉ chép đúng các phụ thuộc khai báo, không duyệt cả cây — `KHÔNG ĐO ĐƯỢC` bằng chạy.
- **Kết luận: LỖI hành vi trên HEAD, hẹp.** PR chỉ đổi hồ sơ, mọi check của đường nhanh XANH, lượt push trên master ĐỎ ở `t82`
  — đúng hình dạng lớp `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (bước bù phán một phần bất biến của bước bị bỏ), đường vào KHÔNG
  phải symlink. Chỉ đạt được bằng một thư mục ≥ ~500 tầng — không thể là nhầm lẫn; xem hạng ở F1.

### H5 — 36 đột biến MỚI của g4 (harness) có chết ĐÚNG LÝ DO không (tín dụng giả mức 2: chết ở `bang` fixture thay vì `bang` thuộc tính)
- **Giả thuyết:** harness chỉ phân hạng theo TÊN ca đích (`DO:<ca>:`); một đột biến có thể làm ca đích đỏ ở một `bang` "fixture vô
  hiệu"/"đối chứng" — vẫn được đếm GIẾT mà không đo thuộc tính.
- **Lệnh:** `R/tmp/mut/mut_harness.py` — lấy NGUYÊN `(tệp, hàm)` của 36 mục g4 trong `DOT_BIEN` (danh sách tên trích từ diff
  `a78a82a..b6104b0`), áp lên bản sao riêng, chạy MỌI ca, đọc thông điệp của ca đích. Log `R/out/mut-harness-g4.log`.
- **Output thật:** 36/36 ca đích ra `[DO]` ở `bang` THUỘC TÍNH (vd `symlink_treo_bo_bo_qua_pyc` ⇒ `t20zj` "treo ten .pyc: chot ca cay
  phai phan nhu t82 (mong []), duoc ['symlink TREO …']"; `mode_git_M_mien_symlink` ⇒ `t20zh` "M/120000 phai TU CHOI o ca ba cap, duoc
  []"), 0 ở `bang` fixture/đối chứng, 0 `[HONG]`.
- **Kết luận: KHÔNG PHẢI LỖI.** Ghi chú: `test_y11_noi_cho_phep_them_gate_registry` (nới bảng cho phép) chết vì chiều "thiếu" của
  phép so KHỚP ĐÚNG, tức nó đo tính hai chiều của `y11` — không đo ca "nới bảng + thêm tấn công cùng lúc" (ca đó theo thiết kế
  KHÔNG đo được: bảng là luật, đổi cả hai là đổi luật, chốt là review).

### H6 — Con số tự khai trong docstring/bảng đo (lớp `bang-do-thieu-neo-va-thieu-kiem-ke` — nợ #694)
- **Lệnh:** `goi/do_lai_so.py` trong `cay/` (4m19s) · `R/tmp/dem_lease.py` trên clone `--single-branch master` + fetch HEAD (`R/tmp/sb`)
  · `goi/kiem_ke.py`.
- **Output thật:** `[1] … do duoc diff: 345; toan allowlist: 63; … NGUYEN BAN do: 8` (khớp D1) · `[2] … 119 tep; … dat 119, truot 0`
  (cây đủ ref) · clone một nhánh: `119 tep; … dat 113, truot 6` · kiểm kê `CA 97 = 69+16+3+9`, `DOT_BIEN 305`, `ca du lieu … 5.5s`.
- **Kết luận (nợ #694, KHÔNG tính P):** D2 khai "6/113 … 0/113" — tử số còn đúng (6, 0), **mẫu số đã trôi 113 → 119** sau merge master;
  câu tự gắn nhãn "(đo bởi reviewer lượt 1)" nên là số CÓ NGÀY, nhưng không ghi ngày/commit đo ⇒ đúng hình dạng "bất biến còn đúng,
  số hạng đã trôi". Không phải lỗi hành vi đường nhanh.

### H7 — Lời khai trong CHÍNH các tệp write set có còn khớp hành vi sau khi packet đổi hành vi không (quét chú thích kề mỗi hunk) ⇒ **LỖI (F2)**
- **Giả thuyết:** packet thêm `if:`/checkout vào bước CÓ SẴN nhưng không đọc lại chú thích có sẵn của bước ấy (CLAUDE.md: "chú
  thích khẳng định về tệp mình đang nằm trong thì phải kiểm trên tệp đó").
- **Lệnh:** đọc ngữ cảnh của MỌI hunk trong `git diff origin/master...b6104b0 -- .github/workflows/ci.yml` (8 hunk) và các docstring
  lý do trong `ops/ci_duong_nhanh.py`; đối chiếu với YAML/mã ngay cạnh: `sed -n 35,79p` · `sed -n 255,276p` ci.yml · `sed -n 270,277p`
  ci_duong_nhanh.py; `grep` xác nhận không ca/đột biến nào neo vào các dòng ấy.
- **Output thật:**
```
ci.yml:37   # Chi ubuntu-latest, khong checkout ma nguon; bo github.ref == 'refs/heads/master'.
ci.yml:61   - uses: actions/checkout@v4 / if: pull_request / fetch-depth: 0   (#674 thêm — 24 dòng dưới câu trên)
ci.yml:79   run: python3 ops/ci_duong_nhanh.py                              (chạy mã của cây merge PR)
ci.yml:271  # … Lượt PR vẫn chạy
ci.yml:272  # selftest, chỉ không giả vờ sinh ra chứng cho một commit không có trong lịch sử.
ci.yml:274  if: ${{ github.event_name == 'pull_request' && needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}   (#674 sửa)
ci_duong_nhanh.py:272-273  "… symlink treo dưới allowlist làm nó ĐỎ trên master trong khi mọi kiểm khác của `kiem-re` vẫn DAT."
   — trên HEAD chính `kiem_mode_git` (120000 trong diff) và `kiem_symlink_treo_ca_cay` (g4) cũng ĐỎ với đúng đầu vào ấy (H2, t20n g4).
```
- **Kết luận: LỖI tài liệu (không đổi hành vi), 3 chỗ cùng một gốc** — xem F2.

### H8 — Merge `a78a82a` có giấu sửa tay không (bản vá g4 chỉ là phần nhìn thấy)
- **Giả thuyết:** commit merge master có thể mang thay đổi ngoài kết quả merge tự động — không lượt nào review riêng.
- **Lệnh:** (trong clone `R/tmp/w`) `git merge-tree --write-tree --no-messages 5ec951c 20ec8d5` so với `git rev-parse a78a82a^{tree}`;
  `git diff --stat a78a82a b6104b0`.
- **Output thật:** `rc=0 auto=5628d9641ec6e826c50ff3b3409d6aec3fb47ce0` · `a78a82a tree=5628d9641ec6e826c50ff3b3409d6aec3fb47ce0` (trùng
  byte); `a78a82a..b6104b0` chỉ đổi `ops/ci_duong_nhanh.py` (+66/−2) và `ops/ci_duong_nhanh_test.py` (+275/−13); commit g4 khai
  "ci.yml khong doi" — đúng.
- **Kết luận: KHÔNG PHẢI LỖI.** Merge sạch, không sửa tay; diff packet so `origin/master` đúng 4 tệp write set, `ci_dang_ky_test.py` `1 0`.
- **Lỗi rig của reviewer, khai thẳng:** lần ghi mục này vào VERDICT lần đầu dùng heredoc KHÔNG trích dẫn, nên các đoạn trong dấu nháy
  ngược bị shell chạy như lệnh, với cwd `/home/user/tra-luat` (kho chính, ngoài sandbox). Đo lại ngay (chỉ đọc): `git merge-tree
  --write-tree` ở đó chỉ "freshen" mtime của 8 đối tượng loose ĐÃ CÓ (cả 8 đều `reachable` từ `a78a82a`, commit 01:04:40; mtime mới
  04:33:56); không đối tượng mới, không đổi ref/index/cây làm việc (`git status --short` rỗng). Các lệnh khác trong dấu nháy là đọc
  (`rev-parse`, `diff --stat`, `w`) hoặc "command not found". Văn bản hỏng đã được viết lại bằng heredoc có trích dẫn.

### H9 — `kiem_symlink_treo_ca_cay` có đọc NGOÀI kho không, chi phí, cây có symlink thư mục/vòng (MÔ TẢ BẰNG LỜI phần thoát cây)
- **Đo được:** trên cây thật `cay`/`w`: `loi=[]`, 147 lần `os.scandir`, 0,013 s (bảng nền). Vòng về tổ tiên KHÔNG phải gốc, symlink thư
  mục vào `__pycache__`, chuỗi symlink, symlink thư mục tới đích bị xoá: đều có ca (`t20zi`/`t20zj`) và đột biến của tôi `R3`/`R4` chết
  đúng ca. `R4` (vòng chỉ so gốc) cho thấy KHÔNG có chốt vòng thì duyệt đi sâu `docs/con/len/con/len/…` tới khi đường dẫn quá dài
  (lỗi ra dạng "symlink TREO …") — chốt vòng làm thông điệp đúng, không phải thứ duy nhất ngăn treo.
- **Mô tả bằng lời (KHÔNG dựng đường thoát cây, theo chỉ thị):** hàm cố ý ĐI THEO symlink thư mục như `copytree`, nên một symlink thư
  mục trỏ RA NGOÀI checkout sẽ khiến nó liệt kê cả cây thư mục bên ngoài ấy; chốt vòng chỉ so `realpath` của TỔ TIÊN trong chuỗi đang
  duyệt, không so ranh giới kho. Hệ quả: (a) không lộ dữ liệu — hàm chỉ `scandir`/`stat`, không đọc nội dung, và chỉ in đường dẫn
  TƯƠNG ĐỐI của mục hỏng; (b) chi phí không bị chặn bởi kích thước kho; (c) mọi trường hợp như vậy đòi symlink đã land qua đường ĐẦY ĐỦ
  (đường nhanh chặn mọi 120000 ở `kiem_mode_git`), và chính `t82` của đường đầy đủ cũng chép đúng cây ngoài ấy — không phải phơi nhiễm
  MỚI do packet. Không đo được trên runner thật.
- **Kết luận: KHÔNG PHẢI LỖI** (giới hạn kế thừa từ `t82`; ghi để người đọc biết ranh giới).

### H10 — Kiểm LỜI KHAI của docstring `kiem_symlink_treo_ca_cay`: "symlink HỢP LỆ không bị chặn … PR hồ sơ SỬA nội dung đích hoặc biến đích thành THƯ MỤC (symlink dưới `docs/`, `references/`) ⇒ mọi bước bị bỏ cho cùng kết quả … (tl selftest: cùng tập ca hỏng)"
- **Giả thuyết:** một symlink hợp lệ từ vùng NGOÀI allowlist (`references/` — vùng của gói phát hành) trỏ vào hồ sơ biến PR hồ sơ thành
  PR đổi nội dung ngoài allowlist; một bước bị bỏ đọc xuyên symlink sẽ lệch.
- **Lệnh:** `R/tmp/hl/hl.py` — BA vế dựng trong MỘT lệnh, cùng bước: PR1 (đường đầy đủ) thêm `references/zz-lk.md`, `docs/zz-lk.md` →
  `ops/specs/ZZ-D.md` và `references/zz-thu` → `ops/specs/zz-thu/`; PR2 hồ sơ: `nen` thêm tệp khác · `noidung` sửa NỘI DUNG hai đích ·
  `thumuc` biến `ZZ-D.md` thành THƯ MỤC; mỗi vế: `kiem-re` HEAD, golden-test, determinism-audit strict, release-check full, `t82`
  THẬT, tl selftest. Rồi `R/tmp/hl/selftest3.sh` chạy lại tl selftest ba vế song song, lưu TOÀN BỘ output, so TẬP TÊN ca FAIL (md5).
- **Output thật** (`R/out/hl-ba-ve.log`, `R/out/hl-selftest-tap-ten.log`):
```
[nen|noidung|thumuc] kiem-re HEAD rc=0 DAT · golden rc=0 · determinism rc=0 · release-check rc=0 · t82 1/1 đạt   (ba vế y hệt)
[nen|noidung|thumuc] tl selftest 1713/1715 rc=1 · tập FAIL md5=9bb837a412ed19c71f9e999294426712 (ba vế trùng):
                     [FAIL] r219_docclaims_l9_tu_tat_khi_quet_hep · [FAIL] r291_docs_ngoai_goi
```
- **Kết luận: KHÔNG PHẢI LỖI — lời khai đứng được, delta = 0** (so bằng tập tên, không bằng số). Hai ca FAIL do chính trạng thái PR1
  (symlink dưới `docs/`/`references/`), có ở cả ba vế — tức PR1 ấy vốn ĐỎ trên đường đầy đủ; tiền đề "symlink hợp lệ đã land" khó
  hơn các lượt trước giả định (ghi để người đọc biết, không phải finding của #674).

## BẢNG LỚP

| Slug | Gốc lớp | Biểu hiện trên b6104b0 | Hạng | Của ai |
|---|---|---|---|---|
| `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (đường vào THỨ BA, không phải symlink) | Bước bù MÔ PHỎNG một phần bất biến của bước bị bỏ thay vì chạy chính mã của nó. g4 viết lại phần symlink của `copytree` (`kiem_symlink_treo_ca_cay`, đệ quy 1 khung/tầng); `t82` thật hỏng thêm vì ĐỘ SÂU (2 khung/tầng). Hình dạng CLAUDE.md "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba": lượt 7 = symlink trong diff, lượt 8 = symlink ngoài diff, lượt 15 = không symlink. | PR chỉ thêm thư mục hồ sơ sâu ≥ ~500 tầng: `kiem-re` DAT, `t82` RecursionError ⇒ ba check xanh, master ĐỎ (F1) | **P3** | **#674** |
| `chu-thich-co-san-khai-hanh-vi-cu` | Packet đổi hành vi của bước/job CÓ SẴN (thêm checkout, thêm `if:` theo `che_do`) nhưng không đọc lại câu khai có sẵn kề bên; ba câu nay mô tả hành vi trước packet | `ci.yml:37` "khong checkout ma nguon" · `ci.yml:271-272` "Lượt PR vẫn chạy selftest" · `ci_duong_nhanh.py:272-273` "mọi kiểm khác của kiem-re vẫn DAT" (F2) | **P3** | **#674** |
| `kiem-mode-git-chot-khong-rang` | (lớp đã DỪNG theo S3 lease g4) | 0 phát hiện mới; `t20zh` + 5 đột biến tự viết chết đúng ca (xem ĐỐI CHIẾU) | — | lớp đã dừng |
| `chot-yaml-chi-do-su-hien-dien` | (nợ #694) | 0 phát hiện mới; tích hợp #668 khoá cả GIÁ TRỊ `if:` cấp job (`y11`), 6 đột biến tự viết chết | — | nợ #694 |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | (nợ #694) | D2 "6/113 · 0/113": mẫu số trôi thành 119 (H6) — báo, không tính P | — | nợ #694 |

## FINDINGS

### buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca [P3] (F1) Thư mục hồ sơ sâu ≥ ~500 tầng: `kiem-re` DAT trong khi `t82` (bị bỏ) RecursionError ⇒ master ĐỎ
**TỆP/DÒNG:** `ops/ci_duong_nhanh.py:106-107` (`CA_DU_LIEU` chỉ `t23/t26/t27`) · `:286-337` (`kiem_symlink_treo_ca_cay`: `duyet` đệ quy
một khung/tầng, chỉ phán symlink) · bước bị bỏ: `ops/lease_publish_test.py:3166` (`t82`: `shutil.copytree(HERE.parent, …)`, đệ quy
`copytree`→`_copytree`, hai khung/tầng). Lời khai bị bác: commit g4 "11 bien the: rc kiem-re == rc t82"; docstring "Chốt DUYỆT như
`copytree` duyệt".

**VẤN ĐỀ:** g4 đóng đường symlink bằng cách MÔ PHỎNG `copytree`, nên chốt chỉ tương đương `t82` trên những gì nó mô phỏng. `copytree`
còn hỏng khi cây sâu quá trần đệ quy, và một PR hồ sơ tạo được điều đó (chỉ thêm tệp mode 100644 dưới `ops/reviews/**`, không symlink,
không thoát cây). Mọi bước GIỮ LẠI trên đường nhanh đều xanh với cây ấy (H4 lệnh 3), mọi bước bị bỏ khác cũng xanh (golden,
determinism, release-check full, release-bundle — đo ở vế N=600), chỉ `t82` đỏ ⇒ PR xanh cả ba check, lượt push trên master ĐỎ ở
`lease-publish selftest`. Hạng **P3** (không P2): chỉ đạt được bằng một thư mục ≥ ~500 tầng — không thể là nhầm lẫn; hậu quả là
master đỏ nhìn thấy được, không có mã lọt. Chủ kho có thể hạ xuống "quan sát" theo giới hạn đã khai ("Allowlist chặn NHẦM LẪN,
không chặn tác giả cố ý"); tôi vẫn ghi P3 vì hợp đồng của `kiem-re` là BÙ bước bị bỏ, lời khai g4 rộng hơn phép đo, và lối sửa rẻ.

**PHẢN CHỨNG** (H4, hai vế một lệnh `R/tmp/sau/sau.py`; ngưỡng `R/tmp/sau/nguong.py`):
```
[nen N=40]  kiem-re HEAD: rc=0 DAT · t82 THAT: rc=0 (1/1 đạt)
[dot N=600] kiem-re HEAD: rc=0 DAT · t82 THAT: rc=1 · ĐỎ t82_A10_…: RecursionError: maximum recursion depth exceeded in comparison
nguong: t82 THAT DAT tới N=490, RecursionError từ N=500 · chot ca cay HEAD LOI 0 tới N=990
```

**HINT** (`HINT.patch`, phần F1 — chỉ `ops/ci_duong_nhanh.py` + `ops/ci_duong_nhanh_test.py`): chạy CHÍNH `t82` trong `kiem-re` thay vì mô
phỏng thêm một lớp — `CA_DU_LIEU += ("t82_A10_dot_bien_A1_A8_tren_ban_sao_CA_CAY_ten_rieng",)` (giữ nguyên neo của mọi đột biến cũ);
`CA_DU_LIEU_CHUAN` thêm `t82`; `t22` so `log[0][-len(CA_DU_LIEU_CHUAN):]` thay cho `[-3:]`; ca mới `t20zl_ca_du_lieu_chay_chinh_t82_bat_cay_qua_sau`
(bản sao cây THẬT không `.git` + thư mục 600 tầng dựng bằng VÒNG LẶP, chốt fixture "chốt symlink cả cây phải DAT trên cây ấy", rồi đòi
`kiem_ca_du_lieu` ĐỎ với `RecursionError`; đối chứng cây thật DAT là `t22`); đột biến `ca_du_lieu_bo_t82` ⇒ `t20zl`. Giữ
`kiem_symlink_treo_ca_cay` (nêu TỪNG đường dẫn treo — `t82` chỉ nói `shutil.Error`). Chi phí đo: `t82` 1,35 s; `t20zl` 9,7 s.
Lối thay thế rẻ hơn nhưng XẤP XỈ: đặt trần độ sâu trong `duyet` (ĐỎ oan trong khoảng trần..490, phụ thuộc trần đệ quy và độ sâu stack
lúc `t82` gọi) — không khuyến nghị.

**ĐỘT BIẾN đo răng của hint** (trên bản đã áp):
```
harness  ca_du_lieu_bo_t82                       : nằm trong DOT BIEN 306/306 (giết đúng t20zl)
reviewer H1_ca_du_lieu_chi_ba_ca_dau (*CA_DU_LIEU[:3]) : CA 95/98 · [DO] t20zl "cay sau 600 tang: kiem_ca_du_lieu phai chay CHINH t82 (copytree) va DO, duoc []" (+ t22, t22b)
reviewer H2_t82_bi_loai_khoi_danh_sach           : CA 95/98 · [DO] t20zl (cùng thông điệp) (+ t22, t22b)
hai vế cũ (R/tmp/sau/hint_hai_ve.py): [nen] kiem-re HINT rc=0 DAT · [dot] kiem-re HINT rc=1 "ca du lieu cua lease_publish_test rc=1: … RecursionError"
                                      (cùng hai vế, kiem-re HEAD: rc=0 / rc=0)
```
**ĐỘ TIN:** cao về hành vi (đo trên `t82` THẬT, hai vế); thấp về khả năng xảy ra ngoài cố ý.

### chu-thich-co-san-khai-hanh-vi-cu [P3] (F2) Ba câu khai có sẵn mô tả hành vi TRƯỚC packet, ngay cạnh dòng packet vừa đổi
**TỆP/DÒNG:** `.github/workflows/ci.yml:37` · `.github/workflows/ci.yml:271-272` · `ops/ci_duong_nhanh.py:272-273`.

**VẤN ĐỀ:** (1) `chuan-bi` khai "khong checkout ma nguon" — packet thêm `actions/checkout` `fetch-depth: 0` ở `pull_request` và chạy
`ops/ci_duong_nhanh.py` của CÂY MERGE PR ngay dưới; câu cũ mô tả SAI ranh giới tin cậy của job (chính docstring module nói bộ phân
loại "chạy từ CÂY MERGE của PR"). (2) "Lượt PR vẫn chạy selftest" nằm ngay trên `if:` mà packet vừa thêm `che_do != 'duong_nhanh'` —
PR hồ sơ KHÔNG chạy selftest. (3) docstring `kiem_loai_tep` (lý do lượt 7) khai "mọi kiểm khác của `kiem-re` vẫn DAT" — từ lượt 10
(`kiem_mode_git`) và g4 (`kiem_symlink_treo_ca_cay`) điều đó sai (H2: 5 lỗi symlink từ chốt cả cây; `t20n` g4 tự ghi "chot ca cay CUNG
neu symlink treo nay"). Không đổi hành vi; đúng loại câu CLAUDE.md đòi kiểm trên chính tệp chứa nó. Không ca/đột biến nào neo vào ba
dòng (đã `grep`), nên sửa không chạm cổng nào.

**PHẢN CHỨNG:** H7 (đọc YAML/mã ngay cạnh, trích nguyên dòng ở trên).

**HINT** (`HINT.patch`, phần F2): sửa ba câu thành khai đúng hành vi hiện tại (`#548 khong checkout — #674 THEM checkout CHI o
pull_request …`; "… TRỪ PR chỉ đổi hồ sơ (#674 …): bước này bị bỏ …"; "… LÚC ẤY (lượt 7) vẫn DAT — nay `kiem_mode_git` và
`kiem_symlink_treo_ca_cay` cũng bắt …"). Chỉ chú thích/docstring.

**ĐỘT BIẾN đo răng:** không áp dụng (tài liệu; không cổng nào canh nội dung chú thích — nói thẳng: lớp này là kỷ luật đọc, máy không
canh). Đo hint không làm đỏ gì: `actionlint` rc=0, suite/registry xanh (dưới).

**ĐỘ TIN:** cao.

## ĐO HINT (`R/HINT.patch`, sha256 `2890a009a595f89bc001907e8d15c4a74ace56983185b26db0dddd799501476d`, 3 tệp — đều trong write set)
| Cây | Kết quả |
|---|---|
| clone mới `R/tmp/ap2` @ `b6104b02d2edddfe89a854f33db908291bec0559` | `git apply --check HINT.patch` ⇒ `APPLY_CHECK_OK`; áp xong `cmp` giống hệt cây đã chạy dưới (`R/tmp/ap`) |
| `python3 -B ops/ci_duong_nhanh_test.py` (đã áp, `R/tmp/ap`) | `CA: 98/98 dat · 0 do · 0 hong` · `DOT BIEN: 306/306 bi giet dung ly do` · `KIEM KE: ca hanh_vi=70 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=9 = 98 · dot bien …ci_dang_ky_test.py=2 + ci.yml=78 + ci_duong_nhanh.py=183 + ci_duong_nhanh_test.py=43 = 306` · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` · rc=0 · 2m15s |
| `python3 -B .claude/dev/ci_dang_ky_test.py` (đã áp) | `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · rc=0 |
| `actionlint .github/workflows/ci.yml` (shellcheck có mặt) · `ruff --select F` hai tệp · `doctrine-scan` | rc=0 · `All checks passed!` · `sạch — 10 tệp, 0 chỗ` |
| `git diff --numstat origin/master -- .claude/dev/ci_dang_ky_test.py` (đã áp) | `1 0` (vẫn đúng một dòng — hint không chạm tệp này) |
| `git status --short --ignored` sau khi chạy | chỉ 3 tệp `M` của hint, không tệp rác |
Hint mới chạy trên BẢN SAO; executor phải tự áp, tự đo, tự commit. `t20zl` chạy cây sâu 600 tầng nên chỉ hợp Linux — bước gọi bộ
test vốn đã `if: runner.os == 'Linux'`.

## KHÔNG ĐO ĐƯỢC (nói thẳng)
- Chạy trên Actions thật (PR thật, nghiệm thu 11; merge ref, `github.sha`, timeout, actor thật) — chỉ đo cục bộ, merge ref dựng bằng
  `merge-tree` + `commit-tree`.
- Windows (`core.symlinks=false`; `gate-ops` có nhãn `windows` cũng chạy `kiem-re`) và Python 3.12 của CI (máy này 3.11.15): ngưỡng
  độ sâu 490/500 của `t82` có thể xê dịch vài tầng trên 3.12; ca `t20zl` của hint dùng 600 tầng, cách xa ngưỡng ở cả hai phía.
- Nhánh lỗi quyền THẬT của `kiem_symlink_treo_ca_cay` (container chạy root) — chỉ đo qua đồ giả của `t20zk`.
- G5 `cong_cu_test` / 8 mảnh `gate-cong-cu` trên cây sâu (không chạy); `don-nhanh` (thiếu `pwsh`); `jsonschema` vắng nên
  `cong_cu.py kiem-tra` đỏ NỀN ở mọi cây (delta 0).
- Model/effort thật của lượt review này (tự khai Opus 5.5 / max, không receipt runtime).

## TÁC ĐỘNG NGOÀI SANDBOX (khai)
- `R/cay` không bị chạm: `git -C cay status --short --ignored` rỗng sau mọi lệnh chạy trong đó.
- `/home/user/tra-luat`: một lỗi rig (heredoc không trích dẫn, H8) làm `git merge-tree --write-tree` chạy ở đó và chỉ cập nhật mtime
  của 8 đối tượng loose ĐÃ CÓ (đều reachable từ `a78a82a`); không tạo đối tượng, không đổi ref/index/cây làm việc. Không commit, không
  push, không đăng GitHub, không chạy CI.

## KẾT LUẬN
`changes_requested` (ngưỡng chủ kho 0 P1 / 0 P2 / 0 P3; mức bảo đảm tối đa của lượt này là `advisory_review` vì cùng họ model).
- Bản vá g4 ĐÃ VÁ THẬT cả bốn mục đối chiếu: P2 lượt 8 (đo bằng `t82` THẬT hai vế — H2), F-B lượt 8 (6/6 đột biến từng sống nay chết),
  P3 lượt 14 (`t20zh`; lớp đã dừng theo S3, không mở lại), tích hợp #668 (6/6 đột biến topology chết; merge `a78a82a` sạch, không sửa
  tay). 36/36 đột biến mới của harness chết ở `bang` THUỘC TÍNH, không tín dụng giả. Đường nhanh đúng trên lịch sử thật: 6/6 PR hồ sơ ⇒
  nhanh + `kiem-re` DAT; 4/4 PR mã + PR của chính packet ⇒ đầy đủ; KHÔNG ĐO ĐƯỢC ⇒ đầy đủ.
- Còn lại hai P3 của #674: **F1** `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (đường vào thứ ba, KHÔNG phải symlink — cây sâu ≥ ~500 tầng
  làm `t82` RecursionError trong khi `kiem-re` DAT; chỉ đạt được bằng cố ý, chủ kho có thể hạ thành quan sát) và **F2**
  `chu-thich-co-san-khai-hanh-vi-cu` (ba câu khai cũ trái với hành vi packet vừa đổi). `HINT.patch` vá cả hai, áp sạch trên
  `b6104b0`, đã chạy: `CA 98/98 · DOT BIEN 306/306 · TONG: DAT`, registry `23/23 + 1025/1025`, actionlint rc=0, ruff/doctrine sạch,
  `ci_dang_ky_test.py` vẫn `1 0`.

TONG: P0=0 P1=0 P2=0 P3=2
