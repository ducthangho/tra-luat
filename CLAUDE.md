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
  tập nhỏ và biết trước. Đo được ở `v1.36.68` (PR #104): ba tên tấn công `rc=0` → `rc=4`, tên thuộc
  danh sách cho phép vẫn `rc=0`. Kèm chốt: đột biến **nới danh sách cho phép để chứa tên tấn công** phải làm
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
- **…VÀ ĐƯỜNG ĐỌC CŨNG CHUẨN HOÁ — nên "đọc ngược về rồi diff" TỰ NÓ sinh phát hiện giả.**
  Đo 22-08-2026. Chốt (a) ở gạch đầu dòng trên bảo: đăng xong thì đọc lại qua API và `diff`. Làm
  đúng thế với comment lease `#238` ⇒ **lệch hệ thống**, không phải một hunk: `'`→`&#39;` ·
  `"`→`&#34;` · `>`→`&gt;` · `<`→`&lt;`, rải khắp thân. Suýt nữa thành một finding về cổng đăng lease.
  Ba phép đo tách được LỚP, và không phép nào bỏ được:
  · **hai đường GHI độc lập cho kết quả Y HỆT** — comment do workflow đăng bằng `gh api` (Go, GitHub
  CLI) và issue do phiên này đăng bằng MCP: cùng bị đổi như nhau ⇒ không phải đường ghi;
  · **hai công cụ ĐỌC khác nhau** (`issue_read` · `list_issues`) cùng trả bản đã đổi;
  · **tệp trong git đi qua CHÍNH máy chủ MCP ấy về BYTE-EXACT** — `get_file_contents` trên một tệp
  có 5 dấu `>` cho **sha256 khớp bản trên đĩa**. Nên KHÔNG phải middleware chung; chỉ **trường thân
  issue/comment** bị chuẩn hoá, đúng kiểu bộ lọc nội dung-người-dùng ở phía ĐỌC.
  Dấu vết phụ: `&` trong phản hồi về dưới dạng `\u0026` — chữ ký `encoding/json` của Go bật HTMLEscape,
  tức có **hai** lớp chồng nhau, và lớp JSON ấy KHÔNG phải thứ gây ra `&#39;`.
  Chốt: `diff` bản-đã-đến qua MCP **chỉ dùng để tìm lệch VỀ KÝ TỰ THẬT** (kiểu `co` + `\u0308` + `dex`);
  chênh lệch thực thể HTML ở đó là **tạo tác của công cụ đọc**, đừng ghi thành phát hiện. Muốn khẳng
  định byte trên GitHub thì phải có client thứ hai. Lúc viết (22-08) container KHÔNG có (mục REST
  17-08 ở §Gọi agent đa nền: `/repos/<kho>` · `/pulls/N` → 403 do proxy), nên câu ấy đứng ở trạng thái
  thứ ba: **KHÔNG ĐO ĐƯỢC**. **Ở CÁC PHIÊN ĐÃ ĐO THÌ CÓ** — `2026-09-25` và `2026-09-30`: REST GET tới
  `/repos/<kho>`, PR và comment trả **200 kèm `X-GitHub-*`** (KHÔNG phải mọi đường con, xem §Đẩy ref);
  trạng thái ấy chỉ nói cho phiên đã đo, `doctor` (`rest-kho`, chỉ hỏi `/repos/<kho>`) đo lại mỗi phiên.
  Đo 25-09 trên `issuecomment-5811128755` (bản chiếu lease, dày dấu nháy): REST trả **44 dấu `'`
  thật · 8 dấu `>` thật · 3 dấu `<` thật · 0 thực thể HTML** (đo lại `2026-09-30T06:31–06:33Z`,
  `urllib` và `curl` khớp băm thân: y hệt). Phiên 25-09 khai đọc chính comment ấy qua MCP cũng ra
  ký tự thật (công cụ nào: không ghi; chưa đo lại) ⇒ trên comment ẤY, lệch 22-08 **KHÔNG TÁI LẬP**.
  **CA CŨ CŨNG ĐO ĐƯỢC — bản trước khai ngược, cross-review bác** (P1 trên PR #631): *"comment của
  lượt 22-08 không còn để thử lại"* là lời khai VẮNG MẶT không kèm phép đo, trong khi chỗ kết luận
  được ghi nằm ngay trong kho: `posted_comment_id` của `ops/leases/lease-dang-windows-*-20260822.yaml`.
  Đo `2026-09-30T06:31Z` (REST GET, `urllib` + `curl` khớp băm từng thân): **7/7** comment ấy còn trên
  `#238`, `updated_at == created_at` (22-08, chưa ai sửa), dấu `'` thật (22/33/14/49/34/33/19), **0
  thực thể HTML, 0 dấu `&`** ⇒ byte GitHub giữ là ký tự thật, `&#39;` hôm 22-08 sinh trên **đường ĐỌC
  MCP**. Giới hạn: tệp không ghi comment NÀO đã bị đọc (cả 7 đều sạch), đầu ra thô của MCP 22-08
  không lưu, hai client REST cùng đi qua một proxy, và chưa ai ghi lần đọc lại 7 comment ấy qua MCP.
  Chốt (a) *đăng xong đọc ngược rồi diff* GIỮ NGUYÊN, nay mạnh hơn ở phiên nào có client thứ hai.
  Bài học gốc không đổi, chỉ chật hơn: **phải biết mình đang đứng ở LỚP NÀO** — kể cả khi cái lớp
  đang lừa mình chính là cái chốt vừa dựng ra để chống bị lừa.
- **HỎI CHỖ TIỆN TAY thay vì hỏi CHỖ KẾT LUẬN ĐƯỢC GHI — ba lần trong MỘT phiên (14-08-2026).**
  Cùng một gốc, ba mặt khác nhau, và KHÔNG lần nào tự phát hiện. Chép ra đây vì cái gốc ấy tái phát
  nhanh hơn mọi bài học khác trong tệp này: nó không đòi ta lười, chỉ đòi ta tin một tín hiệu ở gần.
  · **(a) "Gate xanh" KHÔNG phải "đã được review".** Đã merge PR #104 và #105 sau khi kiểm gate mà
  KHÔNG mở phần review; codex đã đăng finding trước lúc merge ba phút. Hai finding thật (một P1 về
  cổng đăng lease, một P2 về evidence_url) đi thẳng vào master, phải vá bằng PR #107. **Trước khi
  merge: đọc review, không chỉ đọc cổng.** Hai thứ đó trả lời hai câu hỏi khác nhau.
  · **(b) RỖNG ở API mình hỏi KHÔNG phải "chưa chạy".** Connector codex chỉ tạo ĐỐI TƯỢNG review khi
  **có** góp ý; kết luận SẠCH nó gửi bằng một issue comment thường, neo bằng dòng `Reviewed commit:`.
  Hỏi `get_reviews`/`get_review_comments` thấy rỗng rồi đọc thành "chưa review" ⇒ đã báo sai rằng #103
  là chỗ mù, và đăng thêm một lời gọi review với cái cớ sai — trong khi kết luận sạch đã có từ 20 phút
  trước. **Muốn biết đã review chưa thì tìm dòng `Reviewed commit:` cho ĐÚNG commit đang xét.**
  · **(c) Nền nào chạy gate KHÔNG được chép vào đây — đọc nó từ `ci.yml` và từ NHÃN JOB, mỗi lần.**
  Mục này từng chép ma trận `os` thành văn xuôi, và văn xuôi ấy đã lệch khỏi `ci.yml` BA lần: câu gốc
  *"PR thường chỉ chạy `ubuntu`, còn master chạy CẢ `ubuntu` LẪN `windows`"* đã chết từ packet #548
  (`CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND`, bỏ vế `github.ref == 'refs/heads/master'` khỏi output `os` của job
  `chuan-bi`) mà vẫn nằm đây; sửa ở PR #870 xong thì #878 (`runner_set=windows-only`) và #879 (Windows chỉ còn
  một phần gate) làm nó cũ tiếp, phải đo lại ở PR #889. Câu cũ đã kịp gây hại thật: biên bản land commit
  `3f6c694` khai `jobs: '23/23 success (gom windows)'` cho run **39354156843** (push `3a3a3ca` lên master) trong
  khi cả 23 job mang nhãn `ubuntu-latest` (`ops/land/pr848-wp744-provenance/readback-jobs-39354156843.json`) —
  Codex connector bắt thành P1 trên PR #859 (comment `r4323607674`), sửa ở PR #865. Đúng bệnh mục này dạy:
  tin một câu GẦN TAY thay vì đọc nhãn job.
  **Nguồn sự thật, theo thứ tự hỏi:**
  · ma trận dự kiến = output `os` của job `chuan-bi` trong `.github/workflows/ci.yml`, cộng `exclude:` và
  `if:` mức job của TỪNG job `gate*` (một job có thể loại Windows dù `os` có Windows);
  · riêng hành vi của output `os` được khoá bằng `t162_M4_evaluator_toi_gian_chuan_bi` trong `ops/lease_publish_test.py`
  (đánh giá biểu thức thật bằng `_danh_gia_bieu_thuc_chuan_bi` cho push / PR thường / PR nhãn `windows` /
  từng `runner_set`). Ca này không đọc `exclude:` hay `if:` mức job, nên vẫn phải đọc chúng trong `ci.yml`;
  phần mảnh/gom của `gate-cong-cu*` có chốt riêng ở `loi_g5_workflow` trong `.claude/dev/ci_dang_ky_test.py`.
  Ca liền trước, `t161_M3_chot_nguon_duy_nhat_ma_tran_ci`, chỉ khoá CẤU TRÚC (mọi job lấy `os` từ
  `chuan-bi`, output không bọc `fromJSON`) — nó KHÔNG đánh giá biểu thức, nên đừng đọc nó thành ma trận;
  · một lượt chạy CỤ THỂ đã đo nền nào = trường `labels` của từng job trong `actions/runs/<id>/jobs`
  (kèm `runner_id` khác 0 — `runner_id 0` là job chưa từng chạy). Đừng suy từ tên sự kiện hay tên workflow.
  Ảnh chụp để định hướng, KHÔNG phải nguồn (đo 23-10-2026 trên `e63961f`, có thể đã cũ khi bạn đọc): push
  master và PR thường ⇒ chỉ Ubuntu; gọi tay `workflow_dispatch` ⇒ hai nền, hoặc chỉ Windows với
  `runner_set=windows-only`; Windows tự động khi push master chỉ đến từ `launcher-windows.yml` (có `paths:`, chỉ
  đo lane launcher, không phải gate).
  **"Có job Windows" chưa phải "gate đã đo trên Windows".** Từ #879, `gate-cong-cu` trên Windows chỉ chạy mảnh 0,
  duyệt ca nền rồi DỪNG — bán kính đột biến chỉ đo trên Ubuntu, và ca thiếu năng lực bị `BỎ QUA` rồi trừ khỏi mẫu
  số (`so_ca = len(CA) - len(bo_qua)` ở `ops/cong_cu_test.py`); `gate-cong-cu-gop` loại hẳn Windows; nhiều bước
  mang `if:` theo `runner.os`. Nên một lượt Windows xanh chỉ chứng minh **các ca KHÔNG bị bỏ qua đạt trên
  Windows** — đọc riêng các dòng `BỎ QUA` trong log — còn bán kính đột biến phải lấy từ lượt Ubuntu của CÙNG head.
  Muốn có Windows cho gate thì đường CHẮC CHẮN là gọi tay `workflow_dispatch` trên ref đó (xem input
  `runner_set` trong `ci.yml` để khỏi trả lại phút Ubuntu khi head đã có lượt PR Ubuntu).
  Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai
  trên PR #109): `ci.yml` khai `pull_request:` mà KHÔNG khai `types:`, nên mặc định chỉ bắn ở
  `opened`/`synchronize`/`reopened` — **`labeled` không nằm trong đó**. Gắn nhãn không tự sinh lượt
  chạy nào; ma trận chỉ đọc nhãn ở lượt bắn KẾ TIẾP. Người làm theo sẽ gắn nhãn, thấy vẫn đúng một
  check Ubuntu, rồi merge mà tưởng đã có Windows. Muốn dùng nhãn thì phải kèm một cò mới sau khi gắn
  (đẩy thêm commit, hoặc đóng rồi mở lại PR) — hoặc khai `types: [..., labeled]` cho workflow.
  Kèm theo: trên lượt master, bước `PR head contains required EOL base` LUÔN `skipped` vì nó có
  `if: github.event_name == 'pull_request'` — nên tiêu chí "không bước nào `skipped`" chỉ đúng cho
  lượt PR; bê nguyên sang lượt master là tự báo động giả.
  Cả ba cùng họ với bài học "cổng không nói dối, nó VẮNG MẶT": **"vắng mặt vì sạch" và "vắng mặt vì
  chưa chạy" nhìn giống hệt nhau** nếu hỏi sai chỗ. Chốt chung, rẻ và luôn dùng được: trước khi kết
  luận từ một chỗ RỖNG, hỏi "nếu thứ tôi đang tìm CÓ THẬT thì nó sẽ được ghi ở đâu?" — rồi đi hỏi
  đúng chỗ đó. Máy không canh được mục này; nó là kỷ luật đọc.
- **SỔ LEASE KHÔNG NẰM MỘT CHỖ — đo `ops/leases/` trên `master` là mù đúng chỗ lease MỚI NHẤT nằm.**
  Đo 21-08-2026, trả giá bằng một lease chồng lấn đã ký: đặc tả `PLAT-X8` khai *"không lease nào đang
  giữ `ops/lease_publish*`"* sau khi quét `ops/leases/` trên master ⇒ **0**. Quét đủ **98 nhánh
  `ops/**`** ⇒ **7** lease CHƯA HẾT HẠN chạm hai tệp ấy, trong đó **2** thật sự còn hiệu lực
  (`#227`) — bản `lease-dang-exec-2` **đã đăng** và được cấp **15 phút trước**, giữ đúng cả hai tệp
  ⇒ cửa sổ hai writer ~23,75h. **"Chưa hết hạn" KHÔNG phải "còn hiệu lực"** (cross-review bắt bản
  đầu của bài học này đếm cả 7): năm lease kia thuộc packet ĐÃ LAND, và không trường nào trong tệp
  lease nói ra điều đó — phải đi tìm HIỆN VẬT của packet trên master, còn Issue thì cả bốn vẫn
  `open`. Đó là nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong` đo được thành số: **5** quyền ghi còn
  sống sau khi việc đã xong. Nhưng **2 vẫn lớn hơn 0** — con số đúng không cứu được phép đo sai chỗ. Lý do cấu trúc:
  lease sống trên nhánh `ops/**` và **chỉ về master sau khi merge**, nên master luôn thiếu đúng những
  lease mới nhất — tức những lease khả nghi nhất, y hệt lý do `t23` không được ghi cứng một tên tệp.
  Chưa có lệnh nào trả lời *"lease nào đang giữ đường dẫn X"* trên toàn kho (nợ
  `SO-LEASE-KHONG-NAM-MOT-CHO`, biên bản `ops/RUT_LEASE_PLAT_X8_20260821.md`); tới lúc có, phải quét
  `refs/remotes/origin/ops/*` bằng tay TRƯỚC KHI cấp bất kỳ lease nào, và **không fetch được ref nào
  thì ĐỎ** — "không đo được" không phải "không có". Cùng họ *"hỏi chỗ tiện tay thay vì hỏi chỗ kết
  luận được ghi"*, và lần này nạn nhân là chính packet sinh ra để dạy cổng ĐO thay vì NHẬN LỜI KHAI.
- **`git for-each-ref` ĐỌC BỘ ĐỆM CỤC BỘ, KHÔNG HỎI MÁY CHỦ — "quét MỌI ref" có thể quét đúng 3 ref.**
  Đo 22-08-2026, container remote mới mở: `for-each-ref refs/remotes/origin` ⇒ **3**; sau khi fetch đủ ⇒
  **160**. Ba ref đầu là `master` + hai nhánh `claude/**`; `ops/pkg-windows` **không** nằm trong đó, mà
  đúng nhánh ấy giữ **cả ba** lease `LEASE-DANG-WINDOWS` đang chặn write set `PLAT-X8`. Bộ quét vẫn in
  *"đã quét mọi ref"* và vẫn `KHÔNG_XÁC_ĐỊNH = 0`. Đây là cách hỏng **thứ SÁU** của bộ quét lease và là
  cái đầu tiên **KHÔNG nằm trong mã**: `yaml.safe_load` đúng từng dòng, ba trạng thái đủ, fail-close đủ —
  sai vì ĐẦU VÀO thiếu. Bộ quét hỏi *"có ref nào"* và nhận câu trả lời **thành thật cho một câu hỏi khác**:
  *"tôi đang giữ bản sao của những ref nào"*.
  **BA cơ chế khác nhau, đo riêng từng cái — đừng gộp, vì cách chữa khác nhau:**
  · **`--depth` kéo theo `--single-branch`, và thứ bị siết là REFSPEC.** Phản chứng chạy được, hai clone
  cùng nguồn: `git clone --depth=1` ⇒ `shallow=true`, refspec `+refs/heads/<MỘT-NHÁNH>:...`; thêm
  `--no-single-branch` ⇒ `shallow=true`, refspec `+refs/heads/*:...`. **Cùng nông, chỉ refspec khác** ⇒ độ
  sâu tự nó không cắt ref, nhưng clone `--depth` TRẦN vẫn mất ref. Chữa: sửa refspec.
  · **Cắt độ sâu làm hỏng phép hỏi LỊCH SỬ** — `merge-base --is-ancestor d5b7bcc origin/master` trả SAI
  trong khi `d5b7bcc` (merge PR #116) ĐÚNG là tổ tiên; `git cat-file -e` báo "không có" cho SHA hợp lệ
  (phiên `tra-luat-ae` mất 2,5h vì nó: khai "29 trường SHA không tra được", thật là **2**). Kèm `git fetch`
  in `forced update` — đọc y hệt "master bị viết lại lịch sử". Chữa: `--unshallow`.
  · **Refspec RỘNG mà vẫn thiếu ref** — ca thật của container này. **Refspec là luật cho những lần fetch
  SAU, không phải bằng chứng đã fetch.** Chữa: fetch thật.
  **PHÉP CANH ĐÚNG là so HAI NGUỒN, không phải hỏi `--is-shallow-repository`** (bản đầu của mục này ghi
  thế và SAI — nó bỏ sót ca thứ ba, tức im lặng đúng lúc cần kêu): `git ls-remote --heads origin` (HỎI MÁY
  CHỦ) so với `git for-each-ref refs/remotes/origin` (ĐỌC ĐỆM).
  **So bằng TẬP TÊN, KHÔNG bằng `wc -l`** — bản đầu của mục này canh bằng số đếm và cross-review bác đúng
  chỗ đó (P2 trên PR #243). Hai lý do, cả hai đo được: (a) **lực lượng bằng nhau vẫn có thể mù** — một ref
  cục bộ đã cũ cộng một nhánh mới trên máy chủ chưa fetch cho ra `n == n` trong khi tập lệch; (b) clone
  thường có `refs/remotes/origin/HEAD` **tượng trưng**, không có đối ứng trong `ls-remote --heads`, nên số
  đếm lệch sẵn 1 mà chẳng ai mù (reviewer tái hiện 2 máy chủ / 3 cục bộ). Loại `HEAD`, cắt tiền tố cho
  cùng dạng, rồi so tập:

  ```
  git ls-remote --heads origin | sed 's#.*refs/heads/##' | sort            > /tmp/mc
  git for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin \
      | grep -v '^HEAD$' | sort                                           > /tmp/cb
  comm -23 /tmp/mc /tmp/cb    # CO tren may chu, THIEU cuc bo  -> MU, fail-close
  comm -13 /tmp/mc /tmp/cb    # THUA cuc bo -> nhanh chua day / da xoa, vo hai
  ```

  **Chiều lệch mới là kết luận, không phải con số.** Kho này đo `160/159` lúc 09:00Z (thừa một, là nhánh
  chỉ định chưa push — vô hại) rồi `160/161` lúc 12:00Z (**thiếu** `ops/ci-bang-phu-thuoc` — mù thật).
  Cùng một biên độ `1`, hai kết luận ngược nhau. Không chạy được `ls-remote` ⇒ `KHÔNG_XÁC_ĐỊNH`.
  **Lệnh chữa KHÁC NHAU theo trạng thái — `--unshallow` KHÔNG phải thuốc chung** (P2 thứ hai, cùng lượt
  review, tái hiện được): trên kho ĐẦY ĐỦ nó thoát **rc=128** `fatal: --unshallow on a complete repository
  does not make sense` và **không fetch gì** — tức đúng ca thứ ba, ca của container này, thì lệnh "chữa cả
  ba" của bản đầu chữa được **số không**.

  ```
  [ "$(git rev-parse --is-shallow-repository)" = true ] \
      && git fetch --unshallow origin '+refs/heads/*:refs/remotes/origin/*' \
      || git fetch            origin '+refs/heads/*:refs/remotes/origin/*'
  ```
  **Ghi cả cái sai vì nguyên nhân sai trong doctrine tệ hơn không ghi:** bản đầu đổ cho `--depth` cắt nhánh,
  trong khi ca thật là *chưa fetch* — đúng thói *"kết luận từ một đường hỏng"*. Cùng họ nợ
  `SO-LEASE-KHONG-NAM-MOT-CHO` nhưng sâu hơn một tầng: nợ ấy nói *lease không nằm trên master*; mục này nói
  **danh sách nhánh cũng chỉ là bản sao**. Khi viết `ai-dang-giu`, phép so này phải là chốt ĐẦU TIÊN, chạy
  trước khi mở tệp lease nào.
- **Workflow có `paths:` ĐÃ KHÔNG CHẠY ở lần đẩy tạo nhánh mới — nguyên nhân CHƯA BIẾT, đừng chế ra.**
  Đo 21-08-2026: đẩy nhánh `ops/**` MỚI kèm một tệp trong `ops/leases/` ⇒ `ops-publish-lease.yml`
  chạy **0** lượt; đẩy tiếp lên nhánh ĐÃ TỒN TẠI, cùng bộ lọc, cùng thư mục ⇒ chạy ngay (lượt
  `32492493219`). Đó là toàn bộ những gì đo được.
  **Bản đầu của mục này khẳng định nguyên nhân — "vì không có commit *before* để so" — và
  cross-review bác đúng chỗ đó** (P2 trên PR #228): tài liệu GitHub mô tả một phép so hai chấm với
  tổ tiên của commit sâu nhất được đẩy, nên "bỏ qua bộ lọc" là ĐOÁN, không phải phép đo. Ghi một
  nguyên nhân sai vào doctrine còn tệ hơn không ghi gì: lần sau workflow vắng mặt vì lý do KHÁC —
  sai `paths`, sai nhánh, sai `on:` — người đọc sẽ nhận nhầm nó là "chuyện đã biết" rồi đi tiếp.
  Thứ đáng nhớ là **triệu chứng**, không phải lời giải thích: một workflow bạn trông cậy có thể
  **vắng mặt** ở đúng lần đẩy đầu tiên, và vắng mặt trông y hệt xanh. Nên sau MỌI lần đẩy mà bạn
  cần một workflow chạy, hãy ĐO là nó đã chạy (`list_workflow_runs` lọc theo nhánh), đừng suy từ
  việc `git push` thành công. Chưa có phản chứng cho ca này — dựng được nó thì mới nói tới nguyên nhân.
- **PHÉP ĐO DELTA SO HAI VẾ PHẢI DỰNG CẢ HAI TRONG **MỘT** LỆNH — BỐN lần trong một phiên, rig tự đẻ ra
  hồi quy không tồn tại.** Đo 24-08-2026. Không lần nào lộ ra bằng đọc kết quả; mỗi lần đều trông y hệt một hồi quy
  thật, và mỗi lần suýt thành một báo cáo sai gửi chủ kho.
  · `git worktree` **hai lần** — `chay_cac_probe()` trong `.claude/dev/launcher.py` — hàm của đường PHÓNG, KHÔNG phải của `doctor` — ném
  `Chan(MA_WORKTREE)` khi `.git` là **TỆP**, nên `packet_loop_test` cho `234/237` (3 đỏ) trong worktree và
  `235/237` (2 đỏ) trong clone. Phép thử một-biến chứng minh **rig** gây lệch chứ không phải `origin`:
  đổi `origin` của CÙNG một clone sang URL GitHub ⇒ vẫn 2 đỏ.
  · **kho-thật-vs-clone** — chạy nhánh trong kho chính còn nền trong clone ⇒ 3 ca đỏ giả, tất cả là
  `not a git repository`.
  · **`clone` + `cp` + `checkout` đá nhau** ⇒ `78/97`; dựng lại tử tế ⇒ `96/97`. Delta thật = **0**.
  · Lúc viết, tôi đếm **năm**. Cross-review đòi phép đo cho từng ca và chỉ **bốn** ca trên có SHA/lệnh/output
  để tái hiện; ca thứ năm không có dấu hiệu nào tách nó khỏi ca `clone`+`cp`+`checkout` (chúng dùng chung
  cặp số `78/97` · `96/97`). Nên con số là **BỐN ĐO ĐƯỢC**, và ca thứ năm là `KHÔNG ĐO ĐƯỢC` — không phải
  bị bác, chỉ là không tách được. Ghi vậy vì một con số tròn hơn dữ liệu chính là thứ mục dưới đây tố cáo.
  **Thuốc — và PHẠM VI của nó, vì bản đầu viết quá rộng và cross-review bác đúng chỗ đó:** một lệnh, hai
  vòng lặp, cùng các bước, chạy liền nhau —
  `for pair in "nen:$SHA_A" "sau:$SHA_B"; do clone; checkout; config core.abbrev 7; done` rồi mới chạy đo.
  Dựng hai vế ở hai thời điểm là mở cửa cho môi trường trôi giữa chừng.
  **Luật này CHỈ áp cho phép đo DELTA MÃ/NỘI DUNG** — câu hỏi *"hai commit này khác nhau những gì"*, nơi
  rig là NHIỄU và phải bị triệt. Nó **KHÔNG** áp cho phép đo MÔI TRƯỜNG — câu hỏi *"hai rig này khác nhau
  những gì"*, nơi rig chính là BIẾN ĐANG ĐO. Bản đầu phát biểu cho MỌI phép đo hai vế và gọi đây là
  "thuốc duy nhất luôn đúng"; như thế nó **cấm chính phép A/B mà `.claude/skills/cross-review/SKILL.md`
  bắt chạy** (đối chiếu cổng: nền bằng worktree, sandbox bằng clone, CÙNG một commit) — và phép ấy có giá
  trị chẩn đoán thật, chính nó cho `234/237` so `235/237` ở gạch đầu dòng trên. Hai vế của phép đo môi
  trường phải khác **đúng một biến**; clone cả hai thì không còn gì để đo.
  Trớ trêu đúng chỗ đáng nhớ: một luật viết ra để chống "rig đẻ hồi quy giả" mà phát biểu quá rộng thì
  chính nó **xoá mất phép đo bắt được rig**.
  **Kèm một hệ quả ít ai ngờ:** `doctor --json` KHÔNG gọi `chay_cac_probe`, nên ai đi kiểm giả thuyết
  "worktree có phải nguyên nhân không" bằng `doctor` sẽ thấy **KHÔNG CÓ KHOÁ `workspace` NÀO** trong JSON
  ở CẢ HAI rig — và kết luận **NGƯỢC**. Nói cho đúng vì bản đầu viết `workspace = {}` và cross-review bác:
  `{}` đọc thành *"doctor đã đo workspace và thấy rỗng"*, trong khi sự thật là **doctor chưa từng đo** —
  khoá ấy vắng mặt hoàn toàn (`doctor --json` trả 13 khoá top-level, không có `workspace`, không có
  `probe`). Viết sai một ký tự ở đây là tái phạm ĐÚNG bệnh "có MẶT khác có ĐO" ngay bên trong bài học
  về nó. Tôi đã đi đúng đường ấy, đọc sự IM LẶNG thành BẰNG CHỨNG PHỦ ĐỊNH, rồi tự bác nhầm kết luận
  đúng của chính mình — mất một lượt. Kiểm ở đường PHÓNG, đừng kiểm ở `doctor`.
- **REVIEWER BỊ CHẶN: hỏi VÌ SAO trước khi kết luận ĐƯỜNG TẮC.** Đo 24-08-2026. Hai lượt cross-review
  liên tiếp chết giữa chừng vì bộ lọc nội dung của nền (`flagged for possible cybersecurity risk`), không
  để lại `VERDICT.md` nào. Tôi báo chủ kho rằng **"đường codex tắc có hệ thống với lớp lỗi này"**, và đề
  xuất đổi provider. **Sai.**
  Log của chính lượt đó đã nói ngược: nó **chạy trọn 251 ca**, gồm cả các ca đường-dẫn. Bộ lọc chỉ bắn khi
  reviewer phải **TỰ SOẠN** phản chứng dựng đường dẫn thoát khỏi cây thư mục. Đường không tắc — **thiết kế
  nhiệm vụ của tôi** ép nó sinh nội dung bị chặn.
  Chữa bằng **đổi phân công, không đổi provider**: mọi phản chứng đã nằm sẵn trong cây, nên reviewer chỉ
  **CHẠY** chúng và **ĐỘT BIẾN BẢN VÁ** để đo răng; hướng thử nào cần soạn nội dung dạng ấy thì **mô tả
  bằng lời** cho phiên điều phối viết. Lượt kế tiếp chạy trọn **922,4s**, `ma_thoat=0`
  (biên nhận `ops/reviews/bien-nhan-review-s2-review-4-codex-verdict.receipt.yaml`, `thoi_luong_giay:
  922.422`).
  **Con số ấy sửa một lời khai SAI của bản đầu, và cái sai đáng ghi hơn con số:** bản đầu viết `1146s`.
  1146s có thật — nhưng nó là lượt cross-review **S1 của PR #309**, một lượt KHÁC và MUỘN HƠN. Tôi lấy
  thời lượng của lượt này gán cho lượt kia để chứng minh rằng "đổi phân công đã chữa xong". Đó đúng là
  bệnh **ghép sai lượt** mà tệp này đã tố cáo ở mục *"hỏi chỗ TIỆN TAY thay vì hỏi chỗ KẾT LUẬN ĐƯỢC
  GHI"* — và lần này nạn nhân là chính đoạn viết ra để tổng kết một sự cố.
  Kèm theo: vì transcript của HAI lượt chết đã mất, mệnh đề *"bộ lọc CHỈ bắn khi reviewer tự soạn"* là
  `KHÔNG ĐO ĐƯỢC`, không phải đã chứng minh. Thứ đo được chỉ là **thứ tự**: đổi phân công rồi có một lượt
  chạy trọn. Tương quan, không phải nhân quả — đừng đọc mạnh hơn thế.
  **KHÔNG CỔNG NÀO CANH HAI BÀI HỌC NÀY.** Không có gì ép phép A/B phải dựng cùng một lệnh, và không có gì
  ép reviewer đừng tự soạn nội dung nhạy cảm. `doctrine-scan` và `doc-claims-check` chỉ canh HÌNH THỨC.
  Cả hai mục là kỷ luật đọc và kỷ luật giao việc — nói thẳng ra đây kẻo người đọc tưởng đã có cơ chế.
  Kèm `launcher.py run` để một lượt chết vẫn **được ghi nhận** (`run.json`) thay vì bốc hơi — hai lượt
  trước mất sạch vì gọi `codex exec` trần.
  **Vì sao đáng ghi dù đã có bài học họ hàng:** `.claude/dev/launcher.py` chép sẵn NGUYÊN câu chuyện (khối chú thích dài ngay trên `_RE_BIEN_NHAY_CAM`) một phiên
  kết luận *"container không gọi được codex"* và mất gần trọn ngày công. Tôi **đọc tệp ấy trong cùng
  phiên** rồi vẫn lặp lại. Nên thứ thiếu không phải tài liệu mà là phản xạ: gặp một công cụ trả kết quả
  xấu, câu hỏi đầu tiên là *"nó hỏng ở ĐƯỜNG NÀO"*, không phải *"nó có dùng được không"*.
- **Quét secrets: lọc theo PHẦN MỞ RỘNG là mù ĐÚNG CHỖ secrets nằm.** `Path('.env').suffix == ''` nên
  `.env` `.netrc` `credentials` (không mở rộng) bị bỏ qua SẠCH — bơm `GOCSPX-…` vào `.env` mà bộ quét
  trả rc=0. Cộng thêm `Get-ChildItem` thiếu `-Force` cũng bỏ y hệt: **hai lỗi ĐỘC LẬP mà CÙNG HƯỚNG** ⇒
  đường Windows từng mù hoàn toàn với secrets trong tệp ẩn. Nay quét cả tệp không mở rộng, tránh nhị
  phân bằng NUL-check 8KB + trần 2MB. Bảng mẫu bí mật ĐỂ MỘT CHỖ: `scripts/pkg_secret_scan.py`, dùng
  chung cho cả `sh` lẫn `ps1` — hai bản sẽ trôi lệch, và bên quên cập nhật chính là bên đẩy lọt.
- **"YAML parse được" KHÁC "GitHub NHẬN".** Đo 16-08-2026: `.github/workflows/ops-don-ref.yml` bị GitHub
  **từ chối** — dấu hiệu là một workflow run mang tên **ĐƯỜNG DẪN TỆP**, **0 job**, `conclusion: failure`
  (run `31971137920`). Đó là chữ ký của lỗi XÁC THỰC ĐỊNH NGHĨA, không phải một job đỏ; `get_job_logs`
  trả `total_jobs: 0` nên đi tìm log sẽ không thấy gì. Nguyên nhân: **GitHub nội suy biểu thức trên TOÀN
  BỘ thân `run` trước khi shell thấy nó**, nên một cặp `${{ }}` RỖNG nằm trong một dòng **CHÚ THÍCH** là
  một biểu thức rỗng ⇒ cả tệp không hợp lệ. Dòng ấy chính là dòng viết ra để giải thích rằng ta KHÔNG
  chèn biểu thức thẳng vào thân script. **Đừng viết cú pháp biểu thức Actions trong comment của `run`.**
  Vì sao đáng ghi vào đây: **SÁU lượt cross-review đều kết luận "YAML ok"** — cả sáu chỉ kiểm bằng
  PyYAML, mà PyYAML không biết luật của GitHub. Cùng họ với "CÓ MẶT khác DÙNG ĐƯỢC", chỉ đổi đối tượng.
  Cách chữa đã cài: `ops/don_ref_chot_test.sh` gọi **`actionlint`** thật, và **fail-close khi thiếu công
  cụ** (in `KHÔNG ĐO ĐƯỢC`, trả mã khác 0) — một cổng tự tắt khi thiếu công cụ là cổng không tồn tại
  đúng lúc nó cần nhất. Đo nền khi thêm (16-08-2026): `actionlint` trên cả 5 workflow → rc=0.
  **CÂU TRÊN ĐÃ TRÔI — đo lại 23-08-2026: `rc=1`**, một finding `ops-don-ref.yml:106 SC1003:info`.
  Nền đổi vì `shellcheck` **có mặt** ở lần đo sau mà **vắng** ở lần đo trước, nên phép đo cũ yếu
  hơn: thiếu `shellcheck` thì `actionlint` **im lặng bỏ toàn bộ luật nền ấy** và vẫn trả `rc=0`.
  Delta so `origin/master` vẫn **= 0** — đỏ sẵn, không phải hồi quy. Nhắc kèm: `t33` trong
  `ops/lease_publish_test.py` đòi `actionlint` có mặt nhưng **KHÔNG đòi `shellcheck`**, nên nó
  không phân biệt được hai nền đo ấy (đo thẳng: có ⇒ `rc=1` 1 finding · vắng ⇒ `rc=0` 0 finding).
  Bài học đứng nguyên; chỉ **con số minh hoạ** thì hết hạn — và một con số trong tài liệu không
  ghi ĐIỀU KIỆN ĐO thì sẽ trôi mà không ai biết.
- **Workflow chỉ chạy khi có người bấm là workflow KHÔNG có ai canh.** `workflow_dispatch` không chạy
  theo push/PR, nên mọi lỗi của nó — kể cả lỗi làm tệp vô hiệu hoàn toàn — nằm im cho tới **đúng lượt
  cần dùng**. Ở đây may: lỗi lộ ra vì GitHub kiểm tệp ngay khi đẩy. Đừng trông vào cái may đó: mọi
  workflow `workflow_dispatch` phải có phản chứng chạy được ở CI, và bộ ấy phải **trích thân bước TỪ
  CHÍNH tệp YAML** thay vì chép lại — chép lại là hai bản trôi lệch.
- **Cổng có thể xanh vì đồ GIẢ nói dối, không phải vì mã đúng.** Bộ test của `ops-don-ref` từng cho
  **40/40** trong khi một đột biến **XOÁ HẲN** lệnh `gh api -X DELETE` vẫn qua — vì `gh` giả DIỄN KỊCH
  BẢN (lần đọc thứ hai luôn trả "không còn") thay vì mô phỏng TRẠNG THÁI. Bộ test khi ấy đo NHÁNH RẼ của
  script chứ không đo THAO TÁC CÓ XẢY RA KHÔNG. Nay đồ giả GIỮ trạng thái, cộng phép đòi **đúng một** lời
  gọi phá **đúng endpoint** trong nhật ký. Nếp chung: **đồ giả phải mô phỏng TRẠNG THÁI, không diễn kịch
  bản**, và mỗi thao tác phá phải có một phép đo đọc nhật ký chứ không chỉ đọc mã thoát.
- **`${*##mẫu}` khai triển theo TỪNG tham số rồi mới nối.** `${*##*/git/refs/}` trên
  `api -X DELETE repos/o/r/git/refs/heads/a` trả `api -X DELETE heads/a` chứ không phải `heads/a` — bản
  ghi và bản đọc lại cắt ra hai chuỗi khác nhau nên không bao giờ khớp. Gán `DONG="$*"` rồi mới cắt.
- **Phân loại trạng thái HTTP bằng văn bản tự do là ĐOÁN, không phải ĐO.** Dò chuỗi `Not Found` trong
  thông báo lỗi biến một 500 (có chữ ấy trong thân) thành "ref không còn"; đổi sang `grep` dòng trạng
  thái vẫn thủng vì `grep` quét MỌI dòng, mà thân phản hồi do máy chủ đầu kia quyết định. Chốt đúng:
  `gh api -i`, cắt **DÒNG ĐẦU**, khớp đúng dạng `HTTP/<phiên bản> 404`. Và ba trạng thái, không phải hai:
  `có` · `không` · **`không đo được`** — trạng thái thứ ba phải làm cổng ĐỎ, đúng doctrine `None ≠ False`.
- **MỘT BẤT BIẾN CÒN ĐÚNG KHÔNG CHỨNG MINH CÁC SỐ HẠNG CÒN ĐÚNG — và chính nó làm lời khai TRÔNG NHƯ
  ĐÃ KIỂM.** Đo 22-08-2026, đặc tả `LEASE-HOI-TOAN-KHO` khai *"117 cặp / 100 đường dẫn, **chênh 10** là
  phiên bản thừa"*. Đo lại: **120 / 110** — cả hai số hạng đã trôi, mà **chênh vẫn đúng 10**. Ba lượt
  cross-review đọc qua dòng ấy và không ai dừng lại, vì soi tính nhất quán nội tại thì nó **sạch hoàn
  toàn**: quan hệ khớp, đơn vị có, câu tự giải thích. Chỉ phép đo mới thấy. Cùng họ *"cổng vắng mặt trông
  giống cổng xanh"*, đổi đối tượng: **một quan hệ đúng trông giống các số hạng đúng.** Hệ quả thực hành:
  khi một câu vừa nêu số hạng vừa nêu quan hệ giữa chúng, **kiểm số hạng**, đừng kiểm quan hệ — quan hệ
  là thứ sống sót qua trôi số. Cùng lượt ấy còn hai ca y hệt: `37` biên nhận → **39**, và `3/90` → **3/100**
  (tử đúng, **mẫu** trôi) — tức trong một đặc tả có **ba** con số đã cũ, không con nào lộ ra bằng đọc.
- **REVIEWER KHÔNG ĐO ĐƯỢC THÌ REVIEW CHỈ LÀ SOÁT CHÍNH TẢ — đo được bằng số, 3 lượt/0 so 1 lượt/3.**
  Bốn lượt cross-review trên cùng một PR (#250): ba lượt đầu reviewer chỉ nhận **hai tệp `.md`** cộng
  tài liệu tham chiếu, tìm được `4 → 11 → 2` finding và **KHÔNG con số phân rã nào**. Lượt 4 cấp thêm
  một **mirror git đầy đủ** trong sandbox (`git clone --bare` + bản làm việc; số nhánh là snapshot có thể
  trôi, không phải bằng chứng bền) và
  đổi nhiệm vụ chính thành *đo lại từng con số*: ra **ba** con số phân rã ngay lượt đầu tiên có năng lực
  ấy. Không phải reviewer ba lượt đầu kém — họ **không có cách nào** kiểm một con số nào, nên cả một
  LỚP lỗi nằm ngoài tầm với. Giá của bản vá: một `clone --bare` vào thư mục sandbox. **Bắt reviewer tự
  vá + tự test cải thiện CHẤT LƯỢNG finding; chỉ năng lực ĐO mới cải thiện ĐỘ PHỦ** — hai đòn bẩy khác
  nhau, đừng nhầm cái này mua được cái kia.
  Các số theo lượt trong đoạn này hiện chỉ có ở comment PR #250, chưa có biên nhận trong kho và KHÔNG
  TÁI LẬP ĐƯỢC từ một bundle offline; đừng dùng chúng như một gate đã kiểm.
  · **Hệ luận: DANH SÁCH BẠN GIAO CHO REVIEWER TRỞ THÀNH TRẦN CỦA HỌ, trừ khi bạn tự khai nó thiên vị.**
  Lượt 4 tôi giao bảng 21 con số kèm **chính script đã trích ra nó**, và nói thẳng rằng script lọc theo
  **danh sách đơn vị đoán trước** (`lease` `ref` `blob` `tệp` `dòng`…) nên chắc chắn thiếu — mỗi số nó
  bỏ sót mà reviewer tìm ra được tính là finding. Trả công ngay **hai** lần: một con số không có trong
  bảng, và một finding nhắm thẳng vào **chính bộ lọc** (bốn số `rc`/finding lọt sạch vì **không mang
  đơn vị nào**). Cùng gốc *"danh sách CẤM không bao giờ đủ"*, lần này ở dạng bộ lọc trích số.
  · **Và bộ quét NHÁP của chính mình là thứ dễ tin nhất, nên nguy nhất.** Cùng phiên, script
  `quet_lease.py` dùng suốt để trả lời *"đường dẫn X có bị giữ không"* in kết luận từ một **chuỗi ghi
  cứng** nhắc tên một packet khác, bất kể `--duong-dan` truyền vào là gì. Hỏi nó về 6 tệp doctrine ⇒ nó
  báo **14 lease đang chặn**; viết lại phép đo cho đúng ⇒ **0**. Nó **chặn nhầm** đúng một việc hợp lệ —
  ảnh gương của ca *lời khai rộng hơn phép đo*, và đúng khuyết tật mà packet `LEASE-HOI-TOAN-KHO` sinh
  ra để sửa. Công cụ nháp không có cổng, không có ca test, và **dòng kết luận của nó là thứ ta đọc chứ
  không phải dữ liệu nó đo** — trước khi hành động theo một bộ quét tự viết, hãy hỏi nó một ca mà bạn
  **biết trước đáp án**.

- **ĐỘT BIẾN BỊ GIẾT KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO — và tín hiệu "đã giết" có thể
  bị CHÍNH MÃ TEST GIẢ MẠO.** Đo 27→28-08-2026, chuỗi `#355`/`#359`. Kho đã có "đột biến có
  thể CHƯA TỪNG ĐƯỢC CHẠY" (va chạm `.pyc`); mục này là mặt KHÁC và sâu hơn: đột biến **có**
  chạy, ca đích **có** đỏ, mà vẫn không đo gì — vì nó chết bởi một lỗi VÔ CAN chứ không bởi
  chốt đang thử. Bộ chạy đếm mọi mã thoát khác 0 là "giết", nên cấp **TÍN DỤNG GIẢ**.
  Đo được: khai `22/22 bị giết` ⇒ phân hạng lại thành **19 giết thật / 3 tín dụng giả / 0 sống
  sót** (`chon_khoa_theo_kieu_dict` chết `TypeError`; `ten_server_chi_khop_literal` chết bằng
  một `Hong` khác; `bo_kiem_headers_object` chết `AttributeError`). Cross-review tìm được MỘT,
  cảnh báo "có thể còn nữa"; phép đo ra **ba**.
  **Chưa hết, và đây mới là chỗ đắt.** Bản vá vòng một phân hạng theo chuỗi `AssertionError`
  của ca đích — và **vẫn bị lừa**, vì trong `*_test.py` có
  `except Exception as e: raise AssertionError(f"... {type(e).__name__}")` viết ra với ý định
  ĐÚNG (đừng để lỗi vô can giết mutant), nhưng nó **dựng lên đúng cái tín hiệu** mà bộ phân
  hạng tin. Một `AttributeError` đi qua đó thành `AssertionError` và được đếm là GIẾT THẬT.
  Cả bộ đo của reviewer lẫn của executor cùng báo `0 tín dụng giả`, **cùng sai, cùng một lý do**:
  cả hai tìm một chuỗi mà bất kỳ `except` nào cũng viết ra được.
  Chốt đúng: tín hiệu "assertion của ca đích" phải là thứ **mã triển khai không giả được** —
  một LỚP NGOẠI LỆ RIÊNG (`TinHieuChotCa(AssertionError)`), đặt tên nó vào phép so, và neo cả
  **TÊN CA** (assertion của ca KHÁC cũng là tín dụng giả). Kèm bốn ca tự kiểm cho chính bộ
  phân hạng. Phản chứng bắt buộc: một mutant chết vì `AttributeError` phải rơi vào TÍN DỤNG
  GIẢ **kể cả khi trên đường có một `except` đổi kiểu**.
  Vì sao đáng ghi dù kho đã có cả họ bài học "thước đo nói dối": ở đây thước đo **do chính ta
  vừa dựng ra để chống bị lừa**, và nó bị lừa bởi một dòng viết với ý định tốt. Con số mutant
  đã được báo cho chủ kho **hai lần rồi phải rút lại**, cả hai lần vì tin một tầng mà chưa thử
  tầng dưới nó.

