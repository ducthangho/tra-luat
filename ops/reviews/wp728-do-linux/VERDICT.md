9fddb1d19e8e5b753bb687673846d484fb710182

# wp728 r2 g1 — biên bản đo độc lập Linux

Lease: `wp728-r2-g1-codex-reviewer-20261016`; nguồn authority cục bộ là
`ops/leases/wp728-r2-g1-codex-reviewer-20261016.yaml`, comment cấp quyền do người giao việc cung cấp:
https://github.com/ducthangho/tra-luat/issues/728#issuecomment-6204784204.
Không truy cập mạng để xác minh comment. Đã đọc trọn spec r2 trước phép đo.

Đây là đo/audit, không sửa mã. Đích nội dung là SHA dòng 1; checkout chứa rig được bàn giao tại
`1e9d6993736d85897cd979808eaa77fe8a3e17ef`, tree `d9727454efdfaf12afdbc30a1d30b78144ef293d`.
Tree của reviewed_sha: `a4844cb99cc4ee8e2b4ce827f2babe00cb175301`.
Theo chỉ thị bàn giao, HEAD chứa rig là hậu duệ; mọi luật (a)(b)(c) và xuất blob đều dùng reviewed_sha,
không dùng HEAD. Các ghi chú dựng thử của phiên điều phối không được dùng làm bằng chứng.

## Môi trường và phạm vi

```bash
R=/home/user/rv/wp728
E=/home/user/rv/wp728-env
O=/home/user/rv/wp728-ngoai/l1
S="$O/xuat"
RS=9fddb1d19e8e5b753bb687673846d484fb710182
RIG="$R/ops/reviews/wp728-do-linux/rig"
export PATH="$E/pwsh:$E/shim:$PATH" TMPDIR="$O/tmp" HOME="$O/home" PYTHONDONTWRITEBYTECODE=1
export GIT_OPTIONAL_LOCKS=0
```

- `pwsh` resolve: `/home/user/rv/wp728-env/pwsh/pwsh`; phiên bản `7.4.6`; `type -a` chỉ có đường này.
- `python`: `/home/user/rv/wp728-env/shim/python` → `/usr/bin/python3.13`, `Python 3.13.16`.
- `python3`: `/usr/bin/python3`, `Python 3.13.16`; `uname -r`: `6.18.44-fc-v114`.
- Tarball: 71645796 byte; sha256 `6f6015203c47806c5cc444c19d8ed019695e610fbd948154264bf9ca8e157561`.
  Đây là hash bản đã đến, chưa đối chiếu giá trị nhà phát hành công bố.
- Spec tự băm: `daecd8b216663d8a275700adb7f572afeb020a3e34d976460fb5c4f55dc06a40`, khớp lease và giá trị được giao.
- Bắt đầu preflight: `2026-10-16T00:14:19Z`. Thực thi lần lượt REPLAY mục 0–5;
  thêm một lượt M1 với trace thụ động để đếm ca, thêm đọc/đối chiếu đầu ra và snapshot.
  Không soạn hoặc chạy kịch bản điều khiển tiến trình mới; chỉ sinh bản sao wrapper bằng mutate.py đã lưu.
- Mọi tệp do reviewer ghi ở O. Không fetch/push, không sửa R, không mạng, không LIVE/Drive,
  không gọi `nlm` thật hay credential thật. Không chạy doctor với credential thật trong lượt offline này.

## Danh tính và assurance

