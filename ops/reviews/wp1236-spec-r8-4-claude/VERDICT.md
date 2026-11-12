Kết luận vòng 4: **approve**. Không còn P0, P1 hay P2. Có bốn P3; không cái nào chặn thi công.

**Trả lời câu hỏi chính: A14-S0 có đóng được lớp "cài đặt khác mà tưởng tương đương" không?**
- **Phần hằng: đóng.** Cả 91 đột biến kho sinh và 6 cái còn sống ở vòng 3 đều là sửa hằng, nên chết ở phép so byte của A14-S0.
- **Phần logic của `cu_phap_run`: chưa đóng bằng kiến trúc.** Phép kiểm `ast` của A14-S0 chỉ chặn được một đường nhận mới đi qua `re`. Nó không thấy việc biến đổi `b` trước khi gọi `fullmatch`. Tôi đo 17 biến thể giữ nguyên văn sáu hằng:
  - Mọi lỗi dễ mắc khi viết thật đều bị A14-S1 hoặc A14-S6 bắt: `strip`, `rstrip`, `splitlines`, bỏ chú thích, `.match`, `.search`, điều kiện `shell`, gọi qua hàm phụ.
  - Hai biến thể (`b.removesuffix(" &")`, `b.removeprefix("! ")`) qua A14-S0 và A14-S1 với 0 vế đổi. Chỉ A14-S6 bắt được. Vậy A14-S6 không chỉ là "phép đo PHỤ".
  - Một biến thể cố ý (`b.removesuffix(" || :")`) sống qua MỌI ca. Bash thật chạy `python ops/hong_test.py || :` cho rc 0 dù chương trình hỏng đã chạy.
  - Không phải P2: biến thể ấy là cố ý, không phải lỗi "tưởng tương đương". Nhưng cách sửa rẻ: chép nguyên văn hàm 11 dòng vào đặc tả và cho A14-S0 so `ast.dump`. Tôi khuyên sửa luôn ở bản này.

**Kiểm lại số liệu và harness:**
- Mọi script của phiên soạn tôi chạy trên bản sao, vì các script ghi JSON vào chính thư mục của chúng. Mọi JSON khớp byte với kho.
- Harness bản vòng 3 đã làm đúng cả năm điểm của J02: chạy nguyên byte, tệp ở đúng đường dẫn chữ, `bash` thật, `pwsh` giả chặt, ba lớp phân loại. Họ m-S15 nay (b) bắt 12/26, khớp số tôi đo trung thực ở vòng 3.
- Grammar K7-S vẫn đúng trong môi trường sạch: 26 072 lượt Bash thật, 0 thân được nhận mà nuốt lỗi.

**Bốn P3:**
- **K01:** lỗ logic nói ở trên.
- **K02:** vài con số và câu chữ lệch: "34 hạt" thực là 24; phép tính kích thước 540 thực là 555 (≈ 2185, vẫn dưới trần 2300); m-S0f vừa được khai "tương đương" vừa được tính có răng.
- **K03:** đợt B/C/D phải in nguyên văn dòng `GIOI_HAN`, nhưng API của module không xuất hằng ấy, nên chuỗi sẽ bị chép ra nhiều tệp.
- **K04:** một lượt A14-S6 (b) mất 2 phút 55 giây. Cách chạy đột biến kế thừa từ generation 1 chạy ca đích một lần trên bản gốc trước mỗi đột biến. Nếu 84 đột biến nhắm A14-S6 thì tổng thời gian vượt trần 5 400 s của mỗi bộ test trong registry CI (`.claude/dev/ci_dang_ky_test.py`). Trên Windows, ca này chạy bất cứ khi nào có `bash` trên `PATH`, nhưng lại gọi `/usr/bin/bash` ghi cứng.

Tôi không sửa gì trong `repo/`: HEAD vẫn `a1c81b8`, `git status` sạch. Script đo ở `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-4-claude/work/v4/` (`qua_s0.py`, `qua_s0.json`, `grammar_sach_v4.py`, `GHI_CHU_DO.md`).

