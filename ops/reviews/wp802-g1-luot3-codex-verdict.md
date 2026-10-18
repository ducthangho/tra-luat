verdict: changes_requested
reviewed_sha: a0de1f9e3be9d4e63369346c58d77bdb7a1a04c1

Chốt lượt 3: còn **2 lớp P2 cần sửa** — F2 chưa đóng tiêu chí chọn bản rg; F6 là hồi quy resolver Windows do hunk lượt này. F3 còn **1 nợ test P3**, owner executor wp802, cần chủ kho quyết định nếu giữ lại. Không phát hiện P0/P1 trong phạm vi đo. Kết luận xuất phát từ phản chứng mã, không phải vì không gọi được GitHub.

Reviewer: OpenAI Codex, provider `openai_codex`, execution surface `codex_service` (API agent có shell), transport `machine`. Họ model OpenAI theo phiên; model ID/effort/session ID và danh tính executor thực chạy chưa có runtime receipt độc lập: **KHÔNG ĐO ĐƯỢC**. Lease khai reviewer `codex_cli`; đây là dữ liệu cấu hình, không được dùng để đổi lời khai surface thực tế của lượt này. Không tự cấp receipt/assurance/merge authority. Áp ngưỡng prompt: hết P0/P1 và mọi P2 đã đóng; P3 cần quyết định có căn cứ. Đây là lời gọi 3/4 theo assignment, không lấy bộ đếm `used: 0` lịch sử trong lease để reset ngân sách.

Đã đọc prompt.snapshot, SPEC, AGENTS/CLAUDE, protocol §8/§13, adapter cross-review, verdict lượt 1–2 và diff. Checkout `cay-kho/` giữ nguyên; phép đo/vá thử trên clone hoặc scratch ở `review-data/`. Không push, không gọi GitHub, không soạn payload đường dẫn thoát cây. Không phát patch runtime/launcher/hook cho packet sensitive; hướng sửa bên dưới là mô tả. Các tệp EVIDENCE là dữ liệu executor, được đối chiếu và tách khỏi phép chạy độc lập. Log dài được giao agent read-only theo CLAUDE.md bước 5, rồi kiểm lại các dòng quyết định.

Neo: HEAD/tree `a0de1f9e3be9d4e63369346c58d77bdb7a1a04c1` / `dc4671c3242b2967f937bb79ac873ab36fd049ac`; merge-base/tree `fb490a7c3fa2992c6f4635ed091dafa813df2fe7` / `78cf0bfe8ac4b327ce834800ccf687c6d42f52c9`. SPEC SHA-256 `e4fd84e1f079d0ac4841a145d078473576af3a3e4e2f593e4f3e40c5de7200e0`. Diff/numstat cấp trong bundle khớp byte với Git. Drift từ base lease de82ef74 tới merge-base không chạm 6 tệp write set.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn F1–F4: lượt 1 `db1ed4dda529eb30806ecb053d2eef9933e188b1`; lượt 2 `509dfa850ecb73a3624a777c699fd8a05812cc25` còn F2/F5 P2 và nợ test F3 P3. Giữ slug, không reset theo baseline.

