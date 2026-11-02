Verdict: approve
Reviewed commit: 516a33467b1212a90153bb25ed44f28b16d5fac9
Spec sha256: 9fe94ad05cc1129e663cf77706db92685d6130c08c6a375454781a9aca188060

**P0=0, P1=0, P2=0; ba lớp P3 lượt 10 còn mở một phần.** Chốt mới bắt được bỏ đầu/cuối oracle, đổi byte và bỏ ghi fixture âm, nhưng chưa khóa hết các biến thể cũ hoặc cả lớp. Lời khai “gỡ từng assertion là tương đương vì head đúng vẫn xanh” **không được chấp nhận**: các cặp phản chứng bên dưới phân biệt được bản có và không có assertion. Đây là thiếu độ phủ test, không phải lỗi sản phẩm trên head. Theo ngưỡng assignment lượt 11, ghi nợ P3 và approve exact SHA trên.

**55/55 F13 + 6/6 B2 GIET đúng ca**, đủ 61 baseline rc0 và 61 mutant rc3/đúng marker; không HONG, TIN_DUNG_GIA hoặc SONG_SOT trong tập catalogue này. N1′ đạt; không phát hiện chốt mới tự đỏ trên Linux/cấu hình đã đo. **N3′ not_run; N6 not_measured; N7 không áp dụng.** Verdict không thay bằng chứng suite mặc định/CI exact head và không cấp quyền push, merge hay land. [Kiểm cuối](final-audit.json).

**ĐỐI CHIẾU LƯỢT TRƯỚC**

Đã đọc verdict [lượt 9](../tham-chieu/luot9-VERDICT.md), [lượt 10](../tham-chieu/luot10-VERDICT.md) và recipe phản chứng cũ để tái dựng đúng vị trí tiêm. Không nhận số đo cũ thành số đo lượt này. Định danh tự kiểm:

| mục | bằng chứng lượt 11 |
|---|---|
| HEAD | detached, `516a33467b1212a90153bb25ed44f28b16d5fac9`; tree `b67fed4e1ca0dda94f766c8c0323fab5ddc48f4f` |
| chuỗi first-parent | `e5ca45b71f3e2264943b6b44b164e47687671604` → `ad0d3a1d98df13f8697d9fb124b84def14a50b7f` → `b659eaebd3b8d974a9e44cde0fdd1e98f1c04f2b` → HEAD |
| master | `refs/remotes/origin/master` = `9091cf52cf20ac197c1a356d6a33cac6bab0b318`; cũng là parent thứ hai của e5ca45b |
| tree lượt 9 | `ad0d3a1^{tree}` = `refs/tham-chieu/aebc808^{tree}` = `77f4b6c8e9492c6855294b53ed770ddbe31daaab` |
| tree lượt 10 | `b659eae^{tree}` = `refs/tham-chieu/db2c1f5^{tree}` = `3676c40ebb324a0252beed5f4731ca2186fdabf8` |
| spec | SHA-256 đủ 64 ký tự khớp dòng 3 |
| diff parent..head | đúng `ops/ci_provenance_test.py`, **+10/-5**, chỉ thân c62; sản phẩm byte-identical parent |
| diff master..head | đúng hai tệp trong write set, tổng **+190/-6**; dưới trần 450 dòng thêm |

[Preflight](preflight.json), [diff mới](diff-parent.txt), [diff master](diff-master.txt), [kiểm AST/catalogue](static.json). Chỉ dẫn lượt 11 cho phép review cụ thể thay đổi thân c62 này, thay cho giới hạn chỉ đổi tên trong M4 r2; không sửa spec đóng băng. Hai cặp tree bằng nhau không thay review exact head hiện tại.

