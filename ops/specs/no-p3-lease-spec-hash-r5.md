# Đặc tả packet `no-p3-lease-spec-hash` r5 — revision DELTA trên r4: dời nền, đo lại, giữ thiết kế

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-lease-spec-hash` |
| `packet_issue` | #751 (đọc 03:11:42Z 26-10-2026: `open`, `updated_at 2026-10-26T02:50:01Z`). |
| `revision` | 5 |
| `dang_revision` | **DELTA.** Quyết định chủ kho: https://github.com/ducthangho/tra-luat/issues/751#issuecomment-6407123228 (`ducthangho`, `OWNER`, `created_at 2026-10-26T02:50:01Z`), mục 3: *"Đổi nền theo `depends_on` (3) bằng một revision DELTA trên r4: giữ nguyên thiết kế và tiêu chí; nền mới là `master` lúc soạn; đo lại ba bộ đo nền, quần thể lease/A6 và các số phụ thuộc `.claude/dev/ci_dang_ky_test.py`, `ops/ci_duong_nhanh_test.py`"*. Luật đọc ở mục **Luật đọc delta** ngay dưới bảng này. |
| `thay_the_cho` | **r4**: `ops/specs/no-p3-lease-spec-hash-r4.md`, sha256 `40c88b13806e285b1d85961ed9ff99ed89ed2108cdca94d0d8dd6177de0530fd`, blob `d0ba32d208e437e9124be6e1b97d72cfa70ac6f1`, 759 dòng, commit cuối sửa nó `77d4e0a` (vá finding Codex PR #908). Tìm ở `master` trước (đo 03:10Z 26-10-2026: `git show origin/master:<tệp> \| sha256sum` ra đúng băm trên, `master` = `f9f4a8d`); không thấy thì hỏi phiên điều phối. Thứ định danh r4 là băm, không phải tên nhánh hay vị trí tệp. r5 không sửa byte nào của r1–r4. Mọi closure, lease và `spec_hash` từ nay neo **r5**. |
| `review_class` | **sensitive**, như r4. Trần như r4: dòng `tran_kich_thuoc_sensitive` dưới bảng giữ nguyên; ba phép đo OID `8ab1007…` đo lại 03:17:47Z 26-10-2026, dưới hợp đồng môi trường đo, trên bản bare MỚI của `depends_on` (2) (`rev-parse --is-shallow-repository` ra `false`, `master` máy chủ `f9f4a8d`): rc 0 · rc 128 · rc 0. Lời khai "Không cổng nào canh trần" đo lại trên sáu tệp cổng tại `f9f4a8d` (03:13:56Z 26-10-2026): `ADR-0053` `0053` `tran_kich_thuoc_sensitive` `450` ra 0 dòng ở cả sáu; `nang_tran` `ai_nang` `tran_cu` `tran_moi` ra 0 ở năm tệp, 8 · 4 · 2 · 5 ở `.claude/dev/packet_loop.py` — y như r4. Số dòng `docs/PROTOCOL_DA_PHIEN.md` mà r4 dẫn: §20 dòng 1514, 1522 → **1521, 1529**; sáu tệp cổng dòng 1473–1474 → **1480–1481** (bảng ánh xạ ở mục Đo lại). |
| `executor` · `reviewer` | Như r4. Số dòng PROTOCOL mà hàng ấy của r4 dẫn (tại `1d7e642`): §8 dòng 712–714 → **719–721**, dòng 703 → **710**, dòng 712–713 → **719–720**; cùng chữ. `.claude/dev/chon_reviewer.py` không đổi từ `1d7e642`; chạy lại tại `f9f4a8d` (03:12Z 26-10-2026, `--review-class sensitive --luot 1`, ba đường dẫn write set dạng dấu phẩy): `--so-dong` 300 · 399 ⇒ `claude-fable-5`/`xhigh`, "tổng=4"; 400 · 450 ⇒ `claude-fable-5`/`max`, "tổng=5" — y như r4. |
| `base` | `f9f4a8d6da2d351fbcf5203256aba4e1bbf027b7` (merge PR #941) — `master` máy chủ lúc soạn (fetch 03:11Z 26-10-2026). Phép đo dài chạy trên `47cd346358c20c29495a281fde27ba3e3cadde30` (merge PR #938, `master` lúc bắt đầu đo, 02:49:41Z) VÀ ba bộ đo nền chạy lại trên `f9f4a8d`. `git diff --name-only 47cd346 f9f4a8d` ra đúng 3 tệp, cả ba dưới `ops/land/pr881-wp852-*` (hồ sơ land, không phải lease, spec, công cụ hay workflow); `git diff --quiet 47cd346 f9f4a8d -- ops/leases ops/specs .claude .github ops/lease_publish.py` rc 0. Nên số đo A6 và A7 trên `47cd346` đúng nguyên cho `f9f4a8d`. Từ `1d7e642` (nền r4) tới `f9f4a8d`: 46 merge first-parent. `git diff --numstat 1d7e642 f9f4a8d`: ĐỔI `.claude/dev/ci_dang_ky_test.py` +20/−6 (write set VÀ bộ đo nền), `ops/ci_duong_nhanh_test.py` +39/−15 (bộ đo nền), `.github/workflows/ci.yml` +14/−7, `docs/PROTOCOL_DA_PHIEN.md` +13/−4, `ops/reviews/README.md` +22/−0, cùng hai ADR mới `0055`, `0056`; KHÔNG ĐỔI (blob bằng nhau) `ops/lease_publish.py`, `ops/lease_publish_test.py`, `.github/workflows/ops-publish-lease.yml`, `ops/ci_duong_nhanh.py`, `ops/README.md`, `.claude/dev/chon_reviewer.py`, `.claude/skills/soan-spec/SKILL.md`, ADR-0053. r5 KHÔNG đuổi theo `master`; luật lúc cấp ở `depends_on` (3). |
| `write_set` | Như r4, không đổi: `ops/lease_publish.py` · `ops/lease_publish_spec_hash_test.py` (MỚI) · `.claude/dev/ci_dang_ky_test.py` (+1 dòng `MOI`, Mục tiêu 6). Chủ kho xác nhận bằng chữ ở comment `6407123228`, mục 1. |
| `depends_on` | **CHẶN cấp lease** cho tới khi ĐỦ năm điều kiện của r4, đo lại lúc cấp. Hiện trạng lúc soạn r5 (02:49Z–03:20Z 26-10-2026): **(1)** ĐÃ, như r4. **(2) ĐỎ** — đo 03:17:34Z–03:19:42Z dưới hợp đồng môi trường đo (bước mạng chỉ thêm `HTTPS_PROXY`), trên một bản bare MỚI (`git clone --bare --reference` kho cục bộ từ `https://github.com/ducthangho/tra-luat`, rồi MỘT lệnh `fetch --prune origin '+refs/heads/*:refs/heads/*' '+refs/heads/*:refs/remotes/origin/*'`; `adg_r5.sh`): 619 nhánh máy chủ, `master` `f9f4a8d`; so tập tên + OID với cả `refs/remotes/origin` (619) lẫn `refs/heads` (619): thiếu 0, thừa 0; `remote get-url origin` ra đúng URL trên; `rev-parse --is-shallow-repository` ra `false`. Kết quả: `ops/lease_publish.py` `NGƯỜI_GIỮ 0` rc 0 (03:17:36Z); `ops/lease_publish_spec_hash_test.py` `NGƯỜI_GIỮ 0` rc 0 (03:18:03Z); **`.claude/dev/ci_dang_ky_test.py` `NGƯỜI_GIỮ 1: wp899-r4-g5-claude`, rc 11** (03:18:26Z) — lease g5 của #899 (nhánh `ops/wp899-r4-g5-lease` @ `5c67f1d2`, commit 02:10:34Z 26-10-2026, `lease_until 2026-10-28T02:26:00Z`, `spec_path ops/specs/wp899-r4.md`, `base_sha ba222ff`; `write_set_ghi_chu` khai thêm đúng MỘT dòng `MOI` cho `ops/ci_provenance_test.py`). Cùng lượt in `CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ` cho `wp899-r1-g1-claude` và `wp899-r4-g3-claude`, không tính là người giữ. Hai bộ đo nền còn lại và `ci.yml`: `NGƯỜI_GIỮ 0` rc 0 (03:18:51Z–03:19:42Z). Một lượt trước, 03:06:33Z, trên clone đủ ref CÓ cây làm việc và NGOÀI hợp đồng, ra cùng sáu kết quả; lượt ấy không dùng làm bằng chứng. Lease thực thi của #751 CHỜ `wp899-r4-g5-claude` hết hạn, bị thu hồi hoặc #899 land; đo lại (2) lúc cấp. **(3) đã kích hoạt lần HAI** và được xử bằng chính r5: `1d7e642..f9f4a8d` đổi `.claude/dev/ci_dang_ky_test.py` và `ops/ci_duong_nhanh_test.py` (hàng `base`). Luật lúc cấp giữ nguyên chữ r4, thay `1d7e642` bằng `f9f4a8d`: commit nào sau `f9f4a8d` trên `master` đổi một tệp write set hoặc một bộ đo nền ⇒ không cấp trên nền `f9f4a8d`, dời nền bằng revision mới. Hệ quả biết trước: #899 land trước lúc cấp thì sổ đổi (+1 dòng `MOI`) ⇒ (3) kích hoạt lần ba. **(4)** #763 ĐÃ land: PR #930, merge `36057e8` vào `master` (Issue #763 vẫn `open` lúc 03:11:42Z 26-10-2026 — đóng Issue là việc chủ kho); đúng như r4 đoán trước, N = 26 ⇒ đích A7 `27/27`. #892 `closed`/`completed` lúc 2026-10-24T03:46:08Z; lease của nó không còn giữ đường dẫn nào của write set (ô (2)). Luật của (4) đọc rộng như r4 viết cho mọi packet giữ sổ: không lease nào của #751 đồng thời với một lease còn hiệu lực khác giữ `.claude/dev/ci_dang_ky_test.py` — hiện là `wp899-r4-g5-claude`. **(5) ĐÃ**: comment chủ kho `6407123228` (mục 1: quyết định 15-10 về sổ test sống; mục 2: đồng ý đi tiếp ở ngưỡng L4, kèm điều kiện "mỗi chốt mới của `kiem_bam` có một ca test và một đột biến riêng", và "gặp thêm finding P1/P2 cùng hình dạng (a) hoặc A thì executor DỪNG và hỏi"). |
| `kich_thuoc` | Như r4 (3 tệp, ≤ 450 dòng thêm; các số đo kích thước của r4 làm trên `ops/lease_publish.py` không đổi). Một khác biệt: sổ `.claude/dev/ci_dang_ky_test.py` đổi nội dung nhưng phần r5 thêm vào vẫn là +1/−0 (đo A7 dưới: `git diff --numstat` của sổ ra `1 0`). |

tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544

## Luật đọc delta

1. Thân đặc tả của packet này là **r4 (băm ở hàng `thay_the_cho`) cộng tệp này**. Mọi mục của r4 mà tệp này không nhắc thì áp
   NGUYÊN VĂN: Mục tiêu 1–6, Nghiệm thu A0–A7 (gồm luật L6 chung ở đầu Nghiệm thu), Ngoài phạm vi, Hình dạng kế thừa, Chưa đo
   được, và các mục "Vá sau review" làm lịch sử.
2. Chỗ nào r4 và tệp này nói khác nhau, **tệp này thắng**. Riêng ba thứ thay theo luật, không cần nhắc lại từng chỗ:
   (a) mọi chữ "nền lúc cấp" / `<nền>` trong Nghiệm thu là `f9f4a8d`, không phải `1d7e642`; (b) mọi số dòng r4 dẫn vào năm tệp
   đã đổi được dời theo **bảng ánh xạ dòng** ở mục Đo lại; (c) mọi SỐ ĐO nền trong r4 (ca, phản chứng, đột biến, quần thể lease,
   A6, A7) bị thay bởi số ở mục Đo lại — số cũ của r4 còn đúng cho `1d7e642` và giữ làm lịch sử.
3. Thiết kế, write set, yêu cầu của Mục tiêu 1–6 và **40 ca** của r4 giữ nguyên. Tiêu chí nào trong r4 viết theo dạng tương đối
   (A7: đích `N+1/N+1` với N đo ở nền lúc cấp) đọc theo chữ ấy; các con số tuyệt đối dưới đây là N đo ở `f9f4a8d`.
