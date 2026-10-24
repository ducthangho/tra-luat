# Đặc tả packet `no-p3-cong-cu-ho-so` r4 — nợ P3 (b2): bộ kiểm hồ sơ land + bộ kiểm nhãn HINT

tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-cong-cu-ho-so` |
| `packet_issue` | #752 |
| `revision` | 4 |
| `thay_the_cho` | **r3**: tệp `ops/specs/no-p3-cong-cu-ho-so-r3.md` (tên cũ; commit `6c2fe9b` `git mv` nó thành tệp này, 0 dòng đổi), chưa từng vào `master`. Bản cuối của r3 trên nền cũ `c522c17`: sha256 `17e1f9c9d91052e98b2c929cbb78a9acbb42edd6a37ba306110b59ea4905121c`, commit `3456ab163198ce1b23e72a4316ea452fcd22ac9e` (vá P3 lượt 5; byte không đổi tới `c3f6f5f`). Bản đo lại r3 trên nền `1d7e642`: commit `5fc00484f417a1d9824e9ac9a5dba23e1c941e96`, sha256 `409db36c21d760ce8d090eebe92093aa673b3227254c3b08edabaa47722b4716`, vẫn ghi `revision: 3` — đó là điểm xuất phát của r4, vì đổi nền là REVISION MỚI (quyết định chủ kho 23-10-2026, [comment trên Issue #752](https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792), mục 2). Không lease nào neo `spec_hash` của r3 trên cây đang soạn: `git grep -l -F no-p3-cong-cu-ho-so HEAD -- ops/leases` ra 0 tệp (13:53:50Z 23-10-2026; nhánh `ops/**` chưa quét — đo lúc cấp theo `depends_on` (2)). **r2**: `ops/specs/no-p3-cong-cu-ho-so-r2.md`, sha256 `ce39f1e164fd94e342af59a0624cec1fc23fc84574f0ec1e5c627a656a17593b`, commit `a9ef33c24665dedc70f2c839e2357353bd4054af` (vào `master` qua merge `207250f`, tổ tiên của `c522c17` và của nền mới `1d7e642`: `git merge-base --is-ancestor` rc 0, 12:56:05Z 23-10-2026). r1: sha256 `c3fd632282b822365ccd3656cc12f278b7a76a5c0c5484c516cd62033beb8f8a`, commit `55bd0d2`. Thứ định danh các bản là băm, không phải tên nhánh hay tên tệp (tên r3 đã đổi). r4 không sửa byte nào của r1/r2 (cả hai đóng băng, chỉ để lưu vết — nợ `SPEC-R2-751-752-KHONG-DUOC-CAP-LEASE`); lease và `spec_hash` từ nay neo r4. |
| review của r2 | (1) Lượt 2 review đặc tả, reviewer Claude Sonnet 5.5 (subagent `review-sonnet-max`, tự khai): `verdict: changes_requested`, `reviewed_sha` `a9ef33c24665dedc70f2c839e2357353bd4054af`, `spec_sha256` `ce39f1e1…`, lớp mới **0 P1 · 1 P2 · 3 P3 = 4 lớp**; sáu lớp lượt 1: 4 đã đóng, 2 đóng trừ chỗ hẹp (gộp vào lớp mới). `VERDICT.md` sha256 `893a1131bb278028e0c6c60dab7e154ebc16552531dbdfe8dc97fff090b052d8`; `HINT.patch` (6 hunk) sha256 `9bb50b59d5c1c34c4154e4ea7d1345cac7ba4218a17dcefe94c1d7c8512c2c3f`. Lúc soạn r3 hai tệp nằm ở thư mục tạm của phiên điều phối: `git grep` hai băm trên `c522c17` ra 0 kết quả (chưa có bản trong kho; lặp trên `1d7e642` 12:56:42Z 23-10-2026: vẫn 0 tệp mỗi băm); thứ định danh là băm. (2) Connector Codex, PR #762, `pull/762#discussion_r4286041896` (P2 "Apply the sensitive packet size ceiling", `created_at 2026-10-15T17:13:10Z`, dòng 17 của r2 tại commit `4c550bc`; đọc qua `gh api …/pulls/comments/4286041896` ~23:36Z 15-10-2026): r2 tự xếp `sensitive` vì sửa `.claude/dev/ci_dang_ky_test.py` mà lại áp trần thường; 5 tệp ~900 dòng vượt trần `sensitive` 3 tệp/300 dòng. Cách r3 đóng từng lớp: mục "Thay đổi so với r2". |
| `nguon_cap_viec` | Như r2: sổ nợ P3 mục 5 và 6, connector Codex trên PR #722 (mục 5: `pull/722#discussion_r4231959151`, dẫn ở `ops/reviews/README.md` dòng 657 (655 ở `a9ef33c`; README đổi bởi `874feab`, +12 dòng, là commit duy nhất chạm README trong `a9ef33c..c522c17`; đo 16-10-2026 bằng `git show <commit>:ops/reviews/README.md | grep -n 4231959151` trên `a9ef33c`, `c522c17`, `11134f2`; lặp trên `1d7e642` 12:56:42Z 23-10-2026: vẫn dòng 657, dù sáu commit chạm README trong `c522c17..1d7e642`); câu trích và mục 6 KHÔNG ĐO ĐƯỢC offline). Phạm vi (từ r3) do quyết định chủ kho 15-10-2026 **"tách 2 packet"** (chuyển tới qua phiên điều phối; ghi bằng chữ trong thân Issue #763 do `ducthangho` mở `2026-10-15T23:26:04Z`, đọc ~23:27Z): #752 còn đúng bốn tệp MỚI, việc đăng ký hai test vào sổ test sống chuyển sang packet #763 `no-p3-dang-ky-ci` (nay `ops/specs/no-p3-dang-ky-ci-r2.md`; lúc tách là r1). Bốn điểm của r4 do quyết định chủ kho 23-10-2026, neo [comment trên Issue #752](https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792) (mục "Thay đổi so với r3"). Thân Issue #752 (đọc qua `gh api` 13:58:28Z 23-10-2026: `open`, `updated_at 2026-10-23T13:54:01Z`, 1 comment — chính comment ấy) vẫn ghi "Review class: standard". |
| ngưỡng chặn | "Chỉ P1/P2 chặn merge" — giữ như r2; nguồn thẩm quyền riêng cho #752 chưa được ghi (KHÔNG ĐO ĐƯỢC offline). Tiền lệ, KHÔNG phải nguồn: comment #698 `6094652521` (bản đọc lại `ops/land/pr721-wp698-provenance/readback-comment-6094652521.json`) đặt "0 P1 / 0 P2. Lớp P3 trở xuống KHÔNG chặn" cho wp698, không nhắc #752. Với nhãn cổng `sensitive` (hàng dưới), PROTOCOL §8 dòng 626 @ `1d7e642` (621 @ `c522c17`) còn đòi quyết định có căn cứ cho từng finding còn mở. Hàng ấy nay tách hai luật theo `ADR-0054`; đặc tả này không khai dòng `luat_push_va_dung_va`, và ADR-0054 tự ghi "CHƯA KÍCH HOẠT" (dòng 3–5) ⇒ luật cũ áp: hết P0, có quyết định cho từng finding còn mở (đo 12:56Z 23-10-2026). |
| `review_class` | Quyết định chủ kho và thân Issue #752: **`standard`** (thân Issue #763 ghi `sensitive`: `ops/specs/no-p3-dang-ky-ci-r1.md` dòng 11 @ `11134f2`) — bản r3 đầu (`11134f2`) đọc chữ ấy là "packet thường, dưới trần thường ADR-0044" (r1 khai `standard` và ghi "dưới trần thường" ở hàng `kich_thuoc`; r2 khai `sensitive` và bác `standard`, câu ấy 0 lần — đo 16-10-2026 bằng `grep -c`); từ review lượt 3 của r3, đặc tả (r3 rồi r4) KHÔNG dùng cách đọc ấy làm dữ kiện về trần (cuối hàng). `standard` KHÔNG thuộc từ vựng PROTOCOL §3.2 dòng 156 (`routine`/`systemic`/`sensitive`); theo nội dung, bốn tệp mới chỉ đọc, là công cụ báo cáo và test, không đổi authority ⇒ khớp `routine` (PROTOCOL §8 dòng 739 @ `1d7e642`, 730 @ `c522c17`; dòng 156 không đổi giữa hai nền — đo 12:56Z 23-10-2026 bằng so khớp nguyên dòng). **Cổng ép `effective_review_class: sensitive`** — đo 23:35:43Z 15-10-2026, gọi thẳng hàm của `ops/lease_publish.py` @ `c522c17`: `_BANG_LOP` 7 mục, cả 7 `sensitive`, không mục nào khớp bốn đường dẫn ⇒ `_tinh_lop_tu_write_set` rơi về `sensitive`; lưới `_kiem_lop_review` (role `executor`, `schema_version: 2`) 4 giá trị khai × 4 giá trị hiệu lực: chỉ 4 ô `effective_review_class: sensitive` qua, 12 ô còn lại rc 10 (kể cả khai `standard`). Lặp 12:57:03Z 23-10-2026 @ `1d7e642` (tệp không đổi so với `c522c17`: `git diff --quiet` rc 0): y hệt — 7 mục, cả 7 `sensitive`, 0 mục khớp, 4 ô qua, 12 ô rc 10. Lease khai `review_class: routine` + `effective_review_class: sensitive`. Từ r3, đặc tả KHÔNG còn lý do "chạm CI authority" của r2 (bỏ `.claude/dev/ci_dang_ky_test.py`), nhưng lớp hiệu lực vẫn `sensitive` vì cổng `_BANG_LOP` ép (đo trên) ⇒ trần áp cho #752 là trần `sensitive` của `ADR-0053` (dòng 6: ≤ 6 tệp, ≤ 450 dòng thêm; ADR ấy thay đúng cặp số `sensitive` ≤ 3 tệp / ≤ 300 dòng thêm của ADR-0044 dòng 5), có hiệu lực nhờ dòng khai `tran_kich_thuoc_sensitive` ngay dưới tiêu đề (hàng `kich_thuoc`); vượt trần ấy thì phải có khối `nang_tran` do chủ kho nâng (ADR-0053 dòng 32–38) — r4 mang khối ấy (mục `nang_tran` ngay dưới bảng; điều kiện cấp lease `depends_on` (4)). Chữ `standard` của thân Issue không phải khối ấy: nó không nêu số trần nào. Nhãn cổng vẫn kéo theo PROTOCOL §8 dòng 732–734 @ `1d7e642` (724–726 @ `c522c17`; Codex `cross_approved` hoặc `human_audited`) trừ khi chủ kho override bằng quyết định có audit (dòng 729 @ `1d7e642`, 721 @ `c522c17`); r4 không tự hạ ([comment chủ kho 23-10-2026](https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792) không nhắc lớp review). |
| `executor` · `reviewer` | Claude (executor). Review thi hành: Codex `cross_approved` hoặc `human_audited` theo nhãn cổng `sensitive` (PROTOCOL §8 dòng 732–734 @ `1d7e642`; 724–726 @ `c522c17`), trừ khi chủ kho override có audit; lượt review subagent Claude Sonnet chỉ là `review_deferred` (dòng 617 @ `1d7e642`; 612 @ `c522c17`). Chỉ P1/P2 chặn merge. |
| `base` | **Nền đóng băng của r4: `1d7e642092fb3dda15967be44d095f37bb22ac5f`** (merge PR #885) — đổi nền là REVISION MỚI, r4 neo nền này; lúc cấp lease thực thi đo lại theo `depends_on` (3) (quyết định chủ kho 23-10-2026, [comment trên Issue #752](https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792), mục 2). `git ls-remote --heads origin` lúc 12:57:25Z 23-10-2026: `master` = `1d7e642…`, máy chủ 556 nhánh; lặp 13:34:38Z: vẫn `1d7e642…`, 561 nhánh. Lặp 13:55:03Z (`git ls-remote origin refs/heads/master`): `master` đã sang `8324567788caab8dc332d45df458ef415fd305be` (merge PR #891); `gh api repos/ducthangho/tra-luat/compare/1d7e642...8324567` (OID đủ 40 ký tự) lúc 13:55:15Z: `ahead`, 4 commit, 53 tệp, trong đó 2 hồ sơ `ops/land/*-land-evidence.yaml` mới và 1 `ops/reviews/**/*HINT.patch` mới (minh hoạ ở B3). Nền đóng băng KHÔNG theo `master`; số phụ thuộc nền đo lại lúc cấp (L5 của `soan-spec`). Nền cũ `c522c17` là tổ tiên: `c522c17..1d7e642` = 522 commit, 73 commit first-parent. Số đo nền chạy trên bản sao `c3f6f5f` (= `1d7e642` + ba tệp `ops/specs/*.md`, `git diff --stat 1d7e642 c3f6f5f` chỉ ba tệp ấy) hoặc trên cây `git archive 1d7e642`; bảng cũ → mới ở mục "Đo lại nền sau #748 land (nền 1d7e642)". **Nền lúc duyệt (lịch sử):** `c522c173cb58b506bac8cffb24239e16e8459836`; `ls-remote` 23:29:24Z 15-10-2026 thấy `master` đã sang `9fddb1d19e8e5b753bb687673846d484fb710182` (merge PR #755; `git diff --stat c522c17 9fddb1d` = 1 tệp `ops/specs/wp728-do-linux-doc-lap-wp710-r2.md`, +246/−0 dòng), số đo khi ấy lặp trên `9fddb1d` cho đầu ra y hệt. Lease phải đo lại trên `master` lúc cấp. |
| `depends_on` | **CHẶN cấp lease** cho tới khi ĐỦ bốn điều kiện, đo lại lúc cấp; số trong ô này không thay được phép đo lúc cấp. **(1) Đường land A — THOẢ MỘT PHẦN: quyết định trong phiên, chưa neo GitHub** (mục "Đường land" dưới bảng): chủ kho chọn A ("Tách, land cùng lúc") trong phiên điều phối `session_01CSM7GNazhN6uGJb4v1TqBT` ngày 2026-10-16. Đó là lời khai trong phiên, CHƯA phải neo GitHub: neo bền sẽ là comment cấp lease của chủ kho, phải nhắc lại đường A — đo lại lúc cấp (có comment ấy, nhắc A, thì mới coi (1) là đã neo). [Comment chủ kho 23-10-2026](https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792) KHÔNG nhắc đường A (đọc ngược 13:54:41Z) ⇒ (1) vẫn chưa neo. Lý do đường land vẫn quyết định B6: tách packet khiến #752 KHÔNG vào được `master` một mình mà cổng còn xanh (đo S1). **(2)** Trên một clone ĐỦ ref — so `git ls-remote --heads origin` với cả `refs/heads/*` lẫn `refs/remotes/origin/*` (bỏ `HEAD`) theo **cặp (tên, OID)**: thiếu 0, thừa 0, lệch OID 0; không chạy được ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp — `python ops/lease_publish.py ai-dang-giu <đường dẫn> --root <clone>` ra `NGƯỜI_GIỮ 0`, rc 0, cho từng đường dẫn của write set (CLI nhận một đường dẫn mỗi lần). rc 12 là trạng thái thứ ba, không phải "không ai giữ". **Hiện trạng 13:24:28Z–13:26:25Z 23-10-2026 (nền `1d7e642`)**: clone tạm, mọi nhánh fetch từ GitHub, đồng bộ lại NGAY TRƯỚC từng đường dẫn: máy chủ 561 nhánh, `refs/heads` 561, `refs/remotes/origin` 561; `comm -3` trên cặp (tên, OID) ra 0 dòng ở cả hai phía; `master` `1d7e642`; bốn đường dẫn ⇒ mỗi đường `NGƯỜI_GIỮ 0: không có`, rc 0, 0 dòng `HẾT_HẠN`, 0 dòng `CÒN_HẠN` (chưa lease nào từng giữ chúng). Hai lượt trước đó (12:59:50Z–13:01:29Z và 13:23:16Z–13:24:05Z) ra rc 12 `KHÔNG_XÁC_ĐỊNH: cache thiếu nhánh máy chủ` ở 1 rồi 3 trong 4 đường dẫn — nhánh mới (`ops/wp892-spec`, `agent/wp748-r24-claude`) được đẩy lên giữa lúc đồng bộ và lúc đo; đó là trạng thái thứ ba làm đúng việc, không phải "không ai giữ", và đo lúc cấp phải đồng bộ sát lệnh. (Lịch sử: 23:29:51Z–23:31:54Z 15-10-2026, 541 nhánh, HEAD `9fddb1d`, cùng kết quả.) **(3) #748 đã MERGE vào `master`** (không chỉ vào nhánh tích hợp của #748; cùng điều kiện (1) của `ops/specs/no-p3-dang-ky-ci-r1.md` @ `11134f2`, tệp nay là `ops/specs/no-p3-dang-ky-ci-r2.md`) — quyết định chủ kho (c): mọi packet P3-b chờ #748; #752 là P3-b. **Nghĩa của "chờ #748" do chủ kho chốt 23-10-2026** ([comment trên Issue #752](https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792), mục 1): #748 ĐÃ MERGE vào `master` là đủ, KHÔNG đòi `landed: true`. **Đo 13:26:45Z 23-10-2026: THOẢ** — bốn merge first-parent từ nhánh `agent/wp748-*` trong `c522c17..1d7e642` (PR #849 `9422054`, #862 `401d4f1`, #869 `7400df4`, #882 `8223fd2`); Issue #748 `closed`/`completed` từ 2026-10-20T01:19:38Z. Lúc cấp lease thực thi đo lại (mục 2 của comment): cả bốn merge ấy phải là tổ tiên của `base_sha` của lease. Dữ kiện kèm theo, nay KHÔNG còn là điều kiện: cả bốn hồ sơ land của #748 trên `1d7e642` mang `trang_thai_packet.landed: false`; và chủ kho đã cấp lát `wp748-r24` dưới Issue #748 (`issues/748#issuecomment-6365380273`, `ducthangho`, `OWNER`, 12:55:59Z 23-10-2026; lease `wp748-r24-g24-claude-remote-20261023` đăng 13:16:51Z, `base_sha` `1d7e642…`, `lease_until 2026-10-24T01:10:11Z`) — write set 18 hồ sơ `ops/land/*-land-evidence.yaml`, giao write set #752 = ∅, là ĐẦU VÀO ĐỌC của B3 nhưng không chặn cấp lease vì B3 nay là vị từ (13:55:03Z: nhánh `agent/wp748-r24-claude` ở `77ec458`; `gh api repos/ducthangho/tra-luat/compare/77ec458...8324567` (OID đủ 40 ký tự) lúc 13:55:15Z ra `diverged`, `master` thiếu 2 commit của nhánh ⇒ lát ấy chưa vào `master`). Lịch sử: bản r3 đầu (`11134f2`) bỏ điều kiện chờ #748 bằng phép đo write set; review lượt 3 bác, r3 khôi phục; r4 giữ điều kiện với nghĩa chủ kho đã chốt. Thông tin phụ (đo 15-10-2026, lịch sử), KHÔNG thay được quyết định: write set r3 giao write set #748 = ∅ (không xung đột ghi), với cả 8 đường dẫn "Candidate write set" trong thân Issue #748 (`gh api repos/ducthangho/tra-luat/issues/748 --jq .body`, đọc 23:27:59Z; Issue `open`, `updated_at 2026-10-15T16:36:42Z`) lẫn 11 đường dẫn của lease còn hạn `wp748-r11-g11-claude-windows-20261015` (nhánh `ops/wp748-r11-g11-lease` @ `181e3fb`, `lease_until 2026-10-16T04:27:21Z`). Ngoài ra còn ràng buộc ĐỌC: B6(a) đo một tệp #748 đang giữ (`.claude/dev/ci_dang_ky_test.py`; nhánh `agent/wp748-g9-claude` @ `0daeb47` đổi nó +65/−9 dòng so với merge-base với `c522c17`, đo 23:35:49Z) ⇒ đo lại B6(a) sau khi #748 land — đã đo lại 13:30:29Z 23-10-2026 trên `1d7e642` (B6 a: `26/24`). Anh em #751: write set r2 của #751 (3 đường dẫn, `ops/specs/no-p3-lease-spec-hash-r2.md` dòng 14) giao write set #752 (r3, giữ nguyên ở r4) = ∅ (đo ~23:37Z 15-10-2026); r3 của #751 (`ops/specs/no-p3-lease-spec-hash-r3.md` dòng 15 @ `c3f6f5f`) giữ nguyên ba đường dẫn ấy ⇒ vẫn ∅ (đo 13:31:48Z 23-10-2026); r4 của #751 (`ops/specs/no-p3-lease-spec-hash-r4.md` dòng 15 @ `6c2fe9b`, chưa vào `master`) vẫn đúng ba đường dẫn `ops/lease_publish.py` · `ops/lease_publish_spec_hash_test.py` · `.claude/dev/ci_dang_ky_test.py` ⇒ vẫn ∅ (đo 13:55:03Z 23-10-2026 bằng `git show HEAD:<tệp> | grep -n`; tệp ấy đang được vá song song nên đo lại lúc cấp); phần dính sổ test sống chuyển sang #763. **(4) Trần: khối `nang_tran` của r4 (mục ngay dưới bảng) — quyết định đã có, neo [comment trên Issue #752](https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792).** Vì cổng `_BANG_LOP` ép lớp hiệu lực `sensitive` (hàng `review_class`) và đặc tả mang dòng khai `tran_kich_thuoc_sensitive` (hàng `kich_thuoc`), trần gốc của #752 là ADR-0053: ≤ 6 tệp VÀ ≤ 450 dòng thêm. #752 nằm trong vế tệp (4 ≤ 6) nhưng theo ước vượt vế dòng (khoảng 950 > 450; hàng `kich_thuoc`) ⇒ chủ kho nâng bằng khối `nang_tran` đủ bốn trường của ADR-0053 dòng 34–38 (`ai_nang`, `can_cu`, `tran_cu`, `tran_moi`) cộng trường `neo`; trần áp cho #752 là `tran_moi`: **≤ 4 tệp / ≤ 1.000 dòng thêm**, đo bằng `git diff --numstat` base..head — vế dòng nâng 450 → 1.000, vế tệp siết 6 → 4 (bằng write set). Lúc cấp, ĐỦ ba vế mới cấp: (a) lease CHÉP NGUYÊN khối, cả trường `neo`; (b) người cấp đọc ngược comment neo và thấy nó còn đó, tác giả `ducthangho` với `author_association` `OWNER`, bốn trường khớp từng số với khối; (c) comment cấp lease vẫn neo `lease_id` và `spec_sha256` của r4. Thiếu hoặc lệch một vế ⇒ không cấp. Numstat thật (đo trước review) vượt `tran_moi` ở bất kỳ vế nào ⇒ dừng TRƯỚC review và soạn revision, không tự nới. Khối không phải lời khai cổng đã canh: ADR-0053 có **0 cổng** (PROTOCOL §20) và hàng `kich_thuoc` đo lại đủ sáu vị trí cổng ⇒ người cấp và reviewer đo `numstat` bằng tay. Tiền lệ dạng khối theo ADR-0053: `issues/748#issuecomment-6365380273` (`ducthangho`, `OWNER`, 12:55:59Z 23-10-2026: `tran_cu` ≤ 6 tệp / ≤ 450 dòng thêm, `tran_moi` ≤ 18 tệp / ≤ 450 dòng thêm). Tiền lệ trước ADR-0053: `issues/750#issuecomment-6190095083` (`ducthangho`, `OWNER`, `2026-10-15T10:36:49Z`) — "Tôi chấp nhận ngoại lệ trần ADR-0044 cho packet này: tối đa 10 tệp và 500 dòng thêm (thay cho 3 tệp / 300 dòng của packet sensitive)"; bản đọc lại `ops/land/pr759-no-p3-ho-so-provenance/readback-comment-6190095083.json` (đọc 16-10-2026). Lịch sử: r3 chỉ ĐỀ XUẤT 4 tệp / 1.000 dòng thêm và chưa mang khối vì chưa có quyết định để điền `ai_nang`, `can_cu`; lối thu gọn dưới 450 dòng thêm (bản tham chiếu gọn nhất của reviewer lượt 3: 4 tệp, ~350 dòng) chủ kho ghi là "có thể nhưng không bắt buộc". |
| `write_set` | `ops/kiem_ho_so_land.py` (MỚI) · `ops/kiem_ho_so_land_test.py` (MỚI) · `ops/kiem_nhan_hint.py` (MỚI) · `ops/kiem_nhan_hint_test.py` (MỚI). `.claude/dev/ci_dang_ky_test.py` của r2 RA KHỎI write set (quyết định chủ kho 15-10); việc đăng ký thuộc #763. |
| `kich_thuoc` | 4 tệp MỚI, 0 tệp sửa. Ước khoảng 950 dòng thêm, 0 dòng xoá (đơn vị: dòng theo `git diff --numstat`) = 700 (ước r1 cho bốn tệp) + khoảng 200 (ca r2 thêm vào B1, B1b, B4, B7) + khoảng 50 (ca r3 thêm: một URL nhúng tiền tố, bốn ca biên, hai ca B1b, hai vế đầu ra chữ ở B3/B5) — là ƯỚC, không phải đo; đo lại trước review. Mốc đo được để đối chiếu: bản tham chiếu của reviewer lượt 2 (ngoài kho, `wc -l` ~23:37Z): hai công cụ 127 + 46 dòng, ba harness 159 + 64 + 61 dòng, tổng 457 dòng. **Trần áp dụng: trần `sensitive` ADR-0053 dòng 6 (≤ 6 tệp VÀ ≤ 450 dòng thêm)**, vì cổng `_BANG_LOP` ép lớp hiệu lực `sensitive` (hàng `review_class`); trần ấy có hiệu lực qua dòng khai `tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab` ngay dưới tiêu đề — đúng một dòng khớp mẫu ở ADR-0053 dòng 52, và OID ấy (merge PR #791) qua cả ba phép đo dòng 54–56 lúc 13:34:38Z 23-10-2026 trên clone không shallow vừa fetch: `git cat-file -e <OID>:docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md` rc 0, cùng lệnh trên `<OID>^1` rc 128, và OID nằm trên `git rev-list --first-parent origin/master` (`origin/master` = `1d7e642`). Thiếu hoặc hỏng dòng khai ⇒ trần cũ ADR-0044 dòng 5 (≤ 3 tệp / ≤ 300 dòng thêm), fail-closed. Vượt trần ADR-0053 (theo ước, vế dòng) ⇒ r4 mang khối `nang_tran` do chủ kho nâng (mục ngay dưới bảng; `depends_on` (4)): **trần áp cho #752 là ≤ 4 tệp / ≤ 1.000 dòng thêm** (`git diff --numstat` base..head). r4 KHÔNG khai "trần thường" (ADR-0044 dòng 6: ≤ 6 tệp VÀ ≤ 1.000 dòng thêm cộng xoá) như dữ kiện. Dưới trần ADR-0053: 4 tệp ≤ 6 (đạt vế tệp) nhưng ước khoảng 950 > 450 (vượt vế dòng); bản tham chiếu gọn nhất của reviewer lượt 3 (ngoài kho), 4 tệp, 350 dòng, thì nằm TRONG trần ấy — dưới trần ADR-0044 cũ nó vượt vế tệp, nên câu "#752 không thi hành được dưới trần ấy nếu không có ngoại lệ" của bản trước không còn đúng. Khối `nang_tran` (quyết định chủ kho 23-10-2026) 4 tệp / 1.000 dòng thêm: dư 0 tệp, dư khoảng 50 dòng theo ước — sát trần; trần là trần, không phải mục tiêu (`can_cu` của khối). Finding Codex `r4286041896` nhắm đúng chỗ này: bỏ sổ CI khỏi write set giảm vế tệp 5 → 4, không giảm vế dòng (r2 khoảng 900, r3 khoảng 950). Kho có tiền lệ cả hai chiều (đo ~01:40Z 16-10-2026 trên `11134f2`): `ops/specs/wp726-nlm-script-phan-quyet-canary-r1.md` dòng 20–22 (`sensitive` KHÔNG chạm authority ⇒ trần thường, "Chủ kho bác cách xếp này thì tách tiếp") · `ops/specs/N5-LENH-HOOK-WINDOWS.md` dòng 32–37 và ba lease 29–30-08-2026 (`ops/leases/khong-do-duoc-phai-do-exec-1-claude-20260829.yaml` dòng 33–41, `…-exec-1r2-claude-20260829.yaml` dòng 31–35, `n5-lenh-hook-windows-exec-1-claude-20260830.yaml` dòng 24–28: lớp `sensitive` chỉ do mặc định fail-closed, "Vẫn áp trần ≤3 tệp / ≤300 dòng thêm") · `ops/specs/no-p3-ho-so-r2.md` dòng 15 và comment `issues/750#issuecomment-6190095083` cho packet anh em #750 (ngoại lệ 10 tệp, 500 dòng thêm). Từ r3, đặc tả đi chiều chặt cộng nâng trần đích danh (dưới ADR-0053 là khối `nang_tran`) — đúng cách chủ kho đã xử #750, và r4 mang khối ấy theo quyết định chủ kho; chiều thường của wp726 có mã đã vào kho, nhưng việc chủ kho chấp nhận cách xếp ấy KHÔNG ĐO ĐƯỢC (review lượt 3, E5). Numstat thật vượt `tran_moi` (≤ 4 tệp / ≤ 1.000 dòng thêm) ở vế nào ⇒ dừng TRƯỚC review và soạn revision (không tự nới). Sáu tệp tiền lệ ấy, cùng `ops/specs/no-p3-lease-spec-hash-r2.md` của `depends_on`, không đổi tới `1d7e642` (`git diff --quiet 11134f2 1d7e642 -- <bảy tệp>` rc 0, 13:31:48Z 23-10-2026). Không cổng nào cưỡng chế trần — đo đủ SÁU vị trí cổng mà PROTOCOL §20 liệt kê ở mục "Cột cổng đã ĐO" (L6 e của `soan-spec`; r3 chỉ đo hai), lệnh `git show 1d7e642:<tệp> | grep -c -F -- <chuỗi>` cho bảy chuỗi `numstat` `ADR-0044` `ADR-0053` `nang_tran` `ai_nang` `tran_cu` `tran_moi`, 13:53:50Z 23-10-2026: `ops/lease_publish.py` · `.claude/dev/launcher.py` · `.claude/dev/gate_lifecycle.py` · `.github/workflows/ci.yml` · `.github/workflows/ops-publish-lease.yml` ra 0 với cả bảy chuỗi, từng tệp; `.claude/dev/packet_loop.py` ra 0 với ba chuỗi đầu, còn `nang_tran` 10 · `ai_nang` 4 · `tran_cu` 2 · `tran_moi` 5 — tất cả thuộc lệnh `nang-tran` (`cmd_nang_tran`) cho hai trục `vong_review` và `codex_review_calls` (`TRUC_TRAN` dòng 60–61), không có trục kích thước; sáu tệp không đổi giữa `1d7e642` và HEAD `6c2fe9b` (`git diff --quiet` rc 0). Đếm chuỗi là PROXY theo §20: 0 lần nhắc ở năm tệp là bằng chứng mạnh rằng chúng không đọc trần; các lần nhắc ở `packet_loop.py` không tự chứng minh nó canh kích thước — đọc `TRUC_TRAN` mới thấy không có trục ấy (lịch sử: `numstat`, `ADR-0044` trên hai tệp @ `c522c17` ra 0 cả bốn lần, 23:36:35Z 15-10-2026; bốn chuỗi trên hai tệp @ `1d7e642`, 12:57:08Z 23-10-2026, cùng kết quả) ⇒ người giữ đo. |

## `nang_tran` (ADR-0053) — lease chép NGUYÊN khối này

Quyết định chủ kho 23-10-2026, neo [comment trên Issue #752](https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792).
Đọc ngược bằng `gh api repos/ducthangho/tra-luat/issues/comments/6366519792` lúc 13:54:41Z 23-10-2026: tác giả
`ducthangho`, `author_association` `OWNER`, `created_at` = `updated_at` = `2026-10-23T13:54:01Z`, thân sha256
`0d600444084bc691a8c49dc41e52f781c8e1f2ffe45510c387a0e689bc1b7d57` (băm chuỗi `body` UTF-8 không thêm LF cuối;
`gh api … --jq .body | sha256sum` thêm LF nên ra `a19cd1f799649e326222c277e3f886040b7c1be9383441868acb3b0ef0e2a766`,
số mà #763 r2 ghi; đo 15:40Z 23-10-2026). So với bản nháp phiên điều phối giao cho lượt
soạn này: mọi con số trùng theo thứ tự (chỉ thêm dấu chấm của danh sách đánh số); khác định dạng — bản đăng viết "Kèm ba quyết định cùng đợt" thành danh
sách đánh số, bản nháp viết "hai" rồi liệt kê ba. Thứ có thẩm quyền là comment đã đăng, không phải bản nháp.

```yaml
nang_tran:
  ai_nang: ducthangho (chủ kho, thẩm quyền §2 protocol)
  can_cu: >-
    hai công cụ mới + hai bộ test tự đứng, ước ~950 dòng thêm trong 4 tệp; tách tiếp sẽ tách
    công cụ khỏi phản chứng của chính nó. Bản tham chiếu gọn nhất của reviewer (4 tệp / ~350
    dòng) cho thấy nằm dưới 450 là có thể nhưng không bắt buộc; trần mới là trần, không phải
    mục tiêu.
  tran_cu: ≤ 6 tệp / ≤ 450 dòng thêm (ADR-0053)
  tran_moi: ≤ 4 tệp / ≤ 1.000 dòng thêm, đo bằng `git diff --numstat` base..head
  neo: https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792
```

Khối parse được bằng `yaml.safe_load` (đo trước khi đóng băng, xem "Thay đổi so với r3"). Bốn trường đầu chép NGUYÊN VĂN
từ thân comment đã đăng (đổi gạch đầu dòng thành khoá YAML, gấp cột `can_cu`, và xếp `can_cu` lên trước `tran_cu` theo thứ tự
ADR-0053 dòng 34–38; so từng trường sau `yaml.safe_load`: 4/4 trường bằng nhau từng ký tự, đo 17:14Z 23-10-2026); `neo` là trường duy nhất khối có mà
comment không có. Ước ~950 là ƯỚC, chưa phải numstat (mã chưa có): số hạng 700 + ~200 + ~50 ở hàng `kich_thuoc`, không
nằm trong khối vì comment không có; numstat thật đo trước review bằng `git diff --numstat` base..head. Không cổng nào
đọc khối này (hàng `kich_thuoc`): người cấp lease và reviewer đo `git diff --numstat` bằng tay và so với `tran_moi`.

## Đường land — chủ kho chọn A (điều kiện (1) của `depends_on`)

Nguồn quyết định: câu trả lời của chủ kho trong phiên điều phối `session_01CSM7GNazhN6uGJb4v1TqBT` ngày 2026-10-16, lựa chọn "Tách, land cùng lúc" (lời khai trong phiên, chưa phải neo GitHub; neo bền sẽ là comment cấp lease của chủ kho, phải nhắc lại đường A).

Sổ test sống `.claude/dev/ci_dang_ky_test.py` coi MỌI `ops/*_test.py` mức đỉnh là test sống (`tim()`, dòng 104 @
`1d7e642`, 83 @ `c522c17`; nay bỏ qua tệp Git-ignore mà không tracked qua `_git_bo_qua`, dòng 85 — bốn tệp mới không bị
ignore, S1 dưới đây đếm cả hai test) và `kiem()` (dòng 643–645 @ `1d7e642`, 582–584 @ `c522c17`) đỏ cả hai chiều: test
sống chưa đăng ký, và mục đăng ký không có tệp. Bước `test registry` của job `gate-registry` (`.github/workflows/ci.yml`
dòng 1000–1008 @ `1d7e642`, 889–895 @ `c522c17`) chạy sổ ấy với `--chay` ở MỌI sự kiện, không có `if:` theo `che_do` (job
chỉ có `if:` chống huỷ ở dòng 950), và `pull_request:` (dòng 13) không lọc nhánh đích. Đo 13:30:22Z–13:30:37Z
23-10-2026 trên bản sao `c3f6f5f` (= `1d7e642` + ba tệp đặc tả; bốn tệp giả: hai công cụ rỗng, hai test in `1/1`; hai mục
`MOI` chép nguyên dòng 53 rồi chỉ thay khoá, chèn ngay sau nó; lệnh `python3 -B .claude/dev/ci_dang_ky_test.py`, không
`--chay`, từ gốc bản sao; Python 3.11.15, git 2.43.0):

| trạng thái | ứng với | kết quả |
|---|---|---|
| S0 nền | `master` hôm nay | rc 0, `ĐĂNG KÝ: 24/24`, `PHẢN CHỨNG: 1064/1064 đỏ đúng`, `TỔNG: ĐẠT` |
| S1 bốn tệp, không đăng ký | #752 vào `master` một mình | rc 1, đúng hai dòng `ĐỎ: test sống chưa đăng ký: …`, `ĐĂNG KÝ: 26/24`, `TỔNG: ĐỎ` |
| S2 bốn tệp + hai mục `MOI` | #752 và #763 cùng lúc | rc 0, 0 dòng `ĐỎ:`, `ĐĂNG KÝ: 26/26`, `PHẢN CHỨNG: 1064/1064 đỏ đúng`, `TỔNG: ĐẠT`; numstat sổ `2 0` |
| S3 hai mục `MOI`, không có test | #763 vào trước #752 | rc 1, đúng hai dòng `ĐỎ: mục đăng ký không có tệp: …`, `ĐĂNG KÝ: 24/26`, `TỔNG: ĐỎ` |

Lịch sử, nền `c522c17` (23:33:41Z–23:33:57Z 15-10-2026; lặp trên `9fddb1d` y hệt): S0 `23/23`, S1 `25/23`, S2 `25/25`,
S3 `23/25`, `PHẢN CHỨNG: 1025/1025` — cùng rc, cùng số dòng `ĐỎ:`, chỉ số hạng trôi. Đơn vị của `ĐĂNG KÝ: a/b`: a = tệp
test sống trên cây, b = mục trong sổ; `PHẢN CHỨNG: n/n`: ca phản chứng. Chỉ S2 xanh, nên thứ tự #752 trước #763 (câu mà `ops/specs/no-p3-dang-ky-ci-r2.md` dòng 16 @ `6c2fe9b` trích từ thân Issue #763;
thân hiện tại, sửa lần cuối 2026-10-16T01:13:45Z, KHÔNG còn câu ấy — `#752 land trước` 0 lần và `#752 phải land trước` 0 lần, đo 17:02Z 23-10-2026 —,
thân cũ KHÔNG ĐO ĐƯỢC lại), nếu hiểu là merge vào `master`, làm
`gate-registry` VÀ `gate-ops (ubuntu-latest)` của `master` đỏ giữa hai lần merge (cùng một nguyên nhân, B6 d).
Hai đường giữ được `master` xanh:

- **A (giữ quyết định tách — ĐÃ CHỌN):** #752 và #763 vẫn là hai packet, hai lease, hai lượt review, hai trần
  kích thước tính riêng (cả hai `sensitive` theo cổng; trần của #752 là khối `nang_tran` ≤ 4 tệp / ≤ 1.000 dòng thêm, `depends_on` (4)). Lease #752
  chỉ cấp sau khi #748 đã merge vào `master` (`depends_on` (3)), nên head của #752 dựng trên `master` sau #748. #763 dựng trên head ĐÃ DUYỆT (exact SHA) của #752 (hoặc một nhánh tích hợp đã chứa nó; PROTOCOL §5
  dòng 351–355 @ `1d7e642`, 347–351 @ `c522c17`: packet vào integration, mỗi mission một draft land PR). `master` nhận cả hai trong MỘT lần merge —
  PR của #763 chứa cả #752 — sau khi #748 merge. Hệ quả: head riêng của #752 có `gate-registry` ĐỎ đúng hai dòng và `gate-ops` ĐỎ ở ca
  `k01` (B6 a, d) — cùng một nguyên nhân, đỏ có kiểm soát; "required gate xanh trên exact head" (PROTOCOL §5.1 dòng 359 @ `1d7e642`, 355 @ `c522c17`) được đo trên head gộp,
  không trên head #752.
- **B (bỏ tách): không chọn** — gộp lại một packet phải xin ngoại lệ trần `sensitive` (lối thứ hai của finding `r4286041896`).
- **Loại:** merge #752 vào `master` rồi mới tới #763 (đỏ S1 trên `master`); #763 trước (đỏ S3); đổi tên hai tệp test
  để `tim()` bỏ qua — tên do quyết định chủ kho chốt, và mục `MOI` chỉ nhận đường dẫn là test sống (S3), nên đổi tên
  thì #763 không còn gì để đăng ký.

## Thay đổi so với r3

Căn cứ: quyết định chủ kho 23-10-2026, [comment trên Issue #752](https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792)
(đọc ngược 13:54:41Z; mục `nang_tran` ở trên). r4 xuất phát từ bản đo lại nền của r3 (`5fc0048`, sha256 `409db36c…`);
phần chênh giữa bản r3 cuối trên nền cũ (`3456ab1`, sha256 `17e1f9c9…`) và `5fc0048` là lượt đo lại nền, ghi ở mục
"Đo lại nền sau #748 land". Bảng dưới chỉ ghi chỗ r4 đổi so với `5fc0048`.

| chỗ | r3 (`5fc0048`) | r4 | căn cứ |
|---|---|---|---|
| tiêu đề, `revision`, tên tệp | r3, `revision: 3`, `no-p3-cong-cu-ho-so-r3.md` | r4, `revision: 4`, tệp này (`git mv` ở `6c2fe9b`, 0 dòng đổi) | comment mục 2: đổi nền là revision mới |
| `thay_the_cho` | r2, r1 | thêm r3 với hai băm (bản cuối trên nền cũ, bản đo lại trên nền mới); lease và `spec_hash` neo r4 | như trên |
| `base` | "nền hiện hành" `1d7e642` | nền ĐÓNG BĂNG `1d7e642`; ghi `master` đã sang `8324567` (13:55:03Z); số phụ thuộc nền đo lại lúc cấp | comment mục 2 |
| `depends_on` (3) | "#748 land vào `master`", hồ sơ `landed: false` để ngỏ cho chủ kho | #748 ĐÃ MERGE là đủ, không đòi `landed: true`; THOẢ (đo 13:26:45Z); lúc cấp đo lại: bốn merge là tổ tiên của `base_sha` | comment mục 1 |
| `depends_on` (4), mục `nang_tran` mới, `review_class`, `kich_thuoc`, "Đường land" A | đề xuất 4 tệp / 1.000 dòng thêm, chưa có khối | khối đủ bốn trường cộng `neo`; trần áp cho #752 là `tran_moi` ≤ 4 tệp / ≤ 1.000 dòng thêm; ba vế khi cấp (chép khối, đọc ngược comment, neo `lease_id`/`spec_sha256`) | comment phần `nang_tran`; ADR-0053 dòng 32–38 |
| B3 | số cứng `13/14 DAT` + `1 MIEN_TRU`, rc 0 — không đạt được trên `1d7e642` | vị từ trên `S`/`E`/`F` tại `base_sha` của lease, bốn vế (i)–(iv); `F` là finding dữ liệu: báo, ghi nợ, không sửa; đột biến công cụ cộng ca đỏ thật trên cây `1d7e642`; vế "gỡ miễn trừ" rời B3 (răng chuyển sang hai ghim ở ca đỏ thật và B2 không tiêm) | comment mục 3 — chỉ câu "Tiêu chí B3 của #752 viết theo vị từ trên tập hồ sơ land lúc cấp lease, không theo số cứng."; S/E/F, báo-không-sửa và ca đỏ thật là thiết kế của đặc tả, chủ kho xác nhận khi cấp lease |
| Mục tiêu 1 và 3, B3 (iii), B5 | "đầu ra chữ chứa chuỗi glob" | glob phải là một token riêng; thêm đột biến "glob dính hậu tố" | L6 (b), soát dưới |
| `kich_thuoc`, lời khai "không cổng nào cưỡng chế trần" | đo hai tệp, bốn chuỗi | đo đủ sáu vị trí cổng của PROTOCOL §20, bảy chuỗi | L6 (e) |
| trích chéo | #763 `no-p3-dang-ky-ci-r1.md`, #751 `no-p3-lease-spec-hash-r3.md` | `no-p3-dang-ky-ci-r2.md`, `no-p3-lease-spec-hash-r4.md`; trích dẫn neo commit (`@ 11134f2`, `@ c3f6f5f`) và các mục lịch sử giữ nguyên | comment mục 2 |
| "Ngoài phạm vi", "Chưa đo được", "Đổi Ý NGHĨA" | — | thêm hồ sơ `F` và dạng miễn trừ khai trong dữ liệu; cập nhật theo quyết định | — |

Khối `nang_tran` (khối `yaml` có rào duy nhất trong tệp) nạp bằng `yaml.safe_load` lúc 14:05:00Z 23-10-2026: một khoá
`nang_tran`, năm trường `ai_nang` `can_cu` `tran_cu` `tran_moi` `neo`; các cụm `≤ 6 tệp / ≤ 450`, `≤ 4 tệp / ≤ 1.000`,
`~950`, `4 tệp / ~350` có nguyên văn trong thân comment đã đăng (bản đọc ngược 13:54:41Z).

**Soát L6** (`.claude/skills/soan-spec/SKILL.md` dòng 84–125, tệp không đổi giữa `1d7e642` và HEAD `6c2fe9b`) cho mọi
tiêu chí khớp chuỗi:

- **B3 (iii)/(iv) và B5 (glob ở đầu ra):** (a) vế dương là token glob trên đầu ra của công cụ MỚI; trên nền công cụ chưa
  có nên ra đúng màu "chưa làm" — đo 13:58:28Z 23-10-2026 trên worktree đặc tả: `python3 -B ops/kiem_ho_so_land.py --root .`
  và `python3 -B ops/kiem_nhan_hint.py --root . --json` cùng rc 2, `can't open file`; vế âm là đột biến bỏ dòng in.
  (b) đây là đầu ra chương trình, không bị ngắt cột như Markdown, và glob không chứa khoảng trắng; nhưng r3 khớp CHUỖI
  CON nên glob dính hậu tố vẫn xanh — r4 đòi bằng nguyên token, đột biến đổi hậu tố làm ĐỎ. (c) mỗi công cụ một vị trí,
  đo riêng. (d) không áp dụng: chuỗi cố định, không có dạng chữ hay chữ số để lọt.
- **B4 (nhãn L-5):** (b) công cụ khớp NGUYÊN VĂN trên nội dung thô, không nối dòng — đúng L-5 (PROTOCOL đòi nhãn nguyên
  văn). Đo 13:54:38Z 23-10-2026 trên `1d7e642` bằng phép đo độc lập: số tệp chứa nhãn trên nội dung thô, sau khi gộp mọi
  khoảng trắng, và sau khi bỏ ký tự tiền tố dòng diff (cộng, trừ, dấu cách) rồi gộp, đều là 26 ⇒ không tệp HINT nào có
  nhãn bị ngắt dòng, cách khớp thô không mù trên dữ liệu hiện có. Đột biến đổi hậu tố đã có sẵn (chuỗi cụt bỏ
  ` commit`). (a) như B3; (c) đếm theo từng tệp; (d) không áp dụng.
- **B6 (a) (đếm dòng `ĐỎ:`):** (c) đếm theo từng vị trí — mỗi dòng phải nêu đúng một trong hai tệp test; (b) và (d)
  không áp dụng (đầu ra chương trình, định dạng cố định).
- **B6 (c) (dòng `N/N`):** mẫu của sổ ở dòng 53 @ `1d7e642` khớp TRỌN dòng (neo đầu và cuối dòng, cờ nhiều dòng), chỉ
  chữ số, và hàm đọc (`bang_chung_xanh`, dòng 677–678) lấy dòng khớp ĐẦU TIÊN — tiêu chí đã đếm số dòng khớp thay vì tin
  dòng đầu; (d) không áp dụng.
- **`kich_thuoc`, "không cổng nào cưỡng chế trần":** (e) đo đủ sáu vị trí (hàng `kich_thuoc`); r3 chỉ đo hai.
- **B2 (đếm dòng `MIEN_TRU`) và B3 (i) (`ly_do` chứa tên khoá):** (a) vế dương: ca A có đúng một dòng trạng thái `MIEN_TRU`, mỗi
  tệp `F` có tên khoá trượt trong `ly_do`; vế âm: đột biến gỡ mục hoặc lý do rỗng (B2), `ly_do` rỗng / sai khoá / luôn nêu cả hai
  khoá (B3). (b) đầu ra chương trình, không bị ngắt cột. (c) đếm theo VỊ TRÍ: dòng `MIEN_TRU` của B2 là dòng của MỘT tệp (cột trạng
  thái), không phải mọi dòng chứa chữ ấy — mục tiêu 1 buộc in tổng và số `MIEN_TRU`, nên một cài đặt đúng chữ có thể in thêm một
  dòng tổng kết chứa chữ ấy (đo 17:13Z 23-10-2026 trên bản tham chiếu: `grep -c MIEN_TRU` ra 2 còn đếm theo cột trạng thái ra 1;
  đổi nhãn tổng kết sang `n_mien_tru` thì ra 1 và 1); `ly_do` kiểm theo từng tệp `F` và theo CẢ HAI chiều (chứa tên khoá trượt,
  không chứa tên khoá đạt); hai tên khoá không là chuỗi con của nhau. (d) không áp dụng.
- Ngoài hai tiêu chí trên, không tiêu chí nào của r4 khớp chuỗi trên TÀI LIỆU kho; tất cả đo đầu ra công cụ hoặc dữ liệu YAML.

## Thay đổi so với r2

Soạn r3 theo thứ tự: (1) chép r2 ra bản nháp ngoài kho, đổi tên tệp đích trong `HINT.patch` lượt 2 bằng `sed`, rồi
`patch -p0 --fuzz=0` — rc 0, 6/6 hunk, không `.rej`, bản sau vá 223 dòng (khớp số reviewer ghi ở L2); (2) đo lại mọi
con số trên `c522c17` (và lặp trên `9fddb1d`), giờ đo ghi tại chỗ; (3) viết lại các phần mà việc tách packet đổi.

| lớp (hạng, nguồn) | r3 sửa ở đâu |
|---|---|
| `l6-url-gia-dang-khong-giet-in-cung-tien-to` (P2, lượt 2) | B1: thêm ca URL nhúng nguyên tiền tố của L-6 sau một tiền tố lạ, giữ ca giả dạng cũ; dòng đột biến `in` sửa thành "`in` với CHÍNH chuỗi tiền tố ⇒ ca nhúng". Đo lại 23:39:56Z–23:39:57Z (V3, mục B1c). |
| `b1-b1b-b4-gia-tri-ca-va-ca-bien-chua-chot` (P3, lượt 2) | B1c mới, chốt giá trị ca (số 40 chữ số, lồng cả hai khoá, mồi cụt đủ nhãn trừ ` commit`, ca PyYAML có tiêm `{}`), nới regex ⇒ BA ca, bốn ca biên (SHA 41, SHA 64, repo anh em, `landed: 1`), cây trộn cho thứ tự rc, ca thẻ python cho `safe_load`. |
| `glob-in-ra-chi-do-o-khoa-json` (P3, lượt 2) | Mục tiêu 1 và 3 chốt dòng in glob ở đầu ra chữ; B3 và B5 thêm vế "bỏ dòng in glob ở đầu ra chữ ⇒ ĐỎ". |
| `depends-on-anh-em-751-va-so-hoc-kich-thuoc` (P3, lượt 2) | (a) #751: sau tách, write set r3 giao #751 = ∅ (đo) ⇒ quan hệ anh em chuyển sang spec #763; (b) `depends_on` (2) so cặp (tên, OID); (c) `kich_thuoc` số hạng cộng khớp tổng (700 + 200 + 50 = 950); (d) grep trần có giờ đo; (e) `+65/−9` có đơn vị "dòng". |
| Codex P2 `r4286041896` (PR #762) | Tách: `.claude/dev/ci_dang_ky_test.py` và mục tiêu 5 của r2 sang #763; `review_class`, `kich_thuoc`, `executor` · `reviewer` viết lại; B6 viết lại. Phần #752 của finding còn mở sau tách (review lượt 3, lớp P2): đóng bằng điều kiện cấp lease `depends_on` (4) — trần `sensitive` trừ ngoại lệ đích danh. |
| Nợ `SPEC-R2-751-752-KHONG-DUOC-CAP-LEASE` (`ops/land/pr759-no-p3-ho-so-land-evidence.yaml` dòng 407, `trang_thai: mo`) | Phần #752 của nợ được r3 xử lý bằng CẢ HAI lối mà nợ nêu: tách packet, và ngoại lệ trần do chủ kho duyệt (`depends_on` (4), bắt buộc trước khi cấp lease); phần #751 không thuộc r3. r3 không sửa tệp hồ sơ ấy; đổi `trang_thai` là việc của bên ghi sổ sau khi r3 qua review. |

**Ngoài HINT, r3 tự thêm** (mỗi mục có phép đo tại chỗ):

- Mục "Đường land" và điều kiện (1) của `depends_on`: phép đo bốn trạng thái S0–S3 cho thấy #752 không vào `master`
  một mình được; B6(a) đổi thành "đỏ có kiểm soát" đúng hai dòng.
- Hợp đồng đầu ra test với #763 (mục tiêu 2 và 4): đúng MỘT dòng chỉ gồm hai số nguyên ngăn bởi `/` — vì
  `bang_chung_xanh` lấy dòng khớp ĐẦU TIÊN (đo 23:42:14Z: chuỗi hai dòng `2/3` rồi `1/1` ⇒ `False`; `1/1` rồi `2/3`
  ⇒ `True`).
- "Số đo nền" đo lại: 27 hồ sơ (thêm `pr759`, `landed: false` ⇒ `BO_QUA`); 55 tệp HINT, 18 có nhãn; 276 biên nhận.

**Chỗ r3 lệch `HINT.patch`:**

- Hunk 1 thêm #751 vào `depends_on` của #752 — r3 không thêm: write set đã không giao (đo); quan hệ ấy nằm ở #763.
- Hunk 1 và 2 sửa `kich_thuoc` thành "khoảng 902" — r3 thay bằng ước mới (bốn tệp, không còn hai dòng sổ, thêm ca r3).
- Hunk 1 giữ điều kiện chờ #748 — bản r3 đầu (`11134f2`) bỏ nó cho việc cấp lease (đo write set không giao). Review
  lượt 3 bác (lớp P3 số 2); nay KHÔI PHỤC, r3 không còn lệch hunk này ở điểm ấy.
- `HINT.patch` không đụng B6; r3 viết lại B6 vì việc tách.

## Vá sau review lượt 3 (sửa tại chỗ, trước khi đóng băng)

r3 chưa có lease nào neo `spec_hash`, nên vá tại chỗ, giữ `revision: 3`. Bản trước vá: commit `11134f2`, sha256
`f11ac69cd2bd3621d742067ae3ee1f41de519471c41f3244cb90a281d97f9894`. Review lượt 3: reviewer Claude Sonnet 5.5
(subagent `review-sonnet-max`, tự khai; KHÔNG phải Codex), `reviewed_sha` `11134f2c3b29929ee12c043569b070b92c15c6f2`,
`verdict: changes_requested`, **P1 0 · P2 1 · P3 4 = 5 lớp**. `VERDICT.md` sha256
`0ed8ba4213bc53b0f3ce29ccbe5c0670155e38e73dc02be04d6bfb7f6a11f97e`; `HINT.patch` (7 hunk) sha256
`0a1102bd711f45aeae104d12ecf1080ff669e4cebcc754883e9177aa4116b3f4`. Lúc vá, hai tệp nằm ở thư mục tạm của phiên điều
phối, chưa có bản trong kho; thứ định danh là băm. `patch -p0 --fuzz=0` từ gốc worktree: thử khô rc 0, áp thật rc 0,
7/7 hunk, không `.rej`; phần còn lại áp tay như bảng dưới.

| lớp (hạng) | sửa ở đâu |
|---|---|
| `tran-adr-0044-lop-sensitive-cua-752-con-mo-sau-tach` (P2) | Hunk 1, rồi viết lại theo chỉ thị điều phối: `review_class` và `kich_thuoc` nói trần áp cho #752 là trần `sensitive` (≤ 3 tệp, ≤ 300 dòng thêm) TRỪ KHI chủ kho cấp ngoại lệ trần đích danh; `depends_on` thêm (4) — comment cấp lease phải nêu trần bằng số (đề xuất 4 tệp / 1.000 dòng thêm), thiếu ⇒ không cấp; "Đường land" A sửa "hai lớp trần". Không còn câu nào khai "trần thường" như dữ kiện. |
| `depends-on-748-bo-cho-lech-quyet-dinh-c-va-spec-763` (P3) | Áp tay: `depends_on` (3) khôi phục "chờ #748 land vào `master`" theo quyết định chủ kho (c); phép đo write set rời nhau giữ làm thông tin phụ; nhãn (1) đổi thành "THOẢ MỘT PHẦN"; "Đường land" A ghi head #752 dựng trên `master` sau #748 (khớp #763 r1 `depends_on` (2)); dòng lệch HINT về #748 ở trên sửa lại. |
| `b1b-b3-khong-doc-duoc-va-pham-vi-quet-cua-cong-cu-land-chua-co-ca` (P3) | Hunk 3, 4, 6, 7: B1b thêm ca byte không phải UTF-8 và ca thư mục tên `x-land-evidence.yaml` (⇒ rc 3) cùng đột biến "chỉ bắt `yaml.YAMLError`"; B2b mới (phạm vi quét); B3 đòi `len(tep)` bằng số tệp khớp glob. |
| `dan-chung-readme-655-sang-657-va-luat-khong-doi` (P3) | Hunk 2: mục "Luật" ghi chỗ đổi của L-5. Áp tay: `nguon_cap_viec` dòng README 655 → 657 (đo lại trên `a9ef33c`, `c522c17`, `11134f2`). |
| `b1c-19-dot-bien-chi-liet-ke-17` (P3) | Hunk 5: B1c ghi 19 = 13 + 2 biến thể `in` + 4 biên. |

## Số đo nền (đo 13:28:09Z 23-10-2026 trên cây `git archive 1d7e642`; số của `c522c17` ở mục "Đo lại nền sau #748 land (nền 1d7e642)")

Lệnh: một script đo dựng đúng chữ L-6 và L-5 dưới đây (`yaml.safe_load`, PyYAML 6.0.1, Python 3.11.15), chạy
`python3 -B -I <script> <gốc cây>`. Cùng script ấy chạy trên cây `git archive c522c17` tái lập ĐÚNG mọi số cũ của mục
này (27 · 14 · 16 · 13 DAT · 1 trượt · 13 `BO_QUA` = 11 + 2; 55 · 18/35/2/0 · 26 + 9; 29 + 6 + 0 trong 276 biên nhận;
65 · 10 · 2 ở "Hình dạng kế thừa"), nên số mới và số cũ do cùng một định nghĩa. So `c522c17`: `git diff --name-status
c522c17 1d7e642` cho land thêm 24 tệp và sửa 1 (`pr621-skill-bai-hoc`, vẫn `DAT`), HINT thêm 9 tệp, biên nhận thêm 5 tệp.

- **Hồ sơ land:** 51 tệp `ops/land/*-land-evidence.yaml`, 0 thư mục (đơn vị: tệp). 29 tệp có `landed: true`, cả 29 ở
  `trang_thai_packet.landed`; 0 tệp có khoá `landed` mức gốc; 40 tệp có `trang_thai_packet`, 0 tệp có nó khác ánh xạ.
  Theo L-6: 16 đạt (cả 16 dùng mảnh `#issuecomment-`), **13 trượt** = `ops/land/pr672-wp574-land-evidence.yaml` (không
  có `authorized_head_sha` / `authorization_url` ở MỨC GỐC; mục miễn trừ duy nhất) + **12 hồ sơ mới sau `c522c17`**
  (`pr779` `pr791` `pr792` `pr793` `pr800` `pr801` `pr818` `pr823` `pr832` `pr836` `pr848` `pr873`), cả 12 trượt đúng
  một mệnh đề: `authorization_url` trong kho nhưng thiếu mảnh (dạng `…/pull/NNN`). 22 tệp `BO_QUA` = 11 không có
  `trang_thai_packet` + 11 có mà `landed` không phải `True`: `pr684` (khoá `packet_landed`, không có `landed`) và 10 tệp
  `landed: false` (`pr759` `pr772` `pr838` `pr846` `pr849` `pr851` `pr862` `pr866` `pr869` `pr882`). Ghi chú trôi số:
  (a) `pr759` vẫn chờ chủ kho quyết `landed` (`DONG-ISSUE-750`, `cho_chu_kho`), hai khoá mức gốc của nó vẫn hợp lệ ⇒
  chuyển thành `true` thì thêm một `DAT` (`17/30`); (b) lát `wp748-r24` đang chạy (`depends_on` (3)) hạ 18 hồ sơ về
  `landed: false`, trong đó có cả 12 hồ sơ trượt và `pr672`: trên nhánh `agent/wp748-r24-claude` @ `d42713c` (15/18 tệp đã
  sửa, đo 13:28:49Z 23-10-2026) cùng script ra 14 `DAT` / 14 `landed` · 0 trượt · 0 `MIEN_TRU` · 37 `BO_QUA`.
- **HINT:** 64 tệp khớp `ops/reviews/**/*HINT.patch`, 0 thư mục (đơn vị: tệp). Theo chuỗi L-5 ĐẦY ĐỦ: 26 có nhãn, 2
  rỗng (0 byte, vẫn `thu-hoi-lease-a1a-r2/luot7-HINT.patch`, `thu-hoi-lease-a1a-r2/luot10-HINT.patch`), **36 thiếu nhãn
  nguyên văn** = 27 không có nhãn + 9 mang nhãn BỎ DẤU (`ci-duong-nhanh-ho-so/review-luot*-claude-HINT.patch`), 0
  `KHONG_DOC_DUOC`; chuỗi khoá `chưa chạy trên cây thật` và chuỗi cụt không có ` commit` cho cùng 26/36/2. Băm: 35 trong
  36 là bản sao có băm — 29 có sha256 trong 281 tệp `ops/**/*.receipt.yaml`, 6 (`thu-hoi-lease-va-cap-lai-spec/luot{1,2,3,5,6,7}`)
  chỉ có sha256 trong `luot*-VERDICT.md`/`luot*-EVIDENCE.md` cùng thư mục; **1 không ở đâu**:
  `ops/reviews/pr690-advisory-opus55/HINT.patch` (sha256 `07b90fba7de726107fef2e529ab9421a181144d543068fc170d2ff3a63a6619e`;
  `git grep` băm ấy trên `1d7e642` ra 0 tệp; commit đưa tệp vào, `97f818b`, tự khai "byte-exact" kèm 21 610 byte và băm rút gọn `07b90fba...a6619e` — khớp tệp, nhưng không ghi băm đầy đủ).
  Packet vẫn không sửa tệp HINT nào (Ngoài phạm vi); lý do "có băm" nay không phủ tệp này. Chín tệp HINT mới so
  `c522c17` (sáu `pr690-*`, hai `pr838-*`, một `pr870-review-1-codex`): 8 có nhãn đầy đủ, 1 là tệp vừa nêu.

## Luật

Không đổi so với r2, trừ L-5 bỏ vế "15/15 tệp có nhãn đều chứa cả ` commit`" (số cũ; 18/18 trên `c522c17`, 26/26 trên `1d7e642`, xem "Số đo nền").

- **L-6 (`kiem_ho_so_land.py`):** đọc bằng `yaml.safe_load` (thiếu PyYAML ⇒ rc 3, không phải rc 0). Gốc tài liệu phải
  là ánh xạ (tệp rỗng ⇒ `None`, danh sách đều không phải) — nếu không ⇒ rc 3. `landed` đọc ở `trang_thai_packet.landed`
  khi tài liệu có khoá `trang_thai_packet`; không có khoá ấy thì đọc `landed` mức gốc; `trang_thai_packet` có mặt mà
  không phải ánh xạ ⇒ rc 3. Hồ sơ có `landed` **`is True`** (boolean YAML; chuỗi `"true"` KHÔNG tính ⇒ `BO_QUA` kèm lý
  do) thì HAI khoá ở MỨC GỐC tài liệu (không tìm lồng — `pr672` có `authorized_head_sha` ×3 trong `candidates[*]`,
  không tính) phải đạt: `authorized_head_sha` là `str` và `re.fullmatch(r"[0-9a-f]{40}", v)` (KHÔNG `re.match` + `$`:
  `$` còn khớp ngay trước một ký tự xuống dòng ở cuối chuỗi); `authorization_url` là `str`,
  `startswith("https://github.com/ducthangho/tra-luat/")` (KHÔNG `in`) và chứa `#issuecomment-` hoặc
  `#pullrequestreview-` hoặc `#discussion_r`. `landed` khác `True` ⇒ không kiểm. YAML không parse được ⇒ rc 3
  (fail-close), không phải `BO_QUA`.
