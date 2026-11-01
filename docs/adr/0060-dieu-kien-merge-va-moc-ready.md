# ADR-0060 — Điều kiện merge, mốc bỏ draft và làn sổ sách

- **Trạng thái:** Accepted (2026-10-31, chủ kho `ducthangho` duyệt `spec_hash` `614f9eec…afbe5` của đặc tả packet
  ở Issue #1085 issuecomment-6543878208 — tệp định danh bằng băm, tìm theo Issue ấy; thi hành bằng packet
  `DIEU-KIEN-MERGE-VA-SO-SACH` revision 1 · generation 1 — không phải một phiên tự đặt quy ước)

ADR này là luật **độc lập**. Nó không kích hoạt, không sửa và không mượn hiệu lực của `ADR-0054`; chỗ nào hai ADR
nói cùng một việc thì packet áp ADR này đọc ADR này. Mục tiêu của chủ kho: quá trình vá → push → merge → land → ghi
sổ → đóng WP phải nhanh, không bước thừa, vẫn an toàn.

## Vì sao — số đo 31-10-2026

| # | sự kiện | số đo | hệ quả |
|---|---|---|---|
| S1 | luật merge cũ | bảng ngưỡng §8 cho P3 (và P2 ở `routine` chưa áp `ADR-0054`) thành nợ do agent tự ghi | lỏng hơn chỉ thị chủ kho |
| S2 | Windows local | `ADR-0057` §2: chỉ áp khi đã chạy; máy offline thì không áp | lỏng hơn chỉ thị chủ kho |
| S3 | `ADR-0054` | "CHƯA KÍCH HOẠT", chờ #812–#816 (Issue #814, #816 còn `open`) | luật đã viết mà không áp |
| S4 | mốc bỏ draft | không luật nào; "draft" chỉ xuất hiện ở draft land PR của mission | — |
| S5 | PR mở tự động | `ops-open-pr.yml` chạy `gh pr create` không `--draft` | PR ra đời ở trạng thái ready |
| S6 | PR sổ sách | 79 PR tiêu đề `land(`/`ghi-so(`/"ghi sổ" từ 24-10 đến 31-10 | đơn vị: PR |
| S7 | ghi sổ đệ quy | #1050→#1056→#1060, #1058→#1071→#1075; #1056 và #1060 thêm 14.778 dòng | ghi sổ sinh ghi sổ |
| S8 | PR sổ sách chạy Windows đủ | #1071 chỉ chạm `ops/reviews/**`: 35 check run; `gate-packet-loop (windows-latest)` 84 phút | `workflow_dispatch` luôn `day_du` |
| S9 | PR "duyệt landed" | #949, #951, #953, #956; mốc Workflow definition cần GraphQL, 403 trong phiên web | chờ người làm cầu nối dữ liệu |
| S10 | connector tự bắn khi bỏ draft | `ops/reviews/wp461-review-1-codex-verdict.receipt.yaml`: `auto (Draft marked ready…)` | xung đột với "xong connector rồi mới bỏ draft" |
| B1 | git bundle sang Windows | `tra-luat-win`: bundle 882 byte, H/tree/cha khớp, `adr-song` rc=0, 28 s | đường đưa ứng viên chưa push sang máy Windows |
| C1 | connector trên PR draft | PR #1084: `@codex review` lúc ~13:04Z, review 5722826710 neo đúng head lúc 13:07:45Z | connector chạy được khi còn draft |

Số đo B1 và C1 ở phụ lục §8 và §9 của đặc tả.

## Quyết định

**M1 — Severity.** Điều kiện merge: 0 finding P0, P1, P2 mở. Mỗi P3 hoặc **đóng có bằng chứng** (reviewer xác nhận
theo bảng lớp §8.3), hoặc **chủ kho miễn** bằng một comment nêu slug finding, SHA, lý do và hướng xử lý. Trước push,
comment miễn đăng trên Packet Issue, neo SHA ứng viên cục bộ (M12); sau push, đăng hoặc dẫn lại trên PR. Quyết định
miễn neo SHA nào chỉ có hiệu lực cho đúng SHA ấy. Agent không tự ghi nợ P3. Cấm giảm số lớp bằng gộp slug hoặc đổi
hạng. Điều kiện dừng theo P3 chỉ xét khi đã hết P0–P2 và vòng đang xét là vòng vá thêm vì P3: vòng ấy không giảm số
lớp P3 thì dừng, checkpoint chủ kho. Vòng vá P0–P2 không bị điều kiện này chặn, kể cả khi số lớp P3 là 0 → 0. Mọi
điều kiện dừng và trần khác giữ nguyên. Với packet áp ADR này, M1 thay bảng ngưỡng §8; P0 vẫn chặn như cũ.