Reviewer: `openai_codex`, execution_surface `codex_cli`, transport `machine`.
Run launcher `a989021232c449c7bd053f10af59e861`; session CLI
`01a1420e-1dd5-7261-8eb3-a4535d49dba0`. Header CLI tự công bố `gpt-6.1-sol`, effort `xhigh`:
```text
Reading additional input from stdin...
OpenAI Codex v0.162.1
--------
workdir: /home/user/rv
model: gpt-6.1-sol
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR]
reasoning effort: xhigh
reasoning summaries: none
session id: 01a1420e-1dd5-7261-8eb3-a4535d49dba0
--------
```
Nguồn: `O/run/a9890212/stderr.log` và bản chép header `O/model-header.txt`;
metadata `O/run/a9890212/run.json` ghi cùng provider/surface/transport, còn `dang_chay` lúc đọc.
Header/cấu hình không chứng minh họ model thật phục vụ mọi request. Executor WP710 khai Claude theo lease,
chưa có phép đo độc lập danh tính Executor trong lượt này. Mức bằng chứng họ model thực phục vụ cả hai bên:
`khong_do_duoc` tại thời điểm biên bản; chưa có audit danh tính đã hoàn tất được bàn giao.
Không khai `do_may` hoặc tự nhận `cross_approved`. Muốn dùng kết quả để đóng hồ sơ cần
audit đúng điều kiện spec (kể cả audit actor cho cả hai bên nếu dùng `khai_co_audit`, yếu hơn `do_may`),
hoặc đường `human_audited` độc lập neo exact SHA; receipt cuối phải qua bộ kiểm canonical rc 0.
Reviewer không tạo receipt thay launcher/điều phối và chưa chạy validator trên receipt cuối chưa có.

## N0 — ĐẠT

Lệnh: REPLAY mục 0–1; bản lệnh có instrumentation ghi rc tại `O/00-01-preflight.sh`.
Các lệnh chính và mã thoát:

```bash
stat -c %s "$E/dl/powershell-7.4.6-linux-x64.tar.gz"                         # rc 0
sha256sum "$E/dl/powershell-7.4.6-linux-x64.tar.gz"                         # rc 0
command -v pwsh; type -a pwsh                                             # mỗi lệnh rc 0
pwsh -NoProfile -c '$PSVersionTable.PSVersion.ToString()'                   # rc 0
command -v python; python --version; python3 --version; uname -r          # mỗi lệnh hoàn tất, có đầu ra bên dưới
git -C "$R" rev-parse --is-shallow-repository                             # rc 0, false; đo trước (a)
git -C "$R" merge-base --is-ancestor 8b59185975a938504de5963d2310e574dd4858b2 "$RS" # rc 0
git -C "$R" rev-parse "$RS:scripts/nlm-credential-refresh.ps1"             # rc 0
git -C "$R" rev-parse "$RS:scripts/nlm-credential-refresh.Tests.ps1"       # rc 0
git -C "$R" cat-file blob "$RS:scripts/nlm-credential-refresh.ps1" > "$S/nlm-credential-refresh.ps1" # rc 0
git -C "$R" cat-file blob "$RS:scripts/nlm-credential-refresh.Tests.ps1" > "$S/nlm-credential-refresh.Tests.ps1" # rc 0
sha256sum "$S/nlm-credential-refresh.ps1" "$S/nlm-credential-refresh.Tests.ps1" # rc 0
sha256sum "$R/ops/specs/wp728-do-linux-doc-lap-wp710-r2.md"                # rc 0, hash khớp
```

Đầu ra nguyên văn `O/n0.out` (gồm rc thật của các bước):
```text
2026-10-16T00:14:19Z
71645796
stat rc=0
6f6015203c47806c5cc444c19d8ed019695e610fbd948154264bf9ca8e157561  /home/user/rv/wp728-env/dl/powershell-7.4.6-linux-x64.tar.gz
tarball sha256 rc=0
/home/user/rv/wp728-env/pwsh/pwsh
pwsh resolve rc=0
pwsh is /home/user/rv/wp728-env/pwsh/pwsh
pwsh type rc=0
7.4.6
pwsh version rc=0
/home/user/rv/wp728-env/shim/python
Python 3.13.16
Python 3.13.16
6.18.44-fc-v114
environment rc=0
/usr/bin/python3.13
/usr/bin/python3
git status rc=0
git identity rc=0
git diff rc=0
git diff cached rc=0
snapshot sha256 rc=0
false
shallow rc=0
a rc=0
24240a31be4d51332f748d3fdadf3307cb6f1a88
b rc=0
4dc5994c363245219419fc0e2a20350761d6f7f1
c rc=0
export wrapper rc=0
export tests rc=0
33d32769897f97644985def693a6c54c70d2dc4048aed242b557cf4df1e8da5d  /home/user/rv/wp728-ngoai/l1/xuat/nlm-credential-refresh.ps1
7f6e56362e2bea7a2033a8995aa779f12e0141ca4e2c950401a962863a46f1a8  /home/user/rv/wp728-ngoai/l1/xuat/nlm-credential-refresh.Tests.ps1
export sha256 rc=0
```
Hash tự đo tại snapshot đầu, rc 0 (`O/r-before-hashes.txt`):
```text
daecd8b216663d8a275700adb7f572afeb020a3e34d976460fb5c4f55dc06a40  /home/user/rv/wp728/ops/specs/wp728-do-linux-doc-lap-wp710-r2.md
```
Hai tệp xuất cùng thư mục S, giữ đúng tên; M1/M2 và đầu vào mutate đều dùng chính các byte này.
Không có điều kiện N0 KHÔNG ĐO ĐƯỢC nên được chuyển qua M1. Không chạy các phản chứng N0 bằng cách sửa R/môi trường.

