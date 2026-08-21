# ĐẶC TẢ PACKET — `AG-T0-01B`

```yaml
packet_id: AG-T0-01B
packet_issue: 219
revision: 1
review_class: sensitive
executor: antigravity
reviewer: codex | claude   # phiên độc lập, khác nền với executor
assurance_target: cross_approved
base_sha: a7a45119        # = origin/master lúc đóng băng; đã kiểm là tổ tiên nhánh mặc định
```

## `nguon_cap_viec`

`ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md:41` — dòng packet duy nhất của kế hoạch AG chưa land.
`ops/KE_HOACH_DIEU_CHINH_DA_NEN_TANG.md:177` xếp `hoãn — planned_experimental`; người giữ kho
gỡ hoãn 21-08-2026 trong phiên.

## `review_class` — `sensitive`, và vì sao lời khai `systemic` của bảng kế hoạch là SAI

`docs/PROTOCOL_DA_PHIEN.md:573` liệt kê **`launcher`** đích danh trong `sensitive`. Bảng kế
hoạch phân loại theo thứ packet KHÔNG đụng thay vì thứ nó CÓ đụng — cùng hình dạng đã bị đính
chính ở `PLAT-M4` (`ops/DINH_CHINH_REVIEW_CLASS_PLAT_M4.md`), và `:567` nói thẳng *"Executor
không được hạ lớp."*

Hệ quả cứng: **cấm AG–AG land.** Executor Antigravity ⇒ reviewer phải là phiên độc lập khác
nền. `same_provider_approved` KHÔNG đủ cho `sensitive`.

## `write_set` — 2 đường dẫn, liệt kê từng cái

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

`derived_set`: **RỖNG**. Đo được: cả hai đường dẫn nằm trong `_RELEASE_EXCLUDE_DIRS`
(`.claude/`) nên không thuộc `RELEASE_MANIFEST.json` ⇒ không tái sinh manifest, không ghi lại
golden. Đây là điều kiện phân biệt packet này với `AG-T0-03` (khai 3 tệp, đụng 10).

**Giao write set:** lease `plat-m4-exec-2-claude-20260821` khai đúng hai đường dẫn này; packet
`PLAT-M4` đã land ở PR "#204" và quyền ghi đã tiêu — biên bản `ops/DONG_SO_LEASE_PLAT_M4.md`.
Không lease đang sống nào khác chạm hai tệp này.

## `ngoai_pham_vi` — cố ý không làm, kèm lý do

| thứ | vì sao KHÔNG |
|---|---|
| con trỏ AG trong `AGENTS.md` | tệp nằm TRONG `RELEASE_MANIFEST.json` ⇒ sửa nó kéo theo tái sinh manifest, biến `derived_set` từ rỗng thành khác rỗng. Đúng bài học `AG-T0-03` |
| `docs/GOI_AGENT_DA_NEN.md` mục Antigravity | tài liệu, không phải phép đo; tách ra một packet `routine` riêng |
| khai `xac_thuc` cho `agy` | **không có lệnh trạng thái đọc được** (xem `chua_do_duoc`). Kho đã cố ý không khai cho `codex` vì `codex login status` NÓI DỐI — trả giá HAI lần. Không probe > probe biến tín hiệu sai thành xanh |
| `bat_buoc` theo nền (`{mac_dinh, remote, ci}`) | `agy` chưa bắt buộc ở đâu. Nâng lên là quyết định vận hành khác, cần lý do đo được của chính nó |
| gọi `agy -p` trong lượt `doctor` mặc định | đốt quota Gemini của người dùng. Tiền lệ `llm`/`OA-T0-01`: chỉ `--kiem-song` mới gọi thật |

## `muc_tieu` — mỗi mục chiếu vào MỘT đường dẫn của `write_set`

1. **`CONG_CU` có một mục `agy`** — `.claude/dev/launcher.py`.
   `ung_vien: ["agy"]` · `bat_buoc: False` (bool trần, như `llm`) · `vi_sao` nêu provider
   `google_antigravity` / surface `antigravity` · `cai` mang lệnh cài THẬT theo nền
   (Windows PowerShell: `irm https://antigravity.google/cli/install.ps1 | iex` ·
   macOS/Linux: `curl -fsSL https://antigravity.google/cli/install.sh | bash`).
   **KHÔNG** có khoá `xac_thuc`.

