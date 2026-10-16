verdict: changes_requested
reviewed_sha: 3349c8b2e2b544ce98c2ea088e6c09d71b1092f0
reviewed_base: fe05fa6de0a151ced39261ccb97a88026cd1de91
reviewed_files_sha256:
  CHANGELOG.md: 830b049fd6737aeea726658c7ade11570e526efff4fa3aa1aaec3ea2dba8c653
  RELEASE_MANIFEST.json: b38d3d5dd1ca15daad1d0c31933cb3a64c58283666b33a175221780663048039
  ops/reviews/README.md: 7138f93e497de14c7123ed00971f342d812ccb1477d0c7777da2d1e0b8c64fc4
  ops/reviews/pr505-review-1-codex-verdict.md: a0bb40dc74b6029f0456bf18f61cc5a626669a3575a1a8c89347dd421b1eace9
  ops/reviews/pr505-review-1-codex-verdict.receipt.yaml: d04b00fe14ab7dda4ae2179573b3e5b8f076321dbe626cbfe11b0c9d5ac76dc5
  ops/reviews/pr505-review-10-codex-verdict.md: fea4c51180dc5e2e7c3e9532b1b817df1c55aaf0b0b2dbc536270b26c118f9b1
  ops/reviews/pr505-review-10-codex-verdict.receipt.yaml: f497cb527dbe88c77aaa69bce079ff53f48da45bbe5da628e7523e93c205f31c
  ops/reviews/pr505-review-2-codex-verdict.md: 13a0b829fa81f330a8989872b4d3df4ed9968f5f5c563d9baa2dc4912784c4fb
  ops/reviews/pr505-review-2-codex-verdict.receipt.yaml: ca66d737530bdf27268f2b78c9f83e45abdb25d696dd45f3732cdaa9d5ae7daa
  ops/reviews/pr505-review-3-codex-verdict.md: ebaff0d45b1c4eb0b2f15f92462f78cc311698c6e3fd479414d8099b6c751dde
  ops/reviews/pr505-review-3-codex-verdict.receipt.yaml: 7e4092dd26e076c335092529dc72aac614d181395893d7d931bb2184f4485c44
  ops/reviews/pr505-review-4-codex-verdict.md: 83ee3cd4c4d11059328d9a5002e8fdfabad78d961af5b790c49c3f9971f8795b
  ops/reviews/pr505-review-4-codex-verdict.receipt.yaml: 6eccd4d7d59c127dc96d4df200dde02c92af4b593379d80a181c647db91ad995
  ops/reviews/pr505-review-5-codex-verdict.md: e4e825726b4c1073fe875f198bc82bd794bfb96b3768a8eac8e95bb46ea13b88
  ops/reviews/pr505-review-5-codex-verdict.receipt.yaml: 270ad86e339fc12f470f93bf4460e89fff69cae3242dbadf226e25188c6b136d
  ops/reviews/pr505-review-6-codex-verdict.md: e7871b29012d78b95acd2a50f5f9551051efc3380cea80288d9caf3348db7f9d
  ops/reviews/pr505-review-6-codex-verdict.receipt.yaml: 1db71f22ab17d5cc868ef8019b723a625b796313f7e1cbc5f317ab0869809532
  ops/reviews/pr505-review-7-codex-verdict.md: 43b157ffe3f0b7092a303ffbc78629f27d3fb2cc6e3c95a3d3f937546b71fa88
  ops/reviews/pr505-review-7-codex-verdict.receipt.yaml: 1121c0356b323aa0ab809440624a41be79611016e219e9fd5d21ae323d16689e
  ops/reviews/pr505-review-8-codex-verdict.md: 50566f7c0110e471696f65032105c90c929f95b90208486022841b68355be922
  ops/reviews/pr505-review-8-codex-verdict.receipt.yaml: fd64e8ee0d266599bb935ed53711ca7ea0225d3c568ef54100e05e163407c6ba
  ops/reviews/pr505-review-9-codex-verdict.md: 8623f20bad8a67cc08558c26d63d0f026b6224d7f7a31f149dbd71170cdd22c1
  ops/reviews/pr505-review-9-codex-verdict.receipt.yaml: 9135ec16cdd56bf54b75880247c2e3e20392fd3d0bbf4f70f86af273217f7c3a
model_tu_khai: GPT-6 / Codex / OpenAI; tự khai, không chứng thực runtime build
review_round: 1
so_p1: 0
so_p2: 5
so_p3: 1
hint_sha256: 9212942dae3910a9e824126e2511b4d2e381a832c7197e7b0ddd14312b390df8

**CHANGES_REQUESTED — 0 P1, 5 P2 vá được trong PR, 1 P3.** Byte/băm, head, số finding từng receipt và các neo hiện tại đều đúng. Các lỗi cần vá nằm ở câu tổng hợp, ngoại lệ HINT lượt 1, nhãn nguồn transport, hướng dẫn xử lý cache và cách gọi mục nợ “rỗng”. Không có finding mã sản phẩm.

Đo hoàn toàn từ gói hiện tại. “CÓ theo nguồn” nghĩa là đối chiếu được với văn bản/log đã cấp, không nâng thành chứng thực sự kiện GitHub. Phép đếm mutant dưới đây là **đếm lại từng hàng bảng trong verdict**, không nhận công chạy lại mutant sản phẩm của 10 lượt. Kết quả chạy mới của lượt này được tách ở `## Mutant đã chạy`. Không dùng `EVIDENCE.md` để thay nội dung tại head.

## Bảng đo lại

### 1. Hình dạng PR, Git, manifest và cổng

| Khai | Đo | Khớp? |
|---|---|---|
| Head/base theo yêu cầu | 3349c8b2e2b544ce98c2ea088e6c09d71b1092f0 / fe05fa6de0a151ced39261ccb97a88026cd1de91 | CÓ |
| 3 commit 9dc8460 → fa09a48 → 3349c8b | 3349c8b2e2b544ce98c2ea088e6c09d71b1092f0 CHANGELOG r366 + RELEASE_MANIFEST.json tái sinh — ghi sổ #505 (packet #503 M9-FETCH-AUTH): 10 vòng review qua 4 generation, approve dưới điều kiện dừng, land fe05fa6; A3 đo trên PR hồ sơ này<br>fa09a4854b4ccb137d4d1878711981d0a46450c0 ops/reviews: 10 biên nhận v2 cho verdict PR #505 (packet #503 M9-FETCH-AUTH) + README: đoạn nguồn, 14 cảnh báo, 10 hàng mục lục<br>9dc8460f55a61b8b9670606a62f6db40905d851c ops/reviews: đưa NGUYÊN VĂN 10 verdict cross-review codex PR #505 (packet #503 M9-FETCH-AUTH, 4 generation) vào kho | CÓ |
| 23 tệp, +2955/−5 | 23 tệp; +2955/−5; không có tệp mã sản phẩm trong diff | CÓ |
| 10 verdict + 10 receipt + README + CHANGELOG + manifest | Danh sách 23 băm đầy đủ ở metadata đầu VERDICT | CÓ |
| README: 1 đoạn nguồn + 14 hàng caveat + 10 hàng mục lục, +26 dòng | 1 đoạn PR #505; 14 cặp id/verdict; 10 hàng mục lục; 1 dòng trống bổ sung = 26 | CÓ |
| CHANGELOG r366 = 109 dòng thêm | ["109", "0", "CHANGELOG.md"] | CÓ |
| Manifest: 5/5; file_count 180; total_bytes 8274413; VERSION 1.36.68 | release-verify strict ok=true; expected=checked=180; VERSION base=HEAD=1.36.68; tổng size trong manifest=8274413 | CÓ |
| Manifest package_hash/content_hash dd40b514… | dd40b514bbe47126519f784ca87ad0fd425b9baf56240d18a7fbb49cb836cde4; expected=current=full_tree, match=true | CÓ |
| Manifest CHANGELOG bytes/hash 979168 / 830b049f… | 979168 / 830b049fd6737aeea726658c7ade11570e526efff4fa3aa1aaec3ea2dba8c653 | CÓ |
| bien_nhan_v2: 79 ĐẠT, 11/11 legacy, 42 nợ, 0 vi phạm, 0 không đo, tổng132 | bien_nhan_v2: 79 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 132<br>TỔNG: ĐẠT; rc=0 | CÓ, chạy mới |
| t26/t27 QUA | {"t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi": {"rc": 0}, "t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc": {"rc": 0}} | CÓ, chạy mới |
| release-verify --strict --json ok, 180/180 | {"ok": true, "expected_file_count": 180, "checked_file_count": 180, "failed": [], "errors": [], "package_hash_match": true, "rc": 0} | CÓ, chạy mới |
| Suite 147/147 ở de49fa0 | Đếm 147 hàm @ca tại de49fa0, CA khi import HEAD=147. Không chạy lại toàn suite; phần 147 thành công của lịch sử là loại (c). | CÓ số ca; KHÔNG ĐO ĐƯỢC lại toàn bộ pass |
| actionlint 1.7.7 rc=0 trên workflow | Binary nguon/actionlint/actionlint -version=1.7.7; chạy workflow HEAD rc=0 (blob bằng de49fa0) | CÓ, chạy mới |
| ShellCheck 0.9.0 rc=0 mọi head; wrapper AL_VER=1.7.7 | Có trong mô tả verdict từng lượt; lượt này chỉ chạy actionlint và đếm ca, không lặp wrapper/ShellCheck riêng ở 10 head | KHÔNG ĐO ĐƯỢC lại toàn bộ; loại (c) |
| doc-claims-check strict ok / doctrine-scan sạch | Không chạy hai cổng này ở lượt 1; không đọc doctrine bị cấm | KHÔNG ĐO ĐƯỢC |
| Clone không nông, core.abbrev7, detached3349c8b, sạch | is-shallow-repository=false; core.abbrev=7; HEAD đúng; status --porcelain rỗng; diff --check rc=0 | CÓ |
| Workflow +11, test +69, tổng +80/−0 tại de49fa0 và mergefe05fa6 | 11	0	.github/workflows/ops-thu-hoi-admission.yml<br>69	0	ops/lease_publish_test.py; 2 files changed, 80 insertions(+) | CÓ |
| Workflow không đổi 62c299a→de49fa0; SHA184a54a6… | Cả 10 head có SHA256 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23; Git blob b6be81ea533e0c05506314d479c296ca21c65b3c | CÓ |
| “Đúng trần A4 ở MỌI head” | Head1=61, head2=79, head3–10=80 dòng thêm; đều không vượt80. Không coi câu này là khẳng định mọi head bằng80; HINT làm rõ. | CÓ theo nghĩa không vượt trần |
| Nhánh claude/m9-fetch-auth tuyến tính từ62c299a tới de49fa0 | 62c299a 27c413c<br>6254570 62c299a<br>c851f80 6254570<br>2b52173 c851f80<br>19337fa 2b52173<br>301aac8 19337fa<br>8726a1c 301aac8<br>81af1c9 8726a1c<br>3ae4f61 81af1c9<br>de49fa0 3ae4f61; tip ref=de49fa0d077a2a00e9f936240378979a8ebc080c | CÓ |
| de49fa0 cha thứ2 của fe05fa6; fa717ee cha thứ1 | fa717eec2de678cb28180eeddd23ac9a83951993 de49fa0d077a2a00e9f936240378979a8ebc080c | CÓ |
| fa717ee..fe05fa6: first-parent1, tất cả11=10 commit nhánh+merge | first-parent=1; all=11 | CÓ |
| 10 reviewed_base đều base_sha27c413c3 | merge-base(62c299a,fa717ee)=27c413c3e531800431cad9db4452d7236505a5a9; parent62c299a là base này. Không có lease gốc để chứng thực field base_sha của lease. | CÓ base Git; lease KHÔNG ĐO ĐƯỢC |
| git log --all --diff-filter=A đúng 1 commit9dc8460 | Đo riêng cả 10 đường verdict: mỗi đường chỉ 9dc8460f55a61b8b9670606a62f6db40905d851c | CÓ |
| 9dc8460 là tổ tiên HEAD | git merge-base --is-ancestor 9dc8460 HEAD rc=0; 10 blob tại neo băm khớp tệp | CÓ |
| Vững merge/ff, mất squash | Ba cây land có cùng tree: merge v2 rc=0, ff v2 rc=0, squash v2 rc=1/10 vi phạm; chi tiết mục Mutant | CÓ, chạy mới |
| Spec M9 b8200141… trên master qua#475 | b820014107023f818c23b19cbf515d9e74445e0e67cec154a0b2dc34a57a19ac; git show fa717ee:ops/specs/M9-FETCH-AUTH.md tồn tại | CÓ |
| 27 commit master sau base; thiếu ops/cong_cu.py trong lời nhắc cũ | 27 commit 27c413c3..4b5184e; danh sách diff có ops/cong_cu.py | CÓ |

| Khai | Đo | Khớp? |
|---|---|---|
| VERSION 1.36.68 “từ r336” | git log -S1.36.68 -- VERSION tìm commit 3dcdc6a: v1.36.68 — r336, ghi sổ đợt loại ops/ và .mcp.json khỏi kiểm kê gói | CÓ Git |
| Chênh docstring khi áp HINT 1 lên 62c299a rồi so 6254570 | Đếm newline toàn tệp: bản HEAD kế tiếp nhiều hơn đúng 6 dòng; bỏ đúng docstring bằng AST thì prefix/suffix byte bằng nhau | CÓ, đo mới |

### 2. Quét r365/r366/r367 trên toàn mirror

