verdict: changes_requested
reviewed_sha: e849e2eb341801155cd20341b9f77b5116329dcc

**0 P1 / 3 P2 / 0 P3; 7 thể hiện tại 5 cụm vị trí.** Doctrine đã sạch theo phép đọc toàn tệp. Còn một con trỏ mới sai đích, hai mô tả công cụ rộng hơn hành vi thực và bốn chỗ nối hiện vật sai trong ví dụ lệnh. **HINT.patch: 5 hunk / 1 tệp**, dry-run đúng `--fuzz=0` và áp thật trên clone đều rc=0, không fuzz/offset. Chín cổng nền đều rc=0; không suy cổng xanh thành nội dung đúng.

Reviewer: Codex, dựa trên GPT-6 theo chỉ thị phiên; provider OpenAI (`openai_codex`), execution surface agent Codex có shell sandbox qua API, transport `machine`. Không có chứng cứ độc lập về backend model/effort viết verdict. Các phiên bản CLI được thử là Codex 0.154.0 và Claude Code 2.1.269; chúng không chứng nhận danh tính reviewer.

Authority là PROMPT.md của gói. Review ngoại tuyến, không gọi model con, không mạng, không push/merge/đăng GitHub, không sửa cây `cay-kho/`. Chỉ ghi artifact trong gói và thử trên bản sao ngoài cây review. Các thử `record-review` dùng state fixture riêng, không tạo assurance/state thật. Không xác thực lease/generation/GitHub hiện hành ngoài snapshot được giao.

Git xác nhận HEAD đúng, tree `e47fbc282867830bfa83d556fe258826ba1f2075`, base `bb7013c7669da19304a8769e5b25f8c1f8951e9c` là ancestor. Diff toàn PR: **1 tệp, +223/−137**; diff riêng từ `36acc5235057779d861eff08988a9469b17e513a`: **+111/−137**. Adapter hiện **506 dòng**; base 420, lượt5 trước vá 532. [Kiểm Git/cuối lượt](evidence/final-check.json).

## Bản vá lượt 5 có vá quá tay không

**Không thấy mất công cụ đến mức adapter không dùng được (0 P1), nhưng có một con trỏ bị đổi sang sai đích (O01).** Lượt5 cũng viết lại hai mô tả công cụ thành câu vẫn quá rộng (E01/E02). Đã đọc VERDICT-LUOT-5.md, HINT-LUOT-5.patch và replay toàn patch lên blob `36acc52`: **43/43 hunk, rc=0, không fuzz/offset, kết quả bằng byte HEAD**. Đây là đo lại việc áp patch, không nhận lời khai phiên chính. [Replay](evidence/probes.json), [diff lượt5 thực áp](evidence/round5-applied.patch).

ĐỐI CHIẾU LƯỢT TRƯỚC:

| Finding lượt5 | Kiểm trên HEAD | Phân loại |
|---|---|---|
| adapter-chep-doctrine | Tự đọc lại 506 dòng theo 14 vùng; không còn nghĩa vụ review áp dụng chung ngoài con trỏ. Lệnh/cờ/tệp cơ bản được giữ. Tuy nhiên H13 dẫn sai đích và H20/H43 còn mô tả rộng hơn công cụ. | **ĐÃ VÁ THẬT lớp doctrine; VÁ SINH LỖI MỚI ở con trỏ O01; E01/E02 còn sống trong câu viết lại.** |
| loi-khai-vuot-phep-do: E01–E04 cũ | Snapshot sạch chỉ là ảnh chụp; ba lượt #513 không được dùng làm chứng minh nhân quả/tính duy nhất; child chỉ “có thể” bị bỏ lại. Bảng số không bị xoá hoặc phủ định. | **ĐÃ VÁ THẬT bốn thể hiện cũ.** Hai thể hiện lượt6 thuộc cùng lớp nhưng ở vị trí khác. |
| prompt-qua-argv | L87 chuyển Claude sang stdin, giữ các cờ/tool/output; Codex vẫn dùng stdin. CLI thật cộng help với prompt ASCII131072 byte qua stdin rc0. | **ĐÃ VÁ THẬT tuyến argv trong mẫu.** Full model review NOT_RUN; help không chứng minh model xử lý prompt. |

