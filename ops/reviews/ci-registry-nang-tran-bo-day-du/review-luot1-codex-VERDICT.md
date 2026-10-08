verdict: changes_requested
reviewed_sha: f9c8dbd53a21d4048d26572f3147893f6c57e95b
spec_sha256: 78959c880b109a6c77f17c6e0feeaa86f0e21a1b32cb47a02ba8071361a1b90e
reviewer_provider: openai_codex
reviewer_model: gpt-6.1-sol
execution_surface: codex_cli
transport: machine

Tree: `cbfaf5788eca68ee7325604e5bdb2a47ef50d41e`. Review độc lập với executor Claude, phiên CLI `01a11728-0885-7d03-8ebc-2a62375553e1`; model đọc từ header phiên, lưu ở `inputs/session-header.txt`. Không suy identity từ actor GitHub. Không đăng GitHub, push, dispatch/rerun CI hoặc sửa `cay-kho/`/`kho.git/`.

**Hai trục và quyết định.** Áp ngưỡng của PROMPT: chỉ approve khi không còn lớp P1/P2/P3. Có **0 P1 · 1 P2 · 1 P3**. Lỗ test runtime có sẵn trên nền (review Claude lượt 2 gọi là R1); chỉ thị lượt này yêu cầu phân lớp mutant sống, nên không coi quan sát ấy là lớp đã đóng.

| Trục | Kết quả |
|---|---|
| Spec acceptance | M1–M9 đúng trên ứng viên. A1/A2/A3/A5/A6 có bằng chứng dương. A4 có delta 0 ở cả ba bộ, nhưng suite local nguyên bản của launcher/đường nhanh đỏ sẵn do môi trường; không khai mọi gate tại chỗ xanh. |
| Standards | Hai lớp mở dưới đây. Runtime hiện tại dùng 5400 đúng; phép phản chứng phát hiện thiếu chốt cho đường tiêu thụ trần, và dữ liệu giải thích trong Issue/spec còn sai. |

**Bảng lớp — một cơ chế một lớp.**

| Slug | Hạng | Biểu hiện | Phép đo | Hướng vá |
|---|---|---|---|---|
| `tran-runtime-khong-duoc-ca-kiem-khoa` | P2 | `.claude/dev/ci_dang_ky_test.py:2162` chỉ so hằng/quan hệ với job; bỏ ngỏ default ở `:924` và đường `_chay_that` ở `:964`. Tham số đi tới `communicate` ở `:936`. | Hai mutant runtime về 4500: suite **rc=0, 1025/1025**, nhưng probe **rc=1, runtime timeout=4500; GIAY_TOI_DA_MOT_BO=5400**. | Bổ sung đo qua `_chay_that` vào ca p643 hiện có; giữ số ca. Hint đã kiểm. |
| `ty-le-cham-khong-khop-so-do` | P3 | `SPEC.md:42` / `ops/specs/CI-REGISTRY-NANG-TRAN-BO-DAY-DU-r2.md:42` còn 25–40%; `:45` gọi 1,40 là mức chậm nhất và dùng biên ~6%. `readback-issue-705.json:1` (`body`, câu về 25–40%, dòng 20 của bản giải mã ở `inputs/issue-705-body.md`) lặp dải sai. | `static_audit.py`, **rc=0**: pretooluse **32,713–42,232%**, subagent **22,152–26,582%**; max **1,422319**, làm tròn 1,42; 5400/(3645×1,42)−1 = **4,330%**. | Owner cấp erratum/revision mới cho spec và sửa lời giải thích Issue; giữ byte spec r2 đã đóng băng. Hunk spec là đề xuất nội dung, không cấp quyền sửa nó. |

Lớp P2 là lỗi bao phủ phản chứng, **không phải lời khai ứng viên đang chạy trần 4500**. Đối chứng `python3.12 $R/goi/runtime_probe.py` trong bản sao head: **rc=0**, `runtime timeout=5400; GIAY_TOI_DA_MOT_BO=5400; result=(0, '', None)`.

Phản chứng P2 (script `runtime_mutations.py`, luôn restore trước mỗi lần):

```python
# Đột biến 1 — đúng một neo ở W1:924
gioi_han=GIAY_TOI_DA_MOT_BO, env_doi=None
# thành
gioi_han=4500, env_doi=None

# Đột biến 2 — đúng một neo ở W1:964
goc_tam=goc_tam, env_doi=env_theo_che_do(path, che_do)
# thành
goc_tam=goc_tam, gioi_han=4500, env_doi=env_theo_che_do(path, che_do)
```

