verdict: approve
reviewed_sha: 36190a35db647e65d7c6fd4b684d5178dfd82544
spec_sha256: ce14c65668f2076795ed20955d263653e927b0aeddea7d5fd6445f41eb563c7d
reviewer_provider: openai_codex
reviewer_model: gpt-6.1-sol
execution_surface: codex_cli
transport: machine

Tree: `934cfd403dfb4284535a8cf3eee0f7a476c497ba`. CLI v0.160.1, session `01a11761-1a26-7bb3-8c2c-a9d06c335d47`, reasoning xhigh theo header lưu ở `evidence/session-header.txt`. Executor theo lease: `anthropic_claude` / `claude_code` / `claude-opus-5-5`, effort high tự khai. Phiên review độc lập với executor; chỉ đo trên clone/scratch. Header là khai báo của CLI, không chứng minh backend/effort thực của mọi request. Băm và bytes của `cay-kho/`, `kho.git/` khớp snapshot đầu/cuối. Không thao tác GitHub/push/CI/LIVE.

**Quyết định và hai trục.** Áp ngưỡng PROMPT: **0 lớp P1 · 0 lớp P2 · 0 lớp P3 còn mở**. Hai lớp lượt 1 đều **ĐÃ ĐÓNG** trong phạm vi r3; không có lớp **VÁ SINH LỖI MỚI** hoặc **TÁI PHÁT** đo được. Approval này là kết quả review head cục bộ trước push theo S4; A5 trên exact head mới còn `not_run`, cổng land `human_audited` giữ nguyên.

| Trục | Kết quả |
|---|---|
| Spec acceptance | M1–M10 đúng; A1, A2(a)–(e), A3, A6 có bằng chứng dương; A4 delta bằng 0. Suite launcher/đường nhanh nguyên bản đỏ nền được giữ nguyên là failed, không nâng thành pass tuyệt đối. A5 exact head mới chưa đo theo trình tự S4. |
| Standards | Mọi biểu thức trần của đường chạy bộ hiện tại đã kiểm kê và đột biến; không có mutant trần sống trên head mới trong tập đo. M10 bắt sai trần ở cả nhánh nền mô phỏng; không thấy rò con/tạm hoặc thay env/cwd/global patches. Không phát hiện lỗi mới trong diff +9/−1 của lượt 2. |

**Bảng lớp — giữ slug và lịch sử.**

| Slug | Hạng nguồn → còn mở | Nguồn và mọi biểu hiện trong phạm vi | Trạng thái lượt 2, phép đo | Hướng vá / phép đóng |
|---|---|---|---|---|
| `tran-runtime-khong-duoc-ca-kiem-khoa` | P2 → không | Lượt 1 `f9c8dbd53a21d4048d26572f3147893f6c57e95b`, p643 cũ `.claude/dev/ci_dang_ky_test.py:2162`; default `:924`, wrapper `:964`, `communicate` `:936` cùng tệp. Chốt mới `:2162`–`:2171`. | **ĐÃ ĐÓNG**. Hai mutant default/wrapper 4500 vẫn sống trên lượt 1: rc=0, 1025/1025; trên head mới mỗi cái rc=1, 1024/1025, p643 `LỌT`. Clamp tại communicate cũng rc=1 cùng ca. Probe literal communicate cho helper=false ở POSIX và nt mô phỏng. | Nhóm HINT P2 được áp đúng byte các dòng thêm; M10 nằm trong p643 cũ, không thêm ca. Giữ ca truyền trần và các ca kill-tree có sẵn. Không cần hunk mới. |
| `ty-le-cham-khong-khop-so-do` | P3 → không | `SPEC-r2.md:42`/`:45` ghi 25–40% / 1,40 / ~6%; Issue body r1 (dòng 20 của `evidence/inputs/issue-body-original.md`) lặp dải 25–40%; nguồn hiệu lực mới `SPEC.md:46`, `SPEC.md:49`, `SPEC.md:53`–`:55`; comment #705 `6042998795` neo Spec r3/hash và erratum. | **ĐÃ ĐÓNG** bằng erratum r3 có thẩm quyền. `python3.12 -B goi/static_audit.py`, rc=0: dải 22,1519–42,2319%, max làm tròn 1,42; 3645×1,42=5175,9≈5176 s; biên 4,3297%≈4,3%; sức chịu chậm 48,1481%≈48,1%. | Không sửa âm thầm r2. Issue body r1 còn nguyên câu cũ; comment cấp quyền r3 nói rõ lớp P3 đã xử lý bằng erratum. Chỉ nhận tài liệu r3 được neo làm giải thích hiện hành, không khai body r1 đã được sửa. Chú thích W1 đã đúng từ r2. |

