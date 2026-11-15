# ADR-0066 — Admission thu-hoi: bỏ "S tổ tiên H", thay bằng cổng vùng bằng nhau ở mọi merge-base

- **Trạng thái:** Accepted — hiệu lực từ commit land của packet `THU-HOI-ADMISSION-MERGE-BASE-B` (mục *Hiệu lực*).
  Chủ kho `ducthangho` duyệt `spec_hash` `10fe7e052b3e0f4c0acc79e844b6d746466e6b3c98fa030222a08df80203d855` của đặc tả
  `THU-HOI-ADMISSION-MERGE-BASE-A` r13 trên Issue packet #1265:
  https://github.com/ducthangho/tra-luat/issues/1265#issuecomment-6719830665
- **Nguồn:** packet `THU-HOI-ADMISSION-MERGE-BASE-A` #1265 (Mission #1264), đặc tả
  `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-A-r13.md`. Packet anh em mang mã: `THU-HOI-ADMISSION-MERGE-BASE-B` #1266.
- **Ký hiệu:** S = `pull_request.base.sha` mà workflow truyền cho bộ kiểm; H = head của PR; T = tree(H); C = commit
  `workflow_sha` cung cấp mã canonical; B = một merge-base của (S, H); M = commit merge lúc land.

## Bối cảnh

Bộ kiểm `kiem-thu-hoi-github` (`ops/lease_publish.py`, hàm `lenh_kiem_thu_hoi_github`) đòi S là tổ tiên của H, rồi
kiểm trên T. Chủ kho giữ điều kiện ấy ngày 24-09-2026 ở #618
(https://github.com/ducthangho/tra-luat/issues/618#issuecomment-5819533474) với lý do: nếu H không chứa S, một bản thu
hồi thêm vào master sau khi nhánh rẽ sẽ vắng trong T, và bộ kiểm *"không phân biệt được 'PR xoá revocation' với 'PR
chưa thấy nó'"*. Đặc tả cha `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` r9 (sha256
`465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79`) ghi cùng ý ở gạch *"Strict up-to-date: S tổ tiên
H, merge giữ tree H …"*.

Giá của điều kiện ấy, đo ngày 15-11-2026 trên kho đã fetch đủ lịch sử:

- `git log --merges --since=2026-10-16T00:00:00Z --until=2026-11-06T08:25:00Z 08bcb51f` ra 571 commit merge; 206 trong
  số đó có tiêu đề chứa nguyên chuỗi `origin/master`, tức là merge master vào nhánh. Mỗi lần merge như vậy tạo head
  mới và làm mất hiệu lực mọi bằng chứng neo SHA. Đặc tả r13 mục 0 đo thêm trên cùng cửa sổ: 121 commit có thân, 58
  nhắc `thu-hoi`; hai số này ADR chép từ đặc tả, không đo lại. Phép đếm không tách được lần merge nào do admission
  đòi và lần nào vì lý do khác, nên 206 là trần, không phải số lần admission gây ra.
- Vùng mà bộ kiểm đọc chưa từng đổi trên master:
  `git log --first-parent --format=%H 426d1b0 -- ops/thu-hoi .github/coordination/change-impact.v1.json` ra 0 commit.
  Tại `426d1b0`, `ops/thu-hoi` vắng và tệp policy chưa tồn tại.

Tức điều kiện "S tổ tiên H" đòi mọi PR có head không chứa S phải hoà base thì cổng mới xanh, trong khi tình huống nó
chống (master đổi vùng sau khi nhánh rẽ) chưa xảy ra lần nào.

## Quyết định

Năm câu R1–R5 dưới đây là luật. Phần còn lại của ADR giải thích và không nới chúng.

**R1.** Bộ kiểm admission thu-hoi không còn đòi S là tổ tiên của H.

**R2.** Nếu S là tổ tiên của H, bộ kiểm chạy mọi phép kiểm trước ADR này và không so vùng; ngoài các phép đọc trước
ADR này, nó chỉ đọc thêm các commit cần để xác định quan hệ giữa S và H.