| Lớp / finding | Phân loại lượt này | Phép kiểm đóng lớp và kết quả độc lập |
|---|---|---|
| F1 `bare-path-empty-entry` | **VÁ SINH LỖI MỚI** trong đường resolver dùng chung; phản chứng gốc đã sửa | PATH rỗng đầu/giữa, dot, hai bản hỏng trước bản tốt, symlink hỏng/tốt/dangling và non-executable đều đúng trên POSIX. Bare hỏng ⇒ doctor12/BI_CHE đúng bad1; đối chứng tốt ⇒0. Nhưng dùng helper Bash cho `_cac_duong_dan` của mọi công cụ sinh F6 trên Windows. Không tuyên bố resolver đã đóng toàn nền. |
| F2 `installer-selects-broken-path` | **VÁ HỜ ở mức đóng lớp** | Links rc1, rc0 rỗng, invalid-version + choco tốt đều0/DAT đúng choco. Ba biến thể có chữ trong token phiên bản vẫn chọn Links rồi2/DO; Links phiên bản chỉ ở stderr bị bỏ qua dù probe cuối chấp nhận. Cùng cơ chế hai chuẩn khác nhau, còn P2. |
| F3 `hook-pointer-restore` | **ĐÃ VÁ THẬT hành vi; VÁ HỜ nợ test** | Runner với cả hai con trỏ riêng và cả mục hook/YAML trả `[0,0]`, phục hồi true/true. Ca mới chỉ đổi hook: gỡ riêng restore YAML còn PASS. Ca tăng cường thêm mục YAML trên scratch làm mutant ấy chết đúng TinHieuChotCa; còn P3 độ phủ, không phải lỗi restore tại head. |
| F4 `windows-hook-mutation-count` | **ĐÃ VÁ THẬT lời khai** | Giả cờ skip Windows: `[0,6]` cho bảng mới 7 hook/YAML; đúng6 không đo, mutant đối chiếu chuỗi vẫn1/1. Log Windows thật cũng khớp6. Handoff hiện khai tổng quát, không còn số cũ sai. |
| F5 `windows-hook-installer-fallthrough` | **ĐÃ VÁ THẬT** | Bash thật, uname giả từng MINGW/MSYS/CYGWIN × rg hỏng/tốt/flaky: không installer, probe tốt/flaky đúng1 lần. Linux hỏng vẫn apt-get→cargo. Mutant trả điều kiện hai probe làm N8 chết bằng chính assertion nhật ký. |

Bảng lớp: **6 lớp / 2 P2 mở / 1 P3 mở**. F1 phản chứng gốc, F4 và F5 đã có bằng chứng sửa trong phạm vi nêu trên. F2 giữ mọi biểu hiện từ ba lượt; ba token lỗi + kênh stderr là các biểu hiện của một lớp tiêu chí chooser khác probe cuối, sửa chung bằng một chuẩn xác thực. F6 là lớp mới `tool-resolver-prefers-shell-shim`: con trỏ F1 rỗng và việc bỏ ứng viên PATHEXT khác cơ chế, nên ghi lớp mới và nối rõ về hunk chữa F1. Không cộng F6 hai lần vào số P2. F3 không đóng nợ test chỉ nhờ mutant gỡ cả hai restore bị giết.

## BẢNG SĂN

Các lệnh từ rv3, trừ suite/gate có cwd clone tương ứng. Mọi phép Python chạy sản phẩm/test đặt `PYTHONDONTWRITEBYTECODE=1`; Ruff `--no-cache`. Hai cây dựng cùng vòng lệnh: `git clone --no-hardlinks --no-checkout`, `core.abbrev=7`, `core.autocrlf=false`, detached SHA tường minh, origin đặt endpoint repo thật nhưng không dùng mạng. Không dùng worktree. Môi trường local Linux/Python3.13.16.

