verdict: changes_requested
reviewed_sha: cc020e02607bc27eb2a815e1ac282380a155820d
spec_sha256: a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b
reviewer_provider: openai_codex
reviewer_model: KHÔNG ĐO ĐƯỢC
execution_surface: codex_cli
transport: machine

Review độc lập PR #714, WP710 r4/g3, lớp `sensitive`, trên tree `8337342d91298bc1660c398c6e18a3f5938c4ad2`. Base Packet `8c98afacb9285aa71e5200739236284f7a190d4f`; lượt 2 `3903e705d230da3a3d7efb2d6bbfd780899d6f40`; g2 đối chứng `52f32dbe158c1416a52260df130b12d4a7bd5249`. PROMPT SHA-256 khớp `cd76b02d6cad8777da875d697d0808cb74d42d7a537e94d086bdcb614734fba4`. Preflight Spec/HEAD/tree khớp và source sạch. Chỉ ghi dưới `goi/` và thư mục tạm `tmp-review-l3/` trong R. Không sửa nhánh executor, không commit/push/đăng GitHub, không LIVE.

**Kết quả chính:** full selftest **1726/1726**, PowerShell/Linux **passed=31 failed=0**, Ruff F **delta=0** theo tập lỗi so với CẢ g2 và lượt 2. Các gate offline xanh. Tuy nhiên còn **5 lớp mở: P0=0, P1=0, P2=3, P3=2**. Bốn lớp lịch sử còn mở là 1/3/7/8; lớp mới 13 là zombie do subreaper. Lớp 5 đóng được cơ chế thiếu phép đo writer thật trong phạm vi offline. Các phản chứng mới không phải lỗi setup và không dùng suite xanh làm bằng chứng đủ.

Hạng **hiện tại** của lớp 1 được hạ P1→P2 có giải thích: các phản chứng invalid JSON từng làm ba đường Python upload đã được chặn; phần còn lại là khác tập chấp nhận giữa wrapper và Python, gồm decoder BOM. Chưa đo được bypass cổng upload mặc định của Python bằng những phản chứng còn lại. Giữ nguyên slug và lịch sử P1, không tuyên bố lớp đã đóng. Lớp cây tiến trình, bao gồm Windows chưa hoàn thành, vẫn P2 vì vi phạm thứ tự/serialization và phục hồi; không có phép đo LIVE để nâng thành một lỗi credential P1.

**Hai trục:** Spec acceptance = `changes_requested`: #2 chưa đồng nhất hết các đường, #4/#6 còn overlap, #1/#8 thiếu bằng chứng host/Windows/LIVE/admission. Standards/Security = `changes_requested`: thời gian cách ly bị dùng thay bằng chứng cây hết sống; subreaper giết nhưng không thu hồi hậu duệ; tài liệu còn khẳng định parity rộng hơn phép đo. Review này không tạo receipt `cross_approved`, không cấp approval/land/LIVE. Protocol §8 yêu cầu quyết định có căn cứ đúng assurance cho từng lớp mở của Packet sensitive; hiện vật không chứa quyết định ấy trên exact head này.

**Cách tái lập.** R là thư mục chứa PROMPT; S=`R/tmp-review-l3`; C=`S/head`; PW=`R/tools/pwsh/pwsh`. C được sao bằng `cp -a cay-kho S/head`, `git -C C config core.abbrev 7`. `measure.py` chạy từ C, đặt `HOME=S/home`, `TMPDIR=S/temp`, `XDG_CACHE_HOME=S/home/.cache`, `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`, thêm `R/tools/pwsh` vào PATH. Các slice PS có TMPDIR riêng dưới S. Python đo thật **3.11.15**, Ruff **0.15.8**, pwsh **7.4.6**, `IsLinux=True`, `IsWindows=False`. `python3 S/measure.py <log> <command...>` lưu lệnh, cwd, rc, elapsed và output ở `logs/`. Driver rc và rc chương trình con được tách riêng bên dưới. Không lấy log trong zip lượt 2 làm kết quả lượt này.

**Inventory tự dẫn xuất, các đường cùng cơ chế.** AST toàn bộ Python dưới scripts được ghi vào `logs/inventory-ast.json`; đọc thêm shell/PS callers. Ba đường gửi NLM đi qua cùng helper `_nlm_files_after_live_canary`, parser và payload guard:

| Đường ở HEAD | Cổng/sink, tệp `scripts/tl_gws.py` nếu không ghi khác | Kết quả đo |
|---|---|---|
| `nlm-auth-stage`, in-place/`--new`, ±force | preflight :1722 → helper :1730 → public upload :1736 | True đúng 1 upload; False/None/invalid JSON/error không upload; force không bỏ cổng |
| `secrets-set --nlm`, ±`--no-public` | helper :1002 → bundle guard :1015 → bundle upload :1019 → public NLM :1040 | Dương 1 bundle + 1 public; no-public bỏ public; các âm parser được chặn |
| `secrets-set` không `--nlm`, bundle đang có NLM | guard :1015 trước :1019 | rc4, 0 upload, không gửi lại NLM chưa kiểm |
| `secrets-stage` có jar | helper :937 → guard :944 → bundle upload :948 | Dương 1 bundle; âm 0 upload |
| `secrets-stage` thiếu jar / opt-out | :924–:930, guard :944 | thiếu jar rc3; `--no-nlm` loại NLM, không né cổng bằng giữ lại payload |
| Wrapper PS | `nlm-credential-refresh.ps1:428/:442/:449/:456/:463` | version→refresh→canary→stage; stage mặc định vẫn tự kiểm trong Python; custom fake StageCommand được dùng để đo số lần gọi |
| Shell stage callers | `nlm-auto-refresh.sh:78`, `nlm-auth-import.sh:208` | Đi qua lệnh Python, không có cổng upload NLM riêng. Auto-refresh nuốt rc; import có pipefail, full outcome chưa đo |

Helper :832–:860 ghim notebook tại :833, gọi probe :845, đọc snapshot sau canary :855; guard :862–:874 so identity payload. Các nhánh sink update/create/fallback nằm trong `_secrets_upload` :637 và `_stage_enc_upload` :1502; lời gọi :1035/:1553 chỉ stage GWS. Caller `_nlm_auth_alive` khác là doctor (`tl_core/ops_misc.py:1182`), vẫn dùng hợp đồng cũ không yêu cầu thân notebook chặt. Đường load/pull/bootstrap/convert là tải/nạp cục bộ, không coi doctor hoặc login-check xanh là bằng chứng guard stage.

**Bảng lớp xuyên lượt.** Hạng các lớp đã đóng là hạng lịch sử. “ĐÃ ĐÓNG offline” chỉ nhận các biểu hiện và fixture đã kiểm, không nghiệm thu Windows hoặc LIVE. Không phát hiện TÁI PHÁT của bảy lớp đã đóng ở lượt 2 trong các phép đo đã chạy.

