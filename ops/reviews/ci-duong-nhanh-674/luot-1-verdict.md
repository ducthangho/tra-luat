verdict: changes_requested
reviewed_sha: 1687c693c622177742807f0a2abd765547b0e748
Reviewed commit: 1687c693c622177742807f0a2abd765547b0e748

## DOI CHIEU LUOT TRUOC

Lượt 1, chưa có lượt trước. Review độc lập hai trục Spec và Standards/Security; ngưỡng áp dụng: P0=P1=P2=P3=0 mới approve. Chưa đạt ngưỡng.

- Base: `1741e0a1ab7ebce4b26912aefadca56ddfcdc691`; tree head: `22650f29226d713762e5269612dc8fd24222d701`.
- Đã đọc trọn SPEC-r2; SHA256 `b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57` khớp. Đối chiếu AGENTS.md, CLAUDE.md và protocol §8/8.3.
- Đúng bốn tệp trong write set. `.claude/dev/ci_dang_ky_test.py` chỉ thêm một dòng vào DA_NOI (`numstat 1 0`). Không sửa mã nguồn/commit/index của checkout.
- Reviewer: OpenAI Codex qua công cụ thực thi máy trong phiên này; danh tính model cụ thể/effort/launcher receipt không tự đo được từ bundle. Không suy identity từ tài khoản GitHub, không phát hành receipt hay cấp quyền land. Executor Claude theo prompt, chưa có runtime receipt để kiểm độc lập.
- Linux, Python 3.11 tại chỗ; không chạy Windows CI, không mạng. Actions khai Python 3.12: kết quả local không được gọi là kết quả Actions.
- Mọi đường dẫn lệnh dưới tương đối với workspace `rv1`, trừ chỗ ghi `cd cay`. Mọi phép dùng temp đã đặt `TMPDIR=$PWD/tmp` từ workspace; Python dùng `-B`/`PYTHONDONTWRITEBYTECODE=1`. Log và bản sao ngoài checkout, trong `out/`, `tmp/`.
- Giới hạn read-only: lượt `tl --selftest` đầu chạy trong `cay` theo danh sách lệnh giao đã sinh tệp **ignored** ở `references/golden/fixtures/` và `scripts/.tl_state/`. Các lượt sau chuyển sang `tmp/head-run`. Không có tracked/index diff. Snapshot nội dung đầu tiên được lấy sau khi bắt đầu test, nên không tuyên bố đã đo toàn bộ ignored trước test hay rằng cây chưa từng bị ghi. Không xóa dấu vết để làm sạch báo cáo.

## BANG LOP

Nguồn mọi lớp: lượt 1 / SHA ở đầu báo cáo. Tổng **5 lớp**, chi tiết các cửa vào bên dưới.

| Slug | Các biểu hiện/cửa vào | Hạng cao nhất mở | Phương án vá chung | Phép kiểm đóng lớp |
|---|---|---|---|---|
| `kiem-lease-bo-sot-duong-vao` | Lease hết hạn bỏ toàn bộ check; lease `.yml` không được check | P2 | Gọi check cho mọi lease YAML còn tồn tại, không dùng hạn để miễn kiểm | Cùng fixture thiếu trường trên `.yaml`/`.yml`, hết/còn/hỏng/thiếu hạn đều đỏ; tái lập hai mutant riêng |
| `diff-check-tu-ha-nguong` | Bỏ trailing-space, blank-at-EOF và space-before-tab | P2 | Giữ phép `git diff --check` theo đặc tả; không tự thêm ngoại lệ toàn miền | Fixture đã có t20d phải đỏ đúng whitespace; từng loại có mutant riêng |
| `chot-yaml-chi-do-su-hien-dien` | Nuốt lỗi ở step/job; lệnh chỉ còn comment; shell sai | P2 | Kiểm cấu trúc thực thi, shell và error propagation, không chỉ substring | Baseline xanh; mỗi cửa có mutant riêng đỏ đúng y06/y08; full suite vẫn xanh |
| `dac-ta-bo-mat-kiem-du-lieu-ho-so` | Tắt cả lease suite làm mất t27 trên chính miền review được cho chạy nhanh; t23/t26 cũng nằm trong suite bị bỏ | P2 | Đóng băng danh sách kiểm dữ liệu rẻ phải giữ; tách chạy các ca đó | Xóa mục lục/entry/caveat hoặc làm lệch dữ liệu phải đỏ trước merge; push đầy đủ vẫn hoạt động |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | 6/113 không tái lập; bỏ sót phân rã ca và mô tả tự kiểm sai số/sai loại | P3 | Đo cùng scope SHA+refs; kiểm kê mọi khẳng định mới, sửa diễn giải | 113 lease đối chiếu với tập refs; số ca/nhánh tự kiểm lấy từ cấu trúc và khớp doc |

## BANG SAN

### HUONG 1: Phân loại và ba trạng thái fail-close

