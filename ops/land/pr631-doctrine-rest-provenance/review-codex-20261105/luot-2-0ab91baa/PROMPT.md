# Review chéo độc lập lượt 2 — bản vá F1 của PR #631 (ducthangho/tra-luat), head `69f48261618a72b9058e88e875ad8de5d52a8860`

Bạn là reviewer `openai_codex`, phiên mới, chỉ đọc.

**Bối cảnh.** PR #631 (head `6e5c748`, đã merge `0300cac`) sửa mục REST trong `CLAUDE.md`. Lượt 1 cross-review Codex
(run `e7620d63`) cho `changes_requested`, đúng 1 finding:
- **F1 (P2):** các mốc giờ và độ phủ client của những lượt đo 30-09 do executor khai là `06:29Z` (hook),
  `06:30–06:31Z`, `06:31Z`, `07:10–07:11Z`, `07:11Z` và `07:51–07:57Z` (*"`curl` 10"*). Văn bản kể chúng như phép đo
  đã xác nhận, trong khi kho không có biên nhận gốc cho chúng.

Verdict lượt 1 nằm ở `./VERDICT-luot1.md`. Bản vá gồm hai commit chỉ sửa `CLAUDE.md`, là `a5fc816` và `69f4826`. Hai
commit gắn nhãn "lời khai chưa có biên nhận / KHÔNG ĐO ĐƯỢC" cho các mốc ấy, kể cả các mốc cùng lớp ở đoạn readback/MCP.
Commit `d96716c` nằm giữa hai commit trên và chỉ thêm hồ sơ land khác dưới `ops/land/pr1193-wp1189-*`, không thuộc phạm
vi review này.

## Vị trí
- Checkout: `./cay-kho` ở HEAD tách rời `69f4826`. **KHÔNG sửa, tạo hay xoá tệp nào trong `./cay-kho`.**
  Chạy Python với `-B`.
- Mọi tệp bạn tạo phải đặt trong `./out/`.
- Phiên điều phối sẽ chụp snapshot trước và sau.

## Phạm vi
`git -C cay-kho diff 07b773c 69f4826 -- CLAUDE.md`, khoảng +12 −7. Kiểm:
1. **F1 đã đóng chưa.** Mỗi mốc liệt kê ở lượt 1 phải không còn được kể như phép đo đã kiểm, ở **mọi** chỗ nó xuất hiện
   trong `CLAUDE.md`. Tìm khắp tệp, không chỉ trong diff. Gồm cả câu ở §Đẩy ref, mục REST trong §Gọi agent đa nền, và
   mọi đoạn khác chép lại các mốc này. Ví dụ đoạn readback/MCP gần đầu tệp có `2026-09-30T06:31–06:33Z` và
   `2026-09-30T06:31Z`.
   Mốc nào cùng lớp mà còn sót nhãn thì vẫn là F1 chưa đóng. Ghi rõ tệp:dòng.
2. **Bản vá có tạo lời khai mới rộng hơn phép đo không.** Ví dụ: nói "reviewer đo lại" mà biên nhận không ghi điều ấy;
   trỏ tới tệp hay dòng không nói đúng điều được gán; gọi "đóng" thứ chỉ "thu hẹp".
   Kiểm hai neo mới bằng cách đọc chính tệp: `ops/reviews/pr631-review-3-opus-max/VERDICT.md` và
   `ops/reviews/pr631-review-4-opus-max/VERDICT.md`.
3. **Mâu thuẫn mới** với phần còn lại của `CLAUDE.md`.
4. **Cổng hình thức** (`python3 -B`): `.claude/dev/packet_loop.py doctrine-scan --root .`, `.claude/dev/packet_loop.py adr-song --root .`,
   `scripts/tl.py doc-claims-check --json`. Ghi lệnh, rc và marker dương.
5. Không có chuỗi bỏ-qua-CI nguyên văn, không có cú pháp mở biểu thức Actions, không có bí mật trong phần thêm.

Không gọi mạng.

## Thang mức
- P0: phá hoại hoặc lộ bí mật.
- P1: lời khai sai mà người đọc sẽ hành động theo.
- P2: phạm vi khai rộng hơn phép đo, neo sai, hoặc mâu thuẫn.
- P3: mơ hồ dễ đọc sai.

Không ghi nit văn phong.

## Đầu ra
Ghi duy nhất `./out/VERDICT.md`, mở đầu đúng ba dòng:
```
verdict: approve | changes_requested
reviewed_sha: 69f48261618a72b9058e88e875ad8de5d52a8860
so_lop: P0 <n> / P1 <n> / P2 <n> / P3 <n>
```
`approve` chỉ khi P0 = P1 = P2 = P3 = 0.

Sau đó ghi các mục sau:
- trạng thái F1: đóng hoặc mở, kèm bằng chứng;
- bảng finding mới, nếu có;
- mục "Cổng";
- mục "KHÔNG ĐO ĐƯỢC";
- một câu xác nhận bạn không ghi gì vào `./cay-kho`.