| # | Slug / hạng | Lượt 3 | Biểu hiện, bằng chứng, hướng vá |
|---|---|---|---|
| 1 | `stage-canary-true-khi-than-rong-hoac-sai-id` / **P2 hiện tại, P1 lịch sử** | **CÒN MỞ**; các hằng/số/surrogate/depth cũ đã chặn | Python :128–:181/:237–:239; PS :224–:282/:345–:371. Ma trận 101 dạng có 8 lệch ở title/name U+001C–U+001F; BOM bị helper cả hai từ chối nhưng qua stdout tiến trình PS thì stage vẫn được gọi. `parity.py` rc0; các HINT slice n rc1 đúng phản chứng. Chốt một tập whitespace và một chính sách decode BOM chung cho mọi đường; kiểm actual stdout, không chỉ helper. |
| 2 | `stage-nlm-ngoai-nlm-auth-stage-khong-qua-canary` / P1 | **ĐÃ ĐÓNG offline** | Helper/guard/sink ba đường ở inventory. Probe payload/bundle/no-jar/no-nlm và selftest xanh; mutant bỏ guard, đổi identity thành equality, giữ NLM khi opt-out đều đỏ đúng `wp714_nlm_bundle_*`. Không nới guard để chữa tương thích caller. |
| 3 | `khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con` / **P2** | **CÒN MỞ / VÁ SINH LỖI MỚI** | PS :97–:145/:188–:221/:266–:284/:414–:427. Khi chủ cũ chết và hậu duệ bỏ marker, Linux chủ mới rc0/staged trong lúc hậu duệ R/S còn heartbeat, record bị xóa. Cách ly hết hạn cũng cho rc0/staged với `tree_unknown` khi hậu duệ thật còn S; Windows success nhánh `not_measurable` vẫn xóa record và đi tiếp. `process-extra.py`, `unknown-native.py`, q projection và HINT r/s chứng minh. Dùng containment tồn tại qua vòng đời chủ (Job Object trên Windows hoặc supervisor đủ quyền trên Linux), chỉ nhả khi chứng minh toàn cây hết; timer chỉ giới hạn thời gian chờ/trả lỗi, không cấp quyền stage tự động. |
| 4 | `phan-loai-loi-doan-bang-chuoi-tu-do` / P2 | **ĐÃ ĐÓNG fixture offline** | PS :375–:385; Tests case c. Bộ 31 ca phân biệt command-name/login-hint/path/traceback/line401/mixed/HTTP/network; logic không đổi lượt 3. CLI thật/taxonomy thực tế chưa đo. |
| 5 | `test-ps1-thieu-rang` / P2 | **ĐÃ ĐÓNG lỗi writer trong phạm vi offline** | Tests :643–:693 đọc record thật, marker :660, floor :681; q :605–:642 có assertion overlap. Control r rc0; mutant marker r rc1 đúng “did not retain its child marker”, mutant floor r rc1 đúng “owner start”. q Linux0/non-Linux projection1 vì overlap. Bảy mutant PS được đo ca đích, không dùng lỗi setup làm tín dụng. Các ca s/u còn thiếu yêu cầu an toàn/thu hồi được báo ở lớp 3/13; Windows native/CI vẫn not_run, không chuyển thành pass. |
| 6 | `bang-chung-spec1-ghi-thieu-buoc-refresh` / P2 | **ĐÃ ĐÓNG evidence offline** | PS :73–:90/:428–:470, Tests k. Có per-step rc/time/timeout/confirmed/tree/cycle, không mang bước chu kỳ cũ sang chu kỳ sau. `profile_bound_to_cli=false` được khai đúng; fingerprint chỉ của đường dẫn cấu hình. Host gốc/CLI thật chưa chứng minh. |
| 7 | `khai-rong-hon-phep-do-trong-changelog-runbook` / **P3** | **CÒN MỞ / VÁ SINH LỖI MỚI**; hướng dẫn xoay secret cũ đã sửa | `changelog.d/wp-710.md:8–:11` khẳng định JSON được Python/PS nhận giống nhau; docstring `tl_gws.py:133/:139/:141` nói BOM/byte decode cùng nghĩa. Parity 101 và BOM actual stdout phủ định khẳng định tổng quát. RUNBOOK :154–:176/:204–:208, ba lời khắc phục GWS :79–:84/:592–:595/:615–:617 nay có điều kiện/`--nlm`; 2 mutant bỏ cờ đỏ đúng test hướng dẫn mới. Sửa phạm vi lời khai thành đúng các dạng/helper/transport đã đo và công khai phần lệch; không dùng “38/0” làm bằng chứng cho mọi đầu vào. |
| 8 | `huong-dan-cu-con-lech-sau-va-ngoai-write-set` / **P3** | **CÒN MỞ**, ngoài 6 paths | `tl_core/cli.py:150` còn hứa force bỏ canary; `nlm-auto-refresh.sh:76–:80` nuốt stage rc4/5 và in NLM sống; `references/COWORK_PROJECT.md:83–:94`, `docs/WORKFLOW_RASOAT_TU_DONG.md:337`, `tl-setup.ps1:63/:98/:99` còn caller/chỉ dẫn thiếu điều kiện mới, Change-Token không kiểm rc. Reuse shell probe: stage4→shell0/printed_alive=true. HINT stage5→shell0, test đỏ; private propagation mutant→test xanh, undo→đỏ. Cần successor có owner cho caller/help/docs ngoài scope; không áp ngoai_write_set.patch. |
| 9 | `powershell-ve-sinh` / P3 | **ĐÃ ĐÓNG các biểu hiện Linux đã đo** | #requires, PSScriptRoot, Get-Command/ArgumentList, pin :462–:463; d/e/k của suite xanh. `.cmd`, codepage, Global namespace/ACL đa user/native API chưa đo. |
| 10 | `ban-chup-credential-doc-truoc-canary` / P3 | **ĐÃ ĐÓNG snapshot gửi upload** | Helper :845/:855 và các callers inventory. Snapshot-after test ba đường xanh; snapshot-before mutant đỏ đúng `wp710_nlm_stage_doc_credential_sau_canary_ca_ba_duong`. Preflight đọc rồi bỏ bytes không được dùng upload. |
| 11 | `stage-error-output-leaks-credential` / P1 | **ĐÃ ĐÓNG các fixture/đường lỗi kế thừa** | Python :263–:281/:877–:890, boundaries của ba command, public/fallback sink; PS Emit :73–:84. Chạy lại fixtures sẵn có: refusal/upload errors không thoát thông điệp thô/traceback; 2 mutant probe-message/containment đỏ đúng các ca suppression; Tests g xanh. Không soạn fixture rò mới, không tuyên bố mọi ngoại lệ chưa thử đều an toàn. |
| 12 | `trusted-notebook-overwritten-by-stage-config` / P2 | **ĐÃ ĐÓNG fixture offline** | Python :817–:830/:833, PS :462–:463. Loader config thật, có/không token env đều probe notebook tin cậy; test hai profile xanh; pin mutant đỏ đúng ca hai profile. Hai secrets commands load config trước entry vẫn cần TL_CANARY_NOTEBOOK_ID, RUNBOOK :789 khai đúng giới hạn. |
| 13 | `linux-subreaper-khong-thu-hoi-zombie` / **P2** | **VÁ SINH LỖI MỚI** vòng 3 | PS :59–:66 nhận orphan; :114 bỏ Z/X; :156–:163 Stop-Process rồi coi gone, không wait/reap các con đã nhận; Tests u :861–:876 cũng chỉ loại Z khỏi alive. Hai chu kỳ daemon rc0; con chu kỳ 1 ở Z/ppid=owner qua 3 snapshot lúc owner đang ngủ, cuối run hai con còn Z trước cleanup harness. HINT v rc1 đúng PID zombie; scratch thêm reap→rc0/passed1, undo→rc1. Thu hồi các adopted children sau khi dừng, phối hợp với Process/.NET để không tranh thu hồi direct child; kiểm không tăng zombie qua nhiều chu kỳ. |

Lớp 1 là cơ chế tập chấp nhận runtime; lớp 7 là lời khai tài liệu vượt quan sát và có thể sửa riêng. Không đếm mỗi Unicode/BOM/nhánh timeout là một lớp. Lớp 13 tách khỏi lớp 3 vì tiến trình đã chết và không còn overlap, nhưng tài nguyên/process entry chưa được thu hồi; hướng sửa và phép kiểm khác containment cây sống.

