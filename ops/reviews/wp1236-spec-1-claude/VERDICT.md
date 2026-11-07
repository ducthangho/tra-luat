Review xong. Tôi đo lại các con số trên clone ở `b9766fe`; sha256 của đặc tả khớp. Kết luận: **changes_requested**, với 3 finding P1, 5 P2 và 5 P3.

Phần lớn số đo của đặc tả tái lập được, gồm bảng A, cột *neo*, ba trạng thái #1127, bảng lease và nền ruff. Các P1 đều là lỗ thiết kế:
- **Định nghĩa lời khai bỏ sót dạng đang có trong `ops/land/`.** Hồ sơ không miễn trừ `pr1155` có một chuỗi đúng hình dạng "conclusion + số `##[error]`" mà không bị coi là lời khai dương. Bản thân hồ sơ `pr696` mà đặc tả đếm vào bảng B cũng không phải lời khai theo định nghĩa của chính đặc tả.
- **K2 kết hợp ca `c11` chạy trên cây thật trong CI** thì lần đầu sửa `LUAT` sẽ làm đỏ mọi PR.
- **L-7 đòi "≥ 1 lời khai dương"** nên có trạng thái hợp lệ không bao giờ đạt được, ví dụ hồ sơ `owner_waived` theo §10.2.3.

Ghi chú môi trường: prompt nói clone "không nông", nhưng `.git/shallow` có 87 mục. Ba commit #1127 vẫn đọc được nên phép đo không bị ảnh hưởng. Riêng phép đo numstat lúc tạo tệp thì không làm được: các commit thêm tệp đều là graft. Kho không bị sửa (`git status` rỗng); script và cây tạm chỉ nằm dưới `work/`.

# VERDICT wp1236 r1 vòng 1
spec_sha256: d599ff336ac68eb0cb30f36167cf1c9f2beeea04fc2909de7324670b93fa8eee
## Findings
- id: F01
  severity: P1
  vi_tri: §Lời khai gate_output (dòng 129–136); ca A9 (dòng 298)
  van_de: Định nghĩa "lời khai dương" là danh sách CẤM đội lốt danh sách cho phép, nên các giá trị dạng mapping/list, chuỗi tự do và token có dấu câu đều không bị L8 kiểm, kể cả đúng hình dạng lỗi mà packet sinh ra để chặn.
  bang_chung: Chạy `python work/phan_loai.py .` trên 123 hồ sơ. Dưới hai khoá cho phép, các giá trị chia thành:
    · 45 chuỗi dương;
    · 9 dict và 6 list, nằm ở 9 hồ sơ: pr594, pr679, pr680, pr684, pr689, pr696, pr701, pr703, pr707 (cả 9 thuộc `MIEN_TRU_CUTOVER`);
    · 3 chuỗi `not_measured`;
    · 1 chuỗi tự do: `pr1155-wp1143 $.post_merge_provenance.gate_output = '23/23 job success, log tổng không có ##[error]; …'`. Hồ sơ pr1155 KHÔNG miễn trừ và đang `DAT` ở L-6. Đây chính là hình dạng "conclusion + số `##[error]`" của mục `hinh_dang_ke_thua`, nhưng nó không phải lời khai dương nên L8 bỏ qua.
    Regex dương của đặc tả cho False với `measured, xem a.txt`, `measured. a.txt`, `measured/passed`, `measured_partial`, `✅ passed`. Một hồ sơ mới viết `moc_gate_output: {trang_thai: passed}` cũng lọt L8.
  de_xuat: Đảo luật lại:
    · giá trị dưới `gate_output`/`moc_gate_output` phải là chuỗi bắt đầu bằng một token thuộc tập ĐÓNG {passed, measured, not_measured, failed, skipped, not_run, owner_waived};
    · dict, list hay chuỗi khác ⇒ ĐỎ `dinh_dang_loi_khai`;
    · khoá chứa `gate_output`/`gate-output` (casefold) mà không thuộc tập khoá phi-lời-khai đã biết (`gate_output_nguon`, `moc_gate_output_rc_disposition`, `gate_output_nguon_va_gioi_han`) ⇒ coi là lời khai.
    Thêm các vế dict, list, chuỗi tự do và `measured,` vào A9/C4, mỗi vế kèm đột biến.
