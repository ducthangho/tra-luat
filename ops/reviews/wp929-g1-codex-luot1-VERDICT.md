Verdict: request_changes
Reviewed commit: 8a6d795c982fc7e9da2fbfd28a75ca25d5f3eb95
Spec sha256: 79251bee45fc39003d13438d741c4e6319dc80ea6b480dc1b931c93d0c6a7ae6
Reviewed tree: a752a1b5c76cd3766bb2fa0585550b5b8f460c72
Base origin/master: 5775864b04a18c5afe1aafcbb23e54525ce8a3d8

Hoàn tất review: một lỗi sản phẩm P2 và ba finding P3 về độ phủ. Yêu cầu sửa P2 trước khi approve.

## Findings

Vị trí chung của ba P3: `cay-kho/.claude/dev/packet_loop_test.py:8437–8469` (`_r929_adr`, các ca `r929_*` và bảng `MUTANTS`). P3 là đề nghị bổ sung độ phủ, không phải lỗi thực thi đã thấy trên HEAD; P2 là lý do chặn approve.

- [P2] wp929-tree-is-not-activation-file: `cay-kho/.claude/dev/packet_loop.py:2564–2570`, hàm `_che_do_0054`, lấy tên từ `ls-tree --name-only` nhưng không phân biệt tree/blob; thư mục `docs/adr/0731-directory.md` lọt regex, `git show` trả danh sách tên con. Khi tên con chứa cụm khai, hàm nhận nhầm danh sách cây là nội dung ADR và bật chế độ dù không có tệp ADR hợp lệ khai kích hoạt. Lệnh tái hiện: `python3 -B evidence/tree_probe.py`. Output: `040000 tree ... docs/adr/0731-directory.md`; `blob content: 'ordinary note'`; `record-lease: rc=0; luat_adr0054=True; expected=False`. Kết luận: fail-open trên mã HEAD, vi phạm yêu cầu chỉ nhận đúng một **tệp** của M1. Hướng vá: trong `_che_do_0054`, bảo đảm ứng viên là tệp Git hợp lệ trước khi xét nội dung, giữ regex chỉ nhận con trực tiếp. Thêm ca qua `record-lease` với thư mục đuôi `.md`, không có tệp kích hoạt, kỳ vọng False; bỏ kiểm loại đối tượng phải làm ca đỏ. Rủi ro cần giữ: không vô tình nhận tệp lồng sâu hoặc siết mất tên ADR hợp lệ. Không cung cấp bản vá sản phẩm.
- [P3] wp929-filename-boundaries-unmeasured: nới `[0-9]{4}` thành `[0-9]+`, hoặc bỏ yêu cầu đuôi `.md`, không làm ca hiện có nào đỏ. Lệnh `python3 -B evidence/review_runner.py mutants` → cả `review_allow_any_number_length` và `review_allow_non_md` đều `156/156 passed; skipped=0`. Lệnh `python3 -B evidence/behavior_probes.py` → `digit_count_original PASS`, `extension_original PASS`; hai mutant tương ứng đều `AssertionError: ... đòi {'luat_adr0054': False}, được {'luat_adr0054': True}`. HEAD có regex đúng, bộ ca hiện có chưa khóa biên tên. Hướng vá tại nhóm r929/MUTANTS: hai ca âm cho tên ba chữ số và đuôi khác `.md`, giữ ca dương tên bốn chữ số bất kỳ; mutant tương ứng phải chết ở so sánh state. Đáng thêm bằng bảng dữ liệu nhỏ, trong 249 dòng còn dư. Rủi ro: không ghim lại số protocol hoặc vô tình đổi regex sản phẩm vốn đang đúng.
- [P3] wp929-git-error-guards-unmeasured: các ca hiện có không khóa hai chốt fail-closed mới. Lệnh `python3 -B evidence/review_runner.py mutants`: `review_drop_show_rc: 156/156 passed; skipped=0` và `review_drop_ls_rc: 156/156 passed; skipped=0` (153 ca r812/r929 + ba đối chứng). Lệnh `python3 -B evidence/behavior_probes.py`: với fixture dương, Git lỗi được bơm qua wrapper `_git_do` và vẫn chạy CLI `record-lease`; cả `ls_error` lẫn `show_error` đều cho `original ... luat_adr0054 False`, `mutant ... luat_adr0054 True`. HEAD có chốt đúng, nhưng suite không phát hiện khi bỏ chốt; đây là lỗ độ phủ, không phải lỗi xử lý rc của HEAD. Hướng vá tại nhóm test r929 và MUTANTS: thêm ca đọc một ứng viên không kích hoạt bị lỗi trong khi ứng viên còn lại hợp lệ, cùng ca ls-tree trả rc lỗi dù có stdout; bắt buộc False và giữ ca không lỗi True. Rủi ro: đừng để mock làm hỏng fetch/validator/fixture khiến ca chết trước chốt đang đo. Đáng thêm: chốt fail-closed trực tiếp của M1, còn dư 249 dòng theo trần 300.
- [P3] wp929-nfc-unmeasured: bỏ NFC trong `_che_do_0054` không làm ca hiện có nào đỏ. Lệnh `python3 -B evidence/review_runner.py mutants` → `review_drop_nfc: 156/156 passed; skipped=0`. Lệnh `python3 -B evidence/behavior_probes.py` → `NFD_original PASS`, `NFD_mutant AssertionError: ... đòi {'luat_adr0054': True}, được {'luat_adr0054': False}`. Kết luận: HEAD xử lý NFD đúng nhưng chưa có ca bảo vệ yêu cầu NFC của M1. Hướng vá trong nhóm r929: dùng cùng cụm khai được chuyển sang NFD, chạy `record-lease` và đòi True; gắn mutant bỏ NFC. Đáng thêm vì dữ liệu tiếng Việt và chỉ cần một ca nhỏ trong 249 dòng còn dư. Rủi ro: fixture phải thực sự chứa NFD trong Git blob, không bị chuẩn hóa trước khi tới mã đang đo.

