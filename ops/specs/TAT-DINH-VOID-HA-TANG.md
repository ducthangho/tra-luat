# ĐẶC TẢ ĐÓNG BĂNG — `TAT-DINH-VOID-HA-TANG`

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md`
> §3.2, §4) mới được bắt tay. Phiên nào đọc rồi tự làm là tự cấp việc cho mình.
>
> Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**.

`packet_id`: `TAT-DINH-VOID-HA-TANG`
`packet_issue`: `CHUA_CO` — người giữ kho chưa mở. **Không bịa số.**

`review_class`: **`sensitive`** — packet sửa `packet_loop.py`, tức chính bộ cưỡng chế trần
attempt. Sai một chiều thì hoặc khoá cứng packet trên máy đủ công cụ, hoặc mở cửa hậu hoàn
mọi lượt hỏng thật.

## `nguon_cap_viec`

Người giữ kho hỏi trực tiếp trong phiên 22-08-2026: *"Về số lần attempt, đang là 2 lần có ít quá
không, một số môi trường chưa có đủ công cụ nên khi chạy gây ra lỗi… những vấn đề này đã được ghi
chép trong skill chưa, đã tất định hoá chưa"*, rồi duyệt soạn packet.

**Packet này KHÔNG nới trần** — xem B1. Nó đóng đúng cái lỗ làm câu hỏi ấy nảy ra.

`docs/PROTOCOL_DA_PHIEN.md`:767 tự khai việc này còn nợ:

> *"Launcher chỉ ghi bằng chứng và giữ kill-tree/rc `124/125`; nó **không tự động** `void-attempt`.
> **Tự động phân loại infrastructure void cần Packet và phản chứng riêng ở packet-loop.**"*

Packet này đi làm đúng cái đã được hoãn ở đó, không phát minh thêm luật.

## Bằng chứng — ĐO, không suy

### B1. Trần attempt là **3**, không phải 2 — và nới nó là SAI THUỐC

Ba trục **độc lập**; `ADR-0043` tách thẳng (*"trục VÒNG tách khỏi trục LỜI GỌI và trục ATTEMPT"*).
Đo trên lease `ci-bang-phu-thuoc-exec-1-claude-20260822`:

```
attempts_limit: 3          <- so lan tuyen bo DONE          (protocol §12:729 "Mac dinh: 3 attempt/packet")
review_rounds_limit: 2     <- canon ADR-0043                (con so "2" thuong bi nho nham la attempt)
executor_calls_limit: 6
review_calls_limit: 2
```

Nới 3→5 làm mỗi packet chịu được nhiều lượt hỏng hơn mà **vẫn không phân biệt** *"hỏng vì mã sai"*
với *"hỏng vì máy thiếu `rg`"* — tức mất luôn tín hiệu mà trần attempt sinh ra để phát. Cơ chế
đúng đã có sẵn: `void-attempt` hoàn lượt với `LY_DO_VOID = ("quota","rate_limit","infrastructure","permission")`.

### B2. `begin-attempt` KHÔNG đo môi trường — lượt mở ra được trên máy thiếu công cụ

Đọc toàn thân `cmd_begin_attempt` (`packet_loop.py:773-830`): kiểm `state`, kiểm lược đồ lease
(`_kiem_luoc_do_lease`, fail-closed, có finding `legacy-lease-bypass` đã đóng), kiểm `provider`.

```
sed -n '773,830p' .claude/dev/packet_loop.py | grep -cE "cong_cu|doctor|tool|moi_truong|shutil.which"
=> 0
```

**Không một dòng nào** về công cụ. Nên lượt mở ra bình thường trên máy thiếu `rg`/`codex`/`gh`,
chạy, chết, và bị đếm — trừ khi có người **nhớ** gõ tay `void-attempt`.

Và lease cũng không đỡ: quét lease của #245 tìm trường điều kiện công cụ/nền ⇒ **rỗng**.

### B3. `void-attempt` nhận lý do theo LỜI KHAI, không theo bằng chứng

Đây là chỗ tinh tế nhất, và một phép đo cẩu thả đã suýt làm hỏng đặc tả này. Lượt đo ĐẦU của
phiên soạn kết luận *"0 ca test cho `void-attempt`"* — **SAI**. Phép grep dùng mẫu tên `tNN_`
trong khi bộ ấy đặt tên `case_*`. Đo lại: **34** lần nhắc, ít nhất bốn ca có tên riêng
(`case_void_attempt_allowlist`, `case_void_attempt_ly_do_tu_che_bi_tu_choi`, ca `reviewing`,
ma trận codepage), và lệnh đã qua **hai** lượt cross-review (finding
`void-reviewing-accepts-attempt-zero` lượt 6; đột biến phối hợp lượt 7).

**`void-attempt` được canh KỸ.** Nó từ chối lý do ngoài allowlist, từ chối khi `attempts_used <= 0`,
và từ chối hoàn lượt **đã có review** — chú thích của chính nó nói vì sao: *"nếu không, mọi lượt
hỏng đều biến thành «quota» và trần trở thành trang trí"*.

Cái còn thiếu **không phải** phản chứng. Là thứ khác:

```
sed -n '831,870p' .claude/dev/packet_loop.py | grep -nE "bang_chung|evidence|ma_thoat|rc=|stdout_byte|run.json"
=> 3 cho khop, CA BA nam trong CHU THICH, khong phai ma
```

Allowlist trả lời *"chữ này có phải một lý do hợp lệ không"*. Nó **không** trả lời *"lý do này có
THẬT không"*. Gõ `--reason infrastructure` cho một lượt chết vì mã sai thì lệnh nhận, `rc=0`.

Đây **không** phải ca *"danh sách cấm thua từ trong thiết kế"* — allowlist ở đây đúng hình dạng.
Đây là một tầng khác: **allowlist canh TỪ VỰNG, không canh SỰ THẬT.**

### B4. Phần công cụ thì ĐÃ tất định — không cần làm lại

Ghi ra để packet không đi sửa thứ đang chạy tốt:

- `CONG_CU` khai bắt buộc **theo NỀN**: `claude`/`codex`/`gh` mang `{"mac_dinh":…, "remote":…, "ci":…}`.
- Mã thoát riêng: **12** thiếu công cụ bắt buộc · **13** có mặt nhưng chưa xác thực.
- `launcher_test.py` neo hai mã ấy ở **14** chỗ, ca thật `t53` `t54` `t73` `t105` `t106`.
- `doctor --json` đã trả sẵn hình dạng dùng được:
  `ok` · `ok_kha_dung` · `he_dieu_hanh` · `thieu_bat_buoc` · `chua_xac_thuc` · `chua_chung_minh`.
  **Hai khoá `ok` và `ok_kha_dung` tách nhau** — đúng phân biệt *có mặt* vs *dùng được*.

Nên packet này **tiêu thụ** `doctor`, không viết lại phép đo công cụ.

## `write_set`

Đúng hai tệp:

- `.claude/dev/packet_loop.py`
- `.claude/dev/packet_loop_test.py`

### ⚠ Va chạm đã biết với `KET-QUA-PHU-DINH`

`ops/specs/KET-QUA-PHU-DINH.md` (`97948dc3…`) cũng khai `.claude/dev/packet_loop.py` trong
`write_set`, tuy chỉ ở dạng **có điều kiện** (*"mở rộng `adr-song` chỉ ở phần đọc bảng §20
**nếu cần**"*). Hai packet **không được cấp lease chồng lấn**.

Thứ tự đề xuất: packet này **đi TRƯỚC** (nó chạm `cmd_begin_attempt`/`cmd_void_attempt`, vùng mà
`adr-song` không đụng), rồi `KET-QUA-PHU-DINH` rebase lên. Người giữ kho quyết; đặc tả **không tự
sắp lịch cho packet khác** — nó chỉ khai va chạm để không ai cấp mù.

## `ngoai_pham_vi`

- **KHÔNG nới bất kỳ trần nào.** `attempts_limit` giữ 3; đổi trần là `ADR-0043`/`ADR-0034`, không
  phải packet này.
- **KHÔNG viết lại phép đo công cụ** — `launcher.py doctor` đã có và đã có phản chứng (B4).
- **KHÔNG sửa `SKILL.md`.** Công cụ dev không thuộc hiện vật phát hành Cowork; quét 307 dòng
  `SKILL.md` chỉ ra hai chỗ khớp và cả hai là lệnh runtime (`tl doctor`, `profile-doctor`).
  Nhét vào đó vừa sai chỗ vừa tốn trần 200 tệp.
- `ops/lease_publish.py` — write set **đang bị giữ** bởi `LEASE-HOI-TOAN-KHO`.

## `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| **M1** | `begin-attempt` đòi **bằng chứng dương về môi trường**: một ảnh `doctor --json` cho ĐÚNG nền, `thieu_bat_buoc` rỗng. Thiếu/không đọc được ⇒ **từ chối mở lượt** (mã thoát riêng), không mở rồi tính | `packet_loop.py` |
| **M2** | Bằng chứng phải **TƯƠI**: ảnh `doctor` cũ hơn ngưỡng, hoặc chụp trên `he_dieu_hanh` khác máy đang chạy ⇒ từ chối. Ảnh cũ là lời khai về một máy khác | `packet_loop.py` |
| **M3** | `void-attempt --reason infrastructure|permission` đòi **bằng chứng máy**: mã thoát `12`/`13` của launcher, hoặc `trang_thai` + `ma_thoat` trong `run.json`, hoặc `stdout_byte: 0` kèm rc≠0. `quota`/`rate_limit` giữ nguyên đường cũ | `packet_loop.py` |
| **M4** | **Đường thoát PHẢI ĐƯỢC GHI, không được im lặng**: `--khong-co-bang-chung` đòi khối kiểu `nang_tran` (`ai_cho_phep`, `can_cu`) và ghi vào `history`. Không có nó thì M3 sẽ khoá cứng đúng ca mà môi trường chết trước khi kịp ghi sổ | `packet_loop.py` |
| **M5** | **BA trạng thái** cho phép đọc bằng chứng: `co` · `khong` · **`khong_doc_duoc`**. Cái thứ ba **không** được coi là `khong` (fail-close về phía từ chối), và phải in ra khác nhau | `packet_loop.py` |
| **M6** | Phản chứng cho từng luật + đột biến giết đúng ca của nó, đặt tên theo idiom `case_*` của bộ hiện có | `packet_loop_test.py` |

