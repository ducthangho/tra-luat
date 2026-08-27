# Cross-review vòng 3 — packet #319 `MCP-GH-CUU-HO` (PR #339)

```yaml
verdict: changes_requested
reviewed_sha: 97617d3a5372fcce39b0e53064958c24d15775ce
base_sha: b662fe1d07c675a222ae26e734377e305775e4f3
reviewer: claude
executor: codex
con_P1_mo: 1
```

**Nói thẳng cho người giữ kho:** còn **MỘT P1**, nên theo luật *"chỉ P1 mới chặn land"* thì packet
này **chưa land được**. P1 ấy KHÔNG phải lỗi mới do bản vá đẻ ra — nó là **nửa còn lại** của P1 số 2
vòng 2, mà lượt này chỉ đóng được một nửa. Bản vá không làm hỏng thứ gì đang chạy.

---

## 1. Nền đo — tôi chạy được mã, và vỏ của tôi `bind` ĐƯỢC

| phép đo | lệnh | kết quả |
|---|---|---|
| chạy mã | `python3 -c 'print("PROBE_OK")'` | `PROBE_OK`, Python 3.11.15 |
| `bind` loopback | `socket.bind(("127.0.0.1", 0))` + `listen` | **`BIND_OK ('127.0.0.1', 35105)`** |

Đây là khác biệt quan trọng nhất giữa lượt này và lượt của executor. Sandbox `codex` bị
`PermissionError` nên bốn ca cần loopback (`A5` · `A6-302` · `A6-303` · `A7`) phải khai
`KHÔNG_ĐO_ĐƯỢC (nền đỏ)` — đúng `D7b`, và đó là hành xử đúng. **Vỏ của tôi cho `bind`, nên bốn ca ấy
lượt này ĐƯỢC ĐO THẬT**, không phải suy ra. Đặc tả đòi *"nghiệm thu cuối phải chạy ở nền cho
`bind`"* (dòng 141) — lượt này là nền đó.

Nền đo đầy đủ, chạy trong kho tại SHA nghiệm thu:

```
$ cd .claude/dev && python3 mcp_gh_test.py     # 5,3 s
CA         : 39/39 đạt · 0 đỏ
ĐỘT BIẾN   : đã đo 42/42 tập giết
D8(a) đích nằm trong tập giết: ĐẠT
D8(b) không tập giết rỗng: ĐẠT
D8(c) mọi ca có đột biến canh: ĐẠT
TỔNG: ĐẠT                                       rc=0
```

Không ô nào `KHÔNG_ĐO_ĐƯỢC`. Executor **không** trừ bớt ca để lấy số đẹp — tôi đã đối chiếu và xác
nhận sổ ca của bản này là 39, đủ.

### Cảnh báo về rig — tôi đã tự sập một lần, ghi ra để không ai đọc nhầm số của tôi

Lượt đo đầu tiên của tôi cho **BASE `rc=1`** trong khi kho thật cho `rc=0`. Không phải hồi quy: tôi
chạy `khung1` (gọi thẳng mọi ca) rồi mới gọi `chay_cli()` **trong cùng một tiến trình**, và trạng
thái toàn cục rò giữa hai lượt. Dựng lại thành **một tiến trình sạch cho mỗi biến thể, cùng một
lệnh** ⇒ BASE về `rc=0`. Mọi con số dưới đây lấy từ rig đã sửa. Đây đúng bài học *"phép đo delta
phải dựng cả hai vế trong một lệnh"* trong `CLAUDE.md`, và nó bẫy được tôi trước khi tôi kịp báo một
hồi quy không tồn tại.

---

## 2. Phán quyết BỐN P1 của vòng 2

### P1-1 `chot-dich-credential-khong-co-phan-chung` → **ĐÃ VÁ THẬT**

Tôi **tự dựng lại** ba đột biến `if False:` (không dùng bảng `MUTATIONS` của executor), áp lên bản
sao tạm, chạy trọn sổ ca:

| mệnh đề bị vô hiệu | dòng | ca GIẾT nó |
|---|---|---|
| `if u.scheme != "https":` | `mcp_gh.py:29` | **chỉ `A10-scheme`** |
| `if u.hostname != HOST_CHO_PHEP:` | `mcp_gh.py:31` | **chỉ `A9-host`** |
| `if u.path not in DUONG_CHO_PHEP:` | `mcp_gh.py:37` | **chỉ `A11-path`** |

Cả ba đều bị giết. Quan trọng hơn con số: **mỗi cái bị giết bởi ĐÚNG MỘT ca, và ba ca ấy khác nhau**
— tức ba ca thật sự độc lập, không cùng bị một chốt bắt. Đây chính là câu hỏi mà `A4` cũ đã trả lời
sai (tưởng canh HOST, thực ra bị chốt ĐƯỜNG DẪN bắt), nên tôi đã đo riêng thay vì tin tên ca.

Đối chiếu bằng tay khớp với phép đo: `A10` dùng `http://…/mcp/` (host đúng, cổng mặc định 443,
đường dẫn hợp lệ ⇒ chỉ `scheme` bắt được); `A9` dùng hậu tố `…com.example` với đường dẫn `/mcp/`
hợp lệ ⇒ chỉ `hostname` bắt; `A11` dùng `/x` trên host đúng ⇒ chỉ `path` bắt.

Bảng tập giết đầy đủ 42 đột biến: **mọi đột biến bị giết bởi ca đích của nó**, không đột biến nào có
tập giết rỗng.

### P1-2 `cong-that-nam-trong-main-khong-ai-canh` → **VÁ HỜ**

Executor khai đã tách `chay_cli()` và `__main__` nay chỉ còn `sys.exit(chay_cli())`. Khai ấy **đúng
về hình thức** (`mcp_gh_test.py:645-646`), và phần tách là **bảo toàn hành vi** — tôi đã `diff`
`4aa936e0` → `97617d3a`: logic, dòng in, mã thoát y hệt bản cũ, không nuốt lỗi.

Nhưng hai đột biến vòng 2 **chỉ một cái bị giết**. Mỗi biến thể một tiến trình sạch:

| đột biến | vị trí | rc | kết luận |
|---|---|---|---|
| BASE | — | 0 | nền |
| `try: fn()` → `try: pass` | `chay_cac_ca` | **1** | **ĐÃ BỊ GIẾT** (qua `D8(b)`) |
| `d8_ok = ...` → `d8_ok = True` | `ma_thoat`, `mcp_gh_test.py:378` | **0** | **SỐNG SÓT** |

Và `d8_ok = True` không vô hại — nó **tước răng đúng cái chốt vừa giết đột biến kia**. Ghép hai:

```
GHÉP: try-pass + d8_ok=True
CA         : 39/39 đạt · 0 đỏ
D8(a) đích nằm trong tập giết: ĐỎ ['a1_cong_444', … 42 đột biến …]
D8(b) không tập giết rỗng:     ĐỎ ['a1_cong_444', … 42 đột biến …]
TỔNG: ĐẠT                      rc=0
```

**Cổng tự in ĐỎ ở hai trong ba điều kiện `D8` rồi vẫn kết luận `TỔNG: ĐẠT` và thoát `0`.** Không ca
nào chết. Đó là *"cổng nói dối"* ở dạng thuần nhất, nằm ngay trong cổng dựng ra để chặn nó.

Trả lời câu hỏi *"còn dòng quyết định nào trong `__main__` mà không ca nào với tới"*: `__main__` nay
chỉ còn một dòng và nó vô hại. Nhưng **quyết định đã dời xuống `chay_cli`/`ma_thoat`, và phần lớn
thân `chay_cli` vẫn không ca nào chạm** — chi tiết ở finding P1 mục 6.

Công bằng với executor: `d10_main_khong_chay_ca_phai_do` (`:502`) + đột biến `d10_main_luon_xanh` là
tiến bộ thật, chúng khoá được dòng `return 0 if ok else 1`. Vấn đề là `D10` đi vào `ma_thoat` **chỉ
qua đường `ran` lệch `registry`**, nên nó **có MẶT trong `ma_thoat` mà không có ĐO** dòng `d8_ok` —
đúng hình dạng `t24` trong `CLAUDE.md`.