**Parser — phép đo chi tiết.** `parity.py` lấy đúng bốn hàm bằng AST từ HEAD và đúng đoạn `$CanaryKnownKeys`→`function Classify` của PS, không tái viết parser. Cùng 101 chuỗi JSON được đưa vào hai helper; 93 kết quả khớp, 8 lệch:

```text
title_whitespace_001c/001d/001e/001f: Python=false, PS=true
name_whitespace_001c/001d/001e/001f:  Python=false, PS=true
Python reason=CANARY_BODY_INCOMPLETE
```

Đây là ký tự được escape hợp lệ trong JSON, không phải raw control ký tự ngoài chuỗi. Python `strip()` và .NET `IsNullOrWhiteSpace()` dùng tập khác nhau. Các đối chứng gồm tab/newline/NBSP/Unicode spaces/zero-width/BOM trong title, case keys, biên double, underflow, âm zero, duplicate escaped/nested/array, cặp/lẻ surrogate và độ sâu 63–66. Những dạng invalid cũ được chặn và đối chứng hợp lệ còn dương. Rounds Python mutants bỏ từng chốt constant/float/int/surrogate/depth, hoặc hạ depth xuống63, đều làm đúng ca parser đỏ, không import exception.

Decoder là đường riêng trong CÙNG lớp: helper từ chối chuỗi bắt đầu U+FEFF ở cả hai phía, nhưng fake CLI thực sự in UTF-8 BOM trước thân notebook hợp lệ khiến wrapper vẫn gọi fake stage. `transport-native.py` ghi riêng control_title_001c/control_name_001c/bom_canary: cả ba wrapper rc0/status=staged/stage_calls=1, dùng runtime HEAD không sửa. HINT slice `bom_canary` đỏ đúng assertion canary-zero-stage. Vì vậy lời khai “chưa đo BOM qua tiến trình” của executor đúng là một giới hạn chưa đo; reviewer đã đo và thấy lệch theo hướng wrapper lỏng hơn. `StageCommand` mặc định gọi Python vẫn lặp cổng nên không suy phản chứng wrapper này thành upload credential LIVE.

`parser-probe.py` đo thêm 10 dạng ×3 routes ×2 force =60 dòng command-function, và cùng 10 dạng qua PS. NaN/Infinity/-Infinity/nested duplicate đều rc4, uploads0 trên cả ba đường Python; valid uploads1/2/1. Harness kế thừa cũng chạy lại matrix 25 dạng ở `probe_python.py` và các refusal fixtures. `data_conflict` và `outer_bad_title` vẫn được cả hai nhận: đó là câu hỏi schema envelope với CLI thật, chưa có bằng chứng để kết luận mọi metadata mang tên data là notebook thứ hai. Ghi giới hạn ấy, không tạo lớp từ suy đoán. Chỉ nlm-auth-stage thật sự có CLI --force; force trong hai secrets probes là thuộc tính Namespace để kiểm guard, không khai hai CLI ấy hỗ trợ cờ này.

**Cây tiến trình — đã kiểm mọi nhánh chung trước khi chốt.**

