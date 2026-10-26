# Cross-review packet wp929 (Issue #929, revision 1) — lượt 2 (lời gọi Codex CUỐI, trần 2) — reviewer `codex`, lớp `sensitive`

Bạn là REVIEWER độc lập. Executor là phiên Claude Code. Đánh giá bản vá, KHÔNG sửa mã trong `cay-kho/`.

## Hiện vật (thư mục hiện tại)
- `SPEC.md` — đặc tả đóng băng, sha256 `79251bee45fc39003d13438d741c4e6319dc80ea6b480dc1b931c93d0c6a7ae6`. Hợp đồng; đo bản vá theo nó.
- `VERDICT-luot1.md` — verdict lượt 1 (sha256 `8a392561044c0ae6b9d504260149ff441fb8ec81cfe828fd8e06bd8f27c80bbf`), neo `8a6d795`:
  `request_changes`, một P2 (`wp929-tree-is-not-activation-file`) + ba P3.
- `diff-tu-luot1.patch` — `git diff 8a6d795..227dcde`: phần executor sửa sau lượt 1.
- `diff.patch` — `git diff 5775864..227dcde`: toàn bộ diff PR (2 tệp).
- `cay-kho/` — clone đầy đủ (không nông), HEAD detached tại `227dcdebc62c9275f9df09056f66e2124ed5f14c`,
  `origin/master` = `5775864b04a18c5afe1aafcbb23e54525ce8a3d8`. Không có mạng. Thứ định danh mã là BĂM commit.

## Executor khai đã làm (KIỂM, đừng nhận lời)
- P2: `_che_do_0054` đọc `ls-tree -z` đầy đủ, chỉ giữ mục `100644 blob` / `100755 blob` (loại tree, symlink 120000, gitlink).
- P3: thêm ca `r929_thu_muc_ten_md`, `r929_symlink_khong_tinh`, `r929_ba_chu_so_khong_tinh`, `r929_duoi_khac_md_khong_tinh`,
  `r929_nfd_van_tinh`, `r929_show_loi_la_false` và sáu đột biến `r929_bo_kiem_loai_doi_tuong`, `r929_nhan_symlink`,
  `r929_so_chu_so_tuy_y`, `r929_bo_duoi_md`, `r929_bo_nfc`, `r929_bo_rc_show`.
- P3 CHƯA phủ: chốt `ls[0] == 0` (lỗi `ls-tree`) — không bơm được lỗi đó qua đường `record-lease` thật mà không làm hỏng fixture
  trước chốt. Đánh giá xem đây có phải P2 không.

## Việc
1. Kiểm P2 đã đóng: tái chạy phép thử `tree`/thư mục đuôi `.md` của lượt 1 trên HEAD mới ⇒ phải False. Kiểm cả symlink và gitlink.
2. Kiểm bản vá mới không mở lỗ khác: phân tích dòng `ls-tree -z` (mode type oid TAB path); tên tệp chứa TAB/khoảng trắng/ký tự
   không ASCII; tệp `100755`; các điều kiện khác của hàm giữ nguyên; kho thật (`cay-kho`) vẫn False.
3. ĐO trên BẢN SAO TẠM (`cp -a cay-kho tmp/k`): chạy các ca `r929_*`/`r812_r7_activation_*`/`r812_khong_kich_hoat_la_false`
   bằng `chay_suite(..., chi_chay={...})` (nạp `packet_loop_test.py` như module từ `.claude/dev`); chạy các đột biến `r929_*`
   trong bảng `MUTANTS` và xem mỗi cái giết ĐÚNG ca đích tại khẳng định cuối; tự đột biến thêm theo hướng bạn nghĩ có thể lọt.
   Nếu sandbox ký commit (`commit.gpgsign`) làm fixture lỗi, cô lập bằng `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.
4. Write set: đúng 2 tệp `.claude/dev/packet_loop.py` (chỉ `_che_do_0054` + bỏ `ADR0055_TEP`) và `.claude/dev/packet_loop_test.py`;
   ≤ 300 dòng thêm.
   Hướng nào cần dựng nội dung nhạy cảm (đường dẫn thoát cây…) thì MÔ TẢ BẰNG LỜI, đừng tự soạn.

## Đầu ra
Ghi `VERDICT.md` trong thư mục hiện tại NGAY TỪ ĐẦU và cập nhật dần. Dạng:

```
Verdict: approve | request_changes
Reviewed commit: 227dcdebc62c9275f9df09056f66e2124ed5f14c
Spec sha256: 79251bee45fc39003d13438d741c4e6319dc80ea6b480dc1b931c93d0c6a7ae6
## Trạng thái finding lượt 1
- <id>: đóng | còn mở · bằng chứng
## Findings mới
- [P0|P1|P2|P3] <id>: <mô tả> · lệnh · output · kết luận
## Phép đo đã chạy
```
`approve` chỉ khi không có P0/P1/P2 còn mở. Mỗi finding phải có lệnh + output tái hiện được. Dòng cuối stdout của bạn:
`XONG VERDICT sha256=<sha256 của VERDICT.md>`.