| Khai | Đo | Khớp? |
|---|---|---|
| 334 refs/remotes/origin/* hiện tại | 334 | CÓ |
| r365 trên mọi ref: đo lại | ["refs/remotes/origin/HEAD", "refs/remotes/origin/claude/handoff-tra-luat-repo-2ak5th", "refs/remotes/origin/claude/land-502-bookkeeping", "refs/remotes/origin/claude/land-503-bookkeeping", "refs/remotes/origin/claude/spec-thu-hoi-lease-va-cap-lai-20260907", "refs/remotes/origin/master"] | 6 ref (gồm origin/HEAD) |
| r366 có 1 ref trước khi dùng; master 0; r367 0 | Hiện tại r366 trên refs/remotes/origin/claude/land-493-bookkeeping-wip, refs/remotes/origin/claude/land-503-bookkeeping; master không có; r367 không có | CÓ master 0/r367 0; lịch sử KHÔNG ĐO ĐƯỢC |
| ls-remote 332=for-each-ref 332; thiếu cục bộ 0; lúc 11:2xZ | Không có snapshot/log ls-remote. Hiện tại 334 gồm 1 symbolic origin/HEAD và nhánh PR #510; bỏ hai ref này còn 332. Bỏ riêng nhánh PR #510, r366 chỉ còn land-493-bookkeeping-wip. Đây là đối chiếu snapshot, không phục dựng lịch sử ref. | KHÔNG ĐO ĐƯỢC lịch sử; số hiện tại tương thích |
| WIP land-493-bookkeeping-wip chưa merge | tip ff03118…; merge-base --is-ancestor tip origin/master rc=1; PR #493 land tại e82af37 dùng r360 trong CHANGELOG | CÓ Git |
| r359→r360 tiền lệ | git log có 7e236cf: đổi r359→r360 vì master đã chiếm số; việc nhánh WIP tương lai phải đổi số là hướng dẫn, không sự kiện đã xảy ra | CÓ nguồn Git; không suy tương lai |

### 3. Từng scalar, byte/băm và nguồn runtime của 10 receipt

Bảng sau ghi từng trường riêng cho từng lượt. `run.json` được so toàn object với `nguon/m9-runs.json`; băm log được tính từ bytes thật. `cmp`, `sha256sum`, `wc -c` cũng chạy riêng cho đủ 10 verdict. Không đọc các đường tuyệt đối được nhúng trong run.json.

| Khai | Đo | Khớp? |
|---|---|---|
| L1 cmp nguyên byte = True | True | CÓ |
| L1 verdict_sha256 = a0bb40dc74b6029f0456bf18f61cc5a626669a3575a1a8c89347dd421b1eace9 | a0bb40dc74b6029f0456bf18f61cc5a626669a3575a1a8c89347dd421b1eace9 | CÓ |
| L1 verdict_bytes = 21908 | 21908 | CÓ |
| L1 README byte = 21908 | 21908 | CÓ |
| L1 m9-runs.json toàn object = bằng run.json | bằng run.json | CÓ |
| L1 model_reviewer_identity.session_run_id = 28f02cda | 28f02cda | CÓ |
| L1 model_reviewer_identity.run_id_day_du = 28f02cda63fa46b0b2308fe210db81d0 | 28f02cda63fa46b0b2308fe210db81d0 | CÓ |
| L1 model_reviewer_identity.prompt_sha256 = b55a96a073a66cbb42b198cf069d7bda2a5a4b6b635f65e96e00b528d952dede | b55a96a073a66cbb42b198cf069d7bda2a5a4b6b635f65e96e00b528d952dede | CÓ |
| L1 model_reviewer_identity.bat_dau_utc = 2026-09-11T05:02:27.819202+00:00 | 2026-09-11T05:02:27.819202+00:00 | CÓ |
| L1 model_reviewer_identity.ket_thuc_utc = 2026-09-11T05:22:11.871367+00:00 | 2026-09-11T05:22:11.871367+00:00 | CÓ |
| L1 model_reviewer_identity.thoi_luong_giay = 1184.052 | 1184.052 | CÓ |
| L1 model_reviewer_identity.ma_thoat = 0 | 0 | CÓ |
| L1 model_reviewer_identity.trang_thai = xong | xong | CÓ |
| L1 model_reviewer_identity.stdout_byte = 324 | 324 | CÓ |
| L1 model_reviewer_identity.stdout_sha256 = 7afd944547cd1409ebd553304cb9a68d7533b5f05392d1950a0fb14368d69428 | 7afd944547cd1409ebd553304cb9a68d7533b5f05392d1950a0fb14368d69428 | CÓ |
| L1 model_reviewer_identity.stderr_byte = 272251 | 272251 | CÓ |
| L1 model_reviewer_identity.stderr_sha256 = 14833dab1378e45592d7bd959f6f6538b3de2a9edb53a2148c714a5e8a26914c | 14833dab1378e45592d7bd959f6f6538b3de2a9edb53a2148c714a5e8a26914c | CÓ |
| L1 stdout byte thật (receipt + run.json) = 324 | 324 | CÓ |
| L1 stdout sha256 thật (receipt + run.json) = 7afd944547cd1409ebd553304cb9a68d7533b5f05392d1950a0fb14368d69428 | 7afd944547cd1409ebd553304cb9a68d7533b5f05392d1950a0fb14368d69428 | CÓ |
| L1 stderr byte thật (receipt + run.json) = 272251 | 272251 | CÓ |
| L1 stderr sha256 thật (receipt + run.json) = 14833dab1378e45592d7bd959f6f6538b3de2a9edb53a2148c714a5e8a26914c | 14833dab1378e45592d7bd959f6f6538b3de2a9edb53a2148c714a5e8a26914c | CÓ |
| L1 prompt_sha256 / snapshot = b55a96a073a66cbb42b198cf069d7bda2a5a4b6b635f65e96e00b528d952dede | KHÔNG ĐO ĐƯỢC: gói không có prompt.snapshot | KHÔNG ĐO ĐƯỢC |
| L1 duration từ timestamps = 1184.052 | 1184.052 | CÓ |
| L1 README giây làm tròn = 1184 | 1184 | CÓ |
| L1 so_lan_chet_truoc_khi_xong = 0 | KHÔNG ĐO ĐƯỢC: không có khoá/lịch sử retry trong run.json; receipt đã nhãn attestation | KHÔNG ĐO ĐƯỢC |
| L1 model_yeu_cau = gpt-6-astra | gpt-6-astra trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L1 effort = xhigh | xhigh trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L1 head run.json / reviewed_sha = 62c299aa9674aade08263504399539eb60eb89b7 | 62c299aa9674aade08263504399539eb60eb89b7 | CÓ |
| L1 reviewed_sha trong verdict = 62c299aa9674aade08263504399539eb60eb89b7 | 62c299aa9674aade08263504399539eb60eb89b7 | CÓ |
| L1 reviewed_base trong verdict = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L1 verdict trong verdict = changes_requested | changes_requested | CÓ |
| L1 reviewed_base = base thật = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L1 so_p1 = 1 | 1 | CÓ |
| L1 so_p2 = 1 | 1 | CÓ |
| L1 so_p3 = 0 | 0 | CÓ |
| L1 findings_ids = ['t152-khong-do-header-hieu-luc', 't152-khong-khoa-dang-ky-mask'] | ['t152-khong-do-header-hieu-luc', 't152-khong-khoa-dang-ky-mask'] | CÓ |
| L1 lease_id = m9-fetch-auth-exec-1-claude-20260911 | m9-fetch-auth-exec-1-claude-20260911 theo phân bổ generation của verdict/prompt | CÓ nội bộ; lease cấp thật KHÔNG ĐO ĐƯỢC |
| L1 gen README = 1 | 1 | CÓ |
| L1 HINT sha256 = 9f3a5d4ca2b7ebc69e7a4d21a11eae062e96081a79ab7c14dc9554fb408f7437 | 9f3a5d4ca2b7ebc69e7a4d21a11eae062e96081a79ab7c14dc9554fb408f7437 | CÓ |
| L1 HINT bytes = 6177 | 6177 | CÓ |
| L1 worktree_sach = True | True | CÓ |
| L2 cmp nguyên byte = True | True | CÓ |
| L2 verdict_sha256 = 13a0b829fa81f330a8989872b4d3df4ed9968f5f5c563d9baa2dc4912784c4fb | 13a0b829fa81f330a8989872b4d3df4ed9968f5f5c563d9baa2dc4912784c4fb | CÓ |
| L2 verdict_bytes = 24840 | 24840 | CÓ |
| L2 README byte = 24840 | 24840 | CÓ |
| L2 m9-runs.json toàn object = bằng run.json | bằng run.json | CÓ |
| L2 model_reviewer_identity.session_run_id = 6b3e8525 | 6b3e8525 | CÓ |
| L2 model_reviewer_identity.run_id_day_du = 6b3e8525a7b448fd929b41955aa9b265 | 6b3e8525a7b448fd929b41955aa9b265 | CÓ |
| L2 model_reviewer_identity.prompt_sha256 = 79269905687d109095ffa820cea35e66d8538cb081d976738e7223f0acaf7140 | 79269905687d109095ffa820cea35e66d8538cb081d976738e7223f0acaf7140 | CÓ |
| L2 model_reviewer_identity.bat_dau_utc = 2026-09-11T05:28:06.170013+00:00 | 2026-09-11T05:28:06.170013+00:00 | CÓ |
| L2 model_reviewer_identity.ket_thuc_utc = 2026-09-11T05:41:40.060958+00:00 | 2026-09-11T05:41:40.060958+00:00 | CÓ |
| L2 model_reviewer_identity.thoi_luong_giay = 813.891 | 813.891 | CÓ |
| L2 model_reviewer_identity.ma_thoat = 0 | 0 | CÓ |
| L2 model_reviewer_identity.trang_thai = xong | xong | CÓ |
| L2 model_reviewer_identity.stdout_byte = 320 | 320 | CÓ |
| L2 model_reviewer_identity.stdout_sha256 = ad043d8285935c4f1e910994ce07a4ca7224f8d1dfe47febae69a9cdc8f8903e | ad043d8285935c4f1e910994ce07a4ca7224f8d1dfe47febae69a9cdc8f8903e | CÓ |
| L2 model_reviewer_identity.stderr_byte = 207404 | 207404 | CÓ |
| L2 model_reviewer_identity.stderr_sha256 = d621a60def44ad2201ac71fad025747d46cde90c3abead3f3abbd66a74311f23 | d621a60def44ad2201ac71fad025747d46cde90c3abead3f3abbd66a74311f23 | CÓ |
| L2 stdout byte thật (receipt + run.json) = 320 | 320 | CÓ |
| L2 stdout sha256 thật (receipt + run.json) = ad043d8285935c4f1e910994ce07a4ca7224f8d1dfe47febae69a9cdc8f8903e | ad043d8285935c4f1e910994ce07a4ca7224f8d1dfe47febae69a9cdc8f8903e | CÓ |
| L2 stderr byte thật (receipt + run.json) = 207404 | 207404 | CÓ |
| L2 stderr sha256 thật (receipt + run.json) = d621a60def44ad2201ac71fad025747d46cde90c3abead3f3abbd66a74311f23 | d621a60def44ad2201ac71fad025747d46cde90c3abead3f3abbd66a74311f23 | CÓ |
| L2 prompt_sha256 / snapshot = 79269905687d109095ffa820cea35e66d8538cb081d976738e7223f0acaf7140 | KHÔNG ĐO ĐƯỢC: gói không có prompt.snapshot | KHÔNG ĐO ĐƯỢC |
| L2 duration từ timestamps = 813.891 | 813.891 | CÓ |
| L2 README giây làm tròn = 814 | 814 | CÓ |
| L2 so_lan_chet_truoc_khi_xong = 0 | KHÔNG ĐO ĐƯỢC: không có khoá/lịch sử retry trong run.json; receipt đã nhãn attestation | KHÔNG ĐO ĐƯỢC |
| L2 model_yeu_cau = gpt-6-astra | gpt-6-astra trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L2 effort = xhigh | xhigh trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L2 head run.json / reviewed_sha = 6254570b0604b42f9474091b9818dba9cd2b8704 | 6254570b0604b42f9474091b9818dba9cd2b8704 | CÓ |
| L2 reviewed_sha trong verdict = 6254570b0604b42f9474091b9818dba9cd2b8704 | 6254570b0604b42f9474091b9818dba9cd2b8704 | CÓ |
| L2 reviewed_base trong verdict = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L2 verdict trong verdict = changes_requested | changes_requested | CÓ |
| L2 reviewed_base = base thật = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L2 so_p1 = 1 | 1 | CÓ |
| L2 so_p2 = 1 | 1 | CÓ |
| L2 so_p3 = 0 | 0 | CÓ |
| L2 findings_ids = ['t152-bo-sot-fetch-thu-hai', 't152-stub-khong-do-quyen-transport'] | ['t152-bo-sot-fetch-thu-hai', 't152-stub-khong-do-quyen-transport'] | CÓ |
| L2 lease_id = m9-fetch-auth-exec-1-claude-20260911 | m9-fetch-auth-exec-1-claude-20260911 theo phân bổ generation của verdict/prompt | CÓ nội bộ; lease cấp thật KHÔNG ĐO ĐƯỢC |
| L2 gen README = 1 | 1 | CÓ |
| L2 HINT sha256 = ebb87804eb7d1f4d8519aa671ccdbc1e6c5d5610d06f5cbf716d8a2331e3c2d8 | ebb87804eb7d1f4d8519aa671ccdbc1e6c5d5610d06f5cbf716d8a2331e3c2d8 | CÓ |
| L2 HINT bytes = 1032 | 1032 | CÓ |
| L2 worktree_sach = True | True | CÓ |
| L3 cmp nguyên byte = True | True | CÓ |
| L3 verdict_sha256 = ebaff0d45b1c4eb0b2f15f92462f78cc311698c6e3fd479414d8099b6c751dde | ebaff0d45b1c4eb0b2f15f92462f78cc311698c6e3fd479414d8099b6c751dde | CÓ |
| L3 verdict_bytes = 23512 | 23512 | CÓ |
| L3 README byte = 23512 | 23512 | CÓ |
| L3 m9-runs.json toàn object = bằng run.json | bằng run.json | CÓ |
| L3 model_reviewer_identity.session_run_id = 4024cfff | 4024cfff | CÓ |
| L3 model_reviewer_identity.run_id_day_du = 4024cfff9a1b4ff4b91db0c981cc0d9a | 4024cfff9a1b4ff4b91db0c981cc0d9a | CÓ |
| L3 model_reviewer_identity.prompt_sha256 = 24c380d0eade28f03b01699b02b580e21c0256fc1e8b03bd40d730fe06ed05ae | 24c380d0eade28f03b01699b02b580e21c0256fc1e8b03bd40d730fe06ed05ae | CÓ |
| L3 model_reviewer_identity.bat_dau_utc = 2026-09-11T06:04:06.060269+00:00 | 2026-09-11T06:04:06.060269+00:00 | CÓ |
| L3 model_reviewer_identity.ket_thuc_utc = 2026-09-11T06:20:41.317990+00:00 | 2026-09-11T06:20:41.317990+00:00 | CÓ |
| L3 model_reviewer_identity.thoi_luong_giay = 995.258 | 995.258 | CÓ |
| L3 model_reviewer_identity.ma_thoat = 0 | 0 | CÓ |
| L3 model_reviewer_identity.trang_thai = xong | xong | CÓ |
| L3 model_reviewer_identity.stdout_byte = 347 | 347 | CÓ |
| L3 model_reviewer_identity.stdout_sha256 = 03ce7257c3c81080b4b2f2a05be38b8fb1771280bbcf5e54a9731cf81ab2bbb0 | 03ce7257c3c81080b4b2f2a05be38b8fb1771280bbcf5e54a9731cf81ab2bbb0 | CÓ |
| L3 model_reviewer_identity.stderr_byte = 950234 | 950234 | CÓ |
| L3 model_reviewer_identity.stderr_sha256 = e80cec4d8a137be80222b7aeef0fb03254a4ab053bfece75b7f00b5aba237a65 | e80cec4d8a137be80222b7aeef0fb03254a4ab053bfece75b7f00b5aba237a65 | CÓ |
| L3 stdout byte thật (receipt + run.json) = 347 | 347 | CÓ |
| L3 stdout sha256 thật (receipt + run.json) = 03ce7257c3c81080b4b2f2a05be38b8fb1771280bbcf5e54a9731cf81ab2bbb0 | 03ce7257c3c81080b4b2f2a05be38b8fb1771280bbcf5e54a9731cf81ab2bbb0 | CÓ |
| L3 stderr byte thật (receipt + run.json) = 950234 | 950234 | CÓ |
| L3 stderr sha256 thật (receipt + run.json) = e80cec4d8a137be80222b7aeef0fb03254a4ab053bfece75b7f00b5aba237a65 | e80cec4d8a137be80222b7aeef0fb03254a4ab053bfece75b7f00b5aba237a65 | CÓ |
| L3 prompt_sha256 / snapshot = 24c380d0eade28f03b01699b02b580e21c0256fc1e8b03bd40d730fe06ed05ae | KHÔNG ĐO ĐƯỢC: gói không có prompt.snapshot | KHÔNG ĐO ĐƯỢC |
| L3 duration từ timestamps = 995.258 | 995.258 | CÓ |
| L3 README giây làm tròn = 995 | 995 | CÓ |
| L3 so_lan_chet_truoc_khi_xong = 0 | KHÔNG ĐO ĐƯỢC: không có khoá/lịch sử retry trong run.json; receipt đã nhãn attestation | KHÔNG ĐO ĐƯỢC |
| L3 model_yeu_cau = gpt-6-astra | gpt-6-astra trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L3 effort = xhigh | xhigh trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L3 head run.json / reviewed_sha = c851f8005c0493799df87f87e3e4d586e2746634 | c851f8005c0493799df87f87e3e4d586e2746634 | CÓ |
| L3 reviewed_sha trong verdict = c851f8005c0493799df87f87e3e4d586e2746634 | c851f8005c0493799df87f87e3e4d586e2746634 | CÓ |
| L3 reviewed_base trong verdict = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L3 verdict trong verdict = changes_requested | changes_requested | CÓ |
| L3 reviewed_base = base thật = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L3 so_p1 = 1 | 1 | CÓ |
| L3 so_p2 = 0 | 0 | CÓ |
| L3 so_p3 = 0 | 0 | CÓ |
| L3 findings_ids = ['t152-bo-qua-stderr-truoc-mask'] | ['t152-bo-qua-stderr-truoc-mask'] | CÓ |
| L3 lease_id = m9-fetch-auth-exec-1-claude-20260911 | m9-fetch-auth-exec-1-claude-20260911 theo phân bổ generation của verdict/prompt | CÓ nội bộ; lease cấp thật KHÔNG ĐO ĐƯỢC |
| L3 gen README = 1 | 1 | CÓ |
| L3 HINT sha256 = c4f7bcd97801cfd9a1090cba203743e4386b06ed369f4892b1a64d12f1dc5f7d | c4f7bcd97801cfd9a1090cba203743e4386b06ed369f4892b1a64d12f1dc5f7d | CÓ |
| L3 HINT bytes = 665 | 665 | CÓ |
| L3 worktree_sach = True | True | CÓ |
| L4 cmp nguyên byte = True | True | CÓ |
| L4 verdict_sha256 = 83ee3cd4c4d11059328d9a5002e8fdfabad78d961af5b790c49c3f9971f8795b | 83ee3cd4c4d11059328d9a5002e8fdfabad78d961af5b790c49c3f9971f8795b | CÓ |
| L4 verdict_bytes = 21141 | 21141 | CÓ |
| L4 README byte = 21141 | 21141 | CÓ |
| L4 m9-runs.json toàn object = bằng run.json | bằng run.json | CÓ |
| L4 model_reviewer_identity.session_run_id = c2bc3d98 | c2bc3d98 | CÓ |
| L4 model_reviewer_identity.run_id_day_du = c2bc3d98bdfa402f9f165db81220ccbf | c2bc3d98bdfa402f9f165db81220ccbf | CÓ |
| L4 model_reviewer_identity.prompt_sha256 = 229c60f9b0ad272eccdda7f2f47863d48541bb69982b3d94f2d9fec63289e7bf | 229c60f9b0ad272eccdda7f2f47863d48541bb69982b3d94f2d9fec63289e7bf | CÓ |
| L4 model_reviewer_identity.bat_dau_utc = 2026-09-11T06:47:31.511771+00:00 | 2026-09-11T06:47:31.511771+00:00 | CÓ |
| L4 model_reviewer_identity.ket_thuc_utc = 2026-09-11T07:02:09.554169+00:00 | 2026-09-11T07:02:09.554169+00:00 | CÓ |
| L4 model_reviewer_identity.thoi_luong_giay = 878.042 | 878.042 | CÓ |
| L4 model_reviewer_identity.ma_thoat = 0 | 0 | CÓ |
| L4 model_reviewer_identity.trang_thai = xong | xong | CÓ |
| L4 model_reviewer_identity.stdout_byte = 323 | 323 | CÓ |
| L4 model_reviewer_identity.stdout_sha256 = 164c922cf1c470e0046e6a8cd53375552a56269f38263da8b2161078ea26c260 | 164c922cf1c470e0046e6a8cd53375552a56269f38263da8b2161078ea26c260 | CÓ |
| L4 model_reviewer_identity.stderr_byte = 762836 | 762836 | CÓ |
| L4 model_reviewer_identity.stderr_sha256 = bf6f354411251bf529321bf76e26c6010d080bf6f2cb3dcf613b4c6bde62562c | bf6f354411251bf529321bf76e26c6010d080bf6f2cb3dcf613b4c6bde62562c | CÓ |
| L4 stdout byte thật (receipt + run.json) = 323 | 323 | CÓ |
| L4 stdout sha256 thật (receipt + run.json) = 164c922cf1c470e0046e6a8cd53375552a56269f38263da8b2161078ea26c260 | 164c922cf1c470e0046e6a8cd53375552a56269f38263da8b2161078ea26c260 | CÓ |
| L4 stderr byte thật (receipt + run.json) = 762836 | 762836 | CÓ |
| L4 stderr sha256 thật (receipt + run.json) = bf6f354411251bf529321bf76e26c6010d080bf6f2cb3dcf613b4c6bde62562c | bf6f354411251bf529321bf76e26c6010d080bf6f2cb3dcf613b4c6bde62562c | CÓ |
| L4 prompt_sha256 / snapshot = 229c60f9b0ad272eccdda7f2f47863d48541bb69982b3d94f2d9fec63289e7bf | KHÔNG ĐO ĐƯỢC: gói không có prompt.snapshot | KHÔNG ĐO ĐƯỢC |
| L4 duration từ timestamps = 878.042 | 878.042 | CÓ |
| L4 README giây làm tròn = 878 | 878 | CÓ |
| L4 so_lan_chet_truoc_khi_xong = 0 | KHÔNG ĐO ĐƯỢC: không có khoá/lịch sử retry trong run.json; receipt đã nhãn attestation | KHÔNG ĐO ĐƯỢC |
| L4 model_yeu_cau = gpt-6-astra | gpt-6-astra trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L4 effort = xhigh | xhigh trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L4 head run.json / reviewed_sha = 2b52173529365ea04c854c738a1578a97c55a65a | 2b52173529365ea04c854c738a1578a97c55a65a | CÓ |
| L4 reviewed_sha trong verdict = 2b52173529365ea04c854c738a1578a97c55a65a | 2b52173529365ea04c854c738a1578a97c55a65a | CÓ |
| L4 reviewed_base trong verdict = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L4 verdict trong verdict = changes_requested | changes_requested | CÓ |
| L4 reviewed_base = base thật = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L4 so_p1 = 1 | 1 | CÓ |
| L4 so_p2 = 0 | 0 | CÓ |
| L4 so_p3 = 0 | 0 | CÓ |
| L4 findings_ids = ['t152-bo-qua-co-shell-truoc-wf-blob'] | ['t152-bo-qua-co-shell-truoc-wf-blob'] | CÓ |
| L4 lease_id = m9-fetch-auth-exec-2-claude-20260911 | m9-fetch-auth-exec-2-claude-20260911 theo phân bổ generation của verdict/prompt | CÓ nội bộ; lease cấp thật KHÔNG ĐO ĐƯỢC |
| L4 gen README = 2 | 2 | CÓ |
| L4 HINT sha256 = a4057e4a80ac787bfde38ac8b9877498a85f0dbfb62d7e868aa148cf5c7635fc | a4057e4a80ac787bfde38ac8b9877498a85f0dbfb62d7e868aa148cf5c7635fc | CÓ |
| L4 HINT bytes = 4310 | 4310 | CÓ |
| L4 worktree_sach = True | True | CÓ |
| L5 cmp nguyên byte = True | True | CÓ |
| L5 verdict_sha256 = e4e825726b4c1073fe875f198bc82bd794bfb96b3768a8eac8e95bb46ea13b88 | e4e825726b4c1073fe875f198bc82bd794bfb96b3768a8eac8e95bb46ea13b88 | CÓ |
| L5 verdict_bytes = 21826 | 21826 | CÓ |
| L5 README byte = 21826 | 21826 | CÓ |
| L5 m9-runs.json toàn object = bằng run.json | bằng run.json | CÓ |
| L5 model_reviewer_identity.session_run_id = 885398ce | 885398ce | CÓ |
| L5 model_reviewer_identity.run_id_day_du = 885398cefaa74456a7f34daf677fcad8 | 885398cefaa74456a7f34daf677fcad8 | CÓ |
| L5 model_reviewer_identity.prompt_sha256 = 4b4bd36b022a32f3de59cc01185a6e71084413073083ef0ff0d49ac5ffc23da9 | 4b4bd36b022a32f3de59cc01185a6e71084413073083ef0ff0d49ac5ffc23da9 | CÓ |
| L5 model_reviewer_identity.bat_dau_utc = 2026-09-11T07:12:24.540961+00:00 | 2026-09-11T07:12:24.540961+00:00 | CÓ |
| L5 model_reviewer_identity.ket_thuc_utc = 2026-09-11T07:25:19.369995+00:00 | 2026-09-11T07:25:19.369995+00:00 | CÓ |
| L5 model_reviewer_identity.thoi_luong_giay = 774.829 | 774.829 | CÓ |
| L5 model_reviewer_identity.ma_thoat = 0 | 0 | CÓ |
| L5 model_reviewer_identity.trang_thai = xong | xong | CÓ |
| L5 model_reviewer_identity.stdout_byte = 395 | 395 | CÓ |
| L5 model_reviewer_identity.stdout_sha256 = e2729657f78b39f34386ff6a5469d7ae5977130b9fa6fc90668d69f4eef041c2 | e2729657f78b39f34386ff6a5469d7ae5977130b9fa6fc90668d69f4eef041c2 | CÓ |
| L5 model_reviewer_identity.stderr_byte = 279256 | 279256 | CÓ |
| L5 model_reviewer_identity.stderr_sha256 = 80a86f493eceb2d0a093690432b129af36a12ee4ffb259487713e008d2296f11 | 80a86f493eceb2d0a093690432b129af36a12ee4ffb259487713e008d2296f11 | CÓ |
| L5 stdout byte thật (receipt + run.json) = 395 | 395 | CÓ |
| L5 stdout sha256 thật (receipt + run.json) = e2729657f78b39f34386ff6a5469d7ae5977130b9fa6fc90668d69f4eef041c2 | e2729657f78b39f34386ff6a5469d7ae5977130b9fa6fc90668d69f4eef041c2 | CÓ |
| L5 stderr byte thật (receipt + run.json) = 279256 | 279256 | CÓ |
| L5 stderr sha256 thật (receipt + run.json) = 80a86f493eceb2d0a093690432b129af36a12ee4ffb259487713e008d2296f11 | 80a86f493eceb2d0a093690432b129af36a12ee4ffb259487713e008d2296f11 | CÓ |
| L5 prompt_sha256 / snapshot = 4b4bd36b022a32f3de59cc01185a6e71084413073083ef0ff0d49ac5ffc23da9 | KHÔNG ĐO ĐƯỢC: gói không có prompt.snapshot | KHÔNG ĐO ĐƯỢC |
| L5 duration từ timestamps = 774.829 | 774.829 | CÓ |
| L5 README giây làm tròn = 775 | 775 | CÓ |
| L5 so_lan_chet_truoc_khi_xong = 0 | KHÔNG ĐO ĐƯỢC: không có khoá/lịch sử retry trong run.json; receipt đã nhãn attestation | KHÔNG ĐO ĐƯỢC |
| L5 model_yeu_cau = gpt-6-astra | gpt-6-astra trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L5 effort = xhigh | xhigh trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L5 head run.json / reviewed_sha = 19337fad89ff7fdb47475105d7bdde6e910aedf0 | 19337fad89ff7fdb47475105d7bdde6e910aedf0 | CÓ |
| L5 reviewed_sha trong verdict = 19337fad89ff7fdb47475105d7bdde6e910aedf0 | 19337fad89ff7fdb47475105d7bdde6e910aedf0 | CÓ |
| L5 reviewed_base trong verdict = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L5 verdict trong verdict = changes_requested | changes_requested | CÓ |
| L5 reviewed_base = base thật = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L5 so_p1 = 0 | 0 | CÓ |
| L5 so_p2 = 1 | 1 | CÓ |
| L5 so_p3 = 0 | 0 | CÓ |
| L5 findings_ids = ['t152-fixture-ngan-bo-sot-base64-wrap'] | ['t152-fixture-ngan-bo-sot-base64-wrap'] | CÓ |
| L5 lease_id = m9-fetch-auth-exec-2-claude-20260911 | m9-fetch-auth-exec-2-claude-20260911 theo phân bổ generation của verdict/prompt | CÓ nội bộ; lease cấp thật KHÔNG ĐO ĐƯỢC |
| L5 gen README = 2 | 2 | CÓ |
| L5 HINT sha256 = 27b2cc7f89235ec1f818e6a44e9d9362222d18c17abc612ba85880dcf15edbd1 | 27b2cc7f89235ec1f818e6a44e9d9362222d18c17abc612ba85880dcf15edbd1 | CÓ |
| L5 HINT bytes = 533 | 533 | CÓ |
| L5 worktree_sach = True | True | CÓ |
| L6 cmp nguyên byte = True | True | CÓ |
| L6 verdict_sha256 = e7871b29012d78b95acd2a50f5f9551051efc3380cea80288d9caf3348db7f9d | e7871b29012d78b95acd2a50f5f9551051efc3380cea80288d9caf3348db7f9d | CÓ |
| L6 verdict_bytes = 23397 | 23397 | CÓ |
| L6 README byte = 23397 | 23397 | CÓ |
| L6 m9-runs.json toàn object = bằng run.json | bằng run.json | CÓ |
| L6 model_reviewer_identity.session_run_id = 47b042b7 | 47b042b7 | CÓ |
| L6 model_reviewer_identity.run_id_day_du = 47b042b70177409ca185ae1d5eeddd36 | 47b042b70177409ca185ae1d5eeddd36 | CÓ |
| L6 model_reviewer_identity.prompt_sha256 = 9a587c21d19b3a833a0362b0e4832cc1951e554f4082094a25e600340bcfbfb2 | 9a587c21d19b3a833a0362b0e4832cc1951e554f4082094a25e600340bcfbfb2 | CÓ |
| L6 model_reviewer_identity.bat_dau_utc = 2026-09-11T08:27:15.935407+00:00 | 2026-09-11T08:27:15.935407+00:00 | CÓ |
| L6 model_reviewer_identity.ket_thuc_utc = 2026-09-11T08:42:06.561505+00:00 | 2026-09-11T08:42:06.561505+00:00 | CÓ |
| L6 model_reviewer_identity.thoi_luong_giay = 890.626 | 890.626 | CÓ |
| L6 model_reviewer_identity.ma_thoat = 0 | 0 | CÓ |
| L6 model_reviewer_identity.trang_thai = xong | xong | CÓ |
| L6 model_reviewer_identity.stdout_byte = 488 | 488 | CÓ |
| L6 model_reviewer_identity.stdout_sha256 = 52d1d096753a8ca129f2293a9bdd7ac3f5661ff6c508c71a40d0033dad96125c | 52d1d096753a8ca129f2293a9bdd7ac3f5661ff6c508c71a40d0033dad96125c | CÓ |
| L6 model_reviewer_identity.stderr_byte = 705878 | 705878 | CÓ |
| L6 model_reviewer_identity.stderr_sha256 = 3bdbcc56dd915e5239ae16c3ee2126e2d17ae26781eb3ab8dd39caf4bd01bb3d | 3bdbcc56dd915e5239ae16c3ee2126e2d17ae26781eb3ab8dd39caf4bd01bb3d | CÓ |
| L6 stdout byte thật (receipt + run.json) = 488 | 488 | CÓ |
| L6 stdout sha256 thật (receipt + run.json) = 52d1d096753a8ca129f2293a9bdd7ac3f5661ff6c508c71a40d0033dad96125c | 52d1d096753a8ca129f2293a9bdd7ac3f5661ff6c508c71a40d0033dad96125c | CÓ |
| L6 stderr byte thật (receipt + run.json) = 705878 | 705878 | CÓ |
| L6 stderr sha256 thật (receipt + run.json) = 3bdbcc56dd915e5239ae16c3ee2126e2d17ae26781eb3ab8dd39caf4bd01bb3d | 3bdbcc56dd915e5239ae16c3ee2126e2d17ae26781eb3ab8dd39caf4bd01bb3d | CÓ |
| L6 prompt_sha256 / snapshot = 9a587c21d19b3a833a0362b0e4832cc1951e554f4082094a25e600340bcfbfb2 | KHÔNG ĐO ĐƯỢC: gói không có prompt.snapshot | KHÔNG ĐO ĐƯỢC |
| L6 duration từ timestamps = 890.626 | 890.626 | CÓ |
| L6 README giây làm tròn = 891 | 891 | CÓ |
| L6 so_lan_chet_truoc_khi_xong = 0 | KHÔNG ĐO ĐƯỢC: không có khoá/lịch sử retry trong run.json; receipt đã nhãn attestation | KHÔNG ĐO ĐƯỢC |
| L6 model_yeu_cau = gpt-6-astra | gpt-6-astra trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L6 effort = xhigh | xhigh trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L6 head run.json / reviewed_sha = 301aac8e09b2195e0a8e53426d302c910b2a2484 | 301aac8e09b2195e0a8e53426d302c910b2a2484 | CÓ |
| L6 reviewed_sha trong verdict = 301aac8e09b2195e0a8e53426d302c910b2a2484 | 301aac8e09b2195e0a8e53426d302c910b2a2484 | CÓ |
| L6 reviewed_base trong verdict = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L6 verdict trong verdict = changes_requested | changes_requested | CÓ |
| L6 reviewed_base = base thật = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L6 so_p1 = 0 | 0 | CÓ |
| L6 so_p2 = 1 | 1 | CÓ |
| L6 so_p3 = 0 | 0 | CÓ |
| L6 findings_ids = ['t152-fixture-mat-nhanh-padding-base64'] | ['t152-fixture-mat-nhanh-padding-base64'] | CÓ |
| L6 lease_id = m9-fetch-auth-exec-2-claude-20260911 | m9-fetch-auth-exec-2-claude-20260911 theo phân bổ generation của verdict/prompt | CÓ nội bộ; lease cấp thật KHÔNG ĐO ĐƯỢC |
| L6 gen README = 2 | 2 | CÓ |
| L6 HINT sha256 = a7b0abc6cab235abaedf50cd2d692155074a484404df343cdb821b94c644f7f5 | a7b0abc6cab235abaedf50cd2d692155074a484404df343cdb821b94c644f7f5 | CÓ |
| L6 HINT bytes = 3198 | 3198 | CÓ |
| L6 worktree_sach = True | True | CÓ |
| L7 cmp nguyên byte = True | True | CÓ |
| L7 verdict_sha256 = 43b157ffe3f0b7092a303ffbc78629f27d3fb2cc6e3c95a3d3f937546b71fa88 | 43b157ffe3f0b7092a303ffbc78629f27d3fb2cc6e3c95a3d3f937546b71fa88 | CÓ |
| L7 verdict_bytes = 23679 | 23679 | CÓ |
| L7 README byte = 23679 | 23679 | CÓ |
| L7 m9-runs.json toàn object = bằng run.json | bằng run.json | CÓ |
| L7 model_reviewer_identity.session_run_id = 7f38b236 | 7f38b236 | CÓ |
| L7 model_reviewer_identity.run_id_day_du = 7f38b236796440d2ae31d6d280f4d53d | 7f38b236796440d2ae31d6d280f4d53d | CÓ |
| L7 model_reviewer_identity.prompt_sha256 = ab5419c659d71ad60678e17e7ba360418f5f4c11977c7db548fbf2c6aa4bace2 | ab5419c659d71ad60678e17e7ba360418f5f4c11977c7db548fbf2c6aa4bace2 | CÓ |
| L7 model_reviewer_identity.bat_dau_utc = 2026-09-11T09:08:53.591511+00:00 | 2026-09-11T09:08:53.591511+00:00 | CÓ |
| L7 model_reviewer_identity.ket_thuc_utc = 2026-09-11T09:23:20.808140+00:00 | 2026-09-11T09:23:20.808140+00:00 | CÓ |
| L7 model_reviewer_identity.thoi_luong_giay = 867.217 | 867.217 | CÓ |
| L7 model_reviewer_identity.ma_thoat = 0 | 0 | CÓ |
| L7 model_reviewer_identity.trang_thai = xong | xong | CÓ |
| L7 model_reviewer_identity.stdout_byte = 340 | 340 | CÓ |
| L7 model_reviewer_identity.stdout_sha256 = 548a3167cb1741ce5ae101caa32f7a89fb47baab2338e3457b2f954eeaae97b6 | 548a3167cb1741ce5ae101caa32f7a89fb47baab2338e3457b2f954eeaae97b6 | CÓ |
| L7 model_reviewer_identity.stderr_byte = 267316 | 267316 | CÓ |
| L7 model_reviewer_identity.stderr_sha256 = 1c77c9d2c9f2bef5f90cbf06aeac88678a6169605b1fb1d4f89858392c0d7450 | 1c77c9d2c9f2bef5f90cbf06aeac88678a6169605b1fb1d4f89858392c0d7450 | CÓ |
| L7 stdout byte thật (receipt + run.json) = 340 | 340 | CÓ |
| L7 stdout sha256 thật (receipt + run.json) = 548a3167cb1741ce5ae101caa32f7a89fb47baab2338e3457b2f954eeaae97b6 | 548a3167cb1741ce5ae101caa32f7a89fb47baab2338e3457b2f954eeaae97b6 | CÓ |
| L7 stderr byte thật (receipt + run.json) = 267316 | 267316 | CÓ |
| L7 stderr sha256 thật (receipt + run.json) = 1c77c9d2c9f2bef5f90cbf06aeac88678a6169605b1fb1d4f89858392c0d7450 | 1c77c9d2c9f2bef5f90cbf06aeac88678a6169605b1fb1d4f89858392c0d7450 | CÓ |
| L7 prompt_sha256 / snapshot = ab5419c659d71ad60678e17e7ba360418f5f4c11977c7db548fbf2c6aa4bace2 | KHÔNG ĐO ĐƯỢC: gói không có prompt.snapshot | KHÔNG ĐO ĐƯỢC |
| L7 duration từ timestamps = 867.217 | 867.217 | CÓ |
| L7 README giây làm tròn = 867 | 867 | CÓ |
| L7 so_lan_chet_truoc_khi_xong = 0 | KHÔNG ĐO ĐƯỢC: không có khoá/lịch sử retry trong run.json; receipt đã nhãn attestation | KHÔNG ĐO ĐƯỢC |
| L7 model_yeu_cau = gpt-6-astra | gpt-6-astra trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L7 effort = xhigh | xhigh trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L7 head run.json / reviewed_sha = 8726a1c91ac913da041ed021cc787c71ab57ffc6 | 8726a1c91ac913da041ed021cc787c71ab57ffc6 | CÓ |
| L7 reviewed_sha trong verdict = 8726a1c91ac913da041ed021cc787c71ab57ffc6 | 8726a1c91ac913da041ed021cc787c71ab57ffc6 | CÓ |
| L7 reviewed_base trong verdict = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L7 verdict trong verdict = changes_requested | changes_requested | CÓ |
| L7 reviewed_base = base thật = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L7 so_p1 = 0 | 0 | CÓ |
| L7 so_p2 = 1 | 1 | CÓ |
| L7 so_p3 = 0 | 0 | CÓ |
| L7 findings_ids = ['t152-khong-khoa-nguon-token-trong-env'] | ['t152-khong-khoa-nguon-token-trong-env'] | CÓ |
| L7 lease_id = m9-fetch-auth-exec-3-claude-20260911 | m9-fetch-auth-exec-3-claude-20260911 theo phân bổ generation của verdict/prompt | CÓ nội bộ; lease cấp thật KHÔNG ĐO ĐƯỢC |
| L7 gen README = 3 | 3 | CÓ |
| L7 HINT sha256 = b9e367abeec69f95296265d870b0aa4c90999c373279834ea8a0739f0eb27e53 | b9e367abeec69f95296265d870b0aa4c90999c373279834ea8a0739f0eb27e53 | CÓ |
| L7 HINT bytes = 2090 | 2090 | CÓ |
| L7 worktree_sach = True | True | CÓ |
| L8 cmp nguyên byte = True | True | CÓ |
| L8 verdict_sha256 = 50566f7c0110e471696f65032105c90c929f95b90208486022841b68355be922 | 50566f7c0110e471696f65032105c90c929f95b90208486022841b68355be922 | CÓ |
| L8 verdict_bytes = 22488 | 22488 | CÓ |
| L8 README byte = 22488 | 22488 | CÓ |
| L8 m9-runs.json toàn object = bằng run.json | bằng run.json | CÓ |
| L8 model_reviewer_identity.session_run_id = 6b6e237b | 6b6e237b | CÓ |
| L8 model_reviewer_identity.run_id_day_du = 6b6e237b9ddc4f3b8a620a2efdf3b0c0 | 6b6e237b9ddc4f3b8a620a2efdf3b0c0 | CÓ |
| L8 model_reviewer_identity.prompt_sha256 = 0191a98a1fdb7bc0614ec723ad8267a347bf899091aa9f7a58f4d5f7042ed21f | 0191a98a1fdb7bc0614ec723ad8267a347bf899091aa9f7a58f4d5f7042ed21f | CÓ |
| L8 model_reviewer_identity.bat_dau_utc = 2026-09-11T09:27:16.004734+00:00 | 2026-09-11T09:27:16.004734+00:00 | CÓ |
| L8 model_reviewer_identity.ket_thuc_utc = 2026-09-11T09:43:47.246161+00:00 | 2026-09-11T09:43:47.246161+00:00 | CÓ |
| L8 model_reviewer_identity.thoi_luong_giay = 991.241 | 991.241 | CÓ |
| L8 model_reviewer_identity.ma_thoat = 0 | 0 | CÓ |
| L8 model_reviewer_identity.trang_thai = xong | xong | CÓ |
| L8 model_reviewer_identity.stdout_byte = 356 | 356 | CÓ |
| L8 model_reviewer_identity.stdout_sha256 = db143303c7b945fe53a6076ff6f5a6c88ddc3ee4c1f34c27b36217d80c1b538d | db143303c7b945fe53a6076ff6f5a6c88ddc3ee4c1f34c27b36217d80c1b538d | CÓ |
| L8 model_reviewer_identity.stderr_byte = 683782 | 683782 | CÓ |
| L8 model_reviewer_identity.stderr_sha256 = a58a14f5ebcb2fc492f34d8ef3b6e8da3f10337dd57c63e477e230dba09a7968 | a58a14f5ebcb2fc492f34d8ef3b6e8da3f10337dd57c63e477e230dba09a7968 | CÓ |
| L8 stdout byte thật (receipt + run.json) = 356 | 356 | CÓ |
| L8 stdout sha256 thật (receipt + run.json) = db143303c7b945fe53a6076ff6f5a6c88ddc3ee4c1f34c27b36217d80c1b538d | db143303c7b945fe53a6076ff6f5a6c88ddc3ee4c1f34c27b36217d80c1b538d | CÓ |
| L8 stderr byte thật (receipt + run.json) = 683782 | 683782 | CÓ |
| L8 stderr sha256 thật (receipt + run.json) = a58a14f5ebcb2fc492f34d8ef3b6e8da3f10337dd57c63e477e230dba09a7968 | a58a14f5ebcb2fc492f34d8ef3b6e8da3f10337dd57c63e477e230dba09a7968 | CÓ |
| L8 prompt_sha256 / snapshot = 0191a98a1fdb7bc0614ec723ad8267a347bf899091aa9f7a58f4d5f7042ed21f | KHÔNG ĐO ĐƯỢC: gói không có prompt.snapshot | KHÔNG ĐO ĐƯỢC |
| L8 duration từ timestamps = 991.241 | 991.241 | CÓ |
| L8 README giây làm tròn = 991 | 991 | CÓ |
| L8 so_lan_chet_truoc_khi_xong = 0 | KHÔNG ĐO ĐƯỢC: không có khoá/lịch sử retry trong run.json; receipt đã nhãn attestation | KHÔNG ĐO ĐƯỢC |
| L8 model_yeu_cau = gpt-6-astra | gpt-6-astra trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L8 effort = xhigh | xhigh trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L8 head run.json / reviewed_sha = 81af1c90f21e7a7d861200f3a18b3707e0879162 | 81af1c90f21e7a7d861200f3a18b3707e0879162 | CÓ |
| L8 reviewed_sha trong verdict = 81af1c90f21e7a7d861200f3a18b3707e0879162 | 81af1c90f21e7a7d861200f3a18b3707e0879162 | CÓ |
| L8 reviewed_base trong verdict = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L8 verdict trong verdict = changes_requested | changes_requested | CÓ |
| L8 reviewed_base = base thật = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L8 so_p1 = 0 | 0 | CÓ |
| L8 so_p2 = 1 | 1 | CÓ |
| L8 so_p3 = 0 | 0 | CÓ |
| L8 findings_ids = ['t152-bo-sot-header-env-con-sau-fetch'] | ['t152-bo-sot-header-env-con-sau-fetch'] | CÓ |
| L8 lease_id = m9-fetch-auth-exec-3-claude-20260911 | m9-fetch-auth-exec-3-claude-20260911 theo phân bổ generation của verdict/prompt | CÓ nội bộ; lease cấp thật KHÔNG ĐO ĐƯỢC |
| L8 gen README = 3 | 3 | CÓ |
| L8 HINT sha256 = 86968dcdf6fd06676455998050b8690f663c9acbcbbf68f57eb72d150be0697a | 86968dcdf6fd06676455998050b8690f663c9acbcbbf68f57eb72d150be0697a | CÓ |
| L8 HINT bytes = 847 | 847 | CÓ |
| L8 worktree_sach = True | True | CÓ |
| L9 cmp nguyên byte = True | True | CÓ |
| L9 verdict_sha256 = 8623f20bad8a67cc08558c26d63d0f026b6224d7f7a31f149dbd71170cdd22c1 | 8623f20bad8a67cc08558c26d63d0f026b6224d7f7a31f149dbd71170cdd22c1 | CÓ |
| L9 verdict_bytes = 23860 | 23860 | CÓ |
| L9 README byte = 23860 | 23860 | CÓ |
| L9 m9-runs.json toàn object = bằng run.json | bằng run.json | CÓ |
| L9 model_reviewer_identity.session_run_id = 1f427b9d | 1f427b9d | CÓ |
| L9 model_reviewer_identity.run_id_day_du = 1f427b9d8b07428d9effcb368121ce0b | 1f427b9d8b07428d9effcb368121ce0b | CÓ |
| L9 model_reviewer_identity.prompt_sha256 = a3e406b7ac786368a356e8776a9398855188b78ff7a5e8445d652b9c65ba4bc2 | a3e406b7ac786368a356e8776a9398855188b78ff7a5e8445d652b9c65ba4bc2 | CÓ |
| L9 model_reviewer_identity.bat_dau_utc = 2026-09-11T09:47:42.295652+00:00 | 2026-09-11T09:47:42.295652+00:00 | CÓ |
| L9 model_reviewer_identity.ket_thuc_utc = 2026-09-11T10:03:51.142136+00:00 | 2026-09-11T10:03:51.142136+00:00 | CÓ |
| L9 model_reviewer_identity.thoi_luong_giay = 968.846 | 968.846 | CÓ |
| L9 model_reviewer_identity.ma_thoat = 0 | 0 | CÓ |
| L9 model_reviewer_identity.trang_thai = xong | xong | CÓ |
| L9 model_reviewer_identity.stdout_byte = 332 | 332 | CÓ |
| L9 model_reviewer_identity.stdout_sha256 = 190efce7826e89c86f5a992672dd66de17a1bb57827fc6725e3eb2d82971f990 | 190efce7826e89c86f5a992672dd66de17a1bb57827fc6725e3eb2d82971f990 | CÓ |
| L9 model_reviewer_identity.stderr_byte = 653408 | 653408 | CÓ |
| L9 model_reviewer_identity.stderr_sha256 = 5e32ba7de0e4708fc8792bc42170c9d487980e2e0562964356e7b1ae8be4b2f9 | 5e32ba7de0e4708fc8792bc42170c9d487980e2e0562964356e7b1ae8be4b2f9 | CÓ |
| L9 stdout byte thật (receipt + run.json) = 332 | 332 | CÓ |
| L9 stdout sha256 thật (receipt + run.json) = 190efce7826e89c86f5a992672dd66de17a1bb57827fc6725e3eb2d82971f990 | 190efce7826e89c86f5a992672dd66de17a1bb57827fc6725e3eb2d82971f990 | CÓ |
| L9 stderr byte thật (receipt + run.json) = 653408 | 653408 | CÓ |
| L9 stderr sha256 thật (receipt + run.json) = 5e32ba7de0e4708fc8792bc42170c9d487980e2e0562964356e7b1ae8be4b2f9 | 5e32ba7de0e4708fc8792bc42170c9d487980e2e0562964356e7b1ae8be4b2f9 | CÓ |
| L9 prompt_sha256 / snapshot = a3e406b7ac786368a356e8776a9398855188b78ff7a5e8445d652b9c65ba4bc2 | KHÔNG ĐO ĐƯỢC: gói không có prompt.snapshot | KHÔNG ĐO ĐƯỢC |
| L9 duration từ timestamps = 968.846 | 968.846 | CÓ |
| L9 README giây làm tròn = 969 | 969 | CÓ |
| L9 so_lan_chet_truoc_khi_xong = 0 | KHÔNG ĐO ĐƯỢC: không có khoá/lịch sử retry trong run.json; receipt đã nhãn attestation | KHÔNG ĐO ĐƯỢC |
| L9 model_yeu_cau = gpt-6-astra | gpt-6-astra trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L9 effort = xhigh | xhigh trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L9 head run.json / reviewed_sha = 3ae4f6157636949b2941a218deba5dbaa7df1d30 | 3ae4f6157636949b2941a218deba5dbaa7df1d30 | CÓ |
| L9 reviewed_sha trong verdict = 3ae4f6157636949b2941a218deba5dbaa7df1d30 | 3ae4f6157636949b2941a218deba5dbaa7df1d30 | CÓ |
| L9 reviewed_base trong verdict = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L9 verdict trong verdict = changes_requested | changes_requested | CÓ |
| L9 reviewed_base = base thật = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L9 so_p1 = 0 | 0 | CÓ |
| L9 so_p2 = 1 | 1 | CÓ |
| L9 so_p3 = 0 | 0 | CÓ |
| L9 findings_ids = ['t152-fixture-bo-sot-token-lan-hoa-thuong'] | ['t152-fixture-bo-sot-token-lan-hoa-thuong'] | CÓ |
| L9 lease_id = m9-fetch-auth-exec-3-claude-20260911 | m9-fetch-auth-exec-3-claude-20260911 theo phân bổ generation của verdict/prompt | CÓ nội bộ; lease cấp thật KHÔNG ĐO ĐƯỢC |
| L9 gen README = 3 | 3 | CÓ |
| L9 HINT sha256 = 67a3b7d5cf558103ee080931efaf8457d1021e85a5cd3cc4eb75b6a23c77bccc | 67a3b7d5cf558103ee080931efaf8457d1021e85a5cd3cc4eb75b6a23c77bccc | CÓ |
| L9 HINT bytes = 649 | 649 | CÓ |
| L9 worktree_sach = True | True | CÓ |
| L10 cmp nguyên byte = True | True | CÓ |
| L10 verdict_sha256 = fea4c51180dc5e2e7c3e9532b1b817df1c55aaf0b0b2dbc536270b26c118f9b1 | fea4c51180dc5e2e7c3e9532b1b817df1c55aaf0b0b2dbc536270b26c118f9b1 | CÓ |
| L10 verdict_bytes = 23827 | 23827 | CÓ |
| L10 README byte = 23827 | 23827 | CÓ |
| L10 m9-runs.json toàn object = bằng run.json | bằng run.json | CÓ |
| L10 model_reviewer_identity.session_run_id = cb013b5c | cb013b5c | CÓ |
| L10 model_reviewer_identity.run_id_day_du = cb013b5cc4794b40842c55d06b7e6ced | cb013b5cc4794b40842c55d06b7e6ced | CÓ |
| L10 model_reviewer_identity.prompt_sha256 = a763af6edd2bea333420f28a7cab2286db8344b651c2e82a4fe43c90319482af | a763af6edd2bea333420f28a7cab2286db8344b651c2e82a4fe43c90319482af | CÓ |
| L10 model_reviewer_identity.bat_dau_utc = 2026-09-11T10:34:32.130972+00:00 | 2026-09-11T10:34:32.130972+00:00 | CÓ |
| L10 model_reviewer_identity.ket_thuc_utc = 2026-09-11T10:50:12.354197+00:00 | 2026-09-11T10:50:12.354197+00:00 | CÓ |
| L10 model_reviewer_identity.thoi_luong_giay = 940.223 | 940.223 | CÓ |
| L10 model_reviewer_identity.ma_thoat = 0 | 0 | CÓ |
| L10 model_reviewer_identity.trang_thai = xong | xong | CÓ |
| L10 model_reviewer_identity.stdout_byte = 333 | 333 | CÓ |
| L10 model_reviewer_identity.stdout_sha256 = 8e7123ceed2db5ae57051e21f32d82a86639c52b1e7cf576cdd3e7060e671ce7 | 8e7123ceed2db5ae57051e21f32d82a86639c52b1e7cf576cdd3e7060e671ce7 | CÓ |
| L10 model_reviewer_identity.stderr_byte = 580663 | 580663 | CÓ |
| L10 model_reviewer_identity.stderr_sha256 = d40ed3479adf342f7ddf9ff18f082255ed4578e90c69bded38ead645266d6294 | d40ed3479adf342f7ddf9ff18f082255ed4578e90c69bded38ead645266d6294 | CÓ |
| L10 stdout byte thật (receipt + run.json) = 333 | 333 | CÓ |
| L10 stdout sha256 thật (receipt + run.json) = 8e7123ceed2db5ae57051e21f32d82a86639c52b1e7cf576cdd3e7060e671ce7 | 8e7123ceed2db5ae57051e21f32d82a86639c52b1e7cf576cdd3e7060e671ce7 | CÓ |
| L10 stderr byte thật (receipt + run.json) = 580663 | 580663 | CÓ |
| L10 stderr sha256 thật (receipt + run.json) = d40ed3479adf342f7ddf9ff18f082255ed4578e90c69bded38ead645266d6294 | d40ed3479adf342f7ddf9ff18f082255ed4578e90c69bded38ead645266d6294 | CÓ |
| L10 prompt_sha256 / snapshot = a763af6edd2bea333420f28a7cab2286db8344b651c2e82a4fe43c90319482af | KHÔNG ĐO ĐƯỢC: gói không có prompt.snapshot | KHÔNG ĐO ĐƯỢC |
| L10 duration từ timestamps = 940.223 | 940.223 | CÓ |
| L10 README giây làm tròn = 940 | 940 | CÓ |
| L10 so_lan_chet_truoc_khi_xong = 0 | KHÔNG ĐO ĐƯỢC: không có khoá/lịch sử retry trong run.json; receipt đã nhãn attestation | KHÔNG ĐO ĐƯỢC |
| L10 model_yeu_cau = gpt-6-astra | gpt-6-astra trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L10 effort = xhigh | xhigh trong header stderr.log; không có key trong run.json. Chỉ cấu hình yêu cầu. | CÓ cấu hình; model thực KHÔNG ĐO ĐƯỢC |
| L10 head run.json / reviewed_sha = de49fa0d077a2a00e9f936240378979a8ebc080c | de49fa0d077a2a00e9f936240378979a8ebc080c | CÓ |
| L10 reviewed_sha trong verdict = de49fa0d077a2a00e9f936240378979a8ebc080c | de49fa0d077a2a00e9f936240378979a8ebc080c | CÓ |
| L10 reviewed_base trong verdict = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L10 verdict trong verdict = approve | approve | CÓ |
| L10 reviewed_base = base thật = 27c413c3e531800431cad9db4452d7236505a5a9 | 27c413c3e531800431cad9db4452d7236505a5a9 | CÓ |
| L10 so_p1 = 0 | 0 | CÓ |
| L10 so_p2 = 0 | 0 | CÓ |
| L10 so_p3 = 0 | 0 | CÓ |
| L10 findings_ids = [] | [] | CÓ |
| L10 lease_id = m9-fetch-auth-exec-4-claude-20260911 | m9-fetch-auth-exec-4-claude-20260911 theo phân bổ generation của verdict/prompt | CÓ nội bộ; lease cấp thật KHÔNG ĐO ĐƯỢC |
| L10 gen README = 4 | 4 | CÓ |
| L10 HINT sha256 = aef424079ab23e52419281856345c5fb4e559d51762688e3e4734edd024564aa | aef424079ab23e52419281856345c5fb4e559d51762688e3e4734edd024564aa | CÓ |
| L10 HINT bytes = 158 | 158 | CÓ |
| L10 worktree_sach = True | True | CÓ |

### 4. Các trường receipt còn lại và giới hạn của danh tính

| Khai | Đo | Khớp? |
|---|---|---|
| L1 schema_version = 2 | v2 CLI/schema đi qua; parse YAML là integer2 | CÓ |
| L1 receipt_id = pr505-review-1-codex-20260911-28f02cda | pr505-review-1-codex-20260911-28f02cda; khớp tên file/lượt/short_id/ngày run | CÓ |
| L1 kind = review_delivery_receipt | review_delivery_receipt; hợp lệ ở cổng v2 | CÓ |
| L1 packet_id = wp503 | wp503 cùng packet#503 được 10 verdict/prompt nhắc; không có record cấp lease thật | CÓ đối chiếu văn bản |
| L1 phase_key = M9-FETCH-AUTH | M9-FETCH-AUTH trong spec/10 verdict/prompt | CÓ đối chiếu văn bản |
| L1 luot = 1 | 1 đúng review_round trong verdict | CÓ |
| L1 role = reviewer | verdict là báo cáo reviewer; vai trò runtime ngoài gói không chứng thực | CÓ văn bản |
| L1 provider = codex | mri.provider=openai_codex; header CLI ghi OpenAI Codex và provider:openai | CÓ cấu hình/tên nền |
| L1 executor_provider = claude | claude do prompt và receipt tự khai | KHÔNG ĐO ĐƯỢC danh tính thực |
| L1 cross_provider = True | mri.openai_codex khác executor tự khai claude; không chứng thực hai model thực | CÓ hợp đồng/attestation |
| L1 assurance = cross_reviewed | cross_reviewed với changes_requested; v2 chấp nhận hợp đồng máy + phiên review khác nền tự khai | CÓ mức hợp đồng; không chứng thực model build |
| L1 model_reviewer_identity.provider = openai_codex | openai_codex trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L1 model_reviewer_identity.surface = codex_cli | codex_cli trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L1 model_reviewer_identity.transport = machine | machine trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG; run.json.transport=machine | CÓ |
| L1 model_reviewer_identity.model_da_chay = KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | 0 chuỗi modelUsage trong stdout.log và stderr.log; header chỉ cho cấu hình model:gpt-6-astra. Verdict tự khai GPT-6 / Codex / OpenAI. | CÓ giới hạn KHÔNG ĐO ĐƯỢC |
| L1 nguon_cac_scalar_tren = ĐỐI CHIẾU ĐƯỢC với run.json (ngoài kho, `scratchpad/runs/28f02cda/`): run_id/short_id, prompt_sha256, bat_dau_utc, ket_thuc_utc, thoi_luong_giay, ma_thoat, trang_thai, stdout_byte/sha256, stderr_byte/sha256, worktree_sach, head. Dòng cuối stdout `XONG VERDICT sha256=a0bb40dc…` khớp băm tệp. model_yeu_cau, effort, transport và so_lan_chet_truoc_khi_xong là ATTESTATION điều phối, KHÔNG có khoá tương ứng trong run.json. | Tất cả scalar liệt kê đối chiếu đúng; ngoại lệ câu transport không có key là SAI: run.json có transport=machine. Header stderr hỗ trợ model yêu cầu/effort; số lần chết chưa đo. | KHÔNG — P2 nguon-runtime-xep-sai-transport |
| L1 verdict_path = ops/reviews/pr505-review-1-codex-verdict.md | Tệp thật tồn tại; bytes và tên URL cùng ops/reviews/pr505-review-1-codex-verdict.md | CÓ |
| L1 evidence_url = https://github.com/ducthangho/tra-luat/blob/9dc8460f55a61b8b9670606a62f6db40905d851c/ops/reviews/pr505-review-1-codex-verdict.md | commit9dc8460f55a61b8b9670606a62f6db40905d851c là ancestorHEAD; git show blob đúng đường băm=a0bb40dc74b6029f0456bf18f61cc5a626669a3575a1a8c89347dd421b1eace9 | CÓ |
| L1 evidence_url_ghi_chu = Neo BLOB ghim `9dc8460` — commit ĐẦU TIÊN chứa 10 tệp verdict PR #505 (`git log --all --diff-filter=A`, đúng 1 commit). Bản chiếu công khai sớm hơn: PR #505 comment 5629894965 — chiếu frontmatter, ĐỐI CHIẾU LƯỢT TRƯỚC, kết luận, Findings, Mutant, chua_do_duoc; `## BẢNG ĐO` và các bảng shell/bề mặt lộ token CHỈ có trong tệp này. | “commit đầu tiên” khớp Git. Bản chiếu comment/nội dung bị lược không có response GitHub trong gói. | CÓ phần Git; comment KHÔNG ĐO ĐƯỢC |
| L1 hint_patch.noi_dung = thay phép dò chuỗi bằng việc CHẠY đoạn shell auth/fetch với Git config thật + chốt (v) mask; chỉ test | HINT nguồn có 1 hunk; đối chiếu mô tả với HINT/verdict. Kết quả logic mutant là thuật lại nguồn cũ. | CÓ đối chiếu nguồn |
| L1 noi_dung_do_duoc_van_dung[1] = ĐO: workflow 62c299a truyền đúng header ở biên Git/helper cục bộ; t152 bản dò chuỗi cho m5 (COUNT=0), m7 (ghi đè AUTH_B64), m8 (xoá add-mask) SỐNG ⇒ P1 + P2; HINT chạy chính đoạn shell với Git config thật. | Tiêu đề Findings/bảng mutant verdict L1 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L1 noi_dung_do_duoc_van_dung[2] = Mutant m1–m9: 6 GIẾT / 3 SỐNG trên t152 gốc; sau HINT 9/9 GIẾT. Suite 147/147 (AL_VER=1.7.7), actionlint rc=0. | Tiêu đề Findings/bảng mutant verdict L1 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L1 noi_dung_do_duoc_van_dung[3] = Ghi nhận: 27 commit `origin/master` sau base chạm cả `ops/cong_cu.py` (mô tả tác giả thiếu tệp này); token thô đã có sẵn trong argv curl (dòng 118) từ A0. | Tiêu đề Findings/bảng mutant verdict L1 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L1 nang_luc_do_cua_goi.mirror = clone mới từ guong.git (fetch sau push 62c299a), detached 62c299a, core.abbrev 7, không nông; nguon/ có spec M9-FETCH-AUTH.md (sha b8200141…) + actionlint 1.7.7 + VERDICT/HINT các lượt trước của chính reviewer; EVIDENCE.md bổ sung từng lượt | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L1 nang_luc_do_cua_goi.chua_do_duoc = Không mạng; không đọc doctrine; prompt snapshot/stderr.log không kèm; suite chạy trên bản sao ops/.github (t82 copytree) — không phải trực tiếp trong clone. | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L1 hien_vat_reviewer_vao_kho.duong_dan = KHONG_CO | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L1 hien_vat_reviewer_vao_kho.ghi_chu = scratch/logs/*.json\|log, scratch/mutants/, script tái lập (review_matrix.py, probe*.py, validate_hint.py, extra*.py) ở sandbox ngoài kho. | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L1 tuan_thu_cam_cua_reviewer.commit_them_ngoai_head = 0 | run.head đúng, worktree_sach=true, so_muc_ban=0; không có reflog/snapshot đủ chứng minh không từng tạo commit ngoài head. | KHÔNG ĐO ĐƯỢC; attestation |
| L1 tuan_thu_cam_cua_reviewer.bang_chung = run.json worktree_sach: true; điều phối đo sau lượt: git status --porcelain rỗng. | run.json worktree_sach=true và so_muc_ban=0; thao tác git status riêng của điều phối sau lượt không có receipt thực thi độc lập. | CÓ run.json; nửa điều phối KHÔNG ĐO ĐƯỢC |
| L1 github_submitter_identity.actor = ducthangho | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L1 github_submitter_identity.la_tac_gia_PR = True | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L1 github_submitter_identity.ghi_chu = `ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; uỷ quyền merge là chỉ thị chủ kho #503 comment 5632304817 ("các PR thuộc phiên này thực hiện theo khuyến nghị") + "Tôi chọn A" (#503 comment 5633059702, gen 4 kèm điều kiện dừng). | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L1 github_submitter_identity.phien_van_chuyen = https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L1 anchor.loai = canonical_ancestry | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L1 anchor.cuong_do = cao | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L1 anchor.mo_ta = Blob verdict ghim `9dc8460`. Head đã review `62c299a` là tổ tiên của master (`fe05fa6d`, merge commit #505, hai cha fa717ee + de49fa0; nhánh claude/m9-fetch-auth tuyến tính 62c299a → de49fa0). | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L1 anchor.gioi_han = Vững khi land bằng merge commit hoặc fast-forward; squash phá quan hệ tổ tiên. | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L1 khong_do_duoc[1] = Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L1 khong_do_duoc[2] = run.json/stdout.log/stderr.log không vào kho ⇒ scalar runtime là attestation. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L1 khong_do_duoc[3] = Fetch trên runner GitHub thật, secret masker, receipt/artifact thật (A3/M3): sandbox không mạng — đo ở PR hồ sơ r366 sau land, ghi ở CHANGELOG r366/#503, không ở verdict. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L1 khong_do_duoc[4] = Git 2.31/toàn dải, ảnh ubuntu-latest hiện hành, Windows: không chạy trong sandbox. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L1 delivered = True | Có tệp verdict thật tại commit9dc8460, receipt tạifa09a48; chứng minh giao vào kho | CÓ vào kho |
| L1 delivered_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L1 authoritative_source = repo_file | repo_file: bytes gốc 10 verdict cùng sha256 nguồn; URL ghim đúng blob | CÓ |
| L1 receipt_written_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L1 receipt_written_at_utc = 2026-09-11T11:2xZ | Không có runtime viết receipt; giá trị11:2xZ không là timestamp chính xác. Metadata commit thêm receipt=11:13:20Z; CHANGELOG=11:15:14Z, sớm hơn nhãn 11:2x. Không dùng đồng hồ commit để suy giờ thực viết. | KHÔNG ĐO ĐƯỢC thời điểm thực |
| L1 receipt_khong_khai[1] = Không khai `thu-hoi` đã xanh trên #505 — nó ĐỎ tất định (định nghĩa từ master) tới lúc land; chủ kho quyết merge bằng chỉ thị. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L1 receipt_khong_khai[2] = Không khai A3 đã đạt — chưa đo lúc viết. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L1 receipt_khong_khai[3] = Không khai model đã chạy — codex không đo được. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L1 receipt_khong_khai[4] = Không khai các lease gen 1–3 "hết hạn" hay "bị thu hồi vì lỗi bản vá" — chúng bị thay thế vì hết lượt/vòng theo ADR-0043, chủ kho reroute. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L1 dòng cuối stdout khớp verdict_sha256 | XONG VERDICT sha256=a0bb40dc74b6029f0456bf18f61cc5a626669a3575a1a8c89347dd421b1eace9 | CÓ |
| L1 reviewed_files_sha256 trong verdict / .github/workflows/ops-thu-hoi-admission.yml = 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | CÓ |
| L1 reviewed_files_sha256 trong verdict / ops/lease_publish_test.py = 47fe99e88f25eecae6a83c6bb1357a14362e61a9320ce938d6d976fdb99d29ed | 47fe99e88f25eecae6a83c6bb1357a14362e61a9320ce938d6d976fdb99d29ed | CÓ |
| L2 schema_version = 2 | v2 CLI/schema đi qua; parse YAML là integer2 | CÓ |
| L2 receipt_id = pr505-review-2-codex-20260911-6b3e8525 | pr505-review-2-codex-20260911-6b3e8525; khớp tên file/lượt/short_id/ngày run | CÓ |
| L2 kind = review_delivery_receipt | review_delivery_receipt; hợp lệ ở cổng v2 | CÓ |
| L2 packet_id = wp503 | wp503 cùng packet#503 được 10 verdict/prompt nhắc; không có record cấp lease thật | CÓ đối chiếu văn bản |
| L2 phase_key = M9-FETCH-AUTH | M9-FETCH-AUTH trong spec/10 verdict/prompt | CÓ đối chiếu văn bản |
| L2 luot = 2 | 2 đúng review_round trong verdict | CÓ |
| L2 role = reviewer | verdict là báo cáo reviewer; vai trò runtime ngoài gói không chứng thực | CÓ văn bản |
| L2 provider = codex | mri.provider=openai_codex; header CLI ghi OpenAI Codex và provider:openai | CÓ cấu hình/tên nền |
| L2 executor_provider = claude | claude do prompt và receipt tự khai | KHÔNG ĐO ĐƯỢC danh tính thực |
| L2 cross_provider = True | mri.openai_codex khác executor tự khai claude; không chứng thực hai model thực | CÓ hợp đồng/attestation |
| L2 assurance = cross_reviewed | cross_reviewed với changes_requested; v2 chấp nhận hợp đồng máy + phiên review khác nền tự khai | CÓ mức hợp đồng; không chứng thực model build |
| L2 model_reviewer_identity.provider = openai_codex | openai_codex trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L2 model_reviewer_identity.surface = codex_cli | codex_cli trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L2 model_reviewer_identity.transport = machine | machine trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG; run.json.transport=machine | CÓ |
| L2 model_reviewer_identity.model_da_chay = KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | 0 chuỗi modelUsage trong stdout.log và stderr.log; header chỉ cho cấu hình model:gpt-6-astra. Verdict tự khai GPT-6 / Codex / OpenAI. | CÓ giới hạn KHÔNG ĐO ĐƯỢC |
| L2 nguon_cac_scalar_tren = ĐỐI CHIẾU ĐƯỢC với run.json (ngoài kho, `scratchpad/runs/6b3e8525/`): run_id/short_id, prompt_sha256, bat_dau_utc, ket_thuc_utc, thoi_luong_giay, ma_thoat, trang_thai, stdout_byte/sha256, stderr_byte/sha256, worktree_sach, head. Dòng cuối stdout `XONG VERDICT sha256=13a0b829…` khớp băm tệp. model_yeu_cau, effort, transport và so_lan_chet_truoc_khi_xong là ATTESTATION điều phối, KHÔNG có khoá tương ứng trong run.json. | Tất cả scalar liệt kê đối chiếu đúng; ngoại lệ câu transport không có key là SAI: run.json có transport=machine. Header stderr hỗ trợ model yêu cầu/effort; số lần chết chưa đo. | KHÔNG — P2 nguon-runtime-xep-sai-transport |
| L2 verdict_path = ops/reviews/pr505-review-2-codex-verdict.md | Tệp thật tồn tại; bytes và tên URL cùng ops/reviews/pr505-review-2-codex-verdict.md | CÓ |
| L2 evidence_url = https://github.com/ducthangho/tra-luat/blob/9dc8460f55a61b8b9670606a62f6db40905d851c/ops/reviews/pr505-review-2-codex-verdict.md | commit9dc8460f55a61b8b9670606a62f6db40905d851c là ancestorHEAD; git show blob đúng đường băm=13a0b829fa81f330a8989872b4d3df4ed9968f5f5c563d9baa2dc4912784c4fb | CÓ |
| L2 evidence_url_ghi_chu = Neo BLOB ghim `9dc8460` — commit ĐẦU TIÊN chứa 10 tệp verdict PR #505 (`git log --all --diff-filter=A`, đúng 1 commit). Bản chiếu công khai sớm hơn: PR #505 comment 5630046807 — chiếu frontmatter, ĐỐI CHIẾU LƯỢT TRƯỚC, kết luận, Findings, Mutant, chua_do_duoc; `## BẢNG ĐO` và các bảng shell/bề mặt lộ token CHỈ có trong tệp này. | “commit đầu tiên” khớp Git. Bản chiếu comment/nội dung bị lược không có response GitHub trong gói. | CÓ phần Git; comment KHÔNG ĐO ĐƯỢC |
| L2 hint_patch.noi_dung = 2 hunk test: bộ dò `git … fetch` refs/pull độc lập vị trí cờ; stub đòi protocol.https.allow=always | HINT nguồn có 2 hunk; đối chiếu mô tả với HINT/verdict. Kết quả logic mutant là thuật lại nguồn cũ. | CÓ đối chiếu nguồn |
| L2 noi_dung_do_duoc_van_dung[1] = ĐỐI CHIẾU: hai finding lượt 1 ĐÃ VÁ THẬT (áp HINT lượt 1 lên test 62c299a trùng byte HEAD trừ docstring). m10 (fetch thứ hai --quiet trước --no-tags, không header) và m11 (protocol.https.allow=never) SỐNG ⇒ P1 + P2. | Tiêu đề Findings/bảng mutant verdict L2 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L2 noi_dung_do_duoc_van_dung[2] = Sau HINT 11/11 GIẾT; suite 147/147; tổng diff sau HINT +80/−0 đúng trần A4. | Tiêu đề Findings/bảng mutant verdict L2 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L2 nang_luc_do_cua_goi.mirror = clone mới từ guong.git (fetch sau push 6254570), detached 6254570, core.abbrev 7, không nông; nguon/ có spec M9-FETCH-AUTH.md (sha b8200141…) + actionlint 1.7.7 + VERDICT/HINT các lượt trước của chính reviewer; EVIDENCE.md bổ sung từng lượt | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L2 nang_luc_do_cua_goi.chua_do_duoc = Không mạng; không đọc doctrine; prompt snapshot/stderr.log không kèm; suite chạy trên bản sao ops/.github (t82 copytree) — không phải trực tiếp trong clone. | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L2 hien_vat_reviewer_vao_kho.duong_dan = KHONG_CO | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L2 hien_vat_reviewer_vao_kho.ghi_chu = scratch/logs/*.json\|log, scratch/mutants/, script tái lập (review_matrix.py, probe*.py, validate_hint.py, extra*.py) ở sandbox ngoài kho. | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L2 tuan_thu_cam_cua_reviewer.commit_them_ngoai_head = 0 | run.head đúng, worktree_sach=true, so_muc_ban=0; không có reflog/snapshot đủ chứng minh không từng tạo commit ngoài head. | KHÔNG ĐO ĐƯỢC; attestation |
| L2 tuan_thu_cam_cua_reviewer.bang_chung = run.json worktree_sach: true; điều phối đo sau lượt: git status --porcelain rỗng. | run.json worktree_sach=true và so_muc_ban=0; thao tác git status riêng của điều phối sau lượt không có receipt thực thi độc lập. | CÓ run.json; nửa điều phối KHÔNG ĐO ĐƯỢC |
| L2 github_submitter_identity.actor = ducthangho | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L2 github_submitter_identity.la_tac_gia_PR = True | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L2 github_submitter_identity.ghi_chu = `ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; uỷ quyền merge là chỉ thị chủ kho #503 comment 5632304817 ("các PR thuộc phiên này thực hiện theo khuyến nghị") + "Tôi chọn A" (#503 comment 5633059702, gen 4 kèm điều kiện dừng). | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L2 github_submitter_identity.phien_van_chuyen = https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L2 anchor.loai = canonical_ancestry | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L2 anchor.cuong_do = cao | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L2 anchor.mo_ta = Blob verdict ghim `9dc8460`. Head đã review `6254570` là tổ tiên của master (`fe05fa6d`, merge commit #505, hai cha fa717ee + de49fa0; nhánh claude/m9-fetch-auth tuyến tính 62c299a → de49fa0). | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L2 anchor.gioi_han = Vững khi land bằng merge commit hoặc fast-forward; squash phá quan hệ tổ tiên. | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L2 khong_do_duoc[1] = Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L2 khong_do_duoc[2] = run.json/stdout.log/stderr.log không vào kho ⇒ scalar runtime là attestation. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L2 khong_do_duoc[3] = Fetch trên runner GitHub thật, secret masker, receipt/artifact thật (A3/M3): sandbox không mạng — đo ở PR hồ sơ r366 sau land, ghi ở CHANGELOG r366/#503, không ở verdict. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L2 khong_do_duoc[4] = Git 2.31/toàn dải, ảnh ubuntu-latest hiện hành, Windows: không chạy trong sandbox. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L2 delivered = True | Có tệp verdict thật tại commit9dc8460, receipt tạifa09a48; chứng minh giao vào kho | CÓ vào kho |
| L2 delivered_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L2 authoritative_source = repo_file | repo_file: bytes gốc 10 verdict cùng sha256 nguồn; URL ghim đúng blob | CÓ |
| L2 receipt_written_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L2 receipt_written_at_utc = 2026-09-11T11:2xZ | Không có runtime viết receipt; giá trị11:2xZ không là timestamp chính xác. Metadata commit thêm receipt=11:13:20Z; CHANGELOG=11:15:14Z, sớm hơn nhãn 11:2x. Không dùng đồng hồ commit để suy giờ thực viết. | KHÔNG ĐO ĐƯỢC thời điểm thực |
| L2 receipt_khong_khai[1] = Không khai `thu-hoi` đã xanh trên #505 — nó ĐỎ tất định (định nghĩa từ master) tới lúc land; chủ kho quyết merge bằng chỉ thị. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L2 receipt_khong_khai[2] = Không khai A3 đã đạt — chưa đo lúc viết. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L2 receipt_khong_khai[3] = Không khai model đã chạy — codex không đo được. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L2 receipt_khong_khai[4] = Không khai các lease gen 1–3 "hết hạn" hay "bị thu hồi vì lỗi bản vá" — chúng bị thay thế vì hết lượt/vòng theo ADR-0043, chủ kho reroute. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L2 dòng cuối stdout khớp verdict_sha256 | XONG VERDICT sha256=13a0b829fa81f330a8989872b4d3df4ed9968f5f5c563d9baa2dc4912784c4fb | CÓ |
| L2 reviewed_files_sha256 trong verdict / .github/workflows/ops-thu-hoi-admission.yml = 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | CÓ |
| L2 reviewed_files_sha256 trong verdict / ops/lease_publish_test.py = f51a0cf9e4af56e165ee02f35838c8f4b54f5e70c830aa19889ffd7fa9894223 | f51a0cf9e4af56e165ee02f35838c8f4b54f5e70c830aa19889ffd7fa9894223 | CÓ |
| L3 schema_version = 2 | v2 CLI/schema đi qua; parse YAML là integer2 | CÓ |
| L3 receipt_id = pr505-review-3-codex-20260911-4024cfff | pr505-review-3-codex-20260911-4024cfff; khớp tên file/lượt/short_id/ngày run | CÓ |
| L3 kind = review_delivery_receipt | review_delivery_receipt; hợp lệ ở cổng v2 | CÓ |
| L3 packet_id = wp503 | wp503 cùng packet#503 được 10 verdict/prompt nhắc; không có record cấp lease thật | CÓ đối chiếu văn bản |
| L3 phase_key = M9-FETCH-AUTH | M9-FETCH-AUTH trong spec/10 verdict/prompt | CÓ đối chiếu văn bản |
| L3 luot = 3 | 3 đúng review_round trong verdict | CÓ |
| L3 role = reviewer | verdict là báo cáo reviewer; vai trò runtime ngoài gói không chứng thực | CÓ văn bản |
| L3 provider = codex | mri.provider=openai_codex; header CLI ghi OpenAI Codex và provider:openai | CÓ cấu hình/tên nền |
| L3 executor_provider = claude | claude do prompt và receipt tự khai | KHÔNG ĐO ĐƯỢC danh tính thực |
| L3 cross_provider = True | mri.openai_codex khác executor tự khai claude; không chứng thực hai model thực | CÓ hợp đồng/attestation |
| L3 assurance = cross_reviewed | cross_reviewed với changes_requested; v2 chấp nhận hợp đồng máy + phiên review khác nền tự khai | CÓ mức hợp đồng; không chứng thực model build |
| L3 model_reviewer_identity.provider = openai_codex | openai_codex trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L3 model_reviewer_identity.surface = codex_cli | codex_cli trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L3 model_reviewer_identity.transport = machine | machine trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG; run.json.transport=machine | CÓ |
| L3 model_reviewer_identity.model_da_chay = KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | 0 chuỗi modelUsage trong stdout.log và stderr.log; header chỉ cho cấu hình model:gpt-6-astra. Verdict tự khai GPT-6 / Codex / OpenAI. | CÓ giới hạn KHÔNG ĐO ĐƯỢC |
| L3 nguon_cac_scalar_tren = ĐỐI CHIẾU ĐƯỢC với run.json (ngoài kho, `scratchpad/runs/4024cfff/`): run_id/short_id, prompt_sha256, bat_dau_utc, ket_thuc_utc, thoi_luong_giay, ma_thoat, trang_thai, stdout_byte/sha256, stderr_byte/sha256, worktree_sach, head. Dòng cuối stdout `XONG VERDICT sha256=ebaff0d4…` khớp băm tệp. model_yeu_cau, effort, transport và so_lan_chet_truoc_khi_xong là ATTESTATION điều phối, KHÔNG có khoá tương ứng trong run.json. | Tất cả scalar liệt kê đối chiếu đúng; ngoại lệ câu transport không có key là SAI: run.json có transport=machine. Header stderr hỗ trợ model yêu cầu/effort; số lần chết chưa đo. | KHÔNG — P2 nguon-runtime-xep-sai-transport |
| L3 verdict_path = ops/reviews/pr505-review-3-codex-verdict.md | Tệp thật tồn tại; bytes và tên URL cùng ops/reviews/pr505-review-3-codex-verdict.md | CÓ |
| L3 evidence_url = https://github.com/ducthangho/tra-luat/blob/9dc8460f55a61b8b9670606a62f6db40905d851c/ops/reviews/pr505-review-3-codex-verdict.md | commit9dc8460f55a61b8b9670606a62f6db40905d851c là ancestorHEAD; git show blob đúng đường băm=ebaff0d45b1c4eb0b2f15f92462f78cc311698c6e3fd479414d8099b6c751dde | CÓ |
| L3 evidence_url_ghi_chu = Neo BLOB ghim `9dc8460` — commit ĐẦU TIÊN chứa 10 tệp verdict PR #505 (`git log --all --diff-filter=A`, đúng 1 commit). Bản chiếu công khai sớm hơn: PR #505 comment 5630375344 — chiếu frontmatter, ĐỐI CHIẾU LƯỢT TRƯỚC, kết luận, Findings, Mutant, chua_do_duoc; `## BẢNG ĐO` và các bảng shell/bề mặt lộ token CHỈ có trong tệp này. | “commit đầu tiên” khớp Git. Bản chiếu comment/nội dung bị lược không có response GitHub trong gói. | CÓ phần Git; comment KHÔNG ĐO ĐƯỢC |
| L3 hint_patch.noi_dung = 1 hunk test: chốt (v) thêm `and not p.stderr` | HINT nguồn có 1 hunk; đối chiếu mô tả với HINT/verdict. Kết quả logic mutant là thuật lại nguồn cũ. | CÓ đối chiếu nguồn |
| L3 noi_dung_do_duoc_van_dung[1] = ĐỐI CHIẾU: hai finding lượt 2 ĐÃ VÁ THẬT (hunk == HINT). m12 (set -x ngay trước gán AUTH_B64) SỐNG: base64 ra stderr trước mask, t152 chỉ so stdout ⇒ P1. | Tiêu đề Findings/bảng mutant verdict L3 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L3 noi_dung_do_duoc_van_dung[2] = m1–m11 11/11 GIẾT; HINT 1 hunk; suite HEAD và HINT 147/147. Đây là vòng 3/3 của gen 1 (trần nâng 2→3, #503 comment 5630194531). | Tiêu đề Findings/bảng mutant verdict L3 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L3 nang_luc_do_cua_goi.mirror = clone mới từ guong.git (fetch sau push c851f80), detached c851f80, core.abbrev 7, không nông; nguon/ có spec M9-FETCH-AUTH.md (sha b8200141…) + actionlint 1.7.7 + VERDICT/HINT các lượt trước của chính reviewer; EVIDENCE.md bổ sung từng lượt | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L3 nang_luc_do_cua_goi.chua_do_duoc = Không mạng; không đọc doctrine; prompt snapshot/stderr.log không kèm; suite chạy trên bản sao ops/.github (t82 copytree) — không phải trực tiếp trong clone. | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L3 hien_vat_reviewer_vao_kho.duong_dan = KHONG_CO | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L3 hien_vat_reviewer_vao_kho.ghi_chu = scratch/logs/*.json\|log, scratch/mutants/, script tái lập (review_matrix.py, probe*.py, validate_hint.py, extra*.py) ở sandbox ngoài kho. | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L3 tuan_thu_cam_cua_reviewer.commit_them_ngoai_head = 0 | run.head đúng, worktree_sach=true, so_muc_ban=0; không có reflog/snapshot đủ chứng minh không từng tạo commit ngoài head. | KHÔNG ĐO ĐƯỢC; attestation |
| L3 tuan_thu_cam_cua_reviewer.bang_chung = run.json worktree_sach: true; điều phối đo sau lượt: git status --porcelain rỗng. | run.json worktree_sach=true và so_muc_ban=0; thao tác git status riêng của điều phối sau lượt không có receipt thực thi độc lập. | CÓ run.json; nửa điều phối KHÔNG ĐO ĐƯỢC |
| L3 github_submitter_identity.actor = ducthangho | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L3 github_submitter_identity.la_tac_gia_PR = True | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L3 github_submitter_identity.ghi_chu = `ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; uỷ quyền merge là chỉ thị chủ kho #503 comment 5632304817 ("các PR thuộc phiên này thực hiện theo khuyến nghị") + "Tôi chọn A" (#503 comment 5633059702, gen 4 kèm điều kiện dừng). | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L3 github_submitter_identity.phien_van_chuyen = https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L3 anchor.loai = canonical_ancestry | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L3 anchor.cuong_do = cao | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L3 anchor.mo_ta = Blob verdict ghim `9dc8460`. Head đã review `c851f80` là tổ tiên của master (`fe05fa6d`, merge commit #505, hai cha fa717ee + de49fa0; nhánh claude/m9-fetch-auth tuyến tính 62c299a → de49fa0). | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L3 anchor.gioi_han = Vững khi land bằng merge commit hoặc fast-forward; squash phá quan hệ tổ tiên. | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L3 khong_do_duoc[1] = Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L3 khong_do_duoc[2] = run.json/stdout.log/stderr.log không vào kho ⇒ scalar runtime là attestation. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L3 khong_do_duoc[3] = Fetch trên runner GitHub thật, secret masker, receipt/artifact thật (A3/M3): sandbox không mạng — đo ở PR hồ sơ r366 sau land, ghi ở CHANGELOG r366/#503, không ở verdict. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L3 khong_do_duoc[4] = Git 2.31/toàn dải, ảnh ubuntu-latest hiện hành, Windows: không chạy trong sandbox. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L3 delivered = True | Có tệp verdict thật tại commit9dc8460, receipt tạifa09a48; chứng minh giao vào kho | CÓ vào kho |
| L3 delivered_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L3 authoritative_source = repo_file | repo_file: bytes gốc 10 verdict cùng sha256 nguồn; URL ghim đúng blob | CÓ |
| L3 receipt_written_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L3 receipt_written_at_utc = 2026-09-11T11:2xZ | Không có runtime viết receipt; giá trị11:2xZ không là timestamp chính xác. Metadata commit thêm receipt=11:13:20Z; CHANGELOG=11:15:14Z, sớm hơn nhãn 11:2x. Không dùng đồng hồ commit để suy giờ thực viết. | KHÔNG ĐO ĐƯỢC thời điểm thực |
| L3 receipt_khong_khai[1] = Không khai `thu-hoi` đã xanh trên #505 — nó ĐỎ tất định (định nghĩa từ master) tới lúc land; chủ kho quyết merge bằng chỉ thị. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L3 receipt_khong_khai[2] = Không khai A3 đã đạt — chưa đo lúc viết. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L3 receipt_khong_khai[3] = Không khai model đã chạy — codex không đo được. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L3 receipt_khong_khai[4] = Không khai các lease gen 1–3 "hết hạn" hay "bị thu hồi vì lỗi bản vá" — chúng bị thay thế vì hết lượt/vòng theo ADR-0043, chủ kho reroute. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L3 dòng cuối stdout khớp verdict_sha256 | XONG VERDICT sha256=ebaff0d45b1c4eb0b2f15f92462f78cc311698c6e3fd479414d8099b6c751dde | CÓ |
| L3 reviewed_files_sha256 trong verdict / .github/workflows/ops-thu-hoi-admission.yml = 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | CÓ |
| L3 reviewed_files_sha256 trong verdict / ops/lease_publish_test.py = da7aec4701081ea617e25077186afb22c3e9031624b27ea0304386e87c21cbb6 | da7aec4701081ea617e25077186afb22c3e9031624b27ea0304386e87c21cbb6 | CÓ |
| L4 schema_version = 2 | v2 CLI/schema đi qua; parse YAML là integer2 | CÓ |
| L4 receipt_id = pr505-review-4-codex-20260911-c2bc3d98 | pr505-review-4-codex-20260911-c2bc3d98; khớp tên file/lượt/short_id/ngày run | CÓ |
| L4 kind = review_delivery_receipt | review_delivery_receipt; hợp lệ ở cổng v2 | CÓ |
| L4 packet_id = wp503 | wp503 cùng packet#503 được 10 verdict/prompt nhắc; không có record cấp lease thật | CÓ đối chiếu văn bản |
| L4 phase_key = M9-FETCH-AUTH | M9-FETCH-AUTH trong spec/10 verdict/prompt | CÓ đối chiếu văn bản |
| L4 luot = 4 | 4 đúng review_round trong verdict | CÓ |
| L4 role = reviewer | verdict là báo cáo reviewer; vai trò runtime ngoài gói không chứng thực | CÓ văn bản |
| L4 provider = codex | mri.provider=openai_codex; header CLI ghi OpenAI Codex và provider:openai | CÓ cấu hình/tên nền |
| L4 executor_provider = claude | claude do prompt và receipt tự khai | KHÔNG ĐO ĐƯỢC danh tính thực |
| L4 cross_provider = True | mri.openai_codex khác executor tự khai claude; không chứng thực hai model thực | CÓ hợp đồng/attestation |
| L4 assurance = cross_reviewed | cross_reviewed với changes_requested; v2 chấp nhận hợp đồng máy + phiên review khác nền tự khai | CÓ mức hợp đồng; không chứng thực model build |
| L4 model_reviewer_identity.provider = openai_codex | openai_codex trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L4 model_reviewer_identity.surface = codex_cli | codex_cli trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L4 model_reviewer_identity.transport = machine | machine trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG; run.json.transport=machine | CÓ |
| L4 model_reviewer_identity.model_da_chay = KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | 0 chuỗi modelUsage trong stdout.log và stderr.log; header chỉ cho cấu hình model:gpt-6-astra. Verdict tự khai GPT-6 / Codex / OpenAI. | CÓ giới hạn KHÔNG ĐO ĐƯỢC |
| L4 nguon_cac_scalar_tren = ĐỐI CHIẾU ĐƯỢC với run.json (ngoài kho, `scratchpad/runs/c2bc3d98/`): run_id/short_id, prompt_sha256, bat_dau_utc, ket_thuc_utc, thoi_luong_giay, ma_thoat, trang_thai, stdout_byte/sha256, stderr_byte/sha256, worktree_sach, head. Dòng cuối stdout `XONG VERDICT sha256=83ee3cd4…` khớp băm tệp. model_yeu_cau, effort, transport và so_lan_chet_truoc_khi_xong là ATTESTATION điều phối, KHÔNG có khoá tương ứng trong run.json. | Tất cả scalar liệt kê đối chiếu đúng; ngoại lệ câu transport không có key là SAI: run.json có transport=machine. Header stderr hỗ trợ model yêu cầu/effort; số lần chết chưa đo. | KHÔNG — P2 nguon-runtime-xep-sai-transport |
| L4 verdict_path = ops/reviews/pr505-review-4-codex-verdict.md | Tệp thật tồn tại; bytes và tên URL cùng ops/reviews/pr505-review-4-codex-verdict.md | CÓ |
| L4 evidence_url = https://github.com/ducthangho/tra-luat/blob/9dc8460f55a61b8b9670606a62f6db40905d851c/ops/reviews/pr505-review-4-codex-verdict.md | commit9dc8460f55a61b8b9670606a62f6db40905d851c là ancestorHEAD; git show blob đúng đường băm=83ee3cd4c4d11059328d9a5002e8fdfabad78d961af5b790c49c3f9971f8795b | CÓ |
| L4 evidence_url_ghi_chu = Neo BLOB ghim `9dc8460` — commit ĐẦU TIÊN chứa 10 tệp verdict PR #505 (`git log --all --diff-filter=A`, đúng 1 commit). Bản chiếu công khai sớm hơn: PR #505 comment 5630804852 — chiếu frontmatter, ĐỐI CHIẾU LƯỢT TRƯỚC, kết luận, Findings, Mutant, chua_do_duoc; `## BẢNG ĐO` và các bảng shell/bề mặt lộ token CHỈ có trong tệp này. | “commit đầu tiên” khớp Git. Bản chiếu comment/nội dung bị lược không có response GitHub trong gói. | CÓ phần Git; comment KHÔNG ĐO ĐƯỢC |
| L4 hint_patch.noi_dung = 4 hunk test: chạy nguyên phần shell từ đầu bước tới trước NHAN, stub rev-parse cho preflight | HINT nguồn có 4 hunk; đối chiếu mô tả với HINT/verdict. Kết quả logic mutant là thuật lại nguồn cũ. | CÓ đối chiếu nguồn |
| L4 noi_dung_do_duoc_van_dung[1] = ĐỐI CHIẾU: finding lượt 3 ĐÃ VÁ THẬT. m13 (thêm -x vào `set` đầu bước, trước WF_BLOB) SỐNG vì t152 cắt đoạn sau WF_BLOB và tự đặt cờ shell ⇒ P1. | Tiêu đề Findings/bảng mutant verdict L4 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L4 noi_dung_do_duoc_van_dung[2] = m1–m12 12/12 GIẾT; HINT 4 hunk chạy nguyên phần shell từ đầu bước; suite 147/147. Gen 2 lượt 1 (reroute sau gen 1 hết 3/3 lượt+vòng). | Tiêu đề Findings/bảng mutant verdict L4 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L4 nang_luc_do_cua_goi.mirror = clone mới từ guong.git (fetch sau push 2b52173), detached 2b52173, core.abbrev 7, không nông; nguon/ có spec M9-FETCH-AUTH.md (sha b8200141…) + actionlint 1.7.7 + VERDICT/HINT các lượt trước của chính reviewer; EVIDENCE.md bổ sung từng lượt | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L4 nang_luc_do_cua_goi.chua_do_duoc = Không mạng; không đọc doctrine; prompt snapshot/stderr.log không kèm; suite chạy trên bản sao ops/.github (t82 copytree) — không phải trực tiếp trong clone. | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L4 hien_vat_reviewer_vao_kho.duong_dan = KHONG_CO | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L4 hien_vat_reviewer_vao_kho.ghi_chu = scratch/logs/*.json\|log, scratch/mutants/, script tái lập (review_matrix.py, probe*.py, validate_hint.py, extra*.py) ở sandbox ngoài kho. | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L4 tuan_thu_cam_cua_reviewer.commit_them_ngoai_head = 0 | run.head đúng, worktree_sach=true, so_muc_ban=0; không có reflog/snapshot đủ chứng minh không từng tạo commit ngoài head. | KHÔNG ĐO ĐƯỢC; attestation |
| L4 tuan_thu_cam_cua_reviewer.bang_chung = run.json worktree_sach: true; điều phối đo sau lượt: git status --porcelain rỗng. | run.json worktree_sach=true và so_muc_ban=0; thao tác git status riêng của điều phối sau lượt không có receipt thực thi độc lập. | CÓ run.json; nửa điều phối KHÔNG ĐO ĐƯỢC |
| L4 github_submitter_identity.actor = ducthangho | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L4 github_submitter_identity.la_tac_gia_PR = True | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L4 github_submitter_identity.ghi_chu = `ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; uỷ quyền merge là chỉ thị chủ kho #503 comment 5632304817 ("các PR thuộc phiên này thực hiện theo khuyến nghị") + "Tôi chọn A" (#503 comment 5633059702, gen 4 kèm điều kiện dừng). | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L4 github_submitter_identity.phien_van_chuyen = https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L4 anchor.loai = canonical_ancestry | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L4 anchor.cuong_do = cao | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L4 anchor.mo_ta = Blob verdict ghim `9dc8460`. Head đã review `2b52173` là tổ tiên của master (`fe05fa6d`, merge commit #505, hai cha fa717ee + de49fa0; nhánh claude/m9-fetch-auth tuyến tính 62c299a → de49fa0). | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L4 anchor.gioi_han = Vững khi land bằng merge commit hoặc fast-forward; squash phá quan hệ tổ tiên. | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L4 khong_do_duoc[1] = Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L4 khong_do_duoc[2] = run.json/stdout.log/stderr.log không vào kho ⇒ scalar runtime là attestation. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L4 khong_do_duoc[3] = Fetch trên runner GitHub thật, secret masker, receipt/artifact thật (A3/M3): sandbox không mạng — đo ở PR hồ sơ r366 sau land, ghi ở CHANGELOG r366/#503, không ở verdict. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L4 khong_do_duoc[4] = Git 2.31/toàn dải, ảnh ubuntu-latest hiện hành, Windows: không chạy trong sandbox. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L4 delivered = True | Có tệp verdict thật tại commit9dc8460, receipt tạifa09a48; chứng minh giao vào kho | CÓ vào kho |
| L4 delivered_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L4 authoritative_source = repo_file | repo_file: bytes gốc 10 verdict cùng sha256 nguồn; URL ghim đúng blob | CÓ |
| L4 receipt_written_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L4 receipt_written_at_utc = 2026-09-11T11:2xZ | Không có runtime viết receipt; giá trị11:2xZ không là timestamp chính xác. Metadata commit thêm receipt=11:13:20Z; CHANGELOG=11:15:14Z, sớm hơn nhãn 11:2x. Không dùng đồng hồ commit để suy giờ thực viết. | KHÔNG ĐO ĐƯỢC thời điểm thực |
| L4 receipt_khong_khai[1] = Không khai `thu-hoi` đã xanh trên #505 — nó ĐỎ tất định (định nghĩa từ master) tới lúc land; chủ kho quyết merge bằng chỉ thị. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L4 receipt_khong_khai[2] = Không khai A3 đã đạt — chưa đo lúc viết. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L4 receipt_khong_khai[3] = Không khai model đã chạy — codex không đo được. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L4 receipt_khong_khai[4] = Không khai các lease gen 1–3 "hết hạn" hay "bị thu hồi vì lỗi bản vá" — chúng bị thay thế vì hết lượt/vòng theo ADR-0043, chủ kho reroute. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L4 dòng cuối stdout khớp verdict_sha256 | XONG VERDICT sha256=83ee3cd4c4d11059328d9a5002e8fdfabad78d961af5b790c49c3f9971f8795b | CÓ |
| L4 reviewed_files_sha256 trong verdict / .github/workflows/ops-thu-hoi-admission.yml = 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | CÓ |
| L4 reviewed_files_sha256 trong verdict / ops/lease_publish_test.py = eb9fed2b3275352bcffd3708f402367a18cbde3be38b90b81e9cc47be0330547 | eb9fed2b3275352bcffd3708f402367a18cbde3be38b90b81e9cc47be0330547 | CÓ |
| L5 schema_version = 2 | v2 CLI/schema đi qua; parse YAML là integer2 | CÓ |
| L5 receipt_id = pr505-review-5-codex-20260911-885398ce | pr505-review-5-codex-20260911-885398ce; khớp tên file/lượt/short_id/ngày run | CÓ |
| L5 kind = review_delivery_receipt | review_delivery_receipt; hợp lệ ở cổng v2 | CÓ |
| L5 packet_id = wp503 | wp503 cùng packet#503 được 10 verdict/prompt nhắc; không có record cấp lease thật | CÓ đối chiếu văn bản |
| L5 phase_key = M9-FETCH-AUTH | M9-FETCH-AUTH trong spec/10 verdict/prompt | CÓ đối chiếu văn bản |
| L5 luot = 5 | 5 đúng review_round trong verdict | CÓ |
| L5 role = reviewer | verdict là báo cáo reviewer; vai trò runtime ngoài gói không chứng thực | CÓ văn bản |
| L5 provider = codex | mri.provider=openai_codex; header CLI ghi OpenAI Codex và provider:openai | CÓ cấu hình/tên nền |
| L5 executor_provider = claude | claude do prompt và receipt tự khai | KHÔNG ĐO ĐƯỢC danh tính thực |
| L5 cross_provider = True | mri.openai_codex khác executor tự khai claude; không chứng thực hai model thực | CÓ hợp đồng/attestation |
| L5 assurance = cross_reviewed | cross_reviewed với changes_requested; v2 chấp nhận hợp đồng máy + phiên review khác nền tự khai | CÓ mức hợp đồng; không chứng thực model build |
| L5 model_reviewer_identity.provider = openai_codex | openai_codex trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L5 model_reviewer_identity.surface = codex_cli | codex_cli trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L5 model_reviewer_identity.transport = machine | machine trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG; run.json.transport=machine | CÓ |
| L5 model_reviewer_identity.model_da_chay = KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | 0 chuỗi modelUsage trong stdout.log và stderr.log; header chỉ cho cấu hình model:gpt-6-astra. Verdict tự khai GPT-6 / Codex / OpenAI. | CÓ giới hạn KHÔNG ĐO ĐƯỢC |
| L5 nguon_cac_scalar_tren = ĐỐI CHIẾU ĐƯỢC với run.json (ngoài kho, `scratchpad/runs/885398ce/`): run_id/short_id, prompt_sha256, bat_dau_utc, ket_thuc_utc, thoi_luong_giay, ma_thoat, trang_thai, stdout_byte/sha256, stderr_byte/sha256, worktree_sach, head. Dòng cuối stdout `XONG VERDICT sha256=e4e82572…` khớp băm tệp. model_yeu_cau, effort, transport và so_lan_chet_truoc_khi_xong là ATTESTATION điều phối, KHÔNG có khoá tương ứng trong run.json. | Tất cả scalar liệt kê đối chiếu đúng; ngoại lệ câu transport không có key là SAI: run.json có transport=machine. Header stderr hỗ trợ model yêu cầu/effort; số lần chết chưa đo. | KHÔNG — P2 nguon-runtime-xep-sai-transport |
| L5 verdict_path = ops/reviews/pr505-review-5-codex-verdict.md | Tệp thật tồn tại; bytes và tên URL cùng ops/reviews/pr505-review-5-codex-verdict.md | CÓ |
| L5 evidence_url = https://github.com/ducthangho/tra-luat/blob/9dc8460f55a61b8b9670606a62f6db40905d851c/ops/reviews/pr505-review-5-codex-verdict.md | commit9dc8460f55a61b8b9670606a62f6db40905d851c là ancestorHEAD; git show blob đúng đường băm=e4e825726b4c1073fe875f198bc82bd794bfb96b3768a8eac8e95bb46ea13b88 | CÓ |
| L5 evidence_url_ghi_chu = Neo BLOB ghim `9dc8460` — commit ĐẦU TIÊN chứa 10 tệp verdict PR #505 (`git log --all --diff-filter=A`, đúng 1 commit). Bản chiếu công khai sớm hơn: PR #505 comment 5631002727 — chiếu frontmatter, ĐỐI CHIẾU LƯỢT TRƯỚC, kết luận, Findings, Mutant, chua_do_duoc; `## BẢNG ĐO` và các bảng shell/bề mặt lộ token CHỈ có trong tệp này. | “commit đầu tiên” khớp Git. Bản chiếu comment/nội dung bị lược không có response GitHub trong gói. | CÓ phần Git; comment KHÔNG ĐO ĐƯỢC |
| L5 hint_patch.noi_dung = 1 hunk test: fixture token 81 ký tự (vượt ngưỡng wrap 76) | HINT nguồn có 1 hunk; đối chiếu mô tả với HINT/verdict. Kết quả logic mutant là thuật lại nguồn cũ. | CÓ đối chiếu nguồn |
| L5 noi_dung_do_duoc_van_dung[1] = ĐỐI CHIẾU: finding gen2/lượt 1 ĐÃ VÁ THẬT (4 hunk trùng byte). m14 (bỏ -w0) SỐNG vì fixture 16 ký tự cho base64 44 < 76 ⇒ P2 (0 P1). | Tiêu đề Findings/bảng mutant verdict L5 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L5 noi_dung_do_duoc_van_dung[2] = m1–m13 13/13 GIẾT; HINT đổi fixture thành 81 ký tự; suite 147/147. Vòng 2/2 canon của gen 2. | Tiêu đề Findings/bảng mutant verdict L5 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L5 nang_luc_do_cua_goi.mirror = clone mới từ guong.git (fetch sau push 19337fa), detached 19337fa, core.abbrev 7, không nông; nguon/ có spec M9-FETCH-AUTH.md (sha b8200141…) + actionlint 1.7.7 + VERDICT/HINT các lượt trước của chính reviewer; EVIDENCE.md bổ sung từng lượt | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L5 nang_luc_do_cua_goi.chua_do_duoc = Không mạng; không đọc doctrine; prompt snapshot/stderr.log không kèm; suite chạy trên bản sao ops/.github (t82 copytree) — không phải trực tiếp trong clone. | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L5 hien_vat_reviewer_vao_kho.duong_dan = KHONG_CO | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L5 hien_vat_reviewer_vao_kho.ghi_chu = scratch/logs/*.json\|log, scratch/mutants/, script tái lập (review_matrix.py, probe*.py, validate_hint.py, extra*.py) ở sandbox ngoài kho. | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L5 tuan_thu_cam_cua_reviewer.commit_them_ngoai_head = 0 | run.head đúng, worktree_sach=true, so_muc_ban=0; không có reflog/snapshot đủ chứng minh không từng tạo commit ngoài head. | KHÔNG ĐO ĐƯỢC; attestation |
| L5 tuan_thu_cam_cua_reviewer.bang_chung = run.json worktree_sach: true; điều phối đo sau lượt: git status --porcelain rỗng. | run.json worktree_sach=true và so_muc_ban=0; thao tác git status riêng của điều phối sau lượt không có receipt thực thi độc lập. | CÓ run.json; nửa điều phối KHÔNG ĐO ĐƯỢC |
| L5 github_submitter_identity.actor = ducthangho | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L5 github_submitter_identity.la_tac_gia_PR = True | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L5 github_submitter_identity.ghi_chu = `ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; uỷ quyền merge là chỉ thị chủ kho #503 comment 5632304817 ("các PR thuộc phiên này thực hiện theo khuyến nghị") + "Tôi chọn A" (#503 comment 5633059702, gen 4 kèm điều kiện dừng). | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L5 github_submitter_identity.phien_van_chuyen = https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L5 anchor.loai = canonical_ancestry | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L5 anchor.cuong_do = cao | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L5 anchor.mo_ta = Blob verdict ghim `9dc8460`. Head đã review `19337fa` là tổ tiên của master (`fe05fa6d`, merge commit #505, hai cha fa717ee + de49fa0; nhánh claude/m9-fetch-auth tuyến tính 62c299a → de49fa0). | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L5 anchor.gioi_han = Vững khi land bằng merge commit hoặc fast-forward; squash phá quan hệ tổ tiên. | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L5 khong_do_duoc[1] = Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L5 khong_do_duoc[2] = run.json/stdout.log/stderr.log không vào kho ⇒ scalar runtime là attestation. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L5 khong_do_duoc[3] = Fetch trên runner GitHub thật, secret masker, receipt/artifact thật (A3/M3): sandbox không mạng — đo ở PR hồ sơ r366 sau land, ghi ở CHANGELOG r366/#503, không ở verdict. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L5 khong_do_duoc[4] = Git 2.31/toàn dải, ảnh ubuntu-latest hiện hành, Windows: không chạy trong sandbox. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L5 delivered = True | Có tệp verdict thật tại commit9dc8460, receipt tạifa09a48; chứng minh giao vào kho | CÓ vào kho |
| L5 delivered_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L5 authoritative_source = repo_file | repo_file: bytes gốc 10 verdict cùng sha256 nguồn; URL ghim đúng blob | CÓ |
| L5 receipt_written_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L5 receipt_written_at_utc = 2026-09-11T11:2xZ | Không có runtime viết receipt; giá trị11:2xZ không là timestamp chính xác. Metadata commit thêm receipt=11:13:20Z; CHANGELOG=11:15:14Z, sớm hơn nhãn 11:2x. Không dùng đồng hồ commit để suy giờ thực viết. | KHÔNG ĐO ĐƯỢC thời điểm thực |
| L5 receipt_khong_khai[1] = Không khai `thu-hoi` đã xanh trên #505 — nó ĐỎ tất định (định nghĩa từ master) tới lúc land; chủ kho quyết merge bằng chỉ thị. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L5 receipt_khong_khai[2] = Không khai A3 đã đạt — chưa đo lúc viết. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L5 receipt_khong_khai[3] = Không khai model đã chạy — codex không đo được. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L5 receipt_khong_khai[4] = Không khai các lease gen 1–3 "hết hạn" hay "bị thu hồi vì lỗi bản vá" — chúng bị thay thế vì hết lượt/vòng theo ADR-0043, chủ kho reroute. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L5 dòng cuối stdout khớp verdict_sha256 | XONG VERDICT sha256=e4e825726b4c1073fe875f198bc82bd794bfb96b3768a8eac8e95bb46ea13b88 | CÓ |
| L5 reviewed_files_sha256 trong verdict / .github/workflows/ops-thu-hoi-admission.yml = 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | CÓ |
| L5 reviewed_files_sha256 trong verdict / ops/lease_publish_test.py = 2a61f52b737688ebbe573517d8f199b23e3b400edc2f09539e93697a5e04ab6c | 2a61f52b737688ebbe573517d8f199b23e3b400edc2f09539e93697a5e04ab6c | CÓ |
| L6 schema_version = 2 | v2 CLI/schema đi qua; parse YAML là integer2 | CÓ |
| L6 receipt_id = pr505-review-6-codex-20260911-47b042b7 | pr505-review-6-codex-20260911-47b042b7; khớp tên file/lượt/short_id/ngày run | CÓ |
| L6 kind = review_delivery_receipt | review_delivery_receipt; hợp lệ ở cổng v2 | CÓ |
| L6 packet_id = wp503 | wp503 cùng packet#503 được 10 verdict/prompt nhắc; không có record cấp lease thật | CÓ đối chiếu văn bản |
| L6 phase_key = M9-FETCH-AUTH | M9-FETCH-AUTH trong spec/10 verdict/prompt | CÓ đối chiếu văn bản |
| L6 luot = 6 | 6 đúng review_round trong verdict | CÓ |
| L6 role = reviewer | verdict là báo cáo reviewer; vai trò runtime ngoài gói không chứng thực | CÓ văn bản |
| L6 provider = codex | mri.provider=openai_codex; header CLI ghi OpenAI Codex và provider:openai | CÓ cấu hình/tên nền |
| L6 executor_provider = claude | claude do prompt và receipt tự khai | KHÔNG ĐO ĐƯỢC danh tính thực |
| L6 cross_provider = True | mri.openai_codex khác executor tự khai claude; không chứng thực hai model thực | CÓ hợp đồng/attestation |
| L6 assurance = cross_reviewed | cross_reviewed với changes_requested; v2 chấp nhận hợp đồng máy + phiên review khác nền tự khai | CÓ mức hợp đồng; không chứng thực model build |
| L6 model_reviewer_identity.provider = openai_codex | openai_codex trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L6 model_reviewer_identity.surface = codex_cli | codex_cli trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L6 model_reviewer_identity.transport = machine | machine trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG; run.json.transport=machine | CÓ |
| L6 model_reviewer_identity.model_da_chay = KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | 0 chuỗi modelUsage trong stdout.log và stderr.log; header chỉ cho cấu hình model:gpt-6-astra. Verdict tự khai GPT-6 / Codex / OpenAI. | CÓ giới hạn KHÔNG ĐO ĐƯỢC |
| L6 nguon_cac_scalar_tren = ĐỐI CHIẾU ĐƯỢC với run.json (ngoài kho, `scratchpad/runs/47b042b7/`): run_id/short_id, prompt_sha256, bat_dau_utc, ket_thuc_utc, thoi_luong_giay, ma_thoat, trang_thai, stdout_byte/sha256, stderr_byte/sha256, worktree_sach, head. Dòng cuối stdout `XONG VERDICT sha256=e7871b29…` khớp băm tệp. model_yeu_cau, effort, transport và so_lan_chet_truoc_khi_xong là ATTESTATION điều phối, KHÔNG có khoá tương ứng trong run.json. | Tất cả scalar liệt kê đối chiếu đúng; ngoại lệ câu transport không có key là SAI: run.json có transport=machine. Header stderr hỗ trợ model yêu cầu/effort; số lần chết chưa đo. | KHÔNG — P2 nguon-runtime-xep-sai-transport |
| L6 verdict_path = ops/reviews/pr505-review-6-codex-verdict.md | Tệp thật tồn tại; bytes và tên URL cùng ops/reviews/pr505-review-6-codex-verdict.md | CÓ |
| L6 evidence_url = https://github.com/ducthangho/tra-luat/blob/9dc8460f55a61b8b9670606a62f6db40905d851c/ops/reviews/pr505-review-6-codex-verdict.md | commit9dc8460f55a61b8b9670606a62f6db40905d851c là ancestorHEAD; git show blob đúng đường băm=e7871b29012d78b95acd2a50f5f9551051efc3380cea80288d9caf3348db7f9d | CÓ |
| L6 evidence_url_ghi_chu = Neo BLOB ghim `9dc8460` — commit ĐẦU TIÊN chứa 10 tệp verdict PR #505 (`git log --all --diff-filter=A`, đúng 1 commit). Bản chiếu công khai sớm hơn: PR #505 comment 5631810757 — chiếu frontmatter, ĐỐI CHIẾU LƯỢT TRƯỚC, kết luận, Findings, Mutant, chua_do_duoc; `## BẢNG ĐO` và các bảng shell/bề mặt lộ token CHỈ có trong tệp này. | “commit đầu tiên” khớp Git. Bản chiếu comment/nội dung bị lược không có response GitHub trong gói. | CÓ phần Git; comment KHÔNG ĐO ĐƯỢC |
| L6 hint_patch.noi_dung = 1 hunk test: lặp 3 token 81/82/83 ký tự (padding 0/2/1) | HINT nguồn có 1 hunk; đối chiếu mô tả với HINT/verdict. Kết quả logic mutant là thuật lại nguồn cũ. | CÓ đối chiếu nguồn |
| L6 noi_dung_do_duoc_van_dung[1] = ĐỐI CHIẾU: nhánh wrap ĐÃ VÁ THẬT nhưng fixture 81 ký tự (15+81=96 bytes) HẾT padding ⇒ m15 (tr -d '=') SỐNG trên HEAD dù test 19337fa giết được — reviewer tự nhận HINT lượt 5 của mình làm mất độ phủ ⇒ P2 (0 P1). | Tiêu đề Findings/bảng mutant verdict L6 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L6 noi_dung_do_duoc_van_dung[2] = m1–m14 14/14 GIẾT; HINT lặp 3 token 81/82/83; suite 147/147. Vòng 3/3 của gen 2 sau nang_tran (#503 comment 5631624818). | Tiêu đề Findings/bảng mutant verdict L6 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L6 nang_luc_do_cua_goi.mirror = clone mới từ guong.git (fetch sau push 301aac8), detached 301aac8, core.abbrev 7, không nông; nguon/ có spec M9-FETCH-AUTH.md (sha b8200141…) + actionlint 1.7.7 + VERDICT/HINT các lượt trước của chính reviewer; EVIDENCE.md bổ sung từng lượt | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L6 nang_luc_do_cua_goi.chua_do_duoc = Không mạng; không đọc doctrine; prompt snapshot/stderr.log không kèm; suite chạy trên bản sao ops/.github (t82 copytree) — không phải trực tiếp trong clone. | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L6 hien_vat_reviewer_vao_kho.duong_dan = KHONG_CO | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L6 hien_vat_reviewer_vao_kho.ghi_chu = scratch/logs/*.json\|log, scratch/mutants/, script tái lập (review_matrix.py, probe*.py, validate_hint.py, extra*.py) ở sandbox ngoài kho. | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L6 tuan_thu_cam_cua_reviewer.commit_them_ngoai_head = 0 | run.head đúng, worktree_sach=true, so_muc_ban=0; không có reflog/snapshot đủ chứng minh không từng tạo commit ngoài head. | KHÔNG ĐO ĐƯỢC; attestation |
| L6 tuan_thu_cam_cua_reviewer.bang_chung = run.json worktree_sach: true; điều phối đo sau lượt: git status --porcelain rỗng. | run.json worktree_sach=true và so_muc_ban=0; thao tác git status riêng của điều phối sau lượt không có receipt thực thi độc lập. | CÓ run.json; nửa điều phối KHÔNG ĐO ĐƯỢC |
| L6 github_submitter_identity.actor = ducthangho | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L6 github_submitter_identity.la_tac_gia_PR = True | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L6 github_submitter_identity.ghi_chu = `ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; uỷ quyền merge là chỉ thị chủ kho #503 comment 5632304817 ("các PR thuộc phiên này thực hiện theo khuyến nghị") + "Tôi chọn A" (#503 comment 5633059702, gen 4 kèm điều kiện dừng). | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L6 github_submitter_identity.phien_van_chuyen = https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L6 anchor.loai = canonical_ancestry | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L6 anchor.cuong_do = cao | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L6 anchor.mo_ta = Blob verdict ghim `9dc8460`. Head đã review `301aac8` là tổ tiên của master (`fe05fa6d`, merge commit #505, hai cha fa717ee + de49fa0; nhánh claude/m9-fetch-auth tuyến tính 62c299a → de49fa0). | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L6 anchor.gioi_han = Vững khi land bằng merge commit hoặc fast-forward; squash phá quan hệ tổ tiên. | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L6 khong_do_duoc[1] = Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L6 khong_do_duoc[2] = run.json/stdout.log/stderr.log không vào kho ⇒ scalar runtime là attestation. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L6 khong_do_duoc[3] = Fetch trên runner GitHub thật, secret masker, receipt/artifact thật (A3/M3): sandbox không mạng — đo ở PR hồ sơ r366 sau land, ghi ở CHANGELOG r366/#503, không ở verdict. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L6 khong_do_duoc[4] = Git 2.31/toàn dải, ảnh ubuntu-latest hiện hành, Windows: không chạy trong sandbox. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L6 delivered = True | Có tệp verdict thật tại commit9dc8460, receipt tạifa09a48; chứng minh giao vào kho | CÓ vào kho |
| L6 delivered_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L6 authoritative_source = repo_file | repo_file: bytes gốc 10 verdict cùng sha256 nguồn; URL ghim đúng blob | CÓ |
| L6 receipt_written_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L6 receipt_written_at_utc = 2026-09-11T11:2xZ | Không có runtime viết receipt; giá trị11:2xZ không là timestamp chính xác. Metadata commit thêm receipt=11:13:20Z; CHANGELOG=11:15:14Z, sớm hơn nhãn 11:2x. Không dùng đồng hồ commit để suy giờ thực viết. | KHÔNG ĐO ĐƯỢC thời điểm thực |
| L6 receipt_khong_khai[1] = Không khai `thu-hoi` đã xanh trên #505 — nó ĐỎ tất định (định nghĩa từ master) tới lúc land; chủ kho quyết merge bằng chỉ thị. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L6 receipt_khong_khai[2] = Không khai A3 đã đạt — chưa đo lúc viết. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L6 receipt_khong_khai[3] = Không khai model đã chạy — codex không đo được. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L6 receipt_khong_khai[4] = Không khai các lease gen 1–3 "hết hạn" hay "bị thu hồi vì lỗi bản vá" — chúng bị thay thế vì hết lượt/vòng theo ADR-0043, chủ kho reroute. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L6 dòng cuối stdout khớp verdict_sha256 | XONG VERDICT sha256=e7871b29012d78b95acd2a50f5f9551051efc3380cea80288d9caf3348db7f9d | CÓ |
| L6 reviewed_files_sha256 trong verdict / .github/workflows/ops-thu-hoi-admission.yml = 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | CÓ |
| L6 reviewed_files_sha256 trong verdict / ops/lease_publish_test.py = bcc72d708f3e8da80795b1f7f0f98d807591669076770da089fcf850922b18bb | bcc72d708f3e8da80795b1f7f0f98d807591669076770da089fcf850922b18bb | CÓ |
| L7 schema_version = 2 | v2 CLI/schema đi qua; parse YAML là integer2 | CÓ |
| L7 receipt_id = pr505-review-7-codex-20260911-7f38b236 | pr505-review-7-codex-20260911-7f38b236; khớp tên file/lượt/short_id/ngày run | CÓ |
| L7 kind = review_delivery_receipt | review_delivery_receipt; hợp lệ ở cổng v2 | CÓ |
| L7 packet_id = wp503 | wp503 cùng packet#503 được 10 verdict/prompt nhắc; không có record cấp lease thật | CÓ đối chiếu văn bản |
| L7 phase_key = M9-FETCH-AUTH | M9-FETCH-AUTH trong spec/10 verdict/prompt | CÓ đối chiếu văn bản |
| L7 luot = 7 | 7 đúng review_round trong verdict | CÓ |
| L7 role = reviewer | verdict là báo cáo reviewer; vai trò runtime ngoài gói không chứng thực | CÓ văn bản |
| L7 provider = codex | mri.provider=openai_codex; header CLI ghi OpenAI Codex và provider:openai | CÓ cấu hình/tên nền |
| L7 executor_provider = claude | claude do prompt và receipt tự khai | KHÔNG ĐO ĐƯỢC danh tính thực |
| L7 cross_provider = True | mri.openai_codex khác executor tự khai claude; không chứng thực hai model thực | CÓ hợp đồng/attestation |
| L7 assurance = cross_reviewed | cross_reviewed với changes_requested; v2 chấp nhận hợp đồng máy + phiên review khác nền tự khai | CÓ mức hợp đồng; không chứng thực model build |
| L7 model_reviewer_identity.provider = openai_codex | openai_codex trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L7 model_reviewer_identity.surface = codex_cli | codex_cli trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L7 model_reviewer_identity.transport = machine | machine trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG; run.json.transport=machine | CÓ |
| L7 model_reviewer_identity.model_da_chay = KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | 0 chuỗi modelUsage trong stdout.log và stderr.log; header chỉ cho cấu hình model:gpt-6-astra. Verdict tự khai GPT-6 / Codex / OpenAI. | CÓ giới hạn KHÔNG ĐO ĐƯỢC |
| L7 nguon_cac_scalar_tren = ĐỐI CHIẾU ĐƯỢC với run.json (ngoài kho, `scratchpad/runs/7f38b236/`): run_id/short_id, prompt_sha256, bat_dau_utc, ket_thuc_utc, thoi_luong_giay, ma_thoat, trang_thai, stdout_byte/sha256, stderr_byte/sha256, worktree_sach, head. Dòng cuối stdout `XONG VERDICT sha256=43b157ff…` khớp băm tệp. model_yeu_cau, effort, transport và so_lan_chet_truoc_khi_xong là ATTESTATION điều phối, KHÔNG có khoá tương ứng trong run.json. | Tất cả scalar liệt kê đối chiếu đúng; ngoại lệ câu transport không có key là SAI: run.json có transport=machine. Header stderr hỗ trợ model yêu cầu/effort; số lần chết chưa đo. | KHÔNG — P2 nguon-runtime-xep-sai-transport |
| L7 verdict_path = ops/reviews/pr505-review-7-codex-verdict.md | Tệp thật tồn tại; bytes và tên URL cùng ops/reviews/pr505-review-7-codex-verdict.md | CÓ |
| L7 evidence_url = https://github.com/ducthangho/tra-luat/blob/9dc8460f55a61b8b9670606a62f6db40905d851c/ops/reviews/pr505-review-7-codex-verdict.md | commit9dc8460f55a61b8b9670606a62f6db40905d851c là ancestorHEAD; git show blob đúng đường băm=43b157ffe3f0b7092a303ffbc78629f27d3fb2cc6e3c95a3d3f937546b71fa88 | CÓ |
| L7 evidence_url_ghi_chu = Neo BLOB ghim `9dc8460` — commit ĐẦU TIÊN chứa 10 tệp verdict PR #505 (`git log --all --diff-filter=A`, đúng 1 commit). Bản chiếu công khai sớm hơn: PR #505 comment 5632388900 — chiếu frontmatter, ĐỐI CHIẾU LƯỢT TRƯỚC, kết luận, Findings, Mutant, chua_do_duoc; `## BẢNG ĐO` và các bảng shell/bề mặt lộ token CHỈ có trong tệp này. | “commit đầu tiên” khớp Git. Bản chiếu comment/nội dung bị lược không có response GitHub trong gói. | CÓ phần Git; comment KHÔNG ĐO ĐƯỢC |
| L7 hint_patch.noi_dung = 2 hunk test: giữ env bước, chốt TL_TOKEN ∈ {secrets.GITHUB_TOKEN, github.token} | HINT nguồn có 2 hunk; đối chiếu mô tả với HINT/verdict. Kết quả logic mutant là thuật lại nguồn cũ. | CÓ đối chiếu nguồn |
| L7 noi_dung_do_duoc_van_dung[1] = ĐỐI CHIẾU: finding padding ĐÃ VÁ THẬT. m16 (env TL_TOKEN của bước fetch rỗng) SỐNG vì t152 tự cấp token, không kiểm nguồn env YAML ⇒ P2 (0 P1). | Tiêu đề Findings/bảng mutant verdict L7 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L7 noi_dung_do_duoc_van_dung[2] = m1–m15 15/15 GIẾT; m17 (scope hẹp riêng repo) SỐNG hợp lệ; m18–m21 GIẾT. HINT 2 hunk; suite 147/147. Gen 3 lượt 1 (chỉ thị 'chạy đến hết P1, P2'). | Tiêu đề Findings/bảng mutant verdict L7 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L7 nang_luc_do_cua_goi.mirror = clone mới từ guong.git (fetch sau push 8726a1c), detached 8726a1c, core.abbrev 7, không nông; nguon/ có spec M9-FETCH-AUTH.md (sha b8200141…) + actionlint 1.7.7 + VERDICT/HINT các lượt trước của chính reviewer; EVIDENCE.md bổ sung từng lượt | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L7 nang_luc_do_cua_goi.chua_do_duoc = Không mạng; không đọc doctrine; prompt snapshot/stderr.log không kèm; suite chạy trên bản sao ops/.github (t82 copytree) — không phải trực tiếp trong clone. | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L7 hien_vat_reviewer_vao_kho.duong_dan = KHONG_CO | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L7 hien_vat_reviewer_vao_kho.ghi_chu = scratch/logs/*.json\|log, scratch/mutants/, script tái lập (review_matrix.py, probe*.py, validate_hint.py, extra*.py) ở sandbox ngoài kho. | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L7 tuan_thu_cam_cua_reviewer.commit_them_ngoai_head = 0 | run.head đúng, worktree_sach=true, so_muc_ban=0; không có reflog/snapshot đủ chứng minh không từng tạo commit ngoài head. | KHÔNG ĐO ĐƯỢC; attestation |
| L7 tuan_thu_cam_cua_reviewer.bang_chung = run.json worktree_sach: true; điều phối đo sau lượt: git status --porcelain rỗng. | run.json worktree_sach=true và so_muc_ban=0; thao tác git status riêng của điều phối sau lượt không có receipt thực thi độc lập. | CÓ run.json; nửa điều phối KHÔNG ĐO ĐƯỢC |
| L7 github_submitter_identity.actor = ducthangho | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L7 github_submitter_identity.la_tac_gia_PR = True | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L7 github_submitter_identity.ghi_chu = `ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; uỷ quyền merge là chỉ thị chủ kho #503 comment 5632304817 ("các PR thuộc phiên này thực hiện theo khuyến nghị") + "Tôi chọn A" (#503 comment 5633059702, gen 4 kèm điều kiện dừng). | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L7 github_submitter_identity.phien_van_chuyen = https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L7 anchor.loai = canonical_ancestry | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L7 anchor.cuong_do = cao | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L7 anchor.mo_ta = Blob verdict ghim `9dc8460`. Head đã review `8726a1c` là tổ tiên của master (`fe05fa6d`, merge commit #505, hai cha fa717ee + de49fa0; nhánh claude/m9-fetch-auth tuyến tính 62c299a → de49fa0). | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L7 anchor.gioi_han = Vững khi land bằng merge commit hoặc fast-forward; squash phá quan hệ tổ tiên. | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L7 khong_do_duoc[1] = Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L7 khong_do_duoc[2] = run.json/stdout.log/stderr.log không vào kho ⇒ scalar runtime là attestation. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L7 khong_do_duoc[3] = Fetch trên runner GitHub thật, secret masker, receipt/artifact thật (A3/M3): sandbox không mạng — đo ở PR hồ sơ r366 sau land, ghi ở CHANGELOG r366/#503, không ở verdict. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L7 khong_do_duoc[4] = Git 2.31/toàn dải, ảnh ubuntu-latest hiện hành, Windows: không chạy trong sandbox. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L7 delivered = True | Có tệp verdict thật tại commit9dc8460, receipt tạifa09a48; chứng minh giao vào kho | CÓ vào kho |
| L7 delivered_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L7 authoritative_source = repo_file | repo_file: bytes gốc 10 verdict cùng sha256 nguồn; URL ghim đúng blob | CÓ |
| L7 receipt_written_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L7 receipt_written_at_utc = 2026-09-11T11:2xZ | Không có runtime viết receipt; giá trị11:2xZ không là timestamp chính xác. Metadata commit thêm receipt=11:13:20Z; CHANGELOG=11:15:14Z, sớm hơn nhãn 11:2x. Không dùng đồng hồ commit để suy giờ thực viết. | KHÔNG ĐO ĐƯỢC thời điểm thực |
| L7 receipt_khong_khai[1] = Không khai `thu-hoi` đã xanh trên #505 — nó ĐỎ tất định (định nghĩa từ master) tới lúc land; chủ kho quyết merge bằng chỉ thị. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L7 receipt_khong_khai[2] = Không khai A3 đã đạt — chưa đo lúc viết. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L7 receipt_khong_khai[3] = Không khai model đã chạy — codex không đo được. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L7 receipt_khong_khai[4] = Không khai các lease gen 1–3 "hết hạn" hay "bị thu hồi vì lỗi bản vá" — chúng bị thay thế vì hết lượt/vòng theo ADR-0043, chủ kho reroute. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L7 dòng cuối stdout khớp verdict_sha256 | XONG VERDICT sha256=43b157ffe3f0b7092a303ffbc78629f27d3fb2cc6e3c95a3d3f937546b71fa88 | CÓ |
| L7 reviewed_files_sha256 trong verdict / .github/workflows/ops-thu-hoi-admission.yml = 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | CÓ |
| L7 reviewed_files_sha256 trong verdict / ops/lease_publish_test.py = 42a7ac85709a3630d759738cd3214684f42b77d43f45f22faca6aff2727c90e7 | 42a7ac85709a3630d759738cd3214684f42b77d43f45f22faca6aff2727c90e7 | CÓ |
| L8 schema_version = 2 | v2 CLI/schema đi qua; parse YAML là integer2 | CÓ |
| L8 receipt_id = pr505-review-8-codex-20260911-6b6e237b | pr505-review-8-codex-20260911-6b6e237b; khớp tên file/lượt/short_id/ngày run | CÓ |
| L8 kind = review_delivery_receipt | review_delivery_receipt; hợp lệ ở cổng v2 | CÓ |
| L8 packet_id = wp503 | wp503 cùng packet#503 được 10 verdict/prompt nhắc; không có record cấp lease thật | CÓ đối chiếu văn bản |
| L8 phase_key = M9-FETCH-AUTH | M9-FETCH-AUTH trong spec/10 verdict/prompt | CÓ đối chiếu văn bản |
| L8 luot = 8 | 8 đúng review_round trong verdict | CÓ |
| L8 role = reviewer | verdict là báo cáo reviewer; vai trò runtime ngoài gói không chứng thực | CÓ văn bản |
| L8 provider = codex | mri.provider=openai_codex; header CLI ghi OpenAI Codex và provider:openai | CÓ cấu hình/tên nền |
| L8 executor_provider = claude | claude do prompt và receipt tự khai | KHÔNG ĐO ĐƯỢC danh tính thực |
| L8 cross_provider = True | mri.openai_codex khác executor tự khai claude; không chứng thực hai model thực | CÓ hợp đồng/attestation |
| L8 assurance = cross_reviewed | cross_reviewed với changes_requested; v2 chấp nhận hợp đồng máy + phiên review khác nền tự khai | CÓ mức hợp đồng; không chứng thực model build |
| L8 model_reviewer_identity.provider = openai_codex | openai_codex trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L8 model_reviewer_identity.surface = codex_cli | codex_cli trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L8 model_reviewer_identity.transport = machine | machine trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG; run.json.transport=machine | CÓ |
| L8 model_reviewer_identity.model_da_chay = KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | 0 chuỗi modelUsage trong stdout.log và stderr.log; header chỉ cho cấu hình model:gpt-6-astra. Verdict tự khai GPT-6 / Codex / OpenAI. | CÓ giới hạn KHÔNG ĐO ĐƯỢC |
| L8 nguon_cac_scalar_tren = ĐỐI CHIẾU ĐƯỢC với run.json (ngoài kho, `scratchpad/runs/6b6e237b/`): run_id/short_id, prompt_sha256, bat_dau_utc, ket_thuc_utc, thoi_luong_giay, ma_thoat, trang_thai, stdout_byte/sha256, stderr_byte/sha256, worktree_sach, head. Dòng cuối stdout `XONG VERDICT sha256=50566f7c…` khớp băm tệp. model_yeu_cau, effort, transport và so_lan_chet_truoc_khi_xong là ATTESTATION điều phối, KHÔNG có khoá tương ứng trong run.json. | Tất cả scalar liệt kê đối chiếu đúng; ngoại lệ câu transport không có key là SAI: run.json có transport=machine. Header stderr hỗ trợ model yêu cầu/effort; số lần chết chưa đo. | KHÔNG — P2 nguon-runtime-xep-sai-transport |
| L8 verdict_path = ops/reviews/pr505-review-8-codex-verdict.md | Tệp thật tồn tại; bytes và tên URL cùng ops/reviews/pr505-review-8-codex-verdict.md | CÓ |
| L8 evidence_url = https://github.com/ducthangho/tra-luat/blob/9dc8460f55a61b8b9670606a62f6db40905d851c/ops/reviews/pr505-review-8-codex-verdict.md | commit9dc8460f55a61b8b9670606a62f6db40905d851c là ancestorHEAD; git show blob đúng đường băm=50566f7c0110e471696f65032105c90c929f95b90208486022841b68355be922 | CÓ |
| L8 evidence_url_ghi_chu = Neo BLOB ghim `9dc8460` — commit ĐẦU TIÊN chứa 10 tệp verdict PR #505 (`git log --all --diff-filter=A`, đúng 1 commit). Bản chiếu công khai sớm hơn: PR #505 comment 5632623301 — chiếu frontmatter, ĐỐI CHIẾU LƯỢT TRƯỚC, kết luận, Findings, Mutant, chua_do_duoc; `## BẢNG ĐO` và các bảng shell/bề mặt lộ token CHỈ có trong tệp này. | “commit đầu tiên” khớp Git. Bản chiếu comment/nội dung bị lược không có response GitHub trong gói. | CÓ phần Git; comment KHÔNG ĐO ĐƯỢC |
| L8 hint_patch.noi_dung = 1 hunk test: hậu kiểm test -z trên 4 biến AUTH_B64/COUNT/KEY_0/VALUE_0 | HINT nguồn có 1 hunk; đối chiếu mô tả với HINT/verdict. Kết quả logic mutant là thuật lại nguồn cũ. | CÓ đối chiếu nguồn |
| L8 noi_dung_do_duoc_van_dung[1] = ĐỐI CHIẾU: finding nguồn env ĐÃ VÁ THẬT. m22 (export VALUE_0 riêng ngoài nhóm gán tạm) SỐNG vì hậu kiểm chỉ nhìn AUTH_B64/COUNT ⇒ P2 (0 P1). | Tiêu đề Findings/bảng mutant verdict L8 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L8 noi_dung_do_duoc_van_dung[2] = m1–m21 20 GIẾT / 1 SỐNG hợp lệ; HINT 1 dòng test -z trên 4 biến; suite 147/147. | Tiêu đề Findings/bảng mutant verdict L8 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L8 nang_luc_do_cua_goi.mirror = clone mới từ guong.git (fetch sau push 81af1c9), detached 81af1c9, core.abbrev 7, không nông; nguon/ có spec M9-FETCH-AUTH.md (sha b8200141…) + actionlint 1.7.7 + VERDICT/HINT các lượt trước của chính reviewer; EVIDENCE.md bổ sung từng lượt | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L8 nang_luc_do_cua_goi.chua_do_duoc = Không mạng; không đọc doctrine; prompt snapshot/stderr.log không kèm; suite chạy trên bản sao ops/.github (t82 copytree) — không phải trực tiếp trong clone. | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L8 hien_vat_reviewer_vao_kho.duong_dan = KHONG_CO | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L8 hien_vat_reviewer_vao_kho.ghi_chu = scratch/logs/*.json\|log, scratch/mutants/, script tái lập (review_matrix.py, probe*.py, validate_hint.py, extra*.py) ở sandbox ngoài kho. | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L8 tuan_thu_cam_cua_reviewer.commit_them_ngoai_head = 0 | run.head đúng, worktree_sach=true, so_muc_ban=0; không có reflog/snapshot đủ chứng minh không từng tạo commit ngoài head. | KHÔNG ĐO ĐƯỢC; attestation |
| L8 tuan_thu_cam_cua_reviewer.bang_chung = run.json worktree_sach: true; điều phối đo sau lượt: git status --porcelain rỗng. | run.json worktree_sach=true và so_muc_ban=0; thao tác git status riêng của điều phối sau lượt không có receipt thực thi độc lập. | CÓ run.json; nửa điều phối KHÔNG ĐO ĐƯỢC |
| L8 github_submitter_identity.actor = ducthangho | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L8 github_submitter_identity.la_tac_gia_PR = True | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L8 github_submitter_identity.ghi_chu = `ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; uỷ quyền merge là chỉ thị chủ kho #503 comment 5632304817 ("các PR thuộc phiên này thực hiện theo khuyến nghị") + "Tôi chọn A" (#503 comment 5633059702, gen 4 kèm điều kiện dừng). | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L8 github_submitter_identity.phien_van_chuyen = https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L8 anchor.loai = canonical_ancestry | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L8 anchor.cuong_do = cao | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L8 anchor.mo_ta = Blob verdict ghim `9dc8460`. Head đã review `81af1c9` là tổ tiên của master (`fe05fa6d`, merge commit #505, hai cha fa717ee + de49fa0; nhánh claude/m9-fetch-auth tuyến tính 62c299a → de49fa0). | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L8 anchor.gioi_han = Vững khi land bằng merge commit hoặc fast-forward; squash phá quan hệ tổ tiên. | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L8 khong_do_duoc[1] = Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L8 khong_do_duoc[2] = run.json/stdout.log/stderr.log không vào kho ⇒ scalar runtime là attestation. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L8 khong_do_duoc[3] = Fetch trên runner GitHub thật, secret masker, receipt/artifact thật (A3/M3): sandbox không mạng — đo ở PR hồ sơ r366 sau land, ghi ở CHANGELOG r366/#503, không ở verdict. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L8 khong_do_duoc[4] = Git 2.31/toàn dải, ảnh ubuntu-latest hiện hành, Windows: không chạy trong sandbox. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L8 delivered = True | Có tệp verdict thật tại commit9dc8460, receipt tạifa09a48; chứng minh giao vào kho | CÓ vào kho |
| L8 delivered_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L8 authoritative_source = repo_file | repo_file: bytes gốc 10 verdict cùng sha256 nguồn; URL ghim đúng blob | CÓ |
| L8 receipt_written_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L8 receipt_written_at_utc = 2026-09-11T11:2xZ | Không có runtime viết receipt; giá trị11:2xZ không là timestamp chính xác. Metadata commit thêm receipt=11:13:20Z; CHANGELOG=11:15:14Z, sớm hơn nhãn 11:2x. Không dùng đồng hồ commit để suy giờ thực viết. | KHÔNG ĐO ĐƯỢC thời điểm thực |
| L8 receipt_khong_khai[1] = Không khai `thu-hoi` đã xanh trên #505 — nó ĐỎ tất định (định nghĩa từ master) tới lúc land; chủ kho quyết merge bằng chỉ thị. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L8 receipt_khong_khai[2] = Không khai A3 đã đạt — chưa đo lúc viết. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L8 receipt_khong_khai[3] = Không khai model đã chạy — codex không đo được. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L8 receipt_khong_khai[4] = Không khai các lease gen 1–3 "hết hạn" hay "bị thu hồi vì lỗi bản vá" — chúng bị thay thế vì hết lượt/vòng theo ADR-0043, chủ kho reroute. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L8 dòng cuối stdout khớp verdict_sha256 | XONG VERDICT sha256=50566f7c0110e471696f65032105c90c929f95b90208486022841b68355be922 | CÓ |
| L8 reviewed_files_sha256 trong verdict / .github/workflows/ops-thu-hoi-admission.yml = 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | CÓ |
| L8 reviewed_files_sha256 trong verdict / ops/lease_publish_test.py = 7f622c157cffd4705d807e17fc30a571dcdb88f4dbd5f3355e5bbc300fa501be | 7f622c157cffd4705d807e17fc30a571dcdb88f4dbd5f3355e5bbc300fa501be | CÓ |
| L9 schema_version = 2 | v2 CLI/schema đi qua; parse YAML là integer2 | CÓ |
| L9 receipt_id = pr505-review-9-codex-20260911-1f427b9d | pr505-review-9-codex-20260911-1f427b9d; khớp tên file/lượt/short_id/ngày run | CÓ |
| L9 kind = review_delivery_receipt | review_delivery_receipt; hợp lệ ở cổng v2 | CÓ |
| L9 packet_id = wp503 | wp503 cùng packet#503 được 10 verdict/prompt nhắc; không có record cấp lease thật | CÓ đối chiếu văn bản |
| L9 phase_key = M9-FETCH-AUTH | M9-FETCH-AUTH trong spec/10 verdict/prompt | CÓ đối chiếu văn bản |
| L9 luot = 9 | 9 đúng review_round trong verdict | CÓ |
| L9 role = reviewer | verdict là báo cáo reviewer; vai trò runtime ngoài gói không chứng thực | CÓ văn bản |
| L9 provider = codex | mri.provider=openai_codex; header CLI ghi OpenAI Codex và provider:openai | CÓ cấu hình/tên nền |
| L9 executor_provider = claude | claude do prompt và receipt tự khai | KHÔNG ĐO ĐƯỢC danh tính thực |
| L9 cross_provider = True | mri.openai_codex khác executor tự khai claude; không chứng thực hai model thực | CÓ hợp đồng/attestation |
| L9 assurance = cross_reviewed | cross_reviewed với changes_requested; v2 chấp nhận hợp đồng máy + phiên review khác nền tự khai | CÓ mức hợp đồng; không chứng thực model build |
| L9 model_reviewer_identity.provider = openai_codex | openai_codex trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L9 model_reviewer_identity.surface = codex_cli | codex_cli trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L9 model_reviewer_identity.transport = machine | machine trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG; run.json.transport=machine | CÓ |
| L9 model_reviewer_identity.model_da_chay = KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | 0 chuỗi modelUsage trong stdout.log và stderr.log; header chỉ cho cấu hình model:gpt-6-astra. Verdict tự khai GPT-6 / Codex / OpenAI. | CÓ giới hạn KHÔNG ĐO ĐƯỢC |
| L9 nguon_cac_scalar_tren = ĐỐI CHIẾU ĐƯỢC với run.json (ngoài kho, `scratchpad/runs/1f427b9d/`): run_id/short_id, prompt_sha256, bat_dau_utc, ket_thuc_utc, thoi_luong_giay, ma_thoat, trang_thai, stdout_byte/sha256, stderr_byte/sha256, worktree_sach, head. Dòng cuối stdout `XONG VERDICT sha256=8623f20b…` khớp băm tệp. model_yeu_cau, effort, transport và so_lan_chet_truoc_khi_xong là ATTESTATION điều phối, KHÔNG có khoá tương ứng trong run.json. | Tất cả scalar liệt kê đối chiếu đúng; ngoại lệ câu transport không có key là SAI: run.json có transport=machine. Header stderr hỗ trợ model yêu cầu/effort; số lần chết chưa đo. | KHÔNG — P2 nguon-runtime-xep-sai-transport |
| L9 verdict_path = ops/reviews/pr505-review-9-codex-verdict.md | Tệp thật tồn tại; bytes và tên URL cùng ops/reviews/pr505-review-9-codex-verdict.md | CÓ |
| L9 evidence_url = https://github.com/ducthangho/tra-luat/blob/9dc8460f55a61b8b9670606a62f6db40905d851c/ops/reviews/pr505-review-9-codex-verdict.md | commit9dc8460f55a61b8b9670606a62f6db40905d851c là ancestorHEAD; git show blob đúng đường băm=8623f20bad8a67cc08558c26d63d0f026b6224d7f7a31f149dbd71170cdd22c1 | CÓ |
| L9 evidence_url_ghi_chu = Neo BLOB ghim `9dc8460` — commit ĐẦU TIÊN chứa 10 tệp verdict PR #505 (`git log --all --diff-filter=A`, đúng 1 commit). Bản chiếu công khai sớm hơn: PR #505 comment 5632840048 — chiếu frontmatter, ĐỐI CHIẾU LƯỢT TRƯỚC, kết luận, Findings, Mutant, chua_do_duoc; `## BẢNG ĐO` và các bảng shell/bề mặt lộ token CHỈ có trong tệp này. | “commit đầu tiên” khớp Git. Bản chiếu comment/nội dung bị lược không có response GitHub trong gói. | CÓ phần Git; comment KHÔNG ĐO ĐƯỢC |
| L9 hint_patch.noi_dung = 1 hunk test: literal fixture 0123456789abcdef → 0123456789aBcDeF | HINT nguồn có 1 hunk; đối chiếu mô tả với HINT/verdict. Kết quả logic mutant là thuật lại nguồn cũ. | CÓ đối chiếu nguồn |
| L9 noi_dung_do_duoc_van_dung[1] = ĐỐI CHIẾU: finding hậu kiểm ĐÃ VÁ THẬT. m23 (${TL_TOKEN,,} trước encoder) SỐNG vì cả ba fixture toàn chữ thường ⇒ P2 (0 P1); reviewer tự xếp 'cùng mức các finding wrap/padding'. | Tiêu đề Findings/bảng mutant verdict L9 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L9 noi_dung_do_duoc_van_dung[2] = m1–m22 21 GIẾT / 1 SỐNG hợp lệ; m24–m26 GIẾT; HINT 1 literal; suite 147/147. Vòng 3/3 của gen 3 (nang_tran ghi sẵn theo chỉ thị). | Tiêu đề Findings/bảng mutant verdict L9 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L9 nang_luc_do_cua_goi.mirror = clone mới từ guong.git (fetch sau push 3ae4f61), detached 3ae4f61, core.abbrev 7, không nông; nguon/ có spec M9-FETCH-AUTH.md (sha b8200141…) + actionlint 1.7.7 + VERDICT/HINT các lượt trước của chính reviewer; EVIDENCE.md bổ sung từng lượt | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L9 nang_luc_do_cua_goi.chua_do_duoc = Không mạng; không đọc doctrine; prompt snapshot/stderr.log không kèm; suite chạy trên bản sao ops/.github (t82 copytree) — không phải trực tiếp trong clone. | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L9 hien_vat_reviewer_vao_kho.duong_dan = KHONG_CO | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L9 hien_vat_reviewer_vao_kho.ghi_chu = scratch/logs/*.json\|log, scratch/mutants/, script tái lập (review_matrix.py, probe*.py, validate_hint.py, extra*.py) ở sandbox ngoài kho. | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L9 tuan_thu_cam_cua_reviewer.commit_them_ngoai_head = 0 | run.head đúng, worktree_sach=true, so_muc_ban=0; không có reflog/snapshot đủ chứng minh không từng tạo commit ngoài head. | KHÔNG ĐO ĐƯỢC; attestation |
| L9 tuan_thu_cam_cua_reviewer.bang_chung = run.json worktree_sach: true; điều phối đo sau lượt: git status --porcelain rỗng. | run.json worktree_sach=true và so_muc_ban=0; thao tác git status riêng của điều phối sau lượt không có receipt thực thi độc lập. | CÓ run.json; nửa điều phối KHÔNG ĐO ĐƯỢC |
| L9 github_submitter_identity.actor = ducthangho | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L9 github_submitter_identity.la_tac_gia_PR = True | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L9 github_submitter_identity.ghi_chu = `ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; uỷ quyền merge là chỉ thị chủ kho #503 comment 5632304817 ("các PR thuộc phiên này thực hiện theo khuyến nghị") + "Tôi chọn A" (#503 comment 5633059702, gen 4 kèm điều kiện dừng). | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L9 github_submitter_identity.phien_van_chuyen = https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L9 anchor.loai = canonical_ancestry | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L9 anchor.cuong_do = cao | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L9 anchor.mo_ta = Blob verdict ghim `9dc8460`. Head đã review `3ae4f61` là tổ tiên của master (`fe05fa6d`, merge commit #505, hai cha fa717ee + de49fa0; nhánh claude/m9-fetch-auth tuyến tính 62c299a → de49fa0). | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L9 anchor.gioi_han = Vững khi land bằng merge commit hoặc fast-forward; squash phá quan hệ tổ tiên. | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L9 khong_do_duoc[1] = Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L9 khong_do_duoc[2] = run.json/stdout.log/stderr.log không vào kho ⇒ scalar runtime là attestation. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L9 khong_do_duoc[3] = Fetch trên runner GitHub thật, secret masker, receipt/artifact thật (A3/M3): sandbox không mạng — đo ở PR hồ sơ r366 sau land, ghi ở CHANGELOG r366/#503, không ở verdict. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L9 khong_do_duoc[4] = Git 2.31/toàn dải, ảnh ubuntu-latest hiện hành, Windows: không chạy trong sandbox. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L9 delivered = True | Có tệp verdict thật tại commit9dc8460, receipt tạifa09a48; chứng minh giao vào kho | CÓ vào kho |
| L9 delivered_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L9 authoritative_source = repo_file | repo_file: bytes gốc 10 verdict cùng sha256 nguồn; URL ghim đúng blob | CÓ |
| L9 receipt_written_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L9 receipt_written_at_utc = 2026-09-11T11:2xZ | Không có runtime viết receipt; giá trị11:2xZ không là timestamp chính xác. Metadata commit thêm receipt=11:13:20Z; CHANGELOG=11:15:14Z, sớm hơn nhãn 11:2x. Không dùng đồng hồ commit để suy giờ thực viết. | KHÔNG ĐO ĐƯỢC thời điểm thực |
| L9 receipt_khong_khai[1] = Không khai `thu-hoi` đã xanh trên #505 — nó ĐỎ tất định (định nghĩa từ master) tới lúc land; chủ kho quyết merge bằng chỉ thị. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L9 receipt_khong_khai[2] = Không khai A3 đã đạt — chưa đo lúc viết. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L9 receipt_khong_khai[3] = Không khai model đã chạy — codex không đo được. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L9 receipt_khong_khai[4] = Không khai các lease gen 1–3 "hết hạn" hay "bị thu hồi vì lỗi bản vá" — chúng bị thay thế vì hết lượt/vòng theo ADR-0043, chủ kho reroute. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L9 dòng cuối stdout khớp verdict_sha256 | XONG VERDICT sha256=8623f20bad8a67cc08558c26d63d0f026b6224d7f7a31f149dbd71170cdd22c1 | CÓ |
| L9 reviewed_files_sha256 trong verdict / .github/workflows/ops-thu-hoi-admission.yml = 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | CÓ |
| L9 reviewed_files_sha256 trong verdict / ops/lease_publish_test.py = d7d4f9d655edd6c81d9964c573bcf3a6c9ea7e9dcb6d2cca98883cc8bb02beaa | d7d4f9d655edd6c81d9964c573bcf3a6c9ea7e9dcb6d2cca98883cc8bb02beaa | CÓ |
| L10 schema_version = 2 | v2 CLI/schema đi qua; parse YAML là integer2 | CÓ |
| L10 receipt_id = pr505-review-10-codex-20260911-cb013b5c | pr505-review-10-codex-20260911-cb013b5c; khớp tên file/lượt/short_id/ngày run | CÓ |
| L10 kind = review_delivery_receipt | review_delivery_receipt; hợp lệ ở cổng v2 | CÓ |
| L10 packet_id = wp503 | wp503 cùng packet#503 được 10 verdict/prompt nhắc; không có record cấp lease thật | CÓ đối chiếu văn bản |
| L10 phase_key = M9-FETCH-AUTH | M9-FETCH-AUTH trong spec/10 verdict/prompt | CÓ đối chiếu văn bản |
| L10 luot = 10 | 10 đúng review_round trong verdict | CÓ |
| L10 role = reviewer | verdict là báo cáo reviewer; vai trò runtime ngoài gói không chứng thực | CÓ văn bản |
| L10 provider = codex | mri.provider=openai_codex; header CLI ghi OpenAI Codex và provider:openai | CÓ cấu hình/tên nền |
| L10 executor_provider = claude | claude do prompt và receipt tự khai | KHÔNG ĐO ĐƯỢC danh tính thực |
| L10 cross_provider = True | mri.openai_codex khác executor tự khai claude; không chứng thực hai model thực | CÓ hợp đồng/attestation |
| L10 assurance = cross_approved | cross_approved với approve; v2 chấp nhận hợp đồng máy + phiên review khác nền tự khai | CÓ mức hợp đồng; không chứng thực model build |
| L10 model_reviewer_identity.provider = openai_codex | openai_codex trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L10 model_reviewer_identity.surface = codex_cli | codex_cli trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG | CÓ |
| L10 model_reviewer_identity.transport = machine | machine trong _TRANSPORT_CONTRACTS và PROVIDER_HOP_DONG; run.json.transport=machine | CÓ |
| L10 model_reviewer_identity.model_da_chay = KHONG_DO_DUOC — codex exec không xuất modelUsage; reviewer tự khai `GPT-6 / Codex` trong model_tu_khai | 0 chuỗi modelUsage trong stdout.log và stderr.log; header chỉ cho cấu hình model:gpt-6-astra. Verdict tự khai GPT-6 / Codex / OpenAI. | CÓ giới hạn KHÔNG ĐO ĐƯỢC |
| L10 nguon_cac_scalar_tren = ĐỐI CHIẾU ĐƯỢC với run.json (ngoài kho, `scratchpad/runs/cb013b5c/`): run_id/short_id, prompt_sha256, bat_dau_utc, ket_thuc_utc, thoi_luong_giay, ma_thoat, trang_thai, stdout_byte/sha256, stderr_byte/sha256, worktree_sach, head. Dòng cuối stdout `XONG VERDICT sha256=fea4c511…` khớp băm tệp. model_yeu_cau, effort, transport và so_lan_chet_truoc_khi_xong là ATTESTATION điều phối, KHÔNG có khoá tương ứng trong run.json. | Tất cả scalar liệt kê đối chiếu đúng; ngoại lệ câu transport không có key là SAI: run.json có transport=machine. Header stderr hỗ trợ model yêu cầu/effort; số lần chết chưa đo. | KHÔNG — P2 nguon-runtime-xep-sai-transport |
| L10 verdict_path = ops/reviews/pr505-review-10-codex-verdict.md | Tệp thật tồn tại; bytes và tên URL cùng ops/reviews/pr505-review-10-codex-verdict.md | CÓ |
| L10 evidence_url = https://github.com/ducthangho/tra-luat/blob/9dc8460f55a61b8b9670606a62f6db40905d851c/ops/reviews/pr505-review-10-codex-verdict.md | commit9dc8460f55a61b8b9670606a62f6db40905d851c là ancestorHEAD; git show blob đúng đường băm=fea4c51180dc5e2e7c3e9532b1b817df1c55aaf0b0b2dbc536270b26c118f9b1 | CÓ |
| L10 evidence_url_ghi_chu = Neo BLOB ghim `9dc8460` — commit ĐẦU TIÊN chứa 10 tệp verdict PR #505 (`git log --all --diff-filter=A`, đúng 1 commit). Bản chiếu công khai sớm hơn: PR #505 comment 5633349186 — chiếu frontmatter, ĐỐI CHIẾU LƯỢT TRƯỚC, kết luận, Findings, Mutant, chua_do_duoc; `## BẢNG ĐO` và các bảng shell/bề mặt lộ token CHỈ có trong tệp này. | “commit đầu tiên” khớp Git. Bản chiếu comment/nội dung bị lược không có response GitHub trong gói. | CÓ phần Git; comment KHÔNG ĐO ĐƯỢC |
| L10 hint_patch.noi_dung = 0 hunk — approve, không có P1/P2 cần vá | HINT nguồn có 0 hunk; đối chiếu mô tả với HINT/verdict. Kết quả logic mutant là thuật lại nguồn cũ. | CÓ đối chiếu nguồn |
| L10 noi_dung_do_duoc_van_dung[1] = ĐỐI CHIẾU: finding hoa/thường ĐÃ VÁ THẬT (apply trùng byte; kích thước tệp không đổi 304776 B — reviewer chạy python3 -B). m23 SỐNG với test 3ae4f61, GIẾT với HEAD. | Tiêu đề Findings/bảng mutant verdict L10 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L10 noi_dung_do_duoc_van_dung[2] = m1–m34: 33 GIẾT / 1 SỐNG hợp lệ (m17); m27–m34 mới đều GIẾT. Không tìm được mutant âm sống thêm — không suy ra test hoàn chỉnh. | Tiêu đề Findings/bảng mutant verdict L10 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L10 noi_dung_do_duoc_van_dung[3] = Áp điều kiện dừng gen 4 (chỉ P1 hoặc P2 workflow chặn): KHÔNG có finding nào ở cả hai nhóm ⇒ approve; NỢ GHI SANG #499: không có P2 fixture mới; A3/M3 chưa đo. | Tiêu đề Findings/bảng mutant verdict L10 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L10 noi_dung_do_duoc_van_dung[4] = Suite và wrapper 147/147; actionlint 1.7.7 + ShellCheck 0.9.0 rc=0; Git 2.43.0 fetch thật qua helper cục bộ: HEAD nhận H, NHAN==TL_H. | Tiêu đề Findings/bảng mutant verdict L10 và bảng kiểm HINT ở dưới hỗ trợ các số. Git kiểm riêng +11 và các head. Những rc/probe/suite cũ là kết quả loại(c), không chạy lại ở đây. | CÓ theo nguồn; thực thi lịch sử KHÔNG ĐO ĐƯỢC lại |
| L10 nang_luc_do_cua_goi.mirror = clone mới từ guong.git (fetch sau push de49fa0), detached de49fa0, core.abbrev 7, không nông; nguon/ có spec M9-FETCH-AUTH.md (sha b8200141…) + actionlint 1.7.7 + VERDICT/HINT các lượt trước của chính reviewer; EVIDENCE.md bổ sung từng lượt | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L10 nang_luc_do_cua_goi.chua_do_duoc = Không mạng; không đọc doctrine; prompt snapshot/stderr.log không kèm; suite chạy trên bản sao ops/.github (t82 copytree) — không phải trực tiếp trong clone. | Mô tả gói của lượt cũ, không phải gói PR #510 hiện tại (nay có stderr.log). Verdict có khai chạy trên bản sao ops/.github và giới hạn không mạng. Không phục dựng đầy đủ filesystem/clone cũ. | KHÔNG ĐO ĐƯỢC độc lập lịch sử |
| L10 hien_vat_reviewer_vao_kho.duong_dan = KHONG_CO | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L10 hien_vat_reviewer_vao_kho.ghi_chu = scratch/logs/*.json\|log, scratch/mutants/, script tái lập (review_matrix.py, probe*.py, validate_hint.py, extra*.py) ở sandbox ngoài kho. | Diff23 tệp không đưa script/probe/log nguyên bản vào kho; nguon hiện tại có run.json/stdout/stderr và VERDICT/HINT, không có các scratch/logs được dẫn. | CÓ phạm vi gói |
| L10 tuan_thu_cam_cua_reviewer.commit_them_ngoai_head = 0 | run.head đúng, worktree_sach=true, so_muc_ban=0; không có reflog/snapshot đủ chứng minh không từng tạo commit ngoài head. | KHÔNG ĐO ĐƯỢC; attestation |
| L10 tuan_thu_cam_cua_reviewer.bang_chung = run.json worktree_sach: true; điều phối đo sau lượt: git status --porcelain rỗng. | run.json worktree_sach=true và so_muc_ban=0; thao tác git status riêng của điều phối sau lượt không có receipt thực thi độc lập. | CÓ run.json; nửa điều phối KHÔNG ĐO ĐƯỢC |
| L10 github_submitter_identity.actor = ducthangho | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L10 github_submitter_identity.la_tac_gia_PR = True | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L10 github_submitter_identity.ghi_chu = `ADR-0040`: verdict do tài khoản tác giả PR vận chuyển KHÔNG là merge authorization; uỷ quyền merge là chỉ thị chủ kho #503 comment 5632304817 ("các PR thuộc phiên này thực hiện theo khuyến nghị") + "Tôi chọn A" (#503 comment 5633059702, gen 4 kèm điều kiện dừng). | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L10 github_submitter_identity.phien_van_chuyen = https://claude.ai/code/session_01Lnos1VZ4KSzHLG9u4UETiW | Không có response GitHub/phiên claude.ai trong gói; văn bản tự khai tác giả vận chuyển, không coi là merge authorization. | KHÔNG ĐO ĐƯỢC; thuật lại/attestation |
| L10 anchor.loai = canonical_ancestry | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L10 anchor.cuong_do = cao | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L10 anchor.mo_ta = Blob verdict ghim `9dc8460`. Head đã review `de49fa0` là tổ tiên của master (`fe05fa6d`, merge commit #505, hai cha fa717ee + de49fa0; nhánh claude/m9-fetch-auth tuyến tính 62c299a → de49fa0). | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L10 anchor.gioi_han = Vững khi land bằng merge commit hoặc fast-forward; squash phá quan hệ tổ tiên. | Git đã kiểm: blob9dc8460 đúng byte, ancestorHEAD; reviewed head nằm trên chuỗi tuyến tính tới de49fa0, cha thứ 2 fe05fa6; merge/ff qua, squash đỏ. “cao” là mô tả cường độ quan hệ này. | CÓ trong đồ thị hiện có |
| L10 khong_do_duoc[1] = Model build và danh tính model thật của codex exec: không có modelUsage, chỉ có lời tự khai. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L10 khong_do_duoc[2] = run.json/stdout.log/stderr.log không vào kho ⇒ scalar runtime là attestation. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L10 khong_do_duoc[3] = Fetch trên runner GitHub thật, secret masker, receipt/artifact thật (A3/M3): sandbox không mạng — đo ở PR hồ sơ r366 sau land, ghi ở CHANGELOG r366/#503, không ở verdict. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L10 khong_do_duoc[4] = Git 2.31/toàn dải, ảnh ubuntu-latest hiện hành, Windows: không chạy trong sandbox. | Không có modelUsage; raw runtime nằm ngoài cay-kho trong nguon. Không có kết quả runner/mask/artifact A3; hệ nền ngoài Linux không chạy ở lượt này. Câu “đo ở PR hồ sơ” là chỉ nơi nghiệm thu dự kiến, không phải số đo trong verdict. | CÓ giới hạn; sự kiện ngoài gói KHÔNG ĐO ĐƯỢC |
| L10 delivered = True | Có tệp verdict thật tại commit9dc8460, receipt tạifa09a48; chứng minh giao vào kho | CÓ vào kho |
| L10 delivered_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L10 authoritative_source = repo_file | repo_file: bytes gốc 10 verdict cùng sha256 nguồn; URL ghim đúng blob | CÓ |
| L10 receipt_written_by = claude-session | Không có chứng thực runtime của phiên ghi/vận chuyển receipt trong gói | KHÔNG ĐO ĐƯỢC; attestation |
| L10 receipt_written_at_utc = 2026-09-11T11:2xZ | Không có runtime viết receipt; giá trị11:2xZ không là timestamp chính xác. Metadata commit thêm receipt=11:13:20Z; CHANGELOG=11:15:14Z, sớm hơn nhãn 11:2x. Không dùng đồng hồ commit để suy giờ thực viết. | KHÔNG ĐO ĐƯỢC thời điểm thực |
| L10 receipt_khong_khai[1] = Không khai `thu-hoi` đã xanh trên #505 — nó ĐỎ tất định (định nghĩa từ master) tới lúc land; chủ kho quyết merge bằng chỉ thị. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L10 receipt_khong_khai[2] = Không khai A3 đã đạt — chưa đo lúc viết. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L10 receipt_khong_khai[3] = Không khai model đã chạy — codex không đo được. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L10 receipt_khong_khai[4] = Không khai các lease gen 1–3 "hết hạn" hay "bị thu hồi vì lỗi bản vá" — chúng bị thay thế vì hết lượt/vòng theo ADR-0043, chủ kho reroute. | Các giới hạn A3/model thể hiện trong verdict và r366; trạng thái CI/reroute/quyết định chủ kho không có sự kiện GitHub độc lập. Không suy lease hết hạn/bị thu hồi từ hết lượt. | CÓ nhãn giới hạn; sự kiện KHÔNG ĐO ĐƯỢC |
| L10 codex_connector_cung_head.kich_luc = 2026-09-11T10:51:29Z — bỏ draft để merge (merge fe05fa6 lúc 11:06Z) | Không có API response/connector receipt. 10:53:13 trước11:06 là so sánh hai giờ được thuật lại; Git committer timefe05fa6=11:06:29Z không chứng thực sự kiện connector. | KHÔNG ĐO ĐƯỢC; thuật lại (b) |
| L10 codex_connector_cung_head.hoan_tat_luc = 2026-09-11T10:53:13Z — TRƯỚC merge | Không có API response/connector receipt. 10:53:13 trước11:06 là so sánh hai giờ được thuật lại; Git committer timefe05fa6=11:06:29Z không chứng thực sự kiện connector. | KHÔNG ĐO ĐƯỢC; thuật lại (b) |
| L10 codex_connector_cung_head.ket_qua = KHÔNG có review object, KHÔNG có review comment (chỉ bảng tóm tắt Completed, comment 5633351771, commit de49fa0) ⇒ 0 finding theo những gì API trả về — điều phối đọc qua MCP trước khi merge; không phải điều kiện merge, chỉ là kiểm bổ sung. | Không có API response/connector receipt. 10:53:13 trước11:06 là so sánh hai giờ được thuật lại; Git committer timefe05fa6=11:06:29Z không chứng thực sự kiện connector. | KHÔNG ĐO ĐƯỢC; thuật lại (b) |
| L10 dòng cuối stdout khớp verdict_sha256 | XONG VERDICT sha256=fea4c51180dc5e2e7c3e9532b1b817df1c55aaf0b0b2dbc536270b26c118f9b1 | CÓ |
| L10 reviewed_files_sha256 trong verdict / .github/workflows/ops-thu-hoi-admission.yml = 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | 184a54a6ad49a23bae83fb2b00c1613f1426b7248e04641a7042fcda773c9a23 | CÓ |
| L10 reviewed_files_sha256 trong verdict / ops/lease_publish_test.py = 87b85d00ce4627d8f09f1317b72157ead712a99ef20e10f4bd5ebe3d81f9a38b | 87b85d00ce4627d8f09f1317b72157ead712a99ef20e10f4bd5ebe3d81f9a38b | CÓ |

### 5. Đếm finding, mutant và HINT theo từng lượt; 10 hàng mục lục README

| Khai | Đo | Khớp? |
|---|---|---|
| README mục lục L1: \| [`pr505-review-1-codex-verdict.md`](pr505-review-1-codex-verdict.md) \| [`.receipt.yaml`](pr505-review-1-codex-verdict.receipt.yaml) \| `m9-fetch-auth-exec-1-claude-20260911` (#503  gen 1) \| **`changes_requested`** · lượt **1** của PR #505 (packet #503 M9-FETCH-AUTH)  head `62c299a`  khác nền (`codex`; `model_yeu_cau` **`gpt-6-astra`**  `model_da_chay` **KHÔNG ĐO ĐƯỢC**; **1184 s**). P1 `t152-khong-do-header-hieu-luc` + P2 `t152-khong-khoa-dang-ky-mask` (t152 dò chuỗi; m5/m7/m8 SỐNG); HINT chạy chính đoạn shell với Git config thật. \| `62c299a` \| 21 908 \| | Tiêu đề Findings=[1, 1, 0]; ids=['t152-khong-do-header-hieu-luc', 't152-khong-khoa-dang-ky-mask']; head=62c299aa9674aade08263504399539eb60eb89b7; gen=1; giây làm tròn=1184; bytes=21908 | CÓ các số theo nguồn; GitHub KHÔNG ĐO ĐƯỢC |
| L1 số mutant trong receipt/README/CHANGELOG (tập con có ghi rõ phạm vi) | Bảng m1–m9: 6 GIẾT / 3 SỐNG (m5, m7, m8); m17 là SỐNG hợp lệ. Tín dụng sau HINT: 9 GIẾT / 0 SỐNG [] | CÓ đếm từng hàng; không phải chạy lại mutant sản phẩm |
| L1 HINT → head lượt2 | {"round": 1, "apply_rc": 0, "hunks": 1, "whole_byte_match": false, "non_docstring_byte_match": true, "after_hint_bytes": 303788, "next_head_bytes": 304616, "after_hint_sha256": "ffb79d3d222e956c4285c6ea53f8862c2253dcaff1201223a00068093754e9c2", "next_head_sha256": "f51a0cf9e4af56e165ee02f35838c8f4b54f5e70c830aa19889ffd7fa9894223"} | CÓ trừ ngoại lệ docstring L1; P2 |
| L1 BẢNG ĐO trong khoảng 15–23 hàng | 17 hàng dữ liệu, không tính header/separator | Số đo riêng; tổng khoảng 17–25 |
| README mục lục L2: \| [`pr505-review-2-codex-verdict.md`](pr505-review-2-codex-verdict.md) \| [`.receipt.yaml`](pr505-review-2-codex-verdict.receipt.yaml) \| `m9-fetch-auth-exec-1-claude-20260911` (#503  gen 1) \| **`changes_requested`** · lượt **2** của PR #505 (packet #503 M9-FETCH-AUTH)  head `6254570`  khác nền (`codex`; `model_yeu_cau` **`gpt-6-astra`**  `model_da_chay` **KHÔNG ĐO ĐƯỢC**; **814 s**). P1 `t152-bo-sot-fetch-thu-hai` + P2 `t152-stub-khong-do-quyen-transport` (m10/m11 SỐNG); hai finding lượt 1 ĐÃ VÁ THẬT; sau HINT +80/−0 đúng trần. \| `6254570` \| 24 840 \| | Tiêu đề Findings=[1, 1, 0]; ids=['t152-bo-sot-fetch-thu-hai', 't152-stub-khong-do-quyen-transport']; head=6254570b0604b42f9474091b9818dba9cd2b8704; gen=1; giây làm tròn=814; bytes=24840 | CÓ các số theo nguồn; GitHub KHÔNG ĐO ĐƯỢC |
| L2 số mutant trong receipt/README/CHANGELOG (tập con có ghi rõ phạm vi) | Bảng m1–m11: 9 GIẾT / 2 SỐNG (m10, m11); m17 là SỐNG hợp lệ. Tín dụng sau HINT: 11 GIẾT / 0 SỐNG [] | CÓ đếm từng hàng; không phải chạy lại mutant sản phẩm |
| L2 HINT → head lượt3 | {"round": 2, "apply_rc": 0, "hunks": 2, "whole_byte_match": true, "non_docstring_byte_match": true, "after_hint_bytes": 304724, "next_head_bytes": 304724, "after_hint_sha256": "da7aec4701081ea617e25077186afb22c3e9031624b27ea0304386e87c21cbb6", "next_head_sha256": "da7aec4701081ea617e25077186afb22c3e9031624b27ea0304386e87c21cbb6"} | CÓ toàn byte |
| L2 BẢNG ĐO trong khoảng 15–23 hàng | 19 hàng dữ liệu, không tính header/separator | Số đo riêng; tổng khoảng 17–25 |
| README mục lục L3: \| [`pr505-review-3-codex-verdict.md`](pr505-review-3-codex-verdict.md) \| [`.receipt.yaml`](pr505-review-3-codex-verdict.receipt.yaml) \| `m9-fetch-auth-exec-1-claude-20260911` (#503  gen 1) \| **`changes_requested`** · lượt **3** của PR #505 (packet #503 M9-FETCH-AUTH)  head `c851f80`  khác nền (`codex`; `model_yeu_cau` **`gpt-6-astra`**  `model_da_chay` **KHÔNG ĐO ĐƯỢC**; **995 s**). P1 `t152-bo-qua-stderr-truoc-mask` (m12 SỐNG); m1–m11 11/11 GIẾT; vòng 3/3 gen 1 (nang_tran 2→3). \| `c851f80` \| 23 512 \| | Tiêu đề Findings=[1, 0, 0]; ids=['t152-bo-qua-stderr-truoc-mask']; head=c851f8005c0493799df87f87e3e4d586e2746634; gen=1; giây làm tròn=995; bytes=23512 | CÓ các số theo nguồn; GitHub KHÔNG ĐO ĐƯỢC |
| L3 số mutant trong receipt/README/CHANGELOG (tập con có ghi rõ phạm vi) | Bảng m1–m12: 11 GIẾT / 1 SỐNG (m12); m17 là SỐNG hợp lệ. Tín dụng sau HINT: 12 GIẾT / 0 SỐNG [] | CÓ đếm từng hàng; không phải chạy lại mutant sản phẩm |
| L3 HINT → head lượt4 | {"round": 3, "apply_rc": 0, "hunks": 1, "whole_byte_match": true, "non_docstring_byte_match": true, "after_hint_bytes": 304760, "next_head_bytes": 304760, "after_hint_sha256": "eb9fed2b3275352bcffd3708f402367a18cbde3be38b90b81e9cc47be0330547", "next_head_sha256": "eb9fed2b3275352bcffd3708f402367a18cbde3be38b90b81e9cc47be0330547"} | CÓ toàn byte |
| L3 BẢNG ĐO trong khoảng 15–23 hàng | 23 hàng dữ liệu, không tính header/separator | Số đo riêng; tổng khoảng 17–25 |
| README mục lục L4: \| [`pr505-review-4-codex-verdict.md`](pr505-review-4-codex-verdict.md) \| [`.receipt.yaml`](pr505-review-4-codex-verdict.receipt.yaml) \| `m9-fetch-auth-exec-2-claude-20260911` (#503  gen 2) \| **`changes_requested`** · lượt **4** của PR #505 (packet #503 M9-FETCH-AUTH)  head `2b52173`  khác nền (`codex`; `model_yeu_cau` **`gpt-6-astra`**  `model_da_chay` **KHÔNG ĐO ĐƯỢC**; **878 s**). P1 `t152-bo-qua-co-shell-truoc-wf-blob` (m13 SỐNG); m1–m12 12/12 GIẾT; gen 2 lượt 1. \| `2b52173` \| 21 141 \| | Tiêu đề Findings=[1, 0, 0]; ids=['t152-bo-qua-co-shell-truoc-wf-blob']; head=2b52173529365ea04c854c738a1578a97c55a65a; gen=2; giây làm tròn=878; bytes=21141 | CÓ các số theo nguồn; GitHub KHÔNG ĐO ĐƯỢC |
| L4 số mutant trong receipt/README/CHANGELOG (tập con có ghi rõ phạm vi) | Bảng m1–m13: 12 GIẾT / 1 SỐNG (m13); m17 là SỐNG hợp lệ. Tín dụng sau HINT: 13 GIẾT / 0 SỐNG [] | CÓ đếm từng hàng; không phải chạy lại mutant sản phẩm |
| L4 HINT → head lượt5 | {"round": 4, "apply_rc": 0, "hunks": 4, "whole_byte_match": true, "non_docstring_byte_match": true, "after_hint_bytes": 304526, "next_head_bytes": 304526, "after_hint_sha256": "2a61f52b737688ebbe573517d8f199b23e3b400edc2f09539e93697a5e04ab6c", "next_head_sha256": "2a61f52b737688ebbe573517d8f199b23e3b400edc2f09539e93697a5e04ab6c"} | CÓ toàn byte |
| L4 BẢNG ĐO trong khoảng 15–23 hàng | 25 hàng dữ liệu, không tính header/separator | KHÔNG khoảng tổng — P3 |
| README mục lục L5: \| [`pr505-review-5-codex-verdict.md`](pr505-review-5-codex-verdict.md) \| [`.receipt.yaml`](pr505-review-5-codex-verdict.receipt.yaml) \| `m9-fetch-auth-exec-2-claude-20260911` (#503  gen 2) \| **`changes_requested`** · lượt **5** của PR #505 (packet #503 M9-FETCH-AUTH)  head `19337fa`  khác nền (`codex`; `model_yeu_cau` **`gpt-6-astra`**  `model_da_chay` **KHÔNG ĐO ĐƯỢC**; **775 s**). P2 `t152-fixture-ngan-bo-sot-base64-wrap` (m14 SỐNG  fixture 16 ký tự); 0 P1; m1–m13 13/13 GIẾT. \| `19337fa` \| 21 826 \| | Tiêu đề Findings=[0, 1, 0]; ids=['t152-fixture-ngan-bo-sot-base64-wrap']; head=19337fad89ff7fdb47475105d7bdde6e910aedf0; gen=2; giây làm tròn=775; bytes=21826 | CÓ các số theo nguồn; GitHub KHÔNG ĐO ĐƯỢC |
| L5 số mutant trong receipt/README/CHANGELOG (tập con có ghi rõ phạm vi) | Bảng m1–m14: 13 GIẾT / 1 SỐNG (m14); m17 là SỐNG hợp lệ. Tín dụng sau HINT: 14 GIẾT / 0 SỐNG [] | CÓ đếm từng hàng; không phải chạy lại mutant sản phẩm |
| L5 HINT → head lượt6 | {"round": 5, "apply_rc": 0, "hunks": 1, "whole_byte_match": true, "non_docstring_byte_match": true, "after_hint_bytes": 304606, "next_head_bytes": 304606, "after_hint_sha256": "bcc72d708f3e8da80795b1f7f0f98d807591669076770da089fcf850922b18bb", "next_head_sha256": "bcc72d708f3e8da80795b1f7f0f98d807591669076770da089fcf850922b18bb"} | CÓ toàn byte |
| L5 BẢNG ĐO trong khoảng 15–23 hàng | 22 hàng dữ liệu, không tính header/separator | Số đo riêng; tổng khoảng 17–25 |
| README mục lục L6: \| [`pr505-review-6-codex-verdict.md`](pr505-review-6-codex-verdict.md) \| [`.receipt.yaml`](pr505-review-6-codex-verdict.receipt.yaml) \| `m9-fetch-auth-exec-2-claude-20260911` (#503  gen 2) \| **`changes_requested`** · lượt **6** của PR #505 (packet #503 M9-FETCH-AUTH)  head `301aac8`  khác nền (`codex`; `model_yeu_cau` **`gpt-6-astra`**  `model_da_chay` **KHÔNG ĐO ĐƯỢC**; **891 s**). P2 `t152-fixture-mat-nhanh-padding-base64` (m15 SỐNG — do fixture của HINT lượt 5); 0 P1; m1–m14 14/14 GIẾT; vòng 3/3 gen 2. \| `301aac8` \| 23 397 \| | Tiêu đề Findings=[0, 1, 0]; ids=['t152-fixture-mat-nhanh-padding-base64']; head=301aac8e09b2195e0a8e53426d302c910b2a2484; gen=2; giây làm tròn=891; bytes=23397 | CÓ các số theo nguồn; GitHub KHÔNG ĐO ĐƯỢC |
| L6 số mutant trong receipt/README/CHANGELOG (tập con có ghi rõ phạm vi) | Bảng m1–m15: 14 GIẾT / 1 SỐNG (m15); m17 là SỐNG hợp lệ. Tín dụng sau HINT: 15 GIẾT / 0 SỐNG [] | CÓ đếm từng hàng; không phải chạy lại mutant sản phẩm |
| L6 HINT → head lượt7 | {"round": 6, "apply_rc": 0, "hunks": 1, "whole_byte_match": true, "non_docstring_byte_match": true, "after_hint_bytes": 304682, "next_head_bytes": 304682, "after_hint_sha256": "42a7ac85709a3630d759738cd3214684f42b77d43f45f22faca6aff2727c90e7", "next_head_sha256": "42a7ac85709a3630d759738cd3214684f42b77d43f45f22faca6aff2727c90e7"} | CÓ toàn byte |
| L6 BẢNG ĐO trong khoảng 15–23 hàng | 22 hàng dữ liệu, không tính header/separator | Số đo riêng; tổng khoảng 17–25 |
| README mục lục L7: \| [`pr505-review-7-codex-verdict.md`](pr505-review-7-codex-verdict.md) \| [`.receipt.yaml`](pr505-review-7-codex-verdict.receipt.yaml) \| `m9-fetch-auth-exec-3-claude-20260911` (#503  gen 3) \| **`changes_requested`** · lượt **7** của PR #505 (packet #503 M9-FETCH-AUTH)  head `8726a1c`  khác nền (`codex`; `model_yeu_cau` **`gpt-6-astra`**  `model_da_chay` **KHÔNG ĐO ĐƯỢC**; **867 s**). P2 `t152-khong-khoa-nguon-token-trong-env` (m16 SỐNG); 0 P1; m1–m15 15/15 GIẾT  m17 SỐNG hợp lệ; gen 3 lượt 1. \| `8726a1c` \| 23 679 \| | Tiêu đề Findings=[0, 1, 0]; ids=['t152-khong-khoa-nguon-token-trong-env']; head=8726a1c91ac913da041ed021cc787c71ab57ffc6; gen=3; giây làm tròn=867; bytes=23679 | CÓ các số theo nguồn; GitHub KHÔNG ĐO ĐƯỢC |
| L7 số mutant trong receipt/README/CHANGELOG (tập con có ghi rõ phạm vi) | Bảng m1–m21: 19 GIẾT / 2 SỐNG (m16, m17); m17 là SỐNG hợp lệ. Tín dụng sau HINT: 20 GIẾT / 1 SỐNG ['m17'] | CÓ đếm từng hàng; không phải chạy lại mutant sản phẩm |
| L7 HINT → head lượt8 | {"round": 7, "apply_rc": 0, "hunks": 2, "whole_byte_match": true, "non_docstring_byte_match": true, "after_hint_bytes": 304748, "next_head_bytes": 304748, "after_hint_sha256": "7f622c157cffd4705d807e17fc30a571dcdb88f4dbd5f3355e5bbc300fa501be", "next_head_sha256": "7f622c157cffd4705d807e17fc30a571dcdb88f4dbd5f3355e5bbc300fa501be"} | CÓ toàn byte |
| L7 BẢNG ĐO trong khoảng 15–23 hàng | 23 hàng dữ liệu, không tính header/separator | Số đo riêng; tổng khoảng 17–25 |
| README mục lục L8: \| [`pr505-review-8-codex-verdict.md`](pr505-review-8-codex-verdict.md) \| [`.receipt.yaml`](pr505-review-8-codex-verdict.receipt.yaml) \| `m9-fetch-auth-exec-3-claude-20260911` (#503  gen 3) \| **`changes_requested`** · lượt **8** của PR #505 (packet #503 M9-FETCH-AUTH)  head `81af1c9`  khác nền (`codex`; `model_yeu_cau` **`gpt-6-astra`**  `model_da_chay` **KHÔNG ĐO ĐƯỢC**; **991 s**). P2 `t152-bo-sot-header-env-con-sau-fetch` (m22 SỐNG); 0 P1; m1–m21 20 GIẾT / 1 hợp lệ. \| `81af1c9` \| 22 488 \| | Tiêu đề Findings=[0, 1, 0]; ids=['t152-bo-sot-header-env-con-sau-fetch']; head=81af1c90f21e7a7d861200f3a18b3707e0879162; gen=3; giây làm tròn=991; bytes=22488 | CÓ các số theo nguồn; GitHub KHÔNG ĐO ĐƯỢC |
| L8 số mutant trong receipt/README/CHANGELOG (tập con có ghi rõ phạm vi) | Bảng m1–m22: 20 GIẾT / 2 SỐNG (m17, m22); m17 là SỐNG hợp lệ. Tín dụng sau HINT: 21 GIẾT / 1 SỐNG ['m17'] | CÓ đếm từng hàng; không phải chạy lại mutant sản phẩm |
| L8 HINT → head lượt9 | {"round": 8, "apply_rc": 0, "hunks": 1, "whole_byte_match": true, "non_docstring_byte_match": true, "after_hint_bytes": 304776, "next_head_bytes": 304776, "after_hint_sha256": "d7d4f9d655edd6c81d9964c573bcf3a6c9ea7e9dcb6d2cca98883cc8bb02beaa", "next_head_sha256": "d7d4f9d655edd6c81d9964c573bcf3a6c9ea7e9dcb6d2cca98883cc8bb02beaa"} | CÓ toàn byte |
| L8 BẢNG ĐO trong khoảng 15–23 hàng | 22 hàng dữ liệu, không tính header/separator | Số đo riêng; tổng khoảng 17–25 |
| README mục lục L9: \| [`pr505-review-9-codex-verdict.md`](pr505-review-9-codex-verdict.md) \| [`.receipt.yaml`](pr505-review-9-codex-verdict.receipt.yaml) \| `m9-fetch-auth-exec-3-claude-20260911` (#503  gen 3) \| **`changes_requested`** · lượt **9** của PR #505 (packet #503 M9-FETCH-AUTH)  head `3ae4f61`  khác nền (`codex`; `model_yeu_cau` **`gpt-6-astra`**  `model_da_chay` **KHÔNG ĐO ĐƯỢC**; **969 s**). P2 `t152-fixture-bo-sot-token-lan-hoa-thuong` (m23 SỐNG); 0 P1; m1–m22 21 GIẾT / 1 hợp lệ; vòng 3/3 gen 3. \| `3ae4f61` \| 23 860 \| | Tiêu đề Findings=[0, 1, 0]; ids=['t152-fixture-bo-sot-token-lan-hoa-thuong']; head=3ae4f6157636949b2941a218deba5dbaa7df1d30; gen=3; giây làm tròn=969; bytes=23860 | CÓ các số theo nguồn; GitHub KHÔNG ĐO ĐƯỢC |
| L9 số mutant trong receipt/README/CHANGELOG (tập con có ghi rõ phạm vi) | Bảng m1–m26: 24 GIẾT / 2 SỐNG (m17, m23); m17 là SỐNG hợp lệ. Tín dụng sau HINT: 25 GIẾT / 1 SỐNG ['m17'] | CÓ đếm từng hàng; không phải chạy lại mutant sản phẩm |
| L9 HINT → head lượt 10 | {"round": 9, "apply_rc": 0, "hunks": 1, "whole_byte_match": true, "non_docstring_byte_match": true, "after_hint_bytes": 304776, "next_head_bytes": 304776, "after_hint_sha256": "87b85d00ce4627d8f09f1317b72157ead712a99ef20e10f4bd5ebe3d81f9a38b", "next_head_sha256": "87b85d00ce4627d8f09f1317b72157ead712a99ef20e10f4bd5ebe3d81f9a38b"} | CÓ toàn byte |
| L9 BẢNG ĐO trong khoảng 15–23 hàng | 21 hàng dữ liệu, không tính header/separator | Số đo riêng; tổng khoảng 17–25 |
| README mục lục L10: \| [`pr505-review-10-codex-verdict.md`](pr505-review-10-codex-verdict.md) \| [`.receipt.yaml`](pr505-review-10-codex-verdict.receipt.yaml) \| `m9-fetch-auth-exec-4-claude-20260911` (#503  gen 4) \| **`approve`** · lượt **10** của PR #505 (packet #503 M9-FETCH-AUTH)  head `de49fa0`  khác nền (`codex`; `model_yeu_cau` **`gpt-6-astra`**  `model_da_chay` **KHÔNG ĐO ĐƯỢC**; **940 s**). **P1 0 · P2 0 · P3 0** — approve dưới ĐIỀU KIỆN DỪNG gen 4 (không dùng tới); m1–m34 33 GIẾT / 1 SỐNG hợp lệ; NỢ GHI SANG #499 rỗng; A3 chưa đo. Merge `fe05fa6` theo chỉ thị chủ kho (#503 comment 5632304817). \| `de49fa0` \| 23 827 \| | Tiêu đề Findings=[0, 0, 0]; ids=[]; head=de49fa0d077a2a00e9f936240378979a8ebc080c; gen=4; giây làm tròn=940; bytes=23827 | CÓ số/head/gen/runtime; L10 “mục nợ rỗng” SAI |
| L10 số mutant trong receipt/README/CHANGELOG (tập con có ghi rõ phạm vi) | Bảng m1–m34: 33 GIẾT / 1 SỐNG (m17); m17 là SỐNG hợp lệ. Tín dụng sau HINT: L10 không có HINT hunk. | CÓ đếm từng hàng; không phải chạy lại mutant sản phẩm |
| L10 BẢNG ĐO trong khoảng 15–23 hàng | 22 hàng dữ liệu, không tính header/separator | Số đo riêng; tổng khoảng 17–25 |

### 6. Đoạn nguồn README và 14 caveat: so cả nội dung, không chỉ id

Đã chuẩn hoá duy nhất whitespace và dấu in đậm để so README với `mo_ta` + `phai_lam_gi_khi_chay_lai`: **14/14** hàng chứa đủ cả hai trường, mỗi cặp đúng một hàng. README không tự làm mạnh/yếu hơn receipt; các sai lệch dưới đây đã có trong receipt và được chép lên README.

| Khai | Đo | Khớp? |
|---|---|---|
| **PR #505 — nguồn cho 14 cảnh báo và 10 hàng mục lục:** mười verdict codex (khác nền) chấm packet #503 `M9-FETCH-AUTH` (#499 C2a: bước fetch H của `ops-thu-hoi-admission.yml` mang xác thực qua header) qua **bốn generation** lease (exec-1 → exec-4, mỗi lần reroute §12 khi hết lượt/vòng; gen 4 kèm ĐIỀU KIỆN DỪNG chủ kho duyệt); 9 vòng `changes_requested` đều chỉ ở ca test t152, workflow 11 dòng không đổi từ round 1; round 10 `approve` 0/0/0, m1–m34 33 GIẾT / 1 SỐNG hợp lệ. Git, băm/byte, số finding, numstat (+80/−0), suite 147/147, actionlint đối chiếu được trong kho; scalar runtime đối chiếu được với run.json ngoài kho (`28f02cda` … `cb013b5c`); model đã chạy KHÔNG ĐO ĐƯỢC; A3/M3 (runner thật) chưa đo lúc ghi sổ — đo ở PR hồ sơ r366. BẢNG ĐO và các bảng shell/bề mặt lộ token chỉ có trong tệp verdict. | 10 verdict/4 gen/9 changes_requested/1 approve/0/0/0/33 GIẾT+1 SỐNG khớp. Workflowblob ổn định, diff cuối80/0. Git/byte/finding đếm mới; suite lịch sử và mutant đối chiếu từ verdict(c). Runtime có raw run ngoài kho; model thựckhông đo. “A3 chưa đo lúc ghi sổ” khớp r366:93; không phải claim A3 đã xanh. | CÓ phạm vi, với giới hạn nguồn như đã nêu |
| L1 id=CHANGES-REQUESTED-TREN-62c299a-DA-VA-o-6254570-KHONG-phai-trang-thai-cuoi; muc=P2; Verdict chấm head `62c299a` (round 1, gen 1 lượt 1) với 1 P1 / 1 P2 — finding `t152-khong-do-header-hieu-luc`, `t152-khong-khoa-dang-ky-mask`. Executor áp NGUYÊN HINT của chính verdict này tại `6254570`; verdict round 2 đối chiếu từng hunk: ĐÃ VÁ THẬT. Mọi finding của 9 vòng đều ở ca test t152; workflow 11 dòng KHÔNG đổi từ round 1 (sha256 184a54a6…). Hành động: Đọc verdict này làm NGUỒN finding, round 2 làm chốt đóng. Số mutant/tín dụng trong tệp là của head `62c299a`; cây đã land là `de49fa0` (round 10 approve). | ID head/next=62c299a→6254570, đúng parent trực tiếp; số finding/slug khớp tiêu đề. HINT apply rc=0. Workflow cả chuỗi cùng blob. Toàn tệp KHÔNG trùng byte; chỉ ngoài docstring trùng. README và receipt cùng bỏ ngoại lệ. | KHÔNG phần “NGUYÊN” — P2 |
| L2 id=CHANGES-REQUESTED-TREN-6254570-DA-VA-o-c851f80-KHONG-phai-trang-thai-cuoi; muc=P2; Verdict chấm head `6254570` (round 2, gen 1 lượt 2) với 1 P1 / 1 P2 — finding `t152-bo-sot-fetch-thu-hai`, `t152-stub-khong-do-quyen-transport`. Executor áp NGUYÊN HINT của chính verdict này tại `c851f80`; verdict round 3 đối chiếu từng hunk: ĐÃ VÁ THẬT. Mọi finding của 9 vòng đều ở ca test t152; workflow 11 dòng KHÔNG đổi từ round 1 (sha256 184a54a6…). Hành động: Đọc verdict này làm NGUỒN finding, round 3 làm chốt đóng. Số mutant/tín dụng trong tệp là của head `6254570`; cây đã land là `de49fa0` (round 10 approve). | ID head/next=6254570→c851f80, đúng parent trực tiếp; số finding/slug khớp tiêu đề. HINT apply rc=0. Workflow cả chuỗi cùng blob. HINT trùng toàn byte; verdict kế tiếp xác nhận finding đã vá thật. | CÓ theo nguồn và byte |
| L3 id=CHANGES-REQUESTED-TREN-c851f80-DA-VA-o-2b52173-KHONG-phai-trang-thai-cuoi; muc=P2; Verdict chấm head `c851f80` (round 3, gen 1 lượt 3) với 1 P1 / 0 P2 — finding `t152-bo-qua-stderr-truoc-mask`. Executor áp NGUYÊN HINT của chính verdict này tại `2b52173`; verdict round 4 đối chiếu từng hunk: ĐÃ VÁ THẬT. Mọi finding của 9 vòng đều ở ca test t152; workflow 11 dòng KHÔNG đổi từ round 1 (sha256 184a54a6…). Hành động: Đọc verdict này làm NGUỒN finding, round 4 làm chốt đóng. Số mutant/tín dụng trong tệp là của head `c851f80`; cây đã land là `de49fa0` (round 10 approve). | ID head/next=c851f80→2b52173, đúng parent trực tiếp; số finding/slug khớp tiêu đề. HINT apply rc=0. Workflow cả chuỗi cùng blob. HINT trùng toàn byte; verdict kế tiếp xác nhận finding đã vá thật. | CÓ theo nguồn và byte |
| L4 id=CHANGES-REQUESTED-TREN-2b52173-DA-VA-o-19337fa-KHONG-phai-trang-thai-cuoi; muc=P2; Verdict chấm head `2b52173` (round 4, gen 2 lượt 1) với 1 P1 / 0 P2 — finding `t152-bo-qua-co-shell-truoc-wf-blob`. Executor áp NGUYÊN HINT của chính verdict này tại `19337fa`; verdict round 5 đối chiếu từng hunk: ĐÃ VÁ THẬT. Mọi finding của 9 vòng đều ở ca test t152; workflow 11 dòng KHÔNG đổi từ round 1 (sha256 184a54a6…). Hành động: Đọc verdict này làm NGUỒN finding, round 5 làm chốt đóng. Số mutant/tín dụng trong tệp là của head `2b52173`; cây đã land là `de49fa0` (round 10 approve). | ID head/next=2b52173→19337fa, đúng parent trực tiếp; số finding/slug khớp tiêu đề. HINT apply rc=0. Workflow cả chuỗi cùng blob. HINT trùng toàn byte; verdict kế tiếp xác nhận finding đã vá thật. | CÓ theo nguồn và byte |
| L5 id=CHANGES-REQUESTED-TREN-19337fa-DA-VA-o-301aac8-KHONG-phai-trang-thai-cuoi; muc=P2; Verdict chấm head `19337fa` (round 5, gen 2 lượt 2) với 0 P1 / 1 P2 — finding `t152-fixture-ngan-bo-sot-base64-wrap`. Executor áp NGUYÊN HINT của chính verdict này tại `301aac8`; verdict round 6 đối chiếu từng hunk: ĐÃ VÁ THẬT — riêng nhánh wrap; fixture của HINT này làm MẤT nhánh padding (xem round 6). Mọi finding của 9 vòng đều ở ca test t152; workflow 11 dòng KHÔNG đổi từ round 1 (sha256 184a54a6…). Hành động: Đọc verdict này làm NGUỒN finding, round 6 làm chốt đóng. Số mutant/tín dụng trong tệp là của head `19337fa`; cây đã land là `de49fa0` (round 10 approve). | ID head/next=19337fa→301aac8, đúng parent trực tiếp; số finding/slug khớp tiêu đề. HINT apply rc=0. Workflow cả chuỗi cùng blob. Verdict6:35,107–113 xác nhận wrap đã vá thật nhưng HINT 5 gây mất nhánh padding; caveat nói đúng cả hai vế. | CÓ theo nguồn và byte |
| L5 id=HINT-LUOT-5-FIXTURE-81-KY-TU-LAM-MAT-NHANH-PADDING; muc=P2; HINT của verdict này đổi fixture 16 → 81 ký tự để phủ nhánh wrap; 15+81 = 96 bytes chia hết cho 3 nên base64 HẾT padding ⇒ mutant m15 (`tr -d '='`) SỐNG trên `301aac8` dù test `19337fa` giết được. Round 6 tự nhận: *"HINT cũ của reviewer đã chọn fixture không padding; không đổ lỗi cho tác giả vì áp nguyên nó."* Vá ở round 6 bằng ba token 81/82/83. Hành động: Khi thay fixture để phủ một nhánh dữ liệu, kiểm các nhánh dữ liệu KHÁC (độ dài mod 3, wrap 76, hoa/thường) cùng lúc; đừng đọc 'suite 147/147 sau HINT' thành 'độ phủ không giảm'. | Verdict6:35,110–113:16+15=31 bytes,padding==;81+15=96,padding0;HINT 6 tokens81/82/83→input96/97/98,output128/132/132,padding0/2/1. Lời tự nhận reviewer có thật ở:113. HINT 5→301aac8 và HINT 6→8726a1c khớp byte. | CÓ |
| L6 id=CHANGES-REQUESTED-TREN-301aac8-DA-VA-o-8726a1c-KHONG-phai-trang-thai-cuoi; muc=P2; Verdict chấm head `301aac8` (round 6, gen 2 lượt 3) với 0 P1 / 1 P2 — finding `t152-fixture-mat-nhanh-padding-base64`. Executor áp NGUYÊN HINT của chính verdict này tại `8726a1c`; verdict round 7 đối chiếu từng hunk: ĐÃ VÁ THẬT. Mọi finding của 9 vòng đều ở ca test t152; workflow 11 dòng KHÔNG đổi từ round 1 (sha256 184a54a6…). Hành động: Đọc verdict này làm NGUỒN finding, round 7 làm chốt đóng. Số mutant/tín dụng trong tệp là của head `301aac8`; cây đã land là `de49fa0` (round 10 approve). | ID head/next=301aac8→8726a1c, đúng parent trực tiếp; số finding/slug khớp tiêu đề. HINT apply rc=0. Workflow cả chuỗi cùng blob. HINT trùng toàn byte; verdict kế tiếp xác nhận finding đã vá thật. | CÓ theo nguồn và byte |
| L7 id=CHANGES-REQUESTED-TREN-8726a1c-DA-VA-o-81af1c9-KHONG-phai-trang-thai-cuoi; muc=P2; Verdict chấm head `8726a1c` (round 7, gen 3 lượt 1) với 0 P1 / 1 P2 — finding `t152-khong-khoa-nguon-token-trong-env`. Executor áp NGUYÊN HINT của chính verdict này tại `81af1c9`; verdict round 8 đối chiếu từng hunk: ĐÃ VÁ THẬT. Mọi finding của 9 vòng đều ở ca test t152; workflow 11 dòng KHÔNG đổi từ round 1 (sha256 184a54a6…). Hành động: Đọc verdict này làm NGUỒN finding, round 8 làm chốt đóng. Số mutant/tín dụng trong tệp là của head `8726a1c`; cây đã land là `de49fa0` (round 10 approve). | ID head/next=8726a1c→81af1c9, đúng parent trực tiếp; số finding/slug khớp tiêu đề. HINT apply rc=0. Workflow cả chuỗi cùng blob. HINT trùng toàn byte; verdict kế tiếp xác nhận finding đã vá thật. | CÓ theo nguồn và byte |
| L8 id=CHANGES-REQUESTED-TREN-81af1c9-DA-VA-o-3ae4f61-KHONG-phai-trang-thai-cuoi; muc=P2; Verdict chấm head `81af1c9` (round 8, gen 3 lượt 2) với 0 P1 / 1 P2 — finding `t152-bo-sot-header-env-con-sau-fetch`. Executor áp NGUYÊN HINT của chính verdict này tại `3ae4f61`; verdict round 9 đối chiếu từng hunk: ĐÃ VÁ THẬT. Mọi finding của 9 vòng đều ở ca test t152; workflow 11 dòng KHÔNG đổi từ round 1 (sha256 184a54a6…). Hành động: Đọc verdict này làm NGUỒN finding, round 9 làm chốt đóng. Số mutant/tín dụng trong tệp là của head `81af1c9`; cây đã land là `de49fa0` (round 10 approve). | ID head/next=81af1c9→3ae4f61, đúng parent trực tiếp; số finding/slug khớp tiêu đề. HINT apply rc=0. Workflow cả chuỗi cùng blob. HINT trùng toàn byte; verdict kế tiếp xác nhận finding đã vá thật. | CÓ theo nguồn và byte |
| L9 id=CHANGES-REQUESTED-TREN-3ae4f61-DA-VA-o-de49fa0-KHONG-phai-trang-thai-cuoi; muc=P2; Verdict chấm head `3ae4f61` (round 9, gen 3 lượt 3) với 0 P1 / 1 P2 — finding `t152-fixture-bo-sot-token-lan-hoa-thuong`. Executor áp NGUYÊN HINT của chính verdict này tại `de49fa0`; verdict round 10 đối chiếu từng hunk: ĐÃ VÁ THẬT. Mọi finding của 9 vòng đều ở ca test t152; workflow 11 dòng KHÔNG đổi từ round 1 (sha256 184a54a6…). Hành động: Đọc verdict này làm NGUỒN finding, round 10 làm chốt đóng. Số mutant/tín dụng trong tệp là của head `3ae4f61`; cây đã land là `de49fa0` (round 10 approve). | ID head/next=3ae4f61→de49fa0, đúng parent trực tiếp; số finding/slug khớp tiêu đề. HINT apply rc=0. Workflow cả chuỗi cùng blob. HINT trùng toàn byte; verdict kế tiếp xác nhận finding đã vá thật. | CÓ theo nguồn và byte |
| L9 id=HINT-CUNG-KICH-THUOC-TEP-bytecode-cu-lam-phep-do-sai; muc=P2; HINT round 9 đổi 1 literal CÙNG KÍCH THƯỚC tệp (304776 B). Lần đo đầu của executor ở bản sao cho 'm23 SỐNG sau HINT' vì CPython dùng `.pyc` cũ (mtime giây + size không đổi, patch trong cùng giây với lần import trước) — đúng bài học `.pyc` trong CLAUDE.md. Xoá `__pycache__` + `python3 -B` ⇒ m23 ĐỎ; reviewer round 10 cũng chạy `-B` và ghi rõ kích thước không đổi. Hành động: Mọi phép đo trước/sau một HINT cùng kích thước tệp phải xoá `__pycache__` hoặc chạy `python3 -B`; con số 'SỐNG sau HINT' ở #503 comment 5632869731 đã được đính chính ngay trong cùng comment. | Git xác nhận 304776 B ở3ae4f61/de49fa0 và1 literal khác. Verdict10 xác nhận dùng -B nhưng ghi KHÔNG xác minh sự cố executor. Phản chứng scalar cùng size/mtime: riêng -B đọc giá trị cũ 1;xoá cache+-B đọc 2. | KHÔNG chỉ dẫn “hoặc -B” — P2; sự kiện executor KHÔNG ĐO ĐƯỢC |
| L10 id=APPROVE-THEO-DIEU-KIEN-DUNG-GEN-4-chu-kho-duyet-P2-fixture-khong-chan; muc=P2; `approve` round 10 được kết luận dưới ĐIỀU KIỆN DỪNG do chủ kho duyệt (phương án A, #503 comment 5633059702; ghi trong lease `m9-fetch-auth-exec-4-claude-20260911` khoá `dieu_kien_dung`): chỉ P1 hoặc P2 có mutant sống ở WORKFLOW mới chặn; P2 thuần fixture/độ phủ t152 ⇒ approve kèm nợ. Round 10 KHÔNG có finding ở cả hai nhóm và mục `## NỢ GHI SANG #499` rỗng — tức approve này không dùng tới điều kiện nới, nhưng người đọc phải biết điều kiện ấy tồn tại. `approve` vẫn là điều kiện DỪNG, không phải merge authorization (ADR-0040); uỷ quyền merge là chỉ thị chủ kho #503 comment 5632304817. Hành động: Đừng dùng round 10 làm tiền lệ 'P2 fixture không bao giờ chặn' — điều kiện chỉ có hiệu lực cho generation 4 của packet này, sau 9 vòng workflow không đổi. | 0/0/0 khớp; điều kiện gen4 có trong prompt log/verdict. MụcNỢ ở verdict10:164–166 vẫn ghiA3/M3 chưa đo. Quyền chủ kho/lease/comment không có record độc lập. | KHÔNG “mục nợ rỗng” — P2; sự kiện quyền KHÔNG ĐO ĐƯỢC |
| L10 id=A3-M3-CANARY-RUNNER-THAT-CHUA-DO-luc-viet-bien-nhan; muc=P2; Cả 10 verdict đều ghi `chua_do_duoc`: fetch trên runner GitHub thật, secret masker, receipt/artifact thật. Tới lúc viết biên nhận này (sau merge `fe05fa6`), A3 CHƯA đo: PR đầu tiên có sự kiện `pull_request_target` sau land là PR hồ sơ r366 — kết quả ghi ở CHANGELOG r366 và #503, KHÔNG ở verdict. Hành động: Muốn biết bản vá có làm `thu-hoi` xanh trên runner thật không: đọc run `thu-hoi` của PR hồ sơ r366 (hoặc PR kế tiếp), đừng đọc 10 verdict — chúng đo offline. | 10 mục chua_do_duoc đều không chứng thực runner thật. CHANGELOG93 nói KHÔNG khaiA3đạt; không có kết quả xanh trong 109 dòng ở head này. Tên caveat “lúc viết” tách thời điểm rõ; kết quả sự kiện sau đó không có trong gói. | CÓ giới hạn; A3 thật KHÔNG ĐO ĐƯỢC |
| L10 id=BANG-DO-KHONG-LEN-COMMENT-tep-trong-kho-la-ban-du-10-vong; muc=P3; Bản chiếu của cả 10 verdict lên PR #505 (comment 5629894965 … 5633349186) chỉ mang frontmatter, kết luận, ĐỐI CHIẾU, Findings, bảng mutant, chua_do_duoc; `## BẢNG ĐO` (15–23 hàng) và các bảng shell/bề mặt lộ token CHỈ có trong tệp verdict. Hành động: Tra bảng đo trong chính tệp verdict (băm ở biên nhận); sự vắng mặt ở comment không phải reviewer không đo. | 10 bảng dữ liệu=17,19,23,25,22,22,23,22,21,22; nhận diện mụcBẢNGĐO/shell có trongtệp. Không có các comment GitHub để kiểm phần bị lược. | KHÔNG khoảng 15–23 — P3; comment KHÔNG ĐO ĐƯỢC |

### 7. Rà các mệnh đề định lượng trong 109 dòng CHANGELOG r366

| Khai | Đo | Khớp? |
|---|---|---|
| D1–8: r366 / #505 / #503 / #499 C2a; 10 vòng, 4 generation; 10 verdict, 10 receipt, 14 caveat, 10 hàng mục lục; VERSION 1.36.68 | Tên packet/spec, số tệp và VERSION khớp. Generation được đối chiếu với các verdict/prompt, không chứng thực việc cấp lease thật. | CÓ số nội bộ |
| D3–5: r365 chốt26e2555/#506; sau đó #493 e82af37, #507 0bf0ba7, #475 fa717ee, #505 fe05fa6 | Thứ tự Git và subject các merge khớp. #493 dùng r360 trong CHANGELOG; #507 đưa mục r365. | CÓ Git |
| D4: #475 ba spec bản1, A1 nháp0 và lease nháp WINDOWS | git show fa717ee: BO-CONG/M9/WINDOWS đều có heading BẢN1; THU-HOI-LEASE-A1 có heading NHÁP0; lease WINDOWS đuôi .yaml.nhap chưa điền các giá trị chủ kho. Spec cha riêng revision9 cũng tồn tại; câu này không khai toàn bộ danh sách tệp. | CÓ |
| D10–13: 332 refs; thiếu0; lúc11:2xZ; r366 có1 ref, master0, r3670 | Không có log ls-remote trước khi dùng số. Quét toàn bộ snapshot334 refs hiện tại như bảng2; không coi chênh lệch ref hiện tại là bằng chứng lịch sử sai. | KHÔNG ĐO ĐƯỢC trước khi dùng; hiện tại tương thích |
| D15–19: (a) Git/băm/numstat/cổng; (b) GitHub; (c) mutant/probe cũ; 10 run ID; model không đo được | (a) đo mới các phép trong bảng1; (b) không có response GitHub; (c) có verdict/log vận chuyển, thiếu các fixture gốc. Các run ID/digest/runtime khớp; modelUsage có0 lần xuất hiện trong20 log. | CÓ nhãn nguồn |
| D23–29: rc128 could not read Username trên mọi PR; persist-credentials:false; A0; spec bản1 b8200141…; 11 dòng workflow +69 dòng t152 | Spec SHA256 khớp. Numstat cây cuối đúng11/0+69/0. “Mọi PR/không bao giờ xanh” là sự kiện được thuật lại theo(b), không phải phép đo runner ở lượt này. | CÓ Git/code; CI KHÔNG ĐO ĐƯỢC |
| D27–29: đúng1 lời gọi git fetch; mask trước dùng; unset; không ghi config/token vào URL | Diff workflow chỉ gán header cho fetch rồi unset. Các verdict cũ đo ở biên Git/helper; không thay cho runner GitHub thật. | CÓ cấu trúc và nguồn(c) |
| D32–35: 2 tệp, +80/−0; 11/0+69/0; first-parent1, all11; hai cha fa717ee+de49fa0 | Các phép Git trong bảng1 cho đúng các giá trị này tại cây cuối. Head1=61, head2=79, head3–10=80; tất cả không vượt trần80. | CÓ; không kết tội cách hiểu “trong trần” |
| D39–43: gen1–4; 3 lượt; nâng trần2→3; reroute§12; check rc0; state-dir gen2/3/4; các ID comment | Phân bổ: gen1=lượt1–3, gen2=4–6, gen3=7–9, gen4=10 khớp verdict/prompt. Gói không có lease đã phát hành/state/control run độc lập. ID comment được liệt kê riêng bên dưới. | CÓ văn bản; lifecycle thật KHÔNG ĐO ĐƯỢC |
| D45–56: 10 hàng round/gen/head/verdict/P1P2/slug/mutant/run/giây | Đếm tiêu đề Findings, từng hàng mutant và đối chiếu run/scalar/giây làm tròn ở bảng3,5. Các scalar đúng; câu “NỢ…rỗng” của lượt10 sai phạm vi. | CÓ scalar; KHÔNG mục nợ rỗng(P 2) |
| D59–64: ĐÃ VÁ THẬT; áp HINT trùng byte HEAD mọi vòng; ngoại lệ HINT5 mất padding | Tự áp9HINT: HINT1 khác docstring6 dòng; HINT2–9 trùng toàn byte. Verdict6 hỗ trợ wrap đã vá nhưng fixture mới mất nhánh padding. | KHÔNG toàn byte mọi HINT(P 2) |
| D61: Cả9 finding; workflow11 dòng không đổi; SHA184a54a6… trong10 verdict | Có11 finding=4P1+7P2. Số9 là số vòng changes_requested. Cả10băm workflow đúng Git. | KHÔNG 9 finding(P 2); CÓ workflow |
| D62–64: suite147/147, actionlint1.7.7, ShellCheck0.9.0 rc0 mọi head; 10 verdict+receipt neo9dc8460 | Đếm147 ca tại từnghead. Các kết quả chạy lịch sử là(c). Lượt này chạy actionlint1.7.7 trên HEAD, rc0; băm/neo10 verdict được đo lại. | CÓ cấu trúc/nguồn; chưa chạy lại toàn lịch sử |
| D68–71: Sáu vòng3→9; không điểm dừng, luôn dựng được bytes mới; gen4 áp1 literal+1 vòng | 3,4,5,6,7,8,9 là7 vòng. Không có bằng chứng cho mệnh đề luôn tìm được mutant mới. HINT9 có1 literal khác, round10 là1 vòng của gen4. | KHÔNG đếm 6(P 2); CÓ 1 literal/1 vòng |
| D71–72: round10 không dùng điều kiện nới; 0 finding ở cả hai nhóm; không lập tiền lệ P2 fixture | Findings có0P1/P2/P3 mới. Điều kiện gen4 có trong prompt log và verdict; quyền phê duyệt thật của chủ kho không có chứng cứ độc lập. | CÓ nội dung; quyền thật KHÔNG ĐO ĐƯỢC |
| D76–80: HINT9 một literal,304776B; CPython mtime giây+size; xoá cache+-B làm m23 đỏ; comment5632869731 đã đính chính | Một literal và bytes khớp Git. Lịch sử executor là thuật lại; verdict10:111 từ chối xác minh độc lập sự cố cache. Phản chứng mới chỉ chứng minh riêng-B vẫn đọc.pyc cũ. | CÓ bytes; lịch sử KHÔNG ĐO ĐƯỢC; caveat cần vá(P 2) |
| D84–88: comment uỷ quyền 5632304817; ưu tiên#505→#507→#475; ghi-uy-quyen; guard merge rc7 | Không có comment/lease/state-dir/run gốc của guard. Nhãn(b) bao quát; không coi giờ Git là quyền merge. | KHÔNG ĐO ĐƯỢC; nhãn(b) đúng |
| D86–89: #50710:06Z→#47510:52Z→#50511:06Z; #475 merge master hai lần sau#493/#507; manifest xung đột | Git committer time lần lượt10:06:58Z,10:52:03Z,11:06:29Z. Hai merge được chỉ định586e099 và1ef489c có parents đúng. Message kể xung đột manifest; không tái hiện lịch sử xung đột hoặc lý do ưu tiên. | CÓ metadata/hai merge được chỉ định; nguyên nhân KHÔNG ĐO ĐƯỢC |
| D89: connector Completed10:53:13Z trước merge; 0 reviewobject/0 reviewcomment | Không có API response. Receipt10 thuật lại thêm giờ kích10:51:29Z, comment5633351771, headde49fa0. Không dùng các số 0 này thay cho Findings của verdict10. | KHÔNG ĐO ĐƯỢC; nhãn(b) |
| D90–93: A3; hai chữ ký preflight workflow_sha!=S rc12 hoặc rc128; #475 head586e09909:13Z; PR đầu tiên sau land là PR này | Không có CI run log/response. Exacthead r366:93 ghi “mục này KHÔNG khai A3 đã đạt”. Không có mệnh đề đã đo xanh trên#510 trong109 dòng. | KHÔNG ĐO ĐƯỢC sự kiện; CÓ giới hạn rõ |
| D97–99: master26e2555→e82af37, round7/8/10 bắt; 27 commit thiếuops/cong_cu.py; đếm2 hình dạng | Round7 đúng cặp26e→e82; round8 khớpe82; round10 e82→0bf. Đo27 commit và tệp công cụ là đúng. Có thể đếm2 loại sai lệch, nhưng phải giữ từng cặp SHA thật. | KHÔNG các mốc gộp(P 2) |
| D100–101: nợ A3/M3; P3 r365 còn mở; WINDOWS#504 chờ lease, cùng tệp test nay rảnh | Verdict10 ghi A3/M3 chưa đo; receipt2 PR506 có P3 ngoài write set. WINDOWS có lease.nhap chưa điền. Tình trạng đang chờ cấp/đã rảnh không có live lease để chứng thực. | CÓ hồ sơ nợ; live lease KHÔNG ĐO ĐƯỢC |
| D105–108:79=67+2#493+10;11/11 legacy;42 nợ;132 tổng;0 vi phạm;t26/t27;release180;docclaims/doctrine | v2, t26/t27 và release được chạy mới, đúng số. 79−10=69, thêm hai receipt#493 giải thích69−2=67. Không chạy doctrine/docclaims ở lượt này. | CÓ cổng đã chạy; hai cổng còn lại KHÔNG ĐO ĐƯỢC |
| D107–108: manifest tái sinh cùng commit; release-verify lại | 3349c8b thay CHANGELOG+manifest;5 trường manifest đổi, verify strict HEAD xanh. Không có runtime chứng minh chính lệnh generator của tác giả. Đã tái sinh bằng lệnh thật trên bản sao sau HINT và verify xanh. | CÓ hiện vật tương ứng; lịch sử gọi lệnh KHÔNG ĐO ĐƯỢC |

### 8. Danh mục định danh/sự kiện ngoài gói — không suy từ số được nhắc

| Khai | Đo | Khớp? |
|---|---|---|
| GitHub comment id 5629606599 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5629894965 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5630046807 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5630194531 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5630375344 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5630541324 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5630804852 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5631002727 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5631624818 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5631810757 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5632052728 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5632304817 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5632388900 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5632623301 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5632840048 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5632869731 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5633059702 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5633349186 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| GitHub comment id 5633351771 | ID có trong lời khai;không cónội dung/responsecommentGitHubđộc lập để kiểm tác giả,giờ,nội dung,reviewobject hay quyền. | KHÔNG ĐO ĐƯỢC; (b) |
| A3 đãxanh trên#510 theoEVIDENCE/usercontext | Không có run id/CIloghayartifacttrongnguon. CHANGELOGexacthead nói KHÔNG khai đạt. KhôngváPR theo tiềnđềtrái hiệnvật. | KHÔNG ĐO ĐƯỢC; không phải finding PR |
| Hai thời điểm receipt trướcA3 / CHANGELOG sauA3 | Receiptcaveat ghi “lúc viết”; CHANGELOGở head này cũngchưa đạt. Chỉ EVIDENCE thuật lại sau đó xanh. Không cóhai kết quả trái dấu trong PR đểgánmâu thuẫn. | CÓ phân biệtnguồn; A3sau đó KHÔNG ĐO ĐƯỢC |
| Receipt_written_at_utc11:2xZ và lần số hiệu r36611:2xZ | Đây là nhãnxấp xỉ không phải datetime đầy đủ;Gitcommitfa09a48=11:13:20Z,3349c8b=11:15:14Z. Gói không córuntime ghi receipt/scan;không suygiờ thực từ đồng hồ committer. | KHÔNG ĐO ĐƯỢC giờ thực; metadata không trùng nhãn |
| 0 lầnchết của 10phiên | 10 runkếtthúc0/xongkhôngchứng minh chưa có lần thử khác. Lỗi model refresh trongstderr1/3khôngđồngnghĩaphiênreviewchết. | KHÔNG ĐO ĐƯỢC; attestation được ghi |
| Tên lease exec1–4 và generation cấp thật | Không có m9-fetch-auth-exec-*.yamltrong treeHEAD; có phân bổtrongreceipt/verdict/prompt. Không suyđã cấphợp lệ từ tên. | KHÔNG ĐO ĐƯỢC thẩm quyền/thực trạnglease |

## Findings

### r366-tong-hop-truot-so-va-moc [P2]

`CHANGELOG.md:61,68,97` gom các phép đo đúng thành số tổng hợp sai:

- “Cả 9 finding” nhưng đếm **tiêu đề trong mục Findings**, không đếm phần tóm tắt, được **11 finding = 4 P1 + 7 P2** qua 9 vòng. Hai vòng đầu mỗi vòng có hai finding.
- “Sáu vòng liên tiếp (3→9)” bao gồm **7** vòng. Tập đã thử không chứng minh luôn tìm được mutant mới.
- “26e2555 khi thực tế đã e82af37 (round 7/8/10 bắt)” chỉ đúng cặp số ở **round 7**. Verdict 8:47 ghi `e82af37` khớp; verdict 10:50 ghi **prompt e82af37 / đo 0bf0ba7**. Hai “hình dạng” có thể vẫn là 2 loại, nhưng không được thay các số hạng thực tế bằng một cặp SHA chung.

Bằng chứng tái lập: `scratch/luot1/git_measurements.json`, `rounds.json`; `git diff --numstat 27c413c3..<head>`; các tiêu đề Findings của 10 verdict. Đây là lỗi tổng hợp hồ sơ, không phải số P1/P2 trong receipt làm thay đổi kết luận/thẩm quyền: 10 receipt đều khai đúng nên xếp P2. HINT sửa đúng số, mốc và phạm vi câu.

### hint-nguyen-byte-bo-sot-docstring-luot-1 [P2]

`CHANGELOG.md:59–62`, caveat lượt 1 trong receipt và README khai áp NGUYÊN HINT / test trùng byte HEAD. Tự áp `nguon/HINT.rvm9-1.patch` lên test `62c299a`: **rc=0**, tệp sau áp **303788 bytes**, còn test tại `6254570` **304616 bytes**; SHA256 lần lượt **ffb79d3d222e956c4285c6ea53f8862c2253dcaff1201223a00068093754e9c2** và **f51a0cf9e4af56e165ee02f35838c8f4b54f5e70c830aa19889ffd7fa9894223**. Chỉ sau khi bỏ đúng docstring t152 mới khớp byte. Verdict lượt 2:20 tự ghi ngoại lệ này và **6 dòng** chênh; receipt lượt 2 cũng đã khai “trừ docstring”. HINT lượt 2–9 mới khớp toàn tệp tại head kế tiếp.

Nguồn: `scratch/luot1/hint_compare.json` và chín bản sao `hint-1`…`hint-9`. Quan hệ “hai finding đã vá thật” vẫn đúng. Phần sai là tăng mức bằng chứng từ logic trùng byte thành toàn tệp trùng byte; sửa receipt lượt 1 + README + CHANGELOG, không sửa verdict.

### nguon-runtime-xep-sai-transport [P2]

Cả 10 `model_reviewer_identity.nguon_cac_scalar_tren` khai **transport … KHÔNG có khoá tương ứng trong run.json**, gộp nó vào attestation cùng model yêu cầu/effort/số lần chết. Cả **10 run.json có `transport: "machine"`**, bằng đúng receipt; bản gộp `m9-runs.json` cũng có. Không phải thiếu dữ liệu để đối chiếu transport.

`model_yeu_cau` và `effort` không có key trong run.json nhưng **header của cả 10 stderr.log** có `model: gpt-6-astra`, `reasoning effort: xhigh`. Đây là bằng chứng cấu hình yêu cầu, chưa chứng thực model thực chạy. `so_lan_chet_truoc_khi_xong` không có key hoặc lịch sử retry nên **KHÔNG ĐO ĐƯỢC**, nhãn attestation của trường này đúng. Không có một chuỗi `modelUsage` nào trong 20 log; giữ nguyên `model_da_chay: KHONG_DO_DUOC`.

HINT chỉ sửa nhãn nguồn ở 10 receipt. Không nâng assurance hay suy model thực chạy từ header.

### huong-dan-tru-cache-b-van-doc-pyc-cu [P2]

Caveat `HINT-CUNG-KICH-THUOC-TEP-bytecode-cu-lam-phep-do-sai`, trường `phai_lam_gi_khi_chay_lai` của receipt 9 và hàng README tương ứng, chỉ dẫn **xoá cache HOẶC chạy `python3 -B`**. Hai thao tác không tương đương.

Phản chứng an toàn `scratch/luot1/cache-probe/`: import một module chỉ có scalar `generation = 1` để tạo `.pyc`; đổi scalar thành **2**, giữ nguyên **15 bytes** và mtime; chạy tiến trình mới bằng **`python3 -B` vẫn in 1**, rc=0. Xoá `.pyc` rồi chạy `-B` mới **in 2**, rc=0. Kết quả lưu `cache_probe.json`. `-B` ngăn ghi cache mới, không ngăn nạp cache đã tồn tại.

Verdict 9 hỗ trợ HINT đổi một literal; verdict 10:31 hỗ trợ hai tệp đều **304776 B**, và :111 nói rõ **không xác minh độc lập sự cố bytecode của executor**. Hai verdict không chứng minh lựa chọn “hoặc -B” khử được cache cũ. Lịch sử lỗi executor/comment là thuật lại; HINT gắn rõ nguồn và yêu cầu xoá cache cũ trước khi nạp, có thể dùng `-B` sau đó. Không kết luận verdict 10 đã dùng bytecode cũ: không có bằng chứng ấy.

### no-rong-bo-sot-no-a3-m3 [P2]

Receipt 10, caveat `APPROVE-THEO-DIEU-KIEN-DUNG-GEN-4-chu-kho-duyet-P2-fixture-khong-chan`; README cả hàng caveat lẫn mục lục; CHANGELOG bảng round 10 đều gọi **mục `## NỢ GHI SANG #499` “rỗng”**. Mục đó tại verdict 10:164–166 có hai mệnh đề: **không có P2 fixture mới**, nhưng **A3/M3 đã có vẫn chưa đo**, còn nghĩa vụ canary và readback receipt/log/mask thật.

Số finding mới **0/0/0** và “approve không dùng tới điều kiện nới” vẫn đúng. “Không có P2 fixture mới” không đồng nghĩa “mục nợ rỗng”. Hồ sơ cũng nói A3 chưa đo ở các câu khác, nên đây là mâu thuẫn phạm vi của lời tóm tắt, xếp P2. HINT giữ cả hai mệnh đề như nguồn.

### dem-hang-bang-do-sai-khoang [P3]

Receipt 10, caveat `BANG-DO-KHONG-LEN-COMMENT-tep-trong-kho-la-ban-du-10-vong`, và README ghi bảng đo **15–23 hàng**. Đếm riêng hàng dữ liệu của bảng ngay sau `## BẢNG ĐO`, bỏ hàng tên cột/phân cách, dừng trước heading tiếp theo: lượt 1→10 = **17,19,23,25,22,22,23,22,21,22**, khoảng đúng **17–25**. Ví dụ lượt 4 có 25 hàng hiện hữu. Không suy số hàng trên comment GitHub. Sai mô tả kích thước bảng, không làm tăng thẩm quyền; xếp P3. HINT kèm sửa nhỏ này.

## Mutant đã chạy

Mọi phép sửa nằm trong `scratch/luot1/`. Các tên M1–M4 dưới đây thuộc lượt review hồ sơ này, không phải m1–m34 của PR505. Các cổng kiểm nguyên bản, không sửa oracle.

| Khai | Đo | Khớp? |
|---|---|---|
| Đổi verdict_sha256 receipt 10 thành 64 ký tự a (giữ kiểu chuỗi) | v2 rc=1; t26 rc=1; t27 rc=0; release-verify rc=0 | GIẾT đúng chốt chịu lực |
| Xoá duy nhất hàng README caveat A3, giữ receipt | v2 rc=0; t26 rc=0; t27 rc=1;release-verify rc=0 | GIẾT đúng chốt chịu lực |
| Đổi so_p1 receipt 10 từ 0 thành 1 | v2 rc=0; t26 rc=0; t27 rc=0; release-verify rc=0 | SỐNG cả 4 cổng: giới hạn cổng, KHÔNG finding PR |
| Đổi evidence_url tới commit fe05fa6 cùng path không tồn tại | v2 rc=1; t26 rc=0; t27 rc=0; release-verify rc=0 | GIẾT đúng chốt chịu lực |
| land-merge trên fe05fa6 với toàn cây 3349c8b | HEAD=d141a89d956378989d50ccbd84807917db56b2dd; parents=fe05fa6de0a151ced39261ccb97a88026cd1de91 3349c8b2e2b544ce98c2ea088e6c09d71b1092f0; tree=e04df6276bd94660e27d12f14aa111e3131164d1; anchor ancestor rc=0; v2 rc=0; bien_nhan_v2: 79 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 132<br>TỔNG: ĐẠT | Khớp caveat: neo còn |
| land-ff trên fe05fa6 với toàn cây 3349c8b | HEAD=3349c8b2e2b544ce98c2ea088e6c09d71b1092f0; parents=fa09a4854b4ccb137d4d1878711981d0a46450c0; tree=e04df6276bd94660e27d12f14aa111e3131164d1; anchor ancestor rc=0; v2 rc=0; bien_nhan_v2: 79 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 132<br>TỔNG: ĐẠT | Khớp caveat: neo còn |
| land-squash trên fe05fa6 với toàn cây 3349c8b | HEAD=a3208baca97c358d137b1d2656210421c918709f; parents=fe05fa6de0a151ced39261ccb97a88026cd1de91; tree=e04df6276bd94660e27d12f14aa111e3131164d1; anchor ancestor rc=1; v2 rc=1; bien_nhan_v2: 69 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 10 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 132 | Khớp caveat: squash mất canonical ancestry |
| Cache scalar generation 1→2, giữ 15 B/mtime | M5: tạo .pyc cũ→chạy -B in 1;M6:xoá cache→chạy -B in 2; cả hai rc=0. File chỉ có scalar, không dùng nội dung khai thác. | Phản chứng “hoặc -B” được xác nhận |

Manifest hiện tại kiểm 180 tệp và không có đường `ops/reviews/` trong danh sách. Vì vậy release-verify vẫn xanh với M1–M4; t26/t27/v2 mới là các chốt liên quan tới receipt và mục lục.

Lần dựng merge fixture đầu tiên thất bại do cấu hình ký commit kế thừa thử gọi dịch vụ localhost và bị sandbox chặn. Đã tắt signing riêng trong bản sao rồi dựng lại cả ba lối land thành công. Không lấy dữ liệu mạng/GitHub. Không thay cấu hình, ref, index hoặc tệp tracked trong `cay-kho/`. M1 thử đầu bằng 64 số 0 bị YAML hiểu là số; đã bỏ kết quả đó và chạy lại bằng 64 ký tự a, đỏ đúng phép so băm như bảng.

## chua_do_duoc

- Không có `prompt.snapshot` cho cả 10 run. Đối chiếu được digest receipt ↔ run.json ↔ bảng gộp; không băm được snapshot. Không truy cập đường ngoài cwd được ghi trong run.json.
- Không có chứng thực model build/modelUsage. Header chỉ cho cấu hình yêu cầu model/effort và lời tự khai. Không biết số lần review chết trước run thành công; số 0 là attestation. Không chứng thực danh tính thật của executor/người vận chuyển hoặc quyền merge từ tên trường.
- Không có response GitHub cho các comment đã liệt kê, lease phát hành, state generation/reroute, guard rc=7, connector/API 0 objects/0 comments, run CI/A3/M3, secret masking/artifact/receipt thật. Những sự kiện này thuộc nguồn (b). “A3 xanh trên #510” trong EVIDENCE không xuất hiện như một kết quả đã đạt trong 109 dòng r366 ở head review.
- Không có snapshot refs/ls-remote lúc trước khi dùng r366. Đã quét toàn bộ 334 refs hiện có và báo cả hai ref chứa r366; không dùng phép quét hiện tại để khẳng định lịch sử 332 refs đúng hoặc sai tuyệt đối.
- Không chạy lại toàn bộ 147 ca trên từng head, wrapper/ShellCheck trên 10 head, mutant/probe sản phẩm của 10 lượt, hoặc Git 2.31/mọi bản ≥2.31/Windows/ảnh ubuntu-latest thật. Đã đếm 147 ca, chạy actionlint trên HEAD và các cổng hồ sơ được yêu cầu. Số thực thi cũ còn lại chỉ được đối chiếu với verdict/log, thuộc nguồn (c).
- Không kiểm doctrine hoặc ADR/protocol được dẫn như luật, không chạy doctrine-scan/doc-claims-check. Hai lệnh hồ sơ v2/release được người dùng yêu cầu có tự đọc nguồn nội bộ; không mở hoặc đưa nội dung các tài liệu bị cấm vào ngữ cảnh review. Không nhận tín dụng kiểm doctrine ở lượt này.
- Không chứng minh giờ thực viết receipt/scan từ nhãn 11:2xZ hoặc timestamp commit; không chứng minh lịch sử `.pyc` của executor. Phản chứng cache mới chỉ kiểm tính đúng của hướng dẫn chạy lại.

## HINT và kiểm tra kết quả đề nghị

`HINT.patch` là unified diff `patch -p0` từ gốc `cay-kho/`: **12 tệp, 20 hunk** (10 receipt, README, CHANGELOG). Patch sửa cả 5 P2 và P3 nhỏ về số hàng; không đổi 10 verdict hoặc mã sản phẩm, không đưa manifest sửa tay vào patch. Sau khi áp patch, tác giả cần tái sinh manifest bằng `python3 scripts/tl.py release-manifest --deterministic --out RELEASE_MANIFEST.json`.

Đã dry-run và apply thật trên bản sao, rc=0. V2 vẫn 79 ĐẠT/0 vi phạm, t26/t27 QUA. Sau khi tái sinh manifest bằng lệnh trên, release-verify strict JSON có ok=true, expected=checked=180. Cả 10 verdict vẫn khớp nguyên byte `nguon/`. Kho `cay-kho/` cuối lượt vẫn ở HEAD 3349c8b và sạch; không chạy guard/merge/push ở kho gốc.

Hiện vật đo nằm trong `scratch/luot1/`: `audit.py`, `scalar_rows.json`, `literal_byte_checks.json`, `rounds.json`, `git_measurements.json`, `additional_git.json`, `hint_compare.json`, `caveat_pairs.json`, `mutant_counts.json`, `gate_results.json`, `cache_probe.json`, `hint_validation.json`. Các script/bản sao phụ này chưa được land.
