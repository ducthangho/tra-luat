verdict: changes_requested
reviewed_sha: e3bcaf0b376e80367b750ccc8c41cce9b686b407
spec_sha256: 81070fa2c5a00bc0bb63867c7173f310cba9002001b68a26d62726ec904cbf5b
Ket qua: 0 P0, 1 P1, 0 P2, 0 P3.

Phản chứng F08 nguyên văn của lượt 5 đã được vá ở runner đột biến trực tiếp và cả ba chế độ CLI. Tuy nhiên, khẳng định bao **mọi điểm vào chạy ca** còn thiếu hai hàm gọi trực tiếp: `cham_mot_ca` và `chay_bo_ca` vẫn thực thi registry bị cấm trước khi kiểm. Finding cùng lớp F08 bên dưới chỉ nói về hai đường này, không khai rằng CLI đã vá vẫn bị vượt qua.

Reviewer: Codex; provider `openai_codex`, execution_surface `codex_service`, transport `machine` (shell cục bộ qua công cụ). Không suy danh tính từ CLI/tài khoản đăng verdict. Model endpoint cụ thể, identity/authority lịch sử của executor và check-run bên ngoài: KHÔNG ĐO ĐƯỢC độc lập. Executor theo assignment: Claude; lease `wp1079-r1-g7-claude`, packet #1079 r1, sensitive, lượt 6/6 cuối. Review axes: spec và standards/security. Không tạo thêm phiên reviewer.

HEAD/tree: `e3bcaf0b376e80367b750ccc8c41cce9b686b407` / `12b98b8fdd327c4322aba5e5806010cd8a0e3dd4`. BASE: `7eeb1d9a10aea8e1805b66fbf3d68549eb6778da`. SPEC tự băm khớp assignment. Tổng thêm **769 dòng** (49 credential +720 launcher), dưới trần **800** đã được chủ kho nâng; không tính trần thành finding. Không tính lại nợ #1117.

## Cách chạy, phạm vi và tìm lời khai

Mọi lệnh `python3 -B ../review6/common.py <script>.py [args]` dưới đây chạy từ `cay-kho/`. Ví dụ: `python3 -B ../review6/common.py entrypoints.py`. Script/log/bản sao đều ở `../review6/`, ngoài cây review. `common.py` dựng môi trường tối thiểu: PATH công cụ cục bộ, HOME scratch, locale, tắt bytecode, Git global/system trơ, `PIP_NO_INDEX=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`. Không truyền credential của cha, không đọc giá trị secret, không gọi mạng hoặc installer thật. Chỉ dùng marker trơ, shim ghi log và fixture có sẵn; hướng cần tự soạn nội dung nhạy cảm không được triển khai.

Đã đọc `AGENTS.md`, các con trỏ protocol/development/provider và SPEC; authority riêng trong PROMPT cho phép lượt 6 và 800 dòng. Môi trường cloud-runtime không có công cụ `environment_status` khả dụng; không suy trạng thái credential hay mạng từ việc ấy. Không dùng dịch vụ ngoài.

Cách tìm lời khai tránh chỉ lập danh sách theo trí nhớ: `audit.py` duyệt toàn diff theo hunk `@@`, ghi **769/769 dòng thêm** kèm tệp/số dòng vào [claims-all-added-lines.tsv](review6/claims-all-added-lines.tsv); đã đọc các hunk sửa assertion, helper, fixture, ca khóa, bảng mutant, runner/reporter và kênh. Đồng thời duyệt **toàn bộ** `git rev-list BASE..HEAD`, không chỉ log theo path: **34 commit =9 packet +25 master/merge**. Toàn `%B` ở [commits.txt](review6/commits.txt), path/phân loại ở [commit-inventory.json](review6/commit-inventory.json). `claim_history.py` so AST/tập tên/nội dung từng mutant với cha của cả 9 commit packet. Các bảng đo nhóm lời khai dùng cùng phép kiểm; inventory không tự chứng minh một mệnh đề lịch sử.

`diff.patch` khớp byte với `git diff BASE HEAD -- .claude`. Scope đúng hai tệp test. 25 commit master/merge và nội dung ngoài `.claude/` được kiểm kê, không nhận thành thay đổi của packet. Những lời khai CI, quyền chủ kho, session, lịch sử số chạy ở máy khác không có check-run/log độc lập được ghi KHÔNG ĐO ĐƯỢC; không lấy thông điệp Git làm bằng chứng chạy độc lập.

