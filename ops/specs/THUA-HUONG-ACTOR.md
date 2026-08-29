# THUA-HUONG-ACTOR — bộ test lease_publish thừa hưởng môi trường thay vì tự dựng

**Mọi con số dưới đây đo lúc `2026-08-29T08:46:44Z` trên `origin/master = c0cdad1e`.**
L5: ĐO LẠI trước mỗi bước công bố (đăng băm · cấp lease · merge). Con số đúng lúc viết vẫn sai lúc đọc.

| trường | giá trị |
|---|---|
| `packet_id` | `THUA-HUONG-ACTOR` |
| `packet_issue` | **CHƯA MỞ** — nợ nguồn là [#395](https://github.com/ducthangho/tra-luat/issues/395) mục **N0**. Spec này KHÔNG giao việc; §3.2 đòi Packet Issue riêng + lease. |
| `review_class` | `sensitive` |

## `nguon_cap_viec`

Packet **khắc phục**. Không trỏ dòng kế hoạch nào — nó sinh ra từ một sự cố đo được, không từ lộ trình.

- Nợ mẹ: `#395` mục **N0** (đăng `2026-08-29T~08:35Z`).
- Hiện vật tiền nhiệm: `pull/392#issuecomment-5461264141` — biên bản land #392.
- Khuyết tật do packet `#386` `CONG-DUYET-THEO-THAM-QUYEN` land ở `c0cdad1e` sinh ra: cổng thẩm quyền
  mới đọc `GITHUB_ACTOR`, và bộ test `lease_publish` thừa hưởng biến ấy nên verdict của nó phụ thuộc
  **ai đẩy commit**.

## `review_class` — vì sao `sensitive`

Write set là bộ test của **cổng write-set exclusion** — thứ duy nhất chặn hai writer trên một tệp.
§8 xếp `review/land authority` vào `sensitive`; lease tiền nhiệm (`bia-mo-mot-chieu-exec-1r2`) đã phân
đúng lớp ấy cho cùng vùng mã. Không rõ thì lấy mức chặt nhất ⇒ `sensitive`.

`risk: normal` — `ops/**` là dev-side, KHÔNG vào gói phát hành.

## `write_set`

```
ops/lease_publish_test.py
```

**MỘT đường dẫn.** Bản vá là test-side (quyết định Q3), nên `ops/lease_publish.py` KHÔNG cần đụng.

> **ĐIỀU KIỆN DỪNG.** Executor thấy buộc phải sửa `ops/lease_publish.py` để đạt bất kỳ mục tiêu nào
> ⇒ **DỪNG và khai**, KHÔNG tự nới write set. Khi ấy quyết định Q3 đã sai và việc phải làm đã đổi.

**VA CHẠM ĐANG CÓ — đọc trước khi cấp lease.** Đo `08:46:44Z`: `ai-dang-giu ops/lease_publish_test.py`
→ `rc=11`, `NGƯỜI_GIỮ 1 = thu-hoi-lease-exec-1-codex-20260828` (packet `#385`, **PR #388 ĐANG MỞ**,
`lease_expires_at_utc: 2026-08-29T12:20:00Z`). Write set giao nhau **100%** — đúng một đường, không
thừa không thiếu.

Nên packet này là **KẾ NHIỆM của `#385`**: chỉ mở sau khi `#388` land. Chờ lease hết hạn `12:20Z`
rồi chen vào là lách theo ĐỒNG HỒ chứ không theo thực tế — nhánh `codex/thu-hoi-lease-exec-1` vẫn
sống, và khi ấy có hai writer thật.

## `ngoai_pham_vi` — cố ý KHÔNG làm

1. **Không sửa `ops/lease_publish.py`.** Đọc `os.environ` trực tiếp là hành vi ĐÚNG cho môi trường
   thật; khuyết tật nằm ở bộ test. Sửa cổng là tăng bán kính rủi ro của một packet `sensitive` để
   chữa một lỗi không nằm ở đó.
2. **Không chặn bot `ops-publish-lease` ghi ngược `posted_comment_id`.** Đó là nguyên nhân KÍCH HOẠT
   (đã hỏng 4 lần; nay không chỉ giết bản duyệt mà còn làm đỏ gate), nhưng nó ở
   `.github/workflows/ops-publish-lease.yml` — tệp khác, sẽ thành 2 tệp và là một lớp rủi ro khác.
   Tách thành packet riêng; ghi vào `#395` làm **N4**.
3. **Không đụng `t16`/`t17`** (nợ `#395` N2/N3) — khác tệp, khác packet.
4. **Không sửa ADR-0041** dù đây là lần thứ ba liên tiếp phải viết `NGOAI_LE_ADR_0041`. Ba lần cùng
   một hình dạng là dấu hiệu nên sửa điều khoản; việc ấy thuộc thẩm quyền chủ kho, không thuộc packet này.

## `muc_tieu`

Mỗi mục chiếu vào `ops/lease_publish_test.py` — đường dẫn DUY NHẤT trong write set (L2).

| # | mục tiêu |
|---|---|
| **M1** | Mọi chỗ dựng môi trường con chuyển từ **kế thừa** (`dict(os.environ, ...)`) sang **tự dựng** (`clear=True` + tập biến tối thiểu tường minh). Đo `08:46:44Z`: **15** chỗ `dict(os.environ` · **2** chỗ `clear=True`, đơn vị = **lần xuất hiện chuỗi trong tệp**. |
| **M2** | Ca meta **bất biến lúc chạy**: chạy trọn suite dưới ≥3 giá trị `GITHUB_ACTOR` khác nhau, đòi kết quả GIỐNG HỆT. Chốt CHÍNH. |
| **M3** | Ca meta **quét tĩnh**: ĐỎ khi thân một ca dựng môi trường bằng kế thừa. Chốt PHỤ. |
| **M4** | Chốt M2 chạy trong CI **mỗi lượt gate**, không phải chỉ khi gọi tay. |

Bề mặt biến môi trường mà mã sản phẩm đọc, đo `08:46:44Z` — **2** biến (đơn vị = lời gọi `os.environ`
trong `ops/lease_publish.py`): `GITHUB_REPOSITORY` (d.637) · `GITHUB_ACTOR` (d.852). Bề mặt nhỏ và
**liệt kê được**, nên danh sách CHO PHÉP ở M1 là khả thi thật — khác hẳn ca `doctrine-scan` nơi danh
sách cấm thua từ trong thiết kế.

## `nghiem_thu` — mỗi tiêu chí kèm phép đo làm nó ĐỎ (L3)

**M1**
- `A1` Đếm lại: `dict(os.environ` = **0**, và số ca (`^@ca`) vẫn = **124** (đơn vị: lần xuất hiện chuỗi · số ca).
- `A2` **Phép làm ĐỎ:** trả một chỗ bất kỳ về `dict(os.environ, ...)` ⇒ `A1` ĐỎ.

**M2**
- `B1` Suite chạy dưới `GITHUB_ACTOR` ∈ {`github-actions[bot]`, `ducthangho`, `""`} cho **cùng một**
  cặp `(số ca đạt, số ca chạy)` ở cả ba lượt.
  Nền hôm nay, đo `08:0xZ` trên cây `7766fd56`: `github-actions[bot]` → **94/124**;
  `ducthangho` → **123/124** (ca đỏ còn lại là `t33`, thiếu `actionlint` cục bộ — KHÔNG phải lỗi mã).
  Sau vá, ba lượt phải bằng nhau.
- `B2` **Phép làm ĐỎ:** gỡ `clear=True` khỏi **đúng một** ca ⇒ `B1` ĐỎ.
- `B3` **Chốt chống tín dụng giả** (bài học `#355`/`#359`): `B2` phải làm ĐỎ **đúng ca bị gỡ**, không
  phải ca khác. Tín hiệu phải là lớp ngoại lệ RIÊNG mà mã triển khai không giả được, và phải neo
  **TÊN CA**. Một mutant chết vì `AttributeError` phải rơi vào **TÍN DỤNG GIẢ**, kể cả khi trên đường
  có một `except` đổi kiểu.

**M3**
- `C1` Bơm một ca giả dùng `dict(os.environ, ...)` ⇒ M3 ĐỎ.
- `C2` **Phép làm ĐỎ:** cây nguyên vẹn ⇒ M3 XANH (chống chặn oan).
- `C3` M3 KHÔNG được là chốt duy nhất: nó quét CHUỖI, và kho đã đo được rằng quét cách viết không
  phải quét thẩm quyền (`codex-dispatcher` · `cödex` · `cödex`). M2 là chốt chính.

**M4**
- `D1` Bước CI gọi chốt M2 tồn tại và **đã chạy** (không `skipped`) trong một lượt gate thật.
- `D2` **Phép làm ĐỎ:** đặt bước ấy `if: false` ⇒ một ca phải ĐỎ. Chốt không nối vào đường TỰ ĐỘNG
  thì chốt chỉ là tài liệu (bài học r225).
- `D3` Ngân sách: bước `lease-publish selftest` đo **24 giây** trên `ubuntu-latest` lượt
  `33234750843` (`2026-08-29T07:44Z`). ×3 actor ≈ **72s**, tức thêm ~**48 giây**/lượt.

## `hinh_dang_ke_thua` (L4)

Hình dạng: **phép đo thừa hưởng trạng thái môi trường thay vì tự dựng nó.**
Bộ đếm chép từ `CLAUDE.md` mục *"PHÉP ĐO DELTA SO HAI VẾ PHẢI DỰNG CẢ HAI TRONG MỘT LỆNH"* (đo
24-08-2026): **4 ca ĐO ĐƯỢC**, cộng **1 ca KHÔNG TÁCH ĐƯỢC** (đơn vị = sự cố riêng biệt có
SHA/lệnh/output tái hiện được).

N0 là ca thứ **5** đo được của cùng hình dạng — lần này nạn nhân là bộ test của chính cổng thẩm quyền.

**Ngưỡng đang áp:** hình dạng lặp ≥3 lần thì câu hỏi đúng là *"có nên làm việc này không"*, không phải
*"vá thế nào"*. Ở đây đã **5**. Nên M1 cố ý chọn **đổi cấu trúc** (tự dựng môi trường) chứ không vá
từng biến — vá từng biến là lần thứ 6.

## `chua_do_duoc`

1. **Packet Issue riêng chưa mở.** Spec này là DỮ LIỆU, không phải lệnh giao việc. Đọc được spec
   KHÔNG phải được giao việc (§3.2, §4).
2. **Chưa biết bao nhiêu trong 15 chỗ `dict(os.environ` THỰC SỰ cần môi trường kế thừa.** Đếm được
   chuỗi, chưa đọc từng ca. Có thể có ca cần `PATH` thật (ví dụ ca gọi `git`/`actionlint`). Executor
   phải đo từng chỗ; nếu có chỗ buộc phải kế thừa thì **khai ra**, đừng ép `clear=True` cho đủ số.
3. **Chưa đo bản vá có làm chậm suite quá `D3` không.** 72s là phép nhân, không phải phép đo.
4. **`codex` KHÔNG có trong container của phiên soạn spec** (`launcher.py doctor` → rc=12,
   `2026-08-29T07:0xZ`). Phiên này không tự chạy được executor `codex`.
5. **Chưa đo `#388` bao giờ land.** Toàn bộ thứ tự ở `write_set` treo vào việc đó.
