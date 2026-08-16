# Hồ sơ packet wp55 revision 4 — đã land

**Kết quả:** land vào master ngày 16-08-2026 qua PR #130, merge commit
`07fb03d6e245381f6f38e5b79f6a7dadfc76f4eb`. Head được duyệt:
`817598e2a3101c1e550dcba59bd7caea093264f6`.

## VÌ SAO CÓ TỆP NÀY, VÀ VÌ SAO HỒ SƠ PHẢI VÀO MASTER

Doctrine của kho nói *"nguồn sự thật là TỆP TRONG KHO, comment chỉ là bản chiếu"*. Câu ấy
yếu hơn vẻ ngoài của nó khi tệp chỉ nằm trên một nhánh `ops/**` chưa merge: **nhánh xoá được**,
và xoá xong thì con băm trong comment không còn trỏ vào đâu cả — đúng lớp lỗi mà lease #3 của
wp55 từng trả giá (`prompt_sha256_required: 46a833cc…` không ứng với văn bản nào, wp55 đứng im
hai ngày).

Đo được lúc dọn dẹp 16-08: **22 hồ sơ của revision 4 nằm rải trên 9 nhánh `ops/**`, và KHÔNG
tệp nào có trên master** — trong khi revision 2 thì có. Nếu dọn nhánh trước khi land hồ sơ thì
toàn bộ dấu vết kiểm chứng của một packet vừa land sẽ biến mất, và không ai phát hiện ra cho
tới lần cần tra cứu đầu tiên.

Nên thứ tự đúng là: **land hồ sơ vào master TRƯỚC, xoá nhánh SAU.**

## Neo bất biến

