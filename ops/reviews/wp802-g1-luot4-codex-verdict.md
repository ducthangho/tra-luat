verdict: changes_requested
reviewed_sha: 3d65c954cd86c5138d3ad11998b272ead787f88c

Chốt lượt **4/4, CUỐI**: còn **2 lớp P2 mở — F2 và F6**. F3 đã đóng cả hành vi và nợ test. Không phát hiện P0/P1 trong phạm vi đo. Không đề nghị thêm lượt Codex ngoài ngân sách; phần chưa hội tụ cần checkpoint của chủ kho/điều phối. Kết luận dựa trên phản chứng mã, không phải do không gọi được GitHub.

Reviewer OpenAI Codex; provider `openai_codex`, execution surface `codex_service` (API agent có shell), transport `machine`. Model ID/effort/session ID và danh tính executor thực chạy chưa có receipt độc lập: **KHÔNG ĐO ĐƯỢC**. Không suy surface `codex_cli` từ lease; không tự cấp assurance/merge authority. Ngưỡng assignment: hết P0/P1, mọi P2 phải đóng; P3 còn mở phải trình chủ kho quyết định.

Đã đọc assignment/SPEC, AGENTS/CLAUDE, protocol §8/§13, adapter cross-review, ba verdict trước và diff. Không push, không gọi GitHub, không sửa checkout `cay-kho`; mọi phép sửa thử nằm trong `review-data/`. Không tự soạn payload đường dẫn thoát cây. EVIDENCE là dữ liệu executor, tách khỏi phép tự chạy. Nhật ký tăng dần trước khi chốt được giữ tại `review-data/VERDICT-progress.md`.

Neo HEAD/tree: `3d65c954cd86c5138d3ad11998b272ead787f88c` / `5f05431c8fb2df7438cd426635666af310426d0e`; merge-base/tree: `fb490a7c3fa2992c6f4635ed091dafa813df2fe7` / `78cf0bfe8ac4b327ce834800ccf687c6d42f52c9`. SPEC SHA-256 `e4fd84e1f079d0ac4841a145d078473576af3a3e4e2f593e4f3e40c5de7200e0`. Diff/numstat bundle khớp byte với Git. Drift từ base lease `de82ef74` tới merge-base không chạm sáu tệp write set. `abc16deb3d8250a4ddf1add1a23a0eb08f9f3246` tới reviewed head chỉ đổi handoff.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: lượt1 `db1ed4dda529eb30806ecb053d2eef9933e188b1`; lượt2 `509dfa850ecb73a3624a777c699fd8a05812cc25`; lượt3 `a0de1f9e3be9d4e63369346c58d77bdb7a1a04c1`. Giữ slug, không reset lịch sử theo SHA hoặc biểu hiện mới.

| Lớp / finding | Phân loại | Phép kiểm độc lập và kết luận |
|---|---|---|
| F1 `bare-path-empty-entry` | Phản chứng gốc **ĐÃ VÁ THẬT**; hồi quy resolver chung nối F6 | PATH rỗng đầu/giữa, dot, bad symlink, hai bản hỏng trước bản tốt: Bash1/doctor12, BI_CHE đúng bản đầu. Good symlink, dangling, nonexec, chỉ bản tốt: Bash0/doctor0. Không lấy POSIX để tuyên bố mọi resolver Windows đã đóng. |
| F2 `installer-selects-broken-path` | **VÁ SINH LỖI MỚI**, lớp còn P2 | `1.2.3junk`/`1a.2b.3`/`1.2x.3`, rc0 rỗng, rc1 đều lùi choco; stderr-only chọn Links đúng. Nhưng warning trước phiên bản bị chooser từ chối dù checker DAT. Warning stderr: YAML lượt3 thành công, head thất bại, sửa thử bằng checker chuẩn thành công. |
| F3 `hook-pointer-restore` | **ĐÃ VÁ THẬT**, đóng P3 lượt3 | Control có cả mục hook và YAML qua. Gỡ riêng restore hook và gỡ riêng restore YAML đều chết bằng `TinHieuChotCa` của `r802_runner_tra_lai_con_tro_nguoi_goi`. Không suy từ mutant ghép. |
| F4 `windows-hook-mutation-count` | **ĐÃ VÁ THẬT** lời khai hiện tại | Có7 hook/YAML;6 không đo trên Windows,1 parity còn đo. Log Windows khớp6; handoff không giữ con số cũ sai. Hai mutant resolver Windows-only được khai riêng. |
| F5 `windows-hook-installer-fallthrough` | **ĐÃ VÁ THẬT** trong phạm vi kiểm | MINGW/MSYS/CYGWIN × rg tốt/hỏng/flaky: không installer; flaky đúng `RG 1`. Linux hỏng vẫn apt-get rồi cargo. Mutant probe hai lần chết đúng assertion nhật ký. |
| F6 `tool-resolver-prefers-shell-shim` | **VÁ SINH LỖI MỚI**, lớp còn P2 | Shim+x.CMD và cwd chen vào đã chữa; control mới qua, hai mutant đảo lại bị bắt. Nhưng native resolver còn mất công cụ khi PATHEXT rỗng; mất fallback nối PATHEXT cho tên có đuôi; suffix nhiều đoạn cũng lệch. |

