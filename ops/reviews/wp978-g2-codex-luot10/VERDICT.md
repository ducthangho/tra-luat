Verdict: approve
Reviewed commit: db2c1f50bee7c866ad9bea01a3895842bd85cb69
Spec sha256: 9fe94ad05cc1129e663cf77706db92685d6130c08c6a375454781a9aca188060

**P0=0, P1=0, P2=0; P3=3 điểm thiếu độ phủ**, cùng nợ `wp978-git-reader-differential-fuzz`, owner `ducthangho`. Áp ngưỡng assignment lượt 10: survivor không tương đương nhưng sản phẩm vẫn đúng thuộc P3, không chặn approve. **55/55 F13 GIET đúng c62 và 6/6 B2 GIET đúng c53_wd_passed**: 61 baseline rc0 và 61 mutant rc3 đúng marker. Không HONG, TIN_DUNG_GIA hoặc SONG_SOT trong tập 61 mục chuẩn. [Receipt](mutants.json), [tổng hợp](mutants-summary.json).

Ba thay đổi giữ cùng fixture, kỳ vọng và kết quả trên miền đã đo. Linux, ba cặp chạy trực tiếp `--mot-ca c62_git_commit_khong_utf8`: median **6,569 s → 2,106 s**, giảm **67,94%**. Không suy ra số Windows. **N3′ not_run; N6 not_measured; N7 không áp dụng.** Approval chỉ neo SHA dòng 2, không thay suite mặc định/CI trên exact head và không cấp quyền push, merge hay land.

**ĐỐI CHIẾU LƯỢT TRƯỚC**

Đã đọc [verdict lượt 9](../tham-chieu/luot9-VERDICT.md). Tự đo HEAD detached, parent `aebc808ea45408c827e753827b97f94689969db5`, origin/master `9091cf52cf20ac197c1a356d6a33cac6bab0b318` và băm spec: đều khớp. Tree head **3676c40ebb324a0252beed5f4731ca2186fdabf8**. Diff parent..head đúng một tệp test, **+20/-4**, chỉ thân c62; sản phẩm byte-identical parent. Diff master..head đúng hai tệp, **+185/-6**, trong trần kích thước. Assignment lượt 10 là chỉ thị cụ thể để xét tối ưu thân ca; không tự sửa spec đóng băng. [Preflight/diff](preflight.json), [AST và đối chiếu](semantic-audit.json).

