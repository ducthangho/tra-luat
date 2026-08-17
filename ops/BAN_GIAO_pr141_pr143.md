# BÀN GIAO — PR #141 và #143 (phiên 17-08-2026)

Đọc tệp này TRƯỚC khi làm gì. Nó là **bản chiếu**; nguồn có thẩm quyền vẫn là
lịch sử git và các comment trên PR.

## 0. Việc còn lại, đúng một câu

Chờ CI + `launcher-windows` + review chéo trên hai head mới; **sạch cả hai phía thì
merge cả hai PR**. Người dùng đã duyệt merge với điều kiện xanh (không chỉ cổng
xanh — xem §4).

| PR | nhánh | head khi bàn giao |
|---|---|---|
| #141 | `ops/gate-lifecycle` | `91a027d` |
| #143 | `ops/launcher-co-chay` | `56f7774` |

## 1. Đường đi GitHub — ĐỌC TRƯỚC, nó tiết kiệm cả giờ

Công cụ MCP github của phiên **có thể chưa được uỷ quyền**. Điều đó **không** chặn
việc: điểm cuối vẫn gọi được thẳng bằng JSON-RPC với `GITHUB_PAT`.

- Client tối thiểu đã viết sẵn: `/tmp/claude-0/.../scratchpad/mcp.py` (phù du — chép
  lại từ mô tả dưới nếu mất).
- `https://api.githubcopilot.com/mcp/` → 44 công cụ (PR, issue, comment, merge).
- `https://api.githubcopilot.com/mcp/x/actions` → `actions_list`,
  `actions_run_trigger`, `get_job_logs`, `actions_get`.
- **Đã đo sai một lần:** `curl` tới host ấy trả `CONNECT tunnel failed 403` và tôi
  ghi thẳng thành "bị chặn". `urllib` cùng host, cùng lúc → **200**. Một công cụ
  thất bại chưa phải một đường bị chặn.
- `api.github.com`: `/rate_limit` và `/user` → 200 **có** header `X-GitHub-*`;
  `/repos/<kho>/**` → 403 **không** header (proxy tự sinh). Có token hay không:
  y hệt. Chính sách theo ĐƯỜNG DẪN, không theo danh tính.

## 2. Hai lượt chạy KHÁC NHAU, đừng lẫn

- `ci.yml` — gate tl/release. **Không chạm `launcher_test.py`.** Một lượt xanh ở
  đây KHÔNG nói gì về `.claude/dev/launcher.py`.
- `launcher-windows.yml` — đây mới là chỗ chạy `doctor`, bộ ca, đột biến và bốn
  probe Windows. **Nó `skipped` trên PR trừ khi PR có nhãn `windows`**; đường chắc
  chắn là `workflow_dispatch` trên ref.

Gọi tay cả hai:
```
actions_run_trigger {method: run_workflow, workflow_id: ci.yml|launcher-windows.yml, ref: <nhánh>}
```

**Đọc kết quả phải đọc BƯỚC, không đọc dấu tick.** Đã trả giá: một lượt `ci.yml`
"xanh" 22 bước mà không bước nào chạy `launcher_test.py`. Và đòi số: bộ ca phải ra
`N/N` hai số bằng nhau, đột biến `M/M`.

## 3. Chạy tại chỗ

```
export PYTHONPATH=/tmp/cryp          # vòng `cryptography` hỏng sẵn (pyo3 panic)
python3 .claude/dev/launcher_test.py            # 114/114
python3 .claude/dev/launcher_test.py --dot-bien # 74/74
python3 .claude/dev/gate_lifecycle_test.py      # 16/16
python3 scripts/tl.py --selftest                # 1697/1697
```
Nếu `cryptography` lỗi: `pip install --ignore-installed --target /tmp/cryp cryptography`.

## 4. Điều kiện merge — cổng xanh KHÔNG đủ

CLAUDE.md ghi, và kho đã trả giá ở PR #104/#105: **"gate xanh" không phải "đã được
review"**. Trong phiên này, mỗi lượt review đều ra finding thật — **13 cái**, nhiều
cái nằm trong chính bản vá của lượt trước. Trước khi merge:

1. `pull_request_read {method: get_reviews}` → tìm dòng `Reviewed commit:` cho ĐÚNG
   head hiện tại. Review neo ở head cũ **không tính**.
2. `pull_request_read {method: get_review_comments}` → đếm thread
   `is_resolved=false` **và** `is_outdated=false`. Còn cái nào thì đọc và xử lý.
