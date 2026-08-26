verdict: changes_requested
reviewed_sha: f16b6bf9d6085bd1923db9800090faaed1ffdd1b

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `quan-sat-mang-van-thanh-rang-buoc`: VÁ HỜ — dòng 699–703 đã đổi “Ràng buộc” thành điều kiện mặc định và nói cách đóng gói ngữ cảnh đúng bất kể cờ; nhưng bảng dòng 687–693 vẫn ghi mạng đóng là **quan sát** trong cột `DỰA VÀO`, rồi nói thẳng đó là thứ quy trình dựa vào. `if sed -n '656,675p' cay/GOI_AGENT_DA_NEN.md | rg -q 'CƠ CHẾ NAY ĐÃ BIẾT' && sed -n '687,693p' cay/GOI_AGENT_DA_NEN.md | rg -q 'mạng đóng = \*\*quan sát\*\*'; then false; fi` trả `rc=1`: cách xếp hạng mới và bảng vận hành chưa đọc xuôi được với nhau.
- `mo-ta-sandbox-cu-choi-phan-hang-moi`: VÁ SINH LỖI MỚI — executor đúng ở điểm câu trả lời về cờ đã có sẵn tại dòng 328–342 và bản vá nay gọi đúng tên `sandbox_workspace_write.network_access` ở dòng 656–672. Tuy nhiên chính phần vá để lại tiêu đề dòng 645 “QUAN SÁT, chưa phải hàng rào”, dòng 657 “cơ chế đã xác minh”, và dòng 689–693 lại “quan sát chưa rõ cơ chế”. Ngoài ra dòng 649 khai `git ls-remote rc=128` còn dòng 664 khai `rc=0` cho cùng `workspace-write` mặc định. Đây là lỗi mới ngay trong phần vá, không còn là lỗi “chưa biết vì sao” của vòng 1.
- `dieu-kien-do-thieu-phien-ban-codex`: ĐÃ VÁ THẬT — dòng 658 có liền nhau ngày `26-08-2026`, `codex-cli 0.149.1` và `-s workspace-write`; assertion `sed -n '658p' cay/GOI_AGENT_DA_NEN.md | rg -q 'Đo [0-9]{2}-[0-9]{2}-[0-9]{4}, `codex-cli [0-9]+\.[0-9]+\.[0-9]+`, `-s workspace-write`'` trả `rc=0`, bỏ version trong mutation thì `rc=1`.
- `tieu-de-bon-tang-van-rong-hon-than`: ĐÃ VÁ THẬT — tiêu đề dòng 621 chốt cả nơi đo lẫn đối tượng “QUYỀN GHI VÀO KHO”; dòng 623–627 giải thích phản ví dụ `--allowedTools`. Assertion phạm vi/đối tượng trả `rc=0`, mutation hoàn nguyên về phủ định toàn xưng trả `rc=1`.
- `ba-hang-khong-phu-het`: VÁ SINH LỖI MỚI — bảng thật có 5 hàng và đã thêm chiều MỞ/ô dư, nên ca proxy mở của vòng 1 có chỗ. Nhưng dòng 592/602 vẫn tự gọi “Ba HẠNG/Ba hạng”; các hàng không tạo phân hoạch khi một control vừa đóng theo mặc định vừa mở bằng cờ; và không có lần dùng `chưa xếp được` nào sau dòng 620 dù bên dưới còn câu không mang đúng một nhãn. `sed -n '604,610p' cay/GOI_AGENT_DA_NEN.md | rg -c '^\| \*\*'` = `5`, trong khi detector đối chiếu lời “ba” trả `rc=1`.
- `nhan-hang-cu-ngoai-diff-bi-thieu`: ĐÃ VÁ THẬT — dòng 594–597 giới hạn taxonomy vào control của mục này và gọi tên đủ ba ngoại lệ cũ ở dòng 21/435/296. Quét toàn tệp hiện cho `ranh giới=9`, `hàng rào=6`, `cưỡng chế=5`; các cách gọi cũ ngoài mục không còn bị ngầm bắt mang hạng.
- `n5-grep-khong-giu-duoc-nghia`: ĐÃ VÁ THẬT — PR đã rút lời chứng bằng ba grep; ba P2 hiện còn đúng nghĩa ở dòng 553–576. Tôi đảo riêng từng ý “ví dụ thứ sáu khác nguyên nhân”/“log không được git theo dõi”/“nhân quả chưa chứng minh”: mỗi lần các chuỗi neo vẫn cho `rc=0`, đánh giá mệnh đề tương ứng đỏ (`rc=1`), còn `doc-claims-check --strict --path ...` vẫn `ok=true, rc=0`. Như vậy N5 chỉ có răng ở phép review nghĩa, đúng như executor nay khai, không còn bị trình bày như răng của grep.
- `n7-khong-co-duong-do-trong-write-set`: VÁ HỜ — phép bác một phần là thật: baseline `doc-claims-check --strict` quét 105 tệp, roots có `docs`, và mutation tham chiếu nội-cây không tồn tại trên đúng bản sao packet cho `ok=false`, `L1/PATH_MISSING`, strict `rc=2`. Nhưng N7 trong `SPEC.md:91` chỉ gọi `doctrine-scan` và “delta gate”; cùng mutation cho `doctrine-scan --root . --path <bản-sao>` = 8 tệp/0/`rc=0`, còn `--root .` = 7 tệp/0/`rc=0`; CLI không có lệnh delta. Vì vậy phải thu hẹp finding vòng 1 từ “không gate nào có răng” xuống “hai phép N7 nêu không có răng”.
- `lease-trang-thai-hien-tai-khong-nhat-quan`: ĐÃ VÁ THẬT — `LEASE.yaml:62` khớp exact head; dòng 70–72 có đúng 2 mốc review; `da_dung=187`, trần 200, và câu “chưa có dòng nào” đã biến mất. `rg -n 'reviewed_sha_required|lich_su_reviewed_sha|da_dung|chưa có.*dòng' LEASE.yaml` xác nhận các trường trên và 0 hit cho câu cũ.
- `mirror-ref-count-khong-khop`: ĐÃ VÁ THẬT — `git ls-remote --heads kho.git` = 214; đúng 1 ref tên `refs/heads/HEAD`; bỏ nó còn 213. `cay-kho` có 213 remote-tracking ref không-symref và `comm -3` giữa hai tập sau chuẩn hóa = 0. Lời “213 trước clone” là lịch sử không đo lại được, nhưng mô tả bundle hiện tại đã đúng và không còn gọi hai tập thô là y hệt.

