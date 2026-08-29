# ĐẶC TẢ ĐÓNG BĂNG — `CONG-DUYET-THEO-THAM-QUYEN` — **BẢN 1**

| trường | giá trị |
|---|---|
| `packet_id` | `CONG-DUYET-THEO-THAM-QUYEN` |
| `packet_issue` | #386 |
| `nguon_cap_viec` | Issue #386 `CONG-DUYET-DOC-THAM-QUYEN-SONG`. Không phải packet khắc phục của một packet đã land, nên `hinh_dang_ke_thua = khong_ap_dung`. |
| `review_class` | **`sensitive`** — `duyet_danh_tinh.py` quyết định AI ĐƯỢC DUYỆT, tức chạm authority. Vế nghiêm ADR-0044: ≤3 tệp, ≤300 dòng thêm. |

**GIỚI HẠN LỜI KHAI:** chứng minh BYTE tới consumer adapter. KHÔNG tuyên bố model "đã hiểu".
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC** — thứ ba làm cổng ĐỎ, không làm tròn lên.

---

## VÌ SAO — phép đo, không phải lập luận

Đo **02:38–02:47Z 29-08-2026**:

```
collaborator SỐNG (list_repository_collaborators):
    code2nguyen · ducthangho · notebyme88 · zichstudio          (4)
allow-list chép cứng, duyet_danh_tinh.py:47:
    NGUOI_DUOC_DUYET = ("ducthangho", "code2nguyen")            (2)
```

Trên PR **#392**, head `2ff4b8dc`, sau khi `notebyme88` duyệt thật:

```
notebyme88 APPROVED COLLABORATOR sha=2ff4b8dc 2026-08-29T02:38:44Z
→ cổng vẫn ĐỎ:
  "số bản ghi review=2 · được phép duyệt=ducthangho, code2nguyen"
  "ĐỎ: chưa có bản duyệt nào từ danh tính khác `ducthangho` trong code2nguyen, ducthangho"
```

**Cổng ĐỌC ĐƯỢC bản duyệt rồi VỨT ĐI** vì tên không nằm trong hai tên chép cứng. Nó phân biệt
CÁCH VIẾT chứ không phân biệt THẨM QUYỀN — đúng câu reviewer của kho đã viết và `CLAUDE.md`
chép lại.

**Chiều hỏng nguy hiểm hơn chưa ai đo, và không đo được từ phiên này:** người bị GỠ khỏi
collaborator vẫn nằm trong danh sách chép cứng nên vẫn duyệt được, vô thời hạn. Ghi ở
`chua_do_duoc`.

---

## `write_set` — HAI đường

```
.claude/dev/duyet_danh_tinh.py
.claude/dev/duyet_danh_tinh_test.py
```

Không ký tự đại diện. Kích thước hiện tại: 314 và 1122 dòng (đo 02:45Z 29-08).

**Đã đo ai giữ, 02:46Z** (cổng bản master; lần đo đầu trả `rc=12 KHÔNG_XÁC_ĐỊNH` vì nhánh cục
bộ tụt sau origin — cổng tự in cách chữa, đã fast-forward rồi đo lại):

```
cả hai đường → rc=11, NGƯỜI_GIỮ 1: tach-danh-tinh-github-exec-1r6-codex-20260828
  packet #348 TACH-DANH-TINH-GITHUB · Issue CLOSED · hiện vật CÓ trên master
  lease hết hạn 2026-08-29T04:05:00Z
```

