Reviewed commit: cfd3550b6336eecb6847543a5f33200b57dd81ba
Spec SHA-256: 4a512dd38721c3c4eec7978489ba06485feab32f94a0c5637a085d6c694ba38c
verdict: approve
P0=0 P1=0 P2=1 P3=0

**Approve nội dung theo ngưỡng riêng của chỉ thị lượt 3:** không P0/P1; P2/P3 còn mở được nêu rõ để chủ kho quyết. **H01/P2 chưa đóng**, tiếp nối G02; việc reviewer nêu nó không phải quyết định chấp nhận của chủ kho. Không tuyên bố PR đủ điều kiện merge. Đây là lượt Codex 3/3 cuối theo chỉ thị, không tự cấp thêm lượt hoặc sửa branch.

Đã tự đo HEAD và tree `87ef372ec6d779610a2d7ce9aae74b6a57febafb`, base `653fef3f52f3130dd6f597c1036430ffb807fef1`. Băm SPEC7 `35a81f47dbea985ed867147fbf952be485faf5c3106e9c8afed27a0b41a533e1`, SPEC8 ở dòng 2, VERDICT1 `21671d6efcbf876fc30d75ab48fdf730504fa6ad1054695f03825ef2c4555eee`, VERDICT2 `778dac6507e5ca5f56c90d0d2f61bea4d301c2a34b036af1704d644a4c49ea6c`: đều khớp chỉ thị. Delta lượt 3 đúng ba tệp, +79/−6; không thay `launcher.py`, `codex_cred.py`, `ops/cong_cu_test.py` hoặc workflow.

Reviewer: Codex/OpenAI, thực thi shell trực tiếp qua API/cloud, transport `machine`, không kế thừa context executor. Không có telemetry độc lập để xác nhận model ID/effort/receipt assurance; không tự chứng nhận receipt hay trạng thái `cross_approved` trên GitHub. Môi trường Linux, Python3.13.16, Ruff0.17.1, actionlint1.7.7, sandbox workspace-write, không escalation. Chạy trên `review-copy`, base tại `base-copy`, mutant trong cây tạm riêng; Git `core.abbrev=7`. Runner dùng env allowlist, PATH công cụ cho phép, HOME/USERPROFILE/CODEX_HOME/TMPDIR trong thư mục ra. Không dùng credential thật, không ghi `~/.codex` thật, không gọi agent LIVE, không cài qua mạng, không thao tác GitHub. Quyết định/CI từ URL trong prompt là thông tin đầu vào, chưa được xác minh từ xa.

## ĐỐI CHIẾU LƯỢT TRƯỚC

`R` dưới đây là `python -B ../run_clean.py`, chạy từ `review-copy`. Script/log là hiện vật review, không phải bản vá runtime giao executor. Seam storage được khai riêng, không dùng để nhận suite tích hợp xanh.

