verdict: changes_requested
reviewed_head: 8733f0ae7df5d9a1c704c31e6051e8cb5f439fe5
reviewed_sha: 8733f0ae7df5d9a1c704c31e6051e8cb5f439fe5
reviewed_tree: 78e884bd8c2d4debb95b97c719c49fc7d488c76f
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_run: 631922626b43489b85dbb7e84c86f509

## Kết luận

**F858-03 chưa đóng:** `/dev/null` không bảo đảm đứng riêng một dòng. Trình cài kết thúc stdout bằng một tiền tố đường dẫn **không có LF** thì `echo "/dev/null"` nối vào tiền tố ấy. Reader nhận một thư mục thật kết thúc bằng `/dev/null`, đưa nó lên đầu PATH, và `--bat-buoc` với thứ tự `rg,bash` lại trả **rc=2, rg=DO, bash=DAT** trên shell head nguyên vẹn. Đối chứng chỉ thêm LF vào stdout trình cài trả **rc=0, cả hai DAT**.

**F858-04 và F858-05 đóng trong phạm vi finding gốc.** Ca âm mới giết đúng mutant chỉ bỏ `return 1` của lỗi `cygpath -u`; diff có **6 tệp, 438 dòng thêm**, không bỏ ca/assertion/mutant cũ. **F858-01/02 không hồi quy trong các phép đã đóng.** Có thêm **F858-06, P2**, một lỗ coverage khác: mọi fixture đều đặt `GITHUB_PATH`, nên mutant chỉ chạy `cygpath -u` khi biến này có mặt vẫn sống qua các ca liên quan và toàn suite. Phép riêng không đặt biến phân biệt control **rc=0/DAT** với mutant **rc=1**. Đây là finding về test, không phải lỗi runtime đã thấy trên head nguyên vẹn.

Không thấy P0/P1 trong phạm vi đã đo. Còn hai finding P2 mở, chưa có quyết định chấp nhận chúng trong nguồn được cấp; chưa đủ điều kiện approve lớp sensitive. Verdict không cấp quyền merge/land/deploy.

## Neo phiên và phạm vi

HEAD/tree như trên; merge-base với `origin/master` là **637f78029f5a5fe56d35199dd0f75c50274f2c0f**. Spec đọc trực tiếp bằng `git show origin/ops/wp858-spec:ops/specs/wp858.md`, SHA-256 **5a61e959281f852592b2a5420b4618718d2364db8fa6320934d2651bbb7d4c54**, khớp prompt. Lease đọc offline từ **origin/ops/wp858-r1-g2-lease:ops/leases/wp858-r1-g2-claude.yaml**: generation 2, hết hạn 2026-10-24T04:32:00Z, `nang_tran: []`; chỉ thị chủ kho được ghi hộ yêu cầu thu về ≤450. Không dùng g1 làm authority hiện hành, không gọi GitHub để xác nhận heartbeat/CI bên ngoài bundle. [Preflight](evidence/preflight.log), [nền](evidence/merge-base.log), [spec](evidence/wp858-spec.log), [lease](evidence/wp858-lease.log).

Danh tính lấy từ [header CLI đúng run](evidence/model-header.txt) và [metadata đã chọn trường](evidence/run-identity.json). Header chứng minh model/effort CLI công bố, không chứng minh model thực thi từng request. Đây là phiên reviewer riêng qua shell/tools; không tái dùng context executor.

`kho/` được giữ nguyên. Mọi checkout chạy test, fixture và mutant nằm dưới `out/`. Sandbox thực tế là **workspace-write**, không phải cơ chế mount toàn bộ `kho/` read-only; snapshot đầu/cuối đối chiếu nội dung và trạng thái để kiểm delta quan sát được. Linux x86_64, Python **3.13.16**, PyYAML **6.0.3**; không cài dependency/công cụ qua mạng. [Runtime](evidence/runtime.log).

## Đối chiếu lượt trước

Nguồn: `../VERDICT-luot2.md`, reviewed SHA **97544b576392540ce316b2d61e5cc0de3a4a88eb**. Mỗi kết quả bên dưới do reviewer tự chạy trên bản sao của head hiện tại, không nhận số đo executor làm pass.

