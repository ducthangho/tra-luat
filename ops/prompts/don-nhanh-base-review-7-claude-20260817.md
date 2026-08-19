# Cross-review lượt 7 — PR #150. PHẠM VI ĐÓNG BĂNG, MỘT TỆP.

Bạn là REVIEWER, provider **`claude`** (`claude-fable-5`, effort `max`), chạy trong một
**tiến trình HOÀN TOÀN MỚI** — không có ngữ cảnh nào của phiên người vá. **CHỈ ĐỌC**.
Đột biến chạy trên bản sao tạm.

## LƯỢT NÀY KHÔNG ĐỦ MỨC ASSURANCE ĐỂ LAND

§8 đòi cross-provider cho phạm vi workflow; #150 sửa `.github/workflows/ci.yml`. `codex`
**hết quota** — đo được trong phiên cấp lease: `codex exec` chạm API và trả
`You've hit your usage limit … try again at Aug 20th, 2026 6:23 AM`. Tức KHÔNG phải lỗi
xác thực, và có ngày về cụ thể. Chủ kho chấp nhận sai lệch, có ghi.
`assurance: same_provider_approved`. **Đừng viết gì hàm ý "đã đủ điều kiện land".**

(Chi tiết đáng nhớ của phép đo ấy: `codex exec` in ERROR nhưng thoát **`rc=0`**. Đúng
doctrine kho — đừng đọc `rc` thành kết luận.)

## Neo

```
git rev-parse HEAD    # phải = a66cad6940516fe339af83cac645e3ac15d8afae
```

Lease của lượt này **không** có trong cây bạn checkout. Đọc bằng:

```
git show origin/ops/don-nhanh-giu-base-pr:ops/leases/don-nhanh-base-review-7-claude-20260817.yaml
```

## Phạm vi đóng băng — ĐÚNG MỘT TỆP

```
git diff 99e9383e9ff60bb8850f41242beb607808a821e9..HEAD -- scripts/
```

`scripts/don-nhanh_test.ps1` (+66/−7). **`don-nhanh.ps1` KHÔNG đổi.** Mọi thứ khác trong
delta là `ops/**` (verdict lượt 6, biên nhận, mục lục, bàn giao) ⇒ `## Nợ khai báo`.

## Bạn đang review CÁI GÌ

Lượt 6 ra một **P1**: chốt argv của `t21` duyệt **từng token** bằng `-contains`, tức đo sự
CÓ MẶT của token chứ không đo **CÂU HỎI** gửi đi ⇒ mù với token **THỪA**. Thêm
`--limit 30` **sau** `--limit 1000` sống 21/21, mà `gh` thật cờ-sau-thắng ⇒ limit hiệu lực
30 ⇒ tái sinh **đúng lỗ gốc** cả PR #150 sinh ra để vá.

Bản vá hiện tại có **BA LỚP**, và bạn phải xét từng lớp có răng RIÊNG hay không:

1. **Đếm + so `-ceq` TỪNG đối số** (thay cho so chuỗi đã join).
2. **Ghi argv ngăn cách byte NUL** trong `Dung-Gh-Gia` (thay cho xuống dòng).
3. `Select-Object -SkipLast 1` khi bỏ phần tử rỗng cuối (thay cho `$tok[0..(n-2)]`).

## NGƯỜI VÁ ĐÃ TỰ BẮT BA LỖI — ĐỌC KỸ, ĐỪNG TÌM LẠI CHÚNG

Nói thẳng để bạn không tiêu thời gian vào chỗ đã đóng, và để bạn biết bản vá này **đã bị
soi một lớp rồi** — nghĩa là lớp còn sống (nếu có) nằm sâu hơn ba cái này:

- **Gợi ý của reviewer lượt 6 KHÔNG đủ.** Họ đề nghị so **nguyên câu** `-ceq` trên
  `$tok -join ' '`. Người vá làm theo, rồi tự đo và thấy nó **thủng đúng lớp nó sinh ra để
  vá**: JOIN xoá mất **ranh giới đối số**, nên gộp `--json` và giá trị thành MỘT đối số
  (`"--json headRefName,baseRefName"`, 7 đối số) join lại **y hệt** 8 đối số ⇒ đột biến ấy
  **sống 21/21**. Đó là lần thứ TƯ trong kho này một bản vá mở lỗ mới trong cùng hàm.
- **`"\\0"` trong chuỗi PowerShell KHÔNG phải NUL.** PowerShell không coi `\` là ký tự
  thoát (nó dùng backtick), nên `"\\0"` ra tệp thành hai ký tự `\` `0`, `printf` in literal,
  chốt argv đọc được **đúng 1 đối số** ⇒ `t21` **ĐỎ THƯỜNG TRỰC**. Bốn đột biến vẫn "chết"
  20/21 nên bảng nhìn **y hệt** đang chạy đúng — **chỉ BASELINE lộ ra**. Từ đó mọi bảng đột
  biến của người vá chạy baseline TRƯỚC từng con.
- **`$tok[0..($tok.Count-2)]` đếm NGƯỢC khi tệp rỗng.** `Count=1` ⇒ `$tok[0..-1]`, mà
  `0..-1` trong PowerShell là dãy `0,-1` chứ không phải dãy rỗng ⇒ trả HAI phần tử, tức
  "0 đối số" báo thành 2. Hỏng theo hướng ĐỎ nên không phải lỗ, nhưng một phép đếm nói sai
  thì thông điệp chẩn đoán cũng nói sai.

## BẢY câu, tất cả ĐO ĐƯỢC

**1. Ba lớp có răng RIÊNG không.** Dựng lại và chạy: mười đột biến
(`B1` `--limit 30` sau · `B2` `--state closed` thêm · `B3` `--repo x/y` · `B4` `issue list`
· `A1`–`A4` của lượt 5 · `J1` gộp `--json`+giá trị · `J2` gộp `--state`+`open`).
**Và phản chứng cho từng lớp**, vì một lớp không có phản chứng riêng là lớp có thể đang
không có răng: (a) gỡ hẳn chốt + `B1` ⇒ phải **sống lại**; (b) `--STATE` giữ `-ceq` ⇒ chết,
hạ xuống `-eq` ⇒ **sống**; (c) `J3` = một đối số DUY NHẤT chứa xuống dòng
(`"--state`nopen"`) — có NUL ⇒ chết, hạ NUL về `\n` ⇒ **sống**; kèm đối chứng hạ NUL mà
KHÔNG đột biến ⇒ vẫn xanh (chứng minh không phải việc hạ lớp làm đỏ).
**Mọi bảng phải mở đầu bằng baseline** — xem lỗi thứ hai ở trên.

**2. Đột biến SỐNG SÓT thứ N.** Ba lượt gần nhất mỗi lượt tìm ra ít nhất một, và lượt này
người vá tự tìm ra thêm một. Còn không? Đây là câu chính.

**3. Chốt argv VẪN chỉ nằm ở `t21` — MỘT ca.** Lượt 6 đo ra không có đường chết lặng, nhưng
**mã đã đổi hoàn toàn** từ lúc ấy nên phép đo đó KHÔNG còn phủ. Đo lại: đột biến nào làm
`t21` không chạy tới khối argv (ném sớm hơn) mà suite vẫn xanh?

**4. LỜI KHAI TRONG CHÚ THÍCH.** Kho này đã cháy **bốn lần** vì một câu khẳng định sai nằm
trong comment — `t19`, `t21` (lượt 6 bắt), và hai lỗi tự bắt ở trên. Chú thích mới đưa vào
một loạt khẳng định **kiểm được**: "execve cấm byte NUL trong đối số" · "`-eq` mù
hoa-thường" · "`0..-1` đếm ngược" · "`printf '%s\0'` sinh NUL thật còn hai gạch thì không"
· "hỏng theo hướng ĐỎ". **Kiểm từng câu.** Câu nào sai là một finding, bất kể mã đúng.

**5. `argv.txt` ghi ĐÈ mỗi lần gọi.** Lượt 6 đo: script hỏi `gh` đúng **1 lần/lượt**, 19
thư mục GUID riêng, 0 rác lọt giữa các ca. Sau khi đổi cách ghi, còn đúng không? Và giữa
các CA, thư mục `gh` giả là mới hay dùng lại?

**6. NỀN WINDOWS — câu đắt nhất, và là câu mà SÁU lượt trước KHÔNG hỏi.**
`ci.yml` của nhánh này chạy bộ test trên **cả `ubuntu` lẫn `windows`**, và chú thích ngay
tại đó khai *"cả lớp hỏng của script này là lớp hỏng theo NỀN"*. Nhưng `Dung-Gh-Gia` dựng
`gh` giả là script **`#!/bin/sh`** rồi `& chmod +x`, và `printf '%s\0'` là dựng của
`/bin/sh`. Trên Windows không có `chmod`, và một tệp **không phần mở rộng** không chạy được
qua `PATH` (`PATHEXT`). Thêm: `scripts/don-nhanh_test.ps1` và bước CI gọi nó **chỉ có trên
nhánh này, KHÔNG có trên `master`** (đo được: `git ls-tree origin/master scripts/` không có
tệp test, `master:.github/workflows/ci.yml` không có bước `don-nhanh`), mà PR thường chỉ
chạy `ubuntu` ⇒ **bộ này chưa từng chạy trên Windows cho tới lượt gọi tay của phiên cấp
lease**. Đây đúng lớp `CLAUDE.md` đã trả giá (`0/103` trên `windows-latest`, "một job CI
mặc định SKIP là một cổng KHÔNG TỒN TẠI").
Kết quả lượt gọi tay ấy nằm trong lease ở khoá `do_windows`. **Đọc nó, rồi tự kết luận:**
bản vá này có làm tình trạng Windows **xấu đi**, **không đổi**, hay **tốt lên**? Nếu bộ test
vốn đã không chạy được trên Windows thì đó là **nợ có sẵn, không phải do bản vá** — nói
thẳng như vậy; nhưng nếu bản vá làm nó **thêm** phụ thuộc `/bin/sh` thì đó là finding của
lượt này. Phân biệt hai điều đó bằng phép đo, đừng bằng suy luận.

**7. Bản vá đẻ ra gì.** Kho đã có **bốn** lần bản vá đẻ lỗi mới; lần thứ tư xảy ra trong
chính bản vá bạn đang xét. Không phải nghi lễ.

## Số người vá báo — kiểm lại

```
baseline                       21/21   (pwsh 7.4.6, TMPDIR=/dev/shm; chay 8 luot rieng: 8/8)
B1 B2 B3 B4                    moi con 20/21, do t21
A1 A2 A3 A4                    moi con 20/21, do t21
J1 J2 (gop ranh gioi doi so)   moi con 20/21, do t21     <- truoc khi va: J1 SONG 21/21
PHAN CHUNG chot   : go chot + B1                  => 21/21 (B1 song lai)
PHAN CHUNG -ceq   : --STATE giu -ceq => 20/21 | ha xuong -eq => 21/21 (song)
PHAN CHUNG NUL    : J3 co NUL => 20/21 | ha NUL ve \n => 21/21 (song)
DOI CHUNG         : ha NUL ve \n, KHONG dot bien  => 21/21
printf: `printf '%s\0' a bb | od -c` => a \0 b b \0   |   ban hai gach => a \ 0 b b \ 0
dem khi rong: raw='' => 0 (truoc khi sua: 2)
lease_publish 31/31 · eol ok=true violations=[] scanned=425
```

`scanned=425` **KHÔNG** phải `398`/`401` của các lượt trước: `eol_policy.py --all` đọc
**INDEX của git** nên số đổi theo thời điểm đo, không theo mã. Đừng đọc số khác thành hồi quy.

**Môi trường, đã trả giá:**
- `pwsh` KHÔNG cài sẵn; `/dev/shm` **bị xoá giữa các phiên**. Tải 7.4.6 linux-x64; tarball
  giải nén ra `pwsh` **thiếu bit exec** ⇒ `chmod +x`. **Không** phải `/dev/shm` noexec.
  **Kiểm công cụ chạy được TRƯỚC khi đọc bất kỳ con số nào** — một lượt từng trả `rc=127`
  với đầu ra rỗng, trông y hệt "chạy xong sạch".
- **Kho có thể được clone SHALLOW.** Phiên trước đụng: `git rev-list --max-parents=0 HEAD`
  trả 5 "root commit" giả và root thật `394e9346…` **không có trong kho** ⇒ neo danh tính
  không đọc được. `git fetch --unshallow origin` rồi mới đo.
- `TMPDIR=/dev/shm` (sandbox khoá `/tmp`).
- `release-verify --strict` đỏ trong worktree review vì `nhiem_vu.txt` của harness; đo trên
  `git archive HEAD` thì xanh.
- `tl selftest` chết ở `import cryptography` (`pyo3_runtime.PanicException`) — **nợ đã khai,
  nền master hỏng y hệt ⇒ delta 0**. Nối `tail` sau pipeline sẽ nuốt rc.
- REST thẳng tới `api.github.com/repos/...` bị proxy chặn **403 bất kể token**; đường dùng
  được là **MCP github + git**.

## MỖI FINDING PHẢI KÈM GỢI Ý CÁCH VÁ

Với **mỗi** mục trong `## Findings`, thêm khối `**Gợi ý vá:**` bốn phần:

1. **Vá ở đâu** — tệp + hàm/ca, và **tại sao ở đó**.
2. **Vá thế nào** — mô tả thay đổi. Đoạn mã ngắn được, nhưng **đừng viết cả bản vá**.
3. **Ca test khoá nó**, và **đột biến nào phải chết** sau khi vá.
4. **Bản vá này có thể đẻ ra gì.**

Nhiều đường vá ⇒ nêu đường **RẺ NHẤT mà vẫn đóng lớp** trước. Thấy **không nên vá** thì nói
thẳng — "khai thành nợ" là gợi ý hợp lệ. **Gợi ý là gợi ý**: lượt 6 gợi ý một đường mà người
vá đo ra là chưa đủ, và đó là kết cục ĐÚNG chứ không phải người vá cãi bừa.

## Nợ đã khai — KHÔNG nêu lại trừ khi lời khai SAI

`-BoQuaLopPR` không kiểm gì · phụ thuộc `gh` · `.cmd` chỉ chạy Windows · `tl selftest` KHÔNG
ĐO ĐƯỢC · lease không nằm trong cây được review · `gh` phân trang thật chưa ai đo · hằng
`999`/`1000` không tự canh · đột biến pad-chuỗi tương đương hành vi · guard `Nhieu-PR` +
`[null]` (finding_2 lượt 6, **CÒN MỞ, cố ý chưa vá**) · verdict lượt 4 và 5 không có tệp
trong kho.

## Định dạng trả lời

```
verdict: approve | changes_requested | do_not_land
reviewed_sha: <sha40 bạn đã thật sự đọc>
assurance: same_provider_approved

## Danh sách đóng được của lượt 6

Finding P1: ĐÓNG hay CHƯA, kèm phép thử đã chạy. Ba lỗi người vá tự bắt: xác nhận hay bác.

## Findings

CHỈ nhận: hồi quy · lỗ an ninh MỚI · đột biến SỐNG SÓT · lời khai SAI trong chú thích —
trong ĐÚNG `don-nhanh_test.ps1`. MỖI mục kèm khối `**Gợi ý vá:**` bốn phần.

## Nợ khai báo

## Phép đo đã chạy
```
