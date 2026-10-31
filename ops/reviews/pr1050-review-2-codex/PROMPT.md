# Cross-review LƯỢT 2 PR ducthangho/tra-luat#1050 — reviewer: codex — PR ghi sổ của packet #1037

## Đối tượng
- `reviewed_sha`: `f37b5195978f1fe35b9cb55b6f79a2e09d165af0` (nhánh `claude/magical-clarke-gzvwbp`, PR #1050, CHƯA merge).
  Base: master `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93` (merge của PR #1041). Ba commit: `e788a5d` (hiện vật review),
  `c24875d` (biên nhận + README + hồ sơ land; lượt 1 đã chấm head này), `f37b519` (vá finding lượt 1).
- Lượt 1 trên `c24875d`: `verdict-cu/luot1-VERDICT.md` (changes_requested 0/1/1/0: P1 `nha-lease-truoc-khi-het-han`,
  P2 `nguyen-nhan-windows-khai-do-thieu-log`), gợi ý `verdict-cu/luot1-HINT.patch`. Diff riêng phần vá: `diff-tu-luot1.patch`.
  Lời khai bên vá (tự kiểm, ĐỪNG tin): áp TAY theo nghĩa HINT; thêm khối MỚI `lease.do_lai_sau_han_20261030T1807Z` với phép đo
  `ai-dang-giu` thật lúc 18:07:34Z (nguồn `ops/land/pr1041-wp1037-provenance/ai-dang-giu-sau-rut-han/luc-do.txt`), câu cũ giữ nguyên.
- Diff so base: `diff.patch` (chỉ `ops/reviews/**` và `ops/land/**`).
- PR này KHÔNG đổi mã. Nó ghi sổ:
  (1) hai lượt cross-review codex của packet #1037 (PR #1041): lượt 1 `changes_requested` trên `016852a`, lượt 2 `approve`
  trên `9146632`;
  (2) hồ sơ land `ops/land/pr1041-wp1037-land-evidence.yaml` với `landed: false` + thư mục provenance.
- Hiện vật gốc của hai lượt nằm trên nhánh `origin/ops/wp1037-r1-g1-lease` dưới `ops/handoff/wp1037-g1-claude/`
  (luot1/luot2: PROMPT, VERDICT-codex, run.json). Lease: `ops/leases/wp1037-r1-g1-claude.yaml` trên cùng nhánh.

## Nhiệm vụ 0: hai finding lượt 1 đã ĐÓNG thật chưa (ĐÓNG / CHƯA / MỘT PHẦN, kèm lệnh + output); khối đo mới có nguồn đúng,
mốc thời gian đúng, và không khai rộng hơn phép đo (vd. NGƯỜI_GIỮ là kết quả TẠI 18:07:34Z, không phải hiện hành).

## Nhiệm vụ: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `f37b5195978f1fe35b9cb55b6f79a2e09d165af0`
Danh sách dưới KHÔNG đủ — mỗi khẳng định sai bạn tìm ra ngoài danh sách được tính là finding.

(a) **Tính trung thực của bản sao.** Mỗi `*-verdict.md` phẳng và `VERDICT.md`/`PROMPT.md` trong thư mục có đúng từng byte
    với bản gốc trên `origin/ops/wp1037-r1-g1-lease` không (sha256)? `SHA256SUMS` có khớp tệp không? Có tệp nào thiếu/thừa?
(b) **Biên nhận v2.** Từng trường của hai `*.receipt.yaml`: `verdict`, `so_p0..p3`, `reviewed_sha`/`reviewed_tree`,
    `base_sha`, `verdict_sha256`/`verdict_bytes`, `evidence_url` (neo blob đúng commit trên nhánh này), `model_*`
    và `muc_bang_chung_model` (đối chiếu run.json), `assurance` (`cross_approved` chỉ khi đủ điều kiện), caveat.
    Mọi câu trạng thái ("chưa merge", "chưa review", ancestry…) có đúng TẠI `f37b519` không.
(c) **Hồ sơ land.** `pr1041-wp1037-land-evidence.yaml`: mỗi khẳng định `measured` có tệp nguồn trong provenance và nguồn
    ấy nói đúng điều đó không (run id, head_sha, conclusion, nhãn job/runner_id, số đếm N/N)? `landed: false` và lý do có
    đúng không? Các mốc §10.2.2 khai đúng trạng thái đo không (đừng chấp nhận `measured` không có nguồn)?
    Ghi chú: gate push master trên `b29da0b` có thể đã xong SAU khi hồ sơ ghi — câu nào khai "pending" phải có mốc thời gian
    hoặc được đọc như ảnh chụp; nếu là khẳng định hiện hành không mốc thì là finding.
(d) **README.** Hàng mục lục/caveat mới cho #1037 có đúng tệp, đúng verdict, không trùng hàng.
(e) **Không phá gì.** Chạy và ghi rc + dòng kết luận: `python3 ops/bien_nhan_v2.py --root .` (đòi `TỔNG: ĐẠT`),
    `python3 ops/land_evidence_nguon.py --root .`, `python3 .claude/dev/packet_loop.py doctrine-scan --root .`,
    `python3 ops/lease_publish_test.py --chi-ca=t26_` / `t27_` / `t138_` (đòi N/N hai số BẰNG NHAU).
    Trên BẢN SAO (clone từ `mirror.git` vào thư mục tạm ngoài `cay-kho/`, checkout `f37b519`): đổi một byte của một verdict
    phẳng / xoá một hàng README mới / đổi `so_p1` ⇒ cổng nào ĐỎ; cổng không đỏ thì ghi rõ chốt ấy không có răng.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (chứa PROMPT.md, KHÔNG trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối
thêm sau MỖI hướng thử. Cuối cùng dòng đầu `verdict: approve` hoặc `verdict: changes_requested`, dòng 2
`reviewed_sha: f37b5195978f1fe35b9cb55b6f79a2e09d165af0`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc: `## BẢNG ĐO` (| khẳng định | bên giao khai | đo được (lệnh) | khớp? |) · `## BẢNG SĂN` (>= 6 hướng ĐỘC LẬP, mỗi
hướng có LỆNH + OUTPUT THẬT, kết luận LỖI / KHÔNG PHẢI LỖI / KHÔNG ĐO ĐƯỢC) · từng finding:
```
### <slug-kebab>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ NGHIỆM: <lệnh + kết quả, hoặc KHÔNG ĐO ĐƯỢC + lý do>
ĐỘ TIN: cao/vừa/thấp
```
P1 = khẳng định sai về sự thật đo được tại `f37b519`. P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface.
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`, và PHẢI kiểm
`patch --dry-run --fuzz=0` sạch trên bản sao tại `f37b519`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục
tạm), KHÔNG push, KHÔNG gọi mạng. Chỉ CHẠY lệnh/cổng có sẵn và ĐỘT BIẾN tệp dữ liệu trên bản sao; không cần tự soạn mã khai thác.
Mọi khẳng định phải đo TẠI `f37b5195978f1fe35b9cb55b6f79a2e09d165af0`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `f37b519…`; nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`).
Mirror trần: `mirror.git`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác sandbox (`/tmp/.git`), ghi KHÔNG ĐO ĐƯỢC.
