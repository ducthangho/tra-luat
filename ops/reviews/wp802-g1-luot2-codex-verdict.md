verdict: changes_requested
reviewed_sha: 509dfa850ecb73a3624a777c699fd8a05812cc25

Còn **2 lớp lỗi P2 cần sửa**: F2 chưa đóng hết lớp chọn thư mục `rg` hỏng; bản sửa hook sinh đường chạy installer trên Windows khi probe thay đổi giữa hai lần gọi. Không phát hiện P0/P1 trong phạm vi đã đo. Đây là kết luận từ phản chứng offline, **không** phải vì thiếu CI Windows exact-head.

Reviewer: OpenAI Codex, provider `openai_codex`, execution surface `codex_service` (API agent có shell), transport `machine`. Họ model OpenAI theo phiên hiện tại; model ID/effort/session ID và danh tính executor chưa có runtime receipt độc lập trong bundle: `KHÔNG ĐO ĐƯỢC`. Không suy danh tính model từ actor GitHub; không tự chứng nhận receipt/assurance của điều phối. Ngưỡng áp theo prompt: hết P0/P1 và mọi P2 phải đóng hoặc có quyết định rõ; đề nghị sửa cả hai P2, không có căn cứ miễn chúng.

Đã đọc SPEC, CLAUDE.md, AGENTS.md, protocol §8/§13 và adapter review liên quan. `cay-kho/` được giữ nguyên; phép chạy sản phẩm, test và vá thử dùng clone/scratch trong `review-data/`. Không push, không gọi GitHub; không soạn phản chứng thoát cây. Các hướng sửa launcher/hook/runtime dưới đây là mô tả; không phát patch-as-hint runtime cho packet sensitive. Log executor chỉ dùng đối chiếu, không thay phép đo độc lập.

HEAD/tree = `509dfa850ecb73a3624a777c699fd8a05812cc25` / `a9507c916c54a8aea703fa24440d923d09b27eb9`; nền DELTA = `fb490a7c3fa2992c6f4635ed091dafa813df2fe7` / tree `78cf0bfe8ac4b327ce834800ccf687c6d42f52c9`. Cả hai clone dựng trong cùng vòng lệnh từ `kho.git`: `git clone --no-hardlinks --no-checkout`, config `core.abbrev=7`, `core.autocrlf=false`, checkout detached SHA tường minh. Mọi phép Python chạy test/sản phẩm đặt `PYTHONDONTWRITEBYTECODE=1`; Ruff `--no-cache`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn cả F1–F4: `VERDICT_LUOT1.md`, head `db1ed4dda529eb30806ecb053d2eef9933e188b1`. Giữ slug lớp cũ, không reset theo merge master.

| Finding / lớp | Phân loại | Bằng chứng độc lập / giới hạn |
|---|---|---|
| F1 `bare-path-empty-entry` | **ĐÃ VÁ THẬT phần POSIX đã đo** | `probe_review.py`: PATH `:<good>` cho bare rg rc1, doctor rc12/BI_CHE; `:<bad2>:<good>` giữ đúng `cwd/rg`, không ghi đè thành bad2. Dot, mục rỗng giữa PATH, đường tương đối và symlink hỏng đều đúng. Mutant bỏ mục rỗng / bỏ đặt tên trần lên đầu / ghi mọi bản hỏng đều bị assertion N1/F1/N4 tương ứng giết. Ngữ nghĩa shell Windows native chưa đo, giữ trong M-3; không suy mô phỏng thành đã đóng phần Windows. |
| F2 `installer-selects-broken-path` | **VÁ HỜ ở mức đóng lớp**: phản chứng cũ đã sửa, còn biểu hiện cùng cơ chế | rg rc1 trên PATH cũ + WinGet Links tốt ⇒ `cai_cong_cu.sh` rc0/DAT, đúng Links/GITHUB_PATH. Nhưng Links rc0 rỗng hoặc phiên bản không parse được + choco tốt ⇒ vẫn chọn Links, rc2/DO. Chốt chọn thư mục dùng tiêu chí yếu hơn phép kiểm cuối. Xem F2 bên dưới. |
| F3 `hook-pointer-restore` | **ĐÃ VÁ THẬT hành vi** | Gọi runner với CẢ HAI con trỏ hook/yaml riêng: trả `[0,0]`, khôi phục đúng cả hai. Bỏ riêng từng phép khôi phục trên bản sao ⇒ mất đúng con trỏ đó. Runner stock vẫn `[0,0]` ở hai mutant: còn nợ ca test hậu điều kiện (P3, owner executor wp802), không phải lỗi khôi phục còn tồn tại ở head. |
| F4 `windows-hook-mutation-count` | **ĐÃ VÁ THẬT lời khai** | Giả `LA_WINDOWS=True` chỉ để đo skip: runner `[0,4]`; 2 hook + 2 YAML không đo, mutant chuỗi vẫn N6 giết 1/1. Handoff dòng14 khớp. Không phải chạy Windows thật. |

