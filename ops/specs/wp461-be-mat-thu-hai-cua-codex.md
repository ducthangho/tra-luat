---
kieu: dac_ta_packet
packet: WP461-BE-MAT-THU-HAI-CUA-CODEX
packet_id: wp461
ban: r1
trang_thai: de_xuat          # CHUA co lease. `ready` chi khi nguoi giu kho cap lease neo spec_hash nay.
ho_so_lap_luan: https://github.com/ducthangho/tra-luat/issues/461
sinh_ra_tu: >-
  Cross-review luot 9 cua PR #460, finding F05 (P3) — `c44` tang (b) phai KHAI MOT NGOAI LE
  cho hang Codex thay vi doi chieu duoc no. Verdict:
  ops/reviews/pr460-bien-nhan-v2-review-9-gpt6astra-verdict.md
  (sha256 aac3eb1dc28f928f5d2ef1d2b16c871b6db77bff3bd87ceeaa1af13d97b1492b)
ghi_chu_hinh_dang: >-
  Chua cong nao doc tep nay. No la DU LIEU cho packet ke thua, khong phai giao dien.
---

# `wp461` — bề mặt thứ hai của Codex chưa có tên trong hợp đồng dữ liệu

## 1. Phép đo nền (06-09-2026, chạy lại được)

| đo cái gì | lệnh | kết quả |
|---|---|---|
| §2 khai mấy bề mặt cho Codex | đọc `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` hàng Codex | ``​`codex_cli` hoặc Codex service`` — **hai** |
| hợp đồng dữ liệu có mấy | `PROVIDER_HOP_DONG["openai_codex"]["be_mat"]` | `['codex_cli']` — **một** |
| khai trung thực bề mặt thứ hai | `_thieu` với `surface` = `codex_service` · `codex_api` · `Codex service` | **cả ba BỊ TỪ CHỐI** |
| verdict tự mô tả *"Codex service/API"* | `grep` trên `ops/reviews/*-verdict.md` | **13** tệp |
| receipt `openai_codex` khai `surface` | đọc 70 receipt | **12/12 đều `codex_cli`** |

**Hệ quả một câu:** một reviewer chạy trên bề mặt thứ hai **không có giá trị hợp lệ nào để khai
trung thực**. Cùng HÌNH DẠNG `R8-05` (Antigravity lệch `machine`/`machine/local`) và `R7-02`
(chặn quá rộng vì hằng lệch nguồn) — khác ở chỗ lần này lệch **số lượng giá trị**, không phải
giá trị.

## 2. Thứ KHÔNG được kết luận

**12 receipt lịch sử CHƯA bị chứng minh là sai.** Cả 12 đi qua `codex exec`, tức đường **CLI**,
nên `codex_cli` có thể đúng cho *đường gọi* dù mô hình chạy như một dịch vụ. Sự lập lờ ấy là
thứ packet này chấm dứt — nó **không** phải bằng chứng có lỗi.

Và **không có cách nào từ trong kho** xác định một lượt chạy lịch sử thực sự đi qua bề mặt nào:
`codex` không phát `modelUsage`, biên nhận lịch sử chỉ ghi **lời khai**. Nên mục 3 câu (2) là
**quyết định của người giữ kho**, KHÔNG phải phép đo. Đừng biến một quyết định thành một phép
đo giả — đó là đúng lớp lỗi kho đã trả giá bốn lần (*"lỗi ĐO thành lỗi DỮ LIỆU"*).

## 3. Bốn quyết định phải chốt TRƯỚC khi viết mã

1. **Tên máy của bề mặt thứ hai** — `codex_service`? `codex_api`? Hay *"Codex service"* trong §2
   chỉ là cách gọi khác của cùng một bề mặt, và cột ấy phải **rút về một giá trị**?
2. **12 receipt lịch sử đúng hay thiếu chính xác.** Nếu thiếu chính xác thì **KHÔNG sửa hiện vật**
   — chúng neo băm; khai bằng **caveat CÓ TÊN** trong `ops/reviews/README.md`, đúng nếp kho.
3. **Cột surface có thành TẬP không.** Đổi arity là đổi `_LUOC_DO_BANG` và mọi hàng `c28` về arity.
4. **§2 có mọc khối máy đọc được không**, hay giữ dạng người đọc và oracle chép tay gánh.

## 4. Write set dự kiến

```
.claude/dev/launcher.py                      # _TRANSPORT_CONTRACTS (+ _LUOC_DO_BANG neu doi arity)
ops/KE_HOACH_THI_CONG_DA_PROVIDER.md         # §2
ops/bien_nhan_v2_test.py                     # BO_BA_PROVIDER_DONG_BANG, c44, c28 (arity)
CHANGELOG.md
```

**KHÔNG có `ops/bien_nhan_v2.py`.** Nếu hoá ra phải sửa sản phẩm thì spec này **thiếu** ⇒ verdict
`blocked` và đi qua revision mới, đúng §3.2 — không tự mở write set.

## 5. Tiêu chí nghiệm thu

1. Biên nhận khai TRUNG THỰC bề mặt thứ hai **được nhận** (danh sách lỗi **RỖNG**, không phải
   "không có chữ surface" — bài học `R9-F04`); khai sai **bị từ chối vì ĐÚNG cột surface**.
2. `c44` tầng (b) **không còn** nhánh `bang(prov == "openai_codex", …)`; mọi hàng §2 đối chiếu
   được **cả ba** cột.
3. **Đột biến rút bề mặt thứ hai khỏi hợp đồng phải làm ca đích ĐỎ**, và phải **đọc nguyên văn
   thông báo giết** để biết nó chết đúng thuộc tính — `giet_that` chỉ nói đúng CA, không nói
   đúng CHỐT (`R2-04`, `R7-04`, và giới hạn `TinHieuChotCa` reviewer lượt 9 đo được).
4. 12 receipt lịch sử: **0 vi phạm** sau thay đổi — hoặc caveat CÓ TÊN nếu quyết là thiếu chính xác.
5. `bien_nhan_v2.py --root .` rc=0; `lease_publish_test` không thêm ca đỏ; nếu chạm `launcher.py`
   thì `launcher_test.py` phải đo **delta so nền = 0** (và nhớ: `181/181` cần mạng + venv —
   offline là `173/173`, bỏ qua 9, `R9-F08`).

## 6. Bẫy đã biết, chép sang để khỏi trả giá lại

- **`machine` là TIỀN TỐ của `machine/local`** — mọi phép so cột hợp đồng phải so **Ô**, không
  `in`. `c44` tầng (b) đã trả giá đúng chỗ này.
- **Sửa `ops/reviews/README.md` thì phải chạy lại `lease_publish_test`** — `t26`/`t27` đọc chính
  tệp ấy, và một khối chèn giữa bảng **cắt bảng** mà mắt không thấy (`R9-F01`).
- **`_cay_guong` không được lấy oracle từ sản phẩm** — phụ thuộc vòng, `R8-01`.
- **Đột biến chạy trên BẢN SAO TẠM**, không ghi vào tệp thật rồi khôi phục trong `finally`.
