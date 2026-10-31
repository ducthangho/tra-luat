verdict: changes_requested
reviewed_sha: 288ad3ea79ef94e061b649effe7bee2c7e2a0a9b
spec_sha256: 4a512dd38721c3c4eec7978489ba06485feab32f94a0c5637a085d6c694ba38c
Ket qua: 0 P0, 2 P1, 0 P2, 0 P3.

reviewer_family: OpenAI Codex (theo runtime; độc lập với Executor Claude)
provider: openai_codex
execution_surface: codex_service
route: API/tool execution; không phải ChatGPT Web advisory
transport: machine
exact_model_id: runtime không cung cấp; không suy từ tài khoản hoặc lời khai cũ
review_axes: spec, standards_security
reviewed_tree: 608f7892b62b0a6222631cb0a548b6ee6ea524bf

Kết luận: cần sửa F01 (tín dụng đột biến giả) và F02 (fixture gọi installer ambient). Các nhánh không đo được do môi trường được tách khỏi lỗi, không mở lại ba nợ đã chấp nhận #824/#825/#826. Không có approve/land hoặc thay đổi GitHub nào được thực hiện.


Đã đối chiếu độc lập SPEC, diff và cây tại SHA được chỉ định. Các đột biến chạy trên bản sao ngoài `cay-kho/`. Không dùng mạng hoặc credential thật; không đọc verdict cũ của PR #792.


## Nhật ký tăng dần

### 1. Định danh và nguồn đặc tả — KHÔNG PHẢI LỖI

Lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `sha256sum SPEC.md`; so byte `git diff d347d426334bbe1bbb1161184ab0acffee9be054 288ad3ea79ef94e061b649effe7bee2c7e2a0a9b` với `diff.patch` và `--numstat` với `numstat.txt`.
Output: HEAD `288ad3ea79ef94e061b649effe7bee2c7e2a0a9b`; tree `608f7892b62b0a6222631cb0a548b6ee6ea524bf`; SPEC `4a512dd38721c3c4eec7978489ba06485feab32f94a0c5637a085d6c694ba38c`; `diff_exact_match: True`; `numstat_exact_match: True`.
`ops/specs/wp484-r7.md` không có trong head; lấy đúng blob từ `refs/remotes/origin/ops/wp484-r7-spec`, lưu `evidence/SPEC-r7.md`: SHA-256 `35a81f47dbea985ed867147fbf952be485faf5c3106e9c8afed27a0b41a533e1`, khớp SPEC r8. Không dùng master hiện tại làm chuẩn.

### 2. Credential suite và bẫy môi trường — KHÔNG ĐO ĐƯỢC một phần

Lệnh (cwd `cay-kho/`): `env -u CODEX_AUTH_JSON -u OPENAI_API_KEY -u GH_TOKEN -u GITHUB_TOKEN PYTHONDONTWRITEBYTECODE=1 CC_CHI_TIET=1 python3 .claude/dev/codex_cred_test.py`.
Output thật: `nền: 13/18 đạt`; rc=1; năm ca đỏ `t6`, `t9`, `t15`, `t16`, `t18`. Các ca gặp `OSError: Codex home is inside a repository`; t15 có nhánh home tồn tại trả rc=2 thay rc=3 do cùng bẫy. `ls -ld /tmp/.git` xác nhận thư mục rỗng, chỉ đọc. Đây là giới hạn môi trường đã được prompt báo trước, không tính hồi quy. Bộ test tự dừng trước bảng đột biến khi nền đỏ: 0/18 đột biến được chạy bởi lệnh này. Log: `evidence/codex-cred.log`.

Đã khởi chạy toàn bộ launcher suite trên cây thật với nhật ký ngoài kho và bảng đột biến trên bản sao `git archive` của đúng SHA ở `evidence/head-copy/`; không ghi tệp nguồn trong cây được review.


### 3. Merge cuối và cổng tĩnh — KHÔNG PHẢI LỖI

Tái dựng `git merge-tree --write-tree --messages 907214d2cd0b67ff444b3adf734811eab39bfc71 d347d426334bbe1bbb1161184ab0acffee9be054`, với `GIT_OBJECT_DIRECTORY` ngoài cây: rc=0, tree `7fccfab00b36716329d8ec0fb065e49839e9e0fe`, khớp `bf10fab^{tree}`. Chỉ tự gộp `packet_loop_test.py`, không xung đột. Log `evidence/merge-reproduction.txt`.
Ruff 0.17.1 trên 5 tệp Python sửa tay: base d347d42 = 5 F841, head = 5 F841, đều ở launcher_test; DELTA=0. Doctrine head rc=0, `đã quét 10 tệp, 0 chỗ chép doctrine`; adr-song head rc=0, `53 ADR trên đĩa, 53 dòng trong §20, khớp 1–1`.

### 4. Chấm đột biến sai nguyên nhân — LỖI (ứng viên P1)

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_runner.py` (bản sao ngoài cay-kho, không credential, không mạng).
Output: product target ném RuntimeError vô can trước assertion nhưng vẫn `g8_xong_rc0_van_giu_failure_class OK giet 1/1 ... (RuntimeError)`, accounting `(0, 0)`; harness neutral có RuntimeError, mutant cũng không tới assertion nhưng `headline_lay_tong_lam_so_ca_da_chay OK giet 1/1`, accounting `(0, 0)`.
N7 đòi chết đúng assertion; hai nhánh hiện nhận tín dụng giả. Không lấy lỗi /tmp/.git làm hồi quy: phản chứng này dùng lỗi fixture trơ, độc lập với storage. Log `evidence/probe-runner.log`.

### 5. Fixture F04 chạm installer môi trường — LỖI (ứng viên P1)

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_f04_installers.py`.
Chạy nguyên ca `r484_g7_hook_vang_codex_cai_cli_truoc_materialize`, chỉ đặt công cụ môi trường bằng shim vô hại, `rg --version` thất bại; apt-get/sudo/cargo giả chỉ ghi nhật ký rồi thoát 97, actionlint giả chạy được. Output: `F04 fixture result: None (None means pass)` và `AMBIENT installer calls: 6`: apt-get/sudo install, update, install. Ca chỉ kiểm NPM/materialize nên vẫn xanh sau 6 lời gọi installer ngoài fixture; nếu không có shim, nó gọi executable của máy chạy. Không cài gói hay gọi mạng thật. Log `evidence/probe-f04.log`.


