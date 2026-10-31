Verdict: request_changes
Reviewed commit: 99c463d9288798cf7a011e16ce69c36b04520f66
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

**Kết luận cuối: request_changes — 2 finding P2 còn mở** (0 P0, 0 P1, 0 P3 trong phạm vi đã đo). Head và base đều qua toàn suite; C1a/C1b/C2/C3/C6/C9 đạt trong các phép đo Linux. Tuy nhiên, đổi sang `iterdir()` làm lỗi liệt kê thư mục thoát thành traceback, và ba đột biến phá hành vi M1 vẫn qua toàn suite. Ngưỡng packet đòi hết cả P0–P3 nên chưa đủ approve. Báo cáo không cấp quyền merge/land.

Reviewed tree: `b6e042a42845fa52a90d898fc43ff72619f26c80`. Base: `757bde561d09738858506aecf5de2f050a5f0d5e`, tree `ab4a284cd655e867fc0bf35d1580a59d28d348db`. `git rev-parse --is-shallow-repository` trả `false` cho cả hai bản sao.

Các lệnh dưới chạy từ thư mục sandbox trừ khi ghi cwd khác. `measure.py` và `mutate.py` tự đặt `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null` cho tiến trình con. Với `probe.py` chạy trực tiếp, dùng cùng các biến đó. `core.abbrev=7` trên các bản sao trước phép đo. Log stdout/stderr và rc riêng trong `evidence/`; không suy pass chỉ từ rc.

## Bảng tiêu chí

| Tiêu chí | Màu / kết luận | Lệnh hoặc công cụ; output đo được |
|---|---|---|
| C1a | 🟢 Linux; 🟡 Windows KHÔNG ĐO ĐƯỢC | `python3 probe.py head behaviors`: hai YAML hợp lệ sai schema ⇒ rc=1, tổng 2, có `x.RECEIPT.YAML`, không `TỔNG: ĐẠT`; chỉ-x ⇒ rc=1, tổng 1, không “không có tệp”. `python3 mutate.py exact`: c98 `giet_that`, tổng=1; đối chứng sạch. Base: tổng 1 và bỏ x. |
| C1b | 🟢 Linux; 🟡 Windows KHÔNG ĐO ĐƯỢC | Cùng lệnh `behaviors`: YAML hỏng ⇒ rc=2, stderr nêu x, không traceback, không dòng tổng. `python3 probe.py mut-exact behaviors`: rc=1, tổng 1, không x trong stderr. |
| C2 | 🟢 Linux; 🟡 Windows KHÔNG ĐO ĐƯỢC | `python3 probe.py head cases`: c89 `qua`; base suite cũng có c89 `ĐẠT`. `python3 mutate.py isfile`: c89 `giet_that`, c98 `qua`, đối chứng c18 sạch hoàn toàn. |
| C3 | 🟢 | `python3 mutate.py glob`: bản sao helper dùng `tm.glob("*.receipt.yaml")`; c98 `giet_that` vì tổng=1, c89 `qua`, đối chứng sạch. Bản sao và patch lưu riêng, không thêm mutant glob vào bảng thường. |
| C4 | 🟡 KHÔNG ĐO ĐƯỢC đầy đủ | GitHub GET `actions/runs?head_sha=<reviewed SHA>&event=workflow_dispatch&per_page=100` và `actions/runs/41031049365/jobs?per_page=100`: đúng head, `.github/workflows/ci.yml`, job `123980641358`, labels `["windows-latest"]`, runner_id `1000025693`; selftest biên nhận còn `in_progress`, lease-publish `pending`. Chưa có N/N, chưa xác minh input `runner_set`. |
| C5 | 🟡 KHÔNG ĐO ĐƯỢC đầy đủ | `github_fetch_commit_workflow_runs` theo đúng head và GET `actions/runs/41031052871/jobs?per_page=100`: job `123980706092`, đúng head, labels `["ubuntu-latest"]`, runner_id `1000025706`; hai bước cần thiết đều `completed/success`, không skipped. `github_fetch_workflow_job_logs(job_id=123980706092)` lỗi 404 `BlobNotFound`, nên chưa đọc được N/N và `TỔNG: ĐẠT` từ log CI. |
| C6 | 🟢 | `python3 measure.py head gate`: rc=0, `253 ĐẠT v2 · 11/11 miễn trừ · 42 NỢ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`, `TỔNG: ĐẠT`. Đếm riêng `sum(p.name.lower().endswith(".receipt.yaml") for p in Path("work/head/ops/reviews").iterdir())` ⇒ 306. Base gate và phép đếm cũng 306. |
| C7 | 🟡 KHÔNG ĐO ĐƯỢC | `remote_desktop_commander_list_devices({})` trả ASUS-LAPTOP `Online`. Không chạy test local Windows và không ghi khoá/sổ đo: chỉ thị reviewer giới hạn ghi trong sandbox, prompt đã yêu cầu phần Windows ghi không đo được. Không suy máy offline hay lấy CI thay local. ADR-0057/0058 đã đọc. |
| C8 | 🔴 | Hai P2 ở bảng findings; verdict neo đúng head nhưng là `request_changes`. Chưa có cơ sở xác nhận mọi điều kiện merge; không suy ngân sách review từ lời khai lease. Chốt dừng `bo-chon-ung-vien` của SPEC đã kích hoạt. |
| C9 | 🟢 các phép đo tại chỗ | `python3 -m ruff check --no-cache --select F ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` ở head/base: cùng F541 `1677:19`, cùng rc=1, delta=0, Ruff 0.15.15. Doctrine scan rc=0, `10 tệp, 0 chỗ chép doctrine`; `git diff --check <base>..HEAD` rc=0; rg mẫu glob ở head 0 dòng/rc=1, base 2 dòng, mutant-glob 1 dòng; numstat đúng hai tệp `17/3`, `50/0`. Vế dương C1a/C1b đã đo ở trên. |

