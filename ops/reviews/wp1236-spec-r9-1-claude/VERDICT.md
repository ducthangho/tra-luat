Kết luận: **changes_requested**, với 4 finding P2 và 8 finding P3. Kho không bị sửa: HEAD vẫn `89c07bc`, `git status` rỗng. Script đo nằm trong `work/`. Công cụ Write bị từ chối quyền ghi `work/VERDICT.md`, nên tôi ghi tệp ấy bằng Bash, vẫn trong `work/` như được phép.

- **Câu 1 (mục 1–2 của Issue):** có hai đường để một lời khai dương qua L8 mà không có tệp danh-gia khớp provenance:
  - Một tệp ghi `conclusion=failure -> passed` vẫn qua K1–K8 (R02). Bắt được rẻ từ dữ liệu đã có trong kho, không cần log.
  - Văn xuôi dưới khoá không chứa `gateoutput` không bị đọc. Có tiền lệ thật: pr1065 và pr1118, `landed: true`, căn cứ `0 dong ##[error]` (R04).
- **Câu 2 (số đo):** chạy lại bản tham chiếu ra 47/10/9 và 53/40/77, trùng từng byte, và cả sáu fixture đúng. Nhưng đặc tả viết "không nhận `\r`" trong khi pr1312 và pr1317 là tệp CRLF đúng. Theo chữ đặc tả, số phải là 45/10/11 và 55/38/77, nên A1-2 và A1-3 mâu thuẫn nhau (R01). Ở điểm này bản tham chiếu đúng.
- **Câu 3 (nghiệm thu):** ba đột biến không thể làm ca đích của chính nó đỏ: m13, m20 và mC1 (R03). m1 chỉ chết vì chuỗi lý do đổi (R06).

# VERDICT wp1236 r9 vòng 1
spec_sha256: ba466e72bb86c33462847c9ab92469d44acbf6bcc81b4443179d33c2e00940e7
## Findings
- id: R01
  severity: P2
  vi_tri: Thiết kế › doc_danh_gia (dòng 62 "không nhận `\r`"); A1-3 (dòng 202, biến thể `\r\n`) và A1-2 (dòng 189, 201: 47/10/9); MIEN_TRU_L8 (dòng 126: 53/40/77)
  van_de: Hai ca nghiệm thu mâu thuẫn nhau trên dữ liệu thật. Hai tệp danh-gia đúng (pr1312, pr1317) lưu CRLF. Chữ đặc tả loại chúng, bản tham chiếu (`read_text`, newline phổ quát) lại nhận, nên không bản thi công nào qua được cả A1-2 lẫn A1-3.
  bang_chung: `grep $'\r'` trên 66 tệp ⇒ đúng 2 tệp, mỗi tệp 27 CR ở cuối MỌI dòng; `git ls-files --eol` ⇒ `i/crlf w/crlf attr/-text`. Bản sao `thamchieu.py` đọc byte rồi loại `\r` (`work/cr/`) ⇒ `Counter({'passed': 45, 'not_measured': 11, 'failed': 10})`; L8 ⇒ DO 55 / DAT 38 / KHONG_LOI_KHAI 77, pr1312 và pr1317 chuyển DAT→DO. Bộ sinh ghi bằng `open(ra, "w")` ở chế độ văn bản, nên chạy trên Windows sẽ ra CRLF.
  de_xuat: Bản tham chiếu đúng. Nhận tệp mà MỌI dòng kết thúc bằng `\r\n` (chuẩn hoá về `\n`); loại `\r` lẻ hoặc tệp trộn hai kiểu xuống dòng, với lý do có tên. Đổi biến thể A1-3 thành "`\r` lẻ giữa dòng" hoặc "trộn LF/CRLF". Nếu giữ luật chặt thì phải sửa thành 45/10/11 và 55/38/77, thêm pr1312/pr1317 vào `MIEN_TRU_L8`, và ghi hệ quả cho tệp sinh trên Windows.
- id: R02
  severity: P2
  vi_tri: K5 (dòng 83), K7–K8 (dòng 85–90); chua_do_duoc gạch 1 (dòng 297–300)
  van_de: K5 bắt `conclusion` của dòng job bằng provenance nhưng không buộc trạng thái tính ra khớp nó. Tệp ghi `conclusion=failure -> passed` vẫn qua K1–K8, dù chính provenance trong kho cho thấy job ấy thất bại. Không cần log để bắt trường hợp này, nên lý do "log không nằm trong kho" ở chua_do_duoc không áp được.
  bang_chung: Bản sao T-fail (`work/v1/`): lật dòng job 136203672900 từ `-> failed: conclusion=failure` sang `-> passed: x` và dòng tổng sang `passed (39/39 …)` ⇒ `kiem_tep` của bản tham chiếu = `('passed', [])`. Cả ba bộ sinh có `if j["conclusion"] != "success": tt, ct = "failed", …`. Trên 66 tệp: 1956 dòng `-> passed` đều `conclusion=success`; 11 dòng non-success đều `-> failed` ⇒ thêm chốt không chặn oan tệp nào.
  de_xuat: Thêm vào K5: `-> passed` ⇒ `conclusion == "success"`; non-success ⇒ `-> failed` (lý do `ket_luan_lech:<id>`). Thêm ca dùng bản sao T-fail lật như trên, kèm một đột biến gỡ chốt. Biến thể A1-6 "đổi conclusion" nên đổi failure→cancelled trên dòng failed để m8 vẫn chỉ có một ca đích. Thu hẹp câu ở chua_do_duoc thành "chỉ lật được not_measured→passed trên job có conclusion success".
