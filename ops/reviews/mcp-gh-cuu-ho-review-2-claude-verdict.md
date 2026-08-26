# VERDICT — cross-review VÒNG 2, packet `MCP-GH-CUU-HO` (Issue #319, PR #339)

```
verdict: changes_requested
reviewed_sha: 4aa936e0a3be676ed2492f89b25f9742a249a965
base_sha: b662fe1d07c675a222ae26e734377e305775e4f3
reviewer: claude (nền khác executor `codex`)
do_duoc_ma: CÓ
P1: 4
P2: 5
```

---

## 0. Tôi CÓ chạy được mã — probe trước mọi việc khác

```
$ python3 --version
Python 3.11.15
$ python3 -c 'print("PROBE_OK")'
PROBE_OK
```

Vòng 1 `blocked` vì vỏ shell từ chối `python3`. Ở vòng này `Bash` chạy được: mọi con số dưới đây
là phép ĐO trong container này, không phải đọc mã. Một hạn chế còn lại, khai ngay: lệnh `bash`
nhiều dòng có định nghĩa hàm bị từ chối quyền một lần, nên toàn bộ runner đột biến của tôi được
viết thành **tệp Python riêng** rồi gọi `python3 tệp.py` — không thay đổi phép đo nào.

Trạng thái cây khi bắt đầu và khi kết thúc: `git status --porcelain` **RỖNG**, `git rev-parse HEAD`
= `4aa936e0a3be676ed2492f89b25f9742a249a965`. Mọi đột biến chạy trên **bản sao trong
`tempfile.TemporaryDirectory()`**, không lần nào ghi vào cây làm việc.

Write set đo được đúng ba đường dẫn:

```
$ git diff --numstat b662fe1d... 4aa936e0...
+230  -0  .claude/dev/mcp_gh.py
+610  -0  .claude/dev/mcp_gh_test.py
+315  -0  ops/specs/mcp-gh-cuu-ho.md
```

---

## 1. Nền: bộ test tự chạy

```
$ python3 .claude/dev/mcp_gh_test.py        # rc=0, 4,5s
CA         : 35/35 đạt · 0 đỏ
ĐỘT BIẾN   : đã đo 38/38 tập giết
D8(a) đích nằm trong tập giết: ĐẠT
D8(b) không tập giết rỗng: ĐẠT
D8(c) mọi ca có đột biến canh: ĐẠT
GIAO PHẠM VI:
| b6_bo_chot_init | B6 | D6 |
| b7_bo_cam_ghi | B7-khong-ghi | B7-xoa |
TỔNG: ĐẠT
```

Lời tự khai của executor (`rc=0`, 35/35, 38/38, D8 (a)(b)(c) ĐẠT) **tái lập được từng con số**.
Tôi cũng chạy `chay_dot_bien()` riêng và in **tập giết thật của cả 38 đột biến**: mọi tập đều
KHÔNG rỗng, mọi ca đích đều nằm trong tập của nó, đúng hai giao phạm vi được in ra. `loi runner: []`.

Nhưng lời tự khai đúng **không** làm cổng đúng — ba mục dưới đây đo bằng đột biến của tôi.

---

## 2. ĐỘT BIẾN CỦA REVIEWER — bốn đột biến SỐNG SÓT

Runner riêng: chép `mcp_gh.py` + `mcp_gh_test.py` sang thư mục tạm, sửa **một** chuỗi (đòi
`count(chuỗi) == 1`, lệch thì báo `KHÔNG_ĐO_ĐƯỢC`), chạy `python3 mcp_gh_test.py`, đọc `rc` **và**
dòng tổng kết.

| # | đột biến | ở đâu | kết quả suite |
|---|---|---|---|
| M0 | (không đột biến) | — | `rc=0` · 35/35 · **ĐẠT** |
| **M1** | `if u.hostname != HOST_CHO_PHEP:` → `if False:` | `mcp_gh.py:31` | `rc=0` · 35/35 · **ĐẠT** ⇒ **SỐNG SÓT** |
| **M2** | `if u.scheme != "https":` → `if False:` | `mcp_gh.py:29` | `rc=0` · 35/35 · **ĐẠT** ⇒ **SỐNG SÓT** |
| M3 | `if u.username is not None or u.password is not None:` → `if False:` | `mcp_gh.py:22` | `rc=1` · 34/35 · ĐỎ `A3` |
| M4 | `if u.path not in DUONG_CHO_PHEP:` → `if False:` | `mcp_gh.py:37` | `rc=1` nhưng **CA 35/35 đạt · 0 đỏ**; chỉ D8(a)(b) đỏ ở `a8_bo_actions` |
| M5 | `port = CONG_CHO_PHEP if port is None` → `80 if port is None` | `mcp_gh.py:28` | `rc=1` · 25/35 · 10 ca đỏ |
| M6 | `if code == 301: return None` → gọi `super().redirect_request(...)` | `mcp_gh.py:45-46` | `rc=1` · ĐỎ `A5` |
| M7 | `build_opener(_KhongChuyenHuong())` → `build_opener()` | `mcp_gh.py:56` | `rc=1` · ĐỎ `A5 A6-302 A6-303 A7` |
| M8 | `return nd[0]["text"]` → `[:10]` | `mcp_gh.py:108` | `rc=1` · ĐỎ `B2` |
| M9 | `loi = loi_cong_cu(kq); if loi:` → `if False:` | `mcp_gh.py:221` | `rc=1` · ĐỎ `D1 D2` |
| M10 | `chay_cac_ca` ép `module.CASES = ()` | `mcp_gh_test.py:544` | `rc=1` · `CA 0/0` · ĐỎ |
| **N1** | `d8_ok = not failed and not any(d8_errors)` → `d8_ok = True` | `mcp_gh_test.py:605` | xem §3.2 ⇒ **SỐNG SÓT** |
| **N2** | `mutant_names if d8_ok else ()` → `mutant_names` | `mcp_gh_test.py:607` | xem §3.2 ⇒ **SỐNG SÓT** |
| C4' | `try: fn()` → `try: pass` (đúng đột biến đặc tả nêu cho `C4`) | `mcp_gh_test.py:549` | `rc=1` **nhưng `CA 35/35 đạt · 0 đỏ`** |

