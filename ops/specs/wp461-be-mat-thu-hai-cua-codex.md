---
kieu: dac_ta_packet
packet: WP461-BE-MAT-THU-HAI-CUA-CODEX
packet_id: wp461
ban: r2
trang_thai: ready              # bon quyet dinh DA CHOT tai Mission #470; lease r2 neo spec_hash cua BAN NAY.
mission_issue: 470
ho_so_lap_luan: https://github.com/ducthangho/tra-luat/issues/461
neo_uy_quyen: https://github.com/ducthangho/tra-luat/issues/470
thay_the_ban: r1               # r1 spec_hash e74812cf1082daa39226ad3eae74c061afbbf65922b3f886adf3a84ac422df63
ly_do_revision: >-
  Cross-review luot 1 cua PR #469 ra `blocked`, 4 P1. Hai P1 cham thang dac ta:
  `spec-chua-chot-hop-dong` (Q4 chua chot, va Q3 nhu hieu o r1 VO o runtime) va
  `uy-quyen-khong-co-neo-ben`. §3.2 doi thieu o spec phai di qua revision moi.
  Verdict: https://github.com/ducthangho/tra-luat/pull/469#issuecomment-5564937522
sinh_ra_tu: >-
  Cross-review luot 9 cua PR #460, finding F05 (P3) — `c44` tang (b) phai KHAI MOT NGOAI LE
  cho hang Codex thay vi doi chieu duoc no. Verdict:
  ops/reviews/pr460-bien-nhan-v2-review-9-gpt6astra-verdict.md
  (sha256 aac3eb1dc28f928f5d2ef1d2b16c871b6db77bff3bd87ceeaa1af13d97b1492b)
ghi_chu_hinh_dang: >-
  Chua cong nao doc tep nay. No la DU LIEU cho packet ke thua, khong phai giao dien.
---

# `wp461` — bề mặt thứ hai của Codex chưa có tên trong hợp đồng dữ liệu (bản **r2**)

## 1. Phép đo nền (06-09-2026, chạy lại được)

