Kết luận vòng 3: **changes_requested**. Còn một P2: kho sinh A14-S6 bắt được đúng 32 đột biến tôi nêu ở vòng 2, nhưng chưa phủ được cả lớp. Có thêm ba P3. Cả năm P3 của tôi ở vòng 2 đã đóng. Grammar K7-S vẫn đúng khi môi trường sạch, và mọi con số mới hoặc đã đổi đều khớp, trừ ba con số nhỏ ghi ở J02 và J04.

**P2 (J01):** kho sinh chỉ chèn ký tự vào một lệnh `python ops/ab.py w`, và chỉ ghép toán tử giữa hai lệnh đơn. Tôi viết thêm tám cài đặt không tương đương; sáu cái sống qua mọi ca của đặc tả (A14-S1…S6, 52 vế gen 1, 78 thân `run` của `ci.yml@fe84620`, sáu giá trị VL-F). Năm trong sáu cái nguy hiểm khi chạy Bash thật:
- `bash \S+\.sh` (mã regex rất dễ viết ra): nhận `bash ops/hong.sh||true||x.sh`, ra rc 0 dù chương trình hỏng đã chạy.
- Cùng dạng ấy cho `pwsh`.
- Nhận tuỳ chọn trước `P` ở dạng `bash`: `bash -n`, `bash -s` ra rc 0 mà không chạy gì.
- Nhận tuỳ chọn trước `P` ở dạng `python`: `python -h` ra rc 0 mà không chạy gì.
- Ống nhận thêm `|| LENH` ở cuối: `X | Y || Y` dưới `shell: bash` ra rc 0.

Vì vậy câu "Đây là chốt cho LỚP… không phải chờ reviewer chỉ cửa thứ ba" (dòng 998) rộng hơn phép đo. Đây cũng là lần thứ ba trong r8 của hình dạng "vá theo danh sách reviewer chỉ". Theo CLAUDE.md, lặp lần thứ ba thì nên đổi kiến trúc. Hai hướng sửa:
- **Khuyến nghị:** bỏ quyền "viết khác". Module chép nguyên văn hằng regex của tham chiếu, và có một ca so chuỗi.
- **Hoặc:** mở rộng kho. Tôi đã thử một kho mở rộng (829 356 đầu vào, khoảng 55 s): nó bắt cả 8 đột biến mới và cả 32 đột biến lớp I01.

**P3:**
- **J02:** vế (b) của A14-S6 yếu hơn lời mô tả.
  - `sinh_r8.py` đổi tên tệp, nên Bash không bao giờ thấy các ký tự `$ ` ' " \`. Chạy trung thực thì (b) bắt 12/26 đột biến `m-S15`, chứ không phải 7/26.
  - `bash` giả bỏ mọi tuỳ chọn `-*`, nên `bash -n` trông như truyền lỗi.
  - Con số "13/32 nuốt lỗi" thật ra là 6 nuốt thật cộng 7 chương trình không chạy (rc ≠ 0).
- **J03:** các đợt B/C/D phải in dòng `GIOI_HAN`, nhưng không có ca nào kiểm. Mục A1-M2 thiếu A14-S6.
- **J04:** đặc tả ghi "37 ký tự", danh sách của chính nó chỉ có 35. Đặc tả ghi "92 đột biến", đếm được 91. Ước "~60" dòng cho A14-S6 thấp hơn lượng mã tham chiếu cần chép.

Tôi không sửa gì trong `repo/`: HEAD vẫn `487cc87`, `git status` sạch. Các script đo nằm ở `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-3-claude/work/v3/`.

