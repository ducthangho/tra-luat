# ĐẶC TẢ — `LAUNCHER-CON-SONG-ESRCH` — **revision 2, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp685` (ID bền, `wp<issue>`); tên đọc được: `LAUNCHER-CON-SONG-ESRCH`. Lease dùng tên nào cũng phải kèm `packet_issue: 685`. |
| `revision` | **2** |
| `thay_the_cho` | r1 = `ops/specs/launcher-con-song-esrch-r1.md`, sha256 `ee44238c88667e7435abb6b7a513d563d043e8e5e8189e5380f1151b9be337d9`, commit `d96d075` (`d96d0756724d896e025c7405990ef4a406802c76`). r1 giữ nguyên, không sửa đè; r2 là bản duy nhất được cấp lease. |
| `packet_issue` | **#685** |
| `mission_issue` | **#686** (Mission Issue, object ID `5628902742`). Thân #686 khai ngay đầu rằng nó do phiên agent đăng hộ chủ kho bằng credential chủ kho; nguồn thẩm quyền là các câu trả lời của chủ kho được trích trong đó (Q0–Q4 trong thân; Q5 ở comment `5888633201`, xem `nguon_cap_viec`). |
| `nguon_cap_viec` | (r1) Chỉ thị chủ kho 29-09-2026: *"mở packet riêng cho bản vá launcher (race ProcessLookupError) đi"*. Nguồn lỗi: PR #679, job `gate-ops (ubuntu-latest)` `109303373142`, phân tích ở PR #679 comment `5885963131`. (r2) Cross-review lượt 1 trên PR #688, reviewed commit `d96d075`: `changes_requested`, 2 P1 / 3 P2 / 0 P3; VERDICT sha256 `69dbf916648790c7452d6e0bb7fa56b3a44c59df6c568ea29a1c5bf2eba1d9fb` (viết tắt `69dbf916…d9fb`). Mission #686 comment `5888633201` (Q5: điều kiện cấp lease); phiên soạn r2 KHÔNG đọc lại nội dung comment này, coi nó là lời khai của điều phối, và không chép điều kiện nào từ nó vào đặc tả. |
| `objective` | `_con_song` không bao giờ để một ngoại lệ `OSError` của phép hỏi `/proc/<pid>/stat` thoát ra; tiến trình biến mất giữa chừng (ESRCH) được báo là đã chết; lỗi khác KHÔNG được đọc thành "đã chết" chỉ vì không stat được, và một zombie vẫn được báo là đã chết khi nội dung `/proc/<pid>/stat` còn đọc được. |
| `review_class` | **`sensitive`** — protocol §8: *"launcher hoặc gate lifecycle"*. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | `claude` — **Claude Sonnet 5.5, effort high** (Mission #686 Q3); phiên điều phối kiểm lại độc lập và commit. |
| `environment` | **`cloud`**. Bản vá chỉ chạm nhánh Linux của `_con_song`; nhánh Windows trả về trước dòng 650. |
| reviewer | `codex` (`gpt-6-astra`, effort ≥ medium), cần `cross_approved`. Protocol §8: HINT không được chứa mã launcher; chỉ được chứa mã TEST thuần. |
| `depends_on` | Lease `ci-g5-cong-cu-chia-manh-r1-g2-claude` (packet #668) giữ `.claude/dev/launcher_test.py`, `lease_expires_at_utc` = `2026-09-30T07:41:00Z` (đọc từ tệp lease trên nhánh `ops/cap-lease-ci-g5-cong-cu-chia-manh`, commit `7c16d11`; `ai-dang-giu` báo `CÒN_HẠN` lúc 11:14Z 29-09). Phải nhả hoặc hết hạn trước khi cấp lease cho `wp685` (Mission #686 Q1). `.claude/dev/launcher.py`: `NGƯỜI_GIỮ 0` (11:14Z). Chi tiết phép đo ở §8. |
| nền nghiệm thu | `origin/master` `89fc4fac8cea65979cc2483043dc8cd07a6e8518` (đo lại 11:14Z 29-09, vẫn đúng OID này). Nền tiếp nối (continuation base) sẽ khác khi #668 land trước; khai riêng lúc cấp lease, không thay nền này (protocol §3.2.1). |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/launcher-con-song-esrch-r2.md`, không loại dòng nào. Giá trị được công
bố **ngoài** tệp: comment trên #685 và lease, kèm OID commit + đường dẫn. Khối closure dưới đây
nằm **trong** tệp, nên một `spec_hash` không thể đi với hai closure khác nhau. Đổi bất kỳ byte nào
⇒ revision mới, băm mới, lease mới. Băm của r1 (`ee44238c…37d9`) KHÔNG còn dùng để cấp lease.

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

**Thay đổi so với r1** (mỗi dòng ứng với một lớp của VERDICT lượt 1; slug là tên lớp trong bảng lớp):

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

**Bản "r2" trong hai bảng là bản NHÁP của phiên soạn**, dựng ở bản sao tạm chỉ để kiểm hợp đồng Q-A
có thoả được và đo ra số trên. Nó không nằm trong đặc tả này, không phải bản vá đã được chứng nhận;
executor tự viết bản của mình theo lời văn Q-A và tự đo lại.

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
  nhận là đã sửa nó.
- `_con_song` có năm nơi gọi trong `launcher.py`: `:607` (`_con_song_dung_khoa`), `:857` và `:882`
  (`_giet_windows`, tức nhánh Windows), `:1020` và `:1039` (`_giet_cay`). Đo bằng AST (lần lên cây
  cha tới hàm bao, 10:2xZ 29-09; cross-review lượt 1 đo lại độc lập ra đúng năm nơi, 10:52Z):
  **không** lời gọi nào nằm trong thân một `try` bao ngoài, nên `ProcessLookupError` từ `:651` thoát
  thẳng khỏi các hàm ấy.
- Executor phải **grep lại** trên nền tiếp nối trước khi sửa và khai mọi chỗ mới tìm thấy.

## 3. Quyết định

- **Q-A — ngữ nghĩa bản vá.** Q-A là **suy luận của phiên soạn** (từ docstring của `_con_song`, từ
  bài học 124/125 và bài học zombie trong CLAUDE.md, và từ VERDICT lượt 1); **KHÔNG phải quyết định
  chủ kho**. r2 sửa Q-A của r1 theo lượt 1; chủ kho có thể bác bằng revision mới. Hợp đồng, bằng lời:
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
  5. Phạm vi bắt: chỉ họ `OSError`. Ngoại lệ ngoài họ đó (ví dụ `KeyboardInterrupt`) phải thoát ra
     nguyên đối tượng; bản vá KHÔNG được dùng `except Exception` hay `except BaseException`. Ngoại
     lệ `OSError` thoát ra khỏi đường lỗi mới là vi phạm objective.
  6. Nhánh Windows và Darwin, thứ tự các nhánh khác: không đổi.

  **Hệ quả còn lại, khai thẳng:** nếu cả `stat` lẫn phép đọc nội dung đều không dùng được và PID là
  một zombie, hàm báo "còn sống" (vì `kill(pid, 0)` thành công với zombie), và deadline trả 125 thay
  vì 124. Đó là hướng fail-closed — khai "chưa giết được", không khai sai "đã giết" — và là đúng cái
  giá của lời hứa *"không tự khẳng định đã chết khi không có bằng chứng"*. Bảng 2 (cột 4) đo ra
  đúng như vậy. Nó là hành vi được chấp nhận của r2, không phải lỗi cần sửa ở đây.
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

Không đường dẫn nào khác. Đặc tả này (`ops/specs/launcher-con-song-esrch-r2.md`) là hồ sơ của lượt
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
   ⇒ `False`; `OSError` khác ⇒ thử đọc nội dung trước, rồi mới rơi về `os.kill(pid, 0)`. Bảo toàn phép
   phân biệt zombie trong đường lỗi mới. Kèm chú thích theo idiom của tệp (nguồn lỗi ESRCH: PR #679,
   job `109303373142`; nguồn lỗ zombie: cross-review lượt 1 trên PR #688).
2. `.claude/dev/launcher_test.py` — **Hai ca mới**, tên nối tiếp hậu tố lớn nhất: `t156_...` (B1, B2,
   B3, B4) và `t157_...` (B3b), theo §7. Hậu tố `t155` là lớn nhất của các ca mang tiền tố `t` trên
   `89fc4fa` (đếm ở §8); executor **đo lại hậu tố trên nền tiếp nối** trước khi đặt tên vì #668 cũng
   giữ tệp này. Các mục `DOT_BIEN` mới: **đúng theo danh sách ở B5, và chỉ ở đó** — §6 không lặp lại
   con số. Số ca mới và số mục đột biến là hai đơn vị khác nhau.

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
  - `B2-tin-hieu`: seam ném sentinel `KeyboardInterrupt` ⇒ ca bắt NGAY quanh lời gọi và so **đúng đối
    tượng**; trả về bình thường thay vì truyền sentinel ra ⇒ đỏ. **ĐỎ khi** bản vá nuốt `BaseException`.
  - `B2-dem-lan`: seam theo thứ tự — lần hỏi thứ nhất đi `stat` thật, lần thứ hai ném ESRCH; một lời gọi
    `_con_song` phải chạm seam **đúng một lần** và trả đúng theo trạng thái thật. **ĐỎ khi** bản vá gọi
    `exists()` lần hai: `ProcessLookupError` từ lần hai thoát ra, hoặc bộ đếm lần chạm ≠ 1.
- **B3 (mục 2) — đối chứng dương, và zombie chưa `wait`.** Không seam: `_con_song(os.getpid())` ⇒
  `True`; `_con_song` trên PID con đã `wait` ⇒ `False`. Rồi một con thật, session riêng, SIGTERM thật,
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

- **B5 (mục 2) — `DOT_BIEN`: DANH SÁCH CÓ THẨM QUYỀN DUY NHẤT của số mục đột biến mới.** Mọi chỗ khác
  trong đặc tả (kể cả §6) chỉ trỏ về đây. Executor **đếm lại** trên mã thực thi và khai. Bảy mục, mỗi
  mục trỏ đích là ca mới:
  (a) gỡ bản vá (trả `:651` về nguyên dạng nền) ⇒ `t156_...` đỏ ở `B1`;
  (b) thay bản vá bằng bản RỘNG ⇒ `t156_...` đỏ ở `B2-eacces`;
  (c) bỏ phép đọc nội dung trên đường lỗi mới, chỉ hỏi `kill(pid, 0)` ⇒ **cả** `t156_...` (đỏ ở
  `B3-zombie`) **và** `t157_...` (đỏ ở `B3b-giet-cay`);
  (d) chỉ bắt `PermissionError` ở phép hỏi, để EIO thoát ⇒ `t156_...` đỏ ở `B2-eio`;
  (e) nuốt `BaseException` quanh phép hỏi ⇒ `t156_...` đỏ ở `B2-tin-hieu`;
  (f) hỏi `exists()` lần hai ⇒ `t156_...` đỏ ở `B2-dem-lan`;
  (g) khi không đọc được nội dung, trả `False` thay vì rơi về `kill(pid, 0)` ⇒ `t156_...` đỏ ở
  `B2-doc-hong`.
  Mỗi đột biến phải chết **bằng `TinHieuChotCa` của đúng ca đích, đúng nhãn**, không bằng lỗi vô can
  (bài học *"ĐỘT BIẾN BỊ GIẾT KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO"*). Runner hiện có in tên ca kèm
  kiểu ngoại lệ trong ngoặc khi ngoại lệ KHÔNG phải `TinHieuChotCa`, và vẫn cho `OK giet 1/1` — nên
  KHÔNG dùng riêng rc hay chữ `OK` của runner. Phân hạng bằng cách đọc kiểu ngoại lệ, tên ca và nhãn
  (gọi thẳng hàm ca trên bản đột biến để đọc thông điệp `TinHieuChotCa`; runner chỉ in tên ca) và khai
  **ba hạng**: giết thật / tín dụng giả / sống sót, mỗi mục một dòng. Kèm một đối chứng cố ý vô can (ví
  dụ đột biến gây `NameError`) để chứng minh cách phân hạng không cấp tín dụng giả. Kèm chốt ngược cho
  từng mục: nới ca đích để nó không kiểm chốt ấy nữa thì mục tương ứng phải chuyển sang sống sót.
- **B6 (cả write set) — delta và bằng chứng cục bộ thay CI.**
  `python .claude/dev/launcher_test.py` toàn suite **delta = 0 ca đỏ** so với nền, đo **cả hai vế trong
  một lệnh** trên cùng rig (bài học "PHÉP ĐO DELTA SO HAI VẾ": nền và ứng viên cùng dựng bằng một vòng
  lặp, cùng bước). `python .claude/dev/launcher_test.py --dot-bien`: không đột biến cũ nào đổi hạng.
  `python -m ruff check --select F .claude/dev/launcher.py .claude/dev/launcher_test.py`: delta F = 0
  (ruff vắng thì ghi `KHÔNG ĐO ĐƯỢC`, không ghi 0).
  **Nghĩa vụ bằng chứng.** Mọi lệnh B1–B6 chạy **cục bộ trên Linux, đúng SHA ứng viên** (ghi
  `git rev-parse HEAD` cùng log). Log mỗi lệnh gồm: lệnh **nguyên văn**, giờ UTC bắt đầu, rc, và
  **dòng tổng nguyên văn** của runner (số qua / chạy / bỏ qua / đỏ; với `--dot-bien` là dòng tổng và
  ba hạng của B5). Đính vào handoff; reviewer đọc **trước** merge. Xanh của `gate-registry` KHÔNG thay
  cho log này (§8). Sau merge, `launcher-windows.yml` chạy ở lượt `push` master: đọc kết quả cả
  Windows lẫn Ubuntu (`land_obligation`), đừng suy thành công từ việc đã đẩy.
  **ĐỎ khi:** ứng viên có thêm ca đỏ, đột biến cũ đổi hạng, thêm lỗi F, hoặc handoff thiếu log nguyên
  văn cho bất kỳ lệnh nào trong B1–B6.
- **B7 — bằng chứng từ nơi lỗi lộ ra (không phải cổng).** Chạy `ops/lease_publish_test.py` với seam
  ESRCH chèn vào `launcher.py` bản sao tạm, hoặc chạy `t154` lặp nhiều lần song song: chỉ để khai,
  **không** dùng làm tiêu chí vì race chập chờn không đỏ ổn định (luật L3). Cross-review lượt 1
  (hướng 10) đã chạy `t154` với seam ở bản sao: nền ném `ProcessLookupError`, bản HẸP r1 qua; phép đo
  đó chưa áp cho bản r2.

## 8. Số đo nền (thời điểm đo cạnh từng số)

- `origin/master` `89fc4fa` (đo lại 11:09Z và 11:14Z 29-09, sau `git fetch` đủ refspec, rc=0).
  So hai nguồn: 514 nhánh trên máy chủ (`ls-remote --heads`) so với 514 ref cục bộ sau khi loại
  `HEAD`; lần so đầu (11:14:13Z) thiếu 1 nhánh cục bộ (`claude/wp671-windows-bash-nen-escape-g1`, mới
  đẩy) ⇒ fetch lại (11:14:20Z) ⇒ không còn nhánh nào thiếu cục bộ; còn 1 nhánh THỪA cục bộ
  (`claude/bookkeeping-574-land`, không còn trên máy chủ — vô hại). Kho không nông.
- Kích thước trên `origin/master` (`git show origin/master:<tệp> | wc -l`, 11:14:02Z): `launcher.py`
  4308 dòng; `launcher_test.py` 8354 dòng (blob `abf7f6c…`; sha256 tệp `433af9d4…556a`).
- **Số ca của `launcher_test.py`, đếm bằng AST** (11:10:16Z 29-09, trên `origin/master:.claude/dev/launcher_test.py`;
  đếm hàm mức đỉnh mang decorator `@ca`): **189 ca đăng ký = 155 ca tiền tố `t<số>` + 34 ca khác**
  (các ca tiền tố `r`: `r01`–`r21`, `r345`×5, `r347`×2, `r351`×3, `r348`×2, `r349`×1). Hậu tố lớn nhất
  của nhóm `t` là `t155`; 155 hậu tố phân biệt, không trùng, không hổng trong 1..155. **155 không phải
  tổng suite**: nó là hậu tố lớn nhất của một nhóm; bản r1 dùng nó làm tổng và sai. Nghiệm thu B6 phải
  đối chiếu số đăng ký, số chạy, số bỏ qua và số đỏ, không suy tổng từ hậu tố. Sau packet này, số đăng
  ký kỳ vọng tăng đúng bằng số ca mới ở §6.2 (**hai**) — executor đếm lại và khai.
- `DOT_BIEN` ở `launcher_test.py:7012`: **174 mục**; `DOT_BIEN_HARNESS` ở `:7930`: 3 mục (cùng phép đếm
  AST, 11:10:16Z). Đây là số mục ĐỘT BIẾN, khác số ca. Số mục mới: xem B5.
- **Lease** (sau `git fetch` đủ, 11:14Z 29-09):
  `ai-dang-giu .claude/dev/launcher.py` ⇒ `NGƯỜI_GIỮ 0`;
  `ai-dang-giu .claude/dev/launcher_test.py` ⇒ `NGƯỜI_GIỮ 1: ci-g5-cong-cu-chia-manh-r1-g2-claude`
  (`CÒN_HẠN`, rc=11; hết hạn `2026-09-30T07:41:00Z`);
  `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 2` (11:14:59Z);
  `ai-dang-giu .github/workflows/launcher-windows.yml` ⇒ `NGƯỜI_GIỮ 0`.
- Tìm Issue/PR có sẵn cho `ProcessLookupError` / `_con_song` ⇒ 0 kết quả (09:4xZ, phép đo của r1; r2
  KHÔNG đo lại).
- **Đường thực thi `launcher_test.py` trong CI** (đọc mã ở `ci_dang_ky_test.py` trên `89fc4fa`, đo bằng
  AST và chạy thử 11:09:52Z; cross-review lượt 1 đo độc lập bằng cách chạy `chay_moi` với worker giả):
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

Mọi con số phải được **đo lại** trước cấp lease và trước land (L5).

## 9. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục một lượt thất bại. Hình dạng đáng canh, ghi để lượt thi
hành không lặp: *"vá một lỗ mà mở lỗ khác trong cùng hàm"* — và lần này nó xảy ra **hai lần trong cùng
một packet**, cả hai do chính phiên soạn:
1. bản RỘNG (`except OSError: return False`) đóng ESRCH nhưng biến `PermissionError` trên PID sống
   thành "đã chết" (r1 §1);
2. bản HẸP r1 sửa lỗi 1 rồi mở lỗ zombie: đường lỗi mới đi thẳng `kill(pid, 0)` và mất phép phân
   biệt `Z` (bảng 2).
Mỗi bản vá đều ĐÚNG và CÓ RĂNG ở chỗ nó phủ; lỗ nằm ở đường KHÔNG ai chỉ. Chốt: bản vá gồm **nhiều
đường vào** (ESRCH, EACCES, EIO, zombie, tín hiệu ngoài họ `OSError`, số lần hỏi, đọc hỏng) — r2 liệt kê
hết đường TRƯỚC và cho **mỗi đường một chốt riêng** ở B2/B3/B3b và một đột biến riêng ở B5, thay vì vá
theo danh sách đường mà reviewer nêu. B2 khoá bản RỘNG, B3/B3b khoá bản HẸP r1, (d)–(g) khoá các biến
thể còn lại.

## 10. `chua_do_duoc`

- Suite `launcher_test.py` và `--dot-bien` trên nền: chưa chạy ở phiên soạn.
- Ruff: chưa đo (cross-review lượt 1 cũng ghi `python -m ruff` vắng trong sandbox của họ).
- Nhánh Windows và Darwin: không đo (Q4); lần đo Windows đầu tiên là lượt push master sau merge. Các
  bảng ở §1 chỉ đo Linux.
- Một ESRCH thật (không seam) trên `/proc/<pid>/stat`: chỉ thấy một lần ở CI (job `109303373142`),
  không tái hiện được theo yêu cầu; seam là cách đo duy nhất ổn định. Tương tự, EACCES/EIO ở `stat`
  của một PID sống chưa từng được thấy trên kernel thật; bảng 1 và 2 là đầu vào do seam đặt ra.
- Bản r2 trong bảng §1 là bản nháp của phiên soạn; chưa có bản vá của executor nào được đo với B1–B6.
- Nội dung Mission #686 (Q0–Q5), comment `5888633201`, object ID `5628902742`, trạng thái lease #668
  live: phiên soạn không đọc lại từ GitHub; là lời khai của điều phối. Băm thân Issue: KHÔNG ĐO ĐƯỢC.
- Phép đo `t154` của B7 với bản r2: chưa làm.
- Tổng số ca `launcher_test.py` và số mục `DOT_BIEN` sau packet: chưa đo (chỉ kỳ vọng ở §8 và B5).