**Mọi đường trần tới runtime.** `python3.12 -B goi/static_audit.py` rc=0; rg runtime/consumer rc=0; AST lưu đủ 12 mục ở `evidence/timeout-paths.json`. Quét 128 Python sống thấy 31 literal 90/90.0, không literal 4500 còn dùng làm trần registry; kết quả và dòng nguồn ở `ast-old-numbers.json` / `rg-old-numbers-live.log`.

Chuỗi chạy thật: W1:2226 (lambda đủ/nhẹ) hoặc seam mặc định `chay_moi` W1:967 → `_chay_that` W1:963–964 → default `gioi_han` W1:924 lấy hằng W1:700 → `p.communicate(timeout=gioi_han)` W1:936. Ca fixture env W1:1979 gọi trực tiếp `_chay_co_lap` nhưng dùng cùng default, không tạo một giá trị trần riêng. W1:2168 là đường gọi mới của M10. Không thấy consumer trần sống khác ngoài W1.

W1:1777/1788/1796/1799/1801 truyền 60/2/30/30/"x" để thử đồng thời, kill-tree và lỗi kiểu; đó là deadline fixture, không phải trần bộ sản xuất. W1:950 dùng `GIAY_CHO_CAY_DUNG=10` trong cleanup, đi với deadline dừng ở W1:943/951; đây là trần dừng riêng, không đổi thành 5400. Probe timeout tổng hợp đã đo lần communicate thứ nhất 5400, lần cleanup 10, kết quả có lỗi `hết giờ 5400 giây`. Các ca p637 thật vẫn ĐỎ đúng trong A1.

Đột biến tại từng biểu thức trần hiện có, reset từ exact HEAD trước mỗi lần:

| Điểm | Thay đổi | Lệnh / rc / bằng chứng |
|---|---|---|
| Hằng W1:700 (A2a) | 5400 → 4500 | `python3.12 .claude/dev/ci_dang_ky_test.py`, rc=1, p643 `LỌT`, 1024/1025, TỔNG ĐỎ. |
| Default W1:924 (A2e) | `gioi_han=GIAY_TOI_DA_MOT_BO` → `gioi_han=4500` | Cùng lệnh, rc=1, p643 `LỌT`, 1024/1025. |
| Wrapper W1:964 (A2e) | thêm đối số `gioi_han=4500` | Cùng lệnh, rc=1, p643 `LỌT`, 1024/1025. |
| Đối số communicate W1:936 | `gioi_han` → `min(gioi_han,4500)` | Cùng lệnh, rc=1, p643 `LỌT`, 1024/1025; giữ các timeout fixture ngắn để đo được toàn suite. |
| Cùng điểm communicate | `gioi_han` → literal 4500 | `python3.12 -B $R/goi/target_probe.py false`, rc=0 của harness xác minh kỳ vọng âm; helper nguyên văn=false trên cả posix/nt mô phỏng. **Không chạy toàn suite với literal này**, vì nó bỏ các deadline 2/30/60 s của fixture thật. |

Mutant default/wrapper trên head lượt 1 được chạy lại độc lập trên clone: cùng lệnh registry, rc=0 và 1025/1025; không dựa vào lời khai lượt trước. Các probe `*-platforms` có rc=0 vì đã xác nhận helper trả **false**, không phải registry mutant xanh. Lệnh, source delta của từng mutant và rc riêng ở `evidence/*-4500.patch`, `*.json`, `*.log`.

