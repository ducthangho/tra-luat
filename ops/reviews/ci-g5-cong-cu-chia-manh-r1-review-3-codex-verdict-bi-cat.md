# Cross-review độc lập — packet #668, lượt 3

verdict: dang_review
reviewed_sha: 2b501efaab39f5820aae50cd28d0515b6b05ff5a

Bằng chứng được ghi dần; đột biến chỉ thực hiện trên bản sao /tmp.

HƯỚNG 1: Neo review và registry ứng viên
  giả thuyết : Bundle đúng SHA/spec và registry không hồi quy.
  lệnh       : git -C cay-kho rev-parse HEAD; sha256sum SPEC.md;
               python evidence/env.py python -u /tmp/review668-r3/.claude/dev/ci_dang_ky_test.py
  output     : HEAD=2b501efaab39f5820aae50cd28d0515b6b05ff5a;
               SPEC=dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15;
               PHẢN CHỨNG: 1013/1013 đỏ đúng; TỔNG: ĐẠT.
  kết luận   : KHÔNG PHẢI LỖI. Log: evidence/registry.log. Chạy trên clone /tmp; không chạy --chay
               (toàn registry các bộ không thuộc nhiệm vụ). Không dùng A1 tự khai trên SHA lượt 1 làm bằng chứng lượt 3.

HƯỚNG 2: MỚI — main truyền đủ TÊN nhưng mất GIÁ TRỊ bản ghi hoặc vân tay
  giả thuyết : F5 chỉ ghi nhận sorted(ket), nên giữ tên mà phá nội dung vẫn qua t54.
  lệnh       : python evidence/env.py python -u evidence/main_extra.py
  output     : values_lost Counter({'qua': 56}) target=('qua', None), 29.6 s;
               fingerprint_lost Counter({'qua': 56}) target=('qua', None), 28.7 s.
  kết luận   : LỖI (P2), ứng viên F6 nối lớp F2/F5. Đột biến chỉ trên bản sao:
               ket.update nhận cùng tập tên nhưng giá trị None; hoặc truyền {} thay _van_tay() cho writer.
               Mọi 56 ca đều qua, không bỏ qua/không tín dụng giả. Giàn giáo ghi chỉ sorted(ket), không giữ giá trị
               và hoàn toàn bỏ vt. Cặp neo/thay và trạng thái đủ ở evidence/review668_values_lost.json,
               evidence/review668_fingerprint_lost.json. Đang kiểm hậu quả với writer thật để chốt mức.

HƯỚNG 3: Răng từng nhánh _loi_thuc_thi_g5 (đo lại độc lập)
  giả thuyết : Phản chứng đỏ vì nhánh khác, không đo nhánh được tuyên bố.
  lệnh       : python evidence/env.py python -u evidence/branches.py
  output     : gỡ job_keys: 3 LỌT; job_shape: 5 LỌT; step_shell_keys: 7 LỌT;
               action_with: 2 LỌT; setup_env: 1 LỌT. Mỗi lượt suite_ok=False.
  kết luận   : KHÔNG PHẢI LỖI trên cả 5 nhánh phát lỗi. Chạy trọn phan_chung với gỡ riêng từng nhánh,
               giữ cấu trúc if/elif và nhánh khác; xem evidence/branches.log và ablation-*.log.
               Ví dụ độc lập: defaults, runs-on, shell syntax-only, checkout ref, env thiết lập lần lượt mất chốt.
               Đây là kiểm từng nhánh, không chứng minh mọi biểu thức con/đường runtime được phủ.

  Bổ sung HƯỚNG 2: python evidence/env.py python -u evidence/main_wiring.py
               Writer thật: control rc=0, có tệp; values_lost rc=1 [M-loi], không tệp;
               fingerprint_lost rc=1 [M-head], không tệp. Hai đột biến làm hỏng đường thành công thật,
               nhưng t54 chỉ nhìn tên/lời gọi nên không bắt. Chốt F6 ở P2 (thiếu răng M4), không suy thành P1.
               Phép dây nối này giữ tên 56 CA nhưng thân no-op và trả transport BKCON tổng hợp;
               KHÔNG phải 31 đột biến đã đo thật. Bán kính 56/56 ở HƯỚNG 2 là phép riêng chạy CA thật.