| Hướng / lệnh hoặc hiện vật | Output thật rút gọn | Kết luận |
|---|---|---|
| `setup.py`; SHA/spec/diff/write set | Đúng SHA/hash; 6 tệp, **448 thêm /22 xóa**, còn2 dòng tới trần450 | Đạt ADR-0053; không viện Q9 vượt trần |
| `probe_review.py` / doctor | Empty/dot/bad1→bad2→good ⇒12/BI_CHE đúng bad1; only-good/good-link/dangling/nonexec ⇒0; bad-link ⇒12 | Phản chứng POSIX F1 đã chữa |
| `probe_boundaries.py` / timeout-budget | bad→slow→good ⇒12; slow→good ⇒0 không BI_CHE; hết budget ⇒0 mặc định/13 strict, chưa có bản tốt | Không gán timeout/hết budget thành bản hỏng |
| `probe_resolution.py` / 45 đối chứng | 5 công cụ ×9 bố cục; EXE/CMD/PATHEXT/tên có đuôi/tương đối cùng rc0; shim+CMD base0→head12, sửa thử CMD→0; shim+EXE vẫn0 vì CreateProcess có thể tự thêm.exe | **P2 F6**, phép đo thuật toán Windows + seam spawn, không phải OS thật |
| `boundary-results.json` / cwd Windows | Old which chèn cwd cho từng thư mục; head chọn đúng tệp trong PATH cho cả5 công cụ | Xác nhận mục đích sửa helper có tác dụng; không phủ định F6 |
| `installer-results.json` / phản chứng lượt2 | rc1/rỗng/invalid-version ở Links + choco tốt ⇒0/DAT; GITHUB_PATH đúng choco | Biểu hiện cũ đã sửa |
| Cùng script / glob và kênh output | `1a.2b.3`, `1.2x.3`, `1.2.3junk` ⇒2/DO, ghi Links; stderr-only ⇒1 dù Links dùng được theo checker. Scratch cùng chuẩn checker ⇒0/DAT | **P2 F2** vẫn mở |
| Cùng script / nhánh installer | winget tốt: chỉ WINGET; winget lỗi: WINGET,CHOCO; cả hai lỗi:rc1; fallback command-v cuối:0/DAT | Đạt hợp đồng Bash đã đo; stub không là Windows installer thật |
| Cùng script / guard/init | Không ứng viên⇒rc1/không ghi path. Gỡ guard: công thức trực tiếp rc0/rỗng nhưng wrapper kiểm cuối rc2. Gỡ init + RG_DICH thừa kế: chọn seed,0/DAT; head từ chối1 | Hai chốt có tác dụng, thiếu ca stock phủ precondition |
| `hook-results.json` | 9 tổ hợp Windows không installer; good/flaky1probe. Linux hỏng có apt-get,cargo | F5 đóng, N7/N8 POSIX đạt |
| `runner-results.json` | Control hai con trỏ đúng; gỡ YAML độc lập mất YAML nhưng ca stock PASS; ca tăng cường assertion đỏ. AttributeError giả ⇒ runner `[2,0]`, SAI0/1 cho mỗi mục | F3 còn P3; hook/YAML runner không nhận lỗi vô can làm kill |
| `run_suites.py` / full và auth | Head211/223, base201/213 ở CẢ HAI chế độ; mỗi lượt12đỏ/10skip, rc1. Tập12đỏ trùng hoàn toàn | DELTA đỏ0; N/N chưa tái lập do rig `/tmp/.git`, không phải lỗi PR |
| Cùng script / `--dot-bien` | Head267/267, base250/250; rc0/rc0, mỗi bên4 không đo | Tăng đúng17; không đồng nhất headline với mọi kill thật |
| `audit_mutations.py` | 17 wp802 mutant,20 lượt assertion đúng ca,0 lỗi vô can; control10r802+t106 đềuPASS | Các kill mới thật; giới hạn độ phủ ở bảng dưới |
| `run_survivors.py` /5 mutant toàn suite | Gỡ guard/init/grammar, trả resolver về which, gỡ riêng abspath: mỗi mutant không thêm ca đỏ so control | Chốt nào chưa được ca đo phải ghi riêng, không lấy267/267 thay phủ hành vi |
| `run_gates.py` | Ruff5F841 mỗi bên,DELTA0; contract3/errors[]; bash_nen DAT; doctrine10tệp/0; bash-n0; release WORKER head188/188,base187/187,ok=true | N11/local N12 đạt theo phạm vi; không gọi bare lint là xanh |
| `cong-cu-target-results.json` | t23/t49 chạy POSIX trên cả hai cây đềuPASS; các dependency và ca cùng byte | Không có delta PR; native Windows master chưa đo hai ca này |

### Đột biến từng chốt mới và tín dụng

