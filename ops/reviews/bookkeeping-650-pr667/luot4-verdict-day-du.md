**1 P1 / 0 P2 / 0 P3**

verdict: changes_requested

```yaml
reviewed_sha: 80076c6ed5aa87f2e0a7a28262f78a015e0f2dc6
reviewed_tree: 97708ef03645160afcaeb1521636e7e93f10ae9f
base: f8a7829cc44f296c25faf1a6439b603ba840f70b
lease_source: 4fe61ac338408fc0758c4aa67f04f11e03f300b9
previous_cli_reviewed_sha: 9a6f48f548df453e0348af0d877707c8540b6938
role: reviewer
provider: openai_codex
execution_surface: codex_cli
transport: machine
assurance: advisory_review
review_class_applied: sensitive
review_axes: [spec, standards_security]
github_submitter_identity: null
published: false
```

**K1 đã vá thật tại erratum. Toàn lớp `landed-vuot-bang-chung` chưa đóng:** hồ sơ YAML dòng 224 vẫn nói khối `nang_tran` được ghi “sau land”, trong khi chính hồ sơ xác định `landed: false`. Ghi **L1/P1** cho biểu hiện còn sót này. **Giữ nguyên disposition G5/G6 từ lượt 3**, không đếm lại thành P3 mở của #667.

## Phạm vi, authority và preflight

Đây là **CLI lượt 4**, theo assignment trực tiếp: review offline, checkout riêng chỉ đọc, không commit/push/mạng, báo cáo ngoài kho. Chỉ thị bổ sung yêu cầu kiểm K1 và quét toàn bộ văn bản mới của PR, thay phần đối chiếu cũ khi mâu thuẫn. Ngưỡng nội dung áp dụng là **0 P1/P2/P3**; giữ assurance advisory, không tự tạo approval của state machine. Không dùng lease lịch sử đã hết hạn của #650 để cấp quyền làm việc mới. Write set của reviewer chỉ là `/tmp/review667-r4-output/`.

Đo bằng `git rev-parse`: HEAD/tree/base/ref lease đúng bốn OID đầu báo cáo. Checkout **detached**. `origin` là mirror local `/home/user/tra-luat`, không phải phép đọc GitHub hiện hành. Các refs là snapshot được cấp; chỉ có **5 remote-tracking refs**. Không đổi origin/config và không mở repo nguồn ngoài checkout để bù phạm vi. Tracked/untracked sạch; `.codex/` ignored và rỗng. `core.abbrev` repo-local vắng (probe rc=1); các phép đo trong harness ghim **7 qua môi trường tiến trình**, probe hiệu lực rc=0, output `7`.

Diff `origin/master..HEAD`: **15 tệp**, gồm lease, land YAML, erratum, 12 hiện vật dưới thư mục review (kể cả `.gitattributes`). Delta `9a6f48f..HEAD`: **3 tệp, +199/−3** — hai verdict lượt 3 và sửa erratum. **Land YAML không đổi từ lượt 3.** Không có diff sản phẩm/workflow/release artifact.

Spec lịch sử được đối chiếu từ nguồn `0fc9766f39b585df3021ec43427c3866ae8271a2:ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a.md`, blob `8224ba54176f6bbfba528ed2e3fb6555852ba336`. SHA-256 nguồn, local copy và `spec_hash` đều bằng `978058983e8eddefebfba267dbff2ef5cee95daf9b2d4847121d43b8cff89d77`; revision **5**, generation **2**, hash ba đường write set khớp. Immutable acceptance baseline là `5618f61c6ac2fa14aab52b0f5ce3d065aee8e022`; continuation base `04f2b5fea60bbdd2fdd8e8eae9fa00871c92fc77`. Base review bookkeeping không thay hai mốc này.

