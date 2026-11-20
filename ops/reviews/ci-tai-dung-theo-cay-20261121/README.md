# Hồ sơ review đặc tả Đ2 — `CI-TAI-DUNG-THEO-CAY` (lượt 1–5)

Thư mục này lưu năm verdict review đặc tả của Đ2 (tái dùng kết quả CI theo cây ở lượt `push` lên `master`), prompt lượt 5
và mọi bản nháp đặc tả đã đưa review. Nó là nguồn `vai: review` cho mục sổ `xet_lai_cach_lam` đăng trên PR #1320.
Nhánh này không merge.

**Trạng thái pháp lý của các tệp.**

- Mọi đặc tả ở `dac-ta-nhap/` là **bản nháp**: chưa bản nào được chủ kho duyệt băm.
- Năm verdict **không có** slug lớp cho từng finding, **không có** bảng lớp, và từ lượt 2 **không** đối chiếu theo bốn
  nhãn của protocol §8; prompt không đòi những thứ ấy. Theo §8.3 và nhắc của chủ kho ngày 21-11-2026, các verdict này
  **không dùng để vá hay approve**, kể cả kết luận "A r4 đạt" ở lượt 3–5. Chúng vẫn tính vào trần lời gọi Codex (5/10).
- Tệp giữ **nguyên byte** (dòng kết thúc CRLF như lúc review) để sha256 khớp số dẫn trong verdict và trong mục sổ.

| lượt | lời gọi Codex | đặc tả được review (sha256) | verdict (sha256) | kết luận |
|---|---|---|---|---|
| 1 | 1/10 | A r2 `3d878fed…`, B r2 `587e59cf…` (đối chiếu A r1 `b20b6081…`, B r1 `57ccbf1d…`) | `luot1/VERDICT.md` `8e2dc040…` | `changes_requested`, 1 P1, 6 P2, 3 P3 |
| 2 | 2/10 | A r3 `957c4bec…`, B1 r1 `fd24105a…`, B2 r1 `f705edcf…` | `luot2/VERDICT.md` `9cea1406…` | `changes_requested`, 7 P2, 3 P3 |
| 3 | 3/10 | A r4 `04007230…`, B1 r2 `940f6a2e…`, B2 r2 `17cfb8c2…` | `luot3/VERDICT.md` `9909c0bf…` | `changes_requested`, 6 P2, 3 P3 |
| 4 | 4/10 | A r4, B1 r3 `814dfcca…`, B2 r3 `a729dd7c…` | `luot4/VERDICT.md` `d3e4066f…` | `changes_requested`, 5 P2, 2 P3 |
| 5 | 5/10 | A r4, B1 r4 `bd7aa007…`, B2 r4 `21bdbd5c…` | `luot5/VERDICT.md` `6e4b7c6d…` | `changes_requested`, 5 P2, 3 P3 |

Reviewer: Codex CLI (`codex.exe` 0.167.0-alpha.3.2 đóng gói trong Codex Desktop), `-m gpt-6-astra`,
`model_reasoning_effort=xhigh`, `--disable memories` cùng các tính năng apps/browser/computer_use/plugins, sandbox
`workspace-write` trong `C:/r/d2`, không mạng. Gọi thẳng `codex exec`, **không** qua `.claude/dev/launcher.py run`, nên
không có receipt §8.1 (`run.json`, `stdout_sha256`); mỗi lượt chỉ có `events.jsonl`, `rc.txt` (cả năm `rc=0`). Một lần gọi
trước lượt 1 thoát rc 127 (không tìm thấy tệp chạy, chưa sinh output) nên không tính trần.

Hiện vật kèm verdict (`review-evidence/`, `thu/`, script `review_r*.py`, 1,5–2,4 MB mỗi lượt) nằm ở máy executor,
`C:/r/d2/luot1/out` … `luot5/out`; không đưa lên đây. Liên kết tương đối trong verdict trỏ tới các tệp ấy.
