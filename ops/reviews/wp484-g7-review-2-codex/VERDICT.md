Reviewed commit: b355ff8b3d081c8b64ce803f53a4a09216411a29
Spec SHA-256: 4a512dd38721c3c4eec7978489ba06485feab32f94a0c5637a085d6c694ba38c
verdict: changes_requested
P0=0 P1=0 P2=2 P3=0

Chưa approve: còn G01/P2 (một lối bootstrap thuộc lớp F04 chưa được phủ) và G02/P2 (hồi quy của fixture test shell trong lượt vá 2). Hai mục này chưa có quyết định chấp nhận của chủ kho. F01 và nợ CAS đã có quyết định trong r8/r7, không tính vào hai finding mở. Đây là lượt Codex 2/2; cần chuyển checkpoint theo chỉ thị, không gọi lượt ba để tiếp tục vòng vá hiện tại.

Đã tự đo HEAD/tree, băm cả hai spec và bản verdict lượt 1; đều khớp chỉ thị. Tree: `812a7fcc3038c625077a1dbd992ced1e6174185d`. Đã đọc r7+r8, verdict lượt 1, handoff, diff lượt vá 2 và các đường gọi liên quan trong diff so base `653fef3f52f3130dd6f597c1036430ffb807fef1`. Delta lượt vá 2 đúng 7 tệp, +315/−44, trong write set r8.

Reviewer: Codex/OpenAI, công cụ shell thực thi trực tiếp qua API/cloud, transport `machine`; không dùng context executor. Không có telemetry để tự xác nhận model ID/effort hoặc receipt assurance. Môi trường Linux, Python 3.13.16, Ruff 0.17.1, actionlint 1.7.7, sandbox workspace-write, không escalation. Chỉ chạy suite trên bản sao `review-copy`; base và mọi mutant ở cây riêng. Không dùng credential thật, không đăng nhập, không chạy Codex LIVE, không gửi comment hay thao tác GitHub.

## ĐỐI CHIẾU LƯỢT TRƯỚC — F01–F04

Các lệnh dưới chạy từ thư mục ra. `R` = `python -B run_clean.py`; `C <mode>` = `R python -B ../review_checks.py <mode>`. Runner đặt HOME/USERPROFILE/CODEX_HOME/TMPDIR tạm, dùng env allowlist, không truyền token phiên. Store bộ nhớ chỉ thay biên storage bị môi trường chặn; parser, identity, recovery state và logic gọi thật vẫn được chạy.

| Finding lượt 1 | Kết luận | Phép đo trên head mới |
|---|---|---|
| F01 — state không ghi được | **ĐÓNG THEO QUYẾT ĐỊNH CHỦ KHO** | `C retry` rc=0: cả launcher, `cmd_kiem`, materializer đều báo riêng lỗi ghi state và trả thất bại. Mỗi lối gọi hai lần, probe_calls=2; materializer giữ auth cũ. Đây chính là giới hạn đã được r8 chấp nhận, không còn đòi lần sau không probe. [retry.log](retry.log). |
| F02 — mất `token_invalidated` | **ĐÃ ĐÓNG** | `C rejection` rc=0: với rc=1 và rc=0+marker stdout+`token_invalidated` stderr, đều `rejected=True recorded=True next_blocked=True probe_calls=1`. Chạy helper `_kiem_song` thật với child giả; giữ state logic thật. Mutant bỏ chữ ký chết ở assertion. [rejection.log](rejection.log). |
| F03 — probe A nhưng ghi từ chối B | **ĐÃ ĐÓNG trong phép đo và hợp đồng r8** | `C rejection_race` rc=0: cả launcher và `cmd_kiem`: `A_rejected=True B_rejected=False B_blocked=False`. Production chỉ có một call `_danh_dau_auth_hong` trực tiếp trong launcher tại dòng 3216, truyền `da_probe`; call trong `codex_cred.py:524` truyền `raw`. Materializer dùng identity candidate đã lấy trước probe, không đánh dấu bằng cách đọc lại auth hiện tại. Hai mutant đọc lại đều chết ở assertion. [rejection_race.log](rejection_race.log). |
| F04 — bootstrap chết trước cài CLI | **CHƯA ĐÓNG hết lớp; ca vắng CLI lượt 1 đã đóng** | `C bootstrap`, `C bridge_branches` rc=0 và hai ca F04 của kho đạt 1/1: shell cài CLI trước materialize; bridge hoãn khi CLI vắng, hook lỗi thì không prepare. Nhánh có CLI dùng thứ tự cũ `prepare → child → child`. Tuy nhiên executable tồn tại nhưng không chạy được vẫn chết trước installer: **G01** bên dưới, cùng lớp F04, chỉ đếm một finding. [bootstrap.log](bootstrap.log), [bridge_branches.log](bridge_branches.log). |

