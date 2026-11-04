# Cross-review packet wp929 (Issue #929, revision 1) — lượt 3, exact-SHA trên head merge — reviewer `codex`, lớp `sensitive`

Bạn là REVIEWER độc lập. Executor là phiên Claude Code. Đánh giá bản vá, KHÔNG sửa mã trong `cay-kho/`.
Trần lời gọi đã được chủ kho nâng 2 → 3 (#929 issuecomment-6448100522). Đây là lời gọi CUỐI.

## Vì sao có lượt này
Lượt 2 approve neo `227dcde`. PR #933 được merge với head `f3b54d2` = `227dcde` + merge `origin/master` `36057e8`
(chủ kho chỉ thị "xử lý head drift"). Protocol: head đổi thì review cũ stale. Lượt này review ĐÚNG `f3b54d2`.

## Hiện vật (thư mục hiện tại)
- `SPEC.md` — đặc tả đóng băng, sha256 `79251bee45fc39003d13438d741c4e6319dc80ea6b480dc1b931c93d0c6a7ae6`.
- `VERDICT-luot1.md` (neo `8a6d795`, request_changes) và `VERDICT-luot2.md` (neo `227dcde`, approve, một P3 mở).
- `diff.patch` — `git diff 36057e8..f3b54d2` (merge-base → head merge; đúng nội dung PR #933 vào master).
- `windows-gate-packet-loop-40476173630.log` — log job `gate-packet-loop (windows-latest)` của run `ci.yml`
  `workflow_dispatch` trên merge `ab94c4f` (sau khi PR #933 merge): `nền: 871/872`, đỏ `r929_show_loi_la_false`
  (`PermissionError [WinError 5]` khi xoá loose object). Ubuntu cùng run xanh.
- `cay-kho/` — clone đầy đủ (không nông), HEAD detached tại `f3b54d260bcdecf5b6d2348730a958e168bf7330`;
  `refs/remotes/origin/master` được GHIM vào merge-base `36057e8292bcb3b27ceb64b461d7cf29057a8ba3` để diff nhất quán.
  Không có mạng. Thứ định danh mã là BĂM commit.

## Việc
1. Xác minh head: `git -C cay-kho rev-parse HEAD` = `f3b54d2…`; hai tệp write set ở `f3b54d2` giống từng byte `227dcde`
   (`git diff --stat 227dcde f3b54d2 -- .claude/dev/packet_loop.py .claude/dev/packet_loop_test.py` rỗng); phần
   merge từ `36057e8` không chạm write set.
2. Review lại bản vá trên chính `f3b54d2` theo SPEC (M1–M4) — đừng chỉ nhận lời lượt 2: chạy các ca `r929_*`,
   `r812_r7_activation_*`, `r812_khong_kich_hoat_la_false` bằng `chay_suite(..., chi_chay={...})` trên BẢN SAO TẠM
   (`cp -a cay-kho tmp/k`), và đột biến `r929_*` trong bảng `MUTANTS`. Nếu sandbox ký commit làm fixture lỗi, cô lập
   bằng `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.
3. Đánh giá hồi quy Windows trong log: xác nhận nguyên nhân từ mã ca `r929_show_loi_la_false`, xếp hạng (P0–P3) và
   nêu bản vá tối thiểu. Đây là lỗi của chính PR này; xếp hạng theo tác động thật lên gate, không theo nơi phát hiện.
4. Kho thật trong `cay-kho` vẫn không kích hoạt ADR-0054.
   Hướng nào cần dựng nội dung nhạy cảm (đường dẫn thoát cây…) thì MÔ TẢ BẰNG LỜI, đừng tự soạn.

## Đầu ra
Ghi `VERDICT.md` trong thư mục hiện tại NGAY TỪ ĐẦU và cập nhật dần. Dạng:

```
Verdict: approve | request_changes
Reviewed commit: f3b54d260bcdecf5b6d2348730a958e168bf7330
Spec sha256: 79251bee45fc39003d13438d741c4e6319dc80ea6b480dc1b931c93d0c6a7ae6
## Trạng thái finding lượt trước
## Findings mới
- [P0|P1|P2|P3] <id>: <mô tả> · lệnh · output · kết luận
## Phép đo đã chạy
```
`approve` chỉ khi không có P0/P1/P2 còn mở. Mỗi finding phải có lệnh + output tái hiện được. Dòng cuối stdout:
`XONG VERDICT sha256=<sha256 của VERDICT.md>`.
