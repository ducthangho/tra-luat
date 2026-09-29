# ĐẶC TẢ — `LAUNCHER-CON-SONG-ESRCH` — **revision 3, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp685` (ID bền, `wp<issue>`); tên đọc được: `LAUNCHER-CON-SONG-ESRCH`. Lease dùng tên nào cũng phải kèm `packet_issue: 685`. |
| `revision` | **3** |
| `thay_the_cho` | r2 = `ops/specs/launcher-con-song-esrch-r2.md`, sha256 `de9c553aaeb4cb2dae16385e3059a5a196248230a4ed18a42016c8af6fac9ce4`, commit `cdf0575` (`cdf0575358270843fbde51f817f0d6a4d9655dec`). Trước đó: r1 = `ops/specs/launcher-con-song-esrch-r1.md`, sha256 `ee44238c…37d9`, commit `d96d075`. r1 và r2 giữ nguyên, không sửa đè; r3 là bản duy nhất được cấp lease. |
| `packet_issue` | **#685** |
| `mission_issue` | **#686** (Mission Issue, object ID `5628902742`). Thân #686 khai ngay đầu rằng nó do phiên agent đăng hộ chủ kho bằng credential chủ kho; nguồn thẩm quyền là các câu trả lời của chủ kho được trích trong đó (Q0–Q4 trong thân; Q5 ở comment `5888633201`, xem `nguon_cap_viec`). |
| `nguon_cap_viec` | (r1) Chỉ thị chủ kho 29-09-2026: *"mở packet riêng cho bản vá launcher (race ProcessLookupError) đi"*. Nguồn lỗi: PR #679, job `gate-ops (ubuntu-latest)` `109303373142`, phân tích ở PR #679 comment `5885963131`. (r2) Cross-review lượt 1 trên PR #688, reviewed commit `d96d075`: `changes_requested`, 2 P1 / 3 P2 / 0 P3; VERDICT sha256 `69dbf916648790c7452d6e0bb7fa56b3a44c59df6c568ea29a1c5bf2eba1d9fb` (viết tắt `69dbf916…d9fb`). (r3) Cross-review lượt 2 trên PR #688, reviewed commit `cdf0575` (spec sha256 khớp băm r2 ở `thay_the_cho`): `changes_requested`, **0 P1 / 2 P2 / 0 P3**; hai P1 của lượt 1 đã đóng (VERDICT lượt 2, bảng ĐỐI CHIẾU LƯỢT TRƯỚC: bốn trong năm lớp của lượt 1 ĐÃ ĐÓNG, riêng `ma-tran-loi-thieu-chot` còn mở); VERDICT sha256 `19f5faa0a210d28f3a25f94e5ff65883431c2645da19dd9354bc9e51216ba47f` (viết tắt `19f5faa0…a47f`; phiên soạn r3 đo lại băm tệp `VERDICT.md` trong hồ sơ lượt 2 lúc 11:49Z ra đúng chuỗi này), comment PR #688 `5889523704`, đăng 11:40:59Z 29-09 (phiên điều phối đọc qua API sau khi r3 soạn xong, điền vào trước khi đóng băng). Hai lớp P2 của lượt 2: `ma-tran-loi-thieu-chot`, `chot-nguoc-khong-co-lap`. Mission #686 comment `5888633201` (Q5: điều kiện cấp lease); phiên soạn r2 và r3 KHÔNG đọc lại nội dung comment này, coi nó là lời khai của điều phối, và không chép điều kiện nào từ nó vào đặc tả. |
| `objective` | `_con_song` không bao giờ để một ngoại lệ `OSError` của phép hỏi `/proc/<pid>/stat` thoát ra; tiến trình biến mất giữa chừng (ESRCH) được báo là đã chết; lỗi khác KHÔNG được đọc thành "đã chết" chỉ vì không stat được, và một zombie vẫn được báo là đã chết khi nội dung `/proc/<pid>/stat` còn đọc được. |
| `review_class` | **`sensitive`** — protocol §8: *"launcher hoặc gate lifecycle"*. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | `claude` — **Claude Sonnet 5.5, effort high** (Mission #686 Q3); phiên điều phối kiểm lại độc lập và commit. |
| `environment` | **`cloud`**. Bản vá chỉ chạm nhánh Linux của `_con_song`; nhánh Windows trả về trước dòng 650. |
| reviewer | `codex` (`gpt-6-astra`, effort ≥ medium), cần `cross_approved`. Protocol §8: HINT không được chứa mã launcher; chỉ được chứa mã TEST thuần. |
| `depends_on` | Lease `ci-g5-cong-cu-chia-manh-r1-g2-claude` (packet #668) giữ `.claude/dev/launcher_test.py`, `lease_expires_at_utc` = `2026-09-30T07:41:00Z` (đọc từ tệp lease trên nhánh `ops/cap-lease-ci-g5-cong-cu-chia-manh`; `ai-dang-giu` báo `CÒN_HẠN`, `NGƯỜI_GIỮ 1`, rc=11, lúc 11:56:57Z 29-09; cùng kết quả ở 11:45:23Z). Đầu nhánh ấy đã đi từ `7c16d11` (r2) sang `2ae5646` (một commit chỉ thêm hồ sơ review #668, 11:26:38Z); tệp lease g2 giữa hai đầu nhánh KHÔNG đổi (`git diff --quiet 7c16d11 2ae5646 -- <tệp lease>` rc=0, 11:49Z). Phải nhả hoặc hết hạn trước khi cấp lease cho `wp685` (Mission #686 Q1). `.claude/dev/launcher.py`: `NGƯỜI_GIỮ 0`, rc=0 (11:56:47Z; cùng kết quả ở 11:45:12Z). Chi tiết phép đo ở §8. |
| nền nghiệm thu | `origin/master` `89fc4fac8cea65979cc2483043dc8cd07a6e8518` — **vẫn hợp lệ cho hai tệp trong write set** dù `origin/master` đã tiến hai lần trong lúc soạn r3: `1c23933b13f33d6b0ebdb2901a3dec33c474d34c` (thấy 11:44:35Z) rồi `c57df32f0fd8c992ed363d7000f4f761275750ea` (Merge PR #679, commit lúc 11:55:40Z; đo sau `git fetch` đủ refspec rc=0, 11:56:41Z). Với đầu hiện tại: `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ rc=0 (11:56:41Z), và không tệp nào dưới `.claude/` hay `.github/` đổi (chi tiết §8). Đầu `origin/master` sẽ còn trôi: đo lại lúc cấp lease. Nền tiếp nối (continuation base) sẽ khác khi #668 land trước; khai riêng lúc cấp lease, không thay nền này (protocol §3.2.1). |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/launcher-con-song-esrch-r3.md`, không loại dòng nào. Giá trị được công
bố **ngoài** tệp: comment trên #685 và lease, kèm OID commit + đường dẫn. Khối closure dưới đây
nằm **trong** tệp, nên một `spec_hash` không thể đi với hai closure khác nhau. Đổi bất kỳ byte nào
⇒ revision mới, băm mới, lease mới. Băm của r1 (`ee44238c…37d9`) và của r2 (`de9c553a…9ce4`) KHÔNG
còn dùng để cấp lease.

**Closure đóng băng** (các trường dispatcher dẫn xuất, protocol §3.2), điền tay theo **miễn trừ có
phạm vi** ở Mission Issue #686: chỉ `wp685`, hết hiệu lực ở lần đầu một policy canonical cho closure
xuất hiện trên nhánh mặc định.

| trường | giá trị |
|---|---|
| `change_policy_sha` | `null` — chưa có policy canonical; descriptor thay thế là miễn trừ ở #686 |
| `effective_write_set` | `.claude/dev/launcher.py` · `.claude/dev/launcher_test.py` (exact) |
| `effective_review_class` | `sensitive` |
| `required_checks` | Trên PR thi hành: `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-registry (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)` của `.github/workflows/ci.yml`, workflow `thu-hoi` — các job này có thật và phải xanh, nhưng **KHÔNG job nào trong số đó chạy `launcher_test.py`** (`gate-registry` chạy chín bộ thuộc `MOI`, không có `launcher_test.py`; xem §8). Ngoài các check CI, **bắt buộc** bằng chứng cục bộ Linux B1–B6 neo exact candidate SHA (lệnh nguyên văn, giờ UTC, rc, dòng tổng), đính vào handoff và reviewer đọc trước merge; cross-review codex `cross_approved`, 0 P1/P2/P3 |
| `land_obligations` | Chủ kho audit + merge (không tự merge/approve); đọc kết quả `launcher-windows.yml` ở lượt `push` lên master sau merge, cả job Windows lẫn job Ubuntu, và báo; ghi sổ verdict + HINT vào `ops/reviews/` kèm receipt và mục README; thu hồi lease sau land; đóng #685 |

**Descriptor nguồn closure** = `{mission_issue: 686, object_id: 5628902742}`. Lease phải **chép**
đúng các giá trị trên; lệch ⇒ **DỪNG**. Băm thân Issue ở phía nhận là **KHÔNG ĐO ĐƯỢC** từ phiên
soạn (đường đọc MCP chuẩn hoá thực thể HTML trong thân issue, xem CLAUDE.md), nên neo bằng object
ID + số Issue.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

**Thay đổi so với r2** (mỗi dòng ứng với một lớp của VERDICT lượt 2, hồ sơ cross-review PR #688; slug là
tên lớp trong bảng lớp của VERDICT). r3 áp `HINT.patch` của lượt 2 lên bản sao r2 bằng
`patch -p0 --fuzz=0` (rc=0, không hunk bị từ chối, 11:44:22Z 29-09) rồi viết lại phần lời văn quanh nó; các
điểm r3 tự thêm ngoài HINT được nêu riêng ở dòng cuối bảng và ở §9:

| slug lớp | hạng | chỗ sửa trong r3 |
|---|---|---|
| `ma-tran-loi-thieu-chot` | P2 | §3 Q-A.5 viết lại và thêm đoạn làm rõ nội dung hỏng; §1 thêm bảng 3 và bảng 4 (đo lại 11:46Z); §7 B2 thêm ba nhãn `B2-exception`, `B2-parse`, `B2-dem-doc` kèm **ma trận tầng × miền**; B5 từ bảy lên **mười LỚP** đột biến (thêm (h), (i), (j)), kỳ vọng **mười hai mục `DOT_BIEN`** vì (h) và (j) mỗi lớp cần hai vị trí; §9 viết lại lời tổng kết |
| `chot-nguoc-khong-co-lap` | P2 | §7 B5: câu chốt ngược của r2 thay bằng **hai phép đo** — (A) ca đầy đủ, (W) witness cô lập cùng helper — kèm bảng assertion còn hiệu lực và tiêu chí đạt; §6.2 và quy ước chung §7 nêu hợp đồng helper |
| (r3 tự thêm, ngoài HINT) | — | §1 bảng 4 và §2: quan sát đo được về `comm` không phải UTF-8; §7 B2-parse có dạng nội dung thứ tư (không giải mã được); B5 nêu quy tắc **mục `DOT_BIEN` theo ô của ma trận**; §8 đo lại nền, lease, ruff; §9 thêm lượt 2 vào bộ đếm hình dạng; §10 cập nhật |

**Lịch sử: thay đổi r1 → r2** (mỗi dòng ứng với một lớp của VERDICT lượt 1):

| slug lớp | hạng | chỗ sửa trong r2 |
|---|---|---|
| `qa-fallback-mat-zombie` | P1 | §1 (thêm bảng zombie), §3 Q-A viết lại, §6.1, §7 B2/B3, B5 |
| `so-muc-dot-bien-mau-thuan` | P1 | §6.2 trỏ vào B5; B5 là danh sách đột biến có thẩm quyền duy nhất |
| `ci-dang-ky-khong-thuc-thi` | P2 | closure `required_checks`, §5, §7 B6, §8 |
| `ma-tran-loi-thieu-chot` | P2 | §7 B2 (EIO, tín hiệu ngoài `OSError`, đếm lần gọi, đọc hỏng), B5 |
| `dem-ca-bang-hau-to` | P2 | §8 (đếm lại bằng AST), §6.2 đặt tên ca |

---

## 1. Vấn đề

`.claude/dev/launcher.py:650–651` (trên `89fc4fa`), hàm `_con_song` (định nghĩa ở dòng 629), nhánh
không phải Windows:

```python
    trang_thai = Path(f"/proc/{pid}/stat")
    if trang_thai.exists():
```

`Path.exists()` nằm **ngoài** khối `try`. `pathlib` chỉ nuốt errno `(2, 20, 9, 40)`
(`pathlib._IGNORED_ERRNOS`, đo trên Python 3.11.15). Tiến trình đang bị thu hồi làm `stat()` trả
**ESRCH** (errno 3) ⇒ `ProcessLookupError` thoát lên `_con_song_dung_khoa` → `_giet_rieng` → nơi gọi.

Bằng chứng CI (job `109303373142`, PR #679, head `aecdccd`): `t125` chạy toàn suite A/B **song
song**; vế B đỏ đúng một ca, `t154`:

```
ProcessLookupError: [Errno 3] No such process: '/proc/36606/stat'
```

**Phản chứng chạy được, bảng 1 — PID đang sống** (đo lại 11:11:47Z 29-09, Python 3.12.3, trên bản
sao tạm của launcher `89fc4fa`; seam: vá `pathlib.Path.stat` ném lỗi cho đúng đường
`/proc/<pid>/stat` của PID đang xét, `read_text` và `os.kill` không bị vá; PID sống = chính tiến
trình đang chạy):

| bản | ESRCH | EACCES | EIO | không seam: PID sống / PID không tồn tại |
|---|---|---|---|---|
| nền `89fc4fa` | **ném** `ProcessLookupError` | **ném** `PermissionError` | **ném** `OSError` | `True` / `False` |
| bản vá RỘNG (`except OSError: return False`) | `False` | **`False` — SAI** | **`False` — SAI** | `True` / `False` |
| bản vá HẸP **của r1** (OSError khác ⇒ rơi thẳng về `os.kill(pid, 0)`) | `False` | `True` | `True` | `True` / `False` |
| bản r2 (Q-A dưới đây) | `False` | `True` | `True` | `True` / `False` |

**Phản chứng chạy được, bảng 2 — zombie CHƯA `wait`** (cùng lúc, cùng Python; con thật do ca sinh
bằng `start_new_session`, nhận SIGTERM thật, đọc `/proc/<pid>/stat` thấy trạng thái `Z`, KHÔNG được
`wait` trong lúc đo; dọn bằng PID tường minh ở `finally`; seam chỉ vá `Path.stat` của PID ấy).
Cột cuối gọi `_giet_cay(pid, khoa)` trên một con còn SỐNG có seam EACCES ở `stat`, để SIGTERM thật
biến nó thành zombie; mã deadline suy từ `KetGiet.tron_ven` theo `launcher.py:1669`
(`tron_ven` ⇒ `MA_QUA_HAN` 124; ngược lại `MA_GIET_HUT` 125):

| bản | zombie, không seam | zombie, EACCES ở `stat` | zombie, EIO ở `stat` | zombie, EACCES ở CẢ `stat` lẫn `read_text` | `_giet_cay` con sống + SIGTERM + EACCES ở `stat` |
|---|---|---|---|---|---|
| nền `89fc4fa` | `False` | **ném** `PermissionError` | **ném** `OSError` | **ném** `PermissionError` | **ném** `PermissionError` |
| bản vá RỘNG | `False` | `False` | `False` | `False` | `tron_ven=True` ⇒ 124, 0,1 giây — đúng ở ca này, nhưng bảng 1 cho thấy nó sai ở PID sống |
| bản vá HẸP **của r1** | `False` | **`True` — SAI** | **`True` — SAI** | `True` | `tron_ven=False`, `me_da_chet=False` ⇒ **125**, 2,4 giây, 23 lần hỏi `stat` |
| bản r2 | `False` | `False` | `False` | `True` (bảo thủ, xem Q-A) | `tron_ven=True` ⇒ **124**, 0,1 giây, 2 lần hỏi `stat` |

Ba bản Python có trong container cho cùng kết quả ở các ô khoá của bảng 2 (hàng HẸP r1 và hàng r2,
cột EACCES ở `stat` và cột `_giet_cay`): 3.11.15 (11:11:58Z), 3.12.3 (11:11:47Z), 3.13.12 (11:12:01Z).
CI Linux của `ci.yml` dùng `python-version: "3.12"`; job `launcher` của `launcher-windows.yml` dùng
3.13 trên Windows và 3.11 trên Ubuntu.

**Bản "r2" trong các bảng 1, 2 và 3 là bản NHÁP của phiên soạn**, dựng ở bản sao tạm chỉ để kiểm hợp
đồng Q-A có thoả được và đo ra số trên. Nhãn "r2" ở đó chỉ bản nháp dựng theo Q-A.1–4 của r2 (r3 không
đổi Q-A.1–4), KHÔNG phải revision đặc tả r2. Bản nháp không nằm trong đặc tả này, không phải bản vá
đã được chứng nhận; executor tự viết bản của mình theo lời văn Q-A và tự đo lại.

Cross-review lượt 2 tái đo hai bảng trên bằng bản dựng độc lập của họ (VERDICT lượt 2, hướng 2,
11:23:21Z, ba bản Python): các ô khoá khớp (hàng HẸP r1 và hàng r2, `_giet_cay` 125 với 23 lần hỏi
`stat` so với 124 với 2 lần; thời gian 2,32 giây và 0,10 giây ở rig của họ — không phải hằng số). Bảng 1
và 2 ở trên giữ nguyên số r2 đã đo; phiên soạn r3 KHÔNG chạy lại chúng. Phiên soạn r3 chỉ chạy lại
probe `matrix_extra` của lượt 2 (bảng 3) và tự đo thêm bảng 4.

**Bảng 3 — đầu vào mới của r3** (chạy lại lúc 11:46:05Z 29-09, Python 3.12.3, probe `matrix_extra` trong
bản sao rig của cross-review lượt 2; các hàng "biến thể" là đột biến do reviewer dựng ở tệp `x_*.py` của
rig, phiên soạn không viết). Seam: `Path.stat` của PID sống (chính tiến trình probe) ném EACCES; với cột
đầu, `Path.stat` ném một đối tượng `RuntimeError` dựng sẵn; với ba cột nội dung, `Path.read_text` của đúng
đường `/proc/<pid>/stat` trả chuỗi cho sẵn, `<pid>` là PID của probe:

| bản | `RuntimeError` ở `stat` | nội dung rỗng | `<pid> (x)` | `<pid> (x) ` (khoảng trắng cuối) | số lần `read_text` trong lời gọi |
|---|---|---|---|---|---|
| bản nháp Q-A | thoát CHÍNH đối tượng ấy | `True` | `True` | `True` | 1 |
| biến thể "bắt `Exception` ở phép hỏi" | **bị nuốt** (`_con_song` trả `True`) | `True` | `True` | `True` | 1 |
| biến thể "nội dung hỏng ⇒ `False`" | thoát đúng đối tượng | **`False`** | **`False`** | **`False`** | 1 |
| biến thể "tầng đọc chỉ bắt `OSError`" | thoát đúng đối tượng | `ValueError` thoát | `IndexError` thoát | `IndexError` thoát | 1 |
| biến thể "đọc lần hai" | thoát đúng đối tượng | `True` | `True` | `True` | **2** |

Ba biến thể có chữ đậm (nuốt sentinel, `False` cho nội dung hỏng, đọc hai lần) là ba đường mà B1–B5 của r2
để lọt: cả ba PASS hai ca mẫu `t156_...` và `t157_...` do reviewer dựng theo B1–B3b của r2 (VERDICT lượt
2, hướng 3, 11:30:37Z; phiên soạn r3 chạy lại `mutations` lúc 11:46:12Z ra cùng kết quả: bảy đột biến của
r2 chết đúng nhãn, ba biến thể mới PASS cả hai ca, đối chứng `NameError` chết bằng `NameError`). Hàng
"tầng đọc chỉ bắt `OSError`" là **phản chứng phụ**: nó ĐỎ bằng lỗi vô can (`ValueError`/`IndexError`), nên
không được tính là đột biến bị giết đúng lý do.

**Bảng 4 — "nội dung không phân tích được" là những ngoại lệ nào** (phiên soạn r3 tự đo, Python 3.12.3;
biểu thức tách trạng thái của `launcher.py:654`; chuỗi thử dựng tay, `comm` thử thật):

| đầu vào | kết quả (đo 11:46:33Z) |
|---|---|
| rỗng | `ValueError` |
| thiếu dấu đóng ngoặc, ví dụ `32000 x S 1` | `ValueError` |
| hết chuỗi ngay sau dấu đóng ngoặc, `32000 (x)` và `32000 (x) ` | `IndexError` cả hai |
| đầy đủ, `32000 (x) S 1` | `'S'`, không ném |
| `comm` = byte `ff fe` + `ab` (con tự đặt bằng `prctl(PR_SET_NAME)`), `read_text` thật trên `/proc/self/stat` | `UnicodeDecodeError`: là `ValueError`, **không** là `OSError` (`preferred_encoding` `utf-8`; cùng kết quả với `LC_ALL=C.UTF-8`) |
| cùng loại `comm` ấy, PID ĐANG SỐNG, nền `89fc4fa`, không seam (đo 11:46:40Z) | `_con_song(pid)` = **`False`**, `os.kill(pid, 0)` thành công |

Dòng cuối là quan sát về nhánh CŨ, xem §2; nó không thuộc phạm vi sửa.

**Đính chính lời khai của chính phiên soạn — hai lần, cùng hình dạng.** Lần một (r1 §1): bản vá đăng ở
PR #679 comment `5885963131` và thân #685 là bản **RỘNG**; nó đóng ESRCH nhưng biến một
`PermissionError` trên PID **đang sống** thành "đã chết" — đúng lớp lời khai sai *"trả 124 khi tiến
trình còn sống"* mà CLAUDE.md đã trả giá. Lần hai (r2): bản **HẸP** r1 chữa lỗi ấy rồi mở lỗ ở chiều
kia — `kill(pid, 0)` THÀNH CÔNG với zombie, nên bản HẸP báo "còn sống" cho cây đã chết và deadline
trả 125 thay vì 124. Chính r1 §7 B3 chỉ đo PID **đã `wait`**, tức đo đúng chỗ không có zombie. Cross-review
lượt 1 bắt được điều này bằng phép đo (VERDICT hướng 3), không phải bằng đọc.

## 2. Phạm vi đã đo (grep + đọc luồng trên `89fc4fa`)

- Trong `launcher.py` chỉ **một** lời gọi `.exists()` trên đường `/proc`: `:651`.
- Ba chỗ đọc `/proc` khác đều nằm trong `try` bắt `OSError`: `:359` (`_khoa_danh_tinh`, một
  `read_text`), `:430` và `:484` (mỗi chỗ một `iterdir`; phép đọc `stat` bên trong ở `:436` và
  `:490` cũng có `try`). Không cùng dạng lỗi; **không** sửa.
- Nhánh hiện có ngay dưới `:651`: khi `exists()` trả `True` mà `read_text` ném `OSError`,
  `ValueError` hoặc `IndexError` (`:655`), hàm trả `False`. Đó là hành vi CŨ (cross-review lượt 1,
  hướng 7: nó bỏ PID khi `read_text` bị EACCES). Packet này **không** đổi nhánh ấy và **không** được
  nhận là đã sửa nó. **Quan sát mới của r3** (đo 11:46:40Z 29-09, Python 3.12.3, `launcher.py` của
  `89fc4fa`, không seam): một tiến trình ĐANG SỐNG mà `comm` chứa byte không phải UTF-8 (con tự đặt
  bằng `prctl(PR_SET_NAME)`) làm `read_text` ném `UnicodeDecodeError`, và nhánh cũ trả
  `_con_song(pid)` = **`False`** trong khi `os.kill(pid, 0)` thành công. Tức nhánh cũ có thể khai "đã
  chết" cho tiến trình còn sống — đúng lớp lời khai mà objective cấm cho ĐƯỜNG MỚI. Ngoài phạm vi
  (Q-A.3), chưa tìm Issue liên quan, KHÔNG sửa ở đây; ghi lại để không ai đọc `B2-parse` là bằng chứng
  nhánh cũ đã đúng, và để chủ kho quyết có mở Issue riêng hay không. Đây là một PID thật trên một nền;
  tần suất ngoài thực tế: KHÔNG ĐO ĐƯỢC.
- `_con_song` có năm nơi gọi trong `launcher.py`: `:607` (`_con_song_dung_khoa`), `:857` và `:882`
  (`_giet_windows`, tức nhánh Windows), `:1020` và `:1039` (`_giet_cay`). Đo bằng AST (lần lên cây
  cha tới hàm bao, 10:2xZ 29-09; cross-review lượt 1 đo lại độc lập ra đúng năm nơi, 10:52Z):
  **không** lời gọi nào nằm trong thân một `try` bao ngoài, nên `ProcessLookupError` từ `:651` thoát
  thẳng khỏi các hàm ấy.
- Executor phải **grep lại** trên nền tiếp nối trước khi sửa và khai mọi chỗ mới tìm thấy.

## 3. Quyết định

- **Q-A — ngữ nghĩa bản vá.** Q-A là **suy luận của phiên soạn** (từ docstring của `_con_song`, từ
  bài học 124/125 và bài học zombie trong CLAUDE.md, và từ VERDICT lượt 1 và lượt 2); **KHÔNG phải
  quyết định chủ kho**. r2 sửa Q-A của r1 theo lượt 1; r3 KHÔNG đổi ngữ nghĩa Q-A.1–4 và Q-A.6, chỉ nói
  rõ Q-A.5 theo từng tầng và thêm đoạn làm rõ nội dung hỏng (ngay dưới khối "Hệ quả còn lại") theo lượt
  2; chủ kho có thể bác bằng revision mới. Hợp đồng, bằng lời:
  1. Phép hỏi `stat`/`exists` trên `/proc/<pid>/stat` được thực hiện **đúng một lần** mỗi lời gọi
     `_con_song`, và không thử lại.
  2. `ProcessLookupError` ở phép hỏi ấy ⇒ trả `False` (tiến trình đã biến mất).
  3. Phép hỏi không ném lỗi ⇒ hai nhánh sẵn có giữ **nguyên xi**: tệp có ⇒ đọc trạng thái (kể cả
     hành vi cũ ở §2 khi đọc lỗi); tệp vắng ⇒ rơi về `os.kill(pid, 0)` như cũ.
  4. `OSError` khác (EACCES, EIO, …) ⇒ **không** kết luận. Không stat được chưa có nghĩa là không đọc
     được. Trước hết **thử đọc nội dung** `/proc/<pid>/stat`: đọc được và trạng thái là `Z` ⇒ `False`;
     đọc được và không phải `Z` ⇒ `True`. Không đọc được (mọi `OSError`, hoặc nội dung không phân tích
     được) ⇒ rơi về `os.kill(pid, 0)` với ngữ nghĩa sẵn có (`PermissionError` ⇒ `True`,
     `ProcessLookupError` ⇒ `False`). Bước đọc này cũng chỉ làm **một lần**.
  5. Phạm vi bắt, **theo từng tầng** (r3 viết lại cho rõ theo lớp `ma-tran-loi-thieu-chot`; r2 chỉ nói
     "họ `OSError`" và để hở chỗ nội dung hỏng ở bước 4):
     · **Tầng hỏi** (`stat`/`exists`): chỉ bắt họ `OSError`. Mọi ngoại lệ khác thoát ra nguyên đối
       tượng — cả ngoại lệ thuộc `Exception` nhưng không thuộc `OSError` (ví dụ `RuntimeError`) lẫn
       ngoại lệ thuộc `BaseException` nhưng không thuộc `Exception` (ví dụ `KeyboardInterrupt`).
     · **Tầng đọc** (bước 4): bắt `OSError` của phép đọc, và các lỗi **phân tích cục bộ** của nội dung
       đọc được (`ValueError` — kể cả `UnicodeDecodeError`, là con của nó — và `IndexError`); phần bọc
       chỉ gồm đúng phép đọc và biểu thức tách trạng thái, không bọc thêm gì, và tuyệt đối không bọc
       phép hỏi. Nhận diện "không phân tích được" bằng kiểm tra dữ liệu thay cho bắt ngoại lệ cũng
       được; Q-A không quy định cách. Ngoại lệ ngoài hai nhóm ấy (ví dụ `RuntimeError`,
       `KeyboardInterrupt`) thoát ra nguyên đối tượng.
     · Bản vá KHÔNG được dùng `except Exception` hay `except BaseException` ở cả hai tầng. Ngoại lệ
       `OSError` thoát ra khỏi đường lỗi mới là vi phạm objective.
  6. Nhánh Windows và Darwin, thứ tự các nhánh khác: không đổi.

  **Hệ quả còn lại, khai thẳng:** nếu cả `stat` lẫn phép đọc nội dung đều không dùng được và PID là
  một zombie, hàm báo "còn sống" (vì `kill(pid, 0)` thành công với zombie), và deadline trả 125 thay
  vì 124. Đó là hướng fail-closed — khai "chưa giết được", không khai sai "đã giết" — và là đúng cái
  giá của lời hứa *"không tự khẳng định đã chết khi không có bằng chứng"*. Bảng 2 (cột 4) đo ra
  đúng như vậy. Nó là hành vi được chấp nhận của r2, không phải lỗi cần sửa ở đây.

  **Nội dung `/proc/<pid>/stat` hỏng — hai đường, hai kết quả, CÓ CHỦ Ý (r3 nói thẳng điều r2 chỉ để
  suy ra).** Hành vi mong đợi lấy đúng từ mã sẵn có, `launcher.py:652–656` trên `89fc4fa`: nhánh CŨ
  (phép hỏi thành công, tệp có) bọc phép đọc và biểu thức tách trạng thái trong một khối bắt `OSError`,
  `ValueError`, `IndexError` và trả **`False`**. Q-A.3 giữ nhánh ấy nguyên xi (§2). Nhánh MỚI (phép hỏi
  ném `OSError` khác ESRCH): nội dung đọc được nhưng không phân tích được ⇒ **rơi về `os.kill(pid, 0)`**
  như Q-A.4 đã viết, tức trả `True` cho PID sống, KHÔNG trả `False`. Hai đường lệch nhau về nội dung
  hỏng, và chính độ lệch ấy là chỗ một bản vá dùng chung MỘT khối bắt cho cả hai đường sẽ trượt sang
  `False` trên đường mới (đột biến (i) ở B5). Dạng nội dung "không phân tích được" đã đo (bảng 3):
  rỗng, và thiếu dấu đóng ngoặc ⇒ `ValueError`; hết chuỗi ngay sau dấu đóng ngoặc, có hoặc không có
  khoảng trắng cuối ⇒ `IndexError`; không giải mã được ⇒ `UnicodeDecodeError` (con của `ValueError`,
  KHÔNG thuộc `OSError`). Dạng thứ tư không phải suy diễn: `comm` của tiến trình đặt được bằng
  `prctl(PR_SET_NAME)` với byte không phải UTF-8, và khi đó `read_text` thật trên `/proc/<pid>/stat`
  ném đúng `UnicodeDecodeError` (bảng 4).
- **Mission #686 Q1:** ca khoá trong `.claude/dev/launcher_test.py`; xếp sau #668.
- **Mission #686 Q3:** executor Sonnet 5.5, effort high.
- **Mission #686 Q4:** không chạy CI Windows trên PR (không gắn nhãn `windows`, không gọi tay).
  `launcher-windows.yml` tự chạy ở `push` master với `paths: .claude/dev/**`, nên **lần merge là
  lần đo Windows đầu tiên** của bản vá; đọc kết quả ấy là một `land_obligation`.
- **Hệ quả của Q4 cộng chỉ thị thường trực "không chạy CI trên PR làm bằng chứng"** (nói thẳng,
  không che): trên PR thi hành, **không có lượt CI nào chạy `launcher_test.py`** — job `launcher` bị
  tắt trên PR không nhãn `windows` (Q4), và `gate-registry` không chạy tệp này (§8). Bằng chứng thay
  thế duy nhất trước merge là log cục bộ Linux ở B6.

## 4. `write_set`

- `.claude/dev/launcher.py`
- `.claude/dev/launcher_test.py`

Không đường dẫn nào khác. Đặc tả này (`ops/specs/launcher-con-song-esrch-r3.md`) là hồ sơ của lượt
soạn, không thuộc write set thi hành.

## 5. `ngoai_pham_vi`

- `:359`, `:430`, `:484` và mọi chỗ đọc `/proc` đã có `try`; nhánh cũ `exists()` đúng mà `read_text`
  lỗi (§2).
- Nhánh Windows và Darwin của `_con_song`.
- `t125`/`t154` trong `ops/lease_publish_test.py`: không sửa; chúng chỉ là nơi lỗi lộ ra.
- `.github/workflows/**` và `.claude/dev/ci_dang_ky_test.py`. `DA_NOI` (`ci_dang_ky_test.py:69–78`,
  13 mục, trong đó có `launcher_test.py`) chỉ giúp `kiem()` xác nhận rằng có một dòng `run:` trong
  workflow nhắc tới tệp test; nó **không** đưa tệp vào nhóm `MOI` mà `gate-registry` thực thi
  (`ci_dang_ky_test.py:37–53`, 9 mục, không có `launcher_test.py`). Q4 giữ nguyên: PR không nhãn
  `windows` chưa đo `launcher_test.py` qua CI; B6 cục bộ là bằng chứng bắt buộc trước merge. Muốn
  thêm job Linux chạy suite này trên PR thì phải mở revision, authority và write set riêng — packet
  này không tự sửa CI. (Đo 11:14Z 29-09: `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 2`,
  gồm #668 và `ci-duong-nhanh-ho-so-r2-g3-claude`; thêm một lý do để không đụng tệp này.)
- Chạy lại job CI của PR #679: không làm (chỉ thị thường trực).

## 6. `muc_tieu`

1. `.claude/dev/launcher.py` — Chặn lỗi của phép hỏi `trang_thai.exists()` theo Q-A: `ProcessLookupError`
   ⇒ `False`; `OSError` khác ⇒ thử đọc nội dung trước (đúng một lần), rồi mới rơi về `os.kill(pid, 0)` —
   kể cả khi đọc lỗi hoặc nội dung không phân tích được (Q-A.4, và đoạn làm rõ ở §3: đường mới KHÁC đường
   cũ ở điểm này). Bảo toàn phép phân biệt zombie trong đường lỗi mới. Kèm chú thích theo idiom của tệp
   (nguồn lỗi ESRCH: PR #679, job `109303373142`; nguồn lỗ zombie: cross-review lượt 1 trên PR #688;
   nguồn ba đường nuốt sentinel / nội dung hỏng / đọc hai lần: cross-review lượt 2 trên PR #688).
2. `.claude/dev/launcher_test.py` — **Hai ca mới**, tên nối tiếp hậu tố lớn nhất: `t156_...` (B1, B2,
   B3, B4) và `t157_...` (B3b), theo §7. Hậu tố `t155` là lớn nhất của các ca mang tiền tố `t` trên
   `89fc4fa` (đếm ở §8); executor **đo lại hậu tố trên nền tiếp nối** trước khi đặt tên vì #668 cũng
   giữ tệp này. Các mục `DOT_BIEN` mới: **đúng theo danh sách ở B5, và chỉ ở đó** — §6 không lặp lại
   con số. Số ca mới và số mục đột biến là hai đơn vị khác nhau. Hai ca dựng trên MỘT helper theo nhãn
   (quy ước chung ở §7); helper ấy và các đơn vị nhãn nằm trong hai ca mới của `launcher_test.py`, không
   thêm tệp, không thêm ca đăng ký, không sửa runner `--dot-bien`.

## 7. `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3). Đột biến chạy trên **bản sao tạm**, bằng chính
`python .claude/dev/launcher_test.py --dot-bien`. Quy ước chung cho hai ca mới:

- Mỗi `bang(...)` mang **nhãn** ở đầu thông điệp (`B1`, `B2-eacces`, …) để một đột biến chết đúng chốt
  của nó phân biệt được với chết ở chốt khác của cùng ca.
- Seam chỉ chạm đúng `/proc/<pid>/stat` của PID đang xét, có **bộ đếm lần chạm**; ca xác nhận seam đã
  chạm ở từng lời gọi (seam không chạm ⇒ ca không đo gì). Lấy khoá danh tính **trước** khi đặt seam.
- Ca chỉ chuyển **đúng đối tượng ngoại lệ do seam tạo ra** thành `bang(False, ...)`. Cấm
  `except Exception`/`except BaseException` rồi đổi mọi thứ thành `TinHieuChotCa`: ngoại lệ vô can
  phải giữ hạng vô can (runner in kiểu ngoại lệ trong ngoặc sau tên ca — đó là tín dụng giả).
- Sinh tiến trình con: `start_new_session`, tín hiệu thật, dọn bằng **PID tường minh** trong `finally`
  (`kill` rồi `wait`); không `pkill`, không đoán nhóm. Nếu không dựng được điều kiện (ví dụ con không
  chuyển sang `Z` trong thời hạn có trần), ca ném lỗi thường, KHÔNG dùng `bang`.
- **Cấu trúc theo nhãn, MỘT helper dùng chung (r3, lớp `chot-nguoc-khong-co-lap`).** Mỗi nhãn là một
  đơn vị độc lập gồm: đầu vào (seam + lời gọi) và nhóm assertion mang nhãn ấy (kết quả, không-lộ-ngoại-
  lệ, seam đã chạm, bộ đếm). Hai ca đăng ký gọi CÙNG một helper dựng từ các đơn vị đó; helper nhận hai
  tham số tuỳ chọn mà ca đăng ký KHÔNG truyền — tập nhãn CHẠY (mặc định: tất cả, theo thứ tự dưới đây)
  và tập nhãn NỚI (mặc định: rỗng); tên tham số do executor đặt. **"Nới nhãn L"** nghĩa là: đầu vào của
  L vẫn chạy nguyên (seam vẫn đặt, lời gọi vẫn thực hiện), nhưng MỌI assertion mang nhãn L bị bỏ, và
  nếu chính đối tượng ngoại lệ do seam của L tạo ra thoát khỏi lời gọi thì nó bị nuốt (so bằng danh
  tính); mọi ngoại lệ khác vẫn thoát. Nới KHÔNG được là cách để bỏ đầu vào, bỏ thiết lập hay trả sớm.
  Hai ca đăng ký vẫn chỉ là hai ca (§6.2): phép đo dùng tham số là lời gọi TRỰC TIẾP helper từ tập
  lệnh bằng chứng của executor, trên bản sao đột biến (cùng cách B5 đã đòi gọi thẳng hàm ca) — không
  phải ca đăng ký thứ ba và không sửa runner `--dot-bien`.
- **Thứ tự thực thi cố định** trong `t156_...`, đúng thứ tự liệt kê ở đây: `B1`, `B2-eacces`, `B2-eio`,
  `B2-doc-hong`, `B2-tin-hieu`, `B2-dem-lan`, `B2-exception`, `B2-parse`, `B2-dem-doc`, `B3-song`,
  `B3-da-wait`, `B3-zombie`. `bang` ném ở assertion sai ĐẦU TIÊN, nên nhãn báo là nhãn đầu tiên trong
  thứ tự này; B5 dựa vào điều đó. `t157_...` chỉ có `B3b-giet-cay`. B4 không phải nhãn (nó là điều kiện
  nền).

**Ca `t156_...`**

- **B1 (mục 2) — ESRCH.** Seam ném `ProcessLookupError(errno.ESRCH, …)`. Gọi `_con_song(os.getpid())`,
  `_con_song_dung_khoa(os.getpid(), <khoá thật>)` và `_giet_rieng({<pid con đã wait>: "k"}, 0)`: không
  ngoại lệ nào thoát; hai hàm đầu trả `False`. Nhãn `B1`.
  **ĐỎ khi:** chạy trên nền `89fc4fa` ⇒ `ProcessLookupError` thoát ⇒ ca đổi đúng đối tượng ấy thành
  `bang(False, …)` của chính nó.
- **B2 (mục 2) — miền lỗi khác ESRCH, chống bản rộng và bản hẹp giả.** Trên `os.getpid()` (PID sống):
  - `B2-eacces`: seam `PermissionError(errno.EACCES, …)` ⇒ `_con_song` trả **`True`**. **ĐỎ khi** bản
    RỘNG (`except OSError: return False`) ⇒ `False`.
  - `B2-eio`: seam `OSError(errno.EIO, …)` ⇒ `True`, không ngoại lệ nào thoát. **ĐỎ khi** bản chỉ bắt
    `PermissionError`: EIO thoát ra, trái objective "mọi `OSError`".
  - `B2-doc-hong`: seam EACCES ở `stat` **và** seam EACCES ở `read_text` của cùng PID ⇒ `True` (không
    đọc được thì rơi về `kill(pid, 0)`, không tự khẳng định đã chết). **ĐỎ khi** đường đọc hỏng trả
    `False`.
  - `B2-tin-hieu` (tầng hỏi): seam ném sentinel `KeyboardInterrupt` ⇒ ca bắt NGAY quanh lời gọi và so
    **đúng đối tượng**; trả về bình thường thay vì truyền sentinel ra ⇒ đỏ. **ĐỎ khi** bản vá nuốt
    `BaseException`.
  - `B2-dem-lan`: seam theo thứ tự — lần hỏi thứ nhất đi `stat` thật, lần thứ hai ném ESRCH; một lời gọi
    `_con_song` phải chạm seam **đúng một lần** và trả đúng theo trạng thái thật. **ĐỎ khi** bản vá gọi
    `exists()` lần hai: `ProcessLookupError` từ lần hai thoát ra, hoặc bộ đếm lần chạm ≠ 1.
  - `B2-exception` (r3) — miền `Exception` KHÔNG thuộc `OSError` (sentinel `RuntimeError`), **hai tầng,
    hai đầu vào, cùng một nhãn**; thông điệp `bang` ghi tiểu nhãn `hoi` hoặc `doc` ngay sau nhãn.
    · `hoi`: seam `Path.stat` của PID sống ném MỘT đối tượng `RuntimeError` dựng sẵn. `_con_song` phải
      để CHÍNH đối tượng ấy thoát ra. Ca bắt ngay quanh lời gọi và so bằng danh tính (`is`); trả về
      bình thường (kể cả `True`) thay vì ném ⇒ `bang(False, …)`. Đối tượng khác thoát ra ⇒ không bắt
      (vô can).
    · `doc`: seam `Path.stat` ném EACCES (để vào bước 4 của Q-A) và seam `Path.read_text` của đúng
      PID ấy ném MỘT đối tượng `RuntimeError` dựng sẵn khác; chính đối tượng đó phải thoát ra. Cùng
      cách bắt và so như `hoi`.
    **ĐỎ khi:** phép hỏi (đầu vào `hoi`) hoặc khối đọc (đầu vào `doc`) bắt `Exception`. Lý do có nhãn
    này: `KeyboardInterrupt` ở `B2-tin-hieu` thuộc `BaseException` nên bản `except Exception` cho nó
    thoát nguyên, và một mình nó không phân biệt được `except OSError` với `except Exception` (bảng 3:
    `RuntimeError` bị nuốt trong khi B1–B3b của r2 vẫn PASS).
  - `B2-parse` (r3) — nội dung đọc được nhưng KHÔNG phân tích được, trên đường MỚI (Q-A.4 và đoạn làm
    rõ ở §3; đường cũ trả `False` và không thuộc nhãn này). Bốn đầu vào, PID sống (`os.getpid()`),
    seam `Path.stat` ném EACCES, và seam `Path.read_text` của đúng đường `/proc/<pid>/stat`:
    (a) trả chuỗi rỗng; (b) trả chuỗi thiếu dấu đóng ngoặc, ví dụ `<pid> x S 1`; (c) trả chuỗi hết
    ngay sau dấu đóng ngoặc, ví dụ `<pid> (x)`, và cả biến thể có khoảng trắng cuối; (d) ném một
    `UnicodeDecodeError` do ca dựng sẵn (dạng "không giải mã được", có thật: bảng 4). Mỗi đầu vào:
    `_con_song(os.getpid())` phải trả **`True`** (rơi về `kill(pid, 0)`), không ngoại lệ nào thoát.
    **Trong nhãn này KHÔNG ngoại lệ nào được đổi thành `TinHieuChotCa`**: ngoại lệ nào thoát ra khỏi
    `_con_song` (kể cả `ValueError`/`IndexError` của phép tách, kể cả `UnicodeDecodeError` do seam) là
    lỗi vô can, giữ hạng vô can — ca đỏ vì lỗi ấy đúng là ca đỏ (ứng viên không xử lý nội dung hỏng),
    nhưng đó KHÔNG phải một đột biến bị giết đúng lý do (bảng 3, hàng "tầng đọc chỉ bắt `OSError`").
    **ĐỎ khi** (đột biến (i)): đường nội dung hỏng trả `False` ⇒ chết bằng assertion kết quả `True`.
  - `B2-dem-doc` (r3) — số lần ĐỌC nội dung. Gọi `_con_song(os.getpid())` TRỰC TIẾP (không qua
    `_con_song_dung_khoa`), ba đầu vào: (1) `stat` EACCES + `read_text` thật thành công; (2) `stat`
    EIO + `read_text` thật thành công; (3) `stat` EACCES + `read_text` ném EACCES (đọc lỗi). Trong mỗi
    đầu vào, số lần `Path.read_text` chạm đúng đường `/proc/<pid>/stat` của PID ấy **bên trong cửa sổ
    lời gọi `_con_song`** phải bằng **đúng 1** (gồm cả nhánh đọc thành công lẫn nhánh đọc lỗi). Cửa sổ
    đếm chỉ bao lời gọi: mọi lần đọc kiểm soát do chính ca thực hiện (ví dụ đọc để xác nhận trạng
    thái) nằm NGOÀI cửa sổ — lượt 2 đã đo trường hợp nhầm: cộng lần đọc kiểm soát vào thì bản đúng
    báo 2 (VERDICT lượt 2, hướng 7). Phép đọc khoá của wrapper (`_khoa_danh_tinh`, `:359`) không thuộc
    bộ đếm này vì ca gọi trực tiếp. Bộ đếm là lớp quan sát: nó chuyển tiếp sang `read_text` thật và
    KHÔNG thay nội dung, trừ ở các đầu vào "đọc hỏng" đã khai (đầu vào (3) này, và bốn đầu vào của
    `B2-parse`). Giữ nguyên các kiểm đếm `stat` hiện có (`B2-dem-lan`). **ĐỎ khi** (đột biến (j)): bộ
    đếm ≠ 1, tức đọc lại lần hai, ở nhánh nào cũng vậy.
  - **Ma trận tầng × miền của r3** — chốt nào đặt ở tầng nào; ô nào KHÔNG có đầu vào thì nói thẳng là
    KHÔNG ĐO ĐƯỢC, không mượn ô khác che. Đây là bảng có thẩm quyền để suy ra các mục `DOT_BIEN` (dòng biến thể) ở B5:

    | miền | tầng hỏi (`stat`/`exists`) | tầng đọc (`read_text`, bước 4) |
    |---|---|---|
    | `OSError` — ESRCH | `B1` | KHÔNG CÓ đầu vào: KHÔNG ĐO ĐƯỢC |
    | `OSError` khác | `B2-eacces` (`PermissionError`), `B2-eio` (`OSError` EIO) | `B2-doc-hong` (chỉ EACCES; EIO/ESRCH ở tầng đọc KHÔNG ĐO ĐƯỢC — cùng khối bắt `OSError`, EACCES làm đại diện) |
    | `Exception` không thuộc `OSError` | `B2-exception` tiểu nhãn `hoi` | `B2-exception` tiểu nhãn `doc` |
    | `BaseException` không thuộc `Exception` | `B2-tin-hieu` (`KeyboardInterrupt`) | KHÔNG CÓ đầu vào: KHÔNG ĐO ĐƯỢC |
    | nội dung đọc được nhưng hỏng (`ValueError`, `IndexError`, `UnicodeDecodeError`) | — | `B2-parse` (bốn đầu vào) |
    | số lần hỏi / số lần đọc | `B2-dem-lan` (đúng 1) | `B2-dem-doc` (đúng 1, ở nhánh đọc thành công và nhánh đọc lỗi) |

    Ba ô "KHÔNG ĐO ĐƯỢC" (ESRCH ở tầng đọc; EIO ở tầng đọc; `BaseException` ở tầng đọc) là **quyết định
    phạm vi của r3, không phải bỏ sót ngầm**: thêm chúng là thêm đầu vào và đột biến, và r3 dừng ở những gì
    lượt 2 đã đo được. Executor KHÔNG được viết vào handoff rằng các ô ấy "đã khoá".
- **B3 (mục 2) — đối chứng dương, và zombie chưa `wait`.** Không seam: `_con_song(os.getpid())` ⇒
  `True` (nhãn `B3-song`); `_con_song` trên PID con đã `wait` ⇒ `False` (nhãn `B3-da-wait`). Rồi một
  con thật, session riêng, SIGTERM thật,
  đọc `/proc/<pid>/stat` bằng phép đọc **độc lập với launcher** cho tới khi thấy `Z`, **chưa `wait`**;
  đặt seam EACCES chỉ ở `Path.stat` của PID ấy (để `read_text` thật vẫn đọc được): `_con_song` và
  `_con_song_dung_khoa` đều phải `False`. Nhãn `B3-zombie`.
  **ĐỎ khi:** đột biến bỏ phép đọc nội dung trên đường lỗi mới, rơi thẳng về `kill(pid, 0)` ⇒ `True`.
  B3 cũ của r1 (chỉ PID đã `wait`) giữ làm đối chứng nhưng KHÔNG đủ: nó xanh với bản HẸP r1.
- **B4 (mục 2) — nền.** Ngoài Linux (`LA_WINDOWS`, Darwin) hai ca **trả chuỗi lý do** (BỎ QUA có khai
  theo quy ước sẵn của tệp), không trả QUA: nhánh `/proc` không tồn tại ở đó.

**Ca `t157_...`**

- **B3b (mục 2) — chốt tiêu thụ `_giet_cay`.** Con thật CÒN SỐNG, session riêng, `khoa` lấy trước seam;
  seam EACCES ở `Path.stat` của PID ấy; gọi `_giet_cay(pid, khoa)` để SIGTERM thật biến con thành
  zombie chưa `wait`; kết quả phải có `tron_ven=True` (phía deadline ánh xạ 124, `launcher.py:1669`).
  Nhãn `B3b-giet-cay`. Dọn PID con và `wait` trong `finally`. Ca này riêng để đột biến (c) ở B5 làm
  **cả hai** ca `t156_...` lẫn `t157_...` đỏ, mỗi ca bằng `TinHieuChotCa` của chính nó.
  **ĐỎ khi:** đột biến bỏ phép đọc nội dung ⇒ `tron_ven=False` ⇒ tương ứng 125 (bảng 2, hàng HẸP r1).

**Các chốt chung**

- **B5 (mục 2) — `DOT_BIEN`: DANH SÁCH CÓ THẨM QUYỀN DUY NHẤT của đột biến mới.** Mọi chỗ khác trong
  đặc tả (kể cả §6) chỉ trỏ về đây. Executor **đếm lại** trên mã thực thi và khai. **Mười LỚP** đột biến
  (a)–(j), mỗi lớp trỏ đích là ca mới; số mục `DOT_BIEN` thật suy ra từ quy tắc ngay sau danh sách (kỳ
  vọng **mười hai**):
  (a) gỡ bản vá (trả `:651` về nguyên dạng nền) ⇒ `t156_...` đỏ ở `B1`;
  (b) thay bản vá bằng bản RỘNG ⇒ `t156_...` đỏ ở `B2-eacces`;
  (c) bỏ phép đọc nội dung trên đường lỗi mới, chỉ hỏi `kill(pid, 0)` ⇒ **cả** `t156_...` (đỏ ở
  `B3-zombie`) **và** `t157_...` (đỏ ở `B3b-giet-cay`);
  (d) chỉ bắt `PermissionError` ở phép hỏi, để EIO thoát ⇒ `t156_...` đỏ ở `B2-eio`;
  (e) nuốt `BaseException` quanh phép hỏi ⇒ `t156_...` đỏ ở `B2-tin-hieu`;
  (f) hỏi `exists()` lần hai ⇒ `t156_...` đỏ ở `B2-dem-lan`;
  (g) khi không đọc được nội dung, trả `False` thay vì rơi về `kill(pid, 0)` ⇒ `t156_...` đỏ ở
  `B2-doc-hong`;
  (h) thay bắt `OSError` bằng `Exception`, giữ nhánh ESRCH riêng ⇒ `t156_...` đỏ ở `B2-exception` với
  sentinel `RuntimeError`; dựng ở **hai** vị trí, mỗi vị trí một mục `DOT_BIEN` (xem "Quy tắc mục
  `DOT_BIEN`" dưới): ở phép hỏi (đầu vào `hoi`) và ở khối đọc (đầu vào `doc`);
  (i) khi phân tích nội dung hỏng, trả `False` thay vì hỏi PID dự phòng ⇒ `t156_...` đỏ ở
  `B2-parse` bằng assertion kết quả, không phải `ValueError` vô can;
  (j) đọc nội dung dự phòng lần hai ⇒ `t156_...` đỏ ở `B2-dem-doc`; dựng ở **hai** vị trí: lần đọc thứ
  hai đặt sau lần đọc thành công, và lần đọc thứ hai đặt trong xử lý lần đọc lỗi.

  **Quy tắc mục `DOT_BIEN` (r3).** (a)–(j) ở trên là mười LỚP. Mỗi mục `DOT_BIEN` là một bản sao đột
  biến có tên riêng và làm đúng một thay đổi ở đúng một vị trí mã (một mục ghép hai vị trí thì không tách
  được vị trí nào bị giết, nên không hợp lệ); vì thế số mục `DOT_BIEN` = số **dòng biến thể**, suy ra từ các
  ô có đầu vào: mỗi dòng ứng với một lớp ở một vị trí mã mà ma trận ở B2 (hoặc B1, B3, B3b cho (a), (b),
  (c)) có đầu vào để làm nó đỏ; ô "KHÔNG ĐO ĐƯỢC" không sinh dòng. Kỳ vọng: (a)–(g) mỗi lớp một dòng, (i)
  một dòng, (h) hai dòng, (j) hai dòng ⇒ **mười hai mục `DOT_BIEN`**; executor đếm lại trên mã của chính
  mình và khai từng dòng (một dòng không dựng được ở cách triển khai đã chọn phải khai KHÔNG ĐO ĐƯỢC kèm
  lý do, không lặng lẽ bỏ). Vì (c) làm đỏ hai ca, dòng (c) mang hai kết quả đích. Con số "mười hai" là kỳ
  vọng suy ra, không phải danh sách thứ hai: danh sách có thẩm quyền vẫn là (a)–(j) cùng quy tắc này. Lưu ý
  khác biệt so với r2: r2 gọi "bảy mục" và mỗi mục là một mục `DOT_BIEN`; r3 tách "lớp" khỏi "mục" để khỏi
  đọc "mười" thành số mục cần đăng ký.

  Mỗi đột biến phải chết **bằng `TinHieuChotCa` của đúng ca đích, đúng nhãn**, không bằng lỗi vô can
  (bài học *"ĐỘT BIẾN BỊ GIẾT KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO"*). Runner hiện có in tên ca kèm
  kiểu ngoại lệ trong ngoặc khi ngoại lệ KHÔNG phải `TinHieuChotCa`, và vẫn cho `OK giet 1/1` — nên
  KHÔNG dùng riêng rc hay chữ `OK` của runner. Phân hạng bằng cách đọc kiểu ngoại lệ, tên ca và nhãn
  (gọi thẳng hàm ca trên bản đột biến để đọc thông điệp `TinHieuChotCa`; runner chỉ in tên ca) và khai
  **ba hạng**: giết thật / tín dụng giả / sống sót, mỗi mục một dòng. Kèm một đối chứng cố ý vô can (ví
  dụ đột biến gây `NameError`) để chứng minh cách phân hạng không cấp tín dụng giả. Hạng "tín dụng giả"
  gồm mutant chết vì ngoại lệ vô can, và mutant chết bằng `TinHieuChotCa` của một ca KHÁC ca đích. Chết ở
  một nhãn khác của CÙNG ca đích thì không phải tín dụng giả nhưng phải khớp quy tắc nhãn của phép (A1)
  dưới đây.

  **Chốt ngược — hai phép đo riêng, không gộp (r3, lớp `chot-nguoc-khong-co-lap`).** Câu của r2 ("nới ca
  đích để nó không kiểm chốt ấy nữa thì mục tương ứng phải chuyển sang sống sót") không xác định phạm vi,
  và khi nhiều assertion phủ giao nhau thì đọc nó theo nghĩa nào cũng sai: đọc là "nới đúng nhãn mà cả ca
  phải sống" thì bác một bộ test đúng; đọc là "tắt cả ca" thì có cặp đỏ/xanh mà không chứng minh nhãn
  nào có răng. Số đo (rig của cross-review lượt 2, dựng theo B1–B3b của r2, chạy lại lúc 11:46:05Z và 11:46:12Z 29-09):
  nới riêng `B1` thì (a) vẫn chết ở `B2-eacces`; nới riêng `B2-eacces` thì (b) vẫn chết ở `B2-eio`; để cả
  ca sống, (a) phải nới cả năm nhãn `B1`, `B2-eacces`, `B2-eio`, `B2-doc-hong`, `B3-zombie`, còn (b) phải
  nới ba nhãn `B2-eacces`, `B2-eio`, `B2-doc-hong`. Đó là các chốt có ích chồng lên nhau, không phải test
  yếu, và **không được xoá cho gọn**. r3 tách hai phép đo, mỗi dòng biến thể chạy CẢ HAI, ở từng ca đích
  ((c): làm riêng cho `t156_...` và cho `t157_...`):
  · **(A) CA ĐẦY ĐỦ.** Gọi hàm ca đăng ký (mặc định của helper: mọi nhãn chạy theo thứ tự, không nới) trên
    bản sao đột biến. Đo hai lần: **A1** không nới gì; **A2** nới đúng nhãn đích, mọi nhãn khác vẫn hiệu lực.
  · **(W) WITNESS CÔ LẬP.** Gọi TRỰC TIẾP cùng helper ấy (không viết lại assertion ở chỗ thứ hai — hai
    bản sẽ trôi lệch), chỉ chạy đầu vào của nhãn đích. Đo hai lần: **W1** nhãn đích không bị nới; **W0**
    nhãn đích bị nới.

  | phép | đầu vào chạy | assertion còn hiệu lực | kết quả cần có |
  |---|---|---|---|
  | A1 | mọi nhãn, đúng thứ tự | mọi assertion của mọi nhãn (kể cả kiểm seam đã chạm và bộ đếm); assertion sai đầu tiên ném | chết bằng `TinHieuChotCa` của ca đích; nhãn báo = nhãn đích, hoặc một nhãn đứng TRƯỚC nhãn đích trong thứ tự thực thi (khai rõ nhãn nào — hợp lệ) |
  | A2 | mọi nhãn, đúng thứ tự | mọi assertion trừ nhãn đích | KHÔNG đòi gì; khai "sống sót" hoặc "chết ở nhãn Y" (Y là nhãn giết kế tiếp, luôn khác nhãn đích) |
  | W1 | chỉ đầu vào của nhãn đích | chỉ assertion mang nhãn đích | chết bằng `TinHieuChotCa` mà thông điệp mở đầu bằng nhãn đích |
  | W0 | chỉ đầu vào của nhãn đích (vẫn chạy nguyên) | không assertion nào của nhãn đích; còn lại chỉ lỗi thiết lập và ngoại lệ vô can | sống sót (helper trả về bình thường); bộ đếm seam của nhãn ≥ 1 (chứng tỏ đầu vào ĐÃ chạy) |

  Tiêu chí, mỗi dòng biến thể: **ĐỎ** khi A1 sống sót; khi A1 báo nhãn đứng SAU nhãn đích (nhãn đích
  không còn răng hoặc ánh xạ sai); khi W1 không chết đúng nhãn đích; hoặc khi W0 không sống sót. **KHÔNG ĐO
  ĐƯỢC** (không phải giết, không phải sống sót) khi W0 chết bằng ngoại lệ vô can hoặc bộ đếm seam của W0
  bằng 0 — dòng ấy chưa có chốt ngược, và handoff khai thẳng như vậy. A2 là dữ kiện cho log, không phải điều
  kiện đạt. **Không tính là chứng cứ ngược:** bỏ cả ca hoặc trả sớm; nới bằng cách xoá đầu vào; kết luận
  "sống" từ một W0 mà đầu vào không chạy. **Không nới suite thường:** ca đăng ký gọi helper KHÔNG truyền
  tham số nào, và chính A1 trên ca đăng ký khoá điều đó (một thay đổi làm mặc định của helper nới một nhãn
  thì mutant hướng vào nhãn ấy sống ở A1 ⇒ ĐỎ). **Log mỗi dòng biến thể**: tên mục và vị trí, ca đích,
  nhãn đích, A1 (nhãn báo), A2 (sống sót hoặc nhãn Y — đây là "các nhãn khác vẫn giết nó trong ca đầy đủ";
  danh sách ĐỦ mọi nhãn giết được nó cần nới tuần tự và không bắt buộc), W1, W0 kèm bộ đếm seam.
  Cách làm là khả thi, không phải lời hứa: trên rig của lượt 2, chạy lại 11:46:06Z, witness cô lập cho
  đúng cặp — (a) nhãn `B1`: W1 chết `B1`, W0 sống sót; (b) nhãn `B2-eacces`: W1 chết `B2-eacces`, W0 sống
  sót; ba biến thể mới: W1 chết ở `B2-exception`, `B2-parse` và nhãn đếm-đọc (rig gọi là `B2-readcount`,
  đặc tả gọi là `B2-dem-doc`), W0 cả ba sống sót. Đó là rig của reviewer trên bản nháp Q-A, KHÔNG phải
  phép đo trên ứng viên của executor.
- **B6 (cả write set) — delta và bằng chứng cục bộ thay CI.**
  `python .claude/dev/launcher_test.py` toàn suite **delta = 0 ca đỏ** so với nền, đo **cả hai vế trong
  một lệnh** trên cùng rig (bài học "PHÉP ĐO DELTA SO HAI VẾ": nền và ứng viên cùng dựng bằng một vòng
  lặp, cùng bước). `python .claude/dev/launcher_test.py --dot-bien`: không đột biến cũ nào đổi hạng.
  `python -m ruff check --select F .claude/dev/launcher.py .claude/dev/launcher_test.py`: delta F = 0
  (ruff vắng thì ghi `KHÔNG ĐO ĐƯỢC`, không ghi 0). Nền đo được ở r3 (11:49:59Z 29-09, `89fc4fa`,
  ruff 0.15.8 là NHỊ PHÂN độc lập `ruff`, vì `python -m ruff` vắng ở cả `python` lẫn `python3.12` của
  container này): `launcher.py` 0 lỗi F; `launcher_test.py` 5 lỗi F (cả năm là F841, dòng 2566, 3387,
  3629, 4110, 6061). "delta = 0" nghĩa là ứng viên KHÔNG hơn số nền ấy, đo lại trên nền tiếp nối.
  **Nghĩa vụ bằng chứng.** Mọi lệnh B1–B6 chạy **cục bộ trên Linux, đúng SHA ứng viên** (ghi
  `git rev-parse HEAD` cùng log). Log mỗi lệnh gồm: lệnh **nguyên văn**, giờ UTC bắt đầu, rc, và
  **dòng tổng nguyên văn** của runner (số qua / chạy / bỏ qua / đỏ; với `--dot-bien` là dòng tổng và
  ba hạng của B5). Log của B5 còn kèm **từng dòng biến thể** với bốn phép đo A1/A2/W1/W0 như đã định
  ở B5 (kỳ vọng mười hai dòng, cũng là mười hai mục `DOT_BIEN`). Đính vào handoff; reviewer đọc **trước** merge. Xanh của `gate-registry` KHÔNG thay
  cho log này (§8). Sau merge, `launcher-windows.yml` chạy ở lượt `push` master: đọc kết quả cả
  Windows lẫn Ubuntu (`land_obligation`), đừng suy thành công từ việc đã đẩy.
  **ĐỎ khi:** ứng viên có thêm ca đỏ, đột biến cũ đổi hạng, thêm lỗi F, hoặc handoff thiếu log nguyên
  văn cho bất kỳ lệnh nào trong B1–B6.
- **B7 — bằng chứng từ nơi lỗi lộ ra (không phải cổng).** Chạy `ops/lease_publish_test.py` với seam
  ESRCH chèn vào `launcher.py` bản sao tạm, hoặc chạy `t154` lặp nhiều lần song song: chỉ để khai,
  **không** dùng làm tiêu chí vì race chập chờn không đỏ ổn định (luật L3). Cross-review lượt 1
  (hướng 10) đã chạy `t154` với seam ở bản sao: nền ném `ProcessLookupError`, bản HẸP r1 qua.
  Cross-review lượt 2 (hướng 13, 11:29:11Z 29-09) chạy lại trên bản dựng theo Q-A r2: nền ném
  `ProcessLookupError` sau 1 lần chạm seam; bản dựng qua, 31 lần chạm seam, 4,87 giây, các tiến trình con
  cháu được thu hồi hết. Đó là số của reviewer trên bản nháp, không phải phép đo trên ứng viên của
  executor và không do phiên soạn r3 chạy lại.

## 8. Số đo nền (thời điểm đo cạnh từng số)

- **`origin/master` đã tiến; nền nghiệm thu `89fc4fa` vẫn hợp lệ cho write set (đo lại ở r3).**
  Lệnh và kết quả, 29-09: `git fetch -q origin '+refs/heads/*:refs/remotes/origin/*'` rc=0 (11:44:35Z, rồi
  lại 11:56:41Z); `git rev-parse origin/master` ⇒ `1c23933b13f33d6b0ebdb2901a3dec33c474d34c` ở lần đầu,
  ⇒ `c57df32f0fd8c992ed363d7000f4f761275750ea` ở lần sau (`1c23933` là cha thứ nhất của nó). Reflog
  `refs/remotes/origin/master` ghi ba mục liên tiếp `89fc4fa` ⇒ `1c23933` ⇒ `c57df32`, cả ba là
  `fast-forward`; mục thứ hai là lần fetch 11:44:35Z của r3, còn mục thứ ba do một lần fetch KHÔNG phải của
  phiên soạn r3 (r3 chỉ chạy `git fetch` lúc 11:44:35Z và 11:56:41Z, lần sau không đổi gì) — kho
  `/home/user/tra-luat` được dùng chung, nên đầu `origin/master` có thể trôi giữa hai lệnh. Trên đầu hiện tại:
  `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py
  .claude/dev/launcher_test.py` ⇒ **rc=0** (11:56:41Z; cũng rc=0 với `1c23933` ở 11:44Z), tức hai tệp trong
  write set giống hệt. `git rev-list --count 89fc4fa..origin/master` ⇒ 14 commit (11 không phải merge);
  `git diff --shortstat 89fc4fa origin/master` ⇒ **8 tệp, 3100 dòng thêm, 0 xoá**: `ops/land/pr680-wp676-
  land-evidence.yaml`, `ops/leases/t131-deadline-dem-spawn-exec-1-claude-20260929.yaml` và sáu tệp
  `ops/specs/lease-id-ep-kieu-yaml-r1.md`…`-r6.md`; số tệp đổi dưới `.claude/` hoặc `.github/` = **0**
  (`git diff --name-only … | grep -c`). Cùng lúc, ba tệp CI liên quan (`.claude/dev/ci_dang_ky_test.py`,
  `.github/workflows/ci.yml`, `.github/workflows/launcher-windows.yml`) giống hệt (`git diff --quiet`, rc=0,
  11:56:41Z), nên các số ở mục "Đường thực thi" dưới đây còn nguyên. Hai lần ghi
  `89fc4fa` cũ ("đo lại 11:09Z và 11:14Z") vẫn đúng như đã đo lúc ấy; r3 KHÔNG thay nền bằng đầu mới, vì
  nền nghiệm thu neo theo nội dung write set và nó không đổi.
  So hai nguồn ref (11:56:41Z, sau fetch): `git ls-remote --heads origin` rc=0 ⇒ **516** nhánh trên máy
  chủ; **517** ref cục bộ `refs/remotes/origin/*` sau khi loại `HEAD`. So bằng TẬP TÊN (`comm`): thiếu
  cục bộ (có trên máy chủ, không có cục bộ) = **0**; thừa cục bộ = **1** (`claude/bookkeeping-574-land`,
  không còn trên máy chủ — vô hại, cùng nhánh thừa đã ghi ở r2; lần đo 11:44:40Z ra cùng 516/517 và cùng
  kết luận). Kho không nông (`--is-shallow-repository` ⇒ `false`), `core.abbrev` = 7. Không gặp `CHAN [12]`
  nên không phải sửa nhánh cục bộ `master`.
- Kích thước trên `origin/master` (`git show origin/master:<tệp> | wc -l`, 11:49:30Z, khi đó là `1c23933`;
  blob đo lại trùng ở `c57df32` nhờ `git diff --quiet` rc=0 ở trên):
  `launcher.py` 4308 dòng (blob `561ff7a1…`, sha256 `808ce5b3…9fc0`); `launcher_test.py` 8354 dòng (blob
  `abf7f6c…`; sha256 tệp `433af9d4…556a`). Blob của cả hai tệp ở `89fc4fa` và ở `origin/master` trùng nhau
  (`git rev-parse <ref>:<tệp>`).
- **Số ca của `launcher_test.py`, đếm bằng AST** (11:10:16Z 29-09, trên `origin/master:.claude/dev/launcher_test.py`;
  đo lại 11:46:05Z bằng probe `inventory` của lượt 2 trên bản sao rig, ra CÙNG số dưới đây;
  đếm hàm mức đỉnh mang decorator `@ca`): **189 ca đăng ký = 155 ca tiền tố `t<số>` + 34 ca khác**
  (các ca tiền tố `r`: `r01`–`r21`, `r345`×5, `r347`×2, `r351`×3, `r348`×2, `r349`×1). Hậu tố lớn nhất
  của nhóm `t` là `t155`; 155 hậu tố phân biệt, không trùng, không hổng trong 1..155. **155 không phải
  tổng suite**: nó là hậu tố lớn nhất của một nhóm; bản r1 dùng nó làm tổng và sai. Nghiệm thu B6 phải
  đối chiếu số đăng ký, số chạy, số bỏ qua và số đỏ, không suy tổng từ hậu tố. Sau packet này, số đăng
  ký kỳ vọng tăng đúng bằng số ca mới ở §6.2 (**hai**) — executor đếm lại và khai.
- `DOT_BIEN` ở `launcher_test.py:7012`: **174 mục**; `DOT_BIEN_HARNESS` ở `:7930`: 3 mục (cùng phép đếm
  AST, 11:10:16Z; đo lại 11:46:05Z, cùng số). Đây là số mục ĐỘT BIẾN, khác số ca. Số mục mới: xem B5
  (**mười** lớp, kỳ vọng **mười hai** mục `DOT_BIEN`; sau packet: 174 + 12 = 186 nếu đúng kỳ vọng — số kỳ
  vọng, chưa đo).
- **Lease** (chạy trong `/home/user/tra-luat` sau `git fetch` đủ, 29-09; lệnh `python ops/lease_publish.py
  ai-dang-giu <đường dẫn>`; hai lượt đo, mỗi lượt cùng kết quả — 11:45Z–11:49Z và 11:56Z–11:57Z, dưới đây ghi
  giờ lượt sau):
  `.claude/dev/launcher.py` ⇒ rc=0, `NGƯỜI_GIỮ 0: không có` (11:56:47Z);
  `.claude/dev/launcher_test.py` ⇒ rc=11, `NGƯỜI_GIỮ 1: ci-g5-cong-cu-chia-manh-r1-g2-claude`
  (`CÒN_HẠN`; hết hạn `2026-09-30T07:41:00Z`; 11:56:57Z);
  `.claude/dev/ci_dang_ky_test.py` ⇒ rc=11, `NGƯỜI_GIỮ 2: ci-duong-nhanh-ho-so-r2-g3-claude,
  ci-g5-cong-cu-chia-manh-r1-g2-claude` (11:57:08Z; thêm một bản `ci-duong-nhanh-ho-so-r2-g2-claude` hiện
  `CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ`, không tính là người giữ);
  `.github/workflows/launcher-windows.yml` ⇒ rc=0, `NGƯỜI_GIỮ 0` (11:57:20Z).
  Không lần nào gặp `CHAN [12]`. Nhánh `ops/cap-lease-ci-g5-cong-cu-chia-manh` (lease #668) nay ở
  `2ae5646de60219638c2fef8f838cd86920537154` (r2 ghi `7c16d11`): một commit hồ sơ review, tệp lease g2
  không đổi (xem `depends_on`).
- Tìm Issue/PR có sẵn cho `ProcessLookupError` / `_con_song` ⇒ 0 kết quả (09:4xZ, phép đo của r1; r2 và
  r3 KHÔNG đo lại). Tìm Issue cho quan sát `comm` không phải UTF-8 (§2): chưa làm.
- **Đường thực thi `launcher_test.py` trong CI** (đọc mã ở `ci_dang_ky_test.py` trên `89fc4fa`, đo bằng
  AST và chạy thử 11:09:52Z; cross-review lượt 1 đo độc lập bằng cách chạy `chay_moi` với worker giả;
  lượt 2 lặp lại ở hướng 4, 11:24:58Z: 9 lượt gọi worker, 0 lượt `launcher_test.py`; r3 đếm lại
  `MOI` = 9 mục ở `:37` và `DA_NOI` = 13 mục ở `:69`, `launcher_test` chỉ ở `DA_NOI`, 11:55:42Z):
  - `MOI` = dict ở `:37–53`, **9 mục**: `doc_receipt_thu_hoi_test`, `chon_reviewer_test`,
    `gh_readback_test`, `mcp_gh_test`, `mcp_github_doc_test`, `probe_mang_test`,
    `pretooluse_guard_test`, `subagent_ghi_detect_test`, `ops/nhanh_don_duoc_test`. **`launcher_test.py`
    không thuộc `MOI`.**
  - `DA_NOI` = set ở `:69–78`, **13 mục**, có `launcher_test.py`. `kiem()` (`:578–612`) chỉ đòi rằng mỗi
    mục có một dòng `run:` nhắc tới nó trong workflow — tức "đã nối" chứ **không** "được `gate-registry`
    chạy". Dòng nhắc tới `launcher_test.py` là ở `launcher-windows.yml:104` (suite), `:107` (`--dot-bien`)
    và `:206` (probe `t62`).
  - `chay_moi` = hàm ở `:962–1037`, mặc định `moi=MOI`; `--chay` (khai ở `:2011`; nhánh `if ns.chay` ở `:2043`) gọi đúng hàm này. Vậy
    **`gate-registry` chạy 9 bộ, 0 lượt gọi `launcher_test.py`**.
  - Job `launcher` của `launcher-windows.yml`: PR chỉ chạy khi có nhãn `windows`; push master chạm
    `paths: .claude/dev/**` thì chạy cả Windows (Python 3.13) lẫn Ubuntu (Python 3.11); gọi tay
    `workflow_dispatch` tuỳ tham số `runner_set`. Theo Q4 hai đường đầu không xảy ra trên PR này.
    Bản r1 §8 và closure của r1 khai sai điều này; đã sửa ở r2.
- Suite `launcher_test.py` trên nền: **chưa đo** ở phiên soạn — B6 bắt executor đo cả hai vế.
- Ruff nền (11:49:59Z, `89fc4fa`, nhị phân `ruff` 0.15.8; `python -m ruff` vắng): `launcher.py` 0 lỗi F,
  `launcher_test.py` 5 lỗi F (F841 ×5). Chi tiết ở B6.

Mọi con số phải được **đo lại** trước cấp lease và trước land (L5).

## 9. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục một lượt thất bại. Hình dạng đáng canh, ghi để lượt thi
hành không lặp: *"vá một lỗ mà mở lỗ khác trong cùng hàm"* / *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ
ba"* — và tới r3 nó đã xảy ra **ba lần trong cùng một packet**, cả ba do chính phiên soạn:
1. bản RỘNG (`except OSError: return False`) đóng ESRCH nhưng biến `PermissionError` trên PID sống
   thành "đã chết" (r1 §1);
2. bản HẸP r1 sửa lỗi 1 rồi mở lỗ zombie: đường lỗi mới đi thẳng `kill(pid, 0)` và mất phép phân
   biệt `Z` (bảng 2; cross-review lượt 1 bắt bằng phép đo);
3. **(lượt 2, mới ở r3)** r2 khai rằng nó "liệt kê hết đường TRƯỚC và cho mỗi đường một chốt riêng". Lượt
   2 đo được ba đường r2 KHÔNG có chốt — ngoại lệ thuộc `Exception` nhưng không thuộc `OSError` (một
   mình `KeyboardInterrupt` không phân biệt được), nội dung đọc được nhưng hỏng, và số lần ĐỌC (r2 chỉ đếm
   `stat`) — cả ba biến thể PASS hai ca mẫu (bảng 3), cộng một chỗ hở trong chính chốt ngược (nới đúng
   một nhãn nhưng nhãn khác vẫn giết mutant). Cùng hình dạng "danh sách đường tự liệt kê, cho là hết",
   nhưng nạn nhân lần này là ĐẶC TẢ NGHIỆM THU chứ không phải mã.

Mỗi bản vá/đặc tả đều ĐÚNG và CÓ RĂNG ở chỗ nó phủ; lỗ nằm ở đường KHÔNG ai chỉ. Các phép đo chỉ chứng
minh các đường đã thử. Miền kiểm của r3 gồm ESRCH, EACCES, EIO, zombie, ngoại lệ ngoài `OSError` ở hai
tầng hỏi/đọc, nội dung đọc hỏng và số lần hỏi/đọc; **ma trận ở B2 ghi rõ ô nào có đầu vào, ô nào KHÔNG
ĐO ĐƯỢC** (ESRCH ở tầng đọc; EIO ở tầng đọc; `BaseException` ở tầng đọc). B2 khoá bản RỘNG, B3/B3b khoá bản HẸP r1;
các lớp còn lại ở B5 khoá những biến thể đã liệt kê. **Không coi một danh sách mutant hữu hạn là bằng
chứng đã liệt kê hết mọi đường**; executor và reviewer vẫn phải kiểm các đường mới xuất hiện trong chính
cách triển khai được chọn.

**Ngưỡng ba lần đã chạm — câu hỏi đặt cho điều phối/chủ kho, r3 KHÔNG tự trả lời.** CLAUDE.md dạy đếm
hình dạng lỗi chứ không chỉ đếm lỗi: cùng một hình dạng lặp từ ba lần trở lên thì câu hỏi đúng là "có nên
làm việc này theo cách này không", không phải "vá thế nào". Đường hiện tại (giữ phép hỏi `exists()` rồi
dựng thêm một đường lỗi có đọc + `kill(pid, 0)`, Q-A.1–4) tự nó sinh ra nhiều đường cần chốt — đó là lý do
ma trận ở B2 phình dần từ r1 tới r3. Có thể cân nhắc một cấu trúc ít đường hơn (ví dụ dùng chính phép đọc
làm phép hỏi), nhưng nó đổi hành vi nhánh cũ mà Q-A.3 cấm đổi, và r3 chưa đo phương án nào. Nên r3 giữ
hướng của r2 và chỉ nêu ngưỡng; có hỏi lại quyết định gốc hay không là việc của điều phối/chủ kho.

## 10. `chua_do_duoc`

- Suite `launcher_test.py` và `--dot-bien` trên nền: chưa chạy ở phiên soạn. Phiên soạn r3 chỉ chạy lại
  probe của cross-review lượt 2 (bốn probe: `inventory`, `matrix_extra`, `stronger`, `mutations`, 11:46Z; `inventory` thoát rc=1 ở dòng
  cuối vì bản sao rig không có `SPEC.md`, còn các dòng số đã in đủ trước đó)
  trên hai ca mẫu do reviewer dựng ở bản sao rig; không chạy `python .claude/dev/launcher_test.py` đầy đủ.
- Ruff: đo được **nền** (§8, B6: `launcher.py` 0, `launcher_test.py` 5, nhị phân `ruff` 0.15.8); delta của
  ứng viên: chưa có ứng viên. `python -m ruff` vắng trong container soạn r3 (và trong sandbox của cross-review).
- Nhánh Windows và Darwin: không đo (Q4); lần đo Windows đầu tiên là lượt push master sau merge. Các
  bảng ở §1 chỉ đo Linux, Python 3.12.3 cho bảng 3 và 4. Bảng 4 chỉ đo locale UTF-8 (`preferred_encoding`
  `utf-8`, và `LC_ALL=C.UTF-8`); locale không phải UTF-8: KHÔNG ĐO ĐƯỢC.
- Một ESRCH thật (không seam) trên `/proc/<pid>/stat`: chỉ thấy một lần ở CI (job `109303373142`),
  không tái hiện được theo yêu cầu; seam là cách đo duy nhất ổn định. Tương tự, EACCES/EIO ở `stat`
  của một PID sống chưa từng được thấy trên kernel thật; các bảng 1–3 là đầu vào do seam đặt ra.
- Bản "r2" trong bảng §1 là bản nháp của phiên soạn (Q-A.1–4); chưa có bản vá của executor nào được đo với
  B1–B6. Ba hàng "biến thể" của bảng 3 là đột biến do reviewer lượt 2 dựng, không phải bản nào của executor.
- **Chốt ngược A1/A2/W1/W0 (B5)**: mới thấy chạy trên rig của reviewer, cho năm dòng — (a), (b) và ba
  biến thể mới — bằng helper do reviewer viết (cờ nới `REVIEW_RELAX`). Hợp đồng helper ở §7 là lời văn của
  r3, chưa có cài đặt của executor nào; mười hai dòng của B5 chưa dòng nào được chạy trên ứng viên. Mặc
  định "không nới" của helper chỉ được khoá gián tiếp bởi A1 (không có đột biến harness riêng cho nó).
- Ba ô "KHÔNG ĐO ĐƯỢC" của ma trận B2 (ESRCH ở tầng đọc; EIO ở tầng đọc; `BaseException` ở tầng đọc):
  quyết định phạm vi, không phải đã khoá.
- **Bất đối xứng hai đường về nội dung hỏng** (§2, §3): nhánh cũ trả `False`, nhánh mới rơi về `kill`. Đo
  được rằng nhánh cũ báo "đã chết" cho một PID sống có `comm` không phải UTF-8; chưa tìm Issue cho việc
  này, tần suất ngoài thực tế KHÔNG ĐO ĐƯỢC. Packet này không sửa, và không có ca nào khẳng định nhánh cũ
  đúng.
- Nội dung Mission #686 (Q0–Q5), comment `5888633201`, object ID `5628902742`, trạng thái lease #668
  live: phiên soạn không đọc lại từ GitHub; là lời khai của điều phối (số ở §8 đến từ `ai-dang-giu` chạy
  trên ref đã fetch, không phải từ GitHub live). Băm thân Issue: KHÔNG ĐO ĐƯỢC. Giờ chính xác và ID của
  comment PR #688 chứa VERDICT lượt 2: KHÔNG có trong dữ kiện cấp cho phiên soạn r3.
- Phép đo `t154` của B7: chỉ có số của reviewer lượt 2 trên bản nháp (§7 B7); phiên soạn r3 không chạy
  lại, và không có ứng viên của executor để chạy.
- Tổng số ca `launcher_test.py` và số mục `DOT_BIEN` sau packet: chưa đo (chỉ kỳ vọng ở §8 và B5: 191 ca
  đăng ký, 186 mục `DOT_BIEN`).
