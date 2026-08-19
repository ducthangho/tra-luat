# Cross-review lượt 4 — PR #150. PHẠM VI ĐÓNG BĂNG. CÙNG NHÀ CUNG CẤP.

Bạn là REVIEWER, provider **`claude`** (`claude-fable-5`, effort `max`) — **cùng nhà cung
cấp với người vá**. **CHỈ ĐỌC**: không sửa tệp trong kho, không commit, không push. Đột biến
chạy trên bản sao tạm.

## LƯỢT NÀY KHÔNG ĐỦ MỨC ASSURANCE ĐỂ LAND

`docs/PROTOCOL_DA_PHIEN.md` §8: workflow / security path / credential boundary / dispatcher
/ migration / LIVE adapter **phải** có cross-review khác nền tảng hoặc human review có audit;
`same_provider_approved` *"một mình không thay mức assurance bắt buộc"*.

#150 **đụng `.github/workflows/ci.yml`**. Nên dù bạn kết luận gì, lượt này là **phản biện bổ
sung**. Chủ kho đã chấp nhận sai lệch vì `codex` sắp hết quota. **Đừng viết gì hàm ý "đã đủ
điều kiện land".**

Bạn cùng nhà cung cấp với người vá ⇒ **cùng thiên kiến**. Lịch sử của chuỗi này nói rõ điều
đó có hậu quả: hai lượt `codex` đầu mỗi lượt tìm ra một finding thật mà người vá bỏ sót.
**Ưu tiên CHẠY hơn ĐỌC.**

## Neo

```
git rev-parse HEAD    # phải = 05568de6ad054a5f0c9991ecac7e38805d1227c3
```

**Lease của lượt này KHÔNG có trong cây bạn checkout** (nó được commit sau). Đọc bằng:

```
git show origin/ops/don-nhanh-giu-base-pr:ops/leases/don-nhanh-base-review-4-claude-20260817.yaml
```

`ops/leases/` trong cây bạn chỉ có lease các lượt TRƯỚC — đừng đọc nhầm.

## Phạm vi đóng băng — ĐÚNG hai tệp, ĐÚNG một thay đổi

```
git diff bfeedfc4435efde13b81e4370c84f97a5d5afc19..HEAD -- scripts/
```

`scripts/don-nhanh.ps1` (+27/−2) · `scripts/don-nhanh_test.ps1` (+43). Không gì khác.

Mọi thứ ngoài hai tệp trên — kể cả `ops/reviews/**` mà lượt này vừa thêm — ⇒ `## Nợ khai báo`.

## Thay đổi đang xét: đóng nợ `--limit`

**Vấn đề.** `gh pr list --limit N` lấy đúng N phần tử qua bao nhiêu trang cần thiết và
**không cảnh báo** khi tổng số PR mở thật sự lớn hơn N. Khi đếm trả về = N, hai trạng thái
khác nhau cho **cùng một kết quả**: *"có đúng N PR mở"* (danh sách đủ) và *"có nhiều hơn N"*
(danh sách **bị cắt** ⇒ giữ hụt base ⇒ **xoá nhầm**).

**Vá.** (1) nâng trần 200 → 1000 qua tham số mới `-TranPR`; (2) `$js.Count -ge $TranPR` ⇒
**throw** ⇒ fail-close rc=13.

Lập luận của người vá: *nâng số chỉ DỜI biên, chốt mới ĐÓNG lớp*.

## BỐN câu, tất cả ĐO ĐƯỢC

**1. Chốt có đúng biên không, và có chặn oan không.** `t17` (đếm = trần ⇒ từ chối) và `t18`
(đếm < trần ⇒ vẫn xoá). Chạy cả hai. Rồi tự dựng ca **đếm = trần − 1** và **đếm = trần + 1**
nếu bạn cho là bộ 18 ca chưa phủ.

