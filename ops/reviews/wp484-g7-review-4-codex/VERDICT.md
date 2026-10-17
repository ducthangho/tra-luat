Reviewed commit: 0f31bb3e6151dd0cc67e8d4664b139259383b8d5
Spec SHA-256: 4a512dd38721c3c4eec7978489ba06485feab32f94a0c5637a085d6c694ba38c
verdict: approve
P0=0 P1=0 P2=1 P3=0

**Chưa hết P2. H01 đóng một phần; còn biểu hiện J01 qua môi trường startup Bash, cùng một lớp G02/H01.** `approve` theo ngưỡng riêng của chỉ thị lượt 4: không P0/P1 và P2 còn mở được nêu rõ để **chủ kho Issue #484 quyết**. Đây không phải quyết định chấp nhận nợ thay chủ kho hoặc xác nhận đủ điều kiện merge. Attempt 4/4 đã hết; không đề nghị tự động vá hay gọi thêm reviewer.

HEAD/tree tự đo khớp: `0f31bb3e6151dd0cc67e8d4664b139259383b8d5` / `f6074ae53c0f4032eb17b56e01d432c5990c0065`; checkout detached. VERDICT3 băm `9b0fef233238fec7007cc80a6eb5f5ac8bb4c58310da2ced1e50c83b29d0bfc4`, SPEC8 như dòng 2. Delta so `cfd3550b6336eecb6847543a5f33200b57dd81ba` đúng hai tệp +24/−2; mã sản phẩm không đổi.

Reviewer: Codex/OpenAI, độc lập với context executor Claude. Header của chính run `fbfda8b5` ghi Codex CLI `0.163.0`, model `gpt-6.1-sol`, effort `xhigh`, session `01a14a9a-2b92-70c2-80ed-9c0be845ddd0`: [header](logs/runtime-header.log). Khai `provider=openai_codex`, `execution_surface=codex_cli`, `transport=machine`; header không chứng minh model của mọi request hoặc tự tạo receipt `cross_approved`. Linux, Python `3.13.16`, Git `2.43.0`, Ruff `0.16.8`; sandbox `workspace-write`, approval `never`.

## H01 và bảng lớp

| Finding / slug | Trạng thái | Phép đo độc lập |
|---|---|---|
| G02 → H01 → J01 / `hook-scrub-test-unisolated-bootstrap` | **Đóng một phần, còn P2** | Không có startup ngoài fixture: positive có seam 3/3, không gọi installer. `rg` hỏng bị assertion mới bắt; cargo cũng bị bắt khi rg vắng. Tuy nhiên `BASH_ENV` thêm PATH ngoài fixture: ca vẫn 3/3, gọi 18 lần installer spy ngoài `fakebin`; gỡ riêng `BASH_ENV` thì 3/3 và 0 lời gọi ngoài fixture. |
| F01 / `codex-rejected-state-khong-ghi-duoc` | Nợ đã có quyết định SPEC8 | Không tính finding mở; không mở lại acceptance đã được chủ kho hạ. |
| CAS / `codex-auth-json-khong-cas` | Nợ đã có quyết định kế thừa | Không tính finding mở; không tuyên bố thành CAS hoặc đo lại các race kernel trong lượt chỉ H01. |

Một lớp, một biểu hiện còn mở J01; không cộng lại G02 hoặc H01 thành P2 thứ hai. Các finding khác của lượt 3 không được nhận là đã đo lại toàn bộ trong review này.

## J01 — P2 — BASH_ENV có thể đưa installer ra ngoài fakebin mà ca vẫn xanh

**Vị trí:** `.claude/dev/launcher_test.py:7538–7544` lọc PATH rồi sao chép toàn bộ `os.environ`; dòng 7551 chạy Bash với env ấy. Không gỡ `BASH_ENV`. Bash nạp startup trước thân `.claude/hooks/session-start.sh`; startup có thể thêm thư mục vào đầu PATH sau khi fixture đã đặt `fakebin` ở đầu. `command -v` ở hook dòng 97 khi ấy trả executable ngoài fixture; các lời gọi tên trần `apt-get`/`sudo` ở dòng 186–190 đi theo PATH mới. Assertion dòng 7556 chỉ thấy nhật ký do các stub trong fixture ghi.

