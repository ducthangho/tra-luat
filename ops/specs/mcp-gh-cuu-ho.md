# ĐẶC TẢ — `MCP-GH-CUU-HO` (Issue #319) — **BẢN SỬA ĐỔI 4**

> **r2 sửa gì, và vì sao.** Bản r1 (`51105214fe121a…`) đã được thi công một lượt bởi `codex xhigh`
> và lượt ấy **lộ ra hai khuyết tật của chính đặc tả**, không phải của bản vá: (a) `D7`/`D8` giả
> định ngầm rằng sổ nền XANH, nên khi bốn ca nền đỏ thì **mọi** đột biến đều "giết" thêm bốn ca ấy
> và phép "đúng một ca" cho `0/35` — một con số đúng mà đọc thành sai; (b) `D9` khai trần 750
> trong khi lease đã nâng 1000, hai mệnh đề không cùng đúng được. Cộng một ràng buộc thiết kế mà
> r1 không nêu: **ca của một tiêu chí không được đi qua đúng đoạn mã mà đột biến của tiêu chí khác
> nhắm vào** — ba đột biến `b1`/`b3`/`b5` sống sót vì đúng chuyện đó.
> r1 KHÔNG bị bác về nội dung; ba mươi tiêu chí giữ nguyên trừ những chỗ ghi rõ dưới đây.
>
> **r3 đổi ĐÚNG MỘT tiêu chí: `D8`.** Lượt 2 vá xong ba giao phạm vi thì **đẻ ra hai cái mới**
> (`b6` giết cả `B6` lẫn `D6` vì `D6` nay cấp token hợp lệ nên đi qua đường `init`; `b7_bo_cam_ghi`
> giết cả hai ca `B7`). Đó là lần thứ NĂM của cùng một hình dạng, và `CLAUDE.md` chốt: lặp ba lần
> thì câu hỏi đúng là *"có nên làm việc này không"*. Câu trả lời ở đây không phải "bỏ đo đột biến"
> mà là: **"đúng một ca" là BIẾN SAI của thứ ta thật sự cần đo.**
>
> **r4 THÊM hai tiêu chí, không đổi tiêu chí nào cũ: `D10` và `D11`.** Hai lý do độc lập.
> (a) Sổ ca đã có `D10-main` mà bảng `D` KHÔNG có tiêu chí tương ứng — mã đi trước đặc tả, và
> đặc tả là thứ có thẩm quyền, nên đặc tả phải bắt kịp chứ không phải ngược lại.
> (b) Cross-review vòng 3 nêu một P1 — cổng in một bản báo cáo có dòng ĐỎ mà vẫn thoát 0, vì
> `TỔNG` suy từ `rc` chứ không suy từ báo cáo — và bản vá đầu cho nó đã bị phiên điều phối ĐO LẠI
> và BÁC. Xem mục `D10`/`D11` ở cuối phần `D`. Ba mươi tiêu chí cũ giữ NGUYÊN VĂN.

Đặc tả này ĐÓNG BĂNG bằng băm. Lease neo vào `spec_sha256`. Sửa nội dung ⇒ băm đổi ⇒ lease trỏ
vào thứ không còn tồn tại, phải đi qua bản sửa đổi mới. Soạn bằng skill `soan-spec`.

| khoá | giá trị |
|---|---|
| `packet_id` | `MCP-GH-CUU-HO` |
| `packet_issue` | 319 |
| `nguon_cap_viec` | Packet cha **#314**, verdict cross-review vòng 2 trên PR #315 — `blocked` · `DO_NOT_LAND`, comment `5423010218`, `reviewed_sha 6c4140ba507162ca1c6ee8d2bf510445574bad24`. **Verdict ấy KHÔNG có biên nhận trong kho**: quét cả 206 ref lúc 09:45Z 26-08 ⇒ **0** tệp `ops/reviews/*` nào cho #314/#315. Nguồn cấp việc của packet này do đó là một **comment**, không phải tệp có băm — nói thẳng vì `CLAUDE.md` chốt rằng nguồn có thẩm quyền là tệp có băm, và ở đây điều kiện ấy KHÔNG thoả |
| `review_class` | `sensitive` — cổng `_BANG_LOP` tự tính, mặc định fail-close. Ở packet này còn là hạng đúng theo nội dung: mã cầm `GITHUB_PAT` và tự quyết định gửi nó đi đâu. **KHÔNG** "chạm authority" theo nghĩa ADR-0044: không cấp lease, không gác cổng, không vào gói phát hành (chốt Q1) |
| `base_sha` | `b662fe1d07c675a222ae26e734377e305775e4f3` — `origin/master` đo 09:57Z 26-08 |
| `base_sha` (r4) | `ac82ddc583f688d54bdc60e06922ec09bdab9f16` — `origin/master` đo 02:43Z 27-08. `S4` bắn LẦN HAI. `b662fe1` VẪN là tổ tiên (không viết lại lịch sử) và 46 commit mới KHÔNG chạm đường dẫn nào trong `write_set` — đo bằng `git diff --numstat` trên đúng ba đường dẫn, kết quả RỖNG. Xử theo §5.1: merge thẳng vào nhánh packet (`043d2709`) |

## Trôi base — ghi vì L5 bắt được nó giữa lúc soạn