Với **mỗi** mutant: `python3.12 .claude/dev/ci_dang_ky_test.py` **rc=0**, `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT`; `python3.12 $R/goi/runtime_probe.py` **rc=1**, đo được trần 4500. Probe chỉ giả tiến trình con/liveness, không chờ 75/90 phút. Mutant thay `p.communicate(timeout=gioi_han)` thành `...4500` **bị test hiện hữu giết**: rc=1, 1021/1025, đúng các ca p637-A3c; không gộp nó vào số mutant sống. Đo độc lập trên baseline 7e5958e (`preexisting_probe.py`): default runtime về 3000 vẫn **rc=0, 1025/1025**, probe **rc=1, timeout=3000; hằng=4500**; xác nhận lỗ có sẵn, không dựa lời review trước.

Vá tại p643 vì đây là ca đã khóa mục tiêu trần của W1, không cần mở W khác hay thêm ca làm N lệch. Hint dùng child giả để đo timeout thực sự truyền tới `communicate` qua `_chay_that`. Đối chứng sau hint **rc=0, 1025/1025**; hai mutant default/wrapper sau hint đều **rc=1, 1024/1025**, `ĐỘT BIẾN p643-tran-bo-nho-hon-timeout-job: LỌT`. Rủi ro: mock chỉ kiểm truyền tham số, không kiểm một deadline tường dài trên runner; các ca kill-tree hiện hữu vẫn cần giữ.

Vá lớp P3 tại nguồn số của spec và lời giải thích Issue vì chú thích mã W1:697–700 đã đúng 22–42%/~4%. Không đổi các số đo thô hay lựa chọn 5400/105. Ca khóa: tính lại từng tỷ lệ từ 914/1213/1300 và 316/386/400, rồi so dải khai và mẫu số dùng tính biên. Hướng rẻ nhất là erratum có neo, tiếp đó revision/hash/lease mới nếu cần áp hunk spec. Rủi ro: sửa âm thầm spec r2 làm mất tính bất biến; hint không được áp trực tiếp lên tệp đã đóng băng. Nguyên nhân runner là suy luận từ số đo được giao, không được reviewer tái benchmark hai lượt 4604/4586 s.

**Preflight, write set và merge.**

`sha256sum PROMPT.md SPEC.md lease-g2.yaml` **rc=0**:

```text
058296a846c07607eaded73ffde6c278dce6a63497d491ff22412a13ff518508  PROMPT.md
78959c880b109a6c77f17c6e0feeaa86f0e21a1b32cb47a02ba8071361a1b90e  SPEC.md
4cd2d686ef74f91a51dde704ed7d39c2a57850ee57b300f02dc25c3a6dabc73f  lease-g2.yaml
```

`git -C cay-kho rev-parse HEAD HEAD^{tree}` **rc=0**, head/tree như trên; `git -C cay-kho status --short` **rc=0, stdout rỗng**, đầu và cuối lượt. Spec blob tại `6c7f0b50828d708ec952d22f9123ea598ac004ef:ops/specs/CI-REGISTRY-NANG-TRAN-BO-DAY-DU-r2.md` có đúng SHA-256 spec. Write-set hash tính lại là `ad1358ad5099e3cb3ddee76189b1d1292fbd4ebfa875e57be113606e9ab71bb0`; baseline nghiệm thu `7e5958e440285c8d63d2f710cf97ba20b85f2926`; lease r2/g2, sensitive. Lease là lease executor lịch sử, đã hết hạn 02-10; chỉ thị hiện tại cấp review read-only, không gia hạn quyền thi công.

Các lệnh Git dưới đây chạy trên bản sao, **rc=0**:

| Lệnh | Output thực |
|---|---|
| `git diff --name-status ab457c6...f9c8dbd` | Chỉ W1–W4, tất cả M. |
| `git diff --numstat ab457c6...f9c8dbd` | W1 +11/−6; W3 +1/−1; W2 +3/−1; W4 +1/−1. Tổng **4 tệp, +16/−9**. |
| `git merge-base ab457c6 f9c8dbd` | `8c98afacb9285aa71e5200739236284f7a190d4f` |
| `git show -s --format=%H%n%T%n%P%n%B f9c8dbd` | Head/tree như trên; parents `f783fbf363047adf9057b34cb06a60c0deed01df 8c98afacb9285aa71e5200739236284f7a190d4f`. |
| `git diff 8c98afa ab457c6 -- <W1 W2 W3 W4>` | Rỗng; drift không đổi bốn đường. |
| `git merge-tree --write-tree ab457c6 f9c8dbd` | `fb8b2da06c992da1d556051c7d07213c1a83c3fb`, không conflict. |

