# `MCP-GH-CUU-HO` (#319) — KIỂM ĐỘC LẬP bản vá P1 vòng 3 (chốt D11)

**Đây KHÔNG phải verdict review.** Đây là phép đo của phiên điều phối, chạy lại bằng tay để
KHÔNG chuyển tiếp báo cáo của executor mà không kiểm.

- Neo đã commit: `97617d3a5372fcce39b0e53064958c24d15775ce` (ba P1 vòng 2 — đã xác minh ĐẠT).
- Bản vá đang xét: CHƯA COMMIT, 56 dòng diff trên `.claude/dev/mcp_gh_test.py`,
  `sha256(diff) = 3e564de0e26efede9e9b0d5f4668f42460640398862992d8d4aca626d515ff75`.
- Ngân sách sau vá: `230 + 670 = 900/900`. Biên còn **0**. Ca `D9` tự bắn đỏ nếu thêm bất kỳ dòng nào.

## Kết luận một dòng

**P1 vòng 3 CHƯA ĐÓNG.** Bản vá làm cổng đỏ đúng một kịch bản, nhưng đổi lấy một dòng báo cáo SAI,
và bản thân cái chốt KHÔNG có phản chứng nào.

## Phép đo

Đột biến áp theo SỐ DÒNG (không theo chuỗi) — vì hai chuỗi đích nay xuất hiện HAI lần trong tệp
(một lần là mã thật, một lần là dữ liệu trong bảng `MUTATIONS`), nên đột biến theo chuỗi trả
`KHÔNG_ĐO_ĐƯỢC`. Mỗi lần chạy: sao hai tệp sang thư mục tạm, sửa dòng, chạy `python3 mcp_gh_test.py`.

| # | đột biến | phán định | báo cáo in ra | mã thoát |
|---|---|---|---|---|
| NỀN | không sửa | — | `CA 40/40` · `ĐỘT BIẾN 46/46` · `D8(a)(b)(c) ĐẠT` | 0 |
| M1 | dòng 607 `fn()` thành `pass` | **BỊ GIẾT** | `CA 40/40 đạt · 0 đỏ` · `D8(a) ĐỎ ('D11-gate',)` · **`D8(b) ĐẠT`** | 1 |
| M3 | dòng 652 chốt thành `if False:` | **SỐNG SÓT** | `CA 40/40` · `D8 ĐẠT` toàn bộ | 0 |
| M4 | 607 + 652 cùng lúc | BỊ GIẾT | `D8(a) ĐỎ` và **`D8(b) ĐỎ` cả 46 đột biến** | 1 |
| M5 | dòng 664 `rc = 0` | **SỐNG SÓT** | `CA 39/40 đạt · 1 đỏ` · `TỔNG: ĐẠT` | 0 |

## Ba chỗ còn hở

### 1. Chốt GHI ĐÈ phép đo thật bằng một dòng SAI (từ M1 so với M4)

Chốt là hai dòng:

    if not getattr(chay_cli, "d11_da_chay", False):
        d8_errors = (("D11-gate",), (), ())

Nó không THÊM lỗi, nó THAY TOÀN BỘ `d8_errors`. Trong đúng kịch bản nó sinh ra để bắt
(thân ca rỗng), sự thật là `D8(b)` đỏ cho **cả 46** đột biến — M4 in ra đúng như thế khi bỏ chốt.
Có chốt, M1 in `D8(b) không tập giết rỗng: ĐẠT`. Dòng đó **sai**.

Cổng vẫn đỏ, nên verdict cuối không sai. Nhưng báo cáo nay chứa một khẳng định xanh không đúng
sự thật, ở đúng chỗ nó phải mô tả. Đây là CÙNG LỚP lỗi mà finding P1 nêu — báo cáo mâu thuẫn với
thực tế — chỉ dời chỗ.

### 2. Chốt không tự bảo vệ, và cũng KHÔNG cần thiết

- M3 cho thấy xoá chốt là VÔ HÌNH: cổng vẫn `40/40`, `D8 ĐẠT`, `rc=0`. Không phản chứng nào chết.
  Theo D8(b) của chính packet này — không tập giết nào được rỗng — hai dòng ấy là mã KHÔNG ĐO ĐƯỢC
  thêm vào chính cái cổng đang đo mọi thứ khác.
