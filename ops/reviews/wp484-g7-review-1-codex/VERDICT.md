Reviewed commit: 99e79b107d4fd138dcd3e5ad51851a846fac9eb5
Spec SHA-256: 35a81f47dbea985ed867147fbf952be485faf5c3106e9c8afed27a0b41a533e1
verdict: changes_requested
P0=0 P1=0 P2=4 P3=0

Kết luận cuối: yêu cầu thay đổi cho F01–F04 bên dưới. P0/P1 bằng 0 chưa đủ để approve: bốn P2 này chưa có quyết định chấp nhận, và chưa tái lập được bằng chứng xanh đầy đủ N1/N6 trong môi trường này. Nợ CAS đã được Q3 chấp nhận được ghi riêng, không báo lại như một finding mới.

Đã xác minh checkout sạch, HEAD và tree đúng định danh trong chỉ thị. SHA-256 SPEC tự đo khớp.
Đã đọc spec r7, handoff g7, đặc tả kế thừa, diff 25 tệp so master, diff riêng g7 và combined diff merge. Reviewer: Codex/OpenAI qua API với công cụ shell; không có telemetry xác nhận model_id chính xác hoặc receipt assurance trong lượt này. Không dùng context executor, credential thật, device-auth hay network probe thật.

Môi trường: Linux, Python 3.13.16, Ruff 0.17.1, actionlint 1.7.7, sandbox `workspace-write`, không có quyền escalation. KHO không có delta mã nguồn khi kết thúc. Lượt suite đầu có tác dụng phụ tạo marker hook bị ignore; xem mục toàn vẹn checkout, không coi đây là lịch sử tuyệt đối không ghi.

## Findings

### F01 — P2 — XMG chưa đạt N4: lần gọi sau vẫn probe credential đã bị từ chối

- Lớp: `codex-rejected-state-write-fail-open` (kế thừa thread `PRRT_…XMG`).
- Vị trí: `.claude/dev/launcher.py:3197`, `.claude/dev/codex_cred.py:521`; ca mới ở `launcher_test.py:7681` và `codex_cred_test.py:428`.
- Bản vá đã báo lỗi ghi trạng thái, nhưng chưa ngăn lần gọi kế tiếp. N4 của spec r7 yêu cầu cả hai. Handoff tự khai giới hạn này đúng; chưa có quyết định chủ kho cho phép hạ N4 như Q3 đã cho phép riêng với CAS.
- PHÉP ĐO: `python3 -B run_clean.py python3 -B ../rv792-out/review_checks.py retry` (rc=0). Với store trong bộ nhớ, ghi `credential-recovery.json` ném `OSError` giả, hai lần gọi thật hàm đều báo lỗi và đều gọi probe:
  ```text
  launcher rejected credential probe calls= 2
  codex_cred invocation 1 rc= 2 reports state failure= True
  codex_cred invocation 2 rc= 2 reports state failure= True
  codex_cred rejected credential probe calls= 2
  ```
- HINT: thống nhất hợp đồng fail-closed cho mọi lối probe khi state không ghi được; nếu không thể lưu chặn qua tiến trình, cần quyết định/spec revision tường minh cho phần N4 chưa thể đạt. Ca khóa phải gọi lần hai và đếm probe; ca g7 hiện chỉ kiểm thông báo lần đầu. Rủi ro vá: chặn vĩnh viễn nếu không có cách phục hồi bằng snapshot mới.
- Lối thứ ba đã đo: `chuan_bi_xac_thuc` → `_probe_snapshot` → `_ghi_rejected` tại `launcher.py:3015`. Khi cùng lỗi ghi state, lời báo bị gộp thành lỗi chung và hai lần gọi vẫn chạy probe candidate hai lần (`prepare rejected candidate probe calls= 2`). Không phải chỉ có hai callsite `_danh_dau_auth_hong`.

### F02 — P2 — mất dấu hiệu từ chối `token_invalidated` khi chuyển sang probe chung

