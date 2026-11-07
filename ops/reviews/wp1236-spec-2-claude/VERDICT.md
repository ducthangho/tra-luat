Review vòng 2 xong. Kết luận: **changes_requested**. r2 đóng được cả 13 finding vòng 1 của tôi, nhưng sinh ra một lỗ P1 mới và sáu lỗ P2.

**Lỗ P1: K7 không bao giờ đạt.** K7 đòi provenance có bước tên `Run <dòng CMD>`. Thực tế `ci.yml` có 78 bước `run:` và cả 78 đều có `name:` riêng. Trong 7569 bước thành công của 34 tệp provenance, không bước nào mang tên dạng `Run <lệnh>`.
- Hệ quả: không job nào ra `passed`, nên đường dương của L8, L-7 và D2b đều chết. L-7 trên thực tế chỉ còn kiểm định dạng URL của `owner_waived`.
- Fixture `F-ok` lại dựng đúng tên `Run <lệnh>` không có thật, nên mọi ca test sẽ xanh trong khi dữ liệu thật không bao giờ qua.

**Các con số:** phần lớn tái lập được. Có hai chỗ lệch:
- Bảng dạng giá trị cộng ra 68, không phải 64. Ô "chuỗi khác" thật ra là 1, không phải 5.
- L8 hồi tố là 36 hồ sơ chứ không phải 35. `pr679` nằm trong danh sách miễn trừ L5 nhưng băm đã lệch, nên đang bị kiểm đủ luật.

Kho không bị sửa. Các script đo nằm dưới `work/` (`do_r2.py`, `neo_run.py`, `dang_tep.py`, `thu_luat_log_that.py`). Clone lần này không nông (`.git/shallow` không có mục nào).

