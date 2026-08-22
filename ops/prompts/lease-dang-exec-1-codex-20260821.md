# Prompt EXECUTOR — `LEASE-DANG-DUNG-MOT-LAN` (#227), lượt 1

Bạn là **executor** của packet này. Bạn có lease `lease-dang-exec-1-codex-20260821`.

## Nguồn sự thật — theo thứ tự

1. **`ops/specs/LEASE-DANG-DUNG-MOT-LAN.md`** — đặc tả **ĐÓNG BĂNG**, sha256
   `e1026adb569f5b4732197afac9c0f35cdd5a8945d46301b1d4cb062624e7c72c`.
   **KIỂM BĂM TRƯỚC KHI ĐỌC.** Lệch băm ⇒ DỪNG, báo cáo, không làm gì.
   Đặc tả là thứ định nghĩa `write_set`, `muc_tieu`, `nghiem_thu`, `ngoai_pham_vi`. Prompt này
   **không** định nghĩa lại chúng và **không** được đọc rộng hơn chúng.
2. **Thân Issue #227** — bằng chứng đo được, tóm tắt. Bản chiếu; đặc tả mới là authority.
3. `docs/PROTOCOL_DA_PHIEN.md` · `CLAUDE.md` — luật chung.

Tìm đặc tả ở `master` trước; chưa thấy thì `git fetch origin ops/spec-lease-dang` rồi tìm ở đó.
**Thứ định danh tệp là BĂM, không phải tên nhánh** — tên nhánh là thứ trôi và bị xoá.

## Xuất phát

- `base_sha` = `cfaccff9bb373274552042e01edb4bfee81dc0ed` (`master`).
- Nhánh của bạn: `codex/lease-dang-exec-1`. **Sở hữu độc quyền.** Không đụng nhánh khác.

## Việc, gọn trong một câu

Cổng đăng lease đăng **trùng** comment, và **chết cả lượt** khi `packet_issue` trỏ vào một PR.
Vá theo **tám quyết định Q1–Q8** đã chốt trong đặc tả, không hơn.

## Ba điều đặc tả nói mà rất dễ đọc trôi

1. **Q4 — "cô lập" KHÔNG phải "nuốt lỗi".** Một lease bị chặn không được dừng vòng lặp, nhưng
   cuối vòng lượt chạy **vẫn phải thoát khác 0**. Một cổng đỏ biến thành cổng xanh là hỏng nặng
   hơn cái đang vá. `T51` có **hai** đột biến riêng đúng vì hai nửa này hỏng độc lập.
2. **Mọi lớp mới có BA trạng thái, không hai.** `có` · `không` · **`KHÔNG ĐO ĐƯỢC`**. Trạng thái
   thứ ba **CHẶN**, không cho qua. Đây là chỗ đã trả giá nhiều lần trong kho này.
3. **Đồ giả phải mô phỏng TRẠNG THÁI, không diễn kịch bản.** `ops/don_ref_chot_test.sh` từng
   `40/40` trong khi một đột biến **xoá hẳn** lệnh phá vẫn qua — vì đồ giả diễn kịch bản. Ở đây:
   đồ giả `gh` giữ **danh sách comment theo issue**, "đăng" **thêm** vào danh sách ấy, và `T46`
   phải xanh vì lần hỏi thứ hai **thấy thứ lần một vừa thêm**.

## Ngân sách — CỨNG

**≤ 3 tệp, ≤ 300 dòng THÊM** (ADR-0044, packet `sensitive`). Ba tệp là **đúng trần**.

**Tính ra sẽ vượt ⇒ DỪNG, xuất handoff, trả về người giữ kho.** Không tự chia nhỏ packet, không
tự nới trần. Chia packet là quyết định của người giữ kho (§2).

Đo bằng `git diff --numstat cfaccff9..HEAD` và **báo cáo con số**, đừng ước lượng.

## Cổng bắt buộc — bằng chứng DƯƠNG, không tin `rc`

| cổng | tiêu chí |
|---|---|
| `python3 ops/lease_publish_test.py` | `rc=0` **và** `N/N` với **hai số bằng nhau**, **≥ 52 ca** (nền hôm nay 42) |
| `actionlint .github/workflows/*.yml` | `rc=0` cả 5 tệp. Thiếu công cụ ⇒ in `KHÔNG ĐO ĐƯỢC` và **ĐỎ** |
| đột biến | mỗi chốt mới có đột biến giết **đúng ca của nó**, `1/1`. Chạy trên **BẢN SAO TẠM** |
| kích thước | `git diff --numstat` ≤ 3 tệp, ≤ 300 dòng thêm |

**Đột biến giết nhiều ca ⇒ NÓI RA**, đừng làm tròn thành đạt: đó là dấu hiệu ca chưa tách đủ.

**Đột biến SỐNG SÓT không luôn nghĩa là test yếu, và cũng không luôn nghĩa là mã đúng** — nó có
thể **chưa từng được chạy** (kho này đã trả giá vì `.pyc` va chạm mtime-giây). Đột biến nào sống
sót thì phải đo A/B rồi mới kết luận.

## Điều kiện DỪNG

- Gặp lại hình dạng **"lời khai rộng hơn phép đo"** hoặc **"hỏi chỗ tiện tay thay vì chỗ kết luận
  được ghi"** trong chính bản vá của bạn ⇒ sửa ngay, và **khai trong báo cáo**. Hình dạng thứ hai
  đã đếm **5 lần, cùng một tác giả (`claude`)**; bạn là phép thử cho giả thuyết "hình dạng bám
  người viết". Nếu bạn cũng mắc, giả thuyết **sai** và vấn đề nằm ở đặc tả — lúc ấy **báo cáo**,
  đừng tự sửa đặc tả.
- Chốt phải nằm **ngoài** `write_set` ⇒ DỪNG, xuất handoff, mở packet riêng. **Không** nới
  `write_set`.
- Thấy một tiêu chí trong `nghiem_thu` là **sai** ⇒ DỪNG và báo cáo để mở bản sửa đổi đặc tả.
  **Không** tự đổi giữa đường — đặc tả đã đóng băng và lease neo băm của nó.

## Báo cáo cuối — đòi hỏi

1. `git diff --numstat` (số thật).
2. Đầu ra `N/N` của suite, hai số.
3. Bảng đột biến: mỗi ca mới ↔ đột biến ↔ `giết 1/1`.
4. Mục **`chua_do_duoc`** của riêng bạn — thứ bản vá **không** đóng. Đặc tả đã liệt kê 5 mục;
   nếu bạn thấy thêm, **thêm vào**, đừng im lặng. Nói **"thu hẹp"** khi nó chỉ thu hẹp; chữ
   **"đóng"** chỉ dùng khi có phép đo chứng minh đã đóng.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
