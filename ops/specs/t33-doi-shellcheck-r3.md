# ĐẶC TẢ ĐÓNG BĂNG — `T33-DOI-SHELLCHECK`, **bản sửa đổi 3** (delta)

> **CHỈ ghi phần thay đổi** so với r2 (`b9620d17b86f503b12d93359fb6d3423d29c034c29ab372f40cc5d7089b40e71`).
> r1 (`1405d390ca9376725517d01ef5b8d1abffd6a09d78d2b7206c2f068e7711f4da`) và r2 **KHÔNG bị sửa, KHÔNG
> bị xoá**; mọi thứ r3 không nêu thì r2 (rồi r1) nguyên hiệu lực.

```yaml
packet_id: T33-DOI-SHELLCHECK
packet_issue: 249
revision: 3
base_sha: 5561b6b497989447f9185b26abb1bba154564967   # ĐO LẠI trước khi ký — xem §base_sha
```

## Bản này KHÔNG đặc tả gì mới

r3 **không thêm mục tiêu, không đổi write set, không đổi tiêu chí nào**. Nó làm đúng một việc mà r2
tự ra lệnh phải làm:

> *r2/§base_sha:* "Trước khi cấp lease phải đo lại **ba** thứ trên base ấy, vì cả ba đã trôi khi
> `#275` land: `t33`/`t73` ở dòng nào · số ca của suite (nay 88) · `numstat` của bản vá `M3`."

Đã đo lại. **Trong ba thứ r2 nêu, ĐÚNG MỘT trôi** — số ca suite (88 → 97). `t33`/`t73` **giữ nguyên**
dòng 1312/2649, và `numstat` của `M3` **giữ nguyên** 16. Cộng một thứ **thứ tư r2 không lường trước và
không nằm trong ba thứ ấy: tên ca `t89` đã bị chiếm.**
Nếu cấp lease theo r2 nguyên trạng thì executor sẽ ĐỎ ở **mọi** tiêu chí `W11`–`W13` — không phải vì
bản vá sai, mà vì **số ca suite** nằm trong cả ba tiêu chí ấy.

> **Câu trên đã được SỬA sau cross-review lượt 1 của PR #288 (`P2`, codex).** Bản đầu viết *"Cả ba đều
> trôi"* trong khi bảng ở §"Ba thứ r2 dặn đo lại" — cách đó 40 dòng, **trong cùng tệp này** — nói rõ
> `t33`/`t73`/`numstat` KHÔNG đổi. Một đặc tả tự mâu thuẫn với bằng chứng của chính nó là đặc tả mà
> lượt kiểm điều kiện DỪNG về sau sẽ đọc sai. Ghi lại thay vì lặng lẽ sửa, vì đây đúng lớp lỗi mà cả
> phiên này đi săn.

Mọi con số dưới đây đo trên `master = 5561b6b497989447f9185b26abb1bba154564967`, **10:0xZ 23-08-2026**,
`actionlint 1.7.7` + `shellcheck 0.9.0`. Theo **L5**: đo lại trước bước công bố kế tiếp.

---

## `S1` ĐÃ TẮT — điều kiện chặn của r2 không còn

| | |
|---|---|
| `#275` | **MERGED** `2026-08-23T09:21:59Z`, `merged_by: ducthangho`, head `f12736df` |
| lượt review | **3** — lượt 3 `APPROVE` (`830aa85b`); người giữ kho cấp ngoại lệ trần ADR-0043 (2 → 3) tại `63a4cfc9` |
| `#244` | **CLOSED `completed`** `2026-08-23T09:45:30Z` |
| nhánh chưa merge còn đụng `ops/lease_publish_test.py` | **0** (quét toàn bộ 186 ref) |

Phép so hai nguồn tại thời điểm đo: `ls-remote` **186** = `for-each-ref` **186**, `comm -23` **rỗng**
⇒ không mù.

### Nhưng `ai-dang-giu` vẫn báo **NGƯỜI_GIỮ 5** — và đó là câu hỏi cho người giữ kho

Chạy chính lệnh mà `#244` vừa xây (`ops/lease_publish.py ai-dang-giu ops/lease_publish_test.py`, `rc=0`):