**Đã đo:** [review_env_path.py](review_env_path.py) chạy nguyên ca trên bản sao tạm. Tệp startup chỉ thêm thư mục `ambient-tools` do reviewer tạo vào PATH; `rg` trong đó trả 97, `apt-get`/`sudo`/`cargo` chỉ ghi nhật ký riêng và trả 97. Không installer thật, không credential thật, không tải mạng. Không sửa hook hay assertion của ca trong phản chứng `env-escape`.

| Đối chứng | Rc tiến trình ca | Kết quả chính ca | Hook rc | Installer ngoài fixture | Nhật ký installer của fixture |
|---|---:|---|---|---:|---|
| `env-control`: không BASH_ENV | 0 | 3/3 qua | 0,0,0 | 0 | Rỗng |
| `env-escape`: thêm BASH_ENV | 0 | **3/3 qua** | 0,0,0 | **18** | **Rỗng** |
| `env-scrub-control`: chỉ gỡ BASH_ENV trong env hook của bản sao | 0 | 3/3 qua | 0,0,0 | 0 | Rỗng |

Mỗi lượt escape gọi sáu lần ngoài `fakebin`: `apt-get install`, `sudo apt-get install`, `apt-get update`, `sudo apt-get update`, `apt-get install`, `sudo apt-get install`. Cả ba lượt giữ nguyên kiểm materialize đúng một lần, child sạch, child sau materialize, auth đúng và không in snapshot. [Dữ liệu](logs/ambient-path.json), [nhật ký ca xanh](logs/env-escape.log), [nhật ký hook](logs/env-escape-hook.json). Cùng hướng trên head lượt 3 cũng xanh 1/1 và gọi sáu lần installer spy ngoài fixture: [đối chiếu nền](logs/env-base-summary.json). Đây là lối còn sót của H01, không phải hồi quy runtime do delta lượt 4.

BASH_ENV ở đây mô phỏng cấu hình shell thêm PATH, không cần công cụ giả ghi đè tệp trong fixture hay đọc snapshot. Phép đo chứng minh **đã gọi executable ngoài fixture mà ca không phát hiện**. Nó không tuyên bố installer thật đã cài được, đã kết nối mạng hoặc sửa máy; impact thực tế còn tùy startup/PATH và quyền máy chạy.

**Gợi ý để chủ kho quyết:** sửa fixture tại khối dựng env và biên giải/chạy Bash, dùng env được kiểm soát, loại startup/function injection của shell; đặt HOME/CODEX_HOME/TMPDIR tạm. Giữ PATH cần thiết cho coreutils, không loại cả `/usr/bin` vì chứa installer. Ca khóa phải nạp startup inert có thay PATH và kiểm nguồn executable/nhật ký ngoài fixture; sau vá phải 0 lời gọi installer ngoài fixture, đồng thời ba đối chứng mutation bên dưới vẫn phân biệt đúng. Đối chứng gỡ BASH_ENV mới chứng minh đóng lối cụ thể này, chưa chứng minh đã đóng toàn lớp môi trường. Rủi ro vá: loại biến nền cần thiết, làm mất interpreter/coreutils hoặc khiến ca không còn chạy tới materializer. Không giao patch runtime và không sửa KHO.

## Những đường gọi từ chính hook tại head