- id: R03
  severity: P2
  vi_tri: A1-8 (e) + m13 (dòng 207); A2-2 + m20 (dòng 213); C1 + mC1 (dòng 244)
  van_de: Ba đột biến không thể làm ca đích của chính nó đỏ, trong khi đợt A đặt luật "đỏ khi bất kỳ đột biến nào sống". Ai thi công đúng chữ đặc tả cũng không qua được nghiệm thu.
  bang_chung: `python3 -I work/thu_m13_m20.py`: `"44669622916" == 44669622916` là False ⇒ m13 (`==` thay `type is int`) vẫn ra `provenance_0`, tức SONG. Biến thể giết được m13: `run_id: 44669622916.0` hoặc `attempt_yeu_cau: true`. m20 (bỏ lookahead) cho cùng kết quả trên cả sáu đầu vào A2-2 (`measuredx` ⇒ greedy ra `measuredx` ∉ tập ⇒ None ở cả hai) ⇒ SONG; `measured1`, `measured/x`, `passed!` thì giết được. C1 chỉ đòi D2b vắng mặt, nên mC1 (D2b không chạy) không làm C1 đỏ. Phụ thuộc cách dựng: m22 sống nếu đích `../pr1453…` không có trong cây tạm hoặc còn chốt chứa sau `resolve()`; m23 sống nếu symlink trỏ ra ngoài thư mục; mC6 sống nếu đích `..` không phải danh-gia hợp lệ.
  de_xuat: Đổi (e) sang `run_id` float hoặc `attempt_yeu_cau: true`. Thêm `measured1` ⇒ None vào A2-2 làm đích m20. Gán mC1 cho C2, hoặc thêm vế dương cho C1 (in dòng `D2b ĐẠT`). Ghim cách dựng A2-4: `hau-due-x/../danh-gia-gate-output-44669622916.txt` có thật trong thư mục (đích m22), symlink nội bộ trỏ danh-gia hợp lệ (đích m23). Ghim C5: đích `..` là bản sao T-v3-pass hợp lệ nằm ngoài `ops/land/`.
- id: R04
  severity: P2
  vi_tri: Thiết kế › loi_khai (dòng 93–95); Hệ quả 2 (dòng 136); "Ý tưởng một dòng" (dòng 49); chua_do_duoc
  van_de: L8 chỉ đọc khoá có tên chuẩn hoá chứa `gateoutput`. Một hồ sơ mới vẫn khai được gate output dương bằng văn xuôi dưới khoá khác, căn cứ `##[error]`, với `landed: true`, và qua L8. Hệ quả 2 ("chỉ trích … `##[error]` ⇒ ĐỎ") viết vô điều kiện nên rộng hơn phép đo, và đặc tả chưa khai giới hạn này ở đâu.
  bang_chung: Hai tiền lệ thật nằm trong nhóm 77 "không có lời khai": `pr1065-vm-cap-nhat-cong-cu` và `pr1118-ghi-so-bo-sung-1065`, `trang_thai_packet.landed: True`, `landed_dieu_kien: '… (1) gate tren merge SHA 3dfb973: DAT — bon moc §10.2.2: … Gate output (… 0 dong ##[error] tren 23 log …)'`. Quét 77 hồ sơ ấy: 40 hồ sơ có chuỗi nhắc "gate output" kèm passed/measured/DAT dưới khoá không chứa gateoutput.
  de_xuat: Ghi vào chua_do_duoc và docstring L8: "lời khai văn xuôi dưới khoá không chứa gateoutput không được đọc", theo tiền lệ L7 của cùng tệp ("Lời khai văn xuôi … KHÔNG đọc được, không bắt"). Viết lại Hệ quả 2 có điều kiện. Chuyển lớp này sang L-7 (hồ sơ `landed: true` phải có lời khai gateoutput có cấu trúc). Không lọc văn xuôi bằng regex: đó là bài học F12 của r7/r8.
