Reviewed commit: 907214d2cd0b67ff444b3adf734811eab39bfc71
Spec SHA-256: 4a512dd38721c3c4eec7978489ba06485feab32f94a0c5637a085d6c694ba38c
verdict: approve
P0=0 P1=0 P2=0 P3=0

**Không tìm thấy P0/P1/P2 còn mở sau attempt 5 trong phạm vi review này. J01 và lỗi `failure_class` đã đóng bằng các phép đo dưới đây. Không phát sinh finding K01… có phản chứng chạy được.** CAS, F01 và checkpoint là ba nợ đã có quyết định, không tính vào số finding mở. `approve` theo ngưỡng của chỉ thị hiện tại; không xác nhận đã đủ điều kiện merge hoặc toàn bộ gate đã xanh.

HEAD/tree tự đo: `907214d2cd0b67ff444b3adf734811eab39bfc71` / `735f7ee67c4e2bf2612fcdc4d6027eff453baeb0`, checkout detached. Delta từ `0f31bb3e6151dd0cc67e8d4664b139259383b8d5`: đúng 3 tệp, +93/−3; `git diff --check` rc0. Băm VERDICT4 đo lại khớp `841bf022163d7594ce82a9a9411e8a5ab17ab36cfadf343f4cbd8d92c3a4741b`.

Reviewer Codex/OpenAI, context độc lập với executor Claude g7. Run `b28e8193b7c046829b2e2ca877e53efa` tại thư mục ra ghi chương trình `codex`, `transport=machine`; khai `provider=openai_codex`, `execution_surface=codex_cli`, `model_family=openai`. Không tự xác nhận tên model/effort hoặc receipt nhận diện chưa đo được. Linux, Python 3.13.16, Git 2.43.0, Ruff 0.16.8; sandbox workspace-write, approval never. Không truy cập GitHub, không dùng credential thật, không chạy installer thật. Đây là lời gọi review cuối được assignment cấp, không đề nghị tự động gọi thêm.

## Bảng kết luận

| Mục | Kết luận | Bằng chứng độc lập |
|---|---|---|
| J01 / `hook-scrub-test-unisolated-bootstrap` | **Đóng biểu hiện đã báo.** Không cộng lại G02/H01/J01 thành nhiều finding. | Phản chứng `env-escape` cũ trên base vẫn xanh 3/3 nhưng gọi 18 lần installer spy ngoài fixture. Cùng phản chứng trên head: xanh 3/3, 0 lời gọi ngoài fixture. Ca mới J01 xanh 3/3 với seam materializer; mutant bỏ lọc env bị đúng assertion installer ngoài fixture giết. |
| Connector P2 `failure_class` trên `xong`/rc0 | **Đóng.** | Ca mới nguyên bản xanh 1/1, không seam. CLI thật: thành công có/không output đều không có khóa; rc3, signal exit, timeout, interrupt và stop vẫn `unknown`. Mutant giữ khóa làm chính assertion rc0 đỏ. |
| Connector P1 “spec/lease không có trong cây PR” | **Không giữ là P1. Lập luận executor phù hợp tài liệu và có blob kiểm chứng cục bộ.** | `CLAUDE.md:180` nói lease sống trên `ops/**`; protocol §3.2.1 yêu cầu xác minh nguồn OID/path/hash, không buộc đưa spec vào product tree. Ref `origin/ops/wp484-r7-spec` tại `61cadbd2a9b7f44cc1858b819554702981cde632` thực sự có cả spec r7/r8 và lease r8/g7. Spec r8 tại OID lease neo `4d9ea3131ae8f406b14096ed73748750e8634b4a` cũng khớp SPEC8 từng byte/băm. Việc hai tệp vắng ở HEAD sản phẩm không tự tạo lỗi. Không coi ref cache là xác minh trạng thái GitHub hiện tại. |
| CAS / `codex-auth-json-khong-cas` | Nợ có quyết định r7 Q3, không mở lại. | Không tuyên bố đã đóng khe syscall cuối. |
| F01 / `codex-rejected-state-khong-ghi-duoc` | Nợ có quyết định SPEC8, không mở lại. | Không nâng acceptance đã được chủ kho hạ. |
| `launcher-resume-checkpoint-khong-rang-buoc-luot-goc` | Nợ chủ kho quyết theo assignment, không tính finding mở. | Không giả định delta đã ràng buộc checkpoint vào run gốc. |