```
# VERDICT wp1236 r8 vòng 3
spec_sha256: 885017a688ae72fb479ee5e6234dd483f27182285b1f9d8a5b1ee3ee1adad1ee
## Finding vòng 2 của tôi
- I01: CÒN MỞ (một phần) — 32/32 đột biến lớp I01 nay bị A14-S6 (a) bắt (đo lại khớp `dot_bien_sinh_r8.json` từng byte). Nhưng câu "chốt cho LỚP" vẫn rộng hơn phép đo: kho chỉ phủ dạng `python` và cặp hai lệnh ⇒ J01.
- I02: ĐÓNG — Q-r8-4 (c) nay ghi `bash P.sh` vẫn hở, các biến của Python vẫn hở, 22/22 job J `not_measured`; đo lại 30 bước luật = 24 vắng + 5 `bash` + 1 `pwsh`, 0 `sh`.
- I03: ĐÓNG — "tag di động", số đếm khớp: checkout@v4 ×9, setup-python@v5 ×8, download-artifact@v4 ×2, upload-artifact@v4 ×3, 0 ghim 40 hex.
- I04: ĐÓNG — dòng 314–315 và *Phạm vi* có điều kiện môi trường; có dòng `GIOI_HAN` + m-A1b. Phần B/C/D thiếu ca ⇒ J03.
- I05: ĐÓNG — câu `F-ok` khai r8 thay G05 (đối chiếu văn bản G05 ở ISSUE.md:554); hai chốt khai là giới hạn + Q-r8-5; đo lại 0/39 và 28/28.
- I06: ĐÓNG — đủ năm câu: `8983e1b` khác ở hai bước luật (cả hai là bước luật), `:193`/`:226`, 14/24, 31/31, câu ai đo `F-ok`.
- H05 (vòng 1): ĐÓNG — theo I05.
## Findings mới
- id: J01
  severity: P2
  vi_tri: K7-S dòng 384 ("executor được viết khác, miễn tương đương; … ngoài kho ấy là giới hạn khai"); A14-S6 dòng 949 ((iii) chỉ chèn ký tự vào `python ops/ab.py w`; (i) chỉ cặp `A op B`); dòng 996–999 ("Đây là chốt cho LỚP … không phải chờ reviewer chỉ cửa thứ ba"); Phản biện dòng 1434
  van_de: Kho sinh không phủ được lớp. Không có ký tự lạ trong `P` của dạng `bash`/`pwsh`, không có tuỳ chọn giữa tên chương trình và `P`, không có toán tử sau ống. Sáu cài đặt không tương đương sống qua MỌI ca của đặc tả, năm trong số đó nguy hiểm dưới Bash thật. Đây là lần lặp thứ 3 trong r8 của hình dạng "vá theo danh sách reviewer chỉ".
  bang_chung: `python3 -I work/v3/song_sot_v3.py` ⇒ 6/8 sống, mỗi cái có A14-S1 0 đổi lý do, A14-S2 0 hỏng, 0/52 vế gen 1 được nhận, A14-S6a 0/11 838 lệch, 0/78 thân `ci.yml@fe84620` lệch, 0/6 VL-F hỏng. Sáu cái sống: v3a `bash \S+\.sh`, v3b `pwsh -NoProfile -File \S+\.ps1`, v3c `bash(?: -[a-z]+)* P.sh`, v3d `python(?: -[A-Za-z]+)* P.py`, v3f ONG thêm `( \|\| LENH)?` ở cuối, v3h `| ! LENH`. `work/v3/bash_that_v3.py` (tệp dựng đúng tên, /usr/bin/bash thật, env sạch): `bash ops/hong.sh||true||x.sh` (shell vắng) rc 0, DA_CHAY; `pwsh -NoProfile -File ops/hong.ps1||true||x.ps1` rc 0, DA_CHAY (pwsh giả, `||` do bash thật); `bash -n ops/hong.sh`, `bash -s ops/hong.sh`, `python -h ops/hong_test.py` rc 0, KHÔNG chạy; `X | Y || Y` (`shell: bash`) rc 0, DA_CHAY; v3h rc 2 (lỗi cú pháp, vô hại). Đối chứng `work/v3/kho_mo_rong.py`: 57 hạt (5 LENH + 25 ống đôi + 27 ống ba) × chèn 35 ký tự ở mọi vị trí + chèn 24 token ở mọi ranh giới + thay mỗi ` | ` bằng 11 toán tử = 829 356 đầu vào, ~55 s ⇒ bắt 8/8 cái trên và 32/32 lớp I01.
  de_xuat: (A, khuyến nghị, đóng theo kiến trúc) bỏ quyền "viết khác". Module chép NGUYÊN VĂN `P`, `W`, `DANG`, `LENH`, `RE_DON`, `RE_ONG` (kèm `re.ASCII`) và sáu bước `cu_phap_run`. Một ca so `pattern`/`flags` của module với bản chép trong test, kèm đột biến sửa một ký tự mỗi hằng; A14-S6 giữ làm phép đo phụ. (B) giữ quyền viết khác nhưng mở rộng kho như đối chứng trên (hạt giống gồm ba dạng DANG và ống 2–3 thành phần; chèn ký tự/token ở mọi vị trí của MỌI hạt; thay dấu tách ống), thêm v3a–v3f làm đột biến có ca đích A14-S6, và sửa dòng 998–999 cho đúng phạm vi. Cả hai hướng: tính lại `kich_thuoc`.
- id: J02
  severity: P3
  vi_tri: A14-S6 vế (b) dòng 949; dòng 997 ("13/32 còn có thân được nhận mà Bash thật nuốt lỗi"); `sinh_r8.py` `chay_tung_thanh_phan`
  van_de: (b) không chạy chính thân được nhận. (1) Harness đổi tên mọi token tệp thành `ops/_t<i>.<đuôi>`, nên ký tự lạ trong `P` bị xoá trước khi Bash thấy. (2) `bash` giả bỏ MỌI đối số `-*`, nên `bash -n`/`bash -s` trông như truyền lỗi. (3) "13/32 nuốt lỗi" gộp nuốt thật với không chạy (đúng phân biệt H03).
  bang_chung: `work/v3/phan_loai_13.py`: 6/32 nuốt thật (m-S7d…i, rc 0 + DA_CHAY); 7/32 là m-S15[; & | ( ) < >], chỉ "không chạy" rc 2/126/127, 36 thân mỗi cái. `work/v3/b_trung_thuc.py` (tệp dựng đúng đường dẫn chữ): (b) bắt 12/26 m-S15, so với 7/26 khi đổi tên (thêm `$` 24/36; backtick, `'`, `"`, `\` 36/36). `sinh_r8.chay_tung_thanh_phan("bash -n ops/hong.sh\n", None)` ⇒ `[(0, 1, True)]`; bash thật ⇒ rc 0, DA_CHAY False (`bash -s` cũng vậy).
  de_xuat: (b) dựng tệp hỏng đúng đường dẫn chữ, không đổi tên. Dùng /usr/bin/bash thật cho `bash P.sh` (P.sh = `touch DA_CHAY; exit 1`). `pwsh` giả CHẶT: chỉ nhận đúng `-NoProfile -File <tệp>`, lệch ⇒ exit 99. Sửa dòng 997 thành "6/32 nuốt thật + 7/32 không chạy (rc ≠ 0)", hoặc ghi số đo lại sau khi sửa harness (bản trung thực của tôi: 6 + 12 = 18/32 bị (b) bắt).
