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
- **M-4 / C7 (Windows local)**: **KHÔNG ĐO ĐƯỢC** — đã bắt đầu, máy rời mạng giữa chừng. Theo ADR-0057/0058: 14:04Z
  `list_devices` ASUS-LAPTOP `Online`; `D:\tl-win\KHOA.txt` rỗng ⇒ ghi khoá `session_015GtxrZ1Tt93F4NLUUhKYQy`
  `14:05:00Z` hạn `16:05:00Z`; kiểm tải: 4 tiến trình `python.exe` không phải test (2 `browser-use --cli-mcp`, 2
  `proxima_agent.web`), không đụng tới. Clone riêng `D:\tl-win\session_015GtxrZ1Tt93F4NLUUhKYQy` ở `e9e0048`, sạch, không nông,
  `core.abbrev 7`. Lệnh: `python -u ops\bien_nhan_v2_test.py` với `PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1`,
  log `D:\tl-win\session_015GtxrZ1Tt93F4NLUUhKYQy-head.log` (lúc đọc cuối mới có dòng `bien_nhan_v2_test — 97 ca`). Sau đó Desktop
  Commander hết trả lời (~14:16Z), tới 14:36Z `list_devices` báo `Offline`. Không có kết quả N/N local, không ghi được
  `do-luong.csv`, không xoá được khoá: khoá tự hết hiệu lực lúc 16:05Z theo ADR-0058 §3(a). Theo ADR-0057 §2: máy offline ⇒ vế local
  không áp; PR ghi "không đo local".

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

**Nơi lưu verdict**: nguyên văn bốn tệp `VERDICT.md` nằm ở **Phụ lục A** cuối tệp này (chép byte-exact bằng script; băm
sha256 ở bảng trên là băm của tệp gốc, đo lại được bằng cách cắt phần giữa hai dấu `<!-- VERDICT-Ln-BAT-DAU -->` /
`<!-- VERDICT-Ln-KET-THUC -->` — phần ấy không gồm dòng trống bao quanh). Bằng chứng phụ của reviewer (log, script dò) KHÔNG được
lưu. `ops/reviews/**` không thuộc write set nên executor KHÔNG ghi biên nhận v2 vào kho; nếu cổng land cần biên nhận trong
`ops/reviews/`, việc ấy cần lease/thẩm quyền riêng.

## Quan sát khác (ghi, KHÔNG vá)
- Clone của container mở ra nông; phải `fetch --unshallow` trước khi chạy `bien_nhan_v2.py --root .` (nông ⇒ rc=2).
- Codex lượt 3 liệt kê hai lỗi `resolve` (đường dẫn module provider; `--root` trong `main`) thoát traceback khi tiêm `OSError` — có
  sẵn ở base, ngoài write set, không tính finding của packet.
- `gate lifecycle tests` trên Windows in `16/28 ca QUA (bo qua 12, hong 0) - KHONG DU` trong bước "nền không có cgroup"; job vẫn
  `success`. Không thuộc packet này, chưa đối chiếu với master.

## Việc còn lại (không phải của executor)
- Merge/land: chủ kho.
- Biên nhận review trong `ops/reviews/` (nếu cổng land đòi): ngoài write set.

## Phụ lục A — nguyên văn verdict Codex (bốn lượt)

### Lượt 1 — sha256 `2b6249476820cfb79ca8137c0de8b8bcbd40c82ffb381aaa490b50ddfc20fdf4`

<!-- VERDICT-L1-BAT-DAU -->
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
<!-- VERDICT-L1-KET-THUC -->

### Lượt 2 — sha256 `68b2cbe6a1555f3af26702d737fd8c2c1f46a780baf76bc6f7021994fc3827fd`

<!-- VERDICT-L2-BAT-DAU -->
Verdict: request_changes
Reviewed commit: 5efa311fd857f7657a1c687e9ea37693070a37d3
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Kết luận: **request_changes**, còn **1 P2 và 1 P3** (2 lớp, 2 biểu hiện mở). Head qua **96/96 ca · 143/143 đột biến thường · 2/2 tự kiểm**, `TỔNG: ĐẠT`. Ba đột biến sống ở lượt trước nay chết đúng chốt c99. Lỗi liệt kê cũ đã được vá ở iterdir, nhưng EACCES ở `is_dir()` vẫn thoát traceback qua đường `--sinh-no`. Đột biến tương đương bắt `Exception` sống qua toàn suite, cho thấy thiếu chốt phân biệt lỗi lập trình. Ngưỡng áp dụng theo packet: không còn P0/P1/P2/P3. Windows và CI trên head này không được đo độc lập; không suy kết quả từ báo cáo executor.

## Neo và phạm vi

`git -C cay-kho rev-parse HEAD HEAD^{tree} origin/master` (rc=0): head như trên; tree `84f05adc6dcaadd38590431d92b2bc5df4206b99`; base `757bde561d09738858506aecf5de2f050a5f0d5e`.
`git -C cay-kho rev-parse --is-shallow-repository` ⇒ `false`; status gồm ignored/untracked ⇒ rỗng; `sha256sum SPEC.md` khớp dòng 3.
Đã đặt `git -C cay-kho config core.abbrev 7` theo chỉ thị. Các bản sao `work/head`, `work/base` có đủ cây và `.git` là thư mục. Lệnh Python đo chạy với `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` qua `measure.py` hoặc tiền tố môi trường tương đương.

Các script lượt 1 được chép ra gốc sandbox: `measure.py`, `listing_probe.py` giữ nguyên; `probe.py` thêm c99 vào danh sách ca đích; `mutate.py` đổi mốc neo selector từ biểu thức return sang ds, nosort vẫn che sorted bằng list tại return. Không đổi cơ chế phép thử. Diff adapter nằm trong `evidence/adapter-*.patch`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: `VERDICT-LUOT1.md`, reviewed head `99c463d9288798cf7a011e16ce69c36b04520f66` (lượt trước); đối chiếu trên exact head dòng 2 bằng script đã chép kèm.

| Finding P2 lượt 1 | Phân loại | Bằng chứng độc lập trên head mới |
|---|---|---|
| `loi-do-liet-ke-thu-muc-thoat-traceback` | **VÁ HỜ ở cấp lớp; phép tái hiện gốc đã vá thật** | `python3 listing_probe.py`: lỗi scandir ở cả hai đường nay rc=2, không traceback, có marker xác nhận tiêm. Tuy nhiên `python3 review_new.py error-child head sinh access`: EACCES ở stat trước iterdir vẫn rc=1/Traceback tại helper:101. Cùng gốc là thao tác I/O chuẩn bị danh sách nằm ngoài nhánh đổi lỗi đo; xem finding F1. |
| `bo-chon-ung-vien-thieu-rang-hai-duong-goi` | **ĐÃ VÁ THẬT** | `python3 mutate.py sinh_exact --suite`, `nosort --suite`, `noguard --suite`: cả ba rc=1/95 trên 96 ca/TỔNG: ĐỎ. c99 chết đúng chốt sinh nợ, thứ tự, thư mục vắng; c98/c89/c18 đối chứng qua. Thông báo và N/N đầy đủ ở Đợt 1 và Đợt 4. |

Không coi traceback của guard `kiem` ở base là hồi quy mới; F1 khoanh hồi quy vào guard helper mà packet thêm cho `--sinh-no`. Không có finding mới hình dạng `bo-chon-ung-vien`; chốt dừng cũ đã được chủ kho cho làm tiếp theo packet giao lượt này.

## Nhật ký đo

### Đợt 1 — phép tái hiện cũ, C1/C2/C3/C6/C9

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 listing_probe.py` giữ nguyên script lượt 1: head `kiem` và `--sinh-no` đều **rc=2**, stderr có `REVIEW_ENUMERATION_FAULT: scandir`, `KHÔNG ĐO ĐƯỢC: không liệt kê được … (PermissionError …)`, không traceback. Đối chứng không tiêm: `kiem` rc=1/tổng 1/sai schema, sinh nợ rc=0/# 1 tệp. Log và rc thật: `evidence/listing-head-{kiem,sinh}-{fail,control}.{json,stdout,stderr}`.

Ba đột biến cũ đã chết đúng chốt c99 trong lượt chạy ca đích (`python3 mutate.py <tên> --suite`; số đo toàn suite bổ sung ở Đợt 4):

| Đột biến | Phân loại của c99 | Thông báo thực đo |
|---|---|---|
| sinh_exact | giet_that | sinh-no: đòi rc=0, khối nợ nêu x.RECEIPT.YAML, # 1 tệp; được rc=0, khối rỗng, # 0 tệp |
| nosort | giet_that | thứ tự: đòi a,m,z khi iterdir trả ngược; được z,m,a |
| noguard | giet_that | vắng/sinh-no: đòi rc=0 # 0 tệp; được rc=2 … FileNotFoundError |

Cả ba: c98 và c89 `qua`, đối chứng c18 `[true, ""]`. Chi tiết nguyên văn: `evidence/mut-*-cases.stdout`; không coi rc của wrapper là bằng chứng giết.

`python3 mutate.py exact --behaviors` ⇒ c98 `giet_that`, C1a tổng 1; `python3 mutate.py isfile` ⇒ c89 `giet_that`, rc=1 thay rc=2; `python3 mutate.py glob` ⇒ c98 `giet_that`, tổng 1. Cả ba có đối chứng c18 sạch. Các đột biến được tạo trên bản sao đầy đủ, mỗi cái tiến trình riêng.

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 probe.py head behaviors` dựng các kho git thật độc lập:

| Fixture | rc | tổng | Traceback |
|---|---:|---|---|
| bad-order | 2 | [] | False |
| c1a | 1 | ['2'] | False |
| c1b | 2 | [] | False |
| case-pair | 1 | ['2'] | False |
| directory | 2 | [] | False |
| empty | 2 | [] | False |
| missing | 2 | [] | False |
| only-x | 1 | ['1'] | False |
| order | 1 | ['3'] | False |
| sinh-missing | 0 | [] | False |
| sinh-order | 0 | [] | False |
| sinh-upper | 0 | [] | False |