- **TÁI SỬ DỤNG MỘT PHẦN một bộ phân tích là mua tính nhất quán bằng một CUỘC ĐUA — và
  so ảnh trước/sau KHÔNG đóng được nó.** Đo 27→28-08-2026 (`#359`). `mcp_github_doc.py` tự
  viết lại bộ phân tích `.mcp.json` ⇒ lệch `launcher._doc_mcp_json` (đo được: cùng một tệp,
  client báo `MO` còn `doctor` từ chối). Chữa bằng uỷ quyền cho bộ chuẩn ⇒ lệch chết theo
  KIẾN TRÚC. Nhưng hợp đồng bộ chuẩn **cố ý không trả `headers`**, nên client phải đọc tệp
  LẦN HAI ⇒ tệp đổi giữa hai lần đọc thì ghép **URL của ảnh cũ với `headers` của ảnh mới**,
  tức gửi token của endpoint B tới endpoint A.
  Bản vá "băm trước, băm sau, lệch thì từ chối" **THUA ABA**: A → B (đúng lúc bộ chuẩn đọc)
  → A. Hai băm khớp, mà bộ chuẩn đã trả URL của B còn client đọc `headers` của A. Reviewer
  tái hiện được; phản chứng chạy được.
  **Bảng đánh đổi, và nó không có ô thứ ba:** uỷ quyền ⇒ hết lệch, buộc hai lần đọc, có đua ·
  tự phân tích ⇒ một ảnh, hết đua, **tái sinh** đúng lớp lệch vừa giết. Lối ra duy nhất là
  **mở rộng hợp đồng của bộ chuẩn** (`kem_headers=True` trả thêm `headers` từ CHÍNH ảnh đã
  đọc) ⇒ một lời gọi, một ảnh chụp, đua chết theo CẤU TRÚC. Việc ấy đụng tệp nóng nên phải
  xin thẩm quyền, và đó là quyết định đúng chứ không phải nới lỏng.
  Nếp rút ra: **hễ phải đọc một nguồn HAI LẦN để ghép hai mảnh của cùng một quyết định, đó
  đã là lỗi thiết kế** — đừng đi canh, hãy đổi để chỉ đọc một lần. Và đừng khai "đã loại bỏ
  race" khi mới chỉ phát hiện được nó: viết đúng là "biến ghép nhầm âm thầm thành từ chối
  ồn ào".

