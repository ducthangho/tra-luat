# Gọi agent đa nền — tất định, không script spawn tự chế

**Phạm vi.** Cách gọi một phiên Claude hoặc Codex sao cho chạy *giống nhau* trên
máy Windows, macOS/Linux, điện thoại (qua phiên remote) và CI — và sao cho khi
hỏng thì hỏng ở chỗ đọc được.

## Nguyên tắc: chốt là của ta, việc gọi agent là của CLI chính thức

Chúng ta **không viết script spawn agent**. Hai CLI chính thức đã làm việc đó và
được nhà cung cấp bảo trì:

| agent | CLI | cài |
|---|---|---|
| Claude | `claude` | `npm install -g @anthropic-ai/claude-code` |
| Codex | `codex` | `npm install -g @openai/codex` |

`\.claude/dev/launcher.py` **không** gọi agent. Nó dựng các chốt quanh *bất kỳ*
lệnh nào rồi chạy lệnh đó. Nghĩa là nó không cần biết agent nào, không có prompt
dựng sẵn, không có logic phiên — CLI đổi giao diện thì ta không phải sửa gì.

Ranh giới đó là cố ý. Một wrapper spawn tự chế sẽ phải bám theo cờ, biến môi
trường và cơ chế xác thực của hai CLI khác nhau, rồi trôi lệch âm thầm — đúng
lớp lỗi mà `## Bài học đắt giá` trong `CLAUDE.md` đã trả giá nhiều lần.

## Trước tiên: đủ công cụ chưa

```bash
python .claude/dev/launcher.py doctor          # người đọc
python .claude/dev/launcher.py doctor --json   # máy đọc
```

Thoát `12` khi thiếu công cụ **bắt buộc** (git, python). Thiếu `claude`/`codex`
chỉ là cảnh báo — có phiên không cần gọi agent nào cả.

Đã đo trong container Claude Code web (12-08-2026): có `python`, `git`, `node`,
`claude`, `rg`; **không có** `codex`, `gh`, `pwsh`. Hook
`.claude/hooks/session-start.sh` cài phần thiếu khi phiên remote khởi động.

Trên Windows **không có lệnh `python3`**, chỉ `python` và `py`. Đừng cài thêm bí
danh — `doctor` nhận cả ba tên.

## Các chốt

Chạy trước khi gọi agent, hoặc gói luôn lượt gọi:

```bash
# chỉ kiểm, không gọi gì
python .claude/dev/launcher.py check \
  --expected-repo ducthangho/tra-luat \
  --expected-root-commit <sha40> \
  --expected-head <sha40> --expected-ref <nhánh> --require-clean --json

# kiểm rồi gọi CLI chính thức; lệnh đặt sau `--`
python .claude/dev/launcher.py run \
  --run-root ~/.tl-runs --name codex-review \
  --expected-repo ducthangho/tra-luat \
  --prompt-file nhiem_vu.txt --expected-prompt-sha256 <sha256> \
  --deadline-utc 2026-08-13T09:00:00Z \
  -- codex exec -s read-only "Doc tep nhiem_vu.txt va thuc hien dung theo do."

python .claude/dev/launcher.py status --run-root ~/.tl-runs --id <short_id>
python .claude/dev/launcher.py stop   --run-root ~/.tl-runs --id <short_id>
```

Gọi Claude thì thay phần sau `--` bằng `claude -p "..."`. Không có gì khác đổi.

### Neo theo *kho*, không theo đường dẫn

`--workspace` không bắt buộc: thứ tự là `--workspace` → `$TL_WORKSPACE` → thư mục
hiện tại, rồi luôn hỏi `git rev-parse --show-toplevel`. Đường dẫn tuyệt đối là
thứ **duy nhất không mang được sang máy khác** — phiên remote clone kho vào một
đường dẫn không ai biết trước.

Danh tính kho lấy từ `--expected-repo` (chuẩn hoá qua bốn dạng URL, cắt phần đăng
nhập nên token không lọt ra) và `--expected-root-commit` (vân tay bền nhất: không
đổi khi kho bị đổi tên, chuyển chủ, fork; đọc được không cần mạng).

Nêu **host** thì chốt đòi bằng nhau tuyệt đối. Chỉ nêu `owner/repo` thì nó so N
đoạn cuối — nghĩa là bạn chấp nhận không phân biệt host. Muốn chặt thì nêu host,
hoặc dùng commit gốc.

## Mã thoát

| mã | nghĩa |
|---|---|
| 0 | qua hết |
| 2 | tham số sai |
| 3 | không phải repo git / git không chạy được |
| 4 · 5 · 6 | HEAD lệch · ref lệch · worktree bẩn |
| 7 · 8 | prompt (thiếu/rỗng/sha lệch) · hạn chót đã qua |
| 10 | không xác định được danh tính tiến trình → **từ chối giết** |
| 11 | kho không đúng |
| 12 | thiếu công cụ bắt buộc |
| 124 | quá hạn **và đã giết được** |
| 125 | quá hạn **nhưng KHÔNG giết được** — cần người can thiệp |

Tách 124/125 là có lý do: bản trước trả 124 trong khi tiến trình mẹ lẫn cháu vẫn
sống, nên phía gọi tưởng đã dọn xong.

## Ba đường vào, cùng một lệnh

- **Máy cá nhân** — `cd` vào kho rồi chạy. Windows dùng `python`, không `python3`.
- **Điện thoại / Claude Code web** — phiên remote clone kho vào container; hook
  `SessionStart` cài công cụ; lệnh giống hệt vì không có đường dẫn cứng nào.
- **CI** — đặt `TL_WORKSPACE`, còn lại giống hệt.

## Chạy bộ phản chứng

```bash
python .claude/dev/launcher_test.py             # 55 ca
python .claude/dev/launcher_test.py --dot-bien  # 14 đột biến, mỗi cái phải giết đúng ca chỉ định
```

Ba ca tự bỏ qua trên Windows (git giả, giết con cháu, `stop` giết thật) vì cần
cây tiến trình thật. **Chưa chạy trên Windows thì đường Windows chưa được nghiệm
thu** — đúng bài học "script đa nền phải chạy THẬT trên nền đó".
