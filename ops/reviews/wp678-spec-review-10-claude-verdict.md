verdict: changes_requested
reviewed_sha: 42292b4219901137607d3fd9adda26d49f7cfd5e
spec_sha256: 892c80069e640a96d6b0498f9fcc5d66617606bfdfe433c4c16fcf6e2d5ee7e2
model/effort tự khai: Claude Opus 5.5 (`claude-opus-5-5`), effort max — KHÔNG phải codex. Chạy như SUBAGENT do phiên điều
phối giao (lượt 10), cùng họ Claude với phiên soạn r10 ⇒ KHÔNG độc lập khác họ. Model/effort là CẤU HÌNH được giao, không phải
runtime evidence (PROTOCOL :710–711): lượt này không sinh `modelUsage`, không có `session_run_id`; biên nhận của lượt (nếu ghi)
phải tự khai `che_do: subagent_trong_phien_dieu_phoi`, mức `review_deferred`. Có được giao qua định nghĩa `review-opus-max`
hay không: KHÔNG ĐO ĐƯỢC từ phía tôi (chỉ đo được băm tệp định nghĩa, Hướng 4). Không mạng, không đăng GitHub, không
commit/push, không sửa `cay-kho`; ghi chỉ dưới `$R/goi/` và các thư mục `mktemp -d -p "$R"`.

Kết luận nội dung: **0 P1 / 2 P2 / 2 P3** (theo lớp; 7 finding F10-1…F10-7).
P2: `thu-tu-677-bo-ngo-o-dieu-kien-cap` (VÁ SINH LỖI MỚI; lượt 7, 8, 9, 10) ·
`tuong-tac-677-kiem-ke-t70-chua-neu` (VÁ SINH LỖI MỚI; lượt 8, 9, 10).
P3: `hop-dong-dong-bang-thieu-neo` (CÒN MỞ — F9-4 đã vá thật, một biểu hiện có từ r7 mới tìm ra; lượt 1, 2, 7, 8, 9, 10) ·
`so-do-nen-khong-khop` (TÁI PHÁT; lượt 7, 8, 10).

Trả lời câu hỏi gốc, áp cho r10.
(1) Phạm vi: r10 đổi đúng những gì nó khai. Giống byte r9: §1, §2, §5, Phụ lục A; 14 hàng bảng gồm `objective`, mọi giá trị
closure (`change_policy_sha`, `effective_write_set`, `effective_review_class`, `required_checks`, `land_obligations`); A4–A7,
A10. A1 và A9 chỉ đổi số đo/ghi chú blob; hàng reviewer chỉ thêm "`20ec8d5`, và giữa … và `163fd5d`" (Hướng 6). Dời nền là
quyền Q8 điều kiện (4) đã trao, không vượt Q13.
(2) Làm đúng từng chữ r10 thì packet có land được không: có, không P1 — nhưng hai bảo đảm r10 tuyên bố rộng hơn phép đo của
chúng, đo được trên kho bare tại chỗ và trên bản sao suite: chuỗi lệnh cấp (1)/(4)/(5) CẤP NHẦM ở bốn ca chạy đúng từng dòng
(origin là mirror; `comm`/`awk` vắng ⇒ "0 dòng" là bằng chứng ÂM), và lời khai "Vế (iii) do chính `t193` canh trong suite"
không phủ bảy đường GỌI THẬT helper mà cả `t70` lẫn `t193` và mọi phép đo A8 đều xanh ở 3.11/3.12/3.13, trong khi `main()` dưới
seam `nt` ĐỎ (Windows chỉ chạy ở master). Cả hai lớp có cách vá đo được, đã đo (HINT nhóm 1, 2).
(3) Số hạng của việc dời nền `163fd5d`: mọi số đo lại được đều KHỚP — suite 198/198 ở 3.11 và 3.12, AST 11/0/10, tọa độ ca,
ruff 9 cùng tập, điểm nóng 122+4/26/9 và 128/32/10, đột biến `t70` (đủ bảng, kể cả 3.13), cổng biên nhận (5 số `_thieu`, 3 mẫu,
CLI `163fd5d`), A1, A3, phân rã 118 tệp, Q13 từng byte (BẢNG ĐO).
(4) Tín hiệu hội tụ §12 (chỉ báo; chủ kho đã quyết lặp tiếp ở Q13): chuyển tiếp 9→10 = **1/4 = 25%** đọc chặt §8.3 (chỉ
`dieu-kien-dung-12-doc-mot-chuyen-tiep` ĐÃ VÁ THẬT); **2/4 = 50%** nếu người điều phối tách F10-6 khỏi
`hop-dong-dong-bang-thieu-neo` thành lớp riêng. Chuỗi trước: 7→8 = 0/5, 8→9 = 2/7. Ba lượt trở lên: `thu-tu-677-…` (7, 8, 9,
10), `hop-dong-dong-bang-thieu-neo` (1, 2, 7, 8, 9, 10), `so-do-nen-khong-khop` (7, 8, 10). Chi tiết ở ĐỐI CHIẾU LƯỢT TRƯỚC.

## TIỀN KIỂM
- sha256sum $R/SPEC.md -> 892c80069e640a96d6b0498f9fcc5d66617606bfdfe433c4c16fcf6e2d5ee7e2 (khớp)
- git -C $R/cay-kho rev-parse HEAD -> 42292b4219901137607d3fd9adda26d49f7cfd5e (khớp) ⇒ không `blocked`.
- sha256sum $R/PROMPT.md -> 7321e3cb5e5aea4bd5ef084fd818192d60eee3df2296f9b5b570c9e144f3f3f5 (khớp băm điều phối trao)
- Hiện vật lượt 9: luot9/VERDICT.md bb5bf15b…10ee31, luot9/HINT.patch af52b8b5…c861 (khớp PROMPT). r9-r10.diff = diff -u SPEC-r9.md SPEC.md (sha256 phần thân d79eb331… cả hai). cmp SPEC.md với cay-kho/ops/specs/lease-id-ep-kieu-yaml-r10.md: khớp.
- git -C cay-kho diff --name-status 423b4ba 42292b4 ⇒ đúng 4 dòng A (r7, r8, r9, r10); log --diff-filter=A ⇒ r10 tạo bởi 42292b4, r9 bởi 2469f3e.
- PROMPT nhắc mà $R KHÔNG có: luot6/, q10-readback.json, r6-r7.diff (phần ấy của PROMPT là của lượt 7). Thay thế: readback-5911243074.json (Q10) … readback-5928886724.json (Q13).
- Khác lượt 9: mọi object nền đều CÓ trong kho.git (163fd5d, 20ec8d5, a6de9d1, 7e5958e, 5955819, eca94d1, blob 372cbfd/976915a, 35e23d7, 6112b89, 8e630c0 … cat-file -t ra commit/blob).
- Công cụ: python3.11 3.11.15 · 3.12.3 · 3.13.12, PyYAML 6.0.1, git 2.43.0, GNU patch 2.7.6, shellcheck 0.9.0, actionlint 1.7.7, ruff 0.15.8 (nhị phân). Thư mục đo: $R/do10.Nq9r (mktemp; TMPDIR trong đó).