| slug | hạng | file:dòng | phép đo | hướng vá / duy trì |
|---|---|---|---|---|
| `mutation-target-prefix-collision` | P1 cũ, giữ đóng | `ops/ci_provenance_test.py:1071`, `:1853` | c53/c62 mỗi tiền tố một ca; mọi đích của 398 mutant khớp duy nhất. 55 F13 và 6 B2 đều GIET đúng ca. | Giữ c62 và đích F13; không đổi B2/c53_wd_passed. |
| `git-reader-fixture-domain-incomplete` — S01/S02 | P3 cũ, giữ đóng hai biểu hiện | `ops/ci_provenance_test.py:1123`, `:1532` | F13_bo_hai_cham_ten và F13_gap_backslash đều baseline rc0, mutant rc3/DO:c62. Corpus/kỳ vọng giữ nguyên. | Giữ nhân chứng trong corpus của nợ `wp978-git-reader-differential-fuzz`, owner `ducthangho`; không tuyên bố vét hết grammar. |
| `git-reader-oracle-coverage-unlocked` | **P3, đóng hai biểu hiện; lớp còn mở** | `ops/ci_provenance_test.py:1171`, `:1174` | Bỏ đầu hoặc SHA-256: rc3, đếm 454/455. **Thay mục đầu bằng mục thứ hai vẫn rc0**, đủ 455 lượt nhưng mất OID đầu (OID này xuất hiện đúng một lần). Gỡ assertion đếm riêng rc0; bỏ đầu với/cắt assertion cho rc3/rc0. | Nợ **wp978-git-reader-differential-fuzz**, owner **ducthangho**. Ghi sổ định danh các mục thực sự đã so, đối chiếu độc lập với ca dict + SHA-256; khóa bỏ đầu/cuối, thay-bằng-trùng và gỡ assertion bằng kiểm fault injection riêng. Tránh so set làm mất multiplicity hoặc lấy kỳ vọng từ vòng bị cắt. |
| `git-reader-write-receipt-assertion-unlocked` | **P3, có chốt bù; chưa đóng** | `ops/ci_provenance_test.py:1149` | Đổi byte #25 + bỏ assertion OID nay rc3 tại batch-check. Nhưng bỏ riêng assertion OID vẫn rc0; **tiêm `ghi=[]`** với/cắt assertion cho **rc3/rc0**, dù object vẫn được ghi đúng. | Cùng nợ **wp978-git-reader-differential-fuzz**, owner **ducthangho**. Giữ assertion OID; thêm kiểm độc lập tiêm receipt rỗng/sai/thừa/thiếu vào bước ghi và đòi đúng tín hiệu chốt, kể cả khi mọi object tồn tại. Tránh dùng riêng lỗi object để chứng minh receipt được kiểm; không tăng số lần spawn Git theo từng fixture. |
| `git-reader-negative-fixture-existence-unchecked` | **P3, đóng bỏ ghi; lớp còn mở** | `ops/ci_provenance_test.py:1098`, `:1150`, `:1161` | Bỏ #25 khỏi hàng đợi (có/bỏ assertion OID): rc3/missing. Xóa trước batch-check: rc3. **Đúng vị trí xóa của lượt 10**, trước `ca += blob` và sau chốt mới, vẫn **rc0**. Bỏ assertion tồn tại riêng rc0; bỏ ghi với/cắt assertion tồn tại cho rc3/rc0. | Cùng nợ **wp978-git-reader-differential-fuzz**, owner **ducthangho**. Kiểm sổ object ngay ở ranh giới trước khi reader tiêu thụ fixture; khóa bỏ ghi/xóa fixture âm và gỡ chốt. Chỉ yêu cầu tồn tại nhóm thực sự dựng; tránh đòi đầu vào cố ý thiếu tồn tại hoặc fsck graph có parent tổng hợp. Không hứa kiểm mọi thay đổi object sau thời điểm kiểm cuối. |

Các P3 được chấp nhận dưới dạng nợ theo assignment: sản phẩm trên head đúng, không có kỳ vọng sai hoặc tín dụng giả đã đo. Không đánh đồng lỗi kép tiêm chủ ý với lỗi đang xảy ra trên head. **Không tuyên bố cả ba P3 đã ĐÓNG.**

**Phản chứng và lời khai executor**

Mỗi biến thể là bản sao test dưới OUT, chạy c62 qua wrapper dùng dependency của clone head. Neo/thay được kiểm tính duy nhất trong [variants.py](variants.py); từng bản nguồn và receipt được giữ. Mọi rc3 dưới đây đều chứa `DO:c62_git_commit_khong_utf8:`; không tính lỗi setup thành GIET. [Tất cả 21 phép đo](variants.json).