- id: R05
  severity: P3
  vi_tri: dòng 30, 57, 127–129, 158, 201, 263–264
  van_de: Một số con số sai, đều không làm đổi kết luận.
  bang_chung: Script v1 có 20 bản, tổng 50 (đặc tả ghi 19 và 49), đo bằng `sha256sum` và `git ls-files`. Phân rã lời khai là 39 dương-không-tệp, tổng 71 (ghi 36 và 68), vì đếm trên `do_loi_khai.txt` đã cắt ở 230 ký tự, làm dòng pr1042 bị cụt; số hồ sơ 53/40/77 không đổi. m37 làm đổi trạng thái 4/6 tệp, không phải 6/6: pr1055 và pr1142-41388158239 có dòng tổng `not_measured`; A1-2 vẫn đỏ (50/11/5). Không có m38 nào, nên chỉ có 38 đột biến. `thamchieu.py` có tất cả 88 dòng, nên không thể có "phần 95 dòng".
  de_xuat: Sửa các số này; định nghĩa m38 hoặc đổi tổng thành 38.
- id: R06
  severity: P3
  vi_tri: A1-1 m1 (dòng 200); hinh_dang_ke_thua dòng 293
  van_de: m1 không làm T-skip ra `passed`. Cả ba tệp `co_job_skipped` đều còn một dòng job `not_measured`. Như vậy luật K8 "skipped ⇒ not_measured cho mọi phiên bản" chưa có ca nào mà gỡ luật thì trạng thái lật sang passed; m1 chỉ chết vì chuỗi lý do đổi.
  bang_chung: Bản sao `thamchieu.py` bỏ nhánh `co_job_skipped` (`work/m1/`) ⇒ cả ba tệp ra `('not_measured', ['check_bat_buoc:gate-packet-loop (ubuntu-latest)'])`.
  de_xuat: Thêm biến thể T-v2-pass có thêm một job skipped ngoài `CHECK_BAT_BUOC_TEN` (cả tệp lẫn provenance, dòng dạng v2, sửa dòng tổng) ⇒ `co_job_skipped`; dưới m1 ⇒ `passed`. Sửa chú thích "(T-skip ra passed)".
- id: R07
  severity: P3
  vi_tri: MIEN_TRU_L8 (dòng 125–131); B1/mB1 (dòng 233)
  van_de: Đặc tả không nói L8 chạy trước hay sau `MIEN_TRU_CUTOVER`. 8/53 hồ sơ L8-ĐỎ đã được miễn cutover với băm khớp, nên trong cổng thật L8 không chạy trên chúng. Nếu `MIEN_TRU_L8` chứa các hồ sơ ấy, xoá một trong số đó (mB1) vẫn ra rc 0, tức đột biến sống.
  bang_chung: pr594, pr680, pr684, pr689, pr696, pr701, pr703, pr707 có băm == `MIEN_TRU_CUTOVER` (pr679 lệch băm nên vẫn được kiểm); `land_evidence_nguon.py --root .` ⇒ `25/28 miễn trừ`.
  de_xuat: Ghi rõ L8 chạy sau chốt cutover, nên `MIEN_TRU_L8` = 45 mục; mB1 xoá một mục không thuộc cutover.
- id: R08
  severity: P3
  vi_tri: K2/K3 (dòng 71–79)
  van_de: Cổng không đọc cờ toàn vẹn của chính provenance (`moc.run.trang_thai`, `tap_jobs.trang_thai`, `checkout[*].trang_thai`), nên K4 có thể so trên một tập job chưa đủ.
  bang_chung: `work/do_cohieu.py`: 47/47 tệp passed có ba cờ đều passed và `run_attempt` == attempt ở header ⇒ thêm chốt không chặn oan tệp nào.
  de_xuat: Đưa ba điều kiện vào K3 (lý do `provenance_chua_du`), kèm một biến thể và một đột biến.
- id: R09
  severity: P3
  vi_tri: doc_danh_gia, A1-3, A1-11, A2-10, kiem_ho_so, D2b, B4, A1-9
  van_de: Một số chỗ chưa định nghĩa, mà ca kiểm lại đòi "đúng lý do" hoặc "rc đúng bảng".
  bang_chung: Dòng 1 không khớp và `\r` chưa có tên lý do (bản tham chiếu dùng `dau_tep_sai`). A1-11 không nói có sửa dòng tổng không; không sửa thì có thêm `moc_lech`. Chưa định rc CLI cho tệp vắng hay YAML hỏng. Chưa ghi đường dẫn trích tính từ đâu (122/122 trích dẫn thật tương đối với `thu_muc`). Thư mục provenance của D2b chưa định. L8 nạp module từ `ROOT`, nên B4 phải chép script vào gốc tạm. `ast.literal_eval` trên `CHECK_BAT_BUOC` ⇒ `ValueError malformed node` (giá trị là `tuple(genexpr + f-string)`).
  de_xuat: Đặt tên các lý do; ghi base là `thu_muc`; D2b dùng `ops/land/<thành phần đầu>` (tận cùng `-provenance`); định rc CLI; B4 chép script; A1-9 dùng `eval(compile(ast.Expression(node.value)…), {"__builtins__": {"tuple": tuple}})` hoặc nạp module.