Executor là Claude; lease khai `anthropic_claude / claude_code`, model `claude-opus-5-5`, effort chưa đo độc lập. Reviewer dùng context riêng, không nhận context Executor, không gọi Claude reviewer/subagent. Provider/surface/transport theo run được giao; không có header/receipt độc lập của chính run trong input để xác nhận exact model variant, effort hay session ID/runtime từng request. Không suy các trường ấy từ header do Executor thêm vào hiện vật lịch sử. Áp dụng skill `.agents/skills/cross-review/SKILL.md`; chỉ dẫn xuất verdict offline theo assignment, không dùng bước vận chuyển lên GitHub.

## Lớp A — ĐỐI CHIẾU LƯỢT TRƯỚC

### K1 và các disposition được giữ

| Finding lượt 3 | Kết quả lượt 4 | Bằng chứng tự đo |
|---|---|---|
| **K1/P1**, `landed-vuot-bang-chung`, erratum | **da_va_that tại biểu hiện K1**; toàn lớp **chua_va hết**, xem L1 | `review_round4.py`: câu `packet đã land` có ở `9a6f48f`, vắng ở HEAD; dòng 5/10/16 dùng merge, dòng 17 nói rõ **`merged`, CHƯA `landed`** và trỏ YAML. Không còn khẳng định landed trong erratum mới. |
| **H1** đã đóng ở lượt 3 | Giữ **da_va_that** | YAML 37–42 đủ Run/Checkout/Workflow definition/Gate output cho ba run; waiver Gate output không tự bao phủ hai mốc identity. Phép đo cho `H1_all_three_runs_and_four_anchors=true`; đọc đầy đủ nội dung waiver. |
| **G5/G6** | Giữ **disposition_owner**, không P3 mở của #667 | Spec bất biến; erratum vẫn phủ nhận A14 đạt; YAML vẫn ghi nợ validator #669 chưa triển khai. Delta không thay disposition. |

### Bảng bảo toàn G1–G6

Đã chạy lại hai script lượt 1 và script lượt 2 bằng bản sao ngoài checkout. Chỉ đổi ROOT/OUT/ENV qua `run_checks.py`, đường input r1/r2 sang input r4, khóa `workflow_definition` sang `workflow_definition_suy_ra`, và các khoảng dòng trích cho đúng HEAD. Diff chuyển mỏ neo được lưu cạnh từng script. Giữ nguyên phép so Git/hash/timestamp/session/jobs/numstat. Nhãn lịch sử như `G3: AUTHORITY BODY ABSENT` trong script không tự là verdict hiện hành.

| ID / slug | Phán xử hiện tại | Phép đo / vị trí |
|---|---|---|
| **G1** — `ci-danh-tinh-suy-tu-head` | **da_va_that** cho lời khai provenance | YAML 107–111, 129–130, 138, 148–155: `*_suy_ra` là đối chiếu Git, bị rút khỏi provenance. Ba blob/SHA-256 khớp **3/3**, không chứng minh definition của các run. Checkout/definition vẫn chưa đo đúng nguồn. |
| **G2** — `landed-vuot-bang-chung` | **chua_va hết lớp** | Trạng thái chính, correction lease và H1 đúng; K1 ở erratum đã sửa. Còn câu “sau land” ở YAML 224: **L1/P1**. Không gọi toàn lớp đã đóng. |
| **G3** — `authority-thieu-than-readback` | **da_va_that** cho thiếu nội dung disclosure | YAML 70–92; **5/5** core quotes trong input khớp, actor/association/5 checkbox/authorized SHA khớp; update trước merge **36 giây**. Full body, hai câu trích ngoài tập input và human identity độc lập chưa xác minh; không biến thiếu raw body thành finding mới. |
| **G4** — `chuyen-vai-cung-session-chua-khai` | **da_va_that** cho thiếu khai lệch | YAML 188–197; `executor_selected_same_session=True`, `product_commit_session_matches_land=True`. Giữ câu “Khai lech KHONG xoa vi pham.” |
| **G5** — `acceptance-doi-khong-revision` | **disposition_owner**, không P3 mở của #667 | Numstat so `ceb1a3f`: **+650/−0 = 1+114+535**; so immutable baseline: **+730/−10**. Erratum 12–21 và YAML 198–210 giữ A14 không đạt r5; không revision hồi tố. |
| **G6** — `validator-land-chua-co` | **disposition_owner**, implementation **chua_va** ở #669 | YAML 158–159 khai tên `LAND-EVIDENCE-VALIDATOR`, Issue **#669**, con **#499**, quyết định owner 2026-09-28 và ngoài phạm vi bookkeeping. Không tuyên validator đã có. |