- Lớp: `codex-rejection-signature-regression`.
- Vị trí: `.claude/dev/codex_cred.py:208`, `.claude/dev/launcher.py:3191`.
- Master nhận `token_invalidated` là từ chối credential. PR thay `_do_codex_song` bằng `_kiem_song` nhưng danh sách chung thiếu dấu hiệu này; chỉ còn lỗi rc chung, không ghi recovery state và không chặn thử lại.
- PHÉP ĐO: `python3 -B run_clean.py python3 -B ../rv792-out/review_checks.py rejection` (rc=0); cùng `CompletedProcess(rc=1, stderr='token_invalidated')`, không gọi CLI/network:
  ```text
  base token_invalidated ok= False reason= credential BI TU CHOI (token_invalidated) state_marks= 0
  head token_invalidated ok= False reason= codex exec thoát rc=1 state_marks= 0
  head token_revoked ok= False reason= credential BỊ TỪ CHỐI (token_revoked) state_marks= 1
  base rc0 marker plus token_invalidated ok= False reason= credential BI TU CHOI (token_invalidated)
  head rc0 marker plus token_invalidated ok= True reason= rc=0, có TRALUAT-CRED-OK
  ```
- Phép đối chứng bổ sung rc=0 + marker stdout + stderr từ chối cho thấy helper có thể trả khỏe ngay trên đầu ra mà master đã chặn. Đây là fixture đầu ra giả, không phải lời khai đã quan sát Codex thật tạo tổ hợp ấy.
- HINT: giữ hợp của tập dấu hiệu từ chối của master và helper, dùng chung cho mọi probe. Test cả rc khác 0 và rc=0 có marker stdout nhưng stderr báo từ chối; đo state và lần gọi sau. Rủi ro: tránh mở rộng từ khóa quá chung gây chặn nhầm lỗi hạ tầng.

### F03 — P2 — ghi từ chối nhầm credential mới khi auth đổi trong lúc probe

- Lớp: `codex-rejection-identity-race` (mới tìm trong toàn diff so master, kế thừa mã g2).
- Vị trí: `.claude/dev/launcher.py:2913`, `.claude/dev/launcher.py:3197`, `.claude/dev/codex_cred.py:521`.
- Probe từ chối bản A nhưng `_danh_dau_auth_hong(home)` đọc lại auth hiện tại B rồi lưu ID của B. Một tiến trình khác vừa làm mới credential sẽ khiến bản mới chưa từng bị từ chối cũng bị chặn; A lại không có trong lịch sử. Khác khe thay tệp không CAS đã được Q3 chấp nhận.
- PHÉP ĐO: `python3 -B run_clean.py python3 -B ../rv792-out/review_checks.py rejection_race` (rc=0), store bộ nhớ, probe giả đổi auth từ chuỗi inert A sang B trước khi báo A bị từ chối; chạy logic ghi state thật:
  ```text
  old credential recorded rejected= False
  replacement credential recorded rejected= True
  replacement now blocked= True
  second result= False CHỜ snapshot Codex mới probe calls= 1
  codex_cred rc= 2 replacement recorded rejected= True
  ```
- HINT: truyền identity/bytes của credential thực sự được probe vào lớp ghi từ chối; khi auth hiện tại đã đổi thì giữ bản mới, không gán kết quả của bản cũ sang nó. Áp dụng chung cả hai callsite. Ca khóa phải thay auth ở seam sau probe và kiểm ID A/B độc lập. Rủi ro vá: không dùng identity trước probe một cách mù quáng nếu chính CLI đã xoay refresh token; cần phân biệt bản probe với bản mới của tiến trình khác.

### F04 — P2 — bootstrap dừng trước cài Codex khi snapshot mới cần probe

- Lớp: `codex-bootstrap-probe-before-install` (toàn PR so master).
- Vị trí: `.claude/hooks/session-start.sh:89`, `.claude/hooks/session_start.py:107`, `.claude/dev/launcher.py:3011`.
- Điều kiện: máy remote chưa có `codex` trên PATH, home đã có auth cũ, biến mang snapshot mới hơn. Materializer cần live probe trước thay bản cũ; helper không tìm được CLI nên trả thất bại. Shell hook thoát 13 trước khối `npm install -g @openai/codex`; bridge cũng trả 13 trước khi gọi shell. Cơ chế tự dựng CLI vì vậy không tự phục hồi được tình huống này. Master cài CLI trước khối khôi phục auth.
- PHÉP ĐO: `python3 -B run_clean.py python3 -B ../rv792-out/review_checks.py bootstrap` (rc=0). Phần một chạy materializer/probe thật với store fixture phân theo home và PATH trống; phần hai replay chính mã lỗi ấy ở biên CLI của hook bản sao, có npm giả ghi nhận lời gọi:
  ```text
  materializer without codex: ok= False reason= CHƯA ĐO ĐƯỢC probe; giữ nguyên credential cũ, chưa kết luận auth hỏng
  active credential preserved= True
  hook replay rc= 13 npm installation reached= False
  [session-start] CHO snapshot Codex moi; dung truoc cac probe
  ```