| Đường trong hook | Fixture che được gì / còn phụ thuộc gì |
|---|---|
| `co`/`co_chay`, dòng 74,95–104: `command -v` rồi Python chạy executable `--version` | `python3`, `codex`, `claude`, `rg` có stub. PATH không bị đổi bởi startup thì hit đầu thuộc `fakebin`; J01 chứng minh tiền đề ấy không luôn đúng. Không thấy đường installer tuyệt đối bỏ qua PATH trong hook này. |
| npm install hai agent, dòng 150–160 | npm stub ghi `NPM`; codex/claude stub chạy được nên nhánh cài không vào ở positive. Assertion bắt NPM. |
| apt-get, sudo apt-get, cargo install ripgrep, dòng 183–200 | Cả ba tên có stub ghi CAI, trả 97. Khi rg chỉ hỏng version thì `co rg` vẫn đúng nên chưa tới cargo; mutant rg vắng đo thêm cargo và bị bắt. Startup đổi PATH vẫn có thể vượt các stub: J01. |
| actionlint, dòng 204–218 | **Chưa giả actionlint**: probe có thể gọi executable máy chạy ngoài fakebin. Spy độc lập nhận đúng `--version`, ca vẫn 1/1: [kết quả](logs/actionlint-summary.json). Nếu thiếu/hỏng, hook tạo `$HOME/.local/bin` rồi gọi `bash "$GOC/ops/cai_actionlint.sh"`. Fixture không chép `ops/`, nên script vắng; positive quan sát cảnh báo cài thất bại, không chứng minh có tải actionlint. HOME vốn được kế thừa; runner reviewer đặt HOME tạm. Không đếm riêng một P2 chỉ vì version probe/coreutils. |
| requirements, dòng 245–503: git rev-parse, kiểm import, `$PY -m pip install` | Fixture không tạo `requirements.txt`, nên khối này không vào. `$PY` là shim; assertion mới có `SACH -m pip`. Nếu nhánh cài được vào, shim có thể exec Python thật trước khi assertion chạy; không nhận assertion là cơ chế chặn installer trước thực thi. Trong fixture hiện tại, không có đường vào khối qua tệp requirements đã được tạo sẵn. |
| policy/status/doctor, dòng 571–640 | `.claude/dev/codex_env_policy.py` không được chép, Python shim chạy tệp vắng rồi hook đặt cờ chặn codex. `launcher.py credential-status`/`doctor` được shim trả 0; riêng `chuan-bi` exec Python thật. Không có doctor/probe mạng thật sau materializer trong ca có seam. |
| dirname/mkdir/date/head/sed/rm/env/bash, đường script và shebang | Các tiện ích hệ thống còn phụ thuộc máy chạy theo thiết kế; không phải installer mới. Có `#!/bin/bash`, `#!/bin/sh` trong các shim và đường Python thật tuyệt đối được fixture chèn. Không thấy apt-get/npm/cargo/winget/choco/brew/curl/wget bằng đường tuyệt đối trong hook. `$GOC` và CODEX_HOME đã ghim vào sân tạm; interpreter vẫn dùng biến khởi tạo môi trường kế thừa. |
| Biến môi trường | BASH_ENV đã đo như J01. Exported shell functions, ENV, PYTHONPATH/PYTHONHOME và startup Python có thể ảnh hưởng phân giải/khởi tạo; chưa đo từng lối, không cộng finding suy đoán. Cấu hình proxy/npm/pip không tạo nhánh mạng riêng khi installer/requirements không được chạy. AL_VER/AL_DICH được hook gán; startup kế thừa vẫn là biên chưa được làm sạch. |

## Ca còn răng: đột biến trên bản sao

`python -B review_mutants.py` tự dựng mỗi mutant trong cây/tiến trình riêng; không chạy script executor để nhận bằng chứng. [Script](review_mutants.py), [rc và assertion](logs/mutants.json).

| Thử | Rc ca | Hook rc | Kết quả đúng kỳ vọng |
|---|---:|---:|---|
| Positive, shim/case/hook giữ nguyên, seam materializer | 0 | 0 cả 3 | 3/3 qua; không installer |
| (a) rg giả trả 1 | **1** | 0 | **ĐỎ đúng assertion `fixture gọi installer`**; sáu dòng CAI apt-get/sudo |
| (b) như (a), chỉ gỡ `CAI ` khỏi tuple assertion | **0** | 0 | **XANH 1/1**, vẫn sáu lời gọi installer giả; chứng minh đúng assertion mới là răng |
| (c) mutant tay lượt 3 trên ca này: bỏ `unset CODEX_AUTH_JSON` trong hook | **1** | 96 | **ĐỎ bằng assertion của chính ca** `materializer phải chạy đúng 1 lần`; nhật ký có `BAN -c`, hook dừng trước prepare. Không phải SyntaxError/ImportError/storage/setup kill. |
| Bổ sung: không tạo rg giả, PATH reviewer không có rg | **1** | 0 | **ĐỎ `fixture gọi installer`**, bảy dòng CAI, gồm `CAI cargo install ripgrep` |

Chỉ có một mutant tay lượt 3 gắn chính ca H01: bỏ unset. Hai mutant tay lượt 3 cho G01/F04 thuộc các ca khác, không được nhận là đã chạy lại ở đây. Bảng trên là ba mutation bắt buộc (hai đỏ, một xanh đối chứng) và một mutant bổ sung, không phải chạy toàn bộ bảng mutation launcher.

## Bảng hướng thử