F03 còn fallback `da_probe=None` khi lần đọc trước probe không thực hiện được, rồi marker có thể đọc lại. R8 MT9 nói tường minh “đọc không được ⇒ hành vi cũ”; không nhận bản vá là đã loại bỏ mọi race quanh lúc CLI mở/đổi tệp. Không có callsite production thứ ba bỏ tham số ngoài fallback đó trong các đường đã quét.

## Finding mở

### G01 — P2 — Bridge dùng “có executable” để quyết định bỏ qua đường sửa CLI hỏng

- Lớp: `codex-bootstrap-probe-before-install`, tiếp nối F04; không đếm F04 thêm lần nữa.
- Vị trí: `.claude/hooks/session_start.py:124`, `:126`; đối chiếu `.claude/hooks/session-start.sh:151` (`co_chay codex`, có kiểm chạy thật).
- Điều kiện: remote có auth cũ và snapshot mới cần probe; PATH có một executable `codex` nhưng nó không chạy được, ví dụ shim/node/runtime lỗi và trả 127. `shutil.which` vẫn tìm thấy nó. Bridge materialize ngay; probe thất bại, trả 13 trước khi tìm bash, nên shell không được chạy tới nhánh cài lại CLI. Shell trực tiếp biết kiểm `--version` và đi tới npm. Đây là lối còn sót của lớp F04 trong toàn PR; không gọi nó là lỗi mới chỉ do delta lượt 2 sinh ra.
- **PHÉP ĐO:** `C broken_cli` rc=0 (runner/assertion độc lập). Dùng bridge, materializer và helper probe thật, CLI inert trả 127, thay riêng storage bằng store theo home:
  ```text
  existing broken CLI: which_found=True probe_rc=127 bridge_rc=13 shell_reached=False npm_repair_reached=False
  materializer reason= CHƯA ĐO ĐƯỢC probe; giữ nguyên credential cũ, chưa kết luận auth hỏng
  ```
  Đối chứng `C bootstrap` rc=0 chạy shell nguyên bản với installer giả và executable hỏng ban đầu:
  ```text
  shell-broken: rc=0 final_new_auth=True child_env_clean=True events=['npm install -g @openai/codex', 'prepare', 'credential-status:INERT-NEW', 'codex login status', 'doctor:INERT-NEW']
  ```
  [broken-cli.log](broken-cli.log), [bootstrap.log](bootstrap.log). Đối chứng shell thay biên launcher/materializer bằng fixture, không tuyên bố đã cài/promote với CLI hoặc storage thật.
- **HINT:** sửa quyết định hoãn ở bridge để trường hợp CLI có mặt nhưng không dùng được cũng tới được bước sửa công cụ, đồng thời giữ snapshot khỏi môi trường mọi child. Ca khóa: executable có thật, `--version`/probe thất bại; installer giả phải được gọi trước probe/promote, auth cũ giữ khi sửa/probe hỏng. Rủi ro bản vá: thêm probe trước khi scrub có thể truyền snapshot vào child; retry/hoãn thiếu phân loại có thể che lỗi credential thật. Không cần và không đính patch runtime cho packet sensitive.

### G02 — P2 — Fixture scrub shell mới chạy installer ngoài fixture và timeout khi thiếu Codex