```
NGƯỜI_GIỮ 5: lease-dang-windows-exec-2-codex-20260822    het 2026-08-23T11:00:00Z
             lease-dang-windows-exec-3-codex-20260822    het 2026-08-23T15:00:00Z
             plat-x8-exec-2r6-codex-20260822             het 2026-08-23T14:10:00Z
             plat-x8b-exec-1-codex-20260823              het 2026-08-24T00:40:00Z
             lease-hoi-toan-kho-exec-1r4-codex-20260823  het 2026-08-24T08:25:00Z
```

**Cả năm thuộc packet ĐÃ LAND** — `#238` (`LEASE-DANG-WINDOWS`), `PLAT-X8`/`PLAT-X8b`, và `#244`
(đóng `completed`). Hai đường đo độc lập cho **trạng thái packet**, không hơn: (a) `#244` đóng và PR
merged, (b) **0** nhánh chưa merge chạm tệp.

**Đó là TẤT CẢ những gì hai phép đo ấy nói.** Chúng **không** nói *"không lease nào có writer đang
sống"* — bản đầu của r3 viết đúng câu ấy ở đây, và cross-review lượt 2 của PR #288 bắt được rằng nó
**vẫn còn** sau khi tôi đã vá phần kết luận ở §dưới. Tức tôi sửa chỗ mình nhớ và bỏ sót chỗ mình
không nhớ — một lý do nữa để phép đo, chứ không phải trí nhớ, là thứ quyết định.

Đây **đúng** là nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong` hiện thành số: quyền ghi còn sống sau khi
việc đã xong, và **không trường nào trong tệp lease nói ra điều đó** — nên công cụ báo 5 là công cụ
**đúng**, không phải công cụ hỏng. `ai-dang-giu` trả lời *"ai đang giữ"*, không trả lời *"ai đang
dùng"*; hai câu hỏi khác nhau và kho mới chỉ có lệnh cho câu thứ nhất.

**Ba đường xử, người giữ kho chọn — đặc tả không tự quyết:**

| | đường | giá |
|---|---|---|
| **(a)** | **Cấp ngay**, lease khai từng hiện vật land, và khai thẳng rằng đây là **CHẤP NHẬN RỦI RO CÒN LẠI**, không phải rủi ro đã đo bằng không | Rẻ nhất, có vết. Rủi ro **KHÔNG đo được**: không bằng chứng nào nói thẩm quyền ghi đã chấm dứt |
| **(b)** | Chờ hết hạn tự nhiên | Muộn nhất `2026-08-24T08:25:00Z`. Đây là bằng chứng chấm dứt **DUY NHẤT** kho có |
| **(c)** | Thu hồi 5 lease trước | Chưa có đường thu hồi (chính là nợ `AG-T0-01B`) ⇒ phải làm tay |

**Đặc tả KHÔNG đề xuất đường nào — và câu này thay một câu SAI của bản đầu.**

Bản đầu đề xuất `(a)` với lý lẽ *"(b) trả 22 giờ cho một rủi ro **đã đo được là bằng không**"*.
Cross-review lượt 1 của PR #288 (`P1`, codex) bác đúng chỗ đó, và bác đúng:

- Thứ đã đo là **"việc đã LAND"** — Issue đóng, hiện vật trên master, 0 nhánh chưa-merge chạm tệp.
- Thứ được KHAI là **"rủi ro bằng không"**, tức *thẩm quyền ghi đã chấm dứt*.
- **Hai mệnh đề khác nhau.** Land chứng minh việc xong; nó không chứng minh không phiên nào còn hành
  động được dưới `lease_id` ấy. Và **không có bằng chứng chấm dứt bền nào tồn tại** — đó chính là nợ
  `AG-T0-01B`, mà chính tệp này nêu ở hai chỗ khác (§trên: *"quyền ghi còn sống sau khi việc đã
  xong"*; `chua_do_duoc#10`: *"chưa mở từng packet"*).

Nên bản đầu là **hình dạng A — lời khai rộng hơn phép đo — nằm trong chính artefact viết ra để chống
nó**, và nó là căn cứ mà một quyết định cấp lease đã dựa vào. Xem §`bo_dem_A` ngay dưới.

Cách nói đúng: `(a)` **hợp lệ** nếu người giữ kho **chấp nhận rủi ro còn lại** và ghi thẳng như vậy —
đó là thẩm quyền của chủ kho (`§2`). Cái không được phép là gọi việc chấp nhận ấy là *"đã đo bằng
không"*. Chỉ `(b)` mới cho bằng chứng chấm dứt.

