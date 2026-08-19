Mọi phép đo đã xong và đo đúng thứ định đo: thông điệp đỏ của bản hai-gạch là đúng chữ **"gh duoc goi voi 1 doi so, hop dong doi 8"** như tự khai; khối join đúng phép so lượt 6 gợi ý và J1 sống dưới nó. Toàn bộ số người vá báo tái lập được; lượt này tìm ra **hai đột biến sống sót mới (C1, C2)** và **một lời khai lệch tầng** trong chú thích. Verdict đầy đủ:

---

verdict: changes_requested
reviewed_sha: a66cad6940516fe339af83cac645e3ac15d8afae
assurance: same_provider_approved

Lượt này **không cấp điều kiện land** (same-provider, `codex` hết quota tới 2026-08-20 — §8 chưa thoả, chủ kho đã chấp nhận sai lệch có ghi trong lease). Verdict dưới đây chỉ nói về chất lượng bản vá. Neo khớp: HEAD = `a66cad69…`, kho không shallow, delta `99e9383..HEAD` trong `scripts/` đúng một tệp `don-nhanh_test.ps1` (+66/−7), `don-nhanh.ps1` không đổi, phần còn lại toàn `ops/**`.

## Danh sách đóng được của lượt 6

**Finding P1 (chốt `-contains` mù token THỪA): ĐÓNG — và đóng bằng đường tốt hơn đường lượt 6 gợi ý.** Dựng lại đủ mười đột biến trên bản sao tạm, **mọi bảng mở đầu bằng baseline**: baseline 21/21 (3 lượt rời: 1 foreground + 2 trong bảng — đều sạch); `B1` (`--limit 30` sau) · `B2` (`--state closed` thêm) · `B3` (`--repo x/y`) · `B4` (`issue list`) · `A1`–`A4` (lượt 5) · `J1` `J2` (gộp ranh giới) — **mỗi con 20/21, đỏ đúng `t21`**, khớp từng số người vá. Lời khai `--repo` trong chú thích nay ĐÚNG (B3 chết — lượt 6 từng đo nó SAI trên bản cũ).

**Ba lớp có răng RIÊNG — cả ba phản chứng đạt:**
- *Chốt argv:* gỡ hẳn khối chốt + B1 ⇒ **21/21, B1 sống lại**.
- *Lớp `-ceq`:* `--STATE` giữ `-ceq` ⇒ 20/21 đỏ t21; hạ xuống `-eq` ⇒ **21/21, sống** (probe: `'--STATE OPEN' -eq '--state open'` → True, `-ceq` → False).
- *Lớp NUL:* `J3` (một đối số duy nhất chứa xuống dòng) có NUL ⇒ 20/21; hạ NUL về `\n` (cả ghi lẫn đọc) ⇒ **21/21, sống**; đối chứng hạ NUL mà KHÔNG đột biến ⇒ **21/21** — không phải việc hạ lớp làm đỏ.

**Ba lỗi người vá tự bắt: XÁC NHẬN cả ba bằng hành vi, không grep chuỗi.**
1. *Gợi ý lượt 6 không đủ:* dựng đúng phép so nguyên-câu-JOIN lượt 6 đề nghị (`($tok -join ' ') -ceq '…'`) rồi bơm J1 ⇒ **21/21, J1 SỐNG** — JOIN xoá ranh giới đối số đúng như khai; phép đếm+so-từng-phần-tử hiện tại giết J1/J2 (7 ≠ 8). Người vá rẽ khỏi gợi ý là kết cục đúng.
2. *`"\\0"` không phải NUL:* dựng lại bản printf hai-gạch: baseline ⇒ **20/21, t21 ĐỎ THƯỜNG TRỰC** với đúng thông điệp `"gh duoc goi voi 1 doi so, hop dong doi 8"`; chồng B1 lên ⇒ **vẫn 20/21 đỏ t21** — bảng đột biến nhìn y hệt "đang chạy đúng", **chỉ baseline lộ**. Lời khai khớp trọn, trừ một câu đếm-tầng — xem Finding 3.
3. *`0..-1` đếm ngược:* `(0..-1)` = dãy `0,-1` (2 phần tử); với `raw=''`: cách cũ đếm **2**, `Select-Object -SkipLast 1` đếm **0** — khớp "raw='' => 0 (truoc: 2)".

