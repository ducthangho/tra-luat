# Audit vòng 3 — `.claude/dev/launcher.py` @ `0345ab3`

> **TRẠNG THÁI VÁ.** Ba lỗi CHẶN (§1, §2, §3) đã vá ngay sau báo cáo này — xem mục
> `★ dev-side — vá 3 lỗi CHẶN của audit vòng 3` trong `CHANGELOG.md`. Khoá bằng
> t63…t67 + 5 đột biến; bộ phản chứng 67/67, đột biến 22/22. §1 vá làm HAI lớp vì
> lớp đầu (chỉ đếm thành viên nhóm) vẫn để lọt ca cháu `setsid()` — đã đo lại cả
> hai biến thể trên bản vá. **12 mục NÊN SỬA cũng đã vá nốt** (đợt 2) — xem mục
> `★ dev-side — vá nốt 12 mục NÊN SỬA của audit vòng 3`. Sau hai đợt: bộ phản chứng
> 75/75, đột biến 32/32. Phần GHI NHẬN giữ nguyên làm hồ sơ đo đạc; riêng §19 (tệp tạm
> mồ côi) và §17 (`_con_song` không so khoá) đã vá kèm.



**Nền chạy:** Linux (container Claude Code web thật), Python 3.11.15, git 2.43.0.
**Worktree:** tách rời từ `origin/claude/wp55-r2g2-executor-p4tee0`, **không sửa một tệp nào** —
`git status --porcelain` và `git diff --stat` rỗng ở đầu, giữa và cuối phiên.
**Không chạy được:** mọi phép thử cần Windows thật (VIỆC 2 trọn vẹn). Nói rõ ở từng chỗ,
không suy diễn.

---

## VIỆC 1 — chạy thật, báo số

| lệnh | kết quả |
|---|---|
| `python3 .claude/dev/launcher.py doctor` | rc=0 · `DU CONG CU BAT BUOC` · thiếu `codex` (chỉ cảnh báo) |
| `python3 .claude/dev/launcher_test.py` | **62/62 ca (qua 60, bỏ qua 2, hỏng 0)** — rc=0 |
| `python3 .claude/dev/launcher_test.py --dot-bien` | **17/17 đạt (1 không đo được)** — rc=0 |
| `git status --porcelain` + `git diff --stat` ngay sau | **rỗng cả hai** |

Hai ca bỏ qua, đúng như bộ test tự khai:

```
BO QUA t61_run_root_khong_ghi_duoc_KHONG_do_traceback: bo qua khi chay bang root
BO QUA t62_qua_han_ma_khong_giet_het_cay_phai_tra_125: chi do duoc tren Windows
```

### Cơ chế "KHÔNG ĐO ĐƯỢC" có thành chỗ giấu thất bại không?

Ép ba tình huống bằng cách **thay bảng `DOT_BIEN` lúc chạy** (không sửa tệp):

```
1. dot bien VO HAI + ca dich CHAY DUOC
   VO_HAI_ca_chay_duoc   SAI  giet 0/1: (khong ca nao chet)
   => 0/1 dat, hong=1, MA THOAT=1                       <-- ĐÚNG, không giấu được
2. dot bien VO HAI + ca dich BO QUA
   VO_HAI_ca_bo_qua      KHONG DO DUOC tren nen nay
   => 0/0 dat, hong=0, MA THOAT=0                       <-- đúng thiết kế
3. TOAN BO khong do duoc (2/2 ca)
   => 0/0 dat, hong=0, khong_do=2, MA THOAT=0           <-- CỔNG XANH MÀ KHÔNG ĐO GÌ
```

**Kết luận:** cơ chế **đúng** ở điều bạn lo — một đột biến có ca đích *chạy được* mà không
bị giết thì báo **SAI** và thoát 1, không có đường giấu. Nhưng nó **không có sàn**: bảng mà
mọi đột biến đều không đo được in `0/0 đạt` và thoát **0**. Đúng cái doctrine trong CLAUDE.md
("đòi hai số BẰNG NHAU") — `0/0` thoả mãn hình thức đó mà chứng minh **con số không**.
Hiện tại 17/18 đo được nên chưa xảy ra; xem NÊN SỬA §11.

---

## VIỆC 2 — t62 trên Windows: **KHÔNG CHẠY ĐƯỢC**

Máy này là Linux. `taskkill`, `Get-Process ... .StartTime.Ticks`, và phân biệt
trong/ngoài sandbox codex đều là hành vi **Windows thật**; cài `pwsh` trên Linux cũng
**không** giúp, vì `_khoa_danh_tinh` gọi `powershell` (Windows PowerShell) và `_giet_windows`
gọi `taskkill.exe` — hai thứ không tồn tại ở đây. Không suy diễn thay.

**Nhưng lý do bỏ qua t62 thì SAI, và đo được ngay trên Linux** — xem CHẶN §1. Việc đó đổi
bản chất VIỆC 2: t62 không phải "ca chỉ Windows mới có", nó là ca **POSIX cũng có mà đang đỏ**.

Điều duy nhất đo được về đường Windows là **logic mã** (ép `platform.system()=='Windows'`,
thay `subprocess.run` bằng bộ đếm) — xem GHI NHẬN §17. Nó xác nhận nhánh rẽ 124/125 đúng
*theo mã*, **không** xác nhận taskkill hành xử ra sao trên Windows.

---

# CHẶN

## §1. POSIX: `ca_cay=True` là LỜI KHẲNG ĐỊNH KHÔNG CÓ BẰNG CHỨNG → trả 124 trong khi cháu còn sống

Nghi vấn 4.1 của bạn **đúng, và rộng hơn bạn nghĩ**. `setsid` chỉ là một đường; đường thứ hai
đơn giản hơn nhiều: **cháu chỉ cần phớt lờ SIGTERM**. Vòng chờ ở `launcher.py:293-299` thoát
ngay khi **tiến trình mẹ** chết, nên `SIGKILL` ở dòng 301 **không bao giờ được gửi**.