## BẢNG LỚP

| slug lớp | biểu hiện / IDs | hạng còn mở | nguồn | phương án chung / phép kiểm đóng |
|---|---|---|---|---|
| `bare-path-empty-entry` | F1: empty PATH + chọn đúng bad1 | không còn lỗi POSIX đã đo | lượt1 db1ed4d → lượt2 509dfa8 | Resolver độc lập, đặt trước fallback, giữ danh tính bare; native Windows M-3 riêng. |
| `installer-selects-broken-path` | F2 cũ rc1 PATH (đã sửa); F2.2 rc0 rỗng; F2.3 output sai phiên bản | **P2** | lượt1 db1ed4d, còn ở lượt2 509dfa8 | Một tiêu chí chọn ứng viên tương đương kiểm cuối; test rc1/rỗng/sai phiên bản và fallback Links/choco/command-v, GITHUB_PATH đúng. Hai biểu hiện mới chung nguyên nhân nên chỉ một finding/lớp. |
| `hook-pointer-restore` | F3 hook; mở rộng yaml ở lượt2 | P3 nợ test, hành vi đã sửa | lượt1 db1ed4d → lượt2 509dfa8 | Owner executor wp802; thêm ca gọi runner với con trỏ tùy biến, assert trả lại cả hai, gỡ từng restore phải đỏ. |
| `windows-hook-mutation-count` | F4 số skip | đóng lời khai | lượt1 db1ed4d → lượt2 509dfa8 | Handoff 4 không đo / 1 còn đo, khớp nhánh skip; native là M-3. |
| `windows-hook-installer-fallthrough` | F5: Windows probe qua rồi lỗi ⇒ POSIX installer | **P2** | mới lượt2 509dfa8 | Tách nhánh theo OS trước probe; chỉ probe một lần cho Windows. Test stable/broken/flaky, nhật ký không installer trên mọi nhận diện Windows. |

Đếm riêng: **2 lớp P2 mở / 3 biểu hiện sản phẩm mở** (F2.2, F2.3, F5); F3 còn một nợ test P3 với owner và hướng xử lý nêu trên. Không đổi slug F2 để giấu tái diễn. Windows/CI chưa đo không được tính là lỗi code mới.

## BẢNG SĂN

Các lệnh từ thư mục review, trừ suite/gate có cwd `review-data/{base,head}`. `python review-data/probe_review.py` chạy resolver, installer và mutant; `probe_boundaries.py` kiểm biên + A/B vá thử + runner. Output đầy đủ trong các log/JSON cùng thư mục.