## Findings

### Finding 1 — P2 · đột biến sống sót: chốt argv đo LỜI GỌI CUỐI, không đo lời gọi mà kết quả ĐƯỢC DÙNG — `argv.txt` ghi `>` cho phép một lời gọi trang trí xoá dấu vết

Đột biến `C1` vào `don-nhanh.ps1` (2 dòng): lời gọi thật đổi thành `--state closed` và **kết quả của nó được dùng**; thêm một lời gọi thứ hai với câu ĐÚNG hợp đồng ngay sau, vứt kết quả. Suite: **21/21 SỐNG**. Bằng chứng chốt bị lừa chứ không phải may: chạy riêng t21 dưới C1 rồi đọc `argv.txt` — nó chứa đúng 8 đối số hợp đồng (`--state open …`) trong khi `$het` được parse đến từ câu `closed`. Trên `gh` thật đây là tái sinh đúng hậu quả lớp A3/B2 (giữ base PR ĐÃ ĐÓNG, bỏ rơi PR đang mở), và cùng cơ chế tái sinh được mọi lỗ khác (`--limit 30`, `--repo`…) miễn kèm lời gọi trang trí. Không phải hồi quy: bản `-contains` cũ mù y hệt; lượt 6 đã khai "ghi `>` vô hại hôm nay vì script hỏi đúng 1 lần/lượt" — nhưng "đúng 1 lần" hiện là thuộc tính KHÔNG CÓ CHỐT NÀO CANH, và kẻ đột biến chính là người thêm lời gọi thứ hai. Câu 5 của lượt này hỏi đích danh; đo lại ở HEAD: vẫn 1 lời gọi/lượt (19/19 `calls.log` = 1), thư mục gh GUID mới cho từng ca, 0 rác — tức lỗ chưa chảy máu ở HEAD, nhưng chốt không đóng nó.

**Gợi ý vá:**
1. **Vá ở đâu:** `Dung-Gh-Gia` (dòng dựng `printf … > argv.txt`) trong `don-nhanh_test.ps1` — vì lỗ nằm ở CÁCH GHI (đè), phép so hiện tại đã đủ sức bắt một khi bản ghi giữ đủ mọi lời gọi.
2. **Vá thế nào:** đổi `>` thành `>>` (append). Mỗi lời gọi nối thêm 8 record NUL-separated; phép đếm hiện có tự khắc thành chốt "đúng một lời gọi": hai lời gọi ⇒ 16 ≠ 8 ⇒ đỏ, không cần thêm phép so nào. Một ký tự — đường rẻ nhất mà đóng cả lớp.
3. **Ca khoá + đột biến phải chết:** vẫn `t21`. Sau vá: C1 phải 20/21 đỏ t21; baseline và cả 10 con cũ giữ nguyên kết quả (1 lời gọi/lượt đã đo nên bản ghi không đổi). Phản chứng: hạ `>>` về `>` + C1 ⇒ phải sống lại.
4. **Bản vá đẻ ra gì:** nếu mai kia `don-nhanh.ps1` chính đáng gọi `gh` lần thứ hai (phân trang), t21 đỏ và người sửa phải cập nhật hợp đồng test — đúng ý đồ "đổi hợp đồng phải sửa test" đã khai; và tệp append tồn qua nhiều lần chạy script trong CÙNG thư mục gh — hiện mỗi ca một thư mục GUID + một lần chạy nên vô hại, nhưng ai tái dùng `Dung-Gh-Gia` cho ca chạy-script-hai-lần sẽ thấy 16 record: thông điệp đếm tự giải thích, không phải lỗ.

### Finding 2 — P2 · đột biến sống sót: câu hỏi thật gửi `gh` là argv **cộng ENV** — `GH_REPO` đổi repo đích mà chốt argv không thể thấy

