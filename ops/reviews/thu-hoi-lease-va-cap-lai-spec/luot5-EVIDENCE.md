# EVIDENCE — phép đo của phiên điều phối, đo 13:2x–13:4xZ 07-09-2026 trên kho nguồn

Reviewer PHẢI đo lại trong `cay-kho` (mirror đầy đủ, detached tại b416830) — con số dưới đây là LỜI KHAI để đối chiếu, không phải sự thật.

| phép đo | lệnh | giá trị khai |
|---|---|---|
| ref quét | `git for-each-ref --format=%(refname) refs/heads refs/remotes \| grep -v /HEAD$ \| wc -l` | 303 (kho nguồn: 302 remote + 1 local master; trong mirror sẽ KHÁC: master cục bộ có thể vắng — hãy đo và ghi số của mirror) |
| cặp (blob, path) trong ops/leases | script quét mọi ref, `ls-tree -r`, khử trùng theo (blob,path) | 288 |
| đường dẫn lease | như trên, khử theo path | 273 |
| lease_id có >1 blob | | 7 / 273 |
| lease_id CÒN_HẠN | `lease_expires_at_utc` > now | 8 |
| trong đó chưa bia mộ trên ≥1 ref | | 4 (xem SPEC §0) |
| blob r2 KHÔNG bia mộ `26f07b4` nằm trên | `ls-tree` từng ref | 4 ref: heads/master, origin/master, origin/ops/cap-lease-461, origin/claude/soan-spec-3-viec-treo-20260906 |
| blob r2 CÓ bia mộ `fdfde3a` | | 1 ref: origin/ops/lease-wp461-g2 |
| blob mutant #456 KHÔNG bia mộ `8b2103c` | | 11 ref; có bia mộ `1f95042` trên 1 ref |
| `ai-dang-giu .claude/dev/launcher.py` | | NGƯỜI_GIỮ 2, rc=11, 4,1 s; mirror cũng NGƯỜI_GIỮ 2 rc=11 (đã đối chiếu) |
| `ai-dang-giu` 3 đường còn lại của wp461 | | NGƯỜI_GIỮ 2 cả ba |
| `ls-remote` vs `for-each-ref` (tập tên) | `comm -23` / `comm -13` | 0 / 0 |
| actor 5 lượt `ops-publish-lease.yml` gần nhất (run 372–376) | MCP actions_list | ducthangho cả 5, dù commit do phiên agent đẩy |
| `author.login` commit 6635379 (phiên agent) | MCP get_commit | `claude` |
| merge commit b416830 | | author ducthangho, committer web-flow, có gpgsig, `%G?`=E (thiếu khoá) |
| `curl https://github.com/web-flow.gpg` | | HTTP 403, 249 byte |
| `git ls-remote --heads origin 'refs/heads/agent/wp461*'` | | RỖNG |
| `ops/lease_publish_test.py` nền | trực tiếp, không wrapper | 120/121 (t33 đỏ: thiếu actionlint — fail-close cố ý); wrapper có actionlint đang chạy |
| `.claude/dev/packet_loop_test.py` nền | | 278/278, TỔNG: ĐẠT |
| `doc-claims-check --strict` | | rc=0 |
| `doctrine-scan` | | 7 tệp, 0 chỗ chép, rc=0 |
| `_kiem_bia_mo` dùng `any(...)` | `ops/lease_publish.py:595-617` | đúng dòng 606–610 |
| `kiem()` không gọi `_lease_cham_duong` | grep | 0 lần trong `kiem` |
| `ops-publish-lease.yml` lọc | | `ops/leases/**.yaml` `ops/leases/**.yml`; `_quet_lease_toan_kho` dùng `ls-tree -r ops/leases` |

LƯU Ý về mirror: `origin` của `cay-kho` trỏ `../kho.git` (bare cục bộ). `git ls-remote --heads origin` do đó chạy OFFLINE và đếm head của chính mirror (302) — nó KHÔNG phải nguồn có thẩm quyền để so hai nguồn; phép so ấy đã chạy trên kho nguồn TRƯỚC khi clone (0/0). Đừng ghi "ls-remote 302 khớp" thành bằng chứng độ tươi.

## Bổ sung lượt 2 (điều phối đo 14:0x–14:2xZ 07-09-2026)
| phép đo | giá trị |
|---|---|
| `git ls-remote --symref origin HEAD` | `ref: refs/heads/master\tHEAD` |
| `git symbolic-ref refs/remotes/origin/HEAD` trong clone điều phối | `fatal: … not a symbolic ref` |
| `git cat-file -p 6635379 \| grep -c "SSH SIGNATURE"` | 2 (BEGIN/END) — r1 khai "không chữ ký" SAI |
| tệp mang `da_bi_thay_the` trên origin/master / trên #468 | 7 / 11 |
| lease dùng `planned:` (dạng cũ) | 3 (`plat-x4-exec-1`, `plat-x5-exec-1`, `plat-x5-exec-1r2`), đều HẾT_HẠN |
| `_kiem_luoc_do_lease` được gọi từ | `record-lease` (830), `begin-attempt` (872); `record-post`/`transition`/`record-review` 0 lần |
| `packet_loop.py` `--state-dir` mặc định | `.claude/.packet_state` |
| lease #456 lúc 14:27:45Z | CÒN_HẠN (hết 14:30:07Z) |
| lượt 1 run.json | trang_thai xong · ma_thoat 0 · 1842,764 s · stdout 233 B · stderr 777 646 B |
| lease_publish_test với wrapper (actionlint 1.7.7) | 121/121, 8726 B |

