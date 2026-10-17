# Đặc tả packet `no-p3-dang-ky-ci` r1 — đăng ký hai bộ test của #752 vào sổ test sống

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-dang-ky-ci` |
| `packet_issue` | #763 — https://github.com/ducthangho/tra-luat/issues/763 ("Packet NO-P3-DANG-KY-CI: đăng ký hai bộ test của #752 vào ci_dang_ky_test.py", `open`, mở bởi `ducthangho` `2026-10-15T23:26:04Z`; đọc qua `gh api repos/ducthangho/tra-luat/issues/763` ~23:27Z 15-10-2026). |
| `revision` | 1 |
| `thay_the_cho` | Không có revision trước. Nội dung TÁCH từ mục tiêu 5 và B6(a) của `ops/specs/no-p3-cong-cu-ho-so-r2.md` (#752 r2, sha256 `ce39f1e164fd94e342af59a0624cec1fc23fc84574f0ec1e5c627a656a17593b`, commit `a9ef33c`); r2 ấy đóng băng, không sửa. Bản anh em cùng lượt: `ops/specs/no-p3-cong-cu-ho-so-r3.md` (#752 r3). |
| `nguon_cap_viec` | Quyết định chủ kho 15-10-2026 **"tách 2 packet"** (chuyển tới qua phiên điều phối; thân Issue #763 ghi lý do, phạm vi, phụ thuộc và tên tệp đặc tả này). Lý do tách: finding P2 của connector Codex trên PR #762, `pull/762#discussion_r4286041896` ("Apply the sensitive packet size ceiling", `created_at 2026-10-15T17:13:10Z`) — sửa sổ test sống là đổi CI/gate authority nên #752 r2 (5 tệp, ~900 dòng) vượt trần `sensitive` 3 tệp/300 dòng. Nợ `SPEC-R2-751-752-KHONG-DUOC-CAP-LEASE` (`ops/land/pr759-no-p3-ho-so-land-evidence.yaml` dòng 407, `trang_thai: mo`). Hai test được đăng ký là mục tiêu 2 và 4 của #752 r3. |
| ngưỡng chặn | Theo bảng PROTOCOL §8 dòng 621 cho lớp `sensitive`: không còn P0; cần approval tường minh đúng assurance và quyết định có căn cứ cho từng finding còn mở. Ngưỡng "chỉ P1/P2 chặn" của #752 không tự áp sang #763 — chưa có nguồn thẩm quyền riêng cho #763 (KHÔNG ĐO ĐƯỢC). |
| `review_class` | **`sensitive`** · `effective_review_class`: **`sensitive`**. Hai nguồn độc lập khớp nhau, cộng một phép gọi cổng chỉ chứng minh cổng fail-closed (hàng chú thích ngay dưới): (1) thân Issue #763 "Lớp sensitive"; (2) PROTOCOL §8 dòng 724 xếp "workflow/CI authority" vào `sensitive` — sổ này quyết định tập test mà bước `test registry` của job `gate-registry` chạy (`.github/workflows/ci.yml` dòng 889–895), đúng lập luận của finding `r4286041896`; (3) cổng, đo 23:35:43Z 15-10-2026 bằng cách gọi thẳng hàm của `ops/lease_publish.py` @ `c522c17`: `_tinh_lop_tu_write_set([".claude/dev/ci_dang_ky_test.py"])` ⇒ `sensitive` (không mục nào trong 7 mục `_BANG_LOP` khớp, rơi về `sensitive`); lưới `_kiem_lop_review` (role `executor`, `schema_version: 2`) 4 giá trị khai × 4 giá trị hiệu lực (`routine`, `systemic`, `sensitive`, `standard`; đo 16-10-2026 tại `c522c17`; `standard` KHÔNG thuộc `_THU_TU_LOP` của mã — với đúng ba giá trị của mã, lưới là 3 × 3: 3 ô qua, 6 ô rc 10): chỉ 4 ô `effective_review_class: sensitive` qua, 12 ô còn lại rc 10. Patch-as-hint: PROTOCOL §8 dòng 648 chỉ cho packet `sensitive` dùng hint với tệp TEST thuần hoặc tooling không tham gia gate; tệp sổ mang đuôi `_test.py` nhưng LÀ cổng `gate-registry` ⇒ đọc theo hướng chặt (fail-closed): reviewer mô tả finding bằng lời, không đính `HINT.patch` cho tệp này. |
| `review_class` — chú thích nguồn (3) | Nguồn (3) chỉ chứng minh cổng fail-closed, không chứng minh phân lớp theo đường dẫn: `_BANG_LOP` có 7 mục, cả 7 là `sensitive`, và đường không khớp rơi về `sensitive` — nên `_tinh_lop_tu_write_set` trả `sensitive` cho MỌI đường (đo 01:49Z 16-10-2026 tại `c522c17`, gọi thẳng hàm của `ops/lease_publish.py`: `docs/x.md`, `ops/kiem_ho_so_land.py`, `ops/kiem_ho_so_land_test.py` đều ra `sensitive`). Căn cứ phân lớp của packet là nguồn (1) và (2); đừng đếm (3) là nguồn thứ ba độc lập. |
| `executor` · `reviewer` | Thân Issue #763 không ghi executor. Đề xuất Claude (cùng executor với #752); chủ kho chốt lúc cấp lease. Reviewer: Codex `cross_approved` hoặc `human_audited` (PROTOCOL §8 dòng 725–726: hết quota mà chưa có human thì pause). Lượt subagent Claude chỉ là lượt PHỤ, KHÔNG phải `review_deferred` (hàng chú thích ngay dưới). |
| `executor` · `reviewer` — chú thích | `review_deferred` (PROTOCOL dòng 612) KHÔNG dùng được cho packet này: dòng 705–707 cấm nó với workflow/security path, và hàng `review_class` ở trên đã xếp sổ là "workflow/CI authority". Lượt subagent Claude (cùng họ model với executor đề xuất) tối đa là `same_provider_approved`, một mình không thay `cross_approved` cho `sensitive` (dòng 696) — cách viết của `ops/specs/no-p3-lease-spec-hash-r3.md` (hàng `executor` · `reviewer`, cùng commit `11134f2`). |
| `base` | Số đo nền đo trên `c522c173cb58b506bac8cffb24239e16e8459836` theo chỉ thị. `git ls-remote --heads origin` lúc 23:29:24Z: `master` đã sang `9fddb1d` (merge PR #755; `git diff --stat c522c17 9fddb1d` chỉ có `ops/specs/wp728-do-linux-doc-lap-wp710-r2.md`, tệp sổ không đổi); bốn trạng thái của sổ chạy lại trên `9fddb1d` cho đầu ra y hệt (23:38:54Z–23:39:09Z). **Base của lease KHÔNG phải `c522c17`**: nó phải là head ĐÃ DUYỆT của #752 (bốn tệp: hai công cụ và hai test) dựng trên `master` sau khi #748 land, hoặc một nhánh tích hợp đã chứa nó (hàng `depends_on` (2)) — không phải "`master` cộng hai tệp test": đo 03:19Z 16-10-2026, một commit gồm `c522c17` + hai tệp test giả + hai mục `MOI`, KHÔNG có hai công cụ ⇒ `python3 -B .claude/dev/ci_dang_ky_test.py` rc 0, `ĐĂNG KÝ: 25/25`, `PHẢN CHỨNG: 1025/1025 đỏ đúng`, numstat `2 0` (C1 xanh) và `git cat-file -t <base>:<tệp test>` in `blob` cho cả hai (C5 đạt), trong khi `ops/kiem_ho_so_land.py` và `ops/kiem_nhan_hint.py` vắng (`git cat-file -t` rc 128; thông điệp phụ thuộc cây làm việc, xem C5) — C1 và C5 không phân biệt được base thiếu công cụ. Mọi số dưới đây ĐO LẠI trên base ấy lúc cấp, ghi số mới kèm lý do. |
| `depends_on` | **CHẶN cấp lease** cho tới khi ĐỦ năm điều kiện, đo lại lúc cấp; số trong ô này không thay được phép đo lúc cấp. **(1) #748 land vào `master`** — không chỉ vào `mission/748/integration` (lease `wp748-r11-g11-claude-windows-20261015` khai `target_branch_neu_land: mission/748/integration`). Tệp sổ thuộc write set #748: có trong 8 đường dẫn "Candidate write set" của thân Issue #748 (`gh api repos/ducthangho/tra-luat/issues/748 --jq .body`, đọc 23:27:59Z, Issue `open`) và trong 11 đường dẫn của lease r11 (nhánh `ops/wp748-r11-g11-lease` @ `181e3fb`, `lease_until 2026-10-16T04:27:21Z`). Hiện trạng 23:31:54Z: `ai-dang-giu .claude/dev/ci_dang_ky_test.py` (lệnh con của `ops/lease_publish.py`: `python3 ops/lease_publish.py ai-dang-giu <đường dẫn>`) ⇒ rc 11, `CÒN_HẠN wp748-r11-g11-claude-windows-20261015 refs/heads/ops/wp748-r11-g11-lease:ops/leases/wp748-r11-g11-claude-windows-20261015.yaml`, `NGƯỜI_GIỮ 1`, cùng 62 dòng `HẾT_HẠN` (r2 của #752 thấy rc 12 bia mộ một chiều r9→r10 lúc 08:54Z; nay lease r11 khai `thay_the_cho: wp748-r10-…` nên bộ quét ra rc 11). Phép đo của (1) là C4b: `ai-dang-giu` chỉ biết HẠN, không biết đã land, nên không thay được. **(2) Hai tệp test của #752 có trên base của #763.** Thân Issue #763 viết "#752 phải land trước, vì hai tệp test phải tồn tại trên master"; nhưng đo S1 (bảng "Số đo nền") cho thấy `master` chứa #752 mà thiếu hai mục `MOI` thì `gate-registry` ĐỎ. Theo đường A của #752 r3 (mục "Đường land"): base của #763 = head ĐÃ DUYỆT (exact SHA) của #752 dựng trên `master` sau #748, hoặc một nhánh tích hợp đã chứa nó; `master` nhận hai packet trong CÙNG MỘT lần merge. Chỗ lệch câu chữ Issue #763 đã được xử lý: chủ kho chọn đường A trong phiên điều phối `session_01CSM7GNazhN6uGJb4v1TqBT` ngày 2026-10-16 (lời khai trong phiên; neo bền là comment cấp lease của chủ kho, đo lại lúc cấp), và phiên điều phối đã sửa thân Issue #763 cho khớp đường A (land cùng một lần merge) — việc sửa thân Issue KHÔNG đo lại ở phiên vá này, đọc lại thân Issue lúc cấp. Đường B (gộp lại một packet có ngoại lệ trần) không chọn. **Đường A nối tiếp #763 trên #752 TRƯỚC khi #752 vào `master`**: base (cả hai nhánh trên) không phải tổ tiên `master` cho tới khi land (`is-ancestor` một head chưa land ⇒ rc 1, như C4b (1)). PROTOCOL §5 dòng 348 và ADR-0027 dòng 10 ("tránh stacked PR") đặt dependency chạy sau predecessor đã integrated; ADR-0044 dòng 15–17 chỉ cho nối tiếp khi slice sau mọc trên `mission/<issue>/integration` đã nhận slice trước, không trên một PR chưa merge, và dòng 21–22 đòi lease có `base_sha` không phải tổ tiên nhánh mặc định khai `xep_tang{tren_pr, thu_tu_land, ke_hoach_rebase}` (ADR chỉ nêu tên ba trường). Điều kiện cấp thêm: comment cấp lease (cùng chỗ neo đường A) ghi cách tuân — lease có `xep_tang`, hoặc ngoại lệ ADR-0027/0044 bằng chữ của chủ kho. Đo 03:37Z 16-10-2026 tại `c522c17`: `xep_tang` có đúng 1 tệp (ADR-0044), 0 trong 152 lease (tệp `ops/leases/*.yaml`; 4 tệp `.nhap` là bản nháp, không tính) trên `master`, 0 tệp mã cưỡng chế ⇒ cổng hiện KHÔNG chặn, người cấp tự đo; nếu lúc cấp cổng ấy đã có thì thiếu `xep_tang` ⇒ lease bị từ chối (ADR-0044 dòng 22). Kiểm lúc cấp: nửa đầu theo C4b (2); nửa sau theo C5 — `<base>^{commit}` đo được, rồi `ops/kiem_ho_so_land_test.py` và `ops/kiem_nhan_hint_test.py` đều là `blob` (rc 0 của `git cat-file -e` một mình chưa đủ). **(3)** Trên một clone ĐỦ ref — so `git ls-remote --heads origin` với `refs/remotes/origin/*` (bỏ `HEAD`) theo cặp (tên, OID): thiếu 0, thừa 0, lệch OID 0 (đo 23:30:23Z: 541/541/541, `comm -3` 0 dòng); `refs/heads/*` KHÔNG thuộc phép so — số giữa của `541/541/541` chỉ đếm nó — vì trên một `git clone` thường nó chỉ có nhánh mặc định và một commit cục bộ chưa đẩy làm nhánh cục bộ lệch OID, còn `refs/remotes/origin/*` vẫn thiếu 0, thừa 0, lệch 0 (đo 17-10-2026, git 2.43.0, máy chủ trần cục bộ nhiều nhánh); không chạy được ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp — `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ra `NGƯỜI_GIỮ 0`, rc 0; rc 12 là trạng thái thứ ba. Chốt `origin` là máy chủ GitHub: hàng ngay dưới. **(4) Anh em #751** (`no-p3-lease-spec-hash`): write set r2 của #751 (`ops/specs/no-p3-lease-spec-hash-r2.md` dòng 14) có `.claude/dev/ci_dang_ky_test.py` (+1 dòng `MOI`) và một test sống mới `ops/lease_publish_spec_hash_test.py` ⇒ hai lease KHÔNG đồng thời; bên land sau đo lại C1 vì cả hai số của `ĐĂNG KÝ` đổi. Sau khi tách, write set #752 r3 không giao #751 (đo ~23:37Z), nên quan hệ này thuộc #763. **(5) #748 đổi tệp sổ**: nhánh `agent/wp748-g9-claude` @ `0daeb47` đổi nó +65/−9 dòng so với merge-base với `c522c17` (đo 23:35:49Z); ở nhánh ấy `MOI` vẫn là ánh xạ (dòng 37) và dòng 52 vẫn là mục `ops/nhanh_don_duoc_test.py` (đo ~23:36Z). Write set #748 còn có `ops/nhanh_don_duoc_test.py` và `.claude/dev/doc_receipt_thu_hoi_test.py` — hai bộ đang có mục `MOI`. Lúc cấp: nếu `MOI` không còn là ánh xạ đường dẫn → mẫu regex, hoặc mẫu của mục `ops/nhanh_don_duoc_test.py` đổi, thì soạn revision mới trước khi cấp. |
| `depends_on` (3) — ghim máy chủ | Phép so (3) chỉ có nghĩa khi `origin` LÀ máy chủ GitHub: nếu `origin` là một bản sao cũ thì `ls-remote` và `for-each-ref` cùng mù và cùng khớp. Thêm vào (3): `git remote get-url origin` ra `https://github.com/ducthangho/tra-luat` (hoặc dạng có `.git`); khác ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp. Đo 01:50Z 16-10-2026 trên clone mà `origin` là bản sao cục bộ (1 nhánh): `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ rc 0, 24 dòng `HẾT_HẠN`, `NGƯỜI_GIỮ 0: không có` — trong khi máy chủ lúc 23:31:54Z 15-10 có `NGƯỜI_GIỮ 1` (ô `depends_on` (1) của chính đặc tả này). Phép so (3) KHÔNG phát hiện kho nông (hàng `moi_truong_do` (b)): đủ ref chưa đủ để đọc rc của `is-ancestor` (C4b). |
| `depends_on` — đính chính nguồn dẫn | (a) Ô (1) ghi ĐÚNG nguồn, giữ nguyên: "r2 của #752 thấy rc 12 bia mộ một chiều r9→r10 lúc 08:54Z" — phép đo ấy nằm ở `ops/specs/no-p3-cong-cu-ho-so-r2.md` dòng 15 (ngày 15-10-2026; tại `c522c17` `grep -c` "bia mộ một chiều": #752 r2 = 2 ở dòng 15 và 37, #751 r2 = 0). Review lượt 1 khai ô (1) viết "#751": đọc nhầm — đo 02:08:54Z 16-10-2026, `git show 11134f2:` tệp này có đúng 1 dòng chứa "bia mộ một chiều" (dòng 14 tại `11134f2`), và chuỗi ở đó là "r2 của #752 thấy rc 12". (b) Ô (4) dẫn #751 **r2** (`ops/specs/no-p3-lease-spec-hash-r2.md` dòng 14); revision hiện hành là **r3** (`ops/specs/no-p3-lease-spec-hash-r3.md`, cùng commit `11134f2`, `thay_the_cho` r2): `write_set` ở dòng 15, `depends_on` (4) ở dòng 16 — vẫn ba tệp, vẫn "+1 dòng `MOI`" (Mục tiêu 6), nên kết luận (hai lease KHÔNG đồng thời) không đổi; r3 còn nêu: nếu #763 land trước, đích của #751 thành `26/26`. |
| `write_set` | `.claude/dev/ci_dang_ky_test.py` (SỬA: +2 dòng vào `MOI`). |
| `kich_thuoc` | 1 tệp, 2 dòng thêm, 0 dòng xoá (đơn vị: dòng theo `git diff --numstat`) — ĐO, không ước: trạng thái S2 dưới đây cho numstat `2 0` (23:33Z trên `c522c17`). Trần ADR-0044 dòng 5 cho packet `sensitive` chạm authority: ≤ 3 tệp và ≤ 300 dòng thêm ⇒ dư 2 tệp, dư 298 dòng. Không cổng nào cưỡng chế trần: `grep -c` hai chuỗi `numstat` và `ADR-0044` trên `ops/lease_publish.py` và `.claude/dev/packet_loop.py` @ `c522c17` ra 0 cả bốn lần (23:36:35Z); quét rộng hơn hai tệp ấy (đo 16-10-2026 tại `c522c17`; mã sống = `*.py` `*.sh` `*.yml` `*.yaml` `*.ps1` `*.js` trừ `ops/specs`, `ops/reviews`, `ops/land`, `ops/leases`, `ops/evidence`): `git grep -l -I -e ADR-0044 -e 'ADR 0044' -e 0044-nguong` ra 1 tệp, `scripts/tl_selftest.py` (dòng 21867, chú thích đếm tài liệu, không phải cổng); `git grep -l -I -e numstat` ra 5 tệp (`.claude/hooks/pretooluse_guard.py` và test của nó: danh sách cờ git cho phép; `ops/chatgpt_review/build_bundle.py`: ghi `05_NUMSTAT.txt`; `ops/ci_duong_nhanh.py` và test của nó: nhận diện tệp nhị phân), không tệp nào so nó với ngưỡng ⇒ người giữ đo. Cần thêm tệp (ví dụ `ci.yml`, hay đổi trần thời gian vì hai test chạy lâu) ⇒ dừng, soạn revision. |
| `moi_truong_do` | Điều kiện môi trường của MỌI lệnh `git` và lệnh sổ trong tệp này (đo 17-10-2026, git 2.43.0); không đạt một điều kiện ⇒ phép đo ấy KHÔNG ĐO ĐƯỢC ⇒ không cấp. **(a)** Thư mục làm việc là gốc kho: đường dẫn tương đối và `git ls-tree -r` (không kèm `--full-tree`) tính từ đó; chạy từ thư mục con thì `git ls-tree -r` liệt kê ít mục hơn. **(b)** Kho KHÔNG nông — `git rev-parse --is-shallow-repository` ra `false` — trước khi đọc rc của `git merge-base --is-ancestor` (C4b): đó là câu hỏi LỊCH SỬ, khác câu hỏi ref ở `depends_on` (3) (CLAUDE.md, mục "ĐỌC BỘ ĐỆM CỤC BỘ", ý "Cắt độ sâu làm hỏng phép hỏi LỊCH SỬ"). Phản chứng chạy được, chỉ đổi độ nông: dựng một kho trần cục bộ có nhiều nhánh rồi `git clone` nó hai lần qua `file://` — một lần đủ, một lần `--depth=1 --no-single-branch` (hoặc `--depth=1` rồi `git fetch --depth=1 origin '+refs/heads/*:refs/remotes/origin/*'`) ⇒ phép so (tên, OID) của (3) giữa `git ls-remote --heads origin` và `refs/remotes/origin/*` cho `comm -3` 0 dòng ở CẢ HAI kho, nhưng `git merge-base --is-ancestor` một tổ tiên thật có commit trong kho (đỉnh của một nhánh khác) ra rc 0 ở kho đủ và rc 1 ở kho nông; sau `git fetch --unshallow` lại rc 0 (lệnh ấy chỉ chạy khi kho đang nông: trên kho đủ nó thoát rc 128). **(c)** Kho KHÔNG phải bản sao một phần (`git config --get remote.origin.promisor` rỗng), trừ khi máy chủ gọi được. Đo: dựng kho trần cục bộ và đặt `git config uploadpack.allowFilter true` trong đó (không đặt thì máy chủ bỏ bộ lọc: `git clone --filter` chỉ in một cảnh báo `filtering not recognized by server`, kho ra ĐỦ dù `remote.origin.promisor` là `true`, và sau khi xoá kho trần `git cat-file -t <base>:<tệp>` vẫn in `blob`), `git clone --filter=blob:none --no-checkout` nó qua `file://` (mọi vế trên đo qua `file://`; clone theo đường dẫn trần thì git bỏ bộ lọc, chỉ in cảnh báo `--filter is ignored in local clones; use file:// instead.`; kho ra ĐỦ và `git cat-file -t <base>:<tệp>` vẫn in `blob` sau khi xoá kho trần), rồi xoá kho trần ⇒ `git cat-file -e <base>^{commit}` rc 0 nhưng `git cat-file -t <base>:<tệp>` rc 128 dù tệp có trong base (khi máy chủ còn: in `blob` — đo vế này trên một bản clone KHÁC: `git cat-file -t` chạy khi máy chủ còn kéo blob về chính bản clone ấy, nên sau khi xoá kho trần nó ra `blob` rc 0 chứ không rc 128). Nguyên văn (sh, thư mục trống, `GIT_CONFIG_GLOBAL` trỏ tệp rỗng, `GIT_CONFIG_NOSYSTEM=1`): `git init -q -b main w; echo x > w/f; git -C w add f; git -C w -c user.name=a -c user.email=a@b commit -q -m c; git clone -q --bare w srv.git; git -C srv.git config uploadpack.allowFilter true; git clone -q --filter=blob:none --no-checkout file://$PWD/srv.git part; B=$(git -C part rev-parse origin/main); python3 -c "import shutil;shutil.rmtree('srv.git')"; git -C part cat-file -e $B^{commit}; echo rc=$?; git -C part cat-file -t $B:f; echo rc=$?` ⇒ in `rc=0` rồi `rc=128`. **(d)** Cây làm việc không có tệp `*_test.py` ngoài cây của base: sổ đếm chúng bằng `rglob` trên đĩa, nên một tệp thừa — chưa theo dõi hay bị bỏ qua (`info/exclude`) — ở gốc kho, trong `ops/`, trong một thư mục con của `ops/` khác `ops/reviews/`, trong `.claude/dev/`, `.claude/hooks/`, `scripts/`, `scripts/tl_core/` hay `docs/` làm S0 ra rc 1 với đúng một dòng `ĐỎ:`, còn tệp thừa dưới `ops/reviews/` (trực tiếp dưới nó, trong một thư mục con của nó, và cả khi bị `info/exclude`) thì S0 rc 0, 0 dòng `ĐỎ:`, vì `tim()` xếp chúng là hiện vật (đo trên `c522c17`, 17-10-2026); kiểm bằng `git status --porcelain --ignored` rỗng trên cây sạch TRƯỚC khi ghi tệp giả hay sửa tệp sổ — cây đã sửa tệp sổ (S2 chưa commit, M1, M1b, M2, đột biến của C2, C3) không rỗng theo định nghĩa: `git status --porcelain` in ` M .claude/dev/ci_dang_ky_test.py`. **(e)** Chỉ mã thoát và các dòng mà tiêu chí nêu tên là tiêu chí; thông điệp lỗi của git đổi theo loại cây làm việc (C5; đo git 2.43.0), còn ảnh hưởng của phiên bản git khác 2.43.0 và của ngôn ngữ KHÔNG ĐO ĐƯỢC ở container đo (chỉ có git 2.43.0 trên `PATH`; `locale -a` chỉ có `C`, `C.utf8`, `POSIX`; không cài bản dịch git nào). **(f)** Công cụ trên `PATH`: như mục "Số đo nền" (`python3` kèm PyYAML, `git`, `actionlint`); C1, C1b, C8 viết `python`: trên `PATH` chỉ có `python3` thì `python -B …` ra rc 127, nên dùng `python3` thay `python` (đo 17-10-2026, Python 3.11.15: cả ba chạy được bằng `python3`). |

## Số đo nền (`c522c17`; lặp trên `9fddb1d`, đầu ra y hệt)

Tệp sổ tại `c522c17`: 2236 dòng (`wc -l`), sha256 `a1d18f7dd8de529dc2b1b9b6cbac0578477c57d82075ff0bbe6cd2d7a94a8cb8`,
blob `0f8cabc80e6d5b18d59b0d46bb55123f00dd6e12`, commit chạm cuối `36190a3` (`2026-10-07T17:19:25Z`). Nạp mô-đun và
đếm (23:48:19Z): `MOI` 9 mục · `DA_NOI` 14 mục · `DANG_KY` 23 (= 9 + 14; đơn vị: đường dẫn test) · `MOI_WINDOWS` 1 ·
`CACH_LY` 0 · `NHE` và `MAU_DAY_DU` 3 mục mỗi bảng · `GIAY_TOI_DA_MOT_BO` 5400 (giây). Mẫu cần chép là giá trị của
mục `"ops/nhanh_don_duoc_test.py"` ở dòng 52: chuỗi thô, neo đầu và cuối dòng, hai nhóm số nguyên ngăn bởi `/`
(viết bằng lời, không chép chuỗi có dấu chéo ngược — CLAUDE.md, mục "TẦNG VẬN CHUYỂN CŨNG CHUẨN HOÁ CHUỖI").
`ruff check --select F --no-cache` trên tệp sổ: `All checks passed!`, rc 0 (ruff 0.15.8, 23:35:49Z).

Các trạng thái, đo trên clone tạm (ghi thử trong clone, khôi phục sau mỗi bước, `git status --porcelain` rỗng ở
cuối). Lệnh tĩnh: `python3 -B .claude/dev/ci_dang_ky_test.py` (không `--chay`; tiền điều kiện: `PATH` có `python3` kèm PyYAML, `git` và `actionlint` — vắng `actionlint` thì chính S0 ra rc 1, đúng một dòng `ĐỎ: ĐỘT BIẾN ĐỦ (#651 M4): KHÔNG ĐO ĐƯỢC: actionlint FileNotFoundError — fail-close`, `TỔNG: ĐỎ`, không dòng `PHẢN CHỨNG:`, nên số dòng `ĐỎ:` ở C1–C3 chỉ đếm được sau khi cài nó; đo 04:18Z 16-10-2026 trên `c522c17` với `PATH` thường trừ thư mục chứa `actionlint`; hook phiên và CI cài bản ghim 1.7.7 bằng `AL_VER=1.7.7 bash ops/cai_actionlint.sh` (thiếu `AL_VER` thì script thoát rc 2), còn `launcher.py doctor` xếp nó không bắt buộc nên `doctor` xanh chưa đủ). Hai tệp test giả in `1/1`, hai
công cụ giả rỗng. Mục `MOI` chèn bằng cách chép NGUYÊN dòng 52 rồi chỉ thay khoá. Đơn vị của `ĐĂNG KÝ: a/b`:
a = tệp test sống trên cây, b = mục trong sổ.
Quy ước đơn vị và ngày của tệp này: mọi mốc `hh:mm(:ss)Z` là UTC ngày 15-10-2026 trừ chỗ ghi ngày khác (đo 01:51Z 16-10-2026 trên bản tại `11134f2`: 27 trên 33 mốc không kèm ngày, tái lập ở review lượt 7 bằng quy tắc: không có `dd-mm-yyyy` hay `yyyy-mm-dd` trong 28 ký tự trước hoặc sau mốc); `do` = số mục `MOI`
bị `chay_moi` chấm ĐỎ (giá trị hàm trả về; đơn vị: mục); `541/541/541` (ô `depends_on` (3)) = số nhánh trên máy chủ / `refs/heads/*` / `refs/remotes/origin/*` (đơn vị: nhánh);
`MOI_WINDOWS` 1 và `CACH_LY` 0: đơn vị mục; `1025/1025`: đơn vị ca phản chứng của `phan_chung()`. `k dòng thêm tay` ở các mục "Vá sau review" = độ dài chính mục, từ dòng tiêu đề `## Vá sau review lượt N` đến dòng trống cuối mục, kể cả hai dòng ấy và mọi dòng trống ở giữa (đơn vị: dòng; đếm bằng lệnh `awk` ghi trong mỗi mục từ lượt 7 (đổi N cho các lượt trước); số dòng `>` của `diff` giữa bản trước vá đã áp HINT và bản sau KHÔNG phải định nghĩa — mục lượt 11 kèm bốn câu `awk` chèn vào các mục lượt 7–10 nên `diff` ra nhiều hơn k; đo 17-10-2026 tại `5bcf9b0` bằng `awk`: lượt 2 = 11, lượt 3 = 11, lượt 5 = 9, lượt 6 = 9; không kể dòng trống thì ra 8, 9, 7, 7). Quy tắc cho MỌI số đếm trong tệp này: có đủ ba phần — tập (kèm commit hoặc lệnh), quy tắc chọn, lệnh hoặc công thức; số đếm CHÍNH tệp này (số bản, số commit) hay một clone tạm của phiên review (số ref) KHÔNG ghi thành chữ số, vì đổi mỗi lần vá — chỉ ghi lệnh đo (`git log --format=%H -- <tệp>`, `git for-each-ref`); số nào không chống đỡ một quyết định hay một tiêu chí thì bỏ; số về hiện vật ngoài kho (VERDICT, HINT) đi kèm băm sha256 của hiện vật ấy — băm của bản ĐÃ TRAO cho lượt review kế, tính SAU khi lượt review đã trả kết quả; không băm bản còn nằm ở nơi reviewer làm việc, vì bản ấy có thể còn bị sửa sau khi băm. Câu "hai tệp KHÔNG có trong kho" ở các mục "Vá sau review" khẳng định đúng phạm vi phép đo ghi trong mục (các mục cây của commit nêu; mục cây = một dòng của `git ls-tree -r <commit>` không kèm `-t`, tức không tính thư mục); đo rộng hơn — băm mọi blob của kho (`git cat-file --batch-all-objects --batch`) — ra 0 trùng cho mọi băm VERDICT và HINT lượt 1–7 ghi trong tệp này (đo 16-10-2026 tại `692c661`).

| ID | trạng thái | giờ đo | kết quả |
|---|---|---|---|
| S0 | nền | 23:33:41Z | rc 0 · `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` |
| S1 | bốn tệp #752, không mục `MOI` | 23:33Z | rc 1 · `ĐỎ: test sống chưa đăng ký:` ×2 (hai tệp test) · `ĐĂNG KÝ: 25/23` · `TỔNG: ĐỎ` |
| S2 | bốn tệp + hai mục (đích của packet) | 23:33Z | rc 0 · 0 dòng `ĐỎ:` · `ĐĂNG KÝ: 25/25` · `PHẢN CHỨNG: 1025/1025 đỏ đúng` · `TỔNG: ĐẠT` · numstat `2 0` |
| S3 | hai mục, không có hai tệp test | 23:33Z | rc 1 · `ĐỎ: mục đăng ký không có tệp:` ×2 · `ĐĂNG KÝ: 23/25` · `TỔNG: ĐỎ` |
| M1 | đột biến: bỏ mục `ops/kiem_nhan_hint_test.py` | 23:33Z | rc 1 · `ĐỎ: test sống chưa đăng ký: ops/kiem_nhan_hint_test.py` · `ĐĂNG KÝ: 25/24` · `TỔNG: ĐỎ` · numstat `1 0` |
| M1b | đột biến: bỏ mục `ops/kiem_ho_so_land_test.py` | 23:42:14Z | rc 1 · `ĐỎ: test sống chưa đăng ký: ops/kiem_ho_so_land_test.py` · `ĐĂNG KÝ: 25/24` · `TỔNG: ĐỎ` |
| M2 | đột biến: mục thứ hai trỏ `ops/kiem_nhan_hint_tests.py` | 23:33:57Z | rc 1 · `ĐỎ: test sống chưa đăng ký: ops/kiem_nhan_hint_test.py` · `ĐỎ: mục đăng ký không có tệp: ops/kiem_nhan_hint_tests.py` · **`ĐĂNG KÝ: 25/25`** · `TỔNG: ĐỎ` |
| M3 | `chay_moi` thật, hai mục, test thứ hai in `0/0` · `3/4` · `1/1` | 23:34:57Z | `do = 1` · `do = 1` · `do = 0`; dòng log `CI_DANG_KY ops/kiem_nhan_hint_test.py: ĐỎ rc=0` ở hai ca đầu |
| M4 | `chay_moi` thật, mục đúng tên, mẫu thay bằng mẫu của `.claude/dev/gh_readback_test.py` | 23:37:29Z | mẫu đúng `do = 0`, `ĐẠT`; mẫu sai `do = 1`, `CI_DANG_KY ops/kiem_nhan_hint_test.py: ĐỎ rc=0` |

Bốn trạng thái S0–S3 và M1, M2 chạy lại trên `9fddb1d` 23:38:54Z–23:39:09Z: đầu ra y hệt. M2 là chỗ đáng nhớ: hai số
của `ĐĂNG KÝ` BẰNG NHAU mà cổng vẫn ĐỎ — một phép đo chỉ so `N/N` sẽ đọc nó thành xanh (CLAUDE.md, "MỘT BẤT BIẾN CÒN
ĐÚNG KHÔNG CHỨNG MINH CÁC SỐ HẠNG CÒN ĐÚNG").

## Mục tiêu

1. **[`.claude/dev/ci_dang_ky_test.py`]** Thêm đúng hai mục vào `MOI`, ngay sau mục `"ops/nhanh_don_duoc_test.py"`
   (dòng 52 tại `c522c17`; đo lại vị trí trên base thật; phép đo vị trí: C1b): khoá `"ops/kiem_ho_so_land_test.py"` và
   `"ops/kiem_nhan_hint_test.py"`, giá trị là NGUYÊN mẫu của mục `ops/nhanh_don_duoc_test.py` — chép byte từ chính dòng
   ấy rồi chỉ thay khoá, không gõ lại mẫu. Không đổi gì khác: `DA_NOI`, `MOI_WINDOWS`, `NHE`, `MAU_DAY_DU`, `CACH_LY`,
   `GIAY_TOI_DA_MOT_BO`, `kiem()`, `chay_moi()`, `bang_chung_xanh()`, `phan_chung()` giữ nguyên. Hệ quả phải nói thẳng:
   bước `test registry` (`--chay`) sẽ CHẠY hai test trong job `gate-registry` — Ubuntu ở mọi lượt; thêm Windows khi PR
   gắn nhãn `windows` hoặc gọi tay `workflow_dispatch` (đầu ra `os` của job `chuan-bi`, `ci.yml` dòng 50) — và đòi
   dòng đầu tiên khớp mẫu có hai số bằng nhau, lớn hơn 0; JSON thời gian (`loi_json_thoi_gian`) đòi một mục cho mỗi
   khoá `MOI`, tự khớp mà không cần sửa.
   Ba điều "hệ quả" chưa nói: (i) cùng lệnh `--chay` còn chạy ở `.github/workflows/ci-dot-bien-du.yml` dòng 64 (hằng tuần, cron `17 19 * * 6`,
   Ubuntu, `timeout-minutes: 105`) và ở `.claude/dev/chay-cong-windows.ps1` dòng 546 (cổng Windows chạy tay) — hai bộ mới chạy ở cả hai; (ii) gắn nhãn
   `windows` lên PR ĐANG MỞ không tự sinh lượt chạy: `ci.yml` dòng 13 khai `pull_request:` không `types:` (đo 01:51Z 16-10-2026: `on.pull_request` = `None`),
   nhãn chỉ có tác dụng ở lượt bắn kế tiếp — muốn có Windows trước merge thì `workflow_dispatch` trên ref ứng viên; (iii) sổ chỉ nhận bộ khi `rc == 0` VÀ
   dòng đầu tiên khớp mẫu có hai số bằng nhau, lớn hơn 0 (`ok = rc == 0 and any(bang_chung_xanh(...))` trong `chay_moi`).

## Nghiệm thu

- **C1 (xanh trên head của packet):** trên head #763 (base theo `depends_on` (2), cộng hai dòng):
  `python -B .claude/dev/ci_dang_ky_test.py` ⇒ rc 0, 0 dòng `ĐỎ:`, `ĐĂNG KÝ: a/a` với a = b0 + 2, trong đó b0 là số THỨ HAI của dòng
  `ĐĂNG KÝ: a0/b0` đo trên base thật TRƯỚC khi sửa (hai tệp test của #752 đã nằm trên cây nên a0 = b0 + 2: `25/23` ở S1, sau sửa `25/25` trên `c522c17`;
  đừng đọc a0 là "số đo nền": S0 `23/23` không đo lại được trên base thật vì cây đã có hai tệp test), `PHẢN CHỨNG: n/n đỏ đúng` (`1025/1025` trên `c522c17`), `TỔNG: ĐẠT`;
  `git diff --numstat -- .claude/dev/ci_dang_ky_test.py` so với base là `2 0`; `git diff --name-only` so với base đúng một đường
  dẫn. Đo: S2. ĐỎ khi: C2, C3; khi diff chạm thêm tệp; khi numstat khác `2 0`.
- **C1b (hai khoá nằm TRONG `MOI`, liền ngay sau khoá `nhanh`, mẫu bằng mẫu của `nhanh`):**
  `python -B -c "import runpy;m=runpy.run_path('.claude/dev/ci_dang_ky_test.py');M=m['MOI'];n=M['ops/nhanh_don_duoc_test.py'];k=('ops/kiem_ho_so_land_test.py','ops/kiem_nhan_hint_test.py');K=list(M);i=K.index('ops/nhanh_don_duoc_test.py');print(all(x in M and M[x]==n for x in k) and sorted(K[i+1:i+3])==sorted(k),len(M))"`
  ⇒ in `True N`, N = số khoá `MOI` ở base cộng 2 (`True 11` trên `c522c17`: 9 + 2). ĐỎ khi: (a) một khoá chỉ nằm trong `DANG_KY` mà không qua `MOI` — đo 01:50Z 16-10-2026:
  hai dòng `DANG_KY.add(...)` thay cho hai mục `MOI` ⇒ C1, C2, C3 đều XANH (rc 0, `25/25`, `1025/1025`, numstat `2 0`; gỡ từng dòng ⇒ `25/24` + một dòng `ĐỎ:`; đổi tên ⇒ `25/25` + hai dòng `ĐỎ:`),
  nhưng `len(MOI)` vẫn 9, `chay_moi()` mặc định không chạy hai bộ ấy, lệnh trên in `False 9`; (b) mẫu không bằng mẫu `nhanh` — đo cùng lượt: mẫu không neo `^`…`$` ⇒ C1–C4 đều XANH
  (M3: `0/0` và `3/4` vẫn ĐỎ), nhưng nhận cả dòng văn xuôi `xong 5/5 ca (ok)` mà mẫu `nhanh` từ chối (`do` 0 so với 1), lệnh trên in `False 11`; (c) hai khoá không liền ngay sau khoá `ops/nhanh_don_duoc_test.py` — đo 12:36Z–13:57Z 16-10-2026 trên `c522c17` + bốn tệp giả: hai mục đặt ở ĐẦU `MOI` (ngay sau dòng `MOI = {`) ⇒ C1 XANH (rc 0, `25/25`, `1025/1025`, numstat `2 0`) và lệnh C1b của bản trước (không kiểm vị trí) in `True 11`, lệnh nay in `False 11`; cũng `False 11` khi hai mục nằm giữa `MOI` hoặc một mục ở đầu một mục liền sau `nhanh`; đảo thứ tự hai mục mà vẫn liền sau `nhanh` ⇒ `True 11`. C4 phải lấy mẫu từ `MOI` của CHÍNH tệp
  executor (`chay_moi(moi={k: MOI[k] for k in hai_khoá})`, vắng khoá ⇒ KeyError ⇒ ĐỎ), không dựng từ điển tay; `--chay` đầy đủ chạy cả `ops/nhanh_don_duoc_test.py` (3306,45 s theo
  chú thích dòng 693 của sổ) nên không dùng làm phép đo nghiệm thu.
- **C2 (đột biến bỏ một mục ⇒ ĐỎ):** gỡ riêng từng mục trên bản sao tạm ⇒ rc 1, đúng một dòng
  `ĐỎ: test sống chưa đăng ký: <tệp vừa gỡ>`, `ĐĂNG KÝ: 25/24`, `TỔNG: ĐỎ` (M1, M1b); gỡ cả hai ⇒ S1. Phép đo nghiệm thu
  phải chạy CẢ HAI đột biến: một bản cài đặt chỉ thêm một mục qua được đột biến của mục kia.
- **C3 (đột biến trỏ tên tệp sai ⇒ ĐỎ):** một mục trỏ `ops/kiem_nhan_hint_tests.py` ⇒ rc 1, hai dòng `ĐỎ:`,
  `TỔNG: ĐỎ` (M2). Phép đo đọc rc, dòng `TỔNG:` VÀ đếm dòng `ĐỎ:` — không được chỉ so hai số của `ĐĂNG KÝ`, vì ở M2
  chúng bằng nhau (`25/25`). ĐỎ (tiêu chí hỏng) khi một bộ đo nghiệm thu chỉ đọc `ĐĂNG KÝ` mà báo M2 là xanh.
- **C4 (mẫu và dòng đầu ra, tầng `--chay`):** tầng tĩnh không đọc mẫu, nên đo bằng `chay_moi` thật, mẫu của hai ca "test thật" lấy từ `MOI` của tệp executor (C1b; `--chay` đầy đủ không dùng làm phép đo nghiệm thu):
  mục đúng tên mà mẫu bị thay bằng mẫu của một mục khác ⇒ `do = 1` (M4); test in `0/0` hoặc `3/4` ⇒ `do = 1` (M3);
  hai test thật của #752 ⇒ cả hai dòng `CI_DANG_KY …: ĐẠT`, `do = 0`. ĐỎ khi một trong hai test thật cho `ĐỎ`.
- **C4b (điều kiện cấp (1) và nửa đầu (2) — phép đo RIÊNG, `ai-dang-giu` không thay được):** (1) `git merge-base --is-ancestor <SHA merge land #748> origin/master` ⇒ rc 0
  (SHA = `merge_commit_sha` của PR land #748 đọc bằng GET, hoặc, khi đã ghi sổ, trong hồ sơ land `ops/land/*wp748*-land-evidence.yaml`:
  khoá `merge_commit` cấp 0 (chuỗi SHA; 25 trên 27 hồ sơ tại `c522c17`) hoặc `trang_thai_packet.merge_commit.sha` (2 trên 27, chỉ có dạng này — không có khoá `merge_commit` cấp 0 (`pr759-no-p3-ho-so` có cả hai dạng cùng SHA, nên 3 hồ sơ mang khoá lồng):
  `pr721-wp698`, `pr732-wp685`; đo 03:26Z 16-10-2026)); rc 1 ⇒ chưa land;
  rc ≥ 128 hoặc chưa có SHA ⇒ KHÔNG ĐO ĐƯỢC ⇒ không cấp. (2) `git merge-base --is-ancestor <SHA merge land #748> <base>` ⇒ rc 0 VÀ có verdict duyệt #752 neo `reviewed_sha` đúng SHA dùng làm
  base (hoặc SHA ấy là tổ tiên của `<base>` trên nhánh tích hợp). Lệnh cho vế sau: `git merge-base --is-ancestor <reviewed_sha> <base>` ⇒ rc 0. Nơi tra verdict: biên nhận `ops/reviews/*.receipt.yaml` (khoá `reviewed_sha`), quét trên MỌI ref của clone đủ ref ở (3) bằng `git grep -l -F -e <reviewed_sha> <ref> -- ops/reviews` cho từng ref rồi đọc khoá `reviewed_sha` của từng tệp trúng, không chỉ cây của `<base>` hay `origin/master`: biên nhận được ghi bằng commit SAU commit nó duyệt nên không nằm trong cây của chính `reviewed_sha` (đo 16-10-2026 tại `c522c17`: 0 trên 276 biên nhận có mặt trong cây của `reviewed_sha` của nó), và biên nhận ghi trên nhánh PR của #752 chưa ở `master` cho tới khi #752 land (C4b (1)); VÀ dòng `Reviewed commit:` trong comment của connector Codex trên PR của #752 (CLAUDE.md, mục "HỎI CHỖ TIỆN TAY", ý (b)); rỗng ở MỘT chỗ KHÔNG là "chưa duyệt", không thấy ở cả hai ⇒ KHÔNG ĐO ĐƯỢC ⇒ không cấp. "Duyệt" là assurance mà lớp của #752 đòi — `cross_approved` hoặc `human_audited` (PROTOCOL dòng 530 và 724–726) — không phải mọi biên nhận `verdict: approve`: đo 03:41Z 16-10-2026 trên 276 biên nhận tại `c522c17`, 80 có verdict thuộc nhóm duyệt (`approve`, `approved`, `approve_with_findings`) mà chỉ 29 mang `assurance: cross_approved`, 5 mang `review_deferred` (gồm `ops/reviews/no-p3-ho-so-exec-review-1-claude-verdict.receipt.yaml`, cùng họ `no-p3`), 2 mang `same_provider_*`; biên nhận kiểm toán người không mang khoá `assurance` mà mang `role: auditor` VÀ `assurance_dat: human_audited` (9 trên 9 biên nhận `role: auditor`; 0 trên 276 biên nhận mang `assurance: human_audited`; đo 16-10-2026 tại `c522c17`). Hai nơi tra không cùng loại: chỉ biên nhận mang `assurance`; dòng `Reviewed commit:` của connector chỉ cho biết đã có lượt review sạch ở SHA ấy (CLAUDE.md, ý (b)), không neo họ model đã phục vụ lượt chạy mà `cross_approved` đòi (PROTOCOL dòng 606) — chỉ thấy ở connector mà biên nhận chưa có ⇒ assurance KHÔNG ĐO ĐƯỢC ⇒ không cấp. Tra verdict có ba trạng thái, không hơn, trên tập các biên nhận có khoá `reviewed_sha` bằng SHA đang xét: thấy ít nhất một biên nhận có `verdict` thuộc nhóm duyệt và (`assurance: cross_approved`, hoặc `role: auditor` cùng `assurance_dat: human_audited`), VÀ không biên nhận nào khác trong tập có `verdict` ngoài nhóm duyệt ⇒ đạt; thấy biên nhận nhưng không đạt như trên (không biên nhận nào thoả điều kiện ấy; hoặc cùng `reviewed_sha` vừa có biên nhận thoả vừa có biên nhận `verdict` ngoài nhóm duyệt — đo 16-10-2026 tại `c522c17`: 2 trên 267 `reviewed_sha` khác nhau của 276 biên nhận, `efcf5757…` (`t33-doi-shellcheck-review-1` `approve`, `-review-2` `changes_requested`, cả hai `cross_approved`) và `472f11bd…` (`n5-lenh-hook-windows-review-1` `changes_requested`, `-review-2` `approve`, cả hai `cross_approved`), mà luật 'ít nhất một biên nhận thoả' cho cả hai ĐẠT) ⇒ không đạt; không thấy biên nhận nào, kể cả khi connector có dòng `Reviewed commit:` ⇒ KHÔNG ĐO ĐƯỢC; hai trạng thái sau đều ⇒ không cấp. Mỗi lệnh `is-ancestor` ở (1) và (2) có ba trạng thái: rc 0 có · rc 1 không · rc ≥ 128 KHÔNG ĐO ĐƯỢC — và chỉ đọc rc khi hàng `moi_truong_do` (b) đạt (kho nông ⇒ KHÔNG ĐO ĐƯỢC). Vì sao điều kiện (3) không thay được (1): `ai-dang-giu` chỉ biết HẠN (`_phan_loai_lease`: `HẾT_HẠN` khi `lease_expires_at_utc` đã qua) và bia mộ `da_bi_thay_the`,
  không biết packet đã land chưa — fixture đo 01:50Z 16-10-2026: lease trên nhánh CHƯA land vào `master`, đã hết hạn ⇒ `HẾT_HẠN`, `NGƯỜI_GIỮ 0: không có`, rc 0; cùng lease còn hạn ⇒ `NGƯỜI_GIỮ 1`, rc 11.
  Lease r11 của #748 hết hạn `2026-10-16T04:27:21Z` (ô `depends_on` (1)): sau mốc ấy (3) có thể ra rc 0 kể cả khi #748 chưa land. ĐỎ khi (1) hoặc (2) không rc 0.
- **C5 (thứ tự land):** trên một base THIẾU hai tệp test ⇒ S3 (`23/25`, rc 1) — đây là phép đo chứng minh #763 không
  được vào trước #752. Tiêu chí lúc cấp và lúc land: `git cat-file -e <base>^{commit}` rc 0 (đo được), rồi `git cat-file -t <base>:<tệp test>` in `blob` cho cả hai tệp (rc 0 của
  `git cat-file -e` chưa đủ: thư mục cũng rc 0); tệp vắng ⇒ rc 128 ⇒ ĐỎ; `<base>` không tồn tại cũng rc 128 (thông điệp KHÔNG ổn định, phụ thuộc cây làm việc: với SHA đủ 40 hex không tồn tại cũng như với tệp vắng khỏi base, git 2.43.0 in `path '<tệp>' does not exist in '<base>'` khi `<tệp>` KHÔNG có trên đĩa và `path '<tệp>' exists on disk, but not in '<base>'` khi `<tệp>` CÓ trên đĩa; với SHA rút gọn không tồn tại hoặc tên ref không tồn tại in `invalid object name` ở cả hai; đo lại 16-10-2026 tại `c522c17` trên cây có checkout, cây `--no-checkout` và kho `--bare`, mọi ca đều rc 128 — nên chạy `git cat-file -e <base>^{commit}` TRƯỚC và đừng phân biệt "vắng" với "base không tồn tại" bằng thông điệp) ⇒ KHÔNG ĐO ĐƯỢC, không phải "vắng". Hai nguyên nhân ấy chưa đủ: kho một phần mất kết nối cũng cho rc 128 dù tệp có trong base, nên rc 128 sau `git cat-file -e <base>^{commit}` rc 0 chỉ đọc là "vắng" khi hàng `moi_truong_do` (c) đạt.
- **C6 (CI thật):** `gate-registry` xanh trên head gộp (Ubuntu; thêm Windows nếu PR gắn nhãn `windows` hoặc
  `workflow_dispatch`): log bước `test registry` có `CI_DANG_KY ops/kiem_ho_so_land_test.py: ĐẠT`,
  `CI_DANG_KY ops/kiem_nhan_hint_test.py: ĐẠT`, `CI_DANG_KY_THOI_GIAN` có một mục cho mỗi khoá `MOI` (11 nếu base thật
  vẫn 9 mục như `c522c17`), và `TỔNG: ĐẠT`. ĐỎ khi một trong hai dòng là `ĐỎ` hoặc vắng. KHÔNG ĐO ĐƯỢC ngoài GitHub
  Actions; ghi run id và kết luận từng job lúc thi hành. Cổng xanh toàn phần: `ops/specs/no-p3-cong-cu-ho-so-r3.md` B6 (d)
  giao việc đo nó trên head gộp cho C1, C6 và C8 của spec này, nhưng ba tiêu chí chỉ phủ `gate-registry` và một bước của
  `gate-ops` (`ci-duong-nhanh selftest`); nên đặt ở đây: MỌI job của `ci.yml` xanh trên cùng head gộp (bảy job tại `c522c17`,
  đo 03:21Z 16-10-2026: `chuan-bi`, `gate`, `gate-cong-cu`, `gate-cong-cu-gop`, `gate-ops`, `gate-registry`,
  `gate-packet-loop`; đo lại trên base thật vì #748 sửa `ci.yml`). ĐỎ khi một job không xanh (job đã đỏ sẵn trên `master`
  thì ghi "đỏ sẵn, delta = 0" kèm run id của `master`); nếu job đỏ không phải `gate-registry` hay `gate-ops` thì spec này
  chưa dự kiến nguyên nhân ⇒ dừng, soạn revision.
- **C7 (ruff):** `ruff check --select F` trên tệp sổ: delta 0 (multiset) so với base (`All checks passed!` trên
  `c522c17`); ghi phiên bản (container soạn spec có binary 0.15.8, `python3 -m ruff` không có module; CI ghim
  0.15.15). ĐỎ khi chèn một import thừa ⇒ `F401`, rc 1 (đo 23:42:14Z trên bản sao ngoài kho: thêm `import fractions`
  ⇒ `F401`, `Found 1 error.`, rc 1).
- **C8 (người tiêu thụ thứ hai của sổ — job `gate-ops`):** `python -B ops/ci_duong_nhanh_test.py` trên head ⇒ rc 0, `CA: 104/104`, `DOT BIEN: 383/383`, `TONG: DAT`
  (S2; đo 01:32Z–01:37Z 16-10-2026 trên `c522c17` + bốn tệp giả + hai mục `MOI`; ca `k01_so_dang_ky_nhan_muc_da_noi` chạy `kiem()` của sổ trên cây; đơn vị: ca · đột biến;
  số đổi sau #748 vì `ops/ci_duong_nhanh_test.py` thuộc write set #748 — đo lại). ĐỎ khi S1 hoặc S3: `CA: 103/104`, `DOT BIEN: 382/383`, `TONG: DO`, rc 1 (đo cùng lượt) — tức hai trạng thái ấy
  làm đỏ CẢ `gate-registry` LẪN `gate-ops`. Bản `a2069ac` của `ops/specs/no-p3-cong-cu-ho-so-r3.md` (mục "Đường land" A chỉ nêu
  `gate-registry`; B6 (d) "mọi job khác xanh") bỏ sót `gate-ops`; `b6ab45e` đã sửa và bản nay khớp C8 (đo 03:20Z 16-10-2026:
  chuỗi "mọi job khác xanh" còn 1 dòng ở `a2069ac`, 0 dòng ở `b6ab45e` và `5bd6d03`).

## Ngoài phạm vi (cố ý)

- Nội dung hai test và hai công cụ — packet #752.
- `.github/workflows/ci.yml` (thuộc write set #748); gắn hai công cụ (không phải hai test) vào CI — nợ cho packet sau.
- `MOI_WINDOWS` (mẫu chung đủ cho cả hai nền, như mục `ops/nhanh_don_duoc_test.py` hiện có), `NHE`/`MAU_DAY_DU` (hai
  test không có chế độ nhẹ), `GIAY_TOI_DA_MOT_BO`.
- Thêm phản chứng riêng vào `phan_chung()` cho hai mục: `kiem()` kiểm chung mọi mục, và C2/C3 đo bằng đột biến trên bản
  sao tạm; thêm phản chứng sẽ đổi số `1025` và kéo thêm dòng ngoài hai dòng của write set.
- Đăng ký test của #751 (`ops/lease_publish_spec_hash_test.py`) — thuộc #751.

## Hình dạng kế thừa

`khong_ap_dung` (không phải packet khắc phục; tách từ #752 r2, chưa có hồ sơ thi hành tiền nhiệm). Hình dạng cần canh,
đo được ngay ở đây: **một quan hệ đúng trông như các số hạng đúng** — M2 cho `ĐĂNG KÝ: 25/25` mà cổng ĐỎ (C3).

## Chưa đo được

- Thân Issue #763 hiện còn ghi "#752 phải land trước" hay đã sửa theo đường A (land cùng một lần merge): phiên điều phối báo đã sửa, phiên vá này chưa đọc lại thân Issue (`depends_on` (2)); neo bền của đường A là comment cấp lease của chủ kho, chưa có lúc soạn.
- Executor của packet (Issue không ghi).
- CI thật (C6), `ci_dang_ky_test.py --chay` đầy đủ, đường Windows; thời lượng hai test cộng thêm vào `test registry`
  (hai test chưa tồn tại; trần job 105 phút, trần một bộ `GIAY_TOI_DA_MOT_BO` 5400 giây) — đo khi có.
- Danh sách required check của `master`: `gh api …/branches/master/protection/required_status_checks` trả HTTP 403
  `Resource not accessible by integration`.
- Hình dạng tệp sổ sau khi #748 land (nhánh `0daeb47` mới là bản thi hành r9; lease r11 chưa có head thi hành nào trên
  máy chủ lúc 23:29:24Z) — `depends_on` (5) đo lại.
- `gate-ops` (C8): phiên vá KHÔNG đo lại; số trong C8 là của review lượt 1.
- Lời khai về quyết định, phân hạng hay lời của chủ kho — MỌI câu có chữ "chủ kho" trong các mục "Vá sau review lượt N", kể cả mục chưa viết: neo là phiên điều phối `session_01CSM7GNazhN6uGJb4v1TqBT` (lời khai trong phiên), chưa có id comment của chủ kho.
- Lời khai về Issue, lease và nhánh ngoài kho. (a) "chưa lease nào neo đặc tả này" (mục lượt 1): đo 16-10-2026, `git grep -l -F` băm sha256 của MỌI bản của tệp này tính đến `692c661` (`git log --format=%H 692c661 -- ops/specs/no-p3-dang-ky-ci-r1.md`; mỗi bản `git show <commit>:ops/specs/no-p3-dang-ky-ci-r1.md | sha256sum`), `no-p3-dang-ky-ci`, `issues/763` và `#763` trong `ops/leases` của từng ref ra 0 trên mọi ref (`git for-each-ref`) của MỘT clone cục bộ do phiên review dựng — số ref của clone khác sẽ khác nên không ghi ở đây; máy chủ có 541 nhánh lúc 23:30:23Z 15-10 ⇒ phần clone ấy chưa phủ KHÔNG ĐO ĐƯỢC; bản sau `692c661` (kể cả bản neo vào lease) đo lại lúc cấp lease.
  (b) "`.github/workflows/ci.yml` và `ops/ci_duong_nhanh_test.py` thuộc write set #748" (mục "Ngoài phạm vi", C6, C8): đối chiếu một phần — bản thi hành r9 `0daeb47` đổi cả hai tệp (đo 16-10-2026: `git diff --name-only $(git merge-base c522c17 0daeb47) 0daeb47`); write set của lease r11 trên máy chủ KHÔNG ĐO ĐƯỢC.

## Vá sau review lượt 1

Nguồn: verdict `changes_requested` lượt 1 (`reviewed_sha` `11134f2`, `spec_sha256` `9791add6…c031d`; 0 P1 · 2 P2 · 9 P3; VERDICT sha256 `864586fb0177ea1ba549ce6a40150928ad87b757cbea4fbb954de203051bfa5a`, HINT sha256 `db479a3beb2bfb75525732e1e571cce6119ff1fb9cee9236e3df0b9edd44fe78`; hai tệp KHÔNG có trong kho — thứ định danh là băm),
kèm `HINT.patch` 11 hunk — áp bằng `patch -p0 --fuzz=0` (rc 0, 11/11 hunk), rồi chỉnh tay những chỗ ghi dưới. Lượt ấy do
subagent Claude chạy (cùng nhà cung cấp với executor đề xuất) nên không thay review chéo mà lớp `sensitive` đòi. Sửa tại
chỗ, không tăng `revision`: chưa lease nào neo đặc tả này.

| lớp | hạng | chỗ sửa |
|---|---|---|
| `muc-tieu-1-khong-co-phep-do-khoa-trong-moi-va-nguyen-mau` | P2 | C1b mới; C4 lấy mẫu từ `MOI` của tệp executor |
| `depends-on-1-khong-co-phep-do-land-748` | P2 | C4b mới; ô `depends_on` (1) và (2) trỏ C4b |
| `c1-a-nen-cong-2-khong-xac-dinh` | P3 | C1: a = b0 + 2 |
| `depends-on-3-origin-chua-ghim-may-chu` | P3 | hàng `depends_on` (3) — ghim máy chủ, dời xuống ngay sau hàng `depends_on` (HINT đặt nó trước); ô (3) trỏ xuống |
| `depends-on-dan-nham-r2-751-va-rc12` | P3 | hàng đính chính nguồn dẫn: vế (b) NHẬN; vế (a) BÁC — ô (1) vốn ghi "#752", bằng chứng ngay trong hàng |
| `gate-ops-cung-do-o-s1-s3-khong-nhac` | P3 | C8 mới |
| `muc-tieu-1-he-qua-chay-thieu-noi-goi-nhan-windows-va-rc` | P3 | Mục tiêu 1, đoạn "Ba điều hệ quả chưa nói" |
| `review-class-nguon-3-khong-co-rang` | P3 | hàng chú thích nguồn (3); hàng `review_class` đổi "Ba nguồn" thành hai nguồn cộng một phép gọi cổng |
| `reviewer-review-deferred-trai-dong-705` | P3 | hàng chú thích `executor` · `reviewer`; gỡ câu "chỉ là `review_deferred`" ở hàng chính |
| `c5-cat-file-gop-ba-trang-thai` | P3 | C5; ô `depends_on` (2) trỏ C5 |
| `l1-l5-don-vi-do-va-ngay-gio-do-con-thieu` | P3 | đoạn quy ước đơn vị và ngày, ngay sau định nghĩa `ĐĂNG KÝ: a/b` |

Phiên vá đo lại hai P2 (02:07:22Z–02:08:54Z 16-10-2026, clone tạm `c522c17` dựng từ chính kho, chạy kịch bản của
reviewer; D = hai dòng `DANG_KY.add(...)` thay cho hai mục `MOI` (C1b a), E = hai mục `MOI` mang mẫu không neo `^`…`$` (C1b b)):
lệnh C1b trên S0 / S2 / D / E ⇒ `False 9` / `True 11` / `False 9` / `False 11`; D và E vẫn qua C1–C3 (rc 0,
`25/25`, `1025/1025`, numstat `2 0`); fixture `ai-dang-giu` trên nhánh chưa land: lease hết hạn ⇒ rc 0, `NGƯỜI_GIỮ 0`,
còn hạn ⇒ rc 11; `git merge-base --is-ancestor`: tổ tiên rc 0, không phải tổ tiên rc 1, SHA không tồn tại rc 128.

## Vá sau review lượt 2

Review lượt 2 (`approve`, 0 P1 · 0 P2 · 2 P3; VERDICT sha256 `324ee24773ea529295203efc3d2017d76899e4f63abcc4b14b485fa4f177159c`,
HINT sha256 `877791dfb5ca16536e720b8caa33c002a405beeccf4d08d625e24ee187f309f1`). Áp NGUYÊN VĂN 2 hunk của HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (11 dòng thêm tay).

| lớp | hạng | chỗ sửa |
|---|---|---|
| `c4b-2-verdict-duyet-khong-co-noi-tra` | P3 | C4b (2): nêu lệnh, nơi tra verdict duyệt #752 và trạng thái khi không thấy |
| `va-nhan-d-e-khong-dinh-nghia` | P3 | mục "Vá sau review lượt 1": định nghĩa nhãn D, E |

## Vá sau review lượt 3

Bản trước vá: commit `5bd6d03`, sha256 `b1e320a35a06d6d3d22febc432d64c1053f74193e24ef7074f2614595a2eb1b7` (diff của lượt 3 tái lập từ kho bằng `git diff --numstat 5bd6d03 64cad00 -- ops/specs/no-p3-dang-ky-ci-r1.md` = 27 dòng thêm · 6 dòng xoá, đo 16-10-2026; `64cad00` là commit thêm mục này). Review lượt 3 (`approve`,
0 P1 · 0 P2 · 6 P3; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, `reviewed_sha`
`5bd6d0358ab48baed41a9b9d05cbae9a863a74e7`; VERDICT sha256 `3fb414bfc05a5363ea6d4fbed9a3e827d11aa373e77280c670aba2086c558ffc`,
HINT sha256 `e21941e2f1a05e699d18e1a20ce5867cedecdc58b1b61e66bd786a7a06baa508`). Áp NGUYÊN VĂN 5 hunk của HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (11 dòng thêm tay). Sáu lớp: `c8-dan-b6d-r3-752-da-sua-o-b6ab45e` ·
`base-chi-hai-tep-test-lech-head-da-duyet` · `depends-on-2-duong-a-thieu-xep-tang-adr-0044` ·
`c4b-1-khoa-merge-commit-hai-hinh-dang` · `c4b-2-verdict-duyet-khong-neu-assurance` ·
`c6-cong-xanh-toan-phan-752-giao-nhung-khong-do` — chỗ sửa xem từng hunk (dòng `# lop:` trong HINT).

## Vá sau review lượt 4

Bản trước vá: commit `bedcf2f`, sha256 `03defb2b5463ad1f60008500aa57c47cb6ec037776fcf6bd76576e272d71f0d8`. Review lượt 4 (reviewer Claude Sonnet 5.5 subagent
`review-sonnet-max`, `reviewed_sha` `64cad009c42a7a5f5722caa162f7dc120dd9c6d4`; VERDICT sha256 `5e5b79d56ce08422f1ecd87fa9850c480683935d9825a3d65785ba0531d79bdc`, HINT sha256 `4e8bc86a9cf59eaf3690fca1ae19478f81a7654956e681938f0ef2004941b670`;
hai tệp KHÔNG có trong kho — đo 16-10-2026 ở `62924ff`: 0 trên 3520 blob của cây có sha256 bằng một trong hai băm này, và chỉ chính đặc tả này nhắc tới chúng; thứ định danh là băm). Áp NGUYÊN VĂN HINT (`patch -p0 --fuzz=0`, rc 0); không sửa nội
dung nào ngoài HINT và mục này. Ba lớp (`approve`, 0 P1 · 0 P2 · 3 P3): `so-tinh-tien-dieu-kien-actionlint-chua-neu` · `c4b-2-connector-mot-minh-khong-chung-minh-assurance` · `va-luot-3-dan-hien-vat-ngoai-kho-khong-bam`. Vòng vá P3 thêm thứ 1/2 chủ kho cho (16-10).

## Vá sau review lượt 5

Bản trước vá: commit `0cfe253`, sha256 `2a5b408cf8d6debee01df5a7626575fca146f25a04e1d94be8bd0f57a284d7b2` (`git show 0cfe253:ops/specs/no-p3-dang-ky-ci-r1.md` ra đúng băm này).
Review lượt 5 (`approve, 0 P1 · 0 P2 · 3 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `62924ffa23cc2dfc2f0648dd002ba0abba3f11f6`; VERDICT sha256 `d1846914e0aaf46d38fec68ec7b7b6d3e0f6c75480af49a6692b20cdf91337ef`, HINT sha256 `d8692dd5eacc28da196f1c537fdf740651ef0509ef3aa1b7c3c607a99aeeb514`; hai tệp KHÔNG có trong kho — đo 2026-10-16 ở
`0cfe253`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay: `git diff --numstat 0cfe253 e5698ca -- ops/specs/no-p3-dang-ky-ci-r1.md` = 15 dòng thêm · 6 dòng xoá = HINT 6 · 6 (6 hunk, mỗi hunk thay một dòng) + mục này 9 · 0; `e5698ca` là commit thêm mục này). 3 lớp:
`c4b-2-dong-lop-bang-chung-duong-va-pham-vi-quet` · `muc-va-dan-hien-vat-bang-vi-tri-va-phu-dinh-tong-quat` · `va-luot-4-danh-sach-lop-4-muc-cho-3-lop`.

## Vá sau review lượt 6

Bản trước vá: commit `a870bff`, sha256 `6119a3b9ac2f69b82f157bc0281fe95c9c76344a5bf4d433b4f4fe8fbd72431f` (`git show a870bff:ops/specs/no-p3-dang-ky-ci-r1.md` ra đúng băm này).
Review lượt 6 (`approve, 0 P1 · 0 P2 · 3 P3; chủ kho đọc chặt: lời khai sai đo được là P2`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `e5698ca3b3d8b505789bcc76a926213f594e5541`; VERDICT sha256 `db282773bde91b3b25704e34ab6b6eb508a955ff5fc1044c31197bc69c92191d`, HINT sha256 `5ff3046e0474dbbd1cfe2e96b2b168c025af8b7829eb26db41f5db5b8b3619b0`; hai tệp KHÔNG có trong kho — đo 2026-10-16 ở
`a870bff`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay). 3 lớp:
`c4b-2-bien-nhan-cung-sha-mau-thuan-verdict` · `muc-tieu-1-vi-tri-ngay-sau-khong-co-phep-do` · `muc-va-luot-5-so-dong-them-tay-khai-8-do-duoc-9`.

## Vá sau review lượt 7

Bản trước vá: commit `5bcf9b0`, sha256 `bb6a1c643fc4e5bd418e5d817abd124bbfab0cfabd7b3e478d2542eecc1bbedf` (`git show 5bcf9b0:ops/specs/no-p3-dang-ky-ci-r1.md` ra đúng băm này).
Review lượt 7 (`approve, 0 P1 · 0 P2 · 2 P3; chủ kho xếp lớp so-dem-thieu-quy-tac-dem thành P2`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `5bcf9b0387c156789129f95fbf3504b77ed88209`; VERDICT sha256 `2ff50ab9ac80c459ba8f8d35f6d9afc505bad6186e955fcdbe8321aeb9963495`, HINT sha256 `0b382122ef0aa1fd30803b8955b1f6e8735150fbc41b1e48ad6469c84f62f13a`; hai tệp KHÔNG có trong kho — đo 2026-10-16 ở
`5bcf9b0`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 7")} f' <tệp spec> | wc -l` ra `9`). 2 lớp:
`loi-khai-rong-hon-hoac-ngoai-phep-do` · `so-dem-thieu-quy-tac-dem`.

## Vá sau review lượt 8

Bản trước vá: commit `692c661`, sha256 `1646f2facc0166e53e274551c7b33b91f6b7547fc7a59d9685def069c03803b1` (`git show 692c661:ops/specs/no-p3-dang-ky-ci-r1.md` ra đúng băm này).
Review lượt 8 (`changes_requested, 0 P1 · 1 P2 · 3 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `692c6610f9f732657da92e86c213384abca1c867`; VERDICT sha256 `9e765885f1716b753bdfd95012ac8d5cd8e7f8f09793b77f59a1850264713b31`, HINT sha256 `3643dd39d30bb65cdeca0d633fdbbaae539563c2e219c70a032cbaca20f2cdc5`; hai tệp KHÔNG có trong kho — đo 2026-10-16 ở
`692c661`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 8")} f' <tệp spec> | wc -l` ra `9`). 4 lớp:
`c5-thong-diep-git-chi-dung-voi-sha-day-du` · `loi-khai-rong-hon-hoac-ngoai-phep-do` · `so-dem-thieu-quy-tac-dem` · `va-luot-1-hien-vat-ngoai-kho-khong-bam`.

## Vá sau review lượt 9

Bản trước vá: commit `8699d09`, sha256 `3b177ec7450e1705359cf59e8ba598cc8f9b50cf0b281867462e9945f1f06ef4` (`git show 8699d09:ops/specs/no-p3-dang-ky-ci-r1.md` ra đúng băm này).
Review lượt 9 (`changes_requested, 0 P1 · 2 P2 · 1 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `8699d09d4ad5a970553356b89ab65f25fdc7602b`; VERDICT sha256 `2be9fac6cd096f77ca3a01e4151d65a6a246c116be95680fae7555cff3b2626a`, HINT sha256 `710b4714e863b2f11626cac020cea9baca3c17c2d6e45fc848985da1e97d3483`; hai tệp KHÔNG có trong kho — đo 2026-10-17 ở
`8699d09`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 9")} f' <tệp spec> | wc -l` ra `9`). 3 lớp:
`c5-thong-diep-git-con-phu-thuoc-cay-lam-viec` · `muc-cay-don-vi-khong-neu-lenh` · `va-luot-8-bam-verdict-khong-khop-hien-vat`.

## Vá sau review lượt 10

Bản trước vá: commit `7f86e09`, sha256 `26bfda8846e90405b6a0d019c366a9460ba7c21699c7906315a1f10160f2de0b` (`git show 7f86e09:ops/specs/no-p3-dang-ky-ci-r1.md` ra đúng băm này).
Review lượt 10 (`changes_requested, 0 P1 · 1 P2 · 0 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `3976c403696f5411c0ab20a3f7f4b7fd0101a775`; VERDICT sha256 `4764dc5444c39880f6da5ca3de50dab9a078faf49c31a4bf21d5cec4ccdc7b3f`, HINT sha256 `6f8d055d0f8cd0ed1a8cc63ba79260c52409ca8544183ad8b9456e12f2e0dac0`; hai tệp KHÔNG có trong kho — đo 2026-10-17 ở
`7f86e09`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 10")} f' <tệp spec> | wc -l` ra `9`). 1 lớp:
`rc-phu-dinh-sai-tren-kho-nong-va-kho-mot-phan`.

## Vá sau review lượt 11

Bản trước vá: commit `fe890c0`, sha256 `a8761e16f929c568ee6eb7c447af2d20785f0f8c6710d12d8c019b41d9abc569` (`git show fe890c0:ops/specs/no-p3-dang-ky-ci-r1.md` ra đúng băm này).
Review lượt 11 (`changes_requested, 0 P1 · 2 P2 · 5 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `94e4ec25815b7fec4e5533c8c94ab3dbd8ca305a`; VERDICT sha256 `58073482b34cf178bc3a2c0bb0c55d5fae715e7f9f3e69280b963e60b02687f7`, HINT sha256 `b5dfac39820d64a3c50a793539f8eb4c8edc039e420981e297ce3a915ff0047c`; hai tệp KHÔNG có trong kho — đo 2026-10-17 ở
`fe890c0`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT, chính mục này và câu đếm `awk` chèn vào bốn mục lượt 7–10 (mỗi mục một câu, số đếm của chúng giữ nguyên `9`) (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 11")} f' <tệp spec> | wc -l` ra `9`). 7 lớp:
`moi-truong-do-c-phan-chung-thieu-uploadpack-allowfilter` · `moi-truong-do-d-mot-tep-thua-rc-1-rong-hon-phep-do` · `depends-on-3-doc-chu-refs-heads-va-remotes-hai-nghia` · `moi-truong-do-d-kiem-status-rong-khong-ap-dung-cay-da-sua` · `moi-truong-do-e-doi-theo-phien-ban-khong-do-duoc` · `ai-dang-giu-chua-neu-chuong-trinh-chua-lenh` · `moi-truong-do-f-python-va-python3-lech-ten-o-c1-c1b-c8`.

## Vá sau review lượt 12

Bản trước vá: commit `0ebcb89`, sha256 `7a2e20794a2248b25e60fc0fee31e49c6d2b592f6d6ee9890d5cdc95744f49f8` (`git show 0ebcb89:ops/specs/no-p3-dang-ky-ci-r1.md` ra đúng băm này).
Review lượt 12 (`changes_requested, 0 P1 · 2 P2 · 0 P3`; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, tự khai, KHÔNG phải Codex;
`reviewed_sha` `f0632bbb428328d16f070c8718d8f9f58848f182`; VERDICT sha256 `0df9b754bcb3d5c7f775ef1b7458e8ec62c806dac72efb0eb6a34d3cd032bbb1`, HINT sha256 `69744790ab4b21b3965db6a70f0a77ad63f2de42967f06af145179c0e383f782`; hai tệp KHÔNG có trong kho — đo 2026-10-17 ở
`0ebcb89`: 0 trên 3520 mục cây có sha256 bằng một trong hai băm này; thứ định danh là băm). Áp NGUYÊN VĂN HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT và chính mục này (9 dòng thêm tay = chính mục này, từ tiêu đề tới hết dòng trống cuối; đếm: `awk '/^## /{f=($0=="## Vá sau review lượt 12")} f' <tệp spec> | wc -l` ra `9`). 2 lớp:
`moi-truong-do-c-phan-chung-thieu-giao-thuc-file-va-thu-tu-do` · `muc-va-luot-11-dong-them-tay-khai-9-diff-do-duoc-13`.

