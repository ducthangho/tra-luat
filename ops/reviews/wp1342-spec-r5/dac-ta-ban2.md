tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# WP1174-WINDOWS-BACKEND r5 — kháng thoát job: breakaway tường minh, breakaway ngầm, job lồng (bậc r1d-a1-ii), CHỈ phép đo, chưa nối vào runtime

- packet_id: WP1174-WINDOWS-BACKEND; revision: 5;

| trường | giá trị |
|---|---|
| `packet_issue` | #1342 |
| `nguon_cap_viec` | Lộ trình bậc ở §1 đặc tả r1. Đặc tả r4 (`ops/specs/WP1174-WINDOWS-BACKEND-r4.md` trên `origin/ops/wp1342-r4-spec`, sha256 `f435eb5c…1eb8`) §2 "Để r1d-a1-ii" và §9 Q1 (chủ kho 2026-11-18: a1 → a1-i / a1-ii; a1-ii = breakaway tường minh/ngầm, job lồng). r4 land `a2c7d75` (PR #1407, hồ sơ `ops/land/pr1407-wp1342-land-evidence.yaml`, `landed: true`). Comment chủ kho Issue #1342 `issuecomment-6999134364` (2026-11-19T03:51Z): "r1d-a1-ii: kháng thoát job (breakaway tường minh, breakaway ngầm, job lồng)", mỗi phần đặc tả và review riêng. |
| `review_class` | `sensitive` (`.claude/dev/packet_loop_test.py` không có trong `_BANG_LOP` của `ops/lease_publish.py` ⇒ fail-closed `sensitive`; phạm vi là phép đo của runtime trạng thái WP1174) |
| `base` | `4eda94e9effc6cfe7fcc0b3e3fb4151ad437ecbd` (tree `ceba0869d378f6c326955e4e1920a9776ba1a0a7`; master lúc 2026-11-19T10:21Z). Số đo §0 lấy 2026-11-19T09:4xZ–10:2xZ: phần lớn trên `11bd033` (bản 1), rồi xác nhận lại trên `4eda94e` — `git diff --stat 11bd033 4eda94e` chỉ 1 tệp ngoài `.claude/dev/` (7+/7−), blob hai tệp của write set GIỐNG HỆT. L5: người cấp lease đo lại §0 trên OID base thật (1) trước khi công bố băm, (2) lúc cấp lease, (3) trước merge; lệch ⇒ revision đặc tả. |

**Đánh số:** `revision: 5` (ADR-0063, số nguyên); bậc **r1d-a1-ii**. r1d-a2 (transport hai pipe) và r1d-b (probe) là các revision sau.

## 0. Hiện trạng (đo trên `11bd033`, xác nhận trên base `4eda94e`)

Lệnh trong clone `git worktree add --detach … origin/master` (ref vừa `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`, kho không shallow; lúc 09:4xZ `comm -23` tập nhánh máy chủ/đệm = 0 dòng, 339 nhánh; lúc 10:21Z `git ls-remote --heads origin` = 339 dòng. Đây là ảnh chụp lúc soạn; reviewer lượt 1 đếm 340 ref cục bộ — lệch do thời điểm/`HEAD`, không phải bằng chứng); mọi lệnh rc 0 trừ chỗ ghi.

- `git diff --numstat a2c7d75 11bd033 -- .claude/dev/packet_loop.py .claude/dev/packet_loop_test.py` ⇒ RỖNG (và `git rev-parse 4eda94e:<tệp>` ra cùng hai blob dưới đây): hai tệp không đổi từ merge r4. `git merge-base --is-ancestor a2c7d75 11bd033` rc 0. Blob: `packet_loop.py` `f98d3f53e638518790def1f22d78e82623451d41` (7239 dòng), `packet_loop_test.py` `c1ec1c69a7a476689d10ddb60d4e12c092e1f7a3` (18937 dòng).
- `packet_loop.py`: r4 đứng riêng ở 6745–6912: `_1174_WIN_JOB_LIMIT = 0x2000` 6745 (dòng `_1174_WIN_JOB_LIMIT = 0x2000   # JOBOBJECT LimitFlags: KILL_ON_JOB_CLOSE and nothing else (no breakaway bit)` — cùng neo với đột biến a2 của r4), `_1174_win_api_job` 6750 (12 bindings, KHÔNG có `IsProcessInJob`), `_1174_win_spawn_job` 6830. Job tạo bằng `CreateJobObjectW(None, None)`, `LimitFlags = _1174_WIN_JOB_LIMIT`, gán TRƯỚC resume; thu hồi bằng `terminate` + `xac_nhan` (§4 r4).
- `packet_loop_test.py`: khối r4 18560–18934. Hạ tầng dùng lại được (KHÔNG sửa): `_wp1342a1_FX` 18634 (fixture; bước `bt` `cho` `cho0` `ra` `chau` `tro_a` `tro_b`; **bước lạ bị BỎ QUA im lặng** — vòng `for b in buoc` không có nhánh `else`), `_wp1342a1_lenh` 18665, `_wp1342a1_tin` 18669, `_wp1342a1_mo` 18673 (bắt tay: đòi nonce, creation time và `WaitForSingleObject(h, 0) == 258`; 20 dòng vật lý `def`→`return`), `_wp1342a1_ban_sao` 18695, `_wp1342a1_goi` 18702 (luồng quan sát + bàn giao handle; dùng `x.m`, mặc định `han=60`, `join(20)`), `_wp1342a1_ca` 18737 (khung ca: cửa sổ 90 s CHỈ kiểm SAU khi thân ca và dọn xong — không tự cắt các bước chờ, `loi_*`/`het_han_*`/`tu_ket_thuc` ⇒ `KHÔNG ĐO`; ghi `_wp1342a1_FX` ra `d/fx.py`), `_wp1342a1_phu` 18760, `_wp1342a1_giet_cha` 18767. `_native1342` 18159. `_module1174(c)` 10647 nạp một module MỚI mỗi lần gọi (`spec_from_file_location` tên `pl1174_<time_ns>`), nên sửa thuộc tính của một bản nạp không chạm bản nạp khác. Đăng ký r4: `CASES += [...]` 18923 (3 ca thuần) và 18924–18933 (11 ca native); `if __name__ == "__main__"` 18936. `MUTANTS` 3592.
- Numstat r4 (`d59527f..a2c7d75`): `packet_loop.py` +172/-0, `packet_loop_test.py` +376/-0.
- Dòng khai trần: ADR-0053 `8ab1007…` và ADR-0055 `d2e3052…` — mỗi OID: `git cat-file -e <L>:<adr>` rc 0, `git cat-file -e <L>^1:<adr>` rc 128, `git rev-list --first-parent origin/master | grep -xc <L>` = 1 trên `4eda94e`.
- Lease chạm write set: quét `ops/leases/*.yaml` trên mọi `refs/remotes/origin/ops/*` (script tạm, regex dòng `lease_until`/`lease_expires_at_utc`/`expires_at`) tìm lease nhắc `packet_loop` hết hạn sau 2026-11-19T10Z ⇒ **0** lease (giới hạn: chỉ nhánh `ops/*`, chỉ ba tên trường ấy; lệnh `ai-dang-giu` chạy trên kho chính bị `CHAN [12]` vì nhánh cục bộ `master` tụt sau — không đo được bằng lệnh ấy trong phiên soạn; người cấp lease đo lại theo L5).
- Máy đo r4 (hồ sơ land pr1407): Desktop `DESKTOP-T9R33P2` Windows 11 NT 10.0.26300, Python 3.12.10; VM `tra-luat-win` Windows Server 2022 (20348). Tiến trình chạy ca trên hai máy ấy có nằm sẵn trong một job hay không: CHƯA ĐO (§10).
- Bộ kiểm N2 của r4 (`ops/land/pr1407-wp1342-provenance/linux/n2_test_r4.py`, 196 dòng) sau `sed 's/_wp1342a1_/_wp1342a1ii_/g'` (đổi hằng tiền tố VÀ tên trong phản chứng/đối chứng dương), chạy `base_r5 base_r5` (blob `c1ec1c69`): 16/16 phản chứng ĐỎ đúng vế, đối chứng dương `[]`. Hai phản chứng mới (chèn trước `if __name__`): `_wp1342a1_FX = _wp1342a1_FX + "x"` ⇒ ĐỎ (iv) + (ii) ("1 điểm bind ở base, 2 ở head"); mục native ID `wp1342_native_job_thuan` (ID r4) ⇒ ĐỎ (iv). Một khối mô phỏng r5 (`_wp1342a1ii_FX = _wp1342a1_FX + ("…")`, `def _wp1342a1ii_s6` có `import ast` cục bộ + `ast.parse`, một ca native, hai câu `CASES +=`) ⇒ `[]`; cùng khối mà S6 gọi `compile(...)` ⇒ ĐỎ "(iv) tên cấm `compile`".
- Hành vi Win32 dùng làm căn cứ (tài liệu Microsoft theo trí nhớ người soạn và reviewer lượt 1, CHƯA tra lại, CHƯA đo trong kho): `CREATE_BREAKAWAY_FROM_JOB` = `0x01000000`; tiến trình trong job không có `JOB_OBJECT_LIMIT_BREAKAWAY_OK` (`0x800`) gọi `CreateProcess` với cờ ấy thì thất bại `ERROR_ACCESS_DENIED` (5); `JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK` (`0x1000`) cho con tự động rời JOB MANG CỜ ẤY — trong chuỗi lồng, việc rời các job tổ tiên phụ thuộc cờ của từng tổ tiên; breakaway được xét THEO TỪNG JOB trong chuỗi; từ Windows 8 job lồng nhau được hỗ trợ nhưng phép gán vẫn có thể bị từ chối; `IsProcessInJob(process, job, &result)` cần `PROCESS_QUERY_INFORMATION` HOẶC `PROCESS_QUERY_LIMITED_INFORMATION` trên tiến trình và `JOB_OBJECT_QUERY` trên job. Vì chuỗi job tổ tiên của tiến trình chạy ca KHÔNG đọc được bằng API có tài liệu, đối chứng của J4 phải đi qua CHÍNH đường sản phẩm từ CHÍNH tiến trình chạy ca (M2), không qua một tiến trình khác tự gán job.

## 1. Phạm vi r5 (r1d-a1-ii)

CHỈ THÊM phép đo vào `packet_loop_test.py`: ba ca native (J4 breakaway tường minh, J5 breakaway ngầm, J12 job lồng), một ca thuần (S6, cú pháp fixture mở rộng), phần mở rộng fixture dựng bằng cộng chuỗi trên `_wp1342a1_FX`. `packet_loop.py` KHÔNG đổi một byte: Q3 ("cấm tuyệt đối breakaway", `LimitFlags == KILL_ON_JOB_CLOSE`) đã nằm trong mã r4; r5 đo rằng nó có răng trên Windows thật. Không sửa thân định nghĩa nào đang có.

## 2. `write_set`, `ngoai_pham_vi`, ranh giới

```
.claude/dev/packet_loop_test.py
```

Ngoài phạm vi:
- `.claude/dev/packet_loop.py` (mọi byte giữ nguyên; đột biến e1/e2 chỉ chạy trên BẢN SAO TẠM qua driver ngoài kho). Không bind `IsProcessInJob` trong mã sản phẩm (allowlist M1 r4 và J0 khoá đúng 12 tên); binding ấy chỉ ở phía test.
- Không sửa thân hàm/khối nào đang có trong tệp test, kể cả `_wp1342a1_FX`, `_wp1342a1_ca`, `_wp1342a1_goi`, `_native1342`; không gán lại tên base nào. Không đổi `MUTANTS`; không runner mới; không CI Windows; không vào `WP1174_REQUIRED`/`WP1174_BOTH`.
- Không thêm kiểm runtime trong `_1174_win_spawn_job` (vd đọc lại `LimitFlags`, `IsProcessInJob` sau gán): sửa thân hàm r4 là đổi phạm vi ⇒ revision mới (§7).
- **Để r1d-a2:** hai pipe, hạn mức byte, `on_bytes`, `stdin` bytes, CRLF/NUL. **Để r1d-b:** probe. Không nối dây.
- Không API không tài liệu, không `pywin32`, không đồ giả Win32.

Ranh giới bảo đảm: không đổi so với r4 §2 (gồm nợ `wp1342-pre-assign-orphan`). r5 thêm hai câu được ĐO: (a) hậu duệ trong job đích xin breakaway tường minh bị từ chối (J4); (b) hậu duệ sinh bình thường nằm trong job đích (J5). Job lồng (J12) là năng lực CÓ ĐIỀU KIỆN: ca ghi nhánh xảy ra, mỗi nhánh có hậu điều riêng; không khẳng định nhánh nào là bảo đảm. Ngoài bảo đảm như r4: tiến trình do dịch vụ ngoài job tạo thay mặt con (COM/WMI/Task Scheduler).

## 3. Hằng số

Không hằng sản phẩm mới. Hằng phía test (giá trị literal trong ca, mỗi chỗ một lần): `0x01000000` (`CREATE_BREAKAWAY_FROM_JOB`), `0x2800` (đặt vào `_1174_WIN_JOB_LIMIT` của bản nạp riêng cho đối chứng (ii) J4: `KILL_ON_JOB_CLOSE | BREAKAWAY_OK`; đúng MỘT lần trong tệp), `0x2000` (job ngoài J12), tập mã từ chối cho phép `{5}`.

## 4. `muc_tieu` (mọi mục chiếu vào `.claude/dev/packet_loop_test.py`)

| # | mục tiêu |
|---|---|
| M1 | **Fixture mở rộng** `_wp1342a1ii_FX = _wp1342a1_FX + "<nhánh mới>"` (cộng chuỗi; `_wp1342a1_FX` không bị gán lại). Phần thêm là các nhánh `elif` nối tiếp chuỗi `if/elif` của vòng `for b in buoc`, cộng binding `IsProcessInJob([c_void_p, c_void_p, POINTER(c_int)], c_int)` trên `k` của fixture. Ba bước mới, mỗi bước LUÔN để lại tệp kết quả (ghi tạm + `os.replace`, như `ghi`) để bước bị bỏ qua im lặng (§0) lộ thành thiếu tệp ⇒ `KHÔNG ĐO`: **`tach=<cờ>,<vai>,<việc>`**: như `chau` nhưng `Popen` nằm trong `try`; `OSError` ⇒ tệp `tach_<vai>` = `["loi", winerror]`; thành công ⇒ `["ok", pid]`; lỗi khác lan ra (excepthook ⇒ `loi_<vai>` ⇒ `KHÔNG ĐO`). **`vao_job=<LimitFlags>,<đường packet_loop.py>`** (CHỈ J12 dùng): nạp module từ đường dẫn (như `tro_a`), dùng `_1174_win_api_job()` tạo job, `SetInformationJobObject(job, 9, …)` với `LimitFlags` cho trước, rồi `AssignProcessToJobObject(job, GetCurrentProcess())`; giữ handle job tới khi tiến trình thoát; tệp `job_ngoai` = `["ok"]` hoặc `["loi", <bước>, <mã Win32 đọc ngay>]` và khi lỗi thì `sys.exit(0)` (không chạy bước sau). **`tro_c=<đường packet_loop.py>`** (trợ giúp J12, sau `vao_job`): ghi bắt tay `san_sang`; gọi `_1174_win_spawn_job(con, cwd=d, deadline=now+300, truoc_gan, between)` với `truoc_gan(proc)`: giữ `proc`, ghi bắt tay `truoc_gan` (pid + creation time con qua `proc._handle`) rồi `cho('go_truoc_gan', 300)`; `between(job)`: ghi tệp `long` = `[ok1, trong, ok2, ngoai]` từ `IsProcessInJob(proc._handle, job)` và `IsProcessInJob(proc._handle, <job của vao_job>)`; sau lời gọi (bắt `Exception`): tệp `ket_qua` = `["ok", rc]` hoặc `["loi", str(lỗi)]`; rồi `cho('tha_tro_giup', 300)` (hết hạn ⇒ `het_han_tro_giup` ⇒ `KHÔNG ĐO`); KHÔNG ghi `tu_ket_thuc`. Hàm phía test đọc tệp kết quả JSON có hạn và KIỂM SCHEMA trước khi chấm (tệp vắng trong hạn, JSON hỏng, sai số phần tử/kiểu, hay một lời gọi Win32 phía fixture báo FALSE ⇒ `KHÔNG ĐO` nêu tên tệp/bước và mã Win32; KHÔNG BAO GIỜ gộp vào nhãn ĐỎ của sản phẩm). **Hạn chung mỗi ca**: thân ca lấy `het = time.monotonic() + 75` ở dòng đầu (trước fixture đầu tiên của nó; khung r4 tự đo 90 s từ sớm hơn một chút); MỌI bước chờ của r5 (đọc tệp, bắt tay `_wp1342a1_mo(han=…)`, chờ tiến trình, lời gọi `_wp1342a1_goi(han=…)`) nhận `min(hạn riêng, het - now - dự phòng)`, với dự phòng 30 s cho lời gọi `_wp1342a1_goi` (bù `join(20)` + các wait 5 s) và 10 s cho bước khác; phần còn lại ≤ 0 ⇒ `KHÔNG ĐO` ghi tên mốc đang chờ. Lượt `KHÔNG ĐO` vì cạn hạn không bao giờ được tính là đột biến bị giết. Kiểm "tiến trình CHƯA signaled" dùng giá trị THÔ `WaitForSingleObject(h, 0) == 258` (WAIT_TIMEOUT); `WAIT_FAILED` hay giá trị khác ⇒ `KHÔNG ĐO`, không dùng phủ định của `_wp1342a1_tin`. Lệnh dựng argv dùng `_wp1342a1ii_FX`; `d/fx.py` (cháu đọc) giữ `_wp1342a1_FX` do khung r4 ghi — cháu của r5 chỉ dùng bước base. |
| M2 | **J4 breakaway tường minh** `wp1342_native_job_breakaway_tuong_minh` (khung `_wp1342a1_ca`). Hai lời gọi `_1174_win_spawn_job` từ CHÍNH tiến trình chạy ca, qua `_wp1342a1_goi`, CÙNG argv con, cwd, env, `deadline` tính theo hạn chung, cùng `SPAWN_FLAGS`, cùng cơ chế thu kết quả; con bước `tach=0,c0,ra=0`, `tach=0x01000000,c1,ra=0`, `ra=0` (hai cháu cùng argv, chỉ khác cờ sinh); mỗi lời gọi dùng một thư mục con riêng cho tệp kết quả hoặc tên vai riêng để hai lời gọi không đọc nhầm tệp của nhau. Biến DUY NHẤT khác giữa hai lời gọi là `LimitFlags` của job đích. **(ii) Đối chứng trước**: `m2 = _module1174(c)` (bản nạp riêng, §0), đặt `m2._1174_WIN_JOB_LIMIT = 0x2800` (literal DUY NHẤT `0x2800` trong tệp test), gọi qua một namespace sao chép `x` chỉ thay `m=m2` (dùng chung `hs`, `ps`, `bt`). Kiểm: `tach_c0` (ii) == `["ok", int]` và `tach_c1` (ii) == `["ok", int]` và hàm trả 0 — khác ⇒ `KHÔNG ĐO` nhãn **"J4 (ii): job cho phép breakaway mà lời xin vẫn bị từ chối"** (ghi nguyên `tach_c1` (ii); schema sai ⇒ `KHÔNG ĐO` nhãn schema riêng). **Đường đo** với `x.m` (hằng sản phẩm): (i) `tach_c0` == `["ok", int]`, khác ⇒ `KHÔNG ĐO` "J4 (i): cháu thường không sinh được"; (iii) `tach_c1`: `["ok", int]` ⇒ ĐỎ nhãn **"J4: breakaway tường minh được nhận"**; `["loi", 5]` ⇒ qua; `["loi", m]` với `m ≠ 5` ⇒ `KHÔNG ĐO` ghi `m` (danh sách cho phép `{5}`); (iv) hàm trả `0`, không lỗi. Kết quả trả (`WP1342_NATIVE_V1 observed`): winerror đường đo, kết quả đối chứng (ii), `IsProcessInJob(GetCurrentProcess(), NULL)` của tiến trình chạy ca (chẩn đoán). Cháu `ra=0` thoát ngay nên pid cháu chỉ là chẩn đoán. |
| M3 | **J5 breakaway ngầm** `wp1342_native_job_breakaway_ngam`. Con bước `chau=0,chau,bt+cho=tha_j5,300`, `cho=go_chau,300`, `ra=0`. `between(job)` (luồng chính, trước resume): lấy bản sao job `_wp1342a1_ban_sao(x, job, 0, 2)` đưa vào danh sách giữ và `x.hs`. Luồng quan sát (`_wp1342a1_goi`): `_wp1342a1_mo(x, mo, "chau", go=False)`; gọi `IsProcessInJob(h_chau, <bản sao job>, &r)` và `IsProcessInJob(h_chau, None, &r0)` (binding phía test trên `x.k`), LƯU `(ok, r, ok0, r0)` (mã Win32 đọc NGAY khi `ok` FALSE); SAU đó mới ghi `go_chau` (nên phép hỏi diễn ra khi cháu còn sống và con chưa thoát). Sau khi hàm trả, assertion theo thứ tự: quan sát vắng hoặc thiếu bản sao job hoặc lời gọi `IsProcessInJob` với job đích trả FALSE ⇒ `KHÔNG ĐO` (ghi mã); `r == 0` ⇒ ĐỎ nhãn **"J5: cháu ngoài job đích"**; hàm trả `0`, không lỗi; handle cháu signaled ≤ 5 s (`_wp1342a1_tin(x, h, 5000)`, nhãn "J5: cháu chưa signaled trong 5 s"). Cháu không bao giờ được ca tạo `tha_j5`. |
| M4 | **J12 job lồng** `wp1342_native_job_long`. Trợ giúp DÙNG MỘT LẦN qua `_wp1342a1_phu`-tương đương (Popen vào `x.ps`), bước `vao_job=0x2000,<pl>`, `tro_c=<pl>`, `--`, con bước `chau=8,chau,bt+cho=tha_j12,300`, `cho=go_chau,300`, `ra=0`. Ca: đọc `job_ngoai` (≤ 20 s; `["loi",…]` ⇒ `KHÔNG ĐO` "J12: job ngoài không gán được" kèm mã); bắt tay `san_sang` (`go=False`, giữ handle trợ giúp); bắt tay `truoc_gan` (handle CON lấy trước gán, `go=True`); rồi chờ (theo hạn chung) tệp `chau` hoặc `ket_qua`; có `chau` thì bắt tay (`go=True`) TRƯỚC khi đọc `ket_qua`; rồi đọc `ket_qua`. Trình tự dữ liệu được kiểm: `ket_qua == ["ok", …]` mà KHÔNG có bắt tay `chau` đã xác minh ⇒ `KHÔNG ĐO` (fixture không thể ra rc khi con còn chờ `go_chau`); tệp `long` vắng/sai schema hoặc phần tử `ok1`/`ok2` = 0 ở nhánh có `long` ⇒ `KHÔNG ĐO` (ghi mã). Kiểm trợ giúp còn sống bằng `WaitForSingleObject(h_tro, 0) == 258` THÔ (M1) trước MỌI phép chấm VÀ trong `finally` của khối chấm, TRƯỚC khi ghi `tha_tro_giup`; sai, `WAIT_FAILED`, hoặc có `het_han_*` ⇒ `KHÔNG ĐO` "J12: job ngoài đóng trước khi quan sát", và nhãn này THẮNG mọi nhãn ĐỎ phát sinh trong khối (job ngoài còn mở thì `KILL_ON_JOB_CLOSE` của nó không thể dọn hộ). Phân nhánh: **(B) lồng thành công**: `ket_qua == ["ok", 0]` VÀ `long == [1, 1, 1, 1]` (nhãn "J12 (B): con không thuộc cả job trong lẫn job ngoài" nếu khác) VÀ handle con, handle cháu signaled ≤ 5 s (nhãn "J12 (B): con/cháu chưa signaled trong 5 s khi job ngoài còn mở"); **(C) từ chối lồng**: `ket_qua[0] == "loi"` và `"job assignment"` trong `ket_qua[1]`, KHÔNG có tệp `chau`, handle con signaled ≤ 5 s (nhãn "J12 (C): con chưa signaled trong 5 s"); **khác** ⇒ ĐỎ nhãn **"J12: nhánh khác"** kèm `ket_qua`, `long`. Sau phép chấm: ca tạo `tha_tro_giup`; trợ giúp signaled ≤ 5 s (không ⇒ `KHÔNG ĐO`). Kết quả trả ghi nhánh (`B`/`C`) và `long`. |
| M5 | **S6 thuần** `wp1342_pure_spawn_fx_mo_rong` (mọi nền): `_wp1342a1ii_FX.startswith(_wp1342a1_FX)` (nhãn "S6: fixture base bị đổi"); `ast.parse(_wp1342a1ii_FX)` (với `import ast` CỤC BỘ trong thân hàm: tệp test không import `ast` ở mức module, và `compile`/`exec`/`eval` là tên cấm của N2(iv)) không lỗi (nhãn "S6: fixture mở rộng không biên dịch"); cây AST của phần thêm chứa đủ ba hằng chuỗi bước `'tach'`, `'vao_job'`, `'tro_c'` trong phép so `ma == …` (nhãn "S6: thiếu bước <tên>"). |
| M6 | **Đăng ký**: một hoặc hai câu `CASES += [list literal]` sau câu đăng ký r4 cuối cùng (18924–18933) và trước `if __name__`: `("wp1342_pure_spawn_fx_mo_rong", _wp1342a1ii_s6)` và ba mục native mẫu `(ID, _native1342(ID, _wp1342a1ii_<tên>))` cùng hằng ID. Mọi tên mức module mới mang tiền tố `_wp1342a1ii_`. |
| M7 | Đột biến qua driver NGOÀI kho (khuôn r4: `ops/land/pr1407-wp1342-provenance/windows-native/desktop/dot_bien_r4_ban2.py`; mỗi cặp (tìm, thay) khớp ĐÚNG MỘT chỗ trong tệp đích; bản sao tạm; ca đích + đối chứng khoẻ; lỗi import/fixture, quan sát hết hạn hoặc vượt cửa sổ 90 s ⇒ `KHÔNG ĐO`). Bảng §4b. |

## 4b. Đường vào, chốt, ca, đột biến

| # | đường | chốt | dấu hiệu | đột biến (tệp đích) | đối chứng |
|---|---|---|---|---|---|
| 1 | hậu duệ xin breakaway tường minh và được nhận | `LimitFlags` không có `0x800` | J4 ĐỎ "J4: breakaway tường minh được nhận" (đối chứng (ii) đạt trong cùng lượt) VÀ J5 XANH | **e1** `packet_loop.py`: dòng `_1174_WIN_JOB_LIMIT = 0x2000   # JOBOBJECT…` đổi `0x2000` → `0x2800` | J1 xanh |
| 2 | hậu duệ sinh thường tự rời job | `LimitFlags` không có `0x1000` | J5 ĐỎ "J5: cháu ngoài job đích" | **e2** cùng dòng, `0x2000` → `0x3000` | J1 xanh |
| 3 | đối chứng (ii) của J4 không có răng (môi trường che phản chứng mà ca vẫn qua) | đối chứng (ii) phải thấy breakaway thành công | J4 KHÔNG ĐẠT, `KHÔNG ĐO` nhãn "J4 (ii): job cho phép breakaway mà lời xin vẫn bị từ chối" với `tach_c1` (ii) == `["loi", 5]` | **e1c** `packet_loop_test.py`: literal `0x2800` (đúng một chỗ trên head; base 0) → `0x2000` | J1 xanh trên CHÍNH bản sao test đã đột biến |
| 4 | job lồng: thu hồi không xác nhận mà ca vẫn qua | (B) đòi `ket_qua == ["ok", 0]` | J12 ĐỎ "J12: nhánh khác" với `ket_qua == ["loi", <chứa "job not empty">]`, SAU khi `long == [1,1,1,1]` và bắt tay `chau` đã xác minh; chỉ chấm trên máy mà lượt sạch cùng head ra nhánh (B) | **a1** của r4, neo nguyên văn của driver r4 (`ops/land/pr1407-wp1342-provenance/windows-native/desktop/dot_bien_r4_ban2.py` dòng 58: mục `"terminate"` của `dang_ky` → `lambda: None`) | J1 xanh |
| 5 | fixture mở rộng vỡ cú pháp / sửa fixture base | S6 | S6 ĐỎ "S6: fixture mở rộng không biên dịch" / "S6: fixture base bị đổi" | **f1** (Linux) xoá dấu `:` đầu tiên của phần thêm; **f2** (Linux) chèn một ký tự vào đầu `_wp1342a1ii_FX` trước `_wp1342a1_FX` | ca thuần r4 `wp1342_pure_spawn_hang_luong` xanh |

Phân biệt: e1 và e2 cùng làm S1 (r4) đỏ assertion `JOB_LIMIT == 0x2000` — không phải dấu hiệu. e1 tách khỏi e2 bằng J5 XANH dưới e1 (`0x2800` không đổi việc hậu duệ sinh thường thuộc job). Dưới e2, J4 có thể đỏ hoặc xanh (tài liệu không nói rõ lời xin breakaway tường minh khi job chỉ có `SILENT_BREAKAWAY_OK`): kết quả J4 dưới e2 được GHI, không dùng làm dấu hiệu. e2 cũng làm J3/J10/J12 (r4/r5) đỏ (cháu rời job đích) — không dùng làm dấu hiệu. Dưới a1, J5 đỏ ở nhãn "hàm trả 0" (khác nhãn e2). Đối chứng J1: không đột biến nào ở bảng chạm đường spawn hay layout, nên J1 (đi qua `_1174_win_spawn_job`) là đối chứng hợp lệ (khác b/abi của r4).

Đường KHÔNG có kích hoạt tự nhiên, chỉ code review: nhánh (C) của J12 trên Windows ≥ 8 (máy đo dự kiến vào (B)); `vao_job` FALSE; `IsProcessInJob` trả FALSE. Nhánh (C) KHÔNG đi qua bước `terminate` (gán job trong thất bại ⇒ `kill_truoc_gan`), nên a1 không đo được ở (C).

**Driver (M7) cho e1c và kết quả `KHÔNG ĐO` có chủ đích:** driver r4 chỉ sửa bản sao `packet_loop.py` và chỉ tính giết khi kết quả `DO`. Driver r5 phải (a) sửa được bản sao `packet_loop_test.py` và chạy CHÍNH bản sao ấy; (b) với e1c, ghi mã kết quả riêng (vd `GIET_DOI_CHUNG`) và chỉ cấp khi ĐỦ: J4 sạch đạt trên cùng máy cùng lượt; bản sao test có đúng một thay thế; nhãn `KHÔNG ĐO` đúng dòng 3 với `tach_c1` (ii) == `["loi", 5]` (đúng schema); J1 trên chính bản sao đạt. Thiếu tệp, sai schema, mã ≠ 5, cạn hạn ⇒ KHÔNG tính giết.

## 5. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Linux không đổi: CI Ubuntu exact head `GOM: ĐẠT`; sổ ID ca base ⊆ head, mỗi ID base cùng trạng thái (đạt/bỏ qua + lý do); `MUTANTS` head == base; mỗi mốc (tìm) của `MUTANTS` đang có khớp ĐÚNG MỘT lần trên head. Biên nhận ghi từng ID, từng mốc. | Rút một ca base; đổi tên khoá giữ số lượng; phần thêm làm một mốc cũ khớp 2 lần. |
| N2 | Chỉ THÊM. `packet_loop.py` blob head == `f98d3f53…` (numstat không có dòng của nó). `packet_loop_test.py`: chạy bộ kiểm N2 của r4 (`ops/land/pr1407-wp1342-provenance/linux/n2_test_r4.py`, biến đổi DUY NHẤT `sed 's/_wp1342a1_/_wp1342a1ii_/g'` — đổi hằng tiền tố và tên trong phản chứng/đối chứng dương; tiền tố ID giữ `wp1342_pure_spawn_`/`wp1342_native_job_`) với base `c1ec1c69` và head: bốn vế (i)–(iv) XANH, gồm cửa sổ đăng ký sau câu base cuối đọc/biến đổi `CASES` (nay là đăng ký r4 ~18924) và trước `if __name__`; ID mới rời tập ID base (gồm 14 ID r4). Bộ kiểm chạy ngoài kho; bản đã sửa ghi byte-exact trong hồ sơ. | Toàn bộ 16 phản chứng của N2 r4 (sau `sed` §0) ⇒ ĐỎ; thêm hai phản chứng: `_wp1342a1_FX = _wp1342a1_FX + "x"` chèn trong cửa sổ ⇒ (ii)/(iv) ĐỎ (gán lại tên base); mục native `("wp1342_native_job_thuan", _native1342("wp1342_native_job_thuan", _wp1342a1ii_j4))` ⇒ (iv) ĐỎ (ID trùng base r4); đối chứng dương: phần thêm thật của head XANH. |
| N3 | Không nối dây: `_wired1342(head) == []` và `wp1342_additive_byte_preserved` đạt; tập tên mức module mới của `packet_loop.py` = ∅; tập ID ca mới đúng `{wp1342_pure_spawn_fx_mo_rong, wp1342_native_job_breakaway_tuong_minh, wp1342_native_job_breakaway_ngam, wp1342_native_job_long}`. | Thêm một tên vào `packet_loop.py` ⇒ đỏ; thiếu một ID ⇒ đỏ. |
| N4 | S6 đạt trên Linux (CI) và Windows (Desktop); ca thuần r4 không đổi trạng thái. | f1, f2 ⇒ ĐỎ đúng nhãn §4b. |
| N5 | Windows vẫn bị từ chối, không đổi: tập ID base đã ghi (`wp1174_windows_claim_rejected`, 12 ID `WP1174_BOTH`, ca native r1–r3, 11 ca native r4, 3 ca thuần r4) chạy trên base và head CÙNG lượt trên Desktop; so từng ID: trạng thái, lý do bỏ qua, dấu hiệu dương (bỏ trường thời gian/pid/handle). | Một ID lệch ⇒ ĐỎ; đột biến mở chốt claim Windows phải đi tới và đỏ ở assertion đích của `wp1174_windows_claim_rejected` (phản chứng của N5 r4, chạy lại). |
| N6 | J4, J5, J12 ĐẠT trên Desktop, mỗi ca trong cửa sổ 90 s của khung r4; và ĐẠT trên VM `tra-luat-win`. J12 đạt N6 ở nhánh (B) HOẶC (C). Biên nhận ghi ID + mọi assertion + `observed`: winerror J4 (phải là 5), đối chứng (ii) thành công, `(ok, r, ok0, r0)` của J5, nhánh J12 (`B`/`C`) + `long`, `IsProcessInJob(GetCurrentProcess(), NULL)` của tiến trình chạy ca, bản Windows/Python. | Ca native `BỎ QUA` trên Windows ⇒ ĐỎ; cháu/con sống sót ⇒ ĐỎ; ca rơi `KHÔNG ĐO` ⇒ tiêu chí `not_measured`, không `passed`. |
| N7 | Đột biến §4b bị giết đúng dấu hiệu: e1, e2, e1c, a1@J12 trên Desktop (bốn lượt); f1, f2 trên Linux. Hợp đồng N7 r1/r4: driver byte-exact trong hồ sơ land; chỉ tính giết khi assertion đích thất bại (riêng e1c: điều kiện ĐỦ ở đoạn "Driver (M7)" §4b), đối chứng đạt, nhãn khớp. Với e1, J5 phải XANH trong cùng lượt. Ghi kết quả J4 dưới e2 (không chấm). a1@J12 chỉ chấm trên máy mà J12 sạch ra (B); Desktop chỉ ra (C) ⇒ thử VM; cả hai chỉ ra (C) ⇒ `a1@J12: not_measured` (§7). | Đột biến sống; đỏ vì import/fixture/quan sát hết hạn; đỏ với nhãn KHÁC; e1 mà J5 đỏ. |
| N8 | Ruff `--select F` 0.15.15: TẬP diagnostic (mã, tệp, tên) head == base; `adr-song`, `doctrine-scan` rc 0 (ghi riêng); `git diff --check` sạch; `eol_policy --all` ok; `git diff --numstat <base>..<H>` không lọc đường dẫn: tập đường dẫn == write set (đúng MỘT tệp), tổng dòng thêm ≤ **450** (ADR-0053). | Thay một diagnostic bằng diagnostic khác cùng số lượng; tệp thứ hai; vượt 450 ⇒ dừng §7. |

Đo Windows trên **`DESKTOP-T9R33P2`** (ưu tiên); VM `tra-luat-win` đo bổ sung N6. Base và head đo cùng một lượt. KHÔNG CI Windows.

## 6. `pham_vi_e`

Không chạm E4, E5. Không đảo quyết định "chỉ Linux" ⇒ không E3. Ca native chỉ tạo/giết tiến trình và job do chính ca sinh ra; trợ giúp J12 tự gán MÌNH vào job dùng một lần; đối chứng J4 chỉ đổi thuộc tính của một bản nạp module riêng trong ca, không đụng bản nạp khác hay tiến trình chạy ca.

## 7. `luat_dung`

- Trần lời gọi Codex theo `ADR-0055`; trần vòng review theo `ADR-0048`. Chạm trần ⇒ Review Rescue Checkpoint; xin tăng mang **E2**.
- Trần `ADR-0053` (≤ 6 tệp / ≤ 450 dòng thêm) cưỡng chế trên NUMSTAT THẬT: executor đo `git diff --numstat <base>..<H>` không lọc đường dẫn TRƯỚC khi công bố; tập đường dẫn ≠ write set hoặc > 450 ⇒ DỪNG, không push, báo điều phối (**E2**). Không tự cắt ca/assertion/đột biến để lọt trần.
- Ca đo trên head SẠCH làm lộ lỗi sản phẩm (J4 nhận breakaway, J5 cháu ngoài job, J12 nhánh khác) ⇒ DỪNG: sửa `packet_loop.py` nằm ngoài write set, là revision mới; báo chủ kho (**E2**).
- Cần sửa thân định nghĩa đang có hoặc gán lại tên base ⇒ dừng, revision đặc tả.
- J4 đối chứng (ii) không đạt trên CẢ Desktop và VM, hoặc winerror ≠ 5 trên cả hai ⇒ J4 và e1/e1c `not_measured`; quyết định tiếp (mở rộng danh sách mã có căn cứ, đổi máy) là của chủ kho (**E2**).
- J12 `job_ngoai` FALSE trên cả hai máy ⇒ J12 và a1@J12 `not_measured`; **E2**.
- J12 sạch ra nhánh (C) trên cả Desktop và VM (job ngoài gán được, job trong bị từ chối) ⇒ J12 vẫn đạt N6 nhưng `a1@J12: not_measured`; đổi máy hay chấp nhận là quyết định chủ kho (**E2**).
- Máy đo Windows không có trong hạn lease ⇒ tiêu chí native `not_measured`; gia hạn/cấp lại là quyết định chủ kho (**E2**).
- Đặc tả không thuộc Mission ⇒ chờ chủ kho duyệt băm (`ADR-0067`, **E2**) sau khi review độc lập approve.

## 8. `hinh_dang_ke_thua` và ngân sách

`khong_ap_dung`. Ghi chú kế thừa từ r4: hàm mới không decorator; tên mới mang tiền tố riêng; đăng ký chỉ list literal; hook `truoc_gan`/`between` chỉ MƯỢN tài nguyên, chờ có hạn; tiêu chí chỉ có lời khai ghi `not_measured`; phép kiểm "đã signaled" luôn là chờ có hạn 5 s (Q7 r4).

Ngân sách dòng (ước tĩnh theo khối tương tự đo trên `11bd033`; chưa phải numstat):

| khối | căn cứ | ước |
|---|---|---|
| chú thích đầu khối | r4 2 dòng | 2–3 |
| `_wp1342a1ii_FX` (bước `tach`, `vao_job`, `tro_c` + binding; mỗi bước ghi tệp kết quả, đọc mã Win32 ngay) | `_wp1342a1_FX` 30 dòng / 7 bước; `tro_a`+`tro_b` 11 dòng | 30–42 |
| argv, đọc tệp kết quả có hạn + kiểm schema, hạn chung, kiểm WAIT_TIMEOUT thô | `_wp1342a1_lenh` 2, `_wp1342a1_mo` 20 | 18–28 |
| S6 | | 7–10 |
| J4 (đối chứng ii qua bản nạp riêng + đường đo) | J9 24 dòng | 26–38 |
| J5 | J3 7, J9 24 | 20–28 |
| J12 (ba nhánh, trình tự dữ liệu, kiểm job ngoài còn mở trong `finally`) | J10 10, J9 24 | 40–56 |
| đăng ký | r4 2 câu / 11 dòng | 4–6 |
| **tổng** | | **147–211** |

Đầu cao 211 < 450 (biên ~240 dòng). Trần cưỡng chế ở numstat thật (§7).

## 9. Quyết định đã ghi

- **Q1.** Phạm vi a1-ii = breakaway tường minh, breakaway ngầm, job lồng — chủ kho 2026-11-18 (r4 §9 Q1) và Issue #1342 `issuecomment-6999134364`.
- **Q2.** Cấm tuyệt đối breakaway (`LimitFlags == KILL_ON_JOB_CLOSE`) — chủ kho 2026-11-18 (r4 Q3). r5 không đổi hằng, chỉ đo.
- **Q3.** Job còn tiến trình ⇒ `_1174Error`, fail-closed — r4 Q4; J12 nhánh (C) là đường fail-closed đã có.
- **Q4.** Chờ signaled có hạn 5 s — r4 Q7; áp cho J5, J12.
- **Đ1 (đề xuất của người soạn, chờ chủ kho xác nhận khi duyệt băm, E2).** Write set CHỈ `packet_loop_test.py`; không thêm kiểm runtime nào vào `_1174_win_spawn_job`. Căn cứ: ba hạng mục hoãn sang a1-ii trong r4 §2 (J4/J5/J12, e1/e2, job đối chứng) đều là phép đo; chốt sản phẩm (Q2) đã có trong r4.
- **Đ2 (người soạn).** Tập mã từ chối J4 `{5}` (r4 bản 2: "dựa trên tài liệu; mã khác ⇒ `KHÔNG ĐO` và ghi mã thật để mở rộng có căn cứ ở revision sau"); đối chứng (ii) đi qua CHÍNH `_1174_win_spawn_job` từ CHÍNH tiến trình chạy ca, chỉ khác `LimitFlags` (bản nạp module riêng), để cùng chuỗi job tổ tiên, cùng lệnh, cùng cách quan sát (finding lượt 2 r4 cho e1; P1 lượt 1 r5 — bản 1 dùng trợ giúp tự gán job nên không chứng minh được cùng chuỗi tổ tiên).
- **Đ3 (người soạn).** J5 hỏi membership với job ĐÍCH (không với `NULL`) khi cháu còn sống và con chưa thoát (finding lượt 2 r4 cho e2); J12 tách kết quả gán job ngoài / gán job trong / quan sát, giữ handle con bằng `truoc_gan` có bắt tay chờ `go`, quan sát khi job ngoài còn mở (finding lượt 2 r4 cho J12).

## 10. `chua_do_duoc`

- Kích thước thật (ước 147–211; trần cưỡng chế ở numstat).
- Mọi hành vi Win32 ở §0 dòng cuối: theo tài liệu, chưa đo trong kho; đặc biệt lời xin breakaway tường minh khi job chỉ có `SILENT_BREAKAWAY_OK` (J4 dưới e2), và breakaway trong chuỗi job lồng khi tiến trình chạy ca đã nằm trong job.
- Tiến trình chạy ca trên Desktop/VM có nằm sẵn trong job không (N6 ghi lại).
- Nhánh J12 xảy ra trên từng máy (dự kiến (B) trên Windows ≥ 8; chưa đo).
- Lease chạm write set: phép quét tạm §0 ra 0, nhưng chỉ nhánh `ops/*` và ba tên trường; `ai-dang-giu` (công cụ có thẩm quyền) chưa chạy được trong phiên soạn ⇒ người cấp lease chạy nó (L5).
- Hằng số §0 trôi khi master tiến; đo lại theo L5.

## 11. Nhật ký review

- **Lượt 1** (bản 1 sha256 `4657e5d2…`, base `11bd033`; `request_changes`: 1 P1, 4 P2, 1 P3). Bản này: P1 J4 đối chứng (ii) chuyển sang CHÍNH đường sản phẩm từ CHÍNH tiến trình chạy ca, bản nạp module riêng với `LimitFlags = 0x2800` — biến duy nhất khác; bỏ `vao_job` khỏi J4; P2 J12(C) không đo a1 ⇒ a1@J12 chỉ chấm khi lượt sạch ra (B), cả hai máy chỉ (C) ⇒ `not_measured` + §7 E2; P2 thiếu dữ liệu fixture ⇒ kiểm schema, `KHÔNG ĐO` không gộp vào nhãn đỏ, J12 đòi bắt tay `chau` trước `ket_qua`, kiểm trợ giúp bằng `WAIT_TIMEOUT` thô trước mọi phép chấm và trong `finally`; P2 cửa sổ 90 s ⇒ hạn chung mỗi ca (`het = now + 75`, dự phòng 30 s/10 s); P2 e1c ⇒ driver sửa và chạy bản sao test, mã kết quả riêng, điều kiện đủ; P3 ⇒ base `4eda94e` (blob write set không đổi), mô tả breakaway theo từng job, `IsProcessInJob` nhận cả hai quyền truy vấn, `_wp1342a1_mo` 20 dòng, ngân sách tính lại 147–211.
