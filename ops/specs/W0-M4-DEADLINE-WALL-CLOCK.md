# ĐẶC TẢ PACKET — `W0-M4-DEADLINE-WALL-CLOCK`

```yaml
packet_id: W0-M4-DEADLINE-WALL-CLOCK
revision: 1
generation: 1
review_class: sensitive        # sua co che CUONG CHE han chot cua launcher
executor: codex
reviewer: claude
assurance_target: cross_approved
nen_bat_buoc: windows          # xem §6 — KHONG do duoc tren Linux mot minh
```

> **CHƯA CẤP LEASE.** Write set đang bị packet #359 giữ (xem §1). Đặc tả soạn sẵn theo lệnh
> chủ kho 28-08-2026 (*"soạn W0-M4 sẵn đi"*), để khi khoá mở là cấp lease và chạy được ngay.

## 0. Vấn đề — đọc mã, rồi đo, và cả hai đều nói cùng một chuyện

### 0.1 Cơ chế hiện tại, nguyên văn

`launcher.py` tính thời gian còn lại **ĐÚNG MỘT LẦN**, rồi giao cả phần chờ cho `Popen.wait`:

```python
han = _doc_iso(kq["deadline_utc"]) if kq["deadline_utc"] else None
...
con_lai = (han - _bay_gio()).total_seconds()
ma = p.wait(timeout=max(0.0, con_lai))
```

`_bay_gio()` là `datetime.now(timezone.utc)` — **đồng hồ TƯỜNG**. Nhưng `Popen.wait(timeout=…)`
đếm ngược bằng đồng hồ **ĐƠN ĐIỆU** của Python (`time.monotonic`, trên Linux là
`CLOCK_MONOTONIC`).

**Hai đồng hồ khác nhau, và chúng KHÔNG cùng chạy khi máy ngủ.** Đo trên nền này:

```
nen                     : Linux
time.CLOCK_MONOTONIC    : co   <- Popen.wait dem bang cai nay; KHONG chay khi may ngu
time.CLOCK_BOOTTIME     : co   <- CO chay khi may ngu
time.CLOCK_REALTIME     : co   <- dong ho TUONG, cai ma --deadline-utc noi toi
BOOTTIME - MONOTONIC    : 0.000s   (container nay chua tung ngu — nen 0 la DUNG,
                                    khong phai bang chung hai dong ho la mot)
```

Máy ngủ `N` giây giữa chừng ⇒ `CLOCK_MONOTONIC` đứng yên `N` giây ⇒ tiến trình con được
**thêm `N` giây thời gian TƯỜNG** ngoài hạn chót. Hạn chót mang tên `--deadline-utc` —
tên nó nói **UTC**, tức thời gian tường — mà cơ chế cưỡng chế lại là một đồng hồ dừng khi ngủ.

Đây đúng hình dạng kho đã đặt tên: **lời khai rộng hơn cơ chế**. Không phải "hơi lệch vài
giây": một máy xách tay gập lại qua đêm cho sai số **hàng giờ**.

### 0.2 Sổ không ghi gì để phát hiện

```
wall_elapsed_seconds        0 lan trong launcher.py
working_elapsed_seconds     0
working_clock               0
timeout_clock               0
QueryUnbiasedInterruptTime  0
```

`run.json` hôm nay chỉ có `thoi_luong_giay` — **một** con số, không nói nó đo bằng đồng hồ nào.
Nên khi chuyện trên xảy ra, **không có dấu vết nào** để ai đó phát hiện. Cùng bệnh với
`probe_bo_qua` của packet #363: thiếu một trường làm một sai lệch trở thành vô hình.

### 0.3 Cái KHÔNG hỏng — nói ra để đừng ai "sửa" nhầm

`_giet_cay`, phân biệt `124` (đã giết trọn cây) với `125` (quá hạn mà KHÔNG giết được), chốt
zombie, chốt `khoa is None`: **đều đúng và đã có phản chứng**. Packet này **không đụng** chúng.
Nó chỉ sửa *lúc nào* quyết định "quá hạn", không sửa *làm gì sau khi quá hạn*.

## 1. `write_set` — VÀ NÓ ĐANG BỊ CHẶN

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