C1a và chỉ-x đều nêu tên đuôi hoa, không `TỔNG: ĐẠT`; C1b stderr nêu `x.RECEIPT.YAML`. Nội dung từng stdout/stderr và lệnh CLI nằm trong `evidence/fixture-head-*.json`.

`python3 measure.py head gate` và `python3 measure.py base gate` ⇒ cùng rc=0, `253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`, `TỔNG: ĐẠT`. Đếm độc lập bằng `sum(p.name.lower().endswith(".receipt.yaml") for p in Path("work/head/ops/reviews").iterdir())` ⇒ 306; base cũng 306.

`python3 measure.py head doctrine` ⇒ rc=0, `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
`python3 measure.py {head,base} ruff` (Ruff 0.15.15, no-cache, --select F, đúng hai tệp) ⇒ cả hai rc=1 và cùng F541 tại `ops/bien_nhan_v2_test.py:1677:19`; delta 0. Không gọi bare lint là sạch.
`git -C cay-kho diff --numstat 757bde561d09738858506aecf5de2f050a5f0d5e..HEAD` ⇒ `26 3 ops/bien_nhan_v2.py`, `148 0 ops/bien_nhan_v2_test.py`; name-only đúng hai tệp write set; diff --check cùng dải ⇒ rc=0/rỗng.
`rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` ⇒ head 0 dòng/rc=1; base 2 dòng/rc=0; mut-glob 1 dòng/rc=0 (vế âm có đối chứng dương).

### Đợt 2 — độ nhạy của c99, lỗi giàn giáo và khôi phục toàn cục

`python3 new_mutate.py fault_noop`: vô hiệu điều kiện tiêm bằng `False and …` ⇒ c99 `giet_that`, thông báo `liệt kê hỏng [] … được rc=1`, không xanh giả. `python3 new_mutate.py fault_noop_sinh`: chỉ vô hiệu tiêm ở `--sinh-no` ⇒ c99 `giet_that`, thông báo `liệt kê hỏng ['--sinh-no'] … được rc=0: '# 1 tệp'`. Hai đối chứng c98/c89 qua, c18 sạch.
`python3 new_mutate.py order_noop`: fixture trả xuôi ⇒ c99 `gian_giao`, `fixture: iterdir ngược không có hiệu lực`; không được tính là giết thật. Cùng với mutant nosort chết bằng kết quả helper z,m,a, phép đo thứ tự kiểm cả giàn giáo lẫn đầu ra helper.
`python3 new_mutate.py no_os_catch` ⇒ c99 `giet_that`, `CLI chết bằng PermissionError … đòi mã thoát, không traceback`.
`python3 new_mutate.py catch_empty` ⇒ c99 `giet_that`, rc=2 nhưng chỉ báo `không có tệp`, thiếu `không liệt kê được`. Vậy chỉ rc=2 không đủ đánh lừa chốt (4).

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 trace_probe.py` ⇒ c99 `qua`, hai lần PermissionError được tiêm đúng thư mục, modes `[]` và `['--sinh-no']` (`evidence/c99-trace.json`). Bản tracer đầu truy cập sai biến closure `co`, đã được phân loại là lỗi probe và lưu riêng `c99-trace-rig-error.json`; bản chạy đúng đọc mode từ frame c99.
`python3 review_new.py symlink` ⇒ c99 `qua` khi thư mục tạm đi qua symlink (`evidence/symlink-c99.stdout`). Đây chỉ là phép thử symlink trên hệ đang đo, KHÔNG phải bằng chứng Windows.

`python3 review_new.py cleanup <order|kiem|sinh> <runtime|rig>` (6 tiến trình riêng, môi trường chuẩn): cả 6 ghi `restored=true`, `finally_restored=true`, chạy lại c99 sau lỗi đều `['qua', null]`. Fault được tiêm khi Path.iterdir đang là `nguoc` hoặc `hong`, không phải trước khi patch. Với LoiDungCa cả 3 là `gian_giao`; RuntimeError ở order là `tin_dung_gia`, ở hai CLI là `giet_that`. Không quan sát rò Path.iterdir trong 6 nhánh lỗi này.
`python3 probe.py head rig` và `rig-setup` ⇒ c98/c99 đều `gian_giao`; nhánh `except LoiDungCa: raise` mới có hiệu lực. c89 cũ vẫn đổi lỗi rig do main thành `giet_that`; hành vi này ngoài phần sửa lượt 2, không dùng nó để chứng minh mutation mới chết.

### Đợt 3 — mở rộng lỗi I/O và ranh giới bắt ngoại lệ

`python3 review_new.py error-child head <kiem|sinh> late` ⇒ cả hai rc=2/không traceback khi iterator đã yield một mục rồi mới ném PermissionError; stderr có `REVIEW_FAULT_HIT: late` và `không liệt kê được`.
`python3 review_new.py error-child head <kiem|sinh> stat-os` ⇒ cả hai rc=1/Traceback, marker `REVIEW_FAULT_HIT: stat-os`. os.stat của đúng thư mục bị tiêm EACCES; Path.is_dir thật truyền lỗi ra ngoài try. Ở --sinh-no, traceback đi qua `_chon_bien_nhan` dòng 101; ở kiem là guard sẵn có dòng 1459.
`python3 review_new.py error-child <head|base> <kiem|sinh> access` tiêm cùng EACCES vào cả os.stat và scandir/glob của đúng thư mục. Head cả hai rc=1/Traceback; base kiem cũng rc=1/Traceback (lỗi đã có), base sinh rc=0/# 0 tệp, có marker `access-scandir`. Vì vậy hồi quy mới được khoanh ở nhánh `--sinh-no`; lỗi I/O trước iterdir vẫn chưa được chuẩn hoá. Log và mã thoát: `evidence/{head,base}-access-{kiem,sinh}.{json,stdout,stderr}`.

Đo bằng quyền thư mục thật: **KHÔNG ĐO ĐƯỢC**. `python3 actual_permissions.py` không hạ được quyền cho tiến trình con: `os.setgroups([])` trả EPERM ngay cả đối chứng; không có lệnh cổng nào chạy sau chốt đó. Không dùng các rc=1 ấy làm bằng chứng lỗi sản phẩm; finding ở trên chỉ dựa phép tiêm OS có marker trên Path.is_dir thật.

`python3 new_mutate.py broad_literal`: đổi `except OSError` thành `except Exception` ⇒ c98/c99/c89 đều `qua`, c18 sạch. Nếu giữ m147 nguyên văn thì mốc neo mất: `evidence/literal-anchor-check.json` ghi `gian_giao`, không phải oracle giết được lỗi bắt rộng.
`python3 new_mutate.py broad --suite`: đột biến tương đương về nghĩa bằng gán cục bộ `OSError = Exception` trong helper, giữ nguyên mốc neo của m147 để đo hành vi. Ca đích c98/c99/c89 vẫn qua, c18 sạch; toàn suite đã xong: rc=0, 96/96 ca, 143/143 đột biến thường, 2/2 tự kiểm, TỔNG: ĐẠT (463.72 s; xem chốt cuối).
`python3 review_new.py error-child <head|mut-broad> <kiem|sinh> <runtime|value>`: head phát RuntimeError/ValueError ra ngoài (rc=1/traceback); mutant biến chúng thành rc=2/`KHÔNG ĐO ĐƯỢC: không liệt kê được … (RuntimeError/ValueError …)`, không traceback. Tất cả có marker xác nhận lỗi đã tiêm. Đây là khác biệt hành vi thật; head hiện bắt đúng OSError, phần còn thiếu là test phân biệt lỗi lập trình.

### Đợt 4 — toàn suite và xác nhận ba đột biến cũ

| Lệnh (môi trường chuẩn ở đầu tệp) | rc thật của suite | Kết quả nguyên văn rút gọn | Thời gian |
|---|---:|---|---:|
| `python3 measure.py head suite` | 0 | bien_nhan_v2_test: 96/96 ca đạt · 143/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐẠT | 483.28 s |
| `python3 mutate.py sinh_exact --suite` | 1 | bien_nhan_v2_test: 95/96 ca đạt · 142/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐỎ | 476.41 s |
| `python3 mutate.py nosort --suite` | 1 | bien_nhan_v2_test: 95/96 ca đạt · 143/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐỎ | 481.23 s |
| `python3 mutate.py noguard --suite` | 1 | bien_nhan_v2_test: 95/96 ca đạt · 142/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐỎ | 481.72 s |

Trong full log, cả ba mutant có dòng `ĐỎ c99_… [giet_that]` với đúng thông báo đã trích ở Đợt 1. `sinh_exact` còn làm m144 mất neo, `noguard` làm m146 mất neo: hai dòng `gian_giao` ấy KHÔNG được dùng làm bằng chứng giết; bằng chứng là c99 tự đỏ khi chạy trên mutant, trước pha đột biến nội bộ. `nosort` giữ 143/143 đột biến nhưng vẫn đỏ vì c99, đúng kỳ vọng.

Phác thảo oracle đã chạy cho ranh giới ngoại lệ: `python3 boundary_oracle.py head` ⇒ rc=0; `python3 boundary_oracle.py mut-broad` và `mut-broad_literal` ⇒ rc=1. Tiêm một RuntimeError sentinel tại đúng thư mục rồi đòi đúng đối tượng ngoại lệ truyền ra ngoài trên cả hai đường; mỗi đường có hit=1 và Path.iterdir được khôi phục. Chi tiết: `evidence/*-boundary-oracle.{json,stdout,stderr}`. Đây là dữ liệu phản chứng trong sandbox, không phải bản vá giao áp tự động.