**Mock, nền và tài nguyên.** `python3.12 -B goi/runtime_probe.py` rc=0 và cùng script bằng Python3.11 rc=0. Mỗi lượt chạy helper M10 nguyên văn 20 lần trên POSIX native, 20 lần với seam liveness không /proc, 20 lần với nhánh không-POSIX mô phỏng. Mỗi lần đúng một communicate với timeout=5400, thư mục tạo bởi wrapper đã bị xoá; không tạo child, env/cwd cha giữ nguyên và `Popen`/`_pid_song` được trả lại đúng đối tượng gốc. Hai chế độ đủ/nhẹ của wrapper thật đều truyền 5400. Default/wrapper/clamp 4500 khiến helper=false ở cả hai nhánh nền mô phỏng.

`Popen` giả giúp đo tham số, `_pid_song` giả bỏ kiểm liveness vốn phụ thuộc nền; không có nhánh skip trả true. Trần được đo trước nhánh POSIX; mock không biến trần 4500 thành 5400. Phạm vi này không chứng minh taskkill/killpg hay deadline tường 90 phút trên máy thật. Windows và POSIX không /proc vật lý: **KHÔNG ĐO ĐƯỢC**.

**M1–M10 và write set.**

| Mục | Bằng chứng trên ứng viên |
|---|---|
| M1/M8 | W1:700 = int 5400; W1:697–699 ghi đúng 22–42%, ~4% trên 1,42 và các số đo/lý do. |
| M2 | `bam_gate_registry` thật tính `9dd2c23db45fd97c4ce44a98ff0abe74e21b4b2c64a97dab318addb92d3458d9`, khớp W1:742. So dict job nền/head bỏ riêng timeout: giống nhau. |
| M3 | W1:2170–2171 khoá 5400 và `<60×105`; ca float W1:2099 tạo 105.0; ca YAML thô timeout-trung W1:2119 tạo khoá 105 trùng và bị actionlint bắt trong A1. |
| M4/M5/M7 | W2:845 và W3:21 = int 105; chú thích W2:836–837 nêu #705/105; không đổi khoá YAML khác của gate-registry. |
| M6 | AST KHUNG_JOB W4:2199 so nền chỉ đổi ô timeout gate-registry 90→105; A6 y13 mutant đỏ đúng khoá. |
| M9 | Float suy từ timeout ci.yml thật; A6 105 và 120 phân biệt kiểu độc lập với lệch giá trị. |
| M10 | W1:2162–2171 gọi wrapper thật với child giả, đo timeout tới communicate; A2e có răng, N không đổi. |

`git diff --name-status origin/origin-master...36190a35db647e65d7c6fd4b684d5178dfd82544`, rc=0: đúng W1–W4. `git diff --numstat` cùng range, rc=0: W1 +20/−7, W2 +3/−1, W3 +1/−1, W4 +1/−1 ⇒ **4 tệp, +25/−10**, dưới S5. Lượt 2 so `f9c8dbd53a21d4048d26572f3147893f6c57e95b` chỉ W1 +9/−1, đúng nhóm HINT P2. `git show -s` rc=0 neo cha là lượt 1; master `ab457c651eb4428705f0492163080b661c858b72`; merge-base `8c98afacb9285aa71e5200739236284f7a190d4f`; `git merge-tree --write-tree` rc=0, tree `2d66d5b091a3e4b59eb1b587cb33e620217f2f98`, không conflict. Đây là phép đo trên clone, không merge vào kho thật.

**Nghiệm thu — lệnh và rc thật.** Driver `python3.12 -B goi/review_harness.py suites` dựng hai vế trong một setup/lệnh điều phối, cùng công cụ/env và argv mỗi family. Rc từng subprocess dưới đây không bị rc driver che.

