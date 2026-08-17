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
  · **(c) Gate PR và gate master KHÔNG phải một thứ.** `ci.yml` cố ý chỉ chạy `ubuntu` cho PR thường,
  còn master chạy CẢ `ubuntu` LẪN `windows` (Windows tốn gấp đôi phút, để dành cho lượt gác cổng phát
  hành). Nên **"PR xanh" không hàm ý "master xanh"**: với một PR THƯỜNG — không gắn nhãn `windows`,
  không ai gọi tay — lần merge chính là lần đo Windows ĐẦU TIÊN của mã đó. Nói CÓ ĐIỀU KIỆN vì ma
  trận cũng kèm `windows-latest` cho PR gắn nhãn `windows` và cho `workflow_dispatch`; bỏ điều kiện
  ấy là đánh lừa người đang xem đúng một PR như vậy (cross-review bắt được, P2 trên PR #109 — và
  trớ trêu là đoạn ngay trên đã trích đúng điều kiện đó rồi vẫn viết câu quên nó).
  **Muốn có Windows TRƯỚC khi merge thì đường CHẮC CHẮN là gọi tay `workflow_dispatch` trên ref đó.**
  Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai
  trên PR #109): `ci.yml` khai `pull_request:` mà KHÔNG khai `types:`, nên mặc định chỉ bắn ở
  `opened`/`synchronize`/`reopened` — **`labeled` không nằm trong đó**. Gắn nhãn không tự sinh lượt
  chạy nào; ma trận chỉ đọc nhãn ở lượt bắn KẾ TIẾP. Người làm theo sẽ gắn nhãn, thấy vẫn đúng một
  check Ubuntu, rồi merge mà tưởng đã có Windows. Muốn dùng nhãn thì phải kèm một cò mới sau khi gắn
  (đẩy thêm commit, hoặc đóng rồi mở lại PR) — hoặc khai `types: [..., labeled]` cho workflow.
  Đợt 14-08 không dùng đường nào, nên cả sáu lần merge của đợt đúng là sáu lần đo Windows đầu tiên.
  Kèm theo: trên lượt master, bước `PR head contains required EOL base` LUÔN `skipped` vì nó có
  `if: github.event_name == 'pull_request'` — nên tiêu chí "không bước nào `skipped`" chỉ đúng cho
  lượt PR; bê nguyên sang lượt master là tự báo động giả.
  Cả ba cùng họ với bài học "cổng không nói dối, nó VẮNG MẶT": **"vắng mặt vì sạch" và "vắng mặt vì
  chưa chạy" nhìn giống hệt nhau** nếu hỏi sai chỗ. Chốt chung, rẻ và luôn dùng được: trước khi kết
  luận từ một chỗ RỖNG, hỏi "nếu thứ tôi đang tìm CÓ THẬT thì nó sẽ được ghi ở đâu?" — rồi đi hỏi
  đúng chỗ đó. Máy không canh được mục này; nó là kỷ luật đọc.
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
  đúng lúc nó cần nhất. Đo nền trước khi thêm: `actionlint` trên cả 5 workflow của kho → rc=0.
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

## Đẩy ref từ phiên Claude Code trên web (đo 16-08-2026)
Phiên web **KHÔNG xoá được ref** và **KHÔNG đẩy được `refs/tags/*`**. Cùng một `POST /git-receive-pack`:
tạo ref → **200** kèm `X-Github-Request-Id` (đi tới GitHub); xoá ref hoặc đẩy tag → **403**, **không
header GitHub nào**, ~41ms ⇒ 403 do **proxy egress tự sinh**, KHÔNG phải GitHub và KHÔNG phải thiếu
quyền token. Khớp tài liệu: credential git nằm ngoài sandbox, đi qua *"secure proxy using scoped
credentials"*. `curl https://api.github.com` cũng 403; container không có `gh`; MCP GitHub không có tool
xoá nhánh/tạo tag. **Lỗ đã biết của chốt ấy:** nó chặn theo HÌNH DẠNG chứ không theo HẬU QUẢ —
`git push --force` (ép lùi) VẪN được phép, mà ép lùi cũng làm commit thành không tra được y như xoá.

Đường dùng được: `.github/workflows/ops-don-ref.yml` (`workflow_dispatch`, kích hoạt được từ phiên web
qua MCP `actions_run_trigger`). Nó **cấp lại đúng quyền sandbox cố ý không cho**, nên mặc định là THỬ
KHÔ, đòi gõ `XOA`/`TAO`, và bảo vệ `luu-tru/** ops/** claude/** codex/** agent/** mission/**
dispatcher/**` cùng nhánh mặc định. Phản chứng: `ops/don_ref_chot_test.sh`.

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
