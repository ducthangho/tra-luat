# Cross-review lượt 16 — ops/vm/cap-nhat-cong-cu (PR #1065 đã merge; bản vá ở PR #1069) — reviewer: codex

## Đối tượng
- `reviewed_sha`: `210ab81c3f1af36243748458eb5e70180baeab71` (head nhánh `ccr-5249948c-9epnbs`, PR #1069).
- Lượt 1 (`b0814f4`), 2 (`aedd620`), 3 (`bbc3430`), 4 (`e5e2430`), 5 (`ea5ccd5`), 6 (`28fdbdf`), 7 (`00dd9d4`), 8 (`8e67b70`), 9 (`e218901`), 10 (`d005cf4`), 11 (`d20a69e`), 12 (`b667da8`), 13 (`e5838ff`), 14 (`f3231c8`), 15 (`c489c72`) đều `changes_requested`; verdict ở `luot1/`…`luot15/VERDICT.md`; HINT và probe lượt 4–15 của bạn ở `luot4/`…`luot15/` (`HINT.patch`, `probes/`) (đường dẫn trong probe trỏ `../cay-kho` — chạy lại từ đúng chỗ).
- Diff so với `b0814f4` (chỉ `ops/vm/`): `diff.patch`, `numstat.txt`; diff riêng của lượt vá 15 (từ `c489c72`): `diff-tu-luot15.patch`.
  PR #1069 còn chứa `ops/land/pr1065-*` — KHÔNG thuộc phạm vi review này.
- pwsh Linux 7.6.9 ở `pwsh/pwsh`. Executor khai: bộ test 115/115 Linux. Trên head lượt 14 (`c489c72`): 40/40 đột biến đỏ (danh sách đầy đủ: giữ nguyên các
  đột biến lượt trước + định danh số học, hậu cài số học HeThong/ZIP). Head này thêm đột biến bỏ chốt tag ⇒ đỏ đúng 2 ca. Head lượt 13 (`f3231c8`):
  71/71 VM Windows, CHẠY THẬT NguoiDung trên VM ⇒ 11/11 `giu`, rc=0. Head này trên VM: executor báo riêng. Head lượt 9 (`d005cf4`): 69/69 trên VM Windows, và CHẠY THẬT tầng NguoiDung trên VM (tlcommander)
  ⇒ 11/11 giu, rc=0 (npm view / pip index thật trên Windows). Head này: executor báo riêng.
- Hai hợp đồng chung (lượt 8 + 9) mà head này phải thoả — đây là thứ cần kiểm, không chỉ các ca đã liệt kê:
  (A) ChiKiem: một dòng chỉ được khác `loi` khi phiên bản ĐANG CÀI đo được (rc=0 + khớp mẫu).
  (B) Cài thật: dòng ĐẠT (`giu`/`nang_cap`/`cai_moi`) chỉ khi phiên bản SAU cài đo được (rc=0 + khớp mẫu) VÀ BẰNG ĐÍCH. Đích = ghim của bản kê
      (PyYAML/jsonschema/actionlint), hoặc bản mới nhất theo chính trình quản lý gói (`npm view <gói> version`, `pip index versions <gói>`, GitHub release,
      nodejs index) với rc=0. Venv kho: sau pip rc=0 phải đo được python và hai gói khớp ghim. Ngoại lệ có chủ ý, không tính lỗi:
      `can_quyet_dinh` (Node major mới), `can_khoi_dong_lai` (MSI 3010), `python` chỉ báo không nâng.
  Lượt vá 10: `giu` chỉ khi BẰNG đích; cao hơn bản phát hành mới nhất không ghim ⇒ `loi`. NLM: `nlm --version` phải bằng đích.
  Lượt vá 11: "bằng" = bằng ĐỊNH DANH ĐẦY ĐỦ. `ConvertTo-PhienBan` neo cả hai đầu (hậu tố prerelease/build ⇒ null ⇒ Compare null ⇒ không bao giờ `giu`);
  mọi mẫu phiên bản bắt cả hậu tố (`\S*`).
  Lượt vá 12: mọi phép so phiên bản chuỗi dùng `-cne`/`-ceq` (phân biệt hoa/thường). Test-CoTheCai: "đọc được" = ConvertTo-PhienBan khác null — có tệp mà
  phiên bản có hậu tố/không parse được ⇒ `loi`, KHÔNG cài (đóng hồi quy Node tự nâng major).
  Lượt vá 13: TÁCH hai quan hệ. **Bằng đích = Test-CungDinhDanh** (cùng chuỗi, phân biệt hoa/thường, chỉ bỏ tiền tố `v`) — dùng ở MỌI điểm chứng nhận
  (ZIP giu/hậu cài, HeThong giu/hậu cài; npm/pip/nlm/venv vốn so chuỗi `-cne`). **Compare-PhienBan chỉ dùng để SO THỨ TỰ** (cao hơn đích ⇒ `loi`; chọn major Node).
  Lượt vá 14 (CHỈ test): áp `luot14/HINT.patch`.
  Lượt vá 15: Update-CongCuZip có ghim mà `tag_name` trả về khác tag đã xin (theo Test-CungDinhDanh) ⇒ ném trước khi tải/chứng nhận. Executor tự viết chốt
  (một dòng, tương đương phần sản phẩm của `luot15/HINT.patch`; `$moi` vẫn lấy từ `tag_name` — sau chốt nó bằng ghim); phần test áp `luot15/HINT.patch` nguyên văn.

## Nhiệm vụ chính
1. **Đóng finding lượt 15 thật chưa** (đo, đừng nhận lời): `ghim-actionlint-khong-la-dich-chung-nhan` [P2]. Chạy lại `luot15/probes/pinned-release-round15.py`
   và probe lượt 4–15 trên BẢN SAO của head này. Rồi kiểm hai hợp đồng (A)(B) trên TOÀN
   `ops/vm/cap-nhat-cong-cu.ps1`: liệt kê MỌI lời gọi `Add-KetQua` không phải `loi` và cho mỗi cái một phép đo/lập luận nó thoả (A)/(B) hay không.
2. **Bản vá có tự mở lỗ mới không**: các try/catch mới (có nuốt lỗi lập trình, có biến lỗi thành ĐẠT/`bo_qua` không, `continue` trong try); ca test mới có răng thật hay đo đồ giả (đồ giả có diễn kịch bản không);
   ca nào có nhánh "không đo được thì bỏ qua" mà vẫn đếm ĐẠT.
3. **Đường thứ ba** còn lại ở toàn bộ `ops/vm/` tại head này chưa lượt nào chỉ (chỉ báo cái ĐO được hoặc phân tích tĩnh chắc chắn).
4. Chạy `pwsh/pwsh -NoProfile -File cay-kho/ops/vm/cap-nhat-cong-cu_test.ps1` (đặt `TL_TEST_PYTHON=python3`), ghi N/M.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, dòng 2 `reviewed_sha: 210ab81c3f1af36243748458eb5e70180baeab71`, và một dòng `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc:
```
verdict: ...
reviewed_sha: ...

## ĐÓNG FINDING LƯỢT 15
| slug | đã đóng? | phép đo (lệnh + output) |

## BẢNG SĂN   (>= 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT)
HƯỚNG n: <tên>
  giả thuyết : ...
  lệnh       : ...
  output     : ...
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC

### <slug-kebab>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ NGHIỆM: <lệnh + kết quả, hoặc KHÔNG ĐO ĐƯỢC + lý do>
ĐỘ TIN: cao/vừa/thấp
```
P0 = leo quyền / chạy mã chưa kiểm băm bằng SYSTEM. P1 = hành vi sai đo được tại head này. P2 = khai rộng hơn phép đo / thiếu điều kiện / ca test không có răng. P3 = diễn đạt.
"approve" không có output thật là không hợp lệ. P3 không chặn approve. Gợi ý vá (nếu có) vào `HINT.patch`, định dạng `patch -p0` từ gốc `cay-kho/`.

## Ràng buộc
Reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/`, KHÔNG push, KHÔNG gọi mạng.
Thứ cần Windows thật (NTFS junction, icacls, Scheduled Task, msiexec) không chạy được ở đây: phân tích tĩnh + ghi `KHÔNG ĐO ĐƯỢC` kèm lý do; đừng suy thành "đúng".
Mọi khẳng định đo TẠI `210ab81c3f1af36243748458eb5e70180baeab71`. Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached; `core.abbrev=7`).
