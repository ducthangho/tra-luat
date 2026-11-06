# Đặc tả packet — `THU-HOI-ADMISSION-MERGE-BASE-A` (revision 1)

- `packet_id`: **THU-HOI-ADMISSION-MERGE-BASE-A** · `revision`: **1** · trạng thái: nháp, chờ chủ kho duyệt băm.
- `packet_issue`: **#1265** (sub-issue của Mission #1264). Issue không tự cấp việc (protocol §3.2, §4). Packet
  anh em: `THU-HOI-ADMISSION-MERGE-BASE-B` #1266 (mã, đặc tả `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-B-r1.md`). B
  phụ thuộc A: base của B phải chứa commit land của A.
- `nguon_cap_viec`: quyết định chủ kho trong phiên soạn spec ngày 06-11-2026 (Claude Code desktop): vòng 1
  Q1–Q7 và vòng 2 Q8–Q13, chủ kho trả lời cả hai vòng *"Theo khuyến nghị"*. Căn cứ phân tích: tài liệu
  https://claude.ai/artifact/Au5vgKvAZWdqGDHMvkU4cW, mục *"Phương án hợp nhất: tích hợp và admission"*, điểm 4–6.
  Không có dòng kế hoạch trong `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`. Bản ghi bền của hai vòng quyết định nằm
  trong thân Mission #1264, do phiên soạn spec đăng theo yêu cầu của chủ kho ngày 06-11-2026. Thẩm quyền ràng buộc là
  comment duyệt băm đặc tả này do chính chủ kho đăng trên #1265.
