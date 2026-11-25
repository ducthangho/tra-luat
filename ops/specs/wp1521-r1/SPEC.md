# wp1521 r3 — nợ B1a: `KHE_1460` báo ĐỎ trên nền không có khe chưa đo + lượt đột biến của Nghiệm thu 1 chỉ chạy khi diff chạm đầu vào (NO-B1A-N2)
packet_id: wp1521
revision: 3
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
mission_issue: 1172
packet_issue: 1521
risk: sensitive
review_class: sensitive
executor: claude
environment: cloud (Linux)

Trạng thái: r3, lượt soạn cuối (3/3) theo trần `per_new_packet`. Thay r2 (`ops/wp1521-r1@5e8731f`, sha256 `74eaf678…`); r1 (`15f5437`, `d2126b3a…`) được chủ kho duyệt trước review nhưng KHÔNG dùng để cấp lease. Review lượt 2 trên r2 trả `changes_requested` với 2 P2: N2-06 (kiểm kê nghiệm thu mâu thuẫn ánh xạ tên ở 2c; đếm bỏ qua sai) và N2-07 (`doc_diff` tin rc 0 trên lịch sử có nhiều gốc hợp nhất). Lượt 2 xác nhận N2-02, 03, 04 ĐÃ VÁ THẬT; N2-01, N2-05 VÁ SINH LỖI MỚI, chính là hai finding mới N2-06, N2-07. Chưa duyệt băm r3, chưa có lease.

## Mục tiêu
Đóng hai khoản nợ của B1a #1460 (hồ sơ `ops/land/pr1516-wp1460-land-evidence.yaml`, mục `no_ngoai_pham_vi`, khoản 3 và 5). Không đổi hợp đồng `bien_nhan_audit.v1`.
- **K3.** Trên nền mà ca quét biên không chạm được giới hạn đệ quy, các ca và mutant gắn `KHE_1460` hiện tự biến mất, không báo gì. Sau packet này, nền ấy làm gate ĐỎ, trừ khi nền ấy nằm trong danh sách cho phép kèm phép đo đã ghi.
- **K5.** `.claude/dev/ci_dang_ky_test.py --chay` không còn chạy 249 đột biến của khối «Lệnh kiểm» ở mỗi lượt. Lượt thường chạy khối ấy KHÔNG có `--dot-bien`. Lượt đầy đủ chỉ chạy khi diff đo được chạm vùng đầu vào, hoặc khi không đo được diff.

## Hợp đồng

### 1. K3 — từ cổng theo PHIÊN BẢN sang cổng theo PHÉP ĐO
- **1a. Hiện trạng tại base** (đo lại trong review lượt 1): `KHE_1460 = sys.version_info < (3, 14)`. Hằng này gắn BỐN ca:
  - hai ca quét trực tiếp `wp1460-thu-quet-bien-de-quy-{dau-job,bien-nhan-xanh}`;
  - hai ca bọc tiến trình con `wp1460-con-khong-vo-thu-quet-bien-de-quy-{dau-job,bien-nhan-xanh}`.

  Ba mutant `f02r3-*` nhắm vào hai ca BỌC. Đếm tại base: KHE=True ⇒ 314 ca / 118 mutant; KHE=False ⇒ 310 / 115.
- **1b. Phép đo duy nhất, chạy ở tiến trình cha.** Hàm mới `do_khe_1460()` chạy hai lượt quét của `quet_bien` một lần ở tiến trình cha. Với mỗi lượt quét `t ∈ {dau-job, bien-nhan-xanh}` nó trả một bản ghi có cấu trúc `{tran, dat_het, so_do_sau, loi}`. `quet_bien` được phép đổi để trả bản ghi này. Điều kiện ĐẠT cũ, `dat_het and tran > 0`, giữ nguyên ý nghĩa.
- **1c. Bảng quyết định** (theo từng lượt quét `t`; thứ tự ưu tiên từ trên xuống):

  | điều kiện của lượt quét `t` | kết cục của ca quét `t` và ca bọc `t` |
  |---|---|
  | `loi` khác `None` (lượt quét ném), hoặc lượt quét chưa chạy hết dải độ sâu | ĐỎ |
  | `dat_het == False` (dù `tran` bằng bao nhiêu, dù nền có trong danh sách cho phép) | ĐỎ |
  | `tran > 0` và nền CÓ trong `KHONG_KHE_1460` | ĐỎ: lời khai «không có khe» của danh sách bị phép đo bác |
  | `tran > 0` | chạy như base (ĐẠT/ĐỎ theo ca) |
  | `tran == 0`, nền KHÔNG có trong `KHONG_KHE_1460` | ĐỎ, thông báo nêu phiên bản và việc phải làm |
  | `tran == 0`, nền CÓ trong `KHONG_KHE_1460` | BỎ QUA |

  «Nền» là khoá `(sys.version_info[:3], phiên bản jsonschema theo importlib.metadata)`. Kết quả lẫn (một lượt quét `tran > 0`, lượt kia `tran == 0`) vẫn đi qua bảng cho TỪNG lượt quét.
