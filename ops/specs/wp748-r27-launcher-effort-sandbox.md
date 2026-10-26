# Đặc tả packet #748 r27 — launcher.py ghi effort và sandbox mode THỰC TẾ của lượt codex

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| packet | #748 `wp748`, revision 27, generation 27 |
| review_class | `sensitive` (write set gồm `.claude/dev/launcher.py`, lane launcher) |
| write set | `.claude/dev/launcher.py`, `.claude/dev/launcher_test.py` |
| base | `origin/master` lúc cấp lease |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run`, phiên mới, read-only, neo đúng head |

## 1. Vì sao
Connector Codex bắt được một lỗi P1 trên PR #934 (review comment `4372912640`). §8.1 đòi ghi model **và effort** đo được lúc chạy, §8.2 đòi ghi **sandbox mode thực tế**. `run.json` của `launcher.py run` hiện chỉ có `model_phuc_vu`. Hậu quả: không hồ sơ land nào dựa trên launcher đạt được assurance thực thi, kể cả khi review đã neo đúng SHA. Ví dụ là `ops/land/pr932-wp748-r26-land-evidence.yaml`, mục `assurance_81.thuc_thi`.

## 2. Phép đo nền
Đo ngày 25-10-2026, container remote Linux, codex-cli 0.163.0, hai lượt `codex exec` thử nghiệm (không phải lượt review).
- **Effort:** khung `response.created`/`response.completed` do MÁY CHỦ trả về, nằm trong trace `tungstenite::protocol` "Received message", mang trường `response.reasoning.effort`. Lượt thử với `-c model_reasoning_effort="xhigh"` cho 4/4 khung giá trị `"xhigh"`. Đây cũng là nguồn launcher đang dùng để đo model, nên trường mới đi qua đúng bộ lọc và đúng danh sách cho phép của r26.
- **Sandbox:** trace KHÔNG có thông tin sandbox (0 dòng khớp `sandbox_mode`, `SandboxPolicy`, `landlock`, `bwrap`). Cây tiến trình thì có. Lệnh shell của mô hình chạy dưới `bwrap … --argv0 codex-linux-sandbox`, rồi tới `codex-linux-sandbox --sandbox-policy-cwd <cwd> --command-cwd <cwd> --permiss…`, rồi mới tới lệnh. Với `-s read-only`, `argv` của `bwrap` gồm `--ro-bind / /`, `--unshare-net`, `--unshare-pid`, `--cap-drop ALL`. Đó là cơ chế cưỡng chế thật, không phải cấu hình khai báo.

## 3. Thay đổi
1. **Effort.**
   - `_phan_loai_khung` lấy thêm `response.reasoning.effort`. Trường này chỉ hợp lệ khi là chuỗi khác rỗng và `reasoning` là object.
   - Mục trong `ket` thêm khoá `effort`. Thiếu hoặc sai kiểu thì giá trị là `None`; khung vẫn được nhận cho model.
   - `ghi_so` ghi hai trường:
     - `effort_phuc_vu`: danh sách các giá trị khác nhau đã thấy, theo thứ tự gặp lần đầu.
     - `effort_phuc_vu_trang_thai`: `DO_DUOC` khi và chỉ khi `model_phuc_vu_trang_thai == "DO_DUOC"` VÀ mọi khung đã nhận đều có effort. Còn lại là `KHONG_DO_DUOC`, ghi lý do vào `effort_phuc_vu_ly_do`.
   - KHÔNG suy effort từ đối số dòng lệnh hay từ config.
2. **Sandbox (chỉ Linux).**
   - Trong lúc con chạy, một luồng lấy mẫu duyệt hậu duệ của PID con qua `/proc/<pid>/stat` (lấy ppid) và `/proc/<pid>/cmdline`. Chu kỳ ≤ 0,5 s. Luồng KHÔNG đọc `/proc/<pid>/environ` hay bất kỳ tệp nào khác.
   - Với tiến trình có `argv[0]` (basename) là `bwrap` hoặc `codex-linux-sandbox`, launcher trích ra một **bản tóm tắt** gồm:
     - (a) `bwrap`: các cặp `--ro-bind`/`--bind`/`--bind-try`/`--ro-bind-try`, mỗi cặp ghi `(cờ, đích)`; các cờ không đối số `--unshare-net`, `--unshare-pid`, `--unshare-user`, `--cap-drop`.
     - (b) `codex-linux-sandbox`: tên các cờ bắt đầu bằng `--` cùng giá trị của chúng, NGOẠI TRỪ giá trị là đường dẫn. Đường dẫn được thay bằng nhãn `cwd` khi trùng `--workspace` của launcher, còn lại bằng nhãn `khac`.
   - Mọi chuỗi không thuộc danh sách cho phép đều bị bỏ. KHÔNG lưu nguyên `argv`, vì nó chứa lệnh của mô hình và có thể chứa prompt.
   - `run.json` thêm các trường:
     - `sandbox_quan_sat`: danh sách các bản tóm tắt khác nhau, mỗi bản kèm `so_lan`.
     - `sandbox_trang_thai`, nhận một trong các giá trị:
       - `DO_DUOC`: thấy ≥ 1 tiến trình sandbox, VÀ mọi lần lấy mẫu đều thành công.
       - `KHONG_THAY_LENH`: không thấy tiến trình sandbox nào, VÀ stdout không có item `command_execution` nào.
       - `KHONG_DO_DUOC`: một trong ba trường hợp:
         - nền không phải Linux;
         - không đọc được `/proc` hoặc luồng lấy mẫu lỗi;
         - stdout có `command_execution` mà không thấy tiến trình sandbox nào. Lệnh có thể đã chạy ngoài sandbox, hoặc quá ngắn so với chu kỳ lấy mẫu.
     - `sandbox_ly_do`.
   - Lấy mẫu là ĐO TỪ BÊN NGOÀI, có giới hạn: lệnh ngắn hơn chu kỳ có thể lọt. Vì vậy `DO_DUOC` chỉ nói "đã thấy cơ chế sandbox với các cờ X". Nó KHÔNG nói "mọi lệnh đều chạy trong sandbox"; `run.json` ghi rõ giới hạn này trong `sandbox_gioi_han`.
3. Ngoài phạm vi:
   - Không sửa `ops/land_evidence_nguon.py`. Việc regression check từ chối assurance đạt khi thiếu phép đo là một packet riêng, chủ kho quyết.
   - Không đo macOS (seatbelt) và Windows; hai nền này ghi `KHONG_DO_DUOC`.
   - Không đo lại các lượt review đã xong.

## 4. Tiêu chí xong
- Mỗi nhánh trạng thái của effort (`DO_DUOC`, thiếu ở một khung, sai kiểu, model không đo được) và của sandbox (`DO_DUOC`, `KHONG_THAY_LENH`, `KHONG_DO_DUOC`: cả ba lý do) có ít nhất một ca `r927_*`. Ca nào cần `/proc` thật thì chạy trên Linux; nền khác bỏ qua có lý do và vẫn có ca `KHONG_DO_DUOC`.
- Có ca chứng minh `sandbox_quan_sat` KHÔNG chứa chuỗi nào ngoài danh sách cho phép. Fixture phải có `argv` mang một chuỗi bí mật giả, và chuỗi ấy không được xuất hiện trong `run.json`.
- Có ca chứng minh luồng lấy mẫu không mở `environ`.
- Mỗi chốt có một đột biến tay riêng, bị ca đích giết bằng `TinHieuChotCa`. Bộ sinh đột biến regex của r26 tiếp tục phủ mọi literal regex trong khối bộ lọc, kể cả regex mới nếu có.
- `launcher_test` N/N. Ruff delta 0. Lane Windows (nhãn `windows` hoặc lượt push master) xanh.
- Review chéo Codex qua `launcher.py run` trên đúng head cho tới khi đạt 0 P0–P3.

## 5. Trần
- **Lời gọi Codex:** 10, theo dòng khai `ADR-0055` ở đầu tệp. OID `d2e3052…` đã qua ba phép đo của ADR-0055 dòng 34–36 lúc 26-10-2026, trên clone không shallow vừa fetch: `rc 0` · `rc 128` · có trong `--first-parent origin/master`. Lượt connector khi đánh dấu ready cũng tính là một lời gọi.
- **Kích thước:**
  - Dòng khai `ADR-0053` (OID `8ab1007…`; ba phép đo rc 0 · rc 128 · có trong first-parent, cùng lúc) cho trần ≤ 6 tệp / ≤ 450 dòng thêm.
  - Ước lượng là ~500 dòng thêm, gồm ~180 dòng code và ~320 dòng test.
  - **Xin `nang_tran` kích thước:** `ai_nang` chủ kho; `tran_cu` ≤ 6 tệp / ≤ 450 dòng thêm (ADR-0053); `tran_moi` ≤ 2 tệp / ≤ 600 dòng thêm (`git diff --numstat` base..head); `can_cu`: sandbox cần cả luồng lấy mẫu lẫn danh sách cho phép, kèm ca chống rò `argv`.
  - Numstat thật vượt `tran_moi` thì dừng TRƯỚC review và soạn revision.
- Không cổng nào cưỡng chế hai trần này (ADR-0052/0053/0055 tự khai). Người giữ đo bằng tay.