| HƯỚNG | giả thuyết / lệnh | output thật rút gọn | kết luận |
|---|---|---|---|
| 1 | Neo sai SHA/spec/diff; `git rev-parse`, `merge-base`, `sha256sum`, so bytes diff/numstat (`preflight.json`) | Head/tree đúng; spec e4fd84e1…00e0; diff.patch/numstat byte-match; merge-base fb490a7; master drift không chạm write set | KHÔNG PHẢI LỖI |
| 2 | F1 còn xanh với PATH rỗng; `probe_review.py` / resolution | Bare rc1; doctor rc12; bad1→bad2→good nêu đúng bad1; only-good rc0 không BI_CHE | KHÔNG PHẢI LỖI POSIX |
| 3 | Symlink/tương đối làm sai danh tính; cùng script | Symlink hỏng + tốt ⇒ BI_CHE/rc12, `ban_hong` giữ đường symlink; PATH tương đối đúng; thêm good-link/dangling-link đều bare/doctor rc0 đúng | KHÔNG PHẢI LỖI ở fixture đã đo |
| 4 | Normcase/abspath bỏ ứng viên hoặc đo trùng; `normalization.log` | Head PATH tương đối probe `[abs bad, relative good]`; bỏ abspath thành `[abs bad, relative bad, relative good]`; gỡ toàn dedup bị t106 giết. Gỡ riêng abspath qua 10 ca thành phần | Hành vi head đạt; thiếu ca canh riêng abspath. Normcase/case Windows: KHÔNG ĐO ĐƯỢC native |
| 5 | Windows đuôi rỗng/PATHEXT/thứ tự/os.access; thuật toán mô phỏng trong probe + `windows-algorithm-mutations.log` | Có tên không đuôi ⇒ chọn nó trước PATHEXT; bỏ nó ⇒ theo thứ tự PATHEXT. NT path giả: head first/rg.EXE, đảo PATHEXT first/rg.COM, đảo PATH last/rg.EXE, bỏ PATHEXT None | KHÔNG ĐO ĐƯỢC tương đương Git Bash/CreateProcess/ACL thực; chỉ đo thuật toán, không nhận là test Windows |
| 6 | F2 chọn lại bản PATH hỏng; installer Bash thật/stub | Old PATH rc1, Links tốt ⇒ rc0/DAT15.2.0; choco fallback ⇒ DAT; command-v cuối ⇒ DAT | Phản chứng cũ KHÔNG CÒN LỖI |
| 7 | `for…done &&…`/eval dưới `set -euo pipefail` xanh rỗng khi không chọn; cùng script | Không ứng viên chạy ⇒ direct rc1/stdout rỗng, nguyên cai_cong_cu rc1; cả hai installer lỗi ⇒ rc1 | KHÔNG PHẢI LỖI; không có rỗng xanh giả ở các nhánh này |
| 8 | `${ChocolateyInstall:-…}`/GITHUB_PATH lỗi; cùng script | Set/rỗng/vắng ChocolateyInstall đều chọn fallback fixture đúng; GITHUB_PATH vắng vẫn rc0; có biến ghi đúng thư mục. Mutant bỏ ghi bị N6/F2 test giết | KHÔNG PHẢI LỖI trong mô phỏng POSIX; chuyển đổi native chưa đo |
| 9 | Chốt chọn thư mục chỉ tin rc0; `probe_boundaries.py` / silent-candidate | Links rỗng hoặc sai phiên bản, choco tốt ⇒ head rc2/DO, ghi Links; scratch sửa dùng probe kiểm cuối ⇒ rc0/DAT15.2.0, ghi choco. Đối chứng rc1 Links: cả hai DAT | **LỖI P2 F2** |
| 10 | Hook Windows probe hai lần và rơi POSIX; cùng script / hook-double-probe | Round1 cùng flaky chỉ RG1. Head stable: RG1,RG2. Lần đầu qua rồi lỗi: RG1,RG2,apt-get,RG3,cargo,RG4; rc0. Scratch tách nhánh OS: chỉ RG1, không installer | **LỖI P2 F5** |
| 11 | F3 restore vẫn sai; cùng script / pointer | Control `[0,0]`, hook/yaml restored true/true; gỡ restore lần lượt false/true và true/false nhưng runner vẫn `[0,0]` | Head KHÔNG CÒN LỖI chức năng; có nợ coverage P3 |
| 12 | F4 vẫn khai sai skip hoặc runner nhận tín dụng giả; cùng script | Giả Windows `[0,4]`, chuỗi giết1/1; tiêm AttributeError vào hook mutant ⇒ `[1,0]`, SAI giet0/1 | KHÔNG PHẢI LỖI tại 5 mutant hook/YAML |
| 13 | Chốt mới không có răng; audit mutant bản sao | 14 wp802 mutant có đúng assertion ca đích, không lỗi vô can; các chốt còn hở và một kill chỉ do `dirname` được phân tích trong ma trận dưới | Coverage chưa đóng toàn bộ lớp F2/F5 |
| 14 | Suite hồi quy; `python .claude/dev/launcher_test.py` cả hai clone | Head210/222, base201/213, mỗi cây12đỏ/10skip; tập đỏ trùng nhau | DELTA đỏ0; N/N KHÔNG ĐO ĐƯỢC do rig |
| 15 | Auth giả gây hồi quy; cùng suite với CODEX_AUTH_JSON giả | Head218/230, base209/221; mỗi cây12đỏ/2skip; tập đỏ trùng full và nhau | DELTA đỏ0; không tái lập N/N do rig |
| 16 | `--dot-bien` headline khác khai | Head264/264, base250/250; mỗi cây rc0, 4 không đo. Có14 dòng tín dụng ngoại lệ kế thừa giống nhau, không dòng wp802 | Khớp headline; không đồng nhất với toàn bộ kill thật |
| 17 | Khắc phục rig bằng TMPDIR riêng; `tmpdir-probe.json`, CẢ HAI vế | Base/head cùng `Codex home is inside a repository`; private TMPDIR vẫn dưới `.git` workspace và `/tmp/.git` | KHÔNG ĐO ĐƯỢC TMPDIR ngoài repo theo guard trong phạm vi ghi được; không bypass guard |
| 18 | Ruff/static/release | Bare Ruff0.17.1: head/base5F841 rc1, DELTA0; Ruff contract3/3 không lỗi mỗi bên; bash_nen DAT, doctrine10 tệp/0 chỗ, bash-n rc0; WORKER verify ok=true188/188,188 tracked | KHÔNG PHẢI LỖI local; không chứng nhận CI/pin đã cài |
| 19 | Log Windows cũ được dùng như exact-head | Log checkout db1ed4d; install rg DAT15.2.0 rồi bước sau KHONG_DO_DUOC/rc1 | KHÔNG ĐO ĐƯỢC N5/N9/N10 Windows/N12 CI tại509dfa8. Log cũ không thay M-3 |

