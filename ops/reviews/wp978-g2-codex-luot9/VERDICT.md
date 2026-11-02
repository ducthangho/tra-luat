Verdict: approve
Reviewed commit: aebc808ea45408c827e753827b97f94689969db5
Spec sha256: 9fe94ad05cc1129e663cf77706db92685d6130c08c6a375454781a9aca188060

**P0=0, P1=0, P2=0; không phát hiện P3 còn mở trong phạm vi review.** Lỗi trùng tiền tố đã vá thật: **55/55 F13 GIET đúng c62, 6/6 B2 GIET đúng c53_wd_passed**, với 61 baseline rc0 và 61 tiến trình mutant rc3 đúng tín hiệu chốt. Không có HONG, TIN_DUNG_GIA hay SONG_SOT trong tập 61 mục này. **62/62 ca chức năng rc0.** Hai survivor S01/S02 của lượt 8 đã được khóa. Reader đúng **1.440/1.440** phép so độc lập trên graph hợp lệ SHA-1/SHA-256; cả hai kho qua fsck strict rc0. [Kiểm cuối](final-audit.json).

Áp ngưỡng của assignment lượt 9: lỗi sản phẩm, kỳ vọng sai, tín dụng giả và HONG chặn approve; thiếu độ phủ thuần túy thuộc P3. **N3′ của reviewer là not_run; N6 not_measured; N7 không áp dụng.** Approval này chỉ neo SHA trên, không thay bằng chứng suite mặc định/CI trên exact head và không cấp quyền push, merge hay land.

**ĐỐI CHIẾU LƯỢT TRƯỚC**

Đã đọc verdict lượt 8 trên `53ec046fc6c9ebc2b60871a5c0413570d3b0430d`, đọc toàn bộ diff ứng viên so master, diff riêng đổi tên và commit `28b542a`. Không nhận số đo cũ làm số đo lượt này.

| slug / biểu hiện | hạng, trạng thái | file:dòng | phép đo lượt 9 | hướng vá / duy trì |
|---|---|---|---|---|
| `mutation-target-prefix-collision` — connector r4438276217 trên e5ca45b | P1 cũ, **ĐÃ VÁ THẬT** | `ops/ci_provenance_test.py:1071`, `:1221`, `:1827` | Bản e5ca45b: 61/61 mục nhắm c53 trả HONG vì khớp hai ca. Head: tất cả tiền tố cNN duy nhất; 55 F13→c62 và 6 B2→c53 đều GIET đúng ca. | Đổi tên đúng ca #978 và toàn bộ đích F13 như bản vá; giữ B2/c53_wd_passed. Khi thêm ca, kiểm tính duy nhất tiền tố. [Trước](pre-rename-collision.json), [sau](mutants-summary.json). |
| `git-reader-fixture-domain-incomplete` — S01 `colon_key` | P3 cũ, **ĐÃ VÁ THẬT biểu hiện S01** | `ops/ci_provenance_test.py:1118`, `:1511` | F13_bo_hai_cham_ten: baseline rc0, mutant rc3/DO:c62; lệch đúng 35 fixture `tree:` mới. Nhân chứng độc lập SHA-1/SHA-256: head/native giữ metadata, mutant trả None. | Nợ **wp978-git-reader-differential-fuzz**, owner **ducthangho**: đã thêm nhân chứng và mutant; giữ trong corpus khi mở rộng bộ sinh. [Runner](mutant-F13_bo_hai_cham_ten.json), [nhân chứng](domain-witnesses.json). |
| `git-reader-fixture-domain-incomplete` — S02 `backslash_fold` | P3 cũ, **ĐÃ VÁ THẬT biểu hiện S02** | `ops/ci_provenance_test.py:1118`, `:1512` | F13_gap_backslash: baseline rc0, mutant rc3/DO:c62; lệch đúng 35 fixture backslash-LF mới. Nhân chứng độc lập trên cả hai định dạng phân biệt đúng biến đổi này. | Cùng nợ **wp978-git-reader-differential-fuzz**, owner **ducthangho**: đã thêm corpus/đột biến và fuzz seed cố định; tiếp tục dùng oracle native khi mở rộng grammar. [Runner](mutant-F13_gap_backslash.json). |
| `git-commit-body-encoding-lam-hong-metadata` | Giữ đóng trong miền đo | `ops/ci_provenance.py:158`; test `:1071` | N1′ head rc0; sản phẩm c8d92ba rc3 có UnicodeDecodeError. c62 bao gồm kiểm main với reader thật trên ISO-8859-1 và checkout passed. | Giữ đọc bytes, chỉ giải mã OID đã kiểm. [Head](n1-head.json), [base](n1-base.json). |
| `git-object-type-not-checked`, `git-header-cr-split-creates-parents`, `git-header-extension-creates-parents` | Giữ đóng trong miền đo | `ops/ci_provenance.py:170`, `:173`, `:175` | c62 xanh; các mutant bỏ kiểm loại, splitlines, quét parent xuyên header đều rc3/DO:c62. Kiểm chéo độc lập fixture và graph đủ object không thấy lệch. | Giữ loại commit, ranh giới LF và dãy parent liền sau tree; không chuẩn hóa extension thành metadata. [Đột biến](mutants.json), [domain](domain-summary.json). |