Giới hạn provenance đã kiểm: hai đường `ops/reviews/wp858-g1-luot{1,2}-codex-verdict.md` **không có trên ref g2 được cấp** (`git show` mỗi đường **rc=128**); ref g1 không có trong bundle. Vì vậy không xác nhận lời khai “hai verdict đã commit trên nhánh ấy”. Đối chiếu nội dung dựa vào bản lượt 2 local do người dùng cấp, SHA-256 **af2b6196b5ab589408dcc546136f224429e53d7346b6476493fd4dad2a840b01**; kết quả tái đo không phụ thuộc việc bản này đã được đăng hay commit. [Phép kiểm refs/đường dẫn](evidence/previous-verdicts.json).

| Finding lượt 2 | ĐÓNG / CHƯA ĐÓNG | Lệnh và kết quả thật trên head mới |
|---|---|---|
| **F858-01** — nuốt lỗi ghi PATH trong command substitution | **ĐÓNG — ĐÃ VÁ THẬT; không hồi quy** | `python out/edges.py`: git Linux/macOS/Windows mô phỏng đều **rc=0/DAT**, ghi đúng ứng viên (Windows có `W:`); `$GITHUB_PATH` là thư mục đều **rc=1**; `cygpath -w` lỗi **rc=1**, PATH file rỗng. `python out/mutations.py`: mutant bỏ trả lỗi ghi và bỏ trả lỗi `-w` đều chết bởi **TinHieuChotCa của ca hành vi**, ngoài shape. [Edges](evidence/edges-summary.json), [mutant](evidence/independent-mutations.json). |
| **F858-02** — fixture Windows không phân biệt chuyển đổi/bộ lọc cũ | **ĐÓNG trong phạm vi finding gốc — ĐÃ VÁ THẬT; không hồi quy** | `python out/mutations.py`: control Windows PASS; bỏ toàn bộ `cygpath -u` chết bởi **TinHieuChotCa** của ca Windows và shape. Ánh xạ `V:` còn phân biệt được phép đổi; không tái xuất hiện nhánh lọc `-f/-x/.exe` trong hàm. Không coi đây là nghiệm thu native Windows hay chứng minh coverage Windows đầy đủ: xem F858-06. |
| **F858-03** — stdout installer bị nhận làm kết quả chọn | **CHƯA ĐÓNG lớp — VÁ HỜ ở cấp lớp; biểu hiện collision cũ đã sửa** | `python out/edges.py`: N4 stdout thư mục LF/CRLF và thư mục thật trùng sentinel cũ đều **rc=0/DAT**, cả hai thứ tự. `python out/no_newline.py final`: stdout của riêng installer bash không có LF + thư mục `<tiền tố>/dev/null` thật ⇒ **rc=2, rg=DO,bash=DAT**. Cùng cấu trúc fixture nhưng stdout thêm LF ⇒ **rc=0**, cả hai DAT. [Phản chứng có trace](evidence/final-no-newline.json). |
| **F858-04** — chốt lỗi `-u` thiếu ca âm giết mutant | **ĐÓNG — ĐÃ VÁ THẬT** | `python out/edges.py`: stub `-u` in đường đúng rồi thoát 37 ⇒ head **rc=1**, không ghi PATH. `python out/mutations.py`: mutant chỉ bỏ `return 1` ⇒ ca Windows ném **TinHieuChotCa**, thông báo installer đã rc=0 khi `CYGPATH_U_HONG=1`; shape cũng chết vì thiếu nguyên dòng. Chốt hành vi không phụ thuộc riêng kiểm chuỗi. |
| **F858-05** — vượt trần diff sensitive | **ĐÓNG — ĐÃ VÁ THẬT** | `git -C kho diff --numstat 637f78029f5a5fe56d35199dd0f75c50274f2c0f HEAD` ⇒ **6 tệp, 438 thêm, 30 xoá**. `python out/compression.py` và đọc diff `97544b5..HEAD` ⇒ không xoá ca/assertion/mutant cũ; hai mutant mới được thêm. [Numstat](evidence/scope.log), [AST](evidence/compression-audit.json), [diff nguyên văn](evidence/since-round2.log). |

F858-02 được đóng theo đúng các nhánh/đột biến của finding gốc; F858-06 là bối cảnh độc lập chưa được kiểm (biến ghi PATH không tồn tại). F858-04 kiểm **hành động trả lỗi sau khi đã gọi `-u`**; F858-06 kiểm **việc vẫn gọi/chuyển đổi khi không cần ghi PATH**. Hai phép kiểm và hướng bổ sung khác nhau, không đổi tên để xoá lịch sử finding cũ.