Sau mỗi lượt: `git status --porcelain` vẫn RỖNG (không lượt nào đụng cây thật).

---

## 3. Bốn P1

### P1-1 · `chot-dich-credential-khong-co-phan-chung`

`kiem_dich_den` có **sáu** mệnh đề. Chỉ **hai** có ca làm chúng ĐỎ khi bị gỡ:

| mệnh đề | dòng | gỡ ra ⇒ ca nào ĐỎ? |
|---|---|---|
| `username`/`password` | 22 | `A3` — **CÓ** (đo: M3) |
| cổng ≠ 443 | 33 | `A2`, và `A1` — **CÓ** (đo: M5 làm 10 ca đỏ) |
| `query`/`fragment` | 35 | `A2` — CÓ (đột biến `a2_bo_query` của chính bộ test) |
| **`scheme != "https"`** | **29** | **KHÔNG ca nào** (đo: M2 ⇒ `rc=0`, `TỔNG: ĐẠT`) |
| **`hostname != HOST_CHO_PHEP`** | **31** | **KHÔNG ca nào** (đo: M1 ⇒ `rc=0`, `TỔNG: ĐẠT`) |
| **`path not in DUONG_CHO_PHEP`** | **37** | **KHÔNG ca nào** (đo: M4 ⇒ `CA 35/35 đạt · 0 đỏ`) |
| `except ValueError` quanh `u.port` | 24-27 | không ca nào — không ca nào dùng cổng phi số (đọc, chưa đột biến) |

Ba mệnh đề không có phản chứng chính là ba mệnh đề định nghĩa **"nơi nhận credential"** — tức
`muc_tieu` #1, hạng mục số một của packet.

Chốt HOST là chốt **có tải trọng thật**, và đường tới nó đi qua **cờ `--path` của hợp đồng CLI**,
không cần sửa mã: `Phien.__init__` dựng `self.url = DIEM_CUOI + path` (`mcp_gh.py:114`), nên
`--path` nhận một chuỗi không bắt đầu bằng `/` sẽ nối thẳng vào host. Đo:

```
== kiem_dich_den trên BẢN GỐC ==
  host hậu tố   https://api.githubcopilot.com.THUOC_VE_KE_TAN_CONG/mcp/ : CHẶN (host nhận credential không được phép)
  host khác hẳn                                                          : CHẶN
  http không TLS  http://api.githubcopilot.com/mcp/                      : CHẶN (chỉ được gửi credential qua HTTPS)
  đường thuận     https://api.githubcopilot.com/mcp/                     : QUA
== dưới đột biến M1 ==
  host hậu tố    : QUA   ← credential đi tới host của kẻ tấn công
  host khác hẳn  : QUA
== dưới đột biến M2 ==
  http không TLS : QUA   ← Bearer token đi trên đường không mã hoá
```

`A2` có khẳng định `m.kiem_dich_den("https://API.GitHubCopilot.COM/mcp/")` phải QUA — nhưng đó là
vế **thuận**; dưới M1 nó vẫn QUA, nên nó không canh gì. `A4` (gán lại `self.url` sang
`https://evil.example/x`) trông như canh HOST, nhưng đo được là **chốt ĐƯỜNG DẪN** bắt nó: dưới M1
đúng URL ấy vẫn bị chặn vì `/x` không thuộc `DUONG_CHO_PHEP`. Đổi URL của `A4` thành
`https://evil.example/mcp/` là `A4` mất răng với M1.

Cùng họ với bài học `CLAUDE.md` *"đếm SỰ CÓ MẶT của một đường thay vì KHẢ NĂNG của nó"*: chốt có
mặt trong mã, nhưng **không phép đo nào chứng minh nó đang gánh việc**.

**Chữa (đề xuất, không bắt buộc theo cách này):** ba ca mới, mỗi ca gỡ đúng một mệnh đề —
host-hậu-tố phải CHẶN · `http://` phải CHẶN · một đường dẫn ngoài tập phải CHẶN — kèm ba đột biến
`if False:` tương ứng vào `MUTATIONS`.

### P1-2 · `cong-that-nam-trong-main-khong-ai-canh`

`mcp_gh_test.py:589-610` (khối `if __name__ == "__main__":`) là **cổng thật**. Nó không phải hàm
`cong()`. Nó thêm ba quyết định nữa mà `cong()` không thấy:

```python
605    d8_ok = not failed and not any(d8_errors)
606    ok = cong(tuple(name for name, _ in CASES), tuple(ran),
607              mutant_names, mutant_names if d8_ok else (),
608              tuple(failed) + tuple(mutation_errors))
610    sys.exit(0 if ok else 1)
```

**Không ca nào và không đột biến nào chạm 22 dòng này.** Cấu trúc chặn điều đó: runner đột biến
nạp module mục tiêu bằng `spec.loader.exec_module` rồi gọi `chay_cac_ca(mutant)` — khối
`__main__` **không bao giờ thực thi**. `C1`–`C4`, `D7`, `D7b`, `D8` đều gọi các hàm thuần với
tuple tự chế, không đi qua đây.