### Lịch sử lớp

| Slug | IDs / nguồn | Mức còn mở của PR | Phép đóng lớp |
|---|---|---|---|
| `landed-vuot-bang-chung` | G2: CLI1 `392199d…`; H1: CLI2 `900fbbe…`; K1: CLI3 `9a6f48f…`; L1: CLI4 `80076c6…` | **1 P1 / 1 biểu hiện được ghi finding hiện hành** | Đối chiếu mọi câu khẳng định trạng thái trong văn bản mới với `trang_thai_packet`, kể cả câu hồi thuật thời điểm. Không sửa hiện vật lịch sử nguyên byte. |
| `ci-danh-tinh-suy-tu-head` | G1 | Không | Đo bytes Git; kiểm nhãn suy ra và rút khỏi provenance. |
| `authority-thieu-than-readback` | G3 | Không | Đối chiếu phần nội dung có trong input; giữ giới hạn identity/body. |
| `chuyen-vai-cung-session-chua-khai` | G4 | Không | Session/trailer/lease trùng phải được khai đúng. |
| `acceptance-doi-khong-revision` | G5 | Không; owner disposition | Spec bất biến, erratum không biến A14 thành pass. |
| `validator-land-chua-co` | G6 | Không; owner disposition | Nợ #669 còn tên/phạm vi, chưa triển khai. |

Với U của lượt 3 chỉ còn lớp G2/H1/K1, **F/U = 0/1**: K1 đã sửa nhưng lớp chưa đóng do L1. **Không có slug mới**; L1 là biểu hiện cũ được phát hiện khi mở rộng quét theo assignment, không phải lỗi do delta lượt 4 sinh ra. Script xác nhận câu này đã có cả ở `392199d` và `9a6f48f`; review trước đã bỏ sót ý nghĩa trạng thái của nó. Không viết lại verdict cũ để xóa thiếu sót này. Giữ tín hiệu Review Rescue Checkpoint §12 của lớp tái diễn; không tự cấp lượt tiếp, không suy allowance còn lại từ số lượt CLI. Lượt này được user giao trực tiếp.

## Lớp B — Năm finding connector lượt 3 trên `f23f802`

Input chỉ có chuỗi tóm tắt `codex_connector_667.luot3_f23f802` (**3 P1 + 2 P2**), không có raw verdict/mức riêng từng finding. Bảng đối chiếu năm chủ đề được giao; không dựng thêm lời của connector.

| Chủ đề | Hồ sơ hiện tại xử lý thế nào | Phán xử và giới hạn |
|---|---|---|
| Lease “DA LAND” lúc 06:40 | YAML 177–184 trích câu sai, nói lúc ấy chỉ merged; lease giữ nguyên byte với ops ref | **Đính chính đúng biểu hiện lease**. Cả lớp còn L1 ở văn bản mới; không bắt sửa lease lịch sử. |
| Hậu-merge gate thiếu output | YAML 29–42, 143–155: run/job success chỉ điều kiện cần; output chưa đọc; landed false | **Đã sửa giới hạn lời khai**. Gate chưa được chứng minh, không tạo finding chỉ vì `not_measured`. |
| Required context | YAML 41, 119–121, 156–157: chưa đo; `mergeable_state: clean` không chứng minh non-required | **Đã sửa giới hạn lời khai**. Skipped giữ nguyên, không thành passed. |
| `anthropic_claude` vs `claude` (§7 enum) | YAML 10–16 dùng `provider: claude`, taxonomy tách `anthropic_claude`, giải thích ánh xạ | **Đúng schema/taxonomy hiện hành**. Parse YAML không phải validator transition. Không sửa provider của lease lịch sử. |
| Lệnh `ai-dang-giu` không tái lập | YAML 166–172 ghi `python3`, ba path, cwd scratch, origin và refs/heads | **Cách gọi/cwd đã sửa**: help rc=0; mode script **100644**; mã 2093–2096 dùng `Path(a.goc or ".")`. Không chạy quét vì gọi `ls-remote`; không dùng help chứng minh kết quả 489 refs. |

