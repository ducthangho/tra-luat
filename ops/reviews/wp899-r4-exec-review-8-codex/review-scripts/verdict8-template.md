verdict: changes_requested
reviewed_sha: 431681270298ffab8edcd316bdf26670157b4b4e
base_sha: ba222ffd1615f0d74b59985b9612f725211b62f5
Reviewed commit: 431681270298ffab8edcd316bdf26670157b4b4e
reviewed_tree: 9e88f11b3ead6c32ea664546ef6e8124e56eb37f
packet: wp899-r4-g4
generation: 4
spec_hash: be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45
review_class: sensitive
review_round: 8
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI-published)
effort: xhigh (CLI-published)
session_id: 01a1740b-667c-72a1-bd1d-1556c277e8ed
execution_surface: codex_cli
transport: machine
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
assurance: review_deferred

**V2 chưa đạt: P0=0, P1=0, P2=1 theo lớp. F10 còn mở ở một lỗ bộ sinh đã đo được theo mục 3(a) của assignment.** Mã sản phẩm HEAD xử lý đúng phản chứng mới; không biến lỗi của mutant thành lỗi sản phẩm. D02/P3 được giữ theo quyết định chủ kho. Không tự cấp approval, quyền vá, lượt gọi tiếp theo hay quyền land.

## Authority và preflight

Đã đọc prompt offline, toàn bộ spec r4 và các định nghĩa/mục tiêu/nghiệm thu dẫn từ r2/r3; CONTEXT, protocol, CLAUDE, kế hoạch đa provider và adapter cross-review. Spec authoritative của lượt này là bản đóng băng được user chỉ định `.review-input/wp899-r4.md`: SHA-256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45`, khớp. r3/r2 lần lượt `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f` / `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707`.

Checkout độc lập, detached HEAD/tree như đầu verdict; origin `https://github.com/ducthangho/tra-luat.git`, shallow, `core.abbrev=7`. `git merge-base --is-ancestor <base> HEAD` rc0. Immutable acceptance baseline là `ba222ffd…`; candidate là `43168127…`; lượt trước `9b329bfa…` chỉ là mốc đối chiếu, không dời baseline. Spec/lease/ref/state GitHub hiện tại và chi phí provider ngoài bundle **KHÔNG ĐO ĐƯỢC offline**; dùng authority đóng băng user giao, không khai đã readback GitHub.

Diff base→HEAD đúng hai tệp effective write set g4: `ops/ci_provenance.py` +444, `ops/ci_provenance_test.py` +1582, tổng **2026**, trong trần khoảng 2050 do checkpoint cấp. `git diff --check <base> HEAD` rc0. `.claude/dev/ci_dang_ky_test.py` bằng base; registry đỏ là giới hạn đã khai, không là finding mới và không được ghi thành pass.

**Đính chính lời dẫn về delta:** `git diff 9b329bf HEAD -- ops/ci_provenance.py` có thay đổi hai regex `TS` và `RE_GIO`, từ chữ số Unicode `\d` sang `[0-9]`; sản phẩm không hoàn toàn bất biến so lượt 7. Đã kiểm c51, lịch sử timestamp và replay A10 trên chính HEAD này. Đây là ghi nhận phạm vi, không tự nâng thành finding.

Áp Q1–Q12, tiêu chí phân hạng, D01, checkpoint lượt 7, trần dòng và **lời gọi 8/10** theo assignment. Không lấy `limit: 8` trong lease hay V5 cũ để bác quyết định chủ kho mới được giao. Không mở lại D02. Không suy ngân sách lịch sử chưa đo được thành 0.

Môi trường: Linux x86_64, Python3.13.17, PyYAML6.0.3, Git2.43.0, Ruff0.15.15, codex-cli0.164.0. `runtime8-results.json` đọc đúng `session_meta`/`turn_context` của rollout cùng thread/cwd: model và effort là **CLI công bố**; model phục vụ từng request **KHÔNG ĐO ĐƯỢC**. Executor Claude theo assignment, không phải suy từ actor GitHub. Sandbox thực tế workspace-write, mạng restricted/offline, approval never, `.git` read-only. Probe `codex --version` rc0 có cảnh báo không tạo được PATH aliases do read-only; không sửa trust/permission để bỏ cảnh báo. Launcher receipt, stdout `thread.started` và hash rollout sau khi process kết thúc phải do bên vận chuyển đóng băng; A13 chưa hoàn tất từ bên trong lượt đang chạy.

