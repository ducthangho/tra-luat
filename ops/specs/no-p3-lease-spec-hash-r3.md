# Đặc tả packet `no-p3-lease-spec-hash` r3 — nợ P3 (b1): `lease_publish.py check` đối chiếu băm spec và write set

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-lease-spec-hash` |
| `packet_issue` | #751 (`gh api repos/ducthangho/tra-luat/issues/751` lúc 23:57:40Z 15-10-2026: `open`, `updated_at 2026-10-15T05:52:49Z`). |
| `revision` | 3 |
| `thay_the_cho` | **r2**: `ops/specs/no-p3-lease-spec-hash-r2.md`, sha256 `8f700b06b28e4c02c615b591b02a75a2fd901239746eb2a3fb8389dd9f549ec4`, blob `3a708be2867bab1e14e93dab07f0711479e8b867`, commit thêm `a9ef33c24665dedc70f2c839e2357353bd4054af`; vào `master` qua PR #762 (merge vào `master` là `c522c17`; `207250f` là merge vào nhánh của PR, không nằm trên first-parent của `master`) CHỈ ĐỂ LƯU VẾT (nợ `SPEC-R2-751-752-KHONG-DUOC-CAP-LEASE`, hàng dưới). r2 thay r1 (sha256 `17df1dccb4df520acb0d525cfc091dbee07fc8d878cf63f2fe2a4874a1a2fc6c`, commit `55bd0d24`). Thứ định danh r1, r2 là băm, không phải tên nhánh hay vị trí tệp. r3 không sửa byte nào của r1, r2 (đóng băng); mọi closure, lease và `spec_hash` từ nay neo **r3**. |
| review của r2 | **Lượt 2** (hẹp), reviewer Claude Sonnet 5.5 chạy bằng subagent (tự khai): `verdict: approve`, `reviewed_sha` `a9ef33c24665dedc70f2c839e2357353bd4054af`, `spec_sha256` `8f700b06…549ec4`, **0 P1 · 0 P2 · 8 P3**; 11 lớp của lượt 1 ĐÃ ĐÓNG. `VERDICT.md` sha256 `fcb545136985a89e6711f37dd3f4e3c42121202f6d4c7d156b80b13604353102` (167 dòng); `HINT.patch` sha256 `f536ce126e5b1048d29f361534dd60a78c00c80d404535110f5e4126f4fab037` (11 hunk, mỗi hunk một dòng `# lop:`, chỉ văn bản đặc tả). Hai tệp KHÔNG có trong kho ở `c522c17` (`ls ops/reviews` lọc `spec-hash` ⇒ 0 dòng, 00:03:51Z 16-10); thứ định danh là băm. Cách r3 đóng từng lớp: mục **Thay đổi so với r2**. |
| finding sau review | **P2 Codex trên PR #762**: comment review `4286041913` (`pull/762#discussion_r4286041913`), `chatgpt-codex-connector[bot]`, `created_at 2026-10-15T17:13:10Z`, neo r2 dòng 231 tại `4c550bc0fcdf63d92a709d217a3da22b33938a14`, tiêu đề "Keep the documented pre-commit lease check usable" (đọc lại bằng `gh api repos/ducthangho/tra-luat/pulls/comments/4286041913` ~23:30Z). Ý: r2 bắt `check` đọc `spec_path` CHỈ từ `HEAD` đã commit và trả 13 khi spec chưa commit (r2 dòng 89–95), trong khi runbook `ops/README.md` dòng 33–44 bảo soạn lease → `check` → rồi mới commit; r2 tự nhận runbook sẽ sai mà để README nguyên. Ghi sổ thành nợ `SPEC-R2-751-752-KHONG-DUOC-CAP-LEASE` (P2, `trang_thai: mo`) ở `ops/land/pr759-no-p3-ho-so-land-evidence.yaml` dòng 407–418 tại `c522c17`: không lease nào được cấp trên r2; r3 phải xử lý finding trước khi review lại và cấp lease. r3 đóng phần #751 của nợ ấy (hàng C1); phần #752 (`discussion_r4286041896`) thuộc đặc tả khác. |
| `nguon_cap_viec` | Sổ nợ P3 mục 4: review wp685 lượt 2–5 đo `lease_publish.py check` không đọc `spec_hash`, `spec_sha256_required`, `plan_hash`, `write_set_hash`, `spec_path` (VERDICT review lượt 5 r28 sha256 `d3f1d9db4896efe8c1b62112a3d0aa479b64c5dc110da1d323b3297d7e7c45fb`, M11: đột biến D2, D3, D5, D6, D7 cho rc=0 cả năm) — **KHÔNG ĐO ĐƯỢC từ kho**: đo lại 23:50:15Z–23:50:34Z 15-10 trên 540 ref (`refs/remotes/origin/*` của bản bare đủ ref, bỏ `claude/spec-no-p3`): 0/1102 blob trong lịch sử có tên tệp chứa `verdict` (không phân biệt hoa thường) khớp băm này; 831 blob như thế ở đầu nhánh, đều thuộc tập lịch sử ấy. "Sổ nợ P3" sống ở phiên điều phối, ngoài kho. Vế "`check` không đọc các trường ấy" đo lại: `grep -cE` năm tên trong `ops/lease_publish.py` tại `c522c17` = 0 dòng (00:03:51Z 16-10). Ngưỡng chủ kho #698 `6094652521`. Phạm vi do chủ kho chốt 15-10-2026 (Q7, Q8) và quyết định 15-10 cho r2 (test mới phải đăng ký vào sổ test sống) giữ nguyên. Issue #763 (`open`, `ducthangho`, `created_at 2026-10-15T23:26:04Z`, tiêu đề "Packet NO-P3-DANG-KY-CI: đăng ký hai bộ test của #752 vào ci_dang_ky_test.py") nhận phần đăng ký của #752; phần đăng ký bộ test của #751 vẫn thuộc #751 (Mục tiêu 6). |
| `review_class` | **sensitive** — `ops/lease_publish.py` là cổng cấp lease (authority). Trần ADR-0044 dòng 5: ≤ 3 tệp, ≤ 300 dòng thêm. Đo `_tinh_lop_tu_write_set` gọi thẳng tại `c522c17` (23:49Z): từng đường dẫn của write set và cả ba cùng lúc ⇒ `sensitive` (`_BANG_LOP` mở ở dòng 59, mục `ops/lease_publish.py` ở dòng 65; hai tệp còn lại rơi về `sensitive` theo chú thích dòng 56–58); `ops/README.md` cũng ⇒ `sensitive`. |
| `executor` · `reviewer` | Claude (executor). Reviewer: lớp `sensitive` chạm security path ⇒ ADR-0036 dòng 9–10 và PROTOCOL §8 dòng 705–707 đòi **Codex cross-review hoặc `human_audited`**; `review_deferred` bị cấm, `same_provider_approved` một mình không thay được (dòng 696). Subagent Claude Sonnet chỉ là lượt PHỤ; Sonnet không nằm trong `MO_HINH_CHO_PHEP` của `.claude/dev/chon_reviewer.py` (dòng 7). Bộ chọn: `--duong-dan` nhận MỘT chuỗi phân tách bằng dấu phẩy, lặp cờ thì chỉ giá trị CUỐI được dùng — đo 23:49:48Z: lặp ba cờ ⇒ `claude-opus-5`/`xhigh`, "tổng=2", mất dòng "+2 chạm vùng cong"; dạng dấu phẩy cho ba đường dẫn ở 210, 280, 300 dòng ⇒ `claude-fable-5`/`xhigh`, "tổng=4" (23:50:09Z). Đường dự phòng khi Codex không làm mới được: `human_audited` — KHÔNG merge chỉ với Sonnet. Chỉ P1/P2 chặn merge. |
| `base` | `c522c173cb58b506bac8cffb24239e16e8459836` (merge PR #762) — nền ĐO của r3 theo chỉ thị phiên điều phối. `git ls-remote --heads origin` lúc 23:31:30Z: 541 nhánh, `master` máy chủ đã sang `9fddb1d19e8e5b753bb687673846d484fb710182` (merge PR #755); `git diff --stat c522c17 9fddb1d` = 1 tệp `ops/specs/wp728-do-linux-doc-lap-wp710-r2.md` +246, không chạm write set hay bộ đo nền nào. Từ `6f121a3` (nền r2) tới `c522c17`: 17 commit, 87 tệp, toàn `ops/**`; diff trên ba tệp write set, ba bộ đo nền, `ops/README.md`, `ci.yml`, `ops-publish-lease.yml`, `ops/ci_duong_nhanh.py`, cùng `docs/`, `.claude/`, `.github/` = 0 dòng ⇒ mọi số dòng mã r2 dẫn vẫn đúng tại `c522c17`. #748 CHƯA land: mọi số đo nền phải ĐO LẠI sau khi #748 land (L5 của `.claude/skills/soan-spec/SKILL.md`, `depends_on` (3), A0); không lease nào được cấp trước đó. |
| `write_set` | `ops/lease_publish.py` · `ops/lease_publish_spec_hash_test.py` (MỚI) · `.claude/dev/ci_dang_ky_test.py` (+1 dòng `MOI`, Mục tiêu 6) — giữ nguyên ba tệp của r2. `ops/README.md` KHÔNG vào: thiết kế r3 giữ runbook đúng (hàng C1). Đường dự phòng "đưa README vào write set" sẽ là tệp THỨ TƯ, vượt trần sensitive 3 tệp ⇒ cần ngoại lệ trần của chủ kho hoặc tách phần đăng ký; thiết kế r3 tránh được cả hai. |
| `depends_on` | **CHẶN cấp lease** cho tới khi ĐỦ năm điều kiện, đo lại lúc cấp (số trong ô này không thay được phép đo lúc cấp). **(1)** #748 đã land vào `master` — không chỉ vào `mission/748/integration`. Đo 23:31:42Z: CHƯA (`c522c17..origin/master` = 7 commit, toàn spec wp728; Issue #748 `open` lúc 23:57:40Z). **(2)** Trên một clone ĐỦ ref — so `git ls-remote --heads origin` với `git for-each-ref refs/remotes/origin` (bỏ `HEAD`) theo tập tên VÀ OID: thiếu 0, lệch 0; không chạy được ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp — `python ops/lease_publish.py ai-dang-giu <đường dẫn>` ra `NGƯỜI_GIỮ 0`, rc 0, cho từng đường dẫn của write set. Đo 23:32:15Z–23:33:09Z trên bản bare đủ ref (thiếu 0, thừa 0, OID khớp, 541 nhánh): `ops/lease_publish.py` 0 rc 0; `ops/lease_publish_spec_hash_test.py` 0 rc 0; `.claude/dev/ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 1: wp748-r11-g11-claude-windows-20261015`, **rc 11** — lease r11 của #748 (nhánh `ops/wp748-r11-g11-lease` @ `181e3fbd`, hạn `2026-10-16T04:27:21Z`, write set 11 đường dẫn gồm `ops/lease_publish_test.py`, `.claude/dev/ci_dang_ky_test.py`, `ops/ci_duong_nhanh_test.py`, `.github/workflows/ci.yml`; `spec_path ops/specs/wp748-windows-gates-r11.md`; `thay_the_cho` r10). Kho cục bộ `/home/user/tra-luat` lúc 23:31:30Z thiếu 4 nhánh (trong đó `ops/wp748-r11-g11-lease`) và lệch OID 3 nhánh (trong đó `master`, `ops/wp748-r10-g10-lease`) so với máy chủ — đo trên bộ đệm ấy là mù đúng lease đang giữ. **(3)** Nếu bất kỳ commit nào sau `c522c17` trên `master` đổi một tệp của write set hoặc một bộ đo nền (`ops/lease_publish_test.py`, `ops/ci_duong_nhanh_test.py`, `.claude/dev/ci_dang_ky_test.py`) ⇒ dời nền bằng revision mới và đo lại mọi số ở Số đo nền TRƯỚC khi cấp; không cấp trên nền `c522c17`. Lease r11 của #748 khai cả ba bộ ấy ⇒ gần như chắc phải dời nền. **(4)** Write set giao với #763 (`no-p3-dang-ky-ci`) ở `.claude/dev/ci_dang_ky_test.py` ⇒ hai lease KHÔNG được đồng thời; packet land sau phải qua (3). Nếu #763 land trước, N của A7 đổi (bản nháp #763 khai +2 dòng `MOI`: 23 ⇒ 25, đích của #751 thành `26/26`). Bản nháp r3 của #752 (chưa đóng băng, đọc 23:57:40Z) đã đưa sổ RA khỏi write set của nó — giao #751↔#752 ở sổ không còn, chỉ còn #751↔#763. **(5)** Có bằng chứng bền (đường dẫn comment) cho quyết định chủ kho 15-10 về sổ test sống VÀ cho đồng ý đi tiếp ở ngưỡng L4 (mục Hình dạng kế thừa). Hiện trạng: (1) chưa · (2) ĐỎ (rc 11) · (3) chờ (1) · (4) chờ · (5) chưa. |
| `kich_thuoc` | 3 tệp — **đúng trần** sensitive, dư 0 tệp. Trần cứng 300 dòng thêm theo `git diff --numstat` (ADR-0044 dòng 5). Đo bản THĂM DÒ của lượt soạn r3 (KHÔNG giao; dựng từ chữ Mục tiêu 1–3, 5 lên bản sao `c522c17`, 23:35Z): `ops/lease_publish.py` +54/−0, 5 hunk (`-25,0 +26` · `-52,0 +54` · `-1116,0 +1119,49` · `-2294,0 +2346` · `-2305,0 +2358,2`), chưa gồm sửa chú thích dòng 2313 (ước +1/−1) và chưa gồm sửa docstring dòng 15–16 (Mục tiêu 1, thêm sau lượt 3); `ci_dang_ky_test.py` +1/−0 (số reviewer lượt 2) ⇒ bộ test còn ≤ 244 dòng (≤ 242–243 khi tính sửa docstring dòng 15–16, đo lượt 4 dưới). r3 đòi **40 ca** (A1 1 · A2 5 · A2b 3 · A3 5 · A3b 3 · A3c 2 · A4 6 · A4b 9 · A5 4 · A5b 2). Viết tay từng ca KHÔNG vừa (reviewer lượt 2: 27 ca viết tay = 461 dòng ⇒ 52 + 1 + 461 = 514 > 300) ⇒ bộ test PHẢI dạng bảng: một hàm dựng kho, một hàm chạy `check`, một bảng ca. Số "24 ca dạng bảng = 144 dòng" là của reviewer lượt 1, không tái lập. Đo lượt 3 (16-10-2026, cửa sổ 02:12Z–02:55Z; bản dựng KHÔNG giao): đúng 40 ca dạng bảng viết dày = 239 dòng (241 khi thêm dòng BỎ QUA CÓ TÊN trên `nt` mà Mục tiêu 4 đòi) ⇒ `git diff --numstat` +56/−1 (kể cả sửa chú thích dòng 2313) · +239/−0 · +1/−0 = 296 (298) dòng thêm, CHƯA gồm sửa docstring dòng 15–16; đo lượt 4 (16-10-2026, bản thăm dò lượt 4 KHÔNG giao, trên `ops/lease_publish.py` nền): sửa docstring ấy thêm +1/−1 và một hunk khi nối vào dòng 16, hoặc +2/−1 và một hunk khi bọc dòng ⇒ 297–298 (299–300) dòng thêm ≤ 300, dư 3–2 (1–0); cùng bộ test 239 dòng ấy qua `ruff format --line-length 100` = 374 dòng, `--line-length 88` = 428 dòng ⇒ ngân sách ≤ 244 dòng chỉ đủ khi giữ kiểu dày (mỗi ca một hàng bảng, dòng tới ~155 ký tự; nền, dòng dài nhất tính bằng KÝ TỰ: `lease_publish.py` 161, `lease_publish_test.py` 248 — tính bằng BYTE: 174 và 270; đo lượt 4, 16-10-2026, `c522c17`); executor đo `git diff --numstat` ngay khi bộ test xanh. Vượt 300 dòng thêm hoặc cần tệp thứ tư ⇒ dừng TRƯỚC review và soạn revision. |

## Thay đổi so với r2

r3 viết lại từ r2 (không áp `HINT.patch` máy móc: 3/11 hunk được viết cho thiết kế đọc `HEAD` của r2 và sai với thiết kế r3 — xem bảng thứ hai). Mọi con số mới đều đo lại trên `c522c17` hoặc bản sao của nó, kèm thời điểm (giờ UTC, ngày 15-10-2026 trừ chỗ ghi 16-10); số nào không đo lại thì ghi rõ là số của reviewer.

| # | nguồn · hạng | id lớp | chỗ sửa trong r3 |
|---|---|---|---|
| C1 | Codex PR #762 · P2 | `discussion_r4286041913` "Keep the documented pre-commit lease check usable" | Mục tiêu 1 (luật NGUỒN: spec đọc từ ĐĨA dưới `_goc_kho(tep, goc)`, cùng nguồn với tệp lease và `prompt_path` trong `check`; bỏ đọc `HEAD`); Số đo nền (phép đo hành vi nguồn đọc của `check`); A3 viết lại (5 ca, đột biến "đọc `HEAD`" làm đỏ cả năm); A3c mới (đúng trình tự runbook tới đường đăng); hàng `write_set` (README không vào, lý do); Ngoài phạm vi. |
| B1 | lượt 2 · P3 | `a5b-chuoi-bia-mo-lech-muc-tieu-5` | Mục tiêu 5: chuỗi `đã bị thay thế — bia mộ — không kiểm băm`; A5b đo chuỗi con `bia mộ — không kiểm băm`. |
| B2 | lượt 2 · P3 | `hermetic-thieu-cau-hinh-git-cuc-bo` | Mục tiêu 4 (cấu hình git cục bộ, cô lập cấu hình toàn cục, mọi `git clone` kèm `-c core.autocrlf=false`); lý do đo lại dưới thiết kế đĩa (bảng thứ hai, hàng c). |
| B3 | lượt 2 · P3 | `dong-cuoi-bo-test-phai-la-N-tren-N-mot-minh` | Mục tiêu 4 (dòng `N/N` đứng một mình là dòng DUY NHẤT có dạng số/số, và là dòng cuối — hàng g); A7 (phép `chay_moi`). |
| B4 | lượt 2 · P3 | `yeu-cau-muc-tieu-1-chua-co-tieu-chi-do` | Mỗi yêu cầu mà lượt 2 liệt kê (tám đột biến sống sót bộ A của r2) có một ca và một đột biến: A1 (dòng "ĐĂNG ĐƯỢC" và băm 12 ký tự); A2 (thông điệp lệch nêu trường · giá trị khai · giá trị đo; rc 13 KHÔNG kèm "ĐĂNG ĐƯỢC"; thông điệp tệp vắng); A2b (iii) và A4b (thông điệp "64 ký tự hex thường"); A4 (dòng bằng chứng write set; phần tử không phải chuỗi); A5 (ca 3, 4: `spec_path` không băm, `spec_hash: null`). Các yêu cầu khác của Mục tiêu 1–6 CHƯA có ca nào: sáu do lượt 3 đo, năm nhóm do lượt 4 đo, năm nhóm do lượt 5 đo (mục Chưa đo được) — danh sách các nhóm ĐÃ ĐO THẤY, KHÔNG phải tập đóng. |
| B5 | lượt 2 · P3 | `kich-thuoc-viet-tay-15-ca-thieu-so-voi-26-ca` | Hàng `kich_thuoc` (đếm 40 ca của r3, đo bản thăm dò +54, buộc dạng bảng). |
| B6 | lượt 2 · P3 | `a6-so-tuyet-doi-phu-thuoc-so-ref-cua-clone` | A6 (i): tiêu chí là TẬP lease đổi rc; số tuyệt đối đo lại trên `c522c17` kèm điều kiện ref (542 ref cục bộ). |
| B7 | lượt 2 · P3 | `luat-hai-truong-chua-nhat-quan-fixture-va-dang-sai` | Mục tiêu 1 (kiểm DẠNG mọi trường băm có mặt TRƯỚC khi chọn trường quyết định); A2 (tiền đề fixture: lease CHỈ mang trường được sửa); A2b (iii) mới. |
| B8 | lượt 2 · P3 | `chu-thich-check-thuan-va-body-cung-cong-se-sai` | Mục tiêu 1 (chú thích dòng 2313 PHẢI sửa; dòng 2295–2296 nay GIỮ ĐÚNG vì `check` vẫn không chạm git — đo, hàng b); A3 (v) khoá "check THUẦN"; A6b khoá chú thích. |
| G1 | lượt 2 · ghi nhận IV.2 | lời dẫn `depends_on` (4) trỏ r1 của #752 | `depends_on` (4) viết lại: giao nay là #751↔#763. |
| G2 | lượt 2 · ghi nhận IV.3 | trôi ảnh chụp ref (12 → 13 blob hai trường) | Mọi số trên toàn ref đo lại trên bản bare đủ ref, so tên + OID với `ls-remote` trước khi đo (17 blob hai trường, 15 bằng, 2 khác). |
| G3 | lượt 2 · ghi nhận IV.4 | nền sẽ phải dời | Hàng `base`, `depends_on` (3), A0. |
| G4 | lượt 2 · ghi nhận IV.5 | `spec_hash` không kèm `spec_path` (15/612 blob) | Mục tiêu 1: thông điệp "spec: không khai — không kiểm" giữ, chấp nhận như lease cũ (15/619 blob đo lại). |
| G5 | lượt 2 · ghi nhận IV.1 | trần ADR-0044 chờ chủ kho | Hàng `kich_thuoc`; không đổi trần. |

Lệch `HINT.patch` lượt 2, hoặc ngoài HINT:

| hàng | chỗ | vì sao |
|---|---|---|
| (a) | A2 ca 4, Mục tiêu 1 | Hunk `@@ -180` của B4 đòi thông điệp tệp vắng nêu "đã commit tại HEAD" — đúng cho r2, SAI cho r3. Thông điệp r3: "không có tệp … spec phải nằm trong cây cùng lease" (bản thăm dò in đúng như vậy, 23:37:35Z). |
| (b) | Mục tiêu 1, B8 | Hunk `@@ -110` khai HAI chú thích thành sai. Dưới thiết kế r3 chỉ dòng 2313 thành sai; dòng 2295–2296 ("bộ kiểm THUẦN … Chỉ khi `--du-bao` mới chạm git") vẫn đúng. Đo A/B (23:37:35Z): kho git, spec khớp, PATH trỏ thư mục rỗng ⇒ bản thăm dò ĐĨA rc 0, bản đúng chữ r2 (đọc `HEAD`) rc 12; spec lệch ⇒ `check` 13 · `body` 0 ở bản đĩa. |
| (c) | Mục tiêu 4, B2 | Lý do của hunk `@@ -127` ("`core.autocrlf=true` đổi blob CRLF thành LF ở `git add` ⇒ ca CRLF đỏ") không còn áp: ca CRLF r3 đọc ĐĨA. Nhưng cấu hình toàn cục vẫn phá bộ test qua đường khác — đo 23:52:28Z: `HOME` có `core.autocrlf=true`, `git clone` trần ⇒ spec trên đĩa của clone thành `73 70 65 63 20 41 0d 0a` ⇒ `check` 13 (ĐỎ GIẢ ở A3c); cùng clone kèm `-c core.autocrlf=false` ⇒ `73 70 65 63 20 41 0a`, rc 0. Yêu cầu hermetic giữ, lý do đổi. |
| (d) | A4b | Ca "PATH không có git ⇒ rc 12" của r2 BỎ: r3 không gọi git, ca ấy nay là A3 (v) với đáp án rc 0. Trạng thái thứ ba đổi thành "có tệp mà đọc ném `OSError` ⇒ 12" (ca trong tiến trình, chèn lỗi). |
| (e) | A4b, CRLF | Đột biến của ca CRLF đổi từ "đọc qua `GOI_GIT`/`_git`" sang "đọc văn bản" (`read_text` rồi mã hoá lại): đo 23:56:43Z ⇒ ca CRLF rc 13, ĐỎ. Đột biến "đọc blob tại `HEAD`" thuộc A3. |
| (f) | Mục tiêu 1, NUL | Cơ chế cụ thể dưới thiết kế đĩa (Python 3.11.15, đo 23:35Z): `PurePosixPath` nhận chuỗi có NUL không ném; `Path.resolve()` ném `ValueError: embedded null byte`; `Path.is_file()` trả `False`; `read_bytes()` ném `ValueError`. Nên chốt NUL đứng TRƯỚC `resolve()`; gỡ chốt ⇒ rc 1 kèm traceback (đo 23:56:43Z). |
| (g) | Mục tiêu 4, B3 | HINT nói "dòng CUỐI đúng `N/N`". Đo `bang_chung_xanh` (`.claude/dev/ci_dang_ky_test.py` dòng 616–620, `re.search` đa dòng ở dòng 617; 23:58:24Z): `1/1`, `x`, `26/27` ⇒ **True** (xanh giả: khớp dòng ĐẦU có dạng ấy); `26/27`, `27/27` ⇒ False; `a`, `27/27`, `b` ⇒ True. Nên dòng `N/N` phải là dòng DUY NHẤT có dạng số/số đứng một mình, không chỉ là dòng cuối. |
| (h) | Mục tiêu 1, chốt đường dẫn | Mới hoàn toàn: đọc đĩa biến `spec_path` (dữ liệu YAML) thành một lượt đọc hệ tệp, nên r3 thừa kế nguyên chốt của `_kiem_neo_prompt` dòng 973–996 (tuyệt đối, `..`, dấu chéo ngược, `relative_to` sau `resolve()`). Đo 23:56:43Z: gỡ chốt dạng ⇒ ba ca vẫn rc 13 nhưng sai thông điệp (đúng bài học chú thích dòng 977–979); gỡ `relative_to` ⇒ ca symlink ra ngoài kho rc 0. |
| (i) | A6 | Số tuyệt đối của hunk `@@ -190` (140/4/5 · 38/58/3, đo trên `6f121a3`) thay bằng số đo lại trên `c522c17` (Số đo nền). |
| (j) | `kich_thuoc` | Hunk `@@ -16` dẫn 26 ca; r3 đòi 40 ca và có số đo bản thăm dò (+54) thay cho +52 của reviewer. |
| (k) | A2b | Hunk `@@ -105` nói kiểm dạng mọi trường nhưng không thêm ca; r3 thêm A2b (iii), và đo: đột biến "chỉ kiểm dạng trường quyết định" ⇒ ca ấy rc 0, ĐỎ (23:56:43Z). |

## Số đo nền (base `c522c17`, 15-10-2026, giờ UTC, đơn vị ghi rõ)

- Bản sao đo: clone `--no-checkout` của kho cục bộ, `checkout --detach c522c17`, `core.abbrev 7` (23:31:11Z); bản bare đủ ref
  (`git clone --bare --reference` kho cục bộ + `fetch '+refs/heads/*:refs/remotes/origin/*'`, 23:31:42Z; so tập tên + OID với
  `ls-remote --heads`: thiếu 0, thừa 0, 541 nhánh); clone làm việc từ bản bare cho A6 (542 ref cục bộ, bỏ `HEAD`).
- Bảng mã thoát: `RC_OK 0`, `RC_THAM_SO 2`, `RC_TU_CAP 4`, `RC_NEO 6`, `RC_NOI_DUNG 8`, `RC_DA_DANG 9`, `RC_LOP 10`, `RC_DANG_GIU 11`,
  `RC_KHONG_XAC_DINH 12` (`ops/lease_publish.py` dòng 44–52, tệp không đổi từ `6f121a3`). Mã `13` chưa dùng. Docstring `MÃ THOÁT`
  dòng 18–26 thiếu 11, 12; `--help` in 0 dòng chứa `MÃ THOÁT` (00:03:51Z 16-10).
- Lease (kịch bản chỉ-đọc `m_baseline.py` của reviewer lượt 2, `python3 -B -I m_baseline.py <clone> c522c17`, 23:31:20Z): **152** tệp
  `ops/leases/*.yaml` (r2: 150; thêm `no-p3-ho-so-r2-g1-claude.yaml`, `wp741-r1-g1-claude-20261015.yaml`). **99** có `spec_path` + băm
  (8 mang cả hai trường): **94** khớp blob tại `c522c17`, **5** lệch — đúng năm lease r2 đã kể (`gate-tach-job-cat-chi-phi-exec-1`,
  `-1r2`, `-1r3` và `wp461-…-exec-1` mang `da_bi_thay_the`; `…-exec-1r4` không). **60** có `write_set` + `write_set_hash`: **6** khai
  scope `sorted NFC casefold exact …`, khớp công thức (a) 6/6; **54** không scope, khớp (a) 0/54.
- Trên toàn ref (bản bare, 540 ref bỏ `claude/spec-no-p3`; `m_both.py`, `m_unexp.py`, `m_lease_shapes.py`, 23:33:44Z–23:33:51Z): **619**
  blob lease khác nhau; **17** mang cả hai trường băm (15 bằng nhau; 2 khác nhau = `wp709-exec-g1/g2-codex`, `spec_hash f569b613…` ≠
  `spec_sha256_required f739b4aa…`); 7 blob chưa hết hạn lúc 23:33:51Z. Hình dạng: `spec_path` + `spec_hash` hex64 354 · `spec_path` không
  băm 56 ("băm" = `spec_hash` hoặc `spec_sha256_required`; `spec_sha256` không tính, xem Mục tiêu 1) · `spec_path` + `spec_sha256_required` hex64 55 · `spec_path: null` 27 · cả hai trường 17 · `spec_hash` không `spec_path` 15 ·
  `spec_hash: null` 3 — **0** blob mang băm sai dạng.
- **Nguồn đọc của `check`** (kịch bản `do_nguon.py`, kho tạm `git init` + cấu hình cục bộ, gọi `ops/lease_publish.py` của `c522c17` như
  tiến trình con, 23:34:49Z; lease có `prompt_path` + `prompt_sha256_required`): (1) lease + prompt CHƯA commit, khớp ⇒ rc 0; (2) đã commit,
  sửa prompt trên đĩa ⇒ rc 6 ("băm prompt LỆCH"); (3) `HEAD` hợp lệ, lease trên đĩa đổi `granted_by: claude` ⇒ rc 4; (4) `HEAD` mang prompt
  SAI, đĩa đúng ⇒ rc 0; (5) thư mục không có `.git`, có `--root` ⇒ rc 0; (6) PATH trỏ thư mục rỗng (không có git) ⇒ rc 0. Kết luận đo
  được: trong `check`, tệp lease (`_doc_yaml(a.tep)`, dòng 2294) và `prompt_path` (`_kiem_neo_prompt`, đọc byte dưới `_goc_kho(tep, goc)`,
  dòng 985–1001) đều đọc từ ĐĨA, không cần git.
- Hai người tiêu thụ TỰ ĐỘNG của `check` đều chạy trên cây checkout SẠCH của commit được xét, nên với họ đĩa = commit: `ops-publish-lease.yml`
  (`actions/checkout@v4`, `fetch-depth: 0`, 0 dòng `sparse`; `check "$tep" --root .` dòng 216; bộ kiểm lấy từ worktree rời của nhánh mặc
  định, dòng 82–99) và `ops/ci_duong_nhanh.py::kiem_lease` (`check duong --root .` với `cwd=kho`, dòng 541; lease hết hạn đi
  `MA_KIEM_HET_HAN` dòng 121, tức `kiem(bo_qua_han=True)`). Người tiêu thụ THỦ CÔNG (`ops/README.md` dòng 37–38) chạy `check` TRƯỚC khi commit, trên cây CHƯA sạch (đĩa ≠ commit) — đó là lý do `kiem_bam` đọc ĐĨA (luật nguồn, Mục tiêu 1).
- `.gitattributes` dòng 8: `* text=auto eol=lf`. Đo 23:52:28Z trong kho tạm chép tệp ấy: spec CRLF trên đĩa, lease neo băm byte CRLF ⇒
  `check` trước commit rc 0; sau commit, blob là `73 70 65 63 20 41 0a` ⇒ clone sạch rc 13.
- Bộ đo nền trên bản sao `c522c17`: `env -u GITHUB_ACTOR python3 -B ops/lease_publish_test.py` ⇒ `lease_publish: 265/265 đạt; đã chạy=265,
  bỏ qua=0`, rc 0 (23:31:17Z–23:37:39Z); `python3 -B .claude/dev/ci_dang_ky_test.py` (không `--chay`) ⇒ `ĐĂNG KÝ: 23/23`,
  `TRẠNG THÁI: chan=23 cach_ly=0`, `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT`, rc 0 (23:35:23Z–23:35:30Z); `python3 -B
  ops/ci_duong_nhanh_test.py` ⇒ `CA: 104/104 dat · 0 do · 0 hong`, `DOT BIEN: 383/383 bi giet dung ly do`, `TONG: DAT`, rc 0
  (23:35:36Z–23:38:12Z); `ruff check --isolated --select F` (ruff 0.15.8) trên `ops/lease_publish.py` ⇒ 2 F841 sẵn có ở dòng 198–199.
- A6 nền (kịch bản `do_a6.py`, trong tiến trình, `kiem(bo_qua_han=True)` cho 152 lease trên clone 542 ref, 23:38:49Z–23:54:26Z):
  `{rc 0: 143, rc 8: 4, rc 10: 5}`.

## Mục tiêu

1. **[`ops/lease_publish.py`] Băm spec.** Hàm MỚI `kiem_bam(lease, tep, goc) -> list[str]` đặt NGOÀI thân `kiem()`; `lenh_check` gọi nó
   ngay sau dòng `lease, neo = kiem(...)` (dòng 2294), TRƯỚC mọi `print` của lệnh, nên rc 4/6/8/10 luôn thắng và rc 13 không bao giờ đi kèm
   dòng "ĐĂNG ĐƯỢC". `kiem-github` KHÔNG gọi nó (lease đã đăng vẫn ra rc 9). `kiem()` giữ BYTE-IDENTICAL thân và chữ ký trả 2 phần tử
   (`t191` duyệt AST thân `kiem()` nhưng chỉ coi `raise Chan` và lời gọi tên `_kiem_*`/`_doc_*` là chốt (`_la_chot`, `ops/lease_publish_test.py` dòng 9541–9547), nên KHÔNG thấy `kiem_bam`; `t01` dòng 705 `checked, _ = mod.kiem(...)`; số đo của reviewer lượt 1–2 (tên `_kiem_bam_spec`): đúng chữ r1 ⇒
   263/265, đỏ đúng hai ca ấy). Người gọi `kiem()`: `check` (2294), `body` (2314), `kiem-github` (1280, 1282); không gồm
   `kiem-thu-hoi-github`. Mã của `lenh_body` và `kiem_github` không đổi.
   **Luật nguồn (đóng C1): spec đọc từ CÙNG NGUỒN với tệp lease trong từng lệnh.** `check` đọc lease từ ĐĨA (Số đo nền, ca 1–6), nên
   spec đọc từ ĐĨA: tệp `_goc_kho(tep, goc) / spec_path`, cùng gốc mà `_kiem_neo_prompt` dùng cho `prompt_path`, byte thô bằng
   `read_bytes()`, KHÔNG qua git, KHÔNG `read_text()`. Không lệnh nào của packet đọc lease từ REF rồi gọi `kiem_bam` (`kiem-github` đọc
   lease từ đĩa và không gọi; `ai-dang-giu`, `con-tro-treo`, `kiem-thu-hoi-github` đọc ref/tree nhưng không gọi `kiem()`), nên vế "đường
   đọc lease từ ref ⇒ spec từ blob cùng ref" là ràng buộc cho người gọi TƯƠNG LAI (Ngoài phạm vi), không có mã ở đây.
   Hệ quả đo được trên bản thăm dò (23:37:35Z–23:37:58Z): kho đã có `HEAD`, lease + spec MỚI chưa commit ⇒ bản đĩa rc 0, bản đúng chữ r2
   rc 13 (kho chưa commit nào: rc 12) — tức runbook `ops/README.md` dòng 37–38 (`check` trước khi commit) đúng NGUYÊN VĂN dưới r3. Chốt
   băm là ràng buộc toàn vẹn lease↔spec trong CÙNG một ảnh chụp, không phải lớp uỷ quyền: người đẩy được thì sửa được cả hai; uỷ quyền
   vẫn ở `granted_by` và `GITHUB_ACTOR` trong `kiem()`.
   Điều kiện kiểm: lease có `spec_path` (chuỗi khác rỗng) VÀ ít nhất một trường băm có mặt khác `null` trong `spec_hash`,
   `spec_sha256_required`. Thứ tự chốt, mỗi chốt ném `Chan(RC_SPEC_LECH, …)` với `RC_SPEC_LECH = 13` mới trừ chỗ ghi khác:
   (i) **DẠNG trước**: MỌI trường băm có mặt (khác `null`) phải là chuỗi 64 hex thường, kiểm cho CẢ HAI trường trước khi chọn trường
   quyết định (B7) — thông điệp nêu tên trường và "phải là 64 ký tự hex thường" như `_kiem_neo_prompt` dòng 969–971; `null` = vắng.
   Chốt (i) áp cho MỌI lease CHƯA bị thay thế (lease mang `da_bi_thay_the` đã trả ngay đầu hàm, Mục tiêu 5) có trường băm có mặt, kể cả khi thiếu `spec_path` (bản thăm dò làm vậy; 0/619 blob thật sai dạng, kể cả 15
   blob `spec_hash` không `spec_path` — đều hex64 — nên không từ chối lease nào đã có).
   (ii) `spec_path` chứa NUL ⇒ 13, đứng TRƯỚC mọi thao tác hệ tệp (bảng thứ hai, hàng f).
   (iii) `spec_path` tuyệt đối, có thành phần `..`, hoặc chứa dấu chéo ngược ⇒ 13, thông điệp "phải là đường dẫn tương đối trong kho".
   (iv) Sau `resolve()`, tệp không nằm dưới gốc (kể cả symlink trỏ ra ngoài) ⇒ 13, thông điệp "trỏ ra ngoài kho".
   (v) Không phải tệp thường (vắng, thư mục) ⇒ 13, thông điệp nêu đường dẫn đã tìm và "spec phải nằm trong cây cùng lease"; KHÔNG nói
   "đã commit tại HEAD" (bảng thứ hai, hàng a).
   (vi) Có tệp mà `read_bytes()` ném `OSError` ⇒ `RC_KHONG_XAC_DINH` 12 (ba trạng thái: so được · không có tệp ⇒ 13 · không đọc được ⇒ 12).
   (vii) Trường quyết định: `spec_sha256_required` nếu có mặt, không thì `spec_hash`. Hai trường cùng có mặt thì CHỈ
   `spec_sha256_required` quyết định — khớp ⇒ qua bất kể GIÁ TRỊ `spec_hash`, lệch ⇒ 13 bất kể giá trị `spec_hash` (hình dạng wp709;
   PROTOCOL §3.2: `spec_hash` là băm của Packet Spec, không bắt buộc bằng băm byte của tệp). Lệch ⇒ 13, thông điệp nêu tên trường, giá trị
   khai, giá trị đo.
   Thiếu `spec_path` (hoặc không phải chuỗi, rỗng, `null`) hoặc không có `spec_hash` lẫn `spec_sha256_required` ⇒ **không kiểm, không đỏ** (lease cũ, kể cả 15/619
   blob mang `spec_hash` mà không `spec_path`); dòng kết quả của `check` nói "spec: không khai — không kiểm" (nghĩa là không khai `spec_hash` lẫn `spec_sha256_required`; tên thứ ba `spec_sha256` KHÔNG được đọc — đo tại `c522c17`: 57/152 lease mang nó, 5/152 mang nó mà thiếu cả hai tên kia, đều thuộc họ `plat-m4-*`, băm khớp tệp, đều đã hết hạn — muộn nhất 2026-08-22T07:10:00Z).
   **Chú thích phải sửa (B8):** dòng 2313 ("Đi qua ĐÚNG bộ kiểm THUẦN của `check`") thành SAI sau packet — phải nói `body` KHÔNG chạy
   `kiem_bam` (đo bản thăm dò: spec lệch ⇒ `check` 13 · `body` 0). Workflow vẫn an toàn vì `check` đứng trước `body` và rc ≠ 0 thì
   `continue` (`ops-publish-lease.yml` dòng 220–223). Dòng 2295–2296 giữ nguyên vì vẫn ĐÚNG (bảng thứ hai, hàng b). Docstring của `t135`
   (`ops/lease_publish_test.py`, ngoài write set) không đổi và vẫn đúng. Docstring đầu tệp dòng 15–16 ("`check` và `body` cùng đi qua `kiem()`
   thuần") vẫn đúng chữ nhưng ngầm nói hai lệnh cùng một phán quyết, mà sau packet thì không (đo lượt 3, 16-10-2026, cửa sổ 02:12Z–02:55Z): spec lệch ⇒ `check` 13 · `body` 0;
   sửa nó trong cùng lần thêm hàng 13 (Mục tiêu 3) thành "…; riêng `check` còn gọi `kiem_bam` (băm spec/write set)".
2. **[`ops/lease_publish.py`] Băm write set.** Nếu lease có `write_set_hash` VÀ `write_set_hash_scope` bắt đầu bằng
   `sorted NFC casefold exact`: `write_set` phải là danh sách chuỗi (phần tử không phải chuỗi ⇒ 13, không để `TypeError`); tính (a) =
   `sha256(json.dumps(sorted(unicodedata.normalize("NFC", p).casefold() for p in write_set), ensure_ascii=False, separators=(",", ":")).encode("utf-8"))`
   và so; lệch ⇒ 13. Scope vắng hoặc giá trị khác ⇒ **không kiểm, không đỏ**, và `check` in "write_set_hash: scope không nhận ra — không
   kiểm" (54 lease không scope ở trên).
3. **[`ops/lease_publish.py`] Dòng xác nhận là bằng chứng.** Khi kiểm đạt, `kiem_bam` TRẢ dòng bằng chứng mang 12 ký tự đầu băm ĐO cho spec
   và cho write set, `lenh_check` in chúng; KHÔNG `print` trong `kiem()` (stdout của `body` là thân comment). Thêm hàng `13` vào bảng
   `MÃ THOÁT` ở docstring đầu tệp (dòng 18–26); `--help` không in bảng ấy (`argparse` lấy DÒNG ĐẦU của `__doc__`, dòng 2413). Chỉ thêm
   hàng 13; bảng thiếu 11, 12 là nợ sẵn có, KHÔNG thuộc packet.
4. **[`ops/lease_publish_spec_hash_test.py`] Phản chứng.** Bộ test MỚI, tự đứng (không import `ops/lease_publish_test.py`, tệp ấy thuộc
   write set #748), DẠNG BẢNG (hàng `kich_thuoc`). Dựng kho tạm bằng `git init` trong thư mục tạm, gọi `lease_publish.py check` như tiến
   trình con, đọc rc + stdout + stderr. HERMETIC, bốn lớp: (a) xoá `GITHUB_ACTOR` và mọi `GIT_*` khỏi env con (số reviewer lượt 2:
   không xoá ⇒ 27/27 · 0/27 · 27/27 khi biến không đặt, `notebyme88`, `ducthangho`); (b) mọi lệnh `git` của bộ test chạy với
   `GIT_CONFIG_NOSYSTEM=1` và `GIT_CONFIG_GLOBAL` trỏ một tệp rỗng trong thư mục tạm; (c) mỗi kho tạm đặt cấu hình cục bộ
   `core.autocrlf=false`, `user.name`, `user.email`, `commit.gpgsign=false`; (d) mọi `git clone` kèm `-c core.autocrlf=false` (bảng thứ
   hai, hàng c: thiếu nó thì `HOME` có `core.autocrlf=true` làm A3c ĐỎ GIẢ). Ca `kiem-github` dùng `gh` giả ghi ra thư mục tạm trên PATH.
   Ca phụ thuộc nền (`gh` giả bằng shebang, symlink, PATH rỗng) hoặc chạy được trên Windows, hoặc tự BỎ QUA CÓ TÊN kèm lý do khi
   `os.name == "nt"` — không im lặng xanh. Ca A4b "OSError ⇒ 12" chạy TRONG tiến trình: nạp `ops/lease_publish.py` của cây đang thử bằng
   `importlib`, chèn `PermissionError` vào lượt đọc byte của đúng tệp spec, gọi `kiem_bam`, đòi `Chan` mã 12, rồi trả lại hàm gốc.
   Chạy được bằng `python -B ops/lease_publish_spec_hash_test.py`, trả 0 khi đạt, và in đúng MỘT dòng đứng một mình có dạng
   `số/số` — dòng tổng `N/N`, N ≥ 1, hai số bằng nhau — là dòng cuối; không dòng nào khác (kể cả dòng từng nhóm) được có dạng ấy, vì
   `bang_chung_xanh` của sổ lấy dòng ĐẦU khớp (bảng thứ hai, hàng g).
5. **[`ops/lease_publish.py`] Miễn bia mộ.** Lease mang `da_bi_thay_the` (chuỗi khác rỗng) ⇒ `kiem_bam` trả NGAY ĐẦU hàm — trước chốt dạng (i), đường dẫn (ii)–(vi) và kiểm write set —, KHÔNG so băm, và trả
   "spec/write_set: lease đã bị thay thế — bia mộ — không kiểm băm" (PHẢI chứa nguyên văn `bia mộ — không kiểm băm` mà A5b đo; bản có
   ngoặc "(bia mộ) — không kiểm băm" của r2 KHÔNG chứa chuỗi ấy — số reviewer lượt 2: 26/27 với chuỗi có ngoặc). Lý do (đo lại trên
   `c522c17`, A6): chuỗi revision dùng LẠI `spec_path` với băm mới và ghi bia mộ cho lease tiền nhiệm KHI CÒN HẠN — 4/5 lease lệch là
   tiền nhiệm như vậy; `ops/ci_duong_nhanh.py::kiem_lease` đưa MỌI lease CÒN HẠN bị chạm trong PR qua `check` (dòng 541), nên một PR sửa
   spec tại chỗ và ghi bia mộ vào tiền nhiệm còn hạn (hình dạng commit `6635379`) sẽ đỏ `gate-ops` nếu không miễn. Lease HẾT HẠN đi
   `kiem(bo_qua_han=True)` (dòng 539) nên không chạm `kiem_bam`; `ops-publish-lease.yml` bỏ qua rc 9 trước `check` (dòng 204–207).
6. **[`.claude/dev/ci_dang_ky_test.py`] Đăng ký bộ test mới.** Thêm ĐÚNG MỘT dòng vào dict `MOI` (dòng 37–53 ở `c522c17`): khoá
   `"ops/lease_publish_spec_hash_test.py"`, giá trị CHÉP NGUYÊN chuỗi mẫu của dòng `"ops/nhanh_don_duoc_test.py"` (dòng 52; mẫu khớp một
   dòng đứng một mình gồm hai nhóm số cách nhau dấu gạch chéo). Không sửa dòng nào khác. Lý do: `kiem()` của sổ (dòng 579) đòi mọi
   `ops/*_test.py` mức đỉnh (`tim()`, dòng 83) nằm trong `DANG_KY` (dòng 80); sổ CHẠY các bộ `MOI` trong job `gate-registry`
   (`chay_moi` dòng 967; `ci.yml` dòng 895 `--chay`), nên đây cũng là cách nối CI — không sửa `ci.yml`. Nếu #763 land trước, dòng của
   #751 đặt cạnh hai dòng của #763; vẫn đúng một dòng thêm.

## Nghiệm thu

Ký hiệu "đo" = đo trên bản thăm dò của lượt soạn r3 (không giao, dựng từ chữ Mục tiêu 1–3, 5) bằng `do_dot_bien.py` (23:56:43Z–23:57:08Z:
bản thăm dò 15/15 ca đạt; 10 đột biến, mỗi cái chạy trên bản sao riêng trong thư mục tạm) hoặc `do_a3.py` (23:37:35Z–23:37:39Z). Số khác
ghi rõ là của reviewer. Executor phải tự đo lại trên bản dựng của mình.

- **A0 (nền, L5):** trước khi cấp lease, chạy lại mọi phép ở Số đo nền trên `master` SAU khi #748 land. ĐỎ khi: một số nào khác số ghi ở
  đây mà chưa có revision mới ghi số đo mới — khi đó KHÔNG cấp.
- **A1 (khớp ⇒ qua):** lease có spec khớp ⇒ rc 0, stdout chứa 12 ký tự đầu băm đo VÀ dòng "ĐĂNG ĐƯỢC". ĐỎ khi: gỡ dòng in bằng chứng ⇒ ca
  ĐỎ (số reviewer lượt 2); tính gốc theo thư mục chứa lease thay vì `_goc_kho` ⇒ ca rc 13, ĐỎ (đo; đột biến ấy làm đỏ 6/15 ca).
- **A2 (lệch ⇒ 13):** năm ca, mỗi ca dùng lease CHỈ mang đúng trường được sửa (lease mang cả hai trường mà chỉ `spec_hash` lệch là A2b
  (i), rc 0): (1) sửa 1 ký tự `spec_hash` ⇒ 13; (2) sửa 1 ký tự `spec_sha256_required` ⇒ 13, stderr chứa tên trường, giá trị khai và giá
  trị đo; (3) thêm 1 byte vào spec SAU khi tính băm ⇒ 13 và stdout KHÔNG chứa "ĐĂNG ĐƯỢC"; (4) `spec_path` trỏ tệp vắng ⇒ 13, thông điệp
  "không có tệp"; (5) hai trường CÙNG sai và khác nhau ⇒ 13. ĐỎ khi: gỡ phép so ⇒ ít nhất bốn ca rc 0 (số reviewer lượt 2: 8 ca của bộ
  27); thông điệp lệch chỉ ghi "băm lệch" ⇒ ca (2) ĐỎ; gọi `kiem_bam` SAU dòng in "ĐĂNG ĐƯỢC" ⇒ ca (3) ĐỎ (đo: rc vẫn 13, đỏ vì chuỗi,
  2/15 ca); "vắng ⇒ không kiểm" ⇒ ca (4) rc 0, ĐỎ (đo trên cùng nhánh mã ở A3c và A4b (8)).
- **A2b (hai trường, hình dạng wp709):** (i) `spec_hash` KHÁC nhưng `spec_sha256_required` = băm tệp ⇒ rc 0; (ii) `spec_sha256_required`
  SAI nhưng `spec_hash` = băm tệp ⇒ rc 13; (iii) `spec_hash` 63 ký tự cạnh `spec_sha256_required` đúng ⇒ rc 13, thông điệp "64 ký tự hex
  thường". ĐỎ khi: so cả hai trường ⇒ (i) ĐỎ; "khớp một trong hai là đủ" ⇒ (ii) ĐỎ (số reviewer lượt 1–2: chỉ ca ấy giết được đột biến
  này); chỉ kiểm dạng trường quyết định ⇒ (iii) rc 0, ĐỎ (đo, 1/15 ca).
- **A3 (nguồn đọc = ĐĨA cùng gốc với lease, không phải `HEAD`):** (i) kho đã có `HEAD`, lease + spec MỚI chưa commit, khớp ⇒ rc 0 (đúng
  runbook README bước 2); (ii) commit spec + lease, sửa spec trên đĩa không commit ⇒ rc 13; (iii) commit spec SAI, đĩa đúng ⇒ rc 0;
  (iv) thư mục KHÔNG có `.git`, gọi với `--root` ⇒ rc 0; (v) kho git, spec khớp, PATH trỏ thư mục rỗng (không có git) ⇒ rc 0 — khoá vế
  "`check` THUẦN" của chú thích dòng 2295–2296. ĐỎ khi: đọc blob tại `HEAD` (đúng chữ r2) ⇒ cả năm ca ĐỎ — đo 23:37:35Z–23:37:58Z: (i)
  13, (ii) 0, (iii) 13, (iv) 12, (v) 12; bản đĩa 0 · 13 · 0 · 0 · 0.
- **A3b (thứ tự chốt):** (i) lease HẾT HẠN + spec lệch ⇒ `check` rc 8 (không 13); (ii) `kiem-github` (`gh` giả) + dấu "đã đăng" + spec
  lệch ⇒ rc 9 (không 13); (iii) lease còn hạn, chưa đăng, spec lệch ⇒ `check` rc 13. Đo bản thăm dò: (i) rc 8, (iii) rc 13; (ii) là số của
  reviewer lượt 2 (chốt ngoài `kiem()` ⇒ 8 · 9 · 13; trong `kiem()` trước chốt hạn ⇒ 13 · 13 · 13; sau chốt hạn ⇒ 8 · 13 · 13). Thiết kế
  r3 không đổi VỊ TRÍ gọi so với r2, chỉ đổi nguồn đọc. ĐỎ khi: đặt `kiem_bam` TRƯỚC `kiem()` ⇒ (i) ĐỎ; gọi `kiem_bam` ở nhánh đã đăng
  của `kiem_github` ⇒ (ii) ĐỎ — mỗi đột biến đúng một ca (số reviewer lượt 2).
- **A3c (runbook tới đường đăng):** sau A3 (i), làm đúng chữ README dòng 43 `git add ops/leases && git commit` (KHÔNG add spec), rồi
  `git clone -c core.autocrlf=false` sạch và chạy `check` trong clone ⇒ rc 13, thông điệp "không có tệp", không "ĐĂNG ĐƯỢC"; add spec,
  commit, clone sạch lại ⇒ rc 0. Đo: 13 rồi 0 (23:37:35Z); cùng trình tự với `prompt_path` trên cổng HIỆN HÀNH ⇒ rc 6 ở clone sạch — lỗ
  "`git add ops/leases` bỏ sót tệp được neo" là sẵn có và fail-close. ĐỎ khi: "vắng ⇒ không kiểm" ⇒ ca đầu rc 0, ĐỎ (đo); đọc `HEAD` ⇒
  không đổi ca này (13 · 0) — nó đo đường đăng, không đo nguồn; nguồn do A3 khoá.
- **A4 (write set):** scope `sorted NFC casefold exact …` + băm đúng ⇒ rc 0 và stdout chứa 12 ký tự đầu băm write set đo; sai 1 ký tự ⇒ rc
  13; đổi thứ tự `write_set` (băm giữ) ⇒ rc 0; một đường dẫn viết hoa khác ⇒ rc 0; dạng NFD của cùng tên ⇒ rc 0; `write_set` có một phần
  tử số nguyên (kèm scope + băm hợp lệ dạng) ⇒ rc 13, không traceback. ĐỎ khi: bỏ `casefold` ⇒ ca viết hoa ĐỎ; bỏ `normalize` ⇒ ca NFD ĐỎ;
  bỏ `sorted` ⇒ ca đổi thứ tự ĐỎ — mỗi đột biến làm đỏ ÍT NHẤT ca đích (số reviewer: 1 · 1 · 2 ở lượt 1, 4 · 1 · 4 ở lượt 2, phụ thuộc
  fixture); gỡ dòng bằng chứng write set ⇒ ca đầu ĐỎ; gỡ chốt kiểu phần tử ⇒ rc 1 kèm `TypeError`, ĐỎ (số reviewer lượt 2).
- **A4b (ca biên, nguồn đĩa):** (1) spec 6 byte `61 0d 0a 62 0d 0a` trên đĩa + băm byte thô `58055bdc…` ⇒ rc 0; (2) `spec_hash` 63 ký tự
  (lease một trường) ⇒ 13, thông điệp "64 ký tự hex thường"; (3) `spec_path` chứa NUL ⇒ 13, không traceback; (4) `../ngoai.md` ⇒ 13,
  "tương đối"; (5) `spec_path` có dấu chéo ngược thay cho gạch chéo ⇒ 13, "tương đối"; (6) đường dẫn tuyệt đối ⇒ 13, "tương đối";
  (7) symlink trong kho trỏ ra ngoài ⇒ 13, "ngoài kho" (bỏ qua có tên trên `nt`); (8) `spec_path` là thư mục ⇒ 13, "không có tệp";
  (9) đọc ném `PermissionError` (trong tiến trình) ⇒ `Chan` mã 12. ĐỎ khi (đo, mỗi đột biến chạy trên bản sao riêng): đọc văn bản ⇒ (1)
  rc 13; gỡ HẲN chốt dạng hex ⇒ (2) vẫn rc 13 nhưng sai thông điệp (số reviewer lượt 2 — vì thế ca neo THÔNG ĐIỆP); bỏ chốt NUL ⇒ (3) rc 1;
  gỡ chốt dạng đường dẫn ⇒ (4)(5)(6) vẫn rc 13 nhưng sai thông điệp; gỡ `relative_to` ⇒ (7) rc 0; "vắng ⇒ không kiểm" ⇒ (8) rc 0; gộp 12
  vào 13 ⇒ (9) mã 13.
- **A5 (lease cũ không đỏ):** (1) không `spec_path` ⇒ rc 0, "không khai — không kiểm"; (2) `write_set_hash` không scope ⇒ rc 0, "scope
  không nhận ra"; (3) có `spec_path` mà không có `spec_hash` lẫn `spec_sha256_required` (56/619 blob thật — số của lượt soạn r3; lease chỉ mang `spec_sha256`, 5 lease ở `c522c17`, cũng rơi vào dạng này vì cổng không đọc `spec_sha256`) ⇒ rc 0, "không khai — không kiểm"; (4) `spec_hash: null`
  cạnh `spec_sha256_required` đúng ⇒ rc 0. ĐỎ khi: coi thiếu trường là lỗi ⇒ (1)(2) ĐỎ; "có `spec_path` mà không băm ⇒ 13" ⇒ (3) ĐỎ;
  "`null` là băm sai dạng" ⇒ (4) ĐỎ (hai đột biến sau sống sót bộ A của r2, số reviewer lượt 2).
- **A5b (bia mộ):** lease CÒN HẠN mang `da_bi_thay_the`, spec sửa tại chỗ sau khi cấp ⇒ `check` rc 0, stdout chứa `bia mộ — không kiểm
  băm`, và vẫn rc 0 sau khi XOÁ tệp spec (cùng ca, không đổi số ca); cùng hình dạng KHÔNG mang `da_bi_thay_the` ⇒ 13. ĐỎ khi: bỏ miễn ⇒ ca đầu rc 13
  (đo, 1/15 ca); đặt miễn SAU chốt tệp ⇒ ca đầu rc 13 sau khi xoá spec (đo lượt 3, 16-10-2026, cửa sổ 02:12Z–02:55Z): bản thăm dò 40 ca thiếu bước xoá vẫn 40/40.
- **A6 (không hồi quy):** (i) trên một `git clone` (KHÔNG `git archive`) ở nền lúc cấp, trong tiến trình: `kiem(bo_qua_han=True)` rồi
  `kiem_bam(...)` cho mọi lease; TẬP lease đổi rc so với nền phải đúng tập đã khai. Đo trên `c522c17`, clone 542 ref (23:38:49Z–23:54:26Z):
  nền `{0: 143, 8: 4, 10: 5}`, ứng viên `{0: 142, 8: 4, 10: 5, 13: 1}`, tập đổi = {`gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906`
  0 → 13} (cuối chuỗi, spec sửa sau khi cấp); 38 lease được miễn bia mộ, 60 kiểm spec và khớp, 4 kiểm write set và khớp. Số tuyệt đối
  phụ thuộc tập ref cục bộ (`_quet_lease_toan_kho` dòng 694–754 đọc lease cũ của `thay_the_cho` trên MỌI ref cục bộ); tiêu chí là TẬP,
  không phải số. (ii) `ops/lease_publish_test.py` trên ứng viên: số ca đạt bằng nền, delta 0 (nền 265/265; bản thăm dò 265/265,
  23:36:50Z–23:43:02Z). ĐỎ khi: một ca của `lease_publish_test.py` từ đạt sang trượt, hoặc tập lease đổi rc khác tập đã khai; đột biến bỏ
  miễn bia mộ ⇒ 5 lease đổi `0 → 13` thay vì 1 (đo: đúng bốn tiền nhiệm cộng `…-exec-1r4`).
- **A6b (`kiem()` bất biến, chú thích đúng):** `git diff -U0 <nền> -- ops/lease_publish.py` không có hunk nào trong thân `kiem()` (dòng
  1009–1114) và `kiem()` vẫn trả 2 phần tử (bản thăm dò lượt soạn r3: 5 hunk, chưa gồm sửa chú thích `lenh_body` và docstring dòng 15–16; đủ cả hai là 7 hunk, đo lượt 4 — không hunk nào trong khoảng ấy); trong ứng viên, chú thích trong
  `lenh_body` không còn câu "Đi qua ĐÚNG bộ kiểm THUẦN của `check`" mà nói `body` KHÔNG chạy `kiem_bam`. ĐỎ khi: `git diff -U0` có hunk nằm trong
  1009–1114; trả 3 phần tử ⇒ `t01` ĐỎ (`ValueError: too many values to unpack`, đo lượt 3); `grep -c` câu cũ trong ứng viên ≥ 1 ⇒ ĐỎ. Lời gọi
  `kiem_bam(...)` đặt trong `kiem()` KHÔNG làm `t191` đỏ (đo lượt 3, 16-10-2026, cửa sổ 02:12Z–02:55Z): `t191` 1/1 XANH, vì `_la_chot` chỉ coi `raise Chan` và lời gọi
  tên `_kiem_*`/`_doc_*` là chốt; đổi tên hàm thành `_kiem_bam` hoặc thêm `raise Chan` thì `t191` ĐỎ (`KHONG_CHAM`). Thứ bắt lời gọi tên `kiem_bam` là
  `git diff -U0`, A3b (i) (đặt trước chốt hạn: 13 thay vì 8) và A3b (ii) (13 thay vì 9). Số "263/265, đỏ đúng `t01` và `t191`" của lượt 1–2 là của bản
  dựng đặt `_kiem_bam_spec`.
- **A7 (cổng kho):** ruff F delta 0 (multiset) cho các tệp đổi (nền: 2 F841 ở `lease_publish.py`; bản thăm dò: vẫn 2, dời sang dòng
  200–201 khi nối vào dòng 16, hoặc 201–202 khi bọc dòng, tuỳ cách sửa docstring dòng 15–16 — đo lượt 4, đo lại lượt 5). Sổ test sống: `python .claude/dev/ci_dang_ky_test.py` in `ĐĂNG KÝ: N+1/N+1` (hai số BẰNG NHAU) và `TỔNG: ĐẠT`, với N = số
  đăng ký ở nền lúc cấp (tại `c522c17`: N = 23 ⇒ `24/24`; nếu #763 land trước: 25 ⇒ `26/26`). Bộ MỚI chạy qua chính `chay_moi` của sổ,
  không cần `--chay` trọn bộ: `chay_moi(moi={<khoá mới>: MOI[<khoá mới>]})` trả 0 và in `ĐẠT rc=0` (số reviewer lượt 2: dòng cuối `27/27`
  ⇒ `CI_DANG_KY ops/lease_publish_spec_hash_test.py: ĐẠT rc=0`). `ops/ci_duong_nhanh_test.py` (job `gate-ops`) cho số ca và số đột biến
  bằng nền, `TONG: DAT` (nền 104/104 · 383/383; bản thăm dò KHÔNG có tệp test mới và dòng `MOI`: 104/104 · 383/383 · `TONG: DAT`,
  23:49:03Z–23:51:17Z). Kích thước ≤ trần sensitive. ĐỎ khi: bỏ dòng `MOI` ⇒ `test sống chưa đăng ký`, `N+1/N`, `TỔNG: ĐỎ` và
  `k01_so_dang_ky_nhan_muc_da_noi` ĐỎ (số reviewer lượt 2: `CA: 103/104`, `DOT BIEN: 382/383`, `TONG: DO`, rc 1); bộ mới in thêm một dòng
  số/số đứng một mình trước dòng tổng ⇒ `bang_chung_xanh` đọc dòng ấy (đo hàm, bảng thứ hai hàng g); `git diff --numstat` vượt 300 dòng
  thêm hoặc 3 tệp.

## Ngoài phạm vi (cố ý)

- `plan_hash`: không có quy ước chung về tệp plan (chủ kho chốt Q8).
- Sửa `ops/lease_publish_test.py`, `ci.yml` (thuộc write set #748, lease r11 đang giữ). Đăng ký bằng MỘT dòng `MOI` là cách nối CI đúng,
  không sửa `ci.yml`.
- **`ops/README.md`.** Sau packet, bước 2 (dòng 37–38, `check` trước khi commit) vẫn ĐÚNG (A3 (i)). Hai nợ tài liệu sẵn có, KHÔNG do
  packet này gây ra: bảng "Cổng chặn" thiếu rc 13 (như đã thiếu 10, 11, 12); bước 3 (dòng 43) chỉ `git add ops/leases`, bỏ sót tệp được
  neo — với `prompt_path` HIỆN NAY đã cho rc 6 ở đường đăng, với spec sẽ cho rc 13 (A3c), đều fail-close.
- Lệch đĩa/blob do chuẩn hoá EOL (`.gitattributes` dòng 8): spec CRLF trên đĩa + lease neo băm CRLF ⇒ `check` trước commit 0, đường
  đăng 13 (Số đo nền). Lệch luôn rơi về phía ĐỎ ở đường đăng, không bao giờ xanh giả; người soạn lease băm tệp sau khi chuẩn hoá LF.
- Người gọi TƯƠNG LAI đọc lease từ REF (blob) mà muốn kiểm băm spec: phải đọc spec từ blob CÙNG ref/tree với lease (luật nguồn,
  Mục tiêu 1) — không có mã trong packet này.
- Windows của bộ test mới: tại `c522c17`, `ci.yml` dòng 50–53 chỉ thêm `windows-latest` cho `workflow_dispatch` hoặc PR gắn nhãn
  `windows`; push `master` chỉ ubuntu (ADR-0049). Gắn nhãn lên PR đang mở KHÔNG tự sinh lượt chạy (`pull_request` không khai `types:`).
  `launcher-windows.yml` không nhắc `ci_dang_ky_test` hay `lease_publish` (0 dòng, 00:03:51Z 16-10). Muốn có Windows trước merge:
  `workflow_dispatch` trên ref ứng viên (lease khai ngân sách CI tay), hoặc ghi `KHÔNG ĐO ĐƯỢC` và nợ có tên.
- Sửa 54 lease không scope hay 5 lease lệch băm — không phải việc của cổng mới; Mục tiêu 5 (miễn bia mộ) và A5b là bắt buộc vì
  `ops-publish-lease.yml` và `kiem_lease` đều đưa lease còn hạn qua `check`.

## Hình dạng kế thừa

Chép từ lịch sử cổng `lease_publish.py` (CLAUDE.md các mục "BIA MỘ", "rc=8 che rc=9", `t32`): (a) **chốt chạy trước che chốt sau** — vị trí
không còn để executor khai: `kiem_bam` sau `kiem()`, không ở nhánh đã đăng của `kiem-github`; A3b khoá; (b) **dòng xác nhận không đi kèm
việc kiểm** (docstring `kiem`) — A1, A4 khoá. ĐẾM HÌNH DẠNG trong `ops/lease_publish.py` (tệp không đổi từ `6f121a3`, đo lại 00:03:51Z 16-10
trên `c522c17`): (a) ≥ **4** — `#568`/`#566` (dòng 1228–1236), #589 (dòng 1238–1244, 1272–1280), slug `unposted-error-precedence-changes` hai
lượt (dòng 1160–1167 và 1198); (b) 1. BỘ ĐẾM TIỀN NHIỆM (L4, chép từ biên nhận): hình dạng A "lời khai rộng hơn phép đo" = 7
(`ops/reviews/README.md` dòng **484** tại `c522c17`, dời từ 482) và 8 theo `ops/specs/t33-doi-shellcheck-r3.md` dòng 104, 266; E = 4;
D = 3. Ghi thêm, KHÔNG tự tăng bộ đếm (người giữ kho quyết): lượt 2 bắt r2 mắc A ba lần (B5: số 15 ca áp cho 26 ca; B6: số tuyệt đối không
ghi điều kiện ref; B8: chú thích khai rộng hơn mã sau packet; lượt 3 đo thêm hai ca của r3 — A6b khai `t191` đỏ với tên `kiem_bam` (xanh, đo), hàng B4 khai "mỗi yêu cầu có một ca và một đột biến" (sáu yêu cầu sống sót) — người giữ kho quyết có tính vào bộ đếm A hay không); Codex bắt một hình dạng MỚI — **(c) chốt đọc từ một nguồn khác nguồn của
thứ nó ràng buộc**: r2 đã đo lease được đọc từ ĐĨA (r2 dòng 90) mà vẫn chọn `HEAD` cho spec, rồi khai nợ cho runbook mà chính lựa chọn
ấy làm gãy (lần 1). Lượt soạn r3 tự mắc một ca "rig tự đẻ kết quả giả": kịch bản đo `.gitattributes` đặt trùng tên thư mục clone với ca
trước, cho rc 0 sai; chạy lại với tên riêng mới ra rc 13 (23:52:28Z) — số ghi ở trên là số sau khi sửa. Ngưỡng "lần ba" (L4) ĐÃ CHẠM với
(a) và với A: trước khi cấp lease phải có bằng chứng bền (đường dẫn comment) chủ kho đồng ý tiếp — thiếu thì DỪNG (`depends_on` (5)).

## Chưa đo được

- Hành vi trên Windows (đường dẫn, NFC trên NTFS, symlink, `gh` giả, PATH rỗng) — chỉ đo Linux; không trigger tự động nào đo thay.
- Lượt Codex có chạy được không: đo 15-10 sáng (`SAP_HET_HAN`, ảnh chụp cũ ~185 h); lượt soạn r3 KHÔNG đo lại.
- Đường dẫn comment của quyết định chủ kho 15-10 về sổ test sống và về đồng ý đi tiếp ở ngưỡng L4 (`depends_on` (5)).
- VERDICT lượt 5 r28 `d3f1d9db…` và hai vế "đột biến D2, D3, D5, D6, D7 cho rc=0" (nguồn ngoài kho: đo lượt 7 ở `0cfe253`, 0/3520 tệp khớp `d3f1d9db`).
- `VERDICT.md` và `HINT.patch` của mọi lượt review của packet này mà spec dẫn bằng băm (hàng `review của r2` và các mục `Vá sau review lượt N`), bản thăm dò 40 ca cùng ma trận đột biến của lượt 3 (nguồn của 239 dòng, 296 (298), 40/40, `t191` 1/1 ở trên), của lượt 4 (nguồn của 257 = 59 + 197 + 1, dư 43, +1/−1 và +2/−1, 7 hunk, 40/40 của nhóm (7)–(11); các số lượt 4 đo thẳng trên kho — 161/248 ký tự, 174/270 byte, 2765 tệp (mục `git ls-tree -r`, không phải blob khác nhau) — tái lập được từ kho) và của lượt 5 (nguồn của nhóm (12)–(16)), và các kịch bản đo của lượt soạn r3 (`do_nguon.py` `af6eb7dd…`, `dung_tham_do.py` `6dd87cc0…`,
  `do_a3.py` `56f1fbdc…`, `do_b2.py` `b27a6771…`, `do_dot_bien.py` `37bc0d71…`, `do_a6.py` `4b8b4ba6…` — sha256) KHÔNG có trong kho (đo lượt 7 ở `0cfe253`: 0/3520 tệp khớp sáu băm kịch bản và 0 tệp mang tên các kịch bản ấy; VERDICT/HINT: neo ở hàng `review của r2` và các mục `Vá sau review lượt N`); bên thứ
  ba muốn tái lập phải dựng lại bản thăm dò từ chữ Mục tiêu 1–3, 5. Bản thăm dò không được giao (PROTOCOL §8 dòng 648).
- A3b (ii) và các số "của reviewer" ở Nghiệm thu: không đo lại ở lượt soạn r3.
- `python .claude/dev/ci_dang_ky_test.py --chay` trọn bộ (bước CI, nặng) — chỉ chạy bản không `--chay` trên nền; việc sổ CHẠY được bộ mới
  là số của reviewer lượt 2.
- Nội dung cuối cùng của #763 và của #752 r3: hai đặc tả đang soạn, chưa đóng băng lúc đọc (23:57:40Z); `depends_on` (4) phải đo lại lúc cấp.
- Sáu yêu cầu của Mục tiêu 1–3, 5 mà A-list KHÔNG làm ĐỎ (đo lượt 3, 16-10-2026, cửa sổ 02:12Z–02:55Z), bản thăm dò 40 ca, mỗi đột biến một bản sao, cả sáu 40/40: (1) chốt DẠNG áp
  cả khi thiếu `spec_path`; (2) `spec_path` rỗng ⇒ không kiểm; (3) `spec_path` không phải chuỗi ⇒ không kiểm, không `TypeError`; (4) scope giá trị khác
  `sorted NFC casefold exact…` ⇒ không kiểm (A5 (2) chỉ đo scope vắng); (5) `da_bi_thay_the` rỗng hoặc không phải chuỗi KHÔNG miễn; (6) hàng 13 trong docstring
  `MÃ THOÁT`. Executor khai chúng trong PR là kiểm bằng đọc mã; thêm ca (mỗi ca một hàng bảng ≈ 1 dòng) chỉ khi `git diff --numstat` còn dư.
- Năm nhóm yêu cầu nữa mà A-list KHÔNG làm ĐỎ (đo lượt 4, 16-10-2026, cửa sổ 03:00Z–03:56Z; bản thăm dò lượt 4 độc lập, KHÔNG giao, 40 ca dạng bảng, mỗi đột biến một bản sao, tất cả
  40/40): (7) thứ tự miễn bia mộ (Mục tiêu 5) — A5b chỉ ghim vế "trước chốt tệp (v)" bằng bước xoá spec; đặt miễn SAU chốt dạng (i), SAU chốt đường dẫn (iv), hoặc đặt kiểm write set
  TRƯỚC miễn đều 40/40, mà lease bia mộ mang băm sai dạng, `spec_path` ra ngoài kho hay `write_set_hash` lệch khi ấy ra rc 13 thay vì 0; (8) thông điệp tệp vắng (Mục tiêu 1 (v)) — bỏ cụm
  "spec phải nằm trong cây cùng lease", bỏ đường dẫn đã tìm, hoặc đổi thành "đã commit tại HEAD" đều 40/40 (A2 (4) chỉ đòi "không có tệp"); (9) "hex thường" (Mục tiêu 1 (i)) — nhận băm
  viết hoa rồi hạ chữ thường đều 40/40 (không ca nào dùng băm viết hoa); (10) sửa docstring dòng 15–16 (Mục tiêu 1) — không sửa vẫn 40/40 và không tiêu chí nào đo nó (A6b có `grep -c` cho
  chú thích `lenh_body`, không có cho docstring); (11) `write_set` không phải danh sách (Mục tiêu 2 "phải là danh sách chuỗi") — bỏ chốt kiểu danh sách mà giữ chốt kiểu phần tử vẫn 40/40, trong khi `write_set: null` cạnh scope + băm hợp lệ dạng ra rc 1 kèm `TypeError` thay vì rc 13. Cách xử như (1)–(6): khai trong PR là kiểm bằng đọc mã, thêm ca chỉ khi `git diff --numstat` còn dư (bản thăm dò lượt 4 tốn 257 dòng thêm = 59 + 197 + 1, dư 43, nên có chỗ cho ca mới nếu người giữ kho muốn ghim chúng).
- Năm nhóm yêu cầu nữa mà A-list KHÔNG làm ĐỎ (đo lượt 5, 16-10-2026, cửa sổ 04:43Z–05:20Z; bản thăm dò lượt 5 độc lập dựng từ CHỮ A-list, KHÔNG giao: nền 13/40, ứng viên 40/40;
  52 đột biến, mỗi đột biến một bản sao: 31 bị giết, 21 sống 40/40, trong đó 14 thuộc các nhóm (1)–(5), (7)–(9), (11) đã khai — tái lập đúng — và 7 thuộc nhóm mới dưới đây):
  (12) `lenh_body` KHÔNG gọi `kiem_bam` (Mục tiêu 1 "Mã của `lenh_body` … không đổi", chú thích A6b) — cho `lenh_body` gọi `kiem_bam` vẫn 40/40, và `ops/lease_publish_test.py` cùng
  `ops/ci_duong_nhanh_test.py` có 0 chỗ nhắc `spec_path`, `spec_hash`, `spec_sha256_required`; (13) `kiem-github` không gọi `kiem_bam` ở đường lease CHƯA đăng — A3b (ii) chỉ đo đường đã đăng;
  (14) kiểm write set độc lập với kiểm spec (Mục tiêu 2) — để `kiem_bam` thoát sớm khi lease không khai spec thì vẫn 40/40 nếu lease của A4 và của A5 (2) có `spec_path` + băm, và 36/40 nếu lease của cả hai chỉ mang write set:
  A4 và A5 (2) không ghim fixture; (15) thông điệp chốt (i) nêu đúng tên trường — in cứng `spec_hash` cho lỗi dạng của `spec_sha256_required` vẫn 40/40 (A2b (iii) và A4b (2) đều làm hỏng `spec_hash`);
  (16) vị trí và hình dạng lời gọi trong `lenh_check` (Mục tiêu 1 "TRƯỚC mọi `print`", Mục tiêu 3 "`kiem_bam` TRẢ dòng, `lenh_check` in") — gọi giữa hai `print`, gọi sau khối `--du-bao`, hay để `kiem_bam`
  tự `print` rồi trả `[]` đều 40/40. Danh sách (1)–(16) là các nhóm ĐÃ ĐO THẤY, KHÔNG phải tập đóng: mọi yêu cầu bằng chữ trong Mục tiêu 1–6 mà Nghiệm thu
  không nêu đột biến làm đỏ đều thuộc diện "khai trong PR là kiểm bằng đọc mã", kể cả khi chưa có tên ở đây.

## Vá sau review lượt 3

Review lượt 3 (`approve`, 0 P1 · 0 P2 · 6 P3; VERDICT sha256 `8da55a9c4eb778e80357ca324d6a88475f51550f00216468a7fc6ebcba8fd1ef`,
HINT sha256 `ca2315c867764b34c98602d2459281b729f2b09e9176bd5554f590898a4aa1d6`). Áp NGUYÊN VĂN 11 hunk của HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT, trừ chính mục này (9 dòng thêm tay, khi mục được thêm nó là mục cuối tệp; đo lượt 4 trên bản `00a97d3`: bản đã áp HINT lượt 3 khác bản ấy đúng 9 dòng). Sáu lớp: `a6b-t191-chi-thay-raise-chan-va-ten-kiem-doc` ·
`yeu-cau-con-lai-chua-co-tieu-chi-do` · `kich-thuoc-40-ca-chua-co-so-do-giao-duoc` ·
`docstring-dau-tep-check-body-cung-kiem-thuan` · `bia-mo-thu-tu-voi-chot-duong-dan-chua-ghim` ·
`trich-dan-dong-bang-lop-va-quet-lease-lech` — chỗ sửa xem từng hunk (mỗi hunk mang dòng `# lop:` trong HINT). VERDICT.md và HINT.patch lượt 3 KHÔNG có trong kho (đo lượt 4 ở `00a97d3`: không tệp nào ở `ops/reviews`, `ops/specs`, `ops/land`, `ops/prompts` mang hai băm trên, 2765 tệp); thứ định danh là băm.

## Vá sau review lượt 4

Bản trước vá: commit `00a97d3`, sha256 `78acedd10016ee4bedc7f2b3de0764b4702a815d474f1dc13fa903ced84f22d7`. Review lượt 4
(`approve`, 0 P1 · 0 P2 · 4 P3; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, `reviewed_sha`
`00a97d3a60820349df7245837433f166c0cdda55`; VERDICT sha256 `d018e8c404bbb68738a11212c95376429e988b5ecb876b94625e7635bfd9e3f9`,
HINT sha256 `92d3a9142d5544d32c98d13f499833bda1d867d2e5f1e6f92b53bfe5ae28e21f`). Áp NGUYÊN VĂN HINT (`patch -p0 --fuzz=0`,
rc 0); không sửa gì ngoài HINT, trừ chính mục này (đo lượt 5: bản đã áp HINT lượt 4 khác `SPEC.md` ở `d6bc803` đúng 10 dòng thêm tay). VERDICT.md và HINT.patch lượt 4 KHÔNG có trong kho (đo lượt 5 ở `d6bc803`: 0/3513 tệp trên toàn cây mang hai băm trên); thứ định danh là băm. Bốn lớp: `kich-thuoc-so-dem-thieu-docstring-va-don-vi-byte` ·
`yeu-cau-chua-co-ca-vuot-sau-yeu-cau-da-liet-ke` · `trich-dan-bang-chung-xanh-616-619` ·
`luot-3-tep-khong-co-trong-kho-va-muc-tu-than`. Vòng vá P3 thứ 2/2 chủ kho cho; P3 còn lại sau vòng này vào sổ nợ.

## Vá sau review lượt 5

Bản trước vá: commit `b055a2f`, sha256 `fb27457d6a10bd866e73d8d6724e71eb1d6fa20cce0366c8242ace23c44ab61f`. Review lượt 5 (reviewer Claude Sonnet 5.5 subagent
`review-sonnet-max`, `reviewed_sha` `d6bc803e031dff0fe37a56f513282bf1472fc129`; VERDICT sha256 `15ca093e42d53215d9386d971f25bf4d90fd08c81f52590ad473835065fe641c`, HINT sha256 `1255f4f4acc4b13626087b6f8aed4bc5c2a2317e781af00552bbde8ec4a699e1`;
hai tệp KHÔNG có trong kho (đo lượt 6 ở `bedcf2f`: 0/3520 tệp trên toàn cây mang hai băm trên); thứ định danh là băm). Áp NGUYÊN VĂN HINT (`patch -p0 --fuzz=0`, rc 0); không sửa nội
dung nào ngoài HINT và mục này. Lớp: `a7-f841-200-202-sai-phai-la-201-202` · `luot-4-tep-khong-co-trong-kho-va-muc-tu-than-lan-2` · `yeu-cau-chua-co-ca-nhom-12-16-tap-van-mo-lan-3`. Vòng vá P3 thêm thứ 1/2 chủ kho cho (16-10).

## Vá sau review lượt 6

Bản trước vá: commit `62924ff`, sha256 `1da6d190b97ed6cf41ddd961bdad6c2ee38fe498ef13760d2305b1f63dbd62cd`. Review lượt 6 (reviewer Claude Sonnet 5.5 subagent
`review-sonnet-max`, `reviewed_sha` `bedcf2ff7ea53abe70c1c75b8af8b753e0b2e8ef`; VERDICT sha256 `8d572544b2478083ec736a605ac9aa2181cedbebcecc395d12e33e46e3a24971`, HINT sha256 `f6d4efb710256d0bea9a77c8664851916e46124ec7fa0706b82fc9d4ea0f8016`; hai tệp KHÔNG có trong kho
(đo ở `62924ff`: 0/3520 tệp trên toàn cây mang hai băm trên); thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa nội dung nào ngoài HINT và mục này. Lớp: `luot-5-tep-khong-co-trong-kho-va-muc-tu-than-lan-3` · `nhom-14-hai-so-40-40-va-36-40-gan-sai-fixture-thieu-a5-2` · `quy-tac-mo-pham-vi-1-3-5-thieu-muc-tieu-4-6-va-nguon-do-lech`.

## Vá sau review lượt 7

Bản trước vá: commit `e5698ca`, sha256 `573d744d4118de9d4678fca5a2ff1e01458f2cb6dcce2daedb11a6825a080f5a` (`git show e5698ca:ops/specs/no-p3-lease-spec-hash-r3.md` ra đúng băm này).
Review lượt 7 (`approve, 0 P1 · 0 P2 · 5 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `0cfe253a368c36c2c53c687d63930f1283d2f1d9`; VERDICT sha256 `e9f500f4ada50df60587b20d778f00d3abe538d151e87585bd866e7384152634`, HINT sha256 `e7c31a07b3ff5974ed24920ef1335a1be91d84cf6d4d928b0a83f1a9d8b25452`; hai tệp KHÔNG có trong kho — đo 2026-10-16 ở
`e5698ca`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (8 dòng thêm tay). 5 lớp:
`chua-do-duoc-tep-khong-co-trong-kho-khong-neo-commit-lan-4` · `don-vi-3520-blob-la-muc-cay-khong-phai-blob-khac-nhau` · `nguoi-tieu-thu-check-khong-deu-chay-tren-cay-sach` · `spec-sha256-ten-thu-ba-khong-doc-lam-sai-nhan-khong-bam-va-khong-khai` · `thay-the-cho-207250f-la-merge-trong-nhanh-pr-khong-phai-vao-master`.

