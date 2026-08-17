# Prompt review — `doctor`: đo GitHub theo đúng đường MCP

Bạn là REVIEWER, provider `codex`. Người vá là `claude` (§8 cross-provider). CHỈ ĐỌC.

## Bối cảnh — chủ kho chốt

Mọi việc GitHub của kho này đi bằng **MCP**. `.github/workflows/**` dùng `gh` là ngoại lệ
đúng (runner GitHub không có MCP), còn ở phía dev thì đường là MCP.

## Bản vá làm gì

`_do_github` cũ đo hai đường (`git ls-remote`, `gh auth status`) và cho **bất kỳ** đường nào
OK là `DUNG_DUOC` — trong khi MCP không nằm trong phép đo nào, và `launcher.py` chưa từng đọc
`.mcp.json`. Bản vá tách làm hai mục (`git-day-keo`, `github-api`), hạ `gh` xuống thông tin,
thêm trạng thái thứ ba `KHONG_DO_DUOC`, và đọc `.mcp.json`.

## Phải trả lời, mỗi câu kèm phép đo tái lập được

1. **Hợp đồng mới có khai đúng phạm vi đo được không?** `KHONG_DO_DUOC` có thật sự là câu
   trả lời trung thực, hay còn cách đo MCP nào từ tiến trình con mà tôi bỏ sót? Nếu có thì
   nêu — đó là finding.
2. **`gh` còn lật được nhãn ở đường nào không?** Đọc kỹ `_do_github_api`. Và kiểm tầng tiêu
   thụ: `ok_kha_dung`, `--doi-kha-dung`, `chua_chung_minh` — có chỗ nào nâng nhãn lại không
   (đây đúng lớp lỗi P1 `co-credential-van-duoc-coi-la-kha-dung` của lượt trước).
3. **Đọc `.mcp.json` có chỗ nào sai không?** khoá `mcpServers` vs `servers`; tên server viết
   hoa/thường; tệp hỏng; `ws=None` lùi về gốc launcher — lời khai có nêu đủ gốc đã đọc không?
4. **Tách hai mục có làm hỏng gì không** — `KHA_NANG`, chỗ in, mã thoát, JSON.
5. **Bộ test có khoá đủ không?** Chạy `python3 .claude/dev/launcher_test.py`. Nền master lúc
   cấp lease: 100/104, bốn ca đỏ `t85` `t93` `t94` `t96` — **đỏ sẵn**, do cờ chặn codex
   `~/.codex/tra-luat-CHAN-CODEX`, không phải do bản vá. Đòi delta = 0.
   Rồi **tự nghĩ ít nhất HAI đột biến** trên **bản sao tạm** và cho biết có bị bắt không.
   Người vá đã thử bốn (cho `gh` lật nhãn lại · chưa khai → `KHONG_DO_DUOC` · đã khai →
   `DUNG_DUOC` · bỏ phần khai nguồn gốc); cả bốn bị `t105` bắt, nhưng cái thứ nhất **từng
   sống sót** khi ca chỉ giả `subprocess.run` mà không giả `shutil.which` — ca đo MÁY chứ
   không đo HỢP ĐỒNG. Soi xem còn ca nào mắc đúng bệnh ấy.

## Định dạng trả lời — in ra stdout, không ghi tệp

    verdict: approve | changes_requested | do_not_land
    reviewed_sha: <sha>
    ## Findings   (id kebab, mức P1/P2/P3, mô tả, lệnh tái lập, kết quả đo được)
    ## Phép đo đã chạy

Cái gì không đo được thì nói **KHÔNG ĐO ĐƯỢC**. Đừng đoán.
