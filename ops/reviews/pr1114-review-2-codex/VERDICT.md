Verdict: approve
Reviewed commit: 51435a44659c4026539497a47ace971a71a64f40

Đã hoàn tất review độc lập: base/head đều 52/52 CA, 80/80 ĐỘT BIẾN, TONG DAT; delta=0. Repro trước/sau chờ: 26/1800 → 0/1800. Quan sát riêng 20/1200 lượt R→Z sau khi `_giet_nhom` trả. Hai mutant bỏ giết vẫn làm a4/a11/b10 đỏ; a9 dùng mặc định vẫn xanh, chậm thêm khoảng 5 s. Suite tăng 15,017 s (4,92%). Ruff và diff-check đạt. Chi tiết lệnh/output bên dưới.

| Finding P0/P1/P2/P3 | Vị trí | Lệnh tái hiện / output | Hướng vá |
|---|---|---|---|
| Không có (0/0/0/0) | — | Các phép đo dương/âm bên dưới | — |

Ngưỡng áp dụng: không còn P0/P1/P2/P3. Review theo chỉ thị trực tiếp cho PR #1114 lượt 2; chỉ ghi sandbox, đột biến trên bản sao.

Bằng chứng được ghi tăng dần tại đây và trong `evidence/`. Chỉ đột biến các bản sao trong `work/`.

Neo ban đầu đã đo (`evidence/initial-git.json`; mọi lệnh Git dưới rc=0):

```text
git -C cay-kho rev-parse HEAD HEAD^{tree}
51435a44659c4026539497a47ace971a71a64f40
7c160ae144195d4f22089ec49d39e45033030381
git -C cay-kho merge-base HEAD refs/remotes/origin/master
3bdd9877cab2543adc413a32a47decbb585ded97
git -C cay-kho diff --name-only 3bdd987 HEAD
ops/cloud_agent_creds_test.py
git -C cay-kho status --porcelain --untracked-files=all
(không output)
git -C cay-kho ls-files --others --ignored --exclude-standard
(không output)
git -C cay-kho diff --check 3bdd987 HEAD
(không output)
```

Đã tạo hai clone riêng bằng `git clone --shared --no-checkout cay-kho work/{head,base}` rồi checkout detached đúng SHA tương ứng. Suite được chạy qua `python3 probes/run_logged.py {head,base} work/{head,base} python3 ops/cloud_agent_creds_test.py`; wrapper đặt `PYTHONDONTWRITEBYTECODE=1`, giữ output/rc/thời gian trong `evidence/{head,base}.{log,json}`.

Kiểm tĩnh và hồi quy stdin đã hoàn tất:

```text
python3 probes/run_logged.py ruff work/head python3 -m ruff check --select F ops/cloud_agent_creds_test.py
rc=0; All checks passed! (ruff 0.17.3; RUFF_NO_CACHE=true)
python3 probes/run_logged.py diff-check cay-kho git diff --check 3bdd987 HEAD
rc=0; không output
```

`evidence/patch-integrity.json`: `DIFF.patch` khớp byte với diff base→head (4160 byte); `DIFF-TU-LUOT1.patch` khớp diff `e101b11..HEAD -- ops/cloud_agent_creds_test.py` (2424 byte). So toàn bộ cây với lượt 1 còn có thay đổi từ master đã merge; không coi chúng là thay đổi ngoài write set của PR (diff với merge-base chỉ có tệp test).

```text
PYTHONDONTWRITEBYTECODE=1 python3 probes/stdin_regression.py
rc=0
ROUND1_STDIN_CODE_IDENTICAL=True
base: rc=3, DO:p3b4_co_blob:node rc=206: b'REVIEW_LIMIT_32767'
      argc=3, units=87617, input_bytes=0
head: rc=0; 3 lần gọi đều argc=2, units=47;
      input_bytes=[87545,161,87545]
```

Probe so AST của `chay_b`, `p3b4_co_blob`, `JS_GIA`, `JS_CHAY` với commit lượt 1, rồi gọi Node thật qua chốt giả giới hạn 32767 đơn vị UTF-16 của `list2cmdline(argv)` (gồm NUL). Phần stdin không hồi quy trong phép đo này. Windows thật/exception WinError 206 thật: **KHÔNG ĐO ĐƯỢC**; không dùng mô phỏng làm bằng chứng chạy Windows. Log: `evidence/stdin-regression.log`, dữ liệu: `evidence/stdin-regression.json`.

Đo giới hạn helper trực tiếp bằng tiến trình thật:

```text
PYTHONDONTWRITEBYTECODE=1 python3 probes/helper_bounds.py
rc=0
{"label":"default_live_30s","seconds":5.001956,"reported_alive":true,"returncode":-9}
{"label":"zero_live_30s","seconds":0.000097,"reported_alive":true,"returncode":-9}
{"label":"default_self_exit_1s","seconds":1.018280,"reported_alive":false,"returncode":0}
```

`evidence/helper-bounds.{log,json}`: tiến trình ngủ 30 s còn được báo sống **trước** khi helper dọn bằng SIGKILL; `cho_chet=0` không chờ. Tiến trình tự thoát sau 1 s được chấp nhận: đây là độ nới thực sự của thời điểm quan sát, không phải bằng chứng rằng mọi tiến trình đã chết ngay tại thời điểm `_giet_nhom` trả về. Lượt probe đầu của reviewer quên truyền `**kw` nên nhánh gắn nhãn zero vẫn dùng mặc định; đã sửa riêng probe và chạy lại, giữ log cũ ở `evidence/helper-bounds-probe-v1.log`, không tính lỗi probe là finding của PR.

Đối chiếu source bằng `rg -n 'sleep|time.monotonic|_song_roi_don|< 20|HAN_VERSION' cay-kho/ops/cloud_agent_creds_test.py`:

- Dòng 58: con/cháu fixture a4/a9 ngủ 60 s; dòng 149: nhóm a11 ngủ 30 s; dòng 233: con b10 ngủ 60 s.
- Dòng 72–75 đo riêng thời gian `nap`; dòng 121 vẫn chốt `k.giay < 20`. Chờ trong helper không cộng vào `k.giay` và không sửa ngưỡng 20 s.
- Dòng 137: a9 gọi `cho_chet=0`; dòng 120/153/236: a4/a11/b10 dùng mặc định. Đây là toàn bộ bốn callsite.

Đã đối chiếu AST base/head (`evidence/ids.json`): `CA 52 DOT_BIEN 80 same_names_order True`. Danh tính và thứ tự ca/đột biến giữ nguyên; số liệu suite hoàn tất ở phần tiếp theo.

Suite toàn phần đã hoàn tất (hai tiến trình khởi chạy song song trên hai clone riêng; stress repro chưa chạy trong khoảng đo này):

| Bản | CA | ĐỘT BIẾN | Tự kiểm | TONG | rc | Thời gian s |
|---|---:|---:|---|---|---:|---:|
| Base `3bdd987` | 52/52 | 80/80 | DAT (4) | DAT | 0 | 305.446757 |
| Head `51435a44` | 52/52 | 80/80 | DAT (4) | DAT | 0 | 320.464175 |
| Delta head − base | 0 | 0 | 0 | giữ DAT | 0 | +15.017418 (4.92%) |

Lệnh qua wrapper đã ghi ở trên; lệnh thực trong mỗi clone là `PYTHONDONTWRITEBYTECODE=1 python3 ops/cloud_agent_creds_test.py`. Output của cả hai:

```text
CA: 52/52 dat
DOT BIEN: 80/80 bi giet dung ly do
TU KIEM PHAN HANG: DAT (4 dot bien)
TONG: DAT
```

Logs/rc/thời gian: `evidence/base.{log,json}`, `evidence/head.{log,json}`. Không có dòng bỏ qua/lỗi. Đây là một cặp thời gian đo, không phải trung vị nhiều lượt. So AST đã xác nhận cùng tập tên và thứ tự 52 ca/80 mutant.

Ma trận đột biến đã hoàn tất:

```sh
python3 probes/make_mutants.py
python3 probes/mutation_matrix.py
```

Cả hai driver rc=0; mã thoát của từng ca nằm trong bảng. Driver gọi `PYTHONDONTWRITEBYTECODE=1 [CAC_MA=work/mutations/<variant>.py] python3 work/head/ops/cloud_agent_creds_test.py --mot-ca <ca>`. Nhánh (c) gọi `work/head/ops/review_a9_default.py`; chỉ bỏ `, cho_chet=0` ở a9. Định nghĩa thay thế nguyên văn ở `evidence/mutant-definitions.json`; output/rc/timing của từng lệnh con ở `evidence/mutation-matrix.json` và `evidence/case-*.log`. Chỉ khảo sát bốn ca có gọi helper; không tuyên bố đã chạy 52 ca cho mỗi mutant.