4. Lease thực thi neo `spec_path` = tệp này, `spec_hash` = sha256 byte của blob tệp này. Executor đọc CẢ r4 (lấy theo băm) lẫn r5;
   reviewer đo băm cả hai trước khi đọc.

## Thay đổi so với r4

- **Nền** `1d7e642` → `f9f4a8d` (`master` lúc soạn), theo `depends_on` (3) và comment chủ kho `6407123228` mục 3. r5 không đuổi theo `master`.
- **`depends_on`**: (2) người giữ sổ nay là `wp899-r4-g5-claude` (thay `wp892-r2-g2-claude` của r4); (3) kích hoạt lần hai, xử bằng r5; (4) #763 đã land qua PR #930, #892 đã đóng; (5) ĐÃ.
- **Số đo nền** đo lại (mục Đo lại): sổ `ĐĂNG KÝ` 24/24 → **26/26**, `PHẢN CHỨNG` 1064 → **1070**; `ci_duong_nhanh_test` `DOT BIEN` 384 → **392**; `lease_publish_test` giữ 267/267; ruff F giữ 2 F841 dòng 198–199 (phiên bản ruff 0.15.8 → 0.16.9).
- **A7**: N = 26 ⇒ đích **`27/27`** (r4 đã đoán đúng nhánh "#763 land trước"); bỏ dòng `MOI` ⇒ sổ `27/26`, `ci_duong_nhanh_test` `103/104` · `391/392`.
- **A6**: số tuyệt đối không đổi so với r4 (quần thể `ops/leases/` tại `f9f4a8d` cho cùng 171 tệp và cùng phân bố rc); tập đổi rc vẫn đúng một lease.
- **Trục lời gọi Codex — dòng khai MỚI** `tran_loi_goi_codex: ADR-0055@d2e3052…` (dưới bảng đầu). r4 KHÔNG có dòng khai nào ⇒ PR thực thi của #751 chịu trần **hai** lời gọi (ADR-0055 mục "Vì sao": *"Một đặc tả không khai vẫn chịu trần hai sau ADR này"*). Dòng này bật trần mười của ADR-0055 cho PR ấy. OID `<L>` = `d2e3052d479d140b7e7b91df41ec4914fab7d544` (merge PR #926, packet wp919); ba phép đo của ADR-0055 mục Hiệu lực, 03:17:47Z 26-10-2026, dưới hợp đồng môi trường đo, trên bản bare MỚI của `depends_on` (2) (`rev-parse --is-shallow-repository` ra `false`, `master` máy chủ `f9f4a8d`): `git cat-file -e <L>:docs/adr/0055-tran-loi-goi-codex-len-muoi.md` rc 0 · cùng phép trên `<L>^1` rc 128 · `<L>` nằm trong `git rev-list --first-parent origin/master` rc 0. **Đây là thay đổi quản trị duy nhất của r5, ngoài lời giao "giữ nguyên thiết kế và tiêu chí"** — khai thẳng để chủ kho gạch nếu không muốn; gạch thì PR thực thi về trần hai lời gọi.
- **Số dòng** dẫn vào năm tệp đã đổi: dời theo bảng ánh xạ (mục Đo lại). Không mục nào của r4 dẫn vào một dòng mà `1d7e642..f9f4a8d` SỬA (cột `ĐỔI` của bảng); mọi dòng r4 dẫn chỉ dời chỗ, cùng chữ (kiểm từng neo ở bảng "Neo đã kiểm").

