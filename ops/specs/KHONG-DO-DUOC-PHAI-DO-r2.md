# ĐẶC TẢ PACKET — `KHONG-DO-DUOC-PHAI-DO` **revision 2**

| | |
|---|---|
| `packet_id` | `KHONG-DO-DUOC-PHAI-DO` |
| `packet_issue` | **#401** |
| `revision` | **2** (thay `revision 1`, `sha256 3d8bf94c…`) |
| `generation` | 2 |
| `executor` | `claude` |
| `environment` | `cloud` |
| `review_class` | **`sensitive`** |
| `base` | `master` `3922add4` (đo `18:44:18Z 29-08-2026`, không đổi so r1) |
| `assurance_target` | **`human_audited`** — xem `vi_sao_khong_con_cross_approved` |

## `vi_sao_co_revision_nay`

**Khuyết tật nằm ở ĐẶC TẢ r1, không ở lượt thi hành.** Tiêu chí `A3` của r1 viết:

> *"Gỡ `do += 1` khỏi nhánh thứ ba trong `chay_moi()` phải làm ít nhất một ca ĐỎ"*

Đúng chữ, nhưng **quá yếu**: nó chỉ đòi **một** đột biến đổi màu, trong khi bất biến cần bảo vệ
trải trên **cả một miền**. Chính chỗ yếu ấy để lọt **hai** finding P1 liên tiếp của cross-review,
mỗi finding là một ô khác của cùng miền. Một tiêu chí mà mã có thể thoả trong khi bất biến vẫn hở
thì không phải tiêu chí — đó là `soan-spec` §L3 đọc ngược lại.

`PROTOCOL §3.2`: *"finding cho thấy chính spec thiếu thì verdict là `blocked` và đi qua revision mới."*
Đây đúng ca ấy. Chủ kho quyết `18:4xZ 29-08-2026`: siết `A3` thành **phủ trọn miền**.

## `hinh_dang_ke_thua`  — L4, và lần này bộ đếm CÓ THẬT

**Hình dạng: "bảo chứng ở tầng tiêu thụ hở một ô của miền."**
Đếm trong **chính packet này**, mỗi lần đều **tái lập được**, đơn vị = *số ô hở bị phát hiện*:

| # | phát hiện ở | ô hở | đột biến sống sót |
|---|---|---|---|
| 1 | khuyết tật gốc (`436fc32a`) | trạng thái thứ ba không được đếm | cổng làm tròn lên, `KHÔNG ĐO ĐƯỢC` lọt |
| 2 | cross-review lượt 1, `dc72c16b` | `chap_nhan is False` | `do += chap_nhan is None and o_trong_ci` ⇒ **27/27 vẫn xanh**, rc=0 |
| 3 | cross-review lượt 2, `9ab5eb36` | `(True, ngoài CI)` | ô ấy bị làm sai ⇒ **29/29 vẫn xanh**, rc=0 |

**BA lần.** `PROTOCOL §12`: *"Cùng hình dạng lỗi xuất hiện lần thứ ba bắt buộc xem lại có nên tiếp
tục cách làm đó, không chỉ vá lần thứ tư."* Vá lẻ từng ô là cách làm đã thua ba lần; `A3` mới
dưới đây đòi phủ **trọn miền**.

Ghi thêm cho người đọc sau: r1 khai `chua_do_duoc` rằng không có hồ sơ `#361` nên **không chép được**
bộ đếm tiền nhiệm. Bảng trên là bộ đếm do chính packet này sinh ra — packet kế nhiệm nào của
`KHONG-DO-DUOC-PHAI-DO` **phải chép bảng này sang**, đừng bắt đầu lại từ 0.

## `vi_sao_khong_con_cross_approved`

`codex_review_calls_used = 2 / 2` trên PR **#404** — **CẠN**. Hai lượt đều sinh output thật nên đều
tính (§12). §12 cấm *"gọi thêm bằng prompt/phiên khác để lách trần"*.

**Revision này KHÔNG nạp lại bộ đếm, và KHÔNG được mở PR mới để có bộ đếm sạch.** Lý do phải nói
thẳng: revision là đường HỢP LỆ cho *spec sai*, nhưng nếu nó đồng thời rửa sạch bộ đếm review thì
nó thành đúng cái "cờ nới bí mật" mà §12 cấm — chỉ khác là mặc áo hợp lệ. Nên packet r2 giữ nguyên
nhánh `claude/khong-do-duoc-phai-do-exec-1` và PR **#404**, và mức assurance hạ xuống
**`human_audited`** (§8 mục 2): người có danh tính bền, độc lập với executor, tự đọc spec/diff,
ghi evidence và neo verdict vào exact `reviewed_sha`.

## `write_set` — KHÔNG đổi so r1

| type | path |
|---|---|
| `exact` | `.claude/dev/ci_dang_ky_test.py` |

