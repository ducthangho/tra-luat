# Erratum — `LAND-DOC-RECEIPT-THU-HOI-C1a1a.md` (revision 5)

Spec r5 ĐÓNG BĂNG theo băm (sha256 `978058983e8eddefebfba267dbff2ef5cee95daf9b2d4847121d43b8cff89d77`,
blob `8224ba54176f6bbfba528ed2e3fb6555852ba336`, commit nguồn `0fc9766`). Không sửa tệp ấy; đính chính sống ở đây.
Chủ kho chọn ghi erratum (phiên điều phối 2026-09-28, lựa chọn "Errata file in #667") sau khi PR #666 đã merge tại `f8a7829`,
để đóng finding G5 `acceptance-doi-khong-revision` của Codex CLI lượt 1 trên PR #667.

| chỗ | spec r5 ghi | thực tế đã duyệt / đã đo | nguồn |
|---|---|---|---|
| A14 (dòng 188) | tổng dòng thêm trên ba đường write set **≤ 400** (ngoại lệ có phạm vi ADR-0044) | chủ kho nâng **≤ 500** rồi **≤ 650**; ứng viên đã merge (`bf63bb1`) thêm **+650/−0** (`git diff --numstat ceb1a3f bf63bb1` trên ba đường: 1 + 114 + 535) | lease `c1a1a-exec-2-claude-20260927` trường `lech_nguong_duoc_duyet`; human audit #666 comment 5864536112 ("Trần dòng ≤650 (thay 400)") |

**Erratum này KHÔNG biến A14 của r5 thành đạt.** PROTOCOL §3.2 quy định đổi acceptance thì tạo revision mới và
làm lease cũ mất hiệu lực; việc nâng trần đã được làm bằng quyết định trong lease, không qua revision. Đó là một
lệch quy trình đã xảy ra, khai ở `ops/land/pr666-wp650-land-evidence.yaml` (`lech_protocol_khai: A14-KHONG-REVISION`).
Tệp này chỉ ghi lại ngưỡng thực tế đã được duyệt và căn cứ của nó, cạnh spec đóng băng, để người đọc spec không
hiểu nhầm rằng ứng viên đã merge nằm trong ≤ 400. Không tạo revision hồi tố cho packet đã merge. Lúc ghi erratum này (PR #667), packet
mới `merged`, CHƯA `landed`; trạng thái HIỆN HÀNH xem `trang_thai_packet` trong `ops/land/pr666-wp650-land-evidence.yaml`.

Phạm vi đo cần phân biệt: +650 là so với master ngay trước merge (`ceb1a3f`). So với acceptance baseline gốc của
lease (`5618f61…`), numstat ba đường là +730/−10 vì master đã tiến (Codex CLI #667 lượt 1, G5). Không dùng mốc sau
để làm nhỏ con số.