Kiểm mất công cụ: so mọi lệnh/cờ/đường dẫn/tên tệp của cả base và `36acc52` với HEAD, rồi tra protocol. **Không basename tệp nào biến mất; chỉ cờ dài `--short` biến mất**, cùng lệnh `git rev-parse --short`, và cả hai nằm ngay trong phép đo protocol §8 mà L273 trỏ đến. Câu Claude argv được thay bằng mẫu stdin đầy đủ ở L87; hai ví dụ prose rút gọn của nó không cần phục hồi. `same_provider_approved` và `rc=2` thuộc nội dung được giữ ở protocol. Khối ba câu lịch ghi được bỏ, nhưng `>`/`>>` vẫn ở L345. Chuỗi thông báo bộ lọc cũ bị bỏ là thông tin chẩn đoán lịch sử, không làm mất lệnh/cờ/lane. [Kiểm kê và từng quyết định](evidence/tool-retention.md).

Đối chiếu **mọi vị trí dẫn nguồn**, cả comment “xem (1)”/“xem dưới”, các mục §4/§8/§9/§12/§13, tên hàm và tên mục CLAUDE: chỉ **O01 L233** sai đích. §4/§8 không chứa cơ chế neo danh tính kho; nội dung thực ở `docs/GOI_AGENT_DA_NEN.md`, mục “Neo theo kho, không theo đường dẫn”, L395–413. Các câu dẫn về số hướng/lịch ghi có nêu **prompt/yêu cầu của lượt**, không hứa protocol chứa ngưỡng6 hoặc ba câu lịch ghi cũ. [Bảng con trỏ đầy đủ](evidence/pointer-audit.md).

Không có bằng chứng hạ quá tay E01–E04 cũ: L241–244 vẫn nói rõ hai lệnh Git quan sát được gì; L330–343 giữ thời gian/hiện vật và chỉ bỏ kết luận nhân quả/duy nhất; L377–380 giữ sự cố526 con và chỉ bỏ lượng từ mọi bộ test. Các nhãn “thuật lại” ở model/quota/reboot/HINT #518 có sẵn trước commit lượt5, không phải lượt5 vừa làm mờ số liệu đó.

## Adapter có chép doctrine không

**Không tìm thấy mệnh đề doctrine sống trên HEAD.** Tự phân hoạch 14 vùng liên tiếp, phủ **506/506 dòng**, gồm toàn **111 dòng mới**; đọc chủ thể, động từ nghĩa vụ, thời điểm và điều kiện kết thúc của từng câu, kể cả heading/comment/bảng/code. [Bảng14 vùng](evidence/scan-inventory.md).

Những chỗ dễ đếm nhầm đã xét riêng: “đút cả hai trường” là cú pháp bộ chọn; lấy trường từ header là cách đọc output; ngoặc vuông pkill là cú pháp tránh tự khớp; `BẮT BUỘC` ở core.abbrev trỏ ngay yêu cầu cấu hình §8; bảng6/8/2 là lịch sử prompt; khung verdict ghi rõ chỉ là ví dụ, không schema đủ nghiệm thu. Các nội dung về quyền/lịch ghi/phân công/hoàn tất còn lại là con trỏ.

Bảng thể hiện sống rỗng:

| ID | Dòng | Nghĩa vụ review đặt trong adapter |
|---|---|---|

`doctrine-scan` rc=0/7 tệp **không phải chứng minh cho kết luận nghĩa này**. Đột biến M2 thêm một nghĩa vụ không thuộc danh sách chuỗi cấm: cổng vẫn0, nhưng phép đọc bắt được1 vùng. Các ledger gắn hash/độ phủ; script chỉ kiểm tính đầy đủ của annotation do reviewer lập, không tự hiểu tiếng Việt.

