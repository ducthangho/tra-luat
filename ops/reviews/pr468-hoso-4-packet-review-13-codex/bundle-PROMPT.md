# PROMPT — cross-review khác nền, LƯỢT 13, PR #468 `ducthangho/tra-luat`

Bạn là REVIEWER Codex, độc lập với executor (Claude). reviewed_sha = `f77f19895e00835d71644d82f1c54e9b519ccfe6`.
PHẠM VI ĐỌC ĐÓNG: chỉ đọc/ghi trong thư mục này (/tmp/claude-0/-home-user-tra-luat/d706aae3-d737-5ec6-8390-ae296d24c1a2/scratchpad/rv468g). KHÔNG mạng, KHÔNG commit/push. `cay-kho/` = bản sao đầy đủ tại reviewed_sha, **có đủ 303 nhánh trong `refs/remotes/origin/*`** (mirror thật, xem EVIDENCE §Năng lực đo). Ruff 0.15.15 ở `/usr/local/bin/ruff`.

## GHI RA ĐĨA NGAY — bắt buộc
Tạo `VERDICT.md` NGAY (header + `reviewed_sha`), cập nhật sau MỖI kết luận nhỏ. Dòng CUỐI khi xong: `verdict: approve` · `verdict: changes_requested` · `verdict: blocked`; trước đó `verdict: dang-do`. Nếu resume: ĐỌC LẠI `VERDICT.md` rồi làm tiếp. Nếu lập manifest hiện vật, đặt `ARTIFACTS.sha256` và chỉ liệt kê tệp thường (không symlink, không tmp).

## Tài liệu
- `tai-lieu/PROTOCOL-trich-8-12-13.md` (đọc TRƯỚC) · `tai-lieu/cross-review-SKILL.md` (khung VERDICT.md — dùng ĐÚNG khung).
- `tai-lieu/pr468-hoso-4-packet-review-12-codex-verdict.md` — **verdict LƯỢT 12** (2 P1 · 2 P2), lượt liền trước.
- `tai-lieu/DOC-READBACK-SAU-HAN-456.md` — readback sau hạn của một phiên executor KHÁC (14:39Z); `ai-dang-giu-readback.txt` + `ai-dang-giu-*.txt` — readback của phiên này (20:45Z). Cả hai là LỜI KHAI; phép đo của bạn mới là thứ đóng P1.
- `diff-tu-luot12.patch` / `numstat-tu-luot12.txt` — đổi sau 02b0b86: verdict+gói lượt 12, biên nhận/README/GHI-NHAN lượt 12, vá 2 P2 hồ sơ (receipt lượt 10/11), DOC-READBACK. `diff.patch`/`numstat.txt` — toàn PR so master.
- `tai-lieu/*` — 4 đặc tả, 4 thân Issue, bốn lease GATE, nháp, biên nhận 10/11/12, lease #456 bản trên master, ls-remote + ref-coverage; `ci_dang_ky_test.py`.
- `EVIDENCE.md` — cổng đã đo + giới hạn tự khai; mục nó bỏ sót mà bạn chỉ ra được tính là finding.

## Nhiệm vụ, theo thứ tự
### 1 — ĐỐI CHIẾU LƯỢT 12 (bắt buộc), giữ NGUYÊN slug, phân loại `ĐÃ VÁ THẬT · VÁ HỜ · VÁ SINH LỚI MỚI · CHƯA VÁ`, bằng chứng TỰ ĐO:
- `mirror-thieu-ref-khong-du-do-a9` (P1): so TẬP tên `for-each-ref refs/remotes/origin` (bỏ symref HEAD) với `tai-lieu/ls-remote-heads.txt` — phải bằng nhau (303/303, 0 thiếu); OID cũng khớp. Nếu khớp thì bạn ĐÃ có năng lực đo A9 ⇒ P1 này đóng bằng bundle.
- `bia-mo-mot-ref-khong-thu-hoi-moi-ban` (P1): chạy THẬT `python3 -B ops/lease_publish.py ai-dang-giu` cho `.github/workflows/ci.yml` và `.claude/dev/ci_dang_ky_test.py` trong cay-kho (giờ hiện tại > 14:30:07Z). Kỳ vọng NGƯỜI_GIỮ 1 = exec-1r4 ở cả hai, #456 chỉ còn HẾT_HẠN. Đếm ref thật mang blob 8b2103c/1f95042 bằng `git cat-file --batch-check` trên 303 nhánh — đối chiếu con số 11/1 của DOC-READBACK. Nói rõ: đóng bằng THỜI GIAN, cơ chế bia mộ chưa sửa (ngoài phạm vi PR).
- `bien-nhan-luot10-bo-sot-va-tron-dau-vet-phien` và `ghi-nhan-luot11-gan-sai-commit-va-moc-van-chuyen` (P2): kiểm bản vá ở df0800c đúng hai mỏ neo bạn chỉ ra, không đổi identity/assurance/băm.
### 2 — Trục Standards cho phần ĐỔI sau 02b0b86: biên nhận lượt 12 (thread 01a07bff-…, prompt_sha256, 1166.934 s, blob df0800c), hàng README + GHI-NHAN lượt 12 (kể cả lời khai "2 lần phóng đầu chặn rc=11"), DOC-READBACK có tự mâu thuẫn không (đơn vị blob/ref, số 303/306).
### 3 — BẢNG ĐO mọi con số. Nếu không còn finding P1/P2, hãy kết bằng `verdict: approve` và nói rõ approve là cho HỒ SƠ PR #468 (thuần ops/), không phải merge authorization và không phải nghiệm thu bốn packet.

## Định dạng finding
`### <slug-kebab>  [P1|P2|P3]  <tiêu đề>` + TỆP/DÒNG + VẤN ĐỀ + ĐÃ THỬ VÁ + ĐÃ THỬ NGHIỆM + ĐỘ TIN. Gợi ý vá mang nhãn "chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit". Không push gì.

## Ngân sách
Nhắm ≤ 45 phút; sắp hết thì chốt phần đã đo, ghi phần chưa đo là `KHÔNG ĐO ĐƯỢC`, vẫn kết bằng dòng `verdict:`.