Run/job success, inventory **489** và `NGUOI_GIU` trong hồ sơ là lời khai Executor có neo/thời điểm. Sandbox 5 remote refs không tái lập phép quét lịch sử; không suy số 489 sai từ thiếu refs ở đây. Input `/tmp/review667-r4-input/github-readback.json` giữ mức lời khai, không là readback API độc lập của reviewer.

Theo dữ kiện user, Executor đã đăng comment **5866683767** đính chính comment **5865043852** trên #650. Ghi nhận đúng là **lời khai có neo**; không có raw body/receipt của correction trong JSON này và không GET lại. Không suy correction ấy đã đổi bytes YAML trên HEAD, không tạo finding chỉ vì reviewer offline chưa kiểm được comment.

## Lớp C — Quét toàn bộ văn bản mới và finding còn lại

Đã đọc trọn **226 dòng land YAML + 21 dòng erratum**, cả hai là tệp mới so base. `review_round4.py` xuất `claims-scan.txt` (**90 dòng khớp**) bằng lọc không phân biệt hoa/thường và dấu cho các từ về land/merge/complete/success/xanh/đạt/phép đo/suy ra. Bộ lọc chỉ giúp định vị; **không phải trần review hoặc validator ngữ nghĩa**. Kết luận dựa trên đọc toàn văn và đối chiếu Git/input. Lease và verdict nguyên văn lịch sử bị loại khỏi việc bắt lỗi trạng thái mới theo assignment, nhưng được kiểm integrity riêng.

### L1 — P1 — `landed-vuot-bang-chung`: câu hồi thuật “sau land” còn nằm trong hồ sơ mới

**Tệp:dòng:** `ops/land/pr666-wp650-land-evidence.yaml:224` (đọc hết câu tới 226); đối chiếu `:29`, `:35`, `:37–42`.

**Trích nguyên văn mâu thuẫn:**

> `(lease review_budget_ghi_chu, review_budget_ghi_chu_2), nhung khoi nang_tran nay CHI duoc ghi sau land, tai`
>
> `day (Codex #667 P2) — ghi muon, khai thang.`

Cùng tệp:

> `landed: false`
>
> Vi vay trang thai la `merged`, `landed` CON TREO; khong duoc dung tep nay de coi packet la landed.

Đoạn `nang_tran.ghi_chu` khẳng định một sự kiện **đã xảy ra**: khối này được ghi muộn, *sau land*. Đây là lời kể mới của PR #667, không phải trích nguyên văn được đánh dấu sai như `dinh_chinh_lease.cau_sai`. Mốc thực tế có bằng chứng là **sau merge PR #666**. Dùng “sau land” làm mốc đã hoàn thành vẫn ngụ ý packet đã vượt các điều kiện mà dòng 37–42 đang để thiếu. Caveat ở đầu tệp không làm hai lời kể hết trái nhau.

**Hậu quả và mức:** người đọc phần lịch sử nâng trần có thể hiểu #650 đã landed, trong khi packet còn treo trạng thái đó. Spec r5 dòng **249** dùng việc lát trước land làm điều kiện cấp lease cho lát sau. Xếp **P1 theo tiêu chí user** về hồ sơ khiến hạ nguồn hiểu việc chưa chứng minh là đã; không tuyên đã quan sát một transition sai thật trên GitHub. Đây không phải finding về thiếu CI evidence; sửa cách gọi sự kiện merge là đủ, không cần chạy thêm CI hoặc triển khai validator.

**Lệnh ĐÃ CHẠY và output:**

