# Runbook — TÁCH DANH TÍNH GITHUB (nửa NGOÀI kho)

Packet **#348**. Tệp này là **nửa A**: phần mà phiên Claude **không làm được** và đã đo được
là không làm được. Nửa B (cổng đo người duyệt khác người tạo PR) nằm trong kho, xem
`.claude/dev/duyet_danh_tinh.py` và `.github/workflows/duyet-khac-danh-tinh.yml`.

**Đọc câu này trước mọi câu khác:** nửa B **một mình không cưỡng chế được gì**. Chừng nào
bước 2 dưới đây chưa làm — cụ thể là ô *"không cho bypass"* — thì admin đi vòng qua cổng, và
cả packet chỉ là trang trí. Thứ tự đúng là 0 → 1 → 2 → 3 → 4, và bước 2 là bước quyết định.

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

Hệ quả cho toàn bộ tệp này: **mọi phép ĐỌC NGƯỢC (readback) ở đây là việc của con người
trước trình duyệt, hoặc của một máy ngoài proxy này.** Phiên không xác nhận hộ được, và một
runbook nói "sau đó kiểm tra lại" mà không nói AI kiểm thì trên thực tế là không ai kiểm.

Và một chỗ **KHÔNG ĐO ĐƯỢC**, ghi thẳng thay vì đoán: *đẩy thẳng lên `master` có bị chặn
không*. `git push --dry-run` làm mọi thứ **trừ** gửi bản cập nhật, nên máy chủ **chưa từng**
đánh giá branch protection — một `--dry-run` thành công **không** chứng minh đẩy được. Đo
thật nghĩa là ghi vào `master`, nên câu ấy để nguyên trạng thái thứ ba.

## Trạng thái hiện tại, đo được

| | |
|---|---|
| phiên chạy bằng | credential của `ducthangho` — vai **`admin`** |
| cộng tác viên | `ducthangho` (admin) · `code2nguyen` (write) — đúng HAI, không có người thứ ba |
| `master.protected` | `true` — **một BIT**, không phải nội dung luật |
| hành vi thật | Git ghi nhận **15 merge commit** vào `master` trong cửa sổ 26–27/08 |

Về dòng cuối, nói đúng phạm vi phép đo (cross-review lượt 1,
`khang-dinh-khong-lan-nao-bi-chan-khong-co-receipt`): con số 15 tái lập được bằng
`git log origin/master --first-parent --merges --since=2026-08-26T00:00:00Z
--until=2026-08-28T00:00:00Z`. Bản đầu của tệp này viết thêm *"không lần nào bị chặn"* —
câu ấy **rộng hơn phép đo**: một lần merge bị máy chủ TỪ CHỐI không tạo ra object Git nào,
nên **số lần bị chặn là KHÔNG ĐO ĐƯỢC từ kho**. Thứ đo được là 15 lần THÀNH CÔNG.

Mà 15 lần thành công đã đủ nói điều cần nói: bit `protected` bật mà hành vi không đổi. Đó
chính là lý do packet #338 kết luận cổng trong kho không phân biệt được thẩm quyền.

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

## Bước 0 — BOOTSTRAP: làm cho check TỒN TẠI và KHÔNG MƠ HỒ (~6 phút)

**Bước này phải chạy TRƯỚC bước 2 và không thể đảo thứ tự.** Danh sách required check của
GitHub chỉ liệt kê những context **đã từng báo cáo**; chưa có lần chạy nào thì không có gì
để chọn, và người làm sẽ tick nhầm một dòng gần giống.

Còn một cái bẫy nữa, và nó là lý do packet này phải tách workflow (cross-review lượt 1,
`runbook-chua-tach-rieng-bang-chung-cua-check-cong`): context của một check là
`<tên workflow> / <tên job>`. Bản đầu để **cả hai lane trong một tệp**, nên job `cong` xuất
hiện **hai lần cùng một tên** — một lần từ lane tin cậy, một lần từ lane `pull_request` với
kết luận `skipped`. Người đi cấu hình không phân biệt được, và một required check mơ hồ thì
không phải một required check. Nay hai lane là hai tệp, hai `name:`:

| lane | tệp | `name:` | sự kiện | context |
|---|---|---|---|---|
| TIN CẬY | `.github/workflows/duyet-khac-danh-tinh.yml` | `duyet khac danh tinh` | `pull_request_target`, `pull_request_review` | **`duyet khac danh tinh / cong`** |
| phản chứng | `.github/workflows/duyet-phan-chung.yml` | `phan chung duyet khac danh tinh` | `pull_request` | `phan chung duyet khac danh tinh / phan-chung` |

