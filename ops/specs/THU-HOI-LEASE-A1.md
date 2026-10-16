# ĐẶC TẢ — `THU-HOI-LEASE-A1` — **BẢN NHÁP 0** (chưa đóng băng: 5 câu hỏi biên giới đang MỞ)

| trường | giá trị |
|---|---|
| `packet_id` | `THU-HOI-LEASE-A1` (slice **A1** của `THU-HOI-LEASE-VA-CAP-LAI` r9) |
| `packet_issue` | **CHƯA ĐĂNG** — chỉ đăng sau khi biên giới rỗng (soan-spec §1) |
| `nguon_cap_viec` | Spec cha r9 (`ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md`, sha256 `465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79`) §`write_set` dòng **A1**: *"ghim `MOC_BIA_MO_LICH_SU` + `BIA_MO_LICH_SU` từ receipt A0; nghiệm thu wiring thật; đổi cờ `True` khi Q10 đạt; sổ vẫn rỗng"* (ước 90–160 dòng). Nợ tiền đề: Issue **#499 §A** (A1–A4) và **§B** (B1–B5). Chủ kho duyệt đề xuất số 4 phiên 11-09-2026. |
| `review_class` | **`sensitive`** — `ops/lease_publish.py` là cổng đọc lease + `.github/workflows/**`. Vế nghiêm ADR-0044 ≤3 tệp / ≤300 dòng thêm: 3 tệp đúng trần; dòng thêm **chưa ước được** cho tới khi Q2 (schema ADR-0047 lớp 2) chốt. |

**GIỚI HẠN LỜI KHAI:** chứng minh BYTE tới consumer adapter. **Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

Bản này **không** phải đặc tả đóng băng. Nó tồn tại để (1) liệt kê đủ những gì A1 gồm, (2) nêu số đo hiện có, (3) đặt
trọn biên giới câu hỏi cho chủ kho — theo soan-spec §1 *"không hành động cho tới khi người dùng xác nhận đã hiểu giống
nhau"*. Sau vòng trả lời, bản 1 mới có băm để lease neo vào.

---

## Hiện trạng đo được (03:0xZ 11-09-2026, cây `27c413c3`)

```
ops/lease_publish.py:929   SO_THU_HOI_KICH_HOAT = False
ops/lease_publish.py:936   PROFILE_ADAPTER_DA_DUYET: frozenset = frozenset()      # RỖNG — mọi discovery production ⇒ 12
ops/lease_publish.py:938   BIA_MO_LICH_SU: tuple = ()                             # rỗng ở A0
ops/lease_publish.py:943   DESCRIPTOR_Q13_SHA256 = None                           # marker mới ⇒ 12
ops/lease_publish.py:1153  def hoso_adapter_do(...)  · 1176 def kiem_mien_ho_so(...)   # hồ sơ adapter, chưa mang identity lớp 2
ops/lease_publish.py:1657  def _du_bao_check(...)                                 # B1: đọc bản ghi qua GOI_GIT không đỡ decode
ops/lease_publish.py:1617  def _doc_blob_text_12(...)                             # B2: chưa bắt OSError
.github/workflows/ops-thu-hoi-admission.yml:136  uses: actions/upload-artifact@v4   # F07: ghim TAG, spec M9 đòi SHA đã readback
```

