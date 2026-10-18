verdict: approve
reviewed_sha: 5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456

Chốt lượt **5/5, CUỐI: approve**. F2 và F6 của lượt4 đã được vá thật trong phạm vi kiểm độc lập; không còn finding P0/P1/P2 hoặc P3 mở. Không phát hiện hồi quy sản phẩm do bản vá lượt4. Các giới hạn độ phủ và CI chưa đo trực tiếp được khai bên dưới, không được đọc thành các phép đo đã qua.

Reviewer OpenAI Codex; provider `openai_codex`, execution surface `codex_service` (API agent có shell), transport `machine`. Model ID/effort/session ID và danh tính executor thực chạy chưa có receipt độc lập: **KHÔNG ĐO ĐƯỢC**. Không suy surface từ lease, không tự cấp assurance hoặc quyền merge/land. Áp ngưỡng assignment: hết P0/P1 và mọi P2 đóng; P3 mở cần quyết định chủ kho.

Đã đọc prompt.snapshot đầy đủ, SPEC, AGENTS/CLAUDE, protocol §8/§13, adapter cross-review, bốn verdict trước và hai diff. Kiểm cả Spec và Standards/Security. Không push, không gọi GitHub, không sửa checkout `cay-kho` hoặc mirror `kho.git`. Mọi clone/vá thử/output nằm trong `review-data/` của rv5. Không tự soạn payload dựng đường dẫn thoát cây.

Neo HEAD/tree: `5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456` / `78773e6b62eea2c879ac3aa5948dca3d3db94a9a`. Merge-base: `fb490a7c3fa2992c6f4635ed091dafa813df2fe7`. SPEC SHA-256: `e4fd84e1f079d0ac4841a145d078473576af3a3e4e2f593e4f3e40c5de7200e0`. Diff/numstat bundle khớp byte với Git. Base/head dựng cùng một vòng lệnh: clone thường `--no-hardlinks --no-checkout`, detached exact SHA, `core.abbrev=7`, `core.autocrlf=false`, origin trỏ repo thật nhưng chỉ dùng mirror cục bộ. Python3.13.16/Linux; `PYTHONDONTWRITEBYTECODE=1`, TMPDIR trong rv5, Ruff `--no-cache`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: lượt1 `db1ed4dda529eb30806ecb053d2eef9933e188b1`; lượt2 `509dfa850ecb73a3624a777c699fd8a05812cc25`; lượt3 `a0de1f9e3be9d4e63369346c58d77bdb7a1a04c1`; lượt4 `3d65c954cd86c5138d3ad11998b272ead787f88c`. Giữ nguyên sáu slug, không reset lịch sử theo SHA.

| Finding / lớp | Phân loại lượt5 | Đối chiếu độc lập |
|---|---|---|
| F1 `bare-path-empty-entry` | **ĐÃ VÁ THẬT** trong phạm vi đo | Chạy lại9 bố cục shell/doctor: PATH rỗng đầu/giữa, dot, symlink hỏng, hai bản hỏng ⇒ bare1/doctor12, BI_CHE đúng bản đầu. Symlink tốt/dangling/nonexec/chỉ tốt ⇒0/0, không BI_CHE. Resolver Windows chung nối riêng F6. |
| F2 `installer-selects-broken-path` | **ĐÃ VÁ THẬT** | Header, warning stderr trước stdout, comma, stderr-only, prerelease và build riêng đều chọn Links/DAT. Rỗng/rác/rc1 bị loại, lùi choco. Cùng ba đầu vào header/warning/comma và choco hỏng: công thức lượt4 rc1, head rc0 đúng Links. Không còn hai regex quyết định khác nhau. |
| F3 `hook-pointer-restore` | **ĐÃ VÁ THẬT**, giữ đóng | Control11/11; hai mutant gỡ restore hook và YAML riêng đều chết đúng assertion ca r802_runner_tra_lai_con_tro_nguoi_goi; stock runner [0,0]. |
| F4 `windows-hook-mutation-count` | **ĐÃ VÁ THẬT** lời khai |22 wp802 =13launcher+7hook/YAML+2harness; log Windows có6hook/YAML không đo và1 parity còn đo; không còn khai hai resolver Windows-only. |
| F5 `windows-hook-installer-fallthrough` | **ĐÃ VÁ THẬT**, giữ đóng | MINGW/MSYS/CYGWIN × tốt/hỏng/flaky: không installer; flaky chỉ RG1. Linux vẫn apt-get→cargo. Mutant probe hai lần bị assertion nhật ký bắt. |
| F6 `tool-resolver-prefers-shell-shim` | **ĐÃ VÁ THẬT** | Chạy lại đúng12 bố cục của script lượt4 với nguồn shutil.which đang cài:11 parity,1 khác cwd có chủ ý. PATHEXT rỗng, suffix nối thêm, suffix nhiều đoạn đều đúng. Doctor với codex.EXE/PATHEXT rỗng: base0/co=true, head0/co=true. |