**2. `-TranPR` LÀ MỘT THAM SỐ CÔNG KHAI MỚI — nó mở ra gì?** Người vá thêm nó *"chủ yếu để
bộ test dựng được ca chạm trần"*. Hỏi thẳng: một giá trị **ác ý hoặc ngu ngốc** làm gì?
`-TranPR 0` · `-TranPR 1` · `-TranPR -5` · giá trị khổng lồ. Có giá trị nào làm cổng **lỏng
hơn** không, hay mọi giá trị đều fail-close? **Nếu có một giá trị làm nó xoá NHIỀU hơn thì
đó là finding P1** — tham số ấy vừa được thêm vào một script XOÁ NHÁNH.

**3. Đột biến sống sót trong đúng hai tệp.** Người vá chạy ba: bản `bfeedfc` ⇒ 16/18 (đỏ
t17+t18) · M10 bỏ chốt ⇒ 17/18 (đỏ t17) · M11 đổi `-ge` thành `-gt` ⇒ 17/18 (đỏ t17). Có cái
thứ tư không? Gợi ý hướng, không giới hạn: đổi `$js.Count` thành `$prMo.Count` (sau khi đã
gộp head+base và `Sort-Object -Unique`, đếm ấy KHÁC hẳn); đặt chốt SAU khi nạp `$GiuMau`;
so với `$TranPR` sau khi nó bị ép kiểu.

**4. `$js.Count` đếm CÁI GÌ.** `$js` là mảng PR; `$prMo` là danh sách ref đã gộp head+base và
`Sort-Object -Unique`. Chốt so `$js.Count` với `$TranPR` — đó có đúng là đại lượng mà `gh
--limit` giới hạn không? Trả lời bằng phép đo, vì nếu sai đại lượng thì chốt so nhầm hai thứ
và biên nằm sai chỗ.

## Số người vá báo — kiểm lại, đừng tin

```
don-nhanh_test  18/18   pwsh 7.4.6, TMPDIR=/dev/shm
ban bfeedfc  -> 16/18, DO t17 va t18
M10 bo chot cham tran -> 17/18, DO t17
M11 -ge thanh -gt     -> 17/18, DO t17
eol ok=true checked=393 · lease_publish 31/31 · release-verify ok=true failed=0
golden rc=0 · file_count 179
```

`pwsh` **không** cài sẵn — tải PowerShell 7.4.6 linux-x64 từ GitHub release vào scratchpad
rồi chạy, và đặt `TMPDIR=/dev/shm` (sandbox khoá `/tmp`). **`/dev/shm` bị xoá khi phiên khởi
động lại** — người vá đã mất `pwsh` giữa chừng và một lượt đo trả `rc=127` với đầu ra **rỗng**,
trông y hệt "chạy xong sạch". **Kiểm công cụ có mặt TRƯỚC khi đọc bất kỳ con số nào.**

Thiếu `pwsh` ⇒ khai **KHÔNG ĐO ĐƯỢC**, đừng suy từ đọc code.

## Nợ đã khai — KHÔNG nêu lại trừ khi lời khai SAI

`-BoQuaLopPR` không kiểm gì · phụ thuộc `gh` · `.cmd` chỉ chạy Windows · `tl selftest` KHÔNG
ĐO ĐƯỢC (ba lượt trước không ai xác nhận được — giữ nguyên "chưa ai đo") · lease không nằm
trong cây được review · **hành vi phân trang THẬT của `gh` ở kho >1000 PR chưa ai đo** (bản
vá này đo hành vi của SCRIPT khi chạm trần, không đo `gh`) · `gh` bị proxy container chặn cả
REST lẫn GraphQL nên không đo sống được.

## Định dạng trả lời

```
verdict: approve | changes_requested | do_not_land
reviewed_sha: <sha40 bạn đã thật sự đọc>
assurance: same_provider_approved      # BẮT BUỘC dòng này, KHÔNG phải cross_approved

## Danh sách đóng được của lượt trước

Nợ `--limit`: ĐÓNG hay CHƯA, kèm phép thử đã chạy.

## Findings

CHỈ nhận: hồi quy · lỗ an ninh MỚI · đột biến SỐNG SÓT — trong ĐÚNG hai tệp `scripts/`.

## Nợ khai báo

## Phép đo đã chạy
```

Nguồn có thẩm quyền là tệp lease trên **đầu nhánh** (lệnh `git show` ở trên).
