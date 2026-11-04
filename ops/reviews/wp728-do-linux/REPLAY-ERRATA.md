# Đính chính cho `rig/REPLAY.md` — checkout của rig khác với mỏ neo nguồn

`rig/REPLAY.md` là hiện vật đóng băng: phiên điều phối viết nó TRƯỚC lượt đo (spec r2, mục hiện vật), và
`SHA256SUMS.txt` băm nó (`92a93d31…`). Vì vậy KHÔNG sửa tại chỗ; đính chính sống ở tệp này.

## Chỗ sai

Bảng biến của `REPLAY.md` ghi `R` là checkout *"detached ở `reviewed_sha`"* (`9fddb1d19e8e5b753bb687673846d484fb710182`),
rồi mục 2 chạy rig từ `$R/ops/reviews/wp728-do-linux/rig`. Nhưng tại `9fddb1d` **không có** thư mục
`ops/reviews/wp728-do-linux/` (đo: `git ls-tree -r --name-only 9fddb1d` không có `zombie_rig.py`), nên làm đúng chữ
thì lượt chạy lại dừng ở mục 2. Codex connector chỉ ra (P2, PR #764, comment `4438230702`).

## Cách đọc đúng — HAI revision, hai vai

| biến | revision | vai |
|---|---|---|
| `R` | `1e9d6993736d85897cd979808eaa77fe8a3e17ef` (tree `d9727454efdfaf12afdbc30a1d30b78144ef293d`) | checkout CHỨA rig; đúng là checkout lượt đo đã dùng (`VERDICT.md` dòng 11, `run.json` khoá `head`) |
| `RS` | `9fddb1d19e8e5b753bb687673846d484fb710182` (`reviewed_sha`) | mỏ neo NGUỒN sản phẩm; mục 1 xuất hai blob từ `"$RS:…"` như cũ |

`1e9d699` có `9fddb1d` là tổ tiên, nên mọi lệnh `git -C "$R" … "$RS:…"` của mục 1 chạy nguyên văn. Mọi phép đòi
blob/sha256 giữ nguyên, nên đổi chỗ lấy rig KHÔNG đổi byte sản phẩm được đo.

## Đã kiểm trên checkout sạch (02-11-2026)

Worktree mới detached ở `1e9d699`, chạy mục 1 và mục 2 nguyên văn của `REPLAY.md` với `R` như bảng trên:
- `merge-base --is-ancestor 8b59185… "$RS"` ⇒ `rc=0`;
- `rev-parse` hai blob ⇒ `24240a31…` và `4dc5994c…`; sha256 hai tệp xuất ra ⇒ `33d32769…` và `7f6e5636…` (đúng giá trị đòi);
- `zombie_rig.py selftest` ⇒ dòng cuối `selftest 8/8`, `rc=0`;
- sha256 `rig/zombie_rig.py` · `rig/mutate.py` · `rig/REPLAY.md` tại `1e9d699` khớp `SHA256SUMS.txt`
  (`0fee959f…` · `f4a965cc…` · `92a93d31…`).

Mục 0 (pwsh 7.4.6 từ tarball) và M1/M2 cần môi trường `E` nên KHÔNG chạy lại ở lượt kiểm này.