| slug | hạng | file:dòng | phép đo | hướng vá / duy trì |
|---|---|---|---|---|
| `mutation-target-prefix-collision` | P1 cũ, giữ đóng | `ops/ci_provenance_test.py:1071`, `:1852` | c53/c62 mỗi tiền tố đúng một ca; mọi đích của 398 mutant khớp duy nhất. 55 F13 và 6 B2 đều GIET đúng ca, bằng lượt 9. | Giữ tên c62 và đích F13; kiểm tính duy nhất khi thêm ca, không đổi B2. |
| `git-reader-fixture-domain-incomplete` — S01/S02 | P3 cũ, giữ đóng hai biểu hiện | `ops/ci_provenance_test.py:1123` | `F13_bo_hai_cham_ten`, `F13_gap_backslash`: baseline rc0, mutant rc3/DO:c62. Corpus/kỳ vọng giữ nguyên. | Giữ nhân chứng trong nợ **wp978-git-reader-differential-fuzz**, owner **ducthangho**; không tuyên bố vét hết grammar. |
| `git-reader-oracle-coverage-unlocked` | **P3** | `ops/ci_provenance_test.py:1168` | Bỏ mục đầu hoặc SHA-256 cuối khỏi vòng so: **parent rc0, head rc0**. Không phải phép kiểm từng đỏ nay mất tác dụng. [Head đầu](variant-skip-oracle-first-head.json), [parent đầu](variant-skip-oracle-first-parent.json), [head cuối](variant-skip-oracle-sha256-head.json), [parent cuối](variant-skip-oracle-sha256-parent.json). | Nợ **wp978-git-reader-differential-fuzz**, owner **ducthangho**. Kiểm độc lập sổ các mục thực sự đã so với danh sách fixture dict và SHA-256; khóa bằng mutant bỏ đầu/cuối. Chỉ đếm `nat` chưa đủ. Rủi ro: nhầm số OID duy nhất với số mục hoặc lấy kỳ vọng từ chính vòng bị cắt; giữ kiểm trong bộ nhớ để tránh thêm Git mỗi mục. |
| `git-reader-write-receipt-assertion-unlocked` | **P3** | `ops/ci_provenance_test.py:1149` | Bỏ chốt `ghi == ...`: rc0. **Không tương đương**: sửa byte riêng fixture âm số 25, giữ chốt ⇒ rc3; cùng sửa byte và bỏ chốt ⇒ rc0. OID dự tính vẫn đúng cho byte ban đầu; object ghi có OID khác, reader đọc OID thiếu trả None nên `kq == mong` xanh. [Bỏ chốt](variant-remove-oid-assertion.json), [có chốt](extra-negative-byte-change.json), [không chốt](extra-negative-byte-change-no-oid-assert.json). | Nợ **wp978-git-reader-differential-fuzz**, owner **ducthangho**. Giữ chốt hiện có; thêm kiểm test độc lập tiêm sai receipt/byte fixture âm và đòi tín hiệu chốt. Mutant gỡ chốt phải làm kiểm ấy đỏ. Rủi ro: dùng riêng fixture dict sẽ để phép so reader che việc gỡ chốt; không coi hai lỗi kết hợp là lỗi đang có trên head. |
| `git-reader-negative-fixture-existence-unchecked` | **P3** | `ops/ci_provenance_test.py:1097`, `:1159` | Bỏ fixture âm khỏi `cho` vẫn rc0: danh sách OID đối chiếu cũng bị rút cùng phía. Xóa object số 25 sau ghi: parent/head đều rc0. Bỏ ghi đúng fixture ấy trong `cm` cũ cũng rc0. Xóa object dict số 0: cả hai rc3. [Bỏ hàng đợi](extra-negative-omitted-from-queue.json), [head](variant-delete-none-object-head.json), [parent](variant-delete-none-object-parent.json), [bỏ ghi trên parent](extra-negative-not-written-parent.json). | Nợ **wp978-git-reader-differential-fuzz**, owner **ducthangho**. Xác nhận sự tồn tại/loại/byte của các object được dựng, kể cả fixture None, bằng một batch độc lập với reader; khóa bằng mutant bỏ ghi fixture âm. Rủi ro: đòi tồn tại cả đầu vào cố ý thiếu hoặc dùng fsck với parent tổng hợp chưa có object; chỉ kiểm nhóm fixture được dựng, tránh spawn từng object. |

P3 ở đây là độ hở TEST dưới biến đổi có chủ ý; không phải lỗi sản phẩm, kỳ vọng sai trên head hay tín dụng giả của 61 mutant chuẩn. Trên **head chưa đột biến**, toàn bộ commit dựng được đã được đọc lại, không thiếu/sai byte. Bỏ mục oracle và thiếu object âm đều tái hiện trên parent; việc lượt 9 chưa ghi nhận chúng không biến chúng thành hồi quy của diff này.

**Tương đương ngữ nghĩa**

Capture parent/head đều **rc0**: cùng **616 mục SHA-1 + một mục SHA-256**, cùng thứ tự OID, kỳ vọng và kết quả. Digest chung `627d04cf3db3ab6634b5dc5f52a71bb147b7090d757695566d4ba36c5a0dda02`. Có **607 lượt ghi commit**: 597 thường, 9 literal, 1 SHA-256; **598 OID duy nhất**, đọc lại **598/598 đúng byte** bằng Git. Không gọi số lượt ghi là số object duy nhất. [Head](capture-head.json), [parent](capture-parent.json), [tổng hợp head](capture-head-summary.json), [parent](capture-parent-summary.json).

