# Review mã nguồn wp1460 (B1a, Mission #1172) — lượt 4 (LƯỢT CUỐI), Codex, chỉ đọc

Bạn là REVIEWER độc lập (Codex gpt-6-astra, suy luận cao nhất) cho packet wp1460 của kho ducthangho/tra-luat. Đây là phiên MỚI.
Bạn KHÔNG phải executor. Bạn KHÔNG sửa tệp nào trong `src/`, KHÔNG commit, KHÔNG push, KHÔNG gọi GitHub để ghi.
Trả lời bằng tiếng Việt.

## Thứ được review (định danh là BĂM)
- `src/`: clone của https://github.com/ducthangho/tra-luat, đã fetch mọi nhánh `origin/*`.
- Ứng viên H4 = `f5af7469c03e7fe421a3704c731f390842260304`, tree `3f977dc24ae10e4d5007845584469ba3247b9c1d`, nhánh cục bộ `agent/wp1460-r9-g4-fable` (CHƯA đẩy). Chuỗi cha: H3 `d1c28891…` (lượt 3) ← H2 `1c31f5a8…` (lượt 2) ← H1 `4cad0e1c…` (lượt 1). Kiểm: `git -C src rev-parse HEAD HEAD^{tree} HEAD^ HEAD^^ HEAD^^^`.
- Base = `5259239d763c9ffc1677f033bd9a9cf23ede9299`.
- Đặc tả đóng băng r9: `git -C src show 0883d49edc22cf261f471ef71f2dc5f323e8d667:ops/specs/wp1460-r1/SPEC.md`, sha256 phải là `280f6f8d0dc97f29a79ed8ef94d3070d8ae1fe0487b549054137bcdbc4acbb0c`. Đo trước khi đọc.
- Lease: `git -C src show origin/ops/wp1460-r1:ops/leases/wp1460-r9-g4-claude.yaml` (trần 6 tệp / 1700 dòng thêm; khoá `debt` ghi nợ phương án b).
- Quyết định chủ kho cho lượt này: phương án (a) — vá F02-R3 bằng chốt tại TỪNG nơi tiêu dùng đệ quy, KHÔNG phải một biên bắt lỗi ngoài cùng (https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7137001118 và 7137492147). Phương án (b) — revision đặc tả khoanh lời hứa toàn phần — là NỢ, chưa làm.
- Handoff lượt 6: `HANDOFF.yaml` (danh sách nơi tiêu dùng đệ quy kèm phép đo, ca và đột biến mới, câu hỏi mở). Lưu ý: executor khai các cổng chạy lúc 16:46–17:05Z ngày 24-11 trên clone của H4 rồi bị cắt bởi giới hạn API; sau khi tiếp tục KHÔNG chạy lại. Hãy ĐO LẠI tất cả.
- Verdict và probe các lượt trước: `luot-1/`, `luot-2/`, `luot-3/` (probe F02-R3 của lượt 3: `luot-3/depth_contract.py`; probe F02-R2: `luot-2/yaml_boundary_evidence.py`).
- Script A/B nghiệm thu 5: `ab.sh`.
- Đọc thêm: `src/CLAUDE.md`, `src/AGENTS.md`, `src/docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12, §13.

## Lời khai của executor cần bạn ĐO LẠI
- numstat so base: 4 tệp, +1693/−20 (py +1411, workflow +87, schema +34, fixture +161). H3..H4 chỉ đổi `ci_dang_ky_test.py` +119/−24.
- `python .claude/dev/ci_dang_ky_test.py`: rc 0, `PHẢN CHỨNG: 1677/1677 đỏ đúng`, `TỔNG: ĐẠT`, ~267 s. Lượt dưới Python 3.12.13 cũng 1677/1677, nhưng rc và thời gian mất do bị cắt.
- Đột biến: `giết đúng lý do 112/112 · tự kiểm phân hạng 6/6 · nền 105/105`.
- Nghiệm thu 1 độc lập 480/480, 249/249; actionlint rc 0 delta 0; Ruff F delta 0.
- Bản vá: bỏ trần độ sâu 64 trong `_doc_json_du`; `_hop_le_du` bọc `is_valid` của jsonschema ở ba nơi (dấu, biên nhận xanh, biên nhận không xanh), đổi `RecursionError` thành không hợp lệ; `_gt_du` in nguyên văn giá trị đầu vào vào `ly_do` chỉ khi là vô hướng, còn list/dict in `<list>`/`<dict>` (năm nơi).
- Probe lượt 3 (bản chép đã chỉnh): 10 đối chứng của reviewer + 4 ở độ sâu 300 nay xanh như H2; definition measured 5/5; dấu sâu vẫn đỏ 5/5. Probe lượt 3 NGUYÊN BẢN trả rc 1 vì nó khẳng định ứng viên phải đỏ — đó là hành vi mong đợi sau khi sửa; hãy tự xác nhận.
- Ca mới: 5 ca dương (trường không dùng sâu 60/64/70/500 ở run/jobs/artifacts/definition/mảnh) + 5 đột biến trả lại trần; 2 ca quét biên tìm giới hạn parser lúc chạy, chạy lệnh thu ở 43 độ sâu quanh đó, đòi rc 1 + biên nhận hợp lệ và đòi `is_valid` thật sự ném bên trong ít nhất một lần; 1 đột biến chứng minh lượt quét không chạm biên thì ca đỏ.
- Hai ca quét biên và ba dòng đột biến chỉ thêm khi Python < 3.14 (`KHE_1460`), vì trên 3.14.6 không có đầu vào parse được nào làm `is_valid` tràn.

## Câu hỏi cấu trúc (bắt buộc trả lời)
1. **Bản vá có đóng cả LỚP `v1-not-fully-specified` trong đường lệnh thu không, hay còn đường sập nằm ngoài các chốt?** Tự liệt kê độc lập MỌI nơi tiêu dùng đệ quy hoặc có thể ném ngoại lệ bất ngờ trên dữ liệu đầu vào (kể cả `json.dumps` của biên nhận, so sánh, gộp trang, base64, regex, `repr`, ghi tệp, mã hoá), TRƯỚC khi đọc danh sách của executor; đối chiếu; đường thiếu là VÁ HỜ.
2. Tài liệu lồng sâu hơn giới hạn của chính parser JSON (~9994–9997 tầng trên 3.12/3.13) vẫn ĐỎ dù phần sâu là trường không dùng; H2 cũng thế. Executor xếp vào nợ (b). Đây có phải P0–P2 của PR này theo đặc tả r9, hay đúng là ngoài tầm (giống giới hạn tài nguyên), và có đổi kết luận xanh nào mà H2 từng cho không?
3. `KHE_1460` bỏ ca/đột biến trên Python ≥ 3.14 — CI ghim phiên bản nào (đọc `.github/workflows/ci.yml`, job `gate-registry`)? Cổng ấy có thể tự tắt im lặng không?
4. Ca theo văn bản (`_gt_du` năm nơi) và ca biên nhận không xanh dùng schema tự tham chiếu thay vì đầu vào: có là "ca có MẶT" thay vì "ca có ĐO" (CLAUDE.md) không?

## Việc của bạn
1. **Bảng đối chiếu lượt trước (bắt buộc):** F01, F03, F04, F02/F02-R2/F02-R3 — mỗi lớp đúng một nhãn `ĐÃ SỬA ĐÚNG LỚP` · `VÁ HỜ` · `CHƯA SỬA` · `KHÔNG ÁP DỤNG` trên H4, kèm bằng chứng CHẠY được. Đo răng: gỡ RIÊNG từng chốt mới trên bản sao tạm, xác nhận ca đích đỏ đúng `TinHieuChotCa` và đúng tên ca. Ba mutant SỐNG của lượt 3 (`luot-3/VERDICT.md`, bảng đột biến riêng) nay thế nào.
2. **Chạy** ca đã commit, đột biến, nghiệm thu 1, A/B, và probe của lượt 1–3 trên H4; đo lại mọi lời khai.
3. **Hồi quy H3..H4** (`git -C src diff d1c2889 f5af746`): có phá điều gì các lượt trước đã chấp nhận (bảy lựa chọn lượt 1; F01, F03, F04; P1, P2, P4 của lượt 5) không? Đổi `ly_do` sang `<list>`/`<dict>` có đổi kết luận nào không?
4. **Đột biến của riêng bạn** trên bản sao tạm ngoài `src/`; báo SỐNG và GIẾT SAI LÝ DO.
5. **Đầu vào thù địch: chỉ mô tả bằng lời, không tự soạn payload tấn công.** Chỉ dựng fixture DỮ LIỆU thường (JSON/YAML lồng sâu, trường không dùng, tên lạ) để đo; không dựng gì nhằm thoát khỏi cây thư mục.
6. **Lớp nguyên nhân (§8.3)** cho mỗi finding mới, và lớp ấy còn ở đâu khác.
7. **BẢNG SĂN ≥ 6 hướng:** giả thuyết, phép đo, kết quả.
8. Write set: đúng bốn tệp; numstat ≤ 1700; hai tệp hop_dong đúng băm; không có chuỗi đánh dấu bỏ-qua-CI trong tệp hay commit message H1..H4.

## Đầu ra
Ghi TĂNG DẦN vào `out/VERDICT.md`:
- dòng đầu `VERDICT: approve | changes_requested | blocked`;
- `reviewed_sha: f5af7469c03e7fe421a3704c731f390842260304`, `reviewed_tree: 3f977dc24ae10e4d5007845584469ba3247b9c1d`, `spec_sha256: 280f6f8d…`;
- hai trục `Spec` và `Standards/Security`;
- bảng đối chiếu lượt trước; bảng finding mới (id, P0–P3, lớp, tệp:dòng, mô tả, bằng chứng chạy được, gợi ý); bảng đo lại lời khai; bảng đột biến của bạn; BẢNG SĂN; trả lời câu hỏi cấu trúc 1–4; danh sách P3 còn mở dạng `{slug kebab-case, severity}`; mục KHÔNG ĐO ĐƯỢC.
Approve chỉ khi không còn P0–P2. Đây là lượt Codex CUỐI và lượt executor đã hết; điều đó KHÔNG được làm hạ mức finding. Dọn nháp của chính bạn khi xong, giữ `out/`.
