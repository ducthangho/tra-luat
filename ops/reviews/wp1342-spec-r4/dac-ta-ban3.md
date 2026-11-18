tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: nang_tran AskUserQuestion chủ kho 2026-11-18 phiên điều phối #1206 (≤ 2 tệp / ≤ 550 dòng thêm; thay ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab)

# WP1174-WINDOWS-BACKEND r4 — lõi vòng đời tiến trình trong Job Object, Windows native, đứng riêng, KHÔNG pipe (bậc r1d-a1-i), chưa nối vào runtime

- packet_id: WP1174-WINDOWS-BACKEND; revision: 4;

| trường | giá trị |
|---|---|
| `packet_issue` | #1342 |
| `nguon_cap_viec` | Lộ trình bậc ở §1 đặc tả r1. Chủ kho 17-11-2026: seed + BootId vào r3 (land `aeb5cae`, `landed: true`), tiến trình + probe sang r1d. Chủ kho 18-11-2026 (phiên điều phối #1206): "Làm tiếp #1342 r1d", rồi lần lượt tách r1d → r1d-a (tiến trình) / r1d-b (probe); r1d-a → a1 (vòng đời, không pipe) / a2 (transport hai pipe); a1 → **a1-i** (lõi vòng đời, revision này) / a1-ii (kháng thoát job: breakaway tường minh/ngầm, job lồng); và nâng trần kích thước lên 550 cho riêng revision này. §9. |
| `review_class` | `sensitive` (runtime trạng thái WP1174) |
| `base` | `e2c3b82f818bd1739d31261e8129d3ef44915acf`. Số đo §0 lấy lúc 2026-11-18T17:20Z–18:10Z trên OID này. L5: người cấp lease đo lại §0 trên OID base thật (1) trước khi công bố băm, (2) lúc cấp lease, (3) trước merge; lệch ⇒ revision đặc tả. |

**Đánh số:** `revision: 4` (ADR-0063, số nguyên); bậc **r1d-a1-i** của lộ trình. r1d-a1-ii, r1d-a2, r1d-b là các revision sau.

## 0. Hiện trạng (đo trên `e2c3b82`; số dòng từ `def`, gồm dòng trống cuối khối)

- `_1174_process` 4260 (51 dòng, Linux, có pipe): mẫu hợp đồng cho a2, KHÔNG đổi ở r4. `killpg` vô điều kiện chỉ chạy khi đã vào `try` cleanup nội bộ (sau `Popen`, `ExitStack`, `streams`).
- `_1174Error(ValueError)` 3670; `_1174_require`.
- `_1174_win_api` 6419 (18 dòng): `WinDLL("kernel32", use_last_error=True)` mới mỗi lần gọi, bind argtypes/restype tường minh, trả `(c, w, k)`. r1–r3 đứng riêng ở 6406–6742; `_1174_win_seed` 62 dòng, `_1174_win_persist` 45, `_1174_win_read`/`_lock` 35.
- CPython 3.13 `subprocess.py` (Windows, ~1555–1578): `creationflags` chuyển nguyên cho `_winapi.CreateProcess`; giữ process handle ở `Popen._handle` (chi tiết triển khai CPython); ĐÓNG primary thread handle; KHÔNG gọi `ResumeThread`. Do đó phải tìm lại luồng qua Toolhelp.
- `.claude/dev/launcher.py` `_job_windows` 905–973 gán job SAU khi con đã chạy (khe tự khai); `_pid_trong_job` 976–1003 dùng lớp 3. Không sửa launcher.
- Test: `WP1174_BOTH` 12421 (12 ID); `_new1342` 17879, `_additive1342` 17896, `_wired1342` 17920, `_native1342` 18159 (in `WP1342_NATIVE_V1` ở 18165 sau khi thân ca trả về), `_additive1342r2` 18178; đăng ký ca 18170/18171, 18365/18366, 18553/18554; `MUTANTS` 3592 + các `MUTANTS.update`.
- Kích thước tiền nhiệm (numstat): r1 +428 (mã 130 + test 298), r2 +293, r3 +300 (test 188).

## 1. Phạm vi r4 (r1d-a1-i)

Thêm, ĐỨNG RIÊNG (không hàm hiện có nào gọi tới): bindings job/thread có nghiệm thu ABI; ba hằng cho phép; ba hàm thuần; `_1174_win_job_empty`; `_1174_win_spawn_job` chạy MỘT lệnh trong job từ trạng thái treo, chờ tiến trình đầu thoát có hạn, thu hồi cả job theo các bước có hậu điều riêng. stdin/stdout/stderr của con đều `DEVNULL`. Không sửa thân định nghĩa nào đang có.

## 2. `write_set`, `ngoai_pham_vi`, ranh giới bảo đảm

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
```

Ngoài phạm vi:
- Không sửa thân hàm/khối nào đang có (kể cả `_1174_process`, `_1174_win_*` r1–r3, helper test `_new1342` `_additive1342` `_wired1342` `_additive1342r2` `_native1342`). Không đổi `MUTANTS` đang có; không runner mới; không CI Windows.
- **Để r1d-a1-ii:** breakaway tường minh (J4 cũ, danh sách mã `{5}`, job đối chứng cho phép breakaway, đột biến e1), breakaway ngầm (J5 cũ, membership với job đích, e2), job lồng (J12 cũ). Hằng `_1174_WIN_JOB_LIMIT == 0x2000` vẫn khoá ở r4 bằng S1 và J10.
- **Để r1d-a2:** đọc hai pipe, hạn mức byte chung, huỷ I/O có thời hạn (P1 "hai reader" lượt 1), `on_bytes`/callback, trần byte, `stdin` bytes, M3 cũ, P1–P4 cũ, đột biến (d)(f)(g) cũ, **N4 (f)(g) cũ**, CRLF/NUL.
- **Để r1d-b:** probe.
- Không nối dây. Không API không tài liệu, không `pywin32`, không đồ giả Win32 (Q11 r1). Không giới hạn CPU/bộ nhớ/số tiến trình.

**Ranh giới bảo đảm (khai thẳng, có ca đo J10b):**
- Bảo đảm: mọi tiến trình thuộc cây kế thừa job của con (con và hậu duệ do nó tạo SAU khi resume) bị thu hồi khi hàm trả, hoặc khi tiến trình gọi chết SAU lúc gán job thành công (nhờ `KILL_ON_JOB_CLOSE`).
- KHÔNG bảo đảm — nợ có tên **`wp1342-pre-assign-orphan`**: nếu tiến trình gọi chết trong khoảng `Popen` → `AssignProcessToJobObject` (không `finally` nào chạy), con treo bị bỏ lại ngoài job. Con chưa từng chạy lệnh nào (tạo với `CREATE_SUSPENDED`, chưa resume) nên không thể sinh hậu duệ, nhưng tiến trình treo tồn tại tới khi bị giết từ ngoài. Đường đóng triệt để là `CreateProcessW` + `PROC_THREAD_ATTRIBUTE_JOB_LIST` (OS gán job ngay khi tạo); chủ kho đã bác vì kích thước (§9 Q2).
- KHÔNG bảo đảm: ngắt bất đồng bộ trong tiến trình gọi (vd `KeyboardInterrupt`) rơi giữa hai câu lệnh, sau khi một tài nguyên đã nhận nhưng trước khi trạng thái sở hữu được ghi; khi đó đường dọn có thể dựa trạng thái cũ. Hậu quả tối đa tương đương nợ trên (con treo bị bỏ lại) hoặc job chưa đóng tới khi tiến trình gọi thoát (lúc đó `KILL_ON_JOB_CLOSE` dọn).
- Ngoài phạm vi Job Object: tiến trình do dịch vụ ngoài job tạo thay mặt con (COM/WMI/Task Scheduler). Giả định: không tiến trình ngoài nào có quyền can thiệp vào con (chèn luồng, resume hộ) trong khoảng tạo → resume.
- Phiên bản Python hỗ trợ: CPython (`sys.implementation.name == "cpython"`), `sys.version_info >= (3, 11)` (cần `add_note`); khác ⇒ `_1174Error("spawn runtime")` TRƯỚC `Popen`.

## 3. Hằng số (danh sách CHO PHÉP, một giá trị mỗi hằng)

| hằng | giá trị | ý nghĩa |
|---|---|---|
| `_1174_WIN_JOB_LIMIT` | `0x2000` | `LimitFlags` = CHỈ `KILL_ON_JOB_CLOSE` |
| `_1174_WIN_SPAWN_FLAGS` | `0x204` | `creationflags` = CHỈ `CREATE_SUSPENDED` (0x4) \| `CREATE_NEW_PROCESS_GROUP` (0x200) |
| `_1174_WIN_RESUME_OK` | `1` | giá trị DUY NHẤT nhận từ `ResumeThread` |

## 4. `muc_tieu`

| # | mục tiêu |
|---|---|
| M1 | `_1174_win_api_job()`: gọi `_1174_win_api()`; bind trên CÙNG `kernel32` đúng tập (không hơn) với chữ ký: `CreateJobObjectW([V, S], H)`, `SetInformationJobObject([H, c_int, V, D], B)`, `AssignProcessToJobObject([H, H], B)`, `TerminateJobObject([H, UINT], B)`, `QueryInformationJobObject([H, c_int, V, D, P], B)`, `CreateToolhelp32Snapshot([D, D], H)`, `Thread32First([H, V], B)`, `Thread32Next([H, V], B)`, `OpenThread([D, B, D], H)`, `GetProcessIdOfThread([H], D)`, `ResumeThread([H], D)`, `GetHandleInformation([H, P], B)` (`V`=`c_void_p`, `H`=`w.HANDLE`, `D`=`w.DWORD`, `B`=`w.BOOL`, `S`=`w.LPCWSTR`, `P`=`POINTER(DWORD)`). Cấu trúc theo layout Win64 có tài liệu, kiểu độ rộng cố định: `JOBOBJECT_BASIC_LIMIT_INFORMATION` (64 byte, `LimitFlags` offset 16), `IO_COUNTERS` (48), `JOBOBJECT_EXTENDED_LIMIT_INFORMATION` (144), `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION` (48, `ActiveProcesses` offset 40), `THREADENTRY32` (28, `th32OwnerProcessID` offset 12). Trả `(c, w, k, s)` với `s` là namespace các lớp cấu trúc. |
| M2 | Ba hàm THUẦN (mọi nền, không ctypes): (a) `_1174_win_pick_thread(entries, pid)`: `entries` là iterable `(owner_pid, tid)`; trả tid khi có ĐÚNG MỘT mục `owner_pid == pid`; 0 hoặc ≥ 2 ⇒ `_1174Error("suspended start")`. (b) `_1174_win_resume_ok(count)`: không lỗi khi `type(count) is int and count == _1174_WIN_RESUME_OK`; khác ⇒ `_1174Error("suspended start")`. (c) `_1174_win_cleanup(steps)`: chạy TỪNG callable theo thứ tự, mỗi cái trong `try` riêng bắt `BaseException` trừ `KeyboardInterrupt`/`SystemExit` (hai loại này vẫn ghi lại rồi chạy tiếp các bước còn lại, ném lại sau cùng); bước lỗi không chặn bước sau; trả list ngoại lệ theo thứ tự. |
| M3 | `_1174_win_job_empty(k, s, job, wait_s)`: lặp tới `wait_s` giây (bước 0,05 s): `QueryInformationJobObject(job, 1, byref(info), sizeof(info), None)`; FALSE ⇒ đọc `ctypes.get_last_error()` NGAY, `_1174Error("job query")` (không đọc buffer, không coi là rỗng); TRUE và `info.ActiveProcesses == 0` ⇒ trả `None`. Hết `wait_s` ⇒ `_1174Error("job not empty")`. |
| M4 | `_1174_win_spawn_job(argv, *, cwd, deadline, env=None, truoc_gan=None, between=None)` → `int`. **(0)** Kiểm đối số: `argv` là list khác rỗng toàn `str`; `deadline` là `int`/`float` không `bool`, `math.isfinite`, `> time.monotonic()`; `cwd` là `str`; `env` `None` hoặc dict str→str; `truoc_gan`, `between` `None` hoặc callable; vi phạm ⇒ `_1174Error("spawn arguments")`. Sau đó `os.name == "nt"` ("native Windows required"), rồi kiểm phiên bản (§2, "spawn runtime"). **(1)** `CreateJobObjectW(None, None)`; NULL ⇒ `get_last_error` ngay, "job create". ĐĂNG KÝ bước `close_job`. **(2)** `SetInformationJobObject(job, 9, …)` với `info.BasicLimitInformation.LimitFlags = _1174_WIN_JOB_LIMIT`, các trường khác 0; FALSE ⇒ "job limit". **(3)** `proc = Popen(argv, cwd, env, stdin/stdout/stderr=DEVNULL, close_fds=True, creationflags=_1174_WIN_SPAWN_FLAGS)`. NGAY sau khi `Popen` trả (trước mọi kiểm khác): ĐĂNG KÝ bước `kill_truoc_gan` (chỉ hiệu lực khi chưa gán) và `reap`. Sau đó mới kiểm `getattr(proc, "_handle", None)` khác `None` ⇒ thiếu ⇒ "spawn handle" (bước `kill_truoc_gan` dùng `proc.kill()`, vốn cũng dựa `_handle` của CPython; khi thiếu, bước ấy ghi lỗi và nợ `wp1342-pre-assign-orphan` áp dụng). **(4)** `truoc_gan(proc)` nếu có. **(5)** `AssignProcessToJobObject(job, proc._handle)`; FALSE ⇒ "job assignment"; TRUE ⇒ đặt `da_gan = True` NGAY câu lệnh kế tiếp. **(6)** `between(job)` nếu có. **(7)** `snap = CreateToolhelp32Snapshot(0x4, 0)`; so với `INVALID_HANDLE_VALUE = c_void_p(-1).value` (đúng độ rộng con trỏ) ⇒ "thread snapshot"; ĐĂNG KÝ `close_snap`. `te = THREADENTRY32(); te.dwSize = sizeof(te)`; `Thread32First` FALSE ⇒ đọc last-error ngay: 18 (`ERROR_NO_MORE_FILES`) ⇒ danh sách rỗng, khác ⇒ "thread snapshot"; lặp `Thread32Next` tới FALSE với last-error 18 (khác ⇒ "thread snapshot"). Chọn tid bằng `_1174_win_pick_thread`. `th = OpenThread(0x2 \| 0x800, False, tid)`; NULL ⇒ "suspended start"; ĐĂNG KÝ `close_thread`. `GetProcessIdOfThread(th)` == 0 hoặc ≠ `proc.pid` ⇒ "suspended start". `_1174_win_resume_ok(ResumeThread(th))`. Trong suốt (5)–(7) `proc` (và `_handle`) được giữ sống. **(8)** `proc.wait(timeout=deadline - time.monotonic())`; `TimeoutExpired` ⇒ "lifecycle deadline"; ghi `rc`. **(9)** `finally`: `_1174_win_cleanup` với các bước theo thứ tự, mỗi bước một hậu điều: `terminate` (chỉ khi `da_gan`): `TerminateJobObject(job, 1)` FALSE ⇒ lỗi "job terminate"; `xac_nhan` (chỉ khi `da_gan`): `_1174_win_job_empty(…, 5)` — chạy kể cả khi `terminate` lỗi, và là phép xác nhận DUY NHẤT; `kill_truoc_gan` (chỉ khi KHÔNG `da_gan`): `proc.kill()`; `reap`: `proc.wait(5)`, `TimeoutExpired` ⇒ "leader not reaped"; `close_thread`, `close_snap`, `close_job`: `CloseHandle` FALSE ⇒ "handle close". KHÔNG có `proc.kill()` khi đã gán. Ưu tiên lỗi: có lỗi gốc ⇒ ném lỗi gốc, mỗi lỗi dọn ghi bằng `add_note(repr(lỗi_dọn))`; không lỗi gốc mà có lỗi dọn ⇒ ném lỗi dọn ĐẦU TIÊN, các lỗi dọn còn lại ghi `add_note`. Chỉ trả `rc` khi KHÔNG có lỗi nào. |
| M5 | Ca THUẦN (mọi nền) `wp1342_pure_spawn_*`, mỗi vector một assertion có nhãn riêng: **S1** ba assertion: `JOB_LIMIT == 0x2000`, `SPAWN_FLAGS == 0x204`, `RESUME_OK == 1`. **S2** `pick_thread`: `[]` ⇒ lỗi; `[(7,1),(7,2)]` (pid 7) ⇒ lỗi; `[(9,1),(7,5),(8,6)]` ⇒ 5. **S3** `resume_ok` theo thứ tự: `2` ⇒ lỗi (assertion "count=2"); `0` ⇒ lỗi; `0xFFFFFFFF` ⇒ lỗi; `True` ⇒ lỗi; `1` ⇒ qua. **S4** `cleanup([ném, ghi_cờ])` ⇒ cờ được ghi, trả đúng 1 lỗi. **S5** `_1174_win_spawn_job` từ chối "spawn arguments" cho `argv=[]` (assertion đầu tiên), `["x", 1]`, `"x"`, deadline đã qua, `True`, `float("inf")`, `cwd=None`, `between=1`; trên nền khác Windows đối số hợp lệ ⇒ "native Windows required". Không thêm vào `WP1174_REQUIRED`/`WP1174_BOTH`. |
| M6 | Hạ tầng test native (trong `packet_loop_test.py`). **Bindings phía test** (không thuộc allowlist M1): `OpenProcess`, `DuplicateHandle`, `GetCurrentProcess`, `WaitForSingleObject`, `TerminateProcess`, `CloseHandle`, `GetProcessTimes`, `SetHandleInformation` (chỉ để dựng phản chứng `h` nếu cần), chữ ký tường minh. **Bắt tay xác minh danh tính:** fixture ghi `{pid, creation_time (GetProcessTimes trên chính nó), nonce}` bằng ghi tệp tạm + `os.replace` (nguyên tử); nonce do CA cấp qua argv; ca mở `OpenProcess(SYNCHRONIZE \| PROCESS_QUERY_LIMITED_INFORMATION \| PROCESS_TERMINATE)`, đòi `GetProcessTimes(handle).creation == creation_time` trong tệp, và handle chưa signaled; chỉ sau đó ca mới ghi tệp `go` cho fixture đi tiếp. Mọi kiểm vòng đời trên HANDLE đó; tự dọn bằng `TerminateProcess` trên handle giữ khi đột biến sống sót. **Luồng quan sát:** chạy song song khi `_1174_win_spawn_job` đang chặn trong luồng chính; đọc bắt tay, mở handle, ghi `go`; mọi chờ có hạn (≤ 20 s), hết hạn ⇒ `KHÔNG ĐO` (lỗi fixture, không phải dấu hiệu). **Trợ giúp (J10/J10b):** tiến trình python riêng chạy `_1174_win_spawn_job` từ cây làm việc; giao thức tệp: `san_sang` (pid trợ giúp + creation time), `da_gan` hoặc `truoc_gan` (pid + creation time con), `chau` (của cháu, J10); ca xác minh từng mốc trước khi `TerminateProcess` trợ giúp bằng handle `Popen` của chính ca, rồi chờ trợ giúp signaled. |
| M7 | Ca NATIVE `wp1342_native_job_*` qua `_native1342` (nền khác in `BỎ QUA <lý do>`, không tính đạt), lệnh con `sys.executable -B -c …`, mỗi ca có dấu hiệu dương. **J0 ABI**: tập tên bind == allowlist M1; `argtypes`/`restype` từng hàm khớp bảng M1; `sizeof`/`offsetof` khớp số ở M1; chạy trên Win64 (kiểm `sizeof(c_void_p) == 8`, khác ⇒ `KHÔNG ĐO`). **J1 thuận**: con ghi tệp đánh dấu rồi `exit(7)` ⇒ trả `7`, tệp có. **J2 hạn**: con bắt tay rồi `sleep(30)`; deadline = lúc gọi + 3 s; ném "lifecycle deadline" trong khoảng 3–8 s; handle con (qua quan sát) signaled. **J3 mồ côi**: con sinh cháu `DETACHED_PROCESS (0x8)`; cháu bắt tay rồi `sleep(30)`; con chờ `go` của cháu rồi `exit(0)`; hàm trả `0`; handle cháu signaled khi hàm trả. **J6 treo trước gán**: con bắt tay ở dòng đầu; `between(job)` kiểm tệp bắt tay của con CHƯA tồn tại (con chưa chạy); sau khi hàm trả, tệp có. **J7 handle kế thừa**: `between(job)`: `GetHandleInformation(job, &f)` TRUE và `f & 0x1 == 0`. **J8 lỗi trước gán**: `truoc_gan(proc)` lấy bản sao handle con (`DuplicateHandle`, quyền `SYNCHRONIZE \| PROCESS_TERMINATE`) rồi ném `RuntimeError("j8")`; hàm ném lại đúng lỗi ấy; bản sao signaled khi hàm trả (không chờ thêm). **J9 lỗi sau gán**: `truoc_gan` giữ `proc`; ca tạo trước một tiến trình phụ `sleep(30)` (bắt tay, handle giữ); `between(job)` gán tiến trình phụ vào CÙNG job (thành viên thứ hai mà không bước dọn nào ngoài job có thể chạm tới), lấy bản sao handle job, rồi ném `RuntimeError("j9")`; hàm ném lại lỗi ấy; khi hàm trả: handle con và handle tiến trình phụ signaled, `ActiveProcesses == 0` qua bản sao job (query phải TRUE). **J10 cha chết sau gán**: trợ giúp chạy `_1174_win_spawn_job` với con sinh cháu, con và cháu bắt tay và `sleep(30)`; sau khi xác minh `da_gan` + `chau`, ca `TerminateProcess` trợ giúp; handle con và cháu signaled trong ≤ 5 s. **J10b cha chết trước gán (đo nợ)**: trợ giúp dùng `truoc_gan` ghi mốc `truoc_gan` (pid + creation time con lấy qua `GetProcessTimes(proc._handle)`) rồi ngủ; ca mở handle con, xác minh, `TerminateProcess` trợ giúp; sau 2 s: con CHƯA signaled (còn treo, bị bỏ lại — đúng nợ đã khai) VÀ tệp bắt tay của con KHÔNG tồn tại (chưa từng chạy); ca tự dọn con. J10b đạt nghĩa là ranh giới đã khai ĐÚNG như đo, không phải bảo đảm thu hồi. **J11 query lỗi**: `_1174_win_job_empty` với handle tệp (mở bằng `CreateFileW` của r1) ⇒ "job query"; với job rỗng do ca tạo ⇒ `None`. J3, J9, J10 chạy thêm trên VM `tra-luat-win`. |
| M8 | Đột biến qua driver NGOÀI kho (khuôn r1–r3: mỗi cặp (tìm, thay) khớp đúng một chỗ, đổi khối thì neo cả khối làm một cặp; bản sao tạm; ca đích + đối chứng khoẻ; lỗi import/fixture, quan sát hết hạn hoặc watchdog ngoài ca 90 s ⇒ `KHÔNG ĐO`). Bảng §4b. |

## 4b. Đường vào, chốt, ca, đột biến (mỗi đường một chốt; dấu hiệu = ID ca + nhãn assertion, chỉ đột biến đó gây ra)

| # | đường | chốt | dấu hiệu đỏ | đột biến |
|---|---|---|---|---|
| 1 | con thoát, cháu mồ côi còn sống | `terminate` ở (9) | J3 ném "job not empty" | **a1** xoá lời gọi `TerminateJobObject` |
| 2 | tiến trình gọi chết sau gán | `KILL_ON_JOB_CLOSE` | J10 "con/cháu sống sau khi cha chết" | **a2** `_1174_WIN_JOB_LIMIT = 0` |
| 3 | query lỗi đọc thành rỗng | M3 ném "job query" | J11 "handle tệp được nhận là job rỗng" | **a3** nhánh query-FALSE đổi thành `return None` |
| 4 | khe "chạy trước, gán sau" | gán trước resume | J6 "tệp bắt tay của con đã có lúc between" | **b** (khối) dời (7) lên trước (5) và chờ tệp bắt tay của con ≤ 5 s trước khi gán; chờ hết hạn ⇒ `KHÔNG ĐO` |
| 5 | con không treo khi tạo | `CREATE_SUSPENDED` | S1 "SPAWN_FLAGS == 0x204" (tất định; mọi đột biến khác không chạm hằng này) | **c** `_1174_WIN_SPAWN_FLAGS = 0x200` |
| 6 | handle job kế thừa | security attributes `None` | J7 "job handle có HANDLE_FLAG_INHERIT" | **h** chèn sau (1) một dòng bind `SetHandleInformation([w.HANDLE, w.DWORD, w.DWORD], w.BOOL)` trên `k` và gọi `(job, 1, 1)`, đòi TRUE |
| 7 | lỗi sau `Popen`, trước gán | `kill_truoc_gan` | J8 "bản sao con chưa signaled khi hàm trả" | **k1** bỏ đăng ký `kill_truoc_gan` |
| 8 | lỗi sau gán, trước resume | `terminate` khi `da_gan` (không `proc.kill` sau gán) | J9 "tiến trình phụ còn sống VÀ lỗi j9 không có ghi chú job not empty" | **k2** đặt `da_gan = True` sau (7) thay vì sau (5) |
| 9 | bước dọn lỗi chặn bước sau | `_1174_win_cleanup` chạy hết | S4 "bước 2 không chạy" | **k3** `break` sau ngoại lệ đầu |
| 10 | 0/≥2 luồng ứng viên | đúng-một | S2 "hai ứng viên được nhận" | **t1** trả mục khớp đầu tiên |
| 11 | `ResumeThread` ≠ 1 được nhận | `resume_ok` | S3 "count=2" | **t2** `== _1174_WIN_RESUME_OK` đổi thành `in (1, 2)` |
| 12 | treo vô hạn chờ tiến trình đầu | `wait(timeout=…)` | J2 "không ném lifecycle deadline trong 3–8 s" | **d0** bỏ `timeout=` |
| 13 | đối số sai lọt vào Windows | kiểm đối số trước nền | S5 "argv=[] phải là spawn arguments" | **g0** (khối) đổi chỗ khối kiểm `os.name` lên trước khối kiểm đối số |
| 14 | ABI sai lệch | layout cố định | J0 "THREADENTRY32 offset th32OwnerProcessID == 12" | **abi** đổi kiểu trường `th32OwnerProcessID` sang `c_uint64` |

Phân biệt: k2 chỉ đổi hành vi khi có lỗi giữa (5) và (7), nên đường thuận J3 không đổi dưới k2. Ở J9, cả a1 và k2 đều để tiến trình phụ sống; dấu hiệu tách bằng ghi chú lỗi: dưới a1 bước `xac_nhan` vẫn chạy và lỗi gốc `j9` mang `add_note` chứa "job not empty"; dưới k2 không có bước `xac_nhan` nên KHÔNG có ghi chú ấy. Dấu hiệu của k2 = J9 "tiến trình phụ còn sống VÀ không có ghi chú job not empty"; dấu hiệu của a1 = J3 "job not empty". a2/c chạm hai hằng khác nhau; S1 tách assertion theo hằng nên a2 làm đỏ assertion `JOB_LIMIT`, không đỏ `SPAWN_FLAGS`. b giữ cờ treo nên S1 xanh; c không đổi thứ tự nên J6 có thể đỏ hoặc không, dấu hiệu của c chỉ là S1.

Đường KHÔNG có kích hoạt native tự nhiên (chỉ code review, KHÔNG ghi là đã đo bằng ca native): TID cũ giữa snapshot và `OpenThread` (chốt `GetProcessIdOfThread`); `Thread32First/Next` lỗi khác 18; `OpenThread` NULL; `TerminateJobObject` FALSE trên job hợp lệ; `CloseHandle` FALSE; `GetProcessIdOfThread == 0`. Logic chọn/nhận nằm trong hàm thuần đã đo (S2, S3, S4).

## 5. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Linux không đổi: CI Ubuntu exact head `GOM: ĐẠT`; sổ ID ca base ⊆ head, mỗi ID base cùng trạng thái (đạt/bỏ qua + lý do); `MUTANTS` head == base; mỗi mốc (tìm) của `MUTANTS` đang có khớp ĐÚNG MỘT lần trên head. Biên nhận ghi từng ID và từng mốc. | Rút một ca base; đổi tên một khoá giữ số lượng; mã mới làm một mốc cũ khớp 2 lần. |
| N2 | Chỉ THÊM, cả hai tệp. `packet_loop.py`: `_additive1342r2(base, head) == []`. `packet_loop_test.py`: (i) với mỗi định nghĩa mức module của base (def/class/gán), đoạn nguồn (`ast.get_source_segment`) ở head BẰNG TỪNG BYTE và vẫn là một định nghĩa mức module riêng; (ii) không tên mức module nào của base bị định nghĩa lại ở head; (iii) `difflib` trên dòng chỉ có `equal`/`insert`. Phiên điều phối đo lại kèm phản chứng chạy thật. | Sửa một byte thân hàm r1–r3 ⇒ khác `[]`; decorator vào hàm mới ⇒ khác `[]`; chèn `return lambda c: None` vào đầu thân `_native1342` ⇒ (i) ĐỎ; thêm `def _native1342(...)` ở cuối tệp ⇒ (ii) ĐỎ. |
| N3 | Không nối dây + vế dương: `wp1342_additive_byte_preserved` (vế N3, cây làm việc) đạt; VÀ head chứa đúng tập tên mới mức module `{_1174_WIN_JOB_LIMIT, _1174_WIN_SPAWN_FLAGS, _1174_WIN_RESUME_OK, _1174_win_api_job, _1174_win_pick_thread, _1174_win_resume_ok, _1174_win_cleanup, _1174_win_job_empty, _1174_win_spawn_job}` (không thiếu, không thừa tên mới nào khác trong `packet_loop.py`). | Thêm lời gọi `_1174_win_spawn_job` trong `_1174_process` ⇒ đỏ; bỏ một khối bắt buộc ⇒ vế dương đỏ. |
| N4 | M5 (S1–S5) đạt trên Linux (CI) và Windows (Desktop). | c (S1 SPAWN_FLAGS), t1 (S2), t2 (S3 "count=2"), k3 (S4), g0 (S5 argv=[]) ⇒ đỏ đúng dấu hiệu. |
| N5 | Windows vẫn bị từ chối, không đổi: chạy đúng tập ID base đã ghi (`wp1174_windows_claim_rejected` + 12 ID `WP1174_BOTH` + ca native r1–r3) trên base và head cùng lượt; so từng ID trên trạng thái, lý do bỏ qua, dấu hiệu dương (bỏ các trường thời gian/pid). | Một ID lệch; đột biến mở chốt claim Windows phải đi tới và đỏ tại assertion đích của `wp1174_windows_claim_rejected`. |
| N6 | J0–J11 + J10b đạt trên Desktop với dấu hiệu dương; J3, J9, J10 đạt thêm trên VM. Biên nhận ghi ID + mọi assertion + kết quả xác minh creation time. | Ca native `BỎ QUA` trên Windows ⇒ ĐỎ; con/cháu/phụ sống sót ⇒ ĐỎ; ca rơi vào `KHÔNG ĐO` ⇒ tiêu chí `not_measured`, không `passed`. |
| N7 | 14 đột biến §4b bị giết đúng dấu hiệu: Windows (a1 a2 a3 b h k1 k2 d0 abi) trên Desktop; thuần (c t1 t2 k3 g0) trên Linux (và lặp lại trên Desktop cho c). Hợp đồng N7 r1: driver byte-exact trong hồ sơ land; chỉ tính giết khi assertion đích thất bại, đối chứng đạt, và nhãn khớp dấu hiệu đã ghi. | Đột biến sống; đỏ vì import/fixture/quan sát hết hạn; đỏ với nhãn KHÁC. |
| N8 | Ruff `--select F` (phiên bản ghim của gate, ghi số phiên bản): TẬP diagnostic (mã, tệp, tên) head == base, ghi từng tệp; `adr-song`, `doctrine-scan` rc 0 (ghi riêng); `git diff --check` sạch; `eol_policy --all` ok; numstat đúng 2 tệp, ≤ **550** dòng thêm (trần nâng, §9). | Thay một diagnostic bằng diagnostic khác cùng số lượng; tệp thứ ba; vượt 550 ⇒ dừng §7. |

Đo Windows trên **`DESKTOP-T9R33P2`** (ưu tiên, Q8 r1); VM `tra-luat-win` đo bổ sung. Base và head đo cùng một lượt.

## 6. `pham_vi_e`

Không chạm E4, E5. Không đảo quyết định "chỉ Linux" ⇒ không E3. Ca native chỉ giết tiến trình do chính ca sinh ra, qua handle/job của nó.

## 7. `luat_dung`

- Trần lời gọi Codex theo `ADR-0055`; trần vòng review theo `ADR-0048`. Chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- numstat vượt trần nâng 550 ⇒ dừng, revision đặc tả; **E2**.
- Cần sửa thân định nghĩa đang có, sửa ngoài write set, hoặc nối dây ⇒ dừng, revision đặc tả (protocol: thay đổi phạm vi sau đóng băng là revision mới).
- `Popen` trên máy đo không giữ con treo với `CREATE_SUSPENDED` (J6 đỏ trên head sạch, hoặc `ResumeThread` ≠ 1 trên J1) ⇒ dừng, revision đặc tả; không chuyển sang API không tài liệu.
- Máy đo Windows không có trong hạn lease ⇒ tiêu chí native `not_measured`; lease hết hạn theo protocol; gia hạn/cấp lại là quyết định chủ kho (**E2**).
- Đặc tả không thuộc Mission ⇒ chờ chủ kho duyệt băm (`ADR-0067`, **E2**) một lần sau khi review độc lập approve.

## 8. `hinh_dang_ke_thua` và ngân sách

`khong_ap_dung`. Ghi chú: hàm mới không decorator (r2 F2); additive dùng `_additive1342r2` (r2 F1); hook là tham số default `None`, chạy TRÊN đường mặc định, chỉ dùng trong ca test để quan sát/gây lỗi, không thay đường runtime (r3 F5); tiêu chí chỉ có lời khai ghi `not_measured` (Codex P1 PR #1398, #1403). Nợ có tên của revision này: `wp1342-pre-assign-orphan` (§2).

Ngân sách dòng (đếm theo hàm tương tự đo trên `e2c3b82`, gồm dòng trống; chưa phải numstat):

| khối | căn cứ | ước |
|---|---|---|
| hằng | 3 hằng + chú thích | 4–6 |
| `_1174_win_api_job` (12 bindings, 5 cấu trúc) | `_1174_win_api` 18 dòng/10 bindings + 5 lớp | 38–48 |
| 3 hàm thuần | | 22–28 |
| `_1174_win_job_empty` | | 13–16 |
| `_1174_win_spawn_job` | `_1174_process` 51, `_1174_win_seed` 62; thêm Toolhelp, last-error, 7 bước dọn có hậu điều, `add_note` | 95–115 |
| **mã** | | **172–213** |
| bindings phía test | 8 hàm | 12–16 |
| hạ tầng bắt tay + luồng quan sát + trợ giúp có giao thức | | 55–70 |
| S1–S5 tách assertion | | 45–55 |
| J0 ABI | | 18–24 |
| J1, J2, J3, J6, J7, J8, J9, J10, J10b, J11 | r3: 188 dòng test cho phạm vi đơn giản hơn | 120–150 |
| đăng ký ca | | 6–8 |
| **test** | | **256–323** |
| **tổng** | | **428–536 ≤ 550** |

## 9. Quyết định đã ghi

- **Q1.** Tách r1d → r1d-a (tiến trình) / r1d-b (probe) — chủ kho 2026-11-18. Tách tầng hai a1/a2 (chủ kho 2026-11-18). **Tách tầng ba a1-i/a1-ii (chủ kho 2026-11-18)**: a1-i = lõi vòng đời (revision này); a1-ii = breakaway tường minh/ngầm, job lồng.
- **Q2.** Đóng khe "chạy trước, gán sau" bằng `CREATE_SUSPENDED` + gán + `ResumeThread` (tìm luồng qua Toolhelp) — chủ kho 2026-11-18. `CreateProcessW` + `PROC_THREAD_ATTRIBUTE_JOB_LIST` bị bác vì kích thước ⇒ nợ `wp1342-pre-assign-orphan`.
- **Q3.** Cấm tuyệt đối breakaway: `LimitFlags == KILL_ON_JOB_CLOSE` — chủ kho 2026-11-18 (ca đo breakaway ở a1-ii).
- **Q4.** Job còn tiến trình sau khi kết thúc ⇒ `_1174Error`, fail-closed — chủ kho 2026-11-18.
- **Q5.** Nâng trần kích thước cho riêng revision này lên ≤ 2 tệp / ≤ 550 dòng thêm (thay `ADR-0053`) — chủ kho 2026-11-18, phiên điều phối #1206, qua AskUserQuestion; không tách thêm.

## 10. `chua_do_duoc`

- Kích thước thật (ước 428–536, §8).
- `Popen` + `CREATE_SUSPENDED` trên Python 3.13 Windows mới đọc mã, chưa chạy; sai thì §7.
- Các đường chỉ code review (§4b cuối).
- `GetProcessTimes` creation time có độ phân giải 100 ns; hai tiến trình khác nhau cùng pid và cùng creation time được coi là không xảy ra (chưa đo).
- Hằng số §0 trôi khi master tiến; đo lại theo L5.

## 11. Nhật ký review

- **Lượt 1** (bản r1d-a gộp transport; `request_changes` 2 P1, 7 P2, 1 P3): chủ kho tách a1/a2.
- **Lượt 2** (bản r1d-a1, sha256 `234b1804…`; `request_changes`: 2 P1 mới, P2 fixture/ABI/đột biến/N2/N3, P3): chủ kho tách a1-i/a1-ii và nâng trần 550. Bản này xử lý: P1 trước-gán ⇒ khai ranh giới + nợ `wp1342-pre-assign-orphan` + J10b; P1 đường thu hồi ⇒ đăng ký `kill_truoc_gan`/`reap` NGAY sau `Popen` trước mọi kiểm, bỏ `proc.kill()` sau gán, bước dọn tách hậu điều, kiểm `CloseHandle`, `add_note`, khai giới hạn ngắt bất đồng bộ, ghim CPython ≥ 3.11; P2 hook/handle/danh tính ⇒ creation time, `PROCESS_TERMINATE`, luồng quan sát, trợ giúp có giao thức, J9 thành viên thứ hai; P2 ABI ⇒ J0 + đột biến abi, `dwSize`, `Thread32First` lỗi, last-error ngay, `INVALID_HANDLE_VALUE` theo độ rộng con trỏ, `GetProcessIdOfThread == 0`, deadline hữu hạn; P2 đột biến ⇒ b bắt tay, c dấu hiệu S1, h bind đúng chữ ký, k2 có thành viên thứ hai, t2 tách vector; P2 N2 ⇒ AST + cấm trùng tên; N3 vế dương; P3 ⇒ giờ UTC thật, L5 ba mốc, M4 dẫn (9), §2 nhãn N4(f)(g) cũ. Chuyển sang a1-ii: J4, J5, J12, e1, e2.