- M4 cho thấy chốt KHÔNG phải thứ giết M1: bỏ chốt đi thì thân-ca-rỗng vẫn chết, qua `D8(b)`,
  vì mọi tập giết thành rỗng. `D8(b)` đã đủ. Chốt chỉ chen vào TRƯỚC và làm hỏng bản báo cáo.

Bốn đột biến mới (`d11_d8_ok_luon_dung`, `d11_xoa_loi_d8`, `d11_ep_rc_xanh`, `d11_bo_than_ca`)
đều chết qua ca `D11-gate`, nhưng ca ấy dựng một cảnh giả (`CASES` một phần tử, `chay_dot_bien`
thay bằng lambda) trong đó cờ `d11_da_chay` LUÔN được đặt — nên cảnh ấy không bao giờ đi qua nhánh
chốt. Chốt sống ở đường chạy thật, và đường chạy thật không có ai đo.

### 3. `rc = 0` vẫn sống — mã thoát vẫn tách rời báo cáo (M5)

Ép một dòng `rc = 0` cho ra tiến trình thoát **0** trong khi in `CA 39/40 đạt · 1 đỏ`, và dòng cuối
in `TỔNG: ĐẠT`. `TỔNG` suy từ `rc`, không suy từ báo cáo — nên hai nửa của cùng một bản in mâu thuẫn
nhau, và CI nào chỉ đọc mã thoát sẽ thấy xanh. Đây đúng là điều P1 nêu và nó chưa đóng.

Lưu ý cho công bằng: `d11_ep_rc_xanh` CÓ trong bảng và CÓ chết trong sổ đột biến (ca `D11-gate` đỏ
bên trong bản đột biến). Nhưng tính chất đầu-cuối — *mã thoát phải phản ánh báo cáo* — thì không.
Sổ đột biến xanh không chứng minh tính chất đầu-cuối đúng.

## Điều KHÔNG hở

Ba P1 vòng 2 đã commit ở `97617d3a` là LÀNH: chạy lại đúng cây đã commit cho
`CA 39/39 đạt · 0 đỏ`, `ĐỘT BIẾN 42/42`, `D8(a)(b)(c) ĐẠT`, `rc=0`. Ba mệnh đề an ninh
(scheme, hostname, path) nay đều có phản chứng riêng và ba đột biến tương ứng đều chết.

## Vì sao dừng ở đây thay vì vá tiếp

1. **Ngân sách bằng 0.** 900/900. Sửa được thì phải ĐỔI dòng, không THÊM dòng. Cửa còn hẹp nhưng
   khác không — điều kiện dừng S2 chưa bị vi phạm, nhưng biên không đủ cho một bản vá thoải mái.
2. **Finding chỉ ra chính CÁCH VÁ là sai, không phải chi tiết vá sai.** Hướng đúng gần như chắc là
   BỎ chốt và cho `rc` suy RA TỪ bản báo cáo đã in, thay vì tính song song với nó — đó là sửa cấu
   trúc `chay_cli`, không phải thêm một chốt nữa. Protocol §3.2: finding cho thấy đặc tả thiếu thì
   verdict là `blocked` và đi qua revision mới.
3. Vì hai điều trên, phiên điều phối **không commit** bản vá này như "P1 đã đóng". Diff giữ nguyên
   trong bản clone làm việc, băm đã ghi ở trên để đối chiếu.

## Đề xuất cho người giữ kho

- **A (khuyến nghị)** — `blocked` + lease r6: bỏ hai dòng chốt, đổi `chay_cli` để `rc` suy từ bản
  báo cáo (net âm dòng, không cần nâng trần), thêm một ca đo đúng tính chất đầu-cuối
  *mã thoát phản ánh báo cáo*. Nếu ca ấy không đủ chỗ trong 900 thì mới bàn trần.
- **B** — land `97617d3a` (ba P1 vòng 2, ĐÃ LÀNH) và tách P1 vòng 3 sang packet riêng, ghi thành
  NỢ CÓ TÊN. Được phép theo `luat_dung_LAND`? **Không** — `luat_dung_LAND` chỉ cho P2 thành nợ;
  P1 vẫn chặn land. Nên B chỉ hợp lệ nếu người giữ kho hạ hạng finding này, và tôi không tự hạ.
