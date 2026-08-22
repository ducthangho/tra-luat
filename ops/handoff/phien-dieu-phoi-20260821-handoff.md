# Bàn giao phiên điều phối — 2026-08-21

**Từ:** phiên Claude Code (web, remote), vai **điều phối + soạn đặc tả**. **KHÔNG** phải phiên executor
của packet nào, nên bản này **không** theo schema §7 (`ops/handoff/wp55-r4g1-handoff.md` là bản §7 thật).
Đừng đọc nó thành handoff executor: không có `generation`, không có `attempts_used`, không có head để review.

**Tới:** phiên kế tiếp.
**Trạng thái:** không có việc nào đang dở. Mọi thứ đang chờ **quyết định của người giữ kho**.

---

## 1. Neo — đọc bằng BĂM, không bằng tên nhánh

> ⚠ **`spec_sha256` TRONG KHỐI DƯỚI ĐÂY ĐÃ HẾT HIỆU LỰC.** Đặc tả ra **bản 3e** ngày 22-08, băm
> `ce14fb0b75e4…`. Khối neo còn hiệu lực nằm ở **cuối §1**, dưới nhãn *CẬP NHẬT 22-08-2026*.
> Khối cũ giữ nguyên làm bằng chứng — đừng vá lẻ nó, đừng lấy băm từ nó.

```yaml
# MỌI trường dưới đây đo CÙNG MỘT LÚC, trên CÙNG MỘT commit. Đừng vá lẻ từng trường.
# HẾT HIỆU LỰC 22-08 — xem khối CẬP NHẬT ở cuối §1.
do_luc: '2026-08-22'
nhanh: claude/opus-5-plan-steps-y5r6ci
commit_gioi_thieu_bam_spec: 7c19850   # KHÔNG phải head của nhánh. Đây là commit ĐẦU TIÊN mà
                                     # ops/specs/plat-x8.md mang băm ghi bên dưới. Head trôi
                                     # theo mỗi commit; commit này thì không.
base: a5bfe07                      # = origin/master lúc đo
diff_so_master: xem PR 230           # con số này chết ở MỌI commit kế tiếp — đừng ghi cứng,
                                     # đo sống: git diff origin/master...HEAD --shortstat

spec_path: ops/specs/plat-x8.md
spec_sha256: 308d0cf44fc1fcca75bc4d8edb014f560293622334ef25cc621c1e7afe3b2129   # BẢN 3b (bản 3 + hộp cảnh báo)
spec_da_kiem_tren_ban_DA_DEN: true   # git cat-file -p origin/<nhánh>:ops/specs/plat-x8.md | sha256sum

packet_issue: 225
lease: CHUA CAP
pr: 230                            # https://github.com/ducthangho/tra-luat/pull/230
```