- **L-5 (`kiem_nhan_hint.py`):** tệp `*HINT.patch` mà nội dung sau `strip()` không rỗng, không chứa nguyên văn chuỗi
  ĐẦY ĐỦ `chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit` (PROTOCOL dòng 651–652 @ `1d7e642`,
  644–645 @ `c522c17`, ngắt giữa `trách nhiệm` và `commit`: nối bằng MỘT dấu cách) ⇒ xếp **`KHONG_DU_DIEU_KIEN_PATCH_AS_HINT`** (chỉ đo ràng
  buộc 1 của PROTOCOL §8, không đo 2 và 3); rỗng sau `strip()` ⇒ `RONG`; có ⇒ `CO_NHAN`. Đọc UTF-8 nghiêm; giải mã lỗi
  VÀ mọi `OSError` (thư mục tên `*HINT.patch`, symlink treo, quyền) ⇒ `KHONG_DOC_DUOC` (không âm thầm
  `errors="replace"`, không để ngoại lệ thoát).

## Vá sau review lượt 4 (sửa tại chỗ, trước khi đóng băng)

Bản trước vá: commit `a2069ac49fdfadfa1b171cf75f146510f7c83058`, sha256
`9d5715d4cc28319214791a5562ea9380c040a6e0221433b250077053febb5044`. Review lượt 4: reviewer Claude Sonnet 5.5
(subagent `review-sonnet-max`, tự khai; KHÔNG phải Codex), `reviewed_sha` = commit ấy, `verdict: changes_requested`,
**P1 0 · P2 1 · P3 2 = 3 lớp**; `VERDICT.md` sha256 `bbd99a302dc6b7bfac5be07b6b658f68b88f876546f061f0e28f01c4263bbd75`;
`HINT.patch` (5 hunk) sha256 `714de6e502954ae8b8c98e85393e02bf7f6b8475d734818d7652b97f7407c6b3`. Lúc vá, hai tệp nằm ở
thư mục tạm của phiên điều phối, chưa có bản trong kho; thứ định danh là băm. Áp NGUYÊN VĂN cả 5 hunk của HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT.

