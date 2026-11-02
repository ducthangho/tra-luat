VERDICT: changes_requested — P0/P1/P2/P3 = 0/1/3/0

| id | lớp | mức | tệp:dòng | mô tả | sửa đề xuất |
|---|---|---|---|---|---|
| F1 | 5 — hồi quy gate | P1 | `ops/ci_duong_nhanh_test.py:2321` | `t56` gọi `subprocess.run(["bash", …])`. Bộ quét `_loi_goi_tran` đo **base: `[]`; head: `[(2321,20)]`**, không có miễn trừ. `cong_cu_test` gọi cổng này trên đường đầy đủ, nên lời gọi mới làm gate đỏ. | Dùng `ops/bash_nen.py::tim_bash()` như đặc tả yêu cầu. Kiểm bộ quét hết báo dòng này và ca đầu dò vẫn chạy; thiếu bash phải báo không đo được. Không thêm miễn trừ. |
| F2 | 2, 3 — bằng chứng đỏ sai đường chạy | P2 | `ops/ci_duong_nhanh_test.py:2315`; `.github/workflows/ci.yml:741` | DO6 được phân loại `day_du`, nên workflow **không chạy `kiem-re`**. Harness vẫn gọi thẳng nó rồi lấy rc≠0 làm bằng chứng đã bắt DO6. Nhận định `PATH_DELETED` là advisory đúng; chuyển sang đường đầy đủ **chưa đáp ứng A7c**, vì checker đó vẫn không chặn lỗi. | Cho harness đi theo kết quả phân loại và điều kiện bước thực tế. Nếu giữ yêu cầu DO6 phải đỏ, nối phép kiểm vào đường thực chạy; nếu chủ kho chỉ muốn fallback `day_du`, sửa acceptance bằng revision được duyệt. Ca khóa phải phân biệt fallback với validator đỏ; tránh làm đỏ mọi trích dẫn lịch sử. |
| F3 | 3, 4 — thiếu bằng chứng ủy nhiệm | P2 | `ops/ci_duong_nhanh_test.py:71`, `:2284`, `:2315` | Chú thích dẫn bảng `UY_NHIEM` nhưng bảng không tồn tại. Không có ánh xạ từng bước bị bỏ → kết quả đầu dò/base OID theo §2.2/A7. Harness còn bỏ thực thi `bien-nhan v2 selftest` dù khẳng định nó thuộc tập validator. Vì vậy chưa chứng minh các bước bị bỏ được thay thế đủ. | Ghi bảng từ phép đo đã có, khai riêng `packet_loop_test` chưa đo; bổ sung phần thiếu hoặc xin điều chỉnh acceptance. Harness phải chạy đúng tập validator đã khai. Ca khóa: bỏ một dòng ủy nhiệm hoặc một validator phải đỏ; không coi lỗi môi trường là bắt được đầu dò. |
| F4 | 4 — vượt trần đặc tả | P2 | `ops/specs/CI-LAN-LUU-TRU-r1.md:176` | A9 giới hạn **650 dòng thêm**; diff thực tế **875**, vượt **225**. Đúng 6 tệp và không thấy thay đổi ngoài write set. | Rút phần lặp hoặc có revision nâng trần được chủ kho duyệt trước freeze mới. Đo lại numstat trên đúng base/head; tránh rút bằng cách bỏ coverage cần thiết. |

Lớp 1: chưa phát hiện đường fail-open thực tế trong phần đã kiểm. Các điều kiện workflow cho `day_du`, output vắng/lạ, ép Ubuntu và gộp mảnh phù hợp khi đọc diff; chưa thấy bước đường đầy đủ bị giảm ngoài chủ đích.

Bằng chứng độc lập:

- **Passed:** 18 ca phân loại/YAML; `t162`; 10 đột biến trong bộ nhớ bị bắt bằng assertion của ca đích; `actionlint .github/workflows/ci.yml` rc=0; Ruff pin/probe contract rc=0; `git diff --check origin/master` rc=0.
- **KHÔNG ĐO ĐƯỢC:** `y15` rc=4 và bộ quét bash toàn cây rc=3 vì sandbox không cho tạo thư mục tạm. F1 được đo riêng bằng bộ phân tích AST thật trên nội dung base/head, rc=0.
- **Not run:** toàn bộ suite/đột biến, Windows, CI thực tế, A11 và canary A12. Không coi các mục này là pass.

Neo review: head `4b391be203667def57bf91ff0a3654e3c7694cb8`, tree `1e0dd8102be2832fff3b5993dca5c221a42624c0`; base và băm spec khớp chỉ thị. Worktree sạch ở đầu/cuối; không sửa tệp.

Provider `openai_codex`, transport `machine`; model/effort và execution surface qua runtime receipt: **KHÔNG ĐO ĐƯỢC**.