Nguồn spec authoritative được chỉ định trong lease là `4d9ea3131ae8f406b14096ed73748750e8634b4a:ops/specs/wp484-r8.md`, blob `812bf04c48bf2a720a82ced7fcd36600289a4bbf`. Bản tại ref cục bộ và bản `spec-wp484-r8.md` ở thư mục ra cùng SHA-256 như dòng 2. Spec r7 kế thừa tự đo khớp `35a81f47dbea985ed867147fbf952be485faf5c3106e9c8afed27a0b41a533e1`. [Dữ liệu nguồn và storage](logs/provenance.json), [blob đã chép ra scratch](evidence/r8-lease-anchor.txt), [lease cục bộ](evidence/lease.txt). Không copy các hồ sơ này vào KHO. Lease khai `base_sha=653fef3f52f3130dd6f597c1036430ffb807fef1`, `start_from_sha=faaedff19af12063b9c1232e602e2e3fec479861`; candidate review là HEAD ở dòng 1. Head lượt 4 chỉ là mốc so delta của lượt review này, không thay baseline nghiệm thu toàn packet.

## J01, seam và các đường môi trường

`python -B review_hook_and_mutants.py` rc0; kết quả từng tiến trình con nằm trong [hook-and-mutants.json](logs/hook-and-mutants.json). Runner được tự dựng; không chạy `executor-do_g8.py` để nhận bằng chứng. Phản chứng lấy cùng cấu trúc đã dùng lượt 4: startup Bash chỉ thêm thư mục reviewer vào đầu PATH; `rg` trong đó hỏng, installer trong đó chỉ ghi nhật ký và trả 97. Tất cả là canary inert, không đọc credential hoặc tải mạng.

**Giới hạn/seam:** sandbox hiện có `/tmp/.git` chỉ đọc. Probe `_KhoCodex` độc lập trả `OSError: Codex home is inside a repository`. Ca hook nguyên bản rc1, hook rc13; nó dừng trước các assertion cần đo J01. Để đo riêng startup và răng ca, [review_case.py](review_case.py) thay **chỉ launcher materializer được fixture chép vào project tạm** bằng writer inert của snapshot giả. Giữ nguyên thân ca, assertion, Python shim và hook, ngoại trừ đúng mutant được chỉ định. Đây không phải integration/storage pass. Ca `failure_class` và mutant sản phẩm không dùng seam này.

| Đối chứng / ca | Rc ca | Kết quả | Lời gọi installer ngoài fixture |
|---|---:|---|---:|
| Hook nguyên bản, không seam | 1 | 0/1, hook13 vì storage | 0 |
| Positive head, có seam | 0 | 3/3, hook0 cả ba | 0 |
| `env-escape` base `0f31bb3`, có seam | 0 | 3/3; nhật ký installer của fixture rỗng | **18** |
| `env-escape` head `907214d`, có seam | 0 | 3/3; hook0 cả ba | **0** |
| Ca mới `r484_g8_hook_scrub_kin_voi_bash_env`, có seam | 0 | 3/3; giữ assertion `NAP` CÓ và `NGOAI` VẮNG | 0 |

Head lọc `BASH_ENV`, `ENV`, `BASH_FUNC_*`, đặt HOME tạm và giả actionlint. Nhật ký của `env-escape-head` xác nhận env vào hook không còn hai biến startup, HOME nằm trong sân tạm. `NAP` của ca mới là positive control cho startup phía phép dò Bash của test; không coi mọi `NAP` là hook đã bị lọt.

`python -B review_python_env.py` rc0: `PYTHONPATH` với `sitecustomize.py` inert thực sự được nạp **7 lần**, chỉ thêm cùng thư mục ambient vào PATH; ca vẫn 1/1, **0 installer ngoài fixture**. `PYTHONHOME` hợp lệ: 1/1; `PYTHONHOME` sai: **đỏ 0/1**, không phải xanh giả. ENV riêng và exported Bash function: 1/1, không installer ngoài fixture. Đối chứng bổ sung `review_function_control.py` rc0 xác nhận danh sách `BASH_FUNC_*` vào hook rỗng, không marker hàm. [Kết quả Python/env](logs/python-env.json), [đối chứng hàm](logs/function-control-hook.json).

