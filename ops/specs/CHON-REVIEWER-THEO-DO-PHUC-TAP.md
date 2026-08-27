# ĐẶC TẢ PACKET — `CHON-REVIEWER-THEO-DO-PHUC-TAP`

```yaml
packet_id: CHON-REVIEWER-THEO-DO-PHUC-TAP
revision: 3
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
| `tai-lieu` | `references/`, `*.md` ở gốc |
| **`khong-biet`** | **mọi đường dẫn KHÔNG khớp bảng trên** |

`khong-biet` KHÔNG được bỏ qua. Đường dẫn không phân loại được là đường ta chưa nghĩ tới, và
bài học `lease-authority-spoof` nói thẳng: danh sách CẤM thua từ trong thiết kế, phải đảo thành
danh sách CHO PHÉP — mà allow-list thì bắt buộc phải có nhánh "ngoài danh sách" và nhánh ấy
phải ĐẨY LÊN, không phải tha.

**Điểm — cộng dồn, tất định:**

```
+2  review_class == "sensitive"
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

- `review_class` so với ALLOW-LIST `("sensitive", "thuong")` sau khi `strip()`. **KHÔNG
  casefold**, và nói rõ vì sao: giá trị này đọc từ tệp lease, nơi nó được ghi ở đúng một dạng;
  chấp nhận `SENSITIVE` là chấp nhận hai chính tả cho một khái niệm, và kho đã trả giá cho
  chuyện ấy (`lease-authority-spoof`: *"phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN"*).
  Ngoài allow-list ⇒ **`KhongDoDuoc`**, KHÔNG phải "coi như thường".
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

**BẰNG CHỨNG DƯƠNG DUY NHẤT:** `yeu_cau_model` phải CÓ MẶT làm **khoá** trong `modelUsage`.

ĐỎ khi bất kỳ điều nào:

- `ket_qua_json` là `None`/không phải dict ⇒ KHÔNG ĐO ĐƯỢC;
- `is_error` là `True` **hoặc thiếu** (thiếu = không đo được, `None != False`);
- `modelUsage` thiếu/không phải dict/rỗng;
- **`yeu_cau_model` không nằm trong khoá của `modelUsage`** — thử theo thứ tự: (a) khớp KHOÁ;
  (b) nếu không, khớp `canonicalModel` của một mục bất kỳ. Cả hai trượt ⇒ ĐỎ.

**KHÔNG được coi khoá THỪA là lỗi.** `modelUsage` gần như luôn mang thêm mô hình phụ của
harness (`claude-haiku-4-5-20251001` ở cả 6 lượt đo). Luật "đúng một khoá" của revision 1 là
luật SAI và đã bị bác bằng phép đo — xem §0(c′). Hàm phải **kể ra** khoá thừa trong thông báo,
không phải từ chối vì chúng.

**KHÔNG được đọc `rc` hay `subtype` làm bằng chứng ĐẠT.** §0(c) là lý do; ghi lý do ấy vào chú
thích ngay tại hàm, không phải chỉ ở đây.

### 3.4 CLI

`python3 .claude/dev/chon_reviewer.py --review-class sensitive --duong-dan a.py,b.md --so-dong 120 --luot 1`
→ in `model`, `effort`, `giai_thich`; `--json` cho dạng máy đọc. Thoát 0 khi chọn được, khác 0
khi `kiem_dinh_danh` từ chối.

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
6. Ca thiếu `is_error` ⇒ ĐỎ. Ca `modelUsage` chỉ có `canonicalModel` khớp (không khớp khoá)
   ⇒ ĐẠT, và ca `canonicalModel` khớp một mô hình KHÁC ⇒ ĐỎ.
7. Ca ĐƠN ĐIỆU: thêm một khoản điểm không bao giờ làm bậc TỤT (chạy qua mọi tổ hợp
   `review_class` × vùng × ngưỡng, so bằng chỉ số bậc).

**ĐỘT BIẾN — mỗi bản vá một đột biến, và runner phải đòi giết ĐÚNG VÀ CHỈ ĐÚNG tập ca đã khai**
(chạy từng đột biến trên TOÀN BỘ ca, không phải chỉ tập đích). Tối thiểu:

| đột biến | phải giết |
|---|---|
| bỏ nhánh `khong-biet` (coi như không cộng điểm) | ca 2 |
| bỏ bánh cóc | ca 3 |
| nhận bí danh vào allow-list | ca 4 |
| `kiem_ket_qua` đọc `subtype == "success"` thay vì `is_error` | ca 5 |
| `kiem_ket_qua` đòi `modelUsage` có ĐÚNG MỘT khoá (luật sai của revision 1) | ca 5 |
| `kiem_ket_qua` chỉ kiểm `modelUsage` RỖNG, không kiểm có mô hình yêu cầu | ca 5 |
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