```text
python3 -B /tmp/review667-r4-output/review_round4.py
rc=0
K1_old_direct_claim=true
K1_current_direct_claim=false
K1_explicit_merged_not_landed=true
land_yaml_unchanged_since_r3=true
L1_current_sau_land=true
L1_already_at_r3=true
L1_already_at_r1=true
```

`packet_status` trong cùng output ghi `merged: true`, `landed: false` và toàn bộ điều kiện thiếu; script in nguyên văn các dòng mâu thuẫn. `rc=0` ở đây nghĩa là **thu facts thành công**, không phải consistency passed. `git diff 9a6f48f..HEAD -- ops/land/pr666-wp650-land-evidence.yaml` rỗng; finding là **sót biểu hiện cũ**, không đổ lỗi cho bản vá mới tạo ra nó.

**Đề xuất bốn phần:**

1. **Vá ở đâu:** `nang_tran.ghi_chu` dòng 224–225 của YAML, vì chính lời hồi thuật mới này đặt mốc hoàn tất sai. Khi rà cùng lớp, đọc cả câu “land dua tren quyet dinh…” ở 204 và gọi rõ thao tác đã thực hiện là merge; không cần sửa những tên schema/role/mục đích như `land_operator`, “ứng viên land”, “assurance land”. Dòng 204 đang bàn căn cứ thao tác, không được tách thành finding thứ hai chỉ từ chữ “land”.
2. **Vá thế nào:** mô tả khối được ghi **sau khi PR #666 merge tại `f8a7829…`**, giữ lời khai ghi muộn và mọi nguồn nâng trần; nếu nhắc trạng thái packet thì nối rõ tới `trang_thai_packet`. Giữ correction lease và erratum K1 đã đúng. Không dùng từ land trần làm mốc đã hoàn tất khi đang khai landed false.
3. **Ca khóa:** trên cùng exact HEAD, đối chiếu mọi câu thời điểm/trạng thái của hai tệp mới với landed false và checklist thiếu; câu hồi thuật “sau land” phải bị phát hiện, trong khi tên vai/schema, điều kiện tương lai và câu sai lịch sử được gắn nhãn không bị cấm. Đối chứng integrity phải giữ spec/hash, lease, verdict, A14 không đạt và nợ #669. Phép đo hiện tại đã tái hiện mâu thuẫn; **chưa chạy bản vá giả định**, không tuyên đã có validator ngữ nghĩa tự động.
4. **Rủi ro bản vá:** đổi `landed: true` để khớp câu sai hoặc sửa hàng loạt mọi chữ land sẽ làm nặng lỗi/mất lịch sử. Sửa lời hồi thuật tại nguồn là cách hẹp đủ xử lý biểu hiện này; triển khai validator thuộc #669, không phải điều kiện vá L1.

### Kết quả rà phần còn lại