| Chốt / đột biến bản sao | Phép đo và đánh giá |
|---|---|
| Tiêu chí phiên bản / nới thành mọi rc0 | Ca F2 mới chết TinHieuChotCa do Links rỗng bị chọn; **kill thật**. |
| Phần chữ số của glob / chỉ giữ prefix `ripgrep ` | Qua toàn suite, không thêm đỏ; stock chỉ phân biệt rỗng với bản tốt, chưa canh grammar/token. Phản chứng F2 độc lập giết được bằng DAT + đúng thư mục. |
| `: "${RG_DICH:?…}"` / thay `true` | Qua toàn suite; stock luôn có ứng viên tốt. Phép đo không ứng viên phân biệt trực tiếp công thức1→0/rỗng, nhưng wrapper vẫn2/DO nhờ lớp cuối; không báo head xanh giả. |
| `RG_DICH=` / bỏ khởi tạo | Qua toàn suite; có biến thừa kế + không ứng viên mới phân biệt được. Probe reviewer: head1, mutant0/chọn seed. |
| Windows chọn nền trước probe / trả điều kiện hai probe | N8 chết đúng assertion `RG 1` và nhật ký installer,0 lỗi vô can; **kill thật**. Kiểm độc lập MINGW/MSYS/CYGWIN. |
| `_cac_duong_dan` dùng helper theo từng thư mục / trả which | Qua toàn suite Linux; Windows cwd-insertion chỉ đo thuật toán, chưa chạy mutant này trên Windows thật. Không kết luận thiếu ca trên mọi nền; F6 cho thấy thiếu đối chứng shim + CMD của các công cụ khác. |
| Dedup bare `abspath` / chỉ normcase | Qua toàn suite. Seam `_cac_duong_dan` trả đường tương đối: head probe2, mutant3 lần. Resolver PATH hiện trả absolute nên không coi survival tự thân là lỗi sản phẩm hoặc chứng minh mutant không tương đương trên mọi đầu vào tự nhiên. |
| Ca F3 / bỏ cả hai restore | Ca mới đỏ TinHieuChotCa; **kill thật cho hook**. Bỏ riêng hook cũng đỏ; bỏ riêng YAML PASS. Suy từ kill ghép ra “đã canh YAML” là tín dụng độ phủ giả. Ca tăng cường mục YAML diệt được mutant YAML riêng. |
| Các9 launcher +7 hook/YAML +1 harness wp802 đã khai | Audit độc lập đúng20 assertion đích/17mutant,0 ngoại lệ vô can. Không có kill giả do exception trong17mutant này. |
| Mutation runner cũ | Cả base/head có cùng14 dòng nhận kill bằng tín hiệu khác TinHieuChotCa (4 AssertionError trần +10 ngoại lệ kiểu),0 dòng wp802. Đây là tín dụng giả/nợ nền đã nêu lượt1–2,DELTA0; không dùng headline chứng nhận toàn bộ267 kill thật. |

Ngoài yêu cầu từng chốt, đã thử gỡ os.access/PATHEXT:10 r802+t106 Linux không đỏ; non-executable độc lập phân biệt guard access, còn PATHEXT là đường Windows, không suy Linux phủ nó. Mỗi mutant nằm ở bản sao riêng; không viết rồi hoàn nguyên mã được review. Neo ghép bị giết không cho tín dụng tự động cho từng thành phần.

## BẢNG ĐO

| Khẳng định / tiêu chí | Bằng chứng và giới hạn | Đánh giá |
|---|---|---|
| 6 tệp/≤450 thêm | Git thật: launcher61/7,test345/11,hook13/3,changelog9/0,yaml7/1,handoff13/0 ⇒448/22; đúng write set | Đạt; còn2 dòng |
| 10 ca/17 mutant mới | CA233−223=10; mutation271−254=17=9launcher+7hook/YAML+1harness | Khớp handoff |
| N1–N4 | Ca stock + phản chứng độc lập POSIX và mutant đúng assertion | Đạt trong phạm vi đo; F6 là hồi quy khác của helper |
| N6 | Ba prefix Windows/Linux/hook khớp YAML; mutant mỗi bên làm đỏ; PyYAML chỉ phụ thuộc test | Đạt parity chuỗi, không chứng minh chooser |
| N7/N8 | Bash thật/stub installer, cả ba nhận diện Windows và probe biến động | Đạt POSIX simulation, không gọi là Windows native |
| N10 Linux không auth | Executor EVIDENCE231/231/skip2. Reviewer head211/223,total233,skip10,đỏ12; base201/213,total223,skip10,đỏ12;rc1 | N/N **KHÔNG ĐO ĐƯỢC trong rig này**,DELTA đỏ0 |
| N10 Linux auth giả | Cùng số trên với `CODEX_AUTH_JSON='{"tokens":{"x":"gia"}}'`; suite pop biến ngay đầu | DELTA đỏ0, không nhận231/231 là tự tái lập |
| Mutation Linux | Head267/267,base250/250,4 không đo mỗi bên;17 mới có audit riêng | Khớp headline executor, có giới hạn14 tín dụng nền |
| N11 Ruff | Bare Ruff0.17.1,selectF,2file,no-cache: mỗi bên5F841/rc1. Contract cài/probe:3,errors[],rc0 | Đạt DELTA0; chưa chạy binary pinCI0.15.15 |
| N11 khác | bash_nen DAT; doctrine10file/0vi phạm; bash-n0, cả hai cây | Đạt local |
| N12 WORKER | Manifest ngoài checkout,verifystrictok=true; head188/188,base187/187; mọi tệp tracked. Chênh1 đúng fragment wp-802 | Đạt local; job PR exact head **KHÔNG ĐO ĐƯỢC** |
| Lease/ref/usage lịch sử | Blob f6159dc475c261cfbc80725b676b4f9391d6e592 khớp spec/write set/giới hạn3attempt,4calls | Chỉ metadata; server596↔596,hai run lease,usage thực **KHÔNG ĐO ĐƯỢC** |

