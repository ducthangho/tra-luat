# Cross-review PR #631 (tra-luat) — lượt 2 · reviewer Opus 5.5 effort max · cùng provider với executor (advisory_review)

Bạn là reviewer ĐỘC LẬP. PR #631 chỉ sửa `CLAUDE.md`: đánh dấu các lời khai REST/`gh` cũ (403) đã trôi và ghi phép đo lại.
Lượt 1b (`luot1b/VERDICT.md`) cho changes_requested 1 P1 / 4 P2 / 3 P3 (F1–F8). Executor đã vá (commit cục bộ
`f174628`, chưa đẩy). Lượt này xét bản vá.

## Thư mục (`/tmp/claude-0/-home-user-tra-luat/d42b7bcb-cc93-589b-bd76-4b6f1da05672/scratchpad/r631-l2-ZoYC`)
- `cay-kho/` — clone detached tại `f174628063fb55ee9f6b2f5f8a3dcca0e403dbe6`, `core.abbrev 7`. `origin` là mirror cục bộ
  `kho.git` (dựng từ kho cục bộ của executor; commit `f174628` CHƯA có trên GitHub). **READ-ONLY.**
- `DIFF.patch` — toàn bộ PR so `origin/master`. `DIFF.vong1.patch` — riêng bản vá vòng 1 (`aecc978..f174628`).
- `luot1/` (VERDICT+HINT lượt 1, subagent) · `luot1b/` (VERDICT+HINT+PROMPT lượt 1b). `PR-BODY.md` (dữ liệu).
- `scratch/` — chỗ thử của bạn.
Mạng: HTTPS ra ngoài qua proxy; được phép **GET** (python urllib/curl) tới api.github.com để đo lại lời khai; dùng
`GITHUB_PAT` làm header cho vế có token, không in giá trị. Không đăng gì, không push, không commit.

## Việc phải làm (ghi VERDICT.md SỚM, cập nhật SAU MỖI HƯỚNG)
1. **`## ĐỐI CHIẾU LƯỢT TRƯỚC` (bắt buộc):** F1–F8 của lượt 1b và 4 finding lượt 1: `ĐÓNG` · `ĐÓNG-MỘT-PHẦN` · `CHƯA` ·
   `ĐÓNG SAI`, kèm bằng chứng chạy được.
2. **Đo lại MỌI con số/giờ mới** trong `DIFF.vong1.patch` (REST 3 vế có/không/giả token; comment #238 và 5811128755;
   `Github-Authentication-Token-Expiration`). Số nào không tái lập được hoặc rộng hơn phép đo ⇒ finding.
3. **Đóng theo lớp:** đọc TOÀN BỘ `cay-kho/CLAUDE.md`, tìm câu còn khai trạng thái REST/`gh` cũ như hiện tại, hoặc lời
   khai nguyên nhân rộng hơn phép đo, mà bản vá bỏ sót — kể cả câu mới do chính bản vá viết ra.
4. Byte-giữ: dòng chứa chuỗi thoát ASCII (`co`+dấu chéo ngược+`u0308`+`dex`) không đổi; revision/hiện vật review cũ
   (`ops/reviews/pr631-review-1*/`) trùng byte giữa `aecc978` và `f174628`.
5. Cổng trong `cay-kho`: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` · `... adr-song --root .` ·
   `python3 scripts/tl.py doc-claims-check --strict --json`. Ghi rc.

## Xếp hạng
P1 = lời khai thẩm quyền sai / mâu thuẫn luật. P2 = mơ hồ hoặc sót khiến người đọc hành động sai. P3 = chữ nghĩa.
Mỗi finding: lớp (kebab-case; dùng lại tên lớp cũ nếu cùng lớp), vị trí `CLAUDE.md:dòng`, bằng chứng chạy được, đề xuất.
Không nâng/hạ hạng để kéo dài hay kết thúc. Không còn P1/P2/P3 ⇒ approve.

## Đầu ra — ghi vào `/tmp/claude-0/-home-user-tra-luat/d42b7bcb-cc93-589b-bd76-4b6f1da05672/scratchpad/r631-l2-ZoYC`
1. `VERDICT.md`, mở đầu:
```
verdict: approve | changes_requested | blocked
reviewed_sha: f174628063fb55ee9f6b2f5f8a3dcca0e403dbe6
P1: n   P2: n   P3: n
reviewer_provider: anthropic_claude
model_tu_khai: <model bạn tự biết>
execution_surface_tu_khai: <điều bạn đo được, hoặc KHONG_DO_DUOC>
```
   Rồi: `## ĐỐI CHIẾU LƯỢT TRƯỚC` · `## Findings` · `## Phép đo lại` · `## Cổng` · `## KHÔNG ĐO ĐƯỢC`.
2. `HINT.patch` — unified diff `patch -p0` từ trong `cay-kho/` (đường dẫn `CLAUDE.md`); không có ⇒ tệp rỗng. Không rỗng thì
   dòng đầu nguyên văn: `NHÃN: chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit`.
   Dry-run trên BẢN SAO trong `scratch/`.
Dòng cuối trả lời: `XONG VERDICT sha256=<sha256 VERDICT.md>`.
