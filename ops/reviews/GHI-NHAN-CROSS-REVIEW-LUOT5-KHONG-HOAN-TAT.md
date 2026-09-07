# Ghi nhận — cross-review LƯỢT 5 KHÔNG HOÀN TẤT (hạ tầng), `ducthangho/tra-luat`

**Đây KHÔNG phải verdict và KHÔNG phải biên nhận.** Không có `*.receipt.yaml` đi kèm, và
`assurance` của bốn packet `LO-319` · `GATE` · `2A` · `2B` **vẫn dừng ở lượt 4**
(`changes_requested`, 1 P1 / 0 P2 / 1 P3 trên `e5ab4b7`). Tệp này ghi lại **vì sao** lượt 5 không
kết luận được, và **cái gì đã đo được** trước khi nó chết — để phiên sau không trả tiền lại.

## Năm lần chạy, năm lần chết, MỘT nguyên nhân

| lượt | run | bắt đầu (UTC) | chết | sống được | kịp ghi gì |
|---|---|---|---|---|---|
| 4 (lần đầu) | — | 06-09 ~22:5x | disconnect | — | log giữ ở `rv4/run-luot-chet/` |
| 5a | `cccdb19a` | 07-09 00:58:08 | 01:08:02 | 9 ph 54 s | 419 ca tấn công H, 3 cổng ngắn |
| 5b | `901fe63f` | 07-09 01:57:42 | 02:04:38 | 6 ph 56 s | log thô |
| 5-A | `9a972322` | 07-09 ~02:37 | ~02:40 | ~3 ph | `VERDICT-A.md` (bản dở) |
| 5-B | `e11fce32` | 07-09 ~02:37 | ~02:40 | ~3 ph | `VERDICT-B.md` (bản dở) + 3 cổng chạy lại |
| 5-C | `2d47884a` | 07-09 ~02:37 | ~02:40 | ~3 ph | `VERDICT-C.md` (bản dở) + `recompute.py` |

Chữ ký giống nhau từng chữ ở cả năm:

```
ERROR codex_api::endpoint::responses_websocket: failed to connect to websocket:
  IO error: Connection refused (os error 111), url: wss://chatgpt.com/backend-api/codex/responses
{"type":"error","message":"Reconnecting... 2/5 (stream disconnected before completion...)"}
```

**Nguyên nhân đo được — và nó nằm trong TÀI LIỆU, không phải giả thuyết.** Proxy egress của
container remote này khai thẳng ở `/root/.ccr/README.md`, mục *"Not supported through the proxy
(report, do not work around)"*: **`WebSocket upgrades`**. Đường TÁI KẾT NỐI của `codex` dùng
`wss://`, nên **một cú cắt luồng tạm thời biến thành cú chết vĩnh viễn**.

Ba phép loại trừ, để không đổ lỗi nhầm:

- **KHÔNG phải đường codex bị chặn** — probe `codex exec` ngắn lúc 01:57Z và 02:17Z đều
  `turn.completed` với token thật, `rc=0`.
- **KHÔNG phải OOM / hết đĩa** — `free -m` 15,4 GB trống; `df` 29 G trống, tại thời điểm chết.
- **KHÔNG phải bộ lọc nội dung** — không lượt nào có `flagged`; cả năm chết đúng ở tầng vận chuyển.

### Bản vá đã thử, và vì sao nó KHÔNG được tính là bản vá

Truyền `-c features.responses_websockets=false` (và `_v2`) ⇒ `rc=0`. **Phép thử ấy vô nghĩa**, và
nói thẳng ra đây vì nó là đúng bài học *"hỏi bộ quét một ca mà bạn biết trước đáp án"*: khoá **bịa
đặt** `features.khong_he_ton_tai_xyz123` **cũng** cho `rc=0`, và rollout không ghi `features` ⇒
codex nhận im lặng mọi khoá, kể cả khoá không tồn tại. Cờ vẫn được truyền ở lượt 5-A/B/C nhưng
**không có bằng chứng nào nói nó có hiệu lực**.

### Bản vá THẬT: đổi HÌNH DẠNG công việc, không đổi provider

Sau cú chết thứ ba, năm nhiệm vụ được chia thành **ba mảnh độc lập**, mỗi mảnh một sandbox và một
`cay-kho` riêng, chạy song song, kèm chỉ thị *"ghi kết quả ra đĩa NGAY khi có, đừng dồn tới cuối"*.
Kết quả đo được: **cả ba mảnh đều chết, nhưng cả ba đều kịp ghi tệp verdict** — trong khi 5a và 5b
chạy lâu gấp đôi mà **không** để lại verdict nào. Đó là cải thiện có thật, và nó **không** giải
quyết nguyên nhân gốc.

## Cái ĐÃ ĐO ĐƯỢC — và nó có giá trị độc lập

### 1. Lượt 5a: bộ tấn công H do CHÍNH reviewer viết

