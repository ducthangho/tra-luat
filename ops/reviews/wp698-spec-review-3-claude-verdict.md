verdict: changes_requested
reviewed_sha: 276a65f4514034f359ae55c13caa5e0a6d7db1c4
spec_sha256: 53bf55fec7ac8553ee8106a615940bb875846ab095e1fcb0544300a2a28dfe1b
model/effort tự khai: Claude Sonnet 5.5 (`claude-sonnet-5-5`), effort "max" theo chỉ thị điều phối; chạy bằng SUBAGENT trong phiên điều phối. KHÔNG phải codex. Effort thực đo từ bên trong: KHÔNG ĐO ĐƯỢC.
nhãn assurance của lượt này: `review_deferred` — `ops/bien_nhan_v2.py` dòng 703 (`che_do` chứa "subagent"), 720 (từ chối mọi mức trong `ASSURANCE_CAN_DOC_LAP` khi tự khai trong phiên điều phối hoặc thiếu bằng chứng), 736–737 (cùng họ model với executor ⇒ từ chối `cross_approved`). Đặc tả khai đúng điều này.
tổng kết: 0 P1 · 2 P2 · 4 P3 — 6 lớp / 11 biểu hiện (đếm lớp và đếm biểu hiện riêng; 3 lớp NỐI từ 16 lớp lượt 2, 3 lớp MỚI)
tỷ lệ vá thật 2→3 (§12): 13/16 = 81,25% (nghiêm: 12/16 = 75,00%); lớp mới tại r3 (không vào tử số): 3
ngưỡng áp: đặc tả khai 0 P1 · 0 P2 · 0 P3 ⇒ còn 6 lớp mở thì KHÔNG approve (`changes_requested`).
tệp: `HINT.patch` (chỉ sửa văn bản đặc tả r3, 6 nhóm `# lop: <slug>`) và thư mục `evidence/` (script đo + kết quả thô, KHÔNG gồm mã dựng ứng viên — Q14).


## GHI CHÚ KHỞI ĐỘNG VÀ TIỀN KIỂM

- Lượt này BẮT ĐẦU LẠI từ đầu theo chỉ thị điều phối (lượt trước chết ngay đầu vì hết hạn mức API): `goi/VERDICT.md` dở của lượt ấy đã bị GHI ĐÈ, không dùng số nào của nó. Container vừa khởi động lại lúc bắt đầu (uptime 5 phút): 0 tiến trình đo cũ còn sống.
- Dấu vết của lượt trước vẫn nằm trong sandbox (`$R/tmp.n6UxdzSoEY` 843 MB, `$R/tmp.n6uxdzsoey` 3,6 MB): KHÔNG phải của tôi, tôi KHÔNG xoá, KHÔNG dùng làm đầu vào của phép đo nào. Mọi con số là của lượt NÀY, từ ứng viên do lượt NÀY dựng.