- Lớp: `hook-scrub-test-unisolated-bootstrap` — hồi quy do chính lượt vá 2.
- Vị trí: `.claude/dev/launcher_test.py:7516`, `:7522`, `:7529` trong `r484_g2_hook_shell_scrub_truoc_probe`.
- Shim mới `exec` Python thật cho các lệnh `-c`, fixture giữ PATH bên ngoài. Vì materialize đã dời xuống, `co_chay` nay đi qua nhánh `npm install -g @openai/codex` trước điểm đo, và có thể tiếp tục các installer khác. Ca kiểm scrub phụ thuộc CLI/mạng/quyền cài đặt của máy chạy. Bản cũ cố ý dừng ở biên Python trước installer. Trên sandbox có npm nhưng không Codex, full suite đã timeout đúng ca này ở 30 giây, trước khi storage guard trở thành yếu tố quyết định.
- **PHÉP ĐO:** `R python -B ../review_test_teeth.py previous`, `... positive`, `... slow-installer`, từng runner rc=0. Replay ca cũ+hook cũ từ `99e79b1` và ca mới+hook mới, thay materializer bằng fixture để loại nhiễu `/tmp/.git`, chỉ thay công cụ cài đặt bằng spy inert:
  ```text
  shell previous: PASS (materializer storage seam)
  shell previous: installer_calls=[]
  shell positive: PASS (materializer storage seam)
  shell positive: installer_calls=['install -g @openai/codex']
  shell slow-installer: TimeoutExpired, elapsed=30.1s
  shell slow-installer: installer_calls=['install -g @openai/codex']
  ```
  Installer giả chờ 31 giây; ca nguyên bản có timeout=30 nên thất bại, không gọi installer thật trong phép đối chứng. [teeth-previous.log](teeth-previous.log), [teeth-positive.log](teeth-positive.log), [teeth-slow.log](teeth-slow.log). Full suite độc lập cũng ghi `HONG r484_g2_hook_shell_scrub_truoc_probe: TimeoutExpired ... after 30 seconds` tại [launcher-suite.log](launcher-suite.log).
- **HINT:** cung cấp đầy đủ CLI/installer giả trong PATH của fixture để hook không dùng npm/installer máy chủ; installer spy vẫn phải kiểm môi trường sạch. Giữ kiểm materializer đúng một lần, không child Python bẩn, có child sau materializer, auth đúng và không in snapshot. Ca khóa phải đạt khi PATH máy chủ không có Codex và mạng không sẵn; mutant giữ snapshot hoặc đảo thứ tự vẫn phải đỏ. Rủi ro: stub quá rộng có thể che chính đường rò env hoặc bỏ mất điểm đo sau materializer.

## Thứ tự và sức phân biệt của các test đã sửa

- Shell trực tiếp: `npm → prepare → credential-status(new) → login status → doctor(new)`. Bridge thiếu CLI: `npm → credential-status(old) → login status → doctor(old) → prepare`. **Đã đo** việc các probe dưới shell chạy trước materialize ở nhánh hoãn của bridge; đây là hệ quả của MT12/N14 r8, không khẳng định bridge giữ thứ tự của shell trực tiếp/master. Fixture kết thúc có auth mới và shell rc=0; chưa có bằng chứng về một lỗi chức năng riêng khác từ thứ tự này. Không mở finding chỉ từ suy đoán; không coi output doctor trước prepare là bằng chứng cho snapshot mới.
- Snapshot thô không đến shell ở cả hai nhánh bridge đã đo; installer/codex giả không thấy `CODEX_AUTH_JSON` hoặc `TL_CODEX_SNAPSHOT`. Shell trực tiếp chỉ cấp snapshot cho materializer. Nhánh có Codex của bridge vẫn `prepare → bash --version → hook`; lỗi prepare vẫn chặn trước child. Đây là phép đo biên env/fixture, không phải chứng minh mọi child có thể tồn tại đều sạch.
- Test shell đổi từ rc=97 sang nhật ký **vẫn có răng cho scrub**: `review_test_teeth.py leak` bỏ `unset CODEX_AUTH_JSON` trên hook bản sao ⇒ assertion của ca bắt lỗi (`TinHieuChotCa`, lớp assertion), runner rc=0 xác nhận phản chứng; không chết vì storage. Nới mã thoát riêng lẻ không đủ để gọi nó mất răng, vì các assertion nhật ký/auth vẫn còn. Lỗi mới là G02.
- `r484_g2_bridge_scrub_va_chot_remote` ghim `shutil.which` để đo nhánh có CLI là đúng phạm vi; chính ca đạt 1/1. Nhánh thiếu CLI có ca riêng và mutant bỏ hoãn chết ở assertion thứ tự. Hai giá trị `which=None`/có path không phủ executable hỏng G01.
- `bash_nen.tim_bash()` không biến việc thiếu bash thành skip: phản chứng `review_test_teeth.py resolver` trả `(None, ...)` ⇒ `assertion=True skipped=False`. Cổng `cong_cu_test` thực chạy đạt; không chỉ kiểm số chữ `bash` bằng đọc mã.
- Inventory tự trích AST/lịch sử: master 197 ca/233 mutant +4 harness; `faaedff` 197/178 +3; lượt 1 216/246 +4; head mới 220/248 +4. Không mất tên cũ, không trùng tên, mỗi bảng chỉ một phép gán. [inventory.log](inventory.log). Số 218 của executor là số chạy sau hai skip nền, không phải 218 ca đăng ký.