## Đo lại nền tại f9f4a8d

Phiên điều phối Claude đo; đây KHÔNG phải một lượt review. Lệnh chạy dưới hợp đồng môi trường đo của r4 nguyên văn, trừ các phép kê ở độ lệch (5)
(`env -i PATH="$B:/usr/bin:/bin" HOME=$(mktemp -d) GITHUB_REPOSITORY=o/r`, `$B` là thư mục symlink tới đúng năm công cụ
`python3` `git` `actionlint` `shellcheck` `ruff`); bước cần mạng chỉ thêm biến proxy; trạng thái Issue đọc bằng REST (miễn trừ của
hợp đồng). Phiên bản: Python 3.11.17 + PyYAML 6.0.1, git 2.43.0, actionlint 1.7.7, shellcheck 0.9.0 (wheel `shellcheck-py`), ruff
0.16.9. Giờ UTC, mọi mốc là 26-10-2026.

Độ lệch so với chữ r4, khai thẳng: (1) như r4, `ai-dang-giu` quét `refs/heads/*` của bản bare, nên mọi lần fetch dùng
`'+refs/heads/*:refs/heads/*' '+refs/heads/*:refs/remotes/origin/*'` trong cùng một lệnh; (2) A6 dùng `kiem_bam` THĂM DÒ dựng từ
chữ Mục tiêu 1, 2, 5 ngay trong kịch bản, như r4; A7 dùng tệp THẾ CHỖ `ops/lease_publish_spec_hash_test.py` một dòng
`print("1/1")`, như r4; không bản nào được giao; (3) A6 và A7 chạy trên `47cd346`, đúng bằng `f9f4a8d` trên mọi tệp chúng
đọc (hàng `base`); ba bộ đo nền chạy trên CẢ HAI và ra cùng số; `m_cay.py` chạy thẳng trên `f9f4a8d`; (4) `m_cay.py` chạy lại trên `1d7e642` (03:16:20Z) tái lập
đúng số cũ của r4 (171 · 118/18/113/5 · 6, 6/6 · 67, 4/67 · 61/5) — kịch bản có đáp án đã biết. (5) Năm phép
KHÔNG đi qua `$B`: `do_a6.py` chạy bằng `env -i PATH=/usr/bin:/bin HOME=<tạm> GITHUB_REPOSITORY=o/r /usr/local/bin/python3` (đúng
hợp đồng trừ thư mục `$B`); `m_cay.py` và `git grep` trên sáu tệp cổng chạy trong môi trường phiên, chỉ đọc blob git;
`chon_reviewer.py` chạy bằng `env -i PATH=/usr/bin:/bin`, không có `GITHUB_REPOSITORY`; Issue đọc bằng REST. Bốn phép đầu ra đúng
số r4 đã đo dưới hợp đồng; A7, ba bộ đo nền, `depends_on` (2) và các phép OID chạy đúng hợp đồng.