`ops-thu-hoi-admission.yml` hiện **không bao giờ xanh** (#499 C2a) ⇒ mọi nghiệm thu "wiring thật" của A1 là **KHÔNG ĐO
ĐƯỢC** cho tới khi `M9-FETCH-AUTH` land. Đây là phụ thuộc cứng (`depends_on`).

## `write_set` dự kiến (theo r9 slice A1 — không mở rộng ở nháp này)

```
ops/lease_publish.py                         1942 dòng
ops/lease_publish_test.py                    5394 dòng · 146 ca
.github/workflows/ops-thu-hoi-admission.yml   141 dòng
```

Ai giữ (02:54:23Z 11-09, 324/324 ref): cả ba **NGƯỜI_GIỮ 0**. Giao với `M9-FETCH-AUTH` (2/3 đường) và `WINDOWS-LEASE-SUITE`
(1/3) ⇒ cấp **cuối cùng** trong chuỗi M9 → WINDOWS → A1.

## Các mục A1 gồm — chiếu vào write set

| # | mục | tệp | nguồn | chờ chủ kho? |
|---|---|---|---|---|
| **M-A** | F07: ghim `actions/upload-artifact` bằng **commit SHA 40-hex đã readback**; t148 mở chốt "đúng một upload action" thành "đúng SHA X" | workflow + test | #499 A1 | **Q1** — SHA phải do chủ kho readback từ kho ngoài; executor bị cấm tự chọn |
| **M-B** | F08: mở rộng `hoso_adapter_do`/`kiem_mien_ho_so` theo ADR-0047 lớp 2 (identity HTTPS-helper · runtime · thư viện · trust store), rồi duyệt **mỏ neo đầu tiên** vào `PROFILE_ADAPTER_DA_DUYET` | `lease_publish.py` + test | #499 A2 | **Q2** — schema và GIÁ TRỊ đầu tiên là quyết định chủ kho |
| **M-C** | `DESCRIPTOR_Q13_SHA256`: ghim sha256 THÂN comment `5575587924` (PR #475) sau readback | `lease_publish.py` | #499 A3 | **Q3** — readback qua MCP **không byte-exact** (đã đo 22-08: thân comment bị chuẩn hoá thực thể HTML) ⇒ cần client thứ hai |
| **M-D** | `BIA_MO_LICH_SU` + `MOC_BIA_MO_LICH_SU` ghim từ receipt A0 (r9 Q6) | `lease_publish.py` | r9 A1 | không — đo được từ `ops/reviews/pr492-*.receipt.yaml`, nhưng receipt A0 hiện **không có trường mốc** (đo 03:04Z: 8 tệp, không `hinh_dang`, chưa kiểm khoá mốc) — ghi ở `chua_do_duoc` |
| **M-E** | B1 (`_du_bao_check` đỡ decode) · B2 (`_doc_blob_text_12` bắt `OSError`) · B3 (consumer đọc bytes thô nếu thêm so băm) · B4 (F13: 3 fd rò ở đường deadline) · B5 (F14: một snapshot clock cho cả loạt) | `lease_publish.py` + test | #499 B1–B5 | không |
| **M-F** | Đổi `SO_THU_HOI_KICH_HOAT = True` — **chỉ khi Q10 (a)–(i) của r9 đều có facts** | `lease_publish.py` | r9 M3/M9 | **Q5** — (d) required check + strict up-to-date + chặn bypass là việc NGOÀI kho |
| **M-G** | Q7/ADR-0044: một dòng quyết định bền về ngoại lệ dòng của A0 (3 tệp / +2387) | không phải mã — Issue #499 | #499 A4 | **Q4** |

## Câu hỏi biên giới — vòng 1 (hỏi TRỌN biên giới; câu nào phụ thuộc câu đang mở thì để vòng 2)

❓ **Q1 — SHA ghim cho `actions/upload-artifact`.** Phiên không readback được kho ngoài (MCP chỉ mở kho này; REST ngoài
bị proxy chặn). ➡️ Chủ kho mở trang release của `actions/upload-artifact` cho tag **v4 mới nhất đang dùng**, chép commit
SHA 40-hex và **dán vào Issue #499** kèm tên tag; executor ghim `uses: actions/upload-artifact@<sha> # v4.x.y` và t148
khoá đúng SHA ấy. Nếu chủ kho muốn giữ TAG (chấp nhận rủi ro tag di chuyển) thì ghi quyết định ấy — khi đó M-A là
"đóng F07 bằng quyết định", không phải bằng SHA.

❓ **Q2 — Schema ADR-0047 lớp 2 và mỏ neo đầu tiên.** Hồ sơ adapter cần thêm identity của: helper HTTPS (`git-remote-https`
đường dẫn + băm), runtime (`git --version` + băm binary), thư viện TLS (`curl-config`/`openssl version` mà git dùng), trust
store (băm bundle CA). Trên `ubuntu-latest` của Actions các băm ấy **đổi theo image** (image cập nhật hàng tuần) ⇒ mỏ neo
theo băm binary sẽ **chết mỗi tuần** và làm mọi discovery production ⇒ 12. ➡️ Khuyến nghị: lớp 2 ghim theo **hai tầng** —
(i) bắt buộc: tên + phiên bản (`git 2.x`, `curl 8.x`, `OpenSSL 3.x`, đường dẫn helper) và **OS image label** của runner
(`ImageOS`/`ImageVersion` từ env Actions); (ii) băm binary chỉ ghi vào receipt để audit, **không** là điều kiện 12. Mỏ neo
đầu tiên = hồ sơ đo trên lượt canary đầu tiên sau M9 land, chủ kho duyệt bằng comment neo băm hồ sơ. Câu trả lời này
quyết định số dòng thêm (ước +120–180) — vượt 300 thì tách M-B thành packet riêng (S2).

❓ **Q3 — Cách lấy sha256 thân comment `5575587924` cho Q13.** Đường MCP trả thân comment **đã chuẩn hoá** (`'`→`&#39;`,
`&`→`&`, đo 22-08-2026) ⇒ băm qua MCP là băm của một chuỗi KHÁC. ➡️ Chủ kho chạy trên máy cá nhân
`gh api repos/ducthangho/tra-luat/issues/comments/5575587924 --jq .body | sha256sum` (hoặc `pulls/comments/…` nếu là
review comment) và dán băm + lệnh đã chạy vào Issue #499; executor ghim và ghi rõ "băm do chủ kho đo bằng client X".
Không có băm ⇒ `DESCRIPTOR_Q13_SHA256` giữ `None` và A1 **không kích hoạt** (r9 Q13: không có neo ⇒ 12).

❓ **Q4 — Q7/ADR-0044 cho A0 (hồi tố).** A0 = 3 tệp / **+2387** dòng so trần 300; r9 §write_set đã khai ngoại lệ có
phạm vi. ➡️ Chủ kho ghi **một câu** trên #499: *"Chấp nhận ngoại lệ dòng cho A0 theo r9 §write_set; không tách slice hồi
tố"* — đó là dòng quyết định bền mà A4 đòi. Không cần ADR mới (ADR-0044 đã có cơ chế ngoại lệ có phạm vi).

❓ **Q5 — Tách A1 thành A1a / A1b?** M-F (bật cờ) đòi Q10 (d): required check `thu-hoi` + strict up-to-date + chặn bypass
— cấu hình ngoài kho, chỉ chủ kho làm và **readback bằng người**. Nếu gộp vào cùng packet mã thì lease sẽ treo chờ một việc
không thuộc executor. ➡️ **Tách**: `A1a` = M-A…M-E (mã + test, cờ vẫn `False`, ước ≤300 dòng nếu Q2 theo khuyến nghị);
`A1b` = M-F (một dòng + ca nghiệm thu wiring thật) cấp SAU khi chủ kho ghi facts Q10 (a)–(i) lên Issue. Hai spec, hai băm.

**Vòng 2 (sau khi vòng 1 đóng):** ước `numstat` A1a; catalog mutant cho M-B; ca wiring thật cho A1b (join check-run →
suite → run → attempt → artifact bằng đúng token, S≠H) — cần canary M9 đã xanh để có raw response.

## `chua_do_duoc` (nháp)

- **Mốc `MOC_BIA_MO_LICH_SU` trong receipt A0** — chưa kiểm receipt có trường ấy; nếu không có, M-D phải lấy từ journal/
  Packet Issue #488 (r9 nói "readback sau A0").
- **Canary M9 raw response** (r9 `chua_do_duoc` #10) — chưa có vì C2a; A1 không thể đóng băng "wiring thật" trước khi
  `M9-FETCH-AUTH` land.
- **Số dòng thêm** — phụ thuộc Q2/Q5.
- **Hình dạng kế thừa** — chép từ r9 §`hinh_dang_ke_thua` (2/3/1/6) cộng hai hình dạng mới của #499 (C2a: "cổng có mặt
  khác cổng đo được"; C3: "gate xanh lane PR, master đo lần đầu"); biên nhận A0 không mang bộ đếm (đo 03:04Z 11-09).