Các phép đo này không chứng minh cô lập mọi startup Python hoặc mọi biến môi trường. Chưa có phản chứng khác chứng minh ca xanh trong khi installer host thoát fixture; không cộng P2 từ suy đoán, từ việc startup Python có chạy, hoặc từ một cấu hình Python hỏng làm ca đỏ. Nội dung thử cần bí mật, proc/memory hay tải trọng nhạy cảm chỉ được mô tả bằng lời và không thực thi.

## `failure_class`

`python -B review_failure_class.py` và `python -B review_failure_edges.py` đều rc0. [CLI records](logs/failure-class.json), [hai đối chứng bổ sung](logs/failure-edges.json).

| Đường kết thúc | Rc launcher | `trang_thai` / `ma_thoat` trong sổ | `failure_class` |
|---|---:|---|---|
| Thành công có output / không output | 0 / 0 | `xong` / 0 | Không có khóa |
| Thành công có attempt-state ký và void reason được yêu cầu | 0 | `xong` / 0 | Không có khóa; không có `void_reason` |
| Child exit3 | 3 | `xong` / 3 | `unknown` |
| Child chết vì SIGTERM | 1 | `xong` / −15 | `unknown` |
| Quá hạn | 124 | `qua_han` / 124 | `unknown` |
| SIGINT vào launcher | 130 | `bi_ngat` / 130 | `unknown` |
| CLI stop, child xử lý SIGTERM rồi exit0 | 0; stop rc0 | `da_dung` / null ở record stop cuối | `unknown` |
| Đối chứng stop + child rc0, seam riêng ở lần đọc trạng thái cuối | 0 | `da_dung` / 0 | `unknown` |
| Probe chặn trước spawn | 15 | `hong` / 15, `giai_doan=probe` | Không có khóa |
| Popen thất bại trước khi sinh child, override probe có lý do inert | 2 | `hong` / null | Không có khóa |

Hai hàng trước spawn không phải lượt đã chạy rồi mất nhãn: `unknown` chỉ được gán sau Popen thành công, đúng ranh giới phân loại và chống refund kế thừa. Với stop thật, không suy `ma_thoat=0` từ rc launcher0: record stop quan sát được có null. Đối chứng cuối vòng đời dùng seam **chỉ `_doc_so` trả trạng thái `da_dung` tại lần đọc cuối**, còn child/Popen/wait/ghi sổ là thật, để đo chính xác tổ hợp `da_dung` + child0. Không dùng seam này làm bằng chứng stop tích hợp.

Không thấy đường hoàn tất `xong`/0 còn nhãn hoặc đường đã sinh child bị hỏng mất nhãn trong các nhánh đã đo. Điều kiện gỡ khóa nằm sau việc giữ trạng thái stop và dùng cả trạng thái lẫn mã thoát thật, nên rc0 riêng lẻ không xóa nhãn của lượt bị dừng.

## Hai đột biến đã đăng ký

Lấy nguyên cặp cũ/mới và danh sách ca đích bằng AST từ `DOT_BIEN` / `DOT_BIEN_HARNESS`, kiểm neo xuất hiện đúng một lần ở vùng mã thích hợp, compile rồi chạy trên bản sao riêng, tiến trình riêng, `-B`. Không sửa KHO. [Runner độc lập](review_hook_and_mutants.py), [log mutant sản phẩm](logs/g8_xong_rc0_van_giu_failure_class.log), [log mutant harness](logs/g8_fixture_chep_nguyen_moi_truong.log).

| Mutant | Ca đích / rc | Bằng chứng đúng assertion của chính ca |
|---|---|---|
| `g8_xong_rc0_van_giu_failure_class` (`DOT_BIEN`) | `r484_g8_run_xong_khong_mang_failure_class`, rc1, 0/1 | `lượt xong rc=0 vẫn mang failure_class='unknown'` |
| `g8_fixture_chep_nguyen_moi_truong` (`DOT_BIEN_HARNESS`) | `r484_g8_hook_scrub_kin_voi_bash_env`, rc1, 0/1, seam materializer | `installer ngoài fixture đã chạy`; sáu sự kiện `NGOAI apt-get`/`NGOAI sudo`, có `NAP` |

