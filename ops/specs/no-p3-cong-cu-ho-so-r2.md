# Đặc tả packet `no-p3-cong-cu-ho-so` r2 — nợ P3 (b2): bộ kiểm hồ sơ land + bộ kiểm nhãn HINT

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-cong-cu-ho-so` |
| `packet_issue` | #752 |
| `revision` | 2 |
| `thay_the_cho` | **r1**: `ops/specs/no-p3-cong-cu-ho-so-r1.md`, sha256 `c3fd632282b822365ccd3656cc12f278b7a76a5c0c5484c516cd62033beb8f8a`, commit `55bd0d24d299d20ff32a8b2dd42deb200295462e`. Thứ định danh r1 là cặp băm này, không phải tên nhánh chứa nó. r2 không sửa byte nào của r1; lease và `spec_hash` từ nay neo r2. |
| review của r1 | Lượt 1, reviewer Claude Sonnet 5.5 (subagent `review-sonnet-max`, tự khai): `verdict: changes_requested`, `reviewed_sha` `55bd0d24d299d20ff32a8b2dd42deb200295462e`, **0 P1 · 2 P2 · 4 P3 = 6 lớp**. `VERDICT.md` sha256 `0cf329f40dc36cdbde87f9fd75cb154bc9a2a6d03882d5c6aabb4dd7579167bd`; `HINT.patch` (15 hunk, chỉ văn bản đặc tả) sha256 `42cd6b008a9440e9e6223434ea04258e9e875e2e8c9668cb02aae3974892def9`. Lúc soạn r2 (15-10-2026) hai tệp nằm ở thư mục tạm của phiên điều phối, chưa có bản trong kho; thứ định danh chúng là băm. Cách r2 đóng từng lớp: mục "Thay đổi so với r1". |
| `nguon_cap_viec` | Sổ nợ P3 mục 5 và 6, cả hai do connector Codex nêu trên PR #722 (mục 5: review comment `pull/722#discussion_r4231959151` "audit mọi `*-HINT.patch`" — `ops/reviews/README.md` dòng 655 dẫn đúng URL này cho HINT lượt 3 thiếu nhãn, còn câu trích KHÔNG ĐO ĐƯỢC offline; mục 6: schema check `authorized_head_sha` khi `landed: true` — chưa có id comment trong kho, KHÔNG ĐO ĐƯỢC offline). Cách tách và phạm vi do chủ kho chốt 15-10-2026 (Q4, Q7, Q9 — KHÔNG ĐO ĐƯỢC offline). Đăng ký hai test vào sổ test sống `.claude/dev/ci_dang_ky_test.py` (mục tiêu 5): quyết định chủ kho 15-10-2026, chuyển tới qua phiên điều phối (id comment KHÔNG ĐO ĐƯỢC từ phiên soạn r2). |
| ngưỡng chặn | "Chỉ P1/P2 chặn merge" (hàng `executor` · `reviewer`) — nguồn thẩm quyền riêng cho #752 chưa được ghi (KHÔNG ĐO ĐƯỢC offline). Tiền lệ, KHÔNG phải nguồn: comment #698 `6094652521`, bản đọc lại trong kho `ops/land/pr721-wp698-provenance/readback-comment-6094652521.json` (`author_association: OWNER`, `created_at: 2026-10-10T06:28:10Z`) đặt ngưỡng "0 P1 / 0 P2. Lớp P3 trở xuống KHÔNG chặn" cho wp698 (spec r14, lease `wp698-r14-g2-claude`), không nhắc #752. |
| `review_class` | **`sensitive`** · `effective_review_class`: **`sensitive`**. Từ vựng PROTOCOL §3.2 (dòng 156) là `routine`/`systemic`/`sensitive`; `standard` của r1 không thuộc từ vựng. Đo 08:53:17Z 15-10-2026, gọi thẳng hàm của `ops/lease_publish.py` @ `55bd0d2`: `_tinh_lop_tu_write_set` trả `sensitive` cho write set 4 tệp của r1 và cho write set 5 tệp của r2 — `_BANG_LOP` có 7 mục, cả 7 đều `sensitive`, đường không có trong bảng rơi về `sensitive`, nên thêm `.claude/dev/ci_dang_ky_test.py` không đổi lớp; `_kiem_lop_review` (role `executor`, `schema_version: 2`) chặn rc 10 khi `effective_review_class: routine` với mọi giá trị khai (`routine`, `systemic`, `sensitive`, `standard`), cho qua khi `sensitive`. Độc lập với cổng, PROTOCOL §8 dòng 724 xếp "workflow/CI authority" vào `sensitive`, và mục tiêu 5 sửa đúng tệp mà bước CI `test registry` chạy. Trần ADR-0044: hàng `kich_thuoc`. |
| `executor` · `reviewer` | Claude (executor); reviewer subagent Claude Sonnet (`review_deferred`). Chỉ P1/P2 chặn merge. Với lớp `sensitive`, PROTOCOL §8 dòng 724–726 đòi Codex `cross_approved` hoặc `human_audited`; dòng 612: `review_deferred` "vẫn được vào draft land PR nhưng cần xác nhận riêng khi apply"; dòng 621: lớp `sensitive` cần quyết định có căn cứ cho từng finding còn mở. Lượt review subagent không thay được các xác nhận ấy. |
| `base` | `origin/master` `6f121a3810045af27bf65eb723edf36b29e387f2` (đo 15-10 ~06:10Z; đo lại 08:54:02Z bằng `git ls-remote --heads origin`: `master` vẫn `6f121a3`). #748 land sẽ dời nền — xem `depends_on` (3). |
| `depends_on` | **CHẶN cấp lease** cho tới khi cả ba điều kiện dưới đây thoả **và được đo lại lúc cấp**; số trong ô này không thay được phép đo lúc cấp. (1) Packet #748 đã land: tệp sổ `.claude/dev/ci_dang_ky_test.py` đang nằm trong write set của #748 (`ops/specs/wp748-windows-gates-r10.md` mục 4, trên nhánh `ops/wp748-r10-g10-lease` @ `2c03974`; lease `wp748-r9-g9-claude-windows-20261015` trên cùng nhánh liệt kê tệp ấy, `lease_until: 2026-10-15T13:07:00Z`). (2) `python ops/lease_publish.py ai-dang-giu .claude/dev/ci_dang_ky_test.py --root <clone>` ra `NGƯỜI_GIỮ 0`, rc 0, và bốn đường dẫn MỚI của write set cũng `NGƯỜI_GIỮ 0`, trên một clone đủ ref: lệnh quét đọc `refs/heads/*`, nên tập tên `git ls-remote --heads origin` phải bằng cả tập tên `refs/heads/*` lẫn tập tên `refs/remotes/origin/*` (bỏ `HEAD`), thiếu cục bộ 0; không chạy được phép so ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp. rc 12 là trạng thái thứ ba, không phải "không ai giữ". (3) #748 đổi tệp sổ (nhánh `agent/wp748-g9-claude` @ `0daeb47` đổi nó +65/−9 so với merge-base với `master`, đo 08:53Z) ⇒ lúc cấp đo lại B6(a) và "Số đo nền" trên nền mới, ghi số mới kèm lý do; nếu `MOI` không còn là ánh xạ đường dẫn → mẫu regex thì viết lại mục tiêu 5 bằng revision mới trước khi cấp. **Hiện trạng đo 08:54:46Z–08:57:13Z 15-10-2026** trên clone tạm lấy từ GitHub (máy chủ 536 nhánh; `refs/heads` 536; `refs/remotes/origin` 536; thiếu 0, thừa 0; HEAD `55bd0d2`): `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ rc 12 `KHÔNG_XÁC_ĐỊNH`, nguyên văn "bia mộ một chiều 'wp748-r9-g9-claude-windows-20261015' -> 'wp748-r10-g10-claude-windows-20261015' tại refs/heads/ops/wp748-r10-g10-lease:ops/leases/wp748-r9-g9-claude-windows-20261015.yaml; không tìm thấy lease thay thế trỏ ngược bằng thay_the_cho"; bốn đường dẫn mới ⇒ `NGƯỜI_GIỮ 0: không có`, rc 0. Điều kiện (1) và (2) **chưa thoả**. Ghi chú: bản clone review `cay-kho` lúc 08:54:02Z thiếu 2 nhánh so với máy chủ (`agent/wp741-r1-g1-claude`, `ops/wp741-spec`) và chỉ có 1 ref trong `refs/heads` — đo người giữ trên bản ấy là đo sai chỗ. |
| `write_set` | `ops/kiem_ho_so_land.py` (MỚI) · `ops/kiem_ho_so_land_test.py` (MỚI) · `ops/kiem_nhan_hint.py` (MỚI) · `ops/kiem_nhan_hint_test.py` (MỚI) · `.claude/dev/ci_dang_ky_test.py` (SỬA: +2 dòng vào `MOI`). Sổ test sống đòi MỌI `ops/*_test.py` mức đỉnh được đăng ký, và đăng ký với hai tệp test phải đi CÙNG một PR — đo 08:52:27Z–08:52:54Z 15-10-2026 trên clone tạm `55bd0d2`, lệnh `python3 -B .claude/dev/ci_dang_ky_test.py` (không `--chay`): nền `ĐĂNG KÝ: 23/23`, `TỔNG: ĐẠT`, rc 0; thêm bốn tệp giả mà không đăng ký ⇒ `25/23`, `TỔNG: ĐỎ`, rc 1 (`test sống chưa đăng ký`); thêm hai dòng `MOI` ⇒ `25/25`, `TỔNG: ĐẠT`, rc 0; giữ hai dòng `MOI` mà gỡ hai tệp test ⇒ `23/25`, `TỔNG: ĐỎ`, rc 1 (`mục đăng ký không có tệp`). Điều kiện cấp lease: hàng `depends_on`. |
| `kich_thuoc` | 5 tệp (4 MỚI + 1 SỬA). Ước ≤ 900 dòng thêm, 0 dòng xoá (đơn vị: dòng theo `git diff --numstat`): 700 của r1 cho bốn tệp mới, khoảng 200 cho các ca r2 thêm vào B1, B1b, B4, B7, và 2 dòng ở sổ test sống — là ƯỚC, không phải đo; đo lại trước review. Trần ADR-0044: lớp theo cổng là `sensitive`; r2 xếp packet là `sensitive` **KHÔNG chạm authority** — bốn tệp mới chỉ đọc và không thuộc đường nào của `_BANG_LOP`; hai dòng ở sổ chỉ THÊM hai mục bắt buộc vào `MOI`, không đổi `kiem()`, `chay_moi()` hay `bang_chung_xanh()`, tức siết cổng chứ không nới — nên áp trần packet thường (≤ 6 tệp và ≤ 1.000 dòng thêm cộng xoá): 5 tệp, ước ≤ 900 dòng. Tiền lệ cách xếp: `ops/specs/wp726-nlm-script-phan-quyet-canary-r1.md`. Chủ kho bác cách xếp này ⇒ trần `sensitive` chạm authority (≤ 3 tệp, ≤ 300 dòng thêm) bị vượt cả hai vế ⇒ dừng trước review, thiết kế lại cách tách bằng revision mới (đăng ký không tách khỏi test được — hàng `write_set`). Không cổng nào cưỡng chế trần này: `grep -c` hai chuỗi `numstat` và `ADR-0044` trên `ops/lease_publish.py` và `.claude/dev/packet_loop.py` ra 0 cả bốn lần ⇒ người giữ đo. |