Hậu quả đo được — nền M4 (chốt đường dẫn bị gỡ) làm cổng ĐỎ đúng như phải thế, rồi **một** thay
đổi một dòng trong `__main__` làm nó xanh trở lại, trong khi màn hình vẫn in ĐỎ:

```
B. chỉ M4                 rc=1  CA 35/35 đạt · 0 đỏ  TỔNG: ĐỎ
C. M4 + N1 (d8_ok=True)   rc=0  CA 35/35 đạt · 0 đỏ  TỔNG: ĐẠT
                                D8(a): ĐỎ ['a8_bo_actions']   D8(b): ĐỎ ['a8_bo_actions']
D. M4 + N2                rc=0  CA 35/35 đạt · 0 đỏ  TỔNG: ĐẠT
                                D8(a): ĐỎ ['a8_bo_actions']   D8(b): ĐỎ ['a8_bo_actions']
```

Và dạng thuần nhất — **tái dựng lại đúng hình dạng packet sinh ra để đóng**, bằng hai thay đổi
một dòng, cả hai nằm trong vùng không ai canh:

```
HAI ĐỘT BIẾN: (1) `try: fn()` → `try: pass`   (2) `d8_ok = True`
rc=0
CA         : 35/35 đạt · 0 đỏ            ← 35 ca KHÔNG ca nào chạy thân
ĐỘT BIẾN   : đã đo 38/38 tập giết
D8(a) ... : ĐỎ ['a1_cong_444', 'a2_bo_query', ... 38 tên]
D8(b) ... : ĐỎ [... 38 tên]
TỔNG: ĐẠT
```

Đây là site **#6/#7** của `hinh_dang_ke_thua` mọc lại một tầng cao hơn: vòng 1 để lỗ ở vị ngữ
`not DO`, vòng 2 tách sổ, vòng 3 chuyển lỗ vào **dây nối** giữa sổ và `sys.exit`. `cong()` đã sạch;
thứ chưa ai đo là thứ gọi nó.

**Chữa:** đưa khối quyết định ra một hàm thuần (ví dụ `ket_luan(ran, failed, kill_sets, mutation_errors)`
trả `(ok, cac_dong_in)`), để `__main__` chỉ còn `sys.exit(0 if ket_luan(...)[0] else 1)`; rồi thêm ca
+ đột biến cho `ket_luan` — tối thiểu: *D8 đỏ mà `ok` vẫn True* phải ĐỎ.

### P1-3 · `khong-cong-nao-chay-bo-test` — XÁC NHẬN vòng 1

```
$ grep -rn mcp_gh .github scripts ops .claude --include=*.yml --include=*.yaml --include=*.sh --include=*.py
  -> 0 dòng nhắc 'mcp_gh' NGOÀI hai tệp của chính packet
```

`ci.yml` **liệt kê từng tệp bằng tay**, không có bước dò `*_test.py`:

```
ci.yml:92   python ops/cong_cu_test.py
ci.yml:110  python .claude/dev/codex_cred_test.py
ci.yml:112  python .claude/dev/packet_loop_test.py
ci.yml:118  python .githooks/eol_policy_test.py
ci.yml:120  python .githooks/pre_push_test.py
ci.yml:271  python .claude/dev/gate_lifecycle_test.py
ci.yml:306  python scripts/tl_core/command_registry_test.py
```

Tìm `glob`/`rglob`/`**/*_test` trong `.github/workflows/*.yml`: **0 kết quả**. Không cổng nào
buộc một `_test.py` mới phải được đăng ký (`.github/checks/ci_phamvi.py` gác phạm vi **gói phát
hành**, không gác danh sách test).

Nghĩa là: mọi con số của §1 và §2 chỉ tồn tại **khi có người gõ tay**. `CLAUDE.md` đã chốt
*"Workflow chỉ chạy khi có người bấm là workflow KHÔNG có ai canh"*; ở đây còn nhẹ hơn thế — không
có cả cái nút. Một bộ phản chứng 610 dòng không có runner ≡ **cổng vắng mặt**, và vắng mặt trông y
hệt xanh.

Ghi thêm một mặt mà vòng 1 không nêu: `ngoai_pham_vi` #5 khai *"Đưa `mcp_gh.py` lên master là việc
của lượt land"*. Việc **đăng ký runner** không nằm trong `ngoai_pham_vi`, không nằm trong
`muc_tieu`, và write set ba đường dẫn khiến nó **không thể** làm trong packet này. Tức đây là lỗ do
chính write set đóng băng sinh ra, và nó phải được khai thành nợ có tên trước khi land, chứ không
để cho lượt land tự nhớ.

### P1-4 · `b3-chot-cach-ly-mang-neo-theo-TEN`

Đặc tả `B3` viết nguyên văn: *"chốt cô lập phải neo vào đường `main` THẬT đi, **không neo vào tên
hàm ta nhớ**"*. Bản giao nộp neo đúng vào một tên (`mcp_gh_test.py:243-244`):

```python
cu_mo = m._mo_mac_dinh
m._mo_mac_dinh = lambda *args: (_ for _ in ()).throw(AssertionError("đã ra mạng"))
```

Phản chứng chạy được — **refactor bảo toàn hành vi**, nội tuyến opener thay vì tra tên toàn cục:

```python
# mcp_gh.py:119   self._mo = mo or _mo_mac_dinh
#           →     self._mo = mo or (lambda r, t: _OPENER.open(r, timeout=t))
```