- id: F02
  severity: P1
  vi_tri: Thiết kế mục 4 K2 (dòng 104); đoạn "Hạn chế (2)" (dòng 125–127)
  van_de: K2 buộc mọi tệp `gate_output/2` theo băm của `LUAT` HIỆN HÀNH, mà L8 lại chạy trên cây thật trong CI, nên lần sửa `LUAT` đầu tiên (đặc tả tự nhận sẽ phải sửa) làm đỏ mọi hồ sơ mới cùng lúc, kéo đỏ mọi PR.
  bang_chung: Ca `c11_cay_that_dat_va_mien_tru_du` (`ops/land_evidence_nguon_test.py:287`) chạy cổng trên `ROOT_THAT`. Test này đăng ký trong `MOI` (`.claude/dev/ci_dang_ky_test.py:57`) và được job `gate-registry` chạy (`ci.yml:1112`). Muốn tái sinh tệp thì cần log còn trong hạn lưu. Còn muốn hạ lời khai về `not_measured` thì L-7 chặn (xem F03).
  de_xuat: Thay K2 bằng một sổ phiên bản chỉ-thêm `LUAT_PHIEN_BAN = {luat_sha256: LUAT_vN}`.
    · `kiem` đánh giá tệp bằng đúng phiên bản mà tệp khai;
    · băm không có trong sổ ⇒ `not_measured`;
    · rút một phiên bản ra khỏi sổ là quyết định riêng, có miễn trừ.
    Thêm ca: sửa `LUAT` hiện hành ⇒ tệp cũ vẫn `passed` theo phiên bản cũ; đột biến bỏ sổ ⇒ ca đỏ.
