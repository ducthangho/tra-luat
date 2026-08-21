# ĐẶC TẢ PACKET — `AG-T0-01B`, **revision 4**

```yaml
packet_id: AG-T0-01B
packet_issue: 219
revision: 4
thay_the: ops/specs/ag-t0-01b-r3.md   # r3, sha256 25da97c724bc47dfa73012e9f2c460037ca4d873bb60ce49be46a444bbe61a37
review_class: sensitive
executor: antigravity
reviewer: codex        # xem §0bis.2 — KHÔNG còn "codex | claude"
assurance_target: cross_approved
base_sha: ba46a91c0ab939ae903716625f3d3b1e02baf1d8
```

## 0. Delta so `revision 3` — hai finding cross-review lượt 1 (codex, PR "#221")

### 0.1 `P2` — `base_sha` là SHA RÚT GỌN trong chính bản đặc tả dạy về SHA

`r3` đóng băng `base_sha: ba46a91` — bảy ký tự. Finding đúng, và nó đắng: cùng lượt làm việc
ấy tôi viết vào `ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md` §3 rằng *"SHA rút gọn không phải bằng
chứng yếu — nó là bằng chứng có hạn sử dụng"*, sau khi đo được `125f8f0` của sổ nợ **không còn
phân giải được**. Viết ra luật rồi vi phạm nó ở tệp bên cạnh, trong cùng một lượt.

`r4` ghi đủ 40 ký tự: `ba46a91c0ab939ae903716625f3d3b1e02baf1d8` (đã `git cat-file -e`).

Reviewer đề nghị thêm **validation từ chối `base_sha` khác 40 ký tự**. Đúng, nhưng nó nằm ở
`ops/lease_publish.py` — **ngoài write set** của packet này. Ghi vào `PLAT-X6` (Issue "#220"),
cùng chỗ với việc cưỡng chế lời khai `model`: hai chốt, một tệp, một packet.

### 0.2 `P1` — lease chồng lấn: tôi viết ra lời cảnh báo rồi hành động như thể nó là bản vá

Finding: `plat-m4-exec-2-claude-20260821` **vẫn** cấp quyền ghi cho đúng hai đường dẫn này tới
`2026-08-22T02:05:00Z`, trong khi chính `ops/DONG_SO_LEASE_PLAT_M4.md` (dòng 47–51) **thừa
nhận** hết hạn là cơ chế DUY NHẤT được cài đặt và **không cổng nào** nhận ra lời đóng sổ bằng
văn xuôi. Nên một phiên `PLAT-M4` được khôi phục và phiên AG này có thể **cùng khai độc quyền
ghi**.

Đây là fail-open đúng nghĩa, và là hình dạng kho đã trả giá: *"Từ chối mà vẫn để đường nguy
hiểm chạy tiếp là FAIL-OPEN, không phải thận trọng."* Tôi đo được lỗ, viết lỗ ra giấy, rồi cấp
lease như thể việc viết ra đã bịt nó.

**Chữa: dời hiệu lực, không chế thêm cơ chế.** Lease mới
`ag-t0-01b-exec-1r2-antigravity-20260822` có `leased_at_utc: '2026-08-22T02:05:00Z'` — đúng
thời điểm tiền nhiệm hết hạn — và `supersedes_lease` lease cũ. Cửa sổ chồng lấn về **0**.

**Vì sao KHÔNG dùng `supersedes_lease` để thu hồi lease của `PLAT-M4`:** trường ấy có tiền lệ
(`wp55-r2-review-3/4`) nhưng chỉ dùng cho lease **cùng một packet**. Cho một packet thu hồi
lease của packet KHÁC là dựng một đường huỷ đơn phương — đúng thứ reviewer cảnh báo trong cùng
finding (*"cannot cancel a packet that merely appears terminal from stale facts"*). Chờ 16 giờ
rẻ hơn một cơ chế huỷ chưa ai thiết kế.

