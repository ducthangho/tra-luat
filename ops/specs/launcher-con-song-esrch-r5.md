# ĐẶC TẢ — `LAUNCHER-CON-SONG-ESRCH` — **revision 5, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp685` (ID bền, `wp<issue>`); tên đọc được: `LAUNCHER-CON-SONG-ESRCH`. Lease dùng tên nào cũng phải kèm `packet_issue: 685`. |
| `revision` | **5** |
| `thay_the_cho` | r4 = `ops/specs/launcher-con-song-esrch-r4.md`, sha256 `2c84a1bda6e39e9a07a883a506d2a6456a09e0ee2f6229e2b2fbcdb55cc2ae67`, commit `673f00c` (`673f00ca5d0a9880170a49269161b2ca88af811e`). Trước đó: r3 = `ops/specs/launcher-con-song-esrch-r3.md`, sha256 `7ef008f83c9c5efc3ee84864da77db1428133512dd494ecf6058c37f82d1a895`, commit `f8ddd49` (`f8ddd49437d163c230a38fefdcbec582e6cdeb75`); r2 = `ops/specs/launcher-con-song-esrch-r2.md`, sha256 `de9c553aaeb4cb2dae16385e3059a5a196248230a4ed18a42016c8af6fac9ce4`, commit `cdf0575` (`cdf0575358270843fbde51f817f0d6a4d9655dec`); r1 = `ops/specs/launcher-con-song-esrch-r1.md`, sha256 `ee44238c…37d9`, commit `d96d075`. r1, r2, r3 và r4 giữ nguyên, không sửa đè; r5 là bản duy nhất được cấp lease. |
| `packet_issue` | **#685** |
| `mission_issue` | **#686** (Mission Issue, object ID `5628902742`). Thân #686 khai ngay đầu rằng nó do phiên agent đăng hộ chủ kho bằng credential chủ kho; nguồn thẩm quyền là các câu trả lời của chủ kho được trích trong đó (Q0–Q4 trong thân; Q5 ở comment `5888633201`, xem `nguon_cap_viec`). |
| `nguon_cap_viec` | (r1) Chỉ thị chủ kho 29-09-2026: *"mở packet riêng cho bản vá launcher (race ProcessLookupError) đi"*. Nguồn lỗi: PR #679, job `gate-ops (ubuntu-latest)` `109303373142`, phân tích ở PR #679 comment `5885963131`. (r2) Cross-review lượt 1 trên PR #688, reviewed commit `d96d075`: `changes_requested`, 2 P1 / 3 P2 / 0 P3; VERDICT sha256 `69dbf916648790c7452d6e0bb7fa56b3a44c59df6c568ea29a1c5bf2eba1d9fb` (viết tắt `69dbf916…d9fb`). (r3) Cross-review lượt 2 trên PR #688, reviewed commit `cdf0575` (spec sha256 khớp băm r2 ở `thay_the_cho`): `changes_requested`, **0 P1 / 2 P2 / 0 P3**; hai P1 của lượt 1 đã đóng (VERDICT lượt 2, bảng ĐỐI CHIẾU LƯỢT TRƯỚC: bốn trong năm lớp của lượt 1 ĐÃ ĐÓNG, riêng `ma-tran-loi-thieu-chot` còn mở); VERDICT sha256 `19f5faa0a210d28f3a25f94e5ff65883431c2645da19dd9354bc9e51216ba47f` (viết tắt `19f5faa0…a47f`; phiên soạn r3 đo lại băm tệp `VERDICT.md` trong hồ sơ lượt 2 lúc 11:49Z ra đúng chuỗi này), comment PR #688 `5889523704`, đăng 11:40:59Z 29-09 (phiên điều phối đọc qua API sau khi r3 soạn xong, điền vào trước khi đóng băng). Hai lớp P2 của lượt 2: `ma-tran-loi-thieu-chot`, `chot-nguoc-khong-co-lap`. (r4) Cross-review lượt 3 trên PR #688, reviewed commit `8d1e568fa4a63c9e19020b0611299019f245de8e` (là r3 ở `f8ddd49` cộng merge master `c57df32`; reviewed tree `c0d8ee82a032bfb3bb2e0396e82b52ab493e2f3e`; spec sha256 khớp băm r3 ở `thay_the_cho`): `changes_requested`, **0 P1 / 2 P2 / 0 P3**; bốn trong năm lớp của lượt 1 vẫn ĐÃ ĐÓNG (không tái phát), `ma-tran-loi-thieu-chot` **CÒN MỞ**, `chot-nguoc-khong-co-lap` **VÁ SINH LỖI MỚI** (witness cô lập W đã sửa thật, lỗi nằm ở lời khai rằng A1 khoá mặc định của helper); VERDICT sha256 `868dc562c8d6d99bcbc692feec4a5d9bcd45f3aeedb62f7510e4ff62a4b69da7` (viết tắt `868dc562…9da7`; phiên soạn r4 đo lại băm tệp `VERDICT.md` trong hồ sơ lượt 3 lúc 13:07:57Z 29-09 ra đúng chuỗi này), `HINT.patch` sha256 `2371d2d1432211a188d95f73949b0e5781f1fcf27bda17e890d90ac57de3cabd` (đo cùng lúc), comment PR #688 `5890856046`, đăng 13:02:58Z 29-09 (phiên điều phối đọc `created_at` qua REST sau khi r4 soạn xong, điền vào trước khi đóng băng). Hai lớp P2 của lượt 3 giữ slug của lượt 2: `ma-tran-loi-thieu-chot`, `chot-nguoc-khong-co-lap`. (r5) Cross-review lượt 4 trên PR #688, reviewed commit `aa1446e19a6ce3f4b51f678f466f90d4857f1776` (là r4 ở `673f00c` cộng merge master `44620e8`; reviewed tree `65504f7fb737d1fb29028c0134489833a5278b74`; spec sha256 khớp băm r4 ở `thay_the_cho`): `changes_requested`, **0 P1 / 1 P2 / 0 P3**; bốn trong năm lớp của lượt 1 vẫn ĐÃ ĐÓNG (không tái phát), `chot-nguoc-khong-co-lap` **ĐÃ ĐÓNG** (ba biểu hiện tầng đọc của lượt 3 đã đóng; phép D đủ 27 control), `ma-tran-loi-thieu-chot` **CÒN MỞ** (hai ca bắt buộc không phân biệt được "gọi PID dự phòng `os.kill(pid, 0)`" với "trả `True` ngay sau lỗi đọc"; bản sai qua cả hai ca và phép D nhưng báo "sống" cho PID con đã `wait`); VERDICT sha256 `2c479e288d61254deff91c04303cfd495a3ec33473b3ec23a7e2198ccd87665c` (viết tắt `2c479e28…665c`; phiên soạn r5 đo lại băm tệp `VERDICT.md` trong hồ sơ lượt 4 lúc 15:41:11Z 29-09 ra đúng chuỗi này), `HINT.patch` sha256 `59964a4a6b04d93cb74a96f7c416f5559b5464bd0b857be093bcd0b32612c0aa` (đo cùng lúc), comment PR #688 `5891961732`, đăng 14:07:48Z 29-09 (phiên điều phối đọc qua REST, điền vào trước khi đóng băng; phiên soạn r5 không kiểm trên GitHub). Lớp P2 duy nhất của lượt 4 giữ slug của lượt 1 và lượt 3: `ma-tran-loi-thieu-chot`. Mission #686 comment `5888633201` (Q5: điều kiện cấp lease); phiên soạn r2, r3, r4 và r5 KHÔNG đọc lại nội dung comment này, coi nó là lời khai của điều phối, và không chép điều kiện nào từ nó vào đặc tả. |
| `objective` | `_con_song` không bao giờ để một ngoại lệ `OSError` của phép hỏi `/proc/<pid>/stat` thoát ra; tiến trình biến mất giữa chừng (ESRCH) được báo là đã chết; lỗi khác KHÔNG được đọc thành "đã chết" chỉ vì không stat được, và một zombie vẫn được báo là đã chết khi nội dung `/proc/<pid>/stat` còn đọc được. |
| `review_class` | **`sensitive`** — protocol §8: *"launcher hoặc gate lifecycle"*. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | `claude` — **Claude Sonnet 5.5, effort high** (Mission #686 Q3); phiên điều phối kiểm lại độc lập và commit. |
| `environment` | **`cloud`**. Bản vá chỉ chạm nhánh Linux của `_con_song`; nhánh Windows trả về trước dòng 650. |
| reviewer | `codex` (`gpt-6-astra`, effort ≥ medium), cần `cross_approved`. Protocol §8: HINT không được chứa mã launcher; chỉ được chứa mã TEST thuần. |
| `depends_on` | Lease `ci-g5-cong-cu-chia-manh-r1-g2-claude` (packet #668) giữ `.claude/dev/launcher_test.py`, `lease_expires_at_utc` = `2026-09-30T07:41:00Z` (đọc từ tệp lease trên nhánh `ops/cap-lease-ci-g5-cong-cu-chia-manh`; `ai-dang-giu` báo `CÒN_HẠN`, `NGƯỜI_GIỮ 1`, rc=11, lúc 11:56:57Z 29-09; cùng kết quả ở 11:45:23Z). Đầu nhánh ấy đã đi từ `7c16d11` (r2) sang `2ae5646` (một commit chỉ thêm hồ sơ review #668, 11:26:38Z); tệp lease g2 giữa hai đầu nhánh KHÔNG đổi (`git diff --quiet 7c16d11 2ae5646 -- <tệp lease>` rc=0, 11:49Z). Phải nhả hoặc hết hạn trước khi cấp lease cho `wp685` (Mission #686 Q1). `.claude/dev/launcher.py`: `NGƯỜI_GIỮ 0`, rc=0 (11:56:47Z; cùng kết quả ở 11:45:12Z). Chi tiết phép đo ở §8. **Mọi số lease trong ô này là số đo của phiên soạn r3; phiên soạn r4 và r5 KHÔNG đo lại chúng (KHÔNG ĐO ĐƯỢC ở r4 và r5)** — đo lại lúc cấp lease, và không suy "người giữ 0" từ một tập ref chưa so hai nguồn. |
| nền nghiệm thu | `origin/master` `89fc4fac8cea65979cc2483043dc8cd07a6e8518` — **vẫn hợp lệ cho hai tệp trong write set** dù `origin/master` đã tiến nhiều lần từ lúc chọn nền. **Đo lại ở r5:** `git fetch -q origin master` rc=0 (15:36:08Z), `git rev-parse origin/master` ⇒ `44620e8706c86f5517b0f0e0a72759a59fd508ca` (không trôi kể từ r4), rồi `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=0** (15:36:09Z), và cùng lệnh với `-- .claude .github` ⇒ rc=0 (15:36:10Z; chi tiết §8). Đo lại ở r4: `git fetch -q origin master` rc=0, `git rev-parse origin/master` ⇒ `44620e8706c86f5517b0f0e0a72759a59fd508ca` (Merge PR #684, commit lúc 12:39:55Z), rồi `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=0** (13:07:30Z 29-09), và không tệp nào dưới `.claude/` hay `.github/` đổi (rc=0 cùng lúc; chi tiết §8). Ở r3 cùng phép đo ra rc=0 với `1c23933` (11:44Z) và `c57df32` (11:56:41Z). Đầu `origin/master` sẽ còn trôi: đo lại lúc cấp lease. Nền tiếp nối (continuation base) sẽ khác khi #668 land trước; khai riêng lúc cấp lease, không thay nền này (protocol §3.2.1). |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/launcher-con-song-esrch-r5.md`, không loại dòng nào. Giá trị được công
bố **ngoài** tệp: comment trên #685 và lease, kèm OID commit + đường dẫn. Khối closure dưới đây
nằm **trong** tệp, nên một `spec_hash` không thể đi với hai closure khác nhau. Đổi bất kỳ byte nào
⇒ revision mới, băm mới, lease mới. Băm của r1 (`ee44238c…37d9`), của r2 (`de9c553a…9ce4`), của r3
(`7ef008f8…a895`) và của r4 (`2c84a1bd…ae67`) KHÔNG còn dùng để cấp lease.

**Closure đóng băng** (các trường dispatcher dẫn xuất, protocol §3.2), điền tay theo **miễn trừ có
phạm vi** ở Mission Issue #686: chỉ `wp685`, hết hiệu lực ở lần đầu một policy canonical cho closure
xuất hiện trên nhánh mặc định.

| trường | giá trị |
|---|---|
| `change_policy_sha` | `null` — chưa có policy canonical; descriptor thay thế là miễn trừ ở #686 |
| `effective_write_set` | `.claude/dev/launcher.py` · `.claude/dev/launcher_test.py` (exact) |
| `effective_review_class` | `sensitive` |
| `required_checks` | Trên PR thi hành: `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-registry (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)` của `.github/workflows/ci.yml`, workflow `thu-hoi` — các job này có thật và phải xanh, nhưng **KHÔNG job nào trong số đó chạy `launcher_test.py`** (`gate-registry` chạy chín bộ thuộc `MOI`, không có `launcher_test.py`; xem §8). Ngoài các check CI, **bắt buộc** bằng chứng cục bộ Linux B1–B6 neo exact candidate SHA (lệnh nguyên văn, giờ UTC, rc, dòng tổng), đính vào handoff và reviewer đọc trước merge; cross-review codex `cross_approved`, 0 P1/P2/P3 |
| `land_obligations` | Chủ kho audit + merge (không tự merge/approve); đọc kết quả `launcher-windows.yml` ở lượt `push` lên master sau merge, cả job Windows lẫn job Ubuntu, và báo; ghi sổ verdict + HINT vào `ops/reviews/` kèm receipt và mục README; thu hồi lease sau land; đóng #685 |

**Descriptor nguồn closure** = `{mission_issue: 686, object_id: 5628902742}`. Lease phải **chép**
đúng các giá trị trên; lệch ⇒ **DỪNG**. Băm thân Issue ở phía nhận là **KHÔNG ĐO ĐƯỢC** từ phiên
soạn (đường đọc MCP chuẩn hoá thực thể HTML trong thân issue, xem CLAUDE.md), nên neo bằng object
ID + số Issue.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

**Thay đổi so với r4** (mỗi dòng ứng với một lớp của VERDICT lượt 4, hồ sơ cross-review PR #688; slug là
tên lớp trong bảng lớp của VERDICT; các số trong bảng này là số HIỆN HÀNH của r5, còn các bảng lịch sử bên dưới
giữ số của revision cũ). r5 áp `HINT.patch` của lượt 4 (13 hunk, 21599 byte, sha256 `59964a4a…c0aa`) lên bản
sao r4. HINT nhắm r4 nên đường dẫn phải đổi trước khi áp — và **chỉ được đổi hai dòng tiêu đề của patch**
(`sed '1,6s#launcher-con-song-esrch-r4.md#launcher-con-song-esrch-r5.md#'`), không đổi thân: hunk 1 của HINT
lượt 4 có một dòng NGỮ CẢNH nhắc chính tên `launcher-con-song-esrch-r4.md` (r4 đã dùng `sed` toàn cục cho HINT
lượt 3, khi thân patch chưa nhắc tên tệp; cách đó không dùng lại được). Đo 15:41:18Z 29-09 trên hai bản sao r4
riêng: `sed` toàn cục ⇒ `patch -p0 --fuzz=0` **rc=1**, `Hunk #1 FAILED at 46`, 12 trong 13 hunk qua; `sed` chỉ
tiêu đề ⇒ **rc=0**, cả 13 hunk, không tệp `.orig` hay `.rej`, 947 dòng, sha256 bản chỉ-HINT `99eaceb9…cc95`.
Sau đó r5 viết lại lời văn quanh HINT và rà mọi chỗ lặp lại con số hoặc danh sách mà lớp làm đổi (hàng thứ ba):

| slug lớp | hạng | chỗ sửa trong r5 |
|---|---|---|
| `ma-tran-loi-thieu-chot` | P2 | Đóng THEO LỚP chứ không theo hunk. §7 B2 thêm nhãn `B2-pid-du-phong`: bốn tiểu nhãn `song`, `da-wait`, `eperm`, `eio`, mỗi tiểu nhãn chạy tám đầu vào đọc (ba lỗi đọc EACCES/EIO/ESRCH và năm lần đọc parse của `B2-parse`: p1, p2, hai payload của p3, p4) = 32 lời gọi trực tiếp. Phủ: chiều kết quả của PID dự phòng (sống ⇒ `True`, đã `wait` ⇒ `False`, EPERM ⇒ `True`, EIO ⇒ `False`); quan sát đúng MỘT lời gọi `kill(pid, 0)` cho mỗi đầu vào; toàn bộ miền lỗi đọc và parse; mutant bỏ bước quyết định PID. B5 thêm lớp (k) ⇒ **mười một LỚP**. Các tổng đổi: mục `DOT_BIEN` 15 → **19**; cặp (dòng, ca đích) 16 → **20**; bảng sản phẩm 189 → **193**, kèm harness 192 → **196**; nhãn 13 → **14**; đơn vị assertion 22 → **26**; control của D 27 → **32** (13 → 14 mức nhãn, 14 → 18 mức tiểu nhãn); số ca đăng ký **191** không đổi. §1 thêm bảng 6; ma trận, bảng tiểu nhãn, §8, §9, §10 cập nhật cùng lúc; số của r4 chuyển thành lịch sử |
| `chot-nguoc-khong-co-lap` | P2 (ĐÃ ĐÓNG ở lượt 4) | Không đổi ngữ nghĩa phép D, A1/A2/W1/W0. Chỉ cập nhật số hạng theo nhãn mới (26 đơn vị, 32 control) và đoạn "Đã đo" (lượt 4 đã đo 27 control và thứ tự; r5 đo lại với nhãn mới) |
| (r5 tự thêm, ngoài HINT) | — | (1) Dòng (k) của HINT là MỘT dòng ở tiểu nhãn `song`; r5 tách thành bốn dòng (k1)–(k4), mỗi dòng chết ở một tiểu nhãn kết quả khác nhau, vì mutant duy nhất của HINT chết bằng bộ đếm ở `song` nên ba kết quả còn lại không có mutant độc chiếm (bảng 6, đã đo). Hệ quả: 19 mục / 20 cặp / 193 / 196 thay cho 16 / 17 / 190 / 193 mà HINT suy ra. (2) Q-A.4 làm rõ, không đổi ngữ nghĩa: ngữ nghĩa "sẵn có" của khối `kill` gồm cả `OSError` khác ⇒ `False`, và bước ấy phải THỰC SỰ được gọi. (3) Đo lại trên rig sao chép: ma trận 32 đầu vào, D 32 control, 20 cặp, runner, kiểm kê 191 / 193 / 3 / 196, ba phép đảo thứ tự, ruff nền, nền nghiệm thu (bảng 6, B5, §8, §10). (4) Bỏ khối "Bổ sung sau cross-review lượt 4" ở cuối §10 mà HINT thêm vào: nó lặp các số cũ (15 mục, 16 cặp, 17 cặp) ở chỗ thứ hai; số nay chỉ nằm ở B5, §8 và bảng này. (5) §9 ghi lần thứ năm của hình dạng "vá đúng chỗ được chỉ rồi bỏ sót" (kèm bản HINT ở cỡ nhỏ). (6) Lệnh áp HINT chỉ đổi tiêu đề patch (đoạn trên) |

**Lịch sử r3 → r4 trước cross-review lượt 4** (các số trong bảng này là số lịch sử;
số nghiệm thu sau bổ sung ở §7 và §8). Mỗi dòng ứng với một lớp của VERDICT lượt 3, hồ sơ cross-review PR #688; slug là
tên lớp trong bảng lớp của VERDICT. r4 áp `HINT.patch` của lượt 3 lên bản sao r3. HINT nhắm r3 nên đường
dẫn được đổi trước khi áp bằng `sed` (thay `launcher-con-song-esrch-r3.md` bằng
`launcher-con-song-esrch-r4.md`), rồi `patch -p0 --fuzz=0` ⇒ rc=0, không hunk bị từ chối (đo lại trên một
bản sao riêng lúc 13:12:35Z 29-09; lần áp thật lúc soạn cho cùng kết quả và cùng 714 dòng). Bản chỉ-HINT
đó có sha256 `7bd71d25d78464fad44a8a0c9080a7e0be6b0629a8328fbd91c06b76743348d0`. Sau đó r4 viết lại phần
lời văn quanh HINT, rà mọi chỗ lặp lại con số hoặc danh sách mà hai lớp làm đổi (số lớp và số mục đột
biến, số ca, ma trận, danh sách "KHÔNG ĐO ĐƯỢC", lời tổng kết), và sửa hai chỗ HINT để lại: dòng bảng
"Thay đổi so với r2" mô tả r3 bị HINT viết chen con số của r4 (r4 trả lại nguyên văn r3 ở bảng lịch sử
bên dưới), và danh sách B5 dùng tên nhãn không định dạng. r4 cũng bổ sung bốn thứ ngoài HINT, nêu ở dòng
cuối bảng:

| slug lớp | hạng | chỗ sửa trong r4 |
|---|---|---|
| `ma-tran-loi-thieu-chot` | P2 | Đóng THEO LỚP chứ không theo hunk. §7 B2: `B2-doc-hong` từ một đầu vào (EACCES) thành ba (`EACCES`, `EIO`, `ESRCH`, mỗi cái `True`); `B2-tin-hieu` từ một thành hai (`hoi`, `doc`); ESRCH ở tầng hỏi (`B1`, kỳ vọng `False`) và ESRCH ở tầng đọc (`B2-doc-hong` tiểu nhãn `ESRCH`, kỳ vọng `True`) là hai nhãn khác nhau, kỳ vọng ngược nhau. Ma trận tầng × miền **hết ô "KHÔNG ĐO ĐƯỢC"**; thêm **bảng tiểu nhãn** (22 đơn vị). §1 thêm bảng 5 (đo của lượt 3). B5 vẫn **mười LỚP**, kỳ vọng **mười lăm mục `DOT_BIEN`** (từ mười hai) vì (d), (e), (g) mỗi lớp thành hai dòng — mỗi biến thể sai reviewer đã dựng có một dòng giết nó: (d2) đọc chỉ bắt `PermissionError`, (g2) ESRCH ở đọc ⇒ `False`, (e2) nuốt riêng `KeyboardInterrupt` ở đọc. Số mục `DOT_BIEN` sản phẩm sau packet 174 + 15 = 189 (192 kèm harness); ca đăng ký vẫn 191; mười sáu cặp (dòng, ca đích). §3 Q-A.4 nói rõ ESRCH ở tầng đọc; §9 và §10 cập nhật |
| `chot-nguoc-khong-co-lap` | P2 | §7 B5 thêm **phép (D)**: quan sát độc lập thứ `bang` đã thực sự chạy ở ca đăng ký khi dùng mặc định của helper, so với bảng tiểu nhãn viết cứng theo §7; **27 control** bắt buộc (13 mức nhãn — đã đo 13/13 đỏ trên rig lượt 3 — và 14 mức tiểu nhãn, chưa đo); câu "chính A1 khoá mặc định" của r3 bị sửa: A1 không khoá được điều đó. Tiêu chí A1/W1 thêm điều kiện khớp tiểu nhãn; log B6 phải có D; §10 sửa lời khai về mặc định của helper |
| (r4 tự thêm, ngoài HINT) | — | (1) Bảng tiểu nhãn và điều kiện khớp tiểu nhãn ở A1/W1, kèm control mức tiểu nhãn và phép so thứ tự cho D — vì D chỉ ở mức nhãn thì một mặc định bỏ MỘT đầu vào bên trong nhãn vẫn lọt; riêng đầu vào `EIO` của `B2-doc-hong` không có đột biến độc chiếm (đột biến (d2) làm cả `EIO` lẫn `ESRCH` ở tầng đọc thoát, chỉ tiểu nhãn báo `EIO` phân biệt được); (2) §8 đo lại nền lúc 13:07Z (master trôi tới `44620e8`, hai tệp write set vẫn giống hệt); (3) §9 ghi lần thứ tư của hình dạng "vá đúng chỗ được chỉ rồi bỏ sót" và §10 dọn các câu lỗi thời của r3 (ví dụ câu nói ID comment lượt 2 "KHÔNG có" trong khi `nguon_cap_viec` đã có); (4) §1 rút khối mã launcher từ hai dòng còn một dòng (đúng quy ước không đưa mã launcher vào đặc tả, protocol §8) |

**Lịch sử: thay đổi r2 → r3** (mỗi dòng ứng với một lớp của VERDICT lượt 2; nguyên văn bảng của r3, trừ
đường dẫn; các số ở đây là số CỦA r3, không phải số hiện hành — số hiện hành ở B5 và §8):

| slug lớp | hạng | chỗ sửa trong r3 |
|---|---|---|
| `ma-tran-loi-thieu-chot` | P2 | §3 Q-A.5 viết lại và thêm đoạn làm rõ nội dung hỏng; §1 thêm bảng 3 và bảng 4 (đo lại 11:46Z); §7 B2 thêm ba nhãn `B2-exception`, `B2-parse`, `B2-dem-doc` kèm **ma trận tầng × miền**; B5 từ bảy lên **mười LỚP** đột biến (thêm (h), (i), (j)), kỳ vọng **mười hai mục `DOT_BIEN`** vì (h) và (j) mỗi lớp cần hai vị trí; §9 viết lại lời tổng kết |
| `chot-nguoc-khong-co-lap` | P2 | §7 B5: câu chốt ngược của r2 thay bằng **hai phép đo** — (A) ca đầy đủ, (W) witness cô lập cùng helper — kèm bảng assertion còn hiệu lực và tiêu chí đạt; §6.2 và quy ước chung §7 nêu hợp đồng helper |
| (r3 tự thêm, ngoài HINT) | — | §1 bảng 4 và §2: quan sát đo được về `comm` không phải UTF-8; §7 B2-parse có dạng nội dung thứ tư (không giải mã được); B5 nêu quy tắc **mục `DOT_BIEN` theo ô của ma trận**; §8 đo lại nền, lease, ruff; §9 thêm lượt 2 vào bộ đếm hình dạng; §10 cập nhật |

**Lịch sử: thay đổi r1 → r2** (mỗi dòng ứng với một lớp của VERDICT lượt 1):

| slug lớp | hạng | chỗ sửa trong r2 |
|---|---|---|
| `qa-fallback-mat-zombie` | P1 | §1 (thêm bảng zombie), §3 Q-A viết lại, §6.1, §7 B2/B3, B5 |
| `so-muc-dot-bien-mau-thuan` | P1 | §6.2 trỏ vào B5; B5 là danh sách đột biến có thẩm quyền duy nhất |
| `ci-dang-ky-khong-thuc-thi` | P2 | closure `required_checks`, §5, §7 B6, §8 |
| `ma-tran-loi-thieu-chot` | P2 | §7 B2 (EIO, tín hiệu ngoài `OSError`, đếm lần gọi, đọc hỏng), B5 |
| `dem-ca-bang-hau-to` | P2 | §8 (đếm lại bằng AST), §6.2 đặt tên ca |

---

## 1. Vấn đề

`.claude/dev/launcher.py:650–651` (trên `89fc4fa`), hàm `_con_song` (định nghĩa ở dòng 629), nhánh
không phải Windows: dòng 650 gán đường `/proc/<pid>/stat` cho một biến `Path`, và dòng 651 là (trích một
dòng, protocol §8 — đặc tả không chứa mã launcher ngoài ví dụ này):

```python
    if trang_thai.exists():
```

`Path.exists()` nằm **ngoài** khối `try`. `pathlib` chỉ nuốt errno `(2, 20, 9, 40)`
(`pathlib._IGNORED_ERRNOS`, đo trên Python 3.11.15). Tiến trình đang bị thu hồi làm `stat()` trả
**ESRCH** (errno 3) ⇒ `ProcessLookupError` thoát lên `_con_song_dung_khoa` → `_giet_rieng` → nơi gọi.

Bằng chứng CI (job `109303373142`, PR #679, head `aecdccd`): `t125` chạy toàn suite A/B **song
song**; vế B đỏ đúng một ca, `t154`:

```
ProcessLookupError: [Errno 3] No such process: '/proc/36606/stat'
```

**Phản chứng chạy được, bảng 1 — PID đang sống** (đo lại 11:11:47Z 29-09, Python 3.12.3, trên bản
sao tạm của launcher `89fc4fa`; seam: vá `pathlib.Path.stat` ném lỗi cho đúng đường
`/proc/<pid>/stat` của PID đang xét, `read_text` và `os.kill` không bị vá; PID sống = chính tiến
trình đang chạy):

| bản | ESRCH | EACCES | EIO | không seam: PID sống / PID không tồn tại |
|---|---|---|---|---|
| nền `89fc4fa` | **ném** `ProcessLookupError` | **ném** `PermissionError` | **ném** `OSError` | `True` / `False` |
| bản vá RỘNG (`except OSError: return False`) | `False` | **`False` — SAI** | **`False` — SAI** | `True` / `False` |
| bản vá HẸP **của r1** (OSError khác ⇒ rơi thẳng về `os.kill(pid, 0)`) | `False` | `True` | `True` | `True` / `False` |
| bản r2 (Q-A dưới đây) | `False` | `True` | `True` | `True` / `False` |

**Phản chứng chạy được, bảng 2 — zombie CHƯA `wait`** (cùng lúc, cùng Python; con thật do ca sinh
bằng `start_new_session`, nhận SIGTERM thật, đọc `/proc/<pid>/stat` thấy trạng thái `Z`, KHÔNG được
`wait` trong lúc đo; dọn bằng PID tường minh ở `finally`; seam chỉ vá `Path.stat` của PID ấy).
Cột cuối gọi `_giet_cay(pid, khoa)` trên một con còn SỐNG có seam EACCES ở `stat`, để SIGTERM thật
biến nó thành zombie; mã deadline suy từ `KetGiet.tron_ven` theo `launcher.py:1669`
(`tron_ven` ⇒ `MA_QUA_HAN` 124; ngược lại `MA_GIET_HUT` 125):

| bản | zombie, không seam | zombie, EACCES ở `stat` | zombie, EIO ở `stat` | zombie, EACCES ở CẢ `stat` lẫn `read_text` | `_giet_cay` con sống + SIGTERM + EACCES ở `stat` |
|---|---|---|---|---|---|
| nền `89fc4fa` | `False` | **ném** `PermissionError` | **ném** `OSError` | **ném** `PermissionError` | **ném** `PermissionError` |
| bản vá RỘNG | `False` | `False` | `False` | `False` | `tron_ven=True` ⇒ 124, 0,1 giây — đúng ở ca này, nhưng bảng 1 cho thấy nó sai ở PID sống |
| bản vá HẸP **của r1** | `False` | **`True` — SAI** | **`True` — SAI** | `True` | `tron_ven=False`, `me_da_chet=False` ⇒ **125**, 2,4 giây, 23 lần hỏi `stat` |
| bản r2 | `False` | `False` | `False` | `True` (bảo thủ, xem Q-A) | `tron_ven=True` ⇒ **124**, 0,1 giây, 2 lần hỏi `stat` |

Ba bản Python có trong container cho cùng kết quả ở các ô khoá của bảng 2 (hàng HẸP r1 và hàng r2,
cột EACCES ở `stat` và cột `_giet_cay`): 3.11.15 (11:11:58Z), 3.12.3 (11:11:47Z), 3.13.12 (11:12:01Z).
CI Linux của `ci.yml` dùng `python-version: "3.12"`; job `launcher` của `launcher-windows.yml` dùng
3.13 trên Windows và 3.11 trên Ubuntu.

**Bản "r2" trong các bảng 1, 2 và 3 là bản NHÁP của phiên soạn**, dựng ở bản sao tạm chỉ để kiểm hợp
đồng Q-A có thoả được và đo ra số trên. Nhãn "r2" ở đó chỉ bản nháp dựng theo Q-A.1–4 của r2 (r3 không
đổi Q-A.1–4; r4 và r5 cũng không), KHÔNG phải revision đặc tả r2. Bản nháp không nằm trong đặc tả này, không phải bản vá
đã được chứng nhận; executor tự viết bản của mình theo lời văn Q-A và tự đo lại.

Cross-review lượt 2 tái đo hai bảng trên bằng bản dựng độc lập của họ (VERDICT lượt 2, hướng 2,
11:23:21Z, ba bản Python): các ô khoá khớp (hàng HẸP r1 và hàng r2, `_giet_cay` 125 với 23 lần hỏi
`stat` so với 124 với 2 lần; thời gian 2,32 giây và 0,10 giây ở rig của họ — không phải hằng số). Bảng 1
và 2 ở trên giữ nguyên số r2 đã đo; phiên soạn r3 KHÔNG chạy lại chúng. Phiên soạn r3 chỉ chạy lại
probe `matrix_extra` của lượt 2 (bảng 3) và tự đo thêm bảng 4.

**Bảng 3 — đầu vào mới của r3** (chạy lại lúc 11:46:05Z 29-09, Python 3.12.3, probe `matrix_extra` trong
bản sao rig của cross-review lượt 2; các hàng "biến thể" là đột biến do reviewer dựng ở tệp `x_*.py` của
rig, phiên soạn không viết). Seam: `Path.stat` của PID sống (chính tiến trình probe) ném EACCES; với cột
đầu, `Path.stat` ném một đối tượng `RuntimeError` dựng sẵn; với ba cột nội dung, `Path.read_text` của đúng
đường `/proc/<pid>/stat` trả chuỗi cho sẵn, `<pid>` là PID của probe:

| bản | `RuntimeError` ở `stat` | nội dung rỗng | `<pid> (x)` | `<pid> (x) ` (khoảng trắng cuối) | số lần `read_text` trong lời gọi |
|---|---|---|---|---|---|
| bản nháp Q-A | thoát CHÍNH đối tượng ấy | `True` | `True` | `True` | 1 |
| biến thể "bắt `Exception` ở phép hỏi" | **bị nuốt** (`_con_song` trả `True`) | `True` | `True` | `True` | 1 |
| biến thể "nội dung hỏng ⇒ `False`" | thoát đúng đối tượng | **`False`** | **`False`** | **`False`** | 1 |
| biến thể "tầng đọc chỉ bắt `OSError`" | thoát đúng đối tượng | `ValueError` thoát | `IndexError` thoát | `IndexError` thoát | 1 |
| biến thể "đọc lần hai" | thoát đúng đối tượng | `True` | `True` | `True` | **2** |

Ba biến thể có chữ đậm (nuốt sentinel, `False` cho nội dung hỏng, đọc hai lần) là ba đường mà B1–B5 của r2
để lọt: cả ba PASS hai ca mẫu `t156_...` và `t157_...` do reviewer dựng theo B1–B3b của r2 (VERDICT lượt
2, hướng 3, 11:30:37Z; phiên soạn r3 chạy lại `mutations` lúc 11:46:12Z ra cùng kết quả: bảy đột biến của
r2 chết đúng nhãn, ba biến thể mới PASS cả hai ca, đối chứng `NameError` chết bằng `NameError`). Hàng
"tầng đọc chỉ bắt `OSError`" là **phản chứng phụ**: nó ĐỎ bằng lỗi vô can (`ValueError`/`IndexError`), nên
không được tính là đột biến bị giết đúng lý do.

**Bảng 4 — "nội dung không phân tích được" là những ngoại lệ nào** (phiên soạn r3 tự đo, Python 3.12.3;
biểu thức tách trạng thái của `launcher.py:654`; chuỗi thử dựng tay, `comm` thử thật):

| đầu vào | kết quả (đo 11:46:33Z) |
|---|---|
| rỗng | `ValueError` |
| thiếu dấu đóng ngoặc, ví dụ `32000 x S 1` | `ValueError` |
| hết chuỗi ngay sau dấu đóng ngoặc, `32000 (x)` và `32000 (x) ` | `IndexError` cả hai |
| đầy đủ, `32000 (x) S 1` | `'S'`, không ném |
| `comm` = byte `ff fe` + `ab` (con tự đặt bằng `prctl(PR_SET_NAME)`), `read_text` thật trên `/proc/self/stat` | `UnicodeDecodeError`: là `ValueError`, **không** là `OSError` (`preferred_encoding` `utf-8`; cùng kết quả với `LC_ALL=C.UTF-8`) |
| cùng loại `comm` ấy, PID ĐANG SỐNG, nền `89fc4fa`, không seam (đo 11:46:40Z) | `_con_song(pid)` = **`False`**, `os.kill(pid, 0)` thành công |

Dòng cuối là quan sát về nhánh CŨ, xem §2; nó không thuộc phạm vi sửa.

**Bảng 5 — ba ô tầng đọc mà r3 bỏ đo (r4 thêm; số của cross-review lượt 3, phiên soạn r4 chỉ ĐỌC log)**
(reviewer chạy probe `holes` lúc 12:42:57Z 29-09, Python 3.12.3, trong rig của họ; các hàng "biến thể" là
đột biến do reviewer dựng, phiên soạn không viết và KHÔNG chạy lại). Seam: `Path.stat` của PID sống (chính
tiến trình probe) ném EACCES, và `Path.read_text` của đúng đường `/proc/<pid>/stat` ném một đối tượng dựng
sẵn — cột 2: `ProcessLookupError` (ESRCH); cột 3: `OSError` (EIO); cột 4: một sentinel `KeyboardInterrupt`.
Ở mọi ô bộ đếm ghi 1 lần chạm `stat` và 1 lần chạm `read_text`. Cột cuối là kết quả của hai ca dựng theo
B1–B3b của r3 (tức hai ca mẫu r3 mô tả):

| bản | ESRCH ở `read_text` | EIO ở `read_text` | `KeyboardInterrupt` ở `read_text` | hai ca mẫu r3 |
|---|---|---|---|---|
| bản dựng theo Q-A r3 | `True` | `True` | thoát CHÍNH đối tượng ấy | PASS, PASS |
| biến thể "tầng đọc chỉ bắt `PermissionError`" | **thoát** `ProcessLookupError` | **thoát** `OSError` | thoát đúng đối tượng | PASS, PASS |
| biến thể "ESRCH ở tầng đọc ⇒ `False`" | **`False`** | `True` | thoát đúng đối tượng | PASS, PASS |
| biến thể "nuốt riêng `KeyboardInterrupt` ở tầng đọc" | `True` | `True` | **bị nuốt** (`_con_song` trả `True`) | PASS, PASS |

Ba biến thể là ba đường mà B1–B5 của r3 để lọt: cả ba PASS hai ca mẫu, vì r3 chỉ đặt đầu vào EACCES ở tầng
đọc và ghi ba ô còn lại là "KHÔNG ĐO ĐƯỢC" (lý do r3 nêu: EACCES đại diện cho họ `OSError`). Hàng thứ hai
phá đồng thời hai ô (ESRCH và EIO ở tầng đọc) nên cho **bốn sai lệch quan sát** trên ba biến thể: ESRCH ở
tầng đọc thoát; EIO ở tầng đọc thoát; ESRCH ở tầng đọc bị đọc thành "đã chết"; `KeyboardInterrupt` ở tầng
đọc bị nuốt. Cả bốn đo được ngay bằng seam cục bộ, không cần kernel hay đua thật; EACCES không đại diện
được cho họ `OSError`, vì một bản chỉ bắt `PermissionError` ở tầng đọc qua cả hai ca mẫu. Khi thêm đầu vào
tầng đọc vào cùng helper, reviewer thấy mỗi biến thể chết bằng `TinHieuChotCa` đúng ô của nó và bản dựng
đúng không chết (xem B5).

**Bảng 6 — chiều kết quả của bước PID dự phòng (r5 thêm; số của cross-review lượt 4 và số phiên soạn r5 tự đo)**

Phần A — số của reviewer lượt 4 (`04-fallback.log`, 13:34:58Z 29-09, Python 3.12.3; phiên soạn r5 chỉ ĐỌC log).
Seam: `Path.stat` của PID xét ném EACCES; `Path.read_text` của đúng đường `/proc/<pid>/stat` ném lỗi cho
sẵn; `os.kill` không bị vá. Bản "đúng" là bản dựng theo Q-A r4; bản "sai" là bản trả `True` ngay sau lỗi đọc,
không hỏi PID nào:

| đầu vào | bản đúng | bản sai |
|---|---|---|
| PID con đã `wait`, `stat` EACCES + `read_text` EACCES | `False` | **`True`** |
| PID con đã `wait`, `stat` EACCES + `read_text` EIO | `False` | **`True`** |
| PID con đã `wait`, `stat` EACCES + `read_text` ESRCH | `False` | **`True`** |
| PID sống, `read_text` ESRCH; `kill(pid, 0)` lần lượt thành công / ESRCH / EPERM / EIO | `True` / `False` / `True` / `False`, 1 lời gọi mỗi đầu vào | `True` ở cả bốn, **0 lời gọi** |
| hai ca mẫu của r4 (không có nhãn `B2-pid-du-phong`), và phép D | PASS, PASS; D PASS, PASS | **PASS, PASS; D PASS, PASS** |

Dòng cuối là lỗ: bản sai qua toàn bộ nghiệm thu của r4 mà báo "sống" cho PID đã chết.

Phần B — phiên soạn r5 chạy lại ma trận của reviewer (15:33:49Z 29-09, Python 3.12.3, rig sao chép, 4 tiểu
nhãn × 8 đầu vào đọc = 32 lời gọi) trên năm bản: bản đúng (ứng viên dựng theo Q-A r4) và bốn biến thể của lớp
(k) — k1 là biến thể của reviewer (tệp trùng từng byte với biến thể "trả `True` ngay" của họ, đo bằng `cmp`),
k2–k4 do phiên soạn r5 dựng, chỉ ở bản sao rig. Cột "nới" là cùng ma trận với mọi assertion của nhãn bị bỏ
(đầu vào vẫn chạy nguyên), ghi số lần chạm `stat` / `read_text` / `kill(pid, 0)` cộng dồn:

| bản | hai ca mẫu r4 | ma trận, assertion hiệu lực | ma trận, nới (stat / read / kill) |
|---|---|---|---|
| bản đúng | PASS, PASS | PASS | PASS; 32 / 32 / 32 |
| k1: trả `True` ngay | PASS, PASS | `TinHieuChotCa:B2-pid-du-phong song kill count 0` | PASS; 32 / 32 / **0** |
| k2: gọi `kill(pid, 0)`, bỏ kết quả | PASS, PASS | `TinHieuChotCa:B2-pid-du-phong da-wait result True` | PASS; 32 / 32 / 32 |
| k3: tự xử lý `kill`, mọi `OSError` ⇒ `False` | PASS, PASS | `TinHieuChotCa:B2-pid-du-phong eperm result False` | PASS; 32 / 32 / 32 |
| k4: tự xử lý `kill`, `OSError` khác ⇒ `True` | PASS, PASS | `TinHieuChotCa:B2-pid-du-phong eio result True` | PASS; 32 / 32 / 32 |

Bốn biến thể cùng qua hai ca mẫu của r4 và mỗi biến thể chết ở một tiểu nhãn KHÁC nhau: mỗi trong bốn kết quả
(`song`, `da-wait`, `eperm`, `eio`) có đúng một mutant độc chiếm. Ở cột "nới" mọi biến thể chạy đủ 32 đầu vào
(seam đã chạm, không phải tắt đầu vào), nên cái chết ở cột trước là do assertion chứ không do thiếu thiết lập.
Đây là lý do B5 dòng (k) có bốn dòng (k1–k4) chứ không một: mutant của HINT lượt 4 chỉ chạm `song`.

**Đính chính lời khai của chính phiên soạn — hai lần, cùng hình dạng.** Lần một (r1 §1): bản vá đăng ở
PR #679 comment `5885963131` và thân #685 là bản **RỘNG**; nó đóng ESRCH nhưng biến một
`PermissionError` trên PID **đang sống** thành "đã chết" — đúng lớp lời khai sai *"trả 124 khi tiến
trình còn sống"* mà CLAUDE.md đã trả giá. Lần hai (r2): bản **HẸP** r1 chữa lỗi ấy rồi mở lỗ ở chiều
kia — `kill(pid, 0)` THÀNH CÔNG với zombie, nên bản HẸP báo "còn sống" cho cây đã chết và deadline
trả 125 thay vì 124. Chính r1 §7 B3 chỉ đo PID **đã `wait`**, tức đo đúng chỗ không có zombie. Cross-review
lượt 1 bắt được điều này bằng phép đo (VERDICT hướng 3), không phải bằng đọc.

## 2. Phạm vi đã đo (grep + đọc luồng trên `89fc4fa`)

- Trong `launcher.py` chỉ **một** lời gọi `.exists()` trên đường `/proc`: `:651`.
- Ba chỗ đọc `/proc` khác đều nằm trong `try` bắt `OSError`: `:359` (`_khoa_danh_tinh`, một
  `read_text`), `:430` và `:484` (mỗi chỗ một `iterdir`; phép đọc `stat` bên trong ở `:436` và
  `:490` cũng có `try`). Không cùng dạng lỗi; **không** sửa.
- Nhánh hiện có ngay dưới `:651`: khi `exists()` trả `True` mà `read_text` ném `OSError`,
  `ValueError` hoặc `IndexError` (`:655`), hàm trả `False`. Đó là hành vi CŨ (cross-review lượt 1,
  hướng 7: nó bỏ PID khi `read_text` bị EACCES). Packet này **không** đổi nhánh ấy và **không** được
  nhận là đã sửa nó. **Quan sát mới của r3** (đo 11:46:40Z 29-09, Python 3.12.3, `launcher.py` của
  `89fc4fa`, không seam): một tiến trình ĐANG SỐNG mà `comm` chứa byte không phải UTF-8 (con tự đặt
  bằng `prctl(PR_SET_NAME)`) làm `read_text` ném `UnicodeDecodeError`, và nhánh cũ trả
  `_con_song(pid)` = **`False`** trong khi `os.kill(pid, 0)` thành công. Tức nhánh cũ có thể khai "đã
  chết" cho tiến trình còn sống — đúng lớp lời khai mà objective cấm cho ĐƯỜNG MỚI. Ngoài phạm vi
  (Q-A.3), chưa tìm Issue liên quan, KHÔNG sửa ở đây; ghi lại để không ai đọc `B2-parse` là bằng chứng
  nhánh cũ đã đúng, và để chủ kho quyết có mở Issue riêng hay không. Đây là một PID thật trên một nền;
  tần suất ngoài thực tế: KHÔNG ĐO ĐƯỢC.
- `_con_song` có năm nơi gọi trong `launcher.py`: `:607` (`_con_song_dung_khoa`), `:857` và `:882`
  (`_giet_windows`, tức nhánh Windows), `:1020` và `:1039` (`_giet_cay`). Đo bằng AST (lần lên cây
  cha tới hàm bao, 10:2xZ 29-09; cross-review lượt 1 đo lại độc lập ra đúng năm nơi, 10:52Z):
  **không** lời gọi nào nằm trong thân một `try` bao ngoài, nên `ProcessLookupError` từ `:651` thoát
  thẳng khỏi các hàm ấy.
- Executor phải **grep lại** trên nền tiếp nối trước khi sửa và khai mọi chỗ mới tìm thấy.

## 3. Quyết định

- **Q-A — ngữ nghĩa bản vá.** Q-A là **suy luận của phiên soạn** (từ docstring của `_con_song`, từ
  bài học 124/125 và bài học zombie trong CLAUDE.md, và từ VERDICT lượt 1 và lượt 2); **KHÔNG phải
  quyết định chủ kho**. r2 sửa Q-A của r1 theo lượt 1; r3 KHÔNG đổi ngữ nghĩa Q-A.1–4 và Q-A.6, chỉ nói
  rõ Q-A.5 theo từng tầng và thêm đoạn làm rõ nội dung hỏng (ngay dưới khối "Hệ quả còn lại") theo lượt
  2; **r4 KHÔNG đổi ngữ nghĩa Q-A.1–6**, chỉ thêm một câu nói rõ điều Q-A.4 đã hàm ý (ESRCH ở tầng đọc,
  ngay dưới) theo lượt 3; **r5 cũng KHÔNG đổi ngữ nghĩa Q-A.1–6**, chỉ nói rõ thêm điều Q-A.4 đã hàm ý (ngữ
  nghĩa "sẵn có" của bước `kill(pid, 0)` gồm cả lỗi thứ ba, và bước ấy phải THỰC SỰ được gọi) theo lượt 4;
  chủ kho có thể bác bằng revision mới. Hợp đồng, bằng lời:
  1. Phép hỏi `stat`/`exists` trên `/proc/<pid>/stat` được thực hiện **đúng một lần** mỗi lời gọi
     `_con_song`, và không thử lại.
  2. `ProcessLookupError` ở phép hỏi ấy ⇒ trả `False` (tiến trình đã biến mất).
  3. Phép hỏi không ném lỗi ⇒ hai nhánh sẵn có giữ **nguyên xi**: tệp có ⇒ đọc trạng thái (kể cả
     hành vi cũ ở §2 khi đọc lỗi); tệp vắng ⇒ rơi về `os.kill(pid, 0)` như cũ.
  4. `OSError` khác (EACCES, EIO, …) ⇒ **không** kết luận. Không stat được chưa có nghĩa là không đọc
     được. Trước hết **thử đọc nội dung** `/proc/<pid>/stat`: đọc được và trạng thái là `Z` ⇒ `False`;
     đọc được và không phải `Z` ⇒ `True`. Không đọc được (mọi `OSError`, hoặc nội dung không phân tích
     được) ⇒ rơi về `os.kill(pid, 0)` với ngữ nghĩa sẵn có (`PermissionError` ⇒ `True`,
     `ProcessLookupError` ⇒ `False`). Bước đọc này cũng chỉ làm **một lần**. **Làm rõ (r4, không đổi
     ngữ nghĩa):** `ProcessLookupError` (ESRCH) do chính phép ĐỌC ném ra cũng thuộc "mọi `OSError`" ⇒
     rơi về `os.kill(pid, 0)` và trả `True` cho PID sống; nó KHÔNG được đọc thành "tiến trình đã biến mất"
     như ESRCH của phép HỎI ở bước 2. Chỉ `os.kill(pid, 0)` mới quyết định sống hay chết ở đường này. **Làm rõ (r5, không đổi ngữ
     nghĩa):** (i) "ngữ nghĩa sẵn có" là khối `os.kill(pid, 0)` của nền (`launcher.py:657–664` trên `89fc4fa`):
     `ProcessLookupError` ⇒ `False`, `PermissionError` ⇒ `True`, `OSError` khác (ví dụ EIO) ⇒ `False`, không
     lỗi ⇒ đi tiếp như cũ; (ii) hệ quả của "chỉ `os.kill(pid, 0)` mới quyết định" là đường lỗi đọc và đường nội
     dung hỏng phải THỰC SỰ gọi nó (đúng một lần) và trả đúng kết quả của nó — trả `True` ngay, hoặc gọi nó
     rồi bỏ kết quả, đều là vi phạm, kể cả khi PID đang xét là PID sống nên `True` trùng kết quả đúng.
  5. Phạm vi bắt, **theo từng tầng** (r3 viết lại cho rõ theo lớp `ma-tran-loi-thieu-chot`; r2 chỉ nói
     "họ `OSError`" và để hở chỗ nội dung hỏng ở bước 4):
     · **Tầng hỏi** (`stat`/`exists`): chỉ bắt họ `OSError`. Mọi ngoại lệ khác thoát ra nguyên đối
       tượng — cả ngoại lệ thuộc `Exception` nhưng không thuộc `OSError` (ví dụ `RuntimeError`) lẫn
       ngoại lệ thuộc `BaseException` nhưng không thuộc `Exception` (ví dụ `KeyboardInterrupt`).
     · **Tầng đọc** (bước 4): bắt `OSError` của phép đọc, và các lỗi **phân tích cục bộ** của nội dung
       đọc được (`ValueError` — kể cả `UnicodeDecodeError`, là con của nó — và `IndexError`); phần bọc
       chỉ gồm đúng phép đọc và biểu thức tách trạng thái, không bọc thêm gì, và tuyệt đối không bọc
       phép hỏi. Nhận diện "không phân tích được" bằng kiểm tra dữ liệu thay cho bắt ngoại lệ cũng
       được; Q-A không quy định cách. Ngoại lệ ngoài hai nhóm ấy (ví dụ `RuntimeError`,
       `KeyboardInterrupt`) thoát ra nguyên đối tượng.
     · Bản vá KHÔNG được dùng `except Exception` hay `except BaseException` ở cả hai tầng. Ngoại lệ
       `OSError` thoát ra khỏi đường lỗi mới là vi phạm objective.
  6. Nhánh Windows và Darwin, thứ tự các nhánh khác: không đổi.

  **Hệ quả còn lại, khai thẳng:** nếu cả `stat` lẫn phép đọc nội dung đều không dùng được và PID là
  một zombie, hàm báo "còn sống" (vì `kill(pid, 0)` thành công với zombie), và deadline trả 125 thay
  vì 124. Đó là hướng fail-closed — khai "chưa giết được", không khai sai "đã giết" — và là đúng cái
  giá của lời hứa *"không tự khẳng định đã chết khi không có bằng chứng"*. Bảng 2 (cột 4) đo ra
  đúng như vậy. Nó là hành vi được chấp nhận của r2, không phải lỗi cần sửa ở đây.

  **Nội dung `/proc/<pid>/stat` hỏng — hai đường, hai kết quả, CÓ CHỦ Ý (r3 nói thẳng điều r2 chỉ để
  suy ra).** Hành vi mong đợi lấy đúng từ mã sẵn có, `launcher.py:652–656` trên `89fc4fa`: nhánh CŨ
  (phép hỏi thành công, tệp có) bọc phép đọc và biểu thức tách trạng thái trong một khối bắt `OSError`,
  `ValueError`, `IndexError` và trả **`False`**. Q-A.3 giữ nhánh ấy nguyên xi (§2). Nhánh MỚI (phép hỏi
  ném `OSError` khác ESRCH): nội dung đọc được nhưng không phân tích được ⇒ **rơi về `os.kill(pid, 0)`**
  như Q-A.4 đã viết, tức trả `True` cho PID sống, KHÔNG trả `False`. Hai đường lệch nhau về nội dung
  hỏng, và chính độ lệch ấy là chỗ một bản vá dùng chung MỘT khối bắt cho cả hai đường sẽ trượt sang
  `False` trên đường mới (đột biến (i) ở B5). Dạng nội dung "không phân tích được" đã đo (bảng 3):
  rỗng, và thiếu dấu đóng ngoặc ⇒ `ValueError`; hết chuỗi ngay sau dấu đóng ngoặc, có hoặc không có
  khoảng trắng cuối ⇒ `IndexError`; không giải mã được ⇒ `UnicodeDecodeError` (con của `ValueError`,
  KHÔNG thuộc `OSError`). Dạng thứ tư không phải suy diễn: `comm` của tiến trình đặt được bằng
  `prctl(PR_SET_NAME)` với byte không phải UTF-8, và khi đó `read_text` thật trên `/proc/<pid>/stat`
  ném đúng `UnicodeDecodeError` (bảng 4).
- **Mission #686 Q1:** ca khoá trong `.claude/dev/launcher_test.py`; xếp sau #668.
- **Mission #686 Q3:** executor Sonnet 5.5, effort high.
- **Mission #686 Q4:** không chạy CI Windows trên PR (không gắn nhãn `windows`, không gọi tay).
  `launcher-windows.yml` tự chạy ở `push` master với `paths: .claude/dev/**`, nên **lần merge là
  lần đo Windows đầu tiên** của bản vá; đọc kết quả ấy là một `land_obligation`.
- **Hệ quả của Q4 cộng chỉ thị thường trực "không chạy CI trên PR làm bằng chứng"** (nói thẳng,
  không che): trên PR thi hành, **không có lượt CI nào chạy `launcher_test.py`** — job `launcher` bị
  tắt trên PR không nhãn `windows` (Q4), và `gate-registry` không chạy tệp này (§8). Bằng chứng thay
  thế duy nhất trước merge là log cục bộ Linux ở B6.

## 4. `write_set`

- `.claude/dev/launcher.py`
- `.claude/dev/launcher_test.py`

Không đường dẫn nào khác. Đặc tả này (`ops/specs/launcher-con-song-esrch-r5.md`) là hồ sơ của lượt
soạn, không thuộc write set thi hành.

## 5. `ngoai_pham_vi`

- `:359`, `:430`, `:484` và mọi chỗ đọc `/proc` đã có `try`; nhánh cũ `exists()` đúng mà `read_text`
  lỗi (§2).
- Nhánh Windows và Darwin của `_con_song`.
- `t125`/`t154` trong `ops/lease_publish_test.py`: không sửa; chúng chỉ là nơi lỗi lộ ra.
- `.github/workflows/**` và `.claude/dev/ci_dang_ky_test.py`. `DA_NOI` (`ci_dang_ky_test.py:69–78`,
  13 mục, trong đó có `launcher_test.py`) chỉ giúp `kiem()` xác nhận rằng có một dòng `run:` trong
  workflow nhắc tới tệp test; nó **không** đưa tệp vào nhóm `MOI` mà `gate-registry` thực thi
  (`ci_dang_ky_test.py:37–53`, 9 mục, không có `launcher_test.py`). Q4 giữ nguyên: PR không nhãn
  `windows` chưa đo `launcher_test.py` qua CI; B6 cục bộ là bằng chứng bắt buộc trước merge. Muốn
  thêm job Linux chạy suite này trên PR thì phải mở revision, authority và write set riêng — packet
  này không tự sửa CI. (Đo 11:14Z 29-09: `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 2`,
  gồm #668 và `ci-duong-nhanh-ho-so-r2-g3-claude`; thêm một lý do để không đụng tệp này.)
- Chạy lại job CI của PR #679: không làm (chỉ thị thường trực).

## 6. `muc_tieu`

1. `.claude/dev/launcher.py` — Chặn lỗi của phép hỏi `trang_thai.exists()` theo Q-A: `ProcessLookupError`
   ⇒ `False`; `OSError` khác ⇒ thử đọc nội dung trước (đúng một lần), rồi mới rơi về `os.kill(pid, 0)` —
   kể cả khi đọc lỗi hoặc nội dung không phân tích được (Q-A.4, và đoạn làm rõ ở §3: đường mới KHÁC đường
   cũ ở điểm này). Bảo toàn phép phân biệt zombie trong đường lỗi mới. Kèm chú thích theo idiom của tệp
   (nguồn lỗi ESRCH: PR #679, job `109303373142`; nguồn lỗ zombie: cross-review lượt 1 trên PR #688;
   nguồn ba đường nuốt sentinel / nội dung hỏng / đọc hai lần: cross-review lượt 2 trên PR #688; nguồn ba
  đường ESRCH ở tầng đọc / EIO ở tầng đọc / nuốt riêng `KeyboardInterrupt` ở tầng đọc: cross-review lượt 3
  trên PR #688; nguồn việc bước `kill(pid, 0)` phải thực sự được gọi và trả đúng kết quả trên đường lỗi
  đọc/nội dung hỏng: cross-review lượt 4 trên PR #688).
2. `.claude/dev/launcher_test.py` — **Hai ca mới**, tên nối tiếp hậu tố lớn nhất: `t156_...` (B1, B2,
   B3, B4) và `t157_...` (B3b), theo §7. Hậu tố `t155` là lớn nhất của các ca mang tiền tố `t` trên
   `89fc4fa` (đếm ở §8); executor **đo lại hậu tố trên nền tiếp nối** trước khi đặt tên vì #668 cũng
   giữ tệp này. Các mục `DOT_BIEN` mới: **đúng theo danh sách ở B5, và chỉ ở đó** — §6 không lặp lại
   con số. Số ca mới và số mục đột biến là hai đơn vị khác nhau. Hai ca dựng trên MỘT helper theo nhãn
   (quy ước chung ở §7); helper ấy và các đơn vị nhãn nằm trong hai ca mới của `launcher_test.py`, không
   thêm tệp, không thêm ca đăng ký, không sửa runner `--dot-bien`.

## 7. `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3). Đột biến chạy trên **bản sao tạm**, bằng chính
`python .claude/dev/launcher_test.py --dot-bien`. Quy ước chung cho hai ca mới:

- Mỗi `bang(...)` mang **nhãn** ở đầu thông điệp (`B1`, `B2-eacces`, …) để một đột biến chết đúng chốt
  của nó phân biệt được với chết ở chốt khác của cùng ca. Sáu nhãn gồm nhiều đầu vào có tên — `B2-doc-hong`,
  `B2-tin-hieu`, `B2-exception`, `B2-parse`, `B2-dem-doc`, `B2-pid-du-phong` — còn mang **tiểu nhãn** ngay sau nhãn, cách một
  dấu cách (bảng tiểu nhãn ở ngay sau ma trận B2). Nhãn là đơn vị của thứ tự thực thi và của tham số
  CHẠY/NỚI của helper; tiểu nhãn là đơn vị của phép quan sát D và của điều kiện khớp ở B5 (r4).
- Seam stat/read chỉ chạm đúng `/proc/<pid>/stat` của PID đang xét, có **bộ đếm lần chạm**; ca xác nhận seam đã
  chạm ở từng lời gọi (seam không chạm ⇒ ca không đo gì). Lấy khoá danh tính **trước** khi đặt seam. Ngoại lệ có phạm vi: `B2-pid-du-phong`
  thêm observer/seam cho đúng `os.kill(pid, 0)` như mô tả riêng của nhãn ấy.
- Ca chỉ chuyển **đúng đối tượng ngoại lệ do seam tạo ra** thành `bang(False, ...)`. Cấm
  `except Exception`/`except BaseException` rồi đổi mọi thứ thành `TinHieuChotCa`: ngoại lệ vô can
  phải giữ hạng vô can (runner in kiểu ngoại lệ trong ngoặc sau tên ca — đó là tín dụng giả).
- Sinh tiến trình con: `start_new_session`, tín hiệu thật, dọn bằng **PID tường minh** trong `finally`
  (`kill` rồi `wait`); không `pkill`, không đoán nhóm. Nếu không dựng được điều kiện (ví dụ con không
  chuyển sang `Z` trong thời hạn có trần), ca ném lỗi thường, KHÔNG dùng `bang`.
- **Cấu trúc theo nhãn, MỘT helper dùng chung (r3, lớp `chot-nguoc-khong-co-lap`; r4 thêm điều kiện về mặc
  định, xem phép D ở B5).** Mỗi nhãn là một
  đơn vị độc lập gồm: đầu vào (seam + lời gọi) và nhóm assertion mang nhãn ấy (kết quả, không-lộ-ngoại-
  lệ, seam đã chạm, bộ đếm). Hai ca đăng ký gọi CÙNG một helper dựng từ các đơn vị đó; helper nhận hai
  tham số tuỳ chọn mà ca đăng ký KHÔNG truyền — tập nhãn CHẠY (mặc định: tất cả, theo thứ tự dưới đây)
  và tập nhãn NỚI (mặc định: rỗng); tên tham số do executor đặt. **"Nới nhãn L"** nghĩa là: đầu vào của
  L vẫn chạy nguyên (seam vẫn đặt, lời gọi vẫn thực hiện), nhưng MỌI assertion mang nhãn L bị bỏ, và
  nếu chính đối tượng ngoại lệ do seam của L tạo ra thoát khỏi lời gọi thì nó bị nuốt (so bằng danh
  tính); mọi ngoại lệ khác vẫn thoát. Nới KHÔNG được là cách để bỏ đầu vào, bỏ thiết lập hay trả sớm.
  Hai ca đăng ký vẫn chỉ là hai ca (§6.2): phép đo dùng tham số là lời gọi TRỰC TIẾP helper từ tập
  lệnh bằng chứng của executor, trên bản sao đột biến (cùng cách B5 đã đòi gọi thẳng hàm ca) — không
  phải ca đăng ký thứ ba và không sửa runner `--dot-bien`. **Mặc định của hai tham số là một phần của
  hợp đồng và được khoá RIÊNG bằng phép D** (mặc định: mọi nhãn chạy, tập nới rỗng); không được suy
  ra từ việc một đột biến sản phẩm chết ở ca đăng ký, vì đột biến ấy có thể chết ở một nhãn khác.
- **Thứ tự thực thi cố định** trong `t156_...`, đúng thứ tự liệt kê ở đây: `B1`, `B2-eacces`, `B2-eio`,
  `B2-doc-hong`, `B2-tin-hieu`, `B2-dem-lan`, `B2-exception`, `B2-parse`, `B2-dem-doc`, `B2-pid-du-phong`, `B3-song`,
  `B3-da-wait`, `B3-zombie`. `bang` ném ở assertion sai ĐẦU TIÊN, nên nhãn báo là nhãn đầu tiên trong
  thứ tự này; B5 dựa vào điều đó. Trong một nhãn có tiểu nhãn, các đầu vào cũng chạy theo thứ tự cố định
  của bảng tiểu nhãn, và assertion sai đầu tiên quyết định tiểu nhãn báo. `t157_...` chỉ có
  `B3b-giet-cay`. B4 không phải nhãn (nó là điều kiện nền).

**Ca `t156_...`**

- **B1 (mục 2) — ESRCH.** Seam ném `ProcessLookupError(errno.ESRCH, …)`. Gọi `_con_song(os.getpid())`,
  `_con_song_dung_khoa(os.getpid(), <khoá thật>)` và `_giet_rieng({<pid con đã wait>: "k"}, 0)`: không
  ngoại lệ nào thoát; hai hàm đầu trả `False`. Nhãn `B1`.
  **ĐỎ khi:** chạy trên nền `89fc4fa` ⇒ `ProcessLookupError` thoát ⇒ ca đổi đúng đối tượng ấy thành
  `bang(False, …)` của chính nó. `B1` chỉ đo ESRCH ở tầng HỎI (kết quả đúng `False`); ESRCH ở tầng ĐỌC là
  nhãn khác, `B2-doc-hong` tiểu nhãn `ESRCH` (kết quả đúng `True`), và không nhãn nào thay được nhãn kia.
- **B2 (mục 2) — miền lỗi khác ESRCH, chống bản rộng và bản hẹp giả.** Trên `os.getpid()` (PID sống):
  - `B2-eacces`: seam `PermissionError(errno.EACCES, …)` ⇒ `_con_song` trả **`True`**. **ĐỎ khi** bản
    RỘNG (`except OSError: return False`) ⇒ `False`.
  - `B2-eio`: seam `OSError(errno.EIO, …)` ⇒ `True`, không ngoại lệ nào thoát. **ĐỎ khi** bản chỉ bắt
    `PermissionError`: EIO thoát ra, trái objective "mọi `OSError`".
  - `B2-doc-hong` (r4 mở rộng; r3 chỉ có đầu vào EACCES) — ba đầu vào, tiểu nhãn `EACCES`, `EIO`,
    `ESRCH`, chạy đúng thứ tự ấy. Mỗi đầu vào: seam EACCES ở `Path.stat` của PID sống và seam ở
    `Path.read_text` của đúng đường `/proc/<pid>/stat` của PID ấy ném MỘT đối tượng dựng sẵn — lần lượt
    `PermissionError(errno.EACCES, …)`, `OSError(errno.EIO, …)`, `ProcessLookupError(errno.ESRCH, …)`.
    Mỗi đầu vào phải trả **`True`** (không đọc được thì rơi về `kill(pid, 0)`, không tự khẳng định đã
    chết) và không ngoại lệ nào thoát. **ESRCH ở tầng đọc KHÔNG phải ESRCH ở tầng hỏi:** ở tầng hỏi kết quả
    đúng là `False` (`B1`), ở tầng đọc kết quả đúng là `True` — hai ô có kỳ vọng NGƯỢC nhau, nên một bản vá
    dùng chung một nhánh xử lý ESRCH cho cả hai tầng chết ở đúng một trong hai nhãn, và hai nhãn này
    KHÔNG thay được cho nhau. Ca đổi chỉ đúng đối tượng do seam tạo ra thành `TinHieuChotCa` khi nó thoát
    (quy ước chung); ngoại lệ khác giữ hạng vô can. **ĐỎ khi:** tầng đọc chỉ bắt `PermissionError` (EIO
    và ESRCH thoát — tiểu nhãn báo là `EIO`, đầu vào đầu tiên làm nó thoát); đường đọc hỏng trả `False`
    cho mọi lỗi (tiểu nhãn `EACCES`); đường đọc hỏng chỉ trả `False` riêng cho `ProcessLookupError` còn lỗi
    khác vẫn hỏi PID dự phòng (tiểu nhãn `ESRCH`).
  - `B2-tin-hieu` (r4 mở rộng; r3 chỉ có tầng hỏi) — hai đầu vào, tiểu nhãn `hoi` rồi `doc`. `hoi`:
    `Path.stat` của PID sống ném MỘT sentinel `KeyboardInterrupt` dựng sẵn. `doc`: `Path.stat` ném EACCES
    và `Path.read_text` của đúng PID ấy ném một sentinel `KeyboardInterrupt` KHÁC. Mỗi đầu vào: ca bắt ngay
    quanh lời gọi và so **đúng đối tượng** (`is`); trả về bình thường thay vì truyền sentinel ra ⇒ `bang(False,
    …)`. Ngoại lệ khác giữ hạng vô can. **ĐỎ khi:** nuốt `BaseException` quanh phép hỏi (tiểu nhãn `hoi`);
    nuốt riêng `KeyboardInterrupt` ở tầng đọc dù `RuntimeError` vẫn được truyền ra (tiểu nhãn `doc`). Sentinel
    ở tầng hỏi KHÔNG thay phép đo tầng đọc, và sentinel `RuntimeError` của `B2-exception` không thay
    sentinel `KeyboardInterrupt` của nhãn này: bản vá nuốt riêng `KeyboardInterrupt` giữ `RuntimeError`
    thoát nguyên nên `B2-exception` xanh với nó.
  - `B2-dem-lan`: seam theo thứ tự — lần hỏi thứ nhất đi `stat` thật, lần thứ hai ném ESRCH; một lời gọi
    `_con_song` phải chạm seam **đúng một lần** và trả đúng theo trạng thái thật. **ĐỎ khi** bản vá gọi
    `exists()` lần hai: `ProcessLookupError` từ lần hai thoát ra, hoặc bộ đếm lần chạm ≠ 1.
  - `B2-exception` (r3) — miền `Exception` KHÔNG thuộc `OSError` (sentinel `RuntimeError`), **hai tầng,
    hai đầu vào, cùng một nhãn**; thông điệp `bang` ghi tiểu nhãn `hoi` hoặc `doc` ngay sau nhãn.
    · `hoi`: seam `Path.stat` của PID sống ném MỘT đối tượng `RuntimeError` dựng sẵn. `_con_song` phải
      để CHÍNH đối tượng ấy thoát ra. Ca bắt ngay quanh lời gọi và so bằng danh tính (`is`); trả về
      bình thường (kể cả `True`) thay vì ném ⇒ `bang(False, …)`. Đối tượng khác thoát ra ⇒ không bắt
      (vô can).
    · `doc`: seam `Path.stat` ném EACCES (để vào bước 4 của Q-A) và seam `Path.read_text` của đúng
      PID ấy ném MỘT đối tượng `RuntimeError` dựng sẵn khác; chính đối tượng đó phải thoát ra. Cùng
      cách bắt và so như `hoi`.
    **ĐỎ khi:** phép hỏi (đầu vào `hoi`) hoặc khối đọc (đầu vào `doc`) bắt `Exception`. Lý do có nhãn
    này: `KeyboardInterrupt` ở `B2-tin-hieu` thuộc `BaseException` nên bản `except Exception` cho nó
    thoát nguyên, và một mình nó không phân biệt được `except OSError` với `except Exception` (bảng 3:
    `RuntimeError` bị nuốt trong khi B1–B3b của r2 vẫn PASS).
  - `B2-parse` (r3) — nội dung đọc được nhưng KHÔNG phân tích được, trên đường MỚI (Q-A.4 và đoạn làm
    rõ ở §3; đường cũ trả `False` và không thuộc nhãn này). Bốn đầu vào (tiểu nhãn `p1`–`p4`, chạy theo
    thứ tự ấy), PID sống (`os.getpid()`), seam `Path.stat` ném EACCES, và seam `Path.read_text` của đúng
    đường `/proc/<pid>/stat`: (p1) trả chuỗi rỗng; (p2) trả chuỗi thiếu dấu đóng ngoặc, ví dụ
    `<pid> x S 1`; (p3) trả chuỗi hết ngay sau dấu đóng ngoặc, ví dụ `<pid> (x)`, và cả biến thể có khoảng
    trắng cuối (cùng tiểu nhãn `p3`, hai payload); (p4) ném một
    `UnicodeDecodeError` do ca dựng sẵn (dạng "không giải mã được", có thật: bảng 4). Mỗi đầu vào:
    `_con_song(os.getpid())` phải trả **`True`** (rơi về `kill(pid, 0)`), không ngoại lệ nào thoát.
    **Trong nhãn này KHÔNG ngoại lệ nào được đổi thành `TinHieuChotCa`**: ngoại lệ nào thoát ra khỏi
    `_con_song` (kể cả `ValueError`/`IndexError` của phép tách, kể cả `UnicodeDecodeError` do seam) là
    lỗi vô can, giữ hạng vô can — ca đỏ vì lỗi ấy đúng là ca đỏ (ứng viên không xử lý nội dung hỏng),
    nhưng đó KHÔNG phải một đột biến bị giết đúng lý do (bảng 3, hàng "tầng đọc chỉ bắt `OSError`").
    **ĐỎ khi** (đột biến (i)): đường nội dung hỏng trả `False` ⇒ chết bằng assertion kết quả `True`.
  - `B2-dem-doc` (r3) — số lần ĐỌC nội dung. Gọi `_con_song(os.getpid())` TRỰC TIẾP (không qua
    `_con_song_dung_khoa`), ba đầu vào (tiểu nhãn `1`, `2`, `3`, chạy theo thứ tự ấy): (1) `stat` EACCES +
    `read_text` thật thành công; (2) `stat` EIO + `read_text` thật thành công; (3) `stat` EACCES +
    `read_text` ném EACCES (đọc lỗi). Trong mỗi
    đầu vào, số lần `Path.read_text` chạm đúng đường `/proc/<pid>/stat` của PID ấy **bên trong cửa sổ
    lời gọi `_con_song`** phải bằng **đúng 1** (gồm cả nhánh đọc thành công lẫn nhánh đọc lỗi). Cửa sổ
    đếm chỉ bao lời gọi: mọi lần đọc kiểm soát do chính ca thực hiện (ví dụ đọc để xác nhận trạng
    thái) nằm NGOÀI cửa sổ — lượt 2 đã đo trường hợp nhầm: cộng lần đọc kiểm soát vào thì bản đúng
    báo 2 (VERDICT lượt 2, hướng 7). Phép đọc khoá của wrapper (`_khoa_danh_tinh`, `:359`) không thuộc
    bộ đếm này vì ca gọi trực tiếp. Bộ đếm là lớp quan sát: nó chuyển tiếp sang `read_text` thật và
    KHÔNG thay nội dung, trừ ở các đầu vào "đọc hỏng" đã khai (đầu vào (3) này, và bốn đầu vào của
    `B2-parse`). Giữ nguyên các kiểm đếm `stat` hiện có (`B2-dem-lan`). **ĐỎ khi** (đột biến (j)): bộ
    đếm ≠ 1, tức đọc lại lần hai, ở nhánh nào cũng vậy — lần đọc thứ hai đặt sau lần đọc thành công làm
    đầu vào `1` đỏ đầu tiên; lần đọc thứ hai đặt trong xử lý đọc lỗi chỉ chạm ở đầu vào `3`.
  - `B2-pid-du-phong` (r5, thêm sau cross-review lượt 4) — khoá KẾT QUẢ và VIỆC THỰC HIỆN của bước PID dự
    phòng ở Q-A.4, thay vì suy từ `True` trên PID sống. Q-A.4 nói khi không đọc được thì chỉ `os.kill(pid, 0)`
    quyết định sống hay chết; mọi nhãn ở trên đặt đầu vào đọc lỗi hoặc hỏng lên PID SỐNG, nên một bản trả `True`
    ngay sau lỗi đọc — không hỏi PID nào — qua được chúng (lượt 4 đo: qua cả hai ca mẫu của r4 lẫn D) mà vẫn
    báo "sống" cho một PID con đã `wait`. Bốn tiểu nhãn theo thứ tự: `song`, `da-wait`, `eperm`, `eio`. Mỗi
    tiểu nhãn chạy CÙNG tám đầu vào đọc, theo thứ tự: EACCES, EIO, ESRCH (ba lỗi đọc của `B2-doc-hong`), p1,
    p2, p3 không khoảng trắng cuối, p3 có khoảng trắng cuối, p4 (đúng các đầu vào của `B2-parse`: bốn tiểu nhãn, năm lần đọc vì p3 có hai payload), luôn với
    seam `stat` EACCES để vào bước 4. Tổng 4 × 8 = 32 lời gọi `_con_song` trực tiếp. (Con số 32 ở đây là số
    đầu vào của nhãn, KHÔNG phải số control của D; hai số bằng nhau tình cờ, hai đơn vị khác nhau.)
    · `song`: PID là chính tiến trình; `kill` thật thành công ⇒ kết quả `True`.
    · `da-wait`: PID con đã `kill` và `wait` (chết hẳn, không phải zombie); `kill` thật ném ESRCH ⇒ `False`.
    · `eperm`: PID là chính tiến trình; seam CHỈ ở `os.kill` với đúng PID ấy và tín hiệu 0 ném
      `PermissionError(errno.EPERM, …)` ⇒ `True`.
    · `eio`: như `eperm` nhưng seam ném `OSError(errno.EIO, …)` ⇒ `False`.
    Kết quả kỳ vọng của `eperm` và `eio` là ngữ nghĩa SẴN CÓ của khối `os.kill(pid, 0)` ở nền
    (`launcher.py:657–664` trên `89fc4fa`: `ProcessLookupError` ⇒ `False`, `PermissionError` ⇒ `True`, `OSError`
    khác ⇒ `False`); Q-A.4 chỉ nêu hai lỗi đầu, nên r5 ghi rõ lỗi thứ ba ở Q-A.4 (không đổi ngữ nghĩa).
    Observer của `os.kill` chỉ chạm đúng cặp (PID, 0): ghi lại từng lời gọi rồi CHUYỂN TIẾP thật (`song`,
    `da-wait`) hoặc ném lỗi seam (`eperm`, `eio`); tín hiệu khác hay PID khác chuyển tiếp nguyên vẹn; không
    bọc seam ấy quanh thiết lập hay dọn con. Trong mỗi lời gọi ca đòi, theo thứ tự: đúng MỘT lời gọi
    `kill(pid, 0)`; kết quả đúng như trên; bộ đếm seam `stat` = 1 và `read` = 1. Nới nhãn vẫn chạy mọi đầu
    vào và observer, chỉ bỏ assertion. Ngoại lệ thoát ra khỏi `_con_song` giữ hạng vô can như `B2-parse`
    (kể cả `UnicodeDecodeError` của p4 do seam); chỉ đúng đối tượng do seam dựng (lỗi đọc hoặc lỗi `kill`)
    mới đổi thành `TinHieuChotCa`, theo quy ước chung. Không đổi ngữ nghĩa Q-A.3/.4.
    **ĐỎ khi** (lớp (k), mỗi tiểu nhãn có một mutant độc chiếm, đã đo ở bảng 6): bản trả `True` ngay, không
    hỏi PID ⇒ `song` (số lời gọi `kill` bằng 0); bản hỏi PID nhưng bỏ kết quả ⇒ `da-wait` (PID đã `wait`
    được báo `True`); bản tự xử lý `kill` và trả `False` cho `PermissionError` ⇒ `eperm`; bản tự xử lý `kill`
    và trả `True` cho `OSError` khác ⇒ `eio`. `B3-da-wait` (không seam) KHÔNG thay được `da-wait` của nhãn
    này: nó không đi qua đường lỗi mới.
  - **Ma trận tầng × miền (r3 lập; r4 lấp ba ô tầng đọc; r5 thêm hàng chiều kết quả PID dự phòng)** — chốt nào đặt ở tầng nào. Mọi ô của bảng có đầu vào;
    **không còn ô "KHÔNG ĐO ĐƯỢC"** (r3 để trống ba ô tầng đọc là ESRCH, EIO và `BaseException`, và
    lượt 3 đã đo được cả ba bằng seam cục bộ, xem bảng 5 ở §1). Ô nào sau này thiếu đầu vào thì phải nói
    thẳng, không mượn ô khác che. Đây là bảng có thẩm quyền để suy ra các dòng biến thể ở B5:

    | miền | tầng hỏi (`stat`/`exists`) | tầng đọc (`read_text`, bước 4) |
    |---|---|---|
    | `OSError` — ESRCH | `B1` (kết quả đúng `False`) | `B2-doc-hong`, tiểu nhãn `ESRCH` (kết quả đúng `True`) |
    | `OSError` khác | `B2-eacces` (`PermissionError`), `B2-eio` (`OSError` EIO) | `B2-doc-hong`, tiểu nhãn `EACCES` và `EIO` |
    | `Exception` không thuộc `OSError` | `B2-exception`, tiểu nhãn `hoi` | `B2-exception`, tiểu nhãn `doc` |
    | `BaseException` không thuộc `Exception` | `B2-tin-hieu`, tiểu nhãn `hoi` | `B2-tin-hieu`, tiểu nhãn `doc` |
    | nội dung đọc được nhưng hỏng (`ValueError`, `IndexError`, `UnicodeDecodeError`) | — | `B2-parse` (bốn đầu vào `p1`–`p4`) |
    | kết quả bước PID dự phòng (sống, đã chết, EPERM, EIO) và số lời gọi `kill(pid, 0)` | — | `B2-pid-du-phong`: `song`, `da-wait`, `eperm`, `eio`; mỗi tiểu nhãn chạy đủ tám đầu vào đọc (ba lỗi đọc và năm lần đọc parse của `B2-parse`: p1, p2, hai payload của p3, p4) |
    | số lần hỏi / số lần đọc | `B2-dem-lan` (đúng 1) | `B2-dem-doc` (đúng 1, ở nhánh đọc thành công và nhánh đọc lỗi; ba đầu vào `1`–`3`) |

    **Bảng tiểu nhãn — danh sách ĐỘC LẬP các đơn vị assertion, thứ tự cố định** (nguồn của phép quan sát D
    ở B5; viết ở đây, không suy từ cấu hình của helper). Nhãn không liệt kê ở đây (`B1`, `B2-eacces`,
    `B2-eio`, `B2-dem-lan`, `B3-song`, `B3-da-wait`, `B3-zombie` trong `t156_...`; `B3b-giet-cay` trong
    `t157_...`) không có tiểu nhãn, mỗi nhãn là một đơn vị:

    | nhãn | tiểu nhãn theo thứ tự | số đơn vị |
    |---|---|---|
    | `B2-doc-hong` | `EACCES`, `EIO`, `ESRCH` | 3 |
    | `B2-tin-hieu` | `hoi`, `doc` | 2 |
    | `B2-exception` | `hoi`, `doc` | 2 |
    | `B2-parse` | `p1`, `p2`, `p3`, `p4` | 4 |
    | `B2-dem-doc` | `1`, `2`, `3` | 3 |
    | `B2-pid-du-phong` | `song`, `da-wait`, `eperm`, `eio` | 4 |

    Tổng: 13 nhãn của `t156_...` + 1 của `t157_...` = 14 nhãn; sáu nhãn có tiểu nhãn gồm 18 đơn vị; các
    nhãn còn lại (bảy trong `t156_...`, một trong `t157_...`) mỗi nhãn một đơn vị ⇒ 18 + 8 = 26 đơn vị.

    Ba ô tầng đọc mà r3 bỏ đo (ESRCH, EIO, `BaseException`) nay có đầu vào, với ba điều đã đo là sai nếu
    làm tắt: (1) EACCES ở tầng đọc **không đại diện** cho họ `OSError` — một bản chỉ bắt `PermissionError`
    ở tầng đọc qua cả hai ca r3 (bảng 5); (2) ESRCH ở tầng hỏi **không thay** ESRCH ở tầng đọc, kỳ vọng
    ngược nhau; (3) sentinel `RuntimeError` **không thay** sentinel `KeyboardInterrupt` ở tầng đọc. Điều
    thứ tư, đo ở lượt 4 và r5 (bảng 6): (4) `True` trên PID sống **không chứng minh** đã hỏi PID — bản trả
    `True` ngay qua mọi nhãn có PID sống; phải có PID đã `wait` (kết quả `False`), có quan sát đúng lời gọi
    `kill(pid, 0)`, và có kết quả EPERM/EIO của chính lời gọi ấy. Đây là
    chốt của hợp đồng Q-A, không phải lời khai rằng kernel thật đã sinh các lỗi ấy. Handoff phải ghi
    từng đầu vào và nhãn giết (kèm tiểu nhãn).
- **B3 (mục 2) — đối chứng dương, và zombie chưa `wait`.** Không seam: `_con_song(os.getpid())` ⇒
  `True` (nhãn `B3-song`); `_con_song` trên PID con đã `wait` ⇒ `False` (nhãn `B3-da-wait`). Rồi một
  con thật, session riêng, SIGTERM thật,
  đọc `/proc/<pid>/stat` bằng phép đọc **độc lập với launcher** cho tới khi thấy `Z`, **chưa `wait`**;
  đặt seam EACCES chỉ ở `Path.stat` của PID ấy (để `read_text` thật vẫn đọc được): `_con_song` và
  `_con_song_dung_khoa` đều phải `False`. Nhãn `B3-zombie`.
  **ĐỎ khi:** đột biến bỏ phép đọc nội dung trên đường lỗi mới, rơi thẳng về `kill(pid, 0)` ⇒ `True`.
  B3 cũ của r1 (chỉ PID đã `wait`) giữ làm đối chứng nhưng KHÔNG đủ: nó xanh với bản HẸP r1.
- **B4 (mục 2) — nền.** Ngoài Linux (`LA_WINDOWS`, Darwin) hai ca **trả chuỗi lý do** (BỎ QUA có khai
  theo quy ước sẵn của tệp), không trả QUA: nhánh `/proc` không tồn tại ở đó.

**Ca `t157_...`**

- **B3b (mục 2) — chốt tiêu thụ `_giet_cay`.** Con thật CÒN SỐNG, session riêng, `khoa` lấy trước seam;
  seam EACCES ở `Path.stat` của PID ấy; gọi `_giet_cay(pid, khoa)` để SIGTERM thật biến con thành
  zombie chưa `wait`; kết quả phải có `tron_ven=True` (phía deadline ánh xạ 124, `launcher.py:1669`).
  Nhãn `B3b-giet-cay`. Dọn PID con và `wait` trong `finally`. Ca này riêng để đột biến (c) ở B5 làm
  **cả hai** ca `t156_...` lẫn `t157_...` đỏ, mỗi ca bằng `TinHieuChotCa` của chính nó.
  **ĐỎ khi:** đột biến bỏ phép đọc nội dung ⇒ `tron_ven=False` ⇒ tương ứng 125 (bảng 2, hàng HẸP r1).

**Các chốt chung**

- **B5 (mục 2) — `DOT_BIEN`: DANH SÁCH CÓ THẨM QUYỀN DUY NHẤT của đột biến mới.** Mọi chỗ khác trong
  đặc tả (kể cả §6) chỉ trỏ về đây. Executor **đếm lại** trên mã thực thi và khai. **Mười một LỚP** đột biến
  (a)–(k), mỗi lớp trỏ đích là ca mới; số mục `DOT_BIEN` thật là số **dòng biến thể** dưới đây, suy ra từ
  quy tắc ngay sau danh sách (kỳ vọng **mười chín**). Mỗi dòng nêu vị trí mã, hành vi bị đổi, và nhãn giết
  kèm tiểu nhãn mong đợi (tiểu nhãn: bảng ngay sau ma trận B2):
  (a) gỡ bản vá (trả `:651` về nguyên dạng nền) ⇒ `t156_...` đỏ ở `B1`;
  (b) thay bản vá bằng bản RỘNG ⇒ `t156_...` đỏ ở `B2-eacces`;
  (c) bỏ phép đọc nội dung trên đường lỗi mới, chỉ hỏi `kill(pid, 0)` ⇒ **cả** `t156_...` (đỏ ở
  `B3-zombie`) **và** `t157_...` (đỏ ở `B3b-giet-cay`);
  (d) hai dòng, hai vị trí — (d1) ở phép hỏi chỉ bắt `PermissionError` (giữ nhánh ESRCH riêng), để EIO thoát ⇒ `t156_...` đỏ ở
  `B2-eio`; (d2) ở tầng đọc chỉ bắt `PermissionError` thay cho `OSError` (vẫn bắt lỗi phân tích) ⇒
  `t156_...` đỏ ở `B2-doc-hong`, tiểu nhãn `EIO` (ESRCH ở tầng đọc cũng thoát nhưng đứng sau EIO trong thứ
  tự nên không phải tiểu nhãn báo);
  (e) hai dòng, hai vị trí — (e1) nuốt `BaseException` quanh phép hỏi ⇒ `t156_...` đỏ ở `B2-tin-hieu`,
  tiểu nhãn `hoi`; (e2) ở tầng đọc nuốt riêng `KeyboardInterrupt`, vẫn truyền `RuntimeError` ra ⇒ `t156_...`
  đỏ ở `B2-tin-hieu`, tiểu nhãn `doc`;
  (f) hỏi `exists()` lần hai ⇒ `t156_...` đỏ ở `B2-dem-lan`;
  (g) hai dòng, CÙNG vị trí (tầng đọc), hai hành vi — (g1) trả `False` cho mọi lỗi đọc ⇒ `t156_...` đỏ ở
  `B2-doc-hong`, tiểu nhãn `EACCES`; (g2) chỉ trả `False` riêng cho `ProcessLookupError`, các lỗi đọc khác
  vẫn hỏi PID dự phòng ⇒ `t156_...` đỏ ở `B2-doc-hong`, tiểu nhãn `ESRCH`;
  (h) hai dòng, hai vị trí — thay bắt `OSError` bằng `Exception`, giữ nhánh ESRCH riêng: (h1) ở phép hỏi ⇒
  `t156_...` đỏ ở `B2-exception`, tiểu nhãn `hoi`; (h2) ở khối đọc ⇒ `t156_...` đỏ ở `B2-exception`, tiểu
  nhãn `doc`; cả hai với sentinel `RuntimeError`;
  (i) khi phân tích nội dung hỏng, trả `False` thay vì hỏi PID dự phòng ⇒ `t156_...` đỏ ở `B2-parse`
  (tiểu nhãn `p1`, đầu vào đầu tiên) bằng assertion kết quả, không phải `ValueError` vô can;
  (j) hai dòng, hai vị trí — đọc nội dung dự phòng lần hai: (j1) đặt sau lần đọc thành công ⇒ `t156_...`
  đỏ ở `B2-dem-doc`, tiểu nhãn `1`; (j2) đặt trong xử lý lần đọc lỗi ⇒ `t156_...` đỏ ở `B2-dem-doc`, tiểu
  nhãn `3`.

  (k) bốn dòng, CÙNG vị trí (chỗ đường đọc lỗi hoặc nội dung hỏng quyết định sống hay chết, Q-A.4), bốn hành
  vi — mỗi dòng bỏ hoặc bóp méo đúng MỘT chiều của bước PID dự phòng, nên mỗi dòng chết ở một tiểu nhãn kết
  quả riêng của `B2-pid-du-phong`: (k1) trả `True` ngay, không hỏi `kill(pid, 0)` ⇒ `t156_...` đỏ ở
  `B2-pid-du-phong`, tiểu nhãn `song` (số lời gọi `kill(pid, 0)` bằng 0); (k2) gọi `kill(pid, 0)` đúng một lần
  nhưng BỎ kết quả, luôn trả `True` ⇒ đỏ ở tiểu nhãn `da-wait` (PID đã `wait`, kết quả `True` thay vì `False`;
  số lời gọi bằng 1 nên `song` xanh); (k3) tự xử lý `kill` trên đường lỗi mới, mọi `OSError` kể cả
  `PermissionError` ⇒ `False` ⇒ đỏ ở tiểu nhãn `eperm` (kết quả `False` thay vì `True`); (k4) tự xử lý `kill`
  trên đường lỗi mới, `ProcessLookupError` ⇒ `False` nhưng `OSError` khác ⇒ `True` ⇒ đỏ ở tiểu nhãn `eio` (kết
  quả `True` thay vì `False`). Cả bốn dòng đều xanh với hai ca mẫu của r4 (không có nhãn này); không dùng
  `B3-da-wait` (không seam) thay cho PID đã `wait` TRÊN đường lỗi mới. Vì sao bốn dòng chứ không một: HINT
  lượt 4 đề nghị một dòng (k) ở tiểu nhãn `song`; nhưng khi `song` đã giết mutant bằng bộ đếm thì kết quả
  `da-wait`, `eperm`, `eio` không còn mutant nào chạm tới, và tiểu nhãn nào không có mutant độc chiếm thì
  chỉ còn được giữ bởi assertion chứ chưa được đo có răng (đúng chỗ r4 đã nêu cho tiểu nhãn `EIO` của
  `B2-doc-hong`). Đã đo (bảng 6): k2, k3, k4 qua hai ca mẫu của r4 và chết đúng một tiểu nhãn mỗi cái;
  giữ nguyên mọi dòng (a)–(j).

  **Quy tắc mục `DOT_BIEN` (r3; r4 cập nhật cho (d), (e), (g); r5 cập nhật cho (k)).** (a)–(k) ở trên là mười
  một LỚP. Mỗi mục `DOT_BIEN` là một bản sao đột biến có tên riêng và làm đúng một thay đổi ở đúng một vị
  trí mã (một mục ghép hai vị trí thì không tách được vị trí nào bị giết, nên không hợp lệ); hai biến thể
  KHÁC HÀNH VI ở cùng một vị trí (như (g1) và (g2), hay (k1) đến (k4)) cũng là các mục riêng. Vì thế số mục
  `DOT_BIEN` = số **dòng biến thể** ở danh sách trên: (a), (b), (c), (f), (i) mỗi lớp một dòng (5); (d), (e),
  (g), (h), (j) mỗi lớp hai dòng (10); (k) bốn dòng (4) ⇒ **mười chín mục `DOT_BIEN`**. Dòng (c) làm đỏ hai
  ca nên mang hai kết quả đích, do đó mười chín dòng cho **hai mươi cặp (dòng, ca đích)**. Executor đếm lại
  trên mã của chính mình và khai từng dòng (một dòng không dựng được ở cách triển khai đã chọn phải khai
  KHÔNG ĐO ĐƯỢC kèm lý do, không lặng lẽ bỏ). Con số "mười chín" là kỳ vọng suy ra, không phải danh sách thứ
  hai: danh sách có thẩm quyền vẫn là (a)–(k) cùng quy tắc này. Lịch sử của con số: r2 gọi "bảy mục" và mỗi
  mục là một mục `DOT_BIEN`; r3 tách "lớp" khỏi "mục" (mười lớp, mười hai mục, mười ba cặp đích); r4 giữ mười
  lớp nhưng lên mười lăm mục vì (d), (e), (g) mỗi lớp thành hai dòng (mười sáu cặp đích); r5 thêm lớp (k) —
  mười một lớp — với bốn dòng: mười chín mục, hai mươi cặp đích (HINT lượt 4 đề nghị một dòng (k), tức mười
  sáu mục và mười bảy cặp; r5 không theo con số ấy, lý do ở dòng (k)).

  Mỗi đột biến phải chết **bằng `TinHieuChotCa` của đúng ca đích, đúng nhãn — và đúng tiểu nhãn khi dòng
  của nó nêu tiểu nhãn (r4)**, không bằng lỗi vô can
  (bài học *"ĐỘT BIẾN BỊ GIẾT KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO"*). Runner hiện có in tên ca kèm
  kiểu ngoại lệ trong ngoặc khi ngoại lệ KHÔNG phải `TinHieuChotCa`, và vẫn cho `OK giet 1/1` — nên
  KHÔNG dùng riêng rc hay chữ `OK` của runner. Phân hạng bằng cách đọc kiểu ngoại lệ, tên ca và nhãn
  (gọi thẳng hàm ca trên bản đột biến để đọc thông điệp `TinHieuChotCa`; runner chỉ in tên ca) và khai
  **ba hạng**: giết thật / tín dụng giả / sống sót, mỗi mục một dòng. Kèm một đối chứng cố ý vô can (ví
  dụ đột biến gây `NameError`) để chứng minh cách phân hạng không cấp tín dụng giả. Hạng "tín dụng giả"
  gồm mutant chết vì ngoại lệ vô can, và mutant chết bằng `TinHieuChotCa` của một ca KHÁC ca đích. Chết ở
  một nhãn khác của CÙNG ca đích thì không phải tín dụng giả nhưng phải khớp quy tắc nhãn của phép (A1)
  dưới đây.

  **Chốt ngược — hai phép đo riêng, không gộp (r3, lớp `chot-nguoc-khong-co-lap`).** Câu của r2 ("nới ca
  đích để nó không kiểm chốt ấy nữa thì mục tương ứng phải chuyển sang sống sót") không xác định phạm vi,
  và khi nhiều assertion phủ giao nhau thì đọc nó theo nghĩa nào cũng sai: đọc là "nới đúng nhãn mà cả ca
  phải sống" thì bác một bộ test đúng; đọc là "tắt cả ca" thì có cặp đỏ/xanh mà không chứng minh nhãn
  nào có răng. Số đo (rig của cross-review lượt 2, dựng theo B1–B3b của r2, chạy lại lúc 11:46:05Z và 11:46:12Z 29-09):
  nới riêng `B1` thì (a) vẫn chết ở `B2-eacces`; nới riêng `B2-eacces` thì (b) vẫn chết ở `B2-eio`; để cả
  ca sống, (a) phải nới cả năm nhãn `B1`, `B2-eacces`, `B2-eio`, `B2-doc-hong`, `B3-zombie`, còn (b) phải
  nới ba nhãn `B2-eacces`, `B2-eio`, `B2-doc-hong` (các số này là số của rig lượt 2 dựng theo B1–B3b của
  r2; từ r3 thêm các nhãn cũng dùng `stat` ném lỗi nên số nhãn phải nới để (a) sống còn LỚN HƠN — con số ở
  r4: KHÔNG ĐO ĐƯỢC, chưa ai nới tuần tự). Đó là các chốt có ích chồng lên nhau, không phải test
  yếu, và **không được xoá cho gọn**. r3 tách hai phép đo, mỗi dòng biến thể chạy CẢ HAI, ở từng ca đích
  ((c): làm riêng cho `t156_...` và cho `t157_...`):
  · **(A) CA ĐẦY ĐỦ.** Gọi hàm ca đăng ký (mặc định của helper: mọi nhãn chạy theo thứ tự, không nới) trên
    bản sao đột biến. Đo hai lần: **A1** không nới gì; **A2** nới đúng nhãn đích, mọi nhãn khác vẫn hiệu lực.
  · **(W) WITNESS CÔ LẬP.** Gọi TRỰC TIẾP cùng helper ấy (không viết lại assertion ở chỗ thứ hai — hai
    bản sẽ trôi lệch), chỉ chạy đầu vào của nhãn đích. Đo hai lần: **W1** nhãn đích không bị nới; **W0**
    nhãn đích bị nới.

  | phép | đầu vào chạy | assertion còn hiệu lực | kết quả cần có |
  |---|---|---|---|
  | A1 | mọi nhãn, đúng thứ tự | mọi assertion của mọi nhãn (kể cả kiểm seam đã chạm và bộ đếm); assertion sai đầu tiên ném | chết bằng `TinHieuChotCa` của ca đích; nhãn báo = nhãn đích, hoặc một nhãn đứng TRƯỚC nhãn đích trong thứ tự thực thi (khai rõ nhãn nào — hợp lệ). Nếu báo ở nhãn đích thì tiểu nhãn báo phải là tiểu nhãn của dòng (khi dòng nêu tiểu nhãn) |
  | A2 | mọi nhãn, đúng thứ tự | mọi assertion trừ nhãn đích | KHÔNG đòi gì; khai "sống sót" hoặc "chết ở nhãn Y" (Y là nhãn giết kế tiếp, luôn khác nhãn đích) |
  | W1 | chỉ đầu vào của nhãn đích | chỉ assertion mang nhãn đích | chết bằng `TinHieuChotCa` mà thông điệp mở đầu bằng nhãn đích, rồi đúng tiểu nhãn của dòng khi dòng nêu tiểu nhãn |
  | W0 | chỉ đầu vào của nhãn đích (vẫn chạy nguyên) | không assertion nào của nhãn đích; còn lại chỉ lỗi thiết lập và ngoại lệ vô can | sống sót (helper trả về bình thường); bộ đếm seam của nhãn ≥ 1 (chứng tỏ đầu vào ĐÃ chạy) |

  Tiêu chí, mỗi dòng biến thể: **ĐỎ** khi A1 sống sót; khi A1 báo nhãn đứng SAU nhãn đích (nhãn đích
  không còn răng hoặc ánh xạ sai); khi A1 hoặc W1 chết ở nhãn đích nhưng ở tiểu nhãn KHÁC tiểu nhãn của
  dòng (r4: đầu vào của dòng không còn răng riêng, hoặc bị đầu vào khác che); khi W1 không chết đúng nhãn
  đích; khi W0 không sống sót; hoặc khi phép D bên dưới đỏ. **KHÔNG ĐO
  ĐƯỢC** (không phải giết, không phải sống sót) khi W0 chết bằng ngoại lệ vô can hoặc bộ đếm seam của W0
  bằng 0 — dòng ấy chưa có chốt ngược, và handoff khai thẳng như vậy. A2 là dữ kiện cho log, không phải điều
  kiện đạt. **Không tính là chứng cứ ngược:** bỏ cả ca hoặc trả sớm; nới bằng cách xoá đầu vào; kết luận
  "sống" từ một W0 mà đầu vào không chạy. **Không nới suite thường:** ca đăng ký không truyền hai
  tham số tuỳ chọn CHẠY/NỚI. A1 KHÔNG tự chứng minh mặc định này: mutant có thể chết ở nhãn đứng trước
  nhãn đích, trong khi W1 truyền tập NỚI rỗng tường minh lại bật nhãn bị tắt ở suite thường.

  **(D) Chốt mặc định độc lập — QUAN SÁT thứ ĐÃ CHẠY, bắt buộc trước khi nhận bằng chứng A/W (r4, lớp
  `chot-nguoc-khong-co-lap`).** Vì sao cần: lời khai của r3 rằng chính A1 khoá mặc định "không nới" của
  helper là SAI. Lượt 3 nới mặc định của helper (test-only, trên bản sao) để chứa `B3-zombie`, rồi chạy
  A/W cho mọi dòng của r3: cả **mười ba cặp (dòng, ca đích)** của mười hai mục vẫn đạt. Cơ chế: dòng (c)
  bỏ toàn bộ phép đọc dự phòng nên A1 chết sớm ở `B2-doc-hong` (một nhãn hợp lệ đứng TRƯỚC `B3-zombie`,
  được A1 chấp nhận), còn W1 truyền tập NỚI rỗng tường minh nên bật lại `B3-zombie` và chết đúng nhãn;
  không phép nào nhìn thấy rằng ở ca đăng ký `B3-zombie` đã bị tắt. Ràng buộc bằng suy luận từ bằng
  chứng giết mutant sản phẩm không khoá được một thuộc tính của chính harness; D phải quan sát trực tiếp.
  1. **Đối tượng đo.** Trên ứng viên KHÔNG đột biến, gọi hai hàm ca đăng ký (`t156_...`, `t157_...`) đúng
     như suite thường, không override CHẠY/NỚI.
  2. **Quan sát.** Bọc `bang` bằng một observer chỉ ghi và chuyển tiếp nguyên vẹn (không đổi kết quả,
     không trả sớm, hoàn nguyên trong `finally`), ghi MỌI lần `bang` được gọi trong cả hai ca — kể cả
     lần đúng — dưới dạng (nhãn, tiểu nhãn nếu có) lấy từ đầu thông điệp.
  3. **Đối chiếu.** Tập ghi được phải BẰNG danh sách đơn vị ở "bảng tiểu nhãn" (ngay sau ma trận B2: 26
     đơn vị — 14 nhãn, trong đó sáu nhãn tách thành 18 tiểu nhãn), và thứ tự xuất hiện lần đầu của từng đơn
     vị trong mỗi ca phải đúng thứ tự cố định ở §7. Danh sách kỳ vọng viết CỨNG trong tập lệnh bằng chứng
     theo §7, KHÔNG lấy từ cấu hình CHẠY/NỚI của chính helper (lấy từ đó thì D đo helper bằng helper).
     Chỉ ghi seam đã chạm hay nhãn được chọn KHÔNG chứng minh assertion có hoạt động.
  4. **Control (D phải đỏ).** Trên bản sao TEST, không đụng mã sản phẩm: (i) lần lượt làm mặc định NỚI
     chứa từng nhãn trong **14 nhãn** ⇒ D đỏ, báo đúng nhãn thiếu; (ii) lần lượt bỏ assertion của từng
     tiểu nhãn trong **18 tiểu nhãn** của sáu nhãn tách được (bỏ MỘT đầu vào, giữ các đầu vào khác của
     cùng nhãn) ⇒ D đỏ, báo đúng tiểu nhãn thiếu. Bản mặc định đúng phải xanh. Kỳ vọng **32 control**
     (14 + 18) cộng hai lần xanh của bản đúng.
  5. **Chỗ đặt.** D và control của nó nằm ở tập lệnh bằng chứng cục bộ của executor, như phép A/W: không
     thêm ca đăng ký (vẫn hai ca), không sửa runner `--dot-bien`, không tăng số mục `DOT_BIEN` sản phẩm.
  6. **Nghĩa vụ log.** Lệnh nguyên văn, giờ UTC, rc, dòng xanh của bản đúng cho từng ca, và từng dòng
     control kèm đơn vị thiếu. **Không nhận A1/A2/W1/W0 là đủ** nếu thiếu D, nếu bản đúng đỏ, hoặc nếu
     bất kỳ control nào không đỏ.
  Đã đo, ba lần:
  · lượt 3 (rig của reviewer, 12:52:00Z 29-09, Python 3.12.3; observer chuyển tiếp `bang` thật), chỉ mức nhãn:
  bản mặc định đúng xanh ở cả hai ca; 13 control nới mặc định từng nhãn (mười hai nhãn của `t156_...`, một nhãn
  của `t157_...`) đều đỏ, mỗi cái báo đúng nhãn thiếu;
  · lượt 4 (13:32:26Z 29-09, 22 đơn vị): bản đúng xanh ở cả hai ca; 27 control (13 nhãn + 14 tiểu nhãn) đều
  đỏ, mỗi cái báo đúng đơn vị thiếu; đảo thứ tự hai nhãn làm D đỏ dù tập vẫn đủ (`missing=[]`, `order=False`,
  13:40:32Z);
  · phiên soạn r5 (15:35:15Z 29-09, rig sao chép, 26 đơn vị sau khi thêm `B2-pid-du-phong`): bản đúng xanh ở
  cả hai ca; **32 control (14 nhãn + 18 tiểu nhãn) đều đỏ**, mỗi cái báo đúng đơn vị thiếu (riêng nhãn
  `B2-pid-du-phong` báo đủ bốn tiểu nhãn, mỗi tiểu nhãn nới riêng báo đúng tiểu nhãn ấy); ba phép đảo thứ tự
  (hai nhãn đầu; `B2-pid-du-phong` với `B3-song`; `B2-dem-doc` với `B2-pid-du-phong`) đều làm D đỏ với
  `missing=[]`, `order=False` (15:35:38Z).
  **CHƯA ĐO:** tập lệnh bằng chứng của executor và D trên mã của executor.

  **Log mỗi dòng biến thể**: tên mục và vị trí, ca đích, nhãn đích và tiểu nhãn (nếu có), A1 (nhãn và
  tiểu nhãn báo), A2 (sống sót hoặc nhãn Y — đây là "các nhãn khác vẫn giết nó trong ca đầy đủ"; danh
  sách ĐỦ mọi nhãn giết được nó cần nới tuần tự và không bắt buộc), W1, W0 kèm bộ đếm seam.
  Cách làm là khả thi, không phải lời hứa. Đã thấy chạy trên rig của reviewer (bản nháp Q-A, KHÔNG phải
  ứng viên của executor):
  · lượt 2, chạy lại 11:46:06Z: witness cô lập cho đúng cặp — (a) nhãn `B1`: W1 chết `B1`, W0 sống sót;
  (b) nhãn `B2-eacces`: W1 chết `B2-eacces`, W0 sống sót; ba biến thể của bảng 3: W1 chết ở `B2-exception`,
  `B2-parse` và nhãn đếm-đọc (rig gọi là `B2-readcount`, đặc tả gọi là `B2-dem-doc`), W0 cả ba sống sót;
  · lượt 3, 29-09 (probe `prior` bắt đầu 12:40:50Z, probe `holes` 12:42:57Z, cùng Python 3.12.3): mười hai mục của r3 (mười ba cặp đích) đều có W1 chết đúng nhãn đích và
  W0 sống sót với bộ đếm seam ≥ 1, mười hai đột biến đều chết bằng `TinHieuChotCa` ở ca đích, đối chứng
  cố ý vô can (`NameError`) chết bằng `NameError` và không được tính là giết thật; và với ba đột biến
  mới của tầng đọc (bảng 5), witness cô lập trên cùng helper cho: đọc chỉ bắt `PermissionError` ⇒ W1 chết
  ở nhãn phụ ESRCH và nhãn phụ EIO, W0 sống sót; đọc trả `False` riêng cho ESRCH ⇒ W1 chết ở nhãn phụ
  ESRCH, W0 sống sót; nuốt riêng `KeyboardInterrupt` ⇒ W1 chết ở nhãn phụ `KeyboardInterrupt`, W0 sống
  sót (rig gọi các nhãn phụ ấy là `B2-read-ESRCH`, `B2-read-EIO`, `B2-read-KeyboardInterrupt`; đặc tả gọi
  chúng là tiểu nhãn `ESRCH`, `EIO` của `B2-doc-hong` và tiểu nhãn `doc` của `B2-tin-hieu`);
  · lượt 4 (13:32:47Z 29-09): mười lăm dòng của r4 (mười sáu cặp đích) đều được chấp nhận, mỗi W1 đúng nhãn
  và tiểu nhãn đích, mỗi W0 sống sót có bộ đếm seam chạm; runner thật cho `giet 1/1` ở mười bốn dòng và
  `giet 2/2` ở (c);
  · phiên soạn r5 (15:35:39Z–15:35:58Z 29-09, rig sao chép có helper mở rộng): mười chín dòng (hai mươi cặp
  đích) đều được chấp nhận — A1 chết bằng `TinHieuChotCa` đúng nhãn và tiểu nhãn, W1 chết đúng tiểu nhãn, W0
  sống sót có bộ đếm; ở bốn dòng (k1)–(k4) A2 sống sót (khi nới `B2-pid-du-phong` không nhãn nào khác giết
  được chúng, tức nhãn này là chốt DUY NHẤT của lớp (k)), đối chứng `NameError` chết bằng `NameError` và
  không được tính giết; runner thật chọn mười chín bản ghi cho `giet 1/1` ở mười tám dòng và `giet 2/2` ở
  (c), kết quả tổng `(0, 0)`. Ba hạng: 20 cặp giết thật / 0 tín dụng giả / 0 sống sót — trên prototype;
  · chưa có: mười chín dòng chạy trên ứng viên của executor.
- **B6 (cả write set) — delta và bằng chứng cục bộ thay CI.**
  `python .claude/dev/launcher_test.py` toàn suite **delta = 0 ca đỏ** so với nền, đo **cả hai vế trong
  một lệnh** trên cùng rig (bài học "PHÉP ĐO DELTA SO HAI VẾ": nền và ứng viên cùng dựng bằng một vòng
  lặp, cùng bước). `python .claude/dev/launcher_test.py --dot-bien`: không đột biến cũ nào đổi hạng.
  `python -m ruff check --select F .claude/dev/launcher.py .claude/dev/launcher_test.py`: delta F = 0
  (ruff vắng thì ghi `KHÔNG ĐO ĐƯỢC`, không ghi 0). Nền đo được ở r3 và đo lại ở r5 (§8; r3 11:49:59Z 29-09, `89fc4fa`,
  ruff 0.15.8 là NHỊ PHÂN độc lập `ruff`, vì `python -m ruff` vắng ở cả `python` lẫn `python3.12` của
  container này): `launcher.py` 0 lỗi F; `launcher_test.py` 5 lỗi F (cả năm là F841, dòng 2566, 3387,
  3629, 4110, 6061). "delta = 0" nghĩa là ứng viên KHÔNG hơn số nền ấy, đo lại trên nền tiếp nối.
  **Nghĩa vụ bằng chứng.** Mọi lệnh B1–B6 chạy **cục bộ trên Linux, đúng SHA ứng viên** (ghi
  `git rev-parse HEAD` cùng log). Log mỗi lệnh gồm: lệnh **nguyên văn**, giờ UTC bắt đầu, rc, và
  **dòng tổng nguyên văn** của runner (số qua / chạy / bỏ qua / đỏ; với `--dot-bien` là dòng tổng và
  ba hạng của B5). Log của B5 còn kèm **từng dòng biến thể** với bốn phép đo A1/A2/W1/W0 như đã định
  ở B5 (kỳ vọng mười chín dòng, cũng là mười chín mục `DOT_BIEN`, hai mươi cặp đích), và **log của phép D**: lệnh nguyên văn, giờ
  UTC, rc, dòng xanh của bản đúng cho từng ca đăng ký, và từng dòng trong 32 control (14 mức nhãn, 18 mức
  tiểu nhãn) kèm đơn vị thiếu. Đính vào handoff; reviewer đọc **trước** merge. Xanh của `gate-registry` KHÔNG thay
  cho log này (§8). Sau merge, `launcher-windows.yml` chạy ở lượt `push` master: đọc kết quả cả
  Windows lẫn Ubuntu (`land_obligation`), đừng suy thành công từ việc đã đẩy.
  **ĐỎ khi:** ứng viên có thêm ca đỏ, đột biến cũ đổi hạng, thêm lỗi F, handoff thiếu log nguyên văn cho
  bất kỳ lệnh nào trong B1–B6, hoặc thiếu log phép D, bản đúng không xanh ở D, hay có control của D không
  đỏ.
- **B7 — bằng chứng từ nơi lỗi lộ ra (không phải cổng).** Chạy `ops/lease_publish_test.py` với seam
  ESRCH chèn vào `launcher.py` bản sao tạm, hoặc chạy `t154` lặp nhiều lần song song: chỉ để khai,
  **không** dùng làm tiêu chí vì race chập chờn không đỏ ổn định (luật L3). Cross-review lượt 1
  (hướng 10) đã chạy `t154` với seam ở bản sao: nền ném `ProcessLookupError`, bản HẸP r1 qua.
  Cross-review lượt 2 (hướng 13, 11:29:11Z 29-09) chạy lại trên bản dựng theo Q-A r2: nền ném
  `ProcessLookupError` sau 1 lần chạm seam; bản dựng qua, 31 lần chạm seam, 4,87 giây, các tiến trình con
  cháu được thu hồi hết. Cross-review lượt 3 (12:50:55Z 29-09) đo lại trên bản dựng theo Q-A r3: nền ném
  `ProcessLookupError` sau 1 lần chạm seam (1,43 giây); bản dựng qua, 31 lần chạm seam, 5,136 giây, con cháu
  thu hồi hết. Đó là số của reviewer trên bản nháp, không phải phép đo trên ứng viên của executor và không
  do phiên soạn r3, r4 hay r5 chạy lại; thời lượng không phải hằng số.

## 8. Số đo nền (thời điểm đo cạnh từng số)

- **Nền nghiệm thu `89fc4fa` vẫn hợp lệ cho write set — đo lại ở r5 (15:36Z 29-09, kho
  `/home/user/tra-luat`, worktree của phiên soạn).** `git fetch -q origin master` rc=0 (15:36:08Z, xong
  15:36:09Z); `git rev-parse origin/master` ⇒ `44620e8706c86f5517b0f0e0a72759a59fd508ca` (Merge PR #684, commit
  lúc 12:39:55Z; `git rev-list --count 44620e8..origin/master` ⇒ 0, tức đầu master KHÔNG trôi kể từ lượt đo
  của r4). `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master --
  .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=0** (15:36:09Z); cùng lệnh với `-- .claude
  .github` ⇒ rc=0 (15:36:10Z). `git rev-parse origin/master:<tệp>` cho blob `561ff7a1840d65a6fc9953947f71cabe4947b3c9`
  (launcher.py) và `abf7f6cafd36c34392a31f6e1b24f3cd63a3c7c8` (launcher_test.py), `wc -l` ⇒ 4308 và 8354 dòng;
  `git rev-list --count 89fc4fa..origin/master` ⇒ 25 (19 không phải merge); `git diff --shortstat 89fc4fa
  origin/master` ⇒ 15 tệp, 6903 dòng thêm, 0 xoá. Kho không nông, `core.abbrev` = 7. Tất cả trùng số r4 đo
  lúc 13:07Z. Phép so hai nguồn ref: **KHÔNG làm lại ở r5** (chỉ fetch `master`).
- **Ruff nền — đo lại ở r5 (15:36:02Z, nhị phân `ruff` 0.15.8, `--no-cache --select F`, trên blob nền vì
  worktree ở `aa1446e` giữ nguyên hai blob ấy):** `launcher.py` "All checks passed" (0 lỗi F);
  `launcher_test.py` 5 lỗi, cả năm F841 ở dòng 2566, 3387, 3629, 4110, 6061 — trùng số r3 và lượt 3.
- **Nền nghiệm thu `89fc4fa` vẫn hợp lệ cho write set — đo lại ở r4 (13:07Z 29-09, kho
  `/home/user/tra-luat`, worktree của phiên soạn).** `git fetch -q origin master` rc=0 (13:07:29Z);
  `git rev-parse origin/master` ⇒ `44620e8706c86f5517b0f0e0a72759a59fd508ca` (Merge PR #684, commit lúc
  12:39:55Z). `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master --
  .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=0** (13:07:30Z): hai tệp trong write set giống
  hệt; `git rev-parse <ref>:<tệp>` cho blob `561ff7a1840d65a6fc9953947f71cabe4947b3c9` (launcher.py) và
  `abf7f6cafd36c34392a31f6e1b24f3cd63a3c7c8` (launcher_test.py) ở cả `89fc4fa`, `c57df32` lẫn `44620e8`;
  `wc -l` trên `origin/master` ⇒ 4308 và 8354 dòng. Cùng lúc, `git diff --quiet … -- .claude .github` ⇒
  rc=0 và ba tệp CI (`.claude/dev/ci_dang_ky_test.py`, `.github/workflows/ci.yml`,
  `.github/workflows/launcher-windows.yml`) giống hệt (rc=0). `git rev-list --count 89fc4fa..origin/master` ⇒
  **25** commit (**19** không phải merge); `git diff --shortstat 89fc4fa origin/master` ⇒ **15 tệp, 6903
  dòng thêm, 0 xoá**: `ops/land/pr680-wp676-land-evidence.yaml`, `ops/leases/t131-deadline-dem-spawn-exec-1-
  claude-20260929.yaml`, bảy tệp `ops/specs/dot-bien-l-bien-cong-khai-r1.md`…`-r7.md` và sáu tệp
  `ops/specs/lease-id-ep-kieu-yaml-r1.md`…`-r6.md`; số tệp đổi dưới `.claude/` hoặc `.github/` = **0**.
  Kho không nông (`--is-shallow-repository` ⇒ `false`), `core.abbrev` = 7. Phép so hai nguồn ref
  (`ls-remote` với `refs/remotes/origin/*`) **KHÔNG làm lại ở r4** — r4 chỉ fetch `master`, nên 516/517 dưới
  đây là số của r3 (11:56:41Z) và không được đọc như số hiện hành.
- **`origin/master` đã tiến; nền nghiệm thu `89fc4fa` vẫn hợp lệ cho write set (số của phiên soạn r3;
  r4 và r5 đo lại ở hai mục ngay trên).**
  Lệnh và kết quả, 29-09: `git fetch -q origin '+refs/heads/*:refs/remotes/origin/*'` rc=0 (11:44:35Z, rồi
  lại 11:56:41Z); `git rev-parse origin/master` ⇒ `1c23933b13f33d6b0ebdb2901a3dec33c474d34c` ở lần đầu,
  ⇒ `c57df32f0fd8c992ed363d7000f4f761275750ea` ở lần sau (`1c23933` là cha thứ nhất của nó). Reflog
  `refs/remotes/origin/master` ghi ba mục liên tiếp `89fc4fa` ⇒ `1c23933` ⇒ `c57df32`, cả ba là
  `fast-forward`; mục thứ hai là lần fetch 11:44:35Z của r3, còn mục thứ ba do một lần fetch KHÔNG phải của
  phiên soạn r3 (r3 chỉ chạy `git fetch` lúc 11:44:35Z và 11:56:41Z, lần sau không đổi gì) — kho
  `/home/user/tra-luat` được dùng chung, nên đầu `origin/master` có thể trôi giữa hai lệnh. Trên đầu hiện tại:
  `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py
  .claude/dev/launcher_test.py` ⇒ **rc=0** (11:56:41Z; cũng rc=0 với `1c23933` ở 11:44Z), tức hai tệp trong
  write set giống hệt. `git rev-list --count 89fc4fa..origin/master` ⇒ 14 commit (11 không phải merge);
  `git diff --shortstat 89fc4fa origin/master` ⇒ **8 tệp, 3100 dòng thêm, 0 xoá**: `ops/land/pr680-wp676-
  land-evidence.yaml`, `ops/leases/t131-deadline-dem-spawn-exec-1-claude-20260929.yaml` và sáu tệp
  `ops/specs/lease-id-ep-kieu-yaml-r1.md`…`-r6.md`; số tệp đổi dưới `.claude/` hoặc `.github/` = **0**
  (`git diff --name-only … | grep -c`). Cùng lúc, ba tệp CI liên quan (`.claude/dev/ci_dang_ky_test.py`,
  `.github/workflows/ci.yml`, `.github/workflows/launcher-windows.yml`) giống hệt (`git diff --quiet`, rc=0,
  11:56:41Z), nên các số ở mục "Đường thực thi" dưới đây còn nguyên. Hai lần ghi
  `89fc4fa` cũ ("đo lại 11:09Z và 11:14Z") vẫn đúng như đã đo lúc ấy; r3 KHÔNG thay nền bằng đầu mới, vì
  nền nghiệm thu neo theo nội dung write set và nó không đổi.
  So hai nguồn ref (11:56:41Z, sau fetch): `git ls-remote --heads origin` rc=0 ⇒ **516** nhánh trên máy
  chủ; **517** ref cục bộ `refs/remotes/origin/*` sau khi loại `HEAD`. So bằng TẬP TÊN (`comm`): thiếu
  cục bộ (có trên máy chủ, không có cục bộ) = **0**; thừa cục bộ = **1** (`claude/bookkeeping-574-land`,
  không còn trên máy chủ — vô hại, cùng nhánh thừa đã ghi ở r2; lần đo 11:44:40Z ra cùng 516/517 và cùng
  kết luận). Kho không nông (`--is-shallow-repository` ⇒ `false`), `core.abbrev` = 7. Không gặp `CHAN [12]`
  nên không phải sửa nhánh cục bộ `master`.
- Kích thước trên `origin/master` (`git show origin/master:<tệp> | wc -l`, 11:49:30Z, khi đó là `1c23933`;
  blob đo lại trùng ở `c57df32` nhờ `git diff --quiet` rc=0 ở trên, và ở `44620e8` lúc 13:07Z; số dòng
  4308/8354 đo lại ở `44620e8`):
  `launcher.py` 4308 dòng (blob `561ff7a1…`, sha256 `808ce5b3…9fc0`); `launcher_test.py` 8354 dòng (blob
  `abf7f6c…`; sha256 tệp `433af9d4…556a`). Blob của cả hai tệp ở `89fc4fa` và ở `origin/master` trùng nhau
  (`git rev-parse <ref>:<tệp>`).
- **Số ca của `launcher_test.py`, đếm bằng AST** (11:10:16Z 29-09, trên `origin/master:.claude/dev/launcher_test.py`;
  đo lại 11:46:05Z bằng probe `inventory` của lượt 2 trên bản sao rig, ra CÙNG số dưới đây; cross-review
  lượt 3 đo lại bằng AST lúc 12:50:02Z (189 ca = 155 `t` + 34 khác, hậu tố lớn nhất 155, không hổng), cùng
  số; phiên soạn r4 và r5 KHÔNG chạy lại phép đếm AST này (hai tệp giống hệt theo blob, nên số không đổi theo suy ra; r5 chỉ đếm số ca đăng ký của rig sau khi thêm hai ca: 191 = 189 + 2);
  đếm hàm mức đỉnh mang decorator `@ca`): **189 ca đăng ký = 155 ca tiền tố `t<số>` + 34 ca khác**
  (các ca tiền tố `r`: `r01`–`r21`, `r345`×5, `r347`×2, `r351`×3, `r348`×2, `r349`×1). Hậu tố lớn nhất
  của nhóm `t` là `t155`; 155 hậu tố phân biệt, không trùng, không hổng trong 1..155. **155 không phải
  tổng suite**: nó là hậu tố lớn nhất của một nhóm; bản r1 dùng nó làm tổng và sai. Nghiệm thu B6 phải
  đối chiếu số đăng ký, số chạy, số bỏ qua và số đỏ, không suy tổng từ hậu tố. Sau packet này, số đăng
  ký kỳ vọng tăng đúng bằng số ca mới ở §6.2 (**hai**) — executor đếm lại và khai.
- `DOT_BIEN` ở `launcher_test.py:7012`: **174 mục**; `DOT_BIEN_HARNESS` ở `:7930`: 3 mục (cùng phép đếm
  AST, 11:10:16Z; đo lại 11:46:05Z và bởi cross-review lượt 3 lúc 12:50:02Z, cùng số). Đây là số mục ĐỘT
  BIẾN, khác số ca. Số mục mới: xem B5 (**mười một** lớp, kỳ vọng **mười chín** mục `DOT_BIEN`; sau packet:
  bảng sản phẩm 174 + 19 = **193**, cộng 3 mục `DOT_BIEN_HARNESS` = **196** mục; số ca đăng ký 189 + 2 = **191**
  — toàn là số kỳ vọng suy ra, chưa đo trên ứng viên; trên rig sao chép của r5 đếm ra đúng 193 / 3 / 196 và
  191 ca, 15:35:38Z, bảng 6). Để khỏi lẫn với các revision trước: r3 kỳ vọng 174 + 12 = 186 (189 kèm harness),
  lượt 3 đã dựng 12 mục r3 và đếm ra đúng 186 / 189; r4 kỳ vọng 174 + 15 = 189 (192 kèm harness), lượt 4 đã dựng
  15 mục r4 và đếm ra đúng 189 / 192; HINT lượt 4 đề nghị 174 + 16 = 190 (193), r5 thay bằng 174 + 19 = 193 (196)
  vì tách (k) thành bốn dòng (B5). Số ca đăng ký không đổi qua r4 và r5 (191).
- **Lease** (chạy trong `/home/user/tra-luat` sau `git fetch` đủ, 29-09; lệnh `python ops/lease_publish.py
  ai-dang-giu <đường dẫn>`; hai lượt đo, mỗi lượt cùng kết quả — 11:45Z–11:49Z và 11:56Z–11:57Z, dưới đây ghi
  giờ lượt sau):
  `.claude/dev/launcher.py` ⇒ rc=0, `NGƯỜI_GIỮ 0: không có` (11:56:47Z);
  `.claude/dev/launcher_test.py` ⇒ rc=11, `NGƯỜI_GIỮ 1: ci-g5-cong-cu-chia-manh-r1-g2-claude`
  (`CÒN_HẠN`; hết hạn `2026-09-30T07:41:00Z`; 11:56:57Z);
  `.claude/dev/ci_dang_ky_test.py` ⇒ rc=11, `NGƯỜI_GIỮ 2: ci-duong-nhanh-ho-so-r2-g3-claude,
  ci-g5-cong-cu-chia-manh-r1-g2-claude` (11:57:08Z; thêm một bản `ci-duong-nhanh-ho-so-r2-g2-claude` hiện
  `CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ`, không tính là người giữ);
  `.github/workflows/launcher-windows.yml` ⇒ rc=0, `NGƯỜI_GIỮ 0` (11:57:20Z).
  Không lần nào gặp `CHAN [12]`. Nhánh `ops/cap-lease-ci-g5-cong-cu-chia-manh` (lease #668) nay ở
  `2ae5646de60219638c2fef8f838cd86920537154` (r2 ghi `7c16d11`): một commit hồ sơ review, tệp lease g2
  không đổi (xem `depends_on`).
- Tìm Issue/PR có sẵn cho `ProcessLookupError` / `_con_song` ⇒ 0 kết quả (09:4xZ, phép đo của r1; r2 và
  r3 KHÔNG đo lại). Tìm Issue cho quan sát `comm` không phải UTF-8 (§2): chưa làm.
- **Đường thực thi `launcher_test.py` trong CI** (đọc mã ở `ci_dang_ky_test.py` trên `89fc4fa`, đo bằng
  AST và chạy thử 11:09:52Z; cross-review lượt 1 đo độc lập bằng cách chạy `chay_moi` với worker giả;
  lượt 2 lặp lại ở hướng 4, 11:24:58Z: 9 lượt gọi worker, 0 lượt `launcher_test.py`; r3 đếm lại
  `MOI` = 9 mục ở `:37` và `DA_NOI` = 13 mục ở `:69`, `launcher_test` chỉ ở `DA_NOI`, 11:55:42Z):
  - `MOI` = dict ở `:37–53`, **9 mục**: `doc_receipt_thu_hoi_test`, `chon_reviewer_test`,
    `gh_readback_test`, `mcp_gh_test`, `mcp_github_doc_test`, `probe_mang_test`,
    `pretooluse_guard_test`, `subagent_ghi_detect_test`, `ops/nhanh_don_duoc_test`. **`launcher_test.py`
    không thuộc `MOI`.**
  - `DA_NOI` = set ở `:69–78`, **13 mục**, có `launcher_test.py`. `kiem()` (`:578–612`) chỉ đòi rằng mỗi
    mục có một dòng `run:` nhắc tới nó trong workflow — tức "đã nối" chứ **không** "được `gate-registry`
    chạy". Dòng nhắc tới `launcher_test.py` là ở `launcher-windows.yml:104` (suite), `:107` (`--dot-bien`)
    và `:206` (probe `t62`).
  - `chay_moi` = hàm ở `:962–1037`, mặc định `moi=MOI`; `--chay` (khai ở `:2011`; nhánh `if ns.chay` ở `:2043`) gọi đúng hàm này. Vậy
    **`gate-registry` chạy 9 bộ, 0 lượt gọi `launcher_test.py`**.
  - Job `launcher` của `launcher-windows.yml`: PR chỉ chạy khi có nhãn `windows`; push master chạm
    `paths: .claude/dev/**` thì chạy cả Windows (Python 3.13) lẫn Ubuntu (Python 3.11); gọi tay
    `workflow_dispatch` tuỳ tham số `runner_set`. Theo Q4 hai đường đầu không xảy ra trên PR này.
    Bản r1 §8 và closure của r1 khai sai điều này; đã sửa ở r2.
- Suite `launcher_test.py` trên nền: **chưa đo** ở phiên soạn — B6 bắt executor đo cả hai vế.
- Ruff nền (11:49:59Z, `89fc4fa`, nhị phân `ruff` 0.15.8; `python -m ruff` vắng): `launcher.py` 0 lỗi F,
  `launcher_test.py` 5 lỗi F (F841 ×5). Chi tiết ở B6.

Mọi con số phải được **đo lại** trước cấp lease và trước land (L5).

## 9. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục một lượt thất bại. Hình dạng đáng canh, ghi để lượt thi
hành không lặp: *"vá một lỗ mà mở lỗ khác trong cùng hàm"* / *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ
ba"* — và tới r5 nó đã xảy ra **năm lần trong cùng một packet**, cả năm do chính phiên soạn:
1. bản RỘNG (`except OSError: return False`) đóng ESRCH nhưng biến `PermissionError` trên PID sống
   thành "đã chết" (r1 §1);
2. bản HẸP r1 sửa lỗi 1 rồi mở lỗ zombie: đường lỗi mới đi thẳng `kill(pid, 0)` và mất phép phân
   biệt `Z` (bảng 2; cross-review lượt 1 bắt bằng phép đo);
3. **(lượt 2, mới ở r3)** r2 khai rằng nó "liệt kê hết đường TRƯỚC và cho mỗi đường một chốt riêng". Lượt
   2 đo được ba đường r2 KHÔNG có chốt — ngoại lệ thuộc `Exception` nhưng không thuộc `OSError` (một
   mình `KeyboardInterrupt` không phân biệt được), nội dung đọc được nhưng hỏng, và số lần ĐỌC (r2 chỉ đếm
   `stat`) — cả ba biến thể PASS hai ca mẫu (bảng 3), cộng một chỗ hở trong chính chốt ngược (nới đúng
   một nhãn nhưng nhãn khác vẫn giết mutant). Cùng hình dạng "danh sách đường tự liệt kê, cho là hết",
   nhưng nạn nhân lần này là ĐẶC TẢ NGHIỆM THU chứ không phải mã;
4. **(lượt 3, mới ở r4)** r3 vá đúng ba biểu hiện lượt 2 chỉ, và các bản vá ấy CÓ RĂNG (lượt 3 dựng lại
   cả ba đột biến và thấy chúng chết đúng nhãn). Rồi hình dạng lặp ở hai chỗ KHÔNG ai chỉ lúc đó.
   (i) r3 bỏ ba ô tầng đọc (ESRCH, EIO, `BaseException`) và gọi đó là "quyết định phạm vi" với lý do
   "EACCES làm đại diện cho họ `OSError`" — đúng chính giả định mà nghiệm thu phải kiểm — trong khi
   Q-A.4/.5 vẫn ràng buộc các ô ấy và bảng 5 đo được cả ba bằng cùng seam, không cần kernel. (ii) r3
   khai rằng chính A1 khoá mặc định "không nới" của helper: lời khai rộng hơn phép đo, vì A1 chấp nhận
   nhãn đứng trước (đây là bản vá ĐÚNG mà sinh LỖI MỚI: witness cô lập W đã sửa thật, còn mặc định thì
   không có phép quan sát nào). Nạn nhân lần thứ hai liên tiếp là ĐẶC TẢ NGHIỆM THU. Chữa theo lớp:
   ma trận không còn ô trống, mỗi đầu vào có tiểu nhãn và có dòng biến thể giết nó, và mặc định của
   helper có phép quan sát riêng (D) với control cho từng đơn vị.
5. **(lượt 4, mới ở r5)** r4 vá đúng và có răng cho ba biểu hiện lượt 3 chỉ (lượt 4 dựng lại d2/g2/e2 và D ở
   mức nhãn lẫn tiểu nhãn, cả hai đóng), rồi hình dạng lặp ở chỗ KHÔNG ai chỉ: r4 đặt mọi đầu vào đọc lỗi và
   hỏng trên PID SỐNG, nên đường Q-A.4 đi tiếp tới `kill(pid, 0)` không có đối chứng âm — bản trả `True` ngay
   sau lỗi đọc, không hỏi PID nào, qua cả hai ca mẫu lẫn D, mà vẫn báo "sống" cho PID con đã `wait`. Cái
   sai lần này KHÔNG nằm ở đường đầu vào (ESRCH, EIO, parse: r4 đã phủ hết) mà ở **chiều kết quả** của
   bước sau nó. Và bản HINT đề nghị (một dòng (k), một tiểu nhãn bắt cả bốn kết quả) cũng có hình dạng
   ấy ở cỡ nhỏ: mutant duy nhất của nó chết ở tiểu nhãn `song` bằng bộ đếm, nên `da-wait`, `eperm`, `eio`
   không có mutant riêng nào chạm tới chúng (bảng 6: ba biến thể k2–k4 cùng qua hai ca mẫu, mỗi cái chết
   đúng một tiểu nhãn khác nhau). Chữa theo lớp: mỗi tiểu nhãn kết quả có một dòng biến thể độc chiếm (k1–k4)
   và mỗi dòng đã được đo chết đúng tiểu nhãn của nó.

Mỗi bản vá/đặc tả đều ĐÚNG và CÓ RĂNG ở chỗ nó phủ; lỗ nằm ở đường KHÔNG ai chỉ. Các phép đo chỉ chứng
minh các đường đã thử. Miền kiểm của r5 gồm ESRCH, EACCES, EIO, zombie, ngoại lệ ngoài `OSError` ở hai
tầng hỏi/đọc (kể cả `KeyboardInterrupt` ở cả hai tầng), nội dung đọc hỏng, số lần hỏi/đọc và **kết quả của
bước PID dự phòng (sống, đã `wait`, EPERM, EIO) cùng số lần gọi `kill(pid, 0)`**; ma trận ở
B2 ghi rõ đầu vào từng tầng và chiều kết quả. B2 khoá bản RỘNG và các biến thể tầng đọc, B3/B3b
khoá bản HẸP r1; các lớp còn lại ở B5 khoá những biến thể đã liệt kê. **Không coi một danh sách mutant hữu hạn là bằng
chứng đã liệt kê hết mọi đường**; executor và reviewer vẫn phải kiểm các đường mới xuất hiện trong chính
cách triển khai được chọn.

**Ngưỡng ba lần đã chạm — câu hỏi đặt cho điều phối/chủ kho, r4 và r5 KHÔNG tự trả lời.** CLAUDE.md dạy đếm
hình dạng lỗi chứ không chỉ đếm lỗi: cùng một hình dạng lặp từ ba lần trở lên thì câu hỏi đúng là "có nên
làm việc này theo cách này không", không phải "vá thế nào". Đường hiện tại (giữ phép hỏi `exists()` rồi
dựng thêm một đường lỗi có đọc + `kill(pid, 0)`, Q-A.1–4) tự nó sinh ra nhiều đường cần chốt — đó là lý do
ma trận ở B2 phình dần từ r1 tới r5 (số dòng biến thể của B5: bảy ở r2, mười hai ở r3, mười lăm ở r4,
mười chín ở r5; số đơn vị assertion: 22 ở r4, 26 ở r5). Có thể cân nhắc một cấu trúc ít đường hơn (ví dụ dùng chính phép đọc
làm phép hỏi), nhưng nó đổi hành vi nhánh cũ mà Q-A.3 cấm đổi, và r4 lẫn r5 chưa đo phương án nào. Nên r5 giữ
hướng của r2, r3 và r4 và chỉ nêu ngưỡng; có hỏi lại quyết định gốc hay không là việc của điều phối/chủ kho.

## 10. `chua_do_duoc`

- Suite `launcher_test.py` và `--dot-bien` trên nền: chưa chạy ở phiên soạn. Phiên soạn r3 chỉ chạy lại
  probe của cross-review lượt 2 (bốn probe: `inventory`, `matrix_extra`, `stronger`, `mutations`, 11:46Z; `inventory` thoát rc=1 ở dòng
  cuối vì bản sao rig không có `SPEC.md`, còn các dòng số đã in đủ trước đó)
  trên hai ca mẫu do reviewer dựng ở bản sao rig; không chạy `python .claude/dev/launcher_test.py` đầy đủ.
  **Phiên soạn r4 không chạy probe hay suite nào**: nó chỉ áp HINT, đọc log của lượt 3, và chạy các lệnh
  git ở §8 (nền) cùng phép đo băm. **Phiên soạn r5 có chạy** (15:33Z–15:36Z 29-09) probe của lượt 4 trên một
  rig sao chép (bảng 6, B5) — vẫn không chạy `python .claude/dev/launcher_test.py` đầy đủ, không chạy suite
  hay toàn bộ 174 đột biến cũ.
- Ruff: đo được **nền** (§8, B6: `launcher.py` 0, `launcher_test.py` 5, nhị phân `ruff` 0.15.8; cross-review
  lượt 3 đo lại ra cùng số, đúng năm F841 ở dòng 2566, 3387, 3629, 4110, 6061); delta của ứng viên: chưa có
  ứng viên. `python -m ruff` vắng trong container soạn r3 (và trong sandbox của cross-review). Phiên soạn r4
  không chạy ruff; phiên soạn r5 chạy lại nhị phân `ruff` 0.15.8 trên blob nền (§8) ra cùng số.
- Nhánh Windows và Darwin: không đo (Q4); lần đo Windows đầu tiên là lượt push master sau merge. Các
  bảng ở §1 chỉ đo Linux, Python 3.12.3 cho bảng 3, 4, 5 và 6. Bảng 4 chỉ đo locale UTF-8 (`preferred_encoding`
  `utf-8`, và `LC_ALL=C.UTF-8`); locale không phải UTF-8: KHÔNG ĐO ĐƯỢC. Cross-review lượt 3 mô phỏng hai
  nhánh Windows và Darwin bằng seam (hai ca trả chuỗi BỎ QUA, không tính là QUA): đó là mô phỏng nhánh, KHÔNG
  phải hệ điều hành thật, và không thay `land_obligation`.
- Một ESRCH thật (không seam) trên `/proc/<pid>/stat`: chỉ thấy một lần ở CI (job `109303373142`),
  không tái hiện được theo yêu cầu; seam là cách đo duy nhất ổn định. Tương tự, EACCES/EIO ở `stat` hoặc
  ở `read_text` của một PID sống, và `KeyboardInterrupt` giữa hai phép ấy, chưa từng được thấy trên kernel
  thật; các bảng 1–3, 5 và 6 là đầu vào do seam đặt ra. Ba đầu vào tầng đọc của r4 (ESRCH, EIO,
  `KeyboardInterrupt`) và hai kết quả lỗi của `kill(pid, 0)` ở bảng 6 (EPERM, EIO) đo được bằng seam; việc
  chúng có xảy ra trên kernel thật: KHÔNG ĐO ĐƯỢC.
- Bản "r2" trong bảng §1 là bản nháp của phiên soạn (Q-A.1–4); chưa có bản vá của executor nào được đo với
  B1–B6. Các hàng "biến thể" của bảng 3 và bảng 5 là đột biến do reviewer lượt 2 và lượt 3 dựng, còn bảng 6
  do reviewer lượt 4 (mutant bỏ hỏi PID) và phiên soạn r5 (k2–k4) dựng; không hàng nào là bản của executor.
- **Chốt ngược A1/A2/W1/W0 và phép D (B5)**: đã thấy chạy trên rig của reviewer, bằng helper do reviewer
  viết (cờ nới `REVIEW_RELAX`). Lượt 3: mười hai mục của r3 (mười ba cặp đích) và ba đột biến tầng đọc của
  bảng 5; phép D ở **mức nhãn** (13 control đỏ, 12:52:00Z). Lượt 4 (13:32:26Z–13:40:32Z 29-09): mười lăm
  dòng của r4 (mười sáu cặp đích) đều được chấp nhận, D đủ 27 control (13 nhãn + 14 tiểu nhãn, 22 đơn vị) đều
  đỏ đúng đơn vị thiếu, và đảo thứ tự hai nhãn làm D đỏ. Phiên soạn r5 (15:35Z 29-09) dựng lại trên rig sao
  chép, có thêm nhãn `B2-pid-du-phong`: 20 cặp (19 dòng) được chấp nhận, D đủ 32 control (14 nhãn + 18 tiểu
  nhãn, 26 đơn vị), ba phép đảo thứ tự đều đỏ (bảng 6, B5). **CHƯA ĐO**, bao gồm: mười chín dòng của r5
  (hai mươi cặp đích) trên mã của ứng viên nào; tập lệnh bằng chứng của executor; tiểu nhãn báo trong thông
  điệp giết theo ĐÚNG chuỗi của đặc tả này (helper lượt 3 dùng tên nhãn phụ và tên đầu vào khác — `B2-read-ESRCH`,
  `access`/`io`/`read-error`, `empty`/`no-close`/`end`/`space`/`decode` — helper lượt 4 và helper mở rộng
  của r5 đã dùng tiểu nhãn của đặc tả, nhưng đó vẫn là helper của reviewer, không phải của executor); và bản
  thân hợp đồng helper ở §7 — lời văn của r3–r5, chưa có cài đặt của executor nào. Mặc định "không nới"
  của helper phải đo riêng bằng D và control test-only ở B5; A1 có chốt phủ giao nhau nên không chứng minh
  được điều này một mình.
- **Bất đối xứng hai đường về nội dung hỏng** (§2, §3): nhánh cũ trả `False`, nhánh mới rơi về `kill`. Đo
  được rằng nhánh cũ báo "đã chết" cho một PID sống có `comm` không phải UTF-8; chưa tìm Issue cho việc
  này, tần suất ngoài thực tế KHÔNG ĐO ĐƯỢC. Packet này không sửa, và không có ca nào khẳng định nhánh cũ
  đúng.
- Nội dung Mission #686 (Q0–Q5), comment `5888633201`, object ID `5628902742`, trạng thái lease #668
  live: phiên soạn không đọc lại từ GitHub; là lời khai của điều phối (số ở §8 đến từ `ai-dang-giu` chạy
  trên ref đã fetch ở r3, không phải từ GitHub live). Băm thân Issue: KHÔNG ĐO ĐƯỢC. ID comment PR #688
  chứa VERDICT lượt 2 (`5889523704`, đăng 11:40:59Z), lượt 3 (`5890856046`) và lượt 4 (`5891961732`, đăng 14:07:48Z)
  là dữ kiện điều phối cấp; phiên soạn r4 và r5 không kiểm chúng trên GitHub; giờ đăng comment lượt 3
  (13:02:58Z) và lượt 4 (14:07:48Z) do phiên điều phối đọc qua REST và điền vào trước khi đóng băng. (Bản r3
  của mục này ghi ID lượt 2 là "KHÔNG có" trong khi `nguon_cap_viec` của chính r3 đã điền nó; r4 sửa cho
  khớp.)
- Lease và ref: phiên soạn r4 và r5 KHÔNG đo lại các số lease (người giữ `launcher.py` 0, `launcher_test.py` 1, hạn
  `2026-09-30T07:41:00Z`) và KHÔNG so lại hai nguồn ref (516/517) — chỉ fetch `master` để đo nền. Cross-review
  lượt 3 không có ref và object lịch sử của lease #668 trong clone của họ (chỉ 4 ref nhánh; `cat-file -e
  2ae5646^{commit}` rc=128) nên cũng KHÔNG ĐO ĐƯỢC các số ấy; đừng suy "người giữ 0" từ một tập ref chưa so
  hai nguồn (cross-review lượt 4 cũng báo bundle chỉ có 4 ref nhánh và object `2ae5646` vắng, rc 128). Đo lại lúc cấp lease.
- Phép đo `t154` của B7: chỉ có số của reviewer trên bản nháp — lượt 2 (nền ném `ProcessLookupError` sau 1 lần
  chạm seam; bản dựng qua, 31 lần chạm, 4,87 giây) và lượt 3 (12:50:55Z: nền 1 lần chạm, 1,43 giây; bản dựng
  qua, 31 lần chạm, 5,136 giây) và lượt 4 (rig khác: 54 lần chạm, 4,938 giây, seam bơm lỗi đúng một lần — phép đo
  khác, không phủ định 31) — phiên soạn r3, r4 và r5 không chạy lại, và không có ứng viên của executor
  để chạy.
- B6 toàn suite và toàn bộ 174 đột biến cũ: KHÔNG ĐO ĐƯỢC ở r3, r4 lẫn r5. Lượt 3, lượt 4 và phiên soạn r5 chỉ
  đếm được rằng số mỏ neo của 174 mục cũ không đổi (count changes rỗng) — đếm mỏ neo không thay bằng chứng ấy.
- Tổng số ca `launcher_test.py` và số mục `DOT_BIEN` sau packet: chưa đo trên ứng viên nào (kỳ vọng ở §8
  và B5: 191 ca đăng ký; 193 mục `DOT_BIEN` sản phẩm, 196 kèm `DOT_BIEN_HARNESS`; 26 đơn vị assertion và 32
  control của D đếm từ bảng tiểu nhãn). Trên rig sao chép của phiên soạn r5 (prototype, xem bảng 6) đếm ra
  đúng 191 / 193 / 196; đó không phải phép đo trên mã của executor. Các số r4 (15 mục, 16 cặp, 22 đơn vị,
  27 control) trong bảng lịch sử và log cũ không phải tổng nghiệm thu của revision hiện hành.
- **Số của r5 chỉ có trong rig tạm của phiên soạn** (một bản sao `.claude/dev/` của rig cross-review lượt 4,
  cộng một helper mở rộng thêm nhãn `B2-pid-du-phong`, cộng bốn tệp biến thể k1–k4). Rig ấy chưa được đóng
  gói vào kho hay hồ sơ nào; nó **KHÔNG tái lập được từ kho** mà phải dựng lại, và nó không phải mã của
  executor. Mọi con số đo của r5 ở bảng 6 và B5 là số trên prototype ấy.
- PID con đã `wait` bị hệ điều hành tái dùng giữa lúc `wait` và lúc đo: xác suất KHÔNG ĐO ĐƯỢC. Khe này có
  sẵn ở `B1` và `B3-da-wait` và không do r5 mở ra; ở `B2-pid-du-phong` `da-wait`, nếu PID bị tái dùng thì
  `kill(pid, 0)` thật thành công và ca báo `TinHieuChotCa` cho một bản ĐÚNG (dương tính giả); 8 lời gọi
  chạy sát nhau, không có lần `wait` nào chen giữa. Chạy lại là cách phân biệt; ca không khoá được khe này.
