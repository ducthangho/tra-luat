# VERDICT — cross-review PR #264 (hồ sơ `PLAT-X8` + `PLAT-X8b`), reviewer `claude`

verdict: `changes_requested`
reviewed_sha: `cc6657e826d90bebe61ea59983fa83c27db42c34` · base_sha: `05de1ab81c235235b971a6fb8d8ae1fb226295d5` (nhánh đã gộp master; `git diff` giữa hai SHA chỉ chứa nội dung PR)
lease: `handoff-264-review-1-claude-20260823` (role: reviewer, đã tự kiểm tồn tại trên `origin/ops/cap-lease-plat-x8-2` — bảng đo #1)
assurance mục tiêu của lease: `cross_approved` — assurance **thực sự đạt** của lượt này: xem "Assurance" bên dưới.

PR **thuần tài liệu** (15 tệp, `+1702/-0`, không dòng mã sản phẩm) nhưng lớp hiệu lực `sensitive` (đo bằng chính cổng `PLAT-X8`: 15/15 đường dẫn của PR đều rơi mặc định fail-closed, không nằm trong `_BANG_LOP`). Việc của lượt này là ĐO LỜI KHAI, không đo mã.

## Đối chiếu lượt trước

Đây là lượt review đầu tiên của `HANDOFF-264` (khác các packet `PLAT-X8`/`PLAT-X8b` mà PR này ghi hồ sơ) — không có lượt trước để đối chiếu.

## BẢNG ĐO — kể cả cái khớp

| # | khẳng định / lệnh | kết quả đo | khớp? |
|---|---|---|---|
| 1 | Thẩm quyền: `git ls-tree -r --name-only origin/ops/cap-lease-plat-x8-2 -- ops/leases/ \| grep handoff-264` | `ops/leases/handoff-264-review-1-claude-20260823.yaml` có mặt (sau `fetch`) | ✅ có, đủ điều kiện chạy |
| 2 | `sha256sum in-264/PROMPT.md` so `prompt_sha256_required` trong LEASE.yaml | `24144f05…7a7d482` cả hai | ✅ khớp |
| 3 | `git log -1` cây review | `cc6657e8…` — khớp `reviewed_sha_required` của LEASE.yaml | ✅ khớp |
| 4 | `git status --porcelain` cây review | rỗng | ✅ sạch |
| 5 | `git config core.abbrev` | `7` | ✅ đúng yêu cầu prompt |
| 6 | `python3 ops/lease_publish_test.py` trên cây review | `87/87 đạt, rc=0` | ✅ khớp lời khai B-CI-EVIDENCE.md và điều phối |
| 7 | `python3 .claude/dev/packet_loop.py doctrine-scan` | sạch, 7 tệp, 0 chỗ chép doctrine | ✅ khớp lời khai điều phối |
| 8 | `python3 .claude/dev/packet_loop.py adr-song` | sạch, 46 ADR / 46 dòng §20, khớp 1–1 | ✅ (ngoài phạm vi giao nhưng đo cho chắc) |
| 9 | `python3 scripts/tl.py doc-claims-check --strict` | `rc=0` | ✅ (ngoài phạm vi giao nhưng đo cho chắc) |
| 10 | `verdict_sha256`/`verdict_bytes` của 3 biên nhận mới (`plat-x8b-review-1`, `plat-x8-review-3`, `plat-x8-review-4`) so `sha256sum`/`wc -c` tệp thật | cả 3 khớp TỪNG BYTE | ✅ khớp |
| 11 | `evidence_url` của 3 biên nhận: commit có tồn tại? nội dung tại commit đó có khớp `verdict_sha256`? có đúng là commit ĐẦU TIÊN thêm tệp (`git log --diff-filter=A`)? | cả 3 (`1d11f250`, `247c6fb5`, `c69eaf2f`) tồn tại, nội dung khớp băm, và đúng là commit ADD đầu tiên | ✅ khớp |
| 12 | `land-evidence.yaml`: `merge_commit` `647cfead…` có cha là `a22c5f83` + `28f32f7c`? có là ancestor của `origin/master`? | `git log -1 --format='%H %P %s' 647cfead…` khớp đúng hai cha; `merge-base --is-ancestor` ⇒ rc=0 | ✅ khớp |
| 13 | `land-evidence.yaml` post_merge: `_BANG_LOP` trên master = 7 mục, 0 `systemic`/`routine` | `git show origin/master:ops/lease_publish.py \| grep -A12 "_BANG_LOP = ("` ⇒ đúng 7 mục, tất cả `"sensitive"` | ✅ khớp |
| 14 | `t26` có đọc `schema_version`/hai identity/`anchor` không (khẳng định `no_da_khai` của cả 3 biên nhận) | đọc `ops/lease_publish_test.py:911-943` — `t26` chỉ đọc `verdict_path`/`verdict_sha256`/`evidence_url` dạng https; không đụng `schema_version`, identity, `anchor` | ✅ lời tự khai ĐÚNG |
| 15 | Đính chính lý do non-canon lượt 3 (2 identity = `model_reviewer_identity`+`github_submitter_identity`, không phải "hai bên độc lập") so `PROTOCOL:424-440` + `ADR-0040` | đọc trực tiếp cả hai nguồn — khớp nguyên văn đính chính | ✅ đúng |
| 16 | `review_rounds_used`: `PLAT-X8` 0→1 (lượt 4; lượt 3 không tính) và `PLAT-X8b` 0→1 (ngân sách riêng) — có cộng dồn nhầm không | đọc `ADR-0043` ("Trần canon cho MỘT PR packet") + hai receipt — không tìm được chỗ cộng chéo | ✅ không thấy lỗi |
| 17 | `authorization_url: null` trong land-evidence — có chỗ nào trong diff khai ngược? | `grep -rn authorization_url` trên toàn diff | ✅ không có chỗ mâu thuẫn |
| **18** | **`t27` (cổng nâng caveat biên nhận lên `ops/reviews/README.md`) có thực sự đọc field caveat của 3 biên nhận mới không** | **KHÔNG — xem finding P2 #1** | ❌ |
| **19** | **Mọi caveat trong 3 biên nhận mới có nằm ở README chưa** | **THIẾU 1/12 — xem finding P2 #2** | ❌ |
| **20** | **`ops/land/plat-x8-land-evidence.yaml` bookkeeping có còn đúng ở CẢ HAI phía của lần merge #264 không** | **KHÔNG — xem finding P3** | ❌ |
| 21 | CI theo job trên `reviewed_sha` (`B-CI-EVIDENCE.md`) | **KHÔNG ĐO ĐƯỢC bởi reviewer** — `mcp__github__pull_request_read` bị từ chối quyền trong phiên này (không phải 403 GitHub, mà "chưa được cấp"); không có `gh`. Nhận đúng như lời khai của B-CI-EVIDENCE.md: run trên head TRƯỚC (`21c823ca`) ubuntu+windows success, và điều phối khai đã đối chiếu cổng `87/87` hai bên — reviewer **tự đo lại độc lập được phần cổng tại chỗ** (#6,#7 trên) và khớp, nhưng KHÔNG tự đo được phần Actions | n/a |

## Finding 1 — `t27` không kiểm caveat của 3 biên nhận mới vì SAI TÊN TRƯỜNG [P2]

**TỆP/DÒNG:** `ops/reviews/plat-x8b-review-1-claude-verdict.receipt.yaml:144`, `ops/reviews/plat-x8-review-4-claude-verdict.receipt.yaml:148`, `ops/reviews/plat-x8-review-3-claude-verdict.receipt.yaml:126` — cả ba dùng khoá `canh_bao_da_nang_len_muc_luc:`.

**VẤN ĐỀ:** `t27` (`ops/lease_publish_test.py:947-1053`, cổng buộc mọi caveat của một biên nhận phải xuất hiện ở `ops/reviews/README.md`) đọc field `verdict_usage_caveats` (dòng 1038: `d.get("verdict_usage_caveats") or []`). 27/30 biên nhận cũ trong kho dùng đúng tên này. Ba biên nhận MỚI của chính PR này — cả ba, không phải một — dùng tên khác: `canh_bao_da_nang_len_muc_luc`. Không có dòng mã nào trong `ops/lease_publish.py`, `ops/lease_publish_test.py` hay `.claude/dev/packet_loop.py` đọc tên đó (`grep -rn canh_bao_da_nang_len_muc_luc` trên ba tệp ⇒ rỗng). Kết quả: với cả ba biên nhận này, vòng lặp `for c in cac_caveat` ở `t27` chạy trên danh sách RỖNG — cổng **không hề đọc** 12 caveat mà ba biên nhận này tự khai đã "nâng lên mục lục". Đây đúng hình dạng doctrine của kho: *"cổng xanh nhờ rc=0 là cổng có thể bị lừa"*.

**ĐÃ THỬ VÁ:** Có. Trên bản sao cả cây (`git archive cc6657e8` ra `/tmp`, không đụng cây review lẫn kho thật): đổi khoá `canh_bao_da_nang_len_muc_luc:` → `verdict_usage_caveats:` trong đúng 3 tệp receipt (giữ nguyên cấu trúc `id`/`noi_dung`, y hệt 27 biên nhận cũ).

**ĐÃ THỬ NGHIỆM (bốn lượt đo, cả hai chiều):**
1. Baseline (nội dung PR nguyên trạng, chưa vá): `87/87 đạt, rc=0`.
2. Xoá thử một hàng caveat khỏi README (`danh-tinh-khac-phien-la-SUY-TU-VANG-MAT` của `plat-x8b-review-1`) — **CHƯA vá tên trường**: `87/87 đạt, rc=0` — **`t27` không phát hiện**, chứng minh nó mù thật, không chỉ là nghi ngờ lý thuyết.
3. Áp bản vá (đổi tên trường ở 3 tệp) + README VẪN thiếu hàng đó: `86/87`, `t27` ĐỎ ĐÚNG với thông báo trỏ thẳng `danh-tinh-khac-phien-la-SUY-TU-VANG-MAT` / `plat-x8b-review-1-claude-verdict.md` — cổng nay có răng.
4. Khôi phục hàng README + áp bản vá: `87/87 đạt, rc=0` — không hồi quy.

**ĐỘ TIN:** cao — đo bằng mutation hai chiều trên chính cổng thật, không suy luận.

## Finding 2 — Nội dung bị Finding 1 che: caveat `mo-neo-TRUNG-BINH-khong-phai-manh` của `plat-x8b-review-1` chưa lên README [P2, hệ quả của Finding 1]

**TỆP/DÒNG:** `ops/reviews/plat-x8b-review-1-claude-verdict.receipt.yaml` — mục thứ 4 trong `canh_bao_da_nang_len_muc_luc` (`mo-neo-TRUNG-BINH-khong-phai-manh`, nói mỏ neo verdict chỉ là `canonical_ancestry`/`trung_binh`, chết nếu nhánh bị xoá trước khi land). `ops/reviews/README.md` bảng "Cảnh báo đang có hiệu lực" **không có hàng nào** với cặp (`plat-x8b-review-1-claude-verdict.md`, `mo-neo-TRUNG-BINH-khong-phai-manh`) — chỉ có cặp đó cho `plat-x8-review-4-claude-verdict.md` (dòng 117), một verdict KHÁC.

**VẤN ĐỀ:** Đây chính là gap mà Finding 1 che: vì `t27` không đọc trường của biên nhận này, cổng không thể phát hiện caveat thứ 4 (trong 4) của `plat-x8b-review-1` bị bỏ sót khi soạn README — 3/4 được nâng lên (có lẽ chép tay), nhưng cái thứ 4 rơi mất, đúng khớp câu README tự cảnh báo ở đầu tệp: *"một cảnh báo nằm trong tệp không ai mở thì bằng không"* — và ở đây nó còn tệ hơn: cảnh báo về mỏ neo YẾU của chính verdict `approve` đang cấp `cross_approved` cho `PLAT-X8b` bị thiếu đúng chỗ người đọc cần thấy nhất.

**ĐÃ THỬ VÁ:** Có — trên cùng bản sao `/tmp`, thêm hàng README:
`| `plat-x8b-review-1-claude-verdict.md` | `mo-neo-TRUNG-BINH-khong-phai-manh` | (nội dung y hệt hàng đã có của review-4) |`

**ĐÃ THỬ NGHIỆM:** Sau khi thêm hàng (cộng bản vá Finding 1): `87/87 đạt, rc=0`, `t27` không còn kêu về caveat nào của cả 3 biên nhận (đối chiếu tay bằng script liệt kê toàn bộ 12 caveat × cột `(id, tệp verdict)` — cả 12 đều tìm thấy hàng đúng sau khi vá).

**ĐỘ TIN:** cao — đo trực tiếp bằng liệt kê đối chiếu, không suy luận từ mẫu.

**Bản vá này có thể đẻ ra gì:** rủi ro thấp — chỉ đổi tên khoá YAML (không đụng trường neo `verdict_sha256`/`reviewed_sha`/`evidence_url`) và thêm một hàng bảng Markdown lấy nguyên văn từ hàng đã có sẵn cho verdict khác. Rủi ro nếu KHÔNG vá: mọi biên nhận sau này copy 1 trong 3 tệp mới này làm mẫu (đúng thói quen copy-paste mà chính PR #264 đã tự bắt được ở finding `lease-ghi-chu-chep-tu-goi-packet-me-sai-du-lieu`) sẽ nhân bản tên trường sai, và `t27` sẽ tiếp tục xanh giả trên diện rộng hơn.

## Finding 3 — Bookkeeping của `land-evidence.yaml` sẽ SAI đúng lúc PR này land [P3]

**TỆP/DÒNG:** `ops/land/plat-x8-land-evidence.yaml:113` — `'Verdict + biên nhận cả bốn lượt nằm trên nhánh handoff, CHƯA vào master. Chúng chỉ về master khi nhánh này land.'`

**VẤN ĐỀ:** Đúng hình dạng lỗi mà `CLAUDE.md` đã ghi giá ("câu mô tả VỊ TRÍ của một artefact phải đúng ở CẢ HAI phía của lần merge") và đúng thứ mà prompt mục 7 chỉ tên. Câu này khai đúng tại thời điểm PLAT-X8 (#248) land (merge `647cfead`) — khi đó bốn verdict/biên nhận thật sự còn nằm trên nhánh handoff, chưa vào master. Nhưng CHÍNH `land-evidence.yaml` này — cùng với bốn verdict/biên nhận nó nhắc tới — là một phần của PR #264, và PR #264 chính là lượt đưa chúng vào master. Sau khi #264 merge, câu "CHƯA vào master" nằm sờ sờ trên master trong khi chủ ngữ của nó (các verdict ấy) đã có mặt trên master — câu tự phủ định chính nó ngay tại nơi nó neo.

**ĐÃ THỬ VÁ:** Có, trên bản sao `/tmp` — sửa câu để đúng ở cả hai phía, theo đúng mẫu `CLAUDE.md` khuyến nghị ("tìm ở X trước, chưa thấy thì..."):
`'Verdict + biên nhận cả bốn lượt được soạn trên nhánh handoff lúc #248 land; chúng vào master cùng lượt merge PR #264 — tìm trên nhánh handoff của #264 trước, chưa thấy thì đã ở master.'`

**ĐÃ THỬ NGHIỆM:** Không có ca `pytest` khoá câu bookkeeping tự do này (đã `grep` `ops/lease_publish_test.py`/`packet_loop.py` — không cổng nào đọc `ops/land/**`, đúng như chính `land-evidence.yaml` tự khai ở mục `PLAT-X8-LAND-EVIDENCE-KHONG-AI-KIEM`). Không đề xuất dựng gate mới trong write set của lượt này — đây là nợ văn bản, không phải lỗ kỹ thuật; nêu ra để người land #264 sửa câu trước khi merge, hoặc chấp nhận nợ có tên.

**ĐỘ TIN:** cao về HIỆN TƯỢNG (câu sẽ sai sau merge — đọc trực tiếp, không suy luận); trung bình về MỨC ĐỘ QUAN TRỌNG (đây là dòng bookkeeping tự do trong danh sách nợ, không phải trường có thẩm quyền — thấp hơn hẳn hai finding trên).

## Không tìm thấy vấn đề ở các mục còn lại của prompt

- Mục 2 (t26 có validate v2 không): lời tự khai của cả 3 biên nhận ("chưa bộ kiểm nào cưỡng chế v2") ĐÚNG — đọc trực tiếp `t26` xác nhận.
- Mục 3 (cộng dồn review_rounds_used): không tìm thấy cộng chéo giữa `PLAT-X8` và `PLAT-X8b`; `ADR-0043` xác nhận ngân sách tính theo TỪNG packet.
- Mục 4 (land evidence khớp thực tế): merge_commit, ancestry, `_BANG_LOP` trên master — cả ba đo khớp. Riêng bookkeeping có vấn đề — xem Finding 3.
- Mục 5 (đính chính lý do non-canon lượt 3): đúng, đối chiếu `ADR-0040` + `PROTOCOL:424-440` khớp nguyên văn.
- Mục 6 (mục lục README — bảng "Mục lục" chính, không phải bảng caveat): 3 verdict + 3 biên nhận mới đều có hàng đúng, `verdict_path` khớp — chỉ RIÊNG bảng caveat mới thủng (Finding 1/2).

## Assurance thực sự đạt

- Lease `role: reviewer` hợp lệ, tự kiểm tồn tại (bảng đo #1) — không nhận lời khai.
- Cross-provider theo nghĩa hồ sơ: reviewer `claude` đọc lại toàn bộ diff + tự đo lại độc lập trên bản sao riêng, không chỉ tóm tắt.
- **KHÔNG tự khai `cross_approved` cho lượt review NÀY** — lease `assurance_target` là mục tiêu, không phải kết quả tự động; PR #264 tự nó không phải một packet thi công có executor/reviewer theo nghĩa §8 (nó là PR hồ sơ ghi lại bốn lượt review khác), nên khung `cross_approved`/`human_audited` áp cho CÁC PACKET ĐƯỢC GHI (`PLAT-X8`, `PLAT-X8b`), không áp trực tiếp cho việc "duyệt PR #264".
- Mức đúng để khai cho lượt NÀY: đã tự đo độc lập mọi khẳng định kiểm được trong phạm vi công cụ có (không có Actions), tìm được 2 finding P2 + 1 P3 ngoài mọi hướng "trần" mà prompt liệt kê, đã thử vá + đo cả hai chiều trên bản sao riêng theo đúng `yeu_cau_rieng_luot_nay` của lease.
- **KHÔNG xác minh được** "khác phiên soạn đặc tả/prompt/lease" bằng cơ chế nào ngoài lời khai của chính phiên này — suy luận từ VẮNG MẶT (không có quyền ghi `ops/`, không thấy dấu vết soạn lease trong ngữ cảnh phiên), đúng cảnh báo mà `nguoi_review_phai_khac_phien_ghi_chu` của chính lease này đã tự nêu trước.

## Giới hạn của chính lượt review này — nói thẳng

- **Không đo được CI theo job trên `reviewed_sha`** — `mcp__github__pull_request_read` bị từ chối quyền trong phiên (không cấp), không có `gh`. Nhận B-CI-EVIDENCE.md đúng như một LỜI KHAI của điều phối (đã ghi rõ trong bảng đo #21), không trích nó làm phép đo của bản thân.
- **Không quét lại toàn bộ 45 tệp còn lại của diff theo từng dòng** — tập trung vào các trường neo (hash/SHA/commit ancestry), các claim định lượng có thể đo bằng lệnh, và hai file SKILL.md (đọc toàn văn, không thấy vấn đề). Không loại trừ khả năng có lỗi văn phong/nội dung nhỏ khác chưa soi tới trong khối lượng lớn các file `ops/prompts/*.md` là bản sao gần như nguyên văn của các file đã review độc lập ở lượt trước.
- **Không đo được danh tính "phiên khác"** — xem mục Assurance.
- Không chạm cây review thật lẫn kho thật. Mọi vá thử + mutation chạy trên bản sao dựng bằng `git archive` trong thư mục scratchpad ngoài kho; `git status --porcelain` cây review vẫn rỗng, `log cc6657e8..HEAD` rỗng — xác nhận sau cùng.

## Đề xuất

Hai finding P2 (Finding 1+2) nên được vá trước khi coi bốn biên nhận này là "đã qua cổng caveat" — nhưng đây là PR hồ sơ, ba tệp lỗi đã TỒN TẠI trên nhánh khác (`ops/cap-lease-plat-x8-2`) từ trước, và bản vá là đổi tên một khoá YAML + thêm một hàng bảng, rủi ro rất thấp. Finding 3 là nợ văn bản, không chặn kỹ thuật. **Không đề xuất `blocked`** — đề xuất `changes_requested` với gợi ý vá cụ thể ở trên; người vá (không phải reviewer, theo đúng cấm của lease) tự quyết áp nguyên văn hay khác đi, miễn đóng đúng lớp.
