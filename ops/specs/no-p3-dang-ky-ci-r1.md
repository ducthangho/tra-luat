# Đặc tả packet `no-p3-dang-ky-ci` r1 — đăng ký hai bộ test của #752 vào sổ test sống

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-dang-ky-ci` |
| `packet_issue` | #763 — https://github.com/ducthangho/tra-luat/issues/763 ("Packet NO-P3-DANG-KY-CI: đăng ký hai bộ test của #752 vào ci_dang_ky_test.py", `open`, mở bởi `ducthangho` `2026-10-15T23:26:04Z`; đọc qua `gh api repos/ducthangho/tra-luat/issues/763` ~23:27Z 15-10-2026). |
| `revision` | 1 |
| `thay_the_cho` | Không có revision trước. Nội dung TÁCH từ mục tiêu 5 và B6(a) của `ops/specs/no-p3-cong-cu-ho-so-r2.md` (#752 r2, sha256 `ce39f1e164fd94e342af59a0624cec1fc23fc84574f0ec1e5c627a656a17593b`, commit `a9ef33c`); r2 ấy đóng băng, không sửa. Bản anh em cùng lượt: `ops/specs/no-p3-cong-cu-ho-so-r3.md` (#752 r3). |
| `nguon_cap_viec` | Quyết định chủ kho 15-10-2026 **"tách 2 packet"** (chuyển tới qua phiên điều phối; thân Issue #763 ghi lý do, phạm vi, phụ thuộc và tên tệp đặc tả này). Lý do tách: finding P2 của connector Codex trên PR #762, `pull/762#discussion_r4286041896` ("Apply the sensitive packet size ceiling", `created_at 2026-10-15T17:13:10Z`) — sửa sổ test sống là đổi CI/gate authority nên #752 r2 (5 tệp, ~900 dòng) vượt trần `sensitive` 3 tệp/300 dòng. Nợ `SPEC-R2-751-752-KHONG-DUOC-CAP-LEASE` (`ops/land/pr759-no-p3-ho-so-land-evidence.yaml` dòng 407, `trang_thai: mo`). Hai test được đăng ký là mục tiêu 2 và 4 của #752 r3. |
| ngưỡng chặn | Theo bảng PROTOCOL §8 dòng 621 cho lớp `sensitive`: không còn P0; cần approval tường minh đúng assurance và quyết định có căn cứ cho từng finding còn mở. Ngưỡng "chỉ P1/P2 chặn" của #752 không tự áp sang #763 — chưa có nguồn thẩm quyền riêng cho #763 (KHÔNG ĐO ĐƯỢC). |
| `review_class` | **`sensitive`** · `effective_review_class`: **`sensitive`**. Ba nguồn khớp nhau: (1) thân Issue #763 "Lớp sensitive"; (2) PROTOCOL §8 dòng 724 xếp "workflow/CI authority" vào `sensitive` — sổ này quyết định tập test mà bước `test registry` của job `gate-registry` chạy (`.github/workflows/ci.yml` dòng 889–895), đúng lập luận của finding `r4286041896`; (3) cổng, đo 23:35:43Z 15-10-2026 bằng cách gọi thẳng hàm của `ops/lease_publish.py` @ `c522c17`: `_tinh_lop_tu_write_set([".claude/dev/ci_dang_ky_test.py"])` ⇒ `sensitive` (không mục nào trong 7 mục `_BANG_LOP` khớp, rơi về `sensitive`); lưới `_kiem_lop_review` (role `executor`, `schema_version: 2`): chỉ 4 ô `effective_review_class: sensitive` qua, 12 ô còn lại rc 10. Patch-as-hint: PROTOCOL §8 dòng 648 chỉ cho packet `sensitive` dùng hint với tệp TEST thuần hoặc tooling không tham gia gate; tệp sổ mang đuôi `_test.py` nhưng LÀ cổng `gate-registry` ⇒ đọc theo hướng chặt (fail-closed): reviewer mô tả finding bằng lời, không đính `HINT.patch` cho tệp này. |
| `executor` · `reviewer` | Thân Issue #763 không ghi executor. Đề xuất Claude (cùng executor với #752); chủ kho chốt lúc cấp lease. Reviewer: Codex `cross_approved` hoặc `human_audited` (PROTOCOL §8 dòng 725–726: hết quota mà chưa có human thì pause). Lượt subagent Claude chỉ là `review_deferred` (dòng 612). |
| `base` | Số đo nền đo trên `c522c173cb58b506bac8cffb24239e16e8459836` theo chỉ thị. `git ls-remote --heads origin` lúc 23:29:24Z: `master` đã sang `9fddb1d` (merge PR #755; `git diff --stat c522c17 9fddb1d` chỉ có `ops/specs/wp728-do-linux-doc-lap-wp710-r2.md`, tệp sổ không đổi); bốn trạng thái của sổ chạy lại trên `9fddb1d` cho đầu ra y hệt (23:38:54Z–23:39:09Z). **Base của lease KHÔNG phải `c522c17`**: nó phải là `master` sau khi #748 land, cộng hai tệp test của #752 (hàng `depends_on` (2)). Mọi số dưới đây ĐO LẠI trên base ấy lúc cấp, ghi số mới kèm lý do. |
| `depends_on` | **CHẶN cấp lease** cho tới khi ĐỦ năm điều kiện, đo lại lúc cấp; số trong ô này không thay được phép đo lúc cấp. **(1) #748 land vào `master`** — không chỉ vào `mission/748/integration` (lease `wp748-r11-g11-claude-windows-20261015` khai `target_branch_neu_land: mission/748/integration`). Tệp sổ thuộc write set #748: có trong 8 đường dẫn "Candidate write set" của thân Issue #748 (`gh api repos/ducthangho/tra-luat/issues/748 --jq .body`, đọc 23:27:59Z, Issue `open`) và trong 11 đường dẫn của lease r11 (nhánh `ops/wp748-r11-g11-lease` @ `181e3fb`, `lease_until 2026-10-16T04:27:21Z`). Hiện trạng 23:31:54Z: `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ rc 11, `CÒN_HẠN wp748-r11-g11-claude-windows-20261015 refs/heads/ops/wp748-r11-g11-lease:ops/leases/wp748-r11-g11-claude-windows-20261015.yaml`, `NGƯỜI_GIỮ 1`, cùng 62 dòng `HẾT_HẠN` (r2 của #752 thấy rc 12 bia mộ một chiều r9→r10 lúc 08:54Z; nay lease r11 khai `thay_the_cho: wp748-r10-…` nên bộ quét ra rc 11). **(2) Hai tệp test của #752 có trên base của #763.** Thân Issue #763 viết "#752 phải land trước, vì hai tệp test phải tồn tại trên master"; nhưng đo S1 (bảng "Số đo nền") cho thấy `master` chứa #752 mà thiếu hai mục `MOI` thì `gate-registry` ĐỎ. Theo đường A của #752 r3 (mục "Đường land"): base của #763 = head ĐÃ DUYỆT (exact SHA) của #752 dựng trên `master` sau #748, hoặc một nhánh tích hợp đã chứa nó; `master` nhận hai packet trong CÙNG MỘT lần merge. Chỗ lệch câu chữ Issue #763 đã được xử lý: chủ kho chọn đường A trong phiên điều phối `session_01CSM7GNazhN6uGJb4v1TqBT` ngày 2026-10-16 (lời khai trong phiên; neo bền là comment cấp lease của chủ kho, đo lại lúc cấp), và phiên điều phối đã sửa thân Issue #763 cho khớp đường A (land cùng một lần merge) — việc sửa thân Issue KHÔNG đo lại ở phiên vá này, đọc lại thân Issue lúc cấp. Đường B (gộp lại một packet có ngoại lệ trần) không chọn. Kiểm lúc cấp: `git cat-file -e <base>:ops/kiem_ho_so_land_test.py` và `…:ops/kiem_nhan_hint_test.py` đều rc 0. **(3)** Trên một clone ĐỦ ref — so `git ls-remote --heads origin` với `refs/heads/*` và `refs/remotes/origin/*` (bỏ `HEAD`) theo cặp (tên, OID): thiếu 0, thừa 0, lệch OID 0 (đo 23:30:23Z: 541/541/541, `comm -3` 0 dòng); không chạy được ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp — `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ra `NGƯỜI_GIỮ 0`, rc 0; rc 12 là trạng thái thứ ba. **(4) Anh em #751** (`no-p3-lease-spec-hash`): write set r2 của #751 (`ops/specs/no-p3-lease-spec-hash-r2.md` dòng 14) có `.claude/dev/ci_dang_ky_test.py` (+1 dòng `MOI`) và một test sống mới `ops/lease_publish_spec_hash_test.py` ⇒ hai lease KHÔNG đồng thời; bên land sau đo lại C1 vì cả hai số của `ĐĂNG KÝ` đổi. Sau khi tách, write set #752 r3 không giao #751 (đo ~23:37Z), nên quan hệ này thuộc #763. **(5) #748 đổi tệp sổ**: nhánh `agent/wp748-g9-claude` @ `0daeb47` đổi nó +65/−9 dòng so với merge-base với `c522c17` (đo 23:35:49Z); ở nhánh ấy `MOI` vẫn là ánh xạ (dòng 37) và dòng 52 vẫn là mục `ops/nhanh_don_duoc_test.py` (đo ~23:36Z). Write set #748 còn có `ops/nhanh_don_duoc_test.py` và `.claude/dev/doc_receipt_thu_hoi_test.py` — hai bộ đang có mục `MOI`. Lúc cấp: nếu `MOI` không còn là ánh xạ đường dẫn → mẫu regex, hoặc mẫu của mục `ops/nhanh_don_duoc_test.py` đổi, thì soạn revision mới trước khi cấp. |
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

## Nghiệm thu

- **C1 (xanh trên head của packet):** trên head #763 (base theo `depends_on` (2), cộng hai dòng):
  `python -B .claude/dev/ci_dang_ky_test.py` ⇒ rc 0, 0 dòng `ĐỎ:`, `ĐĂNG KÝ: a/a` với a = số đo nền trên base thật
  cộng 2 (`25/25` trên `c522c17`), `PHẢN CHỨNG: n/n đỏ đúng` (`1025/1025` trên `c522c17`), `TỔNG: ĐẠT`;
  `git diff --numstat -- .claude/dev/ci_dang_ky_test.py` so với base là `2 0`; `git diff --name-only` so với base đúng một đường
  dẫn. Đo: S2. ĐỎ khi: C2, C3; khi diff chạm thêm tệp; khi numstat khác `2 0`.
- **C2 (đột biến bỏ một mục ⇒ ĐỎ):** gỡ riêng từng mục trên bản sao tạm ⇒ rc 1, đúng một dòng
  `ĐỎ: test sống chưa đăng ký: <tệp vừa gỡ>`, `ĐĂNG KÝ: 25/24`, `TỔNG: ĐỎ` (M1, M1b); gỡ cả hai ⇒ S1. Phép đo nghiệm thu
  phải chạy CẢ HAI đột biến: một bản cài đặt chỉ thêm một mục qua được đột biến của mục kia.
- **C3 (đột biến trỏ tên tệp sai ⇒ ĐỎ):** một mục trỏ `ops/kiem_nhan_hint_tests.py` ⇒ rc 1, hai dòng `ĐỎ:`,
  `TỔNG: ĐỎ` (M2). Phép đo đọc rc, dòng `TỔNG:` VÀ đếm dòng `ĐỎ:` — không được chỉ so hai số của `ĐĂNG KÝ`, vì ở M2
  chúng bằng nhau (`25/25`). ĐỎ (tiêu chí hỏng) khi một bộ đo nghiệm thu chỉ đọc `ĐĂNG KÝ` mà báo M2 là xanh.
- **C4 (mẫu và dòng đầu ra, tầng `--chay`):** tầng tĩnh không đọc mẫu, nên đo bằng `chay_moi` thật (hoặc `--chay`):
  mục đúng tên mà mẫu bị thay bằng mẫu của một mục khác ⇒ `do = 1` (M4); test in `0/0` hoặc `3/4` ⇒ `do = 1` (M3);
  hai test thật của #752 ⇒ cả hai dòng `CI_DANG_KY …: ĐẠT`, `do = 0`. ĐỎ khi một trong hai test thật cho `ĐỎ`.
- **C5 (thứ tự land):** trên một base THIẾU hai tệp test ⇒ S3 (`23/25`, rc 1) — đây là phép đo chứng minh #763 không
  được vào trước #752. Tiêu chí lúc cấp và lúc land: `git cat-file -e <base>:<tệp test>` rc 0 cho cả hai tệp; ĐỎ khi
  một tệp vắng.
- **C6 (CI thật):** `gate-registry` xanh trên head gộp (Ubuntu; thêm Windows nếu PR gắn nhãn `windows` hoặc
  `workflow_dispatch`): log bước `test registry` có `CI_DANG_KY ops/kiem_ho_so_land_test.py: ĐẠT`,
  `CI_DANG_KY ops/kiem_nhan_hint_test.py: ĐẠT`, `CI_DANG_KY_THOI_GIAN` có một mục cho mỗi khoá `MOI` (11 nếu base thật
  vẫn 9 mục như `c522c17`), và `TỔNG: ĐẠT`. ĐỎ khi một trong hai dòng là `ĐỎ` hoặc vắng. KHÔNG ĐO ĐƯỢC ngoài GitHub
  Actions; ghi run id và kết luận từng job lúc thi hành.
- **C7 (ruff):** `ruff check --select F` trên tệp sổ: delta 0 (multiset) so với base (`All checks passed!` trên
  `c522c17`); ghi phiên bản (container soạn spec có binary 0.15.8, `python3 -m ruff` không có module; CI ghim
  0.15.15). ĐỎ khi chèn một import thừa ⇒ `F401`, rc 1 (đo 23:42:14Z trên bản sao ngoài kho: thêm `import fractions`
  ⇒ `F401`, `Found 1 error.`, rc 1).

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