## N1 — ĐẠT

Lệnh M1 đúng REPLAY mục 3:

```bash
pwsh -NoProfile -File "$S/nlm-credential-refresh.Tests.ps1" > "$O/m1.out" 2> "$O/m1.err"
```

Đầu ra và rc nguyên văn:
```text
passed=34 failed=0
m1 rc=0
```
Không lấy 34 từ lời khai Executor. Chạy thêm chính suite đã băm với trace thụ động, không đổi byte nguồn:

```bash
pwsh -NoProfile -c 'Set-PSDebug -Trace 1; & "/home/user/rv/wp728-ngoai/l1/xuat/nlm-credential-refresh.Tests.ps1"' > "$O/m1-trace.out" 2> "$O/m1-trace.err"
python3 "$O/count-m1.py" > "$O/m1-count.txt"
```

Đếm các dòng thực thi `DEBUG: <dòng>+ >>>> $cases++` trong đầu ra trace, không đếm số vị trí trong nguồn.
Đầu ra nguyên văn (rc của trace và bộ đếm đều 0):
```text
m1 trace rc=0
m1 count rc=0
TRACE_CASE_INCREMENT_TOTAL=34
TRACE_CASE_INCREMENT_BY_LINE=256:7, 281:1, 290:1, 307:1, 323:1, 350:1, 360:1, 366:1, 376:1, 398:1, 416:1, 426:1, 450:1, 486:1, 508:1, 537:1, 551:1, 615:1, 645:1, 689:1, 735:1, 795:2, 884:1, 946:1, 988:1, 1021:1, 1080:1
TRACE_SUMMARIES=[('34', '0')]
M1_ORIGINAL_SUMMARY=passed=34 failed=0
TRACE_COUNT_MATCH=YES
```
Đếm được 34 lần tăng tại 27 vị trí: dòng 256 thực thi 7 lần, dòng 795 thực thi 2 lần,
25 vị trí còn lại mỗi vị trí 1 lần. Cả lượt gốc lẫn trace có `failed=0`; stderr đều 0 byte.
Theo đơn vị ca của suite: passed=34, failed=0, not_run trong phạm vi Linux=0.
Suite không in trường skipped; reviewer ghi riêng 4 khối chỉ Windows không chạy trên Linux
(các vị trí tăng tại dòng 265, 1152, 1183, 1323 có guard `$IsWindows`, không xuất hiện trong trace).

## N2 — ĐẠT

Lệnh tự kiểm REPLAY mục 2, rc tiến trình python3 = 0 (ghi bằng PIPESTATUS, không lấy rc của tee):

