# DOCTRINE-SCAN-DAO-SANG-DANH-SACH-CHO-PHEP — revision 1 / generation 1

## Authority và identity

- packet_issue: 543; packet_id: DOCTRINE-SCAN-DAO-SANG-DANH-SACH-CHO-PHEP; revision 1; generation 1.
- Chỉ thị cấp: chủ kho `ducthangho`, phiên điều phối 16-09-2026, nguyên văn:
  *"doctrine-scan: mở phiên mới, làm luôn đi"*, nối tiếp quyết định trước đó
  *"Mở packet riêng cho doctrine-scan"*. Bản chiếu neo trong Issue #543.
- Người cấp: ducthangho. Recorder: phiên claude, **không** tự xưng dispatcher.
- Executor: **antigravity** / `google_antigravity` / `antigravity`, chạy trên máy chủ kho.
- Reviewer: **claude** / `anthropic_claude` / `claude_code`.
- Review class: **sensitive** — packet sửa một CỔNG cưỡng chế protocol.
  Assurance target: **cross_approved**. Cặp agy↔claude khác provider nên thoả `§8` mục 1.
- Reviewer phải ở session/context/checkout riêng, không fork context executor.

## Baseline

- base_sha / immutable acceptance baseline: `19de56693d06813e6743a30113d0fb87bff3e196`.
- Branch: `agy/doctrine-scan-r1-g1`; branch ownership: exclusive → antigravity.
- target_branch_neu_land: `master` (đích dự kiến; chưa cấp quyền land).

## Nguồn gốc — finding nào, đo ở đâu

`phep-do-doctrine-khong-du-rang`, **P2 / 2 thể hiện**, mở ở lượt cross-review thứ **9** của
PR #529 (packet #523) và **CHƯA VÁ**. `S4` của #523 CẤM chính packet ấy viết cổng này ⇒ phải
đi bằng packet riêng. Đây là packet ấy.

## Cơ chế hiện tại — ĐO trên `19de5669`, không phải trí nhớ

`cmd_doctrine_scan` (`.claude/dev/packet_loop.py:1386`) quét `.claude/skills/**/*.md` cộng
`CLAUDE.md` (và `--path` thêm), chuẩn hoá văn bản bằng `_phang_ca_tep` + `_chuan_hoa`, rồi
tìm **chuỗi con** của bảng `FORBIDDEN_DOCTRINE_PHRASES` (dòng 175):

```
nguong-so-stop-conditions      12 cụm
ten-state-machine-day-du        2 cụm
bang-vai-tro-muc-2             10 cụm
dinh-nghia-trang-thai-hoan-tat  4 cụm
--------------------------------------
4 nhóm · TỔNG 28 chuỗi
```

Phép đo của reviewer lượt 9 (`measure.py doctrine`):

| đầu vào | rc |
|---|---:|
| adapter gốc | 0 |
| thêm đoạn trần ADR-0048 | 0 |
| **thêm TRỌN `§5.1`** | **0** |
| đối chứng `§12` | 6 |

Chép nguyên một mục của protocol mà cổng vẫn xanh.

## Vì sao đây là một LỚP kho đã biết

`CLAUDE.md` ghi nguyên văn, từ sự cố đã trả giá ở cổng `granted_by`:

> Danh sách CẤM không bao giờ đủ — phải đảo thành danh sách CHO PHÉP. […] *"distinguishes
> spelling, not authority"* — phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN. […] thua từ
> trong thiết kế.

`doctrine-scan` **cùng hình dạng** và **chưa đảo**. Nó phân biệt *cách viết*, không phân biệt
*có chép hay không*.

## Objective

Đổi `doctrine-scan` từ *"có chứa một trong 28 chuỗi này không"* sang *"có chép một đoạn dài từ
`docs/PROTOCOL_DA_PHIEN.md` không"* — đo **HÀNH VI CHÉP**, không đo cách viết.

Bất biến phải giữ: **adapter chỉ được TRỎ về protocol, không nhắc lại nội dung ở đó.** Bất biến
ấy KHÔNG được phụ thuộc vào việc ta có đoán đúng 28 chuỗi hay không.

Đặc tả này **không ghi cứng một thuật toán**. Hướng tự nhiên là đo độ chồng lấn n-gram sau
chuẩn hoá giữa mỗi adapter và protocol, ĐỎ khi có một mạch liên tục đủ dài. Executor được chọn
cơ chế khác nếu nó **thoả hết A1–A5**; nhưng phải khai cơ chế đã chọn và vì sao.

## Write set

Sản phẩm: `.claude/dev/packet_loop.py` · `.claude/dev/packet_loop_test.py`.
Phối hợp: `ops/specs/doctrine-scan-dao-sang-danh-sach-cho-phep-r1.md` ·
`ops/leases/doctrine-scan-r1-g1-antigravity.yaml` · `ops/reviews/doctrine-scan/`.

