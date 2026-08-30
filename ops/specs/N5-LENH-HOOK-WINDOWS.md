# ĐẶC TẢ PACKET — `N5-LENH-HOOK-WINDOWS` **revision 1**

| | |
|---|---|
| `packet_id` | `N5-LENH-HOOK-WINDOWS` |
| `packet_issue` | **#405** |
| `revision` | 1 |
| `generation` | 1 |
| `executor` | `claude` |
| `environment` | `cloud` |
| `review_class` | **`sensitive`** — xem `vi_sao_sensitive` |
| `base` | `master` `1dedb8b5` (đo `02:48:09Z 30-08-2026`, hai nguồn khớp: `ls-remote` và `rev-parse`) |
| `assurance_target` | **`cross_approved`** (codex) **+** duyệt khác danh tính |

## `nguon_cap_viec`

Nợ **N5**, sổ nợ #395, comment `5461834774`. Chủ kho giao trực tiếp trong phiên
`2026-08-30 ~02:4xZ` sau một vòng `soan-spec` đủ 5 câu, duyệt trọn gói.

Đây **KHÔNG** phải packet khắc phục của một packet trước: `#329`/PR #342 sinh ra ca `t21`
nhưng không để lại biên nhận nào trong `ops/reviews/` (đo `02:5xZ 30-08`: `ls ops/reviews/`
không có mục nào mang `329`, `342` hay `agent-may`). Xem `hinh_dang_ke_thua`.

## `vi_sao_sensitive`

Lớp là thứ **MÁY TÍNH RA**, không phải lời khai:

```
_tinh_lop_tu_write_set([3 đường dẫn])  ⇒  sensitive
```

**ĐỌC ĐÚNG LÝ DO.** Không đường dẫn nào khớp tiền tố trong `_BANG_LOP`
(`.github/workflows/`, `.github/coordination/`, `packet_loop.py`, `launcher.py`,
`gate_lifecycle.py`, `lease_publish.py`, `tl_gws.py`). Lớp đến từ giá trị **MẶC ĐỊNH
fail-closed**, KHÔNG phải vì packet chạm authority. Vẫn áp trần `≤3 tệp / ≤300 dòng thêm`
theo fail-closed, nhưng **CẤM** khai ngược lại rằng packet "chạm authority" để mượn uy tín
của cụm từ ấy.

## `write_set`

Đúng ba đường dẫn. Trần `sensitive` là 3 tệp ⇒ **không còn chỗ trống**.

| đường dẫn | phủ lối sửa nào |
|---|---|
| `.claude/hooks/subagent_ghi_detect_test.py` | ca `t21` — cả đo (Đ1) lẫn sửa lối 2 và lối 3 |
| `.claude/settings.json` | lệnh hook `bash -c` — lối 1 |
| `.claude/hooks/subagent_ghi_detect.py` | detector — chỉ nếu phép đo chỉ vào nó |

Lease đo `02:48Z 30-08-2026`: cả ba đường dẫn `NGƯỜI_GIỮ 0`.

## `ngoai_pham_vi`

1. **`.github/workflows/**` — KHÔNG chạm.** Thêm nó là 4 tệp ⇒ vượt trần ADR-0044 cho
   `sensitive`; và §8 loại workflow khỏi patch-as-hint đúng vì đó là tầng thẩm quyền.
   Phép đo cho thấy bắt buộc phải sửa `ci.yml` ⇒ **DỪNG** (điều kiện dừng `S3`).

2. **Hai bộ `cach_ly` đỏ vĩnh viễn trên Windows — KHÔNG thuộc packet này.** Đo
   `02:5xZ 30-08` trên `master` `1dedb8b5`:

   ```
   moi_truong_hien_tai()  đòi RUNNER_OS == "Linux"   ⇒ windows-latest trả None
   dem_la_do(None, o_trong_ci=True)  ⇒ True          (fail-closed, chủ ý #401)
   ```

   Hai bộ `cach_ly` (`mcp_gh_test.py`, `pretooluse_guard_test.py`) đều neo
   `github-actions/linux`, nên trên Windows chúng **luôn** ở trạng thái thứ ba ⇒ **luôn ĐỎ**.

   **Hệ quả phải khai thẳng: packet này KHÔNG làm `master` xanh.** Nó đưa số dòng
   `CI_DANG_KY ... ĐỎ` trên Windows từ **3 xuống 2**; `TỔNG` vẫn `ĐỎ`. N5 là dòng đỏ duy
   nhất **do lỗi mã**, không phải dòng đỏ duy nhất. Ai chờ master xanh sau packet này sẽ
   kết luận sai rằng packet thất bại.

   Với tới hai bộ ấy cần thêm 2 tệp ⇒ 5 tệp ⇒ vượt trần. Chúng là **nợ riêng**, và theo
   `hinh_dang_ke_thua` bên dưới, lối đúng cho chúng là **xem lại thiết kế**, không phải vá.

