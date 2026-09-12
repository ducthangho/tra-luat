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

---

# BỔ SUNG SAU VÒNG 9 — bốn lời khai nữa, và cả bốn cùng MỘT nguyên nhân

| ID | nơi lời khai sai NẰM | khai sai | ĐÚNG | đã xử |
|---|---|---|---|---|
| `F6.11` | `F6-HO-SO.md` · `NO_KY_THUAT.md §23` · `TRANG_THAI.md` · spec `#530` rev 1 | `main()` có **hai** hình dạng in; `v6` lọt `4/4`, `v8` bắt `4/4` | `main()` có **BA** nhánh; `v8` loại **2/4**; trên **3** lớp vô can thật: `v6` lọt `3/3`, `v8` lọt `1/3` | sửa tại chỗ + spec lên **revision 2** |
| `F6.12` | cùng bốn nơi | hồi quy `v8` **có biên** `8/454`, 4 ca | mẫu số **493**; thêm **21** lời gọi tiền tố ĐỘNG trên **7 ca nữa** ⇒ **≥29 / ≥10 ca**, không quyết định được tĩnh. **RÚT** lời khai "có biên" | sửa tại chỗ |
| `N40` | `TRANG_THAI.md` | vòng 8 dài **813 s** | **812 s** | sửa tại chỗ |
| `N42` | `TRANG_THAI.md` | exclusion của `#513` là *"`#504` giữ"* | tệp spec ghi **`#503`**, lease `m9-fetch-auth-exec-1-claude-20260911` | sửa tại chỗ |

## Một nguyên nhân, không phải bốn lỗi rời

`F6.11` và `F6.12` cùng sinh từ **một** việc: tôi khớp regex với một **chuỗi TỰ GHÉP** (`f"{ten}: m"`)
thay vì **chạy lớp ngoại lệ thật qua `main()`**. Reviewer chạy thật và thấy ngay nhánh
`except BoQuaNen` mà mô hình của tôi không có.

Đó đúng lỗi `CLAUDE.md` gọi là *"NGHĨ RA được phép thử mà KHÔNG CHẠY nó thì phép thử ấy KHÔNG TỒN TẠI"* —
và trớ trêu là tôi mắc nó **ngay trong** một packet mà cả nội dung là về việc bộ đo nói dối. Tôi viết ra
một phép đo, thấy nó hợp lý, rồi **không chạy nó qua đường thật**.

`N42` là mặt khác của cùng thói: tôi chép con số từ **thân Issue** rồi **quy cho tệp spec**, không mở tệp
spec ra đọc. (Và lần này còn phát hiện thêm: **thân `#513` ghi `#504`, tệp spec ghi `#503`** — hai hiện
vật của cùng packet lệch nhau. Lỗi dẫn nguồn là của tôi; chỗ lệch là của `#513`, đã khai để người giữ biết.)

`N40` thì thuần cẩu thả: shell in `812s`, tôi viết `813 s`.

## Chốt rẻ, và nó là chốt duy nhất bắt được cả hai lớp trên

**Đừng khớp một phép đo với dữ liệu bạn tự dựng. Chạy nó qua đúng đường mà thứ thật sẽ đi.**
Với bộ đo này, "đường thật" nghĩa là: ném ngoại lệ **trong thân một ca**, để `main()` **thật** in ra, rồi
để **nguyên chương trình bộ đo** phân hạng. Mọi con số không đi qua đường ấy là **phỏng đoán**.
Spec `#530` revision 2 nay đặt đúng điều này thành ràng buộc của packet.