Tái hiện (`thu41.sh`, hai biến thể, không sửa launcher):

```
### CA A: cháu TỰ GỌI setsid (thoát nhóm)
trang thai: qua_han  ma_thoat=124
ly do     : qua han: SIGTERM: da tat ca cay
--- CHAU pid=7098 VAN CON SONG  <-- mau thuan voi ma 124
 7098  1  7098 Ss  /usr/local/bin/python3 -c ...
   giet_tron_ven= True

### CA B: cháu CÙNG NHÓM, chỉ phớt lờ SIGTERM
trang thai: qua_han  ma_thoat=124
ly do     : qua han: SIGTERM: da tat ca cay
--- CHAU pid=7116 VAN CON SONG  <-- mau thuan voi ma 124
 7116  1  7115 S   ... signal.signal(SIGTERM, SIG_IGN) ...
   giet_tron_ven= True
```

Ca B là ca nặng: `pgid=7115` — cháu **vẫn nằm trong nhóm**, `killpg(SIGKILL)` sẽ giết được nó,
nhưng mã trả về trước khi tới đó.

**Vì sao đây là CHẶN.** CLAUDE.md của chính kho này viết: *"trả 124 khi tiến trình còn sống là
chốt nói dối"*. Vòng 2 sửa đúng lỗi đó ở Windows rồi để nguyên ở POSIX — nền mà launcher
đang chạy hằng ngày (container remote, CI, máy macOS/Linux). Comment dòng 298
(*"killpg giết theo NHÓM nên cả cây con cháu cùng nhóm đều nhận tín hiệu"*) đúng về tín hiệu
nhưng **nhận tín hiệu ≠ đã chết**, và đó chính là khoảng cách mà vòng 2 đã trả giá để học.

**Kéo theo: hai khẳng định trong tài liệu SAI.**

- `docs/GOI_AGENT_DA_NEN.md:118-119` — *"trên Linux là ca 'mẹ chết mà cháu còn sống' (POSIX
  `killpg` giết theo nhóm nên **không dựng được trạng thái đó**)"*. Tôi dựng được, hai cách.
- `launcher_test.py:1046` (lý do bỏ qua t62) — *"CHỈ ĐO ĐƯỢC TRÊN WINDOWS: trên POSIX `killpg`
  giết theo NHÓM nên **cả cây luôn chết cùng lúc**"*. Chỉ đúng với cháu ngây thơ như fixture
  hiện tại (`time.sleep(8)`); sai với cháu `setsid` hoặc cháu bắt SIGTERM.

Nghĩa là t62 **không phải không đo được trên POSIX — nó sẽ ĐỎ nếu fixture dùng cháu thoát nhóm.**
Việc bỏ qua đang che một khiếm khuyết POSIX thật.

**Đề xuất** (Linux; Darwin thay bằng `ps -o pid=,stat= -g <pgid>`):

```diff
+def _thanh_vien_nhom(pgid: int) -> list[int]:
+    """PID còn SỐNG trong nhóm pgid (bỏ zombie). BẰNG CHỨNG DƯƠNG, không suy đoán."""
+    ra = []
+    for p in Path("/proc").iterdir():
+        if not p.name.isdigit():
+            continue
+        try:
+            nd = (p / "stat").read_text()
+            sau = nd[nd.rindex(")") + 2:].split()
+            if sau[0] == "Z":          # zombie = đã chết
+                continue
+            if int(sau[2]) == pgid:    # trường 5 tính từ 1 = pgrp
+                ra.append(int(p.name))
+        except (OSError, ValueError, IndexError):
+            continue
+    return ra
+
     for _ in range(20):
         time.sleep(0.1)
         if not _con_song(pid):
-            # killpg giết theo NHÓM nên cả cây con cháu cùng nhóm đều nhận tín hiệu
-            return KetGiet(True, True, "SIGTERM: da tat ca cay")
+            # Mẹ chết KHÔNG chứng minh cả cây chết: cháu có thể phớt lờ SIGTERM.
+            con_lai = _thanh_vien_nhom(pid)
+            if not con_lai:
+                return KetGiet(True, True, "SIGTERM: nhom da rong")
+            break                       # còn người trong nhóm -> leo thang SIGKILL
     try:
         os.killpg(pid, signal.SIGKILL)
     except OSError as e:
         return KetGiet(False, False, f"killpg SIGKILL loi: {e}")
     time.sleep(0.3)
-    if _con_song(pid):
-        return KetGiet(False, False, "SIGKILL: KHONG GIET DUOC")
-    return KetGiet(True, True, "SIGKILL: da tat ca cay")
+    con_lai = _thanh_vien_nhom(pid)
+    if _con_song(pid) or con_lai:
+        return KetGiet(not _con_song(pid), False,
+                       f"SIGKILL: con {len(con_lai)} tien trinh trong nhom")
+    return KetGiet(True, True, "SIGKILL: nhom da rong")
```

**Giới hạn phải nói thẳng:** cách trên bắt được ca B (cùng nhóm) nhưng **không** bắt được ca A
(`setsid` thoát nhóm) — không cơ chế nào dựa trên process group làm được. Muốn phủ ca A phải
dùng cgroup v2 (Linux) hoặc Job Object (Windows). Vì vậy docstring `ca_cay` phải hạ giọng
xuống đúng thứ đo được: *"không còn tiến trình sống trong NHÓM"*, chứ không phải "cả cây".

**Khoá lại bằng test:** đổi fixture t62 thành cháu `setsid`/bắt-SIGTERM và **bỏ điều kiện
`if not LA_WINDOWS: return`** — ca này chạy được trên cả hai nền.

---