**Bảng lớp:** 6 slug lịch sử, **2 lớp P2 mở**, không đếm F6 thêm lần nữa ở F1. F2 giữ mọi biểu hiện của hai chuẩn chọn/kiểm không tương đương; cách chữa chung là thống nhất chuẩn, kênh output, multiline và biên token. F6 giữ slug cũ, nối rõ từ biểu hiện shim sang cơ chế resolver thay `which` chưa đầy đủ. F3 không còn P3 mở. Các chốt sống sót dưới đây là giới hạn độ phủ, không tự coi survival là lỗi sản phẩm mới.

## BẢNG SĂN

Tự đo trên Linux/Python3.13.16. Base/head dựng **cùng vòng lệnh**: `git clone --no-hardlinks --no-checkout`, `core.abbrev=7`, `core.autocrlf=false`, detached SHA tường minh, origin URL repo thật nhưng không dùng mạng. Không dùng worktree. Mọi phép Python chạy sản phẩm/test đặt `PYTHONDONTWRITEBYTECODE=1`; TMPDIR trong `review-data/tmp`; Ruff `--no-cache`.

| Hướng / lệnh hoặc hiện vật | Output thật | Kết luận |
|---|---|---|
| `python review-data/setup.py` | HEAD/spec/diff/write set khớp; **6 tệp/473 thêm/22 xóa** | Khớp lời khai; áp quyết định vượt trần trong assignment |
| `python review-data/probe_installer.py`: phản chứng cũ F2 | rc1/rỗng/ba token rác ở Links + choco tốt ⇒0/DAT/choco; stderr-only ⇒0/DAT/Links | Biểu hiện cũ đã chữa |
| Cùng script: header stdout hoặc warning stderr trước version stdout | Checker0/DAT; head bỏ Links. Choco tốt ⇒ chọn bản sau; choco hỏng ⇒ installer1. Checker-fix ⇒0/DAT/Links | **F2 còn mở** |
| Cùng script: warning stderr, A/B YAML lượt3/head | `a0de1f9`:0/DAT/Links; head:1; bản thử:0/DAT/Links | Hồi quy do bản vá `2>&1` |
| Cùng script: biên phiên bản | Prerelease `-rc.1` và build `+build.1` đạt. Dấu phẩy sau token: checker DAT nhưng chooser loại | Hai chuẩn vẫn lệch, cùng F2 |
| `python review-data/probe_resolver.py`: shim+CMD/cwd | Native chọn x.CMD đúng PATH; Bash chọn shim. Which cũ có thể chèn cwd | Biểu hiện gốc F6 và mục đích bỏ cwd đã chữa |
| Cùng script: PATHEXT rỗng | Which tìm codex.EXE, head không có ứng viên. Doctor qua resolver mô phỏng: base0/co=true → head12/co=false/thiếu codex | **F6 P2**, ảnh hưởng công cụ ngoài rg/git |
| Cùng script: tên có đuôi/PATHEXT nhiều đoạn | `x.CMD` với chỉ `x.CMD.EXE`: which có/headNone. `x.a.b`, PATHEXT=.a.b: which có/headNone. Sửa thử tìm được | F6 chưa đóng; fallback tên có đuôi bị bản vá mới cắt |
| Cùng script: hoa/thường, relative/space/quoted PATH | Lower/upper PATHEXT khớp trên FS facade không phân biệt hoa thường. Relative/space cùng executable; quoted PATH cả haiNone | Không có hồi quy các đối chứng này; quoted PATH là giới hạn chung |
| Cùng script: POSIX thật |7 đối chứng tên có đuôi, relative PATH, nonexec, symlink tốt/dangling cùng executable sau chuẩn hóa absolute | Không phát hiện hồi quy POSIX trong phạm vi đo |
| `python review-data/probe_behavior.py`: tên trần |9 bố cục PATH/symlink/permission cho bare và doctor nhất quán | F1 gốc được kiểm độc lập |
| Cùng script: hook |9 tổ hợp Windows giả lập không installer; flaky1probe. Linux có apt-get,cargo | F5 đóng trong phạm vi mô phỏng Bash |
| `python review-data/audit_mutations.py` |18/20 wp802 đo POSIX:21 assertion đúng ca,0 ngoại lệ vô can.2 Windows-only mô phỏng thêm: controlPASS, mỗi mutant assertion đỏ | Kill mới có căn cứ; native khai riêng |
| Cùng script: F3 / lỗi vô can | Hai restore riêng đều bị bắt. Tiêm AttributeError: runner `[1,0]`, `SAI giet 0/1` | F3 đóng; runner hook/YAML không nhận kill giả này |
| `python review-data/run_survivors.py` | Bỏ stderr/init/guard: mỗi bản212/224,tổng234/10skip/12đỏ,rc1; không thêm/mất ca đỏ so control | Ba chốt chưa được suite canh trên precondition cần thiết |
| `python review-data/run_suites.py` | Full/auth: head212/224,base201/213,cùng12đỏ/10skip. Mutation head268/268,base250/250 | DELTA lỗi0; N/N không tái lập do rig |
| `python review-data/run_gates.py`; contract trong probe_behavior | Ruff5F841/5F841,delta0; contract3/errors[]; bash_nenDAT; doctrine10tệp/0; bash-n0; WORKERverifyok=true | Đạt local theo scope; không nhận lint sạch hoặc pinCI đã chạy |