### P1-3 `b3-chot-cach-ly-mang-neo-theo-TEN` → **ĐÃ VÁ THẬT**

Chạy lại đúng phản chứng vòng 2 — refactor **bảo toàn hành vi**, nội tuyến opener:

```python
self._mo = mo or _mo_mac_dinh
# thành
self._mo = mo or (lambda req, timeout: _OPENER.open(req, timeout=timeout))
```

| biến thể | `B3` |
|---|---|
| gốc | ĐẠT |
| gốc + `b3_bo_token` | **ĐỎ** `AssertionError: đã ra mạng` |
| REFACTOR | ĐẠT |
| **REFACTOR + `b3_bo_token`** | **ĐỎ** `AssertionError: đã ra mạng` |
| REFACTOR, chạy trọn 39 ca | không ca nào đỏ |

Vòng 2 phản chứng này làm `B3` mù; nay `B3` vẫn giết `b3_bo_token` sau refactor, và refactor không
làm hỏng ca nào khác. `B3` đã neo vào **đường ra mạng thật**, không vào tên hàm.

Kèm: `B3` khôi phục `socket.create_connection` trong `finally` (`:263-264`) — tôi đo `is` sau khi
chạy ca, đúng đối tượng gốc, **không rò sang ca khác**.

### P1-4 `khong-cong-nao-chay-bo-test` → **CHƯA VÁ, và lời khai ĐÚNG**

`rg mcp_gh` ngoài write set: **chỉ đặc tả nhắc tới**, không workflow nào chạy `mcp_gh_test.py`. Vá
được thì phải chạm `.github/workflows/` — ngoài write set. Mở nợ có tên là **xử lý đúng**.

**Có đủ không — tôi nói KHÔNG chặn land, nhưng nợ phải mô tả đúng rủi ro, vì nó tệ hơn "chưa có
cổng".** Đo được: `launcher-windows.yml:20-27` bắn theo `paths: ['.claude/dev/**']`. Nghĩa là một PR
hoặc một lần đẩy master chạm `mcp_gh.py` **sẽ kích hoạt workflow ấy, nó chạy `launcher_test.py` rồi
XANH** — một check xanh trên đúng đường dẫn vừa sửa, chưa từng chạy bộ test này. Đó là
*"cổng vắng mặt trông giống cổng xanh"*, và nó làm nợ này dễ bị quên hơn nợ thường.

Không có cổng tự cưỡng chế nào bắt được: `ci_phamvi.py` đo phạm vi gói phát hành, không đo
*"mọi `_test.py` có ai chạy không"*.

Đề nghị: **không chặn land vì lý do này** (thật sự ngoài write set), nhưng packet land kế tiếp phải
có điều kiện hoàn tất là nối `mcp_gh_test.py` vào `ci.yml`, và thân nợ phải ghi thẳng câu
*"`launcher-windows.yml` sẽ xanh trên đường dẫn này mà không chạy bộ test"*.

---

## 3. Bảng chấm A/B/C/D

Nền: `bind` được, 39/39 ca, 42/42 đột biến bị giết. `ĐẠT` dưới đây nghĩa là **đã đo**, không phải suy ra.

