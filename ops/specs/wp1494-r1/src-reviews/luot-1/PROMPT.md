# Review mã nguồn wp1494 (B2, Mission #1172) — lượt 1, Codex, chỉ đọc

Bạn là REVIEWER độc lập (Codex gpt-6-astra, suy luận cao nhất) cho packet wp1494 của kho ducthangho/tra-luat.
Bạn KHÔNG phải executor. Bạn KHÔNG sửa tệp nào trong `src/`, KHÔNG commit, KHÔNG push, KHÔNG gọi GitHub để ghi, KHÔNG dispatch workflow.
Trả lời bằng tiếng Việt.

## Thứ được review (định danh là BĂM, không phải tên nhánh)
- Thư mục làm việc: `src/` (clone của https://github.com/ducthangho/tra-luat, đã fetch mọi nhánh `origin/*`, không shallow).
- Ứng viên H = `127b82a8a9e41fda3c4a230810118f0bedfb200d`, tree `862746ce6dae133012b0cfce90bf4913c8784c41`, nhánh cục bộ `agent/wp1494-r5-g2-fable` (CHƯA đẩy lên GitHub). Kiểm: `git -C src rev-parse HEAD HEAD^{tree}`.
- B (base) = `b4b79bf0cd301bb067a22c5245505d9a8ab232cb` (merge PR #1516 của B1a).
- Đặc tả đóng băng: `git -C src show a819291bb08af5e72cdd833b86544ea48d97b1fd:ops/specs/wp1494-r1/SPEC.md`, sha256 phải là `345520e199ba7072c2bea92b876a3db1877cabce7969f82a379bb078d1dc2e4d` (nhánh `origin/ops/wp1494-r1`, revision 5 = r4 cộng khối `nang_tran`). Đo băm trước khi đọc. Đọc TOÀN BỘ đặc tả, kể cả GHIM-B1A, bảng kết cục mục 3, bảng đột biến, mục "Baseline nghiệm thu".
- Lease: `git -C src show origin/ops/wp1494-r1:ops/leases/wp1494-r5-g2-claude-20261125.yaml` (trần 6 tệp / 3500 dòng thêm theo `nang_tran`).
- Tham số thi công Mission r109: `git -C src show 2e70d3b3dada5babd17e6c5e83f8c2b16cacc874:ops/specs/wp1172-source-plan-r4/MCR-1172-r109.md` (B, `ISSUE_THEO_DOI` = 1520, `KHUNG_DAU` = `2026-11-28T19:17:00Z`).
- Handoff của executor: `HANDOFF.yaml` (thư mục hiện tại; sha256 `c937ae597935a9db399f38f35309e98907ab3966226f69835d48b49084b39d9f`), có bảng 207 đột biến.
- Đọc thêm: `src/CLAUDE.md`, `src/AGENTS.md`, `src/docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12.

## Điều kiện của B — đo lại TRƯỚC khi review (đặc tả bắt reviewer tự đo; lệch ⇒ ghi `blocked`)
Đủ mọi điều của mục "Baseline nghiệm thu": B trên first-parent của `origin/master`; hai tệp `hop_dong` tại B bằng GHIM-B1A; `KHUNG_DAU` bằng `khung_cron` của thời điểm committer của B; job `bien-nhan-audit` và bước tải lên tại B; ba tệp mới vắng và 0 mục `canh_tuoi_audit_test` tại B. Kiểm thêm băm khối "Lệnh kiểm" (`d9c78e70…`) trên `d1b08c219227d4b8925702029cd20d4e0febed54:ops/specs/wp1460-r1/SPEC.md`, và bốn hàm chép nguyên văn (`tieu_dung`, `khoa_tu_ten`, `doc_moc`, `khung_cron`) trong `ops/canh_tuoi_audit.py` trùng byte khối ấy.

## Lời khai của executor cần bạn ĐO LẠI (đừng nhận lời)
- numstat `git diff --numstat B H`: 4 tệp, +2873/−0 (`ci_dang_ky_test.py` +1, workflow +29, `ops/canh_tuoi_audit.py` +1000, test +1843).
- `python3 ops/canh_tuoi_audit_test.py` → rc 0; `CA: 320/320 dat` · `DOT BIEN: 207/207 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (5 dot bien)` · `TONG: DAT` (~70 s). Có cờ `--chi-tiet`.
- `python3 .claude/dev/ci_dang_ky_test.py` → rc 0, `PHẢN CHỨNG: 1677/1677 đỏ đúng`, `TỔNG: ĐẠT` (~4–5 phút; tại B 32/32 đăng ký).
- actionlint 1.7.7 + shellcheck: rc 0. Ruff F (`python3 -m ruff`, 0.15.15) delta 0.
Đặt `git config core.abbrev 7` trong mọi bản sao bạn dựng. Ghi lệnh, rc và dòng dương THẬT bạn đo.

## Các lựa chọn executor tự quyết, cần bạn phán theo đặc tả
1. Dòng 134 của bảng đột biến: quan sát khai trong đặc tả không dựng được (schema ghim từ chối mọi biên nhận `ok: false` mang `job`/`manh`); đột biến vẫn bị giết, nhưng bằng quan sát khác (KeyError bị lưới an toàn bắt). Đúng hay là một lỗ đo?
2. Dòng 61: 23 đột biến phủ 32 điều kiện (một số đột biến dùng chung mã, chạy trên hai ca đích). Đặc tả ghi ×32.
3. Đột biến của hàm dùng chung theo luật nơi gọi: LIÊN KẾT (dòng 1–3), dòng 7 và 69 gộp một đột biến bộ phân trang, dòng 96 và 107 mỗi dòng một đột biến, dòng 108 và 109 chạy trên cả ca T2 lẫn T5.
4. Hai đột biến thêm ngoài dòng 82 (giá trị `name`, không đồng thời có cả khoá `True` và `"on"`); khoá YAML trùng: bộ kiểm hình `yaml.safe_load` mù với khoá trùng (đo: `run:` thứ hai ở bước 4 cho cấu trúc bằng tệp thật, actionlint từ chối rc 1) — executor không thêm chốt ngoài đặc tả.
5. Lần thử hết giờ mã hoá `transport_nem:builtins.TimeoutError` (đặc tả cấm so lớp ngoại lệ); `het_gio` chỉ dùng khi cạn hạn của pha.
6. `thong_bao_hoan` chỉ ghi khi luật đòi một sự kiện khác sự kiện đang chờ.
7. T7 là `khong_danh_gia` khi D2 đọc đầu hỏng.
8. Nghiệm thu 3 tại B in `khoi_ma khong_co_trong_cay` (tệp đặc tả B1a không có trong cây tại B), nên bộ test không khoá được bản chép nguyên văn. Chấp nhận được theo đặc tả hay thiếu?
9. `transport_that()` và `main()` (urllib thật, step summary, báo cáo stdout) KHÔNG có ca nào chạy. Soi kỹ: I4 (token chỉ gửi tới `api.github.com`, không gửi `Authorization` tới host của lời chuyển hướng), lớp J/R/S, đọc theo khúc và trần `TRAN_GOI`, mã thoát mục 9.

## Việc của bạn
1. **CHẠY** các ca đã commit và bộ đột biến; đo lại mọi lời khai ở trên.
2. **ĐỘT BIẾN BẢN VÁ** trên một bản sao TẠM ngoài `src/` (vd `cp -r src <nháp>/dot`): gỡ hoặc nới từng chốt quan trọng (bốn trạng thái và chiều một chiều của I2; nghĩa vụ khung cũ; LIÊN KẾT D1↔D2; hạn tuyệt đối kiểm cả lúc HOÀN TẤT; cạn tất-cả-hoặc-không; PATCH/POST đúng một lần gửi vật lý; bất biến "đang chờ không bao giờ bị xoá"; đối soát D14; bộ kiểm miền nhịp tim dùng chung người ghi/người đọc; trần giải nén; bộ kiểm hình workflow mục 8). Đo ca nào đỏ. Một đột biến chỉ tính là GIẾT khi ca ĐÍCH đỏ vì đúng lý do (`TinHieuChotCa` của chính ca ấy). Báo đột biến SỐNG và GIẾT SAI LÝ DO. Ưu tiên chỗ bảng đột biến của executor KHÔNG phủ.
3. **Đầu vào thù địch — chỉ mô tả bằng lời, đừng tự soạn payload tấn công.** Với mỗi hướng, nói đường mã nào xử lý nó và ca đã commit nào phủ nó; chỉ dựng fixture DỮ LIỆU thường (JSON REST giả, zip giả bình thường) để đo, không dựng gì nhằm thoát khỏi cây thư mục:
   - phân trang lặp/thiếu/đổi thứ tự, `total_count` nói dối, `created_at` sai dạng hoặc không có thật;
   - lượt bị chạy lại attempt, lượt `workflow_dispatch` lẫn vào, `head_sha` đổi giữa hai lần đọc D2;
   - comment giả dòng `B2_SU_KIEN` từ người không phải `github-actions[bot]`; thân Issue bị người sửa tay; nhịp tim cũ/hỏng/vắng;
   - phản hồi thiếu `X-GitHub-Request-Id`, chuyển hướng sang http hoặc host lạ, `Content-Length` nói dối, gói zip có nhiều mục hay tổng giải nén lớn;
   - đồng hồ đơn điệu chạm đúng hạn (biên chặt), POST hoàn tất sau hạn;
   - workflow `canh-tuoi-audit.yml` bị thêm khoá/bước/quyền.
4. **Lớp nguyên nhân (§8.3):** mỗi finding gắn một lớp nguyên nhân (slug kebab-case) và trả lời: lớp ấy còn ở chỗ nào khác trong bản vá không? Tìm theo LỚP, không dừng ở trường hợp đầu tiên.
5. **Bảng đối chiếu lớp đặc tả:** đây là lượt review MÃ NGUỒN đầu tiên của packet (bốn lượt trước là review ĐẶC TẢ: `origin/ops/wp1494-r1:ops/specs/wp1494-r1/reviews/` nếu có, và bảng "Thay đổi" của đặc tả). Lấy các lớp đã nêu ở review đặc tả lượt 1–3 (`notification-dedup-before-delivery`, `mutant-oracles-non-discriminating`, `consumer-freshness-anchor-unverified`, `bounded-evaluation-order-dependent`, `heartbeat-value-domain-incomplete`, `unbounded-artifact-expansion`…) và xếp mỗi lớp vào đúng một trong bốn nhãn khi áp vào MÃ: `ĐÃ SỬA ĐÚNG LỚP` · `VÁ HỜ` · `CHƯA SỬA` · `KHÔNG ÁP DỤNG`, kèm bằng chứng đo.
6. **BẢNG SĂN ≥ 6 hướng:** liệt kê ít nhất sáu hướng bạn đã chủ động săn (kể cả hướng không ra gì), mỗi hướng: giả thuyết, phép đo đã chạy, kết quả.
7. Kiểm write set: đúng bốn tệp, `ci_dang_ky_test.py` chỉ thêm đúng một mục MOI nguyên văn đặc tả; không có chuỗi đánh dấu bỏ-qua-CI trong tệp hay commit message.

## Đầu ra
Ghi TĂNG DẦN (sau mỗi phần xong) vào `out/VERDICT.md` trong thư mục hiện tại, gồm:
- dòng đầu: `VERDICT: approve | changes_requested | blocked` (cập nhật khi xong);
- `reviewed_sha: 127b82a8a9e41fda3c4a230810118f0bedfb200d`, `reviewed_tree: 862746ce6dae133012b0cfce90bf4913c8784c41`, `spec_sha256: 345520e1…`;
- hai trục `Spec` và `Standards/Security`;
- bảng finding: id, severity P0–P3, lớp nguyên nhân, tệp:dòng, mô tả, bằng chứng chạy được (lệnh + output), gợi ý vá (chỉ là gợi ý);
- bảng đo lại lời khai; điều kiện của B; bảng đột biến của bạn; bảng đối chiếu lớp đặc tả (bốn nhãn); BẢNG SĂN; phán từng lựa chọn 1–9; mục KHÔNG ĐO ĐƯỢC.
Approve chỉ khi không còn P0–P2. Dọn thư mục nháp của chính bạn khi xong là được, nhưng giữ `out/`.
