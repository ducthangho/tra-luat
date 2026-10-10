# wp685 r28 g5 attempt 1: báo cáo executor subagent

- Packet: #685 `wp685` (`LAUNCHER-CON-SONG-ESRCH`), Mission #686, revision 28, generation 5, attempt 1.
- Checkout: `$SP/wt-685-g5`, nhánh `agent/wp685-r28-g5-claude`, HEAD `ab457c6` (chưa commit, cây có 2 tệp sửa).
  Theo chỉ thị, subagent không commit, không push và không đăng gì lên GitHub.
- Bắt đầu 04:12:49Z. Mọi đo đạc xong lúc 04:33:56Z. Hạn là 05:42:49Z, nên không chạm điều kiện dừng vì hết giờ.
- sha256 của ứng viên (cây làm việc): `launcher.py` `01a9f0e1…d0b1cb`, `launcher_test.py` `87168ddeb0d3…7966`.
  Các log ghi `git rev-parse HEAD` = `ab457c6` cộng hai sha256 này, vì ứng viên chưa có SHA commit. **Phiên điều phối
  phải chạy lại B1–B6 và B8 trên exact SHA sau khi commit**, hoặc ít nhất đối chiếu sha256 hai tệp bằng hai số trên.
  Đặc tả đòi log neo exact candidate SHA, và subagent không tạo được SHA ấy.

## Preflight
- Đặc tả `ops/specs/launcher-con-song-esrch-r28.md` (từ `origin/claude/wp685-r24-doi-executor`): sha256 `8007edf4…e156`, khớp.
- Prompt `ops/prompts/wp685-r28-g5-claude-20261009.md` @ `5f77db6`: sha256 `d3b8cdf5…62ca`, khớp.
- Lease `wp685-r28-g5-claude-20261009`, so các trường closure với đặc tả: `spec_hash` và `spec_sha256_required` = `8007edf4…`;
  `write_set` và `effective_write_set` là đúng hai đường; `effective_review_class: sensitive`; `change_policy_sha: null`;
  `mission_issue: 686`; `write_set_hash` `0a2ec511…` (cách thứ nhất). Mọi trường **khớp**.
- Ba khối mã nhúng trích bằng máy đều khớp băm: `chot_tinh_r12.py` 412 dòng `add42b31…35b6`, khối B8 353 dòng
  `60ee8d5f…75ff`, `kiem_nhan_r12.py` 19 dòng `13f7728d…3b45`.
- Hậu tố `t` lớn nhất trên nền `ab457c6` là `t155`, nên các ca mới là `t156`–`t161`.

## numstat (`git diff --numstat` so `ab457c6`)
| tệp / phần | + / − |
|---|---|
| `launcher.py` (Q-A ở `_con_song`, Q-A.7 latin-1 ở 5 chỗ đọc, chú thích nguồn) | +33 / −5 |
| `launcher_test.py`: `import errno` | +1 |
| `launcher_test.py`: `_con_song_that` đọc bytes (+1 chú thích) | +3 / −2 |
| `launcher_test.py`: helper t156/t157 cộng 2 ca | ≈ +521 |
| `launcher_test.py`: khối B8 r12 nguyên văn (353 dòng) và dòng nối | ≈ +355 |
| `launcher_test.py`: 54 mục `DOT_BIEN` (4 dòng mỗi mục) cộng 1 dòng chú thích | +217 |
| **tổng, 2 tệp** | **+1129 / −7**. Dưới trần 1400 (ADR-0044, ngoại lệ chủ kho); 2 tệp, dưới trần 3 |

## Thay đổi theo mục đặc tả
- **§6.1, Q-A.1–6** (`_con_song`): phép hỏi `exists()` chạy đúng 1 lần trong `try`. `ProcessLookupError` ⇒ `False`;
  `OSError` khác ⇒ `co_tep=None`, không kết luận. Nhánh tệp có (Đ0) giữ nguyên xi, chỉ đổi lời đọc. Đường mới (Đ) đọc
  1 lần và tách theo `)` cuối; `(OSError, ValueError, IndexError)` ⇒ `pass`, rồi rơi xuống khối `os.kill(pid, 0)` của nền.
  Khối kill dùng chung cho K và K0. Không có `except Exception/BaseException` và không bọc lại ngoại lệ.
  Không có hàm trợ giúp mới, nên `DS-E-C3` không áp dụng.
- **§6.3, Q-A.7**: dạng đọc được chọn là `read_text(encoding="latin-1")`, khai ở `DANG_DOC_QA7` (hằng có sẵn trong khối B8).
  Dạng này áp ở 5 chỗ đọc: `_khoa_danh_tinh`, `_thanh_vien_nhom`, `_chup_cay` và 2 khối của `_con_song`.
  `git grep -n 'linux:'` ra đúng 2 chỗ dựng khoá, `:365` và `:499`, đều theo định dạng nền.
  `_con_song_that` đọc bytes.
