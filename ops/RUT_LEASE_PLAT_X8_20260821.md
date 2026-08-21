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

| lease | hết hạn | giữ |
|---|---|---|
| `plat-x5-exec-1` … `1r4` (#206) | tới 22-08 01:50 | `_test.py` |
| `slice-b-c-exec-1` (#215) | 22-08 06:40 | `_test.py` |
| `lease-dang-exec-1` (#227) | 22-08 12:00 | **cả hai** |
| `lease-dang-exec-2` (#227) | 22-08 13:30 | **cả hai** |

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
   dùng — nó đang trỏ bản 3 (`328a74facb84…`).
3. **Trước khi cấp BẤT KỲ lease nào**: quét lease còn sống trên **mọi nhánh `ops/**`**, không chỉ
   master. Chưa có công cụ cho việc này — đó là một nợ, ghi ở dưới.

## Nợ sinh ra từ sự cố này

- `SO-LEASE-KHONG-NAM-MOT-CHO` — chưa có lệnh nào trả lời *"lease nào đang giữ đường dẫn X"* trên
  toàn kho. Mỗi người tự grep, và ai grep master thì mù. Việc này nên là một lệnh con của
  `ops/lease_publish.py` (`ai-dang-giu <đường-dẫn>`) quét mọi ref `refs/remotes/origin/ops/*`, và
  phải fail-close khi không fetch được ref nào — "không đo được" phải ĐỎ, không được thành "không có".
- `PATHS-TREN-NHANH-MOI-CHUA-CO-PHAN-CHUNG` — xem phần đầu.