- gia thuyet: SHA hỏng/git lỗi hoặc push/dispatch có thể rơi vào nhanh hay gọi git không đúng.
- lenh: `cd cay && python3 -B ops/ci_duong_nhanh_test.py`; `python3 -B out/audit-summary.py`.
- output: `CA: 43/43 dat · 0 do · 0 hong`; `DOT BIEN: 55/55 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT`; `TONG: DAT`, rc=0. Các t01/t02/t03/t05/t06/t07/t08 chạy riêng đều `('DAT', '')`.
- ket luan: **KHONG PHAI LOI** trong các ca đã đo. Phân hạng có kiểm rc=4/KeyError thành tín dụng giả; không dùng rc=0 đơn độc làm bằng chứng.

### HUONG 2: Ba chấm, rename, object thiếu, tự phân loại

- gia thuyet: base tiến thêm hoặc rename mã vào allowlist làm chọn sai đường.
- lenh: `python3 -B out/audit-summary.py` (gọi t11, t12, t15 với kho Git thật sẵn trong suite).
- output: ba ca `('DAT', '')`; `.py` dưới `ops/land` cho `duong_nhanh`.
- ket luan: **KHONG PHAI LOI** theo Q2 (bốn prefix, không lọc đuôi). Chỉ chứng minh Git local. Fork/rebase/synthetic merge GitHub: **KHONG DO DUOC**. Tệp phân loại/workflow tự chạy từ cây PR được code khai rõ là giới hạn trust; không tự soạn payload tấn công. Các fixture traversal/control-character có sẵn đã chạy trong suite, không sinh payload thoát cây mới. Symlink/mode thực tế của PR trên GitHub chưa đo.

### HUONG 3: Lease hết hạn và đuôi YAML

- gia thuyet: lease parse được nhưng thiếu nội dung bắt buộc vẫn xanh do lọc trước check.
- lenh: `python3 -B out/reviewer-probes.py`; `python3 -B out/spec-probes.py`.
- output: `expired kiem-re rc=0`/direct check `rc=8 thiếu ... packet_issue, granted_by, reviewed_sha_required`; `live-yml kiem-re rc=0`/direct check `rc=8`; đối chứng `live-yaml kiem-re rc=1`/check `rc=8`. Mở rộng `.yml` trên bản sao: toàn suite vẫn 43/43, 55/55.
- ket luan: **LOI**, lớp `kiem-lease-bo-sot-duong-vao`.

### HUONG 4: Whitespace bị nới

- gia thuyet: bước mang tên diff --check không thực hiện chuẩn check đã đóng băng.
- lenh: `python3 -B out/reviewer-probes.py`; `python3 -B out/spec-probes.py`.
- output: fixture whitespace `kiem-re rc=0` đối chứng `git diff --check rc=2`. Bản sao bỏ `-c CAU_HINH_WHITESPACE` làm t20d rc=3, thông báo chứa `new blank line at EOF` và `trailing whitespace`.
- ket luan: **LOI**, lớp `diff-check-tu-ha-nguong`. Mutant phục hồi chuẩn bị bộ test hiện tại giết vì test đang bảo vệ ngoại lệ ngoài spec.

### HUONG 5: Chốt YAML có răng đối với cổng kiểm rẻ không

- gia thuyet: nuốt lỗi hoặc comment lệnh vẫn được tính là cổng đã nối.
- lenh: `python3 -B out/reviewer-probes.py`; `python3 -B out/entry-probes.py`; `python3 -B out/hint-probe.py`.
- output: ba mutant độc lập `cheap-continue`, `cheap-comment`, `ops-job-continue`: **rc=0, CA 43/43, DOT BIEN 55/55, TONG DAT**. Mở rộng từng cửa: `gate-continue`, `gate-ops-continue`, `gate-packet-loop-continue`, comment riêng doctrine, comment riêng kiem-re, shell pwsh: mỗi cửa **CA 43/43**, không ca lỗi. Hint thử trên bản sao: baseline y06/y08 rc=0; ba mutant đầu rc=3 với `DO:y08...kiem-re khong duoc nuot loi`, `DO:y08...phai chay DUNG hai lenh`, `DO:y06...job bat buoc khong duoc nuot loi`; full hint suite 43/43 + 55/55, rc=0.
- ket luan: **LOI**, lớp `chot-yaml-chi-do-su-hien-dien`. Đây là bằng chứng độ phủ test, không nói checkout hiện tại đã có continue-on-error ở gate-ops.

### HUONG 6: Mất kiểm dữ liệu review ở đường nhanh