**R3.** Nếu S không phải tổ tiên của H, với mọi merge-base B của (S, H), vùng bộ kiểm đọc tại B phải giống hệt vùng
ấy tại S; sau đó mọi phép kiểm hiện có chạy trên T = tree(H).

**R4.** Vùng gồm bản đồ `ops/thu-hoi/**` (đường dẫn → mode, kiểu, OID) và mục
`.github/coordination/change-impact.v1.json` (vắng, hoặc mode, kiểu, OID).

**R5.** Một merge-base có vùng khác vùng tại S, không có merge-base, vượt ngân sách duyệt, thiếu object, object băm
không khớp tên hoặc header commit không đọc được ⇒ rc 12.

Quan hệ giữa S và H có ba trạng thái, và bộ kiểm phải tách đủ cả ba: *là tổ tiên* (R2), *không phải tổ tiên* (R3), và
*không đo được* (R5, rc 12). Trạng thái thứ ba không được xếp vào một trong hai trạng thái đầu. Bộ kiểm tự xác định
quan hệ ấy bằng cách đọc commit qua bộ đọc object có băm lại; giá trị `base.sha` và tên nhánh do workflow truyền chỉ
là đầu vào, không phải bằng chứng về quan hệ.

## Vì sao đủ

Lý do của #618 là bộ kiểm không tách được hai trường hợp khi H không chứa S. Luật mới tách chúng bằng vùng tại B:

- **PR xoá một bản ghi.** Bản ghi mà PR xoá phải có mặt ở chỗ nhánh rẽ, tức tại B. R3 đòi vùng tại B giống hệt vùng
  tại S, nên bản ghi ấy cũng có tại S. Phép append-only S→T hiện có thấy nó có ở S mà vắng hoặc khác ở T, và chặn.
- **PR chưa thấy một bản ghi.** Trường hợp này chỉ tồn tại khi master thêm hoặc đổi vùng sau B. Khi đó vùng tại S
  khác vùng tại B, và cổng trả rc 12 theo R5. PR phải hoà base đúng lúc ấy, không sớm hơn.

Khi vùng tại mọi B bằng vùng tại S, mọi khác biệt của vùng giữa S và T đều do nhánh của PR gây ra, nên kiểm S→T trên
T cho cùng kết luận như khi H chứa S.

## Thay những gì

ADR này thay đúng hai điểm:

1. Gạch *"Strict up-to-date: S tổ tiên H, merge giữ tree H …"* của `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` r9 (sha256
   `465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79`), ở phần áp cho bộ kiểm admission. Tệp đặc tả ấy
   đã đóng băng và không bị sửa; phần còn lại của gạch (bên tiêu thụ so base và head ngay trước land) không thuộc ADR
   này.
2. Quyết định (a) của chủ kho ở #618, `issuecomment-5819533474`: *"giữ chốt tổ tiên của bộ kiểm như thiết kế"*.

Các câu của `docs/PROTOCOL_DA_PHIEN.md` về đo ancestry ở phần preflight admission vẫn đúng nguyên văn và không đổi.

## Giữ nguyên

- S là tổ tiên của C (chống lùi định nghĩa của bộ kiểm).
- Mã canonical lấy từ `workflow_sha`.
- H tải về phải bằng `pull_request.head.sha`.
- T = tree(H).
- Append-only S→T.
- Validator chạy trên toàn namespace của T.
- Chế độ chưa kích hoạt đòi tập revocation rỗng ở cả S lẫn T; `SO_THU_HOI_KICH_HOAT = False`.
- Bộ đọc object có băm lại, bỏ qua `refs/replace` và graft của kho nguồn.

Ba phép đọc tại S của bộ kiểm nền giữ nguyên ở **cả hai** chế độ (S là tổ tiên, S không phải tổ tiên). Vị trí đo ngày
15-11-2026 trên `426d1b0`, tệp `ops/lease_publish.py`:

| phép đọc tại S | dùng cho | dòng |
|---|---|---|
| bản đồ sổ `ops/thu-hoi` | append-only S→T | 2364 |
| mục policy, khi T có marker mới (Q13) | chốt "S chưa có policy" | 2400 |
| OID của bộ kiểm | receipt | 2411 |

Câu R2 chỉ cho đọc thêm các commit của bước xác định quan hệ, và không cấm ba phép đọc ấy.

Hệ quả của việc đọc thêm commit:

1. Các con số đo tài nguyên (`object đã băm` trên dòng `THU_HOI_ADMISSION`, `so_object_da_doc`, `tong_bytes`) có thể
   lớn hơn nền.
2. Ngân sách của bộ đọc dùng chung cho mọi bước, nên bộ kiểm mới có thể chạm trần ở chỗ nền không chạm.
3. Một commit chỉ được đọc thêm để xác định quan hệ mà header không đọc được (ví dụ dòng `committer` hỏng) cũng làm
   bộ kiểm mới trả 12 ở chỗ nền trả 0.

Cả (2) lẫn (3) cho rc 12 theo R5. Ở nhánh S là tổ tiên của H, hai hệ quả ấy chỉ đổi kết quả theo một chiều: một đầu
vào nền trả 0 có thể thành 12 vì ngân sách hoặc vì header, còn ngân sách và header không làm đầu vào nào nền trả 12
thành 0. Nhận định này chỉ nói về hai loại lỗi ấy ở nhánh ấy. Nó không nói về nhánh S không phải tổ tiên của H: ở đó
R3 thay điều kiện ancestry, nên bộ kiểm mới cố ý nhận một số đầu vào mà nền từ chối bằng rc 12.

Receipt lên `schema_version` 2, và khoá `ngan_sach` có thêm `max_commits_merge_base`. Hợp đồng của receipt mới so với
nền nằm ở packet B (đặc tả `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-B-r13.md`, mục tiêu 4).

## Hiệu lực

Luật này có hiệu lực từ commit land của packet `THU-HOI-ADMISSION-MERGE-BASE-B` trên first-parent master; trước commit
ấy luật cũ giữ nguyên, và luật không hồi tố.

Từ lúc ADR này land tới lúc B land, bộ kiểm trên master vẫn là bản đòi S là tổ tiên của H. Trong khoảng ấy ADR là văn
bản đã duyệt mà chưa có mã thi hành.

## Nghĩa vụ cho packet khác

- **#1179 (C1a1b):** thay G3 *"S ≤ H"* bằng hợp đồng của ADR này trước khi đóng băng đặc tả. G4 *"tree(H) = T"* **giữ
  nguyên**: bỏ G3 không cho phép bỏ ràng buộc T với H.
