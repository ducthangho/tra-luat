# Runbook — TÁCH DANH TÍNH GITHUB (nửa NGOÀI kho)

Packet **#348**. Tệp này là **nửa A**: phần mà phiên Claude **không làm được** và đã đo được
là không làm được. Nửa B (cổng đo người duyệt khác người tạo PR) nằm trong kho, xem
`.claude/dev/duyet_danh_tinh.py` và `.github/workflows/duyet-khac-danh-tinh.yml`.

**Đọc câu này trước mọi câu khác:** nửa B **một mình không cưỡng chế được gì**. Chừng nào
bước 2 dưới đây chưa làm — cụ thể là ô *"không cho bypass"* — thì admin đi vòng qua cổng, và
cả packet chỉ là trang trí. Thứ tự đúng là 1 → 2 → 3, và bước 2 là bước quyết định.

## Vì sao phiên không tự làm được — phép đo, không phải lời than

Đo 27-08-2026 từ trong container phiên:

```
GET /user                                     HTTP 200  CO header X-GitHub-*   -> toi GitHub that
GET /repos/…/branches/master/protection       HTTP 403  KHONG header GitHub    -> proxy tu sinh
GET /repos/…/rulesets                         HTTP 403  KHONG header GitHub    -> proxy tu sinh
GET /repos/…/collaborators                    HTTP 403  "path is not permitted through this proxy"
```

Phân biệt bằng **header**, không bằng mã trạng thái: 403 kèm header GitHub là GitHub từ chối;
403 **không** kèm header nào là proxy chặn trước khi ra tới GitHub. Cả hai đường quản trị đều
thuộc loại thứ hai. Cộng thêm: tạo credential đòi tài khoản GitHub của chủ kho, thứ không
tồn tại trong container.

Và một chỗ **KHÔNG ĐO ĐƯỢC**, ghi thẳng thay vì đoán: *đẩy thẳng lên `master` có bị chặn
không*. `git push --dry-run` làm mọi thứ **trừ** gửi bản cập nhật, nên máy chủ **chưa từng**
đánh giá branch protection — một `--dry-run` thành công **không** chứng minh đẩy được. Đo
thật nghĩa là ghi vào `master`, nên câu ấy để nguyên trạng thái thứ ba.

## Trạng thái hiện tại, đo được

| | |
|---|---|
| phiên chạy bằng | credential của `ducthangho` — vai **`admin`** |
| cộng tác viên | `ducthangho` (admin) · `code2nguyen` (write) |
| `master.protected` | `true` — **một BIT**, không phải nội dung luật |
| hành vi thật | **15 lần merge** vào master trong phiên 26–27/08, **không lần nào bị chặn** |

Bit bật mà hành vi không đổi: đó chính là lý do packet #338 kết luận cổng trong kho không
phân biệt được thẩm quyền.

## Bước 1 — danh tính chạy-việc, KHÔNG phải admin (~4 phút)

Chọn **một** trong hai. Khuyến nghị (a).

**(a) GitHub App — khuyến nghị.** App không phải người, không kế thừa vai admin, và chịu
branch protection như mọi danh tính khác.

1. https://github.com/settings/apps → **New GitHub App**
2. Repository permissions, đúng ba mục — **đừng cấp thêm**:
   - `Contents`: **Read and write** (đẩy nhánh `claude/**`)
   - `Pull requests`: **Read and write** (mở PR)
   - `Metadata`: Read (bắt buộc kèm)
   - **KHÔNG** cấp `Administration` — có nó là có lại đúng quyền vừa tách ra.
3. **Install App** → chỉ chọn kho `tra-luat`.
4. Sinh private key, giữ ngoài kho.

**(b) Fine-grained PAT của TÀI KHOẢN KHÁC.** Đăng nhập bằng tài khoản thứ hai (ví dụ
`code2nguyen`), tạo fine-grained PAT giới hạn đúng kho `tra-luat`, quyền `Contents: R/W` +
`Pull requests: R/W`. Tài khoản ấy phải ở vai `write`, **không** phải `admin`.

> Đường (b) đảo vai so với hôm nay: nếu phiên chạy bằng `code2nguyen` thì người duyệt hợp lệ
> là `ducthangho`. Cổng nửa B đúng ở cả hai chiều — nó đo *khác nhau*, không đo *ai*.

## Bước 2 — siết `master`. ĐÂY LÀ BƯỚC QUYẾT ĐỊNH (~4 phút)

Settings → Branches → Add branch protection rule → pattern `master`:

- [x] **Require a pull request before merging**
  - [x] Require approvals: **1**
  - [x] Dismiss stale pull request approvals when new commits are pushed
- [x] **Require status checks to pass before merging**
  - thêm check: **`cong`** (job của workflow *duyet khac danh tinh*)
  - *(check chỉ hiện trong danh sách sau khi nó đã chạy ít nhất một lần trên một PR)*
- [x] **Do not allow bypassing the above settings** ← **KHÔNG CÓ Ô NÀY THÌ CẢ PACKET VÔ NGHĨA**
- [x] Restrict who can push to matching branches → **không** liệt danh tính chạy-việc

Ô cuối cùng của nhóm trên là thứ duy nhất chặn admin. Bốn ô kia đều bị admin đi vòng.

## Bước 3 — trỏ phiên sang credential mới (~2 phút)

Thay `GITHUB_PAT` của môi trường phiên bằng token của danh tính bước 1. Không giữ song song
credential admin trong cùng môi trường — giữ cả hai là chưa tách gì cả.

## Bước 4 — NGHIỆM THU, và nó phải là phép ĐO chứ không phải cảm giác

Sau ba bước, bốn phép đo dưới đây **phải** ra đúng như vậy:

1. Mở một PR nháp bằng danh tính chạy-việc, chưa có ai duyệt → thử merge → **bị từ chối**.
   (Trước bước 2, phép này **thành công** — đó là đối chứng, và nó chứng minh bước 2 có tác dụng.)
2. Trên PR ấy, check **`cong`** hiện **ĐỎ** với lý do *"chưa có bản duyệt nào từ danh tính khác"*.
3. Danh tính chạy-việc tự duyệt PR của chính nó → check **vẫn ĐỎ**, lý do *"chỉ có TỰ DUYỆT"*.
4. Một danh tính khác duyệt → check **XANH** → merge được.

Phép 1 **không có đối chứng thì không nói lên gì**: phải thấy nó thành công *trước* bước 2 và
thất bại *sau* bước 2. Chỉ đo một chiều là đọc một trạng thái sẵn có thành một kết quả.

## Cái này KHÔNG chữa được, nói thẳng

- **Chủ kho vẫn có thể tự tắt bước 2.** Không cơ chế nào trong kho ngăn chủ kho đổi cài đặt
  kho của chính mình. Thứ tách danh tính mua được không phải "không thể", mà là **không thể
  làm âm thầm bằng credential mà phiên đang cầm** — đổi cài đặt là một hành động riêng, ở
  một nơi khác, dưới một danh tính khác.
- **Nửa B chưa đo được ngữ nghĩa trigger của GitHub.** Bộ phản chứng đo *hình dạng tệp*
  workflow, không đo việc `pull_request_target` thật sự lấy workflow từ nhánh cơ sở. Nợ có
  tên: `ngu-nghia-trigger-chua-do-bang-PR-doi-khang`.
- **Danh sách người được duyệt là hằng trong mã** (`NGUOI_DUOC_DUYET`). Sửa nó là sửa mã, và
  việc sửa ấy đi qua chính cổng này — cố ý như vậy.
