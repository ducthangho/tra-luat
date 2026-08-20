# Prompt BẤT BIẾN — Executor `PLAT-M4`, lượt 1, provider `claude`

Tệp này là hợp đồng của MỘT lượt executor. Nó **không** cấp quyền: quyền đến từ
`ops/leases/plat-m4-exec-1-claude-20260820.yaml` (bản chiếu: comment trên `#194`).
Sửa tệp này sau khi lease đã cấp là làm **băm lệch** ⇒ cổng đăng lease trả `rc=6`.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#194` — `[WP PLAT-M4]` |
| revision · generation | 1 · 1 |
| spec | **thân Issue `#194`** là authority. Bản chiếu đọc offline: `ops/specs/plat-m4-packet-issue-nhap.md` — tìm ở `master` trước, chưa thấy thì fetch nhánh `claude/opus-5-plan-steps-y5r6ci` |
| base / start head | `50d8d12e146792368e7100f732ff15a8d32fe48d` (`origin/master` lúc cấp lease) |
| nhánh làm việc | `claude/plat-m4-exec-1` — dựng TỪ base trên, `branch_ownership: exclusive` |
| role | `executor`. KHÔNG review, KHÔNG approve, KHÔNG land việc của chính mình |
| effective write set | đúng hai tệp: `.claude/dev/launcher.py` · `.claude/dev/launcher_test.py` |
| review class | `sensitive` · assurance đích `cross_approved` · reviewer `codex` |
| mô hình · effort | Claude Opus 5 · `xhigh` |
| hạn (wall clock) | lease tới `2026-08-21T06:45:00Z`; `timeout_clock=wall`, fail-closed |

## 2. Việc phải làm

Tách trường `mcp` của `doctor` thành **hai** trường đo hai thứ khác nhau:

- `mcp-cli` — giữ nguyên phép đo hiện có (`_doc_mcp_json` + `claude mcp get`), tức **dây nối**
  phía CLI;
- `mcp-endpoint` — **một lượt `initialize` JSON-RPC thật** tới URL khai trong `.mcp.json`,
  phân loại theo **header `X-GitHub-*`** đúng khuôn `_do_rest_github`.

Năm chốt ở §3 thân Issue `#194` **đã đóng**, thi công theo đúng chúng:

1. mở rộng `t115` sang **cả hai** tên mới — nếu không, ca ấy vẫn xanh mà không còn canh gì;
2. `mcp-endpoint` **KHÔNG** vào `LAM_DUOC_VIEC` (giữ `{git, gh-kho, rest-kho}`);
3. `initialize`, timeout theo `PROBE_TIMEOUT_GIAY`, **không** auto-retry;
4. ca sentinel: token **không** lộ ra byte đầu ra nào, kể cả `--json`;
5. suite chạy **offline**, bốn fixture trạng thái.

## 3. Nghiệm thu và phản chứng

Đọc §4 và §5 của thân Issue `#194`. Bảy phản chứng ở §5 là **bắt buộc**, mỗi đột biến phải
**giết 1/1**. Số nền phải giữ: **137 ca** (`rg -c '^def t[0-9]+_' .claude/dev/launcher_test.py`
đo trên base). `N/N` phải là **hai số bằng nhau**; `rc` đọc **trực tiếp từ tiến trình**, không
qua pipe.

## 4. Điều kiện DỪNG

- Chốt phải nằm ngoài hai tệp write set ⇒ dừng, xuất handoff, mở packet riêng. **Không tự mở
  write set.**
- Cùng một hình dạng lỗi lần thứ hai ⇒ dừng, quyết định về **cách làm**, không mở vòng vá thứ ba.
- Trần review **2 vòng**; hết trần mà chưa approve ⇒ Review Rescue Checkpoint, người giữ chọn.
- Thấy một chốt ở §3 Issue là sai ⇒ **DỪNG và mở revision**, không tự đổi giữa đường.

## 5. Cấm

- Không secret trong bất kỳ đầu ra nào; kiểm biến bí mật bằng **sự tồn tại**, không in nội dung.
- Không `--dangerously-skip-permissions`, không `danger-full-access`, không bypass hook.
- Không merge/land, không xoá nhánh, không ép lùi.
- Không đọc `rc=0` thành bằng chứng: đòi **bằng chứng dương** (`N/N` hai số bằng nhau, `"ok": true`).

## 6. Handoff bắt buộc khi kết thúc lượt

Tối thiểu: packet/revision/generation · base và exact head · provider/model/session/role ·
write set khai báo **và** changed paths thực · lệnh test, `rc`, số đếm dương, skipped/not-run
tách riêng · từng phản chứng đã chạy và invariant nó đo · việc còn lại · vai kế tiếp và **một**
hành động thủ công cụ thể.