## BẢNG ĐO

| khẳng định | PR/EVIDENCE khai | tôi đo được | khớp? |
|---|---|---|---|
| Danh tính packet/PR/head | #318, PR #322, head `f16b6bf` | `git -C cay-kho rev-parse HEAD` = `f16b6bf9d6085bd1923db9800090faaed1ffdd1b`; trạng thái #318/#322 cần GitHub | SHA: có; Issue/PR: `KHÔNG_ĐO_ĐƯỢC` |
| Finding vòng 1 | 7 P1 + 3 P2 | đếm header finding trong `VERDICT_VONG_1.md` = 10, tách 7 P1 + 3 P2 | có |
| Phạm vi diff | 187/0, đúng 1 tệp | `git diff --numstat c35ae1c..f16b6bf` = `187 0 docs/GOI_AGENT_DA_NEN.md`; name-only = 1 | có |
| `diff.patch`/`numstat.txt` | hiện vật của diff | `numstat.txt` đúng `187 0`; SHA-256 của `diff.patch` và output `git diff --binary` cùng là `4aca9e…f30f5bf`; `git diff --check` rc=0 | có |
| Số dòng nền/head (PR bỏ sót) | không khai | 544 ở `c35ae1c`, 699 ở vòng 1, 731 ở head; `544+187=731` | số mới, có |
| Delta riêng vòng vá 2 (PR bỏ sót) | không khai | `git diff --numstat 48cf331..f16b6bf` = 46 thêm/14 xóa, ròng +32 | số mới, có |
| Lease hiện hành | trần 200, dùng 187; trần cũ 165 bị vượt | `LEASE.yaml` = 200/187; `187>165`, còn biên 13 | có |
| Lịch sử trần | 120 → 165 → 200, hai lần S2 | hai khối `nang_tran` ghi đúng 120→165 và 165→200; lịch sử dừng/ủy quyền không có log độc lập | trường: có; lịch sử: `KHÔNG_ĐO_ĐƯỢC` |
| ADR sensitive | 3 tệp/300 thêm; patch 1/187, biên 113 | `ADR_0044.md` = 3/300; `300-187=113` | có |
| Bảng phân hạng | 5 hàng | đếm dòng dữ liệu 604–610 = 5 | có về số hàng |
| Lời tự đếm hạng trong tệp (PR bỏ sót) | không khai; tệp nói “Ba HẠNG/Ba hạng” | bảng có 5 hàng, không phải 3 | không; finding |
| Tiêu đề `####` (PR bỏ sót) | không khai | 7 | số mới, có |
| Từ khóa taxonomy toàn tệp (PR chỉ khai scope) | không khai số | `ranh giới` 9, `hàng rào` 6, `cưỡng chế` 5 lần | số mới, có |
| Ô `chưa xếp được` | có ô dư và phải gọi tên khi dùng | 3 lần xuất hiện, đều ở định nghĩa/giải thích dòng 610/618/619; 0 lần áp cho câu sau dòng 620 | số hàng: có; sử dụng: không |
| Điều kiện phép đo mới | version + ngày + mode ngay cạnh | dòng 658 = `26-08-2026`, `codex-cli 0.149.1`, `-s workspace-write` | có |
| “cách ba trăm dòng” | cờ đã được ghi cách khoảng 300 dòng | cờ ở dòng 334, lời nối lại ở 667–668: khoảng cách 333–334 dòng | có nếu hiểu là số tròn; không phải 300 chính xác |
| Bảng probe mạng mới | bind 1→0; urllib 1→0; git 0→0 ở hai cấu hình | bundle không có raw command/probe/log và tôi không có hai phiên Codex tương ứng để chạy A/B | `KHÔNG_ĐO_ĐƯỢC` |
| Bảng cũ so bảng mới | git cũ 128, mới 0; khai chưa biết vì sao | chính tệp giữ `workspace-write git ls-remote rc=128` ở 649 và `rc=0` mặc định ở 664 | số chép: có; nguyên nhân: `KHÔNG_ĐO_ĐƯỢC`; văn bản tự mâu thuẫn |
| Gate `doc-claims-check` baseline | rc=0; roots có docs | `ok=true`, 105 tệp, 359 advisory/claim, `flags=[]`, `layers_skipped={}`, strict rc=0 | có |
| Răng L1 trên đúng tệp packet | `ok=False`, L1/PATH_MISSING | mutation tham chiếu nội-cây không tồn tại trên `cay/GOI_AGENT_DA_NEN.md`: 1 tệp, 1 flag L1/PATH_MISSING, strict rc=2 | có; PR bỏ sót rc=2 |
| Ba mutation doc-claims khác | SHA 8, SHA 40, test-name đều không bắn | không có chuỗi, vị trí chèn hay raw output trong bundle | `KHÔNG_ĐO_ĐƯỢC` |
| Gate `doctrine-scan` baseline | rc=0 | 7 tệp, 0 chỗ chép, rc=0 | có |
| N7 “delta gate” | delta so `origin/master` = 0 | `packet_loop.py --help` không có subcommand delta; SPEC/PR không nêu lệnh, output hay đơn vị | không đo được như một tiêu chí; finding |
| Mirror trước clone | 213 = 213, comm rỗng | trạng thái lịch sử trước clone không nằm trong bundle | `KHÔNG_ĐO_ĐƯỢC` |
| Mirror trong bundle | 214 head, 1 ref `HEAD`, còn 213; clone 213 non-symref | lần lượt 214/1/213/213; `comm -3` = 0 dòng | có |
| Mirror cấu hình | full, abbrev 7, head f16, origin HTTPS | `false`; `7`; exact f16; đúng URL HTTPS | có |
| CI run exact head | gate đang chạy id 32969274969; ops skipped id 32969267926 | không có metadata Actions trong bundle | `KHÔNG_ĐO_ĐƯỢC` |
| Workflow ops | chỉ push `ops/**` | `.github/workflows/ops-open-pr.yml` đúng trigger ấy | có về cấu hình, không về run |
| Windows | PR thường chỉ Ubuntu | ma trận `ci.yml` chỉ thêm Windows cho dispatch/master/nhãn `windows` | có về cấu hình/không đo run này |
| Chữ ký hai commit packet | `48cf331` chưa ký; từ `f16b6bf` ký | raw commit: `48cf331` có 0 header `gpgsig`, `f16b6bf` có 1; `f16b6bf^=48cf331` | có cho hai commit |
| “48cf331 và 22 commit khác của phiên” | 23 commit cũ chưa ký | nhánh packet từ base đến head chỉ có 2 commit; tập “của phiên” không được định nghĩa để chọn 23 commit trên mọi ref | `KHÔNG_ĐO_ĐƯỢC` |
| “48cf331 neo bởi ba hồ sơ” | verdict, receipt, head PR | verdict và receipt đều neo exact `48cf331`; remote ref packet/head hiện là exact `f16b6bf`, còn `48cf331` chỉ là cha | không; chỉ 2 neo exact đo được |
| Ba `stdout.log` | không có trong kho | `git ls-files '*stdout.log'` = 0 | có về sự vắng mặt; số usage bên trong vẫn `KHÔNG_ĐO_ĐƯỢC` |
| N1 mutation | bỏ phạm vi/đối tượng khỏi tiêu đề phải đỏ | detector scope: baseline rc=0, mutant rc=1; doc-claims trên mutant vẫn rc=0 | có răng review mục tiêu |
| N2 mutation | bỏ/mislabel một hạng phải đỏ | detector nhãn mục tiêu: baseline 0, mutant bỏ `HẠNG` = 1; nhưng detector nhất quán baseline đã rc=1 do “quan sát” và “cơ chế đã biết” cùng tồn tại | bản hiện tại đã đỏ; finding |
| N3 mutation | đổi lại cột cưỡng chế phải đỏ | detector header: baseline 0, mutant 1; detector đọc chéo baseline đã 1 vì bảng vẫn gọi mạng là quan sát | có răng cú pháp, bản hiện tại đỏ về nghĩa |
| N4 mutation | bỏ version/ngày/mode phải đỏ | detector điều kiện baseline 0; bỏ version = 1 | có răng review mục tiêu |
| N5 mutation | đảo nghĩa từng P2 phải đỏ | 3/3 ca: chuỗi neo rc=0, assertion mệnh đề rc=1, doc-claims rc=0; bản gốc cả ba assertion rc=0 | có răng ở review nghĩa, không ở gate cơ học |
| N6 mutation | hunk ngoài write set phải đỏ | baseline bản sao có 1 path; thêm path thứ hai ngoài write set làm detector count rc=1; không thể phá N6 chỉ bằng sửa tệp được phép | có răng |
| N7 mutation | phá tiêu chí phải đỏ | doc-claims rc=2 nhưng không thuộc câu chữ N7; doctrine root/explicit-path đều rc=0, CLI không có delta | N7 vẫn không có đường đỏ riêng |
| Mạng lớp reviewer lượt này | phải tự đo, kết quả phụ thuộc cấu hình | lệnh được giao in 0 dòng ref, 1 dòng fatal ở stderr, rồi `rc=128` | đã đo: rc=128, 0 dòng ref |

