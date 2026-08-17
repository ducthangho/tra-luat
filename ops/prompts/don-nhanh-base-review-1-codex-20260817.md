# Cross-review lượt 1 — PR #150 `don-nhanh`: giữ cả BASE của PR đang mở

Bạn là REVIEWER, provider `codex`. Người vá là `claude` (§8 cross-provider). **CHỈ ĐỌC** —
không sửa tệp trong kho, không commit, không push. Đột biến thì chạy trên **bản sao tạm**.

Cây: `cwd` là worktree ở đúng head cần review. Kiểm trước khi làm gì:

```
git rev-parse HEAD          # phải = 5bc635d2ea64bcedd41378cc33c6b4cdbf03f164
git diff --stat 1a6aedf6b92ff271bf07a8b9deee2f83d430ed49..HEAD   # phải = 6 tệp, +362/−16
```

## Bản vá làm gì

`scripts/don-nhanh.ps1` xoá nhánh remote đã merge. Bản trước chỉ đọc `headRefName` của PR
đang mở. Bản này đọc thêm `baseRefName`, và **từ chối xoá (thoát 13)** khi không đọc được
danh sách PR, trừ khi có cờ tường minh `-BoQuaLopPR`.

Kèm `scripts/don-nhanh_test.ps1` — 9 ca, **script này trước đó không có phản chứng nào**.

## CHỖ ĐÁNG SOI NHẤT — theo thứ tự

**1. Bộ test có đo HỢP ĐỒNG hay chỉ đo ĐỒ GIẢ.** Đây là lớp đã làm chuỗi review
`doctor-github-mcp` dài tám lượt: bốn lượt đầu reviewer đều tìm được đột biến SỐNG SÓT vì
bộ test đặc tả "cái gì phải đúng" thay vì "đúng cái gì được phép". Ở đây `git` là git thật
và "remote" là kho bare thật; chỉ `gh` là giả. Hỏi thẳng: **đồ giả `gh` có mô phỏng TRẠNG
THÁI hay đang diễn KỊCH BẢN?** Nó in cùng một JSON cho mọi lần gọi — đó là kịch bản hay là
trạng thái đúng của một danh sách PR bất biến trong một lượt chạy?

**2. Tìm đột biến SỐNG SÓT.** Người vá đã chạy ba (M1 bỏ `baseRefName`, M2 gỡ fail-close,
M3 không nạp PR vào danh sách giữ) và cả ba chết đúng ca. Ba đột biến do chính người viết
test nghĩ ra thì chỉ chứng minh test khớp với trí tưởng tượng của người ấy. Nghĩ ra cái
**thứ tư** mà bộ test không bắt được.

Vài hướng gợi ý, không giới hạn ở đây:
- đổi `Sort-Object -Unique` thành `Sort-Object`;
- bỏ `Where-Object { -not [string]::IsNullOrWhiteSpace($_) }`;
- đổi `-not $doDuocPR -and -not $BoQuaLopPR` thành `-not $doDuocPR -or -not $BoQuaLopPR`;
- làm `gh` trả **rác** (không phải JSON) — `$doDuocPR` thành gì? có đúng không?
- làm `gh` thoát khác 0 nhưng vẫn in JSON hợp lệ;
- một base tên **trùng mẫu glob** trong `$GiuMau` (ví dụ base tên `luu-tru/x`).

**3. `Duoc-Giu` khớp bằng `-like`, tức GLOB.** Tên nhánh PR đưa vào danh sách giữ **không**
được thoát. Một nhánh tên `a[bc]d` hay `x*` sẽ khớp những tên KHÁC. Hỏi: điều đó làm cổng
**chặt hơn** (giữ oan — vô hại) hay **lỏng hơn** (xoá oan — chết người)? Trả lời bằng phép
thử chạy được, đừng suy luận.