### Evidence Windows và gate-cong-cu

**KHÔNG ĐO ĐƯỢC trực tiếp Windows/CI tại phiên reviewer**; các dòng sau đánh giá log executor được cấp, không tự nhận đã chạy Windows hoặc xác minh server/check-run provenance. Không giữ changes_requested chỉ vì hạn chế này.

| Bằng chứng cấp | Đọc được gì | Không được suy thêm |
|---|---|---|
| `EVIDENCE_windows_39097277600_a0de1f9.log:103,130` | Fetch/checkout đúng full SHA reviewed; job launcher Windows; Python3.13.16 | Không tự xác minh run/attempt/check-run authority qua server |
| N9,log:182–188,215–233,332–339 | Chạy cai_cong_cu.sh; rg DAT15.2.0; shell bước sau vẫn DAT | Stdout installer giữ trong KET_QUA_CAI nên không biết winget hay choco thực chạy |
| N5,log:458,472–473 | Tổng200/200,total233,skip33,hỏng0; N1 đăng ký không có skip,fixtureWindows0byte; các mutant đích hiện đúng tên N1 | Suy luận mạnh rằng N1 đã qua, nhưng **thiếu dòng qua riêng** đúng định dạng SPEC N5. Dòng mutation là ca đỏ của mutant, không thay dòng qua control. Cần nhật ký/--lap-ca exact head để đáp ứng literal N5; không kết luận ca đã bỏ qua |
| Windows mutation,log:752–766 |192/192,79khôngđo.17wp802:11đo,6khôngđo;9launcher+1parityhook+1harness đo;0hậu tố exception ở wp802 | Không chứng nhận6mutant shell POSIX trên Windows; Linux đo chúng riêng |
| `EVIDENCE_gate_cong_cu_windows_cb7f83f.log:806,1058–1067` | Checkoutcb7f83f80625ea161fab750d0700361bee923fcb; t23/t49 đỏ;52/54,total56,skip2,rc1 | Đây là head cũ, không phải ci.yml trên a0de1f9 |
| `EVIDENCE_master_gate_cong_cu_windows_fb490a7.log:853,932–966` | Checkoutfb490a7; dừng ở cài rg KHONG_DO_DUOC,rc3 trước suite | Không thể nói master đã chạy và cũng đỏ t23/t49 |

Đánh giá lời khai executor: **có căn cứ mạnh rằng t23/t49 không do PR**, không chỉ vì “ngoài write set”. Ba tệp `ops/cong_cu_test.py`, `ops/bash_nen.py`, `ops/cai_cong_cu.sh` giống byte giữa base, cb7f83f và reviewed head. t23 dựng manifest riêng công cụ batch-path-t21 (`cong_cu_test.py:2766`–`:2786`), không dùng công thức rg. Assertion tại2832 tìm hai ký tự backslash+r trong stderr; đường warning `C:\Users\runneradmin...` trong log1058 đã có chuỗi đó, giải thích báo đỏ giả từ warning mà không cần lỗi CRLF. t49 tại6015–6038 dựng repo/công cụ quét riêng và mất khóa Unicode; không đọc công thức rg. Reviewer chạy đúng hai ca trên POSIX: cả base/head đều PASS. Giới hạn vẫn là chưa đo chúng trên master Windows; màu đỏ master sớm hơn tự nó không chứng minh cùng nguyên nhân.

Bundle chưa cung cấp ci.yml dispatch/check-run thành công trên exact a0de1f9 hoặc release-verify PR exact head. Giữ M-3/Q7/N12 là phần điều phối cần readback; không tự đổi thành lỗi sản phẩm mới. WindowsApps thật, macOS và việc CLI tìm kiếm nội bộ có dùng rg PATH không vẫn chua_do_duoc theo SPEC.

