# Cross-review PR ducthangho/tra-luat#1056 — reviewer: codex — PR ghi sổ hai lượt review của PR #1050

## Đối tượng
- `reviewed_sha`: `1aae17b5534f78767856f93f7d6089adda224f21` (nhánh `claude/pr1050-review-ghi-so`, PR #1056, CHƯA merge).
  Base: master `6db934145acf6e47d01db5b2dc8c9da417c2d8eb`. Hai commit: `7333f97` (hiện vật), `1aae17b` (biên nhận + README).
- Diff so base: `diff.patch` (đã loại các tệp `*.patch` lồng bên trong cho gọn), `numstat.txt` (180 tệp, +6714, chỉ `ops/reviews/**`).
- PR KHÔNG đổi mã. Nó ghi sổ hai lượt cross-review codex trên PR #1050 (PR ghi sổ của packet #1037, đã merge `79400f3`):
  - lượt 1 trên `c24875d`, launcher run `1b0ff763`: `changes_requested` 0/1/1/0;
  - lượt 2 trên `f37b519`, launcher run `8c095c6b`: `approve` 0/0/0/0.
- Người ghi sổ (executor của PR này) là phiên điều phối Claude `session_01WZT2MvvoQV8QGF1vX9STrJ` — CHÍNH phiên đã gọi hai lượt
  codex ấy (không viết verdict). Hãy soi kỹ chỗ người ghi sổ có thể tự khai thuận lợi cho mình.
- Nhánh `origin/claude/magical-clarke-gzvwbp` là nhánh của #1050 (để tra `c24875d`, `f37b519`).

## Nhiệm vụ: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `1aae17b5534f78767856f93f7d6089adda224f21`
Danh sách dưới KHÔNG đủ — mỗi khẳng định sai bạn tìm ra ngoài danh sách được tính là finding.

(a) **Nội tại hiện vật.** Mỗi thư mục `ops/reviews/pr1050-review-{1,2}-codex/`: `SHA256SUMS` khớp mọi tệp (không thiếu/thừa);
    `VERDICT.md` == verdict phẳng `pr1050-review-{n}-codex-verdict.md` từng byte; `run/run.json` có `head` = reviewed_sha,
    `prompt_sha256` = sha256 `PROMPT.md`, `ma_thoat`, `trang_thai`, `model_phuc_vu`, `effort_phuc_vu` đúng như biên nhận khai;
    `OMITTED.txt` khai đúng băm/bytes (tái lập `git diff b29da0b <reviewed_sha>` và so). `verdict-cu/` của lượt 2 == verdict/HINT lượt 1.
(b) **Biên nhận v2.** Từng trường của hai `*.receipt.yaml`: `verdict`, `so_p0..p3` (đối chiếu dòng 1–3 verdict), `reviewed_sha`/
    `reviewed_tree` (`git rev-parse X^{tree}`), `base_sha` (= merge-base của nhánh #1050 với master LÚC dựng sandbox — kiểm),
    `land_merge_commit` (79400f3 có đúng là merge #1050, cha thứ hai = f37b519), `evidence_url` (blob tại `7333f97` tồn tại, đúng
    byte), `assurance` (cross_approved chỉ cho lượt approve), `model_*`, `review_class` và lời biện minh, caveat. Mọi câu trạng
    thái có đúng TẠI `1aae17b` không.
(c) **README.** Hai hàng mục lục + sáu hàng cảnh báo mới: đúng tệp, đúng verdict/số đếm/run id/head/bytes, không trùng.
(d) **Không phá gì.** Chạy và ghi rc + dòng kết luận: `python3 ops/bien_nhan_v2.py --root .`, `python3 ops/land_evidence_nguon.py --root .`,
    `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, `python3 ops/lease_publish_test.py --chi-ca=t26_` / `t27_` / `t138_`
    (N/N hai số BẰNG NHAU). Trên BẢN SAO (clone từ `mirror.git` vào thư mục tạm ngoài `cay-kho/`): đổi một byte verdict phẳng / xoá
    một hàng README mới ⇒ cổng nào ĐỎ; cổng không đỏ thì ghi rõ chốt ấy không có răng.
(e) **Rò rỉ.** Hiện vật (run.json, stdout/stderr, evidence) có chứa token, khoá, đường dẫn credential hay nội dung bí mật không.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (chứa PROMPT.md, KHÔNG trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối
thêm sau MỖI hướng thử. Cuối cùng dòng đầu `verdict: approve` hoặc `verdict: changes_requested`, dòng 2
`reviewed_sha: 1aae17b5534f78767856f93f7d6089adda224f21`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc: `## BẢNG ĐO` (| khẳng định | bên giao khai | đo được (lệnh) | khớp? |) · `## BẢNG SĂN` (>= 6 hướng ĐỘC LẬP, mỗi
hướng có LỆNH + OUTPUT THẬT, kết luận LỖI / KHÔNG PHẢI LỖI / KHÔNG ĐO ĐƯỢC) · từng finding:
```
### <slug-kebab>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ NGHIỆM: <lệnh + kết quả, hoặc KHÔNG ĐO ĐƯỢC + lý do>
ĐỘ TIN: cao/vừa/thấp
```
P1 = khẳng định sai về sự thật đo được tại `1aae17b`. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface.
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`, và PHẢI kiểm
`patch --dry-run --fuzz=0` sạch trên bản sao tại `1aae17b`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục
tạm), KHÔNG push, KHÔNG gọi mạng. Chỉ CHẠY lệnh/cổng có sẵn và ĐỘT BIẾN tệp dữ liệu trên bản sao; không cần tự soạn mã khai thác.
Mọi khẳng định phải đo TẠI `1aae17b5534f78767856f93f7d6089adda224f21`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `1aae17b…`; nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`).
Mirror trần: `mirror.git`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác sandbox (`/tmp/.git`), ghi KHÔNG ĐO ĐƯỢC.