## Bảng findings

| Mức | Slug lớp | Vị trí | Tái hiện / output / hướng vá |
|---|---|---|---|
| P2 | `loi-do-liet-ke-thu-muc-thoat-traceback` | `ops/bien_nhan_v2.py:96–98` | `python3 listing_probe.py`: tiêm EACCES vào liệt kê, head kiểm và sinh nợ rc=1 + traceback; base kiểm rc=2 không traceback. Chuyển `OSError` thành `KhongDoDuoc`, giữ nghĩa thư mục vắng; chi tiết và rủi ro ở Đợt 3. |
| P2 | `bo-chon-ung-vien-thieu-rang-hai-duong-goi` | `ops/bien_nhan_v2_test.py:3637–3658,4467–4472` | `python3 mutate.py <sinh_exact\|nosort\|noguard> --suite --behaviors`: ba bản lỗi đều rc=0, 95/95, 139/139, 2/2, `TỔNG: ĐẠT`. Thêm oracle và mutant riêng cho sinh nợ, sorted và thư mục vắng; chi tiết ở Đợt 4. |

Hai lớp finding, năm biểu hiện đo được: lớp lỗi liệt kê có hai đường gọi; lớp thiếu oracle có ba đột biến sống. Các đoạn sau giữ nhật ký đã ghi tăng dần, bao gồm lệnh, đối chứng, giới hạn và hướng vá cho từng finding.

Đã đối chiếu đầu vào bằng `git -C cay-kho rev-parse HEAD origin/master`,
`git -C cay-kho status --short`, `sha256sum SPEC.md`: head và băm như trên;
base `757bde561d09738858506aecf5de2f050a5f0d5e`; status rỗng, rc=0.
Kho nguồn được giữ nguyên; phép đo và đột biến dùng bản sao đủ cây trong sandbox.
Ở mốc đầu, Windows CI/local và Linux CI chưa có phép đo độc lập; kết quả đọc CI về sau được ghi trong bảng trên và phần cuối.

## Nhật ký đo