## Năm lớp — bảng quét

Cùng14 vùng dùng cho năm lượt hỏi riêng: nghĩa vụ hay công cụ; bằng chứng hẹp hay lời khai rộng; trạng thái/rc có đúng đối tượng; mọi số/đơn vị/mẫu số; thông tin biến mất và đích con trỏ. Quét thêm mọi producer/consumer của hiện vật và từng23 code fence. Không dùng danh sách finding cũ làm giới hạn.

| Lớp | Thể hiện sống HEAD | Sau HINT trên clone | Cách quét / bảng |
|---|---:|---:|---|
| adapter-chep-doctrine | 0 | 0 | Đọc nghĩa toàn506 dòng,14 vùng; bảng rỗng ở trên. |
| loi-khai-vuot-phep-do | 2 | 0 | Rà lượng từ/điều kiện và đối chiếu helper, shell cùng fixture; E01/E02 dưới đây. |
| phan-hoach-trang-thai | 1, trùng E01 | 0 | Rà mọi nhánh rc, thiếu dữ liệu, chưa chạy/đã chạy, Z/PID, EOF, quota. Không cộng finding lần hai. |
| don-vi-byte | 0 | 0 | Rà mọi số, đơn vị, tỷ số và nguồn lịch sử; bảng rỗng dưới đây. |
| va-qua-tay-mat-cong-cu | 1: O01 | 0 | So toàn blob base/prior/HEAD, các token mất và mọi con trỏ; bảng O01 dưới đây. |

**loi-khai-vuot-phep-do — đủ2 dòng:**

| ID | Dòng HEAD | Phản chứng / tác động | Hunk |
|---|---|---|---|
| E01 | 288–289, gắn lệnh283–284 | Câu “mỗi mã thoát thuộc một lần chạy của cổng” không đúng khi `cd` lỗi. Chạy đúng dạng dòng283 với thư mục fixture vắng: stdout `nen rc=1`, không gọi Python/cổng, shell rc0 do echo. Người đọc bị dẫn tới coi một lần chưa chạy là kết quả gate. | H2 |
| E02 | 496–497 | “Slug sai dạng hoặc thiếu” đều trả khác0 thiếu điều kiện verdict. CLI thật với state fixture hợp lệ: approve không ID rc0/state accepted; blocked không ID rc0; changes_requested không ID rc2; có slug hợp lệ rc0; slug sai dạng rc2. Mẫu changes_requested vẫn đúng; phần mô tả tổng quát mới sai phạm vi. | H5 |

[Log shell và ma trận record-review](evidence/probes.json). Ma trận kiểm hành vi công cụ, không tạo authority review thật.

**phan-hoach-trang-thai — đủ1 dòng, cùng E01:**

| ID | Dòng | Nhánh bị nhập sai |
|---|---|---|
| E01 | 288 | `cd` thất bại/cổng **chưa chạy** được mô tả như một lần cổng đã chạy và trả mã. H2 sửa cách quy mã; không cộng P2 mới. |

Các nhánh khác không thấy gộp sai: rc1 EOF chưa chạy review; thiếu/hỏng sổ và không đọc khoá không suy chết; khoá khớp không suy sống; Z khác tiến trình đang chạy; hai stat như nhau không suy đã chết. Bộ lọc ngắt khác bộ test fail; grep-count stdout0/rc1 khác cổng đỏ. Thử block chẩn đoán thật **60,173 giây** cho hai mẫu bằng nhau trong khi child còn sống.

**don-vi-byte —0 dòng:**

| ID | Dòng | Sai đơn vị / quy đổi / tỷ số |
|---|---|---|

