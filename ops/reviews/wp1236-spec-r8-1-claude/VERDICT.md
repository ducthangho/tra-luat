Kết luận cho r8: **changes_requested**. Grammar K7-S đúng về mặt cú pháp, nhưng còn hai finding P2 nên chưa approve được. Ngoài ra có 6 finding P3, không chặn.

**Grammar đứng vững khi môi trường sạch.** Tôi chạy bash 5.2 và dash thật, đúng ba mẫu lệnh GitHub, với chương trình thoát 1. Không tìm được thân `run` nào mà grammar nhận nhưng lỗi bị nuốt. Đã thử từ khoá shell ở vị trí đối số, các ký tự `= : - .`, `--`, dòng cuối có và không có `\n`. Mọi con số chính của r8 tôi đo lại đều khớp.

**Hai P2:**
- **H01 — môi trường đi vào từ bước trước.** r8 viết rằng `GITHUB_ENV`/`GITHUB_PATH` "đã chặn ở `chan_k7`". Thực ra `chan_k7` chỉ dò chữ trong thân `run:` của bước đứng trước. Bước `uses:` và chương trình ghi vào các tệp ấy không bị chặn. Trên `ci.yml` thật, cả 22 job J đều có `setup-python` đứng trước bước luật. Năm job YAML có thêm `bash ops/cai_cong_cu.sh`, script này ghi `$GITHUB_PATH`. Đo thật: có `BASH_ENV` trong môi trường thì thân `python ops/hong_test.py` thoát 0 dưới cả hai mẫu bash, kể cả có `--noprofile --norc`. Dưới `sh -e` (dash) thì vẫn thoát 1.
- **H02 — dạng `pwsh` không có vế đo.** Có ba chốt mà r8 viết thành lời nhưng không có vế âm hay đột biến nào: đối số đầu của dạng `pwsh` (loại `pwsh -Command`), `P` không bắt đầu bằng `-`, và đuôi tệp đúng theo từng dạng. Tôi viết bảy đột biến không tương đương, bảy cái đều sống qua đủ 98 vế. Vì vậy A14-S không đo được câu "executor viết khác miễn tương đương".

**Đã kiểm, không có vấn đề:**
- Ba cách viết lại R1/R2/R6 làm được (các thân không chứa `${{ }}`), và vẫn giữ dấu hiệu output mà `LUAT_v1` đòi.
- R5 không làm yếu việc truyền lỗi: `don-nhanh_test.ps1` tự `exit 1`/`exit 0` tường minh và đặt `$ErrorActionPreference='Stop'`.

**Không kiểm được:**
- Runner GitHub có chặn đặt `BASH_ENV` qua `GITHUB_ENV` không: phải gọi mạng mới biết.
- Hành vi của `pwsh -Command`: container không có `pwsh`.
- Nội dung các quyết định 6681159074, 6683884474, 6684776121, trong đó có "danh sách đường D1–D8": không có trong ISSUE.md.

Tôi không sửa gì trong `repo/` và `git status` vẫn sạch. Các phép đo nằm ở `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-1-claude/work/` (`benv/`, `soan/`, `census_lai.txt`, `ci_d26b36f.yml`). Script đột biến bổ sung chạy qua stdin, không lưu.

