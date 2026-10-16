# Đặc tả đóng băng — LEASE-PUBLISH-WINDOWS-DO r3 (packet #687)

Revision 3 THAY r2 (`ops/specs/lease-publish-windows-do-r2.md`, blob sha256 `cab12ba9…`). r2 vẫn là hợp đồng của
phần đã thi công tới `807c6c2`. r3 giữ nguyên MỌI tiêu chí của r1 §3/§4 và r2 §3/§4/§5, chỉ đổi các mục dưới.

Lý do revision: packet #677 (DOT-BIEN-L-BIEN-CONG-KHAI) đã land vào master bằng PR #689 (merge `20ec8d5`, +600/−15
trên CHÍNH `ops/lease_publish_test.py`). Gặp hai vướng:
- S5′ của r2 đo so baseline `89fc4fa`, nên merge master xong sẽ tính cả 600 dòng của #677 và vượt trần, dù phần
  của #687 chỉ ~+264.
- Review codex `gpt-6-astra` (r2 §6.6) không chạy được: codex hết quota tới 2026-10-03.

Chỉ thị chủ kho trong phiên Claude Code session_01RU4YGGdYMx94uVcywPjo4F, 2026-10-01 ~01:05Z. Trước đó chủ kho nói:
"#687: ĐỒNg ý, cấp lease và làm đi". Khi được hỏi về hai vướng trên, chủ kho chọn
"Spec r3: đo trần so merge-base, Sonnet review (Recommended)". Mô tả của phương án ấy, chép nguyên văn: "S5′ = git
diff --numstat $(merge-base HEAD origin/master) HEAD -- ops/lease_publish_test.py ≤ 600 (chỉ tính phần của #687).
Review = Sonnet 5.5 advisory_review thay codex, kết thúc bằng human audit của anh như #677. Vá Opus 5.5 max. Cấp
lease g3 theo r3 rồi làm."

## 0. Mốc

- Immutable acceptance baseline cho A8-tương-đương (phần không được đổi): `89fc4fac8cea65979cc2483043dc8cd07a6e8518`.
- Continuation base: `6112b89eefaa358a715d90800789b2d1456c1729` (head nhánh lúc soạn r3).
- Master khi soạn: `20ec8d5d0e86cb7dc01f202c7596407a957e5961` (đã có #677).
- Nhánh: `claude/lease-publish-windows-do`. Không force-push.

## 1. Write set (exact) — không đổi

- `ops/lease_publish_test.py`

## 2. Trần kích thước (S5″ thay S5′ của r2)

- **S5″:** `git diff --numstat $(git merge-base HEAD origin/master) HEAD -- ops/lease_publish_test.py` ≤ **600** dòng
  thêm, đo SAU khi merge master. Đo như vậy là chỉ tính phần của #687; dòng của #677 đã nằm trong merge-base.
- Mọi báo cáo kích thước in CẢ số đo S5″ LẪN `git diff --numstat 89fc4fa HEAD -- ops/lease_publish_test.py`
  (tham khảo, không phải trần).
- Vượt S5″ ⇒ DỪNG trước review, báo chủ kho.

## 3. Bổ sung do #677 đã land (mới ở r3)

- **M1.** Merge `origin/master` vào nhánh bằng merge commit (không rebase). Giải xung đột trên
  `ops/lease_publish_test.py` sao cho GIỮ NGUYÊN hành vi của cả hai phía: các ca `t195`–`t202` cùng helper
  `_chay_buoc_dang_that` của #677, và các ca `t193`/`t194` cùng sửa `t125`/`t160`/`main()` của #687.
- **M2.** Sổ đăng ký BỎ QUA của A1 (r1 §3) phải tính tới các ca của #677 có thể ném `BoQuaNen`. Mỗi ca ném
  `BoQuaNen` với cặp (tệp, job) nào thì phải nằm trong sổ với đúng cặp ấy. Ca nào không ném thì KHÔNG được thêm
  vào sổ (sổ chỉ chứa ca thật sự cần, đúng tinh thần danh sách cho phép). Phải đo bằng chạy thật, không suy từ tên.
- **M3.** Ca khoá: `t193` (hoặc một ca mới) có vế: một ca của #677 ném `BoQuaNen` khi KHÔNG có trong sổ ⇒ ĐỎ.
  Đột biến bỏ một ca #677 khỏi sổ ⇒ đỏ đúng ca ấy (nếu ca ấy có ném); đột biến thêm một ca không ném vào sổ ⇒
  không làm xanh giả ca nào.
- **M4.** Bảng đột biến bắt buộc của r1/r2 (14 của r1, R15–R23, ba dạng unsupported) phải đo LẠI sau merge, trên
  bản sao tạm. Đột biến `L` gốc của #677 (spec #677 r8 §2) vẫn phải chết ≥1 ca.

## 4. Review và assurance (thay r2 §6.6)

- Executor: agent Opus 5.5, effort max (agent `va-spec-opus-max`). Model/effort thực chạy: KHÔNG ĐO ĐƯỢC.
- Reviewer: agent Sonnet 5.5 (`review-sonnet`), cùng họ Claude ⇒ `advisory_review`. Review phân LỚP kèm hint
  patch; lặp vá → review → đăng verdict lên PR/Issue #687 tới 0 P1/P2/P3.
- Packet class `sensitive` (bộ test của cổng đọc lease) ⇒ kết thúc bằng `human_audited` của chủ kho. Không khai
  `cross_approved`.
- Commit ký, không đẩy trong vòng lặp. Sạch thì fetch, merge master nếu tụt, chạy cổng tại chỗ, rồi đẩy MỘT lần.

## 5. Nghiệm thu (thay r2 §6, giữ nguyên các mục không nêu)

1. Linux: một lệnh dựng cả hai vế cùng python — nền là master tại merge-base, nhánh là head. Nhánh phải ra
   `N/N đạt; đã chạy=N, bỏ qua=0`, kể cả `[A]`/`[B]` của `t125`.
2. Bảng đột biến r1 + r2 + M3/M4: mỗi dòng GIẾT đúng assertion của ca đích, không tín dụng giả.
3. ruff `--select F` delta so merge-base = 0; `git diff --check` rc 0; `doctrine-scan` rc 0.
4. S5″ ≤ 600.
5. Windows: KHÔNG CI cho tới khi đủ điều kiện merge; phần Windows khai KHÔNG ĐO ĐƯỢC.
6. Review Sonnet tới 0 P1/P2/P3, rồi human audit của chủ kho.

## 6. Điều kiện dừng

Như r1 §6 và r2 §7, với S5 thay bằng S5″. Thêm: chủ kho chỉ cho MỘT lượt CI khi đủ điều kiện merge; không chạy CI
nào khác. Không mở PR trước lúc sạch (mở PR là kích `pull_request`).