Đã xét các mốc17/27-08 và12-09; 9 lượt model và tần suất8/9,6/9,3/9,2/9 (không phải các nhóm loại trừ nhau); ví dụ500/90000 token không được gọi là share đo thật; bốn nhóm Codex/ba model từ chối/bốn effort; khoảng4 giờ; hai sự cố; 80 dòng log; hai mẫu cách60 giây, `%Y` là mtime giây và `%s` là byte; 50 dòng tail; 40 phút; 201 head lịch sử; 3 trong13 lượt và154/437/299 giây; 35 lệnh; 6 hướng yêu cầu/8 đã thử/2 lỗi; 526 con và14,5 trên16GB là số lịch sử, không tự quy đổi GiB; 7 lượt/6 HINT/13 hunk #518 khác mẫu2/5 #250/#252; OID40hex khác SHA25664hex. Không thấy sai phép quy đổi hoặc lẫn mẫu số. **Không có raw log để đo lại số lịch sử**, nên không gọi việc đọc đúng bối cảnh là xác minh lại từng số.

Những lời khai ưu tiên trong prompt đều đã thu hẹp đúng: `max` bị từ chối chỉ cho spark ở phép thử#518; quota không còn khẳng định pool độc lập; launcher chỉ “có thể” để trạng thái cũ, gắn hai sự cố thuật lại; ba phép kiểm không còn được tuyên mỗi phép là cần. Commit `a8b0cf443ca8475e859ad8ae5e150fce135818d2` tồn tại và message ghi đúng7/6/13 cùng rc0 sáu HINT; đó là **đối chiếu nguồn thuật lại**, không replay sáu HINT#518.

**va-qua-tay-mat-cong-cu — đủ1 dòng:**

| ID | Dòng HEAD | Thiếu/sai | Hunk |
|---|---|---|---|
| O01 | 233 | Con trỏ “hợp đồng neo danh tính kho” đến §4/§8 không có nội dung ấy. Cú pháp cờ và lỗi rc11 vẫn được giữ; sửa đích sang mục công cụ có thật. | H1 |

## Lớp KHÁC tìm được

**lenh-khong-noi-hien-vat —4 thể hiện/2 cụm, có từ base.** Tự liệt kê các đầu vào/đầu ra tệp của mọi khối: PROMPT.md, reviewer.json, run.json/stderr.log, diff.patch/numstat.txt, VERDICT.md, HINT.patch, GOI_Y_VA.diff, mc/cb. Đối chiếu tên, chữ hoa/thường và nơi tạo trước khi đọc; không chỉ gọi help.

| ID | Dòng HEAD | Lỗi và phép đo | Hunk |
|---|---|---|---|
| A01 | 465–466 | `diff -u` xuất stdout nhưng dòng sau đọc GOI_Y_VA.diff chưa được tạo. Nguyên khối sau thay placeholder: rc1, `No such file or directory`; thêm `> GOI_Y_VA.diff`: rc0, kiểm đúng cay/doc.md. | H3 |
| A02 | 472 | Lệnh request-changes đọc verdict.md, khác tệp VERDICT.md ở mục trước. Trên Linux, `test -r verdict.md` rc1; tên đúng rc0. | H4 |
| A03 | 473 | Lệnh approve mắc cùng sai tên; đã kiểm riêng đối số body-file, kết quả1→0. | H4 |
| A04 | 474 | Lệnh comment mắc cùng sai tên; đã kiểm riêng đối số body-file, kết quả1→0. | H4 |

[Phản chứng hiện vật](evidence/artifact-probes.json), [kiểm bản đã áp](evidence/hint-validation.json). **Gh thật NOT_RUN** vì CLI vắng và không có quyền mạng/đăng; bằng chứng A02–A04 là tệp đầu vào trên filesystem phân biệt chữ hoa/thường, không phải lời khai đã nhận lỗi từ API GitHub.

Đã kiểm đủ23 code fence với trạng thái THẬT/PARTIAL/N/A cho từng khối trong [bảng lệnh](evidence/command-audit.md). Kết quả đáng chú ý: recipe mirror thật rc0/non-shallow; nguồn cục bộ355 tên và bộ đệm355 tên, comm rỗng; launcher check remote-local rc11→remote-URL rc0 mà không fetch HTTPS; hai worktree cùng SHA chạy doc-claims strict rc0; helper model nhận canonical alias/phụ và từ chối model lạ; mẫu pkill trần làm shell bị SIGKILL, mẫu ngoặc in CHAY. Những phép này không phát hiện thêm lớp ngoài ba finding đã kê.

