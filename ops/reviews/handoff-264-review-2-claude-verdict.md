# VERDICT — cross-review PR #264, LƯỢT 2, reviewer `claude`

verdict: `approve`
reviewed_sha: `1badac86d8b2982d59d6130d77f74ed97607671a` · base_sha: `05de1ab81c235235b971a6fb8d8ae1fb226295d5`
lease: `handoff-264-review-2-claude-20260823` (role: reviewer). Thẩm quyền tự kiểm: PROMPT.md trong
`in-264b` khớp byte-for-byte với `ops/prompts/handoff-264-review-2-claude-20260823.md` trong cây
review (`diff` rỗng), và cả hai có `sha256 = cbd651c8…dacbe93de`, khớp `prompt_sha256_required` của
LEASE.yaml. Cây review sạch trước và sau khi tôi làm việc (`git status --porcelain` rỗng cả hai lượt
đo), `core.abbrev=7` đúng yêu cầu. `base_sha` là ancestor thật của HEAD (`merge-base --is-ancestor` rc=0).

Không tự khai `cross_approved` cho việc "duyệt PR #264" — cùng lý do lượt 1 đã nêu: PR #264 là PR
**hồ sơ** ghi lại các lượt review của `PLAT-X8`/`PLAT-X8b`, không phải bản thân một packet thi công
có executor/reviewer theo nghĩa §8. Mức đúng để khai cho lượt NÀY: đã tự đo độc lập (không nhận lời
khai) toàn bộ ba finding lượt 1 + toàn bộ nội dung `delta-ban-va.patch` (6 tệp, phần chưa ai soi),
trên bản sao riêng ngoài kho, không chạm cây review/kho thật.

## ĐỐI CHIẾU LƯỢT TRƯỚC — bốn nhãn `§8`, tự đo, không nhận lời khai

### F1 [P2] — `t27` mù vì sai tên trường (`canh_bao_da_nang_len_muc_luc` → `verdict_usage_caveats`)
**Nhãn: ĐÃ VÁ THẬT.**

Bằng chứng tự đo (KHÔNG dùng bản đo của lượt 1 — dựng lại từ đầu trên bản sao riêng của tôi,
`git archive HEAD` ra thư mục scratchpad ngoài kho):
1. `grep -rn canh_bao_da_nang_len_muc_luc` trên toàn kho: chỉ còn **một** chỗ, và đó là **chuỗi giải
   thích trong chính prompt lượt 2** (`ops/prompts/handoff-264-review-2-claude-20260823.md:28`, nhắc
   tên trường CŨ để mô tả finding) — không phải một chỗ dùng thật. `ops/reviews/README.md` có
   **0** lần nhắc tên cũ.
2. `grep -n "verdict_usage_caveats" ops/lease_publish_test.py`: `t27` đọc đúng
   `d.get("verdict_usage_caveats")` (dòng 1038); không tệp `.py` nào khác trong kho đọc field caveat
   (đã grep `ops/lease_publish.py` + `.claude/dev/packet_loop.py`: rỗng).
3. **Mutation hai chiều tự chạy trên bản sao riêng** (không dùng lại kết quả lượt 1):
   - Baseline (cây HIỆN TẠI, đã vá): `python3 ops/lease_publish_test.py` ⇒ `87/87 đạt, rc=0`.
   - Xoá 1 hàng caveat khỏi `README.md` (hàng `mo-neo-TRUNG-BINH-khong-phai-manh` /
     `plat-x8b-review-1-claude-verdict.md`) ⇒ `86/87`, **`t27` ĐỎ**, thông báo trỏ đúng
     `caveat 'mo-neo-TRUNG-BINH-khong-phai-manh' của plat-x8b-review-1-claude-verdict.receipt.yaml
     KHÔNG nằm ở CỘT 'id'...`.
   - Khôi phục hàng ⇒ `87/87 đạt, rc=0` lại — không hồi quy.
4. `verdict_sha256`/`verdict_bytes` của cả 3 tệp `.receipt.yaml` bị đổi tên trường vẫn khớp byte-for-byte
   với `.md` tương ứng (tôi tự tính `hashlib.sha256`/độ dài, không đọc từ verdict lượt 1) — đổi tên
   khoá không đụng trường neo.

Cổng có răng thật, không phải xanh giả.

### F2 [P2] — caveat `mo-neo-TRUNG-BINH-khong-phai-manh` của `plat-x8b-review-1` thiếu hàng README
**Nhãn: ĐÃ VÁ THẬT.**