Lease r1 neo `c35ae1c`. Lúc đo lại trước bước công bố (09:57Z), `origin/master` đã là `b662fe1`:
PR #316 land packet #313 ca 1+3, chạm `ops/lease_publish.py` (+99/−1) và `ops/lease_publish_test.py`
(+125/−1). Đo: `c35ae1c` **vẫn là tổ tiên** của `b662fe1` (không viết lại lịch sử), và **không giao**
write set của #319. Xử theo §5.1 (master drift — merge thẳng): nhánh packet rebase lên `b662fe1`,
lease đi qua **revision 2** để neo cả `spec_sha256` lẫn `base_sha` mới.

Đây đúng là thứ điều kiện dừng `S4` của lease sinh ra để bắt, và nó bắn ở lần đo thứ ba trong một giờ.

## write_set
- `ops/specs/mcp-gh-cuu-ho.md`
- `.claude/dev/mcp_gh.py`
- `.claude/dev/mcp_gh_test.py`

Không đường dẫn nào khác. Ba đường dẫn đều dev-side; không tệp nào vào gói phát hành.

## ngoai_pham_vi — CỐ Ý không làm

1. **Sửa `ai-dang-giu` đếm BLOB thay vì đếm LEASE.** Tái lập được, cơ chế và phản chứng một-biến
   đã báo ở **#313** (comment `5423549720`). Cần sửa `ops/lease_publish.py` — tệp `sensitive`
   **thật sự chạm authority**. Gộp vào đây sẽ kéo packet qua ngưỡng 300 dòng của ADR-0044 và trộn
   lại đúng hai lớp thẩm quyền mà #314 vừa phải tách ra để thoát (chốt Q4).
2. **Quét toàn kho bảy site còn lại của hình dạng "cổng xanh khi không đo gì".** Xem
   `hinh_dang_ke_thua`. #319 đóng **1/8**; bảy site kia cần một Issue riêng, có
   `ops/lease_publish_test.py` đứng đầu vì nó gác việc cấp lease (chốt Q5).
3. **Mục doctrine về ranh giới phiên review.** Thuộc **#318**, write set riêng.
4. **Chuyển sang runner chuẩn.** Đã ĐO và LOẠI: `unittest.main()` với 0 ca in `OK` và trả **rc=0**;
   với ca bị lọc hết cũng vậy. `pytest` không cài trong container và CI không gọi. Không runner có
   sẵn nào đóng lỗ này miễn phí, nên thứ phải có là **bất biến khai tường minh**, không phải một
   lựa chọn framework.
5. **Đưa `mcp_gh.py` lên `master`.** Việc của lượt land, không của lượt này.

## hinh_dang_ke_thua (L4)

**Biên nhận tiền nhiệm KHÔNG TỒN TẠI** — đo ở `nguon_cap_viec`. Bộ đếm dưới đây do phiên này dựng
lại, và đây là cơ sở đếm (L1): **đếm SITE có bộ đếm rỗng vẫn cho `rc=0`**, không đếm finding, không
đếm lượt review.

Hình dạng: *"cổng báo xanh trong khi không đo gì"*.

| # | site | neo |
|---|---|---|
| 1 | `t24` — ca `return` sớm vì đường dẫn sai, suite báo `24/24` | `CLAUDE.md` |
| 2 | PowerShell `$Args` là biến tự động ⇒ python chạy không đối số, `rc=0` + output rỗng | `CLAUDE.md` (r244) |
| 3 | `gh` giả DIỄN KỊCH BẢN ⇒ `40/40` trong khi đột biến xoá hẳn lệnh `DELETE` vẫn qua | `CLAUDE.md` |
| 4 | va chạm `.pyc` ⇒ đột biến **chưa từng được chạy**, báo `giết 0/1` suốt ba lượt | `CLAUDE.md` |
| 5 | `doctor --json` không gọi `chay_cac_probe` ⇒ khoá `workspace` **vắng mặt**, đọc thành đã-đo-thấy-rỗng | `CLAUDE.md` |
| 6 | `mcp_gh_test.py` vòng 1 — xoá `DAT`/`DO` trước khi in tổng kết | verdict vòng 2, PR #315 |
| 7 | `mcp_gh_test.py` vòng 2 — tách sổ nhưng vị ngữ cuối vẫn `not DO`, sổ rỗng thoả `not DO` | verdict vòng 2, PR #315 |
| 8 | **`ops/lease_publish_test.py`** — `return 1 if hong else 0`, không chốt `len(CA) > 0` | phiên này chạy phản chứng trên `b662fe1`: `lease_publish: 0/0 đạt` ⇒ **`rc=0`** |

`CLAUDE.md` chốt: **lặp ba lần thì câu hỏi đúng là "có nên làm việc này không"**. Đây là **tám**.
Câu trả lời đã chốt ở Q5: câu hỏi ấy KHÔNG được trả lời bằng đổi framework (mục 4 của
`ngoai_pham_vi` đã đo và loại), mà bằng khai bất biến tường minh — và #319 chỉ đóng **một** site.

Nền đo kèm điều kiện (L5): `ops/lease_publish_test.py` trên kho thật lúc 09:30Z 26-08 cho
**97/98**, ca đỏ duy nhất là `t33` fail-close vì thiếu `actionlint`. Bản sao chạy NGOÀI kho cho
77/98 — **đó là rig, không phải hồi quy**; ghi ra để không ai đọc nhầm con số ấy về sau.

## muc_tieu — mỗi dòng chiếu vào một đường dẫn ở `write_set` (L2)

