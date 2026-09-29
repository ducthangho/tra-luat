# HARNESS-TU-KIEM-DUNG-CHUNG — đặc tả đóng băng (revision 1)

Nguồn quyết định: chủ kho `ducthangho`, phiên Claude Code executor g3 của #674
(`session_01269GBDswLRWNxxkcxjuByt`), 2026-09-29. Mở successor: "Mở successor cho harness tự kiểm chung"
(~17:00Z). Soạn đặc tả: "Soạn spec cho #694 đi". Q1–Q7 và Q8–Q12 chốt "theo khuyến nghị". Xác nhận hiểu
giống nhau: "Đồng ý, viết spec và đăng băm đi". Số đo trong tệp này lấy ngày 2026-09-29, mỗi số kèm giờ đo.
Đo lại trước mỗi bước công bố (cấp lease, merge).

Đặc tả này KHÔNG cấp việc. Bắt tay chỉ khi có lease còn hiệu lực theo `docs/PROTOCOL_DA_PHIEN.md` §3.2 và §4.

## packet_id · packet_issue
`HARNESS-TU-KIEM-DUNG-CHUNG` · #694

## nguon_cap_viec
Packet khắc phục, cha là #674 (`CI-DUONG-NHANH-HO-SO`). Nguồn gốc:
- verdict Codex lượt 1–6 ở `ops/reviews/ci-duong-nhanh-674/luot-{1..6}-verdict.md` trên nhánh
  `ops/review-674-ci-duong-nhanh` (lượt 6 ở commit `dca9542`, sha256
  `7efc99b38d568a859f53c64673a7372c842e97789be145bf6fbeb477bd1115e2`);
- quyết định chủ kho chọn phương án 1 cho #674 (Issue #674 comment 5894382240), rồi mở successor (#694).

## review_class
`sensitive`. Lý do: mục tiêu M3 sửa `.claude/dev/ci_dang_ky_test.py`, tức sổ đăng ký test của CI. Đây là
"workflow/CI authority" theo `docs/PROTOCOL_DA_PHIEN.md` mục Review Class (đo 17:05Z 29-09: dòng 680).
Fail-closed. Đòi Codex `cross_approved` hoặc `human_audited`. Phần harness tự thân là `systemic`; lớp hiệu
lực lấy mức cao hơn.

### Lệch ADR-0044, khai theo chính ADR (dòng 5–7: "khai lý do trong spec")
Trần `sensitive` chạm authority là ≤ 3 tệp và ≤ 300 dòng thêm.
- **Số tệp: 3, đạt.**
- **Số dòng thêm: ước lượng 700–900, VƯỢT.** Ước lượng từ `af1165d:ops/ci_duong_nhanh_test.py` (đo 17:0xZ
  29-09): 236 dòng logic harness, 187 dòng ca tự kiểm, bảng đột biến 172 dòng.

Lý do chấp nhận:
1. Tệp test mới và dòng đăng ký KHÔNG tách được. `kiem()` của `ci_dang_ky_test.py` báo
   `test sống chưa đăng ký` cho mọi `*_test.py` dưới `.claude/dev/` (đo 17:0xZ 29-09 trên master `44620e8`: `def kiem` dòng 578, lời báo dòng 581).
   Tách ra thì packet thứ nhất tự đỏ.
2. Phần chạm authority chỉ là ĐÚNG MỘT dòng thêm vào `MOI` (M3). Hai tệp còn lại là mã mới, không đổi hành
   vi nào đang có.

**Trần thay thế của packet này:** `git diff --numstat <base>..<head>` trên ba tệp ≤ **1.000 dòng thêm** và
≤ **3 tệp**. Vượt thì DỪNG trước review (S4).

## write_set
1. `.claude/dev/harness_dot_bien.py` (mới)
2. `.claude/dev/harness_dot_bien_test.py` (mới)
3. `.claude/dev/ci_dang_ky_test.py`: CHỈ đúng một dòng thêm vào dict `MOI`, khoá
   `".claude/dev/harness_dot_bien_test.py"`, giá trị là regex ở M3. Không sửa, không xoá dòng nào khác.