Nợ P3 của lượt 8 đã được xử lý đối với **hai biểu hiện còn mở S01/S02 và yêu cầu thêm fuzz được giao**. Không phát hiện survivor không tương đương mới. Đây là kiểm chứng hữu hạn, không phải chứng minh vét hết ngữ pháp Git. Không chạy lại catalogue C/D/B/P riêng của các lượt cũ; không nhận số 25/25, 140/160 hay kết luận tương đương 20 survivor cũ thành phép đo mới của lượt này.

**Bộ chạy đột biến và tín dụng**

Chạy chính `chay_dot_bien(*d)` cho từng mục DOT_BIEN có ca đích c62 hoặc c53, bằng `python -B out/checks.py mutants`; mỗi mục vẫn chạy baseline trước rồi chạy bản đột biến bằng tiến trình con của bộ test. [Script](checks.py), [receipt đầy đủ](mutants.json).

- **39 mục khai báo F13 trong mã nguồn mở rộng thành 55 mutant**, do comprehension; các dòng B2 nhắm c53 mở rộng thành **6 mutant**. Không nhầm số dòng khai báo với số chương trình chạy.
- Mọi tiền tố ca của **toàn bộ 398 mục DOT_BIEN** đều khớp đúng một ca; không còn cNN trùng trong AST hoặc registry CA. Riêng `def c53_` và `def c62_` đều đúng một định nghĩa. Đây là kiểm tĩnh cho 398 mục, **không phải tuyên bố đã chạy 398 mutant**. [Catalogue](static-audit.json).
- S01 chết ở index 77–81 rồi các tổ hợp parent khác; S02 chết từ index 82–86. Cả hai chết do reader chuẩn hóa sai header hợp lệ, không do setup/import hoặc sai kỳ vọng. [Fixture gốc](capture-one.json), [nhân chứng đủ graph](domain-witnesses.json).
- Tự kiểm của runner phân đúng lỗi vô can thành TIN_DUNG_GIA và thay đổi chỉ thêm chú thích thành SONG_SOT. Đối chứng import RuntimeError riêng của reviewer cho **rc4/HONG:c62**, không được đổi thành rc3. [Tự kiểm](classifier-controls.json), [import](import-error.json).
- Caveat đã có ở lượt 8 vẫn còn: tên `F13_cha_chi_40` không mô tả chính xác phép thay do thiếu nhóm ngoặc. Trên head nó chết ở index 602/603 vì chấp nhận parent lỗi / ném UnicodeDecodeError, là vi phạm thật. Reviewer kiểm thêm biến thể giới hạn parent 40 ký tự **đúng nghĩa**: rc3/DO:c62, chỉ lệch index **616**, commit SHA-256. Vì vậy không dùng tên catalogue làm bằng chứng; tính chất dự định vẫn bị bắt. Không xác nhận tín dụng giả hay survivor P3 cho điểm này. [Catalogue thực chạy](mutant-F13_cha_chi_40.json), [đối chứng đúng nghĩa](faithful-parent40.json).

