verdict: changes_requested
reviewed_sha: 42cd314ca070e8e542fbd291b398690c2e5e54fd
spec_sha256: b51b5ffa40dd70086df4785a532b7c356c18244421f55d5eb2157eb8406a95e0
model/effort tự khai: Claude Sonnet 5.5 (`claude-sonnet-5-5`), effort "max" theo chỉ thị điều phối; chạy bằng SUBAGENT (không phải codex). Effort thực đo từ bên trong: KHÔNG ĐO ĐƯỢC.
nhãn assurance của lượt này: `review_deferred` (subagent ⇒ `ops/bien_nhan_v2.py` từ chối mọi mức trong `ASSURANCE_CAN_DOC_LAP`; cùng họ Claude với executor ⇒ từ chối `cross_approved`) — đặc tả khai đúng điều này.
tổng kết: **0 P1 · 0 P2 · 4 P3 = 4 lớp / 5 biểu hiện** — `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia` (CÒN MỞ hẹp, hạ P2→P3) · `a5-bang-noi-khong-ghim-tap-54-do` (MỚI) · `r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat` (TÁI PHÁT hẹp) · `muc-tieu-moi-duong-vao-co-canh-mau-thuan-no-j` (MỚI).
tỷ lệ vá thật 3→4: **4/6 = 66,67 %** (đọc nghiêm 3/6 = 50,00 %); lớp mới 2; lớp tái mở 0 (xem ĐỐI CHIẾU).
`HINT.patch`: sha256 `e4df532df8da8f73402f0254dfc4dd7d79d746ae265d99ee4c20eda265d062cf`; `patch -p0 --fuzz=0 --dry-run --verbose` ⇒ **rc=0**, 8/8 hunk (xem DRY-RUN).
câu hỏi riêng của PROMPT: `ops/cong_cu_test.py` **KHÔNG đổi** giữa `fc852ff` và master `ab457c6` (blob `9edea6b1629b46f27758b2073e74210dc73495b7` ở cả hai; `git diff --quiet` rc=0).
câu hỏi gốc: làm đúng từng chữ r4 thì các lỗ đo F49 / F49-P3 / F50 **ĐÓNG** trên ứng viên độc lập của tôi (Phụ lục F rc=0; 35 dò J và 54 canh GIẾT bán kính 1; tập đóng 401 đúng khai; 232/232 mục cũ không bị ô mới làm chết ở cửa khác;
A4-a…f xanh; mảnh A5 0/8 = 59/59); phần còn lại là bốn lớp P3 nằm ở TẦNG ĐO và LỜI KHAI của chính r4, không ở mã.

## TIỀN KIỂM (làm trước mọi việc khác)