2. **`KHA_NANG` có một mục `antigravity`** — `.claude/dev/launcher.py`.
   Mặc định đo bằng **`agy --version`** (rẻ, không mạng, không quota). `--kiem-song` mới chạy
   một lời gọi thật `agy -p "<câu rẻ>"`. Ba trạng thái, không hai:
   `DUNG_DUOC` · `CO_MAT` (có binary, chưa chứng minh gọi được) · `KHONG_DO_DUOC`.
   Thiếu binary ⇒ `THIEU`. **`KHONG_DO_DUOC` không được làm tròn thành `THIEU`** —
   doctrine `None ≠ False`.

3. **Probe không bao giờ chạy `agy` TRẦN** — `.claude/dev/launcher.py`.
   `agy` trần mở TUI và treo tới `PROBE_TIMEOUT_GIAY`. Mọi lời gọi phải mang cờ không tương
   tác, `stdin=subprocess.DEVNULL`, `encoding="utf-8", errors="replace"`, và timeout.

4. **`antigravity` KHÔNG được tính vào `LAM_DUOC_VIEC`/`DUNG_DUOC` của github hay lane review**
   — `.claude/dev/launcher.py`. `agy --version` chứng minh binary CÓ MẶT, không chứng minh nó
   review được gì. Đây là lần thứ **năm** của cám dỗ "đếm sự CÓ MẶT thay vì KHẢ NĂNG"
   (bốn lần trước: `which(gh)` · `rest-chung` · `gh auth status` · `mcp-endpoint`).

5. **Phản chứng chạy được cho cả bốn mục trên** — `.claude/dev/launcher_test.py`.
   Ca mới bắt đầu từ **`t144`** (đo trên `base_sha`: 143 ca, số lớn nhất là `t143`).

## `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ

| # | tiêu chí | thứ làm nó ĐỎ (đột biến phải giết 1/1) |
|---|---|---|
| N1 | `t144` khẳng định `CONG_CU` có đúng **1** mục `ten == "agy"`, `bat_buoc is False`, và mục ấy **không** có khoá `xac_thuc` | xoá mục `agy` khỏi `CONG_CU`; **và** thêm `"xac_thuc": ["--version"]` vào mục ấy — cả hai đột biến phải làm `t144` ĐỎ |
| N2 | `t144` khẳng định `KHA_NANG` có đúng **1** mục `ten == "antigravity"` | xoá mục ấy khỏi `KHA_NANG` |
| N3 | `t145` bơm `shutil.which` giả + `_chay_van_ban_an_toan` giả, rồi khẳng định **mọi** lời gọi tới `agy` trong nhật ký lệnh đều **có ít nhất một đối số** | sửa probe thành `subprocess.run(["agy"], ...)` (gọi trần) ⇒ `t145` ĐỎ |
| N4 | `t145` khẳng định lượt `doctor` mặc định (không `--kiem-song`) **không** sinh lời gọi nào khớp `["agy", "-p", ...]` | cho probe gọi `agy -p` vô điều kiện ⇒ ĐỎ |
| N5 | `t145` khẳng định `agy --version` rc≠0 (hoặc ném `OSError`) cho ra `KHONG_DO_DUOC`, **không** phải `THIEU`, khi binary CÓ trên PATH | đổi nhánh lỗi thành `THIEU` ⇒ ĐỎ |
| N6 | `t145` khẳng định `antigravity` ở trạng thái `DUNG_DUOC` **không** làm đổi tập `LAM_DUOC_VIEC` của `github` | nối `antigravity` vào `any(...)` của `LAM_DUOC_VIEC` ⇒ ĐỎ (đúng cách `t103` bắt `rest-chung`) |
| N7 | Suite chạy hết, hai số **BẰNG NHAU**: `145/145` ca đã chạy qua (bỏ qua = ca Windows-only sẵn có, hỏng = 0). `rc=0` một mình **không** được nhận làm bằng chứng | ca có `vao` mà không có `ra` trong `--nhat-ky`; hoặc tổng đếm lệch |
| N8 | `--dot-bien` xanh: mỗi đột biến của N1–N6 giết **1/1**; nền không tụt so với `base_sha` (**132/132 đạt** đo trên PR "#204") | một đột biến sống sót; hoặc số nền tụt |
| N9 | `git diff origin/master...HEAD` cho **đúng 2 tệp** = `write_set` | tệp thứ ba xuất hiện |
| N10 | Gate: `doc-claims-check --strict` · `doctrine-scan` · `release-verify` · `golden-test` · `determinism-audit` đều `rc=0` và `"ok": true`; `ci.yml` **cả `ubuntu` LẪN `windows`** trên exact head | bất kỳ cái nào khác 0; hoặc chỉ có lượt `ubuntu` (xem ghi chú dưới) |

