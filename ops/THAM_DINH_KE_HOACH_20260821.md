# BẢN HỢP NHẤT — thẩm định kế hoạch triển khai, 20/21-08-2026

Ba bên độc lập: **codex** (`gpt-5`, `model_reasoning_effort=xhigh`, 3 lượt), **Claude Fable 5**,
**Claude Opus 5**. Ba vòng. Cây duyệt chỉ-đọc `8d6f8779` (master `2663477` + bằng chứng của
ngày gộp vào). Phiên điều phối tự đo lại 14 khẳng định; kết quả ở `BIEN_TAP_do_lai.md`.

## 0. Hai việc CHỈ NGƯỜI GIỮ KHO làm được
- **Q1.** `attempts_limit` của `PLAT-X5` bị hạ **3 → 2** giữa hai revision lease, không lý do,
  không khối `nang_tran`/`ha_tran`, và **tiêu đề tệp r2 vẫn ghi "lượt 1/3"**. Đây có phải chỉ đạo
  của anh không? Đo được rằng nó KHÔNG ĐƯỢC GHI; không đo được rằng nó KHÔNG ĐƯỢC NÓI.
  · Nếu KHÔNG phải chỉ đạo ⇒ đính chính append-only về 3 (chọn phía CÓ NGUỒN của một mâu thuẫn).
  · Nếu LÀ chỉ đạo ⇒ trần 2 đứng, mọi lượt vá tiếp là NỚI THẬT và phải có `nang_tran` đúng khuôn.
- **Q2.** Có bật **required status check** cho job `gate` trên `master` không? Đây là việc NGOÀI kho.
  Kế hoạch dưới đây chạy được ở CẢ HAI trả lời (đường A / đường B), nên câu này không chặn gì.

## 0bis. QUYẾT ĐỊNH CỦA NGƯỜI GIỮ KHO — 21-08-2026

Chép nguyên trạng, không diễn giải. Người quyết: `ducthangho`. Kênh: trực tiếp trong phiên.

| # | Nội dung | Quyết định |
|---|---|---|
| Q1 | `attempts_limit` PLAT-X5 bị hạ 3→2 | **KHÔNG phải chỉ đạo của chủ kho. Để `attempts_limit` là 3.** |
| Q2 | Đóng `#203`/`#206` là `superseded` | **Đồng ý** |
| Q3 | Một Recovery Packet hay hai slice | **Hai slice** (Behavior / Authority, vào integration branch) |
| Q4 | Mở write set `ops/lease_publish.py` | **Mở, theo khuyến nghị** (duyệt tường minh; làm SAU Slice A/B) |
| Q5 | Con số canon của trần vòng review | **Chốt 2** — ghi bằng ADR, không bằng một § |
| Q6 | Hai ngưỡng kích thước packet | **Duyệt** |
| Q8 | Hợp thức hoá đảo vai executor/reviewer | **Theo khuyến nghị** — ADR cho NGOẠI LỆ có vết, KHÔNG đổi mặc định |
| Q9 | Commit bản hợp nhất vào `ops/` | **Có** |

### CẬP NHẬT 21-08-2026, ~03:30Z — Q2 và Q3 ĐÃ BỊ THỰC TẾ VƯỢT QUA

**Đo được:** `master` đi từ `2663477` → `dc1a939`. **PR #207 (`PLAT-X5`) đã land, và nuốt luôn
`#203`/`#205`** — 11 commit, gồm cả `d0acd79`…`a09aae6` của X4 lẫn `3ad7555`…`e071e0a` của X5,
cộng hai commit MỚI (`2284b46`, `117e0c4`) khoá `t25`/`t35` và tách `mkdir` thành `rc=12`.
Nhánh `ops/verdict-x5-review-3` cho thấy X5 đã qua **một vòng review thứ ba** (reviewer `claude`)
trước khi land.