- gia thuyet: bỏ cả suite lease làm dữ liệu review không hợp lệ qua đường nhanh rồi chỉ đỏ sau land.
- lenh: `python3 -B out/review-index-probe.py`; đọc `ci.yml` 561–599, `lease_publish_test.py` 908–944/1269–1412.
- output: bản sao dữ liệu thật `original t27=DAT`; bỏ README `t27=DO AssertionError thiếu ... ops/reviews/README.md`; kho Git fixture xóa cùng path: `deletion classifier=duong_nhanh`, `deletion kiem-re=(0,...kiem-re DAT...)`.
- ket luan: **LOI DAC TA / danh sách bước giữ chưa đủ**, lớp `dac-ta-bo-mat-kiem-du-lieu-ho-so`. Không quy việc bỏ suite nặng là làm trái M2; chính M2 yêu cầu bỏ suite, nhưng còn thiếu danh sách ca kiểm dữ liệu phải giữ.

### HUONG 7: Job, ma trận, required checks và concurrency

- gia thuyet: đổi gate-registry, ma trận hoặc đặt if sai lớp làm check mất.
- lenh: `python3 -B out/audit-summary.py` (so YAML head với `git show 1741e0a:.github/workflows/ci.yml`, chạy y03/y06/y07).
- output: `registry_same=True`, `concurrency_same=True`, `matrix_output_same=True`; ba job `needs=chuan-bi`, `if=None`, số bước bỏ 5/3/1; y03/y06/y07 DAT. Cgroup giữ điều kiện Linux; lifecycle nền khác giữ `!=Linux`. G5 và gate-registry không bị đường nhanh bỏ.
- ket luan: **KHONG PHAI LOI** về các cấu trúc hiện có. Push/dispatch output đầy đủ, nên suite bị bỏ trên PR sẽ bật lại. Không chứng minh hành vi GitHub khi job bị skipped/cancelled/runner không khởi động. Không coi check skipped là pass; không xác nhận thực nghiệm lời khai đó của executor.

### HUONG 8: Lint/shell/YAML và registry

- gia thuyet: expression trong comment run hoặc test mới chưa đăng ký có thể lọt.
- lenh: `actionlint .github/workflows/ci.yml` trong cay; `actionlint tmp/baseline/.github/workflows/ci.yml`; `actionlint tmp/actionlint-comment.yml`; `python3 -B .claude/dev/ci_dang_ky_test.py` trên head và archive base.
- output: actionlint head/base rc=0; ShellCheck 0.9.0; mutant `${{ }}` trong comment run rc=1 `unexpected end of input`. Registry head `23/23`, baseline `22/22`, cả hai `PHẢN CHỨNG: 938/938 đỏ đúng`, `TỔNG: ĐẠT`, rc=0; numstat `1 0`.
- ket luan: **KHONG PHAI LOI**. Registry lần đầu rc=1 vì `/root/.gitconfig` bật ký commit; lần đo hợp lệ dùng `GIT_CONFIG_COUNT=2`, tắt ký commit và ghim abbrev cho tiến trình. Không sửa Git config của checkout. SHA truyền qua env, không nội suy trực tiếp vào shell; git dùng argv list và SHA fullmatch.

### HUONG 9: Số đo lịch sử và bảng bằng chứng

- gia thuyet: số đếm phụ thuộc refs trôi hoặc bảng bỏ sót lời khai mới.
- lenh: `cd cay && python3 -B ../goi/do_lai_so.py`; `python3 -B out/audit-summary.py`; đọc AST/tuple trong `tu_kiem_phan_hang`.
- output: `345` merge đo được, `63` toàn allowlist, `8` raw diff-check đỏ (khớp); `113` lease, `dat 113, truot 0` (**khác 6**). 552 refs, digest ở BANG DO. t=31 (có t99), y=9, k=3; `t22 present=False`; tự kiểm gồm 5 mẫu rc và 3 mutant thực, không phải “bốn ca ... ba ... sai tên” như docstring. Bảng DO_LAI không kê các lời khai phân rã này.
- ket luan: **LOI**, lớp `bang-do-thieu-neo-va-thieu-kiem-ke`. Lần chạy do_lai sai cwd ban đầu (0/ImportError) bị loại, không dùng làm finding.

### HUONG 10: Runtime gate và manifest

- gia thuyet: sửa CI/test kéo theo lệch runtime/manifest hoặc ruff.
- lenh: Ruff F JSON scripts/tl.py trên head/base; Ruff F hai file mới; `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` trong tmp/head-run; `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .`; `python3 -B scripts/tl.py --selftest`.
- output: Ruff head/base 12/12 lỗi với cùng diagnostics (delta=0), hai file mới sạch; manifest `ok=true expected=checked=180`; doctrine-scan sạch 10 tệp/0 chỗ. Selftest đầu 1714/1715 vì cấu hình reviewer ép abbrev=7 qua môi trường đè lên phép A/B 7/8 của r226. Lượt hợp lệ trong tmp/head-run, chỉ tắt ký commit và giữ core.abbrev repo-local: **1715/1715, rc=0** (`out/tl-selftest-correct-env.log`).
- ket luan: lint/manifest/doctrine/selftest **KHONG PHAI LOI**; không tính lần đỏ do rig là lỗi packet.