## §2. `_cap_id`: "mkdir ĐỘC QUYỀN" **không** chặn trùng `short_id` — bản vá vòng 2 không đóng đúng lỗ nó nói

Comment `launcher.py:562-566` viết: *"mkdir KHÔNG exist_ok = hành vi GIÀNH nguyên tử: hai tiến
trình cùng chọn trúng một id thì đúng một bên tạo được. 'Quét rồi mkdir' của bản trước có khe
hở giữa hai bước (audit codex chỉ ra)."*

Thư mục được đặt tên `{sid}-{rid}`, nên `mkdir` độc quyền chỉ chặn **trùng `run_id` đầy đủ**
(uuid4, 2¹²⁸ — chưa ai lo). Cái *thật sự* gây hại — trùng **`short_id`**, thứ docstring hứa
*"ĐẢM BẢO chưa từng dùng"* và *"làm mọi lệnh status/stop trỏ nhầm lượt"* — vẫn chỉ được canh
bằng đúng vòng quét **không nguyên tử** như trước.

Tái hiện (`thu33b.py` — Path-proxy chặn ở `iterdir()` để hai luồng quét xong rồi mới mkdir;
`uuid4` giả trả cùng 8 hex đầu, khác đuôi):

```
luong 0 -> ('cafe1234000000000000000000000002', 'cafe1234')
luong 1 -> ('cafe1234000000000000000000000001', 'cafe1234')
thu muc thuc te: ['cafe1234-cafe...0001', 'cafe1234-cafe...0002']

TRUNG short_id? True   (cafe1234 vs cafe1234)
_tim_luot('cafe1234') -> cafe1234-cafe...0001
=> status/stop cho MOT trong hai luot chay se tro NHAM luot kia.
```

Gọi tuần tự thì vòng quét bắt được đúng (trả `Chan[9]`) — nên lỗi **chỉ hiện khi thật sự đua**,
đúng cửa sổ mà bản vá tuyên bố đã đóng.

**Xác suất thực tế thấp** (2³² + phải đồng thời): 8 lượt `run` song song thật, đo được 0 trùng
(§20). Xếp CHẶN theo đúng yêu cầu của bạn — *"vá của vòng 2 không thật sự ẩn được lỗi"* — chứ
không phải vì nó sắp nổ.

```diff
         thu_muc = run_root / f"{sid}-{rid}"
         try:
+            # GIÀNH short_id trước, nguyên tử: tên thư mục chứa cả rid nên
+            # mkdir của nó KHÔNG bao giờ va nhau khi chỉ trùng short_id.
+            (run_root / f".sid-{sid}").touch(exist_ok=False)
+        except FileExistsError:
+            continue
+        except OSError as e:
+            raise Chan(MA_THAM_SO, f"khong giu duoc short_id: {e}") from None
+        try:
             thu_muc.mkdir(parents=False)
```

(`_tim_luot` và `lenh_status` đều bỏ qua thứ không phải thư mục, nên `.sid-*` vô hại.)

---

## §3. `--run-root` TƯƠNG ĐỐI: sổ ghi `prompt_kin_hoan_toan=True` trong khi con **không nhận được prompt nào** — và trả **rc=0**

`run_root = Path(a.run_root).expanduser()` (dòng 660) **không `resolve()`**, nhưng con được sinh
với `cwd=kq["workspace"]` (gốc repo). Đường dẫn bản chụp thay vào `{PROMPT_FILE}` là **tương đối
theo cwd của launcher**, còn con lại đọc nó **theo gốc repo**. `tim_workspace` quảng cáo rõ là
đứng ở thư mục con vẫn chạy được — nên hai cwd đó lệch nhau là chuyện bình thường.

Tái hiện (`thu31.sh` mục G — chạy từ `repo/con/sau`, `--run-root runs-tuong-doi`):

```
trang thai: xong  ma_thoat=0
rc=0
stdout con : CON KHONG DOC DUOC BAN CHUP
stderr con : cat: runs-tuong-doi/eadae33b-.../prompt.snapshot: No such file or directory
prompt_ban_chup ghi trong so = runs-tuong-doi/eadae33b-.../prompt.snapshot
prompt_kin_hoan_toan        = True      <-- SAI
ma_thoat                    = 0  trang_thai= xong
```

Neo prompt fail-**open** ở dạng tệ nhất: lượt chạy **không hề nhận prompt** được ghi là thành
công sạch, **và** sổ khẳng định prompt đã kín hoàn toàn. Đúng loại "chốt nói dối".

Tài liệu dùng `--run-root ~/.tl-runs` (tuyệt đối sau `expanduser`) nên đường tài liệu không dính —
đây là lỗi **tiềm ẩn**, nhưng không có gì chặn người ta viết `--run-root .runs`.

```diff
-    run_root = Path(a.run_root).expanduser()
+    run_root = Path(a.run_root).expanduser().resolve()
```

(sửa cả ba: `lenh_run:660`, `lenh_status:781`, `lenh_stop:811` — để `status/stop` luôn trỏ
đúng chỗ dù gọi từ thư mục khác.)

---

# NÊN SỬA

## §4. `_kho_khop` **chặn oan** mọi kho có đường dẫn ≥ 4 đoạn, kèm thông điệp tự mâu thuẫn

Luật mới: 3 đoạn = bằng nhau tuyệt đối; 2 đoạn = so hai đoạn cuối; **khác đi = TỪ CHỐI**.
Hệ quả: danh tính đầy đủ, **đúng từng ký tự**, của GitLab subgroup / GHE lồng nhau bị từ chối.

```
remote thuc te : https://gitlab.com/nhom/nhom-con/kho.git
--expected-repo 'gitlab.com/nhom/nhom-con/kho'
  CHAN [11]: kho lech: mong doi gitlab.com/nhom/nhom-con/kho,
                       thuc te ['gitlab.com/nhom/nhom-con/kho']
  rc=11
--expected-repo 'nhom-con/kho'   -> rc=0
```