### Đợt 1 — C1, C6, C9

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 probe.py head behaviors` và bản `base`: log `evidence/{head,base}-behaviors.log`, JSON từng fixture trong `evidence/fixture-*.json`. Kho thử do reviewer dựng độc lập, có git thật và commit.

| Phép đo | Head | Base |
|---|---|---|
| c1a | rc=1; tổng=['2']; traceback=False | rc=1; tổng=['1']; traceback=False |
| only-x | rc=1; tổng=['1']; traceback=False | rc=2; tổng=[]; traceback=False |
| c1b | rc=2; tổng=[]; traceback=False | rc=1; tổng=['1']; traceback=False |
| directory | rc=2; tổng=[]; traceback=False | rc=1; tổng=['1']; traceback=False |
| sinh-upper | rc=0; tổng=[]; traceback=False | rc=0; tổng=[]; traceback=False |
| missing | rc=2; tổng=[]; traceback=False | rc=2; tổng=[]; traceback=False |
| sinh-missing | rc=0; tổng=[]; traceback=False | rc=0; tổng=[]; traceback=False |
| case-pair | rc=1; tổng=['2']; traceback=False | rc=1; tổng=['1']; traceback=False |

`python3 measure.py head gate`: rc=0; `253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`; `TỔNG: ĐẠT`.

Đếm riêng bằng `sum(p.name.lower().endswith(".receipt.yaml") for p in Path("work/head/ops/reviews").iterdir())`: **306**, base cũng **306**.

`python3 measure.py head doctrine`: rc=0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. `python3 measure.py {head,base} ruff`: mỗi lệnh rc=1, cùng một F541 tại `ops/bien_nhan_v2_test.py:1677:19`, delta **0**; Ruff **0.15.15**. Không gọi bare lint này là sạch.

`git -C cay-kho diff --numstat 757bde561d09738858506aecf5de2f050a5f0d5e..HEAD`: `17 3 ops/bien_nhan_v2.py`, `50 0 ops/bien_nhan_v2_test.py`; `git diff --check` cùng dải: rc=0, stdout rỗng.

### Đợt 2 — suite và đột biến đích

`python3 measure.py head suite` → rc=0, 463.23 s; `bien_nhan_v2_test: 95/95 ca đạt · 139/139 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 121/139 đột biến thường khai đối chứng`; `TỔNG: ĐẠT`.

`python3 measure.py base suite` → rc=0, 460.25 s; `bien_nhan_v2_test: 94/94 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 119/137 đột biến thường khai đối chứng`; `TỔNG: ĐẠT`.

Delta đo được: **+1 ca, +2 đột biến thường**, không đổi **2 ca tự kiểm**.

Mỗi đột biến sau được tạo trên bản sao đủ cây bằng `python3 mutate.py <tên>`; bản vá nguyên văn và stdout nằm ở `evidence/mut-<tên>.patch` / `evidence/mut-<tên>-cases.stdout`.

| Đột biến | c98 | c89 | Đối chứng c18 sạch hoàn toàn |
|---|---|---|---|
| glob | giet_that | qua | True |
| exact | giet_that | qua | True |
| isfile | qua | giet_that | True |
| kiem_exact | giet_that | qua | True |
| sinh_exact | qua | qua | True |
| nosort | qua | qua | True |
| noguard | qua | qua | True |

C3: `glob` ⇒ c98 `giet_that`, thông điệp `tổng=1`; c89 `qua`. C2: `isfile` ⇒ c89 `giet_that`, rc=1 không còn tên thư mục; c98 `qua`. Không tính lỗi rig là bằng chứng giết trong các phép này.

C9: `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py`: head **0 dòng, rc=1**; base **2 dòng (1442,1601), rc=0**; bản `mut-glob` **1 dòng (98), rc=0**. JSON lệnh và output trong `evidence/scope.json`.

Regex: `python3 probe.py head total20` ⇒ c98 `giet_that`, `tổng=20`; c89/đối chứng vẫn qua. Không có lỗi khớp nhầm 20 thành 2.

### Đợt 3 — hồi quy lỗi liệt kê thư mục

- [P2] `loi-do-liet-ke-thu-muc-thoat-traceback`: `ops/bien_nhan_v2.py:96–98` — `PYTHONDONTWRITEBYTECODE=1 python3 listing_probe.py` — head khi `scandir(ops/reviews)` ném `PermissionError(EACCES)` trả **rc=1 + Traceback** trên cả đường kiểm và `--sinh-no`; base cùng fault đã xác nhận vào điểm tiêm: kiểm **rc=2, KHÔNG ĐO ĐƯỢC, không Traceback**, sinh nợ **rc=0, # 0 tệp**. Hướng vá: bắt `OSError` của phép liệt kê trong helper và đổi thành `KhongDoDuoc` có tên thư mục; giữ nhánh thư mục vắng trả `[]`, không nuốt lỗi bằng danh sách rỗng và không thêm `is_file()`.

HÌNH DẠNG: `loi-do`. Phép đo chạy trên bản sao head/base đầy đủ, không thay nguồn sản phẩm; tiêm đúng lỗi OS ở điểm liệt kê. Python 3.13 giữ riêng `scandir` cho glob, nên script tiêm cả `os.scandir` và `pathlib._local._StringGlobber.scandir`; mỗi đường lỗi có dấu `REVIEW_ENUMERATION_FAULT` xác nhận đã tiêm. Đối chứng không tiêm dùng cùng fixture `y.receipt.yaml`: cả hai bản kiểm rc=1 không traceback (schema cố ý sai), sinh nợ rc=0 với `# 1 tệp`. Log đầy đủ: `evidence/listing-{head,base}-{kiem,sinh}-{control,fail}.{json,stdout,stderr}`.