| mục (đơn vị) | r4, nền `1d7e642` | r5, nền `f9f4a8d` | lúc đo | lệnh hoặc kịch bản |
|---|---|---|---|---|
| `ops/lease_publish_test.py` (ca) | 267/267 | **267/267** (`đã chạy=267, bỏ qua=0`) — trên `47cd346` và trên `f9f4a8d` | 02:49:41Z–02:56:10Z · 03:11:20Z–03:17:32Z | `python3 -B ops/lease_publish_test.py` (`do_nen.sh`) |
| sổ: `ĐĂNG KÝ` (đường dẫn test) · `TRẠNG THÁI` · `PHẢN CHỨNG` (ca) · `TỔNG` | 24/24 · `chan=24` · 1064/1064 · `ĐẠT` | **26/26** · `chan=26 cach_ly=0` · **1070/1070** · `ĐẠT`, rc 0 | 03:11:20Z–03:11:27Z | `python3 -B .claude/dev/ci_dang_ky_test.py` |
| `ci_duong_nhanh_test`: `CA` · `DOT BIEN` · `TONG` | 104/104 · 384/384 · `DAT` | **104/104** · **392/392** · `DAT`, rc 0 — trên `47cd346` và trên `f9f4a8d` | 03:11:20Z–03:14:16Z | `python3 -B ops/ci_duong_nhanh_test.py` |
| ruff F trên `ops/lease_publish.py` (lỗi) | 2 F841, dòng 198–199 (ruff 0.15.8) | 2 F841, dòng 198–199 (`executor_surface`, `executor_transport`; ruff 0.16.9) | 03:11:20Z | `ruff check --isolated --select F ops/lease_publish.py` |
| `ops/leases/*.yaml` (tệp) | 171 | 171 (thư mục không đổi: `git diff --quiet 1d7e642 f9f4a8d -- ops/leases` rc 0) | 03:16:22Z | `m_cay.py` |
| có `spec_path` + băm · cả hai trường · khớp · lệch (lease) | 118 · 18 · 113 · 5 | 118 · 18 · 113 · 5 | 03:16:22Z | `m_cay.py` |
| `write_set_hash`: có scope, khớp · không scope, khớp (lease) | 6, 6/6 · 67, 4/67 | 6, 6/6 · 67, 4/67 | 03:16:22Z | `m_cay.py` |
| mang `spec_sha256` · không kèm hai tên kia (lease) | 61/171 · 5/171 | 61/171 · 5/171 | 03:16:22Z | `m_cay.py` |
| A6 nền (lease theo rc) | `{0: 157, 8: 9, 10: 5}` | `{0: 157, 8: 9, 10: 5}` | 02:57:33Z–03:01:16Z | `do_a6.py` |
| A6 ứng viên · tập đổi rc | `{0: 156, 8: 9, 10: 5, 13: 1}` · {`gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906` 0 → 13} | CÙNG phân bố · CÙNG tập | 02:57:33Z–03:01:16Z | `do_a6.py` |
| A6 miễn bia mộ · kiểm spec khớp · kiểm write set khớp · đột biến bỏ miễn đổi rc (lease) | 46 · 66 · 4 · 5 | 46 · 66 · 4 · 5, cùng năm tên (`gate-tach-job-cat-chi-phi-exec-1`, `-1r2`, `-1r3`, `-1r4` `-claude-20260906`, `wp461-be-mat-thu-hai-cua-codex-exec-1-claude-20260907`) | 02:57:33Z–03:01:16Z | `do_a6.py` |
| A7 đích `ĐĂNG KÝ` (đường dẫn test) | N = 24 ⇒ 25/25; #763 trước ⇒ 27/27 | **N = 26 ⇒ 27/27**. Tệp thế chỗ + dòng `MOI` chép bằng kịch bản từ dòng mẫu `"ops/nhanh_don_duoc_test.py"`: `ĐĂNG KÝ: 27/27`, `chan=27`, `PHẢN CHỨNG: 1070/1070`, `TỔNG: ĐẠT`, rc 0; `git diff --numstat` của sổ `1 0`; `chay_moi` cho khoá mới trả 0, in `CI_DANG_KY ops/lease_publish_spec_hash_test.py: ĐẠT rc=0` | 03:02:27Z | `do_a7.sh` |
| A7 bỏ dòng `MOI`: sổ · `ci_duong_nhanh_test` | 25/24, `ĐỎ` · 103/104, 383/384, `DO`, `k01_…` ĐỎ | **27/26**, `TỔNG: ĐỎ`, đúng một dòng `ĐỎ:`, rc 1 · **103/104**, **391/392**, `TONG: DO`, rc 1, `k01_so_dang_ky_nhan_muc_da_noi` ĐỎ (`test sống chưa đăng ký: ops/lease_publish_spec_hash_test.py`) | 03:02:28Z · –03:06:20Z | `do_a7.sh`, tệp thế chỗ, không dòng `MOI` |
| A7 tệp thế chỗ + `MOI`: `ci_duong_nhanh_test` | 104/104 · 384/384 | **104/104** · **392/392** · `TONG: DAT`, rc 0 | –03:06:20Z | `do_a7.sh` |
| blob lease ở đầu nhánh (blob) · nhánh | 680 · 559 | **704 · 618** (bỏ nhánh đặc tả `claude/spec-no-p3-r3`, `-r4`, `-r5`) | 03:13:06Z | `m_ref2.py` |
| phân hoạch blob: cả hai trường · `spec_path`+`spec_hash` · `spec_path`+`spec_sha256_required` · `spec_hash` không `spec_path` · `spec_path` không băm · `spec_path: null` · không cả hai | r4 chỉ ghi nhóm đầu: 62 | 80 · 376 · 55 · 15 · 56 · 27 · 95 (tổng 704; 3 trong nhóm cuối mang `spec_hash: null`) | 03:13:06Z | `m_ref2.py` |
| cả hai trường: bằng nhau · khác · chưa hết hạn · sai dạng (blob) | 62: 60 · 2 · 4 · 0 | 80: **78 · 2** (`wp709-exec-g1-codex-20261005`, `wp709-exec-g2-codex-20261006`) · **6** · **0**; toàn bộ 704 blob: chưa hết hạn 9, không đọc được hạn 0, lỗi đọc 0 | 03:13:06Z | `m_ref2.py` (hạn = `lease_expires_at_utc` hoặc `lease_until`, so với giờ chạy) |
| `ai-dang-giu` ba đường dẫn write set (rc) | 0 · 0 · 11, `wp892-r2-g2-claude` | 0 · 0 · **11, `wp899-r4-g5-claude`** | 03:17:36Z–03:18:26Z | `python3 -B ops/lease_publish.py ai-dang-giu <đường dẫn> --root <bản bare>` (`adg_r5.sh`) |
| `ai-dang-giu` `ci.yml` · `lease_publish_test.py` · `ci_duong_nhanh_test.py` (rc) | 11 · 0 · 11 | 0 · 0 · 0 | 03:18:51Z–03:19:42Z | cùng lệnh |
| nhánh máy chủ · thiếu/thừa so `refs/remotes/origin` · so `refs/heads` | 563 · 0/0 · 0/0 | 619 · 0/0 · 0/0; `remote get-url origin` đúng URL | 03:17:36Z | `ls-remote --heads` so `for-each-ref`, tập tên + OID |
| ba phép đo OID ADR-0053 · ADR-0055 (rc) | 0 · 128 · 0 · (không khai) | 0 · 128 · 0 · **0 · 128 · 0** | 03:17:47Z | `git cat-file -e`, `git rev-list --first-parent` trên bản bare của (2) |
| tên khái niệm ADR-0053 trên sáu tệp cổng §20 (dòng) | 0 cho bốn tên; 8 · 4 · 2 · 5 ở `packet_loop.py` | như r4 | 03:13:56Z | `git grep -c -w -F` trên cây `f9f4a8d` |
| bộ chọn reviewer theo `--so-dong` 300 · 399 · 400 · 450 | tổng 4 · 4 · 5 · 5 | như r4 | 03:12Z | `chon_reviewer.py` |
| Issue #751 · #763 · #892 · #899 | `open` · `open` · `open` · — | `open` · `open` · `closed`/`completed` 2026-10-24T03:46:08Z · `open` | 03:11:42Z | REST `issues/<số>` |