3. **Không sửa `ci_dang_ky_test.py`.** Packet #401 vừa land trên chính tệp ấy và cố ý làm
   Windows đỏ thêm `1 → 3`. Đụng vào là hồi quy packet vừa xong.

## `muc_tieu`

Hai mục tiêu, **CÓ THỨ TỰ** — Đ2 không được bắt đầu trước khi Đ1 có kết quả.

| # | mục tiêu | chiếu vào (L2) |
|---|---|---|
| **Đ1** | Thu **vân tay** trên `windows-latest` THẬT: cái gì sinh `rc=1`. Ca `t21` hiện vứt `stdout` đi và chỉ giữ `stderr` — mà `stderr` RỖNG chính là lý do ta đang mù. Làm ca báo cáo đủ: đường dẫn thật `bash` phân giải về, `bash --version`, và `stdout` của lệnh hook. | `.claude/hooks/subagent_ghi_detect_test.py` |
| **Đ2** | Sửa theo đúng thứ tự ba lối ở `thu_tu_ba_loi`, dùng thứ Đ1 đo được. | lối 1 ⇒ `.claude/settings.json` · lối 2 và 3 ⇒ `.claude/hooks/subagent_ghi_detect_test.py` · chỉ khi Đ1 chỉ đích danh ⇒ `.claude/hooks/subagent_ghi_detect.py` |

Đ1 có giá trị ở lại kể cả khi Đ2 đi lối nào: một ca nuốt `stdout` là một ca không chẩn
đoán được, và đó là khuyết tật độc lập với N5.

## `thu_tu_ba_loi` — phiên KHÔNG được tự đổi thứ tự

1. **Lệnh hook hỏng thật trên Windows** ⇒ sửa `.claude/settings.json`. Ca `t21` giữ nguyên
   từng byte. Đây là lối tốt nhất: sửa sản phẩm, và ca cũ chứng minh việc sửa có tác dụng.
2. **Ca `t21` gọi sai cách** (khuyết tật ở vỏ bọc, không ở sản phẩm) ⇒ được sửa ca, **nhưng
   BẮT BUỘC kèm đột biến chứng minh ca vẫn ĐỎ ĐƯỢC** (tiêu chí `A3`). Ca không đỏ được
   không phải ca.
3. **Hook thật sự không chạy được trên Windows** ⇒ khai **trạng thái thứ ba CÓ TÊN, CÓ LÝ
   DO**, theo đúng tiền lệ đang chạy trong kho:
   `BO QUA t55_doctor_nhan_python_khong_can_ten_python3: bo qua tren Windows (can shim khong duoi .exe)`.
   **Lối này CẦN CHỦ KHO DUYỆT RIÊNG — phiên không tự chọn** (điều kiện dừng `S4`).

Vì sao phải chốt trước khi biết đáp án: sửa ca cho hết đỏ làm `master` bớt đỏ trong năm
phút và **bảo chứng biến mất** — đúng họ lỗi `CLAUDE.md` gọi là *"cổng vắng mặt trông giống
cổng xanh"*. Lúc đã biết đáp án thì ai cũng có động cơ đọc lối 2 rộng ra.

## `nghiem_thu`

Mỗi tiêu chí nói rõ **phép đo nào làm nó ĐỎ** (L3).

### `A1` (Đ1) — vân tay đọc được

Log job `windows-latest` của lượt dispatch thứ nhất phải chứa CẢ BA: (a) đường dẫn thật
`bash` phân giải về; (b) `bash --version` dòng đầu; (c) `stdout` của lệnh hook cho ít nhất
một trong bốn tổ hợp.

**ĐỎ khi**: thiếu bất kỳ mảnh nào trong ba, hoặc `t21` vẫn chỉ in `rc=N` mà không kèm
`stdout`. Rỗng-vì-lệnh-không-in-gì vẫn phải in ra chữ `stdout RỖNG`, không được vắng mặt —
vắng mặt và rỗng là hai kết luận khác nhau.

### `A2` (Đ2) — ca xanh trên nền thật

Trên `windows-latest`: `t21` cho **`4/4`** (đơn vị: tổ hợp sự-kiện × nền, tổng `2 × 2`).

**ĐỎ khi**: bất kỳ tổ hợp nào `rc != 0`, hoặc dòng kết quả không phải `dung 4/4`.

### `A3` (Đ2) — CHỐNG RÚT RUỘT CA, tiêu chí quan trọng nhất

Phải có một đột biến **CÓ TÊN** gỡ đúng thứ `t21` sinh ra để canh — nhánh dự phòng
`CLAUDE_PROJECT_DIR` trong lệnh của `.claude/settings.json` — và đột biến ấy phải làm
`t21` **ĐỎ**.