Đo 17:07Z 29-09 bằng `lease_publish.py ai-dang-giu` trên bản sao đủ 513 nhánh:
- (1) và (2): `NGƯỜI_GIỮ 0`.
- (3): `NGƯỜI_GIỮ 2`, là `ci-duong-nhanh-ho-so-r2-g3-claude` (#674, hạn 2026-09-30T10:52Z) và
  `ci-g5-cong-cu-chia-manh-r1-g2-claude` (#668, hạn 2026-09-30T07:41Z).
- Bất biến: **không cấp lease khi (3) còn người giữ khác.**

## ngoai_pham_vi
- **Không chuyển bất kỳ tệp test tiêu thụ nào** sang harness (`ops/ci_duong_nhanh_test.py`,
  `ops/nhanh_don_duoc_test.py`, `ops/cong_cu_test.py`, `.claude/dev/launcher_test.py`, `ops/bien_nhan_v2_test.py`,
  …). Mỗi tệp là một successor riêng (Q1). Lý do: giữ trần kích thước; `ops/ci_duong_nhanh_test.py` còn nằm
  trong write set #674.
- **Không sửa `.github/workflows/ci.yml`** (Q3). Test harness chạy qua bước `test registry` của job
  `gate-registry` nhờ mục `MOI`. `gate-registry` KHÔNG thuộc ba required check; chấp nhận có chủ đích (Q3).
- Không đổi `DA_NOI`, `CACH_LY`, `MOI_WINDOWS`, hay logic nào khác của `ci_dang_ky_test.py`.
- Không chạy Windows CI (Q6). Không mở PR khi chủ kho chưa bảo (Q11). Không land, không deploy.
- Không chép nguyên khối từ `af1165d:ops/ci_duong_nhanh_test.py`. Blob đó là TƯ LIỆU tham chiếu (Q4); harness
  viết lại có API riêng (M1).

## Quyết định đã chốt (Q1–Q12)
- Q1: phạm vi chỉ gồm harness và test riêng của nó; không chuyển consumer.
- Q2: `.claude/dev/harness_dot_bien.py` và `.claude/dev/harness_dot_bien_test.py`.
- Q3: nối CI bằng một dòng `MOI`; không sửa `ci.yml`.
- Q4: base = `origin/master` tại lúc cấp lease. Chỉ cấp lease khi `ci_dang_ky_test.py` không còn người giữ
  khác (xem write_set). Tư liệu tham chiếu: blob `af1165d04977f2e3de1fa0fdbaa9a1775dd9bd30:ops/ci_duong_nhanh_test.py`.
- Q5: nghiệm thu gồm đủ 12 cửa D01–D12 (mục nghiem_thu), mỗi cửa một đột biến riêng.
- Q6: chỉ dùng API di động được. Đo trên Linux; Windows để ở `chua_do_duoc`.
- Q7 và Q12: reviewer Codex `gpt-6-astra` effort high, theo phân lớp, có HINT patch, trần **3 lượt**. Hết 3
  lượt thì là checkpoint của chủ kho, không tự sang lượt 4. Executor là Claude `claude-opus-5-5` (effort xhigh,
  tự khai).
- Q8: `sensitive` kèm lệch ADR-0044 đã khai (trên).
- Q9: dòng in và regex `MOI` như M3.
- Q10: API tối thiểu như M1.
- Q11: như #674. Không PR, không Windows CI; đo tại chỗ.

## muc_tieu
Mỗi mục chiếu vào đúng một đường dẫn trong write_set.

**M1 → `.claude/dev/harness_dot_bien.py`.** Module harness dùng chung. Chỉ dùng thư viện chuẩn Python, API di
động (không `os.getpgid`, `os.O_NOFOLLOW`… khi chưa `hasattr`). Tối thiểu có:
- a. Lớp tín hiệu ca `TinHieuChotCa(AssertionError)` và hàm `bang(dieu_kien, thong_diep)` ném đúng lớp đó.
- b. Sổ ca có NHÓM KHAI TƯỜNG MINH khi đăng ký (không suy từ tiền tố tên), hàm phân hoạch nhóm, và hàm dựng
  dòng `KIEM KE:` từ phân hoạch cùng bảng đột biến.
- c. Bộ chạy ca trong tiến trình. Trả `DAT` / `DO` / `HONG`: `DO` chỉ khi ca ném `TinHieuChotCa`; mọi ngoại lệ
  khác là `HONG`. Gọi ca ĐÚNG MỘT lần.
- d. Bộ chạy một ca cho tiến trình con (`--mot-ca TEN`). Mã thoát: 0 đạt · 3 kèm dòng `DO:<ten>:` · 4 hỏng ·
  2 sai đối số.
- e. Bộ chạy đột biến trên BẢN SAO TẠM:
  - neo thay thế xuất hiện đúng một lần, không thì HONG;
  - bản đột biến phải khác bản gốc;
  - ca đích phải XANH trên bản gốc trước, không thì HONG;
  - vật hoá tập ca đích một lần (iterator, generator đều được); tập rỗng hoặc tên lạ là HONG;
  - tắt ghi bytecode và không để lại `.pyc`;
  - mỗi đột biến dùng cây tạm và tên tệp riêng;
  - được chạy song song, nhưng kết quả đọc theo thứ tự khai báo.
- f. Bộ phân hạng `phan_hang(rc, dau_ra, ten_dich)`: rc=0 là `SONG_SOT`; rc=3 có `DO:<ten_dich>:` là `GIET`;
  rc=3 sai tên hoặc rc=4 là `TIN_DUNG_GIA`; rc khác là `HONG`.
- g. `main(argv)` chuẩn:
  - in `CA: <dat>/<tong> dat · <do> do · <hong> hong`, `DOT BIEN: <giet>/<tong> bi giet dung ly do`, đúng MỘT
    dòng `KIEM KE:`, và dòng cuối `TONG: DAT|DO`;
  - trả 0 chỉ khi mọi ca đạt (tổng > 0), mọi đột biến bị giết (tổng > 0), không có mục xấu, tự kiểm phân hạng
    đạt, và không có tên đột biến trùng;
  - trả 1 khi có bất kỳ điều kiện nào hỏng; trả 2 khi sai đối số;
  - một hàm entrypoint chuyển mã của `main` ra mã thoát tiến trình.
- h. Cách một tệp consumer dùng harness: consumer chỉ KHAI ca, nhóm và đột biến, rồi gọi `main`/entrypoint của
  harness. Không phải tự viết runner, phân hạng hay `main`.

**M2 → `.claude/dev/harness_dot_bien_test.py`.** Bộ test riêng của harness:
- đăng ký ca bằng CHÍNH harness;
- đột biến CHÍNH `harness_dot_bien.py` trên bản sao tạm;
- phủ đủ D01–D12 (nghiem_thu);
- in đúng dòng M3.

**M3 → `.claude/dev/ci_dang_ky_test.py`.** Thêm đúng một mục vào `MOI`:
```
".claude/dev/harness_dot_bien_test.py": r"^harness_dot_bien tests: ([1-9]\d*)/(\1) ca QUA · ([1-9]\d*)/(\3) dot bien GIET$",
```
Dòng in tương ứng của M2, đúng nguyên văn trừ phần số:
`harness_dot_bien tests: N/N ca QUA · M/M dot bien GIET`.

## nghiem_thu
Mỗi tiêu chí nêu phép đo làm nó ĐỎ. "Đột biến" ở đây là đột biến lên `harness_dot_bien.py`, khai trong bảng đột
biến của `harness_dot_bien_test.py`, chạy trên bản sao tạm. "Giết đúng lý do" nghĩa là ca đích ném
`TinHieuChotCa`, được phân hạng `GIET`.

### Mười hai cửa D01–D12 (M1, M2)
Nguồn: sáu lượt Codex của #674 và `CLAUDE.md`. Mỗi cửa có ÍT NHẤT một ca và ĐÚNG một đột biến riêng mang tên
cửa. Đột biến phải làm ca đích ĐỎ đúng lý do.

| cửa | hành vi phải giữ | đột biến bắt buộc (tên gợi ý) |
|---|---|---|
| D01 | bộ chạy ca gọi ca đúng một lần | `D01_runner_khong_goi_ca` và `D01b_runner_goi_hai_lan` (hai đột biến, cùng cửa) |
| D02 | ngoại lệ không phải tín hiệu là `HONG`, không phải `DO` | `D02_hong_thanh_do` |
| D03 | `TinHieuChotCa` là `DO`, không bị nuốt thành `DAT` | `D03_nuot_tin_hieu` |
| D04 | entrypoint chuyển mã của `main` ra mã thoát thật (0/1/2), đo qua TIẾN TRÌNH CON | `D04_entrypoint_rc1_thanh_0` |
| D05 | mỗi vế trong điều kiện `ok` của `main` | một đột biến gỡ từng vế: ca đạt, số giết, mục xấu, tự kiểm, tên trùng |
| D06 | dòng `CA:` / `DOT BIEN:` in tử số THẬT; đo ở kịch bản tử số khác mẫu số | `D06_in_mau_lam_tu` |
| D07 | ĐÚNG MỘT dòng `KIEM KE:`: tập dòng mang nhãn == [dòng đúng] | `D07_thieu`, `D07_lap`, `D07_them_dong_sai` |
| D08 | nhóm ca KHAI tường minh, không suy từ tiền tố; phân hoạch phủ kín, không giao nhau | `D08_suy_nhom_tu_tien_to` |
| D09 | tập ca đích rỗng, lạ, hoặc iterator đã tiêu thụ ⇒ HONG, không bao giờ `GIET` | `D09_bo_vat_hoa` và `D09b_cho_phep_rong` |
| D10 | ca đích đỏ sẵn trên bản gốc ⇒ HONG | `D10_bo_kiem_ban_goc` |
| D11 | neo đột biến phải xuất hiện đúng một lần | `D11_neo_cho_phep_nhieu_lan` |
| D12 | không để lại `.pyc`; hai đột biến cùng kích thước ghi trong cùng một giây vẫn chạy đúng mã của chính nó | `D12_bat_ghi_bytecode` |

Tổng tối thiểu: **12 cửa**. Đếm theo cửa, KHÔNG theo đột biến: D01, D07, D09 có nhiều đột biến, D05 có năm.

### Tiêu chí khác
- **N1 (M2):** `python .claude/dev/harness_dot_bien_test.py` in đúng dòng M3, với hai cặp số BẰNG NHAU và khác 0;
  dòng cuối `TONG: DAT`; rc=0. Đỏ khi: bất kỳ đột biến D01–D12 nào sống sót, hoặc một ca đỏ. Hai vế của mỗi
  cặp phải được đọc từ output, không tin rc (bài học "cổng xanh nhờ rc=0").
- **N2 (M3):** `python .claude/dev/ci_dang_ky_test.py` cho `ĐĂNG KÝ: K+1/K+1`, `PHẢN CHỨNG: P/P đỏ đúng`,
  `TỔNG: ĐẠT`, với K là số đăng ký trên base. Đỏ khi: thiếu dòng `MOI` (báo "test sống chưa đăng ký"), regex
  không khớp output, hoặc có dòng khác đổi (`git diff --numstat` trên tệp này phải ra `1 0`).
- **N3 (M1):** hàm tự kiểm phân hạng của harness (các mẫu rc và đột biến thật: vô can `KeyError` là
  `TIN_DUNG_GIA`, chỉ thêm chú thích là `SONG_SOT`, đột biến thật là `GIET`) đạt. Đỏ khi: đột biến sửa
  `phan_hang` (vd rc=4 thành `GIET`).
- **N4 (M1):** `python -m ruff check --select F` trên ba tệp: tệp mới sạch; delta so với base = 0.
- **N5 (toàn packet):** `git diff --numstat <base>..<head>` chỉ có ba tệp trong write_set; tổng dòng thêm
  ≤ 1.000. Đỏ khi: có tệp thứ tư, hoặc vượt trần.
- **N6 (M2):** mọi đột biến của harness đều GIET qua cơ chế phân hạng của chính harness, và lại được đối chiếu
  bằng một thước ĐỘC LẬP (tiến trình con đọc mã thoát và dòng `DO:`). Mục đích: harness hỏng phân hạng thì
  không thể tự báo xanh cho chính mình. Đỏ khi: đột biến D02/D03 lên `phan_hang` hay runner mà thước độc lập
  không bắt được.

## hinh_dang_ke_thua
Chép từ hồ sơ #674 (Issue #674 comment 5893485608, verdict lượt 1–6 trên `ops/review-674-ci-duong-nhanh`), đếm
theo SỐ LƯỢT REVIEW có lớp đó còn mở. Một lượt có nhiều biểu hiện chỉ tính một lần (§12).

| slug | số lượt xuất hiện ở #674 | trạng thái khi chuyển sang |
|---|---|---|
| `chot-yaml-chi-do-su-hien-dien` | 6 / 6 (lượt 1–6) | nợ có tên, chủ kho đóng theo phương án 1 (comment 5894382240); tầng cuối đã khoá ở #674: entrypoint tiến trình (`t91`), runner (`t92`), kết luận `main` (`t93`) |
| `bang-do-thieu-neo-va-thieu-kiem-ke` | 6 / 6 (lượt 1–6) | nợ có tên, như trên; tầng cuối: tập dòng `KIEM KE:` (`t94`) |

Bộ đếm §12 của packet này bắt đầu từ các số trên, KHÔNG từ 0. Hai lớp này xuất hiện ở bất kỳ lượt review nào
của #694 thì phải ghi tiếp số đếm. Chạm trần 3 lượt (Q7) thì là checkpoint của chủ kho.

Bộ đếm lời gọi Codex của #674 (chỉ để đối chiếu, không cộng dồn sang #694): 7 lời gọi (đo 15:37Z 29-09).

## Điều kiện dừng
- S1: chạm đường dẫn ngoài write_set ⇒ DỪNG.
- S2: `ci_dang_ky_test.py` còn người giữ khác lúc cấp lease hoặc lúc push ⇒ DỪNG.
- S3: một lớp finding xuất hiện ở lượt review thứ 3 của packet này, hoặc hết 3 lượt mà còn P1/P2/P3 ⇒ DỪNG,
  hỏi chủ kho kèm tóm tắt tự chứa.
- S4: vượt trần N5 ⇒ DỪNG trước review.
- S5: hết hạn lease ⇒ ngừng ghi, handoff theo §7.

## chua_do_duoc
1. **Hành vi trên Windows** (Q6): harness dùng API di động, nhưng không có phép đo trên Windows vì chủ kho chưa
   cho Windows CI.
2. **GitHub chạy `gate-registry` thế nào với mục mới:** chỉ đo được sau khi có PR thật; job ấy không thuộc
   required check.
3. **Lợi ích với consumer** (bớt dòng, hết lặp lớp finding): chỉ đo được khi một successor chuyển consumer đầu
   tiên. Không khai con số ở đây.
4. **Kích thước thật:** 700–900 dòng thêm chỉ là ƯỚC LƯỢNG (đo 17:0xZ 29-09 trên blob tham chiếu); trần N5 mới
   là chốt.
5. **K** (số đăng ký trên base) và **P** (số phản chứng) của N2 chưa ghi cứng vì sẽ trôi (đo 17:07Z 29-09 trên
   master `44620e8`: K = 22, P = 938). Đo lại trên base thật lúc cấp lease.