**Ghi chú N10 — Windows là bắt buộc cho packet này, và nhãn KHÔNG đủ.** `ci.yml` khai
`pull_request:` mà không khai `types:` ⇒ `labeled` không sinh lượt chạy nào; gắn nhãn
`windows` rồi merge là tưởng đã đo Windows mà chưa. Đường chắc chắn: gọi tay
`workflow_dispatch` trên exact ref. Packet này đụng đường cài phụ thuộc nền
(`irm ... | iex` vs `curl ... | bash`) nên bỏ Windows là bỏ đúng nửa đang thay đổi.

## `hinh_dang_ke_thua` (L4)

Tiền nhiệm là **PR "#165"** (`agent/ag-packet3-launcher-windows-plan`), `closed_blocked_ci`,
**không merge**. Không có biên nhận review nào để chép số đếm — bộ đếm hình dạng lỗi vì vậy
khởi tạo từ hồ sơ kế hoạch, không từ receipt:

| hình dạng | lần | nguồn |
|---|---|---|
| gộp nhiều mối quan tâm vào một PR | **1** | `ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md:66` — *"Gộp 3 concerns khác nhau"* |
| lệch băm gói vì sửa `AGENTS.md` mà không đồng bộ manifest | **1** | cùng dòng trên |
| required gate Windows bị `skip` | **1** | cùng dòng trên |
| khai `review_class` thấp hơn thực tế (theo VỊ TRÍ thay vì HẬU QUẢ) | **2** | `PLAT-M4` (đã đính chính) + chính bảng kế hoạch AG dòng 41 |

Cả ba hình dạng đầu **đã được chặn bằng thiết kế** của đặc tả này: một mối quan tâm duy nhất ·
`AGENTS.md` nằm ngoài phạm vi · N10 đòi Windows bằng `workflow_dispatch`. Hình dạng thứ tư đạt
**2 lần** — chưa tới ngưỡng 3, nhưng ghi ra để lần sau đếm tiếp chứ không đếm lại từ 0.

## `chua_do_duoc`

Mọi số về `agy` trong đặc tả này đến từ **tài liệu chính thức**
(`antigravity.google/docs/cli/getting-started`, `/docs/cli/install`, `/docs/cli/overview`),
đọc 21-08-2026 — **không** từ một lượt chạy. Cụ thể chưa biết:

1. **`agy --version` có tồn tại không, và in ra chuỗi gì.** Toàn bộ N5 và nhánh mặc định của
   mục tiêu 2 treo vào câu này. Nếu `agy` không nhận `--version` thì probe phải đổi cờ, và đó
   là `revision: 2`.
2. **`agy --help` liệt kê lệnh con nào** — có lệnh con không tương tác nào rẻ hơn `-p` không.
3. **Có tín hiệu xác thực không tương tác nào không.** Tài liệu chỉ có `/logout` trong TUI.
4. **Hành vi khi CHƯA đăng nhập**: `agy --version` có tự mở luồng đăng nhập không? Nếu có thì
   ngay cả `--version` cũng là lời gọi tương tác, và thiết kế probe phải làm lại từ đầu.

Máy người giữ kho đo 21-08-2026: `agy: The term 'agy' is not recognized as a name of a cmdlet`
⇒ **chưa cài trên máy đó**. Đây KHÔNG phải bằng chứng tên lệnh sai — tài liệu Google gọi đích
danh `agy -p "..."`.

**Điều kiện để packet chuyển `ready`:** có output thật của `agy --version` và `agy --help` từ
một máy đã cài. Trước đó, `nghiem_thu` N5 chưa chứng minh được là ĐỎ ĐƯỢC, và một tiêu chí
không thể đỏ thì không phải tiêu chí.
