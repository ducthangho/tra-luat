# Prompt review lượt 2 — `doctor`: đo GitHub theo đúng đường MCP

Bạn là REVIEWER, provider `codex`. Người vá là `claude` (§8 cross-provider). CHỈ ĐỌC.

Nguồn có thẩm quyền của lượt này là TỆP CÓ BĂM trong kho (lease + prompt này). Comment
trên #55 chỉ là bản chiếu.

## Lượt 1 đã xảy ra gì

Verdict lượt 1: `changes_requested` trên `4ff2c6bfe04a205e5989642bc527bc5341db3e0f`, ba
finding — và **finding P1 bác đúng một lời khai của người vá**:

- **P1** `_do_github_api` khai tuyệt đối rằng tiến trình con không đo được MCP, rồi trả
  `KHONG_DO_DUOC` vô điều kiện. Reviewer đưa phép đo chạy được: `claude mcp list` in ra
  server, endpoint và trạng thái health/approval (`Pending approval` trong container ấy).
- **P2** tên server khớp chuỗi con (`"github" in k.lower()`) nên `not-github-backup` được
  tính là đã khai github.
- **P2** `.mcp.json` JSON hợp lệ nhưng sai lược đồ: mảng ở gốc làm `d.get` ném
  `AttributeError`; `{"mcpServers": ["github"]}` bị đọc thành "đã khai server".

Reviewer cũng báo **hai đột biến SỐNG SÓT** qua `t105`: đổi nhận diện tên thành phân biệt
hoa/thường, và thu `except (OSError, ValueError)` về `except OSError`.

## Lượt 2 phải xét gì

Bản vá mới (commit đơn `fc48421`) sửa cả ba, và **thêm một lời khai PHẠM VI tự đo được**:
trong container người vá, `claude mcp list` báo `Pending approval` TRONG KHI phiên agent vẫn
gọi `mcp__github__*` bình thường. Người vá lập luận rằng hai phép đo hỏi hai thứ khác nhau —
`mcp list` đọc trạng thái duyệt server `.mcp.json` cho dự án theo con mắt CLI, tức thứ mà một
tiến trình `claude` MỚI SINH sẽ gặp — và vì `launcher.py` sinh agent bằng CLI nên đó đúng là
câu hỏi cần. **Lập luận này là thứ đáng soi nhất của lượt này.**

Phải trả lời, mỗi câu kèm phép đo tái lập được:

1. **Lời khai phạm vi ấy ĐÚNG không?** Đo trong môi trường của bạn: `claude mcp list` nói gì,
   và phiên bạn có gọi được công cụ `mcp__github__*` không? Nếu hai thứ đó KHÔNG lệch nhau ở
   chỗ bạn thì nói **KHÔNG ĐO ĐƯỢC** cho vế đó — đừng suy ra từ container người vá. Và xét:
   nhãn `CHUA_XAC_THUC` gắn cho một thứ chỉ hỏng-với-agent-sắp-sinh có gây hiểu nhầm không,
   hay câu khai kèm theo đã đủ hẹp?
2. **`khoe` không lên `DUNG_DUOC` — đúng hay lười?** Người vá giữ `Connected` ở
   `KHONG_DO_DUOC` với lý do "CLI nối được không chứng minh PHIÊN gọi được". Đây là chính lớp
   lập luận mà P1 lượt 1 đã bác một lần. Xét lại: còn bằng chứng nào từ tiến trình con nâng
   được nhãn này không? Nếu có thì đó là finding, cùng hạng P1 với lượt trước.
3. **Ba bản vá có đúng và có kín không?** Khớp tên chính xác (`casefold() == "github"`) — có
   chặn oan tên hợp lệ nào không? Kiểm kiểu ở gốc và ở bảng server — còn hình dạng sai lược đồ
   nào lọt (`{"servers": ...}` sai kiểu, giá trị `null`, khoá `github` với giá trị không phải
   object)? Phân ba nhánh của `_suc_khoe_mcp_github` — dòng CLI ở phiên bản khác có làm nó đọc
   nhầm không?
4. **`gh` còn lật được nhãn ở đường nào không** — `_do_github_api` VÀ tầng tiêu thụ
   (`ok_kha_dung`, `--doi-kha-dung`, `chua_chung_minh`). Câu này giữ nguyên từ lượt 1 vì nó là
   lớp lỗi P1 của lượt trước nữa; đừng bỏ qua chỉ vì lượt 1 đã hỏi.
5. **Bộ test.** Chạy `python3 .claude/dev/launcher_test.py` (đặt `TMPDIR` ghi được nếu sandbox
   cần). Nền đo lại cùng lúc, cùng máy — **và nền đã ĐỔI so với lease lượt 1**: cờ chặn
   `~/.codex/tra-luat-CHAN-CODEX` nay không còn, nên bốn ca `t85 t93 t94 t96` hết đỏ.
   `master e38b0be` = **104/104**, nhánh này = **105/105**. Đòi delta = 0 ca đỏ.

   Rồi **tự nghĩ ít nhất HAI đột biến** trên **bản sao tạm** và cho biết có bị bắt không.
   Người vá đã chạy mười một, `t105` bắt hết (`M1`…`M11`, xem thông điệp commit) — trong đó
   `M1`/`M2` chính là hai đột biến bạn báo sống sót ở lượt 1. Việc của bạn là tìm đột biến
   người vá KHÔNG nghĩ tới. Ưu tiên hướng: ca đo MÁY thay vì đo HỢP ĐỒNG (lượt trước đã có
   một ca như thế — `t105` ban đầu chỉ giả `subprocess.run` chứ không giả `shutil.which`, nên
   trên máy không có `gh` thì nhánh ấy không chạy).
6. **Bộ chạy đột biến có tự lừa được không?** Nó ở
   `scratchpad/dotbien_mcp.sh` — NGOÀI kho, nên bạn chỉ xét được phần được mô tả trong thông
   điệp commit. Người vá khai rằng nó từ chối chấm điểm khi mẫu `sed` không còn khớp (in
   `DOT BIEN KHONG DOI GI — BO`). Xét lời khai ấy có che được lỗ nào không.

## Ngoài phạm vi (đã biết, đừng báo lại)

- `.github/workflows/**` dùng `gh` — đúng, runner GitHub không có MCP.
- `.claude/skills/**` và `docs/**` còn lệnh `gh`; lệch với "mọi việc GitHub đi bằng MCP"
  nhưng ngoài phạm vi lượt này.

## Định dạng trả lời — in ra stdout, không ghi tệp

    verdict: approve | changes_requested | do_not_land
    reviewed_sha: <sha>
    ## Findings   (id kebab, mức P1/P2/P3, mô tả, lệnh tái lập, kết quả đo được)
    ## Phép đo đã chạy

Cái gì không đo được thì nói **KHÔNG ĐO ĐƯỢC**. Đừng đoán.
