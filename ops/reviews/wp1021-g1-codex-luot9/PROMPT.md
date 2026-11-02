# Cross-review độc lập — packet #1021 r2 (BIEN-NHAN-V2-GLOB-HOA-THUONG), lượt 9 (lời gọi Codex 9/9 — LƯỢT CUỐI theo trần)

Bạn là reviewer độc lập (họ openai) cho executor họ claude. Viết bằng tiếng Việt.

## Vì sao có lượt này
Lượt 8 (`VERDICT-LUOT8.md`, sha256 `bd891b299d189b83973db7cde3f184b9a17bcc1d3dd5ff7a0e6ee08b068b6ece`) review CÙNG head
`356a27e1378b2162bbc0be2ec06ff08fdacbdead`, kết luận **P0=P1=P2=P3=0 mở**, nhưng `request_changes` vì trở ngại snapshot
`snapshot-thieu-object-lich-su`: clone lượt 8 thiếu commit `4bc94325e647ee5e32373f3af30b8f83b98a90fa` (receipt
`ops/reviews/lease-publish-windows-do-review-r1-codex.receipt.yaml` tham chiếu) ⇒ C6 rc=2 (`3 KHÔNG ĐO ĐƯỢC`) và suite Linux 95/98
(c14, c40, c76). Lượt 8 đề nghị: bổ sung object thật vào **bản sao review mới**, kiểm cat-file/ancestry, chạy lại C6 và toàn suite
trên đúng HEAD, giữ nguyên mẫu số 98.

Executor đã làm đúng thế: `cay-kho/` là clone MỚI, có ĐỦ mọi nhánh của origin (dưới `refs/remotes/origin/*`) và mọi tag (gồm
`luu-tru/*`); object ấy nằm trên tag `luu-tru/lease-publish-windows-do-r1-verdict` và nhánh `origin/ops/do-lease-publish-windows-150`.
Không sửa hai tệp write set, không đổi receipt, không đổi HEAD. Executor KHAI đã đo trên clone này: C6 rc=0 `0 KHÔNG ĐO ĐƯỢC · tổng 306`
`TỔNG: ĐẠT`; suite `98/98 · 153/153 · 2/2` `TỔNG: ĐẠT` — đây là LỜI KHAI, bạn phải tự đo.

## Neo
- Head: `356a27e1378b2162bbc0be2ec06ff08fdacbdead` (detached tại `cay-kho/`, không nông). Base diff tổng: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`.
- SPEC: `SPEC.md`, sha256 `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`.
- Write set: `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py`. Băm nguồn lượt 8 đo: `7f9a86f3…276a6` / `cac81d46…74b87`.
- Đầu vào: `VERDICT-LUOT8.md`, `VERDICT-LUOT7.md`, `DIFF-LUOT8.patch`, `DIFF-TONG-tu-b29da0b.patch`, và `luot8-evidence/`
  (bản chép evidence + script của lượt 8, để tái dùng; script lượt 8 neo `ROOT` theo vị trí tệp — chép ra gốc sandbox nếu cần).

## Phạm vi
1. **Neo và snapshot**: HEAD/tree/SPEC/băm hai tệp nguồn khớp lượt 8; `git cat-file -t 4bc94325e647…` = commit; tổ tiên/ref chứa nó;
   không nông; checkout sạch. Xác nhận snapshot không thay đổi gì trong cây được review so lượt 8 (cùng tree).
2. **ĐỐI CHIẾU LƯỢT TRƯỚC**: trở ngại `snapshot-thieu-object-lich-su` — đo C6 (`python3 ops/bien_nhan_v2.py --root .`, đòi `0 KHÔNG ĐO
   ĐƯỢC`, `TỔNG: ĐẠT`, tổng khớp đếm độc lập) và **toàn suite** `python3 ops/bien_nhan_v2_test.py` (đòi N/N hai số bằng nhau, mẫu
   số 98, `TỔNG: ĐẠT`), riêng c14/c40/c76 phải ĐẠT. Các lớp P cũ (P3 lượt 7, F1/F2/F3, P1 c88, P3 m156/m157, giải xung đột #1037):
   được kế thừa phép đo lượt 8 vì HEAD/tree giống hệt — nói rõ đã kế thừa gì; nếu đủ thời gian, chạy lại ít nhất phép đột biến riêng
   m142, m153, m156, m157.
3. Tiêu chí còn lại C1a/C1b/C2/C3/C9: kế thừa lượt 8 (cùng tree) hoặc đo lại; C4/C5 CI và C7 Windows local: như lượt 8 (đọc độc lập
   được thì đọc, không thì KHÔNG ĐO ĐƯỢC; không nhận lời khai; không chạy test Windows từ xa).
4. Nếu thấy bất kỳ P0–P3 mới nào trong diff tổng thì báo đủ (mức, slug, `tệp:dòng`, tái hiện, `HÌNH DẠNG:`, hướng vá).

## Ràng buộc
- KHÔNG sửa tệp nào trong `cay-kho/`; đột biến/fixture chỉ trên bản sao hoặc qua `_dot_bien_tep` trong sandbox; kiểm snapshot đầu/cuối.
  Không commit/push/fetch, không gọi workflow, không ghi ngoài sandbox (đặt `TMPDIR` trong sandbox).
- Mọi tiến trình đo: `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`;
  `core.abbrev=7` đã đặt. Lưu lệnh/cwd/rc/thời gian/stdout/stderr vào `evidence/`.
- Phản chứng cần nội dung nhạy cảm thì mô tả bằng lời.
- Approve chỉ khi không còn P0/P1/P2/P3 mở VÀ C6 + toàn suite Linux đạt trên head này. C4/C5/C7 KHÔNG ĐO ĐƯỢC tự nó không phải finding
  mã (ghi rõ trong bảng tiêu chí là giới hạn), như cách lượt 4 đã approve.
- Ghi `VERDICT.md` TĂNG DẦN ở gốc sandbox ngay từ đầu.

## Dạng `VERDICT.md`
```
Verdict: approve|request_changes
Reviewed commit: 356a27e1378b2162bbc0be2ec06ff08fdacbdead
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d
```
Sau đó: kết luận ngắn; Neo và cách tái hiện; ĐỐI CHIẾU LƯỢT TRƯỚC (bảng); Bảng tiêu chí; Bảng finding (đếm P0/P1/P2/P3 mở);
Kiểm tra cuối và giới hạn. Verdict không cấp quyền merge/land.
