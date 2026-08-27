# ĐẶC TẢ PACKET — `CHON-REVIEWER-THEO-DO-PHUC-TAP`

```yaml
packet_id: CHON-REVIEWER-THEO-DO-PHUC-TAP
revision: 6
generation: 1
review_class: sensitive          # sua chinh duong REVIEW - thu quyet dinh ai kiem cai gi
executor: codex
reviewer: claude
assurance_target: cross_approved
```

> Chủ kho ra lệnh trực tiếp 27-08-2026: *"executor thì dùng codex, xhigh. reviewer thì chọn từ
> opus 5 high cho tới fable 5 max tùy độ phức tạp. nếu chưa implement trong skill thì lưu ý đưa
> vào để implement việc chọn mô hình theo độ phức tạp."*

## 0. Vấn đề — ba phép đo, không phải ba lo ngại

Đo 27-08-2026 trong chính container này, `claude` 2.1.247. **Cả ba đều FAIL-OPEN.**

**(a) `--effort` sai ⇒ CẢNH BÁO rồi IM LẶNG lùi về mặc định.**

```
$ claude --effort khong-ton-tai -p "x"
Warning: Unknown --effort value 'khong-ton-tai' — ignoring it and using the default effort.
          Valid values: low, medium, high, xhigh, max.
```

Gõ nhầm một bậc nỗ lực ⇒ reviewer chạy ở mức mặc định, và **không có gì trong kết quả nói ra
điều đó**. Một lượt review "xhigh" có thể chưa bao giờ là xhigh.

**(b) `--model` sai ⇒ `rc=0`.**

```
$ claude --model claude-khong-ton-tai-9 -p "OK"; echo "rc=$?"
"claude-khong-ton-tai-9" is not a model this version of Claude Code recognizes...
[claude-code:unrecognized_model] {"model":"claude-khong-ton-tai-9","query_source":"sdk"}
There's an issue with the selected model. It may not exist or you may not have access to it.
rc=0
```

Đúng bài học `CLAUDE.md`: *"Cổng xanh nhờ `rc=0` là cổng CÓ THỂ BỊ LỪA — phải đòi BẰNG CHỨNG
DƯƠNG"*. Một harness chỉ đọc `rc` sẽ ghi nhận "review đã chạy" cho một lượt **không có review nào**.

**(c) `--output-format json` là chỗ DUY NHẤT nói thật, và nó nói ngược `rc`.**

Đo lần đầu ở một thư mục TRỐNG ngoài kho:

| yêu cầu | `rc` | `subtype` | `is_error` | khoá của `modelUsage` |
|---|---|---|---|---|
| `claude-opus-5` | 0 | `success` | `false` | `["claude-opus-5"]` |
| `claude-fable-5` | 0 | `success` | `false` | `["claude-fable-5"]` |
| `claude-khong-ton-tai-9` | 0 | **`success`** | **`true`** | `[]` |

`rc` và `subtype` **cùng nói dối**; `is_error` nói thật.

**(c′) NHƯNG BẢNG TRÊN LÀ CỦA MỘT NGỮ CẢNH, VÀ NÓ KHÔNG TỔNG QUÁT.** Đo lại trong một sandbox
CÓ kho (có `CLAUDE.md`, có `.claude/`), sáu lượt:

| yêu cầu | dùng công cụ? | `is_error` | khoá của `modelUsage` |
|---|---|---|---|
| `claude-opus-5` | không | `false` | `["claude-haiku-4-5-20251001", "claude-opus-5"]` |
| `claude-opus-5` | có | `false` | `["claude-haiku-4-5-20251001", "claude-opus-5"]` |
| `claude-fable-5` | không | `false` | `["claude-fable-5", "claude-haiku-4-5-20251001"]` |
| `claude-fable-5` | có | `false` | `["claude-fable-5", "claude-haiku-4-5-20251001"]` |
| `claude-sonnet-5` | không | `false` | `["claude-haiku-4-5-20251001", "claude-sonnet-5"]` |
| `claude-khong-ton-tai-9` | không | **`true`** | **`["claude-haiku-4-5-20251001"]`** |

Một **mô hình phụ** (`claude-haiku-4-5-20251001`) có mặt ở **cả sáu** lượt — kể cả lượt không
gọi công cụ nào. Hai hệ quả, và cả hai đều bác một luật của REVISION 1:

1. **"đúng một khoá" là luật SAI** — nó làm `kiem_ket_qua` từ chối **mọi lượt chạy thật** trong
   ngữ cảnh có kho. Đó không phải một lỗ, nó là một cổng TỰ KHOÁ: công cụ vô dụng ngay từ lượt
   đầu. (Revision 1 đã viết đúng luật ấy, và bản nháp executor đã cài đúng nó:
   `raise KhongDoDuoc("modelUsage phải có đúng một khoá")`.)