## Bảng tiêu chí

| Tiêu chí | Kết quả | Lệnh và bằng chứng |
|---|---|---|
| C1a | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | `python3 probe.py head behaviors`: c1a rc=1/tổng 2/có x.RECEIPT.YAML/không ĐẠT; only-x rc=1/tổng 1/không "không có tệp". `mutate.py exact --behaviors`: C1a còn tổng 1, only-x không tổng; c98 giet_that. |
| C1b | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | Cùng lệnh: YAML hỏng đuôi hoa rc=2/stderr nêu x/không traceback/không tổng. Mut-exact bỏ sót x, rc=1, tổng 1. |
| C2 | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | Full suite có c89 ĐẠT; `python3 mutate.py isfile`: c89 giet_that, rc=1 thay rc=2, c98/c99 qua, c18 sạch. |
| C3 | ĐẠT trên Linux | `python3 mutate.py glob`: c98 giet_that/C1a tổng 1; đối chứng c18 sạch. Không cho mutant phụ thuộc nền này vào bảng thường. |
| C4 | KHÔNG ĐO ĐƯỢC | Không có phép đo Windows CI độc lập trên exact head trong lượt này; success trên 99c463d do executor cung cấp không thay bằng chứng 5efa311. |
| C5 | KHÔNG ĐO ĐƯỢC | Không có log Ubuntu CI độc lập trên exact head; full suite tại sandbox không được nhận là CI. |
| C6 | ĐẠT | `python3 measure.py head gate`: rc=0, tổng 306, TỔNG: ĐẠT; đếm riêng 306. Base thật cũng rc=0/tổng 306. `--sinh-no` trên head rc=0/# 42 tệp. |
| C7 | KHÔNG ĐO ĐƯỢC | Không chạy Windows local. |
| C8 | KHÔNG ĐẠT | Còn finding F1 (P2), F2 (P3); verdict request_changes trên exact head đã neo. Không cấp quyền merge/land. |
| C9 | ĐẠT | Ruff --select F delta 0 (cả hai bare lint rc=1/cùng F541); doctrine rc=0/10 tệp/0 chỗ; diff --check rc=0; rg 0 dòng, có đối chứng base 2/mut-glob 1; numstat +26/-3 và +148/-0, đúng hai tệp. |

## Finding

| ID | Mức | Slug lớp nguyên nhân | Nguồn/lý do giữ hoặc thêm | Phép đóng |
|---|---|---|---|---|
| F1 | P2 | `loi-do-liet-ke-thu-muc-thoat-traceback` | Giữ slug lượt 1; biểu hiện cũ ở scandir đã đóng, còn biểu hiện I/O trước liệt kê tại is_dir trên --sinh-no | Tiêm EACCES cả stat và liệt kê: hai đường rc=2/không traceback; vắng thật vẫn đúng hành vi cũ; fixture/c99 mới phải giết mutant bỏ bắt lỗi stat. |
| F2 | P3 | `loi-do-thieu-chot-ngoai-le-lap-trinh` | Mới trong phần test cho nhánh bắt OSError; hiện c99 chỉ tiêm PermissionError | Head qua oracle RuntimeError sentinel; mutant bắt Exception phải bị giết thật bởi ca đích, không phải mất neo m147. |

- [P2] `loi-do-liet-ke-thu-muc-thoat-traceback`: `ops/bien_nhan_v2.py:101` (gọi từ `_sinh_no` dòng 1624), khối try bắt đầu ở dòng 103 — `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 review_new.py error-child head sinh access` — rc=1, stderr có `REVIEW_FAULT_HIT: stat-os`, `Traceback`, `PermissionError: [Errno 13] review OS stat failure`; base cùng phép tiêm rc=0/# 0 tệp, marker access-scandir — đưa cả bước kiểm tra thư mục vào chính sách bắt **OSError** và đổi thành KhongDoDuoc, không đổi lỗi truy cập thành vắng/rỗng. Giữ hành vi thật sự thiếu thư mục (`kiem` rc=2, sinh nợ rc=0/# 0 tệp), bổ sung ca tiêm lỗi stat ở helper và đối chiếu guard kiem để hai đường cùng chuẩn lỗi I/O. Không bắt Exception để che lỗi lập trình.

HÌNH DẠNG: `loi-do`.

Bằng chứng chỉ rõ điều kiện lỗi: stat của thư mục biên nhận bị từ chối trước khi iterdir chạy, như lỗi quyền tra cứu đường dẫn. Guard mới nằm ngoài try nên lời khẳng định "lỗi I/O khi chọn biên nhận ⇒ rc=2 không traceback" chưa kín. Ở kiem, cùng lỗi đã có trên base và không được kê riêng thành hồi quy. Bản thử quyền thực tế bị chặn ở setup đã nêu ở Đợt 3; không suy rằng phép chmod thật đã được đo thành công.

- [P3] `loi-do-thieu-chot-ngoai-le-lap-trinh`: `ops/bien_nhan_v2_test.py:3731` (c99 chốt lỗi liệt kê), `ops/bien_nhan_v2_test.py:4568` (m147) — `PYTHONDONTWRITEBYTECODE=1 python3 new_mutate.py broad --suite` — **rc=0, 96/96 ca đạt · 143/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐẠT**, 463.72 s; trong khi RuntimeError/ValueError ở iterdir bị chuyển thành KhongDoDuoc — thêm chốt tiêm lỗi lập trình ngoài OSError và đòi ngoại lệ nguyên gốc truyền ra trên cả hai đường, cùng mutant nới catch phải chết tại chốt đó. `boundary_oracle.py` đã đo head rc=0, cả hai mutant broad/broad_literal rc=1; có hit=1/đường và khôi phục Path.iterdir.

HÌNH DẠNG: `loi-do`.

Đây là thiếu chốt hồi quy, không khẳng định head hiện bắt Exception. Mutant `broad_literal` đổi trực tiếp tên catch, vượt qua c98/c99/c89 và đối chứng, nhưng phá mốc neo văn bản m147 nên không thể dùng lỗi rig để nhận tín dụng giết. Mutant `broad` đặt tên cục bộ `OSError = Exception` trong chính helper: cùng nghĩa bắt rộng, vẫn giữ mốc neo, và sống qua toàn suite. Vì chốt (4) chỉ đưa PermissionError (thuộc OSError), nó không phân biệt catch hẹp với catch rộng. Ảnh hưởng có giới hạn: mutant vẫn fail-closed rc=2, nhưng che nguyên nhân lỗi lập trình thành lỗi đo; do đó xếp P3, không xếp lỗi runtime P2 cho head đang đúng.

## Chốt bằng chứng và giới hạn

`python3 new_mutate.py broad --suite` đã hoàn tất: log `evidence/mut-broad-suite.stdout`, mã thoát và thời gian `evidence/mut-broad-suite.json`. Không đột biến nào còn đang chờ kết quả để lập verdict này.

`python3 probe.py base behaviors` được chạy lại qua `measure.run` trên đúng base: C1a rc=1/tổng 1/bỏ x; only-x rc=2/không tổng; C1b rc=1/tổng 1/bỏ x. `python3 probe.py base cases` ⇒ c89 qua, c18 sạch. `evidence/base-behaviors.*`, `fixture-base-*.json` và `base-cases.stdout` lưu phép đo mới, không tái dùng số của lượt 1.

`PYTHONDONTWRITEBYTECODE=1 python3 integrity.py` ⇒ rc=0. `evidence/final-integrity.json` ghi lệnh/output: head/tree/base vẫn đúng các neo ở đầu; detached, không nông, core.abbrev=7; status gồm tracked/untracked/ignored rỗng; diff worktree và index so HEAD rc=0/rỗng. Hai tệp write set byte-identical với blob HEAD; DIFF.patch và DIFF-LUOT2.patch byte-identical với git diff tương ứng; SPEC vẫn khớp SHA-256. Bản `work/head` chạy suite cũng sạch và cùng HEAD/tree. Snapshot đầu/cuối chứng minh không có delta nội dung quan sát được; không dùng nó để khẳng định toàn bộ lịch sử mọi lần ghi. Thay đổi cấu hình core.abbrev được thực hiện đúng yêu cầu trước đo.

Các phần **KHÔNG ĐO ĐƯỢC**: Windows CI/local, Ubuntu CI trên exact head, và tái hiện bằng quyền hệ điều hành thật sau hạ quyền (setup EPERM). Không dùng kết quả CI của head cũ hoặc lời khai executor để đánh dấu đạt. Những hướng liên quan nội dung nhạy cảm không được dựng thêm. Không có thay đổi mã nguồn trong checkout được review; các script và mutant là hiện vật thử trong sandbox. Verdict này không cấp quyền merge/land.
<!-- VERDICT-L2-KET-THUC -->

### Lượt 3 — sha256 `4c786b0dac87602e2cceda698dd4973891d546c7e6391b9f59d0bf1cbcba388b`

<!-- VERDICT-L3-BAT-DAU -->
Verdict: request_changes
Reviewed commit: 8d9e3e3b55897575b9e69a13f5d1a4f3ff6c9fde
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Kết luận cuối: **request_changes** vì còn **một finding P3 về chốt hồi quy OSError** (F3 bên dưới). F1/P2 và F2/P3 của lượt 2 đều **ĐÃ VÁ THẬT**. Không tìm thấy lỗi runtime mới trong phần thay đổi qua các phép đo đã chạy. Head đạt toàn suite `97/97 · 149/149 · 2/2`, cổng thật rc=0/tổng 306. Mutant thu hẹp helper mới chỉ còn bắt PermissionError vẫn sống qua toàn suite, dù EIO/ESTALE trên mutant thoát traceback; đây là bằng chứng thiếu chốt, không phải lời khẳng định head đang bắt sai. Chi tiết, lệnh và output được ghi tăng dần dưới đây.