- `review_class`: **sensitive** — đổi governance của một cổng đọc lease (`ADR-0047`) và bảng §20 của protocol
  (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease (đo 08:25Z 06-11-2026: `08bcb51f`).
- Executor **Claude**; reviewer **Codex** độc lập (phiên riêng); mức bảo đảm `human_audited` trên exact head
  trước merge (vòng 1 Q6). Điều kiện merge theo `ADR-0060` (mặc định từ `ADR-0062`, không cần dòng khai).

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

(OID là commit LAND trên first-parent master, đo 08:2xZ 06-11 bằng
`git log --first-parent --diff-merges=first-parent --diff-filter=A`: `ADR-0055` ⇒ `d2e3052d…` ngày 25-10,
`ADR-0053` ⇒ `8ab10079…` ngày 17-10.)

## 0. Vấn đề

Bộ kiểm `kiem-thu-hoi-github` (`ops/lease_publish.py`, hàm `lenh_kiem_thu_hoi_github`) đòi S = `base.sha` là tổ
tiên của head H, rồi kiểm trên T = tree(H). Chủ kho giữ điều kiện ấy ngày 24-09-2026 (#618,
https://github.com/ducthangho/tra-luat/issues/618#issuecomment-5819533474) với lý do: nếu H không chứa S, một
bản thu hồi thêm vào master sau khi nhánh rẽ sẽ vắng trong T, và bộ kiểm *"không phân biệt được 'PR xoá
revocation' với 'PR chưa thấy nó'"*. Đặc tả cha `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` r9 (sha256
`465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79`) ghi cùng ý ở gạch *"Strict up-to-date: S tổ
tiên H, merge giữ tree H … Không áp §5.1"*.

Hệ quả đo được (16-10 → 06-11-2026, `origin/master`): 202 commit merge `origin/master` vào nhánh; trong 117 commit
có thân thông điệp, 56 nêu cổng `thu-hoi`. Mỗi lần như vậy tạo head mới và làm mất hiệu lực mọi bằng chứng neo
SHA. Trong khi đó vùng mà bộ kiểm đọc — `ops/thu-hoi/**` và `.github/coordination/change-impact.v1.json` — có
**0** commit first-parent từng chạm, trong toàn lịch sử (đo 08:2xZ 06-11; sổ rỗng, tệp policy chưa tồn tại).

## 1. write_set

- `docs/adr/0066-admission-thu-hoi-theo-merge-base.md` — MỚI.
- `docs/PROTOCOL_DA_PHIEN.md` — chỉ thêm **một** dòng vào bảng §20.

Điều kiện cấp lease: không lease nào còn hiệu lực giữ một đường dẫn của write set, đo bằng
`ops/lease_publish.py ai-dang-giu <đường dẫn>` trên một kho có `refs/heads/*` khớp máy chủ (so tập tên
`git ls-remote --heads origin` với tập ref cục bộ, lệch phía "thiếu cục bộ" phải bằng 0). Đo 06-11: hai đường
dẫn **chưa đo được**: `docs/PROTOCOL_DA_PHIEN.md` ⇒ `CHAN [12]` hai lần liền vì máy chủ thêm nhánh giữa lượt quét
(lần hai: `claude/ghi-so-land-1258`, `ops/wp1239-r4-g3-lease`) — chốt fail-close đúng thiết kế; tệp ADR mới chưa có
kết quả lúc viết. Người cấp lease đo lại ngay trước khi cấp (L5), và chỉ cấp khi cả hai ra `NGƯỜI_GIỮ 0`. Số ADR: trên mọi ref, không tệp nào mang tiền tố `docs/adr/0066-` và không đặc tả nào nhắc
`ADR-0066` (đo 08:2xZ 06-11 trên master: 0 tệp, 0 chỗ nhắc). Bị chiếm ⇒ DỪNG, revision mới đổi số; không tự chọn
số khác.

## 2. ngoai_pham_vi

- Mã của bộ kiểm, test, workflow, validator receipt: thuộc packet B.
- `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` r9 và `ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a.md` r5: đã đóng băng,
  không sửa. ADR-0066 chỉ ghi rằng nó thay một điểm của r9.
- Bản nháp `ops/specs/THU-HOI-LEASE-A1b.md` (#656) và đặc tả #1179 (C1a1b): không sửa; ADR-0066 ghi nghĩa vụ cho
  hai packet ấy (mục tiêu 1f).
- Luật theo ID lease (lease đã thu hồi, phủ write set bằng lease còn hiệu lực) và việc kiểm lại lúc land: thuộc
  A1b và bên tiêu thụ receipt (#499 C1, #1179), theo vòng 1 Q5.
- Các câu của protocol về đo ancestry ở phần preflight admission: vẫn đúng nguyên văn, không sửa.

## 3. muc_tieu

1. `docs/adr/0066-admission-thu-hoi-theo-merge-base.md` — ADR mới, có đủ:
   - a. **Quyết định**, nguyên câu: *"Bộ kiểm admission thu-hoi không còn đòi S là tổ tiên của H."* Kèm luật
     thay thế: nếu S là tổ tiên của H thì giữ nguyên hành vi cũ; nếu không, với **mọi** merge-base B của (S, H),
     vùng bộ kiểm đọc tại B phải giống hệt tại S, rồi mọi phép kiểm hiện có vẫn chạy trên T = tree(H). Vùng gồm
     bản đồ `ops/thu-hoi/**` (đường dẫn → mode, kiểu, OID) và mục `.github/coordination/change-impact.v1.json`
     (vắng, hoặc mode, kiểu, OID). Không có merge-base, vượt ngân sách duyệt hoặc thiếu object ⇒ 12.
   - b. **Vì sao đủ**, trả lời đúng lý do #618: khi vùng tại B bằng vùng tại S, một bản ghi bị PR xoá phải có mặt
     tại B nên cũng có tại S, và phép append-only S→T hiện có bắt nó; một bản ghi "PR chưa thấy" chỉ tồn tại khi
     master đổi vùng sau B, tức vùng tại S khác B, và cổng trả 12 — buộc hoà base đúng lúc cần, không sớm hơn.
   - c. **Thay đúng hai điểm**: (i) gạch *"Strict up-to-date: S tổ tiên H, merge giữ tree H …"* của r9 (sha256 ở
     mục 0), phần áp cho bộ kiểm admission; (ii) quyết định (a) ở #618 `issuecomment-5819533474`.
   - d. **Giữ nguyên**: S là tổ tiên của C (chống lùi định nghĩa); mã canonical từ `workflow_sha`; H tải về phải
     bằng `pull_request.head.sha`; append-only S→T; validator toàn namespace T; chế độ chưa kích hoạt đòi tập
     revocation rỗng ở S và T; `SO_THU_HOI_KICH_HOAT = False`; bộ đọc object có băm lại.
   - e. **Hiệu lực**: từ commit land của packet B trên first-parent master; trước đó luật cũ. Không hồi tố.
   - f. **Nghĩa vụ cho packet khác**: #1179 (C1a1b) thay G3 *"S ≤ H"* và G4 *"tree(H) = T"* bằng hợp đồng mới
     trước khi đóng băng; bên kiểm lúc land (#499 C1/C1b) so vùng của tree(M) với vùng của T và `M^2 == H`; A1b
     (#656) khi bật sổ phải mở rộng vùng sang những gì bộ kiểm mới đọc (lease theo ID) và quyết lại dòng
     *"Q3-diễn giải"* (strict up-to-date) — strict không còn cần cho mục đích của bộ kiểm này.
   - g. **Cưỡng chế**: lệnh và kết quả `rg -c 'ADR-0066'` cho từng vị trí cổng mà §20 của protocol liệt kê, đo
     lúc viết ADR (kỳ vọng 0 ở mọi vị trí trước khi B land); ghi rằng sau khi B land, cổng đọc luật là
     `ops/lease_publish.py` `kiem-thu-hoi-github`.
   - h. **Phương án bị loại** kèm lý do: giữ "S tổ tiên H"; strict up-to-date trên ruleset; merge ba chiều trong
     vùng sổ; tính toàn bộ cây merge-tree(S, H) bằng Git plumbing (trái thiết kế bộ đọc có băm); merge queue
     native (kho thuộc User; workflow `merge_group` lấy định nghĩa từ commit nhóm merge nên PR sửa được).
   - i. Dòng **Trạng thái** dẫn comment duyệt của chủ kho trên Issue packet (neo băm đặc tả này), không phải
     phiên chat.
2. `docs/PROTOCOL_DA_PHIEN.md` — thêm đúng một dòng bảng §20, cùng khuôn các dòng `ADR-0063`…`ADR-0065`:
   cột tóm tắt nói *"Admission thu-hoi: bỏ 'S tổ tiên H', thay bằng cổng vùng bằng nhau ở mọi merge-base"*; cột
   trạng thái *"Accepted — hiệu lực từ land `THU-HOI-ADMISSION-MERGE-BASE-B`"*; cột cổng
   *"`ops/lease_publish.py` `kiem-thu-hoi-github` (sau land B)"*.

## 4. nghiem_thu

Mọi phép khớp chuỗi dưới đây đo trên văn bản **đã nối dòng trong phạm vi từng đoạn** (gộp khoảng trắng, không nối
qua dòng trống), khớp **toàn bộ** câu (L6 b).

| # | tiêu chí | phép đo làm nó ĐỎ | đột biến phải làm nó đổi màu |
|---|---|---|---|
| A1 | `python .claude/dev/packet_loop.py adr-song --root .` rc 0 trên head | rc ≠ 0 | xoá dòng §20 vừa thêm ⇒ rc ≠ 0 |
| A2 | ADR chứa nguyên câu quyết định ở mục tiêu 1a (vế dương) | không khớp | bỏ chữ *"không còn"* khỏi câu ⇒ không khớp; ngắt dòng lại mà giữ nguyên chữ ⇒ vẫn khớp |
| A3 | ADR chứa cả hai định danh bị thay: `465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79` và `issuecomment-5819533474`, mỗi cái ≥ 1 lần | thiếu một | xoá một định danh ⇒ 0 |
| A4 | ADR chứa cụm *"mọi merge-base"* trong đoạn quyết định (vế dương, đếm theo **đoạn quyết định**, không đếm gộp cả tệp — L6 c) | 0 lần trong đoạn ấy | đổi thành *"merge-base đầu tiên"* ⇒ 0 |
| A5 | Bảng §20 có đúng **một** dòng có ô đầu là `ADR-0066` | 0 hoặc ≥ 2 dòng | nhân đôi dòng ⇒ 2 |
| A6 | Mục *Cưỡng chế* của ADR có một dòng cho **từng** vị trí cổng §20 liệt kê (L6 e), kèm lệnh và kết quả | thiếu vị trí nào | bỏ một vị trí ⇒ đỏ khi đối chiếu danh sách §20 |
| A7 | `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0 | rc ≠ 0 | bất biến, xanh sẵn trên nền; răng không thuộc packet này |
| A8 | Kích thước theo `git diff --numstat origin/master...HEAD`: ≤ 2 tệp, ≤ 450 dòng thêm | vượt | — (đo, không cần đột biến) |
| A9 | Không tệp nào ngoài `write_set` đổi (`git diff --name-only origin/master...HEAD`) | có tệp lạ | thêm một tệp ⇒ đỏ |
| A10 | CI required xanh trên exact head; điều kiện `ADR-0060` (0 P0–P2 mở, P3 đóng có bằng chứng hoặc chủ kho miễn, connector đã review đúng commit, human audit trên H) | thiếu điều kiện nào | — |

Vế âm: không áp dụng ở A, vì câu cũ cần xoá nằm ở chú thích workflow — thuộc packet B (tiêu chí B10).

Chạy thử trên nền (worktree tách ở `origin/master` `08bcb51f`, 08:3xZ 06-11-2026):

- A1: `adr-song` rc 0 — *"64 ADR trên đĩa, 64 dòng trong §20, khớp 1–1"*. Răng đã đo: thêm riêng tệp
  `docs/adr/0066-admission-thu-hoi-theo-merge-base.md` mà không thêm dòng §20 ⇒ rc **9**, *"có tệp … mà KHÔNG có
  dòng nào trong §20"*. Tệp thử đã xoá, worktree sạch.
- A7: `doctrine-scan` rc 0 — *"đã quét 10 tệp, 0 chỗ chép doctrine"* (bất biến, xanh sẵn).
- A2–A6: đỏ trên nền vì ADR-0066 chưa tồn tại — đúng màu "chưa làm".

## 5. hinh_dang_ke_thua

Không phải packet khắc phục; chép tự nguyện các lớp cùng họ từ đặc tả #1179 r1 §7 (nhánh
`claude/spec-1179-c1a1b`, commit `7cfb4d7`) và quyết định chủ kho ở #1179 ngày 06-11-2026 07:58Z:

| lớp | số đếm | nguồn | áp ở packet này |
|---|---|---|---|
| `phan-loai-vang-va-khong-do-duoc` | **4** (chạm chốt dừng) | #1179 r1 lượt 1 F4 | ADR phải nói rõ ba trạng thái (là tổ tiên · không phải · không đo được ⇒ 12) |
| `nguon-duoc-tin-ma-chua-xac-minh` | 7 (chuỗi thu hồi) | spec C1a1a r5 §6, chép ở #1179 r1 §7 | ADR không tin `base.sha` hay tên nhánh làm bằng chứng quan hệ |

Một biểu hiện mới của lớp thứ nhất ở bất kỳ lượt review nào của packet này ⇒ DỪNG, Review Rescue Checkpoint
(`ADR-0037`), báo chủ kho.

## 6. Review và ngân sách

Reviewer Codex độc lập, trần 10 lời gọi theo dòng khai `ADR-0055` ở đầu tệp; đếm **trước** mỗi lời gọi. Ngân sách
mềm 2 lời gọi; hai lượt liên tiếp chưa approve ⇒ Review Rescue Checkpoint. Connector `@codex review` trên PR draft
theo `ADR-0060` M6.

## 7. chua_do_duoc

- Kết quả `ai-dang-giu` cho hai đường dẫn của write set: chưa có kết quả dương (mục 1); phải có `NGƯỜI_GIỮ 0` trước
  khi cấp lease.
- Lời khai *"0 commit chạm vùng"* đúng tới 08:2xZ 06-11-2026; đo lại khi viết ADR.
- Comment duyệt băm của chủ kho trên #1265: chưa có lúc viết.