**Bảng lớp:**6 lớp lịch sử,0 lớp mở. F2 bao gồm mọi biểu hiện tiêu chí chooser/checker lệch qua bốn lượt; F6 bao gồm shim/cwd/PATHEXT/suffix của resolver dùng chung. Không cộng F6 thêm lần nữa vào F1. Các survival ở phần săn là giới hạn phép kiểm, không tự coi là lỗi sản phẩm tại head.

## BẢNG SĂN

| Hướng săn / lệnh, hiện vật | Kết quả thật | Ý nghĩa |
|---|---|---|
| `python -B review-data/probe_installer.py` |28 phép: các candidate hợp lệ0/DAT/Links; invalid0/DAT/choco; không ứng viên hợp lệ2, không tệp rg nào1; thiếu PY array126; ba route Python0; command-v fallback đúng; GITHUB_PATH vắng vẫn0 | Đóng các phản chứng F2, gồm fail-closed khi chạy công thức trực tiếp ngoài hợp đồng wrapper |
| A/B công thức lượt4/head, installer-AB-results.json | Header/warning/comma:1→0, checker candidate đều0; head ghi Links | Kiểm đúng hồi quy cũ, không lấy tổng suite để đóng F2 |
| Chooser gọi checker / cwd / tác dụng phụ | Wrapper thật gọi từ ngoài repo; đường có dấu cách; ba route python/python3/py -3. Nhật ký có tra công thức, một checker candidate thành công, rồi checker cuối. Snapshot cây fixture không đổi | Không thấy vòng lặp hoặc ghi tệp trong cây. Kiểm đọc source: kiem-tra chỉ probe rg --version, không gọi installer; cai_cong_cu.sh đã cd GOC trước eval. Đo chạy có tắt bytecode, không chứng nhận mọi side effect của binary rg bên ngoài |
| PATH MSYS / cygpath | Fixture chạy đường có dấu cách; log Windows exacthead cài rgDAT15.2.0 và bước sau vẫnDAT | Reviewer không chạy MSYS/native trực tiếp; cygpath trong phép local là stub. Log Windows bổ sung đường thật, không thay bằng chứng âm cho mọi cấu hình Windows |
| `probe_resolver_exact_round4.py` | Đúng12 bố cục cũ,7POSIX thật; doctor PATHEXT rỗng trở lại0/co=true | Copy đúng script lượt4 sang rv5, chỉ đổi tên output; giữ băm nguồn ở resolver-round4-origin.sha256. Không dùng bộ tự dựng bổ sung thay12 bộ cũ |
| `probe_resolver.py` / resolver-extra-mutation-results.json | Dot-trim, default .JS, direct-name và multipart suffix đúng với nguyên nguồn CPython3.13.16 | Bản hiện tại đúng ở các biên chưa có ca stock canh; comparator là nguồn cài tại chỗ, không chép lại thuật toán which |
| `audit_mutations.py` |11 control qua;20mutant product/hook có23 TinHieuChotCa đúng ca;2harness riêng qua kiểm giết;0 ngoại lệ vô can mới |22 wp802 có bằng chứng riêng; không nhận rc tổng làm tín dụng |
| Ca resolver giả platform | Spy ghi helper thật nhận Windows và kieu_bash=False cho x/y/z.CMD; tất cả trả đúng CMD/EXE/CMD.EXE | Đúng nhánh Windows của helper, không phải return sớm. OS path và sys.platform vẫn của host; không tuyên bố đây là Windows native |
| Mutant quay lại shutil.which trên POSIX | Chết đúng assertion vì which Linux lấy shim x. Mô phỏng12bố cục riêng xác minh bỏ tự chèn cwd; log native cũng có kill | Kill hợp lệ cho shim, nhưng gán nó riêng cho thuộc tính Windows tự chèn cwd trên POSIX là tín dụng quá rộng |
| `probe_behavior.py` |9doctor +9Windows-hook giả lập +1Linux; contract Ruff3/errors[] mỗi cây | F1/F5/parity được kiểm lại, không chỉ kế thừa verdict cũ |
| `run_survivors.py` |7 bản full: 5 bản212/224 như control; 2 bản211/224 chỉ thêm t117 kiểm neo chuỗi, không thêm assertion hành vi sản phẩm | Phân biệt thiếu coverage, guard dư và lỗi mã thực tế |

