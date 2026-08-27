verdict: changes_requested
reviewed_sha: f461413a03b3a28ebdacde1fa17f49c894223682
reviewer: claude (cross-review vòng 4, packet #319, PR #339)

## 0. Khả năng chạy mã và nền đo

- `python3 --version` → `Python 3.11.15`; `python3 -c 'print("PROBE_OK")'` → in được. **Chạy mã ĐƯỢC** — không `blocked`.
- `git status --porcelain` rỗng; `HEAD` đúng `f461413a03b3a28ebdacde1fa17f49c894223682`, base `ac82ddc5` là tổ tiên (log `git log --oneline -5` xác nhận nhánh).
- **Nền `bind` loopback: CÓ.** Thử `socket.bind(('127.0.0.1', 0))` → thành công (`BIND_OK ('127.0.0.1', 42383)`). Khác với sandbox `codex` (từ chối `PermissionError`). Chạy `python3 .claude/dev/mcp_gh_test.py` cho `CA 40/40 đạt · 0 đỏ`, `ĐỘT BIẾN 48/48 tập giết`, `D8(a)(b)(c) ĐẠT`, `TỔNG: ĐẠT`, `rc=0` — khớp con số executor báo trong commit r6 (`CA 40/40 đạt · 0 đỏ · ĐỘT BIẾN 48/48 · TỔNG: ĐẠT · rc=0`). D7b không kích hoạt ở nền này.

## 1. P1 vòng 3 đã đóng THẬT chưa

**Trả lời ngắn: ĐÓNG MỘT PHẦN.** Đúng bug được nêu ở vòng 3 (workaround tự chiếu thay `d8_errors` bằng giá trị dựng sẵn) đã bị gỡ sạch — `grep` không còn dấu vết cờ tự chiếu kiểu cũ. Nhưng **cùng một TRIỆU CHỨNG** (bản in có dòng ĐỎ mà mã thoát/TỔNG vẫn xanh) **vẫn dựng lại được**, qua hai đường KHÔNG nằm trong disclaimer của đặc tả.

### Bảng đột biến của tôi (chạy thật, sửa theo SỐ DÒNG, không theo chuỗi)

Tất cả chạy bằng cách copy `mcp_gh.py` + `mcp_gh_test.py` đã sửa MỘT dòng theo chỉ số vào thư mục tạm riêng, rồi `python3 mcp_gh_test.py` trong thư mục đó.

| # | đột biến (yêu cầu của lượt review) | dòng | BỊ GIẾT hay SỐNG SÓT | bằng chứng |
|---|---|---|---|---|
| 1 | ép mã thoát trả hằng số 0 (`ma_thoat`: `return 0 if xanh else 1` → `return 0`, dòng 381) | 381 | **BỊ GIẾT ở mức CA** (2 ca đỏ: `D10-main`, `D11-gate`), TỔNG in đúng `ĐỎ` — **nhưng tiến trình `rc=0`** | `CA: 38/40 đạt·2 đỏ·ĐỎ` / `ĐỘT BIẾN: KHÔNG_ĐO_ĐƯỢC (nền đỏ)` / `TỔNG: ĐỎ` / `PROCESS_EXIT_CODE=0` |
| 2 | làm `phan_dinh` luôn trả xanh (dòng 377: `return not any(...)` → `return True`) | 377 | **SỐNG SÓT ở mức TỔNG/rc** — báo cáo TỰ MÂU THUẪN | `CA: 39/40 đạt·1 đỏ·ĐỎ` + dòng `ĐỎ D11-gate: AssertionError` **cùng file** với `TỔNG: ĐẠT`, `PROCESS_EXIT_CODE=0` |
| 3 | thân vòng lặp `chay_cac_ca` → `pass` (dòng 606-611) | 606-611 | **BỊ GIẾT sạch** | `CA: 0/40 đạt·ĐỎ`, D8(a)(b) liệt 47 tên ĐỎ, `TỔNG: ĐỎ`, `rc=1` |
| 4a | xoá dòng `lines += dong_d8(...)` (dòng 660) | 660 | **BỊ GIẾT** | `CA: 39/40·1 đỏ·ĐỎ`, `TỔNG: ĐỎ`, `rc=1` |
| 4b | xoá dòng `lines.append("TỔNG: ...")` (dòng 664) | 664 | **BỊ GIẾT** (không có dòng TỔNG nào được in, nhưng `rc=1` đúng vì `ma_thoat(xanh)` không phụ thuộc dòng in) | `rc=1`, không dòng TỔNG |
| 4c | xoá dòng `print(...)` (dòng 665) | 665 | **BỊ GIẾT** (không in gì cả, nhưng `rc=1` đúng) | `rc=1`, stdout rỗng |
| 5 | hard-code **hậu tố** dòng `CA` thành `"ĐẠT"` cứng (bỏ `_du_ca(...) and not failed`, dòng 657) | 657 | **SỐNG SÓT HOÀN TOÀN** qua cả 48 đột biến chính thức | `CA 40/40 đạt·0 đỏ·ĐẠT`, `ĐỘT BIẾN 48/48·ĐẠT`, `D8(a)(b)(c) ĐẠT`, `TỔNG: ĐẠT`, `rc=0` |
| 6 | hard-code **hậu tố** dòng `ĐỘT BIẾN` thành `"ĐẠT"` cứng (bỏ biến `ok`, trong `dong_dot_bien`) | ~450-451 | **SỐNG SÓT HOÀN TOÀN** qua cả 48 đột biến chính thức | y hệt trên: `48/48·ĐẠT`, `TỔNG: ĐẠT`, `rc=0` |

### Trả lời thẳng: bản in và mã thoát có còn mâu thuẫn nhau được nữa không?

**CÓ, dựng được cảnh cụ thể — hai cảnh khác nhau:**

- **Cảnh A (đột biến #2, `phan_dinh` hỏng):** chạy `python3 mcp_gh_test.py` trong `mut/m2_phan_dinh_luon_xanh/`, output là:
  ```
  CA         : 39/40 đạt · 1 đỏ · ĐỎ
    ĐỎ D11-gate: AssertionError: 
  ...
  TỔNG: ĐẠT
  ```
  Đây là **CÙNG MỘT BẢN IN** — dòng thứ hai nói case đỏ, dòng cuối nói TỔNG ĐẠT. `$? == 0`. Bất kỳ ai chỉ đọc dòng cuối hoặc chỉ đọc `$?` sẽ bị lừa y hệt bug vòng 3, dù `d8_errors` không còn bị thay bằng giá trị dựng sẵn nữa — lỗ chỉ chuyển từ "TỔNG suy từ rc" sang "TỔNG/rc cùng suy từ MỘT hàm (`phan_dinh`) mà hàm đó tự nó không có gì canh".
- **Cảnh B (đột biến #1, `ma_thoat` hỏng):** TỔNG đúng nói ĐỎ (báo cáo tự nhất quán), nhưng **tiến trình `python3 mcp_gh_test.py; echo $?` trả về `0`**. Với ai/gate nào (giả sử tương lai có) chỉ hỏi `$?` mà không đọc chữ, đây vẫn là "cổng xanh nhờ rc=0 có thể bị lừa" — đúng câu doctrine của kho.
- **Cảnh C (đột biến #5 và #6, hậu tố CA/ĐỘT BIẾN bị hard-code):** không cần tạo ra bất kỳ ca thật nào bị lỗi — chỉ cần khoá cứng đúng HAI DÒNG mà chính commit r6 khai là tính năng mới của D11 ("hậu tố ĐẠT/ĐỎ trên dòng CA và dòng ĐỘT BIẾN") — và **toàn bộ 48 đột biến + D8(a)(b)(c) đều báo ĐẠT, `rc=0`**, không một ca nào trong sổ 40 ca phát hiện ra. Đây là cảnh nguy hiểm nhất vì nó không cần một lỗi nền nào cả — chỉ cần đúng 2 dòng bị âm thầm khoá cứng là toàn bộ cổng mù vĩnh viễn với MỌI lỗi tương lai mà chỉ lộ qua hậu tố đó.

**Kết luận:** P1 vòng 3, theo đúng CHỮ (dòng bug cụ thể mà vòng 3 chỉ ra) đã được vá. Nhưng theo đúng Ý (bản in và mã thoát không còn mâu thuẫn được) thì **CHƯA đóng** — cùng một hình dạng lỗi tái sinh ở ba chỗ khác, hai trong số đó (#5, #6) hoàn toàn không có phản chứng.

## 2. Chất vấn thang điểm — `D10`/`D11` của r4 có đủ chặt không

**Bản thân TIÊU CHÍ (bảng D10/D11 + điều cấm CHỐT TỰ CHIẾU) là chặt và đúng hướng** — chính điều cấm ấy ("xoá bất kỳ dòng nào của cơ chế D11 mới phải làm ĐỎ một ca CÓ TÊN — không được có dòng nào trong cơ chế mà xoá đi vẫn xanh") là công cụ tôi dùng để tìm ra đột biến #5/#6 ở trên. Đặc tả không sai ở chỗ này.

**Nhưng câu khai "D11 KHÔNG hứa điều không hứa được" — SAI VỀ SỐ, không sai về NGUYÊN LÝ.** Nguyên văn: *"Dòng ngoài cùng nhất — `sys.exit(chay_cli())` — vẫn có thể sửa thành `sys.exit(0)`... `D11` thu hẹp bề mặt ấy xuống MỘT DÒNG DUY NHẤT."* Tôi đo được **ít nhất BỐN dòng khác**, không phải một, cùng có tính chất "sửa xong vẫn xanh":
1. `ma_thoat`'s body (dòng 381) — có đăng ký trong `MUTATIONS` (`d11_ep_rc_xanh`) và "bị giết" **khi áp trong bản sao cô lập của `chay_dot_bien`**, nhưng khi CHÍNH DÒNG NÀY hỏng trong tệp thật (không phải bản sao), `rc` tiến trình vẫn sai (Cảnh B).
2. `phan_dinh`'s body (dòng 377) — tương tự, đăng ký (`d11_phan_dinh_xanh`) nhưng khi hỏng trong tệp thật, TOÀN BỘ báo cáo tự mâu thuẫn (Cảnh A).
3. Hậu tố dòng `CA` (dòng 657) — **KHÔNG có đăng ký nào trong `MUTATIONS`**, sống sót tuyệt đối.
4. Hậu tố dòng `ĐỘT BIẾN` (trong `dong_dot_bien`) — **KHÔNG có đăng ký nào trong `MUTATIONS`**, sống sót tuyệt đối.

Vậy: đặc tả **KHÔNG SAI** (tiêu chí đủ chặt để tự nó bắt được lỗ nếu áp dụng triệt để), nhưng **THIẾU** ở chỗ khai bề mặt còn lại — con số "một dòng duy nhất" là một khẳng định thực nghiệm sai, không phải một quyết định thiết kế. Vì đây là câu tường thuật (không phải một dòng trong bảng `nghiem_thu` có phép đo riêng), tôi không quy đây thành "đặc tả sai" đủ để `blocked` — nhưng người giữ kho cần biết con số đó sai trước khi tin tưởng phần "chua_do_duoc" còn lại của tài liệu.

## 3. Bảng chấm A/B/C/D

| hạng | trạng thái | ghi chú |
|---|---|---|
| A (đích credential, A1-A11) | **ĐẠT**, đã chạy thật với `bind` sẵn, 48/48 tập giết bao gồm cả A5-A7 (301/302/303/307/308) | không có gì mới để nghi ngờ ở hạng này lượt này |
| B (9 bất biến B1-B9 + B7 4 lớp) | **ĐẠT** khi chạy trong nền `bind` được | không đổi so với các lượt trước, không nằm trong write set thay đổi của r6 |
| C (sổ ca bất biến C1-C4) | **ĐẠT hình thức**, nhưng `cong()` (hàm C1-C4/D7 kiểm) **không còn được `chay_cli` gọi trực tiếp** — chỉ hai hàm con `_du_ca`/`_co_dot_bien` của nó mới thực sự nằm trên đường chạy thật. Không phải lỗi, nhưng đáng ghi vì có thể là đúng thứ P2 vòng 2 `c4-khong-bat-duoc-ca-vo-hieu-tren-du-lieu-that` đang nói tới — tôi không có văn bản gốc của P2 đó để đối chiếu chắc chắn (xem mục 5) |
| D (D1-D11) | **ĐỎ ở D10, D11** theo phép đo của tôi — xem mục 1, 2. D1-D9 không đổi so với baseline đã biết, D9 = 900/900 (biên 0, đúng như executor khai) |

## 4. Finding mới

### `hau-to-dat-do-moi-cua-ca-va-dot-bien-khong-co-dot-bien-canh` — **P1**
TỆP/DÒNG: `.claude/dev/mcp_gh_test.py:657` (hậu tố dòng `CA`) và trong `dong_dot_bien` (dòng ~450-451, hậu tố dòng `ĐỘT BIẾN`).
VẤN ĐỀ: Hai hậu tố `ĐẠT`/`ĐỎ` này là phần MỚI mà chính commit r6 khai là cách "mọi điều kiện cũ của `ma_thoat()` nay xuất hiện THÀNH DÒNG BÁO CÁO". Không dòng nào trong hai chỗ này có đột biến riêng trong bảng `MUTATIONS`. Vi phạm trực tiếp điều cấm "CHỐT TỰ CHIẾU" của chính đặc tả r4: *"không được có dòng nào trong cơ chế mà xoá đi vẫn xanh"*.
ĐÃ THỬ VÁ: không — thuộc phạm vi vá của executor.
ĐÃ THỬ NGHIỆM: hard-code cả hai hậu tố thành `"ĐẠT"` (bỏ toàn bộ điều kiện phía sau `+`), chạy `python3 mcp_gh_test.py` — cả hai lần đều cho `CA 40/40 đạt·0 đỏ·ĐẠT`, `ĐỘT BIẾN 48/48·ĐẠT`, `D8(a)(b)(c) ĐẠT`, `TỔNG: ĐẠT`, `rc=0`. Tái lập 100% (đã chạy 2 lần độc lập).
ĐỘ TIN: cao — đo trực tiếp, không suy diễn.
HẬU QUẢ: kết hợp với bất kỳ lỗi nào khiến `main`/`chay_cli` không thực sự chạy hết sổ ca theo cách KHÔNG ném exception (chính là điều D10 sinh ra để chặn — "một `main` trả 0 mà không gọi ca nào"), gate sẽ mù hoàn toàn vì tín hiệu duy nhất còn lại (hậu tố CA) đã bị khoá cứng.

### `d10-main-la-menh-de-luon-dung-khong-con-do-hanh-vi-main` — **P1**
TỆP/DÒNG: `.claude/dev/mcp_gh_test.py:503-504` (`d10_main_khong_chay_ca_phai_do`).
VẤN ĐỀ: So với bản trước r6 (`assert ma_thoat((("c", None),), (), mutants, (), (), ((), (), ())) == 1` — dựng cảnh sổ ca có tên nhưng chưa chạy), bản r6 thoái hoá thành `assert ma_thoat(False) == 1` — một khẳng định về hành vi hai dòng của `ma_thoat(xanh)`, không còn dựng bất kỳ cảnh "main không gọi ca" nào, không kiểm cờ đã đặt như chính D10 trong bảng `nghiem_thu` đòi ("đòi CẢ HAI: mã thoát khác 0 VÀ cờ đã được đặt"). Đột biến `d10_main_luon_xanh` gán cho D10-main **giống hệt byte-for-byte** đột biến `d11_ep_rc_xanh` của D11-gate (cùng tệp, cùng chuỗi cũ, cùng chuỗi mới) — D10 không có đột biến riêng của nó, chỉ ăn theo D11.
ĐÃ THỬ VÁ: không.
ĐÃ THỬ NGHIỆM: so sánh trực tiếp hai dòng trong bảng `MUTATIONS`:
`("d10_main_luon_xanh", "test", "return 0 if xanh else 1", "return 0", "D10-main")` và
`("d11_ep_rc_xanh", "test", "return 0 if xanh else 1", "return 0", "D11-gate")` — xác nhận trùng.
ĐỘ TIN: cao.
Ghi nhận: chính commit r6 cũng tự khai mục này trong phần "CON MỞ" — không phải điều tôi phát hiện độc lập hoàn toàn, nhưng lượt review này XÁC NHẬN bằng đo và LIÊN KẾT nó với finding #1 ở trên: D10 xuống cấp + hậu tố CA không có phản chứng = TOÀN BỘ mục tiêu ban đầu của D10 (chặn "main trả 0 mà không gọi ca nào") hiện không có phản chứng nào canh giữ đầu-cuối.

### `d9-dong-tieu-chi-van-mo-ta-numstat-tren-write-set-nhung-ma-do-tong-dong-hai-tep-ma` — **P2** (kế thừa từ vòng 2, vẫn mở)
TỆP/DÒNG: `ops/specs/mcp-gh-cuu-ho.md`, dòng bảng `D9` trong mục `nghiem_thu` (*"Ngân sách: `git diff --numstat` trên write set, cột dòng THÊM..."*) đối chiếu với `.claude/dev/mcp_gh_test.py:499-500` (`sum(sum(1 for _ in path.open(...)) for path in (NGUON, pathlib.Path(__file__)))`).
VẤN ĐỀ: dòng tiêu chí mô tả "numstat, cột THÊM, trên WRITE SET" (3 tệp, số dòng thêm theo diff); mã đo TỔNG SỐ DÒNG HIỆN TẠI của 2 TỆP MÃ (không phải diff, không tính tệp đặc tả). Mục "Ngân sách — ĐỔI ĐƠN VỊ ĐO ở r3" phía dưới giải thích đơn vị mới nhưng dòng bảng D9 gốc chưa được sửa theo. Đây rất có thể là đúng slug vòng 2 `d9-do-thu-khac-han-thu-D9-noi` (tôi không có văn bản gốc để xác nhận 100%, xem mục 5).
ĐÃ THỬ VÁ: không — không thuộc write set thay đổi của lượt này (mcp_gh_test.py có đổi nhưng d9 test thân không đổi ở r6).
ĐÃ THỬ NGHIỆM: đọc trực tiếp cả hai đoạn văn bản, đối chiếu; `wc -l` xác nhận 230+670=900 khớp d9 test hiện tại.
ĐỘ TIN: vừa (khớp nội dung, không khớp được với văn bản P2 gốc).

## 5. CHỖ KHÔNG ĐO ĐƯỢC

- **5 P2 vòng 2 + 2 P2 vòng 3**: tôi không đọc được `ops/reviews/mcp-gh-cuu-ho-kiem-doc-lap-va-P1-vong3.md` (nhánh `ops/cap-lease-tach-314` không có trong clone này — `git branch -a` chỉ thấy `claude/mcp-gh-cuu-ho-exec-1`). Với slug `b7-xoa-khong-tai-hien-co-che-pyc-ma-no-khai` và `rut-van-ban-bo-content-1-tro-di`: cả hai chạm phần `mcp_gh.py`/hàm B7, và **r6 không đổi các phần đó** (numstat r6 chỉ đổi `mcp_gh_test.py`, và trong đó không đổi các hàm `b7_*`/`rut_van_ban`) — nên hai P2 này **không bị ảnh hưởng bởi lượt này**, coi như còn nguyên trạng thái cũ, KHÔNG ĐO LẠI được nội dung gốc của chúng ở đây. Với `so-lieu-dong-bang-cua-dac-ta-da-troi...`: số hiện tại (900/900) tự nhất quán, nhưng tôi không có bản gốc P2 để xác nhận đây có phải đúng điều họ từng chỉ ra hay không. Với 2 P2 vòng 3: không có slug được cấp trong đề bài, không đoán được nội dung — **KHÔNG ĐO ĐƯỢC**.
- **Trạng thái GitHub/CI thật của PR #339** (checks, review chính thức trên GitHub): không có `gh`, không gọi MCP GitHub trong lượt review này (đề bài không yêu cầu đăng lên PR, chỉ ghi file) — KHÔNG ĐO.
- **`cong-la-ham-chet` (mục 3, hạng C):** tôi xác nhận `cong()` không được gọi trong `chay_cli`, nhưng KHÔNG xác nhận được đây có đúng là ý của P2 vòng 2 `c4-khong-bat-duoc-ca-vo-hieu-tren-du-lieu-that` hay không — thiếu văn bản gốc.

## 6. Việc 3 — nợ "không cổng nào chạy tệp test này"

Nợ này **vẫn mở, và đúng như đề bài gợi ý: mở nợ là ĐỦ cho hiện tại nhưng không được đọc thành "vô hại".** Ba finding P1 ở mục 4 đều là loại lỗi mà nếu MỘT gate CI/pre-commit tương lai tin vào `$?` của tệp này, sẽ **bị lừa hoàn toàn** trong ít nhất hai cảnh (đột biến #1, #5, #6) mà không cần bất kỳ ca thật nào thất bại theo nghĩa "raise Exception". Nợ càng lâu mở, càng dễ có người nối gate vào và tin nhầm. Khuyến nghị: nợ có thể tiếp tục mở cho packet NÀY (đúng luật "chỉ P1 mới chặn land", và nợ tự nó không phải P1 mới) nhưng **ba finding P1 ở mục 4 thì có** — chúng nằm trong write set của chính lượt này (`mcp_gh_test.py`), không phải nợ ngoại lai.

## Kết luận

`changes_requested`. Không có gì cho thấy đặc tả r4 sai hoặc thiếu ở mức phải `blocked` — tiêu chí D10/D11 và điều cấm chốt tự chiếu ĐÚNG HƯỚNG và đủ sắc để tự bắt được lỗ (tôi dùng chính điều cấm đó để tìm finding #1). Vấn đề nằm ở **thi công chưa đạt bar mà chính đặc tả đặt ra**: hai dòng hậu tố mới (CA, ĐỘT BIẾN) không có phản chứng nào — sống sót 100% qua bộ 48 đột biến hiện có — và D10 đã thoái hoá thành mệnh đề luôn đúng, ăn theo đột biến của D11 thay vì có phản chứng riêng. Câu khai "D11 thu hẹp bề mặt xuống một dòng duy nhất" trong đặc tả cần sửa lại cho khớp số đo (ít nhất năm dòng, không phải một), dù đây là ghi chú tường thuật chứ không phải tiêu chí có phép đo riêng nên tôi không tính là lý do `blocked`.