| Mục | Lệnh | Rc / output thật |
|---|---|---|
| A1 | `python3.12 .claude/dev/ci_dang_ky_test.py` trên base `7e5958e440285c8d63d2f710cf97ba20b85f2926`, lượt 1 và head mới | 0/0/0; cả ba `ĐĂNG KÝ: 23/23`, `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT`. Tập tên/đáp án base/head giống nhau. |
| A2a/A2e | Registry sau ba mutant hằng/default/wrapper 4500 | Mỗi cái rc=1, 1024/1025, p643 `LỌT`; lời khai executor **khớp**. |
| A2b | Registry, riêng timeout ci.yml 105→90 | rc=1; `gate-registry đổi (băm b42a413f852e0852f0e59ef8acaf6757a771c2e55e296714426a73e7e308ebc9)`, TỔNG ĐỎ. |
| A2c | Registry, riêng dot-bien-du 105→90 | rc=1; `job: timeout-minutes lệch gate-registry`, TỔNG ĐỎ. |
| A2d | Registry, hằng 6300 (=60×105) | rc=1, p643 `LỌT`, 1024/1025. Bổ sung sửa equality kỳ vọng lên 6300 để bỏ che lấp: vẫn rc=1, chứng minh nhánh `<` có răng. |
| A3 actionlint | `actionlint -oneline .github/workflows/ci.yml` và `...ci-dot-bien-du.yml` trên base/lượt1/head | Cả 6 lượt rc=0, stdout rỗng. |
| A3 Ruff F | `ruff check --no-cache --select F --output-format json .claude/dev/ci_dang_ky_test.py ops/ci_duong_nhanh_test.py` trên base/lượt1/head | rc=0/0/0, tập lỗi `[]/[]/[]`, delta 0 với cả hai mốc như executor khai. Đây là bare F lint; Ruff pin/probe contract riêng nằm trong A1. |
| A4 launcher | `python3.12 .claude/dev/launcher_test.py` base/head | rc=1/1; cùng 179/180 đã chạy qua, tổng 189, bỏ 9, hỏng 1; cùng tập skip và lỗi r351. Delta 0, **failed nền**. |
| A4 t152 | `python3.12 .claude/dev/launcher_test.py --lap-ca t152_hook_cai_dat_va_khop_al_ver_ci --lan 1` base/head | rc=0/0, 1/1 qua, 0 bỏ qua, 0 hỏng. |
| A4 lease | `python3.12 ops/lease_publish_test.py` base/head | rc=0/0, `lease_publish: 198/198 đạt; đã chạy=198, bỏ qua=0`; delta 0. |
| A4 đường nhanh | `python3.12 ops/ci_duong_nhanh_test.py` base/head | rc=1/1, `CA: 103/104 dat · 0 do · 1 hong`, `DOT BIEN: 378/383 bi giet dung ly do`, `TONG: DO`; cùng ca socket và 5 mutant control không xanh, delta 0, **failed nền**. |
| Bổ sung ca socket | `python3.12 -B goi/socket_fixture_probe.py` | Driver rc=0; ca t20zo bằng inode socket thật rc=0/0; 5/5 mutant `GIET`, rc=0/0. Fixture có chỉnh riêng, không khai suite nguyên bản 104/104·383/383 tại chỗ. |
| A6 M6 | `python3.12 ops/ci_duong_nhanh_test.py --mot-ca y13_khoa_topology_cua_ci_yml_ngoai_than_run` sau ci.yml về 90 | rc=3, `khac ['timeout-minutes']`, đúng lý do. |
| A6 M9, 105 | `python3.12 -c ...phan_chung()` sau nới riêng so kiểu của timeout/env thành `==` | rc=1, `p661-M5-du-timeout-float-do: LỌT`, 1024/1025. |
| A6 M9, 120 | Đổi cả hai timeout lên 120, chạy phan_chung thật rồi chọn đúng ca M9 | Control rc=0, `ĐỎ đúng`; nới so kiểu rc=1, `LỌT`. Chỉ xác minh ca M9, không khai toàn suite giả định 120 xanh. |
| A5 exact head mới | Không chạy / không dispatch / không rerun CI | **not_run**. Head mới chưa push; S4 yêu cầu review sạch trước push. Không gán CI của head f9c8dbd cho head 36190a3. |