Lease ấy là **xác chết** (nợ `AG-T0-01B`, Issue #385 — lần thứ TƯ trong một phiên): việc đã
land, Issue đã đóng, nhưng lease chưa hết giờ. Phải thu hồi hoặc đợi hết hạn TRƯỚC khi cấp
lease cho packet này. **Cấp chồng lấn là đúng thứ write-set exclusion sinh ra để chặn.**

## `ngoai_pham_vi` — cố ý KHÔNG làm

- **`.github/workflows/duyet-khac-danh-tinh.yml`** — giữ nguyên. Bản vá KHÔNG đổi chữ ký CLI
  (`--kho --pr --tac-gia --head-sha`), nên workflow không cần sửa. Nếu khi thi công hoá ra
  phải sửa nó thì đó là **S1: DỪNG, khai** — không tự mở đường thứ ba.
- **`.claude/dev/mcp_gh.py`** và `--danh-tinh` / `review-approve` / `ci` / `merge` — thuộc
  packet **P-B `MCP-GH-DANH-TINH-VA-CI`**, tách riêng vì `mcp_gh_test.py` đang bị lease
  `d9-con-ho-exec-1` (#382, Issue **OPEN**, hết 10:14Z) giữ, và vì 4 đường sẽ vượt vế nghiêm
  ADR-0044 ngay từ đầu.
- **Sửa danh sách collaborator trên GitHub** — không thuộc mã.

---

## `muc_tieu` — mỗi dòng chiếu vào một đường trong `write_set`

**M1** *(`duyet_danh_tinh.py`)* — `phan_quyet()` xét **THẨM QUYỀN** lấy từ `author_association`
của chính bản ghi review, thay cho việc so tên với một hằng chép cứng.

**M2** *(`duyet_danh_tinh.py`)* — tập thẩm quyền được nhận là **đúng ba giá trị**:
`OWNER` · `COLLABORATOR` · `MEMBER`. `CONTRIBUTOR` và `NONE` bị **từ chối**.
`CONTRIBUTOR` nghĩa là *từng có commit được merge* — nó KHÔNG mang quyền ghi nào, và người
ngoài gửi một PR được merge sẽ mang nhãn ấy vĩnh viễn.

**M3** *(`duyet_danh_tinh.py`)* — **xoá hẳn** hằng `NGUOI_DUOC_DUYET` và tham số `cho_phep`.
Giữ lại một danh sách tên song song là giữ nguyên đúng khuyết tật: người bị gỡ collaborator
vẫn duyệt được. Mọi chỗ in ra `NGUOI_DUOC_DUYET` (d.309) đổi sang in tập thẩm quyền.

**M4** *(`duyet_danh_tinh.py`)* — chặn tường minh mọi `login` kết thúc bằng `[bot]`, ĐỘC LẬP
với chốt `u["type"] != "User"` đang có (d.188). Hai chốt, hai lý do: `type` là trường TUỲ CHỌN
trong hợp đồng và mã cố ý fail-open trên nó; hậu tố `[bot]` là bất biến của GitHub. Một bot
được thêm làm collaborator sẽ mang `COLLABORATOR` và lọt qua M2 nếu không có M4.

**M5** *(`duyet_danh_tinh_test.py`)* — mỗi mục M1–M4 có ca `rXX_` riêng, và mỗi ca có **đột
biến riêng** giết đúng nó.

**M6** *(`duyet_danh_tinh_test.py`)* — giữ nguyên mọi hành vi đã khoá: neo `head_sha`,
`CHANGES_REQUESTED` chưa gỡ, tự-duyệt bị chặn, `reviews=None` là KHÔNG ĐO ĐƯỢC, mốc hỏng là
KHÔNG ĐO ĐƯỢC cho CẢ phán quyết, lọc state TRƯỚC / chọn mới nhất SAU.

---

## `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ

**A1 (M1, M2) — dữ liệu THẬT của #392 phải cho ĐẠT.** Ca dựng `reviews` đúng như GitHub trả
cho PR #392 (`notebyme88` · `APPROVED` · `COLLABORATOR` · `commit_id=2ff4b8dc…`), `tac_gia`
= `ducthangho`, `head_sha` = `2ff4b8dc…` ⇒ `phan_quyet` trả **`(True, …)`**.
*Phép đo làm nó ĐỎ:* trên mã TRƯỚC bản vá, chính ca ấy trả `(False, "chưa có bản duyệt nào…")`
— tức ca này ĐỎ trên nền và XANH sau vá. Không có vế "ĐỎ trên nền" thì ca không chứng minh
được nó đo bản vá.

**A2 (M2) — `CONTRIBUTOR` bị từ chối.** Cùng bản ghi, đổi `author_association` thành
`CONTRIBUTOR` ⇒ `(False, …)`. Tương tự `NONE`.
*Phép đo làm nó ĐỎ:* đột biến nới tập thẩm quyền thành chấp nhận `CONTRIBUTOR` ⇒ ca ĐỎ.

**A3 (M3) — không còn đường nào đi bằng TÊN.** `grep -n 'NGUOI_DUOC_DUYET' .claude/dev/*.py`
⇒ **0 dòng**. Ca kiểm chính điều đó, đọc từ tệp nguồn.
*Phép đo làm nó ĐỎ:* dựng lại hằng ấy ⇒ ca ĐỎ.

**A4 (M4) — bot mang `COLLABORATOR` vẫn bị chặn.** Bản ghi `login="x[bot]"`,
`author_association="COLLABORATOR"`, `type="User"` (cố ý khai gian trường tuỳ chọn) ⇒
`(False, …)`.
*Phép đo làm nó ĐỎ:* đột biến gỡ chốt `[bot]` ⇒ ca ĐỎ. Ca này phải ĐỎ **khi và chỉ khi** gỡ
chốt `[bot]`, không phải khi gỡ chốt `type` — nếu gỡ `type` cũng làm nó đỏ thì hai chốt chưa
độc lập và M4 chưa đạt.

**A5 (M6) — đối chứng KHÔNG ĐƯỢC ĐỘNG.** Toàn bộ `duyet_danh_tinh_test.py` chạy XANH với số
ca ≥ số ca nền, và bảng đột biến không có mục nào "sống sót" hay "giết nhầm thứ".
*Phép đo làm nó ĐỎ:* bất kỳ ca sẵn có nào chuyển màu.

**A6 — cổng THẬT trên PR #392 chuyển màu.** Sau khi packet land, lượt
`duyet khac danh tinh` trên #392 phải `success`.
*Phép đo:* đọc qua endpoint MCP `/mcp/x/actions`. **Đây là mục duy nhất không đo được
offline** — và là mục đã cắn cả packet W1-P1, nên không được bỏ.

---

## `hinh_dang_ke_thua`

`khong_ap_dung` — packet này không phải packet khắc phục của một packet đã land. Nó là việc
mới sinh từ Issue #386. Bộ đếm hình dạng lỗi bắt đầu từ 0.

---

## `chua_do_duoc` — ghi thẳng

- **Chiều hỏng "người bị GỠ collaborator vẫn duyệt được"** chưa có phản chứng chạy được: cần
  gỡ một người thật khỏi kho rồi đo, mà phiên này không có quyền và không nên có. Bản vá đóng
  chiều ấy **theo thiết kế** (thẩm quyền đọc từ mỗi review, không từ danh sách), nhưng câu ấy
  là suy luận về cấu trúc, KHÔNG phải phép đo. Đừng khai thành đã chứng minh.
- **`author_association` có luôn phản ánh quyền ghi HIỆN TẠI không** — GitHub tính nó tại thời
  điểm gửi review. Một bản duyệt cũ của người sau đó bị gỡ quyền vẫn mang `COLLABORATOR`. Neo
  `head_sha` thu hẹp cửa ấy (bản duyệt phải thuộc commit đang xét) nhưng **không đóng hẳn**.
  Chưa đo được độ rộng còn lại.
- **`duyet khac danh tinh` có phải required status check không** — MCP không có endpoint branch
  protection; lỗi ruleset khi thử merge #389 chỉ nêu `gate (ubuntu-latest)`. Nên chưa biết cổng
  này có chặn merge hay chỉ báo. Không suy đoán.
- **Parity Windows** — job `windows-latest` chỉ chạy ở master, `workflow_dispatch`, hoặc PR gắn
  nhãn `windows`.

---

## Điều kiện DỪNG

- **S1** cần đường dẫn thứ BA — kể cả khi hoá ra phải sửa `duyet-khac-danh-tinh.yml` ⇒ DỪNG, khai.
- **S2** vượt **300 dòng thêm** hoặc 2 tệp ⇒ DỪNG, khai (vế nghiêm ADR-0044 cho `sensitive`).
- **S3** `origin/master` đi tiếp mà CÓ chạm một trong hai đường ⇒ DỪNG.
- **S4** muốn giữ lại `NGUOI_DUOC_DUYET` "cho chắc" ⇒ DỪNG, xem M3.
- **S5** muốn khai một mục ĐẠT mà không có ca làm nó ĐỎ được ⇒ DỪNG.
- **S6** chạm trần HAI vòng review (ADR-0043) ⇒ DỪNG, không tự nâng. Trần này KHÔNG có cổng
  máy nào canh (`review_rounds_used` → 0 tệp, `nang_tran` → 0 tệp, đo 28-08).