## Finding mới và biểu hiện tái mở

| ID | Mức | Tệp:dòng tại reviewed head | Lệnh → kết quả thật | Đề xuất |
|---|---|---|---|---|
| **F858-03 (tái mở)** | **P2** | `ops/cai_cong_cu.sh:44`, tương tác reader `:120`–`:123`; fixture thiếu biến thể tại `.claude/dev/launcher_test.py:8511` | `PYTHONDONTWRITEBYTECODE=1 python out/no_newline.py final` → control LF **rc=0/DAT**; không LF **rc=2, rg=DO,bash=DAT**. Trace ghi `DICH=<sân>/pollution/dev/null` và `export PATH=<thư mục ấy>:…`. Biến thể installer in `/dev/null\r\n` rồi tiền tố thư mục không có LF cũng **rc=2/rg=DO**. [Log gọn](evidence/no-newline-run.log), [JSON/trace](evidence/final-no-newline.json). | Bảo đảm kết quả “giữ PATH” có ranh giới dòng độc lập với byte cuối stdout trình cài, và reader không thể coi kết quả đó là thư mục. Thêm ca N4 stdout không LF, có thư mục hậu tố `dev/null` và rg hỏng, cùng control chỉ thêm LF. Giữ sửa trong phạm vi Q1; nếu cần đổi reader thì xin điều chỉnh write set/authority theo quy trình. |
| **F858-06** | **P2** | `.claude/dev/launcher_test.py:8536`, ca Windows `:8600`; nhánh sản phẩm được bảo vệ `ops/cai_cong_cu.sh:48` | `python out/mutations.py` → mutant `u-only-when-github-path` **7/7 ca r858 liên quan PASS**. Cặp toàn suite có cùng origin/config/env: cả hai **221/234**, đúng tập **13 đỏ/10 bỏ qua**, không lỗi mới. `python out/no_gp_test.py` → không đặt GITHUB_PATH: head **rc=0/DAT, PASS**; mutant **rc=1, TinHieuChotCa** của probe reviewer. [Mutant](mutants/u-only-when-github-path.sh), [delta](evidence/matched-delta.json), [probe](evidence/no-gp-test.json). | Thêm chiều N2 **không có GITHUB_PATH** với `V:` chỉ đổi được bởi `cygpath -u`, bản tên trần hỏng và ứng viên tốt; đòi installer thật rc=0/DAT. Giữ chiều có biến để kiểm `-w`/ghi. Đăng ký mutant gắn nhầm `-u` với biến ghi và đòi ca hành vi giết bằng TinHieuChotCa. Head hiện tại không cần sửa runtime cho finding này. |

**Cơ chế F858-03.** Fixture chỉ dùng stub trình cài vô hại. Trình cài bash in một tiền tố dưới sân tạm bằng `printf`, không thêm LF; đầu ra kế tiếp của hàm là `/dev/null\n`. Vì command substitution gộp chung stdout, dòng cuối trở thành `<tiền tố>/dev/null`, không còn là `/dev/null`. Thư mục đó chứa `rg` fixture trả 1. `bash` tên trần đã DAT nên hàm không ghi `$GITHUB_PATH`, nhưng reader vẫn prefix thư mục vào PATH trong tiến trình hiện tại. Do đó GITHUB_PATH không ghi thêm **không chứng minh** nhánh giữ nguyên PATH đã an toàn. Chỉ stdout của installer **bash** được thay; output của installer/selector `rg` được giữ nguyên để cô lập lỗi wp858.

Thứ tự `rg,bash` đỏ; `bash,rg` vẫn xanh vì bước cài rg chạy sau có thể đưa ứng viên tốt lên trước. Không báo cả hai thứ tự đều đỏ. Đối chứng không có thư mục hậu tố cũng xanh. [Ma trận 12 biến thể N4](evidence/edges-summary.json).