Đo (bọc `socket.socket.connect` để đếm kết nối THẬT):

```
B3 trên bản REFACTOR (chưa đột biến)              : ĐẠT (xanh)
B3 dưới đột biến b3_bo_token trên bản REFACTOR    : ĐẠT (xanh)  -> ĐỘT BIẾN SỐNG SÓT
số lần tiến trình THẬT SỰ mở socket               : 1  [('127.0.0.1', 34483)]
```

Hai chuyện cùng lúc: (a) đột biến gỡ chốt token **sống sót**, vì `assert rc == 3` không phân biệt
được *rc=3 do chốt token* với *rc=3 do lời gọi mạng thất bại*; (b) bộ test **thật sự mở socket ra
ngoài** (cổng 34483 là proxy egress của container). Bộ test tự khai *"phản chứng offline"*
(`mcp_gh_test.py:2`) — lời khai ấy chỉ đúng chừng nào không ai đổi tên một hàm nội bộ.

Xếp P1 vì đây là **chữ của tiêu chí B3 không được thoả**, có phản chứng tái lập. Nói rõ phạm vi:
bản giao nộp **hiện tại** không lộ lỗ này — nó là lỗ về độ bền của phép đo, không phải lỗ đang hở.

---

## 4. Bảng chấm A / B / C / D

Lệnh nền cho mọi ô: `python3 .claude/dev/mcp_gh_test.py` (rc=0). Cột "phép đo riêng" ghi lệnh của
tôi khi có.

### A — đích đến của credential

| # | chấm | phép đo |
|---|---|---|
| A1 | ĐẠT | `a1_cong_444` giết đúng `('A1',)`; M5 làm A2/A4/A8… đỏ |
| A2 | **ĐẠT CÓ ĐIỀU KIỆN** | ba vế CHẶN đo được; vế thứ tư (hoa/thường vẫn QUA) là vế THUẬN, **dưới M1 vẫn QUA** ⇒ không canh chốt HOST — xem P1-1 |
| A3 | ĐẠT | M3 ⇒ `ĐỎ A3: đích đáng lẽ phải bị chặn`; chuỗi lỗi không chứa bí mật |
| A4 | **ĐẠT CÓ ĐIỀU KIỆN** | `a4_bo_chot_gui` giết `('A4',)` ⇒ "có kiểm lại lúc gửi" ĐƯỢC chứng minh; nhưng URL của ca bị bắt bởi chốt ĐƯỜNG DẪN, không phải chốt HOST (đo: dưới M1 vẫn CHẶN) |
| A5 | **ĐẠT** | ca chạy THẬT ở nền này (`bind` được cấp); M6 ⇒ `ĐỎ A5`; M7 ⇒ `ĐỎ A5 A6-302 A6-303 A7` |
| A6 | **ĐẠT** | hai ca riêng `A6-302` `A6-303`, hai đột biến riêng, mỗi cái giết đúng ca của nó |
| A7 | ĐẠT | `a7_theo_307_308` giết `('A7',)` |
| A8 | ĐẠT | `a8_bo_actions` giết `('A8',)`; nhưng A8 chỉ đo vế THUẬN — xem P1-1 |

**Ghi có trọng lượng:** `chua_do_duoc` #6 của đặc tả nói `A5`–`A7` *"chưa từng được xác nhận bởi
một nền độc lập với nền đã phát hiện ra chúng"*. Lượt này **đóng được mục đó**: container review
cấp `bind` trên `127.0.0.1`, ba ca chạy thật, và bốn đột biến chuyển hướng (`a5`,`a6`x2,`a7`) cộng
M6/M7 của tôi đều có răng. Đây là kết quả DƯƠNG duy nhất trong verdict này mà tôi cho là mạnh hơn
lời khai của executor.

### B — chín bất biến

| # | chấm | phép đo |
|---|---|---|
| B1 | ĐẠT | `b1_bo_data` giết `('B1',)`; ca dùng đường `tach_than` riêng, không đụng `B2` |
| B2 | ĐẠT | hai đột biến riêng `b2_cat_than` `b2_cat_text`, **cả hai** giết `('B2',)`; M8 (`[:10]`) ⇒ `ĐỎ B2` |
| B3 | **ĐỎ** | xem **P1-4** |
| B4 | ĐẠT | `b4_bo_jsonrpc` giết `('B4',)`; ca khẳng định `startswith("JSON-RPC error -32000")` |
| B5 | ĐẠT | `b5_bo_urlerror` giết `('B5',)`, và **không** giết `D5` (giao phạm vi của lượt 1 đã hết) |
| B6 | ĐẠT · giao phạm vi được IN | `b6_bo_chot_init` giết `('B6','D6')` — in ra bảng GIAO PHẠM VI, không làm cổng đỏ, đúng `D8` bản r3 |
| B7 | **ĐẠT CÓ ĐIỀU KIỆN** | bốn ca, bốn đột biến, tập giết không rỗng; nhưng cơ chế `.pyc` KHÔNG được tái hiện — xem **P2-4** |
| B8 | ĐẠT | `b8_notification_co_id` giết `('B8',)`; ca khẳng định cả thời điểm lẫn `"id" not in` |
| B9 | ĐẠT | `b9_bo_sid` giết `('B9',)` |

### C — sổ ca bất biến

