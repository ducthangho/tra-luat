# WP523 r14 — independent Codex technical verdict

**VERDICT: APPROVE — 0 P0 / 0 P1 / 0 P2 / 0 P3 trong candidate scope.**

Candidate đủ điều kiện chuyển sang CI plan và các bước evidence được cấp. Đây là technical review với assurance `advisory_review`; không cấp `cross_approved`, `same_provider_approved`, `human_audited` hoặc quyền merge/land. M11 delivery, admission, required CI và final human audit vẫn chưa hoàn tất. Không có finding chưa công bố.

```yaml
reviewed_sha: 15d1b103e8d4dec60f96049eb5ad9b16d436d63f
reviewed_tree: 075b11fd72867138c429eb09f403fd0dd704781c
verdict: approve
assurance: advisory_review
review_axes: [spec, standards_security]
provider: openai_codex
execution_surface: codex_desktop
transport: machine
reviewer_session: /root/review_wp523_r14
requested_model: gpt-6-astra
requested_effort: max
actual_serving_model: KHONG_DO_DUOC
actual_serving_effort: KHONG_DO_DUOC
```

Đây là context mới, không fork Executor và không tái dùng tác giả hint r13. Không có telemetry độc lập chứng minh model/effort đang phục vụ hoặc mức cao hơn Executor. `codex-cli 0.155.1` là version probe của CLI cài trên máy, không chứng minh model của subagent này. Phần còn thiếu ấy không được biến thành lời khai assurance.

## Identity, authority và phạm vi

- Immutable baseline: `395bc7b1be6c275d8de697f8d8541bb36a290c9e`.
- Canonical continuation: `18d42cab74e80fc7635f754323fd13f520ccdcec`.
- Candidate r13: `999cb6ee709128a06655c40f6273727f4f4c3eb1`.
- Authoritative spec: `80cca6f08e1c23b4738fb9467ef466860a3a24e2:ops/specs/QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG-r14.md`, 14,612 bytes, SHA256 `f36696109983d6ff607e4f20db24933f91982432f50b6ba65165da718e9bbccb`.
- Lease source: `45bcb02d0f6e117ab749dc269bef64fef6c0200c:ops/leases/quy-trinh-lap-review-r14-g14-codex.yaml`; spec/revision14/generation14 khớp. Deadline `2026-09-23T09:21:19Z`.
- Đã đọc lại owner continuation comment `5791146266` và lease readback `5791207727` qua GitHub API. Chúng khai rõ agent projection, không phải human audit. Chỉ thị trực tiếp của assignment cho phép lượt review này sau checkpoint; không suy authority từ actor đăng.
- Remote fence đầu/cuối giữ đúng product H, canonical C và authority OID trên. Spec blob r11 kế thừa cũng khớp SHA256 `42b0f477b7db2b1cb954ee9a345c9fcc1a2fb805ec9c260461187180fdc4226b`.

Đã liệt kê **toàn diff trước khi phân loại**. Baseline→candidate có 9 đường: 3 product paths **+79/−1**, r13 ledger +148, r14 ledger +168 và 4 đường inherited canonical. Bốn đường `ops/lease_publish.py`, `ops/lease_publish_test.py`, `ops/nhanh_don_duoc_test.py`, `ops/specs/dang-lease-dau-truoc-kiem-sau-r1.md` byte-identical với canonical C; không có overlay mới của r14 trên chúng. Không dùng việc phân loại inherited để dời baseline.

Product diff: protocol +68 ở §8/§8.3/§12; cross-review adapter +8/−1; work-packet adapter +3. Delta r13→r14 chỉ protocol +33 và ledger r14 mới. R13 ledger giữ nguyên byte. Cả 5 tệp product/ledger có LF, không CR; hai frontmatter adapter không đổi. Phạm vi mã canonical inherited được xác minh identity, không được tuyên bố là một review chức năng mới của #568.

## ĐỐI CHIẾU LƯỢT TRƯỚC / BẢNG LỚP

Raw verdict r13 đọc lại có SHA256 `35e961c83ed6d94181790cbb15e58513f81a03e20e6e1872c7c58cea7eafb274`.

| Slug lớp | Biểu hiện trước | Phân loại r14 | Bằng chứng độc lập |
|---|---|---|---|
| `con-tro-dinh-nghia-phan-hang-sai-dich` | F01a — M1 | **ĐÃ VÁ THẬT** | §8 nay có bảng severity phân biệt routine/systemic/sensitive, class thiếu, P0, ngưỡng Packet chặt hơn và assurance riêng. Ledger M1 trỏ tới quyết định thật. Cùng trạng thái một P2 phân biệt được ba nhánh. |
| cùng slug trên | F01b — M7 | **ĐÃ VÁ THẬT** | §12 nay có đủ ba loại chi theo mục đích/authority, allowance hữu hạn, used/reserved/limit, run/attempt/SHA, cửa sổ và lịch sử unknown. Hai dispatch cùng event nhưng khác mục đích được phân biệt; dispatch được cấp và lệnh owner hoãn CI đều được giữ. |