### `bo_dem_A` — **A = 8. `S2` ĐÃ KÊU.**

Biểu hiện vừa nêu là **hình dạng A**. `#269` chốt rõ: *"Phiên điều phối **không tự tăng** — người giữ
kho quyết."* Đã trình, và người giữ kho quyết **in-session 23-08-2026: TĂNG lên 8**.

```
A = 7  ->  A = 8        B = 2   C = 1   D = 3   E = 4   F = 2
```

**`S2` là điều kiện DỪNG đã đăng ký, và nó vừa kêu lần đầu tiên.** Ghi thẳng ra đây thay vì để nó
trôi, vì đây là lần đầu một chốt dừng của bộ đếm hình dạng thực sự kích hoạt trong kho.

Hai dữ kiện làm nên quyết định, cả hai đo được, và cả hai khác lần ở `#270` (nơi người giữ kho chọn
GIỮ 7):

| | `#270` | lần này |
|---|---|---|
| ai bắt | phiên **tự** phát hiện | **reviewer ngoài** (codex, PR #288) |
| câu sai chống đỡ gì | không chống đỡ thẩm quyền nào; bản vá là một chữ | **chống đỡ một quyết định CẤP QUYỀN GHI** |

Ý nghĩa của `S2`, đọc từ `#269`: bộ đếm tồn tại *"để buộc hỏi «có nên làm việc này nữa không»"* —
tức nó dừng để **XÉT LẠI KIẾN TRÚC**, không phải để hỏi *"vá thế nào"*. `CLAUDE.md` nói cùng điều:
*"cùng một hình dạng lặp ba lần trở lên thì câu hỏi đúng là «có nên làm việc này không»"*.

**Câu hỏi kiến trúc mà `S2` đang đặt ra, nêu thẳng cho phiên sau:** hình dạng lặp lại ở đây không
phải *"một câu viết ẩu"* mà là **một phiên tự viết đặc tả rồi tự thẩm định lời khai của chính nó**.
Ba biểu hiện gần nhất — `#270`, `P1` của PR #288, và cả `P2` — đều sinh ra trong artefact do **một
phiên** vừa soạn vừa tự kiểm. `ADR-0046` §3 đã nêu đúng hướng chữa (*cắt phiên ở biên packet*) nhưng
nó mới `Proposed`, và §3 chỉ cắt giữa **soạn spec** và **thi công** — **không** cắt giữa *soạn* và
*tự thẩm định*. Đó là khoảng trống mà ba biểu hiện này rơi vào.

**Trạng thái thi công dưới `S2`:** xem `dieu_kien_dung` bên dưới. Người giữ kho đã cho biết lập
trường trên trục `(a)`/`(b)` (chấp nhận rủi ro còn lại — xem §trên), nhưng lập trường ấy trả lời
*"nếu đi tiếp thì đi đường nào"*, **không** tự nó trả lời *"có đi tiếp không"*. Hai câu khác nhau, và
`S2` hỏi câu thứ hai. Phiên soạn tệp này **không tự trả lời** câu ấy.

---

## `base_sha`

r2 khai `CHUA_XAC_DINH` **có chủ đích**. Nay xác định được:

```
base_sha := 5561b6b497989447f9185b26abb1bba154564967
```

**Vẫn phải đo lại lúc ký.** master đã đi **27 commit** trong khoảng 08:29Z→10:01Z của chính phiên này
(`7707832f` → `5561b6b4`), tức nhanh hơn một commit mỗi bốn phút. Nếu master đi tiếp trước lúc ký thì
`base_sha` phải là HEAD lúc ấy, và **§`nghiem_thu` phải đo lại** — bảng dưới neo vào `5561b6b4`.

---

## Ba thứ r2 dặn đo lại — cộng một thứ thứ tư

| thứ | r2 (`00d4b3d7`) | r3 (`5561b6b4`) | đổi? |
|---|---|---|---|
| số ca suite | 88 | **97** | **CÓ** — `#244` thêm 9 ca (`t89`–`t97`) |
| `t33` ở dòng | 1312 | 1312 | không |
| `t73` ở dòng | 2649 | 2649 | không |
| `t70` ở dòng | 2604 | 2604 | không |
| `main()` ở dòng | **2904** | **3123** | CÓ |
| mệnh đề nền ở dòng | 189 | **196** | CÓ |
| `numstat` bản vá | 16 | **16** | không |
| **tên ca đề xuất** | `t89` | **`t98`** | **CÓ — xem dưới** |
| `ops/cai_actionlint.sh` | `70af202a620daff5` | `70af202a620daff5` · **0** lần nhắc `shellcheck` | không |

### Thứ tư: **`t89` ĐÃ BỊ CHIẾM**

r2 chọn `t89` vì lúc ấy số hiệu cao nhất là `t88`. `#244` đã thêm `t89`–`t97`, nên số hiệu cao nhất
nay là **`t97`**, và tên r2 đề xuất **trùng một ca đang tồn tại**.

Đây đúng loại lỗi r2 tự cảnh báo ở một chỗ khác (*"`t74` ĐÃ CÓ"*) nhưng không lường được cho chính
mình — vì nó giả định write set đứng yên trong lúc chờ. **Ca đổi tên thành `t98`**, thân giữ nguyên
từng chữ trừ số hiệu và con số trong docstring (`88/88` → `97/97`).

---

## `ca_va_M3` — CHÉP NGUYÊN VĂN, bản đã chạy trên `5561b6b4`

Thay trọn khối `ca_va_M3` của r2. Chèn ngay **trước** `def main() -> int:`:

```python
@ca
def t98_truc_phan_biet_la_NEN_chu_khong_phai_TEN_TEP():
    """Cặp với `t73`: CÙNG tuple, ĐỔI mỗi nền, phải ra kết quả NGƯỢC nhau.

    `t73` một mình chỉ chứng minh "posix thì không bỏ qua". Nó KHÔNG chứng minh quyết
    định ấy tra theo NỀN: thay mệnh đề nền bằng phân biệt theo TÊN TỆP vẫn cho 97/97,
    rc=0 trên toàn chân Ubuntu (đo 23-08-2026). Ca này khoá đúng cái trục ấy.

    Đi qua `main()`, KHÔNG gọi thẳng `_ly_do_bo_qua_workflow` — tuân `r4/Q8`.
    """
    def bo(): raise BoQuaNen(WORKFLOW_DANG, "dang")
    rc, out = _chay_main_meta(bo, "nt")
    bang(rc == 0 and "bỏ qua=1" in out,
         f"cùng tuple mà nền nt KHÔNG bỏ qua: rc={rc}, {out!r}")
```

`numstat` đo được: **16** dòng thêm — không đổi so với r2.

---

## `nghiem_thu` — `W11`–`W13` THAY SỐ, giữ nguyên ý

Ma trận 8 ô, chạy trên `git worktree` rời tại `5561b6b4`, `X1`/`X2` như r2 định nghĩa:

| bản | rc | tổng kết | ĐỎ |
|---|---|---|---|
| BASE | 0 | `97/97 đạt; đã chạy=97, bỏ qua=0` | — |
| `X1` | 1 | `88/89 đạt; đã chạy=89, bỏ qua=8` | `t73` |
| **`X2`** | **0** | **`97/97 đạt; đã chạy=97, bỏ qua=0`** | **KHÔNG CA NÀO** |
| VÁ | 0 | `98/98 đạt; đã chạy=98, bỏ qua=0` | — |
| VÁ+`X1` | 1 | `89/90 đạt; đã chạy=90, bỏ qua=8` | `t73` |
| VÁ+`X2` | 1 | `97/98 đạt; đã chạy=98, bỏ qua=0` | **`t98`** |
| VÁ+`X1` · gỡ `t70` | 1 | `88/89 đạt; đã chạy=89, bỏ qua=8` | `t73` |
| VÁ+`X2` · gỡ `t70` | 1 | `96/97 đạt; đã chạy=97, bỏ qua=0` | **`t98`** |

**Phát hiện đáng ghi: lỗ `X2` SỐNG SÓT qua `#244`.** Packet ấy thêm 9 ca vào đúng tệp này, trong đó
`t95`/`t96`/`t97` đều sinh ra để bịt fail-open, và **không ca nào** chạm trục nền. `X2` vẫn cho
`97/97 rc=0`. Nên `N1` không phải nợ cũ đã tự khép — nó còn nguyên, và nay có thêm bằng chứng rằng
một lượt packet khác đi qua cùng vùng mã cũng không tình cờ đóng nó.

| # | tiêu chí | phép đo làm nó ĐỎ (thay số của r2) |
|---|---|---|
| **W11** | `X2` bị bắt | VÁ ⇒ `98/98`, `rc=0` · VÁ+`X2` ⇒ `97/98`, `rc=1`, ĐỎ `t98_truc_phan_biet_la_NEN_chu_khong_phai_TEN_TEP` · **đối chứng** `X2` không kèm VÁ ⇒ `97/97`, `rc=0` XANH |
| **W12** | `X1` vẫn bị bắt, VÁ không làm yếu `t73` | VÁ+`X1` ⇒ `89/90`, `rc=1`, ĐỎ `t73` |
| **W13** | Răng ở DÂY NỐI, không ở thân hàm (`r4/Q8`) | Gỡ `@ca` của `t70` rồi áp lại: `+X1` ⇒ `88/89`, `rc=1`, ĐỎ `t73` · `+X2` ⇒ `96/97`, `rc=1`, ĐỎ `t98` |
| **W14** | `M4` docstring | **KHÔNG ĐỔI** — vẫn KHÔNG CÓ CỔNG, xem r2/`chua_do_duoc`#4 |

`B1`–`B5` của r1 và ràng buộc chéo `B1`∧`B4` **giữ nguyên**. Lệch bất kỳ số nào ở `W11`–`W13` ⇒
**DỪNG**, báo số đo được, **không sửa ca cho vừa số**.

---

## `ai thi công` — ADR-0046 §3 đổi câu trả lời của r2

ADR-0046 (`Proposed` 22-08-2026, **chưa `Accepted`** — căn cứ của nó còn nằm trong comment GitHub,
chưa đóng băng thành biên nhận) khai ở §3:

> *"**Cắt phiên ở BIÊN PACKET**, tức khi chuyển từ soạn spec sang thi công. Người thi hành **không**
> nên là phiên đã viết đặc tả."*

r1/r2 khai `executor: claude` — đó là **nhà cung cấp**, không phải **phiên**, nên không mâu thuẫn.
r3 làm rõ thêm một tầng:

- `executor` vẫn là **`claude`**, nhưng phải là **PHIÊN MỚI**, không phải phiên đã soạn r1/r2/r3;
- lý do không chỉ là kỷ luật: phiên này đã tự tay viết và chạy ca `t98`, nên nó là bên **kém độc lập
  nhất** để nghiệm thu chính ca ấy;
- `reviewer` vẫn **`codex`**, và theo ADR-0046 §2 phải là **reviewer mới mỗi lượt**, sandbox riêng.

Điều này **thay** câu của r2 rằng *"executor `claude` sẽ chép"* — vẫn chép, nhưng chép ở một phiên
khác. Rủi ro cross-provider mỏng mà r2 khai **vẫn còn nguyên** và không được coi là đã xử.

---

## `dieu_kien_dung` — thay bảng của r2 ở ĐÚNG một dòng

Bảng `S1`–`S7` của r2 giữ nguyên, cộng `S8` mà r3 thêm. **Đổi trạng thái hai dòng:**

| # | điều kiện | trạng thái, đo 23-08-2026 |
|---|---|---|
| **S1** | `#275` chưa merge ⇒ không cấp lease | **ĐÃ TẮT** — merged `09:21:59Z`, `#244` closed `completed` `09:45:30Z` |
| **S2** | Bộ đếm hình dạng `A` chạm **8** | **ĐANG KÊU** — người giữ kho tăng 7 → 8 in-session 23-08. Xem §`bo_dem_A` |
| S3 | `E` chạm 5 | `E = 4`, chưa kêu |
| S4 | `numstat` vượt 120 | chưa đo trên head thi công |
| S5 | số nào của `W11`–`W13` lệch bảng r3 | chưa chạy |
| S6 | cần đường dẫn thứ ba | `write_set` đúng 2 |
| S7 | lượt vá cần đụng `.github/workflows/**` | ⇒ Issue độ phủ, không phải packet này |
| S8 | master đã đi tiếp so `base_sha` mà chưa đo lại `nghiem_thu` | `base_sha` = `5561b6b4` = master lúc đo |

**`S2` đang kêu, và một chốt dừng đang kêu thì THI CÔNG KHÔNG ĐƯỢC BẮT ĐẦU** cho tới khi người giữ
kho trả lời câu mà `S2` đặt ra (*"có nên làm việc này nữa không"* — xem §`bo_dem_A`).

Ghi cho rõ vì ở đây có **hai trục dễ lẫn**, và lẫn chúng là cách một chốt dừng bị vô hiệu trong im
lặng:

- **Trục ĐƯỜNG ĐI** — `(a)` hay `(b)` cho năm lease đã tiêu. Người giữ kho đã chốt: **`(a)`, chấp
  nhận rủi ro còn lại, có ghi**. Đã ghi vào lease bằng đúng chữ ấy.
- **Trục CÓ ĐI KHÔNG** — `S2`. **Chưa có câu trả lời.**

Lập trường trên trục thứ nhất **không** tự nó trả lời trục thứ hai. Lease đã soạn xong và qua cổng
(`rc=0`), nhưng **chưa đẩy**, và không được đẩy tới khi trục thứ hai có câu trả lời.

## Neo — băm đo trên `master = 5561b6b4`, 10:0xZ 23-08-2026

| tệp | sha256 (16 đầu) | so r2 |
|---|---|---|
| `ops/lease_publish_test.py` | **`714e3eb09e033891`** | **ĐỔI** (`ab5cc14016bd189a`) — `#244` thêm 219 dòng |
| `ops/cai_actionlint.sh` | `70af202a620daff5` | không đổi |
| `ops/specs/t33-doi-shellcheck.md` (r1) | `1405d390ca937672` | không đổi |
| `ops/specs/LEASE-DANG-WINDOWS-r4.md` | `11972e8ce5d54330` | không đổi |
| `docs/PROTOCOL_DA_PHIEN.md` | **`2515d808edc881f3`** | **ĐỔI** (`9226c06f7be0be79`) — PR #281, §10 bookkeeping |
| `docs/adr/0043-…` | `ec3b2c3266ff5ab0` | — |
| `docs/adr/0044-…` | `8fa0bf21f0efdd2f` | — |

`ops/specs/t33-doi-shellcheck-r2.md` **chưa có trên master** (`git show` trả rỗng); nó sống trên nhánh
`claude/spec-freeze-n3-n1-269-gw47hw`, băm `b9620d17b86f503b`. Lease phải neo **cả r2 lẫn r3** trong
`spec_ke_thua`, và cả hai phải land trước hoặc cùng lúc với lease.

**Nguồn có thẩm quyền là TỆP CÓ BĂM trong kho.** Bản chiếu lên Issue/comment chỉ là bản chiếu.

---

## `chua_do_duoc` — bổ sung cho r2

Giữ trọn 9 mục của r2 (mục 6 nay **đã đo**: `numstat` = 16 trên base thật). Thêm:

10. **KHÔNG CÓ CÁCH NÀO ĐO ĐƯỢC RẰNG MỘT LEASE ĐÃ CHẤM DỨT — trừ hết hạn.** Đây là mục quan trọng
    nhất của danh sách này, và bản đầu của r3 khai nó quá nhẹ (chỉ nói *"chưa kiểm từng cái"*), rồi
    ở §trên lại rút ra kết luận *"rủi ro đã đo được là bằng không"*. Cross-review `P1` bác đúng chỗ ấy.
    Nói cho chật: thứ đo được là **việc đã LAND** — Issue đóng, hiện vật trên master, 0 nhánh
    chưa-merge chạm tệp. Thứ **KHÔNG** đo được là **thẩm quyền ghi đã chấm dứt**: không trường nào
    trong tệp lease mang trạng thái `đã tiêu`/`đã thu hồi`, không sổ nào ghi, và `ai-dang-giu` cố ý
    trả lời *"ai đang GIỮ"* chứ không *"ai đang DÙNG"*. Nợ `AG-T0-01B` **chính là** khoảng trống này.
    Hệ quả cho người cấp: đường (a) là **chấp nhận rủi ro còn lại**, phải ghi đúng bằng chữ ấy trong
    lease; và phần khai hiện vật từng lease **phải do người cấp tự đo**, không chép từ đây.
11. **Hành vi trên `windows-latest` thật vẫn CHƯA ĐO** — cả 8 ô của r3 vẫn chỉ chạy trên Linux, y hệt
    r2. `B5` của r1 là chỗ đo, và đường chắc chắn là `workflow_dispatch` trên đúng ref (gắn nhãn
    `windows` KHÔNG đủ).
12. **`M1`/`M2` vẫn chưa có số kích thước nào.** Trần **120** của r2 giữ nguyên và vẫn là **ước lượng
    có neo**, không phải số đo.
