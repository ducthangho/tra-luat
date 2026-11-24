**changes_requested — 1 P2 và 2 P3 còn mở, thuộc 3 lớp.** Review class `sensitive`: chưa đạt điều kiện approve của protocol §8/ADR-0060 M1. Hai approve vòng 3 không áp cho bản hiện hành và không miễn P3.

Đặc tả r9 bản sửa 3, vòng 4: `sha256 e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8`. Kho `ducthangho/tra-luat`, checkout detached tại `176feba3a09a4e86c6d8b06487f3e4224571be51`, tree `3befda03f3bb668cb31c1dad4e651356a4fec9dd`; base soạn `8048551a9b1eb886c126d2a1a4df0f95fb285964`. Băm tệp được giao, blob HEAD và ba băm lịch sử đều đã kiểm khớp. Diff chưa ai review là `9e05aac… → 176feba…`.

Các finding sau đã được quét theo lớp trên toàn bộ thiết kế, bảng nghiệm thu A/B/C, phần hệ quả và giới hạn:

| ID / mức | Lớp | Vấn đề và bằng chứng | Cách đóng |
|---|---|---|---|
| U01 / **P3** | `hop-dong-dau-vao-dau-ra-chua-chot` | SPEC:156–175,338: nhánh `owner_waived` chỉ có `oid/chuoi/readback_thu_muc`, nhưng mẫu success chung dùng `<tep>`. C6 nói “không dòng D2b” mà không phân biệt `thieu` với stdout `D2b ĐẠT`. | Chốt mẫu stdout riêng cho nhánh miễn; C6 đòi không vi phạm và đúng một marker thành công. Giữ ca âm `tac_gia`/rc12. |
| U02 / **P3** | `nghiem-thu-khong-co-lap-chot-dich` | SPEC:75,88,284,288: không có ca/đột biến cho `job_id_trung_provenance`; ca trùng ID chưa buộc phân biệt nhánh skipped. Bản sao fixture thật: thêm ID trùng vào provenance vẫn `passed`; lặp dòng skipped làm parser mất dòng mà không báo `job_lap`. | Ma trận chống mất ID trước khi dựng dict: provenance, job/job, skip/skip, job/skip hai thứ tự; ca âm/đối chứng/đột biến riêng và đúng lý do. |
| U03 / **P2** | `pham-vi-kiem-chung-trai-adr-windows` | SPEC:398 loại Windows CI cho toàn packet; write set A/C (220–222) sửa `.claude/dev/**`. ADR-0060 M3 xếp `required`, đòi Windows local cộng thêm Windows CI; ADR-0062 N1 áp mặc định. Q7 chỉ giới hạn OS của luật gate-output, không miễn kiểm mã A/C. | Tách OS evidence được đọc với OS kiểm triển khai; giữ nghĩa vụ M3 cho A/C, phân loại B theo diff thật; không coi skip symlink là Windows xanh. |

U02 là thiếu ràng buộc nghiệm thu của **đặc tả**, không phải kết luận mã tuân thủ K4 có đường lọt. Phép đo chạy trên tham chiếu của soạn giả và bản sao fixture; module r9, L8 và D2b tương lai chưa tồn tại. Chi tiết vị trí, phép đo, cách vá chung và kiểm đóng lớp nằm trong [VERDICT.json](/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/work/VERDICT.json).

**Lịch sử lớp đã dựng lại: 34/34 finding, 12 lớp.** Tiền tố `codex:`/`claude:` phân biệt các ID trùng tên. Mỗi finding gốc thuộc đúng một lớp; các finding nhiều biểu hiện giữ nguyên ID, giải thích cách gộp tại `bang_noi_slug`. Không dùng nhãn ĐÓNG cũ để tự tuyên bố đóng lớp.