- id: J03
  severity: P3
  vi_tri: *Phạm vi của passed* dòng 342–344; bảng B/C/D dòng 1052–1105; A1-M2 dòng 829
  van_de: Luật "đợt B/C/D in lại nguyên văn dòng `GIOI_HAN` trong thông điệp ĐẠT" không có ca nào ở B1–B14, C1–C9, D1–D10, và không đột biến (L3). Không nói CLI `kiem-ho-so` của A1 có in dòng ấy không. A1-M2 liệt kê "A14-S1…S5", thiếu A14-S6 và các đột biến của nó.
  bang_chung: `grep -n GIOI_HAN SPEC.md` ⇒ chỉ dòng 342 (luật), 892 (ca A1), 1437 (Phản biện); dòng 829 "ca A1–A23, A14-S1…S5, A15d".
  de_xuat: Thêm vế vào B1, C1, D1 đòi dòng `GIOI_HAN` nguyên văn khi ĐẠT, kèm đột biến bỏ dòng ở mỗi cổng. Nêu rõ `kiem-ho-so` có in hay không. Sửa A1-M2 thành A14-S1…S6.
- id: J04
  severity: P3
  vi_tri: dòng 949 ("37 ký tự"); `nang_tran.can_cu` dòng 787 ("92 đột biến"); `kich_thuoc` dòng 774 ("A14-S6 kho sinh + 32 đột biến (~60)")
  van_de: Ba con số lệch phép đo.
  bang_chung: `len(sinh_r8.KT)` = 35, khớp đúng danh sách ở dòng 949 (27 dấu + 8 ký tự khác). Bảng disposition đếm được 53 + 6 + 32 = 91 đột biến. Mã tham chiếu cần chép: gram.py 25 + sinh_r8.py 93 + DB_SINH 46 = 164 dòng, so với ước ~60 (tổng 2022 vẫn dưới `tran_moi` 2150).
  de_xuat: Sửa 37 → 35 và 92 → 91 (hoặc ghi rõ đột biến thứ 92 là cái nào). Tính lại ước A14-S6 theo hướng chọn ở J01.