| nhóm | tiêu chí | chấm | ghi chú đo được |
|---|---|---|---|
| A | A1 A2 A3 A4 A8 | ĐẠT | đột biến đích giết đúng ca đích |
| A | **A5 A6-302 A6-303 A7** | **ĐẠT (ĐO THẬT)** | hai `http.server` loopback dựng được; `Authorization` tới đích thứ hai = `[]` cho cả 301/302/303/307/308 |
| A | **A9-host A10-scheme A11-path** | **ĐẠT** | ba ca MỚI, mỗi ca giết đúng một đột biến, **không chồng lấn** |
| B | B1 B2 B4 B5 B6 B8 B9 | ĐẠT | — |
| B | **B3** | **ĐẠT** | sống sót phản chứng refactor của vòng 2; khôi phục sạch |
| B | B7-khong-ghi · B7-cache · B7-ten | ĐẠT | — |
| B | **B7-xoa** | **ĐẠT trên giấy, KHÔNG đo cơ chế nó khai** | P2 còn mở, đo ở mục 4 |
| C | C1 C2 C3 | ĐẠT | phản chứng trên vị ngữ `cong` |
| C | **C4** | **ĐẠT trên giấy, không bắt được ca vô hiệu THẬT** | P2 còn mở, đo ở mục 4 |
| D | D1 D2 D3 D4 D5 D6 D7 D8 D10 | ĐẠT | — |
| D | D7b | ĐẠT (không kích hoạt) | nền tôi XANH nên nhánh `KHÔNG_ĐO_ĐƯỢC` không chạy; ca `d7b` vẫn đo vị ngữ |
| D | **D9** | **ĐẠT về số, SAI về đơn vị** | P2 còn mở, đo ở mục 4 |
| — | **thân `chay_cli` / `ma_thoat`** | **KHÔNG ĐẠT** | P1 mục 6 |

Giao phạm vi cổng in ra — dữ liệu chẩn đoán, `D8` cố ý không làm đỏ:

| đột biến | đích | ca ngoài đích cũng chết |
|---|---|---|
| `b6_bo_chot_init` | B6 | D6 |
| `b7_bo_cam_ghi` | B7-khong-ghi | B7-xoa |
| `c4_khong_goi_ca` | C4 | **D10-main** ← MỚI ở lượt này |

---

## 4. Năm P2 của vòng 2 — cái nào còn đúng

| slug | trạng thái | phép đo |
|---|---|---|
| `so-lieu-dong-bang-cua-dac-ta-da-troi-va-tien-de-doi-don-vi-sai` | **VẪN ĐÚNG, và trôi XA HƠN** | đo ở dưới |
| `d9-do-thu-khac-han-thu-D9-noi` | **VẪN ĐÚNG** | đo ở dưới |
| `c4-khong-bat-duoc-ca-vo-hieu-tren-du-lieu-that` | **VẪN ĐÚNG** | đo ở dưới |
| `b7-xoa-khong-tai-hien-co-che-pyc-ma-no-khai` | **VẪN ĐÚNG** | đo ở dưới |
| `rut-van-ban-bo-content-1-tro-di` | **VẪN ĐÚNG** | đo ở dưới |

Không cái nào vô tình được vá, không cái nào trở nên sai.

**`so-lieu-dong-bang…`** — đặc tả dòng 255 viết *"mã đứng ở **802** (`mcp_gh.py` 230 ·
`mcp_gh_test.py` 572) suốt từ lượt 2"*. Đo tại SHA nghiệm thu:

| đại lượng | đặc tả nói | đo được | lệch |
|---|---|---|---|
| `mcp_gh.py` | 230 | **230** | 0 |
| `mcp_gh_test.py` | 572 | **646** | +74 |
| tổng mã | 802 | **876** | +74 |
| đặc tả | `210 → 258 → 289` | **315** | +26 |

Quan hệ nội tại vẫn sạch (230 + 572 = 802), nên câu ấy **đọc như đã kiểm** — đúng bài học
*"một bất biến còn đúng không chứng minh các số hạng còn đúng"*. Kéo theo một câu nữa sai: dòng 258
viết *"802 nằm dưới ngưỡng 1.000 … với biên gần 200"*; biên thật là **124**. Và chốt chống lặp dòng
268 (*"nếu MÃ chạm 900 thì câu trả lời là TÁCH"*) nay chỉ còn **24 dòng** đệm.