| lớp | hạng | chỗ sửa |
|---|---|---|
| `b6d-gate-ops-cung-do-o-dau-752-moi-job-khac-xanh-sai` | P2 | B6(d) và mục "Đường land" A: head riêng #752 đỏ có kiểm soát ở CẢ `gate-registry` LẪN `gate-ops` (`ci_duong_nhanh_test.py` 103/104, khớp C8 của #763) |
| `r2-doc-chu-standard-dan-nham-nguon-r3-ban-dau` | P3 | hàng `review_class`: câu "trần thường" quy đúng về r3 bản đầu `11134f2` |
| `b2b-song-sot-qua-b3-mau-thuan-len-tep-va-thieu-tiem-mien-tru` | P3 | B2b: vế `len(tep)` của B3 giết `*.yaml`; ghi phải tiêm miễn trừ `{}`; "Chưa đo được" thêm B2b, B3 |

## Vá sau review lượt 5 (sửa tại chỗ, trước khi đóng băng)

Bản trước vá: commit `b6ab45e`, sha256 `9901e8186c99d5977f5144b7d1691d4a5cc6f6be995478b3e88ce321f24743b3`. Review lượt 5
(`approve`, 0 P1 · 0 P2 · 2 P3; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, `reviewed_sha`
`b6ab45e56c41d6aa69bd067a46d8e064ae753c51`; VERDICT sha256 `4f281ba4d763e6395effc879a0ffb09ec212c8cd7fe8f5e88a548ed1bb4e5ef8`,
HINT sha256 `c60a53e657fad36fcc9274f9671b59d1e6fcb578f3614bc15fb4262db955c62d`). Áp NGUYÊN VĂN 3 hunk của HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT. Chủ kho cho đúng MỘT vòng vá P3 này.