## Đã đo lại, khớp
- sha256 SPEC.md = ops/specs/wp1236-r8.md = 885017a6…; HEAD 487cc87; d26b36f..HEAD chỉ đổi ops/specs, ops/reviews; `git status` sạch trước và sau.
- sinh_r8.py: 11 838 đầu vào (1 973 thân × 3 shell × 2), 86 nhận, 0 lệch, 0 nhận mà nuốt lỗi; 5 LENH, 11 toán tử, 16 tiền tố, 19 hậu tố.
- dot_bien_r8.py --sinh: 32/32 bị bắt ở (a), lệch 30–150 đầu vào mỗi đột biến; chỉ số `co_than_nhan_ma_nuot_loi` = 13 (phân rã xem J02).
- probes_r8.py: 109 = 106 chạy shell (41 rc 0 = 36 nuốt thật + 5 không chạy; 65 rc ≠ 0) + 3 chỉ grammar (g_pwsh_shell, g_run_khong_phai_chuoi, g_run_khong_phai_chuoi_pwsh); 7/7 dương. dot_bien_r8.py 53/53; g1 52/52 bị từ chối. Mọi JSON khớp byte với kho.
- census_r8.py khớp từng dòng census_r8.txt (30/24/6; 8983e1b 25/5). Trên fe84620: 24 vắng + 5 bash + 1 pwsh; 24/24 bước đo được là `python`, 14/24 có đối số. ci.yml fe84620 = d26b36f.
- `cai_actionlint.sh` GITHUB_PATH `:193` @fe84620, `:226` @d26b36f; `cai_cong_cu.sh:78`.
- Provenance d26b36f: 39 tệp; 31/31 tệp ci.yml push có J = đúng 22 tên `JOB_BAT_BUOC`, run sớm nhất 40268583940; 0/39 checkout passed ≠ head; 28/28 `workflow_definition` passed khớp blob tại SHA checkout.
- numstat 08bcb51..508d678 = 1 + 539 + 1080 = 1620; ước 1620 + 10 + 392 = 2022 ∈ 1900–2050; `tran_moi` 2150.
- A20 (e′) + m-A20i có răng riêng (vế (e) vẫn bị chốt chồng miền bắt khi gỡ chốt đếm miền mở).
- Grammar K7-S đúng trong môi trường sạch (`work/v3/grammar_sach_v3.py`, bash 5.2.21 thật cho `bash P.sh`, pwsh giả chặt, không đổi tên tệp): 4 272 lệnh đơn (ba dạng DANG; P gồm `.` `..` `./b` `x.py`; W gồm `-c -e -s -n -h -i -m -o pipefail -- - = : exit true if then done time`) và 80 ống 2–3 thành phần, 26 072 lượt × thành phần hỏng ⇒ 0 thân nhận mà rc 0 hay không chạy, 0 lệnh đơn bị từ chối sai.
- `tran_loi_goi_codex_A1_gen2`: dòng khai ADR-0052 ⇒ trần 8 (ADR-0055 chỉ áp khi có dòng khai riêng); điều kiện lượt 2–4 khớp nguyên văn ADR-0052:23–24; 4 ≤ 8; hết trần ⇒ ADR-0037.
KET_LUAN: changes_requested
```