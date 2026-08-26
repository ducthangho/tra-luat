---
kieu: dac_ta_delta
packet: T33-DOI-SHELLCHECK
ban: r4
trang_thai: dang_hieu_luc
thay_the:
  - tep: ops/specs/t33-doi-shellcheck-r2.md
    dong: 232
    sha256_tep_bi_thay: b9620d17b86f503b12d93359fb6d3423d29c034c29ab372f40cc5d7089b40e71
  - tep: ops/specs/t33-doi-shellcheck-r3.md
    dong: 192
    sha256_tep_bi_thay: 78c3ecb40eb8dd7dcf628ef7ea9a372aae5cfbf7a4fcfd25bb4ec7f32fe6ea0d
pham_vi_thay_the: chon_loc      # CHỈ hai dòng trên; mọi phần khác của r2/r3 GIỮ NGUYÊN hiệu lực
ghi_chu_hinh_dang: >-
  CẤU TRÚC NÀY LÀ TẠM. Chưa cổng nào đọc nó — đã đo, không tầng nào phân tích khối này.
  Packet "cơ chế trạng thái đặc tả" (hướng (2) của #297) ĐƯỢC PHÉP đổi hoàn toàn hình dạng.
  Đây là DỮ LIỆU để packet ấy kế thừa, KHÔNG phải giao diện để nó tuân theo. Đừng đọc sự tồn
  tại của khối này thành "đã có cơ chế".
---

# `t33-doi-shellcheck` — bản delta `r4`

**Đây là DELTA, không phải bản viết lại.** Nó thay **đúng hai dòng** trong `r2` và `r3`. Mọi phần
khác của hai bản ấy **giữ nguyên hiệu lực**, và **hai tệp ấy không đổi một byte nào** — ai đang neo
băm `r2`/`r3` vẫn neo đúng.

Căn cứ: Issue **#297**, và quyết định của chủ kho ngày `26-08-2026` trả lời hai câu hỏi mở của nó.

---

## 1. Hai chỗ được hạ — cùng MỘT câu, nguyên văn

`r2:232` và `r3:192` là **cùng một câu**, chỉ khác con số ở dòng ngay trên (`88/88` ở `r2`,
`97/97` ở `r3`).

**Nguyên văn đang có trên master:**

```text
    định ấy tra theo NỀN: thay mệnh đề nền bằng phân biệt theo TÊN TỆP vẫn cho 88/88,
    rc=0 trên toàn chân Ubuntu (đo 23-08-2026). Ca này khoá đúng cái trục ấy.
```

**Sai ở đâu:** `"toàn chân Ubuntu"` chỉ một **job/leg của CI**. Bằng chứng có trong tay là một lượt
chạy trong **worktree cục bộ**; không chỗ nào trong hồ sơ dẫn ra một lượt chạy CI cho đột biến ấy.
Lời khai **rộng hơn phép đo** — hình dạng `A`.

**Bản hạ — chép nguyên văn từ bản vá ĐÃ LAND, không tự nghĩ lại:**

```text
    định ấy tra theo NỀN: thay mệnh đề nền bằng phân biệt theo TÊN TỆP vẫn cho 88/88,
    rc=0 khi chạy cục bộ trên Linux (đo 23-08-2026). Ca này khoá đúng cái trục ấy.
```

(ở `r3`: `88/88` → `97/97`, phần còn lại y hệt.)

**Vì sao chép chứ không soạn lại:** câu thay thế này **không phải** một lời khai mới của `r4`. Nó là
bản vá **đã qua review và đã land** ở `3239279b`, và hôm nay vẫn đứng nguyên trong mã —
`ops/lease_publish_test.py:3134`:

```text
    rc=0 khi chạy cục bộ trên Linux (đo 23-08-2026). Ca này khoá đúng cái trục ấy.
```

Đây đúng luật `#238/r4/Q13` — *"chép bản vá đã chạy, KHÔNG tự nghĩ lại"*. Trớ trêu đáng ghi: chính
luật ấy đã **vận chuyển trung thành** câu sai từ `r2` vào mã (đó là nội dung của #297), và nay nó
vận chuyển **bản vá** theo chiều ngược lại. Luật không sai; thứ sai là để nó chạy một chiều.

**Hệ quả:** sau khi `r4` land, mã và đặc tả **thôi lệch nhau**. Bản ghi lệch hiện sống ở lease `r4`
của #249 (khối `ghi_de_byte_identity_voi_dac_ta`) trở thành **hết thời hiệu** — nó mô tả một trạng
thái không còn nữa.

---

## 2. `r2:215` — NGOÀI PHẠM VI, và đây là lý do

Câu ở `r2:215`:

```text
`X2` là **một mệnh đề**, và nó làm cổng nền tra theo một trục hoàn toàn khác mà **toàn bộ chân Ubuntu
im lặng**. Thứ duy nhất tách hai trục là 8 dòng `BỎ QUA` trên chân `windows-latest` — …
```

Nó dùng **cùng một cách lượng hoá** với câu sai nằm cách đó mười mấy dòng — nhưng **KHÔNG cùng byte**:
`r2:215` viết `toàn bộ chân Ubuntu`, `r2:232` viết `toàn chân Ubuntu`. Đo bằng phép so chuỗi chính xác:

```text
r2:215   'toàn bộ chân Ubuntu' in=True    'toàn chân Ubuntu' in=False
r2:232   'toàn bộ chân Ubuntu' in=False   'toàn chân Ubuntu' in=True
```

(Bản đầu của `r4` viết *"đúng cụm từ"* — **SAI byte**, và cross-review chéo nền bắt được. Trong một
tệp mà nghề của nó là hạ lời khai cho khớp phép đo, một mô tả văn bản sai byte là lỗi cùng họ.)

Câu hỏi *"đây có phải finding không"* đã được đặt **hai lần**. Ghi đáp án ra đây để lần thứ ba không
ra kết quả khác.

### Phép thử phân xử: câu ấy khai **KẾT QUẢ MỘT LƯỢT CHẠY**, hay **SUY LUẬN TỪ TIỀN ĐỀ ĐƯỢC CHỈ RA**?

| | `r2:232` · `r3:192` | `r2:215` |
|---|---|---|
| khai gì | **kết quả một lượt chạy** — `"vẫn cho 88/88, rc=0 … (đo 23-08-2026)"`, có cả **ngày đo** | **một tính chất** — chân Ubuntu không phân biệt được trục này |
| gán cho đâu | **`"toàn chân Ubuntu"`** — một job/leg của CI | cùng cách lượng hoá, nhưng không kèm lượt chạy nào |
| bằng chứng thật có gì | một lượt chạy trong **worktree cục bộ**; không chỗ nào dẫn ra lượt CI | **tiền đề được chỉ ra tại chỗ** (xem dưới) |
| kiểm lại được không | phải **chạy** trên một runner Ubuntu — chưa ai làm | **suy ra được từ mã**, không cần chạy |

Tiền đề của `r2:215`, nêu ngay tại chỗ nên người đọc kiểm được: `t73` truyền `nen="posix"`, **trùng
`os.name` thật** của một runner Linux, nên gỡ mệnh đề nền là **no-op** với nó; thứ phân biệt hai trục
là **8 dòng `BỎ QUA`** trên chân `windows-latest`.

### Luật rút ra — dùng lại được, không cần hỏi lại

**Hình dạng `A` là về LỜI KHAI KẾT QUẢ CHẠY.** Hỏi: *câu này khai một lượt chạy đã xảy ra, hay suy ra
từ tiền đề nó chỉ ra?* Khai lượt chạy thì phải có lượt chạy ấy — đúng nền, đúng phạm vi. Suy luận thì
phải **chỉ ra tiền đề tại chỗ** để người đọc kiểm được mà không phải chạy gì.

**Bản đầu của `r4` dùng một thước KHÁC và nó SAI** — *"bằng chứng hay giải thích"*. Cross-review chéo
nền bác đúng hai chỗ, và cả hai đều đo được: (a) `r2:232` **nằm trong docstring** của ca, tức bản thân
nó cũng là văn giải thích — nên phân đôi ấy không tách được hai câu; (b) `r4` khi ấy viết *"bỏ câu
`232` đi thì không còn gì chứng minh có lỗ"*, **trái ngay bảng đo ở `r2:209-213`** đã ghi
`X2 = 88/88, rc=0, KHÔNG CA NÀO` — **bảng mới là bằng chứng**, không phải câu `232`.
Thước cũ còn nguy hơn là chỉ sai: nó **tha** một lời khai quá phép đo chỉ vì câu ấy nằm trong đoạn
văn giải thích. Thước mới không có cửa đó.

### Khai thẳng: đây là kết luận của một LẬP LUẬN

Không phải của một phép đo. **Không cổng nào phân xử được nó** — kho không có cơ chế canh văn xuôi
(`t42` khớp marker nợ ↔ sổ; `doc-claims-check` đọc trích dẫn số hiệu văn bản). Ai không đồng ý thì
bác bằng lập luận, và `r4` sẽ phải sửa.

**Và `r2:215` KHÔNG "sạch".** Nó dùng cụm từ của câu sai ở gần đó, nên người đọc không tách được hai
thứ bằng mắt — bằng chứng là câu hỏi này đã được hỏi hai lần. Đó là lỗi **DỄ ĐỌC NHẦM**, không phải
lỗi **SAI**. `r4` **không** sửa nó.

---

## 3. `r4` KHÔNG làm gì

- **Không** dựng cơ chế trạng thái máy đọc được (hướng (2) của #297). Đó là packet riêng, chưa có
  đặc tả, và còn một câu hỏi thiết kế chưa ai trả lời: **một cổng LÀM GÌ khi đặc tả bị đánh dấu đã
  thay thế** — từ chối cho lease neo vào (fail-close mạnh, chặn mọi lease đang neo `r2`/`r3`), hay
  chỉ cảnh báo (luật không có răng)?
- **Không** sửa `r2:215`.
- **Không** đụng `r1` (`ops/specs/t33-doi-shellcheck.md`).
- **Không** đo lại toàn bộ số của `r2`/`r3` cho khớp master.

---

## 4. `r4` tự chịu chính phép thử nó đang áp

Một bản đặc tả sửa lỗi *"khai rộng hơn đo"* mà **tự** khai rộng hơn đo thì tệ hơn không sửa. Nên:

- **KHÔNG khai "đã quét hết".** Số đo được là **hai** chỗ hình dạng `A` cộng **một** chỗ cần người
  quyết. `"chỉ ba"` là kết luận của **một** phép quét theo cụm từ — tức một **danh sách đoán trước**
  — không phải một chứng minh. Còn lời khai nào cùng hình dạng mà **không** chứa cụm `"chân Ubuntu"`
  hay không: **CHƯA ĐO ĐƯỢC**.
- **Số `r4` là TÁI DÙNG CÓ CHỦ ĐÍCH, không phải số trống — và bản đầu của `r4` khai SAI chỗ này.**
  Bản đầu viết *"`r4` chưa từng tồn tại trên ref nào"*, và còn bác một câu trong lease đã thu hồi.
  **Cả hai đều sai**, cross-review chéo nền bác được bằng object trong chính cây:

  ```text
  $ git log --all --format='%H %s' -- ops/specs/t33-doi-shellcheck-r4.md
  e87eae9d…  #249 RÚT đặc tả r4 khỏi PR #293 — land phần mã, tách việc đặc tả sang packet riêng
  ee545cf5…  #249 đặc tả r4 (delta): đóng NGUỒN của P2 — hạ lời khai "toàn chân Ubuntu" ở r3:192
  ```

  Tức **đã có một `r4`**, thêm ở `ee545cf5`, **rút** ở `e87eae9d`, chưa bao giờ lên master. Lease
  `spec-r5-overclaim-exec-1` (đã thu hồi) khai *"r4 … chỉ trên nhánh `claude/t33-doi-shellcheck-exec-1`
  (PR #293)"* — **ĐÚNG**. Câu bác nó là câu sai, và nó đã bị rút.

  **Vì sao phép quét của bản đầu trượt:** nó chạy `git cat-file -e "<ref>:<đường-dẫn>"` trên **TIP**
  của từng ref. Tệp được thêm rồi **xoá**, nên không tip nào còn nó. Phép đo trả lời đúng câu
  *"tip nào đang có tệp này"* — và bản đầu đọc nó thành *"tệp này chưa từng tồn tại"*. **Lời khai
  rộng hơn phép đo — hình dạng `A`, ngay trong tệp sinh ra để sửa hình dạng `A`.**

  Điều đo được và giữ nguyên: `ops/specs/t33-doi-shellcheck-r4.md` **vắng ở base `9044a5d`** và vắng
  ở mọi tip đã quét. Tái dùng số `r4` là **có chủ đích**: bản `ee545cf5` có **cùng mục đích** với
  bản này (hạ đúng lời khai `"toàn chân Ubuntu"`) và đã bị rút vì lý do phạm vi, không vì nội dung.
  Ai muốn đọc bản cũ thì tra `ee545cf5`. **Định danh là BĂM, không phải tên bản.**
- **Băm của hai tệp bị thay đã đo tại chỗ**, ghi trong khối đầu tệp. Ai đọc `r4` mà thấy băm không
  khớp thì `r2`/`r3` đã bị động — và khi ấy `r4` phải được xét lại, không được dùng.

---

## 5. Vì sao delta TRƯỚC, cơ chế SAU

Ba lý do, xếp theo sức nặng — ghi lại để người đọc sau không phải dựng lại:

1. **Cái đang gây hại là SỰ LAN TRUYỀN, và cơ chế không chặn được nó.** `r3` tồn tại **vì** `r2` bị
   chép; `r2:232` là **nguồn phát**. Một cơ chế trạng thái làm việc *đánh dấu* trở nên máy-đọc-được
   — nó **không** sửa câu sai, nên ai chép `r2` trong lúc chờ vẫn chép đúng câu ấy.
2. **Hướng (2) chưa có gì để thi công** — chưa đặc tả, chưa packet, chưa lease, và còn câu hỏi thiết
   kế ở §3. Chặn một bản sửa **hai câu** sau một packet chưa có hình hài là để cái cổng **chưa tồn
   tại** chặn việc **đã rõ**.
3. **Delta này không phí công** vì phần đánh dấu ghi bằng khối máy-đọc-được ở đầu tệp: packet cơ chế
   **kế thừa dữ liệu**, không phải đọc văn xuôi rồi đánh dấu lại. Kèm `ghi_chu_hinh_dang` khai thẳng
   rằng hình dạng ấy là **tạm** — thiếu câu đó là lén đặt trước giao diện cho một packet chưa được
   thiết kế.