| Hướng | Lệnh / hiện vật | Output đo được | Kết luận |
|---|---|---|---|
| Installer rg, răng assertion | `python -B review_mutants.py` | a rc1 đúng `fixture gọi installer`; b rc0; c rc1 assertion ca | Bản vá bắt được đường PATH thông thường và giữ răng scrub |
| Cargo fallback khi rg thật sự vắng | [ca/log](logs/rg-absent.log), [hook](logs/rg-absent-hook.json) | rc1, CAI cargo cùng sáu CAI apt/sudo | Cargo stub và assertion có tác dụng |
| Môi trường startup đổi nguồn executable | `python -B review_env_path.py` | 3/3 xanh dù 18 lời gọi ngoài fixture; đối chứng 0 | **J01/P2**, H01 chưa đóng trọn |
| Startup có thật sự chạy không | `python -B review_ambient.py` | ca rc0,1/1; 11 marker startup inert | Env kế thừa có hiệu lực thực tế, không chỉ đọc mã |
| actionlint còn trỏ ra máy chạy | `python -B review_actionlint.py` | rc0,1/1; spy ngoài fakebin nhận `--version` | Phụ thuộc host còn tồn tại; chưa có bằng chứng cài actionlint thành công |
| Ca gốc/storage trong sandbox | `python -B run_clean.py python -B review_case.py review-copy --label raw --repeat 3` | rc1,0/3; hook13 cả ba | Không tái lập claim H01 nguyên bản3/3; dùng seam để đo răng riêng |
| Ca khác đổi màu sau delta | `python -B review_regression.py`, `python -B review_compare.py` | Xem bảng Đã đo | So cùng rig/head–base, không lấy lỗi storage làm finding mới |
| Lint/quota/inventory | `python -B review_static.py`, `python -B review_inventory.py` | F5→5; bash7→7, DAT;221→221, chỉ AST ca H01 đổi | Không thấy tăng nợ hoặc mất ca |

## Đã đo

- Ghi VERDICT.md sớm rồi cập nhật. Đọc chỉ thị snapshot, SPEC8, ba verdict trước, delta, hướng dẫn kho/adapter review, handoff và toàn hook liên quan. Phạm vi lượt này là H01; không dùng claim executor hoặc script `executor-do_h01.py` làm kết quả tự đo.
- Hai clone riêng `review-copy` và `base-copy`, dựng liên tiếp trong cùng bootstrap, checkout đúng hai SHA và ghim `core.abbrev=7`. Mọi mutant nằm ngoài KHO. Runner [run_clean.py](run_clean.py) dùng env cho phép, PATH gồm công cụ hệ thống được chọn và spy inert, HOME/USERPROFILE/CODEX_HOME/TMPDIR nằm trong thư mục ra. Hai suite fake dùng biến inert `CODEX_AUTH_JSON`; module test tự gỡ trước các ca.
- **Seam được khai rõ:** vì `/tmp/.git` chỉ đọc tồn tại, `_KhoCodex` từ chối home dưới `/tmp` với `OSError: Codex home is inside a repository`. Ca nguyên bản raw rc1,0/3, hook13; không tính là mutant kill hay regression sản phẩm. [raw](logs/raw.log), [hook raw](logs/raw-hook.json). Các phép đo răng/J01 thay **riêng launcher materializer được chép vào project tạm** bằng writer inert ghi snapshot giả vào CODEX_HOME. Giữ nguyên thân ca/assertion, Python shim và hook, trừ đúng mutation đang thử. [Runner/seam](review_case.py), [positive3/3](logs/positive.log). Seam không phải integration/storage pass.
- **So hồi quy toàn danh sách ca, không seam materializer:** bốn lượt head/base, có/không snapshot giả được [review_regression.py](review_regression.py) chạy tuần tự. Để tuân thủ cấm installer thật, runner chủ động cho `_r345_venv` trả None, đưa tám ca phụ thuộc vào nhánh KHÔNG ĐO ĐƯỢC sẵn có. Không chạy venv/pip thật và không sửa tệp suite. Do đó đây là phép so với tám ca chưa đo, không phải tái lập full219/219.

| Cây / snapshot ngoài | Rc | Passed | Failed | Skipped | Tổng đăng ký |
|---|---:|---:|---:|---:|---:|
| cfd3550 / không | 1 | 198 | 13 | 10 | 221 |
| 0f31bb3 / không | 1 | 198 | 13 | 10 | 221 |
| cfd3550 / inert | 1 | 198 | 13 | 10 | 221 |
| 0f31bb3 / inert | 1 | 198 | 13 | 10 | 221 |