Đột biến `C2` (1 dòng chèn): `$env:GH_REPO = 'x/y'` ngay trước lời gọi `gh`. Suite: **21/21 SỐNG**, argv.txt vẫn đúng 8 đối số hợp đồng. Trên `gh` thật, `GH_REPO` override repo suy từ remote — `pr list` trả PR của repo KHÁC ⇒ giữ base theo PR của x/y, bỏ rơi base PR đang mở của repo này: cùng hậu quả B3 nhưng **không token nào đổi**, nên phép so nguyên-câu hoàn hảo đến đâu cũng mù. `GH_HOST` cùng lớp. Không phải hồi quy (bản cũ mù y hệt) — đây là "lớp còn sống nằm sâu hơn" đúng như prompt dự đoán: chốt tự mô tả là đo "CÂU HỎI được gửi đi", nhưng nó đo đúng một kênh của câu hỏi.

**Gợi ý vá:**
1. **Vá ở đâu:** `Dung-Gh-Gia` (script gh giả) + khối chốt t21 — cùng chỗ hợp đồng truy vấn đang được đo, không đụng `don-nhanh.ps1` (PR này là test-only).
2. **Vá thế nào:** gh giả ghi thêm một tệp riêng (`env.txt`): `printf '%s\0' "GH_REPO=${GH_REPO-}" "GH_HOST=${GH_HOST-}" > env.txt`; t21 thêm hai `bang` đòi cả hai RỖNG. ĐỪNG nhét vào `argv.txt` — đổi hình dạng bản ghi là đụng phép so đang có răng. Nói thẳng giới hạn: đây là danh-sách-cấm-theo-tên-biến, và doctrine kho đã ghi danh sách cấm không bao giờ đủ (`GH_TOKEN` đổi danh tính, `XDG_CONFIG_HOME` tráo config…) — nhưng không có allow-list rẻ cho env của tiến trình con trong test, nên: vá hai biến đổi ĐỐI TƯỢNG truy vấn (đúng lớp hậu quả vừa đo) + khai phần còn lại thành nợ có tên. **Khai toàn-bộ-thành-nợ cũng là kết cục hợp lệ** nếu chủ kho coi kênh env ngoài mô hình đe doạ của bộ test này (đột biến env là THÊM dòng mới, reviewer con người thấy ngay trong diff) — quyết là của người vá.
3. **Ca khoá + đột biến phải chết:** t21 + hai bang mới; C2 (và biến thể `GH_HOST`) phải 20/21. Phản chứng: gỡ hai bang + C2 ⇒ sống lại. Kèm chốt kiểu PR #104: đột biến NỚI điều kiện (cho phép `GH_REPO` khác rỗng) phải làm ca đích đỏ.
4. **Bản vá đẻ ra gì:** máy dev có `GH_REPO` đặt sẵn trong env ⇒ t21 đỏ oan (hiếm, thông điệp tự giải thích); trên runner GitHub Actions biến được đặt là `GITHUB_REPOSITORY` (tên khác) nên theo hiểu biết hiện tại không đỏ oan CI — **chưa đo trên runner**, người vá nên kiểm một lượt trước khi tin.

### Finding 3 — P3 · lời khai lệch tầng trong chú thích mới của `Dung-Gh-Gia`: `"\\0"` KHÔNG "đi thẳng ra tệp thành HAI ký tự"

