# Thẩm định AG-T0-03 sau khi land, và hợp nhất hai kế hoạch thi công

> **Trạng thái:** hồ sơ thẩm định + biên bản quyết định. Không cấp authority.
> Authority nằm ở Packet Spec, GitHub facts và receipt đã verify.
>
> Mọi con số dưới đây là **đo được**, kèm cách tái lập. Không con số nào gõ tay.

Nền đo: `origin/master` `47847b1812c2703a385549b767f6bf1ce979db4b`
(AG-T0-03 đã land qua PR #175, squash).
Mọi lượt chạy đặt `core.abbrev 7` — đúng như `.github/workflows/ci.yml` ghim.

---

## 1. Hai phép đo môi trường phải ghim trước, nếu không mọi kết luận sau đều sai

### 1.1 `git fetch` qua proxy phiên remote NÓI DỐI; chỉ `git ls-remote` là sự thật

Đo được: sau khi `git push` trả `rc=0`, `git fetch origin --prune` vẫn trả về ref CŨ.
`git ls-remote origin` cùng lúc trả ref MỚI, đúng.

Hệ quả: bài học "đăng lên GitHub xong phải ĐỌC NGƯỢC VỀ" **không chỉ áp cho đường
GitHub API** — nó áp cho cả đường git. Và công cụ đọc ngược phải là `ls-remote`,
không phải `fetch`, vì `fetch` có tầng cache riêng.

### 1.2 Selftest ĐỎ GIẢ 2 ca khi `core.abbrev` = 8

Đo được trên clone đủ lịch sử (1155 object ⇒ git tự nới abbrev lên 8):

```
core.abbrev = 8 (mặc định)  -> 1695/1697, rc=1
                               [FAIL] r218_docclaims_l2_sha_khong_ton_tai
                               [FAIL] r264_doc_claims_phu_docs
core.abbrev = 7 (CI ghim)   -> 1697/1697, rc=0
```

Cơ chế đã được ghi sẵn trong chú thích của `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`:
ngưỡng L2 lấy từ `git rev-parse --short`, mà git nới độ dài viết tắt theo số object.
Ngưỡng 8 trùng độ dài tiền tố UUID notebook ⇒ 18 tiền tố bị hô `SHA_NOT_A_COMMIT`.

CI xanh vì ghim `core.abbrev 7`. **Máy dev không ghim thì đỏ oan** — và đỏ oan này
đứng TRƯỚC mọi cổng khác, nên nó che mất phép đo thật. Ai thẩm định trên clone đủ
lịch sử mà bỏ qua điều này sẽ kết luận "master đang đỏ" — sai.

---

### 1.3 `doctor` báo `mcp=khong` — ĐÚNG với thứ nó đo, SAI với câu người đọc đang hỏi

Đo được trong phiên remote 19-08:

```
launcher.py doctor --kiem-song  ->  github: ... mcp=khong
claude mcp get github           ->  Status: ⏸ Pending approval (run `claude` to approve)
POST https://api.githubcopilot.com/mcp/  ->  HTTP 200 · server: github.com
                                            · mcp-session-id · x-github-request-id
                                            · 44 công cụ dùng được
```

Ba dòng trên **không mâu thuẫn**. `_suc_khoe_mcp_github` hỏi `claude mcp get`, tức nó đo
**CLI đã nối server chưa** — và câu trả lời `Pending approval` là đúng: server khai trong
`.mcp.json` cấp dự án cần một lượt duyệt tương tác, mà phiên remote thì không có.

Nhưng câu người vận hành đang hỏi khi đọc `mcp=khong` là **endpoint có dùng được không**.
Hai câu khác nhau, và ở phiên không tương tác thì câu thứ hai mới quyết định làm được việc
hay không: endpoint **thông hoàn toàn** khi gọi thẳng bằng `GITHUB_PAT`.

Cái giá đã trả thật: một phiên đọc `mcp=khong` cộng với `rest-kho=khong` đã kết luận
**GitHub bị chặn cứng** và báo không đọc được `#177`/`#178` — trong khi đường MCP mở suốt.
Mất trọn một lượt.

Đây là **biến thể thứ ba** của cùng một bệnh mà chính `launcher.py` đã chữa hai lần trước
đó: *đo sự CÓ MẶT thay vì đo KHẢ NĂNG* (`_do_github` chữa cho `rest`), và *ca có MẶT khác
ca có ĐO*. Lần này là **đo DÂY NỐI thay vì đo ĐẦU KIA CỦA DÂY**.

Đề xuất (chưa thi công, cần packet riêng): tách `mcp` thành hai trường như `_do_github` đã
làm với `rest` — `mcp-cli` (`claude mcp get`, đo dây nối) và `mcp-endpoint` (một lượt
`initialize` thật tới URL khai trong `.mcp.json`, đo đầu kia). Áp đúng tiêu chí sẵn có của
`_do_github`: 4xx **có** header `x-github-*` là *tới nơi, thiếu quyền*; **không có** header
là *proxy tự sinh*.

### 1.4 Bản đồ đường GitHub ở phiên remote — và vì sao THÔNG ĐIỆP LỖI NÓI SAI CƠ CHẾ

403 trên đường theo kho trả về nguyên văn:

> *GitHub access is not enabled for this session. An org admin must connect the Claude
> GitHub App for this organization.*

Câu đó dẫn người đọc tới kết luận sai: *thiếu quyền, phải nhờ admin nối App*. **Phép đo
bác bỏ nó.** Thử một kho **CÔNG KHAI của người khác** — thứ không cần quyền gì, không
thuộc org nào của người dùng:

```
GET /user                      -> 200 · 4 header x-github · Server: github.com
GET /rate_limit                -> 200 · 4 header x-github
GET /repos/ducthangho/tra-luat -> 403 · 0 header x-github     (kho riêng)
GET /repos/cli/cli             -> 403 · 0 header x-github     (CÔNG KHAI)
GET /repos/torvalds/linux      -> 403 · 0 header x-github     (CÔNG KHAI)
GET /user/repos                -> 403 · 0 header x-github
GET /search/repositories       -> 403 · 0 header x-github
```

Kho công khai cũng chặn ⇒ **không phải chuyện quyền, cũng không phải chuyện org**. Theo
đúng tiêu chí của `_do_github` trong `launcher.py` (4xx CÓ header `x-github-*` là *tới
nơi, thiếu quyền*; KHÔNG có header là *proxy tự sinh*), cả năm dòng 403 đều có **0**
header ⇒ **GitHub chưa từng nhìn thấy những yêu cầu này**.

Cơ chế thật: **proxy egress cho phép theo DANH SÁCH ĐƯỜNG DẪN**, không theo kho và không
theo quyền. `api.github.com` chỉ mở vài đường danh tính/hạn mức (`/user`, `/rate_limit`);
mọi đường chạm dữ liệu kho đều đóng. Nối Claude GitHub App **có thể** không đổi được gì,
vì chặn không nằm ở tầng cấp quyền.

Hệ quả vận hành: **đừng đi tìm quyền.** Đổi đường.

| đường | kết quả | dùng được? |
|---|---|---|
| `git` clone · fetch · **push tạo/cập nhật ref** | thông (credential riêng, ngoài sandbox) | **có** |
| `git push --delete` ref · đẩy tag | 403 | không qua git — **nhưng có đường khác, xem §1.6** |
| REST `api.github.com` — `/user`, `/rate_limit` | 200 | có, nhưng vô dụng cho việc kho |
| REST `api.github.com/repos/**`, `/search/**`, `/user/repos` | 403, 0 header | **không** — kể cả kho công khai |
| `gh` (mọi lệnh theo kho) | 403 | không — nó đi đường REST ở trên |
| **GitHub MCP** `api.githubcopilot.com/mcp/` | 200, header GitHub đầy đủ | **CÓ — đây là đường làm việc** |

**GitHub MCP là đường duy nhất chạm được dữ liệu kho.** Mặc định trả 44 công cụ; thêm
header `X-MCP-Toolsets: all` mở lên **89** (có nhóm Actions: `actions_list`,
`actions_run_trigger`, `get_job_logs`). Không có công cụ xoá ref/nhánh **trực tiếp** —
đã kiểm cả 89 — nhưng `actions_run_trigger` mở được đường **gián tiếp**, xem §1.6.

### 1.5 `GH_TOKEN` giả đang che credential thật

```
GH_TOKEN      13 ký tự   ← gh đọc CÁI NÀY trước, theo đúng thứ tự tài liệu của gh
GITHUB_TOKEN  13 ký tự
GITHUB_PAT    92 ký tự   ← credential THẬT
```

`gh auth status` báo *"The token in GH_TOKEN is invalid"* — đúng, nhưng nó khiến người
đọc kết luận **sai** rằng phiên không có credential GitHub. Đặt `GH_TOKEN="$GITHUB_PAT"`
thì `gh api user` chạy được ngay (trả `ducthangho`).

Đây là lỗi thật, nhưng **không phải nguyên nhân** của việc không vào được kho: vá xong
thì `gh api repos/...` vẫn 403, vì nó vẫn đi đường bị chặn ở §1.4.

`launcher.py` đã ghi sẵn bẫy này (thứ tự `GH_TOKEN` → `GITHUB_TOKEN` → `GITHUB_PAT`),
nhưng `doctor` chỉ báo `gh-kho=khong` — không nói ra rằng `gh` đang **đọc nhầm biến**.
Đề xuất cho `PLAT-M4`: `doctor` khai thẳng độ dài và biến đang được dùng.

### 1.6 CÓ đường xoá ref từ phiên cloud — đính chính §1.4

**Bản trước của hồ sơ này kết luận sai** rằng phiên cloud không xoá được ref. Đúng phần
*đường git*, sai phần *kết luận chung*: `git push --delete` bị chặn, nhưng kho **đã có
sẵn** một đường khác, và phiên cloud **kích hoạt được nó**.

#### Cơ chế

`.github/workflows/ops-don-ref.yml` chạy trên runner GitHub với `GITHUB_TOKEN` —
**không đi qua proxy egress**, nên nó có đúng quyền mà sandbox cố ý không cấp. Chú thích
đầu tệp gọi nó là *đường sạch DUY NHẤT để một phiên web làm hai việc trên*.

Cái còn thiếu trong hồ sơ trước là: **phiên cloud kích hoạt được workflow đó** bằng
`actions_run_trigger` của GitHub MCP (chỉ hiện khi gửi header `X-MCP-Toolsets: all`).

**Đã đo, không suy luận:**

```
actions_run_trigger  run_workflow  ops-don-ref.yml  ref=master  chi_thu=true
  -> 204 No Content · "Workflow run has been queued"
  -> run 32276889527 · completed / success
```

#### Cách dùng

```
workflow_id: ops-don-ref.yml      ref: master
inputs:
  hanh_dong : xoa-nhanh | xoa-tag | tao-tag
  ref       : tên ref, KHÔNG tiền tố refs/heads; nhiều cái cách nhau dấu phẩy
  xac_nhan  : XOA (hoặc TAO cho tao-tag) — sai một ký tự là dừng
  chi_thu   : true (MẶC ĐỊNH, thử khô) — phải đặt false mới xoá thật
  ly_do     : đi vào log
```

#### Nó TỪ CHỐI gì — và đó là thiết kế, không phải thiếu sót

| vùng | xử lý |
|---|---|
| nhánh mặc định | `exit 2`; đo lúc chạy, không ghi cứng `master`; chặn cả `Master` khác hoa thường |
| `ops/**` `claude/**` `codex/**` `agent/**` `mission/**` `dispatcher/**` | `exit 2` — *nhánh ở đây thường mang hồ sơ chưa vào master, xoá phải do người* |
| `luu-tru/**` dạng NHÁNH | chỉ cho xoá **nếu còn tag giữ commit ấy**; đo bằng `repos/O/R/tags` (đã dereference) |
| `luu-tru/**` dạng TAG | cấm tuyệt đối — tag là mỏ neo của verdict đã công bố |

Nên: nhánh `fix/**`, `docs/**`, `probe-**`… **phiên cloud xoá được**; nhánh trong sáu
vùng bảo vệ thì **vẫn phải do người**.

#### Hai công cụ KHÔNG phải đường này

- **`scripts/don-nhanh.ps1`** — dọn hàng loạt nhánh đã merge, tự đo mỗi lần chạy, bốn
  lớp chốt (ancestor-of-master · danh sách giữ gồm cả **BASE** của PR đang mở · mặc định
  dry-run · đối chiếu lại sau khi xoá). **Không chạy được ở phiên cloud**: cần `pwsh`
  (không có trong ảnh) và `gh` theo đường kho (bị proxy chặn). Đây là công cụ máy local.
- **`launcher.py`** — không dính gì tới xoá ref. `grep -niE 'xoa.?(ref|nhanh|tag)|delete|receive-pack|don-ref'`
  trả **rỗng**. Nó lo vòng đời tiến trình và dò công cụ.

#### Lỗ mà chính kho đã khai — chốt proxy KHÔNG kín

Chú thích `ops-don-ref.yml` ghi thẳng: proxy chặn theo **HÌNH DẠNG** chứ không theo
**HẬU QUẢ** — `git push --force` (ép lùi) **vẫn được phép**, mà ép lùi cũng làm commit
thành không tra được y như xoá. Đo cùng ngày 16-08.

Ghi ra để biết ranh giới thật, **không phải để dùng**. Ép lùi một nhánh chung là hành
động phá hoại dù cổng có cho qua.

Cùng họ, `don-nhanh.ps1` tự khai một lỗ khác: xoá nhánh đang là **BASE** của PR đang mở
khiến GitHub **đóng luôn** các PR nhắm vào nó — mất cả review lẫn thảo luận, và không
thao tác nào dựng lại được trạng thái mở ấy. Lớp *ancestor-of-master* **không** che ca
này, vì một nhánh tích hợp có thể đã vào master trong khi vẫn còn PR mở nhắm vào nó.

#### Bài học phương pháp

Hồ sơ trước kết luận *không có đường* sau khi thử ba đường (git · REST · MCP trực tiếp).
Ba lần thất bại không chứng minh **không tồn tại** — chúng chỉ chứng minh **ba đường đó**
không đi được. Đường thứ tư đã nằm sẵn trong kho từ 16-08, kèm chú thích giải thích chính
xác vì sao nó tồn tại. Cùng họ với bài học đã ghi ở §1.3: **đo đúng thứ mình đang hỏi.**

### 1.7 Bẫy thực thể hoá của GitHub — danh sách ký tự RỘNG HƠN thứ đã ghi

Bản ghi cũ nêu tầng vận chuyển GitHub đổi `"` thành thực thể và `<` thành thực thể. **Danh
sách đó THIẾU.** Đo được 19-08 khi đăng Issue #188:

```
'   ⇒  &#39;      6 lần
>   ⇒  &gt;       4 lần
```

Và chúng nằm trong **KHỐI MÃ CÓ RÀO** (ba dấu huyền), không phải code span nội dòng. Trong
khối rào, GitHub **không giải mã** thực thể ⇒ nó hiện nguyên văn ra màn hình.

**Phép tiền kiểm sai ở đâu.** Tôi soi bằng một biểu thức chỉ khớp span nội dòng, và chỉ tìm
ba ký tự. Nó báo *sạch* trên một thân có **10** thực thể. Sai hai tầng cùng lúc: **hẹp về
ký tự** và **hẹp về vùng**.

**Phép kiểm đúng — bốn ký tự, hai vùng:**

```
ky tu can soi : dau nhay don · dau nhay kep · dau bé hon · dau lon hon
vung can soi  : khoi ma co rao  VA  span noi dong
```

**Và phép đo cuối cùng vẫn là ĐỌC NGƯỢC VỀ, so sha256 của thân gửi với thân đọc về.** Chính
nó bắt được lần này, sau khi tiền kiểm đã cho qua. Tiền kiểm là tiện lợi; đọc-ngược mới là
bằng chứng.

## 2. Thẩm định AG-T0-03: một lỗi làm hỏng đúng tính năng của chính packet

### 2.1 Phép đo

| commit | `tl registry-coverage` (đường người vận hành chạy) | `golden-test` |
|---|---|---|
| `33bfd8d0` (trước F8) | 166/196 = **84.69 %** | rc=0 |
| `7ea03ad4` (sau F8)   | 0/196 = **0.00 %**   | **rc=2 — ĐỎ** |

### 2.2 Căn nguyên

F8 muốn gộp thêm `NESTED_COMMAND_META` chứ không chỉ `COMMAND_META` — **ý định đúng**.
Nhưng bản vá đổi

```python
meta = getattr(tl_module, "COMMAND_META", all_command_meta())   # fallback GÁNH VIỆC
```

thành

```python
raw_top = getattr(tl_module, "COMMAND_META", {})                # fallback thành RỖNG
```

Đường sản xuất truyền `tl_module=_TL`, tức chính `scripts/tl.py`. Mà `tl.py` **không
export** bảng metadata nào — `COMMAND_META` và `NESTED_COMMAND_META` là hằng
module-level của `tl_core/command_registry.py`. Nên meta thành rỗng, và báo cáo tuyên
bố toàn bộ CLI không có lệnh nào được đăng ký.

Đây là lớp lỗi "vá một finding bằng cách gỡ mất thứ đang gánh việc" — bản vá đúng ý
định, sai hệ quả, và hệ quả nằm ở nhánh mà không test nào đi qua.

### 2.3 Đã được chặn trước khi land

Phiên thi công tự phát hiện và vá bằng guard `hasattr` trước khi merge. Master hiện
đo đúng 84.69 %, `golden-test` rc=0. **Finding này khép.**

### 2.4 Vì sao 7/7 ca unit vẫn XANH trong khi tính năng hỏng hoàn toàn

Mọi ca trong `scripts/tl_core/command_registry_test.py` hoặc:

- gọi `compute_parser_coverage(parser)` — `tl_module=None`, rơi vào nhánh ĐÚNG; hoặc
- truyền `MockTLModule` — một mock **có sẵn** `COMMAND_META`.

Mock dựng đúng cái mà module thật thiếu, nên nó che chính xác chỗ thủng. Cùng họ với
bài học đã ghi ở `launcher.py`: **"ca có MẶT khác ca có ĐO"**.

---

## 3. Hai lỗ còn hở SAU khi land — và cách đã vá

Nhánh: `fix/ag-t0-03-regression-guard`, nền `47847b1`.

### 3.1 Lỗi đã vá nhưng KHÔNG có gì giữ

Guard `hasattr` chặn được, nhưng không ca nào cưỡng chế nó ⇒ nó quay lại được bất cứ lúc nào.

Đã thêm `r332_registry_coverage_duong_san_xuat` vào `scripts/tl_selftest.py`. Ca này
**không import hàm và không mock** — chạy `scripts/tl.py registry-coverage --json`
bằng subprocess, đúng như người vận hành và CI gọi, rồi đòi hai điều:

1. `coverage_percent > 0` và `registered_leaf_commands > 0` — phản chứng trực tiếp;
2. số của đường CLI **khớp** số của `validate_registry` — chặn tái diễn "hai đường
   cho hai đáp số" mà chỉ một đường bị golden soi.

**Phản chứng đã chạy** (đây là điều kiện để ca được coi là gánh việc, không phải trang trí):

```
gỡ guard `hasattr`  -> [FAIL] r332 · 1697/1698 · rc=1
giữ guard           -> [OK]   r332 · 1698/1698 · rc=0
```

### 3.2 Bộ unit test của packet CHƯA TỪNG chạy trong CI

`scripts/tl_core/command_registry_test.py` không nằm trong `scripts/test_fragments/`
nên `tl.py --selftest` không khám phá ra nó.

Bằng chứng: ở lượt land, selftest đếm **1697/1697 trên CẢ master lẫn nhánh packet** —
7 ca mới không hề được tính. Nghĩa là bằng chứng "7/7 ca" chỉ tái lập được bằng tay,
và CI sẽ không bao giờ đỏ khi ai đó làm hỏng `compute_parser_coverage`.

Đã thêm bước CI riêng chạy thẳng tệp. Giữ nguyên vị trí tệp (không chuyển sang
`test_fragments/`) để không đụng vào topology gói đang sát trần 200.

### 3.3 Cổng đo tại chỗ trên nhánh vá

```
unit test packet            7/7        rc=0
tl selftest              1698/1698     rc=0   (transport 12/12)
golden-test                            rc=0
gen_instructions           44/44       rc=0
doc-claims-check --strict              rc=0
bundled-fragment                       rc=0
eol-policy 30/30 · pre-push 9/9        rc=0
gate lifecycle             28/28       rc=0
lease-publish              31/31       rc=0
file_count 180 (trần 200, còn 20 khe)
```

---

## 4. Kết quả thật mà packet AG-T0-03 phơi ra

Đây là giá trị của packet, tách khỏi lỗi ở trên:

```
tổng lệnh lá          196
đã có metadata        166   (84.69 %)
CHƯA có metadata       30
trong đó RỦI RO CAO     4   hygiene plan · hygiene reconcile
                            profile-file-add · reconcile
```

30 lệnh không có metadata nghĩa là ~15 % bề mặt CLI **không đi qua hệ phân loại rủi
ro** — registry là thứ lái `risk` / `requires_confirm` / `write_scope`. Bốn lệnh rủi
ro cao mang cờ ghi (`--apply`/`--delete`/`--trash`/`--write`/`--purge`) mà không khai
metadata là nợ đáng đóng trước, không phải đóng đủ 30.

Lưu ý về phép đo "rủi ro cao": nó là heuristic theo **danh sách cờ cứng**. Danh sách
đó chưa được phản chứng nào ghim, nên một lệnh ghi dùng cờ ngoài danh sách sẽ lọt.
Đây là hạn chế đã biết của `parser_tree_coverage.v1`, không phải lỗi.

---

## 5. Hợp nhất hai kế hoạch

Hai kế hoạch đang cùng sống:

- **cũ** — `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` (lane `W0-*`/`W1-*`/`W2-*`)
- **mới** — `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` + `ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md`

### 5.1 DÙNG ĐƯỢC — giữ nguyên

| Thứ | Vì sao giữ |
|---|---|
| Review bundle (§5) + validation receipt (§9) | Đã có hạ tầng CHẠY ĐƯỢC: `ops/chatgpt_review/` với 3 schema, `build_bundle.py`, `validate_note.py`, bộ test. Phần chắc nhất của kế hoạch mới. |
| Ba tầng Review Class `routine`/`systemic`/`sensitive` | Tương thích ngược với cột rủi ro từng packet của kế hoạch cũ — không phải làm lại bảng packet. |
| Nguyên tắc **Evidence Defect thắng Review Class** | Ý mạnh nhất trong cả hai kế hoạch: khuyết tật bằng chứng (SHA rút gọn, gate skip, head stale) chặn land bất kể tầng rủi ro. |
| Quy trình 8 bước (§4 kế hoạch AG) | Thực chất là protocol §12 viết lại. Đã được cưỡng chế bằng `.claude/dev/packet_loop.py`. Không cần xây mới. |
| Non-convergence: dừng sau N vòng | Đúng nguyên tắc; xem §5.2 về việc N đang mâu thuẫn. |

### 5.2 CẦN ĐIỀU CHỈNH

**(a) Cột write-set trong bảng packet đang sai có hệ thống.**
AG-T0-03 khai 3 tệp (`command_registry.py`, `workflow.py`, `test_fragments/<packet>.py`),
thực tế đụng **10** tệp. `references/golden/parser_surface.json` bị khai thuộc AG-T0-05
nhưng AG-T0-03 buộc phải đụng.

Đây **không phải vi phạm phạm vi** — là tái sinh cơ học bắt buộc khi thêm một lệnh.
Kế hoạch phải tách **write set** (thứ người viết tay) khỏi **derived set**
(`references/golden/*.json`, `RELEASE_MANIFEST.json` — thứ máy sinh lại). Không tách
thì cổng phạm vi sẽ báo vi phạm giả ở mọi packet có thêm lệnh.

**(b) Quy ước vị trí test chưa được cưỡng chế.**
Kế hoạch ghi `scripts/test_fragments/<packet>.py`; thi công làm khác, và hậu quả đo
được là test tàng hình với cả selftest lẫn CI (§3.2). Phải chọn một: cưỡng chế quy ước
fragment, hoặc bắt buộc khai bước CI trong Packet Spec. Bản vá hiện tại đi đường thứ hai.

**(c) Ngân sách review — ĐÃ CHỐT: 2 vòng.**

Người giữ kho đã quyết: lấy trần **2 vòng** của kế hoạch mới làm **trần canon của cả
kho**, áp mọi lane và mọi provider. Đã ghi vào cả ba tài liệu kế hoạch.

Ba chi tiết phải nói rõ, vì đo được và không hiển nhiên:

**1. Kế hoạch cũ không phải "4 vòng" — nó là 3.** §8 của
`ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` ghi *"chưa approve sau call 2 **hoặc ba vòng
code/review tổng**, dừng"*. Tức trần cũ là **3 vòng**, đếm lẫn với một trần **2 lời
gọi**. Vậy `W0-R1` chạy **4 vòng** là **vượt cả trần cũ**, không chỉ vượt trần mới.

**2. Không có gì chặn nó — và đó chính là tiền đề của `#177`.** Đo được trên
`.claude/dev/packet_loop.py`: `review_rounds_used` chỉ được khởi tạo (dòng 638) và
**tăng** (dòng 997). Không có `review_rounds_limit`, không nơi nào đọc nó để chặn.

**3. "2 vòng" rơi vào trục CHƯA CÓ TRẦN, không phải trục đang có trần 2.**
Hai bộ đếm, hai trục khác nhau, đã bị lẫn một lần:

| trục | bộ đếm | hằng | cưỡng chế |
|---|---|---|---|
| **vòng** — thứ vừa chốt | `review_rounds_used` | *không có* | **không có gì cả** |
| **lời gọi** — trục chi phí | `codex_review_calls_used` | `MAC_DINH_TRAN_REVIEW_CALL = 2` | có — `checkpoint` + `RC_TRAN` |

Chính chú thích trong `W0-R1` viết: *"Khác `codex_review_calls_used`: một vòng có thể
tốn nhiều lời gọi."* Nên trần 2 lời gọi sẵn có **không** thoả điều khoản 2 vòng.

**Hệ quả cho phạm vi `#177`.** `#177` (W0-R1B) vốn chỉ nhắm làm cho trần **lời gọi**
hết tự nguyện. Quyết định này **mở rộng nó**: phải thêm cả `review_rounds_limit`
(mặc định 2) và dệt nó vào đường bắt buộc, với lượt `void` thuộc `LY_DO_VOID` **không**
tính vào trần vòng. Không làm phần này thì điều khoản vừa chốt vẫn chỉ là kỷ luật của
người vận hành, không phải cổng.

**Không hồi tố `W0-R1`.** Bốn vòng đã chạy là sự thật lịch sử, không xoá được và không
cần xoá. Trần mới áp cho packet nhận từ thời điểm chốt trở đi.

**(d) Kế hoạch Antigravity §3 tự mâu thuẫn với kế hoạch đa provider §12.**
§12 cấm lưu trạng thái động (số PR, đã land chưa, nợ review) trong tài liệu kế hoạch
tĩnh. §3 lưu đúng những thứ đó (`landed_reaudit_pending (PR #163)`…). Một trong hai
phải nhường — nếu không, tài liệu sẽ trôi khỏi sự thật đúng như §12 cảnh báo.

### 5.3 BỎ

| Thứ | Vì sao bỏ |
|---|---|
| `W0-C1`, `W1-C2a` (lane "Codex candidate") | Codex hết quota là vật cản thường trực, không phải sự cố. Kế hoạch đa provider đã thay bằng AG + ChatGPT Web. |
| Toàn bộ **M3 / `W2-*`** (Blocking Authority, GitHub App publisher, Check Run canary) | Chính kế hoạch cũ đã gác sau điều kiện "chỉ khi số đo yêu cầu". Chưa có số đo nào yêu cầu, và kế hoạch mới không cần. |
| Giả định "Codex là reviewer chéo của hồ sơ" | Không còn đúng. Reviewer chéo nay là tập hợp AG / ChatGPT Web / Human Auditor / Claude, chọn theo Review Class. |

### 5.4 GIỮ — quyết định đã lấy

`#177` (W0-R1B) và `#178` (W0-RC) là packet của kế hoạch cũ trên `packet_loop.py`, và
bảng packet của kế hoạch mới không có chúng.

**Quyết: GIỮ.** Lý do: `packet_loop.py` vẫn là thứ cưỡng chế các điều kiện dừng của
protocol §12 mà **cả hai** kế hoạch đều dựa vào. Hai packet này vá lỗ thật trong nó —
`#177` là trần review đang tự nguyện, `#178` là 9 cửa cưỡng chế không có phản chứng.
Bỏ chúng là bỏ nền móng mà kế hoạch mới đứng lên.

Hệ quả: lane `W0-R*` **không** bị kế hoạch mới thay thế. Nó chạy song song, và
`#177` vẫn phụ thuộc `W0-R1 integrated`.

### 5.5 Hiện vật của kế hoạch cũ trên master

```
CÓ   .claude/dev/launcher.py · launcher_test.py
CÓ   .claude/dev/packet_loop.py · packet_loop_test.py
CÓ   .claude/dev/gate_lifecycle.py · gate_lifecycle_test.py
—    .claude/dev/review_connector.py                       (W0-C1, đã BỎ)
—    .github/workflows/review-connector-shadow.yml         (W1-C2b, đã BỎ)
—    ops/review_receipt.py                                 (W0-R2, còn treo)
—    .github/coordination/schemas/review_verdict.v1.schema.json  (W1-P1, còn treo)
```

---

## 6. Nợ còn treo

1. **Cross-review codex cho `W0-R1`.** Assurance hiện là `same_provider_approved`
   (reviewer Fable 5, cùng nền Claude với executor). Đo được lúc thẩm định:
   `codex exec` trả `You've hit your usage limit ... try again at Aug 20th, 2026 6:23 AM`.
   Lưu ý: `codex login status` trả `rc=0 Logged in` KỂ CẢ khi hết quota — token còn
   hạn 159,6 h, nghẽn là quota chứ không phải xác thực. Chỉ
   `python3 .claude/dev/launcher.py doctor --kiem-song` cho tín hiệu trung thực.

2. **Hai re-audit của kế hoạch Antigravity** (`AG-T0-04`/PR #163, `AG-T0-02`/PR #164),
   cả hai `landed_reaudit_pending` vì `reviewed_sha` là SHA rút gọn và stale.

3. **`fix/ag-t0-03-regression-guard` chưa land** — chờ review rồi human land trên
   exact SHA, đúng §12.

4. ~~**Nhánh `agent/ag-t0-03-parser-coverage` là nhánh mồ côi.**~~ **ĐÃ XONG** — người
   giữ kho đã xoá tay ba nhánh (`agent/ag-t0-03-parser-coverage`,
   `fix/ag-t0-03-regression-guard`, `ops/tham-dinh-ag-t0-03-hop-nhat-ke-hoach`), và đã
   bật *Automatically delete head branches* nên từ nay nhánh đã merge tự dọn. Lưu ý:
   tuỳ chọn đó **chỉ áp cho lần merge SAU**, không dọn ngược nhánh đã merge trước đó.