| đo cái gì | lệnh | kết quả |
|---|---|---|
| §2 khai mấy bề mặt cho Codex | đọc `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` hàng Codex | ``​`codex_cli` hoặc Codex service`` — **hai** |
| hợp đồng dữ liệu có mấy | `PROVIDER_HOP_DONG["openai_codex"]["be_mat"]` | `['codex_cli']` — **một** |
| khai trung thực bề mặt thứ hai | `_thieu` với `surface` = `codex_service` · `codex_api` · `Codex service` | **cả ba BỊ TỪ CHỐI** |
| verdict **nhắc** *"Codex service"* | `grep -i` trên `ops/reviews/*-verdict.md` | **13** tệp |
| trong đó **tự mô tả** bề mặt là vậy | đọc từng dòng khớp | **12** (tệp thứ 13 là verdict #460 lượt 9, nhắc trong finding F05) |
| nguyên chuỗi `Codex service/API` | `grep` chuỗi chính xác | **8** tệp |
| receipt `openai_codex` khai `surface` | tại commit thêm spec `f34fc67`: 71 receipt | **12/12 đều `codex_cli`** |
| — đo lại tại `d28c4b1` | 73 receipt | **14/14 đều `codex_cli`** |

**Ba dòng đếm cuối là ĐÍNH CHÍNH của r2** (`dem-nham-vi-tu-tu-mo-ta`, P3 lượt 1): r1 viết *"13
verdict **tự mô tả**"* và *"đọc **70** receipt"*. Vị từ sai và mẫu không ghim SHA. Thêm receipt
mới KHÔNG phải bằng chứng 12 bản cũ sai.

**Hệ quả một câu:** một reviewer chạy trên bề mặt thứ hai **không có giá trị hợp lệ nào để khai
trung thực**. Cùng HÌNH DẠNG `R8-05` (Antigravity lệch `machine`/`machine/local`) và `R7-02`
(chặn quá rộng vì hằng lệch nguồn) — khác ở chỗ lần này lệch **số lượng giá trị**, không phải
giá trị.

## 2. Thứ KHÔNG được kết luận

**12 receipt lịch sử CHƯA bị chứng minh là sai.** Cả 12 đi qua `codex exec`, tức đường **CLI**,
nên `codex_cli` đúng cho *đường gọi* dù mô hình chạy như một dịch vụ.

Và **không có cách nào từ trong kho** xác định một lượt chạy lịch sử thực sự đi qua bề mặt nào:
`codex` không phát `modelUsage`, biên nhận lịch sử chỉ ghi **lời khai**. Nên Q2 dưới đây là
**quyết định của người giữ kho**, KHÔNG phải phép đo. Đừng biến một quyết định thành một phép
đo giả — đúng lớp lỗi kho đã trả giá bốn lần (*"lỗi ĐO thành lỗi DỮ LIỆU"*).

## 3. Bốn quyết định — ĐÃ CHỐT tại Mission #470

| | quyết định | ghi chú |
|---|---|---|
| **Q1** | tên máy bề mặt thứ hai = **`codex_service`** | khớp nguyên văn §2; không bịa tên mới |
| **Q2** | 12 receipt lịch sử **ĐÚNG** — không sửa hiện vật, **KHÔNG** caveat | ⇒ tiêu chí "0 vi phạm" phải thoả **TỰ NHIÊN**; chúng đỏ nghĩa là bản vá SAI |
| **Q3** | cột surface **giữ VÔ HƯỚNG**, **không** đổi arity | `_LUOC_DO_BANG` và mọi ca `c28` về arity KHÔNG phải sửa |
| **Q4** | §2 **giữ prose**, chỉ làm ô surface hàng Codex đối chiếu được | không mọc khối máy đọc được ở lượt này |

## 3bis. HÌNH DẠNG BẢN VÁ — đóng băng, vì r1 để mở chỗ này và nó VỠ

r1 để executor tự chọn nơi đặt hàng mới. Reviewer đo được cách hiểu hiển nhiên nhất (thêm vào
`_TRANSPORT_CONTRACTS`) **không chạy được**: `_dinh_danh_van_chuyen`
(`.claude/dev/launcher.py:199–204`) ném `RuntimeError: provider co nhieu transport: openai_codex`
khi một provider có hai contract — **cả ba** lệnh nền hỏng, kể cả biến thể tuple tên lệnh **rỗng**.

**r2 chốt: hàng mới đi vào `_PROVIDER_NGOAI_CLI`**, bảng `(provider, execution_surface, transport)`
dành cho bề mặt KHÔNG đi qua CLI của launcher:

```python
("openai_codex", "codex_service", "machine"),
```

Căn cứ **đo được**, không phải suy luận — `ops/bien_nhan_v2.py:283–286` đã gộp hai bảng thành TẬP
và không cấm một provider có mặt ở cả hai (`setdefault` + `.add`, không phải gán).

### Phép đo trên worktree rời (đã dọn sau khi đo)

| phép đo | nền | sau vá |
|---|---|---|
| `PROVIDER_HOP_DONG["openai_codex"]["be_mat"]` | `['codex_cli']` | **`['codex_cli','codex_service']`** |
| biên nhận thật khai `surface: codex_service` | 1 lỗi | **tổng lỗi = 0** (RỖNG) |
| khai `codex_api` | 1 lỗi | **1 lỗi**, đúng cột surface |
| khai `chatgpt_web` | 1 lỗi | **1 lỗi**, đúng cột surface |
| khai `codex_cli` | 0 lỗi | **0 lỗi** |
| `_TRANSPORT_CONTRACTS` | — | **không đổi một byte**; arity `{4}` |
| `bien_nhan_v2.py --root .` | — | rc **thật** 0 · 20 ĐẠT v2 · **0 vi phạm** · 0 KHÔNG ĐO ĐƯỢC · tổng 73 |

Vật cản còn lại là **một câu chú thích**, không phải mã: `_PROVIDER_NGOAI_CLI` tự khai *"không bao
giờ chứa"* provider đi qua CLI. Câu ấy đúng khi viết, nay hết đúng — **sửa nó nằm trong write set**.

**Executor KHÔNG được đổi hình dạng này.** Đổi ⇒ verdict `blocked` + revision mới.

## 4. Write set — KHÔNG đổi so r1

```
.claude/dev/launcher.py                      # _PROVIDER_NGOAI_CLI + chú thích của nó
ops/KE_HOACH_THI_CONG_DA_PROVIDER.md         # §2, ô surface hàng Codex
ops/bien_nhan_v2_test.py                     # BO_BA_PROVIDER_DONG_BANG, c44, đột biến mới
CHANGELOG.md
```

**KHÔNG có `ops/bien_nhan_v2.py`.** Phương án 3bis đã chứng minh không cần nó. Nếu hoá ra vẫn
phải sửa sản phẩm thì spec này **thiếu** ⇒ verdict `blocked` + revision mới, đúng §3.2 — không
tự mở write set.

## 5. Tiêu chí nghiệm thu

1. Biên nhận khai TRUNG THỰC `codex_service` **được nhận** với danh sách lỗi **RỖNG** (không phải
   "không có chữ surface" — `R9-F04`); khai `codex_api`/`chatgpt_web` **bị từ chối vì ĐÚNG cột surface**.
2. `c44` tầng (b) **không còn** nhánh `bang(prov == "openai_codex", …)`; mọi hàng §2 đối chiếu
   được **cả ba** cột.
3. **Đột biến rút `codex_service` khỏi hợp đồng phải làm ca đích ĐỎ**, và phải **đọc nguyên văn
   thông báo giết** — `giet_that` chỉ nói đúng CA, không nói đúng CHỐT (`R2-04`, `R7-04`, và giới
   hạn `TinHieuChotCa` reviewer lượt 9 đo được).
4. Receipt lịch sử: **0 vi phạm**, **0 miễn trừ mới**. Theo Q2 điều này thoả tự nhiên; đỏ ⇒ bản vá sai.
5. `_TRANSPORT_CONTRACTS` **không đổi một byte** — kiểm bằng `diff` khối, không bằng mắt.
6. `bien_nhan_v2.py --root .` rc=0 (đọc rc **THẬT**, không phải rc của `tail`);
   `lease_publish_test` không thêm ca đỏ so nền; chạm `launcher.py` ⇒ `launcher_test.py` đo
   **delta so nền = 0**, dựng **cả hai vế trong MỘT lệnh**. Nhớ `181/181` cần mạng + venv;
   offline là `173/173` bỏ qua 9 (`R9-F08`) — sai khác đó là **bằng chứng**, không phải hồi quy.

## 6. Bẫy đã biết, chép sang để khỏi trả giá lại

- **`machine` là TIỀN TỐ của `machine/local`** — mọi phép so cột hợp đồng phải so **Ô**, không `in`.
- **Sửa `ops/reviews/README.md` thì phải chạy lại `lease_publish_test`** — `t26`/`t27` đọc chính
  tệp ấy, một khối chèn giữa bảng **cắt bảng** mà mắt không thấy (`R9-F01`, trả giá ở `fa3f282`).
- **`_cay_guong` không được lấy oracle từ sản phẩm** — phụ thuộc vòng, `R8-01`.
- **Đột biến chạy trên BẢN SAO TẠM**, không ghi vào tệp thật rồi khôi phục trong `finally`.
- **Bộ lọc grep theo TÊN HẰNG thì mù với thay đổi BÊN TRONG bảng.** r1 khai *"#447 không sửa
  `_TRANSPORT_CONTRACTS`"* dựa trên `grep '^[+-].*_TRANSPORT_CONTRACTS'`; diff thật thêm hàng
  `("github", ("gh",), "github_cli", "machine")` (3 hàng ở `c03a409` → 4 hàng ở `bc9aaf7`).
  So **khối đã trích**, đừng grep tên.
- **Va chạm PR: quét theo LEASE là chưa đủ.** `ai-dang-giu` đo lease; một nhánh sửa cùng tệp mà
  không giữ lease nào thì phép đo ấy im lặng. Lượt 1 đo được **22 ref** không phải tổ tiên HEAD
  có diff giao write set, trong khi bảng của r1 chỉ liệt kê 4.