### installer-selects-broken-path [P2] F2 — Glob mới vẫn chọn phiên bản mà probe cuối từ chối

**TỆP/DÒNG:** `ops/cong_cu.yaml:93`; cùng lớp F2 lượt 1–2, không đổi slug. Probe cuối tại `ops/cong_cu.py:184` và regex tại `ops/cong_cu.yaml:83`.

**VẤN ĐỀ:** Mẫu shell `"ripgrep "[0-9]*.[0-9]*.[0-9]*` không phải regex phiên bản. Dấu `*` ăn cả chữ sau chữ số. Links in `ripgrep 1a.2b.3`, `ripgrep 1.2x.3` hoặc `ripgrep 1.2.3junk` vẫn được chọn và ghi vào GITHUB_PATH, rồi `cai_cong_cu.sh` trả rc2/DO dù choco/bin có bản tốt 15.2.0. Các phản chứng cũ rc1/rỗng/invalid-version đã qua, nhưng lớp tiêu chí chooser yếu hơn probe cuối còn mở.

**ĐÃ THỬ VÁ:** Trên YAML tạm trong scratch, dùng cùng regex và phép kiểm trọn token của `cong_cu.py` để chọn ứng viên; các đầu vào trên chuyển sang choco/bin, rc0/DAT. Không sửa cây executor hoặc phát patch runtime.

**ĐÃ THỬ NGHIỆM:** `PYTHONDONTWRITEBYTECODE=1 python review-data/probe_review.py`, `review-data/installer-results.json`. Chạy nguyên Bash `ops/cai_cong_cu.sh rg`; chỉ winget/choco/cygpath và các rg là fixture, không installer thật/mạng. Stock ca hiện chỉ đo Links tốt hoặc rỗng; mutant nới pattern thành chỉ prefix `ripgrep ` qua cả toàn suite, không thêm ca đỏ so control. Biến thể Links chỉ in phiên bản ra stderr bị head bỏ qua (rc1); sửa thử dùng cùng kênh output và bộ kiểm token cuối cho rc0/DAT.

**ĐỘ TIN:** Cao về lỗi chooser/Bash; không nhận là đã chạy Windows native. Quyết định: SỬA bằng một chuẩn tương đương probe cuối và khóa các biên token, không chỉ thêm ví dụ vào glob.

### tool-resolver-prefers-shell-shim [P2] F6 — Resolver mới làm mất bản CMD cùng thư mục trên Windows

**TỆP/DÒNG:** `.claude/dev/launcher.py:2286`, `:2309`–`:2316`; `_phien_ban` gọi trực tiếp bằng subprocess tại `:2341`.

**VẤN ĐỀ:** `_cac_duong_dan` đổi từ `shutil.which` sang helper giả lập Bash cho MỌI công cụ. Helper luôn thử tên không đuôi trước PATHEXT, trả đúng một tệp của mỗi thư mục. Khi thư mục có shell shim `codex` và `codex.CMD` chạy được, danh sách chỉ giữ shim; probe native thất bại và không bao giờ thử CMD cùng thư mục. Tương tự claude/npm; cả gh/node/bash bị ảnh hưởng khi có hai hình dạng tệp đó. Trước bản vá, CPython 3.13 `which` dùng PATHEXT chọn CMD. Cặp shim + EXE là đối chứng khác: CreateProcess có thể tự thêm .exe nên không kết luận cặp ấy gây lỗi spawn. Npm `cmd-shim` cục bộ thực sự tạo đồng thời tệp không đuôi, `.cmd`, `.ps1` (`/opt/node22/lib/node_modules/npm/node_modules/cmd-shim/lib/index.js:234`).

**ĐÃ THỬ VÁ:** Chỉ trong bộ nhớ scratch, cho resolver công cụ native chọn các ứng viên PATHEXT trong từng thư mục; giữ resolver bare shell riêng cho rg/git. Năm công cụ trên đều trở lại rc0/co=true trong cùng seam probe. Executor cần giữ các ứng viên chạy được trong cùng thư mục, không buộc chuẩn tìm của Bash lên đường subprocess native.