| Bản | a4 | a11 | a9 | b10 |
|---|---|---|---|---|
| Head nguyên bản | XANH rc=0; 2.382 s | XANH rc=0; 0.969 s | XANH rc=0; 3.286 s | XANH rc=0; 15.282 s |
| (a) chỉ p.kill() | ĐỎ rc=3; 27.368 s | ĐỎ rc=3; 25.554 s | XANH rc=0; 3.277 s | ĐỎ rc=3; 40.302 s |
| (b) bỏ mọi kill | ĐỎ rc=3; 27.365 s | ĐỎ rc=3; 25.604 s | XANH rc=0; 3.274 s | ĐỎ rc=3; 40.310 s |
| (c) a9 dùng mặc định | XANH rc=0; 2.275 s | XANH rc=0; 0.822 s | XANH rc=0; 8.242 s | XANH rc=0; 15.214 s |

Output các ca đỏ (stdout của mọi ca xanh chỉ là newline):

```text
parent_only: DO:a4_qua_han_giet_ca_nhom:nap mất 22.1 s
parent_only: DO:a11_subreaper_va_esrch:sr=True: dừng=False, sống [49], q=None
parent_only: DO:b10_version_treo_giet_ca_nhom:PID [53, 54] của `agy --version`: còn sống [54]
no_kill: DO:a4_qua_han_giet_ca_nhom:nap mất 22.2 s
no_kill: DO:a11_subreaper_va_esrch:sr=True: dừng=False, sống [70], q=None
no_kill: DO:b10_version_treo_giet_ca_nhom:PID [74, 75] của `agy --version`: còn sống [74, 75]
```

Cả hai lỗi giết thật vẫn bị chốt test bắt (rc=3 + `DO:<đúng ca>:`), không phải lỗi vô can rc=4. a4 đỏ ở giới hạn `nap < 20 s` (nap khoảng 22 s); a11 đỏ vì `da=False` và cháu còn sống; b10 đỏ vì PID còn sống. a9 xanh ở (a)/(b) phù hợp mục tiêu của nó: khi chưa dừng nhóm thì log không được báo đã dừng.

(c) a9 xanh nhưng tăng 4.956 s: con/cháu ngủ 60 s nên sau 5 s vẫn còn sống; `cho_chet=0` giữ nguyên thời điểm quan sát và tránh chờ thừa.

Đo riêng nhánh `_SUBREAPER=False`, vì a11 với hai mutant trên dừng ở nhánh True đầu tiên:

```text
PYTHONDONTWRITEBYTECODE=1 python3 probes/fallback_negative.py
rc=0
head: da=False, alive=[], _giet_nhom=0.000399 s, helper=0.000146 s
parent_only: da=False, alive=[14], _giet_nhom=10.008548 s, helper=5.006570 s
no_kill: da=False, alive=[17], _giet_nhom=10.007742 s, helper=5.014404 s
```

Probe dùng `_giet_nhom` của từng bản và chính `_song_roi_don` của head, chỉ cưỡng bức cờ `_SUBREAPER=False`; thu PID còn sống trước bước dọn. Như vậy cửa sổ 5 s cũng không che hai lỗi này ở nhánh fallback mới được vá. Log: `evidence/fallback-negative.{log,json}`.

Tái hiện race và đo cơ chế đã hoàn tất:

```sh
python3 probes/stress.py before 12 150
python3 probes/stress.py after 12 150
PYTHONDONTWRITEBYTECODE=1 python3 probes/mechanism.py
```

Driver stress chạy đúng hai script được cung cấp, không sửa script:

```text
PYTHONDONTWRITEBYTECODE=1 python3 nguon/repro_a11.py <sandbox>/work/head 150
PYTHONDONTWRITEBYTECODE=1 python3 nguon/repro_a11_va.py <sandbox>/work/head 150
```

Mỗi lệnh có 12 bản chạy song song; trước/sau chạy thành hai đợt kế tiếp. Cây runtime giống nhau vì bản vá chỉ sửa test. Cả 24 tiến trình đều rc=0, đủ 150 vòng/tiến trình, không có `rong`.

| Phép đo | Song song × vòng | Còn sống | Thời gian cả đợt |
|---|---:|---:|---:|
| Script trước vá | 12 × 150 | 26/1800 (1.444%) | 45.959133 s |
| Script thêm chờ 5 s | 12 × 150 | 0/1800 | 45.541786 s |

Log từng tiến trình: `evidence/repro-before-00.log` … `-11.log`, tương tự `repro-after-*`; tổng hợp ở `evidence/repro-{before,after}.json`. Mỗi log kết thúc bằng `song_ngay_sau_giet <n> / 150`.

Các dòng `SONG` trước vá có trạng thái khi đọc lần kế tiếp: {'R': 23, 'Z': 3}. Ba dòng Z là chuyển trạng thái giữa `_con_song` và lần đọc phục vụ print; không phải script coi Z là sống. Không nhận lại con số 34/1800 của executor: số độc lập ở đây là 26/1800.

