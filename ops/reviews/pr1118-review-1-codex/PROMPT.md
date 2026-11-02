# Cross-review lượt 1 PR #1118 — ops/land: ghi sổ bổ sung #1065 — reviewer: codex

## Đối tượng
- `reviewed_sha`: `b13d3ef93724d249b3db6eeef6d3fe43a61b08f9` (nhánh `ccr-5249948c-9epnbs`, PR #1118, nháp). Cây đầy đủ, KHÔNG shallow, ở `cay-kho/`
  (HEAD detached, `core.abbrev=7`; remote `origin` chỉ để định danh — KHÔNG fetch); `refs/remotes/origin/master` = `180039c` (master lúc dựng sandbox), merge-base = `3bdd987`.
- Diff so merge-base: `diff.patch` / `numstat.txt` — CHỈ `ops/land/pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml` và thư mục
  `ops/land/pr1065-vm-cap-nhat-cong-cu-provenance/` (6 tệp `readback-*` mới + `SHA256SUMS.txt`). Không đụng mã.
- Bối cảnh: PR #1065 (script ops/vm) merge `3dfb973`; hồ sơ land ghi `landed: true` qua PR #1111 (merge `4397ee6`, head `f783bee`).
  PR #1118 bổ sung những gì #1111 không tự ghi được: merge commit của chính #1111, gate hậu merge (`41285898441` bị huỷ,
  `41290009265` trên `3bdd987` 23/23), và cập nhật mục `van_hanh_tren_vm` sau PR #1091 (nhãn thuat_lai).
- Quy tắc: `docs/PROTOCOL_DA_PHIEN.md` (§7, §10.2.2, §13.1), cổng `ops/land_evidence_nguon.py`, khuôn các tệp `ops/land/*-land-evidence.yaml` khác.
  Bài học kho ở `CLAUDE.md` (đặc biệt: "kiểm SỐ HẠNG, đừng kiểm quan hệ", "khai rộng hơn phép đo", "chưa hết hạn ≠ còn hiệu lực").

## Năng lực đo bạn CÓ
- `raw-rest/`: phản hồi REST THÔ do executor tải lúc dựng sandbox (`FETCH-LOG.txt` ghi URL, giờ, băm). Các `readback-*.json` mới trong
  kho là BẢN TRÍCH từ cùng endpoint (tải lúc khác, ~11:05Z). Đối chiếu từng trường bản trích với bản thô: thiếu/sai/trích lệch là finding.
- git đầy đủ trong `cay-kho/`: kiểm cha/tree của `4397ee6`, quan hệ tổ tiên (`4397ee6` ⊂ `3bdd987` ⊂ `180039c`), tệp mà các PR xen giữa đổi.
- `python3 cay-kho/ops/land_evidence_nguon.py --root cay-kho` và `--tep ...`; `sha256sum -c` trong thư mục provenance.
- KHÔNG đo được: VM Windows (mục `van_hanh_tren_vm` là thuat_lai — chỉ kiểm nhãn có trung thực và câu có khai rộng hơn nhãn không).

## Nhiệm vụ
1. ĐO LẠI TỪNG CON SỐ/SHA/giờ/lời khai trong phần diff của tệp YAML (và header) với `raw-rest/` + git. Liệt kê bảng: lời khai → nguồn → khớp/lệch.
2. Lời khai có rộng hơn phép đo không (vd "bị thay thế bởi push của #1108/#1112/#1109", "ba PR xen giữa chỉ thêm spec/ops", "run đo cây 3bdd987").
3. Bản trích `readback-*` có trung thực, header tệp YAML mô tả đúng loại tệp (thô vs trích) không; `SHA256SUMS.txt` có khớp.
4. Tính nhất quán với phần hồ sơ đã có (trạng thái, `bookkeeping`, `landed_hieu_luc_tu`, nhãn measured/thuat_lai), và cổng `land_evidence_nguon` ĐẠT.
5. Gì còn cũ/sai trong tệp mà bản bổ sung lẽ ra phải sửa (vd câu header "TRANG THAI", mục khác tự mâu thuẫn với phần mới).

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` NGAY (dòng đầu `verdict: dang_lam`), nối thêm sau mỗi hướng. Cuối cùng dòng 1 `verdict: approve` hoặc `verdict: changes_requested`,
dòng 2 `reviewed_sha: b13d3ef93724d249b3db6eeef6d3fe43a61b08f9`, một dòng `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`
Mỗi hướng: giả thuyết / lệnh / output / kết luận (LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC). Finding: `### <slug>  [P0|P1|P2|P3]` + TỆP/DÒNG, VẤN ĐỀ, ĐÃ THỬ NGHIỆM, ĐỘ TIN.
P1 = lời khai sai đo được (SHA/số/trạng thái sai). P2 = khai rộng hơn phép đo / thiếu nguồn / nhãn sai. P3 = diễn đạt. Chủ kho muốn đóng HẾT P1–P3,
nên ghi cả P3. `approve` chỉ khi 0 finding mọi mức và có output thật. Gợi ý vá (nếu có) vào `HINT.patch` (`patch -p0` từ gốc `cay-kho/`).

## Ràng buộc
CHỈ ĐỌC + ĐO, độc lập với executor (Claude). KHÔNG sửa `cay-kho/`, KHÔNG push, KHÔNG gọi mạng.