### 6. Commit 288ad3e: ca đích tự bỏ qua — KHÔNG PHẢI LỖI cho hành vi bỏ qua

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_skip.py`.
Dùng ca Windows-only t62 trên Linux và mutant headline hiện có; neutral t118 = `(1, 0, [])`. Trên bf10fab: all-skipped `(1, 0)`/SAI 0/1; mixed `(1, 0)`/SAI 1/2. Trên 288ad3e: all-skipped `(0, 1)`/KHONG DO DUOC; mixed `(0, 0)`/OK 1/1, ghi rõ t62 bỏ qua. Phản chứng quay về runner cũ làm phép đòi skip đúng thất bại. Logic skip mới đúng; việc không phân biệt nguyên nhân chết còn lỗi riêng ở hướng 4. Log `evidence/probe-skip.log`.

### 7. Đột biến độc lập theo assertion — KHÔNG PHẢI LỖI một phần / KHÔNG ĐO ĐƯỢC phần storage

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_mutations.py`.
12 cặp neutral/mutant launcher/hook, mỗi cặp chạy trên bản sao ngoài cây, mỗi lần một tiến trình `-B`, cùng `PYTHONDONTWRITEBYTECODE=1`: 9/9 cặp đo được chết đúng assertion đích; 3 cặp storage neutral đã lỗi `/tmp/.git`, không tính giết. Các cặp đạt: 3 chốt trust Windows/POSIX, N5 home sai, N4 lỗi ghi state đường launcher, failure_class, N14 bỏ hoãn bridge, G01 tin shim hỏng, N13 đảo thứ tự cài/materialize. N10 riêng: t17 neutral PASS; bỏ token_invalidated ⇒ AssertionError `codex exec thoát rc=1` của chính ca.
Log/chi tiết: `evidence/independent-mutations.log`, `evidence/independent-mutations.json`. Không diễn giải các mutant storage được runner gốc báo OK là bằng chứng đúng.

### 8. Kết quả suite launcher và bảng đột biến — có giới hạn môi trường và lỗi bộ chấm

Launcher native: rc=1, `201/213 ca DA CHAY QUA (tong 223, bo qua 10, hong 12)`. Mười ca bỏ qua được in tên trong log; 12 ca lỗi đi qua storage dưới /tmp hoặc phụ thuộc materializer ấy. Không tính chúng là hồi quy mới.
Bảng đột biến trên bản sao exact head: rc=0, `DOT BIEN: 250/250 dat (4 khong do duoc tren nen nay)`, tổng 254. Tuy nhiên có ít nhất 5 nhãn OK chứa OSError/AttributeError thay assertion, bao gồm 3 đột biến g7 storage: không công nhận 250 là số giết đúng nguyên nhân. Đây là bằng chứng trực tiếp thêm cho hướng 4, không chỉ phản chứng giả lập. Log `evidence/launcher.log`, `evidence/launcher-journal.log`, `evidence/launcher-mutations.log`.