| | |
|---|---|
| packet issue | 55 · mission 54 · revision 4 · phase F3-03 |
| `spec_path` | `ops/specs/wp55-r4-spec.md` |
| `spec_sha256` | `86d9627caf55ea2cb8e4caa29ef036fd490c190d8481fb4f79dd5d1703eb1afd` |
| `base_sha` | `18da1da6a07ab2c86d716cef1d74ff2cd0e3218a` (tip master lúc đo, sau PR #129) |
| `start_from_sha` | `b0e3e3b6a4c630ba0652b8fc939025d9c4031c67` |
| head đã duyệt | `817598e2a3101c1e550dcba59bd7caea093264f6` |
| merge commit | `07fb03d6e245381f6f38e5b79f6a7dadfc76f4eb` |

## Sổ commit (AC 26) — mỗi commit khai lease nó chạy dưới

| sha | lease_id | nội dung |
|---|---|---|
| `179d5f37` | `wp55-r4-exec-1-claude-20260816` | merge master `18da1da` vào nhánh packet |
| `2432e3f6` | `wp55-r4-exec-1-claude-20260816` | AC 19 bỏ hẳn miễn trừ — xoá cơ chế, nối lại ma trận |
| `817598e2` | `wp55-r4-exec-2-claude-20260816` | xoá hai hằng chết `C3_CU`/`C3_MOI` (AC 19 mục 2) |

Không commit nào ngoài sổ. Đây là chỗ revision 3 hỏng — bốn commit chạy không lease — và AC 26
sinh ra để chặn tái diễn.

## Lease — bốn của dòng chính, ba của việc phụ trợ

| lease | vai | neo | kết cục |
|---|---|---|---|
| `wp55-r4-exec-1-claude-20260816` | executor | `b0e3e3b6` xuất phát | hoàn tất, bàn giao §7 |
| `wp55-r4-review-1-codex-20260816` | reviewer | `2432e3f6` | `do_not_land`, bị `review-2` thay |
| `wp55-r4-exec-2-claude-20260816` | executor | `2432e3f6` xuất phát | hoàn tất, commit `817598e2` |
| `wp55-r4-review-2-codex-20260816` | reviewer | `817598e2` | **`approve`** |
| `wp55-r4-review-viet-lai-codex-20260815` | reviewer | bản viết lại `CLAUDE.md` | `approve` |
| `wp55-r4-review-di-tru-codex-20260815` | reviewer | đường di trú | — |
| `wp55-r4-review-rebase-codex-20260816` | reviewer | bản rebase `c44b2d4` | `approve`, diff byte-for-byte |

**Khuyết đã biết, khai thẳng:** cặp reviewer dùng `supersedes_lease` đúng cách; **cặp executor
thì không**. `exec-1` và `exec-2` cùng khai `branch_ownership: exclusive` trên cùng một nhánh và
cùng còn hạn danh nghĩa, nên đọc máy móc thì AC 26 thấy hai lease chồng nhau. Thực chất `exec-1`
đã đóng bằng bàn giao §7 trước khi `exec-2` được cấp, nhưng không có gì trong hồ sơ nói thế.
Bản ghi giải phóng nằm ở comment `5308802270` trên #55. **Cách chữa cho lượt sau:** lease
executor thế hệ N+1 khai `supersedes_lease` trỏ thế hệ N ngay lúc cấp, giống hệt cặp reviewer.

## Cross-review — §8 cross-provider, executor `claude` ⇒ reviewer `codex`

| lượt | neo | verdict | băm verdict |
|---|---|---|---|
| 1 | `2432e3f6` | `do_not_land` | `fe002e5b245a3f38f183b673809d4fe3362622c7a9653aa3c6a78dd9bfc5b9b4` |
| 2 | `817598e2` | **`approve`** | `8896120bbd77f0b1503fbfcce9d292be6b347cb9416c47f083f2a44471c0f6bb` |

**Một finding bị RÚT, và cách nó bị rút đáng ghi lại.** Lượt 1 nêu
`mutation-kill-set-omits-false-positive-case` ở mức P1 vì tưởng đột biến giết một ca chiều
bắt-oan. Một phiên `claude` đo lại và thấy hai ca "thừa" là ca VIẾT TAY đòi `rc=6` — chiều lọt,
không phải bắt-oan — và chúng chỉ TRÙNG tiền tố `ac19_` với các ca sinh tự động từ `LOP_BAT_OAN`.
Trong đúng miền `LOP_LACH` mà danh sách tự khai thì hai tập khớp tuyệt đối: 37/37 và 43/43.

Phiên `claude` ấy **cùng provider với executor**, nên theo §8 nó KHÔNG có thẩm quyền bác một
finding chống lại sản phẩm của chính provider mình. Phản chứng vì thế được gửi cho reviewer làm
**đầu vào**, và `codex` tự chạy lại cả ba phép đo rồi tự rút. Ghi lại vì đây là tiền lệ: người
đo ra sai sót không đương nhiên là người được phán.

## Nội dung — AC 19 đổi HỢP ĐỒNG, không vá thêm

Bốn lượt cross-review liên tiếp (7, 8, 9, 10) đều tìm ra hình dạng mới của **cùng một** lỗ.
Lượt 10 kết luận nguyên nhân không nằm ở mã: AC 19 của revision 3 đòi scanner phân loại ngữ
nghĩa mở trên văn xuôi — một hợp đồng không cài đặt được, nên mọi bản vá đều là xấp xỉ và mọi
xấp xỉ đều có phản ví dụ.

Revision 4 bỏ hẳn miễn trừ. `packet_loop.py` từ 1503 xuống 1223 dòng (280 dòng, 18,6%). Sáu
phản ví dụ của các lượt 7–10 đóng cùng lúc, không cần vá gì thêm.

**Cái giá, khai thẳng:** 12 ca chuyển từ ma trận bắt-oan sang ma trận lọt. Đó là hợp đồng mới,
không phải hồi quy. Mỗi ca có một ca **cùng hình dạng** ở lại chiều bắt-oan — cặp ấy là thứ
chứng minh cổng phân biệt NỘI DUNG chứ không phân biệt cấu trúc Markdown.

`AC 22–24` rút: cả ba chỉ tồn tại để vá máy dò cấu trúc phục vụ miễn trừ, mà máy ấy đã bị xoá.

## Số liệu (suite tự in — AC 25)

```
ca               : 185      (nền trước: 173)
đột biến         : 34       (nền trước: 44)
lớp lách         : 78       (nền trước: 66)
ca bắt-oan       : 35       (nền trước: 35)
ngoại lệ AC 18   : 0
```

## Gate cuối, kèm chứng đường

```
doctrine-scan trên nhánh                   rc=0
suite trên nhánh                           rc=0   185/185
AC 20 doctrine-scan trên cây ĐÃ MERGE      rc=0
AC 20 suite trên cây ĐÃ MERGE, có GIT_DIR  rc=0
CHỨNG ĐƯỜNG — bỏ GIT_DIR                   rc=1   fatal: not a git repository
gate master 10dc171c ubuntu + windows      success
```

Dòng chứng đường là phép đo cố ý: nó ĐỎ nên `rc=0` ở dòng trên là bằng chứng dương chứ không
phải phép đo rỗng. Nếu bỏ `GIT_DIR` mà vẫn xanh thì điều kiện AC 20 chỉ là nghi lễ.

## Việc CHƯA làm — nói ra thay vì để người sau phát hiện

1. **Lỗ hook token xoay.** Chốt "không ghi đè khi đã đăng nhập" tin `codex login status`, mà
   lệnh ấy chỉ đọc TỆP chứ không hỏi máy chủ; ngày 16-08 nó báo `Logged in` với một token ĐÃ
   THU HỒI. Lỗ thật, **ngoài `write_set`**, cố ý không đóng ở revision này. Công thức đòi bằng
   chứng dương đã ghi ở `docs/GOI_AGENT_DA_NEN.md` (land qua PR #131).
2. **Sổ attempts của revision 3 không khớp thực tế** — bốn commit chạy không lease. Không hồi
   tố sửa được; AC 26 chỉ chặn tái diễn.
3. **Chưa chạy `ruff` / gate phát hành đầy đủ** trên nhánh packet — `packet_loop*.py` là công cụ
   dev-side, không vào gói phát hành.

## Cảnh báo cho packet kế tiếp

`base_sha` mới là **`10dc171cbc29f1f855d2be82ddb8f3f6c811737b`**, không phải `817598e2` và cũng
không phải `18da1da`. Spec revision 4 đã tự dặn hai lần và vẫn suýt sai hai lần theo hai chiều
ngược nhau — một lần neo vào SHA không còn là tip, một lần neo vào SHA chưa bao giờ là tip.
Cùng một câu chữa cả hai: **con số này có phải tip master không, đo lúc nào?**