## Phạm vi

Review độc lập packet #1021 r2, lượt 3. Checkout `cay-kho/` chỉ đọc mã nguồn; bản sao đầy đủ cây, fixture và log đặt trong sandbox. Cấu hình `core.abbrev=7` theo chỉ thị. Mọi tiến trình đo dùng `PYTHONDONTWRITEBYTECODE=1`, fixture Git cô lập bằng `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.

Windows CI/local và Ubuntu CI exact head: chưa có phép đo độc lập; không nhận lời khai executor là kết quả đo. Không cấp quyền merge/land.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding lượt 2 | Kết luận | Bằng chứng chạy lại trên head mới |
|---|---|---|
| F1/P2 `loi-do-liet-ke-thu-muc-thoat-traceback` | **ĐÃ VÁ THẬT** | `review_new.py error-child head {kiem,sinh} {stat-os,access}`: 4/4 rc=2/không traceback, có hit. Bản đồ I/O bên dưới kiểm cả guard, helper, `.git`, liệt kê và đọc/băm. |
| F2/P3 `loi-do-thieu-chot-ngoai-le-lap-trinh` | **ĐÃ VÁ THẬT** | `runtime`/`value` ở iterdir truyền ra; `boundary_oracle.py head` rc=0; `new_mutate.py broad`/`broad_literal`: c100 `giet_that`, c18 sạch. Tracer chốt (7) đủ 4 hit/đúng đối tượng. |

Không finding cũ nào bị giữ là VÁ HỜ hoặc CHƯA VÁ. F3 mới ở cuối là thiếu phép phân biệt các lớp con OSError, khác thiếu chốt lỗi lập trình của F2.


## Đợt 1 — neo và tái hiện lượt 2

`evidence/preflight.json`: `git rev-parse HEAD HEAD^{tree} origin/master` rc=0, lần lượt `8d9e3e3b55897575b9e69a13f5d1a4f3ff6c9fde`, `97e0d90fb6dcda86076272c951a44e1ff79ff554`, `757bde561d09738858506aecf5de2f050a5f0d5e`; detached (`symbolic-ref` rc=1/rỗng), không nông (`false`), `.git` là thư mục, status rỗng. SHA-256 SPEC khớp neo.

Script lượt 2 được chép ra gốc sandbox để `ROOT=parent(__file__)` trỏ đúng nơi. `review_new.py` và `boundary_oracle.py` giữ nguyên byte. `new_mutate.py`/`mutate.py` chỉ đổi mốc `if not tm.is_dir()` sang `if not _hoi_trang_thai(tm.is_dir, tm)`; `probe.py` thêm `c100_` vào danh sách ca; `integrity.py` đổi mốc diff lượt trước từ `99c463d`/`DIFF-LUOT2.patch` sang `5efa311`/`DIFF-LUOT3.patch`. Không chỉnh oracle để nhận kết quả mới.

- F1 **ĐÃ VÁ THẬT** ở phép tái hiện cũ: `python3 review_new.py error-child head {kiem,sinh} {stat-os,access}` — cả 4 tiến trình rc=2, có `REVIEW_FAULT_HIT: stat-os`, stderr `KHÔNG ĐO ĐƯỢC: không đọc được trạng thái .../ops/reviews (PermissionError...)`, không traceback. Log `evidence/rerun-head-*.{stdout,stderr,json}`. Lỗi liệt kê muộn (`late`) cũng rc=2 trên hai đường.
- F2 **ĐÃ VÁ THẬT** ở phép tái hiện cũ: `python3 review_new.py error-child head {kiem,sinh} {runtime,value}` — cả 4 tiến trình rc=1, traceback kết thúc bằng đúng `RuntimeError`/`ValueError: review programming fault`; lỗi lập trình không bị đổi thành KhongDoDuoc. `python3 boundary_oracle.py head` rc=0, hai đường `propagated_same_error=true, hit=1, restored=true`.
- `python3 new_mutate.py broad` và `broad_literal`: c98/c99/c89 `qua`, **c100 `giet_that`**: `lỗi lập trình ở iterdir [] bị nuốt/đổi ... được không ngoại lệ`, đối chứng c18 `[true, ""]`. `boundary_oracle.py mut-broad` và `mut-broad_literal` đều rc=1, có hit=1 nhưng bị đổi thành rc=2. Đây là chết đúng chốt c100, không lấy lỗi mất mốc m147 làm tín dụng.

Các lệnh đo dùng tiền tố môi trường đã nêu. Full suite và bản đồ I/O vẫn đang chạy; chưa kết luận cuối.


## Đợt 2 — tiêu chí và bản đồ hệ tệp

`python3 probe.py head behaviors` (log `head-behaviors` và từng `fixture-head-*`): C1a rc=1, `tổng 2`, nêu x đuôi hoa; only-x rc=1, `tổng 1`, không thông báo không có tệp; C1b rc=2, stderr nêu x, không traceback, không có dòng tổng. Base đo lại: C1a `tổng 1`, only-x rc=2/không có tệp, C1b rc=1/bỏ x. Cặp tên chỉ khác hoa thường đếm 2 ở head. Thư mục đuôi hoa tới bước băm và rc=2.

`python3 mutate.py exact --behaviors`: c98/c99 `giet_that`, đối chứng c18 sạch; mutant bỏ x ở C1a/C1b/only-x. `python3 mutate.py isfile --behaviors`: c89 `giet_that` (rc=1 thay rc=2), đối chứng c18 sạch. `python3 mutate.py glob --behaviors`: c98/c99 `giet_that`, đối chứng c18 sạch; c100 `gian_giao` vì không còn gọi iterdir, KHÔNG lấy tín dụng này làm chết mutant. C3 được chứng minh bởi c98.

C6: `python3 measure.py head gate` và `base gate`: rc=0, `253 ĐẠT v2 · 11/11 miễn trừ ... · 42 NỢ ... · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`, `TỔNG: ĐẠT`. Lệnh đếm riêng dùng `os.listdir` (log `count-head`, `count-base`) cho `casefold_suffix 306` và `exact_suffix 306`. `python3 ops/bien_nhan_v2.py --root . --sinh-no` trên head/base đều rc=0, `# 42 tệp`.

C9: `git diff --numstat 757bde5..HEAD` chỉ hai tệp: `40 5 ops/bien_nhan_v2.py`, `262 0 ops/bien_nhan_v2_test.py`; `git diff --check` rc=0/rỗng. Ruff `--no-cache --select F` head/base cùng rc=1/cùng F541 tại test:1677, output byte-identical nên delta 0. Doctrine-scan head/base rc=0, `đã quét 10 tệp, 0 chỗ chép doctrine`. `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py`: head rc=1/0 dòng; base 2 dòng (1442/1601); mut-glob 1 dòng (116). Dương tính đối chứng là C1a/C1b ở trên, không suy từ vế âm.

### Bản đồ đầy đủ các callsite I/O của mã sản phẩm

Liệt kê độc lập bằng AST (`evidence/fs-call-inventory.json`) và theo các lời gọi từ `main` → `kiem`/`_sinh_no`, gồm bước import nguồn provider và nhánh đọc bằng chứng sau receipt. Bảng dưới đo từng callsite; lệnh cho MỖI ô: `python3 fs_probe.py <head|base> <kiem|sinh> <site>`. Log đầy đủ `evidence/fs-<tree>-<mode>-<site>.{stdout,stderr,json,result.json}` ghi vị trí, hit và khôi phục. `python3 fs_matrix.py` chạy 52 tiến trình độc lập, tất cả có hit dương, khôi phục hàm gốc. Lỗi tiêm là PermissionError thuộc OSError. Không khẳng định đã tiêm mọi syscall bên trong thư viện/importer/Git; đã đo mọi callsite I/O tường minh của tệp sản phẩm trong hai luồng.

| Site và dòng head | Phạm vi / thao tác | Head đo mới | Base đo mới |
|---|---|---|---|
| `provider-resolve` (235) | Không đổi; resolve đường dẫn module trước import nguồn | kiem: rc=1, hit=1, traceback; sinh: rc=1, hit=1, traceback | kiem: rc=1, hit=1, traceback; sinh: rc=1, hit=1, traceback |
| `provider-launcher` (240) | Không đổi; đọc launcher.py | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback |
| `provider-agents` (244) | Không đổi; đọc AGENTS.md | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback |
| `provider-protocol` (244) | Không đổi; đọc PROTOCOL_DA_PHIEN.md | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback |
| `main-resolve` (1581) | Không đổi; resolve --root trước try | kiem: rc=1, hit=1, traceback; sinh: rc=1, hit=1, traceback | kiem: rc=1, hit=1, traceback; sinh: rc=1, hit=1, traceback |
| `guard-isdir` (1471) | Đổi lượt 3; is_dir/stat ops/reviews ở guard kiem | kiem: rc=2, hit=1, không traceback | kiem: rc=1, hit=1, traceback |
| `helper-isdir` (113) | Helper thêm ở packet; bọc lỗi lượt 3; is_dir/stat ops/reviews ở selector (đo riêng cả lần thứ hai trong kiem) | kiem: rc=2, hit=1, không traceback; sinh: rc=2, hit=1, không traceback | Không có callsite này; đối chứng glob ở listing_probe |
| `git-exists` (1472) | Đổi lượt 3; exists/stat .git khi thiếu ops/reviews | kiem: rc=2, hit=1, không traceback | kiem: rc=1, hit=1, traceback |
| `listing` (116) | Đổi glob thành iterdir trong packet; liệt kê thư mục; lỗi ngay và lỗi giữa iterator | kiem: rc=2, hit=1, không traceback; sinh: rc=2, hit=1, không traceback | Không có callsite này; đối chứng glob ở listing_probe |
| `receipt-hash` (677 → 1496/1641) | Không đổi; read_bytes để băm receipt | kiem: rc=2, hit=1, không traceback; sinh: rc=2, hit=1, không traceback | kiem: rc=2, hit=1, không traceback; sinh: rc=2, hit=1, không traceback |
| `receipt-text-kiem` (1497) | Không đổi; read_text receipt ở kiem | kiem: rc=2, hit=1, không traceback | kiem: rc=2, hit=1, không traceback |
| `receipt-text-sinh` (1640) | Không đổi; read_text receipt ở --sinh-no | sinh: rc=2, hit=1, không traceback | sinh: rc=2, hit=1, không traceback |
| `grafts-exists` (1214) | Không đổi; exists/stat .git/info/grafts qua _kho_lanh | kiem: rc=2, hit=42, không traceback | kiem: rc=2, hit=42, không traceback |
| `run-lstat` (1279) | Không đổi; lstat run_json qua _vang | kiem: rc=0, hit=29, không traceback | kiem: rc=0, hit=29, không traceback |
| `run-text` (1434) | Không đổi; read_text run_json | kiem: rc=2, hit=29, không traceback | kiem: rc=2, hit=29, không traceback |
| `verdict-isfile` (1295) | Không đổi; is_file/stat verdict_path | kiem: rc=2, hit=29, không traceback | kiem: rc=2, hit=29, không traceback |
| `verdict-text` (1298) | Không đổi; read_text verdict_path | kiem: rc=2, hit=29, không traceback | kiem: rc=2, hit=29, không traceback |
| `git-run` (843) | Không đổi; subprocess.run trong _git | kiem: rc=2, hit=506, không traceback | kiem: rc=2, hit=506, không traceback |
| `blob-run` (970) | Không đổi; subprocess.run đọc blob Git | kiem: rc=2, hit=253, không traceback | kiem: rc=2, hit=253, không traceback |
| `history-run` (1176) | Không đổi; subprocess.run trong _chay_git | kiem: rc=2, hit=1, không traceback | kiem: rc=2, hit=1, không traceback |

