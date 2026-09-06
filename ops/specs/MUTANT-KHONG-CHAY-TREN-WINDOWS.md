# Đặc tả packet — MUTANT-KHONG-CHAY-TREN-WINDOWS

- `packet_id`: **MUTANT-KHONG-CHAY-TREN-WINDOWS**
- `packet_issue`: **456**
- `revision`: 1
- `generation`: 1
- `executor`: claude · `environment`: cloud
- `review_class`: **sensitive** (chạm chốt bằng chứng dương của một cổng CI; không rõ ⇒ lấy mức chặt nhất)
- `base_sha`: `4f6d42a5` (`origin/master`, đo 06-09-2026)

## `nguon_cap_viec`

Không phải một dòng trong bảng packet của `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`. Đây là
packet **khắc phục**, sinh từ phép đo trong phiên `session_01VgjX75vhuri6GpVtgSAHeW` ngày
06-09-2026 và được chủ kho cấp phép trực tiếp trong phiên. Hiện vật gốc: Issue #456.

Tiền nhiệm gần nhất chạm cùng vấn đề: `ops/specs/CI-CAI-JSONSCHEMA-r3.md` (A5 — nó là chỗ
KHAI rằng parity Windows `KHÔNG ĐO ĐƯỢC`, và packet này là chỗ phép đo ấy trở nên làm được).

## Bối cảnh đo được (mọi số đều kèm thời điểm)

**Đo 06-09-2026, qua `actions_list` + `method: list_workflow_jobs` trên `/mcp/x/actions`:**

| | ubuntu | windows |
|---|---:|---:|
| `test registry` | 14,6 phút | **44,3 phút** |
| `packet-loop selftest` | ~2 phút | 9,4 phút |
| tổng job | 26,7 phút · `success` | 60,2 phút · **`cancelled`** |

Hai commit master liên tiếp — `3500369` và `4f6d42a` — job Windows dừng ở **đúng 60,3 phút**
cả hai lần (`timeout-minutes: 60`, `ci.yml:64`).

**Đo 06-09-2026 trên Linux của container phiên này**, từng bộ mà `test registry` chạy
(đơn vị: giây tường, một lượt, không lặp):

| bộ | giây | phần của bước |
|---|---:|---:|
| `.claude/hooks/pretooluse_guard_test.py` | **346** | **70 %** |
| `.claude/hooks/subagent_ghi_detect_test.py` | 101 | 20 % |
| `ops/nhanh_don_duoc_test.py` | 39 | 8 % |
| 5 bộ còn lại **cộng lại** | 10 | 2 % |
| tổng | 496 | 100 % |

**Tách nền/đột biến của bộ đầu, đo trên BẢN SAO** (vô hiệu vòng lặp đột biến, tệp thật không
bị đụng):

```
NỀN-ONLY  10 giây          ĐẦY ĐỦ  346 giây
⇒ đột biến = 336 giây = 97 % chi phí bộ này, ≈ 68 % chi phí cả bước `test registry`
```

`34` đột biến (đơn vị: mục trong `DOT_BIEN`), mỗi đột biến chạy lại trọn `36` ca
(đơn vị: mục trong `CA`).

**Số này SỬA một suy đoán đã viết ra trong cùng phiên:** tôi đoán
`subagent_ghi_detect_test.py` là bộ tốn nhất vì nó dài `1287` dòng và nhắc đột biến `53` chỗ.
Sai — nó chỉ `101` giây. Số dòng và số mutant KHÔNG dự báo được thời gian.