| biến thể / đối chứng | rc | bằng chứng dương |
|---|---:|---|
| bỏ oracle đầu / bỏ SHA-256 | 3 / 3 | `oracle chỉ so 454 mục`. [Đầu](variant-skip-oracle-first.json), [SHA-256](variant-skip-oracle-sha256.json) |
| đổi byte body fixture #25 | 3 | chốt OID, 597/597 receipt nhưng giá trị khác. [Receipt](variant-negative-byte-change.json) |
| đổi byte #25 + gỡ chốt OID | 3 | batch-check báo `d5baa24ae09f84a08c4dd2c55a4fa1c5125db3ed missing`. [Receipt](variant-negative-byte-change-no-oid.json) |
| bỏ fixture âm khỏi hàng đợi; cùng biến thể gỡ OID | 3 / 3 | sổ lập lúc dựng không bị rút theo `cho`, cùng OID thiếu. [Có chốt OID](variant-negative-omitted-from-queue.json), [bỏ chốt OID](variant-negative-omitted-from-queue-no-oid.json) |
| xóa object #25 trước batch-check | 3 | chốt tồn tại bắt missing. [Receipt](variant-delete-none-after-write-before-existence.json) |
| xóa object #25 đúng vị trí phép thử lượt 10 | **0** | xác nhận `ca[25][1] is None`, object xóa thật; c62 vẫn xanh. Vị trí này nay nằm **sau** batch-check, không được đổi vị trí rồi khai biến thể cũ đã chết. [Receipt](variant-delete-none-old-exact-placement.json) |
| gỡ riêng assertion đếm / tồn tại / OID | **0 / 0 / 0** | tái hiện đúng rc executor khai; rc0 trên head đúng chưa chứng minh tương đương. [Đếm](variant-remove-count-assertion.json), [tồn tại](variant-remove-existence-assertion.json), [OID](variant-remove-oid-assertion.json) |
| bỏ đầu oracle + gỡ assertion đếm | **0** | cùng lỗi bỏ đầu khi còn assertion cho rc3. [Receipt](variant-skip-first-no-count.json) |
| bỏ fixture âm + gỡ assertion tồn tại | **0** | cùng lỗi bỏ ghi khi còn assertion cho rc3; chốt OID vẫn còn. [Receipt](variant-omit-negative-no-existence.json) |
| receipt rỗng, có/bỏ assertion OID | **3 / 0** | object tồn tại không bảo đảm receipt đã được đối chiếu. [Có](variant-receipt-empty.json), [bỏ](variant-receipt-empty-no-oid.json) |
| thay oracle đầu bằng mục thứ hai | **0** | đủ số lần, sai tập mục được so. [Receipt](variant-replace-oracle-first-with-second.json) |
| sai cỡ / sai loại / xóa object literal | 3 / 3 / 3 | chốt tồn tại bắt đúng cả ba. Thông điệp sai loại có thể in `[]` vì phần giải thích chỉ lọc hậu tố cỡ; phép so toàn dòng vẫn đỏ. [Cỡ](variant-wrong-object-size.json), [loại](variant-wrong-object-type.json), [literal](variant-literal-object-missing.json) |
| đảo thứ tự sổ / thêm dòng sổ trùng | 0 / 0 | batch-check trả đúng thứ tự yêu cầu, giữ bản sao lặp. [Đảo](variant-reordered-ledger.json), [trùng](variant-duplicate-ledger-row.json) |

Xác nhận được các số rc executor nêu, nhưng bác suy luận tương đương ở dòng cuối. Không dùng survivor ngoài catalogue để đổi nhãn 61 mutant chuẩn: hai tập phép đo có mục tiêu khác nhau.

**Ngữ nghĩa, byte và cấu hình**

Capture parent/head đều rc0, cùng **616 mục SHA-1 + 1 SHA-256**, cùng OID, byte fixture, thứ tự, kỳ vọng và kết quả. Digest chung của dữ liệu capture chuẩn hóa: `cd66f4479f935aa19e44f09a4663b96294806f87bfe82a152c6d236ce08a80e2`. Digest này dùng schema lượt 11, không so trực tiếp với digest schema lượt 10. [Parent](capture-parent-summary.json), [head](capture-head-summary.json), [script](capture.py).