Các thao tác `root / ...`, `p.name`, `.lower()`, `.endswith()`, `Path.parts`, `is_absolute()`, `sorted(ds)` chỉ xử lý đường dẫn/tên trong bộ nhớ; băm SHA-256 không có I/O ngoài `read_bytes` đã đo. Hai caller selector đổi ở 1476/1636; cả hai dùng một helper. `is_file` ở bảng là kiểm verdict sau receipt, KHÔNG phải lọc receipt.

Đối chứng liệt kê cấp OS: `python3 listing_probe.py` trên head/base, hai đường và control/fail, log `listing-*.json`. Head lỗi scandir rc=2 không traceback; base kiem rc=2/không có tệp, base sinh rc=0/`# 0 tệp` (nuốt lỗi). `review_new.py ... late` ở head cho rc=2 sau khi iterator đã yield một mục, không xuất kết quả nợ dở dang.

Hai lỗi resolve thoát traceback là **có sẵn tại base**, các callsite này không được packet sửa. Đọc nguồn provider lỗi khi sinh nợ vẫn rc=0/#42 ở CẢ head/base; không tính finding mới. `_vang.lstat` nuốt EACCES rồi vẫn thử đọc run_json: ở phép tiêm chỉ-lstat, 29 lần đọc thực còn thành công nên rc=0; phép tiêm `run-text` riêng cho rc=2. Không gọi fallback đọc thành công ấy là lỗi đo bị báo sạch. Các nhánh Git/đọc lịch sử bắt lỗi và rc=2 ở cả head/base. Không yêu cầu packet vá các hành vi có sẵn ngoài phần thay đổi.

## Đợt 3 — c100 và đột biến reviewer

`python3 c100_audit.py <1..7> <rig|runtime|value>`: **21/21 tiến trình rc=0**, mỗi lần tiêm dừng ở một trong bảy lần gọi main khi đang thay Path; sau lỗi `Path.is_dir`, `Path.exists`, `Path.iterdir` đều đúng đối tượng gốc; chạy lại c100 `qua`, đối chứng c18 `[true, ""]`. Không đo thấy rò sang ca sau.

Tracer độc lập (`python3 c100_audit.py trace`, log cuối `c100-trace-final`) ghi 7 lần tiêm; bốn lần RuntimeError của chốt (7) đều đúng đối tượng mốc, hit=1, đủ iterdir/is_dir × kiem/sinh. Bản tracer đầu lỗi KeyError vì tưởng closure giữ biến `ten`; log `c100-trace` được giữ và KHÔNG tính là lỗi sản phẩm. Tracer sửa đọc `goc.__name__`; lần đo trung gian gán cờ từ biến vòng lặp cũ làm nhãn .git sai, nên bản cuối lấy argv từ frame main. Chỉ dùng kết quả tracer cuối.

`python3 extra_mutate.py <tên>` (bản sao đủ cây, từng mutant một tiến trình):

| Mutant | Ca c100 | Ý nghĩa |
|---|---|---|
| helper_empty: lỗi trạng thái trả False | giet_that | Không biến lỗi I/O thành vắng |
| helper_pathless: bỏ đường dẫn và chi tiết lỗi | giet_that | Chốt .git còn kiểm thông báo |
| runtime_replaced: ném RuntimeError mới cùng lời | giet_that | Đo đồng nhất đối tượng, không chỉ kiểu/thông điệp |
| injection_noop | gian_giao | dừng do không tiêm trúng, không tính là bắt lỗi sản phẩm |
| injection_runtime_noop | gian_giao | riêng chốt (7) không thể xanh khi không tiêm trúng |
| runtime_same_message: fixture ném đối tượng khác cùng lời | giet_that | Oracle không nhận RuntimeError giả cùng thông điệp |
| narrow_helper: chỉ bắt PermissionError tại helper mới | qua | **SỐNG TOÀN SUITE**, rc=0/97/97 · 149/149 · 2/2; EIO/ESTALE ở guard/helper/.git thoát traceback trên mutant |
| narrow_listing: chỉ bắt PermissionError tại nhánh liệt kê | qua | **SỐNG Ở CÁC CA ĐÍCH** c98/c99/c100/c89; EIO/ESTALE ở scandir thoát traceback trên mutant. Không chạy toàn suite cho mutant này |

Mọi mutant trên có c18 sạch; log `mut-<tên>-cases.stdout` ghi đầy đủ. `python3 errno_probe.py head <mode> <guard|helper|git|listing> <EIO|ESTALE>`: head rc=2 không traceback tại cả sáu tổ hợp đường đi, hit=1; helper trong kiem tiêm vào lần stat THỨ HAI (attempts=2), phân biệt được với guard. Mutant narrow_helper trả rc=1/traceback cho cả bốn tổ hợp trạng thái; narrow_listing trả rc=1/traceback ở hai đường liệt kê. Đây là lỗi bị đưa vào mutant, chưa phải lỗi runtime của head.