**Không đo lại ở r5**, kèm lý do — số của r4 đứng cho các hàng này:
hàng (g) `bang_chung_xanh` (thân hàm giống hệt qua AST giữa `1d7e642` và `f9f4a8d`, chỉ dời dòng 677 → 679);
nguồn đọc `check` sáu ca, dòng dài nhất, `--help` chứa `MÃ THOÁT`, năm tên trong `lease_publish.py` (cả `ops/lease_publish.py` lẫn
`ops/lease_publish_test.py` byte-identical với `1d7e642`);
A6 (ii) và A6b trên bản thăm dò (bản thăm dò dựng trên `ops/lease_publish.py` không đổi, chạy `ops/lease_publish_test.py` không đổi);
blob `verdict` khớp `d3f1d9db…` và mục cây khớp VERDICT/HINT r2 (hàng `nguon_cap_viec`, `review của r2` của r4 — lời khai lịch sử,
không phụ thuộc nền; chưa đo trên tập nhánh 618);
chạy thử L6 trên nền và trên bản thăm dò (A1, A2 (4), A4, A5 (1), A5b, A6b) — các tiêu chí ấy đọc `ops/lease_publish.py` và bộ test mới,
không đọc hai tệp đã đổi.
Thứ ĐÃ đổi so với r4 trong vùng này chỉ có sổ và `ci_duong_nhanh_test`, nên mọi tiêu chí dựa trên chúng (A7) đã đo lại ở bảng trên.