### phan-hang-mang-tu-mau-thuan  [P1]  Phần mạng mới tự gán hai hạng và hai kết quả cho cùng điều kiện

TỆP/DÒNG: `cay/GOI_AGENT_DA_NEN.md:645-675,685-703`

VẤN ĐỀ: Tiêu đề nói đây là “QUAN SÁT, chưa phải hàng rào”; thân ngay dưới nói “CƠ CHẾ NAY ĐÃ BIẾT” và gán `cơ chế đã xác minh — chiều ĐÓNG`; bảng hai pha lại gán mạng đóng là `quan sát`, rồi dòng 692–693 gọi nó là quan sát “chưa rõ cơ chế”. Riêng `workspace-write` mặc định còn mang `git ls-remote rc=128` ở bảng dòng 649 và `rc=0` ở bảng mới dòng 664. Đoạn `CHƯA ĐO ĐƯỢC` giải thích chưa biết vì sao hai số lệch, nhưng không biến hai mệnh đề hiện tại thành cùng đúng; bảng cũ cần được đánh dấu lịch sử/thu hồi ngay tại chỗ hoặc bỏ khỏi bảng vận hành. N2/N3 vì thế chưa đạt.

ĐÃ THỬ VÁ: không — reviewer không sửa nhánh; hướng tối thiểu là tách từng transport/điều kiện đo, thu hồi số cũ tại chính bảng, rồi dùng một hạng nhất quán trong bảng hai pha.