## Bảng hướng thử

| Hướng thử | Lệnh / log | Output đo được | Kết luận |
|---|---|---|---|
| Ghi state hỏng ở cả 3 lối | `C retry` | 3 lối báo riêng; mỗi lối probe=2 | Đúng r8; F01 theo quyết định |
| Từ chối thắng rc0+marker | `C rejection` | cả rc1/rc0 ghi state, lần sau chặn | F02 đóng |
| Probe A, thay B trước ghi state | `C rejection_race` | A=True, B=False, B_blocked=False ở cả 2 lối | F03 đóng trong seam |
| Thiếu CLI hoàn toàn | `C bootstrap`; ca F04 1/1 | npm trước prepare, cuối có auth mới | Ca F04 lượt 1 đã vá |
| CLI có executable nhưng không chạy | `C broken_cli` | bridge13, shell/npm chưa tới | G01/P2 |
| Snapshot tới installer/shell | `C bootstrap`, `C bridge_branches` | env_clean=True trong các nhánh đã đo | Không thấy rò trong fixture |
| Probe dưới shell trước prepare ở bridge | `C bootstrap` | status(old), doctor(old), prepare | Khác thứ tự; đúng cách hoãn MT12, không nhận health mới |
| Fixture mới tự gọi installer | `review_test_teeth.py previous/positive/slow-installer` | cũ 0 call; mới gọi npm, timeout30.1s | G02/P2 |
| Nhật ký scrub còn bắt mutant | `review_test_teeth.py leak` | assertion sau bỏ unset | Có răng, đo bằng seam materializer |
| Resolver bash vắng bị tha | `review_test_teeth.py resolver` | assertion=True skipped=False | Không bị nới thành skip |
| Merge mất ca/mutant | Trích AST ở `inventory.log` | missing=[], duplicates=[] | Không thấy mất mục |
| Đọc lại trước replace có tác dụng | `C cas_unit`; `cas-mutants.log` | head giữ concurrent; mutant ghi đè, assertion | Thu hẹp đúng; chưa CAS |
| Lint/gate tăng nợ | Ruff F + doctrine/adr ở head/base | F841 5→5; doctrine0→0; adr0→0 | N8/N9 không tăng nợ |
| Quy tắc void/checkpoint | `R python -B .claude/dev/packet_loop_test.py` | 343/343 +1 skip; TỔNG ĐẠT | Đạt trong phạm vi suite |

## Đã đo

