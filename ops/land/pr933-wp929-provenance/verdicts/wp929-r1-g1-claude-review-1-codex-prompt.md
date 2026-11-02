# Cross-review packet wp929 (Issue #929, revision 1) — reviewer `codex`, lớp `sensitive`

Bạn là REVIEWER độc lập. Executor là phiên Claude Code. Đánh giá bản vá, KHÔNG sửa mã trong `cay-kho/`.

## Hiện vật (thư mục hiện tại)
- `SPEC.md` — đặc tả đóng băng, sha256 `79251bee45fc39003d13438d741c4e6319dc80ea6b480dc1b931c93d0c6a7ae6`. Đây là hợp đồng; đo bản vá theo nó.
- `diff.patch` — `git diff 5775864..8a6d795` (2 tệp; nhánh = 2 commit vá + 1 merge master không chạm write set).
- `cay-kho/` — clone đầy đủ (không nông), HEAD detached tại `8a6d795c982fc7e9da2fbfd28a75ca25d5f3eb95`,
  `origin/master` = `5775864b04a18c5afe1aafcbb23e54525ce8a3d8` (base lease cdc4e80 + 2 commit ops/land). Không có mạng.
  Thứ định danh mã là BĂM commit, không phải tên nhánh.

## Việc
1. Đọc `SPEC.md` (M1–M4, N1–N5) và `diff.patch`. Đọc `_che_do_0054` trong `cay-kho/.claude/dev/packet_loop.py`
   và phần `r929_*` / `r812_r7_activation_*` / `_kho812` trong `cay-kho/.claude/dev/packet_loop_test.py`.
2. Kiểm bản vá có đúng M1 không: liệt kê `docs/adr/` trên `origin/master` bằng `git ls-tree`, lọc `^docs/adr/[0-9]{4}-[^/]+\.md$`,
   trừ `ADR0054_TEP`, đọc từng tệp, NFC, đúng cụm `` kích hoạt `ADR-0054` ``, đúng MỘT tệp; 0 / ≥2 / lỗi git ⇒ False;
   các điều kiện khác của hàm giữ nguyên. M2: `ADR0055_TEP` đã bỏ, không hằng mới mang số ADR kích hoạt.
3. ĐO, đừng chỉ đọc. Làm việc trên BẢN SAO TẠM của `cay-kho` (vd `cp -a cay-kho tmp/k`), không sửa `cay-kho/`:
   - Chạy các ca đích: trong thư mục `.claude/dev` của bản sao, nạp `packet_loop_test.py` như module và gọi
     `chay_suite(Path("packet_loop.py").resolve(), Path(<thư mục tạm>), chi_chay={...})`; hoặc chạy cả suite
     `python3 -B .claude/dev/packet_loop_test.py` (dài, có phần tự chạy mọi đột biến của bảng `MUTANTS`).
   - Bốn đột biến M4 nằm trong bảng `MUTANTS` với tên `r929_*`; tự đột biến THÊM bản vá theo hướng bạn nghĩ có thể
     lọt (ví dụ: bỏ `all(rc == 0 ...)`, bỏ `ls[0] == 0`, bỏ NFC, đổi regex tên tệp) và xem ca nào đỏ. Đột biến nào
     SỐNG mà lẽ ra phải chết là finding (ghi rõ có đáng thêm ca không, cân với trần ≤ 300 dòng của spec).
   - Kiểm hành vi trên kho thật: `_che_do_0054` trên `cay-kho` hiện phải trả False (packet KHÔNG kích hoạt ADR-0054).
4. Câu hỏi cần trả lời rõ: (i) có đường nào cho `True` sai (fail-open) không; (ii) ca (a)–(e) có đo đúng thứ chúng
   khai không (ca có MẶT khác ca có ĐO); (iii) có hồi quy cho ca `r812_*` khác không; (iv) diff có ra ngoài write set
   hay vượt phạm vi M1–M4 không.
   Hướng nào cần dựng nội dung nhạy cảm (đường dẫn thoát cây, symlink độc…) thì MÔ TẢ BẰNG LỜI, đừng tự soạn.

## Đầu ra
Ghi `VERDICT.md` trong thư mục hiện tại NGAY TỪ ĐẦU và cập nhật dần (lượt có thể bị cắt). Dạng:

```
Verdict: approve | request_changes
Reviewed commit: 8a6d795c982fc7e9da2fbfd28a75ca25d5f3eb95
Spec sha256: 79251bee45fc39003d13438d741c4e6319dc80ea6b480dc1b931c93d0c6a7ae6
## Findings
- [P0|P1|P2|P3] <id>: <mô tả> · lệnh · output · kết luận
## Phép đo đã chạy
- lệnh · output tóm tắt · kết luận
```
`approve` chỉ khi không có P0/P1/P2. Mỗi finding phải có lệnh + output tái hiện được. Dòng cuối stdout của bạn:
`XONG VERDICT sha256=<sha256 của VERDICT.md>`.