**`d9-do-thu-khac-han-thu-D9-noi`** — `D9` trong đặc tả (dòng 199): *"`git diff --numstat` trên write
set, cột dòng THÊM, ≤ trần của lease"*, và **r2 cố ý KHÔNG ghi cứng con số**. Ca thật
(`mcp_gh_test.py:497-499`) đếm **tổng số dòng của hai tệp** và **ghi cứng `900`**. Hai chỗ lệch:
đo *độ dài tệp* chứ không đo *dòng thêm của diff*, và ghi cứng đúng con số đặc tả dặn đừng ghi cứng.
Hôm nay hai cách cho **cùng 876** (vì `b662fe1` chưa có hai tệp ⇒ dòng thêm = số dòng), nên phép đo
sai trùng kết quả với phép đo đúng — chúng chỉ tách nhau khi có lượt xoá dòng.

**`c4-khong-bat-duoc-ca-vo-hieu-tren-du-lieu-that`** — đo thẳng: ở biến thể `try: pass` (không thân
ca nào chạy), **không ca nào chết, `C4` cũng không**. Cổng đỏ nhờ `D8(b)`, không nhờ `C4`. Lý do:
`chay_cac_ca` gọi `ran.append(name)` **trước** `try`, nên sổ `ran` vẫn đầy. `C4` chỉ đo vị ngữ `cong`
trên tuple bịa (`:396-397`), không đo dữ liệu thật.

**`b7-xoa-khong-tai-hien-co-che-pyc-ma-no-khai`** — đây là phép đo tôi thấy đáng giá nhất trong mục
này. `CLAUDE.md` mô tả cơ chế: CPython coi `.pyc` còn hợp lệ theo **(mtime giây, KÍCH THƯỚC)**. Ca
`b7_xoa_pyc_cu` (`:304-314`) dùng `GIA_TRI = 'cu'` (15 byte) rồi `GIA_TRI = 'moi'` (**16 byte**):

```
kích thước: cu=15  moi=16  -> KHÁC NHAU, va chạm (mtime,size) KHÔNG THỂ xảy ra
  ca HIỆN TẠI (kích thước lệch) : lần2='moi'  -> nạp mã MỚI, cơ chế KHÔNG tái hiện
  kích thước BẰNG NHAU          : lần2='cu1'  -> NẠP MÃ CŨ, cơ chế TÁI HIỆN
```

Nghĩa là bỏ `xoa_pyc` **vẫn nạp mã mới**; đột biến `b7_bo_xoa_pyc` bị giết **chỉ bởi khẳng định vệ
sinh cuối** (`assert not …cache_from_source(…).exists()`), không bởi cơ chế nạp-mã-cũ mà `B7` khai.
Ca hiện tại không thể đỏ vì đúng cái bệnh nó mang tên.

**`rut-van-ban-bo-content-1-tro-di`** — `mcp_gh.py:107-108` chỉ đọc `nd[0]["text"]`. Bơm ba phần tử
`content` ⇒ trả `'PHAN-1'`, mất im lặng phần 2 và 3.

---

## 5. Bản vá có đẻ lỗi mới không

`git diff 4aa936e0 97617d3a` = **48 thêm / 12 xoá, chỉ trong `mcp_gh_test.py`**. `mcp_gh.py` KHÔNG
đổi một dòng nào ở lượt này.

- **`chay_cli()` có nuốt lỗi / đổi mã thoát / đổi dòng in không?** → **KHÔNG.** Đối chiếu từng dòng
  với `__main__` cũ: cùng vị ngữ, cùng `print("TỔNG: …")`, cùng `0/1`. Là phép tách bảo toàn hành vi.
- **Ba ca mới có độc lập không?** → **CÓ**, đo ở P1-1: mỗi ca giết đúng một đột biến riêng.
- **Vá `socket.create_connection` toàn cục có rò không?** → **KHÔNG.** Khôi phục trong `finally`,
  kiểm bằng `is` sau khi chạy ca; chạy trọn suite sau đó vẫn 39/39.
- **Ngân sách** → `git diff --numstat b662fe1 -- <hai tệp mã>` cho **230 + 646 = 876 thêm, 0 xoá**.
  Khai của executor **876/900 là ĐÚNG**. Đệm còn 24 dòng.

Bản vá này **không đẻ lỗi mới** theo nghĩa làm hỏng thứ đang chạy — khác hẳn ba lượt của #318. P1
còn lại là **phần chưa vá**, không phải phần vá hỏng.