- Tạo `VERDICT.md` sơ bộ trước khi chạy suite, sau đó cập nhật; các script và log nằm cùng thư mục ra để tái lập. `review_checks.py`, `review_mutants.py`, `review_test_teeth.py` đều là artifact review, không phải bản vá giao executor áp vào runtime.
- `C retry`, `C rejection`, `C rejection_race`, `C bridge_branches`, `C bootstrap`, `C broken_cli`, `C storage`: runner rc=0 sau hoàn chỉnh seam. Các thử đầu dựng seam thiếu `MAX_BYTES` bị AttributeError đã sửa trong script reviewer, không tính là kill hoặc finding.
- Các ca kho `r484_g7_bridge_vang_codex_hoan_materialize_sau_hook`, `r484_g7_hook_vang_codex_cai_cli_truoc_materialize`, `r484_g2_bridge_scrub_va_chot_remote`: chạy `--lap-ca <tên> --lan 1`, mỗi ca rc=0, 1/1. Logs `bridge-case.log`, `hook-case.log`, `bridge-present-case.log`.
- `R python -B ../review_mutants.py`: rc=0, **9 mutant chết bằng assertion đích**, positive controls rc=0. Mỗi bản sao/thử một tiến trình, `-B`, `PYTHONDONTWRITEBYTECODE=1`. Năm mục launcher g7 lấy nguyên mỏ neo từ `DOT_BIEN`; thêm F02, F03 ở `codex_cred`, và hai mutant tay F04. Ba mutant liên quan storage dùng phép đo độc lập: F01 materializer, F03 và CAS. Không khai đã tái lập ca storage tích hợp của executor. [independent-mutants.log](independent-mutants.log).
- CAS được đo lại bằng dirfd/read/write thật, chỉ bỏ constructor bị guard môi trường chặn: ghi concurrent tại seam fsync tệp tạm trước promotion. Head giữ concurrent; mutant `g7_bo_doc_lai_truoc_replace` chết với `AssertionError: concurrent credential overwritten`, không lỗi setup. Positive và mutant con rc=0/1; runner rc=0. [cas-mutants.log](cas-mutants.log).
- Full launcher **không snapshot**: rc=1, **197/210 chạy đạt, tổng 220, skip10, fail13**. Mười một ca fail liên quan storage/recovery bị guard `/tmp/.git`; một ca `t53` thiếu CLI thật trong PATH đã cô lập; một ca timeout là G02, được tách khỏi nhiễu storage bằng đối chứng riêng. Với `CI=true`, chỉ đo lại t53: rc=0, 1/1, xác nhận yếu tố môi trường. [launcher-suite.log](launcher-suite.log), [t53-ci-control.log](t53-ci-control.log).
- Full launcher **có snapshot inert** cũng in **197/210, tổng220, skip10, fail13**, cùng tập ca thất bại. [launcher-suite-fake.log](launcher-suite-fake.log). Không thu được mã thoát trực tiếp của lượt này do chỉ giữ stdout ở lần tool yield; không dùng nó làm bằng chứng rc hay pass. Canary riêng có snapshot: rc=0, 1/1, [fake-canary.log](fake-canary.log).
- Full `codex_cred_test.py`: rc=1, **13/18**, năm ca t6/t9/t15/t16/t18 fail setup/storage dưới `/tmp`; phase mutation của suite không chạy. Bản chi tiết xác nhận thông báo guard hoặc rc2 thay vì rc3 ở nửa ca home đã tồn tại. Không coi đây là lỗi sản phẩm. [codex-cred-suite.log](codex-cred-suite.log), [codex-cred-detail.log](codex-cred-detail.log).
- `R python -B .claude/dev/packet_loop_test.py`: rc=0, nền **343/343**, một skip `luong_canonical_chay_that` cần pwsh/Windows, TỔNG ĐẠT. Bảng có 344 ca, 106 mutant, 78 lớp lách, 35 ca bắt oan; mutant gắn ca nền Windows bị bỏ qua được log riêng. [packet-loop.log](packet-loop.log).
- `CONG_CU_TEST_BAN_KINH=manh` được runner đặt cho `R python -B ops/cong_cu_test.py`: rc=0; **56 ca**, cổng cây thật ĐẠT, tự kiểm giàn giáo/parallel ĐẠT, không tiền kiểm skip. **470 mutant giao job mảnh, không chạy đủ 470 trong tiến trình này**. [cong-cu.log](cong-cu.log).
- Ruff F no-cache, năm tệp Python sửa tay, head/base đều rc=1, cùng năm F841 trong `launcher_test.py`, delta=0; bốn tệp còn lại 0. [ruff-head.json.log](ruff-head.json.log), [ruff-base.json.log](ruff-base.json.log).
- `packet_loop.py doctrine-scan --root .` và `adr-song --root .`: head/base mỗi lệnh rc=0. Doctrine 10 tệp/0 chỗ; ADR50/50, cùng ngoại lệ0016. Logs `doctrine-{head,base}.log`, `adr-{head,base}.log`.
- `R bash -n .claude/hooks/session-start.sh`: rc=0. `R /root/.local/bin/actionlint -shellcheck= .github/workflows/launcher-windows.yml`: rc=0, không output. Lần gọi actionlint bằng tên trần không tìm thấy trong PATH allowlist; đã dùng đúng executable có sẵn, không cài mới. Đây là kiểm tĩnh, không phải CI Windows hoặc ShellCheck.
- Audit cuối kho được review: HEAD/tree đúng, status kể cả ignored/untracked, diff HEAD, diff cached và hai danh sách ngoài index đều rỗng, tất cả rc=0; băm spec/verdict1 khớp. [checkout-final.log](checkout-final.log). Hook marker phát sinh trong bản sao review, không trong KHO. Không sửa mã, checkout, hay mutant trong KHO.

