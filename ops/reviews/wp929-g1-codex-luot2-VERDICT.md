Verdict: approve
Reviewed commit: 227dcdebc62c9275f9df09056f66e2124ed5f14c
Spec sha256: 79251bee45fc39003d13438d741c4e6319dc80ea6b480dc1b931c93d0c6a7ae6
Reviewed tree: d4ee1762da8bb458ec5d0bc402817dbe610b6a1d
Base origin/master: 5775864b04a18c5afe1aafcbb23e54525ce8a3d8

Không còn P0/P1/P2 trong phạm vi đã review. P2 lượt 1 đã vá thật; giữ một P3 về độ phủ lỗi `ls-tree`, không chặn approve theo ngưỡng của prompt. Verdict chỉ neo commit trên, không xác nhận toàn bộ nghiệm thu N1/N6 hay cấp quyền push/merge/land.

## Trạng thái finding lượt 1

ĐỐI CHIẾU LƯỢT TRƯỚC: nguồn `VERDICT-luot1.md`, SHA256 `8a392561044c0ae6b9d504260149ff441fb8ec81cfe828fd8e06bd8f27c80bbf`, reviewed SHA `8a6d795c982fc7e9da2fbfd28a75ca25d5f3eb95`.

- **wp929-tree-is-not-activation-file: đóng — ĐÃ VÁ THẬT.** Lệnh `python3 -B evidence/behavior_probes.py --focused` rc=0: `r929_thu_muc_ten_md`, `r929_symlink_khong_tinh`, `gitlink_false` đều PASS qua `record-lease`, khẳng định `luat_adr0054=False`. Thư mục `.md` chỉ chứa cụm trong tên con; symlink chỉ chứa cụm trong blob đích; gitlink trỏ commit có cụm trong thông điệp. Lệnh `python3 -B evidence/review_runner.py mutants` rc=0: `r929_bo_kiem_loai_doi_tuong` giết cả ca tree và symlink; `r929_nhan_symlink` giết đúng ca symlink. Output đều là `AssertionError: wp929 ... đòi {'luat_adr0054': False}, được {'luat_adr0054': True}`, tại `_r929_adr` dòng 8460 → `_kiem`. Probe bổ sung `review_accept_gitlink` cũng chết tại khẳng định False/True này. Không có CLI sập hoặc fixture chết trước chốt.
- **wp929-filename-boundaries-unmeasured: đóng — ĐÃ VÁ THẬT.** `python3 -B evidence/review_runner.py baseline` rc=0: `r929_ba_chu_so_khong_tinh`, `r929_duoi_khac_md_khong_tinh` PASS. Lệnh `mutants` trên rc=0: `r929_so_chu_so_tuy_y` và `r929_bo_duoi_md` chết ở khẳng định cuối, cần False nhưng được True; mỗi mutant giữ 3/3 đối chứng xanh. Phạm vi đóng là hai biên chưa được khóa ở lượt 1; các biên parser bổ sung đã đo bên dưới.
- **wp929-nfc-unmeasured: đóng — ĐÃ VÁ THẬT.** Cùng lệnh baseline/mutants: `r929_nfd_van_tinh` PASS; `r929_bo_nfc` → `AssertionError: wp929 ... đòi {'luat_adr0054': True}, được {'luat_adr0054': False}` tại khẳng định cuối; 3/3 đối chứng xanh. Fixture ghi bytes NFD vào blob trước khi chạy lệnh.
- **wp929-git-error-guards-unmeasured: còn mở một phần — P3.** Nhánh `show` ĐÃ VÁ THẬT về độ phủ: `r929_show_loi_la_false` PASS, `r929_bo_rc_show` chết ở khẳng định cuối False/True, 3/3 đối chứng xanh. Nhánh `ls-tree` CHƯA VÁ về độ phủ trong suite của PR; chốt sản phẩm vẫn đúng. Bằng chứng và quyết định giữ nợ ở phần dưới.

## Findings mới

Không phát hiện lớp lỗi sản phẩm mới. Phần còn mở giữ nguyên ID của lượt 1, không đếm thành finding mới:

- **[P3] wp929-git-error-guards-unmeasured** — `.claude/dev/packet_loop_test.py:8463–8495` chưa có ca bảo vệ `ls[0] == 0` tại `packet_loop.py:2576`. Đột biến bỏ riêng chốt này vẫn cho **159/159** ca `r812_*`/`r929_*` xanh. Đây là thiếu độ phủ, **không nâng thành P2**: HEAD có chốt đúng và phép đo lỗi thực tế tại ranh giới `_git_do` cho False.

  Lệnh tái hiện: `python3 -B evidence/behavior_probes.py` (bản script đã sửa mỏ neo TAB); hoặc `python3 -B evidence/behavior_probes.py --focused` để chạy các probe mà không lặp 159 ca. Output đã đo:

  ```text
  LS_RC_MUTANT_EXISTING 159/159 passed; skipped=0
  INJECTED ls ... original_rc=0, injected_rc=128, bytes=209
  HEAD_probes fault_ls SONG None
  review_drop_ls_rc_own_targets fault_ls GIET AssertionError: fault ls: đòi {'luat_adr0054': False}, được {'luat_adr0054': True}
  ```

  `SONG None` là nhãn của harness cho ca không có ngoại lệ, tức PASS trên HEAD. Baseline dương đã kiểm True, sau đó cùng fixture/lease được đưa lại qua subprocess `record-lease`. Wrapper chỉ đổi rc của đúng lệnh `ls-tree -z refs/remotes/origin/master docs/adr/` thành 128, giữ stdout Git thật; khẳng định wrapper chạy đúng một lần. Fetch, validator và dữ liệu lease vẫn nguyên vẹn; CLI trả rc=0 và state đóng về False. Do đó có cách bơm lỗi qua đường CLI thật bằng instrumentation có mục tiêu, dù phá object trong fixture trước fetch có thể làm chết ở chốt khác.

  Quyết định: giữ nợ P3 không chặn approval; owner đề xuất là executor/maintainer `packet_loop_test.py`. Hướng xử lý: thêm ca lỗi `ls-tree` có stdout hợp lệ, baseline dương và mutant bỏ riêng `ls[0] == 0` vào nhóm r929/MUTANTS. Ca phải chết tại so sánh state cuối. Rủi ro cần tránh: hook lỗi quá rộng khiến validator/fetch hỏng, hoặc mutant neo vào một đoạn khác. Chỉ gợi ý sửa test; không cần sửa chốt sản phẩm đang đúng, không cấp thêm vòng review ngoài trần hiện hành.

## Phép đo đã chạy

Các lệnh tính từ thư mục `rv2`, trừ lệnh cổng ghi rõ chạy trong `tmp/k`. Chuẩn bị bằng `mkdir -p evidence tmp && cp -a cay-kho tmp/k`; chỉ ghim `core.abbrev=7` trên bản sao. Runner nạp `tmp/k/.claude/dev/packet_loop_test.py` như module, gọi `chay_suite(..., chi_chay={...})`; fixture và mutant nằm ngoài `cay-kho/`.