```bash
python3 "$RIG/zombie_rig.py" selftest | tee "$O/rig-selftest.txt"
```
```text
DAT   1 zombie cu con lai, con moi nhat da reap => dem 1
DAT   2 pid trung starttime khac o mau => 0 zombie fixture, khong DO_DUOC
DAT   3 hai chu ky lien cung pid starttime khac => hai ban ghi dung hai chu ky
DAT   4 bo lo mot the he => KHONG_DO_DUOC
DAT   5 khe tep rong giua hai lan ghi => bo qua, khong dem la reap
DAT   6 poll tre max_gap > 250 ms => KHONG_DO_DUOC
DAT   7 khong thu duoc danh tinh => KHONG_DO_DUOC
DAT   8 EACCES => KHONG_DO_DUOC
selftest 8/8
rig selftest rc=0
```
Lệnh M2/M2' và N4 theo REPLAY mục 4; bản chạy `O/04-m2.sh` chỉ thêm ghi rc mutate/cmp.
Nguồn rig luôn là bản đã lưu trong R; nguồn wrapper/tests từ S. Hai lượt mỗi loại là hai lượt bắt buộc của N4,
không phải lượt chạy lại do lỗi. Không lượt nào báo `KHONG_DO_DUOC`; số retry rig = 0.
```bash
source /home/user/rv/wp728-ngoai/l1/replay-env.sh
for L in 1 2; do
  python3 "$RIG/zombie_rig.py" run --wrapper "$S/nlm-credential-refresh.ps1" \
      --tests "$S/nlm-credential-refresh.Tests.ps1" --max-cycles 5 --interval 10 \
      > "$O/m2-nen-$L.jsonl"; echo "m2 nen $L rc=$?"
  python3 "$RIG/mutate.py" "$S/nlm-credential-refresh.ps1" "$O/dot-bien-$L.ps1" | tee "$O/mutate-$L.txt"
  echo "mutate $L rc=${PIPESTATUS[0]}"
  python3 "$RIG/zombie_rig.py" run --wrapper "$O/dot-bien-$L.ps1" \
      --tests "$S/nlm-credential-refresh.Tests.ps1" --max-cycles 5 --interval 10 \
      > "$O/m2-dotbien-$L.jsonl"; echo "m2 dotbien $L rc=$?"
done
cmp "$O/dot-bien-1.ps1" "$O/dot-bien-2.ps1" && echo MUTATE_TAT_DINH
echo "cmp rc=$?"
```
Đầu ra rc/đột biến/cmp nguyên văn `O/m2.rc`:
```text
m2 nen 1 rc=0
khop=1 sha256_goc=33d32769897f97644985def693a6c54c70d2dc4048aed242b557cf4df1e8da5d sha256_dot_bien=ec08d75b5e9c3ae9690ec824d4999d06837efd5a530ff88f9d1580a3b3d2d33e
mutate 1 rc=0
m2 dotbien 1 rc=0
m2 nen 2 rc=0
khop=1 sha256_goc=33d32769897f97644985def693a6c54c70d2dc4048aed242b557cf4df1e8da5d sha256_dot_bien=ec08d75b5e9c3ae9690ec824d4999d06837efd5a530ff88f9d1580a3b3d2d33e
mutate 2 rc=0
m2 dotbien 2 rc=0
MUTATE_TAT_DINH
cmp rc=0
```
Bốn dòng `tong_ket` nguyên văn; mỗi tên tệp là đầu ra riêng của một lệnh run:

`O/m2-nen-1.jsonl`:

```json
{"loai": "tong_ket", "trang_thai": "DO_DUOC", "ly_do": [], "zombie_fixture_theo_khoang": [0, 0, 0, 0], "z_con_cua_wrapper_theo_khoang": [0, 0, 0, 0], "max_gap_ms": 85.5, "so_poll": 904, "nhieu": 846, "the_he": [{"pid": 27, "starttime": 184158, "chu_ky": 0, "trang_thai_luc_thu": "S"}, {"pid": 32, "starttime": 185242, "chu_ky": 1, "trang_thai_luc_thu": "S"}, {"pid": 37, "starttime": 186311, "chu_ky": 2, "trang_thai_luc_thu": "S"}, {"pid": 44, "starttime": 187383, "chu_ky": 3, "trang_thai_luc_thu": "R"}, {"pid": 50, "starttime": 188451, "chu_ky": 4, "trang_thai_luc_thu": "S"}], "wrapper_rc": 0, "so_staged": 5, "max_cycles": 5, "interval_s": 10, "sha256_wrapper": "33d32769897f97644985def693a6c54c70d2dc4048aed242b557cf4df1e8da5d", "sha256_tests": "7f6e56362e2bea7a2033a8995aa779f12e0141ca4e2c950401a962863a46f1a8", "sha256_fake": "a894f5af5a369f1d6b0e7d90a15e17e641dff07530d9a58b79b0f2a592cbf3c2"}
```

`O/m2-nen-2.jsonl`:

```json
{"loai": "tong_ket", "trang_thai": "DO_DUOC", "ly_do": [], "zombie_fixture_theo_khoang": [0, 0, 0, 0], "z_con_cua_wrapper_theo_khoang": [0, 0, 0, 0], "max_gap_ms": 52.9, "so_poll": 905, "nhieu": 846, "the_he": [{"pid": 125, "starttime": 193234, "chu_ky": 0, "trang_thai_luc_thu": "S"}, {"pid": 130, "starttime": 194320, "chu_ky": 1, "trang_thai_luc_thu": "S"}, {"pid": 135, "starttime": 195389, "chu_ky": 2, "trang_thai_luc_thu": "S"}, {"pid": 141, "starttime": 196459, "chu_ky": 3, "trang_thai_luc_thu": "R"}, {"pid": 146, "starttime": 197529, "chu_ky": 4, "trang_thai_luc_thu": "R"}], "wrapper_rc": 0, "so_staged": 5, "max_cycles": 5, "interval_s": 10, "sha256_wrapper": "33d32769897f97644985def693a6c54c70d2dc4048aed242b557cf4df1e8da5d", "sha256_tests": "7f6e56362e2bea7a2033a8995aa779f12e0141ca4e2c950401a962863a46f1a8", "sha256_fake": "a894f5af5a369f1d6b0e7d90a15e17e641dff07530d9a58b79b0f2a592cbf3c2"}
```

`O/m2-dotbien-1.jsonl`:

```json
{"loai": "tong_ket", "trang_thai": "DO_DUOC", "ly_do": [], "zombie_fixture_theo_khoang": [1, 2, 3, 4], "z_con_cua_wrapper_theo_khoang": [1, 2, 3, 4], "max_gap_ms": 51.3, "so_poll": 901, "nhieu": 33, "the_he": [{"pid": 78, "starttime": 188697, "chu_ky": 0, "trang_thai_luc_thu": "S"}, {"pid": 83, "starttime": 189779, "chu_ky": 1, "trang_thai_luc_thu": "S"}, {"pid": 88, "starttime": 190847, "chu_ky": 2, "trang_thai_luc_thu": "S"}, {"pid": 94, "starttime": 191914, "chu_ky": 3, "trang_thai_luc_thu": "S"}, {"pid": 99, "starttime": 192981, "chu_ky": 4, "trang_thai_luc_thu": "R"}], "wrapper_rc": 0, "so_staged": 5, "max_cycles": 5, "interval_s": 10, "sha256_wrapper": "ec08d75b5e9c3ae9690ec824d4999d06837efd5a530ff88f9d1580a3b3d2d33e", "sha256_tests": "7f6e56362e2bea7a2033a8995aa779f12e0141ca4e2c950401a962863a46f1a8", "sha256_fake": "a894f5af5a369f1d6b0e7d90a15e17e641dff07530d9a58b79b0f2a592cbf3c2"}
```

`O/m2-dotbien-2.jsonl`:

```json
{"loai": "tong_ket", "trang_thai": "DO_DUOC", "ly_do": [], "zombie_fixture_theo_khoang": [1, 2, 3, 4], "z_con_cua_wrapper_theo_khoang": [1, 2, 3, 4], "max_gap_ms": 59.8, "so_poll": 902, "nhieu": 33, "the_he": [{"pid": 174, "starttime": 197771, "chu_ky": 0, "trang_thai_luc_thu": "S"}, {"pid": 179, "starttime": 198853, "chu_ky": 1, "trang_thai_luc_thu": "S"}, {"pid": 184, "starttime": 199922, "chu_ky": 2, "trang_thai_luc_thu": "S"}, {"pid": 190, "starttime": 200994, "chu_ky": 3, "trang_thai_luc_thu": "S"}, {"pid": 196, "starttime": 202061, "chu_ky": 4, "trang_thai_luc_thu": "R"}], "wrapper_rc": 0, "so_staged": 5, "max_cycles": 5, "interval_s": 10, "sha256_wrapper": "ec08d75b5e9c3ae9690ec824d4999d06837efd5a530ff88f9d1580a3b3d2d33e", "sha256_tests": "7f6e56362e2bea7a2033a8995aa779f12e0141ca4e2c950401a962863a46f1a8", "sha256_fake": "a894f5af5a369f1d6b0e7d90a15e17e641dff07530d9a58b79b0f2a592cbf3c2"}
```