---

## 6. Finding mới

### `cong-tu-mo-cua-bang-hai-dong-trong-duong-quyet-dinh` — **P1**

Thân `chay_cli()` và dòng `d8_ok` trong `ma_thoat` là đường quyết định của cổng, **không ca nào
chạm và không đột biến nào trong `MUTATIONS` nhắm vào**. `D8(c)` chỉ đòi *mọi CA là đích của một đột
biến*; nó không đòi *mọi DÒNG QUYẾT ĐỊNH có đột biến canh*, nên cổng mù với chính nó.

Trích dòng:

```
mcp_gh_test.py:378      d8_ok = not failed and not any(d8_errors)
mcp_gh_test.py:628-629  d8_errors = ((), (), ()) if failed else loi_d8(
                            tuple(name for name, _ in CASES), MUTATIONS, kill_sets)
mcp_gh_test.py:640      rc = ma_thoat(CASES, ran, MUTATIONS, failed, mutation_errors, d8_errors)
```

Phép đo tái lập được — mỗi biến thể một tiến trình sạch, ghi đè lên bản sao tạm, không đụng cây thật:

| đột biến | rc | cổng |
|---|---|---|
| BASE | 0 | ĐẠT (đúng) |
| `d8_ok = True` | **0** | **SỐNG SÓT** |
| `d8_errors = ((), (), ())` | **0** | **SỐNG SÓT** |
| `rc = 0` | **0** | **SỐNG SÓT** |
| `try: pass` trong `chay_cac_ca` | 1 | bị giết |
| bỏ `chay_dot_bien` | 1 | bị giết |

Hậu quả đo được, và đây là lý do nó là P1 chứ không phải P2 — ghép **hai dòng**
(`try: pass` + `d8_errors = ((), (), ())`):

```
CA         : 39/39 đạt · 0 đỏ
ĐỘT BIẾN   : đã đo 42/42 tập giết
D8(a) đích nằm trong tập giết: ĐẠT
D8(b) không tập giết rỗng: ĐẠT
D8(c) mọi ca có đột biến canh: ĐẠT
TỔNG: ĐẠT                                        rc=0
```

**Không một thân ca nào được chạy**, mà cổng in một báo cáo SẠCH HOÀN TOÀN. Đây đúng site #6 và #7
trong bảng `hinh_dang_ke_thua` của chính đặc tả (*"cổng báo xanh trong khi không đo gì"*) — tái sinh
bên trong cổng dựng ra để đóng nó. Với `d8_ok = True` một mình thì cổng còn **tự in ĐỎ hai điều kiện
`D8` rồi vẫn kết luận ĐẠT**, tức bản in và mã thoát nói ngược nhau.

**Đề nghị vá (vừa túi ngân sách):** thêm một ca đo `ma_thoat` qua đường `d8_errors` — ví dụ
`ma_thoat(CASES_1, RAN_KHOP, MUT_1, (), (), (("x",), (), ()))` phải trả `1` — kèm đột biến
`d8_ok = True` nhắm vào ca đó. Khoảng 6 dòng; đệm còn 24 nên **không phải nâng trần, không phải
tách**. Nên cân nhắc thêm một đột biến cho `d8_errors = ((), (), ())`.

### `b3-chi-canh-mot-choke-point` — **P2**

`B3` đếm kết nối bằng cách bọc `socket.create_connection`. Đo độ phủ bằng server loopback của chính
tôi, khi chốt đang bật:

```
đếm create_connection bị gọi: 0
đường socket thô .connect() : KẾT NỐI THÀNH CÔNG (chốt MÙ)
đường tiến trình con (curl) : KẾT NỐI THÀNH CÔNG (chốt MÙ)
```