## Đợt 4 — toàn suite trên head

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 measure.py head suite` đã xong. Tiến trình thật `python3 ops/bien_nhan_v2_test.py` trong `work/head`: **rc=0, 406.32 s**, `97/97 ca đạt · 149/149 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 131/149 đột biến thường khai đối chứng`, `TỔNG: ĐẠT`. Log `evidence/head-suite.{stdout,stderr,json}`; stderr rỗng. Các m148–m153 đều `giet_that` tại c100, m146/m147 vẫn chết ở c99. Không suy pass chỉ từ rc=0.

Phép tiêm ValueError có hai tầng cần phân biệt: tiêm thẳng vào phương thức Path (`errno_probe.py ... value-method`) truyền ra khỏi helper; tiêm sâu hơn vào `os.stat` có thể bị chính `Path.is_dir`/`Path.exists` đổi thành False. Đối chứng `boundary-base-kiem-{guard,git}-value` có cùng hành vi sẵn ở base. Không coi hành vi của pathlib là helper bắt Exception. Log `boundary-head-*` và `boundary-base-*` lưu hai tầng; RuntimeError ở tầng phương thức vẫn truyền nguyên gốc. Điều này không thay kết luận F2 cũ đã vá thật.


## Bảng tiêu chí cuối

| Tiêu chí | Kết quả | Lệnh / output và giới hạn |
|---|---|---|
| Toàn suite head | **ĐẠT** | `python3 measure.py head suite`: rc=0, `97/97 ca đạt · 149/149 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`; 406.32 s. |
| C1a | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | `python3 probe.py head behaviors`: C1a rc=1/tổng 2/nêu x; only-x rc=1/tổng 1; mut-exact giết thật c98. |
| C1b | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | Cùng lệnh: YAML hỏng đuôi hoa rc=2/nêu x/không traceback/không tổng; mut-exact bỏ x và rc=1/tổng 1. |
| C2 | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | Full suite c89 ĐẠT; `python3 mutate.py isfile --behaviors`: c89 `giet_that`, c18 sạch. |
| C3 | **ĐẠT trên Linux** | `python3 mutate.py glob --behaviors`: c98 `giet_that`, c18 sạch. Không thêm mutant phụ thuộc nền vào bảng thường. |
| C4 | **KHÔNG ĐO ĐƯỢC** | Không có phép đo/log Windows CI độc lập trên exact head; không dùng lời khai executor. |
| C5 | **KHÔNG ĐO ĐƯỢC** | Không có phép đo/log Ubuntu CI độc lập trên exact head; full suite sandbox không được gọi là CI. |
| C6 | **ĐẠT** | `python3 measure.py head gate`: rc=0/tổng 306/TỔNG: ĐẠT; đếm riêng `os.listdir` cho 306; base cũng 306. |
| C7 | **KHÔNG ĐO ĐƯỢC** | Không chạy Windows local. |
| C8 | **KHÔNG ĐẠT** | Còn F3/P3; verdict request_changes trên exact SHA đã neo. |
| C9 | **ĐẠT** | Ruff F delta 0 (cùng F541 đã có ở base); doctrine-scan rc=0/10 tệp/0 chỗ; diff --check rc=0; đúng hai tệp write set; rg glob 0 dòng với đối chứng base 2/mut-glob 1; numstat +40/−5 và +262/−0. |

## Finding còn mở

| ID | Mức | Slug | Phạm vi | Bằng chứng quyết định |
|---|---|---|---|---|
| F3 | P3 | `loi-do-thieu-chot-oserror-ngoai-permissionerror` | c100 mới và c99 nhánh liệt kê của packet | Mutant thu hẹp helper chỉ bắt PermissionError sống toàn suite; oracle độc lập EIO/ESTALE phân biệt head với cả hai mutant thu hẹp. |

- [P3] `loi-do-thieu-chot-oserror-ngoai-permissionerror`: `ops/bien_nhan_v2_test.py:3789` và `:3803` (c100, phép hỏi trạng thái), cùng `:3733` (c99, liệt kê), bảng đột biến `:4656`/`:4669` — `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 extra_mutate.py narrow_helper --suite` — tiến trình suite trên bản sao mutant **rc=0, 398.14 s**, `97/97 ca đạt · 149/149 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 131/149 đột biến thường khai đối chứng`, `TỔNG: ĐẠT`; nhưng `python3 errno_probe.py mut-narrow_helper sinh helper EIO` **rc=1**, hit=1, `Traceback ... OSError: [Errno 5] review EIO failure`, trong khi cùng lệnh với `head` rc=2, hit=1, `KHÔNG ĐO ĐƯỢC: không đọc được trạng thái ...`, không traceback — mở rộng test bằng OSError không phải PermissionError và thêm mutant thu hẹp catch phải chết đúng chốt.

HÌNH DẠNG: `loi-do`.

**Vì sao đây là thiếu chốt của phần mới:** `_hoi_trang_thai` tại sản phẩm:88–95 hứa và hiện thực đúng hợp đồng OSError. C100 chỉ tiêm PermissionError/EACCES ở cả is_dir và exists, nên không phân biệt bắt toàn OSError với chỉ bắt PermissionError. Mutant reviewer đặt `OSError = PermissionError` cục bộ trong helper trước `return hoi()`; nghĩa bắt lỗi thu hẹp, vẫn giữ nguyên các mốc văn bản m150/m153. Nó không phá rig, không phá import/parity, không bỏ test, và mọi mutant thường vẫn được báo CÓ RĂNG. Đây là chốt hồi quy thiếu răng cho một phần hợp đồng; xếp P3, **không** xếp P2 runtime vì head đang đúng.

**Đủ các đường của cùng lớp:** `errno_probe.py` đo guard kiem, helper trong kiem (stat lần hai), helper trong sinh nợ, `.git` khi thư mục receipt vắng, và scandir trên hai đường. EIO và ESTALE đều rc=2 ở head. `narrow_helper` phá bốn tổ hợp trạng thái; `narrow_listing` (cùng phép thu hẹp trong selector) còn qua c98/c99/c100/c89 và phá hai tổ hợp liệt kê. Mutant listing chưa chạy toàn suite; không suy rằng nó sống toàn suite. Hai mutant cùng một finding, không tách riêng từng biểu hiện để đẩy sang lượt sau.

**Vá ở đâu và thế nào:** thay đổi test `c100` cho các nhánh is_dir/exists và `c99` cho liệt kê, cùng bảng `_dot_bien`. Không cần đổi mã sản phẩm đang đúng. Giữ các ca PermissionError hiện có và thêm tối thiểu `OSError(errno.EIO, ...)`; kiểm hit dương, rc=2, đúng đường dẫn, không traceback trên tất cả đường liên quan. Thêm mutant `except PermissionError` thay `except OSError` ở mỗi helper, đòi chết tại đúng test trong khi c18 còn sạch. Nếu dùng mutant thay catch trực tiếp, cập nhật mốc rig cho đúng; không lấy lỗi mất neo làm tín dụng. Hai phép thu hẹp tương đương giữ neo đã chạy nằm ở `evidence/mut-narrow_helper.patch` và `evidence/mut-narrow_listing.patch`.

**Ca khóa đã chạy ngoài cây:** `python3 io_boundary_oracle.py head` → rc=0/**12/12**; `... mut-narrow_helper` → rc=1/**4/12** (8 phép lỗi trạng thái bị bỏ bắt); `... mut-narrow_listing` → rc=1/**8/12** (4 phép lỗi liệt kê bị bỏ bắt). Script `io_boundary_oracle.py` gọi mỗi phép tiêm bằng tiến trình riêng, đòi hit=1/rc=2/không traceback. Có thể dùng làm đặc tả phản chứng khi bổ sung c99/c100. Lệnh tạo mutant chỉ chạy lần đầu khi đích chưa có; để chạy lại suite trên hiện vật có sẵn: `cd work/mut-narrow_helper && python3 ops/bien_nhan_v2_test.py` với tiền tố môi trường đã nêu.

**Rủi ro khi vá test:** không chọn ENOENT/ENOTDIR làm lỗi bắt buộc rc=2, vì `Path.is_dir` có thể coi đó là vắng thật; không nới catch thành Exception để chữa test. Giữ chốt vắng thật (sinh nợ rc=0/#0), chốt lập trình đúng đối tượng và finally khôi phục monkeypatch. Tầng tiêm phải rõ: lỗi phát từ os.stat có thể được pathlib xử lý trước helper; EIO đã đo truyền qua thực thi Path thật, nên không dựa riêng vào monkeypatch phương thức để giả định điều đó. `ESTALE` là phép bổ sung đã đo, không bắt buộc làm test phụ thuộc nền này nếu bộ Windows thiếu hỗ trợ tương ứng.

## Tính toàn vẹn và giới hạn cuối

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 integrity.py` (log `evidence/integrity-run.{stdout,stderr,json}`, dữ liệu chi tiết `evidence/final-integrity.json`) rc=0. Head/tree/base vẫn đúng các neo; `.git` thường, detached, không nông, core.abbrev=7. Status bao gồm tracked/untracked/ignored của `cay-kho` và bản sao head rỗng; diff worktree/index so HEAD rỗng. Hai tệp write set byte-identical với blob HEAD; DIFF.patch và DIFF-LUOT3.patch byte-identical với git diff tương ứng; SPEC SHA-256 đúng neo. Đây là đối chiếu nội dung đầu/cuối, không phải lời khẳng định quan sát toàn bộ lịch sử ghi.

Tất cả tiến trình đo dùng để kết luận đã hoàn tất, không còn phép thử đang chờ. Windows CI/local, Ubuntu CI exact head và lỗi quyền phần cứng/hệ tệp thật: **KHÔNG ĐO ĐƯỢC**; các lỗi I/O trong bảng là phép tiêm có hit kiểm chứng. Không tự dựng nội dung nhạy cảm, không sửa mã nguồn checkout được review, không cấp quyền merge/land.
<!-- VERDICT-L3-KET-THUC -->

### Lượt 4 — sha256 `076ef6c837d6d580b9697377c2f0311d4365a7ab8fc1f40cb4b76a2cdaf78482`

<!-- VERDICT-L4-BAT-DAU -->
Verdict: approve
Reviewed commit: e9e0048b48ab610fee1246368b4f134c1ac4ae76
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Kết luận cuối: **approve** trên đúng commit dòng 2; **0 finding P0/P1/P2/P3 mở**. F3 lượt 3 **ĐÃ VÁ THẬT**, F1/F2 lượt 2 vẫn đóng. Head đạt `97/97 ca · 151/151 đột biến thường · 2/2 tự kiểm`, `TỔNG: ĐẠT`; mutant thu hẹp helper nay đỏ đúng c100 trong toàn suite, mutant thu hẹp liệt kê đỏ đúng c99 ở phép ca đích. Cổng thật rc=0/`tổng 306`, khớp phép đếm độc lập. Các lệnh, output và giới hạn được ghi dưới đây; Windows và CI exact head **KHÔNG ĐO ĐƯỢC**. Verdict này không cấp quyền merge/land.

Rà soát packet #1021 r2, lượt 4. Kết quả được ghi tăng dần. Các phép đột biến chỉ thực hiện trên bản sao đủ cây trong sandbox; mã nguồn `cay-kho/` được giữ nguyên. Mọi tiến trình đo dùng `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`; cấu hình `core.abbrev=7` theo chỉ thị.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn đối chiếu: `VERDICT-LUOT3.md` trên `8d9e3e3b55897575b9e69a13f5d1a4f3ff6c9fde` và `VERDICT-LUOT2.md` trên `5efa311fd857f7657a1c687e9ea37693070a37d3`. Không coi lời khai executor hoặc verdict cũ là phép đo trên head hiện tại.

| Finding / lớp cũ | Phân loại trên head mới | Bằng chứng độc lập |
|---|---|---|
| F3/P3 `loi-do-thieu-chot-oserror-ngoai-permissionerror` (lượt 3; hai biểu hiện helper/liệt kê) | **ĐÃ VÁ THẬT** | `extra_mutate.py narrow_helper --suite`: rc=1, 96/97, c100 `giet_that` đúng EIO; `extra_mutate.py narrow_listing`: c99 `giet_that` đúng EIO; c18 đều sạch. `errno_probe.py` đủ EIO/ESTALE, 12/12 ở head rc=2/hit=1/không traceback. Tracer đo đủ cả hai lớp và thử đột biến factory ở Đợt 3 chứng minh m154/m155 có răng riêng. |
| F1/P2 `loi-do-liet-ke-thu-muc-thoat-traceback` (lượt 2) | **ĐÃ VÁ THẬT**, không bị mở lại | `review_new.py error-child head <kiem\|sinh> <stat-os\|access>`: 4/4 rc=2/có hit/không traceback; lỗi liệt kê muộn cũng rc=2. |
| F2/P3 `loi-do-thieu-chot-ngoai-le-lap-trinh` (lượt 2) | **ĐÃ VÁ THẬT**, không bị mở lại | `boundary_oracle.py head` rc=0/2 trên 2 truyền đúng đối tượng; `new_mutate.py broad` và `broad_literal` chết đúng c100, c18 sạch; tracer có đủ bốn RuntimeError mốc. |

