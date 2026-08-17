# BÀN GIAO — lớp cách ly gate (cgroup v2) và sổ nợ kèm theo

Đọc tệp này TRƯỚC khi làm gì. Nó là **bản chiếu**; nguồn có thẩm quyền vẫn là
lịch sử git, `ops/NO_KY_THUAT.md`, và comment trên PR.

Viết lúc PR sổ-nợ vòng 3 (`ops/so-no-vong-3`) **chưa merge**; mọi thứ khác đã ở
trên master.

## 0. Việc còn lại, đúng một câu

Merge PR sổ-nợ vòng 3, rồi xử sổ nợ `ops/NO_KY_THUAT.md` (còn 6 mục) — **không
mở vòng vá thứ n cho lớp cách ly tiến trình**, xem §4.

## 1. Đã land gì (đừng làm lại)

| PR | nội dung | commit trên master |
|---|---|---|
| #141 | **cgroup v2** thay vòng quét cây; fail-close khi dọn không trọn vẹn | `a70f481` |
| #154 | chặn tín hiệu **TRƯỚC** khi cắm handler; đóng khe `rc=1` + rò cgroup | `5f6eb92` |
| #152 | (đóng, gộp vào #154) | — |

Lớp cách ly hiện tại: **Linux → cgroup v2 `cgroup.kill`** · **Windows → Job
Object** · **macOS/FreeBSD → quét cây** (lỗ "đẻ trong lúc dọn" CÒN NGUYÊN, được
khai thẳng trong mã, đừng lặng lẽ bỏ dòng khai ấy).

## 2. Đường đi công cụ — đọc trước, tiết kiệm cả giờ

- **Mở phiên là chạy `doctor` trước mọi việc khác** (CLAUDE.md nay đòi thế).
  `codex` thường CHƯA cài: `npm install -g @openai/codex` rồi
  `python .claude/dev/launcher.py chuan-bi`, kiểm bằng `codex login status`.
  `doctor` **thoát 0 DÙ THIẾU `codex`** — đọc dòng `khong codex`, đừng đọc mã
  thoát thành "đủ đồ".
- **Hook phiên có thể KHÔNG chạy lần nào**: phiên remote gắn kho GIỮA phiên thì
  `CLAUDE_PROJECT_DIR` không được đặt, lệnh hook giải ra `/.claude/hooks/...` và
  **vắng mặt lặng lẽ**. `doctor` mục `hook-phien` so BĂM tệp, tức đo "tệp có mới
  không" chứ KHÔNG đo "hook đã chạy chưa".
- `gh` KHÔNG có và kho cố ý không dùng. GitHub đi qua **MCP JSON-RPC** tới
  `https://api.githubcopilot.com/mcp/` với `GITHUB_PAT`, dùng **`urllib`** —
  KHÔNG `curl` (curl bị proxy chặn 403, urllib cùng host trả 200).
  Endpoint này **chập chờn**: gặp 503/404 thì thử lại vài lần rồi mới kết luận.
  `REST /repos/**` luôn 403 — chính sách theo ĐƯỜNG DẪN, không theo danh tính.

## 3. Chạy tại chỗ

```
python .claude/dev/gate_lifecycle_test.py                     # 26/26
TL_GATE_TAT_CGROUP=1 python .claude/dev/gate_lifecycle_test.py # 26/26 (giả lập macOS)
python scripts/tl.py --selftest                                # 1697/1697
python .claude/dev/launcher_test.py                            # 118/119 QUA
python .claude/dev/launcher_test.py --dot-bien                 # 94/94
python .claude/dev/packet_loop.py doctrine-scan --root .       # sạch
```

`tl selftest` cần `git config --global core.abbrev 7` như `ci.yml`; không ghim
thì `r218`/`r264` đỏ — **đó là môi trường, không phải hồi quy**.

## 4. Chỗ tôi CHƯA yên tâm — nói thẳng

- **Lớp cách ly đã qua NĂM vòng vá** (killpg → chụp một lần → subreaper → điều
  kiện lặng → cgroup → chặn tín hiệu sớm). Doctrine của kho: cùng hình dạng lặp
  ba lần thì hỏi *có nên làm việc này không*. Nếu vòng sáu ló ra, **dừng và hỏi
  người dùng** thay vì vá.