Đo 28-08-2026 (`ai-dang-giu`, sau khi so hai nguồn bằng TẬP TÊN 237=237, `comm` hai chiều RỖNG):

```
.claude/dev/launcher.py       rc=11  NGUOI_GIU 2: mcp-doc-phan-tich-exec-1r3-codex-20260828,
                                                  probe-agent-exec-1-codex-20260828
.claude/dev/launcher_test.py  rc=11  (y het)
```

`mcp-doc-phan-tich-exec-1r3` = packet **#359**, hết hạn `2026-08-28T17:05:00Z`, **CÒN HIỆU LỰC**.
`probe-agent-exec-1` = packet **#363**, đang chờ cùng lý do.

**ĐIỀU KIỆN CẤP LEASE:** cả hai đường trả `rc=0 / NGƯỜI_GIỮ 0`, **và quét LẠI ngay trước khi
đăng** — không dùng kết quả quét cũ. Lease #363 được cấp sau một lần quét sạch lúc 02:05Z rồi
lease #359 land lúc 02:23Z, đúng cửa sổ giữa quét và đăng; không cổng nào canh cửa sổ ấy.

Ba packet cùng xếp hàng trên hai đường này: **#359 → #363 → W0-M4** (và W1-P1). Thứ tự do chủ
kho quyết, không phải do packet nào tự nhận.

## 2. `ngan_sach_kich_thuoc`

| | |
|---|---|
| tệp tối đa | **2** |
| dòng thêm tối đa | **260** |

## 3. Hợp đồng

### 3.1 Chờ theo LÁT, so lại hạn TƯỜNG mỗi lát

Thay một lần `p.wait(timeout=con_lai)` bằng vòng lặp lát ngắn:

```
lap:
    con_lai = (han - <dong ho TUONG>()) .total_seconds()
    neu con_lai <= 0        -> QUA HAN, di tiep nhanh giet-cay DA CO
    lat = min(LAT_GIAY, con_lai)
    thu p.wait(timeout=lat) -> xong thi thoat vong
    (TimeoutExpired -> lap lai)
```

`LAT_GIAY` là hằng **có tên**, mặc định **5.0**, và phải nêu đánh đổi trong chú thích: lát ngắn
bắt được ngủ sớm hơn nhưng đánh thức tiến trình cha thường xuyên hơn.

**Chốt chống hồi quy:** `han is None` (không đặt hạn) vẫn phải là `p.wait()` **chặn vô hạn**,
không phải vòng lát — đừng biến một lượt không hạn thành vòng bận.

### 3.2 HAI đồng hồ, và cả hai phải BƠM ĐƯỢC

- **`dong_ho_tuong`** — mặc định `datetime.now(timezone.utc)`. Đây là đồng hồ **cưỡng chế hạn**;
  `timeout_clock` trong sổ luôn là `"wall"`.
- **`dong_ho_thuc`** — thời gian máy THỨC, chỉ để **GHI SỔ**, KHÔNG cưỡng chế gì.

Cả hai nhận qua đối số (mặc định là thật) để phản chứng bơm được. Một hàm chỉ đọc đồng hồ hệ
thống thì ca của nó không tồn tại.

### 3.3 `dong_ho_thuc` theo NỀN — bảng CHO PHÉP, thiếu thì khai THIẾU

| nền | nguồn | `working_clock` ghi |
|---|---|---|
| Linux | `time.clock_gettime(time.CLOCK_MONOTONIC)` — không chạy khi ngủ | `"CLOCK_MONOTONIC"` |
| Windows | `QueryUnbiasedInterruptTime` (kernel32), **sau khi probe symbol an toàn** | `"QueryUnbiasedInterruptTime"` |
| còn lại / probe hỏng | — | `null` |

**Trên Windows KHÔNG được dùng `time.monotonic()` làm đồng hồ thức**: ở đó nó là
`GetTickCount64`, và cái ấy **CÓ** chạy khi ngủ — dùng nó là ghi một con số sai mang nhãn đúng.
Cũng không dùng QPC.

