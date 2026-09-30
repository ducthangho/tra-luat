Reviewed commit: af1165d04977f2e3de1fa0fdbaa9a1775dd9bd30
verdict: changes_requested
reviewed_sha: af1165d04977f2e3de1fa0fdbaa9a1775dd9bd30
luot: 7 (packet #674 CI-DUONG-NHANH-HO-SO, thay Codex het quota)

TONG: P0=0 P1=0 P2=1 P3=1

## Doc lap — nói thẳng

Reviewer là **Claude (Opus 5.5)**, review mã do **Claude** viết. Cùng họ mô hình với executor ⇒ độ độc lập
YẾU HƠN một lượt Codex: điểm mù chung (cách nghĩ về "đường vào", chọn fixture) có thể lọt cả hai phía. Bù lại
bằng cách chỉ nhận kết luận nào có phép đo chạy được (đột biến trên bản sao, fixture git thật, audit hook).
Không có receipt runtime độc lập về model/effort. Verdict nội dung không cấp quyền land.

## Môi trường và cách đo

- Bản làm việc `scratchpad/rv7-by9j/cay` (clone, HEAD `af1165d0`, nhánh `dau`); `origin/master` là tổ tiên của HEAD.
  Mọi đột biến chạy trên **bản `git clone` riêng từng mutant** trong `scratchpad/rv7-by9j/tmp/mut/<tên>`,
  `PYTHONDONTWRITEBYTECODE=1`, `python -B`. `cay` sạch sau cùng (`git status --short` = 0 dòng).
- Linux, Python 3 hệ thống, actionlint 1.7.7 + shellcheck (có mặt). Không mạng GitHub, không chạy Actions thật.
- Spec: `git show 4105292:ops/specs/CI-DUONG-NHANH-HO-SO-r2.md` — sha256 `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57` (khớp lượt 6).
- Script đột biến của reviewer: `scratchpad/rv7-by9j/tmp/dot_bien_rv7.py` (35 mutant); log từng mutant ở `tmp/mutlog/`.

## Số đo nền (HEAD)

| Lệnh | Kết quả |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python ops/ci_duong_nhanh_test.py` | `CA: 63/63` · `DOT BIEN: 151/151` · `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT`, rc=0, 38,9s tường |
| `KIEM KE` | `hanh_vi=35 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=9 = 63 · dot bien dk=2 + ci.yml=65 + ci_duong_nhanh.py=44 + test=40 = 151` |
| `python .claude/dev/ci_dang_ky_test.py` (gpgsign tắt qua `GIT_CONFIG_*`) | `ĐĂNG KÝ: 23/23`, `PHẢN CHỨNG: 938/938 đỏ đúng`, `TỔNG: ĐẠT`, rc=0 |
| `actionlint .github/workflows/ci.yml` | rc=0 (shellcheck có mặt) |
| `git diff --numstat 89fc4fa HEAD -- .claude/dev/ci_dang_ky_test.py` | `1 0` |
| Suite với HINT.patch (bản sao `tmp/hint`) | `CA: 69/69` · `DOT BIEN: 160/160` · `TU KIEM DAT` · `TONG: DAT`, rc=0; `ruff --select F` sạch |

## DOI CHIEU LUOT TRUOC (lượt 6, reviewed `abcafde0`)

| Lớp | Lượt 6 | Lượt 7 đo lại |
|---|---|---|
| `chot-yaml-chi-do-su-hien-dien` | P2: runner không gọi ca vẫn TONG DAT | **ĐÃ VÁ THẬT** cho biểu hiện đó: t92/t91 có mặt, mutant `test_runner_khong_goi_ca`, `test_entrypoint_rc1_thanh_0` nằm trong 151 và bị giết đúng ca. 11 mutant YAML mới của tôi (env `github.sha` ở bước phân loại/kiem-re, `fetch-depth: 1`, bỏ kiểm sự kiện ở output, mặc định `duong_nhanh`, `\|\| echo che_do=duong_nhanh`, bỏ `pipefail`, bỏ doctrine-scan, sai tên dòng liệt kê) **đều GIẾT** bằng ca hành vi thật (CA 61/63). Không đo được mutant YAML nào sống. |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | P3: thêm dòng KIEM KE sai vẫn xanh | **ĐÃ VÁ THẬT**: t94 so danh sách dòng `== [dong_kiem_ke()]`; mutant `test_main_in_them_dong_kiem_ke_sai` và `..._sai_truoc` trong 151, bị giết. |
| 5 lớp đã đóng | — | Không đo được hồi quy, trừ phần giao nêu ở finding P2 (các cửa **chưa từng có ca** của `kiem_lease`, không phải hồi quy của cửa đã vá). |

## BANG SAN — tìm lỗi THẬT của đường nhanh

HUONG 1 — bước bị bỏ có đọc dữ liệu hồ sơ không (lỗi "skip mà không nên")
  cách đo: audit hook Python (`sys.addaudithook`, qua `sitecustomize` trong `PYTHONPATH`) ghi mọi `open`/`scandir`
  dưới `ops/{land,leases,reviews,specs}` khi chạy TỪNG bước bị bỏ trên bản sao `tmp/aud` (script `tmp/chay_aud.sh`).
  output (`tmp/audlog/SUMMARY` + `*.aud`):
    golden rc=0, 0 sự kiện · determinism rc=0, 1080 scandir / 0 open · release-check rc=0, 360 scandir / 0 open ·
    release-bundle rc=0, 180 scandir / 0 open · gate_lifecycle rc=0, 0 · packet_loop_test rc=0, 206 sự kiện, 0 cái nào
    trong cây thật (toàn fixture tạm) · tl selftest `1715/1715` rc=0, 900 scandir / 0 open ·
    lease_publish_test rc=0: đọc `ops/leases`+`ops/reviews` (t23/t26/t27) và `ops/land`+`ops/specs` = 3 lần `copytree`
    cả cây (t82) + tệp prompt của t23.
  kết luận: **KHÔNG PHẢI LỖI.** Scandir là đi ngang của walk release rồi loại `ops/` (`_RELEASE_EXCLUDE_DIRS`).
  Dữ liệu hồ sơ duy nhất mà bước bị bỏ thực sự kiểm là t23/t26/t27 — đúng ba ca `kiem-re` chạy lại.
  Giới hạn: hook không thấy đọc qua `git show`/`ls-files`, và không thấy tiến trình con tự xoá `PYTHONPATH`.

HUONG 2 — phân loại diff biên (git fixture thật)
  gitlink (submodule 160000) ngoài allowlist + `ops/land/y.yaml` ⇒ `day_du` "1 tep ngoai allowlist: 'scripts/sub'".
  Ba chấm, rename, xoá, object thiếu, tên có dấu: phủ bởi t11–t15, không tái lập lại.
  `.gitattributes` `* -whitespace` trong `ops/land/` KHÔNG tắt được báo dấu xung đột: `git -c core.whitespace=… diff --check` rc=2, 3 dòng "leftover conflict marker" cả có lẫn không có tệp ấy.
  kết luận: **KHÔNG PHẢI LỖI** trong miền đo.

HUONG 3 — timeout 10/5/20 và output vắng
  Đọc ci.yml: `che_do: ${{ github.event_name == 'pull_request' && steps.phan-loai.outputs.che_do || 'day_du' }}`;
  bước phân loại chỉ ghi output ở cuối; checkout hỏng ⇒ tệp script vắng ⇒ rc≠0 ⇒ `continue-on-error` ⇒ output vắng ⇒ `day_du`.
  `actions/checkout` lấy `github.sha` của sự kiện (merge commit mà cha thứ hai là `head.sha` của sự kiện) nên không có đua
  "head đổi giữa sự kiện và checkout". Mutant `fetch-depth: 1`, mặc định `duong_nhanh`, bỏ kiểm sự kiện đều bị giết.
  kết luận: **KHÔNG PHẢI LỖI** (phân tích + đột biến; không tái hiện timeout thật của Actions — KHÔNG ĐO ĐƯỢC).

HUONG 4 — `kiem-re` phụ thuộc người bấm (GITHUB_ACTOR) → P3 dưới.

HUONG 5 — đột biến sản phẩm/ci.yml: 35 mutant, xem bảng dưới → P2 và P3 dưới.

## Bảng 35 mutant của reviewer (`tmp/mut_ket_qua.txt`)

GIẾT (TONG DO bằng ca hành vi): yaml_khong_tieu_thu_generator, lease_tep_xoa_break, lease_het_han_rc0,
lease_het_han_bo_qua_han_false, cadulieu_nem_thanh_dat, kiemre_luon_rc0, main_doi_so_la_thanh_0,
main_doi_so_la_chay_phan_loai, sach_bo_ord127, phan_loai_tu_diff_x_rong, doc_diff_them_diff_filter(AMR),
chan_bytes_strip_nul_cuoi, và 11 mutant YAML ở trên.

**SỐNG — TONG DAT, không tương đương** (9): `yaml_bo_duoi_yml`, `yaml_tep_xoa_break`, `yaml_thieu_pyyaml_cho_qua`,
`lease_thieu_pyyaml_cho_qua`, `lease_nem_bo_qua`, `lease_parse_loi_bo_qua`, `lease_han_date_khong_tz_la_het`,
`diffcheck_nem_thanh_dat`, `diffcheck_rc_128_cho_qua`.

SỐNG nhưng TƯƠNG ĐƯƠNG / vô hại (không tính): `sach_bo_dau_gach_dau` (`/ops/…` vẫn bị chặn bởi thành phần rỗng),
`decode_replace` (không đổi phân loại), `lease_het_han_bat_moi_ngoai_le` (vẫn rc=8), `lease_khong_phai_dict_bo_qua`
(`.get` trên list ném AttributeError ⇒ kiem-re chết rc=1 — vẫn đỏ, chỉ xấu chẩn đoán).

Ghi chú tín dụng giả (không phải finding): `doc_diff_ignore_submodules` cho TONG DO nhưng `CA: 63/63` — nó "chết" chỉ vì
làm neo của 2 mutant có sẵn hết duy nhất (DOT BIEN 149/151), không ca hành vi nào bắt `--ignore-submodules`. HEAD không có
cờ ấy và phân loại gitlink đúng (HUONG 2), nên không mở finding; nêu để executor biết nếu muốn khoá thêm.

### kiem-re-cua-fail-close-chua-co-ca [P2] Chín cửa của ba helper `kiem-re` không có ca nào; gỡ chốt vẫn TONG DAT

TEP/DONG: `ops/ci_duong_nhanh.py` `kiem_yaml` (dòng 158–174), `kiem_diff_check` (177–187), `_han_lease` (190–200),
`kiem_lease` (203–243). Bộ test: `ops/ci_duong_nhanh_test.py` t20a–t21.

VAN DE: `kiem-re` là bước bù DUY NHẤT cho 8 bước nặng bị bỏ ở đường nhanh. HEAD đúng ở mọi cửa dưới đây (đã kiểm), nhưng
**không cửa nào có phản chứng**; mỗi đột biến sau cho `CA 63/63 · DOT BIEN 151/151 · TONG: DAT`:

| Mutant | Hậu quả nếu lọt vào master |
|---|---|
| `yaml_tep_xoa_break` (`continue`→`break` ở tệp đã xoá) | PR xoá `ops/land/a.yaml` + thêm `ops/land/b.yaml` hỏng ⇒ vòng dừng ở `a`, YAML hỏng QUA |
| `yaml_bo_duoi_yml` | `ops/land/*.yml` hỏng không được parse (t20g chỉ phủ `.yml` dưới `ops/leases/`, mà ở đó `kiem_lease` bắt hộ) |
| `lease_parse_loi_bo_qua` | lease NHIỀU tài liệu (`a\n---\nb`) ⇒ `kiem_yaml` (safe_load_all) cho qua, chỉ nhánh parse của `kiem_lease` bắt; gỡ ⇒ `continue` im lặng, lease **không được kiểm gì**. Đo HEAD: `kiem_yaml=[]`, `kiem_lease=["lease khong parse duoc: … ComposerError"]` |
| `lease_nem_bo_qua` | validator lease không spawn được ⇒ lease không kiểm mà vẫn DAT |
| `yaml_/lease_thieu_pyyaml_cho_qua` | thiếu PyYAML ⇒ hai kiểm trả `[]` (fail-open) |
| `lease_han_date_khong_tz_la_het` (nhánh `datetime` của `_han_lease`) | kho CÓ lease hạn không nháy ngoặc: `ops/leases/quy-trinh-lap-review-r15-g16-claude.yaml` (`2026-09-24T10:27:46Z` ⇒ PyYAML trả `datetime`). Đo: HEAD `[]`; mutant ⇒ đi `check` ⇒ `CHAN [8]: lease đã hết hạn` — PR thu hồi đúng lease đó sẽ ĐỎ oan. Mọi fixture của suite đều nháy ngoặc nên nhánh này chưa từng chạy. |
| `diffcheck_nem_thanh_dat`, `diffcheck_rc_128_cho_qua` | `git diff --check` ném/rc 128 ⇒ coi như sạch |

NGUYÊN NHÂN GỐC LỚP: các lượt trước vá theo từng đường reviewer chỉ (hạn/đuôi/rc của lease; ba ca dữ liệu); không ai
**liệt kê hết cửa fail-close** của cả ba helper rồi cho mỗi cửa một ca. Đúng hình dạng CLAUDE.md "VÁ ĐÚNG CHỖ ĐƯỢC CHỈ
RỒI BỎ SÓT ĐƯỜNG THỨ BA". Phần `kiem_lease` giao với lớp đã đóng `kiem-lease-bo-sot-duong-vao`: không phải hồi quy của
cửa đã vá, mà là cửa chưa từng có trong bảng — mở bằng bằng chứng đo (4 mutant TONG DAT).

DA THU VA: có — `out/HINT.patch` (chỉ `ops/ci_duong_nhanh_test.py`, +87 dòng): helper `_cay_tam` + sáu ca hành vi
`t20h`…`t20m`, mỗi ca một cửa, và 9 mutant bền trong `DOT_BIEN`, mỗi mutant neo duy nhất và đích đúng MỘT ca:
`t20h` ← kiem_yaml_bo_duoi_yml · `t20i` ← kiem_yaml_tep_xoa_cat_vong · `t20j` ← hai mutant thiếu PyYAML (patch
`sys.modules['yaml']=None`, đòi validator KHÔNG bị gọi) · `t20k` ← lease_nem_bo_qua + lease_parse_loi_bo_qua (kèm
đối chứng fixture: `kiem_yaml` PHẢI cho qua tệp nhiều tài liệu, để chứng minh chỉ nhánh parse của `kiem_lease` bắt) ·
`t20l` ← han_lease_bo_nhanh_datetime · `t20m` ← hai mutant diff-check.

DA THU NGHIEM: `git -C cay apply --check out/HINT.patch` ⇒ OK trên af1165d0. Bản sao `tmp/hint`: `CA: 69/69`,
`DOT BIEN: 160/160 bi giet dung ly do`, `KIEM KE: hanh_vi=41 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=9 = 69 · …
ops/ci_duong_nhanh.py=53 …= 160`, `TU KIEM PHAN HANG: DAT`, `TONG: DAT`, rc=0; `ruff check --select F` sạch.
Harness tự xác nhận 9 mutant mới chết ĐÚNG ca đích (không tín dụng giả). Nhãn: **chưa chạy trên cây thật — executor tự áp,
tự đo, tự chịu trách nhiệm commit.**

Rủi ro hint: `t20j` dựa vào `mock.patch.dict(sys.modules, {"yaml": None})` làm `import yaml` trong helper ném
`ImportError` (hành vi CPython chuẩn). Ca không đụng `GITHUB_ACTOR` (dùng đồ giả, không validator thật).

### kiem-re-phu-thuoc-actor-su-kien [P3] Đường nhanh thêm một điều kiện ĐỎ mà đường đầy đủ không có: người bấm không phải `ducthangho`

TEP/DONG: `ops/ci_duong_nhanh.py:229–235` (gọi `lease_publish.py check` / `kiem(bo_qua_han=True)`), `ops/lease_publish.py:852`
(chốt `GITHUB_ACTOR ∉ NGUOI_CO_THAM_QUYEN = ("ducthangho",)`).

VAN DE: đo trên lease thật hợp lệ `ops/leases/ci-noi-bang-vao-gate-exec-1-claude-20260822.yaml` qua `kiem_lease`:
`GITHUB_ACTOR` rỗng hoặc `ducthangho` ⇒ `[]`; `chatgpt-codex-connector[bot]` hoặc `claude[bot]` ⇒
`kiem lease (het han) rc=8 … CHAN [4]: GITHUB_ACTOR=… không có thẩm quyền cấp lease`. Trong Actions, `GITHUB_ACTOR` của
`pull_request` là người gây sự kiện. Nên một PR hồ sơ chạm `ops/leases/**` do bot/cộng tác viên đẩy ⇒ `gate-ops` ĐỎ, trong khi
đường đầy đủ (`lease-publish selftest`, t23 chỉ kiểm băm prompt) KHÔNG chạy `kiem` với actor ⇒ XANH. Tác giả không có cách
chọn `day_du` ngoài việc chạm một tệp ngoài allowlist. Fail-close (chặn, không mở) nên P3; đúng chữ "lease_publish.py check"
của đặc tả, nhưng hệ quả "ai bấm quyết định màu" chưa được khai ở docstring D2.
DA THU VA: không vá mã (đây là lựa chọn chính sách của chủ kho). Đề xuất: khai thẳng trong docstring D2 và/hoặc ghi nợ; nếu chủ
kho muốn tách, lựa chọn là chạy kiểm lease với `GITHUB_ACTOR` đã lọc (như fixture t23) — KHÔNG làm khi chưa có quyết định,
vì chốt actor là lớp danh tính duy nhất GitHub xác thực.

### (ghi nhận, KHÔNG phải finding riêng — thuộc P2 trên) nhánh `datetime` của `_han_lease` là đường thật của kho

Tách riêng để không bị đọc thành lỗi lý thuyết: 1/113 lease trên cây dùng hạn không nháy ngoặc (grep
`lease_expires_at_utc: 20`), nên cửa này có người dùng thật. Đã tính vào P2, không cộng thêm vào TONG.

## KHÔNG ĐO ĐƯỢC

- GitHub Actions thật: timeout 10/5/20 phút khi treo, cancel, fork PR, `base.sha` cũ/mới trên PR rebase, runner Windows.
- `GITHUB_ACTOR` thực tế của các PR hồ sơ trong kho (ai/bot nào đẩy) — không truy cập được API; P3 actor dựa trên cơ chế đo tại chỗ.
- Bia mộ hai chiều khi runner chỉ có refs của checkout: trên `cay` (ít ref) lease `r378-symlink-doi-dac-quyen-r43-g43-claude.yaml`
  trượt `CHAN [8]` bia mộ — cùng giới hạn refs đã khai ở docstring D2, không mở lại.
- Audit hook không thấy đọc qua tiến trình git hay tiến trình con xoá `PYTHONPATH`.
- Nghiệm thu 11 (PR thật, thời gian tiết kiệm): chưa có PR thật.
- `tl selftest` chạy trên bản sao với audit hook (1715/1715) — không phải lượt gate chính thức; ruff tl.py không đổi vì
  `git diff origin/master HEAD -- scripts/` rỗng (delta = 0 theo blob, không chạy ruff lại).

## KET LUAN

`changes_requested` — P0=0 P1=0 **P2=1** (`kiem-re-cua-fail-close-chua-co-ca`, 9 mutant TONG DAT, hint giết cả 9)
**P3=1** (`kiem-re-phu-thuoc-actor-su-kien`). Nhánh datetime `_han_lease` thuộc P2, không đếm riêng. Hai lớp kế thừa của lượt 6 đã vá thật và không đo được mutant sống mới trong chúng. Phân loại diff và
tập bước bị bỏ: không tìm được đường nào cho `duong_nhanh` khi lẽ ra `day_du`, không bước bỏ nào đọc dữ liệu hồ sơ ngoài
t23/t26/t27.
