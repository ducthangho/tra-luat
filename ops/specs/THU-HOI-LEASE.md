# Đặc tả ĐÓNG BĂNG — `THU-HOI-LEASE` (Issue #385)

```yaml
schema_version: 1
packet_id: wp385
revision: 1
objective: >-
  `ops/lease_publish.py` có một đường THU HỒI riêng, ngữ nghĩa tách khỏi `da_bi_thay_the`,
  và nó đòi BẰNG CHỨNG đo được chứ không nhận lời khai.
write_set:
  - type: exact
    path: ops/lease_publish.py
  - type: exact
    path: ops/lease_publish_test.py
depends_on: [372]
executor: codex
environment: cloud
risk: normal
review_class: sensitive
effective_review_class: sensitive
```

## Điều kiện tiên quyết ĐÃ THOẢ

`#385` đòi *"chờ #383 land trước"*. Đã land: merge `9e6d50dccd886817864c1ca5fd1c8207d4643654`,
`2026-08-28T11:51:22Z`. Vị từ đối xứng của #372 nay là **nền** của packet này, không phải giả định.

## Nền ĐO ĐƯỢC — `2026-08-28T12:1xZ`, master `9e6d50d`

Quét toàn bộ ref remote, dedup theo `lease_id`, chỉ lấy lease **CÒN_HẠN** và **không có bia mộ**:

```
8  lease CON_HAN, khong co bia mo
3  CHAC CHAN song thua  (nhanh vao master  VA  Issue da dong)  -> 9 duong dan
5  KHONG phan biet duoc
```