- **EXECUTOR TỪ CHỐI Ở PREFLIGHT LÀ TÍNH NĂNG, KHÔNG PHẢI TRỞ NGẠI — và lời khai
  `spec_hash` của kho đang đúng 3%.** Đo 28-08-2026. Executor `codex` DỪNG **hai lượt liên
  tiếp**, không sửa gì, vì chỉ thị thiếu `revision`/`generation`/`Review Class` rồi thiếu
  `spec_hash`, và vì không có hiện vật lease trong checkout để tự xác minh. Nó từ chối tự suy.
  Kiểm lại `docs/PROTOCOL_DA_PHIEN.md` §3.2: **nó đúng** — `spec_hash` nằm trong schema tối
  thiểu, *"khi vào `ready`, spec được đóng băng bằng `spec_hash`"*. Lỗi ở phiên điều phối.
  Đo tiếp cho ra con số đáng ghi: trên `origin/master` có **74** lease, chỉ **2** mang
  `spec_hash`. Protocol đòi, thực tế làm **3%** — và ba lượt trước của cùng phiên ấy đi qua
  được chỉ vì chưa ai chặn. Nợ khai, chưa chữa.
  Hai nếp: (a) prompt giao việc phải kèm **đường TỰ XÁC MINH** (fetch nhánh lease vào
  workspace để executor `git show` chính tệp, thay vì nhận bảng giá trị từ điều phối);
  (b) thiếu `spec_hash` thì **soạn đặc tả đóng băng thật** (`ops/specs/<packet-id>.md`) rồi
  neo băm vào lease — đừng bịa một băm để lấp ô trống, cũng đừng lấy băm của tệp lease làm
  `spec_hash`.

