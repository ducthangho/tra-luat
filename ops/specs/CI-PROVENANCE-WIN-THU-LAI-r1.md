# Đặc tả packet `CI-PROVENANCE-WIN-THU-LAI` r1: thử lại có giới hạn khi `os.replace` gặp `PermissionError` trên Windows

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
windows: required

| trường | giá trị |
|---|---|
| packet_id | `CI-PROVENANCE-WIN-THU-LAI`, revision 1, generation 1 |
| trang_thai | **nháp, chờ chủ kho duyệt băm** (xem `pham_vi_e`) |
| packet_issue | #1475 |
| nguon_cap_viec | Phát hiện Windows của packet #1322 (comment 7049377019: `L4_mode_step_key_truthy` ra `TIN_DUNG_GIA` vì `PermissionError` [WinError 5] khi `os.replace` thư mục). Chủ kho chọn phương án 1 (sửa mã) và trả lời "theo khuyến nghị" cho tám câu hỏi soạn đặc tả, chat phiên executor 21-11-2026 |
| review_class | `sensitive`: hai đường dẫn không có trong `_BANG_LOP` của `ops/lease_publish.py` nên mặc định `sensitive` (đo 01:40Z 21-11 trên `e02d748`) |
| base | `origin/master` lúc cấp lease. Lúc soạn: `e02d748d29cd5165fc29fa1a5a8e9b94593874c7` (đo 01:40Z 21-11) |
| depends_on | `[]`. `ai-dang-giu` cho hai đường dẫn write set: `NGƯỜI_GIỮ 0` (clone mới, refs/heads = máy chủ, đo 01:37Z 21-11) |
| executor · reviewer | executor: phiên Claude Code ghi Issue #1475; reviewer: Codex offline (khác họ model, `cross_approved`) |
| assurance mục tiêu | `cross_approved` trên exact head, cộng duyệt merge của chủ kho |

**Giới hạn lời khai.** Mọi khẳng định ở đây chỉ chứng minh tới đúng phép đo ghi kèm. Ba trạng thái: có · không ·
**KHÔNG ĐO ĐƯỢC**; trạng thái thứ ba làm cổng ĐỎ.

## 1. Phép đo nền

- Hàm `ghi_nguyen_tu` (`ops/ci_provenance.py`, dòng 553–570 trên `e02d748`) có **ba** lời gọi `os.replace`:
  (a) `os.replace(out, cu)` cất bản trước; (b) `os.replace(tam, out)` đưa thư mục tạm vào chỗ; (c) `os.replace(cu, out)`
  hoàn tác trong nhánh `except`. Không lời gọi nào thử lại.
- Lỗi thật (một lần, lượt cả bộ N=1 trên DESKTOP-T9R33P2, Python 3.12.10, ứng viên `7c429aa`, log
  `C:\Users\ThangHD\wp1322-g2\ca_bo_n1_v3.log`, không trong kho): lời gọi (b),
  `PermissionError: [WinError 5] Access is denied: '...\Temp\cip_out_9etb7jnn\.out.tam-pqtgy8ij' -> '...\out'`.
  Máy ấy: Defender `RealTimeProtectionEnabled = True`, dịch vụ `WSearch` đang chạy (đo 08:3xZ giờ máy, 21-11).
- Tái hiện độc lập (mkdtemp cùng cấp → ghi 7 tệp → `os.replace` thư mục), cùng máy, 21-11: **6000 lần, 0 lỗi** (3000 không
  thử lại, 3000 có thử lại). `c48_nguyen_van_va_mien` chạy lặp qua `--mot-ca` trên `7c429aa`: **11 lần, 0 lỗi** lúc soạn
  (vòng 30 lần còn chạy). Lỗi hiếm hơn 1/6000 khi máy rảnh; nguyên nhân (một tiến trình khác giữ handle tệp trong thư mục)
  là **giả thuyết**, chưa đo trực tiếp.
- Ca hiện có `c17_ghi_nguyen_tu` canh hợp đồng "lỗi giữa chừng ⇒ `out` vắng hoặc giữ bản trước", không canh thử lại.
- `python -m ruff check --select F` trên hai tệp write set: `All checks passed!` (đo 01:40Z 21-11, `e02d748`).
  `ops/ci_provenance_test.py` có 133 dòng mục đột biến dạng `    ('` (đếm dòng, cùng thời điểm).

## 2. Write set — 2 đường

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `ops/ci_provenance.py` | M1–M3 |
| W2 | `ops/ci_provenance_test.py` | M4 |

Kích thước dự kiến: 2 tệp, khoảng 25 dòng thêm ở W1 và 50–120 dòng thêm ở W2.

