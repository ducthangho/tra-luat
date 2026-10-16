# ĐẶC TẢ PACKET — `THU-HOI-LEASE-VA-CAP-LAI`

```yaml
packet_id: THU-HOI-LEASE-VA-CAP-LAI
packet_issue: CHƯA CÓ          # điền khi đăng Packet Issue (Bước 3); spec này đóng băng TRƯỚC Issue
revision: 1
review_class: sensitive        # chạm ops/lease_publish.py (lease/publish authority) + .claude/dev/packet_loop.py — §8, fail-closed
executor: claude
reviewer: codex
assurance_target: cross_approved
base_sha: b416830ef2a509d60203d55552ce17950afcf67c   # origin/master lúc đóng băng, đo 13:41Z 07-09-2026
```

**Mọi con số trong tệp này đo lúc `13:2x–13:4xZ 07-09-2026` trên `303` ref** (302 tên nhánh máy chủ +
1 nhánh cục bộ `master`; `git ls-remote --heads origin` so `git for-each-ref refs/remotes/origin` bằng
TẬP TÊN: `comm -23` = **0**, `comm -13` = **0**) trừ khi ghi khác. **Đo lại trước mỗi bước công bố** (L5).
Đơn vị (L1): "lease" = **cặp (blob, đường dẫn) duy nhất** trên mọi ref; "lease_id" = giá trị trường
`lease_id`; "ref" = một dòng của `git for-each-ref refs/heads refs/remotes` trừ `*/HEAD`.

## `nguon_cap_viec`

- Lệnh của chủ kho lập phiên này (`session_01Vt7NfNpABHfSWpxvx4aJGE`, 07-09-2026): *"bổ sung cơ chế
  CHỦ KHO THU HỒI LEASE và CẤP LẠI CHO MỘT PR KHÁC"*. Câu chat KHÔNG phải neo; neo là Packet Issue sẽ
  đăng ở Bước 3.
- Nợ có tên `AG-T0-01B-thu-hoi-lease-chua-co-duong` (`ops/specs/ag-t0-01b-r4.md` §0.2; `CLAUDE.md` mục
  *"LEASE KHÔNG TỰ CHẾT KHI PACKET ĐÃ LAND"*).
- Nợ #473, mục `bia-mo-check-bo-sot-chieu-nguoc` và `cong-check-thieu-do-phu-tham-quyen` (P2 cross-review
  lượt 2 của PR #471) — packet này đóng phần "bia mộ theo từng blob"; phần "bốn trường phái sinh" KHÔNG.