**Cái giá, nói thẳng:** phiên AG không bắt đầu được trước `2026-08-22T02:05:00Z`. Người giữ kho
có thể override bằng một quyết định có ghi, nhưng override ấy phải khai rõ là chấp nhận rủi ro
hai-writer, không được viết như thể rủi ro đã hết.


## 0bis. Delta so `revision 2` (giữ nguyên từ `r3`)

### 0bis.1 Ba mục `chua_do_duoc` của `r2` đã ĐÓNG bằng phép chạy trên Windows

Người giữ kho chạy 21-08-2026, PowerShell 7, `agy 1.1.17` Windows, tài khoản ĐÃ đăng nhập:

| lệnh | rc | đầu ra |
|---|---|---|
| `& "$env:LOCALAPPDATA\agy\bin\agy.exe" --version` | **0** | `1.1.17` |
| `agy models` | **0** | **14 dòng** danh sách model |
| `agy agents` | **0** | **RỖNG** |

Ba kết luận:

1. **Nhánh Windows chạy thật**, không còn chỉ đo bằng `os.name` giả. `agy` gọi qua tên trần
   được sau khi PATH nạp lại ⇒ đường lùi `%LOCALAPPDATA%\agy\bin\agy.exe` (§4.4) là đường
   CỨU HỘ cho phiên chưa nạp PATH, không phải đường chính.
2. **Nhánh `agy models` rc=0 đã được QUAN SÁT** — lần đầu. `xac_thuc: ["models"]` nay có bằng
   chứng dương ở cả hai đầu: `rc=1` + câu từ chối (Linux, chưa đăng nhập) và `rc=0` + danh
   sách model (Windows, đã đăng nhập). Một probe chỉ được tin khi đã thấy **cả hai màu**.
3. **`agy agents` rc=0 + rỗng ĐÚNG TRÊN CẢ HAI NỀN.** Fixture "kẻ nói dối" của tiêu chí `N7`
   vì vậy không phải tật của một nền — nó là hành vi của công cụ.

### 0bis.2 Phát hiện MỚI, không ai lường trước: `agy` chạy được MODEL CỦA ANTHROPIC

Danh sách 14 model do chính `agy models` trả về có:

```
claude-sonnet-4-6         Claude Sonnet 4.6 (Thinking)
claude-opus-4-6-thinking  Claude Opus 4.6 (Thinking)
gpt-oss-120b-medium       GPT-OSS 120B (Medium)
```

**Điều này phá một giả định đã đi vào `r1`, `r2` và cả Issue #219:** rằng "AG là executor,
Claude là reviewer" đương nhiên là `cross_approved` vì hai *provider* khác nhau. Sai. Một
phiên AG đặt `--model claude-opus-4-6-thinking` rồi được một phiên Claude Code review là
**cùng một họ model, khác vỏ công cụ** — tức `same_provider_approved` đội lốt `cross_approved`,
đúng thứ nhãn assurance sinh ra để chặn.

Protocol đã lường trước ở tầng schema mà chưa ai nối vào lane AG:
`docs/PROTOCOL_DA_PHIEN.md:429` khai `model_reviewer_identity: <provider/model/session
attestation>` — **provider VÀ model**, hai thứ riêng; `:546` nói thẳng tên công cụ không tự
quyết định assurance. Kho vẫn suy assurance từ tên CÔNG CỤ (`antigravity` ≠ `claude` ⇒ chéo),
tức **đếm cái vỏ thay vì cái chạy** — cùng hình dạng với "đếm sự CÓ MẶT thay vì KHẢ NĂNG" đã
trả giá năm lần, chỉ đổi đối tượng.

Ba chốt vào đặc tả này:

- **`reviewer: codex`**, bỏ nhánh `| claude`. Với `review_class: sensitive` và executor chạy
  trên harness có thể nạp model Anthropic, reviewer Claude không chứng minh được là chéo.
- **Lease của packet này BẮT BUỘC khai `model` của phiên AG** (giá trị đúng như `agy --model`
  nhận), và verdict khai `model_reviewer_identity` đủ `provider/model/session`. Thiếu một
  trong hai ⇒ evidence defect ⇒ chặn land, theo nguyên tắc khuyết tật bằng chứng của
  `ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md` §1.