ĐÃ THỬ NGHIỆM: `if sed -n '656,675p' cay/GOI_AGENT_DA_NEN.md | rg -q 'CƠ CHẾ NAY ĐÃ BIẾT' && sed -n '687,693p' cay/GOI_AGENT_DA_NEN.md | rg -q 'mạng đóng = \*\*quan sát\*\*'; then false; else true; fi` ⇒ `rc=1`. Lệnh mạng lớp reviewer được giao ⇒ `rc=128`, 0 dòng ref; kết quả đó chỉ là quan sát lượt này, không phân xử hai bảng lịch sử.

ĐỘ TIN: cao

### nam-hang-khong-tao-phan-hoach  [P1]  Ô dư làm phủ hết theo định nghĩa nhưng bảng vẫn không loại trừ và không xếp hết theo nghĩa

TỆP/DÒNG: `cay/GOI_AGENT_DA_NEN.md:592-619,621-697`

VẤN ĐỀ: Ba hàng đầu chưa được chứng minh loại trừ nhau vì đơn vị phân loại không được định nghĩa: cùng control mạng đóng ở mặc định nhưng mở khi truyền cờ; cùng một hàng phép đo chứa cả hai điều kiện nên có thể rơi vào cả chiều ĐÓNG lẫn MỞ. Các claim `--allowedTools` chặn theo hình dạng nhưng mở theo thẩm quyền, `workspace-write` ghi ngoài cây, và `claude -p` mở đều không được gọi `chưa xếp được`; thực tế chuỗi ấy chỉ xuất hiện ba lần trong định nghĩa trước dòng 620. Ô dư không làm bảng hoàn toàn “không thể sai”: vẫn có thể bác bằng câu không nhãn hoặc đa nhãn, và bản hiện tại có cả hai. Nhưng ô dư làm tính “phủ hết” thành đúng hiển nhiên, nên tiêu chí có nghĩa phải là phân hoạch nhất quán và gọi tên ca dư, không phải chỉ đếm 5 hàng. Tệp còn tự nói “Ba HẠNG/Ba hạng” trước bảng 5 hàng.

