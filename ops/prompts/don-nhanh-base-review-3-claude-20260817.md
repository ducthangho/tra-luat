# Cross-review lượt 3 — PR #150 `don-nhanh`. PHẠM VI ĐÓNG BĂNG. CÙNG NHÀ CUNG CẤP.

Bạn là REVIEWER, provider **`claude`** — **cùng nhà cung cấp với người vá**. **CHỈ ĐỌC**:
không sửa tệp trong kho, không commit, không push. Đột biến chạy trên **bản sao tạm**.

## ĐỌC MỤC NÀY TRƯỚC — lượt này KHÔNG đủ mức assurance của protocol

`docs/PROTOCOL_DA_PHIEN.md` §8: workflow, security path, credential boundary, dispatcher,
migration, LIVE adapter **phải** có cross-review khác nền tảng hoặc human review có audit;
`same_provider_approved` *"một mình không thay mức assurance bắt buộc"*.

PR này **đụng `.github/workflows/ci.yml`**, tức đúng một trong các phạm vi ấy. Nên dù bạn
kết luận gì, lượt này chỉ là **phản biện bổ sung**. Chủ kho (`ducthangho`) đã chấp nhận sai
lệch trong phiên vì `codex` sắp hết quota. Điều đó được ghi vào lease, không giấu.

**Hệ quả cho bạn:** đừng viết gì hàm ý "đã đủ điều kiện land". Kết luận của bạn KHÔNG cấp
mức assurance ấy, và nói ngược lại là một lời khai sai.

Bạn cùng nhà cung cấp với người vá nghĩa là bạn có **cùng thiên kiến** với họ. Hai lượt
trước đều do `codex` chạy và **cả hai đều tìm ra một finding thật** mà người vá bỏ sót. Nếu
bạn không tìm được gì, khả năng cao nhất **không phải** là mã đã sạch — mà là bạn đang nhìn
nó theo đúng cách người vá đã nhìn. Hãy ưu tiên **chạy** hơn **đọc**.

## Neo

```
git rev-parse HEAD    # phải = 0ce4d4917afb955c76b17df44657e88eccc6a39f
```

**Tệp lease của lượt này KHÔNG có trong cây bạn đang checkout** — nó được commit *sau* SHA
này. Đây là một nợ đã biết do reviewer lượt 2 nêu. Đọc nó bằng:

```
git show origin/ops/don-nhanh-giu-base-pr:ops/leases/don-nhanh-base-review-3-claude-20260817.yaml
```

`ops/leases/` trong cây bạn chỉ chứa lease **lượt trước** — đừng đọc nhầm nó thành lease của
lượt này.

## Phạm vi đóng băng — ĐÚNG hai tệp

```
git diff 1511dd75a5a4f65c623738f2dc91e384b96bad9a..HEAD -- scripts/
```

`scripts/don-nhanh.ps1` (+21/−4) · `scripts/don-nhanh_test.ps1` (+39/−1). Không gì khác.

Chuỗi `doctor-github-mcp` dài **chín lượt** vì người vá nới phạm vi mỗi lượt. Lượt 9 đóng
băng và `approve` ngay. Findings ngoài hai tệp trên ⇒ xuống `## Nợ khai báo`.

## Lịch sử hai lượt trước — để bạn biết đã đóng cái gì

**Lượt 1** (codex) `changes_requested`, một finding: `gh` thoát khác 0 mà vẫn in JSON hợp lệ
thì fail-close bị mở toang — script trả `rc=0` và **xoá thật**. Đã vá bằng cách bắt
`$LASTEXITCODE` ngay sau `gh`. Lượt 2 xác nhận **ĐÓNG**.

**Lượt 2** (codex) `changes_requested`, một finding: bản vá lượt 1 gộp `2>&1` rồi nối tất cả
lại, nên một dòng **cảnh báo stderr** của `gh` làm `ConvertFrom-Json` chết ⇒ **thao tác hợp
lệ bị từ chối**. Đó là delta bạn đang xét.