- **1d. Lan trạng thái BỎ QUA:**
  - ca quét `t` BỎ QUA ⇒ ca bọc `t` cũng BỎ QUA. Quyết định lấy từ phép đo 1b ở tiến trình CHA; không chạy tiến trình con cho ca bọc bị bỏ qua;
  - mọi mutant có ca đích bị BỎ QUA thì không chạy, mỗi mutant in một dòng `BỎ QUA <mutant>: ca đích <ca> bỏ qua`, và bị loại khỏi cả tử lẫn mẫu `n/n` của bảng đột biến;
  - lượt nền khoẻ của bộ đột biến (baseline) cũng loại các ca bị BỎ QUA.
- **1e. Giá trị ban đầu của `KHONG_KHE_1460`: RỖNG.** Chỉ thêm khoá qua một packet có review, kèm tệp đo trong kho (`ops/specs/wp1521-r1/do/khe-<nền>.txt`, gồm đầu ra `do_khe_1460()` đầy đủ). Packet này chỉ thêm khoá khi executor CHẠY được trên đúng nền ấy.
- **1f. Trạng thái BỎ QUA là cơ chế MỚI** (đo lúc soạn: grep không thấy đường bỏ qua ca nào). Giá trị của ca trong `ca_wp1460` có ba trạng thái: `True`, `False`, và một hằng riêng `BO_QUA_1460` (không phải bool, không ép về bool). Các bên tiêu dùng:
  - bộ tổng hợp ở dòng 3978: ĐẠT/ĐỎ như cũ; BỎ QUA in dòng và không vào tử/mẫu; dòng tổng kết wp1460 in thêm `· bỏ qua K` khi K > 0;
  - `CON_1460`: ca bị bỏ qua không bao giờ tới tiến trình con (1d); nếu vẫn tới thì thoát mã riêng 5, và cha coi mã 5 là ĐỎ;
  - bộ phân hạng đột biến: không đổi luật GIẾT; chỉ thêm lọc 1d trước khi chạy.