- **Ghi batch:** công thức `commit <số byte>\0<payload>` khớp Git; 597 lượt thường được flush trước blob/tag, reader và oracle. Literal vẫn ghi lẻ. Thứ tự ghi giữa nhóm thường/literal đổi, nhưng không có reader chạy giữa hai nhóm; multiset `(OID, raw bytes)` giữ nguyên. Bộ đếm LF streaming độc lập xác nhận **597/597** kỳ vọng M1 của nhóm thường. [Đối chiếu](semantic-audit.json), [từng mục](stream-m1.json).
- **Oracle batch:** 455 lệnh log riêng thành hai lệnh. Git gộp OID trùng; map có đúng **446/446 OID duy nhất** cần kiểm, vòng so vẫn có **455 mục**. `%P` giữ thứ tự và parent trùng trong fixture. Ghép theo `%H` nên không phụ thuộc thứ tự dòng. Đảo thứ tự/loại OID trùng khỏi đầu vào vẫn rc0. [Đối chứng](variant-reversed-dedup-native-input.json).
- **Root và `%P` rỗng:** **44 mục dict có parents=[]** thực sự nằm trong oracle. NUL không bị `.strip()` xóa; dòng cuối `%H\0%T\0` vẫn có ba trường với `p=''`, rồi thành `[]`. Đưa root ra cuối vẫn rc0. Xóa key native hoặc bỏ dòng root ⇒ rc3. `nat.get(x)` thiếu key không thể được nhận nhầm là kỳ vọng None: vòng so chỉ lấy dict và SHA-256. [Root cuối](extra-native-root-last.json), [thiếu key](variant-missing-native-key.json), [thiếu root](variant-missing-native-root.json).
- **Dùng lại kq:** cùng đầu ra reader đã đo và so với `mong`, không đổi OID/chỉ số. Reader hiện tại không giữ cache/trạng thái giữa lần đọc; test gốc không đổi object giữa lần đo và oracle. Thay mọi mục bằng `kq[0]` ⇒ rc3. Parent gọi `doc` cả trong f-string thông điệp, nên trước đây mỗi mục oracle đọc thêm hai lần. [Sai chỉ số](variant-cached-result-wrong-index.json).

Đây là kiểm chứng hữu hạn trên corpus hiện có, không phải chứng minh cho reader tùy ý có trạng thái hoặc mọi grammar Git. Không chạy lại 1.440 mẫu graph/fsck của lượt 9; không nhận số cũ thành phép đo mới. Parent tổng hợp của fixture không tạo graph đủ object, nên không khai fsck sạch.

**Đường dẫn và byte**

Nguyên c62 với `core.autocrlf=true`, `user.useConfigOnly=true`, logOutputEncoding khác mặc định và TMPDIR có khoảng trắng, Unicode hoặc backslash đều **rc0**, qua cả chốt OID và oracle. `write_bytes` không chuyển newline; phép đo xác nhận Git 2.43.0 ở đây không đổi byte commit qua `hash-object -t commit --stdin-paths`. [Cấu hình](autocrlf.gitconfig), [autocrlf](extra-autocrlf.json), [space](extra-path-space.json), [Unicode](extra-path-unicode.json), [backslash](extra-path-backslash.json).

Tên tệp đi qua stdin từng dòng, không qua shell. Backslash trên Linux chỉ kiểm cách đọc tên không đặt trong dấu nháy ở môi trường này; **không kiểm Windows native/đường dẫn ổ đĩa Windows**. Số 482 s/186 s và bản Git for Windows của executor chưa được reviewer đo. Không suy Linux thành bảo đảm Windows. Hướng kiểm path thoát cây chỉ mô tả: kiểm bộ phân giải từ chối tên trỏ ngoài thư mục fixture; phiên này không soạn/thực thi payload đó.

**Răng và đột biến bổ sung**

Gọi chính `chay_dot_bien(*d)` cho từng F13/B2, giữ baseline và tiến trình con của runner. [Script](checks.py) lưu rc, stdout/stderr, neo/thay, ca đích. Parent/head đều **62 ca/398 mutant**, mọi tuple mutant giống nhau; master **61/343**. Ngoài c62, AST các hàm/class test giữ nguyên. Có 39 mục khai báo F13 mở rộng thành 55 mutant; không đếm số dòng thay số chương trình. [Catalogue](static.json), [so sánh](semantic-audit.json).

