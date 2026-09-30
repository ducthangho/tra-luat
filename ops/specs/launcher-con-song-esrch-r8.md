# ĐẶC TẢ — `LAUNCHER-CON-SONG-ESRCH` — **revision 8, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp685` (ID bền, `wp<issue>`); tên đọc được: `LAUNCHER-CON-SONG-ESRCH`. Lease dùng tên nào cũng phải kèm `packet_issue: 685`. |
| `revision` | **8** |
| `thay_the_cho` | r7 = `ops/specs/launcher-con-song-esrch-r7.md`, sha256 `3fc04fe5e74dad82f023f0ec513cc5e19a8ce5a32a9dd54c1d7a157721265286`, commit `4314eed` (`4314eed15be09f34792205059fc2bae9d8b18b2e`). Trước đó (đường dẫn, sha256 đầy đủ và OID đầy đủ của từng bản: ô `thay_the_cho` của r7): r6 `fadad3c7…3c99` (`82d05eb`), r5 `a0842320…7928` (`1b13110`), r4 `2c84a1bd…ae67` (`673f00c`), r3 `7ef008f8…a895` (`f8ddd49`), r2 `de9c553a…9ce4` (`cdf0575`), r1 `ee44238c…37d9` (`d96d075`). r1 đến r7 giữ nguyên, không sửa đè (phiên soạn r8 đo bảy băm bằng `sha256sum` trước khi áp HINT và đo lại lúc đóng băng — giờ ở §10 — khớp cả bảy; `git status --short` chỉ có tệp r8 mới); r8 là bản duy nhất được cấp lease. |
| `packet_issue` | **#685** |
| `mission_issue` | **#686** (Mission Issue, object ID `5628902742`). Thân #686 khai ngay đầu rằng nó do phiên agent đăng hộ chủ kho bằng credential chủ kho; nguồn thẩm quyền là các câu trả lời của chủ kho được trích trong đó (Q0–Q4 trong thân; Q5 ở comment `5888633201`, xem `nguon_cap_viec`). |
| `nguon_cap_viec` | (r1) Chỉ thị chủ kho 29-09-2026: *"mở packet riêng cho bản vá launcher (race ProcessLookupError) đi"*. Nguồn lỗi: PR #679, job `gate-ops (ubuntu-latest)` `109303373142`, phân tích ở PR #679 comment `5885963131`. (r2) đến (r7) Cross-review lượt 1 đến lượt 6 trên PR #688 — reviewed commit, kết luận, số P1/P2/P3, băm VERDICT và HINT, ID comment, giờ đăng: nguyên văn ở ô `nguon_cap_viec` của r7 (sha256 `3fc04fe5…5286`), không chép lại (r8, thu gọn). (r8) Cross-review lượt 7 trên PR #688, reviewed commit `3915f46011d6ab370246b53cac6573d87fbecba0` (r7 ở `4314eed` cộng merge `origin/master`; spec sha256 khớp băm r7 ở `thay_the_cho`). **Reviewer là Claude Opus 5.5, hạng `advisory_review`, CÙNG HỌ với executor và với phiên soạn — KHÔNG phải `cross_approved`** (protocol §8 đòi khác họ); họ model là tự khai của reviewer, không có phép đo máy. Kết luận `changes_requested`, **0 P1 / 4 P2 / 2 P3**: `ma-tran-loi-thieu-chot` **CÒN MỞ — lần thứ tám** (P2), `b2-parse-nhan-dien-theo-gia-tri` còn mở, vá hẹp (P2), và bốn lớp mới `phep-E-D-chi-la-loi-khai` (P2), `ngoai-pham-vi-doc-loi-thanh-124` (P2), `dac-ta-phinh-rang-buoc-ngam` (P3), `khai-khong-do-duoc-ma-do-duoc` (P3); hai lớp P3 của lượt 6 ĐÃ ĐÓNG. VERDICT sha256 `1a21b8669059b8cce3c313bf82a3f2c7de6cb9023be9851707cba74f5538c1ba` (viết tắt `1a21b866…c1ba`), `HINT.patch` sha256 `761504d7501363af47c3ac620412e9a24c6f6f9e4857b13cf71ccbe55597f872` (viết tắt `761504d7…f872`); phiên soạn r8 đo lại cả hai băm trên hồ sơ lượt 7 (giờ ở §10), khớp. Comment PR #688 `5905120228`, đăng 2026-09-30T06:01:02Z (phiên điều phối đọc qua REST; phiên soạn r8 không kiểm trên GitHub). Mission #686 comment `5888633201` (Q5: điều kiện cấp lease); phiên soạn r2 đến r8 KHÔNG đọc lại nội dung comment này, coi nó là lời khai của điều phối, và không chép điều kiện nào từ nó vào đặc tả. |
| `quy_uoc_review` | **(r8, chủ kho chốt 30-09; dữ kiện do phiên điều phối cấp, phiên soạn r8 không kiểm trên GitHub)** Từ r8, mỗi revision chỉ được commit CỤC BỘ và được review trên CHÍNH commit cục bộ ấy; PR chỉ được đẩy khi review ra **0 P1 / 0 P2 / 0 P3**. Thứ định danh revision là sha256 của tệp cộng OID commit, không phải tên nhánh. |
| `objective` | `_con_song` không bao giờ để một ngoại lệ `OSError` của phép hỏi `/proc/<pid>/stat` thoát ra; tiến trình biến mất giữa chừng (ESRCH) được báo là đã chết; lỗi khác KHÔNG được đọc thành "đã chết" chỉ vì không stat được, và một zombie vẫn được báo là đã chết khi nội dung `/proc/<pid>/stat` còn đọc được. |
| `review_class` | **`sensitive`** — protocol §8: *"launcher hoặc gate lifecycle"*. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | `claude` — **Claude Sonnet 5.5, effort high** (Mission #686 Q3); phiên điều phối kiểm lại độc lập và commit. |
| `environment` | **`cloud`**. Bản vá chỉ chạm nhánh Linux của `_con_song`; nhánh Windows trả về trước dòng 650. |
| reviewer | `codex` (`gpt-6-astra`, effort ≥ medium), cần `cross_approved`. Protocol §8: HINT không được chứa mã launcher; chỉ được chứa mã TEST thuần. (r7) Lượt 6 trên PR #688 — review ĐẶC TẢ, không phải review bản thi hành — do Claude Opus 5.5 làm theo chỉ định của chủ kho, hạng `advisory_review`; (r8) lượt 7 cũng vậy. Hai lượt ấy không thay yêu cầu `cross_approved` khác họ cho PR thi hành. |
| `depends_on` | Lease `ci-g5-cong-cu-chia-manh-r1-g2-claude` (packet #668) giữ `.claude/dev/launcher_test.py`, `lease_expires_at_utc` = `2026-09-30T07:41:00Z` (đọc từ tệp lease trên nhánh `ops/cap-lease-ci-g5-cong-cu-chia-manh`; `ai-dang-giu` báo `CÒN_HẠN`, `NGƯỜI_GIỮ 1`, rc=11, lúc 11:56:57Z 29-09; cùng kết quả ở 11:45:23Z). Đầu nhánh ấy đã đi từ `7c16d11` (r2) sang `2ae5646` (một commit chỉ thêm hồ sơ review #668, 11:26:38Z); tệp lease g2 giữa hai đầu nhánh KHÔNG đổi (`git diff --quiet 7c16d11 2ae5646 -- <tệp lease>` rc=0, 11:49Z). Phải nhả hoặc hết hạn trước khi cấp lease cho `wp685` (Mission #686 Q1). `.claude/dev/launcher.py`: `NGƯỜI_GIỮ 0`, rc=0 (11:56:47Z; cùng kết quả ở 11:45:12Z). Chi tiết phép đo ở §8. **Mọi số lease trong ô này là số đo của phiên soạn r3; phiên soạn r4 đến r8 KHÔNG đo lại chúng (KHÔNG ĐO ĐƯỢC ở r4 đến r8; hạn `2026-09-30T07:41:00Z` của lease #668 là số đọc ở r3, trạng thái hiện hành chưa đo)** — đo lại lúc cấp lease, và không suy "người giữ 0" từ một tập ref chưa so hai nguồn. |
| nền nghiệm thu | `origin/master` `89fc4fac8cea65979cc2483043dc8cd07a6e8518` — **vẫn hợp lệ cho hai tệp trong write set** dù `origin/master` đã tiến nhiều lần từ lúc chọn nền. **Đo lại ở r8 (worktree của phiên soạn, HEAD `3915f46`, sạch trừ tệp r8 mới):** `git -C <worktree> fetch -q origin master` rc=0 (06:14:27Z 30-09, xong 06:14:28Z); `git rev-parse origin/master` ⇒ `c16bec639efa0077def4916c25c3e0c17f68dcaa` (Merge PR #693; **không trôi kể từ r7**: `git rev-list --count c16bec6..origin/master` ⇒ 0); `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=0** (06:14:28Z); cùng lệnh với `-- .claude .github` ⇒ rc=0 (06:14:28Z); `git rev-parse origin/master:<tệp>` ⇒ blob `561ff7a1…`, `abf7f6ca…` (giữ nguyên). Các lượt đo lại ở r3 đến r7 (cùng kết luận rc=0): nguyên văn ở ô này và ở §8 của r7 — không chép lại (r8, thu gọn). Đầu `origin/master` sẽ còn trôi: đo lại lúc cấp lease. Nền tiếp nối (continuation base) sẽ khác khi #668 land trước; khai riêng lúc cấp lease, không thay nền này (protocol §3.2.1). |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/launcher-con-song-esrch-r8.md`, không loại dòng nào. Giá trị được công
bố **ngoài** tệp: comment trên #685 và lease, kèm OID commit + đường dẫn. Khối closure dưới đây
nằm **trong** tệp, nên một `spec_hash` không thể đi với hai closure khác nhau. Đổi bất kỳ byte nào
⇒ revision mới, băm mới, lease mới. Băm của r1 (`ee44238c…37d9`), của r2 (`de9c553a…9ce4`), của r3
(`7ef008f8…a895`), của r4 (`2c84a1bd…ae67`), của r5 (`a0842320…7928`), của r6 (`fadad3c7…3c99`) và của r7
(`3fc04fe5…5286`) KHÔNG còn dùng để cấp lease.

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

**Thay đổi so với r7** (mỗi dòng ứng với một lớp của VERDICT lượt 7, hồ sơ cross-review PR #688; slug là tên
lớp trong bảng lớp của VERDICT; số trong bảng là số hiện hành của r8). r8 áp `HINT.patch` của lượt 7 (6 nhóm
`# lop:`, 36 hunk, 99 227 byte, sha256 `761504d7…f872`) lên bản sao r7. Mỗi nhóm là diff ĐỘC LẬP so với r7 gốc
(VERDICT lượt 7, mục DRY-RUN), nên áp nguyên tệp cho đúng bản gộp. HINT nhắm r7 nên chỉ đổi tên tệp trên các
dòng tiêu đề `---`/`+++` của từng nhóm, không đổi dòng ngữ cảnh nào: `cp` r7 thành r8, rồi `sed -E` với biểu thức
`/^(---|[+]{3}) /s#launcher-con-song-esrch-r7.md#launcher-con-song-esrch-r8.md#` trên `HINT.patch`, đưa qua
`patch -p0 --fuzz=0` từ gốc worktree. (Lệnh chạy lúc soạn viết ba dấu cộng bằng ký tự thoát; dạng ghi ở đây không
dùng ký tự thoát — đo lại trên một bản sao r7 riêng lúc 06:17:54Z 30-09, cùng rc và cùng sha256.) Kết quả (lượt áp
06:01Z 30-09): **rc=0**, sáu lần `patching file`, không tệp `.orig` hay `.rej`, 1869 dòng / 238 466 byte, sha256 bản
chỉ-HINT `680710ad426475abd19150dde7569193f51a6709cc1accc84622ffd6820b3b76` (`680710ad…3b76`) — trùng đúng bản gộp
VERDICT lượt 7 khai; r1 đến r7 nguyên byte; `git status --short` chỉ có tệp r8.

**Vì sao r8 KHÔNG dừng ở HINT.** HINT đóng đúng chỗ reviewer chỉ và có răng ở chỗ nó phủ. Nhưng đo trên một rig có
đủ 89 biến thể (E) của r7 — rig của reviewer lượt 7 không có bộ ấy — ra hai lỗ mà HINT để lại, cùng hình dạng *"vá
đúng chỗ được chỉ rồi bỏ sót đường thứ ba"*: (1) đầu vào THẬT mới `utf8-hong-that` nằm CÙNG nhãn `B2-nhanh-cu` với
đích của hai biến thể (E) `d0_value_thoat`, `d0_decode_thoat`; W0 nới cả nhãn nên chạy cả đầu vào ấy, và
`UnicodeDecodeError` THẬT của nó không thuộc bốn loại ghi nhận ⇒ W0 chết vô can — đúng hiện tượng reviewer đã đo khi
thử đặt đầu vào ở `B2-parse`, nay ở phía Đ0; (2) luật "hàm + nguyên dòng" vẫn cấp tín dụng giả cho một bản SAO Y
nguyên văn dòng tách, trong hay ngoài nhánh xử lý (fp4, fp5). Và phép rà mà lượt 7 đặt ra (seam thay CẢ lời gọi) cho
ra một tham số KHÔNG phân biệt được bằng hành vi ở locale UTF-8, phải khai. Số đo: §1 bảng 10.

| slug lớp | hạng | chỗ sửa trong r8 |
|---|---|---|
| `ma-tran-loi-thieu-chot` | P2 | HINT: Q-A.3 nói "nguyên xi" gồm lời gọi `read_text()` không đối số giải mã; hai đầu vào nội dung THẬT `B2-nhanh-cu utf8-hong-that` (Đ0) và `B2-dem-doc 4` (Đ); hai biến thể (E) `d0_giai_ma_long`, `d_giai_ma_long`. r8 thêm, theo LỚP "seam thay CẢ lời gọi": (1) quy ước chung §7 liệt kê mọi seam, tham số nó che và cách đóng từng cái (giải mã: hai đầu vào thật, đo mười hai biến thể giải mã lỏng chết đúng chỗ; `follow_symlinks`: không đổi kết quả; đường dẫn hay API khác: bộ đếm; `encoding="utf-8"` tường minh: KHÔNG ĐO ĐƯỢC bằng hành vi ở locale UTF-8); (2) điều kiện dựng của hai đầu vào thật: `read_text()` thật phải ném `UnicodeDecodeError` NGOÀI cửa sổ đếm; (3) Q-A.4 nói rõ phép đọc mới cũng là `read_text()` không đối số giải mã; (4) loại ghi nhận (2) mở rộng từ observer `kill` sang seam chỉ-đếm của `stat` và `read_text` — thiếu nó, W0 của `d0_value_thoat`, `d0_decode_thoat` chết vô can (bảng 10 dòng 4). Số hiện hành: 17 nhãn; 48 tiểu nhãn; 57 đơn vị; 65 control; 95 biến thể (E); `DOT_BIEN` giữ 54 dòng, 228 / 231 |
| `b2-parse-nhan-dien-theo-gia-tri` | P2 | HINT: so HÀM + NGUYÊN DÒNG, không so chuỗi con. r8 thêm SỐ LẦN: dòng khớp phải xuất hiện trong tệp nguồn của khung đúng bằng số lần executor khai cho nó trên ứng viên (bảng 10 dòng 5). Rà mọi chỗ dùng luật này: quy ước chung loại (4), định nghĩa "nới nhãn", `B2-parse`, `B2-pid-du-phong` p1–p3, `B2-nhanh-cu` p1 và p3, B5 (đối chứng thứ tư đến thứ bảy), §10 |
| `phep-E-D-chi-la-loi-khai` | P2 | (E) và D nộp kèm handoff TẬP LỆNH và BẢNG máy đọc (biến thể của (E); control của D) kèm sha256; tập lệnh thoát khác 0 khi neo không xuất hiện đúng một lần hoặc biến thể trùng ứng viên; nhân chứng dương cho hai đối chứng sống, phân biệt được bản RỖNG (bảng 10 dòng 6); câu "răng BỀN" sửa ở B5 (E) mục 4 và ở `B2-nhanh-cu` |
| `ngoai-pham-vi-doc-loi-thanh-124` | P2 | §2 ghi phép đo; §5 bỏ lý do "không cùng dạng lỗi"; B3b nói rõ phạm vi của chốt; câu hỏi cho chủ kho — sửa ở packet này hay mở packet riêng — ở §11, trả lời TRƯỚC khi cấp lease. Q-A và write set KHÔNG đổi |
| `dac-ta-phinh-rang-buoc-ngam` | P3 | Thứ tự assertion trong một đầu vào nêu tường minh ở quy ước chung, kể cả thứ tự riêng của `B2-pid-du-phong`. Thu gọn: sáu khối lịch sử (HINT), cộng bảng "Thay đổi so với r6", mục (r2)–(r7) của `nguon_cap_viec`, các lượt đo nền r3–r7, lịch sử con số `DOT_BIEN` (B5 và §8), §9 mục 7, hai mục lịch sử của §10 — thay bằng con trỏ tới r7 hoặc r6 kèm sha256. r8 ngắn hơn r7 (§10) |
| `khai-khong-do-duoc-ma-do-duoc` | P3 | Trục N và danh sách bất khả thi mục 10 ghi phép đo bằng seam `Path.iterdir("/proc")` (HINT); phiên soạn r8 đo lại trên ba Python (bảng 10 dòng 8) |
| (r8 tự thêm) | — | §1 bảng 10 (rig riêng, ba Python); đo lại nền nghiệm thu; ô `quy_uoc_review`; §11 Câu hỏi mở |

**Lịch sử r1 → r7** — không chép lại (r8, thu gọn). Bảng "Thay đổi so với r6" nằm nguyên văn ở đầu r7 (sha256
`3fc04fe5…5286`); các bảng r1 → r6 nằm nguyên văn trong r6 (sha256 `fadad3c7…3c99`), từ bảng "Thay đổi so với r5"
trở xuống. Cả hai tệp bất khả xâm phạm, cùng thư mục.

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

**Bảng 10 — số đo của phiên soạn r8 trên rig riêng (r8 thêm; KHÔNG phải ứng viên của executor)**

Rig r8: thư mục `mktemp -d` trong scratchpad của phiên soạn, ngoài kho. Nền: `git archive 89fc4fa .claude/dev` (blob
`561ff7a1…`, `abf7f6ca…`, đo bằng `git hash-object`). Ứng viên nháp: dựng lại bằng thay chuỗi của rig r7, **trùng
từng byte** ứng viên nháp r7. Helper: helper của reviewer lượt 7 (chép), phiên soạn r8 sửa ba chỗ — luật nguồn thêm
số lần; loại ghi nhận (2) cho seam chỉ-đếm `stat`/`read_text`; điều kiện dựng của hai đầu vào thật. 54 dòng đột biến
(chuỗi thay của rig r7). Biến thể (E): 89 của rig r7 cộng 21 của r8 (hai biến thể bắt buộc của HINT, bốn đối chứng
fp2–fp5, mười hai biến thể quét giải mã — năm cách lỏng và `encoding="utf-8"` tường minh, × hai đường — ba
biến thể quét đường/API) = 110; bảng biến thể máy đọc được có sha256
`46103809…8cb6`. Phép D: danh sách 57 đơn vị viết CỨNG theo §7. `PYTHONDONTWRITEBYTECODE=1`; con của rig
`start_new_session`, dọn bằng PID tường minh. Ba Python 3.11.15, 3.12.3, 3.13.12 (UTF-8 mode) trừ khi ghi khác; giờ
UTC 30-09-2026. Mã rig không nằm trong đặc tả (protocol §8).

| # | phép đo | kết quả | giờ UTC |
|---|---|---|---|
| 1 | bản đúng và nền, `t156`/`t157` | ứng viên SONG, SONG (0,29–0,30 giây); nền: `t156` đỏ `TinHieuChotCa:B1 seam escaped`, `t157` đỏ `B3b-giet-cay seam escaped` — ba Python | 06:16:41Z (3.12.3); 06:18:06Z (3.11.15); 06:19:20Z (3.13.12) |
| 2 | A1/A2/W1/W0 cho 54 dòng, 55 cặp, luật nguồn r8 | **55/55** được chấp nhận — ba Python | như dòng 1 |
| 3 | phép D | bản đúng xanh (`t156` 56 đơn vị, `t157` 1); **65 control** (17 nhãn + 48 tiểu nhãn) đều đỏ, báo đúng đơn vị thiếu; **6/6** phép đảo đỏ với `missing=[]`, `order=False` — ba Python | như dòng 1 |
| 4 | (E), 110 biến thể: 106 kỳ vọng chết hay đỏ, 4 kỳ vọng sống | **106/106** đúng kỳ vọng, gồm mười hai cách giải mã lỏng (`errors=` `replace`, `ignore`, `surrogateescape`, `backslashreplace`; `encoding=` `latin-1`, `cp1252`; × Đ0 và Đ) chết đúng `B2-nhanh-cu utf8-hong-that result True` hay `B2-dem-doc 4 kill count 0`, và ba đường/API khác (`open`, `read_bytes`, `os.path.exists`) đỏ bằng bộ đếm hay lỗi "seam không chạm"; bốn biến thể sống thì sống: hai đối chứng sống, và `encoding="utf-8"` tường minh ở Đ0 và ở Đ (hai ca SONG, D xanh — giới hạn đã khai). TRƯỚC khi mở rộng loại (2): `d0_value_thoat`, `d0_decode_thoat` có W0 chết vô can bởi `UnicodeDecodeError` THẬT của `utf8-hong-that` (0/2 ở cả ba Python); sau: 2/2 | 06:16:41Z–06:20:32Z; trước/sau: 06:16:22Z (3.12.3), 06:21:19Z–06:21:21Z (3.11.15, 3.13.12) |
| 5 | luật nguồn `B2-parse`, ba cách, trên (i), (l15), (l16), (l17), (l21) và tám biến thể (sáu đối chứng, `d0_value_thoat`, `d0_index_thoat`); ứng viên C2 viết phép tách đường mới thành hai dòng, cùng (l15), (l17) của nó | chuỗi con (r7): 5/5 dòng, 4/8 biến thể — fp2, fp3, fp4, fp5 được ghi `parse error escaped`, W0 sống (tín dụng giả); C2 (l17) vô can. Nguyên dòng (HINT lượt 7): 5/5, 6/8 — fp4, fp5 tín dụng giả; C2 (l17) nhận khi khai hai dòng, vô can khi khai một. **Nguyên dòng + số lần (r8): 5/5, 8/8; C2 (l15), (l17) nhận khi khai hai dòng** (khai một dòng ⇒ (l17) vô can). C2 tự nó: hai ca SONG, D xanh — ba Python | 06:17:52Z–06:20:46Z |
| 6 | chốt của tập lệnh dựng, và nhân chứng dương | bản RỖNG, neo vắng, neo xuất hiện hai lần ⇒ rc=3, không ghi biến thể; biến thể hợp lệ ⇒ rc=0; control RỖNG của D (bỏ một đơn vị không tồn tại) ⇒ D xanh ⇒ bị đánh "không đỏ đúng" (3.12.3). ENOMEM ở phép hỏi: ứng viên `True`, danh sách trắng ba errno THOÁT `OSError` errno 12, bản RỖNG `True`; AST lời gọi `os.kill` trong `_con_song`: ứng viên 1, khối K0 tách riêng 2, bản RỖNG 1 — ba Python | 06:13:16Z (chốt tập lệnh dựng); 06:35:23Z (control RỖNG của D); như dòng 1 (nhân chứng) |
| 7 | điều kiện dựng của hai đầu vào thật; `follow_symlinks` | con đặt `comm` bằng 15 byte viết dạng hex: `read_text()` thật ném `UnicodeDecodeError` ở UTF-8 mode (mã hoá `utf-8`) và ở locale ASCII (`PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LC_ALL=C`, mã hoá `ANSI_X3.4-1968`); `lstat` ⇒ tệp thường, không phải symlink — ba Python. Dựng tên con bằng CHUỖI tiếng Việt: ở locale ASCII chính lời gọi sinh con ném `UnicodeEncodeError`. Locale giải mã được 15 byte (Latin-1): KHÔNG ĐO ĐƯỢC — container chỉ có `C`, `C.utf8`, `POSIX` | 06:21:18Z–06:21:42Z |
| 8 | trục N: `_giet_cay` trên con sống, seam EACCES ở `Path.stat`; có và không có seam `Path.iterdir("/proc")` EACCES | không seam iterdir: ứng viên 124 (0,11 giây, 2 lần hỏi), (c) 125 (2,36–2,38 giây, 23 lần); có seam: ứng viên 125 "SIGTERM: me da chet, KHONG do duoc cay" (0,10 giây), (c) 125 (2,31 giây); nền ném `PermissionError` — ba Python | 06:21:50Z–06:22:08Z |
| 9 | thứ tự "đếm trước, kết quả sau" thay cho quy ước chung | 47/55 cặp: 8 cặp đỏ vì lệch loại — (l3), (l5), (l13), (l14), (l18), (l20), (m1), (m3); (i) không đỏ vì dòng (i) không nêu loại ở B5 (rig lượt 7 ghi loại cho (i) nên ra 46/55) — 3.12.3 | 06:22:28Z |
| 10 | đầu-cuối `launcher.py run --deadline-utc`, con đổi `comm` SAU lúc sinh (tập lệnh của reviewer lượt 7, chép) | nền và ứng viên nháp: rc=124, `giet_tron_ven=True`, con VẪN SỐNG và ghi tệp sau hạn — 3.12.3 | 06:22:40Z–06:23:06Z |

Không chạy lại ở r8: runner thật `chay_dot_bien`, kiểm kê ca đăng ký và `DOT_BIEN`, chữ ký chết theo nhãn, sàn
Windows, B6 toàn suite và ruff. Với các số về `DOT_BIEN` (228 / 231, runner, sàn 65/231) và B6, số của bảng 9 vẫn là
số hiện hành vì `DOT_BIEN` giữ 54 dòng và blob nền không đổi; số đơn vị, tiểu nhãn và control của bảng 9 là số r7
(r8: dòng 3 ở trên). Chữ ký (bảng 9 dòng 8) không đo lại: hai đơn vị mới không có dòng `DOT_BIEN` nào lấy làm đích
(suy từ B5, không đo); chúng có biến thể (E).

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
  chết" (r8, đo ở gạch đầu dòng dưới); packet này **không** sửa chúng trừ khi chủ kho trả lời khác ở §11.
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
  **Đo thêm ở cross-review lượt 7 (ba Python; ngoài phạm vi, KHÔNG sửa ở packet này — nhưng phải biết trước khi
  cấp lease).** (i) Kích hoạt THẬT, không cần `prctl`: kernel cắt `comm` ở 15 byte, nên một chương trình tên tiếng
  Việt — ví dụ `kiểm_tra_tiến_trình.sh` — có `comm` là UTF-8 bị cắt giữa ký tự; `read_text` thật ném
  `UnicodeDecodeError`, và `_con_song` = `False` cho tiến trình ĐANG SỐNG ở nền lẫn ứng viên nháp. (ii) Cùng lớp đi
  tới 124: `_khoa_danh_tinh` (`:359`) trả `None` và `_thanh_vien_nhom` (`:436`) bỏ qua tiến trình khi phép đọc lỗi,
  nên `_giet_cay` vào nhánh "tiến trình đã biến mất" (`:896–920`) và trả `tron_ven=True`. Đầu-cuối (3.12.3): `launcher.py
  run --deadline-utc` trên một con đổi `comm` như thế SAU lúc sinh (đo bằng `prctl`; một wrapper exec chương trình
  tên tiếng Việt cho cùng `comm` hỏng, như (i)) ⇒ **rc=124**, `ly_do_dung='qua han: tien trinh da khong con chay'`,
  `giet_tron_ven=True`, trong khi con VẪN SỐNG và chưa nhận tín hiệu nào — ở nền và ở ứng viên nháp như nhau
  (phiên soạn r8 chạy lại tập lệnh ấy trên rig riêng: cùng kết quả, §1 bảng 10 dòng 10). Nếu `comm` đã hỏng ngay lúc sinh thì `khoa=None` và lượt chạy trả rc=10 ("tu choi giet"), con cũng còn sống. Vậy câu
  "không cùng dạng lỗi" của r7 đúng về HÌNH (không ngoại lệ nào thoát) mà không đúng về NGHĨA: `:359` và
  `:436`/`:490` cùng lớp "đọc lỗi ⇒ coi như đã chết" mà objective cấm cho `_con_song`, và nó đi tới đúng mã 124 mà
  B3b khoá. Bản vá không gây ra nó (nền cho cùng kết quả). Câu hỏi cho chủ kho, trả lời TRƯỚC khi cấp lease: §11.
  Packet này không tự chọn, không mở rộng write set, không đổi Q-A.
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
  **r8 cũng KHÔNG đổi ngữ nghĩa Q-A.1–6**, chỉ nói rõ theo lượt 7 rằng "nguyên xi" ở Q-A.3 gồm cả chính lời gọi đọc
  (không đối số giải mã), và rằng "nội dung không phân tích được" ở Q-A.4 gồm nội dung THẬT không giải mã được bằng
  lời gọi ấy (ngay dưới bước 3 và bước 4);
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
     **(r8, cross-review lượt 7, không đổi ngữ nghĩa)** "Nguyên xi" gồm cả chính LỜI GỌI đọc: `read_text()`
     không đối số giải mã (không `errors=`, không `encoding=`), nên nội dung THẬT không giải mã được ở nhánh tệp
     có vẫn ⇒ `False` như §2. Lý do đo được: `read_text(errors="replace")` — idiom có sẵn ở `launcher.py:3600`,
     `:3647`, `:3680` — hay `read_text(encoding="latin-1")` ở nhánh tệp có qua hết r7 + D ở ba Python (seam
     `p4` thay CẢ lời gọi nên không thấy tham số), mà đổi kết quả của tiến trình SỐNG có `comm` không UTF-8 từ
     `False` thành `True`. Đầu vào riêng: `B2-nhanh-cu utf8-hong-that` (đường cũ) và `B2-dem-doc 4` (đường mới).
     Đọc bằng API khác (`open`, `read_bytes`) cũng trái "nguyên xi" và bị bộ đếm đọc bắt (§7, "Seam thay CẢ lời
     gọi"). `encoding="utf-8"` hay `errors="strict"` tường minh cũng trái chữ "không đối số", nhưng trùng hành vi khi
     mã hoá mặc định là UTF-8, nên không đầu vào nào phân biệt được ở đó: KHÔNG ĐO ĐƯỢC bằng hành vi (§1 bảng 10).
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
     **Làm rõ (r8, không đổi ngữ nghĩa):** phép đọc của bước 4 cũng là `read_text()` không đối số giải mã, như nhánh
     cũ; nội dung THẬT không giải mã được bằng lời gọi ấy là "không phân tích được" ⇒ rơi về `os.kill(pid, 0)`. Đọc
     lỏng (`errors="replace"`, `encoding="latin-1"`, …) biến nội dung ấy thành "đọc được" và bỏ bước kill — vi phạm, đo
     được ở `B2-dem-doc 4` (§1 bảng 10).
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

Không đường dẫn nào khác. Đặc tả này (`ops/specs/launcher-con-song-esrch-r8.md`) là hồ sơ của lượt
soạn, không thuộc write set thi hành.

## 5. `ngoai_pham_vi`

- `:359`, `:430`, `:484` và mọi chỗ đọc `/proc` đã có `try`; nhánh cũ `exists()` đúng mà `read_text`
  lỗi (§2).
  (r8) Lý do "không cùng dạng lỗi" của r7 bị bỏ: cross-review lượt 7 đo được `:359` và `:436`/`:490` cùng lớp "đọc
  lỗi ⇒ coi như đã chết", tới mã 124 khi tiến trình còn sống (§2). Chúng ở ngoài phạm vi vì đặc tả này mặc định
  KHÔNG mở rộng write set hay Q-A, cho tới khi chủ kho trả lời §11; nếu chủ kho chọn sửa ở packet này thì phải có
  revision mới.
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
  mà vẫn đếm được; (r8) khi lời gọi thật ném, seam chỉ-đếm ghi lại CHÍNH đối tượng ấy rồi ném lại đúng nó, như
  observer `kill` (loại ghi nhận (2) ở dưới). Observer `os.kill(pid, 0)` (chỉ cặp PID đang xét và tín hiệu 0; ghi lại rồi chuyển tiếp thật,
  hoặc ném lỗi seam; tín hiệu khác hay PID khác chuyển tiếp nguyên vẹn) đặt ở (r7): mọi đầu vào mà đường Q-A đi
  qua bước kill — tầng K (`B2-doc-hong`, `B2-parse`, `B2-dem-doc` tiểu nhãn `3` và `4` (r8), `B2-pid-du-phong`, và tiểu nhãn
  `kill`/`kill-*` của `B2-tin-hieu`, `B2-exception`, `B2-thoat-parse`) và tầng K0 (mọi tiểu nhãn `vang*` của
  `B2-nhanh-cu`) — cùng các đầu vào tầng Đ0 (phần tệp có của `B2-nhanh-cu` và lời gọi đường cũ của `B3-zombie`), để
  đếm được con số 0. Ba đầu vào tầng hỏi của `B2-thoat-parse` đặt seam ở `Path.exists` (bảng 7), và
  bộ đếm của chính seam ấy phải ≥ 1 — bằng 0 (ứng viên không hỏi bằng `exists()`) thì ca ném lỗi thường,
  không phải `bang`, và executor đổi seam sang hàm `Path` mà ứng viên thực sự gọi rồi khai vào handoff.
- **Seam thay CẢ lời gọi — tham số nó che, và cách đóng (r8, lớp `ma-tran-loi-thieu-chot` lần thứ tám).** Seam
  ném lỗi hay trả chuỗi dựng sẵn thì thay nguyên lời gọi, nên không thấy đối số của lời gọi. Rà mọi seam của hai ca:
  · `Path.read_text` (ném hay trả payload, ở Đ, Đ0, K và ma trận `B2-pid-du-phong`) che `encoding`, `errors` (và
    `newline` từ 3.13). Đóng bằng hai đầu vào nội dung THẬT (`B2-nhanh-cu utf8-hong-that`, `B2-dem-doc 4`): cách
    giải mã nào làm 15 byte ấy đọc được và tách ra trạng thái thì đổi kết quả (Đ0: `True` thay `False`) hay bỏ bước
    kill (Đ) ở đó — suy từ hợp đồng; đo được mười hai biến thể (sáu cách giải mã lỏng × hai đường) chết đúng tiểu
    nhãn và loại, ba Python, bảng 10 dòng 4. `encoding="utf-8"` hay `errors="strict"`
    tường minh trùng hành vi khi mã hoá mặc định là UTF-8 (hai ca SONG, D xanh — đo): KHÔNG ĐO ĐƯỢC bằng hành vi
    ở đó. `newline` chỉ đổi cách dịch ký tự CR, mà phần sau dấu `)` cuối — phần duy nhất phép tách đọc — do kernel
    ghi và không có CR: suy luận, không đo.
  · `Path.stat` và `Path.exists` (ném) che `follow_symlinks`: `/proc/<pid>/stat` là tệp thường, không phải
    symlink (`lstat`, bảng 10 dòng 7), nên tham số ấy không đổi kết quả.
  · ĐƯỜNG DẪN và API: mọi seam khoá theo đúng chuỗi `/proc/<pid>/stat` của PID đang xét, cộng bộ đếm. Ứng viên
    đọc hay hỏi bằng đường khác hoặc API khác (`open`, `read_bytes`, `os.path.exists`) không chạm seam ⇒ bộ đếm 0
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
- **Thứ tự assertion TRONG một đầu vào (r8, cross-review lượt 7).** Mỗi đầu vào xét theo thứ tự: (1) ngoại lệ thoát
  (phân hạng theo bốn loại, hay danh tính sentinel); (2) kết quả; (3) đếm hỏi; (4) đếm đọc; (5) đếm kill. Riêng
  `B2-pid-du-phong`: (1) ngoại lệ thoát; (2) đếm kill; (3) kết quả; (4) đếm hỏi; (5) đếm đọc. Bước mà đầu vào không
  đòi (không đặt observer, không đếm) thì bỏ, giữ thứ tự các bước còn lại. Loại assertion mà B5 và (E) nêu cho từng
  dòng GIẢ ĐỊNH thứ tự này. Đo, 3.12.3: helper chỉ đổi sang "đếm trước, kết quả sau" làm 9/55 cặp đỏ vì lệch loại ở
  rig lượt 7 ((i), (l3), (l5), (l13), (l14), (l18), (l20), (m1), (m3)) và 8/55 ở rig r8 (cùng danh sách trừ (i), vì
  dòng (i) không nêu loại ở B5; bảng 10 dòng 9), dù ứng viên, helper và 54 dòng đều đúng.
- Ca chỉ chuyển thành `bang(False, ...)` ngoại lệ **có gốc đo được từ chính ca** (r6 nêu đủ bốn loại; r5 chỉ
  nêu loại đầu): (1) đối tượng do seam tạo ra, so bằng danh tính (`is`); (2) ngoại lệ THẬT mà observer của
  `os.kill(pid, 0)` — hay (r8) seam chỉ-đếm của `Path.stat`, `Path.read_text` — vừa chuyển tiếp: seam ghi lại đối
  tượng rồi ném lại đúng nó, nên danh tính biết trước khi nó thoát (cần cho `B2-pid-du-phong` tiểu nhãn `da-wait`,
  nơi ESRCH là của kernel chứ không của seam; và cho hai đầu vào nội dung thật, nơi `UnicodeDecodeError` là của phép
  đọc thật — thiếu mở rộng r8, W0 của hai biến thể (E) `d0_value_thoat`, `d0_decode_thoat` chết vô can khi nới
  `B2-nhanh-cu`, bảng 10 dòng 4); (3) ngoại lệ mới có chuỗi `__cause__` (tức `raise … from …`) chứa một đối tượng loại (1) hoặc (2) —
  bản vá bọc lại ngoại lệ thay vì để nó thoát nguyên đối tượng (Q-A.5); thông điệp ghi `seam wrapped`;
  (4) chỉ ở `B2-parse`, ở các đầu vào parse `p1`–`p3` của `B2-pid-du-phong` (đúng các đầu vào của `B2-parse`), và ở
  hai đầu vào tự nhiên `p1`, `p3` của `B2-nhanh-cu` (r7, cột Đ0), và chỉ sau khi seam đọc đã chạm: ngoại lệ TỰ
  NHIÊN của phép tách trạng thái (nhãn `B2-parse` mô tả cách nhận ra — r8: theo kiểu, đối số VÀ nguồn; nguồn so bằng
  HÀM, NGUYÊN DÒNG đã khai (bỏ khoảng trắng hai đầu) và SỐ LẦN dòng ấy xuất hiện trong tệp nguồn — không bằng chuỗi
  con, tệp hay số dòng). Chuỗi `__context__` (ngữ cảnh ngầm) KHÔNG được tính: một ngoại lệ vô can ném ra
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
  tính; ngoại lệ thật mà observer hay seam chỉ-đếm đã ghi; ngoại lệ bọc lại; ngoại lệ tự nhiên nhận ra theo luật
  của `B2-parse`, kể cả điều kiện nguồn) thoát khỏi lời gọi
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
      phép chỉ số danh sách. **Cách so (r8 sửa r7, cross-review lượt 7 và phiên soạn r8): so HÀM, NGUYÊN DÒNG và SỐ
      LẦN; KHÔNG so chuỗi con, tệp hay số dòng.** Executor khai trong handoff (a) tên hàm chứa biểu thức tách (ở nền
      là `_con_song`; hàm trợ giúp riêng nếu ứng viên tách ra); (b) NGUYÊN VĂN mọi dòng nguồn mà ngoại lệ tự nhiên
      của phép tách có thể ném từ đó — ở nền là một dòng, `return noi_dung[noi_dung.rindex(")") + 2:].split()[0] !=
      "Z"`; biểu thức viết hai dòng thì khai cả hai (dòng `rindex` ném `ValueError`, dòng `[0]` ném `IndexError`); và
      (c) với mỗi dòng của (b), số lần nó xuất hiện (bỏ khoảng trắng hai đầu) trong tệp ứng viên — hai khối đọc Đ0
      và Đ viết cùng một dòng thì khai 2. Ca đòi ba điều: `co_name` của khung trong cùng bằng (a); dòng nguồn của khung
      ấy — đọc từ `co_filename` bằng `linecache` sau `checkcache`, hoặc đọc thẳng tệp — bỏ khoảng trắng hai đầu, BẰNG
      một dòng của (b); và số dòng BẰNG dòng ấy trong CHÍNH tệp `co_filename` (tệp đang chạy, kể cả tệp đột biến tạm
      của runner) đúng bằng số đã khai ở (c). Vì sao không so tệp và số dòng như HINT lượt 6 viết (giữ lý do của r7):
      runner `--dot-bien` nạp mỗi bản đột biến từ một tệp tạm riêng (`launcher_db_NN.py`), nên `co_filename` KHÔNG BAO
      GIỜ bằng tệp executor khai; và đột biến chèn dòng phía trên biểu thức tách làm trôi số dòng — (l16) chèn đúng
      một dòng (bảng 9 dòng 5). Vì sao không so CHUỖI CON như r7: đo ở cross-review lượt 7 (ba Python) — đổi MỘT
      token của biến thể tín dụng giả lượt 6 thành `os.environ.get(…, "").rindex(")")` (fp2), hay chỉ đặt một chú
      thích chứa `rindex(")")` trên một dòng ném `IndexError` không liên quan (fp3), là được ghi `parse error escaped`,
      W1 đúng tiểu nhãn, W0 sống: tín dụng giả qua đủ bốn phép; và khi biểu thức tách viết hai dòng (cách
      `_khoa_danh_tinh` :361–362 viết), `IndexError` ném từ dòng `[0]` không chứa `rindex(")")` nên (l17) chết vô can
      ở A1, W1, W0. Vì sao phải có SỐ LẦN (r8): nguyên dòng một mình vẫn giả được bằng một bản SAO Y nguyên văn dòng
      tách chạy trên chuỗi không liên quan — trong nhánh xử lý `ValueError` (fp4) hay ngay sau khối `try` (fp5) — cả
      hai được ghi `parse error escaped`, W0 sống (đo ba Python, bảng 10 dòng 5). Bản sao làm số lần tăng thêm một,
      nên luật số lần loại cả hai; 54 dòng vẫn 55/55 cặp; biểu thức hai dòng khai đủ hai dòng ⇒ (l15), (l17) chấp nhận
      (khai thiếu dòng `[0]` ⇒ (l17) chết vô can — cùng bảng). Đột biến ĐỔI chính dòng tách (như (m5)) thì dòng ấy
      không còn khớp (b) — hợp lệ, vì các dòng ấy nhắm kết quả chứ không nhắm ngoại lệ tự nhiên. Ngoại lệ có kiểu
      khác hoặc đối số khác — ví dụ một `ValueError` do lỗi khác của ứng viên — vẫn là lỗi vô can, giữ hạng vô can.
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
    (r8) Đối chứng thứ tư đến thứ bảy (bắt buộc), mỗi cái phải chết vô can ở A1, W1 và W0: fp2 (`.rindex(")")` trên
    chuỗi không liên quan trong nhánh xử lý), fp3 (`"".split()[0]` kèm chú thích chứa `rindex(")")`), fp4 (sao y
    nguyên văn dòng tách, trên chuỗi rỗng, trong nhánh xử lý `ValueError`), fp5 (cùng bản sao y, ngay sau khối `try`,
    ngoài nhánh xử lý). Đo (bảng 10 dòng 5, ba Python): luật chuỗi con của r7 cấp tín dụng cho cả bốn; luật nguyên
    dòng của HINT lượt 7 cho fp4, fp5; luật r8: không cái nào.
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
    `read_text` ném EACCES (đọc lỗi); (4) (r8) con THẬT có `comm` UTF-8 hỏng, `stat` EACCES + `read_text` THẬT ném
    `UnicodeDecodeError` ⇒ rơi về `kill(pid, 0)`: `True` (chi tiết ngay dưới đoạn ĐỎ khi). Trong mỗi
    đầu vào, số lần `Path.read_text` chạm đúng đường `/proc/<pid>/stat` của PID ấy **bên trong cửa sổ
    lời gọi `_con_song`** phải bằng **đúng 1** (gồm cả nhánh đọc thành công lẫn nhánh đọc lỗi). Cửa sổ
    đếm chỉ bao lời gọi: mọi lần đọc kiểm soát do chính ca thực hiện (ví dụ đọc để xác nhận trạng
    thái) nằm NGOÀI cửa sổ — lượt 2 đã đo trường hợp nhầm: cộng lần đọc kiểm soát vào thì bản đúng
    báo 2 (VERDICT lượt 2, hướng 7). Phép đọc khoá của wrapper (`_khoa_danh_tinh`, `:359`) không thuộc
    bộ đếm này vì ca gọi trực tiếp. Bộ đếm là lớp quan sát: nó chuyển tiếp sang `read_text` thật và
    KHÔNG thay nội dung, trừ ở các đầu vào "đọc hỏng" đã khai (đầu vào (3) này, và bốn đầu vào của
    `B2-parse`). Giữ nguyên các kiểm đếm `stat` hiện có (`B2-dem-lan`). (r7, quy ước đếm) Mỗi đầu vào còn đòi hỏi
    đúng 1; đầu vào `3` và `4` (đường K) đặt observer `os.kill(pid, 0)` chuyển tiếp thật và đòi đúng 1 lời gọi. **ĐỎ khi** (đột biến (j)): bộ
    đếm ≠ 1, tức đọc lại lần hai, ở nhánh nào cũng vậy — lần đọc thứ hai đặt sau lần đọc thành công làm
    đầu vào `1` đỏ đầu tiên; lần đọc thứ hai đặt trong xử lý đọc lỗi chỉ chạm ở đầu vào `3`.
    **Đầu vào `4` (r8, cross-review lượt 7).** Con sinh bằng `start_new_session`, tự gọi `prctl(PR_SET_NAME, …)` với
    đúng 15 byte của `'kiểm_tra_tiến_trình'.encode()[:15]` — thứ kernel làm với một chương trình tên tiếng Việt:
    `comm` bị cắt ở 15 byte, giữa một ký tự nhiều byte, nên nội dung `/proc/<pid>/stat` THẬT không giải mã được
    (đo: `comm` kết thúc bằng `e1 ba`, hai byte đầu của `ế`). Điều kiện dựng (xác nhận `comm` bằng bytes, rồi
    `read_text()` thật ném `UnicodeDecodeError` ngoài cửa sổ đếm) và cách viết 15 byte: quy ước chung, mục "Seam thay
    CẢ lời gọi"; dọn con bằng PID tường minh. Đây là đầu vào đầu tiên của tầng Đ dùng nội dung THẬT: `p4` của
    `B2-parse` là seam thay CẢ lời gọi `read_text`, nên không thấy tham số giải mã — bản vá đọc đường mới bằng
    `read_text(errors="replace")` qua `p4` mà chết ở đây, loại `kill count 0` (đo ba Python). Đầu vào này ở
    `B2-dem-doc`, KHÔNG ở `B2-parse`: reviewer lượt 7 đo đặt ở `B2-parse` thì W0 của (l15), (l16), (l19), (l21) chết
    vô can vì `UnicodeDecodeError` THẬT không thuộc bốn loại ghi nhận của r7 (51/55 cặp); ở `B2-dem-doc`: 55/55. r8
    giữ vị trí của HINT; với loại (2) mở rộng ở r8, vị trí `B2-parse` còn làm W0 chết vô can hay không: KHÔNG ĐO
    ĐƯỢC ở r8 (chưa thử).
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
    p1–p3, theo quy tắc của `B2-parse` (kể cả điều kiện nguồn và số lần, r7 và r8). Không đổi ngữ nghĩa Q-A.3/.4.
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
      `IndexError` tự nhiên ⇒ **`False`**. Hai đầu vào này dùng luật nhận ra ngoại lệ tự nhiên của `B2-parse` (kiểu,
      đối số, nguồn) để hướng "thoát" chết đúng lý do. `p4`: `read_text` ném MỘT `UnicodeDecodeError` dựng sẵn ⇒
      **`False`**. (HINT lượt 6 gọi `p1` là `rong`; r7 đổi tên cho khớp `B2-parse`.)
      `utf8-hong-that` (r8, cross-review lượt 7): PID là con THẬT đã đổi `comm` như đầu vào `4` của `B2-dem-doc`
      (cùng điều kiện dựng); `stat` và `read_text` THẬT (chỉ đếm, ghi ngoại lệ thật — loại (2)), observer chuyển tiếp
      thật ⇒ **`False`** (hành vi cũ §2), hỏi 1, đọc 1, kill 0. `p4` (seam) đo MỆNH ĐỀ bắt; đầu vào này đo chính LỜI
      GỌI đọc: bản vá `read_text(errors="replace")` hay `read_text(encoding="latin-1")` ở nhánh tệp có qua `p4`, qua
      cả r7 + D, mà chết ở đây, loại `result True` (đo ba Python). Không có dòng `DOT_BIEN` (sàn Windows, B4); biến
      thể (E) `d0_giai_ma_long`. Nó cùng nhãn với đích của `d0_value_thoat` và `d0_decode_thoat`, nên W0 của hai biến
      thể ấy chạy qua nó: thiếu loại (2) mở rộng thì `UnicodeDecodeError` THẬT làm W0 chết vô can (bảng 10 dòng 4).
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
    | R3-Đ | nhóm phân tích × đọc | rơi về `kill(pid, 0)` (Q-A.4, .5) | `B2-parse`: `p1`, `p2` (`ValueError` tự nhiên), `p3` (`IndexError` tự nhiên), `p4` (`UnicodeDecodeError` do seam); `B2-dem-doc 4` (`UnicodeDecodeError` THẬT, r8) | `ValueError` thoát: (l15) ở `p1`, (l16) ở `p2` · `ValueError` sai: (i) · `IndexError` thoát: (l17) · `IndexError` sai: (l18) · `UnicodeDecodeError` thoát: (l19) · `UnicodeDecodeError` sai: (l20) · bọc: (l21) |
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
    | R0-K | `kill` thành công ⇒ `True` (Q-A.4) | `B2-doc-hong`, `B2-parse`, `B2-dem-doc 3`, `4` (r8), `B2-pid-du-phong song` | sai: E `k_ok_sai` (không gọi kill: (k1), tính ở trục C) |
    | R1-Đ0 | ESRCH ở phép đọc cũ ⇒ `False` | `B2-nhanh-cu ESRCH` | thoát: E `d0_ESRCH_thoat` · sai: E `d0_ESRCH_sai` |
    | R2-Đ0 | `OSError` khác ở phép đọc cũ ⇒ `False` | `B2-nhanh-cu EACCES`, `EIO`, `EPERM` | EACCES thoát: E `d0_EACCES_thoat` · EACCES sai: (m1) · EIO thoát / sai: E `d0_EIO_thoat` / `d0_EIO_sai` · EPERM thoát / sai: E `d0_EPERM_thoat` / `d0_EPERM_sai` |
    | R3-Đ0 | nhóm phân tích ở nhánh cũ ⇒ `False` | `B2-nhanh-cu p1` (`ValueError` tự nhiên), `p3` (`IndexError` tự nhiên), `p4` (`UnicodeDecodeError` do seam), `utf8-hong-that` (`UnicodeDecodeError` THẬT, r8) | `ValueError` thoát / sai: E `d0_value_thoat` / `d0_value_sai` · `IndexError` thoát / sai: E `d0_index_thoat` / `d0_index_sai` · `UnicodeDecodeError` thoát / sai: E `d0_decode_thoat` / `d0_decode_sai` · `UnicodeDecodeError` sai do giải mã lỏng (r8): E `d0_giai_ma_long` |
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
    | Đ → K: đọc lỗi hay hỏng | 1 | 1 | 1 | `B2-doc-hong`, `B2-parse`, `B2-dem-doc 3`, `4` (r8), `B2-pid-du-phong`, tiểu nhãn `kill`/`kill-*` của ba nhãn sentinel | hỏi lại: E `k_hoi_hai_lan` · đọc lại: (j2) — thêm E "đọc lại chỉ khi EPERM" (bản vá sai của lượt 6) · kill hai lần: (k5) — thêm E `k_kill_lai_khi_doc_EPERM` · không gọi kill: (k1) — thêm E `d_giai_ma_long` (r8: đọc với `errors="replace"` nên nội dung thật không còn lỗi, không gọi kill) |

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
    — không đầu vào nào của hai ca đi qua, nhưng ĐO ĐƯỢC bằng một seam (r8, cross-review lượt 7): `Path.iterdir`
    ném EACCES riêng cho `/proc` ⇒ `_chup_cay`, `_thanh_vien_nhom` trả `None` ⇒ `_con_lai()` là `None`. Con sống,
    seam EACCES ở `Path.stat`: ứng viên nháp ⇒ `tron_ven=False`, **125** ("SIGTERM: me da chet, KHONG do duoc cay",
    0,10 giây); đột biến (c) ⇒ **125** (2,31 giây) — số của reviewer lượt 7 (3.12.3); phiên soạn r8 đo lại ở ba
    Python, cùng kết quả (bảng 10 dòng 8). Hai nơi ấy dựng `KetGiet(…, False, …)` — `ca_cay` viết cứng
    `False` — nên mã LUÔN là 125; `_con_song` ở đó chỉ đổi `me_da_chet` và thời lượng. Không có rủi ro 124/125 do
    bản vá tại hai nơi ấy; không bắt buộc thêm đầu vào.

    **Kiểm đếm bảng mở rộng** (đếm từ bảng; biến thể và kết quả đo ở bảng 9 và 10): 30 ô (6 hàng × 5 tầng), ô nào cũng
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
    (r8) Hai biến thể (E) mới `d0_giai_ma_long` (R3-Đ0) và `d_giai_ma_long` (trục C, Đ → K) thuộc hạng mục SẴN CÓ nên
    129 / 78 không đổi. Bộ (E) của r8: **95 biến thể** = 78 biến thể hạng mục + 2 biến thể giải mã lỏng + 5 bản vá sai
    của lượt 6 + 2 biến thể lặp có điều kiện + 6 đối chứng của luật `B2-parse` (khác đối số; fp của lượt 6; fp2, fp3,
    fp4, fp5) + 2 đối chứng sống. Đo trên rig r8 (bảng 10 dòng 2 và 4, ba Python): 55/55 cặp; 93 biến thể kỳ vọng
    chết hay đỏ đều đúng kỳ vọng; hai đối chứng sống thì sống.

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
    số ĐO trên một cách cài, không suy từ văn bản (xem đính chính sau bảng 8 về (g1)). **(r8)** Hai đơn vị mới
    (`B2-nhanh-cu utf8-hong-that`, `B2-dem-doc 4`) không có dòng B5 nào lấy làm đích — suy từ B5, không đo lại chữ ký
    ở r8 — nên danh sách trên thành **11** trên 57 đơn vị; cả hai có biến thể E giết đúng lý do (bảng 10 dòng 4).

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

    Bốn điều r3–r5 đã đo là sai nếu làm tắt, điều thứ năm r6 thêm, thứ sáu r7 thêm, thứ bảy r8 thêm: (1) EACCES ở tầng đọc **không đại
    diện** cho họ `OSError` — một bản chỉ bắt `PermissionError` ở tầng đọc qua cả hai ca r3 (bảng 5); (2) ESRCH ở
    tầng hỏi **không thay** ESRCH ở tầng đọc, kỳ vọng ngược nhau; (3) sentinel `RuntimeError` **không thay**
    sentinel `KeyboardInterrupt` ở tầng đọc; (4) `True` trên PID sống **không chứng minh** đã hỏi PID (bảng 6):
    phải có PID đã `wait` (kết quả `False`), có quan sát đúng lời gọi `kill(pid, 0)`, và có kết quả EPERM/EIO của
    chính lời gọi ấy; (5) **một sentinel của nhóm này không đại diện cho nhóm khác và một tầng không đại diện
    cho tầng khác** — `RuntimeError` ở tầng hỏi không thay `IndexError`/`ValueError`/`UnicodeDecodeError` ở tầng
    hỏi (bản HINT lượt 5 qua hai ca r5 và phép D mà vẫn nuốt `IndexError`), và mọi sentinel ở tầng hỏi hay đọc
    không thay cho tầng kill; (6, r7) **đường mới không đại diện cho nhánh cũ, khối kill dùng chung không đại diện
    cho khối kill tách riêng, và phép đếm ở vài nhãn không đại diện cho phép đếm trên mọi đường** — một helper dựng
    đúng theo HINT lượt 6 để lọt 34 biến thể trái Q-A (bảng 9 dòng 7); (7, r8) **một seam thay CẢ lời gọi không
    đại diện cho lời gọi thật** — nó đo mệnh đề bắt, không thấy đối số (giải mã) của lời gọi, nên phải có đầu vào nội
    dung THẬT (quy ước chung, "Seam thay CẢ lời gọi"). Đây là chốt của hợp đồng Q-A, không phải lời khai rằng kernel thật đã sinh các lỗi
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
  166/309 = 53,72 % đo được — suy bằng số học từ cùng phép đếm, không dựng và không chạy). Vì vậy r7 và r8 giữ `DOT_BIEN` ở 54 dòng và đo 78 hạng mục ấy
  bằng phép (E) trong tập lệnh bằng chứng cục bộ (B5); đổi cân bằng này — thêm dòng `DOT_BIEN` cho một số hạng mục
  (tối đa sáu trước khi chạm sàn theo cận dưới), hay cho hai ca chạy nhánh `/proc` trên Windows bằng seam — là
  quyết định của điều phối/chủ kho, r7 và r8 không tự chọn (§11).

**Ca `t157_...`**

- **B3b (mục 2) — chốt tiêu thụ `_giet_cay`.** Con thật CÒN SỐNG, session riêng, `khoa` lấy trước seam;
  seam EACCES ở `Path.stat` của PID ấy; gọi `_giet_cay(pid, khoa)` để SIGTERM thật biến con thành
  zombie chưa `wait`; kết quả phải có `tron_ven=True` (phía deadline ánh xạ 124, `launcher.py:1669`).
  Nhãn `B3b-giet-cay`. Dọn PID con và `wait` trong `finally`. Ca này riêng để đột biến (c) ở B5 làm
  **cả hai** ca `t156_...` lẫn `t157_...` đỏ, mỗi ca bằng `TinHieuChotCa` của chính nó.
  **ĐỎ khi:** đột biến bỏ phép đọc nội dung ⇒ `tron_ven=False` ⇒ tương ứng 125 (bảng 2, hàng HẸP r1).
  **Phạm vi của chốt (r8, cross-review lượt 7).** B3b chỉ phủ lỗi của PHÉP HỎI. Khi phép ĐỌC khoá danh tính lỗi
  (`comm` UTF-8 hỏng), `_giet_cay` vẫn trả `tron_ven=True` — 124 — cho tiến trình còn sống (§2, đo đầu-cuối); ca này
  không khẳng định điều ngược lại, và không đỏ với lỗi ấy.

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
  nguyên văn ở đoạn này của r7 (sha256 `3fc04fe5…5286`) — không chép lại (r8, thu gọn). r7 và r8 KHÔNG thêm dòng nào
  ngoài năm dòng (m) của HINT lượt 6, dù bảng không gian mở rộng có 78 hạng mục không có dòng riêng: dòng Linux-only
  thứ bảy đã đưa Windows xuống dưới sàn (B4); 78 hạng mục ấy được đo bằng phép (E).

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
  12; nên đối chứng này có răng với chính điều kiện nguồn). (r8) Thêm bốn đối chứng fp2, fp3, fp4, fp5 như ở
  `B2-parse` — cả bốn phải chết vô can; luật chuỗi con của r7 cấp tín dụng cho cả bốn, luật nguyên dòng của HINT cho
  fp4, fp5, luật r8 (thêm số lần) cho không cái nào (bảng 10 dòng 5).
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
     thứ tự hai nhãn (năm phép của r6 cộng `B2-pid-du-phong` với `B2-nhanh-cu`) đều đỏ với tập vẫn đủ.
  5. **Chỗ đặt.** D và control của nó nằm ở tập lệnh bằng chứng cục bộ của executor, như phép A/W: không
     thêm ca đăng ký (vẫn hai ca), không sửa runner `--dot-bien`, không tăng số mục `DOT_BIEN` sản phẩm.
  6. **Nghĩa vụ nộp và log (r8 thêm phần nộp, cross-review lượt 7).** Nộp kèm handoff chính tập lệnh của D và BẢNG
     control máy đọc được — mỗi dòng: tên control, thứ bị đổi trên bản sao test (nhãn thêm vào tập NỚI mặc định, hay
     đầu vào bị bỏ), đơn vị thiếu kỳ vọng; cộng danh sách 57 đơn vị viết cứng và sáu cặp đảo thứ tự — mỗi tệp kèm
     sha256; reviewer chạy lại trên đúng SHA ứng viên. Control RỖNG (không đổi gì so với bản test) để D xanh, nên rơi
     đúng vào điều kiện "control không đỏ" ở câu cuối mục này (đo ở rig r8, 3.12.3, 06:35:23Z: bỏ một đơn vị không tồn
     tại ⇒ D xanh ⇒ control bị đánh "không đỏ đúng"). Log: lệnh nguyên văn, giờ UTC, rc, dòng xanh của bản đúng cho từng ca,
     và từng dòng control kèm đơn vị thiếu. **Không nhận A1/A2/W1/W0 là đủ** nếu thiếu D, thiếu tập lệnh hay bảng
     control, nếu bản đúng đỏ, hoặc nếu bất kỳ control nào không đỏ.
  Đã đo (r8 thu gọn: năm lượt trước không chép lại — lượt 3, lượt 4, phiên soạn r5, phiên soạn r6 nằm nguyên văn
  ở D của r6; số của cross-review lượt 6 ở VERDICT lượt 6):
  · phiên soạn r8 (rig riêng, helper r8, 57 đơn vị viết cứng; ba Python; bảng 10 dòng 3): bản đúng xanh (`t156` 56
  đơn vị, `t157` 1); **65 control (17 nhãn + 48 tiểu nhãn) đều đỏ**, mỗi cái báo đúng đơn vị thiếu; sáu phép đảo
  thứ tự đều đỏ với `missing=[]`, `order=False`.
  · phiên soạn r7 (01:33:28Z 30-09, Python 3.12.3; lặp 01:41:40Z ở 3.11.15 và 01:43:18Z ở 3.13.12, cùng kết quả; rig
  riêng, helper r7, 55 đơn vị): bản đúng xanh ở cả hai ca (`t156` 54 đơn vị, `t157` 1); **63 control (17 nhãn + 46
  tiểu nhãn) đều đỏ**, mỗi cái báo đúng đơn vị thiếu; sáu phép đảo thứ tự đều đỏ với `missing=[]`, `order=False`
  (bảng 9 dòng 3).
  **CHƯA ĐO:** tập lệnh bằng chứng của executor và D trên mã của executor.

  **(E) Săn theo bảng không gian mở rộng — MỘT biến thể cho mỗi hạng mục không có dòng B5, trong tập lệnh bằng
  chứng cục bộ, KHÔNG vào `DOT_BIEN` (r7).** Vì sao cần: 78 hạng mục của bảng không gian mở rộng không có mục
  `DOT_BIEN` riêng, và không được có (B4: dòng Linux-only thứ bảy đưa Windows xuống dưới sàn). Không có (E) thì răng
  của các hạng mục ấy chỉ là lời văn — đúng loại "danh sách tự liệt kê, cho là hết" mà §9 đếm tới lần thứ tám.
  1. **Đối tượng.** Với mỗi hạng mục không có dòng B5 (bảng không gian mở rộng, cột (iii) ghi "E"), executor dựng
     MỘT biến thể của CHÍNH ứng viên của mình: một thay đổi ở một vị trí mã, vi phạm hạng mục ấy (chạm thêm hạng
     mục khác thì A1 được báo ở nhãn đứng trước, như một dòng B5 — ví dụ đo được: bản trả `False` cho nội dung đọc
     được ở nhánh cũ chết trước ở `B2-dem-lan`, W1 vẫn chết đúng `B2-nhanh-cu song`). Cộng: bảy bản vá sai của cross-review lượt 6 (năm trùng (m1)–(m5),
     hai cái kia là "hỏi lại khi `OSError` khác EACCES" và "đọc lại chỉ khi EPERM"), biến thể "kill lần hai chỉ khi
     đọc gặp EPERM", sáu đối chứng của luật `B2-parse` (khác đối số; cùng đối số khác nguồn; và r8 thêm fp2, fp3,
     fp4, fp5 — xem `B2-parse`), và hai đối chứng phải SỐNG: một khối K0 tách riêng mà ĐÚNG ngữ nghĩa nền (chứng tỏ các đầu
     vào K0 không bắt oan một cách tách hợp lệ), và bản danh sách trắng ba errno (giới hạn đã khai ở mục 3 — phải
     sống, không thì phép đo đang đo thứ khác). (r8) Cộng hai biến thể giải mã lỏng cho hạng mục SẴN CÓ, như
     (l15)/(l16): `d0_giai_ma_long`, kỳ vọng `B2-nhanh-cu utf8-hong-that` loại `result True`, và `d_giai_ma_long`, kỳ
     vọng `B2-dem-doc 4` loại `kill count 0`; nên 129 hạng mục và 78 hạng mục có (E) không đổi. Trên ứng viên nháp
     bộ này có 89 biến thể ở r7 và **95** ở r8 (kiểm đếm ở B2); số của executor có thể khác nếu cấu trúc mã khác (ví
     dụ không có khối kill dùng chung), và executor khai ánh xạ biến thể → hạng mục.
  2. **Đo.** Mỗi biến thể chạy A1, A2, W1, W0 như một dòng B5. Biến thể hướng thoát/sai/bắt/bọc/đếm/cú pháp: tiêu chí
     y hệt tiêu chí của một dòng B5 (A1 chết bằng `TinHieuChotCa` đúng đích hoặc ở nhãn đứng trước; W1 đúng nhãn,
     tiểu nhãn, loại; W0 sống, bộ đếm ≥ 1). Biến thể hướng thay thế: ca ĐỎ ở A1, W1 và cả W0 bằng lỗi vô can (không
     lọt, và nới nhãn không che được); đó là hạng "đỏ vô can theo thiết kế", không tính giết thật. Sáu đối chứng của
     luật `B2-parse`: đỏ vô can ở A1, W1 và W0. Hai đối chứng sống: cả hai ca SONG, D xanh, VÀ nhân chứng dương của
     mục 5 đúng — thiếu nhân chứng thì đối chứng sống không phân biệt được với bản RỖNG.
  3. **Chỗ đặt và log.** Như D: tập lệnh bằng chứng cục bộ, không thêm ca đăng ký, không sửa runner, không tăng
     `DOT_BIEN`. Log: lệnh nguyên văn, giờ UTC, rc, và mỗi biến thể một dòng (tên, hạng mục của bảng, đích, A1, A2,
     W1, W0, bộ đếm, chấp nhận hay lý do đỏ). **Không nhận bằng chứng B5 là đủ** nếu thiếu (E), hoặc có biến thể
     nào không đúng kỳ vọng.
     **(r8, cross-review lượt 7) Log KHÔNG đủ.** Nộp kèm handoff (i) chính tập lệnh bằng chứng (A/W, D, (E)) và
     (ii) BẢNG biến thể máy đọc được — mỗi dòng: tên, hạng mục, các cặp (neo, thay) trên ứng viên, ca / nhãn / tiểu
     nhãn / loại kỳ vọng — mỗi tệp kèm sha256; reviewer chạy lại chúng trên đúng SHA ứng viên trước khi kết luận.
     Tập lệnh phải ĐỎ với biến thể có neo không xuất hiện ĐÚNG MỘT lần trong ứng viên, hoặc cho ra bản giống hệt
     ứng viên. Lý do đo được: r7 chỉ đòi log, nên răng của 78 hạng mục là một lời khai không ai chạy lại được; và
     bản RỖNG (giống hệt ứng viên) thoả y hệt tiêu chí của hai đối chứng sống — hai ca SONG, D xanh — ở ba Python.
     Đo chốt ở rig r8 (bảng 10 dòng 6): bản RỖNG, neo vắng, neo xuất hiện hai lần ⇒ tập lệnh dựng thoát rc=3, không
     ghi biến thể nào; biến thể hợp lệ ⇒ rc=0.
  4. **Giới hạn khai thẳng (r8 sửa câu "răng BỀN" của r7).** (E) chạy MỘT lần trước merge; nó không nằm trong
     `--dot-bien` nên KHÔNG được đo lại ở các lượt sau. Phép D cũng nằm trong tập lệnh cục bộ và cũng chạy MỘT lần.
     Vậy răng BỀN (đo lại ở mỗi lượt `--dot-bien`) của 78 hạng mục ấy: KHÔNG CÓ. Thứ còn lại sau merge chỉ là
     assertion của hai ca — chạy ở mỗi lượt suite, nhưng không phép nào đo lại rằng chúng còn đỏ được với vi phạm.
     r7 viết "răng BỀN … chỉ là assertion cộng phép D" là sai: D không phải phép đo lặp lại. Một biến thể cho mỗi hạng
     mục cũng không chứng minh mọi cách viết vi phạm hạng mục ấy đều bị bắt.
  5. **Nhân chứng dương cho hai đối chứng sống (r8, cross-review lượt 7).** "Hai ca SONG, D xanh" không phân biệt
     được đối chứng thật với bản rỗng, nên mỗi đối chứng kèm MỘT phép đo chứng tỏ nó thật khác ứng viên: bản danh
     sách trắng ba errno ⇒ `_con_song(os.getpid())` với seam `OSError(errno.ENOMEM, …)` ở `Path.stat` phải THOÁT
     `OSError` errno 12 trong khi ứng viên trả `True`; bản khối K0 tách riêng ⇒ AST của `_con_song` có HAI lời gọi
     `os.kill` (ứng viên: một). Đã đo (ba Python; reviewer lượt 7, và phiên soạn r8 trên rig riêng, bảng 10 dòng 6):
     ENOMEM ⇒ ứng viên `True`, danh sách trắng `OSError errno=12`, bản rỗng `True`; AST ⇒ 1 / 2 / 1.
  Đã đo (phiên soạn r7, rig riêng, ứng viên nháp — KHÔNG phải mã của executor; bảng 9 dòng 6, 7, 11, 12): 87/87 biến
  thể có kỳ vọng chết hay đỏ đều đúng kỳ vọng, hai đối chứng sống thì sống, ở cả ba Python; và trên một helper dựng
  đúng theo HINT lượt 6, 34 trong số ấy lọt hẳn (cả hai ca xanh). Phiên soạn r8 (rig riêng, cùng ứng viên nháp,
  helper r8; bảng 10 dòng 4): bộ 95 biến thể cộng 15 biến thể quét (mười hai quét giải mã — năm cách lỏng và `encoding="utf-8"` tường
  minh, × hai đường — và ba đường/API) — 106/106
  biến thể kỳ vọng chết hay đỏ đều đúng kỳ vọng; bốn biến thể sống thì sống (hai đối chứng sống, và
  `encoding="utf-8"` tường minh ở Đ0 và ở Đ — giới hạn đã khai); ba Python.
  **CHƯA ĐO:** (E) trên mã của executor.

  **Log mỗi dòng biến thể**: tên mục và vị trí, ca đích, nhãn đích và tiểu nhãn (nếu có), loại assertion
  (nếu dòng nêu; r6), A1 (nhãn, tiểu nhãn và loại báo), A2 (sống sót hoặc nhãn Y — đây là "các nhãn khác vẫn giết nó trong ca đầy đủ"; danh
  sách ĐỦ mọi nhãn giết được nó cần nới tuần tự và không bắt buộc), W1, W0 kèm bộ đếm seam.
  Cách làm là khả thi, không phải lời hứa. Đã thấy chạy trên rig của reviewer (bản nháp Q-A, KHÔNG phải
  ứng viên của executor):
  · lượt 2, lượt 3, lượt 4, phiên soạn r5, phiên soạn r6 (nguyên văn ở r6) và cross-review lượt 6 (số ở VERDICT
  lượt 6) — không chép lại (r8, thu gọn);
  · phiên soạn r7 (rig riêng, helper r7 có quy ước đếm theo đường và luật nguồn "hàm + nội dung", ba Python; bảng 9
  dòng 2, 4, 9): năm mươi tư dòng (năm mươi lăm cặp) đều được chấp nhận; kiểm kê 191 / 228 / 3 / 231; runner thật
  cho 53 dòng `giet 1/1`, (c) `giet 2/2`, kết quả `(0, 0)`, không dòng nào in kiểu ngoại lệ trong ngoặc, đối chứng
  `NameError` chết bằng `NameError`;
  · phiên soạn r8 (rig riêng, helper r8 có luật nguồn "hàm + nguyên dòng + số lần" và loại (2) mở rộng, ba Python;
  bảng 10 dòng 2): năm mươi tư dòng (năm mươi lăm cặp) đều được chấp nhận; runner thật và kiểm kê: KHÔNG chạy lại
  ở r8;
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
  D**: lệnh nguyên văn, giờ UTC, rc, dòng xanh của bản đúng cho từng ca đăng ký, và từng dòng trong 65 control (r8; r7: 63)
  (17 mức nhãn, 48 mức tiểu nhãn) cùng các phép đảo thứ tự, kèm đơn vị thiếu; và **log của phép (E)** (B5): mỗi biến
  thể một dòng, kèm ánh xạ sang hạng mục của bảng không gian mở rộng; và phép tính sàn Windows của B4 (lệnh + số). Đính vào handoff; reviewer đọc **trước** merge. Xanh của `gate-registry` KHÔNG thay
  cho log này (§8). Sau merge, `launcher-windows.yml` chạy ở lượt `push` master: đọc kết quả cả
  Windows lẫn Ubuntu (`land_obligation`), kể cả dòng `DOT BIEN:` của bước `Tu dot bien`, đừng suy thành công từ
  việc đã đẩy.
  **ĐỎ khi:** ứng viên có thêm ca đỏ, đột biến cũ đổi hạng, thêm lỗi F, handoff thiếu log nguyên văn cho
  bất kỳ lệnh nào trong B1–B6, hoặc thiếu log phép D, bản đúng không xanh ở D, hay có control của D không
  đỏ; hoặc thiếu log phép (E), hay có biến thể (E) không đúng kỳ vọng; hoặc (r8) thiếu tập lệnh bằng
  chứng, bảng biến thể của (E) hay bảng control của D kèm sha256 (B5 (E) mục 3, D mục 6), thiếu nhân chứng dương
  của hai đối chứng sống ((E) mục 5), hay reviewer chạy lại chúng ra kết quả khác log. Sau merge: `DUOI SAN` ở bước `Tu dot bien`
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

