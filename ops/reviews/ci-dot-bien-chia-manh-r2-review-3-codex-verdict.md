verdict: approved
reviewed_sha: dcfc34f437288af909fe4954613ced44b8d9e920
nguong_ap: sensitive + chỉ thị chủ kho "đến hết P1, P2, P3"

**Kết luận: approved cho review local trên exact SHA này; không còn finding P0/P1/P2/P3 đang mở.** Finding P2 lượt 2 đã vá thật; các số liệu hiện hành khớp. Riêng sai số lịch sử 185 của spec được giữ thành erratum và đánh giá lại là không chặn W1–W3, với căn cứ nêu dưới.

Đã đo **53/53 mục tự đột biến chọn lọc**, đúng từng tập ca đích; **10/10** mutant công cụ; tự kiểm **52/52**; nhẹ **8/8**. Không suy ra đã chạy đủ 239 mutant. **A1/A4 trọn bộ trên HEAD và A7 chưa tự xác minh**; verdict không thay bằng chứng nghiệm thu còn thiếu hoặc quyền land.

## ĐỊNH DANH VÀ PHẠM VI

- HEAD như trên; tree `816c40516b5dc70e7bef302ab146812e1888da69`; base `5618f61c6ac2fa14aab52b0f5ce3d065aee8e022`.
- Spec local và Git blob `b6380bf:ops/specs/CI-DOT-BIEN-CHIA-MANH-r2.md` cùng SHA256 `9a2ab4fe746330f87ef86cc9b9a2bef6da8edde6e198a1989d415827c9fb2783`. Lease đọc từ `1efa6cf40c06e9413cd942a2260aed7b12fb8095`: r2/g1, đúng W1–W3/base, hạn 2026-09-28T15:22Z. W1–W3 không đổi giữa base spec và base lease. Lease ghi rõ chỉ thị chủ kho cho phép vượt hai lượt review; không tự cấp ngoại lệ.
- Reviewer `openai_codex / codex_cli / machine`; header CLI công bố Codex 0.157.1, `gpt-6-astra`, `xhigh`, session `01a0e3c4-8097-7063-a395-30ec9d829ce5` (`evidence/reviewer-header.txt`). Header không chứng thực model/effort của mọi request; danh tính người ký lease và effort Executor không đo độc lập được. Không dùng subagent hay kế thừa context Executor.
- Linux, Python **3.12.3**; phép đối chiếu lỗi nền có thêm Python **3.11.15**; actionlint **1.7.7**, Ruff **0.15.8**. `PYTHONDONTWRITEBYTECODE=1`; Ruff `--no-cache`; Git config fixture riêng `sandbox/git-measure.config` tắt ký commit/tag, ghim abbrev=7. Không sửa cấu hình cây review.
- `do/run_measure.py` lưu command/rc thật/thời gian vào `evidence/<tên>.json`, stdout/stderr vào `.log`. Wrapper tự trả 0; **rc bộ test lấy từ JSON**, không từ wrapper. `tk_muc.py` cũng phải đọc tuple và từng ca đích, không dùng rc helper thay kết luận. Các tiến trình chạy đồng thời; thời gian local không dùng suy thời gian CI.
- Tất cả fixture/đột biến/bản sao ở `sandbox/`, ngoài checkout `cay-kho`. Không mạng GitHub/CI, không commit/push/merge/land, không soạn payload thoát đường dẫn. Sandbox thực tế `workspace-write`, không tuyên bố checkout được mount read-only. Lịch sử ghi tăng dần giữ ở `evidence/review-progress.md`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lượt 2: `2a8af3a8bd7e4ffeb3212bc7d0d6a66daf73a637`, `VERDICT-luot-2.md`.