**Review phần chưa được review: 28b542a**

Commit này thêm hai extension S01/S02 vào ma trận, hai mutant và vòng sinh 150 commit. Ma trận từ 7×10×5 thành **7×12×5 = 420** mẫu. [Diff commit](show-28b542a.txt).

`random.Random(978)` là instance riêng; dữ liệu sinh không dùng đồng hồ hay trạng thái random toàn cục. Capture hai lần cho đúng **150 lượt sinh, 141 OID khác nhau**, gồm **149 dict/1 None** theo M1. Digest thứ tự OID/kỳ vọng/raw bytes giống nhau: `f4b17b0323ebb9a310c035676a7f54f0d6cbf048c3db3f2a93df373e92c3b897`. Không gọi 150 lượt sinh là 150 commit duy nhất. [Lần 1](capture-one-summary.json), [lần 2](capture-two-summary.json).

Oracle có thật: `git log -1 --no-walk --format=%T%n%P` được gọi trong test cho mọi mục có kỳ vọng dict. Mục None do M1 không chạy oracle ở vòng ấy. Reviewer đã đối chiếu thêm **tất cả 597 commit fixture trước nhóm cố ý hỏng**, kể cả các mục None, với Git native và bộ đếm dòng streaming theo LF độc lập: **597/597 kỳ vọng đúng**. Cả 150 mẫu random được native đọc rc0; một mẫu None là giới hạn M1 về số dòng tree, không phải Git từ chối commit.

Biểu thức `so_tree` của test vẫn dùng cùng split/startswith như sản phẩm: độc lập về thực thi, chưa độc lập hoàn toàn về thuật toán. Phép kiểm streaming và oracle của reviewer bổ sung kiểm chéo. Fixture executor dùng parent OID tổng hợp chưa có object, nên **không khai graph fixture executor fsck sạch**. Reviewer dựng lại riêng graph có parent thật trên SHA-1/SHA-256: mỗi định dạng **420 tổ hợp + 300 mẫu grammar seed 97809**, tổng **1.440/1.440 đúng**, 1.158 dict/282 None. Mỗi kho có 720 root đích được truyền tường minh cho `git fsck --strict --no-reflogs --no-dangling`, đều rc0, không stdout/stderr. [Script](domain.py), [từng mẫu](domain-records.json), [SHA-1](domain-fsck-sha1.json), [SHA-256](domain-fsck-sha256.json).

Không cần danh tính Git để dựng object: commit/tag đi qua `hash-object` với author/committer/tagger cố định. Lần capture thứ hai xóa biến môi trường danh tính, bật `user.useConfigOnly=true`, `core.autocrlf=true`, đổi defaultBranch và logOutputEncoding; vẫn rc0 và cùng bytes/OID/kỳ vọng. Object truyền bằng bytes qua stdin nên không chịu chuyển CRLF của checkout. Đo trên **Git 2.43.0/Python 3.13.18**, chưa kiểm phiên bản Git khác hoặc Windows native. Repo fixture `sha1` vẫn dùng mặc định của `git init`; phép đo này sử dụng mặc định SHA-1, không tuyên bố miễn mọi cấu hình Git tùy ý. [Cách đo](audit_capture.py), [cấu hình](ci-no-identity.gitconfig).