- **Bên kiểm lúc land (#499 C1/C1b):** so vùng của tree(M) với vùng của T, và kiểm `M^2 == H`.
- **A1b (#656), khi bật sổ:** mở rộng vùng của R4 sang những gì bộ kiểm khi ấy đọc thêm (lease theo ID), và quyết lại
  dòng *"Q3-diễn giải"* (strict up-to-date). Strict không còn cần cho mục đích của bộ kiểm này.

Luật theo ID lease và việc kiểm lại lúc land không thuộc ADR này; chúng thuộc A1b và bên tiêu thụ receipt.

## Cưỡng chế

Đo ngày 15-11-2026 trên base của lease, `426d1b06e292a7db272a0f942bef0794479b58a6`, cho sáu vị trí cổng mà
`docs/PROTOCOL_DA_PHIEN.md` §20 liệt kê. Cột "số dòng đã đọc" là `git show <base>:<tệp> | wc -l`; số khác 0 cho biết
tệp đọc được, nên kết quả 0 là "đọc được, 0 lần nhắc", không phải "không đọc được".

- `ops/lease_publish.py` — lệnh `git show 426d1b06e292a7db272a0f942bef0794479b58a6:ops/lease_publish.py | grep -c 'ADR-0066'`; số dòng đã đọc 2604; kết quả 0.
- `.claude/dev/packet_loop.py` — lệnh `git show 426d1b06e292a7db272a0f942bef0794479b58a6:.claude/dev/packet_loop.py | grep -c 'ADR-0066'`; số dòng đã đọc 6247; kết quả 0.
- `.claude/dev/launcher.py` — lệnh `git show 426d1b06e292a7db272a0f942bef0794479b58a6:.claude/dev/launcher.py | grep -c 'ADR-0066'`; số dòng đã đọc 5988; kết quả 0.
- `.claude/dev/gate_lifecycle.py` — lệnh `git show 426d1b06e292a7db272a0f942bef0794479b58a6:.claude/dev/gate_lifecycle.py | grep -c 'ADR-0066'`; số dòng đã đọc 1688; kết quả 0.
- `.github/workflows/ci.yml` — lệnh `git show 426d1b06e292a7db272a0f942bef0794479b58a6:.github/workflows/ci.yml | grep -c 'ADR-0066'`; số dòng đã đọc 1184; kết quả 0.
- `.github/workflows/ops-publish-lease.yml` — lệnh `git show 426d1b06e292a7db272a0f942bef0794479b58a6:.github/workflows/ops-publish-lease.yml | grep -c 'ADR-0066'`; số dòng đã đọc 277; kết quả 0.

Lúc ADR này land: **0 cổng**. Không cổng nào đọc luật, và bộ kiểm trên master vẫn thi hành luật cũ.

Sau khi packet B land, cổng đọc luật là `ops/lease_publish.py`, lệnh `kiem-thu-hoi-github`. Lời khai ấy nói về tương
lai và chỉ đúng khi có phản chứng của B (ca B1–B9 trong đặc tả B); một lần nhắc `ADR-0066` trong tệp cổng không chứng
minh điều đó.

## Phương án bị loại

| phương án | lý do loại |
|---|---|
| Giữ "S tổ tiên H" | Mọi PR có head không chứa S phải hoà base thì cổng mới xanh (trần đo được: 206 commit merge master vào nhánh trong ba tuần, không tách được phần do admission), trong khi vùng cần bảo vệ có 0 commit từng chạm. |
| Strict up-to-date trên ruleset | Cùng cái giá hoà base, áp cho mọi PR của kho, kể cả PR không liên quan tới sổ thu hồi. |
| Merge ba chiều trong vùng sổ | Bộ kiểm phải tự quyết kết quả merge của sổ append-only; một sai sót ở bước ấy là sai sót trong chính sổ thu hồi. So bằng nhau đơn giản hơn và fail-close. |
| Tính toàn bộ cây merge-tree(S, H) bằng Git plumbing | Trái thiết kế bộ đọc có băm: bộ kiểm chỉ tin object nó tự đọc và băm lại, không tin kết quả của một lệnh Git chạy trên kho nguồn. |
| Merge queue native | Kho thuộc tài khoản User. Ngoài ra workflow `merge_group` lấy định nghĩa từ commit của nhóm merge, nên một PR sửa được chính workflow kiểm nó. |

## Giới hạn

- ADR này không mang mã. Mọi câu về hành vi của bộ kiểm mới là yêu cầu cho packet B, chưa phải phép đo.
- Phép đếm 0 commit chạm vùng đúng tới `426d1b0`. Khi sổ được bật (A1b), vùng sẽ đổi trên master và rc 12 theo R5 sẽ
  bắt đầu xuất hiện ở các nhánh rẽ trước lần đổi ấy; đó là hành vi mong muốn.
- Vị trí dòng trong bảng ở mục *Giữ nguyên* là của `426d1b0` và sẽ trôi khi tệp đổi.