Không nhận SyntaxError, ImportError, lỗi storage hoặc lỗi dựng runner là mutant kill. Mutant harness bị giết dù hook rc0 và ca bên trong vẫn qua; chính assertion ngoài kiểm nhật ký ambient bắt được escape.

## Bảng hướng thử

| Hướng | Lệnh / hiện vật | Kết quả đo | Kết luận |
|---|---|---|---|
| Tái lập đúng J01 lượt 4 hai chiều | `python -B review_hook_and_mutants.py` | Base18, head0 lời gọi ngoài fixture; cả hai 3/3 | Bản vá chặn phản chứng cũ |
| Positive control `NAP` và mutant env | Cùng runner, ca J01 và mutant harness | Positive3/3; mutant0/1 đúng assertion `NGOAI` | Ca mới có răng với seam đã khai |
| Startup Python / PYTHONHOME | `python -B review_python_env.py` | sitecustomize7 marker, không installer; home sai làm ca đỏ | Chưa có P2 mới chạy được |
| Exported Bash function | `python -B review_function_control.py` | rc0; env hàm vào hook rỗng, không marker | Bộ lọc có hiệu lực ở biên hook |
| Thành công / rc khác0 / ngắt / quá hạn / stop | `review_failure_class.py`, `review_failure_edges.py` | Phân bố nhãn như bảng; hai runner rc0 | Không thấy hồi quy nhãn ở đường đã đo |
| Mutant giữ khóa thành công | Runner hai mutant | rc1 tại assertion của ca mới | Ca không chỉ kiểm trạng thái chung |
| Hồi quy có/không snapshot giả | `review_regression.py`, `review_compare.py` | 0 ca chung đổi màu | Thêm đúng 2 ca; giới hạn storage và installer vẫn được khai |
| Ruff, Bash quota, doctrine, ADR | `review_static.py`, `review_remaining.py` | F5→5; quota7/7; scanner/syntax/gate rc0 | Không tăng nợ F hoặc lời gọi Bash trần |

## Đã đo

- Ghi `VERDICT.md` sớm rồi cập nhật. Xác minh assignment, AGENTS, các phần protocol/CLAUDE/provider áp dụng, SPEC8 cùng r7 kế thừa, VERDICT4, delta, handoff và đường hook/launcher liên quan. Dùng hai clone độc lập trong thư mục ra, đúng hai SHA, `core.abbrev=7`; mọi mutant và hiện vật đều ở thư mục ra.
- Runner dùng env cho phép, HOME/USERPROFILE/CODEX_HOME/TMPDIR tạm. Credential thật của phiên không được truyền vào test. Hai lượt fake chỉ truyền `CODEX_AUTH_JSON` inert; module suite tự gỡ trước các ca. Guard trên PATH của runner chỉ nhận tám lần `npm --version`, không có lệnh cài trong [nhật ký guard](logs/installer-guard.log). Các installer spy của phản chứng/mutant đều là tệp inert riêng. Không chạy venv/pip thật.
- **So từng tên ca toàn suite, không seam materializer:** `python -B review_regression.py` chạy bốn lượt tuần tự; driver rc0, **mỗi suite rc1**. Để tuân thủ cấm installer thật, helper `_r345_venv` được cho trả None, khiến tám ca dùng nhánh không đo được vốn có. Không đổi thân các ca hay nhận những skip này là pass.

| Cây / snapshot ngoài | Rc suite | Passed | Failed | Skipped | Tổng đăng ký |
|---|---:|---:|---:|---:|---:|
| `907214d` / không | 1 | 199 | 14 | 10 | 223 |
| `907214d` / inert | 1 | 199 | 14 | 10 | 223 |
| `0f31bb3` / không | 1 | 198 | 13 | 10 | 221 |
| `0f31bb3` / inert | 1 | 198 | 13 | 10 | 221 |