Các script thích hợp từ lượt 5 được chép, đọc, cập nhật HEAD/root và **chạy lại**; không dùng log cũ làm kết quả mới. `old_proofs.py` bảo tồn nguyên văn counterexample từ các lượt 2–4 trong [previous-proofs](review6/previous-proofs), chạy lại trên HEAD. Các HINT lịch sử được lưu ở [previous-hints](review6/previous-hints); băm HINT 1/3/4/5 và AST hai ca được nhận ở HEAD khớp lời khai provenance. BASE xuất bằng `git archive` ra scratch; archive không có `.git` ở gốc, vì vậy full-suite BASE là đối chứng chẩn đoán môi trường, không khẳng định mọi trạng thái Git của archive tương đương checkout.

## Đối chiếu findings cũ — đo trước các hướng mới

| Finding cũ | Lệnh từ cay-kho/ và output HEAD thực | Kết luận |
|---|---|---|
| Lượt 5 F08: gán CA trực tiếp, runner/CLI không từ chối | `python3 -B ../review6/common.py prior.py`: decorator và direct runner ValueError; hai khóa lượt 5 PASS, gồm default/lap/mutants không chạy marker | **Đã vá phản chứng đúng nguyên văn này**; còn hai đường helper bên dưới, cùng lớp F08 |
| Lượt 3 F08 / lượt 4 F05: own assertion và lời gọi thật sang ca cùng factory | `python3 -B ../review6/common.py old_proofs.py`: product/credential nguyên văn ValueError; harness nguyên văn neutral `loi`, ca cũ dừng ở kiểm neutral. `prior.py`: chính sách mới từ chối trước chạy đúng khóa | Những setup cùng code nay bị cấm theo authority; không coi các khóa cũ đòi neutral xanh là hồi quy. Không khôi phục phép trừ code |
| Lượt 2 F05: ca KHÁC có code riêng | `python3 -B ../review6/common.py oracles.py`: a/b SAI 0/1 có loại; c suffix `(chot cua ca khac)`. Ba phản chứng nguyên văn lượt 2 PASS trong `old_proofs.py` | Đã vá hướng đã đo |
| Lượt 1/2 F01: tên/qualname lớp giả, stdout giả | `python3 -B ../review6/common.py old_proofs.py`: fake RuntimeError và fake AssertionError cùng tên `(1,0)`; own `(0,0)`; wrapped `(1,0)`. `oracles.py`: stdout giả không kênh → loi | Đã vá phần này |
| Lượt 1 F02: dò Bash chạy init/HOME cha | `python3 -B ../review6/common.py fixture.py`: HEAD 0 init/installer; cả hai probe Bash và hook có HOME fixture, không BASH_ENV/ENV/BASH_FUNC | Đã vá |
| Lượt 1 F03: khóa credential chỉ tìm chuỗi | `python3 -B ../review6/common.py locks.py`: mutant thay thực thi, giữ comment → OWN_SIGNAL đúng `r1079_cc_chay_suite_phai_do_hanh_vi` | Đã vá |
| Lượt 2 F06: target thiếu/trùng tên | `python3 -B ../review6/common.py extra.py`: all-missing/partial/duplicate-name đều `(1,0)`; khóa nguyên văn lượt 2 PASS | Đã vá nhánh product đã được finding nêu |
| Lượt 2 F07: khóa neutral chỉ tìm source | `python3 -B ../review6/common.py prior.py`: khóa gỡ thực thi nhưng giữ literal PASS; `locks.py`: gỡ neutral a/b làm đúng khóa OWN_SIGNAL | Đã vá |
| Lượt 4 F09 và câu sai của 5368c34 | `python3 -B ../review6/common.py claim_history.py`: 5548919 thêm 4 tên, sửa 3 hàng; c5acb70 đính chính cả số 5 và lời khai F05 của 5368c34 | Đã đính chính; không tính lịch sử đã sửa thành finding còn mở |
| Lượt 2 F04 | `python3 -B ../review6/common.py old_proofs.py`: forged channel vẫn `(0,0)`; `RECEIVER_UNCHANGED True`, `MAIN_UNCHANGED_EXCEPT_REGISTRY True` so lượt 5 | Nợ **#1117** được chủ kho nhận; phần nhận kênh không đổi, main chỉ thêm validator. Không có bằng chứng bản vá làm nợ tệ hơn, không tính lại |

