# Đặc tả packet `no-p3-lease-spec-hash` r2 — nợ P3 (b1): `lease_publish.py check` đối chiếu băm spec và write set

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-lease-spec-hash` |
| `packet_issue` | #751 |
| `revision` | 2 |
| `thay_the_cho` | **r1**: `ops/specs/no-p3-lease-spec-hash-r1.md`, sha256 `17df1dccb4df520acb0d525cfc091dbee07fc8d878cf63f2fe2a4874a1a2fc6c`, commit `55bd0d24d299d20ff32a8b2dd42deb200295462e`. Thứ định danh r1 là cặp băm này, không phải tên nhánh chứa nó. r2 không sửa byte nào của r1; mọi closure, lease và `spec_hash` từ nay neo **r2**. |
| review của r1 | **Lượt 1**, reviewer Claude Sonnet 5.5 chạy bằng subagent (tự khai): `verdict: changes_requested`, `reviewed_sha` `55bd0d24d299d20ff32a8b2dd42deb200295462e`, **2 P1 · 5 P2 · 4 P3 = 11 lớp**. `VERDICT.md` sha256 `41cd3014b7aa57edb871f53f58eca31e31bad948c804f809fd2196ae2b766caf`; `HINT.patch` (chỉ văn bản đặc tả, 24 hunk, không chứa mã cổng) sha256 `d08878ed0bc0e75b3dcd97d5fbdfc03a0d0092b240e636cbfab1a282b1753aa7`. Thứ định danh hai tệp là băm, không phải nơi lưu. Cách r2 đóng từng lớp: mục **Thay đổi so với r1**. |
| `nguon_cap_viec` | Sổ nợ P3 mục 4: review wp685 lượt 2–5 đo `lease_publish.py check` không đọc `spec_hash`, `spec_sha256_required`, `plan_hash`, `write_set_hash`, `spec_path` (VERDICT review lượt 5 r28 sha256 `d3f1d9db4896efe8c1b62112a3d0aa479b64c5dc110da1d323b3297d7e7c45fb`, M11: đột biến D2, D3, D5, D6, D7 cho rc=0 cả năm) — **KHÔNG ĐO ĐƯỢC từ kho**: đo lại 15-10-2026 09:00:56Z, 0/825 blob khác nhau có tên tệp chứa `verdict` (không phân biệt hoa thường) trên 535 ref khớp băm này (reviewer lượt 1 đếm 1097 theo cách đếm khác, cũng 0); "Sổ nợ P3" sống ở phiên điều phối, ngoài kho; cùng nguồn ấy được trích ở mục Số đo nền cho "VERDICT lượt 5 M10". Vế "`check` không đọc các trường ấy" ĐÃ ĐO LẠI: `grep -cE` năm tên trong `ops/lease_publish.py` tại `6f121a3` = 0 dòng (09:09:38Z). Ngưỡng chủ kho #698 `6094652521`. Cách tách và phạm vi do chủ kho chốt 15-10-2026 (Q7, Q8). **Quyết định chủ kho 15-10-2026 cho r2** (truyền qua phiên điều phối khi giao soạn r2): test mới phải đăng ký vào sổ test sống `.claude/dev/ci_dang_ky_test.py`. Đường dẫn comment neo quyết định ấy: KHÔNG ĐO ĐƯỢC từ phiên soạn r2 — xem `depends_on` (5). |
| `review_class` | **sensitive** — `ops/lease_publish.py` là cổng cấp lease (authority). Trần ADR-0044: ≤ 3 tệp, ≤ 300 dòng thêm. Theo cổng: `_BANG_LOP` (`ops/lease_publish.py` dòng 59) gán `sensitive` cho `ops/lease_publish.py`; hai tệp còn lại của write set không có trong bảng nên rơi về `sensitive` (chú thích dòng 56–58: đường không biết ⇒ `sensitive`). |
| `executor` · `reviewer` | Claude (executor). Reviewer: `ops/lease_publish.py` là cổng cấp lease (security path), lớp `sensitive` ⇒ ADR-0036 dòng 9–10 và PROTOCOL §8 dòng 705–707 đòi **Codex cross-review hoặc `human_audited`**; `review_deferred` bị cấm cho phạm vi này và `same_provider_approved` một mình không thay được (dòng 696). Subagent Claude Sonnet chỉ là lượt PHỤ (`same_provider_approved`); bộ chọn `.claude/dev/chon_reviewer.py` cho packet này (sensitive, 3 đường dẫn của write set r2, 210 dòng, lượt 1) trả `claude-fable-5`/`xhigh` (đo lại 08:55:16Z; giống hệt với 2 đường dẫn/280 dòng của r1), và Sonnet không nằm trong allow-list `MO_HINH_CHO_PHEP` của nó (dòng 7). Đường dự phòng khi Codex không làm mới được (đo 15-10: `SAP_HET_HAN`): `human_audited` — KHÔNG merge chỉ với Sonnet. Chỉ P1/P2 chặn merge. |
| `base` | `origin/master` `6f121a3810045af27bf65eb723edf36b29e387f2` (đo 15-10 ~06:10Z). Đo lại 08:48Z–09:31:46Z trên `cay-kho` (clone chỉ đọc ở `55bd0d2`, cha = `6f121a3`; ảnh chụp ref: `packed-refs` 05:57:10Z, 535 ref): mọi số nền dưới đây tính trên cây cố định `6f121a3` nên không trôi theo giờ. Nền TIẾP NỐI lúc cấp lease: `depends_on` (3). |
| `write_set` | `ops/lease_publish.py` · `ops/lease_publish_spec_hash_test.py` (MỚI) · `.claude/dev/ci_dang_ky_test.py` (+1 dòng `MOI`, Mục tiêu 6). Tệp thứ ba vào write set theo quyết định chủ kho 15-10 và lớp P1 `test-moi-chua-dang-ky-lam-do-gate-registry`; nó đang thuộc write set #748 ⇒ `depends_on`. |
| `depends_on` | **CHẶN cấp lease** cho tới khi ĐỦ năm điều kiện, đo lại lúc cấp (số trong ô này không thay được phép đo lúc cấp). **(1)** Packet #748 đã land vào `master` — không chỉ vào `mission/748/integration` (spec r10 của #748 khai PR nháp vào nhánh ấy). **(2)** Trên một clone ĐỦ ref — so `git ls-remote --heads origin` với `git for-each-ref refs/remotes/origin` (bỏ `HEAD`) theo tập tên VÀ OID: thiếu cục bộ 0, lệch OID 0; không chạy được ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp — `python ops/lease_publish.py ai-dang-giu .claude/dev/ci_dang_ky_test.py` ra `NGƯỜI_GIỮ 0`, rc 0; cùng phép cho `ops/lease_publish.py` và `ops/lease_publish_spec_hash_test.py`. **(3)** Nếu bất kỳ commit nào sau `6f121a3` trên `master` (gồm commit land của #748) đổi một tệp của write set hoặc một bộ đo nền của nghiệm thu (`ops/lease_publish_test.py`, `ops/ci_duong_nhanh_test.py`, `.claude/dev/ci_dang_ky_test.py`) ⇒ dời nền bằng revision mới và đo lại mọi số ở Số đo nền TRƯỚC khi cấp; không cấp trên nền `6f121a3`. Spec r10 của #748 khai cả ba bộ ấy trong write set (dưới), nên khả năng phải dời nền là cao. **(4)** Write set giao với packet anh em #752 (`no-p3-cong-cu-ho-so`): r1 của nó (commit `55bd0d2`) thêm hai tệp `ops/*_test.py` mức đỉnh nên cũng phải đăng ký vào `.claude/dev/ci_dang_ky_test.py` (đo 08:59:10Z: thêm hai tệp ấy vào cây `6f121a3` ⇒ `ĐĂNG KÝ: 25/23`, `TỔNG: ĐỎ`) ⇒ hai lease KHÔNG được đồng thời; packet land sau phải qua điều kiện (3). **(5)** Có bằng chứng bền (đường dẫn comment) cho quyết định chủ kho 15-10 về sổ test sống VÀ cho đồng ý đi tiếp ở ngưỡng L4 (mục Hình dạng kế thừa). **Hiện trạng** đo 08:48Z–08:59Z trên ảnh chụp `cay-kho` (không fetch thêm, nên KHÔNG phải trạng thái máy chủ): lease r9 của #748 `wp748-r9-g9-claude-windows-20261015` (nhánh `ops/wp748-r9-g9-lease`, commit bia mộ `9b56cbc2`) khai `.claude/dev/ci_dang_ky_test.py` và `ops/lease_publish_test.py` trong write set 9 đường dẫn, hạn `2026-10-15T13:07:00Z`, mang `da_bi_thay_the: wp748-r10-g10-claude-windows-20261015`; spec r10 `ops/specs/wp748-windows-gates-r10.md` (commit `2c03974c`, sha256 `734dc22bb91432f18ec521ec2762c65402b308316b4747d34dacb8460eddff62`) khai write set 11 đường dẫn gồm `.claude/dev/ci_dang_ky_test.py`, `ops/lease_publish_test.py`, `ops/ci_duong_nhanh_test.py`; TỆP lease r10 không có trong ảnh chụp ⇒ ai đang giữ lúc này: **KHÔNG ĐO ĐƯỢC**. Blob lease chưa hết hạn trên 535 ref lúc 08:54:34Z: 1 (chính r9, đã bia mộ). Năm điều kiện: chưa thoả hoặc chưa đo. |
| `kich_thuoc` | 3 tệp — **đúng trần** sensitive, dư 0 tệp: mọi nhu cầu tệp thứ tư (ví dụ `ops/README.md`, Ngoài phạm vi) là vượt trần ⇒ dừng TRƯỚC review và soạn revision. Ước ≤ 210 dòng thêm theo `git diff --numstat`, trần cứng 300 (ADR-0044 dòng 5). Đo lại bản dựng tham chiếu của reviewer trên clone `6f121a3` (15-10 08:51Z–09:04Z): `lease_publish.py` +58/−0, `ci_dang_ky_test.py` +1/−0, test dạng bảng 144 dòng (24 ca) ⇒ 203 ≤ 300, dư 97; bản test viết tay từng ca (15 ca) 215 dòng ⇒ 58 + 1 + 215 = 274 ≤ 300, chỉ dư 26. Bỏ ràng buộc cứng "`lease_publish.py` ≤ 90 / test ≤ 190" của r1: nó sai với phép đo, chỉ giữ tổng ≤ 300. |

## Thay đổi so với r1

r2 áp nguyên 24 hunk của `HINT.patch` lên bản sao r1 (`patch -p0 --fuzz=0`, rc 0; kết quả 154 dòng, trùng từng byte bản mong đợi của reviewer), rồi sửa tiếp theo các hàng (a)–(k) ở bảng thứ hai. Mọi con số mới đều đã đo lại trên `cay-kho` hoặc clone của nó, kèm thời điểm; số nào chưa đo lại được thì ghi rõ là số của reviewer.

| # | hạng | slug | chỗ sửa trong r2 |
|---|---|---|---|
| 1 | P1 | `chot-trong-kiem-lam-do-t191-va-t01` | Mục tiêu 1 (hàm `kiem_bam` NGOÀI `kiem()`, `kiem()` byte-identical, người gọi `kiem()` đúng tên); A6b mới; A6 (ii) đòi `lease_publish_test.py` delta 0 trên ứng viên. |
| 2 | P1 | `test-moi-chua-dang-ky-lam-do-gate-registry` | `write_set` thêm `.claude/dev/ci_dang_ky_test.py`; Mục tiêu 6 mới (hàng h); A7; Ngoài phạm vi; `depends_on` (hàng a). |
| 3 | P2 | `ref-doc-blob-khong-xac-dinh-va-a6-vo-nghia` | Số đo nền (giải thích "5 lệch" thay bằng số đo); Mục tiêu 1 (`HEAD` của `_goc_kho`, không có "ref chứa lease"); A6 (i) viết lại. |
| 4 | P2 | `bia-mo-tien-nhiem-do-khi-spec-sua-tai-cho` | Mục tiêu 5 mới (miễn bia mộ, lý do viết lại theo thiết kế r2 — hàng b); A5b; Ngoài phạm vi (rút lời khai "không bị kiểm lại"). |
| 5 | P2 | `thu-tu-chot-va-dem-hinh-dang-khong-co-tieu-chi` | A3b mới; Hình dạng kế thừa viết lại với số đếm đo được và bộ đếm tiền nhiệm. |
| 6 | P2 | `hai-truong-bam-khac-nghia-tu-choi-lease-wp709` | Mục tiêu 1 (luật hai trường); A2 ca 5; A2b mới, kèm một ca thêm (hàng c). |
| 7 | P2 | `ke-hoach-reviewer-khong-khop-luat-kho` | Hàng `executor` · `reviewer`. |
| 8 | P3 | `bang-ma-thoat-khong-nam-o-help` | Mục tiêu 3 (bảng `MÃ THOÁT` ở docstring đầu tệp; KHÔNG `print` trong `kiem()`). |
| 9 | P3 | `kich-thuoc-tach-90-190-khong-khop-phep-do` | Hàng `kich_thuoc` (3 tệp, tổng ≤ 300, không tách cứng). |
| 10 | P3 | `trich-dan-verdict-luot-5-khong-doi-chieu-duoc` | Hàng `nguon_cap_viec` (ba trạng thái cạnh trích dẫn). |
| 11 | P3 | `ca-bien-nho-va-bay-ham-giup` | Mục tiêu 1 (ba trạng thái, byte thô, băm sai dạng, NUL, `write_set` không phải chuỗi); Mục tiêu 4 (hermetic, đa nền); A4b mới. |

Ngoài HINT, hoặc lệch HINT:

| hàng | chỗ | vì sao |
|---|---|---|
| (a) | `depends_on` mới | Chỉ thị phiên điều phối + quyết định chủ kho 15-10: tệp thứ ba của write set đang thuộc #748. |
| (b) | Mục tiêu 5, lý do | HINT dẫn chứng `ci_duong_nhanh.py::kiem_lease` đỏ trên hai lease HẾT HẠN, đo ở bản dựng chốt TRONG `kiem()`. Với thiết kế r2 (chốt ngoài `kiem()`), lease hết hạn đi `kiem(bo_qua_han=True)` và không chạm `kiem_bam`; `ops-publish-lease.yml` bỏ qua lease ĐÃ đăng ở rc 9 trước khi tới `check`. Lý do miễn vẫn đứng nhưng hẹp hơn: lease CÒN HẠN bị chạm trong PR đi qua `check`. Viết lại cho khớp phép đo. |
| (c) | A2b, ca thêm | `spec_sha256_required` SAI + `spec_hash` KHỚP ⇒ 13. Đột biến "khớp một trong hai là đủ" SỐNG SÓT bộ tham chiếu 24 ca của reviewer (đo 08:59:51Z–09:00:00Z: 24/24) và chết ở ca mới (08:56:01Z: rc 0 thay vì 13). |
| (d) | Ngoài phạm vi + Chưa đo được, Windows | HINT khai bộ test mới "chạy cả trên windows-latest ở lượt master … lần merge là lần đo Windows đầu tiên". SAI tại `6f121a3`: `ci.yml` dòng 50–53 chỉ thêm `windows-latest` khi `workflow_dispatch` hoặc PR gắn nhãn `windows`; push `master` chỉ ubuntu (ADR-0049, Accepted 2026-09-16, bỏ `github.ref == 'refs/heads/master'`). |
| (e) | Mục tiêu 1, A4b, CRLF | Số băm CRLF của HINT (`3d6b6492…`, `1a33e19c…`) không tái lập được. Đo lại 09:01:42Z: blob 6 byte `61 0d 0a 62 0d 0a` có băm byte thô `58055bdc…`, qua `GOI_GIT` thành `911169dd…`. Viết bằng byte hex, không dùng chuỗi thoát. |
| (f) | Mục tiêu 1, NUL | Cơ chế cụ thể: `subprocess` ném `ValueError: embedded null byte`; `Path.is_file()` KHÔNG ném (Python 3.11.15) — nên chốt NUL phải đứng trước lời gọi `git`. |
| (g) | A4, A7 | A4: đột biến bỏ `sorted` làm đỏ 2 ca, không phải 1 (đo 09:02:33Z). A7: số đăng ký viết theo N của nền lúc cấp lease, vì #748 hoặc #752 có thể đổi N. |
| (h) | Mục tiêu 6 mới | L2: mỗi đường dẫn của write set phải có một mục tiêu chiếu vào nó; HINT chỉ đặt tệp thứ ba ở `write_set`, A7 và Ngoài phạm vi. |
| (i) | Mục tiêu 1, Ngoài phạm vi | `ops/README.md` §Dùng bước 2 bảo chạy `check` TRƯỚC khi commit; với chốt mới, spec CHƯA commit ⇒ vắng tại `HEAD` ⇒ 13. Thông điệp phải nói điều đó; sửa README là nợ (trần 3 tệp đã kín). |
| (j) | Mục tiêu 3 | HINT nêu "bảng đang thiếu 11, 12" mà không nói có phải thêm không; r2 chốt: chỉ thêm hàng 13. |
| (k) | Mục tiêu 1, vị trí | HINT nói "`lenh_check` gọi nó SAU `kiem()`"; r2 khai cứng thêm: ngay sau dòng gọi `kiem()`, TRƯỚC mọi `print`, để rc 13 không đi kèm dòng "ĐĂNG ĐƯỢC". |

## Số đo nền (đo 15-10-2026 ~06:15Z trên cây `origin/master` `6f121a3`, đơn vị ghi rõ; đo lại 08:48Z–09:31:46Z trên `cay-kho` và clone của nó)

- Bảng mã thoát hiện có: `RC_OK 0`, `RC_THAM_SO 2`, `RC_TU_CAP 4`, `RC_NEO 6`, `RC_NOI_DUNG 8`, `RC_DA_DANG 9`, `RC_LOP 10`,
  `RC_DANG_GIU 11`, `RC_KHONG_XAC_DINH 12` (`ops/lease_publish.py` dòng 44–52). Mã `13` chưa dùng.
- 150 tệp `ops/leases/*.yaml`. 97 lease có cả `spec_path` và (`spec_hash` hoặc `spec_sha256_required`): 92 khớp băm tệp
  spec ĐANG Ở master, 5 lệch (đo lại 09:00:56Z: 4/5 là lease TIỀN NHIỆM mang `da_bi_thay_the` trong chuỗi revision
  `gate-tach-job-cat-chi-phi-exec-1…1r4` và `wp461-…-exec-1`, mà lease KẾ NHIỆM dùng CÙNG `spec_path` với băm mới; 1/5 là `…-exec-1r4`,
  cuối chuỗi, spec sửa sau khi cấp). Đọc ở chính master — ref CHỨA các lease ấy — vẫn lệch 5/5; đọc ở commit THÊM lease khớp 4/5, ở commit
  SỬA lease lần cuối khớp 1/5. Nên "5 lệch" KHÔNG là lý do cho "blob thay vì cây làm việc": lựa chọn ấy đứng bằng A3, không bằng con số
  này.
- 59 lease có `write_set` và `write_set_hash`: 5 lease khai `write_set_hash_scope: sorted NFC casefold exact …` và khớp công
  thức (a) dưới đây; **54 lease không khai scope** và KHÔNG khớp công thức (a) — chúng dùng công thức cũ khác (ví dụ "cách 1/
  cách 2" của wp685, VERDICT lượt 5 M10). Lease mẫu kiểm tay: `wp748-r9-g9-claude-windows-20261015` `3cd3f09c…` khớp (a).
  Đo lại 08:50:38Z bằng kịch bản chỉ-đọc `baseline.py` của reviewer: 150 · 97 · 92 · 5 · 59 · 5 · 54 · 0/54 khớp (a), khớp từng số.
- Bộ đo nền của nghiệm thu, trên clone `--shared` của `cay-kho` ở `6f121a3` (đơn vị: ca, đột biến, mục đăng ký):
  `env -u GITHUB_ACTOR python -B ops/lease_publish_test.py` ⇒ `lease_publish: 265/265 đạt; đã chạy=265, bỏ qua=0`, rc 0 (09:01:27Z–09:11:21Z);
  `python -B .claude/dev/ci_dang_ky_test.py` (không `--chay`) ⇒ `ĐĂNG KÝ: 23/23`, `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT`, rc 0
  (09:04:05Z); `python -B ops/ci_duong_nhanh_test.py` ⇒ `CA: 104/104 dat`, `DOT BIEN: 383/383 bi giet dung ly do`, `TONG: DAT`, rc 0
  (09:22:44Z–09:25:42Z); `ruff check --isolated --select F` (ruff 0.15.8) trên `ops/lease_publish.py`
  ⇒ 2 F841 sẵn có ở dòng 198–199 (09:05:35Z).

## Mục tiêu

1. **[`ops/lease_publish.py`] Băm spec.** Hàm MỚI `kiem_bam(lease, tep, goc) -> list[str]` đặt NGOÀI thân `kiem()`; `lenh_check` gọi nó
   SAU `kiem()` (nên rc 4/6/8/10 luôn thắng, không còn "vị trí" để chọn), `kiem-github` KHÔNG gọi nó (nên lease đã đăng vẫn ra rc 9).
   Vị trí khai cứng: ngay sau dòng `lease, neo = kiem(...)` của `lenh_check` (dòng 2294 ở nền), TRƯỚC mọi `print` của lệnh, để rc 13
   không bao giờ đi kèm dòng "ĐĂNG ĐƯỢC"; `lenh_body` và `kiem_github` không đổi.
   `kiem()` giữ BYTE-IDENTICAL thân và chữ ký trả về 2 phần tử, vì `ops/lease_publish_test.py` (ngoài write set, thuộc #748) có `t191`
   (duyệt AST, đòi MỌI chốt trong `kiem()` được `t190` phủ ở nhánh đã đăng) và `t01` dòng 705 (`checked, _ = mod.kiem(...)`). Đo
   15-10-2026 trên bản dựng ĐÚNG CHỮ r1 (chốt trong `kiem()`, trả 3 phần tử): `lease_publish_test.py` 263/265, đỏ đúng `t01` ("too many
   values to unpack") và `t191` ("`_kiem_bam_spec` … KHONG_CHAM"); bản dựng ngoài `kiem()`: 265/265 (nền 265/265). Đo lại
   09:01:27Z–09:22:41Z trên clone `6f121a3`: nền 265/265; bản dựng ngoài `kiem()` của reviewer 265/265; bản dựng đúng chữ r1 chạy riêng
   từng ca: `t01_executor_assurance_target_is_not_review_verdict` 0/1 (`ValueError: too many values to unpack (expected 2)`) và
   `t191_MOI_chot_cua_kiem_deu_duoc_t190_phu_o_nhanh_DA_DANG` 0/1 (`_kiem_bam_spec`, `_kiem_bam_write_set`: `KHONG_CHAM`); con số trọn bộ
   263/265 của bản ấy là của reviewer, lượt soạn r2 không chạy lại trọn bộ. Người gọi
   `kiem()` là `check` (dòng 2294), `body` (dòng 2314), `kiem-github` (2 chỗ, dòng 1280 và 1282) — KHÔNG gồm `kiem-thu-hoi-github`
   (`lenh_kiem_thu_hoi_github` dòng 2206–2290 không gọi). Nếu lease có
   `spec_path` (chuỗi) VÀ ít nhất một trong `spec_hash`, `spec_sha256_required` (chuỗi 64 hex thường), đọc **blob** của
   `spec_path` tại **`HEAD` của `_goc_kho(tep, goc)`** (lease được đọc từ ĐĨA qua `_doc_yaml`; không có ref nào được đọc — "cùng ref mà
   `kiem` đọc lease" không tồn tại; lease chưa commit mà spec đã commit vẫn được kiểm, spec chưa commit ⇒ vắng ⇒ 13, và thông điệp phải
   nói "spec phải đã commit tại HEAD"; không đọc spec từ cây làm việc). Với người tiêu thụ chính, `ops-publish-lease.yml` chạy bộ kiểm
   lấy từ `origin/master` trên cây được đẩy (`--root .`, dòng 98–99 và 216), nên `HEAD` là commit được đẩy, và chốt mới chỉ có hiệu lực
   cho đường đăng SAU khi land vào `master`. Tính sha256 BYTE THÔ và so với
   `spec_sha256_required` (và `spec_hash` KHI NÓ LÀ TRƯỜNG BĂM DUY NHẤT). Lệch ⇒ `Chan(RC_SPEC_LECH, …)` với `RC_SPEC_LECH = 13` mới,
   thông điệp nêu trường, giá trị khai, giá trị
   đo. Ba trạng thái: git chạy được mà blob vắng ⇒ `RC_SPEC_LECH`; git/`.git`/`HEAD` không dùng được (cây `git archive`, PATH không có
   git) ⇒ `RC_KHONG_XAC_DINH` 12. Đọc BYTE bằng `subprocess` trực tiếp, KHÔNG qua `GOI_GIT`/`_git` (đo lại 09:01:42Z trên
   `ops/lease_publish.py` của `6f121a3`: `_git` trả `Chan 12` cho blob vắng; `GOI_GIT` decode UTF-8 rồi đổi CRLF thành LF, nên blob 6 byte
   `61 0d 0a 62 0d 0a` cho băm `911169dd…` — đúng băm của 4 byte `61 0a 62 0a` — thay vì băm byte thô `58055bdc…`). Băm có mặt mà không
   phải 64 hex thường ⇒ 13 (thông điệp như `_kiem_neo_prompt` dòng 969–971: "phải là 64 ký tự hex thường"), `null` = vắng;
   `spec_path` chứa NUL ⇒ 13 (đo lại 09:01:56Z: không chặn thì `subprocess` ném `ValueError: embedded null byte` và bản dựng đúng chữ r1
   ra rc 1 kèm traceback; `Path.is_file()` thì KHÔNG ném, trả sai, nên chốt phải đứng TRƯỚC lời gọi `git`); `write_set` có phần tử
   không phải chuỗi ⇒ 13 (không để `TypeError`).
   Hai trường cùng có mặt: CHỈ `spec_sha256_required` quyết định — khớp blob ⇒ qua bất kể `spec_hash`, lệch ⇒ 13 bất kể `spec_hash`
   (hình dạng wp709: `spec_hash f569b613…` ≠ `spec_sha256_required f739b4aa…` = băm blob; đo lại 08:54:34Z: 12 blob lease trên 535 ref
   có cả hai trường, 10 bằng nhau, 2 khác nhau — `wp709-exec-g1/g2-codex`;
   PROTOCOL §3.2: `spec_hash` là băm của Packet Spec, không bắt buộc bằng băm byte của tệp). Thiếu `spec_path` hoặc thiếu
   cả hai trường băm ⇒ **không kiểm,
   không đỏ** (lease cũ); dòng kết quả của `check` phải nói rõ "spec: không khai — không kiểm".
2. **[`ops/lease_publish.py`] Băm write set.** Nếu lease có `write_set` (danh sách chuỗi), `write_set_hash` VÀ
   `write_set_hash_scope` bắt đầu bằng `sorted NFC casefold exact`: tính (a) =
   `sha256(json.dumps(sorted(unicodedata.normalize("NFC", p).casefold() for p in write_set), ensure_ascii=False, separators=(",", ":")).encode("utf-8"))`
   và so; lệch ⇒ `RC_SPEC_LECH`. Scope vắng hoặc giá trị khác ⇒ **không kiểm, không đỏ**, và `check` in "write_set_hash:
   scope không nhận ra — không kiểm" (54 lease cũ ở trên rơi vào nhánh này).
3. **[`ops/lease_publish.py`] Dòng xác nhận là bằng chứng.** Khi kiểm đạt, `check` in băm ĐO được (12 ký tự đầu) cho spec và
   write set — theo nếp docstring `kiem` (dòng 1010–1016): dòng xác nhận phải đi kèm việc kiểm, nên `kiem_bam` TRẢ các dòng bằng chứng
   (băm ĐO) cho `lenh_check` in; KHÔNG `print` trong `kiem()` (`body` dùng chung `kiem()` và stdout của nó là thân comment). Bổ sung
   `RC_SPEC_LECH` vào bảng `MÃ THOÁT` ở docstring đầu tệp (dòng 18–26): `--help` KHÔNG in bảng ấy (`argparse` nhận `description` là DÒNG ĐẦU của `__doc__`, dòng 2413;
   đo lại 09:09:38Z: `--help` chỉ in dòng "Cổng chặn cho đường ĐĂNG LEASE BẰNG GIT.", 0 dòng chứa `MÃ THOÁT`). Chỉ thêm hàng `13`; bảng còn thiếu 11, 12 là nợ sẵn có, KHÔNG thuộc packet
   (để executor khỏi phải đoán).
4. **[`ops/lease_publish_spec_hash_test.py`] Phản chứng.** Bộ test MỚI, tự đứng (không import `ops/lease_publish_test.py`,
   vì tệp đó đang thuộc write set #748), dựng kho git tạm bằng `git init` trong thư mục tạm, commit spec + lease, gọi
   `lease_publish.py check` như tiến trình con, HERMETIC: xoá `GITHUB_ACTOR` và `GIT_*` khỏi env con (đo 15-10: bộ 15 ca cho 15/15 khi
   biến không đặt, 0/15 khi `GITHUB_ACTOR=notebyme88` — cổng trả rc 4 cho mọi ca; đúng sự cố N9 của `lease_publish_test.py`; đo lại
   09:11:09Z–09:11:37Z trên bản dựng đúng chữ r1: bản 15 ca của reviewer có xoá `GITHUB_ACTOR` cho 15/15 với cả ba giá trị, bản gỡ dòng
   xoá cho 15/15, 0/15, 15/15 khi biến không đặt, `notebyme88`, `ducthangho`), và đọc rc +
   stdout; ca `kiem-github` dùng `gh` giả ghi ra thư mục tạm trên PATH. Ca nào phụ thuộc nền (`gh` giả chạy bằng shebang, PATH rỗng) phải
   hoặc chạy được trên Windows, hoặc tự BỎ QUA CÓ TÊN kèm lý do khi `os.name == "nt"` — không được im lặng xanh. Chạy được bằng
   `python -B ops/lease_publish_spec_hash_test.py`,
   in `N/N` và trả 0 khi đạt.
5. **[`ops/lease_publish.py`] Miễn bia mộ.** Lease mang `da_bi_thay_the` (chuỗi khác rỗng) ⇒ `kiem_bam` KHÔNG so băm và in
   "spec/write_set: lease đã bị thay thế (bia mộ) — không kiểm băm". Lý do (đo lại 09:00:56Z): chuỗi revision dùng LẠI `spec_path` với băm
   mới và ghi bia mộ cho lease tiền nhiệm KHI CÒN HẠN — 4/5 lease lệch ở master là tiền nhiệm như vậy (ba lease
   `gate-tach-job-cat-chi-phi` có `da_bi_thay_the_luc_utc` 07:50:35Z, 09:44:51Z, 10:17:12Z ngày 07-09, đều trước hạn; `wp461-…-exec-1`
   bị bia mộ ở commit `6635379` lúc 2026-09-07T05:36:33Z, trước hạn 2026-09-08T03:05:00Z, cùng commit với việc sửa spec tại chỗ); lease
   thứ 5 (`…-exec-1r4`) là cuối chuỗi, spec sửa sau khi cấp nên vẫn ra 13 (A6 liệt kê nó). Người tiêu thụ chạm tới `kiem_bam` (đọc mã ở
   `6f121a3`): `ops/ci_duong_nhanh.py::kiem_lease` chạy `lease_publish.py check` cho MỌI lease CÒN HẠN bị chạm trong PR (dòng 541), nên
   một PR sửa spec tại chỗ và ghi bia mộ vào tiền nhiệm còn hạn — đúng hình dạng `6635379` — sẽ đỏ `gate-ops` nếu không miễn; lease HẾT
   HẠN đi `kiem(bo_qua_han=True)` (dòng 539, `MA_KIEM_HET_HAN` dòng 121–124) nên không chạm `kiem_bam`; `ops-publish-lease.yml` chạy
   `kiem-github` TRƯỚC và bỏ qua khi rc 9 (dòng 204–207), nên chỉ lease CHƯA đăng mới tới `check`. Bằng chứng hành vi: A5b.
6. **[`.claude/dev/ci_dang_ky_test.py`] Đăng ký bộ test mới.** Thêm ĐÚNG MỘT dòng vào dict `MOI` (dòng 37–53 ở `6f121a3`): khoá
   `"ops/lease_publish_spec_hash_test.py"`, giá trị CHÉP NGUYÊN chuỗi mẫu của dòng `"ops/nhanh_don_duoc_test.py"` (dòng 52; mẫu khớp
   dòng in cuối dạng `N/M`, hai nhóm số). Không sửa dòng nào khác của tệp. Lý do: `kiem()` của sổ (dòng 579) đòi mọi `ops/*_test.py`
   mức đỉnh (`tim()`, dòng 83–94) nằm trong `DANG_KY` (dòng 80); sổ CHẠY các bộ `MOI` trong job `gate-registry` (`chay_moi` dòng 967;
   `ci.yml` dòng 895 `--chay`), nên đây cũng chính là cách nối CI — không sửa `ci.yml`. Đo lại 09:04:05Z–09:04:23Z trên clone `6f121a3`:
   nền `ĐĂNG KÝ: 23/23`, `TỔNG: ĐẠT`; thêm tệp test chưa đăng ký ⇒ `ĐỎ: test sống chưa đăng ký: ops/lease_publish_spec_hash_test.py`,
   `ĐĂNG KÝ: 24/23`, `TỔNG: ĐỎ`, rc 1; thêm dòng `MOI` ⇒ `ĐĂNG KÝ: 24/24`, `TỔNG: ĐẠT`, rc 0, `git diff --numstat` = `1 0`.

## Nghiệm thu

- **A1 (băm spec khớp ⇒ qua):** lease có spec khớp ⇒ rc 0, stdout chứa 12 ký tự đầu băm đo. ĐỎ khi: đột biến gỡ dòng in ⇒
  ca kiểm chuỗi in ĐỎ.
- **A2 (lệch ⇒ 13):** sửa 1 ký tự `spec_hash` ⇒ rc 13; sửa 1 ký tự `spec_sha256_required` ⇒ rc 13; thêm 1 byte vào spec SAU
  khi tính băm ⇒ rc 13; `spec_path` trỏ tệp vắng ⇒ rc 13; hai trường băm CÙNG sai và khác nhau ⇒ rc 13 (xem A2b). Năm ca riêng. ĐỎ khi:
  đột biến gỡ phép so trong `lease_publish.py` ⇒ ít nhất bốn ca ĐỎ (rc 0 thay vì 13; đo lại 09:02:33Z trên bản dựng tham chiếu: 5 ca)
  — đột biến chạy trên BẢN SAO tạm
  (CLAUDE.md: đột biến không ghi tệp thật).
- **A2b (hai trường, hình dạng wp709):** (i) `spec_hash` KHÁC nhưng `spec_sha256_required` = băm blob ⇒ rc 0; (ii) `spec_sha256_required`
  SAI nhưng `spec_hash` = băm blob ⇒ rc 13. ĐỎ khi: đột biến so cả hai trường ⇒ (i) ĐỎ (rc 13 thay vì 0); đột biến "khớp một trong hai
  là đủ" ⇒ (ii) ĐỎ (rc 0 thay vì 13). Đo lại trên bản dựng tham chiếu: đột biến thứ nhất đỏ đúng 1 ca (09:02:33Z); đột biến thứ hai
  SỐNG SÓT bộ 24 ca của reviewer (24/24, 08:59:51Z–09:00:00Z) và chỉ chết ở ca (ii) (08:56:01Z) — nên ca (ii) là bắt buộc. Lý do: ca "hai trường
  khác nhau ⇒ 13" của r1 từ chối `wp709-exec-g1/g2-codex` (lease codex 05–06-10-2026, đã dùng thật).
- **A3 (đọc tại `HEAD`, không tại cây làm việc):** commit spec + lease, rồi sửa spec trong cây làm việc KHÔNG commit ⇒ rc 0
  (đọc blob); và ngược lại commit spec sai + cây làm việc đúng ⇒ rc 13. ĐỎ khi: đột biến đổi sang đọc tệp từ đĩa ⇒ cả hai
  ca ĐỎ.
- **A3b (thứ tự chốt — chặn hình dạng (a)):** (i) lease HẾT HẠN + spec lệch ⇒ rc 8 (không 13); (ii) `kiem-github` (`gh` giả) + dấu "đã
  đăng" + spec lệch ⇒ rc 9 (không 13); (iii) lease còn hạn, chưa đăng, spec lệch ⇒ `check` rc 13. Đo lại bằng bộ tham chiếu của reviewer
  trên ba bản dựng: chốt trong `kiem()` TRƯỚC chốt hạn (đúng chữ r1) ⇒ (i) 13 (che rc 8), (ii) 13 (che rc 9), 17/24 (09:01:56Z); chốt
  trong `kiem()` SAU chốt hạn ⇒ (i) 8, (ii) 13, 18/24 (09:02:18Z); chốt ngoài `kiem()` ⇒ (i) 8, (ii) 9, (iii) 13, 24/24 (08:55:38Z). ĐỎ
  khi: đột biến đặt `kiem_bam` TRƯỚC `kiem()` ⇒ (i) ĐỎ; gọi `kiem_bam` ở nhánh đã đăng của `kiem_github` ⇒ (ii) ĐỎ — mỗi đột biến đúng
  một ca (đo lại 09:02:33Z).
- **A4 (write set):** scope `sorted NFC casefold exact …` + băm đúng ⇒ rc 0; sai 1 ký tự ⇒ rc 13; đổi thứ tự `write_set`
  (băm giữ) ⇒ rc 0 (vì sắp xếp); một đường dẫn viết hoa khác (casefold) ⇒ rc 0; dạng NFD của cùng tên ⇒ rc 0. ĐỎ khi: đột biến
  bỏ `casefold` ⇒ ca viết hoa ĐỎ; bỏ `normalize` ⇒ ca NFD ĐỎ; bỏ `sorted` ⇒ ca đổi thứ tự ĐỎ — ba đột biến, mỗi cái làm đỏ ÍT NHẤT ca
  đích của nó (đo lại 09:02:33Z: 1, 1 và 2 ca — bỏ `sorted` làm đỏ cả ca đổi thứ tự lẫn ca NFD).
- **A4b (ca biên):** blob CRLF 6 byte `61 0d 0a 62 0d 0a` + băm byte thô ⇒ rc 0; `spec_hash` 63 ký tự ⇒ 13 (không im lặng bỏ qua);
  `spec_path` chứa NUL ⇒ 13 (không traceback rc 1); PATH không có git ⇒ rc 12 (không phải 13). ĐỎ khi: đọc qua `GOI_GIT`/`_git` ⇒ ca CRLF
  ĐỎ; coi băm sai dạng là vắng ⇒ ca 63 ký tự ĐỎ; bỏ chốt NUL ⇒ ca NUL ĐỎ; gộp 12 vào 13 ⇒ ca git-vắng ĐỎ — bốn đột biến, mỗi cái một ca
  (đo lại 09:02:33Z trên bản dựng tham chiếu: 4/4).
- **A5 (lease cũ không đỏ):** lease không `spec_path` ⇒ rc 0 và stdout chứa "không khai — không kiểm"; lease có
  `write_set_hash` không scope ⇒ rc 0 và chứa "scope không nhận ra". ĐỎ khi: đột biến coi thiếu trường là lỗi ⇒ hai ca ĐỎ.
- **A5b (bia mộ):** lease CÒN HẠN mang `da_bi_thay_the`, spec đã sửa tại chỗ sau khi cấp (băm cũ) ⇒ `check` rc 0 và in "bia mộ — không
  kiểm băm"; cùng hình dạng nhưng KHÔNG mang `da_bi_thay_the` ⇒ 13. ĐỎ khi: đột biến bỏ miễn ⇒ ca đầu ĐỎ (rc 13 thay vì 0; đo lại
  08:59:51Z: bộ tham chiếu 23/24, đỏ đúng ca ấy).
- **A6 (không hồi quy):** (i) trên một bản `git clone` (KHÔNG `git archive`) ở `6f121a3`, với 150 lease: trong tiến trình,
  `kiem(bo_qua_han=True)` rồi `kiem_bam(...)`; rc ứng viên khác rc nền ĐÚNG cho tập lease đã khai trước kèm lý do. Đo lại 08:56:24Z trên
  clone `--shared` của `cay-kho` (kịch bản `a6c.py` của reviewer, bản dựng tham chiếu): 1 lease đổi
  (`gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906`, cuối chuỗi, spec sửa sau khi cấp: 0 → 13), 149 còn lại bằng nền (135 rc 0, 9 rc
  8, 5 rc 10); 36 lease được miễn bia mộ; 55 được kiểm spec và khớp; 3 được kiểm write set và khớp. Cách đo r1 KHÔNG đo gì: cây
  `git archive` không có `.git` (bản vá ra 13/12 cho mọi lease có spec), 5 lease `ops/**` mới nhất đều mang `thay_the_cho` nên NỀN đã ra
  rc 12 (số của reviewer: 12/12/12 — "trước/sau bằng nhau" là vô nghĩa), và lúc 08:54:34Z chỉ 1 blob lease chưa hết hạn trên 535 ref
  (`wp748-r9`, đã bia mộ) — "5 lease hiện hành" không tồn tại. (ii) `ops/lease_publish_test.py` chạy trên ứng viên: số ca đạt bằng
  nền, delta 0 (đo lại: nền `6f121a3` 265/265 lúc 09:01:27Z–09:11:21Z; bản dựng tham chiếu ngoài `kiem()` 265/265 lúc
  09:11:21Z–09:21:15Z). ĐỎ khi: bất kỳ ca nào của `lease_publish_test.py` đổi từ đạt sang trượt, hoặc tập
  lease đổi rc khác tập đã khai; đột biến bỏ miễn bia mộ ⇒ 5 lease đổi rc thay vì 1 (đo lại 08:56:24Z–09:02:44Z: 5, đúng bốn tiền nhiệm cộng
  `…-exec-1r4`).
- **A6b (`kiem()` bất biến):** `git diff -U0 6f121a3 -- ops/lease_publish.py` không có hunk nào nằm trong thân `kiem()` (dòng 1009–1114 ở
  nền) và `kiem()` vẫn trả đúng 2 phần tử. ĐỎ khi: đặt chốt trong `kiem()` ⇒ `t191` ĐỎ; trả 3 phần tử ⇒ `t01` ĐỎ (số của reviewer:
  263/265; đo lại 09:21:15Z–09:22:41Z chạy riêng từng ca trên bản dựng đúng chữ r1: `t01_executor_assurance…` 0/1,
  `t191_MOI…` 0/1).
- **A7 (cổng kho):** ruff F delta 0 (multiset) cho các tệp đổi (nền: 2 F841 sẵn có ở `lease_publish.py`; bản dựng tham chiếu: vẫn 2,
  test mới 0, `ci_dang_ky_test.py` có dòng `MOI` 0 — đo lại 09:05:35Z, ruff 0.15.8); sổ test sống: `python .claude/dev/ci_dang_ky_test.py`
  in `ĐĂNG KÝ: N+1/N+1` (hai số BẰNG NHAU) và `TỔNG: ĐẠT`, với N = số đăng ký ở nền lúc cấp lease (tại `6f121a3`: N = 23 ⇒ `24/24`);
  `ops/ci_duong_nhanh_test.py` (job `gate-ops`; bộ đột biến của nó có 3 đột biến trên `ops/lease_publish.py`) cho số ca và số đột biến
  bằng nền, `TONG: DAT` (đo lại: nền `6f121a3` 104/104 · 383/383 lúc 09:22:44Z–09:25:42Z; bản dựng tham chiếu
  ngoài `kiem()` + test + dòng `MOI` 104/104 · 383/383 · `TONG: DAT` lúc 09:25:42Z–09:28:42Z); kích thước ≤ trần sensitive. ĐỎ khi: bỏ dòng `MOI` ⇒ `test sống chưa đăng ký`,
  `N+1/N`, `TỔNG: ĐỎ` và `k01_so_dang_ky_nhan_muc_da_noi` ĐỎ (đo lại 09:28:42Z–09:31:46Z: cùng bản dựng, bỏ dòng `MOI` ⇒ `CA: 103/104`, `DOT BIEN:
  382/383`, `TONG: DO`, rc 1); `git diff --numstat` vượt 300 dòng thêm hoặc 3 tệp.

## Ngoài phạm vi (cố ý)

- `plan_hash`: không có quy ước chung về tệp plan (chủ kho chốt Q8).
- Sửa `ops/lease_publish_test.py`, `ci.yml` (đang thuộc write set #748). "Gắn test mới vào CI — ghi nợ" của r1 SAI về cơ chế: sổ test sống
  `.claude/dev/ci_dang_ky_test.py` đòi mọi `ops/*_test.py` mức đỉnh phải đăng ký, nên tệp test mới KHÔNG đăng ký làm ĐỎ `gate-registry`
  (đo: `ĐĂNG KÝ: 24/23`, `TỔNG: ĐỎ`) và `gate-ops` (`ops/ci_duong_nhanh_test.py`: `k01` đỏ). Đăng ký bằng MỘT dòng `MOI` (Mục tiêu 6) là
  cách nối đúng, không sửa `ci.yml`: registry CHẠY bộ `MOI` trong `gate-registry` (số của reviewer: `24/24`, rc 0, `bang_chung_xanh`
  đúng, kể cả khi `GITHUB_ACTOR=notebyme88`).
- **Windows của bộ test mới — không trigger tự động nào đo.** Tại `6f121a3`, `ci.yml` (dòng 50–53) chỉ thêm `windows-latest` cho
  `workflow_dispatch` hoặc PR gắn nhãn `windows`; push `master` chỉ chạy ubuntu (ADR-0049). Gắn nhãn lên PR đang mở KHÔNG tự sinh lượt
  chạy (`pull_request` không khai `types:`), phải kèm một cò mới. `launcher-windows.yml` CÓ chạy ở push `master` khi chạm `.claude/dev/**`
  (tệp thứ ba của write set chạm vùng ấy), nhưng nó chỉ gọi `launcher.py` và `launcher_test.py`: 0 dòng nhắc `ci_dang_ky_test` hay
  `lease_publish` (đo 09:12:35Z) — nên không đo bộ mới. Muốn có Windows trước merge: `workflow_dispatch` trên ref ứng viên (lease phải khai ngân sách CI tay cho việc ấy),
  hoặc ghi `KHÔNG ĐO ĐƯỢC` và nợ có tên. Mục tiêu 4 đòi các ca phụ thuộc nền tự bỏ qua CÓ TÊN, để lượt Windows nào chạy tới cũng không
  im lặng xanh.
- Sửa 54 lease cũ hay 5 lease lệch băm ở master — không phải việc của cổng mới. Lời khai cũ "chúng không bị kiểm lại trừ khi được đăng"
  SAI (đo 15-10-2026): `ops-publish-lease.yml` đưa mọi tệp lease ACM trong `before..sha` qua `kiem-github` rồi `check` (bỏ qua khi rc 9),
  và `ops/ci_duong_nhanh.py::kiem_lease` đưa mọi lease CÒN HẠN bị chạm trong PR qua `check` (Mục tiêu 5), nên mục tiêu 5 (miễn bia mộ) và
  A5b là bắt buộc, không tuỳ chọn.
- Nợ tài liệu `ops/README.md`, ngoài write set vì trần 3 tệp đã kín: bảng "Cổng chặn" thiếu rc 13 (như đã thiếu 10, 11, 12); §Dùng bước 2
  bảo chạy `check` TRƯỚC khi commit, mà với chốt mới spec CHƯA commit ⇒ rc 13.

## Hình dạng kế thừa

Chép từ lịch sử cổng `lease_publish.py` (CLAUDE.md, các mục "BIA MỘ", "rc=8 che rc=9", `t32`): (a) **chốt chạy trước che chốt sau** —
`kiem()` ném `rc=8` cho lease hết hạn TRƯỚC khi `rc=9` kịp chạy. Vị trí KHÔNG còn để executor "khai": `kiem_bam` chạy sau `kiem()` (nên
không che rc 4/6/8/10) và không chạy ở nhánh đã đăng của `kiem-github` (nên không che rc 9) — A3b khoá cả hai bằng đột biến; (b) **dòng
xác nhận không đi kèm việc kiểm** (docstring `kiem`) — A1 khoá. ĐẾM HÌNH DẠNG, đo lại 15-10-2026 trong chính `ops/lease_publish.py`: (a) ≥
**4** lần cùng hình dạng "chốt/tiền kiểm đứng trước đổi phán quyết của chốt sau", không phải 1 — 20-09-2026 `#568`/`#566` (dòng
1228–1236), #589 P1 24-09 (dòng 1238–1244, 1272–1280), và slug `unposted-error-precedence-changes` hai lượt liền (dòng 1160–1167 và 1198,
"lần thứ hai cùng slug"); (b) 1 lần. BỘ ĐẾM CỦA TIỀN NHIỆM (L4 chép từ biên nhận, không từ CLAUDE.md): hình dạng A "lời khai rộng hơn phép
đo" = 7 (`ops/reviews/README.md` dòng 482, `lease-dang-windows-review-3`) và 8 theo `ops/specs/t33-doi-shellcheck-r3.md` dòng 104, 266 (đo
23-08-2026); E = 4; D = 3 — r1 này không chép bộ nào, và chính nó mắc A ít nhất 3 lần (dòng 20–21, 75, 82). Lượt soạn r2 bắt thêm hai lời
khai rộng hơn phép đo nằm ngay trong `HINT.patch` (bảng lệch HINT, hàng b và d) — cùng hình dạng A; r2 ghi lại để người giữ kho quyết có
tăng bộ đếm hay không, không tự tăng. Ngưỡng "lần ba" (L4) ĐÃ CHẠM
với (a) và với A: trước khi cấp lease phải có bằng chứng bền (đường dẫn comment) chủ kho đồng ý tiếp — thiếu thì DỪNG (`depends_on` (5)).

## Chưa đo được

- Hành vi trên Windows (đường dẫn, NFC trên NTFS, ca `gh` giả, PATH rỗng) — packet chỉ đo Linux; ghi `KHÔNG ĐO ĐƯỢC`. Không trigger
  tự động nào sẽ đo thay (mục Ngoài phạm vi).
- Lượt Codex có chạy được không phụ thuộc làm mới đăng nhập (đo 15-10: `SAP_HET_HAN`, ảnh chụp cũ ~185 h).
- Ai đang giữ `.claude/dev/ci_dang_ky_test.py` lúc này: tệp lease r10 của #748 không có trong ảnh chụp `cay-kho`; trạng thái máy chủ
  không được đo ở bước soạn đặc tả (`depends_on`).
- Đường dẫn comment của quyết định chủ kho 15-10 về sổ test sống (`depends_on` (5)).
- VERDICT lượt 5 r28 `d3f1d9db…` và hai vế "đột biến D2, D3, D5, D6, D7 cho rc=0" (nguồn ngoài kho).
- `python .claude/dev/ci_dang_ky_test.py --chay` trọn bộ (bước CI, nặng) — lượt soạn r2 chỉ chạy bản không `--chay`; việc sổ CHẠY được
  bộ mới (`24/24`, `bang_chung_xanh` đúng) là số của reviewer.
