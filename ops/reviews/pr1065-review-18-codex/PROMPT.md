# Cross-review lượt 18 — head CUỐI của PR #1069 (ops/vm cho PR #1065 + ghi sổ) — reviewer: codex

## Đối tượng
- `reviewed_sha`: `958ca60684f38305a9cf9276af3b99c73940ea97` (head nhánh `ccr-5249948c-9epnbs`, PR #1069). Cây đầy đủ, KHÔNG shallow, ở `cay-kho/` (HEAD detached; `core.abbrev=7`);
  `origin/master` trong cây = `713694b`.
- Lượt 16 (`verdict-luot16.md`) đã `approve` 0/0/0/0 trên `210ab81`. Theo PROTOCOL §5.1 / AGENTS.md §6, head đổi sau review thì review cũ hết hiệu lực;
  head đã đổi `210ab81` → `958ca60684f38305a9cf9276af3b99c73940ea97` qua: (1) commit hiện vật review `cbe05f2` (ops/reviews/pr1065-review-16-codex/, verdict phẳng), (2) biên nhận v2 +
  cập nhật hồ sơ land `5f32e91`, (3) merge `origin/master` `1bc4684` + hàng README `716804b`, (4) merge `origin/master` `7b845f5` giải xung đột README `4b3f07e`, (5) vá P2 lượt 17 `efedc75` (readback thread + sửa lời khai), (6) merge `origin/master` `713694b` (không xung đột) `958ca60684f38305a9cf9276af3b99c73940ea97`.
- Executor khai: `git diff 210ab81 958ca60684f38305a9cf9276af3b99c73940ea97 -- ops/vm` RỖNG (mã đã approve không đổi byte). `git diff origin/master 958ca60684f38305a9cf9276af3b99c73940ea97` chỉ chạm `ops/vm/` (3 tệp, = bản đã approve),
  `ops/land/` (16), `ops/reviews/` (106). Diff ghi sổ so master: `diff-ghi-so.patch`; numstat từ 210ab81: `numstat-tu-210ab81.txt`.
- Lượt 17 (`luot17/VERDICT.md`, chấm `4b3f07e`): `changes_requested` 0/0/1/0 — P2 `khai-resolved-khong-co-readback`; script kiểm của bạn ở `luot17/`. Diff ghi sổ từ `4b3f07e`: `diff-tu-luot17-ghi-so.patch`.
- CI trên `716804b`: 39/39 xanh (thuật lại từ phiên điều phối).

## Nhiệm vụ (khoanh vùng)
0. **Đóng finding lượt 17 thật chưa** (đo): `readback-review-threads-1065.json` có thread, `is_resolved`, quan hệ với 4430537534; SHA256SUMS.txt khớp; lời khai mới không rộng hơn tệp (lưu ý: tệp là TRÍCH từ phản hồi MCP, không phải bản thô).
1. **Xác minh khoanh vùng** (đo): `ops/vm/` tại head bằng byte `210ab81`; mọi tệp khác so `origin/master` chỉ thuộc `ops/land/pr1065-*`, `ops/reviews/pr1065-review-16-codex*`,
   `ops/reviews/README.md`; hai lần merge master không làm mất/hỏng hàng nào của master (đặc biệt bảng `ops/reviews/README.md`: so tập hàng master ⊆ tập hàng head).
2. **Ghi sổ đúng sự thật** (đo, đừng nhận lời): biên nhận `ops/reviews/pr1065-review-16-codex-verdict.receipt.yaml` (sha256 verdict, reviewed_sha/tree, run.json
   khớp, neo blob `cbe05f2` là tổ tiên head) — chạy `python3 ops/bien_nhan_v2.py --root cay-kho`; hồ sơ `ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml`
   — chạy `python3 ops/land_evidence_nguon.py --root cay-kho --tep ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml`, và đối chiếu từng lời khai `measured`
   với tệp readback nó trỏ (SHA256SUMS.txt khớp; con số trong lời khai = con số trong tệp). Có lời khai nào RỘNG hơn phép đo không (vd "41 đột biến", "landed")?
3. **Không có secret / đường dẫn nhạy cảm** trong hiện vật review mới: `python3 cay-kho/scripts/pkg_secret_scan.py cay-kho/ops/reviews/pr1065-review-16-codex`.
4. Nếu (1) cho thấy `ops/vm/` đổi, review lại mã như các lượt trước (pwsh Linux ở `pwsh/pwsh`, `TL_TEST_PYTHON=python3`).

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này NGAY (dòng đầu `verdict: dang_lam`), nối thêm sau MỖI hướng thử. Cuối cùng dòng đầu `verdict: approve` hoặc `verdict: changes_requested`,
dòng 2 `reviewed_sha: 958ca60684f38305a9cf9276af3b99c73940ea97`, và một dòng `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`
Mỗi hướng: giả thuyết / lệnh / output / kết luận (LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC). Finding: `### <slug>  [P0|P1|P2|P3]  <tiêu đề>` + TỆP/DÒNG, VẤN ĐỀ, ĐÃ THỬ NGHIỆM, ĐỘ TIN.
P0 = leo quyền / chạy mã chưa kiểm băm bằng SYSTEM. P1 = hành vi sai đo được. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt. P3 không chặn approve.
"approve" không có output thật là không hợp lệ.

## Ràng buộc
Reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/`, KHÔNG push, KHÔNG gọi mạng. Mọi khẳng định đo TẠI `958ca60684f38305a9cf9276af3b99c73940ea97`.
