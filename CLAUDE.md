# tra-luat — Claude Code Project (dev-side, KHÔNG vào zip deploy)

## Vai trò
Dev/operator cho skill tra-luat. Không tự ý ghi Drive/NLM/registry khi người dùng chưa yêu cầu rõ.
Phiên dev trên máy này ≠ phiên Cowork LIVE (bootstrap từ zip Package — không mang file này).

## Nguồn sự thật
- `scripts/tl.py` là runtime chính; `VERSION` + hằng `VERSION` trong tl.py + header `SKILL.md` phải khớp nhau
  (selftest có guard `skill_md_version_matches_VERSION`).
- `references/API_CONTRACT.md` là hợp đồng webapp (EXPECT_VERSION trong tl.py phải khớp).
- `SKILL.md` là lõi skill — sửa phải nêu lý do + đổi cả vocab/flag nếu thêm cờ mới.
- Kiến trúc ghi/đọc: GHI registry CHỈ qua GAS webapp (LockService + RMW nguyên tử); Drive đọc/push qua gws CLI
  (PRIMARY từ v1.29.0). KHÔNG thêm đường ghi thứ ba (Drive MCP/Sheets MCP).

## Quy trình sửa code
1. `git status` / `git log --oneline -5`
2. Sửa tối thiểu, giữ idiom comment "vX.Y.Z (bằng chứng) — fix"
3. `python -m ruff check --select F scripts/tl.py` — tiêu chí là **DELTA so master = 0**, KHÔNG phải "0 tuyệt đối".
   Nền ĐO 29-07-2026 (v1.35.60): tl.py **12 F821 + 0 F401**; tl_selftest **3914 F821 + 1 F401**.
   12 F821 (10 tên: `build_parser` `load_creds` `norm_sohieu` `_active_profile` `_cache_file` `_dang_bare_key`
   `_entry_drive_id` `_reassemble_parts` `_sha256_file` `_sohieu_key_entry`) là BY DESIGN: stub-farm gán qua
   `globals()[tên]` từ bảng `_STUB_MAP` nên ruff không thấy tĩnh — đã kiểm HÀNH VI: cả 10 resolve sau import,
   không tên nào bị gọi trước lúc bảng stub chạy (đường cứu hộ `_selfheal_module` không có caller mức module).
   Mốc trôi: v1.34.14 = 0 F821 → v1.34.15 (`bfd18ea`, I10 nén 488 stub → `_STUB_MAP` + factory) = 217 → I11 = 11 → r201 = 12.
   **F401 = 0 nhờ `# noqa` CÓ CHỦ ĐÍCH, KHÔNG phải vì xoá import** (r224): `base64` `datetime` `hashlib`
   `unicodedata` `zipfile` ở đầu tl.py là MẶT NAMESPACE dùng chung — 1646 hàm tl_core được re-home
   `__globals__` về tl.py nên tra tên toàn cục ở ĐÂY, kể cả khi tệp gốc đã tự import (profile_mgmt.py có
   `import datetime` riêng mà vẫn NameError khi tl.py thiếu). Số hàm re-home tra từng tên: unicodedata 19 ·
   base64 9 · hashlib 3 · datetime 2 · zipfile 0. **ĐỪNG "dọn import thừa" ở dòng đó** — gate đã ĐỎ 2 lượt vì việc này.
   Ruff KHÔNG nằm trong gate ⇒ ngưỡng này do người giữ; thấy số lạ thì đo lại master TRƯỚC khi nghi bản vá của mình.
4. `python scripts/tl.py --selftest` (phải N/N, thêm test rXX_ cho mỗi fix)
5. Output DÀI (selftest N case, audit/golden JSON, gate logs) → giao agent `tl-auditor` (read-only) tiêu hoá,
   phiên chính chỉ nhận kết luận — giữ context sạch (G5 §11 kế hoạch guard-va-boc-tl-core).
6. `git diff` → CHANGELOG.md (mục ★ vX.Y.Z) → commit
7. Deploy — xem "## Quy ước deploy" bên dưới. KHÔNG tự chạy khi user chưa duyệt.
   Windows: `.\scripts\deploy-package.ps1 -Pull -Push` · Linux/Cowork: `./scripts/deploy-package.sh --push`.
   (Cả hai TRONG repo, cùng quy trình, cùng chốt. `upload-skill-to-Package.ps1/.cmd` đã bỏ từ v1.35.83.)