| Finding/biểu hiện cũ | Phân loại và mức hiện tại | Tự đo trên HEAD |
|---|---|---|
| `invalid-shard-no-execution-unobserved` [P2] | **ĐÃ VÁ THẬT**; không còn P2 trong phạm vi finding | HEAD tự kiểm 52/52. `manh-chay-truoc-xac-thuc` đỏ đúng r549,r550, 2/2; `manh-bo-tu-kiem` đỏ đúng r551, 1/1. Phản chứng độc lập thêm `chay_tu_kiem()` trước parse cũng đỏ đúng r549,r550, tuple (1,0,0). Log `mutants-new-*.log`, `early-tu-kiem.log`. Spy nay đo cả hai bộ chạy. |
| `executor-quantitative-claims` F02a [P3], số ca đo kiểu | **ĐÃ VÁ THẬT** | Bản sao `_bang_kieu -> return a == b`: **933/938**, đúng 5 ca LỌT được khai; HEAD **938/938**. Ca timeout float phân biệt kiểu thật. Log `registry-weak-types.log`, `registry-head.log`. |
| Cùng lớp, F02b [P3], numstat | **ĐÃ VÁ THẬT** trong hồ sơ hiện hành | W1 +324/−7, W2 +80/−10, W3 +46/−0; tổng +450/−17. Bảng giao lượt 3 khớp từng số (`metadata.log`). Không sửa ngược lịch sử commit/lượt 2. |
| Cùng lớp, F02c [P3 lượt 2], nền spec 185 | **CHƯA VÁ tệp spec bất biến; đánh giá lại: không chặn packet W1–W3** | Git blobs tại 5c79fa2 và 68b552d đều **200**; sai số 185 được xác nhận, không được dùng làm mẫu số nghiệm thu. Lý do và giới hạn quyết định ngay dưới. |
| `workflow-matrix-type-confusion` [P2 lượt 1] | **ĐÃ VÁ THẬT**, tái kiểm | Bool/float bị validator chặn; bản sao workflow matrix bool khiến registry thật rc=1. Tháo kiểm kiểu mới khiến năm ca LỌT. |
| `shard-json-schema` [P2 lượt 1] | **ĐÃ VÁ THẬT**, tái kiểm | 86 tình huống CLI cùng probe object cả hai trường ở cả 4 tệp: sai kiểu/schema/tập tên đều đỏ; N=2..8 hợp lệ xanh. Tháo từng chốt qua runner thật đều bị ca đích giết. |

**Phán quyết riêng về 185:** không yêu cầu Executor sửa spec đã đóng băng, không mở thêm P3 chỉ vì tệp nguồn lịch sử vẫn giữ số ấy. Đính chính kiểm được của hồ sơ review này là **nền 200 → lượt 1: 233 → lượt 2: 237 → HEAD: 239**. A1 đã quy định N lấy từ bảng thực tế; chương trình và mọi phép gộp đã đo dùng 239, không dùng 185. Vì thế sai số lịch sử không còn làm sai quyết định nghiệm thu hiện hành. Đây là đánh giá lại phạm vi chặn của F02c, **không phải** tuyên bố spec đã được sửa hoặc âm thầm đổi baseline; vẫn bảo toàn slug/lịch sử P3. Prompt khai đã báo điều phối ở comment **5857809478**; không có bản comment trong bundle và không được gọi GitHub, nên **chưa xác minh việc đăng/nội dung comment**, không dùng lời khai ấy làm bằng chứng đóng lỗi. Nếu cập nhật spec, điều phối phải làm revision/hash mới theo thẩm quyền; việc đó không thuộc patch W1–W3 này.

## BẢNG LỚP

| Slug ổn định | Biểu hiện/lịch sử | Mức còn mở | Phép kiểm đóng/đánh giá lại |
|---|---|---|---|
| invalid-shard-no-execution-unobserved | F01 lượt 2: hai stub không ghi dấu | Không | Spy có đối chứng 52/52 và hai đường chạy trước parse; mục bỏ tự kiểm đỏ đúng r551 |
| executor-quantitative-claims | F02a/b đã sửa; F02c nguồn spec giữ nguyên | Không chặn W1–W3; giữ erratum F02c | Tái lập 933/938 và numstat; đếm AST Git blobs, dùng N=239 theo A1; không nhận 185 là đúng |
| workflow-matrix-type-confusion | Lượt 1, đã đóng lượt 2 | Không | Validator + registry thật + đột biến tháo so kiểu |
| shard-json-schema | Lượt 1, đã đóng lượt 2 | Không | CLI gộp sai schema + đối chứng hợp lệ + tháo từng chốt |

