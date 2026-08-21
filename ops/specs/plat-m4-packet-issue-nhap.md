# BẢN NHÁP Packet Issue — `PLAT-M4` (A4): tách `mcp` thành `mcp-cli` và `mcp-endpoint`

> **⛔ CHƯA ĐƯỢC BẮT ĐẦU — dù NỘI DUNG đã được người giữ duyệt 20-08-2026.**
> Duyệt nội dung **không phải** giao việc, và tệp này **không phải** authority: còn thiếu
> đúng hai thứ — **Packet Issue** (nơi neo `spec_hash`) và **lease** còn hiệu lực
> (`docs/PROTOCOL_DA_PHIEN.md` §3.2 và §4). Prompt, handoff và tệp nháp này **không phải
> lease** (§7).
> Nguồn của packet: `ops/KE_HOACH_DIEU_CHINH_DA_NEN_TANG.md` §3 mục A4.

## 1. Packet Spec đề nghị

```yaml
schema_version: 1
packet_id: PLAT-M4
phase_key: PLAT-M4
priority: P0
executor: claude
model: opus-5          # §2 kế hoạch: Executor Opus 5
effort: xhigh          # §8 kế hoạch: Spec PHẢI khai effort
environment: local
risk: sensitive
review_class: sensitive
depends_on:
  - PLAT-M3            # #185, đã `state:integrated` (PR #189)
                       # KHÔNG phụ thuộc PLAT-M1 (macOS đã tạm hoãn 20-08-2026)
effective_write_set:
  - .claude/dev/launcher.py
  - .claude/dev/launcher_test.py
required_review_assurance: cross_approved
required_independent_reviewer: codex
```

**⛔ NỐI TIẾP `PLAT-M3`, KHÔNG SONG SONG.** Write set trùng khít. Bản đầu của kế hoạch xếp
hai packet này vào cùng cột “song song” — sai, và PR #187 đang mở chính là bản đính chính
đó. `#185` nay là `state:integrated`, nên điều kiện mở đã thoả; **kiểm lại nhãn Issue trước
khi cấp lease**, đừng tin dòng này.

## 2. Vì sao có packet này — bằng chứng đo được

Trong `_do_github`, đường MCP hiện là **một** trường `mcp`, dựng từ hai bước:

```
_doc_mcp_json(ws)             -> `.mcp.json` có khai server tên đúng `github` không
_suc_khoe_mcp_github(ten, mt) -> hỏi `claude mcp get <ten>`, đọc trường `Status:`
```

Cả hai đều hỏi **phía CLI**. Không bước nào chạm tới đầu kia của dây. Mà `.mcp.json` khai:

```json
{"mcpServers": {"github": {"type": "http", "url": "https://api.githubcopilot.com/mcp/", ...}}}
```

Đo được (kế hoạch §1, và lặp lại trong `CLAUDE.md`): `claude mcp get github` trả
**`Pending approval`** trong khi POST `initialize` thẳng tới chính URL ấy bằng `GITHUB_PAT`
trả **HTTP 200, header GitHub đầy đủ, 44 công cụ**. Nghĩa là hai câu hỏi khác nhau, và bản
hiện tại chỉ hỏi câu **không** quyết định được việc.

**Cái giá đã trả bằng tiền thật:** một phiên web/điện thoại đọc `mcp=khong` sẽ kết luận
GitHub bị chặn rồi dừng — *đã xảy ra, mất trọn một lượt* — trong khi endpoint vẫn thông.

Khuôn để tái dùng đã có sẵn và đã đúng: `_do_rest_github` phân loại theo **header
`X-GitHub-*`** chứ không theo mã trạng thái, trả **ba** trạng thái (`mo` · `chan` ·
`khong_do_duoc`) và tách `thanh_cong` khỏi `mo`. `_do_github` cũng đã tách `rest` thành
`rest-chung` (đường proxy cho phép) và `rest-kho` (đường việc thật). A4 làm **đúng phép tách
ấy** cho MCP.

## 3. Năm quyết định — **ĐÃ CHỐT** (người giữ duyệt 20-08-2026, theo khuyến nghị)

Chúng không còn là câu hỏi mở. Lượt thi công **thực hiện đúng** năm chốt dưới đây; thấy
chốt nào sai thì **DỪNG và mở revision**, không tự đổi giữa đường (đổi acceptance là
đổi `spec_hash`).