Không nặn finding từ quyền cài đặt/model/network không có. Cũng không tính lỗi harness thành lỗi sản phẩm: lần import packet_loop bằng runpy thiếu sys.path để tìm launcher, đã sửa runner và tiếp tục phần chưa chạy. Probe layout B20 đầu tiên vô tình thêm redirect, nên chỉ đo layout; đã ghi rõ giới hạn ấy rồi chạy **nguyên recipe** ở probe riêng để phát hiện A01.

## Phép đo nền

Clone `/tmp/rv521-l6-o17c_utl/clean` từ mirror cục bộ bằng `git clone --no-local`, detached exact head, non-shallow, `core.abbrev=7`, status đầu/cuối rỗng. Clone nằm **ngoài** `cay-kho/` và ngoài gói review nên không đổi kiểm kê. Actionlint1.7.7 ghim trong gói được thêm vào PATH; Python3.11.15, Git2.43.0, shellcheck0.9.0. Origin của clone này là mirror cục bộ, không phải GitHub hiện hành. [Setup](evidence/setup.json), [runner](evidence/run_gates.py).

| Lệnh từ gốc clone sạch | rc | Bằng chứng dương |
|---|---:|---|
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | 7 tệp,0 chuỗi cấm. [Log](evidence/gate-doctrine.json) |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | 0 | 47 ADR↔47 dòng; ngoại lệ trạng thái0016 được khai. [Log](evidence/gate-adr.json) |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | 113 đạtv2 +11/11 miễn legacy +42 nợ đóng băng =166;0 vi phạm/chưa đo. Không gọi166 đều đạtv2. [Log](evidence/gate-receipts.json) |
| `python3 ops/lease_publish_test.py` | 0 | 147/147 chạy,0 bỏ qua;37 mutant:34 bị giết,3 sống có chủ đích,0 tín dụng giả. [Log](evidence/gate-lease.json) |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | ok=true, expected=checked=180; package hash khớp. [Log](evidence/gate-release.json) |
| `python3 scripts/tl.py golden-test --json` | 0 | ok=true,20 ca. [Log](evidence/gate-golden.json) |
| `python3 scripts/tl.py doc-claims-check --strict --json` | 0 | ok=true,107 tệp,0 hard flag,374 advisory,0 layer skipped. [Log](evidence/gate-claims.json) |
| `python3 .githooks/eol_policy.py --all --json` | 0 | 2082 scanned,2060 checked,22 skipped,0 vi phạm. [Log](evidence/gate-eol.json) |
| `python3 .claude/dev/idiom_py_test.py` | 0 | 7/7,0 bỏ qua,9 mutant;389 lời gọi trần ngoài phạm vi là nợ chẩn đoán. [Log](evidence/gate-idiom.json) |

Không có cổng nền đỏ, nên không phát sinh nghĩa vụ chạy lại cổng đỏ trên clone sạch thứ hai. Các rc khác0 của phản chứng không bị nhập vào bảng cổng nền. Đây không phải full CI GitHub hoặc full runtime selftest.

## Đột biến và khôi phục

Cây thử `/tmp/rv521-probes-o2pxwwy1/clone`; mọi thay đổi đều ngoài cây review. [Script đột biến](evidence/mutations.py), [log trước/sau/khôi phục](evidence/mutations.json).