**ĐỎ khi**: áp đột biến mà `t21` vẫn xanh. Khi ấy ca đã bị rút ruột, bất kể `A2` xanh.

Đo trên Linux (rẻ, và đủ: nhánh dự phòng là bất biến độc lập nền). Mỗi đột biến một **CÂY
RIÊNG**, chạy `python -B`, phân hạng bằng **so TỪNG CA CÓ TÊN với nền** — KHÔNG bằng
`rc != 0`, vì `rc != 0` cấp tín dụng giả cho đột biến chết vì lỗi vô can.

### `A4` (Đ1+Đ2) — không hồi quy phần còn lại

Trên Linux, `python -B .claude/hooks/subagent_ghi_detect_test.py` phải giữ nguyên hoặc hơn
nền đo `02:0xZ 30-08-2026` tại `1dedb8b5`:

```
TONG: CA 30/30 dat · DOT BIEN 18/18 bi giet
TONG: DAT      (rc=0)
```

**ĐỎ khi**: số ca đạt `< 30`, hoặc số đột biến bị giết `< 18`, hoặc `rc != 0`.

### `A5` (Đ2) — số dòng đỏ trên Windows, khai đúng con số

Trên `windows-latest`, bước `test registry`: số dòng `CI_DANG_KY ... ĐỎ` phải bằng **2**,
và **không** dòng nào trong đó là `subagent_ghi_detect_test.py`. `ĐĂNG KÝ` phải vẫn `21/21`,
`TRẠNG THÁI` vẫn `chan=19 cach_ly=2`.

**ĐỎ khi**: số dòng `!= 2`; hoặc `subagent_ghi_detect_test.py` còn trong danh sách; hoặc
`ĐĂNG KÝ != 21/21`; hoặc `chan/cach_ly` đổi.

**KHÔNG được viết tiêu chí `TỔNG: ĐẠT` hay `master xanh`** — xem `ngoai_pham_vi` mục 2:
hai dòng còn lại nằm ngoài packet, nên `TỔNG` vẫn `ĐỎ` và đó là **ĐẠT**, không phải trượt.

### `A6` — cách đếm dòng log phải tự chứng minh là đếm ĐỦ

Mọi phép đếm dòng qua `get_job_logs` phải in kèm `original_length` và số dòng nhận được, và
phải chỉ ra mốc thời gian dòng đầu phần trả về **sớm hơn** mốc bắt đầu bước 13.

**ĐỎ khi**: không trình được hai mốc ấy. Đo `21:5xZ 29-08`: công cụ trả `500` dòng trên
`original_length: 1180` — **log BỊ CẮT**, và hai lần vừa rồi đếm đúng chỉ vì chỗ cắt rơi
trước bước 13. Đếm mà không kiểm chỗ cắt là đếm trên mẫu bị cắt đội lốt đếm đủ.

## `ngan_sach_do_tren_windows`

Trần **3 lượt** `ci.yml` `workflow_dispatch` cho cả packet. **Lượt 1 BẮT BUỘC là lượt thu
vân tay (`A1`), không phải lượt thử sửa.**

Giá đo `20:29Z`–`21:22Z 29-08-2026`: windows `51m19s`–`54m54s` × hệ số 2, cộng ubuntu
`20m13s`–`25m53s` ⇒ **≈ 122–136 phút TÍNH TIỀN mỗi lượt**. Kho ĐÃ cạn hạn mức Actions một
lần thật (`ci.yml` r245). Kênh rẻ `launcher-windows.yml` (windows `5m13s` ⇒ ~10 phút tính
tiền) **KHÔNG** chạy được `t21`, nên không thay thế được.

Chạm trần 3 mà chưa xanh ⇒ `blocked` + failure evidence. **Không tự xin thêm lượt.**

## `hinh_dang_ke_thua` — L4

**Không chép được bộ đếm tiền nhiệm.** `#329`/PR #342 sinh ra `t21` nhưng `ops/reviews/`
không có biên nhận nào của nó (đo `02:5xZ 30-08`). Bộ đếm dưới đây do **chính packet này**
mở; packet kế nhiệm nào phải chép sang, đừng nạp lại từ 0.

**Hình dạng: *"chốt neo vào Linux, gặp Windows thì không phán quyết được — mà vẫn được khai
như đã phủ mọi nền."***
Đơn vị: *số chốt của kho lộ ra là không chạy hoặc không phán quyết được trên `windows-latest`.*

| # | chốt | bằng chứng |
|---|---|---|
| 1 | `t21_lenh_hook_chay_duoc_khi_CLAUDE_PROJECT_DIR_KHONG_DAT` | `0/4`, `rc=1`, `stderr` rỗng — lượt `33262325596`, `33271198556`, `33271297325` |
| 2 | `t55_doctor_nhan_python_khong_can_ten_python3` | đã mang bỏ-qua CÓ TÊN trên Windows — log job `99149860673` |
| 3 | hai bộ `cach_ly` neo `github-actions/linux` | `moi_truong_hien_tai()` đòi `RUNNER_OS == Linux` ⇒ Windows luôn `None` ⇒ luôn đỏ |

