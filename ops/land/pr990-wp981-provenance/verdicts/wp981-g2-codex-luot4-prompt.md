# Cross-review packet wp981 — lượt 4/4 (trần nâng 3→4, #981 issuecomment-6512475787), lớp sensitive, CHỈ ĐỌC

Bạn là REVIEWER độc lập (họ openai). Không mạng, không push, không sửa mã. Kết quả đưa vào hồ sơ land PR #1027 (§8.1).

## Đối tượng
- `reviewed_sha` = `0eb66e513f2736f0bfc342ddbcbc70b84f773b3b`, tree `04702940110da99d13068b5857f04cedc8d2c3ae`. Đây là head cuối của PR #990,
  đã merge vào master ở `e926bd9`.
- Đây là MERGE commit: cha 1 `afd3a861bdaed63ada0f24ee8dbf2af166e86178` (head lượt 3 đã approve), cha 2 `4488444` (origin/master lúc ấy).
  Write set gồm 2 tệp: `ops/kiem_ho_so_land.py`, `ops/kiem_ho_so_land_test.py`. Cả hai GIỐNG TỪNG BYTE `afd3a86` (và `2c70821`, bản lượt 2 approve).
  **110 tệp ngoài write set đã đổi** giữa `afd3a86` và `0eb66e5` (danh sách: `tep_master_mang_vao.txt`).
- Spec: `SPEC.md` = `ops/specs/wp981-r2.md`, sha256 `3d026415193d3f3b1ceef005cdc99fcc73871b0c7539697f82b4b0198f578079`. Tự băm lại.
- Verdict lượt 3 (trên `afd3a86`): `VERDICT_LUOT3.md`.

## Checkout — BẮT BUỘC CHỈ ĐỌC (bài học #996)
Checkout được review nằm ở `/home/user/wp981-rv4/cay-kho` (detached đúng `reviewed_sha`). Đường dẫn ấy nằm NGOÀI workspace của bạn.
- KHÔNG ghi gì vào đó: không chạy lệnh tạo tệp trong cây, không `git checkout`/`git stash`, không ghi rồi hoàn nguyên.
- Mọi fixture, scratch, cache, bytecode đặt NGOÀI cây, dưới thư mục hiện tại (`./evidence/`). Đặt `TMPDIR=$PWD/evidence/tmp`, `PYTHONDONTWRITEBYTECODE=1`,
  `PYTHONPYCACHEPREFIX=$PWD/evidence/pycache`, và dùng `python -B`.
- Chạy công cụ bằng đường dẫn tuyệt đối, cwd ở cây chỉ khi công cụ cần (`--root /home/user/wp981-rv4/cay-kho`).
- Đầu và cuối lượt: chụp `git -C <cây> rev-parse HEAD 'HEAD^{tree}'`, `git -C <cây> status --porcelain --untracked-files=all --ignored=matching`, `git -C <cây> ls-files -s | sha256sum`.
  Snapshot trước khi bạn chạy (do phiên điều phối đo): ls-files sha256 `9b8bfaf9a19b74a121940db6e3fea58bf369d7324e2287124c399bd5377575e6`, status 0 dòng.
  Verdict phải KHAI RÕ hai snapshot ấy và rằng checkout không bị ghi.

## Trọng tâm
1. Xác minh write set 2 tệp tại `reviewed_sha` giống từng byte `afd3a86` (blob OID + sha256). Merge không có sửa tay (`git diff-tree --cc`).
2. Chạy THẬT trên cây `0eb66e5`:
   - `python -B ops/kiem_ho_so_land_test.py` (kỳ vọng `N/N`);
   - `python -B ops/kiem_ho_so_land.py --root <cây>` và `--json`.
   Báo số hồ sơ landed và mọi dòng `TRUOT`/`LOI`.
3. Trong 110 tệp master mang vào, có tệp nào làm đổi kết quả của cổng không, đặc biệt mọi `ops/land/*-land-evidence.yaml` mới hoặc đổi.
   So kết quả từng hồ sơ giữa `afd3a86` và `0eb66e5`; dựng cây `afd3a86` bằng `git worktree`/`git archive` vào `./evidence/`, KHÔNG vào cây được review.
   Có tệp nào gọi, import hay phụ thuộc hành vi của `kiem_ho_so_land.py` không (`rg -n kiem_ho_so_land`)? Đổi hành vi thì đó có phải lỗi không?
4. Bảng SĂN ≥ 4 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT, kết luận `LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC`.

## Ghi kết quả
Ghi `VERDICT.md` ở thư mục hiện tại NGAY từ đầu (`verdict: dang_lam`) và cập nhật dần.
Kết thúc bằng `verdict: approve` | `changes_requested` | `blocked`. Dòng 2 là `reviewed_sha: 0eb66e513f2736f0bfc342ddbcbc70b84f773b3b` (đủ 40 ký tự).
Mỗi finding: `### <slug>  [P0|P1|P2|P3]  <tiêu đề>`, kèm TỆP/DÒNG, VẤN ĐỀ, ĐÃ THỬ NGHIỆM (lệnh + output), ĐỘ TIN.
Chỉ `approve` khi không còn P0/P1/P2. Viết bằng tiếng Việt.