### Đột biến từng chốt, survival và tín dụng giả

| Chốt / thử nghiệm bản sao | Phân loại |
|---|---|
| Gỡ PATHEXT-empty fallback; cắt nhánh append khi tên có đuôi | Hai mutant mới bị đúng ca resolver bắt bằng TinHieuChotCa. Không còn Windows-only skip trên POSIX. |
| Bỏ rstrip; rút default còn4đuôi; dùng splitext thay suffix đầy đủ; bỏ tên trực tiếp | Cả11 r802 còn qua. Toàn suite: bỏ rstrip/rút default vẫn212/224; splitext/bỏ direct thành211/224 chỉ vì t117 không còn tìm thấy mỏ neo của mutant đã khai. Calibrate riêng neo metadata trong bộ nhớ: t117 qua mà không đổi sản phẩm (survivor-metadata-calibration.json). Không cấp kill hành vi cho hai kết quả metadata này. Comparator bổ sung chứng minh từng mutant làm mất executable đúng biên (dot-trim/.JS/multipart/direct CMD), nên đây là survival có nghĩa. **Head hiện tại không có các lỗi này.** Owner tăng coverage nếu làm tiếp: executor wp802/maintainer launcher. |
| Gỡ file check rg/rg.exe của chooser | Stock không bắt. Phản chứng riêng: Links không có rg, PATH cũ có rg tốt; control chọn PATH cũ, mutant lại ghi Links. Chốt tại head đang hoạt động đúng. |
| Gỡ RG_DICH init hoặc guard cuối | Stock không bắt; phản chứng no-candidate hiện vẫn rc2, kể cả thừa kế RG_DICH tốt. Khác lượt4: vòng for mới trả rc checker/file-check cuối thất bại, nên chuỗi && dừng trước echo. Hai guard này dư trong các bố cục đã đo; không tái báo lỗi stale RG_DICH của code cũ. |
| Thu stderr | Không còn regex shell riêng; checker tự thu stdout+stderr. Stderr-only và warningstderr đều đã chạy, không dùng kill grammar để chứng minh kênh output. |
| Tiêm AttributeError vào ca hook/YAML đích | Runner [1,0], SAI giet0/1; không cấp kill giả. |
|22 wp802 đã khai |13 product + 7 hook/YAML + 2 harness: đúng assertion ca đích,0 tín dụng exception giả trong audit mới. |
| Runner cũ ngoài wp802 |Cả base/head có14 dòng được nhận kill bằng4 AssertionError trần và10 ngoại lệ vô can (4OSError,2FileNotFoundError,1JSONDecodeError,2TypeError,1AttributeError), DELTA0. Tên đầy đủ ở suite-summary.json;0 dòng wp802. Không nhận14 dòng này theo chuẩn tín hiệu TinHieuChotCa. Nợ nền được tách khỏi kết quả mới; headline mutation không chứng nhận mọi kill trong toàn kho là thật. |

Độ phủ chưa tuyệt đối được khai ở đây, không lập finding P3 mới chỉ từ survival. Không có tuyên bố “mọi chốt đã có test”; các phản chứng độc lập đã kiểm mã thực tại các biên trên.

## BẢNG ĐO

