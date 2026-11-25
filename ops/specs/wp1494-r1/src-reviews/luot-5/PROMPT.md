# Review mã nguồn wp1494 (B2, Mission #1172) — lượt 5 HẸP (cuối cùng), Codex, chỉ đọc

Bạn là REVIEWER độc lập (Codex gpt-6-astra, suy luận cao nhất) cho packet wp1494 của kho ducthangho/tra-luat.
Bạn KHÔNG phải executor. Bạn KHÔNG sửa tệp nào trong `src/`, KHÔNG commit, KHÔNG push, KHÔNG gọi GitHub để ghi, KHÔNG dispatch workflow.
Trả lời bằng tiếng Việt.

## Phạm vi (quyết định chủ kho https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7170825561)
Lượt này là review HẸP: (a) RV4-F01 đã sửa đúng lớp chưa; (b) bản vá có gây hồi quy cho phần đã được lượt 4 xếp đúng không, nhất là chốt dừng tài nguyên (RV3-F04) và các phép so hạn (RV3-F03). KHÔNG mở lại các lớp đã đóng trừ khi bản vá H4..H chạm vào chúng hoặc bạn đo được hồi quy. Lỗi CÓ TỪ TRƯỚC H4 mà không do H4..H gây ra: ghi ở mục "Ngoài phạm vi, có sẵn" kèm mức độ, không tính vào verdict trừ khi P0/P1.

## Thứ được review (định danh là BĂM)
- `src/`: clone của https://github.com/ducthangho/tra-luat, đã fetch mọi `origin/*`, không shallow.
- H = `6ffb936e465c36ceba774442d8252f81a8f4ff7d`, tree `a263444f41b92769bd5e5407b200c8fc441f2b71`, nhánh cục bộ `agent/wp1494-r5-g5-fable` (chưa đẩy). Kiểm `git -C src rev-parse HEAD HEAD^{tree}`.
- H4 (lượt 4) = `dac537eb7fdb75fb74e1f0cfa17a67dc4ec69cae`; H4..H chỉ đổi `ops/canh_tuoi_audit.py` (+16/−5) và `ops/canh_tuoi_audit_test.py` (+30/−0). B = `b4b79bf0cd301bb067a22c5245505d9a8ab232cb`.
- Đặc tả: `git -C src show a819291bb08af5e72cdd833b86544ea48d97b1fd:ops/specs/wp1494-r1/SPEC.md`, sha256 phải là `345520e199ba7072c2bea92b876a3db1877cabce7969f82a379bb078d1dc2e4d`. Đo trước khi đọc. Đọc kỹ §3 (tất-cả-hoặc-không), §5 (luật gộp), §6 (báo cáo), và các dòng từ vựng `khong_danh_gia`, `khong_do_duoc`, `het_tai_nguyen_danh_gia`.
- Lease: `git -C src show origin/ops/wp1494-r1:ops/leases/wp1494-r5-g5-claude-20261125.yaml`.
- Handoff executor: `HANDOFF.yaml` (sha256 `dbc5eb70ae194d11d37af28fb67f1f529e268188ea79a19431582a8949038362`); bằng chứng ở `bang-chung-executor/` (log cổng, bản `_g5` của script của bạn).
- Verdict lượt 4 của bạn: `review-4/VERDICT.md`, probe ở `review-4/evidence/` (`rv4_report_contract.py`, `rv4_resource_matrix.py`, `resource_stop.py`, `rv4_mutations.py`…). Lượt 1–3: `origin/ops/wp1494-r1:ops/specs/wp1494-r1/src-reviews/luot-{1,2,3}/`.
- Miễn trừ giữ nguyên: D134 (7157619068); pha mở `urllib open()` (7162892740) — đo lại pha mở trùng byte H4..H, nếu trùng thì áp nguyên.

