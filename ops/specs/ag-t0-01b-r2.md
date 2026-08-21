# ĐẶC TẢ PACKET — `AG-T0-01B`, **revision 2**

```yaml
packet_id: AG-T0-01B
packet_issue: 219
revision: 2
thay_the: ops/specs/ag-t0-01b.md   # r1, sha256 60458925b52415b83939fa303ba5aca7eb01c54ae0ecfedb88df5d4c28fc7868
review_class: sensitive
executor: antigravity
reviewer: codex | claude   # phiên độc lập, khác nền với executor
assurance_target: cross_approved
base_sha: a7a45119
```

## 0. Delta so `revision 1` — MỘT quyết định bị LẬT, không phải một chỗ gõ lại

`r1` viết: *"cố ý KHÔNG khai `xac_thuc`"*, lý do là tài liệu Google không có lệnh trạng thái
đăng nhập. **Lý do ấy đúng về tài liệu và SAI về công cụ.** Đo `agy 1.1.17` (§1): `agy models`
là một probe xác thực **không tương tác, không tốn quota, và KIỂM CHỨNG ĐƯỢC** — nó gọi thật
ra dịch vụ (`Fetching available models...`) rồi trả `rc=1` kèm câu từ chối rõ ràng khi chưa
đăng nhập. Đó chính là thuộc tính mà `codex login status` KHÔNG có, và là điều kiện mà
docstring `_xac_thuc` (`launcher.py:1986`) đặt ra: *"chỉ gắn `xac_thuc` cho công cụ có đầu ra
KIỂM CHỨNG ĐƯỢC"*.

Ghi lại vì nó là bài học chứ không phải thủ tục: **`r1` suy từ TÀI LIỆU, `r2` suy từ PHÉP
CHẠY, và hai bên ra hai thiết kế ngược nhau.** Tài liệu chính thức của Google không liệt kê
`models` ở trang cài đặt; chỉ `agy --help` mới lộ 10 lệnh con.

Bốn thứ khác đổi theo: probe khả dụng (§4.2), luồng đọc đầu ra (§4.3), đường lùi PATH trên
Windows (§4.4), và cấm phân loại bằng dò chuỗi (§4.5).

## 1. Bằng chứng — chạy 21-08-2026, `agy 1.1.17` `linux_amd64`, container CHƯA từng đăng nhập

Cài bằng `curl -fsSL https://antigravity.google/cli/install.sh | bash` ⇒ `/root/.local/bin/agy`,
205.574.400 byte. Mọi lượt gọi đều `stdin=/dev/null`, `timeout 20–25s`.

| lệnh | rc | stdout | stderr |
|---|---|---|---|
| `agy --version` | **0** | `1.1.17` | rỗng |
| `agy --help` | 0 | **0 byte** | 36 dòng (usage + 10 lệnh con) |
| `agy models` | **1** | 0 byte | `Fetching available models...` + `Error: Please sign in to view available models. Launch the CLI without arguments to sign in.` |
| `agy agents` | **0** | **0 byte** | **0 byte** |
| `agy changelog` | 0 | 75.990 byte | rỗng |

Lệnh con có thật: `agent` `agents` `changelog` `help` `install` `mcp` `models` `plugin`
`plugins` `update`.

**`agy --version` KHÔNG mở luồng đăng nhập khi chưa login** — đây là câu hỏi số 4 của
`chua_do_duoc` trong `r1`, và nó là câu duy nhất có thể làm hỏng toàn bộ thiết kế probe. Đã
trả lời bằng phép chạy trong đúng trạng thái chưa-đăng-nhập.

## 2. `nguon_cap_viec`

`ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md:41`. Người giữ kho gỡ `hoãn` 21-08-2026.

## 3. `review_class` — `sensitive`

`docs/PROTOCOL_DA_PHIEN.md:573` liệt kê `launcher` đích danh; `:567` *"Executor không được hạ
lớp."* Bảng kế hoạch khai `systemic` là sai, cùng hình dạng đã đính chính ở `PLAT-M4`. Hệ quả:
**cấm AG–AG land**.

## 4. `write_set` — 2 đường dẫn

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

`derived_set` **RỖNG** (`.claude` thuộc `_RELEASE_EXCLUDE_DIRS`; `grep launcher
RELEASE_MANIFEST.json` = 0). Không lease đang sống nào chạm hai tệp này —
`ops/DONG_SO_LEASE_PLAT_M4.md`.

## 5. `ngoai_pham_vi`