Ca khóa đề nghị: ép lỗi liệt kê trên thư mục có thật; đòi CLI kiểm và sinh nợ rc=2, nêu `ops/reviews`, không traceback; chạy thêm thư mục vắng và `c89` để giữ nghĩa cũ. Rủi ro khi vá: trả `[]` cho mọi `OSError` sẽ biến lỗi đo thành danh sách nợ rỗng; bắt `Exception` quá rộng che lỗi lập trình.

Giới hạn: phép đo bằng quyền hệ thống thực ở `io_probe.py` **KHÔNG ĐO ĐƯỢC** vì sandbox từ chối `os.setgroups([])` (`PermissionError: Operation not permitted`) trước khi gọi cổng. Không dùng các traceback đó làm bằng chứng lỗi sản phẩm. Bằng chứng finding là phép tiêm lỗi riêng đã nêu ở trên.

RIG: `python3 probe.py head rig-setup` tiêm `LoiDungCa` ở `_kho_cau` ⇒ c98/c89 đều `gian_giao`, đối chứng sạch. `python3 probe.py head rig` cố ý thay riêng `bnv2.main` bằng hàm ném `LoiDungCa` ⇒ c98/c89 báo `giet_that`, do `except Exception` đổi thành `bang(False)`. Đây là hạn chế của bắt ngoại lệ nếu tín hiệu rig xuất hiện bên trong API sản phẩm; chưa chứng minh đường fixture/m142 thật phát tín hiệu đó. Không dùng phép giả lập này để tuyên bố m142 đang có tín dụng giả.

### Đợt 4 — ba đột biến sống qua toàn suite

- [P2] `bo-chon-ung-vien-thieu-rang-hai-duong-goi`: `ops/bien_nhan_v2_test.py:3637–3658,4467–4472` — `python3 mutate.py sinh_exact --suite --behaviors`, tương tự `nosort`, `noguard` — **cả ba** bản có lỗi vẫn `95/95 ca đạt · 139/139 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, **rc=0, TỔNG: ĐẠT**. Hướng vá: thêm chốt trực tiếp cho `--sinh-no`, thứ tự helper và thư mục vắng; thêm đột biến đích riêng, không dựa hoàn toàn vào một đột biến helper chung.

HÌNH DẠNG: `bo-chon-ung-vien`. Đây là **một lớp finding, ba biểu hiện** thiếu oracle cho hành vi M1; không báo ba finding rời. Mã sản phẩm trên head đang xử lý đúng ba hành vi; lỗi là bộ kiểm không phát hiện khi chúng bị phá.

| Bản sao / đột biến | Hành vi sai đo riêng | Kết quả suite |
|---|---|---|
| `sinh_exact` | Chỉ thêm lọc `p.name.endswith(".receipt.yaml")` tại vòng lặp `_sinh_no`. `X.RECEIPT.YAML` bị bỏ qua: head `# 1 tệp`, mutant `# 0 tệp`, cùng rc=0. C1a/C1b ở đường kiểm vẫn qua. | rc=0; 95/95,139/139,2/2; 438.8 s; `TỔNG: ĐẠT` |
| `nosort` | Đặt `sorted = list` cục bộ trong helper (giữ neo văn bản m142/m143 để không chết giả vì rig). Tổng vẫn 3 nhưng thứ tự lỗi và khối nợ đổi; lỗi YAML đầu tiên đổi tên a thành z. | rc=0; 95/95,139/139,2/2; 440.11 s; `TỔNG: ĐẠT` |
| `noguard` | Bỏ hai dòng `if not tm.is_dir(): return []` ở helper. `--sinh-no` với thư mục vắng đổi từ rc=0, khối rỗng sang rc=1 + FileNotFoundError/Traceback; đường `kiem` còn guard riêng nên không đổi. | rc=0; 95/95,139/139,2/2; 438.77 s; `TỔNG: ĐẠT` |

Tái chạy trên bản sao đã lưu: `python3 measure.py mut-sinh_exact suite`, `python3 measure.py mut-nosort suite`, `python3 measure.py mut-noguard suite`; hành vi: `python3 probe.py <tên-cây> behaviors`. Tạo mới từ head bằng `mutate.py` trong sandbox trống tương ứng. Mỗi bản là bản sao đủ cây, `.git` là thư mục; mỗi suite là tiến trình riêng.