## BẢNG LỚP

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |
|---|---|---|---|---|---|
| F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` | **P2, còn mở** | `ops/ci_provenance_test.py:1438` không có toán tử cho `ExceptHandler.type`/tuple ngoại lệ; `:484` chỉ khóa nửa YAML error của A18. Guard đúng ở `ops/ci_provenance.py:160`. | Bỏ **riêng một phần tử** `RecursionError` khỏi `(yaml.YAMLError, RecursionError)`: mutant sống **52/52**, HEAD trả None / Gate not_measured, mutant ném RecursionError trên cùng YAML lồng sâu 1201 byte. `gap8-results.json`, `gap8-all52.json`, `gap-e2e8-results.json`; command/rc/hash ở `generator-gap.json`, `gap-e2e.json`. | Vá tại **bộ test/bộ sinh**, vì sản phẩm đang đúng. Đường rẻ: thêm phép bỏ từng ngoại lệ trong tuple của ExceptHandler và một ca A18 phân biệt riêng RecursionError; fixture/fault injection phải được đưa tới đúng reader sau khi dựng REST/log đối chứng. Khóa bằng mutant vừa đo, chỉ nhận TinHieuChotCa đúng ca. Không mở rộng catch thành Exception để làm test xanh. Nguy cơ: độ sâu phụ thuộc recursion limit/PyYAML; mock toàn cục quá sớm làm hỏng fixture thay vì đo reader; chỉ lấy rc khác 0 sẽ cấp tín dụng giả. | khoảng **8–18**; còn 24 dòng dưới trần 2050, phải đo lại, không tự nới scope/trần |
| D02 `uses-nhieu-dong` | P3, nợ theo quyết định | `ops/ci_provenance.py:174` giữ dòng đầu cho uses nhiều dòng. | `history7-copy.py`, ca `name_uses_whole_value`; không có bằng chứng runner thật mới. | **Giữ theo quyết định chủ kho** trong assignment, owner `ducthangho`; không yêu cầu sửa ở wp899, không mở lại thành P1/P2. Hướng xử lý về sau cần scope/authority riêng nếu muốn đổi miền uses malformed. | 0 ở lượt này |

Một lớp P0–P2 mở, một biểu hiện mới. Không đổi slug F10 để xóa lịch sử. Các 32 biểu hiện P1 lượt 7 được vá thật, nhưng **cả lớp chưa đóng** vì lỗ mới được assignment yêu cầu tìm ở bộ sinh.

### Phản chứng F10/P2 và tại sao đúng hạng

Toán tử bậc một tự nhiên: xóa một phần tử của danh sách ngoại lệ được bắt; AST là `ExceptHandler.type = Tuple`. Bản sao mutant chỉ bỏ `RecursionError`, không sửa fixture hay đầu ra mong đợi. `sinh_dot_bien_dong` không tạo phép này. Tập đóng không có survivor này nên không gọi nó là P1 “một mã trong tập đóng sống”; nó là **P2 lỗ bộ sinh**, đúng ngoại lệ mục 3(a)/7 của prompt.

`python -B .review/run8.py generator-gap python -B .review/gap8.py` rc0: mutant 52/52 xanh. Input gồm 600 mức list YAML, 1201 byte, SHA-256 `250f8f81de72fe62fb3c3202430524b7a6938c02969b8be425e8b265d6899eea`; không cần mạng, shell, đường dẫn hay sửa nội dung tin cậy trên HEAD. HEAD `doc_wf` trả None, mutant ném RecursionError; đối chứng YAML sai cú pháp thường đều trả None ở cả hai. Phép đo kiểm riêng nhánh bị bỏ.

`python -B .review/run8.py gap-e2e python -B .review/gap_e2e8.py` rc0: với REST/log hợp lệ và cùng workflow không đọc được, HEAD ra `ghep_buoc.not_measured`, lý do `workflow_tai_sha_khong_doc_duoc`, không marker; mutant ném RecursionError qua đường thu thật. Đây là tính chất A18 “không ném”, không phải suy luận từ tổng số ca. Mã nguồn mutant SHA-256 `321d2374d0fc228b386238c77c2e04db37aa2a84e8e7b3b1a79765eb7455f934`.

## Kiểm bộ sinh và phân hạng

`audit8.py` tái dựng độc lập việc duyệt/chỉnh/compile: **1009** mutant có hiệu lực, 0 lỗi compile bị bỏ, 0 trùng ID; hai phép `return None` đã bằng nguồn gốc (`doc_wf#12`, `_gio#7`) được loại như phép không đổi mã. Có **13 cặp nguồn trùng**, nhưng **cả hai ID của từng cặp đều được giữ**: dict không âm thầm nuốt mutant cùng nguồn. Thêm mã ngoài chín hàm không đổi dãy ID. Kết quả ở `audit8-results.json`.

