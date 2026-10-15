verdict: approve
reviewed_sha: 6616026caff45771c417e61a1cf4a9b87eefcb95
spec_sha256: c5e3c45a99a567c36beb9f6e80067dade9afec124b429292d259f04ecea44410
reviewer_provider: anthropic
reviewer_model: claude-sonnet-5-5 (subagent review-sonnet-max, tự khai)
execution_surface: claude_code_subagent

## BẢNG LỚP

Tổng: **1 lớp — 0 P1 · 0 P2 · 1 P3.** Reviewer là Claude Sonnet 5.5, effort max (tự khai), **KHÔNG phải codex**; cùng họ Claude với executor
(lease ghi `model: claude-opus-5-5`, thân commit ghi Claude Opus 5.5) ⇒ mức `review_deferred`, không thay Codex `cross_approved` hay
`human_audited` mà lớp `sensitive` đòi để land (đặc tả r2, hàng `executor` · `reviewer`). Không mạng, không đăng GitHub, không commit/push.

| slug lớp | hạng | biểu hiện | phương án | phép kiểm / giới hạn |
|---|---|---|---|---|
| `neo-phu-nhan-chu-kho-thieu-chot-danh-tinh-566` | P3 | `ops/land/pr732-wp685-land-evidence.yaml` dòng 72–75 (khoá `neo_phu.ghi_chu`) viết "comment quyết định landed của chủ kho" mà không kèm chốt danh tính; CHÍNH tệp này ở dòng 37 và dòng 63 ghi OWNER + app null KHÔNG tách chủ kho khỏi phiên dùng token chủ kho (#566, tự khai). Phép đo (readback) chỉ cho tài khoản `ducthangho` · OWNER · app null; "của chủ kho" là lời tự nhận trong thân comment (`dang_boi: chu_kho_tu_dang`). Đo: `grep -c 566` trên dòng 64–75 = 0. | Thêm vào ĐÚNG khoá `ghi_chu` một mệnh đề theo mẫu dòng 63, hoặc thu hẹp cụm "của chủ kho" xuống điều đo được (mô tả ở `goi/HINT.patch`, 0 hunk). | Mô phỏng trên bản sao (không phải bản giao): `chk.py` 129/129, `numstat` 14 0, một hunk, `kiem-re` 4 tệp 0 lỗi rc 0. Không đổi kết luận đo nào; `neo_ben`, `landed_hieu_luc_tu`, readback, SHA256SUMS không bị đụng. Lớp này không chặn (chỉ P1/P2 chặn). |

**Điều kiện kèm verdict (không phải lớp, là `KHÔNG ĐO ĐƯỢC` — xem cuối BẢNG ĐO):** (1) N3d (đối chiếu sống `gh api` GET) chưa chạy vì chỉ thị cấm mạng — theo
đặc tả "không tính là đạt"; phải do phiên có mạng chạy trước land. (2) Điều kiện cấp lease — comment chủ kho trên #750 cấp quyền và chấp nhận vượt trần tệp ADR-0044 (4 tệp > 3) —
không kiểm được ngoại tuyến (`lease.yaml` ghi "CHUA CO luc soan"). (3) Land vẫn đòi `human_audited` của chủ kho (lớp `sensitive`).

## BẢNG ĐO

Mọi lệnh chạy trong container, không mạng. `cay-kho` chỉ đọc về NỘI DUNG (`GIT_OPTIONAL_LOCKS=0`; hai chạm vào siêu dữ liệu đã khai ở J(d) và J(e)); mọi bản sao/đột biến nằm trong `do.EhBoRk/` (`mktemp -d -p $R`). Giờ đo: 2026-10-15 10:50Z–11:25Z. Đầu ra thô còn trong `do.EhBoRk/` (`baseline.out`, `mut2.out`, `n5.*.out`, `hintsim.out`, `adg.*.out`, `dry.*`); các bản sao lớn (`kho`, `dry`, `hintsim`, `mut`) đã xoá bằng `shutil.rmtree`.
Công cụ tôi tự viết (không có script của executor trong gói): `do.EhBoRk/chk.py` (129 phép), `mut.py` + `mut_consistent.py` (đột biến), `hintsim.py`, `fmt_check.py`; cây `do.EhBoRk/A0` = `git archive HEAD` bốn tệp + thư mục provenance + hai spec gốc + hồ sơ pr721.

### A. Đầu vào, phạm vi, cỡ

| # | điều đo | lệnh | kết quả thật |
|---|---|---|---|
| A1 | băm SPEC | `sha256sum SPEC.md` | `c5e3c45a99a567c36beb9f6e80067dade9afec124b429292d259f04ecea44410` = băm ghim ⇒ không `blocked`. SPEC cũng = blob `a7ba01e4…` của lease (`git hash-object SPEC.md`; `cat-file blob a7ba01e4…` ⇒ cùng sha256) |
| A2 | `reviewed_sha` | `git -C cay-kho rev-parse HEAD HEAD^` · `branch --show-current` · `merge-base HEAD master` | `6616026caff45771c417e61a1cf4a9b87eefcb95` · cha `6f121a3810045af27bf65eb723edf36b29e387f2` · `claude/no-p3-ho-so-g1` · merge-base `6f121a38…` |
| A3 | `diff.patch` = `git diff 6f121a3` | `git diff 6f121a3 > x; cmp diff.patch x` | cmp rc=0, sha256 `003b5ea2d1b94fa063a843216df1e13220a4842c3b9a0717c5f114aa5e527b0f`, 18.503 byte |
| A4 | cây sạch, 1 commit | `git status --porcelain --untracked-files=all` · `git rev-list --count 6f121a3..HEAD` | 0 dòng · 1 (`6616026c no-p3-ho-so(#750): dinh chinh S2/M8 r14 + O1..O7 r28, neo phu landed wp685 kem readback`). Thân commit: 0 chuỗi bỏ-qua-CI (grep nhiều biến thể) |
| A5 | write set đúng 4 đường | `git diff --name-status 6f121a3..HEAD` | `M ops/land/pr732-wp685-land-evidence.yaml` · `M ops/land/pr732-wp685-provenance/SHA256SUMS.txt` · `A ops/land/pr732-wp685-provenance/readback-comment-6103888794.json` · `A ops/specs/dinh-chinh-p3-wp685-wp698.md` = `write_set` lease/đặc tả |
| A6 | cỡ, chỉ-thêm | `git diff --numstat 6f121a3..HEAD` | `12 0` yaml · `1 0` SHA256SUMS · `1 0` readback · `134 0` md ⇒ 4 tệp · 148 thêm · **0 xoá**. Lease `nang_tran` (≤10 tệp, ≤500 dòng) ĐẠT; đặc tả `kich_thuoc` (ước ≤200) ĐẠT; trần gốc ADR-0044 (≤3 tệp) bị vượt 4 > 3 — đặc tả r2 đã khai lý do và đặt làm điều kiện cấp lease (xem `KHÔNG ĐO ĐƯỢC` 3) |
| A7 | N2 + không chạm pr721 | `git diff --quiet 6f121a3..HEAD -- <r14> <r28>`; `rev-parse 6f121a3:<p>` so `HEAD:<p>`; name-status ở A5 | rc=0 · r14 blob `b427f19d2949c73e2b8088e13999915e8114f186` ở cả hai · r28 blob `fa07ca1bc3707bc273bf25349ffa6f3ca6ad6160` ở cả hai · `ops/land/pr721-wp698-land-evidence.yaml` không có trong diff |
| A8 | không lấy gì từ `ducthangho-patch-1` | `merge-base --is-ancestor 2f30166 HEAD`; `git diff 6f121a3..HEAD` rồi đếm chuỗi `landed_quyet_dinh`; `git grep -F landed_quyet_dinh HEAD` | rc=1 (không phải tổ tiên) · 0 · 0 dòng toàn cây |
| A9 | nguồn O1–O7 | `wc -c`, `wc -l`, `grep -c "^- [*][*]O[0-9]"`, `sed -n 57,63p` rồi `sha256sum` trên `nguon-wp685-r28-luot5-VERDICT.md` | sha256 `d3f1d9db…45fb` · 32.989 byte · 68 dòng · **7** gạch ở dòng 57…63 · băm bảy dòng `7ad7791d184f3734e0716312dea4164bc0ebb882dc0e2e3f5d620a660cc79ab1`. Phụ lục A của SPEC: 7 dòng giữa rào, 6.368 byte, cùng băm; `Phụ lục A == VERDICT[57..63]` từng dòng ⇒ True |
| A10 | không ai khác giữ bốn đường (đọc-chỉ) | `python3 -B ops/lease_publish.py ai-dang-giu <đường>` ×4 trên `cay-kho`; `git grep -l` bốn chuỗi đường dẫn trên 539 ref (`refs/heads`, `refs/remotes`, trừ HEAD) trong `ops/leases` | cả bốn: `NGƯỜI_GIỮ 1: no-p3-ho-so-r2-g1-claude` (`CÒN_HẠN`, ở `refs/remotes/origin/ops/no-p3-ho-so-r2-g1-lease`) — chính lease của packet này, rc=11 (mã "có người giữ"); không người giữ nào khác. `git grep`: đúng 1 blob lease nhắc tới bốn đường; sha256 blob = `lease.yaml` trong gói = `1ac0dbfd3f4b30be2398e2b39ab40cd3ba1bc0f48c61da0eb1951c13ba819df0`. Commit lease `9cfe62e2…` lúc 10:23:58Z; `leased_at_utc` 10:30:00Z; commit thi hành 10:42:50Z |
| A11 | bí mật / tên tệp nhạy cảm trong phần thêm | `grep -c -E` mẫu `ghp_`, `github_pat_`, `GOCSPX-`, `AKIA…`, khối khoá riêng, `Bearer …`, `xox…`, `sk-…`, JWT trên `diff.patch`; tên tệp `*.enc` `tl_secrets*` `*cookie*` `*token*` `credentials*` trong write set; chuỗi `token` ở dòng `+` | 0 · 0 · 0 |

### B. N1 — tệp đính chính (mục tiêu 1–3). `chk.py` trên HEAD: **129 phép, RED=0** (N1 ≈ 89 phép)

| # | điều đo | kết quả |
|---|---|---|
| B1 | sáu giá trị mở đầu tính LẠI từ git (không chép từ đặc tả) | r14: sha256 `ed027f41…1a21` · blob `b427f19d…` · commit nguồn duy nhất `d17ec09088acf674a05638345f7b3ec28ff03c6d`; r28: sha256 `8007edf4…e156` · blob `fa07ca1b…` · commit duy nhất `4a35f633e1b3f05be12eecf74ab9a8a17ef82c69` (`git log --format=%H 6f121a3 -- <p>` mỗi tệp 1 commit). Mỗi giá trị nằm đúng trên dòng nêu đường dẫn của nó ⇒ 6/6 khớp |
| B2 | đúng ba phần | tiêu đề `##`: `S2-r14`, `M8-r14`, `O1..O7-r28` (và chỉ ba) |
| B3 | S2 | một dòng `tệp:` đúng mẫu, đường dẫn r14, sha256 đầy đủ của blob, `dòng 3261–3262`; MỘT khối `text` bằng TUYỆT ĐỐI `r14[3261..3262]` (2 dòng; 12 hex đầu của băm hai dòng nối LF: `ee36e3ddb812` ở cả khối lẫn blob); khối chứa chữ cũ "của r11"; MỘT dòng `chữ đúng:` (dòng 26) chứa `neo `spec_hash` **của r14**`, không chứa "của r11" |
| B4 | M8 | tương tự, `dòng 2729–2731` (3 dòng; 12 hex đầu của băm ba dòng nối LF: `691ecfd4750e` ở cả khối lẫn blob); MỘT dòng `chữ đúng:` (dòng 44) chứa `cùng đường, cùng loại, độ dài không nhỏ hơn (A10 (v), cách tính r14)`, không chứa "với độ dài mọi danh sách" |
| B5 | số đếm trên blob `6f121a3` (tự đo lại, không chép) | r14 = 5.374 dòng (`wc -l`); `grep -n -F 'neo `spec_hash` **của r11**'` ⇒ chỉ dòng 3262; `độ dài mọi danh sách` ⇒ chỉ dòng 2731; `cùng đường, cùng loại` ⇒ 0. Mở rộng phép tìm (ngoài cụm đã ghi): `grep -n -E` với hai mẫu hợp lại ("neo …≤20 ký tự… spec_hash" và "spec_hash …≤30 ký tự… của r1x") ra 6 dòng (34, 68, 3262, 3694, 3695, 3791), đọc từng dòng: chỉ 3262 là chữ cũ (dòng 34 điều kiện (4) của `depends_on` đã ghi "`spec_hash` của **tệp này (r14)**"; 3694–3695 là bảng quyết định lịch sử "Với r2"; 3791 ghi "nay là r14"); "từ điển lồng" chỉ dòng 2731 và 3107 (3107 là định nghĩa A10 (v) đầy đủ, không cũ) ⇒ câu "không chỗ nào khác cần đính chính cùng lượt" đúng, nhưng phép đếm ghi trong tệp hẹp hơn câu ấy (xem QUAN SÁT 5) |
| B6 | bằng chứng S2 | `readback-comment-6091633467.json` (id 6091633467, ducthangho, OWNER): `body` chứa đúng "Tôi đọc S2 theo depends_on (4): neo spec_hash của r14." và "(sót từ r11)" ⇒ câu "Chữ r11 là sót từ r11" có căn cứ |
| B7 | bằng chứng M8 | `ops/reviews/wp698-spec-review-14-claude-verdict.md` sha256 `892eeb8a200cec3083b565ffdfe5e26e078ab4ccdafb861c7324b712028e76c7` (157 dòng); dòng 135 chứa gợi ý "(… cùng đường, cùng loại, độ dài không nhỏ hơn (A10 (v), cách tính r14))", "A10 (v) là tiêu chí nghiệm thu duy nhất" và "không cây nào đo được bị đổi kết luận vì dòng này" ⇒ hai câu trích trong tệp đính chính đúng nguyên văn |
| B8 | O1…O7 | đúng bảy tiêu đề `### O1`…`### O7` theo thứ tự; mỗi khối MỘT rào `text` MỘT dòng, bằng TUYỆT ĐỐI dòng k của Phụ lục A (7/7); `dòng r28:` tập số = Phụ lục B (O1 172·188; O2 188; O3 596·630·3708; O4 162–163; O5 209·232·236·254·275·307; O6 172; O7 không số); `quyết định:` bắt đầu bằng nhãn Phụ lục B (O1, O2 `ghi nhận kèm chữ đề nghị r29`; O3–O7 `chỉ ghi nhận`) |
| B9 | 14 cặp (O, dòng) của Phụ lục B đo lại trên blob r28 (3.940 dòng) | cụm CÓ ở dòng nêu và KHÔNG có ở dòng lệch +1 và −1: 14/14 (O3 là dạng rút gọn `6f07a7cf…25e8`; O4 nối dòng 162–163 sau khi bỏ khoảng trắng hai đầu) |
| B10 | con trỏ O7 (lease `p3_con_mo` 5) | `git show a9ef33c:ops/specs/no-p3-lease-spec-hash-r2.md`: sha256 `8f700b06b28e4c02c615b591b02a75a2fd901239746eb2a3fb8389dd9f549ec4` (khớp tệp đính chính); dòng **10** = hàng `nguon_cap_viec` (dòng 8 của r2 là `thay_the_cho`; dòng 8 của r1 `17df1dcc…` mới là `nguon_cap_viec`); `git cat-file -t master:ops/specs/no-p3-lease-spec-hash-r2.md` ⇒ không có ở master, có ở `refs/remotes/origin/claude/spec-no-p3` = `a9ef33c…` ⇒ câu "tìm ở master trước, chưa thấy thì nhánh `claude/spec-no-p3`" đúng ở cả hai trạng thái |
| B11 | ký tự lạ? | quét mọi code point của tệp đính chính (toàn tệp) và khối `neo_phu` (dòng 64–75): 0 ký tự Cf/Zs/Zl/Zp/Co/Cc/ghép dấu; không tab, không CR, không dấu cách cuối; NFC = chính nó. Khoá trùng: 0 trong toàn bộ YAML hồ sơ pr732, 0 trong JSON readback |
| B12 | "Cả hai đã đóng băng và có lease neo băm" | `git grep -l -F <sha256> 6f121a3 -- ops/leases` ⇒ r14: `wp698-r14-g2-claude.yaml`; r28: `wp685-r28-g5-claude-20261009.yaml` ⇒ đúng |
| B13 | "nguồn không có trong kho" | `git cat-file --batch-all-objects --batch-check` (45.835 đối tượng): 0 blob cỡ 32.989; tiêu đề O1 chỉ có trong `no-p3-ho-so-r2.md` (hai ref spec) và tệp đính chính này ⇒ đúng |

### C. N3, N3b, N3c — hồ sơ pr732 (mục tiêu 4)

| # | điều đo | kết quả |
|---|---|---|
| C1 | `yaml.safe_load`; `trang_thai_packet.landed` | thành công; `True` |
| C2 | `neo_ben` | `https://github.com/ducthangho/tra-luat/pull/739#issuecomment-6103749546` (URL, không phải số) |
| C3 | chỉ-thêm (N3b) | `git diff --numstat` `12 0`; `git diff -U0` rồi đếm dòng mở đầu bằng `@@` = 1; hunk `@@ -63,0 +64,12 @@`, dòng thêm đầu `+    neo_phu:`; khoá `landed_quyet_dinh` vắng (trong `trang_thai_packet` và khắp tệp); mọi giá trị cũ của `trang_thai_packet` (kể cả `landed_hieu_luc_tu`) và `authorized_head_sha` `3089b544…` bằng base; phần còn lại của tài liệu YAML = base ngoài `neo_phu` |
| C4 | vị trí | `list(quyet_dinh_chu_kho)` = `trang_thai, lenh_nguyen_van, luc, neo_ben, neo_ben_do_duoc, neo_phu` (ngay sau `neo_ben_do_duoc`, cùng cấp `neo_ben`); khoá kế của `quyet_dinh_chu_kho` trong `trang_thai_packet` là `landed_ly_do` |
| C5 | tám khoá, đúng thứ tự | `url, luc, nguoi_dang, author_association, performed_via_github_app, so_byte, sha256, ghi_chu` (đúng 8, không thừa) |
| C6 | N3c: neo_phu so readback VÀ so giá trị ghim | readback `id`=6103888794; `url`=`html_url`=`…/issues/685#issuecomment-6103888794`; `nguoi_dang`=`user.login`=`ducthangho`; `author_association`=`OWNER` (cả hai); `performed_via_github_app` `null` (cả hai); `created_at`=`updated_at`=`2026-10-11T00:45:59Z` và `luc`=`2026-10-11T00:45:59Z (created_at = updated_at)` (đúng mẫu tiền lệ `quyet_dinh_chu_kho.luc`); `so_byte`=`len(body.encode('utf-8'))`=631 (kiểu int); `sha256`=sha256(body)=`cc38f7996531c5239f2e4e8ad760fcc20a2720a132f90de81251e65342e8f09b` (đủ 64, bằng giá trị ghim); `ghi_chu` chứa `pull/739#issuecomment-6103749546`; body chứa `landed` và `685`, 0 thực thể HTML (`&#39;` `&#34;` `&gt;` `&lt;` `&amp;`) |
| C7 | không consumer nào đọc khoá hồ sơ pr732 | `git grep -n -E` với mẫu gồm bốn khoá `neo_ben`, `landed_hieu_luc_tu`, `trang_thai_packet`, `neo_phu`, trên `*.py` `*.sh` `*.yml` tại HEAD: chỉ `ops/land/pr621-skill-bai-hoc-provenance/kiem_ho_so.py` (hồ sơ KHÁC) và vài script review cũ đọc pr666; không `*.py/*.sh/*.yml` nào liệt kê `ops/specs/*.md` hay `*-land-evidence.yaml` ngoài allowlist tiền tố của `ops/ci_duong_nhanh.py` dòng 115 ⇒ khối mới không phá consumer đo được |

### D. Readback 6103888794 — định dạng (mục tiêu 5)

| # | điều đo | kết quả |
|---|---|---|
| D1 | kích thước và băm tệp | `wc -c` 2.273 byte (= "phản hồi 2.273 byte" ghi trong đặc tả và thân commit); sha256 tệp `2279f336246128fd3a0570e0089319f5fb6e1f884878a4fa3294d7b6c98d786d` = dòng mới của SHA256SUMS; blob git `d4d5eae13e5da1e7d7bf6f1d802f5cbb152c9977` |
| D2 | cùng khuôn với 9 readback-comment khác của pr732 (`fmt_check.py`) | cả 10 tệp: JSON compact một dòng, `json.dumps(ensure_ascii=False, separators=(',',':'))` tái tạo ĐÚNG từng byte; 0 chuỗi uXXXX; không BOM, không CR, **không LF cuối**; thứ tự khoá cấp 1 giống hệt 9 tệp kia (`url, html_url, issue_url, id, node_id, user, created_at, updated_at, author_association, body, reactions, performed_via_github_app, minimized, pin`); so với `readback-comment-6103749546.json`: cùng tập khoá lá, `user` bằng nhau, khác đúng các trường theo id/thời gian/issue |
| D3 | thân | 631 byte UTF-8, 2 dấu xuống dòng; mở bằng "QUYẾT ĐỊNH LANDED — wp685 r28 g5", dòng 2 `dang_boi: chu_kho_tu_dang`, chứa "wp685 / #685 LANDED tại 77fb0288dca8483f28209cae42c38d4cb97397d9"; đăng sau merge #732 (`merged_at 2026-10-10T16:41:22Z`) và chưa sửa (`updated_at = created_at`) |
| D4 | giới hạn | byte lưu trên GitHub so với byte đã đến: không có client thứ hai (CLAUDE.md, bài học 22-08-2026) ⇒ `KHÔNG ĐO ĐƯỢC`; ở đây chỉ chứng minh được: tệp nhất quán nội tại, khớp giá trị ghim của lần đọc 08:55Z (băm thân), cùng độ dài với phản hồi đó |

### E. N4, N4b — provenance

```
cd ops/land/pr732-wp685-provenance (git archive HEAD)    sha256sum -c SHA256SUMS.txt   -> rc=0, 45 dòng ": OK", 0 FAILED   (wc -l SHA256SUMS.txt = 45 = 44 cũ + 1)
LC_ALL=C sort -c -k2 SHA256SUMS.txt                       -> rc=0      (awk '{print $2}' | LC_ALL=C sort -c -> rc=0)
git diff --name-status 6f121a3..HEAD -- ops/land/pr732-wp685-provenance/
                                                          -> M SHA256SUMS.txt ; A readback-comment-6103888794.json   (chỉ hai dòng)
git diff --numstat ... SHA256SUMS.txt                     -> 1  0
```
Dòng mới nằm GIỮA `readback-comment-6103749546.json` và `readback-comments-732.json`; 44 dòng cũ giữ nguyên là dãy con có thứ tự; băm dòng mới = băm thật của tệp readback. Mọi tệp provenance cũ bằng base (so từng byte với `git show 6f121a3:<p>`).

### F. N5 — cổng kho (dựng merge tạm trong bản sao hard-link `do.EhBoRk/kho`, đã xoá sau khi đo)

```
GOC = git merge-base 6616026c… 6f121a38…            = 6f121a3810045af27bf65eb723edf36b29e387f2
DAU = 6616026caff45771c417e61a1cf4a9b87eefcb95
TREE= git merge-tree --write-tree GOC DAU           = 1a46f73197d84e1e797bb1bc7e0598038672c187   (rc 0; = tree của DAU)
MRG = git commit-tree TREE -p GOC -p DAU            = dea43af060541fbdd705804c52adf9e49b30b466 ; git checkout MRG
CI_DUONG_NHANH_SU_KIEN=pull_request CI_DUONG_NHANH_GOC=$GOC CI_DUONG_NHANH_DAU=$DAU CI_DUONG_NHANH_MERGE=$MRG python3 -B ops/ci_duong_nhanh.py kiem-re
  -> DUONG_NHANH: toan bo 4 tep doi khop allowlist ops/{land,leases,reviews,specs}/** - dung duong nhanh
     DUONG_NHANH: kiem-re DAT (4 tep doi, 0 loi)          rc=0    (~10 s)
python3 -B .claude/dev/packet_loop.py doctrine-scan --root .  -> "doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine"  rc=0
python3 -B ops/ci_duong_nhanh.py kiem-re   (TRẦN)           -> rc=1  "KHONG DO DUOC diff … fail-close ve DAY_DU"  (đúng như đặc tả: không phải phép đo)
```
Bỏ từng biến một trong bốn (`env -i`): SU_KIEN, GOC, DAU, MERGE ⇒ **4/4 rc=1** (fail-close). Ba đột biến N5 (commit lên DAU rồi dựng merge mới): (a) thêm tệp nhị phân `provenance/mutant.bin` ⇒ rc=1 `tep ho so nhi phan … 'ops/land/pr732-wp685-provenance/mutant.bin'` (5 tệp đổi, 1 lỗi); (b) YAML pr732 hỏng cú pháp ⇒ rc=1 `YAML khong parse duoc … ScannerError`; (c) tệp ngoài allowlist `README_mutant.md` ⇒ rc=1 `DAY_DU vi diff co 1 tep ngoai allowlist`. Lease `p3_con_mo` 4 (GOC = merge-base thực) ĐẠT.
Giới hạn: đây là mô phỏng cục bộ; CI GitHub thật (PR chưa mở), Windows: `KHÔNG ĐO ĐƯỢC`.

### G. Đột biến chứng minh răng của tiêu chí (bản sao hard-link, không đụng `cay-kho`)

77 ca: **72 đột biến phải ĐỎ + 4 lệch dòng nhất quán phải ĐỎ + 1 ca đối chứng phải XANH — 77/77 ra đúng dự kiến.** Mỗi đột biến phải làm đỏ ÍT NHẤT MỘT phép CÓ TÊN nêu trước; chết vì lỗi vô can KHÔNG tính (xem sai sót rig b).

| nhóm | đột biến (đều ĐỎ ở phép nêu) |
|---|---|
| N1 lệch dòng | `tệp:` S2 và M8 lệch +1 và −1 (chỉ tiêu đề) ⇒ `tep-so-dong` + `khoi==blob[tep.a..tep.b]`; **lệch NHẤT QUÁN** (tiêu đề và khối trích cùng dịch ±1) ⇒ chỉ phép đã ghim a,b theo mục tiêu 1–2 đỏ (xem QUAN SÁT 2) |
| N1 khối trích | đổi 1 ký tự trong khối S2, M8 ⇒ `khoi==blob`; khối trích là CHỮ ĐÚNG thay vì chữ gốc ⇒ 3 phép đỏ |
| N1 chữ đúng | `r14→r13` (S2; M8 "cách tính r13"); chữ đúng = chữ cũ (S2 r11; M8 r13) ⇒ `chu-dung-chua-chuoi` đỏ; **bỏ dòng `chữ đúng:` mà chuỗi đúng nằm ở dòng khác** ⇒ chỉ phép THEO DÒNG đỏ (grep toàn tệp sẽ lọt — lease `p3_con_mo` 1) |
| N1 sáu giá trị | lệch 1 ký tự từng giá trị trong sáu (sha256/blob/commit × r14/r28) ⇒ 6/6 đỏ; sha256 trong dòng `tệp:` lệch 1 ký tự ⇒ đỏ |
| N1 phần O | bỏ khối O7; đổi 1 ký tự trong khối O3 và O6; đổi chỗ nội dung O3/O4; đổi chỗ hai tiêu đề O3/O4; `dòng r28` lệch ±1 (O2 188→189 và 187; O3 596→595 và 3708→3709; O5 307→308; O4 162–163→163–164); nhãn O3 := nhãn O1; nhãn O1 := "chỉ ghi nhận"; bỏ dòng `quyết định:` của O2; thêm phần thứ tư; đổi tên phần O; "5.374→5.375"; CRLF lẫn vào |
| N2, X | thêm 1 byte vào r14, r28, hồ sơ pr721 ⇒ `X.*` đỏ |
| N3 | sha256 `neo_phu` lệch 1 ký tự; đổi `neo_ben` (…546→…547); sửa 1 chữ `landed_hieu_luc_tu`; sửa 1 ký tự `authorized_head_sha`; **chép dòng `landed_quyet_dinh` của 2f30166** ⇒ hai hunk + khoá có mặt; `landed: false`; xoá một dòng chú thích đầu tệp; `neo_phu` thụt lề sai (con của `trang_thai_packet`) |
| N3c khoá | bỏ từng khoá trong tám (url, luc, nguoi_dang, author_association, performed_via_github_app, so_byte, sha256, ghi_chu) ⇒ 8/8 đỏ; `so_byte` 631→630; `luc` đổi giờ; `ghi_chu` mất `pull/739#issuecomment-6103749546`; app `null→claude-app`; `nguoi_dang→mallory`; `author_association→MEMBER`; `url→URL neo_ben` |
| N3c readback | (i) BỊA người đăng + thân vô nghĩa, `sha256`/`so_byte`/SHA256SUMS cập nhật khớp ⇒ đỏ (`nguoi_dang`, `so_byte`, sha256 ghim); (i-b) ĐÚNG người đăng, thân vô nghĩa, khớp nội bộ ⇒ đỏ (`so_byte`, sha256 ghim); (ii) giữ đúng mọi trường, đổi 1 ký tự thân (cùng độ dài: "g5→g6"), khớp nội bộ ⇒ **chỉ** `N3c.8` (sha256 ghim) đỏ; `updated_at` khác ⇒ đỏ |
| ĐỐI CHỨNG | (ii) + TẮT phép so với sha256 ghim (`NO_PIN=1`) ⇒ **XANH, rc=0** — xác nhận lời khai của đặc tả: chính giá trị ghim là thứ giết (ii) |
| N4, N4b | sửa 1 byte readback không cập nhật SHA256SUMS ⇒ `sha256sum -c` đỏ; xoá 1 dòng cũ khỏi SHA256SUMS; sửa 1 tệp CŨ cùng dòng băm của nó (`sha256sum -c` vẫn đạt, name-status lộ ra); dòng mới ở CUỐI; thêm tệp thừa vào provenance + dòng băm ⇒ đều đỏ |

**Lăng kính "đặc tả có tự giết được không":** trong 73 ca của `mut.py`, **4** chỉ bị phép THÊM của tôi giết (đặc tả tự nó có thể để lọt): bỏ dòng `chữ đúng:` (xem QUAN SÁT 3), "5.374→5.375", CRLF, và bỏ khoá `performed_via_github_app` (QUAN SÁT 1). 68/72 đột biến (không tính ca đối chứng) bị phép mà đặc tả tự nêu giết; việc phân loại phép nào là "của đặc tả" là của tôi (danh sách mẫu ở cuối `mut.py`).

### H. Mô phỏng hướng sửa của lớp P3 (trên bản sao, KHÔNG phải bản giao)

Thêm hai dòng vào `ghi_chu` trong bản sao `hintsim` (`+183 byte`): `chk.py` ⇒ **129/129**, N3b `+14 -0`, một hunk, dòng thêm đầu `    neo_phu:`; trong bản sao git: commit lên DAU, dựng merge mới (`2e621bf7…`/`ef76d1ae…`) ⇒ `kiem-re DAT (4 tep doi, 0 loi)` rc=0, `numstat` yaml `14 0`. Hướng sửa không phá tiêu chí nào đo được.

### I. `KHÔNG ĐO ĐƯỢC`

1. **N3d** — `gh api` GET lại `repos/ducthangho/tra-luat/issues/comments/6103888794` và so `id`, `user.login`, `author_association`, `performed_via_github_app`, `created_at`, `updated_at`, `body` với tệp readback: chỉ thị cấm mạng ⇒ không chạy, không tính là đạt. Phiên có mạng phải chạy trước land.
2. Trạng thái hiện tại của comment trên GitHub (có bị sửa sau 08:55Z và sau lần đọc của executor không), và byte lưu trên GitHub so với byte trong tệp — một client duy nhất.
3. Comment chủ kho trên #750 cấp quyền lease + chấp nhận ngoại lệ trần tệp ADR-0044 (4 > 3): lease ghi "CHUA CO luc soan"; không mạng. Thời điểm commit `6616026` (10:42:50Z) sau `leased_at_utc` (10:30:00Z) nhưng điều đó không chứng minh comment đã có.
4. `origin/master` phía máy chủ còn là `6f121a3` không: chỉ đọc được bản sao (`master` = `origin/master` = `6f121a38…` trong `cay-kho`).
5. CI thật trên GitHub (PR chưa mở); lượt Windows; tác dụng của `ci.yml` ngoài mô phỏng cục bộ.
6. Các giờ "~10:38Z" (`ghi_chu`) và "~10:40Z" (tệp đính chính) do executor tự khai; phép đếm chạy lại cho cùng kết quả (B5) nhưng giờ không kiểm được. Executor đã chạy phép đo nào: không có script/log của executor trong gói.
7. Có thật hay không việc readback là "đầu ra nguyên byte của `gh api`": chỉ có chứng cứ gián tiếp (D1–D3).

### J. Sai sót rig của chính lượt này (đã sửa/khai, để khỏi đọc nhầm)

(a) Lần chạy đầu `chk.py` cho 127/129 vì HAI lỗi hiệu chỉnh của TÔI: cụm O3 trong Phụ lục B là dạng rút gọn `6f07a7cf…25e8` (tôi dùng biểu thức chính quy cho băm đầy đủ), và phép so toàn khối `trang_thai_packet` quên rằng `quyet_dinh_chu_kho` đổi đúng bằng `neo_phu`. Đã sửa, đo lại baseline 129/129 TRƯỚC khi chạy đột biến. Chỗ lỏng thứ ba (không đỏ): với O7, `chk.py` lúc đầu trích số từ chữ `r28` trong lời chú giải nên so [28] với [28]; đã lọc bỏ phần trong ngoặc trước khi trích số. (b) Ở lượt đột biến đầu, ca "dòng mới ở cuối SHA256SUMS" chết bằng `IndexError` của chính `chk.py` (rc=1, 0 phép đỏ) — tín hiệu vô can, KHÔNG tính là giết; đã thêm chốt biên, chạy lại cả bộ 73 ca, ca ấy giờ đỏ ở `N4.3`, `N4.3b` và `N4b.3`. (c) Một lệnh `git grep` của tôi có `2>/dev/null` (chuyển stderr, không `mv`, không ghi đè): vi phạm chữ của "không bao giờ ghi vào /dev/null"; `ls -l /dev/null` sau đó vẫn `crw-rw-rw- 1, 3`; rà lại các lệnh của lượt, chỉ có đúng lệnh ấy. (d) Bản sao dựng bằng `git clone --local` dùng chung inode (hard-link) với `cay-kho`. Sau khi xong, `find cay-kho -newer PROMPT.md -type f` chỉ ra đúng MỘT tệp: đối tượng lỏng `.git/objects/1a/46f73197…` (cây gốc của commit `6616026`, cũng là cây `git merge-tree --write-tree GOC DAU` trả về) có mtime 11:01:56, trùng lúc chạy `kiem-re` lần hai — suy luận (không đo trực tiếp, bản sao đã xoá): `merge-tree --write-tree` ghi lại đúng cây đã có nên git cập nhật mtime của tệp dùng chung. Nội dung không đổi (tên = băm nội dung; `git rev-list --objects HEAD --not 6f121a3` vẫn ra 10 đối tượng, `git cat-file -t` đọc được), `git status --porcelain --untracked-files=all` = 0 dòng, `HEAD` không đổi. Đây vẫn là một chạm vào `cay-kho` ngoài chữ của "không sửa tại chỗ" (chỉ siêu dữ liệu), nên khai. (e) Chạy `ai-dang-giu` ×4 (A10) TẠI CHỖ trên `cay-kho` làm tươi stat cache của `.git/index` (mtime 11:21:17Z; `ops/lease_publish.py` gọi git với env rỗng `{"PATH", "LC_ALL"}` nên không tôn trọng `GIT_OPTIONAL_LOCKS=0` của tôi). Nội dung chỉ mục vẫn = cây HEAD (`git diff-index --cached --quiet HEAD` rc=0; băm danh sách `ls-files -s` = băm danh sách `ls-tree -r HEAD` = `a08f4333…`), `git status --porcelain --untracked-files=all` = 0 dòng, `HEAD` không đổi. Lẽ ra phải chạy trong bản sao; tôi chạy tại chỗ vì coi lệnh là đọc-chỉ — đúng về nội dung, sai về siêu dữ liệu. Lượt review lượt 5 của wp685 ghi cùng hiện tượng ở M1. (f) Tôi tạo tệp đánh dấu `$R/.W_path` ở gốc `$R` (ngoài `goi/` và thư mục `mktemp`) lúc đầu; đã `mv` vào `do.EhBoRk/W_path.txt` trước khi kết thúc. (g) `$R` đạt đỉnh 381 MB (dưới 400 MB) khi checkout bản sao; sau khi xoá bản sao bằng `shutil.rmtree` còn 227 MB; không dùng `rm -rf`/`pkill`.

## CHI TIẾT TỪNG LỚP

### Lớp 1 · P3 · `neo-phu-nhan-chu-kho-thieu-chot-danh-tinh-566`

**Biểu hiện (đo trên `6616026`).** Khối `trang_thai_packet.quyet_dinh_chu_kho.neo_phu` (dòng 64–75) có `ghi_chu` (dòng 72–75):

```
ghi_chu: >-
  Đây là neo PHỤ (packet no-p3-ho-so #750): comment quyết định landed của chủ kho trên #685, mọi giá trị đo
  từ readback-comment-6103888794.json (gh api GET 2026-10-15 ~10:38Z). Neo chuẩn vẫn là neo_ben = …
```

Cụm "của chủ kho" gán tác giả comment cho người, không kèm giới hạn danh tính. Cùng tệp nói ngược lại về chính loại bằng chứng này: dòng 37 "merged_by ducthangho — KHONG tach duoc phien voi chu kho (#338/#566, tu khai)" và dòng 63 "chu kho dang (OWNER + app null khong tach chu kho khoi token chu kho, #566 — tu khai)" (khối `neo_ben_do_duoc`, liền ngay phía trên). `grep -n 566` trên toàn tệp ⇒ dòng 37, 48 (băm tree, vô can), 63; trên dòng 64–75 ⇒ 0. Điều đo được ở D1–D3 chỉ là tài khoản `ducthangho` · OWNER · app null; "chủ kho đăng" là lời trong thân comment (`dang_boi: chu_kho_tu_dang`). Đặc tả r2 (mục tiêu 4) không đòi chốt này nên đây không phải lệch đặc tả; là lời khai rộng hơn phép đo trong bản giao, ở đúng chỗ mà chính hồ sơ này (dòng 37, 63) và lease (`authority_caveat`: "author_association=OWNER khong tach chu kho khoi phien agent dung token chu kho (#566)"; `chua_do_duoc`: "Danh tinh nguoi ky comment cap quyen: #566") đã đánh dấu.

**Hậu quả.** Không đổi quyết định `landed`, `neo_ben`, hay `landed_hieu_luc_tu`. Người đọc hồ sơ land sau này thấy hai khối kề nhau, một khối kèm chốt danh tính, một khối không, và có thể đọc `neo_phu` là bằng chứng mạnh hơn `neo_ben` về danh tính người quyết. Hạng P3: không chặn.

**Phương án.** Xem `goi/HINT.patch` (mô tả, 0 hunk, không chép nội dung tệp authority). Sửa chỉ trong khoá `ghi_chu`; SHA256SUMS và readback không đổi vì `ghi_chu` không nằm trong dây băm. Executor phải COMMIT trước khi đo (phép so `6f121a3..HEAD` không thấy cây chưa commit).

**Phép kiểm sau sửa (executor tự chạy):** `numstat` yaml cột xoá vẫn 0; `git diff -U0` vẫn đúng một hunk với dòng thêm đầu `    neo_phu:`; `yaml.safe_load` OK và `ghi_chu` vẫn chứa `pull/739#issuecomment-6103749546`; `kiem-re` với ĐỦ bốn biến CI trên merge tạm ⇒ `4 tep doi, 0 loi` rc 0; `grep -c 566` trên khối `neo_phu` ≥ 1. Mô phỏng ở mục H đạt cả năm.

**Giới hạn.** Một lượt đo, một người đo, cùng họ Claude với executor.

## QUAN SÁT KHÔNG XẾP LỚP

Tiêu chí: chỉ xếp lớp khi lời khai rộng hơn phép đo VÀ ảnh hưởng quyết định hay việc của executor. Các mục dưới đây không đổi kết luận đo nào của bản thi hành.

1. **N3c không phân biệt khoá VẮNG với `null` (đặc tả, không phải bản giao).** Đột biến "bỏ khoá `performed_via_github_app`" chỉ bị phép "đúng 8 khoá" của tôi giết. Một script N3c viết `neo_phu.get('performed_via_github_app') is None` thấy khoá vắng và `null` y hệt nhau; viết `neo_phu['…']` thì chết bằng `KeyError` — tín hiệu không đặt tên (kiểu tín dụng giả đã ghi ở CLAUDE.md). Bản giao có khoá tường minh `null` nên không dính. Gợi ý cho lần dùng lại khuôn "neo phụ": kiểm `'performed_via_github_app' in neo_phu` trước khi so giá trị.
2. **N1 đọc `a`, `b` từ chính tệp đính chính (đặc tả).** Phép `khoi == blob[tep.a..tep.b]` tự tham chiếu nên LỆCH NHẤT QUÁN (tiêu đề `tệp:` và khối trích cùng dịch ±1) vẫn XANH ở phép đó; bốn ca nhất quán của tôi chỉ chết nhờ phép ghim `a,b` theo mục tiêu 1–2 (`3261–3262`, `2729–2731`). Bản giao đúng khoảng; khuyến nghị ghim `a,b` trong script N1 của lần sau.
3. **Lease `p3_con_mo` 1 (grep trên đúng dòng) — đã tuân thủ.** Mỗi phần có đúng một dòng `chữ đúng:` (26, 44); chuỗi mới xuất hiện đúng 1 lần/tệp, ở chính dòng đó; chữ cũ `neo `spec_hash` **của r11**` xuất hiện 2 lần (dòng 16 phần mô tả, dòng 23 khối trích) nên một phép "cấm chữ cũ" quét toàn tệp sẽ báo động giả — phép theo dòng là phép đúng.
4. **Hình thức:** câu "nguyên văn" ở `Căn cứ` của S2 ngắt dòng giữa chừng ("neo spec_hash⏎của r14"); thân comment có dấu cách. Tương đương Markdown, nhưng `grep -F` câu trích trên một dòng sẽ trượt. Câu trích ở M8 nằm trọn một dòng.
5. **"không chỗ nào khác cần đính chính cùng lượt" (S2)** rộng hơn phép đếm ghi trong tệp (một cụm). Tôi mở rộng phép tìm (B5) ⇒ vẫn không có chỗ thứ hai; câu đúng, chỉ là cơ sở ghi trong tệp hẹp hơn lời khai.
6. **Không có phép đo bền trong kho** cho N1/N3/N4 (đúng thiết kế: gói không sửa mã). Nếu điều phối muốn giữ, `do.EhBoRk/chk.py` + `mut.py` là khuôn dùng lại; chạy: `KHO=<kho git> SPEC_MD=<SPEC.md> TMPD=<thư mục tạm> python3 -B -I chk.py <cây A>`.

## DRY-RUN HINT.patch

- Tệp `goi/HINT.patch`: 25 dòng, 3.129 byte, **0 hunk** (cố ý: lớp duy nhất là P3 và hướng sửa chỉ mô tả), 0 CR, 0 dấu chéo ngược, 0 chuỗi bỏ-qua-CI, 0 dòng bắt đầu `---`/`+++`/`@@`; dòng 1 mang nhãn "chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit". sha256 `8addfe5344dd624b6f984359cbbc32bff7d54da089425ef76a384e021c7b27ba` (băm của chính VERDICT.md không ghi được trong VERDICT.md; điều phối đo trên tệp đã đến).
- Dry-run trên bản sao `do.EhBoRk/dry` (51 tệp, = `git archive HEAD` các đường liên quan): `patch -p0 --fuzz=0 --dry-run < HINT.patch` ⇒ "patch: **** Only garbage was found in the patch input.", **rc=2** (cách GNU patch báo đầu vào KHÔNG có hunk, không phải hunk áp hỏng); `git apply -p0 --check` ⇒ "error: No valid patches in input (allow with "--allow-empty")", rc=128; `git apply -p0 --check --allow-empty` ⇒ **rc=0**; chạy thật `patch -p0 --fuzz=0` trên bản sao ⇒ cùng thông báo, rc=2. Danh sách tệp và sha256 trước/sau BẰNG nhau (`cmp` rc=0, 51 dòng), 0 tệp `.orig`/`.rej`.
- Hệ quả cho điều phối: không có gì để áp bằng máy. Executor tự viết chữ mệnh đề theo HINT, commit, rồi chạy năm phép kiểm ở "Phép kiểm sau sửa".