Merge commit không kéo đường ngoài write set vào diff PR **ba chấm** so master. So **hai chấm** `ab457c6 f9c8dbd` còn thấy sáu đường code/protocol của drift ở master (`packet_loop.py`, `packet_loop_test.py`, hai tài liệu protocol/prompt, `lease_publish.py`, `lease_publish_test.py`); đó là phía master tiến thêm, không được gán thành phần PR đã thêm. Chúng được liệt kê nguyên vẹn trong `write-set-direct.log`.

**Đối chiếu từng M1–M9.**

| Mục | Kết quả và mỏ neo trên candidate |
|---|---|
| M1 | ĐẠT: W1:700 = 5400; chú thích :693–699 nêu số đo/lý do; probe runtime đối chứng 5400. Lớp P2 nói về chốt còn thiếu. |
| M2 | ĐẠT: `bam_gate_registry` thật tính `9dd2c23db45fd97c4ce44a98ff0abe74e21b4b2c64a97dab318addb92d3458d9`, khớp W1:742. So dict job nền/head loại timeout: giống nhau. |
| M3 | ĐẠT: p643 :2162–2163 khóa 5400 và `< 60×105`; `du-timeout-float` :2099 lấy 105.0; `timeout-trung` :2119 tạo khóa 105 trùng và actionlint phát hiện. |
| M4 | ĐẠT: W2:845 timeout là int 105. |
| M5 | ĐẠT: W3:21 timeout là int 105; đồng bộ bằng validator có kiểm kiểu. |
| M6 | ĐẠT: W4:2199 = 105; so AST `KHUNG_JOB` với nền chỉ đổi đúng ô này. y13 đối chứng xanh trong suite; mutant đỏ rc=3 đúng khóa timeout. |
| M7 | ĐẠT: W2:836–837 có #705/105; chỉ chú thích, không thêm thay đổi dict YAML ngoài M4. |
| M8 | ĐẠT: W1:697–699 khai 22–42%, ~4% trên 1,42; tính lại khớp. Lớp P3 ở spec/Issue, không ở chú thích đã vá. |
| M9 | ĐẠT: lấy float từ `_wf0["jobs"]["gate-registry"]["timeout-minutes"]`; A6 cả 105 và 120 phân biệt kiểu, không thắng do lệch giá trị. |

`python3.12 $R/goi/static_audit.py` **rc=0** (record `static-audit-recorded`). Tự kiểm kê bằng `rg --hidden` và AST: **336 tệp** có số cũ, **91 dòng** ở các loại mã/config sống; AST quét **128 tệp Python sống**, thấy **31 literal 90/90.0, không literal 4500**. Danh sách đầy đủ ở `rg-old-numbers-all-files.log`, `rg-old-numbers-live.log`, `ast-old-numbers.json`; thêm `rg-live-registry-consumers.log` rà mọi consumer theo tên, không dựa danh sách spec.

Các số còn lại cùng chữ nhưng khác vai: W1:693/696/697 và W2:834–837 là lịch sử lần nâng/timeout đã đo; W1:876 `90.0 == 90` là ví dụ Python so kiểu; W1:1917 là dữ liệu benchmark worker. `launcher.py:2700`, `mcp_gh.py:113`, `gate_lifecycle_test.py:1042/1196/1363`, `gws_bridge.py:269`, `tl_core/release.py:110/111` là timeout **giây của phép đo/network khác**. Những literal 90 còn lại là cắt chuỗi, độ dài, điểm ưu tiên, TTL hoặc fixture. Các bản spec/lease/land/review lịch sử được giữ byte; không coi bản sao mã nằm trong evidence cũ là consumer CI sống. Không tìm thấy trần registry đang sống bị diff bỏ sót.

**A1–A6 — lệnh, rc và bằng chứng dương.** Mọi lệnh Python chạy ở bản sao exact tree, `core.abbrev=7`, HOME riêng, `PYTHONDONTWRITEBYTECODE=1`, TMPDIR/TEMP/TMP dưới `$R/tmp-review/`. Hai vế cùng một driver `python3.12 goi/review_harness.py suites`, cùng argv cho mỗi bộ. JSON mỗi subprocess lưu rc thật; rc driver không thay rc từng bộ.

