verdict: changes_requested
reviewed_sha: 80947fc16bee1d4ae0571986bcfecbfcb52223b2
spec_sha256: a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b
reviewer_provider: openai_codex
reviewer_model: KHÔNG ĐO ĐƯỢC
execution_surface: codex_cli
transport: machine

Review độc lập PR #714, WP710 r4/g3, lớp `sensitive`. Tree đã đo: `299f248658549090d414e3d1d76e1f3eba06ab85`; base Packet: `8c98afacb9285aa71e5200739236284f7a190d4f`; g2 đối chứng: `52f32dbe158c1416a52260df130b12d4a7bd5249`, tree `6deaa0b62016983c4d51cb28ba599660ff140464`. PROMPT SHA-256: `c6144ec6866aface83fea616b1c3e3083a23e7e8599476d3b7a1235c6b66f26b`. Preflight khớp tất cả các băm bắt buộc, checkout nguồn sạch trước và sau review. Không sửa nguồn, không đăng GitHub, không push, không LIVE.

**Có 8 lớp còn mở: P1 ×3, P2 ×3, P3 ×2; P0 = 0.** Trong mười lớp lượt trước, sáu còn mở, bốn đóng trong phần có phép đo Linux; thêm hai lớp mới phát hiện ở g3. Tổng danh mục hiện tại 12 lớp = P1 ×3, P2 ×5, P3 ×4, trong đó bốn lớp đã đóng = P2 ×2 + P3 ×2. Đếm theo cơ chế, không đếm số đường dẫn/biểu hiện. Lỗi notebook bị config ghi đè được tách khỏi lớp vệ sinh PowerShell để không đếm hai lần.

Selftest và gate offline xanh không đóng các lớp an toàn: Python vẫn stage với mảng JSON chứa nhiều notebook; bundle có NLM vẫn có nhánh không đi qua canary; tiến trình cháu vẫn chạy chồng sau timeout; lỗi canary lọt ra log của cả ba lệnh. Một mutant timeout sai còn qua nguyên bộ PowerShell 23/23. Model phục vụ cụ thể và session/run header: **KHÔNG ĐO ĐƯỢC**, không suy từ tên tài khoản hay lời khai persona. Verdict này không tạo `cross_approved`, không cấp quyền land/LIVE.

**Hai trục.** Spec acceptance: `changes_requested` — #2, #4, #6 chưa đủ; #1 và #8 chỉ có bằng chứng offline/một phần. Standards/Security: `changes_requested` — cổng không phủ toàn bộ payload, parser chưa từ chối trả lời mơ hồ, cây tiến trình chưa được tuần tự hóa đầy đủ và rò văn bản lỗi. Áp §8 cho lớp sensitive: từng finding mở cần sửa hoặc quyết định chấp nhận có căn cứ, đúng assurance; chưa có quyết định ấy trong hiện vật giao cho reviewer.

**Đối chiếu từng acceptance của SPEC r4.**