## BẢNG ĐỐI CHIẾU SPEC

“Đạt phần đo” không thay thế phần nghiệm thu chưa chạy. A1/A4 đầy đủ trên exact HEAD **không được ghi pass** từ fixture, từ suite chọn lọc hoặc từ lời khai ở SHA cũ. Prompt cho phép review chọn lọc, không bắt reviewer chạy lượt đầy đủ khoảng một giờ.

| Mục | Kết luận | Bằng chứng chạy được / giới hạn |
|---|---|---|
| M1 | **Đạt phần đo** | `contracts`, `inventory`, `child-env`, `self`, `mutants-new-*`: 13 chuỗi sai rc=2 trước bộ chạy, RA vắng/rỗng được r549 đo; tên trùng cả hai bảng bị chặn; N=2..8 phủ đúng/rời nhau. 242 lần run không có hai biến mảnh; cắt thiếu mutant ⇒ rc=1, không receipt. r551 đo đúng tập truyền, cả hai bộ chạy, thứ tự tên receipt, băm, sáu số hạng, không dòng MAU_DAY_DU. |
| M2 | **Đạt phần đo** | `gop-boundaries`, `extra`, `mutants-new-*`: N=2..8 hợp lệ xanh; thiếu/thừa tệp, thiếu/trùng/chuyển tên, sai băm/kiểu/N/schema/JSON đỏ. Receipt tự dựng đủ tên/băm được nhận đúng hợp đồng, không chứng minh lịch sử chạy. Chỉ đọc `*.json`; `.txt` ngoài miền. |
| M3 | **Đạt trên toàn bộ mục mới** | 52 TU_KIEM/NHOM_BAT_BUOC/SAN_NHOM; 239 neo duy nhất. **38** mục nhắm r549–r552 + `ghi-so-gop` = **39/39**, mọi tập ca đích đúng; không tín dụng giả hoặc không đo được. Thêm mutant chạy tự kiểm trước parse cũng bị giết đúng. |
| M4 | **Đạt đường CLI** | `m4`, `contracts`: biến đúng chỉ làm bộ mục tiêu nhẹ trong 5 tình huống diff, hai bộ kia giữ nguyên; 6 giá trị lạ CLI rc=2 trước kế hoạch. Vắng/rỗng hợp lệ. Gọi thẳng hàm nội bộ bỏ parser không phải đường vào runtime. |
| M5 | **Đạt phần đo** | `registry-head`, `registry-weak-types`, `registry-no-pinned`, `registry-matrix-bool`, `extra`: workflow thật hợp lệ; 891 thay đổi tầng/kiểu/giá trị đều bị validator từ chối; tháo chốt có phản chứng LỌT. Các lệch A5 đều có p* chạy thật. |
| M6 | **Đạt tĩnh/local** | `w3`, `actionlint`: jobs khớp cấu trúc ghim, matrix/N=4, needs/artifact/permissions đúng; actionlint rc=0. Không chạy artifact Actions thật. |
| M7 | **Đạt phần đo yêu cầu** | HEAD gốc 0/300, dưới rút-lại 0/400, trả bộ sinh cũ 8/300. Nhóm 13 mục qua runner **(13,0,0)**; riêng `dau-phien-bo-vong-rut-lai` đỏ đúng r527,r528, 2/2. Không sửa đích/phân hạng (`mutants-r543.log`). |
| A1 | **not_run trọn trên HEAD** | Phân hoạch tự đo `[3,3,2,2]` / `[60,60,60,59]`, tổng 10/239. Gộp fixture phát GOP 4/4 + 10/10 + 239/239; không đồng nhất với bốn artifact từ bốn lượt đủ thật. Không xác minh rc/thời gian A1 Executor khai tại 2a8af3a, hay trạng thái “đang chạy” trên HEAD. |
| A2 | **Đạt phần đo** | Các sai lệch liệt kê đều CLI rc=1; 39 mutant chốt mảnh/gộp giết đúng ca. |
| A3 | **Đạt phần đo** | CLI sai hình/RA vắng dừng sớm; tự kiểm nay bắt chạy trước xác thực; phân hoạch đúng; r551 bắt in dòng đầy đủ. |
| A4 | **not_run trọn** | Đã đo nhẹ 8/8, TU_KIEM 52/52, DOT_BIEN thật (10,0,0), cùng **53/53** tự đột biến chọn lọc (39 mảnh/gộp + 13 quanh r543 + 1 recursion). Không dùng chúng thay 239/239 full không mảnh. Lời khai 233/233 ở 70d1698 thuộc SHA cũ. |
| A5 | **Đạt** | W2 HEAD 938/938, rc=0; các p661 đúng; chốt sai kiểu/allowlist có răng; env ci.yml ở bước bị env guard, ở job/workflow bị hash guard chặn. |
| A6 | **Đạt trong phạm vi local đã đo** | Base registry 916/916, HEAD 938/938; không mất phản chứng cũ. Ruff F với **0.15.8** base/HEAD đều sạch, delta=0. Actionlint 1.7.7 rc=0; ci.yml/BAM_GATE_REGISTRY không đổi. Chưa chạy Ruff lint đúng 0.15.15, bộ khác full hoặc Windows. |
| A7 | **not_run — sau land** | Không network/CI theo chỉ thị; chưa xác minh upload/download artifact, thời gian thật hay mục tiêu 22–25 phút. Không phải cổng land theo spec. |
| A8 | **Đạt phần đo trực tiếp và chọn lọc** | Ba phép lấy mẫu ở M7 có log/rc; 12 mục nhắm r543 + mục rút-lại qua runner thật đều giết đúng, (13,0,0). Chưa chứng minh trong A4 full như câu chữ A8; không gán pass cho phần full chưa chạy. |