## KHÔNG ĐO ĐƯỢC

- Storage tích hợp: `/tmp/.git` rỗng lại tồn tại trong sandbox. `C storage` xác nhận `OSError: Codex home is inside a repository`; không xóa guard hoặc sửa `_KhoCodex` để biến suite thành xanh. Các seam không chứng minh kernel guard, quyền, ACL hoặc chống race toàn hệ thống.
- Chưa tái lập claim executor launcher218/218 hoặc codex_cred18/18+18/18. Không dùng các fail setup để phủ nhận claim ở môi trường executor. G02 có phản chứng riêng không phụ thuộc setup ấy.
- Mười skip launcher: hai theo nền (`t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`, `r484_g4_windows_sid_alias_identity`); tám do không dựng được venv/pip: bốn ca `r345_*`, hai ca `r347_*`, hai ca `r348_*` được liệt kê đầy đủ trong hai log suite.
- Không chạy toàn bảng `launcher_test.py --dot-bien`, toàn phase mutant codex_cred hoặc 470 mutant công cụ. Không đánh đồng 9 mutant độc lập với các bảng đầy đủ đó.
- Windows native/PATHEXT, ACL/SID/reparse/share-delete, CI Windows/CI trên exact head, trạng thái resolve thread, lease GitHub, wp775 nhả/land và master mới: không có bằng chứng trực tiếp trong lượt cục bộ này.
- Bootstrap npm/Codex thật và máy chủ chấp nhận credential thật không đo. Mọi auth/probe output do reviewer tạo đều inert. Không soạn payload nhạy cảm để khai thác; các hướng đó chỉ được mô tả bằng lời.
- Không suy sạch mọi child/mọi race từ fixture đã đo. Nợ `codex-auth-json-khong-cas` (Q3 r7) và `codex-rejected-state-khong-ghi-duoc` (r8) vẫn được ghi đúng là giới hạn đã chấp nhận, không tái đếm finding mở.

## Điều gì còn chặn và điều gì không

**Chặn approval nội dung ở ngưỡng sensitive:** G01 và G02 còn P2 chưa có quyết định chủ kho. F01 theo r8, F02/F03 và nợ CAS không chặn thêm. Ca F04 vắng CLI, test thứ tự mới và scrub trong các nhánh đã đo đều đạt; không lấy những kết quả đó để đóng lối executable hỏng G01.

**Chưa chứng minh đủ điều kiện merge:** M-1 chưa đạt do verdict này; M-2 chưa xác minh trả lời/resolve thread; M-3 chưa xác minh CI xanh và Windows exact head; M-4 chưa xác minh wp775 và merge master. Head đổi thì M-1/M-3 stale theo M-5. Không merge/land/push, không tự cấp thêm review call. Theo prompt và r8, bước điều phối kế tiếp là checkpoint với hai finding và giới hạn đo nêu trên.