- Khi wrapper còn sống, Linux marked/scrub/nondumpable/version-orphan fixtures không còn heartbeat sau stage; subreaper/parent-link khắc phục được các biểu hiện cũ in-run. `version_orphan` đã được dừng/xác nhận nên được đi tiếp, không còn ghi đè cây chưa xác nhận. Mutant bỏ version-stop đỏ case t với `rc=0 step=stage calls=6`; t baseline trong bộ31 xanh.
- Khi chủ cũ chết, subreaper cũ không còn bảo vệ. `process-extra.py` dùng descendant_exit có sẵn, chỉ đột biến marker của hậu duệ. Marked control: rc5/lock_busy/marked_alive, 0 stage. Scrubbed: rc0/staged, con R/S và heartbeat tiếp tục, record mất. HINT r giữ control marker và thêm biến thể ấy; đỏ đúng “new owner overlapped a descendant of the exited old CLI”. Đây là Linux thật, không phải Windows projection.
- `unknown-native.py` ghép hai fixture có sẵn descendant_exit/nondumpable, dùng runtime không sửa. Lượt đầu rc5/tree_quarantine/tree_unknown/0 stage; sau hạn1, rc0/staged/quarantine_elapsed/tree_unknown, con thật vẫn S và heartbeat, stage_called=true. Python đọc được environ ở mốc trước chủ chết; không dùng quan sát đó để xác định chính PID nào đã làm scan của pwsh unknown. Kết luận được đo là wrapper nhả một thao tác có cây chưa xác nhận trong lúc hậu duệ cũ thật còn sống. HINT s còn tái hiện trực tiếp nhánh .NET đọc environ thất bại, rồi thả live child sau hạn.
- Projection một dòng `$ProcRoot` theo Tests s cũng cho unknown→quarantine→released với con thật còn hoạt động. Tách rõ projection này khỏi phép đo native/Linux ở trên. Default900 không phải upper bound của tuổi tiến trình; chưa chạy chờ900 giây. Tham số1 là giá trị sản phẩm cho phép, không là mutant runtime.
- Windows/non-Linux success: `$tree.State=not_measurable` không thuộc alive/unknown ở :275, nên :280 đặt confirmed=true, :284 xóa record. Projection q rc1 đúng overlap; process-probe nonlinux còn heartbeat_after_stage=true, rc0/staged. Lời khai executor về nhánh này đúng về source/projection, **chưa chứng minh native Windows đã chạy**. Spec #4/#6 vẫn chưa đạt; ưu tiên P2, không được miễn acceptance chỉ bằng RUNBOOK công khai giới hạn. Job Object và đo native là hướng cần thực hiện, không giao runtime hint.
- Timeout không đo được giữ record, version chưa xác nhận dừng ở version; original t xanh và mutant đỏ. Root/marked còn sống chặn; record cũ không marker chuyển sang cách ly kể cả Linux. Ca m xác nhận dead/reused pid không được coi là dead tree, và có lối ra timer. Đây là tăng chặn hợp lệ ở lần đầu nhưng lối ra tự động cùng rủi ro trên, không bằng chứng serialization.
- No-record/marker-gone có đường clear; unreadable/stat/environ được tính unknown; floor/uid/init/kernel lọc phạm vi; zombies bị loại khỏi live set. Record JSON hỏng, clock ngược hoặc root không xác định vẫn chặn, mỗi invocation hữu hạn bởi LockWaitSeconds nhưng cần thao tác phục hồi thủ công. Ca m kiểm record hỏng vẫn rc5 sau bound; không tuyên bố cách ly chữa mọi loại kẹt. Ghi record bằng Set-Content chưa có crash-atomic receipt; cửa sổ chết trước/sau ghi PID và độ đầy đủ của scan chưa đo hết.

Mã **5** của wrapper được trả ra là inconclusive/lock_busy/tree_quarantine, zero operations ở các lượt thực sự bị chặn; lần được released trả0 và thực hiện cả stage. Inventory không tìm thấy caller production trực tiếp gọi wrapper PS trong kho; RUNBOOK :736–:738 ghi đúng rc5. Shell auto-refresh gọi Python stage và nuốt rc4/5, thuộc lớp8; không gán lỗi shell đó cho một caller PS chưa tồn tại. Không coi rc5 của Python containment là cùng outcome với rc5 quarantine của PS.

**Răng của test và thay đổi hướng dẫn.** 16 mutant runtime Python kế thừa +6 mutant parser vòng3 =22/22 đỏ vì assertion đích; 2 mutant bỏ `--nlm` trong RUNBOOK/lời GWS =2/2 đỏ đúng `wp714_huong_dan_secrets_set_kem_nlm`. Có controls xanh, không exception. PS 7 mutant: strict-tree→n/overflow_meta; marker→r/marker; floor→r/owner_start; ignore-unreadable→s/live-root; no-subreaper→u/version; version-continue→t/unconfirmed version; legacy-clear→m/quarantine. Tất cả kết quả cuối rc1 vì đúng property, không dùng lần fixture chưa khởi động làm tín dụng. q projection có răng đối với thiếu containment.

Selftest hướng dẫn mới ở `tl_selftest.py:5212–:5225` đo từng đoạn backtick và có count floor, đã bắt hai mutant bỏ cờ. Nó không kiểm semantics của mọi shorthand, không chạy LIVE GWS remediation, không chứng minh parser parity hoặc process lifetime. Ba lời GWS mới đều có `--nlm`, jar/canary hoặc public-only fallback; đọc code cho thấy chọn đường đó phù hợp payload guard. RUNBOOK mới nói rõ bundle GWS còn cũ khi chỉ sửa public, và `secrets-stage --no-nlm` thay toàn bundle bằng config cục bộ/mất NLM headless. Không phát hiện lỗi runtime mới trong ba lời khắc phục ấy. Chỉ dẫn ngoài write set vẫn còn, thuộc lớp8.

Zombie là lỗi mới có đối chứng đủ: `process-extra.py` daemon keepalive2, cả hai chu kỳ staged/rc0; ba snapshot con1 đều Z/ppid=owner khi owner còn sống. HINT v kiểm trong interval, không phụ thuộc init ngoài wrapper có reap sau exit hay không. Private scratch mutant thêm waitpid cho con đã dừng khiến ca v xanh (`passed=1 failed=0`); bỏ mutant lại đỏ cùng zombie. Runtime đột biến ấy không nằm trong HINT và không được coi là bản sửa đã nghiệm thu toàn bộ .NET/process interactions.

**Spec r4 từng mục.**