## BẢNG SĂN

Lệnh dưới được bọc `python3 do/run_measure.py <label> ...`; trừ khi ghi khác, dùng Python 3.12.3. Mọi đột biến trên bản sao hoặc bản do runner sinh ngoài checkout.

| Hướng | Giả thuyết / lệnh | Output thật | Kết luận |
|---|---|---|---|
| 0 | `do/metadata.py`, băm spec/HEAD/diff/lease | SHA/hash/W1–W3 khớp; 450 dòng thêm; ci.yml không đổi | **KHÔNG PHẢI LỖI** |
| 1 | `do/probe_contracts_r2.py`: k/N lạ/trùng tên lọt | 13 input sai rc=2 trước CASE/TU_KIEM; duplicate DB/TK ValueError | **KHÔNG PHẢI LỖI** |
| 2 | `do/probe_gop_r2.py`: schema/tập tên/băm/số tệp/rác | 86 tình huống; đúng N=2..8 xanh; các phản chứng đỏ | **KHÔNG PHẢI LỖI** trong tập đã thử |
| 3 | `do/probe_extra.py`: object cả 2 trường/cả 4 tệp, tệp rác | Object rc=1; JSON rác rc=1; `.txt` bỏ qua | **KHÔNG PHẢI LỖI**; `.txt` không thuộc `*.json` |
| 4 | Fixture giả có đúng tên/băm | GOP 4/4 + 10/10 + 239/239, rc=0 | **KHÔNG PHẢI LỖI so M2**; không dùng fixture làm bằng chứng mutant đã chạy |
| 5 | `do/probe_env_children.py`: rò biến/mảnh thiếu vẫn xanh | 242 run, LEAKS=[], PARENT_VARS=[]; thiếu ⇒ rc=1, RECEIPT_EXISTS=False | **KHÔNG PHẢI LỖI** |
| 6 | `do/probe_m4.py`: giá trị lạ, lan nhẹ sang bộ khác | 6 chuỗi lạ CLI rc=2; 5 diff giữ hai bộ kia nguyên | **KHÔNG PHẢI LỖI** |
| 7 | `do/probe_contracts_r2.py`: ci.yml nhận biến mảnh | Bước bị env guard; job/workflow bị hash guard chặn | **KHÔNG PHẢI LỖI** |
| 8 | Matrix bool trên `sandbox/workflow-bool` | Registry thật rc=1, lỗi job mảnh lệch hình ghim | **KHÔNG PHẢI LỖI**, tái kiểm lỗi cũ |
| 9 | `_bang_kieu -> ==`; tháo kiểm hai job ghim | 933/938 với 5 LỌT; 928/938 với 10 LỌT; rc=1 | Chốt **có răng**, số khai lượt này đúng |
| 10 | `do/probe_extra.py`: workflow sai hình ở mọi tầng | 891/891 bị từ chối; 0 ngoại lệ/0 lọt; đối chứng gốc hợp lệ | **KHÔNG PHẢI LỖI** trong tập hữu hạn đã đo |
| 11 | `do/probe_credit_r2.py`: TypeError/no-op nhận tín dụng GIẾT | TypeError ⇒ DO_KHAC/TIN DUNG GIA; no-op ⇒ rc_con=0/TIN DUNG GIA; (0,2,0). DOT_BIEN thật (10,0,0) | **KHÔNG PHẢI LỖI** |
| 12 | `do/tk_muc.py <W1> k/3 new` và `ghi-so-gop` | (13,0,0)+(13,0,0)+(12,0,0)+(1,0,0) = 39/39 | **KHÔNG PHẢI LỖI** trên toàn bộ mục mới |
| 13 | Chạy CA/TU_KIEM trước parse, bỏ TU_KIEM | CA trước parse r549,r550 2/2; TU_KIEM trước parse r549,r550 2/2; bỏ TU_KIEM r551 1/1 | **ĐÃ VÁ THẬT** P2 lượt 2 |
| 14 | `do/do_r543.py <W1> 0 300`, `1 400`; trả generator cũ `1 300` | 0/300, 0/400, 8/300 | **KHÔNG PHẢI LỖI**, phép đo có răng |
| 15 | 13 mục r543 qua `do/tk_muc.py ... r543` | **(13,0,0)**, từng đích đúng; rút-lại r527,r528 2/2 | **KHÔNG PHẢI LỖI** |
| 16 | `tk-json-recursion-escape`, Python 3.11/3.12 base và HEAD | 3.11 cả hai (0,1,0), chết r539+r540; 3.12 cả hai (1,0,0), đúng r539 | **KHÔNG PHẢI LỖI packet**, delta=0; không tuyên bố Python3.11 full xanh |
| 17 | A1 bốn mảnh thật, A4 full, A7 runner; hướng cần payload thoát đường dẫn | Không chạy/không tự soạn theo phạm vi review | **KHÔNG ĐO ĐƯỢC / not_run**, không suy pass |