| Mục | Kết quả đo | Trạng thái |
|---|---|---|
| #1 refresh trên host gốc, bounded, version/rc/elapsed/fingerprint; refresh lỗi/timeout/profile thiếu ⇒ 0 stage | Suite PS gốc đạt; từng bước có rc/elapsed thật và fingerprint khai rõ là băm đường dẫn, `profile_bound_to_cli=false`. Pipe-read timeout được giới hạn. Tiến trình cháu không bị ràng buộc vòng đời. CLI thật, fingerprint nội dung hồ sơ và host Windows gốc không được đo. | MỘT PHẦN; lớp 3 mở, lớp 6 đóng phần evidence |
| #2 notebook thật, ID tin cậy, thân JSON; sai/rỗng/parser/auth/network/timeout ⇒ 0 stage | Thân rỗng, garbage, sai ID đơn, thiếu title đều bị chặn ở Python. Mảng nhiều phần tử và ID mâu thuẫn vẫn dương. PS nhận title bool/mảng/object/whitespace và id mảng. Config token có thể đổi ID đã được wrapper truyền. | CHƯA ĐẠT; lớp 1, 12 |
| #3 lệnh stage: True ⇒ đúng 1 upload; False/None/ngoại lệ/force ⇒ 0; mutant None phải đỏ | Ca `wp710_nlm_stage_true_only_upload_count` xanh; mutant `is False` làm chính ca ấy đỏ, rc1. Positive của cả ba lệnh có đúng một lần vào canary; nlm-auth-stage 1 upload, secrets-set 2 sink (bundle + public), secrets-stage 1 bundle. Giá trị True vẫn chưa đủ chặt theo #2. | ĐẠT phần command guard/upload count; #2 chưa đạt |
| #4 wrapper refresh→canary→stage dưới một lock; order/count/stage_failure/sentinel | Suite PS 23/23; mutant đảo thứ tự đỏ vì `got notebook,auth,stage`; stage lỗi trả rc6. Sentinel stdout/stderr của wrapper bị giữ kín. Con cháu vượt vòng đời chủ; sentinel của Python stage rò. | MỘT PHẦN; lớp 3, 5, 11 |
| #5 các status phân biệt, bốn outcome trước stage có 0 stage | Các chuỗi lỗi cũ, traceback line 401, HTTP401/503, mixed signals được suite kiểm; allow-list mới không dựa vào từ auth/login/cookie trần. Timeout/auth/network/inconclusive chính của wrapper fail-closed. | ĐẠT các fixture offline đã chạy; không suy nhãn CLI thật từ mock |
| #6 keepalive off mặc định, opt-in/bounded/stoppable, native Windows không overlap, abandoned takeover | Ca mặc định/opt-in/interval, concurrent, dead/reused/live PID và record hỏng xanh trên Linux; mutants opt-in/interval/record đỏ. Phản chứng con cháu còn heartbeat sau stage của chủ mới. | CHƯA ĐẠT; Windows native và abandoned exception KHÔNG ĐO ĐƯỢC |
| #7 r209 manifest tạm, 8 assertion và negative probe, script mới, 0 pointer failures, manifest committed giữ nguyên | Đo 183 tệp; script có trong manifest; pointers_ok=true, fail=[], advisory=107, baseline=3. Thay con trỏ RUNBOOK thành tệp không có ⇒ pointers_ok=false, đúng cặp fail. Cả tám biến ok1…ok8 và negative probe còn nguyên; selftest xanh. | ĐẠT |
| #8 ghi riêng native/Python/full gates/admission/review theo exact head, phân biệt trạng thái | Python/full gates/Linux pwsh đã chạy và có output dương dưới đây. Native Windows, admission trên g3, required checks GitHub trên g3, LIVE không chạy. Readback cung cấp chủ yếu g2; không coi CI/admission g2 là g3. | MỘT PHẦN; chưa đủ assurance/acceptance cuối |

Write-set: `git diff --name-only 52f32db HEAD` chỉ sáu đường sản phẩm đã cho. So base có thêm năm hồ sơ ops lịch sử; không tính chúng là sửa sản phẩm của g3. `RELEASE_MANIFEST.json`, VERSION và `scripts/nlm-auth.ps1` không có diff so base. Manifest committed SHA-256 nguồn/bản sao cùng `eff247d5f7b7fa0264a3e41994e1ea5ac772b16383ec7a6277e493869269b39a`. Không chạm untracked script của máy canonical; bản đó không nằm trong bundle để đo nội dung. Quyền grant g3 được dẫn trong lease; readback đã giao không chứa hai comment 6035944523/6036110675, nên nội dung hai comment đó không được xác minh độc lập. Chỉ thị reviewer hiện tại của user neo exact head là phạm vi công việc phiên này.

**Danh sách đường stage tự dẫn xuất.** `probe_python.py` duyệt AST mọi `.py` trong scripts; đối chiếu với `rg -n 'nlm-auth-stage|secrets-set|secrets-stage|nlm_cred\.enc|tl_secrets\.enc' scripts` và đọc các shell/PS wrapper. Danh sách không lấy từ báo cáo executor.