Census đủ **49 kiểu AST, 1531 nút** trong chín hàm và hàm lồng của chúng; việc “duyệt mọi nút” không đồng nghĩa có toán tử cho mọi kiểu. Bảng dưới liệt kê cả kiểu có toán tử, kiểu chỉ được tác động qua nút cha/con và kiểu chưa đo toán tử riêng. Không coi một ô “không có toán tử” tự nó là P2 khi chưa có survivor phân biệt được.

{{AST_TABLE}}

`operators8-results.json`: **60** phép thử toán tử bổ sung, **57 GIET**, **3 SONG**; mỗi SONG chạy đủ52 ca. Chúng được kiểm tiếp là tương đương, không bị thổi thành lỗi. Phép bỏ ngoại lệ được đo riêng là phép thứ61 và là survivor phân biệt được F10/P2.

Disposition P3 cho ba survivor ngoài tập: đề xuất **giữ sản phẩm, không ép giết**, owner đề xuất `ducthangho`: `tach_buoc[:1:2]` luôn bằng `[:1]`; `RE_LOI_GOI.fullmatch→match` tương đương trên dòng logic không chứa LF, với regex đã có `^…$`; lần `rstrip→lstrip` thứ hai chỉ thay các đoạn LF rỗng bị `dong_logic`/`if d` loại, còn phép so khối trước đó không đổi. Đây là quyết định không vá có căn cứ, không là biểu hiện P0–P2 mới. Không lấy mẫu hữu hạn làm chứng minh tổng quát; lập luận dựa trên cấu trúc nêu trên, các phép đo là đối chứng bổ sung.

`criteria8-results.json` kiểm rc0, rc4/lỗi vô can, rc3 sai tên và rc3 đúng tên. Sai tên không được GIET. Runner tập đóng kiểm `d.startswith('DO:'+c+':')`; `--tat-ca-ca` được tiêm kết quả rc4 rồi rc3, xác nhận **không dừng ở rc4, dừng ngay ở rc3 đầu**, không gọi ca sau. `chay_ca` phân biệt lớp TinHieuChotCa, không đổi AssertionError/AttributeError vô can thành tín hiệu chốt. Parser của catalogue dùng membership chuỗi thay prefix; trong đường `--mot-ca` tên do chính `chay_ca` gắn, không tìm được credit giả thực tế ở tập đã chạy. Không suy điều này thành bảo đảm với producer output tùy ý.

## Tám chứng minh TUONG_DUONG

Giữ cả8; không tìm được đầu vào phân biệt. Cả8 đã chạy đủ52 ca của HEAD trên từng mutant và có các đối chứng riêng ở `equivalence8-results.json`.