### 9. Kiểm kê lời khai, băm và scope lịch sử — KHÔNG PHẢI LỖI ở phần đo được

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/audit_claims.py`.
Quét TẤT CẢ 2914 dòng thêm không rỗng của 25 tệp bằng unified-diff với line number; gắn nhãn số/SHA/tên ca/điều kiện, không chỉ chọn từ một danh sách tự nghĩ. 1002 dòng có số, 117 có SHA/hex, 177 có tên ca/mutant, 521 có điều kiện (nhãn chồng nhau). Danh mục toàn bộ: `evidence/diff-additions.tsv`; token Git: `evidence/git-identifiers.tsv`; tên ca: `evidence/case-identifiers.tsv`.
5/5 lease g2–g6: băm spec/prompt, write-set hash và base tree đều khớp. R7 35a81f47… và r8 4a512dd3… khớp. Đếm e82af37f..653fef3f = 1580; g6 diff = 24 tệp; g7 không có commit sửa tay packet_loop_test (log first-parent/no-merges rỗng); commit cuối đúng +18/-3 launcher_test và +16/-1 handoff.
SHA object tồn tại không tự chứng minh lời khai CI, thời lượng, số token hay review identity cũ. Những phần cần GitHub/Windows/nhật ký lịch sử ngoài bundle ghi KHÔNG ĐO ĐƯỢC, không gọi mạng, không mở/đọc verdict cũ.


### 10. Ranh giới snapshot, lỗi từ chối và attempt — KHÔNG PHẢI LỖI ở phần đã đo

T14 credential probe: chạy nguyên fixture hiện có; neutral PASS, bỏ `moi.pop` bằng mutant đã đăng ký ⇒ AssertionError của chính t14 (child trơ kiểm môi trường, không dùng credential thật). N10: tập 6 dấu hiệu của `_kiem_song` bằng đúng tập `_do_codex_song` tại base d347d42, gồm token_invalidated; neutral t17 PASS, mutant t17 đỏ.
Home chưa tạo: CLI `codex_cred.py kiem --codex-home <scratch/absent>` trả rc=3 với `KHÔNG_ĐO_ĐƯỢC: thư mục Codex home chưa tồn tại`; bản sao bỏ nhánh lexists trả rc=2 `ĐỎ: không đọc credential an toàn được`. Không tự soạn đường dẫn thoát cây hoặc credential giả dạng thật.
Launcher journal có `r484_g2_checkpoint_resume_va_gia_auth_khong_refund -> qua`, `r484_g2_timeout_sau_output_khong_refund -> qua`, `r484_g2_bridge_scrub_va_chot_remote -> qua`; ba chốt trust trong hướng 7 neutral xanh và mutant đỏ. Nợ ràng buộc resume với lượt gốc #826 được giữ ngoài finding.

### 11. Băm phụ, so sánh gate base và gợi ý test-only — KHÔNG PHẢI LỖI ở phần đã đo

Danh mục SHA256: `evidence/sha256-references.tsv`: 14 giá trị duy nhất, 10 đối chiếu được raw spec/scope trong hiện vật và lịch sử Git; 4 hash hiện vật/proposal bên ngoài chưa đo được. Không suy hash đúng từ độ dài. Số ca khai trong handoff khớp số đăng ký trừ hai ca Windows-only: 99e79b1 216−2=214; b355ff8 220−2=218; cfd3550/0f31bb3 221−2=219; 907214d/bf10fab/head 223−2=221. Đây chỉ kiểm kích thước bộ ca, không tái chứng minh các lần chạy lịch sử.
Đo N9 lại trên bản sao base d347d42 với đủ companion launcher: doctrine-scan rc=0, 10 tệp/0 vi phạm; adr-song rc=0, 53/53; bằng head. Lần dựng fixture base đầu thiếu companion nên import lỗi, đã sửa bản sao và đo lại, không tính là hồi quy. `bash -n` hook rc=0; bash_nen `DAT: không có lời gọi trần mới`.
`HINT.patch` chỉ gợi ý cô lập fixture F04, áp bằng `patch -p0` từ cay-kho; AST và dry-run trên bản sao đạt. Đo cùng phản chứng installer với bản hint ngoài cây: ca PASS, `AMBIENT installer calls: 0` (bản nguyên 6). Hint không sửa runner và không phải đề xuất approve toàn bộ. Log `evidence/hint-validation.log`.

Kiểm toàn bộ byte trước/sau phát hiện suite native sinh một dấu hook ignored `.claude/.packet_state/session-start.ran`; đã dọn đúng tệp mới ấy để khôi phục trạng thái ban đầu. Không đổi nội dung tệp nguồn; bước kiểm băm cuối sẽ ghi ở phần kết quả.


## BANG NGHIEM THU

Các lệnh `python3 -B evidence/...` chạy từ thư mục chứa VERDICT; ba bộ test gốc chạy trong `cay-kho/`, với `PYTHONDONTWRITEBYTECODE=1` và gỡ CODEX_AUTH_JSON/OPENAI_API_KEY/GH_TOKEN/GITHUB_TOKEN của phiên. Đột biến launcher đầy đủ chạy từ `evidence/head-copy/` (bản git archive exact SHA). ĐẠT một nhánh không được đọc thành toàn tiêu chí ĐẠT khi bảng ghi một phần chưa đo.

| Tiêu chí | Lệnh đã chạy | Output thật | Đạt? |
|---|---|---|---|
| N1: toàn bộ launcher, phân biệt bỏ qua | `python3 .claude/dev/launcher_test.py --nhat-ky ../evidence/launcher-journal.log` | `201/213 ca DA CHAY QUA (tong 223, bo qua 10, hong 12)`, rc=1 | KHÔNG ĐO ĐƯỢC trọn bộ: bẫy /tmp/.git và thiếu venv/pip; không coi 12 ca là hồi quy |
| N2: giữ đích đổi trước replace | `python3 -B evidence/probe_mutations.py` (g7_bo_doc_lai_truoc_replace) | neutral và mutant đều `OSError: Codex home is inside a repository` | KHÔNG ĐO ĐƯỢC; không tính giết |
| N3: home hợp lệ chưa tạo | `python3 -B evidence/probe_env_and_absent.py` | nguyên rc=3 `KHÔNG_ĐO_ĐƯỢC: thư mục Codex home chưa tồn tại`; mutant rc=2 `ĐỎ: không đọc credential an toàn được` | ĐẠT nhánh home chưa tạo; t15 trọn ca chưa đo được do nhánh home đã có gặp /tmp/.git |
| N4 r8 đã HẠ: mỗi đường báo riêng lỗi ghi state | `python3 -B evidence/probe_mutations.py`; `codex_cred_test.py` | launcher neutral rc=0; mutant `lỗi ghi trạng thái bị nuốt`; cmd_kiem t16 và materializer neutral bị /tmp/.git | ĐẠT đường launcher; hai đường kia KHÔNG ĐO ĐƯỢC; không mở lại nợ #825 |
| N5: credential-status home sai không traceback | `python3 -B evidence/probe_mutations.py` (g7_home_sai_lai_traceback) | neutral rc=0; mutant rc=1 do chính ca báo `traceback thô` | ĐẠT; ca gốc kiểm cả home tương đối và có parent component |
| N6: credential suite N/N | `python3 .claude/dev/codex_cred_test.py` | `nền: 13/18 đạt`, rc=1, dừng trước đột biến | KHÔNG ĐO ĐƯỢC 5 ca bởi /tmp/.git |
| N7: bản sao ngoài cây, process riêng, đúng assertion | `python3 -B evidence/probe_runner.py`; bảng mutation đầy đủ | RuntimeError vô can được ghi `OK giet 1/1`; credential runner `would grant kill: True`; bảng đầy đủ có 5 OK do OSError/AttributeError | KHÔNG ĐẠT — F01. Nhánh product còn chạy nhiều mutant trong cùng process |
| N8: ruff F delta=0 | `python3 -m ruff check --select F --output-format json` trên 5 tệp sửa tay, đối chiếu blobs base d347d42 | base 5 F841; head 5 F841; delta=0; cả hai rc=1 | ĐẠT theo hợp đồng delta, không khai tuyệt đối sạch |
| N9: doctrine/ADR rc như base | `python3 -B cay-kho/.claude/dev/packet_loop.py doctrine-scan --root cay-kho`; `python3 -B cay-kho/.claude/dev/packet_loop.py adr-song --root cay-kho`; base dùng script/root dưới `evidence/base-gates/` | hai phía rc=0; doctrine 10 tệp/0 vi phạm; ADR 53/53 | ĐẠT |
| N10: token_invalidated, rejection thắng rc/marker | `python3 -B evidence/probe_credential_assertions.py` (t17) | neutral PASS; mutant AssertionError `codex exec thoát rc=1`; tập 6 chữ ký bằng base | ĐẠT; fixture t17 thử cả rc=1 lẫn rc=0+marker+stderr từ chối |
| N11: identity đúng bản probe, cả launcher/cmd_kiem | launcher g7_f03 và credential t18 trong các lệnh trên | neutral OSError /tmp/.git; không nhận tín dụng từ mutant | KHÔNG ĐO ĐƯỢC bằng kernel ở môi trường này |
| N12: materializer báo riêng lỗi state | `python3 -B evidence/probe_mutations.py` (g7_f01_materializer_gop_loi) | neutral OSError /tmp/.git | KHÔNG ĐO ĐƯỢC |
| N13: cài codex trước materialize, installer không thấy snapshot | `python3 -B evidence/probe_mutations.py` (N13-install-after-materialize) | neutral PASS; mutant `materialize chạy TRƯỚC cài codex: ['LAUNCHER chuan-bi', 'NPM install ...', ...]` | ĐẠT thứ tự; an toàn fixture có lỗi riêng F02 |
| N14: bridge hoãn, truyền snapshot bằng tham số, hook hỏng không materialize | `python3 -B evidence/probe_mutations.py` (N14-remove-deferral) | neutral PASS; mutant `thứ tự sai ... ['prepare', 'child', 'child']` | ĐẠT; ca gốc cũng kiểm hook rc=7 và không prepare |
| M-1: approve exact head | lượt độc lập này | changes_requested, F01/F02 | KHÔNG ĐẠT |
| M-2: trả lời/resolve thread và owner authority | Không gọi mạng theo chỉ thị | Không có readback GitHub mới trong bundle | KHÔNG ĐO ĐƯỢC; ba nợ #824/#825/#826 đã được chỉ thị loại khỏi finding |
| M-3: CI/Windows xanh exact head | Không gọi mạng/không có Windows | Chỉ có lời khai lịch sử trong handoff, không có check-run mới đo trực tiếp | KHÔNG ĐO ĐƯỢC, không gọi các lượt bị huỷ/bỏ qua là passed |
| M-4: wp775 land rồi merge lại master | `git merge-base --is-ancestor d8b15cb d347d42`; tái dựng merge-tree | ancestor rc=0; merge tree khớp bf10fab, không xung đột | ĐẠT quan hệ Git; trạng thái lease/CI GitHub không xác minh mới |
| M-5: head đổi thì evidence stale | `git -C cay-kho rev-parse HEAD` đầu/cuối | giữ nguyên 288ad3ea79ef94e061b649effe7bee2c7e2a0a9b | ĐẠT neo của lượt này; không chứng nhận head tương lai |

## BANG DO

Cách tìm: dùng toàn bộ `git diff --unified=0 d347d42 288ad3e`, giữ path/line của MỌI dòng thêm không rỗng; quét số, SHA/hex, tên ca và từ biểu thị điều kiện; sau đó đối chiếu AST, registry mutant, Git object/tree, băm raw spec, lease và chạy hành vi. Danh mục 2914 dòng/25 tệp nằm trong `evidence/diff-additions.tsv`, không chỉ là các câu người review chọn tay. Các nhãn chồng nhau: 1002 dòng có số, 117 SHA/hex, 177 tên ca/mutant, 521 điều kiện. Danh mục này hỗ trợ truy tìm, không tự chứng minh mọi điều kiện của Windows hoặc mọi lời khai lịch sử. Dòng chưa có phép đo hành vi được ghi giới hạn dưới đây, không suy “khớp” từ grep.

| Khẳng định | Diff khai | Đo được (lệnh/hiện vật) | Khớp? |
|---|---|---|---|
| Đúng đối tượng và diff | head 288ad3e, base d347d42 | rev-parse; so byte diff/numstat | Có: 25 tệp, +3186/−267; hai phép so True |
| Spec r8 và kế thừa r7 bất biến | 4a512dd3… và 35a81f47… | sha256sum SPEC; hash blob origin/ops/wp484-r7-spec | Có, đầy đủ hash ở đầu verdict/evidence |
| Merge đầu giải hai xung đột | launcher_test và session-start.sh, mỗi tệp một hunk | merge-tree faaedff/653fef3 trên object store tạm, `evidence/initial-merge.txt` | Có 2 tệp conflict; đọc blob merge đếm đúng 1 conflict hunk ở mỗi tệp |
| “cách 1580 commit” | handoff g7:9 | `git rev-list --count e82af37f..653fef3f` | 1580 |
| Hình dạng g6 +2461/−260, 24 tệp | spec r7/lịch sử g6 | `git diff --numstat e82af37f...faaedff` | Có; 9 tệp mã/workflow + 15 hồ sơ |
| Merge cuối không xung đột | bf10fab nhận d347d42 | merge-tree 907214d/d347d42; object store ngoài kho | Có, tree 7fccfab00b36716329d8ec0fb065e49839e9e0fe bằng bf10fab |
| Patch cuối +18/−3 | launcher_test.py | `git diff --numstat bf10fab 288ad3e` | Có; handoff cùng commit còn +16/−1 |
| Tên và OID Git | các SHA ở code/comment/handoff/lease | `evidence/git-identifiers.tsv`: 65 token giống OID, 30 resolve | 30 object tồn tại; phần còn lại gồm run ID, hash prefix, số GitHub, WinAPI constant; không ép chúng thành Git OID |
| Toàn bộ băm SHA256 thêm trong diff | spec/scope/proposal/hiện vật lịch sử | `evidence/sha256-references.tsv`, lịch sử raw spec + write-set hash | 10/14 đo được và khớp; 4 hiện vật ngoài bundle KHÔNG ĐO ĐƯỢC |
| Lease g2–g6 trỏ đúng spec/prompt/base tree/scope | 5 bản ghi | `python3 -B evidence/audit_claims.py`; lease-measurements.json | 5/5 cho cả bốn nhóm hash/tree; không chứng minh quyết định GitHub từ schema local |
| G7 không sửa tay file wp775 giữ | packet_loop_test chỉ nhận qua merge | first-parent/no-merges log faaedff..head với path này rỗng | Có; diff +31/−9 kế thừa vẫn được review và chạy suite |
| Số ca handoff theo head lịch sử | 214, 218, 219, 221 | AST đếm @ca tại các OID đã ghi ở nhật ký hướng 11 | Khớp cấu trúc: total trừ 2 Windows-only; KHÔNG tái chứng minh pass lịch sử |
| Tên ca/mutant được viện dẫn | N10–N14, r484_g*, t15–t18 | AST + DOT_BIEN; case-identifiers.tsv | Các tên đầy đủ tồn tại; t14_probe_ke_thua_snapshot và t15–t18 “bo/nuot/doc” là nhãn mutant, r484_g là tiền tố, t23 thuộc ops/cong_cu_test |
| Tập rejection phải là hợp với master | token_invalidated không được mất | AST tập của base _do_codex_song và head _kiem_song; t17 A/B | Hai tập cùng 6 phần tử; t17 mutant chết đúng assertion |
| Sống cần rc=0 và marker, rejection thắng | codex_cred._kiem_song | t3/t4/t5/t17 trong nền 13/18; mutant N10 riêng | Đạt các fixture trơ; auth thật/mạng KHÔNG ĐO ĐƯỢC |
| CODEX_HOME được chọn nhất quán, schema trước freshness | code và handoff g2 | launcher baseline, env-policy hai chiều, audit source | env-policy qua; nhánh đọc storage/doctor/schema thuận lợi bị /tmp/.git, KHÔNG ĐO ĐƯỢC trọn vẹn |
| Không đọc credential thô vào child | probe/hook/bridge/run scrub | t14 neutral/mutant, bridge baseline; shell/run fixture có storage | t14 và bridge đo được; shell/run đầy đủ bị materializer của /tmp/.git |
| Store pin/symlink/hardlink/ACL/byte-preservation/8MiB | _KhoCodex và lịch sử Windows/WSL | suite gốc + probe storage | Kernel storage hiện tại bị /tmp/.git; Windows không có. KHÔNG ĐO ĐƯỢC, không biến mock thành bằng chứng kernel |
| Candidate probe riêng, promote refreshed bytes, rollback | _probe_snapshot và recovery | baseline các r484_g2_storage/recovery/probe | KHÔNG ĐO ĐƯỢC bởi /tmp/.git; không tái nêu #824 |
| Ghi rejected identity của bytes đã probe | F03/da_probe | neutral/mutant launcher và t18 | KHÔNG ĐO ĐƯỢC kernel; source có truyền bytes, không lấy kiểm source thay hành vi |
| State ghi hỏng phải báo riêng | F01, ba đường | launcher N4 A/B; materializer/t16 | launcher khớp, hai đường còn lại chưa đo; #825 giữ là nợ chấp nhận |
| Bootstrap shell/bridge và shim --version | F04/G01 | independent-mutations.json | Đúng thứ tự và chặn shim hỏng; fixture N13 có F02 |
| BASH_ENV/installer isolation | fixture helper + fixture F04 mới | probe_f04_installers.py; baseline helper bị /tmp/.git | F04 mới SAI: 6 lời gọi installer ambient mà ca xanh; helper cũ không đo trọn được |
| “mỗi mutant chết đúng assertion” | N7 và handoff | probe_runner.py + full mutation log | SAI: cả product/harness/credential runner nhận lỗi vô can; F01 |
| Runner harness bỏ qua như product | commit 288ad3e | probe_skip.py, t62-only và t62+t118 | Đúng nhánh skip; không chữa F01 |
| Failure_class chỉ giữ cho lỗi/timeout | g8, launcher.py:1835 | g8 neutral + mutant; timeout fixture | Có: success bỏ nhãn; mutant bị assertion; timeout giữ unknown |
| Checkpoint HEAD/prompt/hash; unknown child không hoàn attempt | checkpoint/producer certificate | launcher journal; registered mutants; packet-loop suite | Các ca launcher qua; nợ ràng buộc với lượt gốc #826 không mở lại |
| Trust Windows chỉ đổi separator, POSIX giữ backslash | g6 comments/handoff | 3 neutral/mutant trong independent-mutations | 3/3 đúng assertion; nhánh Windows là mô phỏng platform, không phải kernel Windows |
| Workflow cài manifest deps + tool/canary trước doctor | launcher-windows.yml | đọc diff, bash_nen, YAML hiện có; không chạy installer thật | Thứ tự/source đúng; Py3.13 ACL, choco/CI/check-run thật KHÔNG ĐO ĐƯỢC |
| Thời gian, token count, calls/budget, model identity cũ, CI run ID/URL, Windows “181/182”, manifest 180/180, grant/resolve thread | các handoff/lease/comment lịch sử | chỉ có lời khai, link/OID và raw metadata trong bundle | KHÔNG ĐO ĐƯỢC độc lập khi cấm mạng và không có transcript ngoài bundle; không đọc verdict cũ hoặc tự xác nhận model từ người đăng |
| VERSION/CHANGELOG/RELEASE_MANIFEST và runtime config không bị bản review sửa | ngoài write set và scope | diff name list + băm trước/sau | Các tệp tracked không đổi; không sửa credential thật hoặc config người dùng |

## BANG TEST

| Bộ | N/M thật | Bỏ qua / không đo được |
|---|---|---|
| launcher_test native, rc=1 | 201/213 ca đã chạy; total 223; 12 lỗi môi trường | 10 bỏ qua, tên đầy đủ ở dưới; 12 lỗi liệt kê riêng, không nhận là pass |
| codex_cred_test native, rc=1 | nền 13/18 | 0 ca tự skip; 5 ca bị /tmp/.git: t6, t9, t15, t16, t18. Runner dừng: 0/18 mutant được chạy |
| launcher_test --dot-bien trên bản sao, rc=0 | headline 250/250; total 254 | 4 không đo được theo nền; ít nhất 5 “OK” do exception vô can, không được công nhận là 250 giết đúng nguyên nhân |
| Đột biến launcher/hook độc lập | 9/9 cặp đo được chết đúng assertion; tổng chọn 12 | 3 neutral storage lỗi /tmp/.git; mỗi neutral/mutant là subprocess -B riêng |
| Codex t17 N10 độc lập | 1/1 neutral PASS; 1/1 mutant chết AssertionError | Không có mạng/auth thật |
| Codex t14 env độc lập | 1/1 neutral PASS; 1/1 mutant chết AssertionError | Child trơ thực thi, chỉ dùng fixture có sẵn |
| Runner skip commit cuối | 4/4 phép đòi về all-skipped/mixed ở parent/head khớp; 2/2 neutral t118 qua | t62 được BỎ QUA có chủ đích, không tính như một ca chạy qua |
| Phản chứng runner | Product, harness, credential: 3/3 tái hiện tín dụng giả | Đây là phát hiện lỗi, không là positive gate |
| Phản chứng fixture F04 | Nguyên: ca xanh/6 ambient calls; hint: ca xanh/0 ambient calls | Tất cả installer là shim vô hại, không mạng/cài gói |
| Ruff F | base 5, head 5; delta 0 | rc=1 hai phía là 5 F841 nền |
| doctrine-scan / adr-song | head/base cùng rc=0; 10 tệp/0 vi phạm và 53/53 ADR | Không có skip ngoài ngoại lệ ADR-0016 vốn có |
| bash syntax / bash_nen | rc=0; `DAT: không có lời gọi trần mới` | SyntaxWarning có sẵn được ghi trong log, không phải lỗi test |
| packet_loop_test (kiểm riêng merge) | nền 351/351, total 352; mutant đo được 144/144, total 145; rc=0 | 1 baseline skip `luong_canonical_chay_that`; 1 mutant skip `luong_canonical_chay_that_dao_os_name` (Windows/pwsh) |

Mười ca launcher tự BỎ QUA:

- `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125` — Windows-only.
- `r484_g4_windows_sid_alias_identity` — Windows native SID.
- `r345_chan_socket_that_ma_than_hook_van_chay_dung`.
- `r345_cac_phep_do_cuc_bo_van_dung`.
- `r345_lop_tham_import_van_co_rang`.
- `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`.
- `r347_tham_import_van_song_tren_python_truoc_310`.
- `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`.
- `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`.
- `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO`.

Tám ca r345/r347/r348 tự khai `KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)`; không chạy mạng để chữa môi trường.

Mười hai ca native đỏ do bẫy storage hoặc materializer phụ thuộc nó: `t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac`, `r484_g2_doctor_doc_dung_home_da_materialize`, `r484_g2_schema_truoc_freshness_va_home_materialize`, `r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe`, `r484_g2_storage_kernel_guardrails`, `r484_g2_recovery_probe_rollback_va_snapshot_moi`, `r484_g2_probe_isolated_marker_va_refresh`, `r484_g2_hook_shell_scrub_truoc_probe`, `r484_g8_hook_scrub_kin_voi_bash_env`, `r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do`, `r484_g7_tu_choi_ghi_dung_ban_da_probe`, `r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi`. Log giữ đầy đủ lý do. Không thay primitive storage để làm chúng xanh.

Bốn mutant không đo được theo nền: `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner`, `g2_windows_directory_pin_access`, `124_khi_chau_con_song`. Năm tín dụng không hợp lệ trong full log: `g2_rejected_refresh_khong_phu_thuoc_metadata`, `g7_f03_doc_lai_sau_probe`, `g7_f01_materializer_gop_loi`, `g7_bo_doc_lai_truoc_replace` (OSError), `mcp_bo_kiem_kieu_gia_tri_server` (AttributeError). Đây là ít nhất năm, không khai các nhãn khác tự động đúng.

## BANG SAN

Các hướng độc lập, có lệnh và output thật (log tăng dần ở trên giữ diễn biến đo):

| Hướng | Lệnh / bằng chứng | Output thật | Kết luận |
|---|---|---|---|
| 1. Tính toàn vẹn head/spec/diff | rev-parse, sha256sum; audit_claims.py | head đúng; diff/numstat True; r7/r8 hash khớp | KHÔNG PHẢI LỖI |
| 2. Kho credential/kernel/đường dẫn | native launcher + credential suites; `ls -ld /tmp/.git` | OSError `Codex home is inside a repository`; /tmp/.git hiện hữu | KHÔNG ĐO ĐƯỢC; không dựng đường dẫn thoát cây hay payload credential giống thật |
| 3. Snapshot vào child | t14 fixture A/B; launcher journal bridge | neutral PASS; mutant AssertionError; bridge qua | KHÔNG PHẢI LỖI ở phần đã đo |
| 4. Rejection/rc/marker | t17 fixture A/B; so AST hai tập | PASS; mutant `codex exec thoát rc=1`; hai tập 6 phần tử | KHÔNG PHẢI LỖI |
| 5. Bootstrap shell/bridge | probe_mutations.py N13/N14/G01 | thứ tự đảo làm assertion đỏ; bridge mất hoãn đỏ; shim hỏng được nhận ra | KHÔNG PHẢI LỖI hành vi bootstrap; tích hợp CLI/storage thật KHÔNG ĐO ĐƯỢC |
| 6. Cô lập installer của fixture | probe_f04_installers.py | ca PASS, 6 ambient calls; hint PASS, 0 | LỖI — F02 |
| 7. Tính đúng của mutation oracle | probe_runner.py; full mutation log | RuntimeError vẫn OK giet 1/1; credential `would grant kill: True` | LỖI — F01 |
| 8. Skip của commit 288ad3e | probe_skip.py | parent SAI; head all-skip KHÔNG ĐO ĐƯỢC, mixed OK 1/1 | KHÔNG PHẢI LỖI nhánh skip |
| 9. Trust Windows/POSIX | 3 cặp g6 trong probe_mutations.py | neutral 3 qua, mutant 3 AssertionError | KHÔNG PHẢI LỖI; không nhận mock là kernel |
| 10. Attempt/certificate/checkpoint | launcher journal; packet-loop suite | checkpoint/timeout qua; g8 success mutant đỏ; packet-loop baseline 351/351 | KHÔNG PHẢI LỖI ở phần đã đo; giữ nợ #826 |
| 11. Merge/scope/metadata lịch sử | hai merge-tree ngoài kho; lease/hash inventory | merge cuối tree khớp; 5/5 lease hash khớp; g7 không sửa tay packet_loop_test | KHÔNG PHẢI LỖI phần local; thẩm quyền GitHub KHÔNG ĐO ĐƯỢC |
| 12. Gate và lời khai vận hành | ruff/doctrine/ADR/bash; không gọi GitHub | delta F=0, doctrine/ADR rc=0, bash hợp lệ | KHÔNG PHẢI LỖI local; CI/Windows/time/token/model identity cũ KHÔNG ĐO ĐƯỢC |

### F01-mutation-oracle-unrelated-exception [P1] Bộ chấm đột biến nhận lỗi vô can như assertion giết mutant

TEP/DONG: `.claude/dev/launcher_test.py:10246`–10257 (nhánh product), `:10316`–10333 (nhánh harness, có trong delta cuối); `.claude/dev/codex_cred_test.py:568`–572 và `:610`–611. Neo theo file ở reviewed_sha, không theo master hiện tại.

VAN DE: Product append cả ngoại lệ thường vào `chet`, rồi chỉ so số lượng. Harness chỉ đòi rc=1 và một dòng tổng kết 0/1, dòng mà chay_bo_ca cũng in khi fixture RuntimeError trước assertion. Credential suite cũng gộp mọi Exception vào tập tên đỏ rồi so với phai_chet. Do đó phép chấm cấp tín dụng cho mutant chưa hề bị assertion đích kiểm tra. Không có neutral precheck trong runner launcher nên nền đã đỏ vẫn sinh “250/250 đạt”. Vi phạm N7 và làm mất ý nghĩa chứng cứ của các ca g7 vừa thêm. Product còn dùng chung process giữa các mutant, trái yêu cầu process riêng của N7. Đây là finding về acceptance/chứng cứ của packet; không khẳng định tất cả nhánh lỗi đều mới xuất hiện ở hai commit cuối.

DA THU NGHIEM: `env -u CODEX_AUTH_JSON -u OPENAI_API_KEY -u GH_TOKEN -u GITHUB_TOKEN PYTHONDONTWRITEBYTECODE=1 CC_CHI_TIET=1 python3 -B evidence/probe_runner.py` trên bản sao ngoài cây. Product in `g8_xong_rc0_van_giu_failure_class OK giet 1/1: ... (RuntimeError)` và `(0, 0)`. Harness neutral đã RuntimeError, mutant không tới assertion nhưng vẫn `OK giet 1/1` và `(0, 0)`. Credential t17 neutral có failed set rỗng; chèn RuntimeError vào probe của bản sao làm failed set đúng tên t17 và `would grant kill: True`, không phải AssertionError của t17. Bảng đủ thực tế còn cho ít nhất 5 OK vì OSError/AttributeError, dù baseline storage đỏ. Các hiện tượng /tmp/.git không được tính là lỗi sản phẩm; finding là bộ chấm lại coi chúng là giết hợp lệ.

DO TIN: cao — ba đường tái hiện, có cả neutral/mutant và bằng chứng full runner. Không cần mạng, credential hay Windows.

Gợi ý vá (test/harness): sửa cả ba điểm phân loại kết quả, giữ nguyên logic skip đã đo đúng của 288ad3e. Chạy neutral đúng ca trước khi xét mutant; neutral lỗi thì báo KHÔNG ĐO ĐƯỢC/runner error, không cấp tín dụng. Đưa từng mutant/case vào subprocess riêng `-B`/PYTHONDONTWRITEBYTECODE và trả kết quả có cấu trúc, phân biệt target assertion, exception vô can và skip. Hỗ trợ cả `bang`/TinHieuChotCa lẫn bare assert có traceback nguồn đúng ca/helper của suite; không dùng headline hoặc rc làm chứng cứ nguyên nhân.

Ca khóa: chính `probe_runner.py` phải hết tái hiện tín dụng; RuntimeError/ImportError/AttributeError cùng lỗi neutral không được qua, assertion đích phải vẫn được tính một kill, all-skip/mixed của probe_skip.py phải giữ kết quả. Mutant bỏ kiểm tra loại/nguyên nhân lại phải làm ca khóa đỏ. Rủi ro vá: chặn nhầm bare assert hiện có, nhận sai helper assertion, hoặc biến Windows skip thành lỗi; giữ các đối chứng ấy. Không có HINT runtime; phần này là hướng sửa harness, executor tự dẫn xuất.

### F02-f04-fixture-ambient-installers [P1] Ca bootstrap mới vẫn gọi installer môi trường khi thiếu rg

TEP/DONG: `.claude/dev/launcher_test.py:7815`–7831 và `:7837`–7842, hàm `r484_g7_hook_vang_codex_cai_cli_truoc_materialize`.

VAN DE: Fixture chỉ giả npm/python3, giữ các thư mục PATH không có codex/npm/claude và chép nguyên môi trường. Hook thật tiếp tục chạy sau materialize; nếu rg có mặt nhưng không chạy được hoặc bị thiếu, nó rơi vào nhánh apt-get/sudo/cargo từ môi trường. Ca chỉ kiểm NPM đứng trước materialize và BAN-NPM vắng, nên cả sáu lời gọi installer môi trường vẫn báo qua. Trên runner thật đây có thể là cài gói/cập nhật chỉ mục ngoài fixture trong lúc chạy bộ test. Các guard fakebin và scrub BASH_ENV của helper shell cũ không được áp cho ca F04 mới này.

DA THU NGHIEM: `env -u CODEX_AUTH_JSON -u OPENAI_API_KEY -u GH_TOKEN -u GITHUB_TOKEN PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_f04_installers.py`. Chỉ dựng shim công cụ trơ trong scratch: rg thất bại, actionlint chạy được, apt-get/sudo/cargo ghi log và thoát 97. Ca nguyên trả None (PASS), log có 6 dòng: apt-get/sudo install, apt-get/sudo update, apt-get/sudo install. Không có installer thật hoặc mạng được gọi trong phản chứng. Với HINT trên bản sao: cùng phép đo PASS, ambient calls=0.

DO TIN: cao — nguyên ca bootstrap, executable ambient là shim ghi nhật ký, có A/B 6→0 và không phụ thuộc /tmp/.git.

Gợi ý vá: tại chính fixture N13, giả rg/actionlint chạy được và che mọi installer còn lại bằng shim ghi log rồi thất bại; dựng HOME tạm, lọc BASH_ENV/ENV/BASH_FUNC_* trước child; khẳng định không có lời gọi installer ngoài npm giả. `HINT.patch` là gợi ý test-only theo hướng này, chưa áp cây thật; AST/dry-run và phản chứng installer trên bản sao đã đo. Không sửa hook sản phẩm để né hành vi cần kiểm.

Ca khóa: chạy fixture trong môi trường có rg hỏng và installer ambient chỉ ghi nhận; đòi ambient calls=0 trong khi npm giả vẫn đứng trước chuan-bi. Thêm đối chứng BASH_ENV sống có thể đổi PATH nhưng không lọt vào hook. Mutant gỡ fake rg/installer guard hoặc scrub phải làm ca khóa đỏ; mutant đảo materialize/cài CLI hiện có phải tiếp tục đỏ. Rủi ro vá: fake quá rộng làm mất phép đo bootstrap cài codex thật trong fixture, hoặc bỏ luôn bước sau materialize; giữ nhật ký thứ tự và N13/N14 như đã có.


## Hoàn tất và kiểm toàn vẹn

`packet_loop_test.py` kết thúc rc=0: `nền: 351/351 đạt · BỎ QUA: 1`; tổng 352 ca, 145 mutant; 144 mutant đo được đều OK, một mutant `luong_canonical_chay_that_dao_os_name` tự bỏ qua theo nền (ca đích `luong_canonical_chay_that`); `TỔNG: ĐẠT`. 78/78 lớp lách có ca/đột biến, không có ngoại lệ AC18. Log đầy đủ `evidence/packet-loop.log`.

Kiểm byte cuối (`evidence/final-integrity.json`): **3696/3696 tệp giữ nguyên**, added=[], removed=[], changed=[]; `git status --porcelain` rỗng; HEAD giữ nguyên `288ad3ea79ef94e061b649effe7bee2c7e2a0a9b`, tree `608f7892b62b0a6222631cb0a548b6ee6ea524bf`; không shallow, core.abbrev=7. Các file đột biến, hint, log và object Git của phép tái dựng merge đều nằm ngoài `cay-kho/`.

Giới hạn provenance của lượt này: báo cáo tự khai đúng bề mặt chạy hiện có; không thay receipt/vận chuyển verdict do hệ thống điều phối xác minh. Không xác nhận lại các review identity cũ. Lần liệt kê tệp ban đầu vô tình trả tên các VERDICT khác; không mở nội dung hoặc dùng kết luận của chúng. Không thực hiện mạng, push, sửa ledger land, auth thật hay thay config người dùng. Các hướng cần tự soạn đường dẫn thoát cây hoặc credential giống thật chỉ được mô tả bằng lời; các phép đo tái dùng fixture trơ có sẵn.

`HINT.patch`: gợi ý test-only cho F02, dùng `patch -p0` từ cây đích khi executor tự quyết định áp; ở lượt này chỉ áp/đo trên bản sao. F01 có đầy đủ hướng sửa, ca khóa và rủi ro ở finding, không giả định một patch nhỏ đã đóng toàn lớp.


Bổ sung phép đo N7 cho bằng chứng credential độc lập: `PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/probe_credential_assertions.py` chạy bốn subprocess riêng (t14 neutral/mutant, t17 neutral/mutant), mỗi bản sao riêng, đều `-B` và PYTHONDONTWRITEBYTECODE=1. Hai neutral rc=0 `TARGET PASS`; hai mutant rc=1, traceback neo đúng hàm test và kết thúc AssertionError. Log `evidence/credential-assertions.log`. Không lấy chấm exception gộp của suite gốc thay cho kiểm nguyên nhân trong phép đo độc lập này.
