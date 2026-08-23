# ĐẶC TẢ ĐÓNG BĂNG — `T33-DOI-SHELLCHECK`, **bản sửa đổi 2** (delta)

> **CHỈ ghi phần thay đổi** so với r1 (`1405d390ca9376725517d01ef5b8d1abffd6a09d78d2b7206c2f068e7711f4da`).
> r1 **KHÔNG bị sửa, KHÔNG bị xoá**; mọi thứ r2 không nêu thì r1 nguyên hiệu lực.

```yaml
packet_id: T33-DOI-SHELLCHECK
packet_issue: 249                 # gốc; N1 gộp vào theo quyết định người giữ kho ở #269
revision: 2
review_class: sensitive           # ĐO LẠI bằng chính `_tinh_lop_tu_write_set`, xem §review_class
executor: claude
reviewer: codex
assurance_target: cross_approved
base_sha: CHUA_XAC_DINH           # xem §base_sha — phụ thuộc #275, KHÔNG được điền bừa
```

Mọi con số trong tệp này đo trên `master = 00d4b3d730c185a7ebf0e7c0020bc914b5cb360f`, khoảng
**07:10Z–07:45Z 23-08-2026**, bằng `actionlint 1.7.7` + `shellcheck 0.9.0` cài thật trong container.
Theo **L5**, đo lại trước MỖI bước công bố — đừng chép số từ đây.

---

## Vì sao có bản này

Người giữ kho chốt ở `#269` (comment `5384370472`): **`N3` đi trước, `N1` gộp cùng**. Nhưng `N3`
**đã có đặc tả đóng băng** — chính là r1 của tệp này, đã qua **4 lượt cross-review**. Soạn một đặc tả
`N3` mới dưới `#269` là ghi đè một artefact đã trả giá 4 vòng, và làm hai Issue cùng tuyên bố sở hữu
một write set. Nên r2 là **delta trên r1**, không phải đặc tả mới.

r2 thêm **hai** mục tiêu và **đính chính ba** lời khai của r1. Nó **không** đặc tả một phép dẫn xuất
nào mới cho `M3`: giống `#238/r4`, phần `M3` **chép lại một bản vá ĐÃ CHẠY** kèm phản chứng của chính
bản vá ấy (§`ca_va_M3`).

---

## `nguon_cap_viec`

- r1 giữ nguyên (verdict lượt 2/3 của `#238`).
- **Bổ sung cho `M3`:** `ops/reviews/lease-dang-windows-review-3-claude-verdict.md`
  (`c98d83b8bf1a00b0…`, băm đã kiểm khớp master 23-08) — nợ `P3-1`, nêu lại ở `#269` mục `N1`.
- **Bổ sung cho `M4`:** `#269` mục `N3`, câu *"docstring của `t33` viết «phải XANH trên MỌI workflow»
  trong khi nó lint một tệp"*.
- Quyết định gộp: `#269` comment `5384370472`, in-session 23-08-2026.

**KHÔNG có dòng kế hoạch nào cấp việc này** — như r1 đã khai. Sinh từ phép đo, không từ kế hoạch.

---

## `review_class`

**`sensitive`** — đo lại bằng chính hàm của kho, không đọc bảng bằng mắt:

```
_tinh_lop_tu_write_set(['ops/lease_publish_test.py'])                    -> sensitive
_tinh_lop_tu_write_set(['ops/cai_actionlint.sh'])                        -> sensitive
```

⇒ `assurance_target` = **`cross_approved`**. Giữ r1.

---

## `write_set`

**KHÔNG ĐỔI so với r1** — đúng hai đường dẫn, không ký tự đại diện:

```
ops/lease_publish_test.py
ops/cai_actionlint.sh
```

`M3` và `M4` đều chiếu vào `ops/lease_publish_test.py`, đã có sẵn trong write set ⇒ **L2 thoả, không
phải nới**. Đây là lý do `N1` gộp được vào packet này mà không mở rộng quyền ghi.

**Trần kích thước.** ADR-0044, `sensitive`: **≤ 3 tệp / ≤ 300 dòng thêm**. Write set 2 tệp ⇒ còn dư
một suất tệp, **cố ý không dùng** (xem `ngoai_pham_vi` mục *độ phủ*). Đơn vị đề xuất và số đo ở §`tran_dong`.

