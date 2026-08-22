Đo xong. Cây review sạch, HEAD không đổi (`6eaa3755`), mọi đột biến chạy trên bản sao tạm `/tmp/rv227d/*`.

```
KET_LUAN: can_sua
reviewed_sha: 6eaa3755abd96ef6d8f820daaa6b9d96e2bdd7b5
```

## Neo đã kiểm

`r6` = `4ee67d54…` ✓ · `r5` = `2c8fb5c6…` ✓ · verdict lượt 3 = `79f8bb2a…` ✓. Suite nền `67/67` rc=0.

## Phần CỐT LÕI của r6 — ĐẠT, và tôi đo lại độc lập chứ không chép

Phép dẫn xuất vị trí **có thật**, không phải dời chỗ ghi cứng. 8 hướng tấn công vào chính nó, mỗi hướng một bản sao tạm:

| đột biến YAML | kết quả | ĐỎ |
|---|---|---|
| `C1` = M4 (dời `check` xuống sau POST) | 64/67 | `t51 t63 t67` |
| `C2` **chiều ngược** (dời `$GITHUB_ENV` lên trước POST) | 65/67 | `t66 t67` |
| `C3` đổi tên biến `ID`→`CID` | 64/67 | `t64 t66 t67` |
| `C4` thêm một khoảng trắng trong dòng POST | 60/67 | `t51 t52 t60 t62 t63 t66 t67` |
| `C5` tách dòng POST bằng dấu chéo ngược | 64/67 | `t64 t66 t67` |
| `C6` thêm lời gọi POST **thứ hai** không đăng ký | 64/67 | `t62 t63 t66` |
| `C7` chú thích chứa **nguyên văn** dòng POST đặt đầu vòng lặp | 65/67 | `t66 t67` |
| `C8` chú thích chỉ chứa `gh api` | 67/67 | xanh — **đúng** |

Ba trạng thái của §1 đều **ĐỎ**, và tôi có bằng chứng dương cho trạng thái "không phân tích được":

```
$ cd /tmp/rv227d/run-C4-them_khoang_trang_POST && python3 ops/lease_publish_test.py
  ĐỎ  t66_moi_guard_co_phan_chung_va_ve_theo_vi_tri: ValueError: substring not found
  ĐỎ  t67_ve_khang_dinh_phai_khop_vi_tri_dan_xuat_tu_YAML: ValueError: substring not found
```

Thêm: `t66` **không** chết dưới `C1` — đúng như phải thế, vì kỳ vọng của nó **trôi theo YAML**; chỉ `t67` (sổ đăng ký lệch) chết. Đó là bằng chứng mạnh nhất rằng `t66` dẫn xuất thật.

Và bốn đột biến "guard còn nhưng hành vi sai" (§3) đều chết: bỏ `continue` của `check` → 65/67 (`t51 t66`) · bỏ qua lặng lẽ → 65/67 · `$GITHUB_ENV` cảnh báo thay vì chặn → 66/67 (`t66`) · `mark` nhận id `"0"` → 64/67. **Không ca nào trống ruột** — kể cả guard `$GITHUB_ENV` mà codex tự khai là yếu.

---

## P2 — một trong TÁM guard của sổ **không có ca nào chết khi gỡ nhánh chặn của nó**

Gỡ đúng nhánh xử lý lỗi của khối POST (giữ nguyên `set +e`/`rc=$?`/`set -e`), suite **XANH TRỌN VẸN**:

```
  A5-case_id(POST)   rc=0  lease_publish: 67/67 đạt  ĐỎ=khong
```
7 guard còn lại cùng đột biến ấy đều chết (`A0`…`A7`: 65/67 hoặc 66/67, luôn có `t66`).

Đây **không** phải equivalent mutant. Đồ giả `gh` trả `rc=1` **nhưng in ra một id SỐ hợp lệ** — chính tình huống nhánh ấy sinh ra để chặn:

```
--- BAN GOC (guard rc cua POST CON):
{"rc": 1, "posts": ["dau","giua","cuoi"], "marks": {"dau":true,"giua":false,"cuoi":true}}
--- SAU DOT BIEN A5 (guard rc cua POST BI GO):
{"rc": 0, "posts": ["dau","giua","cuoi"], "marks": {"dau":true,"giua":true,"cuoi":true}}
```
Gỡ guard ⇒ bước **XANH** và `giua` **được `mark` bằng id đến từ một lời gọi hỏng**. Suite không thấy gì.