`prior.py` cho **19/19** khóa r1079 PASS. `claims_extra.py` xác nhận toàn bộ **347 ca cũ còn nguyên số/tên**, cùng 2 ca mới thành **349/349 code object riêng**; credential **18/18**. `kiem_registry` nhận toàn bộ registry hiện hữu. Không có ca hiện có bị cấm nhầm do code trùng. Đây là bằng chứng về tập ca hiện tại, không chứng minh mọi kiểu callable có thể viết trong tương lai.

## BANG NGHIEM THU

| Tiêu chí | Lệnh từ cay-kho/ | Output thực | Đạt? |
|---|---|---|---|
| M1: a chỉ chốt đúng lớp, lỗi khác in tên/loại, giữ skip | `python3 -B ../review6/common.py oracles.py` | own OK 1/1; AttributeError, wrapped, bare AssertionError, other đều SAI 0/1; all-skip `(0,1)`, mixed `(0,0)` | Đạt đối chứng đã đo trong registry hợp lệ |
| M2: neutral a/b trước mutant, cache và fail-close | `python3 -B ../review6/common.py oracles.py`; `python3 -B ../review6/common.py extra.py` | neutral đỏ `(1,0)`; a calls `[True,False,False]`, b marker `['0','1','1']` cho hai mutant | Đạt các đối chứng |
| M3: b đúng nguyên nhân, stdout/rc không là chứng cứ | `python3 -B ../review6/common.py oracles.py`; `python3 -B ../review6/common.py old_proofs.py` | own `(0,0)`; lỗi vô can/cùng tên/wrapped/stdout giả đều `(1,0)` | Đạt phần ca chạy; giữ giới hạn module trước main thuộc #1117 |
| M4: c đúng lớp hoặc assert đúng tệp, không nhận lỗi implementation/đổi kiểu | `python3 -B ../review6/common.py oracles.py` | neutral `{}`; own `{t2}`; AttributeError/wrapped/implementation assert/other có suffix; tệp khác cùng dòng assert PASS khóa loại | Đạt các đối chứng |
| M5: 11 mutant cũ giết bằng chốt của ca | `python3 -B ../review6/common.py historical.py` | 10 OK đúng target; recovery metadata neutral OSError, `RESULT_SPEC11 (1,0)` | 10 đạt; 1 KHÔNG ĐO ĐƯỢC do `/tmp/.git` |
| M6: N13 kín, npm trước materialize | `python3 -B ../review6/common.py fixture.py` | BASE PASS/7 installer+2 init; HEAD PASS/0/0; log npm trước chuan-bi | Đạt cục bộ |
| M7: khóa hành vi và mutant từng chốt | `python3 -B ../review6/common.py prior.py`; `python3 -B ../review6/common.py locks.py`; `python3 -B ../review6/common.py make_hint.py` | 19/19 khóa hiện có PASS; 25 mutant/28 target OWN_SIGNAL; hai khóa helper mới OWN_SIGNAL trên HEAD, prototype 2 PASS, gỡ riêng từng guard đúng khóa OWN_SIGNAL | Khóa đăng ký có răng; **chưa bao hết đường gọi trực tiếp**, F08 |
| A1: ba gate đầy đủ trong điều kiện chuẩn | `python3 -B ../review6/common.py suites.py head` (thực gọi đúng ba lệnh SPEC) | launcher315/339(rc1), mutation511/547(rc1), credential13/18(rc1); BASE296/320,522/522,13/18 | KHÔNG ĐO ĐƯỢC dưới tiền đề `/tmp/.git` vắng; không gọi gate xanh |
| A2: scorer mới/ca BASE, khóa trên scorer/fixture BASE | `python3 -B ../review6/common.py historical.py`; `python3 -B ../review6/common.py legacy.py`; `python3 -B ../review6/common.py fixture_base_lock.py` | 446 hàng:397 OK,34 neutral đỏ,11 SAI,4 skip; base a/b AttributeError vẫn OK,c `{t2}`; khóa neutral/c đỏ TinHieuChotCa; hậu điều N13 trên fixture BASE OWN_SIGNAL | Đạt phản chứng đo được; không xác nhận đủ đúng 11 tên SPEC dưới điều kiện chuẩn |
| A3: installer A/B ghi log | `python3 -B ../review6/common.py fixture.py` | 7→0 installer shim,2→0 init; shim thất bại rc97; không installer thật | Đạt |
| A4: Ruff delta, diff-check, doctrine, CI | `python3 -B ../review6/common.py audit.py` | Ruff5 F841→5 F841 delta0; hai Ruff rc1 nền; diff-check rc0; doctrine rc0 cả hai,10 tệp/0 vi phạm | Local đạt; **CI check-run exact HEAD KHÔNG ĐO ĐƯỢC** do cấm mạng |