> **P1 cross-review bắt được (PR #230, `chatgpt-codex-connector`) — khối neo trên từng TỰ MÂU THUẪN.**
> Nó khai `commit: 38c2123` cạnh `spec_sha256: 308d0cf4…`, nhưng băm của `ops/specs/plat-x8.md`
> **tại** `38c2123` là `9cb54a2e…` (bản 1). Đo thêm thì **ba** trường chết chứ không phải một:
> `commit`, `base`, `diff_so_master`. Nguyên nhân: mỗi lượt sửa chỉ vá **đúng trường vừa được
> nhắc tới** thay vì đo lại cả khối — nên `spec_sha256` luôn mới còn các trường quanh nó ở lại
> quá khứ. Mỉa mai đúng chỗ: trường khai `spec_da_kiem_tren_ban_DA_DEN: true` nằm trong chính
> khối không được đo lại. **Khối neo là MỘT phép đo, không phải một danh sách trường.**

> **CẬP NHẬT 22-08-2026 — đặc tả đã ĐÓNG BĂNG LẠI HAI LẦN sau khi bản bàn giao này viết xong.**
> Hai lượt cross-review (`codex`) ra **bốn P1**, cả bốn đánh vào **một** đường: kế thừa lớp cho lease
> reviewer. Người giữ kho **THU HỒI Q1** — đường kế thừa bị gỡ hẳn, không vá tiếp; reviewer lease
> `schema_version >= 2` nay là `sensitive` **vô điều kiện**. Lý do ở §10 của đặc tả.
>
> | bản | băm | kết cục |
> |---|---|---|
> | 1 | `9cb54a2e4e7c…` | 2 P1 lượt 1 — hết hiệu lực |
> | 2 | `b88c53dfd211…` | 2 P1 lượt 2 — hết hiệu lực |
> | 3 | `328a74facb84…` | hết hiệu lực khi dán hộp cảnh báo |
> | 3b | `308d0cf44fc1…` | bản dùng được **khi ấy**; hết hiệu lực 22-08 khi `#227` land **rồi bị revert** |
>
> Nghĩa là **§3 dưới đây đã lệch một phần**: Q1 không còn là quyết định đang có hiệu lực. Hai thứ
> còn lại (cấp lease, nới bảng phân loại) vẫn chờ. *(Đoạn này viết 22-08 sáng; **bản 3b nay cũng hết
> hiệu lực** — chuẩn hiện tại là **bản 3e** `ce14fb0b75e4…`, xem khối CẬP NHẬT cuối §1.)*
> Đọc **bản 3b** làm chuẩn — băm
> `308d0cf44fc1fcca75bc4d8edb014f560293622334ef25cc621c1e7afe3b2129`, đúng giá trị ở hàng
> `spec_sha256` của khối neo trên; hai chỗ ấy phải luôn khớp nhau. **Bản 3 (`328a74facb84…`) đã
> HẾT HIỆU LỰC** — đọc nó là bỏ qua hộp ⛔ ĐỪNG CẤP LEASE ở đầu đặc tả. Đừng đọc bản bàn giao này.

> **CẬP NHẬT 22-08-2026 — `#227` LAND RỒI BỊ REVERT. Đặc tả ra bản 3e, KHÔNG phải bản 4.**
> Khối neo ở đầu bản bàn giao này là ảnh chụp 21/22-08; bài học P1 ngay phía trên — *"khối neo là MỘT
> phép đo, không phải một danh sách trường"* — nên đây đo lại **cả khối** thay vì vá lẻ:
>
> ```yaml
> # Đo cùng lúc, 22-08-2026.
> commit_gioi_thieu_bam_spec: 36ff7df   # commit ĐẦU TIÊN mang băm bản 3e
> base: 2ab3560                         # = origin/master lúc đo (SAU revert #237)
> spec_path: ops/specs/plat-x8.md
> spec_sha256: ce14fb0b75e437491f184952c0b46a2b8f3ab5ebf8b93cd40afbb67708d92de4   # BẢN 3e
> packet_issue: 225
> lease: CHUA CAP — VA CHAM lease song cua #238, xem duoi
> ```
>
> | bản | băm | kết cục |
> |---|---|---|
> | 3b | `308d0cf44fc1…` | hết hiệu lực khi `#227` land rồi bị revert |
> | 3c | `182ea7621d02…` | hộp ⛔ đổi điều kiện chờ sang `#238` — hết hiệu lực khi thêm chỗ thứ 12 |
> | 3d | `f7f8e6209e4f…` | thêm chỗ thứ 12 (`reviewed_sha_required` kiểm HÌNH DẠNG, không kiểm TỒN TẠI) — hết hiệu lực khi thêm chỗ 13 |
> | 3e | `ce14fb0b75e4…` | **bản dùng được** — thêm chỗ thứ 13: lease `codex` cho packet `sensitive` là ngoại lệ CÓ ĐIỀU KIỆN theo `ADR-0045`, và điều kiện "khai là ngoại lệ §2" chưa được ghi ở đâu |
>
> **Vì sao KHÔNG ra bản 4.** `#227` merge 05:16:40Z (PR #234) ⇒ CI master **ĐỎ trên Windows**
> (`gate(windows-latest)` 59/68) ⇒ revert PR #237, master **`2ab3560`**, bộ test về **42** ca. Land
> lại là packet **`#238`**. Đóng băng bản 4 trên một nền đang đổi là dựng lại đúng bệnh của bản 3.
>
> **Chưa cấp lease được:** `lease-dang-windows-exec-1-codex-20260822` (packet `#238`, hết
> `2026-08-23T10:00:00Z`, trên nhánh `ops/pkg-windows` chưa về master) giữ **đúng cả hai** tệp
> `write_set` của `PLAT-X8`.
>
> **Một phép đo tự bác chính nó trong 20 phút, ghi lại vì nó rẻ và hay tái phát:** quét đủ **99** ref
> lúc 05:2xZ ra *"0 lease chồng lấn"*; 20 phút sau nhánh thứ 99 xuất hiện mang đúng một lease chồng
> lấn. Quét đủ ref là **cần**, không **đủ** — phải quét **ngay trước khi cấp**.

**PR #230 đang mở** (mở 22-08-2026 theo yêu cầu người giữ kho) — xem trường `pr:` trong khối neo,
và đọc lịch sử review của nó trước khi làm gì trên nhánh này. Nhánh đã đẩy, spec tra được bằng
`git fetch origin claude/opus-5-plan-steps-y5r6ci`.

---

## 2. Phiên này đã làm gì

| # | việc | kết quả |
|---|---|---|
| 1 | Hoàn tất hồ sơ `PLAT-M4` | PR **#222** đã merge (`3db588c`) — ba lượt cross-review + `human_audited` của #214/#216 |
| 2 | Rà ba caveat còn mở của `PLAT-M4` | nợ **#1** thành packet mới; nợ **R2** vẫn mở (xem §4) |
| 3 | Chạy `soan-spec` cho nợ #1 | hai vòng chất vấn, 6 câu, người giữ kho duyệt cả 6 |
| 4 | Mở Issue packet | **#225** `[PLAT-X8]` |
| 5 | Đổi định danh `#220` | `PLAT-X6` → **`PLAT-X7`**, bằng đính chính **nối thêm** |
| 6 | Đóng băng đặc tả | `ops/specs/plat-x8.md`, băm ở §1 |

---

## 3. Ba thứ đang CHỜ NGƯỜI GIỮ KHO — phiên mới đừng tự quyết

### 3.1. Cấp lease executor cho #225

Phiên soạn spec **không tự cấp được**: `granted_by` phải là người giữ kho, cổng trả `rc=4` cho lease
tự cấp (`ops/lease_publish.py`, `RC_TU_CAP = 4`).

### 3.2. Nới bảng phân loại hay không — con số bắt buộc phải đưa lên bàn

Bảng `_BANG_LOP` chỉ seed bằng thứ `docs/PROTOCOL_DA_PHIEN.md` §8:572 nói **nguyên văn**; mọi đường
dẫn khác rơi vào nhánh mặc định `sensitive`. Đo trên **15** đường dẫn từng xuất hiện trong `write_set`
của **mọi** lease:

> **15/15 ra `sensitive`.** Trong 10 lease khai lớp, **6 bị NÂNG** (1 `routine` + 5 `systemic`).

Nghĩa là dưới bảng seed, **không packet nào của kho còn là `routine`/`systemic`** — trong khi §8 mặc
định *"Codex chỉ nhận Packet `routine`/`systemic` nhỏ"*. Đây **đúng là** điều Q2=(a) nghĩa là, không
phải lỗi cài đặt, nhưng nó đổi kinh tế vận hành và người giữ kho **chưa có con số này trên bàn lúc
duyệt** — nó đo được sau khi duyệt.

Hai đường, chọn lúc nào cũng được vì chưa cấp lease:
- **giữ nguyên** — chấp nhận mọi packet là `sensitive`; nới bảng thành packet riêng có bằng chứng từng đường dẫn;
- **nới ngay trong `PLAT-X8`** — thêm `docs/**` (trừ `PROTOCOL_DA_PHIEN.md` và `adr/**`) + `CHANGELOG.md`
  vào vế `routine`. Ước ~30 dòng, vẫn dưới trần 300 của ADR-0044.

Đặc tả hiện xếp việc nới bảng vào `ngoai_pham_vi` §4.2. Đổi ý ⇒ **băm đổi** ⇒ phải đóng băng lại
TRƯỚC khi cấp lease.

### 3.3. Mở PR cho nhánh `claude/opus-5-plan-steps-y5r6ci` hay không

---

## 4. Nợ còn mở — KHÔNG thuộc phiên này

| nợ | nguồn | trạng thái |
|---|---|---|
| `chot-tinh-class-van-KHONG-TON-TAI` | biên nhận `plat-m4-human-audit` | → **`PLAT-X8` #225**, đã có spec |
| `no-R2-van-mo` | biên nhận `plat-m4-human-audit` | **VẪN MỞ**. Packet kế tiếp chạm `.claude/dev/launcher.py` hoặc `launcher_test.py` phải vá **CẢ HAI** hàm — `_do_mcp_endpoint` **VÀ** `_do_rest_github`. Vá một là để nợ lại |
| `khong-doc-thanh-cross-provider` | biên nhận `plat-m4-human-audit` | caveat **cách đọc**, không phải việc. Đừng viện `PLAT-M4` làm tiền lệ *"packet `sensitive` land được bằng chữ ký người"* |
| `PLAT-X5-required-status-check` | `ops/NO_KY_THUAT.md` §9 | nợ **THƯỜNG TRỰC** |

---

## 5. Thứ tự packet đã chốt — bốn thứ cùng đòi `ops/lease_publish*`

> ⛔ **MỤC NÀY ĐÃ LẠC HẬU — ĐỌC CẢNH BÁO TRƯỚC KHI CẤP BẤT KỲ LEASE NÀO.** Giữ nguyên văn làm bằng
> chứng; **đừng dùng làm căn cứ vận hành**. Hai câu dưới đây đã bị bác bằng phép đo 22-08:
>
> | mục 5 ghi | đo được 22-08 |
> |---|---|
> | thứ tự bắt đầu từ `PLAT-X8` | `#238` chen lên trước: **`#238` → `PLAT-X8` → `#209` → `PLAT-X7` → mục D** |
> | *"**không lease nào** đang giữ `ops/lease_publish.py` hay `ops/lease_publish_test.py`"* | **SAI.** `lease-dang-windows-exec-1` và `-exec-2` (packet `#238`, hết `2026-08-23T10:00:00Z` và `11:00:00Z`, trên nhánh `ops/pkg-windows` chưa về master) giữ **đúng cả hai** tệp |
> | *"mười lease từng chạm tệp test đều thuộc `PLAT-X4`/`PLAT-X5`/`SLICE-B-C`, đã land"* | đúng **khi ấy**; nay có thêm lease của `#227` và `#238` |
>
> Câu *"không lease nào đang giữ"* sai vì nó quét `ops/leases/` trên **cây đang checkout**, mà lease
> sống nằm trên nhánh `ops/**` và chỉ về master **sau khi merge**. Xem khối CẬP NHẬT ở cuối §1 và
> hộp ⛔ đầu `ops/specs/plat-x8.md`.

```
PLAT-X8 (#225)  →  PLAT-X6 (#209)  →  PLAT-X7 (#220)  →  gói spec-gate (mục D, chưa mở Issue)
```

Đo được: **không lease nào** đang giữ `ops/lease_publish.py` hay `ops/lease_publish_test.py` — mười
lease từng chạm tệp test đều thuộc `PLAT-X4`/`PLAT-X5`/`SLICE-B-C`, đã land. Nên va chạm là **theo kế
hoạch**, xử bằng **thứ tự**, không bằng thu hồi.

`PLAT-X7` phải khai `depends_on: [PLAT-X8]`: hướng chốt #3 của nó (*"với `review_class: sensitive`,
cổng từ chối cặp cùng họ model"*) **tiêu thụ** lớp review hiệu lực, thứ `PLAT-X8` **sản xuất**.

---

## 6. Bốn bẫy phiên này đã đụng — phiên mới đừng đụng lại

1. **`PLAT-X6` từng trỏ HAI Issue** (#209 và #220). Nay #220 = `PLAT-X7`. Tài liệu cũ
   (`ops/prompts/plat-x5-review-2-claude-20260820.md`, `ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md`,
   hai lease `ag-t0-01b-exec-*`, `ops/specs/ag-t0-01b-r*.md`) vẫn ghi `PLAT-X6` cho **cả hai nghĩa**.
   **Tra bằng SỐ ISSUE, không bằng `packet_id`.**

2. **`ops/specs/ag-t0-01b-r4.md` ĐANG BỊ NEO BĂM** `a1007d04…` bởi lease
   `ag-t0-01b-exec-1r2-antigravity-20260822`, hiệu lực từ **22-08**. Sửa một byte trong tệp ấy là làm
   lease trỏ vào băm không tệp nào ứng với. Đó là lý do #220 đổi tên bằng **đính chính nối thêm**,
   không sửa đè thân Issue.

3. **`rg effective_review_class` có một kết quả LỪA.** `ops/chatgpt_review/build_bundle.py:165` có
   chuỗi ấy, nhưng đó là **tên biến cục bộ** — chỉ kiểm enum rồi **chép** giá trị đã khai. Nó không
   tính gì từ `write_set` và không liên quan tới trường của §8. Đừng đọc thành "đã có bản cài đặt một phần".

4. **Hai con số trong biên nhận `PLAT-M4` SAI, đã đính chính trong #225 nhưng KHÔNG sửa trong biên
   nhận** (biên nhận là bản ghi, không sửa đè): ghi *"0/41 lease"*, số thật là **0/49**; và câu *"thứ
   duy nhất chạm nó chỉ CHÉP LẠI giá trị đã khai"* đúng hành vi nhưng sai đối tượng — xem bẫy 3.
   Sự thật chịu tải không đổi: **0 lease khai**, **0 dòng cổng đọc**.

5. **Băm đặc tả trong BẤT KỲ tài liệu nào cũng phải kiểm lại trước khi dùng.** `ops/specs/plat-x8.md`
   đã đóng băng **ba lần trong hai ngày**. Chính bản bàn giao này từng trỏ vào băm bản 1 và trỏ sai
   trong khoảng một ngày. Băm là thứ định danh, nhưng nó **không** bất biến theo thời gian — nó bất
   biến theo NỘI DUNG. Đo `sha256sum` trên tệp thật, đừng chép băm từ tài liệu khác.

---

## 7. Lệnh mở phiên — chạy trước mọi việc khác

```bash
sed -n '1,140p' .claude/dev/launcher.py
python3 .claude/dev/launcher.py doctor
python3 .claude/dev/launcher.py chuan-bi     # khi hook không chạy
```

Đo 21-08 trong container này: `codex` = **`SAP_HET_HAN`** (ảnh chụp `CODEX_AUTH_JSON` cũ ~128h,
refresh token xoay vòng). Cần cross-review thì **kiểm `codex` chạy thật TRƯỚC**, đừng tin
`codex login status` — nó chỉ kiểm tệp đọc được, không kiểm token còn sống.

Cổng trên nhánh này: `python3 ops/lease_publish_test.py` ⇒ **42/42 đạt**, delta so master = **0**.

---

**Đọc được bản bàn giao này KHÔNG phải là được giao việc.** Handoff không phải lease
(`docs/PROTOCOL_DA_PHIEN.md` §7). Thứ giao việc là Packet Issue kèm lease còn hiệu lực (§3.2, §4).