### Đột biến từng chốt và tín dụng

| Chốt / mutant bản sao | Kết quả và ý nghĩa |
|---|---|
| `kieu_bash=False` → mặc định True | Ca F6 mô phỏng Windows chết đúng TinHieuChotCa vì chọn shim. Linux tương đương, runner khai không đo. Log Windows cấp báo1/1. |
| Resolver → `shutil.which` | Ca F6 mô phỏng chết vì cwd chen vào; log Windows báo1/1. Kill này không chứng nhận mọi biên PATHEXT. |
| Gỡ nhánh PATHEXT | Ca F6 mô phỏng chết vì mất x.CMD; control qua. Ca hiện không chứa PATHEXT rỗng hoặc suffix nối thêm. Không nhận mô phỏng là Windows native. |
| Nới `[[ =~ ]]` thành prefix/mọi rc0 | Ca installer chết đúng assertion DAT/thư mục; tokenjunk mới cho răng thật về grammar/token, khác survival lượt3. |
| `2>&1` → bỏ stderr | Qua toàn suite, không thêm đỏ. Phản chứng stderr-only + không bản tốt khác: control0/DAT → mutant1. Chốt có tác dụng, stock chưa canh kênh stderr. |
| Bỏ `RG_DICH=` | Qua toàn suite. Có RG_DICH thừa kế trỏ seed hợp lệ, mọi ứng viên thất bại: control1 → mutant0/DAT/seed. Stock chưa canh precondition này. |
| Bỏ `${RG_DICH:?…}` | Qua toàn suite. Không ứng viên: công thức trực tiếp control1 → mutant0/inrỗng; wrapper vẫn2/DO nhờ checker cuối. Không báo head đang xanh giả. |
| Bỏ riêng restore hook / YAML | Mỗi mutant chết đúng ca F3 bằng TinHieuChotCa; controlPASS. Đã đóng nợ test YAML lượt3. |
|20 wp802 đã khai |18 mutant POSIX có21 assertion đích,0 lỗi vô can;2 Windows-only có mô phỏng riêng và log executor tương ứng. Không có tín dụng exception giả trong tập mới đã audit. |
| Runner cũ | Cả base/head cùng14 dòng nhận kill bằng4 AssertionError trần +10 ngoại lệ kiểu,0 dòngwp802. Đây là tín dụng giả/nợ nền,delta0; headline268/268 không chứng nhận mọi kill thật. |