Probe độc lập `probes/mechanism.py` đặt subreaper thật cho worker nhưng cưỡng bức `m._SUBREAPER=False`, chạy 12 worker × 100 vòng. Sau `_giet_nhom`, probe đọc `/proc/<cháu>/stat` liên tục cho tới Z/biến mất, **không gửi thêm tín hiệu trong khoảng quan sát**; chỉ dọn sau khi đã ghi kết quả. Output tổng hợp từ `evidence/mechanism.json`:

```text
total=1200; observed_R_to_Z=20; all_da=False
elapsed_from_return_to_observed_Z: min=0.505733 ms; median=2.550754 ms; max=5.566970 ms
pid=14202, pgrp=14199, ppid=10856: R -> Z, reads=207, elapsed=0.005566970 s
pid=14218, pgrp=14215, ppid=10862: R -> Z, reads=131, elapsed=0.002486316 s
pid=14435, pgrp=14433, ppid=10862: R -> Z, reads=104, elapsed=0.002106530 s
```

Quan sát này chứng minh được `_giet_nhom` đã trả mà cháu còn R, rồi cháu tự chuyển Z trong vài mili giây sau tín hiệu ban đầu. Đọc source bằng `sed -n '47,74p' cay-kho/ops/cloud_agent_creds.py` cho thấy sau `communicate(timeout=HAN_DON)`, nhánh không subreaper trả `False, ra` trước vòng waitpid/kiểm ESRCH. Giải thích ống đóng trước khi cháu thành zombie phù hợp với cả source và phép đo; không có bằng chứng rằng phải chờ trọn 5 s trên đường đúng. 0/1800 chỉ là kết quả hữu hạn của đợt đo, không phải bảo đảm tuyệt đối không còn race.

Kết luận về độ mạnh của a4/b10 và cửa sổ 5 s:

- a4 vẫn kiểm `nap < 20 s`, rc=0, dòng báo đã dừng, đủ PID cha/con/cháu, không PID sống sau thời gian chờ, và log đã che. Hai mutant giết đều đỏ; suite còn giết đúng mutant bỏ timeout. b10 vẫn kiểm đủ hai PID đã chết và tải/thay đúng tệp; hai mutant đều đỏ ở PID sống. Các chốt ngoài thời điểm quan sát không đổi trong diff.
- Mốc quan sát “ngay sau khi trả” được nới thành “sau tối đa khoảng 5 s”; không khẳng định hai mệnh đề này đồng nhất. Probe `default_self_exit_1s` đã đo chính độ nới đó. Các fixture hiện có sống 30/60 s và các lỗi bỏ giết vẫn bị bắt, kể cả nhánh `_SUBREAPER=False`; không phát hiện ca hiện có nào mất chốt yêu cầu cháu chết trong <5 s. a9 cần còn sống được giữ kiểm ngay.
- Thời gian suite đo tăng 15.017418 s, khoảng 4.92%. Đọc `DOT_BIEN` ở test.py:608–609 và 632 cho thấy hai mutant a4 giữ tiến trình sống và mutant b10 chỉ giết cha nay có thể chờ thêm 5 s mỗi ca; mức tăng đo được phù hợp với ba cửa sổ này. Đây là đối chiếu source với tổng thời gian, không phải trace thời gian riêng từng mutant trong full suite.

Kiểm nguyên vẹn cuối:

```text
python3 probes/final_integrity.py
rc=0
HEAD=51435a44659c4026539497a47ace971a71a64f40
tree=7c160ae144195d4f22089ec49d39e45033030381
tracked_files_hashed=10161; changed=[]
status --porcelain --untracked-files=all: rỗng
ls-files --others --ignored --exclude-standard: rỗng
diff --exit-code HEAD: rc=0, rỗng
diff --cached --exit-code HEAD: rc=0, rỗng
diff --check 3bdd987 HEAD: rc=0, rỗng
base/head copy tracked_diff_rc=0
candidate_head_copy_test_identical=True
```

`evidence/final-integrity.{log,json}` lưu lệnh và output chi tiết. Snapshot đầu/cuối cùng hash chứng minh không có delta quan sát được ở các mốc; không dùng nó để khẳng định toàn bộ lịch sử ghi giữa hai mốc.

Giới hạn: log CI `41289534297`, số đo gốc 34/1800 và Windows thật/WinError 206 thật: **KHÔNG ĐO ĐƯỢC** trong lượt này. Đã thay bằng các phép đo độc lập nêu trên trong phạm vi yêu cầu. Không có finding P0/P1/P2/P3. Verdict chỉ áp dụng exact commit ở dòng 2; không cấp quyền merge/land.