| Acceptance | Bằng chứng trên exact HEAD | Kết luận |
|---|---|---|
| #1 host profile, bounded refresh, version/rc/elapsed/fingerprint; âm zero-stage | Bộ31 có refresh nonzero/timeout/missing profile, evidence từng bước; original-host binding khai false; zombie/overlap còn tồn tại | MỘT PHẦN offline; original browser host/CLI/version thực not_measured |
| #2 real notebook/trusted ID/body/parser/auth/network/timeout, âm zero-stage | Pin/body/id/tri-state và invalid JSON cũ đạt; parity8 lệch, decoder BOM wrapper còn gọi fake stage | CHƯA ĐẠT toàn đường; CLI/schema/canary thực not_measured |
| #3 actual command True đúng1, False/None/error/timeout/force zero; None mutant đỏ | Các functions command qua loader và full selftest; none-allows/force-bypass đỏ đúng count tests; snapshot-after cả ba đường | ĐẠT regression offline đã đo, không suy LIVE upload |
| #4 Windows wrapper lock/order/count/stage failure/suppression | Bộ31 order/status/sentinel xanh; Linux owner-death và nonlinux success còn overlap | CHƯA ĐẠT serialization; native Windows not_run |
| #5 distinct machine outcomes; bốn âm zero-stage | c/g và cases timeout/bad-body/stagefail trong bộ31, output suppression fixtures; stage_failure rc6 có thể đã upload | ĐẠT taxonomy fixture offline; CLI thực not_measured |
| #6 keepalive opt-in/bounded/stoppable, hai native Windows processes không overlap, abandoned owner | Default/off/interval/concurrent/abandoned fixtures xanh Linux; live-tree release và q projection đỏ; zombie trong keepalive | CHƯA ĐẠT; Windows native not_run |
| #7 candidate temporary manifest, đủ8 assertions/negative pointer, script included, manifest committed giữ | Selftest r209 xanh; probe183 files/script included/pointers_ok=true/fail0/advisory107/baseline3; pointer nonexistent→mutant_ok=false đúng RUNBOOK→script | ĐẠT offline. Hàm r209 giữ ok1…ok8 và negative probes; source/copy manifest cùng băm |
| #8 native/Python/full gates/admission/review riêng exact head/tree; mock khácLIVE | Có baselinefull/targeted/PSLinux/Ruff/gates/archive smoke; không có native/admission/remoteCI/LIVE receipts | MỘT PHẦN; phần thiếu không là pass |

**Lệnh, rc và output thực tế.** Các driver/harness dưới S có trong EVIDENCE.zip; stdout đầy đủ và command metadata ở logs. Các bản mutant là scratch, không thay tested SHA.