Các lỗi dựng probe ban đầu đã sửa và chạy lại; xem `review-data/measurement-notes.md`. Không tính lỗi parse YAML, FunctionType hoặc compile nhầm shell thành finding/kill. Chỉ JSON/log cuối của script chạy thành công được dùng kết luận.

## BẢNG ĐO

| Khẳng định / tiêu chí | Tự đo / dữ liệu cấp | Đánh giá và giới hạn |
|---|---|---|
| Exact SHA/spec/diff | Git/hash khớp đầy đủ, preflight.json | Đạt neo offline |
| ADR-0053 / write set | launcher63/7,test366/11,hook13/3,changelog9/0,yaml7/1,handoff15/0 = **473/22,6tệp** | Vượt450 đúng lời khai. Áp quyết định “Chọn a” tại https://github.com/ducthangho/tra-luat/issues/802#issuecomment-6246303988 theo assignment; không lập finding vì vượt trần, không tự xác minh server. |
|11 ca /20 mutant mới |234−223=11;274−254=20 =11launcher+7hook/YAML+2harness | Khớp handoff; Linux6khôngđo =4nền+2Windows-only |
| N1–N4 | Ca stock + doctor/Bash độc lập; t106 giữ fallback/thứ tự, đổi expected theo Q2 | Đạt fixture; không thay kết luận F6 |
| N6 | Ba prefix Windows/Linux/hook khớp; mutant một bên đỏ; PyYAML có mặt | Đạt parity chuỗi, không chứng minh chooser |
| N7/N8 | Hook Bash thật, installer giả có nhật ký,3 uname; Linux vẫn cargo | Đạt mô phỏng POSIX |
| N10 Linux không auth | Head212/224,total234,skip10,đỏ12; base201/213,total223,skip10,đỏ12; rc1/rc1 | N/N **KHÔNG ĐO ĐƯỢC trong rig này**, DELTA đỏ0 |
| N10 auth giả | `CODEX_AUTH_JSON='{"tokens":{"x":"gia"}}'`: cùng số và cùng12cađỏ | DELTA0. Suite pop biến đầu tệp; không suy skip venv/pip do auth. |
| Nguyên nhân12đỏ | Guard báo `Codex home is inside a repository`; `/tmp/.git` ở cả hai vế; suite-summary.json đối chiếu tên | Lỗi hạ tầng, không phải12 hồi quy PR; không nới guard/xóa marker để làm xanh |
| Mutation Linux | Head268/268,6khôngđo; base250/250,4khôngđo; rc0/rc0 | Khớp headline executor; audit mới và14 tín dụng nền phân riêng |
| N11 Ruff bare |0.17.1,`check --no-cache --select F`,2tệp:5F841 mỗi cây,rc1/rc1 | Đạt DELTA0; **lint không sạch**, chưa thực thi binary pinCI0.15.15 |
| Ruff install/probe contract | `loi_ruff_ci()` đọc chính YAML:3checks/errors[] mỗi cây | Chỉ hợp đồng cấu trúc, không thay bare lint |
| N11 còn lại | bash_nenDAT; doctrine10tệp/0; bash-nrc0 cả hai cây | Đạt local |
| N12 WORKER tương đương local | Strictverifyok=true,head188/188,base187/187; manifest ngoài checkout, tất cả tracked | Đạt local; check-run PR exacthead **KHÔNG ĐO ĐƯỢC** |
| Lease/ref/budget live | Blobf6159dc4 khớp spec/write set,3attempt/4calls; assignment ghi lượt4/4 | Metadata lịch sử; không lấy used0 trong lease để reset. Live lease/ref/check authority **KHÔNG ĐO ĐƯỢC** |

### Evidence Windows và CI được cấp

Reviewer **KHÔNG ĐO ĐƯỢC trực tiếp Windows native/CI** và không gọi GitHub xác minh run/attempt/check-run provenance. Các dòng dưới là đánh giá file log, không phải tự chạy. Không dùng thiếu CI làm lý do riêng giữ changes_requested.

