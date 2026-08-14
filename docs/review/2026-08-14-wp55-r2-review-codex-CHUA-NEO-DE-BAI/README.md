# wp55 r2 — review bằng codex — **CHƯA NEO ĐỀ BÀI, KHÔNG phải artifact §8**

> **ĐỌC DÒNG NÀY TRƯỚC.** Thư mục này **KHÔNG** thoả §8 và **KHÔNG** được dùng để
> chuyển `assurance_target: cross_approved`. Nội dung review dùng được; tư cách thủ
> tục thì không. Ba chỗ lệch nêu ở dưới, không chỗ nào che giấu.

> **HEAD ĐÃ DỊCH — bản review này neo vào một head KHÔNG còn là đầu PR.**
> Lượt review đọc `22d2cc92164ca2018c0560aaf9404659ea81f51e`. Finding CHẶN của nó
> đã được sửa, và bản sửa `cf39109c9e5167516c53f2071e5fa7ec5c6afff5` đã
> fast-forward vào nhánh PR ngày 2026-08-14 — nên đầu PR #92 nay là `cf39109c`.
>
> Mọi kết luận dưới đây **chỉ đúng với `22d2cc9`**. Theo đúng luật của kho ("mở lượt
> mới thì bản duyệt cũ hết hiệu lực"), bản review này **không còn hiệu lực** với đầu
> PR hiện tại; lease kế tiếp phải neo `reviewed_sha_required: cf39109c…`.
>
> Đã đo lại trên head mới: merge với master **sạch, 0 xung đột**; suite trên cây đã
> merge **48/48 đạt**; write_set vẫn đúng **6 tệp**.

## Lượt chạy này là gì

Một lượt review thật do `codex` chạy trên write_set của PR #92, gọi qua
`.claude/dev/launcher.py` nên có neo HEAD, neo prompt, hạn chót và sổ lượt chạy.
Chạy ngày 2026-08-14 theo lệnh trực tiếp của chủ kho, **sau khi lease #2 đã hết hạn**,
và **không có** prompt đã neo trong tay.

Giữ lại vì bằng chứng kỹ thuật vẫn giá trị: nó tái hiện được một lỗ CHẶN.

## Ba chỗ LỆCH so với lease `wp55-r2-review-2-codex-20260813`

| Điều kiện lease | Thực tế lượt này |
|---|---|
| `provider: codex` | ✅ `codex-cli 0.147.0`, `Logged in using ChatGPT` |
| `reviewed_sha_required: 22d2cc92164ca2018c0560aaf9404659ea81f51e` | ✅ launcher neo `--expected-head`, khớp |
| `base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2` | ✅ merge-base đo lại, khớp |
| `lease_expires_at_utc: 2026-08-13T18:30:00Z` | ❌ chạy `2026-08-14T01:31:29Z` — **ngoài cửa sổ ~7 giờ** |
| prompt neo `sha256:46a833cc…550dfc` (5292 byte) | ❌ dùng `prompt-da-dung.md`, `sha256:40bf9181…5132` (4065 byte). Đề bài gốc chỉ nằm trong comment #55, phiên chạy không có quyền GitHub API để đọc |
| `access: read-only`, `write_set: []` | ❌ chạy `codex exec --sandbox workspace-write`. Codex có sửa tệp để thử phá chốt rồi khôi phục; worktree kiểm lại **sạch** (`git status -uall` rỗng) |
| `heartbeat_required_minutes: 30` | ❌ không đăng được lên #55 (`api.github.com` trả 403 cho phiên này) |

Hai trong ba chỗ lệch là do phiên điều phối (`claude`) quyết định, không phải do
reviewer: chọn đề bài thay thế, và mở `workspace-write` để reviewer chạy được test.

## Kết luận của reviewer

`VERDICT: CHANGES_REQUESTED` — một finding mức **CHẶN**:

> `.claude/dev/packet_loop.py:335` — `init` tự ghi state `leased` mà không đòi bất
> kỳ bằng chứng hoặc uỷ quyền lease nào. Tái hiện: `init --packet 999999 --mission
> 888888 --executor claude --reviewer codex` → `rc=0`, state `leased`; `begin-attempt`
> → `rc=0`, state `running`.

Đây đúng vùng mà acceptance #55 r2 đòi **chặn từ `init`**, trong khi commit
`22d2cc9` tự nhận "acceptance CHỈ CÒN MỘT CỬA".

Toàn văn ở `stdout.log`.

## Bằng chứng reviewer đã thực sự đo (không đọc chay)

- `packet_loop_test.py`: **43/43** nền; tự đột biến giết **4/4**
- Tự tay phá chốt `attempt_open` rồi chạy lại: **42/43**, đúng ca
  `vao_reviewing_phai_co_luot_dang_mo` chuyển ĐỎ — rồi khôi phục
- `doctrine-scan --root .`: 4 tệp, 0 chỗ chép doctrine; doctrine động 11/11 dòng được phủ
- Tự khai **KHÔNG ĐO ĐƯỢC**: lệnh GitHub thật trong adapter, và hành vi trên Windows

## Tệp trong thư mục

| tệp | nội dung |
|---|---|
| `run.json` | sổ lượt chạy của launcher (neo HEAD, sha prompt, chốt công cụ + xác thực, hạn chót) |
| `stdout.log` | verdict nguyên văn của reviewer |
| `stderr.log` | toàn bộ vết chạy của codex (86.864 token) |
| `prompt-da-dung.md` | đề bài **thay thế** đã dùng — không phải đề bài đã neo |

## Muốn có artifact §8 hợp lệ thì cần

0. Neo vào **`cf39109c`** (đầu PR hiện tại), KHÔNG phải `22d2cc9` như lượt này
1. Lease #3 còn hiệu lực tại thời điểm chạy
2. Đúng prompt neo `sha256:46a833cc…550dfc`
3. `--sandbox read-only` (hoặc sửa lease cho phép ghi trong worktree dùng một lần)
4. Heartbeat 30 phút lên #55

Cả bốn đều cần một phiên **có quyền GitHub API** — xem mục "Quyền GitHub gắn theo
XUẤT XỨ phiên" trong `CLAUDE.md`.