**M2 — Review theo lớp.** Reviewer khái quát mỗi biểu hiện thành một lớp nguyên nhân và quét mọi biểu hiện cùng
lớp trên candidate trước khi báo. Cách ghi (slug, bảng lớp, tỷ lệ đóng lớp) giữ nguyên §8.3.

**M3 — Windows.** Phân loại theo thứ tự, dừng ở bước đầu tiên khớp:

1. PR thuộc làn lưu trữ (M8) ⇒ `not_required`.
2. `required` khi diff chạm `*.ps1`, `*.cmd`, `*.bat`, `*.sh`, `scripts/deploy-*`, `.claude/dev/**`,
   `.github/workflows/**`; hoặc thêm/sửa dòng chứa `os.name`, `sys.platform`, `platform.system`, `subprocess`,
   `encoding=`, `os.sep`, `pathlib` trong tệp mã (`*.py`, `*.ps1`, `*.sh`, `*.yml`; không xét `*.md` và bản ghi
   thụ động); hoặc đặc tả khai `windows: required`.
3. `not_required` khi mọi tệp của diff là `*.md`, hoặc nằm trong `docs/**`, `ops/land/**`, `ops/reviews/**`,
   `ops/specs/**` mà không phải `*.py`, `*.ps1`, `*.sh`, `*.cmd`, `*.bat`.
4. Còn lại `unknown`: reviewer phải chốt `required` hoặc `not_required` kèm lý do trong verdict. `unknown` chưa chốt
   thì chặn.

Reviewer được nâng mức; agent không được hạ. `required` ⇒ chạy trên máy Windows của chủ kho qua Desktop Commander
theo `ADR-0057`/`0058`/`0059` (khoá, kiểm tải, cô lập, sổ đo). Lượt này cộng thêm vào Windows CI, không thay.

"Xanh" đòi đủ ba điều, theo thứ tự:

- (a) hai lượt (SHA nền và ứng viên), cùng máy, dựng trong cùng một lệnh; mỗi lượt chạy trọn tập test bắt buộc và
  có danh sách test ID kèm kết quả. Thiếu lượt, thiếu báo cáo, lỗi setup, hoặc test bắt buộc bị `skipped`/`not_run`
  ⇒ không xanh. Ứng viên chạy 0 test ⇒ không xanh.
- (b) tập test ID đỏ trên ứng viên nằm trong tập đỏ trên nền.
- (c) ca đỏ thuộc tệp trong write set ⇒ chủ kho quyết.

Máy không `Online` trong `list_devices`: hết hạn báo thì báo chủ kho; hết hạn chờ thì packet sang `blocked` (hai hạn
ở mục *Tham số*). Không tự miễn. Với packet áp ADR này, điều này thay câu "máy offline thì vế này không áp" của
`ADR-0057` §2.

**M4 — Đưa ứng viên sang Windows.** Clone nền từ GitHub trong thư mục riêng của phiên, nhập git bundle của ứng viên,
kiểm commit, tree và cha khớp từng hash, rồi mới test. Căn cứ: B1. Bundle lớn chia nhiều lần ghi; trần kích thước
chưa đo.

**M5 — Push.** Nhánh code đẩy một lần chính, sau khi review offline approve và gate trước push đạt trên đúng SHA.
Mỗi lần push thêm cần checkpoint chủ kho và một dòng biên nhận (SHA trước/sau, lý do); số lần tối đa ở mục *Tham
số*. Quá số ấy ⇒ đóng PR, mở generation mới. Không không gian tên nào được miễn đếm.