| Lệnh / phép đo | rc thật | Output hoặc receipt |
|---|---|---|
| `sha256sum PROMPT.md SPEC.md`; `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`; `git -C cay-kho status --short` | 0 | băm/HEAD/tree khớp; status rỗng |
| `sha256sum luot2c/VERDICT.md luot2c/HINT.patch luot2c/EVIDENCE.zip`; `python3 -I -m zipfile -e ... S/evidence2` | 0 | VERDICT `7b90932206bf2a6823b1262d3b79847b1544822e48f67fc958f3c97e4b49982e`; HINT `b91a1613f789327331bb4e53cefa3472ce9522feb02a46935ee6a2afed5471b1`; zip `b3f473b01c7d2804de9d9741dc00a9be5cabe6d0a67ca5249a27c55d42264c52` |
| `cp -a cay-kho S/head`; `git -C C config core.abbrev 7` | 0 | bản sao riêng/home riêng |
| `python3 scripts/tl.py --selftest` từ C, qua measure.py | **0** | **1726/1726**, 356.935s; logs/selftest.log/json |
| `PW -NoProfile -File scripts/nlm-credential-refresh.Tests.ps1` từ C | **0** | **passed=31 failed=0**, 350.219s; logs/powershell.log/json |
| `python3 S/ruff-delta.py` | driver0; ruff1 ×6 | gws97/selftest4392 tại g2/l2/head; multiset(code,message) added=[] removed=[] ở cả4 phép so; không khai Ruff tuyệt đối pass |
| `python3 S/parity.py` | 0; PW helper0 | 101 dạng/8 lệch; logs/parity.json, parity-cases.json, exact helper parity-ps.ps1 |
| `python3 S/transport-native.py` | driver0; measurement script0 | title/name U+001C và BOM qua CLI stdout thật: wrapper0/staged/stage_calls1 ×3; logs/transport-native.json. Đây là3 phép đo, không là suite0/0 đã pass |
| `python3 S/parser-probe.py`, lần cuối có assert PS count | 0; PW0 | 60 rows/10 PS rows, nonfinite0 upload, positive1/2/1; logs/parser-commands-final.log/parser-measured.json |
| `python3 S/probe_more.py` | 0; shell0 | pin đúng2 cấu hình; upload errors leaked=false; shell stage4/shell0/printed_alive=true; manifest183/negative pointer |
| `python3 S/mutations-new.py` | driver0; control0; mutant1 ×16 | đúng ca đích, exception=false; logs/mutations-new.json |
| `python3 S/mutations-round3.py` | driver0; mutant1 ×8; docs control0 | 6 parser +2 docs mutants đỏ đúng property; logs/mutations-round3.json |
| `python3 S/process-probe.py` | driver0; wrapper0 ×5 | Linux controls không heartbeat sau stage; projection nonlinux còn S/heartbeat; version orphan được dừng/xác nhận |
| `python3 S/process-extra.py`, lần complete | 0 | marked takeover5; scrubbed takeover0 với con sống; unknown projection5→0 với con sống; zombie2 cycles; logs/process-extra-complete.log/process-extra.json |
| `python3 S/unknown-native.py` | driver0; wrapper5 rồi0 | runtime Linux không sửa, tree_unknown→quarantine_elapsed; con S/heartbeat/stage; logs/unknown-native.json |
| `PS_ONLY=owner_start_missing python3 S/ps-slices.py`; `PS_ONLY=control_r ...`; `PS_ONLY=record_marker_empty ...`, lần final | driver0 mỗi lệnh; target1/0/1 | target đúng owner-start/marker; logs/ps-owner_start_missing.json, ps-control_r.json, ps-record_marker_empty.json |
| `python3 S/ps-remaining.py` | driver0; các child-driver0 | 6 mutant assertions rc1, q Linux0/projection1; marker lần đầu có setup lỗi bị loại, đã đo lại đúng property |
| `python3 S/hint-slices.py` | driver0; expected target1 ×6, repair0, undo1 | n title/name/BOM, r overlap, s live-unreadable release, v zombie; logs/hint-slices.json |
| `python3 S/test_wp710_block.py S/hint-head` | 1 | 12/13 xanh; chỉ `wp714_shell_khong_nuot_stage_rc5` đỏ |
| `python3 S/shell-tooth.py` | driver0; propagation mutant0; undo1 | HINT13/13 với private repair; undo đỏ đúng shell-rc5, stderr=false |
| `python scripts/tl.py workflow-audit --strict --json` | 0 | ok=true, cards26/tasks60/groups11/commands189/errors=[] |
| `python scripts/tl.py golden-test --json` | 0 | ok=true |
| `python scripts/tl.py determinism-audit --strict --json` | 0 | ok=true, 15 checks |
| `python scripts/gen_instructions.py --selftest` | 0 | 44/44 |
| `python scripts/tl.py release-manifest --out S/candidate-manifest.json` | 0 | ok=true, temporary183 files |
| `python scripts/tl.py release-bundle --out S/bundle1.zip --json` và bundle2 | 0/0 | cùng SHA-256 `ceac40b46d060640026b935702797a9af70bd5f1cbaf388711a130907cd3afd3` |
| `python scripts/tl.py release-verify S/candidate-manifest.json --strict --archive S/bundle1.zip --json` | 0 | ok=true/errors=[] |
| `python3 S/check-artifact.py` → giải nén rồi `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | driver0; verify0 | ok=true/errors=[] trong S/unpacked/tra-luat |
| `python3 scripts/pkg_secret_scan.py S/scan` trên6 tệp sản phẩm | 0 | output rỗng theo hợp đồng; không dựng fixture bí mật mới, không suy scanner bao phủ mọi loại secret |
| `git --no-optional-locks -C cay-kho diff --check 3903e70 HEAD`; diff protected paths so base | 0/0 | whitespace sạch, VERSION/committed manifest/nlm-auth.ps1 không đổi |
| `patch -p0 --fuzz=0 --dry-run -d S/hint-final-dry < goi/HINT.patch`; áp thật trên copy đó | **0/0** | đúng2 TEST paths, không fuzz/offset; bytes khớp generated files; Python AST OK |

Dry-run cuối:

```text
checking file scripts/nlm-credential-refresh.Tests.ps1
checking file scripts/tl_selftest.py
```

Apply cuối:

```text
patching file scripts/nlm-credential-refresh.Tests.ps1
patching file scripts/tl_selftest.py
```

**HINT.patch và dữ liệu.** Nhãn: chưa chạy trên cây thật; executor tự tái dẫn xuất, tự đo, tự chịu trách nhiệm commit và khai hint_provenance nếu dùng. HINT chỉ có `scripts/nlm-credential-refresh.Tests.ps1` và `scripts/tl_selftest.py`; unified diff repo-relative không a/b, `# lop:` nối lớp1/3/7/8/13. Dùng lại descendant_exit/daemon/nondumpable và fakes shell có sẵn; thêm biến thể marker/Unicode/BOM và assertion no-release/reap. Không có hunk runtime credential adapter, shell caller, docs, workflow hoặc ngoài write set. HINT n/r/s/v được chạy riêng; không khai full HINT PowerShell đã chạy. Sau cùng chỉ sửa comment giải thích ở HINT, kiểm lại dry-run/apply/byte-match; logic của các ca đã đo không đổi. Các scratch repair waitpid/shell chỉ để chứng minh răng, không được giao làm runtime hint.