- Giới hạn: đây là hai phép đo seam nối bằng mã lỗi, không phải một lượt bootstrap tích hợp dùng storage kernel/CLI thật. Không thực hiện cài đặt hoặc đăng nhập.
- HINT: tách bước dựng CLI đáng tin khỏi bước probe/promote; gỡ snapshot khỏi môi trường trước installer rồi mới cho materializer riêng nhận nó. Chỉnh cả bridge lẫn shell để không chặn trước bước dựng công cụ cần thiết. Ca khóa: PATH chưa có Codex + auth cũ + snapshot mới, installer giả phải được gọi trước probe; mọi child ngoài materializer phải không thấy raw snapshot. Rủi ro vá: đảo thứ tự có thể đưa secret vào installer/probe nếu chỉ dời câu lệnh mà không giữ ranh giới môi trường.

## Đối chiếu g7 và nợ kế thừa

| Hạng mục | Kết quả review |
|---|---|
| Merge hook | Đúng thứ tự: `unset`/chụp biến shell không export tại dòng 37–40 đứng trước `GOC` có `dirname` dòng 42 và trước ghi dấu vết. Spy thực thi xác nhận ba lệnh ngoài đều sạch. Materializer tại dòng 89 là child chủ ý duy nhất được truyền snapshot. |
| Merge test | Không mất/trùng tên ca hay mục `DOT_BIEN` của master hoặc faaedff. Master 197 ca/233 mutant; faaedff 197/178; merge 212/243; head 216/246. Chỉ một phép gán `DOT_BIEN`. `DOT_BIEN_HARNESS` cũng giữ nguyên cả hai phía. |
| Nghĩa test master | Các seam recovery/home thêm vào t85, t93, t94, t96, t102, t133 để cô lập phép đo; không bỏ các assertion cũ. Hai mutant master đổi neo theo refactor là `chuan_bi_bo_duong_JSON_tho`, `do_codex_song_spawn_ten_tran`; không mất mục. Full suite không báo các ca này đỏ, ngoại trừ t86 bị môi trường storage chặn. |
| XLy / N2 | Phép đọc lại trước replace có tác dụng trong unit dùng dirfd thật; gỡ phép đọc lại thì bản concurrent bị ghi đè. Ca tích hợp g7 không đo được do `/tmp/.git`. Chưa phải CAS. |
| XL- / N3 | Home hợp lệ chưa tạo: rc=3 qua cả CODEX_HOME và `--codex-home`, không tạo credential. Nửa ca home đã có nhưng thiếu auth bị guard môi trường chặn; không nhận là đã xác minh đầy đủ t15. |
| XMG / N4 | Thông báo lỗi ghi được vá và mutant có răng; nghĩa “lần kế không thử lại” chưa đạt — F01. Lối thứ ba materializer cũng đã đo. |
| XML / N5 | Ca có sẵn replay cả relative và parent-component: 1/1, Chan(13), không traceback. Lối `run codex` trả Chan(13) ở seam sau chốt; doctor/live guard trả chặn; `codex_cred kiem` rc=2 và env-policy rc=3 có kiểm soát. Không phát hiện lối traceback thứ ba cho các fixture này. |
| Test không thừa hưởng credential | Canary với biến giả đạt 1/1; bỏ dòng pop làm chính assertion của canary đỏ. Các ca cần snapshot đặt biến tường minh. Không tìm thấy nguồn env khác giữ credential phiên trong các ca đã đọc. Windows native chưa đo; không suy bug chữ thường trên Windows từ hành vi dict case-sensitive ở Linux. |

Nợ **`codex-auth-json-khong-cas`** vẫn mở, mức P2, do chủ kho quyết ở Q3/spec r7: hai syscall đọc–replace vẫn có khe đua với Codex CLI không tuân khóa. Handoff nói **THU HẸP**, không nhận đã đóng, đúng phạm vi phép đo. Không có quyết định tương tự trong spec cho F01–F04. Không soạn thêm payload nhạy cảm để khai thác khe đua.

## Bảng lớp nguyên nhân

