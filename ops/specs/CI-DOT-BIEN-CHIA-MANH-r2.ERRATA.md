# Erratum — `CI-DOT-BIEN-CHIA-MANH-r2.md`

Spec r2 ĐÓNG BĂNG theo băm (sha256 `9a2ab4fe746330f87ef86cc9b9a2bef6da8edde6e198a1989d415827c9fb2783`,
blob `8e2408e39ffcee4588578fe98a3ebe947a6444ef`, commit `b6380bf`). Không sửa tệp ấy; đính chính sống ở đây.
Chủ kho duyệt ghi erratum sau land #664 (issue #661, 2026-09-27: "Đồng ý tất cả").

| chỗ | spec ghi | đo được | nguồn đo |
|---|---|---|---|
| §1, dòng `DOT_BIEN_TU_KIEM` tại `5c79fa2` | **185** mutant | **200** mục | Codex CLI lượt 2 và lượt 3 đếm AST từ Git blob tại `5c79fa2` và `68b552d` — cả hai 200 |
| §5 M2, ví dụ dòng in của `--gop` | `TU DOT BIEN: giet = 185 / 185` | số thật là độ dài bảng lúc chạy | A1 lấy N thực tế; trên head land (`dcfc34f`/`d42cdb3`) N = **239** |

Không ảnh hưởng nghiệm thu: A1 quy định "N = số mục bảng lúc đo, hai số BẰNG NHAU", và mọi phép gộp đã đo
dùng N thực tế. Chuỗi đúng: nền 200 → lượt 1 233 → lượt 2 237 → head 239. Codex lượt 3 phán quyết sai số này
không chặn W1–W3. Verdict gốc: `ops/reviews/ci-dot-bien-chia-manh-r2-review-{2,3}-codex-verdict.md` trên nhánh
`ops/cap-lease-ci-dot-bien-chia-manh` (commit `ec6f0dd`, `2911618`) — chưa vào master.
