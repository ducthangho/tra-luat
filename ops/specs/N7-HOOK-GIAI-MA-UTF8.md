# ĐẶC TẢ ĐÓNG BĂNG — `N7-HOOK-GIAI-MA-UTF8`

Packet Issue: #418 · Nợ gốc: #412 · Khuyết tật họ hàng đã tách: #417

ĐỔI TÊN N6 -> N7 (10:1xZ 30-08-2026): `N6` ĐÃ BỊ CHIẾM bởi
`N6-LOI-KHAI-RONG-HON-PHEP-DO` (#411, nhánh `ops/dac-ta-n6-loi-khai`, có TRƯỚC packet này).
Đo bằng cách quét `ops/specs` trên MỌI ref, không chỉ master — cùng lý do `ops/leases` không
nằm một chỗ. Hai packet trùng số là hai hồ sơ không phân biệt được; đổi số là rẻ nhất.

Đặc tả này ĐÓNG BĂNG khi lease neo băm của nó. Sửa tệp này sau khi cấp lease là làm
`spec_hash` trỏ vào thứ không còn tồn tại — đường đi vòng qua §3.2, không phải sửa chính tả.

## 1. Vấn đề — nêu bằng phép đo, không bằng mô tả

`.claude/hooks/subagent_ghi_detect.py` giải mã byte UTF-8 bằng **codepage ANSI cũ** trên máy
chủ kho (`sys.stdin.encoding` = `locale.getpreferredencoding()` = `cp1258`, trong khi
`sys.getfilesystemencoding()` = `utf-8`).

Hai đường dính, ĐỘC LẬP nhau:

- `json.load(sys.stdin)` — payload harness bị méo ở trường `cwd`.
- `subprocess.run(..., text=True)` trong `_git()` — stdout của git bị méo ở `top`.

Hệ quả đo được (#412, bảng A/B một biến, chỉ đổi `PYTHONUTF8`):

```
                        MAC DINH        PYTHONUTF8=1
so duong da bam noi dung      0                  5
so duong MU                   6                  0
so dong status                5                  5
```

Máy phát hiện ghi **chưa từng phán quyết được điều gì** trên máy này — ghim ở `unknown`
mọi lượt.

## 2. Lối vá — B, ĐÃ CHỐT, không mở lại

1. `main()`: đọc `sys.stdin` dạng **byte** rồi `.decode("utf-8")` tường minh.
2. `_git()`: bỏ `text=True`, giải mã `p.stdout` bằng UTF-8 tường minh.

Lối A (`PYTHONUTF8=1` trong lệnh hook) **đã bị loại** ở #412: nó là biến môi trường, đúng lớp
*"đã đặt khác dùng được"*, và **im lặng** khi vắng. Lối B làm khuyết tật chết theo KIẾN TRÚC.

### 2.1 `errors=` — chọn khác nhau ở hai đường, có lý do

- Đường `_git()` ⇒ **`surrogateescape`**. `strict` sẽ biến một đường dẫn ngoài ASCII thành
  `unknown`, tức **tái tạo đúng sự mù** packet này sinh ra để chữa — chỉ đổi từ *méo âm thầm*
  sang *fail-close ồn ào*. Detector cần SO hai ảnh chụp; `surrogateescape` round-trip không
  mất byte nào nên hai ảnh so được.
- Đường stdin ⇒ **`strict`**. Payload không phải UTF-8 hợp lệ là lỗi THẬT, không phải chuyện
  locale. Hành vi hiện có (`except Exception: return 0`) GIỮ NGUYÊN — đổi nó là việc khác.

Ghi rõ vì dễ chép nhầm: #417 (`ops/lease_publish.py`) đối tượng là một **CỔNG**, ở đó `strict`
đúng hơn. Cùng lớp khuyết tật, hai lựa chọn ngược nhau, vì hai vai khác nhau.

## 3. Write set — ĐÚNG 2 tệp

```
.claude/hooks/subagent_ghi_detect.py
.claude/hooks/subagent_ghi_detect_test.py
```

KHÔNG `.claude/settings.json` (lối B không cần biến môi trường).
KHÔNG `ops/lease_publish.py` (đó là #417).

## 4. Tiêu chí nghiệm thu — bằng SỐ

`rc` của hook là `0` **kể cả khi mù** (D1 = CHỈ TỐ CÁO), nên `rc` không nghiệm thu được gì.
Ca phải đọc báo cáo và khẳng định hai trường có thật trong mã:

| trường | vị trí hiện tại | ngưỡng ĐẠT |
|---|---|---|
| `so_duong_da_bam_noi_dung` | `subagent_ghi_detect.py:333` | `> 0` |
| `mu_noi_dung` | `subagent_ghi_detect.py:104` | `len == 0` |

## 5. CHỐT BẮT BUỘC — ca chạy trên đường dẫn CÓ DẤU

Trên đường dẫn ASCII khuyết tật **vô hình**; ca đặt ở `/tmp/abc` sẽ XANH mà không đo gì.

Chọn ký tự có chủ đích — hai lớp KHÁC NHAU, và đây là chỗ dễ viết hụt nhất:

| lớp | ví dụ | byte tiếp diễn | cp1258 | hành vi |
|---|---|---|---|---|
| MÉO | `ố`(U+1ED1) `ộ`(U+1ED9) | `0x91` `0x99` | CÓ định nghĩa | méo, KHÔNG ném |
| Ô TRỐNG | `ề`(U+1EC1) `Ị`(U+1ECA) `ọ`(U+1ECD) `Ỏ`(U+1ECE) `ỏ`(U+1ECF) `Ố`(U+1ED0) `Ớ`(U+1EDA) `ờ`(U+1EDD) `Ở`(U+1EDE) | `0x81` `0x8a` `0x8d` `0x8e` `0x8f` `0x90` `0x9a` `0x9d` `0x9e` | Ô TRỐNG | ném (hoặc surrogate) |

Ca phải phủ **cả hai** lớp. `Quốc hội` chỉ chạm lớp MÉO — dùng một mình là đo hụt.

**BẢNG TRÊN SINH TỪ PHÉP ĐO, ĐỪNG GÕ TAY — và đây là chỗ đã sai một lần.** Bản đầu xếp `ớ`
THƯỜNG (U+1EDB) vào lớp Ô TRỐNG; sai, vì `ớ` là `e1 bb 9b` và cp1258 **có** định nghĩa `0x9b`
(U+203A). Chỉ `Ớ` **HOA** (U+1EDA, `0x9a`) mới là ô trống. Cross-review codex bắt đúng ô ấy
(P2 trên PR #420). Cùng lượt, tôi còn xếp nhầm `ở` THƯỜNG (U+1EDF, `0x9f` — **có** định nghĩa)
vào lớp ô trống ở thân PR #419 và trong một fixture.

Cặp hoa/thường lệch nhau đúng 1 byte và **chỉ một bản là ô trống**, nên mắt thường đọc không ra:

| cặp | THƯỜNG | lớp | HOA | lớp |
|---|---|---|---|---|
| ơ + sắc | `ớ` U+1EDB `0x9b` | MÉO | `Ớ` U+1EDA `0x9a` | Ô TRỐNG |
| ơ + hỏi | `ở` U+1EDF `0x9f` | MÉO | `Ở` U+1EDE `0x9e` | Ô TRỐNG |

Quy tắc sinh bảng (kiểm được, không trôi): với `e1 bb XX` thì codepoint là `U+1EC0 + (XX-0x80)`;
lớp Ô TRỐNG là đúng tập `XX` mà `bytes([XX]).decode("cp1258")` ném. Ai sửa bảng này phải sinh
lại bằng phép ấy rồi dán, đừng chọn ví dụ bằng trực giác.

## 6. Đột biến bắt buộc

Gỡ bản vá ⇒ ca đích **ĐỎ**. Không có đột biến ấy thì không biết ca đo khuyết tật hay đo thứ khác.

Chống **tín dụng giả** (#355/#359): mutant chết vì lỗi VÔ CAN (`AttributeError`, `TypeError`,
đường dẫn sai) **KHÔNG** tính là giết. Tín hiệu phải là assertion của ĐÚNG ca đích, và phải là
thứ mã triển khai không giả được.

## 7. Điều kiện dừng

- `S1` cần đường dẫn thứ ba ngoài write set ⇒ DỪNG, trình phép đo.
- `S2` phát hiện phải sửa `.claude/settings.json` ⇒ DỪNG (đó là lối A đã bị loại).
- `S3` ca chỉ chạy được trên Windows ⇒ khai THẲNG là ca chỉ-Windows; CẤM để nó im lặng `skip`
  trên Linux. Gợi ý `PYTHONCOERCECLOCALE=0` ở #412 **CHƯA ĐO** — không được chép thành đã
  chứng minh.
- `S4` `origin/master` đi tiếp so `base_sha` mà chưa đo lại ⇒ DỪNG.
- `S5` phát hiện phải đụng `ops/lease_publish.py` ⇒ DỪNG, đó là #417.

## 8. Chưa đo được — gọi tên tử tế, không làm tròn

- Vì sao vế A của A/B **chụp được** baseline (chỉ méo `top`) còn lượt harness THẬT lại `hong`
  — cùng chuỗi `cwd` méo, hai kết cục khác nhau. Biến còn lại là **ai phóng tiến trình**.
  Không tách được trong lượt đo của #412. KHÔNG đổi kết luận (cả hai đều tới `unknown`).
- Ca có dựng được trên CI Ubuntu bằng `LC_ALL=C` không — PEP 538/540 có thể tự nâng về
  `C.UTF-8` và biến ca ĐỎ-đáng-lẽ thành XANH.