Hai chuỗi **giống hệt nhau** mà báo lệch — người đọc sẽ đi tìm lỗi ở remote, không ở chốt.
Và người dùng GitLab/GHE **mất hẳn** lựa chọn neo-theo-host: chỉ còn `nhom-con/kho` (không
phân biệt host) hoặc `--expected-root-commit`.

Ma trận đầy đủ (`thu32.py`), remote `https://ghe.example.com/a/b/c/repo.git`:

| expected | kết quả | nhận xét |
|---|---|---|
| `ghe.example.com/a/b/c/repo` | **False** | chặn oan — đúng y nguyên danh tính |
| `ghe.example.com/c/repo` | False | đúng luật (host ⇒ bằng nhau) |
| `c/repo` | True | đúng luật (2 đoạn cuối) |
| `a/b`, `b/c`, `repo` | False | đúng |

Giả mạo vẫn chặn đúng: `evil.example/github.com/o/r` vs `github.com/o/r` → False;
`github.com.evil.io/o/r` → False; `evil.example/localhost/o/r` vs `localhost/o/r` → False.
Bốn cách viết URL vẫn ra một danh tính, token bị cắt sạch:

```
https://github.com/o/r.git                            -> github.com/o/r
git@github.com:o/r                                    -> github.com/o/r
ssh://git@github.com/o/r                              -> github.com/o/r
ssh://git@github.com:22/o/r                           -> github.com/o/r
https://x-access-token:ghp_SECRET123@github.com/o/r.git -> github.com/o/r
```

Rác trong `expected` được tha đúng mức: `/o/r`, `o/r/`, `o/r.git`, `  o/r  `, `O/R`,
`github.com/O/R.GIT`, `o/r.git/` → True; `o//r` → False (đóng, chấp nhận được).

```diff
-    if len(doan_m) == 3:
-        return t == m                      # host/owner/repo -> bằng nhau tuyệt đối
+    if len(doan_m) >= 3:
+        # ≥3 đoạn = người ta đã nêu HOST -> đòi bằng nhau tuyệt đối. Không giới hạn
+        # đúng 3: GitLab subgroup / GHE lồng nhau có 4+ đoạn và LÀ danh tính hợp lệ;
+        # chặn chúng vừa oan vừa in ra thông điệp "mong doi X, thuc te [X]".
+        return t == m
```

Tính an ninh giữ nguyên (vẫn là bằng-nhau-tuyệt-đối), chỉ bỏ chặn oan.

**Khẳng định tài liệu cần sửa kèm:** `docs/GOI_AGENT_DA_NEN.md:81` và CLAUDE.md
(*"Nêu **host** thì chốt đòi bằng nhau tuyệt đối"*) — hiện chỉ đúng khi danh tính có **đúng
3 đoạn**; ngoài ra là từ chối, không phải so sánh.

## §5. Remote đường dẫn ĐỊA PHƯƠNG — trả lời câu hỏi 3.2

`_danh_tinh_remote` trả `None` cho tất cả: `D:\ho-so\kho`, `/srv/kho.git`, `file:///srv/kho.git`,
`C:/ho so/kho`, `../kho-ben-canh`, UNC. Chúng bị **loại khỏi danh sách**, nên **không thể** làm
chốt báo khớp nhầm. Kho chỉ có remote địa phương thì `remotes=[]` → `CHAN [11]: kho lech: mong
doi o/r, thuc te (khong co remote)` — **fail-closed, đúng**.

Ngoại lệ duy nhất: `file://may-chu/o/r` (có phần host) → `may-chu/o/r`. Không phải lỗ hổng
(muốn khớp vẫn phải trùng), chỉ ghi nhận.

Nhiều remote: một cái khớp → **qua** (rc=0); không cái nào khớp → **chặn** (rc=11). Đúng cả hai.

## §6. `stop` một lượt đã kết thúc: chẩn đoán **sai** ("PID đã bị tái dùng") + gắn nhãn lại lượt chạy

```
$ launcher.py run --run-root R --expected-repo o/r -- true      # chạy xong, rc=0
$ launcher.py stop --run-root R --id <sid>
  KET LUAN  : tu choi giet: khoa danh tinh KHAC (PID da bi tai dung)
  rc=10
  so sau stop: trang_thai= da_dung  ma_thoat= 0  giet_tron_ven= False
```

Tiến trình chỉ **thoát bình thường**; PID không hề bị tái dùng. `_giet_cay` gộp
`_khoa_danh_tinh(pid) is None` (đã chết) chung với "khoá KHÁC" (tái dùng thật — mối nguy mà
cả cơ chế khoá sinh ra để bắt). Hai thứ đối lập, cùng một câu chữ, cùng một mã. Thêm nữa, một
lượt **hoàn tất bình thường** bị ghi lại thành `trang_thai=da_dung`.

Trong phép đua §20, **7/12 lần** `stop` trả 10 chỉ vì con đã kịp thoát.

```diff
     if khoa is None:
         return KetGiet(False, False, "tu choi giet: khong co khoa danh tinh")
+    if not _con_song(pid):
+        return KetGiet(True, True, "tien trinh da khong con chay (khong con gi de giet)")
     if _khoa_danh_tinh(pid) != khoa:
         return KetGiet(False, False, "tu choi giet: khoa danh tinh KHAC (PID da bi tai dung)")
```

và trong `lenh_stop`, chỉ đổi `trang_thai` khi thật sự vừa giết được cái gì đó.

## §7. Mã thoát của **con** đè lên toàn bộ bảng mã của launcher

```
con exit 124 -> launcher rc=124      con exit 11 -> launcher rc=11
con exit 125 -> launcher rc=125      con exit  7 -> launcher rc=7
con exit  12 -> launcher rc=12       con exit  3 -> launcher rc=3
```

