tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# Đặc tả packet — `SUBPROCESS-UTF8-LEASE-PUBLISH` (revision 1)

| trường | giá trị |
|---|---|
| `packet_id` | `SUBPROCESS-UTF8-LEASE-PUBLISH` |
| `packet_issue` | #1331 |
| `revision` | 1 |
| `nguon_cap_viec` | #417, mở lại ở issuecomment-6906817113. Chủ kho chốt vòng hỏi `soan-spec` trong phiên điều phối #1206 ngày 16-11-2026 (Q1: P-A trong bốn packet; Q2: sửa cả lớp; Q6: executor Claude cloud, reviewer Codex, có lượt Windows). |
| `review_class` | `sensitive` (chạm `ops/lease_publish*`, là cổng đăng và thu hồi lease) |
| `base` | nhánh mặc định lúc cấp lease; số đo dưới đây lấy trên `a97a1ca` |

## 0. Vấn đề (đo 16-11-2026 04:2xZ, master `a97a1ca`)

1. **Lớp lỗi.** `ops/lease_publish.py` có đúng **9** lời gọi `subprocess.*`. Số này đếm bằng AST, tính mọi
   `ast.Call` có hàm bắt đầu bằng `subprocess.`. Trong 9 lời gọi ấy, **7** mang `text=True`, theo bảng sau:

   | dòng | hàm | tiến trình con |
   |---|---|---|
   | 70 | `GOI_GH` | `gh api …` (JSON comment/issue, có tiếng Việt) |
   | 1641 | `_repo_tam_co_lap` | `git init --bare` |
   | 1655 | `_tls_tu_git_https_linux` | `git --exec-path` |
   | 1659 | `_tls_tu_git_https_linux` | `/usr/bin/ldd` |
   | 1679 | `hoso_adapter_do` | `git version --build-options` |
   | 1780 | `kham_pha_nguon` | `git … ls-remote --symref` |
   | 1857 | `KhoObject._git_nguon` | `git -C <gốc> …` (đường dẫn, tên ref) |

   Hai lời gọi còn lại đọc bytes: `GOI_GIT` (dòng 76, đã sửa ở `803c248`) và `Popen` (dòng 1915).
2. **Đo trên Windows thật.** Máy `tra-luat-win`, Python 3.12, không đặt `PYTHONUTF8`, `preferred=cp1252`.
   Kịch bản mô phỏng đúng `GOI_GH` với một tiến trình con in JSON UTF-8. Đọc qua `text=True` thì nhận
   `"Tiáº¿ng Viá»‡t …"`, so khớp ra `False`, và **không có ngoại lệ nào**. Đọc bytes rồi decode UTF-8 thì
   khớp. Đặt `PYTHONUTF8=1` thì cả hai đường đều đúng. Bằng chứng: #417 issuecomment-6906817113.
3. Lỗi hỏng **âm thầm**: dữ liệu sai đi tiếp vào phép so khớp, không ai thấy. Đó là lý do phải đóng cả lớp
   chứ không vá từng chỗ.

## 1. `write_set`

```
ops/lease_publish.py
ops/lease_publish_test.py
```

## 2. `ngoai_pham_vi`

- Không sửa `subprocess` ở tệp nào khác: `.claude/dev/**`, `scripts/**`, các `ops/*.py` khác. Những tệp
  ấy thuộc lớp riêng. Packet này chỉ đóng lớp lỗi trong `ops/lease_publish.py` và ghi các chỗ còn lại vào
  `chua_do_duoc`.
- Không đổi thông điệp, mã thoát hay ngữ nghĩa của bất kỳ lệnh con nào trong `lease_publish.py`, trừ việc
  bắt buộc phát sinh từ chuyện decode lỗi (mục tiêu M2).