- **§6.2, §7 B1–B4**: thêm helper theo nhãn `_cs_chay_t156(m, chay=None, noi=())` và `_cs_chay_t157`, gồm 17 nhãn,
  48 tiểu nhãn, 57 đơn vị. Thứ tự cố định, tiểu nhãn và loại assertion đúng chuỗi của đặc tả. Seam `Path.stat`,
  `Path.exists`, `Path.read_text` và observer `os.kill(pid,0)` khoá theo đúng `/proc/<pid>/stat`, đều có bộ đếm và
  ghi `read args`. Exception được phân bốn loại ghi nhận theo danh tính, có `__cause__` và không tính `__context__`.
  Payload theo dõi `_CsChuoi`/`_CsDanhSach` dùng cho `B2-parse`. Hai đầu vào nội dung thật có điều kiện dựng là
  `prctl` 15 byte và `read_text()` không đối số phải ném `UnicodeDecodeError` ngoài cửa sổ đếm. Trên nền
  không phải Linux, hai ca trả chuỗi BỎ QUA.
- **§7 B8**: khối r12 chèn nguyên văn, gồm `t158`–`t161` và `DANG_DOC_QA7`.
- **§7 B5**: thêm 54 mục `wp685_<dòng>_…` vào cuối `DOT_BIEN`, từ (a) đến (m5). Mục (c) có hai đích, tổng 55 cặp.
  Sau đó `DOT_BIEN` có 228 mục cộng harness 3. Tổng số ca là 195.

## Nghiệm thu (log ở `$SP/x685g5/log/`; mỗi log mở bằng khối môi trường (a)–(d) kèm giờ UTC)
Môi trường: Linux `6.18.44-fc-v114` x86_64, `ID=ubuntu`, `VERSION_ID="24.04"`, Python 3.11.15 và 3.12.3.

| tiêu chí | lệnh / log | rc | kết quả |
|---|---|---|---|
| B1–B4, B8 (ứng viên) | `sau_ca.sh` (`--lap-ca tNNN --lan 1` × 6) · `B1-B4_B8_ung_vien_python3.1{1,2}.log` | 0 | 6/6 QUA ở cả 3.11 và 3.12 |
| B1–B4, B8 (nền, test ứng viên) | `B1-B4_B8_nen_python3.1{1,2}.log` | 1 | 6/6 ĐỎ đúng loại: `B1 seam escaped`, `B3b-giet-cay seam escaped`, `B8-sau-sinh 124 noi doi`, `B8-luc-sinh qua han khong giet duoc` (rc=10), `B8-setsid 124 noi doi`, `B8-me-thoat 124 noi doi` |
| B2 chốt tĩnh | `python3.11 chot_tinh_r12.py` (sha256 `add42b31…35b6`) · `B2_chot_tinh_python3.11.log` | 0 | `UNG VIEN: DAT`, 13 đối chứng `DO DUNG LUAT` (`K` không áp dụng cho dạng latin-1), `KET LUAN: DAT \| rc=0` |
| B4 sàn Windows (ước lượng tĩnh) | `san_windows.py` · `B4_san_windows.log` | 0 | nền 11/177; ứng viên 65/231 không đo được, 71,86 %, biên 4 (khớp số của đặc tả) |
| B5 A/W | `bang_chung_aw_d.py … all` · `B5_AW_D_python3.1{1,2}.log` | 0 | **55/55 cặp đạt** ở cả hai Python. W0 sống, bộ đếm ≥ 1. Mỗi dòng ghi A1/A2/W1/W0 |
| B5 D | cùng log | 0 | bản đúng XANH (57 đơn vị, đúng thứ tự); **65/65 control đỏ đúng**; 6/6 phép đảo đỏ |
| B5 (E) | `bang_chung_e.py` · `B5_E_python3.1{1,2}.log`, bảng `bang_E_python3.1x.json` (sha256 `b945c96c…2ce0`) | 0 | **118/118 đạt** = 83 + 35, tập tên khớp danh sách ĐÓNG trích từ đặc tả (thiếu=[], thừa=[]). Biến thể thay thế đỏ vô can ở A1/W1/W0; 8 đối chứng `B2-parse` cộng `dc_j1` vô can; 2 đối chứng sống có nhân chứng dương (ENOMEM ⇒ `OSError errno 12` so với ứng viên `True`; số `os.kill` 1 so với 2) |
| B6 suite, delta | `B6_suite_{nen,ung_vien}_python3.1{1,2}.log`; hai vế dựng trong MỘT lệnh (clone `--shared` ×2 ở `ab457c6`, rồi chép hai tệp ứng viên) | 3.11: 0/0 · 3.12: 1/1 | 3.11: nền 188/188, ứng viên 194/194. 3.12: nền 187/188, ứng viên 193/194; ca đỏ duy nhất là `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` ở CẢ HAI vế (đỏ sẵn, phụ thuộc môi trường). **Delta = 0** |
| B6 `--dot-bien` | `B6_dotbien_*_python3.1{1,2}.log` | 0 | nền `176/176 dat (1 khong do duoc)`; ứng viên `230/230 dat (1 khong do duoc)` ở cả hai Python. 0 mục cũ đổi hạng; 54 mục mới đều `OK` (c: `giet 2/2`) |
| B6 ruff F | `ruff 0.15.8 check --select F --target-version py311` · `B6_ruff_*.log` | 1/1 | nền và ứng viên đều 5 F841, cùng 5 lỗi (chỉ lệch số dòng +2). **Delta multiset = ∅** |
| B7 | — | — | KHÔNG CHẠY. Đây là bằng chứng, không phải cổng. Lý do: ưu tiên B1–B6 và B8 |

