# Đặc tả packet `no-p3-dang-ky-ci` r1 — đăng ký hai bộ test của #752 vào sổ test sống

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-dang-ky-ci` |
| `packet_issue` | #763 — https://github.com/ducthangho/tra-luat/issues/763 ("Packet NO-P3-DANG-KY-CI: đăng ký hai bộ test của #752 vào ci_dang_ky_test.py", `open`, mở bởi `ducthangho` `2026-10-15T23:26:04Z`; đọc qua `gh api repos/ducthangho/tra-luat/issues/763` ~23:27Z 15-10-2026). |
| `revision` | 1 |
| `thay_the_cho` | Không có revision trước. Nội dung TÁCH từ mục tiêu 5 và B6(a) của `ops/specs/no-p3-cong-cu-ho-so-r2.md` (#752 r2, sha256 `ce39f1e164fd94e342af59a0624cec1fc23fc84574f0ec1e5c627a656a17593b`, commit `a9ef33c`); r2 ấy đóng băng, không sửa. Bản anh em cùng lượt: `ops/specs/no-p3-cong-cu-ho-so-r3.md` (#752 r3). |
| `nguon_cap_viec` | Quyết định chủ kho 15-10-2026 **"tách 2 packet"** (chuyển tới qua phiên điều phối; thân Issue #763 ghi lý do, phạm vi, phụ thuộc và tên tệp đặc tả này). Lý do tách: finding P2 của connector Codex trên PR #762, `pull/762#discussion_r4286041896` ("Apply the sensitive packet size ceiling", `created_at 2026-10-15T17:13:10Z`) — sửa sổ test sống là đổi CI/gate authority nên #752 r2 (5 tệp, ~900 dòng) vượt trần `sensitive` 3 tệp/300 dòng. Nợ `SPEC-R2-751-752-KHONG-DUOC-CAP-LEASE` (`ops/land/pr759-no-p3-ho-so-land-evidence.yaml` dòng 407, `trang_thai: mo`). Hai test được đăng ký là mục tiêu 2 và 4 của #752 r3. |
| ngưỡng chặn | Theo bảng PROTOCOL §8 dòng 621 cho lớp `sensitive`: không còn P0; cần approval tường minh đúng assurance và quyết định có căn cứ cho từng finding còn mở. Ngưỡng "chỉ P1/P2 chặn" của #752 không tự áp sang #763 — chưa có nguồn thẩm quyền riêng cho #763 (KHÔNG ĐO ĐƯỢC). |
| `review_class` | **`sensitive`** · `effective_review_class`: **`sensitive`**. Hai nguồn độc lập khớp nhau, cộng một phép gọi cổng chỉ chứng minh cổng fail-closed (hàng chú thích ngay dưới): (1) thân Issue #763 "Lớp sensitive"; (2) PROTOCOL §8 dòng 724 xếp "workflow/CI authority" vào `sensitive` — sổ này quyết định tập test mà bước `test registry` của job `gate-registry` chạy (`.github/workflows/ci.yml` dòng 889–895), đúng lập luận của finding `r4286041896`; (3) cổng, đo 23:35:43Z 15-10-2026 bằng cách gọi thẳng hàm của `ops/lease_publish.py` @ `c522c17`: `_tinh_lop_tu_write_set([".claude/dev/ci_dang_ky_test.py"])` ⇒ `sensitive` (không mục nào trong 7 mục `_BANG_LOP` khớp, rơi về `sensitive`); lưới `_kiem_lop_review` (role `executor`, `schema_version: 2`): chỉ 4 ô `effective_review_class: sensitive` qua, 12 ô còn lại rc 10. Patch-as-hint: PROTOCOL §8 dòng 648 chỉ cho packet `sensitive` dùng hint với tệp TEST thuần hoặc tooling không tham gia gate; tệp sổ mang đuôi `_test.py` nhưng LÀ cổng `gate-registry` ⇒ đọc theo hướng chặt (fail-closed): reviewer mô tả finding bằng lời, không đính `HINT.patch` cho tệp này. |
| `review_class` — chú thích nguồn (3) | Nguồn (3) chỉ chứng minh cổng fail-closed, không chứng minh phân lớp theo đường dẫn: `_BANG_LOP` có 7 mục, cả 7 là `sensitive`, và đường không khớp rơi về `sensitive` — nên `_tinh_lop_tu_write_set` trả `sensitive` cho MỌI đường (đo 01:49Z 16-10-2026 tại `c522c17`, gọi thẳng hàm của `ops/lease_publish.py`: `docs/x.md`, `ops/kiem_ho_so_land.py`, `ops/kiem_ho_so_land_test.py` đều ra `sensitive`). Căn cứ phân lớp của packet là nguồn (1) và (2); đừng đếm (3) là nguồn thứ ba độc lập. |
| `executor` · `reviewer` | Thân Issue #763 không ghi executor. Đề xuất Claude (cùng executor với #752); chủ kho chốt lúc cấp lease. Reviewer: Codex `cross_approved` hoặc `human_audited` (PROTOCOL §8 dòng 725–726: hết quota mà chưa có human thì pause). Lượt subagent Claude chỉ là lượt PHỤ, KHÔNG phải `review_deferred` (hàng chú thích ngay dưới). |
| `executor` · `reviewer` — chú thích | `review_deferred` (PROTOCOL dòng 612) KHÔNG dùng được cho packet này: dòng 705–707 cấm nó với workflow/security path, và hàng `review_class` ở trên đã xếp sổ là "workflow/CI authority". Lượt subagent Claude (cùng họ model với executor đề xuất) tối đa là `same_provider_approved`, một mình không thay `cross_approved` cho `sensitive` (dòng 696) — cách viết của `ops/specs/no-p3-lease-spec-hash-r3.md` (hàng `executor` · `reviewer`, cùng commit `11134f2`). |
| `base` | Số đo nền đo trên `c522c173cb58b506bac8cffb24239e16e8459836` theo chỉ thị. `git ls-remote --heads origin` lúc 23:29:24Z: `master` đã sang `9fddb1d` (merge PR #755; `git diff --stat c522c17 9fddb1d` chỉ có `ops/specs/wp728-do-linux-doc-lap-wp710-r2.md`, tệp sổ không đổi); bốn trạng thái của sổ chạy lại trên `9fddb1d` cho đầu ra y hệt (23:38:54Z–23:39:09Z). **Base của lease KHÔNG phải `c522c17`**: nó phải là head ĐÃ DUYỆT của #752 (bốn tệp: hai công cụ và hai test) dựng trên `master` sau khi #748 land, hoặc một nhánh tích hợp đã chứa nó (hàng `depends_on` (2)) — không phải "`master` cộng hai tệp test": đo 03:19Z 16-10-2026, một commit gồm `c522c17` + hai tệp test giả + hai mục `MOI`, KHÔNG có hai công cụ ⇒ `python3 -B .claude/dev/ci_dang_ky_test.py` rc 0, `ĐĂNG KÝ: 25/25`, `PHẢN CHỨNG: 1025/1025 đỏ đúng`, numstat `2 0` (C1 xanh) và `git cat-file -t <base>:<tệp test>` in `blob` cho cả hai (C5 đạt), trong khi `ops/kiem_ho_so_land.py` và `ops/kiem_nhan_hint.py` vắng (`git cat-file -t` báo `does not exist`) — C1 và C5 không phân biệt được base thiếu công cụ. Mọi số dưới đây ĐO LẠI trên base ấy lúc cấp, ghi số mới kèm lý do. |
| `depends_on` | **CHẶN cấp lease** cho tới khi ĐỦ năm điều kiện, đo lại lúc cấp; số trong ô này không thay được phép đo lúc cấp. **(1) #748 land vào `master`** — không chỉ vào `mission/748/integration` (lease `wp748-r11-g11-claude-windows-20261015` khai `target_branch_neu_land: mission/748/integration`). Tệp sổ thuộc write set #748: có trong 8 đường dẫn "Candidate write set" của thân Issue #748 (`gh api repos/ducthangho/tra-luat/issues/748 --jq .body`, đọc 23:27:59Z, Issue `open`) và trong 11 đường dẫn của lease r11 (nhánh `ops/wp748-r11-g11-lease` @ `181e3fb`, `lease_until 2026-10-16T04:27:21Z`). Hiện trạng 23:31:54Z: `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ rc 11, `CÒN_HẠN wp748-r11-g11-claude-windows-20261015 refs/heads/ops/wp748-r11-g11-lease:ops/leases/wp748-r11-g11-claude-windows-20261015.yaml`, `NGƯỜI_GIỮ 1`, cùng 62 dòng `HẾT_HẠN` (r2 của #752 thấy rc 12 bia mộ một chiều r9→r10 lúc 08:54Z; nay lease r11 khai `thay_the_cho: wp748-r10-…` nên bộ quét ra rc 11). Phép đo của (1) là C4b: `ai-dang-giu` chỉ biết HẠN, không biết đã land, nên không thay được. **(2) Hai tệp test của #752 có trên base của #763.** Thân Issue #763 viết "#752 phải land trước, vì hai tệp test phải tồn tại trên master"; nhưng đo S1 (bảng "Số đo nền") cho thấy `master` chứa #752 mà thiếu hai mục `MOI` thì `gate-registry` ĐỎ. Theo đường A của #752 r3 (mục "Đường land"): base của #763 = head ĐÃ DUYỆT (exact SHA) của #752 dựng trên `master` sau #748, hoặc một nhánh tích hợp đã chứa nó; `master` nhận hai packet trong CÙNG MỘT lần merge. Chỗ lệch câu chữ Issue #763 đã được xử lý: chủ kho chọn đường A trong phiên điều phối `session_01CSM7GNazhN6uGJb4v1TqBT` ngày 2026-10-16 (lời khai trong phiên; neo bền là comment cấp lease của chủ kho, đo lại lúc cấp), và phiên điều phối đã sửa thân Issue #763 cho khớp đường A (land cùng một lần merge) — việc sửa thân Issue KHÔNG đo lại ở phiên vá này, đọc lại thân Issue lúc cấp. Đường B (gộp lại một packet có ngoại lệ trần) không chọn. **Đường A nối tiếp #763 trên #752 TRƯỚC khi #752 vào `master`**: base (cả hai nhánh trên) không phải tổ tiên `master` cho tới khi land (`is-ancestor` một head chưa land ⇒ rc 1, như C4b (1)). PROTOCOL §5 dòng 348 và ADR-0027 dòng 10 ("tránh stacked PR") đặt dependency chạy sau predecessor đã integrated; ADR-0044 dòng 15–17 chỉ cho nối tiếp khi slice sau mọc trên `mission/<issue>/integration` đã nhận slice trước, không trên một PR chưa merge, và dòng 21–22 đòi lease có `base_sha` không phải tổ tiên nhánh mặc định khai `xep_tang{tren_pr, thu_tu_land, ke_hoach_rebase}` (ADR chỉ nêu tên ba trường). Điều kiện cấp thêm: comment cấp lease (cùng chỗ neo đường A) ghi cách tuân — lease có `xep_tang`, hoặc ngoại lệ ADR-0027/0044 bằng chữ của chủ kho. Đo 03:37Z 16-10-2026 tại `c522c17`: `xep_tang` có đúng 1 tệp (ADR-0044), 0 trong 152 lease trên `master`, 0 tệp mã cưỡng chế ⇒ cổng hiện KHÔNG chặn, người cấp tự đo; nếu lúc cấp cổng ấy đã có thì thiếu `xep_tang` ⇒ lease bị từ chối (ADR-0044 dòng 22). Kiểm lúc cấp: nửa đầu theo C4b (2); nửa sau theo C5 — `<base>^{commit}` đo được, rồi `ops/kiem_ho_so_land_test.py` và `ops/kiem_nhan_hint_test.py` đều là `blob` (rc 0 của `git cat-file -e` một mình chưa đủ). **(3)** Trên một clone ĐỦ ref — so `git ls-remote --heads origin` với `refs/heads/*` và `refs/remotes/origin/*` (bỏ `HEAD`) theo cặp (tên, OID): thiếu 0, thừa 0, lệch OID 0 (đo 23:30:23Z: 541/541/541, `comm -3` 0 dòng); không chạy được ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp — `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ra `NGƯỜI_GIỮ 0`, rc 0; rc 12 là trạng thái thứ ba. Chốt `origin` là máy chủ GitHub: hàng ngay dưới. **(4) Anh em #751** (`no-p3-lease-spec-hash`): write set r2 của #751 (`ops/specs/no-p3-lease-spec-hash-r2.md` dòng 14) có `.claude/dev/ci_dang_ky_test.py` (+1 dòng `MOI`) và một test sống mới `ops/lease_publish_spec_hash_test.py` ⇒ hai lease KHÔNG đồng thời; bên land sau đo lại C1 vì cả hai số của `ĐĂNG KÝ` đổi. Sau khi tách, write set #752 r3 không giao #751 (đo ~23:37Z), nên quan hệ này thuộc #763. **(5) #748 đổi tệp sổ**: nhánh `agent/wp748-g9-claude` @ `0daeb47` đổi nó +65/−9 dòng so với merge-base với `c522c17` (đo 23:35:49Z); ở nhánh ấy `MOI` vẫn là ánh xạ (dòng 37) và dòng 52 vẫn là mục `ops/nhanh_don_duoc_test.py` (đo ~23:36Z). Write set #748 còn có `ops/nhanh_don_duoc_test.py` và `.claude/dev/doc_receipt_thu_hoi_test.py` — hai bộ đang có mục `MOI`. Lúc cấp: nếu `MOI` không còn là ánh xạ đường dẫn → mẫu regex, hoặc mẫu của mục `ops/nhanh_don_duoc_test.py` đổi, thì soạn revision mới trước khi cấp. |
| `depends_on` (3) — ghim máy chủ | Phép so (3) chỉ có nghĩa khi `origin` LÀ máy chủ GitHub: nếu `origin` là một bản sao cũ thì `ls-remote` và `for-each-ref` cùng mù và cùng khớp. Thêm vào (3): `git remote get-url origin` ra `https://github.com/ducthangho/tra-luat` (hoặc dạng có `.git`); khác ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp. Đo 01:50Z 16-10-2026 trên clone mà `origin` là bản sao cục bộ (1 nhánh): `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ rc 0, 24 dòng `HẾT_HẠN`, `NGƯỜI_GIỮ 0: không có` — trong khi máy chủ lúc 23:31:54Z 15-10 có `NGƯỜI_GIỮ 1` (ô `depends_on` (1) của chính đặc tả này). |
| `depends_on` — đính chính nguồn dẫn | (a) Ô (1) ghi ĐÚNG nguồn, giữ nguyên: "r2 của #752 thấy rc 12 bia mộ một chiều r9→r10 lúc 08:54Z" — phép đo ấy nằm ở `ops/specs/no-p3-cong-cu-ho-so-r2.md` dòng 15 (ngày 15-10-2026; tại `c522c17` `grep -c` "bia mộ một chiều": #752 r2 = 2 ở dòng 15 và 37, #751 r2 = 0). Review lượt 1 khai ô (1) viết "#751": đọc nhầm — đo 02:08:54Z 16-10-2026, `git show 11134f2:` tệp này có đúng 1 dòng chứa "bia mộ một chiều" (dòng 14 tại `11134f2`), và chuỗi ở đó là "r2 của #752 thấy rc 12". (b) Ô (4) dẫn #751 **r2** (`ops/specs/no-p3-lease-spec-hash-r2.md` dòng 14); revision hiện hành là **r3** (`ops/specs/no-p3-lease-spec-hash-r3.md`, cùng commit `11134f2`, `thay_the_cho` r2): `write_set` ở dòng 15, `depends_on` (4) ở dòng 16 — vẫn ba tệp, vẫn "+1 dòng `MOI`" (Mục tiêu 6), nên kết luận (hai lease KHÔNG đồng thời) không đổi; r3 còn nêu: nếu #763 land trước, đích của #751 thành `26/26`. |
| `write_set` | `.claude/dev/ci_dang_ky_test.py` (SỬA: +2 dòng vào `MOI`). |
| `kich_thuoc` | 1 tệp, 2 dòng thêm, 0 dòng xoá (đơn vị: dòng theo `git diff --numstat`) — ĐO, không ước: trạng thái S2 dưới đây cho numstat `2 0` (23:33Z trên `c522c17`). Trần ADR-0044 dòng 5 cho packet `sensitive` chạm authority: ≤ 3 tệp và ≤ 300 dòng thêm ⇒ dư 2 tệp, dư 298 dòng. Không cổng nào cưỡng chế trần: `grep -c` hai chuỗi `numstat` và `ADR-0044` trên `ops/lease_publish.py` và `.claude/dev/packet_loop.py` @ `c522c17` ra 0 cả bốn lần (23:36:35Z) ⇒ người giữ đo. Cần thêm tệp (ví dụ `ci.yml`, hay đổi trần thời gian vì hai test chạy lâu) ⇒ dừng, soạn revision. |

## Số đo nền (`c522c17`; lặp trên `9fddb1d`, đầu ra y hệt)

Tệp sổ tại `c522c17`: 2236 dòng (`wc -l`), sha256 `a1d18f7dd8de529dc2b1b9b6cbac0578477c57d82075ff0bbe6cd2d7a94a8cb8`,
blob `0f8cabc80e6d5b18d59b0d46bb55123f00dd6e12`, commit chạm cuối `36190a3` (`2026-10-07T17:19:25Z`). Nạp mô-đun và
đếm (23:48:19Z): `MOI` 9 mục · `DA_NOI` 14 mục · `DANG_KY` 23 (= 9 + 14; đơn vị: đường dẫn test) · `MOI_WINDOWS` 1 ·
`CACH_LY` 0 · `NHE` và `MAU_DAY_DU` 3 mục mỗi bảng · `GIAY_TOI_DA_MOT_BO` 5400 (giây). Mẫu cần chép là giá trị của
mục `"ops/nhanh_don_duoc_test.py"` ở dòng 52: chuỗi thô, neo đầu và cuối dòng, hai nhóm số nguyên ngăn bởi `/`
(viết bằng lời, không chép chuỗi có dấu chéo ngược — CLAUDE.md, mục "TẦNG VẬN CHUYỂN CŨNG CHUẨN HOÁ CHUỖI").
`ruff check --select F --no-cache` trên tệp sổ: `All checks passed!`, rc 0 (ruff 0.15.8, 23:35:49Z).

Các trạng thái, đo trên clone tạm (ghi thử trong clone, khôi phục sau mỗi bước, `git status --porcelain` rỗng ở
cuối). Lệnh tĩnh: `python3 -B .claude/dev/ci_dang_ky_test.py` (không `--chay`). Hai tệp test giả in `1/1`, hai
công cụ giả rỗng. Mục `MOI` chèn bằng cách chép NGUYÊN dòng 52 rồi chỉ thay khoá. Đơn vị của `ĐĂNG KÝ: a/b`:
a = tệp test sống trên cây, b = mục trong sổ.
Quy ước đơn vị và ngày của tệp này: mọi mốc `hh:mm(:ss)Z` là UTC ngày 15-10-2026 trừ chỗ ghi ngày khác (đo 01:51Z 16-10-2026 trên bản tại `11134f2`: 27 trên 33 mốc không kèm ngày); `do` = số mục `MOI`
bị `chay_moi` chấm ĐỎ (giá trị hàm trả về; đơn vị: mục); `541/541/541` (ô `depends_on` (3)) = số nhánh trên máy chủ / `refs/heads/*` / `refs/remotes/origin/*` (đơn vị: nhánh);
`MOI_WINDOWS` 1 và `CACH_LY` 0: đơn vị mục; `1025/1025`: đơn vị ca phản chứng của `phan_chung()`.

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
   (dòng 52 tại `c522c17`; đo lại vị trí trên base thật): khoá `"ops/kiem_ho_so_land_test.py"` và
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
- **C1b (hai khoá nằm TRONG `MOI`, mẫu bằng mẫu của `nhanh`):**
  `python -B -c "import runpy;m=runpy.run_path('.claude/dev/ci_dang_ky_test.py');M=m['MOI'];n=M['ops/nhanh_don_duoc_test.py'];k=('ops/kiem_ho_so_land_test.py','ops/kiem_nhan_hint_test.py');print(all(x in M and M[x]==n for x in k),len(M))"`
  ⇒ in `True N`, N = số khoá `MOI` ở base cộng 2 (`True 11` trên `c522c17`: 9 + 2). ĐỎ khi: (a) một khoá chỉ nằm trong `DANG_KY` mà không qua `MOI` — đo 01:50Z 16-10-2026:
  hai dòng `DANG_KY.add(...)` thay cho hai mục `MOI` ⇒ C1, C2, C3 đều XANH (rc 0, `25/25`, `1025/1025`, numstat `2 0`; gỡ từng dòng ⇒ `25/24` + một dòng `ĐỎ:`; đổi tên ⇒ `25/25` + hai dòng `ĐỎ:`),
  nhưng `len(MOI)` vẫn 9, `chay_moi()` mặc định không chạy hai bộ ấy, lệnh trên in `False 9`; (b) mẫu không bằng mẫu `nhanh` — đo cùng lượt: mẫu không neo `^`…`$` ⇒ C1–C4 đều XANH
  (M3: `0/0` và `3/4` vẫn ĐỎ), nhưng nhận cả dòng văn xuôi `xong 5/5 ca (ok)` mà mẫu `nhanh` từ chối (`do` 0 so với 1), lệnh trên in `False 11`. C4 phải lấy mẫu từ `MOI` của CHÍNH tệp
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
  khoá `merge_commit` cấp 0 (chuỗi SHA; 25 trên 27 hồ sơ tại `c522c17`) hoặc `trang_thai_packet.merge_commit.sha` (2 trên 27:
  `pr721-wp698`, `pr732-wp685`; đo 03:26Z 16-10-2026)); rc 1 ⇒ chưa land;
  rc ≥ 128 hoặc chưa có SHA ⇒ KHÔNG ĐO ĐƯỢC ⇒ không cấp. (2) `git merge-base --is-ancestor <SHA merge land #748> <base>` ⇒ rc 0 VÀ có verdict duyệt #752 neo `reviewed_sha` đúng SHA dùng làm
  base (hoặc SHA ấy là tổ tiên của `<base>` trên nhánh tích hợp). Lệnh cho vế sau: `git merge-base --is-ancestor <reviewed_sha> <base>` ⇒ rc 0. Nơi tra verdict: biên nhận `ops/reviews/*.receipt.yaml` (khoá `reviewed_sha`) VÀ dòng `Reviewed commit:` trong comment của connector Codex trên PR của #752 (CLAUDE.md, mục "HỎI CHỖ TIỆN TAY", ý (b)); rỗng ở MỘT chỗ KHÔNG là "chưa duyệt", không thấy ở cả hai ⇒ KHÔNG ĐO ĐƯỢC ⇒ không cấp. "Duyệt" là assurance mà lớp của #752 đòi — `cross_approved` hoặc `human_audited` (PROTOCOL dòng 530 và 724–726) — không phải mọi biên nhận `verdict: approve`: đo 03:41Z 16-10-2026 trên 276 biên nhận tại `c522c17`, 80 có verdict thuộc nhóm duyệt (`approve`, `approved`, `approve_with_findings`) mà chỉ 29 mang `assurance: cross_approved`, 5 mang `review_deferred` (gồm `ops/reviews/no-p3-ho-so-exec-review-1-claude-verdict.receipt.yaml`, cùng họ `no-p3`), 2 mang `same_provider_*`; biên nhận kiểm toán người không có khoá `assurance` (`role: auditor`). Mỗi lệnh `is-ancestor` ở (1) và (2) có ba trạng thái: rc 0 có · rc 1 không · rc ≥ 128 KHÔNG ĐO ĐƯỢC. Vì sao điều kiện (3) không thay được (1): `ai-dang-giu` chỉ biết HẠN (`_phan_loai_lease`: `HẾT_HẠN` khi `lease_expires_at_utc` đã qua) và bia mộ `da_bi_thay_the`,
  không biết packet đã land chưa — fixture đo 01:50Z 16-10-2026: lease trên nhánh CHƯA land vào `master`, đã hết hạn ⇒ `HẾT_HẠN`, `NGƯỜI_GIỮ 0: không có`, rc 0; cùng lease còn hạn ⇒ `NGƯỜI_GIỮ 1`, rc 11.
  Lease r11 của #748 hết hạn `2026-10-16T04:27:21Z` (ô `depends_on` (1)): sau mốc ấy (3) có thể ra rc 0 kể cả khi #748 chưa land. ĐỎ khi (1) hoặc (2) không rc 0.
- **C5 (thứ tự land):** trên một base THIẾU hai tệp test ⇒ S3 (`23/25`, rc 1) — đây là phép đo chứng minh #763 không
  được vào trước #752. Tiêu chí lúc cấp và lúc land: `git cat-file -e <base>^{commit}` rc 0 (đo được), rồi `git cat-file -t <base>:<tệp test>` in `blob` cho cả hai tệp (rc 0 của
  `git cat-file -e` chưa đủ: thư mục cũng rc 0); tệp vắng ⇒ rc 128 ⇒ ĐỎ; `<base>` không tồn tại cũng rc 128 (đo 01:51Z 16-10-2026: cùng dạng thông điệp "does not exist") ⇒ KHÔNG ĐO ĐƯỢC, không phải "vắng".
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

## Vá sau review lượt 1

Nguồn: verdict `changes_requested` lượt 1 (`reviewed_sha` `11134f2`, `spec_sha256` `9791add6…c031d`; 0 P1 · 2 P2 · 9 P3),
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
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT.

| lớp | hạng | chỗ sửa |
|---|---|---|
| `c4b-2-verdict-duyet-khong-co-noi-tra` | P3 | C4b (2): nêu lệnh, nơi tra verdict duyệt #752 và trạng thái khi không thấy |
| `va-nhan-d-e-khong-dinh-nghia` | P3 | mục "Vá sau review lượt 1": định nghĩa nhãn D, E |

## Vá sau review lượt 3

Bản trước vá: commit `5bd6d03`, sha256 `b1e320a35a06…` (đầy đủ ở `truoc-sau.diff` của lượt 4). Review lượt 3 (`approve`,
0 P1 · 0 P2 · 6 P3; reviewer Claude Sonnet 5.5 subagent `review-sonnet-max`, `reviewed_sha`
`5bd6d0358ab48baed41a9b9d05cbae9a863a74e7`; VERDICT sha256 `3fb414bfc05a5363ea6d4fbed9a3e827d11aa373e77280c670aba2086c558ffc`,
HINT sha256 `e21941e2f1a05e699d18e1a20ce5867cedecdc58b1b61e66bd786a7a06baa508`). Áp NGUYÊN VĂN 5 hunk của HINT
(`patch -p0 --fuzz=0`, rc 0); không sửa gì ngoài HINT. Sáu lớp: `c8-dan-b6d-r3-752-da-sua-o-b6ab45e` ·
`base-chi-hai-tep-test-lech-head-da-duyet` · `depends-on-2-duong-a-thieu-xep-tang-adr-0044` ·
`c4b-1-khoa-merge-commit-hai-hinh-dang` · `c4b-2-verdict-duyet-khong-neu-assurance` ·
`c6-cong-xanh-toan-phan-752-giao-nhung-khong-do` — chỗ sửa xem từng hunk (dòng `# lop:` trong HINT).
