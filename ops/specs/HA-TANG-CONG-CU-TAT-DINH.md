# ĐẶC TẢ PACKET — `HA-TANG-CONG-CU-TAT-DINH`, **revision 1**

```yaml
packet_id: HA-TANG-CONG-CU-TAT-DINH
revision: 1
review_class: sensitive       # write set cham .github/workflows/** va .claude/dev/**
assurance_target: cross_approved
```

> **TỆP NÀY ĐÓNG BĂNG SAU KHI CÓ LEASE NEO VÀO. ĐỪNG SỬA** — mỗi lần sửa là vô hiệu hoá
> mọi lease đang neo, **im lặng, không cảnh báo**. Đổi nội dung ⇒ ra **revision MỚI**.
>
> **`executor`, `reviewer`, `generation`, `base_sha` CỐ Ý không có ở đây** — chúng thuộc
> **LEASE**. Bài học đã trả giá hai lần ở `#276`: lần đầu để `executor`/`base_sha` là `null`
> kèm chú thích *"điền sau"*, lần hai sót `reviewer` cùng họ. Một trường trông như chỗ trống
> thì sẽ có người điền, và người ấy làm chết mọi lease.
>
> **`packet_issue` cũng KHÔNG có ở đây**, và đó là lần áp dụng bài học thứ ba: số Issue
> **chưa tồn tại** lúc soạn đặc tả. Bản nháp đầu của chính tệp này để `packet_issue: null`
> kèm chú thích *"điền khi mở Issue"* — tức lại dựng đúng cái chỗ trống mà hai đoạn trên vừa
> cấm. Số Issue sống ở **Issue và LEASE**; đặc tả chỉ giữ thứ biết được lúc đóng băng.

## 0. Vì sao có packet này

Người giữ kho nêu 23-08-2026: *"một số công cụ cần có thì mới test được như actionlint,
cryptography… một số môi trường mặc định lại không có nên khi chạy là fail không đáng có."*

Đo trên container phiên remote cùng ngày:

```
THIEU : actionlint · shellcheck · pwsh · gh · yamllint · shfmt
CO    : jq 1.7 · cryptography · PyYAML · ruff
```

Và một thứ đáng lo hơn việc thiếu — **hai `ruff` khác phiên bản trên CÙNG một máy**:

```
ruff (nhi phan)   ->  0.15.8   /root/.local/bin/ruff
python3 -m ruff   ->  0.16.4
```

Hai đường gọi, hai bộ luật, hai kết quả. Đây là *"có mặt ≠ đúng bản"* ở dạng sống.

## 1. BA kiểu hỏng KHÁC NHAU — gộp lại là lý do vấn đề chưa dứt

| | triệu chứng | ca đã xảy ra |
|---|---|---|
| **(a) ĐỎ oan** | thiếu công cụ ⇒ cổng đỏ, đọc thành lỗi mã | `t33` fail-close vì thiếu `actionlint` |
| **(b) XANH GIẢ** | công cụ **có** nhưng suy giảm ⇒ cổng xanh mà **đo ít hơn** | thiếu `shellcheck` ⇒ `actionlint` **im lặng bỏ cả lớp luật**, vẫn `rc=0` |
| **(c) ca có MẶT mà không ĐO** | suite bỏ qua có in lý do ⇒ vẫn tính là đạt | thiếu `pwsh` ⇒ `N10′` **chưa lần nào được đo** |

**(b) nguy nhất vì nó không kêu.** `CLAUDE.md` đã ghi hậu quả đo được: câu *"actionlint 5
workflow → rc=0"* trôi thành `rc=1` **chỉ vì `shellcheck` có ở lần đo sau mà vắng ở lần trước**.

Cả ba cùng một gốc: **sự sẵn có của công cụ là ĐẦU VÀO của phép đo, nhưng bản thân nó không
được khai và không được đo.**

## 2. `muc_tieu`

Kho **đã giải đúng bài này cho MỘT công cụ**. `ops/cai_actionlint.sh` ghim phiên bản exact,
**cố ý không có nhánh thoát sớm** *"đã có trên PATH thì thôi"*, và `t35` **chạy thật** script
ấy với `actionlint` giả rồi đòi nó từ chối. Packet này **tổng quát hoá đúng cái đó**, không
dựng tầng mới.

| # | mục tiêu | tệp |
|---|---|---|
| **G1** | **MỘT bản kê máy đọc được**: mỗi công cụ có tên · **phiên bản ghim** · công thức cài **theo nền** · lệnh probe · **canary năng lực** (G3). Một nguồn cho hook, `doctor`, CI và từng cổng | `ops/cong_cu.yaml` |
| **G2** | `ops/cai_cong_cu.sh <tên>` đọc bản kê và cài. Giữ **hai tính chất đã chứng minh** của `cai_actionlint.sh`: ghim exact · **không thoát sớm khi đã có trên PATH**. Sau khi cài thì **ĐO LẠI**, không tin `rc` của trình cài | `ops/cai_cong_cu.sh` |
| **G3** | **CANARY bắt suy giảm âm thầm**: fixture có **finding biết trước**. `actionlint` chạy trên một workflow cố ý chứa `SC1003`; **trả sạch ⇒ `shellcheck` vắng ⇒ trạng thái `SUY_GIẢM`**, không phải `sạch` | `ops/canary/` |
| **G4** | **BA trạng thái ở mọi cổng** — `ĐẠT` · `ĐỎ` · **`KHÔNG_ĐO_ĐƯỢC`** — và cái thứ ba có **mã thoát RIÊNG** để CI phân biệt "đỏ thật" với "không đo nổi" | `ops/cong_cu.py` |
| **G5** | **CI kiểm bản kê Ở BƯỚC ĐẦU TIÊN**; thiếu công cụ ⇒ job đỏ **trước khi chạy test nào**, thông điệp nói rõ thiếu gì. Phiên dev/remote thiếu ⇒ in `KHÔNG_ĐO_ĐƯỢC`, **không** tính là đỏ | `.github/workflows/ci.yml` |
| **G6** | Mọi số nền ghi vào hồ sơ mang **vân tay công cụ** (tên + phiên bản). Số không kèm điều kiện đo thì sẽ trôi mà không ai biết | `ops/cong_cu.py` |