| Evidence | Đọc được gì | Giới hạn |
|---|---|---|
| `EVIDENCE_windows_39101166158_abc16de.log:103,126` | Checkoutfullabc16de; Python3.13.16. Git tự đo: code cùng reviewedhead, khác handoff | Có giá trị cho code; **không là CI exact3d65c954** theo M-3 |
| Cùng log:217–238,308–333 | Installer rgDAT15.2.0; bước sau vẫnDAT | N9 có bằng chứng dương trênabc16de; stdout installer bị capture nên không xác định chắc vế winget/choco |
| Cùng log:452,466–475 |201/201,total234,skip33,hỏng0; N1 không có trong skip; hai mutant resolver1/1 | Bằng chứng mạnh N1 qua, nhưng **thiếu dòng qua riêng cho control N1** như literalN5. Dòng mutation không thay control; không chứng minh WindowsApps thật. |
| Cùng log:748–765 |6hook/YAMLkhôngđo;2harness1/1;195/195mutation,79khôngđo | Khớp phân nền; không chứng nhận6mutant shellPOSIX đã đo Windows |
| `EVIDENCE_windows_N9_DO_39101164840_9b45585.log:103,135,191–220` | Checkout9b45585; shellcheckDAT rồi bước cài công cụ lỗi1 trước suite | Git tự đo9b45585 khácabc16de chỉ1dòng rg.cai.windows, cố ý làm hỏng hai installer. Cặp đỏ/xanh hỗ trợ **N9 có răng**, không là A/B native reviewer tự chạy. |
| `EVIDENCE_gate_ops_windows_a0de1f9.log:3103–3126` | t217 thiếu blob chếtPermissionError WinError5 khi xóa objectGit;251/252,skip13,rc1 | Không phải CI xanh. lease_publish.py/test giống byte base/head; không thấy deltaPR liên quan. Lời khai “y hệt master” chưa được log này chứng minh trên SHA master. |
| Cùng log:1420,2714–2758 | Có nhãn[A]/[B], cùng251/252 và cùngt217đỏ | Đây là con của `t125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor`, **không phải** A/B master/head; không dùng nhãnA/B để xác nhận baseline. |

`ci.yml` xanh trên exact reviewedhead, release-verify check-run và M-3 hiện thời vẫn **KHÔNG ĐO ĐƯỢC** từ bundle. WindowsApps thật, macOS và việc CLI dùng rg nội bộ hay PATH vẫn chưa đo theo SPEC. Không biến khoảng trống này thành finding mã mới.

### installer-selects-broken-path [P2] F2 — Hai chuẩn xác thực còn lệch; thu stderr gây hồi quy

**TỆP/DÒNG:** `ops/cong_cu.yaml:93`, đối chiếu probe `:83` và `ops/cong_cu.py:160,184`. Cùng lớp F2 lượt1–3.

**VẤN ĐỀ:** Chooser chỉ neo đầu toàn output, buộc whitespace/end sau token; checker dùng regex multiline và tập ký tự biên riêng. Links in thông báo rồi `ripgrep 15.2.0`: checker trực tiếp0/DAT nhưng chooser bỏ. Choco tốt thì chọn bản sau dù Links hợp lệ; choco hỏng + PATH cũ hỏng thì installer1 dù có bản hợp lệ. Với warning **stderr trước version stdout**, `2>&1` mới còn sinh hồi quy: YAML lượt3 thành công0/DAT/Links, head thất bại1. Dấu phẩy sau phiên bản là biểu hiện khác của cùng cơ chế.

**ĐÃ THỬ VÁ:** Chỉ YAML tạm. Thử multiline riêng sửa được header/warning; sau đó dùng **chính checker chuẩn** quyết định ứng viên. Headerstdout, warningstderr và token có dấu câu đều0/DAT/Links, trong khi head1 khi không bản tốt khác. Đây là thử hướng sửa, không patch ghi branch, chưa chạy gate đầy đủ trên cây sửa executor.

**ĐÃ THỬ NGHIỆM:** `PYTHONDONTWRITEBYTECODE=1 python review-data/probe_installer.py`, `installer-results.json`: nguyên `cai_cong_cu.sh` bằng Bash thật, installer/cygpath/rg là fixture. Có đối chứng token rác/rỗng/rc1/stderr-only và prerelease/build. `audit_mutations.py` chứng minh grammar có răng; `run_survivors.py` chứng minh bỏ thu stderr qua toàn suite không thêm đỏ. Không dùng kill grammar để nhận đã canh kênh output.