### Bảng ánh xạ dòng `1d7e642` → `f9f4a8d`

Dựng từ hunk của `git diff -U0 1d7e642 f9f4a8d -- <tệp>` (`anh_xa.py`). Đọc: "a–b +d" là dòng cũ a…b nay ở a+d…b+d, cùng chữ;
"a ĐỔI → c" là dòng cũ a bị sửa, nay là c.

- `.claude/dev/ci_dang_ky_test.py` (2428 dòng cũ): 1–53 +0 · 54–802 +2 · 803 ĐỔI → 805 · 804 +2 · 805 ĐỔI → 807 · 806–1170 +2 ·
  1171–1174 +3 · 1175–1202 +5 · 1203 ĐỔI → 1208 · 1204–1235 +5 · 1236 ĐỔI → 1241–1242 · 1237–1267 +6 · 1268 ĐỔI → 1274–1275 ·
  1269–2025 +7 · 2026–2284 +14 · 2285 ĐỔI → 2299 · 2286–2428 +14.
- `ops/ci_duong_nhanh_test.py` (3723 dòng cũ): 1–2135 +0 · 2136–2139 +8 · 2140–2141 ĐỔI → 2148–2152 · 2142–2150 +11 ·
  2151–2152 ĐỔI → 2162–2164 · 2153–2288 +12 · 2289 ĐỔI → 2301 · 2290 +12 · 2291 ĐỔI → 2303 · 2292 +12 · 2293–2294 ĐỔI → 2305–2306 ·
  2295 +12 · 2296–2297 ĐỔI → 2308–2309 · 2298–2357 +12 · 2358 ĐỔI → 2370 · 2359–2423 +12 · 2424 ĐỔI → 2436 · 2425–3265 +12 ·
  3266 ĐỔI → 3278–3290 · 3267 +24 · 3268 ĐỔI → 3292 · 3269–3284 +24 · 3285 ĐỔI → 3309 · 3286–3723 +24.