Ca khóa đề nghị: fixture chỉ có `X.RECEIPT.YAML` hợp lệ YAML nhưng sai schema, gọi CLI `--sinh-no`, đòi đúng tên và đúng số 1; helper nhận danh sách thư mục bị đảo thứ tự nhưng phải trả sorted; fixture không có `ops/reviews` đòi đường kiểm rc=2 không traceback, sinh nợ giữ rc=0/khối rỗng. Mỗi đột biến phải giết đúng ca đích và đối chứng vẫn sạch. Rủi ro khi vá test: đừng so thứ tự Path xuyên nền bằng thứ tự Linux ghim cứng; hãy ép thứ tự đầu vào trong fixture và so theo hợp đồng sorted của nền, không dùng hai tệp chỉ khác case trong ca bắt buộc Windows.

**Chốt dừng của SPEC `hinh_dang_ke_thua` đã kích hoạt** bởi finding mới hình dạng `bo-chon-ung-vien` trên M1. Câu hỏi chuyển chủ kho: **“có nên làm tiếp theo cách này không”**. Review đã hoàn tất; không tiến hành vá/đổi thiết kế trước quyết định đó.

### Hành vi biên và giới hạn

- `probe.py head behaviors`: `--sinh-no` nhận `X.RECEIPT.YAML`, rc=0, `# 1 tệp`, băm `37b128c59f1f5097f73f82691cb519f1f568667faab5ced1b4ab979d36837eae`. Thư mục biên nhận vắng trong kho git thật: kiểm rc=2, `kho thật mà không có ... — không phải sạch`, không traceback; sinh nợ rc=0, `# 0 tệp`, giống base. Không gọi hành vi sinh nợ có sẵn này là lỗi mới.
- Hai tên `a.receipt.yaml` và `a.RECEIPT.YAML` cùng tồn tại: head tổng 2, rc=1, cả hai tên có trong lỗi; base tổng 1. Chỉ đo Linux.
- `evidence/order-summary.json`: head thứ tự a,m,z; nosort m,z,a ở cả dòng lỗi và khối sinh nợ. Cùng tổng 3 và rc tương ứng 1/0. Với hai YAML hỏng: head báo a trước, nosort báo z trước, cùng rc=2. Trong các fixture này không đổi kết luận nhưng có đổi đầu ra; chưa suy cho mọi dữ liệu hay thứ tự Windows.
- `probe.py mut-exact behaviors`: C1a rc=1/tổng 1/không x; chỉ-x rc=2/không tổng; C1b rc=1/tổng 1/không x trong stderr. Như vậy cả ba vế sai riêng, dù c98 dừng ở vế đầu khi chạy nguyên ca.

### Bằng chứng CI, Windows local và kiểm tra cuối

Các truy vấn chỉ đọc qua connector GitHub/Remote Desktop Commander; không phát workflow, không ghi ứng dụng ngoài sandbox. Payload gốc được lưu: `evidence/windows-runs.json`, `windows-jobs.json`, `linux-jobs.json`, `ci-log-error.json`, `desktop-devices.json`.

- C4: [run Windows 41031049365](https://github.com/ducthangho/tra-luat/actions/runs/41031049365), job `123980641358`: head đúng, nhãn/runner_id đã đọc từ JSON jobs, selftest biên nhận còn chạy, lease-publish pending. Kết quả cuối và N/N **KHÔNG ĐO ĐƯỢC**.
- C5: [run PR 41031052871](https://github.com/ducthangho/tra-luat/actions/runs/41031052871), job `123980706092`: hai bước cần thiết đã success; log job trả 404 BlobNotFound tại lần đọc. Không coi status success là thay cho N/N. Toàn suite đo tại chỗ cũng không thay CI.
- C7: danh sách thiết bị trả Online nhưng không có lượt local nào do reviewer chạy; test Windows local, so base và sổ đo **KHÔNG ĐO ĐƯỢC**.

`GIT_OPTIONAL_LOCKS=0 git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored` ⇒ rc=0, rỗng; `git -C cay-kho diff --exit-code HEAD --` ⇒ rc=0, rỗng. HEAD/tree cuối khớp các neo đầu báo cáo; `DIFF.patch` byte-identical với `git diff <base>..HEAD`; sha256 SPEC vẫn khớp. Chi tiết lệnh/output: `evidence/final-integrity.json`. Trạng thái đầu/cuối chứng minh không có delta quan sát được; không dùng nó để khẳng định lịch sử mọi lần ghi.

**request_changes** trên exact head đã nêu. Không sửa mã nguồn kho được review; không cấp quyền merge/land. Finding `bo-chon-ung-vien` cần quyết định của chủ kho theo chốt dừng SPEC trước vòng vá tiếp.