`attack-h.json`: **163 ca** `failures: []` · **256 ca vét cạn** `exhaustive_failures: []` ⇒ **419 ca,
0 hỏng**. Cộng một lập luận độc lập rằng `bool(cap)` LUÔN True khi tới nơi ⇒ **xác nhận lời khai của
executor rằng `mH13` là mã chết**.

**Đọc đúng mức:** `419` ca không hỏng là bằng chứng về **BỘ CA**, không phải bằng chứng H đúng —
bốn bộ ca đều do bên bị đo và bên đo cùng nghĩ ra. Reviewer chỉ có ~10 phút trước khi chết, và ba
lượt trước nó hạ được A-c và T' bằng ca mà bộ ca trước đó **không có**.

### 2. Lượt 5-C: tái tính ĐỘC LẬP, khớp từng chữ — rồi bắt được BA lỗi của phiên điều phối

Tái tính từ `mruns_all.tsv` cho `n=9 · min 40,20 · max 49,62 · biên độ 9,42 · trung vị 45,58 ·
trung bình 45,08` — **khớp đặc tả từng chữ**. Kiểm toàn vẹn hiện vật: 43 hàng, 9 cột đều, dòng dài
nhất 78 ký tự, có newline cuối, 28 run duy nhất, 0 cặp trùng ⇒ **không bị cắt**.

Ba lỗi nó bắt được, **đều là lỗi của phiên điều phối**, đều đã vá ở commit mang tệp này:

| # | lỗi | bản vá |
|---|---|---|
| 1 | `mruns_all.tsv` chỉ có thời lượng **JOB** ⇒ bảng tỉ lệ theo **BƯỚC** **không tái tính được** từ hiện vật. Reviewer bị đòi kiểm một bảng mà không được cho dữ liệu để kiểm. | hiện vật mới **`buoc_master.tsv`**: 12 cột, **một hàng mỗi BƯỚC**, 2.062 hàng, giây thô, `KHONG_DO_DUOC` fail-close |
| 2 | Tỉ lệ in như số chính xác trong khi nguồn ghi theo **GIÂY** ⇒ trung vị `8,01×` thật ra nằm trong `7,92–8,06`; max `9,74×` nằm trong `9,71–9,85`. | bảng tỉ lệ nay có cột **dải làm tròn** (`±0,5` giây mỗi số) |
| 3 | Bộ trích số chỉ thấy **chữ số ASCII** ⇒ lọt đúng dòng chứa *"**bảy** lượt"* viết bằng chữ — đúng thiên vị đã tự khai mà vẫn để nguyên. | `trich_so` v5 bắt cả số viết bằng chữ: **1.498 → 1.899** hàng, 1.059 hàng có số viết bằng chữ |

### 3. Lượt 5-B: ba cổng ngắn chạy lại, khớp thông điệp commit

`doctrine-scan` sạch 7 tệp / 0 chỗ chép · `adr-song` 46/46 · `doc-claims-check --strict` `"ok": true`
106 tệp. Kèm một chi tiết thông điệp `2f68617` **bỏ sót**: `adr-song` **tha** ADR `0016` thiếu dòng
trạng thái.

### 4. Nền master TRÔI nhanh hơn tốc độ viết đặc tả — đo hai lần cách nhau 2 giờ 4 phút

| | 00:45:22Z | 02:49:51Z | đổi |
|---|---:|---:|---|
| `n` job Windows `success` | 9 | **11** | +2 head mới |
| biên độ | 9,42 | **10,28** | **+0,86** |
| biên dưới trần 60 | 10,38 | **9,52** | **−0,86** |

Không con số nào sai lúc viết; chúng **hết hạn**, theo chiều XẤU ĐI. Chi tiết ở
`ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md` mục *"ĐO LẠI"*.

## Cái CHƯA AI KẾT LUẬN — nói thẳng

- **§12** (bộ đếm 3/4 · Đ1–Đ5 có đo được không · ba lựa chọn có đủ không) — mảnh B chết trước khi
  kết luận. Câu hỏi *"có nên tiếp tục cách làm này"* **vẫn thuộc chủ kho**, chưa có reviewer khác
  nền nào trả lời.
- **Tấn công H có kết luận** — mảnh A ghi `blocked`/"bản đang đo", không phải `approve` cũng không
  phải `changes_requested`.
- **P1 `span-rong-nuot-ti-le-vo-can`** của lượt 4 — mảnh A đang kiểm thì chết. **Coi như VẪN MỞ.**
- **`uoc-kich-thuoc-lo-con-tinh-nhan-ac`** [P3] — mảnh A kịp ghi `ĐÃ VÁ THẬT` (đo lại T' `21+26`,
  H `21+29`), là kết luận DUY NHẤT hoàn chỉnh của lượt 5.
- **`hint_provenance` 4 hunk bị bác** — chưa ai kiểm bốn lý do ấy.