- **Nếu phiên AG chạy model Anthropic thì reviewer Claude bị LOẠI**; nếu chạy `gpt-oss-*` thì
  reviewer Codex cũng đáng ngờ theo cùng lý lẽ. Chọn model Gemini cho phiên executor là đường
  sạch nhất và nên khai thẳng trong lease.

**Đây là phát hiện của lượt soạn spec, không phải việc của packet.** Nó nói cho packet này
biết ai được review nó; nó KHÔNG mở write set. Việc cưỡng chế lời khai model ở cổng lease là
một packet riêng — đề xuất `PLAT-X6`, chưa mở Issue, chờ người giữ quyết.

## 1. Bằng chứng gộp — hai nền

Linux `linux_amd64`, container phiên, **chưa từng đăng nhập**, cài bằng
`curl -fsSL https://antigravity.google/cli/install.sh | bash` ⇒ `/root/.local/bin/agy`,
205.574.400 byte:

| lệnh | rc | stdout | stderr |
|---|---|---|---|
| `agy --version` | 0 | `1.1.17` | rỗng |
| `agy --help` | 0 | **0 byte** | 36 dòng (10 lệnh con) |
| `agy models` | **1** | 0 byte | `Please sign in to view available models` |
| `agy agents` | 0 | **0 byte** | **0 byte** |
| `agy changelog` | 0 | 75.990 byte | rỗng |

Windows, PowerShell 7, **đã đăng nhập** — bảng ở §0.1.

Lệnh con: `agent` `agents` `changelog` `help` `install` `mcp` `models` `plugin` `plugins`
`update`. **Không có lệnh con `login`** — đăng nhập nằm trong TUI khi chạy `agy` trần.

## 2. `nguon_cap_viec`

`ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md:41`. Người giữ kho gỡ `hoãn` 21-08-2026.

## 3. `review_class` — `sensitive`

`docs/PROTOCOL_DA_PHIEN.md:573` liệt kê `launcher` đích danh; `:567` *"Executor không được hạ
lớp."* Cấm AG–AG land, và nay thêm ràng buộc model ở §0.2.

## 4. `write_set` — 2 đường dẫn

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

`derived_set` **RỖNG** (`.claude` thuộc `_RELEASE_EXCLUDE_DIRS`; `grep launcher
RELEASE_MANIFEST.json` = 0). Không lease đang sống nào chạm hai tệp này
(`ops/DONG_SO_LEASE_PLAT_M4.md`).

## 5. `ngoai_pham_vi`

| thứ | vì sao KHÔNG |
|---|---|
| con trỏ AG trong `AGENTS.md` | nằm trong `RELEASE_MANIFEST.json` ⇒ nở `derived_set` (bài học `AG-T0-03`) |
| `docs/GOI_AGENT_DA_NEN.md` | tài liệu, tách packet `routine` riêng |
| **cưỡng chế lời khai `model` ở cổng lease** | phát hiện §0.2, đụng `ops/lease_publish.py` — packet riêng (`PLAT-X6` đề xuất) |
| `bat_buoc` theo nền cho `agy` | chưa bắt buộc ở đâu |
| `agy -p` trong lượt `doctor` mặc định | đốt quota; `models` đã đủ đo xác thực |
| `agy agents` làm probe | rc=0 + hai luồng rỗng, đo được trên CẢ HAI nền |
| `--dangerously-skip-permissions` · `--sandbox` · `--output-format json` | thuộc packet AG-executor sau |

## 6. `muc_tieu` — mỗi mục chiếu vào MỘT đường dẫn của `write_set`

**6.1 `CONG_CU` có một mục `agy`** — `.claude/dev/launcher.py`.
`ung_vien: ["agy"]` · `bat_buoc: False` · `xac_thuc: ["models"]` ·
`cai`: Windows `irm https://antigravity.google/cli/install.ps1 | iex` ·
macOS/Linux `curl -fsSL https://antigravity.google/cli/install.sh | bash`.