ĐÃ THỬ VÁ: không — cần định nghĩa đơn vị là claim đã kèm điều kiện (không phải control trần), sửa số hạng, rồi audit từng claim sau dòng 620; ca chưa phân xử phải thật sự mang nhãn dư.

ĐÃ THỬ NGHIỆM: đếm hàng = 5; `rg -n 'chưa xếp được' cay/GOI_AGENT_DA_NEN.md` chỉ trả dòng 610/618/619; detector “ba hạng = ba hàng” trả `rc=1`; detector đối chiếu nhãn mạng giữa dòng 645/657/689–693 cũng `rc=1` ngay trên baseline.

ĐỘ TIN: cao

### n7-doc-claims-khong-phai-phep-n7  [P1]  Phản chứng L1 có thật nhưng không làm hai phép nghiệm thu N7 đỏ

TỆP/DÒNG: `SPEC.md:91`; `cay-kho/.claude/dev/packet_loop.py` (CLI `doctrine-scan`); `cay-kho/scripts/tl_core/workflow.py:817-824,1161-1212,1416-1487`

VẤN ĐỀ: Executor đã bác đúng phần rộng quá của finding vòng 1: `doc-claims-check` thật sự phủ `docs/` và có răng L1 trên tệp packet. Nhưng N7 không nêu cổng đó; nó nêu `doctrine-scan --root .` và một “delta gate” không có lệnh. Đột biến L1 chỉ chứng minh một tiêu chí khác có răng cho một lớp con trỏ chết, không chứng minh N7 có thể đỏ. Ba đột biến executor tự khai không bắn càng cho thấy răng ấy hẹp.

ĐÃ THỬ VÁ: không — hướng sửa là đưa command/assertion `doc-claims-check` vào chính N7 với phạm vi răng đã khai, hoặc định nghĩa delta command thật; không nên gọi một cổng ngoài tiêu chí là bằng chứng tiêu chí đã có răng.

ĐÃ THỬ NGHIỆM: mutation tham chiếu nội-cây không tồn tại ⇒ doc-claims strict `rc=2`, `L1/PATH_MISSING`; cùng bản sao ⇒ `doctrine-scan --root . --path ...` quét 8 tệp/0/`rc=0`; lệnh N7 đúng nguyên văn quét 7 tệp/0/`rc=0`; `packet_loop.py --help` không có subcommand delta.

ĐỘ TIN: cao

### probe-mang-moi-khong-tai-lap-duoc  [P2]  Bảng ba dòng làm lật doctrine nhưng bundle thiếu chính lệnh và raw log

TỆP/DÒNG: `PR_VONG_2.md:23-39`; `EVIDENCE.md:65-76`; `cay/GOI_AGENT_DA_NEN.md:656-675`

