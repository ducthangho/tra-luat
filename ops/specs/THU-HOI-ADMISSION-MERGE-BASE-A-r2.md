# Đặc tả packet — `THU-HOI-ADMISSION-MERGE-BASE-A` (revision 2)

- `packet_id`: **THU-HOI-ADMISSION-MERGE-BASE-A** · `revision`: **2** · trạng thái: nháp, chờ chủ kho duyệt băm.
  Thay `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-A-r1.md` (sha256
  `7ed6a49c123744e122c84f92c1e9ff26b2d3ec0913dc3e0791bfb1891e0b4b67`, chưa được duyệt); r1 giữ nguyên trong kho để verdict
  review lượt 1 vẫn tra được theo băm. Thay đổi so với r1: mục 8.
- `packet_issue`: **#1265** (sub-issue của Mission #1264). Issue không tự cấp việc (protocol §3.2, §4). Packet
  anh em: `THU-HOI-ADMISSION-MERGE-BASE-B` #1266 (mã, đặc tả `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-B-r2.md`). B
  phụ thuộc A: base của B phải chứa commit land của A.
- `nguon_cap_viec`: quyết định chủ kho trong phiên soạn spec ngày 06-11-2026 (Claude Code desktop): vòng 1
  Q1–Q7 và vòng 2 Q8–Q13, chủ kho trả lời cả hai vòng *"Theo khuyến nghị"*. Căn cứ phân tích: tài liệu
  https://claude.ai/artifact/Au5vgKvAZWdqGDHMvkU4cW, mục *"Phương án hợp nhất: tích hợp và admission"*, điểm 4–6.
  Không có dòng kế hoạch trong `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`. Bản ghi bền của hai vòng quyết định nằm
  trong thân Mission #1264, do phiên soạn spec đăng theo yêu cầu của chủ kho ngày 06-11-2026. Thẩm quyền ràng buộc là
  comment duyệt băm đặc tả này do chính chủ kho đăng trên #1265.
