# Handoff §7 — wp55 revision 3, phần việc của phiên executor `claude` (g6 → g9)

Bàn giao vì phiên ĐIỀU PHỐI đã tiếp quản nhánh packet (`4085bbf`, và `5ec8fab` trên
`ops/wp55-r3-fix-html-table-token`) và đang tự cấp lease review 11/12. Tiếp tục vá song song
sẽ tái lập đúng sự cố đã trả giá hôm nay — hai phiên cùng đẩy một nhánh, một lease bị đạp.

```yaml
schema_version: 1
packet_id: wp55
revision: 3
role: executor
provider: claude
handoff_reason: nhuong_nhanh_cho_phien_dieu_phoi
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
head_at_handoff: 1a4525a20aa360476a6f59cb157c21097919c457
head_remote_khi_ban_giao: 4085bbf22d565a4189977f0504dfd8e5f748bfce
branch: claude/wp55-r3g5-f3-03
scope_files: 6            # đúng write_set, không nới lần nào
```

## Từng commit chạy dưới lease nào — CÓ BỐN COMMIT NGOÀI SỔ

Đây là phần quan trọng nhất của bản bàn giao. Đọc kỹ trước khi tin `attempts_used`.

| commit | mô tả | lease | trong sổ |
|---|---|---|---|
| `2cccf1e` | g5 — đóng 7 finding lượt 6 | `wp55-r3-exec-5-claude-20260815` | CÓ |
| `1dd5bcf` | g6 — thu miễn trừ về bề rộng AC 19; bỏ ngoại lệ AC 18 | **không** | KHÔNG |
| `91780cb` | g6 — ghi bài học công cụ vào `work-packet` | **không** | KHÔNG |
| `3c4fbc2` | g7 — hàng rào mã lồng một cấp | **không** | KHÔNG |
| `4270210` | g8 — ô bảng HTML không hưởng miễn trừ | **không** | KHÔNG |
| `1a4525a` | g9 — đóng 6 finding lượt 9 | `wp55-r3-exec-9-claude-20260815` | CÓ |

**Bốn commit không lease.** Hai trong số đó (`3c4fbc2`, `4270210`) còn được đẩy KHI lease
reviewer lượt 8 đang neo `91780cb`, làm tip nhánh rời khỏi SHA được thuê soi ⇒ phải huỷ
lease lượt 8 và cấp lại lượt 9. Sổ ghi `attempts_used: 3/3` nhưng **số thật cao hơn**.

Nguyên nhân đo được: phiên executor push lên `claude/**` mà KHÔNG fetch `ops/**` để kiểm
lease đang sống. Bản thảo revision 4 thêm **AC 26** để chặn tái diễn.

## Việc đã đóng — kèm lệnh tái lập, không kèm lời khai suông

| lượt | finding_id | đóng ở | trạng thái |
|---|---|---|---|
| 6 | 7 finding (4 P1 + 3 P2) | `2cccf1e` | đóng, verdict 7 xác nhận |
| 7 | `doctrine-line-break-exemption-bypasses-non-prose` | `1dd5bcf` | đóng |
| 7 | `ac18-overlap-exceptions-have-no-killing-mutant` | `1dd5bcf` | đóng |
| 8 | `…still-bypasses-structured-content` (3 phản chứng) | `3c4fbc2`+`4270210` | đóng |
| 9 | 6 finding (4 P1 + 2 P2) | `1a4525a` | đóng |
| 10 | `…html-table-token-context-bypass` | `5ec8fab` (phiên khác) | đóng |

**Còn mở trên `5ec8fab`, đo lại lúc bàn giao:**

| finding_id | rc đo được | đòi | cần gì |
|---|---|---|---|
| `doctrine-indented-code-block-bypass` | 0 | 6 | sửa mã |
| `doctrine-comment-erases-fence-closer-bypass` | 0 | 6 | sửa mã |
| `doctrine-measurement-marker-semantic-bypass` | 0 | 6 | **SỬA SPEC revision 4** |

## Số liệu — ĐẾM BẰNG MÁY, chép từ đầu ra của suite