- `.github/workflows/ci.yml` (1070 dòng cũ): 1–124 +0 · 125 ĐỔI → 125 · 126–515 +0 · 516–517 +2 · 518–623 +3 · 624–640 +6 ·
  641 ĐỔI → 647 · 642–727 +6 · 728 ĐỔI → 734 · 729–875 +6 · 876 ĐỔI → 882 · 877–947 +6 · 948 ĐỔI → 954–955 · 949–955 +7 ·
  956 ĐỔI → 963 · 957–1023 +7 · 1024 ĐỔI → 1031 · 1025–1070 +7.
- `docs/PROTOCOL_DA_PHIEN.md` (1558 dòng cũ): 1–267 +0 · 268–277 +1 · 278 ĐỔI → 279–284 · 279–283 +6 · 284 ĐỔI → 290–291 ·
  285–1486 +7 · 1487 ĐỔI → 1494 · 1488–1520 +7 · 1521 ĐỔI → 1528 · 1522–1523 +7 · 1524–1558 +9.
- `ops/reviews/README.md` (1162 dòng cũ): 1–696 +0 · 697–982 +18 · 983–1162 +22 — dòng 414, 445, 484 mà r4 dẫn không dời.

### Neo đã kiểm (đọc tệp tại `f9f4a8d`; hàm so thân qua AST)

`.claude/dev/ci_dang_ky_test.py`: `MOI` 38–55 → **38–57** (thêm hai mục của #763 sau dòng mẫu); dòng mẫu `"ops/nhanh_don_duoc_test.py"`
vẫn **53**; `DANG_KY` 82 → **84**; `_git_bo_qua` 85 → **87**; `tim()` 104 → **106**; `kiem()` 640 → **642**; `bang_chung_xanh` 677–681 →
**679–683** (`re.search` 678 → **680**); `chay_moi` 1055 → **1057** — năm thân hàm giống hệt qua AST. `.github/workflows/ci.yml`: job
`gate-registry` 937 → **943**, `--chay` 1008 → **1015**, đầu ra `os` 65–70 không dời. `docs/PROTOCOL_DA_PHIEN.md`: 655–656 → **662–663**,
703 → **710**, 712–714 → **719–721**, 1473–1474 → **1480–1481**, §20 1514 → **1521**, 1522 → **1529**; cùng chữ. `ops/lease_publish_test.py`:
không dời (tệp không đổi).

Kịch bản đo — KHÔNG có trong kho, nằm trong scratchpad của phiên điều phối và mất khi phiên đóng; sha256, 12 ký tự đầu:
`do_nen.sh` `60f4701fd722…` (nền `47cd346`) và `b37eff71e2c5…` (nhận OID nền làm đối số; chạy trên `f9f4a8d`) · `m_cay.py` `4bc64195ec92…` ·
`do_a6.py` `aea18082649a…` · `do_a7.sh` `dd39fe76c411…` · `m_ref.py` `75ca0db33586…` (lượt 03:08:59Z, cùng phân hoạch) ·
`m_ref2.py` `eae59f95ed88…` (thêm đếm hạn) · `anh_xa.py` `71e8830f9956…` · `adg_r5.sh` `6a309d4979ac…`. Bên thứ ba tái lập từ định nghĩa ở từng hàng và ở r4.

Hệ quả đo được cho tiêu chí (ghi để người duyệt quyết, KHÔNG thiết kế lại ở đây): tập đổi rc của A6 (i) không đổi; đích A7 thành
`27/27`; `depends_on` (2) vẫn ĐỎ vì `wp899-r4-g5-claude`, và lease ấy sẽ thêm một dòng `MOI` vào sổ nên #899 land trước lúc cấp thì
(3) kích hoạt lần ba (N = 27 ⇒ đích `28/28`).
