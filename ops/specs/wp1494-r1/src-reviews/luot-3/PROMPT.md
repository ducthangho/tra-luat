# Review mã nguồn wp1494 (B2, Mission #1172) — lượt 3 (LƯỢT CUỐI), Codex, chỉ đọc

Bạn là REVIEWER độc lập (Codex gpt-6-astra, suy luận cao nhất) cho packet wp1494 của kho ducthangho/tra-luat.
Bạn KHÔNG phải executor. Bạn KHÔNG sửa tệp nào trong `src/`, KHÔNG commit, KHÔNG push, KHÔNG gọi GitHub để ghi, KHÔNG dispatch workflow.
Trả lời bằng tiếng Việt.

## Thứ được review (định danh là BĂM, không phải tên nhánh)
- Thư mục làm việc: `src/` (clone của https://github.com/ducthangho/tra-luat, đã fetch mọi nhánh `origin/*`, không shallow).
- Ứng viên H = `c524d1233c2709679e31cd972711d4b8d5534fa8`, tree `0dc451fddbfc48217c6fac9fb46187a0f55fdc0f`, nhánh cục bộ `agent/wp1494-r5-g3-fable` (CHƯA đẩy lên GitHub). Kiểm: `git -C src rev-parse HEAD HEAD^{tree}`.
- B (base) = `b4b79bf0cd301bb067a22c5245505d9a8ab232cb` (merge PR #1516 của B1a).
- Đặc tả đóng băng: `git -C src show a819291bb08af5e72cdd833b86544ea48d97b1fd:ops/specs/wp1494-r1/SPEC.md`, sha256 phải là `345520e199ba7072c2bea92b876a3db1877cabce7969f82a379bb078d1dc2e4d` (nhánh `origin/ops/wp1494-r1`, revision 5 = r4 cộng khối `nang_tran`). Đo băm trước khi đọc. Đọc TOÀN BỘ đặc tả, kể cả GHIM-B1A, bảng kết cục mục 3, bảng đột biến, mục "Baseline nghiệm thu".
- Lease: `git -C src show origin/ops/wp1494-r1:ops/leases/wp1494-r5-g3-claude-20261125.yaml` (trần 6 tệp / 3500 dòng thêm theo `nang_tran`).
- Tham số thi công Mission r109: `git -C src show 2e70d3b3dada5babd17e6c5e83f8c2b16cacc874:ops/specs/wp1172-source-plan-r4/MCR-1172-r109.md` (B, `ISSUE_THEO_DOI` = 1520, `KHUNG_DAU` = `2026-11-28T19:17:00Z`).
- Handoff của executor: `HANDOFF.yaml` (thư mục hiện tại; sha256 `7078af6d04015619e3c81f16859dc74eddf146e0bc3538913ee4d4f6212dac13`); bằng chứng của executor (log cổng, script của reviewer đã chạy lại, bản sửa `*_g3.py`) ở `bang-chung-executor/`.
- Verdict lượt 2 (trên H2 = `d3bcd6a171644b18d9fd37a185cfb8fc6d641ef4`): `review-2/VERDICT.md` và probe ở `review-2/evidence/`; bản commit ở `origin/ops/wp1494-r1:ops/specs/wp1494-r1/src-reviews/luot-2/`.
- Quyết định chủ kho sau lượt 2 (Review Rescue): https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7161189582 — executor lượt 4/4 CHỈ vá hẹp F02 và F03, không cơ chế mới.
- **Miễn trừ đã ghi của chủ kho:** https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7162892740 — giới hạn pha MỞ kết nối (DNS/connect/TLS/gửi/đọc status+header trong `urllib open()`) chỉ bị chặn bởi socket timeout từng thao tác là RỦI RO TỒN DƯ ĐÃ CHẤP NHẬN. Nếu bạn thấy đúng điểm ấy, ghi nó vào mục "Rủi ro tồn dư đã miễn" (không đánh P0–P2, không làm verdict thành changes_requested). Mọi thứ KHÁC trong lớp hạn (đọc thân, mọi đường đã vá) vẫn phán bình thường.
- Verdict lượt 1 (trên H1 = `127b82a8a9e41fda3c4a230810118f0bedfb200d`): `review-1/VERDICT.md` và probe của nó ở `review-1/evidence/` (thư mục hiện tại); bản đã commit ở `origin/ops/wp1494-r1:ops/specs/wp1494-r1/src-reviews/luot-1/`.
- Quyết định chủ kho sau lượt 1: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7157619068 — executor dùng lượt cuối 3/3 vá theo lớp; MIỄN quan sát dòng đột biến 134 (bất khả theo schema ghim), đột biến 134 ghi «tương đương theo schema», ngoài mẫu số, không tín dụng. Không có spec r6; mọi dòng khác giữ yêu cầu.
- Đọc thêm: `src/CLAUDE.md`, `src/AGENTS.md`, `src/docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12.

## Điều kiện của B — đo lại TRƯỚC khi review (đặc tả bắt reviewer tự đo; lệch ⇒ ghi `blocked`)
Đủ mọi điều của mục "Baseline nghiệm thu": B trên first-parent của `origin/master`; hai tệp `hop_dong` tại B bằng GHIM-B1A; `KHUNG_DAU` bằng `khung_cron` của thời điểm committer của B; job `bien-nhan-audit` và bước tải lên tại B; ba tệp mới vắng và 0 mục `canh_tuoi_audit_test` tại B. Kiểm thêm băm khối "Lệnh kiểm" (`d9c78e70…`) trên `d1b08c219227d4b8925702029cd20d4e0febed54:ops/specs/wp1460-r1/SPEC.md`, và bốn hàm chép nguyên văn (`tieu_dung`, `khoa_tu_ten`, `doc_moc`, `khung_cron`) trong `ops/canh_tuoi_audit.py` trùng byte khối ấy.

## Lời khai của executor cần bạn ĐO LẠI (đừng nhận lời)
- numstat `git diff --numstat B H`: 4 tệp, +3342/−0 (`ci_dang_ky_test.py` +1, workflow +29, `ops/canh_tuoi_audit.py` +1048, test +2264); H2..H chỉ đổi hai tệp `ops/canh_tuoi_audit*.py` (+273/−29).
- `python3 ops/canh_tuoi_audit_test.py` → rc 0; `CA: 469/469 dat` · `DOT BIEN: 275/275 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (5 dot bien)` · `TONG: DAT`.
- `python3 .claude/dev/ci_dang_ky_test.py` → rc 0, `PHẢN CHỨNG: 1677/1677 đỏ đúng`. actionlint rc 0; ruff F delta 0. Bộ test không gọi mạng (đã thử vá `connect`/`getaddrinfo` để ném: 469/469).
- F02: `_mot_lan` bọc luồng đệm của `HTTPResponse` (và `HTTPError`) bằng `_NenCoHan` (RawIOBase): mỗi lần đọc nền kiểm hạn tuyệt đối, đặt lại thời gian còn lại lên socket, tối đa một `recv`. Ca/đột biến riêng cho GET API, GET kho, PATCH, POST, thân HTTPError, và `n16_socket_that` (socketpair). Socket lấy qua thuộc tính riêng `SocketIO._sock`.
- F03: N01–N09 thành chín ca riêng với đột biến riêng; N06 sửa để đỏ bằng tín hiệu ca; dòng 61: 64 ca người ghi W2/W7 + 2 đối chứng, 23 đột biến D61 chạy trên W0/W2/W7; thêm ca đóng lớp (dòng 62/116 ở W2/W7, mọi nhánh con `_hinh_rest`, đột biến biên bằng hạn d104/d105/d106/D14, hai nửa `_hinh_issue`, ca PATCH cho vòng đọc). Ba ca cũ (`n15_cho_qua_han`, `n15_han_cuoi_ghi`, `n15_d14_khop_qua_han`) đổi đầu vào sang ĐÚNG bằng hạn.
- Script reviewer lượt 2 trên H: `rv2_distinguish.py` (nguyên) rc 0 `9/9`; `rv2_heartbeat_callers.py` (nguyên) rc 0 192/192; `rv2_mutations.py` (nguyên) rc 0, N02–N05/N07/N08 sống trên ca đích CŨ của bạn nhưng chết đúng một ca mới; `buffered_deadline.py` (nguyên) rc 1 chỉ vì assert mã hoá kết luận cũ (`original_rc==3`) — bốn dòng: t = 30,0 s, `TimeoutError`; bản `_g3` sửa dòng 41–43 cho `4/4 HEAD_BOUNDED_AT_30s`; `rv2_mutations_g3.py` chỉ đổi đối số ca đích N01–N09 và tên tệp ra, 12/12 giết.
Đặt `git config core.abbrev 7` trong mọi bản sao bạn dựng. Ghi lệnh, rc và dòng dương THẬT bạn đo.

## Câu hỏi executor để lại cho bạn
1. Ca đóng lớp vượt danh sách hẹp (khoảng 36 dòng) — trong phạm vi "vá hẹp" hay không?
2. Ba ca cũ đổi đầu vào sang đúng bằng hạn để một ca giết cả đột biến gỡ chốt lẫn đột biến biên — quan sát không đổi; có làm mất phủ "quá hạn" không?
3. Sửa script của bạn (`*_g3.py`) có chấp nhận làm bằng chứng không?

## Việc của bạn
1. **CHẠY** các ca đã commit và bộ đột biến; đo lại mọi lời khai ở trên.
2. **ĐỘT BIẾN BẢN VÁ** trên một bản sao TẠM ngoài `src/` (vd `cp -r src <nháp>/dot`): gỡ hoặc nới từng chốt quan trọng (bốn trạng thái và chiều một chiều của I2; nghĩa vụ khung cũ; LIÊN KẾT D1↔D2; hạn tuyệt đối kiểm cả lúc HOÀN TẤT; cạn tất-cả-hoặc-không; PATCH/POST đúng một lần gửi vật lý; bất biến "đang chờ không bao giờ bị xoá"; đối soát D14; bộ kiểm miền nhịp tim dùng chung người ghi/người đọc; trần giải nén; bộ kiểm hình workflow mục 8). Đo ca nào đỏ. Một đột biến chỉ tính là GIẾT khi ca ĐÍCH đỏ vì đúng lý do (`TinHieuChotCa` của chính ca ấy). Báo đột biến SỐNG và GIẾT SAI LÝ DO. Ưu tiên chỗ bảng đột biến của executor KHÔNG phủ, nhất là mã MỚI giữa H2 và H (`_NenCoHan`, bọc HTTPError, các ca mới).
3. **Đầu vào thù địch — chỉ mô tả bằng lời, đừng tự soạn payload tấn công.** Với mỗi hướng, nói đường mã nào xử lý nó và ca đã commit nào phủ nó; chỉ dựng fixture DỮ LIỆU thường (JSON REST giả, zip giả bình thường) để đo, không dựng gì nhằm thoát khỏi cây thư mục:
   - phân trang lặp/thiếu/đổi thứ tự, `total_count` nói dối, `created_at` sai dạng hoặc không có thật;
   - lượt bị chạy lại attempt, lượt `workflow_dispatch` lẫn vào, `head_sha` đổi giữa hai lần đọc D2;
   - comment giả dòng `B2_SU_KIEN` từ người không phải `github-actions[bot]`; thân Issue bị người sửa tay; nhịp tim cũ/hỏng/vắng;
   - phản hồi thiếu `X-GitHub-Request-Id`, chuyển hướng sang http hoặc host lạ, `Content-Length` nói dối, gói zip có nhiều mục hay tổng giải nén lớn;
   - đồng hồ đơn điệu chạm đúng hạn (biên chặt), POST hoàn tất sau hạn;
   - workflow `canh-tuoi-audit.yml` bị thêm khoá/bước/quyền.
4. **Lớp nguyên nhân (§8.3):** mỗi finding gắn một lớp nguyên nhân (slug kebab-case) và trả lời: lớp ấy còn ở chỗ nào khác trong bản vá không? Tìm theo LỚP, không dừng ở trường hợp đầu tiên.
5. **Bảng đối chiếu lượt trước (BẮT BUỘC):** với từng finding F01, F02, F03 của lượt 1 và F02, F03 của lượt 2, xếp đúng một nhãn `ĐÃ SỬA ĐÚNG LỚP` · `VÁ HỜ` · `CHƯA SỬA` · `VÁ SINH LỖI MỚI`, kèm phép đo. Săn LỚP: liệt kê mọi đường của mỗi lớp trong toàn bản vá (không chỉ chỗ lượt 1 chỉ), và nói đường nào còn hở. Cũng xếp lại các lớp đặc tả dưới đây.
5b. **Bảng đối chiếu lớp đặc tả:** đây là lượt review MÃ NGUỒN đầu tiên của packet (bốn lượt trước là review ĐẶC TẢ: `origin/ops/wp1494-r1:ops/specs/wp1494-r1/reviews/` nếu có, và bảng "Thay đổi" của đặc tả). Lấy các lớp đã nêu ở review đặc tả lượt 1–3 (`notification-dedup-before-delivery`, `mutant-oracles-non-discriminating`, `consumer-freshness-anchor-unverified`, `bounded-evaluation-order-dependent`, `heartbeat-value-domain-incomplete`, `unbounded-artifact-expansion`…) và xếp mỗi lớp vào đúng một trong bốn nhãn khi áp vào MÃ: `ĐÃ SỬA ĐÚNG LỚP` · `VÁ HỜ` · `CHƯA SỬA` · `KHÔNG ÁP DỤNG`, kèm bằng chứng đo.
6. **BẢNG SĂN ≥ 6 hướng:** liệt kê ít nhất sáu hướng bạn đã chủ động săn (kể cả hướng không ra gì), mỗi hướng: giả thuyết, phép đo đã chạy, kết quả.
7. Kiểm write set: đúng bốn tệp, `ci_dang_ky_test.py` chỉ thêm đúng một mục MOI nguyên văn đặc tả; không có chuỗi đánh dấu bỏ-qua-CI trong tệp hay commit message.

## Đầu ra
Ghi TĂNG DẦN (sau mỗi phần xong) vào `out/VERDICT.md` trong thư mục hiện tại, gồm:
- dòng đầu: `VERDICT: approve | changes_requested | blocked` (cập nhật khi xong);
- `reviewed_sha: c524d1233c2709679e31cd972711d4b8d5534fa8`, `reviewed_tree: 0dc451fddbfc48217c6fac9fb46187a0f55fdc0f`, `spec_sha256: 345520e1…`;
- hai trục `Spec` và `Standards/Security`;
- bảng finding: id, severity P0–P3, lớp nguyên nhân, tệp:dòng, mô tả, bằng chứng chạy được (lệnh + output), gợi ý vá (chỉ là gợi ý);
- bảng đo lại lời khai; điều kiện của B; bảng đột biến của bạn; bảng đối chiếu lớp đặc tả (bốn nhãn); BẢNG SĂN; phán ba câu hỏi của executor; mục "Rủi ro tồn dư đã miễn"; mục KHÔNG ĐO ĐƯỢC.
Approve chỉ khi không còn P0–P2. Dọn thư mục nháp của chính bạn khi xong là được, nhưng giữ `out/`.