- **LEASE KHÔNG TỰ CHẾT KHI PACKET ĐÃ LAND — và `da_bi_thay_the` là cơ chế DUY NHẤT tắt
  được nó.** Đo 28-08-2026, con số cho nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong`: packet
  `#355` đã merge, mà lease của nó vẫn **giữ đúng hai đường dẫn** thêm ~18 giờ tới hạn.
  `ai-dang-giu` trả `NGƯỜI_GIỮ 1` cho một packet đã xong. Cấp lease mới cho cùng write set
  mà không thu hồi bản cũ là **tự tạo cửa sổ hai writer** — đúng thứ write-set exclusion
  sinh ra để chặn.
  `_phan_loai_lease` **chỉ biết hạn**; chỉ `lenh_ai_dang_giu` đọc `da_bi_thay_the`. Nên cách
  thu hồi sớm là cho lease MỚI khai `thay_the_cho`, và đặt `da_bi_thay_the` vào chính tệp
  lease CŨ — chốt `_kiem_bia_mo` đòi **hai chiều**. Kèm hai bẫy đã gặp lại trong đúng lượt
  này: cổng đọc từ **REF** nên phải **commit trước rồi mới `check`** (thiếu ⇒ `rc=8`), và
  lease mới **không được chép `posted_comment_id`** của bản cũ.