**BA lần.** `PROTOCOL §12`: *"Cùng hình dạng lỗi xuất hiện lần thứ ba bắt buộc xem lại có nên
tiếp tục cách làm đó, không chỉ vá lần thứ tư."*

Packet này **CỐ Ý chỉ xử mục 1** — mục 1 là lỗi mã có nguyên nhân đo được. Mục 3 là **câu
hỏi THIẾT KẾ**, không phải chỗ vá: nó hỏi *"một chốt neo một nền thì trên nền khác phải đọc
là đỏ, hay là không-áp-dụng?"*, và trả lời nó bằng cách nới write set của packet này chính là
vá lần thứ tư. Lối đúng: **nợ riêng**, đi qua Packet/Mission riêng.

## `chua_do_duoc`

1. **Nguyên nhân gốc của `rc=1`.** Chưa đo. Giả thuyết mạnh nhất — `bash` phân giải về
   `System32/bash.exe` (vỏ WSL) thay vì Git Bash, thoát `1` và báo ra `stdout` — khớp vân
   tay `stderr` rỗng, nhưng **là giả thuyết**. Đối thủ (`command -v python3` hỏng) đã yếu đi
   bằng bằng chứng miễn phí: log job `99149860673` cho thấy runner Windows CÓ `python3` thật
   tại `hostedtoolcache/windows/Python/3.11.9/x64/python3.exe`. Đ1 tồn tại đúng để đóng chỗ này.
2. **Lối sửa cuối cùng.** Phụ thuộc (1). Ba lối đã chốt trước, thứ tự cứng.
3. **Hạn mức Actions còn lại.** Không đo được từ phiên này: proxy chặn `api.github.com/repos/*`,
   và MCP không có tool đọc billing. Trần 3 lượt là **phòng ngừa**, không phải tính từ số dư thật.
4. **Kích thước diff cuối.** Chưa đo được vì lối sửa chưa biết. Tiền lệ ba tệp này:
   `1a0df2a` = `+341/−35` — **đã vượt 300**. Trần chật thật, phải đo lại trước mỗi công bố.

## `dieu_kien_dung`

- `S1` cần đường dẫn thứ tư ⇒ DỪNG, trình phép đo.
- `S2` vượt `≤3 tệp / ≤300 dòng thêm` ⇒ DỪNG, **KHÔNG tự khai cổng ADR-0044 là ĐẠT**.
- `S3` phải sửa `.github/workflows/**` ⇒ DỪNG.
- `S4` phép đo chỉ vào **lối 3** (bỏ qua có tên) ⇒ DỪNG, xin chủ kho duyệt riêng.
- `S5` chạm trần 3 lượt dispatch mà `A2` chưa xanh ⇒ DỪNG, `blocked`.
- `S6` `origin/master` đi tiếp so `base` mà chưa đo lại ⇒ DỪNG.
- `S7` `A4` hồi quy (ca `< 30` hoặc đột biến bị giết `< 18`) ⇒ DỪNG.
- `S8` phát hiện phải đụng `ci_dang_ky_test.py` hay hai bộ `cach_ly` ⇒ DỪNG, đó là packet khác.

## `canh_bao_cho_nguoi_thi_hanh`

1. **Packet này KHÔNG làm `master` xanh.** `3 → 2` dòng đỏ, `TỔNG` vẫn `ĐỎ`. Đó là ĐẠT.
   Đừng "sửa" thêm cho master xanh — đó là cách nhanh nhất để hồi quy packet #401.
2. `stderr` RỖNG không phải "không có lỗi", nó là **kênh sai**. Đọc `stdout`.
3. Hook `subagent_ghi_detect.py:43` đặt `_MA_CLEAN = _MA_CHANGED = _MA_UNKNOWN = 0` — hook
   **không thể** sinh `rc=1`. Ai chẩn đoán ra "hook trả 1" là đã đi sai nhánh.
4. `core.abbrev=7` phải ghim TRONG mọi clone/sandbox, không thì `doc-claims-check --strict`
   cho `rc=2` oan.
5. KHÔNG `git push` thẳng master. KHÔNG ép qua ruleset. Đăng/đọc GitHub qua `mcp_gh.py`.
6. Đăng xong thân PR/Issue thì **đọc ngược về và `diff`**: cặp ngoặc nhọn bị nuốt trên đường
   đăng/đọc. Chênh lệch thực thể HTML thì `html.unescape(da_den) == goc` ⇒ chỉ là tạo tác
   đường đọc, ĐỪNG ghi thành finding.