| Slug | Finding / mức cao nhất | Nguồn | Phép kiểm cần để đóng |
|---|---|---|---|
| `codex-rejected-state-write-fail-open` | F01 / P2 | XMG trên faaedff, chưa đạt N4 trên head review | Hai lần gọi ở cả launcher, credential CLI, materializer khi ghi state thất bại; lần hai không probe credential đã hỏng, hoặc có revision/authority chấp nhận giới hạn. |
| `codex-rejection-signature-regression` | F02 / P2 | Refactor master → probe chung trên PR này | Hợp tập dấu hiệu cũ/mới; từ chối phải thắng rc/marker và sinh recovery state. |
| `codex-rejection-identity-race` | F03 / P2 | `_danh_dau_auth_hong` kế thừa g2 | Probe A thất bại + auth đổi B: không ghi B vào rejected, không chặn nhầm B. |
| `codex-bootstrap-probe-before-install` | F04 / P2 | Hook/bridge kế thừa g2 | Thiếu CLI + auth cũ + snapshot mới: dựng CLI với env sạch rồi mới probe/promote; old auth giữ nguyên khi probe hỏng. |

Đếm: 4 lớp, 4 finding; F01 có ba lối vào, F03 có hai lối vào. Không coi tổng suite xanh hoặc đổi thông báo là đã đóng lớp.

## Hướng thử

Mọi lệnh dưới chạy từ thư mục ra. `R` viết tắt **`python3 -B run_clean.py`**; `C <mode>` viết tắt **`python3 -B run_clean.py python3 -B ../rv792-out/review_checks.py <mode>`**. Runner dùng env allowlist, HOME/USERPROFILE/CODEX_HOME tạm; không truyền các token phiên. Script và log đi kèm nằm cùng `VERDICT.md`.

| Giả thuyết độc lập | Lệnh đã chạy | Output thật rút gọn | Phân loại |
|---|---|---|---|
| Lệnh ngoài đầu hook còn thấy snapshot | `C hook_order` | `hook rc=0`; `dirname: clean`, `mkdir: clean`, `date: clean` | KHÔNG PHẢI LỖI trong nhánh đã đo |
| Merge mất/nhân ca hoặc mutant | `C inventory` | `missing cases=[]`, `missing mutants=[]`, `head duplicate cases=[]`, `head duplicate mutants=[]` | KHÔNG PHẢI LỖI |
| Home hợp lệ chưa tạo bị báo ĐỎ | `C missing_home` | `explicit_home=False rc=3`; `explicit_home=True rc=3` | KHÔNG PHẢI LỖI |
| Home sai làm launcher traceback | `R python3 -B .claude/dev/launcher_test.py --lap-ca r484_g7_credential_status --lan 1`; `C home_entries` | `1/1 qua`; status/run `13`, kiem `2`, policy `3`; `traceback=False` | KHÔNG PHẢI LỖI với fixture đã đo |
| Lỗi ghi state vẫn retry | `C retry` | launcher `probe calls=2`; codex_cred `2`; prepare candidate `2` | LỖI — F01 |
| Refactor mất dấu hiệu từ chối | `C rejection` | `token_invalidated`: base từ chối, head rc=1 chung; rc0+marker: base False, head True | LỖI — F02 |
| Probe A lại đánh dấu B | `C rejection_race` | `old ... rejected=False`, `replacement ... rejected=True`, `replacement now blocked=True` | LỖI — F03 |
| Bootstrap tự cài được khi probe thiếu CLI | `C bootstrap` | materializer `ok=False`; hook `rc=13`, `npm installation reached=False` | LỖI — F04; đo hai seam |
| Pop đầu module làm test mất răng | `R --fake-snapshot python3 -B .claude/dev/launcher_test.py --lap-ca r484_g7_bo_test --lan 1`; `C isolation_mutant` | nền `1/1`; mutant `rc=1`, `bộ test thừa hưởng credential phiên: 'CON\n'` | KHÔNG PHẢI LỖI; canary bắt đúng mutant |
| Đọc lại trước replace không có tác dụng | `C cas_unit` | head `reads=2 kept replacement=True`; mutant `reads=1 kept replacement=False` | KHÔNG PHẢI LỖI cho thuật toán đọc/ghi đã cô lập |
| Ba mutant g7 đều có bằng chứng hợp lệ | `C mutants` | home/state chết ở assertion ca đích; CAS chết vì `Codex home is inside a repository` | KHÔNG ĐO ĐƯỢC ca CAS tích hợp; chỉ 2 kill hợp lệ |
| Full launcher suite tái lập N1 | `R python3 -B .claude/dev/launcher_test.py` | `196/206 ... tong 216, bo qua 10, hong 10`; rc=1 | KHÔNG ĐO ĐƯỢC N1 xanh trong sandbox này |
| Full codex_cred suite tái lập N6 | `R python3 -B .claude/dev/codex_cred_test.py` | `nền: 12/16 đạt`; rc=1; dừng trước mutants | KHÔNG ĐO ĐƯỢC N6 xanh trong sandbox này |
| Lint/gate tăng nợ so base | Ruff F no-cache trên 4 tệp; doctrine/adr head và base | F841 `5→5`, delta 0; doctrine `0→0`; adr `0→0` | KHÔNG PHẢI LỖI theo N8/N9 |
| Quy tắc void/checkpoint hồi quy | `R python3 -B .claude/dev/packet_loop_test.py` | `nền: 343/343 đạt · BỎ QUA: 1`; `TỔNG: ĐẠT`; rc=0 | KHÔNG PHẢI LỖI trong phạm vi suite |

