# Prompt review lượt 5 — `doctor`: đo GitHub theo đúng đường MCP

Bạn là REVIEWER, provider `codex`. Người vá là `claude` (§8 cross-provider). CHỈ ĐỌC.

Nguồn có thẩm quyền của lượt này là TỆP CÓ BĂM trong kho (lease + prompt này). Comment
trên #55 chỉ là bản chiếu.

## Bốn lượt trước

| lượt | SHA | verdict | finding | đột biến bạn báo sống sót |
|---|---|---|---|---|
| 1 | `4ff2c6bf` | changes_requested | 1×P1, 2×P2 | 2 |
| 2 | `fc484213` | changes_requested | 2×P2 | 2 |
| 3 | `109c4278` | changes_requested | 3×P2 | 3 |
| 4 | `9683d916` | changes_requested | 2×P2 | 2 (+1 báo sống sót nhưng thực ra TƯƠNG ĐƯƠNG) |

**BỐN lượt liên tiếp bạn đều tìm được đột biến sống sót, và cả bốn lần cùng một lớp:
`t105` đo ĐỒ GIẢ chứ không đo HỢP ĐỒNG.** Lượt 4 bạn nêu đúng nguyên nhân — oracle mới
đặc tả một TẬP CON lời gọi. Người vá đã sửa ở TẦNG (xem mục 1); lượt này là phép thử
xem cách sửa ấy có thật sự đóng được cả lớp hay không.

## Lượt 5 xét gì

Hai commit: `a1d47a0` (vá hai P2 của lượt 4) và `bf24fe4` (đóng mục lượt 4 khai KHÔNG
ĐO ĐƯỢC).

1. **CHỖ ĐÁNG NGHI NHẤT — chốt đồ giả nay là TOÀN PHẦN, đúng hay chỉ trông có vẻ?**
   Hai thay đổi:
   - `gia_run` **tự từ chối** mọi lời gọi không khớp đặc tả (`bang(goi in cho_phep, …)`),
     nên mọi lời gọi đều bị soi kể cả ở nhánh chưa ai viết ca.
   - `goi_api()` là **đường duy nhất** gọi `_do_github_api` trong `t105` (14 chỗ), và nó
     đếm số lời gọi `claude`.

   **Tìm lượt thứ NĂM.** Hướng đáng thử:
   - `goi_api` lọc lời gọi `claude` bằng `"claude" in " ".join(g[0])` — một lệnh có chữ
     `claude` ở chỗ khác (đường dẫn, đối số) có làm sai số đếm không?
   - Đặc tả `cho_phep` được dựng lại mỗi lời gọi từ `GOI_MONG_DOI()` đọc `ten_mong_doi[0]`
     — có ca nào để `ten_mong_doi` sai giá trị rồi đặc tả tự nới theo không?
   - `bang()` gọi TRONG đồ giả: nó ném `AssertionError` từ bên trong mã đang thử. Có
     đường nào để `_do_github_api` NUỐT ngoại lệ ấy (`except Exception`) làm chốt câm không?
   - Còn hàm nào của module gọi `subprocess` mà `t105` không phủ, hoặc ca nào KHÁC `t105`
     dùng `_do_github_api` mà không qua `goi_api`?

2. **Mục lượt 4 khai KHÔNG ĐO ĐƯỢC nay đã đo — kiểm lại kết luận.** Đo được: nội dung do
   `.mcp.json` kiểm soát **CHÈN ĐƯỢC** một dòng `Status:` thứ hai (`grep -c "Status:"` = 2),
   nhưng nó nằm SAU bản thật nên `.search` (khớp đầu tiên) đọc đúng. Lập luận chống lưng:
   CLI in `Status` trước mọi trường có giá trị do người dùng đặt, và thứ in trước nó
   (tên server, `Scope:`) thì tên phải casefold ra `github` nên không chứa được xuống dòng.
   - Lập luận ấy có lỗ nào không? Có trường nào do người dùng kiểm soát in TRƯỚC `Status`
     mà người vá bỏ sót (scope khác, transport khác — `sse`, `http` có `Headers`)?
   - **Tên server có thật sự không chứa được xuống dòng không?** JSON cho phép `"\n"`
     trong khoá; điều chặn là `casefold() == "github"`. Kiểm lại chốt ấy.
   - Fixture trong test chép lại hình dạng đo được — nó có TRUNG THỰC với đầu ra thật không?

