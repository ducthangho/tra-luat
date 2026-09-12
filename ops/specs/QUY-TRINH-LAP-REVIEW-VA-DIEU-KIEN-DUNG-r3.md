# Đặc tả packet — QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG (revision 3)

- `packet_id`: **QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG**; ID bền `wp523`.
- `packet_issue`: **523** · `mission_issue`: **499**
- `revision`: **3** · `generation`: 2 · soạn **12-09-2026**
- `thay_the_cho`: **revision 2** (`spec_sha256`
  `4ada6921503da3748ef54b019633e440d21a8f23c3c15f7e1064fe8f3ae85a58`, đã cấp packet + lease gen 1, đã
  chạy ít nhất một lượt cross-review). r2 và r1 **giữ nguyên trên đĩa làm hồ sơ**.
- `depends_on`: **`[]`** · `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive**

## `nguon_cap_viec`

Kế thừa r1 và r2. Cộng chỉ thị MỚI của chủ kho 12-09-2026 — **cấp thêm `ops/reviews/`** — bản chiếu ở
[#issuecomment-5646812840](https://github.com/ducthangho/tra-luat/issues/523#issuecomment-5646812840), cùng chỉ thị quy trình *"lặp vá, cross review phân theo lớp, đăng verdict; không ci,
full ci, ci windows cho tới khi merge"*.

## VÌ SAO PHẢI CÓ r3 — hai phép đo, không phải tiện tay

**1. Hiện vật review của packet này không vào được kho.** Write set r2 là **đúng hai** tệp skill. Đo ở
lượt 1: `VERDICT.md` (`sha256` `9695e0eb…`, 29 201 B) **không commit được**, nên nó sống trong sandbox
và chết theo container. Tiền lệ đã trả giá: lượt 1–2 của #522 mất trắng hai tệp verdict, và hai băm
`db9be984…` / `6032ff98…` nay **KHÔNG ĐO ĐƯỢC** vĩnh viễn.

**2. `M7` của chính packet này tạo ra một nghĩa vụ KHÔNG THI HÀNH ĐƯỢC.** `M7` đòi mỗi lượt CI loại
(b) ghi **`run_id` vào biên nhận** — mà r2 không cấp đường ghi biên nhận. Một nghĩa vụ không thi hành
được là một nghĩa vụ sẽ bị bỏ, và packet này lẽ ra phải là packet ĐẦU TIÊN tuân luật nó khai.

`§3.2` và `§5` đều đòi: đổi write set ⇒ **revision mới, generation mới, cấp lại lease**. Nên r2 không
được nới tại chỗ; nó bị **thay**.

## `nang_tran` — đã được cấp TƯỜNG MINH, ghi vào đặc tả

```yaml
nang_tran:
  same_failure_limit: 2 -> 10
  attempts_limit: 3 -> 10
  ai_nang: ducthangho
  can_cu: https://github.com/ducthangho/tra-luat/issues/523#issuecomment-5646812840
  xac_nhan_khuon: 'chủ kho xác nhận "Nâng như #522" — cùng khuôn đã nâng cho #522'