Ba lớp lịch sử trên mang HÌNH DẠNG: `loi-do`; 0 lớp/0 biểu hiện còn mở sau phép đối chiếu. Không có finding mới `bo-chon-ung-vien`.

## Nhật ký đo

### Đợt 1 — neo, phạm vi và phép tái hiện

`evidence/preflight.json`: `git -C cay-kho rev-parse HEAD HEAD^{tree} origin/master` rc=0 ⇒ head đúng dòng 2, tree `e1e840c06edf6d93d7ce0a527ca0d8c2d15dcd41`, base `757bde561d09738858506aecf5de2f050a5f0d5e`; `--is-shallow-repository` ⇒ `false`, `.git` là thư mục, HEAD detached, status tracked/untracked/ignored rỗng. SHA-256 SPEC khớp dòng 3. Hai patch được so byte với `git diff`: đều khớp.

`git diff 8d9e3e3..HEAD -- ops/bien_nhan_v2.py` rc=0/rỗng: mã sản phẩm không đổi từ lượt 3. `git diff --numstat 757bde5..HEAD` ⇒ `40 5 ops/bien_nhan_v2.py`, `283 0 ops/bien_nhan_v2_test.py`; đúng hai tệp write set. `git diff --check 757bde5..HEAD` rc=0/rỗng.

Các script `luot3-probe/*.py` được chép nguyên byte ra gốc sandbox để `ROOT=parent(__file__)` trỏ đúng nơi; chưa thay mốc neo/oracle trong `extra_mutate.py`, `errno_probe.py`, `probe.py`, `mutate.py`, `new_mutate.py`, `review_new.py`, `boundary_oracle.py`, `measure.py`. `work/head` và `work/base` là bản sao đủ cây, gồm `.git` thường; base checkout đúng SHA nêu trên. Các log lệnh chạy qua `measure.run` có ba tệp `.json` (lệnh/rc/thời gian), `.stdout`, `.stderr` trong `evidence/`.

`python3 extra_mutate.py narrow_helper --suite`: ca đích **c100 `giet_that`** với thông báo `[]: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021) — đòi mã thoát, không traceback`; c98/c99/c89 qua, c18 `[true, ""]`. Phần toàn suite đang chạy; chưa suy từ phép ca đích sang toàn suite.

`python3 extra_mutate.py narrow_listing`: ca đích **c99 `giet_that`** với thông báo `[]: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021): '…/ops/reviews' — đòi mã thoát, không traceback`; c98/c100/c89 qua, c18 `[true, ""]`. Script báo rc=0 vì ghi quan sát; trạng thái `giet_that` và thông báo trong `mut-narrow_listing-cases.stdout` mới là bằng chứng chết mutant.

`python3 measure.py head gate` (lệnh tương đương ghi trong `head-gate.json`) rc=0: `253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`, `TỔNG: ĐẠT`. Lệnh riêng `python3 -c 'import os; n=os.listdir("ops/reviews");print("casefold_suffix",sum(x.lower().endswith(".receipt.yaml") for x in n));print("exact_suffix",sum(x.endswith(".receipt.yaml") for x in n))'` ⇒ `306`, `306`. Base cũng đạt và đếm 306.

### Đợt 2 — EIO/ESTALE, F1/F2 và khôi phục phương thức

`python3 errno_probe.py <head|mut-narrow_helper|mut-narrow_listing> <mode> <site> <EIO|ESTALE>` chạy đủ sáu tổ hợp: `kiem/guard`, `kiem/helper`, `sinh/helper`, `kiem/git`, `kiem/listing`, `sinh/listing`. Mỗi tổ hợp/mã lỗi là tiến trình riêng. `evidence/errno-summary.json` tổng hợp 36 log: **head 12/12 rc=2, hit=1, không traceback**; `mut-narrow_helper` **8/12 rc=1/traceback** ở bốn tổ hợp trạng thái, 4/12 liệt kê vẫn rc=2; `mut-narrow_listing` **4/12 rc=1/traceback** ở hai đường liệt kê, 8/12 trạng thái vẫn rc=2. Tất cả 36 phép có hit=1. `kiem/helper` có attempts=2, nên đo riêng lần hỏi trạng thái thứ hai, không nhầm với guard. Head lỗi nêu đúng `ops/reviews`/`.git`; mutant kết thúc `OSError: [Errno 5|116] review EIO|ESTALE failure`.

F1 lượt 2: `python3 review_new.py error-child head <kiem|sinh> <stat-os|access>` ⇒ **4/4 rc=2**, `REVIEW_FAULT_HIT: stat-os`, `KHÔNG ĐO ĐƯỢC: không đọc được trạng thái …/ops/reviews (PermissionError…)`, không traceback. Nhánh iterator đã yield rồi lỗi (`late`) cũng rc=2 trên cả hai đường.

F2 lượt 2: `python3 review_new.py error-child head <kiem|sinh> <runtime|value>` ⇒ **4/4 rc=1**, traceback đúng `RuntimeError|ValueError: review programming fault`; không bị đổi thành KhongDoDuoc. `python3 boundary_oracle.py head` rc=0, hai đường `propagated_same_error=true, hit=1, restored=true`. `python3 new_mutate.py broad` và `broad_literal` ⇒ c100 **giet_that**: `lỗi lập trình ở iterdir [] bị nuốt/đổi: đòi RuntimeError mốc đi thẳng ra, được không ngoại lệ`; c98/c99/c89 qua, c18 sạch.

Phép mới `python3 audit_l4.py head <c99|c100> trace` dùng `sys.settrace` quan sát ngoại lệ THỰC SỰ ném từ `hong`/`gia` trong test nguyên trạng, không đếm lần tạo đối tượng chỉ phục vụ thông báo:

| Chốt / phương thức | Đường | PermissionError(EACCES) thực ném | OSError(EIO) thực ném |
|---|---|---:|---:|
| c99 / iterdir | kiem | 1 | 1 |
| c99 / iterdir | sinh | 1 | 1 |
| c100 / is_dir | kiem | 1 | 1 |
| c100 / is_dir | sinh | 1 | 1 |
| c100 / exists(.git) | kiem | 1 | 1 |

Cả hai lệnh rc=0, ca `qua`, mọi `restored=true`. **5/5 lần EIO có `type(ex) is OSError`, `isinstance(ex, PermissionError)=false`, errno=5**; 5 lần EACCES là PermissionError/errno=13. Vì vậy chốt không qua do Python đổi EIO thành PermissionError. Tracer c100 còn đo bốn RuntimeError của chốt (7), đủ iterdir/is_dir × kiem/sinh, tất cả đúng đối tượng mốc.

`python3 audit_l4.py head <c99|c100> cleanup <stage> <rig|runtime|value>`: c99 stage 1..4, c100 stage 1..10, tổng **42/42 tiến trình rc=0**. Tiêm ngắt tại mỗi lần gọi main khi Path đang bị thay; sau ngắt `Path.is_dir`, `Path.exists`, `Path.iterdir` đều đúng đối tượng gốc; chạy lại chính ca `qua`, c18 sạch, kiểm cuối vẫn khôi phục. Có lỗi giàn giáo/ngoại lệ khi cố tình ngắt, không dùng chúng làm tín dụng giết mutant. Không phát hiện rò monkeypatch trong phạm vi các nhánh đã đo.

### Đợt 3 — đột biến mới của phần EIO

`python3 mutate_l4.py <tên>` tạo một bản sao đầy đủ `work/mut4-<tên>` và patch trong `evidence/`; mỗi đột biến chạy tiến trình riêng. `probe.py` chạy c98/c99/c100/c89 và đối chứng c18. Với đột biến tệp test, `focused_l4.py` lấy bằng AST đúng thân đăng ký m154/m155 cùng hàm `do`/các biến của `_dot_bien` hiện tại; giữ nguyên cơ chế giết thật/đối chứng/khôi phục, chỉ chọn hai đăng ký cần đo. Đây là phép đo chọn lọc, KHÔNG được gọi là toàn suite.

| Đột biến reviewer | Kết quả đo | Diễn giải |
|---|---|---|
| `eio_helper_empty`: EIO trong `_hoi_trang_thai` trả False | c100 **giet_that**, c18 sạch | Vẫn rc=2 nhưng thông báo thành “kho thật mà không có”; chốt bắt được SAI NGHĨA, không chỉ so rc. |
| `eio_git_escape`: chỉ EIO ở `.git` được ném lại | c100 **giet_that**, `CLI chết bằng OSError: [Errno 5]…`; c18 sạch | Phân biệt nhánh `.git` với is_dir, không chết ở phép PermissionError trước đó. |
| `eio_listing_empty`: EIO khi liệt kê trả danh sách rỗng | c99 **giet_that**, c18 sạch | Vẫn rc=2 nhưng thông báo thành “không có tệp”; chốt đòi “không liệt kê được”. |
| `c99_duplicate_permission`: đổi errno của factory mới EIO → EACCES | **SỐNG ở bốn ca thường**, nhưng phép m155 **KHÔNG RĂNG / qua**, focused rc=1; m154 còn CÓ RĂNG | Tracer ghi 4 PermissionError, 0 OSError thuần. Bảng đột biến phát hiện sự mất lớp EIO của c99. |
| `c100_duplicate_permission`: đổi errno của OS_LOI mới EIO → EACCES | **SỐNG ở bốn ca thường**, nhưng phép m154 **KHÔNG RĂNG / qua**, focused rc=1; m155 còn CÓ RĂNG | Tracer ghi 6 PermissionError, 0 OSError thuần, bốn RuntimeError; bảng đột biến phát hiện sự mất lớp EIO của c100. |
| `reverse_osloi`: đảo thứ tự hai factory tại cả hai vòng OS_LOI | **SỐNG** ở các ca thường và focused rc=0/2 trên 2 CÓ RĂNG | Đối chứng tương đương: vẫn đủ 3 EIO + 3 EACCES + 4 RuntimeError, Path khôi phục. Không phải lỗi cần giết; thứ tự factory không thuộc hợp đồng. |