- Không chạm `.github/workflows/**`.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Cả 7 lời gọi ở mục 0 đọc **bytes** (không `text`/`encoding`/`universal_newlines`), rồi decode UTF-8 tường minh. Nên đi qua MỘT hàm dùng chung để luật nằm ở một chỗ. Nơi gọi nhận `str` như trước, và giữ `.replace("\r\n","\n")` ở đúng những chỗ hiện đang dựa vào chế độ text để chuẩn hoá xuống dòng (đối chiếu `GOI_GIT` dòng 76–80) | `ops/lease_publish.py` |
| M2 | Gặp byte không phải UTF-8 thì xử lý fail-closed. Với lời gọi nằm trong đường kiểm, tức lời gọi mà kết quả quyết định rc 0: ra `Chan(RC_KHONG_XAC_DINH, …)` hoặc nhánh lỗi sẵn có của nơi gọi, **không bao giờ** tiếp tục với chuỗi đã thay ký tự. Với lời gọi chỉ để chẩn đoán (`_tls_tu_git_https_linux` đã bắt `UnicodeError` và trả `None`): giữ hành vi trả `None` | `ops/lease_publish.py` |
| M3 | Chốt lớp: một ca test quét AST của `ops/lease_publish.py` và **đỏ** khi có bất kỳ lời gọi `subprocess.*` nào mang `text`, `encoding`, `errors` hay `universal_newlines` | `ops/lease_publish_test.py` |
| M4 | Mỗi lời gọi trong 7 lời gọi có một ca hành vi giả lập codepage. Theo kiểu `t25a` ở `.claude/hooks/subagent_ghi_detect_test.py:876`: thay `subprocess.run` bằng đồ giả trả `tho.decode("cp1252")` khi có `text=True`, trả bytes khi không. Ca đòi hàm đích trả đúng chuỗi UTF-8 có dấu (ví dụ đường dẫn `C:/tl-win/Quốc hội`, JSON có `Tiếng Việt`). Có thể gộp nhiều lời gọi vào một ca, miễn mỗi lời gọi có ít nhất một khẳng định riêng nêu tên hàm | `ops/lease_publish_test.py` |
| M5 | Ca fail-closed của M2: tiến trình con trả byte không phải UTF-8 trên một lời gọi đường kiểm (bắt buộc có `GOI_GH`/`kiem_github` và `_git_nguon`) ⇒ rc 12 hoặc nhánh lỗi tương đương, không ra rc 0 | `ops/lease_publish_test.py` |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Ca M3 xanh trên head | Đột biến: thêm `text=True` vào bất kỳ một trong 7 lời gọi, hoặc thêm `encoding="utf-8"` ⇒ ca M3 đỏ. Chạy đột biến cho ít nhất 2 vị trí khác nhau, trong đó có dòng của `GOI_GH`. Ca M3 phải đếm theo **từng lời gọi** và in danh sách vi phạm (L6c), không chỉ đếm tổng. |
| N2 | Các ca M4 xanh | Đột biến cho mỗi trong 7 lời gọi: trả về `text=True` ở đúng lời gọi đó (nếu đi qua hàm chung thì cho hàm chung nhận cờ `text` rồi bật ở đúng một nơi gọi) ⇒ ca M4 của lời gọi đó đỏ **ở đúng khẳng định nêu tên hàm**, không đỏ vì lỗi vô can. Cả 7 đột biến đều phải giết đúng lý do (bài học "đột biến bị giết không phải bị giết đúng lý do", CLAUDE.md). |
| N3 | Ca M5 xanh | Đột biến: decode với `errors="replace"` (hoặc `surrogateescape`) ở `GOI_GH`/`_git_nguon` ⇒ ca M5 đỏ vì rc 0 hoặc kết quả chứa ký tự thay thế. |
| N4 | `python -u ops/lease_publish_test.py` trên head ra **N/N** với hai số bằng nhau. N = số ca nền đo trên base lúc cấp lease (đo 16-11 trên `a97a1ca` qua CI: `lease_publish: 303/303 đạt`), cộng số ca mới. Ca đỏ vì môi trường phải được so với base và khai rõ. | Bất kỳ ca nào đỏ; hoặc hai số lệch nhau. |
| N5 | Catalog đột biến `t139` (nếu ca mới được đăng ký vào đó) không có tín dụng giả. | Đột biến chết vì lỗi vô can mà vẫn được đếm là giết. |
| N6 | **Windows native** trên `tra-luat-win`, theo ADR-0057/58/59 (khoá `KHOA.txt` 5 trường, nhịp tim ≤ 30 phút, thư mục `C:\tl-win\<session_id>\`). Chạy **không** `PYTHONUTF8` và **không** `PYTHONIOENCODING`, Python 3.12: toàn bộ ca mới (M3–M5) cộng `t129`, `t133`, `t137`, `t151` xanh. Có thêm một phép đo vế âm: cùng ca M4 trên mã **base** (7 lời gọi còn `text=True`) phải ĐỎ trên máy ấy. | Ca mới đỏ trên Windows. Hoặc vế âm trên base lại xanh, nghĩa là ca không đo được codepage thật. |
| N7 | `adr-song` và `doctrine-scan` rc 0. Ruff `--select F` trên hai tệp: delta so với base bằng 0. | rc khác 0, hoặc delta lớn hơn 0. |
| N8 | CI Ubuntu trên head xanh, và gate hậu merge đủ bốn mốc §10.2.2. | Đọc nhãn job và log, không đọc kết luận tổng. |

Chạy thử trên nền (base `a97a1ca`, trước khi đóng băng): M3–M5 là hành vi mới nên không tồn tại trên nền,
tức đang ở màu "chưa làm". Vế âm của N6 chính là phép đo màu đỏ của nền.

## 5. Kích thước và trần

- Dự kiến 2 tệp: khoảng 25–40 dòng sửa trong `lease_publish.py` và khoảng 120–200 dòng thêm trong test.
  Trần `ADR-0053` là ≤ 6 tệp và ≤ 450 dòng thêm, đo bằng `git diff --numstat <base>...HEAD`.
- Lời gọi Codex: theo trần mà `ADR-0055` chọn qua dòng khai ở đầu tệp. Đếm **trước** mỗi lời gọi, kể cả
  lượt connector tự chạy khi bỏ draft.

## 6. `luat_dung`

- Vượt trần `ADR-0053` thì dừng và nén. Muốn nâng trần thì đó là quyết định của chủ kho (E2), mang theo
  số đo `numstat` và danh sách ca.
- Chạm trần lời gọi Codex của `ADR-0055` thì theo luật của ADR ấy (E2).
- Lượt Windows (N6) không chạy được, vì máy offline hoặc khoá do phiên khác giữ: không merge. Ghi trạng
  thái `KHÔNG ĐO ĐƯỢC` và để phiên điều phối tự quyết thời điểm thử lại; đây không phải điểm hỏi chủ kho.

## 7. `pham_vi_e`

Không chạm E4, không chạm E5. Packet sửa cách đọc output của tiến trình con, không đổi thẩm quyền, không
đổi luật đăng hay thu hồi lease.

## 8. `hinh_dang_ke_thua`

Từ #417 và `803c248`. Lỗi này là **"vá đúng chỗ được chỉ rồi bỏ sót đường thứ hai, thứ ba"** (CLAUDE.md,
bài học 12-09). Bản vá `803c248` sửa `GOI_GIT` nhưng để sót 7 lời gọi cùng lớp; lượt rà 16-11 lúc đầu
còn đếm nhầm thành 6, vì grep theo dòng bỏ qua một lời gọi viết trải nhiều dòng. Vì vậy tiêu chí lớp N1
là phép quét AST, không phải grep. Đếm hình dạng lỗi: **lần thứ 2** cùng lớp trong tệp này.

## 9. `chua_do_duoc`

- Lớp `subprocess(text=True)` ở các tệp ngoài write set (`.claude/dev/launcher.py`,
  `.claude/dev/packet_loop.py`, `scripts/*.py`, các `ops/*.py` khác): **chưa đếm**. Nếu cần thì mở
  packet riêng.
- Lời gọi dòng 1655 và 1659 chỉ chạy trên Linux (`sys.platform.startswith("linux")`), nên trên Windows
  không có đường thật để đo. Phép đo của hai lời gọi này chỉ là đồ giả ở M4.
- `gh` không cài trên `tra-luat-win` (chưa đo). N6 đo bằng đồ giả và bằng tiến trình con Python in
  UTF-8, không bằng `gh.exe` thật.