## `nghiem_thu`

| # | nghiệm thu | phép đo làm nó ĐỎ |
|---|---|---|
| **N1** | `begin-attempt` **từ chối** khi `doctor` báo `thieu_bat_buoc` khác rỗng | đột biến bỏ phép kiểm ⇒ ca ĐỎ. Đây là ca tái hiện đúng B2 |
| **N2** | `begin-attempt` **ĐẠT** khi `doctor` sạch — chiều **BẮT OAN** | ca chiều-tha; giết bằng đột biến **SIẾT THÊM** (đòi cả `chua_chung_minh` rỗng), và đột biến ấy phải **KHÔNG** làm N1 đỏ |
| **N3** | Ảnh `doctor` chụp trên `he_dieu_hanh` khác ⇒ từ chối | đột biến bỏ so nền ⇒ ĐỎ |
| **N4** | `void-attempt --reason infrastructure` **không có** bằng chứng ⇒ từ chối | đột biến nhận theo lời khai (hành vi HIỆN TẠI) ⇒ ĐỎ. Ca này chính là phản chứng cho B3 |
| **N5** | `--khong-co-bang-chung` thiếu `ai_cho_phep` ⇒ từ chối; có đủ ⇒ ĐẠT **và** `history` có dấu vết | đột biến bỏ ghi `history` ⇒ ĐỎ. Cửa thoát không ghi sổ là cửa hậu |
| **N6** | `quota`/`rate_limit` **không** đòi bằng chứng máy — chiều BẮT OAN | đột biến bắt cả bốn lý do ⇒ chỉ N6 ĐỎ, N4 vẫn xanh |
| **N7** | Ảnh `doctor` hỏng cú pháp ⇒ `khong_doc_duoc` ⇒ từ chối, **không** rơi về `khong` im lặng | đột biến gộp hai trạng thái ⇒ ĐỎ |
| **N8** | **Delta so master = 0**, và nền đo **TRONG worktree của chính kho** | chép tệp ra thư mục rỗng cho ĐỎ GIẢ — đã trả giá 4 lần |
| **N9** | Bốn ca `void-attempt` **có sẵn** vẫn xanh | chúng canh chốt đã qua hai lượt cross-review; làm đỏ một trong bốn là **hồi quy**, không phải tiến bộ |