| Nghiệm thu | Lệnh/phép đo | Rc và output |
|---|---|---|
| A1 | `python3.12 .claude/dev/ci_dang_ky_test.py`, base rồi head | **0/0**; cả hai `ĐĂNG KÝ: 23/23`, `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT`. Không mất ca. |
| A2a | Hằng về 4500, cùng lệnh registry | **1**; p643 `LỌT`, 1024/1025, TỔNG ĐỎ. |
| A2b | Chỉ gate-registry ci.yml về 90, registry | **1**; `gate-registry đổi (băm b42a413f852e0852f0e59ef8acaf6757a771c2e55e296714426a73e7e308ebc9)`. |
| A2c | Chỉ dot-bien-du về 90, registry | **1**; `ĐỘT BIẾN ĐỦ (#651 M4): job: timeout-minutes lệch gate-registry`. |
| A2d | Hằng 6300 = 60×105, registry | **1**; p643 `LỌT`. Bổ sung đổi luôn equality kỳ vọng thành 6300: vẫn **1**, p643 `LỌT`, chứng minh nhánh `<` có răng. |
| A3 | `actionlint -oneline <workflow>` trên **cả hai workflow**, base/master/head | **0** ở cả 6 lần; stdout rỗng, delta tập lỗi 0. |
| A3 | `ruff check --no-cache --select F --output-format json <W1 W4>` trên base/master/head | **0** cả 3 lần; tập lỗi **[]/[]/[]**, delta theo tập 0 trên cả hai .py đổi. |
| A4 launcher | `python3.12 .claude/dev/launcher_test.py`, base/head | **1/1**; cả hai **179/180** đã chạy qua, tổng **189**, bỏ **9**, hỏng **1**. Cùng skip/fail, delta 0; không khai 188/188. |
| A4 t152 | `python3.12 .claude/dev/launcher_test.py --lap-ca t152_hook_cai_dat_va_khop_al_ver_ci --lan 1`, base/head | **0/0**, `1/1 qua, 0 bo qua, 0 hong`. |
| A4 lease | `python3.12 ops/lease_publish_test.py`, base/head | **0/0**, cả hai `lease_publish: 198/198 đạt; đã chạy=198, bỏ qua=0`. Delta 0. |
| A4 đường nhanh | `python3.12 ops/ci_duong_nhanh_test.py`, base/head | **1/1**, cả hai `CA: 103/104 dat · 0 do · 1 hong`, `DOT BIEN: 378/383 bi giet dung ly do`, `TONG: DO`. Delta ca/mutant và lớp hỏng 0. |
| A5 | Đọc CI run **36866566503**, registry job **110383519032**, liên kết head f9c8dbd | MCP **isError=false**, job/step registry success, `N=2`, `nhanh_don_duoc_test` **day_du, rc=0, 4582,033 s**, `TỔNG: ĐẠT`; job khoảng **84,750 phút < 105**. Reviewer không chạy thêm CI. |
| A6 M6 | ci.yml về 90; `python3.12 ops/ci_duong_nhanh_test.py --mot-ca y13_khoa_topology_cua_ci_yml_ngoai_than_run` | **3**, `DO:y13...:gate-registry...khac ['timeout-minutes']`; không traceback/rc=4. Đảo riêng KHUNG_JOB về 90 cũng **3** cùng lý do. |
| A6 M9, 105 | Nới riêng điểm `_bang_kieu(job.get(k), goc.get(k))` thành so `==`, gọi `phan_chung()` thật | **1**, p661-M5-du-timeout-float-do `LỌT`, 1024/1025. |
| A6 M9, 120 | Nâng **hai** timeout giả định lên 120; chọn đúng ca M9 từ `phan_chung()` | Đối chứng **0**, `ĐỎ đúng`; nới so kiểu **1**, `LỌT`. Chỉ chứng minh ca M9, không khai toàn suite tương lai xanh. |

Rollback riêng fixture M9 về `90.0` cho registry chính **rc=0, 1025/1025**; nhưng khi nới so kiểu, ca vẫn `ĐỎ đúng` do sai giá trị. Phép độc lập A6 đòi `LỌT` nên **rc=1**, bác rollback (`M9-rollback-A6-rejected.log`). Vì vậy A6 thật sự kiểm nguồn giá trị/kiểu, không suy từ một lần suite chính xanh.

Đường nhanh nguyên bản hỏng `t20zo_la_khong_phai_tep_thuong_do` vì `AF_UNIX.bind` bị sandbox trả `PermissionError`; năm mutant báo **HONG do control không xanh**, không phải sống sót của patch. Phép bổ sung (`socket_fixture_probe.py`) tạo inode socket thật `S_IFSOCK` bằng `mknod`: cả hai vế ca t20zo **rc=0**, năm mutant **5/5 GIET, rc=0**. Không gộp thành lời khai suite nguyên bản 104/104·383/383 tại chỗ. CI gate-ops job **110383519026** có log nguyên bản **104/104·383/383, TONG DAT** trên merge ref e4ee9d5 ghép head f9c8dbd với 8c98afa.