## Bài học đắt giá (đã trả giá, không lặp lại)
- **Đối chiếu nhánh/patch ngoài: BẮT BUỘC test HÀNH VI 2 CHIỀU** (fixture họ chạy trên ta + phản chứng bơm vào
  bản họ), KHÔNG grep chuỗi. Mỗi PORT/REJECT phải có bằng chứng chạy được, khoá bằng test rXX_.
- **Ghi giá trị RỖNG qua reg_bulk/upsert bị webapp BỎ QUA** — xoá field phải đi `reg_clear` (`_journaled_reg_clear`).
- Mọi số hiệu/tên VBQPPL phải có NĂM (VBHN thiếu năm = collision — số tái dùng theo năm).
- Subagent KHÔNG được sửa `tl.py` canonical (bài học rogue-edit) — agent chỉ read-only; vá code do phiên chính làm.
- registry claim NLM là ESTIMATE — slot/FULL/overflow phải neo `nlm-get`/`nlm-reconcile` LIVE.
- **Cổng xanh nhờ `rc=0` là cổng CÓ THỂ BỊ LỪA — phải đòi BẰNG CHỨNG DƯƠNG** (`N/N` với hai số BẰNG NHAU,
  `"ok": true`), đừng tin rc. Bằng chứng đã trả giá (r244): `param([string[]]$Args)` trong PowerShell —
  `$Args` là **BIẾN TỰ ĐỘNG** trong hàm nên `@Args` nở ra mảng RỖNG thay vì đối số truyền vào ⇒ python
  chạy KHÔNG đối số, đọc stdin, EOF, **rc=0 + output rỗng**: gate báo xanh mà chẳng chạy gì.
- **Script đa nền: PHẢI chạy THẬT trên nền đó, rồi ĐỐI CHIẾU PARITY hai bản trên cùng đầu vào.**
  (r244: đã tải hẳn PowerShell 7.4.6 vào container để chạy.) 5 lỗi của lượt đó KHÔNG lỗi nào lộ ra bằng
  đọc code; riêng **lỗ AN NINH** chỉ hiện vì hai bản đếm LỆCH (ps1 196 vs sh 198 trên cùng một zip) —
  parity không phải nghi lễ, nó là thứ duy nhất bắt được.
- **PowerShell — 3 bẫy đã trả giá** (r244; chú thích chi tiết nằm ngay tại code):
  · `$Args` là biến tự động (xem trên) → đặt tên khác, vd `$Argv`.
  · `Get-Content -Raw` trên tệp **RỖNG** trả `$null` → `[regex]::Match` ném "Value cannot be null"; ép `[string]`.
  · `Get-Item`/`Get-ChildItem` **BỎ tệp ẩn khi thiếu `-Force`** (trên Unix: mọi tên bắt đầu bằng `.`) —
  `Test-Path` thấy có mà `Get-Item` báo not-found là dấu hiệu kinh điển.
