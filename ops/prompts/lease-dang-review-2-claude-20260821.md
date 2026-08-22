# Prompt REVIEWER — `LEASE-DANG-DUNG-MOT-LAN` (#227), lượt **2** (cuối)

Bạn là **reviewer** lượt 2. Lease `lease-dang-review-2-claude-20260821`.
**CHỈ ĐỌC.** Không sửa mã, không push, không commit. Đầu ra là một **verdict**.

**Đây là vòng review CUỐI** (`review_rounds_limit: 2`). Sau lượt này packet hoặc `cross_approved`
và land, hoặc bị trả về người giữ kho.

## Neo — kiểm trước khi đọc

- Exact head phải review: **`90015a53c7407400f87c9f5a018067849fa1e842`**
  (`origin/codex/lease-dang-exec-1`). Head khác ⇒ DỪNG.
- Head lượt trước (nền của delta): `fefa15b67a2691cf90ee8bfd0ab3880adc5f35d9`.
- Nền của packet: `cfaccff9bb373274552042e01edb4bfee81dc0ed`.
- **Đặc tả BẢN SỬA ĐỔI 2** — authority:
  ```
  git show origin/ops/lease-dang-227:ops/specs/LEASE-DANG-DUNG-MOT-LAN-r2.md > /tmp/spec_r2.md
  sha256sum /tmp/spec_r2.md   # PHẢI = 3f310582de59dce7c109717dbab13ef9467b80c67ffeafc0ac8e1484309e0093
  ```
  Nó **thay thế** bản 1 (`e1026adb…`). Bản 1 còn trong kho làm hồ sơ — **không** phải authority.
- **Verdict lượt 1**:
  ```
  git show origin/ops/lease-dang-227:ops/reviews/lease-dang-review-1-claude-verdict.md
  # sha256 = 42b438ad15fc1a8978dcd3bef023aa1f41d0926b8b87dc9c4d521229c9d6ae41
  ```
Lệch bất kỳ băm nào ⇒ DỪNG, báo cáo.

## Ba con số nền — ĐÃ ĐO LẠI ĐỘC LẬP, đừng tiêu thời gian chứng minh lại

Phiên điều phối chạy trên `90015a53`:

| phép đo | kết quả |
|---|---|
| `git diff --numstat cfaccff9..90015a53` | 3 tệp, **+498/−19** (trần 500) |
| suite, môi trường thường | `rc=0`, **58/58** |
| suite, `GITHUB_ACTIONS`+`GITHUB_REPOSITORY`+`GITHUB_ACTOR` đặt, `gh` **vắng** | `rc=0`, **58/58** y hệt |
| `actionlint .github/workflows/*.yml` | `rc=0`, 5 tệp |

Và hai phép đo cấu trúc, cũng của phiên điều phối:
- `GITHUB_ACTIONS` **không còn dòng nào** trong `ops/lease_publish.py`.
- Đồ thị lời gọi tĩnh: `kiem` · `lenh_check` · `lenh_body` **không** chạm `GOI_GH`/`_doc_gh`/
  `_kiem_loai_so_hieu`/`_kiem_comment_da_co`.
- Chạy thân bước `đăng` trích từ YAML với `gh` giả 403 ở lease **giữa**: 3 lần POST (lease cuối
  **vẫn được thử**), `GITHUB_ENV` có `DA_DOI=1`, bước `rc=1`.

## Việc của bạn — **đo, đừng đọc**

Mỗi phát hiện phải có **lệnh chạy được + đầu ra thật**. Không có phần đó thì finding **không
tồn tại**.

### A. Bảy finding lượt 1 — CÓ THẬT đóng không?

Executor khai **cả bảy ĐÃ ĐÓNG**. Đó là một lời khai; hãy đo nó. Với mỗi finding, dựng lại
**đúng phản chứng của verdict lượt 1** trên head mới và xem nó còn hiện ra không. Chú ý riêng:
- **P2** (comment người ngoài bịt lease): dựng lại **cả hai chiều** (a) người ngoài, (b)
  `lease_id` bịt lease khác.
- **P3-`[]`**: `[]` chặn nhưng `[[]]` **phải cho qua** — một issue thật sự chưa có comment.

### B. Bề mặt MỚI — chỗ lượt 1 chưa hề tồn tại

1. **Lệnh con `kiem-github`.** Nó nay là **thứ duy nhất** đứng giữa một tệp YAML và một comment
   mang danh nghĩa kho. `check` không còn gọi nó ⇒ **ai quên gọi nó thì cổng biến mất mà suite
   vẫn xanh**. Có phép đo nào bắt được việc workflow **không** gọi `kiem-github` không? Nếu
   không, đó là finding — đúng họ "cổng không nói dối, nó VẮNG MẶT".