2. **"`modelUsage` rỗng ⇒ ĐỎ" KHÔNG bắt được model rác** trong ngữ cảnh có kho: ở đó model rác
   cho `modelUsage` **KHÔNG rỗng** — nó chứa đúng mô hình phụ. Một phép kiểm chỉ nhìn RỖNG sẽ
   cho lượt ấy đi qua.

Và `canonicalModel` **khác** khoá khi id có ngày: khoá `claude-haiku-4-5-20251001` →
`canonicalModel: "claude-haiku-4-5"`. Nên so `canonicalModel` một mình cũng không đủ chặt.

**BẰNG CHỨNG DƯƠNG ĐÚNG, và nó là MỘT câu:** *mô hình ĐÃ YÊU CẦU phải CÓ MẶT làm KHOÁ trong
`modelUsage`.* Câu ấy bắt được model rác ở **cả hai** ngữ cảnh (khoá `[]` và khoá chỉ-có-phụ đều
thiếu mô hình yêu cầu), và **không** từ chối lượt hợp lệ nào. Khoá thừa là mô hình phụ của
harness — ghi ra để người đọc biết, KHÔNG coi là lỗi.

Bài học đứng sau, và nó đắt hơn con số: **một bảng đo đúng vẫn có thể sinh ra một luật sai nếu
bảng ấy chỉ có MỘT ngữ cảnh.** Revision 1 đo ở thư mục trống, thấy đúng một khoá, rồi viết luật
"đúng một khoá" — luật ấy mô tả CÁI RIG chứ không mô tả CÔNG CỤ. Cùng họ với bài học
*"phép đo delta phải dựng cả hai vế trong MỘT lệnh"*: rig lặng lẽ trở thành một phần của kết luận.

**(c″) BA LẦN ĐẶC TẢ NÀY SAI, VÀ HAI LẦN CÙNG MỘT GỐC — ghi ở đây vì nó là bài học của packet.**

| revision | luật sai | gốc |
|---|---|---|
| 1 | `modelUsage` phải có ĐÚNG MỘT khoá | đo ở **một** ngữ cảnh (thư mục trống) rồi viết luật mô tả CÁI RIG |
| 2 | không ai validate `review_class` | thiếu sót |
| 3 | allow-list `("sensitive", "thuong")` | **bịa** từ vựng thay vì **đếm** từ vựng đang dùng |
| 4 | §3.3 *"KHÔNG được coi khoá THỪA là lỗi"* | luật viết **rộng hơn miền đã đo**: chỉ đo được MỘT loại khoá thừa (mô hình phụ) là vô hại, rồi cấm từ chối khoá thừa NÓI CHUNG |

Revision 1, 3 và 4 cùng một gốc: **viết luật TRƯỚC khi đo miền giá trị**. Cả hai đều hỏng theo
hướng **fail-CLOSED** — công cụ từ chối đầu vào hợp lệ — nên chúng không lộ ra như một lỗ mà
lộ ra như một cổng không dùng được. Cả hai lần executor cài **đúng** thứ được giao, và cả hai
lần thứ bắt được là **một phép đo trên dữ liệu thật**, không phải một lượt đọc lại mã.

Hệ quả thực hành cho bất kỳ ai viết đặc tả cho packet này về sau: mỗi khi đặc tả nêu một TẬP
GIÁ TRỊ HỮU HẠN (tên mô hình, tên lớp review, tên vùng, tên khoá JSON), **đếm nó trong kho
trước**, và dán số đếm vào đặc tả. Một allow-list không kèm số đếm là một allow-list chưa đo.

**(c‴) VÀ REVISION 4 CŨNG SAI — bắt được bằng một cú tụt THẬT, hai lần trong một ngày.**

§3.3 r4 viết *"**KHÔNG được coi khoá THỪA là lỗi**"*, lý do kèm theo là mô hình phụ có ở cả sáu
lượt đo. Luật ấy **rộng hơn miền đã đo**: bảng (c′) chứng minh được rằng MỘT loại khoá thừa
(mô hình phụ của harness) là vô hại, còn luật thì cấm từ chối khoá thừa **nói chung**.

Hậu quả đo được 27-08-2026, trên chính kho này, **hai lượt cross-review dài liên tiếp**:

| lượt | `modelUsage` | mô hình phục vụ thật | §3.3 r4 |
|---|---|---|---|
| `rv349` (2081s) | `[claude-fable-5, claude-haiku-4-5, claude-opus-4-8]` | `claude-opus-4-8` **84.1%** | **ĐẠT** |
| `rv349b` (1549s) | `[claude-fable-5, claude-opus-4-8]` | `claude-opus-4-8` **87.8%** | **ĐẠT** |

Cả hai `rc=0`, `subtype=success`, `is_error=false`, và `claude-fable-5` **có mặt làm khoá** —
nên bằng chứng dương của (c′) được thoả, và §3.3 r4 cho cả hai đi qua. Tụt **TOÀN PHẦN** thì
(c′) bắt được; tụt **GIỮA CHỪNG** thì lọt. Và tụt giữa chừng là ca ĐÃ XẢY RA.