## NHẬT KÝ TĂNG DẦN
- 10:22Z HƯỚNG 1 (chuỗi lệnh cấp, trọng tâm (1)) xong — xem BẢNG SĂN. Phát hiện: chuỗi CẤP NHẦM theo đúng chữ ở 4 ca (S7a, S7b: origin là mirror; S8a, S8b: thiếu comm/awk ⇒ "0 dòng" là bằng chứng âm).
- 10:28Z suite nền 163fd5d (2 clone dựng trong MỘT lệnh, python/python3 trỏ đúng bản): 3.11.15 198/198 rc=0 (10:14:10Z–10:20:25Z), 3.12.3 198/198 rc=0 (10:20:25Z–10:28:06Z); bỏ qua 0; vào 198 / ra QUA 198 mỗi lượt; 0 .pyc; status --porcelain --ignored 0 dòng. KHỚP r10.
- 10:28Z HƯỚNG 3 (đột biến t70/t193, 39 biến thể × 3.11/3.12/3.13) xong: tái lập ĐỦ bảng r10; thêm 8 đường mới — 7 đường (getattr, functools.partial, alias cấp module, lambda trong hàm bọc, decorator đóng gói, tham số mặc định, lớp) cho t70 1/1 + t193 1/1 + D/G−D/chỉ-lồng y nền, mà main() dưới seam nt ĐỎ "NGOÀI SỔ"; comprehension trong hàm bọc làm t193 3.11 ngược 3.12.
- 10:36Z quét ĐỘNG mọi ca dưới seam nt của t193 trên nền (3.12.3, 382,5 s, 198 ca): N = đúng 12 ca sổ, N == SO_BO_QUA (đúng cặp), N − D = ∅ ⇒ phép đo đề xuất không báo động giả; trên 8 biến thể mới (N1–N8) N − D = {t204} ở cả 3.11 lẫn 3.12 (bản ghi đầu của dòng này viết "7" — sai đếm, sửa thành 8).
- 10:31Z–10:34Z HƯỚNG 4 (biên nhận): năm số _thieu 0/0/1/2/0, ba mẫu kiem()/CLI rc 0/1/2, CLI kho thật 163fd5d "163 ĐẠT v2 · 11/11 · 42 NỢ · 0 vi phạm · 0 KDĐ · tổng 216" rc=0 — KHỚP. a6de9d1: cùng 174/11/42/0/227 nhưng 1 KDĐ (reviewed_sha 4bc9432 của lease-publish-windows-do-review-r1-codex: mirror thiếu nhánh ops/do-lease-publish-windows-150) ⇒ vế "0 KDĐ, rc=0" ở a6de9d1 KHÔNG ĐO ĐƯỢC tại đây.
- 10:3xZ Q13 khớp byte; A1, A3 tái lập trên 163fd5d; ruff 9 (7 F401 + 2 F541) cùng tập; điểm nóng 122+4/26/9 và 128/32/10; AST 11/0/10 — KHỚP.
- 10:44Z suite ở 7e5958e (origin/master lúc dựng sandbox, sau #703 đổi ci.yml): 3.12.3 198/198 rc=0 (10:36:59Z–10:44:09Z) — nền tiếp nối lành.
- 10:45Z bản vá thử `refs/remotes/origin/master` tường minh: S9b/S10b ⇒ KHÔNG CẤP (v) rc=1; đối chứng V0 CẤP, V1 KHÔNG CẤP.
- 10:4xZ PROTOCOL :365–368 (fence mà r10 nói mình mượn) đòi ghi ENDPOINT; chuỗi r10 không ghi/kiểm endpoint. PROTOCOL :276 nêu đích danh `.github/coordination/change-impact.v1.json` — tên không khớp bộ lọc `polic|closure|dispatcher` của đoạn miễn trừ (đo: 0); tệp vắng ở 89fc4fa/20ec8d5/163fd5d/a6de9d1/7e5958e.
- 10:4xZ r8 của đặc tả #677 (`f860ab7`, 29-09 17:09:42Z) vào master qua #699 (`b7e32e0`) — là tệp ops/specs/ duy nhất trong 118 tệp 163fd5d..a6de9d1 mà r10 đếm; r10 vẫn viết "bản đóng băng là r7".
- 10:5xZ HINT.patch cuối (4 nhóm, 11 hunk) — dry-run, áp thật, áp riêng từng nhóm đều sạch (mục DRY-RUN). Một câu nháp của HINT ("`fetch` tự kéo theo" tag) chưa đo được — lệnh thử bị hệ thống quyền từ chối, tôi không vòng qua — nên đã đổi thành điều ĐÃ đo ("`git clone` lấy theo").

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 9 (Claude Opus 5.5 max, subagent, trên `2469f3e`): 0 P1 / 2 P2 / 2 P3, bốn lớp, năm finding. Tự kiểm trên r10 (nhãn finding
theo PROTOCOL :636: ĐÃ VÁ THẬT · VÁ HỜ · VÁ SINH LỖI MỚI · CHƯA VÁ):

| lớp (lượt 9) | finding lượt 9 | trạng thái finding trên r10 | trạng thái LỚP lượt 10 | bằng chứng tự đo |
|---|---|---|---|---|
| `thu-tu-677-bo-ngo-o-dieu-kien-cap` (P2) | F9-1 tập tên không làm `origin/master` tươi | **ĐÃ VÁ THẬT** | **VÁ SINH LỖI MỚI** (P2) | S1 (máy chủ land đổi write set) ⇒ (v) rc=1 KHÔNG CẤP; S1n (quên `fetch`) ⇒ lệch (iii) 2 lần ⇒ KHÔNG_XÁC_ĐỊNH (Hướng 1) |
| | F9-2 lease g2 trên nhánh sẵn tên | **ĐÃ VÁ THẬT** | | S2 ⇒ (iv) `NGƯỜI_GIỮ 1: khac-g2-claude` rc=11; S2n ⇒ KHÔNG_XÁC_ĐỊNH; S4/S5 (đổi sau `fetch`/sau `ls-remote`) ⇒ lệch rồi KHÔNG CẤP |
| | (mới) F10-1 chuỗi đo `origin` bất kể là gì; F10-2 "0 dòng" là bằng chứng âm; F10-3 tên `origin/master` bị che | — | | S7a/S7b, S8a/S8b CẤP NHẦM; S9b/S10b CẤP NHẦM (Hướng 1) |
| `tuong-tac-677-kiem-ke-t70-chua-neu` (P2) | F9-3 nghĩa vụ "gọi" ≠ vị từ `co_names` cấp đỉnh | **ĐÃ VÁ THẬT** | **VÁ SINH LỖI MỚI** (P2) | 21 biến thể R1–R10 tái lập đúng từng ô của A2 ở 3.11/3.12/3.13 (Hướng 3) |
| | (mới) F10-4 "(iii) do `t193` canh" không phủ đường gọi lạ; F10-5 G − D đo ở 3.11 | — | | N1–N4, N6–N8: `t70` 1/1 + `t193` 1/1 + D/G−D/chỉ-lồng y nền, `main()` nt ĐỎ; N5: `t193` 3.11 ngược 3.12 |
| `hop-dong-dong-bang-thieu-neo` (P3) | F9-4 `_thieu` chỉ là điều kiện CẦN | **ĐÃ VÁ THẬT** | **CÒN MỞ** (P3) | mục (a) nay đòi `_thieu` + `kiem()` + CLI; 5 số `_thieu` và 3 mẫu `kiem()`/CLI tái lập (Hướng 4) |
| | (mới, có từ r7) F10-6 hiệu lực miễn trừ đo bằng bộ lọc không thấy đường dẫn policy canonical | — | | PROTOCOL :276 nêu `.github/coordination/change-impact.v1.json`; khớp bộ lọc tên: 0 (Hướng 7) |
| `dieu-kien-dung-12-doc-mot-chuyen-tiep` (P3) | F9-5 đọc §12 theo một chuyển tiếp | **ĐÃ VÁ THẬT** | **ĐÃ VÁ THẬT** | §9 :952–957 và :981–992 đọc hai chuyển tiếp; grep "điểm dừng\|dưới ngưỡng\|<50%" không còn câu đọc một chuyển tiếp (:339 là trích Q12) |

Lớp lượt 7–8 đã đóng — có tái phát không:
- `q10-he-qua-mat-nhan-dien-giai`: KHÔNG tái phát — Q13 trích kèm nhãn và đoạn "Áp vào r10 (việc của phiên soạn r10, không phải lời chủ kho)" (:375); bản chiếu tự ghi là lời khai của phiên điều phối.
- `dong-reviewer-loi-khai-rong-hon-do`, `duong-review-b-chua-do-dau-cuoi`: KHÔNG tái phát — `claude -p` (:40, :167, :339, :343, :1043–1044), `phương án B`, `session_run_id`, `same_provider_approved` chỉ ở lịch sử, trích Q12, phép đo validator, §9/§10 "BỎ ở r9".
- `so-do-nen-khong-khop` (lượt 7, 8; ĐÃ VÁ THẬT ở lượt 9): **TÁI PHÁT** ở lượt 10 (F10-7). Nối slug vì cùng đơn vị nghĩa "lời khai về nền không khớp phép đo trên nền"; người điều phối có thể bác việc nối — hạng và hunk không đổi.

Tín hiệu hội tụ §12 (:1043–1049; §8.3 :755–758 "lớp chỉ được ghi ĐÃ VÁ THẬT khi mọi biểu hiện thuộc phạm vi … đã đóng, không
còn biểu hiện cùng cơ chế do bản vá sinh ra và không còn phần phải đo để đóng lớp"). U (lớp mở cuối lượt 9) = 4.
- đọc chặt: F = {`dieu-kien-dung-12-doc-mot-chuyen-tiep`} ⇒ **1/4 = 25%**. `thu-tu-677-…` và `tuong-tac-677-…` có biểu hiện cùng
  cơ chế do chính bản vá r10 sinh ra (chuỗi lệnh mới; nghĩa vụ (iii) và phép G − D mới); `hop-dong-dong-bang-thieu-neo` còn
  "phần phải đo để đóng lớp" (hiệu lực miễn trừ, F10-6).
- nếu người điều phối tách F10-6 thành lớp riêng ⇒ `hop-dong-dong-bang-thieu-neo` ĐÃ VÁ THẬT ⇒ **2/4 = 50%** (không < 50%).
- Chuỗi tỷ lệ: 6→7 `N/A`, 7→8 0/5, 8→9 2/7, 9→10 1/4 (hoặc 2/4). Đọc chặt thì 9→10 là chuyển tiếp thứ BA liên tiếp < 50%.
  Q13 đã chọn "Áp HINT, lặp không trần" nên đây chỉ là số báo cáo, không phải đề xuất dừng.
- Lớp mới ở lượt 10: 0 (một lớp tái mở: `so-do-nen-khong-khop`).

## BẢNG LỚP

| slug lớp | hạng | biểu hiện | phương án | phép kiểm / giới hạn |
|---|---|---|---|---|
| `thu-tu-677-bo-ngo-o-dieu-kien-cap` | **P2** (VÁ SINH LỖI MỚI) | F10-1 (:53–81, :41): chuỗi đo "máy chủ" = bất cứ gì `origin` trỏ tới, không ghi/kiểm endpoint (fence PROTOCOL :365–368 mà r10 nói mình mượn đòi ghi endpoint) ⇒ clone của một mirror CẤP NHẦM (S7a: máy chủ thật có g2 CÒN_HẠN; S7b: máy chủ thật land đổi write set). F10-2 (:66, :71, :74): tiêu chí (iii)/(vii) "`comm -23` 0 dòng" là bằng chứng ÂM — `comm` vắng (rc=127) hay `awk` vắng (rc=127, `mc` rỗng) đều cho 0 dòng ⇒ cộng máy chủ đổi ngay sau `fetch` thì CẤP NHẦM (S8a, S8b); r10 chỉ vá đúng đường `ls-remote` của cùng cơ chế. F10-3 (P3, :59, :69, :70): tên `origin/master` bị tag/nhánh cục bộ cùng tên che (S9b, S10b CẤP NHẦM khi HEAD tách rời; có nhánh `master` thì `CHẶN [12]` tình cờ) | HINT nhóm 1 (3 hunk): bước (0) `git remote get-url origin` phải là URL mạng của kho canonical; mọi bước rc=0 (riêng `grep -v` rc=1); phép đếm DƯƠNG `comm -12 mc cb \| wc -l` = `wc -l < mc` = `wc -l < may_chu.raw`; `refs/remotes/origin/master` tường minh; stderr có `ambiguous` ⇒ KHÔNG_XÁC_ĐỊNH; §10 ghi phép đo | Kiểm: cùng bộ thử, tiêu chí đề xuất chặn S7a/S7b/S8a/S8b, bản vá tên chặn S9b/S10b, đối chứng vẫn CẤP (Hướng 1). Giới hạn: bộ thử so endpoint bằng đường dẫn máy chủ tại chỗ, không đo dạng URL proxy git thật; đo rồi cấp vẫn KHÔNG nguyên tử (thu hẹp, không đóng) |
| `tuong-tac-677-kiem-ke-t70-chua-neu` | **P2** (VÁ SINH LỖI MỚI) | F10-4 (§4 :404–411, :421–426; A3 :556–557; A8 :606): "Vế (iii) do chính `t193` canh trong suite" — `t193` chỉ chạy ca thuộc ứng viên `_ca_ung_vien_gian_tiep(CA)` (đi theo `co_names` cấp đỉnh + hàm cấp module có `__code__`). Bảy đường GỌI THẬT helper (`globals()[…]`, `functools.partial`, bí danh cấp module, lambda trong hàm bọc, decorator đóng gói, tham số mặc định, phương thức lớp) cho `t70` 1/1, `t193` 1/1, D 13, G − D `{t202}`, chỉ lồng `{t70}` — y nền, ở 3.11/3.12/3.13 — mà `main()` dưới seam `nt` ĐỎ "NGOÀI SỔ"; CI PR chỉ ubuntu ⇒ lộ ở lượt master Windows. Đường thứ tám: ca gọi helper ở guard nền không phải "ngay câu lệnh đầu" của `_chay_buoc_dang` (:2748–2757: hai `import`, hai `if guard_hong` đứng trước). F10-5 (A8 :613): G − D "cùng phép quét" dưới 3.11 — hàm bọc gọi helper trong list comprehension: G thấy ca ở 3.12/3.13, không ở 3.11 ⇒ `t193` 3.11 ngược 3.12 (N5) | HINT nhóm 2 (5 hunk): thu hẹp lời khai về `t193`; thêm **phép quét động** ở A8 (mọi ca `@ca` dưới seam nt của `t193`: N == `SO_BO_QUA` đúng cặp và N − D = ∅); G − D đo ở cả 3.11 lẫn 3.12; sửa "ngay câu lệnh đầu"; §10 ghi phép đo | Kiểm: trên nền N = đúng 12 ca sổ, N − D = ∅ (3.12.3, 382,5 s); trên N1–N8 N − D = `{t204}` ở 3.11 và 3.12; ca làm đúng (R11 cả ba) N − D = ∅, ca tự bắt (R12) N = ∅. Giới hạn: seam chỉ MÔ PHỎNG nền nt; Windows thật KHÔNG ĐO ĐƯỢC |
| `hop-dong-dong-bang-thieu-neo` | **P3** (CÒN MỞ) | F10-6 (đoạn miễn trừ :98–105): "Chưa thấy policy canonical" đo bằng lọc tên chứa `polic`/`closure`/`dispatcher` + dòng thêm nhắc ba cụm — PROTOCOL :276 đặt policy ở `.github/coordination/change-impact.v1.json` (schema `…/schemas/change-impact.v1.schema.json`), tên không khớp bộ lọc (đo: 0). Kết luận vẫn đúng (vắng ở 5 mốc) nhưng phép đo không thể thấy đúng thứ nó tìm; đây là điều kiện hết hiệu lực của chính miễn trừ neo closure | HINT nhóm 4 (1 hunk): đo trực tiếp hai đường dẫn bằng `git cat-file -e <rev>:<đường dẫn>`, lúc cấp và lúc land | Kiểm: `cat-file -e` rc≠0 ở `89fc4fa`, `20ec8d5`, `163fd5d`, `a6de9d1`, `7e5958e` (Hướng 7). Giới hạn: không đo nhánh mặc định live |
| `so-do-nen-khong-khop` | **P3** (TÁI PHÁT) | F10-7 (A2 :490, §10 :1178–1179): "Đặc tả #677 đóng băng ở …-r7.md", "bản đóng băng là r7" — bản PR #689 land theo là r8 (`f860ab7`, 29-09 17:09:42Z, Q18–Q20), có trên master từ #699 (`b7e32e0`), chính là tệp `ops/specs/` duy nhất trong 118 tệp `163fd5d..a6de9d1` mà r10 tự đếm | HINT nhóm 3 (2 hunk) | Kiểm: `git log --diff-filter=A` + `cat-file -e` ở `163fd5d` (vắng) / `b7e32e0`, `a6de9d1` (có). Giới hạn: không đổi hành vi thi hành |

## BẢNG SĂN

Mười bốn hướng: phủ 7 hướng gợi ý của PROMPT (dời sang r9→r10: 1→6, 2→4/5, 3→4/9, 4→5, 5→2, 6→1/10, 7→6/12), năm trọng
tâm lượt 10, và các hướng tự thêm (7, 8, 9, 10, 11, 12, 13, 14).

```
HƯỚNG 1: Chuỗi lệnh cấp (1)/(4)/(5) chạy THẬT trên kho bare tại chỗ          [trọng tâm (1); gợi ý 6]
  giả thuyết : chuỗi fail-close ở mọi nhánh; không đường nào cho cấp nhầm.
  lệnh       : do10.Nq9r/chuoi/chuoi_lib.sh + kich_ban.sh (10:21:57Z–10:22:28Z): mỗi kịch bản một máy chủ bare + clone refspec
               rộng; chuỗi chạy ĐÚNG từng dòng :58–71 (PATH của chuỗi chỉ git awk sort grep comm python→3.11), ghi rc+output
               từng bước; chấm theo ĐÚNG chữ :74–75 (fetch/ls-remote hỏng ⇒ KXĐ; (iii)/(vii) khác 0 dòng ⇒ đo lại một lần; vẫn
               lệch ⇒ KXĐ); song song chấm theo tiêu chí DƯƠNG đề xuất (endpoint + rc mọi bước + phép đếm).
               ai-dang-giu = ops/lease_publish.py của 163fd5d (sha256 dd17b94c…4f83). kich_ban_va.sh (10:45:43Z) cho bản vá tên.
  output     : S0 đối chứng: CẤP | CẤP.  S1 land đổi write set: KHÔNG CẤP (v) rc=1.  S2 g2 CÒN_HẠN nhánh sẵn tên: KHÔNG CẤP
               (iv) NGƯỜI_GIỮ 1 rc=11.  S3 origin không tồn tại: KXĐ fetch rc=128 (ai-dang-giu CHAN [12]).  S4 đổi ngay sau fetch:
               lần 1 LỆCH(iii) 1 dòng → lần 2 NGƯỜI_GIỮ 1 ⇒ KHÔNG CẤP.  S5 đổi sau ls-remote: lần 1 LỆCH(vii) → lần 2 KHÔNG CẤP.
               S1n/S2n (bỏ fetch): LỆCH(iii) cả hai lần ⇒ KXĐ.                                ← tái lập đúng r10 §10
               S7a origin = mirror chưa cập nhật, máy chủ thật có g2 CÒN_HẠN: theo chữ r10 **CẤP** (mọi bước rc=0, comm 0, (iv)
                   NGƯỜI_GIỮ 0 ×2, (v) 0, (vi) 0) | dương: KXĐ (endpoint). Sự thật: `git show claude/lease-khac:…g2` có trên srv,
                   KHÔNG có trên mirror.
               S7b origin = mirror, máy chủ thật land đổi write set: theo chữ **CẤP** | dương: KXĐ.
               S8a `comm` vắng + đổi ngay sau fetch: comm rc=127 "0 dòng" ở (iii) và (vii) ⇒ theo chữ **CẤP** | dương: KXĐ (rc=127).
                   Sự thật: srv có g2, ref theo dõi của cap không có.
               S8b `awk` vắng + đổi ngay sau fetch: awk rc=127, mc 0 dòng, comm rc=0 0 dòng ⇒ theo chữ **CẤP** | dương: KXĐ.
               S8c `sort` cắt ở 4096 byte (ulimit -f 4) + 300 nhánh: mc 75/303 dòng, dòng cuối cắt giữa OID ⇒ LỆCH tình cờ ⇒ KXĐ.
               S9/S10 tag hoặc nhánh cục bộ `origin/master` → nền cũ, có nhánh master: (iv) CHAN [12] TỤT_SAU (chặn tình cờ);
                   stderr 3 dòng "ambiguous".
               S9b/S10b như trên nhưng HEAD tách rời, không nhánh cục bộ: theo chữ **CẤP** ((v) so với ref bị che, rc=0).
               Bản vá `refs/remotes/origin/master`: V9b/V10b ⇒ KHÔNG CẤP (v) rc=1; V0 CẤP; V1 KHÔNG CẤP.   0 .pyc.
  kết luận   : LỖI P2 (F10-1, F10-2) + biểu hiện P3 (F10-3), lớp `thu-tu-677-bo-ngo-o-dieu-kien-cap`. "Thu hẹp, không đóng"
               (:81) đúng cho cửa sổ thời gian; nhưng bốn ca trên không phải cửa sổ thời gian — chuỗi chạy trọn, đúng chữ, CẤP.
```

```
HƯỚNG 2: Dời nền 163fd5d — kiểm SỐ HẠNG                                         [trọng tâm (2); gợi ý 5]
  lệnh       : hai clone `git clone --no-local --no-hardlinks kho.git` dựng trong MỘT lệnh, `checkout --detach 163fd5d`,
               `core.abbrev 7`; `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scratch> python ops/lease_publish_test.py`, PATH có
               python/python3 → đúng bản; `ast` so định nghĩa cấp module; `git diff --numstat/--name-only`; ruff trên `git
               archive` tối thiểu; `git archive <rev> ops/leases` + yaml.safe_load.
  output     : 3.11.15 198/198 rc=0 10:14:10Z–10:20:25Z · 3.12.3 198/198 rc=0 10:20:25Z–10:28:06Z; vào 198/ra QUA 198; bỏ qua 0;
               0 .pyc; porcelain 0. `grep -c '^@ca'` 198; 11506 / 2206 dòng; `20ec8d5..163fd5d`: 7 tệp, `482 63`, lease_publish.py
               giống hệt. AST: thêm 11 (đúng danh sách), xoá 0, đổi thân 10 (đúng danh sách); t70, t178, _ca_doc_than_buoc,
               _chay_buoc_dang, _chay_buoc_dang_that, _buoc_workflow giống thân. Tọa độ (ast): t70 @3039 def 3040–3054; vị từ
               3035–3036; _ca_ung_vien_gian_tiep 3057–3073; SO_BO_QUA 569–575; t193 @10613 10614–10744; t194 10758–10829;
               t195 10996; t199 11098; t202 –11388; t203 11392–11441; helper 10860; t178 :7924–7925 đúng câu trích.
               ruff 0.15.8 F: 20ec8d5 = 163fd5d = 7e5958e = 9 (7 F401, 2 F541), cùng tập bỏ số dòng, lease_publish.py 0.
               Lease: 163fd5d 122 .yaml + 4 .nhap, 0 lỗi parse, 26 tệp, 9 packet (+687); a6de9d1 128, 32 tệp, 10 packet (+677).
               118 tệp 163fd5d..a6de9d1 = 81 land + 7 leases + 29 reviews + 1 specs; .github 0; ngay dưới ops/ 0.
               t125 191,4 s ở lượt 3.11 của tôi (r10 khai 199 s — dao động thời gian chạy).
  kết luận   : KHÔNG PHẢI LỖI ở mọi số đo lại được. Ngoại lệ là một lời khai lịch sử không đo lại: tệp `ops/specs/` duy nhất
               trong 118 tệp là r8 của đặc tả #677 ⇒ F10-7 (Hướng 11).
```

```
HƯỚNG 3: Nghĩa vụ t70 + t193/SO_BO_QUA/literal — đột biến thật 3.11/3.12/3.13      [trọng tâm (3)]
  giả thuyết : đúng chữ thì hai chốt xanh, sai thì đỏ; còn đường (hàm bọc, decorator, getattr) lọt.
  lệnh       : dotbien/dotbien.py (10:25:11Z–10:28:08Z): 39 biến thể, mỗi biến thể một `git archive 163fd5d ops/lease_publish.py
               ops/lease_publish_test.py ops/chay_lease_publish_test.sh .github`; ca mới `t204_moi` chèn trước `def main(`;
               `--chi-ca=t70_` và `--chi-ca=t193_` dưới python3.11/3.12/3.13; probe.py nạp module: D (vị từ t70), G − D, quét lồng
               (đệ quy co_consts), và main(chon=[ca], nen='nt') với `_ly_do_bo_qua_workflow` ép nt (đúng seam t193), sổ mặc định.
               quet_nt.py: chạy MỌI ca dưới seam nt, N = tập ném BoQuaNen.
  output     : (t70/t193; 3.11 | 3.12 | 3.13)  R0 gốc 1/1·1/1 cả ba; D 13, G−D {t202}, chỉ lồng {t70}, sổ 12 cả ba.
               R1 nhắc cấp đỉnh: không thêm 0/1, thêm 1/1 · R2 `if False:` idem · R3 gán biến rồi comprehension idem · R9 t178 nhắc
               cấp đỉnh idem · R4 hàm lồng / R5 lambda / R6 genexp / R8 chuỗi-docstring-chú thích: không thêm 1/1, thêm 0/1 ·
               R7 list comp (và R10 t178 comp): không thêm 1/1|0/1|0/1, thêm 0/1|1/1|1/1 · R1–R10 t193 1/1 ·
               R11 gọi thật cấp đỉnh: không thêm t70 0/1 t193 0/1; chỉ mong 1/1·0/1; mong+sổ ·0/1; mong+literal ·0/1; cả ba 1/1·1/1 ·
               R12 tự bắt: mong ⇒ 1/1·1/1; cả ba ⇒ t193 0/1 · R13 hàm bọc: không thêm 1/1·0/1; sổ+literal 1/1·1/1. ← đủ bảng r10
               (ba bản cùng kết quả ở mọi ô t193; R4 chỉ lồng {t70,t204}; R7 chỉ lồng {t70,t204} ở 3.11, {t70} ở 3.12/3.13;
               R13 G−D {t202,t204})
               N1 `globals()["_chay_buoc_dang_that"](…)` · N2 `functools.partial` cấp module · N3 bí danh `_H204 = helper` · N4 hàm bọc
               gọi helper trong lambda · N6 decorator đóng gói `@_voi204(helper)` · N7 tham số mặc định `h=helper` · N8 staticmethod
               lớp: KHÔNG thêm gì ⇒ t70 1/1, t193 1/1 ở cả ba bản; D 13, G−D {t202}, chỉ lồng {t70} (y nền); main() nt: rc=1 "NGOÀI SỔ".
               N5 hàm bọc gọi helper trong list comp: không thêm ⇒ t193 1/1 | 0/1 | 0/1; sổ+literal ⇒ 0/1 | 1/1 | 1/1;
               G−D {t202} ở 3.11, {t202,t204} ở 3.12/3.13.
               quét động: nền (3.12.3, 382,5 s, 198 ca) N = 12 ca sổ, N == SO_BO_QUA đúng cặp, N−D ∅ (18 ca ném lỗi khác dưới nt —
               không tính); N1–N8 N−D {t204} ở 3.11 và 3.12; R11 cả ba N−D ∅; R12 N ∅.   0 .pyc.
  kết luận   : r10 tái lập ĐÚNG. LỖI P2 F10-4, F10-5 (lớp `tuong-tac-677-kiem-ke-t70-chua-neu`): mọi đường N vi phạm (i) nhưng
               KHÔNG phép đo nào r10 nêu bắt được, và lời khai "(iii) do chính t193 canh" rộng hơn tầm chạy của t193. Đặc tả #687 r3
               M2 tự đòi sổ "đo bằng chạy thật, không suy từ tên" — phép quét động là đúng phép ấy.
```

```
HƯỚNG 4: Hợp đồng biên nhận ba vế khớp kiem()/CLI                                  [trọng tâm (4); gợi ý 2, 3]
  lệnh       : bn/bn10.py (10:31:09Z) nạp ops/bien_nhan_v2.py của clone đầy đủ 163fd5d (sha256 38cda51c…defc, PROVIDER_NGUON_HONG
               None), biên nhận mẫu wp678 từ tiền lệ phan-bien-quy-trinh-review-2; mỗi mẫu một kho git tạm; CLI python3.12.
               CLI trên kho thật 163fd5d, a6de9d1, 7e5958e. Cây `git archive 20ec8d5 ops` (thiếu .claude, AGENTS.md).
               Đọc ngoài $R: ~/.claude/agents/review-opus-max.md (chỉ băm, cỡ, hai khoá frontmatter; 10:34:35Z).
  output     : _thieu: tiền lệ 0 · mẫu 0 · same_provider 1 ("tự khai chạy trong phiên điều phối") · human_audited 2 · bỏ che_do + 'x'
               + same_provider 0.  kiem()/CLI: neo blob đúng ⇒ 0 vi phạm, 0 KDĐ, CLI rc=0 · URL PR ⇒ 1 vi phạm (canonical_ancestry
               không phải URL blob), rc=1 · reviewed_sha vắng ⇒ 0 vi phạm, ĐẠT v2 1, 1 KDĐ mang tên tệp, rc=2.  Cây thiếu nguồn
               provider ⇒ PROVIDER_NGUON_HONG "FileNotFoundError…", CLI rc=2 với mẫu đúng.  Kho thật: 163fd5d "163 ĐẠT v2 · 11/11
               · 42 NỢ · 0 vi phạm · 0 KDĐ · tổng 216" rc=0; a6de9d1 / 7e5958e "174 · 11/11 · 42 · 0 · **1** KDĐ · 227" rc=2.
               ci.yml :590 bien_nhan_v2_test; c1 :345–350 `_kiem` vứt chua_do; bien_nhan_v2 :994–1000 đếm ĐẠT bỏ qua chua_do;
               :1043–1065 rc=2 khi có KDĐ. Định nghĩa: e225b81c…b792c, 1175 byte, model claude-opus-5-5, effort max.
  kết luận   : KHÔNG PHẢI LỖI — mục (a)–(c) khớp mã và mọi số r10 khai. Riêng "0 KDĐ, rc=0 ở a6de9d1": KHÔNG ĐO ĐƯỢC tại đây —
               KDĐ duy nhất là reviewed_sha 4bc9432 của lease-publish-windows-do-review-r1-codex, mà chính biên nhận ấy ghi chỉ
               nhánh ops/do-lease-publish-windows-150 giữ; mirror thiếu nhánh ấy. Mục (a) đọc theo mục mang tên tệp, nên KDĐ của
               tệp khác không làm hỏng (a) — r10 viết đúng điều đó.
```

```
HƯỚNG 5: Q13 trích đúng byte; Q8/Q10/Q11/Q12 còn nguyên                          [trọng tâm (5); gợi ý 4]
  lệnh       : python: body.encode('utf-8') ⇒ sha256, byte, số dòng, thực thể HTML; so từng dòng trích "  > " của §3 với thân.
  output     : 5928886724: sha256 5f1ff74e…0878, 1662 byte, 16 dòng, 0 thực thể, 0 CR, tạo 09:44:15Z, OWNER, app claude; dòng 5,
               7–9, 11, 13 (và dòng trống giữa) có nguyên văn trong thân; 0 dòng trích lạ. Dòng 3 (không trích) khớp diễn giải r10.
               §3 r9→r10: Q1–Q4, Q7, Q8, Q9, Q11 giống byte; Q10 chỉ đổi phần ghi chú áp dụng (cổng biên nhận (a)); Q12 chỉ khác
               khoảng trắng ranh giới. Q10 69cc35b1…/2151 (6 dòng trích), Q11 392069d1…/1741 (13), Q12 4c9d5e19…/1648 (10), Q8
               3a8c40a6…/1187: 0 dòng trích lạ, 0 thực thể.
  kết luận   : KHÔNG PHẢI LỖI. Đoạn "khớp từng byte văn bản điều phối giao" (:363–364): KHÔNG ĐO ĐƯỢC (văn bản ấy không có trong $R).
```

```
HƯỚNG 6: Phạm vi r9→r10 ở mức byte                                                [gợi ý 1, 7]
  lệnh       : so_muc.py tách hàng bảng, mục "## ", A1–A10; word-diff A1, A9, hàng reviewer; áp HINT lượt 9 lên bản sao r9.
  output     : GIỐNG: §1, §2, §5, Phụ lục A; hàng objective, write set §4 (hai đường dẫn), closure (5 hàng), A4–A7, A10.
               A1: chỉ nền/giờ đo/cây archive; A9: "`20ec8d5` và `163fd5d`". Hàng reviewer: chỉ thêm "`20ec8d5`, và giữa … và
               `163fd5d`". HINT lượt 9 lên r9: rc=0, 9/9, một offset 22, 997→1034, sha256 4a1d9591…c964 = ky_vong lượt 9 (đúng §9).
               r9+HINT9 → r10: sửa thêm chỉ ở đầu tệp, §3, §4, §6, §7, §8, §9, §10. grep codex: chỉ lịch sử/trích Q10.
  kết luận   : KHÔNG PHẢI LỖI — r10 đổi đúng những gì bảng đầu tệp khai; dời nền đến từ Q8 điều kiện (4), không từ Q13.
```

```
HƯỚNG 7 (tự thêm): Miễn trừ #682 còn áp không — đo đúng đối tượng
  giả thuyết : phép lọc `polic|closure|dispatcher` thấy được policy canonical nếu nó xuất hiện.
  lệnh       : grep PROTOCOL; `git cat-file -e <rev>:.github/coordination/change-impact.v1.json` (và schema); lọc lại hai khoảng mới.
  output     : PROTOCOL :276 "Change-impact policy chuẩn ở `.github/coordination/change-impact.v1.json`, schema ở
               `.github/coordination/schemas/change-impact.v1.schema.json`". `echo <đường dẫn> | grep -ci 'polic\|closure\|dispatcher'`
               ⇒ 0. cat-file -e: vắng cả hai ở 89fc4fa, 20ec8d5, 163fd5d, a6de9d1, 7e5958e (schemas/ chỉ có review_verdict.v1).
               Lọc r10: 20ec8d5..163fd5d tên 0 dòng 0; 163fd5d..a6de9d1 0/0; a6de9d1..7e5958e 0/0 (khớp r10).
               ops/lease_publish.py :1096 `PATH_POLICY_CLOSURE` trỏ đúng đường dẫn ấy.
  kết luận   : LỖI P3 F10-6 (lớp `hop-dong-dong-bang-thieu-neo`): kết luận đúng, phép đo mù đúng đối tượng; r10 tự ghi
               "không chứng minh vắng mặt" — nhưng phép chứng minh trực tiếp có sẵn và rẻ.
```

```
HƯỚNG 8 (tự thêm): Sau lúc r10 đo — #703 đổi ci.yml (7e5958e)
  lệnh       : git diff 163fd5d 7e5958e -- .github; yaml tên job; suite 3.12 ở 7e5958e (clone n311).
  output     : `.github/workflows/ci.yml` +90/−4 (đường nhanh hồ sơ, packet #674); tên job gate/gate-ops/gate-registry/
               gate-packet-loop giữ nguyên, ma trận os từ chuan-bi; bước `bien-nhan v2 selftest` không có `if:` theo che_do (chạy cả
               đường nhanh); `lease-publish selftest` chỉ bỏ ở đường nhanh (PR thi hành đổi mã ⇒ đầy đủ). Suite 7e5958e: 198/198
               rc=0 (10:36:59Z–10:44:09Z). Hai tệp write set: `git diff --stat 163fd5d 7e5958e` rỗng (khớp điều phối).
  kết luận   : KHÔNG PHẢI LỖI — closure và nền tiếp nối không gãy.
```

```
HƯỚNG 9 (tự thêm): workflow `thu-hoi` của required_checks có chạy trên PR thi hành không
  lệnh       : git show <rev>:.github/workflows/ops-thu-hoi-admission.yml | sed -n '1,40p'
  output     : name: thu-hoi; on: pull_request_target types [opened, reopened, synchronize, ready_for_review, edited], branches
               [master]; không `paths:` (163fd5d và 7e5958e).
  kết luận   : KHÔNG PHẢI LỖI — check bắt buộc không vắng mặt vì bộ lọc đường dẫn.
```

```
HƯỚNG 10 (tự thêm): Đặc tả #687 có ràng buộc gì với packet khác sửa SO_BO_QUA
  lệnh       : git show 163fd5d:ops/specs/lease-publish-windows-do-r{1,2,3}.md | grep sổ/registry/ứng viên
  output     : r3 M2 "Mỗi ca ném BoQuaNen … phải nằm trong sổ … Ca nào không ném thì KHÔNG được thêm … Phải đo bằng chạy thật, không
               suy từ tên"; r1 đột biến "nới sổ thêm tên ca tấn công — phải làm t193 ĐỎ". Không cấm packet khác thêm tên đúng.
  kết luận   : KHÔNG PHẢI LỖI của r10 (nghĩa vụ (iii) hợp với #687); củng cố phương án HINT nhóm 2 (đo sổ bằng chạy thật mọi ca).
```

```
HƯỚNG 11 (tự thêm): Lời khai về đặc tả #677 sau dời nền
  lệnh       : git log --diff-filter=A --format='%h %cI %s' 7e5958e -- ops/specs/dot-bien-l-bien-cong-khai-r8.md; cat-file -e ở
               163fd5d / b7e32e0 / a6de9d1; grep '678' trong r8 của #677.
  output     : f860ab7 2026-09-29T17:09:42Z "spec(#677): r8 — checkpoint sau lượt codex 2 trên PR #689: Q18 …"; vắng ở 163fd5d, có ở
               b7e32e0 (#699) và a6de9d1. r8 #677 không đặt nghĩa vụ mới lên wp678 (Q10 "#677 rồi #678", "A2 sau #678" — r10 đã phủ).
  kết luận   : LỖI P3 F10-7 (lớp `so-do-nen-khong-khop`, TÁI PHÁT).
```

```
HƯỚNG 12 (tự thêm): Điểm mù của `ai-dang-giu` mà điều kiện (1) dựa hẳn vào
  lệnh       : đọc `_lease_cham_duong` (khớp ĐÚNG chuỗi trong write_set dạng list); đếm dạng write_set ở 163fd5d/a6de9d1/7e5958e.
  output     : list 82/88/88, None 40/40/40 (lease review chỉ đọc, hết hạn 08-2026; nhắc lease_publish chỉ trong ghi chú); 0
               write_set dạng chuỗi chạm lease_publish; 4 mục thư mục (ops/reviews/…), 0 glob chạm ops/lease_publish*.py.
  kết luận   : KHÔNG PHẢI LỖI trên kho thật (quan sát: điểm mù có thật trong mã nhưng không lease nào có hình dạng ấy).
```

```
HƯỚNG 13 (tự thêm): Trần vòng review (r10 §10 để KHÔNG ĐO ĐƯỢC)
  lệnh       : đọc docs/adr/0048-tran-vong-review-len-muoi.md; ls-tree ops/reviews | grep wp678 ở 163fd5d và 7e5958e.
  output     : ADR-0048 Accepted 2026-09-12: trần 10 vòng review HỢP LỆ cho một PR packet, vòng chỉ tính khi có biên nhận hợp lệ,
               vượt phải khai `nang_tran` (không cổng nào cưỡng chế). Biên nhận wp678 trên master: 6 (lượt 1–6); lượt 7–9 chưa có.
  kết luận   : QUAN SÁT, không chấm (ngoài phạm vi chấm của đặc tả): nếu lượt 7–10 được ghi biên nhận thì lượt kế tiếp là vòng 11.
```

```
HƯỚNG 14 (tự thêm): A1 và A3 "ĐỎ khi" trên nền mới
  lệnh       : nạp ops/lease_publish.py 163fd5d; mẫu wp55-r4-…yaml bỏ prompt_*; mười dạng viết thành YAML qua _doc_yaml rồi
               kiem(bo_qua_han=True). A3: `_chay_buoc_dang_that(_yaml_that(lid), comments_san=[_dau_bot("True")])` trên clone đầy đủ.
  output     : A1: true/yes/on bool, 1.5/1.50 float, 0x1F/017/1_000/5 int, 2026-09-29 date ⇒ qua; 'yes' str ⇒ qua.
               A3: yes ⇒ rc=0, 0 POST, 2 lời gọi, "đã đăng trước đó"; 'fresh-id' ⇒ rc=0, 1 POST, 4 lời gọi. (bản sao `git archive`
               tối thiểu thiếu ops/bash_nen.py nên A3 phải chạy trên clone đầy đủ.)
  kết luận   : KHÔNG PHẢI LỖI — khớp r10.
```

## BẢNG ĐO

| khẳng định trong spec | spec khai | đo được | khớp? |
|---|---|---|---|
| sha256 r10 / HEAD | 892c8006…/42292b4 | như khai | có |
| r9 tạo bởi 2469f3e, 1 commit chạm, 997 dòng, sha 45c8d314… | có | như khai | có |
| VERDICT/HINT lượt 9 bb5bf15b…/af52b8b5…, 4 nhóm 9 hunk | có | như khai | có |
| HINT lượt 9 lên r9: rc=0, 9/9, offset 22, 997→1034, = 4a1d9591…c964 | có | như khai | có |
| 163fd5d = merge PR #701, base 20ec8d5; r9 commit 05:31:30Z | có | cha 20ec8d5+9d7a523, 05:42:27Z; 2469f3e 05:31:30Z | có (REST merged_at: KĐĐ) |
| `20ec8d5..163fd5d` lease_publish_test `482 63`, lease_publish.py giống | có | như khai | có |
| 7 tệp `20ec8d5..163fd5d`; 118 = 81+7+29+1, .github 0, ngay dưới ops/ 0 | có | như khai | có |
| PROTOCOL, bien_nhan_v2(+test), ops-publish-lease.yml, ci.yml, chay_lease_publish_test.sh giống 20ec8d5↔163fd5d | có | rc=0 cả 6 | có |
| AST thêm 11 / xoá 0 / đổi 10, sáu định nghĩa giống thân | có | như khai | có |
| suite 198/198 ở 3.11 và 3.12, bỏ qua 0 | có | như khai | có |
| t70 :3040–3054, vị từ :3035–3036, mong 13; t193 :10614–10744; sổ :569–575 12 tên; literal :10649–10650 12; t194/t195…t203/helper | có | như khai | có |
| "Hai helper ném … ngay câu lệnh đầu" | đúng | `_chay_buoc_dang`: guard là câu lệnh thứ 5 | **không** (F10-4, P3 phần) |
| bảng đột biến t70/t193 của A2 (3.11/3.12/3.13) | có | đủ từng ô | có |
| "Vế (iii) do chính t193 canh trong suite" | đủ | 7 đường gọi thật: t193 1/1, main nt ĐỎ | **không** (F10-4) |
| G − D "cùng phép quét" (3.11) bắt hàm bọc | có | N5 hàm bọc comprehension: G−D {t202} ở 3.11 | **không** (F10-5) |
| quét nền D 13, R 14, chỉ lồng {t70}, G−D {t202}, sổ 12, D−sổ {t199} | có | D 13, chỉ lồng {t70}, G−D {t202}, sổ 12 | có |
| ruff 9 (7 F401 + 2 F541) cùng tập ở 20ec8d5/163fd5d | có | như khai (cả 7e5958e) | có |
| điểm nóng 122+4/26/9 (163fd5d), 128/32/10 (a6de9d1) | có | như khai | có |
| _thieu 0/0/1/2/0; mẫu kiem() 0/1/0+1KDĐ; CLI rc 0/1/2 | có | như khai | có |
| CLI kho thật 163fd5d 163/11/42/0/0/216 rc=0 | có | như khai | có |
| CLI kho thật a6de9d1 174/11/42/0/**0**/227 rc=0 | có | 174/11/42/0/**1**/227 rc=2 (mirror thiếu 4bc9432) | KHÔNG ĐO ĐƯỢC |
| định nghĩa review-opus-max e225b81c…, 1175 byte | có | như khai | có |
| Q13 sha 5f1ff74e…, 1662 byte, 16 dòng, 0 thực thể, dòng 5/7–9/11/13 | có | như khai | có |
| lease g3 #687: 163fd5d blob 372cbfd hạn 10-02T01:12Z; a6de9d1 blob 976915a hạn 10-01T05:55Z; 5955819 05:42:57Z | có | như khai | có |
| A1 mười dạng qua trên 163fd5d; A3 yes 0 POST / fresh-id 1 POST | có | như khai | có |
| chuỗi lệnh "đo máy chủ", fail-close khi không đo được | có | S7a/S7b/S8a/S8b/S9b/S10b CẤP | **không** (F10-1…3) |
| ca lượt 9 (i)(ii) và ca r10 (iii)(iv) bị chuỗi bắt | có | S1, S2, S1n, S2n, S3, S4, S5 | có |
| "Chưa thấy policy canonical" (lọc chuỗi) | có | vắng (đo trực tiếp); bộ lọc không khớp đường dẫn | có kết luận / phép đo mù (F10-6) |
| "Đặc tả #677 đóng băng ở …-r7.md", "bản đóng băng là r7" | có | r8 (f860ab7) là bản land, trên master từ #699 | **không** (F10-7) |
| 462/462 ref, NGƯỜI_GIỮ live 09:18Z/09:45Z, REST PR #701/#689, thân #682 76bee6fb…/3416, #678 c.5925743728 | có | cần mạng / không có readback | KHÔNG ĐO ĐƯỢC |

## CHI TIẾT TỪNG LỚP

### `thu-tu-677-bo-ngo-o-dieu-kien-cap` — P2 (VÁ SINH LỖI MỚI; lượt 7, 8, 9, 10)
- F9-1, F9-2 ĐÃ VÁ THẬT: chuỗi bắt cả hai ca lượt 9 (đủ chuỗi lẫn khi quên `fetch`) và hai ca r10 tự liệt kê.
- F10-1 (:53–81, :41). Chuỗi gọi kết quả là "máy chủ" nhưng đo bất kỳ `origin` nào; handoff không ghi endpoint. Clone của một
  mirror (đúng kiểu hai clone A8 r10 tự dựng từ `adg2`) chạy trọn chuỗi, đúng chữ, ra CẤP trong khi máy chủ thật có lease CÒN_HẠN
  (S7a) hoặc đã land đổi write set (S7b). Fence PROTOCOL :365–368 — thứ r10 §10 nói mình "mượn" — đòi ghi endpoint.
- F10-2 (:66, :71, :74–75). Tiêu chí "`comm -23` 0 dòng" là bằng chứng ÂM. r10 tự đo đúng cơ chế này ở `ls-remote` (ca (iii),
  pipeline fail-open) và chỉ vá riêng bước ấy; cùng cơ chế còn ở `awk`, `sort`, `comm`: thiếu `comm` (rc=127) hay `awk` (rc=127)
  đều cho 0 dòng, và đó là chốt DUY NHẤT của chuỗi chống ca (iv) "máy chủ đổi ngay sau fetch" ⇒ S8a, S8b CẤP NHẦM. Đúng hình
  dạng *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"* và *"phải đòi BẰNG CHỨNG DƯƠNG"* của CLAUDE.md.
- F10-3 (P3; :59, :69, :70). `origin/master` là tên mơ hồ: `refs/tags/origin/master` hoặc `refs/heads/origin/master` đứng trước
  `refs/remotes/origin/master` khi git phân giải; git chỉ cảnh báo `ambiguous` trên stderr. Có nhánh `master` thì `ai-dang-giu`
  chặn tình cờ; HEAD tách rời không nhánh cục bộ thì CẤP NHẦM (S9b, S10b).
- Vì sao P2, không P1: làm đúng r10 TRONG một clone trực tiếp từ GitHub, đủ công cụ, thì chuỗi đúng; các ca CẤP NHẦM cần một
  điều kiện mà r10 không cấm (origin là mirror; thiếu công cụ; ref trùng tên) — rubric "nhãn lời khai rộng hơn phép đo". §5.1
  kích hoạt #2 vẫn bắt drift chạm write set lúc land.
- Phương án (HINT nhóm 1, đo cùng bộ thử): (0) `git remote get-url origin` ghi vào handoff, phải là URL mạng của kho canonical;
  mọi bước rc=0 (riêng `grep -v` rc=1); phép đếm dương; `refs/remotes/origin/master` tường minh; stderr `ambiguous` ⇒ KXĐ.
- Giới hạn: bộ thử kiểm endpoint bằng đường dẫn máy chủ tại chỗ; dạng URL qua proxy git của phiên thật KHÔNG ĐO ĐƯỢC ở đây
  (kho chính `/home/user/tra-luat` có `origin` = `https://github.com/ducthangho/tra-luat`, đọc không in xác thực). Đo rồi cấp
  vẫn không nguyên tử.

### `tuong-tac-677-kiem-ke-t70-chua-neu` — P2 (VÁ SINH LỖI MỚI; lượt 8, 9, 10)
- F9-3 ĐÃ VÁ THẬT: (i) viết theo vị từ thật (tham chiếu cấp đỉnh), đúng ở 3.11/3.12/3.13; 21 biến thể tái lập từng ô.
- F10-4 (§4 :404–411, :425; A3 :556–557; A8 :606). r10 thêm nghĩa vụ (iii) (#687) và khai "Vế (iii) do chính `t193` canh trong
  suite". `t193` chỉ CHẠY ca thuộc `_ca_ung_vien_gian_tiep(CA)`, vốn chỉ đi theo `co_names` cấp đỉnh và hàm cấp module có
  `__code__`. Bảy cách GỌI THẬT helper (getattr qua `globals()`, `functools.partial`, bí danh cấp module, lambda trong hàm bọc,
  decorator đóng gói, tham số mặc định, phương thức lớp) qua `t70`, `t193` và cả ba phép đo A8 (t70 3.11/3.12, quét lồng = {t70},
  G − D = {t202}) ở 3.11/3.12/3.13, trong khi `main()` dưới seam nt — chính seam của `t193` — ĐỎ "NGOÀI SỔ". CI PR chỉ ubuntu nên
  lộ ở lượt master Windows (bài học "PR xanh ≠ master xanh"). Mọi cách ấy đều trái (i), nhưng A8 tuyên bố đo được (i)/(iii) ⇒
  "nghĩa vụ ở §4 được đo là đạt" khi nó bị vi phạm. Kèm câu "ném … ngay câu lệnh đầu" sai với `_chay_buoc_dang` (guard là câu
  lệnh thứ năm, sau hai `import` và hai `if guard_hong`) — vô hại về hành vi, sửa cùng hunk.
- F10-5 (A8 :613). G − D đo "cùng phép quét" dưới 3.11; hàm bọc gọi helper trong list comprehension chỉ vào G ở 3.12/3.13 ⇒
  G − D trên ứng viên vẫn `{t202}` ở 3.11, và `t193` 3.11 ngược 3.12 (N5). CI (3.12) bắt được nên không lọt land; nhưng phép đo
  r10 đặt sai bản Python.
- Vì sao P2: lời khai rộng hơn phép đo, ở tiêu chí chuẩn tắc (A8 "ĐỎ khi … nghĩa vụ ở §4 không được đo là đạt"). Không P1: làm
  đúng (i) thì không đường nào trên xảy ra.
- Phương án (HINT nhóm 2): phép quét ĐỘNG mọi ca `@ca` dưới seam nt (N == sổ đúng cặp, N − D = ∅) — đo: không báo động giả trên
  nền, bắt cả 8 biến thể ở 3.11 và 3.12; thu hẹp lời khai về `t193`; G − D ở cả 3.11 lẫn 3.12. Đặc tả #687 r3 M2 đòi đúng điều
  này ("đo bằng chạy thật, không suy từ tên").

### `hop-dong-dong-bang-thieu-neo` — P3 (CÒN MỞ; lượt 1, 2, 7, 8, 9, 10)
- F9-4 ĐÃ VÁ THẬT (mục (a) nay khớp `kiem()` và CLI; đo).
- F10-6 (đoạn miễn trừ :98–105; có từ r7, mới tìm ra). Hiệu lực của miễn trừ — mỏ neo của closure điền tay — hết khi policy
  canonical xuất hiện; PROTOCOL :276 nêu đích danh đường dẫn của nó, mà bộ lọc chuỗi r7–r10 dùng không khớp được tên ấy. Kết luận
  hiện đúng (đo trực tiếp: vắng). Nối vào lớp này vì cùng đơn vị nghĩa "neo của hợp đồng đóng băng"; nếu người điều phối tách
  thành lớp riêng thì lớp này ĐÃ VÁ THẬT và tỷ lệ 9→10 thành 2/4.

### `so-do-nen-khong-khop` — P3 (TÁI PHÁT; lượt 7, 8, 10)
- F10-7 (A2 :490; §10 :1178–1179). Lời khai "đặc tả #677 đóng băng ở r7" sai từ lúc ghi (r8 của #677 soạn 29-09 17:10Z, trước khi
  PR #689 land 01-10 00:55Z) và nay mâu thuẫn với chính phép đếm 118 tệp của r10 (tệp `ops/specs/` duy nhất là r8 ấy). Không ảnh
  hưởng nghiệm thu (r10 không neo acceptance vào đặc tả #677). Đây là đúng hình dạng *"MỘT BẤT BIẾN CÒN ĐÚNG KHÔNG CHỨNG MINH CÁC
  SỐ HẠNG CÒN ĐÚNG"*: con số 118 được đo, nội dung của nó không được đọc.

## DRY-RUN HINT.patch

`$R/goi/HINT.patch`: 169 dòng, 57900 byte, sha256 `cb7f265ec904e5f1ef229c7f6194031f7f3c9b9fcd2acdbdb78f1e93bffc1c97`.
4 nhóm `# lop:` — `thu-tu-677-bo-ngo-o-dieu-kien-cap` (3 hunk) · `tuong-tac-677-kiem-ke-t70-chua-neu` (5) ·
`so-do-nen-khong-khop` (2) · `hop-dong-dong-bang-thieu-neo` (1) = 11 hunk. Sinh bằng `$R/do10.Nq9r/hint/sinh_hint10.py`: kiểm
sha256 r10 trước khi sửa; mỗi chuỗi cũ xuất hiện đúng 1 lần trong tệp và trong dòng; không dòng nào bị hai nhóm sửa; ngữ cảnh
không chạm dòng nhóm khác sửa (`assert`); mỗi nhóm là diff ĐỘC LẬP trên r10 gốc, 3 dòng ngữ cảnh; 0 dấu chéo ngược, 0 CR.
Đường dẫn repo-relative, không `a/`/`b/`. Hunk nhóm 1 thay nguyên dòng 41 (`depends_on` là một dòng ~12 KB) — đó là lý do cỡ tệp.

Lệnh (đúng PROMPT), trên tệp trong `goi/` (`cmp` khớp bản sinh), 10:5xZ:
```
T=$(mktemp -d -p "$R") && cp -a "$R/cay-kho" "$T/cay"
cd "$T/cay" && patch -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```
Output (T=`$R/tmp.GTnces2NdP`, GNU patch 2.7.6): **rc=0**; 4 lần "checking file ops/specs/lease-id-ep-kieu-yaml-r10.md";
"Hunk #1 succeeded at 38." "Hunk #2 succeeded at 55." "Hunk #3 succeeded at 1139." · "Hunk #1 succeeded at 404." "Hunk #2 succeeded
at 422." "Hunk #3 succeeded at 554." "Hunk #4 succeeded at 603." "Hunk #5 succeeded at 1141." · "Hunk #1 succeeded at 487." "Hunk #2
succeeded at 1176." · "Hunk #1 succeeded at 95." · "done". 11/11 succeeded; 0 dòng FAILED/fuzz/offset/malformed; `git status
--porcelain --ignored` của bản sao sau dry-run: 0 dòng. (Log: `do10.Nq9r/hint/dry_run_cuoi.log`.)

Áp THẬT tuần tự (`$R/apthat2.bYQV`, `patch -p0 --fuzz=0`): rc=0; 11/11; 8 hunk báo offset (2 hoặc 15 dòng, do nhóm 1 chèn dòng phía
trên), 0 fuzz, 0 FAILED; 0 `.rej`/`.orig`; 1304 → 1319 dòng; `cmp` với `do10.Nq9r/hint/ky_vong.md` (bản dựng độc lập: áp mọi thay
thế trên dòng gốc bằng Python) ⇒ KHỚP từng byte, sha256 `001251f7…755d`. Áp RIÊNG từng nhóm trên r10 gốc: cả 4 rc=0, 0
offset/fuzz/FAILED. (Log: `do10.Nq9r/hint/ap_that_cuoi.log`.)

Nhãn bắt buộc cho người áp (PROTOCOL §8 :600–601): *"chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm
commit"*. Đây là HINT cho một ĐẶC TẢ; mọi thay đổi thành revision 11; phiên soạn r11 phải đo lại mọi số và băm của chính r11 (các
số ghi "review lượt 10 đo" là của lượt này). HINT KHÔNG động vào chỗ phải đổi khi dựng r11 (tiêu đề "revision 10", điều kiện (3)
"đó là revision 10", công thức băm, tên tệp, bảng thay đổi đầu tệp, §9 bộ đếm sau lượt 10).

## GIỚI HẠN VÀ TOÀN VẸN
- KHÔNG ĐO ĐƯỢC từ `$R` (không mạng): trạng thái máy chủ (462 ref, người giữ live 09:18Z/09:45Z), REST PR #701/#689, thân #682
  (76bee6fb…, 3416 byte), #678 comment 5925743728, văn bản điều phối giao cho phiên soạn r10, CLI `a6de9d1` "0 KDĐ" (mirror thiếu
  `4bc9432`), hành vi trên Windows thật, dạng URL `origin` qua proxy git của phiên điều phối, lượt này có được giao qua
  `review-opus-max` hay không, branch protection thật (job nào bắt buộc ngoài closure).
- Đọc NGOÀI `$R` (chỉ đọc, không in thân, không in bí mật): `~/.claude/agents/review-opus-max.md` (băm, cỡ, hai khoá frontmatter);
  URL `origin` của `/home/user/tra-luat` (lọc che xác thực/cổng; ra `https://github.com/ducthangho/tra-luat`). Không in biến môi trường.
- Ghi: chỉ `$R/goi/` và các thư mục `mktemp -d -p "$R"`: `do10.Nq9r` (mọi script/log/kết quả), `ap9.Ivpf`, `tmp.kynKU9rAo7`,
  `apthat.t4NR` (dry-run/áp thật của bản HINT nháp, thay bằng bản cuối), `tmp.GTnces2NdP`, `apthat2.bYQV`; thư mục `rieng.*` tạo
  bằng `tempfile.mkdtemp(dir=$R)` đã xoá trong cùng script. Mọi clone `--no-local --no-hardlinks`; `kho.git` chỉ đọc.
  Kịch bản chuỗi đặt `HOME` vào thư mục con của `do10.Nq9r` (git config --global chỉ ghi ở đó).
- Một bản HINT nháp (sha256 `b20fa6d4…2a2e`) chỉ khác bản cuối một cụm chữ ("`fetch` tự kéo theo" → "`git clone` lấy theo"); bản
  trong `goi/` là bản cuối. Lệnh thử auto-follow tag bị hệ thống quyền từ chối; tôi không chạy lại bằng đường khác.
- CHƯA DỌN được: lệnh `rm -rf` các bản sao nặng của chính lượt này bị hệ thống quyền từ chối, và tôi không xoá bằng đường
  khác. Còn lại (đo `du -sh` lúc 10:5xZ, tổng ~1,4 GB, dưới trần ~4 GB): `do10.Nq9r/n311` 178M, `do10.Nq9r/n312` 176M,
  `apthat.t4NR` 176M, `apthat2.bYQV` 176M, `tmp.GTnces2NdP` 176M, `tmp.kynKU9rAo7` 176M, `do10.Nq9r/bn` 108M (phần lớn là
  `bn/arch20`), `do10.Nq9r/dotbien/v` ~43M, `do10.Nq9r/chuoi/kb*` ~32M. Log cần giữ đã chép vào `do10.Nq9r/hint/`.
- Tiến trình: năm lệnh nền do lượt này sinh (suite 3.11→3.12, đột biến, quét động, suite 7e5958e) đều kết thúc rc=0; không gọi
  lệnh giết nào.
- `cay-kho` cuối lượt: HEAD `42292b42…`, `status --porcelain --ignored` 0 dòng. Theo §8.2, snapshot sạch hai mốc không chứng minh
  chưa từng ghi rồi hoàn nguyên giữa chừng.
- Một lỗi đếm của chính lượt này: dòng nhật ký 10:36Z ban đầu ghi "7 biến thể" cho phép quét động; đã chạy trên 8 (N1–N8), sửa lại.
