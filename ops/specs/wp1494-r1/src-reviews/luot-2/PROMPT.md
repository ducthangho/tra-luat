# Review mã nguồn wp1494 (B2, Mission #1172) — lượt 2, Codex, chỉ đọc

Bạn là REVIEWER độc lập (Codex gpt-6-astra, suy luận cao nhất) cho packet wp1494 của kho ducthangho/tra-luat.
Bạn KHÔNG phải executor. Bạn KHÔNG sửa tệp nào trong `src/`, KHÔNG commit, KHÔNG push, KHÔNG gọi GitHub để ghi, KHÔNG dispatch workflow.
Trả lời bằng tiếng Việt.

## Thứ được review (định danh là BĂM, không phải tên nhánh)
- Thư mục làm việc: `src/` (clone của https://github.com/ducthangho/tra-luat, đã fetch mọi nhánh `origin/*`, không shallow).
- Ứng viên H = `d3bcd6a171644b18d9fd37a185cfb8fc6d641ef4`, tree `7176af1b194328a9e8f1c73619f88abe1bd11fe0`, nhánh cục bộ `agent/wp1494-r5-g2-fable` (CHƯA đẩy lên GitHub). Kiểm: `git -C src rev-parse HEAD HEAD^{tree}`.
- B (base) = `b4b79bf0cd301bb067a22c5245505d9a8ab232cb` (merge PR #1516 của B1a).
- Đặc tả đóng băng: `git -C src show a819291bb08af5e72cdd833b86544ea48d97b1fd:ops/specs/wp1494-r1/SPEC.md`, sha256 phải là `345520e199ba7072c2bea92b876a3db1877cabce7969f82a379bb078d1dc2e4d` (nhánh `origin/ops/wp1494-r1`, revision 5 = r4 cộng khối `nang_tran`). Đo băm trước khi đọc. Đọc TOÀN BỘ đặc tả, kể cả GHIM-B1A, bảng kết cục mục 3, bảng đột biến, mục "Baseline nghiệm thu".
- Lease: `git -C src show origin/ops/wp1494-r1:ops/leases/wp1494-r5-g2-claude-20261125.yaml` (trần 6 tệp / 3500 dòng thêm theo `nang_tran`).
- Tham số thi công Mission r109: `git -C src show 2e70d3b3dada5babd17e6c5e83f8c2b16cacc874:ops/specs/wp1172-source-plan-r4/MCR-1172-r109.md` (B, `ISSUE_THEO_DOI` = 1520, `KHUNG_DAU` = `2026-11-28T19:17:00Z`).
- Handoff của executor: `HANDOFF.yaml` (thư mục hiện tại; sha256 `bac31736440412c589bed469e17cca8b5795e8251d0c5d37cf868bf0a6600a44`), có bảng vá theo finding và bảng 229 đột biến.
- Verdict lượt 1 (trên H1 = `127b82a8a9e41fda3c4a230810118f0bedfb200d`): `review-1/VERDICT.md` và probe của nó ở `review-1/evidence/` (thư mục hiện tại); bản đã commit ở `origin/ops/wp1494-r1:ops/specs/wp1494-r1/src-reviews/luot-1/`.
- Quyết định chủ kho sau lượt 1: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7157619068 — executor dùng lượt cuối 3/3 vá theo lớp; MIỄN quan sát dòng đột biến 134 (bất khả theo schema ghim), đột biến 134 ghi «tương đương theo schema», ngoài mẫu số, không tín dụng. Không có spec r6; mọi dòng khác giữ yêu cầu.
- Đọc thêm: `src/CLAUDE.md`, `src/AGENTS.md`, `src/docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12.

## Điều kiện của B — đo lại TRƯỚC khi review (đặc tả bắt reviewer tự đo; lệch ⇒ ghi `blocked`)
Đủ mọi điều của mục "Baseline nghiệm thu": B trên first-parent của `origin/master`; hai tệp `hop_dong` tại B bằng GHIM-B1A; `KHUNG_DAU` bằng `khung_cron` của thời điểm committer của B; job `bien-nhan-audit` và bước tải lên tại B; ba tệp mới vắng và 0 mục `canh_tuoi_audit_test` tại B. Kiểm thêm băm khối "Lệnh kiểm" (`d9c78e70…`) trên `d1b08c219227d4b8925702029cd20d4e0febed54:ops/specs/wp1460-r1/SPEC.md`, và bốn hàm chép nguyên văn (`tieu_dung`, `khoa_tu_ten`, `doc_moc`, `khung_cron`) trong `ops/canh_tuoi_audit.py` trùng byte khối ấy.

## Lời khai của executor cần bạn ĐO LẠI (đừng nhận lời)
- numstat `git diff --numstat B H`: 4 tệp, +3098/−0 (`ci_dang_ky_test.py` +1, workflow +29, `ops/canh_tuoi_audit.py` +1019, test +2049); diff H1..H chỉ ở hai tệp `ops/canh_tuoi_audit*.py`.
- `python3 ops/canh_tuoi_audit_test.py` → rc 0; `CA: 357/357 dat` · `DOT BIEN: 229/229 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (5 dot bien)` · `TONG: DAT`.
- `python3 .claude/dev/ci_dang_ky_test.py` → rc 0, `PHẢN CHỨNG: 1677/1677 đỏ đúng`, `TỔNG: ĐẠT`. actionlint rc 0; ruff F delta 0.
- Chạy lại script của reviewer lượt 1 trên H: `reviewer_probes.py` rc 1 nguyên bản (`TypeError: len(None)` vì lần thử quá hạn nay không trả byte; thêm một chốt `len(None)` thì rc 0, năm probe T1 cho `rest_sai_hinh`, `late_final_calculation` cho `het_ngan_sach_danh_gia`); `additional_probes.py` rc 0 (thiếu `body` ở W0/W3/W8 ⇒ thoát 3 kèm báo cáo); `reviewer_mutations.py` rc 0 nhưng R23, R24, R25, R27, R28 vẫn SỐNG trên ca ĐÍCH GỐC của reviewer (executor nói các ca ấy không chạm được chốt); `run_survivors.py` rc 0, mỗi đột biến trong năm cái chết đúng một ca — ca đích MỚI dành riêng; `oracle_audit.py` rc 1 vì tra `d134` đã rời bảng.
Đặt `git config core.abbrev 7` trong mọi bản sao bạn dựng. Ghi lệnh, rc và dòng dương THẬT bạn đo.

## Câu hỏi executor để lại cho bạn
1. Hai sửa một dòng vào script của reviewer (chốt `len(None)`; bỏ tên `d134`) có chấp nhận được làm bằng chứng không?
2. R23–R25, R27, R28 bị giết bởi ca đích MỚI dành riêng chứ không bởi ca đích gốc của reviewer — có thoả "giết bởi chính ca đích" không, hay ca gốc của bạn chỉ ra một đường chưa đóng?
3. 23 đột biến dòng 61 chỉ chạy trên ca người đọc (W0); người ghi không sinh được nhịp tim ngoài miền nên không có ca phía người ghi cho từng điều kiện.

## Việc của bạn
1. **CHẠY** các ca đã commit và bộ đột biến; đo lại mọi lời khai ở trên.
2. **ĐỘT BIẾN BẢN VÁ** trên một bản sao TẠM ngoài `src/` (vd `cp -r src <nháp>/dot`): gỡ hoặc nới từng chốt quan trọng (bốn trạng thái và chiều một chiều của I2; nghĩa vụ khung cũ; LIÊN KẾT D1↔D2; hạn tuyệt đối kiểm cả lúc HOÀN TẤT; cạn tất-cả-hoặc-không; PATCH/POST đúng một lần gửi vật lý; bất biến "đang chờ không bao giờ bị xoá"; đối soát D14; bộ kiểm miền nhịp tim dùng chung người ghi/người đọc; trần giải nén; bộ kiểm hình workflow mục 8). Đo ca nào đỏ. Một đột biến chỉ tính là GIẾT khi ca ĐÍCH đỏ vì đúng lý do (`TinHieuChotCa` của chính ca ấy). Báo đột biến SỐNG và GIẾT SAI LÝ DO. Ưu tiên chỗ bảng đột biến của executor KHÔNG phủ, nhất là mã MỚI giữa H1 và H.
3. **Đầu vào thù địch — chỉ mô tả bằng lời, đừng tự soạn payload tấn công.** Với mỗi hướng, nói đường mã nào xử lý nó và ca đã commit nào phủ nó; chỉ dựng fixture DỮ LIỆU thường (JSON REST giả, zip giả bình thường) để đo, không dựng gì nhằm thoát khỏi cây thư mục:
   - phân trang lặp/thiếu/đổi thứ tự, `total_count` nói dối, `created_at` sai dạng hoặc không có thật;
   - lượt bị chạy lại attempt, lượt `workflow_dispatch` lẫn vào, `head_sha` đổi giữa hai lần đọc D2;
   - comment giả dòng `B2_SU_KIEN` từ người không phải `github-actions[bot]`; thân Issue bị người sửa tay; nhịp tim cũ/hỏng/vắng;
   - phản hồi thiếu `X-GitHub-Request-Id`, chuyển hướng sang http hoặc host lạ, `Content-Length` nói dối, gói zip có nhiều mục hay tổng giải nén lớn;
   - đồng hồ đơn điệu chạm đúng hạn (biên chặt), POST hoàn tất sau hạn;
   - workflow `canh-tuoi-audit.yml` bị thêm khoá/bước/quyền.
4. **Lớp nguyên nhân (§8.3):** mỗi finding gắn một lớp nguyên nhân (slug kebab-case) và trả lời: lớp ấy còn ở chỗ nào khác trong bản vá không? Tìm theo LỚP, không dừng ở trường hợp đầu tiên.
5. **Bảng đối chiếu lượt trước (BẮT BUỘC):** với từng finding F01, F02, F03 của lượt 1, xếp đúng một nhãn `ĐÃ SỬA ĐÚNG LỚP` · `VÁ HỜ` · `CHƯA SỬA` · `VÁ SINH LỖI MỚI`, kèm phép đo. Săn LỚP: liệt kê mọi đường của mỗi lớp trong toàn bản vá (không chỉ chỗ lượt 1 chỉ), và nói đường nào còn hở. Cũng xếp lại các lớp đặc tả dưới đây.
5b. **Bảng đối chiếu lớp đặc tả:** đây là lượt review MÃ NGUỒN đầu tiên của packet (bốn lượt trước là review ĐẶC TẢ: `origin/ops/wp1494-r1:ops/specs/wp1494-r1/reviews/` nếu có, và bảng "Thay đổi" của đặc tả). Lấy các lớp đã nêu ở review đặc tả lượt 1–3 (`notification-dedup-before-delivery`, `mutant-oracles-non-discriminating`, `consumer-freshness-anchor-unverified`, `bounded-evaluation-order-dependent`, `heartbeat-value-domain-incomplete`, `unbounded-artifact-expansion`…) và xếp mỗi lớp vào đúng một trong bốn nhãn khi áp vào MÃ: `ĐÃ SỬA ĐÚNG LỚP` · `VÁ HỜ` · `CHƯA SỬA` · `KHÔNG ÁP DỤNG`, kèm bằng chứng đo.
6. **BẢNG SĂN ≥ 6 hướng:** liệt kê ít nhất sáu hướng bạn đã chủ động săn (kể cả hướng không ra gì), mỗi hướng: giả thuyết, phép đo đã chạy, kết quả.
7. Kiểm write set: đúng bốn tệp, `ci_dang_ky_test.py` chỉ thêm đúng một mục MOI nguyên văn đặc tả; không có chuỗi đánh dấu bỏ-qua-CI trong tệp hay commit message.

## Đầu ra
Ghi TĂNG DẦN (sau mỗi phần xong) vào `out/VERDICT.md` trong thư mục hiện tại, gồm:
- dòng đầu: `VERDICT: approve | changes_requested | blocked` (cập nhật khi xong);
- `reviewed_sha: d3bcd6a171644b18d9fd37a185cfb8fc6d641ef4`, `reviewed_tree: 7176af1b194328a9e8f1c73619f88abe1bd11fe0`, `spec_sha256: 345520e1…`;
- hai trục `Spec` và `Standards/Security`;
- bảng finding: id, severity P0–P3, lớp nguyên nhân, tệp:dòng, mô tả, bằng chứng chạy được (lệnh + output), gợi ý vá (chỉ là gợi ý);
- bảng đo lại lời khai; điều kiện của B; bảng đột biến của bạn; bảng đối chiếu lớp đặc tả (bốn nhãn); BẢNG SĂN; phán từng lựa chọn 1–9 của lượt 1 còn mở và ba câu hỏi của executor; mục KHÔNG ĐO ĐƯỢC.
Approve chỉ khi không còn P0–P2. Dọn thư mục nháp của chính bạn khi xong là được, nhưng giữ `out/`.