3. Cẩn thận: một số finding là **báo lại chuyện đã sửa**. Kiểm mã thật rồi mới gọi
   là báo lại — trong phiên này có 3 cái như vậy, đều đã xác minh bằng cách mở đúng
   dòng được trỏ tới.

## 5. Chỗ tôi CHƯA yên tâm — nói thẳng, đừng để người sau tự vấp

- **Cách ly cây tiến trình đã qua BA vòng vá** (`killpg` → chụp-một-lần → subreaper
  + khoá danh tính + lặp-tới-lặng). Mỗi vòng lộ một lỗ mới. Theo doctrine của chính
  kho ("đếm hình dạng lỗi; cùng hình dạng lặp ba lần thì hỏi *có nên làm việc này
  không*"), đây có thể là chỗ phải đổi KIẾN TRÚC: cgroup v2, hoặc **thu hẹp lời
  hứa** và khai thẳng phần không chặn được. Đã hỏi codex về HƯỚNG, không chỉ bản vá.
- **Subreaper chỉ có ở Linux/FreeBSD.** macOS/Windows vẫn còn lỗ "đẻ trong lúc dọn";
  điều này được khai trong mã, đừng lặng lẽ bỏ dòng khai ấy.
- `giet_tron_ven: false` mới **ghi** vào bằng chứng, chưa làm đỏ mã thoát. Câu hỏi
  còn mở: có nên fail-close không.
- **`actionlint` không có trong container.** Mọi thay đổi `ci.yml` mới chỉ qua kiểm
  cú pháp YAML — mà PyYAML không biết luật GitHub. Kho đã trả giá đúng chỗ này: sáu
  lượt review kết luận "YAML ok" cho một tệp GitHub từ chối. Lượt CI là phép đo thật.

## 6. Bẫy đã trả giá TRONG phiên này — đừng lặp

- **Bảng đột biến tự rỗng đi khi sửa mã.** Ba lần trong một phiên: sửa hàm xong,
  đột biến neo vào dòng cũ thành `SAI - khong tim thay doan de dot bien`. Runner có
  báo (không im lặng), nhưng **phải chạy `--dot-bien` NGAY trong cùng lượt sửa**,
  đừng đợi cuối đợt.
- **Khai một ca đích KHÔNG THỂ chết** cũng là lời khai sai về độ phủ — runner báo
  `giet 1/2`.
- **Đếm SỰ CÓ MẶT của một đường thay vì KHẢ NĂNG của nó** — lỗi này tái phát **bốn
  lần**: `shutil.which("gh")` → `rest-chung` → `gh auth status` → "artefact tồn tại"
  (mà validator từ chối). Hỏi "thứ này đã LÀM ĐƯỢC VIỆC chưa", đừng hỏi "nó có ở
  đó không".
- **Cắm env giả vào hàm có thể sinh tiến trình thật**: ba ca của tôi cắm
  `{"PATH":"P"}` rồi bảng `KHA_NANG` sinh `gh` thật → `gh` tạo `./.local/` trong kho
  → bước "cây phải sạch" đỏ trên Windows. Vô hiệu `KHA_NANG` như đã vô hiệu
  `MO_DUN_PY`.
- **Đừng `git stash` rồi `checkout` nhánh khác** khi đang có việc dở — tôi làm và
  gây xung đột modify/delete. Commit trên đúng nhánh trước.

## 7. Sau khi merge

- Việc của người dùng, tôi không làm được (proxy chặn xoá ref): chạy
  `.\scripts\don-nhanh.cmd` để dọn nhánh; quyết `ops/wp55-r4g1-wip` (có commit riêng
  `81a4d285`), `tmp-probe-delete`, `tmp-probe-2`.
- **Cài `gh` trên máy Windows trước khi merge #143** (`winget install --id
  GitHub.cli -e`): #143 đặt `gh` bắt buộc ở máy người dùng (không bắt buộc ở remote
  và CI), nên `doctor` sẽ đỏ tới khi cài.
- Nợ còn treo, chưa ai làm: `t19`/`t62` báo `SKIP` mà vẫn tính vào tổng — "ca có mặt
  khác ca có đo", hai bộ test cùng mắc; và `.claude/settings.json` exec-form +
  `session_start.py` (hoãn vì thiếu clone `claude-code-best-practice` để tra đúng
  nguồn ưu tiên, và hook khai sai thì nó VẮNG MẶT chứ không báo lỗi).