## Đường đi tiếp

Bốn packet **chưa đủ điều kiện `cross_approved`**. Đường chắc chắn nhất là chạy lại lượt 5 **ngoài
container này** — sandbox đã dựng sẵn và chạy được nguyên trạng:

```
scratchpad/rv5/phan-{A,B,C}/     # mỗi mảnh: PROMPT.md · CHUNG.md · cay-kho (detached 2f68617)
scratchpad/chay_manh.sh A|B|C    # đúng lệnh đã dùng, neo --expected-head + --expected-prompt-sha256
```

**KHÔNG** hạ xuống review cùng nền (Claude) để cho xong: bảo chứng sẽ tụt từ `cross_approved` xuống
`same_provider` — đúng thứ mà chuỗi packet này sinh ra để tránh.

## Hiện vật

Toàn bộ ở scratchpad phiên `session_0186nh13XYsStVs1usBCsx5Y`, **KHÔNG trong kho** (chúng là log và
số đo, không phải nguồn có thẩm quyền): `rv5/run-luot-chet-5{,b}/` · `rv5/luot-chet-5-artifacts/` ·
`rv5/phan-{A,B,C}/VERDICT-{A,B,C}.md` · `rv5/phan-{A,B,C}/review-*/` · `buoc_master.tsv` ·
`so-lieu-trich-may-v5.tsv` · `do_buoc_v2.py` · `tinh_lai.py`.

## Phụ lục — FULL-GATE, chạy ĐÚNG MỘT LẦN ở cuối, đo DELTA

Chủ kho đặt: *"đừng chạy gate dài cho tới khi hết P1; chỉ chạy full-gate 1 lần ở cuối."* P1 chưa
hết (lượt 5 không kết luận), nên phép đo này trả lời câu hẹp hơn và nói rõ như vậy: **bản vá tài
liệu có làm hỏng cổng nào không** — đo **DELTA so `origin/master`**, không đòi `rc=0` tuyệt đối.

Hai vế dựng trong **MỘT lệnh, hai vòng lặp, cùng các bước, chạy liền nhau** (bài học *"rig tự đẻ
hồi quy không tồn tại"*): `nen = origin/master = d28c4b1` · `sau = HEAD = 7eb1145`.

| cổng | nền `d28c4b1` | sau `7eb1145` | delta |
|---|---|---|---|
| `ci_dang_ky_test` | `rc=0` · **51/51** phản chứng | `rc=0` · **51/51** | **0** |
| `packet_loop_test` | `rc=0` · **78/78** lớp lách · 219 s | `rc=0` · **78/78** · 204 s | **0** |
| `lease_publish_test` | `rc=1` · **120/121**, chạy 121 bỏ qua 0 | `rc=1` · **120/121** | **0** |
| `doctrine-scan` | `rc=0` | `rc=0` | **0** |
| `adr-song` | `rc=0` 46/46 | `rc=0` 46/46 | **0** |
| `doc-claims-check --strict` | `rc=0` `"ok": true` 106 tệp | `rc=0` `"ok": true` 106 tệp | **0** |

`lease_publish_test rc=1` là **ĐỎ SẴN trên master**, không phải hồi quy: cùng một ca
`t33_workflow_dang_lease_phai_qua_actionlint`, cùng `120/121`, cùng 29 dòng đỏ ở cả hai vế.
`diff` hai bản in cho 34 dòng lệch; sau khi chuẩn hoá tên thư mục tạm ngẫu nhiên (`lp_XXXXXXXX`)
còn **0 dòng** ⇒ toàn bộ là nhiễu của rig.

`doc-claims-check` `advisory_count` **367 → 363**: bản vá **bớt** 4 advisory, `ok: true` cả hai vế.

### Lượt chạy full-gate ĐẦU TIÊN là một CỔNG XANH GIẢ — ghi lại vì nó đắt

Script bản đầu bọc mỗi suite bằng `/usr/bin/time -f ... -o ...`. Nhị phân ấy **không có** trong
container ⇒ cả sáu lượt trả `rc=127`, **suite chưa từng chạy**, và vì `rc` hai vế **giống hệt
nhau** nên phép so DELTA in ra *"khớp từng dòng"*. Nếu dừng ở mã thoát thì đã kết luận
"full-gate sạch" trong khi **không một dòng test nào chạy**.

Thứ bắt được nó **không** phải mã thoát mà là **kích thước đầu ra**: `out=0B` cho cả sáu. Đúng
doctrine của kho — *"cổng xanh nhờ `rc=0` là cổng CÓ THỂ BỊ LỪA; phải đòi BẰNG CHỨNG DƯƠNG
(`N/N` với hai số BẰNG NHAU)"* — và đúng họ với ca `param([string[]]$Args)` ở `r244`:
`rc=0` + output rỗng. Bảng trên vì vậy in **cả hai số** của mỗi suite, không in mã thoát suông.
