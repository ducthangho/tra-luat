# ĐẶC TẢ ĐÓNG BĂNG — `BO-CONG-DUYET-KHAC-DANH-TINH` — **BẢN 1 — ĐÃ CHỐT 11-09-2026** (Q1/Q2/Q4 đồng ý tại #502 comment 5629584614; Q3 chưa đo, xem ghi chú cuối)

| trường | giá trị |
|---|---|
| `packet_id` | `BO-CONG-DUYET-KHAC-DANH-TINH` |
| `packet_issue` | **#502** — thân Issue chép nguyên văn chỉ đạo ở `nguon_cap_viec`; câu trả lời biên giới ở comment 5629584614 |
| `nguon_cap_viec` | Chỉ đạo chủ kho, phiên 11-09-2026, nguyên văn: *"đồng ý các đề xuất, trừ nội dung số 3. tôi muốn bỏ phê duyệt khác danh tính"*. Một câu trong khung chat KHÔNG phải dấu vết bền — `granted_on_instruction` của lease phải neo vào comment trên Packet Issue. Không phải packet khắc phục của một packet đã land theo nghĩa "sửa lỗi"; nó **RÚT** một cổng do packet **#348** (`TACH-DANH-TINH-GITHUB`) dựng và **#386** (`CONG-DUYET-THEO-THAM-QUYEN`, PR #393) sửa. |
| `review_class` | **`sensitive`** — chạm `.github/workflows/**` (PROTOCOL §8: workflow/CI authority) và chạm chính cổng quyết định AI ĐƯỢC DUYỆT. Vế nghiêm ADR-0044: ≤3 tệp, ≤300 dòng thêm — **vượt số tệp (6)**, xem Q1. |

**GIỚI HẠN LỜI KHAI:** chứng minh BYTE tới consumer adapter. KHÔNG tuyên bố model "đã hiểu".
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC** — thứ ba làm cổng ĐỎ, không làm tròn lên.

---

## VÌ SAO — phép đo, không phải lập luận