| Phần đã đọc | Kết luận / giới hạn |
|---|---|
| YAML 27–42: `trang_thai_packet` | Tách merged/landed đúng; ba run, bốn mốc, required contexts và bookkeeping đều có trong checklist. Không biến miễn output thành miễn identity. |
| YAML 103–159: CI, `*_suy_ra`, `provenance_ghi_chu` | Giá trị bytes Git khớp; đã rút khỏi provenance. “XANH” ở 145 bị giới hạn ngay ở 145–146 là mức run/job, điều kiện cần. Không tạo finding vì thiếu output/context đã khai. |
| YAML 53–92: `noi_dung_readback` | Năm core quotes/metadata/timestamp khớp input. Hai câu provider/submitter không có trong tập trích input, full body không có: không khai đã kiểm 7/7 hoặc chứng minh human identity. Giới hạn MCP được ghi. |
| YAML 95–104: merge identity | Parents/tree/time khớp Git; authorized SHA là cha thứ hai của merge; ancestry rc=0. Câu “base không đổi từ lúc mở PR” là lời khai lịch sử, không suy từ tree equality; không quan sát GitHub timeline độc lập. |
| YAML 160–184: bookkeeping/correction | Đưa hồ sơ/lease vào master là việc PR này đang làm; không giả có sẵn ở base. Hai `cat-file -e origin/master:<path>` rc=128 xác nhận path vắng ở base. Lời “DA LAND” được trích làm câu sai rồi sửa rõ. |
| YAML 188–197: `CUNG-SESSION-…` | Khai đúng trùng session/trailer. “Session nay chi thuc hien thao tac merge…” phân biệt operator với auditor trong ngữ cảnh, không xóa việc chính session đó đã execute; câu “KHONG xoa vi pham” còn nguyên. |
| YAML 198–210 và erratum | A14 không đạt vẫn rõ; hai baseline/số numstat được phân biệt. Erratum toàn văn không còn khẳng định packet đã landed. Không đổi G5 disposition. |
| YAML 211–226: nâng trần | Trục vòng và lời gọi vẫn tách; ADR-0048 xác nhận trục vòng 10, không nâng trục lời gọi. Nguồn quyết định nâng 2→8 là lời khai có URL, không kiểm API. Câu mốc thời điểm ở 224 là **L1**. |
| Tên/role/ủy quyền land | Tên `HO SO LAND`, `role: land_operator`, mục tiêu/assurance land, quote cho phép merge không tự khẳng định packet đã landed. Không tạo finding chỉ theo token. |

### Integrity hiện vật và phạm vi `.gitattributes`

`cmp` với bản gốc ngoài checkout cho **cả ba full verdict rc=0**:

| Hiện vật | Bytes | SHA-256 khớp bản gốc |
|---|---:|---|
| `luot1-verdict-day-du.md` | 25298 | `1d1148283b54db965ec9c34ad2747c3dcf895d939441dcfd03516ca4dddfbd1c` |
| `luot2-verdict-day-du.md` | 23787 | `d377ba0d61628b9d8197f582f3d85bf7355eddac97bad981f0887645adf19cf6` |
| `luot3-verdict-day-du.md` | 27625 | `99b805a362d41bcfe2a953e410c5617b05f5e7f37c1d9b7d14f38e70a2a8597c` |

Hai script lượt 1 cũng khớp byte bản gốc (`review_delta.py`). Tệp `luot*-VERDICT.md` là lời kết ngắn kèm chú thích vận chuyển và con trỏ tới bản đầy đủ; không dùng chú thích ấy làm phép đo runtime reviewer. Script lịch sử phụ thuộc scratch/`run_checks.py` gốc, được giữ như evidence; bản chạy r4 chuyển mỏ neo ngoài checkout, không tự gọi các script lưu trữ là validator sản phẩm.

`.gitattributes` chỉ có hai glob `luot*-VERDICT.md` và `luot*-verdict-day-du.md` trong cây thư mục review này, gán `-whitespace`; không áp ra ngoài cây đó. `git check-attr` đo verdict được `whitespace: unset` nhưng vẫn `text: auto`, `eol: lf`. Đối chứng script/JSON/YAML cùng thư mục, land YAML, erratum và verdict ngoài thư mục đều `whitespace: unspecified`. Không nới whitespace sản phẩm hay EOL. `git diff --check` rc=0 được hiểu cùng phạm vi miễn trừ đã đo này.

## Lớp D — Phạm vi và nợ owner

| Nợ | Disposition hiện hành | Không được suy thành |
|---|---|---|
| **G5 / A14-KHONG-REVISION** | Owner **ducthangho**, quyết định 2026-09-28: ghi erratum cạnh spec; đã thực hiện. Giữ nguyên phán quyết lượt 3 theo assignment. | A14 của r5 đạt, revision đã được tạo hồi tố, hoặc lịch sử lệch được xóa. |
| **G6 / LAND-EVIDENCE-VALIDATOR** | Owner **ducthangho** quyết chuyển sang **#669**, con **#499**; YAML ghi tên, ngày và ngoài PR bookkeeping. Giữ nguyên phán quyết lượt 3. | Validator đã triển khai, Issue tồn tại là gate xanh, hoặc reviewer phải viết validator trong #667. |