| Tiêu chí / phép đo | Base → head | Đánh giá |
|---|---|---|
| Write set / ADR-0053 |64/7launcher,374/11test,13/3hook,9/0changelog,7/1yaml,15/0handoff = **6tệp,482thêm,22xóa** | Khớp assignment. Handoff có quyết định vượt450 “Chọn a”: https://github.com/ducthangho/tra-luat/issues/802#issuecomment-6246303988. Ngân sách+1attempt/+1Codex “Chọn1”: https://github.com/ducthangho/tra-luat/issues/802#issuecomment-6247229964. Áp authority được giao; không tự xác minh server. |
| Phạm vi baseline | Merge-base fb490a7 → exacthead | Con số482 là diff packet. de82ef74→head không lọc6paths còn gồm drift master; drift không chạm6tệp write set. Không nhận toàn bộ diff từ de82 là482. |
| N1–N4/N6–N8 |11 r802 qua, parity ba bảng đúng; mutant đúng ca đỏ | Đạt fixture và kiểm hành vi độc lập; Windows native phân riêng bên dưới |
| N10 full, không auth |201/213 (223tổng,10skip,12đỏ) →212/224 (234tổng,10skip,12đỏ); rc1/rc1 | Cùng12ca, DELTA0. Không tự khai N/N local |
| N10 auth giả |201/213 (223tổng,10skip,12đỏ) →212/224 (234tổng,10skip,12đỏ),rc1/rc1; cùng12tên ca,DELTA0 | CODEX_AUTH_JSON='{"tokens":{"x":"gia"}}'; suite pop biến đầu tệp. Đối chiếu đúng tập ca đỏ, không chỉ tổng |
|12ca credential đỏ | Cùng guard “Codex home is inside a repository” | /tmp/.git và marker .git của rig có mặt; không sửa/xóa marker hoặc nới guard để làm xanh. Không phải12 lỗi PR |
| Mutation toàn suite |250/250 →272/272,4khôngđo mỗi cây,rc0/rc0; tổng254→276 =+22 wp802 | Tách số không đo và tín dụng nền; không thay audit22 wp802 |
| N11 bare Ruff | Ruff0.17.1, check --no-cache --select F trên launcher.py/launcher_test.py:5F841 mỗi cây,rc1/rc1 | Đạt DELTA0; lint **không sạch**. Chưa chạy binary pinCI0.15.15 |
| Ruff pin/probe contract | loi_ruff_ci():3checks/errors[] mỗi cây | Chỉ cấu trúc YAML cài/probe, không thay bare lint |
| N11 còn lại | bash_nen quetDAT; doctrine-scan10tệp/0; bash-nrc0 cả hai cây | Đạt local |
| N12 WORKER local | Strict release-verify ok=true,187/187→188/188, mọi manifest file tracked;rc0 | Manifest tạm ngoài checkout. Check-run PR exacthead vẫn KHÔNG ĐO ĐƯỢC |
| N10 executor Linux evidence | EVIDENCE_full.log và full_auth:232/232,tổng234,2skip,rc0; mutation272/272,4khôngđo | Dữ liệu executor, không thay phép tự chạy trong rig; log Linux không mang fullSHA tự đủ để kiểm provenance độc lập |

### Windows/CI — dữ liệu được cấp và phần KHÔNG ĐO ĐƯỢC

Reviewer **KHÔNG ĐO ĐƯỢC Windows native/CI trực tiếp** và không gọi GitHub theo assignment. Đánh giá `EVIDENCE_windows_39109075826_5c6c7a8.log`:

| Mốc log | Bằng chứng / giới hạn |
|---|---|
|103/140 | Fetch và checkout fullSHA đúng reviewed_sha, Python3.13.16. Đã khắc phục lệch exacthead của evidence lượt4. Run/attempt/event/workflow-definition OID và kết luận check-run phía server chưa tự xác minh. |
|217–240 và338–350 | Cài rgDAT15.2.0; bước sau tiếp tụcDAT. Bằng chứng dương N9 trên exacthead trong log. stdout installer bị capture nên chưa xác định chắc winget hay choco thực chạy. |
|466 |201/201,tổng234,33skip,0hỏng. r802_doctor_rg_tran_hong_la_BI_CHE không nằm trong skip. Hỗ trợ mạnh N5/fixture rg.exe0byte; thiếu dòng qua riêng của control N1 như literalN5, không tráo dòng mutation thành control. WindowsApps thật chưa đo. |
|488–492 | Bốn mutant resolver có kill đúng ca, gồm hai mutant mới; sáu mutant shell/YAML vẫn không đo trên Windows. |
|764–779 |6hook/YAMLkhôngđo,1paritycònđo,2harnessgiết; mutation197/197,79khôngđo. Không gọi toàn bộ276mutant là đã đo Windows. |
|560–572 | Có UnicodeDecodeError ở thread đọc subprocess trong phần mutant cũ. Không coi log hoàn toàn sạch, không dùng lỗi thread này làm kill wp802; nguyên nhân native riêng KHÔNG ĐO ĐƯỢC trực tiếp. |

`ci.yml`, release-verify check-run, lease/ref live và receipt assurance hiện thời vẫn **KHÔNG ĐO ĐƯỢC** từ bundle. Không dùng thiếu kết nối GitHub làm lý do giữ changes_requested. WindowsApps thật, macOS và việc CLI dùng rg nội bộ hay PATH giữ nguyên chua_do_duoc của SPEC.