```
$ sha256sum PROMPT.md SPEC.md SPEC-r2.md SPEC-r1.md
4d29044c3f7ae6a612f9ab464cfa0f321b12baefb02b05804940b94dd21f5e68  PROMPT.md
53bf55fec7ac8553ee8106a615940bb875846ab095e1fcb0544300a2a28dfe1b  SPEC.md
f69bb398441168830443d4e095be18247fc4029c930fce8793cfb6574a652c0a  SPEC-r2.md
3a55526305e17cf06c644e2e3448cb8720aa67e8d6c0cab571d8e49dac974996  SPEC-r1.md
$ git -C cay-kho rev-parse HEAD                    -> 276a65f4514034f359ae55c13caa5e0a6d7db1c4
$ cmp SPEC.md cay-kho/ops/specs/ci-g5-cong-cu-va-tiep-r3.md   -> trùng
$ git hash-object ops/cong_cu_test.py ; git rev-parse fc852ff:ops/cong_cu_test.py   -> 9edea6b1629b46f27758b2073e74210dc73495b7 (cả hai)
```
Tiền kiểm KHỚP, không dừng. `origin/master` trong `kho.git`: ref `origin-master` = `7e5958e` (merge PR #703, 2026-10-01T16:52:59+07:00), KHÔNG phải `20ec8d5` như PROMPT; blob `ops/cong_cu_test.py` ở `20ec8d5` và `7e5958e` đều `9edea6b1…` (`git diff --stat fc852ff 7e5958e -- ops/cong_cu_test.py` rỗng). `ab457c6` (phiên điều phối khai là `origin/master` ngày 07-10, write set "không đổi") KHÔNG có trong mirror (`git cat-file -t ab457c6` ⇒ "Not a valid object name"): câu ấy là LỜI KHAI ĐIỀU PHỐI, KHÔNG ĐO ĐƯỢC từ sandbox (không mạng).

## GIỚI HẠN KHAI THẲNG

- KHÔNG mạng: KHÔNG ĐO ĐƯỢC ruleset LIVE `20856202`, số ref, lease #671, `ab457c6`, thời lượng job CI thật, Windows, và việc phiên điều phối đã "báo chủ kho trước khi soạn revision" (S6).
- `jsonschema` không cài ⇒ `t2` luôn `bo_qua` ở MỌI phép đo (đúng như phiên soạn r3 và reviewer lượt 2; CI có jsonschema ghim 4.26.0 nên `t2` chạy ở đó). PyYAML là bản hệ thống, không phải 6.0.3 ghim. ruff chỉ có 0.15.8 (bản ghim 0.15.15 KHÔNG ĐO ĐƯỢC).
- Mọi phép đo đột biến chạy trên Python 3.12.3 (bản `ci.yml` ghim); 3.11.15 và 3.13.12 chỉ dùng cho số đếm tĩnh.
- **Ứng viên là của TÔI, không phải của executor.** Mọi phát hiện "làm đúng từng chữ" là về ứng viên độc lập do tôi dựng từ chữ đặc tả (bốn đời `ind` → `ind4`, xem ĐỐI CHIẾU); executor thật có thể viết khác (kể cả tự tránh các bẫy ở lớp 1–2). Ứng viên và công cụ dựng KHÔNG được giao (Q14).
- **Máy dùng chung, đo tường KHÔNG phải "máy rảnh" tuyệt đối.** `nproc` = 4; một phiên khác (`…/scratchpad/cr710-l1/pwsh/…`) chiếm khoảng 0,3–1 lõi trong suốt buổi đo; tôi không chạm vào nó. Mọi con số thời gian tường chịu ảnh hưởng này (đó cũng chính là bằng chứng cho lớp `t53-…`); con số CPU (`getrusage`) không chịu.
- A5 trọn tám mảnh KHÔNG chạy: chỉ MỘT mảnh (`k = 0/8`) trên nền (52 đột biến) và trên ứng viên (59 đột biến), cộng mẫu 68 đột biến cũ nhắm `t52`/`t53`/`t54` (trong 204) chạy trên ứng viên bằng chính `_do_ban_kinh`. Phần còn lại của 470 đột biến KHÔNG ĐO ĐƯỢC.
- Trên NỀN chỉ đo Phụ lục A (30 dò) và một mẫu 24 dò của Phụ lục H; các câu "PHẢI ĐỎ Ở nền" cho Phụ lục C trọn (221 dò) KHÔNG đo lại — dùng số của r2/r3 và đánh dấu như vậy ở BẢNG ĐO. Các cây IMP-MIN, IMP-GEN, `cand`, `v3_*` KHÔNG có trong sandbox; `cand`/`tv_*` của r3 được thay bằng các biến thể tôi tự dựng từ ứng viên của mình (`go_exc` ≈ `cand` cho miền ngoại lệ; `tv_exc`, `tv_head`, `tv_list`, `go_*`); mỗi biến thể được kiểm "không đột biến thì `t52 t53 t54` phải `qua`" trước khi tin (phép kiểm ấy bắt được ba cây biến thể tự dựng sai của chính tôi — `tv_list`, `go_nfkc_p`, `go_cc_p` — và kết quả của chúng trước khi sửa đã bị bỏ).
- Phản chứng `bo-cu` của Phụ lục F không chạy lại.
- Danh sách dò mới (`y_*`, 28 dò) do tôi liệt kê từ mã nên có thể thiếu; lượt sau tìm ra đường sống nào ngoài danh sách vẫn là finding.


## ĐỐI CHIẾU LƯỢT TRƯỚC (protocol §8/§8.3) — làm TRƯỚC mọi hướng săn mới

Nguồn lượt trước: `luot2/VERDICT.md` (sha256 `e281338f…3968`, Sonnet 5.5 subagent, `reviewed_sha c54b502`, 0 P1 · 4 P2 · 12 P3 = **16 lớp** / 56 biểu hiện). Cách đo: tôi tự dựng ỨNG VIÊN ĐỘC LẬP chỉ từ chữ của §5 M1–M5b + bảng 54 canh (không đọc, không dùng `v3_*`, `cand`, `tv_*` của phiên soạn r3; các cây ấy cũng không có trong sandbox), rồi chạy chính Phụ lục A, C+H (366 dò), D, E, F, G, I của r3 trên nền `fc852ff` (Python 3.12.3) và trên ứng viên; thêm các dò TỰ THÊM ngoài 366 dò (BẢNG SĂN hàng 8–9) và các biến thể làm sai MỘT chỗ để đo răng (hàng 2). Từ vựng (§8): ĐÃ ĐÓNG = ĐÃ VÁ THẬT theo §8.3 (mọi biểu hiện trong phạm vi đo đã đóng, không còn biểu hiện cùng cơ chế do bản vá sinh ra, không còn phần phải đo) · CÒN MỞ · VÁ SINH LỖI MỚI · TÁI PHÁT (cùng cơ chế còn sống sau bản vá).

Ứng viên độc lập — bốn đời, vì sao có bốn (mỗi đời sửa đúng MỘT thứ tìm thấy khi chạy chính tiêu chí của r3):
`ind` (đúng từng chữ) → `ind2` (+ bắt ngoại lệ ở ô bộ ghi, lớp `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia`) → `ind3` (+ ba ô ngoại lệ r2 "giữ từ r2") → `ind4` (+ dựng literal của canh `x3_wr5_nfkc` bằng nối chuỗi, lớp `canh-x3-wr5-nfkc-tu-va-cham-mo-neo`). Kết quả A4 trên `ind4` ở BẢNG ĐO.

| # | slug lượt 2 (hạng) | trạng thái lượt 3 | bằng chứng tự đo | lớp lượt 3 nối |
|---|---|---|---|---|
| 1 | `m5-ngoai-le-chi-ba-kieu` (P2) | **ĐÃ ĐÓNG** | T-E 30/30 GIẾT đúng `t53` trên `ind3`; `tv_exc` (đúng hướng HINT) 7/30 SỐNG: `x3_exc_{kbint,sysexit,genexit,bexgroup,exgroup,re_error,json}` — đúng bảng §1.9.3; `go_exc` (gỡ miền `E698`) ba canh E của r3 SỐNG lại, `z_exc_*` vẫn GIẾT; 8 dò ngoại lệ TỰ THÊM (`y_exc_*`): 7 GIẾT + 1 tương đương (`shutil.Error` là lớp con `OSError`: `issubclass` ⇒ True) | — (nhưng mệnh đề "Bậc hai" của A8 sai trên ứng viên r3: `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan`) |
| 2 | `ra-ha-nguon-main-bo-ghi-chua-co-o` (P2) | **TÁI PHÁT (hẹp)** | ĐÓNG ở T1–T4 và chỗ `write_bytes` của T5: T-C 81 dò = 78 GIẾT đúng `t53`/`t54`/`t52` bán kính 1 + 1 tương đương (`x3_wr5_normpath`) + 2 đối chứng KHÁC (`x3_wr_ra_lower`, `s_ra_realpath`), đúng khai; 11/11 dò TỰ THÊM ở T2–T4 (thành viên U+2063/U+E0020/`ａ` ×8) và ở T5 (`mkdir` ×2, `exists`) GIẾT. CÒN SỐNG ở T5: `unlink` (1) và dòng in (2) — đúng hàng T5 của bảng M2b khai "cùng ô bộ ghi của T4"; và A2 không đo THÀNH VIÊN ở T2–T5 (ứng viên bỏ hai ô thành viên vẫn qua 10/10 dò T-C đã thử, 8/8 dò thành viên SỐNG) | `ra-ha-nguon-main-bo-ghi-chua-co-o` (P3, còn mở) |
| 3 | `head-nhieu-dong-chi-tach-lf-chua-co-o` (P2) | **ĐÃ ĐÓNG** | Phụ lục H trên ứng viên: 44 dò `head` = 41 GIẾT + 3 KHAI SỐNG (đúng khai); `go_tach` 4 SỐNG lại (`x_head_nl_last`, `x3_head_{emsp,us,nel}_last`), 2 vẫn GIẾT (`x3_head_tab_last`, `x_head_lastline`) — đúng §1.9.8; `tv_head` (tập `splitlines` của HINT) 2 SỐNG (`x3_head_us_last`, `x3_head_emsp_last`) trên 44 dò — đúng §1.9.4; 6 dò `head` TỰ THÊM (`y_head_*`: `re.search`, `findall`, `partition`, `rpartition`, regex-token, cắt 40) 6/6 GIẾT | — |
| 4 | `t53-thoi-gian-khong-co-tieu-chi-do` (P2) | **VÁ SINH LỖI MỚI (hẹp)** | tiêu chí A4-g ĐÃ CÓ và có răng (phép ĐẾM không nhiễu 10/10; `tv_naive` ĐỎ cả hai phép, `tv_cham` chỉ ĐỎ đồng hồ); phép ĐỒNG HỒ đỏ giả 2/12 lần khi CPU quá tải, và biên 30 phút ở Δ = 10 s chỉ là điểm giữa của dải đo 24,8–30,3 phút (mảnh A5 thật: nền 522,9 s/52, ứng viên 669,6 s/59, cả hai 'bán kính 1') | `t53-thoi-gian-khong-co-tieu-chi-do` (P3, còn mở) |
| 5 | `a1-tap-dong-thieu-do-theo-nhom-unicode` (P3) | **ĐÃ ĐÓNG** | 27 nhóm có mặt trong `D698` (đo: 27 ở 3.11.15 và 3.12.3); 27 dò xoá-nhóm trên ứng viên: 26 GIẾT + 1 KHÁC (`x3_cat_ll_bk`, đối chứng khai); `tv_list` 4/27 SỐNG (Mc, Me, Pf, Pi) — đúng §1.9.7 | — |
| 6 | `phu-luc-c-dem-209-lech-221` (P3) | **ĐÃ ĐÓNG** | `liet_ke` = 221 (A) · 145 (H) · ghép 366; chữ "209 + 12 = 221" ở §1.9.10 | — |
| 7 | `s1-8-8-nhan-tag-sai` (P3) | **ĐÃ ĐÓNG** | 3.11.15: 120 = 97 TAG + 23; 3.12.3: 127 = 97 + 30 (đếm bằng `unicodedata`) | — |
| 8 | `tran-vong-so-10-hai-cho` (P3) | **ĐÃ ĐÓNG** | quét số mười đứng riêng gần vòng/trần/ADR-0048/`tran_cu`: 6 kết quả = 1 `tran_cu: 10` + 5 ngưỡng Δ | — |
| 9 | `s6-chep-thieu-quy-tac-dung` (P3) | **ĐÃ ĐÓNG** | 14 dòng 1043–1056 của protocol so từng dòng: 14/14 trùng; sha256 đoạn nối LF = `dc93c2a3…f7715` | — |
| 10 | `head-moi-vi-tri-moi-thanh-vien-qua-loi` (P3) | **ĐÃ ĐÓNG** | `objective` nay một dòng (áp HINT lượt 2 lên r2 làm vỡ bảng ở dòng 14–15: đo bằng `patch` + đếm dòng không mở bằng `\|`); ba dò khai SỐNG đúng khai (KHAI 5/5 SỐNG trên ứng viên: 3 `x_head_*` ở `ind2`, 2 `x_f50_*` ở `ind3`) | — |
| 11 | `a5-canh-khong-kiem-bang-do` (P3) | **ĐÃ ĐÓNG** phần nêu; **phép kiểm vẫn thủng ở chỗ khác** | Phụ lục F: `lech-bo` ✓, `tap-ten` ✓ (đo lại), trên ứng viên `so_loi = 0`. Nhưng F không đếm lần xuất hiện của mỏ neo ⇒ lớp MỚI `canh-x3-wr5-nfkc-tu-va-cham-mo-neo` | (lớp mới, nối `a5-…`) |
| 12 | `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` (P3) | **TÁI PHÁT (hẹp)** | định nghĩa nhóm chốt (A1-b2): `go_nfkc_p` 4 SỐNG lại + 6 vẫn GIẾT; `go_cc_p` 1 + 7 — khớp bảng r2/r3; NHƯNG mệnh đề bậc hai của A8 ("gỡ riêng ba ô ngoại lệ của r2 ⇒ hai canh E của r2 SỐNG lại") chỉ đúng trên `IMP-R2-GO` của r2, SAI trên ứng viên r3: ứng viên không có ba ô r2 (`ind2`) vẫn GIẾT `z_exc_*` 5/5; chỉ gỡ ĐỒNG THỜI ba ô và miền `E698` (`go_both`) mới làm chúng SỐNG | `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` (P3, còn mở) |
| 13 | `doc-bang-205-vs-211` (P3) | **ĐÃ ĐÓNG** | cộng từng cột bảng họ §2: 221 · 10 · 211 · 190 · 144 · 16 · 8 · 1; hai hàng Z góp 6 ⇒ 205/184/138 | — |
| 14 | `s11-1-thieu-cach-doc-q4-q9-q13` (P3) | **ĐÃ ĐÓNG** | §11.1 (B): đúng 14 hàng Q1–Q14; nhãn chọn/không chọn chép khớp thân comment `5914438647` (sha256 thân `4a2dba07…684d0`) | — |
| 15 | `a4-d-khong-co-phep-do-may` (P3) | **ĐÃ ĐÓNG** | Phụ lục G trên `ind4`: `"cham": []`, rc=0; phản chứng chạy lại: chạm thân `_van_tay` ⇒ rc=1, chèn ngay sau hàm ⇒ rc=1, chạm `main` ⇒ rc=1 | — |
| 16 | `thu-hoi-do-khong-co-diem-dung` (P3) | **ĐÃ ĐÓNG** | S7b có; `ops/lease_publish.py:1093` `SO_THU_HOI_KICH_HOAT = False`; `trich-log.txt` dòng 102 `thu-hoi · run 36688032631`, 103–104 = mục log thô 765/767 | — |


## TỶ LỆ VÁ THẬT 2→3 (protocol §12; "ĐÃ VÁ THẬT" theo §8.3)

U = 16 slug lớp còn mở cuối lượt 2 (4 P2 + 12 P3; nhiều biểu hiện cùng lớp chỉ tính một lần). F = tập con của U mà lượt 3 xác minh ĐÃ VÁ THẬT (mọi biểu hiện trong phạm vi đo đã đóng, không còn biểu hiện cùng cơ chế do bản vá sinh ra, không còn phần phải đo; cắt phạm vi hay thiếu quan sát không tính là vá).

- **|U| = 16.** **|F| = 13** — `m5-ngoai-le-chi-ba-kieu` · `head-nhieu-dong-chi-tach-lf-chua-co-o` · `a1-tap-dong-thieu-do-theo-nhom-unicode` · `phu-luc-c-dem-209-lech-221` · `s1-8-8-nhan-tag-sai` · `tran-vong-so-10-hai-cho` · `s6-chep-thieu-quy-tac-dung` · `head-moi-vi-tri-moi-thanh-vien-qua-loi` · `a5-canh-khong-kiem-bang-do` · `doc-bang-205-vs-211` · `s11-1-thieu-cach-doc-q4-q9-q13` · `a4-d-khong-co-phep-do-may` · `thu-hoi-do-khong-co-diem-dung`.
- **Không vào F (3):** `ra-ha-nguon-main-bo-ghi-chua-co-o` (TÁI PHÁT hẹp: T5 `unlink` + dòng in SỐNG; A2 không đo thành viên hạ nguồn) · `t53-thoi-gian-khong-co-tieu-chi-do` (VÁ SINH LỖI MỚI hẹp: A4-g đồng hồ/biên) · `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` (TÁI PHÁT hẹp: mệnh đề đầu của A8 bậc hai).
- **Tỷ lệ = 13/16 = 81,25%.** Cách đọc NGHIÊM (xếp `a5-canh-khong-kiem-bang-do` vào TÁI PHÁT vì phép kiểm A5 vẫn thủng ở chỗ khác — lớp mới `canh-x3-wr5-nfkc-tu-va-cham-mo-neo`): 12/16 = 75,00%. Lớp MỚI tại r3 (không vào tử số): 3 — `canh-x3-wr5-nfkc-tu-va-cham-mo-neo` (P2), `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia` (P2), `r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat` (P3). Lớp tái mở (đã đóng rồi mở lại): 0. Phần chưa đo: xem GIỚI HẠN KHAI THẲNG.
- Chuyển tiếp lượt 1→2 theo S6 của r3: 2/8 hoặc 3/8 (< 50%); lượt 2→3: ≥ 75% (≥ 50%) ⇒ KHÔNG có hai chuyển tiếp LIÊN TIẾP < 50% (điều kiện dừng thứ nhất của §12 không kích hoạt). Như §12 dặn: tỷ lệ cao chỉ nói về tập U, không chứng minh hội tụ khi lớp mới vẫn xuất hiện (ba lớp mới, trong đó hai P2).
- **Điều kiện §12 (2) — "một lớp xuất hiện ở ba lượt review khác nhau đòi xem lại cách làm tại checkpoint": KÍCH HOẠT cho ba họ** (đếm theo bảng nối của chính các verdict): họ `ra` — `ra-thieu-hang-chuan-hoa-lop-b` (lượt 1) → `ra-ha-nguon-main-bo-ghi-chua-co-o` (lượt 2) → T5 còn sống (lượt 3); họ thời gian/tiêu chí — `tieu-chi-nghiem-thu-thieu-chinh-xac` (lượt 1) → `t53-thoi-gian-khong-co-tieu-chi-do` (lượt 2) → A4-g đồng hồ/biên (lượt 3); họ bậc hai — `tieu-chi-nghiem-thu-thieu-chinh-xac` (lượt 1) → `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` (lượt 2) → mệnh đề A8 (lượt 3). Quyết định có đưa tới Review Rescue Checkpoint và việc "báo chủ kho kèm bảng lớp TRƯỚC khi soạn revision 4" (S6) thuộc phiên điều phối/chủ kho, không thuộc reviewer; tôi chỉ ghi điều kiện đã thoả. Cả ba biểu hiện lượt 3 đều ở mức P3 hẹp.


## BẢNG LỚP

Mỗi finding có đúng một slug lớp nguyên nhân; đếm lớp và đếm biểu hiện riêng (protocol §8.3). `reviewed_sha` mọi lớp: `276a65f4514034f359ae55c13caa5e0a6d7db1c4`. Lớp nối lịch sử giữ NGUYÊN slug lượt 2 (protocol §8.3: "giữ stable slug"). Cột phương án chỉ MÔ TẢ (Q14); bản vá văn bản nằm ở `HINT.patch`, nhóm mở bằng `# lop: <slug>`.

| slug lớp | hạng | biểu hiện (đếm) | nguồn | phương án (chỉ mô tả; Q14) | phép kiểm đóng lớp / giới hạn |
|---|---|---|---|---|---|
| `canh-x3-wr5-nfkc-tu-va-cham-mo-neo` | P2 | 1: canh `x3_wr5_nfkc` — mỏ neo một dòng `    tep.write_bytes((` có mặt HAI lần khi ghi bảng bằng literal; đột biến rơi vào literal ⇒ lỗi cú pháp ⇒ 9 ca `tin_dung_gia` ⇒ canh KHÁC; Phụ lục F `so_loi = 0` ở cả cây hỏng lẫn cây sạch | MỚI (nối `a5-canh-khong-kiem-bang-do`, P3 lượt 2) | §5: đòi "mỏ neo xuất hiện đúng một lần trong tệp ứng viên sau khi bảng đã ghi" và dặn dựng literal canh một dòng bằng nối chuỗi/escape; A5 thêm (vii) `count == 1` cho 54 mục (hoặc thêm phép đếm vào Phụ lục F — băm đổi) | `count_neo.py`: nền 54/54 = 1 · `ind3` `[('x3_wr5_nfkc', 2)]` · `ind4` 54/54; dò `x3_wr5_nfkc`: KHÁC (`ind3`) → GIẾT `t52_` (`ind4`). Giới hạn: không chạy A5 tám mảnh trọn; dùng đúng đường `_do_ban_kinh` của A5 cho từng canh |
| `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia` | P2 | 1: dò/canh `x_wr_ra_nfkc` trên ứng viên làm đúng từng chữ ra `tin_dung_gia` (`OSError: [Errno 36] File name too long` thoát khỏi ô, cửa `--tu-kiem-gom` chết rc=1) thay vì GIẾT `t52` bằng chốt | MỚI | M2b thêm: ô bộ ghi phải bắt mọi ngoại lệ do `_ket_thuc_manh` ném và so nó như một kết quả với kỳ vọng dựng độc lập | dò `x_wr_ra_nfkc` GIẾT `t52_` (bán kính 1/56) thay vì `tin_dung_gia`; giới hạn: chạy trên ứng viên đúng chữ đầu tiên (`ind`), không trên bản của executor |
| `t53-thoi-gian-khong-co-tieu-chi-do` | P3 | 2: (a) phép ĐỒNG HỒ của A4-g đo giây tường: cùng ứng viên đúng cho Δ = 5,9–11,7 s tuỳ tải, ĐỎ giả 2/12 lần khi CPU quá tải (Δ CPU 6,2–6,5 ổn định); (b) "giữ ≈ 2,5 phút biên" ở Δ = 10 s không chứng minh được: đo mảnh A5 thật cho dải 24,8–30,3 phút | VÁ SINH LỖI MỚI (hẹp; lượt 2, P2) | giữ phép ĐẾM; ghi điều kiện đo + thêm Δ CPU (tự thân + con); thay lời khai biên bằng dải đo và giả định bão hoà CPU của runner; nếu cần biên ≥ 2 phút ở cực CPU thì hạ ngưỡng ≈ 7,5 s | Phụ lục I rảnh ×3 và 4 hog ×3: cùng kết luận trên ứng viên đúng; `tv_cham` vẫn ĐỎ. Giới hạn: runner KHÔNG ĐO ĐƯỢC; phiên khác dùng chung CPU |
| `ra-ha-nguon-main-bo-ghi-chua-co-o` | P3 | 4: T5 `unlink` (1) và dòng in (2) SỐNG; A2 không đo thành viên ở T2–T5 (1: ứng viên thiếu hai phần M2b qua T-C 10/10, 8 dò thành viên SỐNG) | TÁI PHÁT hẹp (lượt 2, P2) | tách hàng T5 của bảng M2b (thêm ô tệp cũ tại `tep` + so dòng in, hoặc khai thẳng vào §10); thêm dò thành viên ngoài `R698` cho T2/T3a/T3b/T4 vào T-C | 3 đột biến T5 GIẾT `t52_`; 8 dò thành viên SỐNG ở `ind3_nomem`, GIẾT ở `ind3`. Giới hạn: `unlink` chỉ đo NFKC và `strip` |
| `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` | P3 | 1: mệnh đề đầu của A8 "Bậc hai" sai trên ứng viên r3 (và câu "chết vì ba ô của r2" ở §1.9.8) | TÁI PHÁT hẹp (lượt 2, P3) | sửa thành "gỡ ĐỒNG THỜI ba ô r2 và miền `E698` ⇒ SỐNG lại; gỡ riêng một ⇒ vẫn GIẾT" | `ind2` 5/5 GIẾT · `var_go_exc` 7/7 GIẾT · `var_go_both` `z_exc_all`, `z_exc_them_valueerror` SỐNG |
| `r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat` | P3 | 2: "ba ngưỡng" của HINT (HINT có hai) ở 4 chỗ; tên `f49_*`/`f50_*` ở §1.8.7 không tra được trong phụ lục | MỚI | đổi "ba" → "hai", bỏ vế ngưỡng chưa từng được đề nghị; thêm bảng ánh xạ tên | `grep -n "ba ngưỡng" SPEC.md` rỗng |

Tổng kết lượt 3: **0 P1 · 2 P2 · 4 P3 = 6 lớp** / 11 biểu hiện — trong đó 3 lớp NỐI từ U của lượt 2 (`t53-…` hạ từ P2 xuống P3, `ra-ha-nguon-…` hạ từ P2 xuống P3, `bac-hai-…` P3) và 3 lớp MỚI (`canh-x3-wr5-…` P2, `m2b-o-bo-ghi-…` P2, `r3-khai-ve-hint-…` P3). Cả hai lớp P2 đều là lớp MỚI do chính chữ r3 sinh ra (không lớp P2 nào của lượt 2 còn ở hạng P2).


## BẢNG SĂN

Mỗi hàng là MỘT HƯỚNG theo mẫu PROMPT (giả thuyết → lệnh → output → kết luận) viết gọn trong một ô; cột kết luận dùng đúng ba nhãn LỖI · KHÔNG PHẢI LỖI · KHÔNG ĐO ĐƯỢC. Hướng dẫn tới lớp có khối đầy đủ trong CHI TIẾT TỪNG LỚP. 16 hướng: 7 gợi ý của PROMPT (hàng 1–7) cộng 9 hướng tự thêm (hàng 8–16).

| # | hướng | giả thuyết → lệnh → output (rút gọn) | kết luận |
|---|---|---|---|
| 1 | Tái hiện Phụ lục A–I | tách chín khối mã từ SPEC.md rồi băm: 9/9 khớp; ghép C+H bằng lệnh của Phụ lục H: sha256 `37b6e8bd…6e55b` khớp, `liet_ke` 221 + 145 = 366, A ∩ ghép = ∅. **Phụ lục A:** trên nền 24 SỐNG + 5 GIẾT + 1 KHÁC (`c49_ra_abspath`, bán kính 2) = đúng "24 sống + 6 đối chứng"; trên ứng viên 21 GIẾT + 1 KHÁC + 8 SỐNG (đúng tám dò F48, nợ Q1). **Phụ lục H** trên ứng viên 145/145 đúng khai (KHAI 5 SỐNG, NGOẠI 5 SỐNG, T-B 67 + 1 KHÁC, T-C 38 + 1 KHÁC + 1 SỐNG, T-D 4, T-E 23). Phụ lục B: sha256 đầu ra `42ca657c…741d` khớp (3.11.15 và 3.12.3). Phụ lục E, F, G, I: BẢNG ĐO | KHÔNG PHẢI LỖI |
| 2 | Răng của A* (bản SAI-nhưng-thoả-chữ) | 9 biến thể dựng từ chính ứng viên, mỗi cái sai MỘT chỗ, kiểm "không đột biến thì `t52 t53 t54` phải `qua`" trước khi tin: `tv_exc` (miền HINT) 7/30 SỐNG ✓ khớp §1.9.3; `go_exc` (≈ `cand`) 22/30 SỐNG ✓ khớp §6 A8; `tv_head` (`splitlines`) 2 SỐNG + 3 KHAI trong 44 dò `head` ✓; `tv_list` (danh sách nhóm) 4/27 SỐNG (Mc, Me, Pf, Pi) ✓; `go_tach` 4 SỐNG lại + 2 GIẾT ✓; `go_nfkc_p` 4 + 6 · `go_cc_p` 1 + 7 ✓; `go_ra2` 4 SỐNG lại + `s_ra_cf` GIẾT ✓; `naive` (không trỏ `TEP_TEST`): Phụ lục I ĐỎ `dem` + `dong_ho`. Bản thiếu thành viên hạ nguồn (`nomem`) qua T-C 10/10 | răng CÓ ở mọi hướng r3 khai; **A2 không phân biệt bản thiếu thành viên hạ nguồn** (hàng 9) |
| 3 | Tín dụng giả | `hang` (Phụ lục D) chỉ nhận `giet_that` đúng ca đích, `khong_qua` khoá theo 4 ký tự đầu tên ca (t23_/t24_/t25_ trùng nhau nhưng không ảnh hưởng đích t52–t54). Trên ứng viên đủ chữ mọi dòng KHÁC đều là đối chứng khai trước (`x3_cat_ll_bk`, `x3_wr_ra_lower`, `s_ra_realpath`, `c49_ra_abspath`) — trừ HAI dòng sinh từ chữ đặc tả: `x_wr_ra_nfkc` trên ứng viên đúng từng chữ (`OSError: [Errno 36] File name too long` thoát khỏi ô ⇒ lớp `m2b-o-bo-ghi-…`) và `x3_wr5_nfkc` (mỏ neo tự va chạm ⇒ lớp `canh-x3-wr5-…`); cả hai bị `hang` phân đúng là KHÁC, không bị lừa | LỖI: P2 ×2; cơ chế phân hạng KHÔNG bị lừa |
| 4 | Trung thành quyết định chủ kho | so 4 hàng nhãn của §11 với thân comment `5914438647`: nhãn chọn/không chọn chép khớp từng chữ; 14 hàng Q của §11.1 (B) (đếm: 14); các cách đọc rộng/chặt hơn chữ đều được liệt kê (Q4, Q9, Q13 …) và đòi comment Q10 xác nhận; không điểm nào TRÁI chữ chủ kho | KHÔNG PHẢI LỖI |
| 5 | Closure + hợp đồng | `required_checks` so `ci.yml`@`fc852ff` bằng PyYAML: đủ sáu job, `gate-cong-cu` matrix os × manh 0–7 `timeout-minutes: 30`; ma trận `os` chỉ thêm `windows-latest` khi `workflow_dispatch`/nhãn `windows` — đúng ở cả `fc852ff` lẫn `7e5958e` (mục "Chạy Windows" §4 đúng; câu "master chạy cả ubuntu lẫn windows" trong `CLAUDE.md` lệch `ci.yml`, ngoài phạm vi); write set 1 tệp: `git diff --name-only` = `ops/cong_cu_test.py`; blob `9edea6b1…` ở `fc852ff`/`423b4ba`/`20ec8d5`/`7e5958e`; trần 300 dòng: ứng viên độc lập +311/−4 (đặc tả ước 292–307 nếu viết như biến thể đo, 268–283 nếu gọn; S5 đã nêu cách xử lý). `origin/master` `ab457c6`, ruleset LIVE, lease #671: KHÔNG ĐO ĐƯỢC | KHÔNG PHẢI LỖI (S5: rủi ro đã khai, +311 > 300 ở bản viết rộng) |
| 6 | Số liệu (số hạng, không chỉ quan hệ) | xem BẢNG ĐO: 74 hàng đo lại; 3 hàng KHÔNG khớp/ĐỎ giả — "ba ngưỡng" của HINT (đặc tả: 3, thực: 2), tên canh `f49_*`/`f50_*` (không tra được), ĐỎ giả của A4-g khi quá tải; ngoài ra hai lời khai rộng hơn phép đo nằm trong hàng khác: "mỗi mỏ neo xuất hiện đúng một lần" (đúng trên nền, sai trên ứng viên ghi bảng bằng literal `repr`) và "giữ ≈ 2,5 phút biên" (ƯỚC, điểm giữa của dải đo) | LỖI P3 (`r3-khai-ve-hint-…`, `t53-…`) và P2 (`canh-x3-wr5-…`); các hàng còn lại khớp, khớp trong dải hoặc là số đo không có đối chiếu (CPU) |
| 7 | Mức assurance | `ops/bien_nhan_v2.py` dòng 703 (`che_do` chứa "subagent"), 720 (`khai in ASSURANCE_CAN_DOC_LAP and (tu_khai_trong_phien or not co_bang_chung)`), 736–737 (cùng họ model ⇒ từ chối `cross_approved`): subagent Sonnet ⇒ `review_deferred` đúng | KHÔNG PHẢI LỖI |
| 8 | Đường CÙNG cơ chế sống ngoài 366 dò | liệt kê theo TẦNG DÒNG CHẢY của `ra`/`head`/ngoại lệ (không theo tên dò); 28 dò mới `y_*` (`extra_rv3.py`): T5 bộ ghi ×6 · `head` ×6 · `main` T2 ×3 · T3a/T3b ×2 · bộ ghi T4 ×3 · ngoại lệ ×8. Trên ứng viên đủ ô: 24 GIẾT + 4 SỐNG: `y_exc_shutil` (tương đương: `shutil.Error` ⊂ `OSError`), `y_wr5_unlink_nfkc`, `y_wr5_print_nfkc`, `y_wr5_print_strip` (T5: chỗ dùng `tep` khác `write_bytes`) | LỖI P3 (lớp `ra-ha-nguon-main-bo-ghi-chua-co-o`, TÁI PHÁT hẹp); 7/8 dò ngoại lệ, 6/6 `head`, 11/11 `main`/bộ ghi khác: KHÔNG PHẢI LỖI |
| 9 | Thành viên × tầng hạ nguồn | bản thiếu hai phần của M2b (ô "mọi `D698`" ở tầng `main` và khúc tên tệp ở bộ ghi; 7 dòng khác `ind3`): toàn bộ 10 dò T-C thử đều GIẾT; 8 dò thành viên (U+2063 · TAG SPACE U+E0020 · `ａ` fullwidth) ở T2/T3a/T3b/T4 SỐNG 8/8; trên ứng viên đủ ô 8/8 GIẾT | LỖI P3 (cùng lớp hàng 8: A2 không đo thành viên hạ nguồn) |
| 10 | Mỏ neo tự va chạm | `count(tim)` của 54 mỏ neo trong tệp: nền 54/54 = 1; `ind3` 53/54, `x3_wr5_nfkc` = 2; `ind4` 54/54. Phụ lục F `so_loi = 0` ở cả hai | LỖI P2 (`canh-x3-wr5-nfkc-tu-va-cham-mo-neo`) |
| 11 | A4-g: đồng hồ, đếm, biên 30 phút | Phụ lục I trên ứng viên đúng: Δ tường 5,9–11,7 s qua 12 lần (đỏ giả 2/12, cả hai khi CPU quá tải), Δ CPU 6,2–6,5 s ở mọi tải; `lon` 67/64 ở 10/10 lần; `tv_naive` ĐỎ cả hai phép, `tv_cham` chỉ ĐỎ đồng hồ. Một mảnh A5 thật: nền 522,9 s (52 đột biến) · ứng viên 669,6 s (59), cả hai "bán kính 1"; dải dự báo mảnh CI ở Δ = 10 s: 24,8–30,3 phút (r3 khai 27,5, điểm giữa) | LỖI P3 (`t53-thoi-gian-khong-co-tieu-chi-do`); phép ĐẾM tất định: KHÔNG PHẢI LỖI |
| 12 | `t47` bỏ qua khi song song có phải lỗ đo | `t47` chỉ `BoQuaMoiTruong` ở ba chỗ (`git replace` lỗi, không dựng INDEX chưa hoà giải, không tạo được symlink); đếm trong 756 dòng kết quả (mỗi dòng = một lượt 56 ca, 4 song song, tải ≈ 5–8 trên 4 lõi) + hai lượt gate đầy đủ: `t47_` chưa lần nào ở `khong_qua`; `t47_par.py ind4 10` (10 vòng × 4 tiến trình cùng chạy ca): 40/40 `qua` (tổng 0 lần `t47_` ở `khong_qua`). `bo_qua` không bao giờ là `chet` trong `hang` ⇒ dù có bỏ qua, phân hạng 3 ca đích không đổi | KHÔNG PHẢI LỖI (không tái hiện; nguyên nhân gốc KHÔNG ĐO ĐƯỢC như r3 khai) |
| 13 | 11 điểm r3 nói HINT lượt 2 sai | bảng 11 điểm ở CHI TIẾT lớp 6: 9 ĐÚNG, 1 ĐÚNG MỘT PHẦN (điểm 5: HINT có hai ngưỡng, không ba), 1 KHÔNG ĐO ĐƯỢC (điểm 4, lập luận theo cấu tạo; r3 cũng không dựng biến thể theo HINT) | LỖI P3 (`r3-khai-ve-hint-…`) cho điểm 5; còn lại KHÔNG PHẢI LỖI |
| 14 | Bậc hai (A1-b2, A2, A3, A8) | `go_nfkc_p` 4 SỐNG lại + 6 GIẾT, `go_cc_p` 1 + 7, `go_tach` 4 + 2, `go_ra2` 4 + `s_ra_cf` GIẾT (canh T5 `x3_wr5_nfkc` SỐNG lại chỉ trên `var_go_ra2_b` dựng sạch), `go_exc` 3 SỐNG lại + `z_exc_*` 7/7 vẫn GIẾT — tất cả khớp §1.9.8; `go_both`: `z_exc_all`, `z_exc_them_valueerror`, `x_exc_typeerror` SỐNG; `ind2` (không ba ô r2): `z_exc_*` 5/5 GIẾT ⇒ mệnh đề đầu của A8 bậc hai chỉ đúng trên `IMP-R2-GO` | LỖI P3 (`bac-hai-trung-so-hieu-va-khong-co-nhom-chuan`, TÁI PHÁT hẹp) |
| 15 | Đột biến CŨ có còn bán kính 1 với ô mới của r3 | mẫu cách đều 68 trong 204 đột biến cũ nhắm `t52`/`t53`/`t54` (22 + 22 + 24) chạy trên `ind4` bằng `_do_ban_kinh`: 68/68 GIẾT đúng ca đích, bán kính 1, 0 KHÁC; mảnh A5 `k=0/8` trên ứng viên: 59/59 `bán kính 1` (53 đột biến cũ + 6 canh `c698_…`: `m_bodau_bk`, `m_cf_tag_ra`, `s2_hong_va_khong_bq`, `x3_head_emsp_last`, `x46_tab_mh`, `x47_tk_bang_1`) | KHÔNG PHẢI LỖI (mẫu, không phải 416; A5 trọn KHÔNG ĐO ĐƯỢC) |
| 16 | Tỷ lệ vá thật 2→3 (§12) | U = 16 lớp lượt 2; F theo §8.3 = 13 (nghiêm 12) ⇒ 81,25% (75,00%); lớp mới 3; §12 (2) kích hoạt cho ba họ (xem phần TỶ LỆ VÁ THẬT) | — |


## BẢNG ĐO

Mỗi hàng: khẳng định của đặc tả, giá trị đặc tả khai, giá trị tôi đo (lệnh ở NHẬT KÝ ĐO và `evidence/`), khớp hay không. Kiểm SỐ HẠNG, không chỉ quan hệ. Hàng "mẫu"/"phần đã đo" nói thẳng phạm vi.

| khẳng định | đặc tả khai | đo được | khớp? |
|---|---|---|---|
| sha256 SPEC.md (đối tượng review) | 53bf55fe…1b (PROMPT, header) | `sha256sum SPEC.md` = 53bf55fec7ac8553ee8106a615940bb875846ab095e1fcb0544300a2a28dfe1b; `git -C cay-kho rev-parse HEAD` = 276a65f… | có |
| sha256 r2 / r1 trong kho | f69bb398…2c0a / 3a555263…4996 | khớp cả hai (`sha256sum SPEC-r2.md SPEC-r1.md`) | có |
| sha256 VERDICT/HINT lượt 1 và lượt 2 | c825a405…2133 · b3308200…a641 · e281338f…3968 · 83b9df33…e832 | khớp cả bốn | có |
| thân comment `5914438647` | sha256 4a2dba07…684d0, 0 dấu chéo ngược | cùng sha256, `count(chr(92))` = 0; tạo 2026-09-30T15:30:26Z; OWNER | có |
| 9 phụ lục A–I: sha256 khối mã | 9 băm khai ở tiêu đề | 9/9 khớp (tách khối ```python + một LF) | có |
| bản ghép C+H | sha256 37b6e8bd…6e55b | khớp; `liet_ke` = 366 tên (221 + 145); A = 30; A∩ghép = ∅ | có |
| chia tập theo hàm `tap` (C / H / ghép) | 155/41/12/7/6 · 68/40/4/23/5/5 · 223/81/16/30/11/5 | đúng từng số (`tap_dem.py`) | có |
| \|D698\| ở 3.11.15 / 3.12.3 | 19.588 (10.982+8.606; Cf 163; NFKC≠ 4.866) / 19.798 (10.984+8.814; 170; 4.928) | 19588 (10982+8606; 163; 4866) / 19798 (10984+8814; 170; 4928) (+3.13.12: 19803) | có |
| Cf ngoài BMP | 3.11: 120 = 97 TAG + 23; 3.12: 127 = 97 + 30 | 120 = 97+23; 127 = 97+30 | có |
| 27 nhóm `category` trong D698; \|R698∩D698\|=13; \|N698∩D698\|=0; \|T698\|=30 | 27 · 13 · 0 · 30 | 27 · 13 · 0 · 30 (cả ba bản Python) | có |
| S1/S2 (3.11.15) | 666.094 / 121.008 (120.888 chưa M1b) | 666094 / 121008 / 120888 | có |
| S1/S2 (3.12.3) | 673.234 / 122.268 (122.148) | 673234 / 122268 / 122148; cửa con của ứng viên độc lập trả [673234, 122268, [], 0] | có |
| số ô bộ ghi M2b | 456 (3.12) / 452 (3.11) | 456 / 452 (và 457 ở 3.13); cửa `--tu-kiem-gom` của ứng viên trả [456, [], 0] | có |
| \|E698\| và \|B698\| ở 3.12.3 | 118 / 67 | child đo 118 khoá (67 builtins + 51), 0 ô lệch, 0 lớp không dựng được | có |
| miền HINT lượt 2 (lớp con Exception trong builtins, ngoài OSError) | 45 lớp (ExceptionGroup bị loại) | 46 lớp con, 45 dựng được bằng `__new__`; không dựng được: ExceptionGroup | có |
| bảng họ §2 cộng cột | 221·10·211·190·144·16·8·1; hai hàng Z góp 6·0·6·6·6·6·6·0 | đúng từng cột; trừ hai hàng Z ⇒ 205/184/138/10/2 | có |
| 54 canh = 16 + 27 + 11; theo họ A1 25 · A2 15 · A3 9 · A8 5 | 54 = 25+15+9+5 | đếm lại từ bảng §5: 54 tên, 40 `t53_` · 12 `t54_` · 2 `t52_` | có |
| `grep -c` 61 dòng đọc môi trường; hai chỗ đọc thật :7468 :7092; `sys.argv` bốn chỗ | 61; :7468 :7092; :7281 :7610 :8187 :8384 | 61; :7468 :7092; :7281 :7610 :8187 :8384 | có |
| số dòng: `_TRUOC_NANG_LUC` :7422 · `_TEN_NANG_LUC` :7456 · `_doc_che_do` :7461 · `_van_tay` :7495 · `_luoi_che_do` :8040 · `_mong_che_do` :8052 · `_luoi_git` :8069 · `_mong_git` :8080 · `_in_tu_kiem_che_do` :8093 · `t54` :6884 · `_in_tu_kiem_main` :7905 · :2292/:2318 · :2256/:2262 | như trái | `sed -n`/`grep -n` khớp từng dòng | có |
| blob `ops/cong_cu_test.py` ở fc852ff / 423b4ba / 20ec8d5 / 7e5958e | 9edea6b1… (trùng nền) | 9edea6b1629b46f27758b2073e74210dc73495b7 cả bốn | có |
| `git diff --name-only fc852ff 20ec8d5`; `rev-list --count` | đúng 2 tệp; 22 | 2 tệp (`pr684-wp677-land-evidence.yaml`, `ops/lease_publish_test.py`); 22 | có |
| 66 tệp khác nhau giữa 423b4ba và fc852ff | 66 (23/3/39/1) | 66 = ops/land 23 · ops/leases 3 · ops/reviews 39 · ops/specs 1 | có |
| `--full-history` (Q11) hai merge | `7c106a5`, `8e630c0` (cha nhánh blob a2010821…) | `7c106a5f` cha `e8c2388e` + `fc852fff`; `8e630c0a` cha `4dc226bc` + `423b4ba1` | có |
| gate nền `CONG_CU_TEST_BAN_KINH=manh` | 55/55, 416 đột biến, rc=0 (không jsonschema: bỏ qua 1) | `55/55 đạt; tổng=56, bỏ qua=1`, `đột biến=416`, `lỗi đột biến=0`, `cổng cây thật=ĐẠT`, rc=0, 271 s | có |
| ruff F nền (0.15.8) | 1 `F841` ở :2606 | 1 `F841` `ci` ở :2606 | có |
| Phụ lục B đầu ra | sha256 42ca657c…741d | cùng sha256 trên 3.11.15 và 3.12.3 | có |
| `required_checks`: tên job và `timeout-minutes` ở ci.yml@fc852ff | gate gate-ops gate-packet-loop gate-cong-cu-gop (a); gate-cong-cu 0–7, timeout 30 (b); gate-registry (c) | PyYAML: đủ sáu job; gate-cong-cu matrix os×manh 0..7, `timeout-minutes: 30`; gom 10; registry 90 | có |
| `SO_THU_HOI_KICH_HOAT`; trich-log dòng 1962/2438/2440/2590/765/767 | :1093 False; 23–25, 99, 103–104 | :1093 `False` (:1079 'CHƯA KÍCH HOẠT'); đúng các dòng nêu | có |
| S6: 14 dòng 1043–1056 của protocol (blob 0dedc3d9…) | sha256 dc93c2a3… (nối LF) | 14/14 dòng trùng; sha256 nối LF, không LF cuối = dc93c2a34d4a6e64b9ab65285bfb431ad43bdf5b8f73f8a960f4205f311f7715 | có |
| quét bảng Markdown / dòng `137.` | 0 hàng lệch; không còn | 32 bảng, 0 lệch; không dòng nào mở bằng `137.` | có |
| số mười gần chữ vòng/trần/ADR-0048/tran_cu | 1 trần VÒNG + 5 ngưỡng Δ | 6 kết quả = `tran_cu: 10` + 5 ngưỡng Δ (dòng 98, 132, 1352, 1429, 1696) | có |
| ADR-0044 / ADR-0048 | sensitive ≤ 3 tệp ≤ 300 dòng; trần vòng 'mười' một chỗ ở | ADR-0044 dòng 5; ADR-0048 'Con số chỉ có MỘT chỗ ở … tệp này' | có |
| `ba ngưỡng riêng lẻ` của HINT lượt 2 (4 chỗ: §0 điểm 5, §1.9.9, §6 A4-g, §11.1 (C)) | ba ngưỡng (`t53`+8, `t54`+4, và `t52`+4 'như HINT') | HINT.patch lượt 2 và VERDICT lượt 2 chỉ có HAI ngưỡng (`t53` ≤ nền+8 s, `t54` ≤ nền+4 s); tổng 12 s chứ không 16 s | KHÔNG |
| bảng bậc hai §1.8.7 dùng tên canh `f49_*`/`f50_*` | (tên trong bảng) | KHÔNG tên nào có trong Phụ lục A/C/H; tên thật là `e49_*` `x46_*` `e50_*` `x47_*` `x50_*` | KHÔNG |
| hợp đồng con–cha trên ứng viên (`doors.py ind4`) | quet [673234, 122268, [], 0] · 118 khoá E698 · 456 ô bộ ghi · 470 đột biến | quet [673234, 122268, [], 0] · exc [118, [], 0, []] · ghi_ra [456, [], 0] · N 470 | có |
| số dòng thêm của bản thi công (S5, Q12 ≤ 300) | ước 292–307 nếu viết như biến thể đo; 268–283 nếu gọn | ứng viên độc lập `git diff --numstat fc852ff` = 311 / 4 (viết không nén; có thêm khối bắt ngoại lệ bộ ghi và ba ô r2) | gần (ngoài 4 dòng ở cận trên; S5 đã nêu DỪNG-hỏi) |
| A4-a: cổng `CONG_CU_TEST_BAN_KINH=manh` | `M/M đạt`, `lỗi đột biến=0`, `cổng cây thật=ĐẠT`, rc=0; đột biến = 470 (416 + 54) | `ind4`: `55/55 đạt; tổng=56, bỏ qua=1` (thiếu jsonschema), `SỐ LIỆU: ca=56 · đột biến=470 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT`, rc=0, 223 s (nền: `đột biến=416`, rc=0, 271 s lúc máy đang chạy dò khác — thời gian tường không so được) | có |
| A4-b: ruff F (0.15.8) | đúng 1 `F841` ở :2606 (nền); ứng viên cùng đa tập (mã, thông điệp) | nền `:2606 F841 ci`; `ind4` `:2667 F841 ci`; `Found 1 error.` ở cả hai | có |
| A4-c: `ci_dang_ky_test.py` không `--chay` | delta 0; 1025/1025 đỏ đúng | đầu ra nền và ứng viên GIỐNG từng byte (`cmp`), `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT` | có |
| A4-e: Phụ lục E | `sau_moc: []` | {"tong": 10, "truoc_anh": [2256, 2262, 2324], "trong_cua_so": 7, "sau_moc": []} | có |
| A4-d: Phụ lục G trên ứng viên | giao rỗng (rc=0) | `"hunk": 14, "cham": []` rc=0 | có |
| A1 (iv): ký tự nguồn | Cf 0 · U+FF01…U+FF5E 0 · NFKC≠ = {U+2026} | `0 0 ['0x2026']` (giống nền) | có |
| số lần xuất hiện của mỏ neo 54 canh | mỗi mỏ neo xuất hiện ĐÚNG 1 lần trên nền (§5, §6) | nền 54/54 = 1; `ind3` 53/54 (`x3_wr5_nfkc` = 2); `ind4` 54/54 | CÓ trên nền; KHÔNG trên ứng viên ghi bảng bằng literal `repr` |
| Phụ lục F: phản chứng | canh yếu cùng tên ⇒ `lech-bo`; bộ cũ đổi ⇒ `bo-cu`; thiếu dòng ⇒ `tap-ten`; ứng viên ⇒ 0 lỗi | ứng viên `so_loi = 0`; `lech-bo` ✓ (`e49_nfkc_bk`); `tap-ten` ✓ (`c698_x3_wr5_nfkc`); `bo-cu` không chạy lại | có (2/3 phản chứng chạy lại; F không bắt tự va chạm mỏ neo) |
| mảnh A5 `k=0/8` (A5, đúng lệnh) | r2: 497–521 s mỗi mảnh 57–58 đột biến; r3: A5 tám mảnh CHƯA chạy trên `v3_all` | nền 522,9 s CPU 1102,2 s `52/52 đột biến bán kính 1`; ứng viên 669,6 s CPU 1619,6 s `59/59 đột biến bán kính 1` (53 cũ + 6 canh `c698_…`) | có (một mảnh trong tám) |
| mô hình §7: số học | 25,4 · 27,5 · 28,8 · 31,6 phút (18,2 × 470/416 × (29,8 + Δ)/29,8) | 25,42 · 27,46 · 28,84 · 31,60 | có (số học đúng) |
| `t47` khi chạy song song | ra `bo_qua` khi song song, `qua` khi riêng; nguyên nhân KHÔNG ĐO ĐƯỢC | 40/40 `qua` (10 vòng × 4 tiến trình cùng chạy ca); 0 lần ở `khong_qua` trong mọi dòng jsonl; hai lượt gate đầy đủ `bỏ qua=1` (chỉ `t2`) | không tái hiện |
| `shutil.Error` là lớp con của `OSError` | (dò `y_exc_shutil` tương đương) | `issubclass(shutil.Error, OSError)` = True; mro `Error → OSError → Exception` | có |
| áp `HINT.patch` lượt 2 lên r2 (`patch -p0 --fuzz=0`) | rc=0, 17/17 hunk, 1653 → 1708 dòng, 74 thêm / 19 xoá; hunk `objective` làm vỡ bảng ở dòng 14–15 | 17 hunk `succeeded`; 1708 dòng; `git diff --no-index --numstat` = 74 / 19; dòng 14 và 15 của bản đã áp không mở bằng `\|` | có |
| ma trận `os` của `ci.yml` | chỉ thêm `windows-latest` khi `workflow_dispatch` hoặc nhãn `windows`; hậu-merge `36696528580` toàn ubuntu | đúng ở `fc852ff` lẫn `7e5958e` (PR #703): biểu thức `chuan-bi.outputs.os` y hệt; (câu 'master chạy cả ubuntu lẫn windows' trong `CLAUDE.md` lệch `ci.yml`, ngoài phạm vi) | có |
| `bien_nhan_v2.py` dòng 703/720/736–737 | subagent ⇒ từ chối mọi mức độc lập; cùng họ ⇒ từ chối `cross_approved` | dòng 703 `"subagent" in …che_do`; 720 `khai in ASSURANCE_CAN_DOC_LAP and (tu_khai_trong_phien or not co_bang_chung)`; 736–737 `hai bên cùng họ model` | có |
| Phụ lục G: phản chứng | chạm thân `_van_tay` ⇒ rc=1; chèn ngay sau `_van_tay` ⇒ rc=1; chạm `main` ⇒ rc=1; ứng viên ⇒ rc=0 | chèn một dòng trong `_van_tay` ⇒ `cham: [["_van_tay", "@@ -7496,0 …"]]` rc=1; chèn ngay sau dòng cuối ⇒ `@@ -7505,0 …` rc=1; chèn trong `main` ⇒ `cham: [["main", …]]` rc=1; `ind4` ⇒ `cham: []` rc=0 | có |
| số lớp trong bao đóng `BaseException.__subclasses__()` ở tiến trình của Phụ lục I | nạp riêng `v3_all` ⇒ 119; nạp thêm nền ⇒ 122 (cửa con thật: 118) | nạp riêng `ind4` ⇒ 117; nạp thêm nền ⇒ 120 (cửa con thật: 118 khoá); độ tăng +3 khớp, giá trị tuyệt đối lệch 2 theo môi trường (PyYAML hệ thống, không jsonschema) | độ tăng có; số tuyệt đối lệch 2 (môi trường) |
| Phụ lục H (145 dò) trên ứng viên độc lập | KHAI 5 SỐNG; NGOAI 5 SỐNG; T-B 67 GIẾT + 1 KHÁC (`x3_cat_ll_bk`); T-C 38 GIẾT + 1 KHÁC (`x3_wr_ra_lower`) + 1 SỐNG (`x3_wr5_normpath`); T-D 4; T-E 23; `head`: mọi dò GIẾT trừ ba KHAI | có 145/145; KHAI SONG=5 · NGOAI SONG=5 · T-B GIET=67 · T-B KHAC=1 · T-C GIET=38 · T-C KHAC=1 · T-C SONG=1 · T-D GIET=4 · T-E GIET=23; `head` (44): Counter({'GIET': 41, 'SONG': 3}) | có |
| Phụ lục C (221 dò) trên ứng viên độc lập | A1–A3, A8: mọi dò GIẾT trừ đối chứng/tương đương/KHAI (T-B 155 · T-C 41 · T-D 12 · T-E 7 · ngoài lớp 6) | đã đo 221/221; NGOAI SONG=6 · T-B GIET=153 · T-B SONG=2 · T-C GIET=40 · T-C KHAC=1 · T-D GIET=12 · T-E GIET=7; chưa đo 0; không GIẾT: [('T-B', 'SONG', 'm_nfkc_no_bk'), ('T-B', 'SONG', 'm_nfkc_khac_bmp_mh'), ('T-C', 'KHAC', 's_ra_realpath'), ('NGOAI', 'SONG', 'g_nfkc_head'), ('NGOAI', 'SONG', 'g_cf_head'), ('NGOAI', 'SONG', 'g_tab_head'), ('NGOAI', 'SONG', 'g_strip_head'), ('NGOAI', 'SONG', 't_cf'), ('NGOAI', 'SONG', 't_tab')] | có |
| Phụ lục A (30 dò) trên ứng viên | nền: 24 SỐNG + 6 đối chứng GIẾT; sau M1–M5 chỉ còn tám dò F48 SỐNG (nợ Q1) | 30/30; T-B GIET=21 · T-B KHAC=1 · T-B SONG=8; SỐNG = e48_gan_lai_moc, e48_get_self, e48_globals, e48_ham_trong_goi_sau, e48_keys_self_pop, e48_sau_cua_so, e48_truoc_anh, e48_trystar | có |
| Phụ lục A (30 dò) trên NỀN | 24 SỐNG + 6 đối chứng bị giết (5 `giet_that` 1/56 + `c49_ra_abspath` bán kính 2) | 30/30; T-B GIET=5 · T-B KHAC=1 · T-B SONG=24; KHÁC: c49_ra_abspath | có |
| Mẫu Phụ lục H trên NỀN | nền: T-B 62/68 phần H SỐNG (sáu đối chứng GIẾT); T-C 37/40; T-E 28/30 SỐNG | mẫu 24 dò: KHAI SONG=2 · NGOAI SONG=2 · T-B GIET=3 · T-B KHAC=1 · T-B SONG=4 · T-C GIET=2 · T-C KHAC=1 · T-C SONG=4 · T-D GIET=2 · T-D SONG=1 · T-E SONG=2 | mẫu — KHÔNG ĐO ĐƯỢC trọn |
| `tv_exc` (miền HINT): T-E | 7/30 SỐNG | 30 dò đã đo: {'SONG': 7, 'GIET': 23}; SỐNG: x3_exc_bexgroup, x3_exc_exgroup, x3_exc_genexit, x3_exc_json, x3_exc_kbint, x3_exc_re_error, x3_exc_sysexit | có |
| `go_exc` (≈ `cand`, đúng chữ M5 r2): T-E | 22/30 SỐNG | 30 dò đã đo: {'SONG': 22, 'GIET': 8}; SỐNG: x3_exc_bexgroup, x3_exc_exgroup, x3_exc_genexit, x3_exc_json, x3_exc_kbint, x3_exc_menh_de_hai, x3_exc_re_error, x3_exc_stopiter, x3_exc_sysexit, x3_exc_warning, x_exc_assertionerror, x_exc_attributeerror, x_exc_eoferror, x_exc_importerror, x_exc_indexerror, x_exc_keyerror, x_exc_lookuperror, x_exc_memoryerror, x_exc_notimplemented, x_exc_typeerror, x_exc_unicodeencodeerror, x_exc_zerodiv | có |
| `tv_head` (tập `splitlines`): 44 dò `head` | 2 SỐNG (`x3_head_us_last`, `x3_head_emsp_last`) | 44 dò đã đo: {'GIET': 39, 'SONG': 5}; SỐNG: x3_head_emsp_last, x3_head_us_last, x_head_cf2063_at17, x_head_cfk_mid_only, x_head_sm_mid_only | có |
| `tv_list` (danh sách nhóm): dò xoá-nhóm | 4/27 SỐNG (Mc, Me, Pf, Pi) | 27 dò đã đo: {'GIET': 22, 'KHAC': 1, 'SONG': 4}; SỐNG: x_cat_mc_bk, x_cat_me_bk, x_cat_pf_bk, x_cat_pi_bk | có |
| Phụ lục I — P/I_ranh_1 | Δ ≤ 10 s; `lon` ≤ 2 × nền; `v3_all` Δ = 7,04 s, `cand` 4,94 s | Δ = 6.35; `lon` 67/64; `goi` 122471; loi = [] | khớp trong dải |
| Phụ lục I — P/I_ranh_2 | Δ ≤ 10 s; `lon` ≤ 2 × nền; `v3_all` Δ = 7,04 s, `cand` 4,94 s | Δ = 6.45; `lon` 67/64; `goi` 122471; loi = [] | khớp trong dải |
| Phụ lục I — P/I_ranh_3 | Δ ≤ 10 s; `lon` ≤ 2 × nền; `v3_all` Δ = 7,04 s, `cand` 4,94 s | Δ = 5.92; `lon` 67/64; `goi` 122471; loi = [] | khớp trong dải |
| Phụ lục I — P/I_tai_1 | Δ ≤ 10 s; `lon` ≤ 2 × nền; `v3_all` Δ = 7,04 s, `cand` 4,94 s | Δ = 7.03; `lon` 67/64; `goi` 122471; loi = [] | khớp trong dải |
| Phụ lục I — P/I_tai_2 | Δ ≤ 10 s; `lon` ≤ 2 × nền; `v3_all` Δ = 7,04 s, `cand` 4,94 s | Δ = 6.84; `lon` 67/64; `goi` 122471; loi = [] | khớp trong dải |
| Phụ lục I — Q/I_quatai_1 | Δ ≤ 10 s; `lon` ≤ 2 × nền; `v3_all` Δ = 7,04 s, `cand` 4,94 s | Δ = 9.72; `lon` 67/64; `goi` 122471; loi = [] | khớp trong dải |
| Phụ lục I — Q/I_quatai_2 | Δ ≤ 10 s; `lon` ≤ 2 × nền; `v3_all` Δ = 7,04 s, `cand` 4,94 s | Δ = 9.00; `lon` 67/64; `goi` 122471; loi = [] | khớp trong dải |
| Phụ lục I — Q/I_quatai_3 | Δ ≤ 10 s; `lon` ≤ 2 × nền; `v3_all` Δ = 7,04 s, `cand` 4,94 s | Δ = 11.70; `lon` 67/64; `goi` 122471; loi = [['dong_ho', 11.7, 10.0]] | ĐỎ giả (ứng viên đúng) |
| cpu_dem — P/cpu_ranh_1 | (không khai) | Δ tường = 6.77; Δ CPU = 6.35 | — |
| cpu_dem — P/cpu_ranh_2 | (không khai) | Δ tường = 6.72; Δ CPU = 6.24 | — |
| cpu_dem — P/cpu_tai_1 | (không khai) | Δ tường = 7.47; Δ CPU = 6.45 | — |
| cpu_dem — Q/cpu_quatai_1 | (không khai) | Δ tường = 8.61; Δ CPU = 6.29 | — |


## CHI TIẾT TỪNG LỚP

Quy ước: mỗi lớp ghi giả thuyết → lệnh → output → kết luận (ba nhãn LỖI · KHÔNG PHẢI LỖI · KHÔNG ĐO ĐƯỢC). Mọi dò chạy bằng CHÍNH `_do_ban_kinh` + `_ket_luan_ban_kinh` của `ops/cong_cu_test.py` trên cây tạm do `_dung_cay_dot_bien` dựng (đúng đường A5), phân hạng bằng ĐÚNG hàm `hang`/`tap` của Phụ lục D (trích nguyên văn từ SPEC.md). `reviewed_sha` mọi lớp: `276a65f4514034f359ae55c13caa5e0a6d7db1c4`.

### LỚP 1 — `canh-x3-wr5-nfkc-tu-va-cham-mo-neo` — **P2** — MỚI (phép kiểm A5 (vi) của lớp `a5-canh-khong-kiem-bang-do` vẫn thủng)

```
HƯỚNG 10: mỏ neo của 54 canh có thật sự xuất hiện ĐÚNG MỘT lần trong tệp ứng viên không
  giả thuyết : §5 bắt "cùng mỏ neo, cùng phép thay" với dò, ĐĂNG KÝ trong bảng nằm TRONG ops/cong_cu_test.py;
               `_dung_cay_dot_bien` thay `than.replace(tim, thay, 1)` (chỉ lần xuất hiện ĐẦU). Nếu literal của bảng chứa
               nguyên văn mỏ neo thì mỏ neo có mặt HAI lần và đột biến rơi vào literal của bảng, không vào chỗ ghi.
               `repr()` thoát dấu xuống dòng thành `\n` nên mỏ neo nhiều dòng không tự có mặt; mỏ neo MỘT dòng thì có.
  lệnh       : python3.12 count_neo.py nen ind3 ind4      (count của mỗi mỏ neo trong ops/cong_cu_test.py; mỏ neo lấy từ bảng canh)
               python3.12 pl/kiem_canh_r3.py nen <ind3|ind4> bang_noi.txt pl/do_dot_bien.py pl/do_dot_bien_r3.py   (Phụ lục F)
               dò `x3_wr5_nfkc` trên ind3 và ind4 bằng do_dot_bien_r3.py (so_neo, hạng theo Phụ lục D)
  output     : nen : 54 canh | mỏ neo xuất hiện != 1 lần: [] | số canh có mỏ neo không chứa xuống dòng: 1
               ind3: 54 canh | mỏ neo xuất hiện != 1 lần: [('x3_wr5_nfkc', 2)] | số canh có mỏ neo không chứa xuống dòng: 1
               ind4: 54 canh | mỏ neo xuất hiện != 1 lần: [] | ...
               Phụ lục F trên ind3 và ind4: {"nen": 416, "ung_vien": 470, "them": 54, "bang_noi": 54, "so_loi": 0, "loi": []} (cả hai)
               ind3  x3_wr5_nfkc: so_neo=2, hạng KHÁC, khong_qua = t29_ t31_ t32_ t45_ t42_ t39_ t52_ t53_ t54_: tin_dung_gia
               ind4  x3_wr5_nfkc: so_neo=1, hạng GIẾT đúng t52_ (bán kính 1/56)
  kết luận   : LỖI (P2)
```

Cơ chế, đo được chứ không suy: canh `x3_wr5_nfkc` là CANH DUY NHẤT trong 54 mà mỏ neo (`    tep.write_bytes((`) không chứa dấu xuống dòng; ghi nó vào bảng như mọi canh khác thì `repr(tim)` giữ nguyên chuỗi, mỏ neo xuất hiện thêm một lần trong chính literal (dòng 2321 của ứng viên, trước chỗ ghi thật ở dòng 7611). Đột biến thay vào literal của bảng ⇒ tệp tạm lỗi cú pháp (`compile()` trên bản đã thay lần đầu: `SyntaxError: unterminated string literal (detected at line 2321)`; trên `ind4`, mỏ neo chỉ ở dòng 7611, `compile()` được) ⇒ 9 ca chết `tin_dung_gia` (không bởi chốt đích) ⇒ dòng A5 của canh không `ok`. Phụ lục F so BỘ (mỏ neo, phép thay, ca đích) theo giá trị nên `so_loi = 0` ở cả hai cây. Cách ghi literal là quyền của executor (đặc tả chỉ nói "cùng mỏ neo"): ghi mỏ neo nhiều dòng bằng chuỗi ba nháy nguyên văn (cách dễ đọc nhất) thì CẢ 54 canh tự va chạm — không riêng canh này.

Vì sao P2 chứ không P1: lỗi ồn ào (A5 đỏ ở dòng của canh, không im lặng) và chữa bằng một dòng; nhưng phát hiện nó chỉ bằng A5 tám mảnh (hoặc chạy dò ấy), tức đúng một lần CI/đo nặng mà Q7 chỉ cho phép một, và Phụ lục F — bước rẻ sinh ra để canh chuyện này — không bắt.

Phương án (chỉ mô tả; Q14): (a) §5 thêm điều kiện "mỏ neo của mỗi mục xuất hiện đúng một lần trong tệp ứng viên SAU khi bảng đã ghi" và dặn dựng literal của canh có mỏ neo một dòng sao cho chuỗi mỏ neo không xuất hiện nguyên văn ngoài chỗ ghi (nối chuỗi, hoặc escape một ký tự); (b) A5 thêm (vii) `tệp.count(mỏ_neo) == 1` cho cả 54 mục (một lệnh `python3 -c`), ĐỎ khi ≠ 1 — hoặc thêm đúng phép đếm ấy vào Phụ lục F (băm Phụ lục F đổi). Không đổi mỏ neo của dò (băm Phụ lục H bị khoá).

Phép kiểm đóng lớp: `python3.12 count_neo.py <cây ứng viên>` ⇒ `[]`; dò `x3_wr5_nfkc` ⇒ GIẾT `t52_`; phản chứng (đột biến phương án): ghi lại literal thô ⇒ (vii) ĐỎ. Giới hạn: không chạy A5 tám mảnh trọn (chỉ đường `_do_ban_kinh` của từng canh — cùng cơ chế dựng cây của A5).

### LỚP 2 — `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia` — **P2** — MỚI

```
HƯỚNG 3b: ô bộ ghi của M2b làm đúng từng chữ có giết ĐÚNG ca đích bằng chốt của nó không
  giả thuyết : M2b dựng 456 ô, mỗi ô gọi `_ket_thuc_manh(0, n, p, …)` rồi so tập mục dưới thư mục ô với kỳ vọng dựng độc lập.
               Một đột biến chuẩn hoá `ra` bằng NFKC mở rộng khúc tên 50 ký tự (vd `㈀` → `(가)`) vượt NAME_MAX (255 byte);
               nếu ô KHÔNG bắt ngoại lệ do bộ ghi đột biến ném, ngoại lệ thoát khỏi cửa `--tu-kiem-gom` ⇒ con chết,
               `t52` ra `tin_dung_gia` thay vì `giet_that` bằng `TinHieuChotCa` (đúng bài học "giàn giáo hỏng ≠ chốt").
  lệnh       : python3.12 pl/do_dot_bien_r3_full.py ind out/p7/x_wr_ra_nfkc.jsonl x_wr_ra_nfkc     (ind = ứng viên đúng từng chữ, chưa bắt ngoại lệ)
  output     : DICH_DAY_DU x_wr_ra_nfkc ["tin_dung_gia", "giàn giáo hỏng (chưa tới chốt nghiệp vụ): cửa --tu-kiem-gom hỏng: rc=1 …
               File "…/ops/cong_cu_test.py", line 7596, in _ket_thuc_manh: if tep.exists() or tep.is_symlink():
               … OSError: [Errno 36] File name too long: 'k(가)(나)(다)(라)(마)(바)(사)(아)(자)(차)(카)(타)(파)(하)(주)(오전)(오후)(一)…'"]
               Sau khi ô bắt ngoại lệ thành dữ liệu `NEM:<kiểu>` (ind2 trở đi): x_wr_ra_nfkc GIẾT đúng t52_ (bán kính 1/56).
  kết luận   : LỖI (P2)
```

Vì sao P2: đây là đúng câu hỏi gốc của PROMPT — tiêu chí có ĐỎ bằng tín hiệu của đúng ca, không bởi lỗi vô can không. Canh `x_wr_ra_nfkc` (tầng T4, một trong 11 canh r3) và dò cùng tên (T-C) ra `tin_dung_gia` ngay ở lần chạy đầu của executor làm đúng từng chữ; A2 và A5 không thể xanh nếu executor không tự thêm một xử lý ngoại lệ mà chữ M2b không nói (`v3_ra` của phiên soạn r3 hẳn có xử lý ấy mới GIẾT, nhưng nó không được truyền xuống chữ). Executor kỷ luật dừng ở preflight thay vì tự suy (CLAUDE.md, "EXECUTOR TỪ CHỐI Ở PREFLIGHT LÀ TÍNH NĂNG"), tức một vòng revision. Lỗi ồn ào và tự phát hiện được, nên không phải P1.

Phương án (chỉ mô tả; Q14): M2b thêm một câu — ô bộ ghi phải bắt MỌI ngoại lệ do `_ket_thuc_manh` ném (kể cả `OSError` do tên dài sau NFKC) và coi nó là kết quả cần so với kỳ vọng dựng độc lập, không để thoát khỏi cửa `--tu-kiem-gom`. Phép kiểm đóng lớp: dò `x_wr_ra_nfkc` trên ứng viên làm theo câu mới GIẾT `t52_` (bán kính 1/56) thay vì `tin_dung_gia`; ứng viên bỏ xử lý ấy ĐỎ ở A2. Giới hạn: tôi không biết executor thật có tự thêm xử lý hay không; đo chỉ trên ứng viên đúng chữ do tôi dựng.

### LỚP 3 — `t53-thoi-gian-khong-co-tieu-chi-do` — **P3** — VÁ SINH LỖI MỚI (hẹp; lượt 2 P2, slug giữ để nối lịch sử)

Phần ĐÃ ĐÓNG: tiêu chí A4-g CÓ và có răng. Phép ĐẾM tất định (lời gọi `_van_tay` băm `TEP_TEST` > 4096 byte ≤ 2 × nền) không nhiễu: `lon` = 67 (nền 64) ở MỌI lần chạy ứng viên đúng (10/10 lần chạy ở mọi mức tải: `ind3` ×2, `ind4` ×8), `tv_naive` ĐỎ `dem` (122.335 > 128) và `dong_ho` (Δ = 71,1 s); `tv_cham` (ứng viên + `time.sleep(11)`) chỉ ĐỎ `dong_ho` (Δ = 18,96 s, `lon` không đổi) — đúng "hai phép có răng riêng" như §1.9.9. Số `goi`/`lon` của ứng viên độc lập: 122.471 / 67 (Phụ lục I của r3 khai 122.473 / 67 cho `v3_all`).

Phần còn MỞ — hai biểu hiện cùng gốc (ngưỡng tuyệt đối theo giây tường rút từ MỘT máy ở MỘT mức tải):

```
HƯỚNG 11a: phép ĐỒNG HỒ của A4-g có đỏ vì lỗi vô can (tải máy) không
  giả thuyết : Δ = tổng qua t52/t53/t54 của (min ứng viên − min nền), giây tường, ngưỡng cứng 10 s. Cùng một ứng viên đúng chữ thì Δ phải gần như không đổi.
  lệnh       : python3.12 pl/chi_phi_r3.py nen ind4      (Phụ lục I nguyên văn, một lệnh; ind4 = ứng viên độc lập đã sửa mỏ neo)
               python3.12 cpu_dem.py nen ind4              (cùng ba ca, đo cả giây tường lẫn CPU tự thân + con bằng getrusage)
               điều kiện: container 4 lõi dùng chung — một phiên khác (`…/scratchpad/cr710-l1/pwsh`) chiếm ≈ 0,3–1 lõi suốt buổi đo (không phải của tôi, không chạm);
               "hog" = `python3.12 -c "while True: pass"` do tôi sinh rồi `kill` + `wait`
  output     : Δ tường (giây), Phụ lục I:  rảnh (chỉ phiên kia): 5,92 · 6,35 · 6,45 (+ 6,06 ở lần đầu)
                                          2 hog: 6,84 · 7,03
                                          4 tiến trình đo của tôi chạy song song: 7,99 · 8,12
                                          4 hog (quá tải): 9,00 · 9,72 · **11,70 (ĐỎ `dong_ho`, rc=1, ứng viên ĐÚNG chữ)**
                                          1 tiến trình ăn CPU + 4 tiến trình đo: **11,43 (ĐỎ)**
               Δ CPU (cpu_dem.py):         rảnh 6,35 · 6,24 | 2 hog 6,45 | 4 hog 6,29 | (lần cũ khi tải) 6,28   ⇒ dao động ±3% so với tường 5,9–11,7 (×2)
  kết luận   : LỖI (P3): phép đồng hồ đỏ giả ở 2/12 lần chạy, cả hai khi CPU bị chiếm quá tải; Δ CPU không nhiễu.
```

```
HƯỚNG 11b: biên "giữ ≈ 2,5 phút" với trần 30 phút ở Δ = 10 s có giữ không (mô hình §7: 18,2 phút × 470/416 × (29,8 + Δ)/29,8)
  giả thuyết : mô hình trộn T₀ tường (29,8 s, 4 song song, máy nhẹ tải) với Δ đo một tiến trình; đo chính đại lượng mô hình nói tới — thời gian MỘT mảnh A5 — nền so ứng viên.
  lệnh       : CONG_CU_TEST_MANH=0/8 CONG_CU_TEST_MANH_RA=<thư mục ngoài cây>/manh-0.txt python3.12 ops/cong_cu_test.py   (đúng lệnh A5; `shard.py` bọc bằng wait4)
               chạy trên nền (52 đột biến) rồi trên ind4 (59 đột biến), liền nhau, máy có phiên khác như trên
  output     : nen  k=0/8 rc=0 tuong=522,9s cpu=1102,2s  "MẢNH 0/8: 52/52 đột biến bán kính 1"
               ind4 k=0/8 rc=0 tuong=669,6s cpu=1619,6s  "MẢNH 0/8: 59/59 đột biến bán kính 1"
               mỗi đột biến: tường 10,06 → 11,35 s (×1,129); CPU 21,20 → 27,45 s (×1,295); cả mảnh: tường ×1,281, CPU ×1,469
               lõi dùng bình quân của cả mảnh: nền 2,11 · ind4 2,42 (trên 4 lõi, chưa bão hoà) — runner 2 vCPU sẽ bão hoà ⇒ tiến về tỷ lệ CPU
               dự báo mảnh dài nhất CI = 18,2 phút × (470/416) × r, r nội suy theo Δ_A4g (6,24 s đo trên ind4): 
                 cơ sở tường : Δ = 6,24 → 23,2 · Δ = 7,04 → 23,6 · Δ = 10 → 24,8 phút
                 cơ sở CPU   : Δ = 6,24 → 26,6 · Δ = 7,04 → 27,4 · Δ = 10 → 30,3 phút
                 đặc tả      :              Δ = 7,04 → 25,4 · Δ = 10 → 27,5 phút
  kết luận   : KHÔNG ĐO ĐƯỢC trên runner; đo được dải: ước của r3 nằm GIỮA hai cực của dải, nên không sai — nhưng "giữ ≈ 2,5 phút biên" ở Δ = 10 s không chứng minh được: đầu trên của dải chạm trần 30
```

Trả lời thẳng câu hỏi "ước 25,4 phút/mảnh có vượt `timeout-minutes: 30` khi máy CI chậm hơn": 30 phút chịu được CI chậm hơn lượt hậu-merge `36696528580` (nơi có con số 18,2 phút) bao nhiêu — với ứng viên Δ ≈ 6,2–7 s: dải 23,2–27,4 phút ⇒ chịu được 9–29%; với ước của r3 (25,4) ⇒ 18%; với ứng viên đúng ở ngưỡng Δ = 10 s: dải 24,8–30,3 ⇒ từ 21% xuống −1% (có thể đã vượt). Tám mảnh của chính lượt ấy lệch nhau 12,7–18,2 phút (±18% quanh trung điểm), tức biên 9–29% cùng bậc với độ lệch giữa các mảnh. Đây là ƯỚC, KHÔNG ĐO ĐƯỢC trên runner.

Hệ quả: phép đồng hồ cứng 10 s vừa có thể đỏ giả khi máy quá tải (11a) vừa chưa chứng minh được biên 30 phút ở ngưỡng (11b); ứng viên đúng chữ có Δ ≈ 6,2 s cách ngưỡng 38% nên ở máy rảnh qua yên ổn. Vì vậy P3 chứ không P2: lỗi nằm ở độ tin cậy của một phép đo phụ, đã được đặc tả khai là ƯỚC, và phép ĐẾM (cổng chính) đúng.

Phương án (chỉ mô tả; Q14): (i) giữ phép ĐẾM tất định; (ii) phép đồng hồ ghi rõ điều kiện đo (máy không chạy tiến trình CPU khác; ghi `uptime` và tiến trình đầu bảng trước và sau) và đo thêm Δ CPU tự thân + con (`resource.getrusage`), đỏ khi vượt ngưỡng CPU — đại lượng này ổn định ±3% ở mọi tải; (iii) bỏ lời khai "giữ ≈ 2,5 phút biên", thay bằng dải đo ở trên kèm giả định bão hoà CPU của runner và ghi `KHÔNG ĐO ĐƯỢC` trên runner; (iv) nếu muốn biên ≥ 2 phút ở cực CPU thì hạ ngưỡng Δ xuống ≈ 7,5 s (dải khi đó 23,6–28,0 phút, tính bằng cùng phép nội suy). Phép kiểm đóng lớp: chạy Phụ lục I ba lần rảnh và ba lần có 4 hog: kết luận GIỐNG NHAU trên ứng viên đúng; `tv_cham` vẫn ĐỎ.

### LỚP 4 — `ra-ha-nguon-main-bo-ghi-chua-co-o` — **P3** — TÁI PHÁT (hẹp; lượt 2 P2)

Phần ĐÃ ĐÓNG (đo trên ứng viên độc lập, Phụ lục H phần T-C 40 dò): 38 GIẾT đúng `t52`/`t54` bán kính 1/56, 1 KHÁC (`x3_wr_ra_lower`, đối chứng khai trước), 1 SỐNG (`x3_wr5_normpath`, tương đương theo cấu tạo khai trước: `tep.parent.mkdir(parents=True)` đã tạo mọi cha trước khi ghi, nên hệ điều hành giải `x/..` đúng như `normpath`). Phần Phụ lục C của T-C: 41 dò: GIET 40 · KHAC 1 (đối chứng khai trước: `s_ra_realpath` KHÁC bán kính 2). Tầng `main` (T2, T3a, T3b) và bộ ghi T4 GIẾT 8/8 dò THÀNH VIÊN tôi tự thêm, và T5 GIẾT 3/3 đột biến `mkdir` ×2 + `exists` (xem dưới). Phần còn MỞ — cùng cơ chế "`ra`/`tep` ở tầng hạ nguồn không có ô đo" — nằm ở hai chỗ:

```
HƯỚNG 8: chỗ dùng `tep` ở T5 ngoài `write_bytes` có ô đo không
  giả thuyết : hàng T5 của bảng M2b (dòng 1112) liệt kê `exists`/`is_symlink`/`unlink`, `parent.mkdir`, `write_bytes`, dòng in và gán
               "cùng ô bộ ghi của T4"; dò/canh của r3 chỉ có hai phép ở `write_bytes` (`x3_wr5_nfkc`, `x3_wr5_normpath`). Dựng đột biến cho
               các chỗ dùng còn lại (cùng cơ chế: chuẩn hoá đường dẫn trước khi dùng) rồi chạy bằng chính `_do_ban_kinh`.
  lệnh       : python3.12 extra_rv3.py <ind3> <jsonl> y_wr5_mkdir_nfkc y_wr5_mkdir_normpath y_wr5_exists_nfkc y_wr5_unlink_nfkc y_wr5_print_nfkc y_wr5_print_strip
               (mỏ neo: `    tep.parent.mkdir(parents=True, exist_ok=True)` · `    if tep.exists() or tep.is_symlink():` · `        tep.unlink()` · dòng `return dong + [f"MẢNH {k}/{n}: … ghi {tep}"], 0`)
  output     : y_wr5_mkdir_nfkc / y_wr5_mkdir_normpath / y_wr5_exists_nfkc: ok → giết đúng 't52_…' · bán kính 1/56
               y_wr5_unlink_nfkc / y_wr5_print_nfkc / y_wr5_print_strip: ĐỎ … đích 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG' vẫn XANH ⇒ đột biến không giết được gì
  kết luận   : LỖI (P3): 3/6 SỐNG
```

Vì sao SỐNG, đo được: (a) `unlink`: dòng `tep.unlink()` nằm trong `if tep.exists() or tep.is_symlink():`. `t52` của nền có ca "tệp cũ cùng tên" (docstring dòng 6787) nên nhánh này chạy, nhưng với đường ASCII mà NFKC không đổi; mọi ô M2b dựng thư mục ô MỚI nên với đường có ký tự NFKC-đổi, `tep` không tồn tại và nhánh không bao giờ chạy; (b) dòng in `… ghi {tep}`: `t52` so TẬP MỤC dưới thư mục ô, không so dòng in ⇒ chuẩn hoá hiển thị không lộ. Hai chỗ không cùng tầm hậu quả: dòng in chỉ là hiển thị; `unlink` là chỗ gỡ tệp cũ/liên kết tượng trưng trước khi ghi, tức đúng chỗ chuẩn hoá sai sẽ gỡ nhầm hay không gỡ. Cả hai đều nằm trong chữ "mọi chỗ dùng là `tep` (T5)" của §1.9.5 và trong hàng T5; r3 chỉ đo `write_bytes`. Không đo: `normpath`/`expanduser`/bỏ-Cf ở `unlink` (chỉ NFKC và `strip`) — cơ chế giống nên SỐNG tương tự, nhưng KHÔNG ĐO ĐƯỢC.

```
HƯỚNG 9: A2/T-C có răng với việc THIẾU ô thành viên ở tầng hạ nguồn không
  giả thuyết : M2b đòi (iii) một đường chứa mọi điểm mã của `D698 ∪ N698` ở tầng `main` (T2/T3) và các khúc tên tệp phủ `D698 ∪ N698` ở
               bộ ghi (T4); mọi dò T-C của đặc tả là dò PHÉP (NFKC, Cf, TAB, Zs, normpath …), không dò nào là dò THÀNH VIÊN ngoài `R698`.
               Một ứng viên bỏ hai phần ấy (giữ 12 + 48 ô) vẫn qua T-C và A2 ⇒ A2 không đo thứ M2b đòi.
  lệnh       : `ind3_nomem` = `ind3` bỏ đúng hai phần (7 dòng khác nhau, `diff | grep -c '^[<>]'` = 7; công thức số ô tự khớp lại)
               python3.12 pl/do_dot_bien_r3.py <ind3_nomem> … <10 dò T-C: x_main_ra_{cf,nfkc,zs} x_wr_ra_{cf,tab,zs} x3_main_ra_mn x3_wr_ra_cc x3_m3a_ra_cf x3_m3b_ra_nfkc>
               python3.12 extra_rv3.py <ind3|ind3_nomem> … <8 dò thành viên: y_main_ra_{u2063,tag20,fwa} y_wr_ra_{u2063,tag20,fwa} y_m3a_ra_u2063 y_m3b_ra_u2063>
  output     : ind3_nomem: 10/10 dò T-C GIẾT (ứng viên thiếu vẫn qua); 8/8 dò thành viên SỐNG ("vẫn XANH ⇒ đột biến không giết được gì")
               ind3 (đủ ô): 8/8 dò thành viên GIẾT đúng `t54_…` (T2/T3) hoặc `t52_…` (T4), bán kính 1/56
  kết luận   : LỖI (P3): thước không phân biệt ứng viên đủ với ứng viên thiếu một phần M2b đòi (cùng hình dạng lớp `a1-tap-dong-…` của lượt 2)
```

Hạng P3 chứ không P2 vì ứng viên làm ĐÚNG chữ M2b đã GIẾT cả 8 dò (lỗ không tồn tại với executor làm đúng chữ); lỗi nằm ở chỗ tiêu chí không bắt được executor lệch chữ.

Phương án (chỉ mô tả; Q14): (T5) tách hàng T5 của bảng M2b: `write_bytes`, `parent.mkdir`, `exists` — "cùng ô bộ ghi của T4"; `unlink` — thêm ô dựng sẵn một tệp cũ (và trên POSIX một liên kết tượng trưng) tại `tep`, kỳ vọng tệp cũ bị thay; dòng in — thêm so dòng in với `Path(p)`; hoặc, nếu chủ kho không muốn thêm ô, ghi thẳng hai chỗ ấy vào §10 (`chua_do_duoc`) và bỏ chúng khỏi hàng T5. (A2) thêm vào tập T-C các dò thành viên ngoài `R698` cho T2, T3a, T3b, T4 (ví dụ U+2063, TAG SPACE U+E0020, một chữ fullwidth), dẫn xuất từ bảng tầng; không thêm canh (trần thời gian §7). Phép kiểm đóng lớp: ba đột biến T5 GIẾT `t52_…`; tám dò thành viên SỐNG trên `ind3_nomem`, GIẾT trên `ind3` (A2 đỏ ở cây thiếu).

### LỚP 5 — `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` — **P3** — TÁI PHÁT (hẹp; lượt 2 P3)

Phần ĐÃ ĐÓNG: số hiệu A1-b2 và định nghĩa nhóm chốt. Đo bằng các cây gỡ dựng từ ứng viên của tôi, mỗi cây chỉ khác MỘT hàm lọc, và (bài học của chính lượt này) chỉ tin kết quả sau khi `t52 t53 t54` KHÔNG đột biến cho `qua` trên cây gỡ (`base_check.py`; ba cây đầu của tôi hỏng ở chỗ này và đã dựng lại): `go_nfkc_p` (`NFKC(c) ≠ c` trừ Zs/Zl/Zp) 4 SỐNG lại (`e49_nfkc_bk`, `e49_nfkc_mh`, `e49_nfkc_head`, `m_nfkc_ngoai_bmp_mh`) + 6 vẫn GIẾT; `go_cc_p` (`Cc` trừ TAB) 1 SỐNG lại (`m_cc_head`) + 7 GIẾT; `go_tach` (gỡ ô nhiều thẻ M1b) 4 SỐNG lại + 2 vẫn GIẾT; `go_ra2` (gỡ ô tầng `main` và bộ ghi M2b) 4 SỐNG lại + `s_ra_cf` vẫn GIẾT, canh T5 `x3_wr5_nfkc` SỐNG lại chỉ trên cây dựng với mỏ neo đã nối chuỗi (`var_go_ra2_b`; trên cây dựng từ `ind3` nó là KHÁC vì lớp `canh-x3-wr5-…`); `go_exc` (gỡ miền `E698`) ba canh E của r3 SỐNG lại, `z_exc_*` 7/7 vẫn GIẾT — đều khớp §1.9.8.

Phần còn MỞ — một mệnh đề bậc hai KHÔNG tái hiện được trên ứng viên của r3:

```
HƯỚNG 14: mệnh đề đầu của A8 "Bậc hai" — "gỡ riêng ba ô ngoại lệ của r2 ⇒ hai canh E của r2 SỐNG lại (đo trên IMP-R2-GO: 2/2)"
  giả thuyết : ứng viên r3 có HAI nguồn giết `z_exc_*`: ba ô ngoại lệ "giữ từ r2" và miền `E698` (đã chứa ValueError, UnicodeDecodeError, RuntimeError).
               Gỡ riêng nguồn thứ nhất không làm `z_exc_*` SỐNG lại vì nguồn thứ hai vẫn giết; mệnh đề đúng trên `IMP-R2-GO` (r2, không có `E698`)
               nhưng không áp được cho bản giao.
  lệnh       : python3.12 final_tally.py hang  (trên out/ind2 · out/var_go_exc · out/var_go_both)  — ind2 = ứng viên KHÔNG có ba ô r2, CÓ E698;
               var_go_exc = CÓ ba ô r2, KHÔNG E698; var_go_both = không có cả hai
  output     : ind2        : z_exc_all · z_exc_base · z_exc_them_runtime · z_exc_them_unicode · z_exc_them_valueerror → GIET ×5
               var_go_exc  : z_exc_* (7 dò, gồm hai đối chứng thu hẹp) → GIET ×7
               var_go_both : z_exc_all · z_exc_them_valueerror → SONG ×2 (và x_exc_typeerror SONG)
  kết luận   : LỖI (P3): chữ A8 mô tả một phép gỡ mà bản giao không thể thoả; thêm vào đó, §1.9.8 ghi "hai canh E của r2 chết vì ba ô của r2" — đúng chỉ khi miền `E698` đã bị gỡ
```

Phương án (mô tả): sửa mệnh đề thành "gỡ ĐỒNG THỜI ba ô của r2 và miền `E698` ⇒ hai canh E của r2 SỐNG lại; gỡ riêng một trong hai ⇒ vẫn GIẾT" kèm phép đo (`go_both`, `ind2`, `var_go_exc`); và sửa "chết vì ba ô của r2" ở §1.9.8 thành "chết vì ba ô của r2 HOẶC miền `E698`". Phép kiểm đóng lớp: cùng ba cây trên cho đúng GIẾT/GIẾT/SỐNG như trên.

### LỚP 6 — `r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat` — **P3** — MỚI

```
HƯỚNG 13: 11 điểm r3 nói HINT lượt 2 sai — r3 có đúng không; số hạng của các lời khai đi kèm
  giả thuyết : §0 điểm 5 (dòng 129), §1.9.9 (dòng 850–851), §6 A4-g (dòng 1355) và §11.1 (C) (dòng 1697) đều viết
               "ba ngưỡng riêng lẻ" của HINT lượt 2; HINT chỉ đề nghị HAI (`t53` ≤ nền + 8 s, `t54` ≤ nền + 4 s).
  lệnh       : grep -n "ba ngưỡng" SPEC.md ; grep -n -i "ngưỡng" luot2/HINT.patch | cut -c1-200 ; sed -n 61,72p luot2/HINT.patch
               python3 -c "print(18.2*470/416*(29.8+12)/29.8, 18.2*470/416*(29.8+16)/29.8)"       (mô hình §7 của chính r3)
  output     : 4 dòng "ba ngưỡng" (129, 850, 1355, 1697); hunk `t53-thoi-gian…` của HINT: "`t53` không quá nền + 8 s và `t54` không quá nền + 4 s" — HAI;
               28.84 (hai ngưỡng thật, Δ = 8 + 4 = 12 s) · 31.62 (Δ = 16 s, có ngưỡng thứ ba `t52` + 4 s mà HINT KHÔNG đề nghị)
  kết luận   : LỖI (P3): lời phản biện "nếu cùng chạm trần thì vượt trần 30 phút" chỉ đúng khi thêm một ngưỡng chưa từng được đề nghị;
               hai ngưỡng thật cho 28,8 phút, dưới trần theo chính mô hình của r3. Phần còn lại của lập luận (HINT không ràng buộc `t52`;
               đếm lời gọi không phân biệt nhanh/chậm) ĐÚNG và đã đo.
```

Biểu hiện thứ hai (cùng cơ chế "tên/số chép từ nguồn không đối chiếu lại hiện vật"): bảng bậc hai §1.8.7 (dòng 529–546 của SPEC.md) dùng tên canh `f49_nfkc_bk`, `f49_cf_*`, `f49_tab_*`, `f50_bang_2`, `f50_tu_2`, `f50_hong_bang_1`, `f50_tk_bang_1` — KHÔNG tên nào có trong Phụ lục A/C/H; tên thật là `e49_*`, `x46_*`, `e50_*`, `x47_*`, `x50_*` (đo: `grep -c f49_nfkc_bk` = 0 ở r1, 2 ở r2 và r3, cả hai đều ở §1.8.7; `e49_nfkc_bk` có ở Phụ lục). Chữ ấy có từ r2 và lượt 2 không bắt; r3 chép nguyên nên "tên trong ngoặc" của bảng không tra được bằng `grep` vào phụ lục. Phương án (mô tả): đổi "ba" → "hai" và bỏ vế "thêm `t52` + 4 s như HINT đề nghị" ở bốn chỗ; thêm một dòng ánh xạ tên (`f49_nfkc_*` ↔ `e49_nfkc_*`; `f49_cf_*` ↔ `e49_cf_*`; `f49_tab_*` ↔ `x46_tab_*`; `f50_bang_2`/`f50_tu_2` ↔ `e50_bang_2`/`e50_tu_2`; `f50_hong_bang_1`/`f50_tk_bang_1` ↔ `x47_*`; `f50_bang_n_tru_1` ↔ `x50_bang_n_tru_1`) ở đầu bảng §1.8.7. Phép kiểm: `grep -n "ba ngưỡng" SPEC.md` rỗng; mọi tên canh trong §1.8.7 tra được trong một phụ lục.


**Bảng 11 điểm r3 nói HINT lượt 2 sai** (PROMPT §0 điểm 3; đo từng điểm, lệnh ở NHẬT KÝ ĐO):

| # | điểm r3 nói về HINT lượt 2 | đo được | kết luận |
|---|---|---|---|
| 1 | hunk `objective` chèn hai dấu xuống dòng giữa một hàng bảng, làm vỡ bảng | áp `luot2/HINT.patch` lên r2 (`patch -p0 --fuzz=0`): 17/17 hunk, 1653 → 1708 dòng, 74/19; dòng 14 và 15 của bản đã áp KHÔNG mở bằng `\|` | ĐÚNG |
| 2 | miền "45 lớp" để lọt 7/30 dò T-E | `tv_exc` 30 dò: 23 GIẾT + 7 SỐNG (`x3_exc_{bexgroup,exgroup,genexit,json,kbint,re_error,sysexit}`) | ĐÚNG |
| 3 | tập `splitlines` để lọt 2/38 dò `head` | `tv_head` 44 dò `head`: 2 SỐNG đúng tên (`x3_head_us_last`, `x3_head_emsp_last`) + 3 KHAI SỐNG | ĐÚNG |
| 4 | hướng `ra` không tách T3a/T3b, không nói T5, một đường ở bộ ghi không phủ thành viên | lập luận theo cấu tạo; không dựng biến thể theo HINT (r3 cũng không); phần T5 và thành viên có hậu thuẫn gián tiếp ở lớp `ra-ha-nguon-…` | KHÔNG ĐO ĐƯỢC |
| 5 | "ba ngưỡng" đồng hồ riêng lẻ, không ràng buộc `t52`, cùng chạm trần thì vượt 30 phút | HINT có HAI ngưỡng (`t53` + 8 s, `t54` + 4 s); Δ = 12 s ⇒ 28,8 phút < 30 theo mô hình r3; "không ràng buộc `t52`" và "đếm lời gọi không phân biệt" (122.471 cho cả hai) ĐÚNG | ĐÚNG MỘT PHẦN |
| 6 | HINT nói "nạp hai phụ lục rồi so" và "spec đính script như Phụ lục E" nhưng không đính | đọc `luot2/HINT.patch`: không có script nào | ĐÚNG |
| 7 | HINT để định nghĩa nhóm cho handoff | đọc HINT; r3 chốt ở §6 A1; tái hiện 4 + 6 và 1 + 7 | ĐÚNG |
| 8 | HINT diễn đạt lại §12 thay vì chép | hunk S6 của HINT là văn xuôi khác protocol; r3 chép 14/14 dòng (sha256 `dc93c2a3…`) | ĐÚNG |
| 9 | HINT dẫn "dòng 765–767"; thực là mục log thô 765/767 ở dòng 103–104 | `sed -n 102,104p trich-log.txt`: dòng 102 `thu-hoi · run 36688032631`, 103 `765: CHAN [12] …`, 104 `767: ##[error] …` | ĐÚNG |
| 10 | 3.12.3: 127 Cf ngoài BMP = 97 + 30 | `dem_unicode.py`: 127 = 97 TAG + 30 (3.11.15: 120 = 97 + 23) | ĐÚNG |
| 11 | HINT thêm ba cách đọc rồi khai "không còn câu hỏi mở", còn Q5/Q7/Q10/Q11/Q12/Q14 | §11.1 (B) có 14 hàng Q1–Q14; hunk `s11-1` của HINT kết bằng "Ngoài mười một điểm này, không còn câu hỏi mở nào" | ĐÚNG |

## DRY-RUN HINT.patch

`HINT.patch` chỉ sửa VĂN BẢN đặc tả r3 (không có mã `ops/cong_cu_test.py`; Q14), sáu nhóm mở bằng `# lop: <slug>` (`canh-x3-wr5-nfkc-tu-va-cham-mo-neo`, `ra-ha-nguon-main-bo-ghi-chua-co-o`, `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan`, `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia`, `r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat`, `t53-thoi-gian-khong-co-tieu-chi-do`); 40 dòng thêm, 9 dòng xoá; không sửa khối mã nào của Phụ lục A–I (băm các phụ lục không đổi). Mỗi nhóm diff trên BẢN GỐC nên dry-run của từng nhóm độc lập, như `HINT.patch` lượt 2. sha256 = `47a2a4b99e1627293283cfa16d4329cea3ec286f02c2b77cd602af2ab7db6074`.

```
$ T=$(mktemp -d -p "$R") && cp -a "$R/cay-kho" "$T/cay" && cd "$T/cay" && patch -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
checking file ops/specs/ci-g5-cong-cu-va-tiep-r3.md
Using Plan A...
Hunk #1 succeeded at 1205.
Hunk #2 succeeded at 1371.
checking file ops/specs/ci-g5-cong-cu-va-tiep-r3.md
Using Plan A...
Hunk #1 succeeded at 1109.
Hunk #2 succeeded at 1310.
checking file ops/specs/ci-g5-cong-cu-va-tiep-r3.md
Using Plan A...
Hunk #1 succeeded at 789.
Hunk #2 succeeded at 1380.
checking file ops/specs/ci-g5-cong-cu-va-tiep-r3.md
Using Plan A...
Hunk #1 succeeded at 1134.
checking file ops/specs/ci-g5-cong-cu-va-tiep-r3.md
Using Plan A...
Hunk #1 succeeded at 126.
Hunk #2 succeeded at 524.
Hunk #3 succeeded at 851.
Hunk #4 succeeded at 1356.
Hunk #5 succeeded at 1698.
checking file ops/specs/ci-g5-cong-cu-va-tiep-r3.md
Using Plan A...
Hunk #1 succeeded at 1429.
done
rc=0
```
rc = 0: 13 hunk ở 6 nhóm, TẤT CẢ `succeeded` không lệch dòng, không fuzz. Kiểm thêm áp THẬT tuần tự trên bản sao tạm khác (`patch -p0 --fuzz=0`, không `--dry-run`): rc=0, 13 hunk `succeeded` (lệch dòng 9–25 chỉ do áp tuần tự), và tệp kết quả giống từng byte bản cộng dồn do bộ dựng tính (`cmp`). Kiểm cấu trúc bản đã áp: 297 hàng bảng Markdown trước và sau, không hàng nào đổi số dấu `|`. `cay-kho/` không bị sửa (`git status --short` rỗng); các bản sao tạm đã xoá. Chạy lại đúng lệnh của PROMPT lần cuối (sau khi dọn, trên thư mục tạm mới rồi xoá): rc=0, 13 dòng `succeeded`, 0 dòng `FAILED`/`offset`/`fuzz` — nhật ký ở `evidence/ket_qua/dryrun_final.txt`.

## NHẬT KÝ ĐO (ghi tăng dần; lệnh + output thật)


**N1. Phụ lục A–I tách từ `SPEC.md` và băm lại** (`extract_pl.py`: khối ```python sau mỗi tiêu đề + một LF): 9/9 KHỚP băm khai (`3d53b90d…` `6707002f…` `c6a4db8b…` `497d12c9…` `b0772b01…` `1125d6be…` `cd0817d5…` `85073478…` `db512319…`). Ghép C+H bằng đúng lệnh của Phụ lục H ⇒ sha256 `37b6e8bd53e8c14bc634a198aa4fabff7400b662d67b38ab80caf90aeef6e55b` = khai. `liet_ke`: A 30 · C 221 · H 145 · ghép 366; `A ∩ ghép = ∅`; C là tiền tố của ghép. Chia tập bằng hàm `tap` của Phụ lục D: C = 155/41/12/7/6, H = 68/40/4/23/5/5 (KHAI 5), ghép = T-B 223 · T-C 81 · T-D 16 · T-E 30 · ngoài 11 · KHAI 5 — KHỚP §6.

**N2. Số đếm tĩnh, ba bản Python** (`dem_unicode.py`, tính từ thuộc tính Unicode, KHÔNG lấy số từ đặc tả):
```
3.11.15 Unicode 14.0.0: |D698|=19588 (BMP 10982 · ngoài 8606 · Cf 163 · NFKC≠ 4866) · Cf ngoài BMP 120 = 97 TAG + 23 · 27 nhóm · R698∩D698=13 · N698∩D698=0 · |T698|=30 · S1=666094 · S2=121008 (120888 khi chưa có M1b) · ô bộ ghi 452
3.12.3  Unicode 15.0.0: |D698|=19798 (10984 · 8814 · 170 · 4928) · Cf ngoài BMP 127 = 97 + 30 · 27 nhóm · |T698|=30 · S1=673234 · S2=122268 (122148) · ô bộ ghi 456
3.13.12 Unicode 15.1.0: |D698|=19803 · S1=673404 · S2=122298 · ô bộ ghi 457   (đặc tả không khai bản này; CI ghim 3.12)
```
Mọi số đặc tả khai cho 3.11.15 và 3.12.3 KHỚP. Bảng họ ở §2 cộng lại từng cột bằng máy: 221 · 10 · 211 · 190 · 144 · 16 · 8 · 1 KHỚP hàng tổng; hai hàng Z góp 6 · 0 · 6 · 6 · 6 · 6 · 6 · 0 ⇒ 205/184/138 sau khi trừ — KHỚP chữ "ngoài hai hàng Z".

**N3. Neo văn bản** (đo trên `kho.git`): `grep -c` 61 dòng `os.environ|env.get|getenv`; hai chỗ đọc thật :7468 và :7092; `sys.argv` đọc thật ở :7281 :7610 :8187 :8384; `_TRUOC_NANG_LUC` :7422 · `_TEN_NANG_LUC` :7456 · `_doc_che_do` :7461 · `_van_tay` :7495 · `_luoi_che_do` :8040 · `_mong_che_do` :8052 · `_luoi_git` :8069 · `_mong_git` :8080 · `_in_tu_kiem_che_do` :8093 · `t54` :6884 · `_in_tu_kiem_main` :7905 · `_chay_1_ca` :2292 (`return "giet_that"` :2318) · hai chỗ ghi trước ảnh :2256 :2262 — KHỚP. `ops/lease_publish.py:1093` `SO_THU_HOI_KICH_HOAT = False` (và :1079 "CHƯA KÍCH HOẠT"); workflow `ops-thu-hoi-admission.yml` dòng 5–6 "chưa là required check"; `on: pull_request_target types: [opened, reopened, synchronize, ready_for_review, edited]`; `trich-log.txt` 104 dòng, mục 1962/2438/2440 ở dòng 23–25, 2590 ở dòng 99, 765/767 ở dòng 103–104 — KHỚP. `.claude/dev/ci_dang_ky_test.py:730` `TIEN_TO_CHUNG = ("ops/cai_", "ops/cong_cu")`. ADR-0048 (Accepted 2026-09-12) "mười vòng", "chỗ ở duy nhất của con số trục VÒNG là tệp này". ADR-0044: sensitive ≤ 3 tệp, ≤ 300 dòng thêm.

**N4. Đoạn S6 chép từ protocol**: 14 dòng 1043–1056 của `docs/PROTOCOL_DA_PHIEN.md` ở `fc852ff` (blob `0dedc3d9…`, cùng blob ở `20ec8d5` và `7e5958e`) so từng dòng với khối trích trong §8 S6: 14/14 trùng; sha256 của 14 dòng nối LF (không LF cuối) = `dc93c2a34d4a6e64b9ab65285bfb431ad43bdf5b8f73f8a960f4205f311f7715` = khai.

**N5. Quét máy trên SPEC.md** (bản độc lập, cùng luật chữ): 32 bảng Markdown đều số `|` ở mọi hàng (0 lệch); không dòng nào mở bằng `137.`; số mười đứng riêng gần chữ vòng/trần/ADR-0048/tran_cu: đúng 6 kết quả = 1 `tran_cu: 10` + 5 ngưỡng Δ (≤ 10 s) — KHỚP lời khai §1.9.10.

**N6. `required_checks` so với `ci.yml`@`fc852ff`** (PyYAML): job `gate` `gate-cong-cu` (matrix os × manh 0–7, `timeout-minutes: 30`) `gate-cong-cu-gop` (10 phút, `if: !cancelled()`) `gate-ops` `gate-registry` (90) `gate-packet-loop` — khớp tên context đặc tả nêu. Lưu ý nền tiếp nối: giữa `fc852ff` và `7e5958e` (PR #703 `ci-duong-nhanh-ho-so`) `ci.yml` đổi +94/−4 (thêm bước phân loại `duong_nhanh` ở `chuan-bi`, `gate`, `gate-ops`; **KHÔNG** chạm `gate-cong-cu`), và `ops/cong_cu_test.py` KHÔNG đổi (blob `9edea6b1…`).

**N7. Ứng viên độc lập `ind4` — dựng và A4 tĩnh** (dựng CHỈ từ chữ §5 M1–M5b + bảng 54 canh; không dùng `v3_*`/`cand`/`tv_*`; mã dựng nằm trong sandbox, KHÔNG giao — Q14):
```
$ git -C ind4 diff --numstat fc852ff -- ops/cong_cu_test.py      -> 311  4  ops/cong_cu_test.py          (đặc tả ước 292–307 nếu viết như biến thể đo; 268–283 nếu gọn)
$ git -C ind4 diff --name-only fc852ff                            -> ops/cong_cu_test.py
$ ruff --version ; ruff check --select F ops/cong_cu_test.py      -> ruff 0.15.8 ; nền ":2606 F841 `ci`" · ind4 ":2667 F841 `ci`" · "Found 1 error." ở cả hai
$ cmp out/cidk_nen.txt out/cidk_ind.txt                           -> trùng; "PHẢN CHỨNG: 1025/1025 đỏ đúng · TỔNG: ĐẠT"          (A4-c)
$ python3.12 pl/ast_dot_bien_r2.py ind4/ops/cong_cu_test.py       -> {"_TRUOC_NANG_LUC": 7502, "_TEN_NANG_LUC": 7536, "tong": 10, "truoc_anh": [2256, 2262, 2324], "trong_cua_so": 7, "sau_moc": []}   (A4-e)
$ python3.12 pl/giao_a4d_r3.py ind4 fc852fff…                     -> {"khoang": {…sáu hàm…}, "hunk": 14, "cham": []} rc=0          (A4-d)
$ python3.12 -c '<lệnh A1 (iv)>' ind4/ops/cong_cu_test.py         -> 0 0 ['0x2026']  (giống nền)
$ CONG_CU_TEST_BAN_KINH=manh python3.12 ops/cong_cu_test.py       -> "cong_cu_test: 55/55 đạt; tổng=56, bỏ qua=1" (t2: thiếu jsonschema) · "SỐ LIỆU: ca=56 · đột biến=470 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT" rc=0, 223 s trên `ind4`   (A4-a; nền: đột biến=416, rc=0)
```
**N8. Hợp đồng con–cha trên `ind4`** (`python3.12 doors.py ind4`): `quet [S1, S2, lệch, không] = [673234, 122268, [], 0]` (đúng S1/S2 của đặc tả cho 3.12.3) · `exc = [118 khoá, [], 0, []]` · `ghi_ra = [456, [], 0]` (456 ô bộ ghi) · `N = 470`.

**N9. Số mỏ neo xuất hiện** (`python3.12 count_neo.py nen ind3 ind4`, mỏ neo lấy từ bộ của dò cùng tên): nền 54/54 = 1 · `ind3` `[('x3_wr5_nfkc', 2)]` (dòng 2321 và 7611) · `ind4` 54/54 = 1; số canh có mỏ neo KHÔNG chứa xuống dòng: 1 (ở cả ba). `compile()` trên `ind3` đã thay lần xuất hiện đầu: `SyntaxError: unterminated string literal (detected at line 2321)`; trên `ind4`: biên dịch được.

**N10. Phụ lục F** (`python3.12 pl/kiem_canh_r3.py nen <cây> bang_noi.txt pl/do_dot_bien.py pl/do_dot_bien_r3.py`): `ind3`, `ind4` → `{"nen": 416, "ung_vien": 470, "them": 54, "bang_noi": 54, "so_loi": 0, "loi": []}`; canh cùng tên phép thay yếu hơn (`NFKC`→`NFKD` ở `c698_e49_nfkc_bk`) → `"so_loi": 1, "loi": [["lech-bo", "e49_nfkc_bk", "c698_e49_nfkc_bk"]]`; bảng nối thiếu một dòng → `[["tap-ten", ["c698_x3_wr5_nfkc"]]]`. (Phản chứng `bo-cu` không chạy lại: KHÔNG ĐO ĐƯỢC ở lượt này.)

**N11. A4-g — Phụ lục I và CPU** (`python3.12 pl/chi_phi_r3.py nen ind4`, `python3.12 cpu_dem.py nen ind4`; số liệu đầy đủ ở lớp `t53-thoi-gian-khong-co-tieu-chi-do`): Δ tường 5,92–6,45 s (rảnh) … 9,0–11,7 s (4 hog); Δ CPU 6,24–6,45 s ở mọi tải; `lon` 67/64 ở 10/10 lần; `goi` 122.471.

**N12. Một mảnh A5 thật** (`shard.py` bọc `CONG_CU_TEST_MANH=0/8 python3.12 ops/cong_cu_test.py` bằng `getrusage`): nền `rc=0 tuong=522.9s cpu=1102.2s "MẢNH 0/8: 52/52 đột biến bán kính 1"`; `ind4` `rc=0 tuong=669.6s cpu=1619.6s "MẢNH 0/8: 59/59 đột biến bán kính 1"`.

**N13. `t47` song song** (`python3.12 t47_par.py ind4 10`: 10 vòng × 4 tiến trình cùng chạy ca `t47`): `{'qua': 40}`; kèm 0 lần `t47_` trong `khong_qua` của mọi dòng jsonl (xem BẢNG SĂN hàng 12).

**N14. Máy dùng chung — điều kiện đo:** `nproc` = 4. Ngoài tiến trình của tôi, một phiên khác (`…/scratchpad/cr710-l1/pwsh/…`, `pwsh`) chiếm ≈ 0,3–1 lõi trong suốt buổi đo; tôi KHÔNG chạm vào nó. Các `uptime` trước/sau từng khối đo nằm trong `phaseP.log`/`phaseQ.log` (xem thư mục `evidence/`). Mọi phép đo thời gian tường vì thế KHÔNG phải "máy rảnh" tuyệt đối; con số CPU không chịu ảnh hưởng này.


## SANDBOX, DỌN DẸP

**Phạm vi ghi.** Chỉ ghi dưới `$R/goi/` và các thư mục `mktemp -d -p "$R"` (TMPDIR trong `$R`). Không mạng, không GitHub, không commit/push. `$R/cay-kho` KHÔNG bị sửa: `git -C cay-kho status --short` → rỗng; `git -C cay-kho rev-parse HEAD` → `276a65f4514034f359ae55c13caa5e0a6d7db1c4`; `cmp SPEC.md cay-kho/ops/specs/ci-g5-cong-cu-va-tiep-r3.md` → trùng; `sha256sum SPEC.md` → `53bf55fe…dfe1b`; `sha256sum PROMPT.md` → `4d29044c…5e68` (khớp lời khai của điều phối).

**Mã dựng ứng viên KHÔNG giao** (Q14). Bốn đời ứng viên độc lập (`ind` đúng từng chữ → `ind2` → `ind3` → `ind4`), các cây biến thể gỡ chốt (`var_*`) và mã dựng chúng nằm ở thư mục làm việc tạm; thư mục ấy bị xoá cuối lượt (xem "SAU DỌN" bên dưới). `evidence/` chỉ giữ: (a) `phu_luc_trich_tu_SPEC/` — chín khối mã Phụ lục A–I trích NGUYÊN VĂN từ `SPEC.md` (băm khớp lời khai; mỗi khối ở hai tên: `pl_X.py` và tên tệp mà đặc tả dùng để gọi nó) cộng `do_dot_bien_r3.py` = ghép C+H đúng lệnh Phụ lục H (sha256 `37b6e8bd…e55b`); (b) `scripts/` — công cụ ĐO của tôi (bộ chạy dò có hàng đợi và `wait4`, bộ đếm mỏ neo/cửa/CPU/mảnh, bộ ráp bảng và bộ dựng HINT; KHÔNG có mã triển khai M1–M5b); (c) `du_lieu/` — dữ liệu vào (54 canh, bảng nối, danh sách dò); (d) `ket_qua/` — kết quả thô (mỗi dò một dòng jsonl, nhật ký từng pha, đầu ra cổng trên nền và trên ứng viên). Không tệp nào trong `evidence/` là bản vá cho `ops/cong_cu_test.py`.

**Quét bí mật** trên toàn `goi/` (mẫu `ghp_`/`github_pat_`/`AWS_`/`CODEX_AUTH`/`Bearer`… và đối chiếu từng giá trị biến môi trường dài ≥ 24 ký tự có tên chứa `KEY|TOKEN|SECRET|PAT|AUTH|PASS`, KHÔNG in giá trị): 0 bí mật. Một khớp duy nhất là biến `CLAUDE_CODE_EXECPATH` (khớp vì tên chứa `PAT`; giá trị chỉ là đường dẫn tệp thực thi `/opt/claude-code/bin/claude`, xuất hiện trong `ket_qua/P/phaseP.log` ở cột "top CPU ngoài tôi"). Không có chuỗi `skip` + `ci` nguyên văn nào trong `goi/` (`grep -rIn` rỗng).

**Máy dùng chung.** `nproc` = 4; đĩa còn ≈ 15 GB lúc bắt đầu dọn; tối đa 4 tiến trình đo của tôi chạy song song (hàng đợi `drive2.py`; CPU từng tiến trình do `wait4` ghi lại); mọi tiến trình con đều được `wait`; chỉ giết tiến trình do chính tôi sinh (PID lấy từ `ps -eo pid,args | awk`, không dùng `pkill -f`). Lúc kết thúc, `ps` chỉ còn một tiến trình `python3.12` của phiên khác (`…/cr678-r12/goi/do/quet_s_ast.py`) — không phải của tôi, không chạm. `$R/tmp.n6UxdzSoEY` và `$R/tmp.n6uxdzsoey` (dấu vết lượt trước, KHÔNG phải của tôi) giữ nguyên.

**SAU DỌN (đo cuối lượt, sau khi `evidence/` đã chép xong).**
```
$ python3.12 (shutil.rmtree, từng đường dẫn kiểm: nằm TRỰC TIẾP dưới $R, tên bắt đầu `tmp`, KHÔNG phải hai thư mục lượt trước)
  xoá 8 thư mục của tôi: 3 thư mục dry-run HINT (T_dry.txt) · 1 thư mục probe (T_probe.txt) · thư mục dò tạm `tmp.XYbsGISiY3` · bản song sinh chữ thường `tmp.f0cqoiqaeu` (do đột biến đổi chữ thường đường dẫn tạo ra) · `tmp_rv` (rỗng) · thư mục làm việc `tmp.f0cQOIqaeu`  -> cả tám "mất"
$ ls $R                                   -> PROMPT.md SPEC-r1.md SPEC-r2.md SPEC.md cay-kho goi kho.git luot1 luot2 r2-r3.diff r3do readback-*.json tmp.n6UxdzSoEY tmp.n6uxdzsoey
$ git -C cay-kho status --short | wc -l   -> 0
$ ps -eo stat | grep -c '^Z'              -> 0 (không zombie); không còn tiến trình `python3.12` nào của tôi
$ find goi -type f | wc -l ; du -sh goi   -> 1644 tệp ; 4.4M   (HINT.patch, VERDICT.md, evidence/)
$ df -h $R                                -> còn 16 GB (trước dọn 15 GB)
```