**KHÔNG phải lỗi hiện tại**: `mcp_gh.py` chỉ đi `urllib` → `http.client` → `socket.create_connection`,
nên hôm nay chốt phủ đúng đường thật, và P1-3 vẫn là ĐÃ VÁ THẬT. Đây là giới hạn phạm vi: lượt sửa
nào thêm một đường ra mạng khác (`socket.connect` trực tiếp, tiến trình con) thì `B3` im lặng mất
răng. Đáng ghi một dòng trong ca để lượt sau không đọc `B3` rộng hơn thứ nó đo.

### `c4-va-d10-dung-chung-vi-ngu-cong` — **P2**

Đột biến `c4_khong_goi_ca` nay giết **cả `C4` lẫn `D10-main`** (bảng giao phạm vi, dòng mới ở lượt
này). `D10` gọi `ma_thoat` → `ma_thoat` gọi `cong`, nên hỏng `cong` là hỏng luôn `D10`. Ràng buộc
thiết kế r2 (đặc tả dòng ~170) nói *"ca của một tiêu chí không được đi qua đúng đoạn mã mà đột biến
của tiêu chí KHÁC nhắm vào"*. Executor **vẫn trong khuôn khổ `D8`** vì `D8` cố ý chỉ IN giao phạm vi
chứ không làm đỏ — nên đây là P2, không phải P1. Chỉ nêu để người land thấy lượt này **thêm một**
giao phạm vi chứ không giảm.

---

## 7. CHỖ KHÔNG ĐO ĐƯỢC

- **Hành vi trên GitHub thật.** Mọi ca đều offline/bơm phản hồi. Không lượt nào chứng minh
  `mcp_gh.py` nói chuyện được với `api.githubcopilot.com` thật. `D2` tự khai điều này
  (`:409` — *"phản hồi bơm; chưa đo được từ công cụ thật"*). Tôi **không** thử gọi thật.
- **Nền Windows.** Đo trên Linux 3.11.15. `.claude/dev/**` chạm tới `launcher-windows.yml` nhưng
  workflow ấy không chạy bộ test này, nên hành vi Windows của `mcp_gh_test.py` là
  `KHÔNG_ĐO_ĐƯỢC` — chưa ai chạy lần nào, kể cả lượt này.
- **Nền cấm `bind`.** Vỏ của tôi cho `bind`, nên tôi **không** đo được đường `D7b` in
  `KHÔNG_ĐO_ĐƯỢC`. Executor đo được đường đó còn tôi đo được đường kia; **hai lượt bù nhau, không
  lượt nào một mình phủ cả hai nền.**
- **Trạng thái vòng 2 nguyên bản.** Tôi suy nó là `4aa936e0` theo `git log` của nhánh; không có
  verdict vòng 2 trong cây để đối chiếu từng chữ. Bốn slug P1 tôi lấy từ prompt, không từ hiện vật
  có băm.
- **Số của đặc tả về lịch sử trần** (750 → 1000 → 1100) và các mốc `11:22Z` / `11:4xZ` 26-08: tôi đo
  được số **hiện tại**, không tái lập được các mốc quá khứ ấy.
- **`.git` gắn CHỈ ĐỌC** — tôi không `git add`, không commit, không push. Tệp verdict này ghi thẳng
  vào cây làm việc.

---

## Tóm tắt cho người land

| P1 vòng 2 | phán quyết |
|---|---|
| `chot-dich-credential-khong-co-phan-chung` | **ĐÃ VÁ THẬT** |
| `cong-that-nam-trong-main-khong-ai-canh` | **VÁ HỜ** — nửa còn lại là P1 duy nhất đang chặn |
| `b3-chot-cach-ly-mang-neo-theo-TEN` | **ĐÃ VÁ THẬT** |
| `khong-cong-nao-chay-bo-test` | **CHƯA VÁ**, khai đúng, ngoài write set — không chặn land |

**Còn 1 P1** (`cong-tu-mo-cua-bang-hai-dong-trong-duong-quyet-dinh`), vá ~6 dòng trong đệm ngân sách
24 dòng. Năm P2 vòng 2 còn nguyên, cộng hai P2 mới. Bản vá không làm hỏng thứ gì đang chạy, và hai
trong bốn P1 đã đóng bằng phản chứng đo được.