## BẢNG ĐO

| khẳng định | khai | đo được | khớp? |
|---|---|---|---|
| Exact head | 509dfa850ecb73a3624a777c699fd8a05812cc25 | đúng OID; tree a9507c…eb9 | có |
| Nền DELTA | fb490a7c3fa2992c6f4635ed091dafa813df2fe7 | merge-base mirror master/head đúng; drift từ de82ef74 không chạm 6 tệp | có |
| SPEC | SHA-256 e4fd84e1…00e0 | đúng đầy đủ e4fd84e1f079d0ac4841a145d078473576af3a3e4e2f593e4f3e40c5de7200e0 | có |
| ADR-0053 | 6 tệp / ≤450 thêm | 6 / **442 thêm,20 xóa** | có, còn8 dòng so trần; không viện Q9 để vượt |
| Write set | 6 đường dẫn SPEC | đúng6: launcher.py61/5, launcher_test.py338/11, hook13/3, changelog9/0, yaml7/1, handoff14/0 | có |
| F1 resolver bare | PATH theo thứ tự, mục rỗng=cwd; đo bare trước | POSIX đạt các phản chứng; Windows chỉ mô phỏng thuật toán | có ở POSIX; native chưa đo |
| F2 chooser | thư mục đầu có rg chạy được, không có ⇒ khác0 | rc1 được bỏ qua; rc0 rỗng/không parse lại bị chọn dù có ứng viên DAT | **không**, F2 |
| Hook Windows | không installer | Windows nhận diện, probe lần1qua/lần2lỗi ⇒ apt-get/cargo | **không**, F5 |
| 9 ca r802 | 9 mới, N1–N8 + phản chứng F1/F2 | đúng9; control9/9, thêm t106 thành10/10 | có với fixture hiện tại |
| 14 wp802 mutant | 9 launcher +5 hook/YAML | đúng14; audit giết đúng ca; không có UNRELATED_EXCEPTION ở tập này | có cho14 đã khai; chưa chứng minh mọi chốt |
| Khôi phục con trỏ | trả đúng hook/yaml người gọi | true/true; gỡ mỗi restore không có ca stock canh | hành vi có; coverage thiếu |
| Skip Windows của DOT_BIEN_HOOK | 4 không đo,1 còn N6 | logic skip mô phỏng đúng `[0,4]`, chuỗi1/1 | có; không phải Windows thật |
| Suite thường | executor230/230,tổng232/skip2 | head210/222,tổng232/skip10/đỏ12; base201/213,tổng223/skip10/đỏ12 | không tái lập N/N; DELTA0 |
| Suite auth giả | executor230/230 | head218/230,tổng232/skip2/đỏ12; base209/221,tổng223/skip2/đỏ12; rc1/rc1 | không tái lập N/N; DELTA0 |
| Mutation headline | executor264/264,4 không đo | head264/264, base250/250; rc0/rc0, mỗi cây4 không đo | có về headline;14 mutant mới audit riêng |
| Ruff bare lint | DELTA F0 | 5F841/5F841, mỗi bênrc1, Ruff0.17.1 | có DELTA0; không phải lint sạch |
| Ruff pin/probe contract | workflow cài/probe theo contract | `loi_ruff_ci`: count3/errors[] cả hai | có về contract; chưa thực thi Ruff CI pin |
| bash_nen / doctrine / hook syntax | DAT / rc0 / bash-n | DAT /10 tệp,0 chỗ /rc0 ở cả hai cây | có |
| WORKER release local | N12 jobCI | manifest/verifyrc0,ok=true188/188;188 tracked,0 extra | local có; CI KHÔNG ĐO ĐƯỢC |
| Windows/CI exact-head | điều phối đo riêng M-3 | bundle chỉ có Windows db1ed4d; không truy cập GitHub | KHÔNG ĐO ĐƯỢC, không dùng để chặn verdict nếu code hết lỗi |
| Lease/ref/usage hiện thời | lease f6159dc4,596↔596 lịch sử,3attempt/4calls | metadata giới hạn từ SPEC/handoff; chưa có server/usage receipt độc lập | KHÔNG ĐO ĐƯỢC live authority/usage; không suy từ số ref mirror |

### installer-selects-broken-path [P2] F2 — Chọn ứng viên rc0 nhưng phiên bản hỏng, bỏ qua bản tốt phía sau