Ba cái chắc chắn: `nang-nhan-menh-de-thu-tam-exec-1` (#364), `tach-danh-tinh-github-exec-1r6`
(#348), `l7-trich-dan-thu-muc-an-exec-1r2` (#378). Chín đường gồm cả `RELEASE_MANIFEST.json` —
artefact **dùng chung**, mọi packet chạm `scripts/**` đều cần.

### Phép đo ĐẦU của phiên điều phối đã SAI — và cái sai ấy là dữ liệu của packet

Lượt đầu tôi dùng **một** tín hiệu, "head của `branch` là tổ tiên của master", và ra **8/8 sống
thừa**. Sai. Nó bắt nhầm hai ca:

* `d9-con-ho-exec-1` (#382): nhánh vừa tạo **tại chính master**, chưa đẩy gì ⇒ "tổ tiên của
  master" đúng về mặt commit, sai hoàn toàn về mặt việc.
* `w1-p1-van-chuyen-prompt-exec-2` (#368): **lượt mới dùng lại nhánh cũ đã merge**; write set của
  nó (`review_verdict_binding.py`, `packet_loop*`) khác hẳn lượt trước.

**Không tín hiệu nào trong hai tín hiệu ấy nằm trong tệp lease.** Phiên điều phối phải tra git
*và* GitHub Issue để đoán, rồi vẫn đoán sai. Đó chính là bằng chứng 1 của `#385` —
*"Không trường nào trong tệp lease nói ra điều đó"* — nay có thêm một lần tái hiện.

**Executor PHẢI đo lại cả ba con số.** Chúng là đo của phiên điều phối, không phải chân lý.

## Bốn việc (từ Issue #385)

1. **Lệnh `thu-hoi` có ngữ nghĩa RIÊNG.** Không mượn `da_bi_thay_the` — trường ấy nghĩa là
   *"bị lease KIA thay thế"* và đòi một lease kế nhiệm; thu hồi thì **không có** kế nhiệm.
   Trường riêng (gợi ý `da_thu_hoi` + `thu_hoi_ly_do` + `thu_hoi_bang_chung`) với vị từ riêng.
   **Ràng buộc cứng:** nó KHÔNG được thành đường gỡ khoá **dễ hơn** `da_bi_thay_the`. Dễ hơn
   nghĩa là mở lại đúng lỗ #372 vừa bịt, chỉ đổi tên trường.

2. **Đòi BẰNG CHỨNG, không nhận LỜI KHAI.** `thu_hoi_bang_chung` chứa SHA merge, và vị từ phải
   kiểm SHA ấy **thật sự là tổ tiên của `master`**. Một lệnh `thu-hoi` nhận lời khai thì **tệ hơn
   không có lệnh** — nó hợp thức hoá đúng thứ #372 vừa chặn.

3. **Dọn 7 hồ sơ cũ bằng chính lệnh mới** — nhưng xem `S3`: việc này **KHÔNG** làm trong packet
   này, vì nó đòi write set `ops/leases/**`. Packet này giao **công cụ**; chạy nó trên corpus là
   một hành vi DỮ LIỆU riêng, có write set riêng.

4. **Trả lời: chuỗi revision có cần bia mộ hai chiều không?** `(A)` giữ nguyên · `(B)` suy từ quy
   ước tên · `(C)` cách khác đo ra tốt hơn. **Không chọn `(A)` chỉ vì nó được liệt trước, không
   chọn `(B)` chỉ vì tiện** — `(B)` là *suy từ CÁCH VIẾT*, đúng hình dạng kho đã trả giá
   (`codex-dispatcher`, `cödex` lọt qua vì cổng phân biệt cách viết chứ không phân biệt thẩm quyền).
   Trả lời bằng **phép đo**, và trả lời trong PR.

## acceptance_criteria

1. `thu-hoi` từ chối khi `thu_hoi_bang_chung` **vắng mặt**.
2. `thu-hoi` từ chối khi SHA **không phải** tổ tiên của `master` (dựng một SHA có thật nhưng ở
   nhánh chưa merge).
3. `thu-hoi` từ chối khi SHA **không tồn tại**, với mã/thông điệp **phân biệt được** với (2).
4. Lease đã thu hồi **thôi được đếm** là người giữ; `ai-dang-giu` trả `NGƯỜI_GIỮ 0` cho đường ấy.
5. Thu hồi **KHÔNG** làm bia mộ một chiều: `_bia_mo_doi_xung` không được coi lease đã thu hồi là
   hồ sơ hỏng ⇒ **không** `rc=12`. **Đây là ca dễ trượt nhất** — hai cơ chế phải sống chung.
6. Vị từ thu hồi **không dễ hơn** `da_bi_thay_the`: khai `da_thu_hoi` mà thiếu bằng chứng ⇒ chặn,
   không im lặng gỡ khoá.
7. Mỗi chốt 1–6 có **ca test riêng** VÀ **đột biến riêng** làm đúng ca ấy ĐỎ.
8. **Bảng BA HẠNG đột biến**: giết thật / tín dụng giả / sống sót. Tín hiệu "assertion của ca đích"
   phải là thứ **mã triển khai không giả được** — lớp ngoại lệ riêng. Trong #359 một
   `except Exception: raise AssertionError(...)` viết với ý định đúng đã lừa **cả hai** bộ đo.
9. `ops/lease_publish_test.py` xanh `N/N`, khai `N`; nền hiện tại **124/124, bỏ qua 0**.
10. Trả lời việc 4 bằng phép đo, viết vào PR.

## Điều kiện dừng

- `S1` cần đường dẫn thứ ba ngoài write set ⇒ DỪNG.
- `S2` vượt trần ADR-0044 cho packet chạm authority: `≤3 tệp / ≤300 dòng thêm` ⇒ DỪNG, trình phép
  đo, xin quyết định. Nền tham chiếu: #372 dùng `64 + 183 = 247` dòng thêm cho hai tệp.
- `S3` phải sửa bất kỳ tệp nào trong `ops/leases/**` ⇒ **DỪNG**. Dọn dữ liệu và vá cổng là hai rủi
  ro khác nhau; gộp thì lúc đỏ không biết bên nào gây ra. Việc 3 nằm ngoài packet này.
- `S4` vị từ thu hồi hoá ra **dễ hơn** `da_bi_thay_the` ở bất kỳ chiều nào ⇒ DỪNG, khai.
- `S5` `origin/master` đã đi tiếp so `base_sha` mà chưa đo lại.
- `S6` bất kỳ lease nào trong 8 lease `CÒN_HẠN` hiện có **đang đăng được** mà hoá thành không đăng
  được ⇒ DỪNG, khai tên lease.

## Ràng buộc

- KHÔNG commit / push / tạo / xoá / đổi ref. Phiên điều phối commit.
- KHÔNG đụng `ops/leases/**` — kể cả để "thử lệnh mới".
- Đồ giả mô phỏng TRẠNG THÁI, không diễn kịch bản.
- ĐỪNG viết chuỗi bỏ-qua-CI nguyên văn ở bất cứ đâu.