### Ghi rõ vì sao G4 tách `KHÔNG_ĐO_ĐƯỢC` khỏi `ĐỎ`

Đây là điều chấm dứt *"fail không đáng có"*. Hôm nay hai thứ đó cùng một mã thoát, nên người
đọc không phân biệt được **"mã sai"** với **"máy thiếu công cụ"** — và mỗi lần thiếu lại tốn
một lượt đi truy mã. Tách mã thoát là rẻ và nó **đo được**.

## 3. `write_set`

```
ops/cong_cu.yaml            ops/cong_cu.py            ops/cong_cu_test.py
ops/cai_cong_cu.sh          ops/canary/               .github/workflows/ci.yml
```

`ops/cai_actionlint.sh` **giữ nguyên, không xoá**: nó đang được `t35` canh, và bỏ nó là bỏ
một phép thử **chạy được**. Bản kê **gọi** nó, không thay nó.

## 4. `ngan_sach_kich_thuoc`

**6 đường dẫn / 400 dòng thêm.** Vượt trần ADR-0044 (≤3 tệp cho `sensitive`) — **có chủ đích**,
và người cấp lease cần biết: bản kê, bộ đọc, bộ cài, canary và cổng CI là **năm mặt của một
cơ chế**. Thấy quá rộng thì cách đúng là **CHIA PACKET**, không phải nén bừa.

## 5. `nghiem_thu` — mỗi ca một đột biến; ca không có đột biến là ca sẽ âm thầm hở

| # | nghiệm thu | đột biến làm nó ĐỎ |
|---|---|---|
| **T1** | thiếu một công cụ bắt buộc ⇒ `KHÔNG_ĐO_ĐƯỢC` với **mã thoát riêng**, **không** phải mã của `ĐỎ` | gộp hai mã thoát làm một |
| **T2** | **canary**: `actionlint` **có** mà `shellcheck` **vắng** ⇒ `SUY_GIẢM`, không phải `sạch` | bỏ canary ⇒ chỉ T2 đỏ |
| **T3** | **chiều BẮT OAN**: đủ công cụ, đúng phiên bản ⇒ `ĐẠT`, không cảnh báo thừa | siết bừa (mọi thứ thành `SUY_GIẢM`) ⇒ **chỉ T3 đỏ** |
| **T4** | công cụ **có mặt nhưng SAI BẢN** ⇒ từ chối, nêu bản mong đợi và bản thấy được | bỏ so phiên bản |
| **T5** | `cai_cong_cu.sh` **không** thoát sớm khi công cụ đã có trên PATH | thêm nhánh thoát sớm ⇒ T5 đỏ |
| **T6** | CI thiếu công cụ ⇒ job đỏ **trước khi chạy test nào** | dời phép kiểm xuống sau bước test |
| **T7** | **hai đường gọi cùng tên** (`ruff` nhị phân vs `python3 -m ruff`) khác phiên bản ⇒ báo, không im | chỉ probe một đường |
| **T8** | vân tay công cụ có trong bản ghi số nền | bỏ vân tay |

**T3 bắt buộc** — thiếu nó thì một bản "cảnh báo tất" cũng xanh, và ta lại đo cái mình đã đặt.

**T2 và T7 là hai ca đáng đọc nhất**: chúng đo thứ hôm nay **không ai đo**, và cả hai đều có
ca thật đã xảy ra làm gốc.

## 6. `dieu_kien_dung`

- Định làm cổng **tự bỏ qua** khi thiếu công cụ ⇒ **DỪNG**. Một cổng tự tắt khi thiếu công cụ
  là cổng không tồn tại **đúng lúc nó cần nhất**.
- Định gộp `KHÔNG_ĐO_ĐƯỢC` vào `ĐẠT` cho "đỡ ồn" ⇒ **DỪNG**: đó là biến (a) thành (b), tức
  đổi một lỗi ồn lấy một lỗi câm.
- Cần ghi ngoài write set ⇒ **DỪNG**, xin revision.
- Vượt 400 dòng hoặc 6 tệp ⇒ **NÉN**, không nới.

## 7. `chua_do_duoc`

- **Không đo được bản kê có ĐỦ không.** Danh sách công cụ hôm nay dựng từ `grep` trên các cổng
  hiện có; công cụ mà **chưa cổng nào gọi tới** thì không cách nào thấy. Bản kê vì thế là
  **danh sách CHO PHÉP đang lớn dần**, không phải bản đầy đủ — và phải nói thế trong chính tệp.
- **Canary chỉ phủ cặp đã BIẾT.** `actionlint`+`shellcheck` là cặp duy nhất kho từng trả giá.
  Cặp suy giảm âm thầm khác, nếu có, **chưa ai tìm**.
- **Chưa đo chi phí phút CI** của việc cài đủ công cụ trên `windows-latest`. `r245` trong
  `ci.yml` đã từng phải cắt vì phút Actions — **đo trước khi nối**, đừng nối bừa.
- **`pwsh` vào bản kê KHÔNG tự làm `N10′` được đo** — nó mới chỉ mở đường. Việc đo `N10′` thuộc
  packet khác.