Classifier tự kiểm vẫn phân đúng lỗi vô can thành `TIN_DUNG_GIA`, thêm chú thích thành `SONG_SOT`; không cộng vào 61 mục. Caveat tên `F13_cha_chi_40` của lượt 9 giữ nguyên: catalogue chết vì parent lỗi/UnicodeDecodeError, không dùng tên làm bằng chứng. Biến thể giới hạn parent 40 ký tự đúng nghĩa chạy riêng: **rc3/DO:c62, index 616 SHA-256**. [Classifier](classifier-controls.json), [parent40](faithful-parent40.json).

| phép thử | rc | bằng chứng và diễn giải |
|---|---|---|
| `nat` cắt/rỗng parent | 3 / 3 | Chốt lệch Git native, xác nhận lời khai executor. [Cắt](variant-nat-parent-cut.json), [rỗng](variant-nat-parent-empty.json). |
| Sai công thức OID dự tính | 3 | Reader lệch: object không nằm tại OID yêu cầu. [Receipt](variant-oid-wrong-formula.json). |
| Bỏ chốt OID; bỏ phần tử oracle | 0 | Survivor thật; phân hạng và phản chứng không tương đương ở bảng P3. |
| Receipt rỗng / bỏ một path batch | 3 / 3 | Chốt OID bắt 0/597 và 596/597. [Rỗng](variant-oid-output-empty.json), [thiếu path](variant-batch-omit-first.json). |
| Bỏ `-w` cả batch | 3 | Fixture dict thành None, reader đỏ; không chứng minh mọi fixture âm đã ghi. [Receipt](variant-batch-no-write.json). |
| Đổi byte fixture dict số 0, có/bỏ chốt OID | 3 / 3 | Bắt lần lượt tại chốt OID và reader; khác fixture âm số 25. [Có chốt](extra-positive-byte-change.json), [bỏ chốt](extra-positive-byte-change-no-oid-assert.json). |
| Xóa object dict, parent/head | 3 / 3 | Cùng bắt index 0. [Parent](variant-delete-dict-object-parent.json), [head](variant-delete-dict-object-head.json). |

Thử đầu tiên nối byte vào **mọi** fixture làm một commit không còn hợp lệ với hash-object: **rc4/CalledProcessError**, lỗi setup do biến đổi reviewer, không phải kết quả `chay_dot_bien` của catalogue. **Không tính GIET hay finding sản phẩm**; đã thay bằng đổi riêng body hợp lệ để đo các cặp rc3/rc0 trên. Capture đầu cũng lỗi instrumentation vì trace gọi thêm Git lúc PATH đang bị mock; đã chặn capture lặp và chạy lại cả hai đạt rc0. [Thử bị loại](variant-batch-byte-change.json), [capture lỗi head](capture-head-instrumentation-error.json), [parent](capture-parent-instrumentation-error.json). Không cấp tín dụng cho các thử lỗi này.

**Thời gian Linux**

Sau khi các batch khác kết thúc, clone riêng đúng parent/head, chạy trực tiếp `python -B ops/ci_provenance_test.py --mot-ca c62_git_commit_khong_utf8`, đảo thứ tự theo cặp:

| lần | parent aebc808 (s) | head db2c1f5 (s) | rc |
|---|---:|---:|---|
| 1 | 6,569 | 2,237 | 0 / 0 |
| 2 | 6,691 | 2,106 | 0 / 0 |
| 3 | 6,368 | 1,959 | 0 / 0 |
| median | **6,569** | **2,106** | |

Giảm **4,463 s**, nhanh khoảng **3,12 lần**. Capture ghi nhận **2.600 → 641 lời gọi Git qua subprocess** (gồm thử thiếu PATH, không tính các lệnh đọc lại riêng của reviewer). Chênh lệch là 596 lệnh ghi lẻ, 453 lệnh oracle, 910 lần đọc lại bị loại. Không chứng minh thời gian suite/timeout Windows. [Số đo trực tiếp](direct-timing.json), [script](last_checks.py). Ba cặp qua wrapper trước đó cũng cùng chiều, giữ riêng ở [timing.json](timing.json), không trộn median trên.

**Bảng nghiệm thu N1′–N3′, N4–N7**