Đây là **1 lớp, 2 biểu hiện**, không phải hai lớp mới. Không tìm thấy biểu hiện mới cùng cơ chế do sửa hai bảng. P0, exact-head, human audit và CI được cấp không bị làm yếu. Slug lịch sử liên quan `gop-dieu-kien-dung-review-class` giữ riêng, không bị đổi tên hoặc tính lặp.

Trong đúng candidate scope của verdict r13: U = {slug F01}, F = U, tỷ lệ 1/1. Kết luận approve dựa trên toàn bộ kiểm Spec/Standards và không còn finding trong scope, không suy từ tỷ lệ. Bốn lớp lịch sử unresolved và các nợ #582/#583/#566 vẫn giữ trạng thái riêng, không được tính thành đã vá bởi slice này.

## Kiểm Spec và Standards

| Nghĩa vụ | Kết luận trong phạm vi review |
|---|---|
| M1/M2 | Severity có quyết định thật; sensitive vẫn cần explicit approval đúng assurance. #523 áp ngưỡng riêng 0 P1/P2/P3; final human audit còn pending. |
| M3/M4 | Một slug cho mỗi finding, biểu hiện và lớp đếm riêng; phương án chung hoặc lý do vá riêng; lần thứ ba tính theo lượt khác nhau và buộc checkpoint. |
| M5/M6 | Mẫu số là tập lớp mở vòng trước; mẫu số 0 là N/A; không nối low-ratio qua N/A; scope-cut/chưa đo/biểu hiện mới cùng cơ chế không thành fixed. Lớp mới báo riêng; high ratio không là approval. |
| M7–M10 | Purpose-based CI không cấm dispatch được cấp, không tự tạo authority; remote/exact-SHA/hậu-merge gate giữ nguyên. Full CI hoãn theo chỉ thị, không khai pass. |
| M11/M12 | Ledger nói đúng delivery chưa xong và lịch sử chi chưa đo. Raw output hiện giao recorder; receipt v2/index/readback còn pending, chưa chấm là hoàn tất. |
| M13–M17 | Adapter chỉ thêm con trỏ/cú pháp bảng, không chép policy. Đã đọc đích §7/§8/§8.3/§12 và current spec/lease theo nghĩa; không thấy luật đã rút được cấp lại. Reviewer tự dựng thước, không lấy targeted output Executor làm oracle. |
| N1/N4 | Các source mutants có target, đủ non-target observations và cả positive/negative controls; setup-red, always-green, always-red, thiếu observation và đối chứng hỏng đều bị từ chối. |
| N2/N3/N5 | Đọc từng đơn vị nghĩa trong toàn product diff; giữ nguyên phạm vi trước lọc; nguồn/đích thực được đối chiếu, có nested-section và line-wrap controls. Phân loại hình thức không thay semantic review. |
| N6–N8 | Chi của cửa sổ reviewer tách khỏi lịch sử; unknown không đổi thành 0. Không có nghĩa vụ nội dung candidate còn thiếu quyết định để dựng thước; các stage evidence chưa thực hiện được ghi riêng. |

Các kiểm có thể tái lập trong `semantic_probes.py`, `semantic-results.json`, `semantic-binding.json`, `mutation-evidence.json` và `source-audit.json`. **68/68** là số scenario hữu hạn, không phải số lỗi hoặc số policy được runtime cưỡng chế. Bốn source mutants nhắm M1/M7 đều làm tiêu chí đích đỏ trong khi giữ đủ non-target controls. Mô hình do reviewer đọc và diễn giải thành quyết định; exact-clause guards chỉ neo bản diễn giải vào text này, không là bộ suy nghĩa tổng quát. Nợ scanner #583 không bị đóng.

Đã thực thi phản chứng Git thật trong scratch: một commit thông thường và một `git merge --squash` đều có một parent, cùng tree nhưng khác commit OID. Điều đó khóa hai suy luận sai: một parent không xác định merge method, tree bằng không chuyển exact-SHA approval.

## Lịch sử và errata