```
# VERDICT wp1236 r8 vòng 4
spec_sha256: 5153cf17e3f5f73871fc0248db783919535b48df94b987f75594acd76924de8b
## Finding vòng 3 của tôi
- J01: ĐÓNG — Cả sáu cái sống vòng 3 (v3a, v3b, v3c, v3d, v3f, v3h) nay có trong bảng và bị bắt: `dot_bien_r8.py --sinh` chạy lại cho 91/91, cả sáu đều `giet`; chúng là sửa hằng nên A14-S0 cũng bắt theo cấu trúc. Câu "chốt cho LỚP… không phải chờ reviewer" đã bỏ. Phần logic còn hở: xem K01.
- J02: ĐÓNG — `sinh_r8.py` chạy nguyên byte (có assert tệp == thân), tệp ở đúng đường dẫn chữ, gọi `/usr/bin/bash` thật, `pwsh` giả thoát 99 khi lệch dạng, ba lớp phân loại; số 13/32 đã bỏ. Đo lại 61 530 / 2 647 / 0 / 0 / 0 và 9 / 40 / 42, JSON khớp byte; mỗi họ m-S15/m-S15b/m-S15p (b) bắt 12/26, khớp số trung thực vòng 3.
- J03: ĐÓNG — B1, C1, D1 đòi dòng `GIOI_HAN`, có m-B1b, m-C1b, m-D1b; A1 đòi cả `kiem-ho-so`, có m-A1c; A1-M2 sửa thành A14-S0…S6. Còn sót câu chữ (K02 g) và chuyện chép chuỗi ra nhiều tệp (K03).
- J04: ĐÓNG — `len(KT)` = 35; đếm được 158 = 53 + 91 + 8 + 6, khớp bảng; ước 2050–2200, trần 2300. Còn lệch nhỏ 540/555 và 34/24 (K02).
## Findings mới
- id: K01
  severity: P3
  vi_tri: K7-S dòng 384–388 ("chỉ dùng RE_DON.fullmatch và RE_ONG.fullmatch để nhận — KHÔNG có đường nhận thứ ba"); A14-S0 dòng 949 ("kiểm bằng ast: thân cu_phap_run chỉ tham chiếu RE_DON, RE_ONG"; m-S0g); dòng 955 và 1007–1012 ("Chốt cho LỚP là A14-S0", "A14-S6 là phép đo PHỤ")
  van_de: A14-S0 ghim hằng nhưng không ghim logic. Một module biến đổi `b` trước khi gọi `fullmatch` vẫn qua A14-S0 dù đọc theo cách chặt hay cách lỏng. Hai biến thể như vậy chỉ A14-S6 bắt được, và một biến thể cố ý sống qua mọi ca mà nuốt lỗi dưới Bash thật. Không chặn thi công: mọi biến thể kiểu lỗi dễ mắc khi viết thật đều đã bị bắt.
  bang_chung: `python3 -I work/v4/qua_s0.py` (qua_s0.json), 17 biến thể giữ nguyên văn khối SPEC.md:390–395. Kết quả theo nhóm — L6 `RE_DON.fullmatch(b.removesuffix(" &"))` và L7 `.removeprefix("! ")`: qua A14-S0 cả hai cách đọc; A14-S1 0 vế đổi; A14-S6a 24 lệch (chỉ ca này bắt); Bash thật trên `python ops/hong_test.py &` và `! python ops/hong_test.py` cho rc 0 và DA_CHAY. L14 `removesuffix(" || :")`: qua A14-S0; A14-S1, S2, S4, 52 vế g1, A14-S6a, 78 thân ci.yml@fe84620 và 6 VL-F đều 0; Bash thật trên `python ops/hong_test.py || :` (shell vắng) cho rc 0 và DA_CHAY. L3, L4, L5, L8, L9, L11, L12, L13, L16, L17 (`rstrip`, `strip`, bỏ chú thích, `splitlines`, CRLF, `|&`, dòng cuối, `; `, run không phải chuỗi ⇒ None, ống khi `shell != sh`): A14-S1 bắt 1–16 vế. L1 `RE_ONG.match` và L15 (hàm phụ): chỉ cách đọc chặt bắt được ở A14-S0, ngoài ra A14-S1/S6 bắt. L10 (tách theo ` | `): tương đương, 0 lệch.
  de_xuat: Chép nguyên văn hàm `cu_phap_run` của gram.py (11 dòng) vào đặc tả, và cho A14-S0 so `ast.dump` thân hàm (bỏ docstring) với bản trong test; khi đó m-S1…S5, m-S19, L1–L17 chết ngay ở A14-S0. Nếu không, ghi chính xác vị từ `ast`: tên toàn cục chỉ được thuộc {RE_DON, RE_ONG, type, str}; thuộc tính trên RE_* chỉ là `fullmatch`; đối số của `fullmatch` đúng là tên `b`; `b` được gán đúng một lần. Kèm theo, thêm đột biến logic m-S7g′/m-S7h′ (dạng L6/L7) nhắm A14-S6 để ca này có răng riêng, và bỏ chữ "PHỤ" hoặc ghi rõ A14-S6 là ca duy nhất bắt nhóm biến thể ấy.
- id: K02
  severity: P3
  vi_tri: dòng 955 (iv), (v); dòng 1005 và 1019–1020; dòng 1010–1011; dòng 778 và 792; dòng 342–343
  van_de: Bảy chỗ câu chữ hoặc con số lệch phép đo hay lệch nhau.
  bang_chung: (a) `hat` của sinh_r8.kho dài 24 (4 + 16 + 4), đặc tả ghi "34 hạt". (b) Chèn ký tự vào ống ba thành phần chỉ lấy mẫu `i % 3 == 0` (222/665), văn bản không nói lấy mẫu. (c) m-S0f "bỏ re.ASCII" được tính có răng, trong khi dòng 1019 nói chính đột biến ấy tương đương; đo được 0 lệch trên 61 530 đầu vào, 116 vế và 12 160 ký tự Unicode, nên nó chỉ chết vì A14-S0 so `flags`. (d) Câu "mọi đột biến của hằng (kể cả m-S6…S15…)" gộp nhầm m-S10, m-S11, m-S13 — chúng là logic điều kiện `shell`, không chết ở A14-S0; ngược lại m-S7d…j chỉ ghi ca đích A14-S6, dù là sửa hằng nên cũng chết ở A14-S0. (e) Dòng A14-S6 viết "v3a…v3h", gợi ý tám cái, nhưng chỉ có sáu (không có v3e, v3g). (f) Các mục test cộng lại 595 − 40 = 555, không phải 540, nên ước ≈ 2185 (vẫn ≤ 2200, dưới 2300, dư 5 %). (g) *Phạm vi của passed* vẫn chỉ nói CLI `kiem` in dòng `GIOI_HAN`, trong khi ca A1 đòi cả `kiem-ho-so`.
  de_xuat: Sửa từng chỗ: 24 hạt; ghi rõ lấy mẫu 1/3 (hoặc bỏ lấy mẫu rồi đo lại số đầu vào); m-S0f ghi là chốt cấu trúc và bỏ hoặc sửa đoạn "tương đương"; phân loại lại m-S10/S11/S13 và m-S7d…j; ghi đúng "v3a–d, v3f, v3h"; sửa 540 thành 555 (≈ 2185); thêm `kiem-ho-so` vào dòng 342.
- id: K03
  severity: P3
  vi_tri: *Phạm vi của passed* dòng 342–344; mục 6 "API xuất" dòng 321–331; B1, C1, D1
  van_de: Đợt B/C/D phải in nguyên văn dòng `GIOI_HAN`, nhưng API xuất không có hằng ấy và các đợt này không được sửa module. Chuỗi vì thế phải chép vào ba tệp cổng và các test, đúng bài học "nhiều bản sao trôi lệch" mà dòng 208 của chính đặc tả nhắc.
  bang_chung: Mục 6 liệt kê đúng sáu tên: kiem, kiem_waiver, kiem_ho_so_gate_output, kiem_so_luat, tap_head_land, la_run_land — không có hằng `GIOI_HAN`. Dòng 321 ghi "đợt B/C/D không được sửa module".
  de_xuat: A1 xuất hằng `GIOI_HAN` trong API. B/C/D nạp hằng ấy qua cùng cách nạp module; test B1/C1/D1 so với hằng của module, cộng một bản chép chữ trong test.
- id: K04
  severity: P3
  vi_tri: A14-S6 dòng 955; bảng disposition dòng 993–1005 (ca đích "A14-S0, A14-S6"); A14-S5 dòng 954 ("chạy khi bash/sh có trên PATH"); *Mọi đợt* dòng 1132 (chạy test trên tra-luat-win)
  van_de: Đặc tả không tính chi phí của A14-S6 (b) trong vòng đột biến, và ghi hai ca đích cho 84 đột biến trong khi bộ chạy kế thừa chỉ nhận một. Chọn A14-S6 làm ca đích thì tổng thời gian vượt trần 5 400 s của mỗi bộ test trong registry CI. Ngoài ra, trên Windows có Git Bash hoặc WSL, điều kiện "có trên PATH" làm A14-S5/S6 chạy, nhưng harness gọi `/usr/bin/bash` và `/bin/sh` ghi cứng, tạo symlink và dùng `pwsh` giả viết bằng `#!/bin/sh`.
  bang_chung: Một lượt A14-S6 (b) trên tham chiếu (`sinh_r8.py`) mất 2 phút 55 giây. Bộ chạy `chay_dot_bien` của generation 1 (`508d678:ops/gate_output_doi_chieu_test.py:1020–1036`) đòi tiền tố ca đích khớp đúng một ca và chạy ca đích trên bản gốc trước mỗi đột biến. 84 × ~175 s ≈ 4,1 giờ, lớn hơn `GIAY_TOI_DA_MOT_BO = 5400` (`.claude/dev/ci_dang_ky_test.py:791`). Chưa đo trên runner GitHub và trên Windows: KHÔNG ĐO ĐƯỢC.
  de_xuat: Ghi một ca đích cho mỗi đột biến: A14-S0 cho 84 đột biến sửa hằng; A14-S6 chỉ cho m-S7d…j và các đột biến logic của K01. Ghi rằng A14-S6 chạy (a) trước và dừng ngay khi có lệch, còn (b) chỉ chạy một lần trên module gốc; ghi kèm chi phí đã đo. A14-S5/S6 chỉ chạy khi `os.name == "posix"`; nền khác thì `BỎ QUA` có ghi dòng, bất kể PATH.
