# Review đặc tả wp1236 r10 bản sửa 3 — vòng 8

**Approve nội dung đặc tả.** Không phát hiện finding P0/P1/P2/P3 còn mở trong phạm vi đặc tả sau quyết định E1. Đây không phải approval mã, nâng trần, miễn nợ lịch sử hay quyền thi công/merge.

- `reviewed_sha`: `81dc1eb73925babe638ed50222e0354bf7488248`.
- Tree: `f97856425daee530ad4d92cd5052f2f0e2720496`.
- SHA-256 đặc tả: `3ee831738c70c5eabb27720e295b4953c9a9bdd1ac29a03cc7b964d28658fcdc`; khớp byte blob tại HEAD.
- So với vòng 7: `33b6803676b12fd069976dedb79f043a268c29c3`.
- Provider/surface/transport: `openai_codex / codex_cli / machine`, theo launcher run `e10bfd1d46bf42b29e8e4293721f94a3`. Serving model/effort: `KHONG_DO_DUOC` trong khi launcher chưa kết thúc. Sandbox thực tế `workspace-write`; phiên giữ repo chỉ đọc và chỉ ghi trong `work/`.

**Nghiệm thu còn bắt buộc kiểm được.** Luật 1 đòi ca đúng lý do, đối chứng và mutant gỡ đúng chốt; luật 2 phủ năm ô trùng ID; luật 4 đòi ma trận miền nghĩa qua đúng consumer; luật 5 đòi ledger từng ID, cộng dồn qua các lượt. SPEC:293–342 còn yêu cầu kill bằng đúng `TinHieuChotCa`, không dùng lỗi vô can/chốt khác bắt thay. SPEC:327–328 buộc reviewer mã quét độc lập; survivor không tương đương là finding theo §8. Hợp đồng này cần reviewer đọc nghĩa và đo target/control; scanner xanh không thay được các nghĩa vụ ấy.

**Luật 5 không làm mất nghĩa vụ khi mất neo.** Đã chạy bộ quét hiện tại trên năm biến thể nguồn, đối chiếu tập ID với kho có băm ghim:

| Nguồn thử | Áp dụng | `KHONG_AP_DUNG` | Tổng ID giữ lại |
|---|---:|---:|---:|
| Module đúng blob r9 `c2d606b` | 127 | 0 | 127 |
| Đổi định dạng/chú thích | 127 | 0 | 127 |
| Đổi tên local, dùng fixture vòng 7 | 125 | 2 | 127 |
| Không có neo | 0 | 127 | 127 |
| Mỗi neo xuất hiện hai lần | 0 | 127 | 127 |

Trên Python 3.12, `hoi-quy` vẫn xuất đủ 127 ID: 125 áp dụng và hai ID có lý do không áp dụng (`reason_claim_failed`, `reason_complete_290_39`); `chay` bị chặn rc 2 vì đòi Python 3.13. Luật 5 bắt buộc disposition/thay thế cùng nghĩa cho từng ID ấy. Không được lấy 125 kết quả thực thi làm đủ 127 nghĩa vụ. Bộ chạy vẫn loại dòng `KHONG_AP_DUNG` khỏi `kq`, nên `HOAN_TAT` riêng lẻ không đóng ledger; đặc tả hiện hành không cho dùng nó thay ledger.

Đã tái hiện phản chứng thiếu `src` của X01: manifest 800 dòng bỏ toàn bộ `src`, hoặc chỉ giữ một `src`, đều bị từ chối rc 2, không có `HOAN_TAT`. Chưa chạy lại baseline/child terminal hoặc toàn bộ pilot của bộ chạy mới; không tuyên bố đã sửa hết công cụ.

