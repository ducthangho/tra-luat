# ĐẶC TẢ — `MCP-GH-CUU-HO` (Issue #319)

Đặc tả này ĐÓNG BĂNG bằng băm. Lease neo vào `spec_sha256`. Sửa nội dung ⇒ băm đổi ⇒ lease trỏ
vào thứ không còn tồn tại, phải đi qua bản sửa đổi mới. Soạn bằng skill `soan-spec`.

| khoá | giá trị |
|---|---|
| `packet_id` | `MCP-GH-CUU-HO` |
| `packet_issue` | 319 |
| `nguon_cap_viec` | Packet cha **#314**, verdict cross-review vòng 2 trên PR #315 — `blocked` · `DO_NOT_LAND`, comment `5423010218`, `reviewed_sha 6c4140ba507162ca1c6ee8d2bf510445574bad24`. **Verdict ấy KHÔNG có biên nhận trong kho**: quét cả 206 ref lúc 09:45Z 26-08 ⇒ **0** tệp `ops/reviews/*` nào cho #314/#315. Nguồn cấp việc của packet này do đó là một **comment**, không phải tệp có băm — nói thẳng vì `CLAUDE.md` chốt rằng nguồn có thẩm quyền là tệp có băm, và ở đây điều kiện ấy KHÔNG thoả |
| `review_class` | `sensitive` — cổng `_BANG_LOP` tự tính, mặc định fail-close. Ở packet này còn là hạng đúng theo nội dung: mã cầm `GITHUB_PAT` và tự quyết định gửi nó đi đâu. **KHÔNG** "chạm authority" theo nghĩa ADR-0044: không cấp lease, không gác cổng, không vào gói phát hành (chốt Q1) |
| `base_sha` | `b662fe1d07c675a222ae26e734377e305775e4f3` — `origin/master` đo 09:57Z 26-08 |

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

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| D1 | `tools/call` trả top-level `error` ⇒ `main` trả mã khác 0 | ca bơm phản hồi lỗi; hiện `main` trả `0` ⇒ ĐỎ |
| D2 | `result.isError == true` ⇒ `main` trả mã khác 0 | ca riêng D1, vì hai đường hỏng khác nhau |
| D3 | `initialize` trả `{"result": {}}` rỗng ⇒ KHÔNG được coi là mở phiên | ca riêng; hiện `loi_cua` trả `None` khi có khoá `result` ⇒ ĐỎ |
| D4 | Phản hồi dạng **list** ⇒ báo lỗi có cấu trúc, KHÔNG `AttributeError` | ca bơm `[]`; hiện ném `AttributeError` không bắt ⇒ ĐỎ |
| D5 | Lỗi vận chuyển khi gửi `notifications/initialized` ⇒ phiên KHÔNG được coi là mở | ca bơm lỗi ở lời gọi thứ hai; hiện giá trị trả bị bỏ ⇒ ĐỎ |
| D6 | Bốn lời gọi CLI cũ chạy y nguyên trên bản mới: `--liet-ke` · `<tên> '<json>'` · `--path` · mã thoát `0/2/3` | ca chạy `main()` cho từng dạng; đổi tên cờ hoặc đổi mã thoát ⇒ ĐỎ |
| D7 | Suite đầy đủ: hai số **BẰNG NHAU** và **> 0**, mọi đột biến bị giết, `rc=0` | `rc` trần KHÔNG đủ — phải đọc dòng tổng kết. Đây chính là bài học của packet |
| D8 | Mỗi đột biến giết **đúng một** ca | giết 0 ca ⇒ ca không có răng; giết nhiều ca ⇒ ca trùng phạm vi |
| D9 | Ngân sách: `git diff --numstat` trên write set, cột dòng THÊM, **≤ 750** | vượt ⇒ điều kiện dừng `S2` của lease, DỪNG và xin nâng trần bằng khối có `ai_nang`/`vi_sao` |

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
6. **`lease_publish.py check` chạy từ HEAD TÁCH RỜI không thấy lease vừa commit.**
   `_cac_ref_cuc_bo` chỉ đọc `refs/heads` + `refs/remotes`, nên commit ở HEAD tách rời là vô hình.
   Đo được: cùng một commit, HEAD tách rời ⇒ `rc=8`; trỏ một nhánh vào đúng commit ấy ⇒ `rc=0`.
   Đáng chú ý vì kho cho reviewer chạy ở **detached exact head**. Chưa đo hệ quả cho đường review;
   đã báo #313.