- **Câu mô tả VỊ TRÍ của một artefact phải đúng ở CẢ HAI phía của lần merge.** Prompt reviewer neo
  theo băm, mà trong prompt lại có câu "tệp nằm ở đâu". Bản đầu ghi "trên master" khi tệp còn ở nhánh
  ops ⇒ ai clone master là dừng ngay; sửa thành "chỉ ở nhánh ops, chưa vào master" ⇒ câu ấy **chết
  đúng lúc merge**. Mỗi lần sửa câu ấy lại đổi băm ⇒ kéo theo cập nhật lease + chiếu lại; ba bản chiếu
  chết chỉ vì một câu chữ. Cách thoát: viết câu đúng ở CẢ HAI trạng thái ("tìm ở `master` trước, chưa
  thấy thì fetch nhánh X"), và nói thẳng trong prompt rằng **thứ định danh tệp là BĂM, không phải tên
  nhánh** — tên nhánh là thứ trôi và bị xoá.
- **"Ca có MẶT" khác "ca có ĐO".** Một ca `return` sớm vì đường dẫn sai vẫn được đếm là ĐẠT: `t24` trỏ
  `HERE.parent.parent` nên tìm thư mục workflow ở TRÊN gốc kho, không thấy thì thoát êm — suite báo
  **24/24** trong khi ca ấy không đo gì, và nó lại là ca sinh ra để chặn đúng bệnh đó. Chỉ lộ vì đã
  đột biến thử sau khi viết. Mọi ca có nhánh "không thấy thì bỏ qua" phải kèm chốt: chỉ được tha khi
  cây rõ ràng là bản sao rời (không `.git`); trong kho thật mà thiếu thì ĐỎ.
- **NGHĨ RA được phép thử mà KHÔNG CHẠY nó thì phép thử ấy KHÔNG TỒN TẠI.** Prompt reviewer do chính
  phiên viết cổng soạn ra **liệt kê `codex-dispatcher` làm hướng tấn công số 1** — rồi cổng
  `ops/lease_publish.py` của phiên đó thua đúng ca ấy (`rc=0`, tự cấp được lease), và phải chờ
  reviewer ngoài chạy mới lộ. Viết một hướng tấn công vào tài liệu cho cảm giác đã lo tới nó, nhưng
  tài liệu không chạy: chỉ có ca test chạy. Nghĩ ra được ca nào thì **biến ngay ca đó thành `rXX_`**,
  đừng để nó nằm trong prompt/README/mô tả PR — chỗ đó là nơi các ca đi chết.
- **Danh sách CẤM không bao giờ đủ — phải đảo thành danh sách CHO PHÉP.** Cùng sự cố trên: cổng từ
  chối đúng hai chuỗi `claude`/`codex`, nên `codex-dispatcher`, `ai-codex-bot`, `cödex` đều lọt.
  Nguyên văn reviewer: *"distinguishes spelling, not authority"* — phân biệt CÁCH VIẾT, không phân
  biệt THẨM QUYỀN. Danh sách cấm phải đoán trước mọi cách viết của kẻ gian (dấu nối, tiền tố, hậu tố,
  đồng tự Unicode, tổ hợp dấu) nên **thua từ trong thiết kế**; danh sách cho phép chỉ phải liệt kê một
  tập nhỏ và biết trước. Đo được ở `v1.36.68` (PR #104): ba tên tấn công `rc=0` → `rc=4`, người có
  thẩm quyền vẫn `rc=0`. Kèm chốt: đột biến **nới danh sách cho phép để chứa tên tấn công** phải làm
  ca đích ĐỎ — không có đột biến ấy thì không biết ca đang đo danh sách hay đo thứ khác.
- **`[skip ci]` trong THÔNG ĐIỆP COMMIT là chốt đặt sai chỗ — nó sống trong LỊCH SỬ.**
  Bước ghi ngược của `ops-publish-lease.yml` từng commit kèm `[skip ci]` để khỏi tự kích hoạt lại.
  Dấu ấy ở lại trong commit, nên khi commit ghi ngược thành **HEAD của một PR** thì nó tắt luôn gate
  của PR đó: PR #100 có **0 check run** mà vẫn hiện `mergeable_state: clean`. Cổng không nói dối —
  nó **vắng mặt**, và trên giao diện "xanh" với "không chạy" nhìn giống hệt nhau. Chốt chống lặp phải
  nằm ở **lượt chạy** (`if:` mức job), đừng nằm trong commit. Khoá bằng `t24` trong
  `ops/lease_publish_test.py`. Nhắc: push bằng `GITHUB_TOKEN` vốn KHÔNG sinh lượt chạy mới, và chốt
  idempotent `rc=9` chặn đăng trùng — nên bỏ `[skip ci]` không hề mở ra vòng lặp vô hạn.
- **ĐỪNG viết `[skip ci]` nguyên văn trong commit message, KỂ CẢ khi đang trích dẫn để giải thích.**
  Đã sập thật: merge commit của PR #100 nhắc `[skip ci]` trong phần *giải thích lỗi trên* và tắt
  luôn gate của master (`464124d` không có lượt chạy nào). GitHub khớp **CHUỖI trên toàn thông điệp**,
  không đọc Markdown — dấu nháy ngược không phải hàng rào, y hệt bài học `doctrine-scan`. Muốn nhắc
  tới nó thì viết tách chữ (`skip` + `ci`) hoặc mô tả bằng lời. Máy KHÔNG canh được chỗ này (`t24`
  chỉ quét workflow, không quét commit sắp tạo) — đây thuần là kỷ luật viết.
- **TẦNG VẬN CHUYỂN CŨNG CHUẨN HOÁ CHUỖI — "chép nguyên văn" chỉ chứng minh được bằng ĐO THỨ ĐÃ ĐẾN,
  không phải thứ đã GỬI.** Đăng hộ verdict cross-review lượt 4 lên PR #92: bản gốc trong kho có băm
  (`d58088be…`), đã kiểm khớp TRƯỚC khi đăng, và người đăng chép từng chữ. Vẫn lệch. Reviewer cố ý
  liệt kê HAI cách viết khác nhau của cùng một tên để dò biên — bản dựng sẵn `cödex` (U+00F6) và bản
  viết bằng **chuỗi thoát ASCII nguyên văn** `co\u0308dex`. Thân comment đi qua MCP nằm trong một
  chuỗi JSON, mà `\u0308` **là escape hợp lệ của JSON**, nên nó bị giải mã thành dấu ghép THẬT ngay ở
  tầng vận chuyển: hai tên khác nhau về byte biến thành hai tên hiển thị y hệt, và một hướng dò biên
  biến mất không để lại dấu. Chỉ lộ vì đã chạy `diff -u` giữa nguồn và bản ĐÃ ĐĂNG (đọc lại qua API)
  — đúng một hunk lệch, mọi dòng khác khớp từng byte.
  Cùng họ với `doctrine-scan` và với dấu bỏ-qua-CI: **một lớp mà ta không coi là lớp**. Chốt: (a) băm
  phải đo trên thứ ĐÃ ĐẾN, nên đăng xong là đọc ngược về và diff, đừng dừng ở "lời gọi trả thành
  công"; (b) phải biết mình đang đứng ở LỚP NÀO — xem ngay dưới; (c) nguồn có thẩm quyền là
  TỆP CÓ BĂM trong kho, comment chỉ là bản chiếu — nói thẳng điều đó ngay trong bản chiếu.
  **Chốt (b) nói cho đúng, vì bản đầu viết sai và cross-review bắt được** (P2 trên PR #106):
  "có dấu chéo ngược thì nhân đôi" là luật QUÁ RỘNG và tự nó tái tạo đúng cái lệch đang bàn.
  Nhân đôi CHỈ đúng khi ta tự tay dựng CHÍNH CHUỖI JSON (đối số của một lời gọi công cụ là như
  vậy). Khi tải trọng được trao cho bộ tuần tự hoá dưới dạng chuỗi ứng dụng (`json.dumps`,
  client MCP/HTTP thường), bộ ấy ĐÃ thoát hộ — nhân đôi thêm một lần nữa thì bên nhận lĩnh
  thừa một dấu chéo. Hai lớp, hai luật ngược nhau, và đoán sai lớp thì hỏng theo cả hai chiều.
  Nên thứ đáng nhớ KHÔNG phải mẹo nhân đôi mà là chốt (a): đo thứ ĐÃ ĐẾN.
  Bằng chứng bẫy này KHÔNG hiếm và KHÔNG chỉ ở MCP: chính hai dòng trên đây, lượt viết đầu cũng bị
  công cụ sửa tệp giải mã mất chuỗi thoát (đối số của nó cũng là chuỗi JSON), phải ghi lại bằng một
  script tự dựng dấu chéo từ `chr(92)` rồi ĐO `repr()` mới thấy. Nói cho ĐÚNG kẻo lại giữ nguyên cái
  mô hình lớp sai vừa sửa ở trên — bản đầu viết "đi vòng qua lớp JSON", và cross-review bắt được
  (P2 trên PR #108): script ấy CŨNG là đối số công cụ nên CŨNG đi qua đúng lớp tuần tự hoá đó, không
  vòng được đi đâu cả. Thứ nó tránh là **cho một dấu chéo NGUYÊN VĂN đi trên đường truyền**: dấu chéo
  được DỰNG SAU khi đã phân tích cú pháp, nên không còn gì để lớp nào giải mã. Đó là HOÃN việc dựng
  chuỗi, không phải né một tầng. Hễ nội dung NÓI VỀ chuỗi thoát thì phải đo nó sau khi ghi.
- **Quét secrets: lọc theo PHẦN MỞ RỘNG là mù ĐÚNG CHỖ secrets nằm.** `Path('.env').suffix == ''` nên
  `.env` `.netrc` `credentials` (không mở rộng) bị bỏ qua SẠCH — bơm `GOCSPX-…` vào `.env` mà bộ quét
  trả rc=0. Cộng thêm `Get-ChildItem` thiếu `-Force` cũng bỏ y hệt: **hai lỗi ĐỘC LẬP mà CÙNG HƯỚNG** ⇒
  đường Windows từng mù hoàn toàn với secrets trong tệp ẩn. Nay quét cả tệp không mở rộng, tránh nhị
  phân bằng NUL-check 8KB + trần 2MB. Bảng mẫu bí mật ĐỂ MỘT CHỖ: `scripts/pkg_secret_scan.py`, dùng
  chung cho cả `sh` lẫn `ps1` — hai bản sẽ trôi lệch, và bên quên cập nhật chính là bên đẩy lọt.

## Gọi agent đa nền (chi tiết: `docs/GOI_AGENT_DA_NEN.md`)
- **KHÔNG viết script spawn agent.** Dùng CLI CHÍNH THỨC: `claude`
  (`@anthropic-ai/claude-code`) và `codex` (`@openai/codex`). `.claude/dev/launcher.py`
  CHỈ dựng chốt quanh một lệnh bất kỳ rồi chạy lệnh đó — không biết agent nào, không
  prompt dựng sẵn. Wrapper tự chế sẽ phải bám theo cờ/biến/xác thực của hai CLI khác
  nhau rồi trôi lệch âm thầm.
- `python .claude/dev/launcher.py doctor` trước khi nghi ngờ bất cứ thứ gì khác.
  Thoát 12 = thiếu công cụ bắt buộc. Container Claude Code web ĐÃ ĐO 12-08-2026:
  có python/git/node/claude/rg, **KHÔNG** có codex/gh/pwsh — `.claude/hooks/session-start.sh`
  cài codex/claude/ripgrep (KHÔNG cài gh, pwsh: kho dùng GitHub qua MCP, không còn
  đường nào cần PowerShell).
- **Không được giả định Windows có `python3`** (bản phổ biến chỉ có `python`, `py`).
  Đừng bắt cài thêm bí danh; tài liệu và script phải nhận cả ba tên.
- **Neo theo KHO, không theo đường dẫn.** Đường dẫn tuyệt đối là thứ duy nhất không
  mang được sang máy khác — phiên remote clone vào đường dẫn không ai biết trước.
  Dùng `--expected-repo` + `--expected-root-commit` (vân tay bền nhất: sống qua đổi
  tên/chuyển chủ/fork, đọc được không cần mạng).

## Bài học lớp "chạy được ở đây" (12-08-2026, codex đo trên Windows thật)
- **`print` giết cả lượt chạy trước khi logic kịp sai.** Console máy Việt là cp1258 nên
  in đường dẫn có dấu ném `UnicodeEncodeError`, rc=1. Bẫy ở ĐẦU RA chứ không ở đối số:
  git nhận đúng, trả đúng, rồi câu print giết. Mọi CLI phải ép stdout/stderr sang UTF-8
  TRƯỚC khi in gì.
- **`taskkill /T /F` KHÔNG đáng tin.** Trả `rc=1 Access denied` ngay trên tiến trình do
  chính mình sinh, trong khi `Stop-Process -Force` giết được. Đã giết thì phải KIỂM LẠI;
  "đã gọi lệnh giết" ≠ "đã chết". Tách mã 124 (quá hạn + đã giết) khỏi 125 (quá hạn +
  KHÔNG giết được) — trả 124 khi tiến trình còn sống là chốt nói dối.
- **ZOMBIE tính là đã chết.** Con vừa bị giết nằm ở trạng thái Z tới khi được `wait` thu
  hồi, mà `os.kill(pid,0)` với zombie vẫn thành công ⇒ báo "chưa giết được" cho tiến
  trình đã chết hẳn.
- **`endswith` để so danh tính = lỗ giả mạo.** `--expected-repo github.com/o/r` từng KHỚP
  remote `https://evil.example/github.com/o/r.git`. Nêu host (≥3 đoạn) ⇒ đòi bằng nhau
  tuyệt đối — KHÔNG bó ở đúng 3 đoạn, vì GitLab subgroup/GHE lồng nhau có 4+ đoạn và bó
  như thế là chặn oan chính danh tính đúng (audit vòng 3).
- **Đột biến ghi vào tệp THẬT rồi khôi phục trong `finally` là bom hẹn giờ.** Lượt chạy bị
  SIGTERM cắt giữa chừng ⇒ `finally` không chạy ⇒ tệp ở lại trạng thái đã méo, và lượt sau
  đọc bản méo làm "bản gốc". Một bản vá NGƯỢC (`if False:` thay cho chốt chống giết nhầm
  PID) đã đi thẳng vào commit theo đường này. Đột biến phải chạy trên BẢN SAO TẠM.
- **Test không được nhét PID của chính nó vào thứ mình đang thử giết.** Ở lượt đột biến
  "giết liều" — đúng lượt cần đo — bộ test tự sát (exit 143). Đó chính là nguyên nhân gốc
  của gạch đầu dòng trên.
- **Đột biến SỐNG SÓT không luôn nghĩa là test yếu.** Đo rồi mới biết: `-uall` so với mặc
  định KHÔNG đổi sạch/bẩn (chỉ `-uno` mới làm chốt mù), và ca "rc=0 mà rỗng" được chặn ở
  BỐN lớp độc lập nên phải đột biến ghép cả bốn. Đột biến sai chỗ ≠ mã sai.
- **Hook dùng đường dẫn TƯƠNG ĐỐI là bẫy tự khoá.** `.claude/settings.json` từng ghi
  `python .claude/hooks/pretooluse_guard.py`; khi cwd của shell trôi vào thư mục con thì
  MỌI lệnh Bash chết trước khi chạy, và không còn đường `cd` về. Luôn dùng
  `$CLAUDE_PROJECT_DIR`.

## Cấm
- Không tự chạy lệnh có `--apply` / `source-delete` / `reg-delete` / `--clear-stale` khi user chưa duyệt (hook sẽ hỏi).
- Không đọc/ghi secrets (`*.enc`, `tl_secrets*`, `*cookie*`, `*token*`, `credentials*`) ngoài đúng quy trình
  `gws-auth-stage`/`secrets-set` mà user yêu cầu.
- Không dùng Drive MCP/Sheets MCP để sửa corpus/registry.
- Không dùng RAG/NLM để trả NGUYÊN VĂN điều luật — nguyên văn chỉ từ nguồn đã verify (extract/web official).

## Khi đóng gói
Bump VERSION (3 chỗ) → CHANGELOG → selftest N/N → user tự chạy cmd (script tự loại .git/.claude/.githooks/
CLAUDE.md/config/enc + quét token). Verify sau deploy: Package trả VERSION mới.

**TRẦN 200 TỆP — cứng, `release-bundle` chết `IMPORT_LIMIT_EXCEEDED` chứ không cắt bớt âm thầm.**
Đã đụng thật ở r244 (thêm 3 script deploy: 199 → 202). Thêm tệp mới mà gần trần thì cách chữa KHÔNG phải
xoá tệp: xét xem nó có phải **dev-side** (runtime Cowork không cần) rồi cho vào
`_RELEASE_EXCLUDE_NAMES_ANYWHERE` — GIỮ trong repo/git, CHỈ loại khỏi GÓI. Tiền lệ: `CLAUDE.md` ·
`.claude/` · `Code.2.21.2k.gs` · 4 script deploy. Nhớ: thêm/xoá tệp ⇒ tái sinh `RELEASE_MANIFEST.json`
và ghi lại golden nếu số đếm kiểm kê đổi (mục 5 §Quy ước deploy).

## Quy ước deploy (AI ĐẨY Package — chốt 30-07-2026)
**Vì sao cần:** Package là MỘT fileId duy nhất (`SKILL_FILEID = 1H5kAt3SRVP7…`) và `drive-push` GHI ĐÈ nội
dung, giữ fileId. KHÔNG có LockService như registry ⇒ **last-writer-wins, im lặng, không cảnh báo**. Sự cố
30-07-2026: hai phiên song song đẩy cùng fileId trong ~20 phút (v1.35.77 rồi v1.35.78); lần đó vô hại vì phiên
sau build từ master mới nhất và đã bao gồm việc của phiên trước — nhưng nếu ngược chiều thì Package THỤT LÙI
âm thầm, và mọi phiên Cowork mới bootstrap bản cũ.

1. **Ai đẩy:** phiên nào bump VERSION cho đợt đó thì phiên ĐÓ đẩy, sau khi user duyệt. Phiên khác KHÔNG đẩy
   trong lúc đợt đang mở. Hai đường (`deploy-package.ps1 -Push` · `deploy-package.sh --push`) vào CÙNG
   fileId ⇒ quy ước áp dụng như nhau, không có ngoại lệ "tôi chỉ đẩy nhanh một bản".
2. **TRƯỚC khi build:** `git fetch origin master` + xác nhận HEAD KHÔNG tụt sau `origin/master`. Tụt sau ⇒
   merge/rebase + chạy lại gate TRƯỚC, không build. (Build từ cây tụt sau = đóng gói bản thụt lùi.)
3. **TRƯỚC khi push:** đọc tên file Package ĐANG có trên Drive
   (`gws drive files get --params '{"fileId":"1H5kAt3SRVP7…","fields":"name,size,md5Checksum"}'`).
   Nếu version trên Drive **≥** version sắp đẩy ⇒ **DỪNG, hỏi user** — nghĩa là phiên khác vừa đẩy.
   Đây là chốt chống thụt lùi duy nhất; không có nó thì mục 1-2 chỉ là lời hứa.
   **ĐÃ CƯỠNG CHẾ CẢ HAI ĐƯỜNG** (rc=3, chặn TRƯỚC `drive-push`; bằng-số cũng chặn):
   - Linux/Cowork: `deploy-package.sh` bước 4, từ v1.35.79. Ghi đè cố ý: `--force-older`.
   - Windows: `deploy-package.ps1` bước 4 (gọi `scripts/deploy-guard.ps1`), từ v1.35.80. Ghi đè cố ý:
     `-ForceOlder`. Chạy chốt riêng để xem Drive đang ở bản nào:
     `.\scripts\deploy-guard.ps1 -Version (Get-Content VERSION).Trim()`.
   Từ v1.35.83 KHÔNG còn đường deploy nào thiếu chốt: `upload-skill-to-Package.ps1` (ngoài repo, không
   có chốt, trôi lệch theo máy) đã BỎ — cả hai nền dùng script TRONG repo.
4. **SAU khi push:** không tin thông báo "đã đẩy". Tải lại từ Drive và đối chiếu **md5/sha256 + VERSION**
   (`deploy-package.sh` bước 5 làm sẵn). Chưa byte-match thì coi như CHƯA deploy.
5. **Thêm/xoá tệp trong cây ⇒ tái sinh `RELEASE_MANIFEST.json`, và ghi lại golden NẾU số đếm kiểm kê đổi.**
   Bỏ bước này thì phiên deploy KẾ TIẾP ăn gate đỏ không phải do nó (bài học r238: `nlm_auth_convert.py`
   làm `files_scanned` 67→68, golden không ghi lại ⇒ `golden` + `determinism` đỏ trên master cho phiên sau).
   Nhắc: `golden-test --write` vẫn CẤM cho diff của một move (R6); chỉ ghi lại khi đã KIỂM diễn biến thực tế
   và xác nhận diff đúng là kiểm kê hợp lệ — kiểm bằng `git diff -- references/golden/` TRƯỚC khi commit.
6. **`core.abbrev` phải = 7 khi chạy gate** (CI ghim `--global`; `deploy-package.sh` ghim repo-local).
   Không ghim ⇒ golden/determinism/doc-claims-check đỏ giả theo kích thước repo — xem ★ v1.35.78 (r241).
7. **Đo nền trước khi nghi bản vá của mình:** gate đỏ ⇒ chạy lại trên `origin/master` sạch, so DELTA. Đỏ sẵn
   thì nói rõ "đỏ sẵn, delta = 0" chứ đừng vá lung tung (cùng doctrine với ngưỡng ruff ở §Quy trình sửa code).

<important if="phát triển Claude Code artifacts">
## Kho tham chiếu Claude Code
Khi cần best practice về Claude Code (agents, commands, skills, hooks,
memory, subagents...), ĐỌC trong ./claude-code-best-practice/best-practice/
TRƯỚC khi dùng kiến thức huấn luyện. Repo này là nguồn ưu tiên.
Cập nhật kho: cd claude-code-best-practice && git pull
(Clone dev-only local — .gitignore + loại bundle qua _RELEASE_EXCLUDE_DIRS; KHÔNG có trong gói deploy.)
</important>