Tại `1a4525a`, khối `SỐ LIỆU (đếm bằng máy)` mà chính suite in ra:

```
ca               : 173
đột biến         : 44
lớp lách         : 66
ca bắt-oan       : 35
ngoại lệ AC 18   : 0
```

Chốt tự in này thêm ở g9 vì finding `packet-suite-mutation-count-mismatch`: executor từng
khai `39 đột biến` trong khi thật là `38`, và suite không assert con số nó khai. **Đừng gõ
tay con số nào vào hồ sơ — chép từ đầu ra.**

Gate tại `1a4525a`: `doctrine-scan rc=0` · suite `173/173 ĐẠT` · `tl.py --selftest 1696/1696`
· `release-verify checked=179 failed=0 extra=0` · `golden-test` 20 ca · `eol_policy` 304/0 ·
AC 20 cây merge (master `2531366`, `GIT_DIR` kho thật): doctrine `rc=0`, suite `173/173`.

## Kỷ luật đã trả giá để học — giữ lấy, đừng dựng lại từ đầu

1. **DANH SÁCH ĐÓNG trước khi vá.** Mỗi lượt nó đều tìm ra nhiều hơn reviewer nêu: 18 so
   với 2 (lượt 7), 18 so với 4 (lượt 8), 18 so với 9 (lượt 9). Bỏ bước này là vá mù.
2. **Đo CẢ HAI chiều.** Hai lần bản vá tự đẻ lỗi ở chiều ngược: g8 đầu độc đuôi tệp, g9
   comment xoá rào đóng thật. Cả hai đều do chỉ đo chiều lọt.
3. **"Fail-closed" KHÔNG phải lý lẽ ở packet này.** AC 19 nói bắt oan văn bản bình thường
   là KHÔNG ĐẠT, ngang với để lọt. Hai chiều cân nhau.
4. **Lớp bị nhiều đường cùng phủ ⇒ đột biến PHỐI HỢP, KHÔNG khai ngoại lệ.** Bỏ cửa ngoại
   lệ đi thì lập tức phơi ra một lời khai sai (`nbsp` khai "hai đường", thật là ba).
5. **Đọc LEASE, không chỉ đọc prompt.** Prompt bị khoá băm nên không mang được mọi thứ;
   mục chỉ nằm trong lease thì executor sẽ bỏ sót — đã xảy ra với mục an ninh, xem dưới.

## Hai lỗi của phiên này, ghi để không ai lặp

**A. Rò rỉ secret, HAI LẦN, cùng một lớp.**

- lần 1: lệnh chẩn đoán in nguyên `CODEX_AUTH_JSON` (5648 ký tự base64, chứa refresh token
  còn sống) ra transcript. **Cần thu hồi và cấp lại credential.**
- lần 2: dòng tôi viết vào `work-packet/SKILL.md` để dạy "kiểm bằng sự tồn tại, không in
  nội dung" **tự nó in ra secret** — `${VAR:+…}` nối `${VAR:-…}`, nhánh "đã đặt" bung ra
  chính giá trị. Phiên điều phối vá ở `4085bbf`.

**B. Đẩy lên nhánh packet mà không kiểm lease đang sống** — xem bảng commit ở trên.

## Việc kế tiếp, theo thứ tự

1. **Chủ kho chốt bốn tham số của spec revision 4** (`ops/specs/wp55-r4-spec.md` trên nhánh
   `ops/wp55-r4-spec-draft`): `N`, `M`, nơi di trú, và khối chứng cứ có được nằm trong
   `CLAUDE.md` không. Chưa chốt thì không cấp lease revision 4 được.
2. Vá `doctrine-indented-code-block-bypass` và `doctrine-comment-erases-fence-closer-bypass`
   — hai lỗi mã thuần, câu chữ AC hiện tại đã đủ.
3. `doctrine-measurement-marker-semantic-bypass` chờ AC 19 mới của revision 4.

Nguyên mẫu AC 19 mới đã dựng và đo: `ops/specs/wp55-r4-ac19-nguyen-mau.py`, **9/9** — đóng
cả bốn phản ví dụ của bốn lượt review mà không bắt oan ca thật.