**Windows, CRLF và `/dev/null`.** Trên Linux đã đo sentinel riêng dòng đi qua reader mà không đổi PATH, kể cả installer in CRLF. `DICH="${DICH%$'\r'}"` chỉ bỏ CR cuối; nó không tạo ranh giới LF trước sentinel, nên không chặn phép nối vừa đo. Installer in `/dev/null` trước rồi một tiền tố không LF cũng tái hiện được lỗi. Không cần biến chính `/dev/null` của hệ thống thành thư mục. Git Bash/MSYS native chưa được đo; không chấp nhận câu “KHÔNG BAO GIỜ là thư mục” như một chứng minh đa nền. Cần kiểm trên runner Windows thật việc nhìn thấy `/dev/null`, CRLF và stdout không LF; các giả thuyết về namespace/remap trên Windows chỉ là hướng kiểm, không được khai là lỗi đã tái hiện.

## Bảng lớp finding

| Slug lớp nguyên nhân | IDs/lịch sử | Trạng thái cuối lượt | Phép kiểm đóng lớp |
|---|---|---|---|
| `loi-ghi-path-bi-nuot-trong-command-substitution` | F858-01, lượt 1 `bfbd273` | Đóng phạm vi cũ | Installer thật trả khác 0 khi lỗi ghi/`-w`, mutant handler chết bằng ca hành vi. |
| `fixture-windows-khong-phan-biet-chuyen-doi-va-duoi-exe` | F858-02, lượt 1 `bfbd273` | Đóng phạm vi cũ | Bỏ đổi `-u` làm ca Windows đỏ; bộ lọc cũ đã bỏ. Native Windows còn chưa đo. |
| `stdout-installer-bi-nhan-lam-ket-qua-chon` | F858-03, lượt 1/2/3 | **Mở, P2** | Giữ PATH khi stdout installer có/không LF, LF/CRLF, thư mục/collision; N4 và control chỉ khác ranh giới dòng. |
| `cygpath-u-error-guard-khong-co-ca-am` | F858-04, lượt 2 `97544b5` | Đóng | Lỗi có stdout hợp lệ vẫn làm installer khác 0; mutant chỉ bỏ return bị hành vi giết. |
| `vuot-tran-diff-sensitive-chua-co-ngoai-le` | F858-05, lượt 2 `97544b5` | Đóng | Numstat ≤450 thêm/≤6 tệp; không bỏ test/assertion/mutant để đạt trần. |
| `chuyen-doi-windows-gan-nham-voi-github-path` | F858-06, mới lượt 3 | **Mở, P2** | Cả có/không GITHUB_PATH đều đo chuyển đổi; mutant gắn nhầm hai việc bị ca hành vi giết. |

**6 lớp đã đối chiếu, 2 lớp mở; 2 biểu hiện mở được báo trong bảng finding.** Không nhân số finding theo hai cách in stdout hoặc theo từng công cụ.

## Đột biến độc lập

`PYTHONDONTWRITEBYTECODE=1 python out/mutations.py` gọi nguyên các ca trên bản shell tạm; control **7 PASS, 0 skip**. Chỉ ngoại lệ **TinHieuChotCa** mới tính kill. [Mã driver](mutations.py), [kết quả từng ca](evidence/independent-mutations.json).

| Mutant | Kết quả thật |
|---|---|
| Bỏ dòng canh | N4 chết bằng **TinHieuChotCa**, đúng biến thể stdout thư mục; shape cũng chết. |
| Đổi về `:giu-nguyen-PATH:` | N4 chết bằng **TinHieuChotCa**, đúng biến thể `in_dau=trung`; shape cũng chết. |
| Chỉ bỏ `return 1` sau lỗi `cygpath -u` | Ca Windows chết bằng **TinHieuChotCa**, đúng `CYGPATH_U_HONG=1`; shape cũng chết. **Survivor lượt 2 đã bị giết.** |
| Bỏ toàn bộ chuyển đổi `-u` | Windows và shape đều **TinHieuChotCa**. |
| Bỏ trả lỗi `-w` | Windows và shape đều **TinHieuChotCa**. |
| Bỏ trả lỗi ghi GITHUB_PATH | Linux và shape đều **TinHieuChotCa**. |
| Chỉ chạy chuyển đổi `-u` khi GITHUB_PATH có giá trị | **SỐNG**, 7/7 liên quan; toàn suite không thêm lỗi. Chỉ probe bổ sung không GITHUB_PATH phân biệt được control/mutant. |

