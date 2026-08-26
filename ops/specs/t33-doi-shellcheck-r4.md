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

Nó dùng **đúng cụm từ** của câu sai nằm cách đó mười mấy dòng. Câu hỏi *"đây có phải finding không"*
đã được đặt **hai lần**. Ghi đáp án ra đây để lần thứ ba không ra kết quả khác.

### Phép thử phân xử: câu ấy được đưa ra làm **BẰNG CHỨNG** hay làm **GIẢI THÍCH**?

| | `r2:232` · `r3:192` | `r2:215` |
|---|---|---|
| vai trò | **bằng chứng** — nó *là* chứng cứ rằng cổng có lỗ | **giải thích** — vì sao bảng đo ngay trên nó ra như vậy |
| người đọc tin điều gì | *"đã có người chạy đột biến trên chân Ubuntu của CI và được rc=0"* | *"chân Ubuntu không phân biệt được trục này"* |
| điều đó đúng không | **KHÔNG** | **CÓ**, và **suy ra được** |
| bỏ câu đi thì mất gì | mất **chứng cứ** — không còn gì chứng minh có lỗ | mất **lời giải thích** — con số vẫn đứng nguyên |
| cơ chế phân biệt có nêu tại chỗ không | không | **có** — *"8 dòng `BỎ QUA` trên chân `windows-latest`"* |

Suy dẫn nằm sau `r2:215`, viết ra để người đọc kiểm được: `t73` truyền `nen="posix"`, **trùng
`os.name` thật** của một runner Linux, nên gỡ mệnh đề nền là **no-op** với nó; 8 dòng `BỎ QUA` phân
biệt hai trục đến từ chân `windows-latest`.

### Luật rút ra — dùng lại được, không cần hỏi lại

**Hình dạng `A` là về BẰNG CHỨNG.** Một câu nhắc phạm vi trong lúc **giải thích** một con số đã nêu
ở chỗ khác thì soi bằng thước khác: hỏi *"có suy ra được không"* và *"cơ chế có được nêu tại chỗ
không"*, chứ **không** hỏi *"đã chạy chưa"*.

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
- **Số `r4` còn trống — đã đo, không đoán.** Quét **227 ref** (`refs/heads` + `refs/remotes/origin`):
  `ops/specs/t33-doi-shellcheck-r4.md` **chưa từng tồn tại** trên ref nào. Hồ sơ cũ khai ngược (lease
  `spec-r5-overclaim-exec-1` đã thu hồi, trường `vi_tri_r4_noi_dung_dung_o_CA_HAI_trang_thai`) là do
  nhầm **lease** `r4` với **đặc tả** `r4` — hai thứ khác nhau mang cùng chữ `r4`.
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