### 3.1 CHỐT: mở rộng `t115` sang cả hai tên mới — lỗ nguy hiểm nhất của packet

`t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec` chốt điều số 1 bằng cách
đọc thẳng mã nguồn:

```python
khoi = nguon[nguon.index("LAM_DUOC_VIEC = {"):]
bang('"mcp"' not in khoi and "'mcp'" not in khoi, ...)
```

Nó tìm **đúng chuỗi `"mcp"` có dấu nháy hai đầu**. Sau khi đổi tên, `"mcp-cli"` và
`"mcp-endpoint"` **không khớp** mẫu ấy. Hệ quả đo được trước cả khi viết: **đột biến thêm
`"mcp-endpoint"` vào `LAM_DUOC_VIEC` sẽ SỐNG SÓT, còn `t115` vẫn báo qua.** Ca canh vẫn ở
đó, vẫn xanh, và không còn canh gì — đúng họ với bài học *“ca có MẶT khác ca có ĐO”*.

⇒ Mở rộng `t115` sang **cả hai tên mới** là **việc bắt buộc**, không phải việc kèm theo. Nó
là phản chứng số 1 ở §5.

### 3.2 CHỐT: `mcp-endpoint` **KHÔNG** vào `LAM_DUOC_VIEC`

Tập ấy giữ nguyên **`{git, gh-kho, rest-kho}`**. `mcp-endpoint` là **chẩn đoán**, in ra
cho người đọc, không có quyền quyết định nhãn `DUNG_DUOC`.

Lý do là lịch sử: kho đã ba lần đếm **sự CÓ MẶT** của một đường thay vì **KHẢ NĂNG** của nó
(`shutil.which("gh")` · `rest-chung` · `gh auth status`), và `t103` sinh ra từ đó. Một lượt
`initialize` chứng minh **endpoint sống và token được nhận**, không chứng minh đọc được kho
này — nó cùng hạng với `rest-chung`, không cùng hạng với `rest-kho`.

Hệ quả ràng buộc lượt thi công: muốn MCP được tính là *làm được việc* thì phải là một
packet KHÁC, probe neo vào **thao tác mức kho đã thành công** (gọi một tool thật, không
phải handshake) và trường ấy phải mang tên `mcp-kho` để cái tên nói đúng thứ nó đo.
Trong packet này: **không**.

### 3.3 CHỐT: `initialize`, timeout theo hằng có sẵn, **không** auto-retry

`initialize` là handshake JSON-RPC, không ghi gì. Vẫn phải khai tường minh trong docstring,
đặt timeout theo hằng `PROBE_TIMEOUT_GIAY` đang dùng, và **không auto-retry** — `doctor` là
phép đo, không phải nỗ lực kết nối.

### 3.4 CHỐT: ca sentinel cho `GITHUB_PAT` — đo, không suy luận

Phải có ca chốt: đặt token **sentinel**, chạy `doctor` và `doctor --json`, rồi khẳng định
chuỗi sentinel **không xuất hiện trong bất kỳ byte nào** của stdout/stderr. Không suy luận
“urllib đâu có in header”; đo.

### 3.5 CHỐT: suite chạy **offline**, bốn fixture, không gọi mạng thật

Suite phải chạy offline, tất định. Cần lớp giả cho `urlopen` (kiểu đã dùng ở các ca hiện có)
và fixture cho **bốn** trạng thái ở §5. Một ca “chỉ chạy khi có mạng” là ca sẽ im lặng biến
mất đúng lúc cần nhất.

## 4. Acceptance

- `doctor` in **hai** trường thay cho một: `mcp-cli=` (dây nối, `claude mcp get`) và
  `mcp-endpoint=` (một lượt `initialize` thật tới URL khai trong `.mcp.json`).
- Mỗi trường có **ba** trạng thái, và `chua-do-duoc` kết xuất **khác** `khong` (`None ≠ False`).
- Phân loại bằng **header** `X-GitHub-*`: 4xx **có** header = *tới nơi, thiếu quyền*
  (`mo`, thao tác không thành công); **không** header = *proxy tự sinh* (`chan`).
- `doctor --json` có hai khoá tương ứng, parse được, **không** lộ token.
- `LAM_DUOC_VIEC` **không đổi**: vẫn đúng `{git, gh-kho, rest-kho}` (chốt §3.2).
- Suite **không tụt dưới 137 ca** (nền đo hôm nay: `rg -c '^def t[0-9]+_' launcher_test.py`
  = 137). Kết quả `N/N` hai số **bằng nhau**, `rc=0`. Suite chạy được **offline**.