**Sai số runner được giữ, không tính finding/pass.** Lần parser command đầu thu PS list rỗng vì ghép helper bỏ mất dòng load rows; kết quả ấy bị loại, đã thêm assert count10 và chạy lại. Hai lần process-extra đầu rc1: thử giảm CAP_SYS_PTRACE bị sandbox từ chối (`setpriv` rc127), sau đó lỗi đặt projection trước khi có PID (`/proc/None/stat`); không escalated, đã sửa driver và đo complete/native riêng. Batch ps-slices đầu bị kết thúc rc137, không có completion receipt; chỉ dùng output target còn lưu và các lượt hoàn tất riêng. Một lượt marker mutant tiếp theo đỏ vì scratch record cũ ngăn fixture khởi động, không được tính có răng; dọn scratch mỗi lần rồi control/marker/floor được đo lại đúng thông báo. make-hint lần đầu rc1 vì anchor mode list không khớp, đã sửa trước dry-run cuối. Không dùng các lỗi này làm lỗi sản phẩm hoặc đổi rc thành pass.

**Phạm vi, authority và KHÔNG ĐO ĐƯỢC.** Diff lượt2→head đúng6 product paths. Diff base→head có thêm5 hồ sơ ops lịch sử ngoài sản phẩm; ngoai_write_set.patch chỉ đọc, không áp. Committed manifest source/copy đều SHA-256 `eff247d5f7b7fa0264a3e41994e1ea5ac772b16383ec7a6277e493869269b39a`. HEAD/tree/status source được kiểm lại, không thay đổi; các nội dung sản phẩm đối chiếu Git blob trong final-integrity.json. Không có snapshot .git/index trước status preflight nên không khai index chưa từng được git refresh stat-cache. Bản untracked nlm-auth.ps1 trên canonical không có trong bundle, nội dung KHÔNG ĐO ĐƯỢC.

Windows native/Windows PowerShell, named mutex/ACL đa user, AbandonedMutexException kernel thật, .cmd/codepage, Job Object/process lifetime native: **not_run**. Projection chỉ chọn nhánh Linux code, không chứng minh kernel Windows. CLI nlm thật/version/schema envelope/browser profile binding, refresh/canary thay jar thật: **not_measured**. LIVE/Drive/deploy: **not_run** theo quyền. Admission/required remote CI/exact-head review receipt/model-serving/session machine evidence: **not_run/not_measured**. Header phiên không cung cấp tên model serving cụ thể; không suy model từ persona GPT-6, tài khoản vận chuyển hoặc executor. Local lease khai g3/offline/Linux và hạn2026-10-08T10:26:45Z; ba readback root được giao không chứa grant comments6035944523/6036110675, không xác minh live GitHub authority. Quyền thực hiện review local này là chỉ thị trực tiếp của user, không tự tạo quyền land hoặc allowance dispatcher.

**Non-convergence.** Tập U lượt2 gồm5 slug; vòng này chỉ lớp5 đóng trọn cơ chế writer/độ mạnh assertion trong offline scope, nên F/U=1/5=20%. Lớp7 sửa hướng dẫn cũ nhưng vẫn có khẳng định parity mới sai; không tính lớp ấy vào tử số. Lượt1→2 trước đó3/8=37.5%, hai tỷ lệ liên tiếp dưới50%; lớp1/3 và các vấn đề ngoài scope xuất hiện qua nhiều lượt. Protocol §12 còn có trần2 Codex review/PR và Review Rescue Checkpoint; lượt3 này thực hiện theo yêu cầu trực tiếp của user, không coi việc đổi prompt/phiên là reset bộ đếm hay tự cấp lượt vá4. Cần quyết định checkpoint có authority trước bước executor/review tiếp theo; có thể thiết kế lại containment, revision/successor hoặc human audit đúng assurance. Không tách stable slice chứa cổng/runtime còn phụ thuộc các lớp đang mở.

**Đề xuất phép thử cho điều phối.** Đo Windows native Job Object, kill-owner và pipe-less/pipe-holder descendants ở mọi bước, concurrent processes/takeover và zero-stage khi không chứng minh toàn cây hết; giữ q đỏ cho tới khi có code/evidence đúng. Đo Linux không có subreaper, owner chết sau/before PID record, real browser unreadable environments, PID reuse/uid transitions, crash giữa Set-Content và recovery; kiểm không tự thả live tree theo timer và không tích zombie qua nhiều cycle. Với CLI thật trên host được cấp quyền, chốt schema data/envelope, stdout encoding/BOM và notebook pin, phân biệt mock với LIVE. Về secret output, dùng những fixture sẵn có để mở rộng đo adapter con/create-update-fallback/exception trước containment và stdout/stderr của mọi frontend; reviewer không soạn payload hay mã rò mới. Tạo successor có owner cho help/caller/setup ngoài write set và cập nhật các luồng phục hồi không có jar.

**Gói cuối.** EVIDENCE.zip:194 entries,383938 bytes, SHA-256 `feb82890755aa8fa9f48b00f6b2b5cb73acba366bb120b84eb20d13aa933c132`, zip CRC kiểm sạch. HINT.patch SHA-256 `7832244d614b839bdb85b380d4405fc4c72a2876eeea0b8b91a489ed355a5078`. `package-evidence.py` rc0; AST các harness Python parse được. Tổng R đo bằng `du -sh` khoảng600 MiB, dưới2 GB. Gói không chứa bản sao repository, binary pwsh hoặc credentials LIVE.
