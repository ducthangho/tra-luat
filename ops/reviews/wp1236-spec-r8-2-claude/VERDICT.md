Kết luận vòng 2: **changes_requested**. Còn một finding P2 mới, cùng lớp với H02 của tôi ở vòng 1, cộng năm P3. Grammar K7-S vẫn đúng khi môi trường sạch. Mọi con số mới hoặc đã đổi tôi đo lại đều khớp.

**Finding P2 mới (I01):** bản sửa chỉ thêm vế và đột biến cho đúng bảy đột biến tôi liệt kê ở vòng 1, không mở rộng ra cả lớp. Tôi viết thêm vài cài đặt không tương đương với bản tham chiếu và nguy hiểm thật. Cả nhóm sống qua toàn bộ A14-S: 109 vế âm, 7 dương, 52 vế gốc gen 1. A14-S5 cũng không bắt được, vì nó chỉ chạy Bash trên các vế có sẵn trong bảng.
- Các đột biến sống:
  - nhận `||` hoặc `&` làm dấu tách ống;
  - nhận `&` ở cuối lệnh đơn;
  - nhận `!` ở đầu lệnh;
  - nhận `|| LENH` sau lệnh đơn;
  - thêm một ký tự đặc biệt vào lớp ký tự của `P`: 22/23 ký tự sống, chỉ `*` bị `g_glob` giết.
- Bash thật cho rc 0 với mọi thân mà các đột biến này nhận, và chương trình hỏng đều đã chạy. Ví dụ: `X || Y`, `X & Y`, `X &`, `! X`, `python ops/hong_test.py||true||x.py`.
- Vì vậy câu "executor viết khác miễn tương đương; ca A14-S đo" vẫn rộng hơn phép đo.

**Các P3:**
- **I02:** phương án (c) của Q-r8-4 không đóng được `BASH_ENV` cho dạng `bash P.sh`. Đo: dưới `sh -e`, thân đó vẫn ra rc 0. Ngoài ra (c) chưa ghi hệ quả trên `ci.yml`.
- **I03:** hai chỗ viết "action đã ghim" là sai. Mọi `uses:` trong `ci.yml` đều theo tag (`@v4`, `@v5`), không ghim SHA.
- **I04:** hai câu "rc gián tiếp" và *Phạm vi của passed* vẫn viết vô điều kiện, chưa kèm giới hạn môi trường thừa kế.
- **I05:** đoạn mô tả `F-ok` còn tự mâu thuẫn. Thêm nữa, không chốt K1–K9 nào đối chiếu SHA checkout với head hay với `moc.workflow_definition.blob`, dù trên dữ liệu thật cả hai đều khớp.
- **I06:** năm lời khai nhỏ lệch phép đo (chi tiết trong khối dưới).

Tôi không sửa gì trong `repo/`; `git status` sạch, HEAD vẫn `8fc339b`. Các script đo nằm ở `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-2-claude/work/` (`dot_bien_them_v2.py`, `g1_qua_dot_bien_v2.py`, `q4c/`, `soan/`).