Mỗi lượt đủ 5 thế hệ, chu kỳ 0–4, mỗi chu kỳ đúng một cặp và starttime tăng;
4 mẫu khoảng nghỉ đều wrapper còn sống, t=1,0 s sau staged, không fixture còn sống tại mẫu.
Nền có `[0,0,0,0]`; đột biến tích lũy `[1,2,3,4]`. Không đọc số zombie để bỏ qua nhãn toàn lượt.
Đối chiếu đầu ra bổ sung bằng python3 đọc JSON, rc 0 (`O/m2-validation.txt`):
```text
m2-nen-1.jsonl: DO_DUOC; 5/5 generations; 4/4 valid samples; zombies=[0, 0, 0, 0]; max_gap_ms=85.5; sample_t_s=[1.0, 1.0, 1.0, 1.0]
m2-nen-2.jsonl: DO_DUOC; 5/5 generations; 4/4 valid samples; zombies=[0, 0, 0, 0]; max_gap_ms=52.9; sample_t_s=[1.0, 1.0, 1.0, 1.0]
m2-dotbien-1.jsonl: DO_DUOC; 5/5 generations; 4/4 valid samples; zombies=[1, 2, 3, 4]; max_gap_ms=51.3; sample_t_s=[1.0, 1.0, 1.0, 1.0]
m2-dotbien-2.jsonl: DO_DUOC; 5/5 generations; 4/4 valid samples; zombies=[1, 2, 3, 4]; max_gap_ms=59.8; sample_t_s=[1.0, 1.0, 1.0, 1.0]
N2_VALIDATION=PASS; N4_REPLAY_SAME_CONCLUSIONS=YES; RIG_RETRIES=0
m2 validation rc=0
```
## N3 — ĐẠT (chỉ ghi nhận, không đóng/mở lớp)

Lệnh REPLAY mục 5 nguyên bản về kịch bản; `O/05-m3.sh` thêm ghi PID, thời điểm và rc:
```bash
source /home/user/rv/wp728-ngoai/l1/replay-env.sh
date -u +%Y-%m-%dT%H:%M:%SZ
sleep 1200 & T=$!
printf '%s\n' "$T" > "$O/m3-target-pid.txt"
T=$T pwsh -NoProfile -c '$sw=[Diagnostics.Stopwatch]::StartNew(); Start-Sleep -Seconds 260;
  $s=(Get-Process -Id ([int]$env:T)).StartTime.ToUniversalTime();
  "{0} {1}" -f $s.Ticks, $sw.Elapsed.TotalSeconds' > "$O/m3-a.txt"
echo "m3 A rc=$?"
T=$T pwsh -NoProfile -c '(Get-Process -Id ([int]$env:T)).StartTime.ToUniversalTime().Ticks' > "$O/m3-b.txt"
echo "m3 B rc=$?"
awk '{print $22}' "/proc/$T/stat" > "$O/m3-proc-starttime.txt"
echo "m3 proc rc=$?"
kill "$T"
echo "m3 kill rc=$?"
python3 - "$O" <<'PY'
import sys; o = sys.argv[1]
a_ticks, a_age = open(f"{o}/m3-a.txt").read().split()
b_ticks = open(f"{o}/m3-b.txt").read().split()[0]
print(f"lech_s = (A - B)/1e7 = {(int(a_ticks) - int(b_ticks)) / 1e7:.3f} ; tuoi_pwsh_A_s = {float(a_age):.1f}")
PY
echo "m3 calculation rc=$?"
date -u +%Y-%m-%dT%H:%M:%SZ
```
Đầu ra nguyên văn `O/m3.out`:
```text
2026-10-16T00:26:28Z
m3 A rc=0
m3 B rc=0
m3 proc rc=0
m3 kill rc=0
lech_s = (A - B)/1e7 = -0.000 ; tuoi_pwsh_A_s = 260.1
m3 calculation rc=0
2026-10-16T00:30:49Z
```
Cùng PID đích: `5` (một biến T, truyền cho cả A và B, đọc /proc trước khi kill).
Dữ liệu thô nguyên văn:

`O/m3-a.txt` (UTC DateTime ticks của PID đích; tuổi Stopwatch của pwsh A, giây):

```text
639277071887058915 260.1020167
```

`O/m3-b.txt` (UTC DateTime ticks của cùng PID):

```text
639277071887063380
```

`O/m3-proc-starttime.txt` (trường 22 /proc của cùng PID, jiffies từ boot):

```text
203415
```

Công thức: `(StartTime_A - StartTime_B).Ticks / 10^7 = (639277071887058915 - 639277071887063380) / 10^7 = -0.0004465 giây`.
Đơn vị DateTime: 100 ns/tick. Tuổi pwsh A đo bằng `Stopwatch.Elapsed.TotalSeconds` là `260.1020167` giây (≥250 s),
đồng hồ đơn điệu. Nguồn StartTime: `System.Diagnostics.Process.StartTime` của .NET trên Linux,
trường 22 `/proc/<PID>/stat` (jiffies từ boot) cộng mốc boot runtime tự tính; sau đó chuyển UTC.
Đây là hai pwsh đọc cùng một PID; không trừ starttime của hai PID khác nhau.
Đây là số đo cloud Linux này; các lời khai WSL 2,9 s/130 s và 7,0 s/256 s chưa được tái đo,
không suy Linux chứng minh WSL. `O/m3.err` có 0 byte.

## N4 — KHÔNG ĐO ĐƯỢC (tổng thể; phần chạy lại ĐẠT)

Hai lượt bắt buộc từ chính rig lưu trong kho cho cùng kết luận:
nền đều `DO_DUOC + [0,0,0,0]`; đột biến đều `DO_DUOC + [1,2,3,4]`.
Hai lệnh mutate đều khớp đúng 1 dòng, rc 0; sha256 đột biến trùng. Đầu ra nguyên văn:
```text
khop=1 sha256_goc=33d32769897f97644985def693a6c54c70d2dc4048aed242b557cf4df1e8da5d sha256_dot_bien=ec08d75b5e9c3ae9690ec824d4999d06837efd5a530ff88f9d1580a3b3d2d33e
khop=1 sha256_goc=33d32769897f97644985def693a6c54c70d2dc4048aed242b557cf4df1e8da5d sha256_dot_bien=ec08d75b5e9c3ae9690ec824d4999d06837efd5a530ff88f9d1580a3b3d2d33e
MUTATE_TAT_DINH
cmp rc=0
```
Lệnh cmp đã chạy trong mục 4:

```bash
cmp "$O/dot-bien-1.ps1" "$O/dot-bien-2.ps1" && echo MUTATE_TAT_DINH
```

Spec N4 còn yêu cầu `SHA256SUMS.txt` cuối bao trọn mọi tệp dưới
`ops/reviews/wp728-do-linux/` trừ chính manifest, được lập SAU khi VERDICT.md và run.json đã chốt.
R được bàn giao chỉ có `.gitattributes` và `rig/`; chưa có manifest/hồ sơ cuối cho phép đo này.
Không có bộ hồ sơ cuối bổ sung được bàn giao trong lượt.

Lệnh kiểm thực chạy:

```bash
sha256sum -c "$R/ops/reviews/wp728-do-linux/SHA256SUMS.txt"
```

Đầu ra nguyên văn và rc:
```text
sha256sum: /home/user/rv/wp728/ops/reviews/wp728-do-linux/SHA256SUMS.txt: No such file or directory
n4 checksum rc=1
```
Rc 1 ở đây là thiếu tệp đầu vào, chưa chứng minh checksum nào sai. Không có dữ liệu để kiểm cả hash
lẫn tính đầy đủ tập thành viên. Vì vậy không nâng phần replay xanh thành N4 tổng thể ĐẠT.
Đây là checkpoint đóng hồ sơ của phiên điều phối, không phải finding lỗi trong mã WP710.
Điều phối cần chép verdict nguyên byte, chốt run.json, lập manifest đầy đủ rồi kiểm rc 0 cùng tập thành viên
trong một snapshot cuối; không cần chạy lại M1/M2 chỉ vì thiếu bước đóng gói này.