`working_clock = null` ⇒ `working_elapsed_seconds = null`. **Không suy, không ước lượng, không
lấy wall thay thế.** `null` ở đây nghĩa là KHÔNG ĐO ĐƯỢC, và nó khác `0`.

**Ba luật đụng API riêng nền — kho đã trả giá bằng một suite `0/103` trên Windows:**

1. `hasattr`/`getattr(..., mặc_định)` **trước** khi đụng; probe symbol trước khi gọi.
2. Truyền **lambda** vào hàm bọc lỗi, đừng truyền thẳng hàm — tra thuộc tính xảy ra **TRƯỚC**
   lời gọi, tức **NGOÀI** `try`.
3. Gán thêm một API mà nền vốn không có thì phải **gỡ lại** khi ra khỏi chốt.

### 3.4 Sổ `run.json` — bốn trường mới

```
wall_elapsed_seconds     : float   luon co
working_elapsed_seconds  : float | null
working_clock            : "CLOCK_MONOTONIC" | "QueryUnbiasedInterruptTime" | null
timeout_clock            : "wall"            HANG, de nguoi doc so biet han duoc cuong che
                                             bang dong ho nao ma khong phai doc ma
```

Giữ nguyên `thoi_luong_giay` đang có (đã có người đọc); **không** đổi ý nghĩa nó.

### 3.5 KHÔNG đụng

Ngữ nghĩa `124`/`125`, `_giet_cay`, chốt zombie, chốt `khoa is None`, `MA_PROBE`, `MA_WORKTREE`.
Packet này chỉ đổi **lúc nào** kết luận quá hạn.

**Và nó chỉ GHI bằng chứng — KHÔNG tự `void-attempt`.** Tự động phân loại một lượt là "vô hiệu
vì máy ngủ" cần Packet riêng và phản chứng riêng ở seam packet-loop.

## 4. Phản chứng

### 4.1 Hai ca kế hoạch đòi

1. **Đồng hồ tường GIẢ nhảy qua hạn trong khi tiến trình còn sống** ⇒ quá hạn, giết cây, `124`
   (hoặc `125` nếu không giết trọn). Ca này chứng minh vòng lát **có** so lại mỗi lát — bản cũ
   sẽ chờ hết `con_lai` đã tính một lần và **không** bắt được cú nhảy.
2. **Đồng hồ thức GIẢ đứng yên trong một quãng "ngủ" mô phỏng** ⇒ `wall_elapsed_seconds` **lớn
   hơn** `working_elapsed_seconds`, và chênh lệch ≈ quãng ngủ.

### 4.2 Ca chống hồi quy và chống chặn oan

3. `han is None` ⇒ chờ chặn vô hạn, **không** vào vòng lát (đo bằng số lần gọi đồng hồ giả).
4. Tiến trình xong **giữa** hai lát ⇒ trả mã thật của con, **không** thành quá hạn.
5. `con_lai <= 0` ngay từ đầu (hạn đã qua lúc phóng) ⇒ quá hạn ngay, không chờ một lát nào.
6. `working_clock = null` ⇒ `working_elapsed_seconds` là `null`, **không** phải `0`, và **không**
   phải bản sao của wall.

### 4.3 Ca NỀN — và đây là chỗ kho đã trả giá

7. Trên nền không có `QueryUnbiasedInterruptTime`: đường Windows phải trả `null` **êm**, không
   ném. Đo bằng cách giả `platform.system() == "Windows"` mà symbol vắng.
8. **Ca bị BỎ QUA trên một nền KHÔNG phải "ca còn sống".** Runner đột biến phải tách
   `killed / survived / not-run / skipped`; skip **không** tính killed, và **mọi ca đích bị bỏ
   qua** ⇒ báo LỖI *"đột biến không đo gì"*, đừng báo ok.

### 4.4 Đột biến — mỗi chốt một cái, giết ĐÚNG và CHỈ ĐÚNG tập khai

| đột biến | phải giết |
|---|---|
| bỏ vòng lát, quay lại `p.wait(con_lai)` một lần | ca 1 |
| lát không so lại hạn (tính `con_lai` ngoài vòng) | ca 1 |
| `dong_ho_thuc` lùi về `time.monotonic()` trên nhánh Windows | ca 2 hoặc ca 7 |
| `working_elapsed` khi không đo được ghi `0` | ca 6 |
| `timeout_clock` ghi `"monotonic"` | ca sổ |
| `han is None` cũng đi vòng lát | ca 3 |

