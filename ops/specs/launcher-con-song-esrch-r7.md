# ĐẶC TẢ — `LAUNCHER-CON-SONG-ESRCH` — **revision 7, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp685` (ID bền, `wp<issue>`); tên đọc được: `LAUNCHER-CON-SONG-ESRCH`. Lease dùng tên nào cũng phải kèm `packet_issue: 685`. |
| `revision` | **7** |
| `thay_the_cho` | r6 = `ops/specs/launcher-con-song-esrch-r6.md`, sha256 `fadad3c7fe293fe9ed93612b5f06ac26e1e2b1026613dd78349018c85f753c99`, commit `82d05eb` (`82d05eb71ca64cbe44da546f1bd3d4b5948a6913`). Trước đó: r5 = `ops/specs/launcher-con-song-esrch-r5.md`, sha256 `a0842320c4a760ca3cbc0c269f3e8f856b0e0bfa40bfc4fde6a20672b7dd7928`, commit `1b13110` (`1b131101e69704de3eb6aa1a3c0fd6e65f810bd9`); r4 = `ops/specs/launcher-con-song-esrch-r4.md`, sha256 `2c84a1bda6e39e9a07a883a506d2a6456a09e0ee2f6229e2b2fbcdb55cc2ae67`, commit `673f00c` (`673f00ca5d0a9880170a49269161b2ca88af811e`); r3 = `ops/specs/launcher-con-song-esrch-r3.md`, sha256 `7ef008f83c9c5efc3ee84864da77db1428133512dd494ecf6058c37f82d1a895`, commit `f8ddd49` (`f8ddd49437d163c230a38fefdcbec582e6cdeb75`); r2 = `ops/specs/launcher-con-song-esrch-r2.md`, sha256 `de9c553aaeb4cb2dae16385e3059a5a196248230a4ed18a42016c8af6fac9ce4`, commit `cdf0575` (`cdf0575358270843fbde51f817f0d6a4d9655dec`); r1 = `ops/specs/launcher-con-song-esrch-r1.md`, sha256 `ee44238c…37d9`, commit `d96d075`. r1, r2, r3, r4, r5 và r6 giữ nguyên, không sửa đè (phiên soạn r7 đo lại sáu băm lúc 01:46:54Z 30-09 bằng `sha256sum`, khớp cả sáu; `git diff --quiet HEAD --` trên sáu tệp ⇒ rc=0); r7 là bản duy nhất được cấp lease. |
| `packet_issue` | **#685** |
| `mission_issue` | **#686** (Mission Issue, object ID `5628902742`). Thân #686 khai ngay đầu rằng nó do phiên agent đăng hộ chủ kho bằng credential chủ kho; nguồn thẩm quyền là các câu trả lời của chủ kho được trích trong đó (Q0–Q4 trong thân; Q5 ở comment `5888633201`, xem `nguon_cap_viec`). |
| `nguon_cap_viec` | (r1) Chỉ thị chủ kho 29-09-2026: *"mở packet riêng cho bản vá launcher (race ProcessLookupError) đi"*. Nguồn lỗi: PR #679, job `gate-ops (ubuntu-latest)` `109303373142`, phân tích ở PR #679 comment `5885963131`. (r2) Cross-review lượt 1 trên PR #688, reviewed commit `d96d075`: `changes_requested`, 2 P1 / 3 P2 / 0 P3; VERDICT sha256 `69dbf916648790c7452d6e0bb7fa56b3a44c59df6c568ea29a1c5bf2eba1d9fb` (viết tắt `69dbf916…d9fb`). (r3) Cross-review lượt 2 trên PR #688, reviewed commit `cdf0575` (spec sha256 khớp băm r2 ở `thay_the_cho`): `changes_requested`, **0 P1 / 2 P2 / 0 P3**; hai P1 của lượt 1 đã đóng (VERDICT lượt 2, bảng ĐỐI CHIẾU LƯỢT TRƯỚC: bốn trong năm lớp của lượt 1 ĐÃ ĐÓNG, riêng `ma-tran-loi-thieu-chot` còn mở); VERDICT sha256 `19f5faa0a210d28f3a25f94e5ff65883431c2645da19dd9354bc9e51216ba47f` (viết tắt `19f5faa0…a47f`; phiên soạn r3 đo lại băm tệp `VERDICT.md` trong hồ sơ lượt 2 lúc 11:49Z ra đúng chuỗi này), comment PR #688 `5889523704`, đăng 11:40:59Z 29-09 (phiên điều phối đọc qua API sau khi r3 soạn xong, điền vào trước khi đóng băng). Hai lớp P2 của lượt 2: `ma-tran-loi-thieu-chot`, `chot-nguoc-khong-co-lap`. (r4) Cross-review lượt 3 trên PR #688, reviewed commit `8d1e568fa4a63c9e19020b0611299019f245de8e` (là r3 ở `f8ddd49` cộng merge master `c57df32`; reviewed tree `c0d8ee82a032bfb3bb2e0396e82b52ab493e2f3e`; spec sha256 khớp băm r3 ở `thay_the_cho`): `changes_requested`, **0 P1 / 2 P2 / 0 P3**; bốn trong năm lớp của lượt 1 vẫn ĐÃ ĐÓNG (không tái phát), `ma-tran-loi-thieu-chot` **CÒN MỞ**, `chot-nguoc-khong-co-lap` **VÁ SINH LỖI MỚI** (witness cô lập W đã sửa thật, lỗi nằm ở lời khai rằng A1 khoá mặc định của helper); VERDICT sha256 `868dc562c8d6d99bcbc692feec4a5d9bcd45f3aeedb62f7510e4ff62a4b69da7` (viết tắt `868dc562…9da7`; phiên soạn r4 đo lại băm tệp `VERDICT.md` trong hồ sơ lượt 3 lúc 13:07:57Z 29-09 ra đúng chuỗi này), `HINT.patch` sha256 `2371d2d1432211a188d95f73949b0e5781f1fcf27bda17e890d90ac57de3cabd` (đo cùng lúc), comment PR #688 `5890856046`, đăng 13:02:58Z 29-09 (phiên điều phối đọc `created_at` qua REST sau khi r4 soạn xong, điền vào trước khi đóng băng). Hai lớp P2 của lượt 3 giữ slug của lượt 2: `ma-tran-loi-thieu-chot`, `chot-nguoc-khong-co-lap`. (r5) Cross-review lượt 4 trên PR #688, reviewed commit `aa1446e19a6ce3f4b51f678f466f90d4857f1776` (là r4 ở `673f00c` cộng merge master `44620e8`; reviewed tree `65504f7fb737d1fb29028c0134489833a5278b74`; spec sha256 khớp băm r4 ở `thay_the_cho`): `changes_requested`, **0 P1 / 1 P2 / 0 P3**; bốn trong năm lớp của lượt 1 vẫn ĐÃ ĐÓNG (không tái phát), `chot-nguoc-khong-co-lap` **ĐÃ ĐÓNG** (ba biểu hiện tầng đọc của lượt 3 đã đóng; phép D đủ 27 control), `ma-tran-loi-thieu-chot` **CÒN MỞ** (hai ca bắt buộc không phân biệt được "gọi PID dự phòng `os.kill(pid, 0)`" với "trả `True` ngay sau lỗi đọc"; bản sai qua cả hai ca và phép D nhưng báo "sống" cho PID con đã `wait`); VERDICT sha256 `2c479e288d61254deff91c04303cfd495a3ec33473b3ec23a7e2198ccd87665c` (viết tắt `2c479e28…665c`; phiên soạn r5 đo lại băm tệp `VERDICT.md` trong hồ sơ lượt 4 lúc 15:41:11Z 29-09 ra đúng chuỗi này), `HINT.patch` sha256 `59964a4a6b04d93cb74a96f7c416f5559b5464bd0b857be093bcd0b32612c0aa` (đo cùng lúc), comment PR #688 `5891961732`, đăng 14:07:48Z 29-09 (phiên điều phối đọc qua REST, điền vào trước khi đóng băng; phiên soạn r5 không kiểm trên GitHub). Lớp P2 duy nhất của lượt 4 giữ slug của lượt 1 và lượt 3: `ma-tran-loi-thieu-chot`. (r6) Cross-review lượt 5 trên PR #688, reviewed commit `1b131101e69704de3eb6aa1a3c0fd6e65f810bd9` (là r5 ở `1b13110`, cha là `aa1446e`; reviewed tree `8d968b7e4df50015cfe75aff548c4fe3baf718ce`, phiên soạn r6 đo lại `git rev-parse HEAD^{tree}` trên worktree ra đúng chuỗi này; spec sha256 khớp băm r5 ở `thay_the_cho`): `changes_requested`, **0 P1 / 1 P2 / 0 P3**; bốn trong năm lớp của lượt 1 vẫn ĐÃ ĐÓNG (không tái phát), `chot-nguoc-khong-co-lap` vẫn **ĐÃ ĐÓNG**, `ma-tran-loi-thieu-chot` **CÒN MỞ** (biểu hiện PID dự phòng của lượt 4 đã đóng: k1–k4 chết đúng tiểu nhãn, phép D đủ 32 control; biểu hiện mới: nhóm bắt `ValueError`/`IndexError` của tầng đọc đem sang tầng hỏi vẫn qua hai ca r5 và phép D, nuốt `IndexError` của phép hỏi, trái Q-A.5); VERDICT sha256 `72c4c3f2cda31a96566c81c6daaf1f2c0ebca1bd464e2a5f61b2d67add4609a4` (viết tắt `72c4c3f2…09a4`; phiên soạn r6 đo lại băm tệp `VERDICT.md` trong hồ sơ lượt 5 lúc 16:48:21Z 29-09 ra đúng chuỗi này), `HINT.patch` sha256 `93b187e208942173c3e6b5bcb241e0c1af4edac7602b0f3781843951209a3531` (viết tắt `93b187e2…3531`; đo cùng lúc), comment PR #688 `5894035533`, đăng 16:09:51Z 29-09 (phiên điều phối đọc qua REST, điền vào trước khi đóng băng; phiên soạn r6 không kiểm trên GitHub). Lớp P2 duy nhất của lượt 5 giữ slug của lượt 1, 3 và 4: `ma-tran-loi-thieu-chot`. (r7) Cross-review lượt 6 trên PR #688, reviewed commit `82d05eb71ca64cbe44da546f1bd3d4b5948a6913` (là r6 ở `82d05eb`, cha là `1b13110`; spec sha256 khớp băm r6 ở `thay_the_cho`). **Reviewer là Claude Opus 5.5 (`claude-opus-5-5`), hạng `advisory_review`, CÙNG HỌ với executor và với phiên soạn — KHÔNG phải `cross_approved`** (protocol §8 đòi khác họ); chủ kho chỉ định Claude thay codex vì codex hết quota; họ model là tự khai của reviewer, không có phép đo máy. Kết luận `changes_requested`, **0 P1 / 2 P2 / 2 P3**; bốn trong năm lớp của lượt 1 vẫn ĐÃ ĐÓNG, `chot-nguoc-khong-co-lap` vẫn **ĐÃ ĐÓNG** (43 control), `ma-tran-loi-thieu-chot` **CÒN MỞ** — lần thứ bảy (biểu hiện lượt 5 đã đóng; biểu hiện mới: bảng không gian r6 bỏ sót nhánh cũ của Q-A.3, hỏi/đọc lại có điều kiện theo lớp ngoại lệ, cú pháp phép tách khi `comm` chứa `)`); ba lớp mới: `b2-parse-nhan-dien-theo-gia-tri` (P2), `so-lieu-noi-bo-lech` (P3), `san-dot-bien-windows` (P3). VERDICT sha256 `902cd85f274474e32e1a1781127599d5c454f239eb908230982c2866891ae255` (viết tắt `902cd85f…e255`), `HINT.patch` sha256 `2ba4acdbf9e190865c6b90a60c6d3843fcea89ad3161e475d626819ff1333a96` (viết tắt `2ba4acdb…1a96`); phiên soạn r7 đo lại cả hai băm trên hồ sơ lượt 6 lúc 01:17:34Z 30-09, khớp. Comment PR #688 `5902146149`, đăng 01:16:56Z 30-09 (phiên điều phối đọc qua REST; phiên soạn r7 không kiểm trên GitHub). Mission #686 comment `5888633201` (Q5: điều kiện cấp lease); phiên soạn r2, r3, r4, r5, r6 và r7 KHÔNG đọc lại nội dung comment này, coi nó là lời khai của điều phối, và không chép điều kiện nào từ nó vào đặc tả. |
| `objective` | `_con_song` không bao giờ để một ngoại lệ `OSError` của phép hỏi `/proc/<pid>/stat` thoát ra; tiến trình biến mất giữa chừng (ESRCH) được báo là đã chết; lỗi khác KHÔNG được đọc thành "đã chết" chỉ vì không stat được, và một zombie vẫn được báo là đã chết khi nội dung `/proc/<pid>/stat` còn đọc được. |
| `review_class` | **`sensitive`** — protocol §8: *"launcher hoặc gate lifecycle"*. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | `claude` — **Claude Sonnet 5.5, effort high** (Mission #686 Q3); phiên điều phối kiểm lại độc lập và commit. |
| `environment` | **`cloud`**. Bản vá chỉ chạm nhánh Linux của `_con_song`; nhánh Windows trả về trước dòng 650. |
| reviewer | `codex` (`gpt-6-astra`, effort ≥ medium), cần `cross_approved`. Protocol §8: HINT không được chứa mã launcher; chỉ được chứa mã TEST thuần. (r7) Lượt 6 trên PR #688 — review ĐẶC TẢ, không phải review bản thi hành — do Claude Opus 5.5 làm theo chỉ định của chủ kho, hạng `advisory_review`; nó không thay yêu cầu `cross_approved` khác họ cho PR thi hành. |
| `depends_on` | Lease `ci-g5-cong-cu-chia-manh-r1-g2-claude` (packet #668) giữ `.claude/dev/launcher_test.py`, `lease_expires_at_utc` = `2026-09-30T07:41:00Z` (đọc từ tệp lease trên nhánh `ops/cap-lease-ci-g5-cong-cu-chia-manh`; `ai-dang-giu` báo `CÒN_HẠN`, `NGƯỜI_GIỮ 1`, rc=11, lúc 11:56:57Z 29-09; cùng kết quả ở 11:45:23Z). Đầu nhánh ấy đã đi từ `7c16d11` (r2) sang `2ae5646` (một commit chỉ thêm hồ sơ review #668, 11:26:38Z); tệp lease g2 giữa hai đầu nhánh KHÔNG đổi (`git diff --quiet 7c16d11 2ae5646 -- <tệp lease>` rc=0, 11:49Z). Phải nhả hoặc hết hạn trước khi cấp lease cho `wp685` (Mission #686 Q1). `.claude/dev/launcher.py`: `NGƯỜI_GIỮ 0`, rc=0 (11:56:47Z; cùng kết quả ở 11:45:12Z). Chi tiết phép đo ở §8. **Mọi số lease trong ô này là số đo của phiên soạn r3; phiên soạn r4, r5, r6 và r7 KHÔNG đo lại chúng (KHÔNG ĐO ĐƯỢC ở r4, r5, r6 và r7; hạn `2026-09-30T07:41:00Z` của lease #668 là số đọc ở r3, trạng thái hiện hành chưa đo)** — đo lại lúc cấp lease, và không suy "người giữ 0" từ một tập ref chưa so hai nguồn. |
| nền nghiệm thu | `origin/master` `89fc4fac8cea65979cc2483043dc8cd07a6e8518` — **vẫn hợp lệ cho hai tệp trong write set** dù `origin/master` đã tiến nhiều lần từ lúc chọn nền. **Đo lại ở r7 (chạy trong worktree của phiên soạn, HEAD `82d05eb`, sạch):** `git fetch -q origin master` rc=0 (01:46:15Z 30-09, xong 01:46:16Z), `git rev-parse origin/master` ⇒ `c16bec639efa0077def4916c25c3e0c17f68dcaa` (Merge PR #693; **master ĐÃ TRÔI**: `git rev-list --count 44620e8..origin/master` ⇒ 22), rồi `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=0** (01:46:16Z), và cùng lệnh với `-- .claude .github` ⇒ rc=0 (01:46:16Z; chi tiết §8). **Đo lại ở r6:** `git fetch -q origin master` rc=0 (16:46:44Z, xong 16:46:45Z), `git rev-parse origin/master` ⇒ `44620e8706c86f5517b0f0e0a72759a59fd508ca` (`git rev-list --count 44620e8..origin/master` ⇒ 0: không trôi kể từ r4 và r5), rồi `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=0** (16:46:45Z), và cùng lệnh với `-- .claude .github` ⇒ rc=0 (16:46:45Z; chi tiết §8). Đo lại ở r5: `git fetch -q origin master` rc=0 (15:36:08Z), `git rev-parse origin/master` ⇒ `44620e8706c86f5517b0f0e0a72759a59fd508ca` (không trôi kể từ r4), rồi `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=0** (15:36:09Z), và cùng lệnh với `-- .claude .github` ⇒ rc=0 (15:36:10Z; chi tiết §8). Đo lại ở r4: `git fetch -q origin master` rc=0, `git rev-parse origin/master` ⇒ `44620e8706c86f5517b0f0e0a72759a59fd508ca` (Merge PR #684, commit lúc 12:39:55Z), rồi `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=0** (13:07:30Z 29-09), và không tệp nào dưới `.claude/` hay `.github/` đổi (rc=0 cùng lúc; chi tiết §8). Ở r3 cùng phép đo ra rc=0 với `1c23933` (11:44Z) và `c57df32` (11:56:41Z). Đầu `origin/master` sẽ còn trôi: đo lại lúc cấp lease. Nền tiếp nối (continuation base) sẽ khác khi #668 land trước; khai riêng lúc cấp lease, không thay nền này (protocol §3.2.1). |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/launcher-con-song-esrch-r7.md`, không loại dòng nào. Giá trị được công
bố **ngoài** tệp: comment trên #685 và lease, kèm OID commit + đường dẫn. Khối closure dưới đây
nằm **trong** tệp, nên một `spec_hash` không thể đi với hai closure khác nhau. Đổi bất kỳ byte nào
⇒ revision mới, băm mới, lease mới. Băm của r1 (`ee44238c…37d9`), của r2 (`de9c553a…9ce4`), của r3
(`7ef008f8…a895`), của r4 (`2c84a1bd…ae67`), của r5 (`a0842320…7928`) và của r6 (`fadad3c7…3c99`) KHÔNG còn
dùng để cấp lease.

**Closure đóng băng** (các trường dispatcher dẫn xuất, protocol §3.2), điền tay theo **miễn trừ có
phạm vi** ở Mission Issue #686: chỉ `wp685`, hết hiệu lực ở lần đầu một policy canonical cho closure
xuất hiện trên nhánh mặc định.

| trường | giá trị |
|---|---|
| `change_policy_sha` | `null` — chưa có policy canonical; descriptor thay thế là miễn trừ ở #686 |
| `effective_write_set` | `.claude/dev/launcher.py` · `.claude/dev/launcher_test.py` (exact) |
| `effective_review_class` | `sensitive` |
| `required_checks` | Trên PR thi hành: `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-registry (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)` của `.github/workflows/ci.yml`, workflow `thu-hoi` — các job này có thật và phải xanh, nhưng **KHÔNG job nào trong số đó chạy `launcher_test.py`** (`gate-registry` chạy chín bộ thuộc `MOI`, không có `launcher_test.py`; xem §8). Ngoài các check CI, **bắt buộc** bằng chứng cục bộ Linux B1–B6 neo exact candidate SHA (lệnh nguyên văn, giờ UTC, rc, dòng tổng), đính vào handoff và reviewer đọc trước merge; cross-review codex `cross_approved`, 0 P1/P2/P3 |
| `land_obligations` | Chủ kho audit + merge (không tự merge/approve); đọc kết quả `launcher-windows.yml` ở lượt `push` lên master sau merge, cả job Windows lẫn job Ubuntu, và báo — kể cả dòng `DOT BIEN:` của bước `Tu dot bien` trên Windows: `DUOI SAN` (dưới sàn 70 % của `--dot-bien`) là ĐỎ của packet này, không phải đỏ sẵn (§7 B4, r7); ghi sổ verdict + HINT vào `ops/reviews/` kèm receipt và mục README; thu hồi lease sau land; đóng #685 |

**Descriptor nguồn closure** = `{mission_issue: 686, object_id: 5628902742}`. Lease phải **chép**
đúng các giá trị trên; lệch ⇒ **DỪNG**. Băm thân Issue ở phía nhận là **KHÔNG ĐO ĐƯỢC** từ phiên
soạn (đường đọc MCP chuẩn hoá thực thể HTML trong thân issue, xem CLAUDE.md), nên neo bằng object
ID + số Issue.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

**Thay đổi so với r6** (mỗi dòng ứng với một lớp của VERDICT lượt 6, hồ sơ cross-review PR #688; slug là tên
lớp trong bảng lớp của VERDICT; các số trong bảng này là số hiện hành của r7). r7 áp `HINT.patch` của lượt 6 (4 nhóm
`# lop:`, 29 hunk, 55 398 byte, sha256 `2ba4acdb…1a96`) lên bản sao r6. Mỗi nhóm là diff ĐỘC LẬP so với r6 gốc
(VERDICT lượt 6, mục DRY-RUN), nên áp nguyên tệp cho đúng bản gộp. HINT nhắm r6 nên chỉ đổi tên tệp trên các dòng tiêu
đề `---`/`+++` của từng nhóm, không đổi dòng ngữ cảnh nào: `cp` r6 thành r7, rồi `sed -E` với biểu thức
`/^(---|[+]{3}) /s#launcher-con-song-esrch-r6.md#launcher-con-song-esrch-r7.md#` trên `HINT.patch`, đưa qua
`patch -p0 --fuzz=0` từ gốc worktree. (Lệnh chạy lúc soạn viết ba dấu cộng bằng ký tự thoát; biểu thức ghi ở đây là
dạng tương đương không dùng ký tự thoát — đo lại dạng này trên một bản sao r6 riêng lúc 01:49:12Z 30-09 cho cùng rc và
cùng sha256.) Kết quả: **rc=0**, bốn lần `patching file`, không tệp `.orig` hay `.rej`, 1646 dòng, sha256 bản chỉ-HINT
`8f0858baa8b52bf9e1c29324aac71ee38909f418cc9b19cc061bb8c21c8fb5c4` (`8f0858ba…fb5c4`) — trùng đúng bản gộp mà VERDICT
lượt 6 khai; `git status --short` chỉ có tệp r7 mới, r1–r6 nguyên byte.

**Vì sao r7 KHÔNG dừng ở HINT.** HINT đóng đúng ba chỗ reviewer chỉ (nhánh cũ bằng `B2-nhanh-cu` năm đầu vào; quy ước
đếm; `comm` chứa `)`) và có răng ở chỗ nó phủ. Nhưng đây là lần thứ **bảy** của cùng một hình dạng, nên r7 làm theo
đúng thứ tự CLAUDE.md dạy — liệt kê MỌI đường của `_con_song` nhánh Linux TRƯỚC, rồi mới đóng (bảng không gian mở rộng,
§7 B2). Phép đo cho thấy việc này không phải nghi lễ: trên rig r7, một helper dựng đúng theo HINT (bản sao
`helper_block_r7.py` của reviewer lượt 6) để lọt **34** biến thể trái Q-A trong 89 biến thể của phép (E) — cả `t156` lẫn
`t157` đều sống (bảng 9 dòng 7). Ngoài ra, câu chữ của HINT về luật nguồn (so `co_filename` và `tb_lineno`) làm 4/8 dòng
`B2-parse` chết vô can khi chạy như runner thật chạy (bảng 9 dòng 5): HINT đúng ở ý, sai ở phép so.

| slug lớp | hạng | chỗ sửa trong r7 |
|---|---|---|
| `ma-tran-loi-thieu-chot` | P2 | Đóng THEO KHÔNG GIAN của MỌI ĐƯỜNG, không chỉ ba chỗ được chỉ. (1) §7 B2 thêm **bảng không gian mở rộng**: năm tầng (H, Đ0, K0, Đ, K — Đ0 và K0 là hai nhánh sẵn có của Q-A.3) × sáu hàng (R0 "không lỗi" + R1–R5) = **30 ô**; ba trục vuông góc: đếm (C: hỏi/đọc/kill × sáu đường, **13** hạng mục), cú pháp phép tách (S: **2**), nơi gọi (N: năm nơi gọi); hướng thứ ba `thay thế` cho mọi thành viên "phải thoát nguyên" (**19**). Tổng **129** hạng mục (95 thoát/sai/bắt/bọc + 19 thay thế + 13 đếm + 2 cú pháp). Bảng r6 (15 ô) bỏ sót nhánh cũ; §9 ghi rõ. (2) `B2-nhanh-cu` từ 5 thành **19 tiểu nhãn** (10 ở cột Đ0, 9 ở cột K0). (3) Quy ước đếm viết lại theo ĐƯỜNG (hỏi ĐÚNG 1; đọc ĐÚNG 1 trên Đ và Đ0, 0 trên K0; kill ĐÚNG 1 trên K và K0, 0 trên Đ0), observer `os.kill(pid, 0)` đặt ở mọi đầu vào đi qua K hoặc K0 và ở các đầu vào Đ0. (4) `B3-zombie` thêm một lời gọi đường cũ (ô S-Đ0 và R0-Đ0). (5) B5 thêm **phép (E)**: mỗi hạng mục không có dòng `DOT_BIEN` có MỘT biến thể trong tập lệnh bằng chứng cục bộ — KHÔNG vào `DOT_BIEN`, vì sàn đột biến Windows (B4). Số `DOT_BIEN` giữ **54** như HINT (13 lớp, 55 cặp, 228 / 231). Các tổng đổi so với HINT: tiểu nhãn 32 → **46**; đơn vị assertion 41 → **55**; control của D 49 → **63** (17 mức nhãn + 46 mức tiểu nhãn); phép đảo thứ tự 5 → **6**; nhãn **17** và ca đăng ký **191** không đổi |
| `b2-parse-nhan-dien-theo-gia-tri` | P2 | Thêm điều kiện NGUỒN như HINT, nhưng **so bằng HÀM và NỘI DUNG dòng nguồn, KHÔNG bằng tệp và số dòng**: runner `--dot-bien` nạp mỗi bản đột biến từ một tệp tạm riêng (`launcher_db_NN.py`), nên `co_filename` không bao giờ bằng tệp executor khai; và đột biến chèn dòng làm trôi số dòng ((l16) chèn một dòng trước biểu thức tách). Đo (bảng 9 dòng 5): so tệp + dòng ⇒ 4/8 dòng `B2-parse` ((l15), (l16), (l17), (l21)) và hai biến thể Đ0 chết vô can; chỉ so số dòng ⇒ (l16) chết vô can; so hàm + nội dung ⇒ 8/8, cả hai biến thể Đ0 đúng, biến thể tín dụng giả của lượt 6 bị loại. Rà mọi chỗ dùng luật này: quy ước chung loại (4), định nghĩa "nới nhãn", `B2-parse`, `B2-pid-du-phong`, `B2-nhanh-cu` (hai đầu vào tự nhiên mới `p1`, `p3` ở cột Đ0), B5 (đối chứng thứ ba), §10 |
| `so-lieu-noi-bo-lech` | P3 | Bốn chỗ, như HINT, cộng rà mọi nơi nhắc lại: (1) `_con_song` 44 dòng (629–672) ở §9; (2) chữ ký / bộ tương đương: nói rõ (g1) phụ thuộc cách cài, và ghi số r7 đo trên rig riêng (40 chữ ký, 13 bộ / 27 đột biến; bộ khác bộ của reviewer vì quy ước đếm r7 và cột K0, bảng 9 dòng 8); (3) `B3-da-wait`: (l22) chết vô can ở đó — ở r7, A2 của (l22) chết ĐÚNG lý do ở `B2-nhanh-cu vang-da-wait` (observer K0), còn `B3-da-wait` vẫn không có dòng giết riêng; (4) bộ đếm dãy: đính chính sau bảng 8 (HINT) và sửa câu "tối đa ba mệnh đề" ở §9 mục 6 |
| `san-dot-bien-windows` | P3 | B4 khai phép tính sàn 70 % như HINT, đo lại trên rig r7 (65/231 không đo được, 71,86 %, trần 69 ⇒ biên 4 — cận dưới tĩnh), cộng bảng "thêm n dòng Linux-only thì còn biên bao nhiêu": dòng thứ bảy ⇒ `DUOI SAN`; đó là lý do phép (E) không vào `DOT_BIEN`. Closure `land_obligations` và B6 nói rõ `DUOI SAN` ở lượt push master là đỏ của packet. Số thật trên Windows: KHÔNG ĐO ĐƯỢC trước merge (Q4) |
| (r7 tự thêm, ngoài HINT) | — | (1) §1 bảng 9 (số đo của phiên soạn r7 trên rig riêng, ba Python). (2) Đo lại nền nghiệm thu: master trôi 22 commit tới `c16bec6`, write set vẫn rc=0 (§8). (3) §9 mục 7 ghi lần thứ bảy, kể cả việc chính HINT để lọt 34 biến thể. (4) Trục N: hai nơi gọi `:1020`, `:1039` không có đầu vào — KHÔNG ĐO ĐƯỢC ở packet này (§10) |

**Lịch sử r5 → r6** (mỗi dòng ứng với một lớp của VERDICT lượt 5, hồ sơ cross-review PR #688; slug là tên
lớp trong bảng lớp của VERDICT; các số trong bảng này là số của r6 — từ r7 là số LỊCH SỬ, tổng hiện hành ở B2,
B5, §8 — còn các bảng lịch sử bên dưới giữ số của revision cũ). r6 áp `HINT.patch` của lượt 5 (24 hunk, 19708 byte, sha256 `93b187e2…3531`) lên bản sao r5.
HINT nhắm r5 nên đường dẫn phải đổi trước khi áp, và **chỉ đổi hai dòng tiêu đề của patch**
(`sed '1,6s#launcher-con-song-esrch-r5.md#launcher-con-song-esrch-r6.md#'`), không đổi thân, như r5 đã làm với
HINT lượt 4. Đo 17:04:02Z 29-09 trên một bản sao r5 riêng: `patch -p0 --fuzz=0` ⇒ **rc=0**, không tệp `.orig` hay
`.rej`, 1122 dòng, sha256 bản chỉ-HINT `74d74d64e79b090fd29e3f53bab3b44a7549f2b6cc88be7a41d006ef5ad6301e` (`74d74d64…301e`;
trùng byte với `SPEC-proposed.md` trong hồ sơ lượt 5); `sed` toàn cục cho cùng rc=0 lần này, vì HINT lượt 5 không
có dòng ngữ cảnh nào nhắc tên tệp. Lệnh áp lúc soạn cũng rc=0.

**Vì sao r6 KHÔNG dừng ở HINT.** HINT lượt 5 đúng về ô nó chỉ (đo lại được: bản gộp `OSError`, `ValueError`,
`IndexError` ở phép hỏi chết ở `hoi-index`, bảng 8 dòng 9) và cũng có răng ở chỗ nó phủ. Nhưng đó là lần thứ
sáu cùng một hình dạng — thêm đúng ô vừa bị chỉ (một tiểu nhãn `hoi-parse`, một dòng (h3)) — trong khi lớp
`ma-tran-loi-thieu-chot` đã mở qua năm lượt liên tiếp, lần nào cũng lộ ô kế bên. CLAUDE.md nêu cách chữa cho
hình dạng này: *đừng vá theo danh sách reviewer liệt kê; tự liệt kê hết đường TRƯỚC, đóng cả loạt, cho mỗi đường
một chốt riêng*. r6 áp HINT (để giữ dấu vết và bảo toàn phần đúng), rồi làm việc chính: dựng bảng không gian
phạm vi bắt ngoại lệ (B2), tìm ô nào thiếu đầu vào hoặc đột biến, đóng hết một lượt, và ĐO cả không gian bằng
một bộ sinh (bảng 8). Bộ đếm hình dạng ở §9 ghi lần thứ sáu và ghi cách làm mới.

| slug lớp | hạng | chỗ sửa trong r6 |
|---|---|---|
| `ma-tran-loi-thieu-chot` | P2 | Đóng THEO KHÔNG GIAN chứ không theo finding. (1) §7 B2 thay "ma trận tầng × miền" bằng **bảng không gian phạm vi bắt ngoại lệ**: 5 hàng (`ProcessLookupError`; `OSError` khác; nhóm phân tích; `Exception` khác; `BaseException`) × 3 tầng (hỏi, đọc, kill) = **15 ô**, 42 hạng mục (thành viên × hướng sai), mỗi ô ghi Q-A yêu cầu gì, đầu vào nào, đột biến nào vi phạm riêng ô; ô hay phần ô bất khả thi hoặc KHÔNG ĐO ĐƯỢC được liệt kê kèm lý do và phép đo (`Path.exists()` nuốt `ValueError` của `stat`: bảng 7). (2) Đầu vào mới: nhãn `B2-eperm-hoi`; tiểu nhãn `EPERM` của `B2-doc-hong`; tiểu nhãn `kill` của `B2-tin-hieu` và `B2-exception`; nhãn `B2-thoat-parse` (6 đầu vào, seam ở `Path.exists` cho tầng hỏi) thay tiểu nhãn `B2-exception hoi-parse` của HINT — vì nhóm phân tích có ba thành viên và ba tầng. (3) Quy ước chung: ngoại lệ được ghi nhận có bốn loại (seam; ngoại lệ THẬT do observer `kill` ghi lại; chuỗi `__cause__`; ngoại lệ tự nhiên của phép tách ở `B2-parse`), thay quy tắc "chỉ đối tượng do seam tạo ra" và lệnh cấm đổi mọi ngoại lệ ở `B2-parse`. (4) B5: (h) trở lại hai dòng; (k) thêm (k5); lớp (l) mới với 29 dòng ⇒ **mười hai LỚP**. Các tổng đổi: mục `DOT_BIEN` 19 → **49**; cặp (dòng, ca đích) 20 → **50**; bảng sản phẩm 193 → **223**, kèm harness 196 → **226**; nhãn 14 → **16**; đơn vị assertion 26 → **36**; control của D 32 → **43** (14 → 16 mức nhãn, 18 → 27 mức tiểu nhãn); số ca đăng ký **191** không đổi. (5) §3 Q-A.4/.5 viết tường minh, không đổi ngữ nghĩa: "OSError khác" là lớp chứ không danh sách errno; phạm vi bắt của bước kill; phép kiểm dữ liệu phải nhận ra mọi dạng nội dung hỏng. (6) §1 thêm bảng 7 và bảng 8; §8, §9, §10 cập nhật cùng lúc |
| `chot-nguoc-khong-co-lap` | P2 (ĐÃ ĐÓNG ở lượt 4 và 5) | Không đổi ngữ nghĩa phép D và A1/A2/W1/W0. Cập nhật số hạng (36 đơn vị, 43 control) và thêm LOẠI assertion vào điều kiện khớp A1/W1 và vào log: hai hướng của cùng một thành viên dùng chung một tiểu nhãn (11 bộ tương đương theo tiểu nhãn, bảng 8 dòng 8), nên loại là thứ duy nhất tách chúng |
| (r6 tự thêm, ngoài HINT) | — | (1) Tầng thứ ba K (bước `kill`), ngoài hai tầng Q-A.5 nêu. (2) Đổi luật `B2-parse` để ba hướng "thoát" của hàng nhóm phân tích × tầng đọc có đột biến chết đúng lý do, kèm đối chứng vô can (bảng 8 dòng 6). (3) Đầu vào và đột biến EPERM ở tầng hỏi và tầng đọc; đột biến "bản vá tối thiểu chỉ bắt `ProcessLookupError`" (l1). (4) Bộ sinh và phép đo đóng (bảng 8 dòng 10–12); nó tìm ra một lỗ (bọc lại `ValueError` tự nhiên) mà danh sách viết tay bỏ sót. (5) Bỏ khối "Bổ sung sau cross-review lượt 5" mà HINT thêm vào: nó lặp các số HINT (20 mục, 21 cặp, 194/197, 33 control) ở chỗ thứ hai, và số hiện hành nay chỉ nằm ở B2, B5, §8 và bảng này. (6) Đo lại nền và ruff (§8) |

**Lịch sử r4 → r5** (mỗi dòng ứng với một lớp của VERDICT lượt 4, hồ sơ cross-review PR #688; slug là
tên lớp trong bảng lớp của VERDICT; các số trong bảng này là số khi r5 đóng băng, KHÔNG phải tổng nghiệm thu
của r6; tổng hiện hành nằm ở §7 và §8). r5 áp `HINT.patch` của lượt 4 (13 hunk, 21599 byte, sha256 `59964a4a…c0aa`) lên bản
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
đổi Q-A.1–4; r4, r5, r6 và r7 cũng không), KHÔNG phải revision đặc tả r2. Bản nháp không nằm trong đặc tả này, không phải bản vá
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

**Bảng 7 — `Path.exists()` nuốt những ngoại lệ nào của `stat` (r6 thêm; số của cross-review lượt 5 và số phiên
soạn r6 tự đo lại)**

Reviewer lượt 5 đo `ValueError` ở seam `Path.stat` (`07-boundary.log`, 15:56:32Z–15:57:47Z 29-09): bản đúng cũng
trả về bình thường, nên không dùng được làm chốt. Phiên soạn r6 đo lại độc lập (16:20:07Z 29-09, ba bản Python
3.11.15, 3.12.3, 3.13.12 — cùng kết quả cả ba). Probe: vá đúng một hàm của `pathlib.Path`, chỉ cho đúng đường
`/proc/<pid>/stat` của tiến trình probe, ném MỘT đối tượng dựng sẵn; gọi `Path.exists()` trên đường ấy; so danh
tính đối tượng thoát ra. Bộ đếm lần chạm seam bằng 1 ở cả mười ô.

| ngoại lệ do seam ném | seam đặt ở `Path.stat` | seam đặt ở `Path.exists` |
|---|---|---|
| `ValueError` | `exists()` trả `False`, không ném (**bị nuốt**) | thoát, đúng đối tượng ấy |
| `UnicodeDecodeError` | `exists()` trả `False`, không ném (**bị nuốt**) | thoát, đúng đối tượng ấy |
| `IndexError` | thoát, đúng đối tượng ấy | thoát, đúng đối tượng ấy |
| `RuntimeError` | thoát, đúng đối tượng ấy | thoát, đúng đối tượng ấy |
| `KeyboardInterrupt` | thoát, đúng đối tượng ấy | thoát, đúng đối tượng ấy |

Hệ quả cho bảng không gian (§7 B2): ô "nhóm phân tích × tầng hỏi" đặt seam ở `Path.stat` chỉ đo được
`IndexError`; `ValueError` và `UnicodeDecodeError` ở seam ấy là **bất khả thi** (thư viện nuốt trước khi ngoại lệ
tới mã launcher, đo ba Python), nên ba đầu vào của ô đặt seam ở `Path.exists` — hàm mà nền thực sự gọi. Việc đặt
seam ở đó buộc ứng viên hỏi bằng `exists()`; ứng viên hỏi bằng lời gọi khác thì seam không chạm và ca ném lỗi
thường (quy ước chung ở §7), không tính là ĐẠT.

**Bảng 8 — số đo của phiên soạn r6 trên rig prototype (r6 thêm; KHÔNG phải ứng viên của executor)**

Rig r6: bản sao `.claude/dev/` của `89fc4fa` (blob `561ff7a1…`, `abf7f6ca…`), cộng ứng viên prototype của phiên
soạn dựng theo Q-A (phép hỏi `exists()` bắt `ProcessLookupError` ⇒ `False`, bắt `OSError` ⇒ bước đọc; khối đọc bắt
`OSError`, `ValueError`, `IndexError` ⇒ rơi về khối kill của nền; mã của nó không nằm trong đặc tả, protocol §8), cộng
helper mở rộng 16 nhãn / 36 đơn vị chèn vào bản sao `launcher_test.py`, cộng 49 tệp đột biến dựng từ ứng viên bằng
thay chuỗi. Python 3.12.3 nếu không ghi khác; `PYTHONDONTWRITEBYTECODE=1`; con của rig session riêng, dọn bằng PID
tường minh. Giờ UTC 29-09-2026.

| # | phép đo | kết quả | giờ UTC |
|---|---|---|---|
| 1 | bản đúng, `t156` và `t157` | PASS, PASS ở cả ba Python | 16:46:35Z (3.12.3); 16:48:58Z (3.11.15); 16:50:49Z (3.13.12) |
| 2 | A1/A2/W1/W0 cho 49 dòng, 50 cặp (dòng, ca đích) | **50/50 được chấp nhận** ở cả ba Python: A1 chết bằng `TinHieuChotCa` đúng nhãn (hoặc nhãn đứng trước), đúng tiểu nhãn, đúng loại assertion; W1 chết đúng nhãn, tiểu nhãn, loại; W0 sống sót với bộ đếm seam ≥ 1 | như dòng 1 |
| 3 | phép D | bản đúng xanh ở cả hai ca; **43 control** (16 mức nhãn + 27 mức tiểu nhãn) đều đỏ, mỗi cái báo đúng đơn vị thiếu; 5 phép đảo thứ tự đều đỏ (`missing=[]`, `order=False`); 36 đơn vị | 16:46:53Z; 16:49:13Z; 16:51:06Z |
| 4 | kiểm kê | 191 ca đăng ký; `DOT_BIEN` 174 + 49 = **223**; harness 3; tổng **226** | 16:46:55Z |
| 5 | runner thật `chay_dot_bien` trên 49 bản ghi | 48 dòng `giet 1/1`, 1 dòng `giet 2/2` (c); kết quả `(0, 0)`; không dòng nào in kiểu ngoại lệ trong ngoặc; đối chứng `NameError` chết bằng `NameError`, runner vẫn in `OK giet 1/1: …(NameError)` | 16:46:55Z; lặp 16:49:15Z, 16:51:09Z |
| 6 | đối chứng cho quy tắc nhận ra ngoại lệ tự nhiên (`ctrl`) | bản phân tích hỏng ném `ValueError` khác đối số ngay sau khi đọc chết bằng `ValueError` vô can, không thành `TinHieuChotCa`. Bản đầu của quy tắc chuỗi ngoại lệ tính cả `__context__`: CÙNG bản hỏng ấy chết bằng `TinHieuChotCa:B2-eacces seam wrapped ValueError` — tín dụng giả; đã bỏ `__context__` | 16:47:02Z; bản đầu 16:26:50Z |
| 7 | bảng không gian ↔ log A/W (tập lệnh đối chiếu) | 15 ô; 42 hạng mục (T1 14, T2 17, T3 11); cả 42 có ít nhất một đột biến với W1 đúng đơn vị và đúng loại; 43 dòng B5 trong bảng, 6 ngoài (c, f, j1, j2, k1, k5); 0 hạng mục sai | 16:58:50Z |
| 8 | chữ ký chết khi chạy riêng từng nhãn | 49 đột biến cho **37** chữ ký; **11** bộ tương đương theo tiểu nhãn gồm 23 đột biến, mỗi bộ chỉ là hai (một bộ ba) HƯỚNG của cùng một thành viên, thông điệp khác loại assertion. Đơn vị không có dòng B5 nào lấy làm đích: `B2-dem-doc 2`, `B3-song`, `B3-da-wait`; trong đó `B3-song` là đơn vị duy nhất không đột biến nào chết khi chạy riêng nhãn | 16:47Z |
| 9 | bản HINT (h3) (`OSError`, `ValueError`, `IndexError` ở phép hỏi) trên helper r6 | A1 và W1 chết ở `B2-thoat-parse hoi-index`, loại `sentinel identity` — cùng chỗ với (l6) | 16:58:16Z |
| 10 | bộ sinh: mọi dãy ≤ 3 mệnh đề trên tám lớp × năm hành động; Python 3.12.3 | tầng H sinh **43 440** dãy, 20 tương đương bản đúng, **2 803** chữ ký khác; tầng Đ sinh 43 440, 48 tương đương, 2 803 chữ ký; tầng K sinh 22 433, 7 tương đương, 2 804 chữ ký. **Mọi chữ ký chết bằng `TinHieuChotCa`, 0 lỗ, và chết đúng ở đơn vị sớm nhất mà đầu vào chữ ký ấy chạm (0 lệch)** | 16:53:04Z–17:00:19Z |
| 11 | bộ sinh dãy ≤ 2 mệnh đề, ba Python | tầng H 1 440 dãy / 415 chữ ký; tầng Đ 1 440 / 416; tầng K 929 / 416; 0 lỗ, 0 lệch ở cả ba Python. LẦN ĐẦU (trước khi sửa quy tắc, 3.12.3): 1 lỗ ở tầng Đ — bọc lại `ValueError` tự nhiên thành `RuntimeError` mới, chết vô can; đã đóng bằng quy tắc `B2-parse` có xét `__cause__` và dòng (l21) | 16:47:37Z; 16:49:48Z; 16:51:48Z; lỗ: 16:35:27Z |
| 12 | bộ sinh ánh xạ errno (bốn errno 13, 1, 5, 3, mỗi errno một hành động, cộng mặc định); ba Python | tầng H 3 125 ánh xạ / 255 chữ ký; tầng Đ 3 125 / 255; tầng K 1 024 / 63; 0 lỗ, 0 lệch ở cả ba Python | 16:48:29Z; 16:50:26Z; 16:52:36Z |

"Chữ ký" ở dòng 8, 10, 11, 12 là bộ kết quả của một đoạn mã trên 8–10 đầu vào tầng ấy (`False`, `True`, thoát kèm
kiểu, thoát đúng đối tượng hay khác), không phải tên đột biến. Bộ sinh chỉ phủ dãy mệnh đề trong ngữ pháp của nó
(tám lớp `ProcessLookupError`, `PermissionError`, `OSError`, `ValueError`, `UnicodeDecodeError`, `IndexError`,
`Exception`, `BaseException`; hành động rơi về bước sau, `False`, `True`, bọc lại bằng `raise … from …`, trả `None`,
và ở dạng errno cả thoát nguyên; ở tầng K không có "rơi về bước sau"). Các giới hạn còn lại nằm ở §10.

**Đính chính bảng 8 (r7, cross-review lượt 6; bảng giữ nguyên số r6 đã ghi).** Dòng 8: `B3-da-wait` cũng không có
đột biến nào chết bằng `TinHieuChotCa` khi chạy riêng nhãn ((l22) chết vô can ở đó), nên `B3-song` KHÔNG phải
đơn vị duy nhất; và 37 chữ ký / 11 bộ / 23 đột biến chỉ tái lập được khi (g1) đổi CẢ nhóm phân tích sang `False` —
(g1) chỉ đổi mệnh đề `OSError` (đúng ánh xạ "R2-Đ EACCES sai" của bảng không gian) cho 36 / 12 / 25, bộ thêm là
(g1, l10). Dòng 10–11: số dãy tầng H và Đ KHÔNG gồm dãy rỗng (43 440 = 40 + 1 400 + 42 000; 1 440 = 40 + 1 400),
còn tầng K GỒM dãy rỗng (22 433 = 1 + 32 + 896 + 21 504; 929 = 1 + 32 + 896): "mọi dãy ≤ 3 mệnh đề" đúng cho K,
lệch 1 cho H và Đ (bộ sinh không nằm trong kho, nên chỉ kiểm được số học, không kiểm được chữ ký: KHÔNG ĐO ĐƯỢC).

**Bảng 9 — số đo của phiên soạn r7 trên rig riêng (r7 thêm; KHÔNG phải ứng viên của executor)**

Rig r7: thư mục tạo bằng `mktemp -d` trong scratchpad của phiên soạn, ngoài kho. Gồm: bản sao `.claude/dev/` của
`89fc4fa` lấy bằng `git archive` (blob `561ff7a1…`, `abf7f6ca…`, đo bằng `git hash-object`); ứng viên nháp dựng theo Q-A
— **trùng từng byte** với ứng viên nháp của cross-review lượt 6 (`cmp`), vì cùng một thay chuỗi trên nền, và mã của nó
không nằm trong đặc tả (protocol §8); 54 tệp đột biến (49 dòng r6 chép nguyên danh sách thay chuỗi của reviewer lượt 6,
cộng 5 dòng (m)); helper r7 do phiên soạn viết theo lời văn §7 của r7 (17 nhãn, 55 đơn vị, luật nguồn có công tắc để
so bốn cách hiểu), chèn vào bản sao `launcher_test.py`; 89 biến thể của phép (E) (B5), mỗi cái MỘT thay chuỗi trên ứng
viên. `PYTHONDONTWRITEBYTECODE=1`; con của rig session riêng, dọn bằng PID tường minh. Python 3.12.3 nếu không ghi khác;
giờ UTC 30-09-2026. Dòng 1–13 là số trên rig, không phải trên mã của executor.

| # | phép đo | kết quả | giờ UTC |
|---|---|---|---|
| 1 | bản đúng và nền, `t156`/`t157` | ứng viên: SONG, SONG (0,36 giây / 0,34 giây); nền `89fc4fa`: `t156` đỏ `TinHieuChotCa:B1 seam escaped`, `t157` đỏ `B3b-giet-cay seam escaped` | 01:33:20Z |
| 2 | A1/A2/W1/W0 cho 54 dòng, 55 cặp (dòng, ca đích), luật nguồn "hàm + nội dung" | **55/55 được chấp nhận** ở cả ba Python. A1 của năm dòng báo ở một nhãn đứng TRƯỚC nhãn đích (hợp lệ theo A1) vì quy ước đếm r7: (c) và (j1) ở `B2-eacces` loại `read count`; (j2), (k1), (k5) ở `B2-doc-hong EACCES` (`read count` / `kill count`). A2 của (l22), (l23), (l24), (l27), (l28), (l29) chết ĐÚNG lý do ở các tiểu nhãn `vang-*` của `B2-nhanh-cu` (khối kill dùng chung) | 01:33:28Z (3.12.3); 01:41:40Z (3.11.15); 01:43:18Z (3.13.12) |
| 3 | phép D | bản đúng xanh ở cả hai ca (`t156` 54 đơn vị, `t157` 1); **63 control** (17 mức nhãn + 46 mức tiểu nhãn) đều đỏ, mỗi cái báo đúng đơn vị thiếu; **6** phép đảo thứ tự (năm của r6 cộng `B2-pid-du-phong` với `B2-nhanh-cu`) đều đỏ với `missing=[]`, `order=False` | như dòng 2 |
| 4 | kiểm kê | 191 ca đăng ký; `DOT_BIEN` 174 + 54 = **228**; harness 3; tổng **231**; 17 nhãn; 46 tiểu nhãn; 55 đơn vị | như dòng 2 |
| 5 | luật nguồn của `B2-parse`, bốn cách hiểu, trên (i), (l15)–(l21) và hai biến thể Đ0 thoát (`p1`, `p3`) cùng hai đối chứng | "không xét nguồn" (r6): 8/8 dòng nhận, nhưng biến thể tín dụng giả của lượt 6 được ghi `B2-parse p1 parse error escaped` — tín dụng giả; "tệp + số dòng" (chữ HINT): (l15), (l16), (l17), (l21) và hai biến thể Đ0 chết VÔ CAN (4/8 dòng nhận) vì `co_filename` là tệp đột biến; "chỉ số dòng": (l16) chết vô can (7/8) vì nó chèn một dòng trước biểu thức tách; **"hàm + nội dung dòng" (r7): 8/8, hai biến thể Đ0 đúng, biến thể tín dụng giả chết vô can, đối chứng khác đối số chết vô can** | 01:37Z–01:38:21Z |
| 6 | phép (E): 89 biến thể (50 thoát/sai/bắt/bọc, 19 thay thế, 8 đếm, 1 cú pháp, 7 bản vá sai của lượt 6, 4 đối chứng) | **87/87** biến thể đúng kỳ vọng: mỗi biến thể "TH" chết bằng `TinHieuChotCa` đúng nhãn, tiểu nhãn và loại ở cả A1 (hoặc nhãn đứng trước) lẫn W1, W0 sống với bộ đếm ≥ 1; mỗi biến thể "thay thế" làm ca ĐỎ bằng `RuntimeError` vô can ở A1, W1 và cả W0 (nới nhãn không che được); hai đối chứng kỳ vọng SONG (khối K0 tách riêng mà đúng ngữ nghĩa; danh sách trắng ba errno — giới hạn đã khai) sống, D xanh | 01:46Z–01:46:47Z (3.12.3, đủ 89); 3.11.15 và 3.13.12: 84 biến thể lúc 01:42:48Z–01:43:18Z và 01:44:30Z–01:45:05Z, ba biến thể đếm thêm sau lúc 01:46:03Z–01:46:04Z, cùng kết quả |
| 7 | 89 biến thể của (E) trên một helper dựng ĐÚNG theo HINT (bản sao `helper_block_r7.py` của reviewer lượt 6, ca đầy đủ `t156` + `t157`) | **36/89 lọt** (cả hai ca SONG): hai đối chứng SONG cộng **34 biến thể trái Q-A** — cột Đ0: ESRCH, EIO, EPERM (thoát, sai), `IndexError` và `UnicodeDecodeError` (thoát, sai), Z đọc được ⇒ `True`, gọi kill trên Đ0, tách theo `)` đầu ở Đ0 (13); cột K0: EPERM, EIO (thoát, sai), đọc thêm trên K0, và cả 15 hạng mục bắt/bọc/thay thế của R3–R5 (20); gọi kill lần hai chỉ khi đọc gặp EPERM (1). Thêm hai biến thể mà helper HINT chỉ bắt bằng lỗi vô can (tín dụng giả nếu là đột biến): Đ0 `ValueError` thoát, K0 ESRCH thoát | 01:46:48Z–01:47:35Z |
| 8 | chữ ký chết khi chạy riêng từng nhãn, 54 dòng | **40** chữ ký; **13** bộ tương đương theo tiểu nhãn gồm **27** đột biến: (c, l1), (d1, l3), (d2, l14), (g1, l10), (g2, l11), (h1, l9), (i, l15, l21), (j2, k1), (l12, l13), (l17, l18), (l19, l20), (l2, m4), (l4, l5). Đơn vị không có dòng `DOT_BIEN` nào giết bằng `TinHieuChotCa` khi chạy riêng nhãn: **9** — `B2-nhanh-cu` `EIO`, `ESRCH`, `EPERM`, `p1`, `p3`, `p4`, `exception`, và `B3-song`, `B3-da-wait`; (l22) chết vô can ở `B3-da-wait` | 01:39:52Z |
| 9 | runner thật `chay_dot_bien` trên 54 bản ghi + đối chứng `NameError` | 53 dòng `giet 1/1`, (c) `giet 2/2`; kết quả `(0, 0)`; không dòng R7 nào in kiểu ngoại lệ trong ngoặc; đối chứng in `OK giet 1/1: t156_…(NameError)` | 01:41:11Z |
| 10 | sàn đột biến Windows, ước lượng TĨNH (cận dưới), tập lệnh của reviewer lượt 6 chạy trên tệp test đã lắp của rig r7 | nền 11/177 không đo được (93,79 %, trần 53); r7 **65/231** (71,86 %, trần 69 ⇒ **biên 4**). Thêm n dòng Linux-only: n = 1…6 vẫn đạt (biên 3, 2, 2, 1, 0, 0); **n = 7 ⇒ `DUOI SAN`** (0,6975) | 01:41:30Z |
| 11 | bảy bản vá sai của cross-review lượt 6 (chuỗi thay chép nguyên), trong (E) | cả bảy chết bằng `TinHieuChotCa` đúng đích ở A1 và W1, W0 sống: hợp nhất về kill ⇒ `B2-nhanh-cu EACCES result`; nhánh cũ bắt `BaseException` ⇒ `tin-hieu sentinel identity`; tệp vắng ⇒ `False` ⇒ `vang result`; hỏi lại khi ESRCH ⇒ `B1 stat count`; hỏi lại khi `OSError` khác EACCES ⇒ `B2-eio stat count`; đọc lại khi EPERM ⇒ `B2-doc-hong EPERM read count`; tách theo `)` đầu ⇒ `B3-zombie result` | như dòng 6 |
| 12 | đối chứng của luật `B2-parse` | biến thể tín dụng giả của lượt 6 (bắt đúng `ValueError` rồi gọi `str.index` độc lập) ⇒ `ValueError: substring not found` VÔ CAN ở A1, W1, W0; đối chứng khác đối số ⇒ `ValueError: khac doi so` vô can | như dòng 6 |
| 13 | B6 — toàn suite `python .claude/dev/launcher_test.py --nhat-ky …`, ba vế trong MỘT vòng lặp (mỗi vế: clone sạch từ worktree, checkout `82d05eb`, `core.abbrev` 7, chép tệp của vế, chạy), tuần tự | nền: `187/188 ca DA CHAY QUA (tong 189, bo qua 1, hong 1)`, rc=1; ứng viên + helper r7: `189/190 ca DA CHAY QUA (tong 191, bo qua 1, hong 1)`, rc=1; hỏng duy nhất ở cả hai vế là `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` (đỏ sẵn ở nền, cùng ca reviewer lượt 6 ghi) ⇒ **delta 0**; vế (m1) — bản hợp nhất về kill mà lượt 6 đo qua 189/190 — nay `188/190 … hong 2`, thêm đúng `t156_r7_…: B2-nhanh-cu EACCES result True` | nền 01:48:42Z; ứng viên 01:50:22Z; (m1) 01:52:02Z |

"Chữ ký" ở dòng 8 theo định nghĩa của bảng 8. Số bộ ở dòng 8 là số ĐO trên một cách cài (ứng viên nháp và helper
r7), không suy từ văn bản; (g1) ở rig r7 là cách cài "chỉ đổi mệnh đề `OSError`" (bộ (g1, l10)).

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
  **r6 cũng KHÔNG đổi ngữ nghĩa Q-A.1–6**, chỉ viết tường minh ba điều Q-A.4 và Q-A.5 đã hàm ý (phạm vi bắt
  của phép hỏi với nhóm phân tích; phạm vi bắt của bước `kill(pid, 0)`; "OSError khác" là LỚP chứ không phải
  danh sách errno) theo lượt 5 — ngay dưới hai bước ấy;
  **r7 cũng KHÔNG đổi ngữ nghĩa Q-A.1–6**, chỉ nói rõ theo lượt 6 rằng "nguyên xi" ở Q-A.3 gồm cả số lần (nhánh
  tệp có đọc đúng một lần và không gọi `kill`; nhánh tệp vắng gọi `kill(pid, 0)` đúng một lần và không đọc) và
  rằng Q-A.3 có đầu vào riêng (ngay dưới bước 3);
  chủ kho có thể bác bằng revision mới. Hợp đồng, bằng lời:
  1. Phép hỏi `stat`/`exists` trên `/proc/<pid>/stat` được thực hiện **đúng một lần** mỗi lời gọi
     `_con_song`, và không thử lại.
  2. `ProcessLookupError` ở phép hỏi ấy ⇒ trả `False` (tiến trình đã biến mất).
  3. Phép hỏi không ném lỗi ⇒ hai nhánh sẵn có giữ **nguyên xi**: tệp có ⇒ đọc trạng thái (kể cả
     hành vi cũ ở §2 khi đọc lỗi); tệp vắng ⇒ rơi về `os.kill(pid, 0)` như cũ. **(r7, cross-review lượt 6,
     không đổi ngữ nghĩa)** Điều khoản này nay có đầu vào riêng — nhãn `B2-nhanh-cu` ở §7: r6 không có đầu vào
     nào đi vào hai nhánh sẵn có với đọc lỗi/nội dung hỏng, hay với tệp vắng trên PID sống, nên bản vá đổi
     chúng qua hết nghiệm thu (đo được, xem `B2-nhanh-cu`). "Nguyên xi" gồm cả kết quả, phạm vi bắt và SỐ LẦN,
     đúng như mã nền `launcher.py:651–664` trên `89fc4fa`: nhánh tệp có đọc đúng một lần, không gọi `kill`, và bắt
     đúng ba nhóm `OSError`, `ValueError`, `IndexError` (⇒ `False`; ngoại lệ khác thoát nguyên); nhánh tệp vắng
     gọi `kill(pid, 0)` đúng một lần với ngữ nghĩa sẵn có của Q-A.4 (i), không đọc nội dung, và không thêm mệnh
     đề bắt nào (nhóm phân tích, `Exception`, `BaseException` ở đó thoát nguyên — cùng khối mã với tầng K).
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
     **Làm rõ (r6, không đổi ngữ nghĩa):** (i) "`OSError` khác (EACCES, EIO, …)" là một LỚP ngoại lệ, không phải
     danh sách trắng errno: mọi `OSError` không phải `ProcessLookupError` ở phép hỏi đều đi vào bước đọc, dù
     mang errno nào (kể cả EPERM); bản vá phân nhánh theo errno, hoặc chỉ nhận một tập errno hữu hạn, là vi
     phạm; (ii) đường lỗi mới KHÔNG được thêm mệnh đề bắt nào ở bước `kill(pid, 0)` ngoài ba mệnh đề của khối
     nền (`ProcessLookupError`, `PermissionError`, `OSError`); ngoại lệ ngoài họ `OSError` do bước này ném
     ra (nhóm phân tích, `Exception` khác, `BaseException` khác) thoát nguyên đối tượng, không bị bắt và không
     bị bọc lại thành đối tượng khác (`raise … from …`).
  5. Phạm vi bắt, **theo từng tầng** (r3 viết lại cho rõ theo lớp `ma-tran-loi-thieu-chot`; r2 chỉ nói
     "họ `OSError`" và để hở chỗ nội dung hỏng ở bước 4). Từ r6 có **ba tầng** (H, Đ, K) của đường mới; từ r7
     bảng không gian mở rộng ở §7 B2 thêm hai tầng Đ0, K0 của hai nhánh sẵn có (Q-A.3) và liệt kê từng ô của cả năm;
     câu chữ dưới đây là hợp đồng, bảng là danh sách kiểm:
     · **Tầng hỏi** (H; `stat`/`exists`): chỉ bắt họ `OSError`. Mọi ngoại lệ khác thoát ra nguyên đối
       tượng — cả ngoại lệ thuộc `Exception` nhưng không thuộc `OSError` (ví dụ `RuntimeError`) lẫn
       ngoại lệ thuộc `BaseException` nhưng không thuộc `Exception` (ví dụ `KeyboardInterrupt`), và cả
       nhóm lỗi phân tích (`ValueError`, `UnicodeDecodeError`, `IndexError`): nhóm này chỉ được bắt cục bộ ở
       tầng đọc và KHÔNG được đưa vào nhóm bắt của phép hỏi (lượt 5 đo được bản làm vậy qua toàn bộ nghiệm
       thu của r5). Ranh giới là ngoại lệ THOÁT KHỎI phép hỏi vào mã launcher: `Path.exists()` tự nuốt
       `ValueError` (kể cả `UnicodeDecodeError`, con của nó) phát sinh bên trong `stat` — đo trên ba bản
       Python (§1 bảng 7) — nên không đòi launcher phục hồi một ngoại lệ thư viện đã nuốt; còn `IndexError` từ
       `stat` thoát qua `exists()` nguyên vẹn, và mọi ngoại lệ ném thẳng từ `exists()` thoát nguyên. Vì vậy
       nhóm phân tích ở tầng hỏi được đo bằng seam đặt ở `Path.exists`, không phải `Path.stat` (B2,
       `B2-thoat-parse`).
     · **Tầng đọc** (Đ; bước 4): bắt `OSError` của phép đọc, và các lỗi **phân tích cục bộ** của nội dung
       đọc được (`ValueError` — kể cả `UnicodeDecodeError`, là con của nó — và `IndexError`); phần bọc
       chỉ gồm đúng phép đọc và biểu thức tách trạng thái, không bọc thêm gì, và tuyệt đối không bọc
       phép hỏi hay bước `kill`. Nhận diện "không phân tích được" bằng kiểm tra dữ liệu thay cho bắt ngoại
       lệ cũng được; Q-A không quy định cách — nhưng kiểm tra dữ liệu phải nhận ra MỌI dạng nội dung hỏng ở
       bảng 4, không chỉ một dạng (bản chỉ nhận ra chuỗi rỗng là vi phạm, B5 dòng (l16)). Ngoại lệ ngoài hai
       nhóm ấy (ví dụ `RuntimeError`, `KeyboardInterrupt`) thoát ra nguyên đối tượng.
     · **Tầng kill** (K; bước `os.kill(pid, 0)` mà đường lỗi rơi vào): chỉ ba mệnh đề của khối nền, với ngữ
       nghĩa ở Q-A.4 (r5 và r6 làm rõ); mọi ngoại lệ khác thoát nguyên đối tượng.
     · Bản vá KHÔNG được dùng `except Exception` hay `except BaseException` ở cả ba tầng, và KHÔNG được bọc lại
       ngoại lệ thoát ra thành đối tượng khác. Ngoại lệ `OSError` thoát ra khỏi đường lỗi mới là vi phạm
       objective.
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

Không đường dẫn nào khác. Đặc tả này (`ops/specs/launcher-con-song-esrch-r7.md`) là hồ sơ của lượt
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
  đọc/nội dung hỏng: cross-review lượt 4 trên PR #688; nguồn việc nhóm phân tích không được bắt ở tầng hỏi và
  việc phạm vi bắt phải đúng ở cả ba tầng hỏi, đọc, kill: cross-review lượt 5 trên PR #688; nguồn việc hai nhánh
  sẵn có phải giữ nguyên xi cả số lần, không hỏi/đọc lại theo lớp ngoại lệ, và tách trạng thái theo dấu `)` cuối:
  cross-review lượt 6 trên PR #688).
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
  của nó phân biệt được với chết ở chốt khác của cùng ca. Tám nhãn gồm nhiều đầu vào có tên — `B2-doc-hong`,
  `B2-tin-hieu`, `B2-exception`, `B2-thoat-parse`, `B2-parse`, `B2-dem-doc`, `B2-pid-du-phong`, `B2-nhanh-cu` (r7) —
  còn mang **tiểu nhãn**
  ngay sau nhãn, cách một dấu cách (bảng tiểu nhãn ở ngay sau bảng không gian B2). Nhãn là đơn vị của thứ tự
  thực thi và của tham số CHẠY/NỚI của helper; tiểu nhãn là đơn vị của phép quan sát D và của điều kiện khớp ở
  B5 (r4).
- Seam stat/read chỉ chạm đúng `/proc/<pid>/stat` của PID đang xét, có **bộ đếm lần chạm**; ca xác nhận seam đã
  chạm ở từng lời gọi (seam không chạm ⇒ ca không đo gì). Lấy khoá danh tính **trước** khi đặt seam. Seam không
  được giao lỗi nào thì chỉ ĐẾM rồi chuyển tiếp thật — đó là cách các đầu vào đường cũ giữ `stat` và phép đọc thật
  mà vẫn đếm được. Observer `os.kill(pid, 0)` (chỉ cặp PID đang xét và tín hiệu 0; ghi lại rồi chuyển tiếp thật,
  hoặc ném lỗi seam; tín hiệu khác hay PID khác chuyển tiếp nguyên vẹn) đặt ở (r7): mọi đầu vào mà đường Q-A đi
  qua bước kill — tầng K (`B2-doc-hong`, `B2-parse`, `B2-dem-doc` tiểu nhãn `3`, `B2-pid-du-phong`, và tiểu nhãn
  `kill`/`kill-*` của `B2-tin-hieu`, `B2-exception`, `B2-thoat-parse`) và tầng K0 (mọi tiểu nhãn `vang*` của
  `B2-nhanh-cu`) — cùng các đầu vào tầng Đ0 (phần tệp có của `B2-nhanh-cu` và lời gọi đường cũ của `B3-zombie`), để
  đếm được con số 0. Ba đầu vào tầng hỏi của `B2-thoat-parse` đặt seam ở `Path.exists` (bảng 7), và
  bộ đếm của chính seam ấy phải ≥ 1 — bằng 0 (ứng viên không hỏi bằng `exists()`) thì ca ném lỗi thường,
  không phải `bang`, và executor đổi seam sang hàm `Path` mà ứng viên thực sự gọi rồi khai vào handoff.
- **Quy ước đếm theo ĐƯỜNG (r7; HINT lượt 6 viết bản đầu, r7 viết lại theo trục C của bảng không gian mở rộng ở
  B2).** Q-A.1 (hỏi đúng một lần), câu "bước đọc này cũng chỉ làm một lần" của Q-A.4, câu "phải THỰC SỰ gọi
  `kill(pid, 0)` (đúng một lần)" của r5, và "nguyên xi" của Q-A.3 là thuộc tính của MỌI đường, không riêng
  `B2-dem-lan`, `B2-dem-doc`, `B2-pid-du-phong`. Trong mỗi lời gọi `_con_song`, ca đòi:
  · **hỏi** ĐÚNG 1 trên mọi đường (seam ở `Path.stat`, loại `stat count`; seam ở `Path.exists` cho ba đầu vào
    `hoi-*` của `B2-thoat-parse`, loại `exists count`);
  · **đọc** ĐÚNG 1 trên đường Đ (đường mới) và đường Đ0 (tệp có); ĐÚNG 0 trên đường K0 (tệp vắng); loại
    `read count`;
  · **kill** ĐÚNG 1 trên đường K và K0; ĐÚNG 0 trên đường Đ0; loại `kill count`.
  Q-A không quy định số lần đọc hay số lời gọi `kill` trên đường ESRCH, trên đường mà phép hỏi ném ngoại lệ
  ngoài họ `OSError`, và số lời gọi `kill` trên đường Đ khi đọc được: ở đó ca không đòi gì (và không đặt
  observer). Một ngoại lệ có chủ ý: `B2-dem-lan` đi đường Đ0 (lần hỏi đầu là `stat` thật) nhưng là nhãn của trục
  hỏi, nên chỉ giữ phép "đọc ≤ 1" của HINT và không đặt observer `kill`; đọc ĐÚNG 1 và kill 0 trên Đ0 do
  `B2-nhanh-cu` và lời gọi đường cũ của `B3-zombie` đo. `B1` đếm hỏi theo TỪNG lời gọi (cộng dồn 1, 2, 3 qua
  ba lời gọi); `B3-zombie` đếm (hỏi, đọc) cộng dồn (1, 1), (2, 2) qua hai lời gọi đường mới, rồi lời gọi đường cũ
  hỏi 1, đọc 1, kill 0. `B3-song`, `B3-da-wait` không có seam nên không đếm; `B3b-giet-cay` chỉ đòi seam đã chạm,
  vì `_giet_cay` gọi `_con_song` nhiều lần. Danh sách mỗi đầu vào đòi gì: bảng trục C ở B2. Lý do đo được: bản vá
  chỉ hỏi lại `exists()` khi gặp ESRCH, hay chỉ khi gặp `OSError` không phải `PermissionError`, hay chỉ đọc lại
  khi phép đọc gặp EPERM, qua hết hai ca r6, phép D và toàn suite — các nhãn r6 chỉ đòi seam "đã chạm" (≥ 1)
  (cross-review lượt 6); và trên helper dựng đúng theo HINT (chỉ đòi hỏi 1, đọc ≤ 1, và kill chỉ ở hai nhãn), bản
  vá đọc thêm trên đường tệp vắng, gọi `kill` trên đường tệp có, hay gọi `kill` lần hai chỉ khi phép đọc gặp EPERM
  vẫn lọt (bảng 9 dòng 7).
- Ca chỉ chuyển thành `bang(False, ...)` ngoại lệ **có gốc đo được từ chính ca** (r6 nêu đủ bốn loại; r5 chỉ
  nêu loại đầu): (1) đối tượng do seam tạo ra, so bằng danh tính (`is`); (2) ngoại lệ THẬT mà observer của
  `os.kill(pid, 0)` vừa chuyển tiếp — observer ghi lại đối tượng rồi ném lại đúng nó, nên danh tính biết
  trước khi nó thoát (cần cho `B2-pid-du-phong` tiểu nhãn `da-wait`, nơi ESRCH là của kernel chứ không của
  seam); (3) ngoại lệ mới có chuỗi `__cause__` (tức `raise … from …`) chứa một đối tượng loại (1) hoặc (2) —
  bản vá bọc lại ngoại lệ thay vì để nó thoát nguyên đối tượng (Q-A.5); thông điệp ghi `seam wrapped`;
  (4) chỉ ở `B2-parse`, ở các đầu vào parse `p1`–`p3` của `B2-pid-du-phong` (đúng các đầu vào của `B2-parse`), và ở
  hai đầu vào tự nhiên `p1`, `p3` của `B2-nhanh-cu` (r7, cột Đ0), và chỉ sau khi seam đọc đã chạm: ngoại lệ TỰ
  NHIÊN của phép tách trạng thái (nhãn `B2-parse` mô tả cách nhận ra — r7: theo kiểu, đối số VÀ nguồn; nguồn so bằng
  HÀM và NỘI DUNG dòng, không bằng tệp hay số dòng). Chuỗi `__context__` (ngữ cảnh ngầm) KHÔNG được tính: một ngoại lệ vô can ném ra
  trong lúc xử lý lỗi seam luôn mang `__context__` là lỗi seam, và nếu tính nó thì ngoại lệ vô can bị ghi
  nhầm thành bằng chứng (đã đo, bảng 8, đối chứng `ctrl`). Cấm `except Exception`/`except BaseException`
  rồi đổi mọi thứ thành `TinHieuChotCa`: mọi ngoại lệ ngoài bốn loại trên giữ hạng vô can (runner in kiểu
  ngoại lệ trong ngoặc sau tên ca — đó là tín dụng giả).
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
  nếu một ngoại lệ thuộc bốn loại ghi nhận của quy ước chung ở trên (đối tượng do seam của L tạo ra, so bằng danh
  tính; ngoại lệ thật observer đã ghi; ngoại lệ bọc lại; ngoại lệ tự nhiên nhận ra theo luật của `B2-parse`, kể cả
  điều kiện nguồn) thoát khỏi lời gọi
  thì nó bị nuốt; mọi ngoại lệ khác vẫn thoát. Nới KHÔNG được là cách để bỏ đầu vào, bỏ thiết lập hay trả sớm.
  Hai ca đăng ký vẫn chỉ là hai ca (§6.2): phép đo dùng tham số là lời gọi TRỰC TIẾP helper từ tập
  lệnh bằng chứng của executor, trên bản sao đột biến (cùng cách B5 đã đòi gọi thẳng hàm ca) — không
  phải ca đăng ký thứ ba và không sửa runner `--dot-bien`. **Mặc định của hai tham số là một phần của
  hợp đồng và được khoá RIÊNG bằng phép D** (mặc định: mọi nhãn chạy, tập nới rỗng); không được suy
  ra từ việc một đột biến sản phẩm chết ở ca đăng ký, vì đột biến ấy có thể chết ở một nhãn khác.
- **Thứ tự thực thi cố định** trong `t156_...`, đúng thứ tự liệt kê ở đây: `B1`, `B2-eacces`, `B2-eio`,
  `B2-eperm-hoi`, `B2-doc-hong`, `B2-tin-hieu`, `B2-dem-lan`, `B2-exception`, `B2-thoat-parse`, `B2-parse`, `B2-dem-doc`,
  `B2-pid-du-phong`, `B2-nhanh-cu` (r7), `B3-song`, `B3-da-wait`, `B3-zombie`. `bang` ném ở assertion sai ĐẦU TIÊN, nên nhãn báo là nhãn đầu tiên trong
  thứ tự này; B5 dựa vào điều đó. Trong một nhãn có tiểu nhãn, các đầu vào cũng chạy theo thứ tự cố định
  của bảng tiểu nhãn, và assertion sai đầu tiên quyết định tiểu nhãn báo. `t157_...` chỉ có
  `B3b-giet-cay`. B4 không phải nhãn (nó là điều kiện nền).

**Ca `t156_...`**

- **B1 (mục 2) — ESRCH.** Seam ném `ProcessLookupError(errno.ESRCH, …)`. Gọi `_con_song(os.getpid())`,
  `_con_song_dung_khoa(os.getpid(), <khoá thật>)` và `_giet_rieng({<pid con đã wait>: "k"}, 0)`: không
  ngoại lệ nào thoát; hai hàm đầu trả `False`. Nhãn `B1`.
  **ĐỎ khi:** chạy trên nền `89fc4fa` ⇒ `ProcessLookupError` thoát ⇒ ca đổi đúng đối tượng ấy thành
  `bang(False, …)` của chính nó, loại `seam escaped` (dòng (a)); hoặc phép hỏi để ESRCH rơi cùng nhánh với
  `OSError` khác, vào bước đọc rồi trả `True` cho PID sống, loại `result True` (dòng (l2)); hoặc (r7) phép hỏi gặp
  ESRCH thì hỏi `exists()` lại một lần rồi mới trả `False` — kết quả đúng, nhưng bộ đếm hỏi cộng dồn theo lời gọi
  lệch, loại `stat count` (dòng (m4)). `B1` chỉ đo ESRCH ở tầng HỎI (kết quả đúng `False`); ESRCH ở tầng ĐỌC là
  nhãn khác, `B2-doc-hong` tiểu nhãn `ESRCH` (kết quả đúng `True`), và không nhãn nào thay được nhãn kia.
- **B2 (mục 2) — miền lỗi khác ESRCH, chống bản rộng và bản hẹp giả.** Trên `os.getpid()` (PID sống):
  - `B2-eacces`: seam `PermissionError(errno.EACCES, …)` ⇒ `_con_song` trả **`True`**, không ngoại lệ nào
    thoát. **ĐỎ khi** bản RỘNG (`except OSError: return False`) ⇒ `False` (dòng (b)); hoặc bản chỉ bắt
    `ProcessLookupError` — bản vá tối thiểu cho đúng ESRCH — nên EACCES thoát (dòng (l1)).
  - `B2-eio`: seam `OSError(errno.EIO, …)` ⇒ `True`, không ngoại lệ nào thoát. **ĐỎ khi** bản chỉ bắt
    `PermissionError`: EIO thoát ra, trái objective "mọi `OSError`" (dòng (d1)); hoặc bản cho
    `PermissionError` vào bước đọc nhưng trả `False` cho `OSError` khác (dòng (l3)).
  - `B2-eperm-hoi` (r6) — seam `PermissionError(errno.EPERM, …)` ở `Path.stat` của PID sống ⇒ `True`, không
    ngoại lệ nào thoát. EACCES và EPERM cùng lớp `PermissionError`, khác errno; nhãn này đo việc bản vá đối xử
    theo LỚP chứ không theo errno (Q-A.4, r6). **ĐỎ khi:** phép hỏi chỉ nhận một tập errno hữu hạn (EACCES và
    EIO) nên EPERM thoát (dòng (l4)); hoặc phép hỏi phân nhánh riêng cho EPERM và trả `False` (dòng (l5)).
    Giới hạn khai thẳng: errno là tập MỞ. EACCES, EPERM, EIO là ba đại diện; một bản vá nhận đúng ba errno ấy
    và từ chối errno thứ tư (ví dụ ENOMEM) qua được nghiệm thu này. Bản vá như thế vẫn là vi phạm Q-A.4 (r6),
    nhưng phép đo chỉ chứng minh tới ba đại diện: KHÔNG ĐO ĐƯỢC cho errno thứ tư trở đi.
  - `B2-doc-hong` (r4 mở rộng; r3 chỉ có đầu vào EACCES; r6 thêm `EPERM`) — bốn đầu vào, tiểu nhãn `EACCES`,
    `EIO`, `ESRCH`, `EPERM`, chạy đúng thứ tự ấy. Mỗi đầu vào: seam EACCES ở `Path.stat` của PID sống và seam ở
    `Path.read_text` của đúng đường `/proc/<pid>/stat` của PID ấy ném MỘT đối tượng dựng sẵn — lần lượt
    `PermissionError(errno.EACCES, …)`, `OSError(errno.EIO, …)`, `ProcessLookupError(errno.ESRCH, …)`,
    `PermissionError(errno.EPERM, …)`.
    Mỗi đầu vào phải trả **`True`** (không đọc được thì rơi về `kill(pid, 0)`, không tự khẳng định đã
    chết) và không ngoại lệ nào thoát. (r7) Observer `os.kill(pid, 0)` chuyển tiếp thật và ca đòi đúng MỘT lời gọi
    (quy ước đếm): đầu vào `EPERM` ở tầng đọc không nằm trong ma trận của `B2-pid-du-phong`, nên thiếu phép đếm này
    thì bản vá gọi `kill` lần hai chỉ khi phép đọc gặp EPERM lọt hết (rig r7, biến thể (E)
    `k_kill_lai_khi_doc_EPERM`: lọt helper dựng theo HINT, chết ở tiểu nhãn `EPERM` loại `kill count` trên helper r7). **ESRCH ở tầng đọc KHÔNG phải ESRCH ở tầng hỏi:** ở tầng hỏi kết quả
    đúng là `False` (`B1`), ở tầng đọc kết quả đúng là `True` — hai ô có kỳ vọng NGƯỢC nhau, nên một bản vá
    dùng chung một nhánh xử lý ESRCH cho cả hai tầng chết ở đúng một trong hai nhãn, và hai nhãn này
    KHÔNG thay được cho nhau. Ca đổi chỉ đúng đối tượng do seam tạo ra thành `TinHieuChotCa` khi nó thoát
    (quy ước chung); ngoại lệ khác giữ hạng vô can. **ĐỎ khi:** tầng đọc chỉ bắt `PermissionError` (EIO
    và ESRCH thoát — tiểu nhãn báo là `EIO`, đầu vào đầu tiên làm nó thoát; dòng (d2)); đường đọc hỏng trả
    `False` cho mọi lỗi (tiểu nhãn `EACCES`; dòng (g1)); đường đọc hỏng chỉ trả `False` riêng cho
    `ProcessLookupError` còn lỗi khác vẫn hỏi PID dự phòng (tiểu nhãn `ESRCH`; dòng (g2)). Năm dòng của r6, mỗi
    dòng một hướng còn thiếu của bảng không gian: đọc không bắt `OSError` nào, chỉ bắt nhóm phân tích (tiểu nhãn
    `EACCES`, thoát; dòng (l10)); đọc nhận errno EACCES và EIO mà không nhận ESRCH (tiểu nhãn `ESRCH`, thoát;
    dòng (l11)); đọc nhận errno EACCES, EIO, ESRCH mà không nhận EPERM (tiểu nhãn `EPERM`, thoát; dòng (l12));
    đọc trả `False` riêng cho EPERM (tiểu nhãn `EPERM`; dòng (l13)); đọc cho `PermissionError` rơi về bước kill
    nhưng trả `False` cho `OSError` khác (tiểu nhãn `EIO`; dòng (l14)).
  - `B2-tin-hieu` (r4 mở rộng; r3 chỉ có tầng hỏi; r6 thêm `kill`) — ba đầu vào, tiểu nhãn `hoi`, `doc`, `kill`,
    chạy theo thứ tự ấy. `hoi`: `Path.stat` của PID sống ném MỘT sentinel `KeyboardInterrupt` dựng sẵn. `doc`:
    `Path.stat` ném EACCES và `Path.read_text` của đúng PID ấy ném một sentinel `KeyboardInterrupt` KHÁC.
    `kill`: `Path.stat` ném EACCES, `Path.read_text` ném EACCES (để rơi về bước kill), và observer của
    `os.kill(pid, 0)` ném một sentinel `KeyboardInterrupt` THỨ BA (đếm lần chạm; r7: đúng 1, quy ước đếm). Mỗi đầu vào: ca bắt
    ngay quanh lời gọi và so **đúng đối tượng** (`is`); trả về bình thường thay vì truyền sentinel ra ⇒
    `bang(False, …)`. Ngoại lệ khác giữ hạng vô can (bọc lại bằng `raise … from …` thì theo quy ước chung là
    `seam wrapped`, cũng `bang(False, …)`). **ĐỎ khi:** nuốt `BaseException` quanh phép hỏi (tiểu nhãn
    `hoi`); nuốt riêng `KeyboardInterrupt` ở tầng đọc dù `RuntimeError` vẫn được truyền ra (tiểu nhãn `doc`);
    thêm mệnh đề bắt `BaseException` vào khối `kill` (tiểu nhãn `kill`; dòng (l25)). Sentinel ở tầng hỏi KHÔNG
    thay phép đo tầng đọc hay tầng kill, và sentinel `RuntimeError` của `B2-exception` không thay sentinel
    `KeyboardInterrupt` của nhãn này: bản vá nuốt riêng `KeyboardInterrupt` giữ `RuntimeError` thoát nguyên
    nên `B2-exception` xanh với nó.
  - `B2-dem-lan`: seam theo thứ tự — lần hỏi thứ nhất đi `stat` thật, lần thứ hai ném ESRCH; một lời gọi
    `_con_song` phải chạm seam **đúng một lần** và trả đúng theo trạng thái thật. **ĐỎ khi** bản vá gọi
    `exists()` lần hai: `ProcessLookupError` từ lần hai thoát ra, hoặc bộ đếm lần chạm ≠ 1.
  - `B2-exception` (r3; r6 thêm `kill`) — miền `Exception` KHÔNG thuộc `OSError` (sentinel `RuntimeError`),
    **ba tầng, ba đầu vào, cùng một nhãn**; tiểu nhãn theo thứ tự `hoi`, `doc`, `kill`. Thông điệp `bang` ghi
    tiểu nhãn ngay sau nhãn. (Bản HINT lượt 5 đặt thêm tiểu nhãn `hoi-parse` ở đây, dùng `IndexError`; r6 chuyển
    nó sang nhãn riêng `B2-thoat-parse` vì nhóm phân tích có ba thành viên và ba tầng, xem ngay dưới.)
    · `hoi`: seam `Path.stat` của PID sống ném MỘT đối tượng `RuntimeError` dựng sẵn. `_con_song` phải
      để CHÍNH đối tượng ấy thoát ra. Ca bắt ngay quanh lời gọi và so bằng danh tính (`is`); trả về
      bình thường (kể cả `True`) thay vì ném ⇒ `bang(False, …)`. Đối tượng khác thoát ra ⇒ không bắt
      (vô can).
    · `doc`: seam `Path.stat` ném EACCES (để vào bước 4 của Q-A) và seam `Path.read_text` của đúng
      PID ấy ném MỘT đối tượng `RuntimeError` dựng sẵn khác; chính đối tượng đó phải thoát ra. Cùng
      cách bắt và so như `hoi`.
    · `kill`: seam `Path.stat` ném EACCES, `Path.read_text` ném EACCES (để rơi về bước kill), và observer
      của `os.kill(pid, 0)` ném MỘT `RuntimeError` dựng sẵn thứ ba (đếm lần chạm; r7: đúng 1); chính đối tượng đó phải
      thoát ra. Cùng cách bắt và so như `hoi`.
    **ĐỎ khi:** phép hỏi (`hoi`; dòng (h1)), khối đọc (`doc`; dòng (h2)) hoặc khối `kill` (`kill`; dòng
    (l26)) bắt `Exception`; hoặc phép hỏi bắt `Exception` rồi ném `RuntimeError` mới bằng `raise … from …`
    (`hoi`, thông điệp `seam wrapped`; dòng (l9)). Lý do có nhãn này: `KeyboardInterrupt` ở `B2-tin-hieu`
    thuộc `BaseException` nên bản `except Exception` cho nó thoát nguyên, và một mình nó không phân biệt được
    `except OSError` với `except Exception` (bảng 3: `RuntimeError` bị nuốt trong khi B1–B3b của r2 vẫn PASS).
  - `B2-thoat-parse` (r6, nhóm phân tích `ValueError`, `IndexError`, `UnicodeDecodeError` phải THOÁT NGUYÊN ở
    tầng hỏi và tầng kill — nơi Q-A.5 không cho bắt chúng) — sáu đầu vào, tiểu nhãn theo thứ tự `hoi-index`,
    `hoi-value`, `hoi-decode`, `kill-index`, `kill-value`, `kill-decode`. Mỗi đầu vào ném MỘT sentinel dựng
    sẵn, ca bắt ngay quanh lời gọi và so **đúng đối tượng** (`is`) như `B2-exception`:
    · `hoi-*`: seam ở **`Path.exists`** (không ở `Path.stat`: bảng 7 — `exists()` nuốt `ValueError` và
      `UnicodeDecodeError` phát sinh trong `stat`, nên ở `Path.stat` chỉ `IndexError` đo được; ba tiểu nhãn dùng
      cùng một seam để cùng một phép đo) ném lần lượt `IndexError`, `ValueError`, `UnicodeDecodeError` dựng sẵn
      (đối số dựng tay, ví dụ `UnicodeDecodeError('utf8', bytes([255]), 0, 1, 'x')`, byte 255 không giải mã được).
      `_con_song` phải để chính đối tượng thoát ra: không đọc dự phòng, không trả kết quả sống/chết.
    · `kill-*`: seam `Path.stat` ném EACCES, `Path.read_text` ném EACCES (để rơi về bước kill), observer của
      `os.kill(pid, 0)` ném lần lượt `IndexError`, `ValueError`, `UnicodeDecodeError` dựng sẵn (đếm lần chạm;
      r7: đúng 1); chính đối tượng đó phải thoát ra. (r7) Ba đầu vào `hoi-*` đòi seam `Path.exists` chạm đúng 1,
      loại `exists count`.
    Thứ tự `index`, `value`, `decode` có chủ ý: `ValueError` là cha của `UnicodeDecodeError`, nên bản bắt
    `ValueError` chết ở `value` (đứng trước) còn chỉ bản bắt riêng `UnicodeDecodeError` mới chết ở `decode`.
    **ĐỎ khi** (mỗi tiểu nhãn một dòng): phép hỏi bắt thêm `IndexError` (dòng (l6)), `ValueError` (dòng
    (l7)) hoặc riêng `UnicodeDecodeError` (dòng (l8)) — bản HINT lượt 5 gọi hợp ba thứ ấy là (h3), chết ở
    `hoi-index`; khối `kill` thêm mệnh đề bắt `IndexError` (dòng (l27)), `ValueError` (dòng (l28)) hoặc riêng
    `UnicodeDecodeError` (dòng (l29)). Nhóm phân tích ở tầng hỏi và kill KHÔNG có nguồn tự nhiên đã biết
    (sentinel do ca dựng); việc `pathlib` hay kernel thật sinh chúng: KHÔNG ĐO ĐƯỢC và không cần cho ô này —
    ô đo hợp đồng "thoát nguyên" của Q-A.5, không đo tần suất.
  - `B2-parse` (r3) — nội dung đọc được nhưng KHÔNG phân tích được, trên đường MỚI (Q-A.4 và đoạn làm
    rõ ở §3; đường cũ trả `False` và không thuộc nhãn này). Bốn đầu vào (tiểu nhãn `p1`–`p4`, chạy theo
    thứ tự ấy), PID sống (`os.getpid()`), seam `Path.stat` ném EACCES, và seam `Path.read_text` của đúng
    đường `/proc/<pid>/stat`: (p1) trả chuỗi rỗng; (p2) trả chuỗi thiếu dấu đóng ngoặc, ví dụ
    `<pid> x S 1`; (p3) trả chuỗi hết ngay sau dấu đóng ngoặc, ví dụ `<pid> (x)`, và cả biến thể có khoảng
    trắng cuối (cùng tiểu nhãn `p3`, hai payload); (p4) ném một
    `UnicodeDecodeError` do ca dựng sẵn (dạng "không giải mã được", có thật: bảng 4). Mỗi đầu vào:
    `_con_song(os.getpid())` phải trả **`True`** (rơi về `kill(pid, 0)`), không ngoại lệ nào thoát.
    **Phân hạng ngoại lệ thoát ra khỏi `_con_song` ở nhãn này (r6 đổi; r3–r5 cấm đổi MỌI ngoại lệ thành
    `TinHieuChotCa`).** Cái giá của lệnh cấm ấy, đo được ở lượt 5 và r6: mọi bản KHÔNG bắt
    `ValueError`, `IndexError` hay `UnicodeDecodeError` ở tầng đọc chỉ chết bằng lỗi vô can, tức tín dụng giả
    (bảng 3, hàng "tầng đọc chỉ bắt `OSError`"), nên ba ô của hàng nhóm phân tích × tầng đọc (hướng
    "thoát") không có đột biến nào chết đúng lý do. Quy tắc mới, hai trường hợp:
    · (p4) `UnicodeDecodeError` do CHÍNH seam dựng: danh tính biết trước ⇒ thoát ra thì `bang(False, …)`
      (thông điệp `seam escaped`), theo quy ước chung.
    · (p1)–(p3) ngoại lệ TỰ NHIÊN của phép tách: ca tự tính TRƯỚC, NGOÀI launcher, cặp (kiểu, đối số) mà biểu
      thức tách trạng thái của nền (`launcher.py:654`; bảng 4) ném trên đúng chuỗi payload — ví dụ
      `ValueError('substring not found')` cho p1 và p2, `IndexError('list index out of range')` cho p3 trên
      Python 3.12.3; ca tính lúc chạy, không viết cứng. Nếu `_con_song` để thoát một ngoại lệ đúng kiểu VÀ
      đúng đối số ấy (hoặc bọc lại bằng `raise … from …` với nguyên nhân là ngoại lệ ấy), SAU khi seam đọc đã
      chạm, ca ⇒ `bang(False, …)` (thông điệp `parse error escaped` hoặc `parse error wrapped`). **Và (r7,
      cross-review lượt 6) NGUỒN:** khung Python TRONG CÙNG của traceback của ngoại lệ ấy (khung cuối chuỗi
      `tb_next`; với `parse error wrapped`: của mắt `__cause__` khớp) phải là dòng biểu thức tách trạng thái ở tầng
      đọc của mã ứng viên. Thiếu điều kiện này thì (kiểu, đối số) là tín hiệu mà mã KHÁC giả được:
      `substring not found` và `list index out of range` là thông điệp CHUNG của mọi `str.index`/`rindex` và mọi
      phép chỉ số danh sách. **Cách so (r7 sửa chữ của HINT): so HÀM và NỘI DUNG dòng, KHÔNG so tệp và số dòng.**
      Executor khai trong handoff (a) tên hàm chứa biểu thức tách (ở nền là `_con_song`; hàm trợ giúp riêng nếu ứng
      viên tách ra) và (b) một chuỗi con của biểu thức tách, có mặt trên đúng dòng ấy ở cả đường Đ lẫn đường Đ0 và
      không có trên dòng nào khác của hàm ấy (ở nền: phần `rindex(")")`); ca đòi `co_name` của khung trong cùng
      bằng (a), và dòng nguồn của khung ấy — đọc từ `co_filename` bằng `linecache` sau `checkcache`, hoặc đọc thẳng
      tệp — chứa (b). Vì sao không so tệp và số dòng như HINT viết: runner `--dot-bien` nạp mỗi bản đột biến từ một
      tệp tạm riêng (`launcher_db_NN.py`, tên riêng là bài học chống va chạm `.pyc`), nên `co_filename` KHÔNG BAO GIỜ
      bằng tệp executor khai; và đột biến chèn dòng phía trên biểu thức tách làm trôi số dòng — (l16) chèn đúng
      một dòng. Đo trên rig r7 (bảng 9 dòng 5): so tệp + dòng ⇒ (l15), (l16), (l17), (l21) và hai biến thể Đ0 chết
      vô can (tín dụng giả nếu là mục `DOT_BIEN`); chỉ so số dòng ⇒ (l16) chết vô can; so hàm + nội dung ⇒ cả tám
      dòng của nhãn và hai biến thể Đ0 đúng, biến thể tín dụng giả của lượt 6 chết vô can. Đột biến ĐỔI chính dòng
      biểu thức tách (như (m5)) thì dòng ấy có thể không còn chuỗi (b) — hợp lệ, vì các dòng ấy nhắm kết quả chứ
      không nhắm ngoại lệ tự nhiên. Ngoại lệ có kiểu khác hoặc đối số khác — ví dụ một `ValueError` do lỗi khác của
      ứng viên — vẫn là lỗi vô can, giữ hạng vô can.
    Quy tắc này hẹp có chủ ý: nó chỉ ghi nhận đúng thứ mà bản vá phải xử lý. Đối chứng đã đo (bảng 8, `ctrl`):
    một bản phân tích hỏng ném `ValueError` khác đối số ngay sau khi đọc vẫn chết bằng `ValueError` vô can, không
    bị ghi nhầm thành bằng chứng. **Nhưng (kiểu, đối số) một mình KHÔNG hẹp như câu trên khai** (cross-review lượt
    6, ba Python): một biến thể ĐÃ bắt đúng `ValueError` của phép tách, rồi trong nhánh xử lý gọi một `str.index`
    độc lập (trên một biến môi trường rỗng) ném `ValueError('substring not found')`, được luật r6 ghi
    `B2-parse p1 parse error escaped` — A1 và W1 đúng nhãn, tiểu nhãn, loại; W0 sống: tín dụng giả qua đủ bốn
    phép. Có điều kiện NGUỒN ở trên thì biến thể ấy chết vô can, còn (i), (l15)–(l21) vẫn chết như cũ (reviewer đo
    cùng lượt: 50/50 cặp; phiên soạn r7 đo lại trên rig riêng với cách so hàm + nội dung: 55/55 cặp, bảng 9 dòng 2 và
    5). Đối chứng thứ ba (bắt buộc): cùng kiểu, cùng đối số, ném từ dòng khác dòng biểu thức tách ⇒ phải chết vô can
    (rig r7: chết `ValueError: substring not found` vô can ở A1, W1 và W0, bảng 9 dòng 12).
    **ĐỎ khi** (tám dòng, mỗi hướng của bảng không gian một dòng): đường nội dung hỏng trả `False` ⇒ chết bằng
    assertion kết quả `True` ở `p1` (dòng (i)); tầng đọc không bắt `ValueError` ⇒ chết ở `p1` (dòng (l15));
    kiểm tra dữ liệu chỉ nhận ra chuỗi rỗng mà không bắt `ValueError` ⇒ `p1` qua, chết ở `p2` (dòng (l16));
    tầng đọc không bắt `IndexError` ⇒ chết ở `p3` (dòng (l17)); `IndexError` ⇒ `False` ⇒ chết ở `p3` (dòng (l18));
    phép đọc chỉ bắt `OSError` còn phần tách bọc riêng nên `UnicodeDecodeError` thoát ⇒ chết ở `p4` (dòng (l19));
    `UnicodeDecodeError` ⇒ `False` ⇒ chết ở `p4` (dòng (l20)); tầng đọc bọc lại `ValueError` tự nhiên thành
    `RuntimeError` bằng `raise … from …` ⇒ chết ở `p1` (dòng (l21), thông điệp `parse error wrapped`).
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
    `B2-parse`). Giữ nguyên các kiểm đếm `stat` hiện có (`B2-dem-lan`). (r7, quy ước đếm) Mỗi đầu vào còn đòi hỏi
    đúng 1; đầu vào `3` (đường K) đặt observer `os.kill(pid, 0)` chuyển tiếp thật và đòi đúng 1 lời gọi. **ĐỎ khi** (đột biến (j)): bộ
    đếm ≠ 1, tức đọc lại lần hai, ở nhánh nào cũng vậy — lần đọc thứ hai đặt sau lần đọc thành công làm
    đầu vào `1` đỏ đầu tiên; lần đọc thứ hai đặt trong xử lý đọc lỗi chỉ chạm ở đầu vào `3`.
  - `B2-pid-du-phong` (r5, thêm sau cross-review lượt 4) — khoá KẾT QUẢ và VIỆC THỰC HIỆN của bước PID dự
    phòng ở Q-A.4, thay vì suy từ `True` trên PID sống. Q-A.4 nói khi không đọc được thì chỉ `os.kill(pid, 0)`
    quyết định sống hay chết; mọi nhãn ở trên đặt đầu vào đọc lỗi hoặc hỏng lên PID SỐNG, nên một bản trả `True`
    ngay sau lỗi đọc — không hỏi PID nào — qua được chúng (lượt 4 đo: qua cả hai ca mẫu của r4 lẫn D) mà vẫn
    báo "sống" cho một PID con đã `wait`. Bốn tiểu nhãn theo thứ tự: `song`, `da-wait`, `eperm`, `eio`. Mỗi
    tiểu nhãn chạy CÙNG tám đầu vào đọc, theo thứ tự: EACCES, EIO, ESRCH (ba lỗi đọc của `B2-doc-hong`), p1,
    p2, p3 không khoảng trắng cuối, p3 có khoảng trắng cuối, p4 (đúng các đầu vào của `B2-parse`: bốn tiểu nhãn, năm lần đọc vì p3 có hai payload), luôn với
    seam `stat` EACCES để vào bước 4. Tổng 4 × 8 = 32 lời gọi `_con_song` trực tiếp. Con số 32 ở đây là số
    đầu vào của nhãn, KHÔNG phải số control của D (D có 63 control ở r7; HINT lượt 6 đề nghị 49; 43 ở r6). Ma trận vẫn tám đầu vào đọc: đầu vào
    `EPERM` ở tầng đọc (r6 thêm ở `B2-doc-hong`) không đưa vào ma trận, vì ma trận đo chiều kết quả của bước
    kill chứ không đo phạm vi bắt của bước đọc.
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
    bọc seam ấy quanh thiết lập hay dọn con. Khi `kill` thật ném (tiểu nhãn `da-wait`: ESRCH của kernel), observer
    ghi lại CHÍNH đối tượng ấy rồi ném lại đúng nó (r6; quy ước chung, loại 2) — nhờ đó một bản vá để ESRCH thật
    thoát ra khỏi `_con_song` vẫn bị nhận ra bằng danh tính, thay vì chết bằng lỗi vô can. Trong mỗi lời gọi ca
    đòi, theo thứ tự: đúng MỘT lời gọi `kill(pid, 0)`; kết quả đúng như trên; bộ đếm seam `stat` = 1 và `read`
    = 1. Nới nhãn vẫn chạy mọi đầu vào và observer, chỉ bỏ assertion. Phân hạng ngoại lệ thoát ra khỏi
    `_con_song` theo quy ước chung (bốn loại) và, cho p1–p4, theo quy tắc của `B2-parse` (kể cả điều kiện nguồn,
    r7). Không đổi ngữ nghĩa Q-A.3/.4.
    **ĐỎ khi** (lớp (k), mỗi tiểu nhãn có một mutant độc chiếm về KẾT QUẢ, đã đo ở bảng 6): bản trả `True`
    ngay, không hỏi PID ⇒ `song` (số lời gọi `kill` bằng 0; dòng (k1)); bản hỏi PID nhưng bỏ kết quả ⇒ `da-wait`
    (PID đã `wait` được báo `True`; (k2)); bản tự xử lý `kill` và trả `False` cho `PermissionError` ⇒ `eperm`
    ((k3)); bản tự xử lý `kill` và trả `True` cho `OSError` khác ⇒ `eio` ((k4)); bản hỏi `kill` hai lần (một lần
    trong xử lý lỗi đọc, một lần ở khối chung) ⇒ `song`, bộ đếm bằng 2 ((k5), r6). Ba hướng "thoát" của khối
    `kill` (r6, lớp (l)): khối chỉ bắt `PermissionError` nên ESRCH thật thoát ⇒ `da-wait` (dòng (l22)); khối chỉ
    bắt `ProcessLookupError` nên EPERM thoát ⇒ `eperm` (dòng (l23)); khối bỏ mệnh đề `OSError` nên EIO thoát ⇒
    `eio` (dòng (l24)). `B3-da-wait` (không seam) KHÔNG thay được `da-wait` của nhãn này: nó không đi qua
    đường lỗi mới.
  - `B2-nhanh-cu` (r7, cross-review lượt 6; r7 mở rộng từ năm thành **mười chín** đầu vào theo bảng không gian mở
    rộng) — hai nhánh SẴN CÓ của Q-A.3, tức phép hỏi KHÔNG lỗi: cột **Đ0** (tệp có ⇒ đọc) và cột **K0** (tệp vắng
    ⇒ `kill(pid, 0)`). Tiểu nhãn theo thứ tự cố định dưới đây. Kỳ vọng là hành vi CŨ (§2, mã nền
    `launcher.py:651–664` trên `89fc4fa`) mà Q-A.3 giữ nguyên xi — KHÔNG phải lời khẳng định rằng hành vi ấy "đúng".
    · Cột Đ0 — PID là chính tiến trình (`os.getpid()`); `Path.stat` THẬT (chỉ đếm, không ném) nên `exists()` đúng;
      observer `os.kill(pid, 0)` chuyển tiếp thật; mỗi đầu vào đòi hỏi 1, đọc 1, kill **0**:
      `song`: `read_text` thật ⇒ **`True`**.
      `EACCES`, `EIO`, `ESRCH`, `EPERM`: `read_text` của đúng đường ấy ném MỘT đối tượng dựng sẵn — lần lượt
      `PermissionError(errno.EACCES, …)`, `OSError(errno.EIO, …)`, `ProcessLookupError(errno.ESRCH, …)`,
      `PermissionError(errno.EPERM, …)` ⇒ **`False`**.
      `p1`: `read_text` trả chuỗi rỗng ⇒ `ValueError` tự nhiên của phép tách ⇒ **`False`**. `p3`: trả `<pid> (x)` ⇒
      `IndexError` tự nhiên ⇒ **`False`**. Hai đầu vào này dùng luật nhận ra ngoại lệ tự nhiên của `B2-parse` (kiểu,
      đối số, nguồn) để hướng "thoát" chết đúng lý do. `p4`: `read_text` ném MỘT `UnicodeDecodeError` dựng sẵn ⇒
      **`False`**. (HINT lượt 6 gọi `p1` là `rong`; r7 đổi tên cho khớp `B2-parse`.)
      `tin-hieu`: `read_text` ném MỘT sentinel `KeyboardInterrupt` dựng sẵn ⇒ chính đối tượng ấy thoát (so `is`).
      `exception`: `read_text` ném MỘT sentinel `RuntimeError` dựng sẵn ⇒ chính đối tượng ấy thoát.
    · Cột K0 — mỗi đầu vào đòi hỏi 1, đọc **0**, kill **1**; trừ `vang-da-wait`, `Path.stat` của PID ném
      `FileNotFoundError(errno.ENOENT, …)` — `exists()` NUỐT errno 2 (`_IGNORED_ERRNOS`) và trả `False`, tức "tệp
      vắng" trên PID ĐANG SỐNG:
      `vang`: observer chuyển tiếp thật ⇒ **`True`**.
      `vang-da-wait`: PID con đã `kill` và `wait`; `stat` THẬT (chỉ đếm), `/proc/<pid>` đã mất nên `exists()` trả
      `False`; observer chuyển tiếp thật, `kill` thật ném ESRCH, observer ghi lại chính đối tượng ấy (quy ước chung,
      loại 2) ⇒ **`False`**.
      `vang-eperm`: observer ném `PermissionError(errno.EPERM, …)` ⇒ **`True`**. `vang-eio`: observer ném
      `OSError(errno.EIO, …)` ⇒ **`False`**.
      `vang-tin-hieu`, `vang-exception`, `vang-index`, `vang-value`, `vang-decode`: observer ném MỘT sentinel dựng
      sẵn — lần lượt `KeyboardInterrupt`, `RuntimeError`, `IndexError`, `ValueError`, `UnicodeDecodeError` — và chính
      đối tượng ấy phải thoát (so `is`).
    Thứ tự có chủ ý, như ở các nhãn khác: `tin-hieu` trước `exception` (bản bắt `BaseException` chết ở `tin-hieu`,
    bản chỉ bắt `Exception` mới tới `exception`); `vang-value` trước `vang-decode` (`ValueError` là cha của
    `UnicodeDecodeError`); `vang-exception` trước ba đầu vào nhóm phân tích (bản bắt `Exception` ở K0 chết ở
    `vang-exception`). Cột K0 dùng CÙNG khối mã kill với tầng K ở nền; nó có đầu vào riêng vì bản vá có thể tách
    hai khối (đo: một khối K0 tách riêng mà đúng ngữ nghĩa thì cả hai ca xanh và D xanh — bảng 9 dòng 6, đối chứng —
    còn khối tách riêng mà sai thì chỉ các đầu vào K0 bắt được).
    **ĐỎ khi** (lớp (m) ở B5): nhánh cũ hợp nhất khối đọc về hướng `kill` (đọc lỗi hay nội dung hỏng ⇒ rơi về
    `kill(pid, 0)` thay vì `False`; dòng (m1), chết ở `EACCES`); nhánh cũ bắt `BaseException` (dòng (m2)); tệp vắng ⇒
    trả `False`, bỏ bước `kill` (dòng (m3)). Mọi hạng mục khác của cột Đ0 và K0 — từng thành viên × từng hướng —
    có MỘT biến thể của phép (E) ở B5 thay vì dòng `DOT_BIEN` (lý do: sàn Windows, B4); danh sách ở bảng không
    gian mở rộng. Đã đo (cross-review lượt 6, ba Python, rig reviewer): bản hợp nhất về `kill` qua HẾT hai ca r6,
    phép D và toàn suite (189/190, bằng ứng viên đúng), mà `_giet_cay` trên một con thật có phép đọc của `_con_song`
    bị EACCES lật **124 → 125** (0,11 giây → 2,36 giây; 2 → 23 lần đọc); bản "tệp vắng ⇒ `False`" báo "đã chết" cho
    PID sống; bản bắt `BaseException` nuốt `KeyboardInterrupt`. Đo ở r7 (rig riêng, ba Python): năm đầu vào của HINT
    lượt 6 để lọt 33 biến thể của hai cột này — 13 ở Đ0, 20 ở K0 (bảng 9 dòng 7); với mười chín đầu vào, 28 trong số
    ấy chết bằng `TinHieuChotCa` đúng tiểu nhãn và đúng loại, 5 biến thể "thay thế" ở K0 làm ca đỏ bằng lỗi vô can
    (không lọt; hướng "thay thế" không có loại ghi nhận — xem bảng không gian mở rộng). Đơn vị của nhãn này không có dòng `DOT_BIEN` nào giết đúng lý do (bảng 9 dòng 8):
    `EIO`, `ESRCH`, `EPERM`, `p1`, `p3`, `p4`, `exception` — chúng có biến thể (E) giết đúng lý do (đo một lần trên
    rig) và được khoá bằng assertion và phép D; răng BỀN (được đo lại ở mỗi lượt `--dot-bien`): KHÔNG ĐO ĐƯỢC, cùng
    tình trạng với `B3-song`, `B3-da-wait`.
  - **Bảng không gian phạm vi bắt ngoại lệ (r6; thay "ma trận tầng × miền" của r3–r5) — DANH SÁCH CÓ THẨM
    QUYỀN của lớp `ma-tran-loi-thieu-chot`; B5 trỏ về đây.** Vì sao thay: lớp này đã mở qua năm lượt cross-review
    liên tiếp và lần nào cũng lộ ô kế bên ô vừa vá (lượt 2: ba đường; lượt 3: ba ô tầng đọc; lượt 4: chiều kết quả
    của bước PID dự phòng; lượt 5: nhóm phân tích ở tầng hỏi). Bảng cũ được lập THEO các finding của từng lượt review, nên mỗi
    lần chỉ thêm đúng hàng vừa bị chỉ. r6 liệt kê TOÀN BỘ không gian trước, theo hai trục sinh ra mọi mệnh
    đề `except` mà một bản vá có thể viết — **lời khai của r6, và lượt 6 đo ra nó rộng hơn phép liệt kê**: ba tầng
    dưới đây chỉ là tầng của ĐƯỜNG MỚI, nhánh cũ của Q-A.3 nằm ngoài. Bảng r6 giữ nguyên ngay dưới (15 ô, số của
    r6); "Bảng không gian MỞ RỘNG (r7)" sau nó liệt kê mọi đường và là danh sách có thẩm quyền từ r7:
    · **Hàng** — các nhóm ngoại lệ mà Q-A phân biệt (năm): **R1** `ProcessLookupError` (ESRCH); **R2** `OSError`
      khác, tức lớp gồm `PermissionError` (EACCES, EPERM) và `OSError` thường (EIO) — danh sách errno chỉ là ví
      dụ (Q-A.4, r6); **R3** nhóm phân tích `ValueError`, `IndexError`, `UnicodeDecodeError`; **R4** `Exception`
      khác (`RuntimeError` làm đại diện); **R5** `BaseException` không thuộc `Exception` (`KeyboardInterrupt`
      làm đại diện).
    · **Cột** — các tầng mà một mệnh đề bắt có thể đứng (ba): **H** phép hỏi (`stat`/`exists`); **Đ** phép đọc
      (`read_text` cộng biểu thức tách trạng thái); **K** bước `os.kill(pid, 0)` mà đường lỗi rơi vào. Q-A.5 của r5
      chỉ nêu H và Đ; r6 thêm K vì Q-A.4 đặt một bước thứ ba có phạm vi bắt riêng (khối nền có ba mệnh đề), và
      r5 đã cho thấy một bản vá tự dựng lại phạm vi ấy cho đường lỗi mới (dòng (k3), (k4)).
    · **Hướng** — mỗi thành viên của một ô có hai cách sai. Ô "phải xử lý" (kết quả xác định): **thoát** (mệnh
      đề bắt thiếu nên ngoại lệ thoát ra) và **sai** (bắt nhưng trả sai kết quả). Ô "phải thoát nguyên": **bắt**
      (nuốt) và **bọc** (thoát nhưng bằng đối tượng khác, `raise … from …`). Hướng chỉ phân biệt được bằng
      LOẠI assertion nằm SAU tiểu nhãn trong thông điệp: `seam escaped`, `seam wrapped`, `parse error escaped`,
      `parse error wrapped`, `sentinel identity`, `result <giá trị>`, `kill count <n>`, và (r7, quy ước đếm)
      `stat count`, `exists count`, `read count`. Log A1/W1 phải ghi loại này.
    Mỗi ô ghi: (i) Q-A yêu cầu gì; (ii) đầu vào (nhãn, tiểu nhãn); (iii) đột biến vi phạm RIÊNG ô ấy, kèm dòng B5.

    | ô | hàng × tầng | (i) Q-A yêu cầu | (ii) đầu vào | (iii) đột biến (hướng: dòng B5) |
    |---|---|---|---|---|
    | R1-H | ESRCH × hỏi | bắt ⇒ `False` (Q-A.2) | `B1` | thoát: (a) · sai (rơi về bước đọc, trả `True`): (l2) |
    | R2-H | `OSError` khác × hỏi | không kết luận, vào bước đọc (Q-A.4) | `B2-eacces` (EACCES), `B2-eio` (EIO), `B2-eperm-hoi` (EPERM) | EACCES thoát: (l1) · EACCES sai: (b) · EIO thoát: (d1) · EIO sai: (l3) · EPERM thoát: (l4) · EPERM sai: (l5) |
    | R3-H | nhóm phân tích × hỏi | thoát nguyên (Q-A.5) | `B2-thoat-parse`: `hoi-index`, `hoi-value`, `hoi-decode` (seam ở `Path.exists`, bảng 7) | bắt `IndexError`: (l6) · bắt `ValueError`: (l7) · bắt riêng `UnicodeDecodeError`: (l8) |
    | R4-H | `Exception` khác × hỏi | thoát nguyên | `B2-exception`: `hoi` | bắt: (h1) · bọc: (l9) |
    | R5-H | `BaseException` × hỏi | thoát nguyên | `B2-tin-hieu`: `hoi` | bắt: (e1) |
    | R1-Đ | ESRCH × đọc | rơi về `kill(pid, 0)`; PID sống ⇒ `True` (Q-A.4, r4) | `B2-doc-hong`: `ESRCH` | thoát: (l11) · sai (`False`): (g2) |
    | R2-Đ | `OSError` khác × đọc | như R1-Đ | `B2-doc-hong`: `EACCES`, `EIO`, `EPERM` | EACCES thoát: (l10) · EACCES sai: (g1) · EIO thoát: (d2) · EIO sai: (l14) · EPERM thoát: (l12) · EPERM sai: (l13) |
    | R3-Đ | nhóm phân tích × đọc | rơi về `kill(pid, 0)` (Q-A.4, .5) | `B2-parse`: `p1`, `p2` (`ValueError` tự nhiên), `p3` (`IndexError` tự nhiên), `p4` (`UnicodeDecodeError` do seam) | `ValueError` thoát: (l15) ở `p1`, (l16) ở `p2` · `ValueError` sai: (i) · `IndexError` thoát: (l17) · `IndexError` sai: (l18) · `UnicodeDecodeError` thoát: (l19) · `UnicodeDecodeError` sai: (l20) · bọc: (l21) |
    | R4-Đ | `Exception` khác × đọc | thoát nguyên | `B2-exception`: `doc` | bắt: (h2) |
    | R5-Đ | `BaseException` × đọc | thoát nguyên | `B2-tin-hieu`: `doc` | bắt: (e2) |
    | R1-K | ESRCH × kill | `False` (Q-A.4, r5) | `B2-pid-du-phong`: `da-wait` | thoát: (l22) · sai (`True`): (k2) |
    | R2-K | `OSError` khác × kill | `PermissionError` (EPERM) ⇒ `True`; `OSError` khác (EIO) ⇒ `False` (Q-A.4, r5) | `B2-pid-du-phong`: `eperm`, `eio` | EPERM thoát: (l23) · EPERM sai: (k3) · EIO thoát: (l24) · EIO sai: (k4) |
    | R3-K | nhóm phân tích × kill | thoát nguyên (Q-A.5, r6) | `B2-thoat-parse`: `kill-index`, `kill-value`, `kill-decode` | bắt `IndexError`: (l27) · bắt `ValueError`: (l28) · bắt riêng `UnicodeDecodeError`: (l29) |
    | R4-K | `Exception` khác × kill | thoát nguyên | `B2-exception`: `kill` | bắt: (l26) |
    | R5-K | `BaseException` × kill | thoát nguyên | `B2-tin-hieu`: `kill` | bắt: (l25) |

    **Kiểm đếm bảng r6 (số của r6, đo bằng tập lệnh trên rig r6, xem bảng 8; tổng hiện hành ở bảng mở rộng
    ngay dưới):** 15 ô; 15 ô có đầu vào và có ít nhất một đột
    biến; 42 hạng mục (thành viên × hướng; KHÔNG gồm hướng `bọc` của mười một thành viên, xem bảng mở rộng
    ngay dưới) — T1 14, T2 17, T3 11 — và cả 42 có ít nhất một đột biến chết đúng
    tiểu nhãn và đúng loại assertion; 43 dòng B5 nằm trong bảng (một hạng mục, `ValueError` thoát ở tầng đọc, có
    hai dòng vì hai dạng nội dung hỏng khác nhau `p1` và `p2`). **Sáu dòng B5 nằm NGOÀI bảng** vì chúng không
    thuộc trục "ngoại lệ nào": (c) bỏ phép đọc (zombie); (f) hỏi lần hai; (j1), (j2) đọc lần hai; (k1) không
    hỏi PID; (k5) hỏi PID hai lần — tất cả là trục ĐẾM và QUYẾT ĐỊNH (`B2-dem-lan`, `B2-dem-doc`,
    `B2-pid-du-phong`, `B3-zombie`). 43 + 6 = 49 dòng.

    **Bảng không gian MỞ RỘNG (r7) — MỌI đường của `_con_song` nhánh Linux, liệt kê TRƯỚC rồi mới đóng. Từ r7 đây
    là DANH SÁCH CÓ THẨM QUYỀN của lớp `ma-tran-loi-thieu-chot`; B5 và phép (E) trỏ về đây.** Bảng r6 ở trên chỉ là
    15 ô của ĐƯỜNG MỚI. Lượt 6 đo được bảy bản vá trái Q-A đi qua chỗ bảng ấy không liệt kê (VERDICT lượt 6, hướng 3:
    bốn qua cả hai ca r6, D và toàn suite, ba qua hai ca r6 và D; bảng đối chiếu của cùng VERDICT ghi "6" — r7 theo
    danh sách tường minh ở hướng 3) — nhánh cũ, hỏi/đọc lại có điều kiện, cú pháp phép tách — và trên rig r7, một helper dựng đúng theo HINT lượt 6 — tức ba chỗ ấy đã được
    vá — vẫn để lọt 34 biến thể trái Q-A (bảng 9 dòng 7). Nên r7 không vá theo ô được chỉ mà đếm lại từ ĐƯỜNG:
    · **Đường** (theo mã nền `launcher.py:650–664` và Q-A): phép hỏi H chạy đúng một lần rồi rẽ nhánh — tệp có ⇒
      phép đọc cũ **Đ0**; tệp vắng ⇒ bước kill cũ **K0**; ESRCH ⇒ `False`; `OSError` khác ⇒ phép đọc mới **Đ**, đọc
      được thì kết quả theo trạng thái, không đọc được hay nội dung hỏng thì bước kill mới **K**; ngoại lệ ngoài họ
      `OSError` ⇒ thoát nguyên. Năm tầng H, Đ0, K0, Đ, K là năm CỘT. Nhánh Windows và Darwin: ngoài phạm vi (Q-A.6).
    · **Hàng** — R1–R5 như bảng r6, cộng **R0** "không lỗi": phép của tầng trả bình thường (hỏi: tệp có hoặc tệp
      vắng; đọc: nội dung đọc được, trạng thái `Z` hoặc không; kill: thành công).
    · **Hướng** — ô "phải xử lý": thoát, sai; ô "phải thoát nguyên": bắt, bọc, và (r7) **thay thế** — ném một đối
      tượng MỚI không có `from` (chỉ mang `__context__`). Hướng thay thế không có loại ghi nhận, THEO THIẾT KẾ: tính
      `__context__` đã bị bác vì tự cấp tín dụng giả (bảng 8 dòng 6). Bản vá thay thế vẫn làm ca đỏ (lỗi vô can),
      nên không lọt nghiệm thu; nó chỉ không phân hạng được thành "giết thật" nếu là một mục đột biến.
    · **Ba trục vuông góc**: **C** đếm (hỏi, đọc, kill) × đường; **S** cú pháp phép tách (`comm` chứa `)` và khoảng
      trắng) × {Đ0, Đ}; **N** nơi gọi `_con_song` (năm nơi, §2).
    Mỗi ô ghi (i) Q-A yêu cầu gì; (ii) đầu vào; (iii) đóng bằng gì — một dòng B5 (mục `DOT_BIEN`, răng BỀN: đo lại ở
    mỗi lượt `--dot-bien`) hoặc MỘT biến thể của phép (E) ở B5 (tập lệnh bằng chứng cục bộ, đo một lần trước merge;
    tên biến thể dưới đây là tên trong rig r7, executor đặt tên của mình và khai ánh xạ). Mười lăm ô của bảng r6 giữ
    nội dung như trên; bảng dưới chỉ thêm cho chúng hàng R0 và hai hướng bọc, thay thế.

    | ô | (i) Q-A yêu cầu | (ii) đầu vào | (iii) đóng bằng (hướng: dòng B5, hoặc E = biến thể của phép (E)) |
    |---|---|---|---|
    | R0-H | hỏi một lần; tệp có ⇒ Đ0, tệp vắng ⇒ K0 (Q-A.1, .3) | tệp có: `B2-nhanh-cu song` và mọi đầu vào Đ0; tệp vắng: `B2-nhanh-cu vang*`, `B3-da-wait` | tệp có sai (bỏ đọc, đi kill): E `h_co_bo_doc` · tệp vắng sai (⇒ `False`, không kill): (m3) |
    | R0-Đ0 | đọc được: `Z` ⇒ `False`, không `Z` ⇒ `True` (nguyên xi) | `B2-nhanh-cu song`; lời gọi đường cũ của `B3-zombie` | không-`Z` sai: E `d0_ok_khongZ_sai` · `Z` sai: E `d0_ok_Z_sai` |
    | R0-K0 | `kill` thành công ⇒ `True` (nền, Linux) | `B2-nhanh-cu vang` | sai: E `k0_ok_sai` |
    | R0-Đ | đọc được: `Z` ⇒ `False`, không `Z` ⇒ `True` (Q-A.4) | `B2-eacces`, `B2-eio`, `B2-eperm-hoi`, `B2-dem-doc 1`, `2`; hai lời gọi đường mới của `B3-zombie` | không-`Z` sai: E `d_ok_khongZ_sai` · `Z` sai: E `d_ok_Z_sai` (bỏ đọc: (c), tính ở trục C) |
    | R0-K | `kill` thành công ⇒ `True` (Q-A.4) | `B2-doc-hong`, `B2-parse`, `B2-dem-doc 3`, `B2-pid-du-phong song` | sai: E `k_ok_sai` (không gọi kill: (k1), tính ở trục C) |
    | R1-Đ0 | ESRCH ở phép đọc cũ ⇒ `False` | `B2-nhanh-cu ESRCH` | thoát: E `d0_ESRCH_thoat` · sai: E `d0_ESRCH_sai` |
    | R2-Đ0 | `OSError` khác ở phép đọc cũ ⇒ `False` | `B2-nhanh-cu EACCES`, `EIO`, `EPERM` | EACCES thoát: E `d0_EACCES_thoat` · EACCES sai: (m1) · EIO thoát / sai: E `d0_EIO_thoat` / `d0_EIO_sai` · EPERM thoát / sai: E `d0_EPERM_thoat` / `d0_EPERM_sai` |
    | R3-Đ0 | nhóm phân tích ở nhánh cũ ⇒ `False` | `B2-nhanh-cu p1` (`ValueError` tự nhiên), `p3` (`IndexError` tự nhiên), `p4` (`UnicodeDecodeError` do seam) | `ValueError` thoát / sai: E `d0_value_thoat` / `d0_value_sai` · `IndexError` thoát / sai: E `d0_index_thoat` / `d0_index_sai` · `UnicodeDecodeError` thoát / sai: E `d0_decode_thoat` / `d0_decode_sai` |
    | R4-Đ0 | thoát nguyên | `B2-nhanh-cu exception` | bắt: E `d0_exception_bat` · bọc: E `d0_exception_boc` · thay thế: E `d0_exception_thaythe` |
    | R5-Đ0 | thoát nguyên | `B2-nhanh-cu tin-hieu` | bắt: (m2) · bọc: E `d0_tin-hieu_boc` · thay thế: E `d0_tin-hieu_thaythe` |
    | R1-K0 | ESRCH ở `kill` ⇒ `False` | `B2-nhanh-cu vang-da-wait` (ESRCH thật, observer ghi lại) | thoát: E `k0_ESRCH_thoat` (và (l22) khi khối kill còn dùng chung) · sai: E `k0_ESRCH_sai` |
    | R2-K0 | EPERM ⇒ `True`; EIO ⇒ `False` | `B2-nhanh-cu vang-eperm`, `vang-eio` | EPERM thoát / sai: E `k0_EPERM_thoat` / `k0_EPERM_sai` ((l23) khi dùng chung) · EIO thoát / sai: E `k0_EIO_thoat` / `k0_EIO_sai` ((l24) khi dùng chung) |
    | R3-K0 | thoát nguyên | `B2-nhanh-cu vang-index`, `vang-value`, `vang-decode` | mỗi thành viên — bắt: E `k0_<tv>_bat` ((l27)–(l29) khi dùng chung) · bọc: E `k0_<tv>_boc` · thay thế: E `k0_<tv>_thaythe` |
    | R4-K0 | thoát nguyên | `B2-nhanh-cu vang-exception` | bắt: E `k0_exception_bat` ((l26) khi dùng chung) · bọc: E `k0_exception_boc` · thay thế: E `k0_exception_thaythe` |
    | R5-K0 | thoát nguyên | `B2-nhanh-cu vang-tin-hieu` | bắt: E `k0_tin-hieu_bat` ((l25) khi dùng chung) · bọc: E `k0_tin-hieu_boc` · thay thế: E `k0_tin-hieu_thaythe` |
    | 15 ô r6, hướng bọc | thoát nguyên | như bảng r6 | R4-H: (l9) · R3-H ×3, R5-H: E `h_<tv>_boc` · R4-Đ, R5-Đ: E `d_<tv>_boc` · R3-K ×3, R4-K, R5-K: E `k_<tv>_boc` |
    | 15 ô r6, hướng thay thế | thoát nguyên | như bảng r6 | R3-H ×3, R4-H, R5-H: E `h_<tv>_thaythe` · R4-Đ, R5-Đ: E `d_<tv>_thaythe` · R3-K ×3, R4-K, R5-K: E `k_<tv>_thaythe` |

    `<tv>` là tên thành viên: `index`, `value`, `decode`, `exception`, `tin-hieu`. "Khi khối kill còn dùng chung":
    (l22)–(l29) sửa khối kill của nền, mà ở ứng viên nháp khối ấy phục vụ cả K lẫn K0; đo trên rig r7, A2 của (l22),
    (l23), (l24), (l27), (l28), (l29) chết đúng lý do ở tiểu nhãn `vang-*` tương ứng (bảng 9 dòng 2). Bản vá TÁCH khối
    K0 ra riêng thì chỉ biến thể E của cột K0 đo được nó.

    **Trục C — đếm × đường** (quy ước đếm ở §7; "—" nghĩa là Q-A không quy định, ca không đòi):

    | đường | hỏi | đọc | kill | đầu vào đo | đóng bằng |
    |---|---|---|---|---|---|
    | H: ESRCH ⇒ `False` | 1 | — | — | `B1` (cộng dồn theo lời gọi) | hỏi lại khi ESRCH: (m4) |
    | H: ngoại lệ ngoài họ `OSError` thoát | 1 | — | — | `B2-tin-hieu hoi`, `B2-exception hoi` (seam `stat`); `B2-thoat-parse hoi-*` (seam `exists`) | hỏi lại sau khi bắt: E `h_thoat_hoi_lai` |
    | Đ0: tệp có | 1 | 1 | 0 | `B2-dem-lan` (hỏi; đọc ≤ 1), `B2-nhanh-cu` phần Đ0, lời gọi đường cũ của `B3-zombie` | hỏi hai lần: (f) · đọc hai lần: E `d0_doc_hai_lan` · gọi kill: E `d0_them_kill` |
    | K0: tệp vắng | 1 | 0 | 1 | `B2-nhanh-cu` phần K0 | hỏi hai lần: E `k0_hoi_hai_lan` · đọc thêm: E `k0_them_doc` · kill hai lần: E `k0_kill_hai_lan` (không kill: (m3), tính ở R0-H) |
    | Đ: đọc được | 1 | 1 | — | `B2-eacces`, `B2-eio`, `B2-eperm-hoi`, `B2-dem-doc 1`, `2`, hai lời gọi đường mới của `B3-zombie` | hỏi lại khi `OSError` khác EACCES: E (bản vá sai của lượt 6) · đọc hai lần: (j1) · không đọc: (c) |
    | Đ → K: đọc lỗi hay hỏng | 1 | 1 | 1 | `B2-doc-hong`, `B2-parse`, `B2-dem-doc 3`, `B2-pid-du-phong`, tiểu nhãn `kill`/`kill-*` của ba nhãn sentinel | hỏi lại: E `k_hoi_hai_lan` · đọc lại: (j2) — thêm E "đọc lại chỉ khi EPERM" (bản vá sai của lượt 6) · kill hai lần: (k5) — thêm E `k_kill_lai_khi_doc_EPERM` · không gọi kill: (k1) |

    Hỏi, đọc hay gọi kill lại CÓ ĐIỀU KIỆN theo lớp ngoại lệ không cần hạng mục riêng: phép đếm đứng ở MỌI đầu vào
    của đường, nên bản vá chỉ lặp lại khi gặp lớp X chết ở đầu vào mang lớp X (đo: ba biến thể có điều kiện của lượt
    6 và r7, bảng 9 dòng 6 và 11). Giới hạn: lớp X không có đầu vào nào (errno thứ tư, lớp con cụ thể) ⇒ KHÔNG ĐO
    ĐƯỢC, như mục 3 và 5 của danh sách bất khả thi dưới đây.

    **Trục S — cú pháp phép tách.** Đầu vào: một zombie thật có `comm` = `x) R (y`, nội dung
    `<pid> (x) R (y) Z …`; chỉ phép tách theo dấu `)` CUỐI mới đọc ra `Z`. S-Đ: hai lời gọi đường mới của `B3-zombie`
    (seam EACCES ở `stat`), đóng bằng (m5). S-Đ0 (r7): lời gọi đường cũ của `B3-zombie` (không seam lỗi, chỉ đếm),
    đóng bằng E `d0_tach_ngoac_dau`.

    **Trục N — nơi gọi** (§2): `:607` (`_con_song_dung_khoa`) — đo qua `B1` (trực tiếp và qua `_giet_rieng`),
    `B3-zombie`, và `B3b-giet-cay` (`_giet_cay` → `_con_lai` → `:607`); `:857`, `:882` (`_giet_windows`) — nhánh
    Windows, ngoài phạm vi (Q-A.6); `:1020`, `:1039` (`_giet_cay` khi `_con_lai` trả `None`, tức không đo được cây)
    — **không đầu vào nào đi qua**: KHÔNG ĐO ĐƯỢC ở packet này. Hai nơi ấy chỉ đọc kết quả boolean nên các đường TRONG
    `_con_song` là một; thứ chưa đo là hệ quả 124/125 đi qua riêng hai nơi ấy.

    **Kiểm đếm bảng mở rộng** (đếm từ bảng; biến thể và kết quả đo ở bảng 9): 30 ô (6 hàng × 5 tầng), ô nào cũng
    có đầu vào. **129 hạng mục**:
    · 95 hạng mục thoát/sai/bắt/bọc = 53 ở 15 ô r6 (42 theo cách đếm của r6, cộng 11 hướng bọc) + 42 ở 15 ô mới
      (hàng R0: 8; cột Đ0: 18; cột K0: 16). Có dòng B5: **45** (42 của r6, cộng (m1), (m2), (m3)). Có biến thể E: **50**
      (11 hướng bọc cũ, cộng 39 hạng mục mới).
    · 19 hạng mục thay thế (H 5, Đ 2, K 5, Đ0 2, K0 5): 19 biến thể E, kỳ vọng ca ĐỎ bằng lỗi vô can.
    · 13 hạng mục đếm (trục C: hỏi trên 6 đường, đọc trên 4, kill trên 3): 5 có dòng B5 ((m4); (f); (j1) cùng (c);
      (j2); (k1) cùng (k5)), 8 có biến thể E (một trong số ấy là bản vá sai của lượt 6).
    · 2 hạng mục cú pháp: (m5) và một biến thể E.
    Tổng: 54 dòng B5 phủ 51 hạng mục (ba cặp dòng chung hạng mục: (l15)/(l16), (c)/(j1), (k1)/(k5)); 78 hạng mục có
    biến thể E. Không hạng mục nào chỉ có lời văn. Đo trên rig r7 (bảng 9 dòng 2 và 6, ba Python): 55/55 cặp của 54
    dòng được chấp nhận; 87 biến thể E có kỳ vọng "chết" hay "đỏ" đều đúng kỳ vọng — 78 biến thể hạng mục, 5 bản vá
    sai khác của lượt 6 (trùng (m1)–(m5)), 2 biến thể lặp có điều kiện, 2 đối chứng của luật `B2-parse` — và hai đối
    chứng kỳ vọng sống thì sống.

    **Ô hoặc phần của ô bất khả thi / KHÔNG ĐO ĐƯỢC — mỗi cái kèm lý do và phép đo** (không ô nào bị bỏ trống
    mà không nói):
    1. R3-H tại seam `Path.stat`, thành viên `ValueError` và `UnicodeDecodeError`: **bất khả thi** ở seam ấy —
       `exists()` nuốt chúng trước khi tới launcher (bảng 7, ba bản Python, 16:20:07Z 29-09). Đo được ở seam
       `Path.exists`, nên ba đầu vào của R3-H dùng seam đó. `IndexError` đo được ở cả hai seam; chọn `Path.exists`
       cho đồng nhất.
    2. R3-H và R3-K: **KHÔNG ĐO ĐƯỢC** rằng hệ điều hành hay `pathlib` thật có bao giờ sinh nhóm phân tích ở
       hai tầng ấy. Nguồn tự nhiên chưa biết, sentinel do ca dựng; ô đo hợp đồng "thoát nguyên", không đo tần suất.
    3. R2 ở cả ba tầng: errno là tập MỞ. EACCES, EPERM, EIO là ba đại diện; bản vá nhận đúng ba errno ấy và
       từ chối errno thứ tư (ví dụ ENOMEM) qua nghiệm thu. **KHÔNG ĐO ĐƯỢC** cho errno thứ tư trở đi. Phân nhánh
       theo errno (danh sách trắng hai hoặc ba errno; EPERM riêng) đã có đột biến: (l4), (l5), (l11), (l12), (l13).
    4. R2-K, thành viên EACCES: gộp vào EPERM — `PermissionError` là lớp chung của hai errno và mệnh đề bắt
       giống hệt; phép đo `os.kill(pid, 0)` trả EACCES trên kernel thật: **KHÔNG ĐO ĐƯỢC** (chưa thử).
    5. Lớp ngoại lệ ngoài năm hàng: con của `OSError` như `TimeoutError`, `InterruptedError`, `BlockingIOError`
       đi cùng R2 (mệnh đề `OSError`); `MemoryError`, `RecursionError`, `TypeError` đi cùng R4; `SystemExit`,
       `GeneratorExit` đi cùng R5. Không có đầu vào riêng — bộ tương đương theo LỚP CHA mà mọi mệnh đề tự
       nhiên bắt; đột biến liệt kê tên một lớp con cụ thể (ví dụ `except (OSError, MemoryError)`): **KHÔNG ĐO ĐƯỢC**.
    6. Mở rộng phạm vi khối `try` sang thêm câu lệnh (bọc luôn `kill` vào khối đọc): không có dạng tự nhiên đã
       biết cho đường lỗi này; hệ quả của nó — nhóm phân tích bị bắt ở tầng K — đã đo qua R3-K.
    7. (r7) R2-K0, thành viên EACCES: gộp vào EPERM như R2-K (mục 4), cùng lý do.
    8. (r7) Cột Đ0 dùng MỘT payload cho mỗi thành viên nhóm phân tích (`p1` rỗng cho `ValueError`, `p3` không khoảng
       trắng cuối cho `IndexError`); `p2` và payload thứ hai của `p3` không lặp lại ở Đ0. Hình dạng "kiểm tra dữ liệu
       thay cho bắt ngoại lệ" ở nhánh cũ (như (l16) ở nhánh mới): chưa có biến thể — **KHÔNG ĐO ĐƯỢC**; nhánh cũ phải
       giữ nguyên xi nên bản vá không có lý do tự nhiên để viết lại phép tách của nó, nhưng đó là suy luận, không phải
       phép đo.
    9. (r7) errno thứ tư và lớp con cụ thể ở cột Đ0 và K0: cùng giới hạn như mục 3 và 5.
    10. (r7) Trục N, `:1020` và `:1039`: **KHÔNG ĐO ĐƯỢC** (xem trục N ở trên).
    11. (r7) Hướng thay thế: không có loại ghi nhận theo thiết kế (xem "Hướng" ở trên). Đo trên rig r7: cả 19 biến
       thể thay thế làm ca đỏ bằng `RuntimeError` vô can ở A1, W1 và W0 (bảng 9 dòng 6) — tức không lọt nghiệm thu;
       phân hạng "giết thật" cho hướng này: bất khả thi theo thiết kế, không phải thiếu đo.

    **Bộ tương đương và đầu vào không có đột biến độc chiếm (yêu cầu (b) của r6).** Trên rig r6 (bảng 8) cho mỗi
    đột biến chạy TỪNG nhãn riêng lẻ và ghi tiểu nhãn chết đầu tiên: 49 đột biến cho 37 chữ ký khác nhau; 11 bộ
    tương đương theo tiểu nhãn gồm 23 đột biến — (d1, l3), (d2, l14), (g2, l11), (h1, l9), (i, l15, l21),
    (k3, l23), (k4, l24), (l4, l5), (l12, l13), (l17, l18), (l19, l20). (Nói rõ ở r7, theo cross-review lượt 6: bộ
    số 37 / 11 / 23 chỉ tái lập được với cách cài (g1) của rig r6, tức đổi CẢ nhóm phân tích sang `False` — chạm thêm
    ô R3-Đ của (i); với (g1) chỉ đổi mệnh đề `OSError`, đúng ánh xạ "R2-Đ EACCES sai", reviewer đo ra 36 chữ ký, 12
    bộ / 25 đột biến, bộ thêm là (g1, l10).) Hai đột biến cùng bộ luôn là hai HƯỚNG
    của cùng một thành viên (thoát và sai, hoặc bắt và bọc), cùng chết ở một tiểu nhãn nhưng ở hai loại
    assertion khác nhau (đã đối chiếu thông điệp A1/W1 của từng bộ trên rig, 16:46Z–16:48Z 29-09): tiểu nhãn không
    tách được chúng, LOẠI assertion tách được, nên log phải ghi loại (xem trên) và A1/W1 phải cùng loại với dòng.
    **Đơn vị không có dòng B5 nào lấy làm đích** (đếm trên 36 đơn vị của bảng tiểu nhãn r6; đơn vị r7 thêm, nếu có,
    ghi ở mô tả nhãn của chúng): `B2-dem-doc`
    tiểu nhãn `2` (`stat` EIO + đọc thật; mọi cách tự nhiên đọc hai lần đều chết ở `1` hoặc `3` trước),
    `B3-song` (đối chứng dương, không seam) và `B3-da-wait` (PID đã `wait`, không seam). Đo trên rig r6 khi chạy
    riêng từng nhãn: `B2-dem-doc 2` vẫn bị (d1) và (l3) làm chết (assertion EIO của nó hoạt động, nhưng đó là
    đầu vào của ô R2-H); `B3-da-wait` KHÔNG bị đột biến nào làm chết đúng lý do — (l22) chỉ làm nó chết VÔ CAN
    (A2 của (l22): khi nới `B2-pid-du-phong`, ESRCH THẬT thoát ở `B3-da-wait`, nơi không có observer, nên là
    `ProcessLookupError` vô can chứ không phải `TinHieuChotCa`; đo lại ở cross-review lượt 6); `B3-song` cũng
    KHÔNG đột biến nào của B5 làm chết. Răng RIÊNG của ba đơn vị này — một đột
    biến lấy đúng chúng làm đích — chưa được đo: **KHÔNG ĐO ĐƯỢC** ở packet này; chúng vẫn được khoá bằng
    assertion và bằng phép D (control bỏ đơn vị ấy đỏ), và đột biến giết chúng nếu có nằm trong 174 mục cũ, không
    đo ở đây. r5 còn hai đơn vị nữa trong tình trạng ấy (`B2-parse p2`, và payload thứ hai của `p3` dùng chung
    tiểu nhãn `p3`); r6 cho `p2` một dòng đích (l16) và giữ payload thứ hai của `p3` chung tiểu nhãn với payload
    đầu, không tách. **(r7)** Trên rig r7 (helper r7, 55 đơn vị; (g1) chỉ đổi mệnh đề `OSError`; bảng 9 dòng 8):
    54 dòng cho **40** chữ ký, **13** bộ / **27** đột biến — (c, l1), (d1, l3), (d2, l14), (g1, l10), (g2, l11),
    (h1, l9), (i, l15, l21), (j2, k1), (l12, l13), (l17, l18), (l19, l20), (l2, m4), (l4, l5). So với các bộ của r6:
    (k3, l23) và (k4, l24) tách ra, vì (l23), (l24) sửa khối kill dùng chung nên chết thêm ở `vang-eperm`,
    `vang-eio` còn (k3), (k4) thì không; ba bộ mới (c, l1), (j2, k1), (l2, m4) do quy ước đếm r7 (cùng tiểu nhãn,
    khác loại assertion). Reviewer lượt 6 đo trên helper theo HINT cũng ra 40 / 13 / 27 nhưng với các bộ KHÁC —
    (k3, l23), (k4, l24) thay cho (c, l1), (j2, k1): tổng trùng không chứng minh thành phần trùng. Đơn vị không có
    dòng B5 nào giết bằng `TinHieuChotCa` khi chạy riêng nhãn, trên 55 đơn vị của r7: **9** — `B2-nhanh-cu` `EIO`,
    `ESRCH`, `EPERM`, `p1`, `p3`, `p4`, `exception`, cùng `B3-song` và `B3-da-wait` (vẫn chỉ (l22) chết vô can ở
    đó); `B2-dem-doc 2` nay bị (d1) và (l3) giết. Bảy đơn vị của `B2-nhanh-cu` có biến thể E giết đúng lý do (đo
    một lần); `B3-song` và `B3-da-wait` không có biến thể E nào lấy làm đích — răng riêng: KHÔNG ĐO ĐƯỢC. Số bộ là
    số ĐO trên một cách cài, không suy từ văn bản (xem đính chính sau bảng 8 về (g1)).

    **Bảng tiểu nhãn — danh sách ĐỘC LẬP các đơn vị assertion, thứ tự cố định** (nguồn của phép quan sát D
    ở B5; viết ở đây, không suy từ cấu hình của helper). Nhãn không liệt kê ở đây (`B1`, `B2-eacces`,
    `B2-eio`, `B2-eperm-hoi`, `B2-dem-lan`, `B3-song`, `B3-da-wait`, `B3-zombie` trong `t156_...`; `B3b-giet-cay`
    trong `t157_...`) không có tiểu nhãn, mỗi nhãn là một đơn vị:

    | nhãn | tiểu nhãn theo thứ tự | số đơn vị |
    |---|---|---|
    | `B2-doc-hong` | `EACCES`, `EIO`, `ESRCH`, `EPERM` | 4 |
    | `B2-tin-hieu` | `hoi`, `doc`, `kill` | 3 |
    | `B2-exception` | `hoi`, `doc`, `kill` | 3 |
    | `B2-thoat-parse` | `hoi-index`, `hoi-value`, `hoi-decode`, `kill-index`, `kill-value`, `kill-decode` | 6 |
    | `B2-parse` | `p1`, `p2`, `p3`, `p4` | 4 |
    | `B2-dem-doc` | `1`, `2`, `3` | 3 |
    | `B2-pid-du-phong` | `song`, `da-wait`, `eperm`, `eio` | 4 |
    | `B2-nhanh-cu` (r7) | `song`, `EACCES`, `EIO`, `ESRCH`, `EPERM`, `p1`, `p3`, `p4`, `tin-hieu`, `exception`, `vang`, `vang-da-wait`, `vang-eperm`, `vang-eio`, `vang-tin-hieu`, `vang-exception`, `vang-index`, `vang-value`, `vang-decode` | 19 |

    Tổng: 16 nhãn của `t156_...` + 1 của `t157_...` = 17 nhãn; tám nhãn có tiểu nhãn gồm 46 đơn vị; các
    nhãn còn lại (tám trong `t156_...`, một trong `t157_...`) mỗi nhãn một đơn vị ⇒ 46 + 9 = **55 đơn vị**
    (HINT lượt 6: 17 nhãn, 32 + 9 = 41; r6: 16 nhãn, 27 + 9 = 36). Đo trên rig r7 (bảng 9 dòng 4): 17 nhãn, 46 tiểu
    nhãn, 55 đơn vị.

    Bốn điều r3–r5 đã đo là sai nếu làm tắt, một điều thứ năm r6 thêm, và một điều thứ sáu r7 thêm: (1) EACCES ở tầng đọc **không đại
    diện** cho họ `OSError` — một bản chỉ bắt `PermissionError` ở tầng đọc qua cả hai ca r3 (bảng 5); (2) ESRCH ở
    tầng hỏi **không thay** ESRCH ở tầng đọc, kỳ vọng ngược nhau; (3) sentinel `RuntimeError` **không thay**
    sentinel `KeyboardInterrupt` ở tầng đọc; (4) `True` trên PID sống **không chứng minh** đã hỏi PID (bảng 6):
    phải có PID đã `wait` (kết quả `False`), có quan sát đúng lời gọi `kill(pid, 0)`, và có kết quả EPERM/EIO của
    chính lời gọi ấy; (5) **một sentinel của nhóm này không đại diện cho nhóm khác và một tầng không đại diện
    cho tầng khác** — `RuntimeError` ở tầng hỏi không thay `IndexError`/`ValueError`/`UnicodeDecodeError` ở tầng
    hỏi (bản HINT lượt 5 qua hai ca r5 và phép D mà vẫn nuốt `IndexError`), và mọi sentinel ở tầng hỏi hay đọc
    không thay cho tầng kill; (6, r7) **đường mới không đại diện cho nhánh cũ, khối kill dùng chung không đại diện
    cho khối kill tách riêng, và phép đếm ở vài nhãn không đại diện cho phép đếm trên mọi đường** — một helper dựng
    đúng theo HINT lượt 6 để lọt 34 biến thể trái Q-A (bảng 9 dòng 7). Đây là chốt của hợp đồng Q-A, không phải lời khai rằng kernel thật đã sinh các lỗi
    ấy. Handoff phải ghi từng đầu vào và nhãn giết (kèm tiểu nhãn và loại assertion).
- **B3 (mục 2) — đối chứng dương, và zombie chưa `wait`.** Không seam: `_con_song(os.getpid())` ⇒
  `True` (nhãn `B3-song`); `_con_song` trên PID con đã `wait` ⇒ `False` (nhãn `B3-da-wait`). Rồi một
  con thật, session riêng, SIGTERM thật,
  đọc `/proc/<pid>/stat` bằng phép đọc **độc lập với launcher** cho tới khi thấy `Z`, **chưa `wait`**;
  đặt seam EACCES chỉ ở `Path.stat` của PID ấy (để `read_text` thật vẫn đọc được): `_con_song` và
  `_con_song_dung_khoa` đều phải `False`. Nhãn `B3-zombie`. **(r7)** Con đặt `comm` = `x) R (y` bằng
  `prctl(PR_SET_NAME)` TRƯỚC khi nhận SIGTERM, và ca xác nhận bằng phép đọc độc lập rằng `(x) R (y)` có trong
  `/proc/<pid>/stat` (không có ⇒ ném lỗi thường, không dùng `bang`): nội dung khi ấy là `<pid> (x) R (y) Z …`,
  chỉ phép tách theo dấu `)` CUỐI mới đọc ra `Z` (Q-A.4 "đọc được và trạng thái là `Z` ⇒ `False`"). Hai lời gọi
  đường mới đếm (hỏi, đọc) cộng dồn (1, 1), (2, 2). **(r7) Lời gọi thứ ba, đường CŨ**, trên cùng zombie ấy, sau khi
  gỡ seam EACCES: seam chỉ ĐẾM (`stat` và `read_text` thật) và observer `os.kill(pid, 0)` chuyển tiếp thật —
  `exists()` đúng nên đi nhánh tệp có (Đ0): `_con_song` phải `False`, hỏi 1, đọc 1, kill 0. Lời gọi này là đầu
  vào của ô R0-Đ0 (`Z` đọc được) và S-Đ0 (bảng không gian mở rộng); cùng nhãn `B3-zombie`, không tiểu nhãn, xếp
  SAU các assertion của hai lời gọi đường mới.
  **ĐỎ khi:** đột biến bỏ phép đọc nội dung trên đường lỗi mới, rơi thẳng về `kill(pid, 0)` ⇒ `True`; hoặc
  đường mới tách theo dấu `)` ĐẦU TIÊN ⇒ đọc ra `R`, trả `True` (dòng (m5); đo ở cross-review lượt 6: qua hết
  hai ca r6, D và toàn suite vì mọi `comm` thật trong r6 không có `)`); hoặc (r7, biến thể E) nhánh cũ tách theo
  dấu `)` đầu tiên (`d0_tach_ngoac_dau`) hay bỏ trạng thái khi đọc được (`d0_ok_Z_sai`) — hai biến thể này lọt
  helper dựng theo HINT (bảng 9 dòng 7) vì ở đó `B3-zombie` chỉ gọi đường mới.
  B3 cũ của r1 (chỉ PID đã `wait`) giữ làm đối chứng nhưng KHÔNG đủ: nó xanh với bản HẸP r1.
- **B4 (mục 2) — nền.** Ngoài Linux (`LA_WINDOWS`, Darwin) hai ca **trả chuỗi lý do** (BỎ QUA có khai
  theo quy ước sẵn của tệp), không trả QUA: nhánh `/proc` không tồn tại ở đó.
  **Hệ quả lên sàn đột biến Windows (r7, cross-review lượt 6).** Mỗi dòng B5 nhắm hai ca này thành KHÔNG ĐO
  ĐƯỢC trên Windows mà vẫn nằm trong mẫu của `_dot_bien_du_san` (`TY_LE_DOT_BIEN_TOI_THIEU_PHAN_MUOI = 7`: ít
  nhất 70 % mục phải đo được, không thì `--dot-bien` in `DUOI SAN` và rc=1 — chính bước `Tu dot bien` của
  `launcher-windows.yml` mà land_obligation đọc). Ước lượng TĨNH (cận dưới: ca trả chuỗi ở đầu thân dưới
  `if LA_WINDOWS` / `os.name == 'nt'` / `platform.system() != 'Linux'`, cộng mục mang giới hạn `('posix', …)`):
  nền 11/177 mục không đo được; sau r6 60/226 (73,45 %, trần 67 ⇒ biên 7); với lớp (m) 65/231 (71,86 %, trần 69
  ⇒ biên 4). Mỗi dòng Linux-only thêm về sau ăn khoảng 0,7 mục biên. Executor khai phép tính này (lệnh + số)
  trong handoff; số THẬT trên Windows: KHÔNG ĐO ĐƯỢC trước merge (Q4) — đọc dòng `DOT BIEN: …` của job Windows
  ở lượt push master và coi `DUOI SAN` là đỏ của packet.
  **Đo lại ở r7 và biên còn lại** (tập lệnh ước lượng của reviewer lượt 6 chạy trên tệp test đã lắp của rig r7,
  01:41:30Z 30-09; bảng 9 dòng 10). Mẫu của sàn là `len(DOT_BIEN) + len(DOT_BIEN_HARNESS)` (runner nền,
  `launcher_test.py:8293`), và dưới sàn thì `--dot-bien` in `!! DUOI SAN` rồi trả 1 (`:8297–8302`). Sau r7 (54 dòng
  mới, như HINT): **65/231 không đo được trên Windows, 71,86 % đo được, trần 69 ⇒ biên 4 mục** — cận dưới tĩnh: ca
  bỏ qua giữa thân không đếm được, nên biên THẬT có thể nhỏ hơn. Thêm n dòng Linux-only nữa: n = 1, 2, 3, 4, 5, 6 ⇒
  biên 3, 2, 2, 1, 0, 0 (vẫn đạt); **n = 7 ⇒ `DUOI SAN`** (69,75 %). Đây là giới hạn CỨNG, đo được, của cách làm
  "thêm một mục đột biến cho mỗi ô": 78 hạng mục của bảng không gian mở rộng không có dòng B5 riêng, và đưa chúng
  vào `DOT_BIEN` sẽ làm Windows rơi xuống dưới sàn ngay (231 + 78 = 309 mục, 65 + 78 = 143 không đo được, còn
  166/309 = 53,72 % đo được — suy bằng số học từ cùng phép đếm, không dựng và không chạy). Vì vậy r7 giữ `DOT_BIEN` ở 54 dòng và đo 78 hạng mục ấy
  bằng phép (E) trong tập lệnh bằng chứng cục bộ (B5); đổi cân bằng này — thêm dòng `DOT_BIEN` cho một số hạng mục
  (tối đa sáu trước khi chạm sàn theo cận dưới), hay cho hai ca chạy nhánh `/proc` trên Windows bằng seam — là
  quyết định của điều phối/chủ kho, r7 không tự chọn.

**Ca `t157_...`**

- **B3b (mục 2) — chốt tiêu thụ `_giet_cay`.** Con thật CÒN SỐNG, session riêng, `khoa` lấy trước seam;
  seam EACCES ở `Path.stat` của PID ấy; gọi `_giet_cay(pid, khoa)` để SIGTERM thật biến con thành
  zombie chưa `wait`; kết quả phải có `tron_ven=True` (phía deadline ánh xạ 124, `launcher.py:1669`).
  Nhãn `B3b-giet-cay`. Dọn PID con và `wait` trong `finally`. Ca này riêng để đột biến (c) ở B5 làm
  **cả hai** ca `t156_...` lẫn `t157_...` đỏ, mỗi ca bằng `TinHieuChotCa` của chính nó.
  **ĐỎ khi:** đột biến bỏ phép đọc nội dung ⇒ `tron_ven=False` ⇒ tương ứng 125 (bảng 2, hàng HẸP r1).

**Các chốt chung**

- **B5 (mục 2) — `DOT_BIEN`: DANH SÁCH CÓ THẨM QUYỀN DUY NHẤT của đột biến mới.** Mọi chỗ khác trong
  đặc tả (kể cả §6) chỉ trỏ về đây; riêng không gian các ĐƯỜNG, bảng không gian mở rộng ở B2 (r7) là bản liệt
  kê có thẩm quyền của các Ô và hạng mục, và mỗi dòng dưới đây thuộc một hạng mục của bảng ấy: 46 dòng ở trục
  "ngoại lệ nào × tầng nào" (kể cả cột Đ0 và hàng R0), 8 dòng ở trục đếm C và cú pháp S ((c), (f), (j1), (j2),
  (k1), (k5), (m4), (m5)); kiểm đếm ở B2. Hạng mục không có dòng ở đây được đo bằng phép (E) bên dưới, KHÔNG
  bằng mục `DOT_BIEN` (sàn Windows, B4). Executor **đếm lại** trên mã thực thi và khai. **Mười ba LỚP**
  đột biến (a)–(m), mỗi lớp trỏ đích là ca mới; số mục `DOT_BIEN` thật là số **dòng biến thể** dưới đây, suy
  ra từ quy tắc ngay sau danh sách (kỳ vọng **năm mươi tư**; r6: bốn mươi chín). Mỗi dòng nêu vị trí mã, hành vi bị đổi, và
  nhãn giết kèm tiểu nhãn mong đợi (tiểu nhãn: bảng ngay sau bảng không gian B2); các dòng (k5), (l1)–(l29) và
  (m1)–(m5) còn nêu LOẠI assertion mà thông điệp chết phải mang (xem "loại assertion" ở B2):
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
  (g) hai dòng, CÙNG vị trí (tầng đọc), hai hành vi — (g1) trả `False` cho mọi lỗi đọc (`OSError`; nói rõ ở r7: rig r6 cài (g1) đổi CẢ nhóm
  phân tích sang `False`, tức chạm thêm ô R3-Đ của (i) — hai cách cài cho hai số bộ tương đương khác nhau, xem
  đính chính sau bảng 8) ⇒ `t156_...` đỏ ở
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

  (k) năm dòng, CÙNG vị trí (chỗ đường đọc lỗi hoặc nội dung hỏng quyết định sống hay chết, Q-A.4), năm hành
  vi — bốn dòng đầu bỏ hoặc bóp méo đúng MỘT chiều của bước PID dự phòng, nên mỗi dòng chết ở một tiểu nhãn kết
  quả riêng của `B2-pid-du-phong`; dòng thứ năm (r6) là trục đếm: (k1) trả `True` ngay, không hỏi `kill(pid, 0)` ⇒ `t156_...` đỏ ở
  `B2-pid-du-phong`, tiểu nhãn `song` (số lời gọi `kill(pid, 0)` bằng 0); (k2) gọi `kill(pid, 0)` đúng một lần
  nhưng BỎ kết quả, luôn trả `True` ⇒ đỏ ở tiểu nhãn `da-wait` (PID đã `wait`, kết quả `True` thay vì `False`;
  số lời gọi bằng 1 nên `song` xanh); (k3) tự xử lý `kill` trên đường lỗi mới, mọi `OSError` kể cả
  `PermissionError` ⇒ `False` ⇒ đỏ ở tiểu nhãn `eperm` (kết quả `False` thay vì `True`); (k4) tự xử lý `kill`
  trên đường lỗi mới, `ProcessLookupError` ⇒ `False` nhưng `OSError` khác ⇒ `True` ⇒ đỏ ở tiểu nhãn `eio` (kết
  quả `True` thay vì `False`); (k5) hỏi `kill(pid, 0)` trong xử lý lỗi đọc RỒI để khối chung hỏi lần nữa (hai lời
  gọi, kết quả vẫn đúng) ⇒ đỏ ở tiểu nhãn `song`, loại `kill count`, bộ đếm bằng 2 — dòng này khác (k1) ở chỗ
  (k1) có 0 lời gọi. Cả bốn dòng đầu đều xanh với hai ca mẫu của r4 (không có nhãn này); không dùng
  `B3-da-wait` (không seam) thay cho PID đã `wait` TRÊN đường lỗi mới. Vì sao bốn dòng chứ không một: HINT
  lượt 4 đề nghị một dòng (k) ở tiểu nhãn `song`; nhưng khi `song` đã giết mutant bằng bộ đếm thì kết quả
  `da-wait`, `eperm`, `eio` không còn mutant nào chạm tới, và tiểu nhãn nào không có mutant độc chiếm thì
  chỉ còn được giữ bởi assertion chứ chưa được đo có răng (đúng chỗ r4 đã nêu cho tiểu nhãn `EIO` của
  `B2-doc-hong`). Đã đo (bảng 6): k2, k3, k4 qua hai ca mẫu của r4 và chết đúng một tiểu nhãn mỗi cái;
  giữ nguyên mọi dòng (a)–(j).

  (l) hai mươi chín dòng (r6), MỘT dòng cho mỗi hướng còn thiếu của bảng không gian ở B2; mỗi dòng ghi ô của bảng
  trong ngoặc vuông, nhãn và tiểu nhãn giết, và loại assertion. Nhóm theo tầng:
  · Tầng H (phép hỏi) —
  (l1) [R2-H] phép hỏi chỉ bắt `ProcessLookupError` (bản vá tối thiểu cho đúng ESRCH), `OSError` khác thoát
  ⇒ đỏ ở `B2-eacces`, loại `seam escaped`;
  (l2) [R1-H] phép hỏi để ESRCH rơi cùng nhánh với `OSError` khác (vào bước đọc, không có nhánh `False` riêng)
  ⇒ đỏ ở `B1`, loại `result True`;
  (l3) [R2-H] phép hỏi cho `PermissionError` vào bước đọc nhưng trả `False` cho `OSError` khác, giữ nhánh ESRCH
  riêng ⇒ đỏ ở `B2-eio`, loại `result False`;
  (l4) [R2-H] phép hỏi chỉ nhận `OSError` mang errno EACCES hoặc EIO (danh sách trắng), errno khác thoát, giữ
  nhánh ESRCH riêng ⇒ đỏ ở `B2-eperm-hoi`, loại `seam escaped`;
  (l5) [R2-H] phép hỏi trả `False` riêng cho errno EPERM, còn lại vào bước đọc ⇒ đỏ ở `B2-eperm-hoi`, loại
  `result False`;
  (l6) [R3-H] phép hỏi thêm `IndexError` vào nhóm bắt ⇒ đỏ ở `B2-thoat-parse`, tiểu nhãn `hoi-index`, loại
  `sentinel identity`;
  (l7) [R3-H] phép hỏi thêm `ValueError` ⇒ đỏ ở `B2-thoat-parse`, tiểu nhãn `hoi-value`, loại `sentinel identity`;
  (l8) [R3-H] phép hỏi thêm riêng `UnicodeDecodeError` ⇒ đỏ ở `B2-thoat-parse`, tiểu nhãn `hoi-decode`, loại
  `sentinel identity`. (Bản
  HINT lượt 5 đề nghị MỘT dòng (h3) gộp `OSError`, `ValueError`, `IndexError` vào phép hỏi; đo trên rig r6 dòng
  ấy chết ở `hoi-index`, cùng chỗ với (l6), nên nó và (l6) là một bộ tương đương theo tiểu nhãn. r6 tách theo
  thành viên để `hoi-value` và `hoi-decode` cũng có đột biến độc chiếm: (l6), (l7), (l8) chết ở ba tiểu nhãn
  khác nhau, thứ tự `index`, `value`, `decode` có chủ ý vì `ValueError` là cha của `UnicodeDecodeError`.)
  (l9) [R4-H] phép hỏi bắt `Exception` rồi ném `RuntimeError` mới bằng `raise … from …` ⇒ đỏ ở `B2-exception`,
  tiểu nhãn `hoi`, loại `seam wrapped`;
  · Tầng Đ (phép đọc) —
  (l10) [R2-Đ] tầng đọc chỉ bắt `ValueError` và `IndexError`, `OSError` thoát ⇒ đỏ ở `B2-doc-hong`, tiểu nhãn
  `EACCES`, loại `seam escaped`;
  (l11) [R1-Đ] tầng đọc chỉ nhận `OSError` mang errno EACCES hoặc EIO ⇒ đỏ ở `B2-doc-hong`, tiểu nhãn `ESRCH`,
  loại `seam escaped`;
  (l12) [R2-Đ] tầng đọc chỉ nhận errno EACCES, EIO hoặc ESRCH ⇒ đỏ ở `B2-doc-hong`, tiểu nhãn `EPERM`, loại
  `seam escaped`;
  (l13) [R2-Đ] tầng đọc trả `False` riêng cho errno EPERM ⇒ đỏ ở `B2-doc-hong`, tiểu nhãn `EPERM`, loại
  `result False`;
  (l14) [R2-Đ] tầng đọc cho `PermissionError` rơi về bước kill nhưng trả `False` cho `OSError` khác ⇒ đỏ ở
  `B2-doc-hong`, tiểu nhãn `EIO`, loại `result False`;
  (l15) [R3-Đ] tầng đọc không bắt `ValueError` (chỉ `OSError` và `IndexError`) ⇒ đỏ ở `B2-parse`, tiểu nhãn
  `p1`, loại `parse error escaped`;
  (l16) [R3-Đ] tầng đọc thay bắt `ValueError` bằng kiểm tra dữ liệu chỉ nhận ra chuỗi rỗng ⇒ `p1` qua, đỏ ở
  `B2-parse`, tiểu nhãn `p2`, loại `parse error escaped`;
  (l17) [R3-Đ] tầng đọc không bắt `IndexError` ⇒ đỏ ở `B2-parse`, tiểu nhãn `p3`, loại `parse error escaped`;
  (l18) [R3-Đ] tầng đọc trả `False` riêng cho `IndexError`, phần còn lại rơi về kill ⇒ đỏ ở `B2-parse`, tiểu
  nhãn `p3`, loại `result False`;
  (l19) [R3-Đ] phép đọc chỉ bắt `OSError` còn biểu thức tách bọc riêng bắt `ValueError` và `IndexError`, nên
  `UnicodeDecodeError` do `read_text` ném thoát ⇒ đỏ ở `B2-parse`, tiểu nhãn `p4`, loại `seam escaped`;
  (l20) [R3-Đ] tầng đọc trả `False` riêng cho `UnicodeDecodeError` ⇒ đỏ ở `B2-parse`, tiểu nhãn `p4`, loại
  `result False`;
  (l21) [R3-Đ] tầng đọc bọc lại `ValueError` tự nhiên thành `RuntimeError` mới bằng `raise … from …` ⇒ đỏ ở
  `B2-parse`, tiểu nhãn `p1`, loại `parse error wrapped`;
  · Tầng K (khối `kill`) —
  (l22) [R1-K] khối `kill` chỉ có mệnh đề `PermissionError`, ESRCH thật thoát ⇒ đỏ ở `B2-pid-du-phong`, tiểu
  nhãn `da-wait`, loại `seam escaped` (đối tượng là ngoại lệ THẬT mà observer đã ghi lại);
  (l23) [R2-K] khối `kill` chỉ có mệnh đề `ProcessLookupError`, EPERM thoát ⇒ đỏ ở `B2-pid-du-phong`, tiểu
  nhãn `eperm`, loại `seam escaped`;
  (l24) [R2-K] khối `kill` bỏ mệnh đề `OSError` (giữ hai mệnh đề kia), EIO thoát ⇒ đỏ ở `B2-pid-du-phong`, tiểu
  nhãn `eio`, loại `seam escaped`;
  (l25) [R5-K] khối `kill` thêm mệnh đề bắt `BaseException` ⇒ đỏ ở `B2-tin-hieu`, tiểu nhãn `kill`, loại
  `sentinel identity`;
  (l26) [R4-K] khối `kill` thêm mệnh đề bắt `Exception` ⇒ đỏ ở `B2-exception`, tiểu nhãn `kill`, loại
  `sentinel identity`;
  (l27) [R3-K] khối `kill` thêm mệnh đề bắt `IndexError` ⇒ đỏ ở `B2-thoat-parse`, tiểu nhãn `kill-index`, loại
  `sentinel identity`;
  (l28) [R3-K] khối `kill` thêm mệnh đề bắt `ValueError` ⇒ đỏ ở `B2-thoat-parse`, tiểu nhãn `kill-value`, loại
  `sentinel identity`;
  (l29) [R3-K] khối `kill` thêm mệnh đề bắt riêng `UnicodeDecodeError` ⇒ đỏ ở `B2-thoat-parse`, tiểu nhãn
  `kill-decode`, loại `sentinel identity`.
  (m) năm dòng (r7, cross-review lượt 6) — cột Đ0 của Q-A.3 và hai trục đếm / cú pháp (xem `B2-nhanh-cu` và
  bảng không gian mở rộng ở B2):
  (m1) [R2-Đ0 EACCES, hướng sai; bản vá chạm cả R1–R3 × Đ0] nhánh cũ: đọc lỗi hay nội dung hỏng ⇒ rơi về
  `kill(pid, 0)` thay vì `False` (hợp nhất hai khối đọc về hướng `kill`) ⇒ đỏ ở `B2-nhanh-cu`, tiểu nhãn `EACCES`
  (đầu vào lỗi đầu tiên của cột Đ0; `song` đứng trước và vẫn đúng), loại `result True`;
  (m2) [R5-Đ0, hướng bắt] nhánh cũ bắt `BaseException` ⇒ đỏ ở `B2-nhanh-cu`, tiểu nhãn `tin-hieu`, loại
  `sentinel identity`;
  (m3) [R0-H, tệp vắng, hướng sai] `exists()` trả `False` ⇒ trả `False`, bỏ `kill(pid, 0)` ⇒ đỏ ở `B2-nhanh-cu`,
  tiểu nhãn `vang`, loại `result False`;
  (m4) [trục C, đường ESRCH, hỏi] ESRCH ở phép hỏi ⇒ hỏi `exists()` lại một lần rồi mới trả `False` ⇒ đỏ ở `B1`,
  loại `stat count`;
  (m5) [trục S, Đ] đường mới tách trạng thái theo dấu `)` ĐẦU TIÊN ⇒ đỏ ở `B3-zombie`, loại `result True`.
  Mỗi dòng (l) là một thay đổi ở một vị trí mã. Dòng (l16) là hình dạng "kiểm tra dữ liệu thay cho bắt ngoại
  lệ" mà Q-A.5 cho phép nhưng chỉ khi nó nhận ra mọi dạng nội dung hỏng. Cả 29 dòng và bảng không gian đều
  đến từ MỘT phép liệt kê trước khi vá (§9), không từ danh sách các finding.

  **Quy tắc mục `DOT_BIEN` (r3; r4 cập nhật cho (d), (e), (g); r5 cho (k); r6 cho (h), (k), (l); r7 cho (m)).**
  (a)–(m) ở trên là mười ba LỚP. Mỗi mục `DOT_BIEN` là một bản sao đột biến có tên riêng và làm đúng một thay đổi ở đúng
  một vị trí mã (một mục ghép hai vị trí thì không tách được vị trí nào bị giết, nên không hợp lệ); hai biến
  thể KHÁC HÀNH VI ở cùng một vị trí (như (g1) và (g2), hay (k1) đến (k5)) cũng là các mục riêng. Vì thế số mục
  `DOT_BIEN` = số **dòng biến thể** ở danh sách trên: (a), (b), (c), (f), (i) mỗi lớp một dòng (5);
  (d), (e), (g), (h), (j) mỗi lớp hai dòng (10); (k) năm dòng (5); (l) hai mươi chín dòng (29); (m) năm dòng
  (5) ⇒ **năm mươi tư mục `DOT_BIEN`**. Dòng (c) làm đỏ hai ca nên mang hai kết quả đích, do đó năm mươi tư dòng
  cho **năm mươi lăm cặp (dòng, ca đích)**. Executor đếm lại trên mã của chính mình và khai từng dòng (một dòng
  không dựng được ở cách triển khai đã chọn phải khai KHÔNG ĐO ĐƯỢC kèm lý do, không lặng lẽ bỏ). Con số "năm
  mươi tư" là kỳ vọng suy ra, không phải danh sách thứ hai: danh sách có thẩm quyền vẫn là (a)–(m) cùng quy
  tắc này. Lịch sử của con số: r2 gọi "bảy mục" và mỗi mục là một mục `DOT_BIEN`; r3 tách "lớp" khỏi "mục"
  (mười lớp, mười hai mục, mười ba cặp đích); r4 giữ mười lớp nhưng lên mười lăm mục vì (d), (e), (g) mỗi lớp
  thành hai dòng (mười sáu cặp đích); r5 thêm lớp (k) — mười một lớp — với bốn dòng: mười chín mục, hai mươi
  cặp đích (HINT lượt 4 đề nghị một dòng (k), tức mười sáu mục và mười bảy cặp; r5 không theo con số ấy, lý do
  ở dòng (k)); r6 thêm dòng (k5) và lớp (l) — mười hai lớp — với hai mươi chín dòng: bốn mươi chín mục, năm mươi
  cặp đích (HINT lượt 5 đề nghị (h3): hai mươi mục, hai mươi mốt cặp; r6 không theo con số ấy, lý do ở
  bảng không gian B2 và ở (l6)–(l8)); r7 thêm lớp (m) — mười ba lớp — với năm dòng: năm mươi tư mục, năm mươi
  lăm cặp đích (cross-review lượt 6: cột Đ0 và hai trục đếm / cú pháp). r7 KHÔNG thêm dòng nào ngoài năm dòng
  của HINT, dù bảng không gian mở rộng có 78 hạng mục không có dòng riêng: dòng Linux-only thứ bảy đã đưa Windows
  xuống dưới sàn (B4); 78 hạng mục ấy được đo bằng phép (E).

  Mỗi đột biến phải chết **bằng `TinHieuChotCa` của đúng ca đích, đúng nhãn — đúng tiểu nhãn khi dòng của nó
  nêu tiểu nhãn (r4) — và đúng loại assertion khi dòng nêu loại (r6)**, không bằng lỗi vô can
  (bài học *"ĐỘT BIẾN BỊ GIẾT KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO"*). Runner hiện có in tên ca kèm
  kiểu ngoại lệ trong ngoặc khi ngoại lệ KHÔNG phải `TinHieuChotCa`, và vẫn cho `OK giet 1/1` — nên
  KHÔNG dùng riêng rc hay chữ `OK` của runner. Phân hạng bằng cách đọc kiểu ngoại lệ, tên ca và nhãn
  (gọi thẳng hàm ca trên bản đột biến để đọc thông điệp `TinHieuChotCa`; runner chỉ in tên ca) và khai
  **ba hạng**: giết thật / tín dụng giả / sống sót, mỗi mục một dòng. Kèm một đối chứng cố ý vô can (ví
  dụ đột biến gây `NameError`) để chứng minh cách phân hạng không cấp tín dụng giả; r6 thêm đối chứng thứ hai
  cho quy tắc nhận ra ngoại lệ tự nhiên của `B2-parse` (một `ValueError` khác đối số phải chết vô can, bảng 8);
  r7 thêm đối chứng thứ ba: `ValueError('substring not found')` CÙNG kiểu CÙNG đối số nhưng ném từ một dòng khác
  dòng biểu thức tách (ví dụ `str.index` trên chuỗi không liên quan trong nhánh xử lý) phải chết vô can (rig r7:
  chết vô can dưới cách so hàm + nội dung, và được ghi NHẦM là `parse error escaped` dưới luật r6 — bảng 9 dòng 5,
  12; nên đối chứng này có răng với chính điều kiện nguồn).
  Hạng "tín dụng giả" gồm mutant chết vì ngoại lệ vô can, và mutant chết bằng `TinHieuChotCa` của một ca KHÁC
  ca đích. Chết ở một nhãn khác của CÙNG ca đích thì không phải tín dụng giả nhưng phải khớp quy tắc nhãn của
  phép (A1) dưới đây.

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
  | A1 | mọi nhãn, đúng thứ tự | mọi assertion của mọi nhãn (kể cả kiểm seam đã chạm và bộ đếm); assertion sai đầu tiên ném | chết bằng `TinHieuChotCa` của ca đích; nhãn báo = nhãn đích, hoặc một nhãn đứng TRƯỚC nhãn đích trong thứ tự thực thi (khai rõ nhãn nào — hợp lệ). Nếu báo ở nhãn đích thì tiểu nhãn báo phải là tiểu nhãn của dòng (khi dòng nêu tiểu nhãn) và loại assertion phải là loại dòng nêu (khi dòng nêu loại; r6) |
  | A2 | mọi nhãn, đúng thứ tự | mọi assertion trừ nhãn đích | KHÔNG đòi gì; khai "sống sót" hoặc "chết ở nhãn Y" (Y là nhãn giết kế tiếp, luôn khác nhãn đích) |
  | W1 | chỉ đầu vào của nhãn đích | chỉ assertion mang nhãn đích | chết bằng `TinHieuChotCa` mà thông điệp mở đầu bằng nhãn đích, rồi đúng tiểu nhãn của dòng khi dòng nêu tiểu nhãn, rồi đúng loại assertion khi dòng nêu loại (r6) |
  | W0 | chỉ đầu vào của nhãn đích (vẫn chạy nguyên) | không assertion nào của nhãn đích; còn lại chỉ lỗi thiết lập và ngoại lệ vô can | sống sót (helper trả về bình thường); bộ đếm seam của nhãn ≥ 1 (chứng tỏ đầu vào ĐÃ chạy) |

  Tiêu chí, mỗi dòng biến thể: **ĐỎ** khi A1 sống sót; khi A1 báo nhãn đứng SAU nhãn đích (nhãn đích
  không còn răng hoặc ánh xạ sai); khi A1 hoặc W1 chết ở nhãn đích nhưng ở tiểu nhãn KHÁC tiểu nhãn của
  dòng (r4: đầu vào của dòng không còn răng riêng, hoặc bị đầu vào khác che); khi A1 hoặc W1 chết đúng nhãn và
  tiểu nhãn nhưng ở loại assertion KHÁC loại dòng nêu (r6: hai hướng của cùng một thành viên dùng chung một
  tiểu nhãn, xem "bộ tương đương" ở B2, nên loại là thứ duy nhất tách chúng); khi W1 không chết đúng nhãn
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
  3. **Đối chiếu.** Tập ghi được phải BẰNG danh sách đơn vị ở "bảng tiểu nhãn" (ngay sau bảng không gian B2:
     55 đơn vị — 17 nhãn, trong đó tám nhãn tách thành 46 tiểu nhãn; HINT lượt 6: 41 / 17 / tám / 32; r6: 36 / 16 /
     bảy / 27), và thứ tự xuất hiện lần đầu của từng đơn
     vị trong mỗi ca phải đúng thứ tự cố định ở §7. Danh sách kỳ vọng viết CỨNG trong tập lệnh bằng chứng
     theo §7, KHÔNG lấy từ cấu hình CHẠY/NỚI của chính helper (lấy từ đó thì D đo helper bằng helper).
     Chỉ ghi seam đã chạm hay nhãn được chọn KHÔNG chứng minh assertion có hoạt động.
  4. **Control (D phải đỏ).** Trên bản sao TEST, không đụng mã sản phẩm: (i) lần lượt làm mặc định NỚI
     chứa từng nhãn trong **17 nhãn** ⇒ D đỏ, báo đúng nhãn thiếu; (ii) lần lượt bỏ assertion của từng
     tiểu nhãn trong **46 tiểu nhãn** của tám nhãn tách được (bỏ MỘT đầu vào, giữ các đầu vào khác của
     cùng nhãn) ⇒ D đỏ, báo đúng tiểu nhãn thiếu. Bản mặc định đúng phải xanh. Kỳ vọng **63 control**
     (17 + 46; HINT lượt 6: 49 = 17 + 32; r6: 43 = 16 + 27) cộng hai lần xanh của bản đúng, và ít nhất sáu phép đảo
     thứ tự hai nhãn (năm phép của r6 cộng `B2-pid-du-phong` với `B2-nhanh-cu`) đều đỏ với tập vẫn đủ.
  5. **Chỗ đặt.** D và control của nó nằm ở tập lệnh bằng chứng cục bộ của executor, như phép A/W: không
     thêm ca đăng ký (vẫn hai ca), không sửa runner `--dot-bien`, không tăng số mục `DOT_BIEN` sản phẩm.
  6. **Nghĩa vụ log.** Lệnh nguyên văn, giờ UTC, rc, dòng xanh của bản đúng cho từng ca, và từng dòng
     control kèm đơn vị thiếu. **Không nhận A1/A2/W1/W0 là đủ** nếu thiếu D, nếu bản đúng đỏ, hoặc nếu
     bất kỳ control nào không đỏ.
  Đã đo, sáu lần:
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
  `missing=[]`, `order=False` (15:35:38Z);
  · phiên soạn r6 (16:46:53Z 29-09, Python 3.12.3; lặp 16:49:13Z ở 3.11.15 và 16:51:06Z ở 3.13.12, cùng kết quả;
  rig sao chép, 36 đơn vị): bản đúng xanh ở cả hai ca; **43 control (16 nhãn + 27 tiểu nhãn) đều đỏ**, mỗi cái
  báo đúng đơn vị thiếu; năm phép đảo thứ tự (`B1` với `B2-eacces`; `B2-thoat-parse` với `B2-exception`;
  `B2-pid-du-phong` với `B3-song`; `B2-dem-doc` với `B2-pid-du-phong`; `B2-eperm-hoi` với `B2-doc-hong`) đều làm
  D đỏ với `missing=[]`, `order=False`.
  · cross-review lượt 6 (00:53Z–00:57Z 30-09, ba Python, rig reviewer cho phương án r7, 41 đơn vị): bản đúng xanh ở
  cả hai ca; **49 control** (17 nhãn + 32 tiểu nhãn) đều đỏ, mỗi cái báo đúng đơn vị thiếu; năm phép đảo thứ tự
  của r6 đều đỏ với `missing=[]`, `order=False`.
  · phiên soạn r7 (01:33:28Z 30-09, Python 3.12.3; lặp 01:41:40Z ở 3.11.15 và 01:43:18Z ở 3.13.12, cùng kết quả; rig
  riêng, helper r7, 55 đơn vị): bản đúng xanh ở cả hai ca (`t156` 54 đơn vị, `t157` 1); **63 control (17 nhãn + 46
  tiểu nhãn) đều đỏ**, mỗi cái báo đúng đơn vị thiếu; sáu phép đảo thứ tự đều đỏ với `missing=[]`, `order=False`
  (bảng 9 dòng 3).
  **CHƯA ĐO:** tập lệnh bằng chứng của executor và D trên mã của executor.

  **(E) Săn theo bảng không gian mở rộng — MỘT biến thể cho mỗi hạng mục không có dòng B5, trong tập lệnh bằng
  chứng cục bộ, KHÔNG vào `DOT_BIEN` (r7).** Vì sao cần: 78 hạng mục của bảng không gian mở rộng không có mục
  `DOT_BIEN` riêng, và không được có (B4: dòng Linux-only thứ bảy đưa Windows xuống dưới sàn). Không có (E) thì răng
  của các hạng mục ấy chỉ là lời văn — đúng loại "danh sách tự liệt kê, cho là hết" mà §9 đếm tới lần thứ bảy.
  1. **Đối tượng.** Với mỗi hạng mục không có dòng B5 (bảng không gian mở rộng, cột (iii) ghi "E"), executor dựng
     MỘT biến thể của CHÍNH ứng viên của mình: một thay đổi ở một vị trí mã, vi phạm hạng mục ấy (chạm thêm hạng
     mục khác thì A1 được báo ở nhãn đứng trước, như một dòng B5 — ví dụ đo được: bản trả `False` cho nội dung đọc
     được ở nhánh cũ chết trước ở `B2-dem-lan`, W1 vẫn chết đúng `B2-nhanh-cu song`). Cộng: bảy bản vá sai của cross-review lượt 6 (năm trùng (m1)–(m5),
     hai cái kia là "hỏi lại khi `OSError` khác EACCES" và "đọc lại chỉ khi EPERM"), biến thể "kill lần hai chỉ khi
     đọc gặp EPERM", hai đối chứng của luật `B2-parse` (khác đối số; cùng đối số khác nguồn), và hai đối chứng phải
     SỐNG: một khối K0 tách riêng mà ĐÚNG ngữ nghĩa nền (chứng tỏ các đầu vào K0 không bắt oan một cách tách hợp
     lệ), và bản danh sách trắng ba errno (giới hạn đã khai ở mục 3 — phải sống, không thì phép đo đang đo thứ khác).
     Trên ứng viên nháp của rig r7 bộ này có 89 biến thể; số của executor có thể khác nếu cấu trúc mã khác (ví dụ
     không có khối kill dùng chung), và executor khai ánh xạ biến thể → hạng mục.
  2. **Đo.** Mỗi biến thể chạy A1, A2, W1, W0 như một dòng B5. Biến thể hướng thoát/sai/bắt/bọc/đếm/cú pháp: tiêu chí
     y hệt tiêu chí của một dòng B5 (A1 chết bằng `TinHieuChotCa` đúng đích hoặc ở nhãn đứng trước; W1 đúng nhãn,
     tiểu nhãn, loại; W0 sống, bộ đếm ≥ 1). Biến thể hướng thay thế: ca ĐỎ ở A1, W1 và cả W0 bằng lỗi vô can (không
     lọt, và nới nhãn không che được); đó là hạng "đỏ vô can theo thiết kế", không tính giết thật. Hai đối chứng
     sống: cả hai ca SONG và D xanh.
  3. **Chỗ đặt và log.** Như D: tập lệnh bằng chứng cục bộ, không thêm ca đăng ký, không sửa runner, không tăng
     `DOT_BIEN`. Log: lệnh nguyên văn, giờ UTC, rc, và mỗi biến thể một dòng (tên, hạng mục của bảng, đích, A1, A2,
     W1, W0, bộ đếm, chấp nhận hay lý do đỏ). **Không nhận bằng chứng B5 là đủ** nếu thiếu (E), hoặc có biến thể
     nào không đúng kỳ vọng.
  4. **Giới hạn khai thẳng.** (E) chạy MỘT lần trước merge; nó không nằm trong `--dot-bien` nên KHÔNG được đo lại ở
     các lượt sau — răng BỀN của 78 hạng mục ấy chỉ là assertion cộng phép D, không phải mục đột biến. Một biến thể
     cho mỗi hạng mục không chứng minh mọi cách viết vi phạm hạng mục ấy đều bị bắt.
  Đã đo (phiên soạn r7, rig riêng, ứng viên nháp — KHÔNG phải mã của executor; bảng 9 dòng 6, 7, 11, 12): 87/87 biến
  thể có kỳ vọng chết hay đỏ đều đúng kỳ vọng, hai đối chứng sống thì sống, ở cả ba Python; và trên một helper dựng
  đúng theo HINT lượt 6, 34 trong số ấy lọt hẳn (cả hai ca xanh).
  **CHƯA ĐO:** (E) trên mã của executor.

  **Log mỗi dòng biến thể**: tên mục và vị trí, ca đích, nhãn đích và tiểu nhãn (nếu có), loại assertion
  (nếu dòng nêu; r6), A1 (nhãn, tiểu nhãn và loại báo), A2 (sống sót hoặc nhãn Y — đây là "các nhãn khác vẫn giết nó trong ca đầy đủ"; danh
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
  · phiên soạn r6 (16:46:35Z–16:46:55Z 29-09, Python 3.12.3; lặp ở 3.11.15 lúc 16:48:58Z và 3.13.12 lúc 16:50:49Z,
  cùng kết quả; rig sao chép, helper mở rộng 16 nhãn / 36 đơn vị): bốn mươi chín dòng (năm mươi cặp đích)
  đều được chấp nhận — A1 chết bằng `TinHieuChotCa` đúng nhãn, tiểu nhãn và loại assertion, W1 chết đúng tiểu nhãn
  và loại, W0 sống sót có bộ đếm seam ≥ 1 (50/50 cặp); runner thật chọn bốn mươi chín bản ghi cho `giet 1/1` ở
  bốn mươi tám dòng và `giet 2/2` ở (c), kết quả tổng `(0, 0)`, không dòng nào in kiểu ngoại lệ trong ngoặc;
  đối chứng `NameError` chết bằng `NameError` và không được tính giết. Chi tiết bảng 8;
  · cross-review lượt 6 (rig reviewer, phương án r7, ba Python): năm mươi tư dòng (năm mươi lăm cặp) đều được
  chấp nhận; kiểm kê 191 ca, 174 + 54 = 228, harness 3, tổng 231;
  · phiên soạn r7 (rig riêng, helper r7 có quy ước đếm theo đường và luật nguồn "hàm + nội dung", ba Python; bảng 9
  dòng 2, 4, 9): năm mươi tư dòng (năm mươi lăm cặp) đều được chấp nhận; kiểm kê 191 / 228 / 3 / 231; runner thật
  cho 53 dòng `giet 1/1`, (c) `giet 2/2`, kết quả `(0, 0)`, không dòng nào in kiểu ngoại lệ trong ngoặc, đối chứng
  `NameError` chết bằng `NameError`;
  · chưa có: năm mươi tư dòng chạy trên ứng viên của executor.
- **B6 (cả write set) — delta và bằng chứng cục bộ thay CI.**
  `python .claude/dev/launcher_test.py` toàn suite **delta = 0 ca đỏ** so với nền, đo **cả hai vế trong
  một lệnh** trên cùng rig (bài học "PHÉP ĐO DELTA SO HAI VẾ": nền và ứng viên cùng dựng bằng một vòng
  lặp, cùng bước). (Trên rig r7, với ứng viên nháp và helper r7, phép đo ấy cho delta 0 — nền 187/188 tổng 189,
  ứng viên 189/190 tổng 191, cùng một ca `r351` đỏ sẵn — bảng 9 dòng 13; đó là số trên bản nháp, không thay phép
  đo của executor.) `python .claude/dev/launcher_test.py --dot-bien`: không đột biến cũ nào đổi hạng.
  `python -m ruff check --select F .claude/dev/launcher.py .claude/dev/launcher_test.py`: delta F = 0
  (ruff vắng thì ghi `KHÔNG ĐO ĐƯỢC`, không ghi 0). Nền đo được ở r3 và đo lại ở r5 và r6; r7 KHÔNG đo lại (§8; r3 11:49:59Z 29-09, `89fc4fa`,
  ruff 0.15.8 là NHỊ PHÂN độc lập `ruff`, vì `python -m ruff` vắng ở cả `python` lẫn `python3.12` của
  container này): `launcher.py` 0 lỗi F; `launcher_test.py` 5 lỗi F (cả năm là F841, dòng 2566, 3387,
  3629, 4110, 6061). "delta = 0" nghĩa là ứng viên KHÔNG hơn số nền ấy, đo lại trên nền tiếp nối.
  **Nghĩa vụ bằng chứng.** Mọi lệnh B1–B6 chạy **cục bộ trên Linux, đúng SHA ứng viên** (ghi
  `git rev-parse HEAD` cùng log). Log mỗi lệnh gồm: lệnh **nguyên văn**, giờ UTC bắt đầu, rc, và
  **dòng tổng nguyên văn** của runner (số qua / chạy / bỏ qua / đỏ; với `--dot-bien` là dòng tổng và
  ba hạng của B5). Log của B5 còn kèm **từng dòng biến thể** với bốn phép đo A1/A2/W1/W0 như đã định
  ở B5 (kỳ vọng năm mươi tư dòng, cũng là năm mươi tư mục `DOT_BIEN`, năm mươi lăm cặp đích), và **log của phép
  D**: lệnh nguyên văn, giờ UTC, rc, dòng xanh của bản đúng cho từng ca đăng ký, và từng dòng trong 63 control
  (17 mức nhãn, 46 mức tiểu nhãn) cùng các phép đảo thứ tự, kèm đơn vị thiếu; và **log của phép (E)** (B5): mỗi biến
  thể một dòng, kèm ánh xạ sang hạng mục của bảng không gian mở rộng; và phép tính sàn Windows của B4 (lệnh + số). Đính vào handoff; reviewer đọc **trước** merge. Xanh của `gate-registry` KHÔNG thay
  cho log này (§8). Sau merge, `launcher-windows.yml` chạy ở lượt `push` master: đọc kết quả cả
  Windows lẫn Ubuntu (`land_obligation`), kể cả dòng `DOT BIEN:` của bước `Tu dot bien`, đừng suy thành công từ
  việc đã đẩy.
  **ĐỎ khi:** ứng viên có thêm ca đỏ, đột biến cũ đổi hạng, thêm lỗi F, handoff thiếu log nguyên văn cho
  bất kỳ lệnh nào trong B1–B6, hoặc thiếu log phép D, bản đúng không xanh ở D, hay có control của D không
  đỏ; hoặc thiếu log phép (E), hay có biến thể (E) không đúng kỳ vọng. Sau merge: `DUOI SAN` ở bước `Tu dot bien`
  của lượt push master là ĐỎ của packet (B4).
- **B7 — bằng chứng từ nơi lỗi lộ ra (không phải cổng).** Chạy `ops/lease_publish_test.py` với seam
  ESRCH chèn vào `launcher.py` bản sao tạm, hoặc chạy `t154` lặp nhiều lần song song: chỉ để khai,
  **không** dùng làm tiêu chí vì race chập chờn không đỏ ổn định (luật L3). Cross-review lượt 1
  (hướng 10) đã chạy `t154` với seam ở bản sao: nền ném `ProcessLookupError`, bản HẸP r1 qua.
  Cross-review lượt 2 (hướng 13, 11:29:11Z 29-09) chạy lại trên bản dựng theo Q-A r2: nền ném
  `ProcessLookupError` sau 1 lần chạm seam; bản dựng qua, 31 lần chạm seam, 4,87 giây, các tiến trình con
  cháu được thu hồi hết. Cross-review lượt 3 (12:50:55Z 29-09) đo lại trên bản dựng theo Q-A r3: nền ném
  `ProcessLookupError` sau 1 lần chạm seam (1,43 giây); bản dựng qua, 31 lần chạm seam, 5,136 giây, con cháu
  thu hồi hết. Đó là số của reviewer trên bản nháp, không phải phép đo trên ứng viên của executor và không
  do phiên soạn r3, r4, r5, r6 hay r7 chạy lại; thời lượng không phải hằng số.

## 8. Số đo nền (thời điểm đo cạnh từng số)

- **Nền nghiệm thu `89fc4fa` vẫn hợp lệ cho write set — đo lại ở r7 (01:46Z 30-09, worktree của phiên soạn, HEAD
  `82d05eb`, sạch).** `git fetch -q origin master` rc=0 (01:46:15Z, xong 01:46:16Z); `git rev-parse origin/master` ⇒
  `c16bec639efa0077def4916c25c3e0c17f68dcaa` (Merge PR #693, commit lúc 2026-09-30T05:59:04+07:00); **master ĐÃ TRÔI**
  kể từ r4–r6: `git rev-list --count 44620e8..origin/master` ⇒ 22.
  `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py`
  ⇒ **rc=0** (01:46:16Z); cùng lệnh với `-- .claude .github` ⇒ rc=0 (01:46:16Z). `git rev-parse origin/master:<tệp>` ⇒
  blob `561ff7a1840d65a6fc9953947f71cabe4947b3c9` và `abf7f6cafd36c34392a31f6e1b24f3cd63a3c7c8` (giữ nguyên); `wc -l` ⇒
  4308 và 8354 dòng (01:46:25Z). `git rev-list --count 89fc4fa..origin/master` ⇒ **47**, trong đó `--no-merges` ⇒
  **37**; `git diff --shortstat 89fc4fa origin/master` ⇒ **37 tệp, 8953 dòng thêm, 5 xoá**; số tệp đổi dưới `.claude/`
  hoặc `.github/` = **0** (`git diff --name-only … | grep -c`). `--is-shallow-repository` ⇒ `false`; `core.abbrev` =
  7. `82d05eb` chưa là tổ tiên của `origin/master` (`merge-base --is-ancestor` rc=1), `44620e8` là tổ tiên của
  `82d05eb` (rc=0). Số 25 / 19 / 15 tệp / 6903 của r4–r6 bên dưới là số LỊCH SỬ. Phép so hai nguồn ref: **KHÔNG làm lại
  ở r7** (chỉ fetch `master`).
- **Độ dài `_con_song` trên nền** (r7, AST `end_lineno` trên bản sao `launcher.py` của `89fc4fa` trong rig r7,
  02:00:46Z 30-09, Python 3.12.3): dòng 629–672, **44 dòng** (kể cả docstring). Khớp số cross-review lượt 6 đo; §9
  của r6 ghi nhầm "77 dòng (629–705)".

- **Nền nghiệm thu `89fc4fa` vẫn hợp lệ cho write set — đo lại ở r6 (16:46Z 29-09, kho
  `/home/user/tra-luat`, worktree của phiên soạn ở `1b13110`).** `git fetch -q origin master` rc=0 (16:46:44Z,
  xong 16:46:45Z); `git rev-parse origin/master` ⇒ `44620e8706c86f5517b0f0e0a72759a59fd508ca`;
  `git rev-list --count 44620e8..origin/master` ⇒ 0 (đầu master KHÔNG trôi kể từ r4 và r5). `git diff --quiet
  89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py`
  ⇒ **rc=0** (16:46:45Z); cùng lệnh với `-- .claude .github` ⇒ rc=0 (16:46:45Z). `git rev-parse
  origin/master:<tệp>` ⇒ blob `561ff7a1840d65a6fc9953947f71cabe4947b3c9` (launcher.py) và
  `abf7f6cafd36c34392a31f6e1b24f3cd63a3c7c8` (launcher_test.py); `wc -l` ⇒ 4308 và 8354 dòng; `git rev-list
  --count 89fc4fa..origin/master` ⇒ 25, trong đó `--no-merges` ⇒ 19; `git diff --shortstat 89fc4fa origin/master`
  ⇒ 15 tệp, 6903 dòng thêm, 0 xoá; `git rev-parse --is-shallow-repository` ⇒ `false`; `core.abbrev` = 7. Tất
  cả trùng số r4 và r5. Phép so hai nguồn ref: **KHÔNG làm lại ở r6** (chỉ fetch `master`). Cross-review
  lượt 5 cũng đo blob và số dòng này ra cùng số (VERDICT lượt 5, bảng ĐO: 4308/8354, 25 commit/19 không merge,
  15 tệp/6903 thêm/0 xoá).
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
- **Ruff nền — đo lại ở r6 (16:59:41Z 29-09, nhị phân `ruff` 0.15.8, `--no-cache --select F`, trên blob nền lấy
  bằng `git show HEAD:<tệp>` ở worktree `1b13110`, vốn giữ nguyên hai blob ấy):** `launcher.py` "All checks
  passed", rc=0 (0 lỗi F); `launcher_test.py` 5 lỗi, cả năm F841 ở dòng 2566, 3387, 3629, 4110, 6061 — trùng số
  r3, lượt 3 và r5. `python -m ruff` không dùng (vắng ở container).
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
  số; phiên soạn r4, r5, r6 và r7 KHÔNG chạy lại phép đếm AST này (hai tệp giống hệt theo blob, nên số không đổi theo suy ra; r5, r6 và r7 chỉ đếm số ca đăng ký của rig sau khi thêm hai ca: 191 = 189 + 2; B6 trên rig r7 in "tong 189" cho nền và "tong 191" cho ứng viên, bảng 9 dòng 13; lượt 5 đo lại bằng AST ra 189 = 155 `t` + 34 khác, hậu tố lớn nhất 155, không hổng);
  đếm hàm mức đỉnh mang decorator `@ca`): **189 ca đăng ký = 155 ca tiền tố `t<số>` + 34 ca khác**
  (các ca tiền tố `r`: `r01`–`r21`, `r345`×5, `r347`×2, `r351`×3, `r348`×2, `r349`×1). Hậu tố lớn nhất
  của nhóm `t` là `t155`; 155 hậu tố phân biệt, không trùng, không hổng trong 1..155. **155 không phải
  tổng suite**: nó là hậu tố lớn nhất của một nhóm; bản r1 dùng nó làm tổng và sai. Nghiệm thu B6 phải
  đối chiếu số đăng ký, số chạy, số bỏ qua và số đỏ, không suy tổng từ hậu tố. Sau packet này, số đăng
  ký kỳ vọng tăng đúng bằng số ca mới ở §6.2 (**hai**) — executor đếm lại và khai.
- `DOT_BIEN` ở `launcher_test.py:7012`: **174 mục**; `DOT_BIEN_HARNESS` ở `:7930`: 3 mục (cùng phép đếm
  AST, 11:10:16Z; đo lại 11:46:05Z và bởi cross-review lượt 3 lúc 12:50:02Z, cùng số). Đây là số mục ĐỘT
  BIẾN, khác số ca. Số mục mới: xem B5 (**mười ba** lớp, kỳ vọng **năm mươi tư** mục `DOT_BIEN`; sau packet:
  bảng sản phẩm 174 + 54 = **228**, cộng 3 mục `DOT_BIEN_HARNESS` = **231** mục (r6: 223 / 226); số ca đăng ký 189 + 2 = **191**
  — toàn là số kỳ vọng suy ra, chưa đo trên ứng viên; trên rig sao chép của r6 đếm ra đúng 223 / 3 / 226 và 191
  ca, 16:46:55Z 29-09, Python 3.12.3, bảng 8; lịch sử: rig của r5 đếm ra 193 / 3 / 196 và 191 ca, 15:35:38Z, bảng 6). Để khỏi lẫn với các revision trước: r3 kỳ vọng 174 + 12 = 186 (189 kèm harness),
  lượt 3 đã dựng 12 mục r3 và đếm ra đúng 186 / 189; r4 kỳ vọng 174 + 15 = 189 (192 kèm harness), lượt 4 đã dựng
  15 mục r4 và đếm ra đúng 189 / 192; HINT lượt 4 đề nghị 174 + 16 = 190 (193), r5 thay bằng 174 + 19 = 193 (196)
  vì tách (k) thành bốn dòng (B5); HINT lượt 5 đề nghị thêm (h3): 174 + 20 = 194 (197 kèm harness), r6 thay bằng
  174 + 49 = 223 (226) vì liệt kê toàn không gian (B2, B5 lớp (l)) và thêm (k5); r7 thay bằng 174 + 54 = 228
  (231) vì thêm lớp (m) (rig của cross-review lượt 6 đếm ra đúng 228 / 3 / 231 và 191 ca, 00:53Z 30-09; rig riêng
  của phiên soạn r7 đếm ra cùng 228 / 3 / 231 và 191 ca, 01:33:28Z 30-09, bảng 9 dòng 4), và r7 KHÔNG thêm dòng nào
  nữa (B4, B5). Số ca đăng ký không đổi (191). Số nhãn 17; 46 tiểu nhãn + 9 đơn vị đơn = 55 đơn vị; D có 63
  control (HINT lượt 6: 17; 32 + 9 = 41; 49 — r6: 16; 27 + 9 = 36; 43). Phép (E) của r7 không thuộc `DOT_BIEN`
  nên không đổi các số 228 / 231.
- **Lease** (SỐ CỦA PHIÊN SOẠN r3 — phiên soạn r4, r5, r6 và r7 KHÔNG đo lại; chạy trong `/home/user/tra-luat` sau `git fetch` đủ, 29-09; lệnh `python ops/lease_publish.py
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
- Suite `launcher_test.py` trên nền: phiên soạn r3–r6 **chưa đo**; phiên soạn r7 đo trên một clone sạch `82d05eb`
  (01:48:42Z 30-09, Python 3.12.3): `187/188 ca DA CHAY QUA (tong 189, bo qua 1, hong 1)`, rc=1, ca hỏng duy nhất
  `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` (đỏ sẵn; cross-review lượt 6 ghi cùng ca) — bảng 9 dòng 13. B6 vẫn bắt
  executor đo cả hai vế trên nền tiếp nối.
- Ruff nền (11:49:59Z, `89fc4fa`, nhị phân `ruff` 0.15.8; `python -m ruff` vắng): `launcher.py` 0 lỗi F,
  `launcher_test.py` 5 lỗi F (F841 ×5). Chi tiết ở B6.

Mọi con số phải được **đo lại** trước cấp lease và trước land (L5).

## 9. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục một lượt thất bại. Hình dạng đáng canh, ghi để lượt thi
hành không lặp: *"vá một lỗ mà mở lỗ khác trong cùng hàm"* / *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ
ba"* — năm lần trước khi r5 được review; lượt 5 đo lần thứ **sáu** (mục 6 dưới đây), và r6 là revision đầu
tiên ĐỔI CÁCH LÀM thay vì vá tiếp: liệt kê toàn không gian trước (mục 6); lượt 6 đo lần thứ **bảy** — chính
phép liệt kê của r6 đã bỏ sót nhánh cũ — và r7 mở rộng phép liệt kê sang MỌI đường (mục 7). Các mục là lịch
sử của cùng một lớp, không phải bảy finding độc lập:
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

6. **(lượt 5, mới ở r6 — lần thứ sáu, và lần r6 đổi cách làm)** k1–k4 và D của r5 có răng (lượt 5 dựng lại và
   thấy đóng), rồi hình dạng lặp một lần nữa ở chỗ KHÔNG ai chỉ: nhóm phân tích chỉ được bắt ở tầng đọc, đem ra
   tầng hỏi vẫn lọt — `RuntimeError`/`KeyboardInterrupt` đều được truyền nguyên nên hai ca r5 và D xanh, trong
   khi `IndexError` bị nuốt. Sáu lượt liền, cùng một cách sai của phiên soạn: vá đúng ô được chỉ. Bài học của
   CLAUDE.md nói đúng điều cần làm — *tự liệt kê hết đường TRƯỚC, đóng cả loạt, cho mỗi đường một chốt riêng* —
   và r6 làm đúng thứ tự ấy thay vì thêm tiểu nhãn `hoi-parse` như HINT đề nghị:
   · **Bước 1, liệt kê.** Bảng không gian ở B2: năm hàng (nhóm ngoại lệ mà Q-A phân biệt) × ba tầng (hỏi, đọc,
     kill) = 15 ô, và trong mỗi ô từng thành viên × hai hướng sai = 42 hạng mục. Tầng kill là tầng thứ ba r6 tự
     thêm (Q-A.5 chỉ nêu hai).
   · **Bước 2, tìm ô thiếu đầu vào hoặc thiếu đột biến.** Kiểm từng hạng mục với B5 của r5. r6 tìm thêm được,
     ngoài lỗ lượt 5 chỉ, sáu chỗ mà chưa reviewer nào chỉ (đều đo được trên rig, bảng 8): (i) bản vá tối thiểu
     cho đúng ESRCH — chỉ bắt `ProcessLookupError` — không có dòng đột biến nào (B5 r5 có bản RỘNG và bản
     `PermissionError`, không có bản HẸP nhất); (ii) phép hỏi cho ESRCH rơi cùng nhánh `OSError` khác không có dòng
     nào; (iii) EPERM chưa từng là đầu vào ở tầng hỏi và tầng đọc (chỉ có ở kill) nên bản chấp nhận đúng hai
     errno EACCES, EIO qua nghiệm thu; (iv) tầng kill không có đầu vào cho ngoại lệ ngoài họ `OSError` nên mệnh đề
     bắt thừa ở đó không ai thấy; (v) ba hướng "thoát" của hàng nhóm phân tích × tầng đọc không thể có đột biến
     chết đúng lý do vì r3–r5 cấm đổi mọi ngoại lệ thành `TinHieuChotCa` — mọi bản không bắt `ValueError`,
     `IndexError` hay `UnicodeDecodeError` chỉ chết vô can, tức tín dụng giả; (vi) ngoại lệ bị BỌC lại
     (`raise … from …`) thoát bằng đối tượng khác nên không được nhận ra.
   · **Bước 3, đóng cả loạt, mỗi hướng một chốt.** 30 dòng mới ((k5) và (l1)–(l29)), 2 nhãn mới và 10 đơn vị mới ở
     bảng tiểu nhãn (26 → 36), bốn loại ngoại lệ được nhận ra ở quy ước chung, quy tắc nhận ra ngoại lệ tự nhiên của
     `B2-parse`. Bản đầu của quy tắc chuỗi ngoại lệ tính cả `__context__`, và đối chứng `ctrl` bắt được đúng bản
     ấy: một `ValueError` vô can ném trong lúc xử lý lỗi seam bị ghi nhầm thành bằng chứng (16:26:50Z 29-09).
     Đúng hình dạng CLAUDE.md nêu — cái chốt dựng ra để chống tín dụng giả tự cấp tín dụng giả — nên chuỗi
     chỉ còn `__cause__`.
   · **Bước 4, phép đo ĐÓNG chứ không chỉ liệt kê.** Ngoài danh sách viết tay, một bộ sinh (bảng 8) dựng MỌI dãy
     tối đa ba mệnh đề `except` (đính chính r7, theo cross-review lượt 6: ở tầng H và Đ là dãy MỘT đến ba mệnh đề,
     không gồm dãy rỗng; ở tầng K là dãy không đến ba — xem đính chính sau bảng 8) trên các LỚP ngoại lệ (tám lớp × hành động {rơi về bước sau, `False`, `True`,
     bọc lại, `None`}) và MỌI ánh xạ errno → hành động (bốn errno, mỗi errno một hành động, cộng hành động mặc định) cho từng tầng;
     mỗi dãy được xếp vào CHỮ KÝ hành vi của nó (kết quả trên 8–10 đầu vào của tầng), dãy có chữ ký trùng bản đúng là
     tương đương và bị loại, và MỖI chữ ký còn lại phải chết bằng `TinHieuChotCa` tại đúng đơn vị sớm nhất mà chữ
     ký ấy chạm. Bộ sinh tìm ra MỘT lỗ mà danh sách
     viết tay bỏ sót — tầng đọc bọc lại `ValueError` tự nhiên thành `RuntimeError` (chết vô can) — và lỗ ấy đã
     đóng bằng quy tắc nhận ra ngoại lệ tự nhiên có xét `__cause__` cùng dòng (l21). Sau đó 0 lỗ trên toàn bộ
     không gian đã sinh (bảng 8).
   Giới hạn khai thẳng: bộ sinh chỉ phủ các dãy mệnh đề trong ngữ pháp của nó; hình dạng nằm ngoài (kiểm tra dữ
   liệu thay bắt ngoại lệ, danh sách errno dài hơn bốn, tên lớp con cụ thể như `TimeoutError`) chỉ được đo bằng
   dòng viết tay (l16), (l4), (l11), (l12) hoặc KHÔNG ĐO ĐƯỢC (B2, mục 3 và 5 của danh sách bất khả thi).
   Đây là lý do hàng "Không coi một danh sách mutant hữu hạn là bằng chứng" bên dưới vẫn đứng.
7. **(lượt 6, mới ở r7 — lần thứ BẢY)** Phần r6 liệt kê có răng ở mọi ô nó liệt kê (lượt 6 dựng lại: 50/50 cặp,
   D 43 control, ba Python), nhưng lời khai "toàn bộ không gian ... mọi mệnh đề `except` mà một bản vá có thể
   viết" rộng hơn phép liệt kê. **Bảng không gian của r6 đã BỎ SÓT nhánh cũ**: hai trục "ngoại lệ nào × tầng nào"
   với ba tầng H, Đ, K chỉ là tầng của ĐƯỜNG MỚI, trong khi Q-A.3 bắt giữ nguyên xi hai nhánh sẵn có (tệp có ⇒
   đọc; tệp vắng ⇒ kill) mà không đầu vào nào của r6 đi vào; và hai trục vuông góc (đếm × ngoại lệ; cú pháp phép
   tách) chỉ được đo ở vài đầu vào. Một bản vá TỰ NHIÊN (hợp nhất hai khối đọc về hướng `kill`) qua hết r6 + D +
   toàn suite mà lật 124 → 125. Chỗ đắt của lần thứ bảy: r6 đã làm đúng cách CLAUDE.md dạy (liệt kê trước), và
   lỗ nằm ngay trong định nghĩa "không gian" của phép liệt kê — hình dạng "danh sách tự liệt kê, cho là hết" lần
   này ở cấp ĐỊNH NGHĨA TRỤC, không phải cấp ô. Và HINT lượt 6 tự nó lặp hình dạng ở cỡ nhỏ: vá đúng ba chỗ được
   chỉ (năm đầu vào nhánh cũ, quy ước đếm "hỏi 1, đọc ≤ 1", một `comm` có `)`), còn trên rig r7 một helper dựng
   đúng theo HINT để lọt 34 biến thể trái Q-A — mười ba ở nhánh cũ tệp có, hai mươi ở nhánh cũ tệp vắng, một ở phép
   đếm `kill` (bảng 9 dòng 7); câu chữ của HINT về luật nguồn (so tệp và số dòng) cũng hỏng dưới chính runner
   `--dot-bien` (bảng 9 dòng 5). Chữa theo lớp ở r7:
   · **Bước 1, định nghĩa không gian từ ĐƯỜNG, không từ tầng của một nhánh.** Năm tầng (H, Đ0, K0, Đ, K) × sáu hàng
     (R0–R5) = 30 ô; ba hướng cho ô "phải thoát nguyên" (bắt, bọc, thay thế); ba trục vuông góc (đếm C, cú pháp S,
     nơi gọi N). 129 hạng mục (B2).
   · **Bước 2, đóng mỗi hạng mục bằng một chốt có răng đo được.** 51 hạng mục có dòng B5 (54 dòng, không thêm
     dòng nào ngoài HINT); 78 hạng mục có biến thể của phép (E), vì dòng Linux-only thứ bảy đưa Windows dưới sàn
     (B4). Đầu vào mới: `B2-nhanh-cu` từ 5 thành 19 tiểu nhãn, lời gọi đường cũ ở `B3-zombie`, observer `kill` trên
     mọi đầu vào đi qua K hoặc K0; quy ước đếm theo đường.
   · **Bước 3, đo đóng.** Rig r7, ba Python: 55/55 cặp; D 63 control + 6 phép đảo; (E) 87/87 đúng kỳ vọng, hai đối
     chứng sống; B6 delta 0 trên bản nháp (bảng 9).
   Giới hạn khai thẳng, và vì sao lần thứ tám vẫn có thể xảy ra: phép liệt kê của r7 chỉ đủ tới các trục nó định
   nghĩa. Ngoài trục: errno thứ tư, lớp con cụ thể, mệnh đề `finally`/`else`, "kiểm tra dữ liệu thay bắt ngoại lệ" ở
   nhánh cũ, hai nơi gọi `:1020`/`:1039`, và mọi cách viết khác MỘT biến thể mỗi hạng mục (§10). Cùng lúc, mỗi dòng
   Linux-only thêm vào làm hẹp sàn đột biến Windows (B4: biên 42 → 7 → 4 mục, dòng thứ bảy ⇒ dưới sàn) — một giới
   hạn CỨNG cho chính cách làm "liệt kê thêm", đo được, và là dữ kiện cho câu hỏi ngưỡng ba lần ngay dưới.

Mỗi bản vá/đặc tả đều ĐÚNG và CÓ RĂNG ở chỗ nó phủ; lỗ nằm ở đường KHÔNG ai chỉ. Các phép đo chỉ chứng
minh các đường đã thử. Miền kiểm của r7 gồm ESRCH, EACCES, EPERM, EIO, zombie, ngoại lệ ngoài `OSError`
(`Exception` và `BaseException`) ở cả năm tầng hỏi, đọc mới, kill mới, đọc cũ, kill cũ, nhóm phân tích ở cả năm
tầng (tự nhiên ở hai tầng đọc, sentinel ở tầng hỏi và hai tầng kill), số lần hỏi/đọc/kill theo từng đường, cú
pháp phép tách với `comm` chứa `)` ở cả hai tầng đọc, và **kết quả của bước PID dự phòng (sống, đã `wait`, EPERM,
EIO) cùng số lần gọi `kill(pid, 0)`**; bảng không gian mở rộng ở B2 ghi rõ ô, đầu vào và chốt từng hướng. B2 khoá bản RỘNG và các biến thể tầng đọc, B3/B3b
khoá bản HẸP r1; các lớp còn lại ở B5 khoá những biến thể đã liệt kê. **Không coi một danh sách mutant hữu hạn là bằng
chứng đã liệt kê hết mọi đường**; executor và reviewer vẫn phải kiểm các đường mới xuất hiện trong chính
cách triển khai được chọn.

**Ngưỡng ba lần đã chạm — câu hỏi đặt cho điều phối/chủ kho, r4, r5, r6 và r7 KHÔNG tự trả lời.** CLAUDE.md dạy đếm
hình dạng lỗi chứ không chỉ đếm lỗi: cùng một hình dạng lặp từ ba lần trở lên thì câu hỏi đúng là "có nên
làm việc này theo cách này không", không phải "vá thế nào". Đường hiện tại (giữ phép hỏi `exists()` rồi
dựng thêm một đường lỗi có đọc + `kill(pid, 0)`, Q-A.1–4) tự nó sinh ra nhiều đường cần chốt — đó là lý do
ma trận ở B2 phình dần từ r1 tới r6 (số dòng biến thể của B5: bảy ở r2, mười hai ở r3, mười lăm ở r4,
mười chín ở r5, bốn mươi chín ở r6, năm mươi tư ở r7 cộng 89 biến thể của phép (E); số đơn vị assertion: 22 ở
r4, 26 ở r5, 36 ở r6, 55 ở r7). Bước nhảy 19 → 49 của r6
KHÔNG phải vì có thêm 30 đường lỗi thật: nó là giá của việc liệt kê đủ 15 ô × hai hướng thay vì vá theo
finding, và chính con số ấy là bằng chứng cho câu hỏi của ngưỡng — một đường thiết kế mà nghiệm thu cần 49
đột biến để khoá phạm vi bắt của một hàm dài 44 dòng trên nền (dòng 629–672, kể cả docstring; AST `end_lineno`, đo lại ở cross-review lượt 6
và ở phiên soạn r7, §8 — r6 ghi nhầm "77 dòng (629–705)") là một đường tự sinh
đường. r7 thêm hai dữ kiện định lượng cho câu hỏi ấy: nghiệm thu nay cần 129 hạng mục cho cùng hàm 44 dòng, và
sàn đột biến Windows chặn cứng việc đưa chúng vào `DOT_BIEN` (B4) — nên phần lớn răng của r7 (78 hạng mục) chỉ đo
được MỘT lần, bằng phép (E), không được đo lại ở các lượt sau. Có thể cân nhắc một cấu
trúc ít đường hơn (ví dụ dùng chính phép đọc làm phép hỏi), nhưng nó đổi hành vi nhánh cũ mà Q-A.3 cấm đổi, và
r4, r5, r6 lẫn r7 chưa đo phương án nào. Nên r7 giữ hướng của r2 đến r6 và chỉ nêu ngưỡng; có hỏi lại quyết
định gốc hay không là việc của điều phối/chủ kho.

## 10. `chua_do_duoc`

- Suite `launcher_test.py` và `--dot-bien` trên nền: chưa chạy ở phiên soạn. Phiên soạn r3 chỉ chạy lại
  probe của cross-review lượt 2 (bốn probe: `inventory`, `matrix_extra`, `stronger`, `mutations`, 11:46Z; `inventory` thoát rc=1 ở dòng
  cuối vì bản sao rig không có `SPEC.md`, còn các dòng số đã in đủ trước đó)
  trên hai ca mẫu do reviewer dựng ở bản sao rig; không chạy `python .claude/dev/launcher_test.py` đầy đủ.
  **Phiên soạn r4 không chạy probe hay suite nào**: nó chỉ áp HINT, đọc log của lượt 3, và chạy các lệnh
  git ở §8 (nền) cùng phép đo băm. **Phiên soạn r5 có chạy** (15:33Z–15:36Z 29-09) probe của lượt 4 trên một
  rig sao chép (bảng 6, B5) — vẫn không chạy `python .claude/dev/launcher_test.py` đầy đủ, không chạy suite
  hay toàn bộ 174 đột biến cũ. **Phiên soạn r6 có chạy** (16:20Z–16:59Z 29-09) một rig sao chép riêng (bảng 7 và
  8, B2, B5) — cũng KHÔNG chạy `python .claude/dev/launcher_test.py` đầy đủ, không chạy suite hay 174 đột biến
  cũ; rig chỉ chạy hai ca `t156_...`/`t157_...` dạng prototype và 49 đột biến mới. **Phiên soạn r7 có chạy**
  (01:30Z–02:01Z 30-09) một rig riêng (bảng 9): hai ca dạng prototype với helper r7, 54 dòng mới, 89 biến thể (E),
  phép D, runner thật trên 54 dòng mới, và **suite đầy đủ hai vế** (nền và ứng viên nháp, bảng 9 dòng 13) — nhưng
  KHÔNG chạy `--dot-bien` trên 174 đột biến cũ; câu "không đột biến cũ nào đổi hạng" của B6: KHÔNG ĐO ĐƯỢC ở r7.
- Ruff: đo được **nền** (§8, B6: `launcher.py` 0, `launcher_test.py` 5, nhị phân `ruff` 0.15.8; cross-review
  lượt 3 đo lại ra cùng số, đúng năm F841 ở dòng 2566, 3387, 3629, 4110, 6061); delta của ứng viên: chưa có
  ứng viên. `python -m ruff` vắng trong container soạn r3 (và trong sandbox của cross-review). Phiên soạn r4
  không chạy ruff; phiên soạn r5 và r6 chạy lại nhị phân `ruff` 0.15.8 trên blob nền (§8; r6 lúc 16:59:41Z) ra cùng số;
  phiên soạn r7 KHÔNG chạy ruff (blob nền không đổi, §8; số F của helper r7 trên rig: KHÔNG ĐO ĐƯỢC).
- Nhánh Windows và Darwin: không đo (Q4); lần đo Windows đầu tiên là lượt push master sau merge. Các
  bảng ở §1 chỉ đo Linux, Python 3.12.3 cho bảng 3, 4, 5 và 6; bảng 7 đo ba Python 3.11.15, 3.12.3, 3.13.12, bảng 8
  đo ba Python cho phép A/W, D và runner, nhưng bộ sinh dãy dài (ba mệnh đề) chỉ chạy ở 3.12.3; bảng 9 đo ba
  Python cho A/W, D và (E), còn luật nguồn, phép so với helper HINT, chữ ký, runner, sàn và B6 chỉ ở 3.12.3.
  **Sàn đột biến Windows (B4): số THẬT trên Windows KHÔNG ĐO ĐƯỢC trước merge** (Q4); số của r7 là ước lượng tĩnh
  cận dưới, biên 4 mục. Bảng 4 chỉ đo locale UTF-8 (`preferred_encoding`
  `utf-8`, và `LC_ALL=C.UTF-8`); locale không phải UTF-8: KHÔNG ĐO ĐƯỢC. Cross-review lượt 3 mô phỏng hai
  nhánh Windows và Darwin bằng seam (hai ca trả chuỗi BỎ QUA, không tính là QUA): đó là mô phỏng nhánh, KHÔNG
  phải hệ điều hành thật, và không thay `land_obligation`.
- Một ESRCH thật (không seam) trên `/proc/<pid>/stat`: chỉ thấy một lần ở CI (job `109303373142`),
  không tái hiện được theo yêu cầu; seam là cách đo duy nhất ổn định. Tương tự, EACCES/EIO ở `stat` hoặc
  ở `read_text` của một PID sống, và `KeyboardInterrupt` giữa hai phép ấy, chưa từng được thấy trên kernel
  thật; các bảng 1–3, 5 và 6 là đầu vào do seam đặt ra. Ba đầu vào tầng đọc của r4 (ESRCH, EIO,
  `KeyboardInterrupt`) và hai kết quả lỗi của `kill(pid, 0)` ở bảng 6 (EPERM, EIO) đo được bằng seam; việc
  chúng có xảy ra trên kernel thật: KHÔNG ĐO ĐƯỢC. Cùng lời khai cho các đầu vào r6 thêm: EPERM ở `stat` và ở
  `read_text`; nhóm phân tích ở tầng hỏi và tầng kill; ngoại lệ ngoài họ `OSError` ở tầng kill — tất cả là
  đầu vào do seam đặt ra, và việc hệ điều hành hay thư viện thật sinh chúng: KHÔNG ĐO ĐƯỢC. Cùng lời khai cho đầu
  vào r7 thêm ở cột Đ0 và K0 (ESRCH/EIO/EPERM ở phép đọc cũ, ENOENT ở `stat` của PID sống, EPERM/EIO và mọi sentinel
  ở `kill` sau tệp vắng): đầu vào do seam đặt ra; tần suất thật: KHÔNG ĐO ĐƯỢC. Riêng `vang-da-wait` và lời gọi
  đường cũ của `B3-zombie` dùng `stat`, phép đọc và `kill` THẬT.
- Bản "r2" trong bảng §1 là bản nháp của phiên soạn (Q-A.1–4); chưa có bản vá của executor nào được đo với
  B1–B6. Các hàng "biến thể" của bảng 3 và bảng 5 là đột biến do reviewer lượt 2 và lượt 3 dựng, còn bảng 6
  do reviewer lượt 4 (mutant bỏ hỏi PID) và phiên soạn r5 (k2–k4) dựng; không hàng nào là bản của executor.
- **Chốt ngược A1/A2/W1/W0 và phép D (B5)**: đã thấy chạy trên rig của reviewer, bằng helper do reviewer
  viết (cờ nới `REVIEW_RELAX`). Lượt 3: mười hai mục của r3 (mười ba cặp đích) và ba đột biến tầng đọc của
  bảng 5; phép D ở **mức nhãn** (13 control đỏ, 12:52:00Z). Lượt 4 (13:32:26Z–13:40:32Z 29-09): mười lăm
  dòng của r4 (mười sáu cặp đích) đều được chấp nhận, D đủ 27 control (13 nhãn + 14 tiểu nhãn, 22 đơn vị) đều
  đỏ đúng đơn vị thiếu, và đảo thứ tự hai nhãn làm D đỏ. Phiên soạn r5 (15:35Z 29-09) dựng lại trên rig sao
  chép, có thêm nhãn `B2-pid-du-phong`: 20 cặp (19 dòng) được chấp nhận, D đủ 32 control (14 nhãn + 18 tiểu
  nhãn, 26 đơn vị), ba phép đảo thứ tự đều đỏ (bảng 6, B5). Phiên soạn r6 (16:46Z–16:53Z 29-09, ba Python) dựng lại trên rig sao
  chép với helper 16 nhãn / 36 đơn vị: 50 cặp (49 dòng) được chấp nhận, D đủ 43 control (16 nhãn + 27 tiểu nhãn),
  năm phép đảo thứ tự đều đỏ (bảng 8). Phiên soạn r7 (01:33Z–01:47Z 30-09, ba Python) dựng lại trên rig RIÊNG với
  helper r7 17 nhãn / 55 đơn vị: 55 cặp (54 dòng) được chấp nhận, D đủ 63 control (17 nhãn + 46 tiểu nhãn), sáu
  phép đảo thứ tự đều đỏ, 87/87 biến thể (E) đúng kỳ vọng (bảng 9). **CHƯA ĐO**, bao gồm: năm mươi tư dòng của r7
  (năm mươi lăm cặp đích; r6: bốn mươi chín / năm mươi) và phép (E) trên mã của ứng viên nào; tập lệnh bằng chứng của executor; tiểu nhãn báo trong thông
  điệp giết theo ĐÚNG chuỗi của đặc tả này (helper lượt 3 dùng tên nhãn phụ và tên đầu vào khác — `B2-read-ESRCH`,
  `access`/`io`/`read-error`, `empty`/`no-close`/`end`/`space`/`decode` — helper lượt 4 và helper mở rộng
  của r5 đã dùng tiểu nhãn của đặc tả, nhưng đó vẫn là helper của reviewer, không phải của executor; helper của
  r6 và của r7 là helper của phiên soạn, cũng không phải của executor); và bản
  thân hợp đồng helper ở §7 — lời văn của r3–r7, chưa có cài đặt của executor nào. Mặc định "không nới"
  của helper phải đo riêng bằng D và control test-only ở B5; A1 có chốt phủ giao nhau nên không chứng minh
  được điều này một mình.
- **Bất đối xứng hai đường về nội dung hỏng** (§2, §3): nhánh cũ trả `False`, nhánh mới rơi về `kill`. Đo
  được rằng nhánh cũ báo "đã chết" cho một PID sống có `comm` không phải UTF-8; chưa tìm Issue cho việc
  này, tần suất ngoài thực tế KHÔNG ĐO ĐƯỢC. Packet này không sửa, và không có ca nào khẳng định nhánh cũ
  đúng.
- Nội dung Mission #686 (Q0–Q5), comment `5888633201`, object ID `5628902742`, trạng thái lease #668
  live: phiên soạn không đọc lại từ GitHub; là lời khai của điều phối (số ở §8 đến từ `ai-dang-giu` chạy
  trên ref đã fetch ở r3, không phải từ GitHub live). Băm thân Issue: KHÔNG ĐO ĐƯỢC. ID comment PR #688
  chứa VERDICT lượt 2 (`5889523704`, đăng 11:40:59Z), lượt 3 (`5890856046`), lượt 4 (`5891961732`, đăng
  14:07:48Z), lượt 5 (`5894035533`, đăng 16:09:51Z) và lượt 6 (`5902146149`, đăng 01:16:56Z 30-09) là dữ kiện điều phối cấp;
  phiên soạn r4, r5, r6 và r7 không kiểm chúng trên GitHub; giờ đăng comment lượt 3 (13:02:58Z), lượt 4 (14:07:48Z),
  lượt 5 (16:09:51Z) và lượt 6 (01:16:56Z) do phiên điều phối đọc qua REST. Họ model của reviewer lượt 6 (Claude
  Opus 5.5) là tự khai trong VERDICT, không có phép đo máy: KHÔNG ĐO ĐƯỢC. (Bản r3
  của mục này ghi ID lượt 2 là "KHÔNG có" trong khi `nguon_cap_viec` của chính r3 đã điền nó; r4 sửa cho
  khớp.)
- Lease và ref: phiên soạn r4, r5, r6 và r7 KHÔNG đo lại các số lease (người giữ `launcher.py` 0, `launcher_test.py` 1, hạn
  `2026-09-30T07:41:00Z`) và KHÔNG so lại hai nguồn ref (516/517) — chỉ fetch `master` để đo nền. Cross-review
  lượt 3 không có ref và object lịch sử của lease #668 trong clone của họ (chỉ 4 ref nhánh; `cat-file -e
  2ae5646^{commit}` rc=128) nên cũng KHÔNG ĐO ĐƯỢC các số ấy; đừng suy "người giữ 0" từ một tập ref chưa so
  hai nguồn (cross-review lượt 4 và lượt 5 cũng báo bundle chỉ có 4 ref nhánh và object `2ae5646` vắng, rc 128;
  lượt 6 báo object `2ae5646` vắng, rc 128). Hạn `2026-09-30T07:41:00Z` của lease #668 là số đọc ở r3; nó có thể
  đã qua hoặc sắp qua lúc cấp lease cho `wp685` — trạng thái hiện hành: KHÔNG ĐO ĐƯỢC ở r7. Đo lại lúc cấp lease.
- Phép đo `t154` của B7: chỉ có số của reviewer trên bản nháp — lượt 2 (nền ném `ProcessLookupError` sau 1 lần
  chạm seam; bản dựng qua, 31 lần chạm, 4,87 giây) và lượt 3 (12:50:55Z: nền 1 lần chạm, 1,43 giây; bản dựng
  qua, 31 lần chạm, 5,136 giây) và lượt 4 (rig khác: 54 lần chạm, 4,938 giây, seam bơm lỗi đúng một lần — phép đo
  khác, không phủ định 31) — phiên soạn r3, r4, r5, r6 và r7 không chạy lại, và không có ứng viên của executor
  để chạy.
- Toàn bộ 174 đột biến cũ (`--dot-bien`): KHÔNG ĐO ĐƯỢC ở r3–r7. Lượt 3, lượt 4, lượt 5 và phiên soạn r5 chỉ đếm
  được rằng số mỏ neo của 174 mục cũ không đổi (count changes rỗng); lượt 6 đếm lại trên ứng viên nháp của họ (0
  mất, 0 lệch, 0 neo trong `_con_song`); phiên soạn r6 và r7 không đếm lại — đếm mỏ neo không thay bằng chứng ấy.
  B6 toàn suite: KHÔNG ĐO ĐƯỢC ở r3–r6; phiên soạn r7 đo trên ứng viên NHÁP với helper r7 (delta 0, bảng 9 dòng
  13) — không phải phép đo trên mã của executor.
- Tổng số ca `launcher_test.py` và số mục `DOT_BIEN` sau packet: chưa đo trên ứng viên nào của executor (kỳ vọng
  ở §8 và B5: 191 ca đăng ký; 228 mục `DOT_BIEN` sản phẩm, 231 kèm `DOT_BIEN_HARNESS`; 55 đơn vị assertion và 63
  control của D đếm từ bảng tiểu nhãn; HINT lượt 6: 41 / 49; r6: 223 / 226 / 36 / 43). Trên rig sao chép của
  phiên soạn r6 (prototype, xem bảng 8) đếm ra đúng 191 / 223 / 226, và trên rig riêng của phiên soạn r7 đếm ra
  191 / 228 / 231 cùng 17 nhãn / 46 tiểu nhãn / 55 đơn vị (bảng 9 dòng 4); đó không phải phép đo trên mã của executor. Các số r4 (15 mục, 16 cặp, 22 đơn vị,
  27 control) và số r5 (19 mục, 20 cặp, 26 đơn vị, 32 control; 193 / 196 sản phẩm) trong bảng lịch sử và log
  cũ, cũng như số HINT lượt 5 (20 mục, 21 cặp, 27 đơn vị, 33 control; 194 / 197), không phải tổng nghiệm thu của r6.
- **Số của r5 chỉ có trong rig tạm của phiên soạn** (một bản sao `.claude/dev/` của rig cross-review lượt 4,
  cộng một helper mở rộng thêm nhãn `B2-pid-du-phong`, cộng bốn tệp biến thể k1–k4). Rig ấy chưa được đóng
  gói vào kho hay hồ sơ nào; nó **KHÔNG tái lập được từ kho** mà phải dựng lại, và nó không phải mã của
  executor. Mọi con số đo của r5 ở bảng 6 và B5 là số trên prototype ấy.
- **Số của r6 cũng chỉ có trong rig tạm của phiên soạn** (một thư mục tạm ngoài kho gồm: bản sao `.claude/dev/` của
  `89fc4fa` lấy bằng `git archive`; ứng viên prototype `_con_song` dựng theo Q-A; helper mở rộng 16 nhãn / 36 đơn
  vị chèn vào bản sao `launcher_test.py`; 49 tệp đột biến dựng từ ứng viên bằng thay chuỗi; tập lệnh đo A/W, D,
  runner, chữ ký, đối chứng, và bộ sinh dãy mệnh đề). Rig không nằm trong kho hay hồ sơ nào, **KHÔNG tái lập
  được từ kho**; dựng lại từ đặc tả này (bảng không gian, B5, quy ước chung) là đủ cho executor và reviewer, và nó
  không phải mã của executor. Vì thế mọi con số ở bảng 7, bảng 8 và B5 mang nhãn "rig r6".
- **Số của r7 cũng chỉ có trong rig tạm của phiên soạn** (thư mục `mktemp -d` trong scratchpad của phiên soạn, ngoài
  kho: bản sao `.claude/dev/` của `89fc4fa`; ứng viên nháp trùng byte ứng viên nháp của reviewer lượt 6; helper r7;
  54 tệp đột biến; 89 tệp biến thể (E); bản sao helper r7 của reviewer lượt 6 để so; tập lệnh A/W, D, (E), luật
  nguồn, chữ ký, runner, sàn, B6). **KHÔNG tái lập được từ kho**; dựng lại từ đặc tả này là đủ; không phải mã của
  executor. Mọi con số ở bảng 9 mang nhãn "rig r7".
- **Luật nguồn của `B2-parse` phụ thuộc lời khai của executor** (tên hàm và chuỗi con của biểu thức tách). Nếu ứng
  viên tách trạng thái bằng một biểu thức không chứa chuỗi con nào riêng cho dòng ấy, hay tách qua nhiều dòng, thì
  cách so "hàm + nội dung" phải được executor điều chỉnh và khai; hành vi của luật trên một cách viết như thế:
  KHÔNG ĐO ĐƯỢC ở r7 (rig chỉ đo ứng viên nháp, biểu thức một dòng).
- **Răng của bộ sinh chỉ tới ngữ pháp của nó.** Bảng 8 báo 0 lỗ trên các dãy mệnh đề bộ sinh dựng; điều đó KHÔNG
  chứng minh mọi cách viết đều bị bắt. Không phủ: kiểm tra dữ liệu thay bắt ngoại lệ ngoài (l16); tên lớp con
  cụ thể của `OSError`/`Exception`/`BaseException` (ví dụ `TimeoutError`, `MemoryError`); errno thứ năm trở đi;
  mệnh đề `finally`; mệnh đề `else` gắn sai; mở rộng khối `try` sang câu lệnh khác. Mỗi cái là **KHÔNG ĐO ĐƯỢC**.
  Cũng ngoài ngữ pháp ấy, và r6 KHÔNG khai: nhánh cũ (cột Đ0) và quyết định tệp vắng; hỏi/đọc lại có điều kiện
  theo lớp ngoại lệ; cú pháp phép tách với `comm` chứa `)` — cross-review lượt 6 dựng được bản vá qua hết r6 + D +
  toàn suite ở cả ba chỗ; r7 phủ bằng bảng không gian mở rộng (B2), `B2-nhanh-cu` mười chín đầu vào, quy ước đếm
  theo đường, lời gọi đường cũ của `B3-zombie`, lớp (m) và phép (E).
- **Răng của phép (E) chỉ tới MỘT biến thể mỗi hạng mục, và chỉ MỘT lần.** 78 hạng mục của bảng không gian mở rộng
  có biến thể (E) chứ không có mục `DOT_BIEN`: răng của chúng được đo một lần trước merge trên mã của executor, rồi
  KHÔNG được `--dot-bien` đo lại ở các lượt sau (B4, B5). Một biến thể mỗi hạng mục không chứng minh mọi cách viết
  vi phạm hạng mục ấy đều bị bắt. Răng riêng của `B3-song` và `B3-da-wait` (không biến thể nào lấy làm đích):
  KHÔNG ĐO ĐƯỢC.
- PID con đã `wait` bị hệ điều hành tái dùng giữa lúc `wait` và lúc đo: xác suất KHÔNG ĐO ĐƯỢC. Khe này có
  sẵn ở `B1` và `B3-da-wait` và không do r5 mở ra; ở `B2-pid-du-phong` `da-wait`, nếu PID bị tái dùng thì
  `kill(pid, 0)` thật thành công và ca báo `TinHieuChotCa` cho một bản ĐÚNG (dương tính giả); 8 lời gọi
  chạy sát nhau, không có lần `wait` nào chen giữa. Chạy lại là cách phân biệt; ca không khoá được khe này.