A2 không dùng số tổng 11 để khai đủ đúng 11 tên SPEC: 10 tên SAI thực đo thuộc SPEC, cộng `PROMPT_FILE_mo_coi_di_tiep` vì r13 BASE gọi registered t70, được bộ chấm mới loại là assertion ca khác. Tên SPEC `g2_rejected_refresh_khong_phu_thuoc_metadata` bị neutral OSError, cùng 33 neutral đỏ khác. `extra.py` đo r13/t70 hiện tại qua helper chung: mỗi ca giết mutant thật riêng OK1/1, đều `(0,0)`.

## BANG DO

| Khẳng định | Diff/commit khai | Đo được (lệnh từ cay-kho/) | Khớp? |
|---|---|---|---|
| Bao mọi điểm vào/CA gán thẳng | helper docstring và `%B` e3bcaf0 | `python3 -B ../review6/common.py entrypoints.py`: main/runner/decorator có guard; direct cham_mot_ca/chay_bo_ca vẫn chạy pass/skip, own chỉ bị từ chối sau chạy | **Không**, F08 còn hai helper; không gán lỗi cho ba chế độ CLI đã sửa |
| Cấm cùng code thay cho đoán identity | ca/chay_suite, c5acb70 và correction e3bcaf0 | `python3 -B ../review6/common.py prior.py`; `python3 -B ../review6/common.py old_proofs.py` | Đạt các cửa đã chặn, phạm vi phổ quát còn F08 |
| Không cấm nhầm tập ca cũ | quyết định từ chối code chung | `python3 -B ../review6/common.py claims_extra.py`:347 cũ đủ/riêng code,349 hiện tại; credential18 | Có ở tập hiện hữu |
| Hai ca HEAD lấy nguyên HINT lượt 5, hai mutant mới, sửa neo | `%B` e3bcaf0 | `python3 -B ../review6/common.py claims_extra.py`:băm HINT ef61… khớp;2 AST True; `claim_history.py`:2 tên thêm,1 hàng đổi | Có |
| 5/5 mutant liên quan, t117 qua | `%B` HEAD | `python3 -B ../review6/common.py claims_extra.py`:đúng5 tên liên quan/6 target OWN_SIGNAL, t117 PASS | Có phần chạy lại hiện tại; không tự xác nhận log lịch sử của executor |
| Loại ngoại lệ a, gồm đổi AttributeError thành AssertionError | cham_mot_ca/docstring | `python3 -B ../review6/common.py oracles.py`:sai loại có suffix và SAI; own OK1/1 | Có trên đường registry hợp lệ |
| Neutral nguyên bản/cache/đỏ đóng cổng | runner a/b, ket_luan_mutant | `python3 -B ../review6/common.py oracles.py`; `python3 -B ../review6/common.py extra.py`:1 neutral/2 mutant, đỏ `(1,0)` | Có |
| Giữ all-skip/mixed và giới hạn nền | ket_luan_mutant/runner comments | Cùng hai lệnh trên; full suite đối chiếu BASE:all `(0,1)`,mixed `(0,0)`,4 skip mutant | Có phần đã đo |
| Stdout/headline/LOAI_HONG không là chứng cứ | cham_lap_ca và ee23c44 | `python3 -B ../review6/common.py oracles.py`; `python3 -B ../review6/common.py locks.py`:fake tail thiếu kênh → loi, bỏ fallback guard chết đúng khóa | Có, không suy thành chống initializer giả kênh |
| Identity thật, tiền tố khac | reporter/ee23c44/5548919 | `python3 -B ../review6/common.py old_proofs.py`:cùng tên RuntimeError/AssertionError SAI; `locks.py`:bỏ identity/prefix đúng OWN_SIGNAL | Có |
| Assertion registered ca KHÁC không nhận | chot_tu_ca_khac, ten_do | `python3 -B ../review6/common.py oracles.py`; `python3 -B ../review6/common.py old_proofs.py`:a/b/c loại code khác; factory bị từ chối setup | Có các đối chứng này |
| Thiếu/trùng tên target đỏ | F06/5548919 | `python3 -B ../review6/common.py extra.py`:3 hình `(1,0)` | Có ở product |
| Credential đúng tệp/dòng assert/kiểu | la_chot_cua_suite/docstring | `python3 -B ../review6/common.py oracles.py`; `python3 -B ../review6/common.py locks.py`:same-line tệp khác bị loại, bỏ từng check đúng khóa đỏ | Có |
| chay_suite gọi classifier thực, khóa không tìm source | chay_suite/F03 và khóa sửa | `python3 -B ../review6/common.py locks.py`:thay câu thực thi, giữ comment OWN_SIGNAL | Có |
| 11 mutant fixture/assertion được sửa | r01,r10,t115 và3 ca đổi assert | `python3 -B ../review6/common.py historical.py`:10 OK;1 neutral OSError | Khớp10;1 KHÔNG ĐO ĐƯỢC |
| r13 không gọi registered t70, alias duy nhất lịch sử | helper/7df242e | `python3 -B ../review6/common.py claims_extra.py`:alias return duy nhất ở5548919 đúng r13→t70; `extra.py`:hai ca hiện tại riêng đều giết1/1 | Có |
| Bố cục bản sao và dependency của harness | _dung_cay_harness/c73dff3/c5acb70 | `python3 -B ../review6/common.py locks.py`:28 target đúng chốt gồm N13 và nạp credential | Có phần dependency được chạy, không khai sao toàn bộ kho |
| Mọi installer/N13 HOME/init nằm trong fixture | N13 code/comment | `python3 -B ../review6/common.py fixture.py`:HEAD0 ambient,3 bước Bash cùng env sạch; npm trước chuan-bi | Có hướng đo được |
| Mỗi chốt đăng ký có mutant đúng target | bảng wp1079/comment | `python3 -B ../review6/common.py locks.py`:25 mutant,28/28 OWN_SIGNAL, trace có target và không registered-other | Có với chốt đã đăng ký; chưa khóa hai helper, xem F08 |
| 5368c34 bỏ phép trừ và correction F05/F08; F09 | messages5368/c5ac/e3bc | `python3 -B ../review6/common.py claim_history.py`:3 ca/2 mutant F08 cũ gỡ,2+2 mới c5ac;HEAD thêm2+2; correction rõ câu sai và4 thay5 | Git/count/correction khớp; phạm vi “mọi điểm vào” còn F08 |
| Nonce có giới hạn module trước main | cham_lap_ca docstring/nợ1117 | `python3 -B ../review6/common.py old_proofs.py`:phản chứng cũ vẫn OK giả; receiver không đổi,main chỉ thêm registry | Giới hạn khai đúng, không tính lại nợ |
| Các số531/536,538/539,541/543; session/model/owner/CI của executor | toàn messages9 commit packet | `python3 -B ../review6/common.py audit.py`; `python3 -B ../review6/common.py claim_history.py`:kiểm source/tập ca/mutant/correction; thiếu rig/log/check-run độc lập lịch sử | KHÔNG ĐO ĐƯỢC các số/identity/CI lịch sử |
| Claim spec/land/approval của25 commit master/merge | toàn `%B BASE..HEAD` | `python3 -B ../review6/common.py audit.py`:đủ inventory OID/path/message; không mạng/không thực thi packet ngoài scope | Git inventory đo được; vận hành ngoài packet KHÔNG ĐO ĐƯỢC |