| # | chấm | phép đo |
|---|---|---|
| C1 | ĐẠT trên DỮ LIỆU THẬT | M10 ép `module.CASES = ()` ⇒ `CA 0/0 đạt` · `TỔNG: ĐỎ` · `rc=1`. Đây là phép đo mà vòng 1 không làm được |
| C2 | ĐẠT (chỉ hàm thuần) | `c2_cho_so_db_rong` giết `('C2',)`; không đo được trên dữ liệu thật vì `MUTATIONS` là hằng |
| C3 | ĐẠT (chỉ hàm thuần) | `c3_cho_ca_hai_rong` giết `('C3',)` |
| C4 | **ĐỎ** | xem **P2-3**: đúng đột biến mà đặc tả nêu cho C4 cho `CA 35/35 đạt · 0 đỏ` |

### D — hợp đồng và cổng

| # | chấm | phép đo |
|---|---|---|
| D1 | ĐẠT | `d1_bo_top_error` giết `('D1',)`; M9 ⇒ `ĐỎ D1 D2` |
| D2 | ĐẠT | ca riêng, và ca tự ghi *"phản hồi bơm; chưa đo được từ công cụ thật"* — trung thực đúng `chua_do_duoc` #2 |
| D3 | ĐẠT | `d3_nhan_result_rong` giết `('D3',)` |
| D4 | ĐẠT | `d4_bo_shape` giết `('D4',)`; `[]` ⇒ `"phản hồi JSON phải là object"`, không `AttributeError` |
| D5 | ĐẠT | `d5_nuot_loi_notification` giết `('D5',)`, và **không** giết `B5` |
| D6 | ĐẠT | `d6_doi_co_cli` giết `('D6',)`; ca chạy cả bốn dạng và khẳng định `0/0/0/2/3` |
| D7 | ĐẠT ở hàm `cong()`, **ĐỎ ở cổng thật** | xem **P1-2** |
| D7b | **ĐẠT** — kiểm riêng | đo trực tiếp: nền đỏ (M3) ⇒ `ĐỘT BIẾN : KHÔNG_ĐO_ĐƯỢC (nền đỏ)`, cả ba dòng D8 in `KHÔNG_ĐO_ĐƯỢC`, bảng giao phạm vi in `KHÔNG_ĐO_ĐƯỢC`, `TỔNG: ĐỎ`. **Không** in `0/N`, **không** trừ ca đỏ nền. Đúng chữ của D7b |
| D8 | (a) ĐẠT (b) ĐẠT (c) **ĐẠT NHƯNG YẾU** | in tập giết thật của 38 đột biến: mọi đích ∈ tập giết; không tập nào rỗng; 38 nhãn đích = đúng 35 tên ca. (c) thoả **do cấu trúc** — `MUTATIONS` được viết sao cho phủ hết `CASES`, nên nó bắt "quên viết đột biến cho ca mới", không bắt "ca vô hiệu" |
| D9 | **ĐỎ** | xem **P2-1** và **P2-2** |

---

## 5. Đối chiếu 11 finding của vòng 1

| finding vòng 1 | kết luận vòng 2 | phép đo |
|---|---|---|
| P1 `bo-test-khong-co-cong-nao-chay` | **XÁC NHẬN** | `grep` ⇒ 0 dòng nhắc `mcp_gh` ngoài packet; `ci.yml` liệt kê tay 7 tệp; 0 kết quả cho `glob`/`rglob` — §P1-3 |
| P1 `cong-that-khong-noi-vao-du-lieu-that` | **XÁC NHẬN, và mạnh hơn vòng 1 khai** | không chỉ "ngoài tầm đo": M4+N1 và M4+N2 cho `rc=0` `TỔNG: ĐẠT` **trong khi màn hình in D8 ĐỎ** — §P1-2 |
| P2 `loi-khai-38-38-bi-giet-rong-hon-phep-do` | **XÁC NHẬN phần HÌNH THỨC · BÁC phần SỐ** | Số đúng: in tập giết thật ⇒ **38/38 tập đều KHÁC RỖNG**, nên "mọi đột biến đều giết được cái gì đó" là mệnh đề ĐO ĐƯỢC. Nhưng (a) dòng in là *"đã **đo** 38/38 tập giết"*, không phải *"38/38 **bị giết**"* — lời tự khai của executor rộng hơn dòng in; (b) đối số `killed` của `cong()` là `mutant_names if d8_ok else ()` (`:607`) — một **hằng gắn cờ**, không phải phép đo độc lập, nên `tuple(killed)==tuple(mutants)` không mang thêm thông tin nào ngoài `d8_ok` |
| P2 `b7-xoa-ca-khong-the-do` | **BÁC như phát biểu · XÁC NHẬN một bệnh KHÁC** | Ca **CÓ THỂ** đỏ: `b7_bo_xoa_pyc` có tập giết `('B7-xoa',)`. Nhưng nó đỏ nhờ khẳng định thứ BA, không nhờ cơ chế nó khai — §P2-4 |
| P2 `d9-ghi-cung-900-trai-chinh-D9` | **XÁC NHẬN** | `mcp_gh_test.py:475` `assert tong <= 900`; `D9` của đặc tả nói *"≤ trần của lease đang hiệu lực"* và r2 khai *"CỐ Ý không ghi cứng con số"* — §P2-2 |
| P2 `don-vi-ngan-sach-doi-sau-khi-truot-va-tien-de-sai` | **XÁC NHẬN, tiền đề SAI đo được** | numstat: cả write set **1155**, hai tệp mã **840**. Đặc tả khai *"mã đứng ở **802** suốt từ lượt 2"* — §P2-1 |
| P2 `chot-mang-neo-theo-ten` | **XÁC NHẬN, có phản chứng chạy được** | refactor bảo toàn hành vi ⇒ `b3_bo_token` SỐNG SÓT, và tiến trình mở 1 socket thật — §P1-4 (nâng lên P1) |
| P2 `dac-ta-dong-bang-co-ba-con-so-ma-mau-thuan` | **XÁC NHẬN** | ba tổng mã trong một đặc tả: **790** (`:285`) · **802** (`:256`) · thực đo **840**; hai số cho `mcp_gh_test.py`: **564** `:276` · **572** `:256` · thực đo **610** — §P2-1 |
| P2 `rut-van-ban-bo-content-1-tro-di` | **XÁC NHẬN** | §P2-5 |
| P2 `review-vong-1-khong-do-duoc` | **XÁC NHẬN đã được sửa ở vòng này** | probe §0 chạy được; toàn bộ verdict này là phép đo |
| "hai mục nhỏ gộp" | **KHÔNG_ĐO_ĐƯỢC** | verdict vòng 1 nằm trên nhánh `ops/cap-lease-tach-314`, không có trong clone này, và tôi được yêu cầu không `git fetch`. Không biết nội dung hai mục ⇒ không chấm |