```
# VERDICT wp1236 r8 vòng 2
spec_sha256: a37c41a37dc4cdebabfbfa50777cc4bc3a5352f0618e5bde31945a0bceb5619c
## Finding vòng 1 của tôi
- G01: ĐÓNG — chua_do_duoc 9 nay ghi run sớm nhất 40268583940. Đo lại: nhỏ nhất trong 31 tệp provenance `ci.yml` `push` trên d26b36f, ở `pr945-wp899-provenance/do-1026-cebb5b2/`. Con số "29/29" đã cũ (I06).
- G02: ĐÓNG — A20 có (f)–(i′) kèm m-A20d…h, mỗi đột biến một vế đích.
- G03: ĐÓNG — dòng 222–225 chỉ áp `CHECK_BAT_BUOC` cho phiên bản có miền mở.
- G04: ĐÓNG — câu "14 tên" đã thay bằng dòng 621–623 (#1257 mở rộng khoá chọn phiên bản).
- G05: ĐÓNG — `F-ok` fetch `fe84620`; phần mâu thuẫn còn sót xem H05/I05.
- G06: ĐÓNG — A3j dựng bằng `moc_gate`. Đo trên readback 41397205258: `labels []`, `runner_id None`, `buoc "not_measured"`, `trang_thai skipped`, khớp câu chữ.
- G07: ĐÓNG — m-A3k ("chốt đủ job chỉ chạy khi chưa có lý do khác") nay khác m-A3d.
- H01: ĐÓNG — *Ranh giới của K7-S* viết lại theo phép đo, và các số liệu khớp: 22/22 job J, 5 job có `cai_cong_cu.sh`, 4 job có `cai_actionlint.sh`, `:78`, `ci_provenance.py:250`; có Q-r8-4. Phần còn sót xem I03/I04.
- H02: ĐÓNG — cả bảy đột biến x1–x7 của tôi nay bị giết (m-S9d/e/f/g/p/q, m-S7c, kt_2b…5e). Nhưng cùng lớp lỗi vẫn hở ở chỗ khác ⇒ I01.
- H03: ĐÓNG — 41 vế rc 0 = 36 nuốt thật + 5 không chạy, có dấu `DA_CHAY`; `l9_04b` rc 0.
- H04: ĐÓNG — A14(i′) có đủ bốn phần, khớp A14-S3.
- H05: CÒN MỞ (một phần) — câu "chỉ thay `log_day_du`" đã sửa, nhưng dòng 853–855 vẫn mâu thuẫn với dòng 859–862 (I05).
- H06: ĐÓNG — (a) có `g_run_khong_phai_chuoi_pwsh` và m-S19 giết đúng vế ấy; (b) A14(c) đòi đúng một lý do của `chan_k7` + m-S20; lệnh `rg` cho *Bỏ ở r8*.
- H07: ĐÓNG — R4a/R4b nêu lý do `91686a6` (thông điệp commit trích đúng; `36ee6cb` thêm bước lúc 02:55Z, `91686a6` gộp lúc 05:19Z); Q-r8-2 ghi hệ quả R1/R2/R6 (29/8/38 dòng).
- H08: ĐÓNG — ba chỗ siết đã liệt kê ở Q-r8-2.
## Findings mới
- id: I01
  severity: P2
  vi_tri: K7-S dòng 381 ("executor được viết khác, miễn tương đương trên mọi đầu vào; ca A14-S đo"); A14-S dòng 908–937 (danh mục vế; A14-S5 + m-S18 "đo bằng Bash, không bằng bảng kỳ vọng"); bảng disposition dòng 939–975; Phản biện dòng 1384
  van_de: A14-S vẫn không đo được tính tương đương. Bản sửa chỉ thêm vế cho đúng bảy đột biến H02 đã nêu. Nhiều cài đặt không tương đương, nguy hiểm thật — dấu tách ống mở thêm `||` hoặc `&`; lệnh đơn nhận `&` cuối, `!` đầu, hay `|| LENH`; lớp ký tự của `P` nhận ký tự đặc biệt — sống qua toàn bộ A14-S1…S5 và 52 vế gen 1. Lý do: bảng chỉ có các cấu trúc ấy khi đi kèm phần tử ngoài `LENH` (`true`, `cat`, `set`…), không có dạng tối giản ghép toàn bằng `LENH`. A14-S5 chỉ chạy Bash trên vế của bảng, nên cũng không bắt được.
  bang_chung: `python3 -I work/dot_bien_them_v2.py` (cwd work/soan, dùng `dung()` của dot_bien_r8.py). Đột biến ` \|\|? `, ` \|+ `, ` [|&] `, DON `{LENH}( &)?`, DON `(! )?{LENH}`, DON `{LENH}( \|\| {LENH})*` ⇒ 0/109 vế âm đổi lý do, 0/7 vế dương hỏng; `work/g1_qua_dot_bien_v2.py` ⇒ 0/52 vế gen 1 đổi lý do. Thân mà đột biến nhận, chạy bằng `chay()` của probes_r8 (Bash thật, môi trường sạch): `X || Y` (bash) rc 0; `X & Y` (bash) rc 0; `X &` rc 0; `! X` rc 0; `X || Y` (shell vắng) rc 0; cả năm đều `da_chay=True`. `X ; Y`, `X && Y` ra rc 1, vô hại nhưng không tương đương. Họ `P`: thêm c vào lớp ký tự đuôi của `P`, với mỗi c trong `; & | ! ( ) { } $ ` ' " \ < > # ? [ ] ~ + , @ % ^` ⇒ đột biến sống (chỉ `*` chết, do `g_glob`). Với `P` có `|`: `python ops/hong_test.py||true||x.py` được nhận, Bash rc 0, da_chay True.
  de_xuat: Thêm vế âm tối giản ghép toàn bằng `LENH`, dưới cả `shell` vắng và `bash`: `X || Y`, `X && Y`, `X ; Y`, `X & Y`, `X &`, `! X`. Thêm họ `kp_<hex>` = `python ops/a<c>b.py` cho 29 ký tự, cộng biến thể ký tự đầu. Mỗi họ có đột biến riêng: m-S7d (` \|+ `), m-S7e (` [|&] `), m-S7f/g (DON `&` cuối / `!` đầu), m-S7h (`|| LENH`), m-S15[c] (thêm c vào `P`). Chắc hơn: cho A14-S5 (hoặc một ca A14-S6 mới) chạy trên một kho đầu vào SINH tổ hợp (`LENH op LENH` với mọi toán tử điều khiển của Bash; mọi ký tự của bảng ở vị trí `DANG`/`P`/`W`), so module với regex tham chiếu và chạy Bash thật trên mọi thân được nhận. Khi ấy câu "tương đương" ở dòng 381 mới có phép đo, và cửa thứ ba không phải chờ reviewer chỉ.