## Đã đo

- `sha256sum spec-wp484-r7.md`: rc=0, `35a81f47dbea985ed867147fbf952be485faf5c3106e9c8afed27a0b41a533e1`.
- `git -C KHO rev-parse HEAD HEAD^{tree}`: rc=0, head `99e79b107d4fd138dcd3e5ad51851a846fac9eb5`, tree `8c19048843e861c306d568e9f9f5ff63a2393ba9`.
- `git -C KHO status --short`: rc=0, output rỗng.
- `C inventory`, `C retry`, `C rejection`, `C rejection_race`, `C bootstrap`, `C hook_order`, `C home_entries`, `C missing_home`, `C cas_unit`, `C isolation_mutant`, `C mutants`: runner rc=0; các assertion độc lập đạt. Rc mutant con được ghi riêng, không lấy rc runner làm bằng chứng mutant bị giết.
- Ba lượt `launcher_test.py --lap-ca` g7: home/state/isolation đều rc=0, mỗi lượt 1/1 qua. Isolation dùng `--fake-snapshot`, giá trị inert.
- `C mutants`: `g7_home_sai_lai_traceback` con rc=1, assertion phát hiện traceback; `g7_nuot_loi_ghi_trang_thai` con rc=1, assertion phát hiện thông báo bị nuốt. `g7_bo_doc_lai_truoc_replace` con rc=1 vì setup nên **không tính kill**. Mỗi mutant trên bản sao riêng, child riêng, `-B` và không ghi bytecode.
- Full launcher: rc=1; 196 passed, 10 failed, 10 skipped. Log [launcher-suite.log](launcher-suite.log). Các lỗi xoay quanh storage bị guard `/tmp/.git` chặn, không dùng làm finding sản phẩm. Hai skip do nền Linux: `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`, `r484_g4_windows_sid_alias_identity`. Tám skip do không dựng được venv/pip: `r345_chan_socket_that_ma_than_hook_van_chay_dung`, `r345_cac_phep_do_cuc_bo_van_dung`, `r345_lop_tham_import_van_co_rang`, `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`, `r347_tham_import_van_song_tren_python_truoc_310`, `r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO`, `r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia`, `r348_dot_bien_bo_isidentifier_lam_ca_dich_DO`.
- Full codex_cred: rc=1; nền 12/16, bốn ca t6/t9/t15/t16 lỗi fixture dưới `/tmp`; chưa chạy phase đột biến. Log [codex-cred-suite.log](codex-cred-suite.log).
- `R python3 -B .claude/dev/packet_loop_test.py`: rc=0; baseline 343/343, một skip `luong_canonical_chay_that` vì cần pwsh trên Windows; 106 đột biến, 78 lớp lách, 35 ca bắt-oan; tổng ĐẠT. Log [packet-loop.log](packet-loop.log).
- `R python3 -m ruff check --no-cache --select F --output-format json .claude/dev/launcher.py .claude/dev/launcher_test.py .claude/dev/codex_cred.py .claude/dev/codex_cred_test.py`: head rc=1, base rc=1; năm F841 giống nhau theo code/tệp/message, đều ở launcher_test; ba tệp còn lại 0. **Delta=0**, không gọi bare lint là xanh. Base chạy bằng `R --repo review-copy ...` sau checkout đúng 653fef3 trong clone riêng. Logs `ruff-head.json.log`, `ruff-base.json.log`.
- `R python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` và `... adr-song --root .`: head/base đều rc=0. Doctrine quét 10 tệp, 0 chỗ; ADR 50/50, cùng ngoại lệ 0016 như base. Logs `doctrine-{head,base}.log`, `adr-{head,base}.log`.
- `bash -n ../rv792/.claude/hooks/session-start.sh`: rc=0.
- `actionlint -shellcheck= ../rv792/.github/workflows/launcher-windows.yml`: rc=0, output rỗng. Đây là kiểm workflow tĩnh, **không** phải lượt CI Windows hay ShellCheck (môi trường không có ShellCheck).