Thời gian riêng, sau khi bộ mutant kết thúc: ba cặp chạy cùng sản phẩm/dependency, so test tại `8cfc2a0` với head. Median **4,074 s → 6,940 s**, tăng **2,866 s** mỗi lần chạy ca. Mức tuyệt đối hợp lý so timeout 300 s của runner trên máy này; không suy ra thời gian suite đầy đủ/CI từ phép đo này. [Số đo](runtime-results.json), [tổng hợp](runtime-summary.json).

**Sản phẩm, chuỗi commit và merge master**

Chuỗi first-parent khớp assignment: `53ec046 → 1a27c96 → 8cfc2a0 → 28b542a → e5ca45b → aebc808`; e5ca45b có parent thứ hai đúng `9091cf52cf20ac197c1a356d6a33cac6bab0b318`. [OID đầy đủ](chain.txt).

Diff master mới..head đúng **hai tệp**: `ci_provenance.py` **+22/-6**, test **+147/-0**; tổng +169/-6, dưới trần 450 dòng thêm nhưng cao hơn dự kiến 60 dòng của r1. Không có tệp ngoài write set. [Diff](diff-master.txt), [numstat](diff-stat.txt).

`git_cuc_bo` giữ **nguyên văn toàn bộ hàm**, kể cả comments/docstring, so với 53ec046; SHA-256 của phần hàm nằm trong [kiểm cuối](final-audit.json). Blob toàn tệp thay đổi vì master mang phần khác vào; không đánh đồng blob toàn tệp với riêng reader. So master, chỉ hàm `git_cuc_bo` và hằng RE_OID_B đổi. Các hàm/class của master trong hai tệp đều giữ nguyên, trừ reader được giao; toàn bộ **61 ca / 343 mutant** của master được giữ, head là **62 ca / 398 mutant** (+1/+55). [Kiểm AST/catalogue](static-audit.json), [phần master mang vào](master-additions-product.txt).

Diff e5ca45b..aebc808 chỉ test **+40/-40**. Tái tạo bằng đúng phép đổi tên hàm và đích F13 cho ra **byte-identical** head; thân test, các neo/thay mutant, B2 và c53_wd_passed không đổi. Product byte-identical e5ca45b. Không thấy giải conflict sai hoặc mất ca master. [Diff đổi tên](diff-rename.txt).

**N1′–N3′ và N4–N7**

| Tiêu chí | Trạng thái | rc và bằng chứng dương |
|---|---|---|
| N1′ | **passed** | `python -B ops/ci_provenance_test.py --mot-ca c62_git_commit_khong_utf8`: head **rc0**; cùng test với CI_PROVENANCE_MA trỏ sản phẩm c8d92ba **rc3**, DO:c62 chứa UnicodeDecodeError. Capture kiểm kỳ vọng và ca chức năng xác nhận ca đã thực thi. [Head](n1-head.json), [base](n1-base.json). |
| N2′ | **passed** | c53/c62 mỗi tiền tố một ca; **55 F13 + 6 B2 GIET**, baseline rc0, mutant rc3 đúng ca cho từng mục. Không HONG/TIN_DUNG_GIA/SONG_SOT trong tập này. [Receipt](mutants.json). |
| N3′ | **not_run** | Không chạy suite mặc định trên head hoặc master, không khai TONG: DAT hay 398/398. Phép đo bổ sung `--tat-ca-ca`: outer rc0, JSON đủ **62/62 ca rc0**, không dừng sớm. Catalogue master 61/343, head 62/398, delta +1/+55. [Các ca](functional-cases.json), [tổng hợp](functional-summary.json). |
| N4 | **passed** | Bare Ruff `python -B -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py`: head/master đều **rc0**, All checks passed, delta F=0. `git diff --check 9091cf5 aebc808` **rc0**. Không khai đã kiểm hợp đồng Ruff pin/probe CI. [Head](n4-head.json), [master](n4-9091cf5.json), [diff](n4-diff.json). |
| N5 | **passed** | `python -B .claude/dev/packet_loop.py doctrine-scan --root .`: **rc0**, 10 tệp/0 chỗ chép. `adr-song --root .`: **rc0**, 59 ADR/59 dòng khớp 1–1, ngoại lệ trạng thái ADR-0016 được tool nêu. [Doctrine](n5-doctrine-scan.json), [ADR](n5-adr-song.json). |
| N6 | **not_measured** | Offline; không đọc check run ci.yml, không lấy lời khai executor làm bằng chứng CI. |
| N7 | **not_applicable; not_run** | git_cuc_bo không thuộc HAM_DONG; không chạy --dot-bien-dong và không khai đạt. [Danh sách](static-audit.json). |

