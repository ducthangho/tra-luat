# Đặc tả packet `no-p3-lease-spec-hash` r4 — nợ P3 (b1): `lease_publish.py check` đối chiếu băm spec và write set

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-lease-spec-hash` |
| `packet_issue` | #751 (`gh api repos/ducthangho/tra-luat/issues/751` lúc 23:57:40Z 15-10-2026: `open`, `updated_at 2026-10-15T05:52:49Z`; đọc lại 13:08:55Z 23-10-2026: vẫn `open`, `updated_at` không đổi). |
| `revision` | 4 |
| `thay_the_cho` | **r3**: `ops/specs/no-p3-lease-spec-hash-r3.md`, sha256 `12a1acb7c0d0145316e311d56d152139c2eb11c7cf7d892e1e5025fbf2e844c5`, blob `63023a67e87c6859621d613ce3a49909324bebe1`, 467 dòng, commit cuối sửa nó `d269836d0e1f4821ef8dfc66b546000eb9c9761c` (vá review lượt 16, 17-10-2026; `git rev-parse` và `sha256sum` trên `git show <commit>:<tệp>` cho cùng blob, cùng băm ở `d269836` và ở `c3f6f5f`). Vị trí: lúc 14:00:44Z 23-10-2026 không nhánh máy chủ nào chứa `d269836` và không commit nào trên mọi ref máy chủ mang blob ấy (bản bare đủ ref của `depends_on` (2); nhánh máy chủ `claude/spec-no-p3-r3` ở `a2069ac`, 16-10-2026, mang một blob r3 sớm hơn, `ec4ffa53`); tìm ở nhánh đặc tả `claude/spec-no-p3-r3` sau khi đẩy, chưa thấy thì hỏi phiên điều phối — thứ định danh là băm, không phải tên nhánh. Bản `5fc0048` của tệp mang tên r3 (blob `602b44fc59cf202fa91a95a18d6f7151a36f75bb`) là bản nháp đo lại của r4 trước `git mv` ở `6c2fe9b`, KHÔNG phải một revision. r4 giữ thiết kế, write set, yêu cầu của Mục tiêu 1–6 và số ca của r3; khác ở nền, trần, `depends_on` và cách đo các tiêu chí khớp chuỗi (mục **Thay đổi so với r3**). r3 thay **r2**: `ops/specs/no-p3-lease-spec-hash-r2.md`, sha256 `8f700b06b28e4c02c615b591b02a75a2fd901239746eb2a3fb8389dd9f549ec4`, blob `3a708be2867bab1e14e93dab07f0711479e8b867`, commit thêm `a9ef33c24665dedc70f2c839e2357353bd4054af`; vào `master` qua PR #762 (merge vào `master` là `c522c17`; `207250f` là merge vào nhánh của PR, không nằm trên first-parent của `master`) CHỈ ĐỂ LƯU VẾT (nợ `SPEC-R2-751-752-KHONG-DUOC-CAP-LEASE`, ghi ở hàng `finding sau review`). r2 thay r1 (sha256 `17df1dccb4df520acb0d525cfc091dbee07fc8d878cf63f2fe2a4874a1a2fc6c`, commit `55bd0d24`). Thứ định danh r1, r2, r3 là băm, không phải tên nhánh hay vị trí tệp. r4 không sửa byte nào của r1, r2, r3 (đóng băng); mọi closure, lease và `spec_hash` từ nay neo **r4**. |
| review của r2 | **Lượt 2** (hẹp), reviewer Claude Sonnet 5.5 chạy bằng subagent (tự khai): `verdict: approve`, `reviewed_sha` `a9ef33c24665dedc70f2c839e2357353bd4054af`, `spec_sha256` `8f700b06…549ec4`, **0 P1 · 0 P2 · 8 P3**; 11 lớp của lượt 1 ĐÃ ĐÓNG. `VERDICT.md` sha256 `fcb545136985a89e6711f37dd3f4e3c42121202f6d4c7d156b80b13604353102` (167 dòng); `HINT.patch` sha256 `f536ce126e5b1048d29f361534dd60a78c00c80d404535110f5e4126f4fab037` (11 hunk, mỗi hunk một dòng `# lop:`, chỉ văn bản đặc tả). Hai tệp KHÔNG có trong kho ở `1d7e642` (0 trên 5049 mục cây có sha256 bằng một trong hai băm, đo 13:13:51Z 23-10-2026; ở `c522c17`: 0 trên 3510, đo 17-10-2026; mục cây định nghĩa ở mục Chưa đo được; băm của r1 và của r2 làm điều khiển dương, mỗi băm khớp đúng 1 mục ở cả hai nền. Lọc tên `git ls-tree -r --name-only 1d7e642 ops/reviews` theo `spec-hash` ra 0 dòng nhưng chỉ phủ `ops/reviews`: toàn cây `1d7e642` có 2 đường dẫn chứa `spec-hash`, là hai bản đặc tả r1, r2); thứ định danh là băm. Cách r3 đóng từng lớp: mục **Thay đổi so với r2**. |
| finding sau review | **P2 Codex trên PR #762**: comment review `4286041913` (`pull/762#discussion_r4286041913`), `chatgpt-codex-connector[bot]`, `created_at 2026-10-15T17:13:10Z`, neo r2 dòng 231 tại `4c550bc0fcdf63d92a709d217a3da22b33938a14`, tiêu đề "Keep the documented pre-commit lease check usable" (đọc lại bằng `gh api repos/ducthangho/tra-luat/pulls/comments/4286041913` ~23:30Z). Ý: r2 bắt `check` đọc `spec_path` CHỈ từ `HEAD` đã commit và trả 13 khi spec chưa commit (r2 dòng 89–95), trong khi runbook `ops/README.md` dòng 33–44 bảo soạn lease → `check` → rồi mới commit; r2 tự nhận runbook sẽ sai mà để README nguyên. Ghi sổ thành nợ `SPEC-R2-751-752-KHONG-DUOC-CAP-LEASE` (P2, `trang_thai: mo`) ở `ops/land/pr759-no-p3-ho-so-land-evidence.yaml` dòng 407–418 tại `c522c17` (tệp không đổi tới `1d7e642`; `git grep -l` mã nợ ấy trên toàn cây `1d7e642` ra đúng 1 tệp là tệp này, 13:25:37Z 23-10-2026): không lease nào được cấp trên r2; r3 phải xử lý finding trước khi review lại và cấp lease. r3 đóng phần #751 của nợ ấy (hàng C1), r4 giữ nguyên cách đóng ấy; phần #752 (`discussion_r4286041896`) thuộc đặc tả khác. |
| `nguon_cap_viec` | Sổ nợ P3 mục 4: review wp685 lượt 2–5 đo `lease_publish.py check` không đọc `spec_hash`, `spec_sha256_required`, `plan_hash`, `write_set_hash`, `spec_path` (VERDICT review lượt 5 r28 sha256 `d3f1d9db4896efe8c1b62112a3d0aa479b64c5dc110da1d323b3297d7e7c45fb`, M11: đột biến D2, D3, D5, D6, D7 cho rc=0 cả năm) — **KHÔNG ĐO ĐƯỢC từ kho**: đo lại 13:12:37Z–13:13:36Z 23-10-2026 trên 557 nhánh (`refs/remotes/origin/*` của bản bare đủ ref, bỏ nhánh của chính đặc tả `claude/spec-no-p3-r3`): 0/1240 blob trong lịch sử có tên tệp chứa `verdict` (không phân biệt hoa thường) khớp băm này; 967 blob như thế ở đầu nhánh, đều thuộc tập lịch sử ấy (lần đo 15-10 trên 540 nhánh: 0/1102 và 831). "Sổ nợ P3" sống ở phiên điều phối, ngoài kho. Vế `check` không đọc các trường ấy đo lại: `grep -cE` năm tên trong `ops/lease_publish.py` tại `1d7e642` = 0 dòng (13:25:13Z 23-10-2026; tệp byte-identical với `c522c17`). Ngưỡng chủ kho #698 `6094652521`. Phạm vi do chủ kho chốt 15-10-2026 (Q7, Q8) và quyết định 15-10 cho r2 (test mới phải đăng ký vào sổ test sống) giữ nguyên. Issue #763 (`open`, `ducthangho`, `created_at 2026-10-15T23:26:04Z`; đọc lại 13:08:55Z 23-10-2026 vẫn `open`; tiêu đề "Packet NO-P3-DANG-KY-CI: đăng ký hai bộ test của #752 vào ci_dang_ky_test.py") nhận phần đăng ký của #752; phần đăng ký bộ test của #751 vẫn thuộc #751 (Mục tiêu 6). |
| `review_class` | **sensitive** — `ops/lease_publish.py` là cổng cấp lease (authority). Trần: ADR-0053 dòng 6, ≤ 6 tệp và ≤ 450 dòng thêm theo `git diff --numstat` — thay đúng cặp số `sensitive` của ADR-0044 dòng 5 (≤ 3 tệp, ≤ 300 dòng thêm); `docs/PROTOCOL_DA_PHIEN.md` §20 dòng 1514, 1522 tại `1d7e642` ghi cả hai ADR là `Accepted`, **0 cổng**. Trần mới CHỈ áp khi đặc tả mang đúng một dòng `tran_kich_thuoc_sensitive: ADR-0053@<OID land>` (ADR-0053 mục Hiệu lực, dòng 48–59): dòng ấy nằm ngay dưới bảng này, OID `8ab100793df9831505f495543a74044b91c2c9ab` (merge PR #791), và đo 13:17:29Z–13:17:31Z 23-10-2026 trên bản bare không nông vừa fetch `master` ⇒ `git cat-file -e <L>:docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md` rc 0 · cùng phép trên `<L>^1` rc 128 · `git rev-list --first-parent refs/remotes/origin/master` chứa `<L>` (rc 0 của `grep -qx`); đo lại 13:57:24Z 23-10-2026 trên bản bare của `depends_on` (2) (`git rev-parse --is-shallow-repository` ra `false`, `master` máy chủ khi ấy `8324567`): rc 0 · rc 128 · rc 0. Thiếu, trùng hay sai dòng ấy ⇒ trần cũ ≤ 3 tệp / ≤ 300 dòng thêm (fail-closed). Không cổng nào canh trần (ADR-0053 dòng 42–46): người cấp lease và reviewer đo bằng tay. Lời khai "không cổng nào" đo theo L6 (e) của `.claude/skills/soan-spec/SKILL.md` trên đủ sáu tệp cổng mà §20 liệt kê (`docs/PROTOCOL_DA_PHIEN.md` dòng 1473–1474), từng tệp, `git grep -c -w -F` trên cây `1d7e642`, 13:57:36Z 23-10-2026 (`do_cong.sh`): `ADR-0053`, `0053`, `tran_kich_thuoc_sensitive`, `450` ra 0 dòng ở cả sáu; `nang_tran`, `ai_nang`, `tran_cu`, `tran_moi` ra 0 ở `ops/lease_publish.py`, `.claude/dev/launcher.py`, `.claude/dev/gate_lifecycle.py`, `.github/workflows/ci.yml`, `.github/workflows/ops-publish-lease.yml`, và 8 · 4 · 2 · 5 dòng ở `.claude/dev/packet_loop.py` — ở đó `nang_tran` chỉ nâng hai trục `vong_review`, `codex_review_calls` (`TRUC_TRAN` dòng 60–61), không có trục kích thước. Nên câu "Không cổng nào canh trần" (trần kích thước của ADR-0053) đứng; số `có nhắc` ở `packet_loop.py` là trục khác, không phải cổng của ADR-0053. Đo `_tinh_lop_tu_write_set` gọi thẳng tại `1d7e642` (13:14:21Z 23-10-2026; `ops/lease_publish.py` byte-identical với `c522c17`, sha256 `d8079330007ab6ba53d328ba2d4abb1d4eb2737e2b5466b702ce9152958014f6`): từng đường dẫn của write set và cả ba cùng lúc ⇒ `sensitive` (`_BANG_LOP` mở ở dòng 59, mục `ops/lease_publish.py` ở dòng 65; hai tệp còn lại rơi về `sensitive` theo chú thích dòng 56–58); `ops/README.md` cũng ⇒ `sensitive`. |
| `executor` · `reviewer` | Claude (executor). Reviewer: lớp `sensitive` chạm security path ⇒ ADR-0036 dòng 9–10 và PROTOCOL §8 dòng 712–714 tại `1d7e642` (705–707 tại `c522c17`) đòi **Codex cross-review hoặc `human_audited`**; `review_deferred` bị cấm, `same_provider_approved` một mình không thay được (dòng 703 tại `1d7e642`, 696 tại `c522c17`). Subagent Claude Sonnet chỉ là lượt PHỤ; Sonnet không nằm trong `MO_HINH_CHO_PHEP` của `.claude/dev/chon_reviewer.py` (dòng 7). Bộ chọn: `--duong-dan` nhận MỘT chuỗi phân tách bằng dấu phẩy, lặp cờ thì chỉ giá trị CUỐI được dùng — đo 23:49:48Z (với `--so-dong` dưới 400 và `--luot` không quá 2; mỗi điều kiện vượt cộng thêm 1 vào tổng — đo lại 17-10-2026; hệ quả với trần 450: hàng `kich_thuoc`): lặp ba cờ ⇒ `claude-opus-5`/`xhigh`, "tổng=2", mất dòng "+2 chạm vùng cong"; dạng dấu phẩy cho ba đường dẫn ở 210, 280, 300 dòng ⇒ `claude-fable-5`/`xhigh`, "tổng=4" (23:50:09Z). Đo lại cả hai dạng tại `1d7e642` với `--review-class sensitive --luot 1` (13:14:21Z 23-10-2026; `chon_reviewer.py` không đổi từ `c522c17`): cùng kết quả. Đường dự phòng khi Codex không làm mới được: `human_audited` — KHÔNG merge chỉ với Sonnet. Chỉ P1/P2 chặn merge. |
| `base` | `1d7e642092fb3dda15967be44d095f37bb22ac5f` (merge PR #885) — nền ĐÓNG BĂNG của r4, đặt sau khi #748 merge: quyết định chủ kho 23-10-2026, https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792 (mục 2: ba đặc tả neo nền `1d7e642` và nâng revision, #751 lên r4; lúc cấp lease thực thi đo lại theo `depends_on` (3)). r4 KHÔNG đuổi theo `master`. `git ls-remote --heads origin` lúc 13:02:47Z 23-10-2026: 558 nhánh, `master` máy chủ = `1d7e642`; đọc lại 13:20:16Z 23-10-2026: 560 nhánh, `master` vẫn `1d7e642`; lúc 13:54:20Z 23-10-2026: 562 nhánh, `master` máy chủ = `8324567` — đúng một merge first-parent sau `1d7e642` (PR #891; 4 commit, 53 tệp), và `git diff --numstat 1d7e642 8324567` trên ba tệp write set, ba bộ đo nền, `.claude/skills/soan-spec/SKILL.md`, `.claude/dev/chon_reviewer.py` và ADR-0053 ra rỗng (`depends_on` (3) chưa kích hoạt lúc ấy). Từ `c522c17` (nền r3 được duyệt, merge PR #762) tới `1d7e642`: 522 commit (73 trên first-parent), 1574 tệp. `git diff --numstat c522c17 1d7e642` trên tệp spec này dẫn: ĐỔI `.claude/dev/ci_dang_ky_test.py` +222/−30 (write set VÀ bộ đo nền), `ops/lease_publish_test.py` +476/−102, `ops/ci_duong_nhanh_test.py` +162/−47, `.github/workflows/ci.yml` +122/−7, `.github/workflows/launcher-windows.yml` +9/−11, `docs/PROTOCOL_DA_PHIEN.md` +41/−19, `.claude/skills/soan-spec/SKILL.md` +54/−2, `ops/reviews/README.md` +18/−0, cùng ba ADR mới `0052`–`0054`; KHÔNG ĐỔI (0 dòng) `ops/lease_publish.py`, `ops/ci_duong_nhanh.py`, `ops/README.md`, `.github/workflows/ops-publish-lease.yml`, `.gitattributes`, `.claude/dev/chon_reviewer.py`, ADR-0036, ADR-0044 ⇒ mọi số dòng spec dẫn vào các tệp không đổi vẫn đúng tại `1d7e642`; số dòng dẫn vào các tệp đã đổi được đo lại tại chỗ (mục `Đo lại nền sau #748 merge`). Lịch sử nền: r3 soạn và được duyệt trên `c522c17`; từ `6f121a3` (nền r2) tới `c522c17`: 17 commit, 87 tệp, toàn `ops/**`; `git diff --numstat 6f121a3 c522c17` ra rỗng trên các đường dẫn tệp mà spec này nêu đầy đủ, TRỪ ba tệp trong `ops/`: `ops/reviews/README.md` +12/−0 (dòng 484 dời từ 482, mục Hình dạng kế thừa), `ops/land/pr759-no-p3-ho-so-land-evidence.yaml` +440/−0 (tệp mới ở khoảng ấy; dòng 407–418 đo tại `c522c17`) và `ops/specs/no-p3-lease-spec-hash-r2.md` +258/−0 (tệp mới: chính r2); đo lượt 18, 23-10-2026. #748 ĐÃ merge vào `master` (merge first-parent của #748 trong `c522c17..1d7e642`: PR #849 `9422054`, #862 `401d4f1`, #869 `7400df4`, #882 `8223fd2`; Issue #748 `closed`/`completed` lúc 2026-10-20T01:19:38Z, đọc 13:08:55Z 23-10-2026, đọc lại 13:56:11Z–13:56:14Z 23-10-2026: như cũ) — mọi số đo nền đã ĐO LẠI trên `1d7e642` (L5 của `.claude/skills/soan-spec/SKILL.md`, `depends_on` (3), A0; mục `Đo lại nền sau #748 merge`); không lease nào được cấp trước đó. |
| `write_set` | `ops/lease_publish.py` · `ops/lease_publish_spec_hash_test.py` (MỚI) · `.claude/dev/ci_dang_ky_test.py` (+1 dòng `MOI`, Mục tiêu 6) — giữ nguyên ba tệp của r2 và r3. `ops/README.md` KHÔNG vào: thiết kế (từ r3, giữ ở r4) giữ runbook đúng (hàng C1). Đường dự phòng "đưa README vào write set" sẽ là tệp THỨ TƯ: lúc soạn r3 nó vượt trần sensitive 3 tệp của ADR-0044 (cần ngoại lệ trần của chủ kho hoặc tách phần đăng ký); dưới trần 6 tệp của ADR-0053 mà r4 áp (hàng `review_class`) nó KHÔNG còn vượt trần, nhưng vẫn là đổi write set ⇒ revision mới. Lý do loại README là hàng C1, không phải trần. |
| `depends_on` | **CHẶN cấp lease** cho tới khi ĐỦ năm điều kiện, đo lại lúc cấp (số trong ô này không thay được phép đo lúc cấp). **(1)** #748 đã MERGE vào `master` — không chỉ vào `mission/748/integration`. Merge là đủ, không đòi hồ sơ land ghi `landed: true` (quyết định chủ kho 23-10-2026, https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792, mục 1): bốn hồ sơ land của #748 tại `1d7e642` — `ops/land/pr849-wp748-land-evidence.yaml`, `ops/land/pr862-wp748-r21-land-evidence.yaml`, `ops/land/pr869-wp748-r22-land-evidence.yaml`, `ops/land/pr882-wp748-r23-land-evidence.yaml` — đều ghi `landed: false` (đo 14:00:44Z 23-10-2026, `do_land748.sh`) và KHÔNG chặn đặc tả này. Đo 13:08:55Z 23-10-2026: ĐÃ — bốn merge first-parent của #748 nằm trong `c522c17..1d7e642` (hàng `base`), Issue #748 `closed`/`completed` lúc 2026-10-20T01:19:38Z. Lần đo 23:31:42Z 15-10: CHƯA (`c522c17..origin/master` khi ấy = 7 commit, toàn spec wp728; Issue #748 `open` lúc 23:57:40Z). **(2)** Trên một clone ĐỦ ref — so `git ls-remote --heads origin` với `git for-each-ref refs/remotes/origin` (bỏ `HEAD`) theo tập tên VÀ OID: thiếu 0, lệch 0, VÀ `git remote get-url origin` ra `https://github.com/ducthangho/tra-luat` (hoặc dạng có `.git`) — nếu `origin` là một bản sao cũ thì `ls-remote` và `for-each-ref` cùng mù và cùng khớp, còn `ai-dang-giu` ra `NGƯỜI_GIỮ 0`, rc 0 cho đường dẫn mà máy chủ đang có người giữ; khác URL hoặc không chạy được ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp — `python3 ops/lease_publish.py ai-dang-giu <đường dẫn> --root <bản bare>` ra `NGƯỜI_GIỮ 0`, rc 0, cho từng đường dẫn của write set. Mọi lệnh của (2), kể cả bước cần mạng, chạy dưới hợp đồng môi trường đo (Số đo nền); phép so chạy TRONG bản bare vừa `fetch`, và chỉ so khi `git for-each-ref refs/remotes/origin` trong bản bare ấy in ít nhất một dòng — in 0 dòng ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp. **ĐỎ hiện tại.** Đo lại lúc soạn r4, 13:54:13Z–13:55:20Z 23-10-2026, trên một bản bare MỚI (`git clone --bare --reference` kho cục bộ từ `https://github.com/ducthangho/tra-luat`, 13:54:13Z–13:54:16Z; rồi trong cùng MỘT lệnh `fetch --prune origin '+refs/heads/*:refs/heads/*' '+refs/heads/*:refs/remotes/origin/*'`, 13:54:20Z; `ls-remote --heads origin` 13:54:20Z; `adg_r4.sh`): 562 nhánh máy chủ; so tập tên + OID với cả `refs/remotes/origin` (bỏ `HEAD`) lẫn `refs/heads` ra thiếu 0, thừa 0, dòng lệch 0; `remote get-url` ra đúng URL trên. Kết quả: `ops/lease_publish.py` `NGƯỜI_GIỮ 0` rc 0 (13:54:21Z); `ops/lease_publish_spec_hash_test.py` `NGƯỜI_GIỮ 0` rc 0 (13:54:41Z); `.claude/dev/ci_dang_ky_test.py` `NGƯỜI_GIỮ 1: wp892-r2-g2-claude`, **rc 11** (13:55:00Z) — lease r2 của #892 (Issue #892 `open` lúc 13:56:11Z–13:56:14Z 23-10-2026; nhánh `ops/wp892-r2-g2-lease` @ `5603c9d3`, commit 13:46:21Z 23-10-2026, `lease_expires_at_utc 2026-10-24T13:46:00Z`, write set 4 đường dẫn y như r1, `spec_path ops/specs/wp892-r2.md`, `thay_the_cho: [wp892-r1-g1-claude]`, `base_sha` = `1d7e642`). Cùng lượt in `CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ` cho `wp892-r1-g1-claude` (nhánh `ops/wp892-r1-g1-lease` nay @ `d5322243`, mang `da_bi_thay_the: wp892-r2-g2-claude`, hạn `2026-10-24T13:01:00Z`) và cho `wp878-r1-g1-claude`, không tính là người giữ. Lượt thứ hai 14:03:55Z–14:04:56Z 23-10-2026 (563 nhánh, thiếu 0, thừa 0, dòng lệch 0): `.github/workflows/ci.yml` và `ops/ci_duong_nhanh_test.py` cùng `NGƯỜI_GIỮ 1: wp892-r2-g2-claude` rc 11, `ops/lease_publish_test.py` `NGƯỜI_GIỮ 0` rc 0. Nên lease thực thi của #751 CHỜ lease `wp892-r2-g2-claude` hết hạn (`2026-10-24T13:46:00Z`) hoặc bị thu hồi, rồi đo lại (2) — người giữ đã đổi một lần trong ngày (r1 cấp 13:01:49Z, r2 thay nó 13:46:21Z), nên tên người giữ ở đây không thay được phép đo lúc cấp; nếu #892 land thì đo lại theo (3). Lần đo trước, 13:20:16Z–13:23:31Z 23-10-2026, trên bản bare đủ ref (thiếu 0, thừa 0, OID khớp, 560 nhánh; `remote get-url` ra đúng URL trên): `ops/lease_publish.py` 0 rc 0; `ops/lease_publish_spec_hash_test.py` 0 rc 0; `.claude/dev/ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 1: wp892-r1-g1-claude`, **rc 11** — lease r1 của #892 (nhánh `ops/wp892-r1-g1-lease` @ `62fb3c1a`, commit 13:01:49Z 23-10-2026, `lease_expires_at_utc 2026-10-24T13:01:00Z`, write set 4 đường dẫn `ops/cong_cu_test.py`, `.github/workflows/ci.yml`, `.claude/dev/ci_dang_ky_test.py`, `ops/ci_duong_nhanh_test.py`; `spec_path ops/specs/wp892.md`; `thay_the_cho: []`; `base_sha` = `1d7e642`); cùng lượt in thêm `CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ wp878-r1-g1-claude`, không tính là người giữ. Lượt đầu 12:58:12Z–13:01:25Z 23-10-2026 (556 nhánh lúc 12:58:02Z cùng ngày) cho `ci_dang_ky_test.py` rc 0 — lease #892 được cấp SAU lượt ấy. Lúc soạn r3 (23:32:15Z–23:33:09Z 15-10, 541 nhánh) người giữ là lease r11 của #748 (`wp748-r11-g11-claude-windows-20261015`, nhánh `ops/wp748-r11-g11-lease` @ `181e3fbd`, hạn `2026-10-16T04:27:21Z`). Hai đường ra `KHÔNG_XÁC_ĐỊNH` đo được trong lần đo lại, cả hai fail-close rc 12: (a) nhánh tạo trên máy chủ sau lần fetch (`cache thiếu nhánh máy chủ: ops/wp892-spec`, 13:01:25Z 23-10-2026); (b) `ai-dang-giu` quét `refs/heads/*` của bản bare (dòng đầu nó in: `PHẠM_VI: quét refs/heads/*`), nên bản bare clone từ trước mà chỉ fetch vào `refs/remotes/origin/*` ra rc 12 `NHÁNH_CỤC_BỘ_TỤT_SAU` (13:01:56Z–13:02:22Z 23-10-2026, cả 7 đường dẫn đã hỏi); lượt đo cuối fetch `'+refs/heads/*:refs/heads/*' '+refs/heads/*:refs/remotes/origin/*'` trong cùng một lệnh. Kho cục bộ `/home/user/tra-luat` lúc 13:23:41Z 23-10-2026 có 538 nhánh `refs/remotes/origin/*` so với 560 trên máy chủ: thiếu 91 (trong đó `ops/wp892-r1-g1-lease`), thừa 69, lệch OID 1 — đo trên bộ đệm ấy là mù đúng lease đang giữ (lúc 23:31:30Z 15-10: thiếu 4, lệch OID 3). **(3)** Điều kiện này ĐÃ xảy ra một lần: `c522c17..1d7e642` đổi `.claude/dev/ci_dang_ky_test.py` (write set) và cả ba bộ đo nền (hàng `base`); nền đã dời sang `1d7e642` bằng revision MỚI r4 (quyết định chủ kho 23-10-2026, comment ở ô (1), mục 2), số đo lại ghi ở mục `Đo lại nền sau #748 merge`. r4 không đuổi theo `master`; LÚC CẤP lease thực thi: nếu bất kỳ commit nào sau `1d7e642` trên `master` đổi một tệp của write set hoặc một bộ đo nền (`ops/lease_publish_test.py`, `ops/ci_duong_nhanh_test.py`, `.claude/dev/ci_dang_ky_test.py`) ⇒ không cấp trên nền `1d7e642`; dời nền bằng revision mới và đo lại mọi số ở Số đo nền TRƯỚC khi cấp. Đo 13:54:20Z 23-10-2026: `master` = `8324567`, 0 dòng đổi trên các tệp ấy (hàng `base`) ⇒ chưa kích hoạt. Lease r2 của #892 (ô (2)) khai `.claude/dev/ci_dang_ky_test.py` và `ops/ci_duong_nhanh_test.py` ⇒ nếu #892 land trước lúc cấp thì (3) kích hoạt. **(4)** Write set giao với #763 (`no-p3-dang-ky-ci`) và — từ 13:01:49Z 23-10-2026 (lease r1, nay là lease r2 từ 13:46:21Z) — với lease còn hạn của #892, cùng ở `.claude/dev/ci_dang_ky_test.py` ⇒ không lease nào của #751 được đồng thời với lease của hai packet ấy; packet land sau phải qua (3). Nếu #763 land trước, N của A7 đổi (`ops/specs/no-p3-dang-ky-ci-r1.md` dòng 19 tại `c3f6f5f` vẫn khai +2 dòng `MOI`: 24 ⇒ 26, đích của #751 thành `27/27`; lúc soạn r3: 23 ⇒ 25, `26/26`); #763 đang soạn r2 song song với r4 này — đo lại lúc cấp. Đặc tả #892 hiện hành (`ops/specs/wp892-r2.md` @ `d90d847f`, nhánh `ops/wp892-spec`, 78 dòng, sha256 `aeac5b18…` bằng `spec_sha256_required` của lease r2; đọc 13:58:03Z 23-10-2026, `do_wp892_r2.sh`): 0 dòng chứa `MOI`, `DA_NOI`, `DANG_KY` hay `ĐĂNG KÝ` (phân biệt hoa thường) và 0 dòng cho ba tên đầu khi không phân biệt hoa thường, khớp nguyên từ; 3 dòng khớp `đăng ký`, `đăng kí`, `dang ky` hoặc `dang_ky` không phân biệt hoa thường — hai là tên tệp `ci_dang_ky_test.py` (dòng 28, 62), một là "đăng ký trong `DOT_BIEN` của bộ" (dòng 60: đột biến của chính bộ test, không phải sổ); 2 dòng nhắc `ci_dang_ky_test` — nó đổi sổ và hai bộ đo nền, không đổi N theo chữ (spec r1 `ops/specs/wp892.md` @ `8a0c3672`, đọc 13:27:32Z 23-10-2026: 0 dòng với mẫu phân biệt hoa thường, 2 dòng nhắc `ci_dang_ky_test`). Bản r3 của #752 (`ops/specs/no-p3-cong-cu-ho-so-r3.md` dòng 16 tại `c3f6f5f`) đã đưa sổ RA khỏi write set của nó — giao #751↔#752 ở sổ không còn; #752 đang soạn r4 song song — đo lại lúc cấp. **(5)** Có bằng chứng bền (đường dẫn comment) cho quyết định chủ kho 15-10 về sổ test sống VÀ cho đồng ý đi tiếp ở ngưỡng L4 (mục Hình dạng kế thừa). Hiện trạng lúc soạn r4 (13:54Z–14:05Z 23-10-2026; hạn lease đang giữ `2026-10-24T13:46:00Z`, nên (2) phải đo lại lúc cấp): (1) ĐÃ (merge; quyết định chủ kho, mục 1) · (2) ĐỎ (rc 11, lease `wp892-r2-g2-claude`) · (3) đã xảy ra một lần, xử bằng r4; chưa kích hoạt lại lúc 13:54:20Z; còn treo theo #892 · (4) chờ (#763 `open` lúc 13:56:11Z–13:56:14Z 23-10-2026; #892 đang giữ sổ) · (5) chưa. Lần đo lại trước (12:58Z–13:28Z 23-10-2026): (1) ĐÃ · (2) ĐỎ (rc 11, lease r1 của #892) · (3) đã xảy ra một lần · (4) chờ · (5) chưa. Lúc soạn r3 (23:31Z–23:58Z 15-10): (1) chưa · (2) ĐỎ (rc 11, lease r11 của #748) · (3) chờ (1) · (4) chờ · (5) chưa. |
| `kich_thuoc` | 3 tệp — trong trần sensitive 6 tệp của ADR-0053 mà r4 áp (hàng `review_class`), dư 3 tệp (trần cũ ADR-0044 dòng 5: 3 tệp, dư 0). Trần cứng 450 dòng thêm theo `git diff --numstat` (ADR-0053 dòng 6; trần cũ 300). Mọi số kích thước dưới đây đo trên `ops/lease_publish.py` của `c522c17`, byte-identical tại `1d7e642` (hàng `base`), nên giữ nguyên; chỉ phép so với trần đổi. Đo bản THĂM DÒ của lượt soạn r3 (KHÔNG giao; dựng từ chữ Mục tiêu 1–3, 5 lên bản sao `c522c17`, 23:35Z): `ops/lease_publish.py` +54/−0, 5 hunk (`-25,0 +26` · `-52,0 +54` · `-1116,0 +1119,49` · `-2294,0 +2346` · `-2305,0 +2358,2`), chưa gồm sửa chú thích dòng 2313 (ước +1/−1) và chưa gồm sửa docstring dòng 15–16 (Mục tiêu 1, thêm sau lượt 3); `ci_dang_ky_test.py` +1/−0 (số reviewer lượt 2) ⇒ bộ test còn ≤ 244 dòng theo ước ấy (theo số đo lượt 3 dưới, +56 đã gồm sửa chú thích: ≤ 243 dòng, và ≤ 241–242 khi tính thêm sửa docstring dòng 15–16, đo lượt 4 dưới). r4, như r3, đòi **40 ca** (A1 1 · A2 5 · A2b 3 · A3 5 · A3b 3 · A3c 2 · A4 6 · A4b 9 · A5 4 · A5b 2). Viết tay từng ca KHÔNG vừa (reviewer lượt 2: 27 ca viết tay = 461 dòng ⇒ 52 + 1 + 461 = 514 > 450, và > 300 của trần cũ) ⇒ bộ test PHẢI dạng bảng: một hàm dựng kho, một hàm chạy `check`, một bảng ca. Số "24 ca dạng bảng = 144 dòng" là của reviewer lượt 1, không tái lập. Đo lượt 3 (16-10-2026, cửa sổ 02:12Z–02:55Z; bản dựng KHÔNG giao): đúng 40 ca dạng bảng viết dày = 239 dòng (241 khi thêm dòng BỎ QUA CÓ TÊN trên `nt` mà Mục tiêu 4 đòi) ⇒ `git diff --numstat` +56/−1 (kể cả sửa chú thích dòng 2313) · +239/−0 · +1/−0 = 296 (298) dòng thêm, CHƯA gồm sửa docstring dòng 15–16; đo lượt 4 (16-10-2026, bản thăm dò lượt 4 KHÔNG giao, trên `ops/lease_publish.py` nền): sửa docstring ấy thêm +1/−1 và một hunk khi nối vào dòng 16, hoặc +2/−1 và một hunk khi bọc dòng ⇒ 297–298 (299–300) dòng thêm ≤ 450, dư 153–152 (151–150) — so trần cũ 300: dư 3–2 (1–0); cùng bộ test 239 dòng ấy qua `ruff format --line-length 100` = 374 dòng, `--line-length 88` = 428 dòng ⇒ dưới trần cũ 300 ngân sách ≤ 243 dòng chỉ đủ khi giữ kiểu dày (mỗi ca một hàng bảng, dòng tới ~155 ký tự; nền, dòng dài nhất tính bằng KÝ TỰ: `lease_publish.py` 161, `lease_publish_test.py` 248 — tính bằng BYTE: 174 và 270; đo lượt 4, 16-10-2026, `c522c17`); dưới trần 450, ngân sách bộ test là 450 − 57 − 1 = 392 dòng (nối docstring) hoặc 450 − 58 − 1 = 391 dòng (bọc dòng), nên bản 374 dòng của `--line-length 100` (đo trên bản 239 dòng, chưa gồm dòng BỎ QUA trên `nt`) cũng vừa, dư 18–17, còn bản 428 dòng của `--line-length 88` vượt 36–37 — kiểu dày không còn bắt buộc theo trần (phép tính 23-10-2026 từ các số đo ấy, không dựng lại bản thăm dò 40 ca; dòng dài nhất đo lại 13:28:58Z 23-10-2026 tại `1d7e642`: vẫn 161/248 ký tự, 174/270 byte, và cùng kịch bản tái lập đúng bốn số ấy tại `c522c17`); executor đo `git diff --numstat <nền>` (tệp mới đã `git add -N` hoặc đã commit — xem A7) ngay khi bộ test xanh. Vượt 450 dòng thêm ⇒ dừng TRƯỚC review và soạn revision, hoặc khai khối `nang_tran` (ADR-0053 dòng 32–38); cần tệp thứ tư là đổi write set ⇒ revision mới — trần 6 tệp không thay được việc ấy. **Hệ quả đã biết của trần 450, khai trước:** ứng viên 400–450 dòng thêm vẫn trong trần nhưng làm bộ chọn reviewer cộng bậc — `.claude/dev/chon_reviewer.py` dòng 94 cộng 1 khi `--so-dong` ≥ 400. Đo 13:57:16Z 23-10-2026 dưới hợp đồng môi trường đo, `--review-class sensitive --luot 1`, ba đường dẫn write set dạng dấu phẩy: `--so-dong` 300 và 399 ⇒ `claude-fable-5`/`xhigh`, "tổng=4"; 400 và 450 ⇒ `claude-fable-5`/`max`, "tổng=5", thêm khoản "+1 số dòng=… >= 400"; 450 cùng `--luot 3` ⇒ `claude-fable-5`/`max`, "tổng=6" (13:57:24Z). Tức effort lên `max` ngay lượt đầu, họ model không đổi. Theo các số ở trên: bản dày (297–300 dòng thêm) dưới ngưỡng 400; bản `--line-length 100` (374 + 57 + 1 = 432 hoặc 374 + 58 + 1 = 433) trên ngưỡng. Đặc tả KHÔNG đổi trần hay ép kiểu dày vì việc này; người cấp lease tính nó vào ngân sách review và truyền đúng `--so-dong` đo bằng `git diff --numstat <nền>`. |

tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

## Thay đổi so với r3

r4 là revision MỚI vì đổi nền: quyết định chủ kho 23-10-2026, https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792 (tác giả `ducthangho`, `created_at 2026-10-23T13:54:01Z`; đọc bằng `gh api repos/ducthangho/tra-luat/issues/comments/6366519792` lúc 13:56:11Z 23-10-2026), mục 2: ba đặc tả neo nền `1d7e642` và nâng revision, #751 lên r4; lúc cấp lease thực thi đo lại theo `depends_on` (3). Thiết kế, write set, yêu cầu của Mục tiêu 1–6 và 40 ca giữ nguyên.

- **Nền** `c522c17` → `1d7e642` (merge PR #885), đóng băng, không đuổi theo `master`; mọi số ở Số đo nền đo lại trên `1d7e642` (mục `Đo lại nền sau #748 merge`); A0 chạy lại trên `1d7e642`, `master` lúc cấp chỉ dùng cho `depends_on` (3). Gỡ lời khai lệch thủ tục của bản nháp `5fc0048` (hàng `depends_on`, ô (3) của nó: "làm TẠI CHỖ trong r3 theo chỉ thị phiên điều phối, KHÔNG bằng revision mới như chữ gốc của ô này đòi (lệch thủ tục, khai thẳng ở đây)"): nay đổi nền đúng bằng revision mới.
- **`depends_on` (1)** theo mục 1 của cùng quyết định: #748 merge vào `master` là đủ; bốn hồ sơ land của #748 ghi `landed: false` không chặn.
- **`depends_on` (2)** đo lại 13:54Z–14:05Z 23-10-2026: người giữ `.claude/dev/ci_dang_ky_test.py` nay là lease r2 của #892 (`wp892-r2-g2-claude`, hạn `2026-10-24T13:46:00Z`), thay lease r1 mà lần đo trước thấy.
- **Trần:** khai `tran_kich_thuoc_sensitive: ADR-0053@8ab1007…` ⇒ ≤ 6 tệp / ≤ 450 dòng thêm thay ≤ 3 / ≤ 300. ADR-0053 mục Hiệu lực (dòng 48–59) chỉ đòi dòng khai và ba phép đo OID, không đòi duyệt riêng. Lời khai "không cổng nào canh" đo trên đủ sáu tệp cổng (hàng `review_class`); hệ quả với bộ chọn reviewer ở 400–450 dòng (hàng `kich_thuoc`).
- **Tiêu chí khớp chuỗi theo L6** của `.claude/skills/soan-spec/SKILL.md` (dòng 84–125 tại `1d7e642`): luật chung ở đầu Nghiệm thu; A1 (fixture không `prompt_path` — có `prompt_path` = `spec_path` thì vế dương xanh sẵn trên nền); A2 (4), A3c, A4b (8) (đủ ba phần thông điệp cộng vế âm `đã commit tại HEAD`, đóng nhóm (8) của Chưa đo được); A2b (iii), A4b (2) (4)–(7), A5, A5b (khớp TRỌN cụm Mục tiêu đặt; A5b thêm vế âm ở ca đối chứng); A6b (khối chú thích đã nối thay `grep -c` theo dòng, thêm vế dương); A7 (chép nguyên qua AST, numstat của sổ, đếm dòng `số/số` bằng chính mẫu của sổ). Số chạy thử trên nền và trên bản thăm dò dựng lại chỉ được ghi cho luật chung, A1, A2 (4), A4 (ca đầu), A5 (1),
A5b, A6b và A7 (phép AST); các chỗ viết lại còn lại — A2b (iii), A3c, A4b (2) và (4)–(8), A5 (2)–(4), A7 (numstat của sổ; đếm dòng `số/số`, cái sau chưa chạy được vì bộ test chưa có) — chưa ghi số chạy thử trong spec này.

## Thay đổi so với r2

r3 viết lại từ r2 (không áp `HINT.patch` máy móc: 3/11 hunk được viết cho thiết kế đọc `HEAD` của r2 và sai với thiết kế r3 — xem bảng thứ hai). Mọi con số mới của lượt soạn r3 đều đo lại trên `c522c17` hoặc bản sao của nó, kèm thời điểm (giờ UTC, ngày 15-10-2026 trừ chỗ ghi ngày khác); số do các bản vá review thêm sau nằm ngoài câu này; số của lần đo lại sau khi #748 merge đo trên `1d7e642` hoặc bản sao của nó ngày 23-10-2026, ghi ngày tại chỗ và liệt kê ở mục `Đo lại nền sau #748 merge`; số nào không đo lại thì ghi rõ là số của reviewer.

| # | nguồn · hạng | id lớp | chỗ sửa trong r3 |
|---|---|---|---|
| C1 | Codex PR #762 · P2 | `discussion_r4286041913` "Keep the documented pre-commit lease check usable" | Mục tiêu 1 (luật NGUỒN: spec đọc từ ĐĨA dưới `_goc_kho(tep, goc)`, cùng nguồn với tệp lease và `prompt_path` trong `check`; bỏ đọc `HEAD`); Số đo nền (phép đo hành vi nguồn đọc của `check`); A3 viết lại (5 ca, đột biến "đọc `HEAD`" làm đỏ cả năm); A3c mới (đúng trình tự runbook tới đường đăng); hàng `write_set` (README không vào, lý do); Ngoài phạm vi. |
| B1 | lượt 2 · P3 | `a5b-chuoi-bia-mo-lech-muc-tieu-5` | Mục tiêu 5: chuỗi `đã bị thay thế — bia mộ — không kiểm băm`; A5b đo chuỗi con `bia mộ — không kiểm băm`. |
| B2 | lượt 2 · P3 | `hermetic-thieu-cau-hinh-git-cuc-bo` | Mục tiêu 4 (cấu hình git cục bộ, cô lập cấu hình toàn cục, mọi `git clone` kèm `-c core.autocrlf=false`); lý do đo lại dưới thiết kế đĩa (bảng thứ hai, hàng c). |
| B3 | lượt 2 · P3 | `dong-cuoi-bo-test-phai-la-N-tren-N-mot-minh` | Mục tiêu 4 (dòng `N/N` đứng một mình là dòng DUY NHẤT có dạng số/số, và là dòng cuối — hàng g); A7 (phép `chay_moi`). |
| B4 | lượt 2 · P3 | `yeu-cau-muc-tieu-1-chua-co-tieu-chi-do` | Mỗi yêu cầu mà lượt 2 liệt kê (tám đột biến sống sót bộ A của r2) có một ca và một đột biến: A1 (dòng "ĐĂNG ĐƯỢC" và băm 12 ký tự); A2 (thông điệp lệch nêu trường · giá trị khai · giá trị đo; rc 13 KHÔNG kèm "ĐĂNG ĐƯỢC"; thông điệp tệp vắng); A2b (iii) và A4b (thông điệp "64 ký tự hex thường"); A4 (dòng bằng chứng write set; phần tử không phải chuỗi); A5 (ca 3, 4: `spec_path` không băm, `spec_hash: null`). Các yêu cầu khác của Mục tiêu 1–6 CHƯA có ca nào: sáu do lượt 3 đo, năm nhóm do lượt 4 đo, năm nhóm do lượt 5 đo (mục Chưa đo được) — danh sách các nhóm ĐÃ ĐO THẤY, KHÔNG phải tập đóng. |
| B5 | lượt 2 · P3 | `kich-thuoc-viet-tay-15-ca-thieu-so-voi-26-ca` | Hàng `kich_thuoc` (đếm 40 ca của r3, đo bản thăm dò +54, buộc dạng bảng). |
| B6 | lượt 2 · P3 | `a6-so-tuyet-doi-phu-thuoc-so-ref-cua-clone` | A6 (i): tiêu chí là TẬP lease đổi rc; số tuyệt đối đo lại trên `c522c17` (rồi trên `1d7e642`, 23-10-2026) kèm điều kiện ref (clone làm việc của Số đo nền; số ref cục bộ đếm bằng `git for-each-ref refs/heads refs/remotes` bỏ `/HEAD`, không ghi thành chữ số). |
| B7 | lượt 2 · P3 | `luat-hai-truong-chua-nhat-quan-fixture-va-dang-sai` | Mục tiêu 1 (kiểm DẠNG mọi trường băm có mặt TRƯỚC khi chọn trường quyết định); A2 (tiền đề fixture: lease CHỈ mang trường được sửa); A2b (iii) mới. |
| B8 | lượt 2 · P3 | `chu-thich-check-thuan-va-body-cung-cong-se-sai` | Mục tiêu 1 (chú thích dòng 2313 PHẢI sửa; dòng 2295–2296 nay GIỮ ĐÚNG vì `check` vẫn không chạm git — đo, hàng b); A3 (v) khoá "check THUẦN"; A6b khoá chú thích. |
| G1 | lượt 2 · ghi nhận IV.2 | lời dẫn `depends_on` (4) trỏ r1 của #752 | `depends_on` (4) viết lại: giao nay là #751↔#763. |
| G2 | lượt 2 · ghi nhận IV.3 | trôi ảnh chụp ref (12 → 13 blob hai trường) | Mọi số trên toàn ref đo lại trên bản bare đủ ref, so tên + OID với `ls-remote` trước khi đo (17 blob hai trường, 15 bằng, 2 khác; đo lại 13:29:49Z 23-10-2026: 62, 60 bằng, 2 khác — Số đo nền). |
| G3 | lượt 2 · ghi nhận IV.4 | nền sẽ phải dời | Hàng `base`, `depends_on` (3), A0. |
| G4 | lượt 2 · ghi nhận IV.5 | `spec_hash` không kèm `spec_path` (15/612 blob) | Mục tiêu 1: thông điệp "spec: không khai — không kiểm" giữ, chấp nhận như lease cũ (15/619 blob đo lại; 15/680 lúc 13:29:49Z 23-10-2026). |
| G5 | lượt 2 · ghi nhận IV.1 | trần ADR-0044 chờ chủ kho | Hàng `kich_thuoc`; không đổi trần. Sau đó ADR-0053 (land `8ab1007`) thay cặp số `sensitive`; lần đo lại 23-10-2026 áp nó qua dòng `tran_kich_thuoc_sensitive` dưới bảng đầu (hàng `review_class`). |

Lệch `HINT.patch` lượt 2, hoặc ngoài HINT:

| hàng | chỗ | vì sao |
|---|---|---|
| (a) | A2 ca 4, Mục tiêu 1 | Hunk `@@ -180` của B4 đòi thông điệp tệp vắng nêu "đã commit tại HEAD" — đúng cho r2, SAI cho r3. Thông điệp r3: "không có tệp … spec phải nằm trong cây cùng lease" (bản thăm dò in đúng như vậy, 23:37:35Z). |
| (b) | Mục tiêu 1, B8 | Hunk `@@ -110` khai HAI chú thích thành sai. Dưới thiết kế r3 chỉ dòng 2313 thành sai; dòng 2295–2296 ("bộ kiểm THUẦN … Chỉ khi `--du-bao` mới chạm git") vẫn đúng. Đo A/B (23:37:35Z): kho git, spec khớp, PATH trỏ thư mục rỗng ⇒ bản thăm dò ĐĨA rc 0, bản đúng chữ r2 (đọc `HEAD`) rc 12; spec lệch ⇒ `check` 13 · `body` 0 ở bản đĩa. |
| (c) | Mục tiêu 4, B2 | Lý do của hunk `@@ -127` ("`core.autocrlf=true` đổi blob CRLF thành LF ở `git add` ⇒ ca CRLF đỏ") không còn áp: ca CRLF r3 đọc ĐĨA. Nhưng cấu hình toàn cục vẫn phá bộ test qua đường khác khi CHƯA có lớp (b) của Mục tiêu 4 — đo 23:52:28Z: `HOME` có `core.autocrlf=true`, `git clone` trần của kho không có `.gitattributes` (như kho tạm `git init`) ⇒ spec trên đĩa của clone thành `73 70 65 63 20 41 0d 0a` ⇒ `check` 13 (ĐỎ GIẢ ở A3c); cùng clone kèm `-c core.autocrlf=false` ⇒ `73 70 65 63 20 41 0a`, rc 0; kho nguồn có `* text=auto eol=lf` (như `.gitattributes` dòng 8) thì cả hai cho `0a` (đo 17-10-2026, git 2.43.0); có lớp (b) (`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL` trỏ một tệp rỗng) thì `HOME` có `core.autocrlf=true` vẫn cho clone trần của kho không có `.gitattributes` ra `73 70 65 63 20 41 0a` (đo 17-10-2026, git 2.43.0), nên lớp (d) là lớp thứ hai. Năm dãy byte của hàng này đo lại 17-10-2026 (14:03:36Z, git 2.43.0) dưới hợp đồng môi trường đo (Số đo nền) cộng đúng một độ lệch: MỘT `HOME` rỗng (`H="$(mktemp -d)"`, rồi `HOME="$H"` thay cho `HOME="$(mktemp -d)"` của tiền tố) dùng CHUNG cho lệnh `git config --global core.autocrlf true` và cho mọi lệnh `git clone` đo sau nó (vế lớp (b) thêm hai biến của lớp ấy): khớp cả năm. Theo đúng chữ tiền tố (mỗi lệnh một `HOME` mới) lệnh ghi cấu hình không tới được lệnh clone: cả năm dãy ra `73 70 65 63 20 41 0a`, dãy thứ nhất KHÔNG phải `0d 0a` (đo lượt 16, 17-10-2026, git 2.43.0) — nên độ lệch này phải nêu `HOME` dùng chung. Yêu cầu hermetic giữ, lý do đổi. |
| (d) | A4b | Ca "PATH không có git ⇒ rc 12" của r2 BỎ: r3 không gọi git, ca ấy nay là A3 (v) với đáp án rc 0. Trạng thái thứ ba đổi thành "Có tệp mà `read_bytes()` ném `OSError` ⇒ `RC_KHONG_XAC_DINH` 12" (Mục tiêu 1 (vi); ca trong tiến trình, chèn lỗi: A4b (9)). |
| (e) | A4b, CRLF | Đột biến của ca CRLF đổi từ "đọc qua `GOI_GIT`/`_git`" sang "đọc văn bản" (`read_text` rồi mã hoá lại): đo 23:56:43Z ⇒ ca CRLF rc 13, ĐỎ. Đột biến "đọc blob tại `HEAD`" thuộc A3. |
| (f) | Mục tiêu 1, NUL | Cơ chế cụ thể dưới thiết kế đĩa (Python 3.11.15, đo 23:35Z): `PurePosixPath` nhận chuỗi có NUL không ném; `Path.resolve()` ném `ValueError: embedded null byte`; `Path.is_file()` trả `False`; `read_bytes()` ném `ValueError`. Nên chốt NUL đứng TRƯỚC `resolve()`; gỡ chốt ⇒ rc 1 kèm traceback (đo 23:56:43Z). |
| (g) | Mục tiêu 4, B3 | HINT nói "dòng CUỐI đúng `N/N`". Đo `bang_chung_xanh` (`.claude/dev/ci_dang_ky_test.py` dòng 677–681 tại `1d7e642`, `re.search` đa dòng ở dòng 678; dòng 616–620 và 617 tại `c522c17`; thân hàm giống hệt, so AST nguồn; đo 23:58:24Z 15-10, đo lại 13:09:24Z 23-10-2026 với mẫu của khoá `ops/nhanh_don_duoc_test.py`): `1/1`, `x`, `26/27` ⇒ **True** (xanh giả: khớp dòng ĐẦU có dạng ấy); `26/27`, `27/27` ⇒ False; `a`, `27/27`, `b` ⇒ True. Nên dòng `N/N` phải là dòng DUY NHẤT có dạng số/số đứng một mình, không chỉ là dòng cuối. |
| (h) | Mục tiêu 1, chốt đường dẫn | Mới hoàn toàn: đọc đĩa biến `spec_path` (dữ liệu YAML) thành một lượt đọc hệ tệp, nên r3 thừa kế nguyên chốt của `_kiem_neo_prompt` dòng 973–996 (tuyệt đối, `..`, dấu chéo ngược, `relative_to` sau `resolve()`). Đo 23:56:43Z: gỡ chốt dạng ⇒ ba ca vẫn rc 13 nhưng sai thông điệp (đúng bài học chú thích dòng 977–979); gỡ `relative_to` ⇒ ca symlink ra ngoài kho rc 0. |
| (i) | A6 | Số tuyệt đối của hunk `@@ -190` (140/4/5 · 38/58/3, đo trên `6f121a3`) thay bằng số đo lại trên `c522c17`, rồi trên `1d7e642` (Số đo nền). |
| (j) | `kich_thuoc` | Hunk `@@ -16` dẫn 26 ca; r3 đòi 40 ca và có số đo bản thăm dò (+54) thay cho +52 của reviewer. |
| (k) | A2b | Hunk `@@ -105` nói kiểm dạng mọi trường nhưng không thêm ca; r3 thêm A2b (iii), và đo: đột biến "chỉ kiểm dạng trường quyết định" ⇒ ca ấy rc 0, ĐỎ (23:56:43Z). |

## Số đo nền (base `1d7e642`, đo lại 23-10-2026; giờ UTC, mốc không ghi ngày là 15-10-2026; đơn vị ghi rõ)

- Bản sao đo (23-10-2026, mọi bước dưới hợp đồng môi trường đo ngay dưới): clone `--no-checkout` của worktree đặc tả, `checkout --detach c3f6f5f`
  (= `1d7e642` cộng đúng ba tệp `ops/specs/no-p3-*`, `git diff --name-only 1d7e642 c3f6f5f`), `core.abbrev 7` (12:56:05Z–12:56:07Z 23-10-2026), và
  một clone thứ hai `checkout --detach 1d7e642`; bản bare đủ ref (`git clone --bare --reference` kho cục bộ từ `https://github.com/ducthangho/tra-luat`,
  12:57:47Z–12:57:52Z 23-10-2026, + `fetch '+refs/heads/*:refs/remotes/origin/*'`, 12:58:02Z 23-10-2026; so tập tên + OID với `ls-remote --heads`: thiếu 0, thừa 0,
  lệch 0, 556 nhánh; fetch lại lúc 13:02:47Z 23-10-2026 — 558 nhánh — và 13:20:16Z 23-10-2026 — 560 nhánh —, mỗi lần thiếu 0, thừa 0, lệch 0; lần fetch 13:01:54Z 23-10-2026 ra thiếu 1 vì một
  nhánh được tạo giữa `fetch` và `ls-remote`, bị loại và đo lại). Lượt soạn r4: một bản bare MỚI cùng cách dựng, 13:54:13Z–13:54:16Z
  23-10-2026, fetch `'+refs/heads/*:refs/heads/*' '+refs/heads/*:refs/remotes/origin/*'` trong một lệnh lúc 13:54:20Z và 14:03:55Z (562 rồi
  563 nhánh, mỗi lần thiếu 0, thừa 0, lệch 0; `depends_on` (2)). Lần soạn r3:
  clone kho cục bộ `checkout --detach c522c17` (23:31:11Z), bản bare 541 nhánh (23:31:42Z). Clone làm việc từ bản bare cho A6 ("ref cục bộ" = `git for-each-ref refs/heads refs/remotes` bỏ ref tên kết thúc `/HEAD`, đúng tập `_cac_ref_cuc_bo` — `ops/lease_publish.py` dòng 524–536 — mà `_quet_lease_toan_kho` đọc; số ấy đổi theo máy chủ và theo cách đọc, không chống đỡ tiêu chí nào — A6 đo TẬP — nên không ghi thành chữ số).
- Hợp đồng môi trường đo — quy tắc cho người chạy lại MỌI lệnh đo của spec, ở bất kỳ mục nào (kể cả bước dựng kho tạm, `git clone` và bước cần
  mạng; trừ các quan sát trạng thái GitHub có ngày giờ — Issue, PR, comment, hàng `packet_issue` và hàng `finding sau review` — bằng `gh api`, công cụ
  của phiên điều phối chứ không nằm trong năm liên kết — `gh` ra rc 127 khi `/usr/bin` và `/bin` không có nó, đo lượt 16 — và đo lại lúc cấp);
  KHÔNG phải lời khai về môi trường của lần đo nào, trừ những lần ghi rõ là đo dưới hợp đồng. Nền Linux (Windows chưa đo, mục Chưa đo
  được), một shell POSIX; lệnh mang đường dẫn tương đối của kho chạy với cwd là gốc bản sao đang đo. Tiền tố, dựng nguyên văn:
  `B="$(mktemp -d)"; for t in python3 git actionlint shellcheck ruff; do ln -s "$(command -v "$t")" "$B/$t"; done` rồi mỗi lệnh chạy dưới
  `env -i PATH="$B:/usr/bin:/bin" HOME="$(mktemp -d)" GITHUB_REPOSITORY=o/r <lệnh>`. `env -i` truyền ĐÚNG ba biến ấy: `PATH`; `HOME` là một
  thư mục rỗng vừa tạo cho MỖI lệnh (không có cấu hình git hay gói Python của người dùng; MỘT `HOME` dùng chung cho hai lệnh chỉ là độ lệch
  mà phép đo nêu tại chỗ, hàng (c) bảng thứ hai); `GITHUB_REPOSITORY=o/r` vì `kiem-github` đọc nó qua
  `_repo_github()` (`ops/lease_publish.py` dòng 856–860; A3b (ii)). `GITHUB_ACTOR` và mọi biến `GIT_*` không có mặt. Công cụ: năm liên kết
  trong `$B` (đo 17-10-2026 dưới chính tiền tố, đo lại 13:04:19Z 23-10-2026 ra cùng phiên bản: Python 3.11.15 nhập được PyYAML 6.0.1, git 2.43.0, actionlint 1.7.7, shellcheck 0.9.0,
  ruff 0.15.8) cộng `/usr/bin` và `/bin` cho `bash`, `sh` và các tiện ích dòng lệnh mà bộ đo nền gọi; trình thông dịch gọi bằng tên `python3`.
  Bước cần mạng (`git clone` hoặc `fetch` từ máy chủ, `ls-remote`, `ai-dang-giu`) dùng CÙNG tiền tố, chỉ thêm biến mạng và xác thực, ghi TÊN
  biến trong biên bản đo, không ghi giá trị. Đo lại 23-10-2026 (12:57:47Z–13:23:41Z, rồi lượt soạn r4 13:54:13Z–14:04:56Z) trên container phiên web, bước cần mạng chỉ thêm
  `HTTPS_PROXY`, như lần đo 17-10-2026 (14:00:09Z–14:03:06Z): `git clone --bare --reference` kho cục bộ, rồi trong bản bare ấy `fetch origin '+refs/heads/*:refs/remotes/origin/*'`
  (lần cuối kèm `'+refs/heads/*:refs/heads/*'` trong cùng lệnh, `depends_on` (2)) và
  `ls-remote --heads origin` đều rc 0; `ai-dang-giu --root <bản bare>` cho ba đường dẫn write set ra rc 0, 0, 11 ở cả hai ngày (11 là `NGƯỜI_GIỮ 1`; ai giữ
  thì đo lại lúc cấp, `depends_on` (2)). Bước cục bộ trong bản bare ấy, dưới hợp đồng không thêm gì: `git for-each-ref refs/remotes/origin`
  (bỏ `HEAD`) khác rỗng và so với kết quả `ls-remote` trên theo tập tên và OID ra thiếu 0, thừa 0, lệch 0; `git remote get-url origin` ra
  `https://github.com/ducthangho/tra-luat`.
  Phép đo nào lấy chính một yếu tố môi trường làm biến đo (ví dụ PATH của tiến trình con, cấu hình git toàn cục, giá trị `GITHUB_ACTOR`) nêu
  độ lệch ấy ngay tại chỗ bằng lệnh dựng nguyên văn, không bằng danh từ, và giữ mọi thứ khác theo hợp đồng. Ngoài hợp đồng này, kết quả KHÔNG được khẳng định; chạy ngoài hợp đồng là chạy
  sai, không phải phản chứng — trừ các quan sát trạng thái GitHub nêu ở câu đầu của bullet này, vốn nằm ngoài hợp đồng theo chính câu ấy, chạy bằng `gh api` và đo lại lúc cấp.
- Bảng mã thoát: `RC_OK 0`, `RC_THAM_SO 2`, `RC_TU_CAP 4`, `RC_NEO 6`, `RC_NOI_DUNG 8`, `RC_DA_DANG 9`, `RC_LOP 10`, `RC_DANG_GIU 11`,
  `RC_KHONG_XAC_DINH 12` (`ops/lease_publish.py` dòng 44–52, tệp không đổi từ `6f121a3` tới `1d7e642`). Mã `13` chưa dùng. Docstring `MÃ THOÁT`
  dòng 18–25 thiếu 11, 12 (dòng 26 là dòng đóng docstring); `--help` in 0 dòng chứa `MÃ THOÁT` (00:03:51Z 16-10; đo lại 13:20:07Z 23-10-2026: 0).
- Lease (kịch bản chỉ-đọc `m_cay.py` dựng lại 23-10-2026 — `m_baseline.py` của reviewer lượt 2 không có trong kho —, đọc blob bằng git, không
  checkout; `python3 -B m_cay.py 1d7e642`, 13:11:05Z–13:11:07Z 23-10-2026; cùng kịch bản trên `c522c17` (13:10:59Z 23-10-2026) tái lập ĐÚNG mọi số của
  lần soạn r3 — 152 · 99 (8) · 94/5 cùng năm tên · 60 · 6 khớp 6/6 · 54 khớp 0/54 · `spec_sha256` 57 và 5 — nên hai lần đo cùng định nghĩa):
  **171** tệp `ops/leases/*.yaml` (`c522c17`: 152; r2: 150). **118** có `spec_path` + băm (18 mang cả hai trường; `c522c17`: 99 và 8):
  **113** khớp blob tại `1d7e642`, **5** lệch — vẫn đúng năm lease r2 đã kể (`gate-tach-job-cat-chi-phi-exec-1`,
  `-1r2`, `-1r3` và `wp461-…-exec-1` mang `da_bi_thay_the`; `…-exec-1r4` không). **73** có `write_set` + `write_set_hash`: **6** khai
  scope `sorted NFC casefold exact …`, khớp công thức (a) 6/6; **67** không scope, khớp (a) **4/67** (`c522c17`: 54, khớp 0/54 — bốn lease mới
  tính đúng công thức (a) mà không khai scope, nên cổng vẫn không kiểm chúng, Mục tiêu 2). "Khớp blob" = sha256 của blob `<commit>:<spec_path>`
  bằng trường quyết định (Mục tiêu 1 (vii)).
- Trên toàn ref (bản bare, ảnh chụp ref lúc fetch 13:20:16Z 23-10-2026: 559 nhánh `refs/remotes/origin/*` bỏ nhánh của chính đặc tả
  `claude/spec-no-p3-r3`; kịch bản dựng lại `m_ref.py` — ba kịch bản `m_both.py`, `m_unexp.py`, `m_lease_shapes.py` của lượt soạn r3 không có
  trong kho —, 13:29:49Z–13:29:57Z 23-10-2026): **680** blob `ops/leases/*.yaml` khác nhau ở ĐẦU các nhánh ấy; **62** mang cả hai trường băm
  (60 bằng nhau; 2 khác nhau, vẫn là `wp709-exec-g1/g2-codex`, `spec_hash f569b613…` ≠ `spec_sha256_required f739b4aa…`); 4 blob chưa hết hạn
  lúc 13:29:51Z 23-10-2026 (theo `_phan_loai_lease`). Hình dạng, phân hoạch loại trừ theo thứ tự này, tổng 680: cả hai trường 62 · `spec_path` +
  `spec_hash` hex64 370 · `spec_path` + `spec_sha256_required` hex64 55 · `spec_hash` không `spec_path` 15 (`spec_sha256_required` không
  `spec_path`: 0) · `spec_path` không băm 56 ("băm" = `spec_hash` hoặc `spec_sha256_required`; `spec_sha256` không tính, xem Mục tiêu 1) ·
  `spec_path: null` 27 (0 blob trong đó có khoá `spec_hash`) · không `spec_path` không băm 95 (trong đó 3 blob mang `spec_hash: null` và KHÔNG có khoá `spec_path`:
  `tach-danh-tinh-github-exec-1r4-codex-20260828`, `-1r5-` và `-1r6-codex-20260828` trên nhánh `ops/cap-lease-tach-danh-tinh-20260827`; đo lượt 18, 23-10-2026,
  dựng lại phân hoạch từ chữ này trên bản bare đủ ref dựng lúc 15:07Z: sáu nhóm còn lại ra đúng số trên, nhóm "cả hai trường" 63 thay vì 62 vì blob lease `wp892-r2-g2-claude` thêm lúc 13:46:21Z)
  — **0** blob mang băm sai dạng. Lần soạn r3
  (540 nhánh bỏ `claude/spec-no-p3`, 23:33:44Z–23:33:51Z): 619 blob · cả hai 17 (15 bằng) · 7 chưa hết hạn · `spec_path` + `spec_hash` 354 ·
  không băm 56 · `spec_path` + `spec_sha256_required` 55 · `spec_path: null` 27 · `spec_hash` không `spec_path` 15 · `spec_hash: null` 3 · sai
  dạng 0; định nghĩa nhóm của ba kịch bản cũ không tra được, nên số từng nhóm của hai lần đo không bảo đảm cùng định nghĩa.
- **Nguồn đọc của `check`** (kịch bản `do_nguon.py`, kho tạm `git init` + cấu hình cục bộ, gọi `ops/lease_publish.py` của `c522c17` như
  tiến trình con, 23:34:49Z; lease có `prompt_path` + `prompt_sha256_required`): (1) lease + prompt CHƯA commit, khớp ⇒ rc 0; (2) đã commit,
  sửa prompt trên đĩa ⇒ rc 6 ("băm prompt LỆCH"); (3) `HEAD` hợp lệ, lease trên đĩa đổi `granted_by: claude` ⇒ rc 4; (4) `HEAD` mang prompt
  SAI, đĩa đúng ⇒ rc 0; (5) thư mục không có `.git`, có `--root` ⇒ rc 0; (6) PATH trỏ thư mục rỗng (không có git) ⇒ rc 0. Kết luận đo
  được: trong `check`, tệp lease (`_doc_yaml(a.tep)`, dòng 2294) và `prompt_path` (`_kiem_neo_prompt`, đọc byte dưới `_goc_kho(tep, goc)`,
  dòng 985–1001) đều đọc từ ĐĨA, không cần git. Đo lại 13:24:54Z–13:24:55Z 23-10-2026 bằng kịch bản dựng lại `do_nguon.sh` (`do_nguon.py`
  không có trong kho), gọi `ops/lease_publish.py` của `c3f6f5f` (byte-identical với `1d7e642` và `c522c17`) như tiến trình con, fixture là lease
  `wp892-r1-g1-claude` cùng spec của nó chép từ nhánh máy chủ (`prompt_path` = `spec_path`, có `prompt_sha256_required`; hạn `2026-10-24T13:01:00Z`, nên người đo lại từ mốc ấy đặt `lease_expires_at_utc` của bản chép ở `2099-01-01T00:00:00Z`, xem A0); riêng ca (6) lệch hợp
  đồng đúng một biến, dựng nguyên văn `E="$(mktemp -d)"; PATH="$E" <đường dẫn tuyệt đối của python3> -B <lease_publish.py> check <lease> --root .`:
  cùng sáu kết quả 0 · 6 · 4 · 0 · 0 · 0.
- Hai người tiêu thụ TỰ ĐỘNG của `check` đều chạy trên cây checkout SẠCH của commit được xét, nên với họ đĩa = commit: `ops-publish-lease.yml`
  (`actions/checkout@v4`, `fetch-depth: 0`, 0 dòng `sparse`; `check "$tep" --root .` dòng 216; bộ kiểm lấy từ worktree rời của nhánh mặc
  định, dòng 82–99) và `ops/ci_duong_nhanh.py::kiem_lease` (`check duong --root .` với `cwd=kho`, dòng 541; lease hết hạn đi
  `MA_KIEM_HET_HAN` dòng 121, tức `kiem(bo_qua_han=True)`). Người tiêu thụ THỦ CÔNG (`ops/README.md` dòng 37–38) chạy `check` TRƯỚC khi commit, trên cây CHƯA sạch (đĩa ≠ commit) — đó là lý do `kiem_bam` đọc ĐĨA (luật nguồn, Mục tiêu 1).
- `.gitattributes` dòng 8: `* text=auto eol=lf`. Đo 23:52:28Z trong kho tạm chép tệp ấy: spec CRLF trên đĩa, lease neo băm byte CRLF ⇒
  `check` trước commit rc 0; sau commit, blob là `73 70 65 63 20 41 0a` ⇒ clone sạch rc 13.
- Bộ đo nền trên bản sao `c3f6f5f` dựng dưới hợp đồng môi trường đo (`git clone --no-checkout` worktree đặc tả,
  `checkout --detach c3f6f5f`, `config core.abbrev 7`, cả ba rc 0), đo 23-10-2026, ba bộ chạy song song: `python3 -B ops/lease_publish_test.py` ⇒
  `lease_publish: 267/267 đạt; đã chạy=267, bỏ qua=0`, rc 0 (12:56:27Z–13:03:11Z 23-10-2026); `python3 -B .claude/dev/ci_dang_ky_test.py` (không `--chay`) ⇒
  `ĐĂNG KÝ: 24/24`, `TRẠNG THÁI: chan=24 cach_ly=0`, `PHẢN CHỨNG: 1064/1064 đỏ đúng`, `TỔNG: ĐẠT`, rc 0 (12:56:27Z–12:56:35Z 23-10-2026);
  `python3 -B ops/ci_duong_nhanh_test.py` ⇒ `CA: 104/104 dat · 0 do · 0 hong`, `DOT BIEN: 384/384 bi giet dung ly do`, `TONG: DAT`, rc 0
  (12:56:27Z–13:00:06Z 23-10-2026); cùng ba bộ trên bản sao `checkout --detach 1d7e642` ra đúng các số ấy (13:04:14Z–13:11:21Z 23-10-2026);
  `ruff check --isolated --select F ops/lease_publish.py` (ruff 0.15.8) ⇒ 2 F841 sẵn có ở dòng 198–199, rc 1 (13:04:18Z 23-10-2026).
  Trên `c522c17` (lượt soạn r3 15-10 23:31Z–23:38Z, đo lại 17-10-2026 13:59:19Z–14:05:48Z): 265/265 · 23/23, `chan=23`, 1025/1025 ·
  104/104, 383/383 · cùng 2 F841.
- A6 nền (kịch bản dựng lại `do_a6.py` — bản cũ cùng tên không có trong kho —, trong tiến trình, `kiem(bo_qua_han=True)` cho 171 lease trên
  clone làm việc từ bản bare, `checkout --detach 1d7e642`, ref cục bộ đếm bằng `git for-each-ref refs/heads refs/remotes` bỏ `/HEAD`,
  13:15:10Z–13:24:46Z 23-10-2026): `{rc 0: 157, rc 8: 9, rc 10: 5}`. Cùng kịch bản trên clone `checkout --detach c522c17` cùng tập ref
  (13:15:10Z–13:23:11Z 23-10-2026) tái lập đúng số lần soạn r3: `{rc 0: 143, rc 8: 4, rc 10: 5}` cho 152 lease (lần soạn r3 23:38:49Z–23:54:26Z).

## Mục tiêu

1. **[`ops/lease_publish.py`] Băm spec.** Hàm MỚI `kiem_bam(lease, tep, goc) -> list[str]` đặt NGOÀI thân `kiem()`; `lenh_check` gọi nó
   ngay sau dòng `lease, neo = kiem(...)` (dòng 2294), TRƯỚC mọi `print` của lệnh, nên rc 4/6/8/10 luôn thắng và rc 13 không bao giờ đi kèm
   dòng "ĐĂNG ĐƯỢC". `kiem-github` KHÔNG gọi nó (lease đã đăng vẫn ra rc 9). `kiem()` giữ BYTE-IDENTICAL thân và chữ ký trả 2 phần tử
   (`t191` duyệt AST thân `kiem()` nhưng chỉ coi `raise Chan` và lời gọi tên `_kiem_*`/`_doc_*` là chốt (`_la_chot`, `ops/lease_publish_test.py` dòng 9869–9875 tại `1d7e642`, 9541–9547 tại `c522c17`), nên KHÔNG thấy `kiem_bam`; `t01` dòng 706 tại `1d7e642` (705 tại `c522c17`) `checked, _ = mod.kiem(...)`; thân `_la_chot`, `_liet_ke_chot_kiem`, `_dem_chot_tho`, `_mien_mot_chot`, `t191_…` và `t01_executor_assurance_target_is_not_review_verdict` giống hệt giữa hai nền — so nguồn từng hàm qua AST, 23-10-2026; số đo của reviewer lượt 1–2 (tên `_kiem_bam_spec`): đúng chữ r1 ⇒
   263/265 trên nền 265 ca của `c522c17`, đỏ đúng hai ca ấy; chưa đo lại trên nền 267 ca). Người gọi `kiem()`: `check` (2294), `body` (2314), `kiem-github` (1280, 1282); không gồm
   `kiem-thu-hoi-github`. Mã của `lenh_body` và `kiem_github` không đổi.
   **Luật nguồn (đóng C1): spec đọc từ CÙNG NGUỒN với tệp lease trong từng lệnh.** `check` đọc lease từ ĐĨA (Số đo nền, ca 1–6), nên
   spec đọc từ ĐĨA: tệp `_goc_kho(tep, goc) / spec_path`, cùng gốc mà `_kiem_neo_prompt` dùng cho `prompt_path`, byte thô bằng
   `read_bytes()`, KHÔNG qua git, KHÔNG `read_text()`. Không lệnh nào của packet đọc lease từ REF rồi gọi `kiem_bam` (`kiem-github` đọc
   lease từ đĩa và không gọi; `ai-dang-giu`, `con-tro-treo`, `kiem-thu-hoi-github` đọc ref/tree nhưng không gọi `kiem()`), nên vế "đường
   đọc lease từ ref ⇒ spec từ blob cùng ref" là ràng buộc cho người gọi TƯƠNG LAI (Ngoài phạm vi), không có mã ở đây.
   Hệ quả đo được trên bản thăm dò (23:37:35Z–23:37:58Z): kho đã có `HEAD`, lease + spec MỚI chưa commit ⇒ bản đĩa rc 0, bản đúng chữ r2
   rc 13 (kho chưa commit nào: rc 12) — tức runbook `ops/README.md` dòng 37–38 (`check` trước khi commit) đúng NGUYÊN VĂN dưới thiết kế đĩa (từ r3, giữ ở r4). Chốt
   băm là ràng buộc toàn vẹn lease↔spec trong CÙNG một ảnh chụp, không phải lớp uỷ quyền: người đẩy được thì sửa được cả hai; uỷ quyền
   vẫn ở `granted_by` và `GITHUB_ACTOR` trong `kiem()`.
   Điều kiện kiểm: lease có `spec_path` (chuỗi khác rỗng) VÀ ít nhất một trường băm có mặt khác `null` trong `spec_hash`,
   `spec_sha256_required`. Thứ tự chốt, mỗi chốt ném `Chan(RC_SPEC_LECH, …)` với `RC_SPEC_LECH = 13` mới trừ chỗ ghi khác:
   (i) **DẠNG trước**: MỌI trường băm có mặt (khác `null`) phải là chuỗi 64 hex thường, kiểm cho CẢ HAI trường trước khi chọn trường
   quyết định (B7) — thông điệp nêu tên trường và "phải là 64 ký tự hex thường" như `_kiem_neo_prompt` dòng 969–971; `null` = vắng.
   Chốt (i) áp cho MỌI lease CHƯA bị thay thế (lease mang `da_bi_thay_the` đã trả ngay đầu hàm, Mục tiêu 5) có trường băm có mặt, kể cả khi thiếu `spec_path` (bản thăm dò làm vậy; 0/680 blob thật sai dạng lúc 13:29:49Z 23-10-2026 — 0/619 lúc soạn r3 —, kể cả 15
   blob `spec_hash` không `spec_path` — đều hex64 — nên không từ chối lease nào đã có).
   (ii) `spec_path` chứa NUL ⇒ 13, đứng TRƯỚC mọi thao tác hệ tệp (bảng thứ hai, hàng f).
   (iii) `spec_path` tuyệt đối, có thành phần `..`, hoặc chứa dấu chéo ngược ⇒ 13, thông điệp "phải là đường dẫn tương đối trong kho".
   (iv) Sau `resolve()`, tệp không nằm dưới gốc (kể cả symlink trỏ ra ngoài) ⇒ 13, thông điệp "trỏ ra ngoài kho".
   (v) Không phải tệp thường (vắng, thư mục) ⇒ 13, thông điệp nêu "không có tệp", đường dẫn đã tìm (chuỗi của `(<gốc kho> / spec_path).resolve()`) và
   "spec phải nằm trong cây cùng lease" (ba phần mà A2 (4) đo); KHÔNG nói "đã commit tại HEAD" (bảng thứ hai, hàng a).
   (vi) Có tệp mà `read_bytes()` ném `OSError` ⇒ `RC_KHONG_XAC_DINH` 12 (ba trạng thái: so được · không có tệp ⇒ 13 · không đọc được ⇒ 12).
   (vii) Trường quyết định: `spec_sha256_required` nếu có mặt, không thì `spec_hash`. Hai trường cùng có mặt thì CHỈ
   `spec_sha256_required` quyết định — khớp ⇒ qua bất kể GIÁ TRỊ `spec_hash`, lệch ⇒ 13 bất kể giá trị `spec_hash` (hình dạng wp709;
   PROTOCOL §3.2: `spec_hash` là băm của Packet Spec, không bắt buộc bằng băm byte của tệp). Lệch ⇒ 13, thông điệp nêu tên trường, giá trị
   khai, giá trị đo.
   Thiếu `spec_path` (hoặc không phải chuỗi, rỗng, `null`) hoặc không có `spec_hash` lẫn `spec_sha256_required` ⇒ **không kiểm, không đỏ** (lease cũ, kể cả 15/680
   blob mang `spec_hash` mà không `spec_path`, 13:29:49Z 23-10-2026; 15/619 lúc soạn r3); dòng kết quả của `check` nói "spec: không khai — không kiểm" (nghĩa là không khai `spec_hash` lẫn `spec_sha256_required`; tên thứ ba `spec_sha256` KHÔNG được đọc — đo tại `1d7e642` (13:11:05Z 23-10-2026): 61/171 lease mang nó, 5/171 mang nó mà thiếu cả hai tên kia — vẫn năm lease họ `plat-m4-*`, băm khớp tệp, đều đã hết hạn, muộn nhất 2026-08-22T07:10:00Z; tại `c522c17`: 57/152 và 5/152).
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
   kiểm" (67 lease không scope ở `1d7e642`, Số đo nền; 54 ở `c522c17`).
3. **[`ops/lease_publish.py`] Dòng xác nhận là bằng chứng.** Khi kiểm đạt, `kiem_bam` TRẢ dòng bằng chứng mang 12 ký tự đầu băm ĐO cho spec
   và cho write set, `lenh_check` in chúng; KHÔNG `print` trong `kiem()` (stdout của `body` là thân comment). Thêm hàng `13` vào bảng
   `MÃ THOÁT` ở docstring đầu tệp (dòng 18–25 tại `c522c17` và `1d7e642`, tệp không đổi); `--help` không in bảng ấy (`argparse` lấy DÒNG ĐẦU của `__doc__`, dòng 2413). Chỉ thêm
   hàng 13; bảng thiếu 11, 12 là nợ sẵn có, KHÔNG thuộc packet.
4. **[`ops/lease_publish_spec_hash_test.py`] Phản chứng.** Bộ test MỚI, tự đứng (không import `ops/lease_publish_test.py`, tệp ấy ngoài
   write set; lúc soạn r3 nó thuộc write set #748, nay #748 đã merge và `ai-dang-giu` cho nó `NGƯỜI_GIỮ 0` lúc 13:21:52Z và 14:04:15Z 23-10-2026), DẠNG BẢNG (hàng `kich_thuoc`). Dựng kho tạm bằng `git init` trong thư mục tạm, gọi `lease_publish.py check` như tiến
   trình con, đọc rc + stdout + stderr. HERMETIC, bốn lớp: (a) xoá `GITHUB_ACTOR` và mọi `GIT_*` khỏi env con (số reviewer lượt 2:
   không xoá ⇒ 27/27 · 0/27 · 27/27 khi biến không đặt, `notebyme88`, `ducthangho`); (b) mọi lệnh `git` của bộ test chạy với
   `GIT_CONFIG_NOSYSTEM=1` và `GIT_CONFIG_GLOBAL` trỏ một tệp rỗng trong thư mục tạm; (c) mỗi kho tạm đặt cấu hình cục bộ
   `core.autocrlf=false`, `user.name`, `user.email`, `commit.gpgsign=false`; (d) mọi `git clone` kèm `-c core.autocrlf=false` (bảng thứ
   hai, hàng c: thiếu CẢ (b) LẪN nó thì `HOME` có `core.autocrlf=true` làm A3c ĐỎ GIẢ; có (b) thì nó là lớp thứ hai). Ca `kiem-github` dùng `gh` giả ghi ra thư mục tạm trên PATH và đặt `GITHUB_REPOSITORY=o/r` trong env con (cùng giá trị với hợp đồng môi trường đo ở Số đo nền; `_repo_github()` đọc biến ấy).
   Ca phụ thuộc nền (`gh` giả bằng shebang, symlink, PATH rỗng) hoặc chạy được trên Windows, hoặc tự BỎ QUA CÓ TÊN kèm lý do khi
   `os.name == "nt"` — không im lặng xanh. Ca A4b (9) (đọc ném `OSError` ⇒ 12) chạy TRONG tiến trình: nạp `ops/lease_publish.py` của cây đang thử bằng
   `importlib`, chèn `PermissionError` vào lượt đọc byte của đúng tệp spec, gọi `kiem_bam`, đòi `Chan` mã 12, rồi trả lại hàm gốc.
   Chạy được bằng `python3 -B ops/lease_publish_spec_hash_test.py`, trả 0 khi đạt, và in đúng MỘT dòng đứng một mình có dạng
   `số/số` — dòng tổng `N/N`, N ≥ 1, hai số bằng nhau — là dòng cuối; không dòng nào khác (kể cả dòng từng nhóm) được có dạng ấy, vì
   `bang_chung_xanh` của sổ lấy dòng ĐẦU khớp (bảng thứ hai, hàng g).
5. **[`ops/lease_publish.py`] Miễn bia mộ.** Lease mang `da_bi_thay_the` (chuỗi khác rỗng) ⇒ `kiem_bam` trả NGAY ĐẦU hàm — trước chốt dạng (i), đường dẫn (ii)–(vi) và kiểm write set —, KHÔNG so băm, và trả
   "spec/write_set: lease đã bị thay thế — bia mộ — không kiểm băm" (A5b của r4 đo TRỌN chuỗi này, L6 (b); r3 chỉ đo chuỗi con
   `bia mộ — không kiểm băm`, mà bản có ngoặc "(bia mộ) — không kiểm băm" của r2 KHÔNG chứa — số reviewer lượt 2: 26/27 với chuỗi có ngoặc). Lý do (đo lại trên
   `c522c17` rồi trên `1d7e642`, A6): chuỗi revision dùng LẠI `spec_path` với băm mới và ghi bia mộ cho lease tiền nhiệm KHI CÒN HẠN — 4/5 lease lệch là
   tiền nhiệm như vậy; `ops/ci_duong_nhanh.py::kiem_lease` đưa MỌI lease CÒN HẠN bị chạm trong PR qua `check` (dòng 541), nên một PR sửa
   spec tại chỗ và ghi bia mộ vào tiền nhiệm còn hạn (hình dạng commit `6635379`) sẽ đỏ `gate-ops` nếu không miễn. Lease HẾT HẠN đi
   `kiem(bo_qua_han=True)` (dòng 539) nên không chạm `kiem_bam`; `ops-publish-lease.yml` bỏ qua rc 9 trước `check` (dòng 204–207).
6. **[`.claude/dev/ci_dang_ky_test.py`] Đăng ký bộ test mới.** Thêm ĐÚNG MỘT dòng vào dict `MOI` (dòng 38–55 ở `1d7e642`, 10 khoá; dòng 37–53 và 9 khoá ở `c522c17`): khoá
   `"ops/lease_publish_spec_hash_test.py"`, giá trị CHÉP NGUYÊN chuỗi mẫu của dòng `"ops/nhanh_don_duoc_test.py"` (dòng 53 ở `1d7e642`, 52 ở `c522c17`; mẫu khớp một
   dòng đứng một mình gồm hai nhóm số cách nhau dấu gạch chéo). Không sửa dòng nào khác. Lý do: `kiem()` của sổ (dòng 640 ở `1d7e642`, 579 ở `c522c17`) đòi mọi
   `ops/*_test.py` mức đỉnh (`tim()`, dòng 104 ở `1d7e642`, 83 ở `c522c17`) nằm trong `DANG_KY` (dòng 82, trước là 80); sổ CHẠY các bộ `MOI` trong job `gate-registry`
   (`chay_moi` dòng 1055, trước là 967; `ci.yml` job mở ở dòng 937, `--chay` ở dòng 1008 — trước là 827 và 895), nên đây cũng là cách nối CI — không sửa `ci.yml`.
   `tim()` tại `1d7e642` thêm một luật so với `c522c17`: tệp bị Git bỏ qua mà chưa tracked không được đếm (`_git_bo_qua`); tệp test mới
   không bị bỏ qua (`git check-ignore` rc 1, 13:25:13Z 23-10-2026) nên vẫn bị đếm — đo được ở A7. Nếu #763 land trước, dòng của
   #751 đặt cạnh hai dòng của #763; vẫn đúng một dòng thêm.

## Nghiệm thu

Ký hiệu "đo" = đo trên bản thăm dò của lượt soạn r3 (không giao, dựng từ chữ Mục tiêu 1–3, 5) bằng `do_dot_bien.py` (23:56:43Z–23:57:08Z:
bản thăm dò 15/15 ca đạt; 10 đột biến, mỗi cái chạy trên bản sao riêng trong thư mục tạm) hoặc `do_a3.py` (23:37:35Z–23:37:39Z). Số khác
ghi rõ là của reviewer. Executor phải tự đo lại trên bản dựng của mình. Các số "đo" của A1–A5b chạy trên kho tạm với `ops/lease_publish.py`
của `c522c17`, byte-identical tại `1d7e642`, nên không phụ thuộc lần dời nền; số của A0, A6, A7 đo lại trên `1d7e642` ngày 23-10-2026 (mục `Đo lại nền sau #748 merge`).

**Luật khớp chuỗi — L6 của `.claude/skills/soan-spec/SKILL.md` — cho mọi tiêu chí dưới đây nói "chứa", "thông điệp", "câu" hay đếm chuỗi.**
(b) Khớp trên văn bản đã chuẩn hoá NFC và đã gộp mọi dãy khoảng trắng (kể cả xuống dòng) thành một dấu cách trong TỪNG đoạn — đoạn là
khối dòng liền nhau không có dòng trống — của đúng luồng nêu tại tiêu chí; thông điệp `Chan` đi stderr dạng `CHAN [<mã>]: …`
(`ops/lease_publish.py` dòng 2451), dòng xác nhận và dòng bằng chứng đi stdout. Cụm phải khớp là TOÀN BỘ chuỗi mà Mục tiêu đặt trong ngoặc
kép, không phải tiền tố hay một mẩu của nó; vế âm "KHÔNG chứa" xét cả stdout lẫn stderr. (a) Mỗi tiêu chí có vế dương trên đầu ra MỚI;
vế âm trên đầu ra CŨ là lần chạy thử cùng ca trên nền (`ops/lease_publish.py` của `1d7e642`) phải ra ĐỎ, cộng vế âm riêng tại tiêu chí khi
chữ cũ có thể sống sót (A2 (4), A5b, A6b). Đo dưới hợp đồng môi trường đo, fixture là lease `wp892-r2-g2-claude` bỏ các trường băm
spec/prompt/write set, `spec_ref`, thay thế và bia mộ rồi thêm đúng trường của ca: `do_l6.py` 14:00:14Z–14:00:15Z 23-10-2026 — A1, A2 (4),
A5 (1), A5b (cả hai ca) ĐỎ trên nền; cùng các ca trên bản thăm dò A6 dựng lại (blob `4bdf59d42a0272101baba5585b1cd874823fdd24`: bản diff
7 hunk của lần đo lại áp bằng `git apply --unidiff-zero` lên `ops/lease_publish.py` nền) đều XANH, 14:00:27Z–14:00:28Z; `do_l6b.py`
14:03:49Z–14:03:50Z — A4 ca đầu: nền ĐỎ, bản thăm dò XANH. (c) Không tiêu chí nào cộng gộp số khớp qua nhiều tệp hay nhiều ca: mỗi phép
khớp chạy trên một luồng của một ca; phép đếm duy nhất là dòng `số/số` ở A7, trên một luồng. (d) Chuỗi đích hoặc do Mục tiêu đặt nguyên văn
(kể cả "phải là 64 ký tự hex thường") hoặc là băm, đường dẫn do máy sinh, nên không có dạng chữ thay chữ số để bắt; dòng `số/số` đếm bằng chính
mẫu của sổ (A7). (e) Lời khai "không cổng nào" của đặc tả này: hàng `review_class`.

- **A0 (nền, L5):** trước khi cấp lease, đo `depends_on` (3) trên `master` lúc cấp; chưa kích hoạt thì chạy lại, trên nền `1d7e642` (r4 không đuổi theo
  `master`, quyết định chủ kho 23-10-2026 mục 2; #748 đã merge) và dưới hợp đồng môi trường đo (Số đo nền), các phép của Số đo nền mà kết quả CHỈ phụ thuộc
  cây `1d7e642`: ba bộ đo nền và `ruff`, bảng mã thoát, các số đếm theo cây (lease, `spec_sha256`, dòng dài nhất, `--help`), nguồn đọc của `check` (sáu ca của Số đo nền, fixture đặt `lease_expires_at_utc` ở `2099-01-01T00:00:00Z`: lease `wp892-r1-g1-claude` hết hạn `2026-10-24T13:01:00Z`
  và `kiem()` kiểm hạn SAU neo prompt (`ops/lease_publish.py` dòng 1104–1110), nên từ mốc ấy — trước mốc `2026-10-24T13:46:00Z` mà `depends_on` (2) chờ — bản chép nguyên cho
  `8 · 6 · 4 · 8 · 8 · 8` thay vì `0 · 6 · 4 · 0 · 0 · 0`; đo lượt 19, 23-10-2026, cửa sổ 16:52Z–17:09Z, đồng hồ giả bằng cách thay tên `datetime` trong module `ops/lease_publish.py` của `1d7e642`:
  fixture nguyên bản ở `2026-10-24T13:00:59Z` cho `0 · 6 · 4 · 0 · 0 · 0`, ở `2026-10-24T13:01:00Z` và ở `2026-10-24T13:46:01Z` cho `8 · 6 · 4 · 8 · 8 · 8`, đặt hạn
  `2099-01-01T00:00:00Z` ở `2026-10-24T13:46:01Z` cho `0 · 6 · 4 · 0 · 0 · 0`), số dòng
  và thân hàm dẫn trích; đã kích hoạt thì revision mới. ĐỎ khi: một số thuộc loại ấy khác số ghi ở đây mà chưa có revision mới ghi số đo mới — khi đó KHÔNG cấp.
  Các số ẢNH CHỤP THEO GIỜ KHÔNG thuộc A0, vì chúng trôi dù nền đóng băng: số nhánh máy chủ, tổng blob lease toàn ref cùng phân hoạch của nó, số blob chưa hết
  hạn, người giữ lease (chỉ `depends_on` (2) đo lại lúc cấp), số tuyệt đối của A6 ("tiêu chí là TẬP, không phải số") và phép so kho cục bộ với máy chủ. Đo lượt 18
  (23-10-2026, bản bare đủ ref dựng lúc 15:07Z, khoảng 100 phút sau lần đo 13:20Z–13:29Z): blob lease toàn ref 681 thay vì 680 (cả hai trường 63 thay vì 62, bằng nhau 61
  thay vì 60, do blob `wp892-r2-g2-claude` thêm lúc 13:46:21Z); blob chưa hết hạn, đếm tại 13:29:51Z trên tập blob ấy, ra 5 thay vì 4 (cùng blob thêm), ra 4 từ
  2026-10-23T15:49:00Z và chỉ ra 1 tại 2026-10-24T13:46:01Z — ngay sau khi lease `wp892-r2-g2-claude`, người giữ mà `depends_on` (2) chờ, hết hạn — vì 4 lease hết hạn trước mốc ấy (`wp878-r1-g1-claude`
  2026-10-23T15:49:00Z, `wp748-r24-g24-claude-remote-20261023` 2026-10-24T01:10:11Z, `wp892-r1-g1-claude` 2026-10-24T13:01:00Z, `wp892-r2-g2-claude` 2026-10-24T13:46:00Z); đọc A0 là "mọi số" thì nó ĐỎ chắc chắn lúc cấp.
- **A1 (khớp ⇒ qua):** lease có spec khớp và KHÔNG mang `prompt_path` ⇒ rc 0, stdout chứa 12 ký tự đầu băm đo VÀ "ĐĂNG ĐƯỢC". Vì sao
  bỏ `prompt_path` (L6 (a)): lease thật thường đặt `prompt_path` = `spec_path` (như `wp892-r2-g2-claude`), và khi ấy `check` của NỀN đã in
  "prompt … khớp băm" kèm đúng 12 ký tự ấy — đo 14:00:14Z 23-10-2026: cùng ca trên nền, có `prompt_path` = `spec_path` ⇒ vế dương XANH
  sẵn; không `prompt_path` ⇒ ĐỎ (stdout chỉ còn dòng "ĐĂNG ĐƯỢC" mang 12 ký tự đầu của `reviewed_sha_required`). ĐỎ khi: gỡ dòng in bằng chứng ⇒ ca
  ĐỎ (số reviewer lượt 2); tính gốc theo thư mục chứa lease thay vì `_goc_kho` ⇒ ca rc 13, ĐỎ (đo; đột biến ấy làm đỏ 6/15 ca).
- **A2 (lệch ⇒ 13):** năm ca, mỗi ca dùng lease CHỈ mang đúng trường được sửa (lease mang cả hai trường mà chỉ `spec_hash` lệch là A2b
  (i), rc 0): (1) sửa 1 ký tự `spec_hash` ⇒ 13; (2) sửa 1 ký tự `spec_sha256_required` ⇒ 13, stderr chứa tên trường, giá trị khai và giá
  trị đo; (3) thêm 1 byte vào spec SAU khi tính băm ⇒ 13 và stdout KHÔNG chứa "ĐĂNG ĐƯỢC"; (4) `spec_path` trỏ tệp vắng ⇒ 13; stderr chứa
  ĐỦ ba phần của Mục tiêu 1 (v) — `không có tệp`, đường dẫn đã tìm (chuỗi của `(<gốc kho tạm> / spec_path).resolve()`) và
  `spec phải nằm trong cây cùng lease` —, stdout lẫn stderr KHÔNG chứa `đã commit tại HEAD` (vế âm: chữ của r2, bảng thứ hai hàng a), stdout
  không chứa "ĐĂNG ĐƯỢC"; (5) hai trường CÙNG sai và khác nhau ⇒ 13. ĐỎ khi: gỡ phép so ⇒ ít nhất bốn ca rc 0 (số reviewer lượt 2: 8 ca
  của bộ 27); thông điệp lệch chỉ ghi "băm lệch" ⇒ ca (2) ĐỎ; gọi `kiem_bam` SAU dòng in "ĐĂNG ĐƯỢC" ⇒ ca (3) ĐỎ (đo: rc vẫn 13, đỏ vì
  chuỗi, 2/15 ca); "vắng ⇒ không kiểm" ⇒ ca (4) rc 0, ĐỎ (đo trên cùng nhánh mã ở A3c và A4b (8)); bỏ cụm `spec phải nằm trong cây cùng
  lease`, bỏ đường dẫn đã tìm, hoặc đổi thông điệp sang `đã commit tại HEAD` ⇒ ca (4) ĐỎ — đo 14:03:49Z–14:03:50Z 23-10-2026 (`do_l6b.py`)
  trên ba bản sao của bản thăm dò A6 dựng lại, mỗi bản một đột biến: cả ba ĐỎ theo chữ r4, cả ba XANH theo chữ r3 (chỉ đòi "không có tệp").
- **A2b (hai trường, hình dạng wp709):** (i) `spec_hash` KHÁC nhưng `spec_sha256_required` = băm tệp ⇒ rc 0; (ii) `spec_sha256_required`
  SAI nhưng `spec_hash` = băm tệp ⇒ rc 13; (iii) `spec_hash` 63 ký tự cạnh `spec_sha256_required` đúng ⇒ rc 13, stderr chứa `spec_hash` và
  `phải là 64 ký tự hex thường` (cụm của Mục tiêu 1 (i)). ĐỎ khi: so cả hai trường ⇒ (i) ĐỎ; "khớp một trong hai là đủ" ⇒ (ii) ĐỎ (số reviewer lượt 1–2: chỉ ca ấy giết được đột biến
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
  `git clone -c core.autocrlf=false` sạch và chạy `check` trong clone ⇒ rc 13, thông điệp đủ ba phần và vế âm như A2 (4) (đường dẫn đã
  tìm là của clone), không "ĐĂNG ĐƯỢC"; add spec,
  commit, clone sạch lại ⇒ rc 0. Đo: 13 rồi 0 (23:37:35Z); cùng trình tự với `prompt_path` trên cổng HIỆN HÀNH ⇒ rc 6 ở clone sạch — lỗ
  "`git add ops/leases` bỏ sót tệp được neo" là sẵn có và fail-close. ĐỎ khi: "vắng ⇒ không kiểm" ⇒ ca đầu rc 0, ĐỎ (đo); đọc `HEAD` ⇒
  không đổi ca này (13 · 0) — nó đo đường đăng, không đo nguồn; nguồn do A3 khoá.
- **A4 (write set):** scope `sorted NFC casefold exact …` + băm đúng ⇒ rc 0 và stdout chứa 12 ký tự đầu băm write set đo; sai 1 ký tự ⇒ rc
  13; đổi thứ tự `write_set` (băm giữ) ⇒ rc 0; một đường dẫn viết hoa khác ⇒ rc 0; dạng NFD của cùng tên ⇒ rc 0; `write_set` có một phần
  tử số nguyên (kèm scope + băm hợp lệ dạng) ⇒ rc 13, không traceback. ĐỎ khi: bỏ `casefold` ⇒ ca viết hoa ĐỎ; bỏ `normalize` ⇒ ca NFD ĐỎ;
  bỏ `sorted` ⇒ ca đổi thứ tự ĐỎ — mỗi đột biến làm đỏ ÍT NHẤT ca đích (số reviewer: 1 · 1 · 2 ở lượt 1, 4 · 1 · 4 ở lượt 2, phụ thuộc
  fixture); gỡ dòng bằng chứng write set ⇒ ca đầu ĐỎ; gỡ chốt kiểu phần tử ⇒ rc 1 kèm `TypeError`, ĐỎ (số reviewer lượt 2).
- **A4b (ca biên, nguồn đĩa):** (1) spec 6 byte `61 0d 0a 62 0d 0a` trên đĩa + băm byte thô `58055bdc…` ⇒ rc 0; (2) `spec_hash` 63 ký tự
  (lease một trường) ⇒ 13, stderr chứa `spec_hash` và `phải là 64 ký tự hex thường`; (3) `spec_path` chứa NUL ⇒ 13, không traceback;
  (4) `../ngoai.md`, (5) `spec_path` có dấu chéo ngược thay cho gạch chéo, (6) đường dẫn tuyệt đối ⇒ mỗi ca 13, stderr chứa
  `phải là đường dẫn tương đối trong kho` (cụm của Mục tiêu 1 (iii), không chỉ "tương đối");
  (7) symlink trong kho trỏ ra ngoài ⇒ 13, stderr chứa `trỏ ra ngoài kho` (bỏ qua có tên trên `nt`); (8) `spec_path` là thư mục ⇒ 13,
  thông điệp đủ ba phần và vế âm như A2 (4);
  (9) đọc ném `PermissionError` (trong tiến trình) ⇒ `Chan` mã 12. ĐỎ khi (đo, mỗi đột biến chạy trên bản sao riêng): đọc văn bản ⇒ (1)
  rc 13; gỡ HẲN chốt dạng hex ⇒ (2) vẫn rc 13 nhưng sai thông điệp (số reviewer lượt 2 — vì thế ca neo THÔNG ĐIỆP); bỏ chốt NUL ⇒ (3) rc 1;
  gỡ chốt dạng đường dẫn ⇒ (4)(5)(6) vẫn rc 13 nhưng sai thông điệp; gỡ `relative_to` ⇒ (7) rc 0; "vắng ⇒ không kiểm" ⇒ (8) rc 0; gộp 12
  vào 13 ⇒ (9) mã 13.
- **A5 (lease cũ không đỏ):** (1) không `spec_path` ⇒ rc 0, stdout chứa `spec: không khai — không kiểm`; (2) `write_set_hash` không
  scope ⇒ rc 0, stdout chứa `write_set_hash: scope không nhận ra — không kiểm`; (3) có `spec_path` mà không có `spec_hash` lẫn `spec_sha256_required` (56/680 blob thật lúc 13:29:49Z 23-10-2026, 56/619 lúc soạn r3; lease chỉ mang `spec_sha256` — 5 lease ở `1d7e642` cũng như ở `c522c17` — cũng rơi vào dạng này vì cổng không đọc `spec_sha256`) ⇒ rc 0, stdout chứa `spec: không khai — không kiểm`; (4) `spec_hash: null`
  cạnh `spec_sha256_required` đúng ⇒ rc 0. ĐỎ khi: coi thiếu trường là lỗi ⇒ (1)(2) ĐỎ; "có `spec_path` mà không băm ⇒ 13" ⇒ (3) ĐỎ;
  "`null` là băm sai dạng" ⇒ (4) ĐỎ (hai đột biến sau sống sót bộ A của r2, số reviewer lượt 2).
- **A5b (bia mộ):** lease CÒN HẠN mang `da_bi_thay_the`, spec sửa tại chỗ sau khi cấp ⇒ `check` rc 0, stdout chứa TRỌN chuỗi của Mục
  tiêu 5 `spec/write_set: lease đã bị thay thế — bia mộ — không kiểm băm`, và vẫn rc 0 sau khi XOÁ tệp spec (cùng ca, không đổi số ca); cùng
  hình dạng KHÔNG mang `da_bi_thay_the` ⇒ 13, và stdout lẫn stderr KHÔNG chứa `bia mộ`. Vế âm ở ca rc 13 chỉ bắt chữ `bia mộ` do `kiem_bam` tự `print` hoặc nhét vào thông điệp 13;
  một `kiem_bam` theo Mục tiêu 3 (TRẢ dòng, `lenh_check` mới in) mà nối dòng miễn vào kết quả của mọi lease qua được `check` thì KHÔNG bị bắt, vì ca rc 13 ném trước mọi `print` (đo lượt 18,
  23-10-2026, bản thăm dò dựng độc lập: đột biến ấy sống 40/40, còn hai đột biến tự `print` bị đúng ca ấy giết). Vế âm cho hình dạng TRẢ dòng phải đặt ở ca ĐẠT: ở A1 (lease KHÔNG mang
  `da_bi_thay_the`, rc 0) stdout lẫn stderr KHÔNG chứa `bia mộ` (không đổi số ca; các đột biến ấy làm A1 ĐỎ, bản đúng XANH). Chạy thử
  14:00:14Z 23-10-2026: cả hai ca ĐỎ trên nền (rc 0, không có chuỗi), XANH trên bản thăm dò dựng lại. ĐỎ khi: bỏ miễn ⇒ ca đầu rc 13
  (đo, 1/15 ca); in chuỗi có ngoặc của r2 hoặc chỉ in phần đuôi ⇒ ca đầu ĐỎ theo chữ (không khớp trọn chuỗi; chưa chạy đột biến này); đặt miễn SAU chốt tệp ⇒ ca đầu rc 13 sau khi xoá spec (đo lượt 3, 16-10-2026, cửa sổ 02:12Z–02:55Z): bản thăm dò 40 ca thiếu bước xoá vẫn 40/40.
- **A6 (không hồi quy):** (i) trên một `git clone` (KHÔNG `git archive`) ở nền lúc cấp, trong tiến trình: `kiem(bo_qua_han=True)` rồi
  `kiem_bam(...)` cho mọi lease; TẬP lease đổi rc so với nền phải đúng tập đã khai. Đo trên `1d7e642`, clone làm việc của Số đo nền (ref cục bộ đếm bằng `git for-each-ref refs/heads refs/remotes` bỏ `/HEAD`; 13:15:10Z–13:24:46Z 23-10-2026;
  ứng viên = nền rồi `kiem_bam` THĂM DÒ dựng từ chữ Mục tiêu 1, 2, 5 trong kịch bản đo, không sửa `ops/lease_publish.py`):
  nền `{0: 157, 8: 9, 10: 5}`, ứng viên `{0: 156, 8: 9, 10: 5, 13: 1}`, tập đổi = {`gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906`
  0 → 13} (cuối chuỗi, spec sửa sau khi cấp) — CÙNG TẬP với lần đo trên `c522c17`; 46 lease được miễn bia mộ, 66 kiểm spec và khớp, 4 kiểm write set và khớp
  (`c522c17`, lần soạn r3 23:38:49Z–23:54:26Z và cùng kịch bản 13:15:10Z–13:23:11Z 23-10-2026: nền `{0: 143, 8: 4, 10: 5}`, ứng viên `{0: 142, 8: 4, 10: 5, 13: 1}`, 38 · 60 · 4). Số tuyệt đối
  phụ thuộc tập ref cục bộ (`_quet_lease_toan_kho` dòng 694–754 đọc lease cũ của `thay_the_cho` trên MỌI ref cục bộ); tiêu chí là TẬP,
  không phải số. (ii) `ops/lease_publish_test.py` trên ứng viên: số ca đạt bằng nền, delta 0 (nền 267/267 tại `1d7e642`; bản thăm dò đo 23-10-2026 — `kiem_bam`
  nối vào `lenh_check` trên bản sao `c3f6f5f` — 267/267, 13:17:17Z–13:26:53Z 23-10-2026; tại `c522c17`: nền 265/265, bản thăm dò 265/265, 23:36:50Z–23:43:02Z). ĐỎ khi: một ca của `lease_publish_test.py` từ đạt sang trượt, hoặc tập lease đổi rc khác tập đã khai; đột biến bỏ
  miễn bia mộ ⇒ 5 lease đổi `0 → 13` thay vì 1 (đo trên cả hai nền: đúng bốn tiền nhiệm cộng `…-exec-1r4`).
- **A6b (`kiem()` bất biến, chú thích đúng):** `git diff -U0 <nền> -- ops/lease_publish.py` (`<nền>` có trong clone và lệnh thoát rc 0 rồi mới đọc kết quả: clone nông không có `<nền>` cho rc 128, stdout rỗng — đo 17-10-2026, git 2.43.0) không có hunk nào trong thân `kiem()` (dòng
  1009–1114) và `kiem()` vẫn trả 2 phần tử (bản thăm dò lượt soạn r3: 5 hunk, chưa gồm sửa chú thích `lenh_body` và docstring dòng 15–16; đủ cả hai là 7 hunk, đo lượt 4 — không hunk nào trong khoảng ấy; bản thăm dò đo 23-10-2026 trên `c3f6f5f`, `git diff -U0 1d7e642` rc 0: 7 hunk, không hunk nào trong khoảng ấy, câu cũ 0 dòng, 13:33:40Z 23-10-2026; `ops/lease_publish.py` không đổi giữa hai nền nên khoảng 1009–1114 giữ nguyên); trong ứng viên, chú thích trong
  `lenh_body` không còn câu "Đi qua ĐÚNG bộ kiểm THUẦN của `check`" mà nói `body` KHÔNG chạy `kiem_bam`. Đo theo L6, không bằng `grep -c`
  theo dòng: "khối chú thích" = dãy dòng liền nhau của `ops/lease_publish.py` mà phần sau thụt đầu dòng bắt đầu bằng `#`, bỏ `#` đầu mỗi
  dòng rồi nối và gộp khoảng trắng; (vế âm) không khối nào của cả tệp chứa câu cũ; (vế dương) các khối nằm giữa dòng `def lenh_body` và
  dòng cuối của hàm (theo `ast`) chứa `kiem_bam` NGUYÊN TỪ ít nhất một lần. Đo 14:00:14Z 23-10-2026 (`do_l6.py`): nền — câu cũ 1 khối,
  `kiem_bam` 0 ⇒ ĐỎ; bản thăm dò dựng lại — 0, 1 ⇒ XANH; đột biến xoá dòng chú thích ấy của bản thăm dò — 0, 0 ⇒ ĐỎ, trong khi `grep -c`
  câu cũ của r3 cho 0 ⇒ XANH GIẢ; đột biến ngắt câu cũ trên nền sang hai dòng chú thích — `grep -c` theo dòng 0 (XANH GIẢ), theo khối 1
  ⇒ ĐỎ. Vế dương chỉ đo sự có mặt của tên; nghĩa phủ định ("KHÔNG chạy") vẫn là kiểm bằng đọc mã. ĐỎ khi: `git diff -U0` thoát rc ≠ 0
  hoặc có hunk nằm trong 1009–1114, hoặc `ast.dump` của `FunctionDef` `kiem` (gồm `decorator_list`) ở ứng viên khác ở nền — hunk chèn ngay trên `def kiem` (một dòng
  `@…`) là `@@ -1008,0 +1009 @@`, cũ 1008 nằm ngoài 1009–1114 nên vế hunk không bắt (đo lượt 18, 23-10-2026: bản thăm dò gắn decorator lên `kiem` qua 40/40 ca A1–A5b
  lẫn vế hunk), còn hunk chèn liền sau `return` không cách dòng trống là `@@ -1114,0 +1115,4 @@` nằm NGOÀI (cách đọc "hunk nằm trong 1009–1114": hunk `-s,n` có n ≥ 1 là TRONG khi đoạn cũ `s … s+n-1` giao 1009–1114; hunk chỉ chèn `-s,0`
  (chèn SAU dòng cũ s) là TRONG khi 1009 ≤ s ≤ 1113, nên `-1008,0` và `-1114,0` là NGOÀI còn `-1009,0` và `-1113,0` là TRONG (đo lượt 19, 23-10-2026, cửa sổ 17:05Z–17:19Z, `git diff --no-index -U0`
  trên bản sao `ops/lease_publish.py` của `1d7e642`: một dòng chú thích chèn sau dòng cũ 1009, 1050 và 1113 cho `@@ -1009,0 +1010 @@`, `@@ -1050,0 +1051 @@`, `@@ -1113,0 +1114 @@`
  với `ast.dump` của `kiem` không đổi, nên chỉ vế hunk bắt được chúng — đọc "đoạn cũ rỗng thì không giao" cho cả ba XANH GIẢ —; một hàm hai dòng đặt liền sau `return` cho
  `@@ -1114,0 +1115,2 @@`, cách một dòng trống `@@ -1115,0 +1116,3 @@`, cách hai dòng trống `@@ -1116,0 +1117,4 @@`: cả ba NGOÀI)); trả 3 phần tử ⇒ `t01` ĐỎ (`ValueError: too many values to unpack`, đo lượt 3); câu cũ còn trong một
  khối chú thích, hoặc `kiem_bam` vắng khỏi chú thích của `lenh_body` ⇒ ĐỎ. Lời gọi
  `kiem_bam(...)` đặt trong `kiem()` KHÔNG làm `t191` đỏ (đo lượt 3, 16-10-2026, cửa sổ 02:12Z–02:55Z): `t191` 1/1 XANH, vì `_la_chot` chỉ coi `raise Chan` và lời gọi
  tên `_kiem_*`/`_doc_*` là chốt; đổi tên hàm thành `_kiem_bam` hoặc thêm `raise Chan` thì `t191` ĐỎ (`KHONG_CHAM`). Thứ bắt lời gọi tên `kiem_bam` là
  `git diff -U0`, A3b (i) (đặt trước chốt hạn: 13 thay vì 8) và A3b (ii) (13 thay vì 9). Số "263/265, đỏ đúng `t01` và `t191`" của lượt 1–2 là của bản
  dựng đặt `_kiem_bam_spec`, trên nền 265 ca. Các phép đo `t01`/`t191` của lượt 1–3 KHÔNG chạy lại trên `1d7e642`; thứ đo được là thân `t01_…`,
  `t191_…` và bốn hàm `_la_chot`, `_liet_ke_chot_kiem`, `_dem_chot_tho`, `_mien_mot_chot` giống hệt giữa hai nền (so nguồn qua AST, 23-10-2026).
- **A7 (cổng kho):** ruff F delta 0 (multiset) cho các tệp đổi (nền: 2 F841 ở `lease_publish.py`; bản thăm dò: vẫn 2, dời sang dòng
  200–201 khi nối vào dòng 16, hoặc 201–202 khi bọc dòng, tuỳ cách sửa docstring dòng 15–16 — đo lượt 4, đo lại lượt 5; bản thăm dò 23-10-2026, nối vào dòng 16: 200–201, 13:16:26Z). Sổ test sống: `python3 .claude/dev/ci_dang_ky_test.py` in `ĐĂNG KÝ: N+1/N+1` (hai số BẰNG NHAU) và `TỔNG: ĐẠT`, với N = số
  đăng ký ở nền lúc cấp (tại `1d7e642`: N = 24 ⇒ `25/25`; nếu #763 land trước: 26 ⇒ `27/27`; tại `c522c17` từng là 23 ⇒ `24/24`). Đo 13:17:04Z–13:17:11Z 23-10-2026 trên bản sao `c3f6f5f` có một tệp
  THẾ CHỖ `ops/lease_publish_spec_hash_test.py` (một dòng `print("1/1")`, không phải bộ test thật) cộng dòng `MOI` chép bằng kịch bản từ dòng mẫu: `ĐĂNG KÝ: 25/25`,
  `chan=25`, `PHẢN CHỨNG: 1064/1064 đỏ đúng`, `TỔNG: ĐẠT`, rc 0 (nền: `ĐĂNG KÝ: 24/24`, khác đích ⇒ ĐỎ đúng màu "chưa làm"). Chép nguyên (Mục tiêu 6, L6 (b)): trong ứng viên,
  `ast.literal_eval` của phép gán `MOI` ở mức đỉnh `.claude/dev/ci_dang_ky_test.py` cho giá trị của khoá `"ops/lease_publish_spec_hash_test.py"`
  BẰNG giá trị của khoá `"ops/nhanh_don_duoc_test.py"` — so giá trị đã phân tích, không so dòng, nên ngắt dòng giữ nghĩa vẫn XANH còn đổi mẫu
  thì ĐỎ —, và `git diff --numstat <nền> -- .claude/dev/ci_dang_ky_test.py` ra đúng 1 dòng thêm, 0 dòng xoá ("Không sửa dòng nào khác").
  Đo 14:00:14Z–14:00:15Z 23-10-2026 (`do_l6.py`, chỉ phép AST): nền ⇒ ĐỎ (10 khoá, thiếu khoá mới); thêm dòng chép nguyên ⇒ XANH (11 khoá);
  đột biến bỏ neo `$` của mẫu ⇒ ĐỎ; ngắt giá trị sang dòng sau ⇒ XANH. Dòng `số/số` (Mục tiêu 4): trong stdout của
  `python3 -B ops/lease_publish_spec_hash_test.py`, số lần CHÍNH mẫu `MOI["ops/lease_publish_spec_hash_test.py"]` khớp (`re.finditer`, cờ
  `re.M` như `bang_chung_xanh`) = đúng 1, lần khớp ấy là dòng cuối khác rỗng, hai nhóm bằng nhau và ≥ 1 — đếm bằng mẫu của sổ chứ không bằng
  một mẫu viết lại, nên lớp chữ số mà sổ nhận cũng là lớp mà phép đếm nhận (L6 (d)); đếm theo dòng là đúng đơn vị vì sổ cũng khớp theo dòng
  (L6 (b) không áp: đây không phải lời khẳng định văn xuôi bị ngắt cột); chưa chạy được vì bộ test chưa có. Bộ MỚI chạy qua chính `chay_moi` của sổ,
  không cần `--chay` trọn bộ: `chay_moi(moi={<khoá mới>: MOI[<khoá mới>]})` trả 0 và in `ĐẠT rc=0` (số reviewer lượt 2: dòng cuối `27/27`
  ⇒ `CI_DANG_KY ops/lease_publish_spec_hash_test.py: ĐẠT rc=0`; trên tệp thế chỗ 13:17:11Z 23-10-2026: trả 0, in `CI_DANG_KY ops/lease_publish_spec_hash_test.py: ĐẠT rc=0`). `ops/ci_duong_nhanh_test.py` (job `gate-ops`) cho số ca và số đột biến
  bằng nền, `TONG: DAT` (nền 104/104 · 384/384 tại `1d7e642`, 104/104 · 383/383 tại `c522c17`; bản thăm dò KHÔNG có tệp test mới và dòng `MOI`: 104/104 · 384/384 · `TONG: DAT`,
  13:17:17Z–13:26:09Z 23-10-2026 — tại `c522c17`: 104/104 · 383/383, 23:49:03Z–23:51:17Z; tệp thế chỗ cộng dòng `MOI`: 104/104 · 384/384 · `TONG: DAT`, 13:17:17Z–13:26:08Z 23-10-2026). Kích thước ≤ trần sensitive. ĐỎ khi: bỏ dòng `MOI` ⇒ `test sống chưa đăng ký`, `N+1/N`, `TỔNG: ĐỎ` và
  `k01_so_dang_ky_nhan_muc_da_noi` ĐỎ (số reviewer lượt 2 trên nền `c522c17`: `CA: 103/104`, `DOT BIEN: 382/383`, `TONG: DO`, rc 1; đo 23-10-2026 với tệp thế chỗ không dòng `MOI`:
  sổ `ĐĂNG KÝ: 25/24`, `TỔNG: ĐỎ`, rc 1, 13:17:04Z 23-10-2026; `ci_duong_nhanh_test.py` `CA: 103/104`, `DOT BIEN: 383/384`, `TONG: DO`, rc 1, `k01_…` ĐỎ, 13:17:17Z–13:26:09Z 23-10-2026); bộ mới in thêm một dòng
  số/số đứng một mình trước dòng tổng ⇒ `bang_chung_xanh` đọc dòng ấy (đo hàm, bảng thứ hai hàng g) và phép đếm dòng `số/số` ra 2; giá trị
  `MOI` của khoá mới khác giá trị mẫu, hoặc numstat của sổ khác 1 thêm / 0 xoá; `git diff --numstat <nền>` (tệp mới đã `git add -N` hoặc đã commit: `git diff --numstat` trần không liệt kê tệp chưa theo dõi và rỗng sau khi commit, nên một ứng viên +302 dòng vẫn xanh — đo 17-10-2026, git 2.43.0) thoát rc ≠ 0 hoặc vượt 450 dòng
  thêm (trần ADR-0053 mà r4 áp, hàng `review_class`; lúc soạn r3 là 300) hoặc 3 tệp (write set).

## Ngoài phạm vi (cố ý)

- `plan_hash`: không có quy ước chung về tệp plan (chủ kho chốt Q8).
- Sửa `ops/lease_publish_test.py`, `ci.yml` (lúc soạn r3 thuộc write set #748 — lease r11 giữ chúng lúc 23:32Z 15-10, hạn `2026-10-16T04:27:21Z`; #748 đã merge (bốn hồ sơ land của #748 ghi `landed: false`, không chặn — `depends_on` (1));
  đo lại `ai-dang-giu` 13:21:52Z–13:22:26Z 23-10-2026: `ops/lease_publish_test.py` `NGƯỜI_GIỮ 0`, `.github/workflows/ci.yml` `NGƯỜI_GIỮ 1: wp892-r1-g1-claude`, rc 11;
  đo lại 14:03:56Z–14:04:15Z 23-10-2026: `ci.yml` `NGƯỜI_GIỮ 1: wp892-r2-g2-claude` rc 11, `ops/lease_publish_test.py` `NGƯỜI_GIỮ 0` rc 0 — `depends_on` (2)).
  Hai tệp ở ngoài write set theo thiết kế: đăng ký bằng MỘT dòng `MOI` là cách nối CI đúng, không sửa `ci.yml`.
- **`ops/README.md`.** Sau packet, bước 2 (dòng 37–38, `check` trước khi commit) vẫn ĐÚNG (A3 (i)). Hai nợ tài liệu: (1) bảng "Cổng chặn"
  đã thiếu rc 10, 11, 12 (sẵn có, đo tại `c522c17`; `ops/README.md` không đổi tới `1d7e642`) và sẽ thiếu thêm rc 13 do CHÍNH packet này đưa vào (README ngoài write set) — nợ do packet
  thêm một hàng; (2) sẵn có, KHÔNG do packet này gây ra: bước 3 (dòng 43) chỉ `git add ops/leases`, bỏ sót tệp được neo — với `prompt_path` HIỆN NAY đã cho rc 6 ở đường đăng, với spec sẽ cho rc 13 (A3c), đều fail-close.
- Lệch đĩa/blob do chuẩn hoá EOL (`.gitattributes` dòng 8): spec CRLF trên đĩa + lease neo băm CRLF ⇒ `check` trước commit 0, đường
  đăng 13 (Số đo nền). Lệch luôn rơi về phía ĐỎ ở đường đăng, không bao giờ xanh giả; người soạn lease băm tệp sau khi chuẩn hoá LF.
- Người gọi TƯƠNG LAI đọc lease từ REF (blob) mà muốn kiểm băm spec: phải đọc spec từ blob CÙNG ref/tree với lease (luật nguồn,
  Mục tiêu 1) — không có mã trong packet này.
- Windows của bộ test mới: tại `1d7e642`, `ci.yml` dòng 65–70 (đầu ra `os` của job `chuan-bi`) cho `workflow_dispatch` với `runner_set`
  `windows-only` (đầu vào mới của `workflow_dispatch`, dòng 25–34) chỉ `windows-latest`; `workflow_dispatch` khác hoặc PR gắn nhãn `windows` ⇒ `ubuntu-latest` + `windows-latest`;
  còn lại, kể cả push `master`, chỉ ubuntu (ADR-0049); tại `c522c17` là dòng 50–53, chưa có `runner_set`. Gắn nhãn lên PR đang mở KHÔNG tự sinh
  lượt chạy (`pull_request` ở dòng 13 vẫn không khai `types:`). `launcher-windows.yml` không nhắc `ci_dang_ky_test` hay `lease_publish` (0 dòng,
  00:03:51Z 16-10; đo lại 13:25:13Z 23-10-2026: 0 dòng, dù tệp đổi +9/−11). Muốn có Windows trước merge:
  `workflow_dispatch` trên ref ứng viên (lease khai ngân sách CI tay), hoặc ghi `KHÔNG ĐO ĐƯỢC` và nợ có tên.
- Sửa 67 lease không scope (54 tại `c522c17`) hay 5 lease lệch băm — không phải việc của cổng mới; Mục tiêu 5 (miễn bia mộ) và A5b là bắt buộc vì
  `ops-publish-lease.yml` và `kiem_lease` đều đưa lease còn hạn qua `check`.

## Hình dạng kế thừa

Chép từ lịch sử cổng `lease_publish.py` (CLAUDE.md, mục "VÀ BIA MỘ HAI CHIỀU CHỈ DÙNG CHO LEASE CÒN SỐNG", đoạn có "che mất" giữa `rc=8` và `rc=9`, và `t32`): (a) **chốt chạy trước che chốt sau** — vị trí
không còn để executor khai: `kiem_bam` sau `kiem()`, không ở nhánh đã đăng của `kiem-github`; A3b khoá; (b) **dòng xác nhận không đi kèm
việc kiểm** (docstring `kiem`) — A1, A4 khoá. ĐẾM HÌNH DẠNG trong `ops/lease_publish.py` (tệp không đổi từ `6f121a3` tới `1d7e642`, đo lại 00:03:51Z 16-10
trên `c522c17`; các số dòng dưới đây vì thế vẫn đúng tại `1d7e642`): (a) ≥ **4** — `#568`/`#566` (dòng 1228–1236), #589 (dòng 1238–1244, 1272–1280), slug `unposted-error-precedence-changes` hai
lượt (dòng 1160–1167 và 1198); (b) 1. BỘ ĐẾM TIỀN NHIỆM (L4, chép từ biên nhận): hình dạng A "lời khai rộng hơn phép đo" = 7
(`ops/reviews/README.md` dòng **484** tại `c522c17`, dời từ 482; vẫn dòng 484 và vẫn `A=7 · D=3 · E=4` tại `1d7e642` — tệp đổi +18/−0, cả ba
hunk sau dòng 660, đo 23-10-2026) và 8 theo `ops/specs/t33-doi-shellcheck-r3.md` dòng 104, 266 (tệp không đổi tới `1d7e642`); E = 4;
D = 3. Ghi thêm, KHÔNG tự tăng bộ đếm (người giữ kho quyết): lượt 2 bắt r2 mắc A ba lần (B5: số 15 ca áp cho 26 ca; B6: số tuyệt đối không
ghi điều kiện ref; B8: chú thích khai rộng hơn mã sau packet; lượt 3 đo thêm hai ca của r3 — A6b khai `t191` đỏ với tên `kiem_bam` (xanh, đo), hàng B4 khai "Mỗi yêu cầu … có một ca và một đột biến" (sáu yêu cầu sống sót) — người giữ kho quyết có tính vào bộ đếm A hay không); Codex bắt một hình dạng MỚI — **(c) chốt đọc từ một nguồn khác nguồn của
thứ nó ràng buộc**: r2 đã đo lease được đọc từ ĐĨA (r2 dòng 90) mà vẫn chọn `HEAD` cho spec, rồi khai nợ cho runbook mà chính lựa chọn
ấy làm gãy (lần 1). Lượt soạn r4 đo thêm hai ca của lớp L6 ("tiêu chí trông chặt mà mù") trong chính chữ r3, cũng KHÔNG tự tăng bộ
đếm: A1 của r3 xanh sẵn trên nền khi fixture mang `prompt_path` = `spec_path`, và A6b của r3 (`grep -c` theo dòng) xanh khi câu cũ bị ngắt
dòng hoặc khi chú thích bị xoá (Nghiệm thu A1, A6b). Lượt soạn r3 tự mắc một ca "rig tự đẻ kết quả giả": kịch bản đo `.gitattributes` đặt trùng tên thư mục clone với ca
trước, cho rc 0 sai; chạy lại với tên riêng mới ra rc 13 (23:52:28Z) — số ghi ở trên là số sau khi sửa. Ngưỡng "lặp ba lần" (L4) ĐÃ CHẠM với
(a) và với A: trước khi cấp lease phải có bằng chứng bền (đường dẫn comment) chủ kho đồng ý tiếp — thiếu thì DỪNG (`depends_on` (5)).

## Chưa đo được

- Hành vi trên Windows (đường dẫn, NFC trên NTFS, symlink, `gh` giả, PATH rỗng) — chỉ đo Linux; không trigger tự động nào đo thay.
- Lượt Codex có chạy được không: đo 15-10 sáng (`SAP_HET_HAN`, ảnh chụp cũ ~185 h); lượt soạn r3 KHÔNG đo lại; lần đo lại nền 23-10-2026 và lượt soạn r4 cũng KHÔNG đo.
- Đường dẫn comment của quyết định chủ kho 15-10 về sổ test sống và về đồng ý đi tiếp ở ngưỡng L4 (`depends_on` (5)); comment 23-10-2026
  (hàng `base`) không nói tới hai việc ấy.
- Byte của comment quyết định chủ kho 23-10-2026 trên GitHub: chỉ đọc qua MỘT client (`gh api`, miễn trừ của hợp đồng), không có client thứ
  hai để đối chiếu; nội dung dẫn ở đây là nội dung đã đọc về.
- Các quyết định chủ kho nêu trong spec mà không kèm đường dẫn comment — Q7, Q8 (hàng `nguon_cap_viec`, mục Ngoài phạm vi); vòng vá P3 "thứ 2/2" và "thêm thứ 1/2" (mục Vá sau review lượt 4, 5); việc chủ kho "đọc chặt" hai lớp thành P2 (mục Vá sau review lượt 8): lời khai của phiên điều phối, KHÔNG tra được từ kho.
- VERDICT lượt 5 r28 `d3f1d9db…` và hai vế "đột biến D2, D3, D5, D6, D7 cho rc=0" (nguồn ngoài kho: đo lượt 7 ở `0cfe253`, 0/3520 tệp khớp `d3f1d9db`; đo lại 23-10-2026: 0/5049 mục cây ở `1d7e642`, 13:13:51Z, và 0/1240 blob tên chứa `verdict` trong lịch sử 557 nhánh, hàng `nguon_cap_viec`).
- `VERDICT.md` và `HINT.patch` của mọi lượt review của packet này mà spec dẫn bằng băm (hàng `review của r2` và các mục `Vá sau review lượt N`), bản thăm dò 40 ca cùng ma trận đột biến của lượt 3 (nguồn của 239 dòng, 296 (298), 40/40, `t191` 1/1 ở trên), của lượt 4 (nguồn của 257 = 59 + 197 + 1, dư 43, +1/−1 và +2/−1, 7 hunk, 40/40 của nhóm (7)–(11); các số lượt 4 đo thẳng trên kho — 161/248 ký tự, 174/270 byte (dòng dài nhất của hai tệp ở `c522c17`, hàng `kich_thuoc`), 2765 mục cây dưới `ops/reviews`, `ops/specs`, `ops/land`, `ops/prompts` ở `00a97d3` (`git ls-tree -r --full-tree 00a97d3 -- ops/reviews ops/specs ops/land ops/prompts | wc -l`; toàn cây ở `00a97d3` là 3513 mục, đo 17-10-2026; mục cây = mục của `git ls-tree -r --full-tree <commit>`, không phải blob khác nhau; thiếu `--full-tree` thì lệnh chỉ liệt kê dưới thư mục làm việc — đo 17-10-2026 ở `3976c40`: 3520 mục từ gốc kho, 3123 từ `ops/`, 247 từ `ops/specs/`) — tái lập được từ kho) và của lượt 5 (nguồn của nhóm (12)–(16)), và các kịch bản đo của lượt soạn r3 (`do_nguon.py` `af6eb7dd…`, `dung_tham_do.py` `6dd87cc0…`,
  `do_a3.py` `56f1fbdc…`, `do_b2.py` `b27a6771…`, `do_dot_bien.py` `37bc0d71…`, `do_a6.py` `4b8b4ba6…` — sha256) KHÔNG có trong kho (đo lượt 7 ở `0cfe253`: 0/3520 tệp khớp sáu băm kịch bản và 0 tệp mang tên các kịch bản ấy; VERDICT/HINT: neo ở hàng `review của r2` và các mục `Vá sau review lượt N`); bốn công cụ đo ở Số đo nền (`m_baseline.py`, `m_both.py`, `m_unexp.py`, `m_lease_shapes.py`) cũng KHÔNG có trong kho (đo lượt 8 ở `2dd7f82`: 0 tệp mang các tên ấy); bên thứ
  ba muốn tái lập phải dựng lại bản thăm dò từ chữ Mục tiêu 1–3, 5. Bản thăm dò không được giao (PROTOCOL §8 dòng 655 tại `1d7e642`, 648 tại `c522c17`).
  Đo lại ở `1d7e642` (13:13:51Z 23-10-2026, 5049 mục cây): 0 mục có sha256 bằng bất kỳ băm VERDICT/HINT nào ở trên hay `d3f1d9db…`, 0 mục khớp
  tiền tố của sáu kịch bản, và 0 tệp mang mười tên kịch bản (sáu của lượt soạn r3, bốn `m_*`); các kịch bản dựng lại cho lần đo lại 23-10-2026
  cũng KHÔNG có trong kho (mục `Đo lại nền sau #748 merge` nêu tên và sha256).
- A3b (ii) và các số "của reviewer" ở Nghiệm thu: không đo lại ở lượt soạn r3.
- `python3 .claude/dev/ci_dang_ky_test.py --chay` trọn bộ (bước CI, nặng) — chỉ chạy bản không `--chay` trên nền; việc sổ CHẠY được bộ mới
  là số của reviewer lượt 2.
- Nội dung cuối cùng của #763 và của #752 r3: hai đặc tả đang soạn, chưa đóng băng lúc đọc (23:57:40Z); `depends_on` (4) phải đo lại lúc cấp.
  Lúc 13:08:55Z 23-10-2026 cả hai Issue vẫn `open`; bản trong `c3f6f5f` của hai đặc tả có commit cuối 17-10-2026 (#763) và 16-10-2026 (#752).
  Lúc soạn r4, #763 (r2) và #752 (r4) đang soạn song song trong cùng nhánh đặc tả; r4 này không đọc nội dung đang sửa của chúng, và cả hai
  Issue vẫn `open` lúc 13:56:11Z–13:56:14Z 23-10-2026.
- Các phép đo "đúng chữ r1/r2" và mọi đột biến của A1–A5b không chạy lại trên `1d7e642` (chúng chạy trên kho tạm với `ops/lease_publish.py`
  byte-identical), trừ các phép chạy thử L6 của lượt soạn r4 ghi ở đầu Nghiệm thu, A1, A2 (4), A5b, A6b và A7; `ci_dang_ky_test.py --chay`
  trọn bộ cũng không chạy ở lần đo lại.
- Các tiêu chí khớp chuỗi viết lại ở r4 chưa chạy trên bản thăm dò 40 ca (không có trong kho, không dựng lại): trừ A2b (iii), A3c, A4b (2) và (4)–(8), A5 (2)–(4), A7 (numstat của sổ; đếm dòng `số/số`) (chưa ghi số chạy thử, mục Thay đổi so với r3), chỉ chạy trên
  `ops/lease_publish.py` nền và trên bản thăm dò A6 dựng lại (chỉ tệp ấy, không bộ test), bằng `do_l6.py` và `do_l6b.py`; bộ test của
  executor phải tự khớp theo luật ở đầu Nghiệm thu. Đột biến "in chuỗi có ngoặc của r2" ở A5b chưa chạy.
- Sáu yêu cầu của Mục tiêu 1–3, 5 mà A-list KHÔNG làm ĐỎ (đo lượt 3, 16-10-2026, cửa sổ 02:12Z–02:55Z), bản thăm dò 40 ca, mỗi đột biến một bản sao, cả sáu 40/40: (1) chốt DẠNG áp
  cả khi thiếu `spec_path`; (2) `spec_path` rỗng ⇒ không kiểm; (3) `spec_path` không phải chuỗi ⇒ không kiểm, không `TypeError`; (4) scope giá trị khác
  `sorted NFC casefold exact…` ⇒ không kiểm (A5 (2) chỉ đo scope vắng); (5) `da_bi_thay_the` rỗng hoặc không phải chuỗi KHÔNG miễn; (6) hàng 13 trong docstring
  `MÃ THOÁT`. Executor khai chúng trong PR là kiểm bằng đọc mã; thêm ca (mỗi ca một hàng bảng ≈ 1 dòng) chỉ khi `git diff --numstat <nền>` (tệp mới đã `git add -N` hoặc đã commit, xem A7) còn dư.
- Năm nhóm yêu cầu nữa mà A-list KHÔNG làm ĐỎ (đo lượt 4, 16-10-2026, cửa sổ 03:00Z–03:56Z; bản thăm dò lượt 4 độc lập, KHÔNG giao, 40 ca dạng bảng, mỗi đột biến một bản sao, tất cả
  40/40): (7) thứ tự miễn bia mộ (Mục tiêu 5) — A5b chỉ ghim vế trước chốt tệp (v) của Mục tiêu 5 bằng bước xoá spec; đặt miễn SAU chốt dạng (i), SAU chốt đường dẫn (iv), hoặc đặt kiểm write set
  TRƯỚC miễn đều 40/40, mà lease bia mộ mang băm sai dạng, `spec_path` ra ngoài kho hay `write_set_hash` lệch khi ấy ra rc 13 thay vì 0; (8) thông điệp tệp vắng (Mục tiêu 1 (v)) — bỏ cụm
  "spec phải nằm trong cây cùng lease", bỏ đường dẫn đã tìm, hoặc đổi thành "đã commit tại HEAD" đều 40/40 (A2 (4) của r3 chỉ đòi "không có tệp";
  r4 viết lại A2 (4) theo L6 và cả ba đột biến ấy làm nó ĐỎ trên bản thăm dò A6 dựng lại, 14:03:49Z–14:03:50Z 23-10-2026 — nhóm này nay có tiêu chí); (9) "hex thường" (Mục tiêu 1 (i)) — nhận băm
  viết hoa rồi hạ chữ thường đều 40/40 (không ca nào dùng băm viết hoa); (10) sửa docstring dòng 15–16 (Mục tiêu 1) — không sửa vẫn 40/40 và không tiêu chí nào đo nó (A6b đo chú thích
  `lenh_body`, không đo docstring); (11) `write_set` không phải danh sách (Mục tiêu 2 "phải là danh sách chuỗi") — bỏ chốt kiểu danh sách mà giữ chốt kiểu phần tử vẫn 40/40, trong khi `write_set: null` cạnh scope + băm hợp lệ dạng ra rc 1 kèm `TypeError` thay vì rc 13. Cách xử như (1)–(6): khai trong PR là kiểm bằng đọc mã, thêm ca chỉ khi `git diff --numstat <nền>` (tệp mới đã `git add -N` hoặc đã commit, xem A7) còn dư (bản thăm dò lượt 4 tốn 257 dòng thêm = 59 + 197 + 1, dư 43, nên có chỗ cho ca mới nếu người giữ kho muốn ghim chúng).
- Năm nhóm yêu cầu nữa mà A-list KHÔNG làm ĐỎ (đo lượt 5, 16-10-2026, cửa sổ 04:43Z–05:20Z; bản thăm dò lượt 5 độc lập dựng từ CHỮ A-list, KHÔNG giao: nền 13/40, ứng viên 40/40;
  52 đột biến, mỗi đột biến một bản sao: 31 bị giết, 21 sống 40/40, trong đó 14 thuộc các nhóm (1)–(5), (7)–(9), (11) đã khai — tái lập đúng — và 7 thuộc nhóm mới dưới đây):
  (12) `lenh_body` KHÔNG gọi `kiem_bam` (Mục tiêu 1 "Mã của `lenh_body` … không đổi", chú thích A6b) — cho `lenh_body` gọi `kiem_bam` vẫn 40/40, và `ops/lease_publish_test.py` cùng
  `ops/ci_duong_nhanh_test.py` có 0 chỗ nhắc `spec_path`, `spec_hash`, `spec_sha256_required`; (13) `kiem-github` không gọi `kiem_bam` ở đường lease CHƯA đăng — A3b (ii) chỉ đo đường đã đăng;
  (14) kiểm write set độc lập với kiểm spec (Mục tiêu 2) — để `kiem_bam` thoát sớm khi lease không khai spec thì vẫn 40/40 nếu lease của A4 và của A5 (2) có `spec_path` + băm, và 36/40 nếu lease của cả hai chỉ mang write set:
  A4 và A5 (2) không ghim fixture; (15) thông điệp chốt (i) nêu đúng tên trường — in cứng `spec_hash` cho lỗi dạng của `spec_sha256_required` vẫn 40/40 (A2b (iii) và A4b (2) đều làm hỏng `spec_hash`);
  (16) vị trí và hình dạng lời gọi trong `lenh_check` (Mục tiêu 1 "TRƯỚC mọi `print`", Mục tiêu 3 "`kiem_bam` TRẢ dòng … `lenh_check` in") — gọi giữa hai `print`, gọi sau khối `--du-bao`, hay để `kiem_bam`
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
rc 0); không sửa gì ngoài HINT, trừ chính mục này (đo lượt 5: bản đã áp HINT lượt 4 khác `ops/specs/no-p3-lease-spec-hash-r3.md` ở `d6bc803` đúng 10 dòng thêm tay). VERDICT.md và HINT.patch lượt 4 KHÔNG có trong kho (đo lượt 5 ở `d6bc803`: 0/3513 tệp trên toàn cây mang hai băm trên); thứ định danh là băm. Bốn lớp: `kich-thuoc-so-dem-thieu-docstring-va-don-vi-byte` ·
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
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 7")} f' <tệp spec> | wc -l` ra `9`). 5 lớp:
`chua-do-duoc-tep-khong-co-trong-kho-khong-neo-commit-lan-4` · `don-vi-3520-blob-la-muc-cay-khong-phai-blob-khac-nhau` · `nguoi-tieu-thu-check-khong-deu-chay-tren-cay-sach` · `spec-sha256-ten-thu-ba-khong-doc-lam-sai-nhan-khong-bam-va-khong-khai` · `thay-the-cho-207250f-la-merge-trong-nhanh-pr-khong-phai-vao-master`.

## Vá sau review lượt 8

Bản trước vá: commit `2dd7f82`, sha256 `904668b5de70bfe17233b7c7f4e8c5d61dee5ef901b8a40aadc4571b3cd8ddaf` (`git show 2dd7f82:ops/specs/no-p3-lease-spec-hash-r3.md` ra đúng băm này).
Review lượt 8 (`approve, 0 P1 · 0 P2 · 3 P3`; chủ kho đọc chặt hai lớp đầu theo thứ tự bảng B của VERDICT thành P2; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `2dd7f827a288a73fe34793c0fe709224d4018052`; VERDICT sha256 `0d305e72314354210edf5c3245638e2ba4b2adcc56a1162232904f80cbf0f4a4`, HINT sha256 `80988aa483f7e0221c7f2073f3a779987a09028b8e3ccb626fd66fe112ad3b0c`; hai tệp KHÔNG có trong kho — đo 2026-10-16 ở
`2dd7f82`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 8")} f' <tệp spec> | wc -l` ra `9`). 3 lớp:
`hien-vat-dan-ten-khong-tra-duoc-trong-kho-lan-5-spec-md-va-cong-cu-m` · `no-tai-lieu-bang-cong-chan-thieu-rc-13-do-packet-them-khong-phai-san-co` · `so-dong-them-tay-cua-muc-luot-7-khai-8-do-ra-9`.

## Vá sau review lượt 9

Bản trước vá: commit `3976c40`, sha256 `d8a3ad52f6d01d3449ae12f8dba202e659309eb1c3a8dcd7f2bf29fc54e9b034` (`git show 3976c40:ops/specs/no-p3-lease-spec-hash-r3.md` ra đúng băm này).
Review lượt 9 (`approve, 0 P1 · 0 P2 · 3 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `a870bff64e0e138f233c6bd1b47aca61164a0919`; VERDICT sha256 `40a03f9ed6437792159c99697286ecde441ac63b72fbb525093a0516c294cb00`, HINT sha256 `f1d02aff20f6d7539c6911c112d0ddd980e0df0547018734792b728c7427c8be`; hai tệp KHÔNG có trong kho — đo 2026-10-17 ở
`3976c40`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 9")} f' <tệp spec> | wc -l` ra `9`). 3 lớp:
`hien-trang-va-lease-r11-dang-giu-khong-neo-thoi-diem-han-da-qua` · `quyet-dinh-chu-kho-hai-lop-dau-mo-ho-va-khong-khai-vang-trong-chua-do-duoc` · `so-dong-them-tay-ban-nay-khong-neo-va-muc-luot-8-thieu-dinh-nghia-dem`.

## Vá sau review lượt 10

Bản trước vá: commit `94e4ec2`, sha256 `b00376be7dd485f76625f54f8c73859b8fba003ebdf708574ce36bb5b56d14a3` (`git show 94e4ec2:ops/specs/no-p3-lease-spec-hash-r3.md` ra đúng băm này).
Review lượt 10 (`changes_requested, 0 P1 · 4 P2 · 4 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `7f86e09c969c50447f96a2bf1c8163d97e1e4ac6`; VERDICT sha256 `3f938cb7c4c465d38d598937f2e30d91060b5d9481461505380a92bbecc3976a`, HINT sha256 `de3373b0ed1ab1d85f472ca752f411e88f1c597b5b4633e52094b73448ed16af`; hai tệp KHÔNG có trong kho — đo 2026-10-17 ở
`94e4ec2`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 10")} f' <tệp spec> | wc -l` ra `9`). 8 lớp:
`depends-on-2-origin-ban-sao-cu-khong-ghim-ai-dang-giu-rc0-sai` · `git-diff-nen-va-rc-numstat-tran-khong-thay-tep-moi` · `so-ref-cua-clone-khong-neo-quy-tac-dem-540-542` · `so-dong-them-tay-muc-luot-9-thieu-dinh-nghia-dem` · `muc-cay-thieu-full-tree-va-thu-muc-lam-viec` · `hang-c-eol-thieu-dieu-kien-kho-nguon-khong-co-gitattributes` · `hang-review-r2-khong-co-trong-kho-chi-do-bang-loc-ten-ops-reviews` · `bo-chon-reviewer-lap-ba-co-thieu-tham-so-so-dong-luot`.

## Vá sau review lượt 11

Bản trước vá: commit `f0632bb`, sha256 `8ffee8747bdd0d3cfac290935f675728bc013a9f387312272b1760500f3470a9` (`git show f0632bb:ops/specs/no-p3-lease-spec-hash-r3.md` ra đúng băm này).
Review lượt 11 (`changes_requested, 0 P1 · 1 P2 · 4 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `fe890c0fe7bd46cdd57a0176c59bed028b427ca4`; VERDICT sha256 `d0d50dcb69b315a0f71dc028e0bda9017b4134e990825cf54a097440fe2b644e`, HINT sha256 `2dca217cee331614e5c443412885155e53d74f99e2c58d54b1f6e065c742abde`; hai tệp KHÔNG có trong kho — đo 2026-10-17 ở
`f0632bb`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 11")} f' <tệp spec> | wc -l` ra `9`). 5 lớp:
`dinh-nghia-muc-cay-full-tree-chen-canh-2765-tep-khac-tap-do` · `hermetic-lop-d-ly-do-sai-khi-co-lop-b-hang-c-thieu-dieu-kien-lop-b` · `kich-thuoc-tran-bo-test-244-tinh-tu-uoc-chu-thich-1-do-lai-243` · `mo-dau-thay-doi-so-voi-r2-ngay-15-10-tru-16-10-nhung-co-17-10` · `trich-dan-docstring-ma-thoat-dong-18-26-gom-dong-dong-docstring`.

## Vá sau review lượt 12

Bản trước vá: commit `e074a25`, sha256 `7624d8a0937930964bedbfbbff4e1f9949986e474fa0a827c10753bf0d7e74ee` (`git show e074a25:ops/specs/no-p3-lease-spec-hash-r3.md` ra đúng băm này).
Review lượt 12 (`changes_requested, 0 P1 · 1 P2 · 0 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `e074a2567c2eda7a491e4c15ef898d905038be8b`; VERDICT sha256 `b2329004a92ca1891d2f5b4ea930d6167319ec7b6f1018065e31b41d2df3c41b`, HINT sha256 `5885af9de70af1cfdde1d9c74c111079b166bbc71cb0e48743382db4bb12ec94`; hai tệp KHÔNG có trong kho — đo 2026-10-17 ở
`e074a25`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 12")} f' <tệp spec> | wc -l` ra `9`). 1 lớp:
`moi-truong-do-an-github-actor-github-repository-a3b-ii-a6-so-do-nen-thieu-dieu-kien-chay-lenh`.

## Vá sau review lượt 13

Bản trước vá: commit `2ef2384`, sha256 `629cef69bd1bf0263f501e721a9ad9c12780487be6dc77889f11cf0f763d4ac5` (`git show 2ef2384:ops/specs/no-p3-lease-spec-hash-r3.md` ra đúng băm này).
Review lượt 13 (`changes_requested, 0 P1 · 1 P2 · 1 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `0ebcb89407309ace85ecfa7bc7bb95933b157fe8`; VERDICT sha256 `c30a6eeedd7bba89512683d49c1f53c8d77314b4f3fdc65d16f44e49ca30ed91`, HINT sha256 `ad031435068047fd5f034c3d6447e1769709fbd04a006da8b9317c82e6894c13`; hai tệp KHÔNG có trong kho — đo 2026-10-17 ở
`2ef2384`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 13")} f' <tệp spec> | wc -l` ra `9`). 2 lớp:
`moi-truong-chay-lenh-bullet-thieu-bien-git-ke-thua-qua-goi-git-git-dir-doi-rc-12-a6-43-tren-152` · `moi-truong-github-actor-github-repository-bi-cat-khoang-trang-hai-dau-bullet-khai-dat-ma-ngoai-rc-4`.

## Vá sau review lượt 14

Bản trước vá: commit `7753b81`, sha256 `c53b66b05fee89a93a03bd34e7ba34236c31c22c62e58c32d0146492b0467bb2` (`git show 7753b81:ops/specs/no-p3-lease-spec-hash-r3.md` ra đúng băm này).
Review lượt 14 (`changes_requested, 0 P1 · 1 P2 · 0 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `7753b81ddc9a4c70a646d3047f8b8e42d7fb1144`; VERDICT sha256 `0602ff45946aba52b97d187ab26eeff3d5b72d1c53d4430c0a3cb3ba1996a110`, HINT sha256 `0dd806a7139f94c222ec377c11233cf01292e953653f5281615f1c1080a7ee75`; hai tệp KHÔNG có trong kho — đo 2026-10-17 ở
`7753b81`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 14")} f' <tệp spec> | wc -l` ra `9`). 1 lớp:
`moi-truong-bo-do-nen-va-buoc-dung-kho-tam-nam-ngoai-danh-sach-lenh-cho-phep-git-dir-lam-lease-publish-test-185-tren-265-ci-dang-ky-rc-1-hoac-ghi-commit-vao-kho-khac`.

## Vá sau review lượt 15

Bản trước vá: commit `0910707`, sha256 `7feab768a5e3e98b3ed1d8ecabdd3ec2bdcfd199d9998f55cae0506260ec33e8` (`git show 0910707:ops/specs/no-p3-lease-spec-hash-r3.md` ra đúng băm này).
Review lượt 15 (`changes_requested, 0 P1 · 3 P2 · 1 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `0910707672a873a7cebde6ed17cb31a8c9450dcd`; VERDICT sha256 `ed81403a32f750d199a7ec77abb2e7aff4722dd94fdc48b636723994e560c0e7`, HINT sha256 `0bde00e02c7a68113fc7748bf0c8342169787fc2686fe1840e7efbd568d08882`; hai tệp KHÔNG có trong kho — đo 2026-10-17 ở
`0910707`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). KHÔNG áp HINT lượt 15; thay bằng vá cấu trúc:
bullet Môi trường chạy lệnh, cùng mọi khẳng định trong bullet ấy về kết quả dưới `GIT_DIR`, `GITHUB_ACTOR`, `GITHUB_REPOSITORY` hay `PATH` khác, bị thay bằng MỘT hợp đồng môi trường đo có tiền tố dựng nguyên văn (Số đo nền), dưới đó ba bộ đo nền, hàng (c) bảng thứ hai và các bước cần mạng được đo lại, và lệnh gọi trình thông dịch dùng `python3`; mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 15")} f' <tệp spec> | wc -l` ra `9`); đóng 4 lớp:
`moi-truong-git-dir-khai-rong-hon-phep-do-nhom-kho-tran-185-tren-265-nhom-kho-khong-tran-188-hoac-189-ci-dang-ky-rc-0-dat-voi-la-git-va-kho-that` · `quy-tac-path-don-doc-con-cua-buoc-can-mang-va-depends-on-2-ke-thua-git-dir-fetch-rc-0-ghi-kho-khac-ban-bare-0-ref` · `quy-tac-path-chi-python3-va-git-khong-du-lease-publish-test-241-hoac-257-tren-265-ci-dang-ky-tong-do-thieu-actionlint-va-lenh-python-rc-127` · `tieu-de-bullet-moi-truong-khai-pham-vi-phep-do-lease-publish-hep-hon-than-quy-tac-moi-lenh-do`.

## Vá sau review lượt 16

Bản trước vá: commit `ac79a8b`, sha256 `33a93f9b99caf713c33d1cf6a2c6089a0adb99d20ab75402e304cb82c2ea60e9` (`git show ac79a8b:ops/specs/no-p3-lease-spec-hash-r3.md` ra đúng băm này).
Review lượt 16 (`changes_requested, 0 P1 · 1 P2 · 1 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `ac79a8b95ec015be8570dce3e1fa778524ce8415`; VERDICT sha256 `f7654c830edf7ec56d9d0adcf07c266765b7c45b93fd60d2340f5dd045c19742`, HINT sha256 `674ba731b08aa6357ee15443db40f6de4f9182ca9b92489e417e7fbf64d4b84d`; hai tệp KHÔNG có trong kho — đo 2026-10-17 ở
`ac79a8b`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 16")} f' <tệp spec> | wc -l` ra `9`). 2 lớp:
`hang-c-home-moi-moi-lenh-theo-chu-tien-to-lenh-config-global-khong-toi-lenh-clone-day-byte-1-ra-0a-khong-0d-0a` · `pham-vi-hop-dong-liet-ke-ba-muc-hep-hon-vi-tu-moi-lenh-do-cua-spec-lenh-do-o-hang-bang-chua-do-duoc-va-gh-api-nam-ngoai-danh-sach-gh-rc-127`.

## Đo lại nền sau #748 merge (nền 1d7e642)

Lần đo lại ngày 23-10-2026 cho nền mới của r4 (quyết định chủ kho 23-10-2026, https://github.com/ducthangho/tra-luat/issues/752#issuecomment-6366519792,
mục 2), do subagent Claude thực hiện theo chỉ thị phiên điều phối; đây KHÔNG phải một lượt review. Lượt soạn r4 (13:54Z–14:05Z) đo thêm
các hàng đánh dấu "r4" ở cuối bảng. Nền mới `1d7e642092fb3dda15967be44d095f37bb22ac5f` (`git rev-parse 1d7e642`). Bản sao đo
`c3f6f5f` = `1d7e642` cộng đúng ba tệp `ops/specs/no-p3-*`; một bản sao `1d7e642` chạy lại ba bộ đo nền làm đối chứng và ra cùng số. Mọi
lệnh chạy dưới hợp đồng môi trường đo nguyên văn (Số đo nền); bước cần mạng chỉ thêm biến `HTTPS_PROXY`; trạng thái Issue đọc bằng `gh api`
(miễn trừ của hợp đồng). Giờ UTC; mọi mốc trong mục này là ngày 23-10-2026, trừ cột "cũ".

Độ lệch so với chữ đặc tả, khai thẳng: (1) `ai-dang-giu` quét `refs/heads/*` của bản bare, nên lượt cuối fetch
`'+refs/heads/*:refs/heads/*' '+refs/heads/*:refs/remotes/origin/*'` trong cùng một lệnh (`depends_on` (2)); (2) ca (6) của nguồn đọc
`check` thay PATH bằng một thư mục rỗng, dựng nguyên văn ở Số đo nền; (3) A6 (i) dùng `kiem_bam` THĂM DÒ dựng từ chữ Mục tiêu 1, 2, 5 ngay
trong kịch bản; A6 (ii), A6b và A7 dùng bản sao `ops/lease_publish.py` có `kiem_bam` chèn vào `lenh_check` (+61/−2, 7 hunk — bản dựng ĐỂ ĐO,
không thay số của hàng `kich_thuoc`); A7 dùng một tệp THẾ CHỖ `ops/lease_publish_spec_hash_test.py` chỉ có một dòng `print("1/1")`; không bản
nào được giao; (4) kịch bản đo của lượt soạn r3 không có trong kho nên được dựng lại, và mỗi kịch bản dựng lại có đáp án đã biết khi có thể:
`m_cay.py` và `do_a6.py` chạy trên `c522c17` tái lập đúng số cũ, `do_dai.py` tái lập 161/248 và 174/270.

| mục (đơn vị) | cũ, nền `c522c17` | mới, nền `1d7e642` | lúc đo | lệnh hoặc kịch bản |
|---|---|---|---|---|
| `master` máy chủ · nhánh máy chủ (nhánh) | `9fddb1d` · 541 (23:31:30Z 15-10) | `1d7e642` · 556, rồi 558, rồi 560 | 12:58:02Z · 13:02:47Z · 13:20:16Z | `git ls-remote --heads origin` so `git for-each-ref refs/remotes/origin` theo tên và OID: thiếu 0, thừa 0, lệch 0 mỗi lần |
| Issue #748 · #751 · #763 | `open` · `open` · `open` (15-10) | `closed`/`completed` lúc 2026-10-20T01:19:38Z · `open` · `open` | 13:08:55Z | `gh api repos/ducthangho/tra-luat/issues/<số>` |
| `ai-dang-giu` cho ba đường dẫn write set (rc) | 0 · 0 · 11, lease r11 của #748 | 0 · 0 · 11, lease `wp892-r1-g1-claude` | 13:20:18Z–13:21:52Z | `python3 -B ops/lease_publish.py ai-dang-giu <đường dẫn> --root <bản bare>` (`adg.sh`) |
| kho cục bộ so máy chủ (nhánh) | thiếu 4 · lệch OID 3 | thiếu 91 · thừa 69 · lệch OID 1 (538 so 560) | 13:23:41Z | `git for-each-ref refs/remotes/origin` trên `/home/user/tra-luat`, chỉ đọc, so `ls-remote` |
| `ops/lease_publish_test.py` (ca) | 265/265 | 267/267 | 12:56:27Z–13:03:11Z | `python3 -B ops/lease_publish_test.py` |
| sổ: `ĐĂNG KÝ` (đường dẫn test) · `PHẢN CHỨNG` (ca phản chứng) | 23/23 · 1025/1025 | 24/24 · 1064/1064 | 12:56:27Z–12:56:35Z | `python3 -B .claude/dev/ci_dang_ky_test.py` |
| `ci_duong_nhanh_test`: `CA` (ca) · `DOT BIEN` (đột biến) | 104/104 · 383/383 | 104/104 · 384/384 | 12:56:27Z–13:00:06Z | `python3 -B ops/ci_duong_nhanh_test.py` |
| ruff F trên `ops/lease_publish.py` (lỗi) | 2 F841, dòng 198–199 | như cũ | 13:04:18Z | `ruff check --isolated --select F ops/lease_publish.py` |
| phiên bản năm công cụ | Python 3.11.15 + PyYAML 6.0.1, git 2.43.0, actionlint 1.7.7, shellcheck 0.9.0, ruff 0.15.8 | như cũ | 13:04:19Z | lệnh in phiên bản của từng công cụ |
| `ops/leases/*.yaml` (tệp) | 152 | 171 | 13:11:05Z | `m_cay.py` |
| có `spec_path` + băm · cả hai trường · khớp · lệch (lease) | 99 · 8 · 94 · 5 | 118 · 18 · 113 · 5, cùng năm tên | 13:11:05Z | `m_cay.py` |
| có `write_set_hash`: có scope, khớp (a) · không scope, khớp (a) (lease) | 6, 6/6 · 54, 0/54 | 6, 6/6 · 67, 4/67 | 13:11:05Z | `m_cay.py` |
| mang `spec_sha256` · không kèm hai tên kia (lease) | 57/152 · 5/152 | 61/171 · 5/171 | 13:11:05Z | `m_cay.py` |
| blob lease ở đầu nhánh (blob) | 619 trên 540 nhánh | 680 trên 559 nhánh | 13:29:49Z–13:29:57Z | `m_ref.py`, bỏ nhánh của chính đặc tả |
| cả hai trường · bằng nhau · chưa hết hạn · sai dạng (blob) | 17 · 15 · 7 · 0 | 62 · 60 · 4 · 0 | 13:29:49Z–13:29:57Z | `m_ref.py` |
| blob tên chứa `verdict`: khớp `d3f1d9db…` · trong lịch sử · ở đầu nhánh (blob) | 0 · 1102 · 831 | 0 · 1240 · 967 | 13:12:37Z–13:13:36Z | `m_verdict.py` |
| mục cây toàn kho (mục) · mục khớp VERDICT/HINT r2 | 3510 · 0 (17-10) | 5049 · 0 | 13:13:51Z | `m_tree.py` |
| A6 nền (lease theo rc) | `{0: 143, 8: 4, 10: 5}` | `{0: 157, 8: 9, 10: 5}` | 13:15:10Z–13:24:46Z | `do_a6.py` |
| A6 ứng viên · tập đổi rc | `{0: 142, 8: 4, 10: 5, 13: 1}` · {`…-exec-1r4` 0 → 13} | `{0: 156, 8: 9, 10: 5, 13: 1}` · CÙNG tập | 13:15:10Z–13:24:46Z | `do_a6.py` |
| A6 miễn bia mộ · kiểm spec khớp · kiểm write set khớp · đột biến bỏ miễn đổi rc (lease) | 38 · 60 · 4 · 5 | 46 · 66 · 4 · 5, cùng năm tên | 13:15:10Z–13:24:46Z | `do_a6.py` |
| A6 (ii) bản thăm dò chạy `lease_publish_test.py` (ca) | 265/265 | 267/267 | 13:17:17Z–13:26:53Z | bản sao dựng bằng `dung_tham_do.py` |
| A6b bản thăm dò: hunk · hunk trong 1009–1114 · dòng chứa câu cũ | 7 · 0 · không ghi | 7 · 0 · 0 | 13:33:40Z | `do_a6b.sh` |
| A7 đích `ĐĂNG KÝ` (đường dẫn test) | N = 23 ⇒ 24/24; #763 trước ⇒ 26/26 | N = 24 ⇒ 25/25 (đo trên tệp thế chỗ + dòng `MOI`: 25/25, 1064/1064, `TỔNG: ĐẠT`); #763 trước ⇒ 27/27 | 13:17:04Z–13:17:11Z | `them_moi.py` rồi lệnh sổ |
| A7 bỏ dòng `MOI`: sổ · `ci_duong_nhanh_test` | `N+1/N` · 103/104, 382/383, `TONG: DO` (số reviewer) | 25/24, `TỔNG: ĐỎ`, rc 1 · 103/104, 383/384, `TONG: DO`, rc 1, `k01_…` ĐỎ | 13:17:04Z · 13:17:17Z–13:26:09Z | tệp thế chỗ, không dòng `MOI` |
| A7 `ci_duong_nhanh_test`: bản thăm dò không tệp mới · tệp thế chỗ + `MOI` | 104/104 · 383/383 · không đo | 104/104 · 384/384 · 104/104 · 384/384 | 13:17:17Z–13:26:09Z | `python3 -B ops/ci_duong_nhanh_test.py` |
| A7 `chay_moi` cho khoá mới | `ĐẠT rc=0` (số reviewer) | trả 0, `ĐẠT rc=0` (tệp thế chỗ) | 13:17:11Z | `do_chay_moi.py` |
| A7 ruff F bản thăm dò (lỗi) | 2 F841, 200–201 hoặc 201–202 | 2 F841, 200–201 (nối vào dòng 16) | 13:16:26Z | `ruff check --isolated --select F ops/lease_publish.py` |
| hàng (g): `bang_chung_xanh` trên ba chuỗi | True · False · True | như cũ | 13:09:24Z | `do_g.py` |
| nguồn đọc `check`, sáu ca (rc) | 0 · 6 · 4 · 0 · 0 · 0 | như cũ | 13:24:54Z–13:24:55Z | `do_nguon.sh` |
| lớp write set · bộ chọn reviewer | `sensitive` · opus-5/xhigh "tổng=2", fable-5/xhigh "tổng=4" | như cũ | 13:14:21Z | `do_lop.py` |
| trần `sensitive` (tệp · dòng thêm) | ADR-0044: 3 · 300 | ADR-0053: 6 · 450, qua dòng khai dưới bảng đầu; ba phép đo OID `8ab1007…`: rc 0 · rc 128 · rc 0 | 13:17:29Z–13:17:31Z | `git cat-file -e`, `git rev-list --first-parent` trên bản bare không nông |
| dòng dài nhất `lease_publish.py` · `lease_publish_test.py` (ký tự; byte) | 161 · 248; 174 · 270 | như cũ | 13:28:58Z | `do_dai.py` |
| `--help` chứa `MÃ THOÁT` · năm tên trong `lease_publish.py` · `launcher-windows.yml` nhắc hai bộ (dòng) | 0 · 0 · 0 | 0 · 0 · 0 | 13:20:07Z · 13:25:13Z | `grep -c` |
| r4 · `master` máy chủ · nhánh máy chủ (nhánh) | `1d7e642` · 560 (13:20:16Z) | `8324567` (PR #891; 0 dòng đổi trên write set, bộ đo nền, SKILL soan-spec, `chon_reviewer.py`, ADR-0053) · 562, rồi 563 | 13:54:20Z · 14:03:56Z | bản bare mới, `adg_r4.sh`: thiếu 0, thừa 0, dòng lệch 0 mỗi lần, so với cả `refs/remotes/origin` lẫn `refs/heads` |
| r4 · `ai-dang-giu` ba đường dẫn write set (rc) | 0 · 0 · 11, `wp892-r1-g1-claude` | 0 · 0 · 11, `wp892-r2-g2-claude` (hạn `2026-10-24T13:46:00Z`) | 13:54:21Z–13:55:00Z | `adg_r4.sh` |
| r4 · `ai-dang-giu` `ci.yml` · `lease_publish_test.py` · `ci_duong_nhanh_test.py` (rc) | 11 · 0 · không ghi | 11 · 0 · 11, người giữ `wp892-r2-g2-claude` | 14:03:56Z–14:04:36Z | `adg_r4.sh` |
| r4 · ba phép đo OID của ADR-0053 (rc) | 0 · 128 · 0 | 0 · 128 · 0 (bản bare không nông, `master` `8324567`) | 13:57:24Z | `git cat-file -e`, `git rev-list --first-parent` |
| r4 · tên khái niệm ADR-0053 trên sáu tệp cổng §20 (dòng) | không đo | 0 cho `ADR-0053` `0053` `tran_kich_thuoc_sensitive` `450` ở cả sáu; `nang_tran` `ai_nang` `tran_cu` `tran_moi` 0 ở năm tệp, 8 · 4 · 2 · 5 ở `packet_loop.py` (trục vòng và lời gọi) | 13:57:36Z | `do_cong.sh` |
| r4 · bộ chọn reviewer theo `--so-dong` 300 · 399 · 400 · 450 (`--luot 1`) | không đo | tổng 4 · 4 · 5 · 5; `xhigh` · `xhigh` · `max` · `max`, cùng `claude-fable-5`; 450 với `--luot 3`: tổng 6, `max` | 13:57:16Z · 13:57:24Z | `chon_reviewer.py` qua `e.sh` |
| r4 · hồ sơ land #748 ghi `landed: false` · r3 trên nhánh máy chủ (tệp · ref) | không đo | 4 · 0 ref chứa `d269836` | 14:00:44Z | `do_land748.sh` |
| r4 · chạy thử L6 trên nền · trên bản thăm dò dựng lại (tiêu chí) | không đo | A1, A2 (4), A4, A5 (1), A5b hai ca, A6b, A7 `MOI`: ĐỎ cả trên nền · XANH cả trên bản thăm dò (A7: trên bản sao sổ có dòng chép nguyên); A1 với `prompt_path` = `spec_path`: XANH ngay trên nền | 14:00:14Z–14:03:50Z | `do_l6.py`, `do_l6b.py` |
| r4 · đặc tả #892 hiện hành: dòng `MOI` `DA_NOI` `DANG_KY` `ĐĂNG KÝ` · dòng nhắc `ci_dang_ky_test` | 0 · 2 (`wp892.md`) | 0 · 2 (`wp892-r2.md`, 78 dòng) | 13:58:03Z | `do_wp892_r2.sh` |

Số dòng dẫn vào tệp đã đổi, cũ → mới (đọc tệp tại `1d7e642`; thân hàm so qua AST bằng `cmp_fn.py`):
`.claude/dev/ci_dang_ky_test.py` — `MOI` 37–53 → 38–55, dòng mẫu `nhanh_don_duoc` 52 → 53, `DANG_KY` 80 → 82, `tim()` 83 → 104 (thân ĐỔI,
thêm `_git_bo_qua`), `kiem()` 579 → 640, `bang_chung_xanh` 616–620 → 677–681 (`re.search` 617 → 678), `chay_moi` 967 → 1055 (ba thân sau
giống hệt); `.github/workflows/ci.yml` — job `gate-registry` 827 → 937, `--chay` 895 → 1008, đầu ra `os` 50–53 → 65–70 (thêm `runner_set`);
`ops/lease_publish_test.py` — `_la_chot` 9541–9547 → 9869–9875, `t01` 705 → 706 (thân giống hệt); `docs/PROTOCOL_DA_PHIEN.md` — 648 → 655,
696 → 703, 705–707 → 712–714 (cùng chữ); `ops/reviews/README.md` — dòng 484 không dời. Mọi số dòng dẫn vào tệp KHÔNG đổi (hàng `base`) giữ nguyên.

Kịch bản đo — KHÔNG có trong kho, chỉ nằm trong scratchpad của phiên đo và mất khi phiên đóng; sha256, 12 ký tự đầu: `chay.sh` `a1a2483e36a9…`
(bọc tiền tố hợp đồng, ghi rc và mốc giờ) · `adg.sh` `4322af28b58c…` · `m_cay.py` `d84cd886125e…` · `m_ref.py` `e80f46eb9931…` ·
`m_verdict.py` `9d791c301d40…` · `m_tree.py` `7c35311e25dc…` · `do_a6.py` `4ef113e3e605…` · `dung_tham_do.py` `1c869c4a3a14…` ·
`them_moi.py` `8eada63afcfb…` · `do_chay_moi.py` `770a7682071d…` · `do_g.py` `8b9b3788adc8…` · `do_lop.py` `8dc11411bf81…` ·
`do_nguon.sh` `19916b7a6149…` · `do_dai.py` `fc05b6958cc3…` · `do_nho.sh` `c2ae1abcc2d0…` · `do_a6b.sh` `464aef375afd…` ·
`do_wp892.sh` `d52413f1ac6a…` · `cmp_fn.py` `093f96c4eac3…` · `smoke.sh` `ee306219e82f…`. Lượt soạn r4 thêm, cùng điều kiện lưu giữ:
`e.sh` `8d41d7ae4b05…` (bọc tiền tố hợp đồng cho một lệnh) · `adg_r4.sh` `3a6c4e9f6ea9…` · `do_cong.sh` `b456d16709d0…` ·
`do_wp892_r2.sh` `2330b26fc696…` · `do_land748.sh` `b3cdf1731b8c…` · `do_l6.py` `97f959fafe4e…` · `do_l6b.py` `44cd85c37c13…`, cùng bản
diff dựng lại bản thăm dò `814aec71ba99…` (đầu ra của `do_a6b.sh`). Bên thứ ba muốn tái lập phải dựng lại từ định nghĩa ghi ở từng hàng
của Số đo nền và ở đầu Nghiệm thu.

Hệ quả đo được cho tiêu chí (ghi để người duyệt quyết, KHÔNG thiết kế lại ở đây): tập đổi rc của A6 (i) KHÔNG đổi, chỉ số tuyệt đối trôi;
đích A7 thành `25/25`; `depends_on` (2) vẫn ĐỎ nhưng vì lease #892 (lúc soạn r4: `wp892-r2-g2-claude`), và lease ấy giữ cả
`ops/ci_duong_nhanh_test.py`, nên (3) kích hoạt nếu #892 land trước lúc cấp; trần dòng thêm 300 → 450 làm câu "chỉ đủ khi giữ kiểu dày" (hàng `kich_thuoc`) và lý do "vượt trần sensitive 3 tệp" (hàng
`write_set`) hết đúng, ngưỡng ĐỎ dòng thêm của A7 nới tương ứng.

## Vá sau review lượt 18

Bản trước vá: commit `fe19221`, sha256 `fce346dae49ba42576b018cfe804911c9c899c93c4c464b7c80f56153ec978f5` (`git show fe19221:ops/specs/no-p3-lease-spec-hash-r4.md` ra đúng băm này).
Review lượt 18 (`changes_requested, 0 P1 · 4 P2 · 4 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `fe19221024f66cc9726c65e01049ec486571ac1d`; VERDICT sha256 `cab92cecf09a263060f7cc8f825e05509a68dfb746a3739c100e955a4fcc8c95`, HINT sha256 `74942aed4d8927d0ca03289cfe74c0dba2117c8e0de349edeba089524df3cfa1`; hai tệp KHÔNG có trong kho — đo 2026-10-23 ở
`fe19221`: 0 trên 5052 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 18")} f' <tệp spec> | wc -l` ra `9`). 8 lớp:
`phan-hoach-toan-ref-3-blob-spec-hash-null-khong-co-khoa-spec-path-nam-o-nhom-khong-spec-path-khong-bam-95-khong-phai-nhom-spec-path-null-27` · `a5b-ve-am-bia-mo-dat-o-ca-rc-13-khong-bat-duoc-dong-mien-in-cho-lease-chua-bi-thay-the-dot-bien-song-40-40` · `a0-doi-moi-so-do-nen-nhung-co-so-anh-chup-theo-gio-nen-khong-bao-gio-xanh-chua-het-han-4-thanh-1-tai-moc-cap-som-nhat` · `lich-su-nen-0-dong-tren-cac-tep-spec-dan-nhung-ops-reviews-readme-md-them-12-dong-giua-6f121a3-va-c522c17` · `a6b-hunk-chen-ngay-tren-def-kiem-co-vi-tri-cu-1008-nam-ngoai-1009-1114-decorator-qua-ca-ve-hunk-lan-40-ca-can-ast-dump` · `a2-4-noi-ba-phan-cua-muc-tieu-1-v-nhung-muc-tieu-1-v-chi-ghi-hai-phan-va-khong-co-tep-chi-nam-o-hang-a` · `moi-cho-ghi-so-chay-thu-tren-nen-va-ban-tham-do-rong-hon-ban-ghi-thieu-a2b-iii-a3c-a4b-a5-2-4` · `748-da-land-con-sot-khi-depends-on-1-doi-sang-merge-va-bon-ho-so-land-ghi-landed-false`.

## Vá sau review lượt 19

Bản trước vá: commit `a578f65`, sha256 `af16068fcc20ad8db2b93718b655e59649dc0ccd876063f1a4c058023e21c909` (`git show a578f65:ops/specs/no-p3-lease-spec-hash-r4.md` ra đúng băm này).
Review lượt 19 (`changes_requested, 0 P1 · 2 P2 · 4 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `a578f6541d980ff1c29371f0a5c980b46fe8a9b5`; VERDICT sha256 `cc6f52fe006381a651619ab91bdc10590b51c8e6bed07221127c348daf5d0d90`, HINT sha256 `825650616db0e8ae15bb8cd692a2fa672a5ab49087050ca2d86d00a6e7571e8c`; hai tệp KHÔNG có trong kho — đo 2026-10-24 ở
`a578f65`: 0 trên 5052 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 19")} f' <tệp spec> | wc -l` ra `9`). 6 lớp:
`a0-nguon-doc-cua-check-nam-trong-danh-sach-chi-phu-thuoc-cay-nhung-fixture-wp892-r1-het-han-2026-10-24t13-01z-sau-do-bon-ca-rc-0-thanh-rc-8-a0-do-khi-cho-r2-het-han` · `muc-cuoi-tro-sai-muc-sau-khi-them-muc-va-sau-review-luot-18-sau-muc-do-lai-nen-bay-cho-dan-dong-14-16-25-34-243-440` · `a6b-hunk-do-dai-0-sat-bien-1114-chua-phan-trong-hay-ngoai-hai-cach-doc-cho-mau-nguoc-nhau-1050-0-lot-qua-cach-doc-doan-cu-rong` · `748-land-con-sot-o-dong-34-sau-khi-lop-8-luot-18-chi-sua-hai-trong-ba-cho-372-583` · `chua-do-duoc-nua-chay-thu-viet-lai-rong-hon-ban-ghi-va-danh-sach-con-lai-o-nghiem-thu-thieu-a7-numstat-va-dem-dong-so-tren-so` · `hop-dong-cau-ket-ngoai-hop-dong-khong-tru-quan-sat-gh-api-ma-cau-dau-dat-ngoai-hop-dong-ton-tu-luot-17-hunk-khong-ap-duoc`.

## Vá sau review lượt 20

Bản trước vá: commit `edf7b59`, sha256 `49327bec03114c6bd9562f7866abb0c27adcdfb1bc8bbb1ea23e82528a0ba96d` (`git show edf7b59:ops/specs/no-p3-lease-spec-hash-r4.md` ra đúng băm này).
Review lượt 20 (`changes_requested, 0 P1 · 1 P2 · 0 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `edf7b59e9155295bac2a9ac12b929af6f5385d56`; VERDICT sha256 `be0adda30ea4c8a8640ea639cd48c3e9547d2b0291df194841d0da9446a1b8b2`, HINT sha256 `ebee654b2c09b8cb6999896d244991e9a3a1c337234f158a7f13a387b4cebb79`; hai tệp KHÔNG có trong kho — đo 2026-10-24 ở
`edf7b59`: 0 trên 5052 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 20")} f' <tệp spec> | wc -l` ra `9`). 1 lớp:
`thay-the-cho-hang-duoi-tro-lech-mot-hang-no-spec-r2-751-752-nam-o-hang-finding-sau-review-cach-hai-hang-ton-tu-r3`.

## Vá sau review lượt 21

Bản trước vá: commit `7ba1209`, sha256 `385f0b0e929f38174af0318d482f2990fa650267b5b1d875c83e3ac5b19a08bd` (`git show 7ba1209:ops/specs/no-p3-lease-spec-hash-r4.md` ra đúng băm này).
Review lượt 21 (`changes_requested, 0 P1 · 1 P2 · 0 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `cd5e4904a5e62c95cc67eb7f2df8333a95294e5d`; VERDICT sha256 `cc349e206d65102b7672ce93a77790eeb87ddcc4e4e7d787d7e9d3d5e14a9b09`, HINT sha256 `6c168456b4126cf3609b60d395b80f2a380f04ece6d3647c60d5d671571b30f3`; hai tệp KHÔNG có trong kho — đo 2026-10-24 ở
`7ba1209`: 0 trên 5052 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 21")} f' <tệp spec> | wc -l` ra `9`). 1 lớp:
`trich-dan-nhay-kep-khong-nguyen-van-voi-nguon-neu-ten-ban-nhap-claude-md-rc-8-che-rc-9-muc-tieu-3-hang-write-set-hang-b4-skill-l4-lan-ba`.