**Gốc**: sổ khoá theo **KHỐI** `set +e`, nhưng thứ được khẳng định là **NHÁNH chặn**. Mục #6 khoá vào `ID=$(gh api …)` (khối POST) lại **đặt tên `case_id`** và ca của nó bơm lỗi vào câu `case "$ID"` — một nhánh nằm **ngoài mọi khối**, nên không có trong tập dẫn xuất. Tôi xác nhận bằng đo: gỡ riêng nhánh `case "$ID"` → 66/67 ĐỎ `t66`, **trùng khít** dòng "Gỡ guard `case ID` | 66/67 | t66" của handoff §3. Tức bảng đột biến của executor đo **nhánh `case`**, còn khoá đăng ký là **khối POST** — hai thứ khác nhau, và cái tên đã che chỗ hở.

Hệ quả với đặc tả: `T66′` đòi *"Gỡ từng guard ⇒ ca của guard đó ĐỎ (tám đột biến riêng)"* — **7/8**, không phải 8/8.

**Vá đề xuất** (~9 dòng): thêm knob `guard_hong="post_rc"` cho `gh_gia.py` (in id số + `SystemExit(1)`) và một ca `t68` khẳng định `rc==1`, `posts.count("giua")==1`, `marks["giua"] is False`. Phản chứng của chính nó là đột biến `A5` ở trên.

## P2 — bộ trích guard phân biệt **CÁCH VIẾT**, không phân biệt **NHÁNH CHẶN**

Thêm một guard chặn thật (gọi `bao_chan` + `continue`) vào thân bước, **không đăng ký**:

```
  D1-chinh_tac(M1)      rc=1  66/67  ĐỎ=['t64']      <- bat duoc
  D5-trong_ham_shell    rc=1  66/67  ĐỎ=['t64']      <- bat duoc
  D2-mot_dong_set+e     rc=0  67/67  ĐỎ=khong        <- LOT
  D3-if_!_cmd           rc=0  67/67  ĐỎ=khong        <- LOT
  D4-cmd_||_rc          rc=0  67/67  ĐỎ=khong        <- LOT
```
`_guard_dan_xuat` neo vào đúng một mẫu (`^set +e$` … `^rc=$?$` … `^set -e$`). Ba cách viết mà một người sẽ gõ thật đều vô hình. Nói cho công bằng: **viết lại** guard sẵn có sang hình dạng khác thì bị bắt (`D6` 66/67 `t64`; `D7` bỏ hết `set +e` → 64/67, `t65` fail-close kêu) — chỗ mù chỉ ở đường **THÊM**. Nhưng đó đúng là đường mà `T64` sinh ra để chặn, và không mục `chua_do_duoc` nào của r2–r6 hay handoff §5 khai nó. Đây là hình dạng "danh sách CẤM không bao giờ đủ" của `CLAUDE.md`: bộ trích liệt kê *cách viết* guard thay vì đòi *mọi nhánh chặn* phải nằm trong tập.

**Vá đề xuất** (2 dòng, đảo sang danh sách CHO PHÉP): mọi nhánh chặn **bắt buộc** gọi `bao_chan` (chỉ nó đặt `BI_CHAN`), nên đếm nó là đủ đóng. Đo nền: 9 lời gọi `bao_chan` vs 8 khối. Nguyên mẫu đã chạy — thêm vào `_guard_dan_xuat`:

```python
bang(len(re.findall(r'bao_chan "', than)) == bat + 1,
     "có nhánh gọi bao_chan nằm ngoài guard được trích")
```
```
  goc                 rc=0  67/67  ĐỎ=khong
  D2-mot_dong_set+e   rc=1  66/67  ĐỎ=['t64']
  D3-if_!_cmd         rc=1  66/67  ĐỎ=['t64']
  D4-cmd_||_rc        rc=1  66/67  ĐỎ=['t64']
```
Kèm chốt: `+1` phải được chú thích là nhánh `case "$ID"`, và P1 ở trên nên xoá luôn dấu `+1` bằng cách đăng ký nhánh ấy tường minh.

## P3 — `_ve_dan_xuat` fail-close **không có phản chứng**

`t65` khoá fail-close cho `_guard_dan_xuat` (rỗng / hỏng). Không ca nào khoá `_ve_dan_xuat`: nó ĐỎ chỉ nhờ `ValueError`/`StopIteration` lọt lên `except Exception` của `main()`. Ai đó bọc `try` hoặc cho `next(..., mặc_định)` là chốt câm mà không ca nào kêu. Vá ~4 dòng: nối vào `t65` một thân đã đổi cách viết dòng POST và đòi `_ve_dan_xuat` **ném**.

## §5 — D lần 4? Tôi trả lời tách làm hai, vì hai trục cho hai câu trả lời khác nhau

