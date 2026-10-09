# Đặc tả đóng băng — LEASE-PUBLISH-WINDOWS-DO r1 (packet #687)

Nợ 2 của #579 (human audit `pull/589#issuecomment-5857502345`). Nguồn finding: cross-review r1
(`issues/687#issuecomment-5888197946`, VERDICT.md sha256 `412d0825335de5850ae4412aa55ad37915c32158f29b89e61a965d3bb875ea81`).
Chỉ thị chủ kho mở packet và cấp lease: trong phiên Claude Code 29-09-2026, chọn phương án "1"
("cấp lease cho `ops/lease_publish_test.py` để vá L1, L2").

## 0. Mốc

- Immutable acceptance baseline = continuation base: `89fc4fac` (`origin/master` lúc mở, sau PR #680).
- Nhánh duy nhất: `claude/lease-publish-windows-do`. Không force-push. Không `[skip`+`ci]` trong commit.

## 1. Mục tiêu

`ops/lease_publish_test.py` không được báo xanh khi (L1) một ca đáng lẽ phải đo lại được miễn,
hoặc (L2) hai lượt con A/B của `t125` cùng hụt ca. Mã nghiệp vụ `ops/lease_publish.py` KHÔNG đổi.

## 2. Write set (exact)

- `ops/lease_publish_test.py`
- `ops/specs/lease-publish-windows-do-r1.md` (chỉ tệp này, đã đóng băng — sửa = revision mới)

Chạm đường ngoài write set (kể cả `ops/lease_publish.py`, `.github/**`) ⇒ DỪNG, báo chủ kho.

## 3. L1 — hợp đồng quyền bỏ ca (P2)

Hiện trạng đo được (verdict r1): `_ly_do_bo_qua_workflow` chỉ tra `matrix.<khoá>`, bỏ qua
`strategy.matrix.include`/`exclude`; nhận mọi nhãn bắt đầu `ubuntu-`; và `main()` cấp BỎ QUA cho
BẤT KỲ ca nào ném `BoQuaNen(WORKFLOW_DANG, 'dang')` — probe của reviewer cho `0/0 đạt; bỏ qua=1; rc=0`.

Phải đạt:
- **A1.** `main()` chỉ chấp nhận `BoQuaNen` từ ca có tên nằm trong một SỔ ĐĂNG KÝ khai tĩnh
  (tên ca → (tệp workflow, job)); ca ngoài sổ, hoặc cặp (tệp, job) ném ra khác cặp đã đăng ký ⇒ ĐỎ.
  Sổ hiện tại đúng bảy ca `t51 t59 t60 t62 t63 t66 t68` với (`ops-publish-lease.yml`, `dang`).
- **A2.** Bộ giải `runs-on` fail-closed: chỉ trả "chỉ Ubuntu" khi phân giải ĐƯỢC TOÀN BỘ tập nhãn
  (tính cả `include`; `exclude` hoặc dạng chưa hỗ trợ ⇒ "không chứng minh được" ⇒ không miễn), và mỗi
  nhãn thuộc DANH SÁCH CHO PHÉP tường minh (`ubuntu-latest`, `ubuntu-24.04`, `ubuntu-22.04`) — không
  khớp tiền tố. `t72` nếu đang dựng nhãn ngẫu nhiên để tự chấp thuận thì phải đổi cho khớp luật mới.
- **A3.** Không bắt buộc tách phần logic độc lập nền của bảy ca ở r1 (verdict ghi là quan sát, hint
  "tách portable" là tuỳ chọn). Nếu KHÔNG tách, handoff phải khai rõ phần chưa đo trên Windows.
- **Ca khoá:** `t193_hop_dong_bo_qua_chi_cap_cho_ca_da_dang_ky` qua CHÍNH `main()` (seam `nen='nt'`):
  (a) ca ngoài sổ ném `BoQuaNen` ⇒ ĐỎ; (b) ca trong sổ ném với (tệp, job) khác ⇒ ĐỎ; (c) matrix
  `os: [ubuntu-latest]` + `include: [{os: windows-latest}]` ⇒ không miễn; (d) nhãn `ubuntu-not-a-runner`
  ⇒ không miễn; (e) đối chứng: ca trong sổ + workflow Ubuntu-only thật ⇒ BỎ QUA hợp lệ.
- **Đột biến bắt buộc** (chạy trên BẢN SAO TẠM): bỏ kiểm sổ · bỏ xử lý `include` · đổi danh sách cho phép
  về khớp tiền tố · nới sổ thêm tên ca tấn công — MỖI cái phải làm `t193` ĐỎ.

## 4. L2 — phép so A/B phải xác minh đủ ca trước khi so (P2)

Hiện trạng: `t125` lấy dòng tổng kết đầu tiên (regex không neo) + tập ĐỎ/BỎ QUA rồi so hai vế; hai con
cùng in `0/0` hoặc `1/1` vẫn QUA (probe thật của reviewer).

Phải đạt:
- **B1.** Trước khi so, mỗi transcript con qua một hàm xác minh: đúng MỘT dòng tổng kết neo đầu dòng;
  mọi ca trong `CA` có đúng một `>>> vao` và một `<<< ra`, cùng thứ tự, không trùng, không tên lạ;
  N/M và `đã chạy`/`bỏ qua` khớp đếm từ transcript; tập bỏ qua ⊆ sổ L1. Hỏng ⇒ `t125` ĐỎ với lý do.
- **B2.** `t160` (fixture parity) được cập nhật để vẫn là đối chứng hợp lệ dưới luật mới.
- **Ca khoá:** `t194_AB_phai_du_bang_chung_truoc_khi_so` cấp transcript giả cho HÀM XÁC MINH:
  cùng 0/0 · cùng 1/1 · hụt một ca · trùng tên · thiếu `ra` · tổng kết lệch marker ⇒ ĐỎ; transcript đủ
  tập ca + skip hợp lệ ⇒ QUA.
- **Đột biến bắt buộc:** bỏ gọi hàm xác minh trong `t125` · chỉ so số tổng thay vì tập tên — mỗi cái
  làm `t194` (hoặc `t125` trên fixture) ĐỎ.

## 5. Nghiệm thu

1. `python ops/lease_publish_test.py` trên Linux: `N/N đạt; đã chạy=N, bỏ qua=0`, N = số ca mới
   (187 + ca thêm). Đo delta so baseline trên CÙNG rig (CLAUDE.md "dựng cả hai vế trong một lệnh").
2. Bảng đột biến §3/§4: mỗi dòng GIẾT đúng ca đích, không tín dụng giả.
3. `python -m ruff check --select F ops/lease_publish_test.py`: delta so baseline = 0.
4. Windows: một lượt `gate-ops (windows-latest)` CHỈ KHI chủ kho cho phép rõ; kỳ vọng `N−7/N−7, bỏ qua=7`
   với đúng tập sổ L1.
5. Cross-review codex `gpt-6-astra` (effort ≥ medium), phân LỚP, kèm hint patch; lặp vá → review →
   đăng verdict lên #687 tới 0 P1/P2/P3.

## 6. Điều kiện dừng

- S1 chạm ngoài write set · S2 CI đỏ vì packet · S5 > 300 dòng thêm (ADR-0044) · S6 hết hạn lease ⇒ DỪNG, báo.
- Không tự merge/approve/land; không tự nới hạn; không cấp generation mới khi một lượt review đang chạy.
- Không chạy CI/Windows làm bằng chứng khi chưa được phép.