| lớp | hạng | chỗ sửa |
|---|---|---|
| `gate-ops-vang-o-hai-cau-chi-nhac-gate-registry` | P3 | hai câu còn chỉ nhắc `gate-registry` nay nêu cả `gate-ops` |
| `va-luot-4-thieu-ban-truoc-va-va-danh-tinh-reviewer` | P3 | mục "Vá sau review lượt 4" thêm bản trước vá, danh tính reviewer, `reviewed_sha` |

## Mục tiêu

1. **[`ops/kiem_ho_so_land.py`]** CLI `python ops/kiem_ho_so_land.py --root . [--json]`: quét
   `ops/land/*-land-evidence.yaml` (không đệ quy; tên tệp là QUY ƯỚC, không ADR nào đặt), in một dòng chứa glob ấy như
   một token riêng (tách theo khoảng trắng; r4 thêm, xem B3) ở đầu ra chữ VÀ khoá `phamvi_glob` ở `--json`; in từng tệp `DAT`/`TRUOT`/`BO_QUA`/`MIEN_TRU` kèm lý do, tổng
   `n_dat/n_landed` và số `MIEN_TRU`; `--json` có `tep[]` (`duong_dan`, `trang_thai`, `ly_do`), `n_dat`, `n_landed`,
   `n_mien_tru`, `phamvi_glob`. Rc 0 khi không tệp nào trượt NGOÀI danh sách miễn trừ; rc 1 khi có; rc 2 lỗi tham số,
   kể cả `--root` không phải thư mục hoặc không chứa thư mục `ops/land` (kiểm TRƯỚC khi quét, không in dòng đếm nào);
   rc 3 khi không đọc được tệp/YAML, gốc hoặc `trang_thai_packet` sai kiểu, thiếu PyYAML, hoặc miễn trừ vắng. Thứ tự ưu
   tiên: 2 trước 3 trước 1 trước 0 — khi đồng thời có tệp trượt và điều kiện rc 3 thì rc 3. Danh sách miễn trừ là hằng
   trong mã, mỗi mục có lý do, và hàm chính nhận nó làm tham số (test tiêm `{}`); bản land chứa đúng một mục:
   `ops/land/pr672-wp574-land-evidence.yaml` — lý do "hồ sơ của packet khác, ghi trước luật L-6; sửa ở packet riêng".
   Miễn trừ một tệp không tồn tại ⇒ rc 3.