**M6 — Draft và đề xuất merge.** PR mở ở draft. Khi chưa đủ mọi điều kiện, cấm cả bốn: bỏ draft; nói "sẵn sàng
merge" hay "có thể merge" ở bất kỳ đâu; gọi merge; bật auto-merge. Báo theo mẫu
`CHƯA ĐỦ ĐIỀU KIỆN MERGE: thiếu …`, liệt kê từng điều kiện còn thiếu.

Điều kiện bỏ draft:

- bằng chứng CI đáp ứng §10.2.2–§10.2.3 trên đúng head; mốc bắt buộc chưa đo được phải ghi thiếu và tiếp tục chặn,
  trừ waiver hợp lệ theo protocol;
- connector đã review đúng commit (dòng `Reviewed commit:` cho đúng SHA) và các finding của nó đã được đọc;
- M1 đạt; M3 đạt nếu `required`;
- PR head bằng SHA đã approve.

Commit mới ⇒ PR về draft.

Cách gọi connector có hai trạng thái theo C1. **C1 ĐẠT (hiện hành):** gọi bằng comment `@codex review` khi PR còn
draft; lượt connector tự động khi bỏ draft trên cùng SHA không mở vòng mới, kết quả của nó chỉ để đối chiếu.
**C1 chưa đạt** (connector đổi cấu hình và phép đo lại cho kết quả khác): connector thành điều kiện merge thay vì
điều kiện bỏ draft; được bỏ draft khi mọi điều kiện khác đủ, kèm dòng `CHƯA ĐỦ ĐIỀU KIỆN MERGE: chờ connector trên
<SHA>`; lượt tự động sau khi bỏ draft là lượt connector duy nhất cho SHA ấy. Trong trạng thái này, bỏ draft không
phải đề xuất merge; câu "sẵn sàng merge" vẫn cấm.

**M7 — Một lần duyệt.** Chủ kho duyệt một lần, neo SHA H. Lần duyệt ấy bao gồm: merge, thu bằng chứng hậu merge,
ghi sổ, nhả lease, đóng WP. Hậu kiểm thất bại ⇒ không `landed`, không đóng WP. Agent không tự duyệt.

**M8 — Sổ sách.** Ghi sổ hoàn tất là một bản ghi có cấu trúc đăng lên Issue của WP và đọc lại khớp. Trường tối thiểu:

- packet, revision, generation, `spec_hash`;
- H và tree(H);
- biên nhận review và cách xử lý từng finding;
- Windows local và CI PR;
- lần duyệt của chủ kho;
- merge M, các cha, tree(M), CI master;
- nghiệm thu từng mục;
- nhả lease.

Bản ghi ấy là **điểm cuối**: không review bằng model, không mở PR, không chạy Windows cho nó. Sửa thì đăng bản ghi
mới trỏ bản cũ.

**Làn lưu trữ.** Phần lưu Git đi qua một PR lưu trữ mỗi tuần. PR ấy chỉ chứa bản ghi thụ động trong `ops/reviews/**`
và `ops/land/**`; không chứa `ops/leases/**` hay `ops/specs/**`. Nó không cross-review bằng model, không chạy Windows,
và không chặn việc đóng WP. Lease và đặc tả đi làn thường.

**M9 — CI.** Giữ CI trên PR và CI trên master sau merge; gate local không thay CI. `full_mutant_audit` bắt buộc khi
diff chạm `.claude/dev/**`, `ops/**/*.py` hoặc `.github/workflows/**`; còn lại không bắt buộc.

**M10 — Hiệu lực.** Luật này áp cho một packet khi và chỉ khi blob đặc tả mà `spec_hash` của lease trỏ tới có
**đúng một** dòng khớp `^dieu_kien_merge: ADR-0060@([0-9a-f]{40})$`, và OID bắt được qua ba phép đo của `ADR-0053`
mục *Hiệu lực*, thay đường dẫn bằng `docs/adr/0060-dieu-kien-merge-va-moc-ready.md`. Thiếu dòng, hai dòng, phép đo
sai hoặc không đo được ⇒ luật cũ, fail-closed. Không hồi tố.

**M12 — Review offline trước push.** Vì M5 đòi approve trước push, ADR này tự ghi cách đọc các điểm §7 và §13 của
protocol trước push:

- mỏ neo là SHA ứng viên cục bộ và bundle của nó;
- handoff, verdict và biên nhận ghi lên Packet Issue;
- sau push, đối chiếu PR head bằng SHA đã approve, rồi dẫn lại evidence vào PR.

