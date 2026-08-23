# Prompt EXECUTOR — `LEASE-DANG-WINDOWS` (#238), lượt **2** — neo đặc tả **r2**

Lease `lease-dang-windows-exec-2-codex-20260822`. **Thay lease lượt 1** (neo `r1`, chưa chạy).

## Đọc trước

`#227` (bản vá của bạn) land rồi **CI master ĐỎ trên Windows** (`59/68`), phải revert. **Đây
không phải lỗi của bạn** — `ci.yml` chỉ chạy `ubuntu` cho PR thường; đường đúng là gọi tay
`workflow_dispatch` trước merge, và **phiên điều phối đã không làm**.

`r1` của đặc tả **CẤM** bỏ qua theo nền. **`r2` ĐẢO lại**, và đây là điểm xoay:

> `ops-publish-lease.yml` khai **`runs-on: ubuntu-latest`**. Tám ca đi qua `_chay_buoc_dang`
> **trích thân bước từ workflow ấy** rồi chạy dưới `bash` — nên trên Windows chúng đo **một thứ
> không bao giờ chạy ở đó**. Giả định POSIX của chúng **HỢP LỆ**; chúng hỏng vì **tình cờ bị thực
> thi sai nền**.

Và docstring `_bash_posix()` **trong chính tệp ấy** đã viết sẵn câu đó trước khi lỗi xảy ra.

## Nguồn sự thật

1. `{PROMPT_FILE}`
2. **`ops/specs/LEASE-DANG-WINDOWS-r2.md`** — sha256
   `d9da7705617c95c8dc394d773de8456712d3cc2a2975e5903e8cb28c934c0d83`
3. `ops/specs/LEASE-DANG-WINDOWS.md` (`r1`, `f555cbe1…`) — nguyên hiệu lực cho mọi thứ `r2`
   không nêu. **`Q3` của `r1` ĐÃ BỊ THAY bằng `Q3′`.**
4. `CLAUDE.md`

**KIỂM BĂM; lệch ⇒ DỪNG.**

## Việc — bốn thứ

### 1. Khôi phục ba tệp mã từ `ba82b06f` (CƠ HỌC)

```
git checkout ba82b06f9df81fc2f13786fec590ec2110d046b7 -- \
  .github/workflows/ops-publish-lease.yml ops/lease_publish.py ops/lease_publish_test.py
```

Không sửa gì thêm ở bước này — ba tệp ấy đã qua bốn lượt cross-review.

### 2. `Q3′` — phạm vi nền **DẪN XUẤT**, không phải danh sách

Ca đọc thân bước của workflow **X** ⇒ nền của ca = **`runs-on` của X**. **Không viết danh sách
tay.** Đọc `runs-on` từ chính tệp YAML.

- **`W6`**: đổi `runs-on` của `ops-publish-lease.yml` thành matrix có `windows-latest` ⇒ tám ca ấy
  **phải chạy trở lại**. Ghi cứng danh sách thì đột biến này **không đổi gì** ⇒ ĐỎ.
- **`W7`** (chống cửa sau): bỏ qua một ca mà workflow của nó **KHÔNG** ubuntu-only ⇒ **ĐỎ**.
- **`W8`**: ca bị bỏ qua phải **IN RA** rằng nó bỏ qua **và vì sao**, kèm `runs-on` đã đọc được.
  Tổng kết khai **số đã chạy / số bỏ qua**. *"Ca có MẶT khác ca có ĐO"* — ca im lặng bỏ qua là ca
  biến mất.

### 3. `Q6` — `t49` phải VÁ THẬT, không được bỏ qua

`t49` **không** trích thân bước của workflow nào; nó đo **mối nối `GOI_GH`** bằng một `gh` giả.
Giả định POSIX của nó là về **bộ đồ giả**, không về một artefact ubuntu-only ⇒ **`Q3′` không áp
dụng**.

Giả thuyết mạnh, **chưa đo**: nó ghi một script **shebang không phần mở rộng** vào `PATH`; Windows
không chạy shebang ⇒ `gh` giả không bao giờ được gọi ⇒ tệp `calls` không sinh. Kiểm rồi vá — cách
vá là của bạn.