Launcher bỏ t62 Windows và tám ca thiếu venv/pip trong sandbox; cùng hỏng `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` ở cả hai vế. Hai tệp launcher/lease test trùng byte base/head; mọi lỗi/skip nêu ở đây là delta 0, không được nâng thành pass toàn bộ. Log/rc/case names giữ nguyên trong evidence.

**Standards về ngân sách job.** Registry có 9 bộ, chạy ThreadPool N=2 theo thứ tự MOI; hai bộ guard/subagent chạy đồng thời, không cộng tuần tự mọi thời gian bộ vào job. Run A5 đo `pretooluse_guard_test` 1291,011 s, `subagent_ghi_detect_test` 403,378 s; bộ dài nhất bắt đầu sau **465,931 s = 7,766 phút** kể từ worker đầu, thiết lập **36,349 s**, teardown **0,676 s**. Hai bộ kia đã xong trước khi bộ dài nhất xong; chiếu thay riêng thời gian bộ dài nhất bằng 5400:

`(36,349 + 465,931 + 5400 + 0,676)/60 = 98,383 phút`, còn **6,617 phút** so trần 105. Có chỗ cho các bộ còn lại theo số đo này; không thấy lỗi cỡ trần job. Giả định giữ thời gian hàng chờ/setup/các bộ khác như lượt đo, không phải bảo đảm mọi runner.

Biên cũ 19% đúng nếu mẫu số là **4500**: `(4500−3645)/4500`; sức chịu chậm so baseline là **23,457%** nếu mẫu số 3645. Biên mới so baseline **48,148%**. Với max thô 1300/914, chiếu 5184,354 s và biên còn **4,160%**; dùng 1,42 làm tròn cho **4,330%**. Lớp P3 là câu 25–40%/“1,40 cao nhất” và cách giải thích ~6%, không phải chọn 5400/105 hay phép đổi 5400 s = 90 phút.

**Hint và hiện vật.** `HINT.patch` unified diff repo-relative, không `a/`/`b/`, hai nhóm `# lop:`. Dry-run trên bản sao candidate **phủ đúng blob spec lease** (spec ở nhánh lease, vắng trên PR), `patch --dry-run -p0 --fuzz=0 -i $R/goi/HINT.patch` **rc=0**, output:

```text
checking file .claude/dev/ci_dang_ky_test.py
checking file ops/specs/CI-REGISTRY-NANG-TRAN-BO-DAY-DU-r2.md
```

Apply chỉ trên scratch **rc=0**; registry đối chứng sau hint **0, 1025/1025**, Ruff F **0**, hai mutant runtime **1/1** đúng p643. Hunk spec nằm ngoài write set PR, chỉ là đề xuất cho owner tạo erratum/revision; không gán quyền sửa r2 cho executor. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

`EVIDENCE.zip` chứa harness, raw logs/rc, phản hồi MCP, bản giải mã CI_DANG_KY_THOI_GIAN, input đóng băng và manifest SHA-256. `commands.json` lưu mọi argv/cwd/rc subprocess trong harness; đọc GitHub có `isError` riêng, không bịa rc. Python 3.12.3, PyYAML 6.0.1, Ruff 0.15.8, actionlint 1.7.7, shellcheck 0.9.0. Không chạy Python 3.11. Ruff/PyYAML khác bản ghim CI; ba vế lint dùng cùng công cụ đã có. Không cài thêm. Dữ liệu cuối vẫn khớp preflight; bản sao base/head sạch.

**KHÔNG ĐO ĐƯỢC / không chạy.** Một lượt suite local nguyên bản đường nhanh đầy đủ xanh do bind bị chặn; toàn bộ launcher đầy đủ xanh do venv/pip và ca r351; runner chậm nhất có đủ 5400 hay không; thời gian thật các lượt bị giết ở 4500; tái benchmark 4604/4586 s; Windows; toàn bộ lịch sử attempt CI (wrapper trang đầu/attempt mới nhất); backend model/effort thực phục vụ ngoài header; danh tính/ý chí người ký lease. A5 là log CI của executor đã đọc lại, không phải CI reviewer tự chạy. Header model là attestation của CLI, không chứng minh riêng backend phục vụ. Không có approval/land authority phát sinh từ verdict này.