Hai lượt, hai finding, **cùng một hàm**. Đếm hình dạng lỗi: đây là lần thứ hai liên tiếp một
bản vá cho hàm ấy đẻ ra lỗi mới. `CLAUDE.md` có mục riêng cho hình dạng này — *"vá một lỗ mà
mở lỗ khác trong cùng hàm"*, và luật kèm theo là **cùng một hình dạng lặp ba lần trở lên thì
câu hỏi đúng là 'có nên làm việc này không', không phải 'vá thế nào'**. Bạn được phép kết
luận rằng cách đọc `gh` này nên đổi KIẾN TRÚC thay vì vá tiếp — nếu có bằng chứng.

## Ba câu hỏi, tất cả ĐO ĐƯỢC

**1. Hồi quy lượt 2 đã đóng chưa.** Dựng `gh` giả in cảnh báo ra **stderr** + `[]` ra stdout,
`rc=0`, rồi chạy `don-nhanh.ps1 -Xoa`. Đòi: `rc=0`, base của PR đang mở **được giữ**, nhánh
rác **bị xoá**. Ba vế, không phải một.

**2. Cách tách luồng có đúng trên mọi ca không.** Bản vá lọc theo kiểu
`[System.Management.Automation.ErrorRecord]`. Thử:
- `gh` in JSON ra stdout **nhiều dòng** (JSON xuống dòng) — nối lại còn parse được không?
- `gh` in cảnh báo **sau** JSON, hoặc xen giữa các dòng JSON;
- stdout rỗng nhưng stderr có nội dung, `rc=0`;
- `gh` không tồn tại nhưng có một tệp `gh` **không executable** trên PATH.

**3. Một đột biến sống sót trong đúng hai tệp.** Người vá chạy ba (bản `1511dd7`, M7 gộp lại
luồng, M8 bỏ kiểm mã thoát). Có cái thứ tư không? "Không tìm được" là kết luận hợp lệ.

## Số người vá báo — kiểm lại, đừng tin

```
don-nhanh_test  15/15   pwsh 7.4.6, TMPDIR=/dev/shm
ban 1511dd7 (SHA luot 2 da review)  ->  14/15, DO dung t14
M7 gop lai stderr vao JSON          ->  14/15, DO t14
M8 tach luong nhung bo kiem rc      ->  13/15, DO t10 va t15
actionlint rc=0 · eol ok=true checked=381 · lease_publish 31/31
release-verify ok=true failed=0 · golden rc=0 · file_count 179
```

Đo phụ trợ mà người vá đã chạy **trước khi** sửa, để chọn cách tách luồng: `gh` in cảnh báo
+ `[]`, `rc=0` ⇒ `$het.Count = 2` (1 ErrorRecord, 1 stdout), stdout nối lại `"[]"`, parse OK.
**Kiểm lại phép đo này** — nó là căn cứ của cả bản vá.

Thiếu `pwsh` thì khai **KHÔNG ĐO ĐƯỢC**. Lượt 1-2 reviewer phải đặt `TMPDIR=/dev/shm` vì
sandbox khoá `/tmp`; làm y vậy.

## Nợ đã khai — KHÔNG nêu lại trừ khi lời khai SAI

`-BoQuaLopPR` không kiểm gì · phụ thuộc `gh` · `.cmd` chỉ chạy Windows · `tl selftest` KHÔNG
ĐO ĐƯỢC trong container (cả hai lượt trước đều không xác nhận được — giữ nguyên "chưa ai đo")
· lease của lượt không nằm trong cây được review.

## Định dạng trả lời

```
verdict: approve | changes_requested | do_not_land
reviewed_sha: <sha40 bạn đã thật sự đọc>
assurance: same_provider_approved      # BẮT BUỘC ghi đúng dòng này, không phải cross_approved

## Danh sách đóng được của lượt 2

Hồi quy lượt 2: ĐÓNG hay CHƯA, kèm phép thử đã chạy và kết quả cả ba vế.

## Findings

CHỈ nhận: hồi quy · lỗ an ninh MỚI · đột biến SỐNG SÓT — trong ĐÚNG hai tệp `scripts/`.

## Nợ khai báo

## Phép đo đã chạy
```

Nguồn có thẩm quyền là **tệp lease trên đầu nhánh** (xem lệnh `git show` ở trên), không phải
tệp lease trong cây bạn checkout, và không phải comment.