## Finding và tính toàn vẹn checkout

Không có finding P0–P3 đủ bằng chứng chạy được trong phạm vi mã đích, rig và REPLAY của lượt này.
Thiếu bằng chứng nghiệm thu N4 được giữ thành checkpoint, không gán thành lỗi reaper hay suy một phép đo đỏ.
Đã đọc/phản biện `zombie_rig.py`, `mutate.py` và mã đích đã xuất; không viết bản vá hay kịch bản tiến trình mới.

Snapshot đầu/cuối: HEAD/tree, Git status gồm tracked/untracked/ignored, diff/index, hash index cùng
spec/lease/ba tệp rig. Các lệnh và rc đối chiếu nằm trong `O/final-checks.out`:
```text
2026-10-16T00:31:04Z
git status rc=0
git identity rc=0
symbolic-ref rc=1 (1 = detached)
reviewed_sha ancestor of rig HEAD rc=0
git diff rc=0
git diff cached rc=0
snapshot sha256 rc=0
snapshot status cmp rc=0
snapshot identity cmp rc=0
snapshot diff cmp rc=0
snapshot index-diff cmp rc=0
snapshot hashes cmp rc=0
0 /home/user/rv/wp728-ngoai/l1/r-before-status.txt
0 /home/user/rv/wp728-ngoai/l1/r-after-status.txt
0 /home/user/rv/wp728-ngoai/l1/r-before-diff.txt
0 /home/user/rv/wp728-ngoai/l1/r-after-diff.txt
0 /home/user/rv/wp728-ngoai/l1/r-before-index-diff.txt
0 /home/user/rv/wp728-ngoai/l1/r-after-index-diff.txt
0 total
1e9d6993736d85897cd979808eaa77fe8a3e17ef
d9727454efdfaf12afdbc30a1d30b78144ef293d
a4844cb99cc4ee8e2b4ce827f2babe00cb175301
33d32769897f97644985def693a6c54c70d2dc4048aed242b557cf4df1e8da5d  /home/user/rv/wp728-ngoai/l1/xuat/nlm-credential-refresh.ps1
7f6e56362e2bea7a2033a8995aa779f12e0141ca4e2c950401a962863a46f1a8  /home/user/rv/wp728-ngoai/l1/xuat/nlm-credential-refresh.Tests.ps1
exported source final sha256 rc=0
ec08d75b5e9c3ae9690ec824d4999d06837efd5a530ff88f9d1580a3b3d2d33e  /home/user/rv/wp728-ngoai/l1/dot-bien-1.ps1
ec08d75b5e9c3ae9690ec824d4999d06837efd5a530ff88f9d1580a3b3d2d33e  /home/user/rv/wp728-ngoai/l1/dot-bien-2.ps1
mutants final sha256 rc=0
```
Bằng chứng snapshot chỉ chứng minh không có delta quan sát được ở hai mốc, không chứng minh toàn lịch sử
ghi/rồi hoàn nguyên. Sandbox thực tế là workspace-write; R được đối xử read-only bằng hành vi,
không tự khai có cơ chế mount R read-only. Không snapshot hoặc review nội dung checkout khác.

parity 101/168: KHÔNG TÁI LẬP ĐƯỢC từ kho; không đo

Phần chưa đo: WSL máy chủ kho, nlm/trình duyệt thật, LIVE/Drive, giá trị hash tarball nhà phát hành,
credential Codex thật, họ model thực phục vụ từng request và receipt assurance cuối đã validate.
Không dùng các lời khai hoặc phép dựng thử trước của điều phối làm bằng chứng độc lập.

N0, N1, N2 đều ĐẠT; N3 đã ghi nhận đủ số/công thức/đơn vị/đồng hồ/tuổi A.
N4 phần tái lập đã ĐẠT nhưng tổng thể KHÔNG ĐO ĐƯỢC vì chưa kiểm manifest/tập thành viên hồ sơ cuối.
Theo luật đóng lớp của spec, giữ lớp mở đúng phần còn thiếu ấy.

Hoàn tất biên bản lúc 2026-10-16T00:31:04.796443+00:00.

KET_LUAN_LOP linux-subreaper-khong-thu-hoi-zombie: mo
VERDICT: changes_requested