### 4. `W1`/`W2` — làm phép đo BÁO ĐƯỢC NGUYÊN NHÂN

Hiện `_chay_buoc_dang` kết bằng `log.read_text()`, nên khi đồ giả không chạy nó ném
`FileNotFoundError` **trần** — **nuốt sạch `rc`, `stdout`, `stderr`**. Phép đo **tự giấu lý do**,
và đó là lý do không ai biết Windows hỏng ở đâu.

Sửa: thiếu bất kỳ tệp nào do đồ giả sinh ⇒ ném lỗi **kèm `rc` + `stdout` + `stderr`**, nói rõ đây
là **KHÔNG ĐO ĐƯỢC**. Làm cho **mọi** chỗ đọc tệp do đồ giả sinh. Ca khoá: bỏ phần đính kèm ⇒ ĐỎ.

## Ngân sách

**≤ 3 tệp, ≤ 90 dòng THÊM so với `ba82b06f`.** Khôi phục là **cơ học**, không tính.
Vượt ⇒ DỪNG + handoff.

## Cổng

| cổng | tiêu chí |
|---|---|
| `python3 ops/lease_publish_test.py` | `rc=0`, `N/N` bằng nhau, **≥ 72 ca** |
| cùng suite, ba biến GitHub đặt, `gh` **vắng** | `N/N` y hệt |
| `actionlint .github/workflows/*.yml` | `rc=0` cả 5 |
| **`shellcheck` PHẢI có mặt** khi chạy `actionlint` | thiếu ⇒ in **KHÔNG ĐO ĐƯỢC** và **ĐỎ** |
| `W6` `W7` `W8` | mỗi cái có đột biến giết **1/1** |
| đột biến bỏ đính kèm `rc/stdout/stderr` | **PHẢI ĐỎ** |
| đột biến quyết định của `#227` | `M1`–`M4` · `A5` · `D3`/`D4` · tám đột biến gỡ guard — **vẫn phải giết** |
| `git diff --numstat ba82b06f..HEAD` | ≤ 3 tệp, ≤ 90 dòng thêm |

**Về `shellcheck`:** phiên điều phối khai *"`actionlint` rc=0"* suốt bốn lượt của `#227` trong khi
`actionlint` của container **không có `shellcheck`** ⇒ nó **im lặng bỏ qua** toàn bộ luật nền ấy,
và CI đỏ ngay lần chạy đầu (`SC2320`). **Kiểm `shellcheck` có mặt TRƯỚC KHI tin `actionlint`**, và
**khai rõ đã đo bằng bản nào**.

## CẤM

- Bỏ qua theo nền **ngoài** điều kiện `Q3′` — đặc biệt **`t49`**.
- Đụng hai finding của verdict `#227` lượt 5 (`bao_chan` khoá theo cách viết · bất biến `set +e`)
  — chúng ở **#235**.
- Sửa `ops/specs/**`.

## Bạn KHÔNG chạy được `workflow_dispatch`

Phiên điều phối sẽ chạy Windows thật trên exact head của bạn và **đó mới là nghiệm thu**
(`W3′`). Suite xanh trong sandbox **chưa phải bằng chứng** — `#227` đã có bốn lượt xanh như thế
rồi vẫn đỏ ở CI.

## Báo cáo cuối

1. `git diff --numstat ba82b06f..HEAD` — số thật.
2. `N/N`, hai lần chạy. Kèm **phiên bản `actionlint` và `shellcheck`**.
3. Bảng đột biến: `W6` `W7` `W8` · đính kèm `rc/stdout/stderr` · toàn bộ đột biến quyết định của
   `#227`. Danh sách đa sát.
4. **Nguyên nhân THẬT của `t49`** — đo được, không phải giả thuyết. Nếu không đo được thì nói là
   không đo được.
5. **Danh sách ca bị bỏ qua trên Windows**, mỗi ca kèm `runs-on` **đã đọc từ YAML** làm lý do.
6. `chua_do_duoc`.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
