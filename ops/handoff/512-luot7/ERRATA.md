# ERRATA — các lời khai số SAI của phiên tác giả, và chỗ chúng nằm

**Vì sao có tệp này:** một số lời khai sai nằm trong **hiện vật lịch sử** — prompt đã giao cho reviewer,
thông điệp commit đã đẩy. Sửa byte của chúng là **làm giả hồ sơ**: reviewer vòng sau sẽ không còn đo lại
được thứ mà reviewer vòng trước đã đọc. Nên chúng được đính chính **ở đây**, không sửa tại chỗ.
Reviewer vòng 8 nói đúng yêu cầu: *"Chỉ yêu cầu bổ sung đính chính, không sửa lịch sử."*

Tệp **sống** (`TRANG_THAI.md`, `F6-HO-SO.md`) thì sửa TẠI CHỖ, kèm một khối `ĐÍNH CHÍNH` ngay cạnh giữ
lại giá trị sai — giấu giá trị sai đi cũng là làm mất hồ sơ.

| ID | Nơi lời khai sai NẰM | Khai sai | ĐÚNG | Đã xử |
|---|---|---|---|---|
| `N31` | thông điệp commit `36f68c7`, **tiêu đề** | "5 mutant sống" | **6** (`N01 N02 N10 N12 N17 N18`) | ĐÍNH CHÍNH tại đây; commit giữ nguyên |
| `N31-b` | `PROMPT.rvwin512-7.md:49` (hiện vật lịch sử) | "năm mutant vòng 6 thấy SỐNG" rồi liệt kê sáu ID | **6** | ĐÍNH CHÍNH tại đây; prompt giữ nguyên byte |
| `N32` | thông điệp commit `36f68c7` | `+1114/−27`, "dư 386" | **+1101/−27**, dư **399** | ĐÍNH CHÍNH tại đây |
| `N32-b` | `TRANG_THAI.md` hàng numstat và mục `A5` | `+1114`, số hạng `1076+32`, `1114 > 300` | **1095 + 6 = 1101** | **đã sửa tại chỗ** + khối ĐÍNH CHÍNH |
| `N37` | `TRANG_THAI.md` §CẬP NHẬT VÒNG 7 | "~8,5 phút" | **895 s = 14 ph 55 s** | **đã sửa tại chỗ** |
| `N38` | `TRANG_THAI.md` bảng bảy lớp, hàng F7 | F7 "SỐNG 6/6 / CHẾT 6/6" | F7 có **năm** phần tử ⇒ **5/5**; `N10` thuộc **F2** | **đã sửa tại chỗ** |
| `N39` | `TRANG_THAI.md` §Việc kế tiếp | "sẽ là 7/10 sau khi phóng" | **8/10** sau khi phóng | **đã sửa tại chỗ** |

## Ba hình dạng, không phải bảy lỗi rời

- **Chép lại thay vì đo lại** (`N31`, `N31-b`, `N32`, `N32-b`): con số `5` và `1114` được chép từ hồ sơ
  lượt trước hoặc suy bằng phép cộng nhẩm. Chốt rẻ: mỗi con số trong một tệp phải kèm **lệnh đã sinh ra
  nó**, và lệnh ấy phải chạy lại được.
- **Ghép sai đồng hồ / sai tập** (`N37`, `N38`): `510s` là của bộ theo dõi, không của lượt chạy; `6` là
  của `F2 ∪ F7`, không của `F7`. Cả hai là **lấy số đúng của một thứ rồi gán cho thứ khác** — đúng bệnh
  mà `CLAUDE.md` gọi là *ghép sai lượt*.
- **Trạng thái trước/sau một hành động** (`N39`): `7/10` đúng **trước** khi phóng, sai **sau**.

## Và lời cảnh báo đắt nhất của cả lượt

`N32` sống sót **hai vòng review**. Lý do: câu mang nó vừa nêu **số hạng** vừa nêu **quan hệ**, và
**quan hệ vẫn đúng** — `1101 ≤ 1500` đúng, `1101 > 300` đúng, y như với `1114`. Ba lượt đọc qua mà không
ai dừng, vì soi tính nhất quán nội tại thì câu ấy **sạch hoàn toàn**.

`CLAUDE.md` đã ghi chính bài học này (`117/100 chênh 10`). Nó vẫn bắt được tôi. Chốt thực hành:
**khi một câu vừa nêu số hạng vừa nêu quan hệ giữa chúng, kiểm SỐ HẠNG — quan hệ là thứ sống sót qua trôi số.**