- **Nền nghiệm thu `89fc4fa` vẫn hợp lệ cho write set — đo lại ở r8 (worktree của phiên soạn, HEAD `3915f46`, sạch
  trừ tệp r8 mới).** `git fetch -q origin master` rc=0 (06:14:27Z 30-09, xong 06:14:28Z); `git rev-parse origin/master`
  ⇒ `c16bec639efa0077def4916c25c3e0c17f68dcaa` (Merge PR #693, commit lúc 2026-09-30T05:59:04+07:00) — **không trôi kể
  từ r7** (`git rev-list --count c16bec6..origin/master` ⇒ 0).
  `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py`
  ⇒ **rc=0** (06:14:28Z); cùng lệnh với `-- .claude .github` ⇒ rc=0 (06:14:28Z). `git rev-parse origin/master:<tệp>` ⇒
  blob `561ff7a1840d65a6fc9953947f71cabe4947b3c9` và `abf7f6cafd36c34392a31f6e1b24f3cd63a3c7c8` (giữ nguyên).
  `3915f46` chưa là tổ tiên của `origin/master` (`merge-base --is-ancestor` rc=1). Các số khác của lượt đo r7 — `wc -l`
  4308 / 8354; `89fc4fa..origin/master` 47 commit (37 không merge), 37 tệp, 8953 dòng thêm, 5 xoá, 0 tệp dưới
  `.claude/` hay `.github/` — đo trên CÙNG `c16bec6` nên vẫn là số hiện hành; nguyên văn ở §8 của r7, không chép lại.
  Phép so hai nguồn ref: **KHÔNG làm lại ở r8** (chỉ fetch `master`).
- **Độ dài `_con_song` trên nền** (r7, AST `end_lineno` trên bản sao `launcher.py` của `89fc4fa` trong rig r7,
  02:00:46Z 30-09, Python 3.12.3): dòng 629–672, **44 dòng** (kể cả docstring). Khớp số cross-review lượt 6 đo; §9
  của r6 ghi nhầm "77 dòng (629–705)".

- **Các lượt đo lại nền của r3 đến r7**, ruff của r5 và r6, và phép so hai nguồn ref 516/517 của r3: nguyên văn ở
  §8 của r6 (r3–r6) và của r7 (r7) — không chép lại (r8, thu gọn). Kết luận của cả năm lượt: hai blob write set không
  đổi (`561ff7a1…`, `abf7f6ca…`), `git diff --quiet … -- .claude .github` rc=0 — trùng lượt đo r8 ở trên.
- Kích thước trên `origin/master` (`git show origin/master:<tệp> | wc -l`, 11:49:30Z, khi đó là `1c23933`;
  blob đo lại trùng ở `c57df32` nhờ `git diff --quiet` rc=0 ở trên, và ở `44620e8` lúc 13:07Z; số dòng
  4308/8354 đo lại ở `44620e8`):
  `launcher.py` 4308 dòng (blob `561ff7a1…`, sha256 `808ce5b3…9fc0`); `launcher_test.py` 8354 dòng (blob
  `abf7f6c…`; sha256 tệp `433af9d4…556a`). Blob của cả hai tệp ở `89fc4fa` và ở `origin/master` trùng nhau
  (`git rev-parse <ref>:<tệp>`).
- **Số ca của `launcher_test.py`, đếm bằng AST** (11:10:16Z 29-09, trên `origin/master:.claude/dev/launcher_test.py`;
  đo lại 11:46:05Z bằng probe `inventory` của lượt 2 trên bản sao rig, ra CÙNG số dưới đây; cross-review
  lượt 3 đo lại bằng AST lúc 12:50:02Z (189 ca = 155 `t` + 34 khác, hậu tố lớn nhất 155, không hổng), cùng
  số; phiên soạn r4 đến r8 KHÔNG chạy lại phép đếm AST này (hai tệp giống hệt theo blob, nên số không đổi theo suy ra; r5, r6 và r7 chỉ đếm số ca đăng ký của rig sau khi thêm hai ca: 191 = 189 + 2; B6 trên rig r7 in "tong 189" cho nền và "tong 191" cho ứng viên, bảng 9 dòng 13; lượt 5 đo lại bằng AST ra 189 = 155 `t` + 34 khác, hậu tố lớn nhất 155, không hổng);
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
  ca, 16:46:55Z 29-09, Python 3.12.3, bảng 8). Các kỳ vọng của r3 đến r6 và của HINT lượt 4, lượt 5 (186 / 189 …
  223 / 226): nguyên văn ở §8 của r7 — không chép lại (r8, thu gọn). r7 thay bằng 174 + 54 = 228 (231) vì thêm lớp
  (m) (rig của cross-review lượt 6 đếm ra đúng 228 / 3 / 231 và 191 ca, 00:53Z 30-09; rig riêng của phiên soạn r7
  đếm ra cùng 228 / 3 / 231 và 191 ca, 01:33:28Z 30-09, bảng 9 dòng 4), và r7 KHÔNG thêm dòng nào nữa (B4, B5); r8
  cũng không. Số ca đăng ký không đổi (191). Số nhãn 17; 48 tiểu nhãn + 9 đơn vị đơn = 57 đơn vị
  (r8; r7: 46 + 9 = 55); D có 65 (r8; r7: 63) control (HINT lượt 6: 17; 32 + 9 = 41; 49 — r6: 16; 27 + 9 = 36; 43).
  Phép (E) của r7 và r8 không thuộc `DOT_BIEN` nên không đổi các số 228 / 231.
- **Lease** (SỐ CỦA PHIÊN SOẠN r3 — phiên soạn r4 đến r8 KHÔNG đo lại; chạy trong `/home/user/tra-luat` sau `git fetch` đủ, 29-09; lệnh `python ops/lease_publish.py
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
  `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` (đỏ sẵn; cross-review lượt 6 ghi cùng ca) — bảng 9 dòng 13; cross-review
  lượt 7 đo lại hai vế trong một lệnh, cùng số, delta 0; phiên soạn r8 KHÔNG chạy lại. B6 vẫn bắt executor đo cả hai vế
  trên nền tiếp nối.
- Ruff nền (11:49:59Z, `89fc4fa`, nhị phân `ruff` 0.15.8; `python -m ruff` vắng): `launcher.py` 0 lỗi F,
  `launcher_test.py` 5 lỗi F (F841 ×5). Chi tiết ở B6.

Mọi con số phải được **đo lại** trước cấp lease và trước land (L5).

## 9. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục một lượt thất bại. Hình dạng đáng canh, ghi để lượt thi
hành không lặp: *"vá một lỗ mà mở lỗ khác trong cùng hàm"* / *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ
ba"* — năm lần trước khi r5 được review; lượt 5 đo lần thứ **sáu** (mục 6 dưới đây), và r6 là revision đầu
tiên ĐỔI CÁCH LÀM thay vì vá tiếp: liệt kê toàn không gian trước (mục 6); lượt 6 đo lần thứ **bảy** — chính
phép liệt kê của r6 đã bỏ sót nhánh cũ — và r7 mở rộng phép liệt kê sang MỌI đường (mục 7); lượt 7 đo lần thứ
**tám** — seam thay cả lời gọi — (mục 8). Các mục là lịch sử của cùng một lớp, không phải tám finding độc lập:
1–6. (lần thứ nhất đến thứ sáu của hình dạng, lượt 0 đến lượt 5) nguyên văn ở §9 của r6 — không chép lại (r8,
   thu gọn). Mỗi lần một dòng: (1) bản RỘNG; (2) bản HẸP r1 mất zombie; (3) ba đường không chốt của r2; (4) ba ô
   tầng đọc của r3 và lời khai "A1 khoá mặc định"; (5) chiều kết quả của PID dự phòng; (6) nhóm phân tích ở tầng
   hỏi — và r6 đổi cách làm: liệt kê toàn không gian trước, kèm bộ sinh dãy mệnh đề (giới hạn của nó: §10).
7. **(lượt 6, mới ở r7 — lần thứ BẢY)** nguyên văn ở §9 mục 7 của r7 (sha256 `3fc04fe5…5286`) — không chép lại (r8,
   thu gọn). Tóm tắt: bảng không gian r6 chỉ là tầng của ĐƯỜNG MỚI, bỏ sót hai nhánh sẵn có của Q-A.3 — lỗ ở cấp
   ĐỊNH NGHĨA TRỤC; HINT lượt 6 tự lặp hình dạng ở cỡ nhỏ (34 biến thể lọt helper dựng theo HINT, bảng 9 dòng 7). r7
   chữa theo lớp: không gian từ ĐƯỜNG (30 ô, 129 hạng mục), mỗi hạng mục một chốt đo được (54 dòng B5, 78 hạng mục
   bằng (E)), và khai thẳng giới hạn cứng của cách làm "liệt kê thêm": sàn đột biến Windows (B4: biên 42 → 7 → 4).
8. **(lượt 7, mới ở r8 — lần thứ TÁM)** Bảng không gian r7 định nghĩa hàng theo LỚP ngoại lệ và đo hàng R3 ở hai
   tầng đọc bằng seam thay CẢ lời gọi `read_text`, nên tham số của chính lời gọi đọc (`errors=`, `encoding=`) nằm
   ngoài mọi trục. Hai bản vá theo idiom có sẵn trong `launcher.py` — `read_text(errors="replace")` — hay
   `encoding="latin-1"` ở nhánh tệp có qua hết r7 + D ở ba Python mà đổi kết quả của tiến trình SỐNG có `comm` không
   UTF-8 (kích hoạt thật: tên tiếng Việt bị kernel cắt ở 15 byte). Lần này lỗ không ở định nghĩa trục mà ở ĐƠN VỊ
   của đầu vào: seam đo mệnh đề bắt, không đo phép đọc. HINT lượt 7 chữa bằng hai đầu vào nội dung thật và hai biến
   thể (E), không thêm dòng `DOT_BIEN` — và tự nó lặp hình dạng ở cỡ nhỏ lần nữa: đầu vào thật mới nằm cùng nhãn với
   đích của hai biến thể (E) của r7 nên làm W0 của chúng chết vô can; luật nguồn "nguyên dòng" vẫn giả được bằng bản
   sao y (bảng 10 dòng 4 và 5). Chữa theo lớp ở r8: rà MỌI seam thay cả lời gọi và khai tham số nó che (quy ước chung,
   "Seam thay CẢ lời gọi"); điều kiện dựng cho đầu vào thật; loại ghi nhận (2) mở rộng cho seam chỉ-đếm; luật nguồn
   thêm số lần. Đo đóng: rig r8, ba Python — 55/55 cặp; D 65 control + 6 phép đảo; (E) 106/106 (bảng 10).

Mỗi bản vá/đặc tả đều ĐÚNG và CÓ RĂNG ở chỗ nó phủ; lỗ nằm ở đường KHÔNG ai chỉ. Các phép đo chỉ chứng
minh các đường đã thử. Miền kiểm của r8 gồm ESRCH, EACCES, EPERM, EIO, zombie, ngoại lệ ngoài `OSError`
(`Exception` và `BaseException`) ở cả năm tầng hỏi, đọc mới, kill mới, đọc cũ, kill cũ, nhóm phân tích ở cả năm
tầng (tự nhiên ở hai tầng đọc, sentinel ở tầng hỏi và hai tầng kill), số lần hỏi/đọc/kill theo từng đường, cú
pháp phép tách với `comm` chứa `)` ở cả hai tầng đọc, nội dung THẬT không giải mã được ở cả hai tầng đọc (r8), và **kết quả của bước PID dự phòng (sống, đã `wait`, EPERM,
EIO) cùng số lần gọi `kill(pid, 0)`**; bảng không gian mở rộng ở B2 ghi rõ ô, đầu vào và chốt từng hướng. B2 khoá bản RỘNG và các biến thể tầng đọc, B3/B3b
khoá bản HẸP r1; các lớp còn lại ở B5 khoá những biến thể đã liệt kê. **Không coi một danh sách mutant hữu hạn là bằng
chứng đã liệt kê hết mọi đường**; executor và reviewer vẫn phải kiểm các đường mới xuất hiện trong chính
cách triển khai được chọn.

**Ngưỡng ba lần đã chạm — câu hỏi đặt cho điều phối/chủ kho, r4 đến r8 KHÔNG tự trả lời.** CLAUDE.md dạy đếm
hình dạng lỗi chứ không chỉ đếm lỗi: cùng một hình dạng lặp từ ba lần trở lên thì câu hỏi đúng là "có nên
làm việc này theo cách này không", không phải "vá thế nào". Đường hiện tại (giữ phép hỏi `exists()` rồi
dựng thêm một đường lỗi có đọc + `kill(pid, 0)`, Q-A.1–4) tự nó sinh ra nhiều đường cần chốt — đó là lý do
ma trận ở B2 phình dần từ r1 tới r6 (số dòng biến thể của B5: bảy ở r2, mười hai ở r3, mười lăm ở r4,
mười chín ở r5, bốn mươi chín ở r6, năm mươi tư ở r7 cộng 89 biến thể của phép (E), năm mươi tư ở r8 cộng 95;
số đơn vị assertion: 22 ở r4, 26 ở r5, 36 ở r6, 55 ở r7, 57 ở r8). Bước nhảy 19 → 49 của r6
KHÔNG phải vì có thêm 30 đường lỗi thật: nó là giá của việc liệt kê đủ 15 ô × hai hướng thay vì vá theo
finding, và chính con số ấy là bằng chứng cho câu hỏi của ngưỡng — một đường thiết kế mà nghiệm thu cần 49
đột biến để khoá phạm vi bắt của một hàm dài 44 dòng trên nền (dòng 629–672, kể cả docstring; AST `end_lineno`, đo lại ở cross-review lượt 6
và ở phiên soạn r7, §8 — r6 ghi nhầm "77 dòng (629–705)") là một đường tự sinh
đường. r7 thêm hai dữ kiện định lượng cho câu hỏi ấy: nghiệm thu nay cần 129 hạng mục cho cùng hàm 44 dòng, và
sàn đột biến Windows chặn cứng việc đưa chúng vào `DOT_BIEN` (B4) — nên phần lớn răng của r7 (78 hạng mục) chỉ đo
được MỘT lần, bằng phép (E), không được đo lại ở các lượt sau. Có thể cân nhắc một cấu
trúc ít đường hơn (ví dụ dùng chính phép đọc làm phép hỏi), nhưng nó đổi hành vi nhánh cũ mà Q-A.3 cấm đổi, và
r4 đến r8 chưa đo phương án nào. r8 thêm một dữ kiện: lần thứ tám không nằm ở ô hay trục còn thiếu mà ở CÁCH ĐO một
ô đã có (ghi chú của reviewer lượt 7) — thêm ô không trả lời được câu hỏi ngưỡng. Nên r8 giữ hướng của r2 đến r7 và
chỉ nêu ngưỡng; có hỏi lại quyết định gốc hay không là việc của điều phối/chủ kho (§11).

## 10. `chua_do_duoc`

- Suite `launcher_test.py` và `--dot-bien` trên nền: các phiên soạn r3 đến r7 đã chạy gì (probe, rig sao chép, rig
  riêng, suite hai vế ở r7) — nguyên văn ở mục này của r7 (sha256 `3fc04fe5…5286`), không chép lại (r8, thu gọn).
  Không phiên soạn nào chạy `--dot-bien` trên 174 đột biến cũ; câu "không đột biến cũ nào đổi hạng" của B6: KHÔNG
  ĐO ĐƯỢC ở r3–r8 (cross-review lượt 7 đo được trên ứng viên nháp của họ: 177 mục cũ cùng hạng nền — VERDICT lượt 7,
  hướng 11 — không phải trên mã của executor). **Phiên soạn r8 có chạy** (06:10Z–06:23Z 30-09) một rig riêng (bảng
  10): hai ca dạng prototype với helper r8, 54 dòng, 110 biến thể (E) và quét, phép D, nhân chứng dương, trục N, điều
  kiện dựng, đầu-cuối 124 — KHÔNG chạy suite đầy đủ, runner thật hay `--dot-bien`.
- Ruff: đo được **nền** (§8, B6: `launcher.py` 0, `launcher_test.py` 5, nhị phân `ruff` 0.15.8; cross-review
  lượt 3 đo lại ra cùng số, đúng năm F841 ở dòng 2566, 3387, 3629, 4110, 6061); delta của ứng viên: chưa có
  ứng viên. `python -m ruff` vắng trong container soạn r3 (và trong sandbox của cross-review). Phiên soạn r4
  không chạy ruff; phiên soạn r5 và r6 chạy lại nhị phân `ruff` 0.15.8 trên blob nền (§8; r6 lúc 16:59:41Z) ra cùng số;
  phiên soạn r7 và r8 KHÔNG chạy ruff (blob nền không đổi, §8; số F của helper r7, r8 trên rig: KHÔNG ĐO ĐƯỢC).
  Cross-review lượt 7 chạy nhị phân `ruff` 0.15.8 trên bản sao ngoài cây: nền cùng năm F841, ứng viên nháp và helper
  của họ cùng năm (VERDICT lượt 7, hướng 5).
- Nhánh Windows và Darwin: không đo (Q4); lần đo Windows đầu tiên là lượt push master sau merge. Các
  bảng ở §1 chỉ đo Linux, Python 3.12.3 cho bảng 3, 4, 5 và 6; bảng 7 đo ba Python 3.11.15, 3.12.3, 3.13.12, bảng 8
  đo ba Python cho phép A/W, D và runner, nhưng bộ sinh dãy dài (ba mệnh đề) chỉ chạy ở 3.12.3; bảng 9 đo ba
  Python cho A/W, D và (E), còn luật nguồn, phép so với helper HINT, chữ ký, runner, sàn và B6 chỉ ở 3.12.3; bảng 10
  đo ba Python cho mọi dòng trừ chốt tập lệnh (dòng 6), thứ tự "đếm trước" (dòng 9) và đầu-cuối (dòng 10), chỉ ở
  3.12.3.
  **Sàn đột biến Windows (B4): số THẬT trên Windows KHÔNG ĐO ĐƯỢC trước merge** (Q4); số của r7 là ước lượng tĩnh
  cận dưới, biên 4 mục. Bảng 4 chỉ đo locale UTF-8 (`preferred_encoding`
  `utf-8`, và `LC_ALL=C.UTF-8`); r8 đo thêm điều kiện dựng ở locale ASCII (bảng 10 dòng 7); locale khác (Latin-1,
  …): KHÔNG ĐO ĐƯỢC — container chỉ có `C`, `C.utf8`, `POSIX`. Cross-review lượt 3 mô phỏng hai
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
  đường cũ của `B3-zombie` dùng `stat`, phép đọc và `kill` THẬT; hai đầu vào r8 (`utf8-hong-that`, `B2-dem-doc 4`)
  dùng nội dung THẬT — tần suất `comm` như thế ngoài thực tế: KHÔNG ĐO ĐƯỢC.
- Bản "r2" trong bảng §1 là bản nháp của phiên soạn (Q-A.1–4); chưa có bản vá của executor nào được đo với
  B1–B6. Các hàng "biến thể" của bảng 3 và bảng 5 là đột biến do reviewer lượt 2 và lượt 3 dựng, còn bảng 6
  do reviewer lượt 4 (mutant bỏ hỏi PID) và phiên soạn r5 (k2–k4) dựng; không hàng nào là bản của executor.
- **Chốt ngược A1/A2/W1/W0 và phép D (B5)**: số của lượt 3, lượt 4 và các phiên soạn r5, r6, r7 (13 → 27 → 32 → 43
  → 63 control) nguyên văn ở mục này của r7, không chép lại (r8, thu gọn). Phiên soạn r8 (06:16Z–06:21Z 30-09, ba Python)
  dựng lại trên rig RIÊNG với helper r8 17 nhãn / 57 đơn vị: 55 cặp (54 dòng) được chấp nhận, D đủ 65 control (17
  nhãn + 48 tiểu nhãn), sáu phép đảo thứ tự đều đỏ, 106/106 biến thể (E) và quét đúng kỳ vọng (bảng 10). **CHƯA ĐO**,
  bao gồm: năm mươi tư dòng (không đổi từ r7; năm mươi lăm cặp đích) và phép (E) trên mã của ứng viên nào; tập lệnh bằng chứng của executor; tiểu nhãn báo trong thông
  điệp giết theo ĐÚNG chuỗi của đặc tả này (helper lượt 3 dùng tên nhãn phụ và tên đầu vào khác — `B2-read-ESRCH`,
  `access`/`io`/`read-error`, `empty`/`no-close`/`end`/`space`/`decode` — helper lượt 4 và helper mở rộng
  của r5 đã dùng tiểu nhãn của đặc tả, nhưng đó vẫn là helper của reviewer, không phải của executor; helper của
  r6, r7 và r8 là helper của phiên soạn, cũng không phải của executor); và bản
  thân hợp đồng helper ở §7 — lời văn của r3–r8, chưa có cài đặt của executor nào. Mặc định "không nới"
  của helper phải đo riêng bằng D và control test-only ở B5; A1 có chốt phủ giao nhau nên không chứng minh
  được điều này một mình.
- **Bất đối xứng hai đường về nội dung hỏng** (§2, §3): nhánh cũ trả `False`, nhánh mới rơi về `kill`. Đo
  được rằng nhánh cũ báo "đã chết" cho một PID sống có `comm` không phải UTF-8; chưa tìm Issue cho việc
  này, tần suất ngoài thực tế KHÔNG ĐO ĐƯỢC; điều kiện kích hoạt thật thì đo được (r8, lượt 7: tên
  tiếng Việt bị kernel cắt ở 15 byte), và hệ quả tới mã 124 khi còn sống (§2). Packet này không sửa (câu hỏi cho chủ
  kho ở §11), và không có ca nào khẳng định nhánh cũ đúng.
- Nội dung Mission #686 (Q0–Q5), comment `5888633201`, object ID `5628902742`, trạng thái lease #668
  live: phiên soạn không đọc lại từ GitHub; là lời khai của điều phối (số ở §8 đến từ `ai-dang-giu` chạy
  trên ref đã fetch ở r3, không phải từ GitHub live). Băm thân Issue: KHÔNG ĐO ĐƯỢC. ID comment PR #688
  chứa VERDICT lượt 2 (`5889523704`, đăng 11:40:59Z), lượt 3 (`5890856046`), lượt 4 (`5891961732`, đăng
  14:07:48Z), lượt 5 (`5894035533`, đăng 16:09:51Z), lượt 6 (`5902146149`, đăng 01:16:56Z 30-09) và lượt 7
  (`5905120228`, đăng 06:01:02Z 30-09) là dữ kiện điều phối cấp; phiên soạn r4 đến r8 không kiểm chúng trên GitHub;
  giờ đăng comment lượt 3 đến lượt 7 do phiên điều phối đọc qua REST. Họ model của reviewer lượt 6 và lượt 7 (Claude
  Opus 5.5) là tự khai trong VERDICT, không có phép đo máy: KHÔNG ĐO ĐƯỢC. Quy ước review từ r8 (ô `quy_uoc_review`)
  là dữ kiện điều phối cấp: KHÔNG ĐO ĐƯỢC từ phiên soạn. (Bản r3
  của mục này ghi ID lượt 2 là "KHÔNG có" trong khi `nguon_cap_viec` của chính r3 đã điền nó; r4 sửa cho
  khớp.)
- Lease và ref: phiên soạn r4 đến r8 KHÔNG đo lại các số lease (người giữ `launcher.py` 0, `launcher_test.py` 1, hạn
  `2026-09-30T07:41:00Z`) và KHÔNG so lại hai nguồn ref (516/517) — chỉ fetch `master` để đo nền. Cross-review
  lượt 3 không có ref và object lịch sử của lease #668 trong clone của họ (chỉ 4 ref nhánh; `cat-file -e
  2ae5646^{commit}` rc=128) nên cũng KHÔNG ĐO ĐƯỢC các số ấy; đừng suy "người giữ 0" từ một tập ref chưa so
  hai nguồn (cross-review lượt 4 và lượt 5 cũng báo bundle chỉ có 4 ref nhánh và object `2ae5646` vắng, rc 128;
  lượt 6 báo object `2ae5646` vắng, rc 128; lượt 7 báo mirror không có nhánh lease). Hạn `2026-09-30T07:41:00Z` của
  lease #668 là số đọc ở r3; nó có thể đã qua hoặc sắp qua lúc cấp lease cho `wp685` — trạng thái hiện hành: KHÔNG ĐO
  ĐƯỢC ở r8. Đo lại lúc cấp lease.
- Phép đo `t154` của B7: chỉ có số của reviewer trên bản nháp — lượt 2 (nền ném `ProcessLookupError` sau 1 lần
  chạm seam; bản dựng qua, 31 lần chạm, 4,87 giây) và lượt 3 (12:50:55Z: nền 1 lần chạm, 1,43 giây; bản dựng
  qua, 31 lần chạm, 5,136 giây) và lượt 4 (rig khác: 54 lần chạm, 4,938 giây, seam bơm lỗi đúng một lần — phép đo
  khác, không phủ định 31) — phiên soạn r3 đến r8 không chạy lại, và không có ứng viên của executor
  để chạy.
- Toàn bộ 174 đột biến cũ (`--dot-bien`): KHÔNG ĐO ĐƯỢC ở các phiên soạn r3–r8 (cross-review lượt 7 đo trên ứng viên
  nháp của họ: cùng hạng nền, xem mục đầu của §10). Lượt 3, lượt 4, lượt 5 và phiên soạn r5 chỉ đếm
  được rằng số mỏ neo của 174 mục cũ không đổi (count changes rỗng); lượt 6 đếm lại trên ứng viên nháp của họ (0
  mất, 0 lệch, 0 neo trong `_con_song`); phiên soạn r6 và r7 không đếm lại — đếm mỏ neo không thay bằng chứng ấy.
  B6 toàn suite: KHÔNG ĐO ĐƯỢC ở r3–r6; phiên soạn r7 đo trên ứng viên NHÁP với helper r7 (delta 0, bảng 9 dòng
  13), cross-review lượt 7 đo lại hai vế trong một lệnh (delta 0), r8 không chạy — không phải phép đo trên mã của
  executor.
- Tổng số ca `launcher_test.py` và số mục `DOT_BIEN` sau packet: chưa đo trên ứng viên nào của executor (kỳ vọng
  ở §8 và B5: 191 ca đăng ký; 228 mục `DOT_BIEN` sản phẩm, 231 kèm `DOT_BIEN_HARNESS`; 57 đơn vị assertion và 65 (r8; r7: 55 / 63)
  control của D đếm từ bảng tiểu nhãn; HINT lượt 6: 41 / 49; r6: 223 / 226 / 36 / 43). Trên rig sao chép của
  phiên soạn r6 (prototype, xem bảng 8) đếm ra đúng 191 / 223 / 226, và trên rig riêng của phiên soạn r7 đếm ra
  191 / 228 / 231 cùng 17 nhãn / 46 tiểu nhãn / 55 đơn vị (bảng 9 dòng 4), trên rig riêng của phiên soạn r8 ra 17
  nhãn / 48 tiểu nhãn / 57 đơn vị / 65 control (bảng 10 dòng 3); đó không phải phép đo trên mã của executor. Các số r4 (15 mục, 16 cặp, 22 đơn vị,
  27 control) và số r5 (19 mục, 20 cặp, 26 đơn vị, 32 control; 193 / 196 sản phẩm) trong bảng lịch sử và log
  cũ, cũng như số HINT lượt 5 (20 mục, 21 cặp, 27 đơn vị, 33 control; 194 / 197), không phải tổng nghiệm thu của r6.
- **Số của r5 và r6** chỉ có trong rig tạm của hai phiên soạn ấy, KHÔNG tái lập được từ kho: nguyên văn ở §10
  của r6 — không chép lại (r8, thu gọn).
- **Số của r7 cũng chỉ có trong rig tạm của phiên soạn** (thư mục `mktemp -d` trong scratchpad của phiên soạn, ngoài
  kho: bản sao `.claude/dev/` của `89fc4fa`; ứng viên nháp trùng byte ứng viên nháp của reviewer lượt 6; helper r7;
  54 tệp đột biến; 89 tệp biến thể (E); bản sao helper r7 của reviewer lượt 6 để so; tập lệnh A/W, D, (E), luật
  nguồn, chữ ký, runner, sàn, B6). **KHÔNG tái lập được từ kho**; dựng lại từ đặc tả này là đủ; không phải mã của
  executor. Mọi con số ở bảng 9 mang nhãn "rig r7".
- **Số của r8 cũng chỉ có trong rig tạm của phiên soạn** (`mktemp -d` trong scratchpad, ngoài kho: nền `git archive`;
  ứng viên nháp trùng byte ứng viên nháp r7; helper r8; 54 tệp đột biến; 110 tệp biến thể (E) và quét, bảng biến thể
  sha256 `46103809…8cb6`; ứng viên C2 và hai bảng khai dòng; tập lệnh A/W, D, (E), nhân chứng, điều kiện dựng, trục N).
  **KHÔNG tái lập được từ kho**; mọi con số ở bảng 10 mang nhãn "rig r8"; không phải mã của executor.
- **Luật nguồn của `B2-parse` phụ thuộc lời khai của executor** (tên hàm, NGUYÊN VĂN các dòng tách và số lần, r8).
  Đo (cross-review lượt 7, và rig r8 bảng 10 dòng 5): biểu thức tách viết hai dòng — luật chuỗi con của r7 làm (l17)
  chết vô can; khai đủ hai dòng ⇒ (l15), (l17) chấp nhận; khai thiếu dòng `[0]` ⇒ (l17) chết vô can (lời khai sai
  làm ca đỏ, không cấp tín dụng giả). Cách viết khác (tách trong hàm trợ giúp, trong comprehension hay generator —
  `co_name` khác theo bản Python), và bản sao y dòng tách đặt trong một hàm cùng tên (a) ở một tệp KHÁC (luật đếm
  theo tệp của khung nên không thấy): KHÔNG ĐO ĐƯỢC (chưa dựng).
- **Răng của bộ sinh chỉ tới ngữ pháp của nó.** Bảng 8 báo 0 lỗ trên các dãy mệnh đề bộ sinh dựng; điều đó KHÔNG
  chứng minh mọi cách viết đều bị bắt. Không phủ: kiểm tra dữ liệu thay bắt ngoại lệ ngoài (l16); tên lớp con
  cụ thể của `OSError`/`Exception`/`BaseException` (ví dụ `TimeoutError`, `MemoryError`); errno thứ năm trở đi;
  mệnh đề `finally`; mệnh đề `else` gắn sai; mở rộng khối `try` sang câu lệnh khác. Mỗi cái là **KHÔNG ĐO ĐƯỢC**.
  Cũng ngoài ngữ pháp ấy, và r6 KHÔNG khai: nhánh cũ (cột Đ0) và quyết định tệp vắng; hỏi/đọc lại có điều kiện
  theo lớp ngoại lệ; cú pháp phép tách với `comm` chứa `)` — cross-review lượt 6 dựng được bản vá qua hết r6 + D +
  toàn suite ở cả ba chỗ; r7 phủ bằng bảng không gian mở rộng (B2), `B2-nhanh-cu` mười chín đầu vào, quy ước đếm
  theo đường, lời gọi đường cũ của `B3-zombie`, lớp (m) và phép (E). Tham số của chính lời gọi đọc cũng ngoài ngữ
  pháp ấy (lượt 7); r8 phủ bằng hai đầu vào nội dung thật và mục "Seam thay CẢ lời gọi" của quy ước chung.
- **Răng của phép (E) chỉ tới MỘT biến thể mỗi hạng mục, và chỉ MỘT lần.** 78 hạng mục của bảng không gian mở rộng
  có biến thể (E) chứ không có mục `DOT_BIEN`: răng của chúng được đo một lần trước merge trên mã của executor, rồi
  KHÔNG được `--dot-bien` đo lại ở các lượt sau (B4, B5). Một biến thể mỗi hạng mục không chứng minh mọi cách viết
  vi phạm hạng mục ấy đều bị bắt. Răng riêng của `B3-song` và `B3-da-wait` (không biến thể nào lấy làm đích):
  KHÔNG ĐO ĐƯỢC.
- (r8) Hai đầu vào nội dung thật (`B2-nhanh-cu utf8-hong-that`, `B2-dem-doc 4`) chỉ đo MỘT dạng nội dung không giải
  mã được (UTF-8 bị cắt giữa ký tự). Điều kiện dựng đo được ở UTF-8 mode và ở locale ASCII (bảng 10 dòng 7); locale
  giải mã được 15 byte ấy: KHÔNG ĐO ĐƯỢC (khi đó điều kiện dựng biến ca thành lỗi thường, không đỏ giả). Tham số giải
  mã: mười hai cách lỏng đo được (bảng 10 dòng 4); `encoding="utf-8"` hay `errors="strict"` tường minh: KHÔNG ĐO ĐƯỢC
  bằng hành vi ở UTF-8 (trùng hành vi); `newline`: suy luận, không đo; cách khác mười hai cách đã dựng: KHÔNG ĐO ĐƯỢC.
- (r8) Kích thước: r8 ngắn hơn r7 cả về số dòng lẫn số byte (r7: 2043 dòng, 264 115 byte; bản chỉ-HINT: 1869 dòng,
  238 466 byte). Số chính xác của r8 không ghi trong chính tệp (ghi vào thì số tự đổi); đo bằng `wc -lc` trên tệp đã
  đóng băng. Băm: phiên soạn r8 đo `VERDICT.md` và `HINT.patch` của lượt 7 và r1 đến r7 bằng `sha256sum` lúc
  06:34:06Z (lần đầu trước khi áp HINT, 06:00Z–06:01Z) 30-09, khớp cả chín.
- PID con đã `wait` bị hệ điều hành tái dùng giữa lúc `wait` và lúc đo: xác suất KHÔNG ĐO ĐƯỢC. Khe này có
  sẵn ở `B1` và `B3-da-wait` và không do r5 mở ra; ở `B2-pid-du-phong` `da-wait`, nếu PID bị tái dùng thì
  `kill(pid, 0)` thật thành công và ca báo `TinHieuChotCa` cho một bản ĐÚNG (dương tính giả); 8 lời gọi
  chạy sát nhau, không có lần `wait` nào chen giữa. Chạy lại là cách phân biệt; ca không khoá được khe này.

## 11. Câu hỏi mở — chủ kho trả lời TRƯỚC khi cấp lease (r8)

1. **Lớp "đọc lỗi ⇒ coi như đã chết" ở `:359` (`_khoa_danh_tinh`) và `:436`/`:490` (`_thanh_vien_nhom`, `_chup_cay`)**
   (cross-review lượt 7, lớp `ngoai-pham-vi-doc-loi-thanh-124`). Phép đo ở §2: tên chương trình tiếng Việt bị kernel
   cắt ở 15 byte làm `comm` không giải mã được; `launcher.py run --deadline-utc` khi ấy trả **rc=124**,
   `giet_tron_ven=True`, trong khi con VẪN SỐNG — ở nền và ở ứng viên nháp như nhau (§1 bảng 10 dòng 10); nếu `comm`
   hỏng ngay lúc sinh thì rc=10 và con cũng còn sống. Bản vá của packet này không gây ra lỗi ấy. Câu hỏi: **sửa ở
   packet này** (cần revision mới: mở rộng Q-A sang các phép đọc ấy, thêm đầu vào và phản chứng đầu-cuối 124/125;
   write set không đổi), **hay mở packet riêng** (đặc tả này giữ nguyên phạm vi)? Đặc tả này KHÔNG tự chọn, KHÔNG mở
   rộng write set hay Q-A; mặc định là không sửa ở đây (§5). Tần suất ngoài thực tế: KHÔNG ĐO ĐƯỢC.
2. Ngưỡng ba lần của hình dạng "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba" — nay tám lần (§9): có hỏi lại quyết
   định gốc (cấu trúc của đường lỗi mới) hay không. Câu hỏi đã nêu từ r4; r8 chỉ thêm dữ kiện, không tự trả lời.
3. Cân bằng `DOT_BIEN` và phép (E) (B4): giữ 54 dòng và đo 78 hạng mục bằng (E) một lần, hay chấp nhận thu hẹp sàn
   đột biến Windows. Câu hỏi đã nêu từ r7; r8 không đổi cân bằng.