**Con số của (c′) cũng phải sửa.** Đếm lại trên **9 lượt** (3 dài + 6 probe ngắn, 27-08-2026):

```
claude-haiku-4-5-20251001   8/9    <- KHONG phai 6/6; mot luot dai KHONG co haiku nao
claude-fable-5              6/9
claude-opus-5               3/9
claude-opus-4-8             2/9    <- ca hai deu la luot TUT
```

Nên allow-list mô hình phụ phải **CHO PHÉP** nó, tuyệt đối không được **ĐÒI** nó có mặt — đòi
thì lặp lại đúng lỗi fail-CLOSED của revision 1, chỉ đổi hình dạng.

Bài học riêng của lần này, khác với (c″): revision 1 và 3 hỏng vì **chưa đếm**. Revision 4 hỏng
vì **đếm rồi nhưng khái quát quá phép đếm** — từ *"loại khoá thừa NÀY vô hại"* nhảy sang
*"khoá thừa nói chung không phải lỗi"*. Một allow-list có số đếm vẫn sai nếu kết luận rộng hơn
thứ số đếm chống đỡ được.

**(d) Và chưa có chỗ nào trong kho ghi chọn mô hình theo cái gì.**

```
grep -rn "fable\|--effort\|--model" .claude/skills/    ⇒  0
```

Nay executor là `codex` còn reviewer là `claude` với **bốn** bậc khả dĩ. Không có luật thì mỗi
lượt một người chọn một kiểu, và chọn thấp thì lỗ lọt — đúng điều đo được ở #341/#342/#343:
mỗi packet cần 3–4 lượt mới sạch.

## 1. `write_set`

```
.claude/dev/chon_reviewer.py            # MOI
.claude/dev/chon_reviewer_test.py       # MOI
.claude/skills/cross-review/SKILL.md
```

**Đúng ba đường. Không đụng gì khác** — đặc biệt KHÔNG đụng `launcher.py`, `packet_loop.py`,
`scripts/tl.py`, `.github/workflows/**`. Cần đụng thì DỪNG và báo, đừng tự mở rộng.

## 2. `ngan_sach_kich_thuoc`

| | |
|---|---|
| tệp tối đa | **3** |
| dòng thêm tối đa | **520** |

Vượt ⇒ DỪNG và NÉN. Đang viết hơn 520 dòng nghĩa là đang làm một packet khác.

## 3. `.claude/dev/chon_reviewer.py` — hợp đồng CHÍNH XÁC

Hai nửa, và nửa thứ hai mới là nửa có răng.

### 3.1 `chon(review_class, duong_dan, so_dong, luot, bac_truoc=None)` → `(model, effort, giai_thich)`

