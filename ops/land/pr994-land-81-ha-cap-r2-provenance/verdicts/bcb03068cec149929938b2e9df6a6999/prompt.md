# Cross-review lượt 3 — packet `land-81-ha-cap` r2 g1 (mission #748), ducthangho/tra-luat — reviewer: codex

Bạn là reviewer ĐỘC LẬP, phiên mới. Executor là một phiên Claude. Không tin lời khai của executor; tự đo.

## Đối tượng
- Kho tại `cay-kho/`. `reviewed_sha` = `e77ac9ea48f3bdebc32d18215ef5ab585fab1fb7` (nhánh `agent/land-81-ha-cap-r2-claude`).
  Trước mọi việc: `git -C cay-kho rev-parse HEAD` phải bằng `reviewed_sha`.
- `e77ac9e` là MERGE COMMIT: cha 1 = `dd877daebbc70c9b74fb883bd69cc52d98b5f33c` (head lượt 2, đã approve 0/0/0/0 — `verdict-cu/review-2-VERDICT.md`),
  cha 2 = `79dbaf443f90daece751d9ab2537796bbd6084bf` (`origin/master` lúc merge). Lý do merge: chủ kho yêu cầu một run PR sạch
  (run PR cũ bị GitHub treo); không có thay đổi nội dung chủ ý nào.
- Base gốc của packet = `44884446f71c89e25f9a72ac58e4f597db63c1ba`. Đặc tả: `cay-kho/ops/specs/land-81-ha-cap-r2-pr870-889-896.md`,
  sha256 phải = `ba96df801af3caebd015b43611fdaaf64b48bf8dc8491c46310742fabd7d7bed`.
- Write set (chỉ 3 tệp): `ops/land/pr870-claude-md-bai-hoc-c-land-evidence.yaml`, `ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml`,
  `ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml`.

## Nhiệm vụ: đo lại
(a) **Merge sạch.** `git diff 79dbaf4 e77ac9e` phải CHỈ chạm 3 tệp write set, và nội dung 3 tệp ấy ở `e77ac9e` phải BẰNG BYTE với `dd877da`
(tức merge không đổi gì trong write set). `git diff dd877da e77ac9e` chỉ được chứa thay đổi của master (`44884446..79dbaf4`), không thêm gì
khác: kiểm `git diff 44884446 79dbaf4` ≡ `git diff dd877da e77ac9e` (so tập tệp và nội dung). Master không được sửa 3 tệp write set sau base
(nếu có thì kiểm hai bên không lẫn).
(b) **§2/§3 đặc tả vẫn đúng trên head mới.** Byte base `44884446` là tiền tố nguyên vẹn của mỗi tệp write set; YAML nạp xong chỉ khác base hai khoá
cấp gốc `assurance_81`, `ha_cap_assurance_81_20261027`; `landed` không đổi; danh sách `thay_the` phủ đủ mọi lời khai §8.1 DAT/cross_approved
(lượt 1 bắt F1/F2, lượt 2 xác nhận đã vá — đo lại, đừng tin). Mọi token nguồn `measured` mới phân giải được và nội dung khớp `run.json`.
(c) **Cổng trên head mới, so với master `79dbaf4`** (dựng bản sao thứ hai ở thư mục tạm NGOÀI `cay-kho/`): `python3 ops/land_evidence_nguon.py --root .`
(đòi `TỔNG: ĐẠT`), `python3 ops/bien_nhan_v2.py --root .`, `python3 .claude/dev/packet_loop.py doctrine-scan --root .`,
`python3 ops/kiem_ho_so_land.py --root .` (nếu chạy được). Không được thêm vi phạm/`KHÔNG ĐO ĐƯỢC` nào so với master. Master đã đổi
`ops/bien_nhan_v2.py`, `ops/kiem_ho_so_land.py` sau base: kiểm riêng xem các cổng MỚI ấy có kêu gì về 3 tệp write set không.
(d) Trần: so master, ≤3 tệp / ≤180 dòng thêm; không đụng `ops/land_evidence_nguon.py`, `ops/reviews/`, không rút `landed`.

## Quyền
Chỉ đọc `cay-kho/`. Không push, không gọi API ghi GitHub. Ghi tệp tạm dưới thư mục làm việc hiện tại (ngoài `cay-kho/`).
Đừng tự soạn nội dung dò thoát đường dẫn; nếu cần thì mô tả bằng lời.

## Đầu ra
Ghi `VERDICT.md` ở thư mục làm việc hiện tại: dòng đầu `verdict: approve|changes_requested`, dòng hai `reviewed_sha: <40 hex>`,
dòng `so_lop: P0 n / P1 n / P2 n / P3 n`, từng finding (id, mức, tệp:dòng, mô tả, tái hiện, đề xuất), mục "Đã đo" với lệnh/rc/kết quả.
`approve` chỉ khi 0 finding P0–P3.
