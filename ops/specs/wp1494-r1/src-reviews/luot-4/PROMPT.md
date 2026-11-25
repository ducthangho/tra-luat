# Review mã nguồn wp1494 (B2, Mission #1172) — lượt 4 (LƯỢT CUỐI, không có lượt 5), Codex, chỉ đọc

Bạn là REVIEWER độc lập (Codex gpt-6-astra, suy luận cao nhất) cho packet wp1494 của kho ducthangho/tra-luat.
Bạn KHÔNG phải executor. Bạn KHÔNG sửa tệp nào trong `src/`, KHÔNG commit, KHÔNG push, KHÔNG gọi GitHub để ghi, KHÔNG dispatch workflow.
Trả lời bằng tiếng Việt.

## Thứ được review (định danh là BĂM, không phải tên nhánh)
- Thư mục làm việc: `src/` (clone của https://github.com/ducthangho/tra-luat, đã fetch mọi nhánh `origin/*`, không shallow).
- Ứng viên H = `dac537eb7fdb75fb74e1f0cfa17a67dc4ec69cae`, tree `b09ec579523ad20492c4160850d6bb349445c0d0`, nhánh cục bộ `agent/wp1494-r5-g4-fable` (CHƯA đẩy lên GitHub). Kiểm: `git -C src rev-parse HEAD HEAD^{tree}`.
- B (base) = `b4b79bf0cd301bb067a22c5245505d9a8ab232cb` (merge PR #1516 của B1a).
- H3 (lượt 3 đã review) = `c524d1233c2709679e31cd972711d4b8d5534fa8`; H3..H chỉ đổi hai tệp `ops/canh_tuoi_audit*.py`.
- Đặc tả đóng băng: `git -C src show a819291bb08af5e72cdd833b86544ea48d97b1fd:ops/specs/wp1494-r1/SPEC.md`, sha256 phải là `345520e199ba7072c2bea92b876a3db1877cabce7969f82a379bb078d1dc2e4d` (revision 5). Đo băm trước khi đọc. Đọc TOÀN BỘ đặc tả.
- Lease: `git -C src show origin/ops/wp1494-r1:ops/leases/wp1494-r5-g4-claude-20261125.yaml` (trần 6 tệp / 3500 dòng thêm theo `nang_tran`).
- Tham số thi công Mission r109: `git -C src show 2e70d3b3dada5babd17e6c5e83f8c2b16cacc874:ops/specs/wp1172-source-plan-r4/MCR-1172-r109.md`.
- Handoff của executor: `HANDOFF.yaml` (thư mục hiện tại; sha256 `29a7b6a4623d0f484aeab4d2f34f0c765c2ca4a13f8aaeb2811d2d2fb60903cd`); bằng chứng của executor (log cổng, script của reviewer đã chạy lại, bản sửa `*_g4.py`) ở `bang-chung-executor/`.
- Verdict lượt 3 (trên H3): `review-3/VERDICT.md`, probe ở `review-3/evidence/` (gồm `rv3_deadline_coverage.py`, `resource_stop.py`, `resource_stop_signals.py`); bản commit ở `origin/ops/wp1494-r1:ops/specs/wp1494-r1/src-reviews/luot-3/`.
- Verdict lượt 2 và lượt 1: `review-2/`, `review-1/` (bản commit ở `.../src-reviews/luot-2/`, `luot-1/`).
- Quyết định chủ kho sau lượt 3 (Review Rescue lần hai): https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7163782461 — executor lượt 5/5 CHỈ vá RV3-F03 và RV3-F04, không cơ chế mới; đây là lượt review Codex cuối.
- **Miễn trừ đã ghi của chủ kho (giữ nguyên):**
  - https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7162892740 — giới hạn pha MỞ kết nối (DNS/connect/TLS/gửi/đọc status+header trong `urllib open()`) chỉ bị chặn bởi socket timeout từng thao tác là RỦI RO TỒN DƯ ĐÃ CHẤP NHẬN. Miễn trừ neo vào H3; mã pha mở ở H được executor khai là trùng byte với H3 — hãy ĐO điều đó (diff H3..H trên các hàm pha mở). Nếu trùng, miễn trừ áp nguyên; ghi vào mục "Rủi ro tồn dư đã miễn" (không đánh P0–P2). Mọi thứ KHÁC trong lớp hạn vẫn phán bình thường.
  - https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7157619068 — MIỄN quan sát dòng đột biến 134 (bất khả theo schema ghim), ngoài mẫu số, không tín dụng.
- Đọc thêm: `src/CLAUDE.md`, `src/AGENTS.md`, `src/docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12.

## Điều kiện của B — đo lại TRƯỚC khi review (lệch ⇒ ghi `blocked`)
Đủ mọi điều của mục "Baseline nghiệm thu" của đặc tả, băm khối "Lệnh kiểm" (`d9c78e70…`) trên `d1b08c219227d4b8925702029cd20d4e0febed54:ops/specs/wp1460-r1/SPEC.md`, và bốn hàm chép nguyên văn (`tieu_dung`, `khoa_tu_ten`, `doc_moc`, `khung_cron`) trùng byte khối ấy.

## Lời khai của executor cần bạn ĐO LẠI (đừng nhận lời)
- numstat `git diff --numstat B H`: 4 tệp, +3415/−0 (`ci_dang_ky_test.py` +1, workflow +29, `ops/canh_tuoi_audit.py` +1051, test +2334).
- `python3 ops/canh_tuoi_audit_test.py` → rc 0; `CA: 478/478 dat` · `DOT BIEN: 289/289 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (5 dot bien)` · `TONG: DAT`. (Phiên điều phối đã đo lại trên clone sạch: khớp.)
- `python3 .claude/dev/ci_dang_ky_test.py` → rc 0, `PHẢN CHỨNG: 1677/1677 đỏ đúng`, `TỔNG: ĐẠT`. actionlint rc 0; ruff F 0.
- RV3-F03: khôi phục ba ca quá hạn tên cũ (`n15_cho_qua_han`, `n15_han_cuoi_ghi`, `n15_d14_khop_qua_han`), tách ca đúng-bằng-hạn riêng; với tám phép so hạn (d104, d106, f02:d14, d105, d99, w0:tron_ven, f02:vong_doc, f02:nen_han) có bộ đột biến gỡ/biên/chỉ-bằng (Q01–Q03 và các bản mới), 24 đột biến đều giết. Executor khai tám phép so là TOÀN BỘ phép so hạn trong mô-đun.
- RV3-F04: dừng ngay khi cạn trần giải nén tổng ở bốn chỗ gọi (`f04:goi`, `f04:t5`, `f04:t3`, `f04:t7`) cộng `f04:e` trả S1 ngay sau mỗi `_phan_luot`; ca `n2_can_tn_t2`, `n2_can_tn_t5` đòi 0 GET đánh giá và 0 lần mở ZIP sau lúc cạn, S1 `het_tai_nguyen_danh_gia`, `sha_audit` null, 1 PATCH, mã thoát 1. Thay đổi hành vi: báo cáo của S1 này có `khung: {}`.
- Script của bạn lượt 3 trên H: `rv3_deadline_coverage.py` (nguyên) rc 0 `RV3_DEADLINE_COVERAGE_COMPLETE`, Q01–Q03 0→3 GIET; `resource_stop.py` (nguyên) rc 0, 0 GET/0 ZIP sau khi cạn; `resource_stop_signals.py` (nguyên) rc 1 vì dòng 33 khẳng định mã CŨ hỏng, bản `_g4` đổi dòng 33–34 thành 2/2.
Đặt `git config core.abbrev 7` trong mọi bản sao bạn dựng. Ghi lệnh, rc và dòng dương THẬT bạn đo.

## Câu hỏi executor để lại cho bạn
1. `khung: {}` trên S1 cạn tài nguyên có chấp nhận được theo đặc tả không (giữ các lượt đã đánh giá sẽ phải đánh dấu lượt chưa đánh giá — executor coi là cơ chế mới)?
2. Miễn trừ pha mở neo H3 — mã pha mở ở H có thật trùng byte không?
3. Hai cấu trúc test chỉ tồn tại để script của bạn chạy nguyên (`g.t = 180.0` rồi `g.t += qua`; hai `thay_ten("_khop", …)` lồng) — có che lỗi nào không?
4. Dừng ở bốn chỗ gọi, không thêm chốt trung tâm trong `_goi`/`_tho_zip` (sẽ không với tới được với caller hiện tại) — đủ đóng LỚP `unbounded-artifact-expansion` chưa, hay còn đường nào sau lúc cạn vẫn làm việc?

## Việc của bạn
1. **CHẠY** các ca đã commit và bộ đột biến; đo lại mọi lời khai ở trên.
2. **ĐỘT BIẾN BẢN VÁ** trên một bản sao TẠM ngoài `src/`: tập trung vào mã MỚI giữa H3 và H (năm chốt `f04:*`, tám phép so hạn và ca của chúng), và săn phép so hạn THỨ CHÍN mà executor khai không có. Một đột biến chỉ tính là GIẾT khi ca ĐÍCH đỏ vì đúng lý do (`TinHieuChotCa` của chính ca ấy). Báo đột biến SỐNG và GIẾT SAI LÝ DO. Lưu ý: `n1_j_doc_theo_khuc` dùng luồng vô hạn có chủ đích — đột biến làm hỏng chốt `TRAN_GOI` có thể ngốn bộ nhớ; chạy dưới `ulimit -v`.
3. **Đầu vào thù địch — chỉ mô tả bằng lời, đừng tự soạn payload tấn công.** Chỉ dựng fixture DỮ LIỆU thường (JSON REST giả, zip giả bình thường) để đo. Ưu tiên: cạn trần tổng ở mọi vị trí (gói đầu, giữa T5, giữa các lượt E, đúng gói cuối), đồng hồ chạm đúng hạn và vượt hạn ở từng phép so, POST hoàn tất sau hạn.
4. **Lớp nguyên nhân (§8.3):** mỗi finding gắn một lớp nguyên nhân (slug kebab-case) và trả lời: lớp ấy còn ở chỗ nào khác trong bản vá không?
5. **Bảng đối chiếu lượt trước (BẮT BUỘC):** với từng finding F01–F03 lượt 1, F02–F03 lượt 2, RV3-F03 và RV3-F04 lượt 3, xếp đúng một nhãn `ĐÃ SỬA ĐÚNG LỚP` · `VÁ HỜ` · `CHƯA SỬA` · `VÁ SINH LỖI MỚI`, kèm phép đo. Xếp lại các lớp đặc tả (`notification-dedup-before-delivery`, `mutant-oracles-non-discriminating`, `consumer-freshness-anchor-unverified`, `bounded-evaluation-order-dependent`, `heartbeat-value-domain-incomplete`, `unbounded-artifact-expansion`…) vào `ĐÃ SỬA ĐÚNG LỚP` · `VÁ HỜ` · `CHƯA SỬA` · `KHÔNG ÁP DỤNG`.
6. **BẢNG SĂN ≥ 6 hướng:** giả thuyết, phép đo đã chạy, kết quả (kể cả hướng không ra gì).
7. Kiểm write set: đúng bốn tệp, `ci_dang_ky_test.py` chỉ thêm đúng một mục MOI nguyên văn đặc tả; không có chuỗi đánh dấu bỏ-qua-CI trong tệp hay commit message.

## Đầu ra
Ghi TĂNG DẦN (sau mỗi phần xong) vào `out/VERDICT.md` trong thư mục hiện tại, gồm:
- dòng đầu: `VERDICT: approve | changes_requested | blocked` (cập nhật khi xong);
- `reviewed_sha: dac537eb7fdb75fb74e1f0cfa17a67dc4ec69cae`, `reviewed_tree: b09ec579523ad20492c4160850d6bb349445c0d0`, `spec_sha256: 345520e1…`;
- hai trục `Spec` và `Standards/Security`;
- bảng finding: id, severity P0–P3, lớp nguyên nhân, tệp:dòng, mô tả, bằng chứng chạy được (lệnh + output), gợi ý vá (chỉ là gợi ý);
- bảng đo lại lời khai; điều kiện của B; bảng đột biến của bạn; bảng đối chiếu lượt trước và lớp đặc tả; BẢNG SĂN; phán bốn câu hỏi của executor; mục "Rủi ro tồn dư đã miễn"; mục KHÔNG ĐO ĐƯỢC.
Approve chỉ khi không còn P0–P2. Dọn thư mục nháp của chính bạn khi xong là được, nhưng giữ `out/`.