## BANG TEST

| Bộ / lệnh thực qua suites.py | N/M / output | Bỏ qua / phần chưa đo |
|---|---|---|
| HEAD `python3 .claude/dev/launcher_test.py` | **315/339** ca đã chạy qua; tổng349,24 đỏ; rc1 | **10 BO QUA**:2 Windows-only +8 venv/pip offline |
| BASE cùng lệnh qua `suites.py base` | **296/320**; tổng330,24 đỏ; rc1 | Cùng10 tên/lý do skip; tập24 tên đỏ bằng HEAD |
| HEAD `python3 .claude/dev/launcher_test.py --dot-bien` | **511/547**, rc1; tổng551;36 SAI đều `neutral do`, không cấp tín dụng | **4 KHÔNG ĐO ĐƯỢC** theo nền, đúng tập BASE |
| BASE cùng lệnh qua `suites.py base` | **522/522**, rc0; tổng526 | 4 không đo theo nền; bộ chấm cũ còn nhận lỗi vô can, số xanh này không chứng minh mutant bị đúng assertion giết |
| HEAD `python3 .claude/dev/codex_cred_test.py` | Nền **13/18**, `TỔNG: ĐỎ`, rc1 | 5 đỏ,0 skip; không chạy vòng mutation chính |
| BASE cùng lệnh qua `suites.py base` | Nền **13/18**, `TỔNG: ĐỎ`, rc1 | Cùng5 tên lỗi gốc; bộ chấm cũ không in suffix loại |
| Khóa wp1079 hiện có / `prior.py` | **19/19 PASS** | 0 skip trên POSIX này |
| Mutant gỡ chốt / `locks.py` | **28/28 OWN_SIGNAL**,25 mutant; trace đúng ca đích | 0 skip |
| Credential từng mutant / `extra.py` | **13 OWN_ASSERTION/18**,5 NEUTRAL_BLOCKED | Không nhận5 bị chặn thành kill; không thay gate |
| Hai khóa mới / `make_hint.py` | HEAD **2 OWN_SIGNAL**; prototype **2 PASS**; gỡ từng guard đúng khóa OWN_SIGNAL | Scratch ngoài kho; chưa full regression prototype |