3. **Chốt mơ-hồ (nhiều tên khớp casefold ⇒ từ chối).** Có chặn oan cấu hình hợp lệ nào
   không? Và người vá khai rằng đột biến `ten[0]` → `ten[-1]` của bạn là **TƯƠNG ĐƯƠNG**
   (đo trên 4 cấu hình, 0 ca lệch) chứ không phải sống sót. **Kiểm lại lời khai đó** — nếu
   nó sai thì đây là finding, và là loại nặng: người vá bác một finding của reviewer.

4. **`gh` còn lật được nhãn không** — `_do_github_api` VÀ tầng tiêu thụ. Giữ từ bốn lượt
   trước; đừng bỏ vì đã hỏi bốn lần.

5. **Số nền.** Chạy và tự đo:
   ```
   TMPDIR=/dev/shm python3 .claude/dev/launcher_test.py
   TMPDIR=/dev/shm python3 .claude/dev/launcher_test.py --dot-bien
   ```
   Người vá đo cùng lúc, cùng máy: suite master `e38b0be` **104/104**, nhánh **105/105**;
   đột biến master **61/61**, nhánh **83/83**. Đòi delta = 0 ca đỏ.

   Lượt 2 và 3 bị sandbox cắt tiến trình ở nhóm ca thao tác cây tiến trình; lượt 4 chạy
   trọn. Nếu lượt này bị cắt thì nói **KHÔNG ĐO ĐƯỢC** cho số tổng và chạy riêng bằng
   `--lap-ca` — đừng suy ra từ số trên.

   Rồi **tự nghĩ ít nhất HAI đột biến** trên **bản sao tạm**, ưu tiên mục 1.

6. **Câu hỏi TỔNG cho lượt này — trả lời thẳng.** Bốn lượt liền có đột biến sống sót cùng
   lớp. Nếu lượt này bạn KHÔNG tìm được nữa, hãy nói rõ đó là vì chốt đã đóng được lớp ấy,
   hay chỉ vì bạn hết hướng tấn công. Hai điều đó khác nhau, và người vá cần biết mình
   đang ở điều nào. Nếu bạn TÌM ĐƯỢC, hãy nói thêm: nó lọt qua vì chốt thiếu một điều
   kiện, hay vì cách chốt (đặc tả lời gọi ở tầng đồ giả) sai từ gốc?

## Ngoài phạm vi (đã biết, đừng báo lại)

- `.github/workflows/**` dùng `gh` — đúng, runner GitHub không có MCP.
- `.claude/skills/**` và `docs/**` còn lệnh `gh` — ngoài phạm vi lượt này.
- Lời khai phạm vi của nhãn `CHUA_XAC_THUC` (agent sắp sinh vs phiên đang chạy) — lượt 2
  đã đo độc lập và xác nhận.
- Ba điều lượt 3 xác nhận đúng và lượt 4 xác nhận lại: `gh` không lật được nhãn; đột biến
  chết bằng `JSONDecodeError`/`AttributeError`/`TypeError` là oracle hợp lệ; đường tiêu thụ
  fail-close (rc=13). Chỉ báo lại nếu bản vá mới làm hỏng một trong ba.

## Định dạng trả lời — in ra stdout, không ghi tệp

    verdict: approve | changes_requested | do_not_land
    reviewed_sha: <sha>
    ## Findings   (id kebab, mức P1/P2/P3, mô tả, lệnh tái lập, kết quả đo được)
    ## Phép đo đã chạy

Cái gì không đo được thì nói **KHÔNG ĐO ĐƯỢC**. Đừng đoán.