**ĐỘ TIN:** Cao về Bash/chooser và A/B hồi quy; không nhận đã cài Windows native. Owner executor wp802. Cần thống nhất chuẩn tương đương checker cuối, cùng multiline/kênh/biên token, rồi khóa bản chọn/DAT/GITHUB_PATH và không ứng viên. **Chưa đóng P2.**

### tool-resolver-prefers-shell-shim [P2] F6 — Resolver native làm mất công cụ hợp lệ ngoài rg/git

**TỆP/DÒNG:** `.claude/dev/launcher.py:2286,2311–2313`; ca mới `.claude/dev/launcher_test.py:8134`. Giữ lớp F6 lượt3: resolver thay `which` cho mọi công cụ.

**VẤN ĐỀ:** `get(PATHEXT, default)` không fallback khi giá trị rỗng; native mode có danh sách đuôi rỗng và bỏ `.EXE` mà CPython3.13 `shutil.which` vẫn tìm bằng default. Chỉ codex.EXE trong PATH: doctor qua resolver Windows mô phỏng + probe thành công có kiểm soát đổi base0/co=true → head12/co=false/thiếu codex. Đây là hồi quy công cụ ngoài BI_CHE.

Native mode mới còn cắt nhánh nối thêm PATHEXT khi tên đã có đuôi được nhận diện: `x.CMD` với chỉ `x.CMD.EXE` được which tìm nhưng headNone. Suffix nhiều đoạn `.a.b` bị splitext nhận sai với `x.a.b`. Cùng cơ chế triển khai lại resolver, không tách finding để tăng đếm. Tên ứng viên hiện tại thường trần; **PATHEXT rỗng đã tác động CONG_CU hiện tại**.

**ĐÃ THỬ VÁ:** Chỉ hàm nguồn tạm: fallback PATHEXT rỗng, giữ tên trực tiếp ưu tiên rồi vẫn thử các đuôi, nhận suffix đầy đủ. Ba đối chứng tìm lại được; shim+x.CMD và không chèn cwd vẫn đúng. Không tuyên bố bản thử tương đương which trên mọi phiên Python/Windows hoặc đã qua CI.

**ĐÃ THỬ NGHIỆM:** `PYTHONDONTWRITEBYTECODE=1 python review-data/probe_resolver.py`, `resolver-results.json`: chạy **nguyên nguồn CPython3.13.16 shutil.which đang cài** và helper product với filesystem facade Windows không phân biệt hoa/thường, cùng PATH/PATHEXT/cwd; doctor thật dùng kết quả resolver và probe seam.12 đối chứng thuật toán (có cwd cũ cố ý khác) và7 POSIX thật. Ca F6 bắt quay lại shim/which và gỡPATHEXT trong mô phỏng, nhưng không chứa ba biên trên. Reviewer native Windows **KHÔNG ĐO ĐƯỢC**; log CI pinPython3.13 củng cố phiên chuẩn đối chiếu, không thay phép thử OS thật.

**ĐỘ TIN:** Cao về sai khác thuật toán/hậu quả doctor; giới hạn Windows native khai rõ. Owner executor wp802. Cần giữ nhận thức cwd của bare shell, bảo toàn tìm ứng viên native cho công cụ khác, khóa biên PATHEXT/suffix riêng. **Chưa đóng P2.**

## TOÀN VẸN VÀ BÀN GIAO

Snapshot đầu/cuối: `cay-kho` **3796/3796 tệp kể cả .git**, `kho.git` **622/622**, khớp byte/mode/symlink, không tệp thay đổi; HEAD/tree/status (gồm ignored/untracked) khớp. `snapshot-comparison.json` đều match=true; băm .git bao gồm index/config/objects. Sandbox thực tế workspace-write; checkout read-only là kỷ luật kiểm ở hai mốc, không tự nhận sandbox cưỡng chế và không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.

Command/rc/log/JSON đúng lượt4 ở `review-data/`: preflight, suite-results/summary, installer-results, resolver-results, behavior-results, mutation-audit, survivors-full-results, gates, snapshot-comparison. `artifact-manifest.json` ghi path/size/SHA-256 sau khi chốt. Không dùng dữ liệu lượt trước thay phép chạy lượt này.

**Quyết định cuối: changes_requested.** F2 và F6 còn P2; F3 đã đóng. Kết thúc lượt4/4, không cấp merge/land hoặc tự mở thêm ngân sách review.