2. **[`ops/kiem_ho_so_land_test.py`]** Bộ test tự đứng, dựng cây tạm, chạy được bằng `python -B <tệp>` từ gốc kho; in
   đúng MỘT dòng chỉ gồm hai số nguyên ngăn bởi `/` (số ca đạt / tổng ca; đơn vị: ca test) và không dòng nào khác có
   dạng ấy — đó là mẫu mà #763 sẽ đăng ký (mẫu của mục `ops/nhanh_don_duoc_test.py`, dòng 53 của sổ tại `1d7e642`, dòng 52 tại `c522c17`; mẫu không đổi).
3. **[`ops/kiem_nhan_hint.py`]** CLI `python ops/kiem_nhan_hint.py --root . [--json]`: liệt kê mọi tệp khớp
   `ops/reviews/**/*HINT.patch` theo L-5, in một dòng chứa glob ấy như một token riêng (tách theo khoảng trắng; r4
   thêm, xem B5) ở đầu ra chữ VÀ khoá `phamvi_glob` ở `--json`; in
   đếm từng loại; `--json` có `tep[]`, `dem{}` theo bốn loại, `phamvi_glob`. Rc 0 khi đọc được hết (công cụ BÁO CÁO,
   không phải cổng); rc 2 lỗi tham số, kể cả `--root` không phải thư mục hoặc không chứa thư mục `ops/reviews` (0 tệp
   không phải là "sạch"); rc 3 khi có `KHONG_DOC_DUOC`. Không ghi tệp nào.
4. **[`ops/kiem_nhan_hint_test.py`]** Như mục tiêu 2 cho công cụ HINT: tự đứng, cây tạm, `python -B <tệp>`, đúng MỘT
   dòng dạng hai số nguyên ngăn bởi `/`.