Chú thích mới viết: *«"\\0" di thang ra tep thanh HAI ky tu `\` `0` va `printf` in ra literal»*. Đo trên pwsh 7.4.6: `"\\0".Length` = **3** (PowerShell không escape backslash — vế ĐÓ của câu đúng), và `Set-Content` ghi dòng đó ra tệp script y nguyên — od tệp: `' % s \ \ 0 '` = **BA** ký tự sau `%s`. Chỉ sau khi printf co `\\`→`\` thì BẢN GHI `argv.txt` mới còn hai ký tự (od: `a \ 0 b b \ 0`). Câu văn gán số đếm của tầng-bản-ghi cho tầng-tệp-script; ai debug bằng `od` đúng tệp mà câu chỉ vào sẽ thấy 3 ≠ 2 ngay tại chỗ chú thích dạy bài học đếm ký tự. Cơ chế tổng (printf in literal, chốt đo "1 đối số", t21 đỏ thường trực) đã xác nhận đúng ở phần trên — sai duy nhất ở chữ "ra tệp".

**Gợi ý vá:**
1. **Vá ở đâu:** comment trong `Dung-Gh-Gia` (khối "MOT dau gach cheo, khong hai") — vì kho này tính lời khai sai trong comment là finding, đã cháy bốn lần.
2. **Vá thế nào:** tách hai tầng trong một câu: ra tệp script vẫn là `\\0` (ba ký tự, PowerShell và Set-Content không đụng); printf co `\\` thành `\`, nên bản ghi argv nhận hai ký tự literal `\` `0` thay vì byte NUL.
3. **Ca khoá:** không ca máy nào canh được câu văn (cùng chỗ đứng với kỷ luật viết đã ghi trong CLAUDE.md); phép thử tay ghi kèm được: od cả hai tệp như trên.
4. **Bản vá đẻ ra gì:** đổi comment đổi hash tệp — không gate nào neo băm tệp này; rủi ro ≈ 0.

## Nợ khai báo

- **Windows (câu 6): tình trạng KHÔNG ĐỔI — nợ CÓ SẴN, không phải do bản vá.** Ba bằng chứng, hai loại: (đo tĩnh) bản `99e9383` đã có nguyên `#!/bin/sh` + `chmod +x` + `printf` trong `Dung-Gh-Gia` — bản vá chỉ đổi format bên trong script sh có sẵn, và mọi dòng PowerShell mới (`ReadAllText`/`-split`/`-SkipLast`) là .NET thuần chạy được cả hai nền; (đo CI, từ lease `do_windows`, run 32060230138 trên đúng SHA này) windows-latest **3/21**, 18 ca đỏ cùng `THIEU git tren PATH` rc=12 — chết tại `don-nhanh.ps1:128`, tức TRƯỚC `Dung-Gh-Gia` lẫn khối argv, nên phần bản vá đổi không bao giờ chạy tới trên Windows; (đo diff) dòng PATH cứng `/usr/bin:/bin` của `Chay-KichBan` — thủ phạm — không nằm trong diff. Suy ra 3 ca đạt là t4/t8/t9: ba ca duy nhất không kiểm rc, chỉ đòi "nhánh còn" — script chết sớm không xoá gì nên chúng xanh, đúng nghĩa "ca có MẶT khác ca có ĐO" (suy luận từ mã + thông điệp lỗi trong lease; log từng ca không lấy được từ phiên này). Hệ quả land giữ nguyên như lease: master chạy CẢ hai nền (đo matrix `ci.yml`) ⇒ merge nguyên trạng thì gate master đỏ ở windows — chờ chủ kho quyết, ngoài phạm vi tệp của lượt này.
- **Delta ngoài `scripts/`** đúng như khai: toàn `ops/**` (lease + prompt + verdict + receipt lượt 6, README mục lục, handoff) — không xét.
- **Nếu vá Finding 2 theo hướng env.txt:** kênh env ngoài `GH_REPO`/`GH_HOST` thành nợ có tên, cần dòng khai trong chú thích.
- **Baseline lặp:** tôi chạy 3 lượt sạch (không phải 8 như người vá) — 3/3 đủ để không nghi chập chờn, ghi để số liệu hai bên không bị đọc nhầm là mâu thuẫn.
- `tl selftest` không đo lại (nợ đã khai, `import cryptography` hỏng cả nền master; diff không đụng tl.py ⇒ delta 0 theo cấu trúc). `release-verify --strict` không đo lại (nợ môi trường `nhiem_vu.txt` đã khai; harness này cũng có tệp đó — thấy trong `git status`).
- Các nợ đã khai còn lại (`-BoQuaLopPR`, phụ thuộc `gh`, `.cmd`, phân trang thật, hằng `999`/`1000`, pad-chuỗi, guard `Nhieu-PR`+`[null]` CÒN MỞ, verdict 4/5 không có tệp): kiểm đúng như khai, không nêu lại.

