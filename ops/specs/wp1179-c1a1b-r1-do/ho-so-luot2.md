# Hồ sơ sau lượt 2 — packet wp1179 (C1a1b), phiên soạn spec 06-11-2026

Tệp này **không** thuộc đặc tả. Nó bổ sung handoff do phiên điều phối #1206 chuyển từ chủ kho (~08:25Z 06-11),
mục 1–8, cho r2 (`ops/specs/wp1179-c1a1b-r2.md`, sha256 `04fa50683c44f3db093ab2396ebef7e0a12b88740eb35745da39c8016e9d108d`).
r2 không được sửa sau review, để giữ đúng băm đã review. Phương án A đã chốt không đổi. Q-R đã kích hoạt ở lượt 2,
nên packet chuyển sang (B), tức human audit.

Mốc đo: head `3c57c3fa6129efafb5c18e76aef1ee71a3713396`, tree `bd57d9e6a495e54bdf664563fcb0b568c97644e8`,
`origin/master` `08bcb51fbed359eaeeca41bc3a0559fe308c0aa9`, đo ~08:26Z 06-11.

## 1. Ngân sách lời gọi Codex — `used / reserved / limit`, kèm nguồn

| đại lượng | giá trị | nguồn | trạng thái |
|---|---|---|---|
| used, trước phiên soạn r1 | **≥ 4**: 3 verdict + 1 lượt mất kết quả | Issue #1179 `6622860952`, `6624954880` (ba log hash) | cận dưới; con số chính xác **unknown** |
| used, phiên soạn r1/r2 | **2**: r1 lượt 1 (run `202041c2`), r2 lượt 2 (run `daedf180`) | `review-luot1/run.json`, `review-luot2-r2/run.json` | đo được |
| used, tổng `U` | **≥ 6** | cộng hai dòng trên | cận dưới, phần dư **unknown** |
| không tính | auto-review từ chối draft3, trước khi chạy model; launcher `CHAN [11]` 07:32Z, trước khi chạy model | `6623060128`; phiên này | ghi, không đếm |
| reserved | **unknown** | chưa có cơ chế reservation nào được đo; snapshot quota cũ `6624954880` (07:11Z 04-11) không phải reservation | unknown |
| limit | **10** | dòng khai `ADR-0055@d2e3052d` trong r2; ba phép đo rc 0/128/0 (phiên soạn, `review-luot1/VERDICT.md`, `review-luot2-r2/VERDICT.md`) | đo được trên snapshot |
| còn lại `limit − U` | **≤ 4**, con số chính xác **unknown** | — | không suy số dư từ cận dưới (protocol §12) |
| journal/state có thẩm quyền của dispatcher cũ | **unknown** | dispatcher cũ chạy trên máy khác. Phiên điều phối mới không truy cập được tệp reconcile trên máy ASUS | unknown |
| state ở checkout NÀY | không có: `python .claude/dev/packet_loop.py status --packet 1179` ⇒ rc **8**, "chưa có state … wp1179.json" (~08:26Z) | phiên soạn | chỉ nói về checkout này, **không** chứng minh state không tồn tại ở nơi khác |

**Đề xuất phục hồi state, kiểm chứng được và không tạo state giả.** Người cấp lease chọn **một** trong hai đường:

- (a) Chủ kho, hoặc dispatcher cũ trên máy của mình, chạy `packet_loop.py status --packet 1179` rồi đăng output thô kèm
  sha256 của tệp state lên #1179. Nếu tệp có, `U` lấy từ đó. Nếu không có, ghi rõ "không có ở máy X".
- (b) Không có (a) thì `U` là cận dưới **6** đã có nguồn. Người cấp lease khai `U = 6` là **cận dưới**, và
  `--codex-review-calls-limit` = `10 − 6 = 4`. Đó là trần **lạc quan**. Vì `U` thật có thể lớn hơn, chủ kho phải duyệt
  rõ việc dùng cận dưới, hoặc hạ limit để chừa biên. Không ghi "còn đúng 4".

## 2. `record-rescue`

Các comment thuật lại quyết định Rescue (`6624905106` cho draft2; `6680102065` và tin nhắn phiên điều phối ~07:57Z
cho r1) **không tương đương** một bản ghi `packet_loop record-rescue` hợp lệ. Mã ở `.claude/dev/packet_loop.py:1333`
chỉ nhận `record-rescue` khi state là `blocked` vì `rescue_required`. Hiện chưa có state nào (mục 1).

Khi init packet ở pha thi công, người khởi tạo state phải:
1. `init --packet 1179 --executor claude --reviewer codex --codex-review-calls-limit <10 − U>` (cách chọn `U`: mục 1);
2. nếu protocol hoặc chốt state đòi Rescue phải nằm trong journal, đưa state về đúng `blocked/rescue_required` bằng
   chính đường của `packet_loop`, rồi `record-rescue --quyet-dinh revision --can-cu "<6624905106; 6680102065; Q-R>"`
   cho từng lần. Không sửa tay tệp state. Đường hợp lệ đưa một state mới vào `blocked/rescue_required` chưa được đo
   trong phiên này: **unknown**. Nếu không có đường ấy, ghi bảng đối chiếu vào lease hoặc handoff, theo protocol §3.2.1.