| mã | quyết định | lập luận / đối chứng |
|---|---|---|
| `ghep_job#24:-1` | giữ | Chỉ lấy phần tử khi danh sách có đúng1 phần tử; [0]=[-1]. 25 cặp tên/job, gồm0/1/nhiều ứng viên, alias và Unicode. |
| `chan_buoc#103:bo_doi_so1` | giữ | Chỉ khác khi thiếu run: `str(None)` và chuỗi rỗng đều không chứa GITHUB_ENV/PATH; 7 dạng bước trước gồm thiếu/null/0/chuỗi/uses. |
| `tach_buoc#173:chuoi2` | giữ | Đổi hoa/thường hằng trong len() giữ nguyên13 ký tự; 5 cấu trúc log. |
| `tach_buoc#173:chuoi3` | giữ | Cùng chứng minh độ dài; 5 cấu trúc log. |
| `tach_buoc#173:chuoi4` | giữ | Cùng chứng minh độ dài; 5 cấu trúc log. |
| `do_dau_duong#127:bo_ve0` | giữ | goi rỗng: all([]) True nhưng comprehension vẫn rỗng, không có vòng lặp marker. 351 cặp, gồm0 lời gọi, blank, slash và nhiều dòng. |
| `do_dau_duong#306:chuoi1` | giữ | Không rstrip LF chỉ thêm đoạn rỗng cuối; nối slash/strip và lọc if d cho cùng dòng logic. Phép so khối trước đó không đổi. 351 cặp. |
| `do_dau_duong#306:chuoi4` | giữ | Cùng nguồn mutant với mục trên; vẫn giữ ID riêng, cùng chứng minh và351 cặp. |

## Tập đóng đã đo

**221/1009 mã được đo độc lập trên HEAD: 213 GIET, 8 tương đương SONG, 0 SONG ngoài danh sách, 0 TIN_DUNG_GIA, 0 chứng minh tương đương bị bác.** Mọi tiến trình con trong receipts này rc0; mỗi GIET giữ tên ca và `DO:<ca>:` thật. Các8 SONG chạy52/52, không suy SONG chỉ từ một target xanh. **788 mã còn lại KHÔNG ĐO ĐƯỢC trong lượt này**, không tuyên bố tái lập toàn bộ1001 kill của executor.

Đã lấy mẫu150 mã với seed899008, chia đều luân phiên chín hàm, tách khỏi frontier ban đầu; đo hết frontier và giữ thêm14 phép đo của chính lượt hiện tại. Không dùng cache/rank executor. Các receipt được dùng lại là phép đo của **chính session này, cùng HEAD và cùng hash nguồn**, không phải log lượt trước. `closed8-selection.json`, `closed8-results.json`, từng `closed8/*.json` giữ selection, source hash, command, rc, ca và output.

| hàm | số mã độc lập |
|---|---:|
| _env_chan | 32 |
| doc_wf | 14 |
| ghep_job | 20 |
| ten_du_kien | 20 |
| _gio | 17 |
| ghep_buoc | 42 |
| chan_buoc | 18 |
| tach_buoc | 23 |
| do_dau_duong | 35 |

**Sai khác con số frontier trong lời dẫn:** parse toàn bộ `.review-input/dot-bien-dong-luot-dau.txt` bằng regex record `[KQ]`, không theo dòng, cho1009 ID duy nhất: **952 GIET +30 SONG +27 TIN_DUNG_GIA =57 mã chưa giết**, không phải58. Có một dòng nối hai record GIET; parser theo dòng sẽ làm sai đếm. Đã đo **đủ57/57 ID thực có**, nay49 GIET +8 tương đương. Một “mã thứ58” không có trong hiện vật được giao là **KHÔNG ĐO ĐƯỢC**, không bịa thêm ID. Log cuối executor có1009 ID và1001 GIET+8 SONG đúng như lời khai; kiểm cấu trúc log không thay kiểm chạy độc lập.

Lượt `python -B ops/ci_provenance_test.py --dot-bien-dong 8` và một lần driver full được ngắt rc130 để đổi sang mẫu/đổi thứ tự ca theo quyền trong prompt; không coi lượt dở dang là pass. Lượt cuối `python -B .review/run8.py closed-sample python -B .review/closed8.py` rc0, `CLOSED8 221 bad 0`. Driver chỉ đổi thứ tự và dừng sau kill đúng ca, như runner gốc; giữ ngoại lệ trước kill trong raw JSON, không dùng nó làm credit.

## Lỗi sản phẩm và phạm vi tìm