## Lời khai executor cần ĐO LẠI
- numstat B..H: 4 tệp, +3456/−0 (1, 29, 1062, 2364), trần 3500.
- Suite: rc 0, `CA: 481/481 dat` · `DOT BIEN: 293/293 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (5 dot bien)` · `TONG: DAT` (phiên điều phối đo lại trên clone sạch: khớp). `ci_dang_ky_test.py` 1677/1677 ĐẠT. actionlint 0, ruff F 0.
- Sửa: `f04:e` giữ điều kiện `if c.can_tn:` nhưng thân là `break` thay vì `return s1(...)`; lượt đã đánh giá giữ nguyên kết quả đo; lượt đang đánh giá lúc cạn được phán `khong_do_duoc`, mã `het_tai_nguyen_danh_gia`; lượt E chưa đánh giá dựng từ mẫu `_luot_trong` (không REST, không ZIP, không gọi `_phan_luot`, mọi phép con `khong_danh_gia`, T4 `dat`); sau khi dựng khung, `if c.can_tn: return s1("het_tai_nguyen_danh_gia")` chạy TRƯỚC O / `dong_den` / S2..S9 / chọn SHA.
- Ca/đột biến mới: `n2_can_tn_giu_luot`/`rv4_giu`; `n2_can_tn_chua_danh_gia`/`rv4_can`, `rv4_con`; `n2_can_tn_khong_dung_luot_giu`/`rv4_s1`.
- Script của bạn: `rv4_report_contract.py` nguyên bản H rc 0 nhưng script thoát 1 ở assert cuối đòi H còn hỏng; `rv4_resource_matrix.py` nguyên bản mọi assert tài nguyên đạt, thoát 1 ở `lost[0]` vì danh sách mất bằng chứng nay rỗng; `resource_stop.py` rc 0; `rv4_mutations.py` rc 1 với 53 dòng giống hệt log lượt 4 của bạn (6 cặp sai lý do nhóm `f02_vong_doc`, có sẵn).

## Câu hỏi executor
1. Ở báo cáo S1, khung gộp theo luật §5 không đổi, nên một khung có thể ghi `dat` trong khi trạng thái tổng là S1, sha null. Ép mọi khung không-thủ-công thành `khong_do_duoc` sẽ là luật gộp mới đặc tả không nêu. Đúng theo đặc tả không, và có gây hiểu sai cho người đọc báo cáo/Issue #1520 không?
2. Lượt cạn bị ép phán `khong_do_duoc`/`het_tai_nguyen_danh_gia` thay vì "mã của phép con đầu tiên" (SPEC ~dòng 158) vì T7 chưa chạy; phép con chạm trần vẫn ghi `goi_vuot_tran`. Đúng hay nên dùng `goi_vuot_tran`?
3. Đường lưới an toàn `danh_gia_nem:` vẫn trả `khung` rỗng — có thuộc lớp RV4-F01 không?

## Việc của bạn
1. CHẠY suite, đo lại lời khai, chạy lại probe lượt 4 của bạn.
2. ĐỘT BIẾN BẢN VÁ trên bản sao tạm ngoài `src/`: gỡ/nới từng chốt mới (giữ lượt, phán lượt cạn, mẫu lượt chưa đánh giá, `return s1` sau dựng khung, cộng năm chốt `f04:*`). Chỉ tính GIẾT khi ca ĐÍCH đỏ vì `TinHieuChotCa` của chính nó. Chạy dưới `ulimit -v` (ca `n1_j_doc_theo_khuc` có luồng vô hạn có chủ đích).
3. Săn theo LỚP `evaluation-report-evidence-dropped`: còn đường S1/S-sớm nào khác bỏ quan sát đã có không? Và lớp ngược: lượt giữ lại có lọt vào kết luận (sha, `dong_den`, fresh, nội dung comment/Issue) qua đường nào không? Chỉ dựng fixture DỮ LIỆU thường; hướng thù địch chỉ mô tả bằng lời.
4. Gắn lớp nguyên nhân (§8.3) cho mỗi finding.
5. Bảng đối chiếu: RV4-F01, RV3-F03, RV3-F04 — nhãn `ĐÃ SỬA ĐÚNG LỚP` · `VÁ HỜ` · `CHƯA SỬA` · `VÁ SINH LỖI MỚI`, kèm phép đo.
6. BẢNG SĂN ≥ 6 hướng.
7. Write set đúng bốn tệp, mục MOI nguyên văn, không dấu bỏ-qua-CI trong tệp hay commit message.

## Đầu ra
Ghi TĂNG DẦN vào `out/VERDICT.md`:
- dòng đầu `VERDICT: approve | changes_requested | blocked`;
- `reviewed_sha: 6ffb936e465c36ceba774442d8252f81a8f4ff7d`, `reviewed_tree: a263444f41b92769bd5e5407b200c8fc441f2b71`, `spec_sha256: 345520e1…`;
- trục `Spec` và `Standards/Security`; bảng finding (id, severity P0–P3, lớp, tệp:dòng, mô tả, bằng chứng chạy được, gợi ý); bảng đo lại lời khai; bảng đột biến; bảng đối chiếu; BẢNG SĂN; phán ba câu hỏi; "Rủi ro tồn dư đã miễn"; "Ngoài phạm vi, có sẵn"; KHÔNG ĐO ĐƯỢC.
Approve chỉ khi không còn P0–P2 trong phạm vi. Không đo được socket thật trong sandbox thì ghi KHÔNG ĐO ĐƯỢC, không tính là lỗi sản phẩm. Dọn nháp của bạn khi xong, giữ `out/`.