- Lease g2 `wp461-…-exec-1g2-claude-20260907` (nhánh `ops/lease-wp461-g2`, PR #474), khoá
  `hoi_tu_nguoi_giu_doi_thao_tac.no_nen`: *"bia mộ tính theo lease_id toàn kho thay vì theo từng blob"*.

## 0. Vấn đề — ĐÃ ĐO, không phải suy đoán

Hôm nay chỉ có **một** đường thu hồi: bia mộ hai chiều (`thay_the_cho` ở lease mới ↔ `da_bi_thay_the` ở
lease cũ), ép bởi `ops/lease_publish.py::_kiem_bia_mo` (dòng 595–617). Nó THỦNG vì bia mộ là **dữ liệu ghi
vào TỆP CŨ**, mà tệp cũ có **nhiều bản sao** trên nhiều ref:

| phép đo | giá trị |
|---|---|
| ref quét | **303** |
| cặp (blob, đường dẫn) trong `ops/leases/` | **288** |
| đường dẫn lease | **273** |
| lease_id có **>1 blob** (tức đã bị sửa sau khi đăng, thường là để đặt bia mộ) | **7 / 273** |
| lease_id `CÒN_HẠN` | **8** |
| trong đó CHƯA bia mộ trên ≥1 ref | **4**: `gate-tach-…-1r4` (1 ref) · `mutant-khong-chay-…-exec-1` (**11** ref, có bia mộ trên 1 ref) · `wp461-…-1g2` (1 ref) · `wp461-…-1r2` (**4** ref, có bia mộ trên 1 ref) |

Ca thật đang chạy, `wp461`:

```
$ python3 ops/lease_publish.py ai-dang-giu .claude/dev/launcher.py        # 4,1 s, rc=11
CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ  wp461-…-exec-1-claude    refs/heads/master:…
CÒN_HẠN                    wp461-…-exec-1r2-claude  refs/heads/master:…                      blob 26f07b4  (0 bia mộ)
CÒN_HẠN                    wp461-…-exec-1g2-claude  refs/remotes/origin/ops/lease-wp461-g2:…
CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ  wp461-…-exec-1r2-claude  refs/remotes/origin/ops/lease-wp461-g2:…  blob fdfde3a  (1 bia mộ)
NGƯỜI_GIỮ 2: wp461-…-exec-1g2-claude-20260907, wp461-…-exec-1r2-claude-20260907
```

Blob `26f07b4` (r2, KHÔNG bia mộ) nằm trên **4** ref: `refs/heads/master` · `origin/master` ·
`origin/ops/cap-lease-461` · `origin/claude/soan-spec-3-viec-treo-20260906`. Blob `fdfde3a` (r2, CÓ bia mộ)
chỉ trên `origin/ops/lease-wp461-g2`. Kết quả trên CẢ BỐN đường ghi của wp461: `NGƯỜI_GIỮ 2`.

Ba hệ quả, mỗi hệ quả có dòng mã:

1. **`check` dùng `any(...)`** (`_kiem_bia_mo`, dòng 606–610): MỘT bản sao có bia mộ trên BẤT KỲ ref nào
   là đủ để `rc=0 ĐĂNG ĐƯỢC`. Nên g2 đăng lọt, còn `ai-dang-giu` vẫn đếm hai người giữ. Hai cổng bất đồng.
2. **`check` KHÔNG đo chồng lấn write set** (không chỗ nào trong `kiem()` gọi `_lease_cham_duong`). `rc=0`
   của `check` không nói gì về độc quyền.
3. **Bia mộ nằm trên nhánh `ops/**` — thân chính `master` vẫn thấy lease cũ sống** cho tới khi nhánh ấy
   merge; và merge xong thì mọi nhánh đã rẽ trước đó (#468) vẫn mang bản chưa bia mộ. Đây là CẤU TRÚC:
   bia mộ đuổi theo bản sao và không bao giờ đuổi kịp.

Tiền lệ thứ hai, cùng hình dạng: lease `mutant-khong-chay-tren-windows-exec-1-claude-20260906` (packet
#456) có bia mộ trên **1** ref (`origin/claude/soan-spec-3-viec-treo-20260906`) và KHÔNG bia mộ trên **11**
ref; hết hạn `2026-09-07T14:30:07Z`. Hai lần trong hai ngày ⇒ đủ để nói hình dạng lỗi này lặp (L4).

**Bất biến đúc kết** (neo quyết định vào đây, không vào con số): *một lease được CẤP ở bất kỳ ref nào
(chỉ có thể THÊM người giữ — chiều an toàn), nhưng một lease chỉ có thể bị THU HỒI ở đúng MỘT chỗ mà mọi
phép đo đều đọc.* Hôm nay chỗ ấy không tồn tại.

## 1. Sáu câu hỏi — trả lời kèm phép đo

### Q1 — Chủ kho phát lệnh thu hồi ở ĐÂU để nó có hiệu lực trên mọi ref?

➡️ **Sổ thu hồi append-only trên nhánh mặc định: `ops/thu-hoi/<lease_id>.yaml`**, mỗi lease bị thu hồi
một tệp, tên tệp = `lease_id` (charset đã bị `LEASE_ID` ép về ASCII `[A-Za-z0-9._-]`, an toàn làm tên tệp).
**Hiệu lực = tệp có mặt tại `refs/remotes/origin/<nhánh mặc định>`** — không phải trên cây làm việc, không
phải trên nhánh tính năng, không phải trên `refs/heads/master` cục bộ. Bản ghi nằm ở ref khác thì tính là
**CHƯA thu hồi** (fail-close về phía "còn giữ").

Vì sao KHÔNG phải các phương án khác — đã cân nhắc, không chép gợi ý:

| phương án | vì sao loại |
|---|---|
| Sửa tệp lease cũ trên MỌI ref | Phải đẩy vào nhánh của người khác (`#468` có 28 commit riêng, `ops-don-ref` cấm xoá); phiên web không xoá/force ref. Bất khả thi, và là chính lỗi hiện nay |
| Bia mộ trong CÙNG nhánh `ops/**` với lease mới (hiện trạng) | Chỉ thấy được từ nhánh ấy; `NGƯỜI_GIỮ 2` là phép đo của chính phương án này |
| Chỉ dùng comment Issue của chủ kho làm sổ | Online-only; `ai-dang-giu` cố ý offline + fail-close (`LEASE-HOI-TOAN-KHO` M2). Comment là hiện vật SỬA ĐƯỢC (`kiem()` dòng 797–811 đã trả giá) |
| `git notes` / ref riêng `refs/thu-hoi/*` | Không fetch mặc định, không đi qua PR, không diff được trong review; phiên web đẩy được `refs/heads/*` nhưng ref lạ chưa đo |
| Đặt sổ trong `ops/leases/thu-hoi/` | `_quet_lease_toan_kho` dùng `ls-tree -r` nên sẽ đọc bản ghi thu hồi như một LEASE và `rc=12` YAML sai lược đồ; `ops-publish-lease.yml` lọc `ops/leases/**.yaml` sẽ cố ĐĂNG nó. Phải nằm NGOÀI `ops/leases/` |

Phép đo cho Q1: sau khi có bản ghi trên `origin/master`, `ai-dang-giu` trên cả bốn đường của wp461 phải
đọc **đúng một ref** (`origin/master`) để kết luận r2 chết trên **cả 4 ref** mang blob `26f07b4` — xem A1.

### Q2 — Làm sao chứng minh danh tính chủ kho?

Đo trước, kết luận sau:

| đối tượng | login GitHub | ai tạo thật |
|---|---|---|
| merge commit `b416830` (PR #471) | `author.login = ducthangho`, `committer = web-flow`, có `gpgsig` (1) | chủ kho bấm merge trên web |
| commit `6635379` (lease r2, đẩy từ phiên Claude) | `author.login = claude` (map từ `noreply@anthropic.com`), không chữ ký | phiên agent |
| **actor** của 5 lượt `ops-publish-lease.yml` gần nhất (run 372–376) | **`ducthangho`** cả 5 | 5/5 do phiên agent push bằng PAT của chủ kho |
| comment Issue do phiên đăng qua MCP | `ducthangho` | phiên agent |

Kết luận **đã được chính merge commit `b416830` thừa nhận**: *"Mọi object mang login ducthangho không phân
biệt được chủ kho gõ với agent gõ hộ bằng PAT"*. `GITHUB_ACTOR` — lớp neo "GitHub xác thực" của
`kiem()` (dòng 833–839) — cũng trả `ducthangho` cho push của agent. **Trong tài khoản chủ kho, KHÔNG có ranh
giới máy nào tách "chủ kho" khỏi "agent cầm PAT của chủ kho".** Spec này không bịa ra một ranh giới ấy.

➡️ Vì vậy bản ghi thu hồi dùng **ĐÚNG chuẩn thẩm quyền của bản ghi CẤP**, không yếu hơn và không giả vờ
mạnh hơn:

1. `thu_hoi_boi` ∈ `NGUOI_CO_THAM_QUYEN` (danh sách CHO PHÉP; tên provider ⇒ `rc=4 RC_TU_CAP`) — cùng hai
   chốt, cùng thứ tự với `granted_by`.
2. `can_cu`: URL một object GitHub **readback được** do tài khoản chủ kho tạo (Issue/comment/PR review),
   thân object phải chứa đúng `lease_id` bị thu hồi. Lớp ONLINE (`kiem-github`, chạy trong workflow) đọc
   lại object ấy và đòi `user.login ∈ NGUOI_CO_THAM_QUYEN`. Lớp này phân biệt được **tài khoản chủ kho**
   với **tài khoản khác** (collaborator, bot) — đó là toàn bộ thứ GitHub xác thực được, và spec nói đúng
   như vậy.
3. **Hiệu lực chỉ khi trên `origin/<mặc định>`** (Q1) ⇒ bản ghi phải đi qua merge vào nhánh mặc định — cùng
   hành vi chủ kho đã làm cho mọi lease (`b416830`, `d28c4b1`, …). Merge là *hành vi* thu hồi; tệp chỉ
   là *lời khai*.

Lớp thứ tư, **NGOÀI phạm vi, nói thẳng vì sao**: xác minh chữ ký `web-flow` của merge commit đưa bản ghi vào
master (`git verify-commit` với khoá công khai GitHub vendor trong kho) sẽ tách được "merge trên web" khỏi
"push thẳng bằng PAT". Chưa làm vì (a) `curl https://github.com/web-flow.gpg` từ container này trả **HTTP 403,
249 byte** — không lấy được khoá để đo; (b) chủ kho push thẳng từ máy mình cũng KHÔNG có chữ ký ấy, chốt sẽ
chặn oan; (c) `%G?` của `b416830` là `E` (không kiểm được vì thiếu khoá) — tức chưa có phép đo dương nào.
Ghi vào `chua_do_duoc`.

### Q3 — Lease mới neo vào bản ghi thu hồi kiểu gì để `check` không còn dựa vào `any(...)`?

➡️ Lease mới GIỮ `thay_the_cho: [X, …]` (schema hiện có, không đổi). `check` thay `any(...)` trên mọi ref
bằng **vị từ đọc ĐÚNG MỘT ref**:

```
thu_hoi_hieu_luc(X, lease_moi) :=
      tồn tại origin/<mặc định>:ops/thu-hoi/X.yaml
        và bản ghi ấy .lease_id == X
        và (.cap_lai_cho rỗng  hoặc  .cap_lai_cho == lease_moi.lease_id)
  HOẶC origin/<mặc định>:ops/leases/X.yaml có .da_bi_thay_the == lease_moi.lease_id     # tương thích ngược, xem Q6
```

Thiếu vế nào ⇒ `rc=8` kèm thông điệp nói tệp nào thiếu ở ref nào. Không đọc `refs/heads/*` cục bộ, không đọc
head được đẩy, không quét toàn kho cho câu hỏi này. Kèm hai chốt mà #473 đã đo là thiếu:

- **Chiều ngược** (`bia-mo-check-bo-sot-chieu-nguoc`): `check` cho lease `L` còn phải hỏi *"có bản ghi
  `ops/thu-hoi/L.yaml` nào trên `origin/<mặc định>` không?"* — có ⇒ `rc=8` (đăng một lease đã bị thu hồi).
- **Độc quyền write set khi cấp lại** (`cong-check-thieu-do-phu-tham-quyen`, phần hẹp): khi `thay_the_cho`
  KHÔNG rỗng, `check` chạy phép tính người giữ (cùng hàm với `ai-dang-giu`, sau khi áp sổ thu hồi) cho TỪNG
  đường trong `write_set`; còn người giữ nào ngoài chính lease đang kiểm ⇒ `rc=11 RC_DANG_GIU`. Phần TỔNG
  QUÁT (mọi lease, kể cả không thay thế) vẫn thuộc #473 — xem `ngoai_pham_vi`.

Trường mới trong lease (tuỳ chọn, chỉ để người đọc đối chiếu, **cổng KHÔNG dùng để quyết**):
`thu_hoi_can_cu: {X: ops/thu-hoi/X.yaml@<sha40 commit master>}`.

### Q4 — `ai-dang-giu` đổi thế nào để MỘT lệnh thu hồi làm rụng TOÀN BỘ bản sao trên 303 ref?

➡️ Sau `_quet_lease_toan_kho`, nạp sổ thu hồi **một lần** từ `origin/<mặc định>:ops/thu-hoi/` (`ls-tree` +
`cat-file`, `yaml.safe_load`, fail-close `rc=12` khi YAML hỏng, tên tệp ≠ `lease_id`, hoặc ref mặc định
không phân giải được). Với MỖI cặp (blob, path): `lease_id ∈ sổ` ⇒ in nhãn **`ĐÃ_THU_HỒI`** (vẫn in, không
biến mất — cùng lý do `A2c` của `LEASE-HOI-TOAN-KHO`), **không** vào tập người giữ, **bất kể** blob nào,
ref nào, có bia mộ hay không. Phân loại bia mộ hiện có giữ nguyên cho lease KHÔNG có trong sổ.

Hai chốt tươi, vì "quét mọi ref" từng quét đúng 3 ref (`CLAUDE.md`, mục `for-each-ref` đọc đệm):

- **M2 hiện có so TẬP TÊN — không bắt ref CŨ** (g2 `ddb3200` đo: nhánh #468 có tên đúng, trỏ commit cũ, đi qua
  sạch). Mở rộng: so **cặp (tên, SHA)** giữa `ls-remote --heads` và `for-each-ref refs/remotes/origin`;
  lệch SHA ở bất kỳ nhánh nào ⇒ `rc=12 KHÔNG_XÁC_ĐỊNH` kèm tên nhánh và hai SHA. Cùng lệnh, không thêm lời
  gọi mạng.
- Ref mặc định lấy từ `refs/remotes/origin/HEAD` (symref); vắng ⇒ `master`; cả hai vắng ⇒ `rc=12`.

Chi phí: một `ls-tree` + N `cat-file` với N = số bản ghi thu hồi (hôm nay **0**, sau di trú **1**), cộng
thêm 0 lời gọi mạng. Thời gian nền `ai-dang-giu` hiện **4,1 s** (đo 13:3xZ) — tiêu chí A6 đòi không quá 2×.

### Q5 — Công việc mà lease bị thu hồi đang làm dở thì sao? Có mất mát ghi không?

Đo trước: `git ls-remote --heads origin 'refs/heads/agent/wp461*'` ⇒ **RỖNG** (g2 đã đo 09:49Z, đo lại
13:4xZ vẫn rỗng) — wp461 chưa có commit nào mồ côi. Nên ca thật hôm nay không mất gì; spec vẫn phải trả lời
cho ca tổng quát:

➡️ **Git không mất commit; thứ mất là QUYỀN, và nó mất có chủ đích** — đúng §4: *"Worker cũ sống lại không
thể heartbeat, push hợp lệ hoặc handoff. Branch/PR cũ chuyển `stale`; generation mới được đọc diff cũ nhưng
không tự cherry-pick."* Ba chỗ cưỡng chế:

1. **Phía executor cũ** (`.claude/dev/packet_loop.py`): `begin-attempt`, `record-post`, `record-review`,
   `transition` — mọi lệnh đi qua `_kiem_luoc_do_lease` — thêm phép hỏi *"`origin/<mặc định>:ops/thu-hoi/
   <lease_id>.yaml` có tồn tại không?"*; có ⇒ `RC_STATE`, ghi `history` sự kiện `lease_revoked_seen`, state
   → `stale`. Ref mặc định VẮNG (kho chưa fetch) ⇒ `RC_STATE` luôn — không đo được thì không mở lượt.
   **Giới hạn khai thẳng:** packet_loop KHÔNG fetch; nó đọc đệm. Đệm cũ ⇒ không thấy thu hồi mới. Đây là
   cùng khe với `hoi_tu_nguoi_giu_doi_thao_tac.chua_cuong_che_duoc` của g2; chốt có răng thật nằm ở (3).
2. **Phía lease mới**: `check` từ chối cấp lại khi còn người giữ (Q3) ⇒ không tồn tại cửa sổ hai lease cùng
   `ĐĂNG ĐƯỢC` cho cùng đường dẫn.
3. **Phía land** (NGOÀI write set, ghi nợ có tên): `land-packets` phải hỏi sổ thu hồi trước khi land một
   PR mang `lease_id` bị thu hồi. Chưa có cổng CI nào đọc lease lúc PR; nợ `LAND-DOC-SO-THU-HOI`.

Không có thao tác "gỡ thu hồi": sổ append-only; muốn cấp lại cho cùng người là một lease MỚI, `lease_id`
mới, `generation` mới (ADR-0025).

### Q6 — Tương thích ngược với bia mộ hai chiều hay thay thế nó? Di trú 4 lease đang sống ra sao?

➡️ **Thay thế cho mọi thu hồi MỚI; đọc tương thích cho lịch sử.** Cụ thể:

- `_bia_mo_doi_xung` và nhãn `ĐÃ_BỊ_THAY_THẾ` giữ nguyên để **5** cặp bia mộ đã có trên master (3 `gate-tach`,
  `wp461-…-exec-1`, `mutant-…` trên #468) vẫn đọc đúng. Không sửa hiện vật lịch sử.
- `check` chỉ còn nhận bia mộ **khi bản có bia mộ nằm trên `origin/<mặc định>`** (Q3, vế thứ hai). Bia mộ ghi
  trong cùng nhánh `ops/**` với lease mới ⇒ `rc=8`, thông điệp trỏ sang `ops/thu-hoi/`. Đây là điểm ĐỔI hành vi
  duy nhất với dữ liệu cũ, và nó cố ý.
- Di trú **4** lease `CÒN_HẠN` chưa bia mộ (đo 13:3xZ):

| lease_id | tình trạng | việc |
|---|---|---|
| `wp461-…-exec-1r2-claude-20260907` | phải chết; chủ kho đã ra lệnh trong lease g2 (`thay_the_cho`, `granted_by: ducthangho`, comment `#461` id `5569885143`) | **bản ghi thu hồi đầu tiên** — nằm trong write set, `can_cu` = comment ấy + PR #474 |
| `mutant-khong-chay-tren-windows-exec-1-claude-20260906` (#456) | hết hạn `2026-09-07T14:30:07Z`, tức trước khi packet này có lease | **KHÔNG di trú** — hội tụ bằng hết hạn, cùng đường (a) g2 đã nêu. Ghi lại làm tiền lệ, không sửa |
| `wp461-…-exec-1g2-claude-20260907` | người giữ hợp lệ | không đụng |
| `gate-tach-…-exec-1r4-claude-20260906` (#463) | người giữ hợp lệ, write set khác | không đụng |

## `write_set`

```
ops/lease_publish.py
ops/lease_publish_test.py
ops/thu-hoi/wp461-be-mat-thu-hai-cua-codex-exec-1r2-claude-20260907.yaml
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
```

Năm đường dẫn, liệt kê đủ, không ký tự đại diện. `ops/thu-hoi/…yaml` là **dữ liệu** — bản ghi thu hồi đầu tiên,
đồng thời là fixture sống cho A1; nó chỉ được viết khi chủ kho cấp lease cho packet này (tức đã chốt Q2 và
xác nhận `can_cu`).

**Kích thước — vượt trần ADR-0044, khai thẳng thay vì cắt test cho vừa.** Trần `sensitive`: ≤ 3 tệp, ≤ 300
dòng thêm. Mốc neo cùng vùng: `LEASE-HOI-TOAN-KHO` (PR #250) 2 tệp / +313; `PLAT-X8` 2 tệp / +265→+313. Packet
này có **5** tệp và ước **+450 ± 100** (lease_publish ≈ 120 · test ≈ 220 · packet_loop ≈ 40 · test ≈ 60 · dữ
liệu ≈ 20 — ước từ số ca A1–A9 bên dưới, chưa có diff). Hai lối, chủ kho chọn ở Q7 (§4):
(i) **tách hai slice**: A = `ops/lease_publish.py` + test + bản ghi (3 tệp) · B = `packet_loop.py` + test,
mọc trên A đã land; hoặc (ii) một packet, ngoại lệ ADR-0044 có ghi lý do: *"phần vượt là ca fail-close; cắt
ca để vừa trần là đổi độ phủ lấy con số"*. **Khuyến nghị (i)** — B không chặn A, và A mới là thứ gỡ cửa sổ
hai writer của wp461. Đo lại `git diff --numstat` trước vòng review; vượt ước tính thì dừng, không tự mở PR
thứ hai (ADR-0044).

## `ngoai_pham_vi`

| thứ | vì sao KHÔNG làm ở đây |
|---|---|
| Sửa `.github/workflows/ops-publish-lease.yml` để bắn khi đẩy `ops/thu-hoi/**` và đăng comment "đã thu hồi" | Tệp sensitive thứ 6, không cần cho hiệu lực: lớp online của bản ghi chạy qua `kiem-github` của LEASE MỚI (workflow đã gọi). Bản ghi thu hồi KHÔNG kèm lease mới thì chưa có comment tự động — nợ `THU-HOI-DANG-COMMENT` |
| Cưỡng chế `generation` / bốn trường phái sinh §3.2 (`change_policy_sha`…) | Nợ #473, khác gốc |
| Độc quyền write set TỔNG QUÁT ở `check` (cả lease không có `thay_the_cho`) | #473 `cong-check-thieu-do-phu-tham-quyen` phần rộng; ở đây chỉ làm ca cấp lại vì đó là ca đang thủng |
| `land-packets` đọc sổ thu hồi | Ngoài write set; nợ `LAND-DOC-SO-THU-HOI` (Q5.3) |
| Xoá nhánh `ops/cap-lease-461`, `ops/lease-wp461-g2` sau khi land | Thao tác phá, `ops-don-ref.yml` + chủ kho; và với sổ thu hồi thì **không còn cần** xoá để hội tụ — đó chính là điểm A1 đo |
| Nâng `timeout-minutes` trong `ci.yml` | Cấm cứng; hình dạng đã hỏng 3 lần |
| Sửa `CHANGELOG.md` | Nằm trong `RELEASE_MANIFEST.json`; sửa là kéo theo tái sinh manifest — việc của đợt phát hành, không của packet ops |
| Chữ ký `web-flow` (Q2 lớp 4) | Không lấy được khoá từ container (403); chặn oan push thẳng của chủ kho |
| Di trú lease `mutant-…-exec-1` (#456) | Hết hạn trước khi packet có lease; sổ ghi một lease đã chết là nhiễu |

## `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | Định nghĩa lược đồ bản ghi thu hồi + hàm nạp sổ từ `origin/<mặc định>:ops/thu-hoi/`, fail-close ba trạng thái | `ops/lease_publish.py` |
| **M2** | `ai-dang-giu`: áp sổ theo `lease_id` trên MỌI bản sao ⇒ nhãn `ĐÃ_THU_HỒI`, không vào tập người giữ; so hai nguồn bằng **(tên, SHA)** | `ops/lease_publish.py` |
| **M3** | `check`: thay `any(...)` bằng vị từ một-ref (Q3); chiều ngược (lease bị thu hồi không đăng được); độc quyền write set khi `thay_the_cho` không rỗng | `ops/lease_publish.py` |
| **M4** | `kiem-github`: đọc lại `can_cu` của từng bản ghi thu hồi mà lease mới dựa vào; `user.login ∈ NGUOI_CO_THAM_QUYEN` và thân chứa `lease_id` | `ops/lease_publish.py` |
| **M5** | Bản ghi thu hồi r2 — dữ liệu, đúng lược đồ M1 | `ops/thu-hoi/wp461-…-exec-1r2-claude-20260907.yaml` |
| **M6** | Ca `rXX_`/`tXXX` + đột biến cho M1–M4, kể cả ca sổ append-only | `ops/lease_publish_test.py` |
| **M7** | `_kiem_luoc_do_lease` hỏi sổ thu hồi; có ⇒ `RC_STATE`, state `stale`, history `lease_revoked_seen`; ref mặc định vắng ⇒ `RC_STATE` | `.claude/dev/packet_loop.py` |
| **M8** | Ca + đột biến cho M7 | `.claude/dev/packet_loop_test.py` |

### Lược đồ bản ghi thu hồi (M1)

```yaml
schema_version: 1
event: lease_revoked
lease_id: wp461-be-mat-thu-hai-cua-codex-exec-1r2-claude-20260907   # == tên tệp không đuôi, bắt buộc
packet_issue: 461                                                     # số nguyên dương, bắt buộc
thu_hoi_boi: ducthangho                                               # ∈ NGUOI_CO_THAM_QUYEN; provider ⇒ rc=4
thu_hoi_luc_utc: '2026-09-07T13:41:32Z'                               # ISO8601 có Z, bắt buộc; không được ở tương lai
ly_do: >-                                                             # bắt buộc, không rỗng
  …
can_cu: https://github.com/ducthangho/tra-luat/issues/461#issuecomment-5569885143   # bắt buộc; object GitHub readback được
cap_lai_cho: wp461-be-mat-thu-hai-cua-codex-exec-1g2-claude-20260907  # tuỳ chọn; rỗng = thu hồi không cấp lại
blob_da_biet_luc_ghi: [26f07b4fe49964034c710864f350402fe5bf55c3, fdfde3a57ab9fd2c83454e9b9b2eff96f77ef229]
                                                                      # tuỳ chọn, CHỈ để đối chiếu; cổng không dùng
```

Bất biến: **append-only** — tệp trong `ops/thu-hoi/` trên nhánh mặc định không bao giờ bị sửa hay xoá
(A8 đo bằng `git log --diff-filter=MD`). Khoá thừa ⇒ `rc=8` (cùng luật `lease-schema-allows-extra-keys`).

## `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó **ĐỎ** (L3). "Kho giả" = bare + working copy dựng trong thư mục tạm bằng
`_git_fixture`, có remote `origin` thật để `ls-remote` chạy (tiền lệ `t109`–`t113`).

**A1 — ca sống, đo trên đủ ref.** Sau khi bản ghi M5 có trên `origin/master`: `ai-dang-giu` trên CẢ BỐN đường
ghi của wp461 in dòng `ĐÃ_THU_HỒI` cho mọi bản sao r2 (**≥ 4** dòng, một cho mỗi cặp (blob, path) — đo lại số
ref lúc ấy) và kết thúc `NGƯỜI_GIỮ 1: wp461-…-exec-1g2-claude-20260907` (hoặc `0` nếu g2 đã land/hết hạn),
`rc` tương ứng; kèm phép so hai nguồn in `MÙ 0` với số ref đo được ghi vào biên nhận. ĐỎ khi: đột biến bỏ phép
nạp sổ (⇒ `NGƯỜI_GIỮ 2`), hoặc đột biến áp sổ theo **blob** thay vì `lease_id` (⇒ bản `26f07b4` vẫn giữ).
Đơn vị: số dòng `ĐÃ_THU_HỒI`, số người giữ, số ref.

**A2 — sổ ở ref khác KHÔNG có hiệu lực.** Kho giả: lease X còn hạn trên 3 ref; bản ghi thu hồi X chỉ trên
`origin/ops/thu-hoi-X` (không trên `origin/master`) ⇒ `ai-dang-giu` vẫn `NGƯỜI_GIỮ 1: X`; sau khi merge nhánh
ấy vào `origin/master` ⇒ `NGƯỜI_GIỮ 0` và **3** dòng `ĐÃ_THU_HỒI`. ĐỎ khi: đột biến nạp sổ từ mọi ref
(`any`) — vế trước đổi màu. Đơn vị: số người giữ, số dòng.

**A3 — `check` vị từ một-ref.** Kho giả, lease mới `Y` khai `thay_the_cho: [X]`: (a) không bản ghi, không bia
mộ ⇒ `rc=8`; (b) bản ghi X trên `origin/master`, `cap_lai_cho` rỗng ⇒ `rc=0`; (c) bản ghi có
`cap_lai_cho: Z ≠ Y` ⇒ `rc=8`; (d) bia mộ hai chiều nằm trên `origin/master` ⇒ `rc=0` (tương thích);
(e) bia mộ hai chiều CHỈ trong cùng nhánh `ops/**` với Y (hình dạng wp461 hôm nay) ⇒ `rc=8`, thông điệp có
chuỗi `ops/thu-hoi/`. ĐỎ khi: khôi phục `any(...)` — (e) đổi màu; bỏ so `cap_lai_cho` — (c) đổi màu. Năm ca,
năm mã thoát.

**A4 — chiều ngược.** Kho giả: bản ghi thu hồi cho chính `Y` trên `origin/master`; `check Y` ⇒ `rc=8`, thông
điệp chứa `ĐÃ_THU_HỒI`. ĐỎ khi: đột biến bỏ phép hỏi chiều ngược ⇒ `rc=0`.

**A5 — độc quyền khi cấp lại.** Kho giả: `Y` khai `thay_the_cho: [X]`, đường `p` trong `write_set` của Y còn
lease `W ≠ X` còn hạn giữ ⇒ `check Y` `rc=11`, thông điệp nêu `W` và `p`; gỡ W ⇒ `rc=0`. ĐỎ khi: đột biến bỏ
vòng lặp write_set ⇒ ca đầu `rc=0`. Kèm phản chứng phạm vi: lease KHÔNG có `thay_the_cho` với cùng W ⇒ `rc=0`
(đúng phạm vi hẹp đã khai — đột biến mở rộng phạm vi làm ca này đổi màu, để biết ca đang đo phạm vi).

**A6 — hai nguồn so (tên, SHA).** Kho giả: nhánh `b` cục bộ trỏ commit cũ hơn máy chủ, tên vẫn khớp ⇒
`ai-dang-giu` `rc=12`, thông điệp có `b` và hai SHA 7 ký tự. ĐỎ khi: đột biến quay về so tập tên ⇒ `rc≠12`.
Kèm: thời gian `ai-dang-giu` trên kho thật ≤ **2×** nền `4,1 s` (đo 3 lần, lấy trung vị; nền đo lại cùng lúc).

**A7 — fail-close ba trạng thái của sổ.** Kho giả: (a) bản ghi YAML hỏng ⇒ `rc=12`; (b) tên tệp ≠ `lease_id`
⇒ `rc=12`; (c) `thu_hoi_boi: codex` ⇒ `rc=4`; (d) `thu_hoi_boi: ai-codex-bot` ⇒ `rc=4`; (e) không phân giải được
`refs/remotes/origin/HEAD` lẫn `origin/master` ⇒ `rc=12`; (f) khoá thừa ⇒ `rc=8`; (g) `thu_hoi_luc_utc` ở tương
lai ⇒ `rc=8`. Bảy ca, bảy mã. ĐỎ khi: thay bất kỳ `raise` bằng `continue` — ca tương ứng thành `rc=0`. Kèm
đột biến **nới `NGUOI_CO_THAM_QUYEN` chứa `ai-codex-bot`** phải làm (d) ĐỎ (để biết ca đo danh sách, không đo
thứ khác — `CLAUDE.md`, mục danh sách cho phép).

**A8 — append-only.** Ca quét `git log --diff-filter=MD --name-only origin/master -- ops/thu-hoi/` trên kho
thật ⇒ **0** dòng; trên kho giả có một commit sửa bản ghi ⇒ **1** dòng và ca ĐỎ. Chốt "tha khi không phải kho
thật" chỉ được tha khi cây không có `.git` (bài học `t24`).

**A9 — `kiem-github` đọc `can_cu`.** Đồ giả GIỮ TRẠNG THÁI cho `gh api` (tiền lệ `t126`): (a) comment do
`ducthangho`, thân chứa `lease_id` ⇒ qua; (b) do `notebyme88` ⇒ `rc=4`; (c) thân không chứa `lease_id` ⇒ `rc=8`;
(d) 404 ⇒ `rc=12`; (e) 500 ⇒ `rc=12` (không đọc thân tự do — dòng trạng thái HTTP). ĐỎ khi: đột biến bỏ so
`user.login` ⇒ (b) `rc=0`.

**A10 — packet_loop.** Kho giả với state `leased` cho `lease_id: X`: (a) không bản ghi ⇒ `begin-attempt` `rc=0`;
(b) bản ghi X trên `origin/master` ⇒ `RC_STATE`, state tệp = `stale`, history có `lease_revoked_seen`;
(c) không có `refs/remotes/origin/*` ⇒ `RC_STATE`, thông điệp có `KHÔNG ĐO ĐƯỢC`; (d) bản ghi chỉ trên nhánh
khác ⇒ `rc=0` (đúng Q1). ĐỎ khi: đột biến đổi (c) thành cho qua ⇒ fail-open; đột biến bỏ ghi `stale` ⇒ (b) state
vẫn `leased`.

**A11 — nền không đổi.** `ops/lease_publish_test.py` và `.claude/dev/packet_loop_test.py`: **N/N** với N = nền
+ số ca mới, delta ca đỏ so `origin/master` = **0**, hai vế dựng trong **MỘT** lệnh (`CLAUDE.md`, mục delta).
Nền đo 13:4xZ 07-09: xem `chua_do_duoc` nếu chưa xong lúc đóng băng. `doc-claims-check --strict` `rc=0`
(nền `rc=0` đo 13:4xZ); `doctrine-scan` `rc=0` (nền: 7 tệp, 0 chỗ chép).

**A12 — bằng chứng dương, không tin `rc`.** Mọi lượt chạy bộ test trong biên nhận ghi **kích thước output
(byte)** và cặp `N/N`; `out=0B` ⇒ chưa chạy, không tính (bài học `/usr/bin/time` rc=127).

## `hinh_dang_ke_thua` (L4)

Chép từ hồ sơ tiền nhiệm, đếm HÌNH DẠNG lỗi:

| hình dạng | số lần | nguồn |
|---|---|---|
| "thu hồi là dữ liệu ghi vào bản sao, không đuổi kịp bản sao" | **2** (wp461-r2 · #456) | §0 |
| "lời khai hội tụ rộng hơn phép đo" (`merge xong là về 1` · `xoá một nhánh là đủ`) | **2** | g2 `3c4c587`, `ddb3200` |
| "hai cổng bất đồng về cùng hồ sơ" (`check rc=0` · `ai-dang-giu rc=12`) | **1** | #473 |

Cùng hình dạng thứ nhất đã tới **2**; lần thứ ba ⇒ hỏi "có nên làm cách này nữa không" (§12). Packet này chính
là câu trả lời "không": đổi CHỖ thu hồi, không vá bia mộ lần nữa.

## `chua_do_duoc`

1. **Ranh giới chủ kho / agent-cầm-PAT** — không đo được từ trong tài khoản (Q2). Spec không hứa; chỉ hứa
   "tài khoản chủ kho" theo `user.login`.
2. **Chữ ký `web-flow`** — `curl` 403 từ container; `%G?=E`. Chưa có phép đo dương nào.
3. **Kích thước diff** — chưa có diff; con số +450 ± 100 là ước từ số ca. Đo lại trước review.
4. **Nền N/N của hai bộ test** — đang chạy nền lúc đóng băng (`lease_publish_test.py` 121 hàm `t`,
   `packet_loop_test.py` 4733 dòng); số cụ thể ghi vào Packet Issue khi có, spec không giữ con số ấy.
5. **Độ tươi phía executor (Q5.1)** — packet_loop đọc đệm, không fetch; chưa có cách đo "đệm cũ bao nhiêu"
   từ trong lệnh. Chốt răng thật là (Q5.2) + nợ `LAND-DOC-SO-THU-HOI`.
6. **Hành vi `actions/checkout fetch-depth: 0` với `refs/remotes/origin/*`** trong `ops-publish-lease.yml`:
   bước "neo bộ kiểm" đã `fetch origin $MAC_DINH`, nên `origin/<mặc định>` có; nhưng M3-độc-quyền cần MỌI
   nhánh máy chủ (`_ten_nhanh_may_chu` so đệm) — chưa đo checkout có nạp đủ `refs/remotes/origin/*` không.
   Nếu không, `check` trong workflow `rc=12` ⇒ fail-close, và executor phải thêm `git fetch origin
   '+refs/heads/*:refs/remotes/origin/*'` vào bước ấy — **ngoài write set** ⇒ dừng, revision. Phải đo ở
   lượt thi công đầu tiên, TRƯỚC khi viết mã.
7. **Nguyên nhân `Connection refused (os error 111)` của codex** — chưa biết; vòng review chạy trong
   `setsid nohup … < /dev/null &`.

## 4. Câu hỏi chủ kho phải chốt khi cấp lease (mỗi câu có khuyến nghị)

❓ **Q7 — tách slice?** ➡️ (i) tách A/B như §`write_set`; A trước.
❓ **Q8 — `can_cu` của bản ghi r2?** ➡️ comment `#461` id `5569885143` (bản chiếu lease g2) + PR #474; nếu chủ
kho muốn một câu do chính mình gõ thì đăng một comment lên #461 *"thu hồi wp461-…-exec-1r2-claude-20260907"*
rồi lấy URL ấy — mạnh hơn, vì thân comment do tài khoản chủ kho tạo trực tiếp.
❓ **Q9 — sổ có nhận bản ghi cho lease ĐÃ hết hạn không?** ➡️ Nhận (không cấm), nhưng `ai-dang-giu` in
`HẾT_HẠN · ĐÃ_THU_HỒI`; cấm sẽ tạo cửa sổ đua giữa lúc soạn và lúc merge.