| Mục | Phân loại | Phép đo trên head hiện tại |
|---|---|---|
| G01 — bridge tin executable có mặt | **ĐÃ VÁ THẬT** nhánh CLI hỏng mà shell nhận ra bằng version | Helper thật trả False với rc127, rc lỗi có output, rc0 rỗng/trắng, vắng executable, không executable; timeout thực8.02s. Version trên stderr hoặc shim tốt trả True. [helper.log](logs/helper.log). Ca G01 gốc đạt1/1; mutant luôn True chết tại assertion `hong: mong False`. [mutants.log](logs/mutants.log), [ca đích](mutant-g01-always-true.log). Native Windows chưa đo. |
| G02 — fixture scrub dùng installer host | **CHƯA VÁ trọn lớp**; nhánh npm/codex/claude đã vá thật | Ca gốc với seam storage positive PASS, npm không được gọi. Bỏ unset làm chính assertion ca đỏ. Thiếu rg vẫn gọi cargo/apt-get host và ca còn PASS: **H01**, cùng lớp G02, chỉ đếm một P2. [positive](logs/teeth-positive.log), [leak](logs/teeth-leak.log), [cargo](logs/teeth-cargo.log), [apt](logs/teeth-apt.log). |
| F04 tổng thể — bootstrap trước probe | **ĐÃ VÁ THẬT** các nhánh vắng CLI/hỏng version theo r8; không nhận version là credential sống | Hai ca F04 gốc đạt1/1. Có CLI: `codex-version → prepare → bash-version → hook`; CLI hỏng: `codex-version → bash-version → hook → prepare`; hook7 không prepare, prepare hỏng trả13. [order.log](logs/order.log). Installer giả sửa CLI trước prepare; ở bridge hoãn, doctor/status vẫn dùng auth cũ trước prepare, đúng MT12/N14. [bootstrap.log](logs/bootstrap.log). Mutant bỏ hoãn/đảo shell đều chết đúng assertion thứ tự. |
| F01 — state không ghi được, ba lối | **ĐÓNG THEO QUYẾT ĐỊNH r8** | Launcher, cmd_kiem, materializer, mỗi lối hai lần: báo riêng lỗi ghi state; probe vẫn hai lần, auth cũ giữ nguyên. Đúng giới hạn r8, không nhận đã nhớ được qua tiến trình. [positive-retry](mutant-positive-retry.log). Mutant nuốt/gộp lỗi đều chết. |
| F02 — token_invalidated | **ĐÃ VÁ THẬT** trong phạm vi đo | rc1 hoặc rc0 + marker stdout + từ chối stderr đều ghi rejected, lần sau chặn, chỉ một probe. Mutant bỏ chữ ký chết tại assertion. [positive-rejection](mutant-positive-rejection.log). |
| F03 — probe A nhưng ghi nhầm B | **ĐÃ VÁ THẬT theo r8** | Cả launcher/cmd_kiem ghi A, không ghi hoặc chặn B; hai mutant đọc lại sau probe đều chết. [positive-rejection_race](mutant-positive-rejection_race.log). AST xác nhận call launcher3216 truyền da_probe, codex_cred524 truyền raw. [mark-calls](logs/mark-calls.log). Fallback đọc trước không được giữ hành vi cũ theo MT9; không nhận đã đóng mọi race. |
| CAS / Q3 | **NỢ ĐÃ CÓ QUYẾT ĐỊNH**, không đếm finding mở | Unit dùng dirfd/read/write thật, bỏ riêng constructor bị guard: đọc hai lần, giữ concurrent. Mutant bỏ đọc lại ghi đè và chết tại assertion. [positive](mutant-positive-cas_unit.log), [mutant](mutant-g7_bo_doc_lai_truoc_replace.log). Vẫn là **thu hẹp**, không thành CAS. |

## H01 — P2 — Fixture vẫn gọi installer rg của máy chạy

- Tiếp nối **G02**, slug `hook-scrub-test-unisolated-bootstrap`. Một lớp mở, một biểu hiện còn mở; không cộng lại G02. Đây là biểu hiện bổ sung được đo ở lượt3, không phải lớp nguyên nhân mới.
- Vị trí: `.claude/dev/launcher_test.py:7521–7535` chỉ giả codex/claude/npm, giữ các thư mục PATH không chứa ba tên ấy; assertion dòng7547 chỉ bắt `NPM`. Hook `.claude/hooks/session-start.sh:187–197` còn cài ripgrep bằng apt-get/cargo.
- **Phép đo:** `R python -B ../review_teeth.py cargo` và `... apt`, runner đều rc0. Không sửa hook hoặc thân ca. Chỉ đưa công cụ host giả lên PATH trước khi fixture tự lọc, thay riêng materializer ở project tạm bằng writer inert vì storage bị guard. Giữ mọi assertion gốc.

  ```text
  positive: PASS, shell_rc=0; host_installer_calls=[]
  cargo:    PASS, shell_rc=0; host_installer_calls=['cargo install ripgrep']
  apt:      PASS, shell_rc=0; host_installer_calls=[
      'apt-get install -y -qq ripgrep', 'apt-get update -qq',
      'apt-get install -y -qq ripgrep']
  ```