## Thay đổi so với r1

Soạn r2 theo thứ tự: (1) chép r1 thành r2, đổi tên tệp đích trong `HINT.patch` từ r1 sang r2 bằng `sed`, rồi
`patch -p0 --fuzz=0` — rc 0, 15/15 hunk, không `.rej`, bản sau vá 66 dòng (khớp số reviewer ghi); (2) đo lại mọi
con số trên bản clone review `cay-kho` @ `55bd0d2` và trên clone tạm lấy từ GitHub, giờ đo ghi tại chỗ; (3) sửa
tiếp phần HINT mà phép đo hoặc chỉ thị điều phối cho thấy chưa đủ.

| lớp (hạng) | r2 sửa ở đâu |
|---|---|
| `write-set-thieu-so-dang-ky-test-ci` (P2) | `write_set` thêm `.claude/dev/ci_dang_ky_test.py` (5 tệp), kèm phép đo bốn trạng thái của sổ; hàng mới `depends_on` (chặn cấp lease tới khi #748 land VÀ `ai-dang-giu` ra `NGƯỜI_GIỮ 0` trên clone đủ ref; hiện trạng rc 12); `kich_thuoc`; mục tiêu 5; B6 viết lại thành bốn vế, ba vế có phép đo ĐỎ đã chạy, vế CI thật KHÔNG ĐO ĐƯỢC; "Ngoài phạm vi" tách `ci.yml` khỏi sổ test sống; "Chưa đo được" (Windows). Căn cứ: quyết định chủ kho 15-10-2026. |
| `l6-menh-de-khong-co-ca-do` (P2) | L-6 chốt `is True`, vị trí đọc `landed`, hai khoá ở MỨC GỐC, kiểu `str`, `fullmatch`, `startswith`, `yaml.safe_load`, gốc không phải ánh xạ ⇒ rc 3; B1 mỗi ca vi phạm đúng một mệnh đề, mỗi đột biến làm đúng ca của nó ĐỎ; B1b cho fail-close. |
| `l5-nguyen-van-chua-chot-nghia` (P3) | L-5 dùng chuỗi đầy đủ có ` commit`; "rỗng" là rỗng sau `strip()`; mọi `OSError` ⇒ `KHONG_DOC_DUOC`; tên lớp khai rõ chỉ đo ràng buộc 1; B4 thêm mồi cụt, tệp chỉ có xuống dòng, thư mục. |
| `so-do-nen-chua-phan-ra` (P3) | "Số đo nền" đo lại 08:51Z: 35 = 26 không nhãn + 9 nhãn bỏ dấu; băm 29 trong `*.receipt.yaml` + 6 trong `luot*-VERDICT.md`/`luot*-EVIDENCE.md`; `pr672` chỉ thiếu hai khoá ở MỨC GỐC; 12 hồ sơ không có `landed` được phân rã 11 + 1. |
| `cli-hop-dong-chua-chot` (P3) | Mục tiêu 1 và 3: thứ tự rc (2 trước 3 trước 1 trước 0), cách tiêm danh sách miễn trừ, `MIEN_TRU` là trạng thái thứ tư, khoá `--json` của cả hai công cụ, `--root` sai ⇒ rc 2 (B7 mới), glob in ra và được đo (B3, B5); B5 khai rõ giới hạn `.gitignore`. **Còn mở:** miễn trừ neo theo đường dẫn, không theo lý do trượt (review G2) — lựa chọn thiết kế chờ chủ kho, ghi ở "Ngoài phạm vi". |
| `tieu-de-nguon-va-lop-khai-ngoai-pham-vi-do` (P3) | `review_class` theo từ vựng PROTOCOL và theo cổng (đo); trần ADR-0044 khai cách xếp và lý do; hàng mới "ngưỡng chặn" trích đúng bản đọc lại của `6094652521` (của wp698); `4231959151` là `discussion_r`; mục 6 và Q4/Q7/Q9 ghi KHÔNG ĐO ĐƯỢC. |

**Ngoài HINT, r2 tự thêm** (mỗi mục có phép đo hoặc nguồn tại chỗ):

- Hàng `depends_on` và phép đo người giữ trên clone đủ ref (rc 12, bia mộ một chiều của #748).
- Chiều ngược của sổ test sống (`23/25` khi có đăng ký mà thiếu tệp) ⇒ đăng ký không tách khỏi test được.
- Vị trí đọc `landed` thành luật (r1 chỉ nêu ở "Số đo nền", HINT bỏ mất vế dự phòng mức gốc), kèm ca B1 cho `landed`
  mức gốc, ca B1b cho `trang_thai_packet` không phải ánh xạ và cho thiếu PyYAML.
- B1 thêm một ca `DAT` cho mỗi mảnh URL: trên kho thật cả 13 hồ sơ đạt dùng `#issuecomment-` (đo 08:51Z), nên bỏ
  `#pullrequestreview-` hay `#discussion_r` khỏi tập cho phép không làm B3 đổi số.
- B3 đo `--json` của công cụ land (review lớp 5 (d) nêu thiếu ca; HINT chỉ thêm khoá).
- Hàng `executor` · `reviewer` trích hệ quả assurance của lớp `sensitive` (PROTOCOL §8 dòng 612, 621, 724–726).
- B3 ghi rõ "luật L5 của `soan-spec`" để khỏi lẫn với luật L-5 của tệp này (review: quan sát, không xếp lớp).

**Chỗ r2 lệch `HINT.patch`:**

- `--root` sai ⇒ **rc 2** (lỗi tham số) ở cả hai công cụ, theo chỉ thị điều phối; HINT đặt rc 3 và chỉ cho công cụ
  HINT. Ca đo chuyển từ B5 sang B7.
- Điều kiện cấp lease: "#748 land **VÀ** `NGƯỜI_GIỮ 0`" theo quyết định chủ kho; HINT viết "land HOẶC thu hồi quyền giữ".
- `kich_thuoc` ước ≤ 900 thay vì ≤ 702 (HINT tự ghi "B1/B4 mở rộng có thể đẩy lên").
- `review_class`: HINT để "xin chủ kho xác nhận lớp review"; r2 khai `sensitive` vì cổng không cho lớp nào khác (đo),
  và chỉ xin chủ kho xác nhận CÁCH XẾP trần ADR-0044.
- Mẫu regex của hai mục `MOI` và ký tự xuống dòng trong L-6/B1 được viết bằng lời thay vì chép chuỗi có dấu chéo
  ngược: chuỗi thoát trong văn bản là thứ tầng vận chuyển có thể giải mã mất (CLAUDE.md, mục "TẦNG VẬN CHUYỂN CŨNG
  CHUẨN HOÁ CHUỖI"). Mẫu thật lấy từ chính tệp sổ (mục tiêu 5).

## Số đo nền (đo lại 08:51:36Z–08:51:40Z 15-10-2026 trên `55bd0d2` = `6f121a3` + ba tệp `ops/specs/`)

Mọi số dưới đây trùng lượt đo ~06:00Z của r1; r2 chỉ phân rã thêm.

- **Hồ sơ land:** 26 tệp `ops/land/*-land-evidence.yaml` (đơn vị: tệp). 14 tệp có `landed: true`, cả 14 ở
  `trang_thai_packet.landed`; không tệp nào có `landed` mức gốc, không tệp nào có `trang_thai_packet` khác ánh xạ.
  Với luật L-6 dưới đây: 13 đạt (cả 13 dùng mảnh `#issuecomment-`), **1 trượt** —
  `ops/land/pr672-wp574-land-evidence.yaml`: KHÔNG có `authorized_head_sha` / `authorization_url` ở MỨC GỐC (nhưng
  có `candidates[0..2].authorized_head_sha` và `authorization.human_audit` — xem L-6). 12 tệp còn lại không có khoá
  `landed` ở cả hai vị trí L-6 đọc: 11 không có `trang_thai_packet` (trong đó `pr554` mang `LANDED: 'CO. …'` và `pr594`
  mang `LANDED: 'CHUA. …'` — khoá HOA, giá trị chuỗi, L-6 không đọc), 1 (`pr684`) có `trang_thai_packet` với
  `packet_landed` mà không có `landed` ⇒ cả 12 là `BO_QUA`.
- **HINT:** 52 tệp khớp `ops/reviews/**/*HINT.patch` (đơn vị: tệp). Theo chuỗi L-5 ĐẦY ĐỦ (có ` commit`; chuỗi khoá
  `chưa chạy trên cây thật` và chuỗi cụt không có ` commit` cho cùng 15; PROTOCOL §8 "patch-as-hint", ràng buộc 1,
  `docs/PROTOCOL_DA_PHIEN.md` dòng 644–645 tại `6f121a3`, không đổi ở `55bd0d2`): 15 có nhãn, 2 tệp rỗng (0 byte:
  `thu-hoi-lease-a1a-r2/luot7-HINT.patch`, `thu-hoi-lease-a1a-r2/luot10-HINT.patch`), **35 thiếu nhãn nguyên văn** = 26
  không có nhãn + 9 tệp `ops/reviews/ci-duong-nhanh-ho-so/review-luot*-claude-HINT.patch` (lượt 08–13, 15–17; glob này
  khớp đúng 9 tệp) mang nhãn BỎ DẤU ở dòng 1 (`chua chay tren cay that — executor tu ap, tu do, tu chiu trach nhiem
  commit`). Cả 35 là bản sao nguyên byte có băm: 29 có sha256 trong 273 tệp `*.receipt.yaml`, 6
  (`thu-hoi-lease-va-cap-lai-spec/luot{1,2,3,5,6,7}-HINT.patch`) có sha256 trong `luot*-VERDICT.md`/`luot*-EVIDENCE.md`
  cùng thư mục, không có biên nhận ⇒ KHÔNG được sửa.

## Luật

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
  ĐẦY ĐỦ `chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit` (PROTOCOL dòng 644–645 ngắt
  giữa `trách nhiệm` và `commit`: nối bằng MỘT dấu cách; 15/15 tệp có nhãn đều chứa cả ` commit`) ⇒ xếp
  **`KHONG_DU_DIEU_KIEN_PATCH_AS_HINT`** (chỉ đo ràng buộc 1 của PROTOCOL §8, không đo 2 và 3); rỗng sau `strip()` ⇒
  `RONG`; có ⇒ `CO_NHAN`. Đọc UTF-8 nghiêm; giải mã lỗi VÀ mọi `OSError` (thư mục tên `*HINT.patch`, symlink treo,
  quyền) ⇒ `KHONG_DOC_DUOC` (không âm thầm `errors="replace"`, không để ngoại lệ thoát).

## Mục tiêu

1. **[`ops/kiem_ho_so_land.py`]** CLI `python ops/kiem_ho_so_land.py --root . [--json]`: quét
   `ops/land/*-land-evidence.yaml` (không đệ quy; tên tệp là QUY ƯỚC, không ADR nào đặt — in glob này ra đầu ra), in
   từng tệp `DAT`/`TRUOT`/`BO_QUA`/`MIEN_TRU` kèm lý do, tổng `n_dat/n_landed` và số `MIEN_TRU`; `--json` có `tep[]`
   (`duong_dan`, `trang_thai`, `ly_do`), `n_dat`, `n_landed`, `n_mien_tru`, `phamvi_glob`. Rc 0 khi không tệp nào trượt
   NGOÀI danh sách miễn trừ; rc 1 khi có; rc 2 lỗi tham số, kể cả `--root` không phải thư mục hoặc không chứa thư mục
   `ops/land` (kiểm TRƯỚC khi quét, không in dòng đếm nào); rc 3 khi không đọc được tệp/YAML, gốc hoặc
   `trang_thai_packet` sai kiểu, thiếu PyYAML, hoặc miễn trừ vắng. Thứ tự ưu tiên: 2 trước 3 trước 1 trước 0 — khi
   đồng thời có tệp trượt và điều kiện rc 3 thì rc 3 (không đọc được thì không có quyền kết luận "trượt"). Danh sách
   miễn trừ là hằng trong mã, mỗi mục có lý do, và hàm chính nhận nó làm tham số (test tiêm `{}` cho cây tạm không có
   `pr672`); bản land chứa đúng một mục: `ops/land/pr672-wp574-land-evidence.yaml` — lý do "hồ sơ của packet khác, ghi
   trước luật L-6; sửa ở packet riêng". Miễn trừ một tệp không tồn tại ⇒ rc 3 (danh sách không được thối).
2. **[`ops/kiem_ho_so_land_test.py`]** Bộ test tự đứng, dựng cây tạm.
3. **[`ops/kiem_nhan_hint.py`]** CLI `python ops/kiem_nhan_hint.py --root . [--json]`: liệt kê mọi tệp khớp
   `ops/reviews/**/*HINT.patch` theo L-5 (in glob này ra đầu ra), in đếm từng loại; `--json` có `tep[]`, `dem{}` theo
   bốn loại, `phamvi_glob`. Rc 0 luôn khi đọc được hết (đây là công cụ BÁO CÁO, không phải cổng); rc 2 lỗi tham số, kể
   cả `--root` không phải thư mục hoặc không chứa thư mục `ops/reviews` (0 tệp không phải là "sạch"); rc 3 khi có
   `KHONG_DOC_DUOC`. Không ghi tệp nào.
4. **[`ops/kiem_nhan_hint_test.py`]** Bộ test tự đứng, dựng cây tạm.
5. **[`.claude/dev/ci_dang_ky_test.py`]** Thêm hai mục vào `MOI`: khoá `"ops/kiem_ho_so_land_test.py"` và
   `"ops/kiem_nhan_hint_test.py"`, giá trị chép NGUYÊN mẫu regex của mục `ops/nhanh_don_duoc_test.py` (dòng 52 của tệp
   sổ tại `55bd0d2`: một dòng chỉ gồm hai số nguyên ngăn bởi `/`). Không đổi gì khác trong tệp. Hệ quả phải nói thẳng:
   sổ ấy CHẠY hai test trong job `gate-registry` (Ubuntu; thêm Windows khi PR gắn nhãn `windows` hoặc gọi tay
   `workflow_dispatch` — đầu ra `os` của job `chuan-bi`, `ci.yml`) và đòi N > 0 bằng nhau — nên "không gắn vào CI" chỉ
   đúng với `ci.yml`.

## Nghiệm thu

- **B1 (L-6 răng):** cây tạm (tiêm danh sách miễn trừ `{}`), mỗi hồ sơ `landed: true` vi phạm đúng MỘT mệnh đề.
  ⇒ `DAT`: hồ sơ đủ, một bản cho mỗi mảnh URL (`#issuecomment-`, `#pullrequestreview-`, `#discussion_r`). ⇒ `TRUOT`:
  SHA 39 ký tự · SHA viết hoa · SHA 40 hex kèm một ký tự xuống dòng ở cuối (dựng bằng khối YAML `|`) ·
  `authorized_head_sha` không phải chuỗi (số) · khoá chỉ có lồng trong `candidates[0]` (đúng hình `pr672`) · URL ngoài
  kho · URL giả dạng `https://evil.example/github.com/ducthangho/tra-luat/pull/1#issuecomment-1` · URL trong kho nhưng
  thiếu mảnh (`…/pull/721`) · hồ sơ không có `trang_thai_packet`, `landed: true` ở mức gốc, SHA viết hoa. ⇒ `BO_QUA`:
  `landed: false` thiếu cả hai; `landed: "true"` (chuỗi). Rc 1. ĐỎ khi, MỖI đột biến làm đúng ca của nó ĐỎ: nới regex
  thành `[0-9a-fA-F]{39,40}` ⇒ hai ca (SHA 39, SHA hoa); `re.match` + `$` ⇒ ca xuống dòng cuối; bỏ kiểm kiểu chuỗi ⇒
  ca số; tìm khoá theo độ sâu ⇒ ca lồng; bỏ kiểm URL ⇒ ca URL ngoài kho; kiểm URL bằng `in` ⇒ ca giả dạng; bỏ riêng
  kiểm mảnh ⇒ ca thiếu mảnh; bỏ một mảnh khỏi tập cho phép ⇒ ca `DAT` của mảnh ấy; `landed` kiểm truthy ⇒ ca chuỗi
  `"true"`; chỉ đọc `trang_thai_packet.landed` ⇒ ca `landed` mức gốc thành `BO_QUA`. (Review lượt 1 đo 15-10-2026 trên
  bản tham chiếu dựng đúng r1, SỐNG SÓT qua B1+B2+B3 của r1: bỏ riêng kiểm mảnh · kiểm URL bằng `in` · bỏ kiểm kiểu
  chuỗi · tìm khoá theo độ sâu · `landed` kiểm truthy · nuốt lỗi YAML; và SHA kèm xuống dòng cuối lọt qua `re.match` +
  `$`. Hai đột biến "bỏ một mảnh" và "chỉ đọc `trang_thai_packet.landed`" do r2 tự thêm: trên dữ liệu thật cả 13 hồ
  sơ đạt dùng `#issuecomment-` và 0 hồ sơ có `landed` mức gốc, nên B3 không phân biệt được chúng.)
- **B1b (fail-close):** YAML hỏng (ngoặc không đóng, tab thụt đầu dòng) ⇒ rc 3; tệp rỗng, gốc là danh sách,
  `trang_thai_packet` là chuỗi ⇒ rc 3; chạy công cụ trong tiến trình con có import `yaml` bị chặn
  (`sys.modules["yaml"] = None` trước khi nạp) ⇒ rc 3. Không ca nào được thành `BO_QUA` âm thầm. ĐỎ khi: đột biến nuốt
  lỗi YAML thành `BO_QUA` ⇒ ca YAML hỏng ĐỎ; để ngoại lệ thoát khi gốc là `None` ⇒ ca tệp rỗng ra rc 1 ⇒ ĐỎ; coi
  `trang_thai_packet` sai kiểu là vắng ⇒ ca chuỗi ĐỎ; nuốt `ImportError` ⇒ ca thiếu PyYAML ĐỎ.
- **B2 (miễn trừ):** hồ sơ trượt có trong danh sách miễn trừ ⇒ rc 0 và dòng `MIEN_TRU` kèm lý do; mục miễn trừ trỏ tệp vắng ⇒
  rc 3. ĐỎ khi: đột biến bỏ kiểm tồn tại ⇒ ca tệp vắng ĐỎ.
- **B3 (trên kho thật):** `python ops/kiem_ho_so_land.py --root .` tại ứng viên ⇒ rc 0, đếm `13/14 DAT` + `1 MIEN_TRU`;
  `--json` cho cùng số (`n_dat` 13, `n_landed` 14, `n_mien_tru` 1) và `phamvi_glob` bằng glob mục tiêu 1 (đo lại lúc thi
  hành theo luật L5 của `soan-spec` — khác luật L-5 của tệp này; số hạng lệch thì ghi số mới và lý do, đừng ép khớp).
  ĐỎ khi: gỡ miễn trừ ⇒ rc 1; bỏ khoá `phamvi_glob` ⇒ ĐỎ.
- **B4 (L-5 răng):** cây tạm có các tệp HINT: có nhãn đầy đủ, thiếu nhãn (một mồi chứa `chưa chạy`; một mồi chứa nhãn
  cụt `… tự chịu trách nhiệm` thiếu ` commit`), rỗng, chỉ có xuống dòng (⇒ `RONG`), byte không phải UTF-8, thư mục tên
  `x-HINT.patch` ⇒ đúng loại; rc 3 vì có `KHONG_DOC_DUOC`. ĐỎ khi: đột biến khớp nhãn bằng chuỗi rút gọn `chưa chạy` ⇒
  tệp mồi chứa `chưa chạy` mà không đủ nhãn ĐỎ; bằng chuỗi cụt bỏ ` commit` ⇒ mồi cụt ĐỎ; đột biến đọc
  `errors="replace"` ⇒ ca byte lỗi ĐỎ; đột biến để `OSError` thoát ⇒ ca thư mục ĐỎ.
- **B5 (trên kho thật, chỉ đọc):** `python ops/kiem_nhan_hint.py --root . --json` ⇒ rc 0, đếm theo loại khớp số đo nền
  (đo lại lúc thi hành), `phamvi_glob` đúng glob mục tiêu 3; `git status --porcelain` rỗng trước VÀ sau khi chạy (tệp bị
  `.gitignore` như `__pycache__` thì phép đo này KHÔNG bắt được). ĐỎ khi: công cụ ghi một tệp NGOÀI `.gitignore` ⇒
  `git status` không rỗng; bỏ khoá `phamvi_glob` ⇒ ĐỎ.
- **B6 (cổng kho):** (a) `python -B .claude/dev/ci_dang_ky_test.py` (không `--chay`; bước CI là `… --chay`, nặng, KHÔNG
  ĐO ĐƯỢC offline) ⇒ `ĐĂNG KÝ: N/N` hai số BẰNG NHAU, `TỔNG: ĐẠT`, rc 0, và `git diff --numstat` của tệp sổ là 2 dòng
  thêm, 0 dòng xoá (đo 08:52Z 15-10-2026 trên clone tạm `55bd0d2` + bốn tệp giả + hai dòng `MOI`: `ĐĂNG KÝ: 25/25`,
  `PHẢN CHỨNG: 1025/1025 đỏ đúng`, rc 0; nền `23/23`); ĐỎ khi gỡ hai dòng `MOI` ⇒ `ĐĂNG KÝ: 25/23`, `TỔNG: ĐỎ`, rc 1; ĐỎ
  khi giữ hai dòng mà thiếu hai tệp test ⇒ `23/25`, rc 1. (b) `ruff check --select F` trên bốn tệp mới: delta 0
  (multiset) so với cơ sở rỗng ⇒ 0 phát hiện (container soạn r2 có binary `ruff` 0.15.8, còn `python3 -m ruff` báo không
  có module — dùng dạng có trên máy thi hành và ghi phiên bản); ĐỎ khi chèn `import os` thừa vào một tệp mới ⇒ `F401`
  cho `os`, rc 1 (đo 09:00:18Z 15-10-2026 trên tệp nháp ngoài kho; tệp không có dòng ấy ⇒ `All checks passed!`, rc 0).
  (c) mỗi test chạy được bằng `python -B <tệp>` và in một dòng `N/N` (đơn vị: ca test; N ≥ 1, hai số bằng nhau); ĐỎ khi
  in `0/0` hoặc `N/M` với N ≠ M — đo 08:53Z: qua `chay_moi` của sổ, test in `0/0` ⇒ `CI_DANG_KY
  ops/kiem_nhan_hint_test.py: ĐỎ`, `do = 1`; `bang_chung_xanh` với `3/4` ⇒ `False`. (d) CI PR xanh — KHÔNG ĐO ĐƯỢC ngoài
  GitHub Actions; ghi run id lúc thi hành.
- **B7 (`--root` sai, cả hai công cụ):** `--root` trỏ (i) đường không tồn tại, (ii) một tệp, (iii) thư mục rỗng ⇒ rc 2
  và không in dòng đếm nào, ở cả `kiem_ho_so_land.py` lẫn `kiem_nhan_hint.py`. ĐỎ khi: đột biến bỏ kiểm `--root` ⇒ ca
  (iii) không còn rc 2 (công cụ HINT ra rc 0 với 0 tệp; công cụ land ra rc khác 2) ⇒ ĐỎ.

## Ngoài phạm vi (cố ý)

- Gắn hai công cụ vào `ci.yml` (thuộc write set #748) — ghi nợ cho packet sau #748. Đăng ký vào sổ test sống (mục
  tiêu 5) là việc KHÁC và nằm TRONG packet này: sổ ấy CHẠY hai test trong job `gate-registry`.
- Sửa `pr672-wp574` hay bất kỳ tệp HINT nào (bản sao nguyên byte có băm).
- Ghi cờ "không đủ điều kiện" vào biên nhận từng lượt — để packet khác quyết định có cần hay không.
- Ghim miễn trừ theo lý do trượt (hoặc theo sha256 tệp) thay vì theo đường dẫn: review lượt 1 đo được tệp miễn trừ đổi
  sang lỗi KHÁC vẫn `MIEN_TRU`, và tệp đã sửa đúng ⇒ `DAT` mà không cảnh báo mục thừa (G2). Lựa chọn thiết kế chờ chủ
  kho; r2 giữ miễn trừ theo đường dẫn và ghi chỗ hở này là đã biết.

## Hình dạng kế thừa

`khong_ap_dung` (công cụ mới). Chép một hình dạng có thể tái phát: **bộ lọc theo danh sách đoán trước mù đúng chỗ**
(CLAUDE.md, "Quét secrets: lọc theo PHẦN MỞ RỘNG") — glob `*HINT.patch` bỏ sót (đo 08:51Z 15-10-2026 trên `55bd0d2`:
10 tệp `.patch`/`.diff` dưới `ops/` không khớp glob, trong đó 5 mang dạng HINT/gợi ý): 3 tệp `*HINT-sanpham.diff`,
`HINT-543-luot1.patch`, `ci-g5-cong-cu-chia-manh-r1-review-20-claude-goi-y-F45.patch` (PROTOCOL §8 gọi artifact là
`goi-y-<finding>.patch`), cộng 2 tệp `hint*.json`; packet CỐ Ý chỉ phủ `*HINT.patch` (đúng phạm vi #722 nêu) và cả hai
công cụ phải in phạm vi glob trong đầu ra (B3, B5 đo việc in ấy).

## Chưa đo được

- Hồ sơ land trên nhánh `ops/**` chưa vào master: công cụ chỉ quét cây được chỉ định, không quét mọi ref.
- Người giữ `.claude/dev/ci_dang_ky_test.py`: lúc soạn r2 bộ quét trả rc 12 `KHÔNG_XÁC_ĐỊNH` (hàng `depends_on`) —
  trạng thái thứ ba, không phải "không ai giữ".
- CI thật (B6 d) và `ci_dang_ky_test.py --chay` đầy đủ: không chạy ở phiên soạn r2.
- Đường Windows: không đo được ở phiên này. Hai test được đăng ký vào `MOI` (mục tiêu 5) nên sẽ chạy trên
  `windows-latest` mỗi khi PR gắn nhãn `windows` hoặc có `workflow_dispatch` (đầu ra `os` của `chuan-bi` ở `ci.yml` @
  `55bd0d2`; lượt push master chỉ có ubuntu). Viết test không phụ thuộc nền: khoá miễn trừ so bằng `as_posix()`,
  fixture ghi bằng `encoding="utf-8"` với `newline` ép về một ký tự LF (không để nền tự đổi sang CRLF).