## Toàn vẹn checkout và phạm vi phép đo

Đã dùng clone riêng `review-copy` cho base; mọi mutant trong thư mục tạm, không sửa mã KHO. Các seam bộ nhớ của F01/F03/F04 đo logic, không chứng minh guard kernel. `cas_unit` đo hàm read/write thật với dirfd nhưng chủ ý không gọi constructor do marker `/tmp/.git`; không thay thế test storage tích hợp.

Sai sót vận hành cần ghi rõ: full launcher suite đầu được chạy trực tiếp theo ví dụ trong chỉ thị. Hook đã tạo `.claude/.packet_state/session-start.ran` bị ignore (birth/mtime `2026-10-17 02:07:31Z`, nội dung `2026-10-17T02:07:31Z cuc_bo`). Đã xóa đúng artifact vừa sinh và thư mục rỗng; không sửa mã nguồn để chữa test. Vì vậy không khai lịch sử run tuyệt đối không có ghi vào KHO. Chốt cuối kiểm HEAD/tree, diff/index và cả ignored/untracked; output được lưu ở `checkout-final.log`. Snapshot đầu chỉ có status thông thường nên không có baseline hash ignored/index metadata để khẳng định hơn nữa.

Audit cuối: HEAD/tree vẫn khớp; status gồm ignored/untracked, diff HEAD, diff cached và hai danh sách tệp ngoài index đều rỗng, mọi rc=0; `FINAL CHECKOUT AUDIT: PASS`. Băm spec đo lại vẫn khớp dòng 2.

## KHÔNG ĐO ĐƯỢC

- Windows native và trạng thái CI/resolve thread/lease trên GitHub: chưa có bằng chứng trong lượt đọc cục bộ này.
- Storage fixture dưới `/tmp`: môi trường có `/tmp/.git` rỗng chỉ đọc; `_KhoCodex` cố ý từ chối mọi home bên dưới. Lượt `codex_cred_test.py` ban đầu rc=1, nền 12/16; bốn ca lỗi setup `Codex home is inside a repository`. Không tính đây là lỗi sản phẩm và không tính mutant chết vì nó là bằng chứng hợp lệ. `unshare` và `chroot` đều bị môi trường từ chối.
- Chưa tái lập launcher 214/214 ở cả hai môi trường có/vắng biến giả. Chỉ chạy full không có snapshot (196 pass như trên) và canary riêng có snapshot. Không suy claim executor sai từ khác biệt sandbox.
- Không tái lập full codex_cred nền 16/16 + mutant 16/16; không chạy toàn bảng launcher `--dot-bien`.
- Native Windows ACL/SID/reparse/share-delete, Windows env case-fold, workflow install dependencies và check run Windows/CI trên exact head: không có Windows/GitHub facts trong lượt này. Actionlint không thay các phép đo ấy.
- Không chạy CLI Codex/device-auth/LIVE với credential thật; không đo khả năng máy chủ chấp nhận token. Các token/child output trong phản chứng đều inert hoặc giả.
- Các hướng cần tự soạn payload thoát cây/mã khai thác không thực hiện theo chỉ thị. Đọc và replay fixture sẵn có khi cần; không tuyên bố đã loại trừ mọi đường rò bí mật hoặc mọi race.

## Điều kiện merge

M-1 chưa đạt: verdict `changes_requested`; F01–F04 cần vá/đo lại hoặc quyết định có thẩm quyền đúng phạm vi. Nợ CAS giữ Q3. M-2 chưa xác minh trả lời/resolve thread; M-3 chưa xác minh CI và Windows; M-4 chưa xác minh wp775 nhả/land và merge master mới. M-5: verdict này chỉ áp dụng head ghi ở dòng đầu, đổi head phải review lại. Không merge, land, push hoặc gửi thông điệp tới người khác.