VẤN ĐỀ: Sáu mã thoát bind/urllib/git là nền của thay đổi phân hạng lớn nhất vòng 2, nhưng bundle chỉ ghi “cùng một probe”, không có command, fixture hay raw output. Tôi chỉ đo được lớp hiện tại theo phép E (`git ls-remote rc=128`, 0 dòng), không dựng được hai phiên `codex-cli 0.149.1` với cờ mặc định/bật để xác nhận bảng. `KHÔNG_ĐO_ĐƯỢC` là kết quả hợp lệ, nhưng doctrine hiện trình bày bảng mới như phép đo đã đủ phân xử trong khi review bundle không cho reviewer tái lập nó.

ĐÃ THỬ VÁ: không — không thể tự bịa raw log; cần kèm command/probe không chứa dữ liệu nhạy cảm và output hai lượt, hoặc hạ lời khai thành số đo một phiên chưa kiểm chéo.

ĐÃ THỬ NGHIỆM: lệnh E đúng nguyên văn ⇒ stderr 1 dòng, stdout ref 0 dòng, `rc=128`. Tìm trong PR/EVIDENCE chỉ thấy bảng kết quả, không có thân probe để chạy lại.

ĐỘ TIN: cao về thiếu bằng chứng; vừa về bản thân sáu mã thoát

### ba-neo-cua-48cf331-dem-sai  [P2]  Head PR không còn là neo exact của commit vòng 1

TỆP/DÒNG: `PR_VONG_2.md:63-66`; `EVIDENCE.md:90-92`; `LEASE.yaml:111-119`

VẤN ĐỀ: Hồ sơ nói `48cf331` được neo bởi verdict, receipt và “head PR này”. Verdict và receipt thật sự ghi exact `48cf331`; nhưng ref packet trong mirror hiện trỏ exact `f16b6bf`, đúng như chính PR/EVIDENCE khai, còn `48cf331` chỉ là cha. Quan hệ tổ tiên giữ commit tra được nhưng không phải “head PR” hay neo exact thứ ba. Con số “48cf331 và 22 commit khác của phiên” cũng không tái lập được vì tập commit “của phiên” không được định nghĩa; riêng lineage packet chỉ có hai commit từ base đến head.

ĐÃ THỬ VÁ: không — sửa lời khai thành hai neo exact cộng một quan hệ ancestry, và định nghĩa ref/range nếu vẫn cần con số 23.

ĐÃ THỬ NGHIỆM: `git -C cay-kho rev-parse refs/remotes/origin/claude/doctrine-ranh-gioi-reviewer-exec-1` = `f16b6bf…`; `git merge-base --is-ancestor 48cf331 f16b6bf` = rc=0; receipt lấy từ history ghi `reviewed_sha: 48cf331…`; raw commit cho `48cf331` 0 `gpgsig`, `f16b6bf` 1 `gpgsig`.

ĐỘ TIN: cao cho số neo; vừa cho tập 23 commit vì phạm vi “phiên” không được định nghĩa

## CHỖ TÔI KHÔNG ĐO ĐƯỢC

- Không có metadata/API GitHub trong bundle nên không xác nhận được trạng thái Issue/PR, hai run id, trạng thái gate đang chạy/skipped, comment, nhãn Windows hoặc lịch sử ref trước clone.
- Không có thân probe/raw log cho bảng mạng mới và không có hai phiên `codex-cli 0.149.1` tương ứng; chỉ đo được lớp của reviewer hiện tại: `rc=128`, 0 dòng ref.
- Không có payload/vị trí/raw output của ba mutation doc-claims còn lại, nên không xác nhận độc lập lời “SHA 8/SHA 40/test-name đều không bắn”.
- Không có cách xác định tập “22 commit khác của phiên”, lịch sử `gpgsign=false`, hay lần thử ký `rc=0`; chỉ kiểm được signature header của hai commit packet.
- Không có raw `stdout.log`, log dừng S2, hoặc bằng chứng độc lập cho hai quyết định nâng trần; kiểm được trạng thái lease hiện hành và phép tính kích thước, không kiểm được lịch sử thao tác/ủy quyền. Trích protocol được cấp chỉ có §8, không có §2 để thẩm định độc lập lời viện dẫn authority.
- Theo ràng buộc, tôi không soạn nội dung dựng đường dẫn thoát khỏi cây hay payload tấn công. Mutation N7 dùng một tham chiếu nội-cây không tồn tại; các hướng nguy hiểm hơn chỉ được mô tả bằng lời.