**Không có P3 mở mới.** L1 thuộc lớp trạng thái G2, không phải lý do mở lại G5/G6. Các phần đã khai `not_measured` và rút khỏi kết luận không trở thành finding vì chưa đo được. Approval nội dung bookkeeping, nếu có sau này, cũng không tự chứng nhận #650 landed hay cấp quyền merge/land #667.

## Đã chạy

Harness `/tmp/review667-r4-output/run_checks.py` ghi argv/cwd/rc và SHA-256 stdout/stderr trong `commands.jsonl`; output thô nằm ở `.stdout`/`.stderr`. Python chạy `-B`, `PYTHONDONTWRITEBYTECODE=1`, cache trỏ ra scratch; `core.abbrev=7` qua môi trường, không ghi cấu hình checkout. Các lệnh đọc nguồn/diff bổ sung được dùng để đối chiếu nội dung, không gọi là test sản phẩm.

| Command / phép đo | rc và output dương | Phán xử |
|---|---|---|
| `git rev-parse HEAD HEAD^{tree} origin/master origin/ops/cap-lease-650` | **0**, khớp bốn OID đầu báo cáo | **passed**, identity local |
| `git diff --check origin/master..HEAD` | **0**, không diagnostic | **passed**, whitespace theo attributes đã đo |
| `git diff --name-status origin/master..HEAD`; `git diff --binary origin/master..HEAD`; `git diff 9a6f48f..HEAD` | **0**, 15 tệp toàn PR / 3 tệp delta | Thu scope/diff thành công |
| `git show origin/ops/cap-lease-650:ops/leases/c1a1a-exec-2-claude-20260927.yaml`, rồi `cmp ops/leases/c1a1a-exec-2-claude-20260927.yaml /tmp/review667-r4-output/lease-source.stdout` | **0/0**, cùng blob `b6d1d2febe989d1e089f6086c5b4b9b6f4de11b9` | **passed**, đúng byte lease |
| `python3 -B /tmp/review667-r4-output/audit_facts.py` | **0**; YAML khóa duy nhất **2/2**, spec/hash/write set/revision/generation khớp, workflow bytes **3/3**, parents/tree/time khớp | **passed** các phép đối chiếu local; không là provenance CI |
| `python3 -B /tmp/review667-r4-output/review_delta.py` | **0**; duplicate negative control: `duplicate key duplicate`; core quotes **5/5**, metadata/checklist/SHA khớp | **passed**, parse bắt khóa trùng và đối chiếu input |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | **0**, `đã quét 10 tệp, 0 chỗ chép doctrine` | **passed**, không chứng minh consistency ngữ nghĩa |
| `python3 -B .claude/dev/packet_loop.py adr-song --root .` | **0**, **50 ADR / 50 dòng**, khớp 1–1, ngoại lệ trạng thái 0016 | **passed** |
| `cmp ops/reviews/bookkeeping-650-pr667/luot1-verdict-day-du.md /tmp/review667-r1-output/VERDICT.md`; tương tự r2/r3 | **0/0/0**, ba băm/byte count ở bảng integrity | **passed** full verdict nguyên văn |
| `python3 -B /tmp/review667-r4-output/reproduce_findings.py` | **0**, hai session matches `True`; numstat như lớp A. Hai lệnh con `git cat-file -e origin/master:<land/lease path>` **128**, path vắng ở base | Thu facts thành công; không gọi rc=128 là pass của lệnh con |
| `python3 -B /tmp/review667-r4-output/review_round4.py` | **0**, K1 before/after, H1 đủ mốc, scan toàn văn, L1 còn đúng như trích dẫn | Thu facts thành công; **consistency failed bởi L1** |
| `python3 -B ops/lease_publish.py ai-dang-giu --help`; `git ls-files -s ops/lease_publish.py` | **0/0**, cú pháp path/`--root`, mode **100644** | **passed** phép kiểm cách gọi; quét thật **not_run** |
| `git check-attr whitespace text eol -- <10 đường đích/đối chứng>` | **0**, bốn verdict được miễn whitespace, sáu đối chứng không miễn; LF giữ nguyên | **passed**, phạm vi attributes |
| `git merge-base --is-ancestor bf63bb1ec485bccf8eec34cc5604f949d70fc7d6 f8a7829cc44f296c25faf1a6439b603ba840f70b` | **0** | **passed**, ancestry |
| `git config --local --get core.abbrev`; probe hiệu lực trong harness | **1**, không giá trị repo-local / **0**, `7` | Không gọi probe vắng là pass; override tiến trình được đo |
| Snapshot đầu/cuối: identity/status/diff/index/untracked/ignored/refs/full PR diff + nội dung | Xem khóa cuối bên dưới | Kiểm read-only ở hai mốc |