## BANG DO

| Khẳng định | Đã khai trong DO_LAI? | Reviewer đo được | Khớp? |
|---|---|---|---|
| 43 ca / 55 mutant giết đúng | Có | 43/43, 55/55, tự kiểm DAT | Có, trong phạm vi mutant có sẵn; không đủ chứng minh các cửa ngoài danh sách |
| Registry baseline 22/22 → 23/23, 938/938 | Có | Cả hai bộ chạy đầy đủ, rc=0, đúng số | Có |
| Registry diff một dòng | Có | `1 0` | Có |
| actionlint head/base 0, ShellCheck 0.9.0, empty-expression mutant 1 | Có | Đã chạy từng phép | Có |
| Ruff tl 12, delta 0; hai file mới sạch | Có | Diagnostics head/base giống nhau; mới sạch | Có (bare lint; không gộp với RUFF CI contract) |
| AL_VER 4 | Có | 4, gate-registry/JOB_G5 không đổi | Có; chưa phải nền sau #668 |
| 345 merge / 63 hồ sơ / 8 raw-check đỏ | Có | 345/63/8 | Có; không ngoại suy thành thời gian CI hay PR thật |
| Lease lỗi 6/113 với bo_qua_han=True | Có | **0/113 lỗi**, rc script=0 | **Không tái lập**; validator còn quét mọi refs cho bia mộ |
| “t01..t22”; tầng registry k01/k03 | **Không** | Không có t04/t22; có 30 t-case hành vi + t99, 9 y-case, 3 k-case (gồm k02) | Thiếu/sai inventory |
| “Bốn ca tự kiểm ... ba đột biến thật (sống sót · lỗi vô can · sai tên)” | **Không** | 5 mẫu rc; ba mutant thật = KeyError, comment tương đương, nới allowlist. Sai tên chỉ nằm trong mẫu rc giả | Không |
| 46,5/52 phút, GitHub skipped được coi đạt | Có, khai chưa đo | Không mạng/không PR thật | KHONG DO DUOC; không xác nhận |
| tl selftest | Spec nghiệm thu 10 | 1715/1715, rc=0, môi trường hợp lệ | Đạt |
| Manifest strict | Spec yêu cầu đo | `ok=true`, 180/180 | Đạt |

Scope refs của phép lease: `git -C cay for-each-ref --format='%(refname) %(objectname)'` có 552 dòng, SHA256 `1864bff1c7c8d73aff4f47dc0e0dc6420127786dbd86a843c96662ec13e4697f`. Hàm `_kiem_bia_mo` gọi `_quet_lease_toan_kho(...doi_chieu_ref=False)`: HEAD/base đơn độc chưa định danh hết đầu vào. Không kết luận số 6 chưa từng đúng ở một bộ refs khác.

Đo bổ sung `python3 -B out/acceptance-extra.py`: đổi kết quả toàn allowlist thành day_du → `GIET` đúng t01; bỏ DA_NOI → `23/22`, `test sống chưa đăng ký: ops/ci_duong_nhanh_test.py`; bỏ lời gọi → `23/23` nhưng có lỗi `CI không gọi mục đăng ký: ops/ci_duong_nhanh_test.py`.

Đối chiếu nghiệm thu: 1–7 có bằng chứng suite/đột biến đã tự chạy; 8 có head/base actionlint + mutant rỗng; 9 có hai số trước/sau, 938/938 và hai mutant DA_NOI/lời gọi trong suite; 10 ruff delta=0, selftest 1715/1715 rc=0 trên bản sao cùng head; 11 **CHUA_DO_DUOC**, không PR thật, không khai đạt. M1/M3/M4 đạt ở các ca đo local; M2 chưa đủ do các finding kiểm rẻ/dữ liệu dưới đây. Q5/#668 là điều kiện tích hợp chưa xác nhận: baseline được giao vẫn có 4 AL_VER và JOB_G5 ba job cũ; không coi kết quả này là approval cho head sau rebase/land #668.

## FINDINGS

### kiem-lease-bo-sot-duong-vao [P2] Đừng miễn toàn bộ check theo hạn và bỏ sót lease `.yml`

TEP/DONG: `ops/ci_duong_nhanh.py:197`, `:210–214`; test `t20a`, `t20e`, `t21`.

VAN DE: M2 giữ `lease_publish.py check` cho lease đổi, không cấp ngoại lệ “hết hạn”. Fixture **đã có sẵn** `LEASE_HET_HAN` thiếu cả packet_issue/granted_by/reviewed_sha_required vẫn được báo `kiem-re DAT`. Lỗi không chỉ là hạn: gọi validator trực tiếp đỏ vì thiếu schema. Cửa thứ hai là `.yml`: `kiem_yaml` nhận cả hai đuôi nhưng `kiem_lease` chỉ nhận `.yaml`, trong khi các reader lease hiện có nhận cả `.yaml/.yml`. Cùng lease còn hạn sai schema đổi đuôi là từ đỏ sang xanh. Các cửa cần khóa: `.yaml` và `.yml`, hạn quá khứ/bằng giờ/còn hạn/hỏng/thiếu; giữ phân biệt tệp đã xóa với tệp còn tồn tại.