- Sổ mới có **606 hàng SHA-1**, gồm **597 lượt thường + 9 literal**, tương ứng **597 OID duy nhất** (9 lượt trùng). Reviewer trace riêng từng lần `cm()` và xác nhận sổ khớp `(OID, len(raw_bytes))` đúng thứ tự, không suy sổ từ `cho`. Batch-check có đủ 606 dòng đúng OID/loại/cỡ. SHA-256 được dựng sau chốt này; được kiểm bởi reader/oracle và readback riêng, không nằm trong sổ SHA-1.
- Đọc lại raw bytes bằng Git cho **607/607 lượt dựng**, gồm SHA-256; tổng **598 object duy nhất**. Cỡ byte SHA-1 từ **113 đến 12.670**, gồm author/message không UTF-8, Unicode và object literal cố ý sai header. `len(b)` tính byte, không tính ký tự. Batch-check kiểm loại/cỡ, không parse ngữ pháp commit literal.
- Oracle có **455 mục so / 446 OID duy nhất**, `da_so=455`; số kỳ vọng được đếm từ `ca`, độc lập với `hop`. Đây là chốt số lượng đúng trên head, chưa phải chốt định danh mục như survivor cho thấy. Reviewer dùng bộ đọc LF streaming và Git native riêng để kiểm **597/597** kỳ vọng nhóm commit thường; không phát hiện kỳ vọng sai. [Capture đầy đủ](capture-head.json).
- `core.autocrlf=true`, `user.useConfigOnly=true`, logOutputEncoding ISO-8859-1 và TMPDIR thường/khoảng trắng/Unicode/kết hợp đều **rc0**. File commit ghi bằng `write_bytes`, qua `hash-object -t commit --stdin-paths`; giữ nguyên byte và không cần danh tính ký/commit. [Cấu hình](autocrlf.gitconfig), [bốn receipt](environment.json).

Các hàm/class test ngoài c62 giữ nguyên AST; mọi tuple mutant parent/head giống nhau. Product byte-identical parent; không thay ngữ nghĩa hoặc kỳ vọng cũ trong miền đã đo. Không chạy lại graph/fuzz 1.440 mẫu lượt 9 và không khai graph fixture fsck sạch vì parent tổng hợp chưa có object. Không chứng minh mọi cấu hình Git, phiên bản Git hoặc Windows native.

**Răng catalogue và nghiệm thu**

Gọi chính `chay_dot_bien(*d)` cho từng F13/B2, giữ baseline và tiến trình mutant của runner; chạy bốn worker process trên bản sao OUT. [Script](catalogue.py), [61 receipt](mutants.json), [tổng hợp](mutants-summary.json). Không có subagent và không chạy suite mặc định.

Tự kiểm classifier phân đúng lỗi vô can thành `TIN_DUNG_GIA`, thêm chú thích thành `SONG_SOT`. Đối chứng import RuntimeError rc4/HONG không được tính GIET. Caveat cũ `F13_cha_chi_40` không diễn đạt chính xác phạm vi thay do ngoặc được giữ minh bạch: catalogue chết vì lỗi thật; biến thể giới hạn parent 40 ký tự đúng nghĩa chạy riêng **rc3/DO:c62 tại index 616 SHA-256**. [Classifier](classifier-controls.json), [import](import-error.json), [parent40](faithful-parent40.json).

| tiêu chí | trạng thái | rc và bằng chứng dương |
|---|---|---|
| N1′ | **passed** | `python -B ops/ci_provenance_test.py --mot-ca c62_git_commit_khong_utf8`: clone exact head **rc0**. Cùng test với `CI_PROVENANCE_MA` trỏ reader c8d92ba **rc3**, DO:c62 chứa UnicodeDecodeError. Capture xác nhận fixture/reader/oracle thực thi; ca còn chạy main trên ISO-8859-1 với mốc checkout passed. [Head](n1-head.json), [base](n1-base.json) |
| N2′ | **passed** | c53/c62 mỗi tiền tố một ca; **55 F13 + 6 B2 GIET**, đủ 61 baseline rc0 và 61 mutant rc3 đúng marker. [Receipt](mutants.json) |
| N3′ | **not_run** | Theo assignment, không chạy suite mặc định head/master; không khai TONG:DAT, 398/398 hoặc 62/62 ca chức năng. Kiểm tĩnh/import: master **61/343**, parent/head **62/398**; mọi mutant master được giữ. Executor chịu phần suite exact head. [Catalogue](static.json) |
| N4 | **passed** | Bare Ruff `python -B -m ruff check --no-cache --select F`: hai tệp head và hai blob master xuất riêng đều **rc0**, All checks passed, delta F=0. `git diff --check 9091cf5 HEAD` **rc0**. Không khai pin/probe Ruff CI. [Head](n4-head.json), [master](n4-master.json), [diff](n4-diff.json) |
| N5 | **passed** | `python -B .claude/dev/packet_loop.py doctrine-scan --root .`: **rc0**, 10 tệp/0 chỗ chép. `adr-song --root .`: **rc0**, 59 ADR/59 dòng khớp 1–1; tool nêu ngoại lệ trạng thái ADR-0016. [Doctrine](n5-doctrine-scan.json), [ADR](n5-adr-song.json) |
| N6 | **not_measured** | Offline; không đọc check run ci.yml, không nhận lời khai executor thành bằng chứng CI. |
| N7 | **not_applicable; not_run** | `git_cuc_bo` không thuộc HAM_DONG; không chạy `--dot-bien-dong`, không khai đạt. [Danh sách](static.json) |