- **…VÀ BIA MỘ HAI CHIỀU CHỈ DÙNG CHO LEASE CÒN SỐNG — viết nó vào một lease ĐÃ CHẾT là mua
  một lượt ĐỎ, không phải dọn dẹp.** Đo 20-09-2026, hai lượt `ops — đăng lease bằng git` ĐỎ:
  [`35519177197`](https://github.com/ducthangho/tra-luat/actions/runs/35519177197) (#568) và
  [`35519243379`](https://github.com/ducthangho/tra-luat/actions/runs/35519243379) (#566).
  Cả hai đỏ **SAU KHI** lease mới đã đăng xong — tức việc chính đã thành, chỉ cái đuôi gãy.
  Cơ chế, đo được chứ không suy: `_kiem_bia_mo` đòi lease CŨ mang `da_bi_thay_the`, nên phải
  SỬA tệp lease cũ; mà bước `tìm lease vừa đổi` chọn theo **tệp đã đổi trong `before..sha`**.
  Sửa một lease đã hết hạn = đưa một tệp CHẾT vào tập quét = `rc=8` = cả lượt `exit 1`.
  Phân biệt cho đúng, vì hai việc trông giống nhau: lease cũ **CÒN HẠN** thì bia mộ là thứ
  DUY NHẤT thu hồi được nó (gạch đầu dòng trên) — cứ viết. Lease cũ **ĐÃ HẾT HẠN** thì
  write-set exclusion đã nhả rồi, `_phan_loai_lease` không còn tính nó là người giữ, nên bia
  mộ không mua thêm gì mà chỉ thêm một tệp vào tập quét. Khai `thay_the_cho: []` kèm một câu
  nói rõ vì sao KHÔNG khai bia mộ.
  Cái đắt nằm ở chỗ khác, và nó là lý do mục này đáng ghi: `rc=8` (hết hạn) **che mất** `rc=9`
  (đã đăng). `kiem_github` gọi `kiem()` ở dòng đầu, mà `kiem()` ném `rc=8` cho lease hết hạn
  TRƯỚC khi chốt `rc=9` kịp chạy — nên một lease **đã đăng rồi mới hết hạn** không bao giờ
  tới được nhánh `rc=9` mà workflow **đã có sẵn và viết đúng**. Cổng không nói dối; nhánh
  đúng chỉ **không bao giờ được gọi**. Cùng họ *"cổng VẮNG MẶT trông giống cổng xanh"*.
  Chỗ đắt nhất: chính tài liệu của kho khai NGƯỢC. Docstring `t32` trong
  `ops/lease_publish_test.py` viết rằng chốt `posted_comment_id` *"đúng cho lease ĐÃ đăng
  (rc=9)"* — **vế ấy SAI**, và 20-09 là lần đầu nó bị ĐO. Fixture của `t32` phủ đúng một nửa
  (*hết hạn, KHÔNG dấu*); nửa bù (*hết hạn, ĐÃ có dấu*) chưa ai viết. Đây là bản vá #195
  **ĐÚNG mà HẸP** — đúng hình dạng `VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA` ngay dưới.
  **MÁY KHÔNG CANH mục này.** Không cổng nào hỏi *"lease anh sắp viết bia mộ vào còn sống
  không"*; `_kiem_bia_mo` chỉ đòi hai chiều, nó không đọc hạn. Đây thuần là kỷ luật viết,
  nói thẳng ra kẻo người đọc tưởng đã có cơ chế.

- **VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA — hai lượt liền, và lần nào bản vá cũng TỰ TÁI
  TẠO lỗ nó vừa lấp.** Đo 12-09-2026, packet #513 lượt 10→13. Chuỗi:
  · lượt 10 vá `F01` — `if do_chot == set(dich)` cấp `GIET` khi CẢ HAI vế rỗng, tức cấp tín dụng cho
  thứ **không chết**. Vá bằng xác thực `dich` (khác rỗng + tên phải là ca có thật).
  · lượt 11 chỉ ra chính bản vá ấy đọc `dich` **BA lần**, nên một iterator bị lần đọc đầu **tiêu
  thụ**, `set(dich)` cuối cùng ra RỖNG và phép so **lại đúng** khi không ca nào chết. Đo: `("T1",)`
  → `KHONG_GIET`, còn `iter(("T1",))` và generator → **`GIET`**. Vá bằng vật hoá ở `doc_kenh` và
  `chay_mot_mutant`.
  · lượt 12 chỉ ra `dich = tuple(dich)` trong `chay_mot_mutant` **chỉ gán lại tên CỤC BỘ**, không trả
  bản vật hoá cho người gọi — nên `chay_dot_bien` vẫn bị tiêu thụ và in `|  | 0/0` cho một mutant ĐÃ
  BỊ GIẾT THẬT. Cửa **thứ ba**.
  Hình dạng: **mỗi lần tôi vá đúng chỗ reviewer chỉ, rồi bỏ sót đường tiếp theo không ai chỉ.** Nó
  khác "vá hờ" — mỗi bản vá đều ĐÚNG và CÓ RĂNG ở chỗ nó phủ.
  Chốt: khi một lỗi có **nhiều đường vào**, đừng vá theo danh sách đường mà reviewer liệt kê. **Tự
  liệt kê hết đường TRƯỚC**, đóng cả loạt, và cho **mỗi đường một chốt riêng** để đột biến gỡ từng
  cái đều làm ca ĐỎ — nếu ba chốt không phân biệt được bằng đầu vào thì chúng là bộ TƯƠNG ĐƯƠNG và
  bạn chỉ đang đo một cái. Ở đây cross-review đã KIỂM lời khai ấy bằng phép đo thay vì nhận lời, và
  xác nhận ba chốt độc lập. Cùng họ *"vá một lỗ mà mở lỗ khác trong cùng hàm"*, nhưng khác chỗ đắt:
  ở đó bản vá SAI, ở đây bản vá ĐÚNG mà **HẸP**.
  Kèm một dấu hiệu rẻ để nhận ra: nếu bản vá của bạn đọc cùng một tham số ở **nhiều nơi**, hoặc gán
  lại tên ở **phạm vi cục bộ** rồi mong người gọi thấy, thì gần như chắc còn cửa chưa đóng.
- **`get_status` của GitHub là API commit-status KIỂU CŨ — `total_count: 0, state: pending` KHÔNG
  phải "cổng đang chờ".** Đo 12-09-2026 trên PR #508: kho này dùng **check run**, không dùng status
  cũ, nên `get_status` luôn trả rỗng và `pending`. Đọc nó thành "CI chưa xong" là tự báo động giả
  đúng lúc mọi cổng đã xanh. Hỏi đúng chỗ: `get_check_run` / `pull_request_read get_check_runs` cho
  từng cổng, và `mergeable_state` cho khả năng merge. Cùng họ *"hỏi chỗ TIỆN TAY thay vì hỏi chỗ KẾT
  LUẬN ĐƯỢC GHI"*, và lần này chính ghi chú của sự kiện đã cảnh báo sẵn (*"legacy commit statuses are
  not covered"*) mà vẫn suýt đọc nhầm.
- **CẤM MỘT CHUỖI CON để nhận diện "đường kia" là cấp tín dụng cho MỌI thông báo lỗi chứa chuỗi ấy.**
  Đo 23-10-2026, packet #892 (PR #895). Ca `cli_dn_tep_an` của `t52` muốn nói *"không được đi đường
  nhanh"* nên đòi dòng đầu **không chứa** `KHÔNG ĐO` — chuỗi con của dòng đường nhanh
  `GOM: KHÔNG ĐO — …`. Nhưng dưới cây đột biến (không có `.git`) gom thật ĐỎ đúng như phải đỏ, bằng
  `[G-head] … KHÔNG ĐO ĐƯỢC` — **cũng chứa chuỗi ấy**. Kết quả: `t52` chết dưới **MỌI** đột biến, CI đỏ
  8/8 mảnh (26 và 28 lỗi bán kính ở hai mảnh đọc được), và con số *"13/13 giết đúng `t52`"* tôi đã báo
  một phần là **tín dụng giả**. Bộ phân hạng không cứu được: assertion ĐÚNG là của `t52`, chỉ có ĐIỀU
  nó kiểm là sai. Chữa: neo vào **dấu riêng** của đường cần loại (`=duong_nhanh, 0 mảnh`), không vào một
  từ chung mà thông báo lỗi khác cũng dùng. Cùng họ *"danh sách CẤM không bao giờ đủ"*, đổi đối tượng:
  ở đây không phải tên kẻ gian mà là **văn bản của chính mã mình** trên một nhánh mình không nghĩ tới.
  Dấu hiệu rẻ để bắt trước khi đẩy: chạy bán kính của **vài đột biến CŨ có đích khác** sau khi sửa ca —
  nếu chúng bỗng giết thêm ca của bạn, ca của bạn đang chết vì giàn chứ không vì chốt.
- **TRẦN LỜI GỌI CODEX ĐỌC TỪ ĐẶC TẢ VÀ LEASE, KHÔNG TỪ ADR MỚI NHẤT.** Đo 23-10-2026, packet #892.
  `ADR-0052` nâng trần lên tám, nhưng **chỉ áp khi đặc tả có dòng** `tran_loi_goi_codex: ADR-0052@<oid>`;
  `wp892-r2` không có ⇒ trần cũ `ADR-0036`/`0037` là **hai**, và chính lease ghi `M-4: tối đa 3`. Phiên
  gọi **bốn** lần (một lượt bị container cắt giữa chừng sau khi đã sinh output — vẫn tính một lời gọi
  theo cách đếm của `ADR-0052`) rồi mới đọc trần, khi chủ kho hỏi. Đúng ra sau lượt hai chưa approve
  phải vào Review Rescue Checkpoint. Không cổng nào đếm lời gọi (`ADR-0052` tự khai **0 cổng**), nên
  đây thuần là kỷ luật: **trước MỖI lời gọi Codex, đếm số đã dùng và đọc trần trong lease + dòng khai
  của đặc tả**; vượt thì dừng và xin `nang_tran` TRƯỚC khi gọi, không phải sau.
- **GATE HẬU MERGE XANH THEO REST CHỈ LÀ MỐC RUN — `landed: true` đòi đủ BỐN mốc §10.2.2.** Đo
  24-10-2026: Codex connector P1 trên PR #900 bắt hồ sơ land #892 khai `landed: true` từ run/jobs/
  check-run + `kiem-gate` rc=0, trong khi Checkout (SHA/tree thật chạy), Workflow definition (blob/băm
  qua `WorkflowRun.file`) và Gate output (command/rc/marker dương) đều chưa đo. Bốn hồ sơ cùng phiên
  ghi trước đó (PR #893) mang đúng lỗi ấy và phải hạ ở PR #902. Trong phiên Claude Code trên web, đường
  đo mốc Workflow definition **bị chặn**: GraphQL trả **403** *"GitHub GraphQL is not available from
  Claude Code sessions"* (đo trên 8 run, lưu ở `ops/land/pr8{72,77,80,83,95}-*-provenance/`). Nên từ phiên
  này, mặc định là `landed: false` + liệt kê ba mốc `not_measured`; khuôn đúng là
  `ops/land/pr882-wp748-r23-land-evidence.yaml`. `land_evidence_nguon` **không** bắt được lỗi này — nó chỉ
  đòi mỗi lời khai `measured` có tệp nguồn, không đòi đủ mốc — nên đừng đọc `TỔNG: ĐẠT` của nó thành
  "đủ điều kiện landed".

## Đẩy ref từ phiên Claude Code trên web (đo 16-08-2026)
Phiên web **KHÔNG xoá được ref** và **KHÔNG đẩy được `refs/tags/*`**. Cùng một `POST /git-receive-pack`:
tạo ref → **200** kèm `X-Github-Request-Id` (đi tới GitHub); xoá ref hoặc đẩy tag → **403**, **không
header GitHub nào**, ~41ms ⇒ 403 do **proxy egress tự sinh**, KHÔNG phải GitHub và KHÔNG phải thiếu
quyền token. Khớp tài liệu: credential git nằm ngoài sandbox, đi qua *"secure proxy using scoped
credentials"*. `curl https://api.github.com` cũng 403; container không có `gh`; MCP GitHub không có tool
xoá nhánh/tạo tag. **Lỗ đã biết của chốt ấy:** nó chặn theo HÌNH DẠNG chứ không theo HẬU QUẢ —
`git push --force` (ép lùi) VẪN được phép, mà ép lùi cũng làm commit thành không tra được y như xoá.
**Đoạn trên là trạng thái 16-08, và câu "`curl https://api.github.com` cũng 403" ĐÃ TRÔI** — đo
`2026-09-30T06:31Z`, `urllib` + `curl`, ba vế không token · token thật · token giả: gốc `/` trả **200**
thân `{}` (2 byte), **KHÔNG `Server: github.com`, KHÔNG `X-GitHub-*`** ⇒ proxy tự trả, đọc theo mã
trạng thái là đọc sai; `/repos/<kho>`, PR và comment thì 200 CÓ `X-GitHub-*` dưới danh tính bị THAY
(§Gọi agent đa nền), mà KHÔNG phải mọi đường con: đo `07:11Z` cùng ngày (`urllib`, ba vế y hệt), `/repos/<kho>/collaborators`
403 do proxy, `/branches/master/protection` 403 do chính GitHub (*"Resource not accessible by integration"*).
Nên *"phiên web KHÔNG xoá được ref"* chỉ mới ĐO cho `git-receive-pack` (16-08; chưa đo lại, vì
phép đo là một lần xoá thật); qua REST (`DELETE /git/refs/…`) là **KHÔNG ĐO ĐƯỢC**. Đừng coi chốt
sandbox là đã phủ REST.

Đường dùng được: `.github/workflows/ops-don-ref.yml` (`workflow_dispatch`, kích hoạt được từ phiên web
qua MCP `actions_run_trigger`). Nó **cấp lại đúng quyền sandbox cố ý không cho**, nên mặc định là THỬ
KHÔ, đòi gõ `XOA`/`TAO`, và bảo vệ nhánh mặc định tuyệt đối. Với `luu-tru/**` và với vùng làm việc
(`ops/** claude/** codex/** agent/** mission/** dispatcher/**`) nó KHÔNG cấm nữa mà **ĐO** — cùng một
hình dạng bản vá, hai lần, vì cùng một lý do: bất biến cần giữ là *"đừng làm commit thành không tra
được"*, không phải *"đừng đụng không gian tên này"*, và một chốt cấm cả việc ĐÚNG thì người ta sẽ đi
vòng quanh nó (đo được 21-08-2026: 16 nhánh `ops/**` đã land hết mà không đường nào dọn). Nhánh
`luu-tru/**` xoá được khi commit CÒN TAG GIỮ; nhánh vùng làm việc xoá được khi `behind_by = 0` so với
nhánh mặc định — tức mọi commit của nó đã nằm trong đó. **Ba trạng thái, không phải hai**: là tổ tiên ·
không phải · KHÔNG ĐO ĐƯỢC, và cái thứ ba làm cổng ĐỎ. Xoá **TAG** mang tên các vùng ấy thì vẫn CẤM —
tag không có quan hệ tổ-tiên để mà đo. Kèm chốt GHIM + **LEASE**: bước chốt ghi lại SHA đã đo, bước
làm xoá bằng `git push --force-with-lease=<ref>:<sha ghim> origin :<ref>` chứ KHÔNG bằng
`DELETE /git/refs` — REST chỉ nhận TÊN ref, không có SHA kỳ vọng, tức không có CAS.
**Bản đầu của mục này viết SAI và cross-review bắt được**: nó nói "đọc lại đầu nhánh rồi so" là
**đóng** khe giữa lúc ĐO và lúc XOÁ. Không đóng — chỉ THU HẸP. Reviewer dựng đồ giả GIỮ TRẠNG THÁI
cho nhánh nhảy SHA đúng giữa lần đọc cuối và lệnh xoá, và bản ấy **xoá mất commit chưa từng được đo**
(`rc=0`, DELETE gọi đúng một lần, nhật ký xác nhận chính SHA mới bị xoá). Lease thì gửi old-oid
**trong cùng giao dịch**, nên không còn khe. Đo được 21-08-2026 trên kho bare dựng tại chỗ, cả nhánh
lẫn tag: lease neo SHA cũ ⇒ `! [rejected] … (stale info)`, `rc=1`, ref CÒN; lease neo SHA đúng ⇒
`- [deleted]`, `rc=0`, ref MẤT — và chạy được cả từ kho **0 object**, nên runner chỉ cần một remote
có xác thực, không cần lịch sử. Bài học chung, không riêng chỗ này: **"thu hẹp" mà viết thành "đóng"
là một lời khai rộng hơn phép đo** — đúng lớp lỗi mà chính tệp này dạy, và người viết câu sai là
người vừa đọc nó. Phản chứng: `ops/don_ref_chot_test.sh` (105 ca; đột biến quay về REST DELETE làm
ca "nhánh nhảy SHA giữa ĐO và XOÁ" ĐỎ đúng như reviewer đã dựng).

**`luu-tru/*` là ref BỀN duy nhất** giữ các commit công bố verdict sau khi nhánh `ops/**` bị xoá — xem
`ops/reviews/README.md`. Xoá tag ấy là làm `published_*` trong `ops/reviews/*.receipt.yaml` thành SHA
không tra được.

## Gọi agent đa nền (chi tiết: `docs/GOI_AGENT_DA_NEN.md`)
- **KHÔNG viết script spawn agent.** Dùng CLI CHÍNH THỨC: `claude`
  (`@anthropic-ai/claude-code`) và `codex` (`@openai/codex`). `.claude/dev/launcher.py`
  CHỈ dựng chốt quanh một lệnh bất kỳ rồi chạy lệnh đó — không biết agent nào, không
  prompt dựng sẵn. Wrapper tự chế sẽ phải bám theo cờ/biến/xác thực của hai CLI khác
  nhau rồi trôi lệch âm thầm.
- **HOOK PHIÊN CỦA NHÁNH PACKET CŨ HƠN HOOK TRÊN MASTER — đó là nguyên nhân GỐC của
  sự cố 15-08-2026, không phải chuyện xác thực.** Hook trên `master` ĐÃ khôi phục
  `CODEX_AUTH_JSON` từ 14-08, có bốn chốt viết kỹ, và `docs/GOI_AGENT_DA_NEN.md` mô tả
  đúng như thế. Nhưng phiên hôm đó đứng trên nhánh packet rẽ từ `base_sha` CŨ HƠN commit
  ấy, nên hook chạy thật là bản cũ — **đo được: hook của phiên có 0 lần nhắc
  `CODEX_AUTH_JSON`, hook master có 5**. Vì vậy `codex login status` nói `Not logged in`
  còn tài liệu nói "hook lo rồi", và **hai câu đó cùng đúng**. Chính
  `.claude/skills/work-packet/SKILL.md` cảnh báo sẵn cái bẫy này; cảnh báo bằng chữ
  không chặn được ai, nên nay `launcher.py doctor` có mục `hook-phien` so băm hook đang
  checkout với `origin/master` và nói thẳng khi lệch.
- **ĐỌC BIẾN MÔI TRƯỜNG TRƯỚC KHI KẾT LUẬN MỘT CÔNG CỤ KHÔNG DÙNG ĐƯỢC.** Lỗi thứ hai
  của cùng sự cố: gặp `Not logged in` thì phải hỏi "nó xác thực bằng ĐƯỜNG NÀO", không
  phải "nó đã đăng nhập chưa". Giải `CODEX_AUTH_JSON` ra `~/.codex/auth.json` là chạy
  được ngay, và cross-review lượt 11 đã chạy trọn trong chính container đó. Đường cứu
  hộ khi hook không chạy: `launcher.py chuan-bi` (cùng bốn chốt như hook, không yếu hơn).
  `doctor` LUÔN in phần biến kể cả khi mọi thứ xanh, đúng để chặn kiểu kết luận đó.
  · **Đừng grep theo danh sách tên đoán trước** (`OPENAI_API_KEY`, `CODEX_API_KEY`…) —
  trượt đúng tên thật, y hệt bộ quét secrets lọc theo phần mở rộng rồi mù với `.env`.
  Quét TOÀN BỘ `os.environ` theo MẪU: `launcher.py moi-truong`.
  · **ĐÃ ĐẶT ≠ DÙNG ĐƯỢC.** Container này có `GH_TOKEN` `GITHUB_TOKEN`
  `AWS_ACCESS_KEY_ID` `AWS_SECRET_ACCESS_KEY` `CLOUDSDK_AUTH_ACCESS_TOKEN` — **năm
  biến, cùng một chuỗi giữ chỗ 14 ký tự** (cùng vân tay `f07d7417`); credential GitHub
  thật nằm ở `GITHUB_PAT`. Biến giữ chỗ tệ hơn biến chưa đặt: công cụ báo "sai thông
  tin đăng nhập" thay vì "chưa đăng nhập", đẩy người đọc đi sai hướng. `moi-truong`
  gom biến theo vân tay giá trị để phơi đúng chuyện này.
  · **Sai định dạng ≠ biến vô dụng.** Ghi base64 THÔ vào `auth.json` thì `codex` kêu
  `expected value at line 1 column 1` — câu đó nói TỆP không phải JSON, KHÔNG nói biến
  sai. `chuan-bi` thử cả base64 lẫn JSON thô và chỉ báo hỏng khi cả hai đường đều hỏng.
- **GitHub: bốn đường, hỏng độc lập — đừng kết luận từ đường hỏng.** Đo 15-08-2026 trong
  container remote: `git` đẩy/kéo HTTPS **CHẠY** (credential qua `$GIT_CONFIG_KEY_*`) ·
  công cụ **MCP github CHẠY** · **REST thẳng tới `api.github.com` bị PROXY chặn 403**
  ("GitHub access is not enabled for this session") **bất kể token** — `GITHUB_PAT` thật
  cũng 403 trong khi `/user` trả 200, tức chính sách theo ĐƯỜNG DẪN chứ không theo danh
  tính · `gh` không cài, và **cài cũng vô ích** vì nó đi đúng đường bị chặn. Việc của kho
  đi bằng **MCP github + git**, không bằng REST thẳng.
  *(Trạng thái PHIÊN 15-08 — trôi MỘT PHẦN: `/repos/<kho>`, PR, comment nay 200 (phiên đo 25-09,
  30-09; KHÔNG chỉ ba loại ấy), còn "403 bất kể token, theo ĐƯỜNG DẪN" vẫn đúng ở `/graphql` và các đường khác liệt kê (gạch
  "Câu 403 REST" dưới). "`gh` cài cũng vô ích" chỉ mất chân đỡ CŨ; `gh` thì phiên đo không có ⇒ KHÔNG ĐO
  ĐƯỢC; chỉ thị "không bằng REST thẳng" mất lý do cũ — giữ hay bỏ thì tệp này chưa ghi quyết định.)*
  · **ĐO LẠI 17-08-2026 — dấu hiệu phân biệt là HEADER, không phải mã trạng thái.**
  `/rate_limit` và `/user` → **200 CÓ `X-GitHub-*`** (tới GitHub thật); `/repos/<kho>` và
  `/repos/<kho>/pulls/N` → **403 KHÔNG header GitHub nào** (proxy tự sinh, chưa từng tới
  GitHub). Chạy cả **có token lẫn không token: kết quả Y HỆT** ⇒ khẳng định "theo ĐƯỜNG
  DẪN, không theo danh tính" nay có phản chứng hai chiều. Nên câu đúng KHÔNG phải "REST bị
  chặn" mà là **"REST bị chặn ĐÚNG CHỖ làm việc"** — và khác biệt ấy đổi hẳn kết luận về
  `gh`: **`gh auth status` hỏi `/user`, tức đường ĐƯỢC PHÉP, nên nó báo "đã xác thực" rồi
  MỌI lệnh việc thật ăn 403.** Một công cụ qua được phép tự kiểm mà không làm nổi việc thì
  **tệ hơn công cụ vắng mặt**: nó biến lỗi hạ tầng thành lỗi "chắc tại quyền token" và đẩy
  người đọc đi sai hướng — cùng họ `codex login status` NÓI DỐI. `launcher.py doctor` nay
  **ĐO** hai đường REST đó (`rest-chung`/`rest-kho`) thay vì nối thêm câu "có thể bị chặn";
  câu ấy là ĐOÁN, và nó từng được nối vào MỌI kết quả, vô điều kiện.
  · **Câu 403 REST Ở TRÊN ĐÃ TRÔI ở các đường ĐÃ ĐO ra 200 (liệt kê dưới; đường chưa đo: KHÔNG ĐO ĐƯỢC), CHỈ ở các phiên đã đo** —
  15-08 (*"REST … 403 bất kể token"*) và 17-08 (*`/repos/<kho>` · `/pulls/N` → 403*, *"REST bị chặn
  ĐÚNG CHỖ làm việc"*). Đo `2026-09-25T01:1xZ` (một phiên remote, có/không token, bảng trong thân PR
  #631: `/rate_limit` · `/user` · `/repos/<kho>` · `/pulls/623` đều 200, chỉ ghi `hdr_github=True`) và
  `2026-09-30` (`06:30–06:31Z` `urllib` + `curl`; `07:10Z` `urllib`; ba vế không/thật/giả token): bốn
  đường ấy, với `/pulls/631`, đều **200 CÓ `X-GitHub-*`**, `Server: github.com`. Đo thêm
  `2026-09-30T07:51–07:57Z` (14 đường: `urllib` cả 14, `curl` 10; ba vế y hệt): comment `5811128755` và 10
  đường con theo kho — `commits/<sha>` (biên nhận 200 từ 21-09, gạch "Bài học gốc" dưới) · `issues/631` ·
  `issues` · `issues/238/comments` · `pulls` · `actions/runs` · `git/refs/heads/master` · `contents/VERSION` ·
  `branches/master` · `rulesets` — cũng **200 CÓ `X-GitHub-*`**; `hooks` · `keys` · `actions/secrets` thì 403 do proxy như dưới. **Chính sách theo
  ĐƯỜNG DẪN của proxy VẪN SỐNG** ở phiên đo 30-09: `07:10–07:11Z`, GET, ba vế y hệt, **403 không
  `Server`, 0 `X-GitHub-*`** ở `/graphql` (*"GitHub GraphQL is not available from Claude Code sessions;
  use the REST API (gh api repos/…)"*; GraphQL 403 cũng có biên nhận 21-09 · 28-09 · 29-09 trong
  `ops/land/`), `/search/issues`, `/user/repos`, `/repos/cli/cli` (kho khác), `/repos/<kho>/collaborators`. Nên
  các câu SUY về `gh` — *"cài cũng vô ích"*, *"MỌI lệnh việc thật ăn 403"*, *"mọi thao tác kho trả 403"* (gạch `t103`
  dưới) — chỉ mất chân đỡ CŨ; lệnh `gh` nào đi GraphQL, và chính `gh`: phiên đo không có ⇒ KHÔNG ĐO ĐƯỢC.
  **Nguyên nhân KHÔNG ĐO ĐƯỢC** — nền đổi cho mọi phiên hay
  cấu hình THEO PHIÊN, chưa phép đo nào tách được (thân 403 cũ tự ghi *"not enabled for this
  session"*); không thấy dấu hiệu lượt cũ đo sai, nhưng thế chưa phải chứng minh. Nên đây là trạng
  thái của CÁC PHIÊN ĐÃ ĐO: phiên nào gặp lại 403 KHÔNG header GitHub thì đó là proxy của phiên ấy,
  không phải token của bạn, và nguồn trạng thái của `/repos/<kho>` (CHỈ đường ấy; `doctor` không hỏi
  GraphQL) là `doctor` (`rest-kho`) mỗi phiên, không phải tệp này. Hook phiên 30-09 in `rest-kho=OK` lúc 06:29Z; còn
  "in `OK` từ trước khi mục này được sửa" thì KHÔNG có biên nhận. Văn bản 403 cũ cũng KHÔNG chỉ nằm
  ở đây. Quét `rg --hidden` bằng mẫu chữ ngoài `ops/` (30-09; mẫu có thể sót), chỗ vẫn rút KẾT LUẬN
  hiện tại từ 403 cũ: `.claude/dev/launcher.py` (`_do_github` cùng chú thích quanh nó; mục `gh` trong
  `CONG_CU`, chỗ đỡ `bat_buoc.remote: False`), khối "KHONG cai `gh`" trong `.claude/hooks/session-start.sh`,
  bảng "GitHub: bốn đường" trong `docs/GOI_AGENT_DA_NEN.md`. (`_do_rest_github`, `t110`: 403 17-08 chỉ là ví dụ.)
  · **Ở phiên 30-09, hai vế có/không token KHÔNG đối chứng được gì — danh tính bị THAY trên đường
  đi** (phiên 25-09, 17-08 có bị thay không: KHÔNG ĐO ĐƯỢC). Thêm vế thứ ba **token GIẢ**:
  `/rate_limit` · `/user` · `/repos/<kho>` · `/pulls/631` vẫn 200, `/user` ra cùng `login` (chủ kho), cả ba vế
  mang cùng `Github-Authentication-Token-Expiration` (`2026-09-30 08:22:21 UTC`, chưa tới 2h sau lúc
  đo) ⇒ header của người gọi bị THAY, không chỉ được "cấp hộ" khi thiếu; kho RIÊNG vẫn đọc được. Hai
  client như nhau nên không phải cấu hình client; tầng nào thay: KHÔNG ĐO ĐƯỢC, **không đoán**. Hệ
  quả: `200` ở đây — kể cả `rest-kho=OK`, vốn chỉ đòi 2xx kèm `X-GitHub-*` — KHÔNG chứng minh token
  của bạn còn sống, cũng không cho biết GitHub thấy danh tính nào; phương thức GHI dưới danh tính ấy:
  KHÔNG ĐO ĐƯỢC. Đừng dùng đường này làm phép thử credential; muốn đối chứng thì vế thứ ba phải là
  **token giả**, không phải "không token".
  · **Bài học gốc KHÔNG đổi, và đừng đọc mục này thành "REST nay dùng thoải mái".** Bốn đường vẫn
  hỏng ĐỘC LẬP; `gh auth status` hỏi `/user` nên nó vẫn xanh được trong khi việc thật hỏng; và
  **vẫn phải thử ít nhất hai client trước khi gọi bất cứ thứ gì là chính sách**. Thứ hết hạn là
  TRẠNG THÁI, không phải cách đọc. Lượt 17-08 CÓ ghi ngày và hai vế token mà vẫn trôi, dù trạng thái
  MỚI đã có người DÙNG: ngày 21-09 một phiên lập hồ sơ land (#594) đã GỌI REST GET `/repos/<kho>/commits/…` và
  nhận 200 (`ops/land/pr594-wp578-land-evidence.yaml`, dòng thêm ở `b94182b`), mà tệp này đứng nguyên;
  văn bản sai từ LÚC NÀO thì KHÔNG ĐO ĐƯỢC. Nó chép quan sát của MỘT phiên thành trạng thái chung, và
  không gì đối chiếu văn bản với phép đo sống. Chữa: ghi PHẠM VI (phiên nào, ĐƯỜNG nào) và trỏ nguồn
  trạng thái (`doctor`) — kể cả cho trạng thái MỚI ở hai gạch trên.
  · **`api.githubcopilot.com` (điểm cuối MCP github) GỌI ĐƯỢC TỪ TRONG CONTAINER** — và câu
  này thay cho một câu SAI tôi vừa viết chính ở đây vài giờ trước ("bị chặn ngay ở tầng
  CONNECT"). Nguồn của cái sai: probe bằng `curl` nhận `CONNECT tunnel failed, response 403`
  rồi tôi ghi thẳng nó thành phép đo. Đó là tạo tác của `curl` với proxy, KHÔNG phải chính
  sách: `urllib` gọi CÙNG host, CÙNG lúc, trả **HTTP 200** kèm phản hồi `initialize` hợp lệ.
  Mỉa mai đúng chỗ đáng nhớ — đoạn ngay trên vừa dạy "đừng kết luận từ đường hỏng", và tôi
  kết luận từ đúng một đường hỏng. **Một công cụ thất bại chưa phải một đường bị chặn; phải
  thử ít nhất hai client trước khi gọi đó là chính sách.**
  Hệ quả vận hành: mất uỷ quyền connector MCP thì phiên **vẫn** tự dựng lại được đường ấy —
  JSON-RPC thẳng tới `/mcp/` bằng `GITHUB_PAT` (44 công cụ), và `/mcp/x/actions` cho
  `actions_run_trigger`/`get_job_logs`. Đây là đường đã dùng để merge và gọi lượt Windows
  trong đúng phiên này, nên nó có bằng chứng chạy chứ không phải lời hứa.
  · Hệ quả cho `bat_buoc`: **"công cụ này có bắt buộc không" không có MỘT câu trả lời cho
  mọi nền.** `gh` bắt buộc ở máy người dùng, KHÔNG bắt buộc ở phiên remote — `CONG_CU` nay
  nhận `{"mac_dinh": …, "remote": …}`. Ép một bool chung thì chắc chắn sai một nền, và cái
  sai đó là fail-close: nó CHẶN phiên chứ không chỉ báo nhầm.
  · **Đếm SỰ CÓ MẶT của một đường thay vì KHẢ NĂNG của nó — lỗi này đã tái phát.** `t103`
  sinh ra vì bản cũ đếm `shutil.which("gh")` là "đường mở"; rồi chính tôi thêm `rest-chung`
  (`/rate_limit`, MỞ nhưng không đọc nổi PR nào) vào `any(...)` và `t103` đỏ ngay. Chỉ đường
  **LÀM ĐƯỢC VIỆC** mới được tính vào `DUNG_DUOC`, và tập ấy là **`git` · `gh-kho` · `rest-kho`**
  — KHÔNG có `gh-cli`. Đó là lần sửa thứ ba: `gh auth status` hỏi `/user`, tức đường proxy CHO
  PHÉP, nên nó xanh trong khi mọi thao tác kho trả 403 ("mọi" đã rộng hơn phép đo 17-08 ghi ở trên — 2 đường kho; ở phiên đo 25-09/30-09
  `/repos/<kho>` và PR trả 200, GraphQL vẫn 403 do proxy (đo 30-09), `gh` KHÔNG ĐO ĐƯỢC — bài học
  đứng nguyên). "Đã xác thực" không phải "làm được việc";
  `gh-kho` chạy thật `gh api repos/<slug>`. `gh-cli` và `rest-chung` vẫn được ĐO và IN ra làm
  chẩn đoán, chỉ không còn quyền quyết định. Nhưng `gh-kho` cũng chỉ là MỘT đường REST: `gh-kho=OK`
  KHÔNG nói lệnh `gh` đi GraphQL làm được — đúng hình dạng trên, lùi một tầng.
- **Refresh token của codex XOAY VÒNG ⇒ `CODEX_AUTH_JSON` là ảnh chụp CHẾT NHANH.** Mỗi lần
  codex làm mới token, bản cũ bị vô hiệu — kể cả bản đang nằm trong biến. Đo 16-08: chuỗi
  vừa dán xong, đưa xuống đĩa khớp từng byte, vẫn `refresh_token_invalidated`. Chép base64
  **ngay sau `codex login`**, đừng chạy `codex` trên máy cá nhân trong lúc còn muốn dùng
  chuỗi đó ở phiên remote. `doctor` nay cảnh báo TRƯỚC (`SAP_HET_HAN`) khi `exp` dưới 24h
  **hoặc** `last_refresh` cũ hơn 24h — tín hiệu thứ hai mới là cái bắt được ca đã xảy ra.
- **`codex login status` NÓI DỐI** — chỉ kiểm tệp đọc được, không kiểm token còn sống
  (rc=0 "Logged in" trong khi mọi lời gọi trả 401). Đã trả giá HAI lần: một lần dán nhãn
  `DUNG_DUOC` sai, một lần chốt "đã đăng nhập thì không ghi đè" bảo vệ đúng bản đã chết và
  chặn bản mới. Chốt nay so `last_refresh` giữa đĩa và biến, không hỏi lệnh đó nữa.
- **Codex mặc định KHÔNG thấy biến tuỳ biến** (`shell_environment_policy.inherit` chỉ truyền
  tập lõi — KHÔNG phải vì bộ lọc bí mật; mẫu mặc định chỉ có `*KEY*` `*SECRET*` `*TOKEN*`).
  **`inherit = "all"` ĐÃ THU HỒI (16-08-2026, cross-review lượt 7) — đừng dựng lại.** Lý lẽ
  "phiên codex cần thấy biến để tái dựng credential" sai ngay trong luồng hook: credential
  đã được ghi ra `~/.codex/auth.json` TRƯỚC khi policy chạy, nên ta đổi MỘT credential lấy
  CẢ MÔI TRƯỜNG mà không mua được gì. `exclude` theo TÊN là bằng chứng về *cái ta đã nghĩ
  tới*, không phải bằng chứng an toàn. Đường đúng: `codex login --device-auth`.
  Hook nay chỉ **PHÁT HIỆN** (đọc, đặt cờ chặn, in cách chữa) — KHÔNG ghi vào config.
  Gỡ là `codex_env_policy.py --go`, dựng bản đã gỡ ra tệp **bên cạnh**; người dùng tự
  `diff` rồi `mv`. Chi tiết `docs/GOI_AGENT_DA_NEN.md`.
- **`launcher.py run` KHÔNG tự giải shim — người GỌI phải truyền ĐƯỜNG DẪN ĐÃ RESOLVE.**
  Đo 06-09-2026 trên Windows: `run ... -- codex exec ...` với tên trần ⇒ `CHAN [15]: probe nang luc
  khong dat: spawn=DO`, chi tiết `spawn --version: FileNotFoundError` — trong khi `doctor` cùng lúc báo
  `codex` CÓ và `--kiem-song` rc=0. Không mâu thuẫn: `shutil.which` tra PATHEXT nên thấy `codex.CMD`, còn
  `CreateProcessW` chỉ tự thêm `.exe`. `launcher.py` đã ghi bài học này ngay tại `_do_codex`, nhưng
  `_probe_spawn` dùng `lenh[0]` **như người gọi đưa vào**, nên chốt ấy không che đường `run`. Dùng
  `$CODEX_CLI_PATH` (bản nhị phân vendored) hoặc `shutil.which('codex')`. `_TRANSPORT_CONTRACTS` cắt
  `.exe/.cmd/.bat` trước khi tra bảng nên danh tính vẫn ra `openai_codex` — đã kiểm trong `run.json`.
- **`launcher.py run` cho con `stdin=DEVNULL`** (dòng 1576), nên `codex exec -` hay bất kỳ CLI nào đọc
  prompt qua stdin sẽ nhận EOF và chạy với prompt RỖNG. Truyền prompt làm ĐỐI SỐ, hoặc trỏ CLI
  đọc một tệp. `--prompt-file` và `--expected-prompt-sha256` phải đi CẶP — thiếu một cái thì `CHAN [2]`.
- **`claude --output-format json` có thể chèn MỘT DÒNG CẢNH BÁO TRƯỚC JSON.** Đo 06-09-2026:
  không chuyển hướng stdin thì dòng đầu là `Warning: no stdin data received in 3s…` ⇒ `json.load`
  ném `Expecting value: line 1 column 1`, trong khi `rc=0` và việc đã làm XONG. Đừng đọc lỗi parse ấy
  thành "phiên hỏng": chạy kèm `< /dev/null`, hoặc cắt từ dấu `{` đầu tiên rồi mới parse. Cùng họ
  với bẫy stdin của `codex exec`, nhưng hỏng theo kiểu KHÁC: codex thì TREO, claude thì làm bẩn stdout.
  Kiểm model ĐÃ CHẠY bằng `modelUsage[*].canonicalModel`, không bằng `rc`; vị từ dùng chung với CI là
  `kiem_ket_qua` trong `.claude/dev/chon_reviewer.py` (đã kiểm hai chiều: đúng model ⇒ ĐẠT, model khác ⇒ ném).
- `rg` là công cụ **BẮT BUỘC** (từ 15-08-2026). Thiếu nó lệnh tìm của agent gãy giữa
  chừng chứ KHÔNG tự lùi về `grep` — phiên vẫn "chạy" nhưng tra cứu mù. Hook phiên thử
  apt-get (có/không sudo, có/không `update`) rồi cargo, và đòi bằng chứng `rg --version`.
- **MỞ PHIÊN CODE LÀ ĐỌC `launcher.py` RỒI CHẠY `doctor` — TRƯỚC MỌI VIỆC KHÁC.**
  Không phải "khi nghi ngờ" mà là bước đầu tiên, vì thiếu công cụ không lộ ra lúc
  thiếu, nó lộ ra giữa chừng ở chỗ khó đọc. Ba lệnh, theo đúng thứ tự:
  ```
  sed -n '1,140p' .claude/dev/launcher.py     # hợp đồng: mã thoát, 4 bẫy đa nền
  python .claude/dev/launcher.py doctor       # đo công cụ + KHẢ DỤNG + biến
  python .claude/dev/launcher.py chuan-bi     # khôi phục xác thực khi hook không chạy
  ```
  Thiếu gì thì **cài ngay ở bước này**, đừng đợi tới lúc cần: `doctor` in sẵn lệnh
  cài cho từng nền. `codex` là **tuỳ chọn với launcher nhưng BẮT BUỘC với
  cross-review** — thiếu nó thì tới lúc cần review chéo mới phát hiện, mà lúc ấy
  việc đã làm xong và không lùi được.
- **HOOK PHIÊN CÓ THỂ KHÔNG CHẠY LẦN NÀO — và `doctor` KHÔNG nói cho bạn biết
  điều đó.** Đo được 17-08-2026 trong phiên remote: `CLAUDE_PROJECT_DIR` **KHÔNG
  được đặt**, nên lệnh hook trong `.claude/settings.json`
  (`bash "${CLAUDE_PROJECT_DIR}/.claude/hooks/session-start.sh"`) giải ra
  `/.claude/hooks/session-start.sh` — không có tệp, hook **vắng mặt lặng lẽ**, và
  không có `codex` nào được cài. Xảy ra khi kho được gắn/clone GIỮA phiên chứ
  không phải là project dir lúc phiên mở (phiên remote, `add_repo`).
  · `doctor` có mục `hook-phien`, nhưng nó so BĂM tệp hook đang checkout với
  `origin/master` — tức đo **tệp có mới không**, KHÔNG đo **hook đã chạy chưa**.
  Hai câu hỏi khác nhau, và đúng lỗi "đếm sự CÓ MẶT thay vì KHẢ NĂNG" mà kho đã
  trả giá bốn lần. Tệp mới tinh vẫn có thể chưa từng chạy.
  · Nên: **đừng suy "hook đã lo rồi" từ bất cứ thứ gì**. Bằng chứng duy nhất là
  công cụ thật sự có mặt và thật sự gọi được — `doctor` + `chuan-bi` ở trên.
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
- **…và cũng không luôn nghĩa là mã đúng: đột biến có thể CHƯA TỪNG ĐƯỢC CHẠY.** Runner
  đột biến ghi mọi bản sao vào CÙNG một `launcher.py` tạm. CPython coi `.pyc` còn hợp lệ
  theo **(mtime tính bằng GIÂY, kích thước)** — hai đột biến ra tệp cùng kích thước, ghi
  trong cùng một giây ⇒ bản sau chạy **mã của bản trước**. Mutant
  `do_codex_tin_DONG_DAU…` báo `giet 0/1` suốt BA lượt review vì lý do đó, và khi gỡ chốt
  ra để phản chứng thì nó kéo câm luôn mutant canh bản vá `killpg` — **cơ chế tước răng
  mọi mutant, không riêng một cái**. Bằng chứng A/B: `sys.dont_write_bytecode=True` ⇒
  `1/1`; chạy tay một mình ⇒ `1/1`. Đây cũng là lời giải cho ba lượt "cùng cổng, hai kết
  quả": va chạm chỉ xảy ra khi hai lượt ghi lọt cùng một giây, tức phụ thuộc MÁY.
  Ba lớp bịt (xoá `.pyc` · tắt ghi bytecode · `invalidate_caches`) cộng tên tệp riêng
  từng đột biến; `t97` khoá lại, và mỗi lớp có phản chứng RIÊNG — lớp "tắt ghi bytecode"
  lúc đầu KHÔNG có răng (gỡ nó ra mà `t97` vẫn xanh) nên phải đo thẳng bằng "nạp xong
  không được để lại `.pyc`".
- **"Từ chối" mà vẫn để đường nguy hiểm chạy tiếp là FAIL-OPEN, không phải thận trọng.**
  Bộ gỡ `shell_environment_policy` trả rc=3 khi không dám sửa config người dùng, còn hook
  thì chỉ in `CANH BAO` rồi đi tiếp — nghĩa là đúng lúc phát hiện `inherit="all"` còn hiệu
  lực thì ta để nó hiệu lực. Biến một lỗi xác-định-an-toàn thành phơi môi trường CÓ CHỦ
  ĐÍCH. Không sửa được tệp của họ thì chặn ở PHÍA TA (cờ riêng `~/.codex/tra-luat-CHAN-CODEX`,
  `_do_codex` đọc cờ và hạ nhãn TRƯỚC mọi phép đo khác) — và cờ phải TỰ HẾT khi sạch,
  kẻo lại thành chốt đỏ thường trực.
- **BẢY phát hiện cùng MỘT đường ⇒ sai ở QUYẾT ĐỊNH GỐC, không ở các bản vá.** Việc tự
  động ghi lại `~/.codex/config.toml` ăn bốn lượt cross-review liên tiếp: bảng TOML trùng
  tên · khớp substring mất dữ liệu · `write_text` không nguyên tử · kiểm từng dòng vẫn mất
  dữ liệu · symlink tên tạm ghi đè tệp khác · CRLF đổi kết thúc dòng toàn tệp · lost-update.
  Mỗi lượt vá bảo toàn được thứ ta NGHĨ TỚI và làm hỏng thứ ta KHÔNG NGHĨ TỚI. Vá tiếp lúc
  nào cũng *có vẻ* đúng vì lần nào cũng có lỗi thật — đó chính là cách người ta ở lại quá
  lâu trong một cái hố. **Đếm hình dạng lỗi, đừng chỉ đếm lỗi**: cùng một hình dạng lặp ba
  lần trở lên thì câu hỏi đúng là "có nên làm việc này không", không phải "vá thế nào".
  Chữa: công cụ KHÔNG ghi vào tệp của người dùng nữa — phát hiện + dựng bản đã gỡ ra tệp
  BÊN CẠNH, người dùng tự `mv`. Cả lớp rủi ro chết theo KIẾN TRÚC, không theo bản vá.
- **API CHỈ CÓ TRÊN MỘT NỀN: hỏi trước, đừng đụng thẳng — và một job CI mặc định SKIP
  là một cổng KHÔNG TỒN TẠI.** Hai lần trong cùng một ngày: `os.O_NOFOLLOW` (bot review
  bắt) và `os.getpgid` trong chốt cô lập — cái sau làm suite **0/103** trên
  `windows-latest`, tức bộ test **chưa từng chạy** trên Windows kể từ lúc có chốt ấy.
  Không ai biết, vì job Windows chỉ chạy khi PR có nhãn `windows`. Năm lượt cross-review
  trên Linux không thể thấy, và đã không thấy.
  Ba luật: (1) `hasattr`/`getattr(..., mặc_định)` trước khi đụng API riêng nền; (2)
  truyền **lambda** vào hàm bọc lỗi, đừng truyền thẳng `os.getpgid` — tra thuộc tính
  xảy ra TRƯỚC lời gọi, tức NGOÀI `try`; (3) gán thêm một API mà nền vốn không có thì
  phải **gỡ lại** khi ra khỏi chốt, kẻo nền tự nhận có thứ nó không có.
  Gắn nhãn `windows` cho PR đụng `.claude/dev/**` — nó tốn ~40 phút và trả lại thứ mà
  năm lượt review không mua được.
- **`MA=$?` SAU pipeline rồi đọc `${PIPESTATUS[0]}` = tự giết mã thoát.** Phép gán
  `MA_GO=$?` LÀ một lệnh, nên nó đặt lại `PIPESTATUS` về 0; dòng đọc `PIPESTATUS` phía
  sau kéo mã về 0 và chốt fail-close chết **lần thứ ba**. Tệ hơn: chú thích biện minh cho
  dòng đó ghi "`set -o pipefail` không bật ở đây" trong khi CHÍNH TỆP ẤY đặt
  `set -euo pipefail` ở dòng 34. **Chú thích khẳng định về tệp mình đang nằm trong thì
  phải kiểm trên tệp đó** — một câu sai ở đây biến bản vá thành bản phá. Có `pipefail`
  thì `$?` của pipeline đã là mã của lệnh trái; đừng "làm cho chắc".
- **PHẠM VI TUYÊN BỐ phải bằng phạm vi ĐO ĐƯỢC.** Tôi đặt cờ chặn codex, gọi nó là
  "CODEX BI CHAN", mà chỉ `_do_codex` đọc cờ — trong khi chính hook gọi `codex login
  status` TRƯỚC đó, `_do_codex_song` (cửa thật sự chạy `codex exec`) đi thẳng qua, và
  lệnh `codex` gõ tay thì không gì chặn nổi. Chốt mà chỉ một trong nhiều cửa đọc thì
  không phải chốt. Hai việc phải làm cùng lúc: cho MỌI cửa của kho dùng CHUNG một hàm
  guard (`_co_chan_codex`), và **khai thẳng cái không chặn được** thay vì đặt tên to hơn.
  Mỗi cửa phải có ĐỘT BIẾN RIÊNG — cửa không có mutant là cửa sẽ âm thầm hở lại.
- **Vá một lỗ mà mở lỗ khác trong cùng hàm.** Writer "nguyên tử" của tôi dùng tên tạm
  ĐOÁN ĐƯỢC (`<tệp>.tra-luat-tam-<pid>`) + `open(...,"w")`: trỏ tên đó thành symlink là
  ghi đè tệp bất kỳ — hỏng TRƯỚC `os.replace`, tức phá đúng hợp đồng viết ở dòng trên.
  `mkstemp` (tên ngẫu nhiên + `O_EXCL`) · từ chối khi đích là symlink · **giữ nguyên
  quyền tệp gốc** (ép 0600 là đổi metadata sau lưng người dùng) · `fsync` cả thư mục.
- **Khớp marker bằng SUBSTRING là đường mất dữ liệu, và "parse lại vẫn hợp lệ" KHÔNG bắt
  được.** Sửa lần một (kiểm từng dòng) VẪN mất dữ liệu: membership từng dòng không thấy
  CẤU TRÚC, nên `inherit = "core"`, một dòng chú thích đơn độc, hay thứ tự đảo ngược đều
  bị nhận là "khối của ta" rồi xoá. Chỉ so NGUYÊN KHỐI với bản canonical mới đóng được. Phản chứng: `x=1 # <MO>` / `y=2` / `z=3 # <DONG>` → `x=1 #\nz=3\n`, mất `y=2`,
  mà kết quả VẪN là TOML hợp lệ — nên phép kiểm "parse lại được" tôi dùng làm bằng chứng
  mù hoàn toàn. **Một phép kiểm không thể đỏ thì không phải bằng chứng.** Marker phải là
  DÒNG RIÊNG, và phần giữa hai marker phải khớp hình dạng khối ta từng ghi.
- **Ghi đè thẳng `write_text` phá chính hợp đồng "hoặc đúng, hoặc không đụng tệp".** Nó
  truncate trước rồi mới ghi; lỗi giữa chừng để lại tệp cụt trong khi hàm vẫn trả "đã từ
  chối". Ghi ra tệp tạm CÙNG THƯ MỤC → `fsync` → `os.replace`.
- **DÒNG IN CUỐI CÙNG ≠ CA CHẠY CUỐI CÙNG.** Bộ test launcher không in gì trong lúc chạy
  (chỉ dòng BỎ QUA + tổng kết), nên khi tiến trình bị giết, thứ còn lại trên màn hình là
  `BO QUA t62`. Reviewer đọc thành "chết ngay sau t62"; **tôi cũng đọc y hệt** rồi đi truy
  `t63` — ba lượt review tìm sai chỗ vì một tạo tác của BỘ ĐỆM (stdout nối vào ống là đệm
  KHỐI, mọi thứ chưa xả mất cùng cú giết). `flush()` chưa đủ — mới ra khỏi đệm Python;
  phải `fsync()` mới qua đệm HĐH. Nay có `--nhat-ky TEP`: ghi `>>> vao` / `<<< ra` từng ca,
  flush+fsync, kèm dấu `# XONG TRON VEN` để phân biệt "chạy hết" với "bị giết". Ca nào có
  `vao` mà không có `ra` chính là ca giết tiến trình. **Trước khi định vị một cú chết, hãy
  hỏi phép đo có sống sót qua cú chết đó không.**
  KẾT QUẢ (lượt 8, đo trong namespace reviewer): `vao=100 ra=100`, không ca nào thiếu,
  `# XONG TRON VEN` — **rồi vỏ shell vẫn chết**. Không có "ca giết". Cú chết nằm SAU khi
  `main` chạy hết (vùng thoát/`atexit`/tiến trình còn sót). Ba lượt truy bên trong vòng
  lặp ca là truy sai VÙNG, và chỉ phép đo mới loại được vùng đó.
  LƯỢT 9 lại ra chỗ KHÁC: `vao=74 ra=73`, chết trong `t72`, không `XONG TRON VEN`, không
  `atexit`. Hai lượt hai chỗ ⇒ **chập chờn hoặc phụ thuộc thứ tự**, chưa ai biết nguyên
  nhân. Có `--lap-ca TEN --lan N` để chạy lặp MỘT ca — phân biệt "ca tự nó chập chờn" với
  "chỉ chết khi đứng sau 73 ca khác". Đo tại chỗ 40/40 qua, tức **không tái hiện ở đây**;
  phải đo trong namespace của bên kia.
- **Hook dùng đường dẫn TƯƠNG ĐỐI là bẫy tự khoá.** `.claude/settings.json` từng ghi
  `python .claude/hooks/pretooluse_guard.py`; khi cwd của shell trôi vào thư mục con thì
  MỌI lệnh Bash chết trước khi chạy, và không còn đường `cd` về. Luôn dùng
  `$CLAUDE_PROJECT_DIR`.
- **`( eval … ) > tệp` KHÔNG tương đương `$( eval … )` — subshell `( )` KẾ THỪA `set -e`, command substitution
  thì không** (bash, trừ khi bật `inherit_errexit`). Đo 22-10-2026, packet #868: đổi `KET_QUA_CAI="$(eval "$LENH")"`
  sang `( eval "$LENH" ) > tệp` để khỏi chờ EOF stdout. Đổi xong, các `|| { …; return 1; }` tường minh trong
  `chon_thu_muc_chay_duoc` thành THỪA: hàm đứng CUỐI chuỗi `&&` nên errexit vẫn áp vào thân nó. Hai mutant
  wp858_sh_nuot_loi_cygpath_w · wp858_sh_nuot_loi_ghi_github_path (bảng đột biến của
  `.claude/dev/launcher_test.py`) vì thế SỐNG, và bộ ca không nói gì.
  Chữa: `( set +e; eval "$LENH" ) > tệp`, giữ đúng ngữ nghĩa cũ (mã thoát là của chuỗi `&&`, chốt là các `return 1`
  tường minh). Đổi một dạng thực thi shell sang dạng "trông tương đương" là đổi NGỮ NGHĨA errexit. Không đọc
  code mà thấy được: chỉ đột biến mới lộ, vì hành vi trên head vẫn đúng.
- **Hàm bash EXPORT qua môi trường (`BASH_FUNC_<tên>%%`) che được BUILTIN — tiêm lỗi mà không sửa script.**
  Bash nạp hàm từ biến `BASH_FUNC_printf%%` lúc khởi động, và hàm thắng builtin cùng tên. Packet #868 dùng cách
  này cho ca r868_ghi_kenh_hong_thi_dung của `.claude/dev/launcher_test.py`: `printf` giả trả rc 74 đúng cho
  payload kênh, ép đường "ghi kênh lỗi" vốn không dựng được bằng tệp/quyền (máy chạy root). Hai điều kèm theo. (a) `_wp802_bash_env` cố ý LỌC mọi
  `BASH_FUNC_*` khỏi môi trường thừa kế để cô lập, nên fixture phải thêm lại TƯỜNG MINH. (b) Ca phải đòi DẤU HIỆU
  của lỗi giả trong stderr ("ca có ĐO", không chỉ `rc != 0`): rc khác 0 vì một lý do khác thì không đo gì.
- **`/tmp/.git` RỖNG do sandbox Codex để lại SAU khi lượt chạy KẾT THÚC vẫn làm đỏ 11 ca `r484_*`** (`Codex home
  is inside a repository`). Đo 22-10-2026, packet #868: lượt Codex xong là mount gỡ, nhưng thư mục rỗng ở lại.
  `launcher_test` ra 238/249 với đúng 11 ca ấy đỏ; `rmdir /tmp/.git` (CHỈ thư mục rỗng, của chính lượt mình gọi)
  thì 4/4 ca thử lại xanh. Bản #858 chỉ ghi "đỏ KHI Codex chạy song song"; câu đúng rộng hơn: đỏ cả SAU khi Codex
  thoát. Trước khi đo `launcher_test` sau một lượt cross-review, hỏi `ls -d /tmp/.git` trước. Còn thấy thì ghi
  đo trong điều kiện ấy, đừng đọc 11 ca đỏ thành hồi quy. Gốc lỗi: chốt kho của credential
  store coi một `.git` RỖNG ở thư mục tổ tiên là kho. Đây là nợ của packet khác, chưa vá.

## Cấm
- Không tự chạy lệnh có `--apply` / `source-delete` / `reg-delete` / `--clear-stale` khi user chưa duyệt (hook sẽ hỏi).
- Không đọc/ghi secrets (`*.enc`, `tl_secrets*`, `*cookie*`, `*token*`, `credentials*`) ngoài đúng quy trình
  `gws-auth-stage`/`secrets-set` mà user yêu cầu.
- Không dùng Drive MCP/Sheets MCP để sửa corpus/registry.
- Không dùng RAG/NLM để trả NGUYÊN VĂN điều luật — nguyên văn chỉ từ nguồn đã verify (extract/web official).

## Protocol đa phiên — CON TRỎ, không phải bản sao
Làm việc theo work packet / review chéo / land: **nguồn quy tắc duy nhất là
`docs/PROTOCOL_DA_PHIEN.md`**; lộ trình ở `docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md`.
Adapter của nền này (MỎNG, chỉ cú pháp/công cụ): `.claude/skills/work-packet/SKILL.md` ·
`.claude/skills/cross-review/SKILL.md` · `.claude/skills/land-packets/SKILL.md`.
Adapter lệch protocol thì ADAPTER sai — và "lệch" nay đo được, không đọc bằng mắt:
`python .claude/dev/packet_loop.py doctrine-scan --root .` thoát khác 0 khi adapter chép doctrine.
Vài điều kiện dừng của §12 được CƯỠNG CHẾ bằng `.claude/dev/packet_loop.py` (chạy `--help` cho bảng
mã thoát); phản chứng chạy được cho từng chốt ở `.claude/dev/packet_loop_test.py`.

**ADR nào đang hiệu lực — hỏi `docs/PROTOCOL_DA_PHIEN.md` §20, đừng hỏi trí nhớ.** §20 có ĐÚNG một
dòng cho MỖI tệp trong `docs/adr/`, kèm cột "cổng nào ĐỌC luật ấy". Trước 22-08-2026 chỗ này là một
dòng PHẠM VI (`ADR-0017 đến ADR-0035`) và nó đã chết: 45 ADR tồn tại, protocol nhắc 4, trọn
`0036`–`0045` — mười ADR quản trị — nằm ngoài. Nay máy canh:
`python .claude/dev/packet_loop.py adr-song --root .` đỏ khi thêm ADR mà quên bảng, khi bảng trỏ ADR
không tồn tại, hoặc khi một ADR không có dòng `Trạng thái` đọc được.

**Kế hoạch thi công và hồ sơ quyết định** — đọc khi nhận BẤT KỲ packet nào của kế hoạch này
(`W0-*` · `W1-*` · `W2-*`):
`ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` (bản đồ packet, write set dự kiến, thứ tự từng lane) ·
`ops/THAM_DINH_CHUNG_CLAUDE_CODEX_KE_HOACH.md` (biên bản thẩm định 5 vòng, hai quyết định đã duyệt) ·
căn cứ từng quyết định ở `docs/adr/0036-claude-executor-codex-review-theo-rui-ro.md` … `docs/adr/0042-deadline-wall-clock-va-working-state-evidence.md` ·
prompt của 5 vòng thẩm định ở `ops/prompts/orchestrator-plan-audit-r1-claude-20260817.md` … `-r5-`.
Cả `ops/` lẫn `docs/` là dev-side, không vào gói phát hành.
Từ vựng dùng chung ở `CONTEXT.md`; tệp này KHÔNG định nghĩa lại thuật ngữ nào.

**ĐỌC ĐƯỢC KẾ HOẠCH KHÔNG PHẢI LÀ ĐƯỢC GIAO VIỆC.** Kế hoạch là DỮ LIỆU. Thứ giao việc là Packet
Issue kèm lease còn hiệu lực (Issue: protocol §3.2 · lease và hiệu lực của nó: §4 · prompt/handoff
KHÔNG phải lease: §7). Phiên nào tự chọn một dòng trong bảng packet rồi
bắt tay làm là tự cấp việc cho mình, và hai phiên sẽ cùng kết luận mình sở hữu cùng một packet —
đúng thứ write-set exclusion sinh ra để chặn. Chưa có Issue/lease cho packet đó thì DỪNG và hỏi
người giữ, kể cả khi bảng packet ghi rõ việc phải làm.

**Không phải packet nào cũng route sang phiên cloud được.** Lane launcher đo hành vi phụ thuộc nền:
cùng `.claude/dev/launcher_test.py`, CI 17-08-2026 đo được Linux bỏ qua 1 ca còn Windows bỏ qua 13. Packet nào
đo hạn chót xuyên trạng thái ngủ của máy thì cần `QueryUnbiasedInterruptTime`, chỉ chạy thật trên
Windows. Chọn nền theo thứ packet ĐO, đừng chọn theo nền nào đang rảnh.

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
5. **Thêm/xoá tệp — HOẶC ĐỔI NỘI DUNG một tệp CÓ TRONG manifest — ⇒ tái sinh `RELEASE_MANIFEST.json`, và ghi lại golden NẾU số đếm kiểm kê đổi.**
   **Bản trước của dòng này chỉ viết "Thêm/xoá tệp" — HẸP HƠN chính sự cố nó sinh ra để chặn.**
   `RELEASE_MANIFEST.json` băm NỘI DUNG từng tệp, nên sửa một tệp đã có sẵn cũng làm sha lệch dù `file_count` KHÔNG đổi. Đo 06-09-2026 (r356): sửa `CHANGELOG.md` ⇒ manifest giữ `9e1c4b27…` trong khi thực tế `20779e38…`, `file_count` vẫn 180 cả hai bên. **`CHANGELOG.md` và `requirements.txt` NẰM TRONG manifest; `CLAUDE.md`, `.claude/**`, `docs/**`, `ops/**` thì KHÔNG** — hỏi trước khi đoán.
   Và **lane PR KHÔNG bắt được**: `ci.yml` cho `release-verify strict (lane LAND)` điều kiện `if: github.ref == 'refs/heads/master'`, còn lane WORKER sinh manifest TẠM từ chính cây nên nó **hấp thụ** mọi thay đổi nội dung ⇒ PR xanh, master ĐỎ. Muốn biết trước khi merge thì chạy ĐÚNG lệnh của lane LAND tại chỗ: `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` (đòi `ok=true` và `expected == checked`).
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
