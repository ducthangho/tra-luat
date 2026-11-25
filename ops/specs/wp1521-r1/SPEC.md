# wp1521 r1 — nợ B1a: `KHE_1460` báo ĐỎ trên nền không có khe chưa đo + lượt 249 đột biến của Nghiệm thu 1 chỉ chạy khi khoá đổi (NO-B1A-N2)
packet_id: wp1521
revision: 1
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
mission_issue: 1172
packet_issue: 1521
risk: sensitive
review_class: sensitive
executor: claude
environment: cloud (Linux)

Trạng thái: bản nháp r1 do phiên điều phối nợ Claude Code `session_015GtxrcVQUG6jMhjTW3bXYg` soạn ngày 2026-11-25. Chưa review, chưa duyệt băm, chưa có lease. Ba quyết định của chủ kho ghi ở mục "Sổ quyết định". Mission chưa ghi revision cho packet này.

## Mục tiêu
Đóng hai khoản nợ của B1a #1460 (hồ sơ `ops/land/pr1516-wp1460-land-evidence.yaml`, mục `no_ngoai_pham_vi`, khoản 3 và 5). Không đổi hợp đồng `bien_nhan_audit.v1`.
- **K3.** Trên nền mà ca quét biên không chạm được giới hạn đệ quy, các ca và mutant gắn `KHE_1460` hiện tự biến mất, không báo gì. Sau packet này, nền ấy làm gate ĐỎ, trừ khi nền ấy nằm trong danh sách cho phép kèm phép đo đã ghi.
- **K5.** `.claude/dev/ci_dang_ky_test.py --chay` không còn chạy 249 đột biến của khối «Lệnh kiểm» ở mỗi lượt. Lượt thường chạy khối ấy KHÔNG có `--dot-bien`. Lượt đầy đủ chỉ chạy khi khoá của môi trường đo không có trong bản ghi đã ghim.

## Hợp đồng

### 1. K3 — từ cổng theo PHIÊN BẢN sang cổng theo PHÉP ĐO
Hiện trạng tại base: `KHE_1460 = sys.version_info < (3, 14)`. Hằng này gắn hai ca `wp1460-thu-quet-bien-de-quy-{dau-job,bien-nhan-xanh}`, hai mục bảng đột biến `thu-quet-bien-de-quy-*`, và ba mutant `f02r3-*`.
- **1a. Bỏ cổng phiên bản.** Hai ca quét biên được đăng ký trên MỌI nền. Hàm `quet_bien` giữ nguyên định nghĩa đạt: ở mọi độ sâu lệnh thu thoát 1 kèm biên nhận không xanh hợp lệ, VÀ `tran > 0`.
- **1b. Nền không có khe.** Nếu ở cả hai ca `tran == 0` (quét không làm `is_valid` thật ném), thì kết quả tra trong một hằng mới `KHONG_KHE_1460`. Đây là danh sách cho phép, khoá là `(major, minor, micro)` của `sys.version_info` và phiên bản `jsonschema`; giá trị là chuỗi trỏ tới phép đo (đường dẫn tệp hoặc URL run, kèm ngày).
  - Có trong danh sách ⇒ ca in đúng một dòng `BỎ QUA wp1460-thu-quet-bien-de-quy-<t>: nền <v> · jsonschema <j> không có khe (đo: <giá trị>) · tran 0/<số độ sâu đã quét>` và được trừ khỏi mẫu số. Ca không được tính là ĐẠT.
  - Không có trong danh sách ⇒ ca ĐỎ, thông báo nêu phiên bản đã đo và việc phải làm: đo lại khe, ghi vào `KHONG_KHE_1460` qua một packet có review.