**TỆP/DÒNG:** `ops/cong_cu.yaml:93`; hợp đồng tiêu thụ tại `ops/cai_cong_cu.sh:72` và kiểm cuối ở `ops/cong_cu.py:184`. Cùng lớp F2 lượt1, không đổi slug.

**VẤN ĐỀ:** Vòng mới chỉ nhìn mã thoát `rg --version`, bỏ toàn bộ output. Fixture có WinGet Links chứa wrapper rc0 nhưng in rỗng hoặc `invalid-version`; choco/bin chứa `ripgrep 15.2.0`. Winget giả lỗi, choco giả thành công. Vòng chọn vẫn nhận Links, ghi thư mục này vào GITHUB_PATH rồi phép kiểm cuối trả rc2/DO vì không parse phiên bản. Công cụ tốt phía sau không được thử. Phản chứng rc1 cũ đã sửa đúng, nhưng tiêu chí chọn ứng viên vẫn yếu hơn chính tiêu chí DAT cần đạt; do đó F2 chưa đóng lớp.

**ĐÃ THỬ VÁ:** Có, chỉ trên YAML tạm trong scratch. Thử dùng chính phép kiểm `cong_cu.py kiem-tra --chi rg` với PATH ứng viên đứng trước khi chọn; không ghi GITHUB_PATH cho ứng viên chưa DAT. Cả rỗng và phiên bản sai đổi rc2/DO→rc0/DAT15.2.0, đúng choco/bin. Đây là thử hướng sửa, chưa chạy gate đầy đủ trên cây executor, không phải patch được cấp để chép mù.

**ĐÃ THỬ NGHIỆM:** `PYTHONDONTWRITEBYTECODE=1 python review-data/probe_boundaries.py`, mục `silent-candidate` trong `boundary-results.json`: head `usable_selected=false` cho2 biểu hiện, scratch-fix true; đối chứng Links rc1 thì cả hai true. Script chạy nguyên `cai_cong_cu.sh` bằng Bash với `set -euo pipefail`/eval thật. Chỉ winget/choco/cygpath là giả, không chạy installer thật hay mạng. Stock mutant thay phép thử phiên bản bằng `true` vẫn qua9 r802+t106: chốt probe mới chưa được canh về hành vi.

**CÁCH KHÓA / TƯƠNG TÁC:** Executor tự thiết kế sửa tại chooser, dùng một tiêu chí phù hợp probe cuối để tránh tái tạo hai chuẩn. Thêm ca Links rc1/rỗng/output không parse và choco hoặc PATH cuối có bản DAT; assert bản được chọn, DAT cuối và GITHUB_PATH. Gỡ phép validate ứng viên phải làm chính ca đỏ. Kiểm trường hợp không ứng viên đạt vẫn khác0, không rỗng xanh; giữ cờ phi tương tác và prefix ba bảng. Nếu dùng checker chung phải giữ timeout/trạng thái chưa đo, tránh thêm phụ thuộc mới ngoài write set. Không cần đổi6 tệp phạm vi.

**ĐỘ TIN:** Cao về hợp đồng Bash/chooser và hậu quả DO; không suy thành đã đo installer Windows native. Đề nghị **SỬA**, chưa miễn P2.

### windows-hook-installer-fallthrough [P2] F5 — Nhánh Windows có thể chạy installer POSIX sau probe thứ hai

**TỆP/DÒNG:** `.claude/hooks/session-start.sh:192` (điều kiện `elif`); xuất phát từ cấu trúc mới tại189.

**VẤN ĐỀ:** Khi RG_WIN=1 và probe đầu thành công, điều kiện189 sai nên shell kiểm `elif ! co_chay rg` lần hai. Nếu lần hai lỗi/timeout, hook đi vào đường apt-get/sudo/cargo dù đã nhận diện Windows. Q4/N8 cấm hook tự cài trên Windows. Ngay cả công cụ ổn định cũng bị probe hai lần, tạo cửa trạng thái thay đổi không cần thiết; finding là đường installer bị mở, không chỉ chi phí probe.

**ĐÃ THỬ VÁ:** Có, trên bản sao khối hook, giới hạn nhánh POSIX theo OS trước khi probe. Với cùng rg giả lần1qua/lần2lỗi, bản thử chỉ gọi RG1, không installer; Linux vẫn có đường cargo khi rg hỏng qua control stock. Executor nên tự tách quyết định OS trước probe để Windows chỉ đo một lần và chỉ in hướng dẫn khi thiếu/hỏng.

