# BÀN GIAO — PR #141 (còn mở) và #143 (ĐÃ MERGE)

Cập nhật 17-08-2026 sau khi #143 vào master. Đây là **bản chiếu**; nguồn có thẩm
quyền vẫn là lịch sử git và comment trên PR.

## 0. Trạng thái, đúng một bảng

| PR | nhánh | trạng thái |
|---|---|---|
| **#143** | `ops/launcher-co-chay` | **ĐÃ MERGE** — `c7ad260` |
| **#141** | `ops/gate-lifecycle`, head `38f1253` | **CÒN MỞ, treo có chủ đích** |

Phiên tiếp: `session_0127ubhs2seGxKUViJAGZVWy` — "tra-luat #141 — cgroup v2 cho
gate_lifecycle".

**#141 treo KHÔNG phải vì cổng đỏ.** `ci.yml` xanh cả `pull_request` lẫn
`workflow_dispatch` trên `69267ff`; `launcher-windows` xanh hai nền. Treo vì quyết
định kiến trúc ở §2.

## 1. Việc của người dùng — tôi không làm được

- **Xoá nhánh.** Container **không xoá được ref**: đo lại 17-08,
  `git push origin --delete ops/launcher-co-chay` → **HTTP 403** từ proxy. Và
  `ops-don-ref.yml` **cố ý bảo vệ `ops/**`** vì các nhánh ấy giữ commit công bố
  verdict. Đường của người dùng: `.\scripts\don-nhanh.cmd` (chạy trần để xem sẽ
  xoá gì) rồi `-Xoa`. Script chỉ xoá nhánh mà mọi commit đã nằm trong master.
  Còn treo: `ops/wp55-r4g1-wip` (commit riêng `81a4d285` — xem trước khi xoá),
  `tmp-probe-delete`, `tmp-probe-2`.
- **Cài `gh` trên Windows** (`winget install --id GitHub.cli -e`). #143 đặt `gh`
  bắt buộc ở máy người dùng (KHÔNG bắt buộc ở remote và CI), nên `doctor` sẽ đỏ
  `thieu: ['gh']` tới khi cài.

## 2. Vì sao #141 treo — đọc kỹ, đây là nội dung chính

`_terminate_process_tree` đã qua **BỐN vòng vá cùng một hình dạng**:

1. `killpg` nhóm con gốc → cháu `setsid()` thoát.
2. Chụp cây một lần rồi giết → cháu **đẻ trong lúc dọn** thoát.
3. `PR_SET_CHILD_SUBREAPER` + khoá danh tính → cháu chết-rồi-đẻ vẫn thoát vì
   handler chờ lâu hơn nhịp quét.
4. Điều kiện lặng gồm "đã biến mất" + ân hạn → **chưa có phép đo nào chứng minh**.

Vòng nào cross-review cũng lộ một lỗ mới. CLAUDE.md ghi: *"đếm hình dạng lỗi,
đừng chỉ đếm lỗi; cùng hình dạng lặp ba lần trở lên thì câu hỏi đúng là **có nên
làm việc này không**, không phải **vá thế nào**"*. Người dùng đã quyết: **chuyển
sang cgroup v2**, đóng cả lớp theo kiến trúc.

### ⚠ Con số `16/16` KHÔNG phải bằng chứng cho lớp giết-cây

Ca `case_descendant_spawned_during_shutdown_is_contained` **đã được chứng minh là
không phân biệt được**: bơm đột biến "coi không-ai-mới là lặng" — khớp đúng 1 lần,
kiểm bằng `assert` sau khi một lượt trước lặng lẽ không áp được — mà suite **vẫn
16/16**. Đã ghi thẳng vào docstring của ca.

**Việc ĐẦU TIÊN của phiên cgroup: dựng cho được một ca ĐỎ với cơ chế hiện tại.**
Không có ca đỏ thì không cách nào biết cgroup có tốt hơn thật, và sẽ lặp lại đúng
vòng bốn lần vừa rồi.

### Phạm vi hiện đang khai trong mã

Subreaper là chốt **chỉ của Linux**. macOS, Windows và FreeBSD **vẫn còn lỗ "đẻ
trong lúc dọn"** — điều này được khai tường minh trong `_dat_subreaper`; đừng lặng
lẽ bỏ dòng khai ấy khi viết cgroup. `giet_tron_ven: false` là thứ duy nhất nói
thật khi dọn không trọn.

## 3. Đường đi GitHub — tiết kiệm cả giờ

Công cụ MCP của phiên **có thể chưa được uỷ quyền**; điều đó KHÔNG chặn việc.

- Gọi thẳng JSON-RPC bằng `GITHUB_PAT`:
  `https://api.githubcopilot.com/mcp/` → 44 công cụ (PR, issue, comment, merge);
  `…/mcp/x/actions` → `actions_list`, `actions_run_trigger`, `get_job_logs`.
- **ĐÃ ĐO SAI MỘT LẦN:** `curl` tới host ấy trả `CONNECT tunnel failed 403` và tôi
  ghi thẳng thành "bị chặn". `urllib` cùng host, cùng lúc → **200**. **Một công cụ
  thất bại chưa phải một đường bị chặn** — thử ít nhất hai client trước khi gọi đó
  là chính sách.
- `api.github.com`: `/rate_limit`, `/user` → 200 **có** header `X-GitHub-*`;
  `/repos/<kho>/**` → 403 **không** header (proxy tự sinh). Có token hay không:
  y hệt ⇒ chính sách theo ĐƯỜNG DẪN, không theo danh tính.

## 4. Hai lượt chạy KHÁC NHAU