Trình tự:

0.1 Merge PR của packet #348 → hai tệp workflow có mặt trên `master`. Lúc này cổng **chưa**
    required, nên chính lần merge ấy không bị nó chặn — cố ý, và đó là cách duy nhất để một
    cổng `pull_request_target` ra đời (nó đọc định nghĩa từ nhánh **cơ sở**).

0.2 Mở một **PR canary** (nhánh vứt đi, sửa một dòng vô hại). Trên tab Checks, đòi thấy đủ
    ba điều — thiếu một là DỪNG, đừng đi tiếp:
    - có một lượt chạy của workflow **`duyet khac danh tinh`**, `event = pull_request_target`;
    - job **`cong`** trong lượt ấy **CÓ KẾT LUẬN** (`failure` là đúng — chưa ai duyệt), **không**
      phải `skipped`;
    - **không** có context nào tên `duyet khac danh tinh / cong` đến từ lượt `pull_request`.
      Lane phản chứng phải hiện dưới tên `phan chung duyet khac danh tinh / phan-chung`.

0.3 Ghi lại `run id` của lượt 0.2. Nó là hiện vật của bước này; "tôi có thấy nó xanh" không
    phải hiện vật.

## Bước 2 — siết `master`. ĐÂY LÀ BƯỚC QUYẾT ĐỊNH (~4 phút)

Settings → Branches → Add branch protection rule → pattern `master`:

- [x] **Require a pull request before merging**
  - [x] Require approvals: **1**
  - [ ] Dismiss stale pull request approvals when new commits are pushed
        ← **để TRỐNG cho tới hết phép N4**, xem bước 4; bật SAU khi nghiệm thu xong
- [x] **Require status checks to pass before merging**
  - thêm đúng context **`duyet khac danh tinh / cong`** (chuỗi đầy đủ, không phải mình chữ `cong`)
  - [x] Require branches to be up to date before merging
- [x] **Do not allow bypassing the above settings** ← **KHÔNG CÓ Ô NÀY THÌ CẢ PACKET VÔ NGHĨA**
- [x] Restrict who can push to matching branches → **không** liệt danh tính chạy-việc

Ô "không cho bypass" là thứ duy nhất chặn admin. Bốn ô kia đều bị admin đi vòng.

**ĐỌC NGƯỢC ngay sau khi lưu** (con người, trong trình duyệt — phiên không đọc được, xem đầu
tệp): mở lại chính trang vừa lưu và đối chiếu từng ô với danh sách trên, **đặc biệt** là
chuỗi context của required check. Lưu xong mà không mở lại thì thứ được kiểm là trí nhớ.

**ĐƯỜNG LÙI, viết trước khi cần đến.** Ô "không cho bypass" áp luật lên cả admin, nên nếu
`master` kẹt (ví dụ context đổi tên và không check nào báo cáo nữa) thì **không có đường sửa
bằng API từ phiên** — REST quản trị 403 ở proxy này. Chữa: một người có vai admin, ngồi
trước trình duyệt, gỡ ô ấy ở đúng trang trên. Đừng bắt đầu bước 2 khi không có người ấy.

## Bước 3 — trỏ phiên sang credential mới (~2 phút)

Thay `GITHUB_PAT` của môi trường phiên bằng token của danh tính bước 1. Không giữ song song
credential admin trong cùng môi trường — giữ cả hai là chưa tách gì cả.

## Bước 4 — NGHIỆM THU: phải CÔ LẬP được cổng mới, không chỉ thấy nó xanh

Bản đầu của tệp này có bốn phép đo, và cross-review lượt 1 bác đúng chỗ yếu nhất: **không
phép nào tách được cổng mới ra khỏi luật `Require approvals: 1`**. Ca "chưa ai duyệt thì
merge bị chặn" được luật approval giải thích **trọn vẹn** — chạy nó xong ta vẫn chưa biết
`cong` có chặn được gì không. Một phép đo mà kết quả giống hệt nhau dù thứ đang đo có tồn
tại hay không thì không phải phép đo.

Chạy theo đúng thứ tự. **N3 là phép cô lập; đừng bỏ nó.**

**N1 — đối chứng TRƯỚC bước 2.** Mở PR nháp bằng danh tính chạy-việc, chưa ai duyệt, thử
merge → **thành công**. Phải làm *trước* khi bật bước 2. Không có chiều này thì N2 chỉ là
đọc một trạng thái sẵn có thành một kết quả.