- Installer giả chỉ ghi log/trả1. Bản thật có thể cài/mở mạng/chậm tới timeout30 khi PATH còn installer nhưng không có rg chạy được. Lời khai fixture kín với installer máy chạy còn rộng hơn phép đo. Không nhận đã thấy mạng thật hoặc đo timeout installer ở lượt này.
- Actionlint cũng chưa được giả, nhưng project fixture không chép `ops/cai_actionlint.sh`: nhánh ấy gọi script vắng rồi cảnh báo, chưa có bằng chứng tải actionlint thành công. Không tính suy đoán đó thành finding khác.
- **Chủ thể quyết định: chủ kho Issue #484.** Hướng xử lý để chủ kho quyết: fixture cung cấp công cụ phụ giả chạy được (ít nhất rg/actionlint), PATH cho phép; mọi installer ngoài dự kiến phải làm ca đỏ. Giữ kiểm materialize đúng một lần, child sạch, child sau materialize và mutant rò snapshot. Hoặc chấp nhận giới hạn bằng quyết định có link. Chưa xác minh quyết định chấp nhận H01; không tự ghi nó thành nợ đã chấp nhận.
- **Đối với verdict:** H01/P2 được nêu rõ theo ngưỡng riêng `prompt.snapshot` lượt3, nên không tự nâng thành P1 để chặn approval. M-1 gốc vẫn cần quyết định chủ kho cho P2 này trước khi nhận đủ điều kiện merge.

## Giới hạn G01 đã kiểm

Version đạt không chứng minh exec/credential dùng được. Fixture độc lập chạy helper, bridge, materializer, probe thật và thay riêng storage bằng store bộ nhớ: version tốt nhưng exec127 ⇒ bridge13, chưa tới shell, auth cũ giữ, lý do `CHƯA ĐO ĐƯỢC probe`, không kết luận auth hỏng. [version-exec-fail.log](logs/version-exec-fail.log). Shell cũng dùng phép thử version, nên chưa có phản chứng rằng đi qua hook sẽ cài lại/sửa được trường hợp này. Đây là giới hạn fail-closed, không phải credential được chấp nhận nhầm hoặc blocker mới đã chứng minh.

Child version nhận stdin DEVNULL, argv chỉ đường CLI/`--version`, env tường minh đã gỡ mọi khóa case-insensitive CODEX_AUTH_JSON. Canary canonical/mixed-case đều không tới child; bash/hook sạch trong cả hai nhánh. Không thấy đường truyền raw snapshot qua env/argv/stdin này. Snapshot còn trong bộ nhớ bridge để materialize sau hook. Không soạn payload đọc bộ nhớ/proc cha, không nhận đã cô lập executable ác ý hoặc mọi cây tiến trình. Timeout đo tiến trình đơn, không nhận kill cả cây.

OSError chuyển thành False rồi hoãn. Seam đường `.cmd` giả đo nhánh OSError, **không phải** kiểm PATHEXT/CreateProcess native. Ca G01 mới skip Windows; hai ca bridge cũ mock helper, nên chúng không chứng minh helper mới chạy được với npm `.cmd` thật.

## Bảng hướng thử

| Hướng thử | Lệnh / bằng chứng | Kết quả |
|---|---|---|
| CLI rc127/rỗng/trắng/rc lỗi có output | `R python -B ../review_probe.py helpers` | False, không tin chỉ có executable |
| CLI treo version | Cùng lệnh | False sau8.02s |
| Snapshot tới version child | Helper và `... review_probe.py order` | Env canonical/mixed-case sạch, stdin null, argv sạch |
| Thứ tự có/vắng CLI, hook hỏng | `R python -B ../review_probe.py order` | Năm tổ hợp đúng thứ tự và rc0/7/13 |
| Version đạt, exec hỏng | `... review_probe.py version_exec_fail` | rc13, giữ auth cũ, không mark rejected nhầm |
| Installer sửa CLI vắng/hỏng | `R python -B ../review_checks.py bootstrap` | Installer trước prepare; child sạch; cuối có auth mới |
| G01 luôn True | `R python -B ../review_mutants3.py` | Chính ca G01 đỏ tại assertion |
| F04 bỏ hoãn/đảo shell | Cùng lệnh | Hai ca thứ tự gốc đỏ tại assertion |
| G02 scrub/bỏ unset | `R python -B ../review_teeth.py positive`, `... leak` | Positive đạt, mutant chết bằng assertion ca |
| G02 thiếu rg, host cargo/apt | `... review_teeth.py cargo`, `... apt` | Ca PASS dù gọi installer ⇒ H01 |
| F01/F02/F03 và CAS | `... review_mutants3.py` | Controls đạt, sáu mutant liên quan chết tại assertion |
| Ca status giải UTF-8 | Positive `r484_g7_credential_status_home_sai_la_chan_khong_traceback` | 1/1, Chan13 không traceback trên Linux; chưa đo Windows |
| Mất/trùng ca sau đổi mock | `python -B run_clean.py python -B review_static.py` | 220→221 ca,248→248 mutant, không trùng, một bảng |
| Lint/doctrine/ADR tăng nợ | Ruff F và hai scan head/base | DeltaF=0; scan đều rc0 |

