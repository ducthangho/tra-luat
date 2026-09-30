Reviewed commit: 57b6578398a63c2afe4e583061440b3156aec155
verdict: changes_requested
reviewed_sha: 57b6578398a63c2afe4e583061440b3156aec155
review_class: advisory_review (reviewer cùng họ executor — Claude Opus)

TONG: P0=0 P1=0 P2=1 P3=1 — 2 lớp của #674; 0 phát hiện mới trong hai lớp nợ #694.

> **Nói thẳng:** reviewer là Claude Opus, executor cũng là Claude Opus. Hai bên CÙNG HỌ model, nên lượt này là
> `advisory_review`, KHÔNG phải `cross_approved`. Packet `sensitive` vẫn cần Codex `cross_approved` hoặc
> `human_audited` ở cổng land. Model/effort thật của lượt này chỉ là tự khai, không có receipt runtime: `KHÔNG ĐO ĐƯỢC`.

## Môi trường và cách đo

- Linux, Python 3.11, git 2.43.0, actionlint (có trên PATH), **shellcheck VẮNG** ⇒ actionlint là phép đo yếu
  (bỏ luật shell), và `t137`/`t159` của lease_publish_test đỏ sẵn ở cả hai vế. ruff 0.15.15. Không mạng GitHub,
  không Actions, không Windows.
- `R/cay` KHÔNG bị sửa. Kiểm lại: `git -C cay status --short` rỗng.
- Mọi đột biến và phản chứng chạy trên bản sao trong `R/tmp/` (clone từ `R/kho.git`, detached đúng head,
  `core.abbrev 7`, `PYTHONDONTWRITEBYTECODE=1`). Script dựng rig nằm ở `R/out/`: `e1-dung.sh`, `e1-chay.sh`,
  `e2-chay.sh`, `e3-chay.sh`, `mut.py`, `hook_lp.py`, `sitecustomize.py`.
- Diff `origin/master...57b6578` gồm đúng 4 tệp write set. `ci_dang_ky_test.py` là `1 0` (một dòng thêm).
  `ci.yml` +87/-4. `ci_duong_nhanh.py` +318. `ci_duong_nhanh_test.py` +2000.

## Số đo nền (HEAD 57b6578, trong `cay/`)

