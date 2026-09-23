# Đặc tả packet #523 — QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG, revision 14

## Identity, nguồn và quyền

- Packet `wp523`; mission499; revision14, generation14; class `sensitive`.
- Executor `openai_codex / codex_desktop / machine`, môi trường Windows local;
  WSL/Linux được dùng cho admission và kiểm offline. Không deploy/LIVE.
- Reviewer Codex phiên/context/checkout mới, yêu cầu model/effort cao hơn theo chỉ thị;
  không fork Executor. Khai model được yêu cầu riêng với serving identity đo được.
  Technical review cùng provider không được tự thành `cross_approved`.
- Final assurance `human_audited` trên exact candidate; audit r12 không áp sang r14.
- Nguồn quyết định: [projection chỉ thị owner](https://github.com/ducthangho/tra-luat/issues/523#issuecomment-5791146266).
  Người ghi là Codex, không tự khai đây là human audit hoặc dispatcher đã được activate.
- Thay r13 đã freeze tại `9f721e5311e2e8eef47a229c43be7376d8aaf2ca`; r13 giữ nguyên.
- Candidate kế thừa để sửa: `999cb6ee709128a06655c40f6273727f4f4c3eb1`; không đổi immutable baseline hoặc canonical continuation base.
  Giữ r1–r13 và draft cũ trong Git; không sửa hồ sơ đã giao.
- Nguồn kế thừa N1–N8/M1–M17: r11 tại `4a9c71a2e80b285679dd159e7a4efcb29a67a1a9`,
  `ops/specs/QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG-r11.md`, SHA256
  `42b0f477b7db2b1cb954ee9a345c9fcc1a2fb805ec9c260461187180fdc4226b`.
- Immutable acceptance baseline: `395bc7b1be6c275d8de697f8d8541bb36a290c9e`.
- Continuation base: `18d42cab74e80fc7635f754323fd13f520ccdcec` (canonical sau #568).
- Reviewed candidate: chưa có khi freeze spec; handoff phải ghi full SHA/tree thật.
- Spec nguồn là blob UTF-8 LF của chính tệp này tại OID được lease mới neo;
  SHA256 tính trực tiếp từ blob, không từ bản PowerShell chuẩn hóa xuống dòng.

Sáu trigger revision theo §3.2 là objective, acceptance, write set, dependency,
executor, environment. R14 thay acceptance/disposition M1/M7 và artifact path so r13;
generation14 thay lease13 đã hết hạn. Spec r13/hash/verdict giữ nguyên.

## Quyết định khắc phục WP523-R13-F01

Nguồn verdict: https://github.com/ducthangho/tra-luat/issues/523#issuecomment-5790944039.
Một lớp `con-tro-dinh-nghia-phan-hang-sai-dich`, hai biểu hiện M1/M7; P2, VÁ HỜ.
Không chia thành hai lớp hay xóa lịch sử `gop-dieu-kien-dung-review-class`.

- M1 GIỮ quyết định severity gốc và đặt đầy đủ ở protocol §8: P0 chặn mọi class;
  routine cần0P1 và ghi P2/P3 thành nợ có tên; systemic cần0P1/0P2, P3 thành nợ;
  sensitive cần explicit approval đúng assurance và quyết định từng finding còn mở.
  Class thiếu/không rõ xử như sensitive. Đây chỉ là ngưỡng severity, không tự cấp
  approval/land. Packet/chỉ thị chặt hơn thắng; #523 hiện cần0P1/P2/P3 và human audit.
- M7 GIỮ ba loại chi CI ở §12: gate tự động do event hợp lệ; phép đo có mục đích,
  allowance hữu hạn công bố trước; thăm dò chưa được cấp bị cấm. Loại xác định theo
  mục đích/authority, không theo tên event. Ghi used/reserved/limit, run ID/attempt,
  exact SHA và cửa sổ đo riêng; số chi lịch sử chưa biết không được ghi0. Không cấm
  workflow_dispatch được cấp. Chỉ thị hiện hành chưa cho chạy CI giữa các vòng vá.
- Bảng reconciliation r14 phải dẫn tới nội dung thật ở §8/§12; giữ bản r13 read-only.
- Phản chứng: cùng trạng thái0P0/0P1/1P2, nợ có tên nhưng chưa approve ở ba class;
  thiếu class; P0; packet chặt hơn; auto gate và hai dispatch khác mục đích. Xóa
  policy/conflation/unknown→0 phải bị phát hiện bằng semantic review hữu hạn.

## Outcome và phạm vi hữu hạn

Đưa hợp đồng bảng lớp và tín hiệu không hội tụ vào protocol; hai adapter chỉ dẫn
đúng mục và minh họa trình bày. Đối chiếu toàn bộ lịch sử để không nhập lại doctrine
sai của PR585. Không merge nguyên khối201 dòng của candidate27283d2.

Product branch mới `codex/wp523-r14-g14` kế thừa candidate r13 ở trên, so với continuation base. Write set exact:

1. `docs/PROTOCOL_DA_PHIEN.md`: chỉ §8 (bao gồm §8.3) và §12.
2. `.claude/skills/work-packet/SKILL.md`.
3. `.claude/skills/cross-review/SKILL.md`.
4. `ops/reviews/wp523-r14-reconciliation.md`: ledger/errata mới, không phải runtime.
Bản r13 đã có trong candidate kế thừa được giữ nguyên byte, không phải đường được sửa.

Ba tệp đầu là sản phẩm: ≤3 tệp, tổng additions ≤300 từ immutable baseline tới candidate.
Liệt kê toàn diff trước khi phân loại; không lọc để giấu đường ngoài tập. Ledger là
review artifact, theo phân biệt r11/ADR-0044; vẫn phải audit nội dung và báo numstat
riêng. Không cộng các khoảng diff chồng nhau hoặc bỏ phần giải conflict.
Diff baseline→continuation của ba tệp sản phẩm hiện rỗng. Với các tệp canonical
kế thừa khác, lưu nguyên danh sách baseline→candidate và baseline→continuation,
ghi rõ inherited; artifact r13 kế thừa được liệt kê riêng; bất kỳ sửa mới ngoài scope trong r13→candidate đều
bị chặn. Việc phân loại inherited không dịch baseline nghiệm thu sản phẩm.

Metadata authority branch `codex/wp523-r14-authority`, exact:

- `ops/specs/QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG-r14.md`;
- `ops/leases/quy-trinh-lap-review-r14-g14-codex.yaml`.

M11 metadata trên branch riêng `codex/wp523-r14-evidence` (không đổi product head):

- `ops/reviews/wp523-r14-review-1-codex-verdict.md`;
- `ops/reviews/wp523-r14-review-1-codex-verdict.receipt.yaml`;
- `ops/reviews/README.md`: chỉ thêm hàng mục lục cho verdict mới, giữ hàng cũ.

Review artifact chưa tồn tại không được khai đã validate. Nếu cần thêm vòng, phải
đối chiếu budget/authority và khai exact artifact paths trước ghi; không wildcard
ghi đè hồ sơ cũ. Bản evidence có review/land riêng theo scope, không tự ghép vào
product candidate sau audit. Chưa tích hợp M11 thì không gọi toàn bộ #523 complete.

Không sửa `.github/**`, hooks, launcher, validator, packet_loop/doctrine-scan,
runtime pháp luật/corpus, release metadata hoặc lease gen11/12. Chưa activate
change-impact policy tự động; effective scope ở đây là các exact paths đã khai,
không tự tạo một closure máy chưa có. Holder toàn kho phải đo trước quyền ghi.

## Tập lịch sử và disposition

Nguồn PR529: chín receipt nguyên byte tại `9683d5006e47d01e38e9ed21697911384cd80007`,
`ops/reviews/pr529-review-{1..9}-codex-verdict.receipt.yaml`. Union `findings_ids`
có17 slug; không cộng thành17 lỗi đang mở. Giữ reviewed SHA, vòng, hash, classification
do lượt cũ khai riêng với phép kiểm hiện tại. Không nâng narrative thành execution.

Nguồn mới nhất: PR585 review5268688511 trên27283d2; PR587 review5268796536 trên0babf61;
PR586 review5270670271 trên816efab; PR597 review5269392593 trên2babb1a. Ledger phải ghi
full OID và comment ID cho từng finding. Đây là23 thể hiện từ bốn review; 13 mục
L-A…L-M chỉ bao phủ585/587. Không suy23 lớp độc lập hoặc coi thiếu kết quả là sạch.

Disposition bắt buộc:

- L-A/B/C/D/F/G: giữ canonical về human assurance, exact-head, P0, remote fence và CI
  được cấp quyền; bỏ nhập các câu sai của585. Đây là tránh nhập lỗi, không phải tuyên
  bố sửa lỗi đã deployed. Không lặp khẳng định âm về #512 khi thiếu run IDs.
- L-E/H: phân biệt lớp/thể hiện, khóa slug, mẫu số0, lớp mới và tín hiệu không hội tụ.
- L-I/J/K/L/M: baseline không dời; lease mới neo spec OID/hash; expiry từ run profile
  được công bố trước; không sửa sai gen11/12 hồi tố, không dùng line number trôi làm neo.
- #586: kiểm đúng PR head/synthetic parents/tree; hợp đồng mới ở revision mới.
- #597: ghi errata theo từng comment, phân biệt graph thực với suy đoán squash,
  bằng chứng model/actor, mẫu số trong/ngoài canonical, hash đúng blob, mỏ neo bền,
  LF chưa biết tầng gây đổi, một parent không chứng minh không squash, số execution
  khác số OID. Giữ nguyên chữ ký/audit/receipt lịch sử.

Bốn lớp unresolved mà canonical §8.3 đã bảo toàn không tự đóng nhờ r14. Đặc biệt
`phep-do-doctrine-khong-du-rang`/alias runtime theo #583, identity signer theo #566,
historical bookkeeping theo #582 vẫn là nợ có tên. Không sửa scanner ở packet này;
không ghi scope-cut là VÁ THẬT; land slice này không đóng các issue nợ hoặc mission499.

## Nghiệm thu của revision14

| ID | Nghĩa vụ và bằng chứng cần có |
|---|---|
| A1 | Đủ từng M1–M17 và N1–N8 trong reconciliation với giữ/sửa/successor/chưa đo cùng nguồn; không chỉ M1–M10. |
| A2 | Bảng lớp toàn phần: từng finding vào đúng một slug, nhiều biểu hiện không nhân số lớp; có phương án theo lớp hoặc lý do phải vá riêng. |
| A3 | Reviewer độc lập phân từng finding trước thành ĐÃ VÁ THẬT/VÁ HỜ/VÁ SINH LỖI MỚI/CHƯA VÁ, với command/evidence và phần chưa đo; thiếu quan sát không là đạt. |
| A4 | Tỷ lệ chỉ dùng tập lớp mở của vòng trước, một lớp chỉ fixed khi mọi biểu hiện trong scope được kiểm và không sinh lỗi cùng cơ chế. Mẫu số0 là N/A. Hai tỷ lệ liên tiếp <50% tạo checkpoint; lớp mới được đếm riêng, tỷ lệ cao không là approval. |
| A5 | Lớp lặp vòng thứ ba đòi xem lại cách làm; nhiều finding cùng lớp trong một vòng không thành ba vòng. Không nâng/reset các budget độc lập. |
| A6 | Open P0 luôn chặn approval; điều kiện severity/class/assurance của Packet và §8 vẫn áp riêng; packet này cần0 P1/P2/P3 trong candidate scope và final human audit. |
| A7 | Adapter mỏng, mỗi con trỏ mới có khái niệm thật tại đích; semantic đọc cả prose/YAML để tránh luật đã rút còn điều khiển. Doctrine-scan xanh chỉ có độ phủ thực của nó. |
| A8 | Ledger bảo toàn17slug,13L-ID và đủ23comment mới, exact source/hash; errata tách phép đo mới, thuật lại và chưa đo. Không sửa hiện vật cũ. |
| A9 | Whole diff/write set/EOL/numstat từ immutable baseline;3productfiles≤300adds; không dời baseline bằng gia hạn. |
| A10 | Targeted checks thật, rc/positive output, reviewer tự dựng phản chứng; không lấy test của executor làm review độc lập. |
| A11 | CI plan khi ready: canonical code admission trong WSL/Linux; required Ubuntu và Windows theo §10.1/spec, full sau technical review, exact identity/provenance; không thừa hưởng waiver568. |
| A12 | M11 raw verdict/hash/receipt v2/index giao Git và readback; budget và số CI đã chi/run IDs/cửa sổ đo khai riêng; thiếu lịch sử là KHONG_DO_DUOC, không phải0. |

N1/N4 áp lên bất kỳ công cụ phản chứng mà executor/reviewer dùng: tiêu chí đích phải
đỏ vì đúng tính chất, các quan sát không-đích đủ và đối chứng có thể lật kết luận.
N2 yêu cầu xét đơn vị nghĩa, vị trí kề một khối được phép không hợp thức hóa nó.
N3 ở A9; N5 ở A7; N6 ở A12; N7/N8: văn bản không đủ dựng thước hoặc không đo được
thì blocked/not_measured, không approve. N1 không yêu cầu xây lại scanner ngoài scope;
độ phủ scanner chưa được đóng và không được dùng làm tiền đề approval.

Reviewer tự dựng các tình huống tối thiểu: nhân bản biểu hiện cùng slug; previous
empty; high ratio kèm lớp mới; cắt phạm vi; lớp thứ ba qua nhiều vòng; target đỏ do
setup; thiếu đối chứng; con trỏ sai mục con; head đổi nhưng tree bằng; old audit
không chuyển SHA; receipt ngân sách0 nhưng chi chưa đo. Các tình huống là nghĩa vụ
kiểm, chưa là lời khai đã chạy; không dùng số từ scanner làm oracle cho ngữ nghĩa.

## Budget, deadline và handoff

Run này07:51:19Z–09:21:19Z23-09-2026, absolute90phút. Lease14 không vượt deadline.
Chỉ thị owner tiếp tục sau checkpoint được ghi tại comment5791146266 (agent projection).

```yaml
nang_tran:
  ai_nang: ducthangho
  can_cu: https://github.com/ducthangho/tra-luat/issues/523#issuecomment-5791146266
  tran_cu: two Codex review calls on the585 workstream, reached
  tran_moi: continue until zero P1/P2/P3 under owner instruction; reserve one call at a time
  numeric_limit: not specified by owner
```

Không suy ra một con số owner chưa cấp. Override theo điều kiện này chỉ cho tiếp tục
vòng vá/review như owner yêu cầu; không reset lịch sử, không bỏ deadline/hard quota/
permission/scope. Known calls585=2 trước r14; reserve1 kế tiếp. PR529 có9receipt nhưng
số invocation lịch sử chưa đo đủ. Attempts/same-failure override lịch sử giữ nguồn
comment5646812840; cơ chế lặp phải được xem lại theo lớp, không lặp prompt/bản vá cũ.
Mỗi review mới dùng context độc lập; không tái dùng reviewer từng sinh hint để tự duyệt.

CI/fullCI chưa chạy trong vòng vá. Khi sạch findings, lập plan hữu hạn trước gọi,
kiểm admission và exact identity; không dùng thiếu lịch sử để nhận remaining allowance.
M11 raw verdict/hash/receipt/index là stage giao evidence riêng, không ghép vào product
head sau audit. Exact artifact paths cho vòng r14 đầu đã liệt kê; vòng sau phải khai
finite paths trước ghi. Human audit/land không được tự cấp từ technical review.

Handoff §7 neo spec hash/generation/base/head/tree, tests và debt. Executor không
chuyển vai reviewer/approver/land trong run. Stale identity/lease, ngoài scope, quota,
thiếu evidence hoặc hết deadline thì handoff. Đổi hợp đồng freeze cần revision mới.
