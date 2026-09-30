# ĐẶC TẢ — `LAUNCHER-CON-SONG-ESRCH` — **revision 11, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp685` (ID bền, `wp<issue>`); tên đọc được: `LAUNCHER-CON-SONG-ESRCH`. Lease dùng tên nào cũng phải kèm `packet_issue: 685`. |
| `revision` | **11** |
| `thay_the_cho` | r10 = `ops/specs/launcher-con-song-esrch-r10.md`, sha256 `e3ae8741732847902dd91985f8801424a83ab1ffee33724dd338c4250e4bde16`, commit `9887bfc` (`9887bfcdf556abb461c14871875b3ec002c8f7da`). Lúc soạn r11 commit ấy là CỤC BỘ (không là tổ tiên của `origin/master` `fc852ff`: `merge-base --is-ancestor` rc=1, 15:31Z 30-09, đo trên kho bare của rig r11); thứ định danh là sha256 cộng OID, không phải tên nhánh. Trước đó: r9 `1a629c89…a3cf` (`468c88e`); r8 đến r1: ô `thay_the_cho` của r10, r9 và r7. r1 đến r10 giữ nguyên, không sửa đè (phiên soạn r11 đo mười băm bằng `sha256sum` trước khi áp HINT và lúc đóng băng, khớp cả mười — §10); r11 là bản duy nhất được cấp lease. |
| `packet_issue` | **#685** |
| `mission_issue` | **#686** (Mission Issue, object ID `5628902742`). Thân #686 khai ngay đầu rằng nó do phiên agent đăng hộ chủ kho bằng credential chủ kho; nguồn thẩm quyền là các câu trả lời của chủ kho được trích trong đó (Q0–Q4 trong thân; Q5 ở comment `5888633201`, xem `nguon_cap_viec`). |
| `nguon_cap_viec` | (r1) Chỉ thị chủ kho 29-09-2026: *"mở packet riêng cho bản vá launcher (race ProcessLookupError) đi"*. Nguồn lỗi: PR #679, job `gate-ops (ubuntu-latest)` `109303373142`, phân tích ở PR #679 comment `5885963131`. (r2) đến (r10) Cross-review lượt 1 đến lượt 9 trên PR #688: nguyên văn ở ô này của r10 (sha256 `e3ae8741…4bde16`; ô ấy trỏ tiếp về r9, r8, r7), không chép lại. Còn hiệu lực từ (r9): **quyết định chủ kho** 2026-09-30T06:42:25Z, nguyên văn *"#688: ngay trong packet này"* — lỗi rc=124 do `comm` không giải mã được SỬA trong `wp685`; neo: PR #688 comment `5905670017` (phiên agent đăng hộ; r11 ĐỌC qua REST: comment có trên PR #688, đăng 2026-09-30T06:42:43Z, chứa đúng câu ấy — §10). **(r11)** Cross-review lượt 10 trên PR #688, reviewed commit `9887bfcdf556abb461c14871875b3ec002c8f7da` (r10, commit CỤC BỘ theo `quy_uoc_review`; spec sha256 khớp băm r10). Reviewer Claude Opus 5.5, effort max — **`advisory_review`, CÙNG HỌ với executor và phiên soạn, KHÔNG phải `cross_approved`**; họ model là tự khai. Kết luận `changes_requested`, **0 P1 / 1 P2 / 4 P3**: `ma-tran-loi-thieu-chot` (P2, TÁI PHÁT lần thứ chín), `b8-khung-ca-thieu-chot` (P3, vá của r10 sinh lỗi mới), `khoa-dinh-dang-khong-co-chot` (P3, phần dư), `khai-khong-do-duoc-ma-do-duoc` (P3, TÁI PHÁT), `required-checks-thieu-ten-context` (P3, mới). VERDICT sha256 `88538f7ccc333ed4a96cf8ad68de7fefd2b040590c55936690ffdd099da685f8`, `HINT.patch` sha256 `b67186af9065ffe335cde751000b41f8c6362d67aa856bd8f11e95193406ff1e`; phiên soạn r11 đo cả hai bằng `sha256sum` trước mọi việc khác, khớp. Comment PR #688 `5913959273`, đăng 2026-09-30T15:03:40Z (r11 đọc qua REST: có; thân comment không so từng byte với tệp VERDICT). **Quyết định chủ kho 2026-09-30 cho r11** (trả lời trắc nghiệm; lời điều phối cấp, không có neo GitHub — phiên soạn không kiểm được): nhãn đã chọn, nguyên văn *"Áp HINT, lặp tiếp (Recommended)"* — r11 = HINT lượt 10 (một hằng `comm` cho trục tách ba hàm, một thước đo đếm `open` cho trục API đọc, thay vì liệt kê API) rồi review lượt 11; nếu lớp `ma-tran-loi-thieu-chot` tái phát lần thứ mười thì DỪNG và thu hẹp (§11.2). Mission #686 comment `5888633201` (Q5, điều kiện cấp lease): r11 ĐỌC qua REST, ba điều kiện ở §11 mục 4. |
| `quy_uoc_review` | **(r8, chủ kho chốt 30-09; dữ kiện do phiên điều phối cấp, phiên soạn r8 không kiểm trên GitHub)** Từ r8, mỗi revision chỉ được commit CỤC BỘ và được review trên CHÍNH commit cục bộ ấy; PR chỉ được đẩy khi review ra **0 P1 / 0 P2 / 0 P3**. Thứ định danh revision là sha256 của tệp cộng OID commit, không phải tên nhánh. |
| `objective` | `_con_song` không bao giờ để một ngoại lệ `OSError` của phép hỏi `/proc/<pid>/stat` thoát ra; tiến trình biến mất giữa chừng (ESRCH) được báo là đã chết; lỗi khác KHÔNG được đọc thành "đã chết" chỉ vì không stat được, và một zombie vẫn được báo là đã chết khi nội dung `/proc/<pid>/stat` còn đọc được. **(r9, quyết định chủ kho 2026-09-30T06:42:25Z, lời điều phối cấp: "#688: ngay trong packet này")** Bốn chỗ đọc `/proc/<pid>/stat` của launcher — `_khoa_danh_tinh`, `_thanh_vien_nhom`, `_chup_cay` và hai khối đọc của `_con_song` — không bao giờ đọc một tiến trình CÒN SỐNG thành "đã biến mất", "đã chết" hay "không có khoá" chỉ vì `comm` không giải mã được hay locale không phải UTF-8 (Q-A.7): `run --deadline-utc` không trả 124 và `stop` không trả 0 khi tiến trình của cây còn sống, và tên chương trình không phải ASCII không làm lượt chạy trả 10 (B8). **(r10)** Khoá danh tính Linux giữ đúng định dạng nền `linux:<starttime>`, để `stop` của một bản launcher khác vẫn so được khoá trong `run.json` (Q-A.7). |
| `review_class` | **`sensitive`** — protocol §8: *"launcher hoặc gate lifecycle"*. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | `claude` — **Claude Sonnet 5.5, effort high** (Mission #686 Q3); phiên điều phối kiểm lại độc lập và commit. |
| `environment` | **`cloud`**. Bản vá chỉ chạm nhánh Linux của `_con_song` (nhánh Windows trả về trước dòng 650) và, từ r9, phép đọc `/proc` trong nhánh Linux của `_khoa_danh_tinh`, `_thanh_vien_nhom`, `_chup_cay` (Q-A.7). |
| reviewer | `codex` (`gpt-6-astra`, effort ≥ medium), cần `cross_approved`. Protocol §8: HINT không được chứa mã launcher; chỉ được chứa mã TEST thuần. (r7) Lượt 6 trên PR #688 — review ĐẶC TẢ, không phải review bản thi hành — do Claude Opus 5.5 làm theo chỉ định của chủ kho, hạng `advisory_review`; (r8 đến r11) lượt 7, 8, 9 và 10 cũng vậy (lượt 8 đến 10: effort max, thay codex hết quota). Các lượt ấy không thay yêu cầu `cross_approved` khác họ cho PR thi hành. |
| `depends_on` | Packet #668 (Mission #686 Q1: xếp sau #668) — **ĐÃ LAND** (PR #696, merge `423b4ba`). Lease cuối của nó, `ci-g5-cong-cu-chia-manh-r1-g3-claude`, đã rút hạn về `2026-09-30T09:55:00Z` (commit `86b23c0f5c2becf17ede9f951892a1d2b40df141`, đầu nhánh `ops/cap-lease-ci-g5-cong-cu-chia-manh`; đọc thẳng từ tệp lease). **Đo ở r10** (§8): `ai-dang-giu .claude/dev/launcher_test.py` ⇒ `NGƯỜI_GIỮ 0`, rc=0 (10:46:54Z 30-09; g1, g2, g3 của #668 đều `HẾT_HẠN`); `ai-dang-giu .claude/dev/launcher.py` ⇒ `NGƯỜI_GIỮ 0`, rc=0 (10:47:06Z). Không còn phụ thuộc lease nào đang giữ write set lúc đo. Hai tệp vẫn phải đo lại lúc cấp lease (Q5 điều kiện 1, §11 mục 4); r11 KHÔNG đo lại `ai-dang-giu`. (r11) Commit rút hạn `86b23c0` nay là tổ tiên của `origin/master` `fc852ff` (Merge PR #697). Số lease của r3 (người giữ 1, hạn 07:41Z): ô này của r9. |
| nền nghiệm thu | **(r10) DỜI sang `origin/master` `423b4ba14078701859b9e6ac101a68a3fc4ddef4`** (Merge PR #696, #668). Lý do, đo: `git -C <worktree> fetch -q origin master` rc=0 (10:45:10Z 30-09); `git ls-remote origin refs/heads/master` ⇒ `423b4ba…`; `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=1**. Diff (`git diff --stat`): chỉ `launcher_test.py`, 2 dòng thêm, 1 dòng xoá, trong `t152_hook_cai_dat_va_khop_al_ver_ci` (hunk `@@ -5997,7 +5997,8 @@`, dòng đổi là dòng 6000 trên `89fc4fa`): assertion đếm `AL_VER` trong `ci.yml` đổi từ 4 chỗ sang 5, cộng một dòng chú thích. `launcher.py` giữ blob `561ff7a1840d65a6fc9953947f71cabe4947b3c9` (sha256 `808ce5b3…9fc0`); `launcher_test.py` đổi blob `abf7f6ca…` ⇒ `3f02fb94abece5aa331f68fc890367cab50ac7a4` (sha256 `882ac43f…97cc`, 8355 dòng). Mọi số nền đo lại trên `423b4ba` ở §8 (số ca, hậu tố, `DOT_BIEN`, dòng runner, ruff, suite, CI). Nền `89fc4fa` vẫn là nền của mọi số đo hành vi `launcher.py` trong tệp này, vì blob `launcher.py` không đổi. Lượt đo nền của r3 đến r9: ô này của r9. **(r11) Nền GIỮ `423b4ba`**, đo: `git ls-remote origin refs/heads/master` ⇒ `fc852fff7da37f1669569572b79571446e61c294` (15:31:19Z 30-09); fetch vào kho bare của rig r11 (không đụng ref của worktree): `423b4ba` là tổ tiên của `fc852ff` (rc=0), 29 commit giữa hai đầu, `git diff --quiet 423b4ba fc852ff -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=0**, `git diff --stat 423b4ba fc852ff -- .claude .github` rỗng — write set và CI không đổi byte nào. Nền tiếp nối (continuation base): khai riêng lúc cấp lease (protocol §3.2.1); đầu `origin/master` còn trôi thì đo lại lúc ấy, theo cùng luật dời nền. |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/launcher-con-song-esrch-r11.md`, không loại dòng nào. Giá trị được công
bố **ngoài** tệp: comment trên #685 và lease, kèm OID commit + đường dẫn. Khối closure dưới đây
nằm **trong** tệp, nên một `spec_hash` không thể đi với hai closure khác nhau. Đổi bất kỳ byte nào
⇒ revision mới, băm mới, lease mới. Băm của r1 (`ee44238c…37d9`), r2 (`de9c553a…9ce4`), r3 (`7ef008f8…a895`),
r4 (`2c84a1bd…ae67`), r5 (`a0842320…7928`), r6 (`fadad3c7…3c99`), r7 (`3fc04fe5…5286`), r8 (`2ae6ee04…2aa3`),
r9 (`1a629c89…a3cf`) và r10 (`e3ae8741…4bde16`) KHÔNG còn dùng để cấp lease.

**Closure đóng băng** (các trường dispatcher dẫn xuất, protocol §3.2), điền tay theo **miễn trừ có
phạm vi** ở Mission Issue #686: chỉ `wp685`, hết hiệu lực ở lần đầu một policy canonical cho closure
xuất hiện trên nhánh mặc định.

| trường | giá trị |
|---|---|
| `change_policy_sha` | `null` — chưa có policy canonical; descriptor thay thế là miễn trừ ở #686 |
| `effective_write_set` | `.claude/dev/launcher.py` · `.claude/dev/launcher_test.py` (exact) |
| `effective_review_class` | `sensitive` |
| `required_checks` | Trên PR thi hành, **tên context** (r11 đọc bằng REST: run `36696528580` — lượt `push` master của `423b4ba`, workflow `gate`/`.github/workflows/ci.yml`, 14 job; run `36737283472` — workflow `thu-hoi`/`ops-thu-hoi-admission.yml`, `pull_request_target`, PR #602): `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-registry (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)`; hai job #668 thêm từ nền `423b4ba` — `gate-cong-cu-gop (ubuntu-latest)` và tám context của ma trận `gate-cong-cu`: `gate-cong-cu (ubuntu-latest, 0)`, `gate-cong-cu (ubuntu-latest, 1)`, `gate-cong-cu (ubuntu-latest, 2)`, `gate-cong-cu (ubuntu-latest, 3)`, `gate-cong-cu (ubuntu-latest, 4)`, `gate-cong-cu (ubuntu-latest, 5)`, `gate-cong-cu (ubuntu-latest, 6)`, `gate-cong-cu (ubuntu-latest, 7)`; và `thu-hoi` — các check này có thật và phải xanh (PR không nhãn chỉ có `ubuntu-latest`: job `chuan-bi`; run trên là lượt `push`, tên ở lượt PR đọc lại trên lượt chạy đầu của PR thi hành), nhưng **KHÔNG check nào trong số đó chạy `launcher_test.py`** (`gate-registry` chạy chín bộ thuộc `MOI`, không có `launcher_test.py`; xem §8). **Đỏ sẵn trên nền (r11 đo):** ở run `36696528580`, `gate-registry (ubuntu-latest)` (job `109832781748`) ĐỎ ở bước 11 `test registry (phạm vi + các bộ chưa được nối)` — log: `ops/nhanh_don_duoc_test.py` rc=-9 sau 4500,384 s, ngoài write set; nếu vẫn đỏ sẵn trên nền của PR thi hành thì ghi "đỏ sẵn, delta 0" kèm lượt nền (CLAUDE.md, Quy ước deploy mục 7), không sửa gì ngoài write set. Ngoài các check CI, **bắt buộc** bằng chứng cục bộ Linux B1–B6 và B8 neo exact candidate SHA, **chạy trên `python3.11` và `python3.12`** (B6; lệnh nguyên văn, giờ UTC, rc, dòng tổng), đính vào handoff và reviewer đọc trước merge; cross-review codex `cross_approved`, 0 P1/P2/P3 |
| `land_obligations` | Chủ kho audit + merge (không tự merge/approve); đọc kết quả `launcher-windows.yml` ở lượt `push` lên master sau merge, cả job Windows lẫn job Ubuntu, và báo — kể cả dòng `DOT BIEN:` của bước `Tu dot bien` trên Windows: `DUOI SAN` (dưới sàn 70 % của `--dot-bien`) là ĐỎ của packet này, không phải đỏ sẵn (§7 B4, r7); ghi sổ verdict + HINT vào `ops/reviews/` kèm receipt và mục README; thu hồi lease sau land; đóng #685 |

**Descriptor nguồn closure** = `{mission_issue: 686, object_id: 5628902742}`. Lease phải **chép**
đúng các giá trị trên; lệch ⇒ **DỪNG**. Neo bằng object ID + số Issue, vì thân Issue sửa được. (r11) Đường
đọc MCP chuẩn hoá thực thể HTML trong thân issue (CLAUDE.md), nhưng REST thì không: r11 đọc được `id` của #686 =
`5628902742` và băm thân `2af24e28…d9de` (§10) — ghi để đối chiếu, không thay neo.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

**Thay đổi so với r10** (mỗi dòng một lớp của VERDICT lượt 10, hồ sơ cross-review PR #688; slug là tên lớp trong bảng
lớp của VERDICT). r11 áp `HINT.patch` lượt 10 (5 nhóm `# lop:`, 28 hunk, 381 dòng / 37 770 byte, sha256
`b67186af…ff1e`) lên bản sao r10 theo chỉ thị điều phối: `cp` r10 thành r11, đổi tên tệp trong HINT bằng `sed -E` (biểu
thức của chỉ thị; mười lần nhắc tên tệp trong HINT đều nằm trên dòng tiêu đề `---`/`+++` — đo bằng `grep`), đưa qua
`patch -p0 --fuzz=0` từ gốc worktree. Kết quả: **rc=0**, năm lần `patching file`, bảy hunk báo offset (mỗi nhóm là diff
độc lập với r10), 0 fuzz, không tệp `.orig` hay `.rej`, 2442 dòng / 279 045 byte, sha256 bản chỉ-HINT
`6cc5e18ebf30c2a10583198436e4472e32e28e8984cef6d35b7c78a07d500ad6` — trùng bản gộp VERDICT lượt 10 khai, và trùng
(`cmp`) bản áp lên một bản sao r10 trong scratchpad trước đó; r1 đến r10 nguyên byte; `git status --short` chỉ có tệp
r11. r11 KHÔNG dừng ở HINT: với mỗi lớp, phiên soạn TỰ LIỆT KÊ hết đường vào trước khi vá (bài học CLAUDE.md "vá đúng chỗ
được chỉ rồi bỏ sót đường thứ ba"); cột phải ghi phần r11 thêm hay THAY. Số đo của r11: bảng 13 (§1). Quyết định chủ
kho cho lượt này: §11 mục 2.

| slug lớp | hạng | chỗ sửa trong r11 |
|---|---|---|
| `ma-tran-loi-thieu-chot` | P2 (TÁI PHÁT, lần thứ chín) | HINT: `_K124_COMM_CHAU` cho cháu `t160`/`t161` (trục S ở ba hàm ngoài); `read args` đếm sự kiện audit `open`; sáu tên (E) `s_*_tach_ngoac_dau`, `g_khoa_open`, `g_nhom_open`, `g_chup_open`; Q-A.7 luật tách theo `)` cuối và "mọi API". r11 liệt kê năm chỗ đọc × hai trục (S: `)` đầu, khoảng trắng; API: sáu đường a1–a6) thành bảng có thẩm quyền ở B2, mỗi ô một đầu vào, một chốt, một tên (E), một số đo, và đóng cả loạt bốn đường HINT không phủ: (1) API ở hai khối đọc của `_con_song` — không có ô, không có tên (E) (thước đo của HINT có bắt `g_d0_open` ở B8 dù HINT chỉ khai ba hàm ngoài — đo; `g_d_open` chỉ helper bắt) ⇒ hai tên `g_d0_open`, `g_d_open` (chốt: seam đếm đọc của helper; `g_d0_open` còn bị cửa sổ B8 bắt); (2) đường `/proc/<pid>/task/…` và (3) fd ống của tiến trình con — thước đo `open` đổi từ "đếm BẰNG số lời đọc trên `/proc/<số>/stat`" sang "không `open` nào trên `/proc/…`, đường tương đối hay fd số NGOÀI lời đọc đã ghi" (đường tuyệt đối không bắt đầu bằng `/proc/` không tính: phòng xa lần nạp module lười, giá là `//proc/…` lọt thước đo này — chốt tĩnh bắt; đo cả hai); (4) phần còn lại của ba hàm ngoài (phạm vi bắt, số lần đọc, fd mở trước) — CHỐT TĨNH so dòng với nền. Đường khoảng trắng của trục S dùng chung đầu vào và chốt, đo trên rig, không thêm tên. DS-E-KHAC 33 → 35; bộ (E) 118; danh sách 120 tên |
| `b8-khung-ca-thieu-chot` | P3 (vá của r10 sinh lỗi mới) | HINT: `n2 >= 1200` và `_giet_cay` quá 60 s ⇒ lỗi thường. r11 THAY cả hai, theo chỉ thị điều phối "ca phải ĐỎ khi con chết vì hết hạn thay vì bị giết": dấu tự thoát do chính con/cháu ghi ở `finally` (ca không phải cha nên không đọc được mã thoát); mẹ của `t160` là con trực tiếp nên đọc bằng mã thoát (`poll()`); (1) của `t160` tính cả mẹ. Tự liệt kê bốn đường "không bị giết mà trông như đã chết" cộng một đường điều kiện dựng; mỗi đường một chốt và một đột biến rig (`WAITK`, `KILLNEVER`, `MEHAN`, `MEBO`; probe cho `ngoai_le`) |
| `khoa-dinh-dang-khong-co-chot` | P3 (phần dư) | HINT: định nghĩa (E) cho dạng latin-1 (`!r`). r11: định nghĩa CHUNG cho cả hai dạng; tự liệt kê hai dạng × ba tổ hợp vị trí = sáu bản, đo cả sáu trên khối r11 ở ba Python; nơi SO khoá không dựng khoá nên không có hàng riêng |
| `khai-khong-do-duoc-ma-do-duoc` | P3 (TÁI PHÁT) | HINT: thay hai lời khai §10 bằng số của reviewer. r11 ĐO LẠI cả hai bằng phép đo của chính phiên soạn, rồi rà MỌI lời khai "KHÔNG ĐO ĐƯỢC"/"CHƯA ĐO" còn lại: đo được thì đo — `kill` EACCES dưới uid 65534 (mục 4 danh sách bất khả thi), kiểm dữ liệu ở nhánh cũ (mục 8), kênh GitHub phía đọc, dạng bytes qua helper, nhóm "dữ kiện điều phối cấp" (REST); chưa dựng thì đổi nhãn thành CHƯA ĐO kèm lý do |
| `required-checks-thieu-ten-context` | P3 (mới) | HINT: `gate-cong-cu-gop (ubuntu-latest)` và "tám context đọc lại sau". r11 đọc tên THẬT bằng REST trên run `36696528580` (chỉ thị điều phối): tám `gate-cong-cu (ubuntu-latest, 0)` … `(ubuntu-latest, 7)`; tự liệt kê MỌI mục của ô: `thu-hoi` cũng chưa phải tên context ⇒ đọc trên run `36737283472`; ghi `gate-registry` đỏ sẵn trên lượt push master `423b4ba` |
| (không phải lớp) nền, dữ kiện GitHub, quyết định | — | `origin/master` trôi sang `fc852ff`, write set và CI không đổi ⇒ nền giữ `423b4ba`; dữ kiện "điều phối cấp" đọc được qua REST (§10); quyết định chủ kho *"Áp HINT, lặp tiếp (Recommended)"* và điểm dừng (§11 mục 2); Q5 (§11 mục 4) |

**Lịch sử r1 → r10** — không chép lại. Bảng "Thay đổi so với r9" nằm nguyên văn ở đầu r10 (sha256 `e3ae8741…4bde16`);
các bảng trước đó ở r9 (sha256 `1a629c89…a3cf`), r8 (sha256 `2ae6ee04…2aa3`), r7 (sha256 `3fc04fe5…5286`) và r6
(sha256 `fadad3c7…3c99`), như r10 đã trỏ. Các tệp ấy bất khả xâm phạm, cùng thư mục.

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

**Bảng 8, 9, 10 — số đo của phiên soạn r6, r7, r8 trên rig riêng** (prototype, KHÔNG phải ứng viên của executor):
nguyên văn ở §1 của r8 (sha256 `2ae6ee04…2aa3`), kèm "Đính chính bảng 8" của r7 và đoạn "Không chạy lại ở r8" —
không chép lại (r9, thu gọn). Mọi chỗ trong tệp này viết "bảng 8", "bảng 9" hay "bảng 10" (kèm số dòng) trỏ vào đúng
bảng ấy của r8, cùng số dòng. Chúng là số ĐO của bản nháp theo r6–r8; ràng buộc hiện hành nằm ở §3 và §7, không ở đó.

**Bảng 11 — số đo của phiên soạn r9 trên rig riêng (r9 thêm; KHÔNG phải ứng viên của executor)**

Rig r9: thư mục `mktemp -d` trong scratchpad của phiên soạn, ngoài kho. Nền: `git archive 89fc4fa .claude/dev` (blob
`561ff7a1…`, `abf7f6ca…`, đo bằng `git hash-object`). Ứng viên nháp ESRCH: bản nháp theo r8 của reviewer lượt 8 (chép;
cùng ứng viên nháp r7–r8). **Ứng viên nháp Q-A.7** (dạng `read_text(encoding="latin-1")` ở năm lời đọc): phiên soạn
dựng lại độc lập bằng thay chuỗi, **trùng từng byte** (`cmp`) bản nháp latin-1 của reviewer lượt 8; M1–M5, M12 cũng
trùng từng byte bản reviewer; ba biến thể `errors="surrogateescape"` mới. Helper: helper của reviewer lượt 8 (chép)
đặt mặc định r9 (payload theo dõi, loại (2) như r7, `B2-dem-doc 4` kill 0, đuôi `e1 ba`) cộng loại `read args` do
phiên soạn r9 cài. Bốn ca B8: khối mã test ở mục B8 (trùng byte). `_con_song_that` đọc bytes. `PYTHONDONTWRITEBYTECODE=1`;
con dọn bằng PID tường minh, kiểm cuối 0 tiến trình sót. Ba Python 3.11.15, 3.12.3, 3.13.12 (UTF-8 mode), trừ khi ghi
khác; giờ UTC 30-09-2026. Mã rig không nằm trong đặc tả (protocol §8).

| # | phép đo | kết quả | giờ UTC |
|---|---|---|---|
| 1 | bốn ca B8 × 12 bản | ma trận ở mục B8, **trùng từng ô ở ba Python**; mọi ô đỏ là `TinHieuChotCa` đúng ca và đúng loại | 09:03:39Z–09:11:54Z |
| 2 | `t156`/`t157` trên helper r9 | ứng viên nháp Q-A.7: SONG, SONG; nền: `B1 seam escaped`, `B3b-giet-cay seam escaped`; ứng viên nháp theo r8: `B2-eacces read args [((), {})]`, SONG | 09:12:09Z; 09:13:26Z; 09:14:56Z |
| 3 | A1/A2/W1/W0 cho 54 dòng, 55 cặp | **55/55** được chấp nhận | như dòng 2 |
| 4 | (E) trên ứng viên nháp Q-A.7 | bộ r8 chép từ rig phiên soạn r8 (93 dòng: 78 hạng mục cùng 15 dòng khác, chạy trên bản sao ứng viên mang đúng các dấu neo của bộ ấy) **93/93**; bộ r9 trọng tâm **33/33** (34 cặp); tách trong hàm trợ giúp **4/4**; B8: dòng 1. Ánh xạ vào (E) mục 6: **111/111 tên có phép đo đúng kỳ vọng** ở ba Python (và 23 dòng đo thêm ngoài danh sách — quét và lặp — cũng đúng). Trong đó: fp, fp2–fp6, fp6b, khác đối số và hai phép giả gọi lại hàm trợ giúp VÔ CAN ở A1, W1, W0; (j1) VÔ CAN (`LookupError`); `d0_value_thoat`, `d0_decode_thoat`, `d0_index_thoat` CHẤP NHẬN; mười hai dạng đọc lệch (`errors=` bốn cách, `cp1252`, `encoding="utf-8"` tường minh; × Đ0, Đ) và M4, M5 chết `read args` ở đầu vào đọc đầu tiên (A1 `B2-dem-lan` hay `B2-eacces`; W1 `B2-nhanh-cu song` hay `B2-eacces`); `d0_giai_ma_lai_utf8` ⇒ `B2-nhanh-cu utf8-hong-that result False`; `d_giai_ma_lai_utf8` ⇒ `B2-dem-doc 4 kill count 1` (W1 `B3-zombie result True`); hai đối chứng sống SONG | như dòng 2 |
| 5 | phép D | bản đúng xanh (`t156` 56 đơn vị, `t157` 1, đúng thứ tự); **65/65 control đỏ**, báo đúng đơn vị thiếu; **6/6** phép đảo `missing=[]`, `order=False`; control RỖNG bị đánh "không đỏ đúng" | như dòng 2 |
| 6 | danh sách ĐÓNG, trích bằng máy từ CHÍNH tệp này (3.12.3) | (E) mục 6: 83 + 26 + 2 = 111 tên, 0 trùng, số đếm khớp dòng đầu nhóm; 78 tên trích theo luật của reviewer lượt 8 từ bảng mở rộng r9 nằm trong 83 (5 còn lại: trục G); 65 khoá control của D trích từ thứ tự thực thi và bảng tiểu nhãn; phép so tập tên: đủ ⇒ XANH, thiếu / thừa / lặp / đổi tên một dòng ⇒ ĐỎ, cả (E) lẫn D | 09:29:51Z |
| 7 | kênh git cục bộ | ba tập lệnh rig (231 / 162 / 174 ký tự `'` `"` `<` `>`) qua commit, push, clone, `git show <OID>:<tệp>`: sha256 khớp cả ba. GitHub thật: KHÔNG ĐO ĐƯỢC | 09:20:45Z |
| 8 | B6, 3.12.3, hai vế trong MỘT lệnh (mỗi vế: clone từ worktree, checkout `5f7485c`, `core.abbrev` 7, chép tệp của vế, chạy) | nền `187/188 ca DA CHAY QUA (tong 189, bo qua 1, hong 1)`; ứng viên nháp + helper r9 + bốn ca B8: `193/194 … (tong 195, bo qua 1, hong 1)`; hỏng duy nhất ở cả hai vế `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` (đỏ sẵn) ⇒ **delta 0**; `--dot-bien` `176/176 dat (1 khong do duoc)` cả hai vế, hạng 176 mục cũ giống hệt, 7 dòng có kiểu ngoại lệ trong ngoặc ở CẢ hai vế (nền, không phải delta) | 09:16:54Z–09:22:08Z |
| 9 | ruff F (nhị phân `ruff` 0.15.8; `python3.12 -m ruff` vắng) | nền 5 F841, ứng viên nháp + helper r9 + B8: 5 F841, cùng năm dòng ⇒ delta 0 | 09:21:56Z |
| 10 | `git grep` trên `5f7485c` mọi lời đọc `/proc/…/stat` | ngoài `launcher.py`: đúng ba chỗ của §5; cộng `launcher_test.py:2142` (`/proc/1/comm`, chẩn đoán môi trường) | 09:20:53Z |

Không chạy lại ở r9: phép đo `stop`, locale ASCII, khoá không đổi định dạng và `cp1252` (số của lượt 8, ghi tại chỗ);
payload `bytes` qua helper; sàn Windows (suy ra từ bảng 9 dòng 10). Lời khai r9 "locale giải mã được 15 byte (Latin-1
thật): KHÔNG ĐO ĐƯỢC" là SAI (cross-review lượt 9, lớp `khai-khong-do-duoc-ma-do-duoc`): `localedef -i en_US -f
ISO-8859-1 <thư mục>/en_US.ISO-8859-1` chạy được (reviewer: không cần root — §10), và `LOCPATH=<thư mục> LC_ALL=en_US.ISO-8859-1
PYTHONUTF8=0` cho `locale.getpreferredencoding(False)` = `ISO-8859-1` ở ba Python; trong locale ấy `t158` của khối r9
QUA trên launcher NỀN — ca có mặt mà không đo (sửa ở B8). Cơ chế payload theo dõi dạng `bytes` cũng đo được (lượt 9, ba
Python: cùng bảng phân hạng với `str`); qua helper đầy đủ: chưa đo. Số đo r10 của cả hai: bảng 12.

**Bảng 12 — số đo của phiên soạn r10 trên rig riêng (r10 thêm; KHÔNG phải ứng viên của executor)**

Rig r10: thư mục `mktemp -d` trong scratchpad của phiên soạn, ngoài kho; `TMPDIR` đặt vào trong rig;
`PYTHONDONTWRITEBYTECODE=1`. Nền `423b4ba` (`git show`). Ứng viên nháp và biến thể `launcher.py`: CHÉP từ rig
cross-review lượt 9 (chỉ đọc), kiểm bằng `diff` trước khi dùng — `cand_a` (latin-1) và `cand_b` (bytes) so nền 20 và 36
dòng; M1–M5, ba `surrogateescape` mỗi bản 2 dòng so `cand_a`, M12 4 dòng; `cand_split` (tách khối kill K0) 12 dòng thêm
so `cand_a`; `WK` (bỏ giải mã ở cả hai chỗ dựng khoá) 4 dòng, `WK1` và `WK2` (một chỗ) 2 dòng so `cand_b`; `WC_crash`
(launcher ném `RuntimeError` khi `comm` không ASCII, tức chết `rc=1`). Phiên soạn r10 tự dựng thêm `P701` = `cand_b` với
f-string lồng cùng loại dấu nháy ở `_khoa_danh_tinh` (cú pháp PEP 701, chỉ hợp lệ từ 3.12). `launcher_test.py` thử =
nền `423b4ba` + `_con_song_that` đọc bytes + khối B8 **trích bằng máy từ chính tệp r10** + helper `t156`/`t157` của
rig r9 (chép, sha256 `635d93fa…0494`); hai bản `DANG_DOC_QA7` (latin-1, bytes). Ô: `TH` = `TinHieuChotCa` (ghi LOẠI),
`VO_CAN` = lỗi thường, `BO_QUA`, `QUA`. "sót" = tiến trình mang dấu của con/mẹ/cháu B8 còn trong `/proc` sau mỗi bản.
Ba Python 3.11.15, 3.12.3, 3.13.12; giờ UTC 30-09-2026.

| # | phép đo | kết quả | giờ UTC |
|---|---|---|---|
| 1 | bốn ca B8 (khối r10, 281 dòng) × 18 bản, ba Python | mười một bản của bảng B8 (nền, `cand_a`, M1–M5, M12, ba `surrogateescape`) **trùng TỪNG Ô bảng B8** ở cả ba Python; `cand_b`, `cand_split` QUA ×4; `WK` QUA / QUA / `khong giet duoc` ("khoa danh tinh KHAC") / QUA; `WK1` QUA / QUA / `khong giet duoc` (khoá KHÁC) / `124 noi doi`; `WK2` QUA / QUA / `124 noi doi` / `124 noi doi`; 0 ô lệch giữa ba Python | 10:52:31Z–11:03:48Z |
| 2 | launcher chết vô can (`WC_crash`, rc=1) và cú pháp PEP 701 (`P701`) qua bốn ca B8 | `WC_crash`: bốn ô lỗi thường ở ba Python — `t158`, `t159` là `RuntimeError: dieu kien dung: launcher khong ket thuc bang ma han chot 124/125/10 kem so JSON: rc=1`; không ô nào là `TinHieuChotCa`. `P701`: ở 3.11 bốn ô lỗi thường (`t158`, `t159` cùng lỗi điều kiện dựng, stderr là `SyntaxError`; `t160`, `t161` `SyntaxError` khi nạp launcher); ở 3.12 và 3.13 QUA ×4 — chỉ vế 3.11 bắt được | như dòng 1 |
| 3 | `P701` ngoài suite; ruff | `python3.11 P701.py --help` rc=1 `SyntaxError: f-string: unmatched '('`; 3.12, 3.13 rc=0. `ruff check --select F`: mặc định `All checks passed!`, `--target-version py311` 1 lỗi (`invalid-syntax … on Python 3.11`); `cand_a`, `cand_b`, nền: 0 lỗi ở cả hai chế độ | 11:00:11Z |
| 4 | hạn sống của con B8 (mã do `_k124_ma_con` sinh, chạy một mình, không ai giết; 3.11.15) | tự thoát rc=0 sau 120,4 s, đúng 1200 nhịp | 10:52:43Z–10:54:44Z |
| 5 | điều kiện dựng hỏng: dòng `prctl` của cháu thay bằng `pass` | `t160`, `t161`: lỗi thường `dieu kien dung: comm cua chau chua doi`, 0 tiến trình sót, ba Python | 11:03:56Z–11:04:50Z |
| 6 | locale ISO-8859-1 (`localedef -i en_US -f ISO-8859-1` vào `LOCPATH` trong rig, rc=0; `LC_ALL=en_US.ISO-8859-1 PYTHONUTF8=0` ⇒ `getpreferredencoding(False)` = `ISO-8859-1` ở ba Python) | `t158`, `t159` BỎ QUA có khai ở mọi bản; `t160`, `t161`: nền và M12 `read args`, `cand_a` QUA, `WK` `t160` `khong giet duoc` (khoá KHÁC) — không phụ thuộc locale; `t156` trên `cand_a`: lỗi thường `dieu kien dung: read_text() giai ma duoc 15 byte`; ba Python | 10:59:09Z; 11:03:56Z–11:05:11Z |
| 7 | helper `t156`/`t157` (helper r9) trên hai cấu trúc khối kill, ba Python | `cand_a` (dùng chung) và `cand_split` (tách K0): SONG, SONG; đếm AST `os.kill` (`_con_song` cộng hàm nó gọi trực tiếp) 1 và 2. `k0_ESRCH_sai`, `k0_EPERM_sai`, `k0_EIO_sai`: trên `cand_a` chết ở nhãn đứng trước `B2-pid-du-phong` (`da-wait result True`, `eperm result False`, `eio result True`), trên `cand_split` chết đúng `B2-nhanh-cu` (`vang-da-wait result True`, `vang-eperm result False`, `vang-eio result True`); `t157` QUA ở cả sáu | 11:03:51Z–11:04:49Z |
| 8 | tiến trình sót sau mỗi bản (quét `/proc`, dấu của con/mẹ/cháu B8) | 0 ở mọi dòng 1–7, TRỪ chín bản đầu của lượt 3.11 dòng 1: `SOT=1`, chính PID của phép đo dòng 4 chạy song song (PID trùng tệp PID của nó), tự thoát ở hạn sống; lượt 3.11 chạy lại riêng: 0 ở cả mười hai bản, ma trận trùng lượt đầu từng ô; quét cuối toàn `/proc` (11:17:02Z): 0 | 11:05:12Z–11:07:58Z |
| 9 | danh sách ĐÓNG (E) mục 6, trích bằng máy từ tệp r10 | `DS-E-HANG-MUC` 83/83, `DS-E-KHAC` 27/27, `DS-E-C3` 2/2, tổng 112, 0 trùng | 11:18:37Z (lúc đóng băng) |
| 10 | nền `423b4ba` (§8) | AST: 189 ca = 155 `t` + 34, hậu tố lớn nhất 155; `DOT_BIEN` 174 (`:7013`), `DOT_BIEN_HARNESS` 3 (`:7931`); ruff 0 / 5 F841 ở cả hai chế độ; `_dot_bien_du_san`: (231, 65) đạt, biên 4 · (237, 65) đạt, biên 6 · (237, 71) đạt, biên 0 · (238, 66) đạt, biên 5 · (238, 72) KHÔNG đạt | 10:47Z–10:47:54Z |
| 11 | `git grep` trên `423b4ba` | chuỗi `linux:` trong `launcher.py`: đúng `:362`, `:494`; lời đọc `stat` ngoài `launcher.py`: đúng `gate_lifecycle.py:906`, `:933`, `ci_dang_ky_test.py:913` | 11:05:12Z |
| 12 | B6, hai vế trong MỘT lệnh cho mỗi Python (mỗi vế: clone từ clone sạch, checkout `423b4ba`, `core.abbrev` 7; vế sau chép `cand_a` và `launcher_test.py` thử) | `python3.11`: nền `188/188 ca DA CHAY QUA (tong 189, bo qua 1, hong 0)` rc=0; nháp `194/194 … (tong 195, bo qua 1, hong 0)` rc=0. `python3.12`: nền `187/188 … (tong 189, bo qua 1, hong 1)` rc=1; nháp `193/194 … (tong 195, bo qua 1, hong 1)` rc=1. Bỏ qua duy nhất ở mọi vế: `t62` (fixture Windows); hỏng duy nhất ở cả hai vế 3.12: `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` (đỏ sẵn ở 3.12, XANH ở 3.11 — nền khác nhau theo bản Python, đúng lý do phải so delta trong CÙNG một bản). **Delta 0 ở cả hai Python.** Vế nháp: `launcher.py` sha256 `2b93bc1e…1c0e` (`cand_a`), `launcher_test.py` sha256 `6fe7f02c…0f79`. `--dot-bien` hai vế: KHÔNG chạy lại ở r10 | 11:08:02Z–11:16:34Z |

**Bảng 13 — số đo của phiên soạn r11 trên rig riêng (r11 thêm; KHÔNG phải ứng viên của executor)**

Rig r11: thư mục `mktemp -d` trong scratchpad của phiên soạn, ngoài kho; `TMPDIR` trong rig, riêng cho mỗi bản;
`PYTHONDONTWRITEBYTECODE=1`. Nền `423b4ba` (`git show`; `launcher.py` sha256 `808ce5b3…9fc0`, `launcher_test.py`
`882ac43f…97cc`). Bản nháp `launcher.py`: 46 bản CHÉP từ rig cross-review lượt 10 (chỉ đọc; `nen` bằng nền từng byte;
mọi bản kiểm bằng phép so dòng theo hàm với nền), cộng 16 bản phiên soạn r11 dựng bằng tập lệnh thay thế có neo (mỗi
neo đúng một lần): `g_d0_open`, `g_d_open`, `SW_khoa`, `SW_nhom`, `SW_chup`, `SW_d0`, `SW_d`, `CAT_khoa`, `TASK_khoa`,
`DIRFD_khoa`, `SL2_khoa`, `ZB_nhom`, `ZB_chup`, `MEBO`, `MEHAN`, `D0_KIEMDL` — 62 bản. Khối B8: trích bằng máy từ
CHÍNH tệp r11 (351 dòng, `950b880a…7bad`); để đối chiếu còn khối r10 (`893b31ce…8366`, trích từ tệp r10), khối bản gộp
HINT (`b929f2b1…091a`, trích từ bản chỉ-HINT) và bản nháp đầu của khối r11 (thước đo `open` tính mọi đường). Helper:
helper r9 (`635d93fa…0494`) tách từ tệp thử của rig r10 — dựng lại tệp ấy đúng từng byte. Tệp test thử: nền
`423b4ba` + `_con_song_that` đọc bytes + khối B8 r11 + helper (latin-1 `c4267574…7905`, bytes `6f07a7cf…3ed8`).
Bộ lái gọi thẳng hàm ca, đặt `PR_SET_CHILD_SUBREAPER` rồi thu hồi mọi hậu duệ mồ côi SAU ca cuối (zombie vẫn nằm trong
`/proc` suốt lúc ca chạy, như dưới PID 1 của container — ngữ nghĩa ca không đổi; các ô trùng bảng 12 và lượt 10 từng
ô). Ô: `TH` = `TinHieuChotCa` (ghi LOẠI), lỗi thường, `BO_QUA`, `QUA`. Ba Python 3.11.15, 3.12.3, 3.13.12; giờ UTC
30-09-2026.

| # | phép đo | kết quả | giờ UTC |
|---|---|---|---|
| 1 | bốn ca B8, khối r11, 54 bản × ba Python | 11 hàng cũ của bảng B8, ba hàng r10 (`WK`, `WK1`, `WK2`) và ba bản latin-1 (`WKa`, `WKa1`, `WKa2`) TRÙNG TỪNG Ô bảng 12 và lượt 10; `cand_a`, `cand_split`, `cand_b`, `cand_b_split` QUA ×4; chín `SX*` và ba `SW_*` của ba hàm ngoài: `_khoa_danh_tinh` ⇒ `t160`, `t161` `124 noi doi`, `_thanh_vien_nhom` ⇒ `t161` `124 noi doi`, `_chup_cay` ⇒ `t160` `124 noi doi`, `t161` `khong giet duoc`; mười `OPEN*`/`PATHOPEN`, `TASK_khoa`, `CAT_khoa`, `g_d0_open` ⇒ `t160`, `t161` `read args` (`open ngoai loi doc Path`); `RTcp1252_khoa` ⇒ `read args` (đối số); `g_d_open`, `SW_d` QUA ×4 (B8 không chạm đường mới); `SW_d0` ⇒ `t160`, `t161` `khong giet duoc`; `ZB_nhom` ⇒ `t158`, `t159` `qua han khong giet duoc`, `t160` `khong giet duoc`; `ZB_chup` QUA ×4; `MEBO` ⇒ `t160` `124 noi doi` (mẹ sống); `WC_crash` bốn ô lỗi thường; `P701` 3.11 bốn ô lỗi thường, 3.12/3.13 QUA ×4; **0 ô lệch giữa ba Python ngoài `P701`**; bộ lái thu hồi 2–4 con mồ côi mỗi bản, 0 con còn sống lúc hết ca | 15:50:44Z–16:03:21Z |
| 2 | thước đo `open` — đối chiếu | khối HINT (3.12): `TASK_khoa`, `CAT_khoa` QUA ở `t160`, `t161`; `g_d0_open` `read args ['open ngoai Path: 51829 su kien open, 51783 loi doc Path']`; khối r11: ba bản ấy `read args` (dòng 1); `DIRFD_khoa` ⇒ `read args` (sự kiện `'/proc/<pid>'`, `'stat'`), ba Python; `SL2_khoa` (`//proc/…`) ⇒ QUA ở `t160`, `t161`, ba Python — giá đã khai của bộ lọc; bản nháp đầu của khối r11 (tính mọi đường) với `_k124_khoa_that` không giải mã ascii (biến thể rig của khối): `cand_a`, `cand_b` QUA ở `t160`, `t161`, ba Python — KHÔNG có đỏ oan; khối r11 cùng biến thể: QUA; log của `TASK_khoa` trên bản nháp đầu ghi `…/encodings/__pycache__/latin_1.cpython-312.pyc` (3.12) — nạp module lười trong cửa sổ; `encodings.ascii`, `encodings.latin_1` không có trong `sys.modules` lúc khởi động (locale UTF-8, ba Python) và vẫn không có ngay trước cửa sổ | 15:50:44Z–16:05:29Z |
| 3 | khung ca, ca chậm, khối r11, ba Python | `nen_WAITK` và `M12_WAITK`: `t158` `qua han khong giet duoc` (rc=124, `tu thoat=han_song`, 122,1–122,2 s), `t159` `qua han khong giet duoc` (rc=10, `han_song`, 121,6–121,7 s); `cand_a_WAITK`: QUA ×2 (4,4–4,5 s); `KILLNEVER`: `t160` `khong giet duoc` (`chau tu thoat=han_song`, `me rc=-15`, 120,3–120,5 s), `t161` `khong giet duoc` (`han_song`, 120,1–120,2 s); `MEHAN`: `t160` `khong giet duoc` (`chau tu thoat=None`, `me rc=0`, 127,2–127,3 s); `MEBO`: `t160` `124 noi doi` (`me rc=None`, 2,5 s); 0 con sống lúc hết ca | 16:04:19Z–16:18:49Z |
| 4 | khung ca — đối chiếu trên khối HINT và r10 (3.12) | khối HINT: `MEBO` `t160` QUA; `MEHAN` `t160` lỗi thường `dieu kien dung: _giet_cay qua 60 s …` (127,2 s); `KILLNEVER` `t160` cùng lỗi thường (120,4 s); khối r10: `MEBO`, `MEHAN` `t160` QUA (`MEHAN` 127,2 s) — cả ba đường xanh hay lỗi thường trên khối cũ, ĐỎ đúng loại trên khối r11 (dòng 3); lượt 10 (VERDICT) đo `nen_WAITK`, `M12_WAITK` trên khối r10: `t158` QUA sau 122 s | 16:04:19Z–16:08:51Z |
| 5 | dấu tự thoát — probe gọi thẳng mã khối (3.12) | con: SIGTERM rc=-15 và SIGKILL rc=-9 ⇒ không dấu; tệp `comm` không ghi được ⇒ rc=1, dấu `ngoai_le`, `_k124_ket_luan` ném `RuntimeError: dieu kien dung …` (không phải `TinHieuChotCa`); cháu: SIGTERM ⇒ vẫn sống, không dấu, SIGKILL rc=-9 ⇒ không dấu; hết hạn: con rc=0 sau 120,4 s, 1200 nhịp, dấu `han_song`; cháu rc=0, dấu `han_song` | 15:47:29Z; 16:04:19Z–16:06:23Z |
| 6 | helper `t156`/`t157` (tệp test thử latin-1), ba Python | `cand_a`, `cand_split` SONG, SONG; nền `B1 seam escaped`, `B3b-giet-cay seam escaped`; M4 `B2-dem-lan read args`, M5 `B2-eacces read args`; `g_d0_open` `B2-nhanh-cu song read count 0`; `g_d_open` `B2-eacces read count 0`; `SW_d0` `B3-zombie result True`; `SW_d` `B2-parse p2 kill count 0`; `D0_KIEMDL` `B2-nhanh-cu p3 parse error escaped (IndexError …)`; `t157` QUA ở mọi bản trừ nền | 15:52:11Z–15:57:20Z |
| 7 | helper, dạng bytes (tệp test thử bytes) | `cand_b`, `cand_b_split`: `t156` `B2-eacces read count 0`, `t157` QUA, ba Python — helper của phiên soạn chỉ seam `read_text` | 15:55:55Z |
| 8 | chốt tĩnh phần còn lại, 62 bản | chạy bằng 3.11: 44 ĐỎ, 18 ĐẠT (danh sách ở B2); 3.13 khác đúng một dòng: `P701` ĐẠT | 16:05:53Z |
| 9 | điều kiện dựng hỏng: dòng `prctl` của cháu thay bằng `pass` | `t160`, `t161`: lỗi thường `dieu kien dung: comm cua chau chua doi`, 0 tiến trình sống lúc hết ca, ba Python | 16:04:43Z |
| 10 | locale | `setpriv --reuid 65534 --regid 65534 --clear-groups`: `uid` trong tiến trình 65534; mở thẳng đường dẫn của thư mục đích bị chặn (thư mục cha 0700); `localedef -i en_US -f ISO-8859-1 /proc/self/fd/7/en_US.ISO-8859-1` rc=0, tệp thuộc `nobody`; `localedef -i ru_RU -f KOI8-R` / `CP1251` / `ISO-8859-5` rc=0; `LOCPATH=… LC_ALL=… PYTHONUTF8=0` ⇒ `getpreferredencoding(False)` đúng tên, giải mã được 15 byte `_K124_COMM` ở cả năm locale, ba Python; bốn ca B8 (3.12) trên nền, `cand_a`, `cand_b`, M12, `WK`, `OPENl1_khoa` trong bốn locale giải mã được (ISO-8859-1 dựng bằng uid 65534, KOI8-R, CP1251, ISO-8859-5): ô Y HỆT nhau ở cả bốn — `t158`, `t159` BỎ QUA có khai; `t160`, `t161`: nền và M12 `read args [('read_text', (), {})]`, `cand_a`, `cand_b` QUA, `WK` `t160` `khong giet duoc` (khoá KHÁC) và `t161` QUA, `OPENl1_khoa` `read args` (open ngoài) — khớp bảng 12 dòng 6 | 15:38:33Z; 16:18:49Z–16:21:26Z |
| 11 | kernel thật dưới uid 65534, mọi PID trong `/proc` (`/proc` gắn `rw,relatime`) | `os.kill(pid, 0)`: EPERM 2329 / 2330 / 2331 (3.11 / 3.12 / 3.13), thành công 1 (chính nó), ESRCH 2 (PID ngoài `pid_max`), **0 EACCES**; `stat` và đọc `/proc/<pid>/stat`: thành công ở mọi PID (2341 / 2342 / 2344), 0 lỗi | 15:40:39Z; 16:12:32Z |
| 12 | B4 — `platform.system` giả Darwin, Windows, FreeBSD | `t158`–`t161` BỎ QUA ×4 ở ba nền giả × ba Python; móc audit KHÔNG được cài | 16:00:09Z |
| 13 | B6, hai vế trong MỘT lệnh cho mỗi Python (hai vế dựng trong cùng một vòng lặp: clone kho bare của rig, checkout `423b4ba`, `core.abbrev` 7, không nông; vế sau chép `cand_a` `48756818…` và tệp test thử latin-1; mỗi lượt suite bọc subreaper ở CẢ HAI vế, `--nhat-ky`) | `python3.11`: nền `188/188 ca DA CHAY QUA (tong 189, bo qua 1, hong 0)` rc=0; nháp `194/194 ca DA CHAY QUA (tong 195, bo qua 1, hong 0)` rc=0. `python3.12`: nền `187/188 … (tong 189, bo qua 1, hong 1)` rc=1; nháp `193/194 … (tong 195, bo qua 1, hong 1)` rc=1. Bỏ qua duy nhất ở mọi vế: `t62`; hỏng duy nhất ở cả hai vế 3.12: `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` (đỏ sẵn; nguyên nhân đo ở lượt 10: PEP 668 của bản 3.12 cài sẵn). **Delta 0 ở cả hai Python**, trùng số bảng 12. Nhật ký ca: 189/189 và 195/195 vào = ra, `# XONG TRON VEN` cả bốn lượt; bốn ca B8 và hai ca helper QUA trong toàn suite; mồ côi thu hồi sau lượt: 5 / 8 / 5 / 7, 0 còn sống | 16:21:39Z–16:30:39Z |
| 14 | ruff 0.15.8 `--select F`, mặc định và `--target-version py311` | nền `launcher_test.py` 5 F841 (2566, 3387, 3629, 4110, 6062); tệp test thử latin-1 và bytes: đúng 5 F841 ấy, cùng dòng; `launcher.py` nền, `cand_a`, `cand_b`: `All checks passed!` — delta 0 ở cả hai chế độ | 16:02:05Z |
| 15 | danh sách ĐÓNG (E) mục 6, trích bằng máy từ tệp r11 | `DS-E-HANG-MUC` 83/83, `DS-E-KHAC` 35/35, `DS-E-C3` 2/2, tổng 120, 0 trùng; đủ tám tên mới | 16:09:43Z (đo lại lúc đóng băng: 16:31:43Z) |
| 16 | REST (GET, `Authorization: Bearer` bằng `GITHUB_PAT`; mọi lời gọi 200 kèm `X-Github-Request-Id`) | run `36696528580`: `push`, `master`, `423b4ba`, workflow `gate` (`ci.yml`), 14 job — tên context ở ô `required_checks`; `gate-registry (ubuntu-latest)` `failure` ở bước 11, log: `ops/nhanh_don_duoc_test.py` rc=-9 sau 4500,384 s; run `36737283472` (`thu-hoi`, `pull_request_target`, PR #602): job `thu-hoi`; #686 `id` 5628902742, thân 3243 byte, sha256 `2af24e28…d9de`, 12 `"` thô, 0 thực thể HTML; comment `5888633201`, `5905670017`, `5907480436`, `5909554178`, `5913959273` (§10); tệp r1 qua `contents` (`3915f46`): sha256 `ee44238c…37d9` = bản cục bộ = `git show` sau `git fetch` | 15:31:42Z–15:58:17Z |
| 17 | nền | `git ls-remote origin refs/heads/master` ⇒ `fc852fff…c294`; kho bare của rig: `423b4ba` là tổ tiên, 29 commit, write set rc=0, `.claude .github` không đổi; `86b23c0` là tổ tiên của `fc852ff`; `9887bfc` không là tổ tiên (rc=1) | 15:31:19Z |
| 18 | zombie của container (đếm `/proc`, trạng thái `Z`) | trước mọi phép đo của r11: 2242, cả 2242 có `PPid` 1; sau ma trận, ca chậm, locale: 2242 / 2242; sau B6: 2242 / 2242 — r11 không để lại zombie nào dưới PID 1; mọi lượt lái và bọc: 0 con còn sống lúc hết, 0 con còn lại sau thu hồi | trước lúc dựng rig (lệnh đếm đầu không in giờ); 16:21:26Z; 16:30:47Z |

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
  `:490` cũng có `try`). Không cùng HÌNH lỗi (không ngoại lệ nào thoát) nhưng cùng NGHĨA "đọc lỗi ⇒ coi như đã
  chết" (r8, đo ở gạch đầu dòng dưới). **(r9) Chủ kho đã trả lời §11.1: SỬA ở packet này** — chỉ phần giải mã
  (Q-A.7); phạm vi bắt của các `try` ấy giữ nguyên.
- Nhánh hiện có ngay dưới `:651`: khi `exists()` trả `True` mà `read_text` ném `OSError`,
  `ValueError` hoặc `IndexError` (`:655`), hàm trả `False`. Đó là hành vi CŨ (cross-review lượt 1,
  hướng 7: nó bỏ PID khi `read_text` bị EACCES). Packet này **không** đổi kết quả, phạm vi bắt hay số lần
  của nhánh ấy (Q-A.3); (r9) chỉ đổi CÁCH GIẢI MÃ của phép đọc (Q-A.7). **Quan sát mới của r3** (đo 11:46:40Z
  29-09, Python 3.12.3, `launcher.py` của `89fc4fa`, không seam): một tiến trình ĐANG SỐNG mà `comm` chứa byte
  không phải UTF-8 (con tự đặt bằng `prctl(PR_SET_NAME)`) làm `read_text` ném `UnicodeDecodeError`, và nhánh cũ
  trả `_con_song(pid)` = **`False`** trong khi `os.kill(pid, 0)` thành công. Tức nhánh cũ khai "đã chết" cho tiến
  trình còn sống. r3–r8 để ngoài phạm vi; **(r9) nay SỬA** theo quyết định chủ kho (§11.1): với Q-A.7 nội dung
  ấy đọc được, nên `B2-nhanh-cu utf8-hong-that` đòi `True`. Đọc lỗi THẬT (`OSError`) ở nhánh cũ vẫn ⇒ `False` như
  nền (Q-A.3). Tần suất ngoài thực tế: KHÔNG ĐO ĐƯỢC.
  **Đo thêm ở cross-review lượt 7 (ba Python; r8 ghi "ngoài phạm vi" — r9: TRONG phạm vi, §11.1).** (i) Kích hoạt THẬT, không cần `prctl`: kernel cắt `comm` ở 15 byte, nên một chương trình tên tiếng
  Việt — ví dụ `kiểm_tra_tiến_trình.sh` — có `comm` là UTF-8 bị cắt giữa ký tự; `read_text` thật ném
  `UnicodeDecodeError`, và `_con_song` = `False` cho tiến trình ĐANG SỐNG ở nền lẫn ứng viên nháp. (ii) Cùng lớp đi
  tới 124: `_khoa_danh_tinh` (`:359`) trả `None` và `_thanh_vien_nhom` (`:436`) bỏ qua tiến trình khi phép đọc lỗi,
  nên `_giet_cay` vào nhánh "tiến trình đã biến mất" (`:896–920`) và trả `tron_ven=True`. Đầu-cuối (3.12.3): `launcher.py
  run --deadline-utc` trên một con đổi `comm` như thế SAU lúc sinh (đo bằng `prctl`; một wrapper exec chương trình
  tên tiếng Việt cho cùng `comm` hỏng, như (i)) ⇒ **rc=124**, `ly_do_dung='qua han: tien trinh da khong con chay'`,
  `giet_tron_ven=True`, trong khi con VẪN SỐNG và chưa nhận tín hiệu nào — ở nền và ở ứng viên nháp như nhau
  (phiên soạn r8 chạy lại tập lệnh ấy: cùng kết quả, bảng 10 dòng 10; r9: `t158` trên nền, bảng 11). Nếu `comm` đã
  hỏng ngay lúc sinh thì `khoa=None` và lượt chạy trả rc=10 ("tu choi giet"), con cũng còn sống. Vậy câu
  "không cùng dạng lỗi" của r7 đúng về HÌNH (không ngoại lệ nào thoát) mà không đúng về NGHĨA: `:359` và
  `:436`/`:490` cùng lớp "đọc lỗi ⇒ coi như đã chết" mà objective cấm cho `_con_song`, và nó đi tới đúng mã 124 mà
  B3b khoá. Bản vá ESRCH không gây ra nó (nền cho cùng kết quả). **(r9) Chủ kho đã trả lời §11.1: sửa ở packet
  này** (Q-A.7, B8; write set không đổi). Đo thêm ở cross-review lượt 8 (3.11.15 / 3.12.3 / 3.13.12): (iii) `stop` trên
  con đổi `comm` sau lúc sinh ⇒ rc=0 "tien trinh da khong con chay" trong khi con vẫn ghi nhịp (+9–10 byte trong 1 s; ba
  Python, nền và ứng viên theo r8 như nhau; bản nháp Q-A.7: rc=0 "SIGTERM: cay da sach", con đã chết) — `stop` trả 0
  đúng khi `_giet_cay` báo `tron_ven`, nên hai đầu vào `_giet_cay` trực tiếp của B8 phủ nó;
  (iv) locale ASCII (`PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LC_ALL=C`) với `comm` UTF-8 HỢP LỆ `tệp_ổn` (10 byte, không bị
  cắt) ⇒ `_khoa_danh_tinh` `None`, `_con_song` `False`, quét nhóm và ảnh chụp không thấy tiến trình — kích hoạt không chỉ
  là tên bị cắt; (v) `launcher_test._con_song_that`, phép kiểm sống ĐỘC LẬP của bộ test, cùng khuôn `read_text()`, cũng
  trả `False` cho tiến trình ấy; (vi) tên chương trình tiếng Việt (exec qua symlink `kiểm_tra_tiến_trình`) cho ĐÚNG 15
  byte `comm` hỏng ngay lúc sinh, không cần `prctl` (ba Python).
- `_con_song` có năm nơi gọi trong `launcher.py`: `:607` (`_con_song_dung_khoa`), `:857` và `:882`
  (`_giet_windows`, tức nhánh Windows), `:1020` và `:1039` (`_giet_cay`). Đo bằng AST (lần lên cây
  cha tới hàm bao, 10:2xZ 29-09; cross-review lượt 1 đo lại độc lập ra đúng năm nơi, 10:52Z):
  **không** lời gọi nào nằm trong thân một `try` bao ngoài, nên `ProcessLookupError` từ `:651` thoát
  thẳng khỏi các hàm ấy.
- Executor phải **grep lại** trên nền tiếp nối trước khi sửa và khai mọi chỗ mới tìm thấy.

## 3. Quyết định

- **Q-A — ngữ nghĩa bản vá.** Q-A.1–6 là **suy luận của phiên soạn** (từ docstring của `_con_song`, từ bài học
  124/125 và bài học zombie trong CLAUDE.md, và từ VERDICT lượt 1 và lượt 2); **KHÔNG phải quyết định chủ kho**. r2
  sửa Q-A của r1 theo lượt 1; r3 đến r8 KHÔNG đổi ngữ nghĩa Q-A.1–6, chỉ viết tường minh điều đã hàm ý — mỗi lần
  làm rõ ghi tại chỗ kèm revision; danh sách từng lần: đoạn này của r8 (sha256 `2ae6ee04…2aa3`). **r9 ĐỔI ngữ
  nghĩa ở đúng một trục — cách giải mã phép đọc `/proc/<pid>/stat` —** theo quyết định chủ kho (§11.1): mệnh đề r8
  ở Q-A.3 và Q-A.4 bị THAY, và thêm Q-A.7. PHẠM VI sửa là quyết định chủ kho; DẠNG sửa (hai dạng đọc cho phép) là
  suy luận của phiên soạn, đo ở bảng 11. Chủ kho có thể bác bằng revision mới. Hợp đồng, bằng lời:
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
     **(r9, ĐỔI ngữ nghĩa theo quyết định chủ kho — thay mệnh đề r8 cùng chỗ.)** "Nguyên xi" KHÔNG còn gồm cách
     giải mã: phép đọc của nhánh tệp có tuân Q-A.7; mọi phần khác của điều khoản này giữ nguyên (kết quả, phạm vi bắt
     ba nhóm, số lần). Lý do đo được (cross-review lượt 8, ba Python): mệnh đề r8 "`read_text()` không đối số" GIỮ
     `_con_song` = `False` cho tiến trình SỐNG có `comm` không giải mã được, và qua `_con_song_dung_khoa` →
     `_giet_rieng`/`_con_lai` điều đó làm `_giet_cay` bỏ qua cháu `setsid` rồi báo "SIGTERM: cay da sach" — 124 khi
     cháu còn sống (B8, đột biến M4). Mệnh đề r8 nguyên văn: Q-A.3 của r8 (sha256 `2ae6ee04…2aa3`).
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
     **(r9, ĐỔI — thay mệnh đề r8 cùng chỗ.)** Phép đọc của bước 4 tuân Q-A.7; nội dung THẬT có `comm` không phải
     UTF-8 là ĐỌC ĐƯỢC, không phải "không phân tích được": trạng thái `Z` ⇒ `False`, khác `Z` ⇒ `True`, không gọi kill.
     Mệnh đề r8 ("`read_text()` không đối số; lỗi giải mã ⇒ rơi về kill") trái vế zombie của objective: lượt 8 đo zombie
     `comm` hỏng + seam EACCES ở `stat` ⇒ ứng viên theo r8 `_con_song` = `True` (vì `kill(zombie, 0)` thành công), bản
     giải mã bền `False` (ba Python).
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
  7. **(r9) Giải mã bền ở CẢ BỐN chỗ đọc `/proc/<pid>/stat`** — `_khoa_danh_tinh` (`:359`), `_thanh_vien_nhom`
     (`:436`), `_chup_cay` (`:490`) và hai khối đọc của `_con_song` (nhánh tệp có; đường lỗi mới). Phép đọc là MỘT
     trong hai dạng, executor chọn, khai trong handoff và trong MỘT hằng `DANG_DOC_QA7` của `launcher_test.py` (tên
     phương thức `Path`, args, kwargs — helper và B8 dùng chung): `read_bytes()` rồi tách trên bytes (các trường số giải
     mã ASCII), hoặc `read_text(encoding="latin-1")` (song ánh byte ↔ ký tự). Cả hai không phụ thuộc locale và không bao
     giờ ném `UnicodeDecodeError`. Vi phạm: `read_text()` không đối số (phụ thuộc locale — đo: locale ASCII làm cả `comm`
     UTF-8 hợp lệ nổ), mọi `encoding=` khác (đo: `cp1252` ném ở byte 0x81), và mọi `errors=`. Nói cho đúng: `errors=
     "replace"` hay `"surrogateescape"` KHÔNG sai hành vi ở locale tương thích ASCII (đo lượt 8: không ném, tách đúng,
     trên `comm` hỏng lẫn `comm` UTF-8 hợp lệ, ở locale UTF-8 và `LC_ALL=C`, ba Python); chúng bị loại để dạng đọc là
     danh sách cho phép ĐÓNG, kiểm được bằng `read args`, và không phụ thuộc locale theo cấu trúc — muốn nhận thì mở
     rộng danh sách và khai. **Định dạng khoá có CHỐT (r10, cross-review lượt 9, lớp `khoa-dinh-dang-khong-co-chot`).**
     Khoá danh tính Linux là `linux:` ghép chuỗi thập phân ASCII của trường 22 (`starttime`) — đúng như nền; dạng bytes
     phải giải mã ASCII trường ấy TRƯỚC khi ghép. Trên nền `423b4ba` khoá Linux được dựng ở ĐÚNG hai chỗ (`git grep`
     chuỗi `linux:` trong `launcher.py`): `:362` (`_khoa_danh_tinh`) và `:494` (`_chup_cay`); nhánh Darwin, Windows
     (`darwin:`, `win:`) ngoài phạm vi (Q-A.6). Ứng viên thêm chỗ dựng khoá thì khai trong handoff, và chỗ ấy cũng theo
     định dạng này. Ca bắt, theo tổ hợp: lệch ở MỘT chỗ ⇒ khoá lệch nội bộ ⇒ `t160`/`t161` đỏ; lệch ở CẢ HAI chỗ (nhất
     quán nội bộ, ví dụ `linux:b'…'`) ⇒ `t160`, `t161` lấy khoá của mẹ bằng phép đọc BYTES độc lập theo định dạng nền
     (`_k124_khoa_that`, đúng tình huống sổ `run.json` do một bản launcher khác ghi) ⇒ `_giet_cay` từ chối (khoá KHÁC) ⇒
     `t160` đỏ `khong giet duoc`; biến thể (E) `g_to_hop_dinh_dang_khoa`. Đo ba tổ hợp trên khối r10: bảng 12. Lý do
     đo được (VERDICT lượt 9, sha256 `0f1b3bdc…ddfa`): bản bytes lệch cả hai chỗ QUA bốn ca B8 của r9 và toàn suite,
     còn `stop` xuyên phiên bản trả rc=10 "khoa danh tinh KHAC" và để con SỐNG. Phạm vi bắt, số lần hỏi/đọc/kill và mọi
     hành vi khác của bốn hàm không đổi. Khoá bằng B8 (bốn ca; `t160`, `t161` còn đòi `read args` trên MỌI lời đọc
     `/proc/<pid>/stat` trong cửa sổ quanh `_giet_cay`, tức cả bốn hàm), bằng hai đầu vào nội dung thật,
     và bằng loại `read args` của helper (quy ước chung, "Seam thay CẢ lời gọi").
     **Phép tách, API đọc và phần còn lại của ba hàm ngoài có CHỐT (r11, cross-review lượt 10, lớp
     `ma-tran-loi-thieu-chot`).** r11 TỰ LIỆT KÊ đường vào của hai trục còn thiếu ở CẢ năm chỗ đọc trước khi vá — bảng
     "Năm chỗ đọc × hai trục" ở B2 là danh sách có thẩm quyền, mỗi ô một đầu vào, một chốt, một tên (E), một số đo.
     (i) Phép tách: tách trường theo dấu `)` CUỐI như nền (dạng bytes: `rindex(b")")`). Hai đường sai: tách theo `)`
     ĐẦU (`index`, `find`, `partition(b") ")`, `split(b")", 1)`, biểu thức chính quy không tham lam) và tách cả dòng
     theo khoảng trắng (`split()[k]`) — cả hai lệch trường khi `comm` chứa `) ` hay khoảng trắng (tên thật kiểu
     `tep (1).sh`). (ii) API: danh sách cho phép đóng ở MỌI API — trong bốn hàm, nội dung `/proc/<pid>/stat` chỉ được
     đọc bằng đúng lời gọi `Path` của `DANG_DOC_QA7` trên đúng đường `/proc/<pid>/stat`; `open()`, `io.open`,
     `Path.open()`, `os.open`, đường `/proc/<pid>/task/…`, `dir_fd`, tiến trình con, fd mở từ trước đều là vi phạm như
     một `encoding=` lạ. (iii) Phần còn lại của ba hàm ngoài — phạm vi bắt, vòng lặp, số lần đọc, mọi dòng không thuộc
     phép đọc — giữ nguyên TỪNG BYTE so nền; khoá bằng "Chốt tĩnh phần còn lại" ở B2, vì hai trục động không phủ hết:
     sự kiện `open` không thấy fd mở trước cửa sổ, thước đo `open` bỏ đường tuyệt đối không bắt đầu bằng `/proc/`
     (`SL2_khoa`, bảng 13), và không đầu vào nào đo phạm vi bắt hay số lần đọc của ba hàm này.
     Chốt động: cháu của `t160`, `t161` mang `comm` `_K124_COMM_CHAU` (có `) ` và khoảng trắng); `read args` của B8 đòi
     không sự kiện audit `open` nào trên `/proc/…`, đường tương đối hay fd số xảy ra NGOÀI một lời đọc `Path` đã ghi; ở
     hai khối đọc của `_con_song` thêm seam của helper ("Seam thay CẢ lời gọi": đọc bằng đường khác thì seam không thấy,
     đếm đọc ra 0). Lý do đo được (VERDICT lượt 10, sha256 `88538f7c…85f8`, ba Python): với khối r10, chín biến thể
     tách theo `)` đầu và mười biến thể đọc qua `open()`/`Path.open()` QUA cả bốn ca B8, còn với `comm` có `) ` hay
     byte 0x81 chúng cho `124 noi doi` hay `khong giet duoc`. r11 đo thêm (bảng 13): đường khoảng trắng ở cả năm chỗ,
     API ở hai khối đọc của `_con_song`, đường `task` mà bộ lọc của HINT không thấy, tiến trình con. Biến thể (E):
     mục 6.

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
  ném đúng `UnicodeDecodeError` (bảng 4). (r9) Với Q-A.7, dạng thứ tư không còn xảy ra ở nội dung THẬT — nó chỉ
  còn là đầu vào seam (`p4`).
- **Mission #686 Q1:** ca khoá trong `.claude/dev/launcher_test.py`; xếp sau #668.
- **Mission #686 Q3:** executor Sonnet 5.5, effort high.
- **Mission #686 Q4:** không chạy CI Windows trên PR (không gắn nhãn `windows`, không gọi tay).
  `launcher-windows.yml` tự chạy ở `push` master với `paths: .claude/dev/**`, nên **lần merge là
  lần đo Windows đầu tiên** của bản vá; đọc kết quả ấy là một `land_obligation`.
- **Hệ quả của Q4 cộng chỉ thị thường trực "không chạy CI trên PR làm bằng chứng"** (nói thẳng,
  không che): trên PR thi hành, **không có lượt CI nào chạy `launcher_test.py`** — job `launcher` bị
  tắt trên PR không nhãn `windows` (Q4), và `gate-registry` không chạy tệp này (§8). Bằng chứng thay
  thế duy nhất trước merge là log cục bộ Linux ở B6, chạy trên `python3.11` (bản Ubuntu của `launcher-windows.yml`
  hậu-merge) và `python3.12` (bản của `ci.yml`); 3.13 trên Windows chỉ đo sau merge.

## 4. `write_set`

- `.claude/dev/launcher.py`
- `.claude/dev/launcher_test.py`

Không đường dẫn nào khác. Đặc tả này (`ops/specs/launcher-con-song-esrch-r11.md`) là hồ sơ của lượt
soạn, không thuộc write set thi hành.

## 5. `ngoai_pham_vi`

- (r9) `:359`, `:430`/`:436`, `:484`/`:490` NAY Ở TRONG phạm vi, chỉ phần giải mã (Q-A.7; chủ kho trả lời §11.1);
  phạm vi bắt của các `try` ấy và mọi hành vi khác giữ nguyên. Vẫn ngoài phạm vi — cùng khuôn `read_text()` trên
  `/proc/<pid>/stat`, `git grep` trên `reviewed_sha` ra đúng ba chỗ ngoài `launcher.py`/`launcher_test.py`; cross-review
  lượt 8 đo trên một cháu CÒN SỐNG có `comm` 15 byte hỏng (ba Python; `comm` thường: cả ba đúng):
  · `.claude/dev/gate_lifecycle.py` `_khoa_pid_proc` (`:899–910`) ⇒ `None` (`tick:…` cho `comm` thường); `_khoa_pid`
    khi ấy lùi về `ps lstart` (khoá `giay:…`, khác định dạng);
  · `.claude/dev/gate_lifecycle.py` `_cac_hau_due` (`:913`, đọc ở `:933`) ⇒ cháu ấy VẮNG khỏi tập hậu duệ — cây giết
    của gate lifecycle bỏ sót nó, cùng hình với B8-setsid của launcher;
  · `.claude/dev/ci_dang_ky_test.py` `_pid_song` (`:904–916`, đọc ở `:913`; AST trên `89fc4fa` và `423b4ba`, r10 — r9
    ghi `:903–913`) ⇒ `[]` cho cháu ấy, theo PID lẫn theo nhóm — phép dò
    rò tiến trình của CI coi nó đã chết.
  **Nợ, KHÔNG sửa ở đây: `DOC-PROC-STAT-GIAI-MA-NGOAI-LAUNCHER`** — ba chỗ trên, hai tệp ngoài write set (một thuộc
  gate lifecycle, một là bộ test CI; người giữ lease của `ci_dang_ky_test.py`: mục "`.github/workflows/**`
  và `.claude/dev/ci_dang_ky_test.py`" của §5; của `gate_lifecycle.py`: chưa đo). Đề nghị packet riêng, cùng Q-A.7
  và một ca khoá kiểu B8 cho từng tệp. Packet này không phụ thuộc chúng (B8 đo `launcher.py` đầu-cuối). Phiên soạn
  r9 đếm lại bằng `git grep` trên `5f7485c` (bảng 11), phiên soạn r10 trên `423b4ba` (bảng 12): ngoài `launcher.py`
  đúng ba chỗ ấy (`gate_lifecycle.py:906`, `:933`, `ci_dang_ky_test.py:913`), cùng số dòng ở cả hai nền; thêm `launcher_test.py:2142` đọc `/proc/1/comm` với `encoding="utf-8"` — phép
  chẩn đoán môi trường bọc trong `_do_an_toan`, không phải phép kiểm sống, ngoài lớp này.
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
2. `.claude/dev/launcher_test.py` — **Sáu ca mới** (r9; r8: hai), tên nối tiếp hậu tố lớn nhất: `t156_...` (B1, B2,
   B3, B4) và `t157_...` (B3b) dựng trên MỘT helper theo nhãn (quy ước chung ở §7), cộng bốn ca B8 `t158_...` đến
   `t161_...` KHÔNG dùng helper (§7 B8). Hậu tố `t155` là lớn nhất của các ca mang tiền tố `t` trên `89fc4fa` (đếm
   ở §8); executor **đo lại hậu tố trên nền tiếp nối** trước khi đặt tên vì #668 cũng giữ tệp này. Các mục
   `DOT_BIEN` mới: **đúng theo danh sách ở B5, và chỉ ở đó** — §6 không lặp lại con số. Số ca mới và số mục đột
   biến là hai đơn vị khác nhau. Helper và các đơn vị nhãn nằm trong `t156_...`, `t157_...`; không thêm tệp, không
   thêm ca đăng ký nào ngoài sáu ca này, không sửa runner `--dot-bien`.
3. (r9) `.claude/dev/launcher.py` — Q-A.7 ở bốn chỗ đọc (§3), kèm chú thích theo idiom của tệp (nguồn: quyết định
   chủ kho, PR #688 comment `5905670017`; cross-review lượt 7 và lượt 8 trên PR #688). `.claude/dev/launcher_test.py` — bốn ca B8, hằng
   `DANG_DOC_QA7`, loại `read args` của helper, và `_con_song_that` đọc BYTES: đó là phép kiểm sống ĐỘC LẬP mà `t62`,
   `t63`, `t66`, `t67` dùng, và với `read_text()` nó báo "đã chết" cho chính tiến trình B8 cần thấy (đo lượt 8). Write
   set hai tệp là ĐỦ: bốn chỗ đọc và mọi nơi gọi của chúng ở `launcher.py`; mọi ca, helper và đột biến ở
   `launcher_test.py`. (r11) Ở ba hàm ngoài `_con_song` chỉ các dòng mà "Chốt tĩnh phần còn lại" (B2) cho phép được
   đổi — phép tách theo `)` cuối, lời đọc đúng lời gọi đã khai; nguồn chú thích thêm: cross-review lượt 10 trên PR #688.

## 7. `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3). Đột biến chạy trên **bản sao tạm**, bằng chính
`python3.11 .claude/dev/launcher_test.py --dot-bien` và `python3.12 …` (B6: không gọi `python` trần). Quy ước chung cho hai ca `t156_...`, `t157_...` (bốn ca B8 có
quy ước riêng ở mục B8; hằng `DANG_DOC_QA7` dùng chung):

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
  mà vẫn đếm được; (r9) khi lời gọi thật ném, seam chỉ-đếm KHÔNG ghi gì và để ngoại lệ đi nguyên — ngoại lệ ấy là VÔ
  CAN (loại ghi nhận (2) chỉ còn observer `kill`, xem dưới). Observer `os.kill(pid, 0)` (chỉ cặp PID đang xét và tín
  hiệu 0; ghi lại rồi chuyển tiếp thật, hoặc ném lỗi seam; tín hiệu khác hay PID khác chuyển tiếp nguyên vẹn) đặt ở
  (r7): mọi đầu vào mà đường Q-A đi qua bước kill — tầng K (`B2-doc-hong`, `B2-parse`, `B2-dem-doc` tiểu nhãn `3`,
  `B2-pid-du-phong`, và tiểu nhãn `kill`/`kill-*` của `B2-tin-hieu`, `B2-exception`, `B2-thoat-parse`) và tầng K0
  (mọi tiểu nhãn `vang*` của `B2-nhanh-cu`) — cùng các đầu vào tầng Đ0 (phần tệp có của `B2-nhanh-cu` và lời gọi
  đường cũ của `B3-zombie`) và (r9) `B2-dem-doc 4` (đường Đ đọc được), để đếm được con số 0. Ba đầu vào tầng hỏi của `B2-thoat-parse` đặt seam ở `Path.exists` (bảng 7), và
  bộ đếm của chính seam ấy phải ≥ 1 — bằng 0 (ứng viên không hỏi bằng `exists()`) thì ca ném lỗi thường,
  không phải `bang`, và executor đổi seam sang hàm `Path` mà ứng viên thực sự gọi rồi khai vào handoff.
- **Seam thay CẢ lời gọi — đối số của lời gọi, và cách khoá (r8 lập; r9 sửa theo Q-A.7 và cross-review lượt 8).**
  Seam ném lỗi hay trả chuỗi dựng sẵn thì thay nguyên lời gọi, nhưng VẪN NHẬN đủ đối số của lời gọi — câu r8 "không
  thấy đối số" sai: lượt 8 đo seam trả payload ghi được `((), {})` cho ứng viên và `((), {'encoding': 'utf-8'})` cho
  biến thể `encoding="utf-8"` tường minh, ở Đ0 và ở Đ. (r9) Mọi chỗ trong đặc tả viết `Path.read_text`/`read_text`
  cho seam, bộ đếm hay payload của phép đọc `/proc/<pid>/stat` trong launcher: đọc là phương thức theo `DANG_DOC_QA7`
  (`read_text` hay `read_bytes`), payload `str` hay `bytes` tương ứng. (r11) Chính điều này là chốt trục API ở hai khối
  đọc của `_con_song`: lời đọc KHÔNG đi qua phương thức đã khai thì seam không thấy và đếm đọc ra 0 — đo (bảng 13, ba
  Python): `g_d0_open` ⇒ `B2-nhanh-cu song read count 0`, `g_d_open` ⇒ `B2-eacces read count 0`; và ngược lại, helper
  chỉ seam `read_text` (helper của phiên soạn) đặt trước ứng viên bytes ĐÚNG cũng ra `B2-eacces read count 0` — helper
  phải seam (ít nhất) đúng phương thức của `DANG_DOC_QA7`. Rà mọi seam của hai ca:
  · Phép đọc (ném hay trả payload, ở Đ, Đ0, K, ma trận `B2-pid-du-phong` và các đầu vào chỉ-đếm): seam GHI (args,
    kwargs) của từng lời gọi trên đúng đường, và ca đòi MỌI bản ghi BẰNG `DANG_DOC_QA7` (loại assertion `read args`,
    xét ngay sau đếm đọc, ở mọi đầu vào có đếm đọc). Vì thế một dạng đọc lệch chết ở đầu vào ĐẦU TIÊN có đọc trên
    đường ấy (Đ0: `B2-dem-lan`; Đ: `B2-eacces`), trước khi tới hai đầu vào nội dung THẬT — `B2-nhanh-cu
    utf8-hong-that` ⇒ `True` (Đ0), `B2-dem-doc 4` ⇒ `True`, đọc được, kill 0 (Đ) — và đuôi UTF-8 hỏng trong `comm`
    của `B3-zombie` (zombie trên đường mới ⇒ `False`). Răng RIÊNG của ba đầu vào ấy là cho vi phạm ĐÚNG đối số mà SAI
    hành vi: giải mã lại UTF-8 sau khi đọc (biến thể (E) `d0_giai_ma_lai_utf8`, `d_giai_ma_lai_utf8`; bảng 11).
    `newline` (3.13) chỉ đổi cách dịch CR, mà phần sau `)` cuối do kernel ghi và không có CR: suy luận, không đo.
  · `Path.stat` và `Path.exists` (ném) che `follow_symlinks`: `/proc/<pid>/stat` là tệp thường, không phải
    symlink (`lstat`, bảng 10 dòng 7), nên tham số ấy không đổi kết quả.
  · ĐƯỜNG DẪN và API: mọi seam khoá theo đúng chuỗi `/proc/<pid>/stat` của PID đang xét, cộng bộ đếm. Ứng viên
    đọc hay hỏi bằng đường khác hoặc API khác (`open`, phương thức đọc không phải dạng khai, `os.path.exists`) không
    chạm seam ⇒ bộ đếm 0
    ⇒ ca đỏ: `read count 0` ở đầu vào đòi đọc 1, hoặc lỗi thường "seam không chạm" ở đầu vào có seam ném (đo ba
    biến thể, bảng 10 dòng 4). Observer `kill` khoá theo cặp (PID, 0); gọi bằng tín hiệu khác hay API khác ⇒
    `kill count 0`.
  Hai đầu vào nội dung THẬT có **điều kiện dựng**: con đặt `comm` bằng đúng 15 byte
  `6b 69 e1 bb 83 6d 5f 74 72 61 5f 74 69 e1 ba` (tức `'kiểm_tra_tiến_trình'.encode()[:15]`, viết dạng byte để lời
  gọi sinh con không phụ thuộc locale — dạng chuỗi làm chính lời gọi sinh con ném `UnicodeEncodeError` ở locale
  ASCII, đo), ca xác nhận bằng phép đọc bytes độc lập rằng `comm` đã đổi, rồi xác nhận NGOÀI cửa sổ đếm rằng
  `read_text()` thật trên đường ấy ném `UnicodeDecodeError`. Một trong hai không đạt ⇒ lỗi thường, KHÔNG `bang`
  (locale giải mã được 15 byte ấy, ví dụ Latin-1, làm điều kiện không dựng được thay vì làm ca đỏ giả).
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
  observer) — TRỪ `B2-dem-doc 4` (r9): Q-A.4 (r9) nói nội dung thật có `comm` không phải UTF-8 là ĐỌC ĐƯỢC, "không gọi
  kill", và ở đó số lời gọi `kill` là dấu hiệu duy nhất phân biệt "đọc được" với "rơi về kill" (cả hai trả `True`
  cho tiến trình sống), nên ca đặt observer và đòi kill 0. Một ngoại lệ có chủ ý khác: `B2-dem-lan` đi đường Đ0 (lần hỏi đầu là `stat` thật) nhưng là nhãn của trục
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
- **Thứ tự assertion TRONG một đầu vào (r8, cross-review lượt 7).** Mỗi đầu vào xét theo thứ tự: (1) ngoại lệ thoát
  (phân hạng theo bốn loại, hay danh tính sentinel); (2) kết quả; (3) đếm hỏi; (4) đếm đọc rồi (r9) `read args`; (5)
  đếm kill. Riêng `B2-pid-du-phong`: (1) ngoại lệ thoát; (2) đếm kill; (3) kết quả; (4) đếm hỏi; (5) đếm đọc rồi
  `read args`. Bước mà đầu vào không
  đòi (không đặt observer, không đếm) thì bỏ, giữ thứ tự các bước còn lại. Loại assertion mà B5 và (E) nêu cho từng
  dòng GIẢ ĐỊNH thứ tự này. Đo, 3.12.3: helper chỉ đổi sang "đếm trước, kết quả sau" làm 9/55 cặp đỏ vì lệch loại ở
  rig lượt 7 ((i), (l3), (l5), (l13), (l14), (l18), (l20), (m1), (m3)) và 8/55 ở rig r8 (cùng danh sách trừ (i), vì
  dòng (i) không nêu loại ở B5; bảng 10 dòng 9), dù ứng viên, helper và 54 dòng đều đúng.
- Ca chỉ chuyển thành `bang(False, ...)` ngoại lệ **có gốc đo được từ chính ca** (r6 nêu đủ bốn loại; r5 chỉ
  nêu loại đầu): (1) đối tượng do seam tạo ra, so bằng danh tính (`is`); (2) ngoại lệ THẬT mà observer của
  `os.kill(pid, 0)` vừa chuyển tiếp — observer ghi lại đối tượng rồi ném lại đúng nó, nên danh tính biết trước khi nó
  thoát (cần cho `B2-pid-du-phong` tiểu nhãn `da-wait`, nơi ESRCH là của kernel chứ không của seam). **(r9) Loại (2)
  CHỈ còn observer `kill`, như r7 — phần r8 mở rộng sang seam chỉ-đếm của `Path.stat` và phép đọc bị BỎ.** Mọi ngoại lệ
  thật đi qua seam chỉ-đếm — `UnicodeDecodeError` của một đột biến đọc lệch dạng, lỗi đối số (`TypeError`,
  `LookupError`), lỗi của một lời gọi thêm — là VÔ CAN. Lý do: (i) phần mở rộng cấp tín dụng giả — lượt 8 đo (ba
  Python) dòng (j1) viết bằng lần đọc thứ hai `read_text(encoding="khong-co-ma-nay")` chết vì `LookupError` được ghi
  `seam escaped`, W0 sống, nên A1/W1/W0 CHẤP NHẬN như giết thật (19/54 dòng B5 không nêu loại); (ii) phần ấy sinh ra
  chỉ để W0 của `d0_value_thoat`, `d0_decode_thoat` khỏi chết vì `UnicodeDecodeError` THẬT của `utf8-hong-that`, mà
  với Q-A.7 đầu vào ấy không còn ném gì trên ứng viên đúng. Đo (lượt 8 và bảng 11, ba Python): loại (2) như r7 +
  Q-A.7 ⇒ 54 dòng 55/55 cặp, hai biến thể ấy CHẤP NHẬN, (j1) VÔ CAN ở A1, W1 và W0; (3) ngoại lệ mới có chuỗi `__cause__` (tức `raise … from …`) chứa một đối tượng loại (1) hoặc (2) —
  bản vá bọc lại ngoại lệ thay vì để nó thoát nguyên đối tượng (Q-A.5); thông điệp ghi `seam wrapped`;
  (4) chỉ ở `B2-parse`, ở các đầu vào parse `p1`–`p3` của `B2-pid-du-phong` (đúng các đầu vào của `B2-parse`), và ở
  hai đầu vào `p1`, `p3` của `B2-nhanh-cu` (r7, cột Đ0): lỗi của phép tách trạng thái mà PAYLOAD THEO DÕI do seam cấp
  tự ném (r9 — `B2-parse` mô tả; nhận bằng DANH TÍNH đối tượng lỗi do seam tạo sẵn, không còn kiểu, đối số, hàm, dòng
  hay số lần). Chuỗi `__context__` (ngữ cảnh ngầm) KHÔNG được tính: một ngoại lệ vô can ném ra
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
  lệ, seam đã chạm, bộ đếm). Hai ca `t156_...`, `t157_...` gọi CÙNG một helper dựng từ các đơn vị đó; helper nhận hai
  tham số tuỳ chọn mà ca đăng ký KHÔNG truyền — tập nhãn CHẠY (mặc định: tất cả, theo thứ tự dưới đây)
  và tập nhãn NỚI (mặc định: rỗng); tên tham số do executor đặt. **"Nới nhãn L"** nghĩa là: đầu vào của
  L vẫn chạy nguyên (seam vẫn đặt, lời gọi vẫn thực hiện), nhưng MỌI assertion mang nhãn L bị bỏ, và
  nếu một ngoại lệ thuộc bốn loại ghi nhận của quy ước chung ở trên (đối tượng do seam của L tạo ra, so bằng danh
  tính; ngoại lệ thật mà observer `kill` đã ghi; ngoại lệ bọc lại; lỗi do payload theo dõi của `B2-parse` ném, r9)
  thoát khỏi lời gọi thì nó bị nuốt; mọi ngoại lệ khác vẫn thoát. Nới KHÔNG được là cách để bỏ đầu vào, bỏ thiết
  lập hay trả sớm. Helper chỉ phục vụ hai ca `t156_...`, `t157_...` (§6.2): phép đo dùng tham số là lời gọi TRỰC
  TIẾP helper từ tập lệnh bằng chứng của executor, trên bản sao đột biến (cùng cách B5 đã đòi gọi thẳng hàm ca) —
  không phải một ca đăng ký thêm và không sửa runner `--dot-bien`. **Mặc định của hai tham số là một phần của
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
    · (p1)–(p3) lỗi của phép tách, nhận bằng DANH TÍNH (r9, cross-review lượt 8 — thay luật "kiểu, đối số, nguồn"
      của r6–r8): seam cấp payload là một PAYLOAD THEO DÕI — kiểu con của `str` (hay của `bytes` nếu Q-A.7 chọn bytes)
      mà các phép tách của nền (`rindex`, `index`, cắt lát, `split`, lấy phần tử `[i]` của danh sách `split` trả về)
      đều trả đối tượng theo dõi cùng loại, và khi hỏng thì ném MỘT đối tượng lỗi do seam TẠO SẴN cho đầu vào ấy
      (`ValueError('substring not found')` ở `p1`, `p2`; `IndexError('list index out of range')` ở `p3` — đối số chỉ
      để đọc log). `_con_song` để thoát chính đối tượng ấy SAU khi seam đọc đã chạm ⇒ `bang(False, …)`, thông điệp
      `parse error escaped`; bọc lại bằng `raise … from …` với nguyên nhân là nó ⇒ `parse error wrapped`. Không còn lời
      khai hàm / nguyên dòng / số lần, không `linecache`. Vì sao đổi: luật vị trí của r7–r8 (chuỗi con → nguyên dòng →
      thêm số lần) nhận ra NƠI ném chứ không nhận ra DỮ LIỆU bị tách, nên mỗi lượt lại có một phép giả mới. Đo lượt 8
      (ba Python), dưới luật r8: (fp6b) thử lại CHÍNH dòng tách đã khai trên chuỗi rỗng trong một vòng lặp (không
      thêm bản sao, số lần không đổi), coi `UnicodeDecodeError` là không đọc được; và (c3) ứng viên tách trong hàm trợ
      giúp (r8 cho phép) gọi lại hàm ấy trên `"0 (x)"` trong nhánh `IndexError` ⇒ A1 và W1 `TH … parse error escaped`,
      W0 SỐNG — tín dụng giả qua đủ bốn phép (bản thô fp6, và bản c3 gọi lại trên chuỗi rỗng: A1, W1 TH, W0 vô can —
      lọt hai phép); r8 §10 khai ca hàm trợ giúp "KHÔNG ĐO ĐƯỢC (chưa dựng)". Dưới payload theo dõi: 54 dòng 55/55
      cặp; `ctrl`, fp…fp6, fp6b và hai phép giả c3 chết VÔ CAN ở A1, W1, W0; ứng viên tách hai dòng (C2) và tách trong hàm trợ giúp (C3) có (l15), (l17)
      CHẤP NHẬN — không cần khai gì. Phiên soạn r9 đo lại trên ứng viên nháp Q-A.7 (bảng 11 dòng 3–4, ba Python): cùng kết quả. Giới hạn (thay giới hạn cũ): ứng viên phải tách trên CHÍNH payload bằng các phép ấy;
      tách bằng phép khác (biểu thức chính quy, `partition`, chuẩn hoá chuỗi trước khi tách) làm (l15)/(l17) chết VÔ CAN
      — đỏ ồn ào, không tín dụng giả; executor mở rộng payload theo dõi cho phép mình dùng và khai. Đột biến ĐỔI chính
      phép tách (như (m5)) vẫn hợp lệ vì các dòng ấy nhắm kết quả. Ngoại lệ không phải đối tượng do seam tạo — kể cả
      cùng kiểu, cùng đối số — là vô can.
    Đối chứng (bắt buộc; mỗi cái phải chết VÔ CAN ở A1, W1 và W0 — dưới payload theo dõi chúng vô can theo cấu trúc,
    giữ làm hồi quy): khác đối số (`ctrl`, bảng 8); cùng đối số khác nguồn (fp, lượt 6); fp2, fp3 (lượt 7); fp4, fp5
    (r8); và (r9) fp6, fp6b cùng hai phép giả gọi lại hàm trợ giúp nếu ứng viên tách trong hàm trợ giúp. Luật r6–r8 và số đo của
    chúng: nguyên văn ở `B2-parse` của r8 (sha256 `2ae6ee04…2aa3`).
    **ĐỎ khi** (tám dòng, mỗi hướng của bảng không gian một dòng): đường nội dung hỏng trả `False` ⇒ chết bằng
    assertion kết quả `True` ở `p1` (dòng (i)); tầng đọc không bắt `ValueError` ⇒ chết ở `p1` (dòng (l15));
    kiểm tra dữ liệu chỉ nhận ra chuỗi rỗng mà không bắt `ValueError` ⇒ `p1` qua, chết ở `p2` (dòng (l16));
    tầng đọc không bắt `IndexError` ⇒ chết ở `p3` (dòng (l17)); `IndexError` ⇒ `False` ⇒ chết ở `p3` (dòng (l18));
    phép đọc chỉ bắt `OSError` còn phần tách bọc riêng nên `UnicodeDecodeError` thoát ⇒ chết ở `p4` (dòng (l19));
    `UnicodeDecodeError` ⇒ `False` ⇒ chết ở `p4` (dòng (l20)); tầng đọc bọc lại `ValueError` tự nhiên thành
    `RuntimeError` bằng `raise … from …` ⇒ chết ở `p1` (dòng (l21), thông điệp `parse error wrapped`).
  - `B2-dem-doc` (r3) — số lần ĐỌC nội dung. Gọi `_con_song` TRỰC TIẾP (không qua `_con_song_dung_khoa`), trên
    `os.getpid()` ở đầu vào 1–3 và trên PID con ở đầu vào 4, bốn đầu vào (tiểu nhãn `1`, `2`, `3`, `4`, chạy theo thứ tự ấy; `4` thêm ở r8): (1) `stat` EACCES +
    `read_text` thật thành công; (2) `stat` EIO + `read_text` thật thành công; (3) `stat` EACCES +
    `read_text` ném EACCES (đọc lỗi); (4) (r8; r9 đổi kỳ vọng) con THẬT có `comm` UTF-8 hỏng, `stat` EACCES + phép đọc
    THẬT theo Q-A.7 ⇒ ĐỌC ĐƯỢC, trạng thái khác `Z` ⇒ `True`, không rơi về kill (chi tiết ngay dưới đoạn ĐỎ khi). Trong mỗi
    đầu vào, số lần phép đọc chạm đúng đường `/proc/<pid>/stat` của PID ấy **bên trong cửa sổ
    lời gọi `_con_song`** phải bằng **đúng 1** (gồm cả nhánh đọc thành công lẫn nhánh đọc lỗi). Cửa sổ
    đếm chỉ bao lời gọi: mọi lần đọc kiểm soát do chính ca thực hiện (ví dụ đọc để xác nhận trạng
    thái) nằm NGOÀI cửa sổ — lượt 2 đã đo trường hợp nhầm: cộng lần đọc kiểm soát vào thì bản đúng
    báo 2 (VERDICT lượt 2, hướng 7). Phép đọc khoá của wrapper (`_khoa_danh_tinh`, `:359`) không thuộc
    bộ đếm này vì ca gọi trực tiếp. Bộ đếm là lớp quan sát: nó chuyển tiếp sang phép đọc thật và
    KHÔNG thay nội dung, trừ ở các đầu vào "đọc hỏng" đã khai (đầu vào (3) này, và bốn đầu vào của
    `B2-parse`). Giữ nguyên các kiểm đếm `stat` hiện có (`B2-dem-lan`). (r7, quy ước đếm) Mỗi đầu vào còn đòi hỏi
    đúng 1; đầu vào `3` (đường K) đặt observer `os.kill(pid, 0)` chuyển tiếp thật và đòi đúng 1 lời gọi; (r9) đầu vào `4` là đường Đ ĐỌC ĐƯỢC: observer vẫn đặt và đòi đúng 0 lời gọi. **ĐỎ khi** (đột biến (j)): bộ
    đếm ≠ 1, tức đọc lại lần hai, ở nhánh nào cũng vậy — lần đọc thứ hai đặt sau lần đọc thành công làm
    đầu vào `1` đỏ đầu tiên; lần đọc thứ hai đặt trong xử lý đọc lỗi chỉ chạm ở đầu vào `3`.
    **Đầu vào `4` (r8 lập; r9 đổi kỳ vọng theo Q-A.7).** Con sinh bằng `start_new_session`, tự gọi `prctl(PR_SET_NAME, …)`
    với đúng 15 byte của `'kiểm_tra_tiến_trình'.encode()[:15]` — thứ kernel làm với một chương trình tên tiếng Việt
    (lượt 8 đo: exec qua symlink tên ấy cho đúng 15 byte này, không cần `prctl`). Điều kiện dựng (xác nhận `comm` bằng
    bytes, rồi `read_text()` KHÔNG đối số thật ném `UnicodeDecodeError` ngoài cửa sổ đếm — chứng tỏ đầu vào có răng với
    cách đọc của nền) và cách viết 15 byte: quy ước chung, mục "Seam thay CẢ lời gọi"; dọn con bằng PID tường minh. Kỳ
    vọng r9: `True`, hỏi 1, đọc 1, `read args` đúng `DANG_DOC_QA7`, kill 0 (observer đặt). Kỳ vọng r8 (`kill count 1`)
    khoá đúng lỗi chủ kho quyết sửa (bản nháp Q-A.7 đỏ ở đó, lượt 8). Đo: trên helper KHÔNG có `read args` (lượt 8, ba
    Python) ứng viên theo r8 đỏ ở đây `kill count 1`; trên helper r9 (bảng 11) nó chết sớm hơn ở `B2-eacces read args`,
    và răng riêng của đầu vào này là biến thể (E) `d_giai_ma_lai_utf8` (đúng đối số, sai hành vi) ⇒ `B2-dem-doc 4 kill
    count 1`. Vị trí `B2-parse` cũng dùng được (lượt 8 đo: loại (2) mở rộng r8 ⇒ W0 của (i), (l15), (l16), (l19), (l21)
    sống 5/5; loại (2) hẹp ⇒ 1/5 — r8 khai "KHÔNG ĐO ĐƯỢC (chưa thử)"); với Q-A.7 đầu vào không còn ném, r9 giữ
    `B2-dem-doc`.
  - `B2-pid-du-phong` (r5, thêm sau cross-review lượt 4) — khoá KẾT QUẢ và VIỆC THỰC HIỆN của bước PID dự
    phòng ở Q-A.4, thay vì suy từ `True` trên PID sống. Q-A.4 nói khi không đọc được thì chỉ `os.kill(pid, 0)`
    quyết định sống hay chết; mọi nhãn ở trên đặt đầu vào đọc lỗi hoặc hỏng lên PID SỐNG, nên một bản trả `True`
    ngay sau lỗi đọc — không hỏi PID nào — qua được chúng (lượt 4 đo: qua cả hai ca mẫu của r4 lẫn D) mà vẫn
    báo "sống" cho một PID con đã `wait`. Bốn tiểu nhãn theo thứ tự: `song`, `da-wait`, `eperm`, `eio`. Mỗi
    tiểu nhãn chạy CÙNG tám đầu vào đọc, theo thứ tự: EACCES, EIO, ESRCH (ba lỗi đọc của `B2-doc-hong`), p1,
    p2, p3 không khoảng trắng cuối, p3 có khoảng trắng cuối, p4 (đúng các đầu vào của `B2-parse`: bốn tiểu nhãn, năm lần đọc vì p3 có hai payload), luôn với
    seam `stat` EACCES để vào bước 4. Tổng 4 × 8 = 32 lời gọi `_con_song` trực tiếp. Con số 32 ở đây là số
    đầu vào của nhãn, KHÔNG phải số control của D (D có 65 control ở r8; 63 ở r7; HINT lượt 6 đề nghị 49; 43 ở r6). Ma trận vẫn tám đầu vào đọc: đầu vào
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
    đòi, theo thứ tự (quy ước chung, "Thứ tự assertion"): không ngoại lệ ghi nhận nào thoát; đúng MỘT lời gọi
    `kill(pid, 0)`; kết quả đúng như trên; bộ đếm seam `stat` = 1 và `read` = 1. Nới nhãn vẫn chạy mọi đầu vào và
    observer, chỉ bỏ assertion. Phân hạng ngoại lệ thoát ra khỏi `_con_song` theo quy ước chung (bốn loại) và, cho
    p1–p3, theo quy tắc của `B2-parse` (payload theo dõi, r9). Không đổi ngữ nghĩa Q-A.3/.4.
    **ĐỎ khi** (lớp (k), mỗi tiểu nhãn có một mutant độc chiếm về KẾT QUẢ, đã đo ở bảng 6): bản trả `True`
    ngay, không hỏi PID ⇒ `song` (số lời gọi `kill` bằng 0; dòng (k1)); bản hỏi PID nhưng bỏ kết quả ⇒ `da-wait`
    (PID đã `wait` được báo `True`; (k2)); bản tự xử lý `kill` và trả `False` cho `PermissionError` ⇒ `eperm`
    ((k3)); bản tự xử lý `kill` và trả `True` cho `OSError` khác ⇒ `eio` ((k4)); bản hỏi `kill` hai lần (một lần
    trong xử lý lỗi đọc, một lần ở khối chung) ⇒ `song`, bộ đếm bằng 2 ((k5), r6). Ba hướng "thoát" của khối
    `kill` (r6, lớp (l)): khối chỉ bắt `PermissionError` nên ESRCH thật thoát ⇒ `da-wait` (dòng (l22)); khối chỉ
    bắt `ProcessLookupError` nên EPERM thoát ⇒ `eperm` (dòng (l23)); khối bỏ mệnh đề `OSError` nên EIO thoát ⇒
    `eio` (dòng (l24)). `B3-da-wait` (không seam) KHÔNG thay được `da-wait` của nhãn này: nó không đi qua
    đường lỗi mới.
  - `B2-nhanh-cu` (r7, cross-review lượt 6; r7 mở rộng từ năm thành **mười chín** đầu vào (r8: **hai mươi**, thêm `utf8-hong-that`) theo bảng không gian mở
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
      `IndexError` tự nhiên ⇒ **`False`**. Hai đầu vào này dùng payload theo dõi của `B2-parse` (r9)
      để hướng "thoát" chết đúng lý do. `p4`: `read_text` ném MỘT `UnicodeDecodeError` dựng sẵn ⇒
      **`False`**. (HINT lượt 6 gọi `p1` là `rong`; r7 đổi tên cho khớp `B2-parse`.)
      `utf8-hong-that` (r8 lập; r9 ĐẢO kỳ vọng theo Q-A.7): PID là con THẬT đã đổi `comm` như đầu vào `4` của
      `B2-dem-doc` (cùng điều kiện dựng); `stat` và phép đọc THẬT (chỉ đếm), observer chuyển tiếp thật ⇒ **`True`**
      (tiến trình SỐNG), hỏi 1, đọc 1, `read args` đúng `DANG_DOC_QA7`, kill 0. Kỳ vọng r8 `False` là chính lời khai
      sai mà chủ kho quyết sửa: bản vá nháp Q-A.7 của lượt 8 đỏ ở đây với kỳ vọng r8 (`result True`). Trên helper KHÔNG
      có `read args` (lượt 8, ba Python) đột biến M4 đỏ ở đây `result False`; trên helper r9 M4 chết sớm hơn ở `read
      args` (A1 `B2-dem-lan`, W1 `B2-nhanh-cu song`), và răng riêng của đầu vào này là biến thể (E) `d0_giai_ma_lai_utf8`
      ⇒ `result False` (bảng 11). Với Q-A.7 đầu vào này không còn sinh ngoại lệ thật, nên W0 của `d0_value_thoat`,
      `d0_decode_thoat` không cần loại (2) mở rộng (đo lượt 8 và bảng 11: hai biến thể CHẤP NHẬN).
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
    `EIO`, `ESRCH`, `EPERM`, `p1`, `p3`, `p4`, `exception` (r8 thêm `utf8-hong-that`) — chúng có biến thể (E) giết
    đúng lý do, nhưng (E) và phép D chỉ chạy MỘT lần, trước merge; sau merge chỉ còn assertion của hai ca, chạy ở mỗi
    lượt suite mà không ai đo lại rằng chúng còn đỏ được. Răng BỀN (đo lại ở mỗi lượt `--dot-bien`): KHÔNG CÓ (r8 sửa
    chữ "KHÔNG ĐO ĐƯỢC" của r7 — không có dòng `DOT_BIEN` nào để đo), cùng tình trạng với `B3-song`, `B3-da-wait`.
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
    | R0-Đ0 | đọc được: `Z` ⇒ `False`, không `Z` ⇒ `True` (nguyên xi) | `B2-nhanh-cu song`, `utf8-hong-that` (r9: nội dung THẬT, `comm` không phải UTF-8); lời gọi đường cũ của `B3-zombie` | không-`Z` sai: E `d0_ok_khongZ_sai` · `Z` sai: E `d0_ok_Z_sai` |
    | R0-K0 | `kill` thành công ⇒ `True` (nền, Linux) | `B2-nhanh-cu vang` | sai: E `k0_ok_sai` |
    | R0-Đ | đọc được: `Z` ⇒ `False`, không `Z` ⇒ `True` (Q-A.4) | `B2-eacces`, `B2-eio`, `B2-eperm-hoi`, `B2-dem-doc 1`, `2`, `4` (r9: nội dung THẬT); hai lời gọi đường mới của `B3-zombie` | không-`Z` sai: E `d_ok_khongZ_sai` · `Z` sai: E `d_ok_Z_sai` (bỏ đọc: (c), tính ở trục C) |
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
    | Đ: đọc được | 1 | 1 | — (0 ở `B2-dem-doc 4`, r9) | `B2-eacces`, `B2-eio`, `B2-eperm-hoi`, `B2-dem-doc 1`, `2`, `4`, hai lời gọi đường mới của `B3-zombie` | hỏi lại khi `OSError` khác EACCES: E `d_hoi_lai_khac_EACCES` (bản vá sai của lượt 6) · đọc hai lần: (j1) · không đọc: (c) |
    | Đ → K: đọc lỗi hay hỏng | 1 | 1 | 1 | `B2-doc-hong`, `B2-parse`, `B2-dem-doc 3`, `B2-pid-du-phong`, tiểu nhãn `kill`/`kill-*` của ba nhãn sentinel | hỏi lại: E `k_hoi_hai_lan` · đọc lại: (j2) — thêm E `d_doc_lai_khi_EPERM` (bản vá sai của lượt 6) · kill hai lần: (k5) — thêm E `k_kill_lai_khi_doc_EPERM` · không gọi kill: (k1) |

    Hỏi, đọc hay gọi kill lại CÓ ĐIỀU KIỆN theo lớp ngoại lệ không cần hạng mục riêng: phép đếm đứng ở MỌI đầu vào
    của đường, nên bản vá chỉ lặp lại khi gặp lớp X chết ở đầu vào mang lớp X (đo: ba biến thể có điều kiện của lượt
    6 và r7, bảng 9 dòng 6 và 11). Giới hạn: lớp X không có đầu vào nào (errno thứ tư, lớp con cụ thể) ⇒ KHÔNG ĐO
    ĐƯỢC, như mục 3 và 5 của danh sách bất khả thi dưới đây.

    **Trục S — cú pháp phép tách.** Đầu vào: một zombie thật có `comm` = `x) R (y`, nội dung
    `<pid> (x) R (y) Z …`; chỉ phép tách theo dấu `)` CUỐI mới đọc ra `Z`. S-Đ: hai lời gọi đường mới của `B3-zombie`
    (seam EACCES ở `stat`), đóng bằng (m5). S-Đ0 (r7): lời gọi đường cũ của `B3-zombie` (không seam lỗi, chỉ đếm),
    đóng bằng E `d0_tach_ngoac_dau`. (r11, cross-review lượt 10) S ở ba hàm ngoài `_con_song` (Q-A.7): đầu vào là cháu
    của `t160`, `t161` mang `comm` `_K124_COMM_CHAU` = `tep (1) ` cộng 7 byte cuối của `_K124_COMM` (15 byte, có `) `,
    khoảng trắng, đuôi UTF-8 hỏng); đóng bằng ba biến thể (E) `s_khoa_tach_ngoac_dau`, `s_nhom_tach_ngoac_dau`,
    `s_chup_tach_ngoac_dau` (DS-E-KHAC, đích là ca B8 như `g_to_hop_dinh_dang_khoa`; bảng mở rộng là đường của
    `_con_song` nên số hạng mục không đổi). Đường thứ hai của trục S (tách cả dòng theo khoảng trắng) ở cả năm chỗ đọc
    dùng CHUNG đầu vào và chốt của đường `)` đầu — cả hai `comm` (`x) R (y`, `_K124_COMM_CHAU`) đều có khoảng trắng, và
    hằng ấy viết cứng trong đặc tả; đo trên rig (bảng 13), không thêm tên (E).

    **Trục G × API (r11, cross-review lượt 10).** `read args` của `t160`, `t161` đòi mọi sự kiện audit `open` trên
    `/proc/…`, đường tương đối hay fd số trong cửa sổ nằm TRONG một lời đọc `Path` đã ghi (B8, assertion (3)), nên đọc
    bằng API ngoài lời gọi đã khai bị bắt kể cả khi hành vi đúng. Hai khối đọc của `_con_song` còn chốt ở helper: seam
    `Path` thay CẢ lời gọi, nên đọc bằng đường khác thì seam không thấy và đếm đọc ra 0. Năm biến thể (E) thêm cho năm
    hạng mục sẵn có `g_khoa`, `g_nhom`, `g_chup`, `g_d0`, `g_d`, không tăng số hạng mục: `g_khoa_open`, `g_nhom_open`,
    `g_chup_open`, `g_d0_open`, `g_d_open` (giữ cách giải mã của ứng viên, chỉ đổi lời đọc sang `open()` — DS-E-KHAC).

    **Năm chỗ đọc × hai trục (r11) — liệt kê TRƯỚC khi vá; danh sách có thẩm quyền của hai trục S và API.** Đường S:
    (s1) tách theo `)` ĐẦU — `index`, `find`, `partition(b") ")`, `split(b")", 1)`, biểu thức chính quy không tham
    lam; (s2) tách cả dòng theo khoảng trắng — `split()[k]`. Đường API: (a1) `open()`/`io.open`/`codecs.open`;
    (a2) `Path.open()`; (a3) `os.open` rồi `os.read`; (a4) đường khác tới cùng nội dung — `/proc/<pid>/task/<pid>/stat`,
    `dir_fd` tương đối, và đường tuyệt đối không bắt đầu bằng `/proc/` (`//proc/<pid>/stat`, `/dev/fd/<n>`); (a5) tiến
    trình con (ví dụ `cat`); (a6) fd mở TRƯỚC cửa sổ. Số đo: bảng 13 (ba Python).

    | chỗ đọc (nền `423b4ba`) | S: đầu vào · chốt · (E) · đo | API: đầu vào · chốt · (E) · đo |
    |---|---|---|
    | `_khoa_danh_tinh` `:359`–`:362` | cháu `t160`, `t161` (`_K124_COMM_CHAU`) · (1)/(2) của `t160`, `t161` · `s_khoa_tach_ngoac_dau` · s1 (`SXa`, `SXb`, `SXp`) và s2 (`SW`): `t160`, `t161` `124 noi doi` | cửa sổ `t160`, `t161` · `read args` (open ngoài lời đọc đã ghi) phủ a1–a3, a4 trên `/proc/…` hay tương đối, a5 — a5 qua fd ống mà `Popen` bọc bằng `io.open` · `g_khoa_open` · a1/a2/a3 (`OPEN*`, `PATHOPEN`), a4 (`TASK_khoa`, `DIRFD_khoa`), a5 (`CAT_khoa`): `read args` (open ngoài); a4 dạng `//proc/…` (`SL2_khoa`): B8 QUA — chốt tĩnh ĐỎ; a6 và mọi đường khác: chốt tĩnh |
    | `_thanh_vien_nhom` `:436`–`:438` | như trên · `s_nhom_tach_ngoac_dau` · s1, s2: `t161` `124 noi doi` (`t160` QUA — cháu `setsid` không nằm trong nhóm của mẹ) | như trên · `g_nhom_open` · `OPEN*_nhom`: `read args` (open ngoài); a6: chốt tĩnh |
    | `_chup_cay` `:490`–`:494` | như trên · `s_chup_tach_ngoac_dau` · s1, s2: `t160` `124 noi doi`, `t161` `khong giet duoc` | như trên · `g_chup_open` · `OPEN*_chup`: `read args` (open ngoài); a6: chốt tĩnh |
    | `_con_song` Đ0 (nhánh tệp có) | zombie `x) R (y` — lời gọi đường cũ của `B3-zombie` · `B3-zombie` · `d0_tach_ngoac_dau` · s2 (`SW_d0`): `t156` `B3-zombie result True` | helper (seam thay cả lời gọi) và cửa sổ `t160`, `t161` (qua `_con_lai`) · đếm đọc; `read args` (open ngoài) · `g_d0_open` · `t156` `B2-nhanh-cu song read count 0`; `t160`, `t161` `read args` (open ngoài) |
    | `_con_song` Đ (đường lỗi mới) | zombie `x) R (y` + seam EACCES ở `stat` — hai lời gọi đường mới của `B3-zombie` · (m5) · `luot6_m5` · s2 (`SW_d`): `t156` `B2-parse p2 kill count 0` | helper · đếm đọc · `g_d_open` · `t156` `B2-eacces read count 0`; B8 không chạm (như M5): QUA ×4 |

    Ô nào dùng CHUNG một chốt với ô khác thì đã ghi; không ô nào chỉ có lời văn. Giới hạn: một đầu vào mỗi trục mỗi
    chỗ (một `comm` có `) ` cho ba hàm ngoài, một zombie cho hai khối của `_con_song`); đường thứ ba của trục S hay trục
    API mà danh sách trên chưa nêu: chốt tĩnh phủ ở ba hàm ngoài, seam đếm đọc phủ ở `_con_song` (mọi đường không đi qua
    lời gọi `Path` đã khai); hành vi riêng của một đường chưa ai nêu: CHƯA ĐO — nêu được thì dựng được biến thể và đo
    được, như mọi đường trong bảng.

    **Chốt tĩnh phần còn lại của ba hàm ngoài (r11).** Q-A.7 hứa: ngoài phép đọc, `_khoa_danh_tinh`,
    `_thanh_vien_nhom`, `_chup_cay` KHÔNG đổi. Ở ba hàm này hành vi đúng CHÍNH LÀ hành vi của nền, nên phép so với nền đo
    đúng lời hứa (khác `_con_song`, nơi cấu trúc đổi có chủ ý và bảng không gian mở rộng là chốt). Luật, chạy bằng
    `python3.11` (một bản cú pháp PEP 701 chỉ lộ ở 3.11 — đo): trích thân ba hàm bằng AST (dòng `def` đến
    `end_lineno`) trên nền `423b4ba` và trên ứng viên; (a) số dòng mỗi hàm BẰNG nền (56 / 57 / 85); (b) dòng thứ i tính
    từ dòng `def` (0) khác nền CHỈ khi i thuộc tập cho phép của dạng đã khai — dạng latin-1: dòng đọc (`_khoa_danh_tinh`
    9 = `:359`, `_thanh_vien_nhom` 28 = `:436`, `_chup_cay` 23 = `:490`); dạng bytes thêm dòng tách và dựng khoá của
    `_khoa_danh_tinh` (11, 12 = `:361`, `:362`), dòng tách và so `Z` của `_thanh_vien_nhom` (29, 30 = `:437`, `:438`),
    dòng tách, so `Z` và dựng khoá của `_chup_cay` (24, 25, 27 = `:491`, `:492`, `:494`); (c) dòng đọc BẰNG dòng nền với
    `.read_text()` thay bằng đúng lời gọi của `DANG_DOC_QA7`; (d) dạng bytes: dòng tách và dòng so `Z` BẰNG dòng nền với
    literal `")"`, `"Z"` thay bằng `b")"`, `b"Z"`. Dòng dựng khoá của dạng bytes để chốt động giữ (khoá độc lập
    `_k124_khoa_that`, Q-A.7). Vị trí và số dòng trên là của `423b4ba`; nền tiếp nối đổi ba hàm này thì dẫn xuất lại
    theo cùng luật và khai trong handoff. Kết quả nộp trong handoff (B6). Đo trên 62 bản nháp của rig r11 (bảng 13): 44 ĐỎ — mọi
    bản lệch ở ba hàm ngoài, kể cả `CAT_khoa`, `TASK_khoa`, `DIRFD_khoa`, `SL2_khoa`, `OPEN*`, `SX*`, `SW_khoa`/`nhom`/
    `chup`, `ZB_*`, M1–M3, M12, `SE_*`, `WKa*`, `WC_crash`, nền, `P701` (chỉ khi chạy bằng 3.11; 3.13 cho ĐẠT); 18 ĐẠT —
    bốn ứng viên nháp, mười một bản không chạm ba hàm ngoài (M4, M5, `g_d0_open`, `g_d_open`, `SW_d0`, `SW_d`,
    `D0_KIEMDL`, `KILLNEVER`, `MEBO`, `MEHAN`, `cand_a_WAITK`) và `WK`, `WK1`, `WK2` (chỉ đổi dòng dựng khoá; chốt động
    bắt, bảng B8).

    **Trục N — nơi gọi** (§2): `:607` (`_con_song_dung_khoa`) — đo qua `B1` (trực tiếp và qua `_giet_rieng`),
    `B3-zombie`, và `B3b-giet-cay` (`_giet_cay` → `_con_lai` → `:607`); `:857`, `:882` (`_giet_windows`) — nhánh
    Windows, ngoài phạm vi (Q-A.6); `:1020`, `:1039` (`_giet_cay` khi `_con_lai` trả `None`, tức không đo được cây)
    — không đầu vào nào của hai ca đi qua, nhưng ĐO ĐƯỢC bằng một seam (r8, cross-review lượt 7): `Path.iterdir`
    ném EACCES riêng cho `/proc` ⇒ `_chup_cay`, `_thanh_vien_nhom` trả `None` ⇒ `_con_lai()` là `None`. Con sống,
    seam EACCES ở `Path.stat`: ứng viên nháp ⇒ `tron_ven=False`, **125** ("SIGTERM: me da chet, KHONG do duoc cay",
    0,10 giây); đột biến (c) ⇒ **125** (2,31 giây) — số của reviewer lượt 7 (3.12.3); phiên soạn r8 đo lại ở ba
    Python, cùng kết quả (bảng 10 dòng 8). Hai nơi ấy dựng `KetGiet(…, False, …)` — `ca_cay` viết cứng
    `False` — nên mã LUÔN là 125; `_con_song` ở đó chỉ đổi `me_da_chet` và thời lượng. Không có rủi ro 124/125 do
    bản vá tại hai nơi ấy; không bắt buộc thêm đầu vào.

    **Trục G — dạng phép đọc (r9, Q-A.7).** Năm hạng mục, mỗi chỗ đọc `/proc/<pid>/stat` một hạng mục, hướng "lệch
    dạng" (đọc bằng dạng ngoài danh sách cho phép): `g_khoa` (`_khoa_danh_tinh`), `g_nhom` (`_thanh_vien_nhom`),
    `g_chup` (`_chup_cay`), `g_d0`, `g_d` (hai khối đọc của `_con_song`). Đầu vào: bốn ca B8 (hành vi đầu-cuối);
    `read args` ở mọi đầu vào có đếm đọc của `t156_...` (G-Đ0, G-Đ) và ở `t160`, `t161` (mọi lời đọc trong cửa sổ, cả
    năm chỗ); hai đầu vào nội dung thật và đuôi `comm` của `B3-zombie` (hành vi khi đối số đúng). Đóng bằng MỘT biến
    thể E mỗi hạng mục: M1–M5 của B8 (trả lời đọc về `read_text()` không đối số). Thêm cho hạng mục sẵn có, không tăng
    số hạng mục: `d0_giai_ma_long`, `d_giai_ma_long` (`errors="replace"` ở G-Đ0, G-Đ); `g_khoa_errors`, `g_nhom_errors`,
    `g_chup_errors` (`errors="surrogateescape"` ở ba hàm ngoài `_con_song`: hành vi đúng ở locale UTF-8, chỉ `read
    args` của `t160`/`t161` bắt được); `d0_giai_ma_lai_utf8`, `d_giai_ma_lai_utf8` (đúng đối số, giải mã lại UTF-8 sau
    khi đọc — răng riêng của hai đầu vào nội dung thật). Tổ hợp `g_to_hop_khoa_nhom` = M12 (B8). Số đo: bảng 11. (r10)
    Tổ hợp `g_to_hop_dinh_dang_khoa` (B8, Q-A.7 "định dạng khoá có CHỐT"): dạng bytes bỏ giải mã trường số ở CẢ HAI chỗ
    dựng khoá (`_khoa_danh_tinh`, `_chup_cay`) — đúng đối số, sai định dạng khoá; miễn "một vị trí" như M12, cùng lý do:
    mỗi vị trí đơn lẻ đã bị `t160`, `t161` giết (hai hàng đối chiếu của bảng B8; lượt 9 và bảng 12, ba Python), chỉ
    tổ hợp nhất quán mới né được thước đo nội bộ — và bị khoá độc lập `_k124_khoa_that` bắt (Q-A.7). (r11,
    cross-review lượt 10, lớp `khoa-dinh-dang-khong-co-chot`) **Định nghĩa chung cho CẢ HAI dạng của Q-A.7:** biến thể
    `g_to_hop_dinh_dang_khoa` là MỘT định dạng khoá khác nền `linux:<chuỗi thập phân ASCII>`, NHẤT QUÁN ở cả hai chỗ
    dựng khoá, đúng đối số đọc. Dạng bytes: bỏ bước giải mã trường số (khoá `linux:b'…'`). Dạng latin-1 — không có bước
    giải mã để bỏ — dùng `!r` ở cả hai chỗ (`f"linux:{sau[19]!r}"`, khoá `linux:'…'`). Tự liệt kê (r11): hai dạng × ba
    tổ hợp vị trí (chỉ `_khoa_danh_tinh`, chỉ `_chup_cay`, cả hai) = sáu bản; nơi SO khoá (`:607`, `:896`, `:921`,
    `lenh_stop` qua `run.json`) chỉ so chuỗi, không dựng — không cần hàng riêng. Đo cả sáu trên khối r11, ba Python
    (bảng 13): dạng nào cũng vậy — cả hai chỗ ⇒ `t160` `khong giet duoc` (khoá KHÁC), ba ô kia QUA; chỉ
    `_khoa_danh_tinh` ⇒ `t160` `khong giet duoc`, `t161` `124 noi doi`; chỉ `_chup_cay` ⇒ `t160`, `t161` `124 noi doi`
    — trùng số lượt 10 và bảng 12. Mỗi vị trí đơn lẻ đã bị giết, nên miễn "một vị trí" giữ nguyên lý do.

    **Kiểm đếm bảng mở rộng** (đếm từ bảng; biến thể và kết quả đo ở bảng 9, 10 và 11): 30 ô (6 hàng × 5 tầng), ô nào cũng
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
    **(r9)** Trục G thêm **5** hạng mục ⇒ **134 hạng mục**; 54 dòng B5 vẫn phủ 51; **83** hạng mục có biến thể E
    (78 + 5). Bộ (E) của r11: **118 dòng** = 83 hạng mục + 35 dòng khác (r10: 110 = 83 + 27; r9: 109 = 83 + 26) — 12
    biến thể thêm của trục G (r11 thêm năm `g_*_open`, một cho mỗi chỗ đọc), 3 biến thể trục S ở ba hàm ngoài (r11), 2
    tổ hợp (M12; r10 thêm `g_to_hop_dinh_dang_khoa`), 2
    biến thể lặp có điều kiện (`d_doc_lai_khi_EPERM`, `k_kill_lai_khi_doc_EPERM`), 5 bản vá sai của lượt 6 trùng
    (m1)–(m5), 8 đối chứng luật `B2-parse` (khác đối số; fp; fp2–fp6; fp6b), 1 đối chứng loại (2) ((j1) sai đối số), 2
    đối chứng sống — cộng 2 phép giả gọi lại hàm trợ giúp nếu ứng viên tách trong hàm trợ giúp. Danh sách tên ĐÓNG:
    (E) mục 6. Bộ 95 của r8 và bộ 89 của r7: đoạn này của r8 (sha256 `2ae6ee04…2aa3`).

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
       giống hệt. `os.kill(pid, 0)` trả EACCES trên kernel thật: r7–r10 ghi "KHÔNG ĐO ĐƯỢC (chưa thử)" — sai nhãn, chưa
       thử không phải không đo được (lớp `khai-khong-do-duoc-ma-do-duoc`). **(r11) ĐÃ THỬ:** dưới uid 65534,
       `os.kill(pid, 0)` trên mọi PID trong `/proc` (2329–2331 PID) ⇒ EPERM ở mọi PID khác chủ, thành công ở chính nó,
       ESRCH với hai PID ngoài `pid_max`, **0 EACCES**, ba Python (bảng 13). Trên các PID đã thử kernel không sinh
       EACCES ở phép này; gộp vào EPERM là gộp một thành viên chỉ seam sinh ra.
    5. Lớp ngoại lệ ngoài năm hàng: con của `OSError` như `TimeoutError`, `InterruptedError`, `BlockingIOError`
       đi cùng R2 (mệnh đề `OSError`); `MemoryError`, `RecursionError`, `TypeError` đi cùng R4; `SystemExit`,
       `GeneratorExit` đi cùng R5. Không có đầu vào riêng — bộ tương đương theo LỚP CHA mà mọi mệnh đề tự
       nhiên bắt; đột biến liệt kê tên một lớp con cụ thể (ví dụ `except (OSError, MemoryError)`): **KHÔNG ĐO ĐƯỢC**.
    6. Mở rộng phạm vi khối `try` sang thêm câu lệnh (bọc luôn `kill` vào khối đọc): không có dạng tự nhiên đã
       biết cho đường lỗi này; hệ quả của nó — nhóm phân tích bị bắt ở tầng K — đã đo qua R3-K.
    7. (r7) R2-K0, thành viên EACCES: gộp vào EPERM như R2-K (mục 4), cùng lý do.
    8. (r7) Cột Đ0 dùng MỘT payload cho mỗi thành viên nhóm phân tích (`p1` rỗng cho `ValueError`, `p3` không khoảng
       trắng cuối cho `IndexError`); `p2` và payload thứ hai của `p3` không lặp lại ở Đ0. Hình dạng "kiểm tra dữ liệu
       thay cho bắt ngoại lệ" ở nhánh cũ (như (l16) ở nhánh mới): r7–r10 ghi "chưa có biến thể — KHÔNG ĐO ĐƯỢC", sai
       nhãn (chưa dựng). **(r11) ĐÃ DỰNG VÀ ĐO:** bản Đ0 chỉ bắt `OSError` rồi kiểm dữ liệu nhận MỘT dạng hỏng (nội dung
       rỗng) ⇒ `t156` `B2-nhanh-cu p3 parse error escaped (IndexError …)`, ba Python (bảng 13) — `p3` giết nó. Một
       biến thể không chứng minh mọi cách kiểm dữ liệu đều bị bắt (giới hạn chung của (E)).
    9. (r7) errno thứ tư và lớp con cụ thể ở cột Đ0 và K0: cùng giới hạn như mục 3 và 5.
    10. (r7; r8 sửa) Trục N, `:1020` và `:1039`: không đầu vào của hai ca đi qua, nhưng đo được bằng seam
       `Path.iterdir("/proc")` — mã luôn 125 ở hai nơi ấy (xem trục N).
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
    biến lấy đúng chúng làm đích — chưa được đo: **CHƯA ĐO** ở packet này (r11 sửa nhãn "KHÔNG ĐO ĐƯỢC" của r6–r10:
    dựng được, chưa dựng); chúng vẫn được khoá bằng
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
    một lần); `B3-song` và `B3-da-wait` không có biến thể E nào lấy làm đích — răng riêng: CHƯA ĐO (r11 sửa nhãn). Số bộ là
    số ĐO trên một cách cài, không suy từ văn bản (xem đính chính sau bảng 8 về (g1)). **(r8)** Hai đơn vị mới
    (`B2-nhanh-cu utf8-hong-that`, `B2-dem-doc 4`) không có dòng B5 nào lấy làm đích — suy từ B5, không đo lại chữ ký
    ở r8 — nên danh sách trên thành **11** trên 57 đơn vị; cả hai có biến thể E giết đúng lý do (bảng 10 dòng 4; với
    kỳ vọng r9: `d0_giai_ma_lai_utf8`, `d_giai_ma_lai_utf8`, bảng 11).

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
    | `B2-dem-doc` | `1`, `2`, `3`, `4` (r8) | 4 |
    | `B2-pid-du-phong` | `song`, `da-wait`, `eperm`, `eio` | 4 |
    | `B2-nhanh-cu` (r7) | `song`, `EACCES`, `EIO`, `ESRCH`, `EPERM`, `p1`, `p3`, `p4`, `utf8-hong-that` (r8), `tin-hieu`, `exception`, `vang`, `vang-da-wait`, `vang-eperm`, `vang-eio`, `vang-tin-hieu`, `vang-exception`, `vang-index`, `vang-value`, `vang-decode` | 20 |

    Tổng: 16 nhãn của `t156_...` + 1 của `t157_...` = 17 nhãn; tám nhãn có tiểu nhãn gồm **48** đơn vị (r8; r7: 46); các
    nhãn còn lại (tám trong `t156_...`, một trong `t157_...`) mỗi nhãn một đơn vị ⇒ 48 + 9 = **57 đơn vị** (r7: 46 + 9 = 55)
    (HINT lượt 6: 17 nhãn, 32 + 9 = 41; r6: 16 nhãn, 27 + 9 = 36). Đo trên rig r7 (bảng 9 dòng 4): 17 nhãn, 46 tiểu
    nhãn, 55 đơn vị.
    Đo trên rig cross-review lượt 7 với hai đầu vào r8 (ba Python): t156 56 đơn vị + t157 1 = 57; D 65/65 control,
    6/6 phép đảo; 54 dòng vẫn 55/55 cặp. Đo lại trên rig riêng của phiên soạn r8 (ba Python, bảng 10 dòng 2 và 3): cùng
    các số ấy.

    Bốn điều r3–r5 đã đo là sai nếu làm tắt, điều thứ năm r6 thêm, thứ sáu r7 thêm, thứ bảy r8 thêm, thứ tám r9 thêm: (1) EACCES ở tầng đọc **không đại
    diện** cho họ `OSError` — một bản chỉ bắt `PermissionError` ở tầng đọc qua cả hai ca r3 (bảng 5); (2) ESRCH ở
    tầng hỏi **không thay** ESRCH ở tầng đọc, kỳ vọng ngược nhau; (3) sentinel `RuntimeError` **không thay**
    sentinel `KeyboardInterrupt` ở tầng đọc; (4) `True` trên PID sống **không chứng minh** đã hỏi PID (bảng 6):
    phải có PID đã `wait` (kết quả `False`), có quan sát đúng lời gọi `kill(pid, 0)`, và có kết quả EPERM/EIO của
    chính lời gọi ấy; (5) **một sentinel của nhóm này không đại diện cho nhóm khác và một tầng không đại diện
    cho tầng khác** — `RuntimeError` ở tầng hỏi không thay `IndexError`/`ValueError`/`UnicodeDecodeError` ở tầng
    hỏi (bản HINT lượt 5 qua hai ca r5 và phép D mà vẫn nuốt `IndexError`), và mọi sentinel ở tầng hỏi hay đọc
    không thay cho tầng kill; (6, r7) **đường mới không đại diện cho nhánh cũ, khối kill dùng chung không đại diện
    cho khối kill tách riêng, và phép đếm ở vài nhãn không đại diện cho phép đếm trên mọi đường** — một helper dựng
    đúng theo HINT lượt 6 để lọt 34 biến thể trái Q-A (bảng 9 dòng 7); (7, r8; r9 sửa tiền đề) **một seam thay CẢ lời
    gọi không đại diện cho lời gọi thật** — kết quả của nó không phụ thuộc cách giải mã của lời gọi, nên cách giải mã
    phải khoá bằng đầu vào nội dung THẬT và bằng `read args` (seam vẫn NHẬN đủ đối số: lượt 8 đo; câu r8 "không thấy
    đối số" sai); (8, r9) **đúng đối số không đại diện cho đúng hành vi** — `read args` bắt mọi dạng đọc lệch, nhưng
    giải mã lại sau khi đọc thì chỉ đầu vào nội dung thật bắt (bảng 11). Đây là chốt của hợp đồng Q-A, không phải lời
    khai rằng kernel thật đã sinh các lỗi ấy. Handoff phải ghi từng đầu vào và nhãn giết (kèm tiểu nhãn và loại
    assertion).
- **B3 (mục 2) — đối chứng dương, và zombie chưa `wait`.** Không seam: `_con_song(os.getpid())` ⇒
  `True` (nhãn `B3-song`); `_con_song` trên PID con đã `wait` ⇒ `False` (nhãn `B3-da-wait`). Rồi một
  con thật, session riêng, SIGTERM thật,
  đọc `/proc/<pid>/stat` bằng phép đọc **độc lập với launcher** cho tới khi thấy `Z`, **chưa `wait`**;
  đặt seam EACCES chỉ ở `Path.stat` của PID ấy (để `read_text` thật vẫn đọc được): `_con_song` và
  `_con_song_dung_khoa` đều phải `False`. Nhãn `B3-zombie`. **(r7; r9 thêm đuôi)** Con đặt `comm` = `x) R (y` cộng
  hai byte `e1 ba` (UTF-8 hỏng ở đuôi) bằng `prctl(PR_SET_NAME)` TRƯỚC khi nhận SIGTERM, và ca xác nhận bằng phép đọc
  BYTES độc lập rằng `(x) R (y` + `e1 ba` + `)` có trong `/proc/<pid>/stat` (không có ⇒ ném lỗi thường, không dùng
  `bang`): nội dung khi ấy là `<pid> (x) R (y…) Z …`, chỉ phép tách theo dấu `)` CUỐI mới đọc ra `Z` (Q-A.4 "đọc được
  và trạng thái là `Z` ⇒ `False`"), và (r9) chỉ phép đọc theo Q-A.7 mới đọc được nó trên đường MỚI: một phép đọc
  giải mã UTF-8 chặt rơi về `kill`, mà `kill(zombie, 0)` thành công ⇒ `result True` (lượt 8 đo M5 chết ở đây khi chạy
  riêng nhãn, ba Python; trên helper r9 A1 của M5 dừng sớm hơn ở `B2-eacces read args`, và biến thể đúng đối số
  `d_giai_ma_lai_utf8` chết ở đây với W1 `B3-zombie result True` — bảng 11). Hai lời gọi
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
- **B4 (mục 2) — nền.** Ngoài Linux (`LA_WINDOWS`, Darwin) sáu ca mới (hai ca helper, bốn ca B8) **trả chuỗi lý
  do** (BỎ QUA có khai theo quy ước sẵn của tệp), không trả QUA: nhánh `/proc` không tồn tại ở đó.
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
  `launcher_test.py:8294` trên `423b4ba`, `:8293` trên `89fc4fa`), và dưới sàn thì `--dot-bien` in `!! DUOI SAN`
  rồi trả 1 (`:8298–8303`; `89fc4fa`: `:8297–8302`). Sau r7 (54 dòng
  mới, như HINT): **65/231 không đo được trên Windows, 71,86 % đo được, trần 69 ⇒ biên 4 mục** — cận dưới tĩnh: ca
  bỏ qua giữa thân không đếm được, nên biên THẬT có thể nhỏ hơn. Thêm n dòng Linux-only nữa: n = 1, 2, 3, 4, 5, 6 ⇒
  biên 3, 2, 2, 1, 0, 0 (vẫn đạt); **n = 7 ⇒ `DUOI SAN`** (69,75 %). Đây là giới hạn CỨNG, đo được, của cách làm
  "thêm một mục đột biến cho mỗi ô": 78 hạng mục của bảng không gian mở rộng không có dòng B5 riêng, và đưa chúng
  vào `DOT_BIEN` sẽ làm Windows rơi xuống dưới sàn ngay (231 + 78 = 309 mục, 65 + 78 = 143 không đo được, còn
  166/309 = 53,72 % đo được — suy bằng số học từ cùng phép đếm, không dựng và không chạy). Vì vậy r7 đến r10 giữ
  `DOT_BIEN` ở 54 dòng và đo các hạng mục còn lại bằng phép (E) trong tập lệnh bằng chứng cục bộ (B5); r9, r10 đặt
  các biến thể lớp 124 (M1–M5, M12; r10 thêm `g_to_hop_dinh_dang_khoa` — B8) ở (E) cùng lý do, nên biên vẫn 4.
  **Giới hạn CỨNG ở trên chỉ đúng cho dòng mà MỌI ca đích đều BỎ QUA trên Windows** (r10, cross-review lượt 9, lớp
  `rang-ben-b8-bo-sot-phuong-an`): runner đếm một dòng là đo được khi còn ít nhất một ca đích chạy (`can_do =
  len(phai_chet) - len(bo_qua)`, `launcher_test.py:8034` trên `423b4ba`), nên một dòng có thêm ĐÍCH ĐA NỀN — một ca
  TĨNH chạy mọi nền, ví dụ AST kiểm năm lời đọc `/proc/<pid>/stat` đúng `DANG_DOC_QA7` — không ăn biên. Đo (lượt 9,
  runner `chay_dot_bien()` thật, 3.12.3, sáu dòng M1–M5, M12 cộng một ca tĩnh làm đích phụ): Linux M1 `giet 4/4`, M2,
  M3, M4 `3/3`, M5 `1/1` (rig không có `t156`), M12 `5/5`; Windows giả lập (`platform.system`) cả sáu `giet 1/1` qua
  ca tĩnh ⇒ 237 mục, 65 không đo được, 72,57 %, **biên 6**; không có ca tĩnh ⇒ năm dòng `KHONG DO DUOC`. Trên Windows
  dòng ấy chỉ đo DẠNG đọc; hành vi vẫn đo lại ở Linux mỗi lượt. Biến thể thứ bảy `g_to_hop_dinh_dang_khoa` sai ĐỊNH
  DẠNG KHOÁ, không sai dạng đọc, nên ca tĩnh ấy không bắt được nó: đưa nó vào `DOT_BIEN` là thêm một dòng Linux-only
  (có ca tĩnh: 238 / 66 ⇒ 72,27 %, biên 5; không có ca tĩnh: 238 / 72 ⇒ 69,75 %, `DUOI SAN` — tính bằng chính
  `_dot_bien_du_san` của `423b4ba`, bảng 12). Đổi cân bằng này — thêm dòng `DOT_BIEN`, thêm ca tĩnh, hay cho các ca
  chạy nhánh `/proc` trên Windows bằng seam — là quyết định của điều phối/chủ kho, r7 đến r10 không tự chọn (§11.3).

**Ca `t157_...`**

- **B3b (mục 2) — chốt tiêu thụ `_giet_cay`.** Con thật CÒN SỐNG, session riêng, `khoa` lấy trước seam;
  seam EACCES ở `Path.stat` của PID ấy; gọi `_giet_cay(pid, khoa)` để SIGTERM thật biến con thành
  zombie chưa `wait`; kết quả phải có `tron_ven=True` (phía deadline ánh xạ 124, `launcher.py:1669`).
  Nhãn `B3b-giet-cay`. Dọn PID con và `wait` trong `finally`. Ca này riêng để đột biến (c) ở B5 làm
  **cả hai** ca `t156_...` lẫn `t157_...` đỏ, mỗi ca bằng `TinHieuChotCa` của chính nó.
  **ĐỎ khi:** đột biến bỏ phép đọc nội dung ⇒ `tron_ven=False` ⇒ tương ứng 125 (bảng 2, hàng HẸP r1).
  **Phạm vi của chốt (r8; r9 sửa).** B3b chỉ phủ lỗi của PHÉP HỎI. Lỗi của phép ĐỌC khoá danh tính, quét nhóm và
  ảnh chụp khi `comm` không giải mã được (124 / 0 / 10 cho tiến trình còn sống, §2) do B8 khoá (r9).

**B8 (r9, lớp `sua-124-trong-packet`, quyết định chủ kho 30-09) — bốn ca khoá `t158_...` đến `t161_...`: `comm`
không giải mã được KHÔNG được làm 124 (hay `stop` rc=0) nói dối.** Bất biến: "124 ⇔ cả cây ĐÃ CHẾT" và "`stop`
rc=0 ⇔ cây đã sạch" không phụ thuộc cách giải mã `comm`. Kích hoạt THẬT: kernel cắt `comm` ở 15 byte nên tên tiếng
Việt thành UTF-8 hỏng; locale không phải UTF-8 làm cả `comm` UTF-8 hợp lệ nổ (§2). **Bốn ca đăng ký riêng, KHÔNG dùng
helper** (r9 chọn; HINT lượt 8 khuyến nghị bốn nhãn của `t157_...`): dạng bốn ca là dạng đã ĐO (lượt 8, bảng 11), dạng
nhãn chỉ có số học (21 nhãn / 61 đơn vị / 69 control); bốn ca riêng giữ helper, A/W và D của `t156_...`, `t157_...`
đúng như r8 (17 nhãn / 48 tiểu nhãn / 57 đơn vị / 65 control).
  · `t158` `B8-sau-sinh` — `run --deadline-utc` (hạn 3 s) trên con đổi `comm` thành 15 byte hỏng 0,5 s SAU lúc sinh
    (launcher đã lấy khoá với `comm` bình thường); con ghi nhịp 0,1 s/lần ra tệp.
  · `t159` `B8-luc-sinh` — như trên, nhưng chương trình là symlink tên `kiểm_tra_tiến_trình` trỏ tới Python: `comm`
    hỏng NGAY lúc exec, không `prctl`.
  · `t160` `B8-setsid` — khoá của mẹ lấy bằng phép đọc BYTES độc lập theo định dạng nền (`_k124_khoa_that`, r10), rồi
    `_giet_cay` gọi trực tiếp: mẹ (session riêng) sinh cháu `setsid`; cháu phớt lờ SIGTERM, đổi `comm`.
  · `t161` `B8-me-thoat` — lấy khoá của mẹ (cùng cách, r10), mẹ thoát, rồi `_giet_cay`; cháu CÙNG NHÓM đổi `comm`, còn
    sống.
Điều kiện dựng (không đạt ⇒ lỗi thường, KHÔNG `bang`): `comm` của con/cháu đọc bằng BYTES đúng 15 byte ấy (cháu:
`_K124_COMM_CHAU`, r11); ở `t158`
khoá trong sổ khác `None`; tên tiếng Việt tạo được; ở `t160`, `t161` observer ghi được ít nhất một lời đọc. Assertion
theo thứ tự; thông điệp mở đầu bằng tên đầu vào rồi LOẠI: (1) `124 noi doi` — không được có 124 (hay `tron_ven=True`)
cùng một tiến trình còn sống hoặc nhịp còn tăng sau 1 s; (2) `qua han khong giet duoc` (`t158`, `t159`) hay `khong
giet duoc` (`t160`, `t161`) — quá hạn phải GIẾT THẬT; (3) chỉ ở `t160`, `t161`: `read args` — observer ghi (phương
thức, args, kwargs) MỌI lời đọc `Path` trên `/proc/<số>/stat` trong cửa sổ quanh `_giet_cay`, mọi bản ghi phải BẰNG
`DANG_DOC_QA7`, và (r11) KHÔNG sự kiện audit `open` nào trên `/proc/…`, trên đường tương đối hay trên fd số được xảy
ra NGOÀI một lời đọc đã ghi — lời đọc `Path` đã khai trên đúng `/proc/<số>/stat` là đường mở tệp DUY NHẤT được phép
(Q-A.7 (ii); kiểm ở ba hàm ngoài VÀ khối đọc nhánh tệp có của `_con_song`, vì `_con_lai` gọi nó trong cửa sổ). Thông
điệp: `read args ['open ngoai loi doc Path: <n> su kien, vd […]']`. HINT lượt 10 đếm "số `open` BẰNG số lời đọc" trên
đúng đường `/proc/<số>/stat`; r11 đổi sang "không `open` nào ngoài" vì hai phép đo (bảng 13): bộ lọc đường của HINT
không thấy `/proc/<pid>/task/<pid>/stat` (`TASK_khoa` QUA ở `t160`, `t161` với khối HINT, 3.12), và bỏ qua fd số,
tức ống của tiến trình con (`CAT_khoa`, cùng kết quả). Đường tuyệt đối KHÔNG bắt đầu bằng `/proc/` không tính, PHÒNG XA chứ không phải lỗi đã gặp: máy
nạp module mở `.pyc` một cách lười ngay trong cửa sổ (đo: log của `TASK_khoa` ghi `…/encodings/__pycache__/latin_1…pyc`),
nên một lần nạp lười ngoài lời đọc đã ghi ở một ứng viên đúng sẽ thành đỏ oan. Với bốn ứng viên nháp điều đó KHÔNG xảy
ra (đo: bản nháp tính mọi đường cho `cand_a`, `cand_b` QUA ở `t160`, `t161`, ba Python, kể cả khi `_k124_khoa_that`
không giải mã ascii — `read_text(encoding=…)` tra codec BÊN TRONG lời đọc đã ghi, còn `bytes.decode("ascii")` đi đường
tắt của CPython, không nạp module). Giá phải khai: đường tuyệt đối tới cùng nội dung mà không bắt đầu bằng `/proc/`
(`//proc/<pid>/stat` — POSIX giữ hai dấu `/` đầu; `/dev/fd/<n>`) thước đo này không thấy — đo: `SL2_khoa` QUA ở `t160`,
`t161` — và chốt tĩnh bắt (ba hàm ngoài), seam đếm đọc bắt (`_con_song`). `t158`, `t159` chạy
launcher ở tiến trình con nên không có observer. Phép kiểm sống đọc BYTES riêng (và `_con_song_that` phải đọc bytes —
§6 mục 3). **Khung ca tự canh điều kiện đo của chính nó (r10, cross-review lượt 9, lớp `b8-khung-ca-thieu-chot`):**
(a) con của `t158`, `t159` tự ghi PID vào `<tệp nhịp>.pid` trước mọi việc khác; `finally` chờ tệp ấy tối đa 2 s rồi
dọn bằng PID ấy, chỉ khi `/proc/<pid>/cmdline` mang đường tệp nhịp của ca — KHÔNG dọn theo PID do launcher-đang-thử
báo; (b) HẠN SỐNG: con ghi tối đa 1200 nhịp (khoảng 120 s) rồi tự thoát, mẹ và cháu của `t160`, `t161` là
`time.sleep(120)` — dọn hỏng thì tiến trình vẫn tự chết; **và (r11, cross-review lượt 10) chết vì HẾT HẠN không phải
bị giết, ca phải ĐỎ đúng loại.** Con và cháu ghi dấu `<tệp>.tu_thoat` ở `finally` — `han_song` khi hết hạn,
`ngoai_le` khi chết vì ngoại lệ; tín hiệu mặc định giết tiến trình KHÔNG chạy `finally`, và ca không phải cha của con
(`t158`, `t159`: cha là launcher, launcher `wait` nó) hay của cháu nên không đọc được mã thoát. Mẹ của `t160` là con
TRỰC TIẾP của ca, nên đọc bằng MÃ THOÁT: `poll()` âm ⇔ tín hiệu giết, `None` ⇔ còn sống, ≥ 0 ⇔ tự thoát. Dấu
`han_song` hay mẹ có mã ≥ 0 ⇒ assertion (2) ĐỎ (`qua han khong giet duoc` / `khong giet duoc`; thông điệp ghi `tu
thoat=han_song` hay `me rc=0`); dấu `ngoai_le` ⇒ lỗi thường (điều kiện dựng: con/cháu chết vô can không được thành
tín dụng); assertion (1) của `t160` tính cả mẹ còn sống (lời (1) nói "một tiến trình còn sống", mã r10 chỉ hỏi cháu).
r11 BỎ hai chốt thời gian của HINT lượt 10 (`n2 >= 1200` và `_giet_cay` quá 60 s ⇒ lỗi thường): lỗi thường không phải
ĐỎ đúng loại; thời gian là đại lượng thay thế, không phải phép đo "có bị giết không"; và chốt 60 s đứng TRƯỚC
assertion nên biến chính các ca "không giết" thành lỗi thường (đo: `MEHAN`, `KILLNEVER` trên khối HINT ⇒ `dieu kien
dung: _giet_cay qua 60 s`; cùng hai bản trên khối r11 ⇒ `TinHieuChotCa` `khong giet duoc` — bảng 13). Lý do đo được (VERDICT lượt 10): launcher nói dối (nền, M12) cộng chờ
con KHÔNG hạn sau `_giet_cay` (`p.wait()` thay `p.wait(timeout=5)`) làm `t158` QUA sau 122 s với khối r10 — ca duy
nhất giết M12 đơn lẻ; `_giet_cay` chờ mãi không SIGKILL làm `t160`, `t161` QUA sau 120 s. **Đường vào r11 tự liệt kê
trước khi vá** — mỗi đường một chốt và một đột biến RIG chứng răng (không phải biến thể (E): như WAITK/KILLNEVER của
lượt 10, chúng sửa khung chạy của launcher chứ không phải một vị trí Q-A); số đo ở bảng 13:

| đường "không bị giết mà trông như đã chết/đã sạch" | ca | chốt (r11) | đột biến rig |
|---|---|---|---|
| con tự thoát ở 1200 nhịp | `t158`, `t159` | dấu `han_song` ⇒ (2) | `nen_WAITK`, `M12_WAITK` (chờ con không hạn) |
| cháu tự thoát ở `time.sleep(120)` | `t160`, `t161` | dấu `han_song` ⇒ (2) | `KILLNEVER` (vòng chờ SIGTERM không bao giờ SIGKILL) |
| mẹ tự thoát ở `time.sleep(120)` | `t160` | mã thoát ≥ 0 ⇒ (2) | `MEHAN` (bỏ sót gốc, chờ 125 s sau SIGKILL cháu) |
| mẹ còn sống khi `_giet_cay` báo `tron_ven` | `t160` | `poll()` là `None` ⇒ (1) | `MEBO` (bỏ sót gốc khi ảnh có hậu duệ) |
| con/cháu chết vì ngoại lệ (không bị giết, chưa hết hạn) | cả bốn | dấu `ngoai_le` ⇒ lỗi thường | probe (bảng 13): tệp `comm` không ghi được ⇒ `ngoai_le` ⇒ `RuntimeError` |
| mẹ của `t161` thoát | `t161` | không phải đường: mẹ thoát CÓ CHỦ Ý và được `wait` trước `_giet_cay` | — |

(c) `_k124_run` đòi sổ JSON có `pid` và rc là một kết cục hạn
chót của `run` (124, 125 hay 10; `launcher.py:1669`, `:1684`), khác thì lỗi thường — launcher CHẾT vô can (`rc=1`) không
được thành `TinHieuChotCa` `qua han khong giet duoc`; (d) `t158`, `t159` trả chuỗi BỎ QUA có khai khi
`locale.getpreferredencoding(False)` giải mã được 15 byte hỏng: ở đó lỗi 124 không tái hiện được, và ca biết mình không
đo gì. `t160`, `t161` KHÔNG BỎ QUA theo locale: `read args` và chốt định dạng khoá của chúng không phụ thuộc locale nên
vẫn đo được, chỉ assertion (1), (2) mất nghĩa ở đó (bảng 12; r11 đo lại ở bốn locale giải mã được: bảng 13). Hai đầu vào nội dung thật của `t156` thì ném lỗi thường ở
locale ấy (điều kiện dựng, quy ước chung) — hai đơn vị trong 57, BỎ QUA sẽ tắt cả ca; (e) `_k124_me_chau` giết mẹ và
cháu trước khi ném lỗi điều kiện dựng, và `t161` dọn cả mẹ. Lý do đo được (VERDICT lượt 9, sha256 `0f1b3bdc…ddfa`,
khối r9): launcher chết `rc=1` ⇒ `t159` ra `TinHieuChotCa` đúng ca, đúng LOẠI (tín dụng giả) và hai con sống vô hạn;
`prctl` vô hiệu ⇒ bốn tiến trình sót; locale ISO-8859-1 ⇒ `t158` QUA trên launcher NỀN. Đo trên khối r10: bảng 12; trên
khối r11: bảng 13.
Đo (khối r9: bảng 11; khối r10: bảng 12; khối r11 ngay dưới: bảng 13 — 3.11.15 / 3.12.3 / 3.13.12, ma trận trùng từng
ô; ứng viên nháp Q-A.7 dạng latin-1 trừ các hàng ghi "bytes"). Mỗi ô đỏ là `TinHieuChotCa` của đúng ca đích, ghi LOẠI;
không ô nào chết vô can. Mười một hàng đầu và ba hàng r10 trùng từng ô giữa khối r10 (bảng 12) và khối r11 (bảng 13);
các hàng r11 là số của khối r11:

| bản | `t158` | `t159` | `t160` | `t161` |
|---|---|---|---|---|
| nền `89fc4fa`; ứng viên nháp theo r8 (y hệt nhau) | `124 noi doi` (rc=124, con sống, nhịp 74→84) | `qua han khong giet duoc` (rc=10, con sống) | `124 noi doi` ("SIGTERM: cay da sach", cháu sống) | `124 noi doi` ("tien trinh da khong con chay", cháu sống) |
| ứng viên nháp Q-A.7 | QUA | QUA | QUA | QUA |
| M1 — `_khoa_danh_tinh` đọc lại bằng `read_text()` không đối số | QUA | `qua han khong giet duoc` | `124 noi doi` | `124 noi doi` |
| M2 — `_thanh_vien_nhom` như thế | QUA | QUA | `read args` | `124 noi doi` |
| M3 — `_chup_cay` như thế | QUA | QUA | `124 noi doi` | `khong giet duoc` |
| M4 — khối đọc nhánh tệp có của `_con_song` như thế | QUA | QUA | `124 noi doi` | `124 noi doi` |
| M5 — khối đọc đường mới của `_con_song` như thế | QUA | QUA | QUA | QUA |
| M12 — M1 cùng M2 (hai vị trí) | `124 noi doi` | `qua han khong giet duoc` | `124 noi doi` | `124 noi doi` |
| `errors="surrogateescape"` ở `_khoa_danh_tinh` / `_thanh_vien_nhom` / `_chup_cay` (ba bản, mỗi bản một chỗ) | QUA | QUA | `read args` | `read args` |
| `g_to_hop_dinh_dang_khoa` (r10; r11: cả hai dạng) — dạng bytes: bỏ giải mã trường số ở `_khoa_danh_tinh` VÀ `_chup_cay` (khoá `linux:b'…'`); dạng latin-1: `!r` ở cả hai chỗ (khoá `linux:'…'`); với khối r9 cả bốn ô QUA | QUA | QUA | `khong giet duoc` (khoá KHÁC) | QUA |
| (r10, đối chiếu tổ hợp; r11: cả hai dạng) chỉ `_khoa_danh_tinh` lệch định dạng | QUA | QUA | `khong giet duoc` (khoá KHÁC) | `124 noi doi` |
| (r10, đối chiếu tổ hợp; r11: cả hai dạng) chỉ `_chup_cay` lệch định dạng | QUA | QUA | `124 noi doi` | `124 noi doi` |
| (r11) `s_khoa_tach_ngoac_dau` — `_khoa_danh_tinh` tách theo `)` ĐẦU (latin-1 `index(")")`; bytes `index(b")")` hay `partition(b") ")`; ba bản); cùng ô: tách cả dòng theo khoảng trắng (rig); với khối r10 cả bốn ô QUA (lượt 10) | QUA | QUA | `124 noi doi` | `124 noi doi` |
| (r11) `s_nhom_tach_ngoac_dau` — như thế ở `_thanh_vien_nhom` (ba bản + khoảng trắng); khối r10: QUA ×4 | QUA | QUA | QUA | `124 noi doi` |
| (r11) `s_chup_tach_ngoac_dau` — như thế ở `_chup_cay` (ba bản + khoảng trắng); khối r10: QUA ×4 | QUA | QUA | `124 noi doi` | `khong giet duoc` |
| (r11) `g_khoa_open` / `g_nhom_open` / `g_chup_open` — lời đọc qua `open()`, `io.open(…, "rb")`, `Path.open()`, giữ cách giải mã (mười bản, mỗi bản một chỗ); cùng ô: `/proc/<pid>/task/…` (`TASK_khoa`), `dir_fd` (`DIRFD_khoa`), tiến trình con (`CAT_khoa`); khối r10: QUA ×4; khối HINT: bảng 13 | QUA | QUA | `read args` (open ngoài lời đọc đã ghi) | `read args` (open ngoài lời đọc đã ghi) |
| (r11) `g_d0_open` — khối đọc nhánh tệp có của `_con_song` qua `open()` (còn chết ở helper: `t156` `B2-nhanh-cu song read count 0`) | QUA | QUA | `read args` (open ngoài lời đọc đã ghi) | `read args` (open ngoài lời đọc đã ghi) |
| (r11) `g_d_open` — khối đọc đường mới qua `open()`: B8 không chạm, như M5; chết ở helper `t156` `B2-eacces read count 0` | QUA | QUA | QUA | QUA |
| (r11, rig) `//proc/<pid>/stat` ở `_khoa_danh_tinh` (`SL2_khoa`) — thước đo `open` không tính đường tuyệt đối ngoài `/proc/`; chốt tĩnh ĐỎ | — | — | QUA | QUA |
| (r11, rig) dạng bytes, so `Z` bằng literal str ở `_thanh_vien_nhom` (`ZB_nhom`) — zombie của chính ca còn trong nhóm | `qua han khong giet duoc` | `qua han khong giet duoc` | `khong giet duoc` | QUA |
| (r11, rig) như thế ở `_chup_cay` (`ZB_chup`) — vô hại cho kết cục: zombie trong ảnh chụp bị `_con_song_dung_khoa` loại; chốt tĩnh ĐỎ | QUA | QUA | QUA | QUA |
| (r11, rig, khung ca) launcher bỏ sót MẸ khi ảnh có hậu duệ (`MEBO`) | QUA | QUA | `124 noi doi` (mẹ sống) | QUA |

M5 không chạm B8 (đường mới chỉ chạy khi `stat` lỗi): nó chết ở `t156_...` `B2-eacces read args` (A1 và W1). M4 chết
thêm ở `t156_...` (`read args`; A1 `B2-dem-lan`, W1 `B2-nhanh-cu song`). Với helper KHÔNG có `read args` (lượt 8) M4
chết ở `B2-nhanh-cu utf8-hong-that result False` và M5 ở `B2-dem-doc 4 kill count 1` và `B3-zombie result True`.
**`t158` KHÔNG bị đột biến ĐƠN nào giết**: `_giet_cay` chỉ kết luận "tien trinh da khong con chay" khi khoá danh tính
VÀ quét nhóm cùng mù, nên ca này khoá một TỔ HỢP; M12 là tổ hợp tối thiểu và chết ở cả bốn ca. M12 là đột biến HAI
vị trí — trái quy tắc "một vị trí" của B5 và (E) — và được MIỄN, có lý do: mỗi vị trí của nó đã có biến thể đơn giết
riêng (M1 ở `t159`; M2 ở `t160` `read args` và `t161`), nên không có câu hỏi "vị trí nào bị giết"; M12 chỉ đo đúng
điều `t158` sinh ra để đo — phản chứng đầu-cuối của sự cố chủ kho quyết sửa.
**Chỗ đặt M1–M5, M12 và `g_to_hop_dinh_dang_khoa` (r11: cùng chỗ cho ba `s_*_tach_ngoac_dau` và năm `g_*_open`):
phép (E)** (B5 (E) mục 1 và 6), KHÔNG vào `DOT_BIEN` — cân bằng
r7–r8 giữ nguyên (B4); răng BỀN của bốn ca B8 vì vậy: KHÔNG CÓ (như các hạng mục (E)). `g_to_hop_dinh_dang_khoa` là tổ
hợp hai vị trí, MIỄN như M12 và cùng lý do: mỗi vị trí đơn lẻ đã có ca giết riêng (hai hàng đối chiếu ở bảng trên). Với
biến thể (E) mà đích là một ca B8, chỉ A1 áp dụng (gọi thẳng hàm ca trên bản sao đột biến; không có helper, không có
nhãn để nới): chết bằng `TinHieuChotCa` của đúng ca, thông điệp mở đầu bằng đúng tên đầu vào, đúng LOẠI như bảng trên.
Đưa các biến thể ấy vào `DOT_BIEN` là câu hỏi §11.3 — ba phương án và giá của từng cái ở B4; chọn phương án nào khác
hiện trạng cũng ⇒ revision mới.
Write set ĐỦ (bốn chỗ đọc và mọi nơi gọi ở `launcher.py`; ca, helper, đột biến ở `launcher_test.py`); ba chỗ cùng khuôn
ngoài write set: nợ ở §5.

Mã test đã đo (MÃ TEST THUẦN — executor tự dẫn xuất lại, tự đo; `DANG_DOC_QA7` phải là dạng ứng viên của executor
khai). Nguồn: khối r9 (233 dòng, sha256 `b60434e9…aeeb`) cộng nhóm `khoa-dinh-dang-khong-co-chot` và nhóm
`b8-khung-ca-thieu-chot` của HINT lượt 9 (khối bản gộp HINT: 279 dòng, sha256 `225a10ce…5868`), cộng ba sửa của r10: con
có hạn sống 1200 nhịp, `_k124_don_con` chờ tệp PID, chú thích đầu khối ghi r10 (khối r10: 281 dòng, sha256
`893b31ce…8366`); (r11) cộng nhóm `ma-tran-loi-thieu-chot` và nhóm `b8-khung-ca-thieu-chot` của HINT lượt 10 (khối
bản gộp HINT: 315 dòng, sha256 `b929f2b1…091a` — phiên soạn r11 trích lại từ bản chỉ-HINT, khớp), rồi ba sửa của r11:
thước đo `open` thành danh sách cho phép (mọi `open` trên `/proc/…`, đường tương đối, fd số phải nằm trong một lời đọc
đã ghi), dấu tự thoát của con và cháu thay hai chốt thời gian của HINT, mẹ của `t160` đọc bằng mã thoát. Khối dưới:
**351 dòng, sha256 `950b880a90b014b0646484282858272ae8888a966f331940a5f0831227ca7bad`, 0 dấu chéo ngược** — dựng bằng
tập lệnh thay thế có neo (mỗi neo đúng một lần) từ khối bản gộp, trích bằng máy từ CHÍNH tệp r11 và `cmp` trùng khối
đã chạy ở rig r11 (bảng 13, ba Python).

```python
# ---------------------------------------------------------------------------------------------
# B8 — ca khoá lớp `sua-124-trong-packet` (MÃ TEST THUẦN của đặc tả r11; executor tự dẫn xuất lại,
# tự đo). Bất biến: "124 ⇔ cả cây ĐÃ CHẾT" và "stop rc=0 ⇔ cây đã sạch" không phụ thuộc cách giải
# mã `comm`. Kích hoạt THẬT: kernel cắt `comm` ở 15 byte, nên tên tiếng Việt thành UTF-8 hỏng.
# ---------------------------------------------------------------------------------------------
_K124_COMM = bytes.fromhex("6b69e1bb836d5f7472615f7469e1ba")   # 'kiểm_tra_tiến_trình'.encode()[:15]
# Cháu của t160/t161 (r11): comm có `) ` (tên thật kiểu `tep (1).sh`) + đuôi UTF-8 hỏng — phủ trục S ở ba hàm ngoài:
# phép tách theo `)` ĐẦU (index/partition/split) lệch trường ở _khoa_danh_tinh, _thanh_vien_nhom, _chup_cay.
_K124_COMM_CHAU = b"tep (1) " + _K124_COMM[8:]                 # 15 byte: 'tep (1) ra_ti' + e1 ba
_NL = chr(10)

# Dạng đọc /proc/<pid>/stat theo Q-A.7 mà ứng viên KHAI (một chỗ, helper t156/t157 và B8 dùng chung):
# (tên phương thức Path, args, kwargs) — ví dụ ("read_bytes", (), {}) nếu chọn đọc bytes.
DANG_DOC_QA7 = ("read_text", (), {"encoding": "latin-1"})


def _k124_song(pid: int) -> bool:
    """Sống THẬT theo /proc đọc BYTES — không giải mã `comm`; zombie = đã chết."""
    try:
        with open(f"/proc/{pid}/stat", "rb") as f:
            nd = f.read()
    except (FileNotFoundError, ProcessLookupError):
        return False
    return nd[nd.rindex(b")") + 2:].split()[0] != b"Z"


def _k124_locale_giai_ma_duoc() -> bool:
    """`read_text()` không đối số giải mã theo mã hoá này; giải mã được 15 byte hỏng thì lỗi 124 KHÔNG tái hiện được."""
    import locale
    try:
        _K124_COMM.decode(locale.getpreferredencoding(False))
    except (UnicodeDecodeError, LookupError):
        return False
    return True


def _k124_don_con(tn):
    """Dọn con B8 bằng PID do CHÍNH con ghi (không tin PID launcher-đang-thử báo), chỉ khi cmdline mang đường nhịp."""
    tp = Path(str(tn) + ".pid")
    _k124_cho_tep(tp, 2.0)
    try:
        pid = int(tp.read_text())
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            cua_ta = str(tn).encode() in f.read()
    except (OSError, ValueError):
        return
    if cua_ta:
        with contextlib.suppress(OSError):
            os.kill(pid, signal.SIGKILL)


_K124_MO = {"cai": False, "bat": False, "trong": 0, "ngoai": []}


def _k124_audit(ev, args):
    """Cửa sổ B8: mọi sự kiện audit `open` trên `/proc/…`, trên đường tương đối (`dir_fd`) hay trên fd số phải nằm
    TRONG một lời đọc Path đã ghi — danh sách cho phép ở tầng API (`open()`, `Path.open()`, `os.open`, đường
    `/proc/<pid>/task/…`, ống của tiến trình con đều là `open` NGOÀI). Đường tuyệt đối ngoài `/proc` không tính: máy
    nạp module mở `.pyc` của codec một cách lười, ngay trong cửa sổ (đo)."""
    if _K124_MO["bat"] and ev == "open" and not _K124_MO["trong"]:
        p = args[0] if isinstance(args[0], int) else os.fsdecode(args[0])
        if isinstance(p, int) or not p.startswith("/") or p.startswith("/proc/"):
            _K124_MO["ngoai"].append(p)


@contextlib.contextmanager
def _k124_ghi_doc():
    """Ghi (phương thức, args, kwargs) của MỌI lời đọc Path trên /proc/<số>/stat trong cửa sổ, và ghi mọi sự kiện
    audit `open` xảy ra NGOÀI các lời đọc ấy: lời đọc Path đã ghi là đường mở tệp DUY NHẤT được phép."""
    if not _K124_MO["cai"]:
        sys.addaudithook(_k124_audit)          # không gỡ được; ngoài cửa sổ hook không làm gì
        _K124_MO["cai"] = True
    ghi = []
    goc = {t: (t in Path.__dict__, getattr(Path, t)) for t in ("read_text", "read_bytes")}

    def boc(ten, g):
        def f(self, *a, **k):
            p = str(self)
            if not (p.startswith("/proc/") and p.endswith("/stat") and p[6:-5].isdigit()):
                return g(self, *a, **k)
            ghi.append((ten, a, k))
            _K124_MO["trong"] += 1
            try:
                return g(self, *a, **k)
            finally:
                _K124_MO["trong"] -= 1
        return f
    for t, (_co, g) in goc.items():
        setattr(Path, t, boc(t, g))
    _K124_MO.update(bat=True, trong=0, ngoai=[])
    try:
        yield ghi
    finally:
        _K124_MO["bat"] = False
        for t, (co, g) in goc.items():
            if co:
                setattr(Path, t, g)
            else:
                delattr(Path, t)


def _k124_ma_con(tep_comm, tep_nhip, cho: float, doi_comm: bool) -> str:
    """Con: ghi PID của chính nó, (tuỳ chọn) chờ `cho` giây rồi đổi comm thành 15 byte hỏng, ghi comm THẬT
    (bytes) ra tệp, rồi ghi nhịp mỗi 0,1 s — tối đa 1200 nhịp (khoảng 120 s) rồi tự thoát: hạn sống. Mọi lối
    thoát KHÔNG do tín hiệu ghi `<tệp nhịp>.tu_thoat` (`han_song` / `ngoai_le`) — ca không phải cha của con."""
    dong = ["import ctypes, os, time",
            f"open({str(tep_nhip) + '.pid'!r}, 'w').write(str(os.getpid()))",
            "ly_do = 'ngoai_le'",
            "try:",
            f"    time.sleep({cho})"]
    if doi_comm:
        dong.append(f"    ctypes.CDLL(None).prctl(15, bytes.fromhex({_K124_COMM.hex()!r}), 0, 0, 0)")
    dong += ["    nd = open('/proc/%d/stat' % os.getpid(), 'rb').read()",
             f"    open({str(tep_comm)!r}, 'wb').write(nd[nd.index(b'(') + 1:nd.rindex(b')')])",
             f"    f = open({str(tep_nhip)!r}, 'a')",
             "    for _ in range(1200):",
             "        f.write('.'); f.flush(); time.sleep(0.1)",
             "    ly_do = 'han_song'",
             "finally:",
             f"    open({str(tep_nhip) + '.tu_thoat'!r}, 'w').write(ly_do)"]
    return _NL.join(dong) + _NL


def _k124_tu_thoat(tep):
    """Dấu TỰ THOÁT mà chính tiến trình ghi ở `finally`: `han_song`, `ngoai_le`; None = không tự thoát (tín hiệu
    giết nó, hay nó còn sống). Tín hiệu mặc định giết tiến trình KHÔNG chạy `finally`, nên dấu phân biệt được hai
    đường mà "đã chết" gộp làm một."""
    try:
        return Path(str(tep) + ".tu_thoat").read_text()
    except FileNotFoundError:
        return None


def _k124_tu_thoat_vo_can(ten, tu):
    if tu not in (None, "han_song"):
        raise RuntimeError(f"dieu kien dung: {ten} tien trinh do ca sinh chet vi {tu} - khong bi giet, khong het han")


def _k124_cho_tep(p, han=10.0):
    het = time.time() + han
    while time.time() < het:
        if p.exists() and p.stat().st_size:
            return True
        time.sleep(0.05)
    return False


def _k124_run(s, lenh):
    """`launcher.py run --deadline-utc` thật (hạn 3 s); trả (rc, sổ run.json dạng --json)."""
    repo = tao_repo(s)
    r = chay("run", "--workspace", str(repo), "--run-root", str(s / "runs"), "--json",
             "--deadline-utc", mai_sau(3), "--", *lenh)
    so = {}
    dong = [d for d in r.stdout.splitlines() if d.startswith("{")]
    if dong:
        so = json.loads(dong[-1])
    if not so.get("pid") or r.returncode not in (MA_QUA_HAN, 125, MA_DANH_TINH):
        raise RuntimeError(f"dieu kien dung: launcher khong ket thuc bang ma han chot 124/125/10 kem so JSON: "
                           f"rc={r.returncode}, stderr={r.stderr[-160:]!r}")
    return r.returncode, so


def _k124_ket_luan(ten, rc, pid, tn):
    """Hai assertion, đúng thứ tự: (1) 124 KHÔNG đi cùng cây còn sống; (2) quá hạn phải GIẾT — con TỰ THOÁT ở hạn
    sống là KHÔNG bị giết (ĐỎ); con chết vì ngoại lệ là lỗi điều kiện dựng (không phải TinHieuChotCa)."""
    n1 = tn.stat().st_size if tn.exists() else 0
    time.sleep(1.0)
    n2 = tn.stat().st_size if tn.exists() else 0
    tu = _k124_tu_thoat(tn)
    _k124_tu_thoat_vo_can(ten, tu)
    song = bool(pid) and _k124_song(pid)
    bang(not (rc == MA_QUA_HAN and (song or n2 != n1)),
         f"{ten} 124 noi doi: rc={rc}, con {pid} song={song}, nhip {n1}->{n2}")
    bang(rc == MA_QUA_HAN and not song and n2 == n1 and tu is None,
         f"{ten} qua han khong giet duoc: rc={rc}, con {pid} song={song}, nhip {n1}->{n2}, tu thoat={tu}")


def _k124_dang_doc(ten, ghi):
    """(3) `read args`: mọi lời đọc /proc/<pid>/stat trong cửa sổ đúng DANG_DOC_QA7, và không `open` nào ngoài chúng."""
    if not ghi:
        raise RuntimeError(f"dieu kien dung: {ten} khong co loi doc /proc/<pid>/stat nao")
    lech = sorted({repr(x) for x in ghi if x != DANG_DOC_QA7})
    if _K124_MO["ngoai"]:                      # mở tệp ngoài lời đọc Path đã ghi: danh sách cho phép đóng ở MỌI API
        lech.insert(0, f"open ngoai loi doc Path: {len(_K124_MO['ngoai'])} su kien, vd {_K124_MO['ngoai'][:2]}")
    bang(not lech, f"{ten} read args {lech[:3]}")


def _k124_khoa_that(pid: int) -> str:
    """Khoá theo ĐỊNH DẠNG NỀN `linux:<starttime>` (trường 22), đọc BYTES độc lập — neo định dạng khoá của Q-A.7."""
    bat, _K124_MO["bat"] = _K124_MO["bat"], False      # lời đọc của CHÍNH ca: không đếm vào `open` của cửa sổ
    try:
        with open(f"/proc/{pid}/stat", "rb") as f:
            nd = f.read()
    finally:
        _K124_MO["bat"] = bat
    return "linux:" + nd[nd.rindex(b")") + 2:].split()[19].decode("ascii")


@ca
def t158_comm_hong_SAU_luc_sinh_qua_han_khong_duoc_124_khi_con_song():
    """`run --deadline-utc`: con đổi comm thành UTF-8 hỏng SAU khi launcher lấy khoá (nền 89fc4fa:
    rc=124, `giet_tron_ven=True`, con vẫn sống)."""
    if platform.system() != "Linux":
        return "bo qua: comm/prctl/proc chi co tren Linux"
    if _k124_locale_giai_ma_duoc():
        return "bo qua: locale hien hanh giai ma duoc 15 byte comm hong - loi 124 khong tai hien duoc o day"
    with San() as s:
        tc, tn = s / "comm.bin", s / "nhip.txt"
        try:
            rc, so = _k124_run(s, [PY, "-c", _k124_ma_con(tc, tn, 0.5, True)])
            pid = so.get("pid")
            if not (_k124_cho_tep(tc, 1) and tc.read_bytes() == _K124_COMM):
                raise RuntimeError("dieu kien dung: con chua doi comm thanh 15 byte hong")
            if not so.get("khoa_danh_tinh"):
                raise RuntimeError("dieu kien dung: comm hong TRUOC luc lay khoa (ca nay can SAU)")
            _k124_ket_luan("B8-sau-sinh", rc, pid, tn)
        finally:
            _k124_don_con(tn)


@ca
def t159_chuong_trinh_ten_tieng_Viet_qua_han_phai_giet_duoc():
    """Tên chương trình tiếng Việt ⇒ comm hỏng NGAY LÚC SINH (kernel cắt 15 byte), không cần prctl
    (nền 89fc4fa: `khoa=None`, rc=10, con vẫn sống)."""
    if platform.system() != "Linux":
        return "bo qua: comm/proc chi co tren Linux"
    if _k124_locale_giai_ma_duoc():
        return "bo qua: locale hien hanh giai ma duoc 15 byte comm hong - loi 124 khong tai hien duoc o day"
    with San() as s:
        ten = s / "kiểm_tra_tiến_trình"
        try:
            os.symlink(PY, ten)
        except (OSError, UnicodeEncodeError) as e:
            raise RuntimeError(f"dieu kien dung: khong tao duoc ten tieng Viet: {e}")
        tc, tn = s / "comm.bin", s / "nhip.txt"
        try:
            rc, so = _k124_run(s, [str(ten), "-c", _k124_ma_con(tc, tn, 0.0, False)])
            pid = so.get("pid")
            if not (_k124_cho_tep(tc, 1) and tc.read_bytes() == _K124_COMM):
                raise RuntimeError("dieu kien dung: comm luc sinh khong phai 15 byte hong")
            _k124_ket_luan("B8-luc-sinh", rc, pid, tn)
        finally:
            _k124_don_con(tn)


_K124_MA_CHAU = _NL.join([
    "import ctypes, os, signal, sys, time",
    "signal.signal(signal.SIGTERM, signal.SIG_IGN)",
    "ly_do = 'ngoai_le'",
    "try:",
    "    ctypes.CDLL(None).prctl(15, bytes.fromhex(sys.argv[2]), 0, 0, 0)",
    "    open(sys.argv[1], 'w').write(str(os.getpid()))",
    "    time.sleep(120)",
    "    ly_do = 'han_song'",
    "finally:",
    "    open(sys.argv[1] + '.tu_thoat', 'w').write(ly_do)"]) + _NL
_K124_MA_ME = _NL.join([
    "import subprocess, sys, time",
    "subprocess.Popen([sys.executable, '-c', sys.argv[5], sys.argv[2], sys.argv[3]],",
    "                 start_new_session=(sys.argv[1] == '1'))",
    "if sys.argv[4] == 'thoat':",
    "    sys.stdin.readline()",
    "    sys.exit(0)",
    "time.sleep(120)"]) + _NL


def _k124_me_chau(s, setsid: bool, me_thoat: bool):
    tp = s / "chau.pid"
    me = subprocess.Popen([PY, "-c", _K124_MA_ME, "1" if setsid else "0", str(tp), _K124_COMM_CHAU.hex(),
                           "thoat" if me_thoat else "o_lai", _K124_MA_CHAU],
                          start_new_session=True, stdin=subprocess.PIPE)
    chau = None
    try:
        if not _k124_cho_tep(tp):
            raise RuntimeError("dieu kien dung: chau chua ghi pid")
        chau = int(tp.read_text())
        with open(f"/proc/{chau}/stat", "rb") as f:
            nd = f.read()
        if nd[nd.index(b"(") + 1:nd.rindex(b")")] != _K124_COMM_CHAU:
            raise RuntimeError("dieu kien dung: comm cua chau chua doi")
    except BaseException:
        if chau:
            with contextlib.suppress(OSError):
                os.kill(chau, signal.SIGKILL)
        with contextlib.suppress(OSError):
            me.kill()
        me.wait()
        raise
    return me, chau


@ca
def t160_giet_cay_chau_setsid_comm_hong_phot_lo_SIGTERM():
    """Cháu `setsid()` (killpg không với tới), comm hỏng, phớt lờ SIGTERM: chỉ ẢNH CHỤP + kiểm
    sống/khoá từng pid giết được nó. Phủ `_chup_cay`, `_con_song` nhánh tệp có, `_khoa_danh_tinh`."""
    if platform.system() != "Linux":
        return "bo qua: setsid/proc chi co tren Linux"
    m = _tai_launcher_thu()
    with San() as s:
        me, chau = _k124_me_chau(s, True, False)
        try:
            with _k124_ghi_doc() as ghi:
                khoa = _k124_khoa_that(me.pid)
                kg = m._giet_cay(me.pid, khoa)
            song = _k124_song(chau)
            me_rc = me.poll()   # mẹ là con TRỰC TIẾP của ca: None = còn sống; < 0 = tín hiệu giết; >= 0 = tự thoát
            tu = _k124_tu_thoat(s / "chau.pid")
            _k124_tu_thoat_vo_can("B8-setsid", tu)
            bang(not (kg.tron_ven and (song or me_rc is None)),
                 f"B8-setsid 124 noi doi: {kg.mo_ta}; chau {chau} song={song}, me rc={me_rc}")
            bang(kg.tron_ven and not song and tu is None and me_rc is not None and me_rc < 0,
                 f"B8-setsid khong giet duoc: tron_ven={kg.tron_ven}, chau song={song}, chau tu thoat={tu}, "
                 f"me rc={me_rc}, {kg.mo_ta}")
            _k124_dang_doc("B8-setsid", ghi)
        finally:
            with contextlib.suppress(OSError):
                os.kill(chau, signal.SIGKILL)
            with contextlib.suppress(OSError):
                me.kill()
            me.wait()


@ca
def t161_giet_cay_me_da_thoat_chau_cung_nhom_comm_hong():
    """Mẹ đã thoát, cháu CÙNG NHÓM comm hỏng còn sống: `_khoa_danh_tinh(me)` = None là ĐÚNG (mẹ đã
    biến mất) và chỉ phép quét nhóm còn thấy cháu. Phủ `_thanh_vien_nhom` (và `_chup_cay` theo nhóm)."""
    if platform.system() != "Linux":
        return "bo qua: nhom tien trinh/proc chi co tren Linux"
    m = _tai_launcher_thu()
    with San() as s:
        me, chau = _k124_me_chau(s, False, True)
        try:
            with _k124_ghi_doc() as ghi:
                khoa = _k124_khoa_that(me.pid)
                me.stdin.write(b"x" + _NL.encode())
                me.stdin.close()
                me.wait(timeout=10)
                kg = m._giet_cay(me.pid, khoa)
            song = _k124_song(chau)
            tu = _k124_tu_thoat(s / "chau.pid")
            _k124_tu_thoat_vo_can("B8-me-thoat", tu)
            bang(not (kg.tron_ven and song), f"B8-me-thoat 124 noi doi: {kg.mo_ta}; chau {chau} song")
            bang(kg.tron_ven and not song and tu is None, f"B8-me-thoat khong giet duoc: tron_ven={kg.tron_ven}, "
                                                          f"chau song={song}, chau tu thoat={tu}, {kg.mo_ta}")
            _k124_dang_doc("B8-me-thoat", ghi)
        finally:
            with contextlib.suppress(OSError):
                os.kill(chau, signal.SIGKILL)
            with contextlib.suppress(OSError):
                me.kill()
            me.wait()
```

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
  tắc này. Lịch sử của con số (bảy mục ở r2 đến năm mươi tư ở r7, cùng các con số HINT lượt 4, lượt 5 đề nghị):
  nguyên văn ở đoạn này của r7 (sha256 `3fc04fe5…5286`) — không chép lại (r8, thu gọn). r7 đến r10 KHÔNG thêm dòng
  nào ngoài năm dòng (m) của HINT lượt 6, dù có 83 hạng mục không có dòng riêng (78 của bảng mở rộng, 5 của trục G):
  dòng Linux-only thứ bảy đã đưa Windows xuống dưới sàn (B4); các hạng mục ấy, và bảy biến thể lớp 124 (M1–M5, M12,
  `g_to_hop_dinh_dang_khoa` — B8), được đo bằng phép (E).

  Mỗi đột biến phải chết **bằng `TinHieuChotCa` của đúng ca đích, đúng nhãn — đúng tiểu nhãn khi dòng của nó
  nêu tiểu nhãn (r4) — và đúng loại assertion khi dòng nêu loại (r6)**, không bằng lỗi vô can
  (bài học *"ĐỘT BIẾN BỊ GIẾT KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO"*). Runner hiện có in tên ca kèm
  kiểu ngoại lệ trong ngoặc khi ngoại lệ KHÔNG phải `TinHieuChotCa`, và vẫn cho `OK giet 1/1` — nên
  KHÔNG dùng riêng rc hay chữ `OK` của runner. Phân hạng bằng cách đọc kiểu ngoại lệ, tên ca và nhãn
  (gọi thẳng hàm ca trên bản đột biến để đọc thông điệp `TinHieuChotCa`; runner chỉ in tên ca) và khai
  **ba hạng**: giết thật / tín dụng giả / sống sót, mỗi mục một dòng. Kèm một đối chứng cố ý vô can (ví
  dụ đột biến gây `NameError`) để chứng minh cách phân hạng không cấp tín dụng giả; r6 thêm đối chứng thứ hai
  cho quy tắc nhận ra ngoại lệ tự nhiên của `B2-parse` (một `ValueError` khác đối số phải chết vô can, bảng 8);
  r7 thêm đối chứng thứ ba (cùng kiểu, cùng đối số, khác nguồn), r8 thêm fp2–fp5, r9 thêm fp6, fp6b và hai phép
  giả gọi lại hàm trợ giúp — danh sách và luật ở `B2-parse` (r9: payload theo dõi, mọi đối chứng vô can theo cấu trúc; đo lượt 8,
  ba Python).
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
     57 đơn vị — 17 nhãn, trong đó tám nhãn tách thành 48 tiểu nhãn (r8; r7: 55 / 46); HINT lượt 6: 41 / 17 / tám / 32; r6: 36 / 16 /
     bảy / 27), và thứ tự xuất hiện lần đầu của từng đơn
     vị trong mỗi ca phải đúng thứ tự cố định ở §7. Danh sách kỳ vọng viết CỨNG trong tập lệnh bằng chứng
     theo §7, KHÔNG lấy từ cấu hình CHẠY/NỚI của chính helper (lấy từ đó thì D đo helper bằng helper).
     Chỉ ghi seam đã chạm hay nhãn được chọn KHÔNG chứng minh assertion có hoạt động.
  4. **Control (D phải đỏ).** Trên bản sao TEST, không đụng mã sản phẩm: (i) lần lượt làm mặc định NỚI
     chứa từng nhãn trong **17 nhãn** ⇒ D đỏ, báo đúng nhãn thiếu; (ii) lần lượt bỏ assertion của từng
     tiểu nhãn trong **48 tiểu nhãn** (r8; r7: 46) của tám nhãn tách được (bỏ MỘT đầu vào, giữ các đầu vào khác của
     cùng nhãn) ⇒ D đỏ, báo đúng tiểu nhãn thiếu. Bản mặc định đúng phải xanh. Kỳ vọng **65 control**
     (17 + 48; r7: 63 = 17 + 46; HINT lượt 6: 49 = 17 + 32; r6: 43 = 16 + 27) cộng hai lần xanh của bản đúng, và ít nhất sáu phép đảo
     thứ tự hai nhãn đều đỏ với tập vẫn đủ: `B1`↔`B2-eacces`, `B2-thoat-parse`↔`B2-exception`,
     `B2-pid-du-phong`↔`B3-song`, `B2-dem-doc`↔`B2-pid-du-phong`, `B2-eperm-hoi`↔`B2-doc-hong` (năm cặp của r6) và
     `B2-pid-du-phong`↔`B2-nhanh-cu` (r7). Đo lượt 8 và bảng 11: 6/6 `missing=[] order=False`, ba Python.
  5. **Chỗ đặt.** D và control của nó nằm ở tập lệnh bằng chứng cục bộ của executor, như phép A/W: D chỉ quan sát
     hai ca của helper; không thêm ca đăng ký, không sửa runner `--dot-bien`, không tăng số mục `DOT_BIEN` sản phẩm.
  6. **Nghĩa vụ nộp và log (r8 thêm phần nộp, cross-review lượt 7).** Nộp kèm handoff chính tập lệnh của D và BẢNG
     control máy đọc được — mỗi dòng: KHOÁ control, thứ bị đổi trên bản sao test (nhãn thêm vào tập NỚI mặc định, hay
     đầu vào bị bỏ), đơn vị thiếu kỳ vọng; cộng danh sách 57 đơn vị viết cứng và sáu cặp đảo thứ tự — dưới dạng TỆP,
     cùng kênh và cùng cách tính sha256 như (E) mục 3; reviewer chạy lại trên đúng SHA ứng viên. (r9) KHOÁ control là
     `nhan:<nhãn>` cho 17 nhãn (thứ tự thực thi ở quy ước chung, cộng `B3b-giet-cay`) và `tieu:<nhãn>/<tiểu nhãn>` cho
     48 tiểu nhãn (bảng tiểu nhãn) — 65 khoá, trích được bằng máy từ chính tệp này (bảng 11). Bảng control có ĐÚNG một
     dòng cho mỗi khoá, và tập lệnh ĐỎ khi thiếu, thừa hay lặp dòng — thiếu một control không phải "control không đỏ",
     nên r8 không bắt được. Control RỖNG (không đổi gì so với bản test) để D xanh, nên rơi đúng vào điều kiện "control
     không đỏ" ở câu cuối mục này (đo ở rig r8 06:35:23Z và bảng 11: bỏ một đơn vị không tồn tại ⇒ D xanh ⇒ control bị
     đánh "không đỏ đúng"). Log: lệnh nguyên văn, giờ UTC, rc, dòng xanh của bản đúng cho từng ca,
     và từng dòng control kèm đơn vị thiếu. **Không nhận A1/A2/W1/W0 là đủ** nếu thiếu D, thiếu tập lệnh hay bảng
     control, nếu bản đúng đỏ, hoặc nếu bất kỳ control nào không đỏ.
  Đã đo: lượt 3 đến phiên soạn r7 — D của r6, VERDICT lượt 6, bảng 9 dòng 3 (không chép lại); phiên soạn r8 — bảng
  10 dòng 3 (65 control đỏ, 6/6 phép đảo). **Phiên soạn r9** (bảng 11; ba Python; helper r9 có `read args`, ứng viên
  nháp Q-A.7; 57 đơn vị viết cứng): bản đúng xanh (`t156` 56 đơn vị, `t157` 1, đúng thứ tự); **65 control đều đỏ**,
  mỗi cái báo đúng đơn vị thiếu; 6/6 phép đảo đỏ với `missing=[]`, `order=False`; control RỖNG bị đánh "không đỏ
  đúng".
  **CHƯA ĐO:** tập lệnh bằng chứng của executor và D trên mã của executor.

  **(E) Săn theo bảng không gian mở rộng — MỘT biến thể cho mỗi hạng mục không có dòng B5, trong tập lệnh bằng
  chứng cục bộ, KHÔNG vào `DOT_BIEN` (r7; r9 thêm trục G và B8).** Vì sao cần: 83 hạng mục (78 của bảng mở rộng, 5 của
  trục G) không có mục `DOT_BIEN` riêng, và không được có (B4: dòng Linux-only thứ bảy đưa Windows xuống dưới sàn).
  Không có (E) thì răng của các hạng mục ấy chỉ là lời văn — đúng loại "danh sách tự liệt kê, cho là hết" mà §9 đếm.
  1. **Đối tượng.** Với mỗi hạng mục không có dòng B5 (bảng không gian mở rộng, cột (iii) ghi "E"; trục G), executor
     dựng MỘT biến thể của CHÍNH ứng viên của mình: một thay đổi ở một vị trí mã, vi phạm hạng mục ấy (chạm thêm hạng
     mục khác thì A1 được báo ở nhãn đứng trước, như một dòng B5 — ví dụ đo được: bản trả `False` cho nội dung đọc
     được ở nhánh cũ chết trước ở `B2-dem-lan`, W1 vẫn chết đúng `B2-nhanh-cu song`). Với trục G, biến thể là M1–M5
     của B8. Cộng 35 dòng khác (r11; r10: 27; r9: 26), tên ở mục 6: mười hai biến thể thêm của trục G (B2, "Trục G";
     r11 thêm năm `g_*_open`, một cho mỗi chỗ đọc, "Trục G × API"); ba biến thể trục S ở ba hàm ngoài (r11, B2 "Trục
     S"); hai tổ hợp —
     M12 và `g_to_hop_dinh_dang_khoa` (miễn "một vị
     trí", B8); hai biến thể lặp có điều kiện ("đọc lại chỉ khi EPERM", "kill lần hai chỉ khi đọc gặp EPERM"); năm bản
     vá sai của cross-review lượt 6 trùng (m1)–(m5); tám đối chứng của luật `B2-parse` (khác đối số; cùng đối số khác
     nguồn; fp2–fp5 của r8; fp6, fp6b của lượt 8 — xem `B2-parse`); một đối chứng của loại (2): (j1) viết bằng lần đọc
     thứ hai sai đối số (`LookupError`), phải VÔ CAN; và hai đối chứng phải SỐNG: `song_K0_tach_rieng` — bản ĐỔI CẤU
     TRÚC khối kill của K0 mà ĐÚNG ngữ nghĩa nền (ứng viên dùng chung một khối kill cho K và K0 thì TÁCH K0 ra; ứng viên
     đã tách thì GỘP lại), chứng tỏ các đầu vào K0 không bắt oan một cấu trúc hợp lệ khác; và `song_ba_errno` — bản danh
     sách trắng ba errno (giới hạn đã khai ở mục 3 của danh sách bất khả thi — phải sống, không thì phép đo đang đo thứ
     khác). Ứng viên tách trạng thái trong một hàm trợ giúp thì cộng hai phép giả gọi lại hàm ấy (mục 6). Trên ứng viên
     nháp bộ này có 89 biến thể ở r7, 95 ở r8, 109 ở r9, 110 ở r10 và 118 ở r11 (tám tên mới của r11 đo ở bảng 13; 110
     tên cũ không chạy lại hết).
     **Tập tên và cấu trúc mã (r10, cross-review lượt 9, lớp `doi-chung-gia-dinh-mot-cau-truc`).** Tập TÊN ở mục 6 cố
     định; cấu trúc mã không thêm, bớt hay đổi tên nào. r10 chọn cách **định nghĩa đối chứng độc lập với cấu trúc**,
     KHÔNG khoá cấu trúc. Lý do: Q-A quy định ngữ nghĩa, không quy định cấu trúc; §7 cho phép cả khối kill dùng chung lẫn
     tách riêng (`B2-nhanh-cu`; bảng mở rộng, "khi khối kill còn dùng chung"); khoá một cấu trúc là thêm một ràng buộc
     không quyết định nào đặt ra, và biến `song_K0_tach_rieng` thành đối chứng SỐNG cho một cấu trúc bị cấm. Rà từng
     tên: (i) mọi tên hạng mục, kể cả `k0_*`, là "một thay đổi ở một vị trí mã vi phạm hạng mục ấy" — không phụ thuộc
     cấu trúc: với khối kill dùng chung, thay đổi ấy chạm cả K và A1 được báo ở nhãn đứng trước (luật chung ở trên; đo
     trên ứng viên dùng chung: bảng 11 dòng 4), với khối đã tách nó chỉ chạm K0 (đo ba biến thể `k0_*` trên ứng viên
     tách: bảng 12); (ii) CHỈ `song_K0_tach_rieng` gắn với cấu trúc, và định nghĩa trên (đổi theo chiều ngược với ứng
     viên) cho một bản KHÁC ứng viên ở mọi cấu trúc, nên không rơi vào "bản giống hệt ứng viên" của mục 3; tên là KHOÁ,
     giữ nguyên dù ứng viên đã tách; (iii) `DS-E-C3` giữ điều kiện "chỉ khi ứng viên tách trạng thái trong hàm trợ
     giúp". Câu r8–r9 "số của executor có thể khác nếu cấu trúc mã khác" bị bỏ vì mâu thuẫn với danh sách ĐÓNG (thiếu
     tên ⇒ ĐỎ). Executor khai ánh xạ biến thể → tên ở mục 6.
  2. **Đo.** Mỗi biến thể có đích ở `t156_...`/`t157_...` chạy A1, A2, W1, W0 như một dòng B5. Biến thể hướng
     thoát/sai/bắt/bọc/đếm/cú pháp/dạng đọc: tiêu chí y hệt tiêu chí của một dòng B5 (A1 chết bằng `TinHieuChotCa`
     đúng đích hoặc ở nhãn đứng trước; W1 đúng nhãn, tiểu nhãn, loại; W0 sống, bộ đếm ≥ 1). Biến thể có đích là ca B8:
     chỉ A1 (B8). Biến thể hướng thay thế: ca ĐỎ ở A1, W1 và cả W0 bằng lỗi vô can (không lọt, và nới nhãn không che
     được); đó là hạng "đỏ vô can theo thiết kế", không tính giết thật. Tám đối chứng của luật `B2-parse`, (j1) và hai
     phép giả gọi lại hàm trợ giúp: đỏ VÔ CAN ở A1, W1 và W0. Hai đối chứng sống: cả hai ca SONG, D xanh, VÀ nhân
     chứng dương của mục 5 đúng — thiếu nhân chứng thì đối chứng sống không phân biệt được với bản RỖNG.
  3. **Chỗ đặt, nộp và log.** Như D: tập lệnh bằng chứng cục bộ, không thêm ca đăng ký, không sửa runner, không tăng
     `DOT_BIEN`. Log: lệnh nguyên văn, giờ UTC, rc, và mỗi biến thể một dòng (tên, tên ở mục 6, đích, A1, A2, W1, W0,
     bộ đếm, chấp nhận hay lý do đỏ). Nộp kèm handoff (i) chính tập lệnh bằng chứng (A/W, D, (E), B8) và (ii) BẢNG
     biến thể máy đọc được — mỗi dòng: tên, tên ở mục 6, các cặp (neo, thay) trên ứng viên, ca / nhãn / tiểu nhãn /
     loại kỳ vọng; reviewer chạy lại chúng trên đúng SHA ứng viên trước khi kết luận. Tập lệnh phải ĐỎ khi: một biến
     thể có neo không xuất hiện ĐÚNG MỘT lần trong ứng viên, hoặc cho ra bản giống hệt ứng viên (đo chốt ở rig r8,
     bảng 10 dòng 6: rc=3, không ghi biến thể); (r9) tập tên ở cột "tên ở mục 6" của bảng KHÁC danh sách ĐÓNG ở mục 6
     — thiếu, thừa hay lặp một tên (lượt 8 đo: trích bằng máy từ lời văn bảng mở rộng r8 ra 50 tên và bỏ sót 7 đứng
     sau " / " cùng 1 mục văn xuôi, tức r8 không gì đỏ khi bảng thiếu hạng mục; r9 thay luật sinh khoá bằng danh sách
     ĐÓNG viết tại chỗ và đặt tên cho mục văn xuôi ấy). **Kênh nộp (r9): TỆP trong một commit (nhánh bằng chứng riêng,
     ngoài write set thi hành) hoặc artifact, KHÔNG dán vào thân comment**; handoff ghi OID commit (hay ID artifact),
     đường dẫn và sha256; reviewer đọc lại tệp từ chính commit hay artifact ấy (`git show <OID>:<đường dẫn>`) rồi mới
     tính sha256. Lý do: thân comment đọc qua MCP bị chuẩn hoá `'` `"` `>` `<` thành thực thể HTML (CLAUDE.md, đo
     22-08-2026); lượt 8 mô phỏng trên ba tập lệnh rig đổi 229 / 162 / 1248 ký tự ⇒ sha256 lệch. Kênh GitHub thật:
     r8–r10 ghi KHÔNG ĐO ĐƯỢC; **(r11) phía đọc ĐO ĐƯỢC** — tệp r1 của chính đặc tả trên nhánh
     `ops/spec-launcher-con-song-esrch` (`3915f46`, có `'` ×2, `"` ×22, `<` ×6, `>` ×6) đọc lại bằng `git fetch` +
     `git show` và bằng REST `contents` đều ra đúng sha256 `ee44238c…37d9` (bảng 13); phía ghi là `git push` một blob
     định danh bằng băm nội dung, phiên soạn không đẩy (chỉ thị điều phối) nên không thử; kênh git cục bộ: bảng 11.
     **Không nhận bằng chứng B5 là đủ** nếu thiếu (E), thiếu
     tập lệnh hay bảng, hoặc có biến thể nào không đúng kỳ vọng.
  4. **Giới hạn khai thẳng (r8 sửa câu "răng BỀN" của r7).** (E) chạy MỘT lần trước merge; nó không nằm trong
     `--dot-bien` nên KHÔNG được đo lại ở các lượt sau. Phép D cũng nằm trong tập lệnh cục bộ và cũng chạy MỘT lần.
     Vậy răng BỀN (đo lại ở mỗi lượt `--dot-bien`) của 83 hạng mục ấy và của bốn ca B8: KHÔNG CÓ. Thứ còn lại sau merge
     chỉ là assertion của các ca — chạy ở mỗi lượt suite, nhưng không phép nào đo lại rằng chúng còn đỏ được với vi
     phạm. Một biến thể cho mỗi hạng mục cũng không chứng minh mọi cách viết vi phạm hạng mục ấy đều bị bắt.
  5. **Nhân chứng dương cho hai đối chứng sống (r8, cross-review lượt 7).** "Hai ca SONG, D xanh" không phân biệt
     được đối chứng thật với bản rỗng, nên mỗi đối chứng kèm MỘT phép đo chứng tỏ nó thật khác ứng viên: bản danh
     sách trắng ba errno ⇒ `_con_song(os.getpid())` với seam `OSError(errno.ENOMEM, …)` ở `Path.stat` phải THOÁT
     `OSError` errno 12 trong khi ứng viên trả `True`; bản ĐỔI CẤU TRÚC K0 ⇒ **số nút gọi `os.kill` (AST) trong thân
     `_con_song` cộng thân mọi hàm mức module của `launcher.py` mà `_con_song` gọi trực tiếp, mỗi hàm tính một lần,
     KHÁC ứng viên** (r10; dạng r8–r9 "HAI lời gọi, ứng viên: một" chỉ đúng cho ứng viên dùng chung). Đã đo: ENOMEM ⇒
     ứng viên `True`, danh sách trắng `OSError errno=12`, bản rỗng `True` (ba Python; reviewer lượt 7, bảng 10 dòng 6);
     phép đếm ⇒ ứng viên dùng chung 1, ứng viên tách 2 (lượt 9; bảng 12).
  6. **(r9) Danh sách tên ĐÓNG của bảng (E)** — mỗi tên đúng MỘT dòng. `DS-E-HANG-MUC`: 78 tên của bảng mở rộng
     (cột (iii), khai triển `<tv>`) cộng 5 của trục G; `DS-E-KHAC`: 35 dòng khác (r11; r10: 27; r9: 26); `DS-E-C3`: chỉ khi ứng viên tách
     trạng thái trong hàm trợ giúp. Tên ở đây là KHOÁ; tên biến thể của executor tự đặt và ánh xạ vào khoá. Dòng đầu
     mỗi nhóm ghi số tên, để tập lệnh tự kiểm số đếm:

```
DS-E-HANG-MUC 83
h_co_bo_doc d0_ok_khongZ_sai d0_ok_Z_sai k0_ok_sai d_ok_khongZ_sai d_ok_Z_sai k_ok_sai
d0_ESRCH_thoat d0_ESRCH_sai d0_EACCES_thoat d0_EIO_thoat d0_EIO_sai d0_EPERM_thoat d0_EPERM_sai
d0_value_thoat d0_value_sai d0_index_thoat d0_index_sai d0_decode_thoat d0_decode_sai
d0_exception_bat d0_exception_boc d0_exception_thaythe d0_tin-hieu_boc d0_tin-hieu_thaythe
k0_ESRCH_thoat k0_ESRCH_sai k0_EPERM_thoat k0_EPERM_sai k0_EIO_thoat k0_EIO_sai
k0_index_bat k0_value_bat k0_decode_bat k0_index_boc k0_value_boc k0_decode_boc
k0_index_thaythe k0_value_thaythe k0_decode_thaythe k0_exception_bat k0_exception_boc k0_exception_thaythe
k0_tin-hieu_bat k0_tin-hieu_boc k0_tin-hieu_thaythe
h_index_boc h_value_boc h_decode_boc h_tin-hieu_boc d_exception_boc d_tin-hieu_boc
k_index_boc k_value_boc k_decode_boc k_exception_boc k_tin-hieu_boc
h_index_thaythe h_value_thaythe h_decode_thaythe h_exception_thaythe h_tin-hieu_thaythe
d_exception_thaythe d_tin-hieu_thaythe
k_index_thaythe k_value_thaythe k_decode_thaythe k_exception_thaythe k_tin-hieu_thaythe
h_thoat_hoi_lai d0_doc_hai_lan d0_them_kill k0_hoi_hai_lan k0_them_doc k0_kill_hai_lan d_hoi_lai_khac_EACCES k_hoi_hai_lan
d0_tach_ngoac_dau
g_khoa g_nhom g_chup g_d0 g_d
DS-E-KHAC 35
d0_giai_ma_long d_giai_ma_long g_khoa_errors g_nhom_errors g_chup_errors d0_giai_ma_lai_utf8 d_giai_ma_lai_utf8
g_khoa_open g_nhom_open g_chup_open g_d0_open g_d_open
s_khoa_tach_ngoac_dau s_nhom_tach_ngoac_dau s_chup_tach_ngoac_dau
g_to_hop_khoa_nhom g_to_hop_dinh_dang_khoa d_doc_lai_khi_EPERM k_kill_lai_khi_doc_EPERM
luot6_m1 luot6_m2 luot6_m3 luot6_m4 luot6_m5
dc_khac_doi_so dc_fp dc_fp2 dc_fp3 dc_fp4 dc_fp5 dc_fp6 dc_fp6b dc_j1_sai_doi_so
song_K0_tach_rieng song_ba_errno
DS-E-C3 2
dc_c3_goi_lai_rong dc_c3_goi_lai_index
```

  Đã đo: r7 và r8 — bảng 9 dòng 6, 7, 11, 12 và bảng 10 dòng 4 (ứng viên nháp theo r7–r8). **r9** (bảng 11, ba
  Python, ứng viên nháp Q-A.7 — KHÔNG phải mã của executor): đủ 109 dòng cộng hai dòng `DS-E-C3`, mỗi dòng đúng kỳ
  vọng; danh sách mục 6 trích lại được bằng máy từ chính tệp này, và tập lệnh so tập tên ĐỎ khi thiếu, thừa hay lặp.
  **r10** (bảng 12, ba Python): tên mới `g_to_hop_dinh_dang_khoa` chết đúng `t160` `khong giet duoc`; ứng viên tách K0
  (chiều gộp của nó chính là ứng viên dùng chung) SONG ở `t156`, `t157` và QUA bốn ca B8; ba biến thể `k0_*` trên hai
  cấu trúc; danh sách mục 6 trích lại bằng máy từ tệp r10: 83 + 27 + 2 = 112 tên, 0 trùng. 109 tên còn lại không
  chạy lại ở r10 (số của r9). **r11** (bảng 13, ba Python, khối B8 r11): tám tên mới — `s_*_tach_ngoac_dau` (chín bản
  `SX*`, latin-1 và bytes) chết đúng ca B8 và đúng LOẠI của hàng bảng B8; `g_khoa_open`, `g_nhom_open`, `g_chup_open`
  (mười bản `OPEN*`/`PATHOPEN`) và `g_d0_open` chết `read args` (open ngoài lời đọc đã ghi) ở `t160`, `t161`,
  `g_d0_open` còn chết ở `t156` `B2-nhanh-cu song read count 0`; `g_d_open` chết ở `t156` `B2-eacces read count 0`
  (B8 không chạm); `g_to_hop_dinh_dang_khoa` ở cả hai dạng chết `t160` `khong giet duoc` (khoá KHÁC); danh sách mục 6
  trích lại bằng máy từ tệp r11: 83 + 35 + 2 = 120 tên, 0 trùng, số đếm khớp dòng đầu nhóm. Các tên cũ có đích B8
  (M1–M5, M12) chạy lại trên khối r11: trùng bảng 12; tên cũ khác không chạy lại. **CHƯA ĐO:** (E) trên mã của executor.

  **Log mỗi dòng biến thể**: tên mục và vị trí, ca đích, nhãn đích và tiểu nhãn (nếu có), loại assertion
  (nếu dòng nêu; r6), A1 (nhãn, tiểu nhãn và loại báo), A2 (sống sót hoặc nhãn Y — đây là "các nhãn khác vẫn giết nó trong ca đầy đủ"; danh
  sách ĐỦ mọi nhãn giết được nó cần nới tuần tự và không bắt buộc), W1, W0 kèm bộ đếm seam.
  Cách làm là khả thi, không phải lời hứa: năm mươi tư dòng (năm mươi lăm cặp) đã được chấp nhận trên bản nháp Q-A
  (KHÔNG phải ứng viên của executor) ở rig reviewer lượt 2 đến lượt 6 và rig phiên soạn r7 (bảng 9 dòng 2, 4, 9;
  runner thật 53 dòng `giet 1/1`, (c) `giet 2/2`), r8 (bảng 10 dòng 2), r9 (bảng 11 dòng 3); chi tiết từng rig: đoạn
  này của r9 (sha256 `1a629c89…a3cf`). r10 không chạy lại. **Chưa có:** năm mươi tư dòng chạy trên ứng viên của
  executor.
- **B6 (cả write set) — delta và bằng chứng cục bộ thay CI.** **Phiên bản Python GHIM (r10, cross-review lượt 9,
  lớp `bang-chung-khong-ghim-python-san`): mọi lệnh dưới đây chạy HAI lần, bằng `python3.11` (bản của job Ubuntu
  `launcher-windows.yml` hậu-merge, `:64`) và bằng `python3.12` (bản của `ci.yml`); KHÔNG gọi `python` trần**
  (container soạn r10: `python` là 3.11.15 — một sự tình cờ của máy, không phải hợp đồng). Bằng chứng thay CI không
  được hẹp hơn CI nó thay. 3.13 (Windows) chỉ đo sau merge (Q4).
  `python3.1x .claude/dev/launcher_test.py` toàn suite **delta = 0 ca đỏ** so với nền, ở TỪNG bản Python, đo **cả hai
  vế trong một lệnh** trên cùng rig (bài học "PHÉP ĐO DELTA SO HAI VẾ": nền và ứng viên cùng dựng bằng một vòng lặp,
  cùng bước). Số trên bản nháp (không thay phép đo của executor): rig r9, 3.12.3, nền `89fc4fa` — bảng 11 dòng 8; rig
  r10, nền `423b4ba`, 3.11 và 3.12 — bảng 12; rig r11, cùng nền, khối B8 r11 — bảng 13 dòng 13. `python3.1x .claude/dev/launcher_test.py --dot-bien`: không đột biến cũ
  nào đổi hạng. `ruff check --select F --target-version py311 .claude/dev/launcher.py .claude/dev/launcher_test.py`
  (nhị phân `ruff`; `python -m ruff` vắng trong container này): delta F = 0 (ruff vắng thì ghi `KHÔNG ĐO ĐƯỢC`, không
  ghi 0). Nền trên `423b4ba` (10:47:54Z 30-09, ruff 0.15.8), có và không có `--target-version py311` như nhau:
  `launcher.py` 0 lỗi F; `launcher_test.py` 5 lỗi F, cả năm F841 (dòng 2566, 3387, 3629, 4110, 6062; trên `89fc4fa`
  dòng cuối là 6061). "delta = 0" nghĩa là ứng viên KHÔNG hơn số nền ấy, đo lại trên nền tiếp nối. Lý do ghim đo
  được (VERDICT lượt 9; đo lại ở bảng 12): một bản dạng bytes dùng f-string lồng CÙNG loại dấu nháy (cú pháp PEP 701,
  chỉ hợp lệ từ 3.12) qua suite 3.12 như ứng viên đúng, trong khi `python3.11 launcher.py --help` ⇒ rc=1
  `SyntaxError`; ruff mặc định (kho không có cấu hình ruff) báo `All checks passed!`, chỉ `--target-version py311` bắt.
  **Nghĩa vụ bằng chứng.** Mọi lệnh B1–B6 và B8 chạy **cục bộ trên Linux, đúng SHA ứng viên** (ghi
  `git rev-parse HEAD` cùng log), ở từng bản `python3.11` và `python3.12`, mỗi bản một log. Log mỗi lệnh gồm: lệnh
  **nguyên văn**, giờ UTC bắt đầu, `python3.1x --version`, rc, và
  **dòng tổng nguyên văn** của runner (số qua / chạy / bỏ qua / đỏ; với `--dot-bien` là dòng tổng và
  ba hạng của B5). Log của B5 còn kèm **từng dòng biến thể** với bốn phép đo A1/A2/W1/W0 như đã định
  ở B5 (kỳ vọng năm mươi tư dòng, cũng là năm mươi tư mục `DOT_BIEN`, năm mươi lăm cặp đích), và **log của phép
  D**: lệnh nguyên văn, giờ UTC, rc, dòng xanh của bản đúng cho từng ca đăng ký, và từng dòng trong 65 control (r8; r7: 63)
  (17 mức nhãn, 48 mức tiểu nhãn) cùng các phép đảo thứ tự, kèm đơn vị thiếu; và **log của phép (E)** (B5): mỗi biến
  thể một dòng, kèm ánh xạ sang tên ở (E) mục 6; **log của bốn ca B8** trên ứng viên và A1 của mười bốn biến thể lớp
  124 (M1–M5, M12, `g_to_hop_dinh_dang_khoa`; r10 — cộng ba `s_*_tach_ngoac_dau`, ba `g_*_open` của ba hàm ngoài và
  `g_d0_open`, r11); **đầu ra của chốt tĩnh phần còn lại** (B2, r11) chạy bằng `python3.11` trên SHA ứng viên;
  và phép tính sàn Windows của B4 (lệnh + số). Đính vào handoff; reviewer đọc **trước** merge. Xanh của `gate-registry` KHÔNG thay
  cho log này (§8). Sau merge, `launcher-windows.yml` chạy ở lượt `push` master: đọc kết quả cả
  Windows lẫn Ubuntu (`land_obligation`), kể cả dòng `DOT BIEN:` của bước `Tu dot bien`, đừng suy thành công từ
  việc đã đẩy.
  **ĐỎ khi:** ứng viên có thêm ca đỏ, đột biến cũ đổi hạng, thêm lỗi F, handoff thiếu log nguyên văn cho
  bất kỳ lệnh nào trong B1–B6 và B8 (ở TỪNG bản Python 3.11 và 3.12; r10), hoặc thiếu log phép D, bản đúng không xanh
  ở D, hay có control của D không
  đỏ; hoặc thiếu log phép (E), hay có biến thể (E) không đúng kỳ vọng; hoặc (r8) thiếu tập lệnh bằng
  chứng, bảng biến thể của (E) hay bảng control của D kèm sha256 (B5 (E) mục 3, D mục 6), thiếu nhân chứng dương
  của hai đối chứng sống ((E) mục 5), hay reviewer chạy lại chúng ra kết quả khác log; hoặc (r9) tập tên của bảng
  (E) khác danh sách ĐÓNG ở (E) mục 6, bảng control của D thiếu, thừa hay lặp khoá (D mục 6), tệp nộp không đọc lại
  được từ commit hay artifact đã khai hoặc sha256 không khớp bytes đọc lại, hay bất kỳ ca B8 nào không QUA trên ứng
  viên; hoặc (r10) handoff thiếu kết quả `git grep -n 'linux:' .claude/dev/launcher.py` trên SHA ứng viên, hay kết quả
  ấy có chỗ dựng khoá ngoài hai chỗ của Q-A.7 mà handoff không khai; hoặc (r11) handoff thiếu đầu ra của chốt tĩnh
  phần còn lại, hay chốt ấy ĐỎ trên ứng viên. Sau merge: `DUOI SAN` ở bước `Tu dot bien` của lượt push master là ĐỎ của packet (B4).
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

- **(r11) Nền GIỮ `423b4ba`** — đầu `origin/master` trôi sang `fc852ff` (15:31:19Z 30-09), write set và `.claude`,
  `.github` không đổi byte nào (ô nền nghiệm thu; bảng 13 dòng 17); mọi số nền dưới đây vẫn là số của `423b4ba`.
  Đo thêm bằng REST (bảng 13 dòng 16): lượt `push` master của `423b4ba` (run `36696528580`) ĐỎ ở `gate-registry
  (ubuntu-latest)` vì `ops/nhanh_don_duoc_test.py` rc=-9 sau 4500,384 s — ngoài write set, đỏ sẵn trên nền (ô
  `required_checks`).

- **(r10) Nền nghiệm thu DỜI sang `423b4ba`** (worktree của phiên soạn, HEAD `468c88e`, sạch trừ tệp r10 mới):
  `git fetch -q origin master` rc=0 (10:45:10Z 30-09, xong 10:45:11Z); `git rev-parse origin/master` ⇒
  `423b4ba14078701859b9e6ac101a68a3fc4ddef4` (Merge PR #696, commit lúc 2026-09-30T16:30:11+07:00), trùng `git ls-remote
  origin refs/heads/master`; `git rev-list --count c16bec6..origin/master` ⇒ 44. `git diff --quiet
  89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒
  **rc=1**: một hunk ở `t152` (ô nền nghiệm thu). `-- .claude .github` ⇒ rc=1, 4 tệp (`ci_dang_ky_test.py`,
  `launcher_test.py`, `.claude/hooks/session-start.sh`, `.github/workflows/ci.yml`; 278 dòng thêm, 10 xoá);
  `launcher-windows.yml` không đổi (`git diff --quiet` rc=0). `89fc4fa..423b4ba`: 91 commit (76 không merge), 61 tệp,
  15 426 dòng thêm, 54 xoá (11:01:04Z). Blob trên `423b4ba`: `launcher.py` `561ff7a1…` (không đổi, 4308 dòng),
  `launcher_test.py` `3f02fb94…` (8355 dòng). `468c88e` chưa là tổ tiên của `origin/master` (rc=1). **Phép so hai
  nguồn ref (r10, trên clone sạch trong rig r10, 10:46:50Z):** `git ls-remote --heads origin` và `git for-each-ref
  refs/remotes/origin` (bỏ `HEAD`) cùng 457 tên, `comm` hai chiều rỗng, `--is-shallow-repository` false. Lượt đo nền
  r3 đến r9 (nền `89fc4fa`, `c16bec6`): §8 của r9 — không chép lại.
- **Độ dài `_con_song` trên nền** (r7, AST `end_lineno` trên bản sao `launcher.py` của `89fc4fa` trong rig r7,
  02:00:46Z 30-09, Python 3.12.3): dòng 629–672, **44 dòng** (kể cả docstring). Khớp số cross-review lượt 6 đo; §9
  của r6 ghi nhầm "77 dòng (629–705)".

- Kích thước (`git show <ref>:<tệp> | wc -l`, r10): trên `423b4ba` — `launcher.py` 4308 dòng (blob `561ff7a1…`, sha256
  `808ce5b3…9fc0`), `launcher_test.py` 8355 dòng (blob `3f02fb94…`, sha256 `882ac43f…97cc`); trên `89fc4fa` —
  `launcher_test.py` 8354 dòng (blob `abf7f6ca…`, sha256 `433af9d4…556a`). Lượt đo kích thước r3–r9: §8 của r9.
- **Số ca của `launcher_test.py`, đếm bằng AST** (hàm mức đỉnh mang decorator `@ca`). r10 trên `423b4ba` (10:47Z 30-09,
  Python 3.12.3) và trên `89fc4fa` (cùng lúc): **189 ca đăng ký = 155 ca tiền tố `t<số>` + 34 ca khác**, hậu tố lớn
  nhất `t155`, 155 hậu tố phân biệt, không hổng trong 1..155 — cả hai nền như nhau (bản vá #696 không thêm ca). Phân
  rã nhóm `r` (`r01`–`r21`, `r345`×5, `r347`×2, `r351`×3, `r348`×2, `r349`×1) và các lượt đếm r3–r9: §8 của r9. **155
  không phải tổng suite**: nó là hậu tố lớn nhất của một nhóm; bản r1 dùng nó làm tổng và sai. Nghiệm thu B6 phải
  đối chiếu số đăng ký, số chạy, số bỏ qua và số đỏ, không suy tổng từ hậu tố. Sau packet này, số đăng ký kỳ vọng
  tăng đúng bằng số ca mới ở §6.2 (**sáu**) — executor đếm lại trên nền tiếp nối và khai.
- `DOT_BIEN` ở `launcher_test.py:7013` trên `423b4ba` (`:7012` trên `89fc4fa`): **174 mục**; `DOT_BIEN_HARNESS` ở
  `:7931` (`:7930`): 3 mục (AST, r10, cả hai nền cùng số). Đây là số mục ĐỘT BIẾN, khác số ca. Số mục mới: xem B5
  (**mười ba** lớp, kỳ vọng **năm mươi tư** mục `DOT_BIEN`); sau packet: bảng sản phẩm 174 + 54 = **228**, cộng 3 mục
  `DOT_BIEN_HARNESS` = **231** mục; số ca đăng ký 189 + 6 = **195** — số kỳ vọng suy ra, chưa đo trên ứng viên của
  executor. r7 đến r10 KHÔNG thêm dòng `DOT_BIEN` nào ngoài lớp (m) (B4, B5); phép (E) và bốn ca B8 không thuộc
  `DOT_BIEN` nên không đổi 228 / 231. Số nhãn 17; 48 tiểu nhãn + 9 đơn vị đơn = 57 đơn vị; D có 65 control (r8 đến
  r10). Các kỳ vọng của r3 đến r7 và của HINT lượt 4 đến lượt 6: §8 của r7, r9.
- **Lease** (r10; `ai-dang-giu` của `ops/lease_publish.py` bản `origin/master`, `python3` = 3.11.15). Lượt thứ nhất
  chạy ở kho chính `/home/user/tra-luat` sau `git fetch --prune` đủ ref và sau khi đưa nhánh `master` cục bộ về
  `origin/master` (tụt 44, fast-forward): **`CHAN [12]`, rc=12** cho cả hai tệp (10:46:23Z) — nhánh cục bộ
  `ops/spec-lease-id-ep-kieu-yaml` của một phiên khác khai upstream không còn trên máy chủ. Phiên soạn r10 KHÔNG sửa
  cấu hình nhánh của phiên khác; thay vào đó đo trên một clone sạch trong rig r10 (`git clone --no-checkout
  --reference`, origin là GitHub, 10:46:50Z; phép so hai nguồn ref 457/457 ở gạch đầu dòng trên):
  `.claude/dev/launcher_test.py` ⇒ rc=0, `NGƯỜI_GIỮ 0: không có` (10:46:54Z; `ci-g5-cong-cu-chia-manh-r1-g1-claude`,
  `-g2-`, `-g3-` đều `HẾT_HẠN`); `.claude/dev/launcher.py` ⇒ rc=0, `NGƯỜI_GIỮ 0` (10:47:06Z). Tệp lease g3 trên
  `86b23c0`: `lease_expires_at_utc: '2026-09-30T09:55:00Z'` (thu hồi bằng rút hạn). Clone sạch chỉ có nhánh cục bộ
  `master`; hai commit chỉ có ở kho chính, không có trên máy chủ (`git log --branches --not --remotes`: `468c88e`,
  `5f7485c`) chỉ chạm `ops/specs/launcher-con-song-esrch-r8.md`, `-r9.md` — không tệp lease nào. Số lease của r3: §8
  của r9.
- **Đường thực thi `launcher_test.py` trong CI** (r10, AST và YAML trên `423b4ba`; các lượt đo r1–r9 trên `89fc4fa`:
  §8 của r9 — cùng kết luận):
  - `ci_dang_ky_test.py`: `MOI` = dict ở `:37–53`, **9 mục**, KHÔNG có `launcher_test.py`; `DA_NOI` = set ở `:69–78`,
    **13 mục**, có `launcher_test.py`. `kiem()` (`:578–612`) chỉ đòi mỗi mục `DA_NOI` có một dòng `run:` nhắc tới nó
    trong workflow — "đã nối", **không** "được `gate-registry` chạy". `chay_moi` (`:962–1037`) mặc định `moi=MOI`;
    `--chay` khai ở `:2176`, nhánh `if ns.chay` ở `:2208` (trên `89fc4fa`: `:2011`, `:2043`). Vậy **`gate-registry`
    chạy 9 bộ, 0 lượt gọi `launcher_test.py`**.
  - `ci.yml`: bảy job (`chuan-bi`, `gate`, `gate-cong-cu`, `gate-cong-cu-gop`, `gate-ops`, `gate-registry`,
    `gate-packet-loop`; hai job `gate-cong-cu*` do #668 thêm), khai `python-version: "3.12"`; không bước `run:` nào
    của job nào nhắc `launcher_test` hay `launcher.py`.
  - `launcher-windows.yml` (không đổi so với `89fc4fa`): `:64` chọn Python 3.13 cho Windows, 3.11 cho Ubuntu; dòng
    nhắc `launcher_test.py` ở `:104` (suite), `:107` (`--dot-bien`), `:206` (probe `t62`). Job `launcher`: PR chỉ chạy
    khi có nhãn `windows`; push master chạm `paths: .claude/dev/**` thì chạy cả Windows lẫn Ubuntu; gọi tay
    `workflow_dispatch` tuỳ `runner_set`. Theo Q4 hai đường đầu không xảy ra trên PR này.
- Suite `launcher_test.py` trên nền: số của r7 đến r9 (nền `89fc4fa`/`c16bec6`, 3.12.3, `187/188 … (tong 189, bo qua
  1, hong 1)`, hỏng duy nhất `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc`, đỏ sẵn): §8 của r9 và bảng 11 dòng 8. r10
  trên `423b4ba` (bảng 12 dòng 12): `python3.11` ⇒ `188/188 … (tong 189, bo qua 1, hong 0)`, rc=0; `python3.12` ⇒
  `187/188 … (tong 189, bo qua 1, hong 1)`, rc=1, hỏng `r351` — **nền khác nhau theo bản Python**, nên delta chỉ so
  trong CÙNG một bản. B6 vẫn bắt executor đo cả hai vế trên nền tiếp nối, ở cả hai bản Python.
- Ruff nền trên `423b4ba` (10:47:54Z 30-09, nhị phân `ruff` 0.15.8; `python -m ruff` vắng), có và không có
  `--target-version py311` như nhau: `launcher.py` 0 lỗi F, `launcher_test.py` 5 lỗi F (F841 ×5). Chi tiết ở B6. Số
  trên `89fc4fa` (r3, r9): cùng 0 / 5.
- Tìm Issue/PR có sẵn cho `ProcessLookupError` / `_con_song` ⇒ 0 kết quả (phép đo của r1; r2 đến r10 KHÔNG đo lại).
  Tìm Issue cho quan sát `comm` không phải UTF-8 (§2): chưa làm.

Mọi con số phải được **đo lại** trước cấp lease và trước land (L5).

## 9. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục một lượt thất bại. Hình dạng đáng canh, ghi để lượt thi
hành không lặp: *"vá một lỗ mà mở lỗ khác trong cùng hàm"* / *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ
ba"* — năm lần trước khi r5 được review; lượt 5 đo lần thứ **sáu**, và r6 là revision đầu tiên ĐỔI CÁCH LÀM thay
vì vá tiếp: liệt kê toàn không gian trước; lượt 6 đo lần thứ **bảy** — chính phép liệt kê của r6 đã bỏ sót nhánh cũ
— và r7 mở rộng phép liệt kê sang MỌI đường; lượt 7 đo lần thứ **tám** — seam thay cả lời gọi; lượt 8 đo lần thứ
**chín** — chính các bản vá r8; lượt 9 đo lần thứ **mười** — chính các bản vá r9; lượt 10 đo lần thứ **mười một**.
Các mục là lịch sử của cùng một lớp, không phải mười một finding độc lập:
1–7. (lượt 0 đến lượt 6) nguyên văn ở §9 của r6 (mục 1–6) và của r7 (mục 7), sha256 `fadad3c7…3c99` và
   `3fc04fe5…5286`. Mỗi lần một dòng: (1) bản RỘNG; (2) bản HẸP r1 mất zombie; (3) ba đường không chốt của r2; (4) ba
   ô tầng đọc của r3 và lời khai "A1 khoá mặc định"; (5) chiều kết quả của PID dự phòng; (6) nhóm phân tích ở tầng
   hỏi; (7) bảng không gian r6 chỉ là tầng của ĐƯỜNG MỚI — r7 chữa bằng không gian từ ĐƯỜNG (30 ô, 129 hạng mục) và
   khai giới hạn cứng: sàn đột biến Windows (B4: biên 42 → 7 → 4).
8. **(lượt 7, mới ở r8 — lần thứ TÁM)** nguyên văn ở §9 mục 8 của r8 (sha256 `2ae6ee04…2aa3`). Tóm tắt: seam thay CẢ
   lời gọi đo mệnh đề bắt, không đo phép đọc, nên tham số giải mã nằm ngoài mọi trục; r8 thêm hai đầu vào nội dung
   thật, điều kiện dựng, loại (2) mở rộng cho seam chỉ-đếm, luật nguồn thêm số lần.
9. **(lượt 8, mới ở r9 — lần thứ CHÍN)** Ba bản vá của r8 cùng ĐÚNG ở chỗ được chỉ và cùng mở một đường chưa ai chỉ:
   (i) loại (2) mở rộng cấp tín dụng giả cho lỗi đối số ((j1) `LookupError`); (ii) luật vị trí `B2-parse` thêm số lần
   vẫn thua một phép giả chạy lại CHÍNH dòng đã khai (fp6b) và một phép giả gọi lại hàm trợ giúp (c3) — lần thứ ba
   của cùng luật; (iii) mệnh đề "`read_text()` không đối số" viết ra để khoá cách đọc của nền đã KHOÁ luôn lỗi 124 mà
   chủ kho quyết sửa. r9 chữa theo lớp và THU HẸP thay vì phình: bỏ hẳn luật vị trí (payload theo dõi, nhận bằng danh
   tính), bỏ hẳn phần mở rộng của loại (2), và đổi trục giải mã từ "giữ như nền" sang danh sách cho phép đóng (Q-A.7)
   khoá bằng `read args` cộng hành vi. Chính r9 cũng có dấu hiệu của hình dạng này: `read args` đặt ngay sau đếm đọc
   che răng hành vi của hai đầu vào nội dung thật (M4, M5 chết sớm ở `read args`), nên r9 thêm hai biến thể "đúng đối
   số, sai hành vi" để hai đầu vào ấy có răng riêng — đo được, không suy (bảng 11).
10. **(lượt 9, mới ở r10 — lần thứ MƯỜI)** Hai bản vá của r9 cùng ĐÚNG ở chỗ được chỉ và cùng mở một đường chưa ai
   chỉ: (i) Q-A.7 mở dạng bytes và KHAI "khoá giữ định dạng" mà không tiêu chí nào đỏ được — mọi phép so khoá dùng
   khoá do CHÍNH ứng viên sinh; (ii) danh sách ĐÓNG của (E) biến câu r8 "số có thể khác nếu cấu trúc khác" và nhân
   chứng viết cho MỘT cấu trúc thành mâu thuẫn. r10 chữa bằng một thước đo ĐỘC LẬP với ứng viên (khoá đọc bytes theo
   định dạng nền) và bằng định nghĩa đối chứng không phụ thuộc cấu trúc, rồi tự rà các đường kế bên: mọi chỗ dựng
   khoá và cả ba tổ hợp lệch, mọi tên gắn cấu trúc trong danh sách đóng, mọi lệnh `python` trần. Cả ba lớp P2 của
   lượt 9 nằm ở HỢP ĐỒNG BẰNG CHỨNG, không ở ngữ nghĩa của `_con_song` (VERDICT lượt 9, HƯỚNG 7: ngữ nghĩa đúng ở mọi
   nơi gọi).
11. **(lượt 10, mới ở r11 — lần thứ MƯỜI MỘT)** r9 mở ba hàm ngoài vào phạm vi, r10 thêm trục định dạng khoá, và
   hai trục còn lại của chính các chỗ đọc ấy — cú pháp phép tách và API đọc — không có ô; bản vá hạn sống của r10 thì
   biến "không giết" thành xanh. Chủ kho chọn áp HINT và lặp tiếp (§11.2). r11 áp HINT rồi TỰ LIỆT KÊ đường vào của
   hai trục ở CẢ năm chỗ đọc trước khi vá, và tìm được bốn đường HINT không phủ, mỗi đường đo được: API ở hai khối đọc
   của `_con_song` (không ô, không tên (E) — thước đo của HINT có bắt `g_d0_open` ở B8 dù HINT chỉ khai ba hàm ngoài,
   đo; `g_d_open` thì B8 không chạm, chỉ helper bắt);
   đường `/proc/<pid>/task/…` mà bộ lọc đường của HINT không thấy; tiến trình con (fd ống) mà bộ lọc bỏ qua vì là fd
   số; và phần còn lại của ba hàm ngoài (phạm vi bắt, số lần đọc, fd mở trước) mà không trục động nào đo. Hai đường đầu đóng bằng động, hai đường sau bằng MỘT chốt tĩnh — ở đó hành vi đúng là hành vi nền nên phép so
   dòng đo đúng lời hứa. Với hạn sống: bốn đường "không bị giết mà trông như đã chết" (con, cháu, mẹ tự thoát; mẹ còn
   sống), mỗi đường một chốt và một đột biến rig. Chính phiên soạn r11 cũng suýt ghi một lời khai rộng hơn phép đo:
   thấy đường `.pyc` trong log của thước đo `open` thì suy ra "bản nháp đầu đỏ oan ứng viên bytes đúng" và viết vào
   đặc tả; phép đối chiếu dựng ngay sau đó cho `cand_b` QUA (bảng 13) — lời khai bị gỡ trước khi đóng băng, bộ lọc giữ
   lại và được ghi đúng là PHÒNG XA, kèm cái giá của nó (`SL2_khoa`).

Mỗi bản vá/đặc tả đều ĐÚNG và CÓ RĂNG ở chỗ nó phủ; lỗ nằm ở đường KHÔNG ai chỉ. Các phép đo chỉ chứng
minh các đường đã thử. Miền kiểm của r11 gồm ESRCH, EACCES, EPERM, EIO, zombie, ngoại lệ ngoài `OSError`
(`Exception` và `BaseException`) ở cả năm tầng hỏi, đọc mới, kill mới, đọc cũ, kill cũ, nhóm phân tích ở cả năm
tầng (tự nhiên ở hai tầng đọc, sentinel ở tầng hỏi và hai tầng kill), số lần hỏi/đọc/kill theo từng đường, cú
pháp phép tách (`)` đầu và khoảng trắng) với `comm` chứa `)` ở cả năm chỗ đọc (r11: thêm ba hàm ngoài), nội dung THẬT có `comm` không phải UTF-8 ở cả hai tầng đọc,
dạng phép đọc ở cả năm chỗ đọc (r9), API đọc ở cả năm chỗ đọc (r11), phần còn lại của ba hàm ngoài bằng phép so dòng với nền (r11), định dạng khoá danh tính ở cả hai chỗ dựng khoá và hai dạng (r10, r11), khung ca B8 không nhận "tự thoát" là "bị giết" (r11), và **kết quả của bước PID dự phòng (sống, đã `wait`, EPERM, EIO) cùng số lần
gọi `kill(pid, 0)`**; bảng không gian mở rộng ở B2 ghi rõ ô, đầu vào và chốt từng hướng. B2 khoá bản RỘNG và các
biến thể tầng đọc, B3/B3b khoá bản HẸP r1, B8 khoá lỗi 124 do giải mã; các lớp còn lại ở B5 và (E) khoá những biến
thể đã liệt kê. **Không coi một danh sách mutant hữu hạn là bằng chứng đã liệt kê hết mọi đường**; executor và
reviewer vẫn phải kiểm các đường mới xuất hiện trong chính cách triển khai được chọn.

**Ngưỡng ba lần đã chạm — câu hỏi đặt cho điều phối/chủ kho, r4 đến r10 KHÔNG tự trả lời.** CLAUDE.md dạy đếm
hình dạng lỗi chứ không chỉ đếm lỗi: cùng một hình dạng lặp từ ba lần trở lên thì câu hỏi đúng là "có nên
làm việc này theo cách này không", không phải "vá thế nào". Đường hiện tại (giữ phép hỏi `exists()` rồi
dựng thêm một đường lỗi có đọc + `kill(pid, 0)`, Q-A.1–4) tự nó sinh ra nhiều đường cần chốt — số dòng biến thể của
B5: bảy ở r2, mười hai ở r3, mười lăm ở r4, mười chín ở r5, bốn mươi chín ở r6, năm mươi tư từ r7 (cộng 89 biến thể
(E) ở r7, 95 ở r8, 109 ở r9, 110 ở r10, 118 ở r11); số đơn vị assertion: 22 ở r4, 26 ở r5, 36 ở r6, 55 ở r7, 57 ở r8 đến r11. Bước nhảy
19 → 49 của r6 là giá của việc liệt kê đủ không gian thay vì vá theo finding; với một hàm dài 44 dòng trên nền
(dòng 629–672, kể cả docstring; §8), nghiệm thu nay cần 134 hạng mục, và sàn đột biến Windows chặn cứng việc đưa
chúng vào `DOT_BIEN` (B4) — nên phần lớn răng (83 hạng mục (E) và bốn ca B8) chỉ đo được MỘT lần. Có thể cân nhắc
một cấu trúc ít đường hơn (ví dụ dùng chính phép đọc làm phép hỏi), nhưng nó đổi hành vi nhánh cũ mà Q-A.3 cấm
đổi, và r4 đến r10 chưa đo phương án nào. Dữ kiện mới: lần thứ chín và thứ mười đều do chính các bản vá của lượt
trước sinh ra; r9 THU HẸP (bỏ hai luật) và r10 thêm một thước đo độc lập thay vì thêm luật; lần thứ mười một nằm ở
ba hàm ngoài mà r9 mở và ở khung ca của r10. Có hỏi lại quyết định gốc hay không là việc của điều phối/chủ kho — lượt
này chủ kho chọn lặp tiếp, kèm điểm dừng (§11.2).

## 10. `chua_do_duoc`

Lịch sử theo từng revision của mục này: §10 của r10 (sha256 `e3ae8741…4bde16`), r9 (sha256 `1a629c89…a3cf`) và r8
(sha256 `2ae6ee04…2aa3`) — không chép lại. Dưới đây là các giới hạn HIỆN HÀNH.

- **Mọi số đo của đặc tả là số trên bản NHÁP của phiên soạn hay reviewer, không phải mã của executor.** CHƯA ĐO trên
  ứng viên của executor: năm mươi tư dòng B5 (năm mươi lăm cặp), 118 dòng (E) (cộng hai dòng `DS-E-C3` nếu áp
  dụng), phép D và 65 control, bốn ca B8, suite hai vế ở `python3.11` và `python3.12`, `--dot-bien`, ruff delta,
  tập lệnh bằng chứng, chốt tĩnh phần còn lại, và tiểu nhãn/loại trong thông điệp giết theo ĐÚNG chuỗi của đặc tả.
  Helper của r6 đến r11 là helper của phiên soạn (r9: chép helper reviewer lượt 8 rồi cài `read args`; r10, r11: chép
  helper r9, sha256 `635d93fa…0494`, r11 tách lại từ tệp thử của rig r10 và dựng lại đúng từng byte), không phải
  của executor; hợp đồng helper ở §7 là lời văn. Mặc định "không
  nới" của helper phải đo riêng bằng D; A1 có chốt phủ giao nhau nên không chứng minh được điều này một mình.
- Số của các rig r5 đến r11 chỉ có trong rig tạm của từng phiên soạn (thư mục `mktemp -d` trong scratchpad, ngoài
  kho) — **KHÔNG tái lập được từ kho**; dựng lại từ đặc tả là đủ. Rig r9: bảng 11. Rig r10: bảng 12. Rig r11: bảng 13
  (bản nháp `launcher.py` chép từ rig cross-review lượt 10, kiểm bằng diff; phiên soạn r11 dựng thêm các bản mới; helper
  chép rig r9 qua rig r10; khối B8 trích từ chính tệp r11). ĐO LẠI ở r11: bốn ca B8 trên các bản của bảng 13, các ca
  chậm của khung ca, helper trên các biến thể `_con_song`, locale, điều kiện dựng hỏng, B4, B6 hai vế ở hai Python,
  ruff, chốt tĩnh. KHÔNG chạy lại ở r10, r11 (số hiện hành là của r9, bảng 11): A/W của 54 dòng B5, phép D và 65
  control, phần lớn 110 tên (E) cũ (r11 chạy lại những tên có đích B8 và các tên `_con_song` của bảng 13),
  `--dot-bien` hai vế.
- **Nhánh Windows và Darwin: không đo** (Q4); lần đo Windows đầu tiên là lượt push master sau merge. **Sàn đột biến
  Windows (B4): số THẬT KHÔNG ĐO ĐƯỢC trước merge**; số hiện hành là ước lượng tĩnh cận dưới của r7 (biên 4), không
  đổi vì `DOT_BIEN` không đổi — suy ra, không đo lại ở r8 đến r10 (phép tính biên bằng `_dot_bien_du_san` của
  `423b4ba` ở B4 là số học trên số đếm, không phải lượt `--dot-bien` trên Windows). Cross-review lượt 3 và lượt 8 mô phỏng Darwin/Windows
  bằng seam (ca trả chuỗi BỎ QUA, không tính là QUA): mô phỏng nhánh, KHÔNG phải hệ điều hành thật, và không thay
  `land_obligation`. Bảng 11 đo ba
  Python ở dòng 1–5; dòng 6–10 chỉ ở 3.12.3 hay không phụ thuộc Python. Bảng 12: số Python ghi ở từng dòng.
- **Kernel thật.** ESRCH thật trên `/proc/<pid>/stat` chỉ thấy một lần ở CI (job `109303373142`); EACCES/EIO/EPERM ở
  `stat` hay phép đọc của PID sống, sentinel ở mọi tầng, nhóm phân tích ở tầng hỏi và kill, ENOENT ở `stat` của PID
  sống, lỗi của `kill(pid, 0)` — tất cả là đầu vào do seam đặt ra. Việc hệ điều hành thật sinh chúng: r10 ghi KHÔNG
  ĐO ĐƯỢC; **r11 đo ở cấu hình của container** (bảng 13): dưới uid 65534, `/proc` gắn `rw,relatime` (không
  `hidepid`), `stat` và đọc `/proc/<pid>/stat` THÀNH CÔNG ở mọi PID (2341–2344, ba Python), `kill(pid, 0)` chỉ ra EPERM
  hay ESRCH, 0 EACCES — tức ở cấu hình này kernel KHÔNG sinh các lỗi ấy; cấu hình khác (`hidepid`, LSM): CHƯA ĐO
  (chưa dựng). Dùng `stat`, phép đọc và `kill` THẬT: `vang-da-wait`, lời gọi đường cũ của `B3-zombie`, hai đầu vào
  nội dung thật và bốn ca B8. Tần suất `comm` không phải UTF-8 ngoài thực tế: KHÔNG ĐO ĐƯỢC.
- **Giải mã.** Hai đầu vào nội dung thật và B8 chỉ đo MỘT dạng `comm` không giải mã được (UTF-8 bị cắt giữa ký tự,
  15 byte); điều kiện dựng đo được ở UTF-8 mode và locale ASCII (bảng 10 dòng 7); locale giải mã được 15 byte ấy
  (ISO-8859-1): ĐO ĐƯỢC bằng `localedef` vào `LOCPATH` riêng (cross-review lượt 9; bảng 12 — r9 ghi KHÔNG ĐO ĐƯỢC là
  sai). **(r11, lớp `khai-khong-do-duoc-ma-do-duoc`, TÁI PHÁT ở hai lời khai của r10 — sửa bằng phép đo của chính
  phiên soạn r11, bảng 13.)** "Không cần root": ĐO ĐƯỢC — `setpriv --reuid 65534 --regid 65534 --clear-groups` chạy
  `localedef -i en_US -f ISO-8859-1` vào thư mục đích 0777 truyền bằng fd đã mở (`/proc/self/fd/7/…`; đọc thẳng đường
  dẫn thì bị chặn vì thư mục cha 0700 — đo, cùng lượt) ⇒ `uid` trong tiến trình 65534, rc=0, tệp thuộc `nobody`; locale
  ấy cho `ISO-8859-1` và giải mã được 15 byte ở ba Python. r10 ghi "KHÔNG ĐO ĐƯỢC" là sai: bị chặn ở ĐƯỜNG DẪN, không ở
  năng lực. Locale giải mã được mà KHÔNG phải ISO-8859-1: ĐO ĐƯỢC — `localedef -i ru_RU -f KOI8-R`, `-f CP1251`, `-f
  ISO-8859-5` đều rc=0; `getpreferredencoding(False)` ra đúng tên ấy và cả ba giải mã được 15 byte ở ba Python; B8
  trong bốn locale giải mã được (ISO-8859-1 dựng bằng uid 65534, KOI8-R, CP1251, ISO-8859-5): `t158`, `t159` BỎ QUA
  có khai, `t160`, `t161` như ISO-8859-1 của bảng 12 dòng 6 (bảng 13). r10 ghi "KHÔNG ĐO ĐƯỢC (không dựng)" là sai:
  chưa dựng không phải không đo được. Đối số giải mã: ĐO ĐƯỢC bằng seam ghi
  đối số (lượt 8; r8 khai "KHÔNG ĐO ĐƯỢC" từ tiền đề sai), khoá bằng `read args` (bảng 11). `cp1252` đo được là không
  bền (lượt 8); bộ giải mã khác không cần đo vì Q-A.7 chỉ nhận hai dạng. `newline`: suy luận, không đo. Ứng viên dạng
  BYTES: bốn ca B8 đo được (lượt 9, bảng 12 và bảng 13, ba Python: QUA ×4); qua helper `t156`/`t157`: helper của phiên
  soạn chỉ seam `read_text`, và r11 ĐO rằng nó không phục vụ dạng bytes — ứng viên bytes đúng chết `B2-eacces read
  count 0` ở ba Python (bảng 13; quy ước "Seam thay CẢ lời gọi" đòi seam đúng phương thức của `DANG_DOC_QA7`); qua
  helper seam `read_bytes`: CHƯA ĐO (chưa dựng). Payload `bytes`: cơ chế đo được (lượt 9, ba Python, cùng bảng phân
  hạng với `str`); qua helper đầy đủ: CHƯA ĐO (chưa dựng). `errors="replace"`/`"surrogateescape"` bị loại vì danh sách đóng, không vì hành vi (lượt 8 đo
  chúng đúng hành vi ở locale tương thích ASCII).
- **Nhận diện lỗi phép tách của `B2-parse` (payload theo dõi).** Giới hạn: ứng viên phải tách trên chính payload bằng
  các phép payload phủ; phép khác (biểu thức chính quy, `partition`, chuẩn hoá trước khi tách) làm (l15)/(l17) chết vô
  can — đỏ ồn ào, không tín dụng giả. Đo (lượt 8 và bảng 11, ba Python): tách hai dòng và tách trong hàm trợ giúp có
  (l15), (l17) chấp nhận; fp…fp6b và hai phép giả gọi lại hàm trợ giúp vô can.
- **Răng của bộ sinh chỉ tới ngữ pháp của nó** (bảng 8). Không phủ: kiểm tra dữ liệu thay bắt ngoại lệ ngoài (l16);
  tên lớp con cụ thể của `OSError`/`Exception`/`BaseException`; errno thứ năm trở đi; `finally`; `else` gắn sai; mở
  rộng khối `try` sang câu lệnh khác — mỗi cái CHƯA ĐO bằng bộ sinh (ngoài ngữ pháp của nó; dựng tay được — r11 dựng
  và đo một: kiểm dữ liệu ở nhánh cũ, mục 8 danh sách bất khả thi ở B2). Nhánh cũ, hỏi/đọc lại có điều kiện, cú pháp phép tách,
  tham số của lời gọi đọc, dạng phép đọc và định dạng khoá nằm ngoài ngữ pháp ấy; r7–r10 phủ bằng bảng không gian mở rộng, trục C, S,
  G, hai đầu vào nội dung thật, `read args`, khoá độc lập `_k124_khoa_that` và B8.
- **Răng của phép (E) chỉ tới MỘT biến thể mỗi hạng mục, và chỉ MỘT lần** (83 hạng mục và bốn ca B8; B4, B5): một
  biến thể mỗi hạng mục không chứng minh mọi cách viết vi phạm đều bị bắt. Răng riêng của `B3-song` và `B3-da-wait`
  (không biến thể nào lấy làm đích): CHƯA ĐO (r11 sửa nhãn — dựng được, chưa dựng). Kênh nộp qua GitHub thật: phía đọc
  ĐO ĐƯỢC ở r11 (byte-exact, hai client — B5 (E) mục 3, bảng 13); phía ghi không thử (phiên soạn không đẩy).
- **Dữ kiện do điều phối cấp — (r11) phần lớn nay ĐỌC ĐƯỢC qua REST** (GET, `Authorization: Bearer` bằng
  `GITHUB_PAT`, mã 200 kèm `X-Github-Request-Id` — tới GitHub thật; 15:39:53Z 30-09; bảng 13). r2–r10 ghi cả nhóm là
  "KHÔNG ĐO ĐƯỢC từ phiên soạn"; đúng với đường MCP (chuẩn hoá thân) và với các lượt REST bị proxy chặn đã ghi trong
  CLAUDE.md, không đúng với phiên này. Đọc được: #686 có `id` = `5628902742` (khớp object ID của descriptor), thân
  3243 byte, sha256 `2af24e288730933f43b8e05e00688815fbe3d2a4974a77797b0b6d4354aed9de`, 12 dấu `"` thô và 0 thực thể
  HTML (REST không chuẩn hoá); comment `5888633201` trên #686 (2026-09-29T10:45:55Z, Q5 — §11 mục 4); `5905670017` trên
  PR #688 (06:42:43Z, chứa nguyên văn *"#688: ngay trong packet này"* kèm giờ 06:42:25Z); `5907480436` (lượt 8,
  08:39:42Z), `5909554178` (lượt 9, 10:40:32Z), `5913959273` (lượt 10, 15:03:40Z) trên PR #688 — PR #688 có 11
  comment, lượt 1 đến lượt 10 cộng comment quyết định. VẪN KHÔNG ĐO ĐƯỢC từ phiên soạn: ô `quy_uoc_review` và quyết
  định chủ kho cho r11 (lời điều phối, không có neo GitHub); họ model tự khai của reviewer lượt 6 đến lượt 10; nội
  dung comment VERDICT so từng byte với tệp VERDICT (không so). Thân Issue sửa được sau khi băm, nên neo vẫn là object
  ID cộng số Issue; băm trên ghi để đối chiếu.
- **Lease và ref:** r10 ĐO (§8): hai nguồn ref 457/457 trên clone sạch, `NGƯỜI_GIỮ 0` cho cả hai tệp write set. Ở kho
  chính cùng lệnh ra `CHAN [12]` vì một nhánh cục bộ của phiên khác (§8); kết quả ở kho chính: KHÔNG ĐO ĐƯỢC mà không
  sửa cấu hình của phiên ấy. Số ấy là của 10:46Z–10:47Z 30-09; r11 KHÔNG đo lại; đo lại lúc cấp lease (Q5 điều kiện
  1, §11 mục 4), và đừng suy "người giữ 0" từ một tập ref chưa so hai nguồn.
- **B7 (`t154`)**: chỉ có số của reviewer lượt 2 đến lượt 4 trên bản nháp; phiên soạn r3 đến r10 không chạy lại.
- **Số kỳ vọng sau packet** (§8, B5): 195 ca đăng ký; 228 mục `DOT_BIEN` sản phẩm, 231 kèm `DOT_BIEN_HARNESS`; 17 nhãn,
  48 tiểu nhãn, 57 đơn vị, 65 control. Rig r9 đếm ra 195 ca (bảng 11 dòng 8) và 17 / 48 / 57 / 65 (dòng 5); `DOT_BIEN`
  của rig r9 giữ 174 + 3 (không thêm dòng; `--dot-bien` 176/176). Rig r10: số ca của suite hai vế ở bảng 12. Không
  phải phép đo trên mã của executor.
- (r10, r11) **Kích thước và băm.** Số dòng và số byte chính xác của một revision không ghi trong chính tệp (ghi vào
  thì số tự đổi); đo bằng `wc -lc` trên tệp đã đóng băng. So sánh: r10 2362 dòng / 270 260 byte; bản chỉ-HINT lượt 10
  2442 / 279 045 (sha256 `6cc5e18e…0ad6`, trùng bản gộp VERDICT lượt 10 khai). Băm: phiên soạn r11 đo `VERDICT.md`,
  `HINT.patch` của lượt 10 và r1 đến r10 bằng `sha256sum` trước khi áp HINT và lại lúc đóng băng, khớp cả mười hai.
- PID con đã `wait` bị hệ điều hành tái dùng giữa lúc `wait` và lúc đo: xác suất KHÔNG ĐO ĐƯỢC. Ở `B2-pid-du-phong`
  `da-wait`, PID bị tái dùng thì `kill(pid, 0)` thật thành công và ca báo `TinHieuChotCa` cho một bản ĐÚNG (dương tính
  giả); chạy lại là cách phân biệt; ca không khoá được khe này. Ở B8, PID của con hay cháu bị tái dùng giữa lúc giết
  và lúc kiểm sống: cùng giới hạn.

## 11. Câu hỏi mở — chủ kho trả lời TRƯỚC khi cấp lease (r8; r9; r10; r11)

1. **ĐÃ TRẢ LỜI (r9).** Chủ kho, 2026-09-30T06:42:25Z (lời điều phối cấp; neo: PR #688 comment `5905670017`, phiên
   agent đăng hộ — phiên soạn r9 KHÔNG kiểm trên GitHub): *"#688: ngay trong packet này"*. Lớp "đọc lỗi ⇒ coi như đã
   chết" do giải mã ở `:359`, `:436`, `:490` và hai khối đọc của `_con_song` được sửa ở packet này: Q-A.7, B8; write
   set không đổi. Ba chỗ cùng khuôn ngoài write set: nợ ở §5. Tần suất ngoài thực tế: KHÔNG ĐO ĐƯỢC.
2. Ngưỡng ba lần của hình dạng "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba" — nay mười một lần (§9): có hỏi lại
   quyết định gốc (cấu trúc của đường lỗi mới) hay không. Câu hỏi đã nêu từ r4; r9, r10 chỉ thêm dữ kiện, không tự trả
   lời. **ĐÃ TRẢ LỜI CHO LƯỢT NÀY (r11).** Chủ kho, 2026-09-30, trả lời trắc nghiệm (lời điều phối cấp, không có neo
   GitHub; phiên soạn r11 không kiểm được), nhãn đã chọn nguyên văn: *"Áp HINT, lặp tiếp (Recommended)"*. Nghĩa, theo
   lời điều phối: r11 = HINT lượt 10 — một hằng `comm` cho trục tách của ba hàm, một thước đo đếm `open` cho trục API
   đọc, thay vì liệt kê API — rồi review lượt 11; **nếu lớp `ma-tran-loi-thieu-chot` tái phát lần thứ mười thì DỪNG
   và thu hẹp**, không vá tiếp. r11 giữ đúng hai thước đo ấy (hằng `_K124_COMM_CHAU`; thước đo `open`, chỉ đổi từ "đếm
   bằng số lời đọc" sang "không `open` nào ngoài lời đọc đã ghi" vì phép đo — bảng 13) và THÊM đúng những gì phép tự
   liệt kê đường vào đòi (B2, bảng "Năm chỗ đọc × hai trục"; chốt tĩnh phần còn lại). Quyết định gốc (cấu trúc đường
   lỗi mới) KHÔNG được hỏi lại ở lượt này.
3. Cân bằng `DOT_BIEN` và phép (E) (B4): r10 và r11 giữ 54 dòng và đo 83 hạng mục cùng bảy biến thể lớp 124 (M1–M5, M12,
   `g_to_hop_dinh_dang_khoa`) bằng (E) MỘT lần — răng BỀN của bốn ca B8: KHÔNG CÓ. (r11: tám tên mới — ba
   `s_*_tach_ngoac_dau`, năm `g_*_open`; bảy có đích B8, `g_d_open` đích helper — cũng chỉ ở (E); số dưới đây CHƯA
   tính chúng, và chọn (b) hay (c) có đưa chúng vào `DOT_BIEN` hay không thì tính lại bằng cùng `_dot_bien_du_san`.
   Chốt tĩnh phần còn lại của r11 là phép kiểm trên ứng viên, không phải dòng `DOT_BIEN`.) Ba phương án, số của B4 (cận dưới
   tĩnh; biên tính bằng `_dot_bien_du_san` của `423b4ba`):
   (a) giữ hiện trạng ⇒ biên 4, không có răng BỀN cho B8;
   (b) đưa M1–M5, M12 vào `DOT_BIEN` như dòng Linux-only ⇒ 71/237 không đo được trên Windows, 70,04 %, **biên 0**;
   thêm `g_to_hop_dinh_dang_khoa` ⇒ `DUOI SAN`. Hạ sàn hay đánh dấu dòng Linux-only ra khỏi mẫu số thì phải sửa
   runner `--dot-bien`, mà đặc tả cấm, và sàn 70 % là luật chung của kho;
   (c) **(r10, cross-review lượt 9, lớp `rang-ben-b8-bo-sot-phuong-an`)** đưa M1–M5, M12 vào `DOT_BIEN` KÈM một ca
   TĨNH chạy mọi nền làm đích phụ (ví dụ AST kiểm năm lời đọc đúng `DANG_DOC_QA7`) ⇒ **biên 6** (reviewer lượt 9 đo
   bằng runner thật, Windows giả lập: 237 mục, 65 không đo được, 72,57 %); thêm `g_to_hop_dinh_dang_khoa` (ca tĩnh
   không bắt được nó) ⇒ biên 5. Được: Linux đo lại hành vi bốn ca B8 ở MỖI lượt `--dot-bien` (răng BỀN). Giá: thêm
   một ca đăng ký (sửa §6 mục 2, §8 số ca và số mục `DOT_BIEN`); trên Windows dòng ấy chỉ đo DẠNG đọc; đo Windows
   THẬT: KHÔNG ĐO ĐƯỢC trước merge.
   r10 KHÔNG chọn. Chủ kho giữ (a) ⇒ lease r10; chọn (b) hay (c) ⇒ revision mới (đổi B4, B5, B8, §6, §8). r11 cũng
   không chọn; giữ (a) ⇒ lease r11.
4. **(r11) Điều kiện cấp lease của Q5 — ĐÃ ĐỌC, không phải câu hỏi mới.** Mission #686 comment `5888633201` (phiên
   agent đăng hộ chủ kho; đăng 2026-09-29T10:45:55Z), r11 đọc qua REST lần đầu (r2 đến r10 không đọc): chủ kho *"Cấp
   lease cho wp 678, wp685 (khi #668 nhả launcher_test.py)"*, kèm ba điều kiện, TẤT CẢ đo lại ngay trước khi cấp:
   (1) `ai-dang-giu` cho `.claude/dev/launcher.py` và `.claude/dev/launcher_test.py` đều `NGƯỜI_GIỮ 0` — r11 KHÔNG đo
   lại; (2) lease neo `spec_hash` của r1 `ee44238c…37d9` "trừ khi đặc tả đổi revision trước đó" — đặc tả đã đổi tới
   r11, nên lease neo băm của r11 (công thức ở đầu tệp); (3) #668 land trước và đổi write set thì nền nghiệm thu phải
   dời bằng revision mới trước khi cấp — r10 đã dời sang `423b4ba`, và r11 đo write set không đổi tới `fc852ff` (ô
   nền nghiệm thu).