Mutant sống thay **điều kiện đi vào nhánh `-u`** thành phụ thuộc thêm biến ghi PATH; giữ nguyên câu lệnh/handler mà shape kiểm. Đây là thay đổi hành vi không tương đương: ngoài GitHub Actions, installer không có biến GITHUB_PATH vẫn phải dùng được `--win`. Không dùng code chết/chú thích giả để đánh lừa shape, không tính lỗi cú pháp hay giàn giáo làm kill.

Runner sẵn có `python .claude/dev/launcher_test.py --dot-bien` trả **rc=0, 293/293 đạt, 4 không đo được**. Số này khớp lời khai executor nhưng không phủ mutant mới. Đặc biệt dòng “OK” cho mutant bộ chọn gốc tạm không chứng minh native kill hợp lệ khi control `r858_goc_*` đang đỏ môi trường; không dùng headline thay kiểm loại tín hiệu. [Log toàn bảng](evidence/all-mutations.log).

## Kiểm việc thu gọn F858-05

`git diff 97544b5 HEAD` có **5 tệp đổi, 72 thêm/95 xoá**; `scripts/tl_selftest.py` không đổi kể từ lượt 2. So với merge-base, phân rã dòng thêm là **launcher_test 353 + manifest 11 + changelog 13 + shell 33 + YAML 16 + selftest 12 = 438**; có 30 dòng xoá.

`python out/compression.py` loại docstring khi so AST: **461 hàm → 461; 244 ca @ca → 244; 818 lời gọi bang → 818; 85 assert → 85**. Không mất tên hàm/ca. Chỉ **4 thân hàm** đổi ngoài docstring: stub `-u`, thêm ca âm `-u`, thêm N4 collision, thêm shape nguyên dòng guard. Đọc đối chiếu các thân này xác nhận assertion cũ còn nguyên. Bảng mutant **262+25+8 → 262+27+8**, hai mục mới, không bỏ mục cũ; anchor sentinel cũ được cập nhật theo sản phẩm. YAML sau parse **bằng nhau**, chỉ nén comment. Shell chỉ đổi câu lệnh sentinel trong phần hành vi, còn lại nén comment; manifest cập nhật hash/size changelog. Vì vậy lời khai “không bỏ ca âm, đột biến hay assertion” có bằng chứng cấu trúc và diff, không chỉ số đếm. [So AST các hàm đổi](evidence/compression-functions.diff), [log](evidence/compression-run.log).

## Bảng lệnh → kết quả thật

Lệnh tính từ workspace trừ khi nêu cwd. Driver đặt `PYTHONDONTWRITEBYTECODE=1`, `PIP_NO_INDEX=1`, TMPDIR dưới `out/`; chỉ dùng auth fixture giả. Hai cây nền/head dựng bởi cùng `python out/review.py setup` qua clone local không hardlink, cùng origin và cấu hình Git. Ghi argv/cwd/rc/thời lượng/stdout/stderr ra `evidence/`; rc=0 của driver thu kết quả không có nghĩa mọi subprocess đã pass.

