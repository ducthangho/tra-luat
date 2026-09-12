# EVIDENCE — vòng review 9, PR #512 / packet #504

Mọi con số dưới đây là **lời khai**. Việc của bạn là **ĐO LẠI**. Chỗ nào tôi khai rộng hơn phép đo, đó
là một finding.

## Neo — write set KHÔNG đổi một byte kể từ vòng 7

| | |
|---|---|
| `reviewed_sha` | `36f68c7e95e0de1fcf8e2311db33a164816db20f` — **y hệt vòng 7 và vòng 8** |
| base / `merge-base` | `bb7013c7669da19304a8769e5b25f8c1f8951e9c` |
| write set exact | `ops/lease_publish_test.py` · `ops/chay_lease_publish_test.sh` |
| lease | `windows-lease-suite-exec-2-claude-20260912`, gen 2, hết `2026-09-13T14:22:00Z` |
| vòng | **9**; đã dùng 8/10 |

**Không có thay đổi mã nào trong PR giữa vòng 7, 8 và 9.** Kiểm điều đó trước — nếu nó sai thì mọi kết
luận `ĐÃ VÁ THẬT` của hai vòng trước phải xét lại.

## Việc đã làm sau vòng 8 — TẤT CẢ ngoài write set

Vòng 8 để lại **một** lớp P1: `F6` (bộ đo đột biến `dotbien512.py`). Chủ kho quyết **dời `F6` sang packet
riêng** — chỉ thị bền **#504 comment `5646460376`**.

1. **Issue `#530`** `CHAM-DOT-BIEN-MIEN-NHIEM-LEASE-SUITE` + spec **đóng băng**
   `SPEC-packet-F6-530.md`, sha256 `5fcc14b5e33ecf130172bc1cafbb0ca229ddae8363069284eba5fcca49602781`.
   **Chưa có lease.**
