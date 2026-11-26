# Cross-review ĐẶC TẢ wp1466 r9 — lượt 9 (reviewer: Codex, effort high)

Bạn là REVIEWER độc lập và chỉ đọc. Không sửa kho, không push, không gọi API GitHub để ghi. Chỉ ghi vào `out/` trong thư
mục làm việc: verdict vào `out/VERDICT.md`, nháp và script đo cũng để dưới `out/`. Viết verdict bằng tiếng Việt.

## Đối tượng
- Kho `github.com/ducthangho/tra-luat`.
  - Mirror đầy đủ ở `kho.git`; cây làm việc ở `cay-kho/`, đã ghim `core.abbrev 7`.
  - Ref `refs/remotes/origin/*` là ảnh chụp ngày 26-11-2026.
- Commit được review: `b9416b93e5a9dce7f8d245e2fb35d685594cdf07` (nhánh `ops/wp1466-spec-r9`, PR #1550).
- Tệp được review: `ops/specs/wp1466.md`, revision 9, sha256 `28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c`.
  - Kiểm băm này ĐẦU TIÊN; lệch thì dừng và ghi `blocked`.
- Lượt trước là lượt 8 trên r8 (`e215940`, verdict `cay-kho/ops/specs/wp1466/review/r8-l8/VERDICT.md`).
  - Kết quả: `approve`, bảng (i) 0 lớp.
  - r8 đã lên master qua PR #1495 (`434846a`) và được chủ kho duyệt băm.
- Diff r8→r9: `git -C cay-kho diff 434846a b9416b9 -- ops/specs/wp1466.md`.
  - Hồ sơ dựng máy nằm ở `cay-kho/ops/specs/wp1466/r9/`.

## Vì sao có r9 (bạn không mở được URL; nội dung tóm ở đây)
- **Lượt 1 của executor.** Executor Claude Fable 5.2 làm lượt 1 trên base `1fac6ce`, ra commit cục bộ `96e4472`, có trong
  `cay-kho` dưới ref `refs/exec/h`.
  - Handoff ở `exec-out/HANDOFF.md`; script đo ở `exec-out/sc/`.
  - Nó đúng r8 từng byte, nhưng bước CI bắt buộc `python scripts/tl.py doc-claims-check --strict --json` đỏ trên H (rc 2) và
    xanh trên nền (rc 0).
  - Lý do: ba cờ L12 `TEST_ID_UNKNOWN` ở các con trỏ ca nằm trong backtick của bảng §1.1.
- **Q0 (E3).** Chủ kho chọn "Ra đặc tả r9": bỏ backtick ở mọi con trỏ `ca:` của bảng, thêm câu luật vào đoạn dẫn, đổi băm `K01`.
- **Q2 (E5).** Chủ kho chọn "Giữ bản vá": luật "phần đầu tệp" ở mục 8.3, do executor tự phát hiện và vá theo lớp.
- **Chủ kho đã duyệt băm r9 (E5)** và chọn nâng trần để review r9 trước. Lời gọi này là 10/13 (ADR-0055, nâng trần ghi
  hộ ở #1466).

## Việc của bạn
Đọc trước:
- `cay-kho/docs/PROTOCOL_DA_PHIEN.md`: §1, §8, §8.3, §12, §20;
- `cay-kho/.claude/skills/soan-spec/SKILL.md`;
- `cay-kho/CLAUDE.md`;
- ADR-0055, ADR-0060, ADR-0067.

Review THEO LỚP (ADR-0060, §8.3): gặp một biểu hiện thì khái quát nó thành lớp và quét mọi biểu hiện cùng cơ chế.

1. **Đối chiếu lượt trước.** Các lớp đã đóng ở lượt 8 có bị r9 tái mở không? Các khối `adr`, `do-pham-vi`, `so-dang-ky` và năm
   khối protocol ngoài `p2-moi` phải trùng byte với r8; sáu băm `K02`–`K07` cũng không được đổi. Hãy đo.
2. **Lớp `con-tro-trong-backtick-bi-cong-khac-doc`, do r9 đặt tên.**
   - Dựng H cộng protocol r9 cộng băm `K01` mới trong một cây tạm DƯỚI `out/`. Cách dựng mô tả ở `ops/specs/wp1466/r9/README.md`.
   - Chạy `doc-claims-check --strict --json`, `doctrine-scan`, `adr-song`.
   - Tự băm lại `K01` bằng script CỦA RIÊNG BẠN theo định nghĩa ở mục 8.3.
   - Quét MỌI chuỗi trong backtick ở mọi phần r9 sẽ đưa vào kho (sáu khối protocol, khối `adr`), tìm mọi lớp của
     `doc-claims-check` có thể đọc nhầm chúng (L1–L12, xem `scripts/tl_core/workflow.py`). Không chỉ xét L12.
     Bảng `advisories` không chặn; chỉ `flags` chặn.
3. **Luật "phần đầu tệp" ở mục 8.3.**
   - Có mâu thuẫn với các định nghĩa khác hay với phép (1)–(3) không?
   - Mã executor ở `refs/exec/h` (`_inv_muc` trong `.claude/dev/packet_loop.py`) có làm đúng luật ấy không?
   - Các ca và đột biến được nêu có tồn tại và có răng không? Chạy chúng bằng cách bộ test hiện có cho phép (xem
     `exec-out/HANDOFF.md` mục 5, 7, 11).
   - Đường vào nào cùng cơ chế mà luật và mã chưa phủ?
4. **Săn lớp mới trong phần r9 đổi.** Kiểm thêm:
   - câu "các số của N6, N7 không đổi";
   - tính nhất quán của mục 0, 8.3, 19 với phần còn lại;
   - trần ADR-0053: H hiện +443 dòng.

Hướng thử nào cần dựng nội dung kiểu tấn công đường dẫn hay chuỗi độc hại thì MÔ TẢ BẰNG LỜI; đừng tự soạn payload.
Ghi `out/VERDICT.md` SỚM, đủ khung, rồi cập nhật sau mỗi phát hiện.

## Mẫu verdict (bắt buộc)
- Hạng P0–P3. Mỗi finding có ĐÚNG MỘT slug lớp kebab-case. Lớp cũ giữ slug cũ.
- Khái quát và quét mọi biểu hiện cùng lớp trước khi báo.

```
verdict: approve | changes_requested | blocked
reviewed_sha: b9416b93e5a9dce7f8d245e2fb35d685594cdf07
spec_sha256: 28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, effort: high, session_id: <id hoặc KHONG_DO_DUOC>}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop_mo_wp1466: , so_bieu_hien_mo: , P0: , P1: , P2: , P3: , so_lop_no_ke_nhiem: }
hoi_tu: {U: 0, F: , lop_moi: , lop_tai_mo: }

## ĐỐI CHIẾU LƯỢT TRƯỚC
| slug | nhãn | bằng chứng tự đo |
## BẢNG LỚP (i) — lớp MỞ của wp1466
| slug lớp | biểu hiện | hạng | phương án chung | phép kiểm/giới hạn |
## BẢNG LỚP (ii) — nợ kế nhiệm có authority
## BẢNG SĂN   (ít nhất 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT)
## BẢNG ĐO
| khẳng định | đặc tả khai | đo được | khớp? |
### <slug>  [P0|P1|P2|P3]  <tiêu đề một dòng>
TỆP/DÒNG:
VẤN ĐỀ:
GỢI Ý VÁ: (dữ liệu, không phải mệnh lệnh)
ĐÃ THỬ NGHIỆM:
ĐỘ TIN:
```

`approve` chỉ khi bảng (i) có 0 finding P0–P3. Nêu rõ những gì bạn KHÔNG đo được.