| Đột biến | Lệnh / biến đổi | rc trước→sau→khôi phục | Kết luận |
|---|---|---|---|
| M1 nhắm lời khai mới L497 | Trong packet_loop.py đổi `if a.verdict == "changes_requested" and not ids:` thành `if not ids:`. Chạy CLI `record-review --verdict approve --reviewed-sha <HEAD>` không finding-id, dùng state fixture hợp lệ. | CLI **0→2→0**; oracle đòi0/0finding/accepted: **0→1→0**. | Câu khái quát HEAD phù hợp với mutant chặt hơn, không phù hợp mã thật. Phép thử phân biệt được điều kiện verdict bị xoá. |
| M2 nhắm phép đọc doctrine | Thêm dòng507: “Reviewer phải nộp ít nhất chín hướng thử trước khi được kết thúc lượt.” Đọc lại: chủ thể reviewer, nghĩa vụ tối thiểu và điều kiện kết thúc; không là cú pháp/lịch sử. Chạy `semantic_scan.py <bản> <ledger>` cho ba bản có hash và phân hoạch đầy đủ. | Ledger **0→1→0**; doctrine-scan trên mutant vẫn **0**. | Phép đọc bắt1 vùng doctrine mà cổng chuỗi bỏ qua. Script chỉ kiểm hash/độ phủ/annotation, **không phải semantic detector tự động**. |

M1 khôi phục hash packet_loop `066a812207175f8fb3aa55c454ab44cd6f421724752feaaa2bc2f648dff37a71`; M2 khôi phục hash adapter `d8fd378d3f7b20161a73235d4344c0948a3303596484bf0dabca4b412673b1b3`. Cả hai có so byte bằng trước và status rỗng. [Ledger/checker](evidence/semantic_scan.py), [phần hoàn nguyên M2](evidence/finish_semantic.py). Không tự soạn chuỗi tấn công đường dẫn hoặc payload thoát thư mục.

## HINT.patch và giới hạn

**Nhãn patch-as-hint:** “chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”.

[HINT.patch](HINT.patch) là unified diff repo-relative cho `patch -p0`, **5 hunk/1 tệp** `.claude/skills/cross-review/SKILL.md`. Đã chạy đúng:

```bash
cd cay-kho && patch -p0 --fuzz=0 --dry-run < ../HINT.patch
```

**rc=0**. Bản kiểm verbose và áp thật ở clone cũng rc=0, **5/5 hunk không fuzz/offset**, bằng byte `evidence/adapter-fixed.md`. Sau áp: doctrine-scan, idiom, doc-claims strict, git diff --check đều0; adapter không CR và kết thúc LF; khối tạo/đọc diff đã sửa rc0; cả ba body-file trỏ tệp tồn tại. Đọc lại toàn bản đã áp: năm lớp và lớp mới đã kê đều0 thể hiện. Đây là kết quả trên **bản gợi ý**, không thay verdict changes_requested của HEAD gốc. Clone đã được hoàn nguyên đúng byte/status sạch. [Log áp/kiểm](evidence/hint-validation.json).

| Hunk | Finding sở hữu duy nhất | Thể hiện đóng | Có chạm câu lượt5 vừa viết? |
|---|---|---|---|
| H1 | va-qua-tay-mat-cong-cu | O01 L233 | **Có**, H13 lượt5: con trỏ mới sai đích; đổi sang mục công cụ thực. |
| H2 | loi-khai-vuot-phep-do | E01 L288–289, cũng đóng nhánh trạng thái | **Có**, H20 lượt5: bỏ doctrine nhưng viết quá rộng “mỗi mã … một lần chạy cổng”; bổ sung nhánh cd chưa gọi cổng. |
| H3 | lenh-khong-noi-hien-vat | A01 L465–466 | Dòng diff có từ base, được lượt5 giữ; thêm redirect kết nối hai lệnh. |
| H4 | lenh-khong-noi-hien-vat | A02/A03/A04 L472–474 | Ba tên tệp có từ base, được lượt5 giữ; sửa đủ3 đối số. |
| H5 | loi-khai-vuot-phep-do | E02 L497 | **Có**, H43 lượt5: ý “thiếu slug đều lỗi” có từ trước và được viết lại, vẫn bỏ điều kiện changes_requested. |