## BẢNG ĐO

| Khẳng định | Executor khai | Reviewer đo được | Khớp? |
|---|---|---|---|
| #1 `_bang_kieu` yếu | 933/938, đúng 5 ca kiểu LỌT | rc=1, 933/938; matrix-bool, matrix-float, manh-timeout-float, du-fetch-depth-false, du-timeout-float | **Có** (`registry-weak-types`) |
| #2 W2 HEAD | 938/938, TỔNG: ĐẠT | Đúng, rc=0; base 916/916 | **Có**, Python 3.12.3/config fixture đã khai |
| #3 nhóm mảnh/gộp | 39 mục GIẾT; chạy trước parse r549,r550 2/2 | 38 mục r549–r552 + ghi-so-gop, tất cả đúng đích | **Có**, 39/39 |
| #3 lịch sử sửa đích | Trước sửa đích mục ấy chỉ 38/39 | Probe lượt 2 giữ đích chỉ r549 nay trả **(0,1,0)**, ca đỏ thực tế r549,r550; mục đã sửa đích là (1,0,0) | **Tái hiện cơ chế lệch đích**; không có log nguyên gốc của lượt lịch sử 38/39 để xác thực cả run |
| #4 inventory | 239 mục, neo duy nhất, 52 ca đạt, nhẹ 8/8 | Đúng cả bốn; 52 nhóm bắt buộc/SAN_NHOM | **Có** |
| #5 numstat | W1 324/7; W2 80/10; W3 46/0; tổng 450/17 | Đúng từng tệp và tổng | **Có** |
| #6 A4 tại 70d1698 | 52/52 nhóm, 233/233 mutant, 10/10; rc=0; 5571s chạy chồng A1 | Blob đúng 233 và 52; không có log/receipt gốc để xác minh rc/5571s, không tái chạy full | **Chỉ khớp số bảng; chưa xác minh lượt chạy**; không coi là A4 HEAD |
| #7 A1 tại 2a8af3a; HEAD đang chạy | 4 mảnh 60/59/59/59, gộp 237/237; rc=0 | Bảng 237 đúng; phân hoạch toán học khớp. HEAD là 60/60/60/59, tổng239. Không đo bốn lượt thật hoặc trạng thái công việc Executor | **Chỉ khớp phân hoạch**; rc/gộp thật chưa xác minh |
| Spec §1 tại 5c79fa2/68b552d | 185 tự đột biến | **200**, đếm AST từ đúng Git blobs | **Không khớp nguồn lịch sử**; erratum và phán quyết không chặn ở trên |
| Commit 70d1698 | +33 mục, 200→233, 48→52 | AST đúng; HEAD239 gồm thêm4 ở lượt2 và thêm2 ở lượt3 | **Có** |
| Commit 2a8af3a | +5 p*, +4 kịch bản schema, 6 mutant riêng | Giữ kết quả lượt2: 5 p*; thêm5/bỏ1 mục so lượt1, net+4; sáu chốt có mutant | **Khớp cách đếm**, không hiểu là net+6 |
| Commit dcfc34f | hai mutant mới; năm ca kiểu thực sự LỌT | Diff đúng hai tên mới; đã chạy đúng r549/r550/r551; năm ca LỌT khớp | **Có** |
| M7/A8 | Generator hẹp, không lặp liên tiếp, hết chết lây | HEAD0/300 gốc, 0/400 mutant; generator cũ8/300 | **Khớp tính chất**; số lỗi ngẫu nhiên không cần bằng10/300 nền |

