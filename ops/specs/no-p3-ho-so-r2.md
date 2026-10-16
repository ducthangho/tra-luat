# Đặc tả packet `no-p3-ho-so` r2 — nợ P3 (a): đính chính spec đóng băng + neo phụ landed wp685

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-ho-so` |
| `packet_issue` | #750 |
| `revision` | **2** |
| `thay_the_cho` | **r1**: `ops/specs/no-p3-ho-so-r1.md`, sha256 `694f8435201e0cae1aa2c63619c03d6090d57bbece66ecab929e467343ddaa67`, blob `2cd2c92288dc07e54e58bd959fdc4936d4cfcee0`, commit `55bd0d24d299d20ff32a8b2dd42deb200295462e` (2026-10-15T05:55:53Z). Thứ định danh r1 là cặp băm này, không phải tên nhánh chứa nó. Tệp r1 **giữ nguyên** để băm của nó vẫn tra được; r2 là tệp riêng. r1 chưa được neo vào lease nào: 0 trong 618 blob lease khác nhau ở đầu 601 ref của bản sao `cay-kho` nhắc `694f8435`, `no-p3-ho-so` hay issue 750 (đo 15-10-2026 09:00Z). |
| review của r1 | **Lượt 1**, reviewer Claude Sonnet 5.5 (`claude-sonnet-5-5`, subagent, tự khai): `verdict: changes_requested`, `reviewed_sha: 55bd0d24d299d20ff32a8b2dd42deb200295462e`, **0 P1 · 6 P2 · 7 P3 = 13 lớp** (đơn vị: lớp trong BẢNG LỚP của VERDICT). `VERDICT.md` sha256 `32cb9187370ca03bdf1d01b1e27a8e31db6e6c6a3ca2a160987ec9bd758a6be1` (178 dòng, 44.325 byte); `HINT.patch` sha256 `14be78ac84b3c05643b87515fcba35d63505fdeaf9cc98e1a91fb2631c29cf9c` (134 dòng, 21.073 byte, 17 hunk). Cả hai nằm ở scratchpad phiên điều phối, KHÔNG có trong kho; băm đo 15-10-2026 ~08:55Z trên tệp đã đến. |
| `nguon_cap_viec` | Sổ nợ P3 của phiên điều phối `session_01CSM7GNazhN6uGJb4v1TqBT`, mục 1, 2, 3, 11; ngưỡng chủ kho, nguyên văn "Lớp P3 trở xuống KHÔNG chặn; chúng được ghi vào sổ nợ và xử lý ở một packet riêng" (#698 comment `6094652521`, đặt cho wp698 g2; #686 comment `6094654297`, đặt cho wp685 g5 — chỉ đúng cho hai lease ấy; đo lại 15-10-2026 ~08:52Z trên `ops/land/pr721-wp698-provenance/readback-comment-6094652521.json` và khoá `mission_comments[4]` của `ops/reviews/wp685-r28-g5-exec-review-1-codex/evidence/reviewer/preflight-remote.json`); `no_con_mo` của `ops/land/pr721-wp698-land-evidence.yaml` (mục `S2-SPEC-HASH-CUA-R11` dòng 355, `M8-GIU-RANG-CACH-NOI-R13` dòng 357). Cách tách ba packet do chủ kho chốt trong phiên soạn spec ngày 15-10-2026 (Q1–Q10, "đồng ý hết" hai vòng). **Hai quyết định chủ kho 15-10-2026 cho r2** (truyền qua phiên điều phối; chưa có bản ghi trong kho): (a) nhánh `ducthangho-patch-1` BỊ BỎ — packet này tự làm neo phụ kèm readback (xem "Ngoài phạm vi"); (b) chép NGUYÊN VĂN bảy gạch O1…O7 của VERDICT nguồn vào Phụ lục A của r2 để executor có nguồn trong kho. |
| `review_class` | **`sensitive`** (khai; cũng là `effective_review_class` dự kiến). Ba căn cứ, đo 15-10-2026 08:51–08:58Z trên `cay-kho`: (1) PROTOCOL §8 dòng 724 xếp "review/land authority" vào `sensitive`, và `ops/land/pr732-wp685-land-evidence.yaml` là hồ sơ mang `landed` và `authorized_head_sha` của wp685; (2) `ops/lease_publish.py` `_tinh_lop_tu_write_set` (dòng 357) tra từng đường qua `_BANG_LOP` (dòng 59; 7 mục, cả 7 là lớp `sensitive`), đường không có trong bảng cũng rơi về `sensitive` — gọi thẳng hàm trên bốn đường của write set: từng đường và cả bốn ⇒ `sensitive`; (3) PROTOCOL dòng 622: thiếu/không rõ ⇒ `sensitive`. Giá trị `standard` của r1 KHÔNG thuộc enum `routine`, `systemic`, `sensitive` (PROTOCOL dòng 156): `.claude/dev/chon_reviewer.py` `_lop_review` (dòng 62–66) ném `KhongDoDuoc: review_class ngoài allow-list: 'standard'` (đo). Khai thấp hơn (`routine`, như HINT gợi ý) không đổi lớp hiệu lực — dispatcher lấy mức cao hơn giữa khai báo và classifier (PROTOCOL dòng 719–720) — mà chỉ thêm một chỗ lệch giữa đặc tả và lease. |
| `executor` · `reviewer` | Claude (executor). Reviewer: subagent Claude Sonnet (cùng họ) ⇒ mức `review_deferred`. Với lớp `sensitive`, PROTOCOL §8 (dòng 724–726) đòi Codex `cross_approved` hoặc `human_audited`; `review_deferred` chỉ cho vào draft PR (§8 mức 4, dòng 612: "cần xác nhận riêng khi apply"). Vì vậy land của packet đòi `human_audited` của chủ kho — cùng điều kiện mà cả hai comment ngưỡng ở `nguon_cap_viec` giữ ("Land vẫn đòi … human_audited"). Ngưỡng review: 0 P1 / 0 P2 để đạt, P3 không chặn nhưng mỗi P3 còn mở phải có quyết định ghi lại (bảng ngưỡng PROTOCOL §8, hàng `sensitive`, dòng 621); căn cứ ngưỡng cho packet NÀY là quyết định phiên soạn spec 15-10-2026, chưa có bản ghi trong kho. |
| `base` | `origin/master` `6f121a3810045af27bf65eb723edf36b29e387f2`. Đo 15-10-2026 08:54Z: `git ls-remote origin` (máy chủ) trả `refs/heads/master` = `6f121a3…`; `origin/master` của `cay-kho` (08:48Z) cùng giá trị. Giờ "~06:10Z" của r1 bị bỏ: nó muộn hơn giờ commit 05:55:53Z của chính r1. |
| `write_set` | `ops/specs/dinh-chinh-p3-wp685-wp698.md` (MỚI) · `ops/land/pr732-wp685-land-evidence.yaml` · `ops/land/pr732-wp685-provenance/readback-comment-6103888794.json` (MỚI) · `ops/land/pr732-wp685-provenance/SHA256SUMS.txt` |
| `kich_thuoc` | **4 tệp. Ước ≤ 200 dòng thêm, 0 dòng xoá** (đơn vị: dòng `git diff --numstat` so `6f121a3`; xoá = 0 khoá bằng N3b và N4b). Căn cứ ước, đo 15-10-2026 ~08:57Z: bản khung tệp đính chính dựng đúng định dạng N1 (khối trích thật của r14 và của Phụ lục A, phần chữ để trống) = 113 dòng; khối `neo_phu` = 9 dòng (bản mô phỏng N3c); readback = 1 dòng (9/9 tệp `readback-comment-*.json` hiện có của pr732 là JSON một dòng không có LF cuối, `wc -l` = 0); `SHA256SUMS.txt` = 1 dòng. **Trần ADR-0044** (dòng 5–7): packet `sensitive` chạm authority ≤ 3 tệp và ≤ 300 dòng thêm; packet thường ≤ 6 tệp và ≤ 1.000 dòng thêm cộng xoá. Đọc fail-closed — chính lý do khai `sensitive` ở trên là hồ sơ land thuộc "review/land authority" — thì packet CHẠM authority: số dòng ĐẠT (ước ≤ 200 ≤ 300) nhưng **4 tệp > 3: VƯỢT trần tệp**. ADR-0044 dòng 6–7: vượt thì "dừng TRƯỚC review để revision thiết kế, hoặc khai lý do trong spec". r2 khai lý do và KHÔNG cắt mục tiêu nào: trong bốn tệp chỉ `pr732-wp685-land-evidence.yaml` mang thẩm quyền land, và packet chỉ THÊM vào nó một khối ~9 dòng dưới `quyet_dinh_chu_kho` (N3b khoá 0 dòng xoá, đúng một hunk); hai tệp provenance là dữ liệu chỉ thêm (N4b khoá `A` và `M` `1 0`); tệp còn lại là tài liệu MỚI ở `ops/specs/`. Lời khai lý do KHÔNG phải ngoại lệ đã có: **điều kiện cấp lease** là chủ kho chấp nhận vượt trần tệp bằng một comment trên #750, và lease dẫn URL comment ấy. Chủ kho không chấp nhận ⇒ r3 tách hai packet, không bỏ mục nào: (i) `ops/specs/dinh-chinh-p3-wp685-wp698.md` — mục tiêu 1–3, N1–N2, 1 tệp; (ii) ba tệp `ops/land/` — mục tiêu 4–6, N3–N4, 3 tệp; write set rời nhau. Đọc ngược lại (hồ sơ land không phải authority) cho trần thường 6 tệp / 1.000 dòng: ĐẠT. Đọc nào đúng là quyết định của chủ kho, không phải dữ kiện. |

## Thay đổi so với r1

Soạn r2 ngày 15-10-2026, 08:48–09:10Z: (1) chép r1 vào thư mục tạm và áp `HINT.patch` của review lượt 1 bằng
`patch -p0 --fuzz=0` — rc 0, 17/17 hunk, 0 fuzz, 0 offset, 0 tệp `.orig`/`.rej`; bản sau HINT 115 dòng (khớp số reviewer
ghi), sha256 `516f62a017a5f504eafbd84955b50c1c07982edfa3f8b5e57fb3dffd4cef5b35`; (2) đổi tên đích thành
`ops/specs/no-p3-ho-so-r2.md`; (3) áp hai quyết định chủ kho 15-10-2026 và ĐO LẠI mọi con số mới trên `cay-kho` (bản sao
chỉ đọc tại `55bd0d2`, 601 ref), ghi giờ đo cạnh số. Một sửa hình thức áp cho cả tệp: lệnh đếm O của HINT viết mẫu `grep`
bằng dấu chéo ngược thoát dấu sao; r2 viết cùng mẫu bằng lớp ký tự `[*][*]` (cùng nghĩa, đo cùng kết quả 7).

| lớp (hạng) | chỗ sửa trong r2 | trạng thái · lệch HINT |
|---|---|---|
| `review-class-standard-ngoai-enum` (P2) | hàng `review_class`, `executor` · `reviewer`, `kich_thuoc` | **Đóng.** Lệch HINT: khai `sensitive` thay vì `routine`. Hệ quả: trần tệp ADR-0044 bị vượt (4 > 3) — r2 khai lý do, đặt điều kiện cấp lease và phương án tách cho r3; quyết định chấp nhận vượt trần còn ở chủ kho. |
| `n5-kiem-re-thieu-bien-moi-truong` (P2) | N5 | **Đóng**, theo HINT. |
| `n1-khong-khoa-chu-dung-va-dot-bien-so-dong-song` (P2) | N1 | **Đóng.** Phần S2 và M8 theo HINT; thêm phép kiểm sáu giá trị mở đầu (sha256, blob, commit × hai spec). Lệch HINT: phần O không còn "reviewer so với VERDICT cấp kèm" mà so máy với Phụ lục A và Phụ lục B. |
| `n3-n4-khong-khoa-bat-bien-chi-them` (P2) | mục tiêu 6, N3b, N4b | **Đóng**, theo HINT; N3b thêm phép đòi khoá `landed_quyet_dinh` vắng mặt. |
| `neo-phu-bia-van-xanh` (P2) | mục tiêu 5 (giá trị kỳ vọng, điều kiện DỪNG), N3c, N3d | **Đóng.** Lệch HINT: giá trị kỳ vọng lấy từ một lần GET của phiên soạn r2 (08:55Z) thay vì từ lời khai trong `2f30166`; sha256 thân được ghim trong đặc tả nên N3c giết luôn đột biến "readback bịa giữ đúng trường chủ kho" mà HINT để N3d (cần mạng) gánh — mô phỏng 08:57Z. Giới hạn: một lần đọc, một client. |
| `nguon-o1-o6-khong-co-trong-kho` (P2) | Phụ lục A, mục tiêu 3, N1 | **Đóng** theo quyết định chủ kho (b). Lệch HINT: executor không phải nhận tệp từ điều phối; nguồn nằm ở Phụ lục A, kèm sha256 của tệp nguồn và của bảy dòng. Phương án B của reviewer (đưa VERDICT vào `ops/land/pr732-wp685-provenance/`) không dùng; write set giữ bốn đường. Slug giữ tên cũ vì là định danh, không phải số đếm. |
| `o7-va-quyet-dinh-moi-o-chua-chot` (P3) | mục tiêu 3, Phụ lục B, N1 | **Đóng.** Lệch HINT: O7 được GHI (chỉ ghi nhận, trỏ #751) thay vì cố ý bỏ, vì quyết định (b) chép đủ bảy gạch; mọi "O1–O6"/"sáu" mang nghĩa đếm trong đặc tả đổi thành "O1–O7"/"bảy"; chữ "sáu" của chính VERDICT nguồn giữ nguyên trong trích dẫn. |
| `n2-n3-chinh-xac-hoa` (P3) | đầu mục Nghiệm thu, N3, mục tiêu 4 | **Đóng**, theo HINT; thêm khoá thứ tám `ghi_chu` cho câu "neo chuẩn vẫn là" mà r1 đòi ghi nhưng chưa đặt chỗ. |
| `trich-nguong-sai-nguyen-van` (P3) | `nguon_cap_viec`, `executor` · `reviewer` | **Đóng**, theo HINT; đo lại hai thân comment. |
| `thoi-diem-do-sau-gio-commit` (P3) | `base` | **Đóng.** Lệch HINT: thay "giờ đo thật KHÔNG ĐO ĐƯỢC" bằng phép đo mới (`git ls-remote`, 08:54Z). Mọi giờ đo của r2 nằm sau commit r1 và trước commit chứa r2. |
| `erratum-ten-lien-ket-dang-ky-chua-khai` (P3) | "Ngoài phạm vi", N1 | **Đóng**, theo HINT; thêm giá trị blob và commit nguồn đo được của hai spec gốc. |
| `hinh-dang-ke-thua-khong-chep-bo-dem` (P3) | "Hình dạng kế thừa" | **Đóng**, theo HINT; thêm hình dạng (d) "đếm theo câu tóm tắt của nguồn". |
| `nhanh-chu-kho-chua-merge-ghi-cung-neo` (P3) | "Ngoài phạm vi", N3b, N3c | **Đóng** theo quyết định chủ kho (a). Lệch HINT: bỏ bước "trước khi ghi, hỏi chủ kho bỏ hay giữ" (đã có câu trả lời: bỏ). Đo thêm: 0 PR từ nhánh ấy (08:57Z), nên lớp không lên P2. |

## Ngoài phạm vi (cố ý)

- **KHÔNG sửa** `ops/specs/ci-g5-cong-cu-va-tiep-r14.md` (sha256 `ed027f410aac7eeedd60335459ba8cfef521a34730fea68c1255533bb56f1a21`) hay `ops/specs/launcher-con-song-esrch-r28.md` (sha256 `8007edf4e00aaefc298bf299bf19be9a71c54e73ff6a1610eb676a806773e156`): cả hai đã đóng băng, có lease neo băm; sửa đè làm băm trong lease trỏ vào thứ không còn tồn tại.
- **KHÔNG sửa** quyết định `landed` của wp685 hay neo chuẩn của nó; chỉ THÊM neo phụ.
- Mục nợ 4 (#751), 5–6 (#752), nhóm `ops/cong_cu_test.py` (chờ #748) và hai mục đo Windows: thuộc packet khác.
- **KHÔNG đóng** hai mục `S2-SPEC-HASH-CUA-R11` và `M8-GIU-RANG-CACH-NOI-R13` trong `no_con_mo` của `ops/land/pr721-wp698-land-evidence.yaml` (ngoài write set): sau packet này hai mục vẫn "mở" ở đó; trỏ sang tệp đính chính hay đóng chúng thuộc packet khác.
- **Tệp đính chính không cần băm hay đăng ký riêng** — đo 15-10-2026 ~08:52Z: không mã nào liệt kê `ops/specs/*.md` (ngoài allowlist tiền tố ở `ops/ci_duong_nhanh.py` dòng 115), `ops/` không nằm trong `RELEASE_MANIFEST.json` (0 chỗ `"ops/`). Tiền lệ `ops/specs/*.ERRATA.md` (`CI-DOT-BIEN-CHIA-MANH-r2.ERRATA.md`, `LAND-DOC-RECEIPT-THU-HOI-C1a1a-r5.ERRATA.md`) mở bằng sha256 + blob + commit của spec gốc và câu "Không sửa tệp ấy; đính chính sống ở đây"; tệp này gộp hai spec nên đặt tên `dinh-chinh-…`, và PHẢI mở bằng ba thứ ấy cho CẢ HAI spec gốc. Giá trị đo 15-10-2026 08:56Z tại `6f121a3` (mỗi tệp có đúng 1 commit chạm tới): r14 blob `b427f19d2949c73e2b8088e13999915e8114f186`, commit nguồn `d17ec09088acf674a05638345f7b3ec28ff03c6d`; r28 blob `fa07ca1bc3707bc273bf25349ffa6f3ca6ad6160`, commit nguồn `4a35f633e1b3f05be12eecf74ab9a8a17ef82c69`.
- **Nhánh `ducthangho-patch-1` KHÔNG merge — quyết định chủ kho 15-10-2026 (a).** Đo 15-10-2026: đầu nhánh = `2f30166f482552162f3cdc993c19e44594ae79dd` cả ở `cay-kho` (08:48Z) lẫn máy chủ (`git ls-remote`, 08:54Z); một commit của chủ kho (2026-10-11T07:55:44+07:00, cha `b2ca3a182db3dee45b214ebba95be93c016ba140` = merge PR #739; `master` đã tiến 38 commit so với nó); KHÔNG là tổ tiên của `master` (`merge-base --is-ancestor` rc 1); là commit chưa merge DUY NHẤT chạm write set (`git log --all --not master` trên bốn đường, 09:00Z); 0 PR ở mọi trạng thái có head là nhánh ấy (`gh api` GET `pulls?head=ducthangho:ducthangho-patch-1&state=all`, 08:57Z). Commit thêm đúng một dòng vào hồ sơ pr732, cấp `trang_thai_packet`, nguyên văn:
  `landed_quyet_dinh: 'chu kho #685 comment 6103888794 (2026-10-11T00:45:59Z); gate push tren 11cf185 (run 38076548735) success'`.
  Chủ kho quyết bỏ nhánh: neo phụ cho comment `6103888794` do CHÍNH packet này làm, kèm readback (mục tiêu 4–6). Executor
  **KHÔNG** chép dòng ấy, không cherry-pick, merge hay rebase lên `2f30166`; hồ sơ sau packet KHÔNG có khoá
  `landed_quyet_dinh` (khoá bằng N3b và N3c). Dòng được chép nguyên văn ở đây chỉ để người đọc thấy giờ trong đó trùng giá
  trị kỳ vọng đo được ở mục tiêu 5 — nhánh có thể bị xoá và commit thành không tra được. Xoá ref nhánh ấy KHÔNG thuộc packet
  này (ref, không phải tệp của write set). Lease: 0 trong 618 blob lease khác nhau ở đầu 601 ref nhắc tới bất kỳ đường nào
  của write set (so chuỗi `pr732-wp685-land-evidence`, `pr732-wp685-provenance`, `dinh-chinh-p3-wp685-wp698`,
  `readback-comment-6103888794`; đo 08:53Z); đo lại lúc cấp lease (L5).

## Mục tiêu

Mỗi dòng chiếu vào đúng một đường dẫn của `write_set` (L2).

1. **[`ops/specs/dinh-chinh-p3-wp685-wp698.md`] Đính chính S2 của wp698 r14 (mục nợ 1).** Dòng 3261–3262 của r14 ghi
   "chưa có comment chủ kho xác nhận closure neo `spec_hash` **của r11** (Q10)". Chữ đúng: "… neo `spec_hash` **của r14**"
   — đúng như chủ kho đã đọc ở comment cấp quyền #698 `6091633467` ("Tôi đọc S2 theo depends_on (4): neo spec_hash của r14";
   đo ~08:55Z: chuỗi có trong `body` của `ops/land/pr721-wp698-provenance/readback-comment-6091633467.json`). Đo ~08:52Z
   trên blob `6f121a3`: cụm "neo `spec_hash` **của r11**" có đúng 1 chỗ trong 5.374 dòng của r14, ở dòng 3262.
2. **[cùng tệp] Đính chính M8 "Giữ răng" của wp698 r14 (mục nợ 2).** Dòng 2729–2731: vế "tập khoá `KQ` của ba cửa con chứa tập
   của g1 với độ dài mọi danh sách và từ điển lồng không nhỏ hơn (A10 (v))" thiếu "cùng đường, cùng loại". Chữ đúng theo
   gợi ý VERDICT review đặc tả lượt 14 (`ops/reviews/wp698-spec-review-14-claude-verdict.md`, sha256
   `892eeb8a200cec3083b565ffdfe5e26e078ab4ccdafb861c7324b712028e76c7`, dòng 135; đo ~08:55Z): "… cùng đường, cùng loại, độ
   dài không nhỏ hơn (A10 (v), cách tính r14)". Ghi rõ: điều kiện CẦN, không đổi kết luận đo nào (theo chính VERDICT ấy).
3. **[cùng tệp] Ghi nhận O1–O7 của wp685 r28 (mục nợ 3).** Nguồn: mục "QUAN SÁT KHÔNG XẾP LỚP" của VERDICT review lượt 5
   r28 (sha256 `d3f1d9db4896efe8c1b62112a3d0aa479b64c5dc110da1d323b3297d7e7c45fb`), chép nguyên văn ở **Phụ lục A** của
   chính đặc tả này (quyết định chủ kho (b)). Executor đọc nguồn từ Phụ lục A, không cần tệp VERDICT; có tệp ấy thì
   `sha256sum` phải bằng băm trên và dòng 57–63 của nó phải bằng Phụ lục A từng byte — lệch ⇒ DỪNG. Với mỗi O1…O7 ghi: khối
   nguyên văn (từ Phụ lục A, không tóm tắt), dòng r28 bị nói tới và quyết định — đúng như **Phụ lục B**. Phạm vi lời khai,
   tệp đính chính nói đúng mức này, không mạnh hơn: với O1–O6, VERDICT nói thẳng không cái nào đổi quyết định hay việc của
   executor (VERDICT dòng 7, 54) và diff r27 → r28 không chạm acceptance hay closure (dòng 7); với O7, VERDICT chỉ xếp nó
   vào cùng mục "không xếp lớp" của một verdict `approve` 0 lớp và ghi "đã biết, không hồi quy" — không có câu riêng về
   acceptance hay closure.
   - **Đếm** (đo ~08:52Z trên tệp nguồn): mục ấy có **bảy** gạch đầu dòng, dòng 57…63 = O1…O7
     (`grep -c "^- [*][*]O[0-9]"` = 7); dòng 7, 12, 54 của VERDICT nói "sáu"/"O1–O6" — đó là chữ của nguồn, tệp đính chính
     trích nguyên, không sửa. r1 đếm sáu theo câu tóm tắt ấy; r2 đếm trên tệp.
   - **Trước r2, nguồn không nằm trong kho** (đo 08:53Z, `cay-kho` 601 ref, 45.743 đối tượng git, 23.761 blob): 0 blob dài
     32.989 byte (cỡ của VERDICT), 0 blob chứa "hẹp hơn diff ở hai chỗ không chuẩn tắc" (tiêu đề O1). Phụ lục A là chỗ đầu
     tiên chữ ấy vào kho.
4. **[`ops/land/pr732-wp685-land-evidence.yaml`] Neo phụ landed wp685 (mục nợ 11).** Thêm khối `neo_phu` dưới
   `trang_thai_packet.quyet_dinh_chu_kho` (cùng cấp `neo_ben`, ngay sau khối `neo_ben_do_duoc`, đứng trước `landed_ly_do`)
   với tám khoá: `url` (= `html_url` của readback), `luc` (`'<created_at> (created_at = updated_at)'` khi hai giá trị bằng
   nhau, như tiền lệ `quyet_dinh_chu_kho.luc`; khác nhau thì ghi cả hai), `nguoi_dang` (`user.login`), `author_association`,
   `performed_via_github_app` (nguyên giá trị: `null` hay tên), `so_byte` (số byte UTF-8 của `body`), `sha256` (của `body`
   UTF-8), `ghi_chu` (nói đây là neo PHỤ; **neo chuẩn vẫn là** `neo_ben` = `pull/739#issuecomment-6103749546`;
   `landed_hieu_luc_tu` không đổi). Mọi giá trị đo từ readback ở mục 5, không lấy từ dòng `landed_quyet_dinh` của `2f30166`.
5. **[`ops/land/pr732-wp685-provenance/readback-comment-6103888794.json`] Readback thô** của comment ấy: đầu ra nguyên byte
   của `gh api repos/ducthangho/tra-luat/issues/comments/6103888794` (GET), không sửa, không định dạng lại.
   **Giá trị kỳ vọng** — phiên soạn r2 GET một lần lúc 15-10-2026 08:55Z bằng `gh api` (client GitHub tích hợp của Claude
   Code, qua proxy của phiên; rc 0, phản hồi 2.273 byte): `id` 6103888794 · `html_url`
   `https://github.com/ducthangho/tra-luat/issues/685#issuecomment-6103888794` · `user.login` `ducthangho` ·
   `author_association` `OWNER` · `performed_via_github_app` `null` · `created_at` = `updated_at` = `2026-10-11T00:45:59Z` ·
   `body` 631 byte UTF-8, sha256 `cc38f7996531c5239f2e4e8ad760fcc20a2720a132f90de81251e65342e8f09b`, chứa chuỗi `landed` và
   `685`, 0 thực thể HTML (`&#39;`, `&#34;`, `&gt;`, `&lt;`). Giờ ấy trùng lời khai của chủ kho trong `2f30166` (xem "Ngoài
   phạm vi"). Đây là MỘT lần đọc bằng MỘT client; readback của executor là lần đọc thứ hai, N3d là lần thứ ba.
   DỪNG — không đặt `neo_phu`, không dựng readback từ bản đọc MCP, không tự sửa giá trị kỳ vọng — nếu: (a) `gh api` GET không
   chạy được trong phiên executor (CLAUDE.md ghi REST tới `repos/<kho>` từng bị proxy chặn 403 ở phiên web, đo 15–17-08-2026;
   phiên soạn r2 GET được ngày 15-10, nhưng phiên executor là phiên khác nên điều này KHÔNG ĐO ĐƯỢC trước); (b) bất kỳ trường
   nào ở trên lệch giá trị kỳ vọng — comment bị sửa sau 08:55Z cũng là lệch (`updated_at` đổi): báo điều phối, chủ kho
   quyết; (c) `body` không chứa `landed` hoặc không chứa `685`. Tiền lệ của chính kho: `ops/land/pr478-land-evidence.yaml`
   dòng 104 gọi sự tồn tại và nội dung comment không kèm response thô và phép đối chiếu độc lập là ATTESTATION, không phải
   bằng chứng.
6. **[`ops/land/pr732-wp685-provenance/SHA256SUMS.txt`] Cập nhật** dòng băm cho tệp ở mục 5; mọi dòng cũ giữ nguyên. Tệp đang xếp theo tên theo
   `LC_ALL=C` (44 dòng, `sha256sum -c` 44 OK, `LC_ALL=C sort -c -k2` rc 0, đo ~08:50Z): chèn dòng mới giữa `readback-comment-6103749546.json` và `readback-comments-732.json`, không nối vào cuối.

## Nghiệm thu

Mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3). Mọi đột biến phải được commit: phép so `6f121a3..HEAD` không thấy cây làm việc
chưa commit (review lượt 1 đo, 15-10-2026 06:02–06:45Z).

- **N1 (mục 1–3):** tệp đính chính mở bằng sha256, blob và commit nguồn của CẢ HAI spec gốc, đúng sáu giá trị ở "Ngoài phạm
  vi" (thiếu hay lệch một ⇒ ĐỎ), rồi có đúng ba phần `S2-r14`, `M8-r14`, `O1..O7-r28`.
  - **S2, M8:** mỗi trích gồm dòng `tệp: <đường> · sha256 <64 hex> · dòng <a>–<b>`, rồi khối ```` ```text ```` chép NGUYÊN các
    dòng a..b của blob `6f121a3:<đường>` (cả dòng, không rút thành cụm); thêm dòng `chữ đúng:` mang đúng chuỗi ở mục 1 và
    mục 2. Phép đo ĐỎ: script trích dòng a..b từ blob và so BẰNG TUYỆT ĐỐI với khối trích, so sha256 đầy đủ của blob, và
    `grep -F` hai chuỗi chữ đúng. Đột biến (mỗi cái phải ĐỎ): số dòng lệch +1 và lệch −1 ở TỪNG phần; đổi một ký tự trong
    khối trích; `r14` → `r13` ở chữ đúng; chữ đúng = chữ cũ. Review lượt 1 đo (15-10-2026 06:02–06:45Z): trích CỤM rồi so
    "chứa" (cách r1 tự dùng ở mục 1–2) thì lệch +1 SỐNG ở S2 (cụm ở dòng 3262 trong 3261–3262) lẫn M8 (cụm ở dòng 2731 trong
    2729–2731), và không phép đo nào của r1 chạm chữ đúng (đổi `r14` thành `r13` hay giữ nguyên `r11` vẫn XANH).
  - **O1..O7:** đúng bảy khối `### O1` … `### O7`, theo thứ tự. Khối thứ k có một khối ```` ```text ```` chứa đúng MỘT dòng,
    BẰNG TUYỆT ĐỐI dòng thứ k của Phụ lục A (đọc từ blob của đặc tả r2 tại commit mà lease neo); rồi dòng `dòng r28:` mang
    đúng tập số dòng của O ấy ở Phụ lục B; rồi dòng `quyết định:` bắt đầu bằng đúng nhãn ở Phụ lục B. Phép đo ĐỎ: script so
    từng khối với Phụ lục A, so tập số dòng và nhãn với Phụ lục B, và với mỗi cặp (dòng, cụm kiểm) ở Phụ lục B kiểm cụm nằm
    trong dòng ấy của blob `6f121a3:ops/specs/launcher-con-song-esrch-r28.md` (O4: nối dòng 162–163 bằng một dấu cách sau
    khi bỏ khoảng trắng đầu và cuối mỗi dòng). Đột biến (mỗi cái phải ĐỎ): bỏ khối O7; đổi một ký tự trong một khối O; đổi
    thứ tự hai khối; một số dòng r28 lệch +1 hay −1; đổi nhãn quyết định của O3 thành nhãn của O1. Đo 15-10-2026 08:52Z: cả
    14 cặp (O, dòng) ở Phụ lục B có cụm ở dòng nêu và KHÔNG có ở dòng lệch +1 hay −1.
- **N2 (spec gốc bất biến):** `git diff --stat 6f121a3..HEAD -- ops/specs/ci-g5-cong-cu-va-tiep-r14.md ops/specs/launcher-con-song-esrch-r28.md`
  rỗng. Đột biến: chạm một byte spec gốc ⇒ lệnh trả không rỗng ⇒ ĐỎ.
- **N3 (mục 4–6):** `yaml.safe_load` hồ sơ pr732 thành công; `trang_thai_packet.landed` vẫn `true`; `neo_ben` vẫn đúng chuỗi
  `https://github.com/ducthangho/tra-luat/pull/739#issuecomment-6103749546` (trường là URL, không phải số `6103749546`);
  `neo_phu.sha256` = sha256 của trường `body` trong readback (UTF-8). Đột biến: sửa 1 ký tự sha256 ⇒ ĐỎ; đổi `neo_ben` ⇒
  ĐỎ (cả hai review lượt 1 đã đo ĐỎ, 06:02–06:45Z).
  - **N3b (chỉ THÊM):** `git diff --numstat 6f121a3..HEAD` của hồ sơ pr732 có 0 dòng xoá; `git diff -U0` có đúng MỘT hunk
    với dòng thêm đầu là `    neo_phu:`; khoá `landed_quyet_dinh` không có trong `trang_thai_packet`. Đột biến: sửa một chữ
    của `landed_hieu_luc_tu` hay của `authorized_head_sha` ⇒ ĐỎ (review lượt 1 đo: N3 như r1 viết XANH ở cả hai); chép dòng
    `landed_quyet_dinh` của `2f30166` ⇒ ĐỎ (hai hunk, và khoá có mặt).
  - **N3c (neo phụ chép đúng, đúng chủ, đúng giá trị kỳ vọng):** script so `neo_phu` với readback VÀ với giá trị kỳ vọng ở
    mục 5: readback `id` = 6103888794; `url` = `html_url` = URL kỳ vọng; `nguoi_dang` = `user.login` = `ducthangho`;
    `author_association` = `OWNER` ở cả hai; `performed_via_github_app` là `null` ở cả hai; `created_at` = `updated_at` =
    `2026-10-11T00:45:59Z` và phần trước dấu cách đầu tiên của `luc` bằng nó; `so_byte` = số byte UTF-8 của `body` = 631;
    `sha256` = sha256 của `body` = `cc38f799…f09b` (đủ 64 ký tự như mục 5); `ghi_chu` chứa `pull/739#issuecomment-6103749546`.
    Đột biến (mỗi cái phải ĐỎ): (i) readback bịa người đăng khác, thân vô nghĩa, `sha256`/`so_byte`/SHA256SUMS cập nhật cho
    khớp; (ii) readback giữ đúng mọi trường chủ kho, đổi một ký tự của thân, `sha256`/`so_byte`/SHA256SUMS cập nhật nhất quán;
    (iii) chép dòng `landed_quyet_dinh`; (iv) `sha256` lệch một ký tự. Đo 15-10-2026 08:57Z trên bản mô phỏng (hồ sơ pr732
    tại `6f121a3` chèn khối `neo_phu` 9 dòng, readback = phản hồi GET ở mục 5): nền XANH, cả bốn đột biến ĐỎ; bỏ riêng phép
    so với sha256 kỳ vọng thì (ii) XANH — nên chính giá trị ghim trong đặc tả là thứ giết (ii), ca mà review lượt 1 đo là
    sống qua N3, N3b, N3c, N4, N4b của HINT.
  - **N3d (đối chiếu sống, reviewer chạy):** `gh api` GET lại cùng đường và so các trường ổn định (`id`, `user.login`,
    `author_association`, `performed_via_github_app`, `created_at`, `updated_at`, `body`) với tệp readback; không có mạng ⇒
    ghi KHÔNG ĐO ĐƯỢC, không tính là đạt. Đột biến: sửa 1 ký tự `body` của readback (cập nhật SHA256SUMS cho khớp) ⇒ N3d
    ĐỎ. Nói cho đúng phạm vi: khi giá trị đã ghim ở mục 5, mọi đột biến TRÊN HIỆN VẬT mà N3d bắt thì N3c cũng bắt; giá trị
    riêng của N3d là đối chiếu với MÁY CHỦ — nó bắt comment bị sửa sau các lần đọc trước (`updated_at` mới), và ca hai lần
    đọc trước cùng sai một kiểu.
- **N4:** `sha256sum -c` trong `ops/land/pr732-wp685-provenance/` (theo `SHA256SUMS.txt`) đạt hết. Đột biến: sửa 1 byte
  readback ⇒ ĐỎ (review lượt 1 đã đo ĐỎ, 06:02–06:45Z).
  - **N4b (provenance chỉ THÊM):** `git diff --name-status 6f121a3..HEAD -- ops/land/pr732-wp685-provenance/` chỉ có `A readback-comment-6103888794.json` và
    `M SHA256SUMS.txt`; `git diff --numstat` của `SHA256SUMS.txt` = `1 0`; `LC_ALL=C sort -c` trên cột tên đạt. Đột biến: xoá một dòng cũ; sửa một tệp
    cũ cùng dòng băm của nó; để dòng mới ở cuối tệp ⇒ ĐỎ (review lượt 1 đo: N4 như r1 viết XANH ở cả ba).
- **N5 (cổng kho):** CI PR xanh; bước `DUONG_NHANH - kiem re …` của `ci.yml` (dòng 646–657, đo ~08:52Z) chạy `doctrine-scan`
  rồi `kiem-re` VỚI bốn biến `CI_DUONG_NHANH_SU_KIEN=pull_request`, `CI_DUONG_NHANH_GOC` (base), `CI_DUONG_NHANH_DAU` (head
  PR), `CI_DUONG_NHANH_MERGE` (`github.sha`, commit merge ref). Dựng lại tại chỗ: `GOC` = `6f121a3…`, `DAU` = head PR, `MRG`
  = commit `git merge --no-ff` DAU vào GOC, checkout `MRG`, rồi
  `CI_DUONG_NHANH_SU_KIEN=pull_request CI_DUONG_NHANH_GOC=$GOC CI_DUONG_NHANH_DAU=$DAU CI_DUONG_NHANH_MERGE=$MRG python ops/ci_duong_nhanh.py kiem-re`
  ⇒ ĐẠT (`4 tep doi, 0 loi`, rc 0; cả 4 tệp nằm trong `ops/{land,specs}/**`). Lệnh TRẦN `python ops/ci_duong_nhanh.py kiem-re`
  KHÔNG phải phép đo: rc 1 ("kiem-re CHI chay khi diff toan ho so") trên CẢ cây sạch lẫn cây thêm tệp nhị phân (review lượt 1
  đo, 06:02–06:45Z). Đột biến: thêm một tệp nhị phân vào provenance rồi chạy ĐÚNG lệnh có bốn biến ⇒ rc 1, dòng
  `tep ho so nhi phan` (đỏ vì tệp nhị phân, không vì thiếu biến; đã đo 15-10 ở PR #749 và lại ở review lượt 1).
  `doctrine-scan` chỉ đọc `.claude/skills/**`, `.agents/skills/**`, `CLAUDE.md` (đo ~08:58Z: 10 tệp, rc 0) — không tệp nào
  trong write set, nên KHÔNG thể đỏ do packet này; giữ làm cổng CI, không tính là tiêu chí nghiệm thu.

## Hình dạng kế thừa

`khong_ap_dung` cho đếm hình dạng lỗi của mã (packet không sửa mã). Ghi lại bốn hình dạng đã gặp ở packet tiền nhiệm hay
ở chính r1, có thể tái phát ở đây: (a) **tệp nhị phân trong hồ sơ** bị `kiem-re` từ chối (PR #749 lượt `0876395`; lời khai
trong thân commit `c29ee11`) — readback phải là JSON văn bản; (b) **lời khai vị trí/số dòng trôi** (L5) — mọi số dòng trong
tệp đính chính phải đo trên blob tại `6f121a3`; (c) **vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba** — wp685 r28 §9 đếm 15
lần tới lượt 14 (r28 dòng 3541–3550), wp698 r14 §9 gọi tên nó (dòng 3493). Đính chính chữ cũng dính hình dạng ấy, nên
executor tự liệt kê MỌI chỗ cùng hình dạng trước khi viết. Đã liệt kê trên blob `6f121a3` (đo ~08:52Z): "neo `spec_hash`
**của r11**" ở r14 = 1 chỗ (dòng 3262); "độ dài mọi danh sách" ở r14 = 1 chỗ (dòng 2731); "cùng đường, cùng loại" ở r14 =
0 chỗ. Executor chạy lại và ghi số. (d) **đếm theo câu tóm tắt của nguồn thay vì đếm trên nguồn** — r1 viết "O1–O6" vì
VERDICT tự nói "sáu" (dòng 7, 12, 54) trong khi mục có bảy gạch; mọi số đếm trong tệp đính chính phải đếm trên tệp, không
chép từ câu tóm tắt.

## Chưa đo được

- Liệu reviewer cùng họ (Sonnet) có bắt được sai về NGHĨA trong phần O (sai về CHỮ thì N1 bắt bằng máy) — không đo được
  trước; mức `review_deferred`.
- Thân comment 6103888794 có thể bị tầng đọc MCP chuẩn hoá thực thể HTML (CLAUDE.md, bài học 22-08-2026): băm phải tính
  trên readback REST (`gh api`), không trên bản đọc qua MCP.
- Comment 6103888794: phiên soạn r2 đọc được MỘT lần bằng MỘT client (08:55Z, mục 5). Byte lưu trên GitHub so với byte đã
  đến: chưa có client thứ hai để đối chiếu (CLAUDE.md, bài học 22-08-2026); readback của executor và N3d là lần đọc thứ hai,
  thứ ba, cùng loại client. Việc phiên executor gọi được `gh api repos/…`: KHÔNG ĐO ĐƯỢC trước.
- Sổ nợ P3 của phiên điều phối (mục 1, 2, 3, 11), quyết định Q1–Q10 và hai quyết định chủ kho 15-10-2026 cho r2 không có
  bản ghi trong kho: KHÔNG ĐO ĐƯỢC.
- Lượt CI `gate-ops` đỏ ở `0876395` của PR #749 chỉ có lời khai trong thân commit `c29ee11` ("gate-ops tren 0876395 DO … 23 tep .zip/.log.gz"); chạy lại CI thật: KHÔNG ĐO ĐƯỢC.
- Chủ kho có chấp nhận vượt trần tệp ADR-0044 (hàng `kich_thuoc`) hay không: quyết định chưa có; là điều kiện cấp lease.

## Phụ lục A — nguyên văn O1…O7 (VERDICT review wp685 r28 lượt 5)

Nguồn: VERDICT review wp685 r28 lượt 5, sha256 `d3f1d9db4896efe8c1b62112a3d0aa479b64c5dc110da1d323b3297d7e7c45fb`
(68 dòng, 32.989 byte; nằm ở scratchpad phiên điều phối, không có trong kho trước r2), dòng 57–63, mục "QUAN SÁT KHÔNG XẾP
LỚP". Bảy dòng trong khối dưới đây BẰNG từng byte dòng 57–63 của tệp ấy; sha256 của bảy dòng ấy, mỗi dòng kết thúc bằng một
LF (6.368 byte), là `7ad7791d184f3734e0716312dea4164bc0ebb882dc0e2e3f5d620a660cc79ab1` (đo 15-10-2026 ~08:52Z). Kiểm lại
không cần tệp nguồn: lấy các dòng giữa hai dòng rào của khối, nối mỗi dòng với một LF, băm; lệch ⇒ Phụ lục A đã bị sửa ⇒
DỪNG. Chữ trong khối là của reviewer lượt 5, không phải lời khai của đặc tả này; các số `L<n>` trong khối là số dòng r28,
riêng `L168`, `L170` của O4 là số dòng r27.

```text
- **O1 — bảng "Thay đổi so với r27" hẹp hơn diff ở hai chỗ không chuẩn tắc** (kéo theo ba câu dựa vào bảng ấy: ô `thay_the_cho` mục (r28) *"danh sách đủ các chỗ đổi … là bảng 'Thay đổi so với r27'"*, MCR gạch 3 *"the places changed from r27 to r28 are listed in the spec's table of changes against r27"*, và vế r27 → r28 của ô `revision`). (a) Câu mới L172 *"Phiên soạn r28 đã rà băm rút gọn và trích dòng PROTOCOL bằng script; kết quả không phải acceptance và không ràng buộc ai."* không có ở cột "chỗ sửa trong r28" — hàng cuối chỉ ghi "bảng này", trong khi hàng tương ứng của bảng r26 (do r27 viết) ghi "bảng này và đoạn kiểm r27". (b) Ô "HINT lệch phép đo" của hàng `bam-rut-gon-lech-ban-day-du` (L188): bảng r28 khai "bỏ số đếm của VERDICT lượt 3"; word-diff (M2, M3) cho thấy còn bỏ vế "rà toàn tệp thêm" và thêm "ở cột bên trái … là phần ngoài HINT". Nghĩa giữ nguyên (VERDICT lượt 3 ghi đúng "Phần đầu r26: 71 băm rút gọn", đọc ở `../cr685-r26/goi/VERDICT.md`), chỉ bớt một lời khai phạm vi rà của phiên soạn r27 — đúng hướng chỉ thị. Vì sao không xếp lớp: cả hai nằm trong khối bảng/kiểm của r28, không chuẩn tắc; không đổi tiêu chí, closure, authority hay việc executor; phần r23 → r28 mà chủ kho dựa vào đo bằng nhau (M4, M5). Nếu có r29 vì lý do khác: hàng cuối "…; bảng này và câu kiểm r28 ngay dưới"; hàng 2 "…; ô 'HINT lệch phép đo' bỏ số đếm của VERDICT lượt 3 và vế 'rà toàn tệp thêm', nói ba chỗ sai đuôi là phần ngoài HINT".
- **O2 — con trỏ "ở cột bên trái"** trong ô "HINT lệch phép đo" (L188, cột 5): ba chỗ sai đuôi được liệt kê ở cột 3 ("chỗ sửa trong r27"); cột liền trái (cột 4, "đo lại của phiên soạn r27") nay chỉ còn câu thu gọn. Đọc chặt thì con trỏ lệch một cột; đọc là "một cột phía trái" thì đúng. Ô lịch sử, không quyết định nào dựa vào. Nếu có r29: "ở cột 'chỗ sửa trong r27'".
- **O3 — bằng chứng cho phép sửa đuôi ngoài HINT chỉ còn ở r27.** Ba chỗ §1 L596, L630, §10 L3708 (`6f07a7cf…3ed8` → `…25e8`, sửa từ r27) nay không còn câu bằng chứng trong r28: câu *"Tệp test thử 'bytes' của rig r11 (`lt11_bytes.py`) có sha256 `6f07a7cfecea…3925e8`; bản 'latin-1' … `c4267574…7905`"* bị bỏ (M7: −1 mỗi chuỗi); bản đầy đủ `6f07a7cfecea40852ac0671f6dc9261ab811860ecb434b41fe66599b7b3925e8` chỉ có ở VERDICT lượt 4 M9. r28 vẫn khai việc sửa ("sửa đuôi … cho khớp băm đầy đủ", ô `revision`) và khai việc bỏ câu ("bỏ cả câu về tệp thử 'bytes' của rig r11", bảng r28 hàng 2). Vì sao không xếp lớp: con trỏ "chữ đầy đủ của r27 ở tệp r27" đúng (blob r27 `3cf7ddb8…ac25` không đổi ở HEAD), phép sửa đã được lượt 4 đo đúng, và băm rig §1/§10 không vào acceptance, closure hay việc executor.
- **O4 — con trỏ "chữ đầy đủ của r27 ở tệp r27" dẫn tới đúng hai lời khai mà lượt 4 đo là rộng hơn phép đo** (r27 L168 "(19 chỗ)"; L170 "8 … không có bản trong kho hay scratchpad", "25 … đo không được ở đây"). Chữ đã sửa (HINT lượt 4) chỉ còn ở `luot4/HINT.patch` và bản trung gian `acaa21e2…010d`, không ở kho; r28 nêu VERDICT/HINT lượt 4 chỉ bằng sha256, và VERDICT/HINT lượt 1–4 đều nằm ở scratchpad điều phối (M10), không có trong kho cục bộ (M18: 0/23 073 blob cùng kích thước với tám tệp ấy). VERDICT lượt 4 đã đăng lên GitHub chưa, và ref phía máy chủ: `KHÔNG ĐO ĐƯỢC` (lý do 5). Vì sao không xếp lớp: r28 đóng dấu các kết quả ấy "không phải acceptance và không ràng buộc ai"; không quyết định nào dựa vào chúng. Việc đáng làm thuộc ghi sổ, không thuộc đặc tả: lưu VERDICT/HINT các lượt vào nơi có băm trong kho, để con trỏ băm của r28 trỏ tới thứ đọc lại được.
- **O5 — phạm vi chỉ thị "bỏ mọi số đếm phép rà".** PROMPT.md tóm tắt chỉ thị là "bỏ mọi số đếm phép rà khỏi spec"; r28 chỉ thu gọn ô/đoạn của r27. Năm đoạn "Kiểm lúc soạn r22…r26" (r28 L307, L275, L254, L236, L209) và các ô "đo lại" của bảng r24, r25, r26 vẫn giữ số đếm lịch sử (ví dụ L232 "`diff -U0` r23 → r24: 14 hunk"). Lời tự mô tả của r28 khớp việc nó làm (`nguon_cap_viec` mục (r28): *"thu gọn phần tự khai phép rà của phiên soạn (không ghi số đếm phép rà vào đặc tả)"*; bảng r28: *"thu gọn chính các ô và đoạn ấy"*), và mỗi đoạn lịch sử tự khai phạm vi ("mọi số đếm dưới đây đo trên chính tệp rNN"). Nguyên văn chỉ thị giao cho phiên soạn r28: `KHÔNG ĐO ĐƯỢC` (lý do 3). Vì sao không xếp lớp: lịch sử, không ảnh hưởng quyết định; chỉ thị có ý rộng hơn hay không là việc điều phối tự quyết.
- **O6 — câu tự khai mới L172.** Vế "đã rà băm rút gọn" có bằng chứng (`../wp685-r28/rg_r28.tsv`, 293 dòng, ghi trước commit r28); vế "trích dòng PROTOCOL" không có tệp đầu ra nào ⇒ `KHÔNG ĐO ĐƯỢC` (lý do 3). Đo thay: công cụ phiên soạn trên r28 `{'KHOP': 18, 'SO_CU': 1}` rc=0 và bộ đếm độc lập 13 chỗ chuỗi 597/598, cả 13 là chữ r27 đã đo đúng (M6). Vì sao không xếp lớp: câu tự đóng dấu không ràng buộc ai; không quyết định nào dựa vào nó.
- **O7 — đã biết, không hồi quy:** ba giá trị YAML của lease nháp bị cắt ở " #" (M13); cổng lease không đọc `spec_sha256_required`, `spec_hash`, `plan_hash`, `write_set_hash`, `spec_path` (M11: D2, D3, D5–D7 rc=0) ⇒ chuỗi băm chỉ có phép đo tay, phải đo lại cả năm mắt xích sau mọi lần đổi byte. Mission r8 `spec_hash` của wp709 `f569b613…005c`: ngoài chuỗi wp685, không xét (HẸP).
```

## Phụ lục B — dòng r28 và quyết định của từng O

Số dòng r28 lấy từ chính khối O (dạng `L<n>`), riêng O4 lấy từ phép đo bổ sung của review đặc tả lượt 1 (con trỏ ngắt
dòng). Cụm kiểm đo 15-10-2026 08:52Z trên blob `6f121a3:ops/specs/launcher-con-song-esrch-r28.md` (3.940 dòng): có ở dòng
nêu, không có ở dòng lệch +1 hay −1. Nhãn quyết định là chuỗi đầu của dòng `quyết định:` trong tệp đính chính.

| O | dòng nguồn | dòng r28 | cụm kiểm | nhãn quyết định · ghi chú |
|---|---|---|---|---|
| O1 | 57 | 172 · 188 | 172: `Phiên soạn r28 đã rà băm rút gọn và trích dòng PROTOCOL bằng script` · 188: `ở cột bên trái` | `ghi nhận kèm chữ đề nghị r29` — chữ đề nghị là câu "Nếu có r29 vì lý do khác: …" trong chính khối O1; packet này không mở r29 |
| O2 | 58 | 188 | `ở cột bên trái` | `ghi nhận kèm chữ đề nghị r29` — câu "Nếu có r29: …" trong khối O2 |
| O3 | 59 | 596 · 630 · 3708 | `6f07a7cf…25e8` (cả ba dòng) | `chỉ ghi nhận` |
| O4 | 60 | 162–163 (nối) | `chữ đầy đủ của r27 ở tệp r27` | `chỉ ghi nhận` — `L168`, `L170` trong khối là dòng r27, không phải r28 |
| O5 | 61 | 209 · 232 · 236 · 254 · 275 · 307 | 209: `**Kiểm lúc soạn r26**` · 232: `` `diff -U0` r23 → r24: 14 hunk `` · 236: `**Kiểm lúc soạn r25**` · 254: `**Kiểm lúc soạn r24**` · 275: `**Kiểm lúc soạn r23**` · 307: `**Kiểm lúc soạn r22**` | `chỉ ghi nhận` |
| O6 | 62 | 172 | `Phiên soạn r28 đã rà băm rút gọn và trích dòng PROTOCOL bằng script` | `chỉ ghi nhận` |
| O7 | 63 | — (khối không nêu dòng r28; nó nói về lease nháp và cổng lease) | — | `chỉ ghi nhận` — vế "cổng lease không đọc `spec_sha256_required`, `spec_hash`, `plan_hash`, `write_set_hash`, `spec_path`" là mục nợ 4 của packet #751 (`ops/specs/no-p3-lease-spec-hash-r1.md` dòng 8), không xử ở đây |