**Thời gian Linux**

Sau khi các batch khác kết thúc, chạy trực tiếp c62 trên hai clone sạch đúng b659eae/head, năm cặp đảo thứ tự. Tất cả **10/10 rc0**; đây là thời gian cả tiến trình, không phải suite hoặc Windows. [Số đo/lệnh](timing.json), [tổng hợp](timing-summary.json).

| lần | b659eae (s) | head (s) |
|---|---:|---:|
| 1 | 2,5142 | 2,5334 |
| 2 | 2,5388 | 2,5407 |
| 3 | 2,3994 | 2,4273 |
| 4 | 2,3600 | 2,3624 |
| 5 | 2,4561 | 2,4102 |
| median | **2,4561** | **2,4273** |

Chênh median **−0,0288 s (−1,17%)** nằm trong dao động quan sát; không kết luận chốt mới làm nhanh hơn hoặc miễn phí. Profile riêng xác nhận **641 → 642 lời gọi Git**, thêm đúng một `cat-file --batch-check`, mẫu đo lệnh này **0,0208 s**. [Profile](runtime-profile.json). Phần thông điệp assertion tạo tuple các cỡ cho mỗi dòng dù điều kiện đúng, có chi phí trong bộ nhớ; số đo có trace không được cộng thẳng vào benchmark trực tiếp. Chưa thấy hồi quy thời gian tổng đáng kể trên Linux này. Probe dòng đầu của reviewer trỏ nhầm khối ghi blob, đã loại và chạy lại với neo assertion động; [artifact bị loại](runtime-profile-invalid-line-probe.json) không phải lỗi sản phẩm.

**Định danh, toàn vẹn và giới hạn**

Packet #978 r2/g2, lease `wp978-r2-g2-claude`, lượt **11/11**, `review_class: sensitive`, `assurance_target: cross_approved`. Reviewer Codex/họ OpenAI; executor họ Claude theo assignment. Phiên reviewer độc lập, không dùng context executor hoặc subagent. Run `33a99dc0134a4f25a9ad5e533d38a248`; launcher ghi `openai_codex / codex_cli / machine`. Exact serving model/effort không có số đo độc lập trong run metadata đã đọc; không suy từ actor GitHub. Không tự tạo receipt/state hoặc gửi verdict ra ngoài.

Linux, **Python 3.13.18 / Git 2.43.0 / Ruff 0.17.3**. Thử nghiệm dùng bytecode off, TMPDIR tuyệt đối trong OUT, global/system Git config `/dev/null` trừ đối chứng đã nêu, Git optional locks off, clone `--no-hardlinks`, Ruff no-cache. **10.814/10.814 tệp tracked SRC cùng SHA-256 đầu/cuối**; HEAD/tree/status SRC giữ nguyên và sạch, hai clone sạch. Đây là phép đo hai mốc cho tracked bytes/status, không phải audit mọi byte nội bộ `.git` hoặc chứng minh toàn bộ lịch sử thao tác. [Đầu](source-before.json), [cuối](source-after.json), [audit](final-audit.json).

Mọi script, biến thể, fixture và kết quả ghi dưới OUT; không sửa mã SRC, không mạng/GitHub/push/merge/land. Hướng thử đường dẫn thoát cây chỉ mô tả bằng lời: kiểm bộ phân giải từ chối tên trỏ ra ngoài thư mục fixture; phiên này không soạn/thực thi payload đó. Không xác minh freshness remote/lease online. Giữ ngoài phạm vi D02, F10/D05 của #899, sửa `.claude/dev/ci_dang_ky_test.py`, mốc Workflow definition, LIVE CI, Windows native, nội dung master ngoài hai tệp và timeout 300 s của `chay_con`.

Tái lập: [bootstrap](bootstrap.py) cần đích clone mới; [common](common.py), [runner variants](run_case.py), [variants](variants.py), [capture](capture.py), [catalogue](catalogue.py), [gates](gates.py), [environment/controls/timing](extra_checks.py), [profile](profile_runtime.py), [audit cuối](final_audit.py). [Verdict tiến độ](VERDICT.progress.md) lưu kết luận tạm; văn bản hiện tại là verdict cuối.
