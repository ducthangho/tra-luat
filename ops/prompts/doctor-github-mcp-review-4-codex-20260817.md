# Prompt review lượt 4 — `doctor`: đo GitHub theo đúng đường MCP

Bạn là REVIEWER, provider `codex`. Người vá là `claude` (§8 cross-provider). CHỈ ĐỌC.

Nguồn có thẩm quyền của lượt này là TỆP CÓ BĂM trong kho (lease + prompt này). Comment
trên #55 chỉ là bản chiếu.

## Ba lượt trước

| lượt | SHA | verdict | finding | đột biến bạn báo sống sót |
|---|---|---|---|---|
| 1 | `4ff2c6bf` | changes_requested | 1×P1, 2×P2 | 2 |
| 2 | `fc484213` | changes_requested | 2×P2 | 2 |
| 3 | `109c4278` | changes_requested | 3×P2 | 3 |

**BA LƯỢT LIÊN TIẾP đều tìm được đột biến sống sót, và cả ba lần cùng một nguyên nhân:
`t105` đo ĐỒ GIẢ chứ không đo HỢP ĐỒNG.** Lượt 1: chỉ giả `run`, không giả `which`.
Lượt 2: đồ giả nuốt mọi kwargs. Lượt 3: `cmd[:3]`, không đếm số lần gọi, `timeout>0`.

Người vá kết luận nguyên nhân gốc KHÔNG phải ba chỗ thiếu, mà là **cách chốt**: mỗi lần
lại liệt kê những gì PHẢI ĐÚNG — tức một danh sách CẤM các cách sai. Lượt này đảo thành
danh sách CHO PHÉP (xem mục 1).

Tương tự ở bộ phân loại sức khoẻ: ba bản bổ dòng tóm tắt `claude mcp list` là ba kiểu
sai khác nhau. Đo thật (dựng server MCP trong HOME tạm) cho thấy dòng ấy KHÔNG THỂ bổ
đúng — phần trước dấu phân cách là CÂU LỆNH của server:

    broken: /nonexistent/binary  - × Failed to connect — ENOENT: ...

Nên chuyển sang `claude mcp get <tên>`, trả TRƯỜNG CÓ NHÃN `Status:`.

## Lượt 4 xét gì

Hai commit: `9d79e5f` (vá ba P2 của lượt 3) và `9683d91` (một lỗi người vá TỰ tìm ra).

1. **CHỖ ĐÁNG NGHI NHẤT — chốt "danh sách cho phép" của đồ giả.** Đồ giả nay ghi nhật ký
   mọi lời gọi; `doi_goi_claude_dung_dac_ta` đòi nhật ký lời gọi `claude` **BẰNG ĐÚNG**
   `[(("claude","mcp","get",<tên>), {capture_output:True, text:True, timeout:30})]`.
   Ba lượt bạn đều thắng ở lớp này — **tìm lượt thứ tư**. Hướng đáng thử:
   - Chốt chỉ lọc lời gọi có `cmd[0] == "claude"`. Một bản vá gọi `["/usr/bin/claude",…]`
     hoặc `["npx","claude",…]` thì sao?
   - Nó được gọi ở NHỮNG ĐIỂM NÀO? Có nhánh nào của `_do_github_api` chạy mà không ai
     kiểm nhật ký không (ví dụ các ca `(3c)`, `(3c2)`, `(4b)`, `(4c)` gọi `_do_github_api`
     nhưng không gọi `doi_goi_claude_dung_dac_ta`)? Nếu có, một đột biến chỉ sai TRONG
     những nhánh ấy sẽ sống.
   - `nhat_ky.clear()` nằm trong chốt — bỏ chốt đi thì rác tích lại có làm ca sau đỏ oan
     hay xanh oan không?
   - Lời gọi `gh` KHÔNG bị đặc tả nào ràng buộc. Che được gì?