## Đã đo

- Tạo VERDICT.md sớm rồi cập nhật. Đọc chỉ thị, r7/r8, hai verdict trước, hướng dẫn kho, handoff, delta lượt3 và các đường runtime liên quan. Không dùng tổng suite để đóng từng finding.
- Full launcher không snapshot và có snapshot inert: mỗi lượt **rc1, 199/211 chạy đạt, tổng221, skip10, fail12**, cùng tập tên fail/skip. Lệnh `R python -B .claude/dev/launcher_test.py` và `python -B ../run_clean.py --fake-snapshot python -B .claude/dev/launcher_test.py`. [launcher](logs/launcher.log), [launcher-fake](logs/launcher-fake.log). Mười một ca lỗi storage/recovery như lượt trước; scrub thứ12 dừng sau materializer vì guard, không còn timeout npm. Không coi chúng là hồi quy sản phẩm đã chứng minh.
- Full codex_cred: `R env CC_CHI_TIET=1 python -B .claude/dev/codex_cred_test.py`, **rc1, nền13/18**. t6/t9/t15/t16/t18 lỗi storage/setup; phase18 mutant không chạy vì nền đỏ. [cred.log](logs/cred.log). Không nhận toàn bộ t15 xanh khi nửa home đã tồn tại bị guard.
- Helper/order/version-exec-fail/bootstrap/storage và bốn mode teeth đều **runner rc0** với marker/assertion như log. Storage rc0 chỉ xác nhận quan sát được KHÔNG ĐO ĐƯỢC, không phải storage pass.
- `R python -B ../review_mutants3.py`: **rc0, chín mutant** trong cây/tiến trình riêng chết bằng assertion đích; chín positive controls rc0. Cộng mutant scrub qua teeth là **10 mutant assertion**, không phải toàn bảng248 launcher/18 codex_cred. [mutants.log](logs/mutants.log). Helpers reviewer lượt2 `review_checks.py`/`review_mutants.py` được đọc lại và chạy trên head mới; `review_mutants3.py` cập nhật neo G01/F04. Không tính ImportError/AttributeError/SyntaxError là kill. `-B` và PYTHONDONTWRITEBYTECODE=1 áp dụng mọi mutant.
- `R python -B .claude/dev/packet_loop_test.py`: **rc0, nền343/343**, skip1 Windows/pwsh; tổng **ĐẠT**. Bảng344 ca,106 mutant,78 lớp lách,35 ca bắt oan; mutant gắn ca Windows skip được báo riêng, không nhận là đã giết. [packet.log](logs/packet.log).
- `R env CONG_CU_TEST_BAN_KINH=manh python -B ops/cong_cu_test.py`: lần đầu rc1 vì runner thiếu basename. Sau bổ sung basename, full **rc1,55/56**, cổng cây thật **ĐẠT**, tự kiểm giàn giáo/song song đạt; t5 đỏ vì runner thiếu od. [tools-rerun.log](logs/tools-rerun.log). Bổ sung od vào PATH runner rồi chạy riêng hàm t5 nguyên bản: **rc0,1/1**, không đổi mã. [tools-t5-control.log](logs/tools-t5-control.log). Không nhận đây là một lượt full56/56 hoặc full rc0. Toàn470 mutant giao job mảnh, không chạy ở tiến trình này.
- Static: `python -B run_clean.py python -B review_static.py` **rc0**. Bare Ruff `python -B -m ruff check --no-cache --select F --output-format json` trên năm tệp Python: head/base đều rc1, cùng năm F841 tại launcher_test, **DELTA=0**; bốn tệp kia0. `bash -n` hook và `actionlint -shellcheck=` workflow mỗi lệnh rc0; kiểm tĩnh, không phải Windows/ShellCheck. Inventory ca/mutant: master197/233, lượt1 216/246, lượt2 220/248, head221/248; không trùng tên, mỗi cây một bảng DOT_BIEN. [static.log](logs/static.log).
- `R python -B .claude/dev/packet_loop.py doctrine-scan --root .` và `... adr-song --root .`: head/base đều **rc0**. Doctrine10 tệp/0 chỗ; ADR50/50 cùng ngoại lệ0016. [doctrine head](logs/doctrine-scan-review-copy.log), [base](logs/doctrine-scan-base-copy.log), [ADR head](logs/adr-song-review-copy.log), [base](logs/adr-song-base-copy.log).
- Audit đầu/cuối KHO: HEAD/tree đúng, status cả ignored/untracked, diff HEAD/index và danh sách ngoài index đều sạch, tất cả rc0. SHA-256 **3686 tệp tracked** không đổi. [checkout-before.json](logs/checkout-before.json), [checkout-after.json](logs/checkout-after.json). Không sửa checkout/branch executor; marker hook/cache/mutant ở cây ngoài KHO. Snapshot chỉ chứng minh không có delta quan sát giữa hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.

