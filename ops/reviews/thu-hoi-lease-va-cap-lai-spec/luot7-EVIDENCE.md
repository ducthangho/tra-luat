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

## Bổ sung lượt 6 (điều phối = phiên 2, container MỚI; đo 03:0x–03:2xZ 08-09-2026)
| phép đo | giá trị |
|---|---|
| lượt 5 run.json (phiên 1 khai, README hiện vật) | xong · ma_thoat 0 · 2394,7 s; VERDICT sha256 1596d5627f62aa9958beac4655a9b7135d565bfb4f9949e3d262f64196f595e0; HINT 8ca8474be2654a60d9e5a98d688f442e940c8ab12521a4f07697c25ef4621ab9; PROMPT 704183b1… |
| r6 | commit `2aee80a`, sha256 `f78135cff428f0744476d7f27426f459d926578c4bac4a4339928330c4a0d6a5`; vá theo HINT lượt 5 (12 hunk); CHƯA lượt nào review |
| quyết định chủ kho tại checkpoint | comment PR #475 id **5578460203**, user.login=ducthangho (OWNER), created_at 2026-09-08T03:03:21Z; readback qua MCP: "review #475 tới hết P1", bộ đếm KHÔNG reset, lời gọi kế = 7, không sửa mã khi chưa có lease |
| head nhánh spec / base / origin/master | `0ecee1f` (commit bàn giao, sau r6) / `b416830` (merge-base, không đổi) / `585c7d5` — master đi **48** commit, nhánh spec **9** commit riêng; nhánh spec KHÔNG merge master |
| kho điều phối | clone ban đầu **shallow** (`--is-shallow-repository` = true, chỉ 3 ref) ⇒ `git fetch --unshallow origin '+refs/heads/*:refs/remotes/origin/*'` ⇒ false |
| `ls-remote --heads` vs `for-each-ref` (TẬP TÊN, bỏ HEAD) | **309 / 309**; `comm -23` = 0 · `comm -13` = 0 (đo SAU fetch đủ; trước fetch là mù 3/309) |
| ref theo công thức spec (kho điều phối) | **310** = 309 remote + 1 local (`claude/spec-…`); lượt 1–5 khai 303 = 302 + 1 ⇒ máy chủ có thêm **7** nhánh từ 07-09 |
| mirror `cay-kho` | clone từ bare `kho.git` chỉ được 42 ref (1 head + tag) ⇒ fetch thêm `+refs/remotes/origin/*:refs/remotes/origin/*` ⇒ for-each-ref tổng 350; công thức spec **310**; HEAD detached `b416830`; `status --porcelain` chỉ `?? ops/specs/…` (spec untracked); không shallow |
| lease CÒN_HẠN trên HEAD nhánh spec (`ops/leases/`, clock 03:10Z 08-09) | **1** (`wp461-…-exec-1r2`, hạn 05:27:42Z 08-09, không `da_bi_thay_the` trên cây này) |
| `ai-dang-giu .claude/dev/launcher.py` (kho điều phối, 310 ref) | `NGƯỜI_GIỮ 2`: g2 (CÒN_HẠN, ref `ops/lease-wp461-g2`) + r2 (CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ trên ref ấy) — rc KHÔNG đo (đi qua `tail`) |
| g2 hạn / gate-r4 hạn | 09:52:00Z / 10:17:12Z 08-09 (chưa qua lúc phóng) |
| codex CLI | `codex-cli 0.153.4` tại `/opt/node22/bin/codex`; auth từ `CODEX_AUTH_JSON` (ảnh chụp 36,1 h — `doctor` SAP_HET_HAN; `chuan-bi` giữ nguyên) |
| scratch lượt 1–5 | **MẤT** (scratchpad container cũ không còn) — reviewer phải dựng lại harness |
| đồng hồ | `date -u` 03:08:38Z vs PR `updated_at` 03:06:24Z (MCP) — không drift đáng kể; HTTP `Date` github.com không lấy được qua proxy |