## 3. Ngoài phạm vi

| thứ | lý do |
|---|---|
| thêm ngoại lệ Defender, đổi cấu hình máy Windows | phương án 2, chủ kho không chọn |
| thử lại cho lỗi `OSError` khác `PermissionError` | có thể che lỗi thật (đĩa đầy, đường dẫn sai) |
| thử lại trên Linux/macOS | đổi tên thư mục trên POSIX không hỏng thoáng qua kiểu này; giữ hành vi "hỏng là ném ngay" |
| sửa các `os.replace`/ghi tệp khác trong kho | chỉ `ghi_nguyen_tu` có bằng chứng lỗi |
| chạy cả bộ `ci_provenance_test.py` trên Windows (ADR-0060 M3) | chủ kho miễn, xem A6 và `pham_vi_e` |
| đánh giá lại A5 của #1322 | việc SAU land, không thuộc write set (xem `chua_do_duoc`) |

## 4. Mục tiêu

| # | mục tiêu | đường |
|---|---|---|
| M1 | Một hàm bọc duy nhất cho `os.replace` trong `ghi_nguyen_tu`, dùng cho CẢ BA lời gọi (a)(b)(c). Khi nền là Windows (`os.name == "nt"`) và lỗi là `PermissionError`, thử lại **tối đa 5 lần**, chờ trước lần thử lại thứ k (k = 0..4) là `0,05 × 2^k` giây (tổng chờ tối đa 1,55 s). Hết lượt thì ném **chính** `PermissionError` của lần cuối | W1 |
| M2 | Mọi lỗi khác `PermissionError`, và mọi lỗi trên nền khác Windows, ném ngay ở lần đầu, không ngủ | W1 |
| M3 | Hợp đồng cũ giữ nguyên: lỗi giữa chừng ⇒ `out` vắng hoặc giữ nguyên bản trước; thư mục tạm được dọn. Nền và hàm ngủ phải tiêm được từ test (tham số hoặc thuộc tính mô-đun), không vá `os.name` toàn cục | W1 |
| M4 | Ca tự kiểm mới trong W2 cho M1–M3, cùng các mục đột biến riêng trong `DOT_BIEN` theo hợp đồng `TinHieuChotCa` hiện có; mỗi chốt có một đột biến gỡ đúng chốt ấy làm ca đích ĐỎ | W2 |

## 5. Nghiệm thu

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | **Thử lại thành công, từng lời gọi.** Với nền Windows tiêm được: `os.replace` ở lời gọi (b) ném `PermissionError` k lần (k = 1 và k = 5) rồi thành công ⇒ `ghi_nguyen_tu` xong, `out` đúng nội dung mới, số lời gọi `os.replace` cho (b) là k+1. Ca riêng làm (a) ném 1 lần rồi thành công khi có bản trước. Ca riêng cho (c): (b) hỏng hẳn bằng lỗi không thử lại, (c) ném `PermissionError` 1 lần rồi thành công ⇒ bản trước được trả về `out` | đột biến bỏ thử lại (gọi `os.replace` thẳng) ⇒ ca ĐỎ; đột biến chỉ bọc (b), để (a) hay (c) gọi thẳng ⇒ ca ĐỎ (mỗi lời gọi một đột biến) |
| A2 | **Có giới hạn.** `os.replace` (b) ném `PermissionError` mãi ⇒ `ghi_nguyen_tu` ném `PermissionError`, đúng **6** lời gọi (1 + 5), đối tượng lỗi là của lần cuối; `out` vắng (không bản trước) hoặc giữ bản trước; không còn thư mục `.tam-` | đột biến nâng giới hạn (6 → 7 lời gọi) ⇒ ĐỎ; đột biến nuốt lỗi sau khi hết lượt ⇒ ĐỎ |
| A3 | **Chờ đúng.** Hàm ngủ tiêm được ghi lại các khoảng chờ: dãy với 5 lần thử lại là `[0.05, 0.1, 0.2, 0.4, 0.8]` | đột biến đổi hệ số hay bỏ ngủ ⇒ ĐỎ |
| A4 | **Chỉ `PermissionError`.** Trên nền Windows tiêm được, `os.replace` (b) ném `OSError` (errno khác EACCES, không phải `PermissionError`) ⇒ ném ngay, 1 lời gọi, 0 lần ngủ | đột biến bắt `OSError` thay `PermissionError` ⇒ ĐỎ |
| A5 | **Chỉ Windows.** Nền tiêm là không phải Windows, `os.replace` (b) ném `PermissionError` ⇒ ném ngay, 1 lời gọi, 0 lần ngủ | đột biến bỏ điều kiện nền ⇒ ĐỎ |
| A6 | **Windows thật** (ADR-0060 M3, phạm vi chủ kho chốt): trên DESKTOP-T9R33P2, hai vế (nền = base lease, ứng viên = head) dựng trong cùng một lệnh: `--mot-ca c17_ghi_nguyen_tu` ĐẠT cả hai vế; ca mới ĐẠT trên ứng viên; `L4_mode_step_key_truthy` qua `chay_dot_bien` lặp 5 lần mỗi vế ra `GIET` 5/5 trên ứng viên. **Chủ kho miễn** lượt chạy cả bộ của M3 (câu Q6, chat 21-11-2026) | ca nào không ĐẠT, hay L4 không `GIET` 5/5 trên ứng viên ⇒ ĐỎ; thiếu log hai vế ⇒ ĐỎ |
| A7 | **Không hồi quy Linux.** `python ops/ci_provenance_test.py` (chế độ mặc định) in `CA: x/x dat`, `DOT BIEN: y/y bi giet dung ly do` (hai số bằng nhau), `TONG: DAT`; `CI_DANG_KY ops/ci_provenance_test.py: ĐẠT` trên CI PR; `ruff --select F` delta 0 so base trên hai tệp | bất kỳ số nào lệch, hay `TONG: DO` ⇒ ĐỎ |

