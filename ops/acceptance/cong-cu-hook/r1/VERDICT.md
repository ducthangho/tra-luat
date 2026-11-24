# CONG-CU-HOOK r1 — review độc lập Codex offline (2/2 lời gọi) + đo của executor

**Căn cứ:** đặc tả `ops/specs/cong-cu-hook-r1.md` §4–§5, lease `ops/leases/cong-cu-hook-r1-g1-claude.yaml` (`review_calls_limit: 2`),
Issue #1474, PR #1477.

## Các lượt
| lượt | run (`launcher.py run`) | head review | kết luận | sandbox | model phục vụ |
|---|---|---|---|---|---|
| 1 | `169cce85`, 01:48:37Z → 01:53:08Z, `ma_thoat` 0 | `509b0f60df7645f2ce9d9de407203835555dcf17` | **request_changes**: 2 P2, 1 P3, 5 đột biến sống | `KHONG_DO_DUOC` | `gpt-6-astra` |
| 2 | `f68244ec`, 02:00:39Z → 02:04:13Z, `ma_thoat` 0 | `fff63475008775c09b6ef4eedbf8c76bc6103a5a` | **request_changes**: 1 P2, 1 P3; ba finding lượt 1 đã sửa; 20/20 đột biến bị giết | `DO_DUOC` | `gpt-6-astra` |

Lệnh, cả hai lượt: `python3 .claude/dev/launcher.py run --workspace <clone tại head> --expected-repo ducthangho/tra-luat
--expected-root-commit e13f74bb… --expected-head <head> --prompt-file <p> --expected-prompt-sha256 <sha> -- /opt/node22/bin/codex exec
-m gpt-6-astra --sandbox workspace-write --skip-git-repo-check -C <thư mục review> "…{PROMPT_FILE}…"`.

Trước lượt 1 có một lần chạy bị launcher chặn `CHAN [11]`: clone chưa có remote GitHub. Lần đó không gọi Codex, nên không tính vào trần.

## Xử lý finding
| finding | xử lý | bằng chứng |
|---|---|---|
| L1 F1474-01 P2: probe `ruff --version` trần và trình cài không có trần thời gian, hook có thể không tới `doctor` | mọi lệnh ngoài đi qua `_cc_chay_tran` (`timeout -k 5`): probe 30 s, mỗi lần cài 180 s, ngân sách khối 300 s; còn dưới 15 s thì `HET NGAN SACH`; ca `r1474_probe_ruff_tran_treo_bi_cat`, `r1474_trinh_cai_lo_TERM_van_bi_giet`, `r1474_het_ngan_sach_khong_cai` | `64aa677`; lượt 2 tái hiện: probe treo kết thúc sau 1,1 s, trình cài lờ TERM kết thúc sau 12,2 s |
| L1 F1474-02 P2: đo hỏng mà vẫn `pip install ruff` | đo/bản kê hỏng thì `return 1` ngay; ca `r1474_do_hong_khong_pip_ruff` | `64aa677`; lượt 2: JSON hỏng, thiếu PyYAML, YAML hỏng ⇒ 0 lần cài, 0 lần pip |
| L1 F1474-03 P3: dòng DAT thiếu số công cụ | in `DAT (n cong cu)`; ca 1 và ca 2 đòi đúng số | `64aa677`; lượt 2 xác nhận |
| L1: 5 đột biến sống (`name_regex`, `no_timeout`, `current_PATH`, `after_codex_auth`, `first_tool_only`) | ca tên lạ, ca hai công cụ thiếu, `ruff` trần chỉ nằm trên `PATH_GOC`, ca cấu trúc đòi khối đứng trước `# --- Xác thực codex` | lượt 2: 5/5 bị giết bằng `TinHieuChotCa` |
| executor tự tìm, trước lượt 2: `$(( 1x ))` làm chết CẢ hook dù khối chạy dưới `\|\|` | `_cc_so` lọc biến không phải số; ca `r1474_bien_tran_khong_phai_so_dung_mac_dinh` | `fff6347` |
| L2 F1474-04 P2: trần probe/cài bằng 0 làm GNU `timeout` tắt hẳn | 0 về mặc định (tham số `duong`); ngân sách 0 vẫn hợp lệ (bỏ qua cài) | `3b473aa`; ca `r1474_tran_bang_0_ve_mac_dinh_so_0_dau_la_thap_phan`, đột biến `wp1474_tran_0_tat_timeout` |
| L2 F1474-05 P3: `018` bị đọc thành số bát phân | ép thập phân `10#`, tối đa 6 chữ số | `3b473aa`; cùng ca, đột biến `wp1474_so_0_dau_bat_phan`, `wp1474_bo_gioi_han_chu_so` |

Phần sửa theo lượt 2 (`3b473aa`) **không** qua lời gọi Codex offline thứ ba, vì trần là 2. Connector Codex review head cuối trên PR #1477.

## Đo của executor trên head code cuối `3b473aa`
- 19/19 ca `r1474_*` đạt.
- 18/18 đột biến `wp1474_*` bị giết đúng lý do (`TinHieuChotCa` của ca đích), đo trên bản sao tạm của hook.
- `.claude/dev/launcher_test.py` đầy đủ: `rc=0`, 445/445 ca chạy qua, 0 hỏng. Hai ca bỏ qua (`t62`, `r484_g4`) chỉ dành cho Windows và đã bỏ qua trên Linux từ trước. Nhật ký `vao=447 ra=447`, cây sạch suốt lượt chạy.
- `ops/cloud_agent_creds_test.py` (bộ này đọc hook): CA 60/60, DOT BIEN 91/91, TONG: DAT.
- Delta so `origin/master` `e02d748` = 0:
  - `ruff check --select F` trên `launcher_test.py`: 5 → 5;
  - `shellcheck` trên hook: 1 → 1 (cùng SC2015 ở dòng 203).
  - `bash -n` OK; `doctrine-scan` sạch.
- Chạy thật khối trong container: `cong-cu-ban-ke: DAT (8 cong cu)`, `ruff: DAT 0.15.15`, cảnh báo `ruff` trần 0.16.9, `rc=0`, dưới 1 giây.

## Sai khác so với đặc tả (bổ sung, không sửa tệp đóng băng)
§2 chỉ đặt trần 180 s cho mỗi lần cài. Bản cuối thêm:
- trần probe 30 s;
- ngân sách khối 300 s;
- `timeout -k 5`;
- ba biến `TL_CC_TRAN_PROBE_GIAY`, `TL_CC_TRAN_CAI_GIAY`, `TL_CC_NGAN_SACH_GIAY` để test rút ngắn trần.

Lượt 2 đánh giá các phần này là hợp lý và không cần sửa đặc tả. Lượt 2 cũng ghi rằng ngân sách 300 s chặn việc **bắt đầu** cài, chưa phải trần cứng cho cả khối. Probe sau khi cài và 5 s ân hạn của `-k` có thể kéo dài thêm một chút.

## Giới hạn còn lại (đã nêu, không chặn)
- Không có lệnh `timeout` thì lệnh chạy không trần; đặc tả cho phép điều này.
- Chưa chạy trên BusyBox. Một `timeout` giả không nhận `-k` thì ra `KHONG DO DUOC`, không cài gì.
- `ruff` trần 0.16.9 của ảnh container chỉ được cảnh báo, không gỡ.