Mục tiêu 5 của r2 (thêm hai mục `MOI`) KHÔNG còn ở đây: nó là mục tiêu 1 của `ops/specs/no-p3-dang-ky-ci-r2.md` (#763; dòng 68 @ `6c2fe9b`, đo 13:55:03Z 23-10-2026; ở r1 cũng là mục tiêu 1).

## Nghiệm thu

- **B1 (L-6 răng):** cây tạm (tiêm danh sách miễn trừ `{}`), mỗi hồ sơ `landed: true` vi phạm đúng MỘT mệnh đề.
  ⇒ `DAT`: hồ sơ đủ, một bản cho mỗi mảnh URL (`#issuecomment-`, `#pullrequestreview-`, `#discussion_r`). ⇒ `TRUOT`:
  SHA 39 ký tự · SHA viết hoa · SHA 40 hex kèm một ký tự xuống dòng ở cuối (khối YAML `|`) · `authorized_head_sha`
  là số nguyên 40 chữ số thập phân · cả HAI khoá hợp lệ chỉ nằm lồng trong `candidates[0]` · URL ngoài kho · URL giả
  dạng `https://evil.example/github.com/ducthangho/tra-luat/pull/1#issuecomment-1` · URL nhúng nguyên tiền tố của L-6
  sau một tiền tố lạ `https://evil.example/?next=https://github.com/ducthangho/tra-luat/pull/1#issuecomment-1` · URL
  trong kho nhưng thiếu mảnh (`…/pull/721`) · hồ sơ không có `trang_thai_packet`, `landed: true` ở mức gốc, SHA viết
  hoa. ⇒ `BO_QUA`: `landed: false` thiếu cả hai; `landed: "true"` (chuỗi). Rc 1. ĐỎ khi, MỖI đột biến làm đúng ca của
  nó ĐỎ: nới regex thành `[0-9a-fA-F]{39,40}` ⇒ BA ca (SHA 39, SHA hoa, hồ sơ `landed` mức gốc); `re.match` + `$` ⇒
  ca xuống dòng cuối; bỏ hẳn kiểm kiểu ⇒ ca số và ca lồng; thay bằng `str(v)` ⇒ ca số; tìm khoá theo độ sâu ⇒ ca lồng;
  bỏ kiểm URL ⇒ ca URL ngoài kho; kiểm URL bằng `in` với CHÍNH chuỗi tiền tố của L-6 ⇒ ca nhúng tiền tố (ca giả dạng
  chỉ giết `in` bỏ scheme hay bỏ host: chuỗi tiền tố KHÔNG là chuỗi con của URL giả dạng); bỏ riêng kiểm mảnh ⇒ ca
  thiếu mảnh; bỏ một mảnh khỏi tập cho phép ⇒ ca `DAT` của mảnh ấy; `landed` kiểm truthy ⇒ ca chuỗi `"true"`; chỉ đọc
  `trang_thai_packet.landed` ⇒ ca `landed` mức gốc.
- **B1b (fail-close):** YAML hỏng (ngoặc không đóng, tab thụt đầu dòng) ⇒ rc 3; tệp rỗng, gốc là danh sách,
  `trang_thai_packet` là chuỗi hoặc null ⇒ rc 3; chạy công cụ trong tiến trình con có import `yaml` bị chặn
  (`sys.modules["yaml"] = None` trước khi nạp) VÀ tiêm miễn trừ `{}` ⇒ rc 3; một cây chứa CẢ hồ sơ trượt lẫn hồ sơ
  YAML hỏng ⇒ rc 3; hồ sơ mang thẻ `!!python/object/apply:builtins.print` ⇒ rc 3 và không in gì từ thẻ; một hồ sơ
  `*-land-evidence.yaml` có byte không phải UTF-8 và một THƯ MỤC tên `x-land-evidence.yaml` ⇒ rc 3, không phải traceback
  rc 1 (mục tiêu 1: "rc 3 khi không đọc được tệp"). Không ca nào
  được thành `BO_QUA` âm thầm. ĐỎ khi: nuốt lỗi YAML thành `BO_QUA` ⇒ ca YAML hỏng; để ngoại lệ thoát khi gốc là `None`
  ⇒ ca tệp rỗng; coi `trang_thai_packet` sai kiểu là vắng ⇒ ca chuỗi/null; nuốt `ImportError` ⇒ ca thiếu PyYAML (chỉ
  khi đã tiêm `{}`: không tiêm thì rc 3 đến từ "miễn trừ vắng" và đột biến sống); đảo thứ tự ưu tiên rc ⇒ ca cây trộn
  (ra 1 thay vì 3); `yaml.unsafe_load` ⇒ ca thẻ python (rc khác 3 và tải trọng của thẻ chạy); chỉ bắt `yaml.YAMLError`
  ⇒ hai ca không đọc được (đo 16-10-2026 trên bản tham chiếu: cả hai ra rc 1 kèm traceback, ca YAML hỏng vẫn rc 3).
- **B1c (giá trị ca đã chốt — đo lại 23:39:22Z–23:39:57Z 15-10-2026, lặp 23:46:26Z):** chạy lại harness của
  reviewer lượt 2 (bản sao ngoài kho, `python3 -B -I`) trên bản tham chiếu dựng đúng chữ L-6: với giá trị ca CŨ (số `12345`, lồng chỉ
  `authorized_head_sha`) thì `str(v)`, tìm theo độ sâu và `in` với chính tiền tố đều SỐNG SÓT; với tập ca B1 ở trên
  cộng bốn ca biên — `TRUOT`: SHA 41 hex, SHA 64 hex, URL repo anh em
  `https://github.com/ducthangho/tra-luat-evil/pull/1#issuecomment-1`; `BO_QUA`: `landed: 1` — tức 19 ca, bản đúng chữ
  xanh và **19/19 đột biến bị giết, 0 sống sót** (19 = 13 nêu ở B1, "bỏ một mảnh" tính 3, + 2 biến thể của `in` chỉ nhắc trong
  ngoặc ở B1: `"github.com/ducthangho/tra-luat/" in url` bỏ scheme và `"ducthangho/tra-luat" in url` bỏ host, + 4 biên), gồm bốn đột biến biên (`{40,}` ⇒ SHA 41 và SHA 64; nhận cả 40 lẫn 64
  hex ⇒ SHA 64; bỏ dấu `/` cuối tiền tố ⇒ repo anh em; so `!= True` thay `is True` ⇒ `landed: 1`). B1b chạy lại
  23:40:05Z: bốn đột biến fail-close chết đúng ca, `nuot_importerror` chỉ chết ở ca có tiêm `{}` (rc 0) — đúng điều
  kiện đã chốt. Hai ca cây trộn và thẻ python đo lại 23:51:07Z (bản tham chiếu + hai đột biến, cây tạm): cây trộn —
  đúng chữ rc 3, đảo thứ tự rc 1, trong khi cây chỉ có hồ sơ trượt (rc 1) hay chỉ có YAML hỏng (rc 3) không phân biệt
  được hai bản; thẻ `!!python/object/apply:builtins.print` — đúng chữ rc 3 và tải trọng KHÔNG chạy, `unsafe_load` rc 1
  và tải trọng CHẠY (reviewer lượt 2 dùng hồ sơ có đủ hai khoá nên ghi rc 0; cả hai đều khác 3).
- **B2 (miễn trừ — đo HẰNG CỦA BẢN GIAO, không tiêm):** chạy CLI thật, không tiêm danh sách, trên cây tạm mà test tự DỰNG
  (không chép tệp sống của kho) chỉ một tệp tên `ops/land/pr672-wp574-land-evidence.yaml` với đúng hai tính chất
  `trang_thai_packet.landed: true` và không có hai khoá ở mức gốc (ca A) ⇒ rc 0 và đúng MỘT dòng trạng thái `MIEN_TRU` (dòng
  của một tệp, cột trạng thái bằng `MIEN_TRU`; dòng tổng kết có chữ ấy không tính) kèm lý do khác rỗng; cùng lệnh trên cây
  tạm KHÔNG có tệp ấy (ca B) ⇒ rc 3 (miễn trừ vắng). Không chép tệp sống vì lát `wp748-r24` hạ nó về `landed: false` (đo 16:58Z
  23-10-2026: tip nhánh `agent/wp748-r24-claude` `f08efa1043680134e3534eef8ac95dd901ae7dab` có `pr672` ở `landed: False`; tip
  `master` `d9ef666b3cbe5acb246c2bdfb0b6e294f2fdbffc` còn `True`, byte bằng `1d7e642`; ca A với tệp của nhánh ra `BO_QUA`, 0 dòng
  `MIEN_TRU`, ĐỎ cả với bản đúng chữ). Hai ca
  đọc hằng của bản giao nên đo luôn câu "đúng một mục" của mục tiêu 1; danh sách tiêm (B1, B1b, B2b) tắt hằng ấy và
  KHÔNG đo nó. ĐỎ khi, MỖI đột biến làm đúng ca của nó ĐỎ: bỏ kiểm tồn tại ⇒ ca cây thiếu `pr672` (rc khác 3); gỡ mục
  `pr672` khỏi hằng ⇒ ca cây có `pr672` ra `TRUOT`, rc 1; thêm một khoá thứ hai vào hằng ⇒ ca cây chỉ có `pr672` ra rc 3
  (khoá thừa trỏ tệp vắng); lý do của mục `pr672` rỗng ⇒ ca cây có `pr672` (dòng `MIEN_TRU` không kèm lý do). Đo 15:44Z
  23-10-2026 trên bản tham chiếu của reviewer lượt 7 (ngoài kho): cả bốn đột biến ĐỎ khi B2 đọc hằng bản giao; khi B2
  chỉ tiêm danh sách thì chỉ đột biến đầu ĐỎ, ba đột biến sau qua. Đo lại 17:14Z 23-10-2026 (lượt 8) với tệp do test dựng thay cho
  bản sao nguyên byte: kết quả y hệt ở cả hai cách đọc (bản đúng chữ XANH; cách đọc hằng: cả bốn đột biến ĐỎ; cách tiêm: chỉ bỏ
  kiểm tồn tại ĐỎ).
- **B2b (phạm vi quét — mệnh đề "không đệ quy, tên tệp là quy ước" của mục tiêu 1):** cây tạm (tiêm danh sách miễn trừ
  `{}` như B1: không tiêm thì rc 3 vì miễn trừ vắng, ở cả bản đúng lẫn hai đột biến — đo 16-10-2026 trên bản tham chiếu) có
  `ops/land/z-land-evidence.yaml` đủ hai khoá (⇒ `DAT`), `ops/land/x-provenance.yaml` và
  `ops/land/sub/y-land-evidence.yaml`, hai tệp sau mang `landed: true` thiếu hai khoá (bị quét sẽ `TRUOT`) ⇒ rc 0 và
  `tep[]` có đúng MỘT phần tử, `z-…`. ĐỎ khi quét `ops/land/*.yaml` hoặc đệ quy (`rglob("*-land-evidence.yaml")`) ⇒ rc 1
  và `tep[]` có phần tử ngoài phạm vi (đo: 2 phần tử cho mỗi đột biến). Đo 16-10-2026 trên bản tham chiếu, TRƯỚC khi B3
  có vế `len(tep)`: cả hai đột biến SỐNG SÓT qua B1–B3 vì trên `c522c17` `*.yaml` chỉ thêm
  `ops/land/pr666-wp650-provenance.yaml` (`BO_QUA`; 28 tệp thay vì 27) và quét đệ quy không thêm tệp nào. SAU vế
  `len(tep)` của B3, đột biến `*.yaml` chết ở B3 (`len(tep)` 28 khác 27); chỉ đột biến đệ quy còn sống tới B2b. Trên
  `1d7e642` (đo 13:28:09Z 23-10-2026, script ở "Số đo nền"): `*.yaml` vẫn chỉ thêm đúng tệp ấy (52 tệp thay vì 51; tệp ấy
  không có `trang_thai_packet` lẫn `landed` ⇒ `BO_QUA`), quét đệ quy vẫn không thêm tệp nào ⇒ cùng kết luận, với
  `len(tep)` 52 khác 51 trên cây đầy đủ (40 khác 39 trên bản sao đã bỏ `F` mà B3 (ii) đo; 15:36Z 23-10-2026, bản tham
  chiếu của reviewer lượt 7).
- **B3 (trên kho thật — VỊ TỪ, không số cứng; quyết định chủ kho 23-10-2026,
  [comment trên Issue #752](https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792), mục 3):** đo trên
  cây `base_sha` của lease thực thi, đo lại lúc thi hành (L5 của `soan-spec`). Mọi tập tính theo ĐƯỜNG DẪN, không
  tên tệp nào ghi sẵn trong tiêu chí, trừ khoá miễn trừ duy nhất của mục tiêu 1 (`ops/land/pr672-wp574-land-evidence.yaml`)
  ở `E` và ở hai ghim của "Ca đỏ thật":
  - `S` = các tệp khớp `ops/land/*-land-evidence.yaml` (không đệ quy) trên cây ấy.
  - `F` (finding của DỮ LIỆU) = các tệp trong `S`, ngoài `E`, mà một phép đo ĐỘC LẬP với công cụ thấy trượt L-6:
    `landed` `is True` và trượt ít nhất một mệnh đề, hoặc chạm một điều kiện rc 3 của L-6 (không đọc được, gốc hay
    `trang_thai_packet` sai kiểu). Phép đo độc lập = một script đúng chữ L-6 (`yaml.safe_load`), KHÔNG import mã của
    packet; băm script và đầu ra của nó ghi vào biên nhận.
  - `E` (miễn trừ trong mã) = các tệp công cụ in `MIEN_TRU`; một tệp chỉ tính vào `E` khi đo được cả ba: có mục trong
    hằng miễn trừ (mục tiêu 1: khoá duy nhất `ops/land/pr672-wp574-land-evidence.yaml`), lý do in ra khác rỗng, và phép đo độc lập cũng thấy nó trượt (miễn trừ không được che
    một hồ sơ đạt).
  - Cụm "hồ sơ có miễn trừ khai rõ" KHÔNG có trong thân comment neo (0 lần "miễn trừ", 0 lần "khai rõ"; đo 15:38Z
    23-10-2026): đặc tả đọc nó là `E` cộng `F`, mỗi tệp `F` do executor KHAI như dưới đây — cách đọc là thiết kế của đặc
    tả, chủ kho xác nhận khi cấp lease.

  ⇒ ĐẠT khi đủ bốn vế: (i) trên cây đầy đủ — nếu `F` có tệp chạm điều kiện rc 3 thì rc 3 (danh sách `TRUOT` khi ấy
  không bị ràng buộc, vế (ii) gánh phần còn lại); nếu không thì tập đường dẫn công cụ in `TRUOT` bằng đúng `F`, `ly_do`
  từng tệp chứa tên khoá của MỖI mệnh đề mà phép đo độc lập thấy trượt (`authorized_head_sha` hoặc `authorization_url`) và
  KHÔNG chứa tên khoá của mệnh đề mà nó thấy đạt,
  `n_dat`, `n_landed`, `n_mien_tru` ở `--json` bằng số đếm cùng tên của phép đo độc lập (số tệp `DAT`, số tệp có `landed`
  là `True`, và số tệp của `E`; như B5 so `dem`), rc 1 khi `F` khác rỗng, rc 0 khi `F` rỗng; (ii) trên bản
  sao cây ấy đã bỏ đúng các tệp `F` khỏi `ops/land/` (không sửa tệp nào khác): rc 0, `n_dat + n_mien_tru` bằng `n_landed`, `len(tep)` bằng số tệp khớp glob trên bản sao;
  (iii) đầu ra chữ có một dòng mà một TOKEN (tách theo khoảng trắng) BẰNG đúng chuỗi `ops/land/*-land-evidence.yaml` —
  khớp chuỗi con không tính; (iv) `--json` có `phamvi_glob` BẰNG đúng chuỗi ấy.

  **Executor gặp `F` khác rỗng:** BÁO — liệt kê đường dẫn và mệnh đề trượt trong thân PR và biên nhận, ghi là nợ dữ liệu
  cho bên ghi sổ — rồi đi tiếp: đó không phải lỗi công cụ, không phải lý do dừng packet. KHÔNG sửa hồ sơ nào
  (`ops/land/**` nằm ngoài write set), KHÔNG thêm tệp `F` vào hằng miễn trừ, KHÔNG nới L-6 để `F` đạt.

  ⇒ ĐỎ khi (đột biến CÔNG CỤ, chạy trên bản sao, mỗi đột biến đổi màu vế ghi kèm): bỏ riêng kiểm mảnh URL ⇒ tệp `F`
  trượt mảnh thành `DAT` ⇒ (i) ĐỎ; tiền tố URL siết thành `https://github.com/ducthangho/tra-luat/pull/` ⇒ hồ sơ đạt
  dùng `/issues/` thành `TRUOT` ⇒ (ii) ĐỎ (trên `1d7e642`: 2 trong 16 hồ sơ đạt dùng `/issues/`, 14 dùng `/pull/`; đo
  13:58:28Z 23-10-2026 bằng phép đo độc lập); quét `*.yaml` ⇒ `len(tep)` lệch số tệp khớp glob ⇒ (ii) ĐỎ (40 khác 39
  trên bản sao đã bỏ `F` của `1d7e642` — 52 khác 51 chỉ trên cây đầy đủ, nơi vế (ii) không đo; 28 khác 27 trên `c522c17`,
  nơi `F` rỗng nên bản sao trùng cây đầy đủ); bỏ dòng in glob ở đầu ra chữ, hoặc in glob dính hậu tố (ví dụ
  `ops/land/*-land-evidence.yaml.bak`) ⇒ (iii) ĐỎ (khoá JSON một mình không đo việc in ra màn hình — reviewer lượt 2 đo
  J2: bỏ dòng in giữ nguyên rc, đếm và khoá JSON); bỏ khoá `phamvi_glob` hoặc đổi giá trị ⇒ (iv) ĐỎ; `ly_do` rỗng, nêu sai khoá, hoặc luôn nêu cả hai khoá ⇒ (i) ĐỎ (đo 17:12Z
  23-10-2026 trên bản tham chiếu của reviewer lượt 8, ngoài kho, vế `ly_do` đọc hai chiều: cả ba ĐỎ; đọc một chiều chứa thì
  đột biến luôn nêu cả hai khoá vẫn ĐẠT, 12 tệp `F` chỉ trượt `authorization_url`).

  **Ca đỏ thật (cây cố định, không trôi):** cây `git archive 1d7e642` — nền đóng băng của r4 — có `F` khác rỗng; công cụ
  trên cây ấy phải ra rc 1 với tập `TRUOT` bằng đúng `F` của cùng cây; tập đường dẫn in `MIEN_TRU` bằng đúng
  {`ops/land/pr672-wp574-land-evidence.yaml`} (ghim hằng: `pr672` trượt trên cây này theo phép đo độc lập, nên tập này là
  HẰNG BẢN GIAO của mục tiêu 1 chứ không phải thứ công cụ tự khai); và `n_dat`, `n_landed`, `n_mien_tru` ở `--json` bằng
  số đếm cùng tên của phép đo độc lập (16, 29, 1 trên cây này; ghim bộ đếm). Đột biến chạy trên cây ấy, mỗi cái đổi màu
  phép ghi kèm: "bỏ riêng kiểm mảnh URL" ⇒ (i) ĐỎ; "gỡ mục `pr672` khỏi hằng" ⇒ ghim hằng ĐỎ (tập `MIEN_TRU` rỗng); "thêm
  12 tệp `F` vào hằng" ⇒ ghim hằng ĐỎ (13 phần tử) và (i) ĐỎ; "bỏ sót hai hồ sơ hợp lệ khỏi bộ đếm" ⇒ ghim bộ đếm ĐỎ
  (`n_dat` 14 khác 16, `n_landed` 27 khác 29). Đo 15:36Z 23-10-2026 trên r4 CHƯA vá (bản tham chiếu của reviewer lượt 7,
  ngoài kho): "gỡ mục" và "bỏ sót" đều ra B3 ĐẠT (vế (i)–(iv) xanh), "thêm 12 tệp" ra ĐẠT khi `E` đọc rộng (15:42Z: đỏ khi `E`
  chỉ nhận khoá `pr672`) — nên hai ghim thuộc B3. Ca này giữ răng cho B3 kể cả khi `F` tại `base_sha` của lease rỗng;
  executor chạy cả hai cây.

  Vế ĐỎ "gỡ miễn trừ ⇒ rc 1" của r3 RA KHỎI B3: dưới vị từ nó không đổi màu — gỡ mục `pr672` khỏi hằng thì tệp ấy rời
  `E` và vào `F` đúng theo định nghĩa (phép đo độc lập thấy nó trượt), nên (i) và (ii) vẫn đạt; còn nếu lát `wp748-r24`
  vào `master` thì `pr672` thành `BO_QUA`. Răng của hằng bản giao nằm ở HAI chỗ: hai ghim của "Ca đỏ thật" ngay
  trên và B2 (CLI thật, không tiêm); B1, B1b, B2b tiêm `{}` nên không đo hằng.

  **Minh hoạ có giờ đo, KHÔNG phải đích** (script `l6_doc_lap.py` của lượt soạn r4, ngoài kho, đã xoá khi dọn thư mục
  đo — tái lập bằng bất kỳ script đúng chữ L-6; PyYAML 6.0.1, Python 3.11.15): trên `1d7e642` (13:54:38Z 23-10-2026) `S` 51 tệp, `F` 12 tệp (cả 12 chỉ trượt mảnh URL, danh sách ở
  "Số đo nền"), `E` 1, 16 `DAT`, 22 `BO_QUA`, 0 tệp chạm điều kiện rc 3 — khớp lượt đo 13:28:09Z; trên `master`
  `8324567` (13:55:46Z; cây = `git archive 1d7e642` của `ops/land` và `ops/reviews`, cộng đúng ba tệp khớp glob của
  B3/B5 trong 53 tệp mà `compare` liệt kê dưới hai thư mục ấy — 52 thêm, 1 sửa là `ops/reviews/README.md`, không tệp
  nào bị xoá — tải bằng
  `gh api -H 'Accept: application/vnd.github.raw' repos/ducthangho/tra-luat/contents/<tệp>?ref=<OID>`): `S` 53, `F` 12,
  `E` 1, 16 `DAT`, 24 `BO_QUA` — hai hồ sơ mới `ops/land/pr870-claude-md-bai-hoc-c-land-evidence.yaml` và
  `ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml` mang `landed: false` và `authorization_url: KHONG_AP_DUNG`,
  tức thành `landed: true` thì rơi vào `F`; trên nhánh `agent/wp748-r24-claude` @ `d42713c` (lượt đo 13:28:49Z, 15/18
  tệp đã sửa): 14 `DAT` / 14 `landed`, `F` rỗng, `E` rỗng, 37 `BO_QUA`. Lịch sử `c522c17` (bản tham chiếu 23:37:59Z
  15-10-2026): 13 `DAT`, `E` 1, `F` rỗng, 13 `BO_QUA`, `len(tep)` 27.
- **B4 (L-5 răng):** cây tạm có các tệp HINT: có nhãn đầy đủ; thiếu nhãn — một mồi là văn xuôi chứa `chưa chạy`, một
  mồi mang NHÃN ĐẦY ĐỦ TRỪ ` commit` (mồi chỉ có đuôi `… tự chịu trách nhiệm` thì chuỗi khoá và chuỗi cụt sống sót —
  đo lại 23:40:06Z); rỗng; chỉ có xuống dòng (⇒ `RONG`); byte không phải UTF-8; thư mục tên `x-HINT.patch` ⇒ đúng
  loại; rc 3 vì có `KHONG_DOC_DUOC`. ĐỎ khi: khớp nhãn bằng `chưa chạy` ⇒ hai mồi; bằng chuỗi khoá
  `chưa chạy trên cây thật` hoặc chuỗi cụt bỏ ` commit` ⇒ mồi cụt; `errors="replace"` ⇒ ca byte lỗi; để `OSError`
  thoát ⇒ cả bảy ca; rỗng theo kích thước 0 hoặc không `strip()` ⇒ ca chỉ có xuống dòng.
- **B5 (trên kho thật, chỉ đọc):** `python ops/kiem_nhan_hint.py --root . --json` ⇒ rc 0, `dem` khớp số đo nền (đo lại
  lúc thi hành; trên `1d7e642`, script đúng chữ L-5 đo 13:28:09Z 23-10-2026: `CO_NHAN` 26 ·
  `KHONG_DU_DIEU_KIEN_PATCH_AS_HINT` 36 · `RONG` 2 · `KHONG_DOC_DUOC` 0, 64 tệp ⇒ vế rc 0 vẫn đạt được; bản tham chiếu
  23:37:59Z 15-10-2026 trên `c522c17`: 18 · 35 · 2 · 0, 55 tệp; trên `master` `8324567`, phép đo độc lập 13:55:46Z
  23-10-2026: 26 · 37 · 2 · 0, 65 tệp — tệp mới `ops/reviews/pr889-review-1-codex/HINT.patch` thiếu nhãn; mọi số ở đây là
  minh hoạ, đích là `dem` bằng phép đo độc lập trên cùng cây), `phamvi_glob` BẰNG đúng glob mục tiêu 3; chạy thêm không
  `--json` ⇒ đầu ra chữ có một dòng mà một TOKEN (tách theo khoảng trắng) BẰNG đúng chuỗi `ops/reviews/**/*HINT.patch`
  (khớp chuỗi con không tính); `git status --porcelain` rỗng trước VÀ sau (tệp bị `.gitignore` như `__pycache__` thì phép
  đo này KHÔNG bắt được). ĐỎ khi: công cụ ghi một tệp ngoài `.gitignore` ⇒ `git status` không rỗng; bỏ khoá
  `phamvi_glob` hoặc đổi giá trị ⇒ ĐỎ; bỏ dòng in glob ở đầu ra chữ, hoặc in glob dính hậu tố (ví dụ
  `ops/reviews/**/*HINT.patch.orig`) ⇒ ĐỎ.
- **B6 (cổng kho, theo đường land A):** (a) trên head của #752 (chưa có mục `MOI`):
  `python -B .claude/dev/ci_dang_ky_test.py` (không `--chay`) ⇒ rc 1, `ĐĂNG KÝ: 26/24` (tệp test trên cây / mục
  trong sổ), ĐÚNG HAI dòng `ĐỎ:` và cả hai là `test sống chưa đăng ký:` cho đúng hai tệp test của write set, `TỔNG: ĐỎ` (S1, đo
  13:30:29Z 23-10-2026 trên `1d7e642`; `25/23` trên `c522c17`, 23:33Z 15-10-2026). ĐỎ (tiêu chí trượt) khi số dòng `ĐỎ:`
  khác 2 hoặc có dòng loại khác: thêm một test lạ thứ ba ⇒ ba dòng `ĐỎ:`, `ĐĂNG KÝ: 27/24` (đo 13:30:37Z 23-10-2026; `26/23`
  trên `c522c17`, 23:42:14Z). Số `26/24` đã đo lại sau khi #748 land; đo lại nữa nếu #751 hay packet nào khác thêm test
  sống vào `master` trước. (b) `ruff check --select F` trên bốn tệp mới: delta 0 (multiset) so với cơ sở rỗng; máy đo
  lại 23-10-2026 vẫn có binary `ruff` 0.15.8 (`python3 -m ruff` báo không có module), CI @ `1d7e642` vẫn ghim 0.15.15 —
  dùng dạng có trên máy thi hành và ghi phiên bản. ĐỎ khi chèn một import thừa ⇒ `F401`, rc 1 (đo 13:31:22Z 23-10-2026:
  bốn tệp giả `All checks passed!` rc 0; một tệp có `import fractions` ⇒ `F401`, rc 1; lịch sử 23:42:14Z 15-10-2026 y
  hệt). (c) mỗi test chạy bằng `python -B <tệp>` in đúng một dòng dạng `N/N` (N ≥ 1, hai
  số bằng nhau); phép đo ĐẾM số dòng khớp dạng ấy trong đầu ra. ĐỎ khi số dòng ấy khác 1 (sổ chỉ đọc dòng khớp ĐẦU
  TIÊN: đo 23:42:14Z 15-10-2026, `2/3` rồi `1/1` ⇒ `False`, `1/1` rồi `2/3` ⇒ `True` — dòng thứ hai không được canh; lặp
  13:31:15Z 23-10-2026 trên `1d7e642`: y hệt), hoặc dòng duy nhất là `0/0` hay `N/M` với N khác M: qua `chay_moi` thật của
  sổ với mẫu dòng 53 @ `1d7e642` (dòng 52 @ `c522c17`) — test in `0/0` hoặc `3/4` ⇒ `CI_DANG_KY …: ĐỎ`, `do = 1`; `1/1` ⇒
  `ĐẠT`, `do = 0` (đo 13:31:15Z 23-10-2026; lịch sử 23:34:57Z 15-10-2026 y hệt). (d) CI trên PR của #752: `gate-registry` VÀ `gate-ops (ubuntu-latest)` ĐỎ
  là DỰ KIẾN, cùng một nguyên nhân (hai test sống chưa đăng ký) — `gate-ops` đỏ vì bước `ci-duong-nhanh selftest`
  (`.github/workflows/ci.yml` dòng 696–698 @ `1d7e642`, 660–662 @ `c522c17`; `if: runner.os == 'Linux'`, không `if:` theo
  `che_do`) chạy `ops/ci_duong_nhanh_test.py`, mà ca `k01_so_dang_ky_nhan_muc_da_noi` gọi `kiem()` của sổ trên cây. Đo
  13:31:29Z–13:39:44Z 23-10-2026 trên bản sao `c3f6f5f` (= `1d7e642` + ba tệp đặc tả), cùng bốn trạng thái của mục "Đường
  land", lệnh `python3 -B ops/ci_duong_nhanh_test.py`, mỗi trạng thái khoảng 2 phút: S0 ⇒ rc 0, `CA: 104/104`,
  `DOT BIEN: 384/384`, `TONG: DAT`; S1 (bốn tệp giả, không mục `MOI`) ⇒ rc 1, đúng một dòng `[DO] k01_…` (hai dòng `test
  sống chưa đăng ký` trong lời báo), `CA: 103/104`, `DOT BIEN: 383/384`, `TONG: DO`; S2 (thêm hai mục `MOI`) ⇒ rc 0,
  `CA: 104/104`, `DOT BIEN: 384/384`, `TONG: DAT`; S3 ⇒ rc 1, đúng một dòng `[DO] k01_…`, `CA: 103/104`,
  `DOT BIEN: 383/384`. Lịch sử 02:18Z–02:23Z 16-10-2026 trên `c522c17`: S1 `103/104` · `382/383`, S2 `104/104` ·
  `383/383` — tức sau #748 chỉ tổng đột biến trôi (383 → 384), cấu trúc đỏ/xanh giữ nguyên; C8 của
  `ops/specs/no-p3-dang-ky-ci-r2.md` phải mang cùng số mới (dòng 141 @ `6c2fe9b` ghi `CA: 104/104`, `DOT BIEN: 384/384`
  cho head gộp, đo 13:55:03Z 23-10-2026; tệp đang được vá song song nên đối chiếu lại lúc cấp). ĐỎ (tiêu chí trượt) khi `ci_duong_nhanh_test.py` ra số
  ca đỏ khác 1 hoặc ca đỏ khác `k01`. Required check của `master` (đo 13:31:58Z 23-10-2026): endpoint branch protection
  vẫn HTTP 403 `Resource not accessible by integration`, nhưng `gh api repos/ducthangho/tra-luat/rules/branches/master`
  trả ruleset `20856202` với `required_status_checks` = `gate (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)`,
  `gate-ops (ubuntu-latest)`, `gate-cong-cu-gop (ubuntu-latest)` (mục cuối liệt kê hai lần) — `gate-ops (ubuntu-latest)`
  BẮT BUỘC, `gate-registry` KHÔNG; đường A không đưa head #752 vào `master` một mình nên không dựa vào điều ấy. Job khác: KHÔNG ĐO ĐƯỢC ngoài GitHub Actions, ghi run id lúc thi hành; một job đỏ
  ngoài hai job này là chưa dự kiến. Cổng xanh toàn phần đo trên head gộp, thuộc nghiệm thu C1, C6 và C8
  của #763.
- **B7 (`--root` sai, cả hai công cụ):** `--root` trỏ (i) đường không tồn tại, (ii) một tệp, (iii) thư mục rỗng ⇒ rc 2
  và không in dòng đếm nào, ở cả `kiem_ho_so_land.py` lẫn `kiem_nhan_hint.py`. ĐỎ khi: đột biến bỏ kiểm `--root` ⇒ ca
  (iii) không còn rc 2 (công cụ HINT ra rc 0 với 0 tệp; công cụ land ra rc khác 2) ⇒ ĐỎ.

## Ngoài phạm vi (cố ý)

- Đăng ký hai test vào `.claude/dev/ci_dang_ky_test.py` — packet #763.
- Gắn hai công cụ vào `.github/workflows/ci.yml` (thuộc write set #748) — ghi nợ cho packet sau #748.
- Sửa `pr672-wp574` hay bất kỳ tệp HINT nào (bản sao nguyên byte; trên `1d7e642` 35/36 tệp thiếu nhãn có băm trong kho,
  1 không — "Số đo nền").
- Sửa bất kỳ hồ sơ land nào, kể cả các tệp `F` của B3 (finding dữ liệu: báo và ghi nợ, không sửa — B3).
- Nhận dạng miễn trừ do CHÍNH hồ sơ khai (ví dụ `authorization_url: KHONG_AP_DUNG` kèm `authorization_ghi_chu`, có ở hai
  hồ sơ mới trên `8324567`, minh hoạ ở B3): L-6 không biết dạng ấy, nên hồ sơ như vậy mà `landed: true` thì là `F`.
  Có nhận dạng nó hay không là quyết định thiết kế của chủ kho, không phải của r4.
- Ghi cờ "không đủ điều kiện" vào biên nhận từng lượt.
- Ghim miễn trừ theo lý do trượt (hoặc sha256 tệp) thay vì đường dẫn: chỗ hở G2 của review lượt 1 (tệp miễn trừ đổi
  sang lỗi KHÁC vẫn `MIEN_TRU`; tệp đã sửa đúng ⇒ `DAT` mà không cảnh báo mục thừa). Lựa chọn thiết kế chờ chủ kho.

## Hình dạng kế thừa

`khong_ap_dung` (công cụ mới). Hình dạng có thể tái phát: **bộ lọc theo danh sách đoán trước mù đúng chỗ** (CLAUDE.md,
"Quét secrets: lọc theo PHẦN MỞ RỘNG") — đo 13:28:09Z 23-10-2026 trên `1d7e642`: 81 tệp `.patch`/`.diff` dưới `ops/`,
17 không khớp glob `ops/reviews/**/*HINT.patch` — mười tệp đã có ở `c522c17` (ba `*HINT-sanpham.diff`, `HINT-543-luot1.patch`,
`ci-g5-cong-cu-chia-manh-r1-review-20-claude-goi-y-F45.patch`, bốn tệp `land-doc-receipt-thu-hoi-c1a1a/luot{4,5,6,8}-*`,
`billing.diff`) cộng bảy tệp mới (sáu tệp dưới `ops/reviews/wp773-r1-g1-exec-review-{6,7,8,9}-codex/evidence/`, và
`ops/specs/WINDOWS-BASH-NEN-ESCAPE-r1.patch`) — cộng 2 tệp `hint*.json` (không đổi); lịch sử 23:33:02Z 15-10-2026 trên
`c522c17`: 65 · 10 · 2. Packet CỐ Ý chỉ phủ
`*HINT.patch` và cả hai công cụ in phạm vi glob ở cả đầu ra chữ lẫn JSON (B3, B5 đo cả hai).

## Chưa đo được

- Neo GitHub của đường land A: chủ kho chọn A trong phiên điều phối (2026-10-16), nhưng chưa có comment cấp lease nào nhắc lại — chưa tồn tại lúc soạn; [comment chủ kho 23-10-2026](https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792) không nhắc A; đo lại lúc cấp (điều kiện (1) của `depends_on`).
- Khối `nang_tran`: quyết định ĐÃ CÓ và đã đọc ngược (13:54:41Z 23-10-2026, mục `nang_tran`); numstat thật CHƯA có vì
  mã chưa có — đo trước review và so với `tran_moi` (điều kiện (4) của `depends_on`).
- #748: điều kiện (3) ĐÃ ĐO theo nghĩa chủ kho chốt (merge vào `master`, không đòi `landed: true`); kết cục của lát
  `wp748-r24` vẫn chưa biết (13:55:03Z 23-10-2026: nhánh ở `77ec458`, chưa vào `master`) nhưng không còn chặn gì — B3 là
  vị từ, lát ấy đổi số minh hoạ và hạ `pr672` về `landed: false` (đo 16:58Z 23-10-2026), nên B2 dựng tệp `pr672` thay vì
  chép tệp sống.
- Tập `F` của B3 tại `base_sha` của lease thực thi: chưa biết vì lease chưa cấp; số trên `1d7e642` và `8324567` chỉ là
  minh hoạ.
- Required check của nhánh đích KHÁC `master` (nhánh tích hợp của đường A): chưa đo. Của `master` đã đo (B6 d); trước đó
  (15-10-2026) chỉ hỏi endpoint branch protection, trả HTTP 403 — nay endpoint ấy vẫn 403, đường đo được là endpoint
  rules của nhánh.
- Hồ sơ land trên nhánh `ops/**` chưa vào `master`: công cụ chỉ quét cây được chỉ định.
- CI thật (B6 d), `ci_dang_ky_test.py --chay` đầy đủ, và đường Windows: không chạy ở phiên soạn r3, cũng không ở lượt
  đo lại nền 23-10-2026, cũng không ở lượt soạn r4. Viết test không
  phụ thuộc nền: khoá miễn trừ so bằng `as_posix()`, fixture ghi `encoding="utf-8"` với `newline` ép về LF.
- Câu trích của comment `r4231959151`, mục 6 sổ nợ, Q4/Q7/Q9 của chủ kho: không có bản trong kho.
- Mọi phép đo đột biến ở B1/B1b/B1c/B2b/B3/B4 chạy trên BẢN THAM CHIẾU của reviewer (ngoài kho), không trên mã thật — mã thật
  chưa có; executor phải chạy lại cùng các đột biến trên mã của mình. Lượt đo lại nền 23-10-2026 KHÔNG chạy lại các đột
  biến ấy (bản tham chiếu không có trong kho); chúng dựng trên cây tạm nên không phụ thuộc nền, trừ phần số tệp của B2b/B3
  đã đo lại bằng script ở "Số đo nền". Bốn vế (i)–(iv) của B3, B2 và các đột biến kèm theo đã chạy trên bản tham chiếu
  của reviewer (lượt 7: 15:36Z–15:44Z; lượt 8: 16:50Z–17:14Z, 23-10-2026; ngoài kho), CHƯA chạy trên mã của executor; vế token
  của B5 và các đột biến kèm theo CHƯA chạy trên mã nào; lượt soạn r4 chỉ chạy phép đo độc lập trên cây thật (số minh hoạ ở B3, B5) và đo màu "chưa làm" trên nền.

## Đo lại nền sau #748 land (nền 1d7e642)

Chỉ thị: chủ kho duyệt đổi nền từ `c522c17` sang `1d7e642092fb3dda15967be44d095f37bb22ac5f` sau khi #748 land (chuyển qua
phiên điều phối, 23-10-2026), đo lại mọi số phụ thuộc nền. Đo 12:54Z–13:39:44Z 23-10-2026 (UTC) trên: (i) bản sao
`git clone` của worktree đặc tả, checkout `c3f6f5f` (= `1d7e642` + ba tệp `ops/specs/*.md`), mỗi trạng thái S0–S3 một bản
sao riêng, dựng đúng chữ đặc tả (hai công cụ rỗng, hai test in `1/1`, hai mục `MOI` chép nguyên dòng 53 rồi chỉ thay
khoá); (ii) cây `git archive` của `c522c17` và `1d7e642` cho "Số đo nền"; (iii) một clone fetch mọi nhánh từ GitHub cho
`depends_on` (2) và ba phép đo của ADR-0053. Môi trường: Python 3.11.15, PyYAML 6.0.1, git 2.43.0, `ruff` 0.15.8,
`PYTHONDONTWRITEBYTECODE=1`, `python3 -B`. Các mục lịch sử ("Thay đổi so với r2", "Vá sau review lượt 3/4/5") giữ nguyên
số của thời điểm ấy; lượt đo lại này không sửa chúng.

| chỗ | cũ (`c522c17`, 15/16-10-2026) | mới (`1d7e642`, 23-10-2026) | đơn vị |
|---|---|---|---|
| `base` | `c522c17` (lặp `9fddb1d`) | `1d7e642` (`ls-remote` 12:57:25Z, 13:34:38Z) | commit |
| nhánh máy chủ, `depends_on` (2) | 541 | 561 (13:24:28Z–13:26:25Z; `comm -3` 0 dòng) | nhánh |
| `ai-dang-giu` bốn đường dẫn | `NGƯỜI_GIỮ 0` ×4, rc 0 | `NGƯỜI_GIỮ 0` ×4, rc 0 (hai lượt trước rc 12 vì nhánh mới) | đường dẫn |
| trần `sensitive` | ADR-0044 dòng 5: ≤ 3 / ≤ 300; vượt cả hai vế | ADR-0053 dòng 6: ≤ 6 / ≤ 450 qua dòng khai; đạt vế tệp, vượt vế dòng theo ước | tệp / dòng thêm |
| đề xuất nâng | ngoại lệ 4 / 1.000, nâng cả hai vế | khối `nang_tran`, `tran_moi` 4 / 1.000, chỉ vế dòng nâng | tệp / dòng thêm |
| `grep -c -F` cưỡng chế trần | `numstat`, `ADR-0044` trên hai tệp: 0 ×4 | `lease_publish.py` 4 chuỗi: 0; `packet_loop.py`: 0 ×3, `nang_tran` 10 (trục vòng và lời gọi) | dòng khớp |
| PROTOCOL | 156 · 347–351 · 355 · 612 · 621 · 644–645 · 721 · 724–726 · 730 | 156 · 351–355 · 359 · 617 · 626 · 651–652 · 729 · 732–734 · 739 | số dòng |
| `ops/reviews/README.md`, `4231959151` | 657 | 657 | số dòng |
| sổ: `tim()` · `kiem()` · mẫu `nhanh` | 83 · 582–584 · 52 | 104 · 643–645 · 53 | số dòng |
| `ci.yml`: `test registry` · `ci-duong-nhanh selftest` · `pull_request:` | 889–895 · 660–662 · 13 | 1000–1008 · 696–698 · 13 | số dòng |
| S0 | `23/23`, `1025/1025` | `24/24`, `1064/1064` | tệp / mục; ca phản chứng |
| S1 = B6(a) | `25/23`, 2 dòng `ĐỎ:` | `26/24`, 2 dòng `ĐỎ:` | tệp / mục |
| S2 | `25/25`, `1025/1025`, numstat `2 0` | `26/26`, `1064/1064`, numstat `2 0` | tệp / mục |
| S3 | `23/25` | `24/26` | tệp / mục |
| B6(a), thêm test lạ thứ ba | `26/23`, 3 dòng `ĐỎ:` | `27/24`, 3 dòng `ĐỎ:` | tệp / mục |
| `ci_duong_nhanh_test.py` S0 · S1 · S2 · S3 | — · `103/104` `382/383` · `104/104` `383/383` · `103/104` `382/383` (C8 của #763) | `104/104` `384/384` · `103/104` `383/384` · `104/104` `384/384` · `103/104` `383/384` | ca; đột biến |
| hồ sơ land | 27 tệp; 14 `landed`; 16 `trang_thai_packet` | 51 tệp; 29 `landed`; 40 `trang_thai_packet` | tệp |
| L-6 | 13 `DAT` · 1 trượt (miễn trừ) · 13 `BO_QUA` = 11 + 2 | 16 `DAT` · 13 trượt (1 miễn trừ + 12) · 22 `BO_QUA` = 11 + 11 | tệp |
| B3 đích | rc 0, `13/14` + 1 `MIEN_TRU`, `len(tep)` 27 | đo ra rc 1, `16/29`, 12 `TRUOT`, 1 `MIEN_TRU`, `len(tep)` 51 — ĐỔI Ý NGHĨA | tệp |
| B2b: `*.yaml` · đệ quy | 28 · 27 | 52 · 51 | tệp |
| `pr759` thành `true` | `14/15` | `17/30` | tệp |
| HINT: tổng · `CO_NHAN`/thiếu/`RONG`/không đọc | 55 · 18/35/2/0 | 64 · 26/36/2/0 | tệp |
| thiếu nhãn: không nhãn + bỏ dấu | 26 + 9 | 27 + 9 | tệp |
| băm của tệp thiếu nhãn: biên nhận + VERDICT + không ở đâu | 29 + 6 + 0, trong 276 biên nhận | 29 + 6 + **1**, trong 281 biên nhận | tệp |
| L-5, tệp có nhãn chứa ` commit` | 18/18 | 26/26 | tệp |
| "Hình dạng kế thừa": `.patch`/`.diff` · không khớp · `hint*.json` | 65 · 10 · 2 | 81 · 17 · 2 | tệp |
| `ruff` máy đo · CI ghim | 0.15.8 · 0.15.15 | 0.15.8 · 0.15.15 | phiên bản |
| B6(c): dòng khớp đầu tiên · `chay_moi` `0/0` `3/4` `1/1` | `False`/`True` · `do` 1, 1, 0 | y hệt | — |
| #748 | Issue `open` (23:27:59Z 15-10) | `closed`/`completed` 2026-10-20T01:19:38Z; 4 merge; 4 hồ sơ `landed: false`; lát `wp748-r24` đang chạy | — |
| required check `master` | 403, KHÔNG ĐO ĐƯỢC | ruleset `20856202`: `gate-ops (ubuntu-latest)` bắt buộc, `gate-registry` không | context |

**Đổi Ý NGHĨA, không chỉ đổi số** (báo lại cho chủ kho lúc đo, khi tệp còn mang tên r3 — bản ấy không tự thiết kế lại; kết
cục ở r4 ghi sau dấu ⇒, theo [comment chủ kho 23-10-2026](https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792)):

1. B3: vế rc 0 không đạt được trên `1d7e642` (12 hồ sơ mới trượt mệnh đề mảnh URL), và vế ĐỎ "gỡ miễn trừ ⇒ rc 1" mất
   răng; nếu `wp748-r24` land thì rc 0 trở lại nhưng `MIEN_TRU` về 0 và vế ấy vẫn mất răng. ⇒ r4: B3 viết theo vị từ
   (mục 3 của comment); 12 hồ sơ ấy là `F`, finding dữ liệu; vế "gỡ miễn trừ" rời B3, răng nằm ở đột biến công cụ và ca
   đỏ thật trên cây `1d7e642`.
2. Trần: `ADR-0053` thay cặp số `sensitive`; #752 hết vượt vế tệp, chỉ còn vượt vế dòng theo ƯỚC; bản tham chiếu gọn
   nhất (4 tệp, 350 dòng) nay nằm trong trần, nên câu "không thi hành được nếu không có ngoại lệ" hết đúng; nâng thì
   khối `nang_tran` phải vào đặc tả trước khi đóng băng — r3 chưa mang khối vì chưa có quyết định. ⇒ r4 mang khối
   (`tran_moi` ≤ 4 tệp / ≤ 1.000 dòng thêm).
3. HINT: một tệp thiếu nhãn không có băm ở đâu trong kho; phạm vi "không sửa tệp HINT nào" giữ nguyên. ⇒ r4 không đổi.
4. `depends_on` (3): #748 đã merge và Issue đã đóng, nhưng cả bốn hồ sơ land của nó `landed: false` và lát `wp748-r24`
   đổi đầu vào của B3 — chủ kho đã duyệt đổi nền, r3 ghi dữ kiện, không tự kết luận thêm. ⇒ r4: merge là đủ (mục 1 của
   comment); đổi nền là revision mới (mục 2).
5. Required check của `master` đo được: `gate-ops (ubuntu-latest)` bắt buộc; đường A không đổi. ⇒ r4 không đổi.

## Vá sau review lượt 7

Bản trước vá: commit `7b03c0c`, sha256 `ac0d966da1c3d608ed429e4d377c68a94aefe2ecc3870f400f995a28dd854afb` (`git show 7b03c0c:ops/specs/no-p3-cong-cu-ho-so-r4.md` ra đúng băm này).
Review lượt 7 (`changes_requested, 0 P1 · 2 P2 · 4 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `fe19221024f66cc9726c65e01049ec486571ac1d`; VERDICT sha256 `eb05eef9796fbf198b93848bcc9cd36ee6dd804f6912c50a8a19b7d7b5a795ab`, HINT sha256 `18a715adb291ad66ee5ef4f404cf0a529e17d170a2396bc3f034aa0900bdf0cd`; hai tệp KHÔNG có trong kho — đo 2026-10-23 ở
`7b03c0c`: 0 trên 5052 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (10 dòng thêm tay, đo bằng `diff` bản đã áp HINT với bản này: một dòng trống ngăn cách đứng trước tiêu đề, cộng 9 dòng của chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm 9 dòng: `awk '/^## /{f=($0=="## Vá sau review lượt 7")} f' <tệp spec> | wc -l` ra `9`). 6 lớp:
`b3-vi-tu-khong-ghim-hang-mien-tru-nen-rang-o-b2-khong-duoc-chung-minh` · `nang-tran-can-cu-them-so-ngoai-comment-nen-dieu-kien-khop-tung-so-khong-thoa` · `b3-so-len-tep-52-khac-51-khong-phai-cua-ve-ii` · `b3-bo-dem-va-ly-do-khong-doi-chieu-phep-do-doc-lap` · `b3-cum-trich-va-cot-can-cu-rong-hon-comment-muc-3` · `trich-dan-bam-commit-thieu-chinh-xac-97f818b-va-bam-than-comment`.

## Vá sau review lượt 8

Bản trước vá: commit `3d9f4f9`, sha256 `782bde1395de1fa284428bb99e684d391c7256d31c1899aa973a63b550253e4c` (`git show 3d9f4f9:ops/specs/no-p3-cong-cu-ho-so-r4.md` ra đúng băm này).
Review lượt 8 (`changes_requested, 0 P1 · 1 P2 · 3 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `a578f6541d980ff1c29371f0a5c980b46fe8a9b5`; VERDICT sha256 `6ddd85dd36aefa7f69451635b4e94f86fc0895808440a00c1c73a1c213a39633`, HINT sha256 `beb2104a42ba4f91dd425d4b22b3880315fc03f0d0597f22eb5d4cc75bfabbcb`; hai tệp KHÔNG có trong kho — đo 2026-10-24 ở
`3d9f4f9`: 0 trên 5052 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); ngoài HINT chỉ sửa tay hai chỗ — dòng 16 và dòng 197 đổi `mục cuối` thành tên mục "Đo lại nền sau #748 land (nền 1d7e642)" (cùng lớp `muc-cuoi-tro-nham-sau-khi-luot-14-them-muc-cuoi` của #763 lượt 15, áp sang tệp này) — và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 8")} f' <tệp spec> | wc -l` ra `9`). 4 lớp:
`b2-ban-sao-pr672-nguyen-byte-khong-ghim-nguon-lat-r24-ha-landed-lam-ca-a-khong-dat-duoc` · `b3-ly-do-chi-chan-thieu-va-dong-mien-tru-b2-khong-xac-dinh-soat-l6-chua-phu-hai-tieu-chi-chuoi-moi` · `trich-dan-ngoac-kep-khong-nguyen-van-vi-tu-khong-so-cung-va-752-land-truoc` · `loi-khai-tuyet-doi-ve-viec-da-lam-rong-hon-phep-do-chi-doi-9-dong-khong-ten-tep-nao`.