KHÔNG đụng: `docs/PROTOCOL_DA_PHIEN.md`; bất kỳ tệp nào trong `.claude/skills/**` hay
`.agents/skills/**` (đó là write set đang mở của #538); `.github/workflows/**`;
`scripts/tl.py`; `ops/nhanh_don_duoc_test.py` (#540); `RELEASE_MANIFEST.json`.

## Acceptance

**A1 — ĐẢO DẤU ba phép đo của reviewer lượt 9.** Trên cơ chế mới, dựng lại đúng ba đầu vào ấy:
thêm TRỌN `§5.1` vào một adapter ⇒ **ĐỎ**; `§12` ⇒ **vẫn ĐỎ**; đoạn trần ADR-0048 ⇒ ĐỎ nếu nó
là chép, hoặc **khai rõ vì sao không phải chép** — không được im lặng bỏ qua.
Ghi lệnh + `rc` thật cho từng ca. Đọc `rc` TRỰC TIẾP, không qua pipe.

**A2 — KHÔNG NỚI LỎNG.** Mọi thứ 28 chuỗi hiện bắt được thì cơ chế mới cũng phải bắt. Chốt
chạy được: với TỪNG nhóm trong `FORBIDDEN_DOCTRINE_PHRASES`, dựng một adapter tạm chứa cụm của
nhóm ấy và đòi cơ chế mới ĐỎ. Nhóm nào cơ chế mới **không** bắt được thì phải khai tường minh
kèm lý do, không được lặng lẽ mất.

**A3 — KHÔNG BẮT OAN.** `doctrine-scan` trên cây `master` hiện hành (`19de5669`) phải `rc=0`.
Một cổng đỏ thường trực là cổng sẽ bị tắt, và khi ấy nó không tồn tại đúng lúc cần nhất.
Chạy trên CẢ hai tập: `.claude/skills/**` và `.agents/skills/**`.

**A4 — CON TRỎ KHÔNG PHẢI CHÉP.** Adapter buộc phải nhắc số mục (`§3.2`, `§8`), tên trường
schema (`assurance_target`, `reviewed_sha`), tên trạng thái — nếu không thì không trỏ được.
Cơ chế mới phải **cho phép** những thứ ấy. Chốt: một adapter chỉ gồm con trỏ và câu dẫn phải
`rc=0`; đó là ca ÂM bắt buộc, thiếu nó thì không biết cổng đang đo chép hay đo độ dài.

**A5 — MỖI CHỐT MỘT ĐỘT BIẾN RIÊNG.** Mỗi chốt mới trong `packet_loop_test.py` phải có một đột
biến làm **ca đích** ĐỎ. Đột biến chạy trên **BẢN SAO TẠM**, không đụng tệp thật — bài học
"bom hẹn giờ" của kho: lượt chạy bị cắt giữa chừng thì `finally` không chạy và tệp ở lại méo.
Đột biến bị giết phải giết **đúng lý do**: chết bằng chốt của ca đích, không bằng một lỗi vô
can. Khai rõ ca nào giết ca nào.

**A6 — REVIEW.** Cross-review khác nền (reviewer `claude`), neo ĐÚNG SHA ứng viên, không P1/P2
thì mới `approve`. Verdict + biên nhận v2 commit vào `ops/reviews/doctrine-scan/`. Comment
GitHub chỉ là **bản chiếu**, nguồn có thẩm quyền là tệp có băm.

**A7 — CỔNG.** Trước khi báo xong: `doctrine-scan` · `adr-song` · `doc-claims-check --strict`
(`core.abbrev=7`) · `git diff --check` · `release-verify --strict` (`ok=true`,
`expected_file_count == checked_file_count`) · `bien_nhan_v2` — mỗi cái `rc=0`, đọc trực tiếp.
Cộng `python3 .claude/dev/packet_loop_test.py` phải N/N với **hai số bằng nhau**.
`RELEASE_MANIFEST.json` **nằm ngoài write set**: `.claude/**` không có trong manifest nên sửa
hai tệp này KHÔNG làm manifest lệch — nếu đo ra lệch thì DỪNG và báo, đừng tái sinh manifest.

## Cấm

- Không chạy CI tay, không `workflow_dispatch`, không full CI, không lane `windows`.
  `manual_ci_budget: 0`. Chỉ thị chủ kho đang đứng: *"CI Window gặp lỗi đã biết, để đỡ tốn
  tiền, không chạy CI Windows"*.
- Không merge, không land, không deploy, không đụng ruleset.
- Không tự review, không tự approve.
- Không sửa `docs/PROTOCOL_DA_PHIEN.md` để cổng dễ xanh hơn.
- Không nới bảng cấm cũ rồi gọi đó là đã đảo sang danh sách cho phép.
- Không viết cụm bỏ-qua-CI nguyên văn trong thông điệp commit, kể cả khi trích dẫn.

## Điều kiện dừng

Hết `run_minutes`, hoặc chạm một điều kiện dừng của `docs/PROTOCOL_DA_PHIEN.md §12`, hoặc
A1–A5 không thoả được bằng cơ chế đã chọn. Ở ca thứ ba: **DỪNG và báo**, kèm phép đo cho thấy
vì sao — đừng đổi acceptance cho vừa bản vá. Đổi acceptance là `revision` mới, và đó là quyết
định của chủ kho.

## Ghi chú về băm

`spec_hash` = SHA-256 của toàn bộ bytes UTF-8/LF của tệp này, lưu NGOÀI tệp (trong lease và
Issue receipt) để không có vòng tự băm. Đổi bytes sau khi cấp quyền cần revision/generation
mới; không amend spec đã công bố để làm khớp nội dung.