- **Trục vế (câu hỏi prompt nêu): KHÔNG phải D.** Nhãn chỉ có hai (`VE_TRUOC_POST`/`VE_SAU_POST`) nhưng `t66` thực tế tính **hai boolean độc lập** — `co_post` theo vị trí POST và `da_mark` theo vị trí `mark` — nên tập vế phân **ba** lớp: trước POST · sau POST trước `mark` · sau `mark`. `C2` chứng minh trục thứ hai có răng. Không cần trục nữa.
- **Trục ĐƠN VỊ guard: đúng hình dạng D lần 1–2 (khối vs nhánh).** Câu kiểm chứng đặt ở độ phân giải **khối** trong khi thứ được khẳng định sống ở độ phân giải **nhánh** — và nó đã sinh ra đúng một lỗ đo được (P2 thứ nhất).

Tôi **không** tự tuyên D lần 4 ⇒ DỪNG, và nói rõ lý do để người giữ kho tự quyết: lựa chọn "guard = khối `set +e`" là của **r5/Q25**, đã qua hai lượt review, không phải nước đi mới của lượt 6; cái mới chỉ là một nhánh sót không được khai. Nếu người giữ kho đọc bộ đếm theo hình dạng chứ theo tác giả, thì đây là **D = 4** và chốt đã đăng ký của r6 biến verdict này thành `dung_lai` — tôi nêu thẳng chứ không giấu sau chữ `can_sua`.

Hai chốt riêng của lượt 6 thì **không** kêu: `M4` giết `T67` (đo lại độc lập, `C1`), và không guard nào có vế bất khả thi.

## §4 Hồi quy — 9 dòng xoá, từng dòng có lý do

Cả 9 đều là **viết lại tại chỗ**, không dòng nào mất chức năng: chữ ký `_chay_buoc_dang` (+`guard_hong`) · `mark` một dòng → khối (chỗ móc lỗi `github_env`) · `viet(...)` (chỗ móc `packet_issue`) · `.replace("gh api"…)` (nối thêm `echo BI_CHAN`) · dòng `env` (+`GUARD_HONG`) · 4 dòng trong `gh_gia.py` (thêm `lease` vào comment, `ge.exists()`→`ge.is_file()`, hai đường lùi cho `body`/`payload`). Hai đường lùi ấy **không** phải đồ giả diễn kịch bản: chúng chỉ hiện khi guard bị GỠ, và khi ấy `gh` **thật sự đã được gọi** cho lease đó — chúng giữ TRẠNG THÁI cho quan sát được, đúng doctrine. Bộ ca 63 → 67, không ca nào bị xoá hay đổi tên. Một hạt sạn P3 nhỏ: `"env": ghe.read_text() if ghe.exists()` sẽ ném `IsADirectoryError` nếu lease `cuoi` không chạy tới `mark` (chỗ khôi phục tệp); hôm nay không tới được, nhưng nó biến một lỗi sản phẩm tương lai thành một cú crash khó đọc.

## Ngân sách

Ba bản vá cộng lại ≈ **15 dòng** (9 + 2 + 4) — **lọt** trần còn `27` (`+633/660`). Đây là con số người giữ kho hỏi.

## `da_do_gi`

40 lượt chạy suite trên bản sao tạm: gỡ nhánh chặn từng guard (8) · gỡ nhánh `case "$ID"` (1) · gỡ cả khối guard (8) · tấn công phép dẫn xuất vị trí (8) · hình dạng guard thêm/viết lại (7) · guard-còn-hành-vi-sai (4) · nguyên mẫu bản vá (4). Cộng hai lượt probe hành vi chứng minh `A5` không phải equivalent mutant. `actionlint` 1.7.7 rc=0. Cây review sạch, HEAD `6eaa3755`.

## `khong_do_duoc`

- **Vẫn chưa có lượt GitHub Actions THẬT, chưa có Windows** — không đóng được từ container. **Thu hẹp**, không đóng: thân bước đã chạy thật dưới bash tại chỗ qua 40 cấu hình.
- Chưa đo `gh` thật (mọi lượt đi qua đồ giả).
- **Ngoài delta, không đo**: `ops/lease_publish.py` (+105/−7 của lượt trước) và phần YAML (+70/−8) — tôi chỉ đột biến chúng, không rà nội dung.
- Cửa sổ "POST xong, `mark` hỏng" · khe race hai nhánh `ops/**` · `t59` chỉ so `argv[0:2]` · ruleset ngoài kho: **giữ nguyên `chua_do_duoc` của r2–r6**, không mục nào tôi thấy khai hẹp hơn thực tế — trừ chỗ **thiếu hẳn** hai mục P2 ở trên.