- id: I02
  severity: P3
  vi_tri: Q-r8-4 phương án (c), dòng 1213–1214
  van_de: (c) "đòi `shell: sh` (dash không đọc `BASH_ENV`) — vẫn hở `PATH`" vừa sai vừa thiếu hệ quả. Dạng `bash P.sh` dưới `sh` vẫn sinh một bash không tương tác, và bash ấy đọc `BASH_ENV`. `python` có kênh môi trường riêng (vd `PYTHONPATH` trỏ một `sitecustomize`; chỉ mô tả bằng lời, không dựng). Ngoài ra không bước luật nào khai `shell: sh`, và ống đòi `bash`, nên (c) cũng chặn 22/22 job J cho tới khi viết lại cả 30 bước, giống (b).
  bang_chung: work/q4c: `env -i PATH=… BASH_ENV=env_trap.sh sh -e s_bash.sh` với `s_bash.sh = bash ops/hong.sh` (`exit 1`) ⇒ rc 0. Cùng lệnh không có `BASH_ENV` ⇒ rc 1. Thân `python ops/hong_test.py` có `BASH_ENV` ⇒ rc 1. `/bin/sh` → dash. Census fe84620: 30 bước luật = 24 `shell` vắng + 5 `bash` + 1 `pwsh`, 0 bước `sh`.
  de_xuat: Ghi (c) đúng là chỉ đóng `BASH_ENV` cho dạng `python`/`pwsh`; dạng `bash` vẫn hở, các biến môi trường riêng của python vẫn hở. Thêm hệ quả "22/22 job J not_measured tới khi viết lại 30/30 bước" như đã làm cho (b).
- id: I03
  severity: P3
  vi_tri: *Ranh giới của K7-S* dòng 419–420; Q-r8-4 (a) dòng 1211–1212
  van_de: Lập luận cho (a), "môi trường do mã kho tại SHA checkout và các action ĐÃ GHIM viết ra, cùng ranh giới với nội dung `P.py`", dựa trên một lời khai sai. Không action nào được ghim theo SHA; tag `@v5` là tag di động. Vì vậy mã ghi môi trường có thể đổi giữa hai run cùng SHA checkout, trong khi provenance và workflow mà `kiem` đọc không đổi.
  bang_chung: `git show fe84620:.github/workflows/ci.yml | grep -o 'uses: *[^ #]*' | sort | uniq -c` ⇒ 9 `actions/checkout@v4`, 8 `actions/setup-python@v5`, 2 `actions/download-artifact@v4`, 3 `actions/upload-artifact@v4`; 0 mục ghim 40 hex.
  de_xuat: Sửa thành "action theo tag di động, không ghim SHA". Trình (a) cho chủ kho với tiền đề đúng ấy, hoặc thêm một phương án "ghim SHA cho các `uses:` đứng trước bước luật" vào packet viết lại R1–R6.