- `python -B review_compare.py` **rc0**: so tên từng ca cho **0 ca đổi trạng thái** head/base trong cả hai môi trường và 0 ca đổi giữa có/không snapshot trên head. Cả bốn lượt cùng 13 tên đỏ,10 tên skip; không làm tròn thành claim executor219/219. Mười ba lỗi gồm 11 ca storage/recovery, ca scrub dừng theo storage và t53 do PATH runner thiếu rg. Hai skip theo nền Windows; tám skip venv/pip do giới hạn có chủ ý ở trên. [Rc từng command](logs/regression-summary.json), [tên và trạng thái so sánh](logs/compare.json), [log head không snapshot](logs/review-copy-clean.log), [log head có snapshot](logs/review-copy-fake.log).
- Đối chứng riêng t53 sau khi chỉ bổ sung rg có sẵn của hệ thống vào PATH của tiến trình đối chứng: head/base đều **rc0,1/1**. Không chạy lại hoặc đổi kết quả bốn lượt suite trước đó. [t53 control](logs/t53-control.log).
- `python -B review_static.py`: runner rc0. Bare Ruff `/root/.local/bin/ruff check --no-cache --select F --output-format json` trên năm tệp Python của packet: head/base **đều rc1, năm F841 trong launcher_test, DELTA=0**, cùng vị trí/message; bốn tệp còn lại0. Không gọi bare Ruff là xanh. `bash -n` hook mỗi cây **rc0**. `python -B ops/bash_nen.py quet --root . --json` mỗi cây **rc0, DAT**, đọc `blob-index`, đếm launcher_test **7**, quota **7**, không lệch. AST mỗi cây221 ca, không trùng tên, chỉ thân ca H01 thay đổi. [Tổng static](logs/static.json), [inventory](logs/inventory.log).
- Probe storage độc lập chạy `_KhoCodex(home_tạm)` cho đúng `OSError: Codex home is inside a repository`; không sửa guard, xóa `/tmp/.git` hay dùng storage seam để nhận integration xanh.

## KHÔNG ĐO ĐƯỢC

- Launcher219/219 có/không snapshot và H01 nguyên bản3/3 trên storage thật trong sandbox này. Kết quả3/3 của reviewer là **có seam materializer**, không gán cho bản gốc.
- Tám ca cần venv/pip thật không được chạy vì chỉ thị cấm installer thật; hai ca Windows không đo trên Linux. Không suy chúng pass từ AST không đổi hoặc từ ca khác xanh.
- Native Windows, toàn bộ bảng mutation launcher, storage kernel/ACL/SID/reparse, bootstrap thật, credential/máy chủ thật: không đo. Không dùng giới hạn này để cộng finding sản phẩm suy đoán.
- CI Ubuntu trên exact head và comment chủ kho nâng trần: đã thử mở URL qua web, cả hai `Cache miss`; không có dữ liệu CI/authority trực tiếp được xác minh từ xa. [Log](logs/web-status.log). Dùng assignment hiện tại làm thẩm quyền cho lượt review này; không dùng credential thật để đọc GitHub.
- Các hướng cần đọc bí mật, proc/memory hoặc nội dung khai thác nhạy cảm chỉ mô tả bằng lời. Canary startup/PATH đã chạy chỉ dùng tệp và công cụ inert của reviewer, không đọc thông tin xác thực của phiên.
- Chưa có quyết định chủ kho chấp nhận J01/H01. CAS và F01 đã có quyết định không làm J01 tự đóng. Chưa xác nhận đủ M-2/M-3/M-4 để merge và không thao tác push/merge/land/GitHub.

## Toàn vẹn KHO

`python -B finish_audit.py` **rc0**: HEAD/tree đúng, checkout detached (symbolic-ref rc1 đúng kỳ vọng), status gồm ignored/untracked, diff HEAD/index và danh sách ngoài index đều rỗng; các command đọc còn lại rc0. **SHA-256 của 3.686 tệp tracked không đổi**, snapshot trước/sau bằng nhau; SPEC8 và VERDICT3 băm lại vẫn khớp. [Audit](logs/audit-summary.json), [snapshot trước](logs/checkout-before.json), [snapshot sau](logs/checkout-after.json).

Không sửa KHO/branch executor; hook marker, bản sao, cache/output và mutant nằm trong thư mục ra. Hai snapshot chứng minh không có delta quan sát được giữa hai mốc, không chứng minh mọi thao tác lịch sử chưa từng ghi rồi hoàn nguyên. Các thử đầu của reviewer có lỗi bố trí PATH (gom công cụ vào thư mục bị fixture lọc) và đọc nhầm cấu trúc JSON scanner đã được sửa trước các phép đo báo cáo; không tính chúng là mutant kill hay finding sản phẩm.