### 2. K5 — lượt đột biến của khối «Lệnh kiểm» chạy theo DIFF của đầu vào
- **2a. Thay cho bản ghi khoá.** Không có bản ghi «đã đo» trong cây. Quyết định dùng lại `doc_diff()` có sẵn (#643, ba trạng thái: tập · rỗng · `None`, fail-close) cùng biến `CI_DANG_KY_SU_KIEN`/`GOC`/`DAU` mà `gate-registry` đã truyền. `doc_diff` giữ nguyên.
  - **Chốt hợp lệ của diff** (thêm ở bộ chọn K5, NGOÀI `doc_diff`): diff chỉ được dùng để BỎ QUA khi `git merge-base --all GỐC ĐẦU` thoát 0 và in ĐÚNG MỘT SHA.
  - Không đo được, hoặc nhiều hơn một gốc hợp nhất (lịch sử criss-cross) ⇒ coi như `None`, chạy đủ.
  - Lý do (review lượt 2, N2-07): khi có nhiều gốc hợp nhất, `git diff GỐC...ĐẦU` vẫn rc 0 nhưng tự chọn một gốc. Reviewer dựng được đồ thị mà diff ra RỖNG trong khi cây hợp nhất đổi `ci_dang_ky_test.py`; đảo thứ tự cha thì kết quả lật.
- **2b. Vùng đầu vào** của lượt đột biến:
  - `.claude/dev/ci_dang_ky_test.py`, vì tệp này chứa khối «Lệnh kiểm», `BAM_HOP_DONG` và `THU_MUC_HOP_DONG`;
  - mọi tệp dưới thư mục mà `THU_MUC_HOP_DONG` trỏ tới, tính tại HEAD và cả tại GỐC khi hai bên khác nhau;
  - `.github/workflows/ci.yml`, vì nó ghim Python và `jsonschema` cho `gate-registry`;
  - `requirements.txt`.
- **2c. Ca Nghiệm thu 1** `wp1460-hop-dong-lenh-kiem-480-va-dot-bien-249` tách thành hai ca.
  - **`wp1460-hop-dong-lenh-kiem-fixture`** luôn chạy khối «Lệnh kiểm» KHÔNG có `--dot-bien`. Ca đạt khi:
    - rc bằng 0;
    - stdout TRÙNG BYTE với dòng ĐẦU và dòng CUỐI của `DAU_RA_LENH_KIEM`. Hai dòng ấy được TÍNH từ hằng, không chép thành chuỗi thứ hai.
  - **`wp1460-hop-dong-lenh-kiem-dot-bien`** chạy CÓ `--dot-bien` khi một trong hai điều xảy ra:
    - `doc_diff()` trả `None`. Trường hợp này gồm mọi lượt ngoài push/pull_request và mọi lượt chạy local không có biến;
    - diff chạm vùng 2b.

    Ca đạt khi đầu ra trùng byte `DAU_RA_LENH_KIEM`. Khi diff đo được mà không chạm vùng, ca in đúng một dòng `BỎ QUA wp1460-hop-dong-lenh-kiem-dot-bien: diff <GỐC ngắn>...<ĐẦU ngắn> không chạm vùng đầu vào` và mang trạng thái `BO_QUA_1460`.
- **2d. Hệ quả cần nói đúng mức:**
  - PR nào chạm `ci_dang_ky_test.py` vẫn trả trọn chi phí đột biến, kể cả chính packet này và #1522;
  - lượt `schedule`/`workflow_dispatch` của `ci.yml` (nếu có) và lượt local luôn chạy đủ;
  - phụ thuộc bắc cầu của `jsonschema` (`attrs`, `referencing`, `jsonschema-specifications`, `rpds-py`) KHÔNG được ghim và KHÔNG nằm trong vùng. Một lần đổi ngầm của chúng giữa hai lượt PR không chạm vùng sẽ không làm lượt đột biến chạy lại. Đây là giới hạn đã khai, KHÔNG ĐO ĐƯỢC bằng diff. Lượt push lên `master` mà không chạm vùng cũng bỏ qua.
- **2e. Đổi nghiệm thu của packet đã land.** Nghiệm thu 1 của wp1460 r9 ghi: «Bộ test của PR giao nộp chạy lại đúng các phép này». Sau packet này câu ấy chỉ còn đúng khi diff chạm vùng hoặc không đo được diff. Thẩm quyền: quyết định chủ kho «Chạy khi khoá đổi». Cơ chế diff thay cho bản ghi khoá vì review lượt 1 (N2-03, N2-04) chỉ ra rằng bản ghi khoá không kiểm chứng được và tự tham chiếu H cuối. Chủ kho được hỏi lại khi xin duyệt băm r2.
- **2f.** Ca `wp1460-hop-dong-bam-hai-tep-va-lenh-kiem` giữ nguyên.

### 3. Bất biến
- Không sửa hai tệp `ops/specs/wp1460-r1/hop_dong/*`, `LENH_KIEM_HOP_DONG`, `BAM_HOP_DONG`, `DAU_RA_LENH_KIEM`, lệnh thu, `ci-dot-bien-du.yml`, `ci.yml`, `doc_diff`.
- Được phép đổi các bên tiêu dùng trạng thái mà 1d/1f nêu: `quet_bien`, `ca_wp1460`, `CON_1460`, bộ tổng hợp, bộ lọc mutant. Luật ĐẠT/GIẾT cũ giữ nguyên ý nghĩa.
- Không đường nào biến một ca chưa đo thành ĐẠT. BỎ QUA chỉ sinh ra từ hai nguồn: bảng 1c, và diff đo được không chạm vùng ở 2c.
- Tình trạng mạng: `doc_diff` chỉ gọi `git` cục bộ, như tại base.

## Nghiệm thu
1. **Kiểm kê A/B trong MỘT lệnh.** Trên nền có khe (CI 3.12; nền executor), so base với head theo TÊN, với ĐÚNG MỘT ánh xạ đổi tên được phép (2c): `wp1460-hop-dong-lenh-kiem-480-va-dot-bien-249` → hai ca `wp1460-hop-dong-lenh-kiem-fixture` và `wp1460-hop-dong-lenh-kiem-dot-bien`. Ngoài ánh xạ ấy:
   - mọi ca và mutant có tên ở base vẫn có mặt, với cùng kết cục ĐẠT/GIẾT;
   - phần chênh chỉ gồm các ca/mutant mới, mỗi cái được liệt kê tên;
   - không so tổng;
   - không giữ một ca mang tên cũ chỉ để kiểm kê khớp.
   Đếm tại base (đo trong review lượt 2): 314 ca. Áp riêng ánh xạ đổi tên ⇒ 315, trước khi thêm các ca mới.
2. **K3, chuỗi tiêu dùng trọn vẹn.** Ca tiến trình con thay kết quả `do_khe_1460()` bằng các bộ giá trị điều khiển, chạy trọn chuỗi gồm ca trực tiếp, ca bọc, bộ lọc mutant và dòng tổng kết. Kiểm đúng tập ca và các dòng in ra cho TỪNG hàng của bảng 1c:
   - (a) `tran > 0`, `dat_het` đúng, không có trong danh sách ⇒ như base;
   - (b) `tran == 0`, `dat_het` đúng, không có trong danh sách ⇒ ĐỎ, cả ca trực tiếp lẫn ca bọc;
   - (c) `tran == 0`, `dat_het` đúng, có trong danh sách, CẢ HAI lượt quét ⇒ bỏ qua 4 ca (2 ca quét, 2 ca bọc) và 3 mutant `f02r3-*`. Tử và mẫu mỗi bên giảm đúng 4 ca / 3 mutant, mỗi cái có dòng `BỎ QUA` riêng;
   - (d) như (c) nhưng `dat_het` sai, thử riêng hai lỗi «rc sai» và «biên nhận không hợp schema» ⇒ ĐỎ;
   - (e) có trong danh sách mà `tran > 0` ⇒ ĐỎ;
   - (f) kết quả lẫn, tức chỉ một lượt quét rơi vào hàng BỎ QUA. Đo lúc soạn theo bảng mutant tại base:
     - riêng `dau-job` bị bỏ ⇒ đúng 2 ca và 2 mutant (`f02r3-dau-job-is-valid-khong-chot`, `f02r3-quet-khong-cham-gioi-han-thi-ca-do`);
     - riêng `bien-nhan-xanh` bị bỏ ⇒ đúng 2 ca và 1 mutant (`f02r3-bien-nhan-xanh-is-valid-khong-chot`);
     - lượt quét còn lại chạy theo đúng hàng của nó;
   - (g) lượt quét ném ⇒ ĐỎ, không BỎ QUA.
3. **K5.** Ca tiến trình con có spy trên argv của tiến trình «Lệnh kiểm», chạy với các bộ biến sự kiện/diff điều khiển (kho git tạm có hai commit):
   - diff không chạm vùng ⇒ đúng một lần chạy, không `--dot-bien`, kèm dòng BỎ QUA;
   - diff chạm `ci_dang_ky_test.py` ⇒ có `--dot-bien`;
   - diff chạm một tệp dưới `THU_MUC_HOP_DONG` ⇒ có `--dot-bien`;
   - lặp lại ca trên khi `THU_MUC_HOP_DONG` trỏ thư mục khác `wp1460-r1` ⇒ có `--dot-bien`;
   - diff chạm `ci.yml` ⇒ có `--dot-bien`;
   - diff chạm `requirements.txt` ⇒ có `--dot-bien`;
   - không biến sự kiện ⇒ có `--dot-bien`;
   - sự kiện `schedule` ⇒ có `--dot-bien`;
   - GỐC không phải tổ tiên của ĐẦU khi push ⇒ có `--dot-bien`;
   - đồ thị criss-cross có hai gốc hợp nhất, dựng theo CẢ HAI thứ tự cha, mà `doc_diff` ra rỗng ⇒ có `--dot-bien` ở cả hai;
   - đối chứng tuyến tính, đổi một tệp ngoài vùng ⇒ vẫn bỏ qua. Đối chứng này chạy trong cùng lệnh với hai ca criss-cross;
   - đầu ra hai dòng sai một byte ⇒ ĐỎ.
4. **Thời gian.** Ghi giây của bước `test registry` trong `gate-registry` trên lượt CI PR của H (ở đây diff chạm `ci_dang_ky_test.py` nên chạy đủ), và trên một lượt PR KHÔNG chạm vùng nếu có. Đây là số đo, không phải ngưỡng.
5. **Đột biến riêng cho MỖI chốt mới.** Chạy trên BẢN SAO tạm, tên tệp riêng, tắt bytecode. Phân hạng bằng lớp ngoại lệ riêng của ca đích, neo tên ca; chết vì lỗi vô can ⇒ tín dụng giả. Tối thiểu:
   - (i) trả lại cổng phiên bản `* KHE_1460`;
   - (ii) `tran == 0` coi như ĐẠT;
   - (iii) bỏ điều kiện `dat_het` trước khi BỎ QUA;
   - (iv) bỏ hàng «có trong danh sách mà `tran > 0`»;
   - (v) bỏ tra `KHONG_KHE_1460` và luôn BỎ QUA;
   - (vi) ép `BO_QUA_1460` về bool;
   - (vii) ca bọc vẫn ĐẠT khi ca trực tiếp BỎ QUA;
   - (viii) ca bọc bị bỏ đi mà không có dòng BỎ QUA;
   - (ix) giữ mutant có ca đích bị bỏ trong mẫu `n/n`;
   - (x) giữ ca bị bỏ trong baseline đột biến;
   - (xi) ca BỎ QUA được đếm như ĐẠT;
   - (xii) vùng 2b bỏ `THU_MUC_HOP_DONG`;
   - (xiii) vùng ghi cứng `ops/specs/wp1460-r1/hop_dong/`;
   - (xiv) vùng bỏ `ci.yml`;
   - (xv) `doc_diff() is None` coi như không chạm vùng;
   - (xvi) lượt thường so `DAU_RA_LENH_KIEM` đầy đủ, hoặc không so byte;
   - (xvii) bỏ chốt «đúng một gốc hợp nhất»;
   - (xviii) chốt chỉ đòi «ít nhất một» gốc hợp nhất;
   - (xix) ca bọc của lượt quét KHÔNG bị bỏ vẫn bị bỏ, khi kết quả lẫn.

   Đòi `n/n` giết thật.
6. **Cổng kho.** `python .claude/dev/ci_dang_ky_test.py --chay` N/N, kèm số bỏ qua; Ruff F delta = 0 trên mọi `.py` đổi (đo nền master trước); numstat trong trần; CI PR Ubuntu xanh.

## Write set
- Nhánh đặc tả `ops/wp1521-r1` (không thuộc PR giao nộp): `ops/specs/wp1521-r1/SPEC.md`, `ops/leases/wp1521-*.yaml`.
- PR giao nộp: `.claude/dev/ci_dang_ky_test.py`. Tuỳ chọn thêm một tệp đo `ops/specs/wp1521-r1/do/khe-<nền>.txt` cho mỗi nền ghi vào `KHONG_KHE_1460` (1e). Không tệp nào khác.

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
| r3 | Review lượt 2, 2 P2. `skip-state-consumer-contract-incomplete` (N2-06): nghiệm thu 1 khai đúng ánh xạ một tên cũ thành hai tên mới; 2(c)/(f) ghi số đếm đã đo (4/3; 2/2; 2/1). `mutation-cache-fingerprint-detached-from-inputs` (N2-07): chốt «đúng một gốc hợp nhất» ở bộ chọn K5, kèm ca criss-cross theo hai thứ tự cha và đối chứng tuyến tính; thêm 3 đột biến. |
| r2 | Review lượt 1, 5 finding, sửa theo lớp:<br>• `skip-state-consumer-contract-incomplete` (N2-01): bốn ca chứ không phải hai; lan BỎ QUA sang ca bọc, mutant và baseline (1a, 1d, 1f).<br>• `skip-waiver-masks-measured-failure` (N2-02): bảng 1c đặt `dat_het` trước mọi quyết định bỏ qua; có hàng riêng cho kết quả lẫn và kết quả ném.<br>• `mutation-cache-enrollment-without-verified-evidence`, `self-referential-final-head-cache-bootstrap`, `mutation-cache-fingerprint-detached-from-inputs` (N2-03..05): bỏ bản ghi khoá; dùng `doc_diff()` có sẵn, vùng đầu vào tính theo `THU_MUC_HOP_DONG` thực tế; phụ thuộc bắc cầu khai là giới hạn KHÔNG ĐO ĐƯỢC (2d).<br>Nghiệm thu và bảng đột biến viết lại theo đó. |