## Phép đo đã chạy

Môi trường: pwsh 7.4.6 linux-x64 tải mới vào `/dev/shm` (tarball thiếu bit exec ⇒ `chmod +x`, kiểm `7.4.6` chạy được TRƯỚC khi đọc số), `TMPDIR` riêng từng lượt trong `/dev/shm`, kho không shallow, HEAD = SHA lease đòi. Mọi đột biến trên bản sao tạm trong scratchpad (mỗi con một thư mục, diff xác nhận đã áp); cây repo không bị ghi.

1. **Bảng chính 22 lượt** (mở đầu và kết thúc bằng baseline): baseline ×2 **21/21**; B1 B2 B3 B4 A1 A2 A3 A4 J1 J2 — **mỗi con 20/21 đỏ t21**; gỡ-chốt+B1 **21/21** (sống lại); ST giữ `-ceq` **20/21** / hạ `-eq` **21/21**; J3 **20/21** / hạ-NUL+J3 **21/21** / hạ-NUL-không-đột-biến **21/21**; **C1 21/21 SỐNG** · **C2 21/21 SỐNG**; S1 (không bao giờ gọi gh, vẫn rc=13) **13/21** — t21 chết đúng tại bang `Test-Path`, khớp y hệt số NOGH lượt 6 ⇒ không có đường chết lặng trên mã mới (câu 3).
2. **Xác nhận lời tự khai:** so-nguyên-câu-JOIN (gợi ý lượt 6) + J1 ⇒ **21/21 sống**; printf hai-gạch baseline ⇒ **20/21 t21 đỏ thường trực** ("goi voi 1 doi so, hop dong doi 8"), + B1 ⇒ vẫn 20/21 — chỉ baseline lộ.
3. **Instrument:** 19 thư mục gh GUID riêng = 19 ca dùng gh; `calls.log` mỗi thư mục đúng 1 byte (1 lời gọi/lượt); mỗi thư mục đúng {gh, argv.txt, calls.log} — 0 rác (câu 5). Dump argv t21 ở HEAD: 65 byte, 8 NUL, đúng 8 đối số khớp `$mong` từng byte (lời khai "dump ra đúng 8" ĐÚNG). argv t21 dưới C1: đúng 8 đối số hợp đồng — bằng chứng chốt bị lừa.
4. **Lời khai chú thích:** execve/spawn cấm NUL — `os.execv`/`subprocess` ném "embedded null byte"; pwsh đưa arg `"a`0b"` tới `/bin/sh` thì phía nhận thấy `argc=1 [a]` — NUL không có đường tới gh giả ⇒ separator không nhập nhằng. `-eq`/`-ceq`: True/False. `0..-1`: dãy `0,-1`. printf một-gạch/hai-gạch: od khớp từng ký tự số người vá báo. `Get-Content` trên argv.txt: 1 "dòng" chứa NUL nhúng (đúng "tách theo dòng làm mất ranh giới"). Cờ-SAU-thắng của `gh` thật đo offline hai chiều qua tầng validate: `--limit 5 --limit 0` ⇒ `invalid value for --limit: 0` (giá trị cuối được dùng); `--limit 0 --limit 5` ⇒ qua validate, chết ở tầng mạng. Câu duy nhất sai: Finding 3.
5. **Cổng khác:** `lease_publish_test.py` **31/31**; `eol_policy --all --json` **ok=True, violations=[], scanned=425** — khớp từng số, kể cả lời dặn 425 ≠ 398/401.
6. **Tĩnh:** `git show 99e9383:…` xác nhận `#!/bin/sh`+`chmod`+`printf '%s\n'` có sẵn bản cũ; matrix `ci.yml` nhánh này (dispatch/master/nhãn ⇒ hai nền, PR thường ⇒ ubuntu); master không có bước don-nhanh, không có tệp test.