## 3. Lượt draft3 bị auto-review từ chối, và vì sao hai lượt của phiên này không phải lượt ấy gọi lại

Lượt bị từ chối là review **draft3** (sha256 `de10ed3d…41b1`) trên máy dispatcher cũ, với lý do: chưa có reconcile bền
cho budget và Review Rescue (`6623060128`). Hai lượt của phiên này review **nội dung khác**:

- r1 (sha256 `3dc6a2b9…6d04`) và r2 (`04fa5068…108d`) được soạn lại từ nội dung Issue trên master `889334fb`, theo
  bàn giao `6679422380` ("draft4 không phải nguồn").
- Draft3 và draft4 không được đọc, không được chép.

Các tiền đề mà lý do từ chối nêu đã có căn cứ mới trước lượt 1:
- quyết định Rescue `revision` (`6624905106`);
- bàn giao có thẩm quyền cho phiên điều phối mới, kèm chỉ thị "tối đa 2 lượt Codex" (`6679422380` và chỉ thị giao
  việc);
- bảng ngân sách giữ lịch sử ≥ 4 (r1 §0).

Không dùng provider, máy hay phiên khác để né. Cả hai lượt đều là Codex qua `launcher.py run` trong container của
phiên này.

**Giới hạn của lập luận:** budget vẫn chưa "reconcile" theo nghĩa state có thẩm quyền (mục 1: journal cũ unknown).
Nếu chủ kho coi đó là tiền đề chưa thoả, thì lý do từ chối cũ vẫn đứng. Hai lượt của phiên này khi ấy phải được
chủ kho xác nhận là chấp nhận được. Phiên này báo điểm ấy lên phiên điều phối.

## 4. Draft4

Phiên này không có, không đọc, và không đăng toàn văn draft4 (sha256 `2522c11f…6229`) ở bất kỳ đâu. Chỉ sha256 và
bản tóm tắt đã có sẵn trên Issue được nhắc lại.

## 5. Master drift, đo đầy đủ

`git diff --stat 889334fb87c25136a13c6776a40a25b401820e04 08bcb51fbed359eaeeca41bc3a0559fe308c0aa9`, toàn cây, rc 0:
**1 tệp**, `.githooks/eol_policy_test.py` (+698/−92).

Lọc theo write set và các phụ thuộc, rc 0, stdout **rỗng** (0 tệp đổi). Danh sách đã lọc:
- write set: `.claude/dev/doc_receipt_thu_hoi_git.py`, `.claude/dev/doc_receipt_thu_hoi_test.py`;
- module và sổ: `.claude/dev/doc_receipt_thu_hoi.py`, `.claude/dev/ci_dang_ky_test.py`;
- producer: `ops/lease_publish.py`, `.github/workflows/ops-thu-hoi-admission.yml`;
- workflow và công cụ: `.github/workflows/ci.yml`, `.claude/dev/packet_loop.py`, `.claude/dev/launcher.py`;
- luật: `docs/PROTOCOL_DA_PHIEN.md`, `docs/adr`;
- spec nguồn: C1a1a, spec cha, A1b;
- `CLAUDE.md`, `AGENTS.md`.

Số đo trong r2 neo `889334fb` vẫn còn đúng cho mọi tệp phụ thuộc trên. Người cấp lease phải đo lại trên base thật.

## 6. #1170

Theo phiên điều phối, #1170 đã dừng ở g4 (`6649658505`). Lease #1170 không thuộc write set r2. Dù vậy, trước khi cấp
lease vẫn phải quét **toàn bộ** ref và holder: so tập tên `ls-remote` với `for-each-ref`, rồi chạy `ai-dang-giu` trên
cả hai đường write set và trên `doc_receipt_thu_hoi.py`. Lần đo cuối của phiên này (07:25:56Z, 776 = 776 ref) là
lịch sử, không phải phép đo trước lease.

## 7. Phạm vi

C1a1b chỉ kiểm receipt **nhất quán với C tự khai**. Ngoài phạm vi: C1a2, C1b, Q17/T2, #656, #564, #499. Không trộn
#1160 (r2 §5).

## 8. Gate trên head `3c57c3f`

| gate | kết quả | ghi chú |
|---|---|---|
| `doctrine-scan` | passed (rc 0, cục bộ) | |
| `adr-song` | passed (rc 0, cục bộ, đo trên r1) | |
| `ci_dang_ky_test.py` (kiểm sổ) | passed (`TỔNG: ĐẠT`, cục bộ, đo trên r1) | |
| `git diff --check origin/master HEAD` | **failed** | khoảng trắng trong các log evidence chép nguyên văn (`review-luot1/evidence/{basic,counts,holders}.txt`, `review-luot2-r2/evidence/final-r2.txt`); bản thân hai tệp spec sạch |
| CI trên `7cfb4d7` | `gate`, `gate-ops`, `gate-packet-loop`, `gate-registry`, `gate-nhanh-*` 8/8, `gate-nhanh-gop`, `gate-cong-cu-gop`, `chuan-bi`: passed · `thu-hoi`: **failed** (head tụt base `08bcb51`) · `mo`, `gate-cong-cu`: skipped | skipped không tính là pass |
| CI trên `3c57c3f` | not_run (chưa push) | |
| Windows, full mutant audit | not_run (pha spec, theo chỉ thị) | |
| Human audit (B) | not_run | việc của chủ kho |