Đặc tả và lease land bằng **PR RIÊNG** (#403), không nằm trong write set.

## `ngoai_pham_vi` — KHÔNG đổi so r1

**N5** (`subagent_ghi_detect_test.py` rc=1 — thứ đang thực sự làm master đỏ) · **N7** (chậm 2,91×) ·
thêm neo `github-actions/windows` vào `CACH_LY` · `.github/workflows/ci.yml` · `ops/leases/**`.

## `muc_tieu` — 1–4 giữ nguyên r1, thêm mục 5

Mọi mục chiếu vào đường dẫn duy nhất `.claude/dev/ci_dang_ky_test.py` (**[CDK]**).

1. **[CDK]** Tách quyết định "có tính là ĐỎ không" thành hàm thuần `dem_la_do`.
2. **[CDK]** Nhận diện "đang ở CI" bằng `GITHUB_ACTIONS == "true"`, **độc lập** với `moi_truong_hien_tai`.
3. **[CDK]** `chay_moi()`: `chap_nhan is None` **và** trong CI ⇒ tính ĐỎ; ngoài CI ⇒ cảnh báo, không tính.
4. **[CDK]** Phản chứng canh ở **tầng tiêu thụ**, không chỉ ở vị từ.
5. **[CDK] MỚI —** Bảo chứng tầng tiêu thụ phải phủ **TRỌN MIỀN ĐẾM** bằng một cấu trúc **liệt kê
   miền** (bảng/vòng lặp), không phải danh sách ca rời rạc. Miền là
   `chap_nhan ∈ {None, True, False}` × `o_trong_ci ∈ {True, False}` = **6 ô**.

## `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| A1 | `dem_la_do(None, True)` ⇒ `True` | đột biến trả `False` ⇒ ca ĐỎ |
| A2 | `dem_la_do(None, False)` ⇒ `False` | đột biến trả `True` ⇒ ca ĐỎ |
| **A3** | **PHỦ TRỌN MIỀN.** Với **MỖI** trong 6 ô: (a) có ≥1 ca đi qua **chính `chay_moi`** khẳng định `do` đúng cho ô ấy; **và** (b) tồn tại một đột biến làm sai **RIÊNG ô ấy** mà bộ phản chứng **ĐỎ**. | Chạy 6 đột biến, mỗi cái hỏng đúng một ô. **Ô nào không làm bộ test đỏ ⇒ A3 KHÔNG ĐẠT.** Ngoài ra: gỡ hẳn `do += dem_la_do(...)` phải ĐỎ. **Cấm khai ĐẠT bằng "ít nhất một ca đỏ"** — đó là lỗi của r1 |
| **A3b** | **MỚI —** ca phải sinh từ cấu trúc **liệt kê miền**, để thêm giá trị vào miền mà quên ca thì lộ ra ngay | đọc mã: nếu ca lại là danh sách rời rạc thì A3b KHÔNG ĐẠT dù A3 đạt |
| A4 | `trong_ci` độc lập `RUNNER_OS` | đột biến suy từ `moi_truong_hien_tai` ⇒ ca ĐỎ |
| A5 | không hồi quy: `ĐĂNG KÝ 21/21`, `chan=19 cach_ly=2`, mọi đột biến cũ còn "ĐỎ đúng" | `python .claude/dev/ci_dang_ky_test.py` ⇒ `TỔNG: ĐẠT` rc=0 |
| A6 | `gate (ubuntu-latest)` **success** trên **exact head** đang xin land | lượt `pull_request` của PR #404 |
| A7 | Windows in ba dòng đỏ | **KHÔNG ĐO ĐƯỢC** — chủ kho quyết không chi ngân sách Windows. Không suy từ A6 |
| **A8** | **MỚI —** verdict `human_audited` neo đúng `reviewed_sha` đang xin land | thiếu ⇒ chưa đủ assurance, không được land |

## `chua_do_duoc`

- **A7** — như trên. A6 xanh **không** thay được.
- **Nguyên nhân `rc=1` của N5** và **nguyên nhân chậm 2,91× (N7)** — ngoài phạm vi, chưa đào.
- **Nợ neo linux có tái hiện cùng nguyên nhân trên windows không** — chưa đo; vì thế không thêm neo.
- **Ruleset / branch protection / "Dismiss stale approvals" (N10)** — REST `repos/*` 403, MCP không
  có tool đọc. Vẫn là lời khai.
- **Biên nhận `ops/reviews/*.receipt.yaml` cho hai lượt review đã dùng** — CHƯA lập, vì lease cho
  đúng một đường dẫn và thêm tệp là chạm điều kiện dừng S1. Hệ quả: bộ đếm review chỉ sống trong
  comment PR #404 (`5464067034`, `5464183462`) — đúng nợ **N12**. Phải đi bằng PR hồ sơ riêng.
- **Liệu 6 ô đã là TRỌN miền chưa** — đúng với `dem_la_do` hiện tại, vì `chap_nhan` chỉ nhận
  `None|True|False` và `o_trong_ci` là bool. Nếu ai mở rộng miền thì A3b là thứ bắt được, **nhưng
  chính A3b chưa từng bị kiểm bằng một lượt review chéo** — trần đã cạn trước khi nó ra đời.