`python3.12 -B goi/compare_suites.py`, rc=0, kiểm cả rc, tập tên, tập skip/fail và summary, không chỉ tổng số. Launcher và lease test trùng byte base/head; đường nhanh có đúng thay đổi M6.

**Standards về cỡ job.** `python3.12 -B goi/historical_ci_projection.py`, rc=0, tính lại dữ liệu CI **offline của lượt 1**, không đọc lại GitHub và không nhận là A5 mới: N=2; bộ dài 4582.033 s, đủ, rc=0; setup 36.349 s, chờ worker 465.931 s, teardown 0.676 s. Chiếu thay riêng bộ dài bằng 5400 cho 98.383 phút, còn 6.617 phút so trần 105. W1 runtime/W2/W3 và các bộ thật không đổi giữa lượt1/lượt2 ngoài ca đo mới. Không thấy mâu thuẫn cỡ trần; phép chiếu phụ thuộc setup/hàng chờ/các bộ khác giữ như run cũ, không bảo đảm runner chậm nhất.

**Preflight, hiện vật và giới hạn đo.** `sha256sum PROMPT.md SPEC.md lease-g3.yaml`, rc=0, khớp đầu/cuối:

```text
6849dd4a749d8615a7067e5cdfb73ea9549a147f71b536ed8b8f35a0714044e0  PROMPT.md
ce14c65668f2076795ed20955d263653e927b0aeddea7d5fd6445f41eb563c7d  SPEC.md
deeac218ec76019de24faf1b07fd07e6e37faf51aed03a2c83fa2c52ad01d6a8  lease-g3.yaml
```

`git -C cay-kho rev-parse HEAD HEAD^{tree}` rc=0, đúng head/tree nêu đầu tệp; `git -C cay-kho status --short` rc=0, stdout rỗng ở hai mốc. Snapshot bytes kể cả ignored/untracked và Git metadata bằng nhau, chỉ chứng minh không có delta quan sát ở hai mốc. Spec blob thật tại `36473cdeb9782356fd0a498d516f8e1347934785:ops/specs/CI-REGISTRY-NANG-TRAN-BO-DAY-DU-r3.md` khớp SHA-256; write-set hash tính lại `ad1358ad5099e3cb3ddee76189b1d1292fbd4ebfa875e57be113606e9ab71bb0`; comment cấp quyền `6042998795` khớp lease_id/spec hash. Lease executor r3/g3 từ 07-10 17:00Z đến 08-10 17:00Z; trường SHA parent được lease giải nghĩa rõ là start/baseline, verdict neo exact head mới.

Các phép git đầu dùng ref `origin-master` trong working clone trả rc=128 (merge-tree rc=1), vì clone ánh xạ ref thành `origin/origin-master`; đã đo lại thành công, giữ cả log lỗi rig và log `retry-*`. Không coi lỗi rig là lỗi PR. Môi trường: Python 3.12.3 và probe thêm Python 3.11.15; PyYAML6.0.1; Ruff0.15.8 (khác pin CI0.15.15), actionlint1.7.7, shellcheck0.9.0. Ba vế dùng cùng công cụ có sẵn; không cài dependency.

**KHÔNG ĐO ĐƯỢC / không chạy:** A5 trên head mới và thời gian bộ dài trên runner đó; mọi gate merge/land trên exact SHA mới; Windows thật/POSIX không /proc thật và kill/taskkill trên các nền ấy; suite launcher tuyệt đối xanh (9 skip, r351 đỏ nền); suite đường nhanh nguyên bản tuyệt đối xanh (socket bị chặn); deadline tường thật 5400 s và sức chịu runner chậm nhất; tái benchmark 4604/4586 s, các thời gian vượt 4500 bị cắt; backend model/effort và danh tính/ý chí người ký lease. Không dùng kết quả chưa đo làm pass.

`EVIDENCE.zip` chứa harness lượt 2, input đóng băng, source liên quan, source snapshots, raw logs/rc, bảng delta/đột biến và manifest SHA-256; `EVIDENCE-README.md` ghi cách tái hiện và cách đọc rc của probe âm. Không có lớp mở nên không phát sinh HINT.patch.