## Bổ sung lượt 3 (điều phối đo 14:3x–15:2xZ 07-09-2026)
| phép đo | giá trị |
|---|---|
| lease #456 lúc 14:30:12Z | HẾT_HẠN (hạn 14:30:07Z) |
| `git ls-remote --get-url origin` (kho điều phối) | `https://github.com/ducthangho/tra-luat` |
| 4 lease gate-tach (#463) trên #468: hạn | exec-1 03:37:33Z · 1r2 07:50:35Z · 1r3 09:44:51Z · 1r4 10:17:12Z, đều 2026-09-08; r1→r2→r3 bia mộ, r4 sống |
| `.github/coordination/change-impact.v1.json` + `schemas/change-impact.v1.schema.json` | KHÔNG tồn tại; `schemas/` chỉ có `review_verdict.v1.schema.json` |
| `duyet-khac-danh-tinh.yml` | `pull_request_target` (opened/reopened/synchronize/ready_for_review) + `pull_request_review`; checkout `base.ref`; `permissions: contents: read, pull-requests: read` |
| `ci.yml` lane PR | checkout `fetch-depth: 0`; chạy `bash ops/chay_lease_publish_test.sh` với `AL_VER=1.7.7` (dòng ~206) và `python .claude/dev/packet_loop_test.py` (dòng 133) |
| lượt 2 run.json | xong · ma_thoat 0 · 3322,421 s · stdout 183 B · stderr 4 964 212 B; VERDICT sha256 bb29329551222c3ee75124c549d66516a8e3ee40e6152a1dbfe58fa43a01e9f2; HINT 02b562b36c546f3a9620849c8df3a088306c7e01e211cb21a467f069bcf60c9c |

## Bổ sung lượt 4 (điều phối đo 16:1x–21:0xZ 07-09-2026)
| phép đo | giá trị |
|---|---|
| lượt 3 run.json | xong · ma_thoat 0 · 2737,086 s · stdout 212 B · stderr 3 488 714 B; VERDICT sha256 6b8dde212e39420939eed8795fde335e8dbaf37d9421135346256b1ef53df771; HINT 0a81bd8b2288cc5c235a7e5477785014c0c431005cbb842a8f89713c275662d8 |
| Quyết định chủ kho Q13/Q14 | comment PR #475 id 5575587924, user.login=ducthangho (OWNER), created_at 2026-09-07T20:59:59Z; đã readback qua API: thân chứa "trần mới: 6 lượt" và ngoại lệ closure |
| Đồng hồ container vs GitHub | 21:01:07Z vs HTTP Date 21:01:10Z; uptime 26863 s — không drift; AskUserQuestion chờ ~4h47m |
| `.github/coordination/schemas/` | chỉ `review_verdict.v1.schema.json`; `change-impact.v1.json` + schema đều vắng (xác nhận reviewer lượt 3) |

## Lượt 4a CHẾT (đo 21:29Z 07-09-2026) — tính là lời gọi review thứ 4 theo §12
| phép đo | giá trị |
|---|---|
| run 0b08d653 | trang_thai xong · ma_thoat 1 · 1601,457 s · stdout **0 B** · stderr 1 891 237 B · 183 508 token |
| nguyên nhân | stderr đuôi: `ERROR: This content was flagged for possible cybersecurity risk` ×2 — bộ lọc nền bắn khi reviewer TỰ SOẠN probe dựng remote helper/config độc hại (mục 2(a) prompt 4a). KHÔNG phải `Connection refused`, KHÔNG phải proxy |
| hệ quả | theo §12 lời gọi đã sinh output ⇒ đếm: đã dùng **4/6**; lần phóng lại (4b) là lời gọi **5/6** |
| `scratch/` của 4a | giữ nguyên (coverage_r4.py, followup_r4.py, probes-r4.json, …) để 4b tái dùng, không dựng lại |

## Bổ sung lượt 5 (điều phối đo 22:0xZ 07-09-2026)
| phép đo | giá trị |
|---|---|
| lượt 4b run.json (4cd80fb4) | xong · ma_thoat 0 · 2076,6 s · stdout 231 B · stderr 743 428 B; VERDICT sha256 7d3017ecf3fe2cd3117c35150b9ba63d6ec76b7a4dd8694ac7065622d7e17f77; HINT 4a0321fd79f2ec0e1ea330dd7526e8aaf4cd7dbdb20c0be211a7d3e4a2751706 |
| quyết định chủ kho ~22:0xZ | dùng lời gọi 6/6 trên r5 (ghi §0 spec, commit e5989c3); reviewer 4b khuyến nghị dừng/ADR — chủ kho chốt tiếp |
| check-run `pull_request_target` gắn với H | `cong` (duyet-khac-danh-tinh.yml) id 101767296495 dưới head 1ebd86e của PR #475 (đo lượt 1); lặp lại trên 5a2616c, 3c0cf91, ead8959, 12fa79c, c1a5039, e5989c3 |