| Slug | Finding cũ | Vòng có finding | Trạng thái trên e3efa593 |
|---|---|---|---|
| `xuong-dong-khong-khop-byte-that` | `codex:R01`, `claude:R01` | 1 | **DA_VA_THAT** |
| `nghiem-thu-khong-co-lap-chot-dich` | `codex:R02`, `claude:R03`, `claude:R06`, `codex:S01`, `codex:S03`, `claude:S03`, `claude:S05`, `claude:S06`, `codex:T01`, `claude:T01` | 1, 2, 3 | **VA_MOT_PHAN** |
| `nang-tran-thieu-hop-dong-authority` | `codex:R03`, `claude:R11` | 1 | **DA_VA_THAT** |
| `d2b-thieu-neo-attempt` | `codex:R04` | 1 | **DA_VA_THAT** |
| `so-do-khong-cung-pham-vi-nguon` | `codex:R05`, `claude:R05`, `codex:S02`, `claude:S04`, `claude:T05` | 1, 2, 3 | **DA_VA_THAT** |
| `trang-thai-job-khong-khop-conclusion` | `claude:R02` | 1 | **DA_VA_THAT** |
| `landed-khong-buoc-loi-khai-hop-le` | `claude:R04`, `claude:S01` | 1, 2 | **DA_VA_THAT** |
| `l8-chua-chot-thu-tu-cutover` | `claude:R07` | 1 | **DA_VA_THAT** |
| `khong-kiem-co-toan-ven-provenance` | `claude:R08` | 1 | **DA_VA_THAT** |
| `hop-dong-dau-vao-dau-ra-chua-chot` | `claude:R09`, `claude:S07`, `codex:T02`, `claude:T03` | 1, 2, 3 | **VA_MOT_PHAN** |
| `nguon-doc-khong-neo-cung-snapshot` | `claude:R12`, `claude:S02` | 1, 2 | **DA_VA_THAT** |
| `he-qua-gioi-han-khai-thieu` | `claude:R10`, `claude:T02`, `claude:T04` | 1, 3 | **DA_VA_THAT** |

`DA_VA_THAT` trong bảng là đóng lỗi **đặc tả** bằng nội dung hiện hành và phép đo được dẫn cho từng lớp trong JSON; không chứng nhận implementation chưa viết. Với lớp công bố hệ quả/giới hạn, nghĩa vụ cũ là công bố đúng phạm vi. Log/provenance/readback không ký và L8 chưa neo head vẫn là giới hạn công khai, không được coi đã vá runtime.

Có **3 lớp xuất hiện ở cả vòng 1, 2, 3**: nghiệm thu không cô lập chốt đích; số đo không cùng phạm vi nguồn; hợp đồng đầu vào/đầu ra chưa chốt. Đếm một lớp một lần mỗi vòng dù cả hai reviewer cùng báo. Hai lớp đầu ra/nghiệm thu còn mở một phần ở vòng 4; lớp Windows là mới, không đưa vào tử số hội tụ.

| Chuyển tiếp | Hội tụ theo §12 |
|---|---|
| 1 → 2 | `KHONG_DO_DUOC`: thiếu bảng lớp và phạm vi quét tại lượt cũ; không suy tỷ lệ lớp từ số ID được ghi ĐÓNG. |
| 2 → 3 | `KHONG_DO_DUOC`: cùng thiếu hụt; có biểu hiện được tách sang ID mới và approve khi P3 còn mở. |
| 3 → 4 | **2/4 = 50%** trên bốn lớp mở dựng từ bảy P3 vòng 3: đóng lớp số đo và công bố hệ quả; hai lớp còn lại `VA_MOT_PHAN`. Các nghĩa vụ cũ khác không đổi trong diff bản sửa 3 và được đối chiếu ở bảng trên. |

§12 đã chạm điều kiện một lớp xuất hiện ba lượt: lượt vá kế phải xét lại cách làm, dùng ma trận toàn lớp thay vì vá tiếp từng ví dụ. Không tự mở thêm review, không reset lịch sử r7/r8 hoặc ngân sách. Checkpoint không tự sinh câu hỏi chủ kho ngoài E1–E5.

**Bản sửa 3 và mục 1–2 của Issue.** Sửa `mC6`, giới hạn kết luận của `mC12`, bổ sung `m50`, fallback `failed:-`, phạm vi attempt chỉ khi passed, công bố hậu duệ/waiver cũ và sửa `60/62` đều có căn cứ. `m50` chỉ làm checkout rỗng đổi màu; healthy và A1-14(a–c) không đổi. Hợp đồng success nhánh miễn còn U01.