- **Khe "cố tình trèo ra" KHÔNG chặn được** bằng uỷ quyền cgroup không đặc quyền:
  quyền cần để chuyển VÀO chính là quyền cho phép trèo RA một tầng. Sổ nợ mục 1.
  Đã thử một bản PHÁT HIỆN và **đo thấy nó sai cả hai chiều** — đừng làm lại
  bản ấy mà không đọc mục 1 trước.
- **Mức review**: Codex HẾT QUOTA. Claude review Claude chỉ là
  `same_provider_approved` (§8 mục 3) — **KHÔNG đủ** cho PR đụng workflow/security.
  Phiên Claude cũng đã báo `seven_day: allowed_warning`.
- **Branch protection cưỡng chế up-to-date**: `behind` thì merge trả 405
  "Required status check `gate (ubuntu-latest)` is expected". Không có đường tắt
  — hoà master, chạy lại, chờ CI, rồi mới merge.

## 5. Bẫy đã trả giá TRONG đợt này — đừng lặp

- **Vá tệp bằng script mà tìm chuỗi từ ĐẦU TỆP**: `s.index(moc_ket)` không truyền
  vị trí bắt đầu → khớp một chỗ sớm hơn → `s[:i] + moi + s[j:]` **nhân bản** cả
  một vùng ~5 ca. Nó **không báo lỗi**, nó làm hỏng nội dung. Rồi bản "dọn trùng"
  cắt theo `dòng bắt đầu bằng "def "` lại **ghép đầu ca này vào thân ca kia** —
  và tổng `N/N` KHÔNG lộ ra vì `CASES` chỉ liệt kê tên. **Dùng ranh giới AST.**
- **Dựng nội dung dài bằng chuỗi nội tuyến trong `python3 -c "..."`**: shell nuốt
  phần trong dấu backtick (command substitution) → đăng lên PR một comment hỏng
  mà không hay. **Ghi ra TỆP rồi đọc tệp.**
- **Đặt probe sai chỗ rồi kết luận "reviewer sai"**: tôi chèn độ trễ SAU
  `atexit.register` nên không thấy rò cgroup, suýt bác một P1 đúng. Đặt đúng
  khoảng mới thấy.
- **Đọc giới hạn của phép đo MÌNH DỰNG thành thuộc tính của thứ được đo**: tôi
  cắt log bằng `tail -1` rồi kết luận "runner không in tên ca hỏng" — nó in sẵn.
- **Ghép số của hai lượt chạy vào một câu** (`thoát 12` + `ok=True`): hai thứ ấy
  bất khả cùng lượt. Giữ nguyên stdout của ĐÚNG lượt bất thường.
- **Bảng số theo giây là hệ quả, không phải nguyên nhân**: mốc thời gian không
  đơn điệu vì preflight dài ngắn tuỳ máy/tải. Neo phép đo vào **PHA**.

## 6. Sổ nợ — `ops/NO_KY_THUAT.md`

Còn **6 mục** (mục 4 đã đóng: nhánh khác sửa headline `launcher_test`, đi xa hơn
điều kiện đặt ra). Mỗi mục ghi *đo được gì / vì sao chưa làm / điều kiện coi là
xong*. Đọc mục 1 và mục 7 trước — hai mục ấy có nhiều người dễ vấp lại nhất.

Manh mối nóng nhất: **mục 7** — `doctor` chớp (thoát 12 rồi 0). Cơ chế đã dựng
lại được bằng shim: một lượt `--version` hết hạn ⇒ bị đếm là thiếu. Lần chớp tới
chỉ cần chạy `doctor --json` và **giữ nguyên stdout** là đóng được nửa đường.

## 7. Việc của người dùng, đừng làm hộ

Xoá nhánh: container **không xoá được ref** (`git push --delete` → 403) và
`ops-don-ref.yml` cố ý bảo vệ `ops/**`. Người dùng chạy `.\scripts\don-nhanh.cmd -Xoa`.
Đang chờ xoá: `ops/gate-lifecycle`, `ops/no-ky-thuat-muc6`, `ops/tin-hieu-chan-som`.