## KHÔNG ĐO ĐƯỢC

- **Storage tích hợp:** `/tmp/.git` tồn tại; constructor _KhoCodex từ chối home dưới /tmp: `OSError: Codex home is inside a repository`. [storage.log](logs/storage.log). Không xóa guard hoặc vá constructor để suite xanh. Store bộ nhớ/unit bỏ constructor không chứng minh ACL/kernel/reparse hoặc chống race toàn hệ thống.
- Chưa tái lập claim executor launcher219/219 hoặc codex_cred18/18 +18/18. Mười skip launcher: Windows t62/SID alias và tám ca venv/pip (bốn r345,hai r347,hai r348), tên đầy đủ ở hai log suite; skipped không phải passed.
- Toàn248 mutant launcher,18 mutant codex_cred và470 mutant công cụ chưa chạy. Không nhận các mutant định hướng thay cho toàn bảng. Không có một lượt full cong_cu rc0 trong phép đo này; có kết quả full55/56 và đối chứng t5 sau sửa runner.
- Windows native/PATHEXT/.cmd, SID/ACL/share-delete, CI xanh exact head: chưa đo. Claim launcher-windows xanh tại7cc31e9 không thay kết quả cfd3550, vì helper G01 được thêm sau commit đó. Windows t23/t49 đỏ sẵn chỉ là lời khai executor; diff không đụng ops xác nhận phạm vi thay đổi, không chứng minh baseline Windows đỏ sẵn.
- Resolve thread/lease GitHub, wp775 land/nhả tệp, master mới và M-2/M-4: chưa xác minh trực tiếp. Không suy model/session assurance từ tài khoản vận chuyển verdict.
- Bootstrap/npm/Codex/server credential thật không đo. Mọi credential/tool trong phản chứng đều inert. Hướng cần payload nhạy cảm chỉ mô tả bằng lời, không soạn payload.

## Điều gì CHẶN, điều gì để chủ kho quyết

**Approval nội dung lượt3:** không tìm thấy P0/P1. H01/P2 được nêu rõ để chủ kho quyết nên verdict approve theo ngưỡng riêng đầu vào; G02 chưa đóng trọn lớp. Không biến thiếu phép đo Windows hoặc version không bảo đảm exec thành lỗi chức năng chưa chứng minh. Nợ `codex-auth-json-khong-cas` Q3 và `codex-rejected-state-khong-ghi-duoc` r8 đã có quyết định, không đếm lại.

**Chưa đủ điều kiện merge:** cần quyết định có link cho H01/P2 theo M-1 gốc; readback thread M-2; CI xanh + Windows exact head M-3; wp775/master M-4. Reviewer không miễn những gate này, không merge/land/push, không tự gọi Codex lượt4. Head đổi thì verdict/CI cũ stale theo M-5.