VỊ TỪ THUẦN. Nhận dữ liệu làm đối số — điều kiện để có ca BIẾT TRƯỚC ĐÁP ÁN
(bài học `MOC_MO_HO_CO_SAN`, PR #343).

**Vùng, phân loại theo TIỀN TỐ đường dẫn, ALLOW-LIST:**

| vùng | tiền tố |
|---|---|
| `cong` | `.github/workflows/`, `.claude/hooks/`, `.claude/dev/packet_loop`, `ops/lease_publish` |
| `giao-thuc` | `docs/PROTOCOL_DA_PHIEN.md`, `docs/adr/`, `.claude/skills/` |
| `runtime` | `scripts/` |
| `dev` | `.claude/dev/` (phần còn lại), `ops/` (phần còn lại) |
| `tai-lieu` | `references/`, `*.md` ở gốc, `docs/` (phần còn lại) |
| **`khong-biet`** | **mọi đường dẫn KHÔNG khớp bảng trên** |

**REVISION 6 — bảng trên lần đầu được ĐẾM trên `write_set` THẬT.** Cho tới r5, bảng vùng là
bảng DUY NHẤT trong đặc tả này chưa qua phép đếm mà chính §0(c″) bắt buộc — một sự bỏ sót đáng
ghi, vì packet này tồn tại để dạy đúng luật ấy. Đếm 51 đường `write_set` duy nhất trên mọi
nhánh (27-08-2026):

```
dev 23 · cong 12 · khong-biet 11 · giao-thuc 4 · tai-lieu 1
```

**11/51 (~22%) rơi `khong-biet`**, mỗi đường +3 điểm. Chiều hỏng là LEO bậc — an toàn, nhưng
mọi packet chạm các đường quen thuộc ấy đều trả phí review đắt nhất. Bổ sung, có lý do:

| đường | vùng | vì sao |
|---|---|---|
| `.github/checks/` | `cong` | mã cổng CI — cùng loại với `.github/workflows/` |
| `.claude/settings.json` | `cong` | quyền + hook: mặt điều khiển, không phải cấu hình phong cách |
| `RELEASE_MANIFEST.json` | `cong` | `release-verify` đọc nó làm nguồn chân lý |
| `.claude/agents/` | `giao-thuc` | frontmatter ÉP quyền agent (`disallowedTools`) — một hợp đồng, không phải tài liệu |
| `docs/` (phần còn lại) | `tai-lieu` | tài liệu; `docs/PROTOCOL_DA_PHIEN.md` và `docs/adr/` vẫn là `giao-thuc` và đứng TRƯỚC trong thứ tự khớp |
| `.gitignore` | `dev` | |

**Tiền tố `planned:`** (protocol §8 định nghĩa) phải được **bóc ra trước khi phân loại**, rồi
phân loại phần còn lại. `planned:ops/x.sh` là `dev`, không phải `khong-biet`. Đây là một NHÃN,
không phải một phần của đường dẫn — coi nó là đường dẫn thì mọi lease dùng nhãn hợp lệ của
protocol đều bị tính +3 oan.

Sau bổ sung, đếm lại trên đúng 51 đường ấy: **`khong-biet` = 0**. Con số này phải được đo lại
mỗi khi bảng đổi; một bảng vùng không kèm số đếm là một bảng chưa đo.

`khong-biet` KHÔNG được bỏ qua. Đường dẫn không phân loại được là đường ta chưa nghĩ tới, và
bài học `lease-authority-spoof` nói thẳng: danh sách CẤM thua từ trong thiết kế, phải đảo thành
danh sách CHO PHÉP — mà allow-list thì bắt buộc phải có nhánh "ngoài danh sách" và nhánh ấy
phải ĐẨY LÊN, không phải tha.

**Điểm — cộng dồn, tất định:**

```
+2  review_class == "sensitive"
+1  review_class == "systemic"
+2  cham vung `cong`
+1  cham vung `giao-thuc`
+1  so_tep >= 5
+1  so_dong >= 400
+1  luot >= 3
+3  co vung `khong-biet`
```

**Bậc:**

| điểm | model | effort |
|---|---|---|
| `<= 0` | `claude-opus-5` | `high` |
| `1–2` | `claude-opus-5` | `xhigh` |
| `3–4` | `claude-fable-5` | `xhigh` |
| `>= 5` | `claude-fable-5` | `max` |

**BÁNH CÓC (`bac_truoc`) — không bao giờ TỤT bậc giữa các lượt của cùng một packet.** Truyền
`bac_truoc=(model, effort)` của lượt trước; kết quả phải `>=` bậc ấy. Lý do: lượt sau thường có
diff NHỎ hơn (chỉ còn phần vá), nên điểm tụt và reviewer bị hạ cấp **ĐÚNG LÚC** vừa có bằng chứng
là lượt trước chưa đủ. `bac_truoc=None` ở lượt 1.

`giai_thich` phải liệt kê từng khoản điểm đã cộng và bậc cuối — để người đọc verdict biết vì sao,
không phải tin một con số.

### 3.1b VALIDATE ĐẦU VÀO — và đây là chỗ REVISION 2 tự dẫm lên chính mình

Đo trên bản thi công theo revision 2 (gọi thẳng `chon()`):

```
review_class='sensitive'  -> claude-fable-5/xhigh     <- dung
review_class='sensitve'   -> claude-opus-5/xhigh      <- GO NHAM MOT CHU, TUT MOT BAC
review_class='SENSITIVE'  -> claude-opus-5/xhigh      <- HOA THUONG, TUT MOT BAC
review_class=None         -> claude-opus-5/xhigh
duong_dan=[]              -> claude-opus-5/xhigh      <- WRITE SET RONG, KHONG day len
so_dong=-999, luot=-5     -> claude-opus-5/high
```

**Đó ĐÚNG là con bọ mà packet này sinh ra để diệt.** §0(a): `--effort` gõ sai thì CLI cảnh báo
rồi im lặng lùi về mặc định. Ở đây `review_class` gõ sai thì hàm im lặng **bớt 2 điểm** và hạ
cấp reviewer — không cảnh báo, không dấu vết. Một công cụ chống fail-open mà bản thân nó
fail-open thì tệ hơn không có: nó phát ra một con số trông như đã được kiểm.

Bắt buộc:

- `review_class` so với ALLOW-LIST **`("routine", "systemic", "sensitive")`** sau khi `strip()`.
  **KHÔNG casefold**, và nói rõ vì sao: giá trị này đọc từ tệp lease, nơi nó được ghi ở đúng một
  dạng; chấp nhận `SENSITIVE` là chấp nhận hai chính tả cho một khái niệm, và kho đã trả giá
  (`lease-authority-spoof`: *"phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN"*).
  Ngoài allow-list ⇒ **`KhongDoDuoc`**.

  **REVISION 3 GHI ALLOW-LIST NÀY SAI, và cái sai đáng ghi hơn bản vá.** Nó ghi
  `("sensitive", "thuong")` — một từ vựng tôi **nghĩ ra**, không phải từ vựng kho **đang
  dùng**. Đếm trên toàn bộ tệp lease của mọi nhánh `ops/**`:

  ```
  review_class: sensitive   570
  review_class: systemic    167
  review_class: routine      22
  review_class: thuong        0     <- tu toi bia ra
  ```

  Hệ quả nếu land: allow-list ấy **từ chối 167 lease thật** (`systemic`) bằng `KhongDoDuoc` —
  lại một cổng TỰ KHOÁ, đúng hình dạng của lỗi revision 1. Và nó chấp nhận một giá trị **không
  tồn tại**. `docs/PROTOCOL_DA_PHIEN.md:144` khai đúng ba giá trị ấy từ đầu; tôi không đọc.
  Executor phát hiện và ghi vào mục *"chỗ tôi không chắc"* thay vì im lặng làm theo — đó đúng
  là việc của mục ấy.

- Ưu tiên `effective_review_class` khi lease có cả hai trường (đo được: 147 lần xuất hiện) —
  **NHƯNG CHỈ THEO CHIỀU LÊN.** Protocol §8: *dispatcher ghi `effective_review_class` bằng mức
  CAO HƠN giữa khai báo và classifier; executor không được hạ lớp.* Nên `effective` THẤP hơn
  `review_class` chỉ có thể là lease hỏng hoặc bị sửa tay, và tin nó là tự mở một cửa mà
  protocol đã đóng. Luật: xếp hạng `routine < systemic < sensitive`, lấy **hạng CAO HƠN** giữa
  hai trường. Đếm trên toàn kho: **0/8203** (ref,tệp) có `effective` thấp hơn khai báo — lỗ
  chưa bị dẫm, nhưng một công cụ sinh ra để chặn fail-open thì không được tự mở.
  Nó là lớp SAU escalation, tức lớp thật sự có hiệu lực.
- `duong_dan` sau khi chuẩn hoá mà **RỖNG** ⇒ `KhongDoDuoc`. Write set rỗng nghĩa là không đo
  được phạm vi, và không đo được thì không được cho ra bậc THẤP. Cùng lý lẽ với `khong-biet`.
- `so_dong` và `luot` phải là số nguyên `>= 0` (và `luot >= 1`). Ngoài khoảng ⇒ `KhongDoDuoc`.
  Số âm không phải một phạm vi nhỏ; nó là một phép đo hỏng.

Mỗi chốt một ca `rXX_` và một đột biến riêng. Đột biến "coi review_class lạ như thường" phải
giết ca đích — không có nó thì không biết ca đang đo allow-list hay đo thứ khác.

### 3.2 `kiem_dinh_danh(model, effort)` → ném `KhongDoDuoc` nếu sai

ALLOW-LIST, so BẰNG NHAU:

```
MO_HINH_CHO_PHEP = ("claude-opus-5", "claude-fable-5")
NO_LUC_CHO_PHEP  = ("low", "medium", "high", "xhigh", "max")
```

**Bí danh (`opus`, `fable`, `sonnet`) phải BỊ TỪ CHỐI** dù CLI chấp nhận: bí danh trỏ "bản mới
nhất", tức một mục tiêu DI ĐỘNG, và cả kho này neo mọi thứ bằng định danh bền. Một verdict ghi
`model: opus` không tái lập được sau khi bí danh trỏ chỗ khác.

### 3.3 `kiem_ket_qua(yeu_cau_model, ket_qua_json)` → ném `KhongDoDuoc` nếu không chứng minh được

VỊ TỪ THUẦN — nhận **dict đã phân tích**, KHÔNG tự gọi CLI. Một ca test phải chạy được offline,
không mạng, không xác thực; hàm nào tự gọi CLI thì ca của nó không tồn tại ở CI.

**REVISION 5 THAY HẲN LUẬT CỦA r4.** Xem §0(c‴): r4 cấm coi khoá thừa là lỗi *nói chung*, và
hai lượt tụt GIỮA CHỪNG có thật đã đi qua nó. Luật mới là **MỘT phép so TẬP HỢP**.

**ĐỊNH NGHĨA.** Với mỗi mục của `modelUsage`, *danh tính* của nó là `canonicalModel` nếu có,
ngược lại là tên khoá. Gọi:

- `phu` = các mục có danh tính mang tiền tố thuộc allow-list mô hình phụ — **`("claude-haiku-",)`**;
- `chinh` = tập danh tính của mọi mục **còn lại**.

**MIỀN GIÁ TRỊ ĐÃ ĐẾM (9 lượt, 27-08-2026)** — dán số vào đặc tả theo đúng luật của §0(c″):

```
claude-haiku-4-5-20251001   8/9      <- CHO PHEP, KHONG DOI phai co
claude-fable-5              6/9
claude-opus-5               3/9
claude-opus-4-8             2/9      <- ca hai deu la luot TUT
```

ĐỎ khi bất kỳ điều nào, **theo đúng thứ tự này** — thứ tự là một phần của hợp đồng, không phải
chi tiết cài đặt:

1. `ket_qua_json` không phải dict; hoặc `modelUsage` thiếu/rỗng/không phải dict ⇒ KHÔNG ĐO ĐƯỢC;
2. `yeu_cau_model` **không** thuộc `chinh` ⇒ ĐỎ, và thông báo **phải chứa chuỗi `"model yêu cầu"`**;
3. `chinh` còn phần tử **khác** `yeu_cau_model` ⇒ **mô hình LẠ** ⇒ ĐỎ. Thông báo phải nêu đích
   danh mô hình lạ. **Đây là điều r4 cấm, và là chỗ P1 lọt.**
4. `is_error` không bằng `False` (thiếu = không đo được, `None != False`).

**VÌ SAO (4) ĐỨNG SAU (2) VÀ (3), không phải trước.** Ca *model-rác* (`--model` sai) trả
`is_error: true` **và** `modelUsage` chỉ có mô hình phụ. Kiểm `is_error` trước thì nó bị chặn ở
nhánh `is_error`, và người đọc thông báo sẽ đi tìm lỗi harness thay vì thấy *"model yêu cầu
không có mặt"* — tức chẩn sai chỗ. Bộ phản chứng khoá đúng thứ tự này (§4).

**KHÔNG ĐƯỢC ĐÒI mô hình phụ phải CÓ MẶT.** Đo được `8/9`, không phải `9/9` — một lượt dài không
có haiku nào. Đòi nó có mặt là lặp lại lỗi fail-CLOSED của revision 1 dưới hình dạng khác.

**KHÔNG được đọc `rc` hay `subtype` làm bằng chứng ĐẠT.** §0(c) là lý do; ghi lý do ấy vào chú
thích ngay tại hàm, không phải chỉ ở đây. Nhắc lại vì (c‴) làm nó nặng hơn: cả hai lượt tụt đều
`rc=0` **và** `subtype=success`.

Thông báo ĐẠT vẫn phải **kể ra** mô hình phụ đã bỏ qua.

**HƯỚNG HỎNG KHI HARNESS ĐỔI MÔ HÌNH PHỤ:** fail-CLOSED, kèm thông báo nêu đích danh mô hình lạ.
Với một cổng danh tính đó là hướng chấp nhận được — và khi ấy allow-list được cập nhật bằng một
phép ĐẾM mới, không bằng phỏng đoán.

**BẰNG CHỨNG LUẬT NÀY ĐÚNG** — chạy trên cả 9 lượt đã đếm ở trên: **7 ĐẠT / 2 ĐỎ**, và đúng 2 ĐỎ
là hai lượt tụt thật. **0 dương tính giả**, kể cả lượt không có mô hình phụ.

### 3.4 CLI

`python3 .claude/dev/chon_reviewer.py --review-class sensitive --duong-dan a.py,b.md --so-dong 120 --luot 1`
→ in `model`, `effort`, `giai_thich`; `--json` cho dạng máy đọc. Thoát 0 khi chọn được, khác 0
khi `kiem_dinh_danh` từ chối.

**REVISION 6 THÊM `--bac-truoc model,effort`** (tuỳ chọn). Không có nó, **bánh cóc của §3.1 —
một luật BẮT BUỘC — không thể hiện thực được qua lối vào DUY NHẤT mà tài liệu dạy.** Người làm
đúng theo `SKILL.md` ở lượt 2 (diff nhỏ lại) sẽ nhận bậc TỤT, đúng kịch bản §3.1 nêu là lý do
bánh cóc tồn tại. Đặc tả r5 tự mâu thuẫn giữa §3.1 (bắt buộc) và §3.4 (không có đường).

Đây không phải lo ngại lý thuyết: **phiên điều phối đã vấp đúng nó ngày 27-08** khi chọn bậc
cho cross-review lượt 3 của PR #349 — phải áp bánh cóc BẰNG TAY vì CLI không nhận `bac_truoc`.

Giá trị sai dạng (thiếu dấu phẩy, model/effort không thuộc bảng) ⇒ `KhongDoDuoc`, KHÔNG im lặng
bỏ qua — im lặng bỏ qua là fail-OPEN đúng loại §0(a) đã trả giá.

## 4. `.claude/dev/chon_reviewer_test.py` — phản chứng

Chạy `python3 .claude/dev/chon_reviewer_test.py`, thoát 0 khi ĐẠT.

**Bắt buộc:**

1. Ca BIẾT TRƯỚC ĐÁP ÁN cho **cả bốn** bậc, mỗi bậc ít nhất một ca.
2. Ca cho `khong-biet`: một đường dẫn lạ (`vi-du/la.txt`) phải đẩy lên bậc cao nhất.
3. Ca BÁNH CÓC hai chiều: `bac_truoc` cao hơn ⇒ giữ bậc cao; `bac_truoc` thấp hơn ⇒ KHÔNG bị kéo xuống.
4. Ca `kiem_dinh_danh`: bí danh `opus`/`fable` bị TỪ CHỐI; `claude-opus-5` được nhận; effort sai bị TỪ CHỐI.
5. Ca `kiem_ket_qua`, fixture lấy từ **CẢ HAI** bảng §0(c) và §0(c′) — chín bản ghi:
   · thư mục trống: `claude-opus-5` ĐẠT · `claude-fable-5` ĐẠT · `claude-khong-ton-tai-9`
     (`modelUsage: {}`) ĐỎ;
   · sandbox có kho: bốn lượt hai-khoá (`opus`/`fable`, có và không dùng công cụ) **ĐỀU ĐẠT** —
     đây là ca chặn luật "đúng một khoá" quay lại;
   · sandbox có kho, model rác: `is_error: true`, `modelUsage` **CHỈ CÓ mô hình phụ** ⇒ ĐỎ.
     Ca này là ca quan trọng nhất của cả mục: nó ĐỎ vì **thiếu mô hình yêu cầu**, KHÔNG phải vì
     `modelUsage` rỗng — một bản vá chỉ kiểm rỗng sẽ để nó đi qua.
6d. **Ca BACKSLASH (revision 6) — bắt buộc.** `la\\la.md` KHÔNG ở gốc, nên nó KHÔNG phải
   `tai-lieu`. Cài đặt r4/r5 đo *"ở gốc"* bằng *"không chứa `/`"*, nên mọi đường Windows-separator
   đuôi `.md` rơi xuống bậc ĐÁY. Đường lạ phải đẩy LÊN theo luật `khong-biet`, không được tụt.
   Chiều ngược (`.github\\workflows\\ci.yml` → `khong-biet`, leo lên) đã an toàn sẵn.
6e. **Ca EFFECTIVE THẤP HƠN KHAI BÁO (revision 6) — bắt buộc.** Lease
   `{review_class: sensitive, effective_review_class: routine}` phải chấm theo **sensitive**.
   Ca `r12` của r4 đóng đinh đúng hành vi SAI (đáp án là bậc THẤP) — phải sửa ca ấy, không phải
   thêm ca mới bên cạnh nó.
6f. **Ca NHÃN `planned:` (revision 6) — bắt buộc.** `planned:ops/x.sh` phải phân loại là `dev`,
   không phải `khong-biet`.
6g. **Ca BÁNH CÓC QUA CLI (revision 6) — bắt buộc.** Lượt 2 với diff nhỏ hơn, truyền
   `--bac-truoc` bậc lượt 1 ⇒ bậc KHÔNG được tụt. Thiếu ca này thì §3.1 vẫn không có đường
   hiện thực qua lối vào được tài liệu hoá.
6b. **Ca TỤT GIỮA CHỪNG (revision 5, §0(c‴)) — bắt buộc.** `modelUsage` mang **CẢ HAI** mô hình
   chính, ví dụ `{claude-fable-5: …, claude-opus-4-8: …}` với `is_error: false`, yêu cầu
   `claude-fable-5` ⇒ **ĐỎ**. Đây là dữ liệu THẬT của hai lượt `rv349`/`rv349b`, không phải
   fixture bịa. Ca này là thứ duy nhất phân biệt r5 với r4.
6c. **Ca KHÔNG có mô hình phụ — bắt buộc.** `modelUsage` chỉ có đúng mô hình yêu cầu (đo được
   `8/9`, không phải `9/9`) ⇒ **ĐẠT**. Ca này chặn hướng hỏng fail-CLOSED "đòi haiku phải có".
6. Ca thiếu `is_error` ⇒ ĐỎ. Ca `modelUsage` chỉ có `canonicalModel` khớp (không khớp khoá)
   ⇒ ĐẠT, và ca `canonicalModel` khớp một mô hình KHÁC ⇒ ĐỎ.
7. Ca ĐƠN ĐIỆU: thêm một khoản điểm không bao giờ làm bậc TỤT (chạy qua mọi tổ hợp
   `review_class` × vùng × ngưỡng, so bằng chỉ số bậc).

**ĐỘT BIẾN — mỗi bản vá một đột biến, và runner phải đòi giết ĐÚNG VÀ CHỈ ĐÚNG tập ca đã khai**
(chạy từng đột biến trên TOÀN BỘ ca, không phải chỉ tập đích). Tối thiểu:

| đột biến | phải giết |
|---|---|
| bỏ nhánh `khong-biet` (coi như không cộng điểm) | ca 2 |
| `systemic` không cộng điểm (coi như `routine`) | ca `review_class` |
| bỏ ưu tiên `effective_review_class` | ca `review_class` |
| bỏ bánh cóc | ca 3 |
| nhận bí danh vào allow-list | ca 4 |
| `kiem_ket_qua` đọc `subtype == "success"` thay vì `is_error` | ca 5 |
| `kiem_ket_qua` đòi `modelUsage` có ĐÚNG MỘT khoá (luật sai của revision 1) | ca 5 |
| `kiem_ket_qua` chỉ kiểm `modelUsage` RỖNG, không kiểm có mô hình yêu cầu | ca 5 |
| `kiem_ket_qua` nới `chinh == {yeu_cau}` thành `yeu_cau in chinh` (bỏ nhánh mô hình LẠ) | ca tụt-giữa-chừng |
| `kiem_ket_qua` nới thành `issubset` / so tiền tố / so chuỗi con | ca tụt-giữa-chừng |
| `kiem_ket_qua` ĐÒI mô hình phụ phải CÓ MẶT (thay vì cho phép) | ca `modelUsage` không có mô hình phụ |
| `kiem_ket_qua` bỏ `canonicalModel`, chỉ so tên khoá | ca khoá-theo-ngày |
| `kiem_ket_qua` kiểm `is_error` TRƯỚC phép so tập hợp | ca model-rác (phải chặn ở nhánh MODEL) |
| `_cac_duong_dan` coi `\` như ký tự thường (đường Windows đuôi `.md` → `tai-lieu`) | ca backslash |
| `chon` lấy thẳng `effective_review_class` thay vì hạng CAO HƠN | ca effective-thấp-hơn |
| bỏ bóc tiền tố `planned:` trước khi phân loại vùng | ca nhãn `planned:` |
| `main` HOÁN VỊ `a.so_dong` và `a.luot` | ca CLI |
| `--bac-truoc` bị bỏ qua im lặng thay vì áp bánh cóc | ca bánh cóc qua CLI |
| khớp danh tính nới từ so-BẰNG sang chuỗi con / tiền tố | ca `claude-opus-5x` phải ĐỎ |
| hạ ngưỡng biên DƯỚI (`luot>=3→>=2`, `len>=5→>=4`, `so_dong>=400→>=399`, `diem<=4→<4`) | ca ghim biên tuyệt đối |
| `is_error` thiếu ⇒ đọc thành `False` | ca 6 |

Nền có ca ĐỎ ⇒ **TỪ CHỐI công bố điểm đột biến** (bài học P1 của PR #342).

## 5. `.claude/skills/cross-review/SKILL.md` — mục mới

Thêm **một** mục, đặt ngay sau `## Bước 0 — CÔNG CỤ`. Nội dung bắt buộc:

- bảng bậc ở §3.1 (điểm → model/effort) và câu bánh cóc;
- **ba cái bẫy đo được ở §0**, kèm đúng số đo, kèm câu *"`rc` và `subtype` cùng nói dối"*;
- hai lệnh: chọn bậc TRƯỚC khi phóng, và kiểm `modelUsage` SAU khi phóng;
- cú pháp phóng reviewer claude headless, **kèm cờ quyền** — thiếu chúng thì reviewer chạy
  được nhưng **không gọi nổi công cụ nào**, tức một lượt review không đo được gì:
  `claude --model <id> --effort <bac> --output-format json --allowedTools Bash Read Write Edit Glob Grep --permission-mode acceptEdits --add-dir <sandbox> -p "$(cat PROMPT.md)"`
  (đo 27-08: cả `-p "$(cat TEP)"` lẫn `-p < TEP` đều chạy — hai dạng tương đương, đừng khai
  một dạng là sai);
- **`--dangerously-skip-permissions` BỊ TỪ CHỐI khi chạy dưới root** (đo 27-08: *"cannot be
  used with root/sudo privileges for security reasons"*, tiến trình thoát ngay `rc=1`,
  `1.151s`). Container phiên chạy dưới root, nên đường ấy KHÔNG dùng được — phải đi bằng
  `--allowedTools` + `--permission-mode`. Ghi ra để người sau không mất một lượt phóng;
- câu giới hạn: mục này KHÔNG thay §8 của protocol, nó chỉ nói **chọn bậc nào**.

**KHÔNG chép doctrine** — `packet_loop.py doctrine-scan --root .` phải `rc=0`.

## 6. Cổng phải xanh trước khi mở PR

```
python3 .claude/dev/chon_reviewer_test.py
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 .claude/dev/packet_loop.py adr-song --root .
python3 scripts/tl.py doc-claims-check --strict --json
python3 scripts/tl.py workflow-audit  --strict --json
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 ops/lease_publish_test.py
git config core.abbrev 7        # BAT BUOC truoc khi chay cong
```

Cổng nào đỏ ⇒ **đo nền trên `origin/master` sạch rồi so DELTA**; đỏ sẵn thì nói "đỏ sẵn,
delta = 0", đừng vá lung tung.

## 7. Điều KHÔNG được làm

- không đụng đường nào ngoài `write_set`;
- không gọi `claude`/`codex` LIVE bên trong ca test — fixture là dữ liệu đã đo ở §0;
- không đọc `rc` làm bằng chứng ĐẠT ở bất cứ đâu;
- không tự merge, không tự đẩy lên `master`, không tạo PR khác;
- nghĩ ra được một hướng hỏng thì **biến ngay thành ca `rXX_`**, đừng để nó nằm trong chú thích.