Giữ minh bạch những khác biệt câu chữ r1 đã nêu ở lượt 8: M1 viết `cat-file -p`, sản phẩm dùng `--batch` để nhận bytes và loại object cùng lần; M2 chỉ nhắc UnicodeDecodeError, test hiện chuyển mọi ngoại lệ phát từ reader thành tín hiệu vi phạm hợp đồng không-ném theo assignment; tên M3 literal text=True được thay bằng giải mã toàn stdout. Không tự sửa đặc tả đóng băng. R2 đã thay N1/N2/N3; áp ngưỡng hạng của assignment lượt 9 khi diễn giải Q1′.

**Định danh và toàn vẹn**

- Packet #978 r2/g2, lease `wp978-r2-g2-claude`, lượt **9/10**, review_class **sensitive**, assurance_target **cross_approved**; reviewer họ OpenAI, executor họ Claude theo assignment. Run `676c6847849343dcb5fcb8220a3e1d15`; launcher ghi `openai_codex / codex_cli / machine`. Exact serving model/effort **không đo được**; không suy từ tên tài khoản. Không có context Executor hay subagent trong lượt này.
- HEAD detached đúng SHA dòng 2; tree **77f4b6c8e9492c6855294b53ed770ddbe31daaab**; origin/master đúng base được giao. Spec r1 băm lại: **eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638**; r2 đúng dòng 3. [Preflight](preflight.json).
- **10.814/10.814 tệp tracked SRC không đổi SHA-256 đầu/cuối**; HEAD/tree, diff và status gồm untracked/ignored không đổi, sạch. Bản sao HEAD trong OUT giữ đúng nội dung tracked và status sạch. Không suy phép đo hai mốc thành chứng minh chưa từng ghi rồi hoàn nguyên, hoặc kiểm mọi byte nội bộ .git. [Đầu](source-before.json), [cuối](source-after.json), [kiểm cuối](final-audit.json).
- Linux; Python **3.13.18**, Git **2.43.0**, Ruff **0.17.3**. Bytecode tắt, TMPDIR tuyệt đối trong OUT, Git global/system config `/dev/null` trừ phép thử cấu hình được nêu, optional locks tắt, clone riêng `--no-hardlinks`, core.abbrev=7, Ruff no-cache. Trường versions ban đầu trong preflight có khóa trùng khi thu Python/Ruff; **versions trong final-audit.json là số đo đúng, đầy đủ**.

Mọi bản sao, phép thử, fixture, mutant và báo cáo nằm trong OUT; SRC chỉ đọc. Không mạng, GitHub, push, merge hay land; không soạn nội dung đường dẫn thoát cây. Freshness remote/issuecomment không được xác minh offline. D02 và F10/D05 của #899, sửa `.claude/dev/ci_dang_ky_test.py`, mốc Workflow definition, LIVE CI, Windows native và nội dung master ngoài hai tệp không tính hạng. Các ca B2/ca master chỉ được kiểm hồi quy theo yêu cầu merge, không mở rộng phạm vi tính năng.

Lệnh và rc nằm trong các JSON liên kết; script tái lập: [bootstrap](bootstrap.py), [checks](checks.py), [capture](audit_capture.py), [domain](domain.py), [controls/timing](extra_checks.py), [kiểm cuối](final_audit.py). `domain.py` cần thư mục domain mới khi chạy lại. [Verdict cập nhật trong quá trình](VERDICT.progress.md).