2. **Nợ có tên**: `ops/NO_KY_THUAT.md` **§23**.
3. **Lease gen 2** đã đăng (marker #504 comment `5646489814`), vì gen 1 hết hạn `14:05:00Z`.
4. **Bản bộ đo mặc định chọn bằng phép đo** trên **10 control** — xem dưới.

### `F6` hoá ra là một PORT, không phải thiết kế mới

Kiến trúc cần cho `F6` **đã land**: packet `CHAM-DOT-BIEN-MIEN-NHIEM-CA-VO-CAN`, Issue **`#513`**,
closed-completed. `cay-kho/ops/nhanh_don_duoc_test.py` đã có `TinHieuChotCa` (`:30`), `chot()` (`:34`),
ba trạng thái (`:48`), `sinh_dau_phien()` (`:51`), **kênh JSONL** neo `(dau_phien, mutant, lan_thu)`
(`:70`–`:72`), `dong_luot(rc)` (`:83`), `doc_kenh` (`:90`), `DOT_BIEN_TU_KIEM` (`:2236`).

Và `ngoai_pham_vi` #4 của `#513` ghi rõ *"KHÔNG đụng `ops/lease_publish_test.py` — #504 giữ"*. Tức `F6`
là **hệ quả đoán được của một write-set exclusion**. **Kiểm lời khai này** — nó là lập luận trung tâm cho
việc dời `F6` ra khỏi PR.

### Bản bộ đo — ba biến thể, cùng 10 control, khác nhau đúng MỘT dòng

| bản | tệp trong `do-cua-tac-gia/` | đúng | **lọt** (false GREEN) | **hồi quy** (false RED) |
|---|---|---|---|---|
| `v0` tiền tố bắt buộc | `dotbien512_REGEX_CU.py` | `4/10` rc=1 | 6 | 0 |
| `v6` hậu tố tuỳ chọn | `dotbien512_VA_VONG6.py` | `7/10` rc=1 | 3 | 0 |
| **`v8` (MẶC ĐỊNH)** | **`dotbien512.py`** | `7/10` rc=1 | 2 | **1** |

Lý do giữ `v8` dù vòng 8 xếp bản vá ấy là `VÁ SINH LỖI MỚI`: **cả BỐN** lớp ngoại lệ của kho —
`BoQuaNen`, `Chan`, `HetNganSachDay`, `TinHieuChotCa` — thiếu hậu tố `Error`/`Exception`, nên `v6` cấp
tín dụng giả **4/4** còn `v8` bắt **4/4**. Tập lọt của `v6` **không có biên**; hồi quy của `v8`
**đếm được**: `8/454` assertion, 4 ca (`t96 t133 t136 t151`).

**Bộ đo được giao ở trạng thái TỰ BÁO ĐỎ** (`7/10`, `rc=1`) — cố ý.

## Đã đo trên `36f68c7` — kèm ĐIỀU KIỆN ĐO

| phép đo | kết quả khai |
|---|---|
| suite đầy đủ | `155/155 đạt; đã chạy=155, bỏ qua=0` ở **`[A]` (log 1055) · `[B]` (1060) · CHA (1156)**; **0** dòng `  ĐỎ  `; rc=0 |
| `t125` · `t158` · `t160` ở CHA | `55.445s` · `3.381s` · `0.066s`, QUA |
| catalogue 16 đột biến, bộ đo mặc định + 10 control | `16/16 giết thật, 0 tín dụng giả, 0 sống sót`, rc=0, **không ca nào đổi phân hạng** so lần đo trước |
| `doctrine-scan` · `adr-song` | rc=0, `7 tệp / 0 chỗ chép` · rc=0, `47 ADR / 47 dòng §20` |
| `git diff --numstat bb7013c 36f68c7` (2 đường) | **+1101 / −27** (`1095 + 6`) |

**ĐIỀU KIỆN ĐO của `155/155`:** `actionlint 1.7.7` + **`shellcheck 0.9.0`**, Linux, python 3.11.15.
Thiếu `shellcheck` ⇒ `t137`/`t159` ĐỎ với `KHÔNG ĐO ĐƯỢC` — **fail-close đúng thiết kế**, không phải hồi
quy. Log của **cả hai** lượt có trong `do-cua-tac-gia/`.

## TỰ KHAI các lỗi của chính tôi mà hai vòng trước bắt được — và một lỗi MỚI

Tất cả đã đính chính bằng hồ sơ (`do-cua-tac-gia/ERRATA.md`), **không sửa byte** hiện vật lịch sử.

| ID | khai sai | đúng |
|---|---|---|
| `N31`/`N31-b` | "5 mutant sống" | **6** |
| `N32`/`N32-b` | `+1114`, số hạng `1076+32`, dư `386` | **+1101** (`1095+6`), dư **399** |
| `N37` | "~8,5 phút" | **895 s = 14 ph 55 s** |
| `N38` | F7 `6/6` | F7 có **năm** phần tử ⇒ `5/5`; `N10` thuộc **F2** |
| `N39` | "7/10 sau khi phóng" | **8/10** |
| **MỚI** | "**BA** lớp ngoại lệ của kho" | **BỐN** — bộ lọc base class bỏ mất `HetNganSachDay` |

**Và một lỗi PHÉP ĐO, tự khai:** phép đo `8/454` cùng phép đếm lớp ngoại lệ có **một lần chạy trên cây
SAI** — nhánh hồ sơ nền `master` (`147` ca) thay vì `36f68c7` (`155` ca, có `t153`–`t160`). Lộ ra vì
`t153`–`t160` **vắng mặt** trong kết quả. Chữa bằng **ghim BLOB** (`git show 36f68c7:…`) thay vì tin
nhánh đang checkout. **Kiểm cả lời đính chính này** — nếu nó cũng sai thì đó là finding nặng hơn.

## `KHÔNG ĐO ĐƯỢC` — đừng đọc thành ĐẠT

- **`A3`/`A4` Windows**: không lượt Windows nào chạy trên head này (chỉ thị chủ kho: **không CI bằng
  tay**; `full CI` và `CI Windows` **chỉ đến khi merge**). Linux `155/155` **không** chứng nhận Windows.
  Các mốc thời gian Windows trong docstring (`N07`, `N11`–`N15`, `N17`, `N18`, `N30` của vòng 7)
  **thiếu log nguồn trong kho** — nợ hồ sơ có thật, chưa chữa.
- **Chống giả mạo tín hiệu của catalogue**: bộ đo chạy ngoài tiến trình, đọc CHUỖI ⇒ `KHÔNG ĐO ĐƯỢC`
  đầy đủ. Đây là lý do packet `#530` tồn tại.
- **`S8-bo-deadline`**: gốc trong `ops/lease_publish.py`, ngoài write set (`S3`).
- **`A5`**: `KHÔNG ĐẠT` — `1101 > 300`; override lên `1500` **không** đổi nhãn nghiệm thu đóng băng.
- **Lượt workflow đăng lease gen 2 ĐỎ** (`run 34699156658`): không phải lỗi gen 2 — workflow lặp qua
  **mọi** tệp lease đổi trong push, và tệp gen 1 (chạm chỉ để mang bia mộ) bị từ chối đúng vì **đã hết
  hạn**. Khai thành nợ mới; `.github/workflows/**` ngoài write set.
- **Trạng thái GitHub trực tiếp** từ sandbox: `KHÔNG ĐO ĐƯỢC` (không mạng).
