# Đặc tả đóng băng — LEASE-PUBLISH-WINDOWS-DO r2 (packet #687)

Revision 2 THAY r1 (`ops/specs/lease-publish-windows-do-r1.md`, blob sha256 `87375af3…e230`). r1 vẫn là
hợp đồng của phần đã thi công tới `807c6c2`; r2 giữ nguyên MỌI tiêu chí của r1 §3/§4/§5 và thêm các mục dưới.

Lý do revision: cross-review r2 (`issues/687#issuecomment-5889287916`) — `CHANGES_REQUIRED`, lớp L1/L2/L4
P2 (7 đột biến sống trên `807c6c2`) và L5 P2 (toàn diff +445 vượt S5=300 của r1). Chỉ thị chủ kho trong phiên
Claude Code 29-09-2026, trả lời câu hỏi về trần S5: chọn **"Nâng trần, revision r2"** — mô tả phương án được
chọn: "Soạn spec r2: trần tính riêng ops/lease_publish_test.py ≤ 600 dòng thêm, spec/lease không tính; cấp lease
g2 thay g1 (bia mộ hai chiều). Rồi Opus vá L1/L2/L4, review r3."

## 0. Mốc

- Immutable acceptance baseline: `89fc4fac8cea65979cc2483043dc8cd07a6e8518` (KHÔNG đổi).
- Continuation base: `807c6c2898b2338cbc8f97cbcd8540519fbe4f8a` (head r1 đã review ở r2).
- Nhánh: `claude/lease-publish-windows-do`. Không force-push.

## 1. Write set (exact) — không đổi so với r1

- `ops/lease_publish_test.py`

## 2. Trần kích thước (thay S5 của r1)

- **S5′:** `git diff --numstat <baseline> <head> -- ops/lease_publish_test.py` ≤ **600** dòng thêm.
- Hồ sơ điều phối (`ops/specs/lease-publish-windows-do-r*.md`, `ops/leases/lease-publish-windows-do-*.yaml`)
  KHÔNG tính vào S5′; mọi báo cáo kích thước phải in CẢ toàn diff lẫn riêng tệp mã.
- Vượt S5′ ⇒ DỪNG trước review, báo chủ kho.

## 3. Bổ sung L1 (từ r2-L1)

- **A2′.** Bộ giải `runs-on` kiểm cấu trúc `strategy`/`matrix`/`exclude` TRƯỚC mọi nhánh trả sớm (kể cả
  `runs-on` literal hoặc list): có `exclude`, trục matrix dạng không hỗ trợ, hay strategy sai kiểu ⇒ không miễn.
- **A4.** `t193` có vế âm đi qua `main()` với SỔ MẶC ĐỊNH, trong đó YAML ở ĐÚNG đường `WORKFLOW_DANG` (trên cây
  fixture biệt lập, không đụng tệp thật của kho) đổi sang có Windows ⇒ ca trong sổ ném đúng cặp vẫn ĐỎ.
- **A5.** Định danh đường dẫn: alias (symlink, `..`) trỏ CÙNG tệp ⇒ được miễn; cùng basename khác tệp ⇒ ĐỎ.
  Nền không tạo được symlink ⇒ vế symlink khai BỎ QUA có lý do (đếm, in), vế `..` vẫn phải đo.
- **Đột biến phải ĐỎ:** R15 (main tin sổ thay đọc YAML thật) · R20 (resolve → absolute) · ba dạng
  unsupported `fixed_exclude`/`list_exclude`/`bad_other_axis` được miễn.

## 4. Bổ sung L2 (từ r2-L2)

- **B3.** Hàm xác minh parse TUẦN TỰ thành bản ghi ca: mỗi `<<< ra` có đúng một trạng thái ∈ {QUA, DO, BO_QUA}
  và thời lượng hợp lệ; `len(kết quả) == len(tên ca)`; QUA+DO+BO_QUA == tổng; tên ca kỳ vọng DUY NHẤT (kiểm
  trước so chuỗi). Dòng chẩn đoán xen giữa marker và CRLF vẫn phải được nhận.
- **B4.** `t194` thêm vế ĐỎ: trạng thái lạ/khuyết · đủ tên nhưng mọi trạng thái hỏng · CA trùng · dòng BỎ QUA
  lệch `<<< ra` · rc sai (cả ở hàm xác minh lẫn wiring t125).
- **B2′.** `t160` dựng transcript ĐỦ ca và dùng hàm xác minh THẬT (spy bọc được phép), không mock trả `[]`.
- **Đột biến phải ĐỎ:** R16 (bỏ đối chiếu BỎ QUA) · R17 (bỏ kiểm rc) · R18/R19 (t125 bỏ truyền rc).

## 5. L4 mới — seam của `main()` phải bảo toàn trạng thái

- **C1.** Ca meta (mở rộng t193 hoặc ca mới) chụp `CA` (danh sách + identity hàm), `SO_BO_QUA`, `os.name`,
  `sys.argv`; gọi seam `chon`/`nen`/`so` nhiều lượt, gồm lượt fixture ném lỗi; tất cả phải nguyên trạng sau
  mỗi lượt.
- **Đột biến phải ĐỎ bởi assertion "rò trạng thái"** (không dựa vào `NotImplementedError` của `WindowsPath`):
  R21 (`nen` ghi `os.name`) · R22 (`chon` ghi đè `CA`). R23 vẫn phải bị giết.

## 6. Nghiệm thu (thay §5 r1, giữ nguyên các mục không nêu)

1. Linux, hai vế cùng lệnh cùng python: nền `187/187 bỏ qua=0`; nhánh `N/N đạt; đã chạy=N, bỏ qua=0`.
2. Bảng đột biến: 14 của r1 + R15–R23 + ba dạng unsupported, mỗi dòng GIẾT đúng assertion của ca đích.
3. ruff `--select F` delta = 0.
4. S5′ ≤ 600.
5. Windows: KHÔNG CI cho tới khi merge (chỉ thị chủ kho) ⇒ phần Windows khai KHÔNG ĐO ĐƯỢC.
6. Cross-review codex `gpt-6-astra` (effort ≥ medium), phân LỚP, kèm hint patch; lặp tới 0 P1/P2/P3;
   verdict đăng lên #687.

## 7. Điều kiện dừng

Như r1 §6, với S5 thay bằng S5′. Không chạy CI/full CI; không mở PR (mở PR kích `pull_request`).
