tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174-WINDOWS-BACKEND r4 — tiến trình con nhốt trong Job Object, Windows native, đứng riêng (bậc r1d-a), chưa nối vào runtime

- packet_id: WP1174-WINDOWS-BACKEND; revision: 4;

| trường | giá trị |
|---|---|
| `packet_issue` | #1342 |
| `nguon_cap_viec` | Lộ trình bậc ở §1 đặc tả r1 (bậc r1c gồm seed ACL, BootId, Job Object). Chủ kho chấp thuận ngày 17-11-2026 việc tách bậc này: seed và BootId vào r3 (land `aeb5cae`, hồ sơ `ops/land/pr1390-wp1342-land-evidence.yaml`, `landed: true`), tiến trình (Job Object) và probe sang **r1d** (§3 đặc tả r3). Chủ kho ngày 18-11-2026 (phiên điều phối #1206): "Làm tiếp #1342 r1d". Đặc tả này đề xuất tách r1d thành **r1d-a** (tiến trình, revision này) và **r1d-b** (probe, revision sau); xem §9 Q1. |
| `review_class` | `sensitive` (runtime trạng thái WP1174) |
| `base` | `e2c3b82f818bd1739d31261e8129d3ef44915acf` lúc soạn. Lease ghi OID base thật lúc cấp, và người cấp đo lại §0 trên base ấy. |

**Đánh số:** `revision: 4` là revision thứ tư của packet (ADR-0063 đòi số nguyên). Đây là bậc **r1d-a** của lộ trình, không phải bậc "r2" (nối dây) hay "r3" (mutator) trong bảng bậc của đặc tả r1.

## 0. Hiện trạng (đo 2026-11-18 trên `e2c3b82`; số dòng tính từ `def` tới dòng cuối thân, không gồm decorator)

| Linux | hàm (dòng) | bất biến |
|---|---|---|
| tiến trình có ranh giới | `_1174_process` 4260–4308 | Kiểm `deadline` còn hạn, `max_bytes` là `int` > 0, `stdin` là `None` hoặc `bytes` (sai ⇒ `_1174Error`). `stdin` phục vụ từ một `TemporaryFile` đã ghi trọn. `Popen(..., close_fds=True, start_new_session=True)`. Đọc hai pipe không chặn bằng `selectors`; tổng byte vượt `max_bytes` ⇒ "transport byte budget"; hết hạn ⇒ "transport deadline". Trong `finally` LUÔN `os.killpg(child.pid, SIGKILL)` (kể cả khi tiến trình đầu đã thoát mà hậu duệ còn giữ pipe), chờ, đóng pipe. `on_bytes` được gọi ĐÚNG MỘT LẦN với số byte thật đã đọc, ở mọi lối ra (tràn ⇒ `max_bytes+1`, lỗi trước khi đọc ⇒ `0`). Trả `CompletedProcess(argv, rc, stdout, stderr)`. |
| người gọi | `_1174_api` 4324–4350 (gọi 4341); `_1174_fetch_objects` (gọi 5619) | Không đổi ở r4. |
| probe | `_1174_probe` 4038–4073 | Thuộc r1d-b, ngoài r4. |

Các ca Linux đang khoá hợp đồng này nằm ở `.claude/dev/packet_loop_test.py` 13622–13636: hết hạn ngắt trong < 0,8 s; hậu duệ giữ pipe phải chết sau khi tiến trình đầu thoát; tràn byte. Có thêm `MUTANTS["m1174_transport_timeout"]` (13699) và `["m1174_transport_orphan"]` (13702). r4 không đụng các ca và mutant này.

Mẫu Windows trong kho: `.claude/dev/launcher.py` `_job_windows` 905–973 (`CreateJobObjectW`, `SetInformationJobObject` lớp 9 với `KILL_ON_JOB_CLOSE` `0x2000`, `OpenProcess`, `AssignProcessToJobObject`) và `_pid_trong_job` 976–1003 (`QueryInformationJobObject` lớp 3). Chú thích ở đó tự khai KHE HỞ: `Popen` gán job SAU khi con đã chạy, nên cháu sinh trong khoảng ấy nằm ngoài job. r4 đóng khe này (M2(c)).

r1–r3 đã có, đứng riêng, ở dòng 6406–6742 trên `e2c3b82`: `_1174_WIN_FIXED`, `_1174_win_path`, `_1174_win_platform`, `_1174_win_api`, `_1174_win_open`, `_1174_win_profile`, `_1174_win_identity`, `_1174_win_volume`, `_1174_win_read`, `_1174_win_api_ghi`, `_1174_win_lock`, `_1174_win_persist`, `_1174_win_api_bao_mat`, `_1174_win_seed_acl`, `_1174_win_seed`, `_1174_win_boot_id`. Test có `_new1342` 17879, `_additive1342` 17896, `_wired1342` 17920, `_native1342` (dấu hiệu `WP1342_NATIVE_V1`, 18165), `_additive1342r2` 18178. Chốt không-nối-dây `_wired1342` (ca `wp1342_additive_byte_preserved`, chạy trên CÂY LÀM VIỆC) phủ mọi khối mới `def _1174_win_*` không decorator, default là hằng.

Kích thước: r1 +428, r2 và r3 đều dưới trần (hồ sơ land). Ước lượng r4 (tĩnh, chưa đo): mã ~100–130, test ~170–230, tổng ~270–360 dòng thêm. Nếu gộp cả probe (r1d-b) thì ước ~420–520, vượt hoặc sát trần; đó là lý do đề xuất tách (§9 Q1). Đo numstat thật; vượt trần thì theo §7, không cắt assertion hay cleanup để ép số dòng.

## 1. Phạm vi r4

Thêm, ĐỨNG RIÊNG (không hàm hiện có nào gọi tới):
- bindings Job/thread;
- `_1174_win_process` cùng hợp đồng với `_1174_process`, trong đó tiến trình con được gán vào Job Object TRƯỚC khi chạy lệnh đầu tiên;
- ca test thuần (Linux) và native (Windows).

Không sửa thân định nghĩa nào đang có, kể cả các hàm `_1174_win_*` của r1–r3.

## 2. `write_set`

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
```

## 3. `ngoai_pham_vi`

- Không sửa thân hàm/khối nào đang có, kể cả `_1174_process`, `_1174_win_*` của r1–r3, và các helper test `_new1342`, `_additive1342`, `_wired1342`, `_additive1342r2`, `_native1342`.
- Không probe (r1d-b); không nối dây (bậc sau).
- Không dùng API không có tài liệu (`NtResumeProcess`, `NtSuspendProcess`); không `pywin32`; không đồ giả Win32 trên Linux (Q11 của r1).
- Không cho phép `JOB_OBJECT_LIMIT_BREAKAWAY_OK` hay `SILENT_BREAKAWAY_OK`: hậu duệ không được tách khỏi job.
- Không giới hạn CPU, bộ nhớ hay số tiến trình của job (chỉ giới hạn vòng đời).
- Không đổi `MUTANTS`; không thêm runner; không CI Windows.

## 4. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Hàm MỚI `_1174_win_api_job()`: gọi `_1174_win_api()`, rồi bind với argtypes/restype tường minh trên CÙNG đối tượng `kernel32`: `CreateJobObjectW`, `SetInformationJobObject`, `AssignProcessToJobObject`, `TerminateJobObject`, `QueryInformationJobObject`, `CreateToolhelp32Snapshot`, `Thread32First`, `Thread32Next`, `OpenThread`, `ResumeThread`, `GetHandleInformation`. Khai cấu trúc `JOBOBJECT_EXTENDED_LIMIT_INFORMATION` (kèm `JOBOBJECT_BASIC_LIMIT_INFORMATION`, `IO_COUNTERS`), `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION` và `THREADENTRY32`. Không bind API ngoài tập này. Trả các đối tượng cần dùng. | `.claude/dev/packet_loop.py` |
| M2 | `_1174_win_process(argv, *, cwd, deadline, max_bytes, env=None, on_bytes=None, stdin=None, between=None)`, cùng hợp đồng với `_1174_process` (§0) cộng các bước sau. (a) Kiểm đối số ĐÚNG như Linux: `deadline` còn hạn, `type(max_bytes) is int` và > 0, `stdin` là `None` hoặc `bytes`. Sau đó mới đòi `os.name == "nt"` ("native Windows required"). Vi phạm ⇒ `_1174Error`; `on_bytes(0)` vẫn được gọi đúng một lần. (b) Tạo job với security attributes mặc định (handle KHÔNG kế thừa). Đặt `LimitFlags` CHỈ gồm `KILL_ON_JOB_CLOSE` (`0x2000`); không cờ breakaway. (c) `Popen(argv, cwd, env, stdin=<TemporaryFile>, stdout=PIPE, stderr=PIPE, close_fds=True, creationflags=CREATE_SUSPENDED (0x4) \| CREATE_NEW_PROCESS_GROUP (0x200))`. Rồi `AssignProcessToJobObject(job, process handle)`. Gán thất bại ⇒ kết thúc tiến trình đang treo và `_1174Error` "job assignment". Gán xong mới tìm luồng của tiến trình qua `CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD)`: phải có ĐÚNG MỘT luồng với `th32OwnerProcessID == pid`; mở bằng `THREAD_SUSPEND_RESUME`; `ResumeThread` phải trả `1` (đếm treo cũ); khác ⇒ kết thúc và `_1174Error` "suspended start". Mọi handle snapshot/thread đóng trong `finally`. `between(job)` là hook kiểm thử, chạy SAU gán và TRƯỚC resume (khuôn `between` của `_1174_win_read`/`_1174_win_seed`). (d) Đọc hai pipe bằng hai luồng nền: mỗi lần đọc tối đa 65536 byte; cộng dồn dưới một khoá chung; dừng khi EOF. Luồng chính chờ tới khi cả hai luồng xong và tiến trình đầu thoát. Mỗi vòng chờ ≤ 0,1 s kiểm `deadline` ("transport deadline") và tổng byte ≤ `max_bytes` ("transport byte budget"); tổng thật được ghi để báo `on_bytes` đúng như Linux (tràn ⇒ `max_bytes+1`). (e) `finally`: LUÔN `TerminateJobObject(job, 1)`, kể cả khi tiến trình đầu đã thoát mà hậu duệ còn sống. Sau đó đòi `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION.ActiveProcesses == 0` (lớp 1), thử lại tới 5 s; còn khác 0 ⇒ `_1174Error` "job not empty". Chờ luồng đọc (có timeout), đóng pipe, `CloseHandle(job)`. (f) Trả `CompletedProcess(argv, rc, stdout, stderr)`. | `.claude/dev/packet_loop.py` |
| M3 | Ca THUẦN (mọi nền), ID `wp1342_pure_process_refuse`. Với từng đối số sai (`deadline` đã qua; `max_bytes` = `0`, `-1`, `True`, `1.0`, `"8"`; `stdin` = `"x"`, `bytearray(b"x")`): `_1174_win_process` từ chối với đúng lý do của Linux, và `on_bytes` ghi đúng `[0]`. Trên nền khác Windows, đối số hợp lệ ⇒ "native Windows required", `on_bytes == [0]`. Không thêm vào `WP1174_REQUIRED`/`WP1174_BOTH`. | `.claude/dev/packet_loop_test.py` |
| M4 | Ca NATIVE (Windows; nền khác in `BỎ QUA <lý do>`, không tính đạt), qua `_native1342`, dấu hiệu `WP1342_NATIVE_V1`, ID `wp1342_native_proc_*`. Lệnh con là `sys.executable -B -c …`. **P1** stdout/stderr/rc đúng bytes; `on_bytes` = tổng đúng. **P2** `stdin` 100 KiB được con đọc đủ, băm khớp; con KHÔNG đọc stdin vẫn thoát, không chặn. **P3** con `sleep(30)`, deadline +0,5 s ⇒ "transport deadline" trong < 5 s; pid con đã chết (`OpenProcess` + `GetExitCodeProcess` ≠ `STILL_ACTIVE` 259, hoặc không mở được); `ActiveProcesses == 0`. **P4** in 4096 byte, `max_bytes=128` ⇒ "transport byte budget", `on_bytes == [129]`. **P5 (mồ côi)** con sinh cháu bằng `subprocess.Popen` với `DETACHED_PROCESS` (`0x8`), cháu `sleep(30)` và giữ một tệp mở; con ghi pid cháu ra tệp rồi THOÁT NGAY, `rc == 0`. Sau khi `_1174_win_process` trả về, cháu phải đã chết (cùng phép của P3). **P6 (breakaway)** con thử sinh cháu với `CREATE_BREAKAWAY_FROM_JOB` (`0x01000000`) và in kết quả. Đạt khi lời sinh bị từ chối (`OSError`, `ERROR_ACCESS_DENIED` 5), HOẶC sinh được nhưng sau khi hàm trả về cháu đã chết. Cháu sống sót ⇒ ĐỎ. **P7 (treo trước gán)** `between(job)`: (i) `GetHandleInformation(job)` không có `HANDLE_FLAG_INHERIT`; (ii) con chưa chạy dòng đầu tiên: con ghi một tệp đánh dấu ngay khi khởi động, và ở thời điểm `between` tệp ấy CHƯA tồn tại; hàm trả về rồi thì tệp CÓ. Không dựng được điều kiện ⇒ `KHÔNG ĐO ĐƯỢC`, không in đạt. | `.claude/dev/packet_loop_test.py` |
| M5 | Đột biến qua driver NGOÀI kho, theo khuôn r1–r3: mỗi cặp (tìm, thay) khớp đúng một chỗ, chạy trên bản sao tạm, có ca đích và ca đối chứng khoẻ, lỗi import/fixture ⇒ `KHÔNG ĐO`. Đột biến Windows: **(a)** bỏ `KILL_ON_JOB_CLOSE` VÀ bỏ `TerminateJobObject` (giữ kiểm `ActiveProcesses`) ⇒ P5 ĐỎ, tại "job not empty" hoặc tại "cháu còn sống"; **(b)** dời `ResumeThread` lên TRƯỚC `AssignProcessToJobObject`, kèm `time.sleep(0.5)` giữa hai bước ⇒ P7 ĐỎ (tệp đánh dấu đã có lúc `between`) và/hoặc P5 ĐỎ; **(c)** bỏ cờ `CREATE_SUSPENDED` ⇒ P7 ĐỎ, hoặc ĐỎ tại "suspended start"; **(d)** bỏ kiểm `deadline` trong vòng chờ ⇒ P3 ĐỎ ("< 5 s"); **(e)** thêm `0x800` (`BREAKAWAY_OK`) vào `LimitFlags` ⇒ P6 ĐỎ. Đột biến THUẦN (chạy trên Linux bằng cùng driver): **(f)** bỏ vế `max_bytes>0` ⇒ `wp1342_pure_process_refuse` ĐỎ tại dòng `0`; **(g)** đưa `os.name == "nt"` lên TRƯỚC kiểm đối số ⇒ ĐỎ tại dòng đầu tiên (trên Linux lý do đổi sang "native Windows required"). | `.claude/dev/packet_loop_test.py` (ca đích) |

## 4b. Đường vào và chốt (mỗi đường một chốt riêng, có đột biến phân biệt)

| đường để một tiến trình sống ngoài vòng đời của lời gọi | chốt | ca | đột biến |
|---|---|---|---|
| con thoát, cháu mồ côi còn sống | job + `TerminateJobObject` + `KILL_ON_JOB_CLOSE` | P5 | (a) |
| cháu sinh trong khe "chạy trước, gán sau" | `CREATE_SUSPENDED` + gán trước resume | P7, P5 | (b), (c) |
| cháu xin breakaway | KHÔNG đặt cờ breakaway (danh sách cho phép: `LimitFlags == 0x2000`) | P6 | (e) |
| treo vô hạn | kiểm `deadline` mỗi ≤ 0,1 s | P3 | (d) |
| tràn byte | kiểm tổng byte | P4 | (không thêm mutant: nằm trong bảng N8 nếu review đòi) |
| đối số sai lọt vào Windows | kiểm đối số trước nền | ca thuần | (f), (g) |

## 5. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Linux không đổi: CI Ubuntu exact head, gom `GOM: ĐẠT · 16 mảnh · <n> ca`; mọi ca `wp1174_*`, `wp1342_*` đang có đạt theo tính áp dụng; `MUTANTS` ở head bằng CHÍNH XÁC base (cùng tập khoá, cùng giá trị). | Một ca đỏ; đổi tên một khoá `MUTANTS` mà giữ nguyên số lượng ⇒ phép so ĐỎ. |
| N2 | Chỉ THÊM. Đo một lần trên PR bằng `_additive1342r2(<blob base>, <blob head>)` ⇒ `[]`. Executor ghi lệnh và kết quả vào thân PR; phiên điều phối đo lại, kèm phản chứng chạy thật (bài học Codex P1, PR #1403). | Sửa một byte thân hàm r1/r2/r3 ⇒ khác `[]`; thêm decorator vào hàm mới ⇒ khác `[]`. |
| N3 | Không nối dây: `wp1342_additive_byte_preserved` (vế N3, trên cây làm việc) đạt. | Thêm lời gọi `_1174_win_process` trong `_1174_process` ⇒ ca ĐỎ. |
| N4 | M3 đạt trên Linux (CI) và Windows (Desktop). | Đột biến (f), (g) ⇒ ĐỎ đúng dòng. |
| N5 | Windows vẫn bị từ chối, không đổi: `wp1174_windows_claim_rejected` và 12 ca `WP1174_BOTH` đạt y hệt base; ca native r1–r3 vẫn đạt. | Một ca lệch base. |
| N6 | Ca native M4 (P1–P7) đạt trên Desktop, mỗi ca có dấu hiệu dương. P5 và P6 chạy thêm trên VM `tra-luat-win`. | Ca native in `BỎ QUA` trên Windows ⇒ ĐỎ; cháu sống sót ⇒ ĐỎ. |
| N7 | Năm đột biến Windows (a)–(e) bị giết đúng ca đích trên Desktop; (f), (g) bị giết trên Linux. Theo hợp đồng N7 của r1: driver byte-exact trong hồ sơ land; chỉ tính giết khi assertion hành vi của ca đích thất bại và đối chứng đạt; chuỗi không khớp ⇒ `KHÔNG ĐO`. | Đột biến SỐNG, hoặc ca "đỏ" vì lỗi import/fixture. |
| N8 | Ruff `--select F` delta 0 trên hai tệp; `adr-song`, `doctrine-scan` rc 0; `git diff --check` sạch; `eol_policy --all` ok; numstat ≤ 2 tệp và ≤ 450 dòng thêm (`ADR-0053`). | Một cổng thất bại ⇒ ĐỎ; vượt trần ⇒ dừng theo §7. |

Đo Windows (N4 phần Windows, N5, N6, N7 phần Windows) trên **`DESKTOP-T9R33P2`** (ưu tiên, Q8 của r1). VM `tra-luat-win` là dự phòng và đo bổ sung P5/P6. Base và head đo trong cùng một lượt.

## 6. `pham_vi_e`

Không chạm E4, không chạm E5. Không đảo quyết định "chỉ Linux" (primitive chưa nối dây), nên không có E3. Ca native chỉ giết tiến trình do chính ca sinh ra, thông qua job của nó; không giết tiến trình nào khác trên máy đo.

## 7. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`; trần vòng review theo `ADR-0048` và protocol. Chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- `git diff --numstat` vượt `ADR-0053` ⇒ dừng; câu hỏi mang **E2**.
- Cần sửa thân một định nghĩa đang có, sửa ngoài write set, hoặc nối dây để một tiêu chí đạt ⇒ dừng triển khai và làm revision đặc tả. Chỉ hỏi **E1** khi không còn phương án có phép đo chống đỡ; thiếu quyền ⇒ **E2**.
- Nếu `Popen` của bản Python trên máy đo không chạy được với `CREATE_SUSPENDED` (con chạy luôn, hoặc không tìm được đúng một luồng) ⇒ dừng; không chuyển sang API không có tài liệu; làm revision đặc tả (ví dụ `CreateProcessW` trực tiếp, kích thước lớn hơn).
- Desktop và VM cùng offline quá hạn lease ⇒ **E2**.
- Đặc tả không thuộc Mission nên phải chờ chủ kho duyệt băm theo `ADR-0067` — **E2**, một lần, sau khi review độc lập approve.

