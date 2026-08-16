# AC 19 mới ảnh hưởng gì tới `ops/moi-truong-ba-p1` — đã đo

**Cho phiên đang giữ `ops/moi-truong-ba-p1`.** Bản rà từ phiên wp55, đo trên
`a3fd3ff705bf4831495b1988de7655b32dc68197` và master `d5b7bcc`.

Kết luận ngắn: **118 dòng các bạn thêm hoàn toàn sạch. Không phải sửa gì.** Nhưng nhánh sẽ
ĐỎ vì một dòng các bạn không đụng tới, và cách chữa là rebase chứ không phải sửa.

## Bối cảnh — AC 19 vừa đổi hợp đồng

Chủ kho chốt 15/08: AC 19 của wp55 revision 4 **bỏ hẳn miễn trừ**.

> Cụm trong danh sách cấm KHÔNG được xuất hiện ở bất kỳ hình dạng nào — liền dòng, ngắt
> dòng, trong khối mã, trong bảng, trong tag. Không ngoại lệ nào.

Trước đó có một miễn trừ cho *"văn xuôi kể lại kết quả đo bị ngắt dòng"*. Nó bị bỏ sau khi
bốn lượt cross-review liên tiếp phá được mọi cách cài, và sau khi đo ra rằng chỗ duy nhất
cần nó đã được xử lý bằng cách viết lại câu.

## Đo được trên nhánh của các bạn

| | rc |
|---|---|
| hợp đồng CŨ (còn miễn trừ) | **0** — sạch |
| hợp đồng MỚI (không miễn trừ) | **6** — `CLAUDE.md:82` |

```
CLAUDE.md:82: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
```

**Dòng 82 KHÔNG phải của các bạn.** Nó có sẵn trên master từ trước, và nhánh
`moi-truong-ba-p1` rẽ ra trước khi nó được sửa.

## 118 dòng các bạn thêm — sạch tuyệt đối

Quét riêng phần `+` của diff `master..a3fd3ff` trên `CLAUDE.md`:

```
cụm cấm một dòng  : 0
cụm cấm ngắt dòng : 0
```

Không có gì phải sửa trong phần các bạn viết.

## Cách chữa: rebase, đừng sửa tay

Dòng 82 đã được xử lý ở `c44b2d4c351cbe7f519e1b46aadf68d45e98af86` — một commit hai dòng,
đã qua **hai** lượt cross-review (`approve`, không finding):

```
người có / thẩm quyền   →   tên thuộc / danh sách cho phép
```

**ĐÃ LÊN MASTER 16-08** qua PR #129, land bằng merge commit
`18da1da6a07ab2c86d716cef1d74ff2cd0e3218a` (không ff — master theo nếp merge commit). Tip
master hiện là `18da1da`, không còn là `d5b7bcc`.

**Việc của các bạn bây giờ: rebase `moi-truong-ba-p1` lên `18da1da` là hết đỏ.** Không cần
sửa gì thêm. **Đừng sửa dòng 82 ở nhánh các bạn** — sẽ va với `c44b2d4` và tạo xung đột
không cần thiết.

Đã đo trên chính `18da1da`, kèm chứng đường để phép đo không rỗng:

```
scanner r3g5 (CÒN miễn trừ) @ 18da1da  ->  rc=0
mô phỏng r4  (BỎ miễn trừ)  @ 18da1da  ->  rc=0    master sạch cả dưới hợp đồng MỚI
scanner r3g5 (CÒN miễn trừ) @ d5b7bcc  ->  rc=0
mô phỏng r4  (BỎ miễn trừ)  @ d5b7bcc  ->  rc=6    CLAUDE.md:82 'người có thẩm quyền'
```

Hai dòng cuối là chứng đường: chúng chứng minh phép mô phỏng thật sự bắt được lỗi, nên
`rc=0` ở dòng thứ hai là bằng chứng dương chứ không phải một phép đo không đo gì. Nói cách
khác: rebase lên `18da1da` an toàn **kể cả khi** revision 4 bỏ hẳn miễn trừ AC 19.

## Không va chạm hunk

Hai bên cùng sửa `CLAUDE.md` nhưng ở vùng rời nhau:

```
moi-truong-ba-p1 : @@ -171,6 +171,64 @@   và   @@ -209,6 +267,66 @@
c44b2d4          : @@ -79,8  +79,8  @@
```

Rebase sẽ sạch, không xung đột.

## Một việc nên làm trước khi các bạn khoá bộ test

Nếu suite của luồng môi trường có ca nào dựa vào việc `doctrine-scan` **tha** một cụm cấm bị
ngắt dòng, ca ấy sẽ đỏ khi AC 19 mới được cài. Ở wp55 đã đo: **hai** ca chiều-tha phải
chuyển sang ma trận lọt. Đáng quét trước một lượt để khỏi bị bất ngờ.

## Không đề nghị gì thêm

Luồng môi trường có lease riêng và cross-review riêng, đang ở lượt 10. Bản rà này chỉ để
các bạn không phải tự phát hiện chuyện dòng 82 bằng một lượt gate đỏ.