| Đường/payload | Sink và cổng hiện tại | Kết quả |
|---|---|---|
| `cmd_nlm_auth_stage`, mới/in-place/force | tl_gws.py:1496 preflight → :1504 helper → :1510 `_stage_enc_upload` | Canary 1 lần khi dương, upload 1; parser nhiều notebook còn hở |
| `cmd_secrets_set --nlm`, bundle + public, ±no-public | tl_gws.py:782 preflight → :787 helper → :798 bundle, :819 public | Dương: 1 gate, 2 sink; nonpositive chặn cả hai |
| `cmd_secrets_set` đổi token/webapp/gws nhưng không --nlm, bundle cũ đã có nlm_auth | tl_gws.py:765 đọc bundle → :770/:772/:774 đổi trường → :798 upload lại nguyên nlm_auth | 0 gate, rc0, bundle mang NLM vẫn upload |
| `cmd_secrets_stage`, jar có | tl_gws.py:726 preflight → :729 helper → :739 bundle | Dương: 1 gate, 1 upload; nonpositive chặn |
| `cmd_secrets_stage`, jar thiếu/config đã có nlm_auth/--no-nlm | tl_gws.py:710 full config → :724/:726 bỏ nhánh gate → :738/:739 upload | Có NLM trong config: upload NLM với 0 gate, kể cả --no-nlm; config thường không có NLM: mặc định rc0 ghi đè bundle thiếu NLM |
| Shell gọi stage | nlm-auto-refresh.sh:78; nlm-auth-import.sh:208 | Đi qua lệnh Python; không có sink Drive credential riêng ở shell. auto-refresh nuốt rc4; import chuyển stderr qua tail/sed |
| PS gọi stage | nlm-credential-refresh.ps1:10/:183 | Wrapper probe thêm trước stage; lệnh Python vẫn có gate riêng. Probe wrapper không thay cổng upload |

Hai helper lá có nhánh cập nhật/tạo/fallback: `_secrets_upload` tl_gws.py:497/:499; `_stage_enc_upload` :1294/:1302/:1309. Không có gate ở sink; sự an toàn phụ thuộc mọi nhánh dựng payload ở trên. AST cũng tìm :814/:1332 là upload GWS riêng, không phải NLM. Các `nlm-auth-load/pull`, bootstrap, env-reimport/tl_fetch là đường đọc/nạp hoặc hướng dẫn gọi, không phải sink NLM mới. Chỉ có hai caller production `_nlm_auth_alive`: helper stage tl_gws.py:680 và doctor ops_misc.py:1182; các caller khác là test.

**Mười lớp của lượt trước, tự đo lại.** Dòng là của HEAD g3. “ĐÃ ĐÓNG” chỉ cho lỗi cụ thể có phép đo; không đồng nghĩa native Windows/LIVE đã được nghiệm thu.