---

## 6. Ba lỗ hổng `muc_tieu` — đóng thật chưa, và đo bằng gì

| lỗ | trong MÃ | trong BẰNG CHỨNG | đo bằng |
|---|---|---|---|
| **1. Khoá nơi nhận credential bằng origin chuẩn hoá** | **ĐÓNG** — `kiem_dich_den` so `scheme`+`hostname`+cổng đã chuẩn hoá, từ chối userinfo/query/fragment, và đo được là chốt CHẶN cả host-hậu-tố lẫn `http://` | **KHÔNG ĐÓNG** | M1 và M2 sống sót ⇒ ba trong sáu mệnh đề không có phản chứng nào (P1-1) |
| **2. Kiểm lại đích TẠI THỜI ĐIỂM GỬI** | **ĐÓNG** — `goi()` gọi lại `kiem_dich_den(self.url)` trước khi dựng header `Authorization` (`:123` trước `:131`) | **ĐÓNG một phần** | `a4_bo_chot_gui` (thay lời gọi bằng `pass`) giết đúng `('A4',)`; ca còn khẳng định `not da_mo` — chưa mở kết nối nào. Điều **chưa** được đo: chốt gọi lại ấy có bắt được đích đổi HOST không (dưới M1 thì không) |
| **3. KHÔNG đi theo chuyển hướng** | **ĐÓNG** | **ĐÓNG — và đây là mục vững nhất của packet** | ba ca loopback chạy THẬT ở nền này; M6 (một mã trả `super()`) ⇒ `ĐỎ A5`; M7 (dùng opener mặc định) ⇒ `ĐỎ A5 A6-302 A6-303 A7`; bốn đột biến của chính bộ test mỗi cái giết đúng ca của nó. Phạm vi đúng như `chua_do_duoc` #1: đây là hành vi của `urllib`, không phải của điểm cuối thật |

---

## 7. Năm P2

### P2-1 · `so-lieu-dong-bang-cua-dac-ta-da-troi-va-tien-de-doi-don-vi-sai`

Đặc tả đóng băng bằng băm, lease neo vào `spec_sha256` — nên số trong nó là **lời khai có thẩm
quyền**, không phải ghi chú. Đo tại `reviewed_sha`:

| đặc tả khai | dòng | thực đo | lệch |
|---|---|---|---|
| `mã đứng ở **802**` | `:256` | **840** | +38 |
| `mcp_gh_test.py 572` | `:256` | **610** | +38 |
| `Phần MÃ thật là 790` (`mcp_gh.py 226 · mcp_gh_test.py 564`) | `:275,:285` | 230 · 610 = **840** | +50 |
| `trần của lease r2: ≤ 750 dòng thêm, 3 tệp` | `:203` | cả write set **1155**; chỉ mã **840** | vượt theo **cả hai** đơn vị |

Nguy hiểm hơn từng con số lẻ: **tiền đề của việc đổi đơn vị đo ở r3 không còn đúng.** `:253-257`
lập luận *"cả ba lần chạm trần đều do ĐẶC TẢ nở, không do mã — mã đứng ở 802 suốt từ lượt 2"*.
Tại `reviewed_sha`, mã đã nở thêm **38 dòng** sau chính lời khai đó. Và `:263` kết luận *"802 nằm
dưới ngưỡng 1.000 của lớp `thường` với **biên gần 200**"* — biên thật là **160** theo ngưỡng 1.000,
và **60** theo chốt chống lặp 900 của `:270`.

Đây đúng bài học `CLAUDE.md` *"MỘT BẤT BIẾN CÒN ĐÚNG KHÔNG CHỨNG MINH CÁC SỐ HẠNG CÒN ĐÚNG"*:
quan hệ *"mã < trần"* vẫn đúng, nên câu đọc vào rất sạch, trong khi cả ba số hạng đã trôi.

Không đề nghị sửa đặc tả (sửa ⇒ đổi băm ⇒ lease trỏ vào thứ không còn tồn tại). Đề nghị: **lượt
land phải đăng bảng đối chiếu số-khai / số-đo** để người land THẤY rằng lời khai đã cũ, đúng như
`:266-268` tự đòi (*"con số theo cả hai đơn vị phải được báo ở mọi lượt"*) — mà lượt này chưa ai báo.

### P2-2 · `d9-do-thu-khac-han-thu-D9-noi`

```python
473  def d9_ngan_sach_900_dong_ma():
474      tong = sum(sum(1 for _ in path.open(encoding="utf-8")) for path in (NGUON, pathlib.Path(__file__)))
475      assert tong <= 900, f"hai tệp mã dùng {tong}/900 dòng"
```

