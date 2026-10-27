Verdict: approve
Reviewed commit: 53ec046fc6c9ebc2b60871a5c0413570d3b0430d
Spec sha256: eccd6dd2917f76d6158d5c9574f4d4c2070ba22ef3da96b4dfcf6e820c301638

**P0=0, P1=0, P2=0, P3=1 lớp (hai survivor mới).** Áp ngưỡng mới của chủ kho trong assignment lượt 8: lỗi sản phẩm, kỳ vọng sai và tín dụng giả chặn approve; thiếu độ phủ thuần túy thuộc P3. Không tìm thấy lỗi sản phẩm trong miền đã đo. Reader đúng **1.860/1.860** phép so với Git native/M1 trên graph hợp lệ, ngoài bộ hồi quy 50/50. Ma trận executor đúng 350/350 kỳ vọng. 53/53 ca chức năng đạt; 53/53 F13 được runner phân hạng GIET; 25/25 mutant C lượt 7 bị giết. [Audit cuối](final-audit.json).

Lớp độ phủ **chưa đóng hoàn toàn**: S01/S02 còn sống và có nhân chứng không tương đương. Giữ nợ **`wp978-git-reader-differential-fuzz`**, owner **`ducthangho`**, xử lý bằng test vi sai sinh ngẫu nhiên theo ngữ pháp header Git ở packet sau, theo quyết định chủ kho được chép trong prompt (#978 issuecomment-6445001458). Không dùng việc đổi hạng để gọi lỗi sản phẩm là thiếu fixture.

Verdict chỉ neo SHA trên; không cấp quyền push, merge hoặc land. **N3 vẫn `not_run` của reviewer, N6 `not_measured`**; kết luận này không thay bằng chứng suite đầy đủ/CI trên exact head mà executor và quy trình tích hợp còn phải cung cấp.

**ĐỐI CHIẾU LƯỢT TRƯỚC**

Đã đọc verdict lượt 1, bản tạm lượt 2, lượt 3–7; không nhận các số cũ làm phép đo của lượt này. Sản phẩm không đổi từ `aa2a1f3`. Diff `bf8ef91..53ec046` chỉ sửa `ops/ci_provenance_test.py`, thêm mẫu parent ABA/AAA và folding/tên trường. Script hồi quy được đọc, sao vào OUT và bỏ phần ghi kết luận cũ trước khi dùng.

| Lớp / biểu hiện | Kết luận trên head | Bằng chứng tự đo lượt 8 |
|---|---|---|
| `git-commit-body-encoding-lam-hong-metadata` | Giữ đóng trong miền đo | N1 head rc0/base rc3 có UnicodeDecodeError; reader 50/50 đúng. Bảy biến thể SHA-1 qua main head đều rc0/checkout passed, gồm Latin-1 author/message, không khai encoding, extension không UTF-8 và body giống metadata. [Reader](independent-results.json), [main](independent-main-results.json). |
| `git-object-type-not-checked` | Giữ đóng | Blob dạng commit, blob không UTF-8, tree/tag trả None trên SHA-1/SHA-256. Main blob: head rc0 nhưng checkout not_measured; base rc0/checkout passed. Không dùng outer rc0 để suy checkout passed. |
| `git-header-cr-split-creates-parents` | Giữ đóng | CR-author fsck strict rc0, native không có cha, ancestry rc1. Main control/CR head rc12/12, đều failed; base rc12/0. [Git](cr-author-results.json), [main](cr-author-main-results.json). |
| `git-header-extension-creates-parents` | Giữ đóng | Parent sau committer/extension: native/head không nhận làm cha; fsck strict rc0. Head main control và hai biến thể đều rc12/failed, base hai biến thể rc0/passed. [Reader](extension-finding.json), [main](extension-main-results.json). |
| `git-reader-fixture-domain-incomplete` — C lượt 7 | **ĐÃ VÁ THẬT 25 biểu hiện C đã cung cấp; lớp còn mở P3** | C01–C25 đều child rc3, DO đúng c53; bao gồm toàn bộ 15 survivor lượt 7. S01/S02 mới sống đủ 53/53 ca nhưng sai trên nhân chứng. [Kết quả](mutant-results.json), [audit nguyên nhân](mutant-reason-audit.json). |
| D/B/P lượt 5–6 | Giữ đóng các biểu hiện không tương đương cũ | D: 39 GIET/10 sống; B/P: 23 GIET/10 sống. Chỉ 20 mục tương đương đã nêu ở lượt 7 còn sống, đúng danh sách cũ. Không có rc4. |
| Batch framing, lỗi Git, OID, parent/SHA-256 | Giữ khóa trong miền đo | 53 child F13 rc3 đúng c53; runner 53/53 GIET. 22 probe không-ném không có exception thoát ra. [Edges](no-throw-edges.json), [runner](n2-prescribed-results.json). |
| Bộ bọc ngoại lệ reader | Không xác nhận tín dụng giả | AttributeError trong reader rc3 vì vi phạm không-ném; lỗi import và binding ngoài reader rc4/TIN_DUNG_GIA. Literal text=True với input str rc3/UnicodeDecodeError. [Đối chứng](wrapper-controls.json). |

Thay đổi hạng của lớp độ phủ là quyết định mới của chủ kho, **không phải tuyên bố toàn lớp đã được vá**. Không reset slug hay lịch sử các lượt trước.

**Bảng lớp còn mở**

| slug | hạng | file:dòng | phép đo | hướng vá |
|---|---|---|---|---|
| `git-reader-fixture-domain-incomplete` | **P3, không chặn** | `ops/ci_provenance_test.py:1115`, `:1120` — miền extension/header; vị trí mutation `ops/ci_provenance.py:151` | S01 bỏ dấu `:` cuối tên trường; S02 nối backslash-LF. Mỗi bản c53 rc0 và đủ 53/53 ca rc0. Bốn nhân chứng SHA-1/SHA-256 fsck strict rc0: head criterion rc0, mutant rc3. Head đúng cả 1.860 mẫu vi sai. | Nợ **wp978-git-reader-differential-fuzz**, owner **ducthangho**: bộ sinh theo grammar, nhãn M1 độc lập, oracle native và graph đầy đủ ở packet sau. Giữ reader đang đúng; đưa hai nhân chứng và phép biến đổi này vào corpus hồi quy. |

**Hai survivor mới và nhân chứng**

| ID | Thay đổi tổng quát | Nhân chứng SHA-1 | Sai khác và phép đo |
|---|---|---|---|
| S01 `colon_key` | Tách tên trường ở SP đầu, `rstrip(b":")` riêng tên rồi ghép lại | `f28fa0f7967c5a9963b2ac4883e2fa6fde6aa4c9`; extension sau committer là `tree: <OID>` | Native/head giữ tree và ba parent A,B,A; mutant tạo tree cấp ngoài thứ hai, trả None. Có 38 mẫu phân biệt trong phép quét; c53 rc0, toàn ca 53/53 rc0. |
| S02 `backslash_fold` | Xóa cặp byte backslash-LF trước khi tách header/body | `957bd6971c2316b95b87a862e4c49a46da6d7c93`; sau committer có `tree` + backslash + LF, tiếp theo SP + OID | Native/head giữ metadata; mutant nối thành `tree <OID>`, trả None. Có 32 mẫu phân biệt; c53 rc0, toàn ca 53/53 rc0. |

Hai phép biến đổi áp chung lên dữ liệu, không nhận diện SHA, fixture hay tên ca. Đây là hai biểu hiện cùng lớp chuẩn hóa sai header. Nhân chứng SHA-256: S01 `891936d37935a0979027eb92cc5c3a4b40b98e91b9063a72eb011861f365c082`; S02 `e97293921f9856f495107359a9ebb68191ad650f7251d6dd4ab55589a4121a95`.

[Catalogue neo/thay và hash](new-mutant-catalogue.json), [c53/toàn ca](new-mutant-results.json), [raw bytes/native/expected/fsck và criterion](new-witnesses.json). Bốn criterion head **rc0 + CA: 1/1 dat**, bốn criterion mutant **rc3 + DO:r978_header_grammar:** là tiến trình con thật; không suy từ rc0 của collector. Các commit chứng minh được ghi bằng hash-object thông thường, không dùng --literally.

Tái lập một cặp từ thư mục chứa PROMPT.md, với hiện vật OUT hiện tại:

```sh
PYTHONDONTWRITEBYTECODE=1 python -B out/criterion.py sha1-cross-25-3-2 out/head/ops/ci_provenance.py
PYTHONDONTWRITEBYTECODE=1 python -B out/criterion.py sha1-cross-25-3-2 out/S01_colon_key.py
```

Kỳ vọng rc0 rồi rc3. S02 dùng fixture `sha1-cross-31-3-2` và tệp `out/S02_backslash_fold.py`.

**Tính đúng của test và tín dụng đột biến**

Ma trận head có **7 × 10 × 5 = 350 mẫu**, gồm **210 dict / 140 None**. Đã capture chính c53 chạy xanh, giữ raw bytes/OID/expected; đối chiếu 350 mẫu bằng nhãn grammar (extension 1–4 phải None) và state machine duyệt byte theo LF/dòng trống. Native Git rc0 trên cả 350. Không phát hiện expected M1 sai. [Audit từng mẫu](matrix-exact-audit.json), [tổng hợp](matrix-audit-summary.json), [capture](c53-capture.json).

Biểu thức so_tree của executor không gọi reader nhưng dùng cùng split/startswith với sản phẩm: độc lập về thực thi, **chưa độc lập về thuật toán**. Kiểm nhãn grammar/state machine của reviewer bổ sung kiểm chéo. None theo M1 không đồng nghĩa native không đọc được commit: M1 cố ý từ chối nhiều dòng tree cấp ngoài, kể cả extension sau committer. Không xem khác biệt này là lỗi sản phẩm.

Graph c53 dùng OID cha tổng hợp chưa có object; không tuyên bố graph đó fsck sạch. Reviewer dựng lại toàn bộ ma trận trên hai định dạng bằng cha thật, thêm **560 phép liên trục** và **600 mẫu grammar có seed 97808**: tổng **1.860 phép so, 1.764 cặp repo/OID khác nhau**, đúng 1.860/1.860. Fsck strict truyền toàn bộ root đích tường minh, rc0 cả hai kho. [Script](domain.py), [fixture](domain-fixtures.json), [tổng hợp](domain-summary.json), [fsck SHA-1](domain-fsck-sha1.json), [SHA-256](domain-fsck-sha256.json). Đây là phép quét hữu hạn, không chứng minh vét hết ngữ pháp Git.

Audit chương trình thực sự sinh ra của **160 mutant**: 53 F13 và 107 C/D/B/P; **140 GIET, 20 sống, 0 rc4**. Trong 140 mục chết, 132 được tái hiện trực tiếp trên input thất bại đầu tiên của c53; tám còn lại là bảy chốt PATH/rc/framing/timeout và một chốt OID SHA-256, có output cụ thể. [Inventory/diff/hash](mutant-inventory.json), [audit lý do](mutant-reason-audit.json).

**Lưu ý tên F13_cha_chi_40 tại `ops/ci_provenance_test.py:1230`:** phép thay catalogue thiếu nhóm ngoặc quanh and dưới not; chương trình thực tế không từ chối parent SHA-256 hợp lệ. Nó chết ở index 382/383 vì chấp nhận parent lỗi zz / giải mã parent chứa byte lỗi. Đây là vi phạm M1/không-ném thật do mutation, không phải lỗi setup/import vô can; nhưng **không lấy tên này làm bằng chứng khóa lỗi parent chỉ 40 hex**. Reviewer tạo riêng phép thay có nhóm ngoặc đúng: chết đúng index 396, commit SHA-256 hợp lệ, rc3/DO đúng c53. Tính chất dự định vẫn được test bắt trực tiếp; không xác nhận thiếu độ phủ hay tín dụng giả cho tính chất đó. Nên sửa tên hoặc biểu thức catalogue khi bảo trì. [Phân tích A/B, neo/thay](parent40-audit.json), [child đúng nghĩa](faithful-parent40-c53.json).

Hai mươi survivor cũ: D10/D11/D12/D14/D16/D31/D33/D38/D39/D42; B05/B06/B12; P02–P08. Lấy frame cat-file --batch thật của 1.860 fixture strict-valid rồi phát lại cho từng parser: **37.200/37.200 khớp**, không exception. Đây là **replay stdout thật với subprocess được mock**, không phải 37.200 lời gọi Git mới. [Receipt](old-equivalence-domain.json).

Lập luận tương đương trong miền strict-valid: D10/D11 cắt NUL trong miền không chứa NUL; D12/B05/B06/B12 giữ prefix trước LF-LF đầu; D14/D16/D33/P02–P04/P08 không vượt author để nhận continuation làm parent; D31 replacement giữ các byte ASCII quyết định parser; D38/D39 không đổi metadata thật hợp lệ hoặc số tree; D42 có guard đúng một tree; P05–P07 strip/tách parent vốn là OID thuần. Không suy tương đương riêng thành tương đương của mọi phép hợp thành; không đề nghị dùng replacement thay implementation M1.

**N1–N7**

| Tiêu chí | Trạng thái | rc và bằng chứng dương |
|---|---|---|
| N1 | **passed** | `python -B ops/ci_provenance_test.py --mot-ca c53_git_commit_khong_utf8`: head rc0; cùng test với CI_PROVENANCE_MA trỏ sản phẩm base rc3, DO đúng c53 có UnicodeDecodeError. [Head](n1-head.json), [base](n1-base.json). |
| N2 | **passed về hành vi các chương trình đột biến thực tế** | checks.py rc0; import test rồi gọi chay_dot_bien(*d) cho mọi F13: **53/53 GIET**, mỗi lần kiểm baseline trước. 53 child riêng đều rc3/DO đúng c53. Literal text=True và parent40 đúng nghĩa được kiểm thêm. [Runner](n2-prescribed-results.json), [child](mutant-results.json), [exit](process-exit-receipts.json). |
| N3 | **not_run** | Không chạy suite mặc định. Riêng --tat-ca-ca outer rc0, JSON đủ **53/53 ca rc0**. Catalogue base 52 ca/292 mutant; head 53 ca/345 mutant, delta +1/+53. Không khai 345/345 hoặc TONG: DAT trên head. [Ca](all-head.json), [tổng hợp](all-head-summary.json), [catalogue](catalogue-counts.json). |
| N4 | **passed** | `python -B -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py`: head/base rc0, All checks passed, delta F=0. git diff --check base head rc0. Đây là bare lint, không phải pin/probe Ruff CI. [Head](n4-head-ruff.json), [base](n4-base-ruff.json), [diff](n4-diff.json). |
| N5 | **passed** | `python -B .claude/dev/packet_loop.py doctrine-scan --root .` rc0: 10 tệp/0 chỗ chép. adr-song --root . rc0: 55 ADR/55 dòng khớp 1–1, ghi ngoại lệ trạng thái ADR-0016. [Doctrine](n5-doctrine.json), [ADR](n5-adr.json). |
| N6 | **not_measured** | Offline, không đọc check run ci.yml; không lấy lời khai executor thay phép đo. |
| N7 | **not_applicable; not_run** | git_cuc_bo không thuộc HAM_DONG; không chạy --dot-bien-dong, không khai đạt. [Danh sách](catalogue-counts.json). |

Receipt suite bf8ef91 của executor thuộc commit trước, không dùng làm N3 cho 53ec046. Giữ minh bạch chênh câu chữ spec cũ: M1 nói -p, sản phẩm dùng --batch lấy loại object và bytes cùng lần; M2 chỉ nêu UnicodeDecodeError, bộ bọc hiện nhận lỗi từ frame reader theo hợp đồng không-ném trong assignment; M3 tên F13_doc_text_true được thay bằng F13_giai_ma_toan_stdout; N3 dự kiến +3, thực +53 mutant. Không tự sửa spec đóng băng hay tuyên bố khớp nguyên văn các câu này.

**Định danh, phạm vi và toàn vẹn**

- HEAD detached **53ec046fc6c9ebc2b60871a5c0413570d3b0430d**, tree **30b97db6d5c0f3c9444304306dbf8b40aad2cf26**. Local origin/master đúng base **c8d92ba05c3ea875d8f84d94195430302690286d**. Chuỗi tám commit và hash đặc tả khớp assignment. [Preflight](preflight.json).
- Diff base..head đúng **2 tệp, +157/-6**; vượt dự kiến 60 dòng thêm nhưng dưới trần sensitive 6 tệp/450 dòng. AST chỉ git_cuc_bo đổi ở cấp hàm, thêm regex OID; main/moc_checkout/git_blob/doc_wf/REST không đổi. [Diff](preflight-diff.json), [diff lượt 8](preflight-step-diff.json), [scope](scope.json).
- Reviewer Codex/họ OpenAI, executor họ Claude theo assignment/lease; **review_class sensitive, assurance_target cross_approved**. Launcher run **2e306e6d008746ff88bc06b24175e79e**, khai openai_codex / codex_cli / machine; exact serving model/effort **not_measured**. Không có context executor hoặc subagent. [Identity](identity.json). Freshness remote/issuecomment không được xác minh trong phiên cấm mạng; authority review là assignment hiện tại, lượt cuối 8/8.
- Linux, Python 3.13.17, Git 2.43.0, Ruff 0.17.3. Python bytecode tắt; TMPDIR tuyệt đối dưới OUT; Git global/system config /dev/null, optional locks tắt; clone riêng không hardlink, core.abbrev=7; Ruff no-cache. [Versions](versions.json).
- **7.205/7.205 tệp tracked SRC không đổi SHA-256**, bản sao head khớp; HEAD/tree/spec không đổi, diff/index và status gồm untracked/ignored sạch đầu/cuối. [Đầu](source-before.json), [cuối](source-after.json), [bản sao](copy-after.json). Không suy thành kiểm mọi byte .git hoặc chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.
- Hai lỗi collector reviewer đã sửa và chạy lại: serialize surrogate trong JSON; thiếu khóa label khi in summary extension. Giữ log ban đầu, không tính thành lỗi sản phẩm hay bằng chứng pass: [JSON](audit-test-initial-error.log), [summary](extension-initial-error.log). Lượt sửa xong rc0; receipt con giữ mã thoát thật. [Audit](final-audit.json), [exit](process-exit-receipts.json).

Mọi phép thử/fixture/mutant/báo cáo nằm dưới OUT; SRC chỉ đọc. Script chính: [bootstrap](bootstrap.py), [checks](checks.py), [audit test](audit_test.py), [vi sai](domain.py), [audit lý do](reason_audit.py), [kiểm cuối](final_audit.py). Lệnh/cwd/rc/output nằm trong JSON tương ứng. [Verdict trung gian](VERDICT.intermediate.md), [tiến độ](VERDICT.progress.md). Khi tái tạo toàn bộ fixture, dùng OUT mới; script dựng kho không thiết kế để chạy đè tùy ý lên hiện vật cũ.

D02 và F10/D05 của #899, .claude/dev/ci_dang_ky_test.py, mốc Workflow definition, LIVE CI, Windows native và SHA-256 toàn tuyến main ngoài phạm vi; không tính hạng hoặc khai đã đo. Không soạn/thử nội dung đường dẫn thoát cây. Không mạng, GitHub, push, merge hay land.