```
$ sha256sum SPEC.md SPEC-r3.md SPEC-r2.md SPEC-r1.md
b51b5ffa40dd70086df4785a532b7c356c18244421f55d5eb2157eb8406a95e0  SPEC.md      (= spec_sha256 của PROMPT: KHỚP)
53bf55fec7ac8553ee8106a615940bb875846ab095e1fcb0544300a2a28dfe1b  SPEC-r3.md   (KHỚP)
f69bb398441168830443d4e095be18247fc4029c930fce8793cfb6574a652c0a  SPEC-r2.md   (KHỚP)
3a55526305e17cf06c644e2e3448cb8720aa67e8d6c0cab571d8e49dac974996  SPEC-r1.md   (KHỚP)
$ git -C cay-kho rev-parse HEAD     -> 42cd314ca070e8e542fbd291b398690c2e5e54fd   (KHỚP reviewed_sha)
$ git hash-object cay-kho/ops/cong_cu_test.py ; git rev-parse fc852ff:ops/cong_cu_test.py
9edea6b1629b46f27758b2073e74210dc73495b7  (cả hai; blob nền)
$ git -C kho.git rev-parse master-ab457c6:ops/cong_cu_test.py ; git -C kho.git diff --quiet fc852ff master-ab457c6 -- ops/cong_cu_test.py ; echo rc=$?
9edea6b1629b46f27758b2073e74210dc73495b7 ; rc=0       => `ops/cong_cu_test.py` KHÔNG đổi giữa nền fc852ff và master hiện tại (ab457c6, merge PR #712)
```
Tiền kiểm KHỚP, không dừng. Master `ab457c6` KHÁC nền ở 217 tệp (hồ sơ + vài tệp khác); trong số các tệp mà packet đọc: `.github/workflows/ci.yml` (+94 dòng: đường nhanh hồ sơ, packet #674; `gate-cong-cu` vẫn `timeout-minutes: 30`, ma trận 8 mảnh, `gate-cong-cu-gop` 10 — đo bằng PyYAML ở cả hai ref), `ops/lease_publish_test.py` (+1544), `docs/PROTOCOL_DA_PHIEN.md` (+54/−10; 14 dòng trích ở S6 giữ nguyên chữ nhưng dời từ dòng 1043 sang 1087). Cả 416 mục `DOT_BIEN` cũ có số lần mỏ neo GIỐNG HỆT ở hai ref (đo, 0 lệch). Không điểm nào trong số này đổi một câu của đặc tả.

## GIỚI HẠN KHAI THẲNG (đọc trước khi tin bất kỳ con số nào dưới đây)

1. **Ứng viên là của TÔI, không phải của executor.** Tôi dựng một ứng viên ĐỘC LẬP theo đúng chữ r4 trên bản sao nền `fc852ff`
   (không dùng cây `v4_*`/`tv_*` của phiên soạn; không dùng `r4do/cong_cu/dung_v4.py`): `+287/-4` dòng
   (`git -C trees/c_all diff --numstat fc852ff -- ops/cong_cu_test.py` ⇒ `287  4  ops/cong_cu_test.py`), sha256 tệp
   `39599c2f706ada39605579999e00ef8d3feefd8b97fa3d5e239082277f059432`, `DOT_BIEN` 470 mục, `CA` 56. Mọi câu "làm đúng chữ r4 thì …" dưới đây là
   câu về MỘT cách đọc chữ r4, không phải về bản giao. Theo Q14 và chỉ thị điều phối, **mã dựng ứng viên KHÔNG được công bố**
   (`evidence/` chỉ có công cụ ĐO, dò, kết quả thô, và bản sinh `HINT.patch` chỉ sửa văn bản).
2. **Không mạng, không GitHub.** Mọi dữ kiện GitHub lấy từ tệp đọc-ngược có sẵn (`readback-*.json`, `r4do/kq/issue698_comments.json`) và từ `kho.git`
   (mirror). Trạng thái GitHub LIVE (comment mới, PR, CI hiện tại): **KHÔNG ĐO ĐƯỢC**.
3. **Runner CI, số vCPU, Windows: KHÔNG ĐO ĐƯỢC** (không có runner; Q8 cấm Windows). Mọi kết luận về biên 27,9/30 phút là kết luận theo MÔ HÌNH của §7.
4. **Máy đo dùng chung**: 4 lõi, loadavg 3,9–19,6 trong lúc đo (ghi ở từng phép đo; `/proc/loadavg` trong `out/I/*.json` mục `dong_ho.loadavg`); còn một reviewer khác chạy song song. Số GIÂY là nhiễu;
   số CPU và hạng GIẾT/SỐNG/KHÁC là thứ tôi dựa vào.
5. **Phiên bản công cụ**: Python 3.12.3 (đúng bản CI ghim) cho mọi phép đo hạng; 3.11.15 và 3.13.12 chỉ để đo số học Unicode. PyYAML 6.0.1 (CI ghim 6.0.3). `jsonschema` VẮNG ⇒ `t2` bị bỏ qua
   (`bỏ qua=1`, như lượt đo r1). ruff 0.15.8 (bản ghim 0.15.15 vắng ⇒ A4-b chỉ đo bằng 0.15.8 — **KHÔNG ĐO ĐƯỢC** với 0.15.15).
6. **A5 tám mảnh trọn: KHÔNG chạy — chỉ một mảnh (0/8)** (một mảnh ≈ 30 phút CPU, 13 phút tường với 3 tiến trình; tám mảnh là nhiều giờ trên máy chung). Bảy mảnh còn lại (411 mục) không chạy ở bán kính đầy đủ. Thay vào đó tôi đo:
   (a) 54 canh và 2 đối chứng ở chế độ ĐẦY ĐỦ (`_do_ban_kinh` trên 56 ca; bán kính thật); (b) 35 dò J ở chế độ đầy đủ; (c) mọi dò còn lại của tập đóng 401 và 30 dò Phụ lục A ở chế độ NHANH (chỉ ca đích);
   (d) bán kính của 232 mục CŨ có tệp đích `ops/cong_cu_test.py` trên ba cửa `t52/t53/t54` — nơi duy nhất có ô mới; (e) mảnh A5 `0/8` TRỌN trên ứng viên, đúng lệnh A5 (`CONG_CU_TEST_MANH=0/8`, tệp mảnh ngoài cây, 3 tiến trình): rc=0, `cong_cu_test: 55/55 đạt`, `MẢNH 0/8: 59/59 đột biến bán kính 1`, 772,4 s tường, 1789,4 s CPU (30,33 s CPU mỗi đột biến; phiên soạn đo `v4_all` 30,57 s) — 59/59 dòng `ok … bán kính 1/56`, trong đó 6 canh và 53 mục cũ.
   Phần còn lại của 470 mục — 184 mục cũ có tệp đích khác (`ops/bash_nen.py` 161, `ops/cong_cu.py` 19, …) và 53 ca không phải cửa chạy trên 204 mục cũ của tệp test — **KHÔNG ĐO ĐƯỢC** ở bán kính đầy đủ; lý do tin chúng không đổi: ô mới nằm ở ba cửa, không gọi mã của chúng.
7. **Ca "có MẶT" khác ca "có ĐO"**: ở `CLAUDE.md` có bài học về ca `return` sớm. Ở phần đo bán kính tôi chỉ kết luận khi `giay` > 0 và có dòng kết quả cho từng ca đã chạy (xem `evidence/results/r_c_all.jsonl`, trường `giay`).
8. Tôi không in biến môi trường; mọi lệnh dưới đây không đọc bí mật.

## ĐỐI CHIẾU LƯỢT TRƯỚC (protocol §8/§8.3) — làm TRƯỚC mọi hướng săn mới

Nguồn lượt 3: `luot3/VERDICT.md` (`sha256sum` ⇒ `d3d848edec273353371bc714d06f9d9e1c0080c829a3285352732007dee4b955`), `luot3/HINT.patch`
(`47a2a4b99e1627293283cfa16d4329cea3ec286f02c2b77cd602af2ab7db6074`; áp lên `SPEC-r3.md`: rc=0, 13/13 hunk, 2668→2699 dòng, +40/−9 — khớp §0 r4 dòng 94) [L202].
`reviewed_sha` lượt 3 = `276a65f`; lượt này `42cd314`. Sáu lớp lượt 3: 2 P2 + 4 P3. Bốn nhãn của §8: ĐÃ ĐÓNG · CÒN MỞ · VÁ SINH LỖI MỚI · TÁI PHÁT.

Cách đối chiếu (CLAUDE.md: test HÀNH VI hai chiều, không grep chuỗi): (i) dựng ứng viên độc lập `c_all` theo chữ r4 rồi chạy các phụ lục NGUYÊN VĂN của r4 trên nó
(băm 10/10 phụ lục KHỚP, [L75]); (ii) bơm phản chứng vào BẢN CỦA r4: bốn biến thể mỏ neo, ba biến thể A4-g, các cây gỡ M6/T5/J-TV/A8; (iii) dò thêm NGOÀI tập đóng (`y4_*`, 11 dò; hai bảng nối đổi tên).

| # | slug lớp lượt 3 | hạng L3 | nhãn lượt 4 | bằng chứng chính |
|---|---|---|---|---|
| 1 | `canh-x3-wr5-nfkc-tu-va-cham-mo-neo` | P2 | **ĐÃ ĐÓNG** | Phụ lục F r4 trên 4 cây: `c_all` rc=0 (0/470 lệch) · `c_lit` rc=1 (1) · `c_tq` rc=1 (55) · `c_cu` rc=1 (1); `x3_wr5_nfkc` GIẾT `t52_…` bán kính 1/56 ở chế độ đầy đủ [L178, L181, L187, Đ05, Đ07] |
| 2 | `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia` | P2 | **CÒN MỞ (hẹp)** | biểu hiện gốc ĐÃ ĐÓNG (`x_wr_ra_nfkc` GIẾT 1/56; J-NEM 11/11 GIẾT). Còn: chỗ gọi THỨ SÁU (`y4_luoi_git_*` 3/3 KHÁC) và răng thiếu (bản bắt `(Exception, SystemExit)` qua J-NEM 11/11; 8 dò `y4_*_kbint/genexit` KHÁC) [L456, L471, L489] |
| 3 | `t53-thoi-gian-khong-co-tieu-chi-do` | P3 | **ĐÃ ĐÓNG** (phạm vi đo được; runner KHÔNG ĐO ĐƯỢC, đã khai) | 6 lượt `c_all`: r = 1,2700–1,3063, mảnh ước 26,27–27,02 phút, rc=0; `tv_cpu` ĐỎ chỉ `cpu` (r 1,4174); `tv_naive` ĐỎ `dem`+`cpu` (r 3,9584); `tv_cham` rc=0 (đã khai ở §10) [Đ10] |
| 4 | `ra-ha-nguon-main-bo-ghi-chua-co-o` | P3 | **ĐÃ ĐÓNG** | J-T5 10/10, J-TV 15/15, J-NEM 11/11 GIẾT (đầy đủ, bán kính 1); răng: `v4_t5_r3` 6 SỐNG, `go_hai` 3, `go_in` 3, `nomem` 15/15 SỐNG; T-C 115: 113 GIẾT + 1 tương đương (`x3_wr5_normpath`) + 1 đối chứng KHÁC (`x3_wr_ra_lower`); 28 dò `y_*` của lượt 3: **27 GIẾT + 1 SỐNG** (`y_exc_shutil`, tương đương đã khai: `issubclass(shutil.Error, OSError)` ⇒ `True`) [Đ06, Đ08, Đ09, Đ14] |
| 5 | `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` | P3 | **ĐÃ ĐÓNG** (phần A8 mới viết; A1-b2/A2/A3 giữ chữ r3, KHÔNG đo lại) | A8 trên ba cây gỡ: gỡ riêng `E698` ⇒ 3 canh E r3 SỐNG, 2 canh r2 GIẾT; gỡ riêng ba ô r2 ⇒ cả 5 canh GIẾT; gỡ cả hai ⇒ cả 5 SỐNG + 2 đối chứng GIẾT [L471] |
| 6 | `r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat` | P3 | **TÁI PHÁT (hẹp)** — biểu hiện mới, cùng cơ chế | "ba ngưỡng" 4→0 chỗ, bảng ánh xạ `f49_*`/`f50_*` có; NHƯNG nhãn "24 canh r2" (3 chỗ) sai so với §5: 24 = 9 canh r1 + 15 canh r2 [L205, L211, L214, L504] |

Ghi chú đếm: "J-NEM 11" trong báo cáo này = 10 dò của nhóm J-NEM trong Phụ lục J (`x4_t1_thoat_ra`, `x4_head_thoat`, `x4_t2_thoat_ra`, `x4_t2_resolve_ra`, `x4_t3a_thoat_ra`, `x4_t3b_thoat_ra`, `x4_t4_thoat_ra`, `x4_t4_bytes_ra`, `x4_t4_nfd_ra`, `x4_t4_nfkd_ra`) cộng `x_wr_ra_nfkc` của Phụ lục H — đúng bảng §1.10.3 của r4. "Đầy đủ" = `_do_ban_kinh` chạy trọn 56 ca (bán kính thật); "nhanh" = chỉ ca đích của dò.

### TỶ LỆ VÁ THẬT 3→4 (protocol §12; "ĐÃ VÁ THẬT" theo §8.3)

- **U = 6** (2 P2 + 4 P3, mỗi lớp một lần). **F = 4** — `canh-x3-wr5-nfkc-tu-va-cham-mo-neo` · `t53-thoi-gian-khong-co-tieu-chi-do` · `ra-ha-nguon-main-bo-ghi-chua-co-o` · `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan`.
  **Không vào F (2):** `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia` (CÒN MỞ hẹp: cùng cơ chế "ngoại lệ thoát khỏi ô ⇒ tin_dung_gia" ở chỗ gọi mà bản vá không liệt kê) ·
  `r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat` (TÁI PHÁT: bản vá sửa đúng hai biểu hiện được chỉ rồi sinh biểu hiện thứ ba cùng nguồn — nhãn lấy từ tên cây đo thay vì từ phân loại của chính §5).
- **Tỷ lệ = 4/6 = 66,67 %.** Cách đọc nghiêm (xếp `t53-…` ra ngoài vì vCPU runner không đo được dù chữ r4 đã khai): 3/6 = 50,00 %.
  Hai chuyển tiếp liên tiếp: 2→3 = 13/16 = 81,25 % (lượt 3 [`luot3/VERDICT.md`, TỶ LỆ VÁ THẬT 2→3]) và 3→4 = 66,67 % (hoặc 50,00 %) — cả hai ≥ 50 %, nên điều kiện dừng thứ nhất của §12 KHÔNG kích hoạt.
- **Lớp MỚI tại r4 (không vào tử số): 2**, cả hai P3 — `a5-bang-noi-khong-ghim-tap-54-do`, `muc-tieu-moi-duong-vao-co-canh-mau-thuan-no-j`. **Lớp tái mở** (đã ĐÃ VÁ THẬT rồi mở lại): 0 — riêng `a5-bang-noi-khong-ghim-tap-54-do`
  cùng HỌ `a5-*` với `a5-canh-khong-kiem-bang-do` (P3 lượt 2, F ở lượt 3) nhưng khác đối tượng: lớp cũ là "A5 chỉ so TÊN mục thêm, không so BỘ" (r3 đã vá bằng phép so bộ, r4 giữ nguyên và tôi đo vẫn có răng: `lech-bo`, `bo-cu`, `tap-ten`);
  lớp mới là "không ai ghim TẬP 54 dò ở cột trái của bảng nối". Nếu điều phối thấy hai lớp cùng một cơ chế thì xếp lại thành TÁI MỞ — số lớp mở không đổi, chỉ nhãn.
- **Điều kiện §12 (2)** (r4 khai: "đã thoả cho ba họ `ra`, thời gian/tiêu chí, bậc hai"): đối chiếu `luot3/VERDICT.md` phần TỶ LỆ VÁ THẬT 2→3 — lời của r4 khớp (13/16 = 81,25 %, 12/16 = 75,00 % cách đọc nghiêm; ba họ đúng tên, đúng chuỗi slug lượt 1→2→3);
  r4 KHÔNG tự quyết checkpoint (§0 dòng 142–144; S6) — đúng chữ protocol §12. Tôi **không** quyết checkpoint. Hai điều tôi thêm vào lời khai ấy: (a) lời khai chỉ đếm ba họ, nhưng mục (c) của chính nó (§12 S6) đã liệt kê THÊM "họ ngoại lệ" — nếu đếm `m5-ngoai-le-chi-ba-kieu` (lượt 2) → `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia` (lượt 3) → cùng lớp CÒN MỞ hẹp (lượt 4) thì họ ngoại lệ cũng đủ ba lượt khác nhau; (b) họ ngoại lệ là họ duy nhất mà lượt này còn thấy biểu hiện CÓ THẬT (xem lớp 2). Đây là điều kiện để điều phối/chủ kho đọc, không phải quyết định của tôi [L249, L394].

## BẢNG LỚP

Mỗi finding có đúng một slug lớp nguyên nhân (protocol §8.3); đếm lớp và đếm biểu hiện riêng. `reviewed_sha` mọi lớp: `42cd314ca070e8e542fbd291b398690c2e5e54fd`. Cột phương án chỉ MÔ TẢ (Q14);
văn bản sửa đặc tả (không có mã) nằm ở `HINT.patch`, mỗi nhóm mở bằng `# lop: <slug>`.

| slug lớp | hạng | biểu hiện (đếm) | nguồn | phương án (chỉ mô tả; Q14) | phép kiểm đóng lớp / giới hạn |
|---|---|---|---|---|---|
| `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia` | P3 (hạ từ P2) | 2: (1) chỗ gọi THỨ SÁU của mã bị đo — vòng `_luoi_git` cũ của `--tu-kiem-che-do`, nơi ba ô M5 của r2 gọi `_van_tay()` dưới `except Exception`: 3 dò `y4_luoi_git_{runtime,value,unicode}_exit` SỐNG trên nền, KHÁC (tín dụng giả) trên ứng viên làm đúng chữ r4; (2) J-NEM không có răng cho chữ "MỌI `BaseException`": bản bắt `(Exception, SystemExit)` qua J-NEM 11/11 và 54 canh; 8 dò `y4_{t1,t2,t4,head}_{kbint,genexit}` GIẾT trên bản bắt `BaseException`, KHÁC trên bản kia | CÒN MỞ (hẹp) từ lượt 3 (P2 `m2b-…`) | §5 M6: sửa "đúng năm chỗ" thành sáu chỗ (hàng thứ sáu: vòng `_luoi_git`), vòng ấy phải bắt `BaseException`; Phụ lục J kế tiếp thêm hai họ dò (ném `BaseException` khác `SystemExit` ở bốn chỗ gọi; ném `SystemExit` ở ba kiểu ngoại lệ M5) vào J-NEM, hoặc §10 khai giới hạn bằng chữ | 11 dò `y4_*` (`evidence/scripts/blk_mine.py`): sau vá phải GIẾT đúng ca đích trên ứng viên, KHÁC trên bản bắt `(Exception, SystemExit)`; đột biến: đổi vòng `_luoi_git` về `except Exception` ⇒ 3 dò ra KHÁC. Giới hạn: 11 dò là của tôi, ngoài tập đóng 401, không thuộc 470 mục; ứng viên là của tôi |
| `a5-bang-noi-khong-ghim-tap-54-do` | P3 | 1: A5 và Phụ lục F r4 chỉ đòi MỖI tên cột trái là một dò có thật và bộ của mục bằng bộ của dò ấy; không đòi cột trái = 54 tên của bảng canh §5. Hai bảng nối đổi tên (54 dò đầu của tập đóng ngoài bảng §5 — 41 T-B, 7 T-C, 4 T-D, 2 T-E; và 35 dò J + 19 dò T-C — tất cả 108 dò GIẾT đúng ca đích trên ứng viên) ⇒ F rc=0, `dem_neo` 0/470, `so_loi` 0 | MỚI (họ `a5-*`; không tái mở `a5-canh-khong-kiem-bang-do`, xem TỶ LỆ VÁ) | A5/Phụ lục F kế tiếp ghim tập cột trái bằng DANH SÁCH CHO PHÉP 54 tên đóng băng (không bằng danh sách cấm), trả mã 1 thẻ `tap-do` khi lệch; ghi vào "ĐỎ KHI" của A5 | `c_swap`, `c_swap2`: rc=0 hôm nay ⇒ rc=1 `tap-do` sau vá; đột biến nới danh sách cho phép để chứa tên tấn công phải làm ca đích đỏ lại. Giới hạn: chỉ xảy ra khi executor ĐỔI tên (sai-nhưng-thoả-chữ); làm đúng chữ r4 không dính |
| `r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat` | P3 | 1 (3 chỗ): nhãn "24 canh r2" ở §0 dòng 118, §1.10.2 dòng 1035 và 1622; số 55 = 11 + 24 + 20 ĐÚNG nhưng 24 = 9 canh r1 + 15 canh r2 theo phân họ 16/27/11 của chính §5 (canh "r2" của §5 là 27) | TÁI PHÁT (hẹp) từ lượt 3 (P3) | đổi nhãn thành "24 canh cũ (9 r1 + 15 r2)" ở ba chỗ và nói thẳng vì sao nhãn "r2" lệch (cây đo của r4 gọi cả 43 canh r1+r2 là `r2_<dò>`) | `grep -n "24 canh r2"` rỗng sau vá; 55 giữ nguyên (đo `c_tq`: 11 + 24 + 20 [L211, L214]). Giới hạn: lỗi nhãn, không ảnh hưởng gì phép đo |
| `muc-tieu-moi-duong-vao-co-canh-mau-thuan-no-j` | P3 | 1: dòng `objective` (dòng 15) viết "Mỗi đường vào có ít nhất một đột biến canh … bán kính 1" không giới hạn theo r1–r3, trong cùng ô liệt kê đường vào của r4 (bốn chỗ M6, lần gọi thứ hai và so dòng in của T5, thành viên hạ nguồn); §10 (dòng 2110–2112) và §11.1 (D) điểm 22 (dòng 2272) nói r4 KHÔNG thêm canh, tổng giữ 54/470, nợ `j-chua-co-canh-wp698` | MỚI | giới hạn câu mục tiêu theo "đường vào của r1–r3" và trỏ nợ `j-chua-co-canh-wp698` ngay tại câu ấy | `grep -n "Mỗi đường vào có ít nhất"` còn đúng một câu và có giới hạn; A5/F/S5 (54/470/300) không đổi. Giới hạn: nếu điều phối đọc "tự mâu thuẫn" trong thang hạng là tự động P1 thì lớp này P1 — tôi xếp P3 vì mâu thuẫn nằm ở một câu mục tiêu còn mọi cổng và nợ có tên nhất quán ở ≥ 3 chỗ |

Tổng kết lượt 4: **0 P1 · 0 P2 · 4 P3 = 4 lớp** / 5 biểu hiện — 2 lớp NỐI từ U của lượt 3 (`m2b-…` P2→P3 CÒN MỞ hẹp; `r3-khai-ve-…` P3 TÁI PHÁT hẹp) và 2 lớp MỚI (`a5-bang-noi-…`, `muc-tieu-moi-…`, cả hai P3).
Bốn lớp ĐÃ ĐÓNG của lượt 3 (xem ĐỐI CHIẾU). `approve` chỉ khi 0 lớp ⇒ **`changes_requested`**.

## BẢNG SĂN

Mẫu: `HƯỚNG n: tên / giả thuyết / lệnh / output / kết luận: LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC`. Thẻ `[L<i>]` = mục `L<i>` của `evidence/logs/lenh_va_ket_qua.md`; thẻ `[Đ<n>]` = dòng đo ở BẢNG ĐO / `evidence/results/`.
Hạng lớp ghi ở BẢNG LỚP; hướng KHÔNG PHẢI LỖI cũng ghi số đo để lượt sau khỏi đo lại.

| HƯỚNG | tên | giả thuyết | lệnh / output (tóm) | kết luận |
|---|---|---|---|---|
| 1 | Ứng viên độc lập theo chữ r4 chạy Phụ lục F r4 + J | làm đúng từng chữ r4 thì F xanh và 35 dò J GIẾT bán kính 1 (hai P2 lượt 3 đã đóng) | `pl_F.py nen c_all bang_noi_all.txt …` ⇒ rc=0, `dem_neo {muc:470, lech:0}`, `so_loi:0`; `do_dot_bien_r4.py` 35 dò đầy đủ ⇒ `G35 S0 K0` [Đ05, Đ06] | **KHÔNG PHẢI LỖI** (lớp 1 ĐÃ ĐÓNG) |
| 2 | Mỏ neo "so với số nền" mở lỗ mới? | một mục nền đã trùng 2 lần, ứng viên thêm một bản trùng NỮA mà F không bắt | đếm nền: 232 mục `cong_cu_test.py` đếm 1, 181 mục khác đếm 1, ba mục `bn_*` của `ops/bash_nen.py` = 2, 2, 3 [L190]; bản trùng cho `bn_*` buộc phải sửa `bash_nen.py` ⇒ ngoài write set (A4-f `git diff --name-only` ≠ `{ops/cong_cu_test.py}` ⇒ ĐỎ); F bắt trùng của mục `cong_cu_test.py` (c_tq 20 mục cũ, c_cu 1) [Đ05] | **KHÔNG PHẢI LỖI** (lỗ phải đi qua tệp ngoài write set) |
| 3 | Bảng nối đổi tên | A5/F chỉ ghim bộ theo TÊN cột trái, không ghim tập 54 tên | cây `c_swap` (54 dò đầu của tập đóng ngoài bảng §5: 41 T-B, 7 T-C, 4 T-D, 2 T-E) ⇒ F rc=0 (`so_loi 0`); cây `c_swap2` (35 dò J + 19 dò khác) ⇒ F rc=0 [L296, L483, L486, Đ05] | **LỖI** — lớp `a5-bang-noi-khong-ghim-tap-54-do` (P3) |
| 4 | M6: điểm gọi còn sót (AST) | ngoài 4 chỗ + M5b còn chỗ gọi cùng cơ chế | AST trên nền: `_van_tay` 11 chỗ (`_main_gop` 1, `_in_tu_kiem_gom` 1, `_in_tu_kiem_che_do` 7, `main` 2), `_doc_che_do` 2, `_ket_thuc_manh` 8, `main` 2 [L220]; chỗ thứ sáu = vòng `_luoi_git` cũ trong `_in_tu_kiem_che_do` (`except Exception`, ba hàng M5 của r2); 3 dò `y4_luoi_git_*`: nền SỐNG, ứng viên KHÁC [L489] | **LỖI** — lớp `m2b-…` (P3, CÒN MỞ hẹp) |
| 5 | M6: sai-nhưng-thoả-chữ `(Exception, SystemExit)`; `KeyboardInterrupt`/`GeneratorExit` | J-NEM (chỉ `SystemExit` và lớp con `Exception`) không phân biệt bản bắt MỌI `BaseException` với bản bắt `(Exception, SystemExit)` | cây `v_exc_sys`: J-NEM `G11 S0 K0` (qua hết); 8 dò `y4_*_{kbint,genexit}`: `c_all` G8, `v_exc_sys` K8, `v_exc` K8 [L489, L471] | **LỖI** — cùng lớp `m2b-…` |
| 6 | `KeyboardInterrupt`/`GeneratorExit` bị nuốt có làm hỏng hành vi dừng của bộ chạy không | `except BaseException` ở cửa con nuốt Ctrl-C ⇒ bộ chạy treo | `sigint_exp.py`: SIGINT cho CẢ nhóm: cha thoát rc=−2 sau 0,11–0,34 s, 0 tiến trình mồ côi; SIGINT chỉ cho cửa con: ở hai lượt thử: một lượt ca ra `giet_that` với ô lệch ghi `['NEM','KeyboardInterrupt']` (Ctrl-C bị nuốt thành DỮ LIỆU so lệch ⇒ đỏ), một lượt cửa con chết rc=−2 ⇒ `tin_dung_gia` (đỏ); không lượt nào ra XANH [L558, L561] | **KHÔNG PHẢI LỖI** |
| 7 | A4-g theo CPU: đỏ đúng nguyên nhân, nhiễu | r đỏ giả khi tải; không đỏ khi nguyên nhân khác | `run_I.sh` ×9 (bảng ở Đ10): 6 lượt `c_all` rc=0, r 1,2700–1,3063 (loadavg 5–14); `tv_cpu` rc=1 chỉ `cpu` (r 1,4174); `tv_naive` rc=1 `dem`+`cpu` (r 3,9584; 122456 lời gọi băm lớn vs 64); `tv_cham` rc=0 (Δ tường 29,1 s, r 1,2728) | **KHÔNG PHẢI LỖI** (CPU máy khác: KHÔNG ĐO ĐƯỢC) |
| 8 | Biên 27,9 phút vs trần 30 | "biên ≥ 2 phút" đúng với mọi mẫu CI trong kho | 18,23×(59/52)×1,35 = 27,92 (đúng khai); mẫu CI thứ hai có sẵn trong kho (run `36689211190`, job dài nhất 18,32) ⇒ 28,06 phút, biên 1,94 [L290]; vCPU runner KHÔNG ĐO ĐƯỢC | **KHÔNG ĐO ĐƯỢC** (quan sát lệch 0,06 phút; chữ r4 đã khai "theo mô hình", ba giả định) — không lập lớp |
| 9 | T5: bản đúng vs sai-nhưng-thoả-chữ | cách viết bộ ghi của r3 / bỏ lần gọi thứ hai / bỏ phép so dòng in lọt J-T5 | `v_t5_r3`: S6 K0 G4; `go_hai`: S3; `go_in`: S3; `go_wr`: K7; J-TV `nomem` S15/15 [L459] | **KHÔNG PHẢI LỖI** (răng đủ) |
| 10 | A8 bậc hai (ba cây gỡ) | mệnh đề r4 sai trên ứng viên | `v_go_e698`: 3 canh E r3 SỐNG, 2 canh r2 GIẾT; `v_go_r2exc`: 5/5 GIẾT; `v_go_exc2`: 5 canh SỐNG + 2 đối chứng GIẾT [L471] | **KHÔNG PHẢI LỖI** |
| 11 | Tập đóng 401 + Phụ lục A trên ứng viên | còn dò SỐNG ngoài khai | T-B `G222 S2` (hai tương đương IMP-R2F) · T-C `G113 S1 K1` (`x3_wr5_normpath` tương đương, `x3_wr_ra_lower` đối chứng) · T-D `G16` · T-E `G30` · ngoài lớp `S11` · KHAI `S5`; A (30): `G22 S8` (`e48_*`, lớp A ngoài packet) [L495] | **KHÔNG PHẢI LỖI** |
| 12 | 54 canh bán kính 1 | canh nào ra KHÁC / bán kính 2 | `do_dot_bien_r4.py` đầy đủ trên 54 canh + 2 đối chứng ⇒ `G54 S0 K2` (K = `c49_ra_abspath`, `s_ra_realpath`, đúng khai) [Đ07] | **KHÔNG PHẢI LỖI** |
| 13 | Bán kính của 232 mục CŨ trên ba cửa `t52/t53/t54` | ô mới làm một mục cũ chết thêm ở cửa khác ⇒ A5 ĐỎ mà S4 cấm sửa | 232 mục `DOT_BIEN` cũ có tệp đích `ops/cong_cu_test.py` (ca đích `t54` 89 · `t52` 65 · `t53` 50; 28 mục ca đích ngoài ba cửa: `t39` 18 · `t42` 3 · `t29` 2 · `t45` 2 · `t32` 2 · `t31` 1). `door_radius.py` trên ứng viên: 576 lượt chạy cửa — 492 lượt ở cửa KHÁC ca đích: **492/492 `qua`** (0 mục chết thêm ở `t52/t53/t54` ⇒ 0 bán kính 2 do ô mới); 84 lượt ở ca đích của 84 mục chưa có kết quả nhanh: **84/84 `giet_that`**; cộng 120/120 `giet_that` của lượt nhanh trước ⇒ **204/204** mục có ca đích là một cửa vẫn bị đúng ca đích giết. 28 mục ca đích ngoài ba cửa: `full_muc.py` (`_do_ban_kinh` 56 ca + `_ket_luan_ban_kinh`) ⇒ **G28 S0 K0** [`evidence/results/r_c_all.jsonl`, `f_c_all.jsonl`] | **KHÔNG PHẢI LỖI** (phạm vi: 232/232 mục cũ của tệp đích; 53 ca không phải cửa chạy trên 204 mục đầu: KHÔNG ĐO ĐƯỢC — ô mới không nằm ở đó; 184 mục có tệp đích khác: KHÔNG ĐO ĐƯỢC — ô mới không gọi mã của chúng) |
| 14 | A4-a…f trên ứng viên | ô mới làm đỏ bộ 56 ca / phạm vi | A4-a nền & ứng viên: `55/55 đạt; tổng=56, bỏ qua=1`, `đột biến=416→470`, `cổng cây thật=ĐẠT`, rc=0; A4-b F841 `ci` :2606 (nền) / :2661 (ƯV); A4-d `hunk 16, cham []`; A4-e `sau_moc []`; A4-f 1 tệp [Đ12, L314, L317] | **KHÔNG PHẢI LỖI** |
| 15 | Trần 300 dòng, write set với M6 | M6 đẩy ứng viên quá 300 dòng | ứng viên `+287/−4`; (c_tq +324, c_cu +289); S5 đã khai "có thể VƯỢT 300 ⇒ DỪNG" | **KHÔNG PHẢI LỖI** (vẫn là biên mỏng 13 dòng; chữ r4 nói thẳng) |
| 16 | Trung thành quyết định chủ kho | r4 đổi/bỏ một quyết định | đọc lại `readback-5914438647.json` (2122 byte; OWNER; 2026-09-30T15:30:26Z) so với bảng đối chiếu §11.1: Q1–Q14 từng điểm; khối `nang_tran` dùng ADR-0048 `tran_cu: 10` (ADR-0048 có thật, Accepted 2026-09-12 [Đ21]) | **KHÔNG PHẢI LỖI** |
| 17 | Mức assurance `review_deferred` | tự nâng mức | `ops/bien_nhan_v2.py` dòng 502: `ASSURANCE_CAN_DOC_LAP = {cross_approved, same_provider_approved, human_audited}`; dòng 720: từ chối khi tự khai chạy trong phiên điều phối; reviewer Sonnet cùng họ Claude với executor ⇒ từ chối `cross_approved` [L229] | **KHÔNG PHẢI LỖI** |
| 18 | Số học trong §0/§1.10 | số sai | #D698 19588 (3.11) / 19798 (3.12) / 19803 (3.13); S1 = 19801×34 = 673 234; S2 = 6×19798+16×210+4×30 = 122 268 (cửa t53 in đúng `[673234, 122268, …]`); T698 = 30; 396 khúc, NFD 3/NFKC 5/NFKD 8 > 255 byte; 29 `isspace`, 10 `splitlines`, R698∩D698 = 13 [L281, L426, L561] | **KHÔNG PHẢI LỖI** |
| 19 | Master `ab457c6` | `ops/cong_cu_test.py` đổi | `git diff --quiet fc852ff master-ab457c6 -- ops/cong_cu_test.py` rc=0; blob `9edea6b1…` cả hai; 416 mỏ neo cũ: 0 lệch số đếm; `.github/workflows/ci.yml` +94 dòng nhưng `gate-cong-cu` vẫn `timeout-minutes: 30`, 8 mảnh | **KHÔNG PHẢI LỖI** [L332, L235, L258] |
| 20 | Vệ sinh văn bản | chuỗi thoát, dấu bỏ-qua-CI, Cf, bảng lệch | 0 chéo ngược, 0 dạng bỏ-qua-CI, 0 Cf, 0 chỗ giữ (dạng tên bao bằng hai cặp dấu @), bảng Markdown đều ô; 3352 dòng, 349 771 byte [L450] | **KHÔNG PHẢI LỖI** |
| 21 | Câu mục tiêu vs nợ J | tự mâu thuẫn | dòng 15 vs dòng 2110–2112 và 2272 [L320] | **LỖI** — lớp `muc-tieu-moi-duong-vao-co-canh-mau-thuan-no-j` (P3) |
| 22 | Nhãn "24 canh r2" | nhãn lệch hiện vật | 3 chỗ; 55 = 11 + 24 + 20 đúng, 24 = 9 + 15 [L205, L211, L214, L504]; `r4do/kq/bang_noi.txt`: 43 canh r1+r2 đều tên `r2_…` | **LỖI** — lớp `r3-khai-ve-…` (P3, TÁI PHÁT) |
| 23 | Lời khai §12(2) | khai điều kiện sai | khớp `luot3/VERDICT.md` (13/16 = 81,25 %; ba họ; chuỗi slug lượt 1→2→3); r4 không tự quyết checkpoint | **KHÔNG PHẢI LỖI** (kèm hai điều thêm ở ĐỐI CHIẾU) |
| 24 | 28 dò `y_*` của reviewer lượt 3 trên ứng viên | còn dò SỐNG ngoài khai | `runpool.py c_all c_all_y names_y.txt` (đầy đủ, 56 ca, bán kính thật) ⇒ `G27 S1`; S = `y_exc_shutil`; theo họ: `exc` 8 (7 G + 1 S), `head` 6 G, `wr5` 6 G (kể cả `y_wr5_unlink_nfkc`, `y_wr5_print_nfkc`, `y_wr5_print_strip` mà lượt 3 đo SỐNG), `main` 3 G, `wr` 3 G, `m3a`/`m3b` 1 G mỗi họ [Đ14] | **KHÔNG PHẢI LỖI** (khớp §1.10.8: 27 GIẾT + 1 SỐNG tương đương) |
| 25 | Tên trong code span của đặc tả | tên dò/canh không tra được | 3942 code span (1364 khác nhau), 301 có hình dạng tên; 127 không tra tự động — mọi cái đều là mẫu có sao/tiền tố, tên cây biến thể (`v4_*`, `tv_*`), họ `f49_*`/`f50_*` (có trong bảng nối), hoặc dò `y_*` của lượt 3 [L344, L347] | **KHÔNG PHẢI LỖI** |
| 26 | Răng của chính Phụ lục F | F xanh dù canh yếu / bộ cũ đổi / bảng thiếu / mỏ neo trùng | `lech-bo`, `bo-cu`, `tap-ten`, `dem-neo` đều bắt; gỡ chốt `dem-neo` khỏi F ⇒ `c_lit` rc=0 (chốt có răng) [Đ05b] | **KHÔNG PHẢI LỖI** |
| 27 | A5 mảnh 0/8 trên ứng viên | mảnh 59 đột biến có mục bán kính 2 / KHÁC | `chay_manh.py c_all 0/8` ⇒ rc=0; `MẢNH 0/8: 59/59 đột biến bán kính 1`; 59/59 dòng `ok`; tệp mảnh ghi `sha256_test` = băm tệp ứng viên (`39599c2f…`); 772,4 s tường, 1789,4 s CPU [Đ16] | **KHÔNG PHẢI LỖI** (khớp phiên soạn: 59/59; 7 mảnh còn lại KHÔNG ĐO ĐƯỢC) |

## BẢNG ĐO

Mọi số dưới đây có lệnh đo lại được (thẻ `[L<i>]` trong `evidence/logs/lenh_va_ket_qua.md`, tệp thô trong `evidence/results/`, công cụ trong `evidence/scripts/`).
Ba trạng thái: **có** · **không** · **KHÔNG ĐO ĐƯỢC**. Cột "khớp?" so với CHỮ của đặc tả r4.

| # | khẳng định | đặc tả khai | đo được | khớp? |
|---|---|---|---|---|
| Đ01 | băm đặc tả r4 / r3 / r2 / r1 | `b51b5ffa…95e0` / `53bf55fe…dfe1b` / `f69bb398…2c0a` / `3a555263…4996` | `sha256sum SPEC*.md` ⇒ đúng bốn băm; `git -C cay-kho rev-parse HEAD` ⇒ `42cd314c…e5e54fd` [L8] | KHỚP |
| Đ02 | blob `ops/cong_cu_test.py` | PROMPT: "đo xem có đổi so với `fc852ff` không" | `git hash-object` và `git rev-parse fc852ff:ops/cong_cu_test.py` ⇒ `9edea6b1629b46f27758b2073e74210dc73495b7` (cả hai); `git -C kho.git diff --quiet fc852ff master-ab457c6 -- ops/cong_cu_test.py` ⇒ rc=0, blob master `9edea6b1…` ⇒ **KHÔNG đổi** [L69, L332] | KHỚP |
| Đ03 | master `ab457c6` khác nền ở đâu | — | 217 tệp (hồ sơ + vài tệp); 416 mỏ neo nền: 0 lệch số đếm; `ci.yml`: `gate-cong-cu` vẫn `timeout-minutes: 30`, 8 mảnh, `gate-cong-cu-gop` 10; 14 dòng PROTOCOL §12 trích ở S6 giữ nguyên chữ, dời dòng 1043→1087 [L235, L258, L332, L335] | KHỚP (không câu nào của đặc tả đổi) |
| Đ04 | băm 10 phụ lục A–J; số dò | A 30 · C 221 · H 145 (366 sau ghép) · J 35 ⇒ 401 | trích bằng `extract.py`: 10/10 KHỚP; `liet_ke`: 30 / 366 / 401 [L75, L133] | KHỚP |
| Đ05 | Phụ lục F r4 trên 4 cây (`c_all`, `c_lit`, `c_tq`, `c_cu`) | rc 0 · 1 (1) · 1 (55) · 1 (1) | `evidence/results/F/F_*.json`: `c_all` rc=0 `dem_neo {470,0}` · `c_lit` rc=1 `["dem-neo","c698_x3_wr5_nfkc",2,1]` · `c_tq` rc=1 55 lệch · `c_cu` rc=1 `["dem-neo","f35_writer_parents",2,1]` [L178, L181, L187] | KHỚP |
| Đ05b | răng của chính F | `lech-bo` · `bo-cu` · `tap-ten` · gỡ `dem-neo` ⇒ `v4_lit` rc=0 | cả bốn bắt; F bỏ `dem-neo` trên `c_lit` ⇒ rc=0 (`evidence/results/F/rang_cua_F.txt`) | KHỚP |
| Đ05c | F với bảng nối đổi tên | — (không khai) | `c_swap` (54 dò ngoài bảng §5: 41 T-B, 7 T-C, 4 T-D, 2 T-E) rc=0; `c_swap2` (35 dò J + 19 dò T-C) rc=0, `so_loi` 0 [L296, L486] | **LỆCH** — lớp `a5-bang-noi-…` |
| Đ06 | 35 dò Phụ lục J, ứng viên | GIẾT hết, bán kính 1 | `summ.py c_all_J` ⇒ `G35 S0 K0 ?0` (đầy đủ 56 ca) | KHỚP |
| Đ07 | 54 canh bán kính 1; 2 đối chứng | 54 GIẾT; `s_ra_realpath` KHÁC (bán kính 2), `c49_ra_abspath` giết 2/56 | `summ.py c_all_canh` ⇒ `G54 S0 K2` (K = hai đối chứng) | KHỚP |
| Đ08 | tập đóng 401 + Phụ lục A trên ứng viên | T-B 224 · T-C 115 · T-D 16 · T-E 30 · ngoài lớp 11 · KHAI 5; chỉ đối chứng/tương đương/KHAI sống | T-B `G222 S2` · T-C `G113 S1 K1` · T-D `G16` · T-E `G30` · ngoài lớp `S11` · KHAI `S5`; A: `G22 S8` [L278, L495] | KHỚP |
| Đ09 | răng của bản vá: J-NEM/T5/TV/A8 | §6 A2, A8 (bảng) | J-NEM: `v_nocatch` G0 K11 · `v_exc` G5 K6 · `go_t1` K1 · `go_head` K1 · `go_main` K4 · `go_wr` K5; J-T5: `v_t5_r3` S6 · `go_hai` S3 · `go_in` S3; J-TV `nomem` S15/15; A8: `go_e698` S3 + G2 · `go_r2exc` G5 · `go_exc2` S5 + 2 đối chứng G [L456, L459, L471] | KHỚP từng ô |
| Đ10 | A4-g (Phụ lục I r4), 9 lượt | r 1,259–1,308 (6 lượt); mảnh ≈ 26,0–27,1; ngưỡng 1,35 ⇒ 27,9; `tv_naive` đỏ `dem`+`cpu`; `tv_cpu` chỉ `cpu`; `tv_cham` không bắt | 6 lượt `c_all`: r = 1,3063 · 1,2841 · 1,3013 · 1,2727 · 1,2841 · 1,2700 (trung bình 1,2864), mảnh 26,27–27,02, `lon` 67/64, rc=0; `tv_cpu` rc=1 `[cpu 1.4174 1.35]`; `tv_cham` rc=0 (r 1,2728; Δ tường 29,1 s); `tv_naive` rc=1 `[dem 122456 64][cpu 3.9584 1.35]`; loadavg 5,2→19,6 [L513–L522, L555] | KHỚP |
| Đ10b | biên 27,9 → trần 30 | "≥ 2 phút theo mô hình" (mẫu CI `36696528580`, job dài nhất 18,23) | 18,23×(59/52)×1,35 = 27,92 ⇒ biên 2,08; mẫu CI thứ hai trong kho (`36689211190`, dài nhất 18,32) ⇒ 28,06 ⇒ biên 1,94 [L208, L290] | LỆCH 0,06 phút (quan sát) |
| Đ11 | SIGINT/KeyboardInterrupt | — | cha thoát rc=−2 sau 0,11–0,34 s, 0 tiến trình mồ côi [L558, L561] | KHÔNG PHẢI LỖI |
| Đ12 | A4-a nền và ứng viên | `M/M đạt`, `lỗi đột biến=0`, `cổng cây thật=ĐẠT`, rc=0 | nền: `55/55 đạt; tổng=56, bỏ qua=1`, `đột biến=416`; ứng viên: cùng `55/55`, `đột biến=470`; cả hai `lỗi đột biến=0`, `cổng cây thật=ĐẠT`, rc=0, 4,2 và 4,9 phút (`evidence/results/A4/`) | KHỚP |
| Đ13 | A4-b/d/e/f, A1(iv) | delta 0; G `cham []`; E `sau_moc []`; 1 tệp; `0 0 ['0x2026']` | ruff 0.15.8: `F841` ở :2606 (nền) và :2661 (ứng viên), cùng thông điệp; G `hunk 16 cham []` rc=0; E `tong 9 sau_moc []`; `git diff --name-only` ⇒ `ops/cong_cu_test.py`; A1(iv) cả hai `0 0 ['0x2026']` [L314, L317] | KHỚP (ruff 0.15.15: KHÔNG ĐO ĐƯỢC) |
| Đ13b | A4-c `ci_dang_ky_test.py` | `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT`, delta 0 | nền và ứng viên: `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT`, rc=0 (`evidence/results/A4/ci_dang_ky_*.out`) | KHỚP |
| Đ14 | 28 dò `y_*` (lượt 3) trên ứng viên | r4 §1.10.8 (lượt 3 cũng đo thế): 27 GIẾT + 1 SỐNG (`y_exc_shutil`) | 27 GIẾT + 1 SỐNG (`y_exc_shutil`); `evidence/results/y_c_all.jsonl` | KHỚP (§1.10.8) |
| Đ15 | bán kính 232 mục cũ trên `t52/t53/t54` | A5: mọi mục bán kính 1 (phiên soạn chỉ chạy mảnh 0/8: 59/59) | 492/492 lượt ở cửa khác ca đích `qua`; 204/204 ca đích-cửa GIẾT; 28/28 mục ca đích ngoài cửa G (đầy đủ) [Đ15 = `evidence/results/r_c_all.jsonl`, `f_c_all.jsonl`] | KHỚP (0 bán kính 2) |
| Đ16 | A5 mảnh 0/8 | (phiên soạn chạy mảnh 0/8, 59/59; `v4_all`: 1097,4 s tường, 1803,8 s CPU) | rc=0, `MẢNH 0/8: 59/59 đột biến bán kính 1`; 772,4 s tường, 1789,4 s CPU, loadavg 1,96→2,19; 30,33 s CPU mỗi đột biến (`evidence/results/manh/`) | KHỚP (hai cách viết độc lập cho CPU mỗi đột biến 30,33 và 30,57 s) |
| Đ17 | S1/S2, D698, T698, khúc tên | S1 = 673 234, S2 = 122 268 (3.12); #D698 19 588/19 798; T698 = 30; 396 khúc, 3/5/8 | cửa `t53` in `[673234, 122268, …]`; `#D698` = 19 588 / 19 798 / 19 803 (3.11.15 / 3.12.3 / 3.13.12); `isspace` 29, tách dòng 10, R698∩D698 13; 396 khúc (3.12.3), 392 (3.11.15); NFD 3 · NFKC 5 · NFKD 8 > 255 byte [L281, L426, L561] | KHỚP |
| Đ17b | miền ngoại lệ M5b, đo TRONG cửa con `--tu-kiem-che-do` | #B698 = 67; #E698 = 118 = 67 + 51 (`yaml` 11, `shutil` 7, `lease_publish_test` 4, `subprocess` 3, chính tệp 3 …); 0 ô lệch; 0 lớp không dựng được | chạy `python3.12 ops/cong_cu_test.py --tu-kiem-che-do` trên ứng viên, đọc `KQ`→`exc`: 118 khoá, lệch 0, không dựng được 0; theo mô-đun gốc `builtins` 67 · `yaml` 11 · `shutil` 7 · `lease_publish_test` 4 · `subprocess` 3 · `__main__` 3 · `bash_nen` 2 · … ; `B698 ⊂ khoá` đúng (`evidence/results/door_che_do_c_all.txt`). Nạp mô-đun trong tiến trình khác (không phải cửa con) cho 117 vì `_hashlib` chưa được nạp — số có thẩm quyền là số của cửa con | KHỚP |
| Đ17c | số ô của M2b và M3 | M2b T2/T3a/T3b: 61 đường × 2 chế độ = 122 ô; M3: 162 ô = 57 + 56 + 1 + 48 | `small_checks.py` trên ứng viên: `_duong_ra_698()` 61 (12 cấu trúc + 16×3 + 1) ⇒ 122; `_luoi_m3_698()` 162 = `truc-bq` 57 · `truc-hong` 56 · `truc-tk` 1 · `tich` 48 (`evidence/results/small_c_all.txt`) | KHỚP |
| Đ18 | thời lượng 8 job CI | 17,58 · 18,23 · 15,83 · 18,05 · 18,12 · 12,67 · 17,67 · 18,05 phút | tính lại từ `readback-jobs-36696528580.json` / `r4do/kq/run_36696528580_jobs.json`: đúng tám số; bước G5 của job dài nhất 17,82 [L208, L290] | KHỚP |
| Đ19 | trần 300 dòng | `v4_all` +291/−4 | ứng viên +287/−4 (8393 → 8676 dòng); biến thể `c_tq` +324 (vượt), `c_cu` +289 | KHỚP (biên mỏng; S5 khai) |
| Đ20 | "ba ngưỡng" (lượt 3 P3) | 0 chỗ còn | `grep -c -i "ba ngưỡng"`: r3 = 4, r4 = 0; `grep -c f49_nfkc_bk`: r1 0 · r2 2 · r3 2 · r4 4 [L205] | KHỚP |
| Đ21 | trung thành quyết định chủ kho | bảng §11.1 Q1–Q14 | `readback-5914438647.json` (2122 byte, tác giả `ducthangho`, `OWNER`): Q1 chỉ F49+F50 · Q2 fullwidth là nợ (A1(iv) đo `0 0`) · Q3 giữ TAB, `>=2`, `len(CA)-1`, `hong`, `tien_kiem` · Q4 trục trọn `0…len(CA)` (M3: 57 + 56 + 1 + 48 = 162 ô) · Q5 lặp tới 0/0/0 · Q9 · Q10 · Q12 ≤ 3 tệp, ≤ 300 dòng (S5) · Q13 · Q14 không patch-as-hint (đặc tả chỉ mô tả; HINT lượt này chỉ sửa văn bản); ADR-0048 `0048-tran-vong-review-len-muoi.md` Accepted 2026-09-12 [L66] | KHỚP: đối chiếu từng chữ của Q1–Q14 (thân comment `5914438647` + nhãn hai lượt) với bảng §11.1 (B) — mọi cách đọc rộng/hẹp/chặt hơn chữ (Q1 rộng, Q2 rộng, Q3 vượt chữ, Q4 hẹp, Q9 chặt, Q10 và Q13 rộng, Q14 hẹp) đều có dòng ở cột "so với chữ"; tôi KHÔNG thấy lệch nào không được khai; Q5: "2" là trục VÒNG của ADR-0043, r4 nêu rõ và dùng `tran_cu: 10` của ADR-0048 |
| Đ22 | §12(2) | ba họ đã thoả; 13/16 | `luot3/VERDICT.md`: 13/16 = 81,25 %, 12/16 = 75,00 %, ba họ `ra`, thời gian/tiêu chí, bậc hai | KHỚP (thêm: họ ngoại lệ) |
| Đ23 | vệ sinh | không chuỗi thoát, không dấu bỏ-qua-CI, không Cf | 0 / 0 / 0; 3352 dòng, 349 771 byte; bảng Markdown đều [L450] | KHỚP |

## CHI TIẾT TỪNG LỚP

### LỚP 1 — `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia` — **P3** — CÒN MỞ (hẹp; lượt 3 là P2, slug giữ để nối lịch sử)

Phần ĐÃ ĐÓNG (đo trên ứng viên độc lập `c_all`): ô bộ ghi để `OSError: File name too long` lọt khỏi ô — dò/canh `x_wr_ra_nfkc` GIẾT `t52_…` bán kính 1/56 (đầy đủ); 11/11 dò J-NEM GIẾT đúng ca đích
ở bốn chỗ gọi (`doc`, quét `head`, `main`, bộ ghi) cộng M5b; răng đủ: `v_nocatch` 0/11 GIẾT (11 KHÁC), `v_exc` 5/11, gỡ riêng từng chỗ ⇒ đúng dò của chỗ ấy KHÁC (1 · 1 · 4 · 5) [Đ09].

**Biểu hiện 1 — chỗ gọi THỨ SÁU.**
- HƯỚNG 4: điểm gọi còn sót / giả thuyết: §5 M6 viết "các ô mới của r2–r4 gọi mã bị đo ở đúng năm chỗ"; một ô MỚI của r2 gọi `_van_tay()` ở chỗ thứ sáu dưới `except Exception` của nền.
- Lệnh: AST trên nền, đếm lời gọi của sáu hàm mã bị đo [L220]; đọc vòng `for rc, ra, loi in _luoi_git():` trong `_in_tu_kiem_che_do` của nền (`except Exception as ex:  # noqa: BLE001` rồi
  `kq["luoi_git"].append("NEM:" + type(ex).__name__)`); ba hàng M5 của r2 (`ValueError`, `UnicodeDecodeError`, `RuntimeError`) đi qua CHÍNH vòng ấy (bảng `nem` của vòng). Dò: chèn sau neo `EXC` của `_van_tay`
  một nhánh `except RuntimeError:` (hoặc `ValueError`, `UnicodeDecodeError`) gọi `sys.exit(698)` — ba dò `y4_luoi_git_{runtime,value,unicode}_exit` (`evidence/scripts/blk_mine.py`).
- Output [L489]: nền `S S S` (không ô nào của nền ném các kiểu ấy); ứng viên (chữ r4) `K K K`, lý do: `giàn giáo hỏng (chưa tới chốt nghiệp vụ): cửa --tu-kiem-che-do hỏng: rc=186` (698 mod 256 = 186) ⇒ `tin_dung_gia`,
  không phải `giet_that`. Cùng kết quả trên `v_exc` và `v_exc_sys`.
- kết luận: **LỖI** (chữ r4 không liệt kê chỗ này; vòng `_luoi_git` cũ vẫn bắt `Exception`).

**Biểu hiện 2 — J-NEM không có răng cho chữ "MỌI `BaseException`".**
- HƯỚNG 5 / giả thuyết: M6 đòi bắt "mọi `BaseException`"; mọi dò NÉM của nhóm J-NEM chỉ ném `SystemExit` hoặc một lớp con của `Exception` nên một bản bắt `(Exception, SystemExit)` — trái chữ — qua hết.
- Lệnh: cây `v_exc_sys` (bốn chỗ gọi bắt `(Exception, SystemExit)`) chạy 11 dò J-NEM; thêm 8 dò `y4_{t1,t2,t4,head}_{kbint,genexit}` (ném `KeyboardInterrupt`/`GeneratorExit` qua `(_ for _ in ()).throw(…)` ở đúng chỗ của dò `thoat` tương ứng).
- Output [L489, L471]: J-NEM trên `v_exc_sys` = `G11 S0 K0` (qua hết); 8 dò `y4_*`: `c_all` `G8`, `v_exc_sys` `K8`, `v_exc` `K8` (lý do `giàn giáo hỏng … cửa --tu-kiem-{che-do,main,gom} hỏng: rc=-2` cho `KeyboardInterrupt` và `rc=1` cho `GeneratorExit`, tức cửa con chết thay vì GIẾT bằng chốt); nền `S` (6) hoặc `K` (2: `y4_t2_*`, vì hai hàng cũ của `_luoi_noi_main` có ký tự ngoài ASCII — đúng như §5 M6 nói).
- kết luận: **LỖI** (cùng lớp). Hậu quả: bản làm sai-nhưng-thoả-chữ lọt A2/A5; đột biến thật ném `KeyboardInterrupt`/`GeneratorExit` ra `tin_dung_gia` thay vì GIẾT. Không đột biến nào trong 470 mục thuộc dạng này ⇒ lỗ đo cho tương lai, không đỏ nghiệm thu hôm nay.

**Phương án (chỉ mô tả).** (a) §5 M6: đổi "đúng năm chỗ" thành sáu và thêm hàng cho vòng `_luoi_git` (`_van_tay()` dưới `except Exception` của nền; phải đổi thành `BaseException`); (b) Phụ lục J kế tiếp (băm đổi, tập đóng 401 + n dò) thêm hai họ vào J-NEM:
ném `BaseException` khác `SystemExit` ở mỗi trong bốn chỗ gọi, và ném `SystemExit` khi `_van_tay` gặp một trong ba kiểu ngoại lệ của M5; hoặc nếu chủ kho không muốn thêm, §10 nêu giới hạn bằng chữ. `HINT.patch` nhóm `# lop: m2b-…` chỉ sửa văn bản (không đưa mã dò).
**Phép kiểm đóng lớp:** 11 dò `y4_*` GIẾT đúng ca đích (`t53_…`) trên ứng viên làm đúng; ba dò `y4_luoi_git_*` ra KHÁC khi đổi vòng về `except Exception`; tám dò `y4_*_{kbint,genexit}` ra KHÁC trên bản `(Exception, SystemExit)`.
**Giới hạn:** 11 dò là của tôi (ngoài 401); ứng viên là của tôi; mỗi dò đo ở chế độ NHANH (chỉ ca đích).

### LỚP 2 — `a5-bang-noi-khong-ghim-tap-54-do` — **P3** — MỚI (họ `a5-*`)

- HƯỚNG 3 / giả thuyết: A5 và Phụ lục F r4 kiểm (i) bộ sáu trường của 416 mục cũ, (ii) tập tên thêm = cột phải của bảng nối, (iii) bộ của mục = bộ của dò CÙNG TÊN ở cột trái, (iv) `dem-neo` — nhưng không đòi cột trái = 54 tên của bảng canh §5.
  Vậy executor đổi dò (sai-nhưng-thoả-chữ) vẫn qua cổng.
- Lệnh [L296, L483, L486; `evidence/results/F/`]: dựng `c_swap` — ứng viên có 54 canh là 54 dò đầu tiên của tập đóng không thuộc bảng §5 (41 T-B, 7 T-C, 4 T-D, 2 T-E; `s_bk_strip`, `s_bk_lower`, `s_mh_nfkd`, …; cả 54 GIẾT đúng ca đích trên ứng viên, đo ở chế độ nhanh/đầy đủ) — và `c_swap2` — 35 dò J + 19 dò T-C (`p_cf_ra_*` …) đã GIẾT (không dò nào thuộc bảng §5; F chạy hết 470 mục ở cả hai cây):
  `python3.12 -B -I pl_F.py trees/nen trees/c_swap out/bang_noi_swap.txt do_dot_bien.py do_dot_bien_r4.py`, tương tự `c_swap2`.
- Output: `{"nen": 416, "ung_vien": 470, "them": 54, "bang_noi": 54, "dem_neo": {"muc": 470, "lech": 0}, "so_loi": 0, "loi": []}` rc=0 ở CẢ HAI cây. Đối chứng [Đ05b]: bảng nối thiếu một dòng ⇒ rc=1 `tap-ten`; một canh có phép thay yếu hơn dò ⇒ rc=1 `lech-bo` — tức F CÓ răng với cột phải và với nội dung, chỉ thiếu răng với TẬP cột trái.
- Bằng chứng khuếch đại: 16 dò canh r1 — lõi F49/F50 của Q1 (`e49_*`, `x46_tab_*`, `e50_*`, `x47_*`, `x50_*`) — nằm ở Phụ lục A; Phụ lục A ∩ tập đóng 401 = ∅ (đo: 0), nên 16 canh ấy là bảo vệ MÁY (cổng) duy nhất của 16 dò đó; 38/54 dò canh còn lại (r2, r3) có thêm bảo vệ từ tập đóng.
  Đo: `A ∩ 401 = 0`, `16 canh r1 ⊂ A`, `canh ⊂ 401 = 38`.
- kết luận: **LỖI** (P3: chỉ xảy ra khi executor ĐỔI tên; làm đúng chữ r4 — lấy 54 tên từ §5 — không dính; hậu quả: sau land, các lỗ F49/F50 do 16 canh r1 gác không còn gác mà cổng vẫn xanh).
- **Phương án (chỉ mô tả):** cột trái của bảng nối phải bằng ĐÚNG tập 54 tên ở cột "dò (phụ lục)" của bảng canh §5 — danh sách CHO PHÉP đóng băng, không phải danh sách cấm; Phụ lục F kế tiếp so tập và trả mã 1 thẻ `tap-do` khi lệch; thêm vào "ĐỎ KHI" của A5.
  **Phép kiểm đóng lớp:** `c_swap` và `c_swap2` ⇒ rc=1 `tap-do`; `c_all` ⇒ rc=0; đột biến: nới tập cho phép để chứa tên của `c_swap` ⇒ ca `c_swap` đỏ lại phải ĐỎ. **Giới hạn:** F là phụ lục băm — sửa F là đổi băm (§5 phụ lục); `HINT.patch` chỉ sửa chữ của A5/§5.

### LỚP 3 — `r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat` — **P3** — TÁI PHÁT (hẹp)

- HƯỚNG 22 / giả thuyết: r4 đã sửa hai biểu hiện lượt 3 chỉ ra ("ba ngưỡng" → hai; `f49_*`/`f50_*` ↔ bảng ánh xạ) nhưng vẫn khai một nhãn không khớp hiện vật.
- Lệnh: `grep -n -E '24 canh r2|24 canh' SPEC.md` [L504]; dựng `c_tq` (ba nháy cho 11 hàng r3) và đếm 55 mục lệch theo họ [L211, L214]; đọc `r4do/kq/bang_noi.txt` (43 dòng `r2_…` + 11 dòng `r3_…`).
- Output: ba chỗ — `118: (24 canh r2, vốn viết bằng chuỗi thoát, cũng lệch)`, `1035: | v4_tq | … | 11 canh r3, 24 canh r2, 20 mục cũ …`, `1622: … 55 mục lệch — 11 canh r3, 24 canh r2 và 20 mục cũ`. Đo `c_tq`: 35 canh lệch = 11 r3 + 24; 24 = **9 canh r1 + 15 canh r2** theo phân họ 16/27/11 của chính §5; 20 mục cũ (đúng 20 tên khai). Tức SỐ đúng, NHÃN sai: "canh r2" của §5 là 27 canh.
  Nguồn nhãn: cây đo của r4 đặt tên cả 43 canh r1 + r2 là `r2_<dò>` (`r4do/kq/bang_noi.txt`: 43 `r2`, 11 `r3`).
- kết luận: **LỖI** (cùng cơ chế với lượt 3: lời khai lấy từ tên cây đo thay vì đối chiếu với phân loại của chính đặc tả). Hậu quả: người đọc đối chiếu §5 (27 canh r2) thấy 24 ≤ 27 nhưng không dò ra 9 canh r1 nằm trong con số ấy.
- **Phương án:** đổi nhãn thành "24 canh cũ (9 r1 + 15 r2)" ở ba chỗ, kèm một câu giải thích nhãn `r2_…` của cây đo (HINT nhóm `# lop: r3-khai-ve-…`). **Phép kiểm:** `grep -n "24 canh r2" SPEC.md` rỗng; `11 + 24 + 20 = 55` giữ nguyên.

### LỚP 4 — `muc-tieu-moi-duong-vao-co-canh-mau-thuan-no-j` — **P3** — MỚI

- HƯỚNG 21 / giả thuyết: câu mục tiêu chưa giới hạn theo r1–r3 nên mâu thuẫn với nợ `j-chua-co-canh-wp698` của r4.
- Lệnh [L320]: đọc dòng 15 (`objective`), dòng 2110–2112 (§10), dòng 2272 (§11.1 (D) điểm 22).
- Output: dòng 15 cột 1517: `Mỗi đường vào có ít nhất một đột biến canh trong DOT_BIEN, chỉ đúng ca đích giết nó bằng TinHieuChotCa, bán kính 1; …` và, trong CÙNG ô, câu `(r4) Mọi ô mới gọi mã bị đo phải biến mọi BaseException … ở cả bốn chỗ gọi …; T5 có ô gặp tệp cũ và ô so dòng in; …`.
  Dòng 2272: `22. **Không thêm canh** cho các đường của r4: tổng giữ 54 canh, 470 đột biến; nợ j-chua-co-canh-wp698 (§10).` Dòng 2110–2112: `khối bắt ở doc, ở quét head, ở vòng main, hai lần gọi bộ ghi và phép so dòng in không có canh`.
- kết luận: **LỖI** (P3). Hậu quả: người đọc mục tiêu mà bỏ qua §10 sẽ đòi canh cho đường của r4 ⇒ vượt A5 (470), F (54) và S5 (300 dòng). Mọi cổng và số liệu đều nhất quán ở 54/470/300 nên không có ô nào của executor đổi.
- **Phương án:** giới hạn câu "Mỗi đường vào có ít nhất một đột biến canh …" theo "đường vào của r1–r3" và trỏ nợ `j-chua-co-canh-wp698` ngay tại câu ấy. **Phép kiểm:** câu còn đúng một lần và có giới hạn; A5/F/S5 không đổi.

## DRY-RUN HINT.patch

`$R/goi/HINT.patch` — sha256 `e4df532df8da8f73402f0254dfc4dd7d79d746ae265d99ee4c20eda265d062cf` (100 dòng; 4 nhóm mở bằng `# lop: <slug>`; 8 hunk). CHỈ sửa VĂN BẢN `ops/specs/ci-g5-cong-cu-va-tiep-r4.md`
(tiêu đề `--- ops/specs/ci-g5-cong-cu-va-tiep-r4.md`, không tiền tố); KHÔNG có mã `ops/cong_cu_test.py`, không đưa mã dò hay mã dựng ứng viên (Q14). Sinh bằng `evidence/scripts/make_hint.py` + `hint_edits.py`
(mỗi chuỗi cần thay có mặt ĐÚNG MỘT lần trong r4 — script `assert`).

```
$ T=$(mktemp -d -p "$R") && cp -a "$R/cay-kho" "$T/cay" && cd "$T/cay" && patch -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
… checking file ops/specs/ci-g5-cong-cu-va-tiep-r4.md · Hunk #1 succeeded at 1605. · Hunk #2 succeeded at 1824.        (nhóm a5-bang-noi-…)
… Hunk #1 succeeded at 1576. · Hunk #2 succeeded at 1588.                                                           (nhóm m2b-…)
… Hunk #1 succeeded at 115. · Hunk #2 succeeded at 1032. · Hunk #3 succeeded at 1619 (offset -10 lines).           (nhóm r3-khai-…)
… Hunk #1 succeeded at 12.                                                                                           (nhóm muc-tieu-moi-…)
done        rc=0
```
(đầu ra đầy đủ: `evidence/results/hint_dry_run.txt`). **rc = 0, 8/8 hunk, 0 fuzz** (offset −10 dòng ở một hunk chỉ do áp tuần tự bốn nhóm lên cùng một tệp, như các lượt trước).

Áp THẬT trên cùng bản sao (không `--dry-run`): rc=0, không `.rej`/`.orig`; tệp đặc tả 3352 → 3363 dòng (+19/−8 dòng theo `diff`), 349 771 → 353 025 byte; 0 dấu chéo ngược; 0 dạng bỏ-qua-CI;
bảng Markdown vẫn đều số ô; dòng `objective` vẫn là MỘT dòng bảng, nay có "của r1–r3" và trỏ nợ `j-chua-co-canh-wp698`; "24 canh r2" còn 0 chỗ; bản sao tạm đã xoá bằng `shutil.rmtree`.

Phạm vi HINT (nói thẳng điều nó KHÔNG làm): không viết lại Phụ lục F hay Phụ lục J (đổi mã dò là đổi băm — việc của r5); không rà mọi chỗ khác trong đặc tả còn viết "bốn chỗ gọi" (r5 phải rà `grep -n "bốn chỗ"`);
không đổi con số nào; nhóm `m2b-…` mô tả HỌ dò cần thêm bằng lời, không đưa mã của 11 dò `y4_*` (chúng nằm ở `evidence/scripts/blk_mine.py` làm tài liệu đo).

## NHẬT KÝ ĐO

Toàn bộ lệnh và đầu ra thật (62 mục `L<i>`, cắt 5000 ký tự mỗi mục): `evidence/logs/lenh_va_ket_qua.md`. Kết quả thô theo từng phép đo: `evidence/results/`. Mốc thời gian (giờ máy, 07-10-2026): bắt đầu 15:43Z; phép đo cuối (mảnh A5 0/8) xong 18:58Z; dọn dẹp và chốt tệp sau đó.
Thứ tự đo: tiền kiểm → trích phụ lục + băm → dựng ứng viên → Phụ lục F ×4 biến thể → J đầy đủ ×35 → 54 canh đầy đủ → tập đóng 401 + A (nhanh) → cây biến thể cho răng (J-NEM/T5/TV/A8/y4) →
Phụ lục I ×9 → SIGINT → A4-a ×2 + A4-b..f → bán kính cửa 232 mục cũ → bán kính đầy đủ 28 mục cũ → `y_*` ×28 → mảnh A5 0/8 → HINT.

## SANDBOX, DỌN DẸP

- Ghi CHỈ dưới `$R/goi/` và các thư mục `mktemp -d -p "$R"`; `cay-kho/` KHÔNG sửa tại chỗ (`git -C cay-kho status --short` rỗng, `HEAD` vẫn `42cd314c…`, `sha256sum cay-kho/ops/specs/ci-g5-cong-cu-va-tiep-r4.md` vẫn `b51b5ffa…`).
- Không mạng, không GitHub, không commit/push. Không in biến môi trường.
- Mọi tiến trình đo là `subprocess` có `wait`; bể đo tối đa 3 tiến trình. Nói thẳng hai chỗ không sạch: (i) vài lệnh lẻ rất ngắn (Phụ lục F ~1 s, một phép đếm, một lần chạy cửa `--tu-kiem-che-do` ~10 s) chạy CẠNH bể đang đủ 3 tiến trình, nên có vài giây tồn tại 4 tiến trình đo; (ii) hai lần tôi dừng bể giữa chừng (lần đầu bằng `pkill -f`, lần sau bằng `pgrep -f` + `kill`) — cả hai lần mẫu `-f` khớp luôn dòng lệnh của vỏ shell của tôi nên vỏ chết với mã 144, không mất dữ liệu đo (kết quả mỗi dò ghi tệp riêng, bể chạy tiếp được); các tiến trình mồ côi tự kết thúc rồi tôi mới sang bước kế. `python3 -B`, `PYTHONDONTWRITEBYTECODE=1`.
- Hai thư mục tạm của tôi (`tmp.sdxD2qA6d5` — giàn đo, hơn 470 MB với cây liên kết cứng — và `tmp.sdxd2qa6d5` — 3,6 MB rò ra do dò `x3_wr_ra_lower` hạ chữ thường đường ghi: một tác dụng phụ ĐÚNG như §1.9.5 mô tả) đã xoá bằng `shutil.rmtree` ở cuối.
- Đĩa: `$R` còn lại chỉ có `goi/` (VERDICT.md, HINT.patch, `evidence/`) cùng các hiện vật được giao.