```

Nâng này **KHÔNG** chữa lớp nào; nó chỉ cho phép **đo tiếp**. `phep-do-doctrine-khong-du-rang` vẫn là
nợ về **cơ chế đo**, và `packet_loop.py` không nằm trong write set nên packet này **không** được vá
scanner.

## `review_class` và ngưỡng — `ADR-0044` nói cho chật

`sensitive` ⇒ ≤ **3 tệp**, ≤ **300 dòng thêm**. Packet này giữ **đúng hai** tệp SẢN PHẨM.

`ops/reviews/` là **hiện vật review bất biến** — `ci.yml` khai thẳng chúng *"không phải mã sống để CI
chạy"* — nên **KHÔNG** tính vào phép đếm tệp sản phẩm của `ADR-0044`. Nói ra ở đây để `A9` không mơ hồ,
đúng tiền lệ spec r3 của #522. Trần **300 dòng thêm** áp cho **hai tệp sản phẩm**, không áp cho hiện
vật review.

## `write_set`

| # | đường dẫn | kiểu | vì sao |
|---|---|---|---|
| 1 | `.claude/skills/cross-review/SKILL.md` | exact | bên SINH bảng phân hạng và verdict |
| 2 | `.claude/skills/work-packet/SKILL.md` | exact | bên ĐỌC bảng ấy và quyết vá / merge / dừng |
| 3 | `ops/reviews/` | prefix | `VERDICT.md` + `*.receipt.yaml` + hàng Mục lục của các lượt |

**KHÔNG** đụng `docs/PROTOCOL_DA_PHIEN.md` (adapter là MỎNG; `doctrine-scan` đỏ khi adapter chép
doctrine). **KHÔNG** đụng `.claude/hooks/**`. **KHÔNG** đụng r1/r2 của chính đặc tả này.

## `ngoai_pham_vi`

Giữ **nguyên năm mục của r2**: không chép con số trần vào skill · không viết cổng cưỡng chế · không đổi
định nghĩa P1/P2/P3 · không tự quyết thay chủ kho ở Rescue Checkpoint · không biến quy định hậu-merge
thành *"khỏi cần CI"*. Thêm:

6. **KHÔNG sửa `VERDICT.md` của một lượt đã giao** — chúng neo theo băm. Sửa là làm bản chiếu đã đăng
   thành lời khai sai.

## `muc_tieu`

`M1`–`M10` **giữ nguyên từ r2** (và r2 giữ `M1`–`M7` từ r1 — **đọc r1 cho định nghĩa đầy đủ, đừng đọc
dòng liệt kê tóm tắt**; chính chỗ ấy đã sinh 1 P1 + 4 P2 ở lượt 1). r3 thêm:

| # | mục tiêu | chiếu vào |
|---|---|---|
| M11 | **Hiện vật cross-review của packet này SỐNG TRONG GIT**: mỗi lượt có `VERDICT.md` nguyên byte + `*.receipt.yaml` hợp lược đồ v2 + một hàng trong bảng Mục lục của `ops/reviews/README.md`. | 3 |
| M12 | **`M7` thi hành được**: nghĩa vụ ghi `run_id` vào biên nhận nay có đường ghi. Nếu `N = 0` (không chi lượt (b) nào) thì biên nhận khai thẳng **`0`**, không bỏ trống. | 3 |

## `nghiem_thu`

`A1`–`A13` **giữ nguyên từ r1 và r2**. r3 thêm:

**A14 (M11) — hiện vật sống trong git, đếm được.**
`packet_loop.py bien-nhan --packet 523` ⇒ **≥ 1** biên nhận reviewer PHÂN BIỆT ĐƯỢC, và
`ops/bien_nhan_v2.py` ⇒ `rc=0` **0 vi phạm**. Mỗi `VERDICT.md` trong kho có `sha256` **khớp** bản chiếu
đã đăng trên PR.
**Phép làm ĐỎ:** thêm biên nhận trỏ một `verdict_path` không tồn tại ⇒ `bien-nhan` xếp là **mồ côi** và
không đếm ⇒ ĐỎ · hai biên nhận cùng `reviewed_sha` ⇒ đếm là **một** vòng, không phải hai.
**Đo nền trước khi vá:** `bien-nhan --packet 523` hiện `rc=11`, **0** biên nhận.

**A15 (M11) — hàng Mục lục là nghĩa vụ, cổng đã có răng.**
Mỗi tệp verdict thêm vào `ops/reviews/` phải có một hàng trong bảng **Mục lục** của
`ops/reviews/README.md`, ở **CỘT `tệp verdict`**.
**Phép làm ĐỎ:** thêm verdict mà không thêm hàng ⇒ `t27` của `ops/lease_publish_test.py` ĐỎ. Cổng này
**đã có răng, đo được 12-09-2026 trên #522**: nó bắt đúng chỗ ấy, CI `146/147`, ca đỏ duy nhất là `t27`.

**A16 (M12) — `run_id` khai được cả khi bằng 0.**
Biên nhận phải có chỗ khai số lượt CI loại (b) đã chi cùng `run_id` của chúng; `N = 0` thì khai **`0`**
tường minh.
**Phép làm ĐỎ:** bỏ trống trường ấy ⇒ không phân biệt *"chưa chi lượt nào"* với *"chưa ai ghi"* ⇒ ĐỎ.
Đây đúng lớp *"vắng mặt vì sạch và vắng mặt vì chưa nhìn tới nhìn giống hệt nhau"*.

**A9 viết lại cho khớp write set mới:** `git diff --numstat` ⇒ **đúng hai** đường dẫn ngoài
`ops/reviews/`, `additions` của hai đường ấy ≤ **300**. Đường thứ ba nào ngoài `ops/reviews/` ⇒ ĐỎ.

**Điều kiện dừng:** `sensitive` ⇒ `approve` **tường minh**. Packet này phải là packet đầu tiên tuân
**chính** quy trình nó khai — gồm `M8` và `M10`.

## `chua_do_duoc`

Giữ **hai mục của r2** (không cổng nào canh M1–M10; *"dự đoán vòng này là cuối"* không đo được — nợ
`DIEU-KIEN-VONG-CUOI-KHONG-DO-DUOC`). Thêm:

3. **`HEAD-DOI-VI-HIEN-VAT-REVIEW`** — `M8` phân xử **hai** nguyên nhân head đổi, nhưng đo được trên
   #522 một ca **THỨ BA**: head đổi vì **hiện vật của CHÍNH lượt review** (`approve` neo `7bdd8ad`,
   head merge `73558aa`, `diff` = đúng ba tệp `ops/reviews/**`, không có thay đổi sản phẩm). Xếp nó vào
   *"tác giả đẩy commit ⇒ làm lại"* tạo vòng lặp không bao giờ đóng. **r3 KHÔNG giải quyết ca này** —
   nó chỉ ghi tên nợ; cách phân xử thuộc một revision sau, và packet này sẽ **tự gặp** ca ấy ngay khi
   commit verdict của mình. Khi gặp: khai thẳng trong bản chiếu, đừng tự suy approve còn hiệu lực.
4. **`grep -i` không đo được tiêu chí văn bản tiếng Việt** — đo được 12-09-2026: hai lần gọi cho hai
   kết quả khác nhau trên cùng một tệp cho `gọi tên`/`GỌI TÊN`. Mọi tiêu chí `A1`–`A16` phải đo bằng
   `python casefold` hoặc parse cấu trúc, **không** bằng `grep -i`. Chưa ai đo nguyên nhân; ghi triệu
   chứng, không ghi lời giải thích.