| # | Slug, hạng lượt trước | Phân loại | Biểu hiện/phép đo/hướng xử lý |
|---|---|---|---|
| 1 | `stage-canary-true-khi-than-rong-hoac-sai-id` — P1 | CÒN MỞ | tl_gws.py:127/:132/:171/:175; nlm_cli.py:299/:301 bỏ các phần tử sau phần tử đầu; PS:173/:174/:175/:176/:177. 50 dòng ma trận, garbage/rỗng/sai ID đơn đều chặn; `[đúng,sai]`, `[đúng,{}]`, `[đúng,đúng]` vẫn rc0 upload=1 với cả force; hai ID mâu thuẫn vẫn nhận. PS các kiểu title/id sai vẫn status=staged. HINT body case đỏ đúng assertion. Giữ raw envelope/cardinality trước khi notebook_get làm mất dữ liệu, cho phép duy nhất object/singleton không mâu thuẫn, title/name là chuỗi khác trắng; không chỉ kiểm raw đã bị rút còn phần tử đầu. |
| 2 | `stage-nlm-ngoai-nlm-auth-stage-khong-qua-canary` — P1 | CÒN MỞ; VÁ SINH LỖI MỚI ở output, tách lớp 11 | tl_gws.py:710/:724/:726/:737/:739; :765/:770/:772/:774/:780/:798; cổng :729/:787. Ba đường local jar chính được vá thật (canary 1 lần trước sink). Nhưng payload có nlm_auth từ remote/config vẫn upload với 0 gate; no-jar mặc định ghi đè bundle thiếu NLM với rc0. HINT payload case đỏ. Đặt invariant ở payload trước mọi sink: không gửi lại credential chưa được xác nhận; jar thiếu mặc định phải dừng, --no-nlm phải thật sự bỏ nlm_auth khỏi config. Nếu owner muốn miễn việc republish remote credential, cần exception có tên/owner/authority, hiện không có. |
| 3 | `khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con` — P2 | CÒN MỞ | PS:23/:47/:52/:79/:81/:88/:92/:94/:101/:142/:146. Pipe wait đã bounded; direct-child record có kiểm PID/start time, ca b/m xanh. Nhưng timeout khi root đã thoát trả child_confirmed_exited=true, xóa record trong khi cháu sống. Đo rc3 wall=2.872s, descendant_alive=true, record=false; B rc0 staged và heartbeat sau B stage=true. HINT o rc1 đúng lỗi overlap. Ràng buộc/toàn bộ cây hoặc bằng chứng mọi descendant đã kết thúc trước takeover; tránh khoảng trống spawn→record. Record theo temp user không đủ bao phủ host nhiều user. Native Windows không được đo. |
| 4 | `phan-loai-loi-doan-bang-chuoi-tu-do` — P2 | ĐÃ ĐÓNG | PS:106/:110/:111/:112/:113/:114, :162/:169. Case c kiểm tám fixture, control rc0; mutant regex auth/login/cookie trần rc1 vì err_conn_reset bị inconclusive thay vì network_failure. Ba ví dụ cũ và mixed/HTTP/traceback đạt. Nhãn vẫn là allow-list văn bản có giới hạn, RUNBOOK:713 đã khai đúng; chưa đo taxonomy CLI thật. |
| 5 | `test-ps1-thieu-rang` — P2 | CÒN MỞ | Tests.ps1:302/:304 chỉ đo wall của linger, không kiểm status/zero-stage/kết thúc descendant; :308/:323 không đòi B thành công sau takeover; suite chưa chạy native Windows/không có workflow tham chiếu Tests.ps1. Tám mutant chọn lọc bị giết đúng lý do, nhưng mutant “root đã thoát ⇒ timeout=false rc=0” sống qua NGUYÊN BỘ 23/23, rc0. Thêm assertion outcome/zero-stage/cây tiến trình (HINT o), đòi bằng chứng dương ca takeover; chạy native Windows, đưa CI vào successor đúng write set hoặc nợ có owner. Không tính nhánh AbandonedMutex đã được phủ trên Linux. |
| 6 | `bang-chung-spec1-ghi-thieu-buoc-refresh` — P2 | ĐÃ ĐÓNG | PS:24/:29/:31/:32/:34/:38/:148/:159/:166/:185, Tests:331 và RUNBOOK:690. Output có rc/elapsed/timeout/exited riêng cho version/refresh/canary/stage, cycle; lỗi refresh rc7 không có step sau. Mutant bỏ xóa evidence chu kỳ cũ rc1 đúng “cycle 2 evidence carries stale steps”. Fingerprint băm đường dẫn và không bind CLI được khai tường minh; không gọi nó là fingerprint nội dung hồ sơ. |
| 7 | `khai-rong-hon-phep-do-trong-changelog-runbook` — P3 | CÒN MỞ | RUNBOOK:699 nói mọi status khác staged có “0 lần stage”, trái với stage_failure; PS:183/:186/:187 đã gọi stage rồi mới báo lỗi. Đo fake stage rc9 ⇒ wrapper rc6, status=stage_failure, steps gồm stage. Câu cuối :711 “kiểm Drive” đúng nhưng không sửa được heading sai. Phân biệt gọi stage, upload đã thử và upload đã xác nhận; ghi rõ stage_failure không bảo đảm zero upload. Các mô tả profile, lock giữ qua sleep, stage defaults đã sửa. |
| 8 | `huong-dan-cu-con-lech-sau-va-ngoai-write-set` — P3 | CÒN MỞ | cli.py:150 help force vẫn hứa bỏ canary; nlm-auto-refresh.sh:76/:78/:79/:80 nuốt lỗi stage và dùng login-check/count báo sống. Chạy NGUYÊN script với nlm/gws/python giả: stage trả4 nhưng shell rc0, printed_alive=true. Ngoài sáu đường: không sửa. Cần successor/nợ có owner để cập nhật help và để wrapper báo rc/thất bại; lịch secrets-set ở COWORK_PROJECT:83 vẫn cần hướng dẫn outcome mới. |
| 9 | `powershell-ve-sinh` — P3 | ĐÃ ĐÓNG phần đã đo; phát hiện mới tách lớp 12 | PS:1/:10/:125/:126/:127/:133/:134/:176/:183; Tests:1/:115 và setup fake. Đã đổi biến tự động, #requires, neo PSScriptRoot, case-sensitive ID, command resolution và timeout spawn; ca d/e/k xanh. Probe stage nhận env đúng trong fake con. Shim .cmd, API trên từng phiên bản PS7 và Windows native KHÔNG ĐO ĐƯỢC; không xác nhận lời RUNBOOK “kể cả .cmd”. Không tính lỗi config overwrite lần nữa trong lớp P3 này. |
| 10 | `ban-chup-credential-doc-truoc-canary` — P3 | ĐÃ ĐÓNG lỗi snapshot đem upload | tl_gws.py:680/:689; :729/:787/:1504. Ca thật WP710 snapshot dùng canary đổi jar v1→v2, giải mã bytes đã gửi ở cả ba đường, đạt; mutant lấy snapshot trước canary rc1 đúng ca `wp710_nlm_stage_doc_credential_sau_canary_ca_ba_duong`. Preflight :726/:782/:1496 vẫn gọi hàm đọc FULL bytes, không phải chỉ stat hỏi “có”; snapshot ấy bị bỏ nên không còn lỗi stale-upload cũ. Không suy probe CLI thật có xoay jar từ mock. |