DA THU VA: **có, từng phần trên bản sao** — khôi phục gọi check qua điều kiện hạn và mở `.yml`; không sửa cay. Hướng tối thiểu dưới đây là hint, không phải patch đã được áp vào sản phẩm:

```diff
--- ops/ci_duong_nhanh.py
+++ ops/ci_duong_nhanh.py
@@
-    for duong in sorted(x for x in doi if x.startswith("ops/leases/") and x.endswith(".yaml")):
+    for duong in sorted(x for x in doi if x.startswith("ops/leases/") and x.endswith((".yaml", ".yml"))):
@@
-        han = _han_lease(lease.get("lease_expires_at_utc"))
-        if han is not None and han <= bay_gio:
-            print(f"DUONG_NHANH: lease {duong!r} da het han - `check` la cong DANG lease (rc=8 theo thiet ke), "
-                  "chi con phep YAML-parse", file=ra)
-            continue
```

Chốt riêng: t21 phải mong có lời gọi cho lease hết hạn; thêm fixture hết hạn **sao đủ lease_publish.py** và đòi rc=1/diagnostic validator. t20e chạy cùng fixture có sẵn cho cả hai đuôi. Mutant 1 phục hồi `continue` theo hạn phải đỏ ca hết hạn; mutant 2 rút tuple về `.yaml` phải đỏ ca `.yml`. Sửa t20a vì fixture “sạch” hiện chứa lease thiếu schema, không đổi expected tùy tiện để làm suite xanh. Nếu nhu cầu bookkeeping cần chấp nhận lease hết hạn, ghi **DAC TA cần quyết định của chủ kho**; executor không tự nới luật hay bắt reviewer sửa SPEC-r2.

DA THU NGHIEM: `out/reviewer-probes.py` đo cả hai false-green, direct check rc=8, đối chứng `.yaml` rc=1. `out/spec-probes.py`: phục hồi gọi check làm t21 đỏ đúng tập lời gọi; thêm `.yml` vẫn full 43/43 + 55/55, chứng minh thiếu chốt. t20a cũng đỏ nhưng vì fixture thiếu script rc=2; **không tính lượt đỏ t20a là giết đúng lỗi schema**.

Rủi ro vá: lease hết hạn hợp lệ cũng sẽ đỏ theo check hiện hành; đó là hệ quả của spec đóng băng, cần quyết định rõ nếu muốn ngoại lệ, không được lặng lẽ bỏ toàn bộ validation.

DO TIN: cao.

### diff-check-tu-ha-nguong [P2] Phép kiểm rẻ vô hiệu hóa ba loại lỗi whitespace ngoài đặc tả

TEP/DONG: `ops/ci_duong_nhanh.py:62`, `:162–171`; `ops/ci_duong_nhanh_test.py:t20d`.

VAN DE: M2 giữ `git diff --check`. Code tự ghi “khác chữ trần” rồi truyền `core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab`. Ngoại lệ áp toàn miền hồ sơ, không chỉ dòng nội dung patch, và không có trong SPEC-r2. Con số lịch sử 8/63 mô tả một sự đánh đổi, không cấp quyền đổi acceptance. t20d và mutant đang bảo vệ hành vi lệch spec.

DA THU VA: **có trên bản sao**, khôi phục lệnh raw:

```diff
--- ops/ci_duong_nhanh.py
+++ ops/ci_duong_nhanh.py
@@
-        r = chay(["git", "-c", CAU_HINH_WHITESPACE, "diff", "--check", "--no-renames", f"{goc}...{dau}"],
+        r = chay(["git", "diff", "--check", "--no-renames", f"{goc}...{dau}"],
```

Chốt riêng: t20d đổi kỳ vọng thành đỏ vì whitespace; giữ fixture conflict-marker t20c và fixture sạch làm đối chứng. Tách kiểm trailing space / newline EOF / space-before-tab; mỗi cấu hình `-<loại>` riêng phải làm ca tương ứng đỏ. Đổi tên/chiều mutant `diff_check_bo_tinh_chinh_whitespace`: mutant phải **thêm nới lỏng** vào bản đúng, không “giết” bản khôi phục chuẩn. Gỡ hằng/import/comment không còn đúng khi executor tái dẫn xuất.

DA THU NGHIEM: `out/reviewer-probes.py`: raw check rc=2/kiem-re rc=0 cùng fixture. `out/spec-probes.py`: t20d rc=3, diagnostic whitespace đúng; không lỗi hạ tầng. Riêng space-before-tab chưa dựng thêm fixture mới; phải thêm ca đóng cửa này, không suy từ hai lỗi kia.