Ba chỗ lệch với `D9` của đặc tả:

1. **Đơn vị.** `D9` nói *"`git diff --numstat` trên write set, **cột dòng THÊM**"*. Ca đếm **số
   dòng trong tệp**. Ở đây hai số trùng nhau **chỉ vì cả hai tệp là tệp mới** (`-0` ở numstat);
   sau lần sửa đầu tiên chúng tách ra và ca sẽ đo sai thứ.
2. **Ngưỡng ghi cứng.** `D9` nói *"≤ trần của lease đang hiệu lực"*, và `:194` khai thẳng
   *"r2 **CỐ Ý không ghi cứng** con số ở đây"* vì *"đó chính là hình dạng 'sửa TRƯỜNG, quên VĂN
   BẢN' mà packet này sinh ra để chặn"*. Ca ghi cứng `900`. `900` cũng **không phải trần nào**: nó
   là ngưỡng TÁCH ở `:270`, còn trần lease r2 ở `:203` là **750** — mà `840 > 750`.
3. **Phạm vi.** `:251` đòi đặc tả *"vẫn phải báo cáo"* riêng. Ca không đếm `ops/specs/…` (315 dòng),
   và không có ca nào báo. Không đo được ⇒ không ai thấy `1155`.

Tôi **không đo được trần thật** của lease đang hiệu lực: tệp lease nằm trên nhánh `ops/**` không có
trong clone detached này, và tôi được yêu cầu không `git fetch`. ⇒ **KHÔNG_ĐO_ĐƯỢC**, ghi thẳng
thay vì suy. Nhưng ba lệch trên đo được không cần trần.

### P2-3 · `c4-khong-bat-duoc-ca-vo-hieu-tren-du-lieu-that`

Đặc tả `C4` mô tả **đúng** đột biến phải giết ca: *"bỏ lời gọi thân ca nhưng GIỮ dòng ghi sổ ĐẠT"*.
Tôi chạy đúng nó (`mcp_gh_test.py:548-549`, `try: fn()` → `try: pass`):

```
rc=1
CA         : 35/35 đạt · 0 đỏ      ← sổ ca KHÔNG thấy gì bất thường
D8(a): ĐỎ [38 tên]   D8(b): ĐỎ [38 tên]   D8(c): ĐẠT
TỔNG: ĐỎ
```

Cổng có đỏ — nhưng **không phải nhờ C1–C4**. Lý do cấu trúc: `chay_cac_ca` (`:547-549`) ghi
`ran.append(name)` **rồi mới** gọi `fn()`, nên `tuple(ran) == tuple(registry)` là **bất biến của
runner**, không phải phép đo. Vị ngữ `_du_ca` không thể phân biệt "ca đã đo" với "ca chỉ được điểm
danh" — đúng chữ *"ca có MẶT khác ca có ĐO"*. `C4` chỉ đo hàm thuần `cong()` với tuple tự chế
`(("c",), (), ...)` mà đường thật **không bao giờ sinh ra**.

Thứ thật sự bắt được là `D8(b)` — mà `D8(b)` lại bị tắt bằng một dòng ở `__main__` (P1-2). Ghép hai
lại: `C4' + N1` ⇒ `rc=0` `TỔNG: ĐẠT` `CA 35/35 đạt`, 35 ca không ca nào chạy. Hai P2/P1 riêng lẻ,
nhưng chúng che nhau: mỗi cái một mình vẫn đỏ, cùng nhau thì xanh.

### P2-4 · `b7-xoa-khong-tai-hien-co-che-pyc-ma-no-khai`

`b7_xoa_pyc_cu` (`:288-298`) dựng ca cho site #4 của `hinh_dang_ke_thua`: *"hai đột biến ra tệp
**cùng kích thước**, ghi trong cùng một giây ⇒ bản sau chạy mã của bản trước"*. Hai tải trọng nó
dùng **không cùng kích thước**:

```
kích thước thân:  cũ = 15B ("GIA_TRI = 'cu'\n")   mới = 16B ("GIA_TRI = 'moi'\n")   -> KHÁC NHAU
nạp lại KHÔNG xoá pyc, cùng mtime giây  ->  GIA_TRI = 'moi'
=> khẳng định thứ HAI (dòng 297) KHÔNG có răng
pyc còn sót lại: True  ->  chỉ khẳng định thứ BA (dòng 298) mới giết đột biến
```

CPython vô hiệu `.pyc` theo **(mtime giây, KÍCH THƯỚC)**; ca ghim mtime nhưng để kích thước lệch,
nên nhánh nguy hiểm — cùng giây **và** cùng cỡ — không bao giờ được đi vào. Ca vẫn ĐỎ được (nhờ
`assert not …exists()`), nên vòng 1 nói *"không thể ĐO"* là **quá mạnh**; nhưng nó đo **"có tệp
`.pyc` sót lại không"**, một thứ yếu hơn hẳn **"mã cũ có bị chạy không"**. Chữa rẻ: đổi hai tải
trọng thành cùng độ dài (ví dụ `'cu_'` và `'moi'`).

### P2-5 · `rut-van-ban-bo-content-1-tro-di`

```python
107      if isinstance(nd, list) and nd and isinstance(nd[0], dict) and "text" in nd[0]:
108          return nd[0]["text"]
```

Đo:

```
vào: content = [{"text":"PHAN-1"}, {"text":"PHAN-2"}, {"text":"PHAN-3"}]
ra : 'PHAN-1'        mất PHAN-2 và PHAN-3: True
```