**6.2 `KHA_NANG` có một mục `antigravity`** — `.claude/dev/launcher.py`. Bốn trạng thái:

| trạng thái | điều kiện |
|---|---|
| `DUNG_DUOC` | `agy models` rc=0 **và** có đầu ra (stdout+stderr) |
| `CO_MAT` | `--version` rc=0 nhưng `models` rc≠0 — đã cài, chưa đăng nhập |
| `KHONG_DO_DUOC` | timeout hoặc `OSError` — **không** làm tròn thành `THIEU` |
| `THIEU` | không thấy binary, kể cả sau đường lùi 6.4 |

**6.3 Đọc CẢ HAI luồng, không bao giờ gọi `agy` TRẦN** — `.claude/dev/launcher.py`.
`--help` và `models` (nhánh lỗi) ghi ra **stderr**, stdout 0 byte. `agy` trần mở TUI ⇒ treo.
Mọi lời gọi: có cờ/lệnh con, `stdin=subprocess.DEVNULL`, `encoding="utf-8", errors="replace"`,
timeout. Dùng `_xac_thuc` (`launcher.py:2003` đã cộng hai luồng), đừng viết lại.

**6.4 Đường lùi PATH trên Windows** — `.claude/dev/launcher.py`. Trình cài ghi PATH vào
**registry** rồi broadcast; phiên đang mở không nhận. `which` trượt ⇒ thử
`%LOCALAPPDATA%\agy\bin\agy.exe`; thấy tệp ⇒ trạng thái *"đã cài, PATH phiên này chưa thấy —
mở terminal mới"*, **không** phải `THIEU`.

**6.5 Cấm phân loại bằng dò chuỗi tự do** — `.claude/dev/launcher.py`. Trình cài in log THÀNH
CÔNG ra stderr với tiền tố `ERROR:`. Phân loại theo `rc` và lệnh con.

**6.6 `antigravity` KHÔNG vào `LAM_DUOC_VIEC`** — `.claude/dev/launcher.py`. `models` chứng
minh dịch vụ trả lời, không chứng minh review được gì — cùng hạng `rest-chung`/`mcp-endpoint`.

**6.7 Phản chứng chạy được cho 6.1–6.6** — `.claude/dev/launcher_test.py`. Ca mới từ **`t144`**
(base `ba46a91`: xác nhận lại số ca TRƯỚC khi đặt tên — `r2` đo 143 ca trên `a7a45119`).

## 7. `nghiem_thu`

| # | tiêu chí | đột biến phải giết 1/1 |
|---|---|---|
| N1 | `t144`: `CONG_CU` có đúng 1 mục `agy`, `bat_buoc is False`, `xac_thuc == ["models"]` | xoá mục; đổi `xac_thuc` sang `["--version"]` |
| N2 | `t144`: `KHA_NANG` có đúng 1 mục `antigravity` | xoá mục |
| N3 | `t145`: mọi lời gọi `agy` trong nhật ký giả đều có ≥1 đối số | `subprocess.run(["agy"], ...)` |
| N4 | `t145`: lượt mặc định không sinh lời gọi `["agy","-p",…]` / `["agy","--print",…]` | gọi `-p` vô điều kiện |
| N5 | `t145`: `models` rc=0 với đầu ra **chỉ trên stderr** ⇒ `DUNG_DUOC` | probe chỉ đọc `stdout` |
| N6 | `t145`: `TimeoutExpired`/`OSError` ⇒ `KHONG_DO_DUOC` | đổi nhánh lỗi thành `THIEU` |
| N7 | `t145`: rc=0 + **cả hai luồng rỗng** ⇒ KHÔNG `DUNG_DUOC` (dạng thật của `agy agents`, đo trên hai nền) | bỏ điều kiện `co_loi_ra` |
| N8 | `t146`: `os.name == "nt"` giả, `which` trượt, tệp có ở `%LOCALAPPDATA%\agy\bin\agy.exe` ⇒ không `THIEU` | bỏ đường lùi 6.4 |
| N9 | `t145`: `antigravity` `DUNG_DUOC` không đổi tập `LAM_DUOC_VIEC` của `github` | nối vào `any(...)` |
| N10 | Suite: hai số BẰNG NHAU, `N/N` ca đã chạy qua (bỏ qua = ca Windows-only sẵn có, hỏng = 0) | ca có `vao` không có `ra`; tổng lệch |
| N11 | `--dot-bien`: mỗi đột biến N1–N9 giết 1/1; nền không tụt | mutant sống sót |
| N12 | `git diff origin/master...HEAD` = đúng 2 tệp | tệp thứ ba |
| N13 | `doc-claims-check --strict` · `doctrine-scan` · `release-verify` · `golden-test` · `determinism-audit` rc=0 + `"ok": true`; `ci.yml` **cả `ubuntu` LẪN `windows`** trên exact head | cái nào khác 0; chỉ có `ubuntu` |
| N14 | Lease khai `model` của phiên AG; verdict khai `model_reviewer_identity` đủ `provider/model/session`; hai giá trị **KHÁC HỌ MODEL** | lease/verdict thiếu trường; hoặc executor và reviewer cùng họ model |