### Write set **KHÔNG RẢNH** — đo 07:48Z 23-08-2026

Đây là thay đổi **nặng nhất** so với r1, và nó lật ngược câu *"write set rảnh, cấp lease được ngay"*
của Issue `#249`.

Quét **133 blob lease duy nhất trên 180 ref** (đã `--unshallow` + fetch đủ; phép so
`ls-remote` ↔ `for-each-ref` cho `comm -23` **rỗng** ⇒ không mù):

| đường dẫn | lease chạm | CÒN HẠN | người giữ THẬT |
|---|---|---|---|
| `ops/lease_publish_test.py` | 32 | **14** | `lease-hoi-toan-kho-exec-1r3-codex-20260823` (`#244`) |
| `ops/cai_actionlint.sh` | 2 | **0** | — |

Người giữ thật, đo được chứ không suy:

```
lease_id            : lease-hoi-toan-kho-exec-1r3-codex-20260823
packet_issue        : 244
write_set           : ops/lease_publish.py · ops/lease_publish_test.py   (ĐÚNG hai, không đại diện)
branch_ownership    : exclusive   (branch: codex/lease-hoi-toan-kho-exec-1r2)
leased_at_utc       : 2026-08-23T07:50:00Z
lease_expires_at_utc: 2026-08-24T07:50:00Z
PR                  : #275 MỞ (tạo 07:08:32Z)
diff PR #275        : +151 ops/lease_publish.py · +135 ops/lease_publish_test.py
verdict luot 1      : changes_requested, neo 13e3a9cf  -> packet DANG SUA, chua xong
```

**Con số 14 KHÔNG phải kết luận** — *"chưa hết hạn"* khác *"còn hiệu lực"*, đúng bài học
`SO-LEASE-KHONG-NAM-MOT-CHO`. 11 lease kia thuộc `PLAT-X8`/`PLAT-X8b`/`LEASE-DANG-*`, là packet đã
land (hồ sơ nằm trọn trên master); chúng là nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong` chứ không phải
writer sống. Thứ quyết định là **một** dòng: `#244` đang giữ ĐỘC QUYỀN và **đang ghi thật** vào đúng
tệp `M3`/`M4` cần. Vì vậy §`base_sha` neo vào *bất biến* (`#275` đã land hay chưa), **không** neo vào
số 14 — số ấy phân rã theo giờ, bất biến thì không.

**Bằng chứng sống cho L5, thu được TRONG chính phiên soạn tệp này.** Bản đầu của mục này ghi
`132 blob / 178 ref / 31 chạm / 13 còn hạn`, đo lúc 07:2xZ và **đúng lúc ấy**. Bốn mươi phút sau, phép
so `ls-remote` ↔ `for-each-ref` cho `comm -23` **KHÔNG rỗng**: hai nhánh mới trên máy chủ mà bản sao
cục bộ không có, một trong hai là `ops/verdict-lease-hoi-toan-kho-1`. Fetch rồi đo lại ⇒
`133 / 180 / 32 / 14`, **và một lease `r3` hoàn toàn mới** được cấp lúc 07:50Z — tức người giữ `#244`
đổi giữa hai lần đo. Cả **bốn** số hạng trôi trong khi bất biến (*`#244` đang giữ độc quyền*) không
đổi một chữ. Nếu neo quyết định vào con số thay vì vào bất biến, đặc tả này đã sai trong vòng 40 phút.

**Cảnh báo cho người đo lại:** bộ quét nháp của chính phiên này lúc đầu đọc trường `expires_at` (tên
trong protocol §4:260) trong khi tệp lease thật dùng `lease_expires_at_utc` ⇒ trả **31/31
`KHÔNG_ĐO_ĐƯỢC`**. Ca chứng (hỏi một đường dẫn bịa) vẫn cho `0` nên nó **không** lộ ra. Hỏi bộ quét một
ca mà bạn biết trước đáp án là cần, nhưng **chưa đủ**.

---

## `base_sha`

**`CHUA_XAC_DINH`, và đây là trạng thái ĐÚNG, không phải chỗ trống chưa điền.**