Tự liệt kê lại **toàn bộ** 12 caveat của 3 biên nhận mới bằng script tự viết (đọc `verdict_usage_caveats`
qua `yaml.safe_load`, đối chiếu từng cặp `(id, tệp verdict)` với TỪNG dòng của bảng README — không
nhìn lướt, không tin số "12" của lượt 1):

| tệp | số caveat | tất cả có hàng README? |
|---|---|---|
| `plat-x8-review-3-claude-verdict` | 4 | có |
| `plat-x8-review-4-claude-verdict` | 4 | có |
| `plat-x8b-review-1-claude-verdict` | 4 | có |

Tổng **12/12**, **0 MISSING**. Riêng caveat bị Finding 2 nêu (`mo-neo-TRUNG-BINH-khong-phai-manh` của
`plat-x8b-review-1`) nay có hàng riêng ở `README.md:112`, tách biệt với hàng của `plat-x8-review-4`
ở dòng 118 (hai hàng cùng `id` nhưng khác cột "tệp verdict" — đúng, vì đây là hai verdict riêng cùng
loại caveat).

### F3 [P3] — dòng bookkeeping `land-evidence.yaml` tự phủ định sau merge
**Nhãn: ĐÃ VÁ THẬT.**

Tự đọc `ops/land/plat-x8-land-evidence.yaml` trên cây hiện tại, không dùng lại trích dẫn của lượt 1:
- Câu mới dùng khối `>-` (folded scalar) — tự parse bằng `yaml.safe_load`: ra đúng **1 chuỗi**, không
  vỡ kiểu, `bookkeeping` vẫn là list 3 phần tử toàn `str` — **không có hồi quy YAML**.
- Nội dung: *"Verdict + biên nhận cả bốn lượt được SOẠN trên nhánh handoff trong lúc #248 land; chúng
  vào master cùng lượt merge PR #264. Phép tra đúng ở CẢ HAI phía..."* — tôi tự đối chiếu với
  `diff.patch` toàn PR: cả 4 cặp `.md`/`.receipt.yaml` (`plat-x8-review-3`, `plat-x8-review-4`,
  `plat-x8b-review-1`, và chính `plat-x8-land-evidence.yaml`) đều nằm trong danh sách 17 tệp của PR
  #264 (`diff --git a/... new file mode` hoặc modified) — câu khẳng định "chúng vào master cùng lượt
  merge #264" là **đúng sự thật**, không chỉ đúng cú pháp.
