# Cross-review lượt 6 — PR #150. PHẠM VI ĐÓNG BĂNG, MỘT TỆP.

Bạn là REVIEWER, provider **`claude`** (`claude-fable-5`, effort `max`), chạy trong một
**tiến trình HOÀN TOÀN MỚI** — không có ngữ cảnh nào của phiên người vá. **CHỈ ĐỌC**.
Đột biến chạy trên bản sao tạm.

## LƯỢT NÀY KHÔNG ĐỦ MỨC ASSURANCE ĐỂ LAND

§8 đòi cross-provider cho phạm vi workflow; #150 sửa `.github/workflows/ci.yml`; `codex`
**hết quota**. Chủ kho chấp nhận sai lệch, có ghi. `assurance: same_provider_approved`.
**Đừng viết gì hàm ý "đã đủ điều kiện land".**

Số đo của chuỗi này: **sáu lượt, sáu lần tìm ra thứ thật.** Ba lượt gần nhất tìm ra lỗi
nằm trong **chính phần test**. Nếu bạn không tìm được gì, khả năng cao nhất không phải
"sạch" mà là "đang nhìn theo đúng cách người vá đã nhìn".

## Neo

```
git rev-parse HEAD    # phải = 99e9383e9ff60bb8850f41242beb607808a821e9
```

Lease của lượt này **không** có trong cây bạn checkout. Đọc bằng:

```
git show origin/ops/don-nhanh-giu-base-pr:ops/leases/don-nhanh-base-review-6-claude-20260817.yaml
```

## Phạm vi đóng băng — ĐÚNG MỘT TỆP

```
git diff 12dd16ea6d92a177898a78fb9a547bda1d601dbb..HEAD -- scripts/
```

`scripts/don-nhanh_test.ps1` (+57/−3). **`don-nhanh.ps1` KHÔNG đổi.** Mọi thứ khác ⇒
`## Nợ khai báo`.

## Lượt 5 tìm ra gì, và đây là bản vá cho nó

**Finding P2** — `Dung-Gh-Gia` sinh `gh` giả **mù với argv**: in cùng một JSON bất kể được
hỏi gì. Nó mô phỏng **trạng thái** nhưng không mô phỏng **hợp đồng truy vấn**, nên bốn đột
biến vào dòng gọi `gh` đều sống 21/21:
`--limit $TranPR`→`--limit 200` · bỏ hẳn `--limit` · `--state open`→`--state closed` ·
`--json headRefName,baseRefName`→`--json headRefName` (**tái tạo đúng lỗ gốc mà cả PR #150
sinh ra để vá**).

**Bản vá:** `gh` giả ghi `"$@"` ra `argv.txt` (đường dẫn **tuyệt đối**, nhúng lúc tạo);
`t21` đòi đủ sáu token `--state open --limit 1000 --json headRefName,baseRefName`.

**Kèm ba thứ nhỏ hơn, cũng từ lượt 5:**
- `t20` thêm chốt đòi dòng `cua 999 PR dang mo` — trước nó xanh-vì-lý-do-sai khi helper trả
  rỗng, và chỉ `t21` bắt được, tức `t21` từng là **điểm hỏng đơn**.
- `Nhieu-PR` thêm guard `$So -lt 1` (bẫy `1..0` chạy ngược, và bẫy unwrap mảng-đơn).
- Chú thích `t19` sửa một **lời khai sai** của người vá: "10/9 là cặp số nhỏ nhất" là sai;
  thứ nhỏ nhất là **đếm = 10**.

## SÁU câu, tất cả ĐO ĐƯỢC

**1. Chốt argv có thật sự giết bốn con kia không.** Tự dựng lại cả bốn và chạy. Người vá
báo mỗi con 20/21 đỏ `t21`. **Và phản chứng cho chính chốt:** gỡ ba dòng đòi argv ra rồi
chạy lại `--limit 200` — nó phải **sống lại** 21/21. Không có phản chứng ấy thì không biết
`t21` đang đo argv hay đo thứ khác.

**2. CHỐT ARGV CHỈ NẰM Ở `t21` — MỘT CA.** Đó lại đúng bệnh vừa chữa cho `t20` (điểm hỏng
đơn). Hỏi: đột biến nào làm `t21` **không chạy tới** phần đòi argv (ví dụ ném sớm hơn) mà
suite vẫn xanh? `t21` có `bang` trước phần argv — thứ tự ấy có làm chốt argv thành **chết
lặng** trong ca nào không?

**3. `argv.txt` GHI ĐÈ mỗi lần gọi.** Script gọi `gh` bao nhiêu lần trong một lượt? Nếu >1
thì tệp chỉ giữ lần **cuối** — chốt đang đo lời gọi nào? Và giữa các CA, thư mục `gh` giả
là mới hay dùng lại (rác của ca trước có lọt sang ca sau không)?

