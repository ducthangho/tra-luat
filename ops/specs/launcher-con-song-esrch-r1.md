# ĐẶC TẢ — `LAUNCHER-CON-SONG-ESRCH` — **revision 1, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp685` (ID bền, `wp<issue>`); tên đọc được: `LAUNCHER-CON-SONG-ESRCH`. Lease dùng tên nào cũng phải kèm `packet_issue: 685`. |
| `revision` | **1** |
| `packet_issue` | **#685** |
| `mission_issue` | **#686** (Mission Issue, object ID `5628902742`). Thân #686 khai ngay đầu rằng nó do phiên agent đăng hộ chủ kho bằng credential chủ kho; nguồn thẩm quyền là các câu trả lời của chủ kho được trích trong đó (Q0–Q4). |
| `nguon_cap_viec` | Chỉ thị chủ kho 29-09-2026: *"mở packet riêng cho bản vá launcher (race ProcessLookupError) đi"*. Nguồn lỗi: PR #679, job `gate-ops (ubuntu-latest)` `109303373142`, phân tích ở PR #679 comment `5885963131`. |
| `objective` | `_con_song` không bao giờ để một ngoại lệ `OSError` của phép hỏi `/proc/<pid>/stat` thoát ra; tiến trình biến mất giữa chừng (ESRCH) được báo là đã chết, còn lỗi khác KHÔNG được đọc thành "đã chết". |
| `review_class` | **`sensitive`** — protocol §8: *"launcher hoặc gate lifecycle"*. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | `claude` — **Claude Sonnet 5.5, effort high** (Mission #686 Q3); phiên điều phối kiểm lại độc lập và commit. |
| `environment` | **`cloud`**. Bản vá chỉ chạm nhánh Linux của `_con_song`; nhánh Windows trả về trước dòng 650. |
| reviewer | `codex` (`gpt-6-astra`, effort ≥ medium), cần `cross_approved`. Protocol §8: HINT không được chứa mã launcher; chỉ được chứa mã TEST thuần. |
| `depends_on` | Lease `ci-g5-cong-cu-chia-manh-r1-g2-claude` (packet #668) giữ `.claude/dev/launcher_test.py` tới `2026-09-30T07:41:00Z` (đo 10:04Z 29-09). Phải nhả hoặc hết hạn trước khi cấp lease cho `wp685` (Mission #686 Q1). |
| nền nghiệm thu | `origin/master` `89fc4fac8cea65979cc2483043dc8cd07a6e8518`. Nền tiếp nối (continuation base) sẽ khác khi #668 land trước; khai riêng lúc cấp lease, không thay nền này (protocol §3.2.1). |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/launcher-con-song-esrch-r1.md`, không loại dòng nào. Giá trị được công
bố **ngoài** tệp: comment trên #685 và lease, kèm OID commit + đường dẫn. Khối closure dưới đây
nằm **trong** tệp, nên một `spec_hash` không thể đi với hai closure khác nhau. Đổi bất kỳ byte nào
⇒ revision mới, băm mới, lease mới.

**Closure đóng băng** (các trường dispatcher dẫn xuất, protocol §3.2), điền tay theo **miễn trừ có
phạm vi** ở Mission Issue #686: chỉ `wp685`, hết hiệu lực ở lần đầu một policy canonical cho closure
xuất hiện trên nhánh mặc định.

| trường | giá trị |
|---|---|
| `change_policy_sha` | `null` — chưa có policy canonical; descriptor thay thế là miễn trừ ở #686 |
| `effective_write_set` | `.claude/dev/launcher.py` · `.claude/dev/launcher_test.py` (exact) |
| `effective_review_class` | `sensitive` |
| `required_checks` | Trên PR thi hành: `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-registry (ubuntu-latest)` (chạy `launcher_test.py` qua `ci_dang_ky_test.py --chay`), `gate-packet-loop (ubuntu-latest)` của `.github/workflows/ci.yml`, workflow `thu-hoi`; cross-review codex `cross_approved`, 0 P1/P2/P3 |
| `land_obligations` | Chủ kho audit + merge (không tự merge/approve); đọc kết quả `launcher-windows.yml` ở lượt `push` lên master sau merge và báo; ghi sổ verdict + HINT vào `ops/reviews/` kèm receipt và mục README; thu hồi lease sau land; đóng #685 |

**Descriptor nguồn closure** = `{mission_issue: 686, object_id: 5628902742}`. Lease phải **chép**
đúng các giá trị trên; lệch ⇒ **DỪNG**. Băm thân Issue ở phía nhận là **KHÔNG ĐO ĐƯỢC** từ phiên
soạn (đường đọc MCP chuẩn hoá thực thể HTML trong thân issue, xem CLAUDE.md), nên neo bằng object
ID + số Issue.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

---

## 1. Vấn đề

`.claude/dev/launcher.py:650–651` (trên `89fc4fa`), hàm `_con_song`, nhánh không phải Windows:

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

**Phản chứng chạy được** (đo 10:1xZ 29-09 trên bản sao tạm của launcher `89fc4fa`; seam: vá
`pathlib.Path.stat` ném lỗi cho đường `/proc/*/stat`):

| bản | ESRCH, PID đang sống | EACCES, PID đang sống | không seam: PID sống / PID không tồn tại |
|---|---|---|---|
| nền `89fc4fa` | **ném** `ProcessLookupError` | **ném** `PermissionError` | `True` / `False` |
| bản vá RỘNG (`except OSError: return False`) | `False` | **`False` — SAI** | `True` / `False` |
| bản vá HẸP (Q-A dưới đây) | `False` | `True` (rơi về `os.kill`) | `True` / `False` |

Seam chỉ vá `Path.stat` là đủ tái hiện trên **cả ba** bản Python có trong container: 3.11.15,
3.12.3, 3.13.12 (CI Linux dùng `python-version: "3.12"`).

**Đính chính lời khai của chính phiên soạn:** bản vá đăng ở PR #679 comment `5885963131` và thân
#685 là bản **RỘNG**. Nó đóng ESRCH nhưng biến một `PermissionError` trên PID **đang sống** thành
"đã chết" — đúng lớp lời khai sai *"trả 124 khi tiến trình còn sống"* mà CLAUDE.md đã trả giá.
Đặc tả này chốt bản HẸP.

## 2. Phạm vi đã đo (grep + đọc luồng trên `89fc4fa`)

- Trong `launcher.py` chỉ **một** lời gọi `.exists()` trên đường `/proc`: `:651`.
- Ba chỗ đọc `/proc` khác đều nằm trong `try` bắt `OSError`: `:359` (`_khoa_danh_tinh`), `:430`,
  `:484`. Không cùng dạng lỗi; **không** sửa.
- `_con_song` có năm nơi gọi trong `launcher.py`: `:607` (`_con_song_dung_khoa`), `:857` và `:882`
  (`_giet_windows`, tức nhánh Windows), `:1020` và `:1039` (`_giet_cay`). Đo bằng AST (lần lên cây
  cha tới hàm bao, 10:2xZ 29-09): **không** lời gọi nào nằm trong thân một `try` bao ngoài, nên
  `ProcessLookupError` từ `:651` thoát thẳng khỏi các hàm ấy.
- Executor phải **grep lại** trên nền tiếp nối trước khi sửa và khai mọi chỗ mới tìm thấy.

## 3. Quyết định

- **Q-A — ngữ nghĩa bản vá** (suy từ docstring của `_con_song` và bài học 124/125 trong CLAUDE.md;
  chủ kho có thể bác bằng revision mới): `ProcessLookupError` khi hỏi `stat` ⇒ trả `False` (tiến
  trình đã biến mất). **Mọi `OSError` khác** ⇒ **không** kết luận, rơi về nhánh `os.kill(pid, 0)`
  sẵn có (ở đó `PermissionError` ⇒ `True`, `ProcessLookupError` ⇒ `False`). Không đổi thứ tự hay
  ngữ nghĩa các nhánh khác.
- **Mission #686 Q1:** ca khoá trong `.claude/dev/launcher_test.py`; xếp sau #668.
- **Mission #686 Q3:** executor Sonnet 5.5, effort high.
- **Mission #686 Q4:** không chạy CI Windows trên PR (không gắn nhãn `windows`, không gọi tay).
  `launcher-windows.yml` tự chạy ở `push` master với `paths: .claude/dev/**`, nên **lần merge là
  lần đo Windows đầu tiên** của bản vá; đọc kết quả ấy là một `land_obligation`.

## 4. `write_set`

- `.claude/dev/launcher.py`
- `.claude/dev/launcher_test.py`

Không đường dẫn nào khác. Đặc tả này là hồ sơ của lượt soạn, không thuộc write set thi hành.

## 5. `ngoai_pham_vi`

- `:359`, `:430`, `:484` và mọi chỗ đọc `/proc` đã có `try`.
- Nhánh Windows và Darwin của `_con_song`.
- `t125`/`t154` trong `ops/lease_publish_test.py`: không sửa; chúng chỉ là nơi lỗi lộ ra.
- `.github/workflows/**`, `ci_dang_ky_test.py` (bị #668 giữ; `launcher_test.py` đã có trong sổ
  `DA_NOI`, không cần đăng ký thêm).
- Chạy lại job CI của PR #679: không làm (chỉ thị thường trực).

## 6. `muc_tieu`

1. `.claude/dev/launcher.py` — Bọc `trang_thai.exists()` theo Q-A: `ProcessLookupError` ⇒
   `return False`; `OSError` khác ⇒ coi như không có tệp và rơi về nhánh `os.kill(pid, 0)`. Kèm
   chú thích theo idiom của tệp (nguồn: PR #679, job `109303373142`).
2. `.claude/dev/launcher_test.py` — Một ca mới `t156_...` (số kế tiếp; `t155` là lớn nhất trên
   `89fc4fa`) theo §7, và một mục mới trong `DOT_BIEN`.

## 7. `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3). Đột biến chạy trên **bản sao tạm**, bằng chính
`python .claude/dev/launcher_test.py --dot-bien`.

- **B1 (mục 2) — ca ESRCH.** Seam vá `pathlib.Path.stat` ném `ProcessLookupError(errno.ESRCH, …)`
  cho đúng đường `/proc/<pid>/stat` (mọi đường khác đi `stat` thật). Gọi `_con_song(os.getpid())`,
  `_con_song_dung_khoa(os.getpid(), <khoá thật>)`, `_giet_rieng({<pid không tồn tại>: "k"}, 0)`:
  không ngoại lệ nào thoát; hai hàm đầu trả `False`. Ngoại lệ thoát phải được ca **bắt và biến
  thành `bang(False, …)`** (tức `TinHieuChotCa` của đúng ca này), không để lọt ra như lỗi vô can.
  **ĐỎ khi:** chạy trên nền `89fc4fa` ⇒ `ProcessLookupError` ⇒ ca đỏ bằng tín hiệu của chính nó.
- **B2 (mục 2) — ca EACCES, chống bản vá rộng.** Cùng seam nhưng ném
  `PermissionError(errno.EACCES, …)`: `_con_song(os.getpid())` phải trả **`True`** (rơi về
  `os.kill(pid, 0)` trên chính tiến trình đang chạy).
  **ĐỎ khi:** đột biến thay bản vá hẹp bằng bản RỘNG (`except OSError: return False`) ⇒ `False`.
- **B3 (mục 2) — đối chứng không seam.** `_con_song(os.getpid())` ⇒ `True`; `_con_song` trên một PID
  vừa `wait` xong của tiến trình con do ca tự sinh ⇒ `False`. Giàn hỏng không thể xanh vì đối chứng
  dương này.
- **B4 (mục 2) — nền.** Ngoài POSIX Linux (`LA_WINDOWS`, Darwin) ca **trả chuỗi lý do** (BỎ QUA có
  khai theo quy ước sẵn của tệp), không trả QUA: nhánh `/proc` không tồn tại ở đó.
- **B5 (mục 2) — `DOT_BIEN`.** Thêm **hai** mục, mỗi mục trỏ đích là ca mới:
  (a) gỡ bản vá (trả `:651` về nguyên dạng nền) ⇒ B1 đỏ;
  (b) thay bản vá hẹp bằng bản rộng ⇒ B2 đỏ.
  Mỗi đột biến phải chết **bằng `TinHieuChotCa` của đúng ca mới**, không bằng lỗi vô can (bài học
  *"ĐỘT BIẾN BỊ GIẾT KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO"*). Khai kết quả ba hạng: giết thật / tín
  dụng giả / sống sót.
- **B6 (cả write set) — delta.** `python .claude/dev/launcher_test.py` toàn suite **delta = 0 ca
  đỏ** so với nền, đo **cả hai vế trong một lệnh** trên cùng rig (bài học "PHÉP ĐO DELTA SO HAI VẾ").
  `python .claude/dev/launcher_test.py --dot-bien`: không đột biến cũ nào đổi hạng.
  `python -m ruff check --select F .claude/dev/launcher.py .claude/dev/launcher_test.py`: delta F = 0
  (ruff vắng thì ghi `KHÔNG ĐO ĐƯỢC`, không ghi 0).
  **ĐỎ khi:** ứng viên có thêm ca đỏ, đột biến cũ đổi hạng, hoặc thêm lỗi F.
- **B7 — bằng chứng từ nơi lỗi lộ ra (không phải cổng).** Chạy `ops/lease_publish_test.py` với
  seam ESRCH chèn vào `launcher.py` bản sao tạm, hoặc chạy `t154` lặp nhiều lần song song: chỉ để
  khai, **không** dùng làm tiêu chí vì race chập chờn không đỏ ổn định (luật L3).

## 8. Số đo nền (thời điểm đo cạnh từng số)

- `origin/master` `89fc4fa` (10:04Z 29-09); `launcher.py` 4308 dòng; `launcher_test.py` 8354 dòng,
  155 ca, lớn nhất `t155`.
- `ai-dang-giu .claude/dev/launcher.py` ⇒ `NGƯỜI_GIỮ 0`;
  `ai-dang-giu .claude/dev/launcher_test.py` ⇒ `NGƯỜI_GIỮ 1: ci-g5-cong-cu-chia-manh-r1-g2-claude`
  (10:04Z).
- Tìm Issue/PR có sẵn cho `ProcessLookupError` / `_con_song` ⇒ 0 kết quả (09:4xZ).
- `launcher_test.py` chạy trên Linux qua job `gate-registry` (`ci_dang_ky_test.py --chay`, tệp nằm
  trong `DA_NOI`); trên Windows qua `launcher-windows.yml` (PR: chỉ khi có nhãn `windows`; push
  master: luôn, cả Windows lẫn Ubuntu).
- Suite `launcher_test.py` trên nền: **chưa đo** ở phiên soạn — B6 bắt executor đo cả hai vế.

Mọi con số phải được **đo lại** trước cấp lease và trước land (L5).

## 9. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục một lượt thất bại. Hình dạng đáng canh, ghi để lượt
thi hành không lặp: *"vá một lỗ mà mở lỗ khác trong cùng hàm"* — bản vá rộng của chính phiên soạn
là ví dụ đã đo ở §1; B2 tồn tại để khoá đúng nó.

## 10. `chua_do_duoc`

- Suite `launcher_test.py` và `--dot-bien` trên nền: chưa chạy ở phiên soạn.
- Ruff: chưa đo.
- Nhánh Windows: không đo (Q4); lần đo đầu là lượt push master sau merge.
- Một ESRCH thật (không seam) trên `/proc/<pid>/stat`: chỉ thấy một lần ở CI (job `109303373142`),
  không tái hiện được theo yêu cầu; seam là cách đo duy nhất ổn định.