**failed / giới hạn lệnh đọc:** L1 là consistency failure nêu trên. Một lần đọc ADR bằng tên đoán `0048-tran-vong-review-canon-10.md` trả rc=1 (không có tệp); đã tìm bằng `rg --files` và đọc đúng `0048-tran-vong-review-len-muoi.md`, rc=0. Một lệnh `rg` tìm heading/list trong ba verdict ngắn không khớp, rc=1; không dùng kết quả đó làm gate. Không có required check nào được đổi từ skipped/không chạy sang passed.

**not_run:** mạng/fetch/GET GitHub và đăng verdict; tải CI logs/artifacts; quét `ai-dang-giu` 489 refs; fullCI/selftest sản phẩm/ma trận Python/Windows; Ruff pin/probe và bare lint; release/deploy; launcher doctor có probe mạng/credential. Đây là review bookkeeping, không nhận các suite 156/156 hoặc 162/162 trong hồ sơ là test vừa chạy ở r4.

**skipped theo lời khai input:** launcher/mở PR ở lượt PR, bốn Probe Windows trên job Ubuntu. Giữ skipped, chưa chứng minh non-required.

**not_measured:** CI Checkout/Workflow definition/Gate output đầy đủ; required contexts; raw body và danh tính human độc lập; inventory lịch sử; live PR head/base, trạng thái #669; body/receipt correction 5866683767; runtime model/effort độc lập của run này; allowance toàn lịch sử. Không dùng những phần này làm căn cứ landed.

Môi trường: Linux x86_64, `/usr/local/bin/python3` **3.11.15**, PyYAML **6.0.1**, Git **2.43.0**. Sandbox thực tế **workspace-write**, checkout chỉ đọc theo hành vi; không tuyên sandbox chặn mọi write. Snapshot nội dung gồm **2365 tracked paths**, cộng trạng thái untracked/ignored và thư mục ignored rỗng. Không snapshot repo nguồn ngoài checkout. So đầu/cuối chỉ chứng minh không có delta tại các mốc, không chứng minh chưa từng ghi rồi hoàn nguyên.

Băm input r4: `1f76f35926c41dd73228fb5e32266ee728d3fc45e69fe4cf25ee3815f3f79061`; land YAML: `11d4a5790ccbb9c1d8263163cbb12adf769e17b712a2ea5457d420daf5838b56`; lease: `3e1f52ca56a70826561fbafa07cf8eb6699fc2bb6ea24552550dccdab6248f65`; erratum: `8cc354174f41c9fdaae6ad575d72488209fdb623c784687200f28ff6e3491ac1`. Đây là băm bytes đã đọc, không xác minh nguồn GitHub. Verdict chưa được đăng/nhận assurance trong state machine và không là authorization merge/land.

Khóa cuối: **SNAPSHOT_UNCHANGED 9/9** (8 nhóm output Git và manifest nội dung); **2365 tracked paths** khớp băm, `.codex/` vẫn rỗng, full PR diff byte-exact. Lệnh snapshot cuối rc=0; HEAD/tree/base/ref lease không đổi. Không commit, push, mạng hoặc ghi checkout.