Rủi ro vá: hồ sơ chứa patch/Markdown có whitespace chủ ý sẽ đỏ. Nếu chủ kho muốn ngoại lệ phải xử lý ở đặc tả/chuẩn của kho, không dùng số lịch sử làm approval ngầm.

DO TIN: cao.

### chot-yaml-chi-do-su-hien-dien [P2] Suite vẫn xanh khi cổng kiểm rẻ bị vô hiệu hóa

TEP/DONG: `ops/ci_duong_nhanh_test.py:674–678`, `:700–715`; phạm vi `y06`, `y08`.

VAN DE: y08 tìm substring lệnh, nên comment được tính là thực thi; không khóa shell và `continue-on-error`. y06 chỉ cấm if ở job, bỏ qua `continue-on-error` của cả ba required jobs. Đã liệt kê từng cửa: nuốt rc ở bước kiểm rẻ; comment doctrine-scan; comment kiem-re; thay bash bằng pwsh; nuốt rc ở gate, gate-ops, gate-packet-loop. Sai shell có thể gây đỏ oan; các cửa còn lại có thể làm mất tác dụng cổng mà suite vẫn báo đủ. Đây là thiếu răng của cổng mới, không phải yêu cầu xây ranh giới chống tác giả chủ động sửa cả test lẫn workflow.

DA THU VA: **có**. [HINT.patch](HINT.patch) chỉ sửa test, đã kiểm áp `patch -p0 --fuzz=0 --dry-run` trên bản sao (rc=0). Nhãn: **chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem commit**.

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
         bang("if" not in wf["jobs"][job], f"{job}: KHONG duoc co `if:` cap job — check se VANG MAT thay vi bao ket qua")
+        bang(wf["jobs"][job].get("continue-on-error", False) is False,
+             f"{job}: job bat buoc khong duoc nuot loi")
@@
     run = str(b.get("run", ""))
+    bang(b.get("continue-on-error", False) is False, "kiem-re khong duoc nuot loi")
+    bang(b.get("shell") == "bash", "kiem-re can shell bash")
+    bang([d.strip() for d in run.splitlines() if d.strip()] == [
+        "set -euo pipefail",
+        "python .claude/dev/packet_loop.py doctrine-scan --root .",
+        "python ops/ci_duong_nhanh.py kiem-re",
+    ], "kiem-re phai chay DUNG hai lenh, khong chap nhan comment/nuot rc")
```

Chốt riêng: thêm mutant độc lập cho cả bảy cửa nêu trên vào DOT_BIEN, neo duy nhất, đòi baseline xanh và đúng y06/y08 đỏ (không nhận actionlint/shell crash là giết test đúng). Lệnh thêm sau này phải cập nhật danh sách chuẩn có review. Nếu thêm kiểm dữ liệu ở finding kế, điều chỉnh expected run đồng bộ; không giữ hint nguyên văn máy móc.

DA THU NGHIEM: `out/hint-probe.py`: baseline y06/y08 rc=0; bước continue, comment hai lệnh, job gate-ops continue đều rc=3 đúng ca/lý do; full suite với hint rc=0, 43/43, 55/55, tự kiểm DAT. `out/entry-probes.py` đo riêng sáu biểu hiện mở rộng trên bản gốc: 43/43 từng cửa. Sau hint, `out/hint-entries.py` đã đo riêng **7/7 cửa**, mỗi cửa rc=3 đúng y06/y08; patch áp thật trên bản sao bằng `patch -p0 --fuzz=0`, rc=0. Không tính thêm `.yml` (một sửa đúng còn sống) như mutant sai của lớp này.

Rủi ro vá: whitelist run chặt sẽ yêu cầu cập nhật khi đổi lệnh hợp lệ; đây là chủ đích cho cổng authority nhỏ. Không mở rộng JOB_G5/ci_dang_ky logic trái Q6.

DO TIN: cao.

### dac-ta-bo-mat-kiem-du-lieu-ho-so [P2] DAC TA cần giữ kiểm dữ liệu thật khi bỏ suite lease

TEP/DONG: `SPEC-r2.md` M2 và danh sách bước giữ tối thiểu; `.github/workflows/ci.yml:592–599`; chú thích cũ `:561–578`; `ops/lease_publish_test.py:1305`.

VAN DE: Spec yêu cầu bỏ lease-publish selftest, nhưng suite này chứa cả kiểm dữ liệu kho thật. t27 kiểm mục lục/caveat của `ops/reviews`, đúng một prefix luôn chọn nhanh. Xóa README vẫn nhanh và kiem-re DAT; t27 nguyên gốc lập tức đỏ. Cổng được thiết kế để chặn trước merge mất ở PR hồ sơ rồi bật lại trên push master, khiến lỗi được phát hiện quá muộn. Comment kế bước bị bỏ vẫn khẳng định t27 phải chặn trước master. Đây là thiếu phân tách của **DAC TA/danh sách bước cần đóng băng qua review**, không yêu cầu executor sửa đặc tả.

Cửa cần kiểm kê: README bị xóa; dòng mục lục bị xóa; verdict/receipt mới không có trong bảng; caveat mất khỏi bảng; ngoài t27 còn t23 (neo prompt lease thật) và t26 (băm/evidence_url receipt thật). Các chốt về mã workflow nằm ngoài prefix sẽ vẫn full. Không khẳng định bien-nhan-v2 thay được toàn bộ kiểm legacy/t27 chỉ vì job ấy còn chạy.

DA THU VA: **chưa áp workflow** (authority); đã thử gọi t27 riêng trên bản sao dữ liệu thật. Hướng cụ thể đề nghị chủ kho đóng băng: giữ các ca kiểm dữ liệu rẻ ngoài nhánh bỏ suite nặng, ít nhất t27. Ví dụ hướng trong workflow sau doctrine-scan, trong cùng khối bash kiểm rẻ:

```diff
--- .github/workflows/ci.yml
+++ .github/workflows/ci.yml
@@
           python .claude/dev/packet_loop.py doctrine-scan --root .
           python ops/ci_duong_nhanh.py kiem-re
