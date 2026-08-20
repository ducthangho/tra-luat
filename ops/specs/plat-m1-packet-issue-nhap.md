# BẢN NHÁP Packet Issue — `PLAT-M1` (A1): macOS chưa từng được đo

> **⛔ TẠM HOÃN — người giữ kho quyết định 20-08-2026: tạm thời bỏ macOS.**
> Tệp này **không** còn là hàng đợi; nó là **hồ sơ** của hai lỗi đã đo được (§3.1 và
> §3.2) để lần sau mở lại không phải đo lại từ đầu. Không mở Issue từ nó, không cấp
> lease cho nó. Quyết định ghi tại `ops/KE_HOACH_DIEU_CHINH_DA_NEN_TANG.md` §3 mục A1
> và bảng §5.
>
> **⛔ CHƯA ĐƯỢC BẮT ĐẦU. ĐÂY LÀ BẢN NHÁP, KHÔNG PHẢI AUTHORITY.**
> Phiên Claude soạn để người giữ kho duyệt rồi tự mở Issue và cấp lease. Thứ giao việc là
> Packet Issue kèm lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md` §3.2 và §4); prompt,
> handoff và tệp nháp này **không phải lease** (§7).
> Nguồn của packet: `ops/KE_HOACH_DIEU_CHINH_DA_NEN_TANG.md` §3 mục A1.

## 1. Packet Spec đề nghị

```yaml
schema_version: 1
packet_id: PLAT-M1
phase_key: PLAT-M1
priority: P1
executor: claude
model: opus-5          # §2 kế hoạch: Executor Opus 5
effort: high           # §8 kế hoạch: Spec PHẢI khai effort, không khai thì mặc định `high` và thường sai
environment: local
risk: normal
review_class: systemic
depends_on: []
effective_write_set:
  - .github/workflows/launcher-windows.yml
  - .github/workflows/launcher-nen.yml      # planned: đích của lần đổi tên
required_review_assurance: cross_approved
required_independent_reviewer: codex
```

**Write set khai HAI đường dẫn, không phải một.** Kế hoạch ghi một dòng
(`launcher-windows.yml` *(đổi tên thành `launcher-nen.yml`)*), nhưng với git thì đổi tên là
**xoá một path và thêm một path**. Khai một đường dẫn thì phép kiểm write set trên từng
commit sẽ báo path lạ ở đúng commit làm việc chính.

## 2. Vì sao có packet này — bằng chứng đo được trên `50d8d12`

```
rg -c 'Darwin' .claude/dev/launcher.py     -> 12 dòng chạm Darwin
rg -i -n 'macos' .github/workflows/        -> 0 kết quả
```

`launcher.py` sinh ra chính vì mục tiêu đa nền, có đường riêng cho Darwin ở `_chup_cay`,
`_khoa_danh_tinh`, `_thanh_vien_nhom` và bảng gợi ý cài đặt. **Không dòng nào từng chạy
trên một máy macOS thật.** Đúng lớp bệnh kho đã đặt tên nhiều lần: *đo sự CÓ MẶT thay vì
đo KHẢ NĂNG*.

## 3. Bốn thứ ĐO ĐƯỢC mà kế hoạch chưa nêu — mỗi thứ đổi hình dạng bản vá

### 3.1 `if:` nằm ở MỨC JOB, nên nhãn không tách được nền

```yaml
    strategy:
      matrix:
        os: [windows-latest, ubuntu-latest]
    if: >-
      github.event_name != 'pull_request'
      || contains(github.event.pull_request.labels.*.name, 'windows')