**ĐÃ THỬ NGHIỆM:** `review-data/probe_resolution.py` và `resolution-results.json`: 45 đối chứng = 5 công cụ × 9 bố cục, cùng fixture cho base/head. Dùng nhánh Windows của CHÍNH mã `shutil.which` CPython 3.13 đang cài, bật platform Windows cho helper; filesystem POSIX, probe WinError193 là seam giả. Khi chỉ EXE/CMD, PATHEXT đảo, tên có đuôi hoặc PATH tương đối: hai cây cùng rc0. Khi shim không đuôi cùng CMD: base rc0/co=true, head rc12/co=false; bản thử CMD rc0. Với shim + EXE, seam giữ khả năng tự thêm .exe: cả hai rc0, dù đường resolver chọn khác nhau. Trên Linux tuyệt đối/tương đối: hai cây rc0, chỉ biểu diễn đường dẫn chuyển thành tuyệt đối. Mutant trả resolver về which qua toàn suite Linux mà không thêm ca đỏ. Phép đo cwd-insertion riêng xác nhận helper mới có ích về chọn đúng thư mục, nhưng không giải quyết việc bỏ CMD cùng thư mục.

**ĐỘ TIN:** Cao về thay đổi thuật toán và việc bỏ mất ứng viên; KHÔNG ĐO ĐƯỢC CreateProcess/ACL/NT filesystem thật tại đây. Không gọi mô phỏng này là chạy Windows. Đây là hồi quy sản phẩm mới do hunk lượt 3, cần ca Windows có cặp shell shim + CMD.

### hook-pointer-restore [P3] F3 — Ca mới chỉ canh khôi phục hook, chưa canh YAML

**TỆP/DÒNG:** `.claude/dev/launcher_test.py:8140`, `:10587`.

**VẤN ĐỀ:** Hành vi hiện tại trả đúng cả hai con trỏ. Ca F3 mới chỉ tạo đột biến hook; YAML không bao giờ đổi nên assertion hai con trỏ không kiểm được nhánh khôi phục YAML. Bỏ riêng khôi phục YAML vẫn qua ca ấy, trong khi bỏ hook hoặc cả hai làm đúng `TinHieuChotCa`. Mutant harness khai báo gỡ cả hai chỉ chứng minh phần hook.

**ĐÃ THỬ VÁ / ĐÃ THỬ NGHIỆM:** Đột biến trên tệp test sao tạm, ghi `review-data/mutation-audit.json`; đối chứng độc lập hai loại mục mất đúng con trỏ khi gỡ riêng từng restore; ca tăng cường thêm mục YAML giết được mutant YAML bằng TinHieuChotCa trong khi control vẫn PASS (`runner-results.json`). Không sửa checkout.

**ĐỘ TIN:** Cao. Nợ test lớp F3 còn mở, owner executor wp802; thêm mục YAML độc lập rồi gỡ mỗi restore phải làm đúng ca đỏ. Chủ kho cần quyết định P3 nếu giữ lại.

## TOÀN VẸN VÀ BÀN GIAO

Snapshot đầu/cuối checkout `cay-kho`: **3765/3765 tệp ngoài `.git` khớp byte,0delta**, cùng HEAD/tree/status (kể cả ignored/untracked)/diff/index. Xem `review-data/snapshot-comparison.json`. Sandbox thực tế workspace-write; read-only checkout là kỷ luật được kiểm bằng snapshot, không tự nhận sandbox cưỡng chế. Snapshot chỉ chứng minh hai mốc không có delta quan sát, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.

Các lệnh, rc và output đầy đủ ở `review-data/`: preflight.json, suite-results.json, các log base/head full/auth/mutation, installer-results.json, doctor-results.json, hook-results.json, resolution-results.json, boundary-results.json, runner-results.json, mutation-audit.json, survivors-full-results.json và base/head-gates.json. Artifact manifest ghi path/size/SHA-256 của script, log, dữ liệu và verdict sau khi chốt; không dùng artifact lịch sử lượt khác thay cho lượt này.

**Quyết định cuối: changes_requested.** Cần đóng F2 và F6; F3 còn P3 nợ test với owner/hướng xử lý đã nêu. Việc xin quyết định P3 và kiểm receipt/CI/merge thuộc điều phối/chủ kho; review này không cấp quyền land.
