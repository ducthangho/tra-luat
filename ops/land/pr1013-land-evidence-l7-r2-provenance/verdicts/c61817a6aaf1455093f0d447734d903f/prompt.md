# Cross-review (sensitive) — packet land-evidence-l7 r2 g1, mission #748, kho ducthangho/tra-luat

Bạn là REVIEWER độc lập, phiên mới, sandbox READ-ONLY. Không sửa tệp nào. Checkout ở thư mục làm việc hiện tại,
HEAD phải = ab25bd0f0f98139ed901605d04576903a92b9cf7 (kiểm `git rev-parse HEAD`; lệch thì dừng và báo).
Base = 0a8f4d78d30854247a7147e45f5586bf856925da. Diff cần review: `git diff 0a8f4d7..ab25bd0`
(chỉ hai tệp `ops/land_evidence_nguon.py`, `ops/land_evidence_nguon_test.py`).

Đặc tả đóng băng: `ops/specs/land-evidence-l7-r2-moi-do-sau.md` (sha256 phải = b43528c572e55bb29049fec44196550ddb5ff88ca356aa2d444473a823b9995a;
tự đo bằng `sha256sum`). Đọc toàn bộ đặc tả, docstring đầu `ops/land_evidence_nguon.py` (luật L1–L7) và CLAUDE.md
phần "Bài học" (đặc biệt: đột biến bị giết đúng lý do, danh sách cấm vs cho phép, ca có MẶT khác ca có ĐO).

Nhiệm vụ: tìm lỗi THẬT của bản vá so với §2/§3 đặc tả. Hướng nên soát:
1. Luật §2: khối gốc mapping là nguồn duy nhất (khoá lồng DAT ⇒ ghi chú, không vi phạm); không có khối gốc ⇒ mọi khoá
   lồng (mọi độ sâu, kể cả list) chuẩn hoá ra DAT là MỘT vi phạm với thông báo đúng định dạng đặc tả; giá trị không phải
   chuỗi ⇒ không áp, ghi chú; MIEN_TRU_L7 giữ nguyên. Có đường nào lọt (khoá không phải chuỗi, gốc tài liệu là list,
   assurance_81 vô hướng/list/null, đường dẫn trùng chuỗi `$.assurance_81.reviewer_assurance_81` do khoá chứa dấu chấm, v.v.)?
2. Bốn ca r1 "L7 không áp" ở c17 đã được đổi sang đòi ĐỎ theo r2. §3 ghi "các ca L7 r1 hiện có vẫn đạt" — đánh giá việc
   đổi này đúng với §2 hay là vi phạm đặc tả.
3. Đột biến mới (`L7r2_*` trong DOT_BIEN): mỗi chốt mới có đột biến riêng bị giết đúng ca đích chưa (gỡ độ sâu → c20,
   gỡ list → c21, đảo khối gốc → c22)? Có chốt nào KHÔNG có đột biến? Có đột biến nào chỉ giết vì lý do vô can?
4. Ca test có đo đúng điều nó khai không (chuỗi `chua`/`khong` có quá rộng/hẹp không — xem bài học "CẤM MỘT CHUỖI CON")?
5. Docstring/chú thích có khai rộng hơn phép đo không.

Sandbox read-only nên có thể không chạy được bộ test (nó cần thư mục tạm). Cứ THỬ chạy
`python ops/land_evidence_nguon.py` (chỉ đọc cây thật) và nếu được thì
`python ops/land_evidence_nguon_test.py --mot-ca c22_l7r2_khoi_goc_la_nguon_duy_nhat`. Không chạy được thì nói rõ
"KHÔNG ĐO ĐƯỢC" cho phần đó và review bằng đọc mã. Executor khai đã đo trên head này: test `CA: 22/22`,
`DOT BIEN: 104/104 bi giet dung ly do`, `TONG: DAT`; cây thật `54 ĐẠT · 25/28 miễn trừ · 0 vi phạm`, chỉ pr870/pr889
có ghi chú `$.cap_nhat_20261026.reviewer_assurance_81` — coi đó là LỜI KHAI cần kiểm, không phải sự thật.

Hướng thử nào cần soạn đầu vào đặc biệt thì MÔ TẢ BẰNG LỜI, không cần dựng.

ĐẦU RA (bắt buộc, cuối cùng): một khối
```
VERDICT: APPROVE | REQUEST_CHANGES
reviewed_head: <sha40>
spec_sha256: <đo được>
FINDINGS:
- [P0|P1|P2|P3] <tệp:dòng> — <mô tả> — <đường tái hiện cụ thể> — <đề xuất sửa>
(hoặc "- không có")
DA_DO: <những gì đã chạy được, kèm rc>
KHONG_DO_DUOC: <những gì không chạy được>
```
APPROVE chỉ khi 0 finding P0–P3.