```
# VERDICT wp1236 r8 vòng 1
spec_sha256: 2a8c42e1d711e3c09281df6d36eb8c5a698c577ebad688e52e9ce0583c5828ff
## Finding vòng 7 của tôi
- G01: CÒN MỞ — chua_do_duoc 9 (dòng 1184) vẫn ghi "run sớm nhất 40842340568 của pr1013" và "29/29"; Codex lượt 3–4 trên gen 1 cũng đo "run nhỏ nhất 40268583940". P3, ngoài phạm vi r8 khai, không chặn.
- G02: CÒN MỞ — A20 (dòng 878) vẫn chỉ có (a)–(e); các điều kiện tự kiểm sổ của r7 vẫn không có vế đỏ. P3.
- G03: CÒN MỞ — dòng 222–223 vẫn áp điều kiện "chứa đủ CHECK_BAT_BUOC" cho MỌI phiên bản, kể cả miền đã đóng. P3.
- G04: CÒN MỞ — dòng 602–603 giữ nguyên câu về `JOB_BAT_BUOC` 14 tên của #1257. P3.
- G05: ĐÓNG — dòng 838–839 ghi rõ SHA checkout của bản sao provenance trỏ commit tạm, nên F-ok passed được; còn sót một câu mâu thuẫn ở dòng 830 (H05).
- G06: CÒN MỞ — A3j (dòng 858) vẫn dựng hình REST thay vì hình `ci_provenance.moc_gate`. P3.
- G07: CÒN MỞ — m-A3k (dòng 859) vẫn trùng m-A3d. P3.
## Findings mới
- id: H01
  severity: P2
  vi_tri: K7-S *Ranh giới của K7-S* dòng 409–411; K7 `chan_k7` dòng 306–307; *Phạm vi của passed* dòng 337
  van_de: Câu "GITHUB_ENV/GITHUB_PATH (đã chặn ở chan_k7)" và "BASH_ENV… đã bị chặn" rộng hơn phép đo. chan_k7 chỉ dò CHỮ trong thân `run:` đứng trước; bước `uses:` và chương trình ghi tệp `$GITHUB_ENV`/`$GITHUB_PATH` không bị chặn, và kênh ấy có thật trước bước luật ở 22/22 job J. Biến `BASH_ENV` đi qua kênh này làm một thân grammar nhận (`python P.py`) thoát 0 dưới cả hai mẫu bash, tức lập luận "DANG là tên chương trình nguyên văn" không còn đứng.
  bang_chung: (1) `env -i PATH=… BASH_ENV=<tệp: trap 'exit 0' EXIT> bash -e s.sh`, với s.sh = `python ops/hong_test.py` (thoát 1) ⇒ rc 0; `bash --noprofile --norc -eo pipefail s.sh` ⇒ rc 0; không có BASH_ENV ⇒ rc 1 cả hai; `sh -e` (dash) có BASH_ENV ⇒ rc 1. (2) yaml.safe_load ci.yml@fe84620: cả 8 job YAML chứa bước luật đều có `uses: actions/setup-python@v5` trước bước luật đầu; gate, gate-cong-cu, gate-ops, gate-registry, gate-packet-loop có thêm `bash ops/cai_cong_cu.sh shellcheck|rg`, ghi `$GITHUB_PATH` (ops/cai_cong_cu.sh:78); bốn job trong đó (trừ gate-ops) có thêm `bash ops/cai_actionlint.sh` (:226). Các thân này không nhắc `GITHUB_PATH` nên chan_k7 không chặn — và A15 còn ĐÒI chan_k7 = 0 bước bị chặn. Docstring ops/ci_provenance.py:250 tự ghi "Bước `uses:` đứng trước là giới hạn khai, không chặn."
  de_xuat: Viết lại câu cho đúng: chan_k7 chỉ chặn khi thân run trước nhắc NGUYÊN VĂN `GITHUB_ENV`/`GITHUB_PATH`; bước `uses:` và chương trình ghi các tệp ấy thì không, và có thật ở 22/22 job J. Môi trường thừa kế (BASH_ENV, SHELLOPTS, BASH_FUNC_*%%, PATH) qua kênh này là giới hạn cùng hạng với "ghi đè tệp trên PATH". Ghi giới hạn vào *Phạm vi của passed* và Q6. Muốn chặt hơn thì trình chủ kho thành câu hỏi riêng, kèm hệ quả đo được: trên ci.yml hiện tại, mọi job J đều bị chặn.
- id: H02
  severity: P2
  vi_tri: K7-S dòng 379 ("executor được viết khác … ca A14-S đo"), dòng 398–399; A14-S dòng 883–898; bảng disposition dòng 908–934; Phản biện dòng 1302
  van_de: Ba chốt mà K7-S viết thành lời không có vế âm và không có đột biến riêng: đối số đầu của dạng pwsh (loại `pwsh -Command`, bỏ `-NoProfile`), `P` không bắt đầu bằng `-`, và đuôi đúng theo từng DANG. Do đó A14-S không đo được tính tương đương mà dòng 379 dựa vào. Một cài đặt nhận `pwsh -NoProfile -Command exit` (bước xanh mà không chạy chương trình gate nào) vẫn qua đủ A14-S.
  bang_chung: Chạy `dung()` của dot_bien_r8.py (bản sao trong work/soan) với bảy đột biến: x1 P cho `-` ở ký tự đầu; x2 DANG pwsh = `pwsh( W)+`; x3 `-NoProfile` tuỳ chọn; x4 python bỏ đuôi `.py`; x5 đuôi bất kỳ cho mọi DANG; x6 W thêm `+,@%^`; x7 ống không dấu cách. Cả bảy ⇒ "0 vế âm đổi lý do, 0 vế dương hỏng" trên 91+7 vế, trong khi bản gốc từ chối từng đầu vào phân biệt (`python -x.py`, `pwsh -Command Get-Date`, `pwsh -File a.ps1`, `python ops/x`, `bash ops/x.py`). Có 0/98 vế chứa `pwsh` trong thân run (chỉ g_pwsh_shell, qua khoá shell). Có m-S9b riêng cho bash, không có bản tương ứng cho pwsh. Mã thoát của `pwsh -Command` theo tài liệu pwsh: KHÔNG ĐO ĐƯỢC (container không có pwsh).
  de_xuat: Thêm các vế âm `pwsh -NoProfile -Command exit`, `pwsh -File x.ps1`, `pwsh -NoProfile -File x.py`, `python -x.py`, `python ops/x`, `bash ops/x.py`. Thêm đột biến riêng: m-S9p (nới riêng dạng pwsh), m-S9d (P cho `-` đầu), m-S9e (nới đuôi), mỗi cái một ca đích. Với x6/x7 (vô hại với shell): thêm vế, hoặc ghi chúng là đột biến không tương đương được chấp nhận, kèm lý do.
- id: H03
  severity: P3
  vi_tri: *Phản chứng đã chạy* dòng 431–435; vế `l9_04_va_va` của probes_r8.py
  van_de: "36 vế … tức lỗi bị nuốt thật" đếm cả 5 vế mà chương trình hỏng KHÔNG được gọi. Ngoài ra l9_04 dựng lại khác VERDICT lượt 9 (Codex: cả 10 biến thể Bash rc 0; bản dựng lại rc 1), nên dạng `&&` nuốt lỗi thật không có trong bảng.
  bang_chung: probes_r8.json: 5 vế g_python_c, g_python_stdin, g_lenh_ngoai_ds, g_python_c_tran, g_bash_c_tran có rc 0 vì chạy chương trình khác. Đo: `python ops/hong_test.py && true` + dòng `true` dưới `bash -e` ⇒ rc 0; l9_04 (một dòng) ⇒ rc 1; gram trả `lenh_ngoai_cu_phap` cho cả hai.
  de_xuat: Ghi 36 = 31 nuốt lỗi + 5 không chạy chương trình gate. Thêm vế `l9_04b` = `X && true\ntrue` cho khớp VERDICT lượt 9.
- id: H04
  severity: P3
  vi_tri: A14 dương (i′), dòng 871
  van_de: Lý do kỳ vọng `cu_phap_run:ong_khong_bash_tuong_minh:packet-loop selftest` thiếu phần tên job, lệch dạng bốn phần ở dòng 422–423 và ở A14-S3 (dòng 904). Ca so danh sách lý do, nên một trong hai chỗ buộc phải sai.
  bang_chung: dòng 422 `cu_phap_run:<lý do>:<name REST của job>:<tên bước REST>`; dòng 904 `…:gate-packet-loop (ubuntu-latest):packet-loop selftest`.
  de_xuat: Sửa (i′) thành `cu_phap_run:ong_khong_bash_tuong_minh:gate-packet-loop (ubuntu-latest):packet-loop selftest`.
- id: H05
  severity: P3
  vi_tri: Fixture `F-ok`, dòng 829–831 so với dòng 838–839
  van_de: Câu "chỉ thay `log_day_du`" mâu thuẫn với câu mới của r8 "SHA checkout của bản sao provenance trỏ commit ấy".
  bang_chung: trích hai câu nêu trên.
  de_xuat: Ghi "thay `log_day_du` và `checkout[*].sha` (23 mục) bằng OID commit tạm; `moc.run.head_sha` giữ `fe84620`".
- id: H06
  severity: P3
  vi_tri: dòng 936–938 (đột biến tương đương); K7 dòng 310 ("Áp SAU chan_k7"); *Bỏ ở r8* dòng 417–420
  van_de: (a) Câu "đổi thứ tự bước 1–2 là tương đương" sai khi ca so lý do: với run không phải chuỗi + `shell: pwsh`, bản gốc ra `lenh_ngoai_cu_phap` còn bản đảo ra `shell_ngoai_cu_phap`. Không vế nào có cặp ấy nên đột biến này sống. (b) Hai luật "Áp SAU chan_k7, chỉ ghi lý do của chan_k7" và "executor không giữ lại mã cũ" không có ca hay đột biến nào làm đỏ (L3).
  bang_chung: g_run_khong_phai_chuoi có shell None; A14 chỉ đòi "lý do riêng", không đòi danh sách lý do đúng một mục của chan_k7.
  de_xuat: Thêm vế (run None, shell "pwsh") ⇒ `lenh_ngoai_cu_phap` và bỏ chữ "tương đương". A14(c) phải đòi danh sách lý do ĐÚNG một mục của chan_k7, kèm đột biến "vẫn gọi K7-S sau khi chan_k7 đã chặn". Với *Bỏ ở r8*: ghi thẳng là kiểm bằng đọc diff, chưa có phép đo.
- id: H07
  severity: P3
  vi_tri: bảng R1–R6 dòng 474–481; Q-r8-2 dòng 1147–1151
  van_de: (a) R4 tách `update-linux.sh --selftest` ra bước riêng, tức đảo ngược 91686a6 ("run Linux updater selftest in existing lease step"), mà đặc tả không nhắc. 91686a6 gộp đúng bước riêng do 36ee6cb thêm trước đó vài giờ. (b) Q-r8-2 chỉ nói chung "một P.sh có thể nuốt lỗi", không nói hệ quả cụ thể: R1/R2/R6 dời NGUYÊN VĂN đúng ba thân K7-S từ chối (29, 8, 38 dòng, có `if`, `$(…)`, heredoc) vào P.sh, nên sau khi viết lại ba bước ấy thành đo được mà bằng chứng truyền lỗi không đổi gì so với hôm nay.
  bang_chung: `git show 91686a6 -- .github/workflows/ci.yml` (xoá bước "Linux updater selftest (wp1178)", gộp vào bước lease); `git log 8983e1b..fe84620 -- ci.yml` = d8cad9b, 36ee6cb, 91686a6; thân ba bước in từ ci.yml@fe84620.
  de_xuat: Ghi lý do của 91686a6 vào R4, hoặc ghi "chưa rõ, packet viết lại phải hỏi". Thêm vào Q-r8-2 câu hệ quả cho R1/R2/R6 để chủ kho chọn có ý thức.
- id: H08
  severity: P3
  vi_tri: grammar K7-S dòng 366–403; Q-r8-2
  van_de: r8 chặt hơn quyết định 6692008457 ở ba chỗ mà không khai thành câu hỏi: quyết định chỉ cấm "chuyển hướng phức", r8 cấm mọi chuyển hướng; quyết định cho "đối số", r8 cấm mọi đối số có nháy; quyết định nói "một lệnh đơn", r8 chỉ nhận ba chương trình. Cả ba đều fail-closed và không đụng bước nào của ci.yml hiện tại.
  bang_chung: ISSUE.md dòng 474 (văn bản quyết định); census: 24/24 bước đo được đều là `python P.py` trần.
  de_xuat: Thêm một dòng vào Q-r8-2 liệt kê ba chỗ siết kèm lý do (builtin/từ khoá; `>` giấu output khỏi dấu hiệu; nháy cần phân tích cú pháp).
## Đã đo lại, khớp
- sha256 SPEC.md = ops/specs/wp1236-r8.md = 2a8c42e1…; HEAD cf0ee8b = d26b36f + 8 tệp chỉ thêm (đặc tả + 7 hiện vật); git status sạch trước và sau.
- probes_r8.py chạy lại trên bản sao: rc 0; 91/91 vế âm bị từ chối (88/2/1); 36 vế rc_bash 0 (16 l8, 9 l9, 2 connector, 9 g); 7/7 vế dương được nhận với rc 1; JSON khớp bản trong kho; g_* = 39, kt_* = 24.
- dot_bien_r8.py: 40/40 giết đúng ca đích, 0 làm hỏng vế dương; JSON khớp.
- census_r8.py: output khớp từng dòng census_r8.txt — d26b36f và fe84620: 30/24/6; 8983e1b: 25/5; luat_sha256 ee0f2db8…; 91686a6 nằm giữa 8983e1b và fe84620, và chính nó đổi bước lease thành 5 dòng.
- Provenance pr1231: J = 22; 13 cặp (job J, bước ngoài grammar) trên 10 job, cả 13 REST success ⇒ A15d 13 mục, 10/22 job.
- Sáu thân ngoài grammar không có `${{ }}`; dấu hiệu LUAT_v1 của chúng đến từ chương trình còn giữ lại sau R1–R6 ⇒ "giữ nguyên dấu hiệu output, luat_sha256 không đổi" đứng được.
- R5: don-nhanh_test.ps1 đặt `$ErrorActionPreference='Stop'` và tự `exit 1`/`exit 0` (dòng 21, 653–654); thân hiện tại đã là `pwsh -NoProfile -File …` ⇒ bỏ `shell: pwsh` không làm yếu việc truyền lỗi.
- numstat 08bcb51..508d678: 539 + 1080 + 1 = 1620; ước 1620 + 10 + 215 ≈ 1845, nằm trong 1750–1900, trần 1950.
- VL-F: cả sáu giá trị nguyên văn được gram nhận với shell tương ứng ⇒ F-ok passed làm được; F-ok-goc ⇒ 13 mục cu_phap_run.
- Bash/dash thật, ba mẫu lệnh GitHub, môi trường sạch: thân `python ops/hong_test.py fi then done esac -- a=b c:d -x ./.. time` được nhận và cho rc 1 cả ba ⇒ từ khoá và `= : - .` ở vị trí đối số không phá việc truyền lỗi.
- Kế thừa từ A1, mục 1–5, khớp văn bản VERDICT lượt 3–9 trong ISSUE.md (F01–F11; 4491937587; 4493205470 "16 nhóm / 13 mẫu"; KHONG 00; 101 đột biến / 4 tự kiểm). l8_01…16 và l9_01…10 khớp danh mục trong 6690875449 / 6690900537 / 6691822431 (trừ rc của l9_04, xem H03).
- tran_loi_goi_codex_A1_gen2 nhất quán với ADR-0052 (trần 8 theo PR; lượt 2 trở đi chỉ khi còn P0–P2; hết trần ⇒ ADR-0037) và với cách ADR-0055 đếm connector ở PR #909.
KET_LUAN: changes_requested
```