**Không tìm được lỗi sản phẩm HEAD** trong các phép đo này. `product8-results.json` có300 kịch bản M4/M12 seed899008 tự dựng REST độc lập với tên/số/giờ do sản phẩm suy:106 ghép passed,194 not_measured;160 marker gồm7 passed,5 failed,148 not_measured. Đã thử alias Unicode/ký tự regex/khoảng trắng, matrix, steps hỗn hợp run/uses/skipped, số thứ tự có gap và đảo thứ tự REST, tên lệch, giờ ngoài cửa sổ, metadata sai number, count lệch, job không khớp, env/defaults ba mức, shell và nguồn GITHUB_PATH trước bước.

Đối chứng bổ sung:169 ca assertion lịch sử lượt3–7, hai script lượt1/2 mỗi script34 quan trắc (không ném),32 mutant P1 lượt7 tái dựng trên HEAD và bị c51 giết đúng ca, cùng52 ca repository. `history8-results.json`, `prior-f10-8-results.json` ghi scope cụ thể. Không coi một script chỉ in quan trắc là assertion suite. Bộ oracle mới ban đầu có5 lệch do kỳ vọng nhầm `dong_khop` khi marker failed; đã giữ raw tại `product8-initial-oracle-errors.json`, sửa oracle theo contract hiện hữu rồi đo lại300/300, không báo5 lệch ấy thành lỗi sản phẩm.

## ĐỐI CHIẾU F01–F11 (nguồn lượt7, SHA9b329bf…)

