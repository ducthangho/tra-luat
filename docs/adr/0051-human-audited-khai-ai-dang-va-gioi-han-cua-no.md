# ADR-0051 — `human_audited` khai AI ĐĂNG, và giới hạn của lời khai ấy

- **Trạng thái:** Accepted (2026-09-19, Packet #566 `HUMAN-AUDITED-KHAI-AI-DANG`, chủ kho `ducthangho` phê duyệt tại https://github.com/ducthangho/tra-luat/issues/566#issuecomment-5741393245)
- **Cổng ĐỌC luật này:** `ops/bien_nhan_v2.py`

## Bối cảnh — ba phép đo, không phải ba lo ngại

### `Đ1` — `author_association` KHÔNG phân biệt được người với agent

Đo 04:11Z 19-09-2026, bằng cách đăng một comment rồi **đọc ngược về qua API**: phiên agent trong kho
này chạy bằng credential chủ kho, nên comment do **nó** đăng trả

```
user.login          = ducthangho
author_association  = OWNER
```

**y hệt** một comment chủ kho tự gõ. Không có trường nào trong hiện vật phân biệt được hai thứ.

Hệ quả cho hồ sơ đã có: khuôn `PLAT-M4` khai một dòng *"tác giả: không phải phiên agent"*. Không dữ
liệu nào **trong** biên nhận ấy chứng minh nổi câu đó.

### `Đ2` — lời khai quan trọng nhất hiện không có chốt nào canh

Phản chứng **chạy được**, không phải giả định. Khi dựng biên nhận `human_audited` cho #551, một regex
chuyển `phien_doc_lap` vào `model_reviewer_identity` đã bắt **rộng hơn ý định** và kéo theo **bốn**
khoá lẽ ra ở top-level — trong đó có `dang_boi`. Triệu chứng đo được: `yaml.safe_load` trả
`dang_boi = None` ở top-level trong khi tệp **có** dòng `dang_boi: phien_agent_dang_ho` — nó nằm sai
chỗ.

Và cổng `bien_nhan_v2` **VẪN XANH y hệt** cả trước lẫn sau bản vá: `132 ĐẠT v2 · 0 vi phạm · 0 KHÔNG
ĐO ĐƯỢC · tổng 185`. Vì cổng **không đọc** `dang_boi`.

Nên lời khai trung thực quan trọng nhất của một biên nhận `human_audited` — *ai thật sự đăng* — có
thể nằm sai chỗ, hoặc vắng mặt hoàn toàn, mà không cổng nào kêu.

### `Đ3` — loại mỏ neo ĐÚNG lại là loại làm cổng ĐỎ

Lược đồ v2 có `protected_evidence_ref`, và đó là loại mỏ neo **đúng** cho một audit của người: hiện
vật là một comment được bảo vệ. Nhưng cổng **không có đường đo** cho nó, nên nó rơi vào **trạng thái
thứ ba** và làm cổng ĐỎ.

Hệ quả **thực tế đã xảy ra**, không phải lo xa: biên nhận `human_audited` của #551 phải khai
`canonical_ancestry` trên blob của **bản chiếu** để "cho đo được" — tức mỏ neo trỏ vào **bản sao**
thay vì nguồn có thẩm quyền, và phải tách thêm `nguon_co_tham_quyen_url` ra một trường riêng để
người đọc đừng nhầm. Một chốt cấm cả việc ĐÚNG thì người ta sẽ đi vòng quanh nó — cùng bài học với
`ops-don-ref`.

## Quyết định

**(1) `human_audited` PHẢI khai `dang_boi` ở TOP-LEVEL**, giá trị trong danh sách **CHO PHÉP**
`{chu_kho_tu_dang, phien_agent_dang_ho}`. Thiếu, rỗng, sai giá trị, hoặc **đặt sai chỗ** ⇒ cổng TỪ
CHỐI.

Danh sách **cho phép**, không phải danh sách cấm — bài học `doctrine-scan`: một danh sách cấm phải
đoán trước mọi cách viết của kẻ gian nên thua từ trong thiết kế.

Đọc ở top-level và **chỉ** top-level. Nếu cổng cũng tra trong ánh xạ con thì nó **hợp thức hoá**
đúng cái lỗi `Đ2` sinh ra để bắt. Thông báo lỗi nói thẳng khi tìm thấy `dang_boi` bên trong một khối
`model_<vai>_identity` — một lý do sai đẩy người đọc đi sửa nhầm chỗ.

**(2) `dang_boi: phien_agent_dang_ho` PHẢI kèm `dang_boi_chi_thi_nguyen_van` khác rỗng.** Một lời
khai "agent đăng hộ" mà không trích được chỉ thị thì không ai kiểm lại được — tức lại là một lời khai
không có phép đo. `chu_kho_tu_dang` **không** đòi trích: hai giá trị phải phân biệt được bằng đầu
vào, nếu không hai chốt là một bộ tương đương và ta chỉ đang đo một thứ.

**(3) Cấp đường đo cho `anchor.loai: protected_evidence_ref`**: cổng đọc `posted_comment_id` và
`nguon_co_tham_quyen_url`, đòi URL đúng dạng comment GitHub (`#issuecomment-<số>` hoặc
`#discussion_r<số>`) **và** id trong URL **khớp** `posted_comment_id`.

Đây là chốt **đối chiếu hai nguồn**, không phải chốt hình dạng: `posted_comment_id` là số GitHub
cấp, `nguon_co_tham_quyen_url` là URL người viết — bắt chúng khớp nghĩa là một trong hai sai thì lộ.
Chỉ kiểm hình dạng thì một URL đúng dạng trỏ comment **khác** vẫn qua, và đó đúng là thứ mỏ neo này
phải chặn.

`check_object` **GIỮ NGUYÊN** trạng thái thứ ba. Khai đã cấp đường đo cho cả hai là một lời khai
rộng hơn phép đo — đúng lớp lỗi packet này sinh ra để chặn.

## Điều ADR này khai THẲNG là KHÔNG đạt được

**(a) Nó KHÔNG chứng minh được ai gõ.** `Đ1` là phép đo, và nó không đổi: `author_association` trả
`OWNER` cho cả hai. `dang_boi` là một lời **KHAI**, không phải một phép **ĐO**.

**(b) Nó đóng được "IM LẶNG", KHÔNG đóng được "CỐ TÌNH".** Khi credential dùng chung, một phiên agent
muốn khai gian vẫn ghi được `chu_kho_tu_dang`. Thứ chốt này mua là: lời khai ấy **phải có mặt** và
**phải ở đúng chỗ**, nên nó không còn vắng mặt trong im lặng như `Đ2`. Nó không mua tính trung thực.

**(c) Thẩm quyền của một lượt `human_audited` nằm ở CHỈ THỊ trong phiên, không ở metadata của
comment.** Hệ quả vận hành: khi phiên agent đăng hộ, bản chiếu chỉ thị phải tồn tại **trước**, và
`dang_boi_chi_thi_nguyen_van` phải trích được từ nó.

**(d) Ba chốt trên KHÔNG làm đỏ biên nhận nào đang có.** Đo trên 184 biên nhận lúc 14:0xZ 19-09-2026:
`132 × v2` · `52 × v1`; đúng **2** biên nhận `provider: human`
(`plat-m4-human-audit-ducthangho-verdict` · `slice-b-c-human-audit-ducthangho-verdict`), **cả hai
thiếu `dang_boi`**, **cả hai là v1** và **cả hai nằm trong danh sách NỢ ĐÓNG BĂNG** (ghim băm).
Quyết định (1) là luật **v2** ⇒ không chạm chúng.

Nói thẳng hệ quả kẻo đọc nhầm thành công trạng: **cổng này sẽ KHÔNG từ chối gì cả ở thời điểm land.**
Nó canh biên nhận **tương lai**. Giá trị của nó là `Đ2`, không phải một con số vi phạm.

## Ca đo chạy được cho từng mục

| mục | ca | đột biến làm nó ĐỎ |
|---|---|---|
| (1) bắt buộc `dang_boi` | `c64_human_audited_thieu_dang_boi_phai_CHAN` | `m73_bo_chot_bat_buoc_dang_boi` |
| (1) đặt sai chỗ = thiếu | `c65_dang_boi_trong_anh_xa_con_KHONG_tinh_la_co` | `m74_dang_boi_tra_ca_TRONG_anh_xa_con` |
| (2) đòi trích chỉ thị | `c66_phien_agent_dang_ho_phai_trich_duoc_chi_thi` | `m75_bo_doi_trich_chi_thi` |
| (3) đối chiếu hai nguồn | `c67_protected_evidence_ref_co_duong_do_va_doi_chieu_HAI_nguon` | `m76_neo_comment_chi_kiem_HINH_DANG_khong_doi_chieu` |

Cả bốn đo được `giet_that` với đối chứng sạch. `m76` **đổi đối chứng một lần**: bản đầu dùng `c41`,
và harness từ chối cấp tín dụng vì `c41` phần (g) đo đúng phép đối chiếu ấy nên nó đỏ theo — "đột
biến phá cả cổng". Ghi lại vì đó là chốt chống tín dụng giả chạy **đúng**, không phải một trở ngại.

## Hai ca cũ ĐỔI HỢP ĐỒNG, có chủ ý

`c24` thu hẹp còn `check_object`, và `c41` phần (g) chuyển từ *"trạng thái thứ ba"* sang *"đo hai
chiều"*. Đây là hệ quả trực tiếp của quyết định (3), không phải nới cổng: `c24` vẫn có răng
(`m15_bo_nhanh_hai_loai_anchor_khong_co_duong_do`, neo lại theo nhánh `check_object` còn lại), và
`c41` phần (g) nay có **cả** chiều dương lẫn chiều âm.

## Xung đột lợi ích, khai ở đây chứ không giấu

Phiên soạn đặc tả #566 **cũng** là phiên phát hiện `Đ1`/`Đ2`/`Đ3` **và** là executor của #551.
Không còn vòng độc lập nào bằng máy (`codex` hết quota review, `agy` hết quota). Packet này được
land bằng **chính cơ chế nó đang vá** — `human_audited` — và verdict bắt buộc khai điều đó, kèm sự
thật rằng tại thời điểm land, `dang_boi` vẫn chưa có cổng nào đọc.
