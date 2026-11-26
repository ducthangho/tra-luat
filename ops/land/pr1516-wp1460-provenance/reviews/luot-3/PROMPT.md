# Review mã nguồn wp1460 (B1a, Mission #1172) — lượt 3 (LƯỢT CUỐI), Codex, chỉ đọc

Bạn là REVIEWER độc lập (Codex gpt-6-astra, suy luận cao nhất) cho packet wp1460 của kho ducthangho/tra-luat. Đây là phiên MỚI.
Bạn KHÔNG phải executor. Bạn KHÔNG sửa tệp nào trong `src/`, KHÔNG commit, KHÔNG push, KHÔNG gọi GitHub để ghi.
Trả lời bằng tiếng Việt.

## Thứ được review (định danh là BĂM)
- `src/`: clone của https://github.com/ducthangho/tra-luat, đã fetch mọi nhánh `origin/*`.
- Ứng viên H3 = `d1c28891acec4f861a9f26e092d92b71bd08af9d`, tree `0e44eaf4a22f66d5c04d243f691f252695e64889`, nhánh cục bộ `agent/wp1460-r9-g3-fable` (CHƯA đẩy). Cha H2 = `1c31f5a88ba125af708a9609085c0edd2f8dc3ee` (lượt 2), ông H1 = `4cad0e1c140ced47030b5c2834ae000d9670671f` (lượt 1). Kiểm: `git -C src rev-parse HEAD HEAD^{tree} HEAD^ HEAD^^`.
- Base = `5259239d763c9ffc1677f033bd9a9cf23ede9299`.
- Đặc tả đóng băng r9: `git -C src show 0883d49edc22cf261f471ef71f2dc5f323e8d667:ops/specs/wp1460-r1/SPEC.md`, sha256 phải là `280f6f8d0dc97f29a79ed8ef94d3070d8ae1fe0487b549054137bcdbc4acbb0c`. Đo trước khi đọc. r9 khác r7 chỉ ở dòng revision, đoạn Trạng thái, mục Kích thước (hai khối `nang_tran`) và bảng Thay đổi.
- Lease: `git -C src show origin/ops/wp1460-r1:ops/leases/wp1460-r9-g3-claude.yaml` (trần 6 tệp / 1700 dòng thêm).
- Handoff lượt 5 của executor: `HANDOFF.yaml` (danh sách đường vào của lớp, đường đã an toàn kèm phép đo, bảng đột biến mới).
- Probe nháp của executor (KHÔNG commit, chỉ để tham khảo, đừng nhận kết quả của chúng): `executor-probes/` (`fuzz_a5.py`, `fuzz_b5.py`, `fuzz_c5.py`, `surr.py`, `yaml_boundary_final.py`).
- Verdict và probe của lượt 1: `luot-1/`; của lượt 2: `luot-2/` (probe F02-R2 là `luot-2/yaml_boundary_evidence.py`). Các script viết cho bố cục `src/` như ở đây.
- Script A/B nghiệm thu 5: `ab.sh`.
- Đọc thêm: `src/CLAUDE.md`, `src/AGENTS.md`, `src/docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12, §13.

## Lời khai của executor cần bạn ĐO LẠI
- numstat so base: 4 tệp, +1598/−20 (`ci_dang_ky_test.py` +1316/−20, workflow +87, schema +34, fixture +161). Lượt 5 chỉ đổi `ci_dang_ky_test.py` (+39/−7 so H2).
- `python .claude/dev/ci_dang_ky_test.py`: rc 0, `PHẢN CHỨNG: 1646/1646 đỏ đúng`, `TỔNG: ĐẠT`, ~240 s.
- Đột biến: `ĐỘT BIẾN wp1460: giết đúng lý do 98/98 · tự kiểm phân hạng 6/6 · nền 92/92` (9 dòng mới).
- Nghiệm thu 1 độc lập: 480/480, 249/249, `TONG: DAT`. actionlint rc 0 delta 0; Ruff F (`python3 -m ruff`, 0.15.15) delta 0.
- Probe F02-R2 của lượt 2: trên H3, 64/512/900 tầng đều rc 1 + biên nhận không xanh hợp lệ có lý do X2.
- Bốn đường executor khai đã đóng:
  P1 `yaml.safe_load` trong `job_ky_vong_du`: bắt đúng sáu lớp (RecursionError, KeyError, IndexError, AttributeError, TypeError, OverflowError) quanh RIÊNG lời gọi parser, đổi thành ValueError ⇒ lý do X2; không bắt `Exception` chung.
  P2 tên job không mã hoá được UTF-8 (surrogate) lọt vào hình xanh rồi sập khi ghi ⇒ nay X2.
  P3 `_doc_json_du`: JSON sâu ~9993–9997 tầng parse được rồi jsonschema tràn khi dựng repr ⇒ trần độ sâu 64 không đệ quy ở bộ đọc.
  P4 `lay()` dựng đường dẫn từ tên job có NUL ném ValueError ⇒ nay bắt ⇒ lý do X4.

## Câu hỏi mở của executor, cần bạn phán
1. Danh sách sáu lớp ngoại lệ ở P1: quá rộng (che lỗi lập trình) hay chưa đủ (PyYAML đời sau)? So với lựa chọn khác.
2. P3 thêm luật đầu vào "độ sâu JSON ≤ 64" mà đặc tả không nêu. Có trái đặc tả không: có ca XANH hợp lệ nào theo hợp đồng mà bị hạ đỏ vì luật này không (đo trên hình REST/dấu/mảnh thật mà schema và fixture cho phép)? Phương án thay: bắt RecursionError ở từng bên tiêu dùng đệ quy.
3. P2 và P4 vượt ra ngoài biểu hiện reviewer nêu; executor thêm theo chỉ thị vá theo lớp. Có làm đổi kết luận xanh/đỏ của ca hợp lệ nào không?
4. Ca P2 và P3 đã commit là ca tất định, không tái tạo chính cú sập (tính di động, cửa sổ độ sâu phụ thuộc nền); dưới đột biến chúng đỏ vì lý do đổi. Như thế có đủ "ca có ĐO" không, hay là "ca có MẶT" (bài học trong CLAUDE.md)?

## Việc của bạn
1. **Bảng đối chiếu lượt trước (bắt buộc):** F01, F03, F04 (lượt 2 xếp ĐÃ SỬA ĐÚNG LỚP) và F02/F02-R2 (lượt 2 xếp VÁ HỜ): xếp lại mỗi lớp vào đúng một nhãn `ĐÃ SỬA ĐÚNG LỚP` · `VÁ HỜ` · `CHƯA SỬA` · `KHÔNG ÁP DỤNG` trên H3, kèm bằng chứng CHẠY được. Với F02: tự liệt kê độc lập mọi đường vào của lớp `v1-not-fully-specified` trong đường lệnh thu (`--thu-bien-nhan-audit`) TRƯỚC khi đọc danh sách của executor, rồi đối chiếu; đường thiếu là VÁ HỜ. Đo răng: gỡ RIÊNG từng chốt mới trên bản sao tạm, xác nhận ca đích đỏ đúng `TinHieuChotCa` và đúng tên ca.
2. **Chạy** ca đã commit, bộ đột biến, nghiệm thu 1, A/B, probe của lượt 1 và lượt 2 trên H3; đo lại lời khai.
3. **Hồi quy H2..H3** (`git -C src diff 1c31f5a d1c2889`): có phá điều gì lượt 1–2 đã chấp nhận (bảy lựa chọn của lượt 1; F01, F03, F04) không? Có sinh lớp lỗi mới không (bắt ngoại lệ che lỗi lập trình, trần độ sâu hạ đỏ ca hợp lệ, đổi lý do mà không đổi kết luận)?
4. **Đột biến của riêng bạn** trên bản sao tạm ngoài `src/`; báo SỐNG và GIẾT SAI LÝ DO.
5. **Đầu vào thù địch: chỉ mô tả bằng lời, đừng tự soạn payload tấn công.** Nói đường mã xử lý và ca phủ cho: YAML lồng sâu / thẻ kiểu lạ / bí danh; JSON lồng sâu ở mỗi điểm REST và trong dấu, mảnh; tên job hoặc artifact có ký tự không mã hoá được hoặc NUL; số rất lớn. Chỉ dựng fixture DỮ LIỆU thường để đo, không dựng gì nhằm thoát khỏi cây thư mục.
6. **Lớp nguyên nhân (§8.3)** cho mỗi finding mới, và lớp ấy còn ở đâu khác.
7. **BẢNG SĂN ≥ 6 hướng:** giả thuyết, phép đo, kết quả.
8. Write set: đúng bốn tệp; numstat ≤ 1700; hai tệp hop_dong đúng băm; không có chuỗi đánh dấu bỏ-qua-CI trong tệp hay commit message H1..H3.

## Đầu ra
Ghi TĂNG DẦN vào `out/VERDICT.md`:
- dòng đầu `VERDICT: approve | changes_requested | blocked`;
- `reviewed_sha: d1c28891acec4f861a9f26e092d92b71bd08af9d`, `reviewed_tree: 0e44eaf4a22f66d5c04d243f691f252695e64889`, `spec_sha256: 280f6f8d…`;
- hai trục `Spec` và `Standards/Security`;
- bảng đối chiếu lượt trước (bốn nhãn); bảng finding mới (id, P0–P3, lớp, tệp:dòng, mô tả, bằng chứng chạy được, gợi ý); bảng đo lại lời khai; bảng đột biến của bạn; BẢNG SĂN; phán câu hỏi 1–4; danh sách P3 còn mở (slug kebab-case + severity) nếu có; mục KHÔNG ĐO ĐƯỢC.
Approve chỉ khi không còn P0–P2. Đây là lượt Codex CUỐI theo trần của lease và hết lượt executor; điều đó KHÔNG được làm hạ mức finding — ghi đúng mức. Dọn nháp của chính bạn khi xong, giữ `out/`.