SHA256 HINT: `7d28a48d5a0529fa343f060b1c3f01b7ba1df548622e548c2ff69c30560ebf20`. [Bản đồ hunk](evidence/hint-map.json).

Giới hạn: không kiểm account/quota/reset/pool/effort backend hoặc chất lượng review thực; không chạy full Claude/Codex model; không có raw logs sáu HINT#518, năm hiện vật#250/#252 hay toàn bộ prompt/run#513 để replay lịch sử/nhân quả. Không tái lập reboot/PID reuse, Windows/macOS hoặc runner tích clone dài ngày. Gh/API GitHub/MCP publish/CI hiện hành NOT_RUN; các phép shell stand-in không được gọi là dịch vụ hoạt động. Không chạy npm install, ghi credential, dọn thư mục tạm hoặc sửa protocol/tooling thật.

Đã ghi hai artifact trước phép đo và cập nhật dần; [nhật ký trước bản chốt](evidence/verdict-progress.md). Kiểm cuối xác nhận cây review còn đúng HEAD/tree, adapter bằng blob HEAD và status rỗng. Không dùng status rỗng làm chứng minh một tiến trình bất kỳ chưa từng ghi rồi hoàn nguyên.

### va-qua-tay-mat-cong-cu [P2] Con trỏ mới về danh tính kho dẫn đến mục không chứa nội dung đó

**O01, L233; H1 đóng cả lớp có1 thể hiện.** §4/§8 tồn tại nhưng không mô tả cờ/chuẩn hoá danh tính kho mà câu dẫn hứa. Người xử lý lỗi rc11 sẽ tìm sai nơi; nội dung có thật ở docs/GOI_AGENT_DA_NEN.md L395–413. H1 đổi đích và gọi rõ đó là chi tiết cờ công cụ, không đưa lại doctrine. Đã kiểm heading tồn tại và launcher local-origin→URL cho11→0 trên fixture. Không phải P1 vì cú pháp chính/error vẫn được giữ. Rủi ro vá: heading nguồn có thể đổi về sau; hiện khớp nguyên văn. Độ tin cao.

### loi-khai-vuot-phep-do [P2] Mô tả mã thoát bỏ điều kiện chạy cổng và loại verdict

**E01/E02, L288–289 và496–497; H2/H5 đóng đủ2 thể hiện.** Hai câu được lượt5 viết lại vẫn rộng hơn phép đo: mã cd được gọi là kết quả cổng, còn điều kiện finding của changes_requested bị áp sang approve/blocked. Đã chạy nhánh cd vắng và ma trận5 trường hợp CLI thật; M1 phân biệt được điều kiện bị bỏ. H2/H5 mô tả đúng các nhánh của shell/helper, giữ nguyên lệnh và không thêm tiêu chí review. Ca khoá là chính nhánh chưa chạy và approve/blocked không finding; không cần sửa product helper để làm cho câu sai thành đúng. Rủi ro vá thấp, chỉ đổi mô tả. Độ tin cao về hành vi; không khai mẫu changes_requested hiện tại bị hỏng.

### lenh-khong-noi-hien-vat [P2] Hai ví dụ đọc tệp không khớp hiện vật vừa hướng dẫn tạo

**A01–A04, L465–466 và472–474; H3/H4 đóng đủ4 thể hiện.** Một khối không lưu stdout trước khi đọc GOI_Y_VA.diff; ba lệnh kế tiếp dùng sai chữ hoa/thường của VERDICT.md. Đây là lỗi có từ base, được tìm theo yêu cầu quét toàn tệp. H3 thêm redirect; H4 sửa đủ3 tên. Recipe diff đã chạy1→0; ba đường tệp đã kiểm1→0 trên Linux, rồi kiểm lại từ bản áp HINT. Gh thật chưa được chạy, nên không khẳng định đã tái lập toàn đường đăng PR. Rủi ro vá: redirect `>` ghi lại tệp đích đúng như mẫu artifact, không tạo quyền ghi/publish mới. Độ tin cao về lỗi nối tệp và giới hạn đã nêu.