## Đã đo lại, khớp
- sha256 SPEC.md = HEAD:ops/specs/wp1236-r8.md = 5153cf17…; HEAD a1c81b8; `git status` sạch trước và sau; khối SPEC.md:390–395 trùng byte với gram.py:4–9.
- probes_r8: 109/109 vế âm bị từ chối, 41 rc 0, 36 nuốt thật, 7/7 dương. dot_bien_r8: 53/53. g1_qua_grammar: 52/52. Ba JSON khớp byte với kho.
- sinh_r8: 61 530 đầu vào, 2 647 được nhận, 0 lệch, 0 nuốt lỗi, 0 không chạy; 35 ký tự, 30 token, 16 tiền tố, 19 hậu tố, 11 toán tử. dot_bien_r8 --sinh: 91/91, 9 nuốt, 40 chỉ không chạy, 42 chỉ (a), lệch 24–1 440. Hai JSON khớp byte.
- census_r8 (d26b36f, fe84620, 8983e1b) khớp census_r8.txt: 30/24/6 và 25/5.
- Grammar K7-S đúng trong môi trường sạch (`work/v4/grammar_sach_v4.py`, bash 5.2.21 thật, `pwsh` giả chặt): 4 272 lệnh đơn + 80 ống, 26 072 lượt, 0 thân nhận mà rc 0 hay không chạy, 0 lệnh đơn bị từ chối sai.
- 158 đột biến = 53 + 91 + 8 + 6, khớp bảng disposition. `flags` của RE_DON và RE_ONG = 256 = `re.compile("", re.ASCII).flags`.
- Q-r8-1…5 và `tran_loi_goi_codex_A1_gen2` không đổi so với vòng 3: số đo vẫn khớp; trần 8 lời gọi theo dòng khai ADR-0052, 4 ≤ 8, hết trần thì đi ADR-0037; hướng đổi phương pháp không kéo theo hệ quả mới.
KET_LUAN: approve
```