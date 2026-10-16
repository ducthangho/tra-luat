# ĐẶC TẢ ĐÓNG BĂNG — CAI-CONG-CU-SIGPIPE revision 2

Packet Issue: #675 · PR #681 · revision trước: `ops/specs/CAI-CONG-CU-SIGPIPE-r1.md` (sha256 `17a5fee7…`).
Lý do revision: cross-review lượt 1 (`ops/reviews/cai-cong-cu-sigpipe-r1-review-1-codex-verdict.md`,
sha256 `c8e86ff1…7352`, `changes_requested` trên `41d03d8`). Chủ kho chọn (29-09-2026, AskUserQuestion):
"Revision r2, nâng trần ~300" và "Gộp [B1] vào r2".

## 0. Ba mốc Git (§3.2.1)
- Immutable acceptance baseline: `cd23c7dbc7833d64a8e87e8ffd94f194c18e0060` (KHÔNG đổi so với r1).
- Continuation base: `41d03d8c0ab3374adef6e3d159ac568ae67bc429` (head r1 g1 trên `claude/cai-cong-cu-sigpipe-r1-g1`).
  Generation mới làm tiếp trên chính nhánh ấy (không rewrite lịch sử), và **merge `origin/master`** vào nhánh
  (drift đã đo ở PR #681: 2 tệp bookkeeping #574, không trúng kích hoạt §5.1).
- Reviewed candidate: exact head do executor tạo, diff đo từ `cd23c7d`.

## 1. Objective (giữ r1, mở rộng)
Như r1 §1, cộng: đóng B1 — `ops/don_ref_chot_test.sh` không còn phép dò đối số bằng pipeline
`printf … | grep -q` có thể đảo nhánh khi SIGPIPE; và W4 `ops/do_sigpipe.sh` đóng F1/F2/F3.

## 2. Đính chính r1 §3 (lời loại trừ SAI)
r1 §3 ghi `don_ref_chot_test.sh:327,333` "141 cũng ra nhánh 'đã thấy', đúng ngữ nghĩa". **SAI.**
`if ! printf '%s\n' "$@" | grep -q X`: khi `grep -q` khớp sớm và `printf` ăn SIGPIPE, pipefail cho 141,
`!` biến 141 thành ĐÚNG ⇒ vào nhánh fallback, nối thêm `GIA_REF_STATE=…`/`NEO_TEP=…` mặc định SAU giá
trị tường minh (reviewer tái hiện với 20.000 đối số). Không có `-e` nên script không chết — lỗi là ĐẢO NHÁNH.
Phần còn lại của r1 §3 giữ nguyên (reviewer đã đo lại: HƯỚNG 5 của verdict lượt 1).

## 3. Write set (exact)
- W1 `ops/cai_cong_cu.sh` · W2 `ops/cai_actionlint.sh` · W3 `ops/dung_goi_review.sh` — giữ nguyên bản vá r1
  (đã được xác nhận tương đương trên 5.436 phép so); chỉ sửa nếu một finding mới đòi.
- W4 `ops/do_sigpipe.sh`
- W5 `ops/don_ref_chot_test.sh` (MỚI ở r2)
NGOÀI write set, tuyệt đối không chạm: `ops/cong_cu_test.py`, `.github/workflows/ci.yml`,
`.claude/dev/ci_dang_ky_test.py` (lease #668) và mọi tệp khác. Tệp đến từ merge `origin/master` không tính
là sửa của packet.

## 4. Việc phải làm
- **F1 (P2)** W4 phải chứng minh phép gán được trích **nằm trên đường chạy thật**, không chỉ khớp văn bản.
  Cách do executor chọn (ví dụ: chạy chính script trong fixture offline với producer giả và đòi giá trị/sentinel
  đúng; hoặc từ chối ngữ cảnh không chứng minh được). Khoá: đột biến bọc dòng vào hàm không gọi, và vào
  here-doc `: <<'X' … X`, đều phải làm W4 ĐỎ; head vẫn xanh; baseline vẫn đỏ `rc141` từng điểm.
  Không chạy mạng, không cài thật, không ghi ngoài thư mục tạm.
- **F3 (P2)** tự kiểm (c) phải đi qua **chính bộ chấm của (b)** (dùng chung một hàm phán quyết) và đòi kết
  quả ĐỎ vì 141. Khoá: đột biến bản sao W4 đổi nhánh chấm (b) thành luôn đúng ⇒ (c) ĐỎ.
- **F2 (P3)** thiếu bất kỳ W1/W2/W3 nào ⇒ `rc=2` + `KHÔNG ĐO ĐƯỢC` nêu tên tệp, không tổng kết xanh.
- **W4 corpus** (từ verdict HƯỚNG 6): thêm đầu vào có `*` (và `?`/`[`/`%`), để đột biến kiểu
  `${LENH//\*/}` bị bắt.
- **B1 (P2)** W5 dòng 327,333: bỏ pipeline, dò đối số trực tiếp (ví dụ vòng `for a in "$@"; case "$a" in
  GIA_REF_STATE=*) …`), giữ đúng quy tắc khớp theo ĐẦU từng đối số. Khoá: một phép đo (trong W4 hoặc
  trong W5, executor chọn và ghi lý do) cho: khớp ở đầu + ≥ 20.000 đối số đệm ⇒ KHÔNG nối fallback; không
  khớp ⇒ vẫn nối mặc định. Phải ĐỎ trên dòng cũ, XANH trên dòng mới.
- Mọi đột biến chỉ trên BẢN SAO TẠM (`mktemp -d`, dọn bằng `trap`).

## 5. Nghiệm thu
- A1 như r1 (W4 N/N trên head; mỗi điểm W1–W3 baseline đỏ riêng) + các khoá F1/F2/F3/B1 ở §4, mỗi khoá có
  đột biến riêng làm ca đích ĐỎ.
- A2 `python ops/cong_cu_test.py` N/N (ghi số, thời gian, công cụ phụ đã cài); `t5` lặp ≥ 200 lần, 0 lần 141.
- A3 như r1 (bash_nen, actionlint+shellcheck, shellcheck W1–W5 delta 0 so `cd23c7d`; ruff: packet không sửa `.py`).
- A4 `python .claude/dev/ci_dang_ky_test.py` delta 0.
- A6 (MỚI) `bash ops/don_ref_chot_test.sh` N/N trên head, bằng số ca của baseline (không mất ca); và
  `python ops/lease_publish_test.py` (bộ gọi W5) không đỏ vì packet — delta 0 so `cd23c7d`.
- A5 cross-review Codex tới 0 P1/P2/P3; verdict đăng #675.

## 6. Điều kiện dừng
- S1 chạm đường ngoài W1–W5 ⇒ DỪNG. · S2 lease hết hạn ⇒ ngừng ghi, handoff.
- S3 cùng hình dạng finding ≥ 3 lần ⇒ hỏi chủ kho. · S4 không merge/land/approve/force-push/deploy.
- S5 diff từ `cd23c7d` (không tính tệp đến từ merge master) > **300** dòng thêm ⇒ DỪNG, hỏi chủ kho.