`B2` khai bất biến *"**KHÔNG cắt chuỗi** — cả ở tách thân lẫn ở rút văn bản"*. Cắt theo **ký tự**
được canh (hai đột biến `[:6000]`); cắt theo **phần tử** thì không: cả ba chỗ nhắc `content` trong
bộ test (`:147`, `:233`, `:383`) đều dùng danh sách **một phần tử hoặc rỗng**, nên không ca nào
thấy được. Mất im lặng ở đây nguy đúng kiểu `B2` sinh ra để chặn — người gọi `json.loads` một tải
trọng bị xén sẽ thấy JSON hợp lệ mà thiếu dữ liệu.

Không xếp P1 vì `muc_tieu` không đòi hỗ trợ nhiều phần tử `content` và đây là mã mới (không phải
hồi quy). Nhưng phải hoặc canh, hoặc khai vào `chua_do_duoc`.

---

## 8. CHỖ KHÔNG ĐO ĐƯỢC

1. **Trần thật của lease đang hiệu lực.** Tệp lease sống trên nhánh `ops/**`, clone này detached ở
   `4aa936e0` và tôi được yêu cầu không `git fetch`. Nên P2-2 chấm được ba lệch về **đơn vị / nguồn
   thẩm quyền / phạm vi**, nhưng câu *"840 có vượt trần không"* là **KHÔNG_ĐO_ĐƯỢC**. Đây đúng nợ
   `SO-LEASE-KHONG-NAM-MOT-CHO` của `CLAUDE.md`, gặp lại từ phía reviewer.
2. **Nội dung verdict vòng 1.** Nằm ở `ops/reviews/mcp-gh-cuu-ho-review-1-claude-verdict.md` trên
   nhánh `ops/cap-lease-tach-314`, không có trong clone. Mười finding được liệt kê trong nhiệm vụ
   thì chấm được; "hai mục nhỏ gộp" thì không.
3. **Hành vi chuyển hướng của `api.githubcopilot.com` THẬT.** Y như `chua_do_duoc` #1: `A5`–`A7` đo
   `urllib`, không đo máy chủ kia. Tôi không thử gọi điểm cuối thật.
4. **`result.isError` từ một công cụ THẬT.** `D2` dùng phản hồi bơm và tự khai như thế. Tôi giữ
   nguyên trạng thái ấy — không dựng được máy chủ MCP thật trong lượt này.
5. **`ci.yml` có chạy được `mcp_gh_test.py` không nếu được đăng ký.** Tôi đo được rằng **không nơi
   nào gọi nó**; tôi KHÔNG đo được nó sẽ xanh/đỏ trên `windows-latest` (`A5`–`A7` cần `bind`; nền
   Windows chưa ai chạy). `CLAUDE.md` đã ghi Linux bỏ qua 1 ca / Windows bỏ qua 13 ca cho một suite
   khác — nên đây là câu hỏi thật, không phải lo xa.
6. **Kích thước ngân sách theo đơn vị "trần lease" ở lượt land.** Xem (1).
7. **Tôi không commit, không `git add`, không push** — `.git` mount chỉ đọc; tệp verdict này nằm
   trong cây làm việc, chưa staged. `git status --porcelain` trước khi viết tệp: RỖNG.

---

## 9. Vì sao `changes_requested` chứ không `blocked`

Đo được, không suy: bộ test **chạy trọn** ở nền này, mọi con số executor khai đều **tái lập được**,
và mục khó nhất của packet — ba tính chất chuyển hướng mà lượt thi công 1 không chạy nổi — nay có
**một nền độc lập** xác nhận, kèm hai đột biến của tôi (M6, M7) cho thấy nó có răng. Đó là công
việc thật và nó đứng vững.

Thứ chặn `approved` là ba mệnh đề định nghĩa nơi nhận credential không có phản chứng nào (P1-1),
và hình dạng chính packet sinh ra để đóng đã mọc lại ở **dây nối giữa sổ và `sys.exit`** (P1-2) —
đo bằng hai thay đổi một dòng cho `rc=0` `TỔNG: ĐẠT` với 35 ca không chạy gì. Cộng việc không cổng
nào chạy bộ test (P1-3), nên mọi con số ở trên hôm nay chỉ tồn tại khi có người gõ tay.

Cả bốn P1 đều là **thêm ca + thêm đột biến + một lần tách hàm**, không đòi thiết kế lại: đều nằm
trong write set đã đóng băng, trừ P1-3 — mục ấy phải mở nợ có tên vì write set ba đường dẫn không
cho chạm `.github/workflows/`.

---

**Đường dẫn verdict:** `ops/reviews/mcp-gh-cuu-ho-review-2-claude-verdict.md`
**Số finding:** **P1 = 4** · **P2 = 5**

| mã | mức |
|---|---|
| `chot-dich-credential-khong-co-phan-chung` | P1 |
| `cong-that-nam-trong-main-khong-ai-canh` | P1 |
| `khong-cong-nao-chay-bo-test` | P1 |
| `b3-chot-cach-ly-mang-neo-theo-TEN` | P1 |
| `so-lieu-dong-bang-cua-dac-ta-da-troi-va-tien-de-doi-don-vi-sai` | P2 |
| `d9-do-thu-khac-han-thu-D9-noi` | P2 |
| `c4-khong-bat-duoc-ca-vo-hieu-tren-du-lieu-that` | P2 |
| `b7-xoa-khong-tai-hien-co-che-pyc-ma-no-khai` | P2 |
| `rut-van-ban-bo-content-1-tro-di` | P2 |