| thứ | vì sao KHÔNG |
|---|---|
| con trỏ AG trong `AGENTS.md` | tệp nằm trong `RELEASE_MANIFEST.json` ⇒ nở `derived_set` (bài học `AG-T0-03`) |
| `docs/GOI_AGENT_DA_NEN.md` | tài liệu, tách packet `routine` riêng |
| `bat_buoc` theo nền cho `agy` | chưa bắt buộc ở đâu; nâng lên cần lý do đo được riêng |
| dùng `agy -p` trong lượt `doctor` mặc định | đốt quota Gemini. §1 cho thấy **không cần**: `models` đã đủ đo xác thực |
| dùng `agy agents` làm probe | §1: `rc=0` + **cả hai luồng rỗng** — kẻ nói dối kinh điển |
| `--dangerously-skip-permissions` · `--sandbox` · `--output-format json` | thuộc packet AG-executor sau, không thuộc discovery |

## 6. `muc_tieu` — mỗi mục chiếu vào MỘT đường dẫn của `write_set`

**4.1 `CONG_CU` có một mục `agy`** — `.claude/dev/launcher.py`.
`ung_vien: ["agy"]` · `bat_buoc: False` · `xac_thuc: ["models"]` (**đổi so r1**) ·
`cai` mang lệnh thật theo nền: Windows `irm https://antigravity.google/cli/install.ps1 | iex` ·
macOS/Linux `curl -fsSL https://antigravity.google/cli/install.sh | bash`.

**4.2 `KHA_NANG` có một mục `antigravity`** — `.claude/dev/launcher.py`. Bốn trạng thái:

| trạng thái | điều kiện đo được |
|---|---|
| `DUNG_DUOC` | `agy models` rc=0 **và** có đầu ra (stdout+stderr) |
| `CO_MAT` | binary chạy được (`--version` rc=0) nhưng `models` rc≠0 — đã cài, chưa đăng nhập |
| `KHONG_DO_DUOC` | timeout hoặc `OSError` — **KHÔNG** được làm tròn thành `THIEU` |
| `THIEU` | không tìm thấy binary, kể cả sau đường lùi 4.4 |

**4.3 Probe đọc CẢ HAI luồng, và không bao giờ gọi `agy` TRẦN** — `.claude/dev/launcher.py`.
§1 đo được: `--help` và `models` ghi ra **stderr**, stdout **0 byte**. Một probe đọc stdout
một mình sẽ thấy rỗng và kết luận sai. `agy` trần mở TUI ⇒ treo tới `PROBE_TIMEOUT_GIAY`.
Mọi lời gọi: có cờ/lệnh con, `stdin=subprocess.DEVNULL`, `encoding="utf-8", errors="replace"`,
timeout. (`_xac_thuc:2003` đã cộng hai luồng — dùng nó, đừng viết lại.)

