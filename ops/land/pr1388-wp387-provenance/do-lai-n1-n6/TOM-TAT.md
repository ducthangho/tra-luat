# Đo lại N1–N6 sau merge — #387 packet A (PR #1388, merge `e4fdf09`)

Chủ kho yêu cầu đo các tiêu chí còn là lời khai để xét `landed`. Phiên điều phối #1206 làm việc này ngày 2026-11-18,
trên Linux với Python 3.13.18. Cây merge, cây base `d1ca71a` (base của lease) và các bản sao đều nằm trong clone sạch ở
scratchpad, `core.abbrev 7`, và `/tmp/.git` không tồn tại.

| tiêu chí | phép đo | tệp | kết quả |
|---|---|---|---|
| N1, (a) đỏ trên base | `launcher_test.py` của e4fdf09 + `launcher.py` của d1ca71a, `--lap-ca r387_m1_chau_ghi_muon_khai_pham_vi_bam --lan 1` | `n1-a-tren-base.txt` | rc 1, `HONG …: TinHieuChotCa: r387(a) cay chua chet ma khai None`, đúng câu spec đòi |
| N1, (a), (a′) đạt | `--lap-ca` từng ca trên cây merge sạch | `do-tay-n1-n2-n3-e4fdf09.json` | rc 0 cả hai |
| N1, đo tay | xoá vế băm khỏi thân (a) trên bản sao | `do-tay-n1-n2-n3-e4fdf09.json`, driver `do_tay_1388.py` | (a′) ĐỎ rc 1: `r387(a') than (a) do o ve khac, khong phai ve bam` |
| N1, đột biến | `--dot-bien` | `dot-bien-e4fdf09.stdout.txt` | `r387_khai_cay_chet_luon_true`, `r387_ket_thuc_sau_vong_cho`, `r387_fixture_gui_tin_hieu_theo_pid_chau`: `OK giet 1/1`, ca (a) |
| N2, (b) đạt | `--lap-ca` trên cây merge sạch | `do-tay-n1-n2-n3-e4fdf09.json` | rc 0 |
| N2, đo tay | xoá dòng gán `log_bam_luc_utc` trong `launcher.py` trên bản sao | như trên | (b) ĐỎ rc 1 bằng `TinHieuChotCa` (`log_bam_luc_utc=None …`), không có `KeyError` |
| N2, đột biến | `--dot-bien` | `dot-bien-e4fdf09.stdout.txt` | `r387_khai_cay_chet_luon_false`, `r387_moc_bam_truoc_khi_con_thoat`: `OK giet 1/1`, ca (b) |
| N3 | 11 ca mới, mỗi ca một tiến trình `--lap-ca` | `do-tay-n1-n2-n3-e4fdf09.json` | 11/11 rc 0; tổng wall 19,14 s (< 25 s; đo gồm cả thời gian khởi động interpreter) |
| N3, đột biến | `--dot-bien` | `dot-bien-e4fdf09.stdout.txt` | mọi mục spec liệt kê `OK giet 1/1` đúng ca đích, gồm neo M5 `xoa_prompt_khi_wrapper_vua_thoat` → `t76` |
| N4, suite | toàn suite trên base | `suite-base-d1ca71a.txt` | base 413/413 (tổng 415, bỏ qua 2); merge 424/424 (tổng 426, bỏ qua 2, xem `../launcher-test-toan-suite-e4fdf09.txt`); tập bỏ qua giống nhau: `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`, `r484_g4_windows_sid_alias_identity` |
| N4, đột biến | `python .claude/dev/launcher_test.py --dot-bien` trên merge, 16:14:24Z–16:26:57Z | `dot-bien-e4fdf09.stdout.txt`, `.rc.txt`, `.bat-dau.txt` | rc 0, dòng cuối `DOT BIEN: 720/720 dat  (6 khong do duoc tren nen nay)`; 720 dòng `OK  giet`; 18 đột biến mới của A (16 + 2 harness) và neo M5 đều OK |
| N4, sáu mục không đo được | so tên mục giữa base và head | `khong-do-duoc-ke-thua.txt` | 5 mục windows (`r1335_N3c_win_giu_argv0_goc`, `r1335_F2_win_path_theo_cwd_launcher`, `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner`, `g2_windows_directory_pin_access`) cùng `124_khi_chau_con_song` (ca đích t62 bị bỏ qua); cả 6 đều có trong `DOT_BIEN` của base |
| N6, ruff | `ruff check --no-cache --select F` hai tệp, ruff 0.17.5 | `ruff-F-d1ca71a.txt`, `ruff-F-e4fdf09.txt` | base rc 1 (5 F841), merge rc 1 (5 F841, cùng mã) ⇒ delta 0 |
| N6, doctor | `launcher.py doctor` trên base và merge, cùng máy | `doctor-d1ca71a.trich.txt`, `doctor-e4fdf09.trich.txt` | rc 0 = rc 0 |
| N6, run.json | một lượt `launcher.py run -- python -c "print(1)"` trên merge | `n6-run-e4fdf09.txt` | `"version": "1.6.1"`; có đủ `log_bam_cay_da_chet`, `log_bam_cho_giay`, `log_bam_luc_utc` |

Ghi chú:
- `dot-bien-e4fdf09.stderr.txt` có 5 dòng `Could not find platform dependent libraries <exec_prefix>`. Đây là cảnh báo của
  interpreter ở các bản sao đột biến, không làm đổi rc hay dòng kết luận.
- Các dòng `r1335 to hop … LECH` trong stdout là chẩn đoán của một ca, in trước bảng đột biến. Chúng không phải mục đột biến.

Chưa đo:
- Native Darwin/Windows (thuộc packet B).
- Phép đỏ của `doctrine-scan`, `adr-song` và `doctor`. Spec ghi rõ packet này không có phép đỏ cho ba lệnh đó.