Trong phạm vi đã kiểm, chưa tìm thấy lời khai `passed/measured` mới qua thiết kế L8/D2b mà thiếu tệp danh-gia khớp provenance run land, ngoài các giới hạn đã khai. L8 buộc ít nhất một tệp và mọi tệp qua K1–K8; D2b thêm neo run/attempt/head. Waiver hợp lệ và miễn theo băm là các disposition riêng. Kết luận này dựa trên giả định tin provenance được cấp; không chứng minh authenticity GitHub hay nội dung log. Lệch mục 3 của Issue đã được đặc tả khai tường minh, không bị nhầm thành đạt mục đó.

Các phép đo chính đã chạy, rc thực bằng 0:

| Command | Bằng chứng dương / phạm vi |
|---|---|
| `python3 -B ops/reviews/wp1236-r9-soan/thamchieu.py .` | 66 tệp: **47/10/9**; sáu fixture đúng; output trùng byte tệp trong kho. |
| `python3 -B ops/reviews/wp1236-r9-soan/do_loi_khai.py .` | 170 hồ sơ: **25/56/39/50**; **93** vi phạm phân rã **39/36/12/2/2/2**. |
| `python3 -B ../work/audit_r4.py` | `AUDIT_R4_COMPLETE`: **94/94** landed, 0 lệch; **60/62** cặp hồ sơ-token; CRLF/CR lẻ/trộn + target/non-target; conclusion; bốn vế K3; B8; archive; OID ADR và 28 ca/50 mutant. |
| `python3 -B ../work/audit_targets_r4.py` | `TARGETS_R4_COMPLETE`: ba dạng landed và false control; m50 target/non-target; năm CHECK_BAT_BUOC; 48 M8/0 attempt, bốn waiver và ba M8 hậu duệ. |
| `python3 ../kiem_verdict_lop.py ../work/VERDICT.json --vong 4` | `HOP_LE (§8.3): 3 finding, 3 lop`. |

Output và hash lưu trong `execution_receipts` của JSON; phép đo chi tiết: [audit_r4.json](/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/work/audit_r4.json), [audit_targets_r4.json](/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/work/audit_targets_r4.json). Validator: [kiem_verdict.txt](/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/work/kiem_verdict.txt). 50 bản script đúng 20/28/2 theo ba hash; `kich_thuoc/nang_tran`, dòng ADR-0053/0055, `pham_vi_e` và `luat_dung` không có sai số/vi phạm mới được xác định ngoài U03 về nghĩa vụ kiểm chứng. Numstat triển khai và quyền nâng trần chưa được giả định là đã có.

`passed`: các phép đo offline ở trên. `failed`: yêu cầu đặc tả U01–U03. `skipped`: không có phép đo đã chạy bị bỏ qua. `not_run`: mã r9/L8/D2b tương lai, full CI, Windows local/CI, Ruff lint/pin-probe và API GitHub. Các thử nghiệm tham chiếu không thay cho gate implementation. Lệnh đọc đầu tiên đoán nhầm thư mục provenance pr1440 báo tệp vắng; đã tìm đúng bằng `rg`, không dùng lỗi setup đó làm finding.

Provider `openai_codex`, execution surface `codex_service` (API/công cụ shell), transport `machine`; không có launcher receipt để tự khai CLI, model/effort/session phục vụ là `KHONG_DO_DUOC`. Context reviewer độc lập với Executor; không tạo subagent. Sandbox thực `workspace-write`, nhưng mọi ghi nằm trong `work/`. Không gọi mạng/GitHub, không commit/push.

Snapshot trước/sau: **17.357 tệp, delta 0**, gồm ignored `.codex/` đã có trước; HEAD/tree/status/diff/index không đổi. Đây chỉ là đối chiếu hai mốc trong checkout được giao, không chứng minh toàn lịch sử run hoặc repo nguồn ngoài phạm vi quan sát. Chi tiết: [preflight.json](/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/work/preflight.json), [postflight.json](/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/r9-4-codex/work/postflight.json).

KET_LUAN: changes_requested