Trước khi đóng băng: A1–A5 đo hành vi mới nên đúng màu "chưa làm" trên base (chưa có hàm bọc; ca chưa tồn tại). A7 canh
bất biến và xanh sẵn trên CI master `e02d748` (run 44840271109 của `f77feb5` và lượt của `010046f`; đo lại khi cấp lease).
A6 chỉ đo được trên máy Windows của chủ kho.

## 6. `luat_dung`

- Điểm dừng của `docs/PROTOCOL_DA_PHIEN.md` §12; trần kích thước của `ADR-0053`; trần lời gọi Codex của `ADR-0055`;
  điều kiện merge của `ADR-0060`.
- **E2** khi chạm trần `ADR-0053` hay `ADR-0055`: mang theo mức đã dùng, còn thiếu bao nhiêu, để làm gì.
- **E2** nếu đo trên Windows cho thấy 5 lần thử lại không đủ (L4 vẫn ra `TIN_DUNG_GIA` vì `PermissionError` sau khi hết
  lượt): mang theo số đo, khoảng chờ đã dùng, đề xuất giới hạn mới. Không tự nới giới hạn.

## 7. `pham_vi_e`

- E4: **không chạm**.
- E5: **khai chạm** vì không rõ: `ops/ci_provenance.py` là công cụ thu provenance CI §10.2.2 mà hồ sơ land đọc; một lỗi ở
  đường ghi nguyên tử có thể để lại `out` sai. Theo `ADR-0067`, không rõ thì coi là thuộc ⇒ chủ kho duyệt băm đặc tả này.

## 8. `hinh_dang_ke_thua`

Packet khắc phục cho phát hiện Windows của #1322. Bảng lớp §8.3 của #1322 (verdict lượt 9,
`ops/reviews/pr1467-review-9-codex/VERDICT.md`) có bốn lớp, không lớp nào trùng cơ chế này; lớp gần nhất là
`loi-luong-nen-bi-tinh-la-giet-dung` (lỗi hạ tầng bị đổi thành `GIET`), đếm **7** biểu hiện F4..F4g ở #1322, đã đóng. Lỗi
ở đây ngược chiều: lỗi hạ tầng làm một đột biến đáng `GIET` thành `TIN_DUNG_GIA`. Đặt lớp mới
`loi-moi-truong-windows-doi-ten-thu-muc`, số biểu hiện bắt đầu ở **1** (lời gọi (b), lượt N=1 của #1322). Reviewer phải
quét đủ ba lời gọi (a)(b)(c) như CÙNG lớp.

## 9. `chua_do_duoc`

- Nguyên nhân gốc (tiến trình nào giữ handle lúc đổi tên): chưa đo; xem Defender bằng quyền admin không có trong phiên.
- 5 lần thử lại với tổng chờ 1,55 s có đủ cho mọi lần lỗi thật hay không: chỉ có một mẫu lỗi; A6 đo một phần.
- Kết quả vòng `c48` 30 lần trên `7c429aa`: còn chạy lúc soạn.
- A5 của #1322: đánh giá lại sau land (chạy lại `L4_mode_step_key_truthy` trên master mới, Windows), ghi bằng biên bản M8
  mới trên #1322 trỏ comment 7055070964.