**ĐÃ THỬ NGHIỆM:** Cùng lệnh `probe_boundaries.py`, mục `hook-double-probe`: `uname` giả MINGW64_NT-10.0, chạy nguyên hàm co/co_chay và khối rg lấy từ hook bằng Bash thật. Round1 cùng fixture flaky: `[RG1]`, không installer. Head stable: `[RG1,RG2]`; head flaky: `[RG1,RG2,apt-get install -y -qq ripgrep,RG3,cargo install ripgrep,RG4]`, rc0, `no_installer=false`. Scratch-fix: `[RG1]`, rc0, `no_installer=true`. Installer chỉ là stub ghi nhật ký. Không cần Windows native để chứng minh cấu trúc rẽ nhánh shell này.

**CÁCH KHÓA / TƯƠNG TÁC:** Thêm đối chứng Windows rg tốt, hỏng từ đầu, và probe thay đổi; tất cả không được có installer trong nhật ký. Assert đúng số probe Windows (một), giữ cảnh báo/lệnh in khớp YAML khi thiếu, giữ test Linux apt/cargo. Mutant bỏ gate OS của nhánh POSIX phải làm ca flaky đỏ. Thiếu uname hiện rơi POSIX là hành vi kế thừa, không nhận là đã đo an toàn Windows khi thiếu uname.

**ĐỘ TIN:** Cao, hồi quy do bản sửa lượt2. Đề nghị **SỬA**, chưa miễn P2.

## ĐỘT BIẾN VÀ GIỚI HẠN ĐỘ PHỦ

Audit chạy trên **bản sao tạm**, mỗi mutant nạp source mới; phân biệt `TinHieuChotCa` với exception vô can. Control9 r802+t106 đều PASS. Không dùng headline mutation để tự chứng nhận mọi kill.

| chốt / mutant | bằng chứng / kết luận |
|---|---|
| Tắt BI_CHE; bỏ nó khỏi thiếu | N1/N3/F1/t106 assertion đỏ; giết đúng quyết định |
| Luôn BI_CHE; bỏ git; mở scope tại dòng tran | N2/N3/N4 assertion đỏ; phạm vi hiện chỉ gate tại dòng tran, đúng cách thiết kế mới |
| Bỏ empty PATH; không đưa bare lên đầu; hong_dau cho mọi lỗi | F1 assertion đỏ; mutant cuối nêu nhầm bad2; N4 cũng bắt hong_dau ngoài phạm vi |
| Đảo PATH; bỏ đuôi rỗng | N1/F1 assertion đỏ trên POSIX |
| PATHEXT bị bỏ/đảo | 10 ca thành phần Linux còn xanh; mô phỏng NT phát hiện kết quả đổi. Không kết luận native Windows pass/coverage từ đó; N5 exact-head phải đo riêng |
| Bỏ os.access | 10 ca thành phần còn xanh. Reviewer thêm non-executable: bare/head rc0, mutant rc12/BI_CHE sai; chốt head có tác dụng, stock chưa canh. Không báo lỗi head |
| Gỡ toàn dedup | t106 assertion thứ tự probe đỏ |
| Bỏ riêng abspath | 10 ca còn xanh; độc lập PATH tương đối đo trùng bare trong mutant, head không trùng. Normcase native chưa đo |
| Đổi launcher/hook command prefix | N6/N8 assertion đúng chuỗi, đúng yêu cầu parity |
| Hook co_chay→co; bỏ nhận diện Windows | N7/N8 assertion nhật ký đúng; không dùng lỗi setup để tính kill |
| Bỏ Links; bỏ GITHUB_PATH | Ca installer mới giết bằng rc1/DAT thiếu hoặc pathfile rỗng, đúng chốt |
| Bỏ break | Ca installer mới rc1, assertion DAT đỏ; loop không giữ kết quả thành công |
| Bỏ thư mục choco; bỏ default ChocolateyInstall | 10 ca thành phần vẫn xanh; reviewer có ca choco và biến vắng/rỗng độc lập, stock chưa canh những nhánh này |
| Đổi probe thành true | 10 ca thành phần vẫn xanh; test hiện chỉ có Links tốt nên không đo việc từ chối ứng viên xấu. Liên quan trực tiếp F2 |
| Bỏ candidate command-v thẳng | N6 đỏ vì yêu cầu tail phải có chữ dirname: **không là tín dụng hành vi** cho đường fallback. Mutant giữ dirname nhưng bỏ command-v vẫn10/10xanh; reviewer có đối chứng command-v-last riêng |
| Bỏ từng restore hook/yaml | Runner vẫn `[0,0]`, độc lập thấy pointer sai. Nợ test F3, owner executor wp802 |
| Tiêm AttributeError vào hook mutant | Runner `[1,0]`, SAI0/1, không nhận giết giả |