**4. Chốt argv dùng `-contains` trên mảng token.** Nó **không** kiểm thứ tự, không kiểm
token **thừa**, không kiểm token xuất hiện đúng chỗ. Đột biến nào lợi dụng được?
Ví dụ: thêm `--limit 30` **sau** `--limit 1000` (cờ sau thắng ở nhiều CLI) — `t21` còn đỏ
không? **Nếu không thì đây là finding P1**, vì nó là đúng lớp `--limit` vừa vá.

**5. Chốt `t20` đòi chuỗi `cua 999 PR dang mo` — ghim theo CÂU CHỮ đầu ra.** Đổi câu in
trong `don-nhanh.ps1` (việc chính đáng) sẽ làm `t20` đỏ oan. Đó có phải cái giá chấp nhận
được không, hay có đường ghim theo **hành vi** rẻ tương đương? Lượt 5 có gợi ý một đường
(cho một PR trỏ base là nhánh thật rồi đòi nhánh ấy được giữ) — nó **rẻ hơn hay đắt hơn**?

**6. Đột biến sống sót thứ tư.** Ba lượt gần nhất mỗi lượt tìm ra ít nhất một. Còn không?

## Số người vá báo — kiểm lại

```
21/21   pwsh 7.4.6, TMPDIR=/dev/shm
A1 --limit 200        -> 20/21 do t21      A2 bo --limit      -> 20/21 do t21
A3 --state closed     -> 20/21 do t21      A4 bo baseRefName  -> 20/21 do t21
PHAN CHUNG: go chot argv + A1 -> 21/21 (A1 SONG LAI)
helper-rong -> 18/21, t20 DO that (truoc chi t21 bat)
Nhieu-PR: -1->0, 0->0, 1->1, 2->2
eol ok=true checked=398 · lease_publish 31/31 · release-verify ok=true · golden rc=0
file_count 179
```

**Môi trường, đã trả giá:**
- `pwsh` KHÔNG cài sẵn. Tải 7.4.6 linux-x64; **tarball giải nén ra `pwsh` THIẾU BIT EXEC**
  (rc=126) — `chmod +x`. Không phải `/dev/shm` noexec.
- `TMPDIR=/dev/shm`. **`/dev/shm` bị xoá khi phiên khởi động lại** — một lượt đo trả `rc=127`
  với đầu ra **rỗng**, trông y hệt "chạy xong sạch". **Kiểm công cụ có mặt TRƯỚC khi đọc số.**
- `release-verify --strict` trong worktree review ĐỎ vì `nhiem_vu.txt` của harness nằm trong
  `extra_files`; đo trên `git archive HEAD` thì xanh.
- `tl selftest` chết ở `import cryptography` (`pyo3_runtime.PanicException`) — nợ đã khai,
  năm lượt đều thế. Nối `tail` sau pipeline sẽ nuốt rc; bằng chứng là **chữ ký trong output**.

## MỖI FINDING PHẢI KÈM GỢI Ý CÁCH VÁ

Với **mỗi** mục trong `## Findings`, thêm khối `**Gợi ý vá:**` bốn phần:

1. **Vá ở đâu** — tệp + hàm/ca, và **tại sao ở đó**.
2. **Vá thế nào** — mô tả thay đổi. Đoạn mã ngắn được, nhưng **đừng viết cả bản vá**: viết
   hộ cả bản vá là bạn tự biến mình thành người vá, rồi lượt sau đang review chính đề xuất
   của mình.
3. **Ca test khoá nó**, và **đột biến nào phải chết** sau khi vá.
4. **Bản vá này có thể đẻ ra gì.** Kho đã có **ba lần** bản vá đẻ ra lỗi mới; không phải
   nghi lễ.

Nhiều đường vá ⇒ nêu đường **RẺ NHẤT mà vẫn đóng lớp** trước. Thấy **không nên vá** thì nói
thẳng — "khai thành nợ" là gợi ý hợp lệ. **Gợi ý là gợi ý**: người vá được làm khác, và lượt
sau bạn không được coi "đã làm đúng theo gợi ý của tôi" là bằng chứng đúng.

## Nợ đã khai — KHÔNG nêu lại trừ khi lời khai SAI

`-BoQuaLopPR` không kiểm gì · phụ thuộc `gh` · `.cmd` chỉ chạy Windows · `tl selftest` KHÔNG
ĐO ĐƯỢC · lease không nằm trong cây được review · `gh` phân trang thật chưa ai đo · hằng
`999` của `t20` không tự canh · đột biến pad-chuỗi tương đương hành vi.

## Định dạng trả lời

```
verdict: approve | changes_requested | do_not_land
reviewed_sha: <sha40 bạn đã thật sự đọc>
assurance: same_provider_approved

## Danh sách đóng được của lượt 5

Finding P2 + ba mục nhỏ: ĐÓNG hay CHƯA, kèm phép thử đã chạy.

## Findings

CHỈ nhận: hồi quy · lỗ an ninh MỚI · đột biến SỐNG SÓT — trong ĐÚNG `don-nhanh_test.ps1`.
MỖI mục kèm khối `**Gợi ý vá:**` bốn phần.

## Nợ khai báo

## Phép đo đã chạy
```