`ls -ld /tmp/.git` xác nhận thư mục `dr-xr-xr-x` hiện hữu. Không xóa, đổi quyền hoặc sửa sandbox. Cùng tập24 tên đỏ/10 tên+lý do skip ở BASE và HEAD; thêm349−330=19 khóa r1079 đều PASS. Log còn chỉ rõ `/var/tmp` read-only ở2 ca và thiếu CLI ở t53; các lỗi storage/materializer/run nối tiếp đều có ở BASE. A1 yêu cầu `/tmp/.git` vắng nên **KHÔNG ĐO ĐƯỢC điều kiện chuẩn**, không đọc các lỗi này thành hồi quy hoặc gọi gate xanh.

10 launcher skip:2 Windows-only (`t62`, `r484_g4_windows_sid_alias_identity`) +8 venv/pip offline (`r345_*`4, `r347_*`2, `r348_*`2). Credential có5 đỏ nền và0 skip; dừng trước vòng mutation chính. Phép đo bổ sung từng mutant credential (`extra.py`) chỉ xác nhận13 OWN_ASSERTION và5 NEUTRAL_BLOCKED; không thay thế gate đầy đủ. 4 mutant không đo theo nền được liệt kê nguyên văn trong [summary.json](review6/summary.json).

## BANG SAN