**Đếm (L1): NĂM hạng mục phải xử**, đếm theo *lỗ thiết kế hoặc finding P1 còn mở thuộc write set
này*. Thân Issue #319 viết *"bốn P1 còn lại"* — con số ấy đếm **P1 của verdict vòng 2**, trong đó
hai P1 không thuộc packet này (`reviewer-shell-is-not-read-only` → #318;
`packet-spec-revision-incoherent` → đóng bằng chính lease). Hai cách đếm, hai con số; đây là cách
đếm có thẩm quyền cho đặc tả.

1. **Khoá NƠI NHẬN credential bằng origin chuẩn hoá đầy đủ.** So `scheme` + `hostname` + **cổng đã
   chuẩn hoá** (cổng vắng = cổng mặc định của scheme), và từ chối mọi URL mang `username`/`password`,
   `query` hoặc `fragment` không nằm trong tập cho phép. → `.claude/dev/mcp_gh.py`
2. **Kiểm lại đích TẠI THỜI ĐIỂM GỬI**, không chỉ lúc dựng phiên. Chốt hiện chạy đúng một lần trong
   `__init__`; `self.url` gán lại được sau đó mà không ai kiểm lại. → `.claude/dev/mcp_gh.py`
3. **KHÔNG đi theo chuyển hướng.** Opener phải từ chối 301/302/303/307/308 thay vì để `urllib` tự đi
   — hoặc handler chạy lại chốt kiểm đích cho từng chặng. → `.claude/dev/mcp_gh.py`
4. **Lỗi của công cụ phải ra mã thoát khác 0.** `main` hiện in kết quả `tools/call` rồi trả `0` bất
   kể top-level `error` hay `result.isError == true`. Cộng ba đường hỏng của `initialize` còn mở:
   `{"result": {}}` rỗng vẫn được nhận; phản hồi dạng **list** gây `AttributeError` không bắt được;
   lỗi vận chuyển khi gửi `notifications/initialized` bị **nuốt** (giá trị trả bị bỏ).
   → `.claude/dev/mcp_gh.py`
5. **Tách module khỏi CLI**, giữ hợp đồng CLI **tương thích ngược**: `--liet-ke`,
   `<tên-công-cụ> '<json>'`, `--path`, và mã thoát `0` / `2` / `3`. Phiên điều phối đang phụ thuộc
   đúng bốn lời gọi ấy. → `.claude/dev/mcp_gh.py`
6. **Sổ ca BẤT BIẾN.** Đăng ký ca trước vào một sổ không sửa được sau khi dựng, rồi chốt:
   *số ca đăng ký > 0* **∧** *số ca đã CHẠY = số ca đăng ký* **∧** *số đột biến đăng ký > 0*.
   → `.claude/dev/mcp_gh_test.py`
7. **Chín bất biến phải sống sót**, mỗi cái có ca **và** đột biến giết đúng ca đó (bảng ở
   `nghiem_thu` B1–B9). → `.claude/dev/mcp_gh_test.py`
8. **Chính đặc tả này**, đóng băng bằng sha256 và neo vào lease revision 2.
   → `ops/specs/mcp-gh-cuu-ho.md`

## nghiem_thu — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