## Phép đo đã chạy

- `python3 -B evidence/audit_source.py` → head, base, spec hash và diff đều khớp; 54 mục ADR, đúng một tệp chứa cụm nhưng đó là ADR-0054 bị loại. Không có tệp kích hoạt hợp lệ.
- `_che_do_0054(cay-kho, SPEC.md)` → `False`; thử thêm dòng khai hợp lệ neo commit đưa ADR-0054 vào kho → vẫn `False`.
- AST sản phẩm ngoài `_che_do_0054` và hằng bị bỏ giống base. Diff: hai tệp, 51 dòng thêm; `git diff --check 5775864..8a6d795` rc=0.
- Bốn đột biến M4 đã làm đúng ca (a)–(d) đỏ bởi `AssertionError` tại so sánh `luat_adr0054`; mỗi đột biến giữ ba đối chứng khác họ xanh. Đột biến trỏ ADR khác cũng giết đúng ca (e).
- N3 Ruff 0.17.2: base/head đều rc=1 với cùng 1 F841 + 2 F541; delta=0.
- N4 trên bản sao: `doctrine-scan` rc=0 (10 tệp); `adr-song` rc=0 (54 ADR/54 dòng).
- N5 lần đầu: lỗi Git commit trong fixture, rc=128; đã tái hiện nguyên nhân là global `commit.gpgsign=true` gọi dịch vụ ký không truy cập được trong sandbox. Chạy lại chỉ cô lập cấu hình Git bằng `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`: rc=0, `PHẢN CHỨNG: 1070/1070 đỏ đúng`, `TỔNG: ĐẠT`; không sửa cổng hoặc cấu hình nguồn.
- `python3 -B evidence/review_runner.py baseline`: `153/153 passed; skipped=0`, gồm toàn bộ 149 ca `r812_*` và bốn ca `r929_*`; chưa thấy hồi quy trong tập này.
- `python3 -B evidence/review_runner.py mutants`: tám đột biến có sẵn (bốn M4 + bốn r812 liên quan) giết đúng ca đích, giữ ba đối chứng mỗi đột biến xanh. Năm đột biến bổ sung đều sống trong tập 156 ca đã đo; phản chứng bổ sung qua `record-lease` trong `behavior_probes.py` phân biệt HEAD với từng mutant. Đây không phải tuyên bố đã chạy toàn bộ suite dưới từng đột biến.
- `python3 -B evidence/tree_probe.py`: tái hiện độc lập P2 ở trên; tệp con chỉ chứa `ordinary note`, cụm khai chỉ xuất hiện trong TÊN của nó.
- `python3 -B evidence/summarize.py`: xác nhận kết quả M4, năm mutant sống, 153 ca đạt; 5.810 tệp nguồn giống từng byte so snapshot đầu, không thêm/xóa/đổi tệp, Git tracked/untracked/ignored sạch. Hai tệp trên bản sao đã kiểm thử giống từng byte với nguồn.
- Log và script tái hiện ở `evidence/`: `baseline.log`, `mutants.log`, `behavior-probes.log`, `tree-probe.log`, `source-audit.log`, `summary.log`. Chưa chạy toàn bộ 870 ca/1243 đột biến và không suy N1 đầy đủ từ tập đích; N6 chưa đo vì bundle offline.