- `review_class`: **sensitive** — đổi governance của một cổng đọc lease (`ADR-0047`) và bảng §20 của protocol
  (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease (đo 01:14Z 07-11-2026: `9607e3eb`).
- Executor **Claude**; reviewer **Codex** độc lập (phiên riêng); mức bảo đảm `human_audited` trên exact head
  trước merge (vòng 1 Q6). Điều kiện merge theo `ADR-0060` (mặc định từ `ADR-0062`, không cần dòng khai).

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

(OID là commit LAND trên first-parent master, đo 08:2xZ 06-11 bằng
`git log --first-parent --diff-merges=first-parent --diff-filter=A`: `ADR-0055` ⇒ `d2e3052d…` ngày 25-10,
`ADR-0053` ⇒ `8ab10079…` ngày 17-10. Review lượt 1 đo lại ba phép `cat-file -e L:ADR` rc 0, `cat-file -e L^1:ADR`
rc 128, L nằm trên first-parent, cho cả hai.)

## 0. Vấn đề

Bộ kiểm `kiem-thu-hoi-github` (`ops/lease_publish.py`, hàm `lenh_kiem_thu_hoi_github`) đòi S = `base.sha` là tổ
tiên của head H, rồi kiểm trên T = tree(H). Chủ kho giữ điều kiện ấy ngày 24-09-2026 (#618,
https://github.com/ducthangho/tra-luat/issues/618#issuecomment-5819533474) với lý do: nếu H không chứa S, một
bản thu hồi thêm vào master sau khi nhánh rẽ sẽ vắng trong T, và bộ kiểm *"không phân biệt được 'PR xoá
revocation' với 'PR chưa thấy nó'"*. Đặc tả cha `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` r9 (sha256
`465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79`) ghi cùng ý ở gạch *"Strict up-to-date: S tổ
tiên H, merge giữ tree H … Không áp §5.1"*.

Hệ quả đo được. Phép đo: `git log --merges --since=2026-10-16T00:00:00Z --until=2026-11-06T08:25:00Z 08bcb51f`
(ngày commit), giữ commit có tiêu đề chứa nguyên chuỗi `origin/master`; "có thân" là `%b` còn ký tự sau khi bỏ khoảng
trắng; "nhắc thu-hoi" là tiêu đề hoặc thân chứa `thu-hoi`. Kết quả (đo 07-11-2026, khớp số review lượt 1 đo độc lập):
trong 571 commit merge của cửa sổ, **206** commit merge `origin/master` vào nhánh; **121** có thân; **58** nhắc
`thu-hoi`. (r1 ghi 202/117/56 từ một bộ lọc không ghi lại lệnh, nên không tái lập được; r2 thay bằng số có lệnh.)
Mỗi lần merge như vậy tạo head mới và làm mất hiệu lực mọi bằng chứng neo SHA. Trong khi đó vùng mà bộ kiểm đọc —
`ops/thu-hoi/**` và `.github/coordination/change-impact.v1.json` — có **0** commit first-parent từng chạm, trong toàn
lịch sử (`git log --first-parent --format=%H origin/master -- ops/thu-hoi/ .github/coordination/change-impact.v1.json`,
đo 01:14Z 07-11-2026 trên `9607e3eb`; sổ rỗng, tệp policy chưa tồn tại).

## 1. write_set

- `docs/adr/0066-admission-thu-hoi-theo-merge-base.md` — MỚI.
- `docs/PROTOCOL_DA_PHIEN.md` — chỉ thêm **một** dòng vào bảng §20.

Điều kiện cấp lease: không lease nào còn hiệu lực giữ một đường dẫn của write set, đo bằng
`ops/lease_publish.py ai-dang-giu <đường dẫn>` trên một kho có `refs/heads/*` khớp máy chủ (so tập tên
`git ls-remote --heads origin` với tập ref cục bộ, lệch phía "thiếu cục bộ" phải bằng 0). Đo 06-11-2026:
`docs/PROTOCOL_DA_PHIEN.md` ⇒ `NGƯỜI_GIỮ 0` (lượt quét bắt đầu 15:10Z);
`docs/adr/0066-admission-thu-hoi-theo-merge-base.md` ⇒ `NGƯỜI_GIỮ 0` (17:08Z). Hai lượt trước đó bị chốt fail-close
chặn vì máy chủ thêm nhánh giữa lượt quét; làm mới cache rồi chạy lại ngay thì ra kết quả trên. r2 không quét lại.
Người cấp lease đo lại ngay trước khi cấp (L5), và chỉ cấp khi cả hai ra `NGƯỜI_GIỮ 0`.

Số ADR: không ref nào có tệp mang tiền tố `docs/adr/0066-` (đo 01:46Z 07-11-2026 bằng
`git log --remotes=origin --format= --name-only -- 'docs/adr/0066-*'` sau khi fetch đủ 787/787 nhánh, tập tên khớp
`git ls-remote --heads origin`, thiếu cục bộ 0). Bị chiếm ⇒ DỪNG, revision mới đổi số; không tự chọn số khác.

**Va chạm đã biết với WP1174 (#1174).** Bộ duyệt C6 của WP1174 có `docs/PROTOCOL_DA_PHIEN.md` trong write set, lease dự
kiến tối đa 24 giờ, hạn cứng `2026-11-08T08:03:01Z`. Đo 15:0xZ 06-11-2026: WP1174 chưa được cấp lease, chưa có nhánh,
commit metadata P chưa có trên máy chủ. Write set của WP1174 không có `docs/adr/**`, nên không tranh số ADR. Thứ tự đề
xuất: cấp lease A **trước** khi cấp lease WP1174, vì A chỉ 2 tệp và khoảng nửa ngày. Nếu WP1174 được cấp trước thì A
chờ lease ấy nhả, không xin chia tệp.

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
   - a. **Quyết định**, gồm đúng năm câu dưới đây, chép **nguyên văn** (giữ dấu `` ` ``), mỗi câu nằm trọn trong một
     đoạn của mục Quyết định; được ngắt dòng tuỳ ý trong đoạn:
     - R1: *"Bộ kiểm admission thu-hoi không còn đòi S là tổ tiên của H."*
     - R2: *"Nếu S là tổ tiên của H, bộ kiểm giữ nguyên hành vi trước ADR này và không đọc vùng tại S."*
     - R3: *"Nếu S không phải tổ tiên của H, với mọi merge-base B của (S, H), vùng bộ kiểm đọc tại B phải giống hệt
       vùng ấy tại S; sau đó mọi phép kiểm hiện có chạy trên T = tree(H)."*
     - R4: *"Vùng gồm bản đồ `ops/thu-hoi/**` (đường dẫn → mode, kiểu, OID) và mục
       `.github/coordination/change-impact.v1.json` (vắng, hoặc mode, kiểu, OID)."*
     - R5: *"Một merge-base có vùng khác vùng tại S, không có merge-base, vượt ngân sách duyệt, thiếu object hoặc
       object băm không khớp tên ⇒ rc 12."*
   - b. **Vì sao đủ**, trả lời đúng lý do #618: khi vùng tại B bằng vùng tại S, một bản ghi bị PR xoá phải có mặt
     tại B nên cũng có tại S, và phép append-only S→T hiện có bắt nó; một bản ghi "PR chưa thấy" chỉ tồn tại khi
     master đổi vùng sau B, tức vùng tại S khác B, và cổng trả 12 — buộc hoà base đúng lúc cần, không sớm hơn.
   - c. **Thay đúng hai điểm**: (i) gạch *"Strict up-to-date: S tổ tiên H, merge giữ tree H …"* của r9 (sha256 ở
     mục 0), phần áp cho bộ kiểm admission; (ii) quyết định (a) ở #618 `issuecomment-5819533474`.
   - d. **Giữ nguyên**: S là tổ tiên của C (chống lùi định nghĩa); mã canonical từ `workflow_sha`; H tải về phải
     bằng `pull_request.head.sha`; T = tree(H); append-only S→T; validator toàn namespace T; chế độ chưa kích hoạt
     đòi tập revocation rỗng ở S và T; `SO_THU_HOI_KICH_HOAT = False`; bộ đọc object có băm lại, bỏ qua
     `refs/replace` và graft của kho nguồn.
   - e. **Hiệu lực**: từ commit land của packet B trên first-parent master; trước đó luật cũ. Không hồi tố.
   - f. **Nghĩa vụ cho packet khác**: #1179 (C1a1b) thay G3 *"S ≤ H"* bằng hợp đồng mới trước khi đóng băng; G4
     *"tree(H) = T"* **giữ nguyên** — bỏ G3 không cho phép bỏ ràng buộc T với H. Bên kiểm lúc land (#499 C1/C1b) so
     vùng của tree(M) với vùng của T và `M^2 == H`. A1b (#656) khi bật sổ phải mở rộng vùng sang những gì bộ kiểm mới
     đọc (lease theo ID) và quyết lại dòng *"Q3-diễn giải"* (strict up-to-date) — strict không còn cần cho mục đích
     của bộ kiểm này.
   - g. **Cưỡng chế**: một dòng cho **từng** vị trí cổng mà §20 của protocol liệt kê (mục *Cột "cổng đã ĐO" nghĩa là
     gì*): `ops/lease_publish.py`, `.claude/dev/packet_loop.py`, `.claude/dev/launcher.py`,
     `.claude/dev/gate_lifecycle.py`, `.github/workflows/ci.yml`, `.github/workflows/ops-publish-lease.yml`. Mỗi dòng
     ghi lệnh (`git show <base>:<tệp> | grep -c 'ADR-0066'`), số dòng của tệp đã đọc (để phân biệt "đọc được, 0 lần"
     với "không đọc được") và kết quả. Đo trên base của lease; kỳ vọng 0 ở cả sáu (đo thử 07-11-2026 trên `9607e3eb`:
     cả sáu ra 0, số dòng 2604 · 3761 · 5611 · 1688 · 1184 · 277). Ghi rằng sau khi B land, cổng đọc luật là
     `ops/lease_publish.py` `kiem-thu-hoi-github`, và lời khai ấy chỉ đúng khi có phản chứng của B (ca B1–B9).
   - h. **Phương án bị loại** kèm lý do: giữ "S tổ tiên H"; strict up-to-date trên ruleset; merge ba chiều trong
     vùng sổ; tính toàn bộ cây merge-tree(S, H) bằng Git plumbing (trái thiết kế bộ đọc có băm); merge queue
     native (kho thuộc User; workflow `merge_group` lấy định nghĩa từ commit nhóm merge nên PR sửa được).
   - i. Dòng **Trạng thái** dẫn comment duyệt của chủ kho trên Issue packet (neo băm đặc tả này), không phải
     phiên chat.
2. `docs/PROTOCOL_DA_PHIEN.md` — thêm đúng một dòng bảng §20 (bảng A, ngay sau dòng `ADR-0065`), nguyên văn:

   ```
   | `ADR-0066` | Admission thu-hoi: bỏ 'S tổ tiên H', thay bằng cổng vùng bằng nhau ở mọi merge-base | Accepted — hiệu lực từ land `THU-HOI-ADMISSION-MERGE-BASE-B` | 0 cổng (đo lúc land A); sau land B: `ops/lease_publish.py` `kiem-thu-hoi-github` |
   ```

   Cột cổng ghi `0 cổng` vì đó là giá trị đo được lúc A land (mục tiêu 1g); vế "sau land B" là lời khai về tương lai,
   không phải `có nhắc` hay phép đo.

## 4. nghiem_thu

Mọi phép khớp chuỗi dưới đây đo trên văn bản Markdown thô (giữ dấu `` ` ``) **đã nối dòng trong phạm vi từng đoạn**
(gộp mọi chuỗi khoảng trắng thành một dấu cách, không nối qua dòng trống), khớp **toàn bộ** câu (L6 b).

| # | tiêu chí | phép đo làm nó ĐỎ | đột biến phải làm nó đổi màu |
|---|---|---|---|
| A1 | `python .claude/dev/packet_loop.py adr-song --root .` rc 0 trên head | rc ≠ 0 | xoá dòng §20 vừa thêm ⇒ rc 9 |
| A2 | Mục Quyết định của ADR chứa nguyên câu R1 | không khớp | bỏ chữ *"không còn"* ⇒ không khớp; ngắt dòng lại mà giữ nguyên chữ ⇒ vẫn khớp |
| A3 | ADR chứa cả hai định danh bị thay: `465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79` và `issuecomment-5819533474`, mỗi cái ≥ 1 lần (đếm từng định danh) | thiếu một | xoá một định danh ⇒ 0 |
| A4 | Mục Quyết định chứa nguyên từng câu R2, R3, R4, R5 — **bốn** phép khớp riêng, mỗi câu một vị trí (L6 c) | một câu không khớp | mỗi đột biến sau phải làm đúng câu của nó đỏ: R2 bỏ *"và không đọc vùng tại S"*; R3 đổi *"giống hệt"* thành *"chứa"*, đổi *"mọi merge-base"* thành *"merge-base đầu tiên"*, đổi *"T = tree(H)"* thành *"tree(S)"*; R4 bỏ cụm mục `.github/coordination/change-impact.v1.json`; R5 đổi *"rc 12"* thành *"rc 0"*. Ngắt dòng lại trong đoạn ⇒ vẫn khớp |
| A5 | Bảng §20 có đúng **một** dòng có ô đầu là `` `ADR-0066` ``, và dòng ấy bằng nguyên văn dòng ở mục tiêu 2 (so sau khi gộp khoảng trắng) | 0 hoặc ≥ 2 dòng; hoặc lệch nội dung | nhân đôi dòng ⇒ 2; đổi cột cổng thành `có nhắc: lease_publish.py×1` ⇒ lệch |
| A6 | Mục *Cưỡng chế* của ADR có một dòng cho **từng** vị trí trong sáu vị trí ở mục tiêu 1g, mỗi dòng có lệnh, số dòng đã đọc và kết quả (L6 e) | thiếu vị trí nào, hoặc thiếu số dòng | bỏ dòng `gate_lifecycle.py` ⇒ đỏ khi đối chiếu danh sách sáu vị trí |
| A7 | `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0 | rc ≠ 0 | bất biến, xanh sẵn trên nền; răng không thuộc packet này |
| A8 | Kích thước theo `git diff --numstat origin/master...HEAD`: ≤ 2 tệp, ≤ 450 dòng thêm | vượt | — (đo, không cần đột biến) |
| A9 | Không tệp nào ngoài `write_set` đổi (`git diff --name-only origin/master...HEAD`) | có tệp lạ | thêm một tệp ⇒ đỏ |
| A10 | CI required xanh trên exact head; điều kiện `ADR-0060` (0 P0–P2 mở, P3 đóng có bằng chứng hoặc chủ kho miễn, connector đã review đúng commit, human audit trên H) | thiếu điều kiện nào | — |

**Năm vế L6 cho các tiêu chí khớp chuỗi** (vế không áp dụng ghi lý do):

| tiêu chí | (a) dương / âm | (b) trọn mệnh đề, nối đoạn | (c) từng vị trí | (d) chữ / số | (e) đủ vị trí cổng |
|---|---|---|---|---|---|
| A2 | dương; âm không áp ở A: câu cũ nằm trong chú thích workflow, thuộc B10 | trọn câu R1, nối đoạn | một câu | không có số | không phải lời khai về cổng |
| A3 | dương; không xoá nguồn cũ nên không có âm | hai định danh là token trọn vẹn, không bị ngắt dòng giữa token | đếm từng định danh | không có ngưỡng số | không áp |
| A4 | dương; âm thuộc B10 | trọn từng câu R2–R5, nối đoạn | bốn câu, bốn phép khớp | R5 viết `rc 12` bằng chữ số; đột biến `rc 0` đo đúng dạng ấy | không áp |
| A5 | dương (đúng một dòng, đúng nội dung) | so nguyên dòng bảng | một dòng | số `0` ở cột cổng là giá trị đo, không phải ngưỡng | cột cổng ghi giá trị đo theo mục tiêu 1g |
| A6 | dương | mỗi dòng là một vị trí, không khớp cụm | sáu vị trí, đếm riêng | kết quả ghi bằng chữ số | đủ sáu vị trí của §20 |

Chạy thử trên nền:

- A1 (worktree tách ở `08bcb51f`, 08:3xZ 06-11-2026): `adr-song` rc 0 — *"64 ADR trên đĩa, 64 dòng trong §20, khớp
  1–1"*. Răng đã đo: thêm riêng tệp `docs/adr/0066-admission-thu-hoi-theo-merge-base.md` mà không thêm dòng §20 ⇒
  rc **9**, *"có tệp … mà KHÔNG có dòng nào trong §20"*. Review lượt 1 đo thêm: thêm cả ADR giả lập lẫn dòng liền bảng
  ⇒ 65/65, rc 0. Đo lại 07-11-2026 trên cây `354d538b` (nội dung `docs/` bằng `9607e3eb`): rc 0, 64/64.
- A7: `doctrine-scan` rc 0 — *"đã quét 10 tệp, 0 chỗ chép doctrine"* (07-11-2026; bất biến, xanh sẵn).
- A2–A6: đỏ trên nền vì ADR-0066 chưa tồn tại — đúng màu "chưa làm".

## 5. hinh_dang_ke_thua

Không phải packet khắc phục; chép tự nguyện các lớp cùng họ từ đặc tả #1179 r1 §7 (nhánh
`claude/spec-1179-c1a1b`, commit `7cfb4d7`) và quyết định chủ kho ở #1179 ngày 06-11-2026 07:58Z:

| lớp | số đếm | nguồn | áp ở packet này |
|---|---|---|---|
| `phan-loai-vang-va-khong-do-duoc` | **4** (chạm chốt dừng) | #1179 r1 lượt 1 F4 (review lượt 1 xác nhận số 3/7 có nguồn trong clone; số 4 dựa quyết định chủ kho ngoài clone) | ADR phải nói rõ ba trạng thái (là tổ tiên · không phải · không đo được ⇒ 12) |
| `nguon-duoc-tin-ma-chua-xac-minh` | 7 (chuỗi thu hồi) | spec C1a1a r5 §6, chép ở #1179 r1 §7 | ADR không tin `base.sha` hay tên nhánh làm bằng chứng quan hệ |

Review lượt 1 không thấy biểu hiện mới của hai lớp này. Một biểu hiện mới của lớp thứ nhất ở bất kỳ lượt review nào
của packet này ⇒ DỪNG, Review Rescue Checkpoint (`ADR-0037`), báo chủ kho.

## 6. Review và ngân sách

**Review đặc tả, trước khi chủ kho duyệt băm:** review độc lập của chính đặc tả này (Codex, ≤ 2 lời gọi, tính trên PR
đưa đặc tả vào kho, chung cho A và B). Finding P0–P2 ⇒ sửa đặc tả và tính băm mới trước khi duyệt.
Lịch sử: lượt 0 (06-11-2026 17:54:25Z–17:54:41Z) dừng trước khi model chạy, HTTP 400 `model_not_found`; lượt 1
(17:56:04Z–18:31:15Z) review r1, `changes_requested`, 7 P2 + 1 P3, verdict chiếu ở
https://github.com/ducthangho/tra-luat/pull/1268#issuecomment-6700056296. Lượt 0 có tính là một lời gọi hay không
do chủ kho quyết; review r2 chỉ chạy khi chủ kho cho phép.

**Review mã:** reviewer Codex độc lập, trần 10 lời gọi theo dòng khai `ADR-0055` ở đầu tệp; đếm **trước** mỗi lời
gọi. Ngân sách mềm 2 lời gọi; hai lượt liên tiếp chưa approve ⇒ Review Rescue Checkpoint. Connector `@codex review`
trên PR draft theo `ADR-0060` M6.

**Phân loại theo `ADR-0060`:** M3 Windows = `not_required` (bước 3: mọi tệp của diff là `*.md`); M9
`full_mutant_audit` không áp (diff không chạm `.claude/dev/**`, `ops/**/*.py`, `.github/workflows/**`).

**Ngân sách đóng của PR** (đề xuất trong đặc tả; chủ kho chốt khi duyệt băm): ≤ 2 lượt CI Ubuntu (head hoặc attempt,
rerun cũng tính); 1 phiên executor; không gắn nhãn `windows`, không gọi tay `ci.yml`, không Windows CI. Hết trần
hoặc không biết mức đã dùng ⇒ dừng ở checkpoint chủ kho.

## 7. chua_do_duoc

- Kết quả `ai-dang-giu` (mục 1) đúng tới lúc đo, 15:10Z–17:08Z 06-11-2026; nó cũ đi theo từng nhánh mới, nên người cấp
  lease phải đo lại.
- Lời khai *"0 commit chạm vùng"* đúng tới 01:14Z 07-11-2026; đo lại khi viết ADR.
- Comment duyệt băm của chủ kho trên #1265: chưa có lúc viết.

## 8. Thay đổi so với r1

| nguồn | thay đổi |
|---|---|
| F05 `phep-khop-khong-phu-menh-de` (P2) | mục tiêu 1a đóng băng nguyên văn năm câu R1–R5; A4 khớp trọn từng câu R2–R5 kèm đột biến cho quan hệ bằng nhau, lượng từ, đích T, thành phần vùng, mã thoát |
| F01 (P2, ở B) | R2 nói thẳng nhánh tổ tiên không đọc vùng tại S, khớp hợp đồng receipt của B r2 |
| ghi chú review: A §0 không tái lập được | số 202/117/56 thay bằng 206/121/58 kèm lệnh và bộ lọc |
| ghi chú review: A6 phải ghim tên, lệnh, kết quả | mục tiêu 1g liệt kê sáu vị trí, đòi số dòng đã đọc; A6 đỏ khi thiếu một vị trí |
| ghi chú review: invariant `tree(H) = T` | mục tiêu 1d thêm T = tree(H); 1f giữ G4, chỉ thay G3 |
| ghi chú review: cột cổng §20 | dòng §20 đóng băng nguyên văn; cột cổng ghi `0 cổng (đo lúc land A)` theo ba giá trị hợp lệ của §20 |
| ghi chú review: vế L6 không áp phải ghi | thêm bảng năm vế L6 dưới mục 4 |
| F08 (P3, ở B) | A giữ mốc hiệu lực land B; B r2 sửa câu tóm tắt cho khớp |