- `python -B review_compare.py` rc0: **0 ca chung đổi trạng thái** head/base trong cả hai môi trường, và 0 ca đổi giữa clean/fake trên head. Ca mới `failure_class` pass; ca J01 mới đỏ cùng chỗ storage của ca hook cũ. Các ca đỏ chung gồm 11 ca storage/recovery, một ca hook dừng theo storage, và `t53` vì rig không có claude/codex/gh chạy được. Head thêm ca J01 bị cùng giới hạn. Không coi chúng là hồi quy hoặc làm tròn thành 221/221. [Tổng bốn lượt](logs/regression-summary.json), [so từng ca](logs/compare.json), [log head clean](logs/review-copy-clean.log), [dữ liệu đầy đủ từng ca](logs/review-copy-clean.json).
- `python -B review_static.py` rc0: bare Ruff `check --no-cache --select F --output-format json` trên năm tệp Python của packet **rc1 ở cả hai cây**, cùng năm F841 trong `launcher_test.py`, cùng vị trí/message; **DELTA=0**, bốn tệp còn lại0. Không gọi bare Ruff xanh. `bash -n .claude/hooks/session-start.sh` rc0 hai cây. `python -B ops/bash_nen.py quet --root . --json` rc0, `DAT`, nguồn `blob-index`, đếm launcher_test **7**, quota **7**, không lệch. AST xác nhận 221→223 ca, không mất ca; chỉ đổi thân ca hook cũ và thêm hai ca g8. [Static summary](logs/static-summary.json), [dữ liệu Ruff/scanner](logs/static-full.json).
- `python -B review_remaining.py` rc0: `packet_loop.py doctrine-scan --root .` và `adr-song --root .` đều rc0 ở hai cây; bằng chứng dương lần lượt 10 tệp/0 chỗ chép doctrine và 50 ADR/50 dòng khớp1–1. [Gate bổ sung](logs/additional-gates.json).
- `python -B validate_evidence.py` rc0: kiểm lại số18→0, positive3/3, hai assertion kill đúng mục, không đổi màu ca chung, source nguyên vẹn và gate bổ sung.
- `python -B finish_audit.py` rc0: HEAD/tree đúng, detached; status gồm ignored/untracked, diff HEAD/index của **KHO đều rỗng**. SHA-256 của **3.686 tệp tracked không đổi** giữa snapshot trước/sau; SPEC8 và VERDICT4 vẫn khớp. Hai bản sao test chỉ sinh marker hook ignored, không đổi tệp tracked. [Audit](logs/audit-summary.json), [trước](logs/checkout-before.json), [sau](logs/checkout-after.json).

Một số lượt dựng runner ban đầu có lỗi chuỗi sitecustomize, đụng tên tệp marker/log và giả định sai về metadata trước spawn/stop. Đã sửa, chạy lại trên fixture mới và chỉ dùng log cuối cùng đã kiểm; không tính các lỗi ấy là finding hoặc mutant kill.

## KHÔNG ĐO ĐƯỢC

- Không tái lập được claim executor **221/221** có/không snapshot, hoặc J01 nguyên bản3/3 trên storage thật, trong sandbox này. Kết quả J013/3 và mutant harness là **có seam materializer**. Không xóa `/tmp/.git`, sửa guard storage hay sửa KHO để làm integration xanh.
- Tám ca venv/pip không chạy: bốn ca `r345_*` phụ thuộc `_r345_venv`, hai ca `r347_*`, hai ca `r348_*`; tên và lý do từng ca có trong dữ liệu suite. Hai ca Windows `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125` và `r484_g4_windows_sid_alias_identity` skip trên Linux. Không suy pass từ việc chúng không đổi mã.
- Native Windows, kernel/ACL/SID/reparse đầy đủ, bootstrap/installer thật, credential/máy chủ thật, toàn bộ bảng mutation launcher, và các gate ngoài phạm vi so delta chưa đo lại. Không dùng các giới hạn này để cộng finding sản phẩm suy đoán.
- Không đọc GitHub, CI exact head, thread resolve, trạng thái wp775 hoặc comment nâng trần từ xa. Assignment hiện tại là thẩm quyền cho attempt5 và lời gọi cuối; blob lease/spec cục bộ chỉ chứng minh nội dung đang có trong object store. Công cụ `environment_status` của skill môi trường không có callable trong phiên; không suy readiness mạng/credential.
- Không xác nhận đủ M-2/M-3/M-4 để merge; không push, đăng verdict lên GitHub, merge, land hoặc deploy. Verdict này không tự tạo receipt `cross_approved` hay thay quyết định chủ kho.