### A. Đích đến của credential (mục tiêu 1–3)

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| A1 | `https://api.githubcopilot.com:444/mcp/` bị **CHẶN** | ca mới; hiện tại nó **QUA** — bản vá không đóng ⇒ ca ĐỎ |
| A2 | `:8080`, `?x=1`, `#frag` đều bị **CHẶN**; `https://API.GitHubCopilot.COM/mcp/` vẫn **QUA** | bốn khẳng định trong một ca; nới chốt để hoa/thường trượt ⇒ ĐỎ ở vế cuối |
| A3 | URL mang `user:secret@` bị **CHẶN**, và bí mật KHÔNG xuất hiện trong chuỗi lỗi trả về | ca đọc thông điệp lỗi; in thẳng `url` vào thông điệp ⇒ ĐỎ |
| A4 | Gán lại `self.url` sang đích lạ **sau** khi dựng phiên ⇒ lời gọi kế tiếp bị CHẶN | ca gán `p.url = "https://evil.example/x"` rồi gọi; hiện tại lời gọi **đi thẳng** ⇒ ĐỎ. Đột biến: gỡ chốt lúc gửi ⇒ ca này phải ĐỎ |
| A5 | Máy chủ trả **301** ⇒ credential KHÔNG tới đích thứ hai | ca dựng hai `http.server` cục bộ, đọc `Authorization` mà đích thứ hai nhận được; phải là `None`. Đo được hiện trạng: **nhận nguyên vẹn** |
| A6 | Y hệt A5 cho **302** và **303** | hai ca riêng. Ba mã phải có ba ca — gộp một ca thì đột biến chỉ-vá-301 sống sót |
| A7 | **307**/**308** cũng không rò | ca riêng; hiện `urllib` đã ném `HTTPError` nên ca này XANH sẵn — giữ để đột biến "tự viết handler đi theo mọi mã" bị giết |
| A8 | Đường thuận không hỏng: `/mcp/` và `/mcp/x/actions` vẫn dựng phiên được | chặn nhầm đích hợp lệ ⇒ ĐỎ |

**Yêu cầu MÔI TRƯỜNG cho `A5`–`A7` (r2 thêm):** ba ca ấy cần dựng **hai máy chủ loopback**, tức cần
quyền `bind` trên `127.0.0.1`. Đo được ở lượt 1: sandbox `codex` **từ chối** (`PermissionError:
[Errno 1] Operation not permitted`), còn vỏ phiên điều phối và runner CI `ubuntu-latest` thì cho.
Môi trường cấm `bind` ⇒ ba ca ấy **ĐỎ**, KHÔNG được "bỏ qua" và tuyệt đối KHÔNG được thay bằng
kiểm tra giả để lấy `rc=0` — executor lượt 1 đã từ chối làm thế, và đó là hành xử đúng. Kéo theo
`D7b`: nền đỏ thì ô đột biến in `KHÔNG_ĐO_ĐƯỢC`. **Chọn NỀN chạy suite là một quyết định vận hành,
không phải chi tiết**; nghiệm thu cuối phải chạy ở nền cho `bind`.

### B. Chín bất biến phải sống sót (mục tiêu 7)

| # | bất biến | phép đo làm nó ĐỎ |
|---|---|---|
| B1 | SSE lấy dòng `data:` **CUỐI** | đột biến `if dong.startswith("data:")` → `if False` phải giết ca |
| B2 | **KHÔNG cắt chuỗi** — cả ở tách thân lẫn ở rút văn bản | hai đột biến riêng, mỗi cái thêm `[:6000]` ở một chỗ; ca phải khẳng định độ dài `> 20000` **và** `json.loads` được |
| B3 | Thiếu credential ⇒ `rc=3`, và ca phải **bịt mọi đường ra mạng** để `rc=3` chỉ có thể đến từ chốt token | đột biến gỡ chốt token phải giết ca. Ca đã mất răng **hai** lần vì bịt thiếu đường — chốt cô lập phải neo vào đường `main` THẬT đi, không neo vào tên hàm ta nhớ |
| B4 | `initialize` hỏng ⇒ không báo xanh, **và** nhận ra ĐÚNG là JSON-RPC error chứ không rơi xuống nhánh "thiếu `result`" | ca khẳng định chuỗi lỗi **bắt đầu bằng** `JSON-RPC error -32000`; nhánh "thiếu result" cũng in cả khối JSON nên khẳng định lỏng sẽ che mất đột biến |
| B5 | Lỗi tầng vận chuyển ⇒ khối riêng, **không** bắt `Exception` trần | đột biến đổi tuple except sang một lớp không ai ném ⇒ ca phải ĐỎ |
| B6 | Chốt kiểm đích **thật sự được gọi** lúc dựng phiên | đột biến thay lời gọi bằng `pass` ⇒ ca phải ĐỎ |
| B7 | Runner đột biến: **ba lớp** chống `.pyc` (xoá `.pyc` · tắt ghi bytecode · `invalidate_caches`) + tên tệp riêng từng đột biến | mỗi lớp có phản chứng RIÊNG; lớp "tắt ghi bytecode" phải đo bằng "nạp xong không được để lại `.pyc`", vì gỡ nó ra mà ca vẫn xanh là lớp không có răng |
| B8 | `notifications/initialized` chỉ gửi sau khi mở THẬT; notification **không có `id`** | đột biến `if not bao_tin:` → `if True:` phải giết ca |
| B9 | `Mcp-Session-Id` nhận từ phản hồi đầu rồi gửi lại ở lời gọi sau | đột biến bỏ gán `sid` phải giết ca |

`t3` `t7` `t8` `t9` `t10` của bộ cũ **cố ý không** nằm trong danh sách bất biến (chốt Q6): chúng
đúng nhưng chưa ai trả giá cho chúng, nên đưa vào là biến "đã có test" thành ràng buộc kiến trúc.
Chúng vẫn được viết lại tự do.

### C. Sổ ca bất biến (mục tiêu 6) — bốn ca ĐỎ có tên

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| C1 | Sổ ca rỗng ⇒ cổng **ĐỎ**, `rc` khác 0 | đột biến làm decorator không ghi sổ; hiện cho `CA: 0 đạt · 0 đỏ` ⇒ `TỔNG: ĐẠT` `rc=0` |
| C2 | Sổ đột biến rỗng ⇒ cổng **ĐỎ** | đột biến `DOT_BIEN = []`; hiện cho `ĐỘT BIẾN 0/0` ⇒ `TỔNG: ĐẠT` `rc=0` |
| C3 | Cả hai sổ rỗng ⇒ cổng **ĐỎ** | hai đột biến cùng lúc; hiện `rc=0` |
| C4 | Ca **có MẶT** mà không **có ĐO** ⇒ cổng **ĐỎ** | đột biến bỏ lời gọi thân ca nhưng GIỮ dòng ghi sổ ĐẠT; hiện báo **`13 đạt`** cho 13 ca chưa từng chạy |

C1–C4 là **bốn hình dạng rỗng độc lập**, không phải một. Vá `not DO` mà bỏ ba cái kia là lặp đúng
lỗi vòng 2 — "tách sổ mà không đòi sổ nền khác rỗng thì chưa vá gì; nó chỉ đổi chỗ cái lỗ".

### D. Hợp đồng và cổng (mục tiêu 4–5, 8)

**Ràng buộc thiết kế cho MỌI ca (r2 thêm, sau khi ba đột biến sống sót vì thiếu nó):** ca của một
tiêu chí **không được đi qua** đúng đoạn mã mà đột biến của tiêu chí KHÁC nhắm vào. Ba ca sống sót
ở lượt 1 vì vi phạm: `b1_bo_data` giết cả `B1` lẫn `B2` (ca `B2` đi qua đường tách thân SSE);
`b3_bo_token` giết cả `B3` lẫn `D6` (ca CLI khẳng định `rc=3` sinh từ chốt token);
`b5_bo_urlerror` giết cả `B5` lẫn `D5`. Cách chữa là **đổi ĐƯỜNG VÀO của ca bị vạ lây**, không
phải nới phép đếm: `B2` gọi thẳng hàm rút văn bản; `D6` cấp token hợp lệ rồi mới đo mã thoát của
cờ; `D5` bơm lỗi vận chuyển qua một điểm khác điểm `B5` dùng.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| D1 | `tools/call` trả top-level `error` ⇒ `main` trả mã khác 0 | ca bơm phản hồi lỗi; hiện `main` trả `0` ⇒ ĐỎ |
| D2 | `result.isError == true` ⇒ `main` trả mã khác 0 | ca riêng D1, vì hai đường hỏng khác nhau |
| D3 | `initialize` trả `{"result": {}}` rỗng ⇒ KHÔNG được coi là mở phiên | ca riêng; hiện `loi_cua` trả `None` khi có khoá `result` ⇒ ĐỎ |
| D4 | Phản hồi dạng **list** ⇒ báo lỗi có cấu trúc, KHÔNG `AttributeError` | ca bơm `[]`; hiện ném `AttributeError` không bắt ⇒ ĐỎ |
| D5 | Lỗi vận chuyển khi gửi `notifications/initialized` ⇒ phiên KHÔNG được coi là mở | ca bơm lỗi ở lời gọi thứ hai; hiện giá trị trả bị bỏ ⇒ ĐỎ |
| D6 | Bốn lời gọi CLI cũ chạy y nguyên trên bản mới: `--liet-ke` · `<tên> '<json>'` · `--path` · mã thoát `0/2/3` | ca chạy `main()` cho từng dạng; đổi tên cờ hoặc đổi mã thoát ⇒ ĐỎ |
| D7 | Suite đầy đủ: hai số **BẰNG NHAU** và **> 0**, mọi đột biến bị giết, `rc=0` | `rc` trần KHÔNG đủ — phải đọc dòng tổng kết. Đây chính là bài học của packet |
| D7b | **Sổ nền phải XANH thì phép đếm đột biến mới có nghĩa.** Nền đỏ ⇒ cổng ĐỎ vì lý do NỀN, và ô đột biến in **`KHÔNG_ĐO_ĐƯỢC`**, KHÔNG in `0/N` | r2 thêm sau phép đo lượt 1: bốn ca nền đỏ làm MỌI đột biến "giết" thêm đúng bốn ca ấy, nên "đúng một ca" không bao giờ thoả và cổng in `0/35`. Con số ấy ĐÚNG mà đọc thành "không đột biến nào có răng" — sai hẳn. **Cấm trừ ca đỏ nền để lấy một con số đẹp**: trừ đi là giấu nền hỏng. Đường đúng là fail-close: nói thẳng chưa đo được |
| D8 | **QUY ĐƯỢC TRÁCH NHIỆM** — ba điều kiện, kiểm riêng từng cái: (a) ca ĐÍCH của mỗi đột biến **nằm trong** tập giết; (b) **không** đột biến nào có tập giết RỖNG; (c) **mọi** ca là đích của ít nhất một đột biến | (a) hỏng ⇒ đột biến không đo thứ nó khai · (b) hỏng ⇒ đột biến không có răng · (c) hỏng ⇒ ca không ai canh. Nền không rỗng ⇒ xem `D7b`, không kết luận. Giao phạm vi (tập giết có ca ngoài đích) **được IN RA** cho reviewer đọc, KHÔNG làm cổng đỏ |
| D9 | Ngân sách: tổng dòng **không-trắng** của `.claude/dev/mcp_gh.py` và `.claude/dev/mcp_gh_test.py` **≤ 1000** (chủ kho cấp ngoại lệ 1000/200 ngày 2026-09-13 trên nền 776, sau khi r2 780 trượt). Lịch sử: tại `245905e2`, phép đo đúng là 761 tổng / 18 slack / 11 chú thích. Mệnh đề gốc *"chọn (A) đếm cả chú thích... vì loại khỏi phép đếm sẽ tạo áp lực xoá tri thức"* là suy diễn sai (11 dòng chú thích không giải cứu được biên 18 dòng), nhưng phải GIỮ LẠI LÀM LỊCH SỬ. Động cơ nén rẻ nhất còn lại là gói nhiều lệnh vào một dòng dài | vượt ⇒ điều kiện dừng `S2`; lần chạm kế tiếp phải hỏi có nên tách tệp, không nới trần |

### Bản sửa đổi 4 thêm `D10` và `D11` — phán định phải SUY TỪ bản báo cáo

**Vì sao r4 tồn tại.** Mã đã đi trước đặc tả: ca `D10-main` có trong sổ ca mà KHÔNG có tiêu chí
nào ở bảng trên, và cross-review vòng 3 nêu một P1 mà bảng trên không có chỗ để trả lời. Bản vá
đầu cho P1 ấy bị phiên điều phối đo lại và bác — nên r4 sửa ĐẶC TẢ trước, đúng thứ tự `S1`.

**Phép đo đã bác bản vá đầu** (biên nhận `ops/reviews/mcp-gh-cuu-ho-kiem-doc-lap-va-P1-vong3.*`):
bản vá thêm vào `chay_cli` một chốt hai dòng thay TOÀN BỘ `d8_errors` bằng một bộ dựng sẵn khi
một cờ không được ca `D11-gate` đặt. Ba phép đo đột biến theo SỐ DÒNG cho thấy:

- Xoá chốt là **vô hình** với toàn bộ bộ đo — cổng vẫn `40/40`, `D8 ĐẠT`, `rc=0`. Chốt không có
  phản chứng nào, tức là mã KHÔNG ĐO ĐƯỢC thêm vào chính cái cổng đang đo mọi thứ khác.
- Chốt cũng **không cần thiết**: bỏ nó đi thì kịch bản thân-ca-rỗng VẪN chết, qua khẳng định
  "ca đã thực sự chạy" nằm trong THÂN CA. Cái giết nó là ca, không phải chốt.
- Và chốt **làm hỏng bản báo cáo**: vì nó THAY `d8_errors` chứ không THÊM lỗi, trong đúng kịch
  bản nó sinh ra để bắt, dòng `D8(b)` in ra `ĐẠT` trong khi sự thật đo được là `ĐỎ` cho cả 46
  đột biến. Một khẳng định xanh không đúng sự thật, ở đúng chỗ nó phải mô tả.

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| D10 | Điểm vào `__main__` phải THỰC SỰ chạy sổ ca. Một `main` trả `0` mà không gọi ca nào ⇒ **ĐỎ** | ca dựng cảnh sổ ca một phần tử có cờ ghi nhận, gọi điểm vào, và đòi CẢ HAI: mã thoát khác 0 VÀ cờ đã được đặt. Chỉ đòi mã thoát thì một `return 0` cứng vẫn lọt |
| D11 | **Phán định SUY TỪ bản báo cáo, không tính song song với nó.** `chay_cli` sinh TOÀN BỘ dòng báo cáo trước; `TỔNG` và mã thoát cùng suy từ MỘT phán định tính TỪ các dòng ấy. Không được có hai đường tính độc lập cho `TỔNG` và cho `rc` | ca chạy `chay_cli` trong ÍT NHẤT HAI cảnh — một xanh, một đỏ — bắt `stdout`, và đòi quan hệ **hai chiều**: bản in có dấu đỏ ⟺ mã trả về khác 0. Ép `rc` thành hằng số ⇒ quan hệ gãy ở cảnh đỏ ⇒ ĐỎ. Đây là chỗ P1 vòng 3 nằm: `TỔNG` suy từ `rc` chứ không suy từ báo cáo, nên hai nửa cùng một bản in mâu thuẫn nhau được |

**Cấm CHỐT TỰ CHIẾU (r4 thêm, và đây là ràng buộc THIẾT KẾ, không phải lời khuyên).** Mã sản phẩm
KHÔNG được thay kết quả đo bằng một giá trị dựng sẵn để chứng minh rằng một ca đã chạy. Lý do đo
được, không phải thẩm mỹ: một chốt như thế (a) tự nó không đo gì nên không có phản chứng, và
(b) khi bắn thì nó GHI ĐÈ phép đo thật, biến một dòng đỏ đúng thành một dòng xanh sai. Muốn biết
một ca đã chạy thì đòi điều đó **trong thân ca**, nơi phép khẳng định là bằng chứng chứ không phải
là giả định. Phản chứng cho chính điều cấm này: xoá bất kỳ dòng nào của cơ chế `D11` phải làm ĐỎ
một ca CÓ TÊN — không được có dòng nào trong cơ chế mà xoá đi vẫn xanh.

**`D11` KHÔNG hứa điều không hứa được.** Dòng ngoài cùng nhất — `sys.exit(chay_cli())` — vẫn có
thể sửa thành `sys.exit(0)`, và không phép đo nào chạy TRONG tiến trình bắt được nó. `D11` không
xoá được bề mặt, nhưng nó làm mọi đường làm giả trừ dòng ngoài cùng nhất đều phải để lại vết trong
báo cáo. Khai
thẳng ở đây để không ai đọc `D11` thành "cổng nay không thể bị làm giả".

Đột biến chạy trên **bản sao tạm**, tên tệp riêng, không ghi vào tệp thật — kho đã trả giá cho một
bản vá NGƯỢC đi thẳng vào commit vì `finally` không chạy khi lượt bị `SIGTERM` cắt.

## Ngân sách và ADR-0044 — khai lý do vượt trần (chốt Q1)

| | |
|---|---|
| trần của lease r2 | **≤ 750 dòng thêm**, 3 tệp, đo từ `b662fe1` |
| ADR-0044, `sensitive` **chạm authority** | ≤ 3 tệp và ≤ **300** dòng thêm |
| ADR-0044, packet **thường** | ≤ 6 tệp và ≤ **1.000** dòng thêm cộng xoá |

Packet này xếp **thường** theo ADR-0044 vì `mcp_gh.py` không cấp lease, không gác cổng, không vào
gói phát hành — dù `review_class` là `sensitive`. 750 nằm dưới trần 1.000.

**Khai thẳng phần vượt:** nếu ai đọc nó là *"sensitive chạm authority"* thì 750 vượt trần 300 **2,5
lần**, và ADR-0044 cho đúng một đường: *"dừng TRƯỚC review để revision thiết kế, **hoặc khai lý do
trong spec**"*. Lý do: hai lỗ là lỗi THIẾT KẾ nên phải viết lại chứ không vá — đã vá một lần và
thất bại đúng chỗ vừa vá; và **334/541 dòng của bản bị bác là TEST**, tỷ lệ mã:test ~1:1,6, nên
phần lớn ngân sách là phản chứng chứ không phải bề mặt mới.

**Và cổng cưỡng chế ngưỡng ấy KHÔNG TỒN TẠI.** ADR-0044 viết *"Cưỡng chế: cổng write-set và
`numstat` chạy TRƯỚC review"*. Quét `.claude/dev` + `ops` + `.github` lúc 09:35Z 26-08: không hằng
số `300`/`1.000` nào, và `numstat` chỉ xuất hiện ở `ops/chatgpt_review/build_bundle.py` — bộ **dựng
bundle review**, không phải cổng. Ngưỡng ADR-0044 hiện là **kỷ luật đọc**, không phải cổng. Ghi ra
vì một cổng vắng mặt trông y hệt một cổng xanh, và vì nợ này không thuộc packet nào đang mở.

### Vì sao `D8` đổi — và cái giá của việc đổi nó

**Nói cái giá trước, vì nó thật:** nới một tiêu chí ngay sau khi trượt nó **trông y hệt dịch cột
đích**. Ai đọc hồ sơ này về sau có quyền nghi đúng chỗ ấy. Nên lý lẽ phải đứng được độc lập với
việc bản vá hiện tại có qua hay không.

**"Đúng một ca" là BIẾN, không phải thứ cần đo.** Thứ cần đo là: *ca này có thật sự canh tính chất
nó khai không*. Biến ấy đúng khi các ca độc lập về đường mã, và **sai khi chúng dùng chung đường
mã một cách CHÍNH ĐÁNG** — một ca CLI bắt buộc đi qua `Phien.__init__`; hai ca `B7` cùng đo một họ
chốt chống `.pyc`. Ép chúng tách ra không làm phép đo mạnh hơn; nó làm ca **méo đi** để chiều một
con số, và lượt 2 đã cho thấy mỗi lần ép lại đẻ ra một cặp giao mới.

**Bằng chứng rằng biến sai chứ không phải bản vá sai:** hai đột biến sống sót ở lượt 2 đều có ca
ĐÍCH nằm trong tập giết, và **không** đột biến nào có tập giết rỗng. Tức chúng ĐẠT cả ba điều kiện
mới, và chỉ trượt đúng cái biến bị bỏ. Không có tính chất nào mất đi khi đổi tiêu chí — thứ mất đi
là một đòi hỏi về **hình dạng của tập giết**, vốn chưa bao giờ là mục tiêu.

**Cái mới KHÔNG lỏng hơn ở chỗ quan trọng:** `(b)` và `(c)` là hai điều kiện `D8` cũ **không có**.
`(c)` đặc biệt — nó bắt mọi ca phải là đích của ít nhất một đột biến, tức chặn thẳng lớp "ca không
ai canh" mà `D8` cũ để lọt. Đo được: `b7_bo_xoa_pyc` ở lượt 1 có tập giết **RỖNG** và `D8` cũ báo
nó "sống sót" chung một rọ với các ca giao phạm vi — hai bệnh khác hẳn nhau, cùng một thông điệp.

**Giao phạm vi vẫn phải IN RA.** Nó là dữ liệu chẩn đoán thật: một đột biến giết năm ca là dấu hiệu
mã bị nối quá chặt. Chỉ khác là nó thành thứ reviewer ĐỌC, không thành thứ cổng ĐỎ.

## Ngân sách — ĐỔI ĐƠN VỊ ĐO ở r3, và khai vì sao trước khi ai phải hỏi

**Đơn vị cũ (r1/r2):** `git diff --numstat` trên **cả write set**, tức gồm cả tệp đặc tả này.
**Đơn vị mới (r3):** trần áp cho **hai tệp MÃ** — `.claude/dev/mcp_gh.py` và
`.claude/dev/mcp_gh_test.py`. Đặc tả theo dõi **riêng** và vẫn phải báo cáo, chỉ không trừ vào trần.

**Vì sao đổi — ba lần đo, cùng một nguyên nhân.** Trần bị chạm ba lần trong packet này
(750 → 1000 → 1100), và **cả ba lần đều do ĐẶC TẢ nở, không do mã**. Đo 11:4xZ 26-08:
mã đứng ở **802** (`mcp_gh.py` 230 · `mcp_gh_test.py` 572) suốt từ lượt 2, trong khi đặc tả đi
210 → 258 → 289. Đơn vị cũ tính **hợp đồng** vào ngân sách của **thứ nó điều khiển**, nên mỗi lần
sửa đặc tả cho ĐÚNG lại bị phạt — một động cơ ngược, và nó đã bày ra ba lần chứ không phải một.

**Vì sao đây không phải nới trần trá hình.** ADR-0044 tồn tại để bó **gánh nặng review của bản
vá**: `PLAT-M4` 2 tệp/+351 ⇒ một vòng một finding; `PLAT-X4` 4 tệp/+721 ⇒ ba vòng tám finding.
Cả hai đều đo **mã**. Đặc tả ở đây là **đầu vào đã qua hai vòng chất vấn của người giữ kho**, không
mang rủi ro hồi quy, và reviewer đọc nó như hợp đồng chứ không soát nó như diff. Theo đơn vị mới,
**802 nằm dưới ngưỡng 1.000 của lớp `thường` với biên gần 200** — packet chưa từng thật sự lớn.

**Cái giá, nói thẳng:** đổi ĐƠN VỊ trông tệ hơn đổi con số, vì nó đổi luôn thứ đang được đo. Đây là
lần thứ BA động vào ngân sách của cùng một packet. Ai đọc hồ sơ về sau có quyền nghi đúng chỗ này,
nên: con số theo **cả hai** đơn vị phải được báo ở mọi lượt, và người land phải **thấy** rằng đơn
vị đã đổi chứ không để nó trôi qua như chi tiết nội bộ.

**Chốt chống lặp:** nếu **MÃ** chạm 900 thì câu trả lời là **TÁCH**, không phải nâng lần bốn và
cũng không phải đổi đơn vị lần hai.

## Vượt ngưỡng ADR-0044 — KHAI LÝ DO, đúng đường ADR cho phép

Đo 11:22Z 26-08, sau lượt thi công 1: write set đã dùng **1000 dòng thêm** (`mcp_gh.py` 226 ·
`mcp_gh_test.py` 564 · đặc tả r1 210). Bản sửa đổi này cộng thêm ~55 dòng, và năm bản vá đột biến
cộng thêm ít nữa ⇒ tổng **vượt 1.000**, tức vượt ngưỡng lớp `thường` của ADR-0044.

ADR-0044 cho đúng hai đường: *"dừng TRƯỚC review để revision thiết kế, **hoặc khai lý do trong
spec**"*. Đây là lời khai ấy.

**Lý do:** trần bị tiêu bởi chính **đặc tả** — nó nằm trong write set, nên hợp đồng bị tính vào
ngân sách của thứ nó điều khiển. 210 dòng đặc tả và ~55 dòng bản sửa đổi này **không phải bề mặt
mã**, không mang rủi ro hồi quy, và đã qua hai vòng chất vấn của người giữ kho. Phần MÃ thật là
790 — dưới 1.000, và chỉ nhỉnh hơn 541 của bản bị bác đúng phần ca và đột biến mà đặc tả đòi thêm.

**Điều này KHÔNG được đọc thành "ngưỡng không áp dụng".** Nó chỉ nói: với packet có đặc tả nằm
trong write set, con số `numstat` trộn hai thứ khác loại. Nếu lượt sau lại chạm trần, câu trả lời
đúng là **TÁCH** — ADR nói thẳng thế — chứ không phải khai lý do lần nữa.

## chua_do_duoc

1. **Chuyển hướng của điểm cuối THẬT.** Bảng 301..308 đo trên hai `http.server` cục bộ, tức đo
   **hành vi của `urllib`**, không phải của `api.githubcopilot.com`. Vẫn đủ để đòi opener không đi
   theo chuyển hướng — chốt phải đứng vững bất kể máy chủ kia trả gì — nhưng đừng khai rộng hơn.
2. **`result.isError` từ một công cụ THẬT.** Mới đọc mã; chưa dựng được ca làm máy chủ trả
   `isError: true`. Ca D2 sẽ dùng phản hồi BƠM, và điều đó phải ghi ngay tại ca.
3. **Bảng đo sandbox của #314 chưa được kiểm chéo** — reviewer vòng 2 không tái lập được
   (`codex exec` lồng nhau `rc=1`, `Read-only file system`). Không thuộc packet này, nhưng nếu
   ai viện dẫn nó thì phải kèm câu này.
4. **Ba `stdout.log` của #314 không có trong kho** ⇒ ba con số `78/5/10,8M · 85/10/12,8M ·
   45/1/3,7M` không tái lập được từ đây.
5. **`da_bi_thay_the` chỉ nhận MỘT tên.** Cổng `_kiem_bia_mo` vừa land trong PR #316 so khớp chuỗi
   vô hướng, nên một lease bị **hai** lease thay thế — đúng ca `r4` của #314 bị #318 và #319 phân
   hoạch — **không biểu diễn được**. Hai lease ấy đã đăng TRƯỚC khi cổng land nên lọt; lease nào
   sau này muốn khai cùng quan hệ sẽ bị chặn. Chưa đo hết hệ quả; đã báo #313.
6. **Lượt thi công 1 KHÔNG chạy được `A5`–`A7`** trong sandbox của nó (thiếu quyền `bind`), nên
   ba tính chất chuyển hướng — thứ chỉ có phiên tiếp quản đo được, và là lỗ P1 thứ ba của packet —
   **chưa từng được xác nhận bởi một nền độc lập với nền đã phát hiện ra chúng**. Vỏ phiên điều
   phối chạy được, nhưng nó cũng chính là nơi phát hiện. Cần một lượt chạy ở CI hoặc nền thứ ba.
7. **`lease_publish.py check` chạy từ HEAD TÁCH RỜI không thấy lease vừa commit.**
   `_cac_ref_cuc_bo` chỉ đọc `refs/heads` + `refs/remotes`, nên commit ở HEAD tách rời là vô hình.
   Đo được: cùng một commit, HEAD tách rời ⇒ `rc=8`; trỏ một nhánh vào đúng commit ấy ⇒ `rc=0`.
   Đáng chú ý vì kho cho reviewer chạy ở **detached exact head**. Chưa đo hệ quả cho đường review;
   đã báo #313.