2. **Vòng lặp `đăng` mới** bọc `set +e` quanh **mọi** lệnh. Q4 của đặc tả: *"cô lập" KHÔNG phải
   "nuốt lỗi"*. Tìm một đường mà một lỗi nay **bị nuốt** — lượt chạy XANH trong khi có chuyện
   sai. Đặc biệt: `rc=9` từ `kiem-github` ⇒ `continue` **không** đặt `BI_CHAN`. Đúng hay là một
   lỗ mới?
3. **`bao_chan()`** dùng `$tep` từ phạm vi gọi. Nó có in đúng tệp trong mọi nhánh không?
4. **Thứ tự `kiem-github` TRƯỚC `check`.** Nghĩa là lời gọi mạng xảy ra **trước** khi
   `granted_by`/`GITHUB_ACTOR`/hạn lease được kiểm. Một tệp lease rác gửi được lời gọi mạng nào
   không, và nó có quan trọng không?
5. **Neo tác giả `github-actions[bot]`.** Ai đặt được `user.login` thành chuỗi đó? Trên GitHub
   thật thì không, nhưng phép **đo** của bạn có phân biệt được "không đặt được" với "không ai
   thử" không?

### C. Chính ĐẶC TẢ r2

Bản 1 **có một lỗi thiết kế thật** và nó lọt qua lượt 1 vì không ai soi đặc tả. Bản 2 do **cùng
một người** viết, ngay sau khi mắc lỗi ấy. Soi nó:
- Q9 dời hai lớp sang `kiem-github` — có **mua thêm** bề mặt nào không (xem B.1, B.4)?
- `nghiem_thu` r2 có tiêu chí nào **không thể ĐỎ** không? (`T52` của bản 1 là đúng loại ấy.)
- `chua_do_duoc` r2 có mục nào **khai hẹp hơn thực tế** không?

### D. Chất lượng phép đo

Executor khai 13 đột biến, mỗi cái giết đúng ca của nó. **Chọn ít nhất ba** và chạy lại — gồm
**bắt buộc** hai cái này (lượt 1 chúng sống hoặc chưa tồn tại):
- `[os.environ.get("GH_PATH") or "gh", "api", …]`
- cho `kiem()` gọi mạng trở lại.

Rồi **nghĩ ra đột biến của riêng bạn** cho các chốt mới và chạy. Nghĩ ra được ca nào thì
**chạy nó** — một hướng tấn công nằm trong văn bản là một hướng đã chết.

**Mọi đột biến chạy trên BẢN SAO TẠM.** Cây review phải sạch và HEAD không đổi khi bạn xong.

## Ngoài phạm vi — ĐỪNG báo

`ngoai_pham_vi` và `chua_do_duoc` của **đặc tả r2**: không thêm `pull-requests: write` · không
cấp `GH_TOKEN` cho bước tự kiểm · không sửa R4 · không dọn 4 tệp lease thiếu `posted_comment_id`
· không dọn 7 comment trùng · không đăng lại lease lên #214 · không đổi `dung_than()` · chưa có
lượt chạy Actions thật · chưa có Windows · khe race hai nhánh `ops/**` chỉ **thu hẹp**.
Thấy một mục trong `chua_do_duoc` khai **hẹp hơn thực tế** thì ĐÓ mới là finding (mục C).

## Verdict — định dạng

```
KET_LUAN: <cross_approved | can_sua | dung_lai>
reviewed_sha: 90015a53c7407400f87c9f5a018067849fa1e842
```
Rồi từng finding: **P1/P2/P3** · một câu nêu lỗi · **lệnh + đầu ra thật** · đề xuất vá.

Kèm **bảng bảy finding lượt 1**: từng cái **ĐÓNG** (kèm phép đo của bạn) hay **KHÔNG ĐÓNG**.

Cuối verdict, hai mục bắt buộc:
- **`da_do_gi`** — đã chạy những gì, dựng lại được.
- **`khong_do_duoc`** — thứ bạn **không** đo được và **vì sao**. **"Thu hẹp"** khi nó chỉ thu
  hẹp; **"đóng"** chỉ khi có phép đo.

Đây là vòng cuối: nếu bạn kết luận `cross_approved`, hãy nói thẳng **cái gì vẫn còn hở** —
`approve` không có nghĩa là không còn gì.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