**4.4 Đường lùi PATH trên Windows** — `.claude/dev/launcher.py`. Trình cài ghi PATH vào
**registry** rồi broadcast; phiên terminal đang mở **không** nhận (chính nó cảnh báo *"is not
present in your active Environment PATH"*, đo trên máy người giữ kho 21-08). `shutil.which`
trượt ⇒ `doctor` sẽ bảo người **vừa cài xong** đi cài lại. Khi `which` trượt trên Windows,
thử đường dẫn tất định `%LOCALAPPDATA%\agy\bin\agy.exe`; thấy tệp ở đó ⇒ trạng thái riêng
*"đã cài, PATH phiên này chưa thấy — mở terminal mới"*, **không** phải `THIEU`.

**4.5 Cấm phân loại bằng dò chuỗi tự do** — `.claude/dev/launcher.py`. Trình cài in log THÀNH
CÔNG ra stderr với tiền tố `ERROR:` (`ERROR: logging before google.Init: ... Successfully
added ...`). Phân loại theo `rc` và theo lệnh con, không theo chữ trong đầu ra — cùng bài học
`Not Found` trong thân phản hồi HTTP.

**4.6 `antigravity` KHÔNG vào `LAM_DUOC_VIEC`** — `.claude/dev/launcher.py`. `models` chứng
minh dịch vụ TRẢ LỜI, không chứng minh review được gì — cùng hạng `rest-chung`/`mcp-endpoint`.
Lần thứ **năm** của cám dỗ "đếm sự CÓ MẶT thay vì KHẢ NĂNG".

**4.7 Phản chứng chạy được cho 4.1–4.6** — `.claude/dev/launcher_test.py`. Ca mới từ **`t144`**
(base có 143 ca, số lớn nhất `t143`).

## 7. `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ

| # | tiêu chí | đột biến phải giết 1/1 |
|---|---|---|
| N1 | `t144`: `CONG_CU` có đúng **1** mục `agy`, `bat_buoc is False`, `xac_thuc == ["models"]` | xoá mục; đổi `xac_thuc` sang `["--version"]` (probe không kiểm chứng được) |
| N2 | `t144`: `KHA_NANG` có đúng **1** mục `antigravity` | xoá mục |
| N3 | `t145`: mọi lời gọi tới `agy` trong nhật ký lệnh giả **đều có ≥1 đối số** | đổi probe thành `subprocess.run(["agy"], ...)` |
| N4 | `t145`: lượt mặc định (không `--kiem-song`) **không** sinh lời gọi khớp `["agy","-p",...]` hoặc `["agy","--print",...]` | cho probe gọi `-p` vô điều kiện |
| N5 | `t145`: `models` rc=0 với đầu ra **CHỈ trên stderr** ⇒ `DUNG_DUOC` | đổi probe sang chỉ đọc `stdout` ⇒ ra `CO_MAT` sai |
| N6 | `t145`: `models` `TimeoutExpired`/`OSError` ⇒ `KHONG_DO_DUOC`, **không** `THIEU` | đổi nhánh lỗi thành `THIEU` |
| N7 | `t145`: rc=0 mà **cả hai luồng rỗng** ⇒ **không** được `DUNG_DUOC` (dạng thật của `agy agents`) | bỏ điều kiện `co_loi_ra` |
| N8 | `t146`: trên `os.name == "nt"` giả, `which` trượt + tệp có ở `%LOCALAPPDATA%\agy\bin\agy.exe` ⇒ **không** `THIEU` | bỏ đường lùi 4.4 |
| N9 | `t145`: `antigravity` ở `DUNG_DUOC` **không** đổi tập `LAM_DUOC_VIEC` của `github` | nối `antigravity` vào `any(...)` (đúng cách `t103` bắt `rest-chung`) |
| N10 | Suite: hai số **BẰNG NHAU** — `146/146` ca đã chạy qua (bỏ qua = ca Windows-only sẵn có, hỏng = 0). `rc=0` một mình không phải bằng chứng | ca có `vao` mà không có `ra` trong `--nhat-ky`; tổng đếm lệch |
| N11 | `--dot-bien`: mỗi đột biến N1–N9 giết 1/1; nền **132/132** không tụt (đo trên PR "#204") | một mutant sống sót; nền tụt |
| N12 | `git diff origin/master...HEAD` = **đúng 2 tệp** | tệp thứ ba |
| N13 | `doc-claims-check --strict` · `doctrine-scan` · `release-verify` · `golden-test` · `determinism-audit` đều rc=0 + `"ok": true`; `ci.yml` **cả `ubuntu` LẪN `windows`** trên exact head | bất kỳ cái nào khác 0; hoặc chỉ có lượt `ubuntu` |

**Ghi chú N13 — Windows bắt buộc, và gắn nhãn KHÔNG đủ.** `ci.yml` khai `pull_request:` mà
không khai `types:` ⇒ `labeled` không sinh lượt chạy nào. Đường chắc chắn là `workflow_dispatch`
trên exact ref. Mục 4.4 là mã **chỉ chạy trên Windows** — bỏ lượt Windows là bỏ đúng phần mới.

## 8. `hinh_dang_ke_thua` (L4)

Tiền nhiệm **PR "#165"**, `closed_blocked_ci`, không merge, **không có biên nhận review** ⇒ bộ
đếm khởi tạo từ hồ sơ kế hoạch:

| hình dạng | lần | đã chặn bằng gì |
|---|---|---|
| gộp nhiều mối quan tâm vào một PR | 1 | packet một mối quan tâm |
| lệch băm gói vì sửa `AGENTS.md` không đồng bộ manifest | 1 | `AGENTS.md` ngoài phạm vi |
| required gate Windows bị `skip` | 1 | N13 đòi `workflow_dispatch` |
| khai `review_class` thấp hơn thực tế | 2 | §3 |
| **suy thiết kế từ TÀI LIỆU thay vì PHÉP CHẠY** | **1** | §0 — chính `r1` của packet này |

Hình dạng cuối mới đếm 1; ghi ra để lần sau đếm tiếp chứ không đếm lại từ 0.

## 9. `chua_do_duoc`

Ba trong bốn mục của `r1` đã đóng bằng §1. Còn lại, khai thẳng:

1. **Toàn bộ số đo là `linux_amd64`.** Đường Windows (4.4) và lệnh cài `irm ... | iex` **chưa**
   được đo với `agy --version` trên Windows — máy người giữ kho cài xong nhưng chưa dán output.
   N8 vì vậy đo bằng `os.name` **giả**, không phải Windows thật; N13 (lượt CI Windows) là phép
   đo thật duy nhất cho nhánh ấy, nên nó bắt buộc, không tuỳ chọn.
2. **`agy models` rc=0 chưa từng được quan sát** — container này chưa đăng nhập, nên chỉ đo
   được nhánh `rc=1`. Nhánh `DUNG_DUOC` sẽ được đóng bằng fixture giả ở `t145`, và **một lượt
   chạy thật** trên máy đã đăng nhập nên được ghi vào PR làm bằng chứng dương.
3. **`agy models` có gọi mạng.** Nó chậm hơn `--version` và là một đường chớp `t53` mới. Chưa
   đo phân bố thời gian; `PROBE_TIMEOUT_GIAY` hiện dùng chung, chưa biết có đủ không.