Nền có ca ĐỎ ⇒ **TỪ CHỐI công bố điểm đột biến**.

## 5. Cổng, và NỀN đã đo sẵn

```
git config core.abbrev 7
python3 .claude/dev/launcher_test.py
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 .claude/dev/packet_loop.py adr-song --root .
python3 scripts/tl.py doc-claims-check --strict --json
python3 scripts/tl.py workflow-audit  --strict --json
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 ops/lease_publish_test.py
```

**Nền đo 28-08-2026 trên `origin/master`:**

```
launcher_test : 154/154 ca DA CHAY QUA (tong 155, bo qua 1, hong 0)
                - KHONG DU: 1 ca BO QUA, chua do gi
                (t62: fixture Windows; ban POSIX la t63)
lease_publish : 114/114  CHI KHI co actionlint 1.7.7 + shellcheck 0.10.0 tren PATH.
                Thieu hai cong cu => 95/114 — MOI TRUONG, khong phai hoi quy.
```

## 6. WINDOWS — packet này KHÔNG kết thúc được trên Linux

`QueryUnbiasedInterruptTime` chỉ chạy thật trên Windows. Trên Linux mọi ca đụng nó **bị bỏ qua**,
và §4.3 ca 8 nói rõ: bỏ qua **không** phải đạt.

Chủ kho đã ngỏ ý cho chạy trên máy Windows của họ (28-08-2026). Ghi nhận và nói đúng điều kiện:

- CI có ma trận Windows, nhưng **PR thường chỉ chạy `ubuntu`**;
- **gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ**: `ci.yml` khai `pull_request:` mà **không**
  khai `types:`, nên mặc định chỉ bắn ở `opened`/`synchronize`/`reopened` — **`labeled` không nằm
  trong đó**. Gắn nhãn không sinh lượt chạy nào; ma trận chỉ đọc nhãn ở lượt bắn KẾ TIẾP;
- đường **CHẮC CHẮN** là gọi tay `workflow_dispatch` trên đúng ref, hoặc đẩy thêm một commit sau
  khi đã gắn nhãn;
- chạy trên máy Windows của chủ kho là **đường thứ ba**, và nó cho thứ CI không cho: một lần ngủ
  THẬT. Nếu dùng đường ấy, biên bản phải ghi **máy nào, phiên bản Windows nào, ai chạy** — một
  phép đo trên máy cá nhân mà không ghi danh tính máy thì lượt sau không tái lập được.

**Điều kiện hoàn tất có Windows:** `launcher_test.py` trên Windows phải `N/N` với **0 ca bỏ qua
trong nhóm W0-M4**. Còn ca bỏ qua trong nhóm ấy ⇒ **chưa xong**, dù Linux xanh.

## 7. Điều KHÔNG được làm

- không đổi ngữ nghĩa `124`/`125`, không đụng `_giet_cay`;
- không dùng `time.monotonic()`/QPC làm đồng hồ THỨC trên Windows;
- không lấy wall thay cho working khi không đo được — `null`, và `null ≠ 0`;
- không tự `void-attempt`; packet này chỉ GHI bằng chứng;
- không đụng đường nào ngoài `write_set`;
- nghĩ ra được một hướng hỏng thì **biến ngay thành ca `rXX_`**, đừng để trong chú thích.

## 8. Cái packet này KHÔNG chữa

Nó **không** làm hạn chót đúng khi **đồng hồ tường bị chỉnh** (NTP nhảy, người sửa giờ). Đồng hồ
tường là thứ `--deadline-utc` chọn làm chuẩn, nên chỉnh giờ vẫn đổi hạn — đó là **thuộc tính của
hợp đồng**, không phải lỗi. Muốn miễn nhiễm cả chuyện ấy thì cần một hợp đồng hạn chót khác, và
đó là packet khác. Ghi ra đây để không ai đọc W0-M4 mạnh hơn nó.