| Lệnh / cwd | Kết quả thật |
|---|---|
| `git -C kho rev-parse HEAD HEAD^{tree}`; `merge-base HEAD origin/master`; băm byte spec | **rc=0**, OID/tree/nền/spec khớp các mốc ở đầu verdict. |
| `git -C kho diff --check 637f780 HEAD`; `git -C kho diff --numstat 637f780 HEAD` | **rc=0**; diff-check rỗng; **6 tệp/438 thêm/30 xoá**. |
| `python out/compression.py` | **rc=0**; không mất ca/assertion/mutant, các thay đổi hành vi đúng 4 hàm đã nêu. |
| `python out/checks.py suites`: mỗi cây `python .claude/dev/launcher_test.py --nhat-ky <log>` với/không CODEX_AUTH_JSON giả | Cả bốn **rc=1**; bảng delta bên dưới. [Nền sạch](evidence/base-suite-clean.log), [nền giả](evidence/base-suite-fake.log), [head sạch](evidence/head-suite-clean.log), [head giả](evidence/head-suite-fake.log). |
| `python .claude/dev/launcher_test.py --lap-ca <tên> --lan 1` ở `out/head` cho N4, Windows, shape | Mỗi lệnh **rc=0, 1/1 qua, 0 bỏ qua**. [N4](evidence/r858_bat_buoc_bash_khong_dua_rg_hong_len_dau.log), [Windows](evidence/r858_cai_windows_chon_ban_chay_duoc.log), [shape](evidence/r858_hinh_dang_cong_thuc_cai.log). |
| `python out/edges.py`; `python out/no_newline.py final`; `python out/no_gp_test.py` | Driver **rc=0**; rc con có cả 0/1/2 như bảng finding. N4 không LF là phép đỏ thật trên head; no-GP control PASS/mutant TinHieuChotCa. |
| `python out/mutations.py` | **rc=0** driver; control 7 PASS, 6 mutant chết đúng TinHieuChotCa, 1 mutant sống. |
| `python .claude/dev/launcher_test.py --nhat-ky <log>` ở `out/head` và `out/mutant-no-gp`, cặp cùng origin/core.abbrev/env | Cả hai **rc=1, 221/234**, cùng 13 đỏ/10 bỏ qua; delta lỗi **0**. [Control](evidence/matched-head-suite.log), [mutant](evidence/matched-mutant-no-gp-suite.log), [so tập](evidence/matched-delta.json). |
| `python .claude/dev/launcher_test.py --dot-bien` ở `out/head` | **rc=0, 293/293**, 4 không đo được; giới hạn tín dụng như trên. |
| Hai `python scripts/tl.py --selftest` song song ở `out/head` | Cả hai **rc=0, 1731/1731**, mỗi lượt đều `[OK] edit_skill_assert_count_gate_dry`. [Lượt 1](evidence/parallel-selftest-1.log), [lượt 2](evidence/parallel-selftest-2.log). |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ở `out/head` | **rc=0, ok=true**, expected_file_count=checked_file_count=**190**, failed/extra/missing rỗng. [Log](evidence/release-verify.log). |
| `CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py` ở `out/head` | **rc=0, 61/61**, bỏ qua=0, tiền kiểm bỏ qua=0, cổng cây thật ĐẠT, lỗi đột biến=0. **470 mutant giao job mảnh, không chạy đủ bán kính trong lệnh này.** [Log](evidence/cong-cu-manh.log). |
| `python scripts/tl.py golden-test --json`; `python scripts/tl.py doc-claims-check --strict --json` ở `out/head` | Đều **rc=0, ok=true**. [Golden](evidence/golden.log), [doc-claims](evidence/doc-claims.log). |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` ở `out/head` | **rc=0**, sạch, 10 tệp/0 chỗ chép doctrine. [Log](evidence/doctrine.log). |
| `bash -n ops/cai_cong_cu.sh`; `actionlint` ở `out/head` | Đều **rc=0**, stdout/stderr rỗng. [Bash](evidence/bash-syntax.log), [actionlint](evidence/actionlint.log). |
| `python -m ruff check --no-cache --select F .` ở `out/base`, `out/head` | Cả hai **rc=1, 8.806 finding**, delta=0. Đây là bare lint toàn cây, không đồng nhất scope với lời khai 4.409. Ruff **0.17.1**. [Nền](evidence/ruff-base.log), [head](evidence/ruff-head.log). |
| `python -m ruff check --no-cache --select F scripts/tl.py scripts/tl_selftest.py` ở `out/base`, `out/head` | Cả hai **rc=1, 4.404 finding**, delta=0. [Nền](evidence/ruff-scripts-base.log), [head](evidence/ruff-scripts-head.log). |
| `python -m ruff check --no-cache --select F scripts/tl.py scripts/tl_selftest.py .claude/dev/launcher_test.py` ở `out/base`, `out/head` | Cả hai **rc=1, 4.409 finding**, delta=0. Tái lập được số 4.409 trong scope ba tệp này; không gọi bare lint là pass tuyệt đối. [Nền](evidence/ruff-three-files-base.log), [head](evidence/ruff-three-files-head.log). |
| `python -B -c '<runpy ci_dang_ky_test.py; loi_ruff_ci()>'` ở `out/head` | **rc=0, RUFF_CONTRACT 3 []**; pin/probe contract đo riêng, không suy bare lint pass. [Log](evidence/ruff-contract.log), [argv đầy đủ](evidence/ruff-contract.json). |
| `python out/review.py snapshot` | HEAD/tree/status/diff/index và hash **4.839 tệp tracked** trùng snapshot đầu; không delta tracked/untracked/ignored. [Integrity](evidence/integrity.json). |

| Cây / môi trường | Passed | Skipped | Failed | Tổng | rc |
|---|---:|---:|---:|---:|---:|
| Nền, không auth giả | 214 | 10 | 12 | 236 | 1 |
| Nền, auth giả | 214 | 10 | 12 | 236 | 1 |
| Head, không auth giả | 221 | 10 | 13 | 244 | 1 |
| Head, auth giả | 221 | 10 | 13 | 244 | 1 |

**Delta thô: +1 ca đỏ**, đúng `r858_goc_tam_tranh_to_tien_co_git` mới. Trên head, ca này và t86 chọn `/var/tmp` rồi lỗi **EROFS**; nền t86 đỏ vì Codex home nằm dưới tổ tiên `.git`. 11 ca `r484_*` đỏ chung trong môi trường có `/tmp/.git` chỉ đọc. Không coi +1 là hồi quy runtime, cũng không khai delta số ca đỏ bằng 0. [Mountinfo](evidence/mounts.log), [delta](evidence/suite-delta.json). Không sửa `_KhoCodex`, t86 hay các ca packet khác để ép xanh.

## Không đo được

- **Native Windows/macOS, Git Bash/MSYS, `.exe`/PATHEXT và trình cài thật**: chưa có capability; các ca Windows ở đây là Bash/Python trên Linux với stub `cygpath` ánh xạ `V:`. Chưa xác nhận floor 70% và N2 trên runner Windows thật.
- **N5 end-to-end sạch**: `/tmp/.git` là mount ro, các gốc thay thế không ghi được trong sandbox này. Không tháo mount/nới storage; không chạy lại t86 ×10 để gọi thất bại lặp là chứng nhận thành công. Control gốc tạm native đỏ, nên không tính headline mutant tương ứng làm bằng chứng đã giết đúng hành vi.
- **10 ca launcher bỏ qua**: 8 ca cần venv/pip không dựng được offline, 1 fixture chỉ Windows và 1 ca native Windows SID. Không cộng chúng vào số qua; 11 ca r484 lỗi môi trường vẫn giữ trạng thái failed, không đổi thành skipped.
- **GitHub/CI/lease ngoài bundle**: theo lệnh không gọi GitHub; không xác nhận ci.yml, workflow_dispatch Windows, check-run provenance, thread resolution, heartbeat hiện tại hay quyết định khác ngoài lease đã cấp. Không có quyền push/merge/land/deploy.
- **Provenance verdict trước trên nhánh lease**: đã đo thiếu cả hai đường được nêu trong prompt ở ref g2 và thiếu ref g1; không xác nhận trạng thái commit bên ngoài bundle. Bản lượt 2 local vẫn đọc được và được dùng làm nguồn đối chiếu như đã khai.
- **470 mutant cong_cu_test**: lệnh `manh` giao cho job mảnh; chưa chạy/thu kết quả đủ bán kính trong lượt này. Bộ launcher 293/293 không thay phép đo đó.
- **Python** theo phụ lục chủ kho (a): chỉ rc=0 và không in/ghi thư mục bản hỏng; nợ `python-probe-khong-theo-PATH` còn mở. Không sửa `ops/cong_cu.py`, không khai Python ứng viên đã được probe theo PATH.
- Hướng namespace/đường dẫn trên Windows cần nội dung hoặc môi trường ngoài khả năng được cấp chỉ được mô tả ở trên, không báo thành phép đã chạy.

Hai sai lệch giàn giáo reviewer được giữ riêng: ma trận edges đầu đã vô tình đổi stdout của cả trình cài rg, nên không dùng nó làm finding; bản cuối chỉ đổi installer bash. Lượt selftest đầu đã ép `core.abbrev=7` qua env, làm r226 không đổi được abbrev trong Git fixture; đã bỏ override env, giữ pin ở config local checkout và chạy lại. [Log đầu](evidence/edges-run.log), [selftest đầu](evidence/selftest.log). Chúng không được tính là lỗi sản phẩm hay kill đột biến.

Snapshot sạch chứng minh không có delta ở hai mốc quan sát, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Các hiện vật review đều dưới `out/`; không có patch sản phẩm, commit, push hoặc liên lạc GitHub. Hash verdict, driver, shell mutant và evidence nằm trong [SHA256SUMS](SHA256SUMS); bản clone/fixture không nằm trong danh mục băm này.