Cả sáu mutant có c18 sạch. Hai mutant làm mất EIO chỉ sống ở tầng ca thường; không được mô tả là sống qua toàn suite. Không có mutant sai hành vi sản phẩm nào trong tập mới này sống ở ca đích. Log chi tiết `mut4-*-cases.stdout`, `mut4-*-focused.{stdout,json}`, `mut4-*-trace.stdout`; m154/m155 trên head đối chứng focused rc=0/cả hai `giet_that`.

### Đợt 4 — C1/C2/C3/C9

`python3 probe.py head behaviors` (`head-behaviors` và từng `fixture-head-*`) ⇒ C1a rc=1/`tổng 2`/nêu `x.RECEIPT.YAML`/không `TỔNG: ĐẠT`; chỉ-x rc=1/`tổng 1`/không “không có tệp”; C1b rc=2/stderr nêu x/không traceback/không dòng tổng. Thư mục `X.RECEIPT.YAML` tới bước băm rồi rc=2. Base được đo lại: C1a tổng 1/bỏ x, chỉ-x rc=2/không có tệp, C1b rc=1/bỏ x.

`python3 mutate.py exact --behaviors` ⇒ c98/c99 **giet_that**, c18 sạch; fixture C1a/C1b/chỉ-x bỏ x. `python3 mutate.py isfile --behaviors` ⇒ c89 **giet_that**, `đòi rc=2 nêu tệp hỏng, được rc=1`, c18 sạch. `python3 mutate.py glob --behaviors` ⇒ c98/c99 **giet_that** vì bỏ x, c18 sạch; c100 `gian_giao` vì không gọi iterdir KHÔNG được tính làm tín dụng chết. C3 dựa vào c98 và kết quả fixture, không dựa vào lỗi giàn giáo.

C9: Ruff **đỏ sẵn, delta=0**, không ghi “Ruff sạch”: `python3 -m ruff check --no-cache --select F --output-format json ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` head/base cùng rc=1, chỉ F541 `f-string without any placeholders`, cột 19 tại cùng dòng nội dung của test; vị trí dịch 1677 → 1678 do import. So chuẩn hóa theo tên tệp/rule/thông báo/cột/nội dung dòng cho delta 0 (`criteria-summary.json`); `python3 -m ruff --version` ⇒ `ruff 0.15.15`. Chỉ đo bare lint theo tiêu chí; không suy đã đo pin/probe CI.

`python3 .claude/dev/packet_loop.py doctrine-scan --root .` head/base rc=0: `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` head rc=1/0 dòng, base 2 dòng (1442/1601), mutant glob rc=0/1 dòng (116). Vế dương C1a/C1b đã đo riêng ở trên. `python3 summarize_l4.py` rc=0 đối chiếu các log criterion và cleanup bằng assertion; kết quả `evidence/criteria-summary.json`.

### Đợt 5 — toàn suite và chốt cuối

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 measure.py head suite` chạy `python3 ops/bien_nhan_v2_test.py` trong `work/head`: **rc=0, 401.34 s**, stderr rỗng, output:

```text
bien_nhan_v2_test: 97/97 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 133/151 đột biến thường khai đối chứng
TỔNG: ĐẠT
```

`python3 extra_mutate.py narrow_helper --suite` đã hoàn tất phần suite trên bản sao mutant: **rc=1, 403.08 s**, stderr rỗng, **96/97 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt**, `TỔNG: ĐỎ`. Ca thường duy nhất đỏ:

```text
ĐỎ  c100_LOI_TRANG_THAI_thu_muc_la_rc2_va_LOI_LAP_TRINH_di_thang [giet_that]: []: CLI chết bằng OSError: [Errno 5] I/O error (tiêm, #1021) — đòi mã thoát, không traceback
```

Log `head-suite.{json,stdout,stderr}` và `mut-narrow_helper-suite.{json,stdout,stderr}`. m154/m155 trong head đều **CÓ RĂNG / giet_that** tại đúng c100/c99. Không lấy rc đơn lẻ hoặc việc giàn giáo hỏng làm bằng chứng đạt. Không chạy toàn suite cho narrow_listing vì phép tái hiện được yêu cầu ở mutant ấy là ca đích; không suy số liệu toàn suite cho nó.

## Bảng tiêu chí cuối

| Tiêu chí | Kết quả | Lệnh / output quyết định |
|---|---|---|
| Suite head | **ĐẠT** | `python3 measure.py head suite`: rc=0, 97/97 · 151/151 · 2/2, `TỔNG: ĐẠT`; Đợt 5. |
| C1a | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | `probe.py head behaviors`: rc=1/tổng 2/nêu x; chỉ-x tổng 1/không “không có tệp”. `mutate.py exact --behaviors` giết thật c98, c18 sạch. |
| C1b | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | Cùng phép behaviors: YAML hỏng đuôi hoa rc=2/nêu x/không traceback; mutant exact bỏ x. |
| C2 | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | Suite head in `ĐẠT c89_B2_receipt_KHONG_DOC_DUOC_la_rc2_khong_traceback`; `mutate.py isfile --behaviors` ⇒ c89 `giet_that`, c18 sạch. |
| C3 | **ĐẠT phép hoàn nguyên glob được yêu cầu** | `mutate.py glob --behaviors` ⇒ c98 `giet_that` vì tổng 1/bỏ x, c18 sạch. Không đưa mutant glob phụ thuộc nền vào bảng thường. |
| C4 | **KHÔNG ĐO ĐƯỢC** | Không có phép đo độc lập job/runner/log Windows CI trên exact head trong lượt này. |
| C5 | **KHÔNG ĐO ĐƯỢC** | Không có phép đo độc lập job/runner/log Ubuntu CI trên exact head trong lượt này; suite vừa chạy không được nhận là CI. |
| C6 | **ĐẠT** | `measure.py head gate`: rc=0/`tổng 306`/`TỔNG: ĐẠT`; lệnh `os.listdir` riêng đếm 306. Base cũng 306. |
| C7 | **KHÔNG ĐO ĐƯỢC** | Không chạy Windows local; không suy kết quả từ ghi chú lease/ADR hay báo cáo executor. |
| C8 — phần review | **ĐẠT ngưỡng nội dung review** | 0 P0/P1/P2/P3 mở, exact reviewed SHA đúng dòng 2; lượt cuối theo assignment. Các cổng CI/Windows chưa đo không được coi đã đạt; không cấp quyền merge/land. |
| C9 | **ĐẠT** | Ruff F delta 0; doctrine rc=0/10 tệp/0 chỗ; diff-check rc=0; glob 0 dòng; numstat đúng hai tệp +40/−5 và +283/−0. Đợt 1/4 và `criteria-summary.json`. |

## Bảng finding cuối

| Mức | Số finding mở | Vị trí / tái hiện / hướng vá |
|---|---:|---|
| P0 / P1 / P2 / P3 | **0 / 0 / 0 / 0** | Không có finding mới cần vá trong phạm vi đã đo. Bằng chứng đóng ba lớp lịch sử nằm ở bảng đối chiếu và Đợt 1–5. |

Không tạo mục `[P0..P3]` hay gán `HÌNH DẠNG` cho một lỗi không tồn tại. Các mutant tương đương hoặc chỉ sống ở một tầng được phân biệt rõ tại Đợt 3; không che mutant sống, cũng không biến đối chứng tương đương thành finding.

## Toàn vẹn cuối và giới hạn

`python3 integrity.py` qua `measure.run('integrity-run', ...)`: **rc=0**; `evidence/final-integrity.json` ghi lại lệnh và kết quả. Head/tree/base không đổi so neo ban đầu, detached, không nông, `core.abbrev=7`. Status gồm tracked/untracked/ignored của `cay-kho` và `work/head` rỗng; diff worktree/index so HEAD rỗng. Hai tệp write set byte-identical với blob HEAD; DIFF.patch và DIFF-LUOT4.patch byte-identical với diff tương ứng; SPEC giữ đúng SHA-256 dòng 3. Đây là đối chiếu nội dung tại hai mốc, không phải lời khẳng định đã quan sát toàn bộ lịch sử ghi.

`integrity.py` là script cũ duy nhất được chỉnh: mốc `previous-head` từ `99c463d` thành `8d9e3e3`, diff lượt từ `5efa311`/`DIFF-LUOT3.patch` thành `8d9e3e3`/`DIFF-LUOT4.patch`, cùng tên khóa assert tương ứng. Không đổi oracle kiểm toàn vẹn. `evidence/adapter-integrity.patch` giữ diff; `probe-provenance.json` ghi SHA-256 và xác nhận **15/16 script cũ nguyên byte**. Các script mới là `audit_l4.py`, `focused_l4.py`, `mutate_l4.py`, `summarize_l4.py`.

Tất cả tiến trình đo dùng cho kết luận đã hoàn tất. Các lỗi I/O được nêu là phép tiêm có hit kiểm chứng, không phải đo sự cố phần cứng/quyền truy cập thật. Windows CI/local và Ubuntu CI exact head: **KHÔNG ĐO ĐƯỢC**. Không dùng lời khai executor thay số đo, không sửa mã nguồn checkout được review, không cấp quyền merge/land.
<!-- VERDICT-L4-KET-THUC -->