- Chín receipt PR529 từ `9683d5006e47d01e38e9ed21697911384cd80007`: **9/9 receipt hash, 9/9 raw verdict hash khớp**; union đúng 17 slug và khớp bảng ledger.
- GET lại bốn review objects và **23 comment** PR585/586/587/597: full API reviewed SHA và từng comment ID có trong ledger. Raw JSON và body hashes được lưu riêng; 23 comment không được coi là 23 lớp độc lập.
- Các lỗi human-route/exact-head/P0/dispatch/ratio của draft585 không bị nhập lại. Đây là tránh nhập lỗi của draft, không phải tuyên bố sửa lỗi deployed.
- 597-D: các blob đo lại đúng 4,606/5,333/5,333 bytes và đúng ba hashes trong ledger. 597-A: anchor `5c9abef…` là ancestor của API head thật `2babb1a…` (rc0). Reviewed draft `27283d2…` không thuộc canonical C (rc1).
- Hai synthetic OID `97f149ad…` và `4895b646…` không có object trong clone (rc128); không nhận lỗi đó thành kết luận ancestry, không chuyển finding trên chúng sang PR head thật. Không đo lại protected archival policy, partition lịch sử toàn kho hoặc tầng transport làm đổi final-LF.
- #582/#583/#566, bốn lớp unresolved được bảo toàn trong §8.3, invocation/CI lịch sử chưa đủ dữ liệu vẫn là nợ/unknown. Không sửa receipt, audit, spec hoặc lease cũ.

## Kiểm tra đã chạy

| Command/scope | Rc và bằng chứng | Trạng thái |
|---|---|---|
| `python -B .claude/dev/packet_loop.py --state-dir <scratch>/state doctrine-scan --root <clone>` | rc0; 10 tệp, 0 bản sao bị scanner phát hiện | passed trong độ phủ scanner |
| cùng tool `adr-song --root <clone>` | rc0; 50/50 ADR, exception0016 được khai | passed |
| `python -B scripts/tl.py doc-claims-check --strict --json` | rc0; ok=true, 110 files, 0 hard flags, 381 advisories | passed scope mặc định; ops ledger đo riêng |
| `git diff --check B H` | rc0, không lỗi whitespace | passed |
| `loi_ruff_ci()` | rc0; `RUFF_CONTRACT 3 []` | passed pin/probe contract |
| Ruff0.15.20 `check --no-cache --select F scripts/tl.py` | rc1, 12 F821; canonical baseline run cũng rc1, input và output byte-identical | **failed bare lint; delta0** theo CLAUDE.md |
| `semantic_probes.py` | rc0; 68/68, 4 source mutants đủ target/non-target/controls | passed hữu hạn |
| `audit_sources.py` cuối | rc0; 9 receipt hashes,17 slug,23 comment; EOL/frontmatter/scope và topology được đo | passed |
| Admission, full CI, Windows/Linux full gates, final human audit, land | Reviewer không chạy | not_run |

Commands/rc/hash chi tiết ở `command-evidence.json`, `targeted-commands.json`, `source-audit-commands.json`, `sources-commands.json`, `historical-verdict-hashes.json`. Mọi cache/temp/fixture nằm ngoài checkout.

Hai lỗi ở harness của reviewer được giữ lại: lần đầu parser giả định `findings_ids` toàn string nên rc1 khi gặp mapping; lần kế trích bảng chưa giới hạn section nên nhận nhầm ba OID ở bảng hash vào tập slug. Đã đọc dữ liệu thật, giới hạn đúng section và chạy lại thành 17/17. Đây là lỗi setup/phạm vi của phép đo reviewer, không phải product finding hoặc mutant chết đúng tiêu chí; hiện vật đầu ở `reviewer-harness-first-attempt.json` và `source-audit-unbounded-extraction.json`.

## Snapshot, budget và bàn giao

Bootstrap snapshot khớp **2,142/2,142** file trước review. Snapshot cuối: **0 file đổi/thêm/xóa; HEAD/tree, working/index diff, tracked/untracked/ignored và local refs giữ nguyên**. Remote H/C/authority cũng không đổi. Kết quả ở `snapshot-comparison.json`. Snapshot hai mốc không chứng minh chưa từng có ghi rồi hoàn nguyên; filesystem là `danger-full-access`, read-only bằng role discipline. Không đọc/snapshot root repo D:/ ngoài assignment.

Known585 calls trước run=2, lượt này là call3 theo owner override5791146266; reviewer không gọi model/subagent khác. Tổng invocation lịch sử chưa đo đủ, không reset; không bịa trần số owner chưa cấp. Reviewer không dispatch CI, run IDs trong cửa sổ review là []; lịch sử CI toàn packet vẫn `KHONG_DO_DUOC`. Claim407 lease của preflight nguồn không được reviewer tái lập trọn scope và không dùng làm quyền ghi.

Recorder tiếp tục giao nguyên raw verdict/hash, receipt v2 và index trên evidence branch/path r14 đã cấp; đọc lại byte/hash sau vận chuyển. Sau technical readiness, lập CI plan hữu hạn, chạy canonical-code admission và required CI đúng identity, rồi final human audit/land theo authority riêng. Head đổi làm verdict này stale. M11 chưa tích hợp thì không gọi toàn bộ #523 complete; land slice cũng không đóng mission499 hoặc các nợ lịch sử.

Finished UTC: `2026-09-23T08:30:19.338558+00:00`.