r1 khai `base_sha: 08bb4ecd6dbdb87267cb8179f52ac28c151eb4b9`. Số ấy **hết hiệu lực**: `#275` đang
thêm **+135 dòng** vào chính `ops/lease_publish_test.py`, nên mọi số hiệu dòng, số ca, và số `numstat`
đo trước khi nó land đều là số của một cây sẽ không còn tồn tại.

Điều kiện điền, người giữ kho chốt in-session 23-08: **xếp SAU `#244`**.

```
base_sha := HEAD cua master NGAY SAU khi #275 merge
```

Trước khi cấp lease phải đo lại **ba** thứ trên base ấy, vì cả ba đã trôi khi `#275` land:
`t33`/`t73` ở dòng nào · số ca của suite (nay **88**) · `numstat` của bản vá `M3`.

---

## `ngoai_pham_vi`

Giữ đủ bốn mục của r1. **Đổi một mục và thêm hai:**

| thứ | vì sao KHÔNG làm ở đây |
|---|---|
| Vá finding `SC2320` | Giữ r1 — đã được `#238` vá. **Xem đính chính Đ1**: `SC1003` mà `#269` nêu là finding KHÁC, ở tệp KHÁC, và cũng ngoài phạm vi |
| Bệnh đăng trùng + `ai-dang-giu` | `#244`. **Nay là quan hệ THỨ TỰ, không chỉ phân công** — xem §write_set |
| **Mở rộng `t33` sang workflow khác** | **ĐỔI so với r1: vẫn ngoài phạm vi, nhưng nay có SỐ ĐO và một Issue phải mở.** Xem §`do_phu` |
| Ghim `shellcheck` khác nếp `AL_VER` | Giữ r1 |
| **`N2` `N6` của `#269`** | Người giữ kho chốt: `N2` để sau (fail-close, chỉ sai chẩn đoán), `N6` tách riêng (khoá quan hệ caveat ↔ `reviewed_sha`, khác lớp) |
| **`N4` của `#269`** | Cần **một cổng** trên `gate_bat_buoc` của lease, không vá bằng văn xuôi. Cùng họ `N6`, không phải packet này |

### `do_phu` — độ phủ lint của kho, đo 23-08-2026

Đo thẳng, không suy:

| workflow | `t33` | `don_ref_chot_test.sh` | được lint bởi |
|---|---|---|---|
| `ci.yml` | không | không | **KHÔNG GÌ** |
| `launcher-windows.yml` | không | không | **KHÔNG GÌ** |
| `ops-open-pr.yml` | không | không | **KHÔNG GÌ** |
| `ops-don-ref.yml` | không | CÓ, nhưng **`-shellcheck= -pyflakes=`** | một phần |
| `ops-publish-lease.yml` | CÓ (shellcheck bật) | không | một phần |

**3/5 workflow không cổng nào lint.** Và tệp duy nhất mà `shellcheck` đổi được kết quả
(`ops-don-ref.yml`) lại được lint bởi lời gọi **cố ý tắt shellcheck** — `ops/don_ref_chot_test.sh:310`.
Không có chú thích nào giải thích lựa chọn `-shellcheck= -pyflakes=` ấy.

Vì sao **không** mở rộng ở đây, ba lý do đo được:

1. Mở `t33` ra cả 5 tệp ⇒ **ĐỎ ngay hôm nay**: `rc=1`, finding `SC1003` ở `ops-don-ref.yml:106`.
2. Chữa nó cần `.github/workflows/ops-don-ref.yml` vào write set — **L2 nói phải quyết TẠI ĐÂY**, và
   quyết định là: không, vì
3. `SC1003` nằm ở dòng 143, trong một mẫu `case` **lọc tên ref** (`*' '*|*'*'*|…|*'\'*|*//*`) — tức
   một **đường an ninh**. Đó là dương tính giả (mẫu ấy cố ý khớp dấu chéo ngược literal), nên hai cách
   chữa — viết lại mẫu, hay đặt `# shellcheck disable=SC1003` — đều là **đụng vào bộ lọc an ninh** để
   làm vừa lòng một linter. Việc ấy đáng một packet có review riêng, không đáng một hunk kèm theo.