- id: I04
  severity: P3
  vi_tri: K7 "rc gián tiếp" dòng 314–315; *Phạm vi của passed* dòng 339–341; Q-r8-4 khuyến nghị dòng 1215
  van_de: Hai câu vẫn khẳng định vô điều kiện rằng `conclusion: success` là "bằng chứng rc 0 của CHƯƠNG TRÌNH" và rằng `passed` phủ rc gián tiếp. Chúng không kèm giới hạn môi trường thừa kế mà chính *Ranh giới* và Q6 đã khai. Q-r8-4 (a) lại đòi "ghi thẳng trong thông điệp của cổng", nhưng thông điệp ĐẠT ở dòng 341 không có chữ nào về giới hạn ấy, và không ca nào ở B/C/D canh thông điệp.
  bang_chung: trích dòng 314 "…là bằng chứng rc 0 của CHƯƠNG TRÌNH được gọi, do GitHub ghi" và dòng 341 "thông điệp ĐẠT in 'điều kiện cần cho §10.2.2 Gate output (OS: ubuntu-latest)'".
  de_xuat: Thêm "với môi trường mà bước nhận được (Ranh giới của K7-S, Q-r8-4)" vào dòng 314 và vào *Phạm vi của passed*. Nếu giữ yêu cầu của (a), ghi nội dung câu thông điệp và một ca kiểm nó.
- id: I05
  severity: P3
  vi_tri: Fixture `F-ok` dòng 851–864; K1/K3/K7 dòng 275–303
  van_de: (1) Dòng 853–855 vẫn viết "FETCH ĐÚNG `fe84620` (… không commit `ci.yml` vào một OID khác), nên workflow là `ci.yml` nguyên văn". Điều đó trái với dòng 859–862 (VL-F commit thành con, workflow của `F-ok` ≠ nguyên văn), và trái với văn bản quyết định G05 mà không khai đây là chỗ lệch. (2) Thiết kế VL-F buộc K1–K9 không được ràng SHA checkout với `head_sha`, và cũng không được so workflow tại SHA checkout với `moc.workflow_definition.blob`. Trên dữ liệu thật, cả hai phép so đều khớp 100%, nên chốt rẻ nhất bị loại chỉ vì fixture (hình dạng "luật dựng trên fixture tự đặt"). `F-ok` còn mang `workflow_definition.blob = 2b2c9aa` của bản gốc trong khi `kiem` phân tích `ci.yml` của commit con.
  bang_chung: quét 39 tệp `ci_provenance/1` trên d26b36f: 0/39 có `checkout passed ≠ head_sha`; 28/28 tệp có `workflow_definition passed` cho `oid == head` và `git rev-parse <checkout>:<path> == workflow_definition.blob`; pr1231: `workflow_definition {oid fe84620…, blob 2b2c9aa2…}`; `git show 91686a6` cho `index 2463651f..2b2c9aa2`.
  de_xuat: Sửa câu ở dòng 853–855 cho khớp VL-F, và ghi thẳng r8 thay G05. Chọn một: (a) cho `F-ok` mang `head_sha` = OID con cả ở provenance lẫn header (fixture tự do chọn head), rồi thêm chốt `checkout == head_sha` (0/39 tác động thật) cùng chốt "khi `workflow_definition` passed thì blob tại SHA checkout phải bằng nó"; hoặc (b) khai thẳng hai chốt này là giới hạn, kèm phép đo trên.
- id: I06
  severity: P3
  vi_tri: dòng 863–864; dòng 23; dòng 416; Q-r8-2 dòng 1197; chua_do_duoc 9 dòng 1243
  van_de: Năm lời khai nhỏ lệch phép đo. (a) "Codex và Claude vòng 1 cùng đo `F-ok + VL-F` ⇒ passed": vòng 1 tôi chỉ đo sáu giá trị VL-F qua `gram.py` (chưa có module), không đo `kiem`. (b) "8983e1b khác hai SHA kia một bước": khác HAI bước luật. (c) `cai_actionlint.sh:226` là dòng tại d26b36f; tại fe84620, SHA mà câu ấy nêu, nó là `:193`. (d) "24/24 bước đo được là `python P.py` trần": 14/24 có đối số (dòng 480 viết đúng; chữ "trần" lấy từ H08 của tôi). (e) "29/29 tệp … có trong kho": trên base r8 là 31/31, kết luận vẫn đứng.
  bang_chung: VERDICT vòng 1 của tôi ("VL-F: cả sáu giá trị … được gram nhận ⇒ F-ok passed làm được"); diff ci.yml 8983e1b→fe84620 đổi `ci-duong-nhanh selftest` (thêm env `CI_DUONG_NHANH_CHE_DO`) và `lease-publish selftest`; `git show fe84620:ops/cai_actionlint.sh | grep -n GITHUB_PATH` ⇒ 193; liệt kê 24 thân ⇒ 14 có đối số; quét provenance d26b36f ⇒ 31 tệp, 31/31 có J = đúng 22 tên `JOB_BAT_BUOC`.
  de_xuat: Sửa năm câu theo số đo, kèm điều kiện đo (SHA, thời điểm).
