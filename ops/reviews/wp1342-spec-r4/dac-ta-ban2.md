tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174-WINDOWS-BACKEND r4 — vòng đời tiến trình trong Job Object, Windows native, đứng riêng, KHÔNG pipe (bậc r1d-a1), chưa nối vào runtime

- packet_id: WP1174-WINDOWS-BACKEND; revision: 4;

| trường | giá trị |
|---|---|
| `packet_issue` | #1342 |
| `nguon_cap_viec` | Lộ trình bậc ở §1 đặc tả r1. Chủ kho 17-11-2026: seed + BootId vào r3 (land `aeb5cae`, `ops/land/pr1390-wp1342-land-evidence.yaml`, `landed: true`), tiến trình + probe sang r1d. Chủ kho 18-11-2026 (phiên điều phối #1206): "Làm tiếp #1342 r1d"; tách r1d thành r1d-a (tiến trình) / r1d-b (probe); sau review lượt 1, tách tiếp r1d-a thành **a1** (vòng đời trong job, revision này) và **a2** (transport hai pipe, revision sau). §9. |
| `review_class` | `sensitive` (runtime trạng thái WP1174) |
| `base` | `e2c3b82f818bd1739d31261e8129d3ef44915acf` lúc soạn (đo §0 lúc 2026-11-18T17:2xZ). Lease ghi OID base thật lúc cấp; người cấp đo lại §0 trên base ấy trước khi công bố băm (L5). |

**Đánh số:** `revision: 4` (ADR-0063, số nguyên). Đây là bậc **r1d-a1** của lộ trình; r1d-a2 và r1d-b là các revision sau.

## 0. Hiện trạng (đo trên `e2c3b82`; số dòng tính từ `def`, không gồm decorator)

- `_1174_process` 4260–4308 (Linux, có pipe) — mẫu hợp đồng cho a2, KHÔNG đổi ở r4. Lưu ý chính xác: `os.killpg(child.pid, SIGKILL)` vô điều kiện chỉ chạy khi đã vào `try` cleanup nội bộ (sau `Popen`, sau `ExitStack`, sau khởi tạo `streams`); `on_bytes` ở `finally` ngoài.
- `_1174Error(ValueError)` 3670; `_1174_require`.
- `_1174_win_api` 6419–6435: tạo `WinDLL("kernel32", use_last_error=True)` mới mỗi lần gọi, bind argtypes/restype, trả `(c, w, k)`. r1–r3 khác đứng riêng ở 6406–6742 (`_1174_win_path` … `_1174_win_boot_id`).
- CPython 3.13 `subprocess.py` nhánh Windows (reviewer lượt 1 đọc, dòng ~1555–1578): `creationflags` chuyển nguyên cho `_winapi.CreateProcess`; giữ process handle (`Popen._handle`, chi tiết triển khai CPython), ĐÓNG primary thread handle, KHÔNG gọi `ResumeThread`. Vì vậy muốn resume phải tìm lại luồng (Toolhelp). r4 phụ thuộc `Popen._handle` — ghi rõ và kiểm có mặt (M2).
- `.claude/dev/launcher.py` `_job_windows` 905–973 (`CreateJobObjectW`, lớp 9, `KILL_ON_JOB_CLOSE` `0x2000`, gán SAU khi con đã chạy — KHE tự khai) và `_pid_trong_job` 976–1003 (lớp 3). r4 đóng khe này cho primitive mới, không sửa launcher.
- Test: `WP1174_BOTH` 12421 (12 ID); `_new1342` 17879, `_additive1342` 17896, `_wired1342` 17920, `_native1342` **18159** (in marker `WP1342_NATIVE_V1` ở 18165 sau khi thân ca trả về), `_additive1342r2` 18178; đăng ký ca ở 18170/18171, 18365/18366, 18553/18554. `MUTANTS` 3592 và các `MUTANTS.update`.
- Kích thước tiền nhiệm (numstat): r1 +428, r2 +293, r3 +300.

## 1. Phạm vi r4 (r1d-a1)

Thêm, ĐỨNG RIÊNG (không hàm hiện có nào gọi tới): bindings job/thread; ba hàm thuần nhỏ; một hàm kiểm job rỗng; `_1174_win_spawn_job` chạy MỘT lệnh trong job từ trạng thái treo, chờ tiến trình đầu thoát có hạn, rồi thu hồi cả job và xác nhận job rỗng. stdin/stdout/stderr của con đều `DEVNULL` — KHÔNG pipe. Không sửa thân định nghĩa nào đang có.

## 2. `write_set` và `ngoai_pham_vi`

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
```

Ngoài phạm vi:
- Không sửa thân hàm/khối nào đang có (kể cả `_1174_process`, `_1174_win_*` r1–r3, helper test `_new1342` `_additive1342` `_wired1342` `_additive1342r2` `_native1342`). Không đổi `MUTANTS` đang có; không runner mới; không CI Windows.
- **Để r1d-a2 (transport):** đọc hai pipe, hạn mức byte chung và cơ chế huỷ I/O có thời hạn (finding P1 "hai reader" lượt 1), `on_bytes` và ma trận callback, trần byte, `stdin` bytes, ca thuần từ chối đối số kiểu `_1174_process` (M3 cũ), ca P1–P4 cũ, đột biến (d)(f)(g) cũ, CRLF/NUL, deadline sau output một phần.
- **Để r1d-b:** probe.
- Không nối dây. Không API không tài liệu (`NtResumeProcess`…), không `pywin32`, không đồ giả Win32 (Q11 r1). Không giới hạn CPU/bộ nhớ/số tiến trình.
- Phạm vi bảo đảm: tiến trình thuộc cây kế thừa job (con và hậu duệ do nó tạo). Tiến trình do dịch vụ ngoài job tạo thay mặt con (COM/WMI/Task Scheduler, `CREATE_BREAKAWAY` qua dịch vụ) nằm NGOÀI bảo đảm của Job Object và ngoài r4. Giả định: không tiến trình ngoài nào có quyền can thiệp vào con (chèn luồng, `ResumeThread` hộ) trong khoảng tạo→resume.

## 3. Hằng số (danh sách CHO PHÉP, một giá trị mỗi hằng)

| hằng | giá trị | ý nghĩa |
|---|---|---|
| `_1174_WIN_JOB_LIMIT` | `0x2000` | `LimitFlags` của job = CHỈ `KILL_ON_JOB_CLOSE`; không `BREAKAWAY_OK` (0x800), không `SILENT_BREAKAWAY_OK` (0x1000) |
| `_1174_WIN_SPAWN_FLAGS` | `0x204` | `creationflags` của con = CHỈ `CREATE_SUSPENDED` (0x4) \| `CREATE_NEW_PROCESS_GROUP` (0x200) |
| `_1174_WIN_RESUME_OK` | `1` | giá trị DUY NHẤT nhận từ `ResumeThread` (đếm treo trước thao tác) |

## 4. `muc_tieu`

| # | mục tiêu |
|---|---|
| M1 | `_1174_win_api_job()`: gọi `_1174_win_api()`, bind trên CÙNG `kernel32` đúng tập sau (không hơn): `CreateJobObjectW`, `SetInformationJobObject`, `AssignProcessToJobObject`, `TerminateJobObject`, `QueryInformationJobObject`, `IsProcessInJob`, `CreateToolhelp32Snapshot`, `Thread32First`, `Thread32Next`, `OpenThread`, `GetProcessIdOfThread`, `ResumeThread`, `GetHandleInformation`; argtypes/restype tường minh (HANDLE trả về là `c_void_p`, DWORD là `w.DWORD`). Khai cấu trúc `JOBOBJECT_BASIC_LIMIT_INFORMATION`, `IO_COUNTERS`, `JOBOBJECT_EXTENDED_LIMIT_INFORMATION`, `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION`, `THREADENTRY32` theo layout Win64 có tài liệu. Trả `(c, w, k, cấu_trúc)`. |
| M2 | Ba hàm THUẦN (chạy mọi nền, không ctypes): (a) `_1174_win_pick_thread(entries, pid)`: `entries` là iterable `(owner_pid, tid)`; trả tid khi có ĐÚNG MỘT mục `owner_pid == pid`; 0 hoặc ≥2 ⇒ `_1174Error("suspended start")`. (b) `_1174_win_resume_ok(count)`: không lỗi khi `type(count) is int and count == _1174_WIN_RESUME_OK`; mọi giá trị khác (0, 2, `0xFFFFFFFF`, `True`) ⇒ `_1174Error("suspended start")`. (c) `_1174_win_cleanup(steps)`: chạy TỪNG callable trong `steps` theo thứ tự, mỗi cái trong `try` riêng; bước lỗi không chặn bước sau; trả danh sách ngoại lệ theo thứ tự. |
| M3 | `_1174_win_job_empty(k, s, job, wait_s)`: lặp tới `wait_s` giây, mỗi lần `QueryInformationJobObject(job, 1, …)`. Query trả FALSE ⇒ `_1174Error("job query")` NGAY (không bao giờ đọc buffer khi query lỗi, không coi là rỗng). Query thành công và `ActiveProcesses == 0` ⇒ trả. Hết `wait_s` mà còn > 0 ⇒ `_1174Error("job not empty")`. |
| M4 | `_1174_win_spawn_job(argv, *, cwd, deadline, env=None, truoc_gan=None, between=None)` → `int` (mã thoát tiến trình đầu). Thứ tự: **(0)** kiểm đối số: `argv` là list khác rỗng toàn `str`; `deadline` là `int`/`float` (không `bool`) và `> time.monotonic()`; `cwd` là `str`; `truoc_gan`, `between` là `None` hoặc callable; vi phạm ⇒ `_1174Error("spawn arguments")`. Sau đó mới `os.name == "nt"` ("native Windows required"). **(1)** `CreateJobObjectW(None, None)` (handle KHÔNG kế thừa); NULL ⇒ lỗi; ĐĂNG KÝ ngay bước dọn `CloseHandle(job)`. **(2)** `SetInformationJobObject(job, 9, …)` với `LimitFlags == _1174_WIN_JOB_LIMIT`; FALSE ⇒ lỗi. **(3)** `Popen(argv, cwd=, env=, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, close_fds=True, creationflags=_1174_WIN_SPAWN_FLAGS)`; thiếu `Popen._handle` ⇒ lỗi "spawn handle"; ĐĂNG KÝ ngay bước dọn TRƯỚC-GÁN: `proc.kill()` rồi `proc.wait(5)` (giết bằng chính process handle gốc, không theo PID). **(4)** `truoc_gan(proc)` nếu có. **(5)** `AssignProcessToJobObject(job, proc._handle)`; FALSE ⇒ `_1174Error("job assignment")`. TRUE ⇒ đánh dấu ĐÃ GÁN (bước dọn job ở (8) có hiệu lực; bước dọn trước-gán vẫn giữ làm dự phòng). **(6)** `between(job)` nếu có. **(7)** `CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD=0x4, 0)`; `INVALID_HANDLE_VALUE` ⇒ "thread snapshot"; ĐĂNG KÝ `CloseHandle(snap)`. Duyệt `Thread32First/Next`; kết thúc hợp lệ CHỈ khi Next trả FALSE với `GetLastError == ERROR_NO_MORE_FILES (18)`, mã khác ⇒ "thread snapshot". Chọn tid bằng `_1174_win_pick_thread`. `OpenThread(THREAD_SUSPEND_RESUME 0x2 \| THREAD_QUERY_LIMITED_INFORMATION 0x800, False, tid)`; NULL ⇒ "suspended start"; ĐĂNG KÝ `CloseHandle(th)`. Đòi `GetProcessIdOfThread(th) == proc.pid` (chống TID cũ) ⇒ khác ⇒ "suspended start". `ResumeThread(th)` qua `_1174_win_resume_ok`. **(8)** chờ tiến trình đầu: `proc.wait(timeout=deadline - time.monotonic())`; `TimeoutExpired` ⇒ `_1174Error("lifecycle deadline")`. **(9)** `finally`: chạy `_1174_win_cleanup` với các bước đã đăng ký, theo thứ tự: nếu ĐÃ GÁN thì `TerminateJobObject(job, 1)` (FALSE ⇒ ghi lỗi "job terminate") rồi `_1174_win_job_empty(…, 5)`; bước trước-gán (kill+wait); đóng thread; đóng snapshot; `proc.wait(5)`; `CloseHandle(job)`. Ưu tiên lỗi: có lỗi gốc ⇒ ném lỗi gốc, gắn các lỗi dọn làm `__context__`/ghi chú; không có lỗi gốc mà có lỗi dọn ⇒ ném lỗi dọn ĐẦU TIÊN. Chỉ trả mã thoát khi KHÔNG có lỗi nào, tức đã xác nhận job rỗng. |
| M5 | Ca THUẦN (mọi nền) ID `wp1342_pure_spawn_*`: **S1** `_1174_WIN_JOB_LIMIT == 0x2000` và `_1174_WIN_SPAWN_FLAGS == 0x204` và `_1174_WIN_RESUME_OK == 1` (từng hằng một assertion riêng). **S2** `_1174_win_pick_thread`: `[]`, `[(9,1)]`, `[(7,1),(7,2)]` ⇒ lỗi; `[(9,1),(7,5),(8,6)]` với pid 7 ⇒ 5. **S3** `_1174_win_resume_ok`: 1 qua; 0, 2, `0xFFFFFFFF`, `True` ⇒ lỗi. **S4** `_1174_win_cleanup`: bước 1 ném, bước 2 vẫn chạy (ghi cờ), trả đúng 1 lỗi theo thứ tự. **S5** `_1174_win_spawn_job` từ chối `argv=[]`, `["x", 1]`, `"x"`, `deadline` đã qua, `deadline=True`, `cwd=None`, `between=1` với "spawn arguments"; trên nền khác Windows đối số hợp lệ ⇒ "native Windows required". Không thêm vào `WP1174_REQUIRED`/`WP1174_BOTH`. |
| M6 | Ca NATIVE (Windows; nền khác in `BỎ QUA <lý do>`, không tính đạt), qua `_native1342`, ID `wp1342_native_job_*`. Lệnh con `sys.executable -B -c …`. Mọi pid fixture được BẮT TAY: tiến trình tự ghi `pid` + nonce ngẫu nhiên vào tệp tạm khi vào thân; ca mở handle `SYNCHRONIZE \| PROCESS_QUERY_LIMITED_INFORMATION` ngay sau khi đọc tệp, xác nhận đối tượng vẫn sống và chưa signaled lúc mở, rồi chỉ kiểm vòng đời trên HANDLE đó (không mở lại theo pid). Mỗi ca có đường tự dọn (`TerminateProcess` trên handle giữ) khi đột biến sống sót. Tập API Win32 riêng của PHÍA TEST (bind trong `packet_loop_test.py`, không thuộc allowlist M1): `OpenProcess`, `DuplicateHandle`, `GetCurrentProcess`, `WaitForSingleObject`, `TerminateProcess`, `CloseHandle`, cùng bindings M1 cho job đối chứng J4(ii)/J12. **J1 (đường thuận)** con ghi tệp đánh dấu rồi thoát `rc=7` ⇒ hàm trả `7`, tệp có. **J2 (hạn)** con `sleep(30)`, deadline +0,5 s ⇒ "lifecycle deadline" trong < 5 s; handle con giữ (lấy qua bắt tay) signaled. **J3 (mồ côi)** con sinh cháu `DETACHED_PROCESS (0x8)`; cháu bắt tay rồi `sleep(30)`; con chờ bắt tay của cháu rồi thoát `rc=0`; hàm trả `0`; sau đó handle cháu signaled. **J4 (breakaway tường minh)** con thử sinh cháu với `CREATE_BREAKAWAY_FROM_JOB (0x01000000)`, ghi `winerror` ra tệp. Đạt ⇔ lời sinh bị từ chối với `winerror ∈ {5}` (danh sách cho phép; mã khác ⇒ `KHÔNG ĐO`, ghi mã thật). Đối chứng trong cùng ca: (i) cùng argv KHÔNG cờ breakaway sinh được; (ii) một job đối chứng do CA dựng bằng bindings M1 với `LimitFlags = 0x2000\|0x800`: cùng lời sinh breakaway THÀNH CÔNG (chứng minh job ngoài không che phản chứng); đối chứng (ii) không đạt ⇒ `KHÔNG ĐO`. **J5 (breakaway ngầm)** con sinh cháu bình thường, gọi `IsProcessInJob(cháu, NULL)` qua ctypes và ghi kết quả, rồi thoát. Đạt ⇔ cháu ở trong job VÀ handle cháu signaled sau khi hàm trả. **J6 (treo trước gán)** `between(job)`: tệp đánh dấu do con ghi ở dòng đầu CHƯA tồn tại; sau khi hàm trả, tệp CÓ. **J7 (handle kế thừa)** `between(job)`: `GetHandleInformation(job)` thành công và KHÔNG có `HANDLE_FLAG_INHERIT (0x1)`. **J8 (lỗi trước gán)** `truoc_gan` ném `RuntimeError`; hàm ném lại lỗi ấy; con (handle lấy trong `truoc_gan` bằng `DuplicateHandle` của `proc._handle`) signaled trong ≤ 5 s. **J9 (lỗi sau gán)** `between` lấy bản sao handle con và handle job (`DuplicateHandle`) rồi ném `RuntimeError` (con đã gán, vẫn treo); hàm ném lại lỗi ấy; sau đó handle con signaled và `ActiveProcesses == 0` đọc qua bản sao handle job (query phải thành công). **J10 (cha chết)** ca sinh một tiến trình python TRỢ GIÚP gọi `_1174_win_spawn_job` với con sinh cháu, cả hai bắt tay rồi `sleep(30)`; ca `TerminateProcess` tiến trình trợ giúp (không `finally` nào chạy); handle con và cháu signaled trong ≤ 5 s (nhờ `KILL_ON_JOB_CLOSE` khi OS đóng handle job). **J11 (query lỗi)** `_1174_win_job_empty` với handle KHÔNG phải job (handle tệp tạm mở bằng `CreateFileW` của r1) ⇒ "job query"; với job rỗng hợp lệ do ca tạo ⇒ trả. **J12 (job lồng, năng lực có điều kiện)** tiến trình trợ giúp tự gán vào job ngoài (`LimitFlags = 0x2000`, không breakaway) rồi gọi `_1174_win_spawn_job` như J3. Ghi lại nhánh đã xảy ra: hoặc thành công và cháu signaled, hoặc "job assignment" và con signaled. Nhánh nào khác (trả thành công mà cháu sống, hoặc lỗi khác) ⇒ ĐỎ. Không khẳng định nhánh nào là bảo đảm. |
| M7 | Đột biến qua driver NGOÀI kho (khuôn r1–r3; mỗi cặp (tìm, thay) khớp đúng một chỗ; bản sao tạm; ca đích + đối chứng khoẻ; lỗi import/fixture hoặc hết watchdog ngoài ca ⇒ `KHÔNG ĐO`). Mỗi đột biến có DẤU HIỆU ĐỎ riêng (ID ca + chuỗi assertion), bảng §4b. |

## 4b. Đường vào, chốt, ca, đột biến (mỗi đường một chốt riêng)

| # | đường để tiến trình sống ngoài vòng đời lời gọi / kết quả sai | chốt | ca đích (dấu hiệu đỏ) | đột biến |
|---|---|---|---|---|
| 1 | con thoát, cháu mồ côi còn sống | `TerminateJobObject` ở (9) | J3: hàm ném "job not empty" | **a1** xoá lời gọi `TerminateJobObject` |
| 2 | tiến trình Python chết trước `finally` | `KILL_ON_JOB_CLOSE` | J10: "con/cháu sống sau khi cha chết" | **a2** `_1174_WIN_JOB_LIMIT = 0` |
| 3 | query lỗi đọc thành rỗng | M3 ném "job query" | J11: "query lỗi được nhận là rỗng" | **a3** thay nhánh query-FALSE bằng `return` |
| 4 | cháu sinh trong khe "chạy trước, gán sau" | gán TRƯỚC resume | J6: "tệp đánh dấu đã có lúc between" | **b** dời khối (7) lên trước (5), kèm `time.sleep(0.5)` sau resume |
| 5 | con không treo khi tạo | `CREATE_SUSPENDED` trong `_1174_WIN_SPAWN_FLAGS` | J1: hàm ném "suspended start" (ResumeThread=0); S1 vế cờ | **c** `_1174_WIN_SPAWN_FLAGS = 0x200` |
| 6 | cháu xin breakaway | không `0x800` | J4: "breakaway thành công" | **e1** `_1174_WIN_JOB_LIMIT = 0x2800` |
| 7 | cháu breakaway ngầm | không `0x1000` | J5: "cháu ngoài job" | **e2** `_1174_WIN_JOB_LIMIT = 0x3000` |
| 8 | handle job kế thừa sang con | security attributes `None` | J7: "job handle kế thừa được" | **h** chèn `SetHandleInformation(job, 1, 1)` ngay sau tạo job (gọi qua `c.windll.kernel32` trong dòng thay) |
| 9 | lỗi sau `Popen` trước gán để con treo sống | bước dọn trước-gán (kill+wait trên handle gốc) | J8: "con treo còn sống" | **k1** xoá bước dọn trước-gán khỏi danh sách đăng ký |
| 10 | lỗi sau gán trước resume để con treo sống | bước dọn job ở (9) khi ĐÃ GÁN | J9: "job không rỗng / con sống" | **k2** đặt cờ ĐÃ GÁN sau (7) thay vì sau (5) |
| 11 | bước dọn lỗi chặn bước sau | `_1174_win_cleanup` chạy hết | S4: "bước 2 không chạy" | **k3** `break` sau ngoại lệ đầu tiên trong `_1174_win_cleanup` |
| 12 | 0 hoặc ≥2 luồng ứng viên | `_1174_win_pick_thread` đúng-một | S2: "nhiều ứng viên được nhận" | **t1** trả mục khớp đầu tiên |
| 13 | `ResumeThread` ≠ 1 được nhận | `_1174_win_resume_ok` | S3: "count=2 được nhận" | **t2** đổi `== 1` thành `>= 1` |
| 14 | treo vô hạn chờ tiến trình đầu | `proc.wait(timeout=…)` | J2: "không ném lifecycle deadline trong < 5 s" (watchdog ngoài ca 60 s) | **d0** bỏ `timeout=` |
| 15 | đối số sai lọt vào Windows | kiểm đối số trước nền | S5 dòng `argv=[]` (trên Linux lý do phải là "spawn arguments") | **g0** đưa kiểm `os.name` lên trước kiểm đối số |

Đường KHÔNG có kích hoạt native tự nhiên, khai thẳng (không tính là đã đo bằng ca native): TID cũ giữa snapshot và `OpenThread` (chốt `GetProcessIdOfThread`); snapshot lỗi/duyệt kết thúc bằng mã khác 18; `OpenThread` NULL; `TerminateJobObject` FALSE trên job hợp lệ. Logic chọn/nhận của các đường này nằm trong hàm thuần đã đo (S2, S3); phần gọi Win32 chỉ đọc mã code review.

## 5. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Linux không đổi: CI Ubuntu exact head `GOM: ĐẠT`; sổ ID ca của base là TẬP CON của head và mọi ID base đạt/bỏ-qua y như base; `MUTANTS` head == base (cùng khoá, cùng giá trị); mỗi mốc (tìm) của `MUTANTS` đang có vẫn khớp ĐÚNG MỘT lần trên head. | Rút đăng ký một ca base ⇒ đỏ; đổi tên một khoá giữ số lượng ⇒ đỏ; mã mới làm một mốc mutant cũ khớp 2 lần ⇒ đỏ. |
| N2 | Chỉ THÊM, cả hai tệp: `_additive1342r2(<blob base>, <blob head>)` cho `packet_loop.py` ⇒ `[]`; và với `packet_loop_test.py`, `difflib` trên dòng: mọi opcode là `equal` hoặc `insert` (không `replace`/`delete`). Executor ghi lệnh + kết quả vào thân PR; phiên điều phối đo lại kèm phản chứng chạy thật. | Sửa một byte thân hàm r1/r2/r3 ⇒ khác `[]`; thêm decorator vào hàm mới ⇒ khác `[]`; sửa một byte thân `_native1342` trong tệp test ⇒ có opcode `replace`. |
| N3 | Không nối dây: `wp1342_additive_byte_preserved` (vế N3, cây làm việc) đạt. N2 và N3 là CẶP: N3 chỉ quét dạng tham chiếu mà predicate AST nhận, N2 chứng minh khối mới tồn tại và chỉ thêm. | Thêm lời gọi `_1174_win_spawn_job` trong `_1174_process` ⇒ đỏ. |
| N4 | M5 (S1–S5) đạt trên Linux (CI) và Windows (Desktop). | Đột biến c (S1), t1 (S2), t2 (S3), k3 (S4), g0 (S5) ⇒ đỏ đúng dấu hiệu. |
| N5 | Windows vẫn bị từ chối, không đổi: chạy ĐÚNG tập ID base đã ghi (`wp1174_windows_claim_rejected` + 12 ID `WP1174_BOTH` + ca native r1–r3) trên base và head trong cùng lượt; trạng thái, lý do nếu bỏ qua, và dấu hiệu dương của ca native khớp từng ID. | Một ID lệch base; đột biến mở chốt Windows (đổi `_1174_require(os.name != "nt" …)` của đường claim) ⇒ đỏ tại `wp1174_windows_claim_rejected`. |
| N6 | M6 J1–J12 đạt trên Desktop, mỗi ca có dấu hiệu dương; J3, J4, J5, J10 chạy thêm trên VM `tra-luat-win`. Biên nhận ghi ID + assertion đầy đủ + nhánh J12 đã xảy ra + mã `winerror` J4. | Ca native in `BỎ QUA` trên Windows ⇒ ĐỎ; cháu/con sống sót ⇒ ĐỎ; J4/J12 rơi vào `KHÔNG ĐO` ⇒ tiêu chí `not_measured`, không `passed`. |
| N7 | Mười lăm đột biến §4b bị giết đúng DẤU HIỆU đã ghi: Windows (a1 a2 a3 b c e1 e2 h k1 k2 d0) trên Desktop; thuần (c t1 t2 k3 g0) trên Linux. Hợp đồng N7 của r1: driver byte-exact trong hồ sơ land; chỉ tính giết khi assertion đích thất bại và đối chứng đạt; chuỗi không khớp hoặc lỗi trước hành vi đích ⇒ `KHÔNG ĐO`. | Đột biến SỐNG; ca "đỏ" vì import/fixture; đỏ với dấu hiệu KHÁC dấu hiệu đã ghi. |
| N8 | Ruff `--select F` (bản ghim của gate) trên hai tệp: TẬP diagnostic (mã, tệp, tên) của head == base (không chỉ số lượng); `adr-song`, `doctrine-scan` rc 0; `git diff --check` sạch; `eol_policy --all` ok; numstat đúng 2 tệp, ≤ 450 dòng thêm (`ADR-0053`). | Thay một diagnostic bằng diagnostic khác cùng số lượng ⇒ đỏ; tệp thứ ba ⇒ đỏ; vượt trần ⇒ dừng theo §7. |

Đo Windows (N4 phần Windows, N5, N6, N7 phần Windows) trên **`DESKTOP-T9R33P2`** (ưu tiên, Q8 r1); VM `tra-luat-win` dự phòng và đo bổ sung. Base và head đo trong cùng một lượt.

Ngân sách dòng (ước tĩnh, chưa đo): mã — bindings + cấu trúc 40–50, hằng + 3 hàm thuần 20–25, `_1174_win_job_empty` 12–15, `_1174_win_spawn_job` 65–80 ⇒ **140–170**; test — S1–S5 45–55, helper bắt tay/handle/trợ giúp 40–50, J1–J12 130–160 ⇒ **215–265**. Tổng **355–435**. Đo numstat thật; vượt 450 ⇒ §7, không cắt assertion/cleanup để ép số.

## 6. `pham_vi_e`

Không chạm E4, E5. Không đảo quyết định "chỉ Linux" (primitive chưa nối dây) ⇒ không E3. Ca native chỉ giết tiến trình do chính ca sinh ra, qua handle/job của nó.

## 7. `luat_dung`

- Trần lời gọi Codex theo `ADR-0055`; trần vòng review theo `ADR-0048`. Chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- numstat vượt `ADR-0053` ⇒ dừng; **E2**.
- Cần sửa thân định nghĩa đang có, sửa ngoài write set, hoặc nối dây ⇒ dừng, revision đặc tả.
- `Popen` của Python trên máy đo không giữ con treo với `CREATE_SUSPENDED` (J6 đỏ trên head sạch, hoặc `ResumeThread` ≠ 1 trên đường thuận) ⇒ dừng; không chuyển sang API không tài liệu; revision đặc tả.
- Máy đo Windows không có trong hạn lease ⇒ tiêu chí native ghi `not_measured`; lease hết hạn theo protocol; quyết định gia hạn/cấp lại thuộc chủ kho (**E2**).
- Đặc tả không thuộc Mission ⇒ chờ chủ kho duyệt băm theo `ADR-0067` (**E2**), một lần, sau khi review độc lập approve.

## 8. `hinh_dang_ke_thua`

`khong_ap_dung`. Ghi chú từ r1–r3 và lượt land 18-11: hàm mới không decorator (r2 F2); so additive dùng `_additive1342r2` (r2 F1); hook là tham số default hằng `None`, không phải seam bỏ qua mã runtime (r3 F5) — `truoc_gan`/`between` chạy TRÊN đường mặc định, không thay nó; tiêu chí chỉ có lời khai ghi `not_measured` (Codex P1 PR #1398, #1403).

## 9. Quyết định đã ghi

- **Q1.** Tách r1d thành r1d-a (tiến trình) và r1d-b (probe) — chủ kho 2026-11-18. **Tách tầng hai a1/a2 (chủ kho 2026-11-18)**, sau review lượt 1 (ước lượng gộp 375–550 dòng): a1 = vòng đời trong job không pipe (revision này), a2 = transport hai pipe (revision sau).
- **Q2.** Đóng khe "chạy trước, gán sau" bằng `CREATE_SUSPENDED` + gán + `ResumeThread` (tìm luồng qua Toolhelp) — chủ kho 2026-11-18.
- **Q3.** Cấm tuyệt đối breakaway: `LimitFlags == KILL_ON_JOB_CLOSE` — chủ kho 2026-11-18.
- **Q4.** Job còn tiến trình sau khi kết thúc ⇒ `_1174Error`, fail-closed — chủ kho 2026-11-18.

## 10. `chua_do_duoc`

- Kích thước thật (ước 355–435).
- `Popen` + `CREATE_SUSPENDED` trên Python 3.13 Windows chỉ mới đọc mã (reviewer lượt 1), chưa chạy; nếu sai thì §7.
- Job lồng là năng lực CÓ ĐIỀU KIỆN (Win8+ hỗ trợ, nhưng gán có thể bị từ chối tuỳ tổ hợp giới hạn); J12 ghi nhánh xảy ra, không khẳng định bảo đảm.
- J4: danh sách mã cho phép `{5}` dựa trên tài liệu; mã khác ⇒ `KHÔNG ĐO` và ghi mã thật để mở rộng có căn cứ ở revision sau.
- Các đường §4b chỉ có code review (TID cũ, snapshot lỗi, `OpenThread` NULL, terminate FALSE).
- Hằng số §0 trôi khi master tiến; người cấp lease đo lại.

## 11. Nhật ký review

- Lượt 1 (Codex, master `e2c3b82`, verdict `request_changes`: 2 P1, 7 P2, 1 P3) trên bản r1d-a gộp transport. Xử lý: chủ kho tách a1/a2. Thuộc a1, đã đóng trong bản này: P1 sở hữu cleanup (M4 đăng ký dọn theo mốc, `_1174_win_cleanup`, J8/J9/S4, k1–k3); P2 luồng treo (M2 a/b, S2/S3, t1/t2, `GetProcessIdOfThread`, b/c tách dấu hiệu, ABI M1 + S1); P2 job rỗng (M3 ném "job query", J11/a3, bắt tay + giữ handle, a1/a2 tách); P2 breakaway/lồng/kế thừa (J4 danh sách mã + đối chứng job cho phép breakaway, J5/e2, J7/h, J12); P2 N1–N8 (sổ ID, so chỉ-chèn tệp test, ruff theo tập, N5 phản chứng, N7 dấu hiệu); P2 dự toán (ngân sách theo khối); P3 văn bản (`_native1342` 18159, §9 "Quyết định đã ghi", job lồng có điều kiện, máy đo offline ⇒ `not_measured`). Chuyển sang a2: P1 hai reader, ma trận `on_bytes`, trần byte, (d)(f)(g), M3 cũ.
