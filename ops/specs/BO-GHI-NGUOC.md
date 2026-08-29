# ĐẶC TẢ PACKET — `BO-GHI-NGUOC`

- `packet_id`: `BO-GHI-NGUOC`
- `packet_issue`: **#396**
- `mission`/sổ nợ: **#395**
- `base_sha`: `ef4098d4e1cb7b73dfda48fce202435635109dde` (master, merge PR #392 lúc 11:26:29Z 29-08-2026)
- `executor`: `claude` · `reviewer_provider`: `codex` · `assurance_target`: `cross_approved`

> **Mọi con số trong đặc tả này đo trong khoảng 12:01Z–12:35Z ngày 29-08-2026** trên
> `ef4098d4`, Linux, python 3.11.15. Đo lại trước mỗi bước công bố (soan-spec §L5).

## `nguon_cap_viec`

Phương án đã thống nhất qua 3 vòng review chéo với codex:
`https://github.com/ducthangho/tra-luat/issues/395#issuecomment-5462277546`.
Ba lượt codex `8b156117…` (223s) · `82e1332f…` (157s) · `c1a24eae…` (73s), đều `ma_thoat=0`.

Đây **không phải** packet khắc phục của một packet đã chạy hỏng; nó là thi hành lần đầu của một
phương án. Xem `hinh_dang_ke_thua`.

## `review_class`

**`sensitive`** — tính máy từ `_BANG_LOP` (`ops/lease_publish.py:59–67`):
`.github/workflows/` ⇒ `sensitive`; `ops/lease_publish.py` ⇒ `sensitive`. Lớp cao nhất thắng.

Trần ADR-0044 cho packet chạm authority: **≤3 tệp / ≤300 dòng thêm**.
Ước lượng `+10–30 / −120–220` — **âm ròng**. Đây chủ yếu là XOÁ MÃ.

> Cảnh báo của soan-spec §L5, ca `PLAT-X8`: con số dòng thêm ở đây **chống đỡ một lời khai về
> THẨM QUYỀN** (cổng ADR-0044 ĐẠT hay cần ngoại lệ người giữ kho). Vì vậy nó phải được **đo lại
> bằng `git diff --numstat` ngay trước khi mở PR**, không được chép lại từ dòng này.

## `write_set`

| # | đường dẫn | vì sao BẮT BUỘC |
|---|---|---|
| W1 | `.github/workflows/ops-publish-lease.yml` | nơi bước writeback + `git commit`/`git push` sống |
| W2 | `ops/lease_publish.py` | nơi `mark` / `_ghi_comment_id` / chốt `posted_comment_id` sống |
| W3 | `ops/lease_publish_test.py` | bộ test **GHIM** bước writeback; xem `bay_da_do` |

Đúng 3 đường dẫn, không ký tự đại diện. Đặc tả này (`ops/specs/BO-GHI-NGUOC.md`) và tệp lease
nằm trên **nhánh lease** `ops/cap-lease-bo-ghi-nguoc`, KHÔNG nằm trong write set của nhánh thi
hành — cùng quy ước với `THU-HOI-LEASE.md` trên `ops/cap-lease-bia-mo-mot-chieu`.

## `bay_da_do` — không có lát cắt 1 tệp

Đã kiểm từng dòng, đây là lý do W3 bắt buộc:

| ca | dòng | vì sao ĐỎ nếu chỉ sửa W1/W2 |
|---|---|---|
| `t52` | 2389–2396 | đọc `_buoc_workflow("ghi ngược comment id")` rồi assert lên `if:` của nó (`always()`, `env.DA_DOI == '1'`) ⇒ xoá bước ⇒ ĐỎ |
| `t25` | 748 | đòi `thay >= 4`, đếm *wrapper + check + body + **mark*** ⇒ bỏ lời gọi `mark` ⇒ ĐỎ |
| `SO_GUARD_DANG` | 2518 | cùng `t64–t68`, đòi guard `"không ghi được comment id"` |
| `t11` | 353 | ca riêng cho chính lệnh `mark` |

`t24` **KHÔNG** đỏ vì bỏ commit — nó chỉ cấm dấu bỏ-qua-CI trong dòng commit.

## `muc_tieu`

Mỗi mục chiếu vào **đúng một** đường dẫn ở `write_set` (soan-spec §L2).

1. **[W1]** Bỏ bước `ghi ngược comment id` (d.292–308) và lời gọi `mark` cùng cờ `DA_DOI`
   (d.274–290) khỏi `ops-publish-lease.yml`.
2. **[W1]** Thu quyền `contents: write` (d.49) — workflow không còn cần ghi vào kho.
3. **[W2]** Gỡ `_ghi_comment_id` (d.921–933), `lenh_mark` (d.958–962) và parser `mark` (d.1035).
4. **[W2]** Gỡ hai chốt dựa trên `posted_comment_id` (d.804–807 và d.820–823) và dòng ghi nó vào
   thân comment (d.932). Chống lặp còn lại là `_kiem_comment_da_co` (d.662) — xem `danh_doi`.
5. **[W3]** Sửa helper `_goi_lop_gh` (d.163–177) cho hermetic: **mặc định xoá `GITHUB_ACTOR`**
   khỏi môi trường con. **KHÔNG** dùng `os.environ.pop` toàn cục — quá thô, nó che mất chính ca
   cần chứng minh hành vi khi actor vắng. Ca nào cần actor thì **đặt tường minh** qua `env_them`.
6. **[W3]** Thêm ca **A/B**: spawn lại **toàn bộ** `lease_publish_test.py` dưới một `GITHUB_ACTOR`
   lạ, kèm cờ chống đệ quy để chính ca A/B không tự gọi lại mình, rồi đòi **số đạt BẰNG** lượt
   không có actor.
7. **[W3]** Tháo các ca đang GHIM bước writeback ở bảng `bay_da_do`.

## `nghiem_thu`

Mỗi tiêu chí nêu **phép đo làm nó ĐỎ** (soan-spec §L3).

| # | chiếu | tiêu chí | ĐỎ khi |
|---|---|---|---|
| A1 | 5,6,7 | `GITHUB_ACTOR=ke-la-mat python ops/lease_publish_test.py` cho **cùng số đạt** với `env -u GITHUB_ACTOR ...` | còn bất kỳ helper nào rò actor sang môi trường con |
| A2 | 5 | hoàn nguyên riêng dòng sửa helper (trả về `moi = dict(os.environ)` không xoá) ⇒ ca A/B ĐỎ | ca A/B không đổi màu ⇒ nó không đo cái nó tưởng nó đo |
| A3 | — | `t02d_GITHUB_ACTOR_khong_co_tham_quyen_bi_CHAN` vẫn ĐỎ khi gỡ chốt `GITHUB_ACTOR` khỏi `lease_publish.py` | chốt thẩm quyền mất răng — đây là **điều kiện ÂM**, packet này không được làm nó yếu đi |
| A4 | 1,2 | `grep -nE 'git commit\|git push\|contents: write\|DA_DOI\|mark' .github/workflows/ops-publish-lease.yml` ⇒ **rỗng** | còn bất kỳ đường tạo commit bot lên head PR |
| A5 | 1 | `actionlint .github/workflows/ops-publish-lease.yml` sạch (đây là `t33`) | workflow sai luật GitHub sau khi cắt bước |
| A6 | 3,4 | `python ops/lease_publish.py mark --help` ⇒ lỗi "invalid choice"; `grep -c posted_comment_id ops/lease_publish.py` ⇒ **0** | còn sót đường ghi ngược ở tầng CLI |
| A7 | tất cả | `git diff --numstat` ⇒ **3** tệp, dòng thêm **≤300** | vượt trần ADR-0044 ⇒ cần ngoại lệ người giữ kho, KHÔNG được tự khai ĐẠT |
| A8 | tất cả | suite đầy đủ đạt **124/124** trên runner có `actionlint` | bất kỳ hồi quy nào |

## `danh_doi` — khai thẳng, KHÔNG phải thay thế tương đương

Bỏ `posted_comment_id` là bỏ một chốt chạy **ĐƯỢC OFFLINE**. Nó được đọc ở
`lease_publish.py:804` (chốt **xuyên nhánh**, thuần đọc git) và `:820` (chốt trong tệp).
Thay bằng `_kiem_comment_da_co` (d.662) là đổi **offline, hai lớp** lấy **online, một lớp**.

Hàm ấy **fail-close** (d.622–629 · 631–633 · 667–681): mất mạng hoặc `gh` lỗi thì CHẶN chứ không
lọt. An toàn — nhưng **giảm tính sẵn sàng**: không có mạng thì không đăng được lease.

Kết luận sau 3 vòng review: **không tồn tại tín hiệu nào vừa offline, vừa xuyên nhánh, vừa không
do ai ghi.** Nhận đánh đổi này có ý thức.

## `ngoai_pham_vi`

| thứ KHÔNG làm | lý do đo được |
|---|---|
| bỏ chốt `GITHUB_ACTOR` | xác thực ≠ uỷ quyền; bỏ nó mở lại finding `lease-authority-spoof` mà #393 vừa vá |
| thay allowlist bằng `GET /repos/{o}/{r}/collaborators/{u}/permission` | quyền repo KHÔNG phải quyền cấp lease |
| thêm `notebyme88` vào `NGUOI_CO_THAM_QUYEN` | chủ kho đã quyết giữ nguyên một tên (12:28Z 29-08). Gate xanh lại nhờ test hermetic, không cần nới quyền. Không trộn "xoá mã" với "nới quyền" trong một diff `sensitive` |
| chữa TOCTOU | nợ CŨ, không đổi. Thứ tự thật: `_kiem_comment_da_co` → POST (W1 d.260) → `mark` (d.274–280) → `DA_DOI=1` (d.283) → push (d.292–308). `mark` xảy ra **quá muộn để làm mutex**. Chống lặp là **at-least-once**, KHÔNG được khai là exactly-once |
| cấp PAT cho bot | phân tích ở `#issuecomment-5461948700` |
| chuyển sổ lease sang Issue | đúng hướng kiến trúc, quá lớn cho đợt này |
| tối ưu `_quet_lease_toan_kho` | 61 dòng, 10.512 tree entry → 260 `(blob,path)`. Chưa có bằng chứng SLO thất bại; tối ưu cache/index dễ tạo thêm khe "không quét đủ ref" |
| bật "Dismiss stale approvals" | **0 dòng mã**, và phải đến SAU khi A4 xanh (mục 5 của #395) ⇒ đóng N10 |
| chữa `t33` thiếu `actionlint` | lỗi môi trường máy đo, không phải mã. Đã cài `actionlint` 1.7.7 tại chỗ để có ngang bằng với runner |

## `hinh_dang_ke_thua`

**`khong_ap_dung`** — và đây là lời khai có chủ ý, không phải ô để trống.

Soan-spec §L4 đòi packet **khắc phục** chép bộ đếm hình dạng lỗi từ biên nhận tiền nhiệm.
`BO-GHI-NGUOC` không phải khắc phục của một lượt chạy hỏng: nó là thi hành lần đầu của phương án
#395. Không có biên nhận tiền nhiệm nào để chép, nên bộ đếm bắt đầu từ 0 một cách hợp lệ.

Quan hệ với packet **#385 `THU-HOI-LEASE`** là **chồng lấn write set**, không phải kế thừa lỗi:
PR #388 (head `b92b401a`, base `9e6d50d`, `+219/−4`, `mergeable_state=unstable`) còn mở và chạm
W2+W3. Lease của nó đã bị thay thế **minh thị hai chiều** bởi lease của packet này.

## `chua_do_duoc`

Ghi thẳng, không giấu sau chữ "có thể":

1. **Thời lượng bước `lease-publish selftest` trên Windows.** Job `gate (windows-latest)` của run
   `33250134032` chưa từng chạy tới bước 17 — lúc 12:07Z vẫn `in_progress`, kẹt ở bước 13
   `test registry` từ 11:37:05Z. Suite spawn nhiều subprocess, mà spawn trên Windows đắt hơn
   Linux nhiều lần ⇒ **không được ngoại suy** 25s của ubuntu sang Windows. Ca A/B nhân đôi suite,
   nên nếu Windows đắt thì cái giá rơi vào đúng nền đang là nút thắt.
2. **Kết luận của `gate (windows-latest)` trên `ef4098d4`.** Nợ **N5/N6** không thuộc packet này
   và **không** bị nó đóng. Nếu Windows đỏ thì đó KHÔNG phải hồi quy do packet này.
3. **Ruleset / branch protection / required checks**: REST `repos/*` trả 403 qua proxy, MCP không
   có tool đọc. Suy được MỘT điều — *"Dismiss stale approvals" gần như chắc chắn đang TẮT*, vì 3
   bản duyệt cũ vẫn `APPROVED` sau khi head dịch. Đó là **SUY**, không phải ĐO.
4. **Push bằng `GITHUB_TOKEN` có sinh lượt chạy mới không.** Workflow d.66 khai là KHÔNG, nhưng
   đo được một ca ngược: gate run `33234750843` `created_at=04:50:01Z`, 6 giây sau commit ghi
   ngược của bot (04:49:55Z). Cơ chế CHƯA BIẾT. Packet này **xoá** đường ghi ngược nên câu hỏi ấy
   trở thành vô nghĩa về sau — nhưng nó chưa từng được trả lời, và đừng ghi là đã trả lời.