**N2 — sau bước 2, cùng tình huống** → merge **bị từ chối**, và check `duyet khac danh tinh
/ cong` **ĐỎ** với lý do *"chưa có bản duyệt nào từ danh tính khác"*.
*(N2 một mình KHÔNG chứng minh được `cong` là thứ chặn — luật approval cũng đang chặn.)*

**N3 — CÔ LẬP status gate.** Tạm đặt **Require approvals: 0** trong bước 2, giữ nguyên
required status check. Trên chính PR ấy (vẫn chưa ai duyệt):
- luật approval nay **không** chặn gì;
- merge **vẫn bị từ chối**, và thứ duy nhất còn đỏ là `duyet khac danh tinh / cong`.
Đó là bằng chứng cổng mới tự nó chặn được. **Đặt lại Require approvals: 1 ngay sau phép này.**

**N4 — CÔ LẬP luật neo head, tức thứ cổng mới mua thêm.** Điều kiện: ô *"Dismiss stale
approvals"* đang TRỐNG (bước 2 đã dặn).
1. Người khác duyệt PR ở head `H1` → cả hai luật xanh, nút merge sáng.
2. Đẩy thêm một commit vô hại → head thành `H2`.
3. `Require approvals: 1` **vẫn thoả** (bản duyệt không bị gỡ), nhưng `cong` **ĐỎ** với lý do
   *"bản duyệt … thuộc commit KHÁC head hiện tại"*, và merge **bị chặn**.
Sau khi ghi kết quả, **bật** ô "Dismiss stale approvals" (phòng thủ nhiều lớp) và đi tiếp.

**N5 — người duyệt THOẢ branch protection nhưng NGOÀI danh sách của cổng.** Đây là ca
reviewer đòi, và nó đo đúng thứ `NGUOI_DUOC_DUYET` sinh ra để đo. Hôm nay kho có **đúng
hai** cộng tác viên và **cả hai đều nằm trong danh sách**, nên ca này không chạy được bằng
người thứ ba. Chạy được bằng cách thu hẹp danh sách:
1. Một PR nhỏ bỏ `code2nguyen` khỏi `NGUOI_DUOC_DUYET`; merge nó (lúc này `code2nguyen` vẫn
   còn trong danh sách **trên nhánh cơ sở**, nên nó duyệt được chính PR ấy).
2. Mở PR canary do danh tính chạy-việc tạo; `code2nguyen` duyệt.
3. `Require approvals: 1` **thoả**; `cong` **ĐỎ** (*"chưa có bản duyệt nào từ danh tính
   khác"*); merge **bị chặn**.
4. Hoàn nguyên bước 1. PR hoàn nguyên phải do danh tính chạy-việc tạo và do `ducthangho`
   duyệt — vì lúc này `code2nguyen` đang ở ngoài danh sách.

**N6 — chiều XANH, kẻo cả bộ trên chỉ chứng minh ta chặn được mọi thứ.** Một danh tính khác,
trong danh sách, duyệt đúng head hiện tại → `cong` **XANH** → merge được.

## Cái này KHÔNG chữa được, nói thẳng

- **Chủ kho vẫn có thể tự tắt bước 2.** Không cơ chế nào trong kho ngăn chủ kho đổi cài đặt
  kho của chính mình. Thứ tách danh tính mua được không phải "không thể", mà là **không thể
  làm âm thầm bằng credential mà phiên đang cầm** — đổi cài đặt là một hành động riêng, ở
  một nơi khác, dưới một danh tính khác.
- **Nửa B chưa đo được ngữ nghĩa trigger của GitHub.** Bộ phản chứng đo *hình dạng tệp*
  workflow, không đo việc `pull_request_target` thật sự lấy workflow từ nhánh cơ sở. Bước 0.2
  và N1–N6 là chỗ đo hành vi thật; tới khi chúng chạy, nợ vẫn mở. Nợ có tên:
  `ngu-nghia-trigger-chua-do-bang-PR-doi-khang`.
- **Danh sách người được duyệt là hằng trong mã** (`NGUOI_DUOC_DUYET`). Sửa nó là sửa mã, và
  việc sửa ấy đi qua chính cổng này — cố ý như vậy.
- **Không phép nào ở đây chạy được từ phiên.** Toàn bộ bước 0, 2 và 4 đòi một con người có
  vai admin trước trình duyệt. Runbook này là bản chỉ đường cho người ấy, không phải một
  script chờ được chạy.