```

Điều kiện ấy gác **cả matrix**, không gác từng phần tử. Thêm `macos-latest` vào nguyên chỗ
cũ nghĩa là: gắn nhãn `windows` thì **macOS cũng chạy** (runner macOS đắt gấp ~10 lần
Linux), và **không có cách nào gọi riêng macOS**. Kế hoạch nói *“chỉ chạy khi push master,
gọi tay, hoặc gắn nhãn `macos`”* — muốn đúng câu đó thì điều kiện phải **hạ xuống mức phần
tử matrix** (ví dụ `matrix.include` mang theo tên nhãn của từng nền, rồi gác ở job/step
theo `matrix.nhan`). Đây là quyết định thiết kế phải chốt TRƯỚC khi viết.

### 3.2 Bước cài `ripgrep` HỎNG trên macOS — đây là lỗi thật, không phải giả định

```bash
if [ "${RUNNER_OS:-}" = "Windows" ]; then choco install ripgrep -y ...
else sudo apt-get update -qq && sudo apt-get install -y -qq ripgrep; fi
```

Nhánh `else` chạy `apt-get` — trên macOS runner **không có** `apt-get`. Mà `rg` là **công cụ
bắt buộc** từ 15-08-2026, nên `doctor` ngay bước sau sẽ thoát **12** và cả nhánh macOS đỏ vì
lý do **không liên quan gì tới macOS**. Phải thêm nhánh `brew install ripgrep`, và giữ đúng
nếp đã ghi trong chính tệp workflow: bằng chứng là `rg --version` chạy được, không phải
`command -v`.

### 3.3 Đổi tên làm CHẾT 8 chỗ tham chiếu nằm NGOÀI write set

```
docs/AUDIT_LAUNCHER_VONG_7.md:68
ops/BAN_GIAO_pr141_pr143.md:8, 38, 44          <- dòng 44 là lệnh gọi: workflow_id: launcher-windows.yml
ops/KE_HOACH_DIEU_CHINH_DA_NEN_TANG.md:32, 86
ops/leases/doctor-github-mcp-review-7-codex-20260817.yaml:117
ops/leases/doctor-github-mcp-review-8-codex-20260817.yaml:110
```

Ba đường ra, người giữ chọn **một** và ghi lý do:

- **(a)** Bỏ phần đổi tên. Rẻ nhất, không nợ; cái giá là tên tệp tiếp tục nói sai (nó không
  còn chỉ chạy Windows).
- **(b)** Giữ đổi tên, **mở rộng write set** sang các tệp tài liệu ở trên. Cái giá: packet
  phình, và hai tệp `ops/leases/*.yaml` là **sổ chép thêm** — sửa hồi tố một lease đã đăng
  là chuyện khác hẳn, tôi khuyến nghị **không** đụng chúng.
- **(c)** Giữ đổi tên, **ghi nợ tường minh** vào `ops/NO_KY_THUAT.md` cho các tham chiếu cũ.
  Nhưng `ops/NO_KY_THUAT.md` cũng nằm ngoài write set ⇒ vẫn phải mở rộng, chỉ là mở ít hơn.

Kèm hai hệ quả nhỏ nằm **trong** tệp: khối `paths:` tự trỏ tên mình phải đổi theo, và
`concurrency.group` dùng `github.workflow` nên đổi `name:` là đổi nhóm gộp — vô hại nhưng
phải biết trước kẻo đọc log thấy lạ. Ngoài ra lịch sử lượt chạy **không** đi theo tên mới:
trang Actions sẽ có hai mục.

### 3.4 Nhãn `labeled` — tệp NÀY đã đúng, đừng bê bài học của `ci.yml` sang

`launcher-windows.yml` khai `pull_request: types: [opened, synchronize, reopened, labeled]`,
tức gắn nhãn **có** sinh lượt chạy mới. Bài học trong `CLAUDE.md` (*gắn nhãn không tự sinh
lượt chạy*) là về **`ci.yml`**, nơi `pull_request:` không khai `types:`. Đừng “sửa” chỗ đã
đúng, và đừng suy ngược rằng nhãn `macos` sẽ tự chạy ở `ci.yml`.

## 4. Acceptance

- macOS chạy **thật** trọn bốn bước đang có: `doctor` · bộ phản chứng · tự đột biến · cây
  làm việc sạch. Bằng chứng là một lượt chạy có `conclusion: success` cho phần tử
  `macos-latest`, đọc ngược từ GitHub — không phải YAML “có vẻ đúng”.
- **Số ca bỏ qua của TỪNG nền là đầu ra dương**, in ra chỗ đọc được (job summary), tách bốn
  con số: tổng · qua · bỏ qua · hỏng. Nền chuẩn để so: CI 17-08-2026 đo Linux bỏ qua **1**,
  Windows bỏ qua **13**; macOS chưa có số nào.
- Gọi được **riêng** macOS mà không kéo Windows, và ngược lại (§3.1).
- `rg --version` chạy được trên cả ba nền (§3.2).
- `actionlint` trên tệp đã sửa: rc=0, và **fail-close khi thiếu công cụ** — in `KHÔNG ĐO
  ĐƯỢC` rồi trả mã khác 0. Cổng tự tắt khi thiếu công cụ là cổng không tồn tại đúng lúc cần.
- **Nếu macOS lộ ca HỎNG thật thì DỪNG** và mở packet riêng. Sửa `launcher.py` nằm **ngoài**
  write set này.

## 5. Phản chứng bắt buộc

Vấn đề riêng của packet này: write set là **một tệp YAML**, không có tệp test nào để gắn ca.
Chốt cơ học phải sống ở đâu là **quyết định thứ tư** người giữ phải chốt:

- **(a)** chấp nhận bằng chứng chỉ là **lượt chạy thật** (đủ cho lần này, nhưng không có gì
  chặn lần sau ai đó gỡ `macos-latest` ra);
- **(b)** mở rộng write set thêm **một tệp test** phân tích YAML và khẳng định ba phần tử
  matrix cùng cách gác theo nhãn — khi ấy có đột biến thật: **gỡ `macos-latest` ⇒ ca đích
  ĐỎ**; **hạ điều kiện nhãn về mức job ⇒ ca đích ĐỎ**.

Khuyến nghị **(b)**. Lý do đã trả giá: *nghĩ ra được phép thử mà không chạy nó thì phép thử
ấy không tồn tại* — và một hàng phòng thủ nằm trong phần mô tả PR là hàng phòng thủ chết.

Ngoài ra, bất kể chọn gì:

- Lượt chạy phải cho thấy `macos-latest` **có job**, không phải `skipped`. “Vắng mặt vì
  sạch” và “vắng mặt vì chưa chạy” nhìn giống hệt nhau trên giao diện.
- Đột biến bước cài `rg`: ép nhánh `apt-get` cho macOS ⇒ lượt macOS phải ĐỎ ở `doctor` với
  `THIEU rg`, chứng minh bước ấy thật sự đang gác.

## 6. Non-goals — KHÔNG làm trong packet này

- **Không** đụng `.claude/dev/launcher.py` hay `launcher_test.py`, kể cả khi macOS đỏ.
- **Không** đụng `.github/workflows/ci.yml` — đó là packet A2 (`PLAT-M2`, Sonnet 5).
- **Không** bật macOS theo mọi push: runner macOS đắt gấp ~10 lần Linux.
- **Không** hạ chuẩn `doctor` để cho nhánh macOS xanh. Thiếu công cụ thì **cấp đủ công cụ**.

## 7. Ràng buộc

- **Đừng viết cú pháp biểu thức Actions trong comment của `run`.** GitHub nội suy biểu thức
  trên toàn bộ thân `run` trước khi shell thấy nó; một cặp rỗng trong dòng chú thích làm
  **cả tệp** không hợp lệ — dấu hiệu là một run mang tên đường dẫn tệp, **0 job**,
  `conclusion: failure`. PyYAML **không** bắt được ca này; chỉ `actionlint` bắt.
- `core.abbrev` = 7 trước mọi cổng, nếu không hai ca doc-claims đỏ oan.
- Trần review **2 vòng**, đếm theo vòng. Mỗi finding kèm khối `Gợi ý vá` bốn phần.
- Đọc ngược mọi thứ đã đăng lên GitHub; `git fetch` qua proxy nói dối — dùng `git ls-remote`.

## 8. Vì sao `systemic` chứ không `routine`

Nó đổi hình dạng **cổng CI** và mở một dòng chi phí runner mới. Sai chiều rộng thì hoặc đốt
phút macOS ở mọi lượt gắn nhãn `windows`, hoặc dựng một nền “có mặt trong YAML mà chưa từng
chạy” — đúng thứ bệnh packet này sinh ra để chữa.