**N13 — nhãn `windows` KHÔNG đủ.** `ci.yml` khai `pull_request:` không kèm `types:` ⇒ `labeled`
không sinh lượt chạy. Đường chắc chắn: `workflow_dispatch` trên exact ref.

## 8. `hinh_dang_ke_thua` (L4)

Tiền nhiệm PR "#165" `closed_blocked_ci`, không biên nhận review:

| hình dạng | lần | đã chặn bằng gì |
|---|---|---|
| gộp nhiều mối quan tâm vào một PR | 1 | packet một mối quan tâm |
| lệch băm gói vì sửa `AGENTS.md` | 1 | `AGENTS.md` ngoài phạm vi |
| required gate Windows bị `skip` | 1 | N13 |
| khai `review_class` thấp hơn thực tế | 2 | §3 |
| suy thiết kế từ TÀI LIỆU thay vì PHÉP CHẠY | 1 | §0bis của `r2` — chính `r1` |
| **suy assurance từ tên CÔNG CỤ thay vì thứ ĐANG CHẠY** | **1** | §0bis.2 + N14 |

Hình dạng cuối là biến thể thứ **sáu** của "đếm cái vỏ thay vì cái chạy" trong kho này. Chưa
tới ngưỡng ba lần cho riêng biến thể assurance; ghi để đếm tiếp.

## 9. `chua_do_duoc`

1. **`agy models` trên Windows đi luồng nào (stdout hay stderr) — CHƯA phân biệt được.**
   PowerShell hiển thị hai luồng như nhau. Quyết định KHÔNG phụ thuộc vào câu này (`_xac_thuc`
   cộng cả hai), nhưng nói thẳng là chưa đo, đừng để ai đọc bảng §0.1 rồi tưởng đã biết.
2. **Chưa đo `agy --model <id>` có thật sự nhận các id ở §0.2 không**, và chưa có đường nào
   ghi lại model mà một phiên AG ĐÃ dùng. N14 vì vậy hiện dựa vào **lời khai**, không dựa
   vào phép đo — đó là điểm yếu đã biết của nó, và là lý do đề xuất `PLAT-X6`.
3. **`agy models` gọi mạng** ⇒ một đường chớp `t53` mới; chưa đo phân bố thời gian, chưa biết
   `PROBE_TIMEOUT_GIAY` dùng chung có đủ không.

4. **Hai chốt đề xuất từ cross-review lượt 1 nằm ngoài write set** và đã chuyển sang `PLAT-X6`
   (Issue "#220"): (a) từ chối `base_sha` khác 40 ký tự; (b) một đường thu hồi lease bền, được
   dispatcher công nhận, kèm ca test cho tiền nhiệm ĐÃ LAND nhưng CHƯA HẾT HẠN. Chừng nào (b)
   chưa có, cách duy nhất tránh chồng lấn vẫn là **chờ hết hạn** — `r4` chọn đúng cách đó.