**Không thấy câu hiện hành buộc nghiệm thu luật 3.** Đã đọc toàn bộ 585 dòng và quét mọi tham chiếu. Dòng 300, 318–328, 585 xác định rõ luật 3 là khuyến nghị; dòng 439 đã đổi phương án tách sang nghĩa vụ luật 4. Câu “bất kỳ đột biến nào sống” ở 379–382 nói về bộ test đợt A, không tái lập ngưỡng cho toàn bộ manifest luật 3. Các dòng 553/561/570/578 là bảng xử lý lịch sử; tham chiếu `(g)–(l)` ở 561 không hạn chế reviewer hiện tại. Nhãn “ĐO CHÍNH THỨC” trong docstring công cụ cũng không cấp quyền nghiệm thu vượt đặc tả.

**Đối chiếu mọi lớp vòng 7:** JSON có đủ 15 mục lịch sử. Mười hai lớp đã `DA_VA_THAT` được giữ nguyên; 23 đoạn hợp đồng của 11 lớp khớp nguyên văn bản trước, lớp số đo được đếm lại riêng. Không tái mở lớp đã đóng.

| Lớp còn chưa đóng | Nhãn vòng 8 | Bằng chứng và phần còn lại |
|---|---|---|
| `nghiem-thu-khong-co-lap-chot-dich` — X01 cùng các finding trước | `VA_MOT_PHAN` | Phản chứng thiếu `src` đã bị chặn; inventory hồi quy được giữ. E1 rút luật 3 khỏi acceptance, không phải chứng minh vá cả lớp. Chờ mã r10, ledger và quét độc lập. |
| `test-thieu-chot` — L01/L02, alias lịch sử | `VA_MOT_PHAN` | Nghĩa vụ ma trận, target/control, sáu fixture CLI và kho reviewer còn nguyên. Chưa có bằng chứng mã r10 đóng L01/L02. Không đếm alias lần hai. |
| `mo-ta-duong-dan-lech-hop-dong` — L03 | `VA_MOT_PHAN` | Đo r9: plain và `./tệp` đều trả `[]`, nhưng docstring vẫn ghi cấm `.`. SPEC:122–124,563 đã rõ; chờ mã sửa docstring và reviewer mã xác nhận. |

Hội tụ **7→8 = 0/2**, F rỗng. Giữ lịch sử lặp lớp và checkpoint §12; scope cut không tính là vá. Đính chính `ma4_sang_5 = KHONG_DO_DUOC`, không chép `0/1` sai của vòng 6/7. Đã đọc `run.json` vòng 6: cả model và effort đều `KHONG_DO_DUOC`. Approval đặc tả này không reset budget hoặc cấp thêm lượt review.

**Số tổng và trần nhất quán:** 30 ca sàn = 17 A1 + 13 A2; năm luật, bốn bắt buộc; 50 mutant đánh số kế thừa; kho 127 ID. Sinh manifest hai lần được cùng 800 ID/hash; đối chiếu pilot có đủ 927 ID/hash, phân hạng 764 giết + 153 sống + 10 lỗi vô can. Đây là kiểm artifact pilot cũ, không chạy lại 927 mutant. Số 34 là nhóm survivor của kho trong pilot, không giảm ledger 127 ID. Numstat r9 đo lại bằng 335 + 988 + 1 = 1324 dòng trên ba tệp. R10 vẫn chỉ có ước lượng, chưa có số đo mã.

Đề nghị **1700 dòng vẫn CHỜ E2** (SPEC:432–440); việc thu hẹp luật 3 không tự cấp quyền nâng trần, cũng không buộc phải hạ một mức dự phòng công sức đã ghi là ước lượng. E5/spec hash, lease và audit trước merge vẫn riêng. Authority E1 được nhận từ chỉ thị người dùng; không gọi mạng để xác minh comment.

Phép đo và command/rc nằm trong `audit_r8.json`, `runtime_r8.json`, `unchanged_contracts.json`, `dotpath_r8.json`, `preflight.json` và `final_snapshot.json`. Các phép kiểm nêu trên `passed`; rc 2 của các ca từ chối là kết quả âm mong đợi. Windows, CI, Ruff, full selftest/release, mã r10 và LIVE đều `not_run`, không tính pass. Validator §8.3: xem `kiem_verdict.txt`.

KET_LUAN: approve