Các lệnh chạy từ thư mục `rv`; đã dựng bản sao bằng `cp -a cay-kho tmp/k`. Runner nạp module từ `tmp/k/.claude/dev`, gọi `chay_suite` trên bản sao và đặt mọi fixture/đột biến ngoài nguồn.

| Ca | Đột biến kiểm chứng | Lỗi đúng tại khẳng định cuối |
| --- | --- | --- |
| (a) `r929_kich_hoat_so_bat_ky` | `r929_duong_dan_co_dinh_0055` | `AssertionError`: cần True, được False |
| (b) `r929_hai_chuoi_roi_khong_tinh` | `r929_hai_chuoi_roi` | `AssertionError`: cần False, được True |
| (c) `r929_hai_tep_kich_hoat` | `r929_mot_tro_len` | `AssertionError`: cần False, được True |
| (d) `r929_chi_adr0054_tu_neu_cum` | `r929_bo_loai_tru_adr0054` | `AssertionError`: cần False, được True |
| (e) `r812_r7_activation_adr_name` | `r812_r7_activation_adr_name` | `AssertionError`: cần False, được True |

Lệnh cổng trên `tmp/k`: `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .`; `python3 -B .claude/dev/packet_loop.py adr-song --root .`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null PYTHONDONTWRITEBYTECODE=1 python3 -B .claude/dev/ci_dang_ky_test.py`. N3 dùng `python3 -B -m ruff check --no-cache --select F` trên hai tệp HEAD và hai blob tương ứng từ base; `audit_source.py` lưu và so cùng mã/chẩn đoán, bỏ khác biệt số dòng do diff.

## Trả lời bốn câu hỏi

1. **Có fail-open:** HEAD bật chế độ khi ứng viên là Git tree đuôi `.md`, chỉ tên con chứa cụm; xem `wp929-tree-is-not-activation-file`. Với các ứng viên tệp thường, phép đo lỗi `ls-tree`/`show` trên HEAD đều đóng về False. Kho thật hiện False.
2. **(a)–(e) có đo đúng:** tất cả đi qua `record-lease`, đọc lại trường state. (a) chết tại kiểm True sau đổi sang `0731-bat-ky.md`, không chết ở baseline; (b)/(c)/(d) chết tại kiểm False sau thay đúng dữ liệu; (e) chết tại kiểm False sau đổi đích thành ADR-0053. Các lỗi đều `AssertionError`, không phải CLI sập. Nhưng các ca ấy không bao quát kiểu đối tượng Git, lỗi đọc, NFC và biên regex.
3. **Hồi quy r812:** 149/149 ca hiện có đạt, không skip. Bốn đột biến r812 liên quan shallow, kích hoạt, dòng §20 và tên ADR vẫn giết đúng ca; không có bằng chứng hồi quy trong tập đã đo.
4. **Write set/phạm vi:** đúng hai tệp, 51 dòng thêm (6 sản phẩm +45 test), không đổi docs, manifest, VERSION hoặc frozen spec. AST ngoài hàm/hằng được phép giống hệt base; hằng ADR0055_TEP đã bỏ, không thêm hằng runtime ghim số kích hoạt. Số 0099 chỉ là fixture theo M3; tên 0055 cũ chỉ còn trong đột biến M4 có chủ ý.

## Giới hạn và môi trường

- Review độc lập bằng Codex/OpenAI với shell/tools trong sandbox Linux, không mạng; không sửa/đẩy kho nguồn, merge/land hoặc gửi thông điệp bên ngoài. Commit/push chỉ xảy ra trong fixture tới remote bare tạm. Không suy model/effort runtime cụ thể hoặc assurance đã được xác thực từ nhãn provider của bundle.
- Toàn bộ fixture, đột biến và script đo nằm ngoài `cay-kho/`; không tự dựng symlink hoặc đường dẫn thoát cây.
- Chỉ báo những phép đo đã chạy; không coi N1 toàn suite hoặc N6 CI xanh. `ci_dang_ky_test.py` được chạy không `--chay` như N5 yêu cầu.