14 mutant wp802 đã khai đều được audit trực tiếp và chết bằng assertion đúng ca đích; mutant command-v là mutant reviewer thêm để vạch giới hạn phép so cấu trúc, không gán nhầm thành một trong14 của executor. Runner `DOT_BIEN` tổng quát vẫn có nhánh tính AssertionError/Exception vô can là kill: đo lại thấy **14 dòng** ở cả base và head, cùng tên mutant, **0 dòng wp802**; gồm 4 AssertionError trần và 10 ngoại lệ kiểu. Đây là tín dụng giả/nợ nền đã nêu lượt1, lưu riêng trong `legacy-mutation-exception-credits.json`. Không dùng tổng mutation để nói toàn bộ kill đều thật.

## GIỚI HẠN NGHIỆM THU VÀ TOÀN VẸN

- N1–N4/N6–N8: fixture stock đạt, nhưng F2/F5 cho thấy chưa đóng lớp M4/M5/M6. N5, N9, Windows N10 và N12 trên CI exact-head: **KHÔNG ĐO ĐƯỢC** offline; điều phối kiểm M-3 riêng. Log db1ed4d không phải bằng chứng509dfa8. WindowsApps thật/macOS vẫn chưa đo theo SPEC.
- N10 Linux N/N: chưa tái lập vì12 lỗi nền. Đã thử TMPDIR riêng cho **cả hai vế** bằng probe storage, vẫn dưới marker `.git`; không có vị trí ghi được ngoài mọi repo theo guard trong sandbox này. Không xóa marker hay nới guard để đổi kết quả. Những phép đo còn thiếu được giữ là chưa đo, không tính là PASS.
- N11: bare lint DELTA0; bash_nen/doctrine/bash-n đạt. Ruff contract kiểm cấu trúc cài/probe, khác bare lint; không nhận phiên Ruff0.17.1 là đã chạy pin CI0.15.15. N12 tương đương WORKER local đạt188/188.
- Snapshot `cay-kho` đầu/cuối: **3765/3765 tệp byte-match,0 thay đổi**, HEAD/tree/status (gồm ignored/untracked)/diff/index không delta; xem `snapshot-comparison.json`. Sandbox thực tế workspace-write; read-only ở đây là kỷ luật đã kiểm qua snapshot, không tự nhận sandbox cưỡng chế. Snapshot chỉ chứng minh không có delta quan sát tại hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.

## Nhật ký phép đo — đợt 1

Các dòng nhật ký giữ trạng thái tại thời điểm ghi; kết luận/bảng phía trên là bản chốt sau cùng.

- Exact head/tree: `509dfa850ecb73a3624a777c699fd8a05812cc25` / `a9507c916c54a8aea703fa24440d923d09b27eb9`.
- Merge-base đo từ mirror: `fb490a7c3fa2992c6f4635ed091dafa813df2fe7`; SHA-256 SPEC khớp `e4fd84e1f079d0ac4841a145d078473576af3a3e4e2f593e4f3e40c5de7200e0`.
- Dựng CẢ HAI clone bằng cùng vòng Python: `git clone --no-hardlinks --no-checkout`, `core.abbrev=7`, `core.autocrlf=false`, checkout detached SHA tường minh. Không dùng worktree.
- Diff thật: 6 tệp, 442 dòng thêm / 20 dòng xóa. Master drift từ base lease tới merge-base không chạm cả 6 tệp.
- `probe_review.py`: PATH `:<good>`, `:<bad2>:<good>`, `.`, mục rỗng giữa PATH, đường tương đối và symlink tới bản hỏng đều cho rc12, đúng `ban_hong`; only-good rc0, không BI_CHE.
- Installer qua Bash thật, `CONG_CU_NEN=windows` + installer/cygpath giả: WinGet Links/choco/command-v fallback đạt; không ứng viên chạy được ⇒ rc1, stdout rỗng; cả hai installer lỗi ⇒ rc1. `${ChocolateyInstall:-…}` xử lý biến rỗng/vắng đạt. Chưa phải bằng chứng Windows native.
- `/tmp/.git` tồn tại. Bộ suite đang chạy; chưa nhận N/N executor là đã tái lập.
- 14 mutant `wp802_*` trên bản sao đã có assertion đúng ca; đang audit thêm chốt PATHEXT, vòng chọn thư mục và runner.

## Nhật ký phép đo — đợt 2

Hai lỗi P2 đã tái hiện bằng Bash thật; không phụ thuộc Windows native:

1. **`windows-hook-installer-fallthrough`** (`session-start.sh:192`): giả `uname=MINGW64_NT-10.0`, `rg --version` lần đầu qua, các lần sau rc1. Head gọi `RG 1, RG 2, apt-get install …, RG 3, cargo install ripgrep, RG 4`, rc0. Với rg ổn định head vẫn gọi hai lần. Thử giới hạn nhánh POSIX theo OS trên bản sao: chỉ `RG 1`, không installer. Vi phạm Q4/N8.
2. **`installer-selects-broken-path`**, nối F2 (`ops/cong_cu.yaml:93`): WinGet Links chứa rg rc0 nhưng stdout rỗng hoặc không parse được phiên bản, choco/bin chứa rg tốt 15.2.0. Head chọn Links, ghi vào GITHUB_PATH rồi `cai_cong_cu.sh` rc2/DO; bản tốt bị bỏ qua. Thử dùng chính tiêu chí kiểm tra của `cong_cu.py` cho từng ứng viên trên bản sao: cả hai đầu vào rc0/DAT 15.2.0, chọn choco/bin. Không chỉ kiểm sự thành công của tiến trình để quyết định thư mục dùng được.

Bằng chứng: `review-data/probe_boundaries.py`, `boundary-results.json`, `probe-boundaries.log`.

- F3: hai con trỏ của người gọi hiện được khôi phục đúng; riêng mutant bỏ mỗi phép khôi phục vẫn được runner báo `[0,0]`, nhưng phép kiểm độc lập thấy mất đúng con trỏ đó. Chưa có ca stock canh hậu điều kiện runner.
- F4: giả cờ skip Windows cho `[0,4]`; 4 mutant không đo và mutant chuỗi còn N6 giết 1/1, khớp handoff hiện tại.
- Tiêm AttributeError vô can vào runner hook: `[1,0]`, `SAI giet 0/1`, không tính giết giả.
- Đã thử TMPDIR riêng trong workspace; guard vẫn thấy cả `.git` ở workspace và `/tmp/.git`, tiếp tục từ chối storage. Mọi vị trí ghi được theo sandbox đều ở dưới `/tmp`; chỉ thị còn cấm ghi ngoài thư mục review. Vì vậy không có TMPDIR ngoài mọi repo theo guard trong quyền hiện tại. Không sửa/bỏ marker, không vá/bypass guard; suite N/N còn là giới hạn hạ tầng, không tự quy 12 ca đỏ nền thành hồi quy.

## Nhật ký phép đo — đợt 3

- Suite thường: head210/222,tổng232/skip10/đỏ12,rc1; base201/213,tổng223/skip10/đỏ12,rc1. Auth giả: head218/230,tổng232/skip2/đỏ12,rc1; base209/221,tổng223/skip2/đỏ12,rc1. Tập12 ca đỏ giống nhau ở cả4lượt; DELTA0. Tám skip venv/pip của full không xuất hiện trong auth; không quy thay đổi điều kiện venv/pip cho auth giả (suite đã pop biến ngay đầu).
- Hồi quy F5 được A/B thêm với code hook lượt1 db1ed4d: cùng fixture Windows flaky, lượt1 chỉ RG1/không installer; head RG1,RG2,apt-get,RG3,cargo,RG4; hướng sửa chỉ RG1.
- F2 thêm đối chứng Links rc1 + choco tốt: head và bản thử đều DAT; chỉ head thua2 biên rc0/rỗng và rc0/sai phiên bản.
- Symlink tốt và dangling symlink đều bare/head rc0; non-executable bị shell/head bỏ qua đúng. Mutant bỏ os.access tạo BI_CHE sai/rc12 cho non-executable trong phép kiểm riêng, trong khi10 ca thành phần stock không bắt được.

## Nhật ký phép đo — chốt

- `--dot-bien`: base **250/250**, head **264/264**, mỗi cây rc0 / 4 không đo; tăng đúng 14 mutant wp802. Tập 14 dòng ngoại lệ được tính kill ở harness cũ giống nhau giữa hai vế; không dòng wp802. Audit riêng 14 mutant mới đều assertion đúng ca.
- Cả 6 lượt suite đã kết thúc và có headline; mã thoát/thời gian lưu `suite-results.json`, tập ca đỏ/skip và headline trong `suite-summary.json`. Tổng suite không thay kết quả phản chứng F2/F5.
- Snapshot checkout nguồn cuối khớp đầu: 3765 tệp ngoài `.git`, HEAD/tree/status/diff/index không delta quan sát; `snapshot-comparison.json` có `match=true`.
- Kết luận chốt: **changes_requested**, 2 lớp P2 mở (F2 và F5), F3 hành vi đã sửa nhưng còn nợ test P3 có owner executor wp802. Windows/CI exact-head M-3 và N/N trong rig sạch vẫn chưa đo được ở quyền hiện tại; không lấy chúng làm lý do giả cho 2 finding code.
- Các tệp evidence chính và verdict có path/size/SHA-256 trong `review-data/artifact-manifest.json` (manifest được tạo sau khi chốt nội dung).