| Hướng độc lập | Lệnh từ cay-kho/ | Output thật | Phân loại |
|---|---|---|---|
| 1. Toàn vẹn/spec/diff/scope | `python3 -B ../review6/common.py audit.py` | DIFF_MATCH True,769 dòng,2 tệp,HEAD/tree đúng,status rỗng | KHÔNG PHẢI LỖI |
| 2. Registry main/decorator/runner | `python3 -B ../review6/common.py prior.py` | 19 PASS;CA cùng code ValueError;349/349 riêng code | KHÔNG PHẢI LỖI ở các cửa đã vá |
| 3. Registry hai API gọi ca trực tiếp | `python3 -B ../review6/common.py entrypoints.py` | pass:cham `qua`,batch1/0/[];skip vẫn chạy;own ValueError sau calls[target] | **LỖI F08** |
| 4. Tín dụng giả product/đổi kiểu | `python3 -B ../review6/common.py oracles.py` | attribute/wrapped/implementation AssertionError SAI;own OK1/1 | KHÔNG PHẢI LỖI các đối chứng |
| 5. Harness lớp giả/stdout giả | `python3 -B ../review6/common.py old_proofs.py`; `python3 -B ../review6/common.py oracles.py` | fake RuntimeError/AssertionError cùng tên `(1,0)`;fake tail không kênh loi | KHÔNG PHẢI LỖI |
| 6. Credential tệp khác/cùng dòng assert | `python3 -B ../review6/common.py oracles.py` | same-assert-line khác tệp bị loại;wrapped/impl/other có suffix;own{t2} | KHÔNG PHẢI LỖI phần đo được |
| 7. Chặn nhầm kill thật | `python3 -B ../review6/common.py oracles.py`; `python3 -B ../review6/common.py extra.py` | own a/b OK1/1;c{t2};r13/t70 mỗi ca riêng OK1/1;347 ca cũ không code trùng | KHÔNG PHẢI LỖI trong registry hợp lệ đã đo;F08 là thực thi registry bị cấm |
| 8. Neutral/cache/all-skip/mixed | `python3 -B ../review6/common.py oracles.py`; `python3 -B ../review6/common.py extra.py` | neutral đỏ `(1,0)`;cache1+2;all `(0,1)`,mixed `(0,0)` | KHÔNG PHẢI LỖI |
| 9. Target thiếu/trùng tên | `python3 -B ../review6/common.py extra.py` | all/partial/duplicate `(1,0)` | KHÔNG PHẢI LỖI F06 cũ |
| 10. Cha thù địch N13/installer/init/HOME | `python3 -B ../review6/common.py fixture.py` | BASE7 installer+2init;HEAD0/0;npm trước chuan-bi | KHÔNG PHẢI LỖI ở HEAD |
| 11. Hậu điều N13 trên fixture BASE | `python3 -B ../review6/common.py fixture_base_lock.py` | OWN_SIGNAL,9 marker ambient,trace N13+bang | KHÔNG PHẢI LỖI: phản chứng dương |
| 12. Gỡ từng chốt wp1079 | `python3 -B ../review6/common.py locks.py` | TOTAL28 OWN_SIGNAL28,25 mutant | KHÔNG PHẢI LỖI với chốt đăng ký |
| 13. Scorer mới/ca BASE và11 mutant SPEC | `python3 -B ../review6/common.py historical.py`; `python3 -B ../review6/common.py legacy.py` | 397OK/34neutral/11SAI/4skip;SPEC10OK/1neutral;BASE nhận AttributeError cả3 đường | Lỗi gốc được tái hiện/vá ở phần đo được;1 storage KHÔNG ĐO ĐƯỢC |
| 14. Khóa hai helper và hướng sửa | `python3 -B ../review6/common.py make_hint.py` | HEAD2 OWN_SIGNAL;prototype2PASS;remove-single/remove-batch đúng khóa OWN_SIGNAL;19 khóa cũ PASS;dry-run0 | **LỖI F08**, có đối chứng hướng sửa |
| 15. Kênh giả trước main | `python3 -B ../review6/common.py old_proofs.py` | forged channel `(0,0)`;receiver/main-ngoài-guard không đổi | Nợ #1117 đã nhận, không là finding mới |
| 16. Lời khai Git/provenance/count | `python3 -B ../review6/common.py claim_history.py`; `python3 -B ../review6/common.py claims_extra.py` |9 commit packet;4 thêm/3 sửa ở5548919;5 mutant HEAD liên quan;HINT băm/AST khớp | KHÔNG PHẢI LỖI phần Git;CI/identity lịch sử KHÔNG ĐO ĐƯỢC |
| 17. Gate đầy đủ và môi trường | `python3 -B ../review6/common.py suites.py head`; `python3 -B ../review6/common.py suites.py base`; `python3 -B ../review6/common.py summarize.py` | HEAD315/339,511/547,13/18;BASE296/320,522/522,13/18;cùng24 tên đỏ/10skip;36 mutant HEAD đều neutral đỏ | Gate chuẩn KHÔNG ĐO ĐƯỢC;không dùng lỗi nền làm finding |

### F08-shared-code-khong-phai-ca-khac [P1] Hai hàm gọi ca trực tiếp vẫn thực thi CA bị cấm trước khi kiểm registry

TEP/DONG: `.claude/dev/launcher_test.py:188` (`cham_mot_ca`; gọi fn tại194 trước mọi kiểm registry), `:14876` (`chay_bo_ca`; gọi fn tại14889). `kiem_registry` tại58 khai bao “mọi điểm vào chạy ca”, nhưng chỉ được gọi ở decorator68, classifier178, runner14601 và main15007. `%B` HEAD cũng dùng phạm vi “moi diem vao chay ca”.

VAN DE: Với registry `CA=[target,alias]` có chung `__code__`, direct `chay_dot_bien` và CLI đã từ chối đúng trước khi chạy. Nhưng hai helper thực thi ca được dùng trực tiếp trong chính suite (`chay_bo_ca` dùng ở t99 và ca kiểm headline; `cham_mot_ca` dùng ở các meta-test) vẫn bỏ qua preflight. Nếu target pass hoặc skip, `chot_tu_ca_khac` không được gọi, nên registry bị cấm được chạy và trả kết quả bình thường. Nếu target ném own signal, validator trong classifier mới nổ ValueError **sau khi thân ca đã chạy**. Đó không phải chính sách từ chối trước thực thi đã được dùng để đóng F05/F08. Đây là khoảng hở phạm vi của cùng finding, không đòi hỗ trợ lại factory bị chủ kho cấm và không khẳng định tín dụng giả ở ba chế độ CLI đã sửa.