- Tìm chỗ khác cùng bệnh mà lượt 1 bỏ sót: `grep -rn "chưa vào master\|CHƯA vào master\|chỉ về master"`
  trên toàn kho — chỗ duy nhất còn dạng câu tương tự và **có khả năng tự phủ định theo cách này** là
  `ops/reviews/plat-x8-review-4-claude-verdict.receipt.yaml:132` (*"Verdict + biên nhận lượt 3 chỉ nằm
  trên nhánh handoff, KHÔNG trên nhánh phối hợp packet"*) — nhưng mục đó có `trang_thai: DA_DONG`, nói
  về quan hệ với nhánh `ops/cap-lease-plat-x8-2` (không phải `master`) tại một mốc thời gian đã khoá
  bằng SHA cụ thể (`247c6fb5`/`8cd2262b`), không phải câu "còn hiệu lực tới lúc land" như F3 gốc —
  **không cùng bệnh**, không cần vá thêm. Các chỗ còn lại khớp mẫu grep đều mô tả tài liệu/quy trình
  chung (`THAM_DINH_KE_HOACH…`, `RUT_LEASE_PLAT_X8…`) hoặc lease khác đã đóng, không phải claim vị trí
  của chính nội dung PR #264.

## BẢNG ĐO — kể cả cái khớp, tự đo trên bản sao/cây riêng

| # | khẳng định / lệnh | kết quả đo (thời điểm: lượt review này) | khớp? |
|---|---|---|---|
| 1 | `sha256sum in-264b/PROMPT.md` vs `ops/prompts/handoff-264-review-2-claude-20260823.md` trong cây | cả hai `cbd651c8…dacbe93de`, `diff` rỗng | ✅ |
| 2 | `git rev-parse HEAD` cây review | `1badac86…` = `reviewed_sha_required` | ✅ |
| 3 | `git status --porcelain` (trước và sau việc của tôi) | rỗng cả hai lượt | ✅ sạch |
| 4 | `git config core.abbrev` | `7` | ✅ |
| 5 | `git merge-base --is-ancestor 05de1ab8… HEAD` | rc=0 | ✅ base_sha là ancestor thật |
| 6 | `python3 ops/lease_publish_test.py` (cây review, tại chỗ) | `87/87 đạt, rc=0` | ✅ |
| 7 | `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | `sạch — 7 tệp, 0 chỗ chép doctrine`, rc=0 | ✅ |
| 8 | `git archive HEAD` ra bản sao scratchpad riêng, chạy lại `ops/lease_publish_test.py` | `87/87 đạt, rc=0` (độc lập với #6) | ✅ |
| 9 | Mutation: xoá 1 hàng caveat README trên bản sao riêng | `86/87`, `t27` ĐỎ đúng tên caveat | ✅ có răng |
| 10 | Khôi phục hàng, chạy lại | `87/87 đạt, rc=0` | ✅ không hồi quy |
| 11 | `grep -rn canh_bao_da_nang_len_muc_luc` toàn kho | 1 chỗ, là mô tả trong prompt lượt 2 (không phải dùng thật) | ✅ không sót tên sai |
| 12 | Liệt kê 12 caveat (3×4) đối chiếu README bằng script tự viết | 12/12 có hàng, 0 MISSING | ✅ |
| 13 | `verdict_sha256`/`verdict_bytes` 3 tệp `.md` (tự tính `hashlib`) vs `.receipt.yaml` | khớp cả 3 (không đụng bởi đổi tên khoá) | ✅ |
| 14 | `yaml.safe_load` trên `plat-x8-land-evidence.yaml` sau vá | parse OK, `bookkeeping` 3 phần tử, đều `str` | ✅ không hồi quy kiểu |
| 15 | Đối chiếu câu F3 mới với `diff.patch` (4 tệp verdict/receipt + chính land-evidence có trong PR #264 không) | cả 4 đều nằm trong 17 tệp của PR #264 | ✅ đúng sự thật, không chỉ đúng cú pháp |
| 16 | `diff --git` toàn `delta-ban-va.patch` | đúng 6 tệp, tất cả đã soát ở trên | ✅ không sót phần nào của delta |
| **17** | **`B-CI-EVIDENCE.md` — kiểm `head=` như hướng dẫn mục GIỚI HẠN của chính tệp đó** | **KHÔNG THỰC HIỆN ĐƯỢC** — khối log dán trong tệp không hề in trường `head=` nào để đối chiếu; chỉ có `run <id>: 2 job` + tên job. Không có cách tự kiểm theo đúng chỉ dẫn của tệp | ⚠️ xem "Giới hạn" |
| **18** | **CI run `32612665951` trạng thái** | Cả hai job `in_progress`, **conclusion = None** (chưa xong), `30 bước đã chạy, 0 HONG` — đây là ảnh chụp GIỮA CHỪNG, không phải run đã hoàn tất `success` | ⚠️ xem "Giới hạn" |

## Không tìm thấy vấn đề mới chặn kỹ thuật trong `delta-ban-va.patch`

Đã đọc và tự đo toàn bộ 6 tệp của delta (danh sách #16 ở trên):
`ops/land/plat-x8-land-evidence.yaml`, `ops/prompts/handoff-264-review-2-claude-20260823.md` (mới),
`ops/reviews/README.md`, và ba `.receipt.yaml`. Không phát hiện thêm finding P1/P2 mới ngoài việc xác
nhận ba finding lượt 1 đã đóng thật. Không tìm được chỗ nào trong delta lặp lại đúng bệnh của F1
(tên trường sai) hay F3 (câu tự phủ định vị trí) mà chưa được vá.

## Assurance thực sự đạt

- Lease `role: reviewer` hợp lệ, tự kiểm PROMPT.md khớp hash (bảng đo #1) — không nhận lời khai.
- Toàn bộ phép đo trong "ĐỐI CHIẾU LƯỢT TRƯỚC" và "BẢNG ĐO" là **tự chạy lại từ đầu** trên bản sao
  scratchpad riêng (`git archive` ra ngoài kho) và trên cây review tại chỗ — không copy số của lượt 1,
  kể cả khi kết quả trùng với lượt 1 (ví dụ #12: 12/12 caveat — tôi đếm lại bằng script riêng, không
  đọc bảng của lượt 1 rồi xác nhận bằng mắt).
- **KHÔNG tự khai `cross_approved`** cho việc duyệt PR #264 — cùng lý do lượt 1 đã nêu (PR hồ sơ, không
  phải packet thi công trực tiếp). Khung `cross_approved`/`human_audited` áp cho các packet ĐƯỢC GHI
  (`PLAT-X8`, `PLAT-X8b`), không áp cho việc duyệt PR ghi hồ sơ này.
- **KHÔNG xác minh được** "khác phiên soạn lease/prompt" bằng cơ chế nào ngoài suy luận từ VẮNG MẶT
  (phiên này không có quyền ghi `ops/`, không thấy dấu vết soạn lease trong ngữ cảnh phiên) — đúng
  giới hạn mà chính `nguoi_review_phai_khac_phien_ghi_chu` của lease đã tự nêu trước, và đúng bài học
  `CLAUDE.md` "SUY TỪ VẮNG MẶT không phải phép đo dương tính".

## Giới hạn của chính lượt review này — nói thẳng

- **`B-CI-EVIDENCE.md` không cho phép tự kiểm đúng như chỉ dẫn của chính nó**, và nội dung nó mang là
  ảnh chụp một run **CHƯA HOÀN TẤT** (`in_progress`, conclusion `None`), không phải một run `success`
  đã xong. Khác với bằng chứng CI của lượt 1 (khai job `success` cho head TRƯỚC). Tôi khai đúng nguồn:
  đây là **lời khai của điều phối về một run giữa chừng**, KHÔNG phải bằng chứng "CI xanh trên head
  này" — và tôi không có công cụ Actions (không `gh`, `mcp__github__pull_request_read` không sẵn trong
  phiên này) để tự đo lại phần Actions. Không nhận đây là "đã đo CI".
  Điều này **không đổi verdict** vì: (a) phần cổng thật sự quan trọng của lượt này (`t27`/toàn bộ
  `lease_publish_test.py`, `doctrine-scan`) tôi đã tự đo lại độc lập tại chỗ VÀ trên bản sao riêng,
  cả hai `rc=0`; (b) PR #264 là PR hồ sơ, không sinh mã chạy production; (c) nếu run Actions kết thúc
  và có bước hỏng, đó là tín hiệu người land phải tự kiểm lại trước khi merge — nêu rõ trong "Đề xuất".
- Không quét lại từng dòng của 11 tệp trong diff toàn PR nằm NGOÀI `delta-ban-va.patch` (đã được lượt 1
  đo) — tập trung 100% năng lực của lượt này vào phần `delta-ban-va.patch` CHƯA AI SOI, đúng trọng tâm
  lease giao.
- Không xác minh được thời điểm THẬT các verdict/receipt "được SOẠN trong lúc #248 land" (câu văn F3)
  bằng archaeology git đầy đủ (commit timestamps trên nhánh handoff) — chấp nhận đây là claim narrative
  P3, thấp rủi ro, không phải trường có thẩm quyền (giống đánh giá của lượt 1).
- Không chạm cây review thật lẫn kho thật ở bất kỳ bước nào — `git status --porcelain` rỗng, không có
  commit lạ, xác nhận trước VÀ sau (bảng đo #3). Mọi mutation/thử vá chạy trên bản sao dựng bằng
  `git archive HEAD` trong thư mục scratchpad ngoài kho, không phải `/tmp` trực tiếp.
- Không xác minh được "phiên review này khác phiên soạn lease/prompt" bằng bằng chứng dương tính —
  xem mục Assurance.

## Đề xuất

Ba finding lượt 1 đều **ĐÃ VÁ THẬT**, xác nhận bằng đo lại độc lập (không chỉ đọc lời khai), bao gồm
mutation hai chiều cho F1 và liệt kê đối chiếu đầy đủ cho F2. Không tìm thêm finding P1/P2 chặn kỹ
thuật nào trong `delta-ban-va.patch`. **Đề xuất `approve`.**

Một điểm nên xử trước khi LAND (không chặn duyệt PR, nhưng chặn "land an toàn"): CI Actions cho
`reviewed_sha` **chưa xác nhận hoàn tất** tại thời điểm review này — người thực hiện land nên tự đo
lại `head=`/conclusion thật của run `32612665951` (hoặc run mới hơn) bằng công cụ có quyền Actions,
đừng suy "0 HONG giữa chừng" thành "CI xanh", đúng bài học đã trả giá của kho này
("gate xanh chỉ là chưa chạy xong" / "cổng vắng mặt trông giống cổng xanh").