- id: R10
  severity: P3
  vi_tri: Hệ quả cho hồ sơ mới (dòng 133–138); A2-11 (dòng 222)
  van_de: Thiếu ba hệ quả. (1) Lời khai dương về run PR hoặc dispatch Windows luôn ĐỎ qua K3. (2) Tên tệp danh-gia phải nằm trong chính chuỗi lời khai; danh sách `nguon:` riêng không tính. (3) A2-11 lệch Issue mục 3 (bản SAU #1235 phải ĐẠT) mà chưa khai.
  bang_chung: `pre_merge_checks` có 5 lời khai `measured — gate-output-<run>.txt` của run PR/Windows (pr1023, pr1042 ×3, pr1063). `git show 7f22121:…pr1127…yaml` dòng 51 dẫn `ci/gate-output-41356691133.txt` dạng tom.
  de_xuat: Thêm ba gạch vào Hệ quả, và ghi độ lệch so với Issue mục 3 vào ngoai_pham_vi.
- id: R11
  severity: P3
  vi_tri: khối `nang_tran` (dòng 266–272)
  van_de: Khối thiếu ba trường ADR-0053 đòi: `ai_nang`, `tran_cu`, `tran_moi` (đang dùng `dot`, `tran_de_nghi`, `thay_the`).
  bang_chung: `docs/adr/0053…md` dòng 34–37; r8 dòng 808–811 dùng đúng mẫu.
  de_xuat: Thêm `ai_nang: ducthangho (chờ duyệt băm)`, `tran_cu: {tep: 6, dong_them: 450}`, `tran_moi: {tep: 3, dong_them: 650}`; giữ `thay_the`.
- id: R12
  severity: P3
  vi_tri: L8 (dòng 122); D2b (dòng 123)
  van_de: (a) `kiem_ho_so(Path)` đọc và parse hồ sơ lần thứ hai, trái docstring L4 ("Băm L5 và luật đo trên CÙNG một lần đọc"), và bỏ qua `nap_yaml` vốn chặt hơn. (b) D2b nạp module từ origin/master nhưng đọc danh-gia và provenance từ cây làm việc, nên tệp chưa commit hoặc đã sửa cục bộ vẫn qua.
  bang_chung: `ops/land_evidence_nguon.py` dòng 25–26 (L4), `nap_yaml` dòng 214–245; `_canon` chỉ chép các tệp trong CANON từ origin/master.
  de_xuat: (a) Cho API nhận dữ liệu đã nạp: `kiem_ho_so(du_lieu, thu_muc)`, còn CLI tự đọc. (b) D2b đòi tệp được track và trùng `refs/remotes/origin/master`, hoặc khai giới hạn này ở chua_do_duoc.
## Đã đo lại, khớp
- sha256 SPEC.md khớp; repo HEAD `89c07bc`, `git status` rỗng trước và sau.
- `thamchieu.py` chạy lại ⇒ trùng byte `do_tep.txt`: 47/10/9 (6 `provenance_0`, 3 `co_job_skipped`). `do_loi_khai.py` ⇒ trùng byte: 53/40/77 = 170.
- 66 tệp theo sha dòng đầu: v1 29, v2 35, v3 2; ba băm `BO_SINH` là sha256 của ba bản script có thật.
- Sáu fixture A1-1 đúng trạng thái, lý do và phiên bản bộ sinh.
- `CHECK_BAT_BUOC` ở `packet_loop.py:2485`, đúng năm tên; `DAT_MOC` = (passed, owner_waived); `RC_STATE` 8, `RC_GATE` 12.
- `ci.yml` có `on.push.branches: [master]` ⇒ K3 đủ để loại run push từ nhánh khác.
- pr1453: 39 job ở cả hai provenance; dòng 106 khai `measured — … FAILED 38/39`.
- bb47274 và 7f22121 có thật, là tổ tiên của 8048551; job gate-registry dùng `fetch-depth: 0` ⇒ A1-2 và A2-11 chạy được trong CI.
- Không có symlink dưới `ops/land`; không có *.yaml hỏng trong 55 thư mục provenance; ngoài `ops/land`, `ops/reviews`, `ops/specs` không mã nào đọc danh-gia ⇒ câu "không cổng nào đọc" đúng (L6(e)).
- Dòng trần ADR-0053@8ab1007 và ADR-0055@d2e3052 hợp lệ (tệp có ở OID, cha không có, không đổi tới HEAD); `pham_vi_e` khai E5 khớp ADR-0067.

KET_LUAN: changes_requested
