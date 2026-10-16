# Đặc tả packet wp766 — t81 chập chờn khi `os.getpid()` trùng PID giả của fixture

Đặc tả đóng băng, soạn theo skill `soan-spec`. Sửa tệp này là đổi băm; muốn đổi thì soạn `wp766-r2.md`, không sửa đè.
Đặc tả KHÔNG cấp việc: cần Issue #766 + lease còn hiệu lực do chủ kho cấp (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4).

**Trạng thái quyết định:** mọi mục đánh dấu ➡️ là KHUYẾN NGHỊ của phiên soạn, CHƯA được chủ kho chốt. Chủ kho chốt
(hoặc sửa) trong comment cấp lease; chốt khác khuyến nghị thì phải ra `wp766-r2.md` trước khi cấp lease.

## packet_id · packet_issue

- `packet_id`: `wp766`
- `packet_issue`: [#766](https://github.com/ducthangho/tra-luat/issues/766)
- `mission_issue`: 766 (packet đứng riêng, không có mission cha)
- `revision`: 1
- `depends_on`: `[743]` — xem §Xung đột write set.

## nguon_cap_viec

Packet khắc phục. Nguồn: finding của reviewer Codex trên PR #765 (packet #743), tái hiện bằng cách ép `os.getpid`
về 10/11/12 — đỏ trên master `9fddb1d` lẫn head `80e0fac`; PID không trùng thì `--lap-ca` 20/20 xanh. Finding này
NGOÀI write set/objective của #743 (lỗi có sẵn trên master), nên tách thành packet riêng thay vì nới #743.

## Lỗi — đo, không suy

`t81_chup_cay_windows_thieu_creationdate_phai_fail_closed` (`.claude/dev/launcher_test.py`) dựng cây giả bằng PID
cứng `10` (gốc), `11` (con mù, khoá `None`), `12` (con thường). `_chup_cay` (`.claude/dev/launcher.py`) bỏ PID của
chính tiến trình: `ra.pop(os.getpid(), None)` — **đúng ý đồ** ("tuyệt đối không tự giết mình"), KHÔNG phải lỗi mã
sản phẩm. Fixture giả định ngầm rằng `os.getpid()` ∉ {10, 11, 12}; giả định ấy sai trong namespace PID mới.

Đo 02:15Z 16-10-2026, `9fddb1d`, Python 3.13.16, `launcher_test.py --lap-ca t81… --lan 1`, ép `os.getpid`:

| `getpid` | kết quả | vế hỏng |
|---|---|---|
| 11 | HỎNG | (a) `hau due khong lay duoc khoa bi bo qua im lang` — con mù bị `pop` nên ảnh không còn fail-closed |
| 12 | HỎNG | (b) `tien trinh mu NGOAI cay khong duoc lam hong ca anh` — ảnh thiếu 12 |
| 99999 | qua | — |
| 10 | theo reviewer #765: HỎNG; phiên soạn chưa đọc được dòng kết quả riêng (bị cắt khỏi output) — **executor đo lại** |

## review_class

➡️ `sensitive`. Diff dự kiến chỉ chạm tệp TEST, nhưng tệp ấy là bộ test của launcher (§8 "launcher hoặc gate
lifecycle"), và §8 tính lớp fail-closed theo đường dẫn; executor không được hạ lớp. Chủ kho có thể hạ xuống
`routine` bằng quyết định có audit — phiên soạn không tự hạ. Theo tiền lệ wp743 (cùng hai tệp): reviewer `codex`,
assurance đích `human_audited`.

## write_set (exact)

1. `.claude/dev/launcher_test.py`
2. `changelog.d/wp-766.md`

**KHÔNG** có `.claude/dev/launcher.py`. Nếu executor kết luận phải sửa mã sản phẩm thì đó là phát hiện ngoài spec:
dừng, handoff, ra r2 — không tự mở write set.

## Xung đột write set

Đo 02:17Z 16-10-2026 bằng `python ops/lease_publish.py ai-dang-giu <path>` sau khi fetch đủ
`+refs/heads/*` (so tập tên: 545 nhánh máy chủ, 0 thiếu cục bộ):

- `.claude/dev/launcher_test.py` ⇒ **NGƯỜI_GIỮ 1**, rc=11: `wp743-r1-g1-claude-20261016`
  (`refs/remotes/origin/ops/wp743-r1-g1-lease`, CÒN_HẠN tới `2026-10-18T06:00:00Z`, PR #765).
- `changelog.d/wp-766.md`: tệp chưa tồn tại; không đo riêng.

Hệ quả: **không được cấp lease wp766 khi lease wp743 còn giữ `launcher_test.py`**. ➡️ Thứ tự khuyến nghị: #765 land
trước, rồi cấp lease wp766 trên master SAU land. Lý do: (i) #765 sửa chính tệp này nên base trước #765 sẽ conflict;
(ii) t81 sẽ còn đỏ chập chờn trên CI của #765 — chủ kho quyết #765 có land với t81 chập chờn hay không (lỗi đỏ sẵn,
delta = 0). Lựa chọn khác (thu hồi wp743 sớm bằng bia mộ, hoặc nhét bản vá vào #765) là quyết định của chủ kho.
**Đo lại `ai-dang-giu` (L5) ngay trước lúc cấp lease** — con số trên trôi.

## base

Chưa chốt: ➡️ SHA `origin/master` NGAY SAU khi #765 land, đo lại lúc cấp lease. `9fddb1d` chỉ là nền đo lỗi.
Lease neo `start_from_sha` vào SHA đo lúc cấp, không neo vào số trong tệp này.

## muc_tieu

Mỗi mục chiếu vào đúng một đường dẫn ở write set (L2). Neo theo TÊN ca/hàm, không theo số dòng.

| # | Mục | Đường dẫn |
|---|---|---|
| M1 | **Liệt kê TRƯỚC khi vá** mọi ca trong `launcher_test.py` đưa PID giả cứng vào đường mã có loại trừ `os.getpid()` thật (đo trên base: `_chup_cay` `ra.pop(os.getpid(), None)` và `_giet_rieng` `if q == os.getpid()`), bằng phép đo ép `os.getpid` về từng PID giả mà ca ấy dùng. Ghi bảng ca × PID × kết quả vào thân PR. Chỉ những ca ĐỎ dưới phép đo mới thuộc M2; ca không đỏ ghi rõ "không bị ảnh hưởng, vì …". | `launcher_test.py` |
| M2 | Fixture của t81 (và mọi ca M1 tìm ra) sinh PID giả bảo đảm khác `os.getpid()` và khác `os.getppid()` đọc LÚC CHẠY ca, giữ nguyên quan hệ cây (gốc · con mù · con nhánh khác) và nguyên hai vế (a)/(b). Không đổi ngữ nghĩa vế nào. | `launcher_test.py` |
| M3 | Ca hồi quy mới (tên `t…` theo quy ước tệp) ép `os.getpid` trùng LẦN LƯỢT 10, 11, 12 (PID cứng cũ) và trùng PID cha giả mà fixture dùng, mỗi lần chạy lại thân t81 ⇒ phải xanh. Ép `os.getpid` phải được hoàn nguyên (harness cô lập toàn cục của tệp đã chụp/hoàn nguyên; ca vẫn phải tự hoàn nguyên trong `finally`). | `launcher_test.py` |
| M4 | Bảng đột biến (`--dot-bien`) thêm đột biến quay fixture về PID cứng 10/11/12, đích = ca M3. Hai đột biến sẵn có của t81 (`chup_cay_khong_fail_closed_trong_cay`, `chup_cay_fail_closed_ca_may`) vẫn phải bị giết sau M2 — nếu chuỗi `old` của chúng không còn khớp thì sửa chuỗi, không xoá đột biến. | `launcher_test.py` |
| M5 | Mảnh changelog tiếng Anh, theo khuôn `changelog.d/wp-727.md`: lỗi, cách sửa, phép đo, thứ chưa đo. | `changelog.d/wp-766.md` |

## nghiem_thu

Mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3).

| Mục | Tiêu chí | Phép đo làm ĐỎ |
|---|---|---|
| M1 | Bảng ca × PID × kết quả có trong thân PR, đo trên base, mỗi ô có lệnh tái lập. | Thiếu bảng; hoặc reviewer ép `getpid` về một PID giả trong một ca KHÔNG có trong bảng và ca ấy đỏ. |
| M2 | Với mọi `p` ∈ {1, 10, 11, 12, PID cha giả} và mọi PID giả mới của fixture: `--lap-ca t81… --lan 1` với `os.getpid` ép về `p` ⇒ qua. | Bất kỳ `p` nào ra HỎNG. |
| M2 | Hai vế (a)/(b) còn răng: hai đột biến sẵn có của t81 vẫn bị giết, bởi CHỐT của t81 (không bởi traceback/lỗi vô can). | `--dot-bien` báo một trong hai sống, hoặc chết vì ngoại lệ không phải assertion của t81. |
| M3 | Ca M3 xanh trên base đã vá; ca M3 ĐỎ khi fixture quay về PID cứng. | Đột biến M4 sống. |
| M3 | Không rò `os.getpid` bị ép sang ca sau. | Chạy toàn suite ⇒ một ca sau M3 đổi kết quả so với chạy toàn suite trên base. |
| M4 | `--dot-bien` của tệp: 0 đột biến sống mới so với base; đột biến M4 bị giết bởi ca M3. | Sống > 0 mới, hoặc M4 chết bởi ca khác. |
| chung | `python .claude/dev/launcher_test.py` trên Python **3.12 và 3.13**: delta = 0 so base ngoài ca M3 (tập ca HỎNG/BỎ QUA giống hệt base; tổng tăng đúng số ca mới). Dựng hai vế base/sau trong **một** lệnh, cùng rig (bài học "phép đo delta"). | Tập ca HỎNG khác base, hoặc số ca tăng khác số ca thêm. |
| chung | `python -m ruff check --select F .claude/dev/launcher_test.py`: delta F so base = 0. | Delta > 0. |
| M5 | Mảnh changelog tồn tại, tiếng Anh, khai phép đo và thứ chưa đo. | Thiếu tệp, hoặc khai rộng hơn phép đo (reviewer dựng được phản ví dụ). |

Điều kiện merge: review độc lập 0 P1 / 0 P2 trên đúng head; assurance theo `review_class` đã chốt; chủ kho uỷ quyền
land bằng comment bền neo đúng head.

## Trần kích thước

`docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md`: ≤ 3 tệp và ≤ 300 dòng thêm. Dự kiến 2 tệp, < 120 dòng
(chưa đo — ước lượng của phiên soạn). Vượt ⇒ DỪNG, xin ngoại lệ chủ kho. Báo dạng "2 tệp / N dòng thêm; trần 300".

## ngoai_pham_vi

- Sửa `_chup_cay` / `_giet_rieng` trong `launcher.py`: việc loại trừ PID của chính mình là đúng; lỗi nằm ở fixture.
- Ép mọi ca khác của tệp dùng PID động "cho chắc": chỉ sửa ca mà phép đo M1 cho ra ĐỎ (không widen).
- Thêm lượt CI chạy trong namespace PID mới: không cần — M3 tái lập điều kiện bằng cách ép `os.getpid`.
- Windows CI: diff chỉ chạm test thuần Python và fixture `m.platform.system = lambda: "Windows"`; ➡️ không đòi lượt
  `windows-latest` trước merge (chủ kho chốt).

## hinh_dang_ke_thua

`khong_ap_dung` cho số đếm từ biên nhận tiền nhiệm (finding đến từ review #765, packet #743 khác lớp lỗi). Hình dạng
ghi nhận để lượt sau đếm: **H-PID — fixture giả định ngầm về môi trường chạy (PID) làm ca chập chờn theo rig** — lần 1.
Cùng họ CLAUDE.md "phép đo delta... rig tự đẻ ra hồi quy" và "cùng cổng, hai kết quả": lần này rig KHÔNG chỉ nhiễu
mà quyết định xanh/đỏ.

## chua_do_duoc

- Kết quả riêng của `getpid=10` trong phép đo của phiên soạn (dòng bị cắt); chỉ có lời khai reviewer #765.
- Tần suất thực của va chạm trên CI GitHub (runner thường có PID lớn) — chưa có lượt CI đỏ vì t81 được ghi nhận.
- Các ca khác bị ảnh hưởng: chưa liệt kê — đó là M1.
- Python 3.12: phiên soạn chỉ đo trên 3.13.16.
