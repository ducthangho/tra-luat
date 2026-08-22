# RÚT lease `plat-x8-exec-1-codex-20260821` — 21-08-2026

**Trạng thái: lease KHÔNG có hiệu lực và CHƯA TỪNG được đăng.** Không cần đường thu hồi — kho vốn
không có đường ấy (nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong`: cơ chế duy nhất được cài đặt là chờ
hết hạn). Bản ghi này tồn tại để lượt sau không đào lại từ đầu.

| khoá | giá trị |
|---|---|
| `lease_id` | `plat-x8-exec-1-codex-20260821` |
| packet | `PLAT-X8`, Issue #225 |
| đã đăng | **KHÔNG** — không có `posted_comment_id`, không có bản chiếu trên #225 |
| lý do rút | va chạm write set với `lease-dang-exec-2-codex-20260821` (#227), **cả về cửa sổ lẫn về nội dung** |
| người quyết | người giữ kho, in-session 21-08-2026 |

## Vì sao lease này KHÔNG được đăng — và đó là MAY, không phải chốt

`.github/workflows/ops-publish-lease.yml` **không chạy lần nào** trên lần đẩy tạo nhánh
`ops/plat-x8-lease-exec-1`. Đo: `list_workflow_runs` lọc theo nhánh ⇒ **0** lượt của workflow ấy;
chỉ `ops-open-pr.yml` chạy và `skipped`.

Nguyên nhân nhiều khả năng là **chốt `paths` không đánh giá được trên lần tạo NHÁNH MỚI** — không có
commit "before" để so, nên bộ lọc `paths: ops/leases/**.yaml` không khớp gì. Đối chứng trong cùng
kho: nhánh `ops/lease-dang-227` **đã tồn tại** và có **3** lượt chạy thành công trong cùng buổi.

**Nói thẳng phần chưa đo:** đây là suy luận từ hai quan sát, KHÔNG phải phép đo có phản chứng. Chưa
ai dựng ca "đẩy nhánh mới có tệp trong `ops/leases/`" để xem workflow có bắn không. Cho tới lúc có ca
ấy, **đừng trông vào việc nhánh mới không tự đăng** — nó là hành vi chưa được khoá, và lần này nó
tình cờ đứng về phía an toàn. Lần sau có thể không.

## Va chạm — đo được, hai tầng

### Tầng 1: cửa sổ

`lease-dang-exec-2-codex-20260821` (#227) — **đã đăng** (`posted_comment_id: 5370452295`),
`granted_by: ducthangho`, hiệu lực `2026-08-21T13:30:00Z` → `2026-08-22T13:30:00Z`, giữ
`ops/lease_publish.py` + `ops/lease_publish_test.py` + `.github/workflows/ops-publish-lease.yml`.

Lease `PLAT-X8` khai `leased_at_utc: 2026-08-21T13:45:00Z` ⇒ **chồng lấn ~23,75 giờ** trên hai tệp,
tức HAI writer cùng khai độc quyền. Đúng hình dạng P1 mà `ag-t0-01b-exec-1r2` đã phải chữa bằng cách
dời hiệu lực.

### Tầng 2: nội dung — và đây mới là tầng làm "dời hiệu lực" KHÔNG đủ

Nhánh thi công `codex/lease-dang-exec-1` đã có mã thật:

| đo | kết quả |
|---|---|
| `kiem()` bị sửa | **2 hunk** (`@@ -278`, `@@ -305`) |
| khối hằng ngay sau `RC_NEO = 6` | bị sửa (`@@ -42,6 +44,10`) |
| `BAT_BUOC` | bị sửa |
| hàm mới | `GOI_GH` `_doc_gh` `_repo_github` `_kiem_loai_so_hieu` `_kiem_comment_da_co` `kiem_github` `lenh_kiem_github` |
| bộ test | master **42** ca → nhánh 227 **58** ca |

`PLAT-X8` phải chèn `RC_LOP = 10` vào **đúng khối hằng ấy** và thêm chốt vai/`schema_version` vào
**đúng `kiem()`**. Hai bản vá cùng hàm, cùng vùng.

Dời hiệu lực chỉ chữa tầng 1. `PLAT-X8` vẫn khởi hành từ một base sắp bị thay ⇒ rebase + đo lại toàn
bộ. Nên quyết định là **xếp thứ tự**, không phải chạy song song:

```
#227 (LEASE-DANG-DUNG-MOT-LAN)  →  PLAT-X8 (#225)  →  #209  →  PLAT-X7 (#220)  →  gói spec-gate
```

## NGUYÊN NHÂN GỐC — phép đo hỏi chỗ TIỆN TAY

Đặc tả `ops/specs/plat-x8.md` §3 khai:

> *"không lease nào đang giữ `ops/lease_publish.py` hay `ops/lease_publish_test.py`"*

Câu ấy đo `ops/leases/` **trên master**. Đúng với master, **sai với thực tế**: lease sống nằm trên
các nhánh `ops/**` và chỉ về master sau khi merge. Quét đủ **98 nhánh `ops/**`** ra **7** lease còn
sống chạm hai tệp đó:

| lease | hết hạn | giữ | packet đã land? |
|---|---|---|---|
| `plat-x5-exec-1` … `1r4` (#206) | tới 22-08 01:50 | `_test.py` | **RỒI** — `ops/chay_lease_publish_test.sh` + `ops/cai_actionlint.sh` có trên master |
| `slice-b-c-exec-1` (#215) | 22-08 06:40 | `_test.py` | **RỒI** — dấu của nó có trong `ops/NO_KY_THUAT.md` trên master |
| `lease-dang-exec-1` (#227) | 22-08 12:00 | **cả hai** | **CHƯA** |
| `lease-dang-exec-2` (#227) | 22-08 13:30 | **cả hai** | **CHƯA** |

**ĐỌC CỘT CUỐI TRƯỚC KHI DÙNG SỐ 7.** Bản đầu của biên bản này đếm cả bảy là *"lease còn sống"*, và
cross-review bắt đúng chỗ đó (P2 trên PR "#228"): **"chưa hết hạn" KHÔNG phải "còn hiệu lực"**. Năm
lease đầu thuộc packet đã land — việc xong rồi, chỉ mốc hết hạn là chưa tới. Số va chạm THẬT với
`PLAT-X8` là **2**, cả hai của `#227`.

**Đừng đọc thành "vậy quét toàn nhánh là thừa".** Hai điều đứng nguyên, và điều thứ hai mới là gốc:

1. Quét master ra **0**. Cả hai lease `#227` — kể cả bản **đã đăng**, cấp trước 15 phút — đều vô
   hình ở đó. Con số đúng là 2 chứ không phải 7, và **2 vẫn lớn hơn 0**.
2. **Không có cách nào ĐỌC ĐƯỢC để biết một lease đã tiêu hay chưa.** Cột cuối bảng trên phải dựng
   BẰNG TAY, bằng cách đi tìm HIỆN VẬT của từng packet trên master — không phải bằng một trường
   trong tệp lease. Trạng thái Issue cũng không trả lời được: đo 22-08, **cả bốn** Issue #206 #215
   #225 #227 đều còn `open` trong khi hai packet đầu đã land. Đây chính là nợ
   `AG-T0-01B-thu-hoi-lease-chua-co-duong` đã khai từ trước — *"mọi packet land sớm hơn hạn đều để
   lại một quyền ghi còn sống"* — và nay đo được nó để lại **5** cái.

Nên lệnh `ai-dang-giu` ở phần nợ phải trả **ba** trạng thái cho mỗi lease — `còn hiệu lực` ·
`đã tiêu` · **`không xác định được`** — chứ không phải đếm đầu tệp. Trạng thái thứ ba phải làm người
cấp lease DỪNG LẠI, không được lẳng lặng tính là `đã tiêu`.

**Sổ lease KHÔNG nằm một chỗ.** Mọi câu "không lease nào đang giữ X" đo trên master là mù theo cấu
trúc, và chỗ mù nằm đúng ở lease MỚI NHẤT — tức lease khả nghi nhất, y hệt lý do `t23` không được
ghi cứng một tên tệp.

Mỉa mai đúng chỗ đáng nhớ: cả packet `PLAT-X8` sinh ra để dạy cổng **ĐO** thay vì **NHẬN LỜI KHAI**,
mà đặc tả của nó lại nhận một lời khai đo ở chỗ mù. Cùng họ với `doctrine-scan`, với dấu bỏ-qua-CI,
với `gh auth status`: **một lớp mà ta không coi là lớp**.

## Việc cho lượt sau — ĐỪNG bỏ bước nào

1. **Chờ #227 land**, rồi đo lại `origin/master`.
2. **Đặc tả `PLAT-X8` phải ra bản 4** — ba con số hiện tại chết theo #227:
   - §0 ghi *"bộ test = 42/42"* ⇒ sàn thật sẽ là **58**;
   - §6 `A9` đòi `N >= 42` ⇒ phải nâng;
   - §3 phải khai ĐÚNG bảng lease còn sống, đo trên **mọi nhánh `ops/**`**, không chỉ master.
   Bản 4 ⇒ băm đổi ⇒ lease mới neo băm mới. Prompt
   `ops/prompts/plat-x8-exec-1-codex-20260821.md` GIỮ LẠI nhưng phải neo lại băm đặc tả trước khi
   dùng — nó đang trỏ bản 3b (`308d0cf44fc1…`, tức bản 3 + hộp cảnh báo).
3. **Trước khi cấp BẤT KỲ lease nào**: quét lease còn sống trên **mọi nhánh `ops/**`**, không chỉ
   master. Chưa có công cụ cho việc này — đó là một nợ, ghi ở dưới.

### ĐÍNH CHÍNH 22-08-2026 — mục 1 KHÔNG xảy ra như dự tính, và mục 2 có một con số SAI

Nguyên văn phía trên giữ nguyên làm bằng chứng. Những gì đo được khi thực hiện:

| mục | biên bản ghi | thực tế đo |
|---|---|---|
| 1 | *"chờ `#227` land, rồi đo lại"* | `#227` land 05:16:40Z (PR #234) **rồi bị REVERT** 40 phút sau (PR #237): CI master ĐỎ trên Windows, `gate(windows-latest)` **59/68**. Master nay **`2ab3560`**, bộ test về **42** ca. Land lại là packet **`#238`** |
| 2 | *"sàn thật sẽ là **58**"* | **SAI.** Lúc `#227` còn trên master, sàn đo được là **68** — không phải 58. Nay đã revert nên sàn lại là 42; đo lại khi `#238` land |
| 2 | *"ba con số chết theo `#227`"* | **mười một chỗ.** Hộp ⛔ bản 3b nâng lên sáu; đo lại toàn bảng ra mười một, trong đó một chỗ không phải con số mà là **mệnh đề sự kiện** (xem dưới) |
| 2 | đặc tả *"phải ra bản 4"* | ra **bản `3i`**, không phải bản 4 — nền còn đang đổi, đóng băng bản 4 lúc này là dựng lại đúng bệnh của bản 3. Băm `ca852d95ab59…` (`3c`→…→`3i`; `3f` sửa chỗ 12 vì con số cũ là tạo tác của clone nông, `3g` sửa một khẳng định về cổng KHÔNG TỒN TẠI) |
| 3 | *"chưa có công cụ"* | vẫn chưa. Nợ `SO-LEASE-KHONG-NAM-MOT-CHO` **còn nguyên**; lượt này quét bằng script rời |

**Mục 3 đã cứu đúng một lần — và cách nó cứu mới là thứ đáng ghi.** Quét đủ **99** ref lúc 05:2xZ ra
*"0 lease chồng lấn, cấp lease được"*. **Hai mươi phút sau**, nhánh `ops/pkg-windows` xuất hiện mang
`lease-dang-windows-exec-1-codex-20260822` (packet `#238`, hết `2026-08-23T10:00:00Z`) giữ **đúng cả
hai** tệp `write_set` của `PLAT-X8` ⇒ kết luận đảo chiều. Nên câu đúng không phải *"quét mọi ref"* mà
là **"quét mọi ref NGAY TRƯỚC KHI CẤP"**: quét đủ là **cần**, không **đủ**. Số ref cũng phải đo chứ
đừng chép — 98 → 99 trong một lượt làm việc.

Hai thứ nữa suýt làm phép đo sai lần nữa:

- **Tên trường hạn là `lease_expires_at_utc`.** Lượt quét đầu đoán `het_han`/`expires_at`/`deadline`,
  nhận `None` cho **cả 42** tệp; `None` đọc thành *"không có hạn"* thì bảng ra `0 lease còn hạn` —
  đúng cái kết luận sai mà biên bản này sinh ra để chặn. Họ *"đừng grep theo danh sách tên đoán trước"*.
- **Chỗ thứ mười một không phải con số mà là mệnh đề sự kiện:** §2 khai *"lần **đầu tiên**
  `ops/lease_publish.py` vào một `write_set`"* — sai, vì `#227` mở tệp ấy trước; nay **7/61** lease
  mang nó. Đo lại một bảng số thì bắt được số sai; chỉ đọc lại câu chữ mới bắt được mệnh đề sai.

## Nợ sinh ra từ sự cố này

- `SO-LEASE-KHONG-NAM-MOT-CHO` — chưa có lệnh nào trả lời *"lease nào đang giữ đường dẫn X"* trên
  toàn kho. Mỗi người tự grep, và ai grep master thì mù. Việc này nên là một lệnh con của
  `ops/lease_publish.py` (`ai-dang-giu <đường-dẫn>`) quét mọi ref `refs/remotes/origin/ops/*`, và
  phải fail-close khi không fetch được ref nào — "không đo được" phải ĐỎ, không được thành "không có".
- `PATHS-TREN-NHANH-MOI-CHUA-CO-PHAN-CHUNG` — xem phần đầu.