⇒ **Phải mở một Issue riêng** cho lỗ độ phủ này (người giữ kho chốt in-session 23-08). Nó mang cả ba
việc: 3/5 workflow không được lint · `don_ref_chot_test.sh` tắt shellcheck không nêu lý do · quyết
`SC1003`. **Cổng cho `M4` sống ở Issue đó, không sống ở đây** — xem `chua_do_duoc` mục 4.

---

## `muc_tieu`

`M1` và `M2` của r1 **giữ nguyên, không sửa một chữ**. r2 thêm:

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M3** | Khoá **TRỤC PHÂN BIỆT** của cổng nền: quyết định bỏ qua phải tra theo **NỀN**, không theo **TÊN TỆP**. Cặp với `t73` trên CÙNG tuple | `ops/lease_publish_test.py` |
| **M4** | Hạ câu docstring của `t33` xuống **đúng bằng phép đo**: nó lint `ops-publish-lease.yml`, không phải *"MỌI workflow"* | `ops/lease_publish_test.py` |

### Phép đo làm nên `M3`

`t73` chứng minh *"nền `posix` thì tuple (`WORKFLOW_DANG`, job `dang`) không được bỏ qua"*. Nó **KHÔNG**
chứng minh quyết định ấy tra theo nền. Phản chứng, chạy trên worktree rời của `00d4b3d7`:

```
X1 = bo han menh de nen  : `if (nen or os.name) == "nt" and nhan and all(`  ->  `if nhan and all(`
X2 = doi sang TEN TEP    : ... -> `if tep.name != "ops-publish-lease.yml" and nhan and all(`
```

| bản | rc | tổng kết | ĐỎ |
|---|---|---|---|
| BASE (nguyên vẹn) | 0 | `88/88 đạt; đã chạy=88, bỏ qua=0` | — |
| `X1` | 1 | `79/80 đạt; đã chạy=80, bỏ qua=8` | `t73` |
| **`X2`** | **0** | **`88/88 đạt; đã chạy=88, bỏ qua=0`** | **KHÔNG CA NÀO ← đây là lỗ** |

`X2` là **một mệnh đề**, và nó làm cổng nền tra theo một trục hoàn toàn khác mà **toàn bộ chân Ubuntu
im lặng**. Thứ duy nhất tách hai trục là 8 dòng `BỎ QUA` trên chân `windows-latest` — chân **không
chạy cho PR thường** (`ci.yml` khai `pull_request:` không kèm `types:`, nên gắn nhãn `windows` cũng
không sinh lượt chạy nào; đường chắc chắn là `workflow_dispatch` trên đúng ref).

### `ca_va_M3` — CHÉP NGUYÊN VĂN, KHÔNG tự nghĩ lại

Theo `#238/r4/Q13`: cho executor tự nghĩ lại chính là đường mở ra hình dạng `E` lần sau. Ca dưới đây
**đã chạy**, số ở §`nghiem_thu` là số của chính nó. Chèn ngay **trước** `def main() -> int:`:

```python
@ca
def t89_truc_phan_biet_la_NEN_chu_khong_phai_TEN_TEP():
    """Cặp với `t73`: CÙNG tuple, ĐỔI mỗi nền, phải ra kết quả NGƯỢC nhau.

    `t73` một mình chỉ chứng minh "posix thì không bỏ qua". Nó KHÔNG chứng minh quyết
    định ấy tra theo NỀN: thay mệnh đề nền bằng phân biệt theo TÊN TỆP vẫn cho 88/88,
    rc=0 trên toàn chân Ubuntu (đo 23-08-2026). Ca này khoá đúng cái trục ấy.

    Đi qua `main()`, KHÔNG gọi thẳng `_ly_do_bo_qua_workflow` — tuân `r4/Q8`.
    """
    def bo(): raise BoQuaNen(WORKFLOW_DANG, "dang")
    rc, out = _chay_main_meta(bo, "nt")
    bang(rc == 0 and "bỏ qua=1" in out,
         f"cùng tuple mà nền nt KHÔNG bỏ qua: rc={rc}, {out!r}")
```

Ba điều về hình dạng ca này, mỗi điều là một quyết định đã cân:

- **`t89`, không `t74`.** `t74` ĐÃ CÓ (`t74_A1_A2_executor_khong_duoc_ha_lop_va_ve_dung_phai_QUA`,
  dòng 2666). Số hiệu cao nhất hiện tại là `t88`.
- **Ca RIÊNG, không nối vào `t73`.** Biến thể nối vào `t73` cũng chạy được và rẻ hơn (**3** dòng
  `numstat` so với **16**), nhưng nhãn ĐỎ của nó vẫn là `t73_nen_posix_khong_duoc_bo_qua_ca_nao` trong
  khi lỗi là chuyện nền `nt` — một ca gánh hai mệnh đề, đúng thứ `#238` đã trả giá. Người giữ kho chọn
  ca riêng, in-session 23-08.
- **Đi qua `main()`.** `_chay_main_meta` vá `os.name` rồi gọi `main()` thật; dây nối là
  `ops/lease_publish_test.py:2911` (`ly_do = _ly_do_bo_qua_workflow(ex.tep, ex.ten_job)`). Ca này
  **không** gọi thẳng hàm trợ giúp ⇒ tuân `r4/Q8`, và §`nghiem_thu` có phép kiểm chạy được cho điều đó.

### Phép đo làm nên `M4`

Docstring `t33` viết *"`actionlint` phải XANH trên mọi workflow"*. Thân ca lint **đúng một** tệp:
`goc / "ops-publish-lease.yml"`. Đó là **hình dạng A** — lời khai rộng hơn phép đo — nằm trong chính ca
sinh ra để chống một cổng nói dối. Bộ đếm `A` đang ở **7**, ngưỡng DỪNG là **8**; người giữ kho đã quyết
**giữ 7** (`#269`), nên `M4` là vá một vết đã biết, không phải khai một vết mới.

---

## `tran_dong`

**Đơn vị: `git diff --numstat` trên `write_set`, cột dòng THÊM.** Không phải dòng mã logic, không phải
toàn bộ range `base..HEAD` — nói thẳng vì đây đúng là câu mà `N4` của `#269` tồn tại để sửa, và vì
`#238/r4/Q14` đã trả giá một lần cho chính chỗ này.

Số đo được, trên `00d4b3d7`:

| khoản | numstat (thêm) | ghi chú |
|---|---|---|
| `M3` — ca `t89` kèm docstring | **16** | bản CHÉP NGUYÊN VĂN ở trên, đã chạy |
| `M3` — biến thể trần, không docstring | 8 | **không chọn** — kho có nếp mỗi ca một docstring nêu vì sao |
| `M3` — biến thể nối vào `t73` | 3 | **không chọn** — nhãn ĐỎ lẫn hai mệnh đề |
| `M4` — sửa câu docstring | ~2–4 | chưa đo được: phụ thuộc câu chữ cuối |
| `M1` + `M2` (r1) | **chưa có số** | r1 không đo được, và r2 cũng không |

**`#269` khai `N1` giá *"~2 dòng `git diff --numstat`"* — SAI trong chính đơn vị nó nêu.** Số nhỏ nhất
đo được là **3** (biến thể rẻ nhất, đã loại), và hình dạng được chọn là **16**. Đây là **lần thứ hai**
cùng một lỗi trên cùng vùng mã: `#238` verdict khai *"5 dòng"* (dòng mã logic) trong khi `numstat` cho
**8**, và `r4/Q14` phải ghi thẳng *"đừng lấy số 5 làm chuẩn"*. Ghi lại ở đây vì lời cảnh báo ấy rõ ràng
**đã không chặn được lần tái phát**.

**Đề xuất trần: `≤ 120` dòng thêm, `≤ 2` tệp.** Neo:

- `M3` + `M4` đo được ≈ **20**;
- `M1` + `M2` **chưa ai đo** — `M2` phải thêm đường cài `shellcheck` ghim phiên bản vào
  `ops/cai_actionlint.sh` (tệp hiện **0** lần nhắc `shellcheck`), cộng fixture workflow sai shell cho
  `B2`. r1 nêu mốc neo `PLAT-X8` cùng vùng: `+265` rồi `+313`, tức **đã vượt** trần `sensitive` 300 của
  ADR-0044;
- 120 chừa chỗ cho phần chưa đo mà vẫn **chật hơn nhiều** trần 300, để lượt vượt phải DỪNG và khai lý
  do chứ không trôi tới 300 rồi mới kêu.

Vượt trần ⇒ **DỪNG trước review**, khai lý do theo ADR-0044, xin bản sửa đổi. Không tự nới.

---

## `nghiem_thu`

`B1`–`B5` của r1 **giữ nguyên**, gồm cả ràng buộc chéo *"`B1` và `B4` cùng phải xanh trong một lượt"*.
r2 thêm:

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **W11** | `X2` bị bắt. | Ba số phải khớp CHÍNH XÁC, đã đo trên `00d4b3d7`: bản vá nguyên vẹn ⇒ `89/89 đạt; đã chạy=89, bỏ qua=0`, `rc=0` · bản vá **+** `X2` ⇒ `88/89 đạt; đã chạy=89, bỏ qua=0`, `rc=1`, ĐỎ `t89_truc_phan_biet_la_NEN_chu_khong_phai_TEN_TEP` · **đối chứng** `X2` **không** kèm bản vá ⇒ `88/88`, `rc=0` (XANH — đây là lỗ; tái hiện được thì mới biết ca đo đúng thứ ấy) |
| **W12** | `X1` vẫn bị bắt — bản vá **không** làm yếu `t73`. | bản vá **+** `X1` ⇒ `80/81 đạt; đã chạy=81, bỏ qua=8`, `rc=1`, ĐỎ `t73_nen_posix_khong_duoc_bo_qua_ca_nao` |
| **W13** | **Răng nằm ở DÂY NỐI, không ở thân hàm** (`r4/Q8`). | Gỡ `@ca` của `t70_W6_matrix_co_Windows_phai_chay_lai_tam_ca` — ca **DUY NHẤT** gọi thẳng `_ly_do_bo_qua_workflow` (đo: 4 lần xuất hiện trong tệp; dòng 189 định nghĩa, 2303 và 2911 là dây nối, 2607 là `t70`) — rồi áp lại từng đột biến. **Cả hai vẫn phải ĐỎ:** `+X1` ⇒ `79/80`, `rc=1`, ĐỎ `t73` · `+X2` ⇒ `87/88`, `rc=1`, ĐỎ `t89` |
| **W14** | `M4`: câu docstring của `t33` **không còn** khai rộng hơn thân ca. | **KHÔNG CÓ CỔNG — xem `chua_do_duoc` mục 4.** Đây là tiêu chí của **REVIEWER**, không phải của máy. Khai thẳng theo **L3** thay vì làm tròn thành đã có |

Lệch bất kỳ số nào ở `W11`–`W13` ⇒ **DỪNG**, báo số đo được. **Không sửa ca cho vừa số.**

Ba trạng thái, không phải hai: `có` · `không` · **`KHÔNG ĐO ĐƯỢC`** — và trạng thái thứ ba làm cổng
**ĐỎ**. Áp cho cả `B1`/`B4` của r1 (thiếu công cụ ⇒ ĐỎ, không bỏ qua) lẫn `W11`–`W13` (không dựng được
đột biến ⇒ ĐỎ, không kết luận "chắc là đạt").

---

## `hinh_dang_ke_thua`

**ĐÍNH CHÍNH r1.** r1 khai `A = 6 · B = 2 · C = 1 · D = 3 · E = 2`, đo từ
`ops/reviews/lease-dang-review-5-claude-verdict.receipt.yaml:92` (`bo-dem-sau-luot-5`). Con số ấy
**đúng lúc r1 viết** và **sai bây giờ**: biên nhận ấy thuộc packet **TRƯỚC** `#238`, còn bốn lượt của
chính `#238` đã đẩy `A` 6→7 và `E` 2→4.

Bộ đếm kế thừa cho r2, nguồn là `ops/specs/LEASE-DANG-WINDOWS-r4.md:72-73` (tệp trên master, băm đã
kiểm khớp `11972e8ce5d54330…`), xác nhận bởi `#269` comment `5384370472`:

```
A = 7   B = 2   C = 1   D = 3   E = 4   F = 2
```

- **`A = 7`, GIỮ 7.** Người giữ kho quyết ở `#269`; `M4` của packet này là vá một biểu hiện đã đếm,
  không khai biểu hiện mới. Ngưỡng DỪNG là **8**.
- **`E = 4`.** `#238` chạy **bốn** lượt executor và **cả bốn** lần lỗi nằm ở ĐẶC TẢ, không ở bản vá.
  Đó là lý do `M3` chép một bản vá đã chạy thay vì mô tả một phép dẫn xuất.
- **`F = 2` KHÔNG CÓ HIỆN VẬT BIÊN NHẬN.** Quét **47** biên nhận trên master ⇒ **0** lần. Ba chỗ duy
  nhất nhắc `F = 2` đều là prompt/spec, không phải biên nhận. r1 đã bắt đúng chỗ này và **đính chính
  ấy vẫn đứng** — chép `F = 2` sang đây để giữ liên tục hồ sơ, **không** được dùng nó làm cổng dừng.
  (r1 đo **39** biên nhận lúc 18:4xZ 22-08; nay **47**. Mẫu số trôi, kết luận `0` không đổi — đúng bài
  học *"kiểm SỐ HẠNG, đừng kiểm quan hệ"*.)

---

## `chua_do_duoc`

Giữ trọn ba mục của r1 (bản `shellcheck` CI sẽ nhận · workflow khác có đỏ khi bật shellcheck không ·
`SC2320` là finding duy nhất hay chỉ là đầu tiên). Thêm:

4. **`M4` không có cổng, và kho không có cơ chế nào để dựng một cổng như thế.** Đã tìm: `t42` —
   ca mà docstring của `t34` viện dẫn là *"canh cho docstring này không trôi rộng ra"* — thật ra khớp
   **marker nợ ↔ sổ `ops/NO_KY_THUAT.md`** hai chiều, **không** đọc văn xuôi docstring. Không có bộ
   canh docstring nào trong kho. Nên `W14` là tiêu chí của người, và lỗ ấy chỉ đóng được bằng cổng độ
   phủ ở Issue sẽ mở (§`do_phu`).
5. **Hành vi của `M3` trên chân `windows-latest` THẬT.** Tám cell của ma trận đột biến đều đo trên
   Linux. Trên `nt` thật, `_chay_main_meta` không cần vá `os.name` nữa và đường đi khác. `B5` của r1
   (lượt Actions thật trên exact head, gọi bằng `workflow_dispatch`) là chỗ đo — **chưa đo**.
6. **`numstat` thật của `M3` trên base thật.** Số **16** đo trên `00d4b3d7`. `#275` thêm +135 dòng vào
   cùng tệp; ca chèn *trước* `def main()` nên vị trí sẽ trôi. Con số có thể không đổi, nhưng
   **chưa ai đo nó trên base sẽ dùng**.
7. **`M1`/`M2` chưa có số kích thước nào** — r1 không đo được, r2 cũng không. Trần 120 đề xuất ở
   §`tran_dong` vì thế là **ước lượng có neo**, không phải số đo. Đo lại trước review.
8. **Byte thật của `#275` trên GitHub.** Đọc qua MCP; REST thẳng tới `repos/…` bị proxy chặn 403 trong
   container này, nên không có client thứ hai để đối chứng. Số `+151/+135` đọc từ `git diff` trên ref
   đã fetch — đó là bằng chứng git, đủ chắc; nhưng *trạng thái PR* (mở/đóng/merge) thì chỉ có một
   đường đọc.
9. **`don_ref_chot_test.sh` tắt shellcheck vì lý do gì.** Đọc 20 dòng quanh lời gọi: chú thích giải
   thích vì sao gọi `actionlint`, **không** giải thích `-shellcheck= -pyflakes=`. Chưa hỏi được người
   viết. Đừng đoán trong Issue độ phủ.

---

## Điều kiện DỪNG — đăng ký sẵn

Cổng dừng nào kêu thì **DỪNG và hỏi người giữ kho**, không tự quyết đi tiếp:

| # | điều kiện | trạng thái hiện tại |
|---|---|---|
| **S1** | `#275` chưa merge ⇒ **không cấp lease**, không bắt tay | **ĐANG KÊU** — `#275` mở 07:08Z; verdict lượt 1 `changes_requested`; lease `r3` cấp 07:50Z, hạn `2026-08-24T07:50Z`. Packet đang SỬA, chưa xong |
| **S2** | Bộ đếm hình dạng **`A` chạm 8** | `A = 7`, người giữ kho chốt giữ 7 |
| **S3** | Bộ đếm **`E` chạm 5** | `E = 4`. `M3` chép bản vá đã chạy nên không tái tạo `E`; **đặc tả thêm một phép dẫn xuất mới cho `M3` là chạm `S3`** |
| **S4** | `numstat` trên write set **vượt 120** dòng thêm | chưa đo trên base thật |
| **S5** | Bất kỳ số nào của `W11`–`W13` **lệch** so với bảng | đo được trên `00d4b3d7`; phải đo lại trên base thật |
| **S6** | Cần một đường dẫn **thứ ba** | `write_set` đúng 2. Xin lease sửa đổi, **không** tự nới — kể cả khi trần ADR-0044 còn dư suất tệp |
| **S7** | Lượt vá sau verdict cần đụng `.github/workflows/**` | ⇒ đó là Issue độ phủ, không phải packet này |

---

## Ai làm gì — và cross-provider có THẬT không

| vai | ai | ghi chú |
|---|---|---|
| executor | `claude` | giữ r1 |
| reviewer | `codex` | giữ r1 |
| assurance | `cross_approved` | `review_class: sensitive` ⇒ bắt buộc |

**Khai thẳng một rủi ro đã xảy ra ở `#238` và có thể lặp:** lượt cuối của `#238` mang nhãn
`cross_approved` nhưng phần cross-provider **rất mỏng** — reviewer `claude` viết bản vá, executor
`codex` chỉ **chép** lại (`r4/Q13` yêu cầu đúng như vậy, có lý do). Nghĩa là ở lượt ấy, bên "thi công"
và bên "nghĩ ra bản vá" **không độc lập**.

`M3` của r2 **lặp lại đúng hình dạng đó**: ca `t89` do phiên soạn đặc tả này (`claude`) viết và chạy;
executor `claude` sẽ chép. Nên với riêng `M3`:

- **giá trị cross-provider nằm ở `codex`, ở vòng REVIEW**, không nằm ở khâu thi công;
- reviewer `codex` phải **tự dựng lại** `X1`/`X2` và **tự chạy** `W11`–`W13`, không nhận bảng số ở trên
  làm bằng chứng. Reviewer phải được cấp **mirror git đầy đủ** trong sandbox — `#250` đo được: ba lượt
  chỉ có tệp `.md` cho `4 → 11 → 2` finding và **không con số phân rã nào**; lượt thứ tư có năng lực đo
  ra **ba** con số phân rã ngay lượt đầu;
- `M1`/`M2` **không** dính hình dạng này: chưa ai viết bản vá cho chúng.

Ghi ra đây vì nhãn `cross_approved` sẽ trông y hệt nhau ở cả hai trường hợp, và **không trường nào
trong biên nhận nói ra sự khác biệt ấy**.

---

## Neo — băm đã kiểm 23-08-2026 trên `master = 00d4b3d7`

| tệp | sha256 (16 đầu) |
|---|---|
| `ops/lease_publish_test.py` | `ab5cc14016bd189a` |
| `ops/specs/LEASE-DANG-WINDOWS-r4.md` | `11972e8ce5d54330` |
| `ops/reviews/lease-dang-windows-review-2-claude-verdict.md` | `e5dd9584d2e01172` |
| `ops/reviews/lease-dang-windows-review-3-claude-verdict.md` | `c98d83b8bf1a00b0` |
| `docs/PROTOCOL_DA_PHIEN.md` | `9226c06f7be0be79` |
| `ops/specs/t33-doi-shellcheck.md` (r1) | `1405d390ca937672` |

Cả 6 khớp giá trị neo lúc soạn ⇒ **không lệch**, không phải đo lại.

**Nguồn có thẩm quyền là TỆP CÓ BĂM trong kho.** Mọi bản chiếu của đặc tả này lên Issue hay comment chỉ
là bản chiếu; lệch thì tệp đúng.