Tập lệnh bằng chứng (sha256): `bang_chung_aw_d.py` `5e6a3307…adee2`, `bang_chung_e.py` `c71e1a8b…87f2`,
`sinh_dot_bien.py` `b51ac77e…5d2a`, `san_windows.py` `9af6cbde…ae0`, `chay_log.sh` `18079ffe…56cf`, `sau_ca.sh` `774fe879…4486`.
Ánh xạ tên (E): tên biến thể trùng đúng khoá ở mục 6. Các biến thể k0_* và k_* là các cặp giống nhau về mã, vì
ứng viên dùng chung một khối kill (xem điểm mơ hồ 3).

## Điểm đặc tả mơ hồ và cách đọc
1. **A1 cho phép chết ở nhãn đứng trước.** (c), (j1), (j2), (k1), (k5) chết ở A1 tại một nhãn sớm hơn, ví dụ (j1) chết
   ở `B2-eacces read count 2`. Nguyên nhân là quy ước đếm r7 đặt `read/kill count` ở mọi đầu vào. Ở W1 cả năm dòng chết
   đúng nhãn, tiểu nhãn và loại. Tôi đọc cách này là hợp lệ theo bảng A1.
2. **Phân hạng D.** Hai loại control được dựng **lúc chạy trên bản nạp lại của tệp test**, không phải bằng sửa văn bản
   tệp. Control (i) gán `__defaults__` của helper. Control (ii) bọc `_CsNhan.kiem` để bỏ đúng một (nhãn, tiểu nhãn).
   Tôi coi đây là "bản sao test" theo nghĩa rộng.
3. **(E) với khối kill dùng chung.** `k_ok_sai`/`k0_ok_sai`, `k_<tv>_boc`/`k0_<tv>_boc` và `k_<tv>_thaythe`/`k0_<tv>_thaythe`
   là cùng một thay đổi ở cùng vị trí, vì chỉ có một vị trí. `k0_<tv>_bat` trùng mã với (l25)–(l29), và `luot6_m*` trùng
   (m1)–(m5). Khác nhau chỉ ở đích kỳ vọng: W1 ở nhãn `B2-nhanh-cu vang-*` hay ở nhãn của tầng K.
4. **fp2–fp6b.** Định nghĩa gốc nằm ở r8, không có trong r28. Tôi tự dựng 8 đối chứng: mỗi cái ném một `ValueError`
   mới không qua payload theo dõi, gồm `int("…")`, `"".rindex`, `str(payload).rindex`, vòng thử lại trên `""`, v.v.
   Cả 8 vô can ở A1/W1/W0.
5. **Seam đọc.** Seam trả payload hay ném thì thay cả lời gọi. Seam chỉ đếm thì chuyển tiếp thật. Seam ném một đối
   tượng dựng sẵn và tái dùng cùng đối tượng ở mọi lần chạm. Hàm theo lần chạm, dùng cho `B2-dem-lan`, cũng ghi đối
   tượng nó tạo vào tập "do seam tạo".
6. **Neo exact SHA.** Ứng viên chưa được commit. Log neo vào HEAD `ab457c6` cộng sha256 hai tệp (xem đầu báo cáo).
7. **`copyable_prompt.md`**: tôi điền `GATE_TIER` = T3, vì packet `sensitive` và có thay đổi launcher. Đây là phán
   đoán; mẫu không quy định giá trị. `PR_URL` và `HEAD_SHA` để trống cho phiên điều phối điền.

## Điều kiện dừng gặp phải
Không gặp. Không vượt trần, không lệch lease, chốt tĩnh không đỏ, không có delta. Mọi tiến trình con đều được
`wait`. Sau các lượt đo, `ps` không còn tiến trình con nào của ca. Phần của tôi trên đĩa là `$SP/x685g5` ≈ 0,7 GB, gồm
3 rig clone `--shared`.