- id: F03
  severity: P1
  vi_tri: Bảng "Luật mới", dòng L-7 (dòng 143); ca B2 (dòng 317)
  van_de: Điều kiện "≥ 1 lời khai gate_output dương" của L-7 làm ba trạng thái hợp lệ trở thành không bao giờ đạt.
  bang_chung:
    (a) `owner_waived` là disposition hợp lệ theo §10.2.3 (`docs/PROTOCOL_DA_PHIEN.md:974`). D2 (`DAT_MOC`, `packet_loop.py:3095`) và D2b của chính đặc tả đều nhận nó, nhưng L-7 không đếm nó là dương ⇒ hồ sơ landed dùng `owner_waived` sẽ TRUOT.
    (b) Run 41356691133 của #1127 có 14/37 job Windows. K6 đòi mọi job `-> passed`, `LUAT` không có biến thể theo OS, và chính `danh_gia_gate.py:6` ghi rằng lane Windows ra `not_measured` là đúng ⇒ run windows-and-ubuntu không bao giờ `passed`.
    (c) Miễn trừ neo theo băm, nên sửa một hồ sơ landed cũ (kiểu #1235 sửa #1127) là mất miễn trừ. Khi đó L-7 cần một tệp `gate_output/2` dựng từ log; log quá hạn thì không tạo được, còn hạ lời khai về `not_measured` thì trượt "≥ 1 dương" ⇒ hồ sơ không còn đường sửa.
  de_xuat:
    · L-7 nhận "≥ 1 lời khai gate_output thuộc {dương qua `kiem`; `owner_waived` có neo waiver đúng §10.2.3}";
    · ghi rõ hệ quả với run có job Windows: hoặc thêm `LUAT` theo OS, hoặc cho K3 khai phạm vi job;
    · với hồ sơ cũ mất miễn trừ, cho đường `not_measured` kèm quyết định chủ kho thay vì đòi lời khai dương.
- id: F04
  severity: P2
  vi_tri: K3–K5 (dòng 105–109); quy tắc `failed` (dòng 112)
  van_de: `kiem` không đối chiếu tên job và `conclusion` trong tệp với `provenance.yaml`, dù provenance có cả hai trường, trong khi `LUAT` lại được chọn theo tên job tự khai.
  bang_chung: `ops/ci_provenance.py:350-353` ghi `name` và `conclusion` của từng job vào `moc.gate_output.jobs`. Cả 34 tệp `ci_provenance/1` đều có hai trường này, và pr957 r27 có 1 job `conclusion: failure`. Hệ quả:
    · đổi tên `gate (ubuntu-latest)` thành `chuan-bi` thì chỉ cần 1 dòng `che_do=…` thay vì 18 bước;
    · ghi `conclusion=success` cho một job failure thì ra `passed` thay vì `failed`.
    Yêu cầu 1 của Issue là lời khai "phải KHỚP trạng thái trong provenance".
  de_xuat: Thêm một K: với mỗi `job_id`, tên và `conclusion` trong tệp phải bằng provenance; trạng thái `failed` lấy từ `conclusion` của provenance. Thêm hai ca kèm đột biến bỏ từng phép so.
- id: F05
  severity: P2
  vi_tri: Thiết kế mục 1 (`LUAT`, dòng 84–87), mục 2 (dòng `BUOC`), K5 (dòng 108–109)
  van_de: Mô hình K5 "mỗi bước có một dòng trích `re.fullmatch`" không biểu diễn được ba trong bốn loại dấu hiệu của `LUAT` gốc, và đặc tả không nói phải chuyển chúng thế nào.
  bang_chung: `danh_gia_gate.py:44-80` có, ngoài regex thường:
    · `JSON_OK`: 7/18 bước của `gate (`. Đây là đối tượng JSON nhiều dòng — `python .githooks/eol_policy.py --all --json` in 9 dòng, `"ok": true,` nằm ở dòng 4 và thụt lề. Bản `danh_gia` ghi dấu hiệu là chuỗi tổng hợp `ok:true`, không phải dòng log thật.
    · `CUOI:` (6 chỗ, đòi dòng TỔNG CUỐI) và `KHONG:` (1 chỗ, đòi một dòng VẮNG MẶT): một dòng trích không chứng minh được "là dòng cuối" hay "không có".
    Ngoài ra nhiều regex gốc không neo `$`: `^(\d+)/\1 ca DA CHAY QUA` từng cho `passed` dòng "290/290 … - KHONG DU: 74 ca BO QUA" (`pr1130 …/danh-gia-gate-output-41365578430.txt`). Một bước có ≥ 2 regex thì chữ "≥ 1 dòng" của K5 cũng mơ hồ.
  de_xuat: Định nghĩa trong đặc tả cách biểu diễn từng loại:
    · `JSON_OK`: dòng nào, và nhận diện mức gốc ra sao;
    · `CUOI`: `tom` phải trích MỌI dòng TỔNG của bước theo thứ tự, `kiem` xét dòng cuối;
    · `KHONG`: ghi thẳng là chỉ dựa vào lời khai của `tom`.
    Viết rõ "mỗi regex bắt buộc ⇒ ≥ 1 dòng `BUOC`". Thêm ca cho từng loại.
- id: F06
  severity: P2
  vi_tri: Dòng 146–147 (cách `packet_loop.py` nạp module)
  van_de: D2b nạp `<root>/ops/gate_output_doi_chieu.py` từ cây làm việc, trái mẫu `_canon` mà `packet_loop.py` dùng cho mọi validator `ops/` (#812), nên nhánh đang đóng WP tự cấp bộ kiểm của chính nó.
  bang_chung: `packet_loop.py:2404` (`CANON`) và `2420–2444` (`_canon`, `_nap`): validator được lấy từ `refs/remotes/origin/master`, đọc không được thì `KHÔNG ĐO ĐƯỢC`.
  de_xuat: Thêm module vào `CANON` và nạp bằng `_nap`. Thêm ca D: sửa module ở cây làm việc không đổi kết quả D2b.
- id: F07
  severity: P2
  vi_tri: Thiết kế mục 5 (dòng 113–115); L8, L-7, D2b (dòng 142–144)
  van_de: Không có gì neo run của tệp `gate_output/2` vào run mà lời khai hoặc biên bản nói tới.
  bang_chung:
    · K1 chỉ neo tệp với provenance, và `kiem_ho_so_gate_output` nhận bất kỳ provenance cùng run nào trong `<hồ sơ>-provenance/`.
    · pr1130 trích hai tệp `danh_gia` của hai run khác nhau (41365578445 và 41365578430). Nhiều lời khai nằm ngay cạnh khoá `run_id`, vd `pr1042 $.pre_merge_checks[1]`. Vậy một lời khai post-merge có thể được "neo" bằng tệp của run PR hoặc của run cũ.
    · D2b so `run_id` của tệp với `ci_master.run_id`, nhưng không ai so `provenance.moc.run.head_sha` với `merge_commit` — trường mà D1 đã bắt buộc có.
  de_xuat:
    · D2b thêm `provenance.moc.run.head_sha == bb["merge_commit"]`;
    · L8/L-7: mapping chứa lời khai có khoá `run_id` anh em thì run của tệp phải bằng nó;
    · phần còn lại ghi vào `ngoai_pham_vi`/`chua_do_duoc`.
    Kèm ca và đột biến.
- id: F08
  severity: P2
  vi_tri: "Thêm, không hồi quy", phản chứng #1127 (dòng 302–306); Q2 (dòng 394–395)
  van_de: Vế dương của phản chứng #1127 ("ĐẠT trên bản sửa của `7f22121` trích tệp `gate_output/2` dựng từ fixture cùng run_id") không thi công được như đã viết.
  bang_chung:
    · `ops/land/pr1127-wp1120-provenance/ci/provenance.yaml` có 37 job và 37 khoá `log_day_du`, còn `F-ok` có 3 job với 3 log giả ⇒ trượt K3 và K4.
    · Muốn ĐẠT thì hoặc phải thay provenance — khi ấy không còn là #1127 — hoặc chép 37 băm thật rồi gõ tay `BUOC` cho cả 14 job Windows, tức dựng đúng kiểu giả mạo mà đoạn "Ranh giới tin cậy" đã thừa nhận.
    · Với log thật, 14 job Windows ra `not_measured`, nên "bản SAU ĐẠT" theo cách diễn giải ở Q2 cũng không đạt được bằng dữ liệu thật.
  de_xuat: Ghi rõ cây tạm gồm blob `7f22121` với provenance được THAY bằng `F-ok`. Hoặc bỏ vế dương và nói thẳng ở Q2 rằng #1127 chỉ ĐẠT nhờ miễn trừ.
- id: F09
  severity: P3
  vi_tri: Bảng B (dòng 191–195), tổng (dòng 200), Q1 (dòng 389)
  van_de: Bảng B và các tổng lệch với định nghĩa của chính đặc tả.
  bang_chung:
    · `python work/do_loi_khai.py . work/loi_khai.json` ⇒ B = 14 hồ sơ / 21 lời khai, không phải 15/22.
    · `pr696-wp668` có `moc_gate_output` là LIST mapping (dòng 417 của hồ sơ), nên theo định nghĩa không phải lời khai. Thêm nữa, L5 bỏ qua pr696 toàn bộ ở `main()` (`land_evidence_nguon.py:385–390`).
    · Tổng chuỗi dương là 45 (24 + 21), không phải 46. "≥ 36" phải là 35, và `MIEN_TRU_L8` ≈ 35 mục.
  de_xuat: Sửa các số. Cho script đo gọi đúng hàm định nghĩa lời khai của module.
- id: F10
  severity: P3
  vi_tri: Mục C (dòng 197–198); `chua_do_duoc` 2 (dòng 411); `kich_thuoc` đợt B (dòng 239)
  van_de: Số mà đặc tả ghi "chưa đo" đo được ngay, và cho thấy miễn trừ L-7 lớn hơn nhiều so với bảng A gợi ý.
  bang_chung: L-6 có 49 hồ sơ `DAT`: 25 hồ sơ có lời khai dương, 24 hồ sơ không có (pr1055, pr1065, pr1118, pr1137, pr621, pr666, pr680, pr689, pr696, pr701, pr703, pr707, pr714, pr718, pr721, pr732, pr765, pr778, pr864, pr881, pr924, pr931, pr950, pr963). Áp hồi tố L-7 ⇒ 49/49 hồ sơ landed ĐỎ ⇒ hằng miễn trừ L-7 cần 49 mục.
  de_xuat: Ghi số này vào đặc tả và cộng khoảng 50–100 dòng (dict cộng bản chép trong test) vào ước lượng đợt B.
- id: F11
  severity: P3
  vi_tri: Dòng 58, 136, 142, 144, 259, 266–267, 105, 397–398
  van_de: Một số câu định nghĩa và phạm vi chưa chặt.
  bang_chung:
    (a) Câu "cùng biên token với `RE_KHAI_DO`" sai: `RE_KHAI_DO = \s*measured(?:\s|—|-|:)` (`land_evidence_nguon.py:104`) không có `passed`, `(` hay hết chuỗi.
    (b) Lời khai `measured` mà không có THƯ MỤC provenance thì đã ném `KhongDoDuoc` ở `land_evidence_nguon.py:255`, trước khi L8 chạy ⇒ kết quả là KHÔNG ĐO ĐƯỢC chứ không phải ĐỎ như Q3/C3.
    (c) pr945 có 2 tệp `ci-provenance-*.yaml` mang schema `ci_provenance/1` nhưng vẫn bị xếp vào bảng B; chưa rõ "provenance" định nghĩa theo tên tệp hay theo schema.
    (d) C-M1 không nói cổng làm gì khi không nạp được module, trong khi B-M1 nói rc 3.
    (e) Chốt đường dẫn của D2b thiếu luật symlink/resolve.
    (f) Job `not_run` (runner_id 0) không có trong `log_day_du` (`ci_provenance.py:385`), nên K3 không đạt được; chưa nói `failed` hay `not_measured` thắng.
    (g) A-M3 "Không sửa mục khác" không có phép đo nào làm nó ĐỎ (trái L3).
    (h) `tu_do` = 16 không tái lập được: ra 18 nếu đếm mọi tệp được trích, 13 nếu chỉ đếm tệp gate-output/kiem-gate.
  de_xuat: Sửa câu chữ, chốt từng điểm, và thêm ca cho (b), (d), (f).
- id: F12
  severity: P3
  vi_tri: `kich_thuoc` đợt A (dòng 238)
  van_de: Ước lượng "test ~250 dòng" thấp hơn tỷ lệ test/module của mọi cổng `ops/` cùng loại, nên khả năng vượt trần 450 dòng là cao.
  bang_chung: Tỷ lệ hiện tại: `land_evidence_nguon` 719/412 = 1,75; `kiem_ho_so_land` 418/177 = 2,36. Module ~180 dòng ⇒ test ~315–425 ⇒ tổng ~496–606. Numstat lúc tạo tệp không đo được vì clone nông (các commit thêm tệp là graft).
  de_xuat: Ghi rủi ro này, và xét trước phương án tách fixture hoặc tách ca ra đợt sau.
- id: F13
  severity: P3
  vi_tri: Định dạng `gate_output/2`, dòng `MOC_GATE_OUTPUT` (dòng 94); đoạn "Ranh giới tin cậy" (dòng 117–123)
  van_de: Dòng `MOC_GATE_OUTPUT: passed` khai trọn mốc Gate output của §10.2.2, trong khi chỉ đo marker và conclusion.
  bang_chung: §10.2.2 (`docs/PROTOCOL_DA_PHIEN.md:949`) đòi job/check-run, runner/OS/runtime, command/rc, marker và artifact ID/hash. Định dạng mới không có runner/OS/artifact và cũng không đối chiếu chúng. Trong khi đó provenance có sẵn `labels`, `runner_name`, `image`.
  de_xuat: Đối chiếu `labels`/`image` với provenance, hoặc ghi rõ L8 là điều kiện CẦN, chưa phải ĐỦ, cho mốc này.
## Đã đo lại, khớp
- Ba cổng:
  · `land_evidence_nguon --root .` ⇒ `98 ĐẠT · 25/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 123`, TỔNG ĐẠT;
  · `kiem_ho_so_land` ⇒ `49/49 … 0 miễn trừ · rc=0`;
  · `rg "gate_output|provenance" ops/kiem_ho_so_land.py` = 0 dòng;
  · vị trí trong mã: D2 ở dòng 3475, `DAT_MOC` dòng 3095, `kiem_ho_so` dòng 243, `importlib.util` dòng 34.
- Hồ sơ và provenance:
  · 123 hồ sơ; 27 hồ sơ có `provenance.yaml` `ci_provenance/1` (32 tệp);
  · 753 job `not_measured` + 1 `failed` (pr957 r27 40437650224), 0 job `passed`;
  · cả 34/34 tệp `ci_provenance/1` có `log_day_du`, và tập khoá = tập job không skipped.
- Dạng tệp đo bổ sung:
  · `danh_gia` 6 hồ sơ; `tom` 7 hồ sơ (3 hồ sơ chỉ có tom: pr1095, pr1128, pr1141);
  · 7 bản sao `danh_gia_gate.py`, cùng sha256 `b87f9697…`; chuỗi marker bị cắt `m[:90]`; `LUAT` của `gate (` có 18 bước;
  · nguyên mẫu `tom_gate_output.py kiem`: chỉ pr1127 rc 0, 7 tệp còn lại rc 1; job `gate (ubuntu-latest)` của pr1127 có 7 marker.
- Bảng A: 21 hồ sơ / 24 lời khai dương; cột *L-6 nay* khớp 21/21; cột *neo* khớp 21/21 (từ pr1095 2/2 tới pr631 1/2).
- #1127, ba blob `bb47274` / `936744e` / `7f22121`: `ĐẠT` ở `land_evidence_nguon --tep` và `DAT` ở `kiem_ho_so_land`.
- `kiem-dong-wp` trên `bien-ban-m8.yaml` của #1120 (dùng chính biên bản thay cho lease) chỉ thiếu D4 ⇒ D2 nhận lời khai `passed`.
- Ruff 0.17.3 `--select F`: `packet_loop.py` 1 lỗi (F841), `packet_loop_test.py` 2 lỗi (F541), năm tệp còn lại 0.
- `ai-dang-giu`:
  · đợt A: cả ba đường dẫn `NGƯỜI_GIỮ 0`;
  · đợt B: `NGƯỜI_GIỮ 0`, kèm ba lease `HẾT_HẠN` wp752-r4-g1, wp981-r1-g1, wp981-r2-g2;
  · đợt C: `CÒN_HẠN wp1240-r1-g1-claude`, rc 11, `lease_until 2026-11-06T17:32:53Z`;
  · đợt D: `NGƯỜI_GIỮ 0`.
- #1210 r2: write set gồm `packet_loop.py` và `packet_loop_test.py`, nạp `_url_hop_le` qua importlib; `TIEN_TO_URL`, `MANH_URL`, `_url_hop_le`, `_menh_de_truot` có ở `kiem_ho_so_land.py:35–59`.
- Job `gate-registry` checkout với `fetch-depth: 0` (`ci.yml:1060`), nên ca phản chứng đọc blob cũ chạy được trong CI. Kích thước test hiện có: 719 và 418 dòng.
- Không đo được (không có mạng): "755 nhánh" từ `ls-remote`.
KET_LUAN: changes_requested