## `review_class` và ngưỡng kích thước

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp và ≤ 300 dòng thêm**. Write set dưới đây là **2 tệp**,
nằm trong ngưỡng, **không cần khai vượt trần**.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.claude/hooks/pretooluse_guard_test.py` | nơi vòng lặp đột biến chạy và nơi tiêu chí `dat` được tính |
| 2 | `.claude/dev/ci_dang_ky_test.py` | nơi mẫu bằng chứng dương của bộ ấy được khai (`MOI`) |

Không ký tự đại diện. Không đường dẫn nào khác.

## `ngoai_pham_vi`

1. **`.github/workflows/ci.yml` — CỐ Ý không đụng.** Tổng thời gian thật của job Windows
   **chưa ai đo**: `60,2` phút là số **BỊ CẮT** ở trần, bước `19`→`43` chưa từng chạy. Cắt
   `≈30` phút để lại `≈30` phút cho `24` bước chưa đo — *có vẻ* đủ, **chưa chứng minh**. Sửa
   cổng lúc này là suy đoán; đường đúng là vá xong rồi gọi `workflow_dispatch` mà ĐO.
2. **`subagent_ghi_detect_test.py` (`101`s) và `nhanh_don_duoc_test.py` (`39`s)** — để packet
   sau. `ADR-0044` đo được cái giá của packet to: `PLAT-M4` 2 tệp ⇒ **1 vòng, 1 finding**;
   `PLAT-X4` 4 tệp ⇒ **3 vòng, 8 finding**. Trả gấp ba vòng review để lấy thêm `29 %` là lỗ.
   Khi hình dạng bản vá đã chứng minh trên bộ đầu, chép sang hai bộ kia là việc rẻ.
3. **Nợ "gate chậm dần"** (`ci.yml:63` tự khai là *"nợ riêng"*; ubuntu từng `25m14s`, tức đã
   vượt trần `25` cũ). Không gộp.
4. **Song song hoá `chay_moi()`** — đã cân nhắc và BỎ: cắt đột biến khỏi Windows lấy được
   cùng khoản tiết kiệm mà không đụng `ci_dang_ky_test.py:243` `chay_moi`, vốn có phản chứng
   bám vào chữ ký hàm ("ĐƯỜNG NỐI ĐỂ ĐO, không phải cấu hình").

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | Trên Windows, vòng lặp đột biến của bộ này KHÔNG chạy. Ca **nền** vẫn chạy đủ. | `write_set` #1 |
| M2 | Trên Windows, bộ in một dòng bằng chứng **DƯƠNG** khai rõ đột biến không đo ở đây và đo ở đâu. Tiêu chí `dat` vẫn đòi bằng chứng dương, không được im. | `write_set` #1 |
| M3 | Sổ đăng ký chấp nhận dòng Windows ấy làm bằng chứng xanh, và **chỉ** khi nền là Windows. | `write_set` #2 |
| M4 | Trên Linux, hành vi KHÔNG đổi một chút nào — vẫn `34` đột biến, vẫn dòng `DOT BIEN x/y bi giet`. | `write_set` #1, #2 |

## `nghiem_thu`

**A1 (M1) — đột biến thật sự không chạy trên Windows.**
Phép làm ĐỎ: giả lập nền Windows (`os.name == "nt"`) rồi đo **số lần sinh tiến trình con**;
nếu con số ấy còn tỉ lệ với `len(DOT_BIEN)` thì ĐỎ. Không đo bằng thời gian tường — thời gian
trôi theo máy.

**A2 (M2) — chốt bằng chứng dương KHÔNG bị làm im.**
Đột biến bắt buộc: **xoá điều kiện nền** để nhánh Windows chạy trên MỌI nền. Ca đích phải ĐỎ.
Đột biến thứ hai: làm nhánh Windows in dòng **của Linux** (`DOT BIEN 0/0 bi giet`) — ca đích
phải ĐỎ, vì `0/0` chính là "tập rỗng thoả `not song`" mà bài học #319 sinh ra để chặn.

**A3 (M3) — sổ đăng ký phân biệt được nền.**
Phép làm ĐỎ: đưa dòng bằng chứng **Windows** vào một lượt chạy khai nền **Linux** ⇒ phải ĐỎ.
Và ngược lại: dòng Linux trên nền Windows ⇒ phải ĐẠT (Windows được phép đo đủ nếu ai đó chạy
tay). Hai chiều, không phải một.

**A4 (M4) — Linux không đổi.**
`python .claude/dev/ci_dang_ky_test.py --chay` trên `ubuntu-latest` phải `success`, và bản in
của bộ này phải còn nguyên dạng `TONG: CA n/n dat · DOT BIEN 34/34 bi giet`. Con số `34` là
số đo ngày 06-09-2026 — **đo lại tại lúc thi công**, đừng chép.

**A5 — bằng chứng Windows THẬT, không phải suy luận.**
`workflow_dispatch` `ci.yml` trên nhánh packet. Đòi: job `gate (windows-latest)` có
`conclusion == success` (KHÔNG phải `cancelled`), **và** bước `test registry` có
`conclusion == success` với `completed_at` đọc được — tức chứng minh nó *chạy hết*, không phải
chỉ *không đỏ*. Đọc qua `actions_list` + `method: list_workflow_jobs`.
Phép làm ĐỎ: job lại `cancelled` ở trần ⇒ A5 ĐỎ.

**A6 — không đụng hành vi nào khác.** `git diff --numstat` chỉ hiện đúng 2 đường dẫn ở
`write_set`.

## `hinh_dang_ke_thua`

Chép từ hồ sơ tiền nhiệm `CI-CAI-JSONSCHEMA` (r1→r2→r3) — bộ đếm **hình dạng lỗi**, không phải
đếm lỗi:

| hình dạng | số lần đã gặp | ghi chú |
|---|---:|---|
| nâng `timeout-minutes` để mua cổng xanh | **3** (`25` → `45` → `60`) | `ci.yml:63` tự kết luận *"NÂNG TRẦN KHÔNG CHỮA NGUYÊN NHÂN"*. Packet này **không** được lặp lần thứ tư. |
| khai một phép đo là `KHÔNG ĐO ĐƯỢC` rồi để nguyên | **1** (`CI-CAI-JSONSCHEMA-r3` A5) | Nay đã đo được. Bài học: *"không đo được"* phải kèm **công cụ nào thiếu**, kẻo nó hết hạn mà không ai biết. |
| cổng vắng mặt trông giống cổng xanh | nhiều | Job `cancelled` KHÔNG phải `failure`; `get_job_logs` trả `failed_jobs: 0`. |

Ba lần cho hình dạng thứ nhất là ngưỡng mà `CLAUDE.md` bảo phải hỏi *"có nên làm việc này
không"* thay vì *"vá thế nào"* — và câu trả lời của packet này là **không nâng trần**.

## `chua_do_duoc`

1. **Tổng thời gian thật của job Windows.** `60,2` phút là số bị cắt; bước `19`→`43` chưa từng
   chạy trên Windows ở bất kỳ lượt nào đo được. Nên **không** khẳng định được rằng cắt đột biến
   là ĐỦ để job vừa trần. A5 là phép đo trả lời câu ấy — nếu nó ĐỎ thì đó là **kết quả**, không
   phải thất bại của thiết kế, và là căn cứ cho packet kế đụng `ci.yml`.
2. **Nền của bộ này không xanh trong container phiên soạn spec.** `rc=1`, 3 ca đỏ sẵn:
   `t11_lo_336_co_that_VA_bi_chan` · `t15_cong_kiem_bang_khop_nguon_that` ·
   `t33_cong_hoi_RUNTIME_chu_khong_parse_van_ban`. CI ubuntu xanh ⇒ lệch **rig**, không phải hồi
   quy. Hệ quả thực hành: phiên thi công **không** dùng container này làm nền so sánh cho ca nền;
   phải so trên `origin/master` bằng cùng một lệnh, hai vế dựng trong MỘT lần chạy.
3. **Tỉ lệ `3x` của Windows là đo TỔNG BƯỚC, không phải đo riêng đột biến.** Giả định "đột biến
   trên Windows cũng đắt gấp ~3" là **nội suy**, chưa đo. Ước `44,3p → ~14p` đứng trên giả định
   ấy; A5 mới là thứ kiểm nó.
4. **Không có đường đo Windows tại chỗ trong phiên này** (container Linux). Mọi khẳng định về
   hành vi Windows phải đi qua CI.