`rc=124` **không** phân biệt được "launcher cưỡng chế hạn chót và giết được cả cây" với
"con tự thoát 124" — mà con thoát 124 là chuyện thường (con chạy `timeout(1)`, hoặc con là một
launcher khác). Bảng mã ở `launcher.py:30-44` và `GOI_AGENT_DA_NEN.md:87-98` trình bày các mã
này như ngữ nghĩa của launcher, **không một chữ cảnh báo**.

Sổ **có** phân biệt (`trang_thai` = `qua_han` / `xong`). Đề xuất tối thiểu: ghi rõ trong cả hai
bảng rằng 0-255 có thể là của con, và phía gọi tự động phải đọc `trang_thai` trong `run.json`
chứ đừng đọc mã trần.

Bảng mã cũng **thiếu 3 mã mà chương trình thật sự trả**: `130` (Ctrl-C), `141` (đứt ống),
`1` (mã con ngoài 0..255, số thật nằm ở `ma_thoat_that`).

## §8. `{PROMPT_FILE}` mà **không** truyền `--prompt-file` → con nhận chuỗi nguyên văn, rc=0, im lặng

```
$ launcher.py run --run-root R --expected-repo o/r -- bash -c 'echo "con nhan: $1"' _ '{PROMPT_FILE}'
trang thai: xong  ma_thoat=0
rc=0
stdout con: con nhan: {PROMPT_FILE}
```

Người vận hành tin prompt đã được neo; agent nhận một đường dẫn vô nghĩa. Không cảnh báo,
không mã lỗi.

```diff
         else:
             ban_ghi["prompt_kin_hoan_toan"] = False
         _ghi_so(thu_muc, ban_ghi)
+    elif any("{PROMPT_FILE}" in x for x in lenh_con):
+        raise Chan(MA_THAM_SO,
+                   "lenh co {PROMPT_FILE} nhung khong truyen --prompt-file: "
+                   "con se nhan chuoi nguyen van")
```

## §9. `prompt.snapshot` — bề mặt lộ **mới**, đúng như bạn nghi

Bạn bỏ argv khỏi sổ vì lý do bí mật (`_tom_tat_lenh`, dòng 573-588) rồi ghi **toàn văn prompt**
ra đĩa. Đo được:

```
-rw-r--r--  1 root root 26 ... /.../prompt.snapshot     (0644 — MỌI user đọc được)
drwxr-xr-x  2 root root ...   /.../<run-dir>            (0755)
umask hien tai: 0022
```

Và bản chụp **không bao giờ bị xoá** sau khi con thoát.

Đánh giá — **nên giữ**, vì nó là thứ duy nhất đóng được cửa sổ TOCTOU sau khi sinh con (đã
kiểm: hoạt động đúng, §14). Nhưng argv ít nhất là **phù du**; tệp này **vĩnh viễn** và
**world-readable**. Với `--run-root` trong `/tmp` trên máy nhiều người dùng, mọi prompt đọc
được bởi bất kỳ ai. Ba việc:

```diff
-        ban_chup = thu_muc / "prompt.snapshot"
-        ban_chup.write_bytes(b)
+        ban_chup = thu_muc / "prompt.snapshot"
+        # Prompt có thể chứa bí mật — chính vì thế argv đã bị bỏ khỏi sổ. Ghi 0600
+        # ngay từ lúc tạo (write_bytes để lại 0644 theo umask).
+        _fd = os.open(ban_chup, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
+        with os.fdopen(_fd, "wb") as _f:
+            _f.write(b)
```

thêm `os.chmod(thu_muc, 0o700)` ngay sau `_cap_id`, và xoá bản chụp khi con thoát trừ khi
người dùng xin giữ (`--giu-ban-chup`). Không cần "chỉ ghi khi được yêu cầu tường minh" — mặc
định kín + xoá sau là đủ, mà vẫn giữ được bảo đảm.

## §10. Ctrl-C: sổ ghi `trang_thai="xong"` cho lượt chạy **bị ngắt và bị giết**

```
launcher returncode = 130                         <-- đúng
trang_thai    = xong                              <-- SAI
ma_thoat      = 130
ly_do_dung    = bi ngat: SIGTERM: da tat ca cay
con con song? False      moc HOAN-TAT? False      <-- con chưa chạy xong
```

`qua_han` là False nên nhánh cuối rơi vào `"xong"` (dòng 768). `lenh_status` liệt kê đúng
trường `trang_thai` này, nên người/máy đang poll đọc ra "kết thúc bình thường". Đây **đúng lớp
lỗi** đã vá cho `stop` ở f08e45b (t50), chỉ là bỏ sót nhánh KeyboardInterrupt.

```diff
     except KeyboardInterrupt:
         ban_ghi["ly_do_dung"] = "bi ngat: " + _giet_cay(p.pid, khoa).mo_ta
+        bi_ngat = True
         ma = 130
...
-        ban_ghi["trang_thai"] = "qua_han" if qua_han else "xong"
+        ban_ghi["trang_thai"] = ("bi_ngat" if bi_ngat
+                                 else "qua_han" if qua_han else "xong")
```

(khởi tạo `bi_ngat = False` cạnh `qua_han = False`.)

## §11. Cổng đột biến không có **sàn**: `0/0 đạt` → thoát 0

```diff
         hong, khong_do = chay_dot_bien()
         do_duoc = len(DOT_BIEN) - khong_do
+        if do_duoc == 0:
+            print("\n!! KHONG do duoc dot bien nao tren nen nay — cong nay KHONG chung minh gi")
+            return 1
```

## §12. Đăng ký hook trên Windows: **hai lỗi độc lập, cùng hướng**

`.claude/settings.json` hiện dùng:

```json
"command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh\""
```

