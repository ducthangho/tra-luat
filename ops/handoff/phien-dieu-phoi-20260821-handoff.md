# Bàn giao phiên điều phối — 2026-08-21

**Từ:** phiên Claude Code (web, remote), vai **điều phối + soạn đặc tả**. **KHÔNG** phải phiên executor
của packet nào, nên bản này **không** theo schema §7 (`ops/handoff/wp55-r4g1-handoff.md` là bản §7 thật).
Đừng đọc nó thành handoff executor: không có `generation`, không có `attempts_used`, không có head để review.

**Tới:** phiên kế tiếp.
**Trạng thái:** không có việc nào đang dở. Mọi thứ đang chờ **quyết định của người giữ kho**.

---

## 1. Neo — đọc bằng BĂM, không bằng tên nhánh

```yaml
nhanh: claude/opus-5-plan-steps-y5r6ci
commit: 38c2123
base: 3db588c                      # = origin/master lúc phiên kết thúc
diff_so_master: 1 tệp, +205 dòng   # chỉ ops/specs/plat-x8.md

spec_path: ops/specs/plat-x8.md
spec_sha256: 328a74facb8440c11326cd074796ec7a23d2c509d8e2b0a2b63325951c0e3e24   # BẢN 3
spec_da_kiem_tren_ban_DA_DEN: true   # git cat-file -p origin/<nhánh>:… | sha256sum

packet_issue: 225
lease: CHUA CAP
pr: CHUA MO
```

> **CẬP NHẬT 22-08-2026 — đặc tả đã ĐÓNG BĂNG LẠI HAI LẦN sau khi bản bàn giao này viết xong.**
> Hai lượt cross-review (`codex`) ra **bốn P1**, cả bốn đánh vào **một** đường: kế thừa lớp cho lease
> reviewer. Người giữ kho **THU HỒI Q1** — đường kế thừa bị gỡ hẳn, không vá tiếp; reviewer lease
> `schema_version >= 2` nay là `sensitive` **vô điều kiện**. Lý do ở §10 của đặc tả.
>
> | bản | băm | kết cục |
> |---|---|---|
> | 1 | `9cb54a2e4e7c…` | 2 P1 lượt 1 — hết hiệu lực |
> | 2 | `b88c53dfd211…` | 2 P1 lượt 2 — hết hiệu lực |
> | 3 | `328a74facb84…` | **bản dùng được** |
>
> Nghĩa là **§3 dưới đây đã lệch một phần**: Q1 không còn là quyết định đang có hiệu lực. Hai thứ
> còn lại (cấp lease, nới bảng phân loại) vẫn chờ. Đọc đặc tả bản 3 làm chuẩn, đừng đọc bản này.

**Chưa mở PR** — người giữ kho chưa yêu cầu. Nhánh đã đẩy, spec tra được bằng
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
