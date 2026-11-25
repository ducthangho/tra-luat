# Review mã nguồn wp1460 (B1a, Mission #1172) — lượt 2, Codex, chỉ đọc

Bạn là REVIEWER độc lập (Codex gpt-6-astra, suy luận cao nhất) cho packet wp1460 của kho ducthangho/tra-luat. Đây là phiên MỚI, không phải phiên lượt 1.
Bạn KHÔNG phải executor. Bạn KHÔNG sửa tệp nào trong `src/`, KHÔNG commit, KHÔNG push, KHÔNG gọi GitHub để ghi.
Trả lời bằng tiếng Việt.

## Thứ được review (định danh là BĂM, không phải tên nhánh)
- Thư mục làm việc: `src/` (clone của https://github.com/ducthangho/tra-luat, đã fetch mọi nhánh `origin/*`).
- Ứng viên H2 = `1c31f5a88ba125af708a9609085c0edd2f8dc3ee`, tree `d316445a44465cd563ce72b64a65b4893e63ad0c`, nhánh cục bộ `agent/wp1460-r8-g2-fable` (CHƯA đẩy). Cha của nó là H1 = `4cad0e1c140ced47030b5c2834ae000d9670671f` (ứng viên lượt 1). Kiểm: `git -C src rev-parse HEAD HEAD^{tree} HEAD^`.
- Base = `5259239d763c9ffc1677f033bd9a9cf23ede9299`.
- Đặc tả đóng băng: `git -C src show d26c8ae8d27a0bddd71bbd08a5153bb47b879130:ops/specs/wp1460-r1/SPEC.md`, sha256 phải là `33d433b018d6eb74048fe27f2cc517b01276a28b76edbe50ffea387a0614dd0c`. Đo trước khi đọc.
- Lease: `git -C src show origin/ops/wp1460-r1:ops/leases/wp1460-r8-g2-claude.yaml` (trần 6 tệp / 1600 dòng thêm).
- Handoff lượt 4 của executor: `HANDOFF.yaml` (danh sách đường vào theo từng lớp, bảng đột biến 95 dòng, cổng).
- Verdict lượt 1 và toàn bộ probe của reviewer lượt 1: `luot-1/` (`VERDICT.md`, `review_probe.py`, `hash_evidence.py`, `reviewer_mutants.py`, `class_evidence.py`, `structure_checks.py`, `REPRODUCE.md`…). Các script ấy viết cho bố cục `src/` y như ở đây.
- Script A/B nghiệm thu 5: `ab.sh`.
- Đọc thêm: `src/CLAUDE.md`, `src/AGENTS.md`, `src/docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12, §13.

## Lời khai của executor cần bạn ĐO LẠI
- numstat so base: 4 tệp, +1566/−20 (`ci_dang_ky_test.py` +1284/−20, workflow +87, schema +34, fixture +161; hai tệp hop_dong trùng byte `844b5218…`, `ce859573…`).
- `python .claude/dev/ci_dang_ky_test.py`: rc 0, `PHẢN CHỨNG: 1619/1619`, `TỔNG: ĐẠT`, ~221 s (base 1226/1226).
- Đột biến wp1460: `giết đúng lý do 89/89 · tự kiểm phân hạng 6/6 · nền 83/83`.
- Nghiệm thu 1 độc lập: 480/480, 249/249, `TONG: DAT`. A/B 32/32; A/B fixture đã commit 68/68.
- actionlint 1.7.7 + shellcheck 0.9.0 rc 0, 0 finding; Ruff F (`python3 -m ruff`, 0.15.15) rc 0, delta 0.
- Probe lượt 1 chạy lại trên H2: `reviewer_mutants.py` 40 GIẾT + 1 tự kiểm (lượt 1: 37 + 3 SỐNG); bốn probe JSON+`.loi`, hai năm biên, hai ref có nháy đều cho kết quả đúng.
Đặt `git config core.abbrev 7` trong mọi bản sao bạn dựng.

## Câu hỏi mở của executor, cần bạn phán
1. Bước 2 "đo HEAD" của job thu (hình PR0 ghim) vẫn nội suy `github.sha` / `run_id` / `run_attempt` vào thân shell. Executor giữ nguyên vì miền hex/số và vì đổi nó là đổi hình PR0. Có cùng lớp với F03 không, có phải P0–P2 không?
2. Năm < 1000 trên glibc nay ra không xanh thay vì tự đệm năm, vì oracle tiêu dùng đóng băng tính lại bằng cùng `strftime`. Bản thân oracle đóng băng vẫn tràn ở năm 0001; executor không đụng (cấm sửa). Phán: đúng hướng không; phần oracle có phải finding của PR này không, hay nợ đặc tả?
3. `jobs[].run_id` vẫn chưa đối chiếu chéo (lượt 1 ghi chú, không phải finding).
4. Executor tự thêm bốn đường sập cùng lớp F02 (JSON lồng sâu → `RecursionError`, giá trị ma trận > 4300 chữ số, attempt > 4300 chữ số trong tên artifact REST, đối số không mã hoá được UTF-8 → thoát 2). Kiểm từng đường và xem còn đường nào cùng lớp chưa đóng.

## Việc của bạn
1. **Bảng đối chiếu lượt trước (bắt buộc):** với F01, F02, F03, F04 của `luot-1/VERDICT.md`, xếp mỗi lớp vào đúng một nhãn — `ĐÃ SỬA ĐÚNG LỚP` · `VÁ HỜ` · `CHƯA SỬA` · `KHÔNG ÁP DỤNG` — kèm bằng chứng CHẠY được trên H2. Với mỗi lớp, đối chiếu danh sách đường vào executor khai trong handoff với danh sách BẠN tự liệt kê độc lập trước khi đọc của họ; đường nào thiếu là VÁ HỜ. Đo răng từng chốt: gỡ RIÊNG từng chốt (mỗi đường một chốt) trên bản sao tạm và xác nhận ca đích đỏ đúng lý do (lớp `TinHieuChotCa` và đúng tên ca), không phải `AttributeError`/`KeyError`/`TypeError` hay ca khác.
2. **Chạy** các ca đã commit và bộ đột biến của bản vá; đo lại lời khai ở trên; chạy lại probe của lượt 1 trên H2 và đối chiếu với kết quả lượt 1.
3. **Hồi quy do bản vá:** diff H1..H2 (`git -C src diff 4cad0e1 1c31f5a`) có làm hỏng điều gì lượt 1 đã chấp nhận (lựa chọn 1–7; các lớp đặc tả `ĐÃ SỬA ĐÚNG LỚP`) không? Bản vá có thêm lớp lỗi mới không (vd bộ đọc REST chung nuốt lỗi khác, kiểm schema hai hình đổi kết luận xanh/đỏ sai, `env:` thiếu giá trị hoặc sai tên)?
4. **Đột biến của riêng bạn** trên bản sao tạm ngoài `src/` cho các chốt mới; báo SỐNG và GIẾT SAI LÝ DO.
5. **Đầu vào thù địch — chỉ mô tả bằng lời, đừng tự soạn payload tấn công.** Với mỗi hướng sau, nói đường mã nào xử lý và ca nào phủ; chỉ dựng fixture DỮ LIỆU thường để đo, không dựng gì nhằm thoát khỏi cây thư mục: giá trị context có ký tự cần quote đi qua `env:`; tệp `.loi` rỗng hoặc không đọc được cạnh JSON tốt; JSON REST cực lớn hoặc lồng sâu; mốc thời gian ở biên lịch; số attempt hoặc chỉ số mảnh rất lớn; byte workflow REST khác tệp checkout.
6. **Lớp nguyên nhân (§8.3)** cho mỗi finding mới, và trả lời lớp ấy còn ở đâu khác.
7. **BẢNG SĂN ≥ 6 hướng:** giả thuyết, phép đo, kết quả (kể cả hướng không ra gì).
8. Kiểm write set: đúng bốn tệp; numstat ≤ 1600; không có chuỗi đánh dấu bỏ-qua-CI trong tệp hay commit message H1, H2.

## Đầu ra
Ghi TĂNG DẦN vào `out/VERDICT.md`:
- dòng đầu `VERDICT: approve | changes_requested | blocked`;
- `reviewed_sha: 1c31f5a88ba125af708a9609085c0edd2f8dc3ee`, `reviewed_tree: d316445a44465cd563ce72b64a65b4893e63ad0c`, `spec_sha256: 33d433b0…`;
- hai trục `Spec` và `Standards/Security`;
- bảng đối chiếu lượt 1 (bốn nhãn); bảng finding mới (id, P0–P3, lớp, tệp:dòng, mô tả, bằng chứng chạy được, gợi ý); bảng đo lại lời khai; bảng đột biến của bạn; BẢNG SĂN; phán câu hỏi 1–4; mục KHÔNG ĐO ĐƯỢC.
Approve chỉ khi không còn P0–P2. Lưu ý cho kết luận: lease đã dùng HẾT lượt executor (4/4), và numstat còn ~34 dòng tới trần; đừng vì thế mà hạ mức finding — chỉ ghi đúng mức. Dọn nháp của chính bạn khi xong, giữ `out/`.