| Lệnh | Kết quả |
|---|---|
| `python3 -B ops/ci_duong_nhanh_test.py` | `CA: 71/71 dat · 0 do · 0 hong` · `DOT BIEN: 168/168 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` · rc=0 · 41,7s |
| `KIEM KE` | `hanh_vi=43 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=9 = 71 · dot bien ci_dang_ky_test.py=2 + ci.yml=65 + ci_duong_nhanh.py=59 + ci_duong_nhanh_test.py=42 = 168` (khớp `goi/kiem_ke.py`) |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 938/938 đỏ đúng` · `TỔNG: ĐẠT` · rc=0 |
| `actionlint .github/workflows/ci.yml` | rc=0. Phép đo YẾU vì shellcheck vắng |
| `ruff check --no-cache --select F ops/ci_duong_nhanh.py ops/ci_duong_nhanh_test.py` | `All checks passed!` |
| `goi/do_lai_so.py` (trong `cay/`) | `[1] … do duoc diff: 345; toan allowlist: 63; … NGUYEN BAN do: 8` · `[2] … 113 tep; … dat 113, truot 0` |
| `goi/do_lai_so.py` trên clone `--single-branch master` + fetch head (`tmp/sb`, 2 ref) | `[2] … 113 tep; … dat 107, truot 6` ⇒ lời khai D2 "6/113 clone chỉ-master · 0/113 bản sao đủ ref" **đúng** |
| `kiem_ca_du_lieu` (qua `kiem_ke.py`) | `loi = [] \| 4.2s` (docstring khai "~6 giây"; khác máy, không phải finding) |

Ghi chú: lượt đầu tôi chạy `do_lai_so.py` từ ngoài `cay/` và ra `0/0/0` cùng `ModuleNotFoundError`. Đó là lỗi của
rig (tệp này đòi chạy trong `cay/`), không phải của executor.

## ĐỐI CHIẾU LƯỢT TRƯỚC (ba verdict lượt 7 trên `af1165d` → bản vá `57b6578`)

Mỗi dòng có một phép đo của riêng tôi: đột biến tự viết, **khác chữ** với đột biến của harness, chạy trên bản sao
`cay`, và phải chết đúng ca đích.

| Lớp / finding lượt 7 | Nguồn | Trạng thái | Bằng chứng tự đo |
|---|---|---|---|
| `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` P2 (symlink treo dưới allowlist) | luot-7 F1 | **VÁ HỞ** | Phần đã phủ **có răng**: gỡ lời gọi `kiem_loai_tep` ⇒ `CA 70/71`, đỏ đúng `t20n`; `is_symlink` bỏ qua `ops/specs/` ⇒ `CA 70/71`, đỏ đúng `t20n`. Phần còn hở: chốt chỉ nhìn tệp **trong diff**, còn `t82` quét **cả cây**. Một symlink hợp lệ vào cây qua PR đầy đủ, rồi thành treo khi PR hồ sơ xoá đích ⇒ lọt (F1). |
| `kiem-re-cua-fail-close-chua-co-ca` P2 (9 cửa + `safe_load_all`) | luot-7-opus-af1165d, luot-7 F2 | **ĐÃ VÁ THẬT** cho các cửa đã liệt kê | `endswith((".yaml",))` ⇒ `CA 70/71`, đỏ `t20h`; nhánh `datetime` của `_han_lease` bị tắt ⇒ `CA 70/71`, đỏ `t20l`. 9+1 đột biến của harness (`kiem_yaml_*`, `kiem_lease_*`, `han_lease_*`, `diff_check_*`) đều nằm trong 168/168. Cửa MỚI do chính bản vá mở ra (vế symlink HỢP LỆ) chưa có ca ⇒ F2. |
| `kiem-re-phu-thuoc-actor-su-kien` P3 | luot-7, luot-7-opus-af1165d | **ĐÃ XỬ LÝ theo quyết định chủ kho** (khai trong docstring D2, không đổi chốt) | Docstring dòng 53–56 khai đúng hệ quả mà lượt 7 đo: bot đẩy thì ra `CHAN [4]`. Không ghi finding chính sách. |
| `bang-do-thieu-neo-va-thieu-kiem-ke` P3 (dòng `TU KIEM PHAN HANG:` không neo) — **nợ #694** | luot-7-opus-subagent-g3 | **ĐÃ VÁ THẬT** | `t93` nay đòi TẬP 5 dòng tổng kết. Hai đột biến `test_main_tu_kiem_in_so_sai` và `test_main_tu_kiem_luon_in_dat` nằm trong 168/168. Không có phát hiện mới. |
| `diff-check-tu-ha-nguong` P3 (D1 thu hẹp từng loại) | luot-7-opus-subagent-g3 | **ĐÃ VÁ THẬT** | Tôi đổi `-space-before-tab` thành `space-before-tab` (BẬT lại loại ấy, khác chữ với đột biến harness) ⇒ `CA 69/71`, đỏ `t20d` và `t23_fixture_sach…`. |
| `kiem-re-bo-sot-duong-vao` P3 (`.yml`, tệp đã xoá ở `kiem_yaml`) | luot-7-opus-subagent-g3 | **ĐÃ VÁ THẬT** | Đã thấy qua `t20h` ở trên. `kiem_yaml_tep_xoa_cat_vong` nằm trong 168/168, đích `t20i`. |
| `chot-yaml-chi-do-su-hien-dien` — **nợ #694** | lượt 6 | Không có phát hiện mới | 65 đột biến `ci.yml` của harness nằm trong 168/168. Không tìm được đột biến YAML nào sống. |

## BẢNG LỚP

| Slug | Gốc lớp | Biểu hiện | Hạng | Của ai |
|---|---|---|---|---|
| `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` | Bước bù `kiem-re` phán trên **tập tệp trong diff**. Bước bị bỏ (`t82` của `lease-publish selftest`) phán trên **cả cây**. Một PR chỉ-hồ-sơ **xoá** một tệp có thể làm hỏng một bất biến toàn cây ở tệp **không nằm trong diff**. | Symlink hợp lệ (vào qua PR đầy đủ, ngoài allowlist) thành treo khi PR đường nhanh xoá đích. `kiem-re` rc=0, `t82` rc=1 ⇒ PR xanh, master **ĐỎ** | **P2** | **#674** — VÁ HỞ của lượt 7 F1 |
| `kiem-re-cua-fail-close-chua-co-ca` | Docstring của `kiem_loai_tep` khai hai vế ("chặn mọi symlink, **treo hay không**") nhưng ca `t20n` chỉ có vế treo. Đột biến trên vế còn lại chỉ "chết" vì neo đột biến khác vỡ. | Đột biến `is_symlink() and not exists()` ⇒ `CA 71/71`, `DOT BIEN 167/168`, `TONG: DO`. Đây là tín dụng giả qua `HONG … neo … thay 0` của `loai_tep_cho_symlink_qua` | **P3** | **#674** |

Hai lớp nợ #694 (`chot-yaml-chi-do-su-hien-dien`, `bang-do-thieu-neo-va-thieu-kiem-ke`): **0 phát hiện mới**.

## BẢNG SĂN

### H1 — Kiểm kê TOÀN BỘ dữ liệu mà các bước bị bỏ đọc từ cây thật (audit hook, không grep)
- **Giả thuyết:** ngoài t23/t26/t27/t82 còn có ca hoặc bước bị bỏ khác đọc dữ liệu dưới `ops/{land,leases,reviews,specs}`.
- **Lệnh (lease_publish_test):** `python3 -B out/hook_lp.py <nen> ops/lease_publish_test.py out/audit-lp.json`, với
  `sys.addaudithook` gắn theo từng ca, ghi `open/os.listdir/os.scandir` dưới 4 thư mục và `subprocess.Popen` có cwd trong cây.
  **Lệnh (các bước khác):** `sitecustomize.py`, được mọi tiến trình con thừa kế qua `PYTHONPATH`, chạy golden,
  determinism, release-check full, release-bundle, packet_loop_test, gate_lifecycle_test, tl selftest.
- **Output thật:** lease_publish_test `RAN 185+2/187` (hai ca đỏ là `t137` và `t159`, do vắng shellcheck). Chỉ bốn ca
  đọc dữ liệu thật: `t23 {'ops/leases': 114, 'ops/specs': 17}` · `t26 {'ops/reviews': 377}` · `t27 {'ops/reviews': 190}` ·
  `t82 {'ops/land': 29, 'ops/leases': 118, 'ops/reviews': 1651, 'ops/specs': 167}`. Các bước còn lại chỉ có hai kiểu đọc:
  (a) `os.scandir` 4 thư mục, từ `rglob` của `_build_release_manifest`, loại bằng `"ops" ∈ rel.parts`;
  (b) `git log --diff-filter=D --name-only` (golden, determinism, tl selftest ×9), là tập tệp từng bị xoá cho doc-claims.
- **Kết luận:** bề mặt đọc gồm `t23/t26/t27` (đã chạy trong `kiem-re`), `t82` (copytree cả cây), rglob (loại theo
  tên), và lịch sử xoá. `t82` là điểm hở duy nhất có tính **toàn cây** ⇒ dẫn tới H2 và F1.

### H2 — Hai vế trong MỘT lệnh: 8 loại dữ liệu hồ sơ mới, chạy MỌI bước bị bỏ
- **Giả thuyết:** loại dữ liệu mà lượt 7 chưa thử có tạo delta.
- **Lệnh:** `bash out/e1-dung.sh && bash out/e1-chay.sh`. Vế nen = `57b6578`. Vế dot = `57b6578` cộng: gitlink
  `ops/specs/sub` (mode 160000), tên tệp không-UTF-8 `ops/reviews/\377\376.md`, **xoá** `ops/land/pr480-land-evidence.yaml`,
  `ops/specs/-n.md`, `ops/leases/X.YAML` hỏng, `ops/leases/x.json` hỏng, `ops/land/run.sh` mode 755, `ops/land/bom.yaml` có BOM.
- **Output thật** (`out/e1-ket-qua.txt`):
```
phanloai     nen[rc=0] dot[rc=0]      (dot: che_do=duong_nhanh, 8 tep)
kiemre       nen[rc=0] dot[rc=0]
relcheck/golden/determinism/bundle/packetloop  nen rc=0 · dot rc=0
leasepub     nen[rc=1] dot[rc=1]      (ca hai 185/187, DO dung t137 t159 — shellcheck vang)
selftest     == tl selftest 1715/1715 == ca hai ve
lifecycle    chay lai TUAN TU: nen 28/28 · dot 28/28 (luot song song dau do ca hai ve vi tranh cgroup/khoa — nhieu cua rig)
```
- **Kết luận: KHÔNG PHẢI LỖI** cho tám loại này (delta = 0 ở mọi bước bị bỏ).

### H2b — Symlink TREO sinh bằng XOÁ ĐÍCH (tệp symlink KHÔNG nằm trong diff) ⇒ **LỖI (F1)**
- **Lệnh:** `bash out/e2-chay.sh` (hai vế trong một lệnh; PR1 thêm `docs/zz-lien-ket.md -> ../ops/specs/ZZ-DICH.md`, PR2 xoá đích).
- **Output thật:**
```
nen PR1 phan-loai: che_do=day_du
nen t82 rc=0 | DAT t82_A10_dot_bien_A1_A8_tren_ban_sao_CA_CAY_ten_rieng
dot PR1 phan-loai: che_do=day_du
dot PR2 phan-loai: che_do=duong_nhanh
dot PR2 kiem-re rc=0 | DUONG_NHANH: kiem-re DAT (1 tep doi, 0 loi)
dot t82 rc=1 | shutil.Error: [('…/e2/dot/docs/zz-lien-ket.md', '…/repo/docs/zz-lien-ket.md', "[Errno 2] No such file or directory …
```

### H3 — Răng của bản vá `57b6578` (đột biến của reviewer, khác chữ với harness)
- **Lệnh:** `python3 -B out/mut.py <tên>`. Mỗi đột biến chạy trên một `copytree` riêng của `cay`, qua FULL suite.
- **Output thật:**
```
V_yaml_tuple_chi_yaml:        CA 70/71 · DOT BIEN 167/168 · TONG: DO · do=[t20h_kiem_yaml_duoi_yml_ngoai_lease_do]
V_ws_them_tab_vao_cau_hinh:   CA 69/71 · DOT BIEN 162/168 · TONG: DO · do=[t20d_…, t23_fixture_sach_…]
V_han_datetime_thanh_con_han: CA 70/71 · DOT BIEN 167/168 · TONG: DO · do=[t20l_han_lease_timestamp_yaml_khong_nhay_ngoac]
V_loai_tep_bo_qua_specs:      CA 70/71 · DOT BIEN 166/168 · TONG: DO · do=[t20n_kiem_re_symlink_ho_so_do]
H_bo_loai_tep (HEAD):         CA 70/71 · DOT BIEN 166/168 · TONG: DO · do=[t20n_kiem_re_symlink_ho_so_do]
ca_du_lieu_bo_t26 / _t27:     CA 69/71 · TONG: DO (ca hanh vi do)
loai_tep_chi_chan_treo:       CA 71/71 dat · 0 do · DOT BIEN 167/168 · TONG: DO   <- SONG ve hanh vi; "chet" vi
                              [DOT BIEN KHONG BI GIET DUNG] loai_tep_cho_symlink_qua: HONG … neo … thay 0   (TIN DUNG GIA)
loai_tep_chi_duoi_md:         CA 71/71 dat · TONG: DO   <- cung co che tin dung gia
```
- **Kết luận:** các chốt lượt 7 có răng. Riêng vế "symlink HỢP LỆ" **KHÔNG có ca** ⇒ **LỖI (F2)**.
  Kiểm thêm lỗ mới quanh `is_symlink`. (a) Tệp đã xoá: `is_symlink` trả False, và đúng như vậy (xoá không phải
  symlink). (b) Thư mục cha là symlink: git không theo dõi tệp dưới một symlink, nên thành phần symlink ấy tự nó
  nằm trong diff và bị bắt. Một symlink cha CÓ SẴN không bao giờ có tệp con được theo dõi. (c) Windows
  (`core.symlinks=false`): `is_symlink` trả False nhưng `t82` cũng không đỏ ⇒ không có delta; chân ubuntu vẫn
  bắt. Chỉ suy luận, Windows `KHÔNG ĐO ĐƯỢC`.

### H4 — Các bước KHÔNG bị bỏ có ngầm dựa vào sản phẩm của bước bị bỏ không (đường nhanh có xanh được không)
- **Lệnh:** `bash out/e3-chay.sh`. Hai clone sạch. A chạy CHỈ các bước không bị bỏ, đúng thứ tự `ci.yml`. B chạy mọi bước.
  Bước lane WORKER chạy lại với `RUNNER_TEMP` đặt đúng (lượt đầu của rig thiếu biến này ⇒ đỏ cả hai vế).
- **Output thật:** `A wfaudit/docclaims/phamvi/phamvitest/tlboot/biennhan rc=0` · `B` (thêm selftest, golden,
  determinism, relcheck, bundle) mọi bước rc=0 · lane WORKER: `A … manifest tam: 180 tep, tat ca deu duoc git theo doi`
  rc=0 · `B` y hệt.
- **Kết luận: KHÔNG PHẢI LỖI.** Không bước nào bị bỏ để lại sản phẩm cho bước sau.
  `KHÔNG ĐO ĐƯỢC`: G5 `cong_cu` (thiếu shellcheck), `don-nhanh` (thiếu pwsh), bước "PR head contains EOL base" (cần sự kiện PR thật).

### H5 — D1: `git diff --check` có còn bắt dấu xung đột khi PR mang `.gitattributes` không
- **Lệnh:** kho tạm `tmp/e4/k`, `git -c core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab diff --check B...H`.
- **Output thật:** attribute `-whitespace` (kho đang dùng ở 3 thư mục `ops/reviews/*`) ⇒ `leftover conflict marker … rc=2`,
  tức vẫn bắt. Attribute `*.md -diff` (tệp thành nhị phân) ⇒ `rc=0`, kể cả khi thêm `--text`.
- **Kết luận: KHÔNG PHẢI LỖI** của đường nhanh. Đường đầy đủ không chạy `--check` nên không có delta. Muốn tắt
  thì PR phải cố ý thêm `-diff`/`binary`/`conflict-marker-size`, và trường hợp đó thuộc giới hạn đã khai ("Allowlist
  chặn NHẦM LẪN, không chặn tác giả cố ý"). Câu D1 "thứ `--check` báo bất kể cấu hình" đúng theo nghĩa đen với
  *cấu hình* (`core.whitespace`). Nó không nói tới *attribute*; ghi lại để người đọc biết ranh giới.

### H6 — Các con số tự khai trong docstring hoặc bảng đo
- **Lệnh:** `goi/do_lai_so.py` trong `cay/` và trong clone single-branch; `goi/kiem_ke.py`.
- **Output thật:** `345 / 63 / 8` khớp. `113 dat 113 truot 0` (đủ ref) và `dat 107 truot 6` (một nhánh) khớp. Kiểm kê
  `71` ca / `168` đột biến khớp dòng `KIEM KE`. `ca du lieu … 4.2s` so với khai "~6 giây": khác máy, trong ngưỡng.
- **Kết luận: KHÔNG PHẢI LỖI.** Bảng `DO_LAI.md` không bỏ sót khẳng định định lượng nào của `57b6578` (bản vá không thêm con số).

### H7 — Timeout `chuan-bi` 10/5/20 + `continue-on-error`
- **Lý lẽ + đọc `ci.yml` dòng 45–83:**
  - Checkout hỏng hoặc hết giờ (10) ⇒ `continue-on-error` giữ job xanh. Bước phân loại có `if` chỉ theo sự kiện, nên
    `success()` ngầm vẫn đúng và bước vẫn chạy. Thiếu script hoặc object ⇒ rc≠0 hoặc `doc_diff`=None ⇒ output vắng
    hoặc `day_du` ⇒ `outputs.che_do` = `'day_du'`.
  - `main` ghi `che_do=` là thao tác cuối, nên hết giờ (5) giữa chừng chỉ có thể làm vắng output, không làm sai.
  - Hết giờ cấp job (20) ⇒ `chuan-bi` đỏ ⇒ ba context bắt buộc không được tạo ⇒ PR bị CHẶN (đóng, không mở). 10+5 < 20.
- **Kết luận: KHÔNG PHẢI LỖI.** Hành vi thật trên Actions: `KHÔNG ĐO ĐƯỢC`.

## FINDINGS

### buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca [P2] (F1) Symlink TREO do PR hồ sơ XOÁ ĐÍCH: `kiem-re` DAT, `t82` bị bỏ, master ĐỎ

**TỆP/DÒNG:** `ops/ci_duong_nhanh.py:181-186` (`kiem_loai_tep` chỉ lặp `doi`) · `:282` (`lenh_kiem_re`) ·
bước bị bỏ `lease-publish selftest` → `ops/lease_publish_test.py:3155` (`shutil.copytree(HERE.parent, …)` cả cây, theo symlink).

**VẤN ĐỀ:** Bản vá lượt 7 chặn symlink **trong diff**, còn bước mà nó bù (`t82`) phán **cả cây**. Có một đường hai PR,
mỗi PR đều hợp lệ khi đứng riêng:
1. PR1 chạm `docs/` (ngoài allowlist ⇒ `day_du` ⇒ `kiem-re` không chạy). Nó thêm một symlink **hợp lệ** `docs/x.md -> ../ops/specs/D.md`.
   `t82` chạy và qua, vì symlink còn trỏ tới tệp có thật.
2. PR2 chỉ xoá `ops/specs/D.md` ⇒ `duong_nhanh`. `doi = {ops/specs/D.md}`; tệp symlink **không** nằm trong diff ⇒
   `kiem_loai_tep` không thấy nó. `t82` bị bỏ. Ba required check xanh; lượt push trên master cho `gate-ops` **ĐỎ**.

Symlink cũng có thể nằm ngay dưới allowlist nếu nó vào qua một PR đầy đủ (PR đầy đủ không chạy `kiem-re`). Hỏng theo
chiều mở, đúng hình dạng mà lượt 7 F1 xếp P2: đường nhanh cho qua thứ mà đường đầy đủ từ chối. Không có mã nào lọt,
và master đỏ thì nhìn thấy được ⇒ P2, không phải P1. Master hiện có 0 symlink (`git ls-files -s | awk '$1=="120000"'`
rỗng), nên đây là đường còn mở, chưa từng xảy ra.

**PHẢN CHỨNG:** H2b ở trên (`out/e2-chay.sh`): `dot PR2 kiem-re rc=0 … DAT (1 tep doi, 0 loi)` · `dot t82 rc=1 | shutil.Error`.

**HINT** (`HINT.patch`, chỉ `ops/ci_duong_nhanh.py` + `ops/ci_duong_nhanh_test.py`):
- `kiem_symlink_treo_ca_cay(kho)`: `os.walk` **cả cây**. Bỏ qua đúng những gì `t82` bỏ qua (`.git`, `__pycache__`,
  `*.pyc`). Symlink nào `islink and not exists` là lỗi. `onerror` biến lỗi duyệt thành
  `KHONG DO DUOC` (fail-close, không nuốt). Nối vào `lenh_kiem_re`.
- Ca `t20p_kiem_re_symlink_treo_NGOAI_diff_do`: dựng đúng kịch bản hai PR bằng git thật, kèm đối chứng (PR hồ sơ sửa
  tệp KHÁC ⇒ DAT) và chốt fixture (PR xoá đích phải ra `duong_nhanh`).
- Ca `t20q_symlink_treo_khong_duyet_duoc_cay_la_do`: `os.walk` lỗi ⇒ ĐỎ.
- Bốn đột biến có đích riêng: `kiem_re_bo_symlink_treo_ca_cay` và `symlink_treo_vi_tu_luon_sai` ⇒ `t20p`;
  `symlink_treo_chi_quet_tep_khong_quet_thu_muc_con` ⇒ `t20p`; `symlink_treo_nuot_loi_duyet` ⇒ `t20q`.
- Đo trên cây thật: hàm mới trả `[]` cho `cay`, `e1/nen`, `e1/dot` và `e2/nen`; trả đúng một lỗi
  `'docs/zz-lien-ket.md'` cho `e2/dot`; mỗi lượt 0,01s.

**ĐỘT BIẾN đo răng của hint** (runner độc lập `out/mut.py`, trên bản đã áp):
```
H_bo_goi_treo:          CA: 72/73 dat · 1 do · DOT BIEN 170/173 · TONG: DO · do=['t20p_kiem_re_symlink_treo_NGOAI_diff_do']
H_vi_tu_sai:            CA: 72/73 dat · 1 do · DOT BIEN 170/173 · TONG: DO · do=['t20p_kiem_re_symlink_treo_NGOAI_diff_do']
H_nuot_loi:             CA: 72/73 dat · 1 do · DOT BIEN 171/173 · TONG: DO · do=['t20q_symlink_treo_khong_duyet_duoc_cay_la_do']
```
Mỗi đột biến chết đúng một ca hành vi, và đó là ca đích (không có tín dụng giả).

**Nợ còn lại (khai, không vá):** hint đóng bất biến *symlink treo toàn cây*. Gốc lớp vẫn là: `kiem-re` được liệt kê
bằng tay theo những gì đã biết mà bước bị bỏ phán. Lối ra tổng quát là với mỗi bước bị bỏ, đo tập ca đọc cây thật (như
H1), rồi đòi `kiem-re` chạy đúng tập ấy. Việc đó nằm ngoài một bản vá tối thiểu; đề xuất đặt tên nợ
`buoc-bi-bo-doc-ca-cay` cho #694 hoặc successor. Chủ kho quyết.

**ĐỘ TIN:** cao. Có phản chứng chạy được, hai vế trong một lệnh, và delta đúng một ca (`t82`).

### kiem-re-cua-fail-close-chua-co-ca [P3] (F2) Vế "symlink HỢP LỆ" của `kiem_loai_tep` không có ca: đột biến sống, "chết" nhờ tín dụng giả

**TỆP/DÒNG:** `ops/ci_duong_nhanh.py:184` (docstring: "chặn mọi symlink, treo hay không") ·
`ops/ci_duong_nhanh_test.py` `t20n_kiem_re_symlink_ho_so_do` (chỉ có `symlink_to("khong-ton-tai")`).

**VẤN ĐỀ:** Đúng hình dạng "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba" trong CLAUDE.md. Bản vá khai hai vế, nhưng
chỉ vế treo có ca. Một lần "tối ưu" về `is_symlink() and not exists()` sẽ mở lại đường symlink hợp lệ dưới allowlist.
Đường ấy thành treo khi một PR hồ sơ sau xoá đích (tổ hợp với F1). Bộ test vẫn báo `TONG: DO`, nhưng chỉ vì đột biến
đè lên neo của `loai_tep_cho_symlink_qua`. Đó là tín dụng giả, không phải phép đo.

**PHẢN CHỨNG:** `python3 -B out/mut.py loai_tep_chi_chan_treo` trên HEAD ⇒ `CA: 71/71 dat · 0 do · 0 hong` ·
`DOT BIEN: 167/168` · `[DOT BIEN KHONG BI GIET DUNG] loai_tep_cho_symlink_qua: HONG RuntimeError: ha tang: neo dot bien phai
xuat hien DUNG MOT lan, thay 0`. Đột biến `loai_tep_chi_duoi_md` cũng cho `CA 71/71`, cùng cơ chế.

**HINT** (trong `HINT.patch`): `t20n` thêm nhánh `hop-le` với một symlink hợp lệ `ops/specs/hop-le.md -> S.md`, phải ĐỎ
và log phải chứa `la symlink` (chỉ `kiem_loai_tep` in chuỗi này, nên chốt toàn cây của F1 không che được). Thêm đột biến
`loai_tep_chi_chan_treo` ⇒ `t20n`.

**ĐỘT BIẾN đo răng của hint** (trên bản đã áp):
```
loai_tep_chi_chan_treo: CA: 72/73 dat · 1 do · DOT BIEN 170/173 · TONG: DO · do=['t20n_kiem_re_symlink_ho_so_do']
H_bo_loai_tep:          CA: 72/73 dat · 1 do · DOT BIEN 169/173 · TONG: DO · do=['t20n_kiem_re_symlink_ho_so_do']
```
Sau khi có chốt toàn cây, `H_bo_loai_tep` vẫn chết đúng `t20n` nhờ vế hợp lệ: hai chốt phân biệt được bằng đầu vào,
không phải một bộ tương đương.

**ĐỘ TIN:** cao.

## ĐO HINT (`R/HINT.patch`, sha256 ở cuối báo cáo gửi phiên điều phối)

| Cây | Kết quả |
|---|---|
| clone mới `tmp/apply` @ `57b6578` | `git apply --check HINT.patch` ⇒ `APPLY_CHECK_OK`; áp xong `cmp` giống hệt bản hint đã chạy |
| `python3 -B ops/ci_duong_nhanh_test.py` (đã áp) | `CA: 73/73 dat · 0 do · 0 hong` · `DOT BIEN: 173/173 bi giet dung ly do` · `KIEM KE: … = 73 · … ops/ci_duong_nhanh.py=64 … = 173` · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` · rc=0 |
| `python3 -B .claude/dev/ci_dang_ky_test.py` (đã áp) | `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 938/938 đỏ đúng` · `TỔNG: ĐẠT` · rc=0 |
| `actionlint .github/workflows/ci.yml` · `ruff --select F` hai tệp | rc=0 (yếu, không có shellcheck) · `All checks passed!` |

Hint chỉ chạm `ops/ci_duong_nhanh.py` (+25/−1) và `ops/ci_duong_nhanh_test.py` (+50), cả hai trong write set. Không
chạm `ci.yml`, cũng không chạm `ci_dang_ky_test.py`. Hint mới chạy trên bản sao; executor phải tự áp, tự đo và tự commit.

## CHƯA ĐO ĐƯỢC
Chạy thật trên Actions (PR thật, nghiệm thu 11) · timeout thật · Windows (`core.symlinks=false`, chân `windows`) ·
actor thật · actionlint **có** shellcheck (container thiếu) · G5 `cong_cu`/`don-nhanh` (thiếu shellcheck, pwsh) ·
model/effort thực chạy của chính lượt review này.

## KẾT LUẬN
`changes_requested`. P0=0 P1=0 **P2=1** (`buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca`, của #674, vá hở lượt 7) **P3=1**
(`kiem-re-cua-fail-close-chua-co-ca`, của #674). Ngưỡng chủ kho là 0/0/0 nên chưa đạt. Hint áp sạch và cho 73/73 · 173/173.
Mức bảo đảm tối đa của lượt này là `advisory_review` (cùng họ model). Land vẫn cần Codex `cross_approved` hoặc `human_audited`.

TONG: P0=0 P1=0 P2=1 P3=1 — 2 lớp (cả hai của #674); nợ #694: 0 phát hiện mới.
