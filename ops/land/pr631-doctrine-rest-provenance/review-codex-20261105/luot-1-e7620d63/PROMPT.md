# Review chéo độc lập — PR #631 (ducthangho/tra-luat), head `6e5c74849af68e748c4844bedf5856ead4c60be3`

Bạn là reviewer `openai_codex`, phiên mới, chỉ đọc. Executor và bốn lượt review trước đều là Claude, cùng họ. Lượt này
là lượt cross-provider đầu tiên mà chủ kho đòi ("vòng lặp codex tới hết P1/P2/P3", issuecomment-5826012645). PR đã merge
vào master (`0300cac`); kết quả của bạn quyết định hồ sơ land `ops/land/pr631-doctrine-rest-land-evidence.yaml` có được
nâng lên `landed: true` hay không.

## Vị trí
- Checkout kho: `./cay-kho` (HEAD tách rời tại đúng `6e5c748`). **KHÔNG sửa, tạo hay xoá tệp nào trong `./cay-kho`**
  (kể cả tệp tạm, `.pyc`, cache). Chạy Python với `-B` và `PYTHONDONTWRITEBYTECODE=1`. Mọi tệp bạn tạo đặt trong `./out/`
  hoặc thư mục tạm của hệ thống.
- Ref `origin/*` đã có sẵn trong checkout, không cần mạng.
- Phiên điều phối sẽ chụp snapshot toàn bộ cây `./cay-kho` (hash từng tệp, status, index) trước và sau lượt của bạn; lệch
  là lượt bị loại.

## Phạm vi review
Diff của PR: `git -C cay-kho diff 9091cf52cf20ac197c1a356d6a33cac6bab0b318 6e5c748` (merge-base với master lúc merge).
Gồm `CLAUDE.md` (+82 −4, hai chỗ trong các mục REST/GitHub) và 18 tệp biên nhận `ops/reviews/pr631-review-*/`.
Trọng tâm là `CLAUDE.md`. Các biên nhận chỉ cần kiểm có khớp với những gì `CLAUDE.md` trích từ chúng không.

Kiểm, theo thứ tự ưu tiên:
1. **Lời khai rộng hơn phép đo.** Mỗi câu khẳng định trạng thái (200/403, header, "đã trôi", "KHÔNG ĐO ĐƯỢC", số đếm,
   ngày giờ, run/comment id) phải có phạm vi (phiên nào, đường nào) và neo được. Câu nào khái quát từ một phiên thành
   trạng thái chung, hoặc gọi "đóng" thứ chỉ "thu hẹp", là finding.
2. **Neo trong kho.** Mọi đường dẫn tệp, tên hàm, tên ca test, mục doctor (`rest-kho`, `gh-kho`, `t103`, `t110`,
   `_do_github`, `_do_rest_github`, `CONG_CU`, `bat_buoc.remote`, khối "KHONG cai `gh`" trong `.claude/hooks/session-start.sh`,
   bảng trong `docs/GOI_AGENT_DA_NEN.md`, `ops/land/pr594-wp578-land-evidence.yaml`, `ops/leases/lease-dang-windows-*-20260822.yaml`…)
   mà diff nhắc tới phải tồn tại ở `6e5c748` và nói đúng điều diff gán cho nó. Đọc chính tệp, đừng đoán.
3. **Mâu thuẫn nội tại** giữa đoạn mới với phần còn lại của `CLAUDE.md` (cùng mục REST, mục "Đẩy ref", mục "GitHub: bốn
   đường", các bài học về "hỏi chỗ tiện tay", "có MẶT khác có ĐO"). Chỗ nào một câu cũ vẫn khẳng định điều mà đoạn mới
   bảo đã trôi, mà không có nhãn, là finding.
4. **Cổng hình thức**, chạy trong checkout bằng `python3 -B`:
   - `.claude/dev/packet_loop.py doctrine-scan --root .`
   - `.claude/dev/packet_loop.py adr-song --root .`
   - `scripts/tl.py doc-claims-check --json` (nếu đỏ, so với `9091cf5` để nói delta; ghi rõ nếu không chạy được).
   Ghi lệnh, rc và marker dương vào VERDICT.
5. **Chuỗi nhạy cảm**: không có chuỗi bỏ-qua-CI nguyên văn, không có `${{ }}` trong văn bản workflow, không có bí mật.

Không cần (và không được) gọi mạng để đo lại REST: phép đo REST nằm ngoài sandbox. Nếu một lời khai chỉ kiểm được
bằng mạng, ghi nó vào mục "KHÔNG ĐO ĐƯỢC" chứ không coi là finding, trừ khi chính văn bản tự mâu thuẫn.

## Thang mức
- P0: sai nghiêm trọng gây hành động phá hoại hoặc lộ bí mật.
- P1: lời khai sai/không neo được mà người đọc sẽ hành động theo (vd. kết luận một đường bị chặn/mở sai).
- P2: phạm vi khai rộng hơn phép đo, neo trỏ sai chỗ, mâu thuẫn với phần khác của tệp.
- P3: diễn đạt mơ hồ có thể đọc sai, lỗi chính tả làm đổi nghĩa.
Nit thuần tuý về văn phong thì không ghi.

## Đầu ra
Ghi DUY NHẤT tệp `./out/VERDICT.md`, mở đầu đúng ba dòng:
```
verdict: approve | changes_requested
reviewed_sha: 6e5c74849af68e748c4844bedf5856ead4c60be3
so_lop: P0 <n> / P1 <n> / P2 <n> / P3 <n>
```
`approve` chỉ khi P0 = P1 = P2 = P3 = 0. Sau đó: bảng finding (id, mức, tệp:dòng, trích nguyên văn, vì sao, cách sửa đề
xuất), mục "Đã kiểm" (từng neo ở mục 2 kèm kết quả), mục "Cổng" (lệnh/rc/marker), mục "KHÔNG ĐO ĐƯỢC", và một câu xác
nhận bạn không ghi gì vào `./cay-kho`.