| Phép đo | Kết quả thực đo |
| --- | --- |
| `python3 -B evidence/audit_source.py before` và `after` | rc=0; hash SPEC/verdict trước, HEAD/tree/base khớp; cả hai patch khớp byte với Git; `SOURCE_DELTA []`; 5.816 tệp gồm metadata Git không đổi giữa hai snapshot; tracked/untracked/ignored sạch |
| `python3 -B evidence/review_runner.py baseline` | rc=0; **159/159 PASS**, gồm 149 ca r812 và 10 ca r929; skipped=0. Có toàn bộ `r812_r7_activation_*` hiện có và `r812_khong_kich_hoat_la_false` |
| `python3 -B evidence/review_runner.py mutants` | rc=0; **14/14** mutant giết đúng ca đích tại `_kiem`, không chết ở baseline hay lỗi CLI; mỗi mutant giữ **3/3** đối chứng khác họ xanh |
| `python3 -B evidence/behavior_probes.py --focused` | rc=0; **12/12** probe HEAD PASS; **4/4** mutant bổ sung chết tại so sánh state cuối |
| Đột biến `review_drop_ls_rc` trên tập hiện có | **159/159 PASS**, skipped=0; bằng chứng trong `evidence/behavior-probes-first.log`, đã đối chiếu đủ tên với baseline |
| `python3 -B evidence/real_and_lint.py` | rc=0; kho thật False cả với SPEC đã giao và dòng khai hợp lệ neo commit đưa ADR-0054 vào kho; Ruff delta=0 |
| Trong `tmp/k`: `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0; sạch, 10 tệp |
| Trong `tmp/k`: `python3 -B .claude/dev/packet_loop.py adr-song --root .` | rc=0; 54 ADR, 54 dòng §20 |
| Trong `tmp/k`: `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null PYTHONDONTWRITEBYTECODE=1 python3 -B .claude/dev/ci_dang_ky_test.py` | rc=0; không `--chay`; `PHẢN CHỨNG: 1070/1070 đỏ đúng`; `TỔNG: ĐẠT` |
| `git -C cay-kho diff --check 5775864..227dcde` | rc=0 |
| `python3 -B evidence/summarize.py` | rc=0; kiểm kết quả/trace, đủ tên ca; hai tệp đã kiểm thử giống byte với hai tệp nguồn |

Mười mutant r929 trong bảng `MUTANTS` đều đã đo, bao gồm bốn M4 bắt buộc:

| Mutant | Ca đích chết tại khẳng định cuối |
| --- | --- |
| `r929_duong_dan_co_dinh_0055` | `r929_kich_hoat_so_bat_ky`: cần True, được False |
| `r929_hai_chuoi_roi` | `r929_hai_chuoi_roi_khong_tinh`: cần False, được True |
| `r929_mot_tro_len` | `r929_hai_tep_kich_hoat`: cần False, được True |
| `r929_bo_loai_tru_adr0054` | `r929_chi_adr0054_tu_neu_cum`: cần False, được True |
| `r929_bo_kiem_loai_doi_tuong` | `r929_thu_muc_ten_md` và `r929_symlink_khong_tinh`: cần False, được True |
| `r929_nhan_symlink` | `r929_symlink_khong_tinh`: cần False, được True |
| `r929_so_chu_so_tuy_y` | `r929_ba_chu_so_khong_tinh`: cần False, được True |
| `r929_bo_duoi_md` | `r929_duoi_khac_md_khong_tinh`: cần False, được True |
| `r929_bo_nfc` | `r929_nfd_van_tinh`: cần True, được False |
| `r929_bo_rc_show` | `r929_show_loi_la_false`: cần False, được True |

Bốn mutant r812 đã chạy thêm: `r812_r7_activation_adr_name`, `r812_bo_kich_hoat`, `r812_bo_shallow`, `r812_nhan_nhieu_dong_khai`. Tất cả chết đúng tại khẳng định state; bao gồm ca (e) kích hoạt ADR khác.

**Parser và đối tượng Git.** `ls-tree -z` phân tách bản ghi bằng NUL; `partition("\t")` chỉ tách TAB đầu giữa metadata và đường dẫn. Hai trường đầu metadata là mode/type; chỉ `100644 blob` và `100755 blob` được đọc nội dung. `040000 tree`, `120000 blob`, `160000 commit` bị loại. Probe CLI xác nhận tên có TAB, khoảng trắng/tiếng Việt, newline và mode executable đều True; tệp lồng thư mục hoặc tên năm chữ số đều False; một tệp ghi chú thường cùng tệp kích hoạt hợp lệ vẫn True. Probe lỗi `show` có stdout hợp lệ vẫn False. Bốn mutant reviewer bổ sung: bỏ rc `ls-tree`, bỏ `100755`, đổi sang tách TAB cuối, nhận gitlink — đều bị probe tương ứng giết tại khẳng định cuối. Các probe bổ sung này là evidence reviewer, chưa được nhập vào suite PR.

**Phạm vi.** Diff đúng hai tệp: `packet_loop.py` thêm 7/bớt 3 dòng; `packet_loop_test.py` thêm 71/bớt 4 dòng; tổng **78 dòng thêm ≤ 300**. AST sản phẩm ngoài `_che_do_0054` và hằng `ADR0055_TEP` được bỏ giống base; không đổi chữ ký, `ADR0054_TEP`, `LUAT_0054_RE` hay thêm hằng runtime ghim số kích hoạt. Các chốt shallow, land-OID, first-parent và dòng §20 giữ nguyên trong diff; 149 ca r812 đều xanh. Master từ base lịch sử `cdc4e80...` đến base review `5775864...` chỉ đổi bốn tệp dưới `ops/land/`, không chạm write set.

**Kho thật và Ruff.** Kho thật chỉ có chính ADR-0054 chứa cụm, nên không tự kích hoạt. Probe thêm dòng khai với land-OID `7cc384ec9e02ed79b429ac6ee2455d3bfbb75b16` vẫn False. Ruff 0.17.2 được chạy thật trên hai blob base/head với `check --no-cache --select F --output-format json`: cả hai rc=1, cùng 1 F841 + 2 F541; so filename/code/message cho delta=0. Đây là N3 đạt tiêu chí delta, không phải lint sạch.

**Giới hạn và tính toàn vẹn phép đo.** Không chạy toàn bộ N1 gồm 876 ca/1.249 mutant; không suy full-suite PASS từ tập đích. N6 check run CI chưa đo vì bundle offline. Lượt đầu script probe reviewer rc=1 do mỏ neo TAB quá ngắn trúng dòng 2507 thay vì `_che_do_0054` dòng 2569; kết quả 159 ca cho mutant rc đã hoàn tất trước lỗi đó. Đã giữ log gốc, sửa mỏ neo thành duy nhất, chạy lại nhóm probe bằng `--focused` rc=0 và kiểm trace đầy đủ; không tính mutant TAB neo sai là bằng chứng về sản phẩm.

Review độc lập trong phiên Codex/OpenAI với shell/tools Linux, transport máy qua tools; không có bằng chứng độc lập về model/effort đã phục vụ, launcher receipt hay assurance runtime, nên không tự xác nhận `cross_approved`. Sandbox thực tế là workspace-write; checkout nguồn được giữ read-only theo nhiệm vụ và kiểm snapshot, không tuyên bố OS cưỡng chế read-only. Snapshot đầu/cuối chứng minh không có delta quan sát được, không chứng minh toàn bộ lịch sử ghi. Không sửa `cay-kho/`, không truy cập mạng, không push ra ngoài; commit/push của fixture chỉ tới bare repo tạm. Không tự soạn đường dẫn thoát cây. Evidence/script/log nằm trong `evidence/`.