**Hai lớp phát hiện mới.**

| Slug | Hạng | Biểu hiện, phép đo, hướng xử lý |
|---|---|---|
| `stage-error-output-leaks-credential` | P1 | tl_gws.py:169/:190/:191 đưa exception/error thô vào message; :683/:688 in message ở mọi lệnh, callsites :729/:787/:1504. Đo network/unknown error với sentinel giả: rc4, uploads=[], leaked=true ở cả ba lệnh. A/B g2→g3: nlm-auth-stage đã rò từ g2; secrets-set/secrets-stage g2 không probe, không rò sentinel này, g3 bổ sung probe và mở thêm hai đường rò mới. Các lỗi sink vẫn có văn bản không kiểm soát ở :767/:824, :1299/:1301/:1305 và ngoại lệ lan từ :739/:798/:1510; thêm probe upload error: cả ba leaked=true, secrets-set thậm chí rc0/warn. nlm-auth-import.sh:208 chuyển stderr vào log, PS wrapper thì giữ kín. HINT sentinel case rc1, đủ sáu refusal fixture. Dùng mã trạng thái/loại ngoại lệ đóng để xuất console, không đưa str(error)/stdout/stderr credential subprocess ra log; xử lý tương tự ở lỗi upload/encryption. Không dùng truncate như biện pháp giữ bí mật. |
| `trusted-notebook-overwritten-by-stage-config` | P2 | PS:183 truyền TL_NOTEBOOK_ID nhưng tl_gws.py:1487/:1489 load_creds khi lấy token từ config; profile_env.py:171/:174/:357/:365 áp notebookId config, ghi đè ID wrapper. Đo cùng notebook A: env token có ⇒ probe A, rc0; token chỉ trong config profile B ⇒ probe B, rc0, upload vẫn được gọi. HINT pinning case rc1. RUNBOOK:683/:684 hứa hai canary dò cùng notebook nên đường credential config được tài liệu hỗ trợ không giữ được promise mới. Loader có từ trước; đây là lỗ của bản vá truyền ID mới được phát hiện trong g3, không khai loader là dòng mới hay hồi quy chung mọi caller. Giữ ID canary tin cậy xuyên credential loading hoặc dừng khi config xung đột; test lệnh thực với loader thật, không chỉ fake StageCommand đọc env. |

**Doctor và canary parser.** Đã tìm hết caller production. Doctor không truyền require_notebook_body, vì default mới vẫn false; fixture `{}` và sai ID vẫn alive=true ở CẢ g2 và g3. Không tìm được hồi quy mới ở doctor qua các fixture này, cũng không coi việc doctor báo sống là bằng chứng credential sống. Full selftest giữ xanh các ca r45/r56 (True/expired/inconclusive/retry). Chưa chạy doctor với hệ thống thật. Ma trận Python còn đo scalar/null/singleton/data wrapper/type sai/title trắng, JSON có flag âm, duplicate key: mọi output được giữ trong log; chỉ các trả lời nhiều notebook/ID mâu thuẫn được dùng làm finding mơ hồ, không tự bịa hợp đồng mới cho mọi khóa JSON tùy ý.