## FINDINGS

**Không có finding P0/P1/P2/P3 còn mở trên diff được review.** Không có patch gợi ý vì không có lỗi code mới cần vá. F02c lịch sử được giữ thành erratum và đánh giá lại tường minh ở trên; không coi 185 là số đúng và không tuyên bố đã sửa tệp spec.

Kiểm chứng log độc lập `do/final_audit.py`: **53 tên duy nhất**, tập ca đỏ của từng mục bằng đúng bảng hiện hành; không dòng tín dụng giả/không đo được trong sáu log chọn lọc Python3.12 (`evidence/selected-audit.json`). Các phản chứng cố ý sai được ghi riêng, không trộn vào con số 53/53.

## GIỚI HẠN VÀ KIỂM READ-ONLY

- A1/A4 trọn bộ trên exact HEAD, A7 GitHub/artifact/thời gian, Ruff lint đúng pin CI 0.15.15 và Windows **chưa xác minh**. Các khẳng định Executor về run cũ không có log gốc trong bundle; thiếu phép đo không được đổi thành “khai sai”, cũng không được ghi pass.
- Hàm `ke_hoach` nội bộ có thể nhận tham số chưa validate nếu gọi trực tiếp; đường CLI đã validate trước. `doc_bien_manh` nhận falsey phi chuỗi trong dict giả không đại diện `os.environ` chỉ chứa chuỗi. Không nâng hai trường hợp giả lập ấy thành lỗ runtime.
- Đảo thứ tự các tên trong receipt giữ nguyên tập phủ vẫn phù hợp M2. JSON sai phần tử kiểu object có thể trả traceback TypeError; vẫn rc≠0, không phát bằng chứng đủ, không phải đường fail-open.
- Snapshot đầu/cuối: **2251/2251** tệp ngoài `.git`, **0 thêm/xóa/đổi**; HEAD/tree giữ nguyên; status tracked/untracked/ignored và diff/index rỗng (`evidence/checkout-verification.json`). Chỉ chứng minh không có delta giữa hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Mirror chỉ đọc; chưa có snapshot mirror đầu phiên nên không tuyên bố kiểm toàn bộ mirror bằng hai mốc.
- Review local và quyền land là hai việc riêng. Verdict không cấp phép CI/merge/land, không tự tạo `human_audited`, và hết hiệu lực nếu HEAD đổi.