HƯỚNG 4: MỚI — tiền kiểm KHÔNG ĐO ĐƯỢC ở main, khác nền CA ĐỎ
  giả thuyết : Sáu kịch bản F5 có nen_do nhưng không có tiền kiểm bị bỏ qua; bỏ riêng nhánh này còn sống.
  lệnh       : python evidence/env.py python -u evidence/main_extra.py;
               python evidence/env.py python -u evidence/main_wiring.py
  output     : skip_precheck Counter({'qua': 56}) target=('qua', None), 30.1 s.
               Rig writer thật + tiền kiểm không khả dụng: bản chuẩn rc=1, không tệp, [M-nen];
               bản bỏ `or tien_kiem_bo_qua` rc=0, ghi tệp mảnh, dù in BỎ QUA (TIỀN KIỂM).
  kết luận   : LỖI (P2), thêm biểu hiện vào F6 cùng lớp main thiếu răng. Phản chứng nằm ở
               evidence/review668_skip_precheck.json và evidence/main-wiring.json.
               Không gọi mã ứng viên hiện tại fail-open: chốt sản phẩm có, nhưng không ca nào canh việc gỡ nó.
               Cần kích thích riêng tiền kiểm unavailable, không thể thay bằng nen_do rồi nói đã phủ cả hai.

HƯỚNG 5: MỚI — lỗi I/O giữa lúc thay tệp mảnh và đường gom sau đó
  giả thuyết : Ghi không nguyên tử để lại tệp dở có thể được gom xanh, hoặc symlink bị nhận như tệp thường.
  lệnh       : python evidence/env.py python -u evidence/io_failure.py
  output     : injected partial write -> OSError, còn 80 byte;
               CLI --gop: rc=1 [G-dau]; symlink: lỗi=1 [G-tep];
               bộ tổng hợp control: GOM MẢNH 8/8, lỗi=0;
               thay mảnh bị đứt giữa chừng: lỗi=1 [G-dau].
  kết luận   : KHÔNG PHẢI LỖI fail-open. Writer không nuốt OSError; gom từ chối tệp dở/link.
               Không đánh đồng bộ BKCON tổng hợp với A1 đo thật. Không yêu cầu ghi nguyên tử mới ngoài spec;
               còn tệp dở sau lỗi không làm upload chạy tiếp trong workflow ghim. Log evidence/io-failure.log.

HƯỚNG 6: Hồi quy gate, actionlint, t152, Ruff F
  giả thuyết : Các thay đổi mới làm hỏng gate hoặc hợp đồng kế thừa.
  lệnh       : CONG_CU_TEST_BAN_KINH=manh CONG_CU_TEST_TIEN_TRINH=2 python evidence/env.py python -u /tmp/review668-r3/ops/cong_cu_test.py;
               python evidence/env.py python -u evidence/compat.py
  output     : gate rc=0; TỰ KIỂM SONG SONG (N126): ĐẠT;
               SỐ LIỆU: ca=56 · đột biến=250 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT.
               head/base: actionlint rc=0; t152 1/1 qua, 0 bỏ qua, 0 hỏng, rc=0;
               Ruff rc=1 ở cả hai, cùng tập finding; RUFF_DELTA_ZERO True.
  kết luận   : KHÔNG PHẢI LỖI trên phạm vi đã chạy. actionlint=1.7.7, Ruff=0.15.15 đúng pin.
               Ruff chỉ đạt delta=0, không phải bare lint xanh. Log evidence/gate.log, compat.log, compat.json.
               Gate giao bán kính 250 cho mảnh; không dùng dòng đó làm bằng chứng đã chạy đủ 250.

---
GHI CHÚ CỦA EXECUTOR (không phải lời reviewer): lượt này bị bộ lọc nội dung của nền cắt giữa chừng —
stderr: "This content was flagged for possible cybersecurity risk", codex rc=1, 102.079 token. Tệp dừng ở
`verdict: dang_review`; không có kết luận cuối. F6 (HƯỚNG 2 + HƯỚNG 4) có phản chứng chạy được và được xử lý như finding.
