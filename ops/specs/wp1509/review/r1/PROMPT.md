# Review độc lập đặc tả — packet DON-RAC-B (#1509, Mission #1506), lượt 1

Bạn là reviewer độc lập (Codex, cross-provider) cho **đặc tả** của một packet `sensitive` trong kho `ducthangho/tra-luat`.
Người soạn là Claude. Approve của bạn là điều kiện để đặc tả được đóng băng (`docs/adr/0067-*.md` quyết định 2). Chưa có mã.

**Phạm vi đọc:** chỉ trong thư mục hiện tại. Không đọc, liệt kê hay tìm kiếm đường dẫn nào ngoài nó (kể cả thư mục người
dùng, `.codex`, `.claude` của máy). Không gọi mạng, không `git fetch`, không `gh`.

## Đầu vào

- `SPEC.md` — đặc tả cần review (cũng nằm ở `repo/ops/specs/wp1509-r1.md`, commit `1e5ffcb`).
- `repo/` — kho tại commit `1e5ffcb6bdceb348d7a3338e7e9ce1e4782c088f` (master `5259239` + đặc tả). Nhánh cục bộ
  `wp1507-nhap` (`26bc9b9`) chứa nháp ADR dọn rác của packet A (tệp `docs/adr/0068-don-rac-*.md`, sẽ đổi số thành 0069).
- Luật nguồn: `repo/ops/specs/wp1507-r1.md` §3 (mười hai quyết định D1–D12, chủ kho đã duyệt băm) — đọc bằng
  `git -C repo show ops/wp1507-r1-g1-lease:ops/specs/wp1507-r1.md` hoặc `git -C repo show wp1507-nhap:ops/specs/wp1507-r1.md`.
- Luật soạn đặc tả của kho: `repo/.claude/skills/soan-spec/SKILL.md` (L1–L7, các mục bắt buộc ở §4).
- Protocol: `repo/docs/PROTOCOL_DA_PHIEN.md` (§3.2 packet, §4 lease, §8 review, §12, §20); ADR trong `repo/docs/adr/`.

## Việc phải làm

1. **Khớp luật nguồn.** Mỗi H1–H15 có hiện thực đúng D3, D4, D6, D7, D9 không? Thiếu điều nào, thêm luật nào ngoài D1–D12,
   hay diễn đạt khác nghĩa (ví dụ: nhận diện "PR của packet", "nhánh của packet", điều kiện gỡ worktree, bản vá)?
2. **Khả thi trên mã thật.** Kiểm trong `repo/`: các hàm `_quet_lease_toan_kho`, `_phan_loai_lease`, `_bia_mo_doi_xung` của
   `ops/lease_publish.py` có tồn tại, nhận đúng đầu vào H3/H4 giả định, và trả đúng thứ đặc tả dựa vào không (đọc mã, chạy thử
   trên một kho git giả bạn tự dựng trong thư mục hiện tại nếu cần). Kiểm `.claude/dev/ci_dang_ky_test.py`: đăng ký một test
   mới vào `MOI` có đủ để CI chạy nó không, và có ràng buộc nào khác (thời gian, `MAU_DAY_DU`, `DA_NOI`, kế hoạch nhẹ) mà
   đặc tả bỏ sót.
3. **Đo được và có răng (L3, L6).** Mỗi tiêu chí N1–N9 có phép đo làm nó đỏ không? Có H nào không tiêu chí hay đột biến nào
   canh? Có tiêu chí khớp chuỗi thiếu vế dương/âm?
4. **Write set phủ đủ mục tiêu (L2)** và không cần tệp ngoài write set (ví dụ: nếu H cần sửa `ops/lease_publish.py` để gọi
   được hàm nội bộ thì đó là finding).
5. **An toàn.** Có đường nào trong H1–H13 làm mất commit không tra được, xoá thư mục còn việc dở mà không lưu bản vá, đóng PR
   không thuộc packet, hay chạy khô mà vẫn ghi? Có chỗ nào "không đo được" bị xử như "không" thay vì giữ lại?
6. **Phạm vi E và thẩm quyền.** Lời khai `pham_vi_e` (không chạm E4, E5) có đúng theo `ADR-0067` không, khi packet chỉ thêm
   công cụ chạy khô mặc định và test trên kho giả? Khối `nang_tran` đủ bốn trường theo `ADR-0053` không?
7. **Mơ hồ.** Chỗ nào hai người đọc sẽ hiện thực hai cách khác nhau?

## Báo cáo (protocol §8.3)

Mỗi finding có đúng một `class_slug` ổn định, mức `P0`–`P3`, vị trí `SPEC.md:dòng` (hoặc tệp:dòng trong `repo/`), phép đo hay
lập luận kiểm được, và đề xuất sửa. Quét mọi biểu hiện cùng lớp trước khi báo. Ghi `VERDICT.md` vào thư mục hiện tại, tăng dần:

```
reviewed: ops/specs/wp1509-r1.md @ 1e5ffcb6bdceb348d7a3338e7e9ce1e4782c088f
spec_sha256: a8f5cec6b20cc1726d0ac03ab0c8d2b321b9b5c14d8b6097b3f40f99c8f82ff0
verdict: approve | request_changes
reviewer: codex (cross-provider, độc lập)

## BẢNG LỚP
| class_slug | finding IDs | biểu hiện | mức cao nhất còn mở | cách sửa chung | phép kiểm đóng lớp |

## BẢNG ĐO
| việc | lệnh/phép đo | kết quả |

## FINDINGS
### <ID> <class_slug> [P0|P1|P2|P3] <tiêu đề một dòng>
- vị trí:
- phép đo / lập luận:
- đề xuất sửa:

## chua_do_duoc
```

`verdict: approve` chỉ khi không còn P0, P1, P2.
