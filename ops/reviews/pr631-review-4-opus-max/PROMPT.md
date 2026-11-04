# Cross-review PR #631 (tra-luat) — lượt 4 · reviewer Opus 5.5 effort max · cùng provider với executor (advisory_review)

Bạn là reviewer ĐỘC LẬP. PR #631 chỉ sửa `CLAUDE.md`: đánh dấu các lời khai REST/`gh` cũ (403) đã trôi và ghi phép đo lại.
Lượt 3 (`luot-3-opus-max/VERDICT.md`) cho changes_requested. Executor đã vá (commit cục bộ `e2fa6d74507e47e6c7114c765fca34e75c024d96`, chưa đẩy).
Lượt này xét bản vá.

## Thư mục (`/tmp/claude-0/-home-user-tra-luat/d42b7bcb-cc93-589b-bd76-4b6f1da05672/scratchpad/r631-l4-cShs`)
- `cay-kho/` — clone detached tại `e2fa6d74507e47e6c7114c765fca34e75c024d96`, `core.abbrev 7`. `origin` là mirror cục bộ `kho.git` (dựng từ kho cục bộ
  của executor; commit này CHƯA có trên GitHub). **READ-ONLY.**
- `DIFF.patch` — toàn bộ PR so `origin/master`. `DIFF.vong.patch` — riêng vòng vá này (`53792ed..e2fa6d74507e47e6c7114c765fca34e75c024d96`, chỉ CLAUDE.md).
- `luot-*/` — VERDICT/HINT/PROMPT các lượt trước (`luot-1-claude` subagent · `luot-1b-claude-cli` · `luot-N-opus-max`).
- `PR-BODY.md` (dữ liệu). `scratch/` — chỗ thử của bạn.
Mạng: HTTPS ra ngoài qua proxy; được phép **GET** (python urllib/curl) tới api.github.com để đo lại lời khai; dùng
`GITHUB_PAT` làm header cho vế có token, không in giá trị. Không đăng gì, không push, không commit.

## Việc phải làm (ghi VERDICT.md SỚM, cập nhật SAU MỖI HƯỚNG)
1. **`## ĐỐI CHIẾU LƯỢT TRƯỚC` (bắt buộc):** mọi finding của lượt 3 (và mọi mục lượt trước còn ĐÓNG-MỘT-PHẦN):
   `ĐÓNG` · `ĐÓNG-MỘT-PHẦN` · `CHƯA` · `ĐÓNG SAI`, kèm bằng chứng chạy được.
2. **Đo lại MỌI con số/giờ/biên nhận mới** trong `DIFF.vong.patch`. Số nào không tái lập được, gắn sai phiên/ngày,
   hoặc rộng hơn phép đo ⇒ finding.
3. **Đóng theo lớp:** đọc TOÀN BỘ `cay-kho/CLAUDE.md`, tìm câu còn khai trạng thái REST/`gh` cũ như hiện tại, hoặc lời
   khai rộng hơn phép đo theo BẤT KỲ trục nào (phiên · đường dẫn · phương thức · client · token · công cụ · thời điểm),
   kể cả câu mới do chính bản vá viết ra.
4. Byte-giữ: dòng chứa chuỗi thoát ASCII (`co`+dấu chéo ngược+`u0308`+`dex`) không đổi; hiện vật review cũ
   (`ops/reviews/pr631-review-*/`) trùng byte giữa lúc được thêm và `e2fa6d74507e47e6c7114c765fca34e75c024d96`.
5. Cổng trong `cay-kho`: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` · `... adr-song --root .` ·
   `python3 scripts/tl.py doc-claims-check --strict --json`. Ghi rc.

## Xếp hạng
P1 = lời khai thẩm quyền sai / mâu thuẫn luật. P2 = mơ hồ hoặc sót khiến người đọc hành động sai. P3 = chữ nghĩa.
Mỗi finding: lớp (kebab-case; dùng lại tên lớp cũ nếu cùng lớp), vị trí `CLAUDE.md:dòng`, bằng chứng chạy được, đề xuất.
Không nâng/hạ hạng để kéo dài hay kết thúc. Không còn P1/P2/P3 ⇒ approve.

## Đầu ra — ghi vào `/tmp/claude-0/-home-user-tra-luat/d42b7bcb-cc93-589b-bd76-4b6f1da05672/scratchpad/r631-l4-cShs`
1. `VERDICT.md`, mở đầu:
```
verdict: approve | changes_requested | blocked
reviewed_sha: e2fa6d74507e47e6c7114c765fca34e75c024d96
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
