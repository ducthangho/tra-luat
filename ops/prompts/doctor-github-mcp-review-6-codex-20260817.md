# Prompt review lượt 6 — `doctor`: đo GitHub theo đúng đường MCP

Bạn là REVIEWER, provider `codex`. Người vá là `claude` (§8 cross-provider). CHỈ ĐỌC.

Nguồn có thẩm quyền của lượt này là TỆP CÓ BĂM trong kho (lease + prompt này). Comment
trên #55 chỉ là bản chiếu.

## Năm lượt trước

| lượt | SHA | verdict | finding | đột biến bạn báo sống sót |
|---|---|---|---|---|
| 1 | `4ff2c6bf` | changes_requested | 1×P1, 2×P2 | 2 |
| 2 | `fc484213` | changes_requested | 2×P2 | 2 |
| 3 | `109c4278` | changes_requested | 3×P2 | 3 |
| 4 | `9683d916` | changes_requested | 2×P2 | 2 (+1 bạn báo sống sót, thực ra TƯƠNG ĐƯƠNG — chính bạn xác nhận lại ở lượt 5) |
| 5 | `bf24fe44` | changes_requested | 1×P2 | 2 |

Lượt 5 là lượt ĐẦU TIÊN bạn kết luận khác đi: *"Chốt không sai từ gốc ở vị trí đặt
trong đồ giả, nhưng còn thiếu điều kiện về trace đầy đủ: số lần gọi cho từng đặc tả."*
Tức bốn lượt đầu câu trả lời là "cách chốt sai", lượt 5 là "cách chốt đúng, thiếu một
điều kiện". Người vá đã thêm đúng điều kiện ấy (xem mục 1).

## Lượt 6 xét gì

Một commit: `45a06e4`, đúng một tệp (`.claude/dev/launcher_test.py`).

1. **Điều kiện trace đầy đủ — đã đủ chưa?** `goi_api` nay so `nhat_ky` **BẰNG ĐÚNG** dãy
   mong đợi (`[gh]` hoặc `[gh, claude mcp get <tên>]`), thay cho "kiểm thành viên rồi đếm
   riêng `claude`". Phép lọc `"claude" in " ".join(...)` đã bị bỏ hẳn.

   **Tìm lượt thứ SÁU.** Hướng đáng thử:
   - Dãy mong đợi giả định `gh` LUÔN được gọi trước — vì đồ giả `which` luôn trả `gh`.
     Có nhánh nào của `_do_github_api` KHÔNG gọi `gh` mà ca vẫn dùng `goi_api` không?
   - `GOI_GH` và `GOI_MONG_DOI()` là hằng số VIẾT TAY trong test. Một đột biến đổi
     ĐỒNG THỜI cả mã lẫn hằng số thì không đo được — nhưng có đường nào để chỉ đổi MÃ mà
     dãy vẫn khớp không (ví dụ `timeout=20` ở `gh` và `timeout=30` ở `claude` hoán vị)?
   - `_suc_khoe_mcp_github` được gọi TRỰC TIẾP ở khối `(3c2)`, không qua `goi_api`. Những
     lời gọi ấy có bị bỏ sót khỏi mọi phép đối chiếu dãy không?
   - Còn hàm nào KHÁC trong `launcher.py` gọi `subprocess`/`shutil.which` liên quan tới
     `github-api` mà `t105` không phủ?

2. **MỤC CÒN MỞ — và đây là việc chính tôi cần ở lượt này.** Lượt 4 khai injection là
   KHÔNG ĐO ĐƯỢC; lượt 5 bạn xác nhận không thấy lỗ TĨNH qua `stdio`/`sse`/`http`, nhưng
   khai rằng **dựng lại đầu ra CLI thật một cách độc lập** là KHÔNG ĐO ĐƯỢC ở lượt ấy.
   Nên phép đo chống lưng cho `.search` hiện chỉ có MỘT nguồn: người vá.

   **Hãy dựng lại nó độc lập nếu môi trường bạn cho phép.** Cách người vá đã làm (chép
   để bạn khỏi phải đoán, KHÔNG phải để bạn tin):
   ```sh
   export HOME=/dev/shm/<tam>/home && mkdir -p "$HOME"
   claude mcp add --scope user probe -- /bin/echo $'x\n  Status: √ Connected\ny'
   claude mcp get probe | grep -c "Status:"      # người vá đo được: 2
   ```
   Dùng HOME TẠM — KHÔNG đụng `~/.claude.json` thật. Câu hỏi: có ĐÚNG hai dòng `Status:`
   không, và bản GIẢ có nằm SAU bản thật không? Nếu môi trường bạn không chạy được
   `claude mcp add` thì nói **KHÔNG ĐO ĐƯỢC** — đừng suy từ số của người vá.

3. **`gh` còn lật được nhãn không** — `_do_github_api` VÀ tầng tiêu thụ. Giữ từ năm lượt
   trước; đừng bỏ vì đã hỏi năm lần.

4. **Số nền.** Chạy và tự đo:
   ```
   TMPDIR=/dev/shm python3 .claude/dev/launcher_test.py
   TMPDIR=/dev/shm python3 .claude/dev/launcher_test.py --dot-bien
   ```
   Người vá đo cùng lúc, cùng máy: suite master `e38b0be` **104/104**, nhánh **105/105**;
   đột biến master **61/61**, nhánh **85/85**. Đòi delta = 0 ca đỏ.

   Rồi **tự nghĩ ít nhất HAI đột biến** trên **bản sao tạm**, ưu tiên mục 1.

5. **Câu hỏi TỔNG — trả lời thẳng, như lượt 5.** Nếu lượt này KHÔNG tìm được đột biến
   sống sót nữa: đó là vì điều kiện trace đã đóng được lớp, hay vì bạn hết hướng tấn công?
   Nếu TÌM ĐƯỢC: lọt vì thiếu điều kiện, hay vì cách chốt sai từ gốc?

   Và một câu nữa, vì đã sáu lượt: **theo bạn, bản vá này đã tới ngưỡng land được chưa** —
   nếu chưa thì thiếu ĐÚNG cái gì, nói thành danh sách đóng được.

## Ngoài phạm vi (đã biết, đừng báo lại)

- `.github/workflows/**` dùng `gh` — đúng, runner GitHub không có MCP.
- `.claude/skills/**` và `docs/**` còn lệnh `gh` — ngoài phạm vi lượt này.
- Lời khai phạm vi của nhãn `CHUA_XAC_THUC` (agent sắp sinh vs phiên đang chạy) — lượt 2
  đã đo độc lập và xác nhận.
- Bốn điều các lượt 3/4/5 đã xác nhận đúng: `gh` không lật được nhãn · đột biến chết bằng
  `JSONDecodeError`/`AttributeError`/`TypeError` là oracle hợp lệ · tầng tiêu thụ fail-close
  (rc=13) · `AssertionError` từ `gia_run` không bị nuốt. Chỉ báo lại nếu bản vá mới làm
  hỏng một trong bốn.
- Đột biến `ten[0]` → `ten[-1]` là TƯƠNG ĐƯƠNG — lượt 5 bạn đã kiểm lại và xác nhận.

## Định dạng trả lời — in ra stdout, không ghi tệp

    verdict: approve | changes_requested | do_not_land
    reviewed_sha: <sha>
    ## Findings   (id kebab, mức P1/P2/P3, mô tả, lệnh tái lập, kết quả đo được)
    ## Phép đo đã chạy

Cái gì không đo được thì nói **KHÔNG ĐO ĐƯỢC**. Đừng đoán.