**Tư cách của việc này:** người giữ kho xác nhận **đã cho phép** phiên ấy. Nên Q2 ("đóng
`#203`/`#206` là `superseded`") và Q3 ("hai slice từ integration branch") **không bị vi phạm** —
chúng bị **thay bằng một ngoại lệ có phép**. Ghi cả hai vế: quyết định từng là gì, và thực tế đã
đi đường nào. Xoá dấu vết một trong hai vế là làm hỏng chính thứ tài liệu này sinh ra để giữ.

**Và phải ghi một điều bất lợi cho chính bản hợp nhất này.** Cách chuỗi thực sự được xử lý —
MỘT VÒNG REVIEW THỨ BA TRÊN HEAD GỘP, rồi land cả cụm — gần đúng phương án `(d)` của **Fable 5**
mà **Opus 5** đã bác và bản hợp nhất đã theo Opus. Thực tế cho thấy đường ấy đi được.
Lập luận của Opus KHÔNG sai về dữ kiện: biên nhận X5 neo `base_sha: a09aae62`, nên 721 dòng của
X4 chưa verdict nào phủ — điều đó vẫn đúng, và vòng 3 chính là thứ đã lấp chỗ ấy. Nhưng
**kết cục thực nghiệm nghiêng về Fable**, và tài liệu này ghi điều đó thay vì im lặng.

**BÀI HỌC SÂU NHẤT CỦA ĐỢT, và nó KHÔNG phải lỗi mã:**
Bản hợp nhất này tốn khoảng ba giờ máy của ba bên độc lập, và **bị thực tế vượt qua trong vài
giờ** — vì nó nằm trên một **PR CHƯA MERGE** trong khi công việc vẫn chạy. Phiên kia không có
cách nào đọc được nó. Nói gọn: **một kế hoạch chưa vào master không phải kế hoạch, nó là một đề
xuất.** Chốt rút ra, rẻ và dùng được ngay: **land tài liệu kế hoạch TRƯỚC, rồi mới thi hành từ
nó** — ngược với thứ tự đã làm ngày 21-08.

### ĐÍNH CHÍNH 22-08-2026 — câu "vòng 3 đã lấp chỗ ấy" là SAI

**Append-only. Không câu nào ở trên bị xoá hay sửa đè** — vế sai ở lại làm bằng chứng, đúng nếp
mà chính mục `CẬP NHẬT ~03:30Z` đặt ra khi nó từ chối xoá dấu vết một trong hai vế.

Mục trên viết:

> *"…721 dòng của X4 chưa verdict nào phủ — điều đó vẫn đúng, và **vòng 3 chính là thứ đã lấp chỗ ấy**."*

Vế in đậm **sai**. Đo 22-08-2026:

| phép đo | kết quả |
|---|---|
| `base_sha` của `plat-x5-review-1-claude-verdict.receipt.yaml` | `a09aae62` |
| `base_sha` của `plat-x5-review-2-…` | `a09aae62` |
| `base_sha` của `plat-x5-review-3-…` (dòng 22) | **`a09aae62`** |
| tệp verdict `plat-x4-*` trong `ops/reviews/` | **0** |
| nhánh `ops/verdict-x4-*` trên remote | **0** |
| review trên PR `#205` | **1**, của bot connector, neo `d0acd79f` = commit ĐẦU của X4 |

Cả **ba** vòng neo cùng một `base_sha`. Vòng 3 chỉ đẩy `reviewed_sha` **về phía trước**
(`e071e0aa` → `2284b465` → `117e0c42`); nó **không** hạ đáy vùng phủ. Vùng `909d3e17..a09aae62`
— đúng 4 tệp, `+721/-159` — vẫn nằm **dưới** đáy của cả ba.

**Vì sao lỗi này đáng ghi thay vì lặng lẽ sửa:** nó biến một nợ CÓ THẬT thành một nợ ĐÃ ĐÓNG trong
sổ. Nợ chưa ghi thì còn có người vấp phải; nợ ghi nhầm là đã trả thì **không ai đi đòi nữa**. Và
cơ chế gây ra nó rất rẻ để lặp lại: đọc `reviewed_sha` rồi kết luận về vùng phủ, trong khi thứ
quyết định vùng phủ là `base_sha`.

Nợ nay có tên và có nhà: `ops/NO_KY_THUAT.md` mục **12**
(`PLAT-X4-721-dong-chua-verdict-nao-phu`), kèm điều kiện coi là XONG.

Ghi thêm một điều bất lợi cho chính bản hợp nhất, cùng nếp với đoạn trên: mục `CẬP NHẬT ~03:30Z`
kết luận *"kết cục thực nghiệm nghiêng về Fable"*. Kết luận ấy đứng trên giả định rằng vòng 3 đã
phủ hết cụm gộp. Giả định ấy nay đo được là sai, nên **cán cân Fable/Opus của đoạn ấy chưa được
phân định** — không phải nghiêng về Opus trở lại, mà là **chưa có phép đo nào phân định**.

### Kế hoạch thi hành — BẢN THAY THẾ cho `V0`–`V6`

`V1`/`V2`/`V3` **BỎ**. Đo được vì sao: phần lớn nội dung của Slice A/Slice B đã vào master theo
lần land trên — `t25` P1 **đã đóng** (nay đếm `thay_wrapper`, thấy lời gọi wrapper), `t35` đã
siết, `mkdir` đã tách mã thoát, wrapper + `cai_actionlint` + `t36`–`t40` đã có (bộ kiểm 41 ca).
Còn lại của Slice B chỉ đủ một packet nhỏ, không phải một slice. `V1` (integration branch) sinh
ra để chặn đúng cái chuỗi ấy, mà chuỗi đã land.

| # | việc | vì sao là bây giờ |
|---|---|---|
| **A** | Sửa tài liệu này cho khớp thực tại + gộp master + **merge PR #210 NGAY** | tài liệu đang nói sai; và theo bài học trên, nó phải vào master TRƯỚC khi ai thi hành từ nó |
| **B** | Xong `#204` (gộp master → gate → review vòng 3 → land) | đang dở; trần vòng 2→3 đã được duyệt |
| **C** | Packet nhỏ: hai mục sổ nợ + hạ lời khai `t34` + ca máy đòi docstring liệt kê đủ 5 dạng đã ĐO là lọt | phần còn lại DUY NHẤT của Slice B; Q7 (không bật) làm nó thành nợ VĨNH VIỄN, nên phải vào sổ |
| **D** | **Gói `lease_publish`** — spec_hash · cross-provider · băm tồn tại thật · 4 mức assurance · đổi/vượt trần phải có căn cứ · timestamp không ở tương lai · reservation gate · hình dạng kế thừa | **giá trị cao nhất còn lại**. Lần land vừa rồi càng chứng minh: thứ ràng buộc là CỔNG QUẢN TRỊ, không phải mã |
| **E** | Sandbox reviewer thành SCRIPT fail-đóng | ba lần trả giá, lần thứ ba là lỗi của chính phiên điều phối ngày 21-08 |
| **F** | Đồng bộ văn bản trần vòng + `so-canon` + xoá hai lời khai "ĐO ĐƯỢC" sai | rẻ, làm cuối |

**ĐO ĐƯỢC, còn mở tại lúc viết:** `ops/NO_KY_THUAT.md` có **0** mục cho
`PLAT-X5-required-status-check`, và `.github/workflows/ci.yml` khai **2** chuỗi "NỢ CÓ TÊN" mà sổ
nợ có **0** mục tương ứng. Đó là đối tượng của mục **C**, và nó ĐỎ ngay hôm nay.

**Q7 — ĐÃ TRẢ LỜI 21-08-2026: KHÔNG BẬT.** Người quyết: `ducthangho`.

Trước đó tệp này ghi Q7 ở trạng thái thứ ba (`chưa quyết`, không phải `không`). Nay nó thành một
QUYẾT ĐỊNH, và hệ quả khác hẳn — nên phải viết lại chứ không để nguyên câu cũ:

- **ĐƯỜNG B là đường CHÍNH THỨC, không còn là mặc định tạm.** Không còn nhánh A để chờ.
- **`t34` SỐNG lâu dài.** Việc phải làm ở Authority Slice không còn là "xoá `t34` sau khi đọc lại
  cấu hình" mà là **hạ lời khai của nó xuống đúng phạm vi đo được** — liệt kê nguyên văn năm dạng
  gọi đã ĐO là lọt (`python -m` · `python3 -u` · shebang trực tiếp · `uv run` · `python -X`) — kèm
  một ca máy đòi docstring chứa đủ năm dạng ấy, để lời khai không trôi rộng ra lần nữa.
- **Giá phải trả, nói bằng số chứ không bằng chữ:** câu hỏi "CI có thật sự chạy gate không" **vĩnh
  viễn không có nhà**; nợ `PLAT-X5-required-status-check` thành **nợ thường trực**, không phải nợ
  có hạn, và phải được ghi vào `ops/NO_KY_THUAT.md` đúng như thế. `t34` che **3/8 = 37,5%** dạng
  gọi đã biết, nên mỗi lần đổi cách gọi vẫn sẽ đẻ một finding.
- **Cái KHÔNG mất:** với `PATH` thiếu `actionlint` vẫn có **8 ca đỏ**. Thứ mất là **DETECTION**,
  không phải **PROTECTION** — đừng đọc quyết định này thành "bỏ ngỏ cổng".
- Mọi mục khác của kế hoạch chạy nguyên vẹn: `t34` là mục DUY NHẤT từng treo vào việc ngoài kho,
  và nay nó hết treo.

### Hệ quả ghi được ngay từ các quyết định trên
- Q1 ⇒ `ops/DINH_CHINH_TRAN_ATTEMPT_PLAT_X5.md` (append-only, KHÔNG sửa lease cũ).
- Q5 ⇒ `docs/adr/0043-tran-vong-review-canon-la-hai.md`.
- Q6 ⇒ `docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md`.
- Q8 ⇒ `docs/adr/0045-ngoai-le-dao-vai-executor-reviewer.md`.
- Q2 + Q3 ⇒ thi hành ở `V1`–`V3`; cần Packet Issue + lease mới, **chưa phiên nào được tự bắt tay**.
- Q4 ⇒ thi hành ở `V4`, và ADR-0044 khai thẳng rằng nó vượt lệnh cấm cũ ở
  `ops/THAM_DINH_CHUNG_CLAUDE_CODEX_KE_HOACH.md:96` bằng một duyệt mới, không bằng cách lờ đi.

### Cái các quyết định này KHÔNG cấp
Không quyết định nào ở trên là một lease. `V0` (#204) và mọi slice sau đó vẫn cần **Packet Issue +
lease còn hiệu lực** theo §3.2/§4. Phiên nào đọc bảng này rồi bắt tay làm là tự cấp việc — đúng thứ
`CLAUDE.md` cấm ("ĐỌC ĐƯỢC KẾ HOẠCH KHÔNG PHẢI LÀ ĐƯỢC GIAO VIỆC").

## 1. Ba bên đồng thuận tuyệt đối (không ai phản đối ở bất kỳ vòng nào)
1. **`#204` (PLAT-M4) LAND ĐẦU TIÊN.** Vá đúng 1 finding P2 (URL có `userinfo` vẫn được probe →
   `urlsplit`, từ chối khi `username`/`password` khác None) + thêm 4 hàng thiếu vào
   `ops/reviews/README.md` cho `t27` xanh. Review vòng 2/2 **trong ngân sách** (calls 2/3, rounds 1/2)
   — không nới gì. ĐO: M4 tụt sau master **0 commit**, diff đúng 2 tệp (+351/−25), nền 142/142,
   đột biến 132/132.
2. **KHÔNG land `a09aae62` (#205) hay `e071e0aa` (#207)** dưới bất kỳ hình thức nào, kể cả kèm
   "bảng đóng-finding". ĐO: biên nhận X5 neo `base_sha: a09aae62` ⇒ **721 dòng của X4 chưa verdict
   nào phủ**. Bảng đóng-finding *"ghi lại một phép đo không tồn tại"*.
3. **KHÔNG nới trần hồi tố, KHÔNG sửa đè lease/receipt đã phát hành.** Đính chính chỉ append-only.
4. **`t25` SỐNG và phải SIẾT** (đó chính là bản vá P1). ĐO hai chiều: bỏ `$NEO` khỏi lời gọi
   **wrapper** ⇒ 40/40 rc=0, KHÔNG ca nào đỏ; bỏ khỏi lời gọi `.py` ⇒ 39/40 đỏ `t25`.
   Và required status check KHÔNG phủ được nó: `ops-publish-lease.yml:42-44` là
   `on: push: branches: ['ops/**']` — đường PUSH, không phải đường PR.
5. **`t35` giữ, chỉ sửa fail-open**; phần chạy-script-thật là test hành vi, không được xoá lây.
6. **`t34` chết SAU, không chết TRƯỚC.** Xoá guard khi chốt thay thế chưa được ĐO là
   **fail-open có chủ đích**. Xoá phải nằm CÙNG COMMIT với bằng chứng readback.
7. **Neo `spec_path` + `spec_sha256`** bằng ĐÚNG cơ chế `RC_NEO=6` đang chạy cho `prompt_path`.
   ĐO: **0/9 lease có `spec_hash`**; 2 lease nhắc `spec_path` và cả hai là `null`; `ops/specs/`
   không có tệp nào cho `PLAT-*`. Lease X5 ghi thẳng `spec_note: AUTHORITY LÀ THÂN ISSUE "#206"`.
   ⇒ cả ba packet chạy trên đặc tả NGOÀI KHO, KHÔNG BĂM, SỬA ĐƯỢC KHÔNG ĐỂ VẾT. Đây là **gốc của B3**.
8. **Dời chốt quản trị vào `ops/lease_publish.py`** — cổng máy DUY NHẤT nằm trên đường lease:
   băm phải trỏ commit CÓ THẬT (ba trạng thái) · cross-provider (CHÉP logic đã có ở
   `packet_loop.py:570`, ĐO hai chiều rc=4 / rc=0) · `review_class` bắt buộc, vắng ⇒ `sensitive` ·
   `assurance_target` ∈ đúng 4 mức §8 · đổi/vượt trần phải có căn cứ · `leased_at_utc` không ở tương lai.
9. **Reservation gate**: không cấp lease reviewer khi packet hết đường vá. Fixture đỏ có sẵn:
   `plat-x5-review-1-claude` khai `attempts 2/2`.
10. **Bộ đếm hình dạng phải KẾ THỪA xuyên packet** (`hinh_dang_lap: 3` của X4 không chặn được X5 vì
    #206 là packet mới, đếm lại từ 0).
11. **ADR chốt con số canon 2/3 vòng** + `doctrine-scan so-canon` trên `ops/KE_HOACH_*.md` + xoá hai
    lời khai "ĐO ĐƯỢC" sai (`DA_PROVIDER:267-269`, `THAM_DINH_AG_T0_03:394`).
12. **Sandbox reviewer thành SCRIPT fail-đóng** (hai lượt review đầu ngày đều `blocked` và đều
    `tieu_mot_loi_goi: true` ⇒ hoàn vốn ngay lần đầu) · **sổ nợ phải là SỔ** (phản chứng sống trên
    master: `ci.yml:216` khai "NỢ CÓ TÊN" mà `NO_KY_THUAT.md` có 0 mục) · **cổng cho bước gom
    bằng chứng** (`t27` đỏ 34/35 chính vì bước gom của cuộc thẩm định này).
13. **"Không đổi gì": cả ba BÁC.**

## 2. Bất đồng còn lại — và vì sao ĐẾM PHIẾU cho kết quả SAI
Vòng 3 hai bên đổi chỗ: Fable và codex chọn **MỘT** Recovery Packet; Opus chọn **HAI** slice
(Behavior / Authority) PR vào `mission/<issue>/integration`. Phiếu 2–1 cho MỘT.

**Nhưng số liệu mà chính phe đa số đề ra lại bác phe đa số.** ĐO (`git diff --numstat 909d3e17..e071e0aa`):

| | tệp | thêm | xoá | thêm+xoá | kết cục thật |
|---|---:|---:|---:|---:|---|
| `#204` M4 | 2 | 351 | 25 | 376 | **1 vòng · 1 finding** |
| `#205` X4 | 4 | 721 | 159 | 880 | **3 vòng · 8 finding** |
| gói "MỘT packet" | 5 | 923 | 210 | **1133** | — |

- Trần **codex tự đề**: ≤ 6 tệp **VÀ ≤ 1.000 dòng thêm+xoá**. Gói một-packet = **1133** ⇒ **VƯỢT**.
  Kể cả sau khi xoá `t34` (95 dòng) ở đường A vẫn ≈ **1038** ⇒ vẫn vượt.
- Trần **Opus tự đề**: packet `sensitive` ≤ 3 tệp **VÀ ≤ 300 dòng thêm**. Gói một-packet vượt **3×**.

⇒ Hai trần độc lập, do hai bên khác nhau đặt ra, **cùng bác** gói một-packet. Đếm phiếu cho "MỘT";
đo cho "HAI". Kho này có luật cho tình huống đó.

**KHUYẾN NGHỊ CỦA PHIÊN ĐIỀU PHỐI: theo Opus — HAI slice, và điều kiện của Opus là thứ làm bất đồng tan.**

Opus tìm ra điều kiện codex chưa nêu: hai slice PR vào **`mission/<issue>/integration`**, KHÔNG vào
master. ĐO: ngày 20-08 KHÔNG có integration branch nào cho lane PLAT (chỉ `origin/mission/76/integration`
của mission cũ) và 7/8 lease khai `target = master`. Nguyên văn Opus: *"Cái chuỗi không sinh ra từ
việc chia hai packet; nó sinh ra từ việc chia hai packet mà BỎ integration branch."*
Phản đối của Fable ("hai packet trên write set giao 100% tái tạo cái chuỗi") đúng cho hai PR
chồng lên nhau; **không** đúng cho hai PR nối tiếp vào integration.

Đường cắt: **BEHAVIOR vs AUTHORITY**, không phải "sửa lỗi vs authority" của codex — vì
`ops/cai_actionlint.sh` chứa CẢ 5 sửa lỗi thật LẪN magic-bytes, nên lát cắt của codex cắt xuyên một tệp.

| slice | nội dung | tệp | ước | class |
|---|---|---:|---:|---|
| **A — Behavior** | `cai_actionlint.sh` + wrapper + `t36`–`t40` | 3 | ~+700 | `systemic` |
| **B — Authority** | 2 workflow + siết `t25` + sửa `t35` + số phận `t34` | 3 | ~+200 | `sensitive` |

Slice B là nơi **P1 nằm**, và ~200 dòng/3 tệp **vừa khít trần `sensitive`** của Opus. Đó là lợi ích
thật của việc tách, và nó lớn hơn phiền toái nối tiếp.

## 3. Thứ tự thi công — MỘT mục treo vào việc ngoài kho, mọi mục khác chạy bất kể
```
V0   #204 vá P2 + 4 hàng README → review vòng 2/2 → LAND ĐẦU TIÊN
     (KHÔNG gộp E4/C5: giữ packet sắp-sạch khỏi phình)
V0'  Đính chính append-only trần attempt X5 sau khi có trả lời Q1. KHÔNG sửa lease cũ.
     KHÔNG tiêu attempt nào trên e071e0aa.
     Ghi nợ PLAT-X5-required-status-check + don-nhanh-…-windows vào ops/NO_KY_THUAT.md
V1   Dựng mission/<issue>/integration từ master.        ← KHOÁ CHỐNG TÁI LẬP CHUỖI
V2   Slice A (Behavior)  → integration
V3   Slice B (Authority) → integration        #203/#206 chuyển `superseded`,
                                              giữ nhánh + 5 verdict + 5 receipt làm hồ sơ
V4   Gói lease_publish: spec_hash · cross-provider · băm tồn tại · 4 mức assurance ·
     đổi/vượt trần có căn cứ · timestamp · reservation gate · hình dạng kế thừa
V5   ADR canon 2/3 vòng + so-canon + xoá 2 lời khai "đo được" sai
V6   Vệ sinh: cổng cho bước gom · sandbox reviewer fail-đóng · sổ nợ là SỔ
```
**ĐƯỜNG A** (bật được required check): trong Slice B, MỘT commit duy nhất chứa cả ba — (i) bằng chứng
readback cấu hình; (ii) xoá `t34` + nửa nghĩa-vụ-YAML của `t35`; (iii) đóng mục nợ.
Lưu ý ĐO ĐƯỢC: `.claude/dev/gh_readback.py` **chỉ** readback nội dung đã đăng, **không** đọc branch
protection ⇒ phải bổ sung đường đọc hoặc dán output tay có vết. Không đọc được ⇒ **KHÔNG ĐO ĐƯỢC** ⇒
rơi sang đường B, không phải "chắc là bật rồi".

**ĐƯỜNG B** (không bật, hoặc không đo được): `t34` SỐNG, chỉ sửa MỘT docstring cho khớp 5 dạng đã ĐO
là lọt (`python -m` · `python3 -u` · shebang · `uv run` · `python -X`), kèm ca máy đòi docstring chứa
đủ 5 dạng. Không thêm một dòng cưỡng chế nào vào tệp tử tù.
**Đường B mất gì, nói bằng số:** câu hỏi "CI có thật sự chạy gate không" **vĩnh viễn không có nhà**;
`t34` bắt **3/8 = 37,5%** dạng gọi nên mỗi lần đổi cách gọi lại đẻ một finding. Nhưng với `PATH`
thiếu `actionlint` vẫn có **8 ca đỏ** ⇒ cái mất là **DETECTION**, không phải **PROTECTION**.
**Đường B KHÔNG chặn gì khác**: V0–V2, V4–V6 và toàn bộ Slice A chạy nguyên vẹn ở cả hai đường.

## 4. Điều kiện dừng — viết trước, không thương lượng lại
1. Slice A hoặc B chạm **vòng 2** mà vẫn ra một finding hình dạng S1 ⇒ **DỪNG, không vòng 3**.
   Kết luận bắt buộc: bảo đảm ấy phải đến từ required status check, không từ bộ test.
2. Bất kỳ trần nào cần nới lần nữa ⇒ **DỪNG**. ĐO: trục CALL đã đi `2→3→4→5` với **hai bậc không
   căn cứ** (`plat-x4-review-2:54` chỉ có đúng một dòng số, không một chữ biện hộ).
   Lần thứ năm phải đọc thành **trần khởi điểm đặt sai**, không thành thói quen.
3. Readback required check không đo được ⇒ đường B, KHÔNG xoá `t34`. "Đã bật rồi" ≠ "đã đo".
4. Slice B mọc trên một PR chưa merge thay vì trên integration ⇒ **DỪNG**.
5. Packet `sensitive` vượt 3 tệp / 300 dòng thêm mà spec không khai lý do ⇒ DỪNG và tách.
6. V4 gặp hình dạng "một dạng khai báo mới lách chốt khai báo" quá 2 lần ⇒ DỪNG, xét lại chính V4.
7. Không đọc được Issue/Packet durable facts ⇒ dừng fail-closed.
8. Không đổi prompt / session / tên packet để mở thêm vòng.
9. Mọi lease mới thiếu `spec_path` + `spec_sha256` ⇒ rc=6, KHÔNG NGOẠI LỆ — kể cả Slice A/B,
   chúng là packet ĐẦU TIÊN phải có spec đóng băng.

## 5. Điều khoản khoá của bản này
Nguyên văn Opus, giữ nguyên: *"mọi mục ở đây chỉ sống nếu nó có `rXX_` và một đột biến đổi màu,
không phải vì nó nằm trong danh sách này."*
Căn cứ: bẫy B1 (`$?` sau pipe) tái phát **BA lần trong MỘT ngày** với **ba bên đã đọc bài học** —
phiên điều phối hôm 20-08, Fable 5 (tự khai đầu bản vòng 2), và phiên điều phối lần nữa khi đo chốt
cross-provider. ⇒ Kết luận không còn là "người thực thi ẩu"; nó là phép đo về **hiệu lực của việc
công bố bằng CHỮ**. Mọi đề xuất dạng "ghi thêm vào CLAUDE.md / thêm chốt vào SKILL" phải kèm một ca
`rXX_` chạy được, nếu không nó là chỗ các ca đi chết.

## 6. Chưa đo được — chung cho cả ba bên
GitHub facts (thân Issue #194/#203/#206 = **authority thật sự** của cả ba packet; PR; comment id) ·
branch protection / required contexts (thứ toàn bộ đường A dựa vào) · **"CI xanh trên `e071e0aa`"
vẫn CHƯA có nguồn độc lập** — reviewer chép từ packet và tự khai như vậy · Windows (mọi thí nghiệm
chạy trên Linux; `N/N` của bước Windows chưa ai đọc được vì `get_job_logs` chỉ trả phần ĐUÔI) ·
**thiên lệch môi trường**: container thẩm định CÓ `actionlint 1.7.7` ở `/usr/local/bin`, runner
GitHub thì không ⇒ kết luận "8 ca đỏ trên runner thật" là suy từ phép đo PATH sạch + ĐỌC ·
chi phí hai chiều (không có token/thời lượng cho 4 lượt codex-review) · `packet_loop` có được chạy
với state dir ngoài kho không (đo được VẮNG THAM CHIẾU, không đo được vắng SỬ DỤNG) ·
sáu kích hoạt drift §5.1 với 3 commit master mới.