**Lệnh và mã thoát thật.** R là thư mục chứa PROMPT; S=`R/tmp-review-pF1Ci1`, C=`S/head`, PW=`R/tools/pwsh/pwsh`. Môi trường các lần chạy hợp lệ: `HOME=S/home TMPDIR=S/temp XDG_CACHE_HOME=S/home/.cache PYTHONDONTWRITEBYTECODE=1`; PATH thêm tools/pwsh để child `pwsh` dùng đúng binary. Python 3.11.15, ruff 0.15.8, PowerShell 7.4.6 Linux. Lệnh selftest và gate chạy từ C, có `git config core.abbrev 7` trên chính bản sao. Script/JSON/log chi tiết và mutation driver trong EVIDENCE.zip; không có credential thật.

| Lệnh | rc thật | Output dương/kết quả |
|---|---|---|
| `sha256sum PROMPT.md SPEC.md`; `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --short` | 0 từng lệnh | Các băm đầu verdict khớp; status rỗng |
| `cp -a cay-kho S/head`; `git -C C config core.abbrev 7` | 0, 0 | Bản sao độc lập, HEAD/tree đúng |
| `python scripts/tl.py --selftest` | 0 | `== tl selftest 1718/1718 ==` |
| `ruff check --isolated --no-cache --select F --output-format json` trên g2/g3 `tl_gws.py`, `tl_selftest.py` | 1 ×4 | gws 97/97; selftest 4392/4392; multiset (code,message) thêm=[], bớt=[] cho cả hai ⇒ delta0 |
| `PW -NoProfile -File C/scripts/nlm-credential-refresh.Tests.ps1` | 0 | Tệp nguyên bản, `passed=23 failed=0` |
| `python S/test_wp710_block.py C` qua mutate.py control | 0 | Cả bốn ca WP710 xanh, giữ nguyên assertion |
| `python S/mutate.py` | driver 0; 8 mutant rc1 | None-allow, force bypass, strict flag off, ID/title bỏ, bypass secrets-set/stage, snapshot-before: 8/8 bị ca đích giết, không parse/exception giả |
| `python S/mutate_ps.py PW` | driver 0; 8 control rc0, 8 mutant rc1 | auth regex, title, order, opt-in, stderr, stale evidence, interval, live-record: assertion đúng lý do trong JSON/log |
| `PW -NoProfile -File S/ps-mut-full/scripts/nlm-credential-refresh.Tests.ps1` | 0 | Mutant timeout false khi root đã thoát SỐNG: `passed=23 failed=0` |
| `python S/probe_python.py C` | 0 | 50 rows parser; gate_count; preserved/config bundle bypass; canary error leak; AST inventory |
| `python S/probe_ps.py PW` | 0 | Malformed title/id nhận staged; descendant timeout rc3/record=false; B staged trong khi cháu heartbeat |
| `python S/probe_more.py` | 0 | Token config đổi ID; nguyên shell rc0 dù stage4; upload-error leak; manifest183/negative pointer |
| `cp -a C S/g2`; `git -C S/g2 checkout --detach 52f32db`; `python S/compare_g2.py S/g2`; như vậy cho C | 0 từng lệnh | Doctor fixture không hồi quy; hai đường secrets mới rò thông điệp canary ở g3 |
| `python scripts/tl.py workflow-audit --strict --json` | 0 | ok=true, 26 cards, 60 tasks, 11 groups, 189 commands, errors=[] |
| `python scripts/tl.py golden-test --json` | 0 | ok=true, 20/20 cases |
| `python scripts/tl.py determinism-audit --strict --json` | 0 | ok=true, 15 checks |
| `python scripts/gen_instructions.py --selftest` | 0 | `44/44` |
| `python scripts/tl.py release-manifest --out S/candidate-manifest.json` | 0 | ok=true; ghi ra ngoài checkout, không đổi manifest committed |
| `python scripts/tl.py release-bundle --out S/bundle1.zip --json` và bundle2 | 0, 0 | ok=true ×2; archive_sha256 cùng `98065b4f72fc40715d7430cfbf481f5e107b118d6b088ad37715dcc7b83559d0` |
| `python scripts/tl.py release-verify S/candidate-manifest.json --strict --archive S/bundle1.zip --json` | 0 | ok=true, errors=[] |
| Giải nén bundle vào S/unpacked; `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` từ unpacked/tra-luat | 0 | ok=true, errors=[] |
| `python C/scripts/pkg_secret_scan.py S/scan` — chỉ sáu tệp; rồi thêm mẫu bí mật GIẢ | 0; đối chứng 1 | detected=false; đối chứng detected=true. Không chép mẫu vào verdict |
| `git -C cay-kho diff --check 52f32db HEAD`; diff base cho manifest/VERSION/nlm-auth | 0, 0 | Không whitespace lỗi, không diff các đường được bảo vệ |
| `patch --dry-run -p0 --fuzz=0 -d S/hint-head < goi/HINT.patch` | 0 | Xem output dưới; không hunk fail |
| `patch -p0 --fuzz=0 -d S/hint-head < goi/HINT.patch` | 0 | Chỉ hai tệp TEST được patch, không runtime |
| `python S/test_wp710_block.py S/hint-head` | 1 | 7 ca: ba ca gốc còn xanh, ca body đã mở rộng + bundle + sentinel + pinning đỏ đúng boolean; không exception |
| `python S/run_hint_ps.py PW` | driver 0; n/o mỗi rc1 | n: `ambiguous or non-string notebook body must not stage: title_bool`; o: `new owner staged while the old owner grandchild still performed operations` |