2. **`_suc_khoe_mcp_github` sau khi đổi sang trường có nhãn.**
   - `_RE_STATUS` là `^\s*Status:\s*(.+?)\s*$` với `re.MULTILINE` và dùng `.search` —
     nó lấy dòng `Status:` **ĐẦU TIÊN**. Đầu ra `mcp get` còn có dòng `Issue:`; có đường
     nào để một dòng khác chen lên trước, hoặc để nội dung do máy chủ/người dùng kiểm
     soát tự tạo ra một dòng `Status:` giả không?
   - `_MCP_KHOE` khớp BẰNG ĐÚNG, `_MCP_HONG` khớp TIỀN TỐ. Bất đối xứng ấy có chỗ nào
     hở? `_RE_TRANG_TRI = ^[^0-9a-z]+` cắt ký hiệu đầu — nó cắt cả gì khác?
   - Mặc định là `khong_do_duoc`. Kiểm ở TẦNG TIÊU THỤ rằng đó là fail-close.

3. **Lỗi người vá tự tìm (`9683d91`) — xét cả bản vá LẪN cách nó được tìm ra.**
   `claude mcp get` phân biệt hoa/thường trong khi `.mcp.json` khớp `casefold()`, nên
   dùng sẵn chuỗi `"github"` làm một khai báo hợp lệ (`GitHub`) bị báo là không đo được.
   Kèm theo: **CLI trả `rc=0` khi KHÔNG tìm thấy server** (`No MCP server named ...`).
   - Bản vá truyền `ten[0]` — khi `.mcp.json` khai NHIỀU tên khớp (`github` và `GitHub`
     cùng lúc) thì `ten[0]` phụ thuộc thứ tự khoá trong JSON. Đó có phải hành vi đúng,
     hay là một chỗ bất định?
   - Còn đường nào khác mà `rc=0` của CLI này nói dối không?

4. **`_doc_mcp_json` nay trả BA giá trị.** Mọi nhánh `return` có trả đủ ba không, và
   nhánh nào trả tên `None` mà lẽ ra phải có tên?

5. **`gh` còn lật được nhãn không** — `_do_github_api` VÀ tầng tiêu thụ. Giữ từ ba lượt
   trước; đừng bỏ vì đã hỏi ba lần.

6. **Số nền.** Chạy và tự đo:
   ```
   TMPDIR=/dev/shm python3 .claude/dev/launcher_test.py
   TMPDIR=/dev/shm python3 .claude/dev/launcher_test.py --dot-bien
   ```
   Người vá đo cùng lúc, cùng máy: suite master `e38b0be` **104/104**, nhánh **105/105**;
   đột biến master **61/61**, nhánh **79/79**. Đòi delta = 0 ca đỏ.

   Lượt 2 và lượt 3 gặp sandbox cắt tiến trình ở nhóm ca thao tác cây tiến trình. Nếu
   lượt này cũng vậy thì nói **KHÔNG ĐO ĐƯỢC** cho số tổng và chạy riêng bằng `--lap-ca`.

   Rồi **tự nghĩ ít nhất HAI đột biến** trên **bản sao tạm**, ưu tiên mục 1.

## Ngoài phạm vi (đã biết, đừng báo lại)

- `.github/workflows/**` dùng `gh` — đúng, runner GitHub không có MCP.
- `.claude/skills/**` và `docs/**` còn lệnh `gh` — ngoài phạm vi lượt này.
- Lời khai phạm vi của nhãn `CHUA_XAC_THUC` (agent sắp sinh vs phiên đang chạy) — lượt 2
  đã đo độc lập và xác nhận. Chỉ báo lại nếu có phép đo NGƯỢC LẠI.
- Ba điều lượt 3 đã xác nhận là ĐÚNG: `gh` không lật được nhãn; đột biến chết bằng
  `JSONDecodeError`/`AttributeError`/`TypeError` là oracle hợp lệ; đường tiêu thụ
  fail-close (rc=13). Chỉ báo lại nếu bản vá mới làm hỏng một trong ba.

## Định dạng trả lời — in ra stdout, không ghi tệp

    verdict: approve | changes_requested | do_not_land
    reviewed_sha: <sha>
    ## Findings   (id kebab, mức P1/P2/P3, mô tả, lệnh tái lập, kết quả đo được)
    ## Phép đo đã chạy

Cái gì không đo được thì nói **KHÔNG ĐO ĐƯỢC**. Đừng đoán.