Tài liệu chính thức (https://code.claude.com/docs/en/hooks):

> The `command` string is passed to a shell: `sh -c` on macOS and Linux, **Git Bash on Windows,
> or PowerShell when Git Bash isn't installed.**

Máy Windows **không có Git Bash** ⇒ chuỗi trên được giao cho **PowerShell**, ở đó:
1. `bash` không tồn tại; **và**
2. `$CLAUDE_PROJECT_DIR` là **biến PowerShell chưa định nghĩa** → nở ra **rỗng**, nên ngay cả
   đường dẫn cũng mất (PowerShell đọc biến môi trường bằng `$env:CLAUDE_PROJECT_DIR`).

Đúng khuôn "hai lỗi ĐỘC LẬP mà CÙNG HƯỚNG" trong CLAUDE.md. Cách đăng ký tốt hơn theo tài liệu —
**exec form**, không qua shell nào cả:

> **Exec form** runs when `args` is present. Claude Code resolves `command` as an executable on
> `PATH` and spawns it directly with `args` as the argument vector. There is no shell...
> Prefer exec form for any hook that references a path placeholder.

```diff
           {
             "type": "command",
-            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh\""
+            "command": "bash",
+            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/session-start.sh"]
           }
```

(Tài liệu cũng có trường `shell` nhận `"bash"`/`"powershell"` nếu muốn ghim tường minh.)
Vẫn cần `bash` trên PATH — nhưng thân hook đã tự chặn bằng `CLAUDE_CODE_REMOTE`, và môi trường
remote là Linux, nên trên Windows nó chỉ là một thông báo hook lỗi vô hại thay vì im lặng hỏng.

**Hook thất bại giữa chừng thì sao** — tài liệu trả lời dứt khoát:

> | `SessionStart` | Can block? **No** | Shows stderr to user only |

Phiên **vẫn chạy tiếp**. Quan trọng hơn:

> The exceptions are `UserPromptSubmit`, `UserPromptExpansion`, and **`SessionStart`, where
> stdout is added as context that Claude can see and act on.**

Nghĩa là `exit 1` ở dòng 84 **không đạt được gì** (không chặn được phiên, Claude không thấy
stderr) — nhưng bảng `doctor` và dòng `THIEU CONG CU BAT BUOC` in ra **stdout** thì Claude
**có** thấy. Thiết kế vô tình đúng; nên ghi lại điều đó vào chú thích để đừng ai "dọn" mấy
dòng echo đó đi.

## §13. `doctor` không đo hai công cụ mà môi trường **thật sự phụ thuộc**: `bash` và `npm`

- `settings.json` gọi hook qua `bash`; `session-start.sh` là bash script. Windows thiếu Git Bash
  ⇒ hook hỏng, mà `doctor` vẫn in `DU CONG CU BAT BUOC`.
- `session-start.sh:32` rẽ nhánh trên `co npm`; `doctor` chỉ đo `node`.

Bảng lệnh cài còn lại **đúng**: `Git.Git`, `Python.Python.3.12`, `BurntSushi.ripgrep.MSVC`,
`OpenJS.NodeJS.LTS` (winget ID hợp lệ), `xcode-select --install`, các gói brew/apt. Bỏ `gh`,
`pwsh` là **cố ý và đúng** (kho dùng GitHub qua MCP). Ba tên `python3/python/py` là đúng —
đo lại hôm nay: container có `python`, `python3`, **không** có `py`.

## §14. Không có timeout ở bất kỳ subprocess nào trên **đường giết**

Chỉ `_phien_ban` (dòng 885) có `timeout=15`. `_git()`, `_khoa_danh_tinh` (`powershell`/`ps`) và
`taskkill` đều **không**. Một `powershell.exe` treo (máy tải nặng, chính sách AV) sẽ **treo
vĩnh viễn** đường cưỡng chế hạn chót — đúng thứ mà `--deadline-utc` tồn tại để bảo đảm.
Thêm `timeout=15` + `except subprocess.TimeoutExpired` cho cả bốn.

## §15. Dấu mốc pip là **bằng chứng ÂM**, không phải bằng chứng dương

Tái hiện chính xác khối `session-start.sh:64-76`:

```
=== A. doi tep roi DOI LAI (A -> B -> A) ===
    requirements='pypdf==4.0' -> CAI (roi dat moc)
    requirements='pypdf==3.0' -> CAI (roi dat moc)
    requirements='pypdf==4.0' -> BO QUA pip        <-- môi trường đang là 3.0
=== B. hai du an KHAC NHAU, requirements.txt GIONG HET, chung TMPDIR ===
    requirements='pypdf==4.0' -> BO QUA pip        <-- chưa từng cài ở dự án này
```

Dấu mốc nói *"đã từng cài sha này ở TMPDIR này"*, không phải *"gói đang có"*. Ca A là lỗi thật:
sau A→B→A môi trường im lặng không khớp `requirements.txt`. Ca B vô hại **ở đây** (pip cài
global, không venv) nhưng sẽ sai ngay khi có venv.

Trong container này `TMPDIR` **không đặt** → mốc nằm ở `/tmp` (per-container), nên rủi ro
"TMPDIR chia sẻ" bị bó hẹp. Đề xuất: đặt mốc theo `(sha, sys.prefix)` và để trong `.git/`
của dự án thay vì `TMPDIR`; hoặc kiểm bằng chứng dương (`pip install --dry-run -r` / thử import).

---

# GHI NHẬN

**§16. VIỆC 4.2 — sạch.** Không chỗ nào trong `launcher.py` quyết định dựa vào chuỗi. Cả ba
điểm quyết định dùng boolean: `ma = MA_QUA_HAN if ket_giet.tron_ven else MA_GIET_HUT` (736),
`return MA_OK if ket.tron_ven else MA_DANH_TINH` (829), `giet_tron_ven=` (733, 826). `mo_ta`
chỉ chảy vào `ly_do_dung` và `print`. `launcher_test.py:808/815` có so chuỗi `"SIGTERM: da tat"`
nhưng đó là **fixture tự nó ghi ra rồi kiểm còn nguyên** (t50), không phụ thuộc chữ của sản xuất.
Nhắc nhẹ: `KetGiet.__str__` trả `mo_ta`, nên `f"{ket}"` vẫn ra chuỗi — cửa quay lại lối cũ vẫn mở,
chỉ là hiện chưa ai đi.

**§17. VIỆC 4.3 — powershell x2 mỗi lượt `_giet_cay`, không phải "nhiều lần".**
Đo bằng cách ép `platform.system()=='Windows'` + đếm lời gọi (không đo được độ trễ thật):

```
NGOAI sandbox (taskkill rc=0, chết): ['powershell','taskkill','powershell'] -> ca_cay=True  -> 124
TRONG sandbox (taskkill rc=1, chết): ['powershell','taskkill','powershell'] -> ca_cay=False -> 125
xau nhat (taskkill rc=1, còn sống) : ['powershell','taskkill','powershell'] -> 125
```

Cộng 1 lần lúc sinh con (`lenh_run:712`) ⇒ **~3 lần/lượt hạn chót**. Với ước lượng ~1s của bạn
là ~3s — chậm nhưng chưa phải vấn đề. **Vấn đề thật là điều kiện tranh chấp**: `_con_song` trên
Windows là `_khoa_danh_tinh(pid) is not None`, **không so với khoá mong đợi**. PID bị tái dùng
trong 1-2s chờ powershell ⇒ đọc thành "còn sống" ⇒ **125 giả**. Fail-closed (an toàn) nhưng báo
động nhầm, và độ chậm làm nó dễ xảy ra hơn. Sửa một dòng: cho `_con_song(pid, khoa)` so khoá.

Nhánh 124/125 theo hai điều kiện sandbox mà bạn hỏi là **đúng theo mã**. Taskkill có thật sự
rc=0 ngoài sandbox / rc=1 trong sandbox hay không thì **KHÔNG ĐO ĐƯỢC ở đây**.

**§18. Ghi sổ đồng thời — sạch.** 8 writer + 3 reader, 60 vòng/writer: **0 lỗi ghi, 0 lần đọc
trúng JSON cụt, 0 tệp `.tmp` sót**. 8 lệnh `run` song song cùng `--run-root`: 8 thư mục,
8 `run.json` đọc được, **0 trùng short_id**, 0 `.tmp`, 0 sổ hỏng, đủ 8 tên. `stop` đua với `run`
đang kết thúc, **12/12 lần** `trang_thai=da_dung` — quyết định của `stop` **không** bị runner đè.
(Lưu ý: `os.replace` đè lên tệp đang được mở đọc là an toàn trên POSIX; trên Windows có thể
`WinError 5` nếu người đọc mở không kèm `FILE_SHARE_DELETE` — **chưa đo được**.)

**§19. Tệp `.tmp` mồ côi tích luỹ vĩnh viễn.** Writer bị SIGKILL giữa `write_text` và `os.replace`
để lại `run.json.<pid>.<uuid>.tmp`. Tên riêng theo pid+uuid (bản vá vòng 2) nên **không bao giờ
bị ghi đè** — khác tên cố định cũ vốn tự lành. Không ai dọn; `status`/`_tim_luot` bỏ qua nên
vô hại về chức năng, chỉ là rác không giới hạn. Đề xuất: dọn `*.tmp` cũ hơn 1 ngày trong `_ghi_so`.

**§20. Bản chụp prompt **hoạt động đúng** ở ba ca còn lại của 3.1.**
- Đổi tệp **sau** khi `run.json` xuất hiện → con vẫn đọc bản chụp:
  `con doc duoc: PROMPT-GOC-KHONG-DUOC-DOI` trong khi `tep goc bay gio: PROMPT-DA-BI-TRAO-DOI`.
- Đổi tệp **giữa lúc kiểm và lúc chạy** → `CHAN [7]: prompt DOI giua luc kiem va luc chay`.
- Không dùng `{PROMPT_FILE}` → `prompt_kin_hoan_toan = False`. Trung thực.
- `{PROMPT_FILE}` nằm trong đối số ghép và **xuất hiện nhiều lần** → thay đúng hết
  (`--file=/…/prompt.snapshot`, `/…/prompt.snapshot:/…/prompt.snapshot`) — `str.replace` thay
  mọi lần, không chỉ lần đầu.

**§21. Tài liệu KHÔNG nói quá về bảo đảm này — nó không nói gì cả.** `{PROMPT_FILE}` **không
xuất hiện một lần nào** trong `docs/GOI_AGENT_DA_NEN.md`. Ví dụ chủ đạo (dòng 57-62) truyền
`--prompt-file nhiem_vu.txt` rồi bảo agent tự đọc `nhiem_vu.txt` theo tên — tức là đường
`prompt_kin_hoan_toan=false`, còn nguyên cửa sổ TOCTOU sau khi sinh con. Cơ chế mạnh có mà
không ai biết để dùng. Nên thêm vào tài liệu và đổi ví dụ chủ đạo sang `{PROMPT_FILE}`.

**§22. Hook đã chạy THẬT trong container remote thật — bằng chứng dương mới.**
Hook chỉ tồn tại trên nhánh này, **không có trên master**, và `settings.json` đang hoạt động
trong phiên của tôi chỉ có `PreToolUse` — nên trước hôm nay **nó chưa từng chạy trong phiên
remote nào**. Đã chạy:

```
[session-start] cai @openai/codex ...
[session-start] cai requirements.txt ...
[session-start] kiem cong cu:
  co codex    codex-cli 0.147.0
KET LUAN  : DU CONG CU BAT BUOC
[session-start] xong
real 0m10.536s     RC-HOOK=0
```

`codex` từ **không có** → `/opt/node22/bin/codex`; mốc `/tmp/.tl_reqs_baa00d08d382f4e9` được tạo;
worktree vẫn sạch. Guard `CLAUDE_CODE_REMOTE` **đủ**: đo trong container này
`CLAUDE_CODE_REMOTE=true` (có thật). `CLAUDE_PROJECT_DIR` không có trong env của shell tôi,
nhưng hook có đường lùi `$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)` — đúng và đã dùng.
Hook **không** đặt `timeout`; lượt lạnh của tôi 10.5s, mạng chậm hơn có thể chạm trần hook —
nên ghim `"timeout"` tường minh (chưa đo tới trần).

**§23. Khẳng định về container trong CLAUDE.md/tài liệu: ĐÚNG, đo lại hôm nay.**
Có `python`, `python3`, `git`, `node`, `npm`, `claude`, `rg`, `bash`; **không** có `codex`
(trước hook), `gh`, `pwsh`, `py`. Khớp từng chữ.

**§24. VIỆC 3.4 — không có fail-open, nhưng 141 nhập nhằng CẢ HAI CHIỀU.**
`doctor` thiếu công cụ + cắt ống, **60 lượt, 0 lần ra 0**:

```
| head -1    -> 141 x1, 12 x29        | head -c 1  -> 12 x30
| head -n 0  -> 141 (mọi lượt)        | true       -> 141 (mọi lượt)
```

Nhưng `doctor` **ĐỦ công cụ** (rc thật = 0) mà bị cắt ống thì:

```
| head -n 0  -> 141, 20/20 lượt       | true -> 141, 20/20 lượt
```

Nên **triệu chứng bạn định sửa vẫn còn**: phía gọi kiểm `rc != 0` vẫn đọc một môi trường **lành
lặn** thành hỏng — chỉ khác là nay sạch sẽ (141) thay vì traceback. Mà kiểm `rc == 12` cũng
không xong, vì lúc thiếu công cụ đôi khi ra 141. `status` giữ đúng mã (0 và 2) kể cả với 6154
byte đầu ra bị cắt; `run` thì **mất** mã thật (con thoát 3 → launcher trả 141).

`session-start.sh` **không** cắt ống nên an toàn. **BrokenPipeError trên Windows**: không đo
được; Python ánh xạ `ERROR_BROKEN_PIPE`/`ERROR_NO_DATA` thành `BrokenPipeError` nên về nguyên
tắc có, nhưng `Select-Object -First 1` của PowerShell là pipeline **đối tượng** trong tiến trình,
dừng thượng nguồn theo cách khác — **phải đo trên Windows mới biết**.

Sửa: giữ mã thật, đừng phát minh 141 khi quyết định đã có.

```diff
     if a.json:
-        print(json.dumps({...}))
+        try:
+            print(json.dumps({...}))
+        except BrokenPipeError:
+            pass          # người đọc đóng ống: KHÔNG đổi kết luận đã tính xong
     return MA_THIEU_CONG_CU if thieu_bat_buoc else MA_OK
```

(áp cho cả nhánh không-json của `lenh_doctor` và `lenh_status`; giữ `except BrokenPipeError`
trong `main` làm lưới cuối.)

**§25. `except BrokenPipeError` trong `main` là anh em của `except Chan`, không bọc nó.**
Nếu `print(f"CHAN [...]", file=sys.stderr)` (dòng 1018) ném BrokenPipeError khi **stderr** cũng
là ống đã đóng, ngoại lệ thoát ra ngoài `main` → traceback thô. Đo thử `check ... 2>&1 | head -c 1`
ra rc=4 sạch, chưa dựng được ca này, nhưng lỗ hình thức vẫn đó. Bọc dòng in stderr bằng
`try/except BrokenPipeError`.

---

## Có vá nào của vòng 2 KHÔNG thật sự ẩn được lỗi?

**Có hai.**

1. **`_cap_id` "mkdir độc quyền"** (§2) — đóng đúng cái collision không ai lo (run_id đầy đủ),
   để nguyên cái nó tuyên bố đóng (short_id). Comment nói sai về việc mình làm.
2. **`BrokenPipeError → 141`** (§24) — dọn traceback (thật sự có giá trị) nhưng **không** dọn
   triệu chứng gốc: phía gọi kiểm `rc != 0` vẫn báo "THIẾU CÔNG CỤ" oan cho môi trường lành.

Còn lại giữ được: giao thức `KetGiet` bằng boolean (§16), `stop` không bị runner đè (§18),
tệp tạm riêng theo writer (§18), bản chụp prompt (§20), chuẩn hoá danh tính remote (§4),
`_kho_khop` chống giả mạo (§4).

---

## Kết luận

**Chưa** — đường Windows chưa đủ tin cậy để thay hai script PowerShell, và **việc còn thiếu
đúng là MỘT: chạy toàn bộ bộ test + `--dot-bien` + t62 trên Windows thật, ở CẢ HAI điều kiện
sandbox/ngoài sandbox, rồi đối chiếu parity với lượt Linux trên cùng đầu vào** — đúng doctrine
"script đa nền phải chạy THẬT trên nền đó" mà chính kho này đã trả giá để học ở r244.

Nhưng phải nói thêm một điều mà vòng này mới lộ ra: **rào cản lớn nhất bây giờ không nằm ở
Windows.** Ba lỗi CHẶN của vòng 3 đều ở **POSIX** — nền mà launcher đang chạy hằng ngày. Cái
nặng nhất (§1) là **đúng lớp lỗi mà vòng 2 đã vá cho Windows rồi bỏ quên ở POSIX**, và nó đang
được che bởi một dòng "chỉ đo được trên Windows" **sai sự thật**. Vá §1-§3 trước; nghiệm thu
Windows sau.