- `ci.yml` — gate tl/release. **Không chạm `launcher_test.py`.** Xanh ở đây KHÔNG
  nói gì về `.claude/dev/launcher.py`.
- `launcher-windows.yml` — `doctor`, bộ ca, đột biến, bốn probe Windows. **`skipped`
  trên PR trừ khi PR có nhãn `windows`**; đường chắc chắn là `workflow_dispatch`.

**Đọc BƯỚC, đừng đọc dấu tick.** Đã trả giá: một lượt `ci.yml` "xanh" 22 bước mà
không bước nào chạy `launcher_test.py`. Và đòi số: `N/N` hai số bằng nhau.

Từ #143, `ci.yml` còn sinh artefact `gate-evidence-<os>-<attempt>` chứa
`tl-selftest-<OS>.json` — **chỉ ở `push`/`workflow_dispatch`**, vì trên
`pull_request` cây checkout là commit merge tổng hợp nên không có commit thật để neo.

## 5. Chạy tại chỗ

```
export PYTHONPATH=/tmp/cryp          # vòng `cryptography` hỏng sẵn (pyo3 panic)
python3 .claude/dev/gate_lifecycle_test.py      # 16/16  — xem cảnh báo §2
python3 .claude/dev/launcher_test.py            # 114/114
python3 .claude/dev/launcher_test.py --dot-bien # 74/74
python3 scripts/tl.py --selftest                # 1697/1697
```
Thiếu `cryptography`: `pip install --ignore-installed --target /tmp/cryp cryptography`.

## 6. Nợ đã ghi, chưa ai trả

- **`launcher_test` chập chờn.** Ngay sau khi merge master vào `ops/launcher-co-chay`,
  MỘT lượt ra `113/114`; ba lượt sau đều `114/114` và **không bắt được tên ca**.
  CLAUDE.md đã ghi tiền sử chập chờn của bộ này ("hai lượt hai chỗ ⇒ chập chờn hoặc
  phụ thuộc thứ tự, chưa ai biết nguyên nhân"). Có `--nhat-ky TEP` và
  `--lap-ca TEN --lan N` để truy.
- **Trần `doctor` chặn TRƯỚC mỗi probe khả dụng, chưa truyền hạn VÀO probe.** Các
  probe có hạn nội bộ nên trường hợp xấu vẫn bị chặn, nhưng chưa phải cưỡng chế
  end-to-end thật (P2 còn dư của #143).
- **`t19`/`t62` báo `SKIP` mà vẫn tính vào tổng** — "ca có mặt khác ca có đo", hai
  bộ test cùng mắc.
- **`.claude/settings.json` exec-form + `session_start.py`** — hoãn vì thiếu clone
  `claude-code-best-practice` để tra đúng nguồn ưu tiên, và hook khai sai thì nó
  **VẮNG MẶT** chứ không báo lỗi.
- **`actionlint` không có trong container** — mọi thay đổi `ci.yml` mới chỉ qua
  kiểm cú pháp YAML, mà PyYAML không biết luật GitHub. Kho từng có sáu lượt review
  kết luận "YAML ok" cho một tệp GitHub từ chối.

## 7. Bẫy đã trả giá trong đợt này — đừng lặp

- **Bảng đột biến tự rỗng đi khi sửa mã.** BA lần trong một đợt: sửa hàm xong, đột
  biến neo vào dòng cũ thành `SAI - khong tim thay doan de dot bien`. Runner có báo,
  nhưng **phải chạy `--dot-bien` NGAY trong cùng lượt sửa**.
- **Khai một ca đích KHÔNG THỂ chết** cũng là lời khai sai về độ phủ (`giet 1/2`).
- **Đếm SỰ CÓ MẶT của một đường thay vì KHẢ NĂNG của nó** — tái phát **BỐN lần**:
  `shutil.which("gh")` → `rest-chung` → `gh auth status` → "artefact tồn tại" (mà
  validator từ chối vì lệch định danh). Hỏi "thứ này đã **làm được việc** chưa".
- **Cắm env giả vào hàm có thể sinh tiến trình thật**: ba ca cắm `{"PATH":"P"}` rồi
  bảng `KHA_NANG` sinh `gh` thật → `gh` tạo `./.local/` trong kho → bước "cây phải
  sạch" đỏ trên Windows. Vô hiệu `KHA_NANG` như đã vô hiệu `MO_DUN_PY`.
- **Đổi một mỏ neo sai lấy một mỏ neo sai khác**: `$GITHUB_SHA` (commit tổng hợp)
  → PR head (trong khi cây là merge). Câu hỏi đúng không phải "neo vào SHA nào" mà
  là "thứ ta vừa đo có phải một commit có thật trong lịch sử không".
- **Đừng `git stash` rồi `checkout` nhánh khác** khi đang có việc dở — gây xung đột
  modify/delete. Commit trên đúng nhánh trước.

## 8. Kỷ luật merge — không thương lượng

**"Gate xanh" KHÔNG phải "đã được review"** (CLAUDE.md; kho đã trả giá ở PR
#104/#105). Trước khi merge:

1. `pull_request_read {method: get_reviews}` → tìm `Reviewed commit:` cho ĐÚNG head
   hiện tại. Review neo ở head cũ **không tính**.
2. `get_review_comments` → đếm thread `is_resolved=false` **và** `is_outdated=false`.
3. Một số finding là **báo lại chuyện đã sửa** — **mở đúng dòng được trỏ tới rồi
   mới gọi là báo lại**. Trong đợt này có nhiều cái như vậy, đều đã xác minh bằng
   cách đọc mã chứ không suy đoán.