| lớp | kết quả | bằng chứng / giới hạn |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | GIỮ ĐÓNG trong phạm vi đo | c22, metadata thiếu/kiểu; không suy ghép passed thành Gate passed. |
| F02 `nhac-ten-script-thanh-thuc-thi` | GIỮ ĐÓNG các phản chứng đã giao | c23/c25–27/c35/c40–43, composite/nested/lệch bước trong lịch sử1/2; giữ giới hạn gốc tin của spec. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | GIỮ ĐÓNG | c20: thiếu/lặp/total đổi, jobs/artifacts; REST fake giữ state. |
| F04 `rest-gia-khong-neo-run` | GIỮ ĐÓNG | c20 URL khác run/attempt/log bị từ chối, catalogue tương ứng. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | GIỮ ĐÓNG | c01/c18/c19/c22 và receipts A7 dương/âm; giữ lỗi I/O/REST tách biệt. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | GIỮ ĐÓNG | c24 mock redirect/network và header; không đo endpoint thật. |
| F07 `a10-doi-sha-khi-checkout-skipped` | GIỮ ĐÓNG theo authority | Replay13+1/22+1; không lấy REST head bù SHA chuan-bi. |
| F08 `nguon-workflow-git-khong-duoc-kiem-thu` | GIỮ ĐÓNG | c34 Git/blob thật trong scratch, thiếu path/nonUTF8; c32 thiếu workflow. |
| F09 `thoi-diem-khong-hop-le-van-ghep` | GIỮ ĐÓNG trong phạm vi đo | c38/c51, lịch/giờ sai, Unicode/fraction/offset, quan trắc1/2, đối chứng alias/step đúng. |
| F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` | **32 biểu hiện P1 lượt7 ĐÃ VÁ THẬT; cả lớp CHƯA VÁ HẾT** | baseline c51 rc0, từng32 mutant rc3 đúng c51;221 mã tập đóng không có survivor bất hợp lệ; lỗ ExceptHandler/Tuple mới P2 sống52/52 và đổi A18. |
| F11 `chan-path-chua-co-phan-chung` | GIỮ ĐÓNG | c42, source trước/khác job/sau, PATH riêng, lịch sử và oracle mới. |
| D01 | GIỮ ĐÓNG theo quyết định | c46/c49/c51 phân biệt env null với vắng ở workflow/job. |
| D02 | GIỮ NỢ P3 theo quyết định, không mở lại | uses nhiều dòng giữ dòng đầu; disposition của chủ kho được áp nguyên. |

Theo lớp P0–P2, U lượt7={F10}, F=∅: **0/1 lớp cũ đóng toàn bộ**; không lấy32 biểu hiện được vá làm32 lớp đã đóng. Nếu tính cả P3 D02, U={F10,D02}, F vẫn rỗng: giữ nợ theo authority không phải vá mã. Việc đổi thước ở checkpoint đã được user giao; kết quả này không tự cấp thêm vòng hay quyền thi công.

## A1–A27

| tiêu chí | kết quả / phạm vi |
|---|---|
| A1 | passed c01: help đủ cờ, sai đối số rc2 và dòng đếm. |
| A2 | passed c02: attempt lệch failed/rc12 và đối chứng. |
| A3 | passed c03–09: Linux/Windows fixture, thiếu/nhiều/lệch SHA, PR parents; không là Windows/PR LIVE execution. |
| A4 | passed c10–15 và probes M4/M12; runner0/skipped, regex đúng bước, import MOI. |
| A5 | passed c16: Workflow definition luôn not_measured, path chỉ là lời khai. |
| A6 | passed c17: fault injection giữ đích cũ/không hiện vật nửa vời. |
| A7 | passed c18/c19; criteria8-results.json có baseline rc0 và mutant rc3 đúng ca cho bỏ dòng đếm/gộp REST vào12; không dùng tổng suite thay receipt riêng. |
| A8 | {{SUITE_STATUS}} Độ phủ bộ sinh vẫn chưa đủ vì F10/P2. |
| A9 | **failed, giới hạn đã khai g4**: registry25/24, `test sống chưa đăng ký`; Ruff contract3/3. Full `--chay` not_run. Không sửa registry ngoài write set, không gọi nó passed. |
| A10 | Replay offline passed, byte-identical cả hai; REST/LIVE/freshness KHÔNG ĐO ĐƯỢC. |
| A11 | passed local: đúng2 tệp/2026 dòng, diff-check0, Ruff2 tệp0, doctrine10/0, ADR53/53; trần theo checkpoint. |
| A12 | not_run/not_measured: không đẩy, không ls-remote; bước này chỉ đo ở phiên có authority/phạm vi tương ứng. |
| A13 | partial/not_measured: CLI identity cùng thread/cwd/model/effort đã đọc; receipt launcher, stdout thread.started và hash rollout sau khi process kết thúc cần bên vận chuyển hoàn tất. |
| A14 | passed c25: env metadata mang màu không thành kịch bản. |
| A15 | passed c26: subset khối không thành xác thực. |
| A16 | passed c27/c52 và đối chứng: toàn khối, đúng nguyên văn, lời gọi tối giản. |
| A17 | passed c28–31/c46/c48–52, D01 và nguồn chặn; giữ giới hạn uses trước bước của spec. |
| A18 | Hành vi HEAD passed trong phạm vi đo; **test/generator còn F10/P2** ở nhánh RecursionError. Không chấp nhận tổng suite thay phép khóa nhánh ấy. |
| A19 | passed c33 và các job/alias độc lập trong lịch sử/oracle300; đọc chế độ đúng job. |
| A20 | passed c36; số nhóm/REST/YAML, không zip cắt ngắn. |
| A21 | passed c37/c48–52 và tên lệch trong oracle300. |
| A22 | passed c38/c51, lịch/format/header/window và dữ liệu thật A10. |
| A23 | passed c39/c47–52, key/name/prefix/duy nhất; không tuyên bố đánh giá biểu thức matrix. |
| A24 | passed c40/c35 và nested probes lịch sử; không ép giết biến đổi tương đương. |
| A25 | passed c41 và composite probes; composite thật trên runner KHÔNG ĐO ĐƯỢC. |
| A26 | passed c42/c47–51, ENV/PATH trước/khác job/sau/skipped; oracle độc lập có nguồn PATH trước bước. |
| A27 | passed c43, khối của bước khác không thành marker. |

## Replay A10 offline

`python -B .review/run8.py replay python -B .review/replay8.py` rc0; **37/37** log khớp SHA256SUMS, provenance tái sinh từ HEAD và Git objects cục bộ **khớp từng byte** bản đo trên52e9573. **0 khác biệt provenance cần giải thích**.

| run / attempt | Run | Checkout / ghép | Gate / marker | SHA-256 provenance |
|---|---|---|---|---|
|39342960764 /1|passed|13 checkout passed b27fe85… +1 chuan-bi not_measured; ghép13/14|14 Gate not_measured,0 failed;0 marker MOI|`5ad9afeafb5312101ae326d738855e8adb1e46e7e4240944c2b21e12ed2bafe0`|
|40074551995 /1|passed|22 checkout passed dc65714… +1 chuan-bi not_measured; ghép22/23|23 Gate not_measured,0 failed;8 marker nhanh_don_duoc not_measured/che_do_khong_xac_dinh; gate-nhanh-gop không marker|`24ffa770ff268876c030f12f59fee1010956138ba2ca3fa4370710456ffd185b`|

Labels đều ubuntu-latest; Workflow definition vẫn not_measured. Không đo freshness/retention REST, GraphQL, native Windows/pwsh, PR synthetic merge thật, composite thật hay action đổi môi trường. Không dùng replay thay LIVE hoặc CI provenance mới.

## Lệnh, trạng thái và bằng chứng dương

Các lệnh Python được chạy qua `python -B .review/run8.py <nhãn> <command...>`, đặt PYTHONDONTWRITEBYTECODE=1, TMPDIR/TMP/TEMP/cache vào `.review/`; wrapper giữ rc con thật, stdout/stderr, byte và SHA-256 trong `<nhãn>.json`. Không lấy rc0 của driver làm pass cho mọi mục con: xem rank/rows bên trong.

| phép đo | kết quả |
|---|---|
| `python -B ops/ci_provenance_test.py` | {{SUITE_STATUS}} `suite.json`, stdout/stderr. |
| `python -B .review/closed8.py` | rc0;221 mã,213 GIET+8 tương đương, `CLOSED8 221 bad 0`;788 còn lại KHÔNG ĐO ĐƯỢC. |
| AST audit /61 toán tử ngoài tập | audit rc0,1009 nguồn/0 compile lỗi/0 ID collision;60 probe57 kill+3 equivalent;1 gap sống có phản chứng A18. |
| `python -B .review/prior_f10_8.py` | rc0,32/32 P1 lượt7 bị c51 giết đúng ca; baseline xanh. |
| `python -B .review/history8.py` | rc0;169 assertion cases xanh,2×34 quan trắc không ném; không là mọi frontier lịch sử. |
| `python -B .review/product8.py` | rc0,300/300 khớp oracle đã sửa; log lỗi oracle ban đầu được giữ riêng. |
| `python -B -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py` | rc0, All checks passed. Bare lint scripts/tl.py not_run. |
| Ruff pin/probe contract |3/3 hợp đồng trong registry stdout; tách khỏi bare lint trên2 tệp. |
| `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc0,10 tệp/0 chỗ chép doctrine. |
| `python -B .claude/dev/packet_loop.py adr-song --root .` | rc0,53 ADR/53 dòng, exemption0016 giữ nguyên. |
| `python -B .claude/dev/ci_dang_ky_test.py` | rc1, registry25/24, TỔNG: ĐỎ do mục MOI được rút theo g4; không bỏ qua kết quả. |
| Full release/selftest toàn kho, CI mới, connector, remote/LIVE, merge/deploy | **not_run**, ngoài lượt offline; không tự miễn gate/land. |

Không có required job skipped nào được đọc thành passed. Các phép không đo được được ghi đúng phạm vi; các lượt bị ngắt giữ rc130, không tự void hay hoàn ngân sách.

## Read-only và bàn giao

{{SNAPSHOT_STATUS}}

Các hiện vật bền trong `.review/`. Một probe end-to-end ban đầu dùng tempfile mặc định ngoài checkout trong `/tmp` và context manager đã dọn; đã chạy lại cùng phép đo bằng wrapper với temp trong `.review/` (`gap-e2e.json`). Không khai rằng chưa từng tạo tệp tạm ngoài `.review/` trong cả lịch sử session. Không sửa branch Executor, push, đăng GitHub, gọi agent, merge, land hay LIVE. Verdict/evidence không tự thay receipt vận chuyển hay required check.

Kết quả cần bàn giao là **changes_requested vì F10/P2**, kèm disposition P3 đã nêu và phạm vi chưa đo. Chủ kho/điều phối quyết định phần còn lại trong budget10 đã cấp; reviewer không tự mở vòng thi công hoặc mở rộng Packet.