DA THU NGHIEM:

- `python3 -B ../review6/common.py entrypoints.py` → `pass cham_mot_ca result ('qua','review_target') calls ['review_target']`; `pass chay_bo_ca result (1,0,[]) calls ['review_target']`; batch cả hai trả `(2,0,[])`, calls target+alias. Skip trả lần lượt `('bo_qua',...)`, `(0,1,[])` sau khi target đã chạy. Own ở cả hai chỉ ValueError sau calls `['review_target']`. AST xác nhận không có guard ở hai hàm.
- `python3 -B ../review6/common.py make_hint.py` → hai khóa mới `r1079_review6_{cham_mot_ca,chay_bo_ca}_kiem_registry_truoc_chay` đều **OWN_SIGNAL** trên bản sao HEAD; trace có chính hàm khóa, helper kiểm và bang, không registered-other. Không dựa vào FileNotFoundError, neutral đỏ hay stdout.
- Prototype chỉ thêm preflight `kiem_registry(CA)` trước khi gọi ca ở hai hàm, trên bản sao ngoài kho: **2/2 PASS**, cả pass/skip/own bị từ chối trước marker. Gỡ guard single chỉ khóa single OWN_SIGNAL; gỡ guard batch chỉ khóa batch OWN_SIGNAL. **19/19** khóa r1079 hiện có vẫn PASS trên prototype. Chưa khai prototype là bản vá đã qua full regression.

DO TIN: cao — direct API thật, marker trơ chứng minh thứ tự, hai ca khóa đúng nguyên nhân và phép gỡ guard độc lập. Không cần credential, mạng, storage hoặc Windows. 347 ca cũ/349 ca hiện tại đều code riêng; không có bằng chứng validator cấm nhầm ca hiện hữu. P1 theo PROMPT cho sai hành vi/phạm vi khẳng định sai đo được; không tách thêm P2 cho ca khóa thiếu cùng đường này.

Gợi ý vá: đặt validator chung tại các consumer thực sự gọi ca **trước** mọi fn/nhật ký/side effect; bao cả direct `cham_mot_ca` và `chay_bo_ca`, giữ guard sớm ở main/runner/decorator. Kiểm toàn bộ registry CA đang dùng, không chỉ tập target đã lọc. Giữ helper không đăng ký được meta-test gọi và giữ chế độ lặp hợp lệ; không cấm list lặp của cùng ca vì nhầm nó là registry. Giữ các đối chứng own/other khác code, neutral/cache, skip, target thiếu/trùng tên, r13/t70/helper. Mỗi điểm nối guard cần mutant bỏ chính điểm nối làm đúng ca khóa đỏ. Không dùng phép trừ code đã mở lại F05. Nếu hai helper thực sự không thuộc hợp đồng registry thì phải có ranh giới được SPEC/authority cho phép và lời khai thu hẹp có căn cứ; hiện cả code docstring lẫn nhiệm vụ review yêu cầu kiểm mọi đường chạy ca.

[HINT.patch](HINT.patch) là **test-only**, `patch -p0` từ `cay-kho/`, chứa hai khóa và helper của chúng; không chứa bản vá runner. Nhãn: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Đã dry-run rc0 trên bản sao exact HEAD và chạy phản chứng ở trên. SHA256: `68ff2f0f82a88be22545096dcf609f4afb1ee8dc1aeec7bb1c86adb981ced4a6`.

## Toàn vẹn cuối

`python3 -B ../review6/common.py summarize.py` → **10161/10161 tệp tracked giữ nguyên**, added=[], removed=[], changed=[]; `git status --porcelain` rỗng; HEAD/tree vẫn exact SHA/tree ở đầu verdict. Bằng chứng máy: [integrity-final.json](review6/integrity-final.json). Các lệnh test hoàn tất với rc thật trong [head-suites.json](review6/head-suites.json) và [base-suites.json](review6/base-suites.json); [summary.log](review6/summary.log) xác nhận `FAILED_NAMES_EQUAL True`, `SKIPS_EQUAL True`, 36/36 mutant SAI của HEAD đều neutral đỏ.

Nhật ký tăng dần gốc được giữ tại [verdict-progress.md](review6/verdict-progress.md). Các log và script phản chứng mới đều ở `review6/`. Không sửa cây review, không push, không gọi mạng hoặc dùng credential thật. Verdict chặn dựa vào F08 hai direct helper; lỗi môi trường, trần đã nâng và nợ #1117 không tính vào số finding.