- Cây làm việc sạch sau khi chạy test.

## 5. Phản chứng bắt buộc

1. **Đột biến thêm `"mcp-endpoint"` (và `"mcp-cli"`) vào `LAM_DUOC_VIEC` ⇒ ca đích ĐỎ.**
   Bịt đúng lỗ §3.1. Không có ca này thì cả packet chỉ là đổi tên.
2. Fixture **200 CÓ header** ⇒ `mcp-endpoint=OK`. Đột biến *phân loại theo mã trạng thái
   thay vì header* ⇒ ca đích ĐỎ.
3. Fixture **403 KHÔNG header** ⇒ `chan` kèm chữ “proxy tự sinh”, **không** đọc thành thiếu
   quyền. Đột biến gộp hai ca ⇒ ĐỎ.
4. Fixture **401 CÓ header** ⇒ `mo` **và** thao tác **không** thành công. Đột biến gộp `mo`
   với `thanh_cong` ⇒ ĐỎ (đây đúng là P1 mà cross-review đã bắt trên đường `rest`).
5. Fixture **timeout/DNS** ⇒ `khong_do_duoc`, kết xuất khác `khong`. Đột biến ép về `False`
   ⇒ ĐỎ.
6. Token **sentinel** không xuất hiện trong bất kỳ byte đầu ra nào, kể cả `--json`. Đột biến
   in URL kèm token hoặc echo header ⇒ ĐỎ.
7. `.mcp.json` khai server nhưng **thiếu `url`**, hoặc `url` không phải `http(s)` ⇒
   `khong_do_duoc` **có lý do đọc được**, không traceback, không đoán mặc định.

Mỗi đột biến phải **giết 1/1**. Nhắc bẫy đã trả giá: runner đột biến từng ghi mọi bản sao
vào cùng một tệp tạm và CPython dùng lại `.pyc` theo *(mtime giây, kích thước)* — mutant khi
ấy **chưa từng chạy** mà báo `giet 0/1`. Nếu thấy `0/1`, kiểm cơ chế trước khi kết luận mã đúng.

## 6. Non-goals — KHÔNG làm trong packet này

- **Không** đổi ngữ nghĩa `_do_rest_github` đang có; chỉ **tái dùng** khuôn phân loại của nó.
- **Không** sửa `.mcp.json`, không thêm server, không đụng credential.
- **Không** đổi `LAM_DUOC_VIEC` — chốt §3.2 đã đóng cửa này; muốn mở thì là packet khác.
- **Không** đụng workflow (A1/A2), không cài `gh`, không dựng đường REST mới cho kho.
- Thấy chốt phải nằm ngoài hai tệp write set ⇒ **DỪNG**, xuất handoff, mở packet riêng.

## 7. Ràng buộc

- Write set đúng hai tệp, kiểm trên **TỪNG commit**, không chỉ trên diff gộp.
- `core.abbrev` = 7 trước mọi cổng.
- Trần review **2 vòng**. Mỗi finding kèm khối `Gợi ý vá` bốn phần.
- Packet đụng `.claude/dev/**` ⇒ **phải có lượt Windows**. Đường chắc chắn là gọi tay
  `workflow_dispatch` trên đúng ref; gắn nhãn `windows` chỉ ăn ở lượt bắn kế tiếp, nên nếu
  dùng nhãn thì phải đẩy thêm một commit sau khi gắn.
- Đọc ngược mọi thứ đã đăng lên GitHub bằng `git ls-remote`; `git fetch` qua proxy nói dối.

## 8. Vì sao `sensitive`

`doctor` là thứ **mọi phiên đọc để quyết định đi đường nào**. Sai một chiều thì phiên kết
luận “GitHub bị chặn” và dừng dù đường vẫn thông — mất trọn một lượt, đã xảy ra. Sai chiều
kia còn tệ hơn: dán nhãn `DUNG_DUOC` cho một đường không làm nổi việc, tức biến lỗi hạ tầng
thành lỗi “chắc tại quyền token” và đẩy người đọc đi sai hướng — đúng cái bẫy
`codex login status` và `gh auth status` đã dựng hai lần trong kho này.