## 8. `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục. Ghi chú từ r1–r3 (không phải bộ đếm lỗi):
- Hàm mới không decorator, vì `_new1342` bỏ qua khối có decorator (r2 F2).
- Phép so additive dùng `_additive1342r2` (r2 F1).
- Hook kiểm thử là tham số `between=None` có default hằng, không phải seam bỏ qua mã runtime (r3 F5: seam `doc=` đã bị bác vì bỏ qua đường mặc định).
- Bài học hồ sơ land 18-11 (Codex P1 trên PR #1398 và #1403): tiêu chí nào chỉ có lời khai thì ghi `not_measured`, không ghi `passed`.

## 9. Câu hỏi cho chủ kho (trước khi duyệt băm)

- **Q1. Tách r1d thành r1d-a (Job Object, đặc tả này) và r1d-b (probe, revision sau)?** *Khuyến nghị: có.* Gộp cả hai ước ~420–520 dòng, vượt hoặc sát trần `ADR-0053`; r2/r3 đều sát trần. Probe Windows còn cần quyết định riêng: probe đo những mục nào; tranh chấp khoá giữa hai tiến trình đo bằng gì trên Windows; và `eligible` luôn `False` cho tới khi có ADR (Q10 của r1). Tách ra thì mỗi phần review gọn hơn.
- **Q2. Đóng khe "chạy trước, gán job sau" bằng `CREATE_SUSPENDED` + gán + `ResumeThread` (tìm luồng qua Toolhelp)?** *Khuyến nghị: có.* Đây là cách duy nhất dùng API có tài liệu mà vẫn giữ được `subprocess.Popen`. Mẫu `launcher.py` tự khai khe này còn hở. Cách khác là gọi `CreateProcessW` trực tiếp kèm `PROC_THREAD_ATTRIBUTE_JOB_LIST`: kín hơn nhưng thêm ~80–120 dòng và phải tự dựng pipe, vượt trần. Nếu chủ kho chấp nhận khe hở như launcher thì bỏ M2(c), P7 và đột biến (b), (c), giảm ~40 dòng.
- **Q3. Cấm tuyệt đối breakaway (P6)?** *Khuyến nghị: có.* Danh sách cho phép `LimitFlags == KILL_ON_JOB_CLOSE`; hậu duệ nào xin breakaway sẽ bị từ chối. Linux không có khái niệm tương đương, vì `killpg` chỉ giết đúng nhóm.
- **Q4. Lỗi "job not empty" sau `TerminateJobObject` là `_1174Error` (fail-closed), không chỉ cảnh báo?** *Khuyến nghị: có.* Cùng nguyên tắc với Linux: không chứng minh được đã dọn sạch thì không báo thành công.

## 10. `chua_do_duoc`

- Kích thước thật: ước tĩnh ~270–360 dòng thêm; vượt trần thì theo §7.
- `Popen` + `CREATE_SUSPENDED` trên Python 3.13 Windows: thiết kế dựa trên việc `Popen` truyền `creationflags` nguyên vẹn và không tự resume. Chưa chạy thử trên Desktop/VM; nếu sai thì theo §7.
- Job lồng nhau: nếu chính tiến trình Python đã nằm trong một job không cho breakaway (vd dịch vụ, Desktop Commander), việc gán vào job mới chỉ được bảo đảm từ Windows 8. Máy đo là Windows 10/11; chưa đo khi tiến trình cha đã ở trong job.
- P6: Windows có thể từ chối lời sinh breakaway bằng mã khác 5 tuỳ phiên bản; ca nhận mọi `OSError`, miễn cháu không sống sót.
- Ca native chỉ chạy được trên Windows; các hằng số của §0 sẽ trôi khi master tiến, người cấp lease đo lại.

**Trả lời của chủ kho (2026-11-18, phiên điều phối #1206, qua AskUserQuestion):** Q1 có — tách r1d thành r1d-a (Job
Object, đặc tả này) và r1d-b (probe, revision sau); Q2 `CREATE_SUSPENDED` + gán job + `ResumeThread` (tìm luồng qua
Toolhelp); Q3 cấm tuyệt đối breakaway (`LimitFlags == KILL_ON_JOB_CLOSE`); Q4 job còn tiến trình sau khi kết thúc ⇒
`_1174Error`, fail-closed.
