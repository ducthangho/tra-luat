# Cross-review lượt 2 — packet `land-81-ha-cap` r2 g1 (mission #748), ducthangho/tra-luat — reviewer: codex

Bạn là reviewer ĐỘC LẬP, phiên mới. Executor là một phiên Claude. Không tin lời khai của executor; tự đo.

## Đối tượng
- Kho tại `cay-kho/` (clone đã checkout). `reviewed_sha` = `dd877daebbc70c9b74fb883bd69cc52d98b5f33c`
  (nhánh `agent/land-81-ha-cap-r2-claude`). Base = `44884446f71c89e25f9a72ac58e4f597db63c1ba` (ông của head; cha là `3519c3d`, head lượt 1).
  Clone là bản nông; base có trong object store. Trước mọi việc: `git -C cay-kho rev-parse HEAD` phải bằng `reviewed_sha`.
- Thay đổi toàn packet: `git -C cay-kho diff 44884446 dd877da` — chỉ 3 tệp:
  `ops/land/pr870-claude-md-bai-hoc-c-land-evidence.yaml`, `ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml`,
  `ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml`.
- Đặc tả đóng băng: `cay-kho/ops/specs/land-81-ha-cap-r2-pr870-889-896.md`, sha256 phải bằng
  `ba96df801af3caebd015b43611fdaaf64b48bf8dc8491c46310742fabd7d7bed`. Đặc tả là thước đo duy nhất về phạm vi; tự đọc §1–§5.
- Tiền lệ hình dạng (r1): khối `assurance_81` và `ha_cap_assurance_81_20261027` trong `cay-kho/ops/land/pr924-wp923-land-evidence.yaml`.

## Lượt trước
Lượt 1 (`verdict-cu/review-1-VERDICT.md`, trên `3519c3d`) ra `changes_requested` 0/0/2/0: F1, F2 — `ha_cap_assurance_81_20261027.thay_the`
của #870 và #889 bỏ sót `$.cap_nhat_20261026.landed_ly_do` (văn xuôi "truoc khi reviewer_assurance_81 dat"). Bản vá
`3519c3d..dd877da` thêm đúng một mục vào mỗi danh sách — lời khai của bên vá, tự kiểm. Kiểm F1/F2 đã đóng, VÀ đo lại toàn bộ
(a)–(e) trên head mới như thể lượt đầu: bản vá có thể để sót đường thứ ba hoặc phá bất biến tiền tố byte.

## Nhiệm vụ: đo lại từng khẳng định
Danh sách dưới KHÔNG đủ; mỗi khẳng định sai bạn tự tìm ra được tính là finding.

(a) **Đúng §2 của đặc tả.** Với mỗi hồ sơ: `assurance_81.reviewer_assurance_81 = CHUA_DAT`; `review_exact_sha` đúng (#870, #889
`DAT`; #896 `CHUA_DAT` kèm ghi chú comment 6431407190 trên PR #956 là căn cứ của `landed`, không của `review_exact_sha`);
`thuc_thi` đủ `model` (measured), `effort` (not_measured + lý do), `sandbox_mode` (not_measured + lý do); `lich_su` nêu đúng đường dẫn ở bảng §1.
Khối `ha_cap_assurance_81_20261027` ở cuối tệp phải liệt kê **TỪNG** đường dẫn trong tệp đang khai §8.1 `DAT` hoặc `cross_approved`
— tự quét toàn tệp (mọi độ sâu, cả văn xuôi), mỗi đường dẫn bị bỏ sót hoặc liệt kê sai là finding. Ghi đúng comment duyệt
`landed` (#870/#889: 6411410063 trên PR #951; #896: 6431407190 trên PR #956), và nói rút `landed` là quyết định riêng của chủ kho.

(b) **Mọi con số/ID trong khối mới khớp nguồn.** Mở chính `ops/reviews/<...>/run/run.json` được trỏ tới: `run_id` (8 hex đầu),
`ma_thoat`, `head`, `model_phuc_vu_trang_thai`, số sự kiện `model_phuc_vu` và tên model, `lenh.so_doi_so`, việc vắng mọi trường
effort/sandbox. Verdict `.md` được trỏ tới có thật là approve 0 P0–P3 trên đúng head đó không.

(c) **Không sửa gì cũ.** Byte của base phải là tiền tố nguyên vẹn của mỗi tệp mới; YAML nạp xong so với base chỉ khác hai khoá
cấp gốc `assurance_81`, `ha_cap_assurance_81_20261027`; không khoá trùng (kể cả khoá cấp gốc trùng với khoá sẵn có); `landed` các khối cũ không đổi.

(d) **Cổng.** Trong `cay-kho/` chạy và ghi rc + dòng tổng: `python3 ops/land_evidence_nguon.py --root .` (đòi `TỔNG: ĐẠT`),
`python3 ops/bien_nhan_v2.py --root .`, `python3 .claude/dev/packet_loop.py doctrine-scan --root .`. Hai cổng sau phải KHÔNG thêm
vi phạm hay `KHÔNG ĐO ĐƯỢC` so với base: dựng bản sao thứ hai checkout `44884446` trong thư mục tạm NGOÀI `cay-kho/`, chạy cùng
lệnh, so số. Đo răng: trên một bản sao tạm (không phải `cay-kho/`), đổi một token nguồn `measured` mới thành đường dẫn không tồn
tại ⇒ `land_evidence_nguon` phải ĐỎ; ghi kết quả.

(e) **Trần và cấm**: ≤3 tệp / ≤180 dòng thêm (so base `44884446`); không đụng `ops/land_evidence_nguon.py`, `ops/reviews/`, không rút `landed`.

## Quyền
Chỉ đọc `cay-kho/`. Không push, không gọi API ghi GitHub, không sửa `cay-kho/`. Được ghi tệp tạm dưới thư mục làm việc hiện tại
(ngoài `cay-kho/`). Đừng tự soạn nội dung dò thoát đường dẫn; nếu cần hướng thử như vậy thì mô tả bằng lời trong verdict.

## Đầu ra
Ghi `VERDICT.md` ở thư mục làm việc hiện tại (KHÔNG trong `cay-kho/`):
- dòng đầu: `verdict: approve` hoặc `verdict: changes_requested`; dòng hai `reviewed_sha: <40 hex>`;
- dòng `so_lop: P0 n / P1 n / P2 n / P3 n`;
- mỗi finding: id, mức (P0–P3), tệp:dòng, mô tả, cách tái hiện, đề xuất vá;
- mục "Đã đo": từng phép đo của (a)–(e) với lệnh, rc, kết quả.
`approve` chỉ khi 0 finding P0–P3.