## Đã đo lại, khớp
- sha256 SPEC.md = ops/specs/wp1236-r8.md = a37c41a3…; bản vòng 1 `git show cf0ee8b:…` = 2a8c42e1…; HEAD 8fc339b; `git status` sạch trước và sau.
- probes_r8.py (bản sao trong work/soan): rc 0; 109/109 vế âm bị từ chối (106/2/1); 41 rc 0 = 36 nuốt thật (16 l8, 10/11 l9 trừ l9_04, 6 connector, 4 g_: bash_c, sh_c, ong_khong_bash, ong_sh) + 5 không chạy (đúng năm tên đã nêu); 7/7 vế dương được nhận, rc 1, `DA_CHAY`; JSON khớp byte; nhóm vế: g_ 47, kt_ 29, l8 16, l9 11, conn 6.
- dot_bien_r8.py: 53/53 giết đúng ca đích, 0 vế dương hỏng; JSON khớp byte.
- g1_qua_grammar.py: 26 + 26 = 52/52 bị từ chối, gồm `explicit_bash` và `straight`; JSON khớp byte; 7/7 sha256 khớp g1/README.md.
- census_r8.py: output khớp từng dòng census_r8.txt — d26b36f và fe84620: 30/24/6, 8983e1b: 25/5; luat_sha256 ee0f2db8…; 6 thân ngoài grammar 29/8/2/5/1/38 dòng.
- ci.yml@fe84620: 8 job YAML (22 job J), mọi job có `checkout@v4` + `setup-python@v5` trước bước luật đầu; `cai_cong_cu.sh` ở gate, gate-cong-cu, gate-ops, gate-registry, gate-packet-loop; `cai_actionlint.sh` ở bốn job trong số đó (trừ gate-ops); không thân `run:` nào đứng trước nhắc `GITHUB_*`; `cai_cong_cu.sh:78`; `ci_provenance.py:250`.
- A15 trên pr1231: T 23, J 22; 43 lượt = 30 None + 13 có lý do; 29 tên = 23 + 6; tên duy nhất vắng ở REST là `tl selftest (luot PR — khong sinh bang chung)`; A15d 13 mục = gate 2 + gate-cong-cu 8 + gate-ops 3; m-A15c: `che_do_shell`@508d678 gắn cờ 0/30 bước.
- `91686a6` (05:19Z 05-11, "run Linux updater selftest in existing lease step") gộp bước `Linux updater selftest (wp1178)` mà `36ee6cb` (02:55Z) vừa thêm.
- numstat 08bcb51..508d678 = 1 + 539 + 1080 = 1620; ước 1620 + 10 + 325 = 1955 ∈ 1850–2000; `tran_moi` 2050; "53 + 6 đột biến" = 59 khớp `can_cu`.
- Dòng khai đầu tệp ADR-0052/0053 @8ab1007: `cat-file -e` rc 0, parent rc 128, có trong `--first-parent origin/master`, clone không nông.
- `tran_loi_goi_codex_A1_gen2`: điều kiện lượt 2–4 khớp nguyên văn ADR-0052 (giữ ở ADR-0055); 4 ≤ trần 8.
- `JOB_BAT_BUOC`: 22 tên, không trùng, mỗi tên khớp đúng một tiền tố `MUC`; 31/31 provenance `ci.yml` `push` có J đúng 22 tên ấy.
- Grammar đúng khi môi trường sạch: 218 thân được nhận (25 token W gồm `-c -e -o pipefail +e exit true if then done time = : ..`, ống hai chiều, biến thể P), chạy dưới `bash -e`, `bash --noprofile --norc -eo pipefail`, `sh -e` ⇒ 0 thân rc 0.
KET_LUAN: changes_requested
```