Mọi phép so của §7 giữ nguyên, chỉ đổi mỏ neo.

## Tham số

| tham số | giá trị |
|---|---|
| báo chủ kho khi máy Windows không Online | 15 phút |
| packet sang blocked khi máy Windows không Online | 24 giờ |
| số lần push thêm tối đa mỗi PR | 2 |
| hạng chặn merge | P0, P1, P2 |
| P3 còn mở | đóng có bằng chứng hoặc chủ kho miễn |
| dòng khai hiệu lực | dieu_kien_merge: ADR-0060@<oid40> |

## Những gì KHÔNG đổi

- Check bắt buộc của CI và branch protection giữ nguyên.
- `ADR-0057`/`0058`/`0059` giữ nguyên, trừ câu "máy offline thì không áp" của `ADR-0057` §2 với packet áp ADR này.
- Bốn mốc §10.2.2 không nới. Mốc chưa đo được xử lý đúng như §10.2.2–§10.2.3: ghi thiếu và tiếp tục chặn, trừ
  waiver hợp lệ đúng scope theo protocol; waiver không viết lại kết quả thành `passed`.
- Executor vẫn chỉ ghi trong effective write set; agent không tự approve hay merge.

## Cưỡng chế — M11

**1 cổng** (packet C, #1106): `.claude/dev/packet_loop.py kiem-merge` (điều kiện bỏ draft/merge K0–K6) và `kiem-dong-wp` (đóng WP
D1–D4), không đọc state. Đo trên đủ sáu vị trí cổng mà §20 của protocol liệt kê bằng
`rg -c 'ADR-0060|dieu_kien_merge' <tệp>`:

| vị trí cổng | kết quả |
|---|---|
| `ops/lease_publish.py` | 0 dòng |
| `.claude/dev/packet_loop.py` | 6 dòng (đo khi thi công packet C; lúc soạn ADR: 0) |
| `.claude/dev/launcher.py` | 0 dòng |
| `.claude/dev/gate_lifecycle.py` | 0 dòng |
| `.github/workflows/ci.yml` | 0 dòng |
| `.github/workflows/ops-publish-lease.yml` | 0 dòng |

Ngoài hai lệnh ấy, ADR là kỷ luật executor và reviewer. Ba packet kế nhiệm biến nó thành cổng máy:

- **B** — collector bốn mốc: phần còn lại của #899, đo mốc Workflow definition bằng workflow Actions chỉ đọc.
- **C** — cổng điều kiện merge và đóng WP trong `packet_loop.py`, tách khỏi `ADR-0054` (cửa `accept` hiện đòi
  packet áp `ADR-0054`). Đã làm: `kiem-merge`, `kiem-dong-wp` (#1106).
- **D** — gọn hiện vật review, validator cho làn lưu trữ.

## Nợ

- Chú thích ở `.github/workflows/ci.yml` (job `gate-nhanh-manh`) ghi `full_mutant_audit` "BẮT BUỘC trước
  merge/land/release", rộng hơn M9, trong khi `ci-dot-bien-du.yml` chỉ chạy theo lịch hoặc gọi tay. Chưa sửa, vì
  `ci.yml` nằm ngoài write set của packet này.
- Branch protection của `master` chưa đo được từ phiên web (HTTP 403).

## Phương án bị loại

- **Đẩy ứng viên vào một không gian tên riêng và không tính là lần push:** vẫn là đưa code chưa đủ điều kiện lên
  remote, và mở đường lách bằng đổi tên ref.
- **Dùng Windows local thay Windows CI:** `ADR-0057` đã bác; local là một máy, không có run hay attempt GitHub.
- **Đưa biên nhận review vào chính lần push duy nhất:** biên nhận approve của SHA H không thể nằm trong commit H;
  thêm vào thì sinh SHA mới và phá exact-SHA.
- **Một PR sổ sách cho mỗi packet:** vẫn nhân đôi số PR và số lần merge master; bản ghi trên Issue đạt cùng mục tiêu
  mà không có PR.
- **Bot commit thẳng vào master:** thêm một writer vào canonical, cần quyền và ruleset riêng.
