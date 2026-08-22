# Prompt EXECUTOR — `LEASE-DANG-WINDOWS` (#238), lượt 1 — **GIAI ĐOẠN 1: LÀM PHÉP ĐO ĐỌC ĐƯỢC**

Lease `lease-dang-windows-exec-1-codex-20260822`.

## Đọc trước — chuyện đã xảy ra, và vai của bạn trong đó

`#227` (bản vá của bạn, bốn lượt cross-review) land rồi **CI master ĐỎ trên Windows**, phải
revert. **Chín ca đỏ đều là ca MỚI của `#227` và chưa ca nào từng chạy trên Windows.**

**Đây KHÔNG phải lỗi của bạn.** `ci.yml` chỉ chạy `ubuntu` cho PR thường; đường đúng là gọi tay
`workflow_dispatch` trước khi merge, và **phiên điều phối đã không làm** — dù chính nó trích bài
học ấy trong thân PR. Nói ra để bạn khỏi đi tìm lỗi ở chỗ không có.

## Nguồn sự thật

1. `{PROMPT_FILE}`
2. **`ops/specs/LEASE-DANG-WINDOWS.md`** — sha256
   `f555cbe1a368c12040726dd706ce25ed8dd4041bd8a2f840590810a3c3908a26`
3. `CLAUDE.md`

**KIỂM BĂM; lệch ⇒ DỪNG.**

## Giai đoạn 1 — ĐÚNG BA việc, và KHÔNG có việc thứ tư

### 1. Khôi phục ba tệp mã từ `ba82b06f` (CƠ HỌC)

```
git checkout ba82b06f9df81fc2f13786fec590ec2110d046b7 -- \
  .github/workflows/ops-publish-lease.yml ops/lease_publish.py ops/lease_publish_test.py
```

Không sửa gì thêm ở bước này. Ba tệp ấy đã qua bốn lượt cross-review.

### 2. `W1`/`W2` — làm phép đo BÁO ĐƯỢC NGUYÊN NHÂN

Hiện `_chay_buoc_dang` kết bằng `log.read_text()`, nên khi đồ giả không chạy nó ném
`FileNotFoundError` **trần** — **nuốt sạch `rc`, `stdout`, `stderr`** của tiến trình con. Phép đo
**tự giấu lý do**, và đó là lý do không ai biết Windows hỏng ở đâu.

Sửa: thiếu bất kỳ tệp nào do đồ giả sinh ⇒ ném lỗi **kèm `rc` + `stdout` + `stderr`**, nói rõ đây
là **KHÔNG ĐO ĐƯỢC**, không phải "phép đo cho kết quả sai". Làm tương tự cho `t49` và **mọi** chỗ
khác đọc tệp do đồ giả sinh.

Thêm ca khoá cho chính việc này: bỏ phần đính kèm ⇒ ca ấy phải **ĐỎ**.

### 3. Push, rồi DỪNG

```
git push origin codex/lease-dang-windows-1
```

**KHÔNG đoán nguyên nhân Windows. KHÔNG vá gì cho Windows ở lượt này.**

Bạn **không gọi được `workflow_dispatch`** từ sandbox. **Phiên điều phối sẽ chạy Windows thật và
trả log về cho bạn ở lượt 2.** Giai đoạn 1 chỉ có một mục tiêu: **làm cho log ấy đọc được.**

## CẤM

- **`skip` / `xfail` / rẽ nhánh theo `os.name` để lấy xanh.** Một ca bỏ qua trên Windows là ca
  **không tồn tại** đúng nơi nó cần nhất.
- Đụng hai finding của verdict `#227` lượt 5 (`bao_chan` khoá theo cách viết · bất biến
  `set +e`) — chúng ở **#235**.
- Sửa `ops/specs/**`.

## Ngân sách

**≤ 3 tệp, ≤ 60 dòng THÊM so với `ba82b06f`.** Khôi phục ba tệp là **cơ học**, không tính.
Vượt ⇒ DỪNG + handoff.

## Cổng

| cổng | tiêu chí |
|---|---|
| `python3 ops/lease_publish_test.py` | `rc=0`, `N/N` bằng nhau, **≥ 69 ca** |
| cùng suite, ba biến GitHub đặt, `gh` **vắng** | `N/N` y hệt |
| `actionlint .github/workflows/*.yml` | `rc=0` cả 5 |
| **`shellcheck` PHẢI có mặt khi chạy `actionlint`** | thiếu ⇒ in **KHÔNG ĐO ĐƯỢC** và **ĐỎ** |
| đột biến bỏ phần đính kèm `rc/stdout/stderr` | **PHẢI ĐỎ** |
| `git diff --numstat ba82b06f..HEAD` | ≤ 3 tệp, ≤ 60 dòng thêm |

**Về `shellcheck`, đọc kỹ:** phiên điều phối khai *"`actionlint` rc=0"* suốt bốn lượt trong khi
`actionlint` của container **không có `shellcheck`** ⇒ nó **im lặng bỏ qua** toàn bộ luật nền
`shellcheck`, và CI đỏ ngay lần chạy đầu (`SC2320`). **Kiểm `shellcheck` có mặt trước khi tin
`actionlint`**, và **khai rõ đã đo bằng bản nào**.

## Báo cáo cuối

1. `git diff --numstat ba82b06f..HEAD` — số thật.
2. `N/N`, hai lần chạy. Kèm **phiên bản `actionlint` và `shellcheck`** đã dùng.
3. Đột biến khoá `W1`/`W2` — giết `1/1`.
4. **Danh sách MỌI chỗ trong tệp test đọc một tệp do đồ giả sinh**, và chỗ nào đã được bọc.
   Chỗ nào chưa ⇒ **khai thẳng**.
5. `chua_do_duoc`, **bắt buộc** có câu: *nguyên nhân Windows CHƯA ĐƯỢC ĐO*.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
