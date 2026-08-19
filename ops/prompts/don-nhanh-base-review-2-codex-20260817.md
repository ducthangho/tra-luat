# Cross-review lượt 2 — PR #150 `don-nhanh`: PHẠM VI ĐÓNG BĂNG

Bạn là REVIEWER, provider `codex`. Người vá là `claude` (§8). **CHỈ ĐỌC** — không sửa tệp
trong kho, không commit, không push. Đột biến chạy trên **bản sao tạm**.

```
git rev-parse HEAD    # phải = 1511dd75a5a4f65c623738f2dc91e384b96bad9a
```

## PHẠM VI ĐÓNG BĂNG — đọc kỹ, đây là điều kiện của lượt này

Lượt 1 đã `changes_requested` với **đúng một** finding. Lượt này chỉ hỏi **một** câu:
finding ấy đã đóng chưa, và bản vá đóng nó có đẻ ra cái gì mới không.

**KHÔNG mở rộng.** Không đề xuất ca mới ngoài phạm vi dưới, không rà lại phần lượt 1 đã
kết luận, không đòi thêm lớp. Ý hay thì cho vào `## Nợ khai báo`.

Nói thẳng vì sao: chuỗi `doctor-github-mcp` dài **chín lượt**, và nguyên nhân chính là
người vá nới phạm vi mỗi lượt — lượt 8 cả hai finding đều nhắm một ca do chính lượt 8 đẻ
ra. Lượt 9 đóng băng phạm vi và `approve` ngay. Lượt này lặp lại cách ấy có chủ đích.

## Delta cần xét — ĐÚNG hai tệp mã

```
git diff 5bc635d2ea64bcedd41378cc33c6b4cdbf03f164..HEAD -- scripts/
```

`scripts/don-nhanh.ps1` (+21/−?) · `scripts/don-nhanh_test.ps1` (+79/−?).

Hai tệp còn lại trong delta là **hồ sơ ops** (lease + prompt lượt 1) — không phải mã, bỏ qua.

## Finding lượt 1 — nguyên văn điều đã kết luận

> `gh` thoát khác 0 nhưng in JSON hợp lệ làm fail-close bị mở. Không kiểm `$LASTEXITCODE`
> ngay sau `gh`; `ConvertFrom-Json` vẫn thành công, `$doDuocPR = $true`, rồi nhánh đã merge
> bị xoá. Ca `gh` in `[]`, `exit 1`: script trả `rc=0` và xoá `ops/xong-viec`, trong khi ca
> đòi `rc=13` và remote không đổi.

## Ba câu hỏi, tất cả ĐO ĐƯỢC

**1. Finding đã đóng chưa.** Dựng lại **đúng** ca của bạn ở lượt 1 (`gh` in `[]`, `exit 1`)
và chạy `don-nhanh.ps1 -Xoa`. Đòi **hai** thứ: `rc=13` **và** remote **không đổi**. Chỉ đo
mã thoát thì một bản "in lỗi rồi vẫn xoá" vẫn xanh.

**2. Bản vá có đẻ ra đường lệch mới không.** Nó thêm một chốt thứ hai: `rc=0` mà **đầu ra
RỖNG** cũng bị coi là KHÔNG ĐO ĐƯỢC. Hỏi:
- chốt ấy có chặn **oan** đường bình thường không (`gh` in `[]`, rc=0 ⇒ phải VẪN xoá được)?
- `$tho` gom cả `2>&1`; một dòng **cảnh báo trên stderr** đi kèm JSON hợp lệ thì
  `ConvertFrom-Json` còn parse được không, hay bản vá vừa làm hỏng một ca thực tế?
  Đây là câu tôi nghi nhất về chính bản vá của mình.

**3. Một đột biến sống sót trong ĐÚNG hai tệp trên.** Lượt 1 bạn tìm được cái thứ tư khi
người vá đã chạy ba. Lượt này người vá chạy bốn (xem dưới). Có cái thứ năm **trong phạm vi
này** không? Không có thì nói "không tìm được", đó là một kết luận hợp lệ.

## Số người vá báo — kiểm lại, đừng tin

```
don-nhanh_test  13/13   pwsh 7.4.6, TMPDIR=/dev/shm
ban 5bc635d (SHA ban da review)  ->  11/13, DO t10 va t12
M4 bo kiem ma thoat gh            ->  12/13, DO t10
M5 bo kiem dau ra RONG            ->  12/13, DO t12
M6 catch van dat doDuocPR=true    ->  10/13, DO t10 t11 t12
actionlint rc=0 · eol ok=true checked=379 · lease_publish 31/31
release-verify ok=true failed=0 · golden rc=0, 0 dong doi · file_count 179
```

Bốn ca mới: `t10` gh rc≠0 + JSON hợp lệ → từ chối · `t11` rác → từ chối · `t12` rỗng → từ
chối · `t13` **đối chứng dương**, rc=0 + JSON hợp lệ → vẫn xoá bình thường.

Môi trường lượt 1 của bạn cần `TMPDIR=/dev/shm`; giữ nguyên cách ấy. Thiếu `pwsh` thì khai
**KHÔNG ĐO ĐƯỢC**, đừng suy từ đọc code.

## Người vá tự khai một lỗi của chính lượt vá này

`[string]$X = $null` trong PowerShell cho **chuỗi rỗng** chứ không cho `$null`, nên `gh` giả
in rỗng ở khắp nơi và `t1 t2 t3` đột ngột đòi `rc=13`. Đã sửa bằng
`$PSBoundParameters.ContainsKey`. **Kiểm lời khai này** — nếu cách sửa ấy vẫn còn lỗ (ví dụ
ai đó truyền `-ThoNguyen $null` tường minh) thì nói.

## Nợ đã khai, KHÔNG nêu lại trừ khi lời khai SAI

`-BoQuaLopPR` không kiểm gì · phụ thuộc `gh` · `.cmd` chỉ chạy Windows · `tl selftest`
KHÔNG ĐO ĐƯỢC trong container (lượt 1 bạn cũng không xác nhận được — giữ nguyên trạng thái
"chưa ai đo", đừng đoán).

## Định dạng trả lời

```
verdict: approve | changes_requested | do_not_land
reviewed_sha: <sha40 bạn đã thật sự đọc>

## Danh sách đóng được của lượt 1

Finding lượt 1: ĐÓNG hay CHƯA, kèm phép thử đã chạy và kết quả hai vế (rc + remote).

## Findings

CHỈ nhận: hồi quy · lỗ an ninh MỚI · đột biến SỐNG SÓT trong ĐÚNG hai tệp `scripts/`.
Ngoài phạm vi ⇒ xuống `Nợ khai báo`.

## Nợ khai báo

## Phép đo đã chạy
```

Nguồn có thẩm quyền là **tệp lease trong kho**. Băm prompt này phải khớp
`prompt_sha256_required`.