**4. Fail-close có thật sự đứng TRƯỚC mọi lệnh xoá không.** Đọc thứ tự thực thi, đừng đọc ý
định. Có đường nào tới `git push --delete` mà không đi qua chốt ấy?

**5. `-BoQuaLopPR` khi `gh` CÓ và đọc ĐƯỢC.** Lúc đó `$doDuocPR = $true` nên nhánh
`-BoQuaLopPR` không chạy. Cờ ấy có im lặng vô tác dụng trong tình huống người dùng tưởng nó
có tác dụng không? Đó là lỗi giao diện hay là đúng?

**6. Bước CI mới.** `shell: pwsh` + `run: pwsh -NoProfile -File …` — có **gọi pwsh hai lần
lồng nhau** không, và nếu có thì mã thoát của lượt trong có tới được runner không? Đây đúng
lớp lỗi `rc=0 mà rỗng` kho đã trả giá. **Dùng `actionlint` thật**, đừng dùng PyYAML: kho đã
có ca một tệp workflow PyYAML parse được mà GitHub từ chối, và **sáu lượt cross-review đều
kết luận "YAML ok"** vì cả sáu chỉ kiểm bằng PyYAML. Thiếu `actionlint` thì khai **KHÔNG ĐO
ĐƯỢC**, đừng thay bằng thứ khác.

## Số người vá báo — kiểm lại, đừng tin

```
don-nhanh_test           9/9    pwsh 7.4.6, chạy thật
bộ test trên MASTER chưa vá  5/9, đỏ đúng t1 t5 t6 t9
M1 7/9 (đỏ t1 t9) · M2 8/9 (đỏ t5) · M3 6/9 (đỏ t1 t2 t9)
actionlint 5 workflow    rc=0, nền master cũng rc=0 ⇒ delta 0
eol-policy --all         ok=true checked=377 violations=0
lease_publish            31/31
release-verify --strict  ok=true failed=0 extra=0 missing=0
golden-test rc=0, references/golden/ 0 dòng đổi
file_count               179 (KHÔNG đổi)
```

Nếu môi trường bạn thiếu `pwsh` thì **khai KHÔNG ĐO ĐƯỢC** cho mọi mục cần nó, đừng suy từ
việc đọc code. Người vá tải pwsh 7.4.6 vào container để chạy; bạn làm được thì làm.

## Nợ người vá đã tự khai — KHÔNG cần nêu lại, trừ khi lời khai SAI

1. `tl selftest` KHÔNG ĐO ĐƯỢC trong container (`pyo3_runtime.PanicException` khi tiến
   trình con nạp `cryptography`); nền `origin/master` sạch hỏng **y hệt** ⇒ delta 0.
   **Kiểm lời khai này** — nếu nền master KHÔNG hỏng thì đó là finding.
2. `-BoQuaLopPR` không kiểm gì, nó tin người gõ.
3. Lớp này phụ thuộc `gh`; máy thiếu `gh` không xoá được nếu không nêu cờ.
4. `.cmd` chỉ chạy trên Windows; hai đường sẽ trôi lệch.

## Định dạng trả lời — theo ĐÚNG thứ tự này

```
verdict: approve | changes_requested | do_not_land
reviewed_sha: <sha40 bạn đã thật sự đọc>

## Findings

CHỈ nhận: hồi quy · lỗ an ninh MỚI · đột biến SỐNG SÓT · P1 làm cổng/CI không chạy được.
Mỗi mục phải có phép thử CHẠY ĐƯỢC, không phải nhận định.

## Nợ khai báo

Mọi thứ khác. Ý hay, chỗ có thể chặt hơn, giới hạn — vào đây, KHÔNG vào Findings.

## Phép đo đã chạy

Lệnh + kết quả THẬT. Mục nào không chạy được thì ghi KHÔNG ĐO ĐƯỢC kèm lý do.
```

Nguồn có thẩm quyền là **tệp lease trong kho**, không phải comment. Băm prompt này phải khớp
`prompt_sha256_required` trong lease.