+          python -c "import runpy; runpy.run_path('ops/lease_publish_test.py')['t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc']()"
```

Đây chỉ là hướng/diff trong finding, không có workflow patch artifact. Executor nên gói checker rẻ rõ ràng trong phạm vi được cấp; rà t23/t26 và quyết định giữ hay chứng minh được thay tương đương. `check` lease hiện tại không tự chứng minh mục lục review đúng. Không thêm lệnh gọi thẳng toàn bộ suite rồi gọi đó là nhanh.

Chốt riêng: xóa README trên bản sao → kiểm rẻ đỏ; xóa entry/caveat, để lại verdict/receipt thật → đỏ; mutate bỏ lời gọi checker riêng trong workflow → y08 đỏ. Với t23/t26 nếu giữ hoặc thay bằng checker khác, mỗi cửa prompt/hash/evidence_url cần mutant riêng, đối chứng dữ liệu thật xanh. Những hướng chưa chạy ở lượt này không được coi đã đóng lớp.

DA THU NGHIEM: `python3 -B out/review-index-probe.py` cho original t27 DAT, without-index DO đúng thiếu README; classifier deletion nhanh, kiem-re rc=0. Push/dispatch không chọn nhanh theo t03 và output YAML: suite bật lại, không chữa việc bỏ chốt trước merge. Chưa chạy GitHub PR thật.

Rủi ro vá: đọc hết hồ sơ có chi phí; phải đo từng checker và tránh kéo cả selftest nặng trở lại. Đây là đầu vào cho quyết định đóng danh sách M2, không phải thay Spec tự động.

DO TIN: cao cho lỗ t27; phạm vi thay thế t23/t26 cần đo riêng.

### bang-do-thieu-neo-va-thieu-kiem-ke [P3] Bằng chứng định lượng không tái lập hết và bỏ sót lời khai mới

TEP/DONG: `ops/ci_duong_nhanh.py:45–46`; `ops/ci_duong_nhanh_test.py:5`, `:10`, docstring `tu_kiem_phan_hang`; bundle `goi/DO_LAI.md`/`goi/do_lai_so.py`.

VAN DE: Script đo được giao chạy đúng cwd trên head trả **113 đạt/0 trượt**, không phải 6/113. Hàm kiểm bia mộ đọc toàn bộ refs, trong khi lời khai/bảng chỉ nói “trên master/cây hiện tại”; thiếu neo tập refs nên phép đo không cùng scope chắc chắn. Ngoài ra bảng định lượng bỏ sót mô tả t01..t22 (không t22), k01/k03 (còn k02) và “bốn ca tự kiểm ... ba đột biến thật ... sai tên” (thực tế 5 mẫu rc; mutant thật thứ ba là nới allowlist, không sai tên). Theo yêu cầu packet, mỗi lời khai định lượng bảng bỏ sót được ghi finding; gom các biểu hiện cùng lớp inventory/scope ở đây, không dùng 43/43 tổng để che phân rã sai.

DA THU VA: **chưa áp**, đã tự đo số và scope. Hint cụ thể: công bố lệnh, exact SHA, tập refs + digest, danh sách lease lỗi và mã lỗi; hoặc ghi số cũ không tái lập thay vì tiếp tục dùng nó làm căn cứ. Trong code test sửa mô tả cho đúng các ca thực:

```diff
--- ops/ci_duong_nhanh_test.py
+++ ops/ci_duong_nhanh_test.py
@@
-  1. Hành vi bộ phân loại (`ca t01..t22`): đồ giả cho ca thuần + KHO GIT THẬT cho ca cần ngữ nghĩa git
+  1. Hành vi bộ phân loại và kiểm rẻ (các ca t01–t21, có nhánh a–f): đồ giả + KHO GIT THẬT
@@
-  3. Nối vào sổ test sống (`ca k01`, `k03`): mục `DA_NOI` và lời gọi thật trong `run:`.
+  3. Nối vào sổ test sống (`ca k01`, `k02`, `k03`): mục `DA_NOI`, vị trí tệp và lời gọi thật trong `run:`.
@@
-    """Bốn ca tự kiểm cho CHÍNH bộ phân hạng, cộng ba đột biến thật (sống sót · lỗi vô can · sai tên)."""
+    """Năm mẫu rc cho bộ phân hạng; ba mutant thật: sống sót, lỗi vô can, nới allowlist bị giết.
+    Sai tên ca chỉ được kiểm bằng mẫu rc, chưa phải một mutant thật.
+    """
```

```diff
--- ops/ci_duong_nhanh.py
+++ ops/ci_duong_nhanh.py
@@
-    còn hạn phải qua `check` (lỗi ⇒ ĐỎ). Đo trên master: 6/113 tệp lease trượt `kiem(bo_qua_han=True)`
-    (bia mộ hai chiều), nên "bỏ qua hạn" không phải lối thoát.
+    Số lease trượt còn phụ thuộc tập refs do kiểm bia mộ quét toàn kho. Số 6/113 chưa tái lập
+    trên bundle review này (552 refs: 0/113 trượt); không dùng số cũ để miễn kiểm lease.
```

Hunk docstring sản phẩm phải viết lại đồng bộ với cách xử lý finding lease; không giữ một đoạn diễn giải chính sách đã bỏ. Bổ sung DO_LAI thuộc gói bàn giao, không tự mở write set repo.

Chốt riêng: kiểm kê phân rã t/y/k và tự kiểm từ AST/danh sách ca; mutant đổi con số hoặc loại ca phải làm phép đối chiếu tài liệu đỏ. Phép lease ghi đủ refs + từng failure; đổi tập refs phải đổi scope receipt, không tuyên bố số cũ áp cho snapshot mới. Đây là hint phép đo chưa có test tự động được triển khai; không tuyên bố đã đóng bằng diff tài liệu.

DA THU NGHIEM: `cd cay && python3 -B ../goi/do_lai_so.py` rc=0: 345/63/8 và 113/113 đạt; `out/audit-summary.py` cho t=31/y=9/k=3, không t22, 552 refs/digest. Đọc tuple `tu_kiem_phan_hang`: 5 mẫu rc/3 mutant như mô tả ở trên. Không đo lại 46,5/52 phút hay GitHub skipped; bảng đã khai giới hạn đó nên không báo thành lỗi số đo.

DO TIN: cao về số đo bundle và inventory; vừa về nguyên nhân số 6 cũ vì không có snapshot refs executor đã dùng.

## KIEM TRA CUOI

HEAD/tree cuối khớp đầu; tracked diff và cached diff đều rc=0, spec hash không đổi. Danh sách ignored artifact do selftest và lệnh kiểm nằm ở `out/final-state.log`. Không đưa ignored vào lời khẳng định “cây sạch hoàn toàn”. Các log cuối đã thu đủ rc, không lấy log đang chạy làm nghiệm thu.

## DOT BIEN SONG SOT VA GIOI HAN

- Sai hành vi, **full suite** vẫn xanh: bước kiểm rẻ `continue-on-error: true`; comment cả hai lệnh kiểm rẻ; job gate-ops `continue-on-error: true`.
- Sai hành vi/cấu hình, **43 ca** vẫn xanh khi đo từng cửa: continue-on-error từng job gate/gate-ops/gate-packet-loop; comment riêng doctrine; comment riêng kiem-re; shell kiểm rẻ pwsh. Không giả vờ chạy 55 mutant cho từng cửa mở rộng.
- Sửa đúng nhưng suite không nhạy: thêm `.yml` vào lease filter vẫn full 43/43 + 55/55. Không tính nó là “mutant lỗi bị giết thiếu”; dùng làm chứng cứ thiếu fixture cho cửa ấy.
- Đã thử hint TEST: full 43/43 + 55/55; baseline y06/y08 xanh, ba mutant chính đỏ đúng assertion/ca. Bổ sung `out/hint-entries.py` đã áp patch thật trong bản sao (rc=0) và đo riêng cả bảy cửa: 7/7 rc=3 đúng y06/y08. HINT không sửa workflow, không được coi là bản vá đã land.
- Không soạn payload tấn công/path escape mới; không làm thử nghiệm GitHub/Windows; không khai nghiệm thu 11 đạt. Chưa đo quyền/lease live, dependency #668, required statuses thật hay thời gian tiết kiệm.

TONG: P0=0 P1=0 P2=4 P3=1
So lop: 5. Ket luan changes_requested; khong approve/merge/land.