### installer-selects-broken-path [P2] F2 — ĐÃ ĐÓNG

**TỆP/DÒNG:** ops/cong_cu.yaml:93; consumer ops/cai_cong_cu.sh:10,72; checker ops/cong_cu.py:_chay/kiem_tra_1/main.

**VẤN ĐỀ:** Lịch sử là chooser khác chuẩn checker cuối (rc/output/multiline/stderr/biên token); lượt4 còn loại header/warning/comma dù checkerDAT.

**ĐÃ THỬ VÁ:** Đối chiếu hunk hiện tại dùng chính cong_cu.py kiem-tra --chi rg với PATH candidate, không còn sửa thử cần thiết để đóng phản chứng. Các biến thể gỡ checker/filecheck/init/guard chỉ chạy trên bản sao tạm, không ghi nhánh hoặc phát patch runtime.

**ĐÃ THỬ NGHIỆM:**28probe local, thêm ca mọi tệp rg vắng (rc1/không GITHUB_PATH), cùng6A/B, ba routePython, cwdngoài cây, no-candidate/PYvắng và đối chứng grammar/kênh output. Header/warning/comma lượt4rc1→headrc0/DAT/đúngLinks. Native bổ sung bằng log exacthead, không tự chạy.

**ĐỘ TIN:** Cao về chooser/checker Bash và hồi quy cũ; giới hạn MSYS/native/provenance nêu riêng. Mọi biểu hiện F2 đã đo đều đóng; không còn P2 mở.

### tool-resolver-prefers-shell-shim [P2] F6 — ĐÃ ĐÓNG

**TỆP/DÒNG:** .claude/dev/launcher.py:2285,2306–2321; .claude/dev/launcher_test.py:8135.

**VẤN ĐỀ:** Lịch sử là thay which bằng resolver chung làm chọn shim và mất executable khi PATHEXT rỗng hoặc tên đã có suffix; lượt4 thiếu thuật toán nhận suffix đầy đủ và append.

**ĐÃ THỬ VÁ:** Head đã fallback PATHEXT rỗng, rstrip dấu chấm, nhận endswith đủ suffix, thử tên trực tiếp khi phù hợp rồi vẫn append; chỉ tìm đúng thư mụcPATH. Đột biến gỡ từng phần được thử trong bản sao; không có sửa chữa trên cây executor.

**ĐÃ THỬ NGHIỆM:** Đúng script12bố cục lượt4 với nguyên nguồn CPython3.13.16 cài tại chỗ,7POSIX thật, doctorcodex/PATHEXT rỗng, comparator bổ sung và spyplatform. Ca stock đi đúng nhánh helper Windows; không coi việc giả platform là phép đo WinAPI.

**ĐỘ TIN:** Cao về thuật toán và hậu quả doctor trong phạm vi kiểm; native thật dựa evidence cấp. Biên dot/defaultJS/directsuffix có kiểm độc lập nhưng stock coverage còn giới hạn. F6 đã đóng, không còn P2 mở.

### Toàn vẹn và bàn giao

Snapshot trước/sau: **cay-kho3796/3796 tệp kể cả .git; kho.git622/622**, không thay đổi byte/mode/symlink. HEAD/tree, tracked/untracked/ignored, diff staged/unstaged đều giữ nguyên (snapshot-comparison.json). Sandbox thực tế workspace-write; read-only checkout được thực hiện bằng kỷ luật và kiểm hai mốc, không tự nhận sandbox cưỡng chế hoặc chứng minh không từng ghi rồi hoàn nguyên trong toàn bộ run.

Các script/log/JSON lượt5 nằm trong review-data: preflight, suite-results/suite-summary, installer-results/AB/fileguard, resolver-exact-round4-results, resolver-results, mutation-audit, survivors-full-results, behavior-results, gates và snapshot-comparison. measurement-notes.md ghi lỗi setup đã loại bỏ; không tính chúng thành finding/kill. VERDICT-progress.md lưu bản ghi tăng dần trước khi chốt; artifact-manifest.json neo path/size/SHA-256 của hiện vật chính sau khi writer kết thúc.

**Quyết định cuối: approve, exact reviewed_sha 5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456.** Kết thúc lượt5/5. Việc đăng receipt/state, kiểm CI/assurance còn thiếu và quyết định merge/land thuộc điều phối/chủ kho; không tự mở thêm ngân sách hay cấp quyền land.
