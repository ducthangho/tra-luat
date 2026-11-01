# Cross-review PR #1091 — ops/vm: -DangKyLich lần hai chết vì icacls /T để tệp với DACL rỗng — reviewer: codex

## Đối tượng
- `reviewed_sha`: `d58d649ff061ff125bc004414ed4a0787de8e5f3` (nhánh `ccr-5249948c-9epnbs`, PR #1091). Cây đầy đủ, KHÔNG shallow, ở `cay-kho/` (HEAD detached, `core.abbrev=7`); `origin/master` = `90c101b`.
- Diff so master: `diff.patch` (`numstat.txt`): CHỈ `ops/vm/cap-nhat-cong-cu.ps1` (+8/-1) và `ops/vm/cap-nhat-cong-cu_test.ps1`. Mã nền (`ops/vm/` ở master `90c101b`) đã qua 20 lượt cross-review của
  PR #1065/#1069; lượt 16 approve trên `210ab81` — verdict ở `verdict-luot16.md` để bạn biết các hợp đồng đã chốt.
- Sự cố (đo trên VM Windows Server 2022 thật, 31-10-2026): chạy lại `-DangKyLich` khi thư mục cài đặt đã có tệp ⇒ rc=6 "Access to the path …requirements.txt is denied".
  Tái hiện trên thư mục thử: `icacls <dir> /inheritance:r /grant:r <SID>:(OI)(CI)… /T /C /L /Q` trả rc=0 nhưng tệp con có DACL RỖNG.
- Vá: ACL đặt cho riêng thư mục (bỏ `/T`), rồi `icacls "<dir>\*" /reset /T /C /L /Q` khi thư mục có con. Đồ giả icacls trong test mô phỏng hành vi đo được
  (ACE (OI)/(CI) không áp lên tệp; /reset thừa kế từ cha; ghi đè tệp DACL rỗng bị từ chối) + ca `dk_chay_dang_ky_lai_tren_ban_cai_cu`.
- Executor khai: Linux 116/116, VM Windows 72/72; đột biến trả /T không reset ⇒ đỏ 2 ca, bỏ reset ⇒ đỏ 1 ca. Chạy THẬT trên VM (1/11): `-DangKyLich` rc=0 từ head `cb39aca`
  (cùng ops/vm với head này), bản cài khớp băm, ACL tệp `Users:(I)(RX) Administrators:(I)(F) SYSTEM:(I)(F)`, tác vụ NguoiDung LastTaskResult=0, 11/11 giu. (Thuật lại — reviewer không đo được.)

## Nhiệm vụ
1. Bản vá có đúng và đủ không: còn đường nào để tệp/thư mục con trong thư mục cài đặt kết thúc với ACL sai (thư mục con lồng, tệp ẩn, tệp đang bị khoá, wildcard `*` của icacls
   bỏ sót gì, `Get-ChildItem -Force` đếm khác icacls)? `/reset` có thể mở quyền ghi cho tài khoản thường không (thừa kế từ đâu)? Thứ tự setowner → ACL thư mục → reset → chép → setowner → đo lại.
2. Đồ giả mới có răng thật hay diễn kịch bản (mô hình có khớp hành vi đo trên VM; có ca nào xanh nhờ đồ giả)? Đột biến trên BẢN SAO.
3. Chạy `pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1` (`TL_TEST_PYTHON=python3`), ghi N/M.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` NGAY (dòng đầu `verdict: dang_lam`), nối thêm sau mỗi hướng. Cuối cùng dòng 1 `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: d58d649ff061ff125bc004414ed4a0787de8e5f3`,
một dòng `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.` Mỗi hướng: giả thuyết / lệnh / output / kết luận (LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC). Finding: `### <slug>  [P0|P1|P2|P3]` + TỆP/DÒNG, VẤN ĐỀ, ĐÃ THỬ NGHIỆM, ĐỘ TIN.
P0 = leo quyền / chạy mã chưa kiểm băm bằng SYSTEM. P1 = hành vi sai đo được. P2 = khai rộng hơn phép đo / thiếu điều kiện / test không răng. P3 = diễn đạt (không chặn approve).
"approve" không có output thật là không hợp lệ. Gợi ý vá (nếu có) vào `HINT.patch` (`patch -p0` từ gốc `cay-kho/`).

## Ràng buộc
CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/`, KHÔNG push, KHÔNG gọi mạng. Windows native (icacls/NTFS) KHÔNG đo được ở đây: phân tích tĩnh + ghi KHÔNG ĐO ĐƯỢC.