Cổng `duyet khac danh tinh / cong` (packet #348, các commit `9848a2f` → `bc30d2a` → `b292bea` → `8fb6c9e` →
`94ab0e6`; sửa sang đọc THẨM QUYỀN ở `c0cdad1`, packet #386) đòi **một review `APPROVED` từ danh tính KHÁC
tác giả PR**, neo đúng `head_sha`. Nó chỉ cưỡng chế được khi **nửa A** (branch protection, `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md`
bước 2: required check + "không cho bypass") được cấu hình — và chính runbook nói: *"nửa B một mình không cưỡng chế
được gì"*.

**Đo được trong 24 giờ qua — cổng KHÔNG chặn gì, chỉ tốn:**

| sự kiện | đo | nguồn |
|---|---|---|
| PR #500 merge `c00c88a0` lúc **01:05:01Z 11-09** | tại head merge **không có** review `APPROVED` nào từ danh tính khác tác giả ⇒ `cong` ĐỎ, PR vẫn merge được | CHANGELOG `r364`, đính chính tại `dae1aed`; biên nhận `ops/reviews/pr500-review-2-codex-verdict.receipt.yaml` |
| PR #501 merge `27c413c3` lúc **01:54:04Z 11-09** | `notebyme88` duyệt 01:20:27Z (`cong` xanh, run `34550273565`), rồi một push đính chính (`dae1aed`) **tự động DISMISS** bản duyệt ⇒ `cong` ĐỎ lại tại head merge, PR vẫn merge được | cùng biên nhận |

Hai lần merge với `cong` ĐỎ ⇒ **`cong` không phải required check** và **không có luật "require approvals"** đang
chặn `master` (đo bằng HẬU QUẢ, không đọc được cài đặt — xem `chua_do_duoc`). Cái cổng mua được hôm nay là
**không** (không chặn ai), cái nó tốn là **có**: mỗi PR đều mang một check đỏ; muốn xanh phải gọi tay tài khoản
thứ hai duyệt, và **mọi push sau đó xoá bản duyệt** — trên #501 điều ấy xảy ra ngay trong cùng một giờ. Chủ kho
quyết định rút: đây là quyết định quản trị (§2), không phải kết luận kỹ thuật của phiên này.

**Nửa A đã từng được cấu hình chưa — KHÔNG ĐO ĐƯỢC** từ phiên (REST quản trị 403 tại proxy, runbook đã đo
27-08-2026). Hậu quả đo được ở trên chỉ nói: *hiện không có luật nào chặn*. Nếu chủ kho đã bật rồi tắt, hay chưa
từng bật, phiên không phân biệt được; việc gỡ nửa A (nếu có) là của chủ kho trước trình duyệt — `ngoai_pham_vi`.

---

## `write_set` — SÁU đường, không ký tự đại diện

Đo kích thước **03:00:02Z 11-09-2026** trên `origin/master` = `27c413c3`:

```
.github/workflows/duyet-khac-danh-tinh.yml       74 dòng   XOÁ (lane tin cậy, pull_request_target)
.github/workflows/duyet-phan-chung.yml           62 dòng   XOÁ (lane phản chứng, pull_request)
.claude/dev/duyet_danh_tinh.py                  338 dòng   XOÁ (bộ quyết định)
.claude/dev/duyet_danh_tinh_test.py            1235 dòng   XOÁ (phản chứng + đột biến)
.claude/dev/ci_dang_ky_test.py                  549 dòng   SỬA 1 dòng: gỡ mục `DA_NOI`
ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md            212 dòng   SỬA: khối ĐÃ RÚT ở đầu tệp (giữ thân làm lịch sử)
```

Vì sao `ci_dang_ky_test.py` phải vào write set (L2): `kiem()` (dòng 170–175) đỏ với thông điệp *"mục đăng ký
không có tệp"* khi một tên trong `DA_NOI` không còn tệp — dòng 60 đang ghi `.claude/dev/duyet_danh_tinh_test.py`.
Xoá tệp mà không gỡ dòng ấy là làm CI `test registry` (bước 16 của `ci.yml`) ĐỎ.

**Đã đo ai giữ — `ai-dang-giu` bản master, chạy trong bản sao sạch detach `27c413c3`, 02:54:23Z 11-09-2026**, sau
khi so hai nguồn ref (máy chủ **324** · đệm **324** · `comm` hai chiều **0/0** ⇒ không mù):

```
cả sáu đường → NGƯỜI_GIỮ 0
  HẾT_HẠN: tach-danh-tinh-github-exec-1r3..1r6-codex-20260828 (5 đường đầu; nhánh ops/cap-lease-tach-danh-tinh-20260827)
  HẾT_HẠN: cong-ngoai-write-set-exec-1r2..1r5-codex-20260828 (ci_dang_ky_test.py; nhánh ops/cap-lease-tach-314)
```

Giao thoa TIỀM TÀNG, chưa phải lease: nháp `ops/leases/lo-319-linux-bang-chung-xanh-exec-1-claude-20260906.yaml.nhap`
khai write set `.claude/dev/ci_dang_ky_test.py` (LO-319, packet #464). Đuôi `.nhap` không được `ai-dang-giu` đếm.
Nếu chủ kho cấp LO-319 trước packet này thì packet này phải **đợi** hoặc **tách** mục M5 — ghi ở điều kiện dừng S3.

Kích thước bản vá dự kiến: `git diff --numstat` ≈ **+15 / −1710** (xoá 4 tệp = −1709 dòng, sửa 2 tệp ≈ +15/−1).
Số ấy là ước từ kích thước hiện tại; executor đo lại trước review (L5).

## `ngoai_pham_vi` — cố ý KHÔNG làm

- **Nửa A trên GitHub** (branch protection / ruleset: required check `duyet khac danh tinh / cong`, "require
  approvals", "không cho bypass") — chỉ chủ kho trước trình duyệt; phiên không đọc được (403 tại proxy) và không nên
  có quyền. Sau khi packet land, nếu nửa A còn trỏ vào context đã biến mất thì `master` **kẹt** với mọi PR — chính
  runbook đã viết đường lùi cho ca ấy (bước 2, "ĐƯỜNG LÙI"). Xem Q3.
- **`ops/specs/CONG-DUYET-THEO-THAM-QUYEN.md`**, **`ops/leases/*tach-danh-tinh*`**, **`ops/leases/cong-duyet-theo-tham-quyen-*`**,
  **`ops/reviews/**`** (kể cả hai hàng README nhắc cổng này) — hồ sơ đã đóng băng, có băm; không sửa.
- **`docs/PROTOCOL_DA_PHIEN.md` §8 `human_audited`** ("người audit có danh tính bền trên GitHub, độc lập với
  Executor") — là mức assurance của protocol, KHÔNG phụ thuộc cổng này; giữ nguyên.
- **ADR** — không có ADR nào dựng cổng này (`ls docs/adr | grep -i duyet` = 0, đo 02:52Z 11-09), nên không có
  ADR nào để đánh `Superseded`. Xem Q2 về việc có mở ADR mới hay không.
- **`ops/cai_actionlint.sh`**, **`ops/cai_cong_cu.sh`** — dùng chung với `ci.yml`, giữ.
- **`CHANGELOG.md`**, **`RELEASE_MANIFEST.json`**, verdict/biên nhận — đi PR hồ sơ theo ADR-0034, như #500/#501,
  không nằm trong write set packet (tiền lệ: `c0cdad1`, `9848a2f`, `b292bea` đều không chạm CHANGELOG).
- **`ops/reviews/README.md`** — hai hàng cảnh báo nhắc cổng (dòng 72, 77) là lịch sử của verdict N5; giữ.

---

## `muc_tieu` — mỗi dòng chiếu vào một đường trong `write_set`

**M1** *(`.github/workflows/duyet-khac-danh-tinh.yml`)* — **xoá tệp**. Không còn workflow nào khai job `cong`.

**M2** *(`.github/workflows/duyet-phan-chung.yml`)* — **xoá tệp**. Lane phản chứng mất đối tượng khi M4 xoá bộ test.

**M3** *(`.claude/dev/duyet_danh_tinh.py`)* — **xoá tệp**. Không giữ "để dành": mã không ai gọi là mã không ai đo
(đo 02:53Z 11-09: ngoài chính hai tệp `duyet_danh_tinh*` và hai workflow, chỉ `ci_dang_ky_test.py:60` nhắc tên).

**M4** *(`.claude/dev/duyet_danh_tinh_test.py`)* — **xoá tệp**, cùng lý do M3.

**M5** *(`.claude/dev/ci_dang_ky_test.py`)* — gỡ đúng một mục `".claude/dev/duyet_danh_tinh_test.py",` khỏi `DA_NOI`
(dòng 60). Không đụng `MOI`, `MOI_WINDOWS`, `CACH_LY`, `loi_ruff_ci`, `loi_launcher_windows`.

**M6** *(`ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md`)* — thêm khối **ĐÃ RÚT** ngay dưới tiêu đề: packet rút, ngày, lý do
(trỏ mục VÌ SAO ở đây), và **việc chủ kho phải làm ở nửa A** (gỡ required check `duyet khac danh tinh / cong` nếu có;
gỡ "require approvals" nếu có). Giữ nguyên thân tệp phía dưới làm lịch sử — không xoá, vì runbook là bản ghi duy nhất
mô tả nửa A từng được đề nghị thế nào, và đường lùi ở bước 2 vẫn đúng cho ca `master` kẹt.

---

## `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ

**A1 (M1, M2)** — `ls .github/workflows/duyet-*.yml` ⇒ **0 tệp**; `grep -rn "duyet-khac-danh-tinh\|duyet-phan-chung\|duyet_danh_tinh" --include='*.yml' --include='*.yaml' --include='*.py' --include='*.sh' .` ⇒ **0 dòng** ngoài `ops/specs/**`, `ops/leases/**`, `ops/reviews/**`, `ops/RUNBOOK_*` (hồ sơ).
*Phép đo làm nó ĐỎ:* để sót một trong hai workflow, hoặc để sót dòng 60 của `ci_dang_ky_test.py`.

**A2 (M5)** — `python .claude/dev/ci_dang_ky_test.py` XANH trên cây sau vá, và **ĐỎ trên cây "xoá 4 tệp nhưng chưa gỡ
dòng 60"** với đúng thông điệp `mục đăng ký không có tệp: .claude/dev/duyet_danh_tinh_test.py`. Executor phải chạy
cả hai vế và chép hai dòng in ra vào PR (vế ĐỎ chứng minh M5 không phải sửa thừa).

**A3 (M1–M4)** — `actionlint` (ghim `AL_VER=1.7.7`, có `shellcheck`) trên toàn `.github/workflows/` ⇒ `rc=0`; cùng
lệnh `ops/don_ref_chot_test.sh` chạy được. `AL_VER=1.7.7 bash ops/chay_lease_publish_test.sh` ⇒ `N/N` với N = số ca
nền **146** (đo 02:5xZ 11-09 tại chỗ, Linux) — `t34` quét mọi workflow còn lại, `t24` quét dấu bỏ-qua-CI; delta so
`origin/master` = 0.
*Phép đo làm nó ĐỎ:* bất kỳ ca sẵn có nào đổi màu.

**A4 (M6)** — Khối ĐÃ RÚT nằm **trước** tiêu đề `## Vì sao phiên không tự làm được`, có đúng ba mục: packet/ngày ·
lý do (trỏ spec này bằng đường dẫn) · việc nửa A của chủ kho. `python scripts/tl.py doc-claims-check --strict` không
đỏ thêm (runbook nằm ngoài tập quét mặc định — ghi rõ để người đọc không tưởng cổng ấy canh tệp này).
*Phép đo làm nó ĐỎ:* thiếu mục "việc nửa A" — đó là mục duy nhất người sau cần.

**A5 — CI lane PR không còn check `cong` và không còn check `phan-chung`.** Trên PR của packet, danh sách check run
tại head **không** có `duyet khac danh tinh / cong` và **không** có `phan chung duyet khac danh tinh / phan-chung`
— lưu ý `pull_request_target` lấy định nghĩa từ nhánh CƠ SỞ, nên **trên chính PR này `cong` VẪN CHẠY** (định nghĩa
còn ở `master`) và sẽ ĐỎ nếu không có ai duyệt. Vì vậy A5 đo ở **PR ĐẦU TIÊN SAU KHI LAND**, không đo trên PR của
packet. Ghi kết quả (số PR, head, danh sách check) vào biên nhận/CHANGELOG của PR hồ sơ.
*Phép đo làm nó ĐỎ:* check `cong` vẫn xuất hiện trên PR sau land ⇒ tệp chưa mất khỏi `master` hoặc nửa A vẫn gọi tên.

**A6 — gate `master` sau land XANH ở lane ubuntu**, và lane Windows **không đổi trạng thái** so với lượt liền trước
(nợ #499 C3 làm Windows `cancelled` sẵn — packet này không được khai "Windows xanh" và cũng không bị quy là làm
Windows đỏ; đo bằng bước 20 `lease-publish selftest` của cả hai lượt).

**A7 — kích thước.** `git diff --numstat origin/master...HEAD` cộng dồn: **dòng thêm ≤ 30**; số tệp = **6**. Vượt
30 dòng thêm là dấu hiệu executor đang "làm thêm" — DỪNG (S2).

---

## `hinh_dang_ke_thua` (L4)

Chép từ hồ sơ #348/#386 (không có biên nhận v2 cho #348; số đếm lấy từ chú thích trong chính hai workflow và spec #386):

| hình dạng | số lần | nguồn |
|---|---|---|
| "danh sách cấm đội lốt allow-list" | **7** | `duyet-phan-chung.yml` chú thích *"chỗ thứ bảy của họ…"*; `94ab0e6` |
| "cổng phân biệt CÁCH VIẾT chứ không phân biệt THẨM QUYỀN" | **1** (đã chữa ở #386) | `ops/specs/CONG-DUYET-THEO-THAM-QUYEN.md` §VÌ SAO |
| "cổng có MẶT khác cổng CƯỠNG CHẾ" (nửa B không có nửa A) | **1 → 3** | runbook dòng 7–9; hai lần merge với `cong` ĐỎ 11-09 (bảng VÌ SAO) |

Hình dạng thứ ba chạm 3 lần là lý do packet này tồn tại: theo chốt "lặp ba lần thì hỏi có nên làm nữa không",
câu trả lời của chủ kho là **không làm nữa**.

---

## `chua_do_duoc` — ghi thẳng

- **Cài đặt nửa A hiện tại** (required check, require approvals, bypass) — REST quản trị 403 tại proxy; chỉ suy
  được từ hậu quả (hai merge với `cong` ĐỎ). Nếu có ruleset "require approvals" mà admin bypass được, phiên cũng
  thấy y hệt. Chủ kho đọc trực tiếp trong Settings → Branches / Rules.
- **`master` có kẹt sau land không** — chỉ kẹt nếu nửa A đang require context `duyet khac danh tinh / cong`; vì
  không đo được nửa A nên câu này ở trạng thái thứ ba. Đường lùi: runbook bước 2 "ĐƯỜNG LÙI".
- **Parity Windows** — lane Windows đang `cancelled` vì #499 C3, nên A6 chỉ đo được "không đổi", không đo được "xanh".

---

## Điều kiện DỪNG

- **S1** cần đường dẫn thứ BẢY ⇒ DỪNG, khai (kể cả `ops/reviews/README.md` hay `CHANGELOG.md` — hai tệp ấy đi PR hồ sơ).
- **S2** dòng thêm > 30 ⇒ DỪNG (packet này XOÁ, không xây).
- **S3** `ai-dang-giu .claude/dev/ci_dang_ky_test.py` có NGƯỜI_GIỮ ≥ 1 lúc bắt tay (LO-319 được cấp trước) ⇒ DỪNG, hỏi
  chủ kho tách M5 hay đợi.
- **S4** `origin/master` đi tiếp mà CÓ chạm một trong sáu đường ⇒ DỪNG, đo lại.
- **S5** muốn "giữ lại `duyet_danh_tinh.py` phòng khi cần" ⇒ DỪNG, xem M3.
- **S6** chạm trần HAI vòng review (ADR-0043) ⇒ DỪNG, không tự nâng.

---

## Câu hỏi biên giới — ĐÃ CHỐT (chủ kho: *"Bước 1: Đồng ý"*, #502 comment 5629584614)

| câu | kết luận |
|---|---|
| Q1 | **ĐỒNG Ý** — ngoại lệ ADR-0044 có phạm vi cho SỐ TỆP: 6 tệp, dòng thêm ≤ 30 (ghi vào lease `ngoai_le_adr_0044`) |
| Q2 | **ĐỒNG Ý** — không mở ADR |
| Q3 | **CHƯA ĐO** — chủ kho đọc tại `https://github.com/ducthangho/tra-luat/settings/branches` và `/settings/rules`, trả lời trên #502. Mặc định làm việc: *chưa từng bật* (hai merge #500/#501 với `cong` ĐỎ đã đi qua). KHÔNG chặn cấp lease/thi công; là điều kiện trước khi LAND (A5) |
| Q4 | **ĐỒNG Ý** — song song với M9/WINDOWS; không cấp trùng LO-319 |

Nguyên văn bốn câu hỏi giữ dưới đây làm hồ sơ:

❓ **Q1 — Ngoại lệ ADR-0044 về SỐ TỆP.** Vế nghiêm cho `sensitive` là ≤3 tệp; packet này chạm **6** (4 xoá + 2 sửa nhỏ),
dòng thêm ≈ 15. Tách thành hai packet thì cây ở giữa **hỏng**: xoá workflow mà giữ test ⇒ lane phản chứng mất; xoá test
mà giữ dòng 60 ⇒ `test registry` ĐỎ trên `master`. ➡️ **Cấp ngoại lệ có phạm vi cho SỐ TỆP** (ghi vào lease:
`ngoai_le_adr_0044: so_tep 6, dong_them ≤ 30`), giữ nguyên trần dòng thêm. Tiền lệ: A0 (#488) đã có ngoại lệ dòng có
phạm vi ở spec r9 §write_set.

❓ **Q2 — Có mở ADR "rút cổng duyệt khác danh tính" không.** Không ADR nào dựng cổng; PROTOCOL không nhắc nó. ➡️ **Không
mở ADR**; quyết định ghi ở ba chỗ đã có: Packet Issue (chỉ đạo nguyên văn), khối ĐÃ RÚT trong runbook (M6), mục ★ CHANGELOG
của PR hồ sơ. Nếu chủ kho muốn một dòng bền hơn thì mở ADR `Accepted` một trang — khi ấy write set thêm `docs/adr/0048-*.md`
+ dòng §20 PROTOCOL (`adr-song` đòi), tức 8 tệp.

❓ **Q3 — Nửa A: chủ kho xác nhận trạng thái hiện tại.** Hai lần merge với `cong` ĐỎ cho thấy không luật nào đang chặn;
nhưng nếu nửa A đang bật với bypass admin thì sau land `master` sẽ kẹt cho danh tính không phải admin. ➡️ Chủ kho mở
Settings → Branches / Rules, ghi vào Packet Issue một trong ba: *chưa từng bật* · *đã bật, sẽ gỡ TRƯỚC khi land* ·
*đã bật, để nguyên* (khi ấy A5 phải đo thêm "PR từ danh tính `notebyme88` merge được").

❓ **Q4 — Thứ tự với các packet khác đang chờ cấp.** Write set không giao với `M9-FETCH-AUTH`, `WINDOWS-LEASE-SUITE`,
`THU-HOI-LEASE-A1`; chỉ giao TIỀM TÀNG với LO-319 (nháp). ➡️ Chạy **song song** với M9/WINDOWS; nếu cấp LO-319 thì cấp
packet này TRƯỚC (bản vá 1 dòng ở `ci_dang_ky_test.py`) hoặc SAU khi LO-319 land — không chồng.