Mutation sống sót, neo/thay đã chạy trên bản sao, không phải hint runtime: trong `Invoke-Bounded`, neo duy nhất `if (-not $done) {` được chèn nhánh `if ($process.HasExited) { $exited=$true; return @{timeout=$false;rc=0;out='';err='';elapsed=$watch.Elapsed.TotalSeconds;exited=$true} }` trước xử lý timeout. Fake linger làm root thoát nhưng cháu giữ pipe; lỗi “cho qua timeout” không làm assertion nào của nguyên bộ 23 ca đỏ. Không tính mutant này là pass chức năng.

Output dry-run cuối:

```text
checking file scripts/tl_selftest.py
checking file scripts/nlm-credential-refresh.Tests.ps1
checking file scripts/tl_selftest.py
checking file scripts/nlm-credential-refresh.Tests.ps1
Hunk #2 succeeded at 401 (offset -20 lines).
checking file scripts/tl_selftest.py
Hunk #1 succeeded at 4774 (offset -54 lines).
checking file scripts/tl_selftest.py
Hunk #1 succeeded at 4829 (offset -91 lines).
```

Offset của dry-run do các nhóm diff TEST cùng tệp được kiểm trên bytes gốc; fuzz=0. Áp thật trên bản sao lần lượt sáu section không có offset/hunk fail, kết quả bytes khớp cây TEST sinh hint. HINT mang nhãn “chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”; chỉ thêm test/fixture ở `scripts/tl_selftest.py`, `scripts/nlm-credential-refresh.Tests.ps1`, nhóm `# lop:` cho lớp 1/2/3/11/12. Lớp 5 được phản chứng bằng mutant và ca o; lớp tài liệu 7/8 có hướng sửa mô tả, không gửi mã runtime.

**KHÔNG ĐO ĐƯỢC / không chạy.** Native Windows: `not_run`, gồm mutex/kernel/ACL/global namespace đa user, abandoned exception, .cmd shim và process tree thật. LIVE refresh/canary/Drive: `not_run`, bị loại bởi phạm vi công việc; mọi upload_count là mock. `nlm auth refresh` CLI thật, version/JSON thật, việc probe xoay jar: `not_measured`. Admission/required CI g3: `not_run`/`not_measured`; review này không gọi remote để biến lời khai g2 thành bằng chứng g3. Hai comment grant g3 không có trong readback: `not_measured`. Model cụ thể/session header: `not_measured`. Không nhận lời khai “đóng cả mười” làm bằng chứng. Linux không chứng minh Windows.

Lần khởi động PW đầu không đặt HOME riêng trả rc134 vì cố tạo cache `/root/.cache/powershell` trên filesystem chỉ đọc; không coi đó là lỗi sản phẩm. Đã sửa môi trường trước suite thật và đo lại version/suite thành công. Harness đầu cho manifest dùng sai API bind, và harness hint thiếu `_TL_MODULE`, mỗi lần Python rc1; đã sửa runner, đo lại, không tính các lỗi harness ấy là finding hay mutation bị giết. Dry-run xây hint đầu rc1 do context phụ thuộc nhóm trước; artifact cuối đã tái dẫn xuất với context độc lập và dry-run/apply đều rc0 như trên.

Tất cả hiện vật mới nằm trong goi/ hoặc thư mục tạm S dưới R; tổng dung lượng dưới 2 GB. Checkout nguồn và copy control cuối sạch. Native/CI thiếu và tám lớp mở giữ verdict `changes_requested`; cần review lại exact SHA sau khi executor sửa.