## `hinh_dang_ke_thua`

Nợ để lại **có chủ đích**: packet này làm `begin-attempt` **đòi** bằng chứng, nhưng **không** làm
lệnh nào tự chạy `doctor` hộ. Tự động hoá bước chụp là việc sau — và nó cần quyết định riêng, vì
một lệnh tự chụp rồi tự duyệt ảnh của chính mình thì phép đo mất tính độc lập.

## `chua_do_duoc`

- **Không đo được lý do `quota`/`rate_limit` có thật không.** Chúng ở phía nhà cung cấp, không để
  lại dấu vết máy trong kho. M3 vì thế **chỉ** siết hai lý do có dấu vết đo được, và đặc tả khai
  thẳng thay vì hứa siết cả bốn — *"PHẠM VI TUYÊN BỐ phải bằng phạm vi ĐO ĐƯỢC"*.
- **RỦI RO THẬT, nói ra chứ không giấu: M3 có thể khoá oan.** Ca môi trường chết trước khi kịp ghi
  `run.json` là ca **có thật**, và ở đúng ca ấy bằng chứng máy sẽ vắng mặt. M4 tồn tại vì thế; nếu
  reviewer thấy M4 quá dễ lách thì **đó là finding đúng**, và cách chữa là siết `can_cu`, không
  phải bỏ M4 — bỏ nó là biến một lỗi hạ tầng tạm thời thành ngõ cụt vĩnh viễn, đúng bệnh mà chú
  thích trong `cmd_void_attempt` đã ghi.
- **Ngưỡng "tươi" của ảnh `doctor` chưa có số.** Executor phải đề xuất và bảo vệ bằng phép đo, đừng
  bê một con số từ đặc tả này — ở đây cố ý **không** ghi số.
- Chưa đo trên `windows-latest`. Packet chạm `packet_loop.py`, mà CI 17-08-2026 đo được cùng bộ
  test bỏ qua 1 ca trên Linux và 13 trên Windows ⇒ **phải gọi tay `workflow_dispatch`**, vì gắn
  nhãn `windows` KHÔNG sinh lượt chạy nào.