- **1c. Ba mutant `f02r3-*`.** Mutant chỉ được đăng ký khi ca đích của nó KHÔNG bị bỏ qua ở 1b. Khi bỏ qua, bảng đột biến in một dòng `BỎ QUA` cho từng mutant, nêu tên ca đích. Không mutant nào biến mất mà không có dòng.
- **1d. Giá trị ban đầu.** `KHONG_KHE_1460` ban đầu RỖNG. Base đã có lời khai «3.14.6 KHÔNG có» (chú thích tại `KHE_1460`, verdict lượt 4 của PR #1516), nhưng đó không phải một phép đo có tệp trong kho. Muốn đưa 3.14.6 vào danh sách thì executor phải chạy hai ca trên 3.14.6 thật và ghi đầu ra vào một tệp bằng chứng trong write set (mục Write set, tệp tuỳ chọn). Không chạy được thì danh sách vẫn rỗng; đó không phải lỗi của packet.
- **1e. Giữ nguyên.** `quet_bien`, `YAML_VO_1460`, `CON_1460`, `_hop_le_du`, và mọi ca/mutant không gắn `KHE_1460`. Ca năm 0999 (`nam_khong_dem`) là điều kiện khác, không thuộc K3, và giữ nguyên.

### 2. K5 — lượt 249 đột biến chạy theo khoá
- **2a. Khoá.** `khoa_dot_bien_1460()` trả một tuple gồm: sha256 hai tệp `ops/specs/wp1460-r1/hop_dong/*` ĐO trên đĩa; sha256 của `LENH_KIEM_HOP_DONG` (utf-8); phiên bản `jsonschema` lấy qua `importlib.metadata.version("jsonschema")`; `sys.version_info[:2]`.
- **2b. Bản ghi ghim.** Hằng `DA_DO_DOT_BIEN_1460` là một tập khoá, mỗi khoá kèm chuỗi trỏ tới lượt đầy đủ đã đạt (run CI hoặc tệp log trong write set, kèm ngày). Giá trị ban đầu chỉ gồm những khoá mà executor ĐO được bằng lượt đầy đủ đạt trên chính H của PR. Ít nhất phải có khoá của `gate-registry` trên CI (Python 3.12, `jsonschema` 4.26.0). Nguồn của khoá ấy là log job `gate-registry` của lượt CI PR trên H.
- **2c. Ca Nghiệm thu 1.** Ca `wp1460-hop-dong-lenh-kiem-480-va-dot-bien-249` tách thành hai ca:
  - `wp1460-hop-dong-lenh-kiem-fixture`: luôn chạy khối «Lệnh kiểm» KHÔNG có `--dot-bien`. Đạt khi rc 0 và stdout TRÙNG BYTE với hai dòng: dòng ĐẦU và dòng CUỐI của `DAU_RA_LENH_KIEM`. Hai dòng ấy được TÍNH từ hằng `DAU_RA_LENH_KIEM`, không chép thành chuỗi thứ hai, để khi #1522 đổi oracle (480 → 486) thì chỉ phải sửa một hằng.
  - `wp1460-hop-dong-lenh-kiem-dot-bien-249`: chạy CÓ `--dot-bien` khi `khoa_dot_bien_1460()` KHÔNG có trong `DA_DO_DOT_BIEN_1460`, HOẶC khi biến môi trường `CI_DANG_KY_DOT_BIEN_1460=du` được đặt. Đạt khi đầu ra trùng byte `DAU_RA_LENH_KIEM` như hiện nay. Khi bỏ qua, in đúng một dòng `BỎ QUA wp1460-hop-dong-lenh-kiem-dot-bien-249: khoá <băm ngắn> đã đo (<giá trị bản ghi>)`.
  - Khoá lạ mà lượt đầy đủ ĐẠT thì ca ĐẠT và in thêm khoá đầy đủ để người bảo trì ghi vào bản ghi. Ca KHÔNG tự sửa tệp.
- **2d. Tiến trình con khởi động sớm.** Cơ chế `_lk_som` giữ: lượt nào cần chạy thì khởi động sớm như cũ.
- **2e. Băm hai tệp vẫn kiểm mỗi lượt.** Ca `wp1460-hop-dong-bam-hai-tep-va-lenh-kiem` giữ nguyên. Nhờ vậy, đổi hai tệp hoặc khối «Lệnh kiểm» mà không cập nhật `BAM_HOP_DONG` thì vẫn ĐỎ như trước. Cập nhật `BAM_HOP_DONG` mà không thêm khoá mới thì lượt đầy đủ tự chạy (2c).
- **2f. Đây là đổi nghiệm thu của một packet đã land.** Nghiệm thu 1 của wp1460 r9 viết: «Bộ test của PR giao nộp chạy lại đúng các phép này trên hai tệp đã chép». Sau packet này câu ấy chỉ còn đúng khi khoá đổi. Quyết định chủ kho «Chạy khi khoá đổi» (mục Sổ quyết định) là thẩm quyền của thay đổi này. Hồ sơ land của packet này phải trỏ tới quyết định ấy.

### 3. Bất biến
- Không sửa hai tệp `ops/specs/wp1460-r1/hop_dong/*`, khối `LENH_KIEM_HOP_DONG`, `BAM_HOP_DONG`, `DAU_RA_LENH_KIEM`, lệnh thu `--thu-bien-nhan-audit`, `ci-dot-bien-du.yml`, `ci.yml`.
- Không thêm đường nào biến một ca thành ĐẠT khi nó chưa đo.
- **Trạng thái BỎ QUA là cơ chế MỚI.** Tại base, `ca_wp1460` trả `{tên: bool}` và bộ tổng hợp (`for _t, _ok in ca_wp1460().items(): _them(_t, _ok)`, dòng 3978) chỉ biết đạt/đỏ. Đo bằng grep lúc soạn: `ci_dang_ky_test.py` không có đường BỎ QUA nào cho ca. Packet thêm trạng thái thứ ba, chỉ dành cho các ca ở 1b và 2c, theo ba luật:
  - ca ở trạng thái ấy in dòng `BỎ QUA` của nó;
  - ca không được đếm vào cả tử lẫn mẫu;
  - dòng tổng kết của bộ wp1460 in thêm `· bỏ qua K` khi K > 0.

  Một mutant làm ca BỎ QUA đếm như ĐẠT phải bị giết (Nghiệm thu 5, mục ix).
- Không đọc mạng. Khoá và bản ghi tính offline.

## Nghiệm thu
1. **K3 trên nền có khe** (CI 3.12, và nền của executor). Hai ca quét biên ĐẠT với `tran > 0`. Đếm ca/mutant trên nền ấy không đổi so với base: A/B dựng trong MỘT lệnh; ghi `N/N` của base và của head.
2. **K3 trên nền không khe, giả lập.** Ca tiến trình con thay `is_valid` bằng bản không bao giờ ném rồi chạy hai ca quét biên, với `KHONG_KHE_1460` rỗng ⇒ cả hai ĐỎ, thông báo chứa phiên bản. Với `KHONG_KHE_1460` chứa khoá đang chạy ⇒ hai dòng `BỎ QUA` đúng mẫu 1b, ca bị trừ khỏi mẫu số, và ba mutant `f02r3-*` có dòng `BỎ QUA`.
3. **K5.** Ca tiến trình con có spy trên argv của tiến trình «Lệnh kiểm»:
   - khoá có trong bản ghi ⇒ đúng MỘT lần chạy, không `--dot-bien`;
   - khoá vắng (đổi phiên bản `jsonschema` giả trong khoá) ⇒ có một lần chạy `--dot-bien`;
   - `CI_DANG_KY_DOT_BIEN_1460=du` ⇒ có một lần chạy `--dot-bien`;
   - đầu ra hai dòng sai một byte ⇒ ĐỎ.
4. **Thời gian.** `python .claude/dev/ci_dang_ky_test.py --chay` trên CI PR (`gate-registry`) ghi giây của bước trước và sau. Số đo, không phải ngưỡng chặn. Tham chiếu: hồ sơ B1a ghi ~268 s; số đo lúc soạn ở mục cuối.
5. **Đột biến riêng cho MỖI chốt mới.** Chạy trên BẢN SAO tạm, tên tệp riêng, tắt bytecode; phân hạng bằng lớp ngoại lệ riêng của ca đích, neo tên ca; chết vì lỗi vô can ⇒ tín dụng giả. Tối thiểu:
   - (i) trả lại cổng phiên bản `* KHE_1460`;
   - (ii) `tran == 0` coi như ĐẠT;
   - (iii) bỏ tra `KHONG_KHE_1460`, luôn BỎ QUA;
   - (iv) khoá bỏ phiên bản `jsonschema`;
   - (v) khoá bỏ băm `LENH_KIEM_HOP_DONG`;
   - (vi) bỏ nhánh `CI_DANG_KY_DOT_BIEN_1460`;
   - (vii) lượt thường so `DAU_RA_LENH_KIEM` đầy đủ thay vì hai dòng, hoặc không so byte;
   - (viii) mutant `f02r3-*` bị bỏ không có dòng `BỎ QUA`;
   - (ix) ca BỎ QUA được đếm như ĐẠT (tử và mẫu cùng tăng).

   Mỗi đột biến phải làm ĐỎ đúng ca đích. Đòi `n/n` giết thật.
6. **Cổng kho.** `python .claude/dev/ci_dang_ky_test.py --chay` N/N; Ruff F delta = 0 trên mọi `.py` đổi (đo nền master trước); numstat trong trần; CI PR Ubuntu xanh.

## Write set
- Nhánh đặc tả `ops/wp1521-r1` (không thuộc PR giao nộp): `ops/specs/wp1521-r1/SPEC.md`, `ops/leases/wp1521-*.yaml`.
- PR giao nộp: `.claude/dev/ci_dang_ky_test.py`. Tuỳ chọn thêm một tệp bằng chứng `ops/specs/wp1521-r1/do/khe-<phiên bản>.txt` cho mỗi nền ghi vào `KHONG_KHE_1460` hoặc `DA_DO_DOT_BIEN_1460` khi nguồn không phải run CI. Không tệp nào khác.

## Ngoài phạm vi
- Khoản 1, 2, 4 của nợ B1a (lời hứa toàn phần, tài liệu sâu hơn parser, oracle năm 0001, `jobs[].run_id`) thuộc #1522.
- Đổi Python của `gate-registry`; dời lượt đột biến sang workflow khác; `ci.yml`; `ci-dot-bien-du.yml`.

## Baseline nghiệm thu
Immutable acceptance baseline: commit `origin/master` lúc cấp lease, ghi vào lease. Lúc soạn là `437257a3` (2026-11-25).

## Kích thước
Trần mặc định của lớp `sensitive` theo `ADR-0053`: ≤ 6 tệp, ≤ 450 dòng thêm theo `git diff --numstat` so baseline. Đo trước MỖI lần xin review. Vượt trần ⇒ DỪNG trước review.

## Quy trình và quyền
- **Điều kiện cấp lease:**
  1. Chủ kho duyệt băm đặc tả này.
  2. Mission revision xếp packet vào hàng `.claude/dev/ci_dang_ky_test.py`.
  3. Lease B2 `wp1494-*` (và mọi lease khác giữ `.claude/dev/ci_dang_ky_test.py`) đã hết hạn hoặc đã thu hồi hai chiều. `ai-dang-giu` chạy trên MỌI ref sau khi so TẬP TÊN ref cục bộ với `ls-remote`, thiếu 0.
- **Vai (đề xuất, chủ kho chốt khi duyệt băm):** executor Claude Code, Fable 5.2. Reviewer Codex gpt-6-astra, mức suy luận cao nhất, phiên độc lập, chỉ đọc. Reviewer CHẠY ca và đột biến có sẵn trong cây và có bản sao kho đủ để đo lại.
- **Trần:** theo Mission r96 `per_new_packet`, trừ khi Mission revision cho packet này ghi khác. Lời gọi Codex trên PR theo dòng khai `ADR-0055`. Trước MỖI lời gọi phải đếm số đã dùng.
- **Windows (`ADR-0060` M3):** diff chạm `.claude/dev/**` ⇒ `required`. Chỉ đạt khi có dòng chủ kho `windows: <H> mien` neo đúng H cuối, hoặc một lượt Windows local được cấp.
- Audit exact-H và merge theo `ADR-0060`. Merge do chủ kho bấm.
- **Hoàn tác:** revert PR giao nộp.

## Sổ quyết định (chủ kho, công cụ hỏi đáp trong phiên điều phối nợ, 2026-11-25 ~07:4xZ; ghi hộ lên #1172 cùng lúc với lời xin duyệt băm)
- Gom: «2 packet» — N1 #1522 (khoản 1, 2, 4), N2 #1521 (khoản 3, 5).
- K5: «Chạy khi khoá đổi».
- K3: «Báo ĐỎ».

## Số đo lúc soạn (2026-11-25, `master` `437257a3`)
- `.claude/dev/ci_dang_ky_test.py` tại base: `KHE_1460` ở dòng 1865; ca Nghiệm thu 1 ở dòng 2015–2028; `BAM_HOP_DONG` ở dòng 1845–1848.
- Nền phiên soạn: Python 3.13.18, `jsonschema` 4.26.0, PyYAML 6.0.3. `gate-registry` trên CI ghim Python 3.12 (verdict lượt 4 của PR #1516, câu hỏi cấu trúc 3).
- Đo THẲNG khối «Lệnh kiểm» trên hai tệp v1, trên nền phiên soạn:
  - không `--dot-bien`: hai dòng `FIXTURE: 480/480 …` và `TONG: DAT`, rc 0, 2,50 s;
  - có `--dot-bien`: ba dòng của `DAU_RA_LENH_KIEM`, rc 0, 212 s. Số này đo trong lúc một lượt đột biến khác chạy song song, nên cao hơn chạy riêng.
- Không dùng `--chay` để đo phần này. `--chay` chạy cả registry: cùng lúc, lượt `--chay` ấy in `PHẢN CHỨNG: 1677/1677` và chạy các bộ `day_du` khác, nên số giây của nó không phải của wp1460. Hồ sơ B1a ghi `7 s → ~268 s`, nhưng không ghi số đo ấy lấy theo bước nào. Nghiệm thu 4 đo lại theo bước `gate-registry`.
- Quét toàn ref 2026-11-25 ~07:3xZ (so tập tên ls-remote với for-each-ref, thiếu 0): `.claude/dev/ci_dang_ky_test.py` có NGƯỜI_GIỮ 1, là `wp1494-r5-g2-claude` (B2).

## Thay đổi
| revision | thay đổi |
|---|---|
| r1 | bản đầu |