| tiêu chí | trạng thái | rc và bằng chứng dương |
|---|---|---|
| N1′ | **passed** | Head `--mot-ca c62_git_commit_khong_utf8` **rc0**; cùng test với CI_PROVENANCE_MA trỏ reader c8d92ba **rc3**, DO:c62 và UnicodeDecodeError. Capture xác nhận fixture/reader/oracle/main thực thi, không chỉ dựa stdout trắng. [Head](n1-head.json), [base](n1-base.json). |
| N2′ | **passed** | Tiền tố c53/c62 duy nhất; **55 F13 + 6 B2 GIET**, 61 baseline rc0, 61 mutant rc3 đúng ca; bằng lượt 9. [Receipt](mutants.json). |
| N3′ | **not_run** | Không chạy suite mặc định head/master; không khai TONG:DAT, 398/398 hoặc 62/62 ca chức năng. Catalogue kiểm tĩnh/import: master 61/343, head 62/398. Executor vẫn cần suite/CI exact head. |
| N4 | **passed** | Bare Ruff `python -B -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py`: head/master **rc0**, All checks passed, delta F=0. `git diff --check 9091cf5 HEAD` **rc0**. Không khai pin/probe Ruff CI. [Head](n4-head.json), [master](n4-master.json), [diff](n4-diff.json). |
| N5 | **passed** | `python -B .claude/dev/packet_loop.py doctrine-scan --root .`: **rc0**, 10 tệp/0 chỗ chép. `adr-song --root .`: **rc0**, 59 ADR/59 dòng khớp; tool nêu ngoại lệ trạng thái ADR-0016. [Doctrine](n5-doctrine-scan.json), [ADR](n5-adr-song.json). |
| N6 | **not_measured** | Offline, không đọc check run ci.yml; không lấy lời khai executor làm bằng chứng CI. |
| N7 | **not_applicable; not_run** | git_cuc_bo không thuộc HAM_DONG; không chạy `--dot-bien-dong`, không khai đạt. [Danh sách](static.json). |

**Định danh, toàn vẹn và giới hạn**

Packet #978 r2/g2, lease `wp978-r2-g2-claude`, lượt **10/10**, review_class `sensitive`, assurance_target `cross_approved`. Reviewer Codex/họ OpenAI, executor họ Claude theo assignment; độc lập, không dùng context Executor/subagent. Run `3fdb471c81784020a2f7dba1caec6f88`; launcher ghi `openai_codex / codex_cli / machine`. Exact serving model/effort không đo được; không suy từ tài khoản đăng review. Chưa gửi verdict ra dịch vụ ngoài.

Linux; Python **3.13.18**, Git **2.43.0**, Ruff **0.17.3**. Script kiểm dùng bytecode off, TMPDIR tuyệt đối trong OUT, Git global/system config `/dev/null` trừ đối chứng đã nêu, optional locks off, clone `--no-hardlinks`, Ruff no-cache. **10.814/10.814 tệp tracked SRC cùng SHA-256 đầu/cuối**; HEAD/parent/tree và status gồm untracked/ignored giữ sạch, clone head sạch. Phép đo hai mốc không phải kiểm mọi byte nội bộ .git hoặc chứng minh lịch sử mọi thao tác. [Đầu](source-before.json), [cuối](source-after.json), [kiểm cuối](final-audit.json).

Mọi bản sao, fixture, đột biến, báo cáo trong OUT; không sửa SRC. Không mạng/GitHub/push/merge/land, không soạn payload path thoát cây. Không xác minh freshness remote/lease online. D02, F10/D05 của #899; sửa `.claude/dev/ci_dang_ky_test.py`; mốc Workflow definition; LIVE CI; Windows native; nội dung master ngoài hai tệp; timeout 300 s của chay_con ngoài diff: giữ ngoài phạm vi. B2 được chạy để kiểm hồi quy theo assignment.

Script tái lập: [bootstrap](bootstrap.py), [runner/gates](checks.py), [capture](capture.py), [mutant test](variants.py), [bổ sung](extra.py), [timing/controls cuối](last_checks.py), [audit](audit.py). [Verdict tiến độ](VERDICT.progress.md). Bootstrap/clone cần đích mới khi chạy lại; JSON ghi lệnh và rc thật từng phép đo.