```
# VERDICT wp1236 r2 vòng 2
spec_sha256: 570b10851be95875662da56df3dcb6d6f028429f4cb2e2f1291c3604eb618a0c
## Finding vòng 1 của tôi
- F01: ĐÓNG — định nghĩa lời khai nay fail-closed với tập token ĐÓNG; mapping/list/chuỗi tự do ĐỎ `dinh_dang_loi_khai`; ca A15/C6 có đột biến (phần dư nhỏ về chuẩn hoá tên khoá: G09d).
- F02: ĐÓNG — sổ `LUAT_PHIEN_BAN` chỉ-thêm, tệp kiểm bằng phiên bản nó khai, A9(b) phủ đúng kịch bản sửa LUAT; nhưng tính "chỉ-thêm" chưa có cổng canh (G07).
- F03: ĐÓNG — (a) `owner_waived` được nhận; (b) Q7 khả thi: cả 28 tệp provenance của run push đo được đều 23 job, 0 job Windows; (c) có đường sửa cho hồ sơ cũ. Mục tiêu "trạng thái hợp lệ phải đạt được" bị G01 và G03 phá lại.
- F04: ĐÓNG — K5 lấy `name`/`labels`/`conclusion` từ provenance; ca A4a/b có đột biến.
- F05: ĐÓNG — bốn loại dấu hiệu có cách biểu diễn và cách kiểm; còn hở luật viết lại đuôi regex và cách nhận diện bước (G11).
- F06: ĐÓNG — D2b nạp module từ `origin/master`, có ca D7; nhưng phụ thuộc `_url_hop_le` của module chưa được thiết kế (G04).
- F07: ĐÓNG — có *Neo run* và D2b so `head_sha` với `merge_commit`; không còn đường neo vào run khác mà vẫn ĐẠT. Hình dạng `moc_10_2_2` thì không neo được (G05).
- F08: ĐÓNG — vế dương thay provenance bằng `F-ok`; Q2 nói rõ #1127 chỉ ĐẠT nhờ miễn trừ.
- F09: ĐÓNG — 45 = 44 + 1 đúng; còn lỗi số mới ở bảng dạng giá trị (G08).
- F10: ĐÓNG — 49/49 = 32 + 17, đo lại khớp; ước lượng đợt B đã cộng miễn trừ.
- F11: ĐÓNG — các vế a, c, d, e, f, g đã sửa; vế (b) và (h) còn sót, ghi ở G09a và G08 (đều P3).
- F12: ĐÓNG — ước lượng lại theo tỷ lệ, kèm `nang_tran` cho đợt A (rủi ro còn lại: G10).
- F13: ĐÓNG — mục *Phạm vi của `passed`* ghi "điều kiện CẦN"; `labels` đưa vào K5.
## Findings mới
- id: G01
  severity: P1
  vi_tri: K7 (dòng 175–177); F-ok (dòng 436); A13 (dòng 456); chua_do_duoc 3 (dòng 600–601)
  van_de: K7 đòi provenance có bước tên `Run <dòng CMD>`, nhưng mọi bước `run:` của `ci.yml` đều có `name:` riêng, và `ten_du_kien` trả đúng `name:` ấy, nên K7 không bao giờ đạt ⇒ không job nào `passed` ⇒ đường dương của L8, L-7, D2b chết; fixture `F-ok` dựng tên `Run <lệnh>` không có thật nên test xanh còn dữ liệu thật thì không bao giờ qua.
  bang_chung:
    · `ci.yml` @3163f4d: 78 bước `run:`, số bước không có `name:` = 0.
    · Quét 34 tệp `ci_provenance/1`: 7569 bước success (trừ Set up/Complete job); số bước tên `Run <lệnh>` (không phải `Run actions/…`) = 0.
    · `ops/ci_provenance.py:208-212`: `ten_du_kien` trả `s["name"]` khi bước có `name`.
    · Ví dụ pr1127, job `gate (ubuntu-latest)`: các bước tên 'eol-policy selftest', 'golden-test', 'release-check full'…
    · Dòng lệnh đầu (CMD) của 3 bước LUAT là `set -euo pipefail` ('tl selftest (co bang chung exact-identity)', 'lease-publish selftest', bước cgroup chứa gate_lifecycle), nên CMD không mang danh tính bước.
    · chua_do_duoc 3 ghi "chưa đo", nhưng đo được offline ngay.
  de_xuat:
    · `tom` ghi cho mỗi bước của luật: số thứ tự bước REST + tên bước REST (lấy từ `jobs.json`, ghép nhóm log ↔ bước như `ci_provenance.ghep_buoc`) + các dòng lệnh chứa nhãn.
    · `kiem` đòi bước cùng số/tên trong `provenance.buoc` có `conclusion: success`, và đòi nhãn LUAT có mặt trong các dòng lệnh đã ghi.
    · `F-ok` chép tên bước THẬT từ một provenance thật (vd `pr1231`), không tự đặt `Run <lệnh>`.
    · Thêm ca chạy K7 trên provenance thật `pr1231`; đột biến quay về so `Run <CMD>` ⇒ ca ĐỎ.
- id: G02
  severity: P2
  vi_tri: K7 (dòng 178–180); Q6 (dòng 580–581); *Phạm vi của `passed`* (dòng 196)
  van_de: Tiền đề của Q6 — bước `run:` chạy dưới `bash -e -o pipefail` nên `success` là bằng chứng rc 0 — sai so với `ci.yml`; rc gián tiếp chỉ đúng nhờ một bất biến không ai canh.
  bang_chung:
    · `ci.yml` không có `defaults`. Trong 36 bước `run:` chứa nhãn LUAT, 26 bước không khai `shell:`, nên GitHub chạy `bash -e {0}` (không pipefail); 9 bước `shell: bash`, 1 bước `pwsh`.
    · Hôm nay mỗi bước là một lệnh `python …` đơn, hoặc tự mở đầu bằng `set -euo pipefail`, nên rc vẫn truyền ra. Không gì chặn một bản `| tee` sau này.
    · Bước LUAT của `chuan-bi` ('phan loai diff', chạy `ops/ci_duong_nhanh.py`) mang `continue-on-error: true`, nên `success` của job không chứng minh rc 0. REST trả `conclusion` gì cho bước ấy khi nó lỗi thì KHÔNG ĐO ĐƯỢC offline.
  de_xuat: Sửa câu Q6 cho đúng: rc gián tiếp chỉ đúng khi bước là lệnh đơn hoặc tự bật pipefail. Ghi rõ không cổng nào canh điều đó và trình lại Q6 với số đo này. Hoặc đòi `tom` ghi `shell`/`continue-on-error` của bước (đọc workflow tại head) và để `kiem` hạ bước có `continue-on-error` hay ống không pipefail xuống `not_measured`.
- id: G03
  severity: P2
  vi_tri: Bảng luật, dòng L-7 (dòng 237); Q7 (dòng 583–585); B7 (dòng 485); Q8 (dòng 587–588)
  van_de: Q7 bảo hồ sơ ghi run Windows là `not_measured`, nhưng L-7 đòi MỌI khoá lời khai của hồ sơ landed phải dương hoặc `owner_waived`, nên làm theo Q7 là TRUOT, còn xoá lời khai `not_measured` trung thực thì lại DAT (khuyến khích không ghi).
  bang_chung:
    · Trích L-7: "MỌI khoá lời khai phải là lời khai dương … hoặc `owner_waived` có neo. `not_measured` không cho hồ sơ landed".
    · B7: "một lời khai `not_measured` ⇒ `TRUOT`", với đột biến m-B7b canh đúng điều đó.
    · Q7: "run Windows khai `not_measured` hoặc `owner_waived`".
    · Hình dạng này có thật trong kho: `pr1029` mang cả `measured` lẫn `not_measured`.
  de_xuat: L-7 chỉ đòi các lời khai NEO vào run land (head = `merge_commit`) phải dương hoặc `owner_waived`, và cần ≥ 1 lời khai như thế. Lời khai cho run khác chỉ cần đúng định dạng (L8). Thêm ca: hồ sơ landed có lời khai dương cho run land cộng `not_measured` cho run Windows ⇒ DAT.
- id: G04
  severity: P2
  vi_tri: *Lời khai*, gạch `owner_waived` (dòng 218–219); D2b nạp module (dòng 240–245); A-M1 (dòng 398); B-M1 (dòng 407)
  van_de: Module mới cần `_url_hop_le` của `ops/kiem_ho_so_land.py`, trong khi đợt B cho `kiem_ho_so_land` nạp ngược module mới. Đặc tả không nói chiều phụ thuộc, nên có vòng nạp; và D2b chỉ chép MỘT tệp module ra thư mục tạm, nên phụ thuộc hoặc không nạp được (KHÔNG ĐO ĐƯỢC vĩnh viễn) hoặc rơi về cây làm việc (thủng canon, đúng thứ F06 đã đóng).
  bang_chung:
    · `_url_hop_le` chỉ có ở `ops/kiem_ho_so_land.py:46`.
    · `_canon` (`packet_loop.py:2420–2438`) chỉ chép các tệp trong danh sách vào thư mục tạm.
    · Đặc tả: "Hai cổng `ops/` nạp module cùng thư mục bằng `importlib`". Nếu cả hai phía nạp ở mức module bằng `spec_from_file_location`, mỗi lần nạp tạo module mới và nạp phía kia ⇒ đệ quy không dừng.
  de_xuat: Chốt chiều phụ thuộc: module nhận hàm kiểm URL qua tham số, hoặc nạp `_url_hop_le` LƯỜI bên trong hàm. D2b chép cả hai tệp từ `origin/master`. Thêm ca D8 (thư mục tạm có module + phụ thuộc ⇒ D1 dương chạy được) và ca B9 (nạp `kiem_ho_so_land` không đệ quy), mỗi ca kèm đột biến.
- id: G05
  severity: P2
  vi_tri: *Neo run cho lời khai* (dòng 222–229); A16 (dòng 459); D2b (dòng 238)
  van_de: Luật "`run_id` gần nhất ở mapping chứa hoặc tổ tiên" không neo được hình dạng `moc_10_2_2`/`bon_moc_10_2_2` (run nằm ở mapping ANH EM, vd `ci_master.run_id` — đúng chỗ D2b neo cho cùng hình dạng), nên ra `thieu_run_id`; đặc tả không nói tác giả phải đặt `run_id` ở đâu, mà đặt ở gốc thì mọi lời khai thiếu `run_id` riêng (kể cả pre-merge) bị neo vào run ấy; head cũng được lấy độc lập với chỗ lấy `run_id`.
  bang_chung:
    · `python -I work/neo_run.py`: 45 lời khai dương; 30 có `run_id` cùng mapping (sha khớp head provenance ở mọi ca có provenance); 15 không có `run_id` ở bản thân lẫn tổ tiên.
    · 15 lời khai ấy đều thuộc hình dạng `moc_10_2_2`, có `merge_commit` ở tổ tiên: pr1029, pr1040, pr1051, pr1064, pr1155, pr1193, pr1197, pr631 (×2), pr791, pr793, pr870, pr889, pr896, pr945.
    · `pr1155` có `ci_master.run_id = 41425851232` ở mức gốc, đúng lược đồ M8 mà D2b đọc.
  de_xuat:
    · Định nghĩa neo cho `moc_10_2_2`: lấy `ci_master.run_id` anh em, như D2b. Hoặc đòi `run_id` nằm NGAY trong mapping chứa lời khai và cấm thừa kế từ mức gốc.
    · Head lấy từ CHÍNH mapping đã cấp `run_id`.
    · Thêm vế A16(g) cho hình dạng `moc_10_2_2` + `ci_master`, và vế A16(h): `run_id` ở gốc không được neo lời khai pre-merge.
- id: G06
  severity: P2
  vi_tri: *Lời khai*, gạch `owner_waived` (dòng 218–219); *Đường sửa* (dòng 257–258); B7 (dòng 485); A17 (dòng 460)
  van_de: Neo `owner_waived` chỉ là một URL đúng tiền tố và mảnh, yếu hơn §10.2.3 (owner, exact SHA, context/OS, lý do, phạm vi) và yếu hơn chính câu chữ của đặc tả ("có neo comment chủ kho"); cộng với G01, mọi hồ sơ landed sẽ đi đường này, nên L-7 trên thực tế chỉ còn kiểm định dạng URL.
  bang_chung:
    · `_url_hop_le` (`kiem_ho_so_land.py:46`) chỉ kiểm `startswith(TIEN_TO_URL)` và có một trong `MANH_URL` — comment của bất kỳ ai cũng qua.
    · `docs/PROTOCOL_DA_PHIEN.md:974-975` đòi waiver bền của owner kèm "nguồn/actor, exact SHA, context/OS, lý do, phạm vi/hạn".
    · Mục N2 của chính đặc tả đòi bắt miễn trừ không có "comment chủ kho nêu exact SHA".
  de_xuat: Đòi cùng chuỗi `owner_waived` chứa một SHA 40 hex bằng head của run được neo (hoặc `merge_commit`), kèm URL. Ghi thẳng rằng actor không kiểm được offline (đưa vào `ngoai_pham_vi`), và sửa câu "neo comment chủ kho" thành "neo URL". Thêm vế A17(c) URL đúng nhưng thiếu/sai SHA ⇒ ĐỎ, kèm đột biến. Hoặc trình mức neo này thành một Q riêng cho chủ kho.
- id: G07
  severity: P2
  vi_tri: Thiết kế mục 1, sổ luật (dòng 124–130); A9 (dòng 452)
  van_de: Bất biến "sổ chỉ-thêm, không sửa phiên bản cũ" không có phép đo nào làm nó ĐỎ (trái L3).
  bang_chung:
    · A9 chỉ thử (a) băm không có trong sổ và (b) thêm v2. Không ca nào kiểm `khoá == sha256(json.dumps(giá trị))` cho từng mục, cũng không có bản chép kỳ vọng tập khoá trong test (như cơ chế `MIEN_TRU`).
    · Khoá ghi cứng ⇒ sửa `LUAT_v1` tại chỗ làm đổi âm thầm ngữ nghĩa của mọi tệp khai v1.
    · Khoá tính lúc nạp ⇒ sửa tại chỗ vô hiệu âm thầm mọi tệp cũ.
  de_xuat: Thêm ca A19: (a) mọi mục có `khoá == băm(giá trị)`; (b) test chép riêng tập khoá + băm `LUAT_v1`. Đột biến m-A19a sửa một regex của `LUAT_v1` trên bản sao ⇒ ĐỎ; m-A19b bỏ phép tự kiểm băm ⇒ ĐỎ.
- id: G08
  severity: P3
  vi_tri: Bảng dạng giá trị (dòng 69–78); dòng 85–87; L8 hồi tố (dòng 263); kich_thuoc đợt C (dòng 371); Q1 (dòng 565); bảng ba dạng tệp, dòng `tu_do` (dòng 91–92, 98)
  van_de: Số lệch.
  bang_chung:
    · `python -I work/do_r2.py .` ⇒ measured 44 · passed 1 · not_measured 3 · chuỗi khác **1** · mapping 9 · list 6 = 64. Đặc tả ghi "chuỗi khác 5", tổng thành 68 ≠ 64; 4 giá trị thừa đúng bằng số giá trị của ba khoá phi-lời-khai.
    · `pr679-wp678` có trong `MIEN_TRU_CUTOVER` nhưng băm lệch: cổng in "MẤT MIỄN TRỪ … ĐẠT", nên nó bị kiểm đủ luật. Nó mang `$.post_merge_checks[0].moc_gate_output` dạng list ⇒ L8 ĐỎ. Vậy L8 hồi tố = **36**, `MIEN_TRU_L8` = 36 mục, và chỉ 8/9 hồ sơ thật sự được L5 miễn.
    · `tu_do` theo định nghĩa ghi trong đặc tả ra 13 hồ sơ (11 chỉ có dạng này), không phải 16. Câu "hai reviewer xác nhận cách đếm này" gán sai: F11h vòng 1 của tôi báo KHÔNG tái lập được.
  de_xuat: Sửa 5→1, 35→36 (cả kích thước đợt C và Q1), 16→13. Bỏ câu "hai reviewer xác nhận". Ghi rằng tập L5 có hiệu lực phải tính theo BĂM, không theo tên.
- id: G09
  severity: P3
  vi_tri: Bảng luật, dòng L8 (dòng 236); dòng 55 và 187; D2b (dòng 244); *Khoá lời khai* (dòng 208–211); dòng 20, 595, 612–613
  van_de: Một số câu chưa đúng hoặc chưa chặt.
  bang_chung:
    (a) "Thư mục provenance vắng ⇒ KHÔNG ĐO ĐƯỢC theo L4" chỉ đúng khi có lời khai `measured` hoặc khoá `positive` (`land_evidence_nguon.py:255`). Hồ sơ chỉ có `passed`/`owner_waived` thì không qua L4, và L8 chưa định nghĩa kết quả cho ca này.
    (b) "Log đầy đủ không nằm trong kho" quá rộng: có 124 tệp `.log` dưới `ops/land/`, vd `pr1155-wp1143-provenance` chứa log đầy đủ dạng `gh run view --log` (150–250 KB) của `chuan-bi`/`gate-ops` cho 3 run.
    (c) D2b "không đọc được module" vào `thieu` cùng rc 12 với vi phạm, trong khi `_canon` dùng `RC_STATE` 8 — hai trạng thái bị gộp làm một.
    (d) Tên khoá `gate output`, `GateOutput`, `gateoutput` lọt định nghĩa lời khai, vì `casefold` vẫn đòi `_` hoặc `-`.
    (e) Tại `4c2b72c` không có `ops/reviews/wp1236-spec-1-*` lẫn `ops/specs/wp1237-r1.md` — câu chỉ vị trí phải đúng ở cả hai phía của merge.
  de_xuat:
    · (a) Ghi kết quả cho ca thư mục vắng kèm một ca test.
    · (b) Sửa câu và dùng log có sẵn để đo một phần chua_do_duoc 2.
    · (c) Tách lý do KHÔNG ĐO ĐƯỢC bằng mã riêng.
    · (d) So khoá sau khi bỏ mọi ký tự không phải chữ/số (chứa `gateoutput`).
    · (e) Viết "tìm ở master trước, chưa thấy thì ở nhánh X" và neo bằng băm.
- id: G10
  severity: P3
  vi_tri: kich_thuoc và `nang_tran` (dòng 367–384); F-ok (dòng 431–436)
  van_de: Trần 750 dòng của đợt A có khả năng vượt; `can_cu` chưa có số đo numstat như ADR-0053 đòi.
  bang_chung:
    · Numstat lúc tạo tệp của cổng tương tự gần nhất: `ci_provenance` 393 + 656 = 1049; `land_evidence_nguon` 279 + 318 = 597; `kiem_ho_so_land` 140 + 263 = 403.
    · Hai nguyên mẫu `danh_gia_gate.py` + `tom_gate_output.py` đã là 196 + 103 dòng, trước khi thêm K1–K9, lời khai, Neo run và CLI.
    · `F-ok` buộc chứa đủ 18 bước của `gate (`, vì đó là job DUY NHẤT có `JSON_OK` — không còn "tối giản".
    · ADR-0053 dòng 26–29 tự ghi +721 dòng "đã là quá lớn".
  de_xuat: Cân nhắc tách `tom` (sinh tệp) khỏi `kiem` (+ lời khai + Neo run) thành A1/A2, hoặc chọn job `JSON_OK` nhỏ hơn cho `F-ok`. Ghi tiền lệ +721 vào `can_cu`.
- id: G11
  severity: P3
  vi_tri: Thiết kế mục 1, gạch `fullmatch` (dòng 131–134); `F-luat` (dòng 437–438); A5 (dòng 448)
  van_de: "Viết lại cho đủ dòng" không có luật cho phần đuôi, và cách nhận diện bước của LUAT gốc (`tim_buoc` dò chuỗi con trên MỌI dòng lệnh; `TL_SELFTEST` nhận diện bằng output) không có trong mô hình mới.
  bang_chung:
    · LUAT gốc có 8 regex dòng không neo `$`: `cong_cu_test`, `MẢNH`, `targeted_mutant_gate: DAT`, `bien_nhan_v2_test`, `TL_SELFTEST_PATS[1]`, `OK ci_phamvi`, `ca DA CHAY QUA`, `DOT BIEN … dat`.
    · Đuôi `.*` làm `fullmatch` mất răng. `F-luat` sinh log từ chính LUAT nên không phát hiện được.
    · `danh_gia_gate.py:106-119`, `:125-129`.
  de_xuat: Chốt đuôi của từng regex theo dòng log thật, và cấm `.*` ở cuối. Mỗi regex viết lại có một vế âm trong `F-luat` (vd `BỎ QUA 74`). Đặc tả hoá cách `tom` gán nhãn → bước, kể cả ca `TL_SELFTEST`.
## Đã đo lại, khớp
- sha256 đặc tả `570b1085…` (cũng bằng `ops/specs/wp1236-r2.md` tại `4c2b72c`). Clone không nông; HEAD = `3163f4d` + đặc tả.
- Tên khoá: `moc_gate_output` 42 · `gate_output` 22 · `moc_gate_output_rc_disposition` 2 · `gate_output_nguon` 1 · `gate_output_nguon_va_gioi_han` 1. Không khoá nào chứa `gate-output`.
- Lời khai: 46 hồ sơ; 44 hồ sơ có lời khai khác `not_measured`, tổng 61 lời khai; 22 có / 22 không có provenance; 9 trong danh sách `MIEN_TRU_CUTOVER` (danh sách khớp từng tên); 35 hồ sơ ngoài L5; chỉ `not_measured`: pr1109, pr1137.
- Provenance theo schema: 28 hồ sơ / 34 tệp (pr945 có 2 tệp).
- Bảng L8 35 dòng: cột số tệp provenance, số lời khai, dạng và L-6 khớp 35/35.
- L-7: 49 hồ sơ `DAT` = 32 có khoá lời khai + 17 không có (danh sách 17 tên khớp). `kiem_ho_so_land` 49/49 rc 0; `land_evidence_nguon` 98 ĐẠT · 25/28 miễn trừ · 0 vi phạm.
- Ruff 0.17.3 `--select F`: `packet_loop.py` 1 (F841), `packet_loop_test.py` 2 (F541); bốn tệp `ops/` và `ci_dang_ky_test.py` 0.
- ADR-0052/0053 @ `8ab1007` qua đủ ba phép đo hiệu lực (rc1 = 0, rc2 = 128, nằm trên first-parent); mỗi dòng `tran_*` xuất hiện đúng 1 lần.
- `danh_gia_gate.py`: `LUAT` có 10 loại job; `gate-registry` có `CUOI` + `KHONG`; `gate-packet-loop` có `CUOI`; chỉ `gate (` có `JSON_OK`. `ci_provenance.py:348-353` ghi `name`/`conclusion`/`labels`/`buoc`.
- Mục `MOI` là một dòng mỗi mục, nên A-M3 "numstat `1 0`" làm được. `kiem_ho_so_land` rc 3 khớp ngữ nghĩa "không nạp được" (B8). D1 đòi `moc_10_2_2` đúng bốn khoá; `ci_master.run_id` và `merge_commit` có trong lược đồ M8.
- Run push master trong provenance: 23 job, toàn Ubuntu, mọi job khớp một tiền tố `LUAT` (Q7 khả thi về tập job).
- Không kiểm được: nhánh `ops/wp1240-r1-g1-lease` và tệp nguồn của N1/N2 (không có trong clone); con số "755 nhánh" (không có mạng).
KET_LUAN: changes_requested
```