## Bổ sung lượt 7 (điều phối = phiên 2; đo 08:1x–08:4xZ 09-09-2026)
| phép đo | giá trị |
|---|---|
| lượt 6 run.json (ac23aff9) | xong · ma_thoat 0 · 2889,067 s · stdout 85 B · stderr 4 049 518 B; VERDICT sha256 9090aadd34f34ea6607bae2e55cd87daffd2f1f43a2df10b2190b4db4e8d7db8; HINT 47fbf8cba3265a8f4ad285d03f1fe21136a0c7edff01bc5155959501b05fb84c (7 hunk); stderr có đúng 2 dòng "flagged for possible cybersecurity" — cả hai là reviewer ĐỌC CLAUDE.md/EVIDENCE, không phải bộ lọc bắn |
| reviewer tuân cấm lượt 6 | `git -C cay-kho status --porcelain` = chỉ `?? ops/specs/…`; `log b416830..HEAD` = 0 |
| HINT lượt 6 lên r7 | `patch -p0 --dry-run`: 5/7 hunk áp (offset 4), hunk #4 (`ngoai_pham_vi`) + #7 (Q7–Q13) FAILED vì r7 đã sửa cùng vùng ⇒ vá tay |
| r7 / r8 | r7 `d612ced` sha256 `6a0ea66b…` (kế toán); r8 `bfb0f9a` sha256 `48ea894a81b776742ae7152a8ce039d1b46eee3acd0e63a67a77cce5b21effe0`, 594 dòng |
| ADR-0047 | `e69e4ff` bản đầu; lớp 2 viết lại + lớp 3 thêm giải object dir bằng API Git trong `bfb0f9a`; `adr-song` 47/47; `doctrine-scan` 7 tệp/0 (8/0 với `--path` spec); `doc-claims-check --strict` ok:true |
| CI | `gate (ubuntu)` ĐỎ trên `d612ced`: `tl selftest 1708/1709`, ca `r291_docs_ngoai_goi` (ratchet `docs/**/*.md` 71→72 vì ADR-0047); vá `3a72ea4`: kê khai slot 72/252 + tái sinh `RELEASE_MANIFEST.json` (file_count 180 không đổi); local selftest **1709/1709**, `release-verify --strict` ok. Gate trên `3a72ea4`/`bfb0f9a`: chưa đo được (API check-runs 403 từ phiên này). `cong` đỏ theo thiết kế |
| lease mới trên máy chủ (03:32Z 08-09) | nhánh `ops/cap-lease-mu-ref-va-verdict`: Issue #482 `mu-ref-khong-phu-tag-exec-1-claude-20260908` (write set `CLAUDE.md`, `ops/kiem_mu_ref.py`, `ops/kiem_mu_ref_test.py`) + #483 `verdict-khong-boc-hoi-…`; hạn 09-09 03:32Z; `ai-dang-giu` cho 5 đường PR #475 chạm (spec, README review, ADR, PROTOCOL, tl_selftest, manifest) đều NGƯỜI_GIỮ 0 sau fetch (310/310 tập tên khớp). **Mirror cay-kho KHÔNG có nhánh này** (mirror dựng 03:12Z 08-09) |
| hạn g2 / gate-r4 / r2 | 09:52:00Z / 10:17:12Z / 05:27:42Z 08-09 — **đều đã qua** lúc phóng lượt 7 (09-09) ⇒ tập CÒN_HẠN toàn kho tại clock lượt 7 phải đo lại, không chép 6/3 |
| scratch lượt 6 | chép nguyên từ rv6 sang rv8 (`scratch/luot6/`, 85 MB) để tái dùng; scratch lượt 1–5 vẫn mất |
| codex auth | `CODEX_AUTH_JSON` ảnh chụp 65 h (`doctor` SAP_HET_HAN); lượt 6 chạy trọn với ảnh 36 h; lượt 7 là phép thử |
