# ĐẶC TẢ — `R378-SYMLINK-DOI-DAC-QUYEN` — **revision 2, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `packet_id` | `R378-SYMLINK-DOI-DAC-QUYEN` |
| `revision` | **2** |
| `thay_the_cho` | revision 1, `f6cb467e5ce9b52e3e1e97d66726a9e52a2e58997f0d6adee5d9e8b68dd4c098` |
| `packet_issue` | **#574** |
| `nguon_cap_viec` | Nợ #574, mở theo chỉ thị chủ kho 20-09-2026 (*"Land xong thì mở nợ r378"*). Chỉ thị cấp lease r1: *"Cấp lease cho r378 đi"*, cùng phiên ~16:2xZ. **r2** là hệ quả của cross-review lượt 4, dưới chỉ thị 21-09-2026: *"Chạy lặp cross review, vá, đăng verdict cho tới khi approve"*. Xem §8. |
| `review_class` | **`sensitive`** — chạm `scripts/tl_selftest.py`, harness dùng chung, và ca đích đo một **chốt an ninh**. Cùng lớp mà #565 đã dùng cho chính tệp này. |
| `assurance_target` | **`human_audited`** — không đổi. **ĐÍNH CHÍNH lời khai của r1:** r1 viết `cross_approved` *"KHÔNG ĐẠT ĐƯỢC"* vì quota. Câu ấy **hết hiệu lực** — **bốn** lượt cross-review codex đã chạy trọn trên packet này (§8). Hạn quota là trạng thái tại thời điểm đo, không phải thuộc tính của đường. Điều KHÔNG đổi: một lượt review máy vẫn **không** cấp được `human_audited`. |
| `executor` | `claude` |

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

---

## 0. Quyết định của chủ kho — câu mà #574 dành riêng cho người giữ kho

Nợ #574 §*"Việc phải làm"* mục 3 khai rằng cách xử `KHÔNG ĐO ĐƯỢC` *"là một quyết định của người
giữ kho, không phải chỗ để executor tự chọn"*. Đã hỏi và đã chốt:

> **ĐỎ — fail loud như `_c41`.**

Dựng được indirection thì ca đo như thường; **không** dựng được thì ném `AssertionError` **có tên**
và ca **ĐỎ**. Không bỏ qua êm, không tha.

Giá phải trả, ghi thẳng chứ không làm nhẹ: trên một nền không dựng nổi reparse point, suite sẽ đỏ
vì **MÔI TRƯỜNG**. Khác với bệnh `r330` mà #565 vừa chữa ở đúng một điểm — lần này nó **NÓI RA**
lý do bằng một tên lỗi đọc được, thay vì đỏ câm.

### 0.1 — Vì sao có revision 2

Cross-review `codex` **lượt 4** phán `A6` là **`VÁ HỜ`** và ra một **P2**:
`phan-hang-giet-gia-thieu-doi-chung` — **lần thứ TƯ cùng slug**.

Đột biến `m11` cho `_r378_classify` so **TÊN LỚP** (`type(exc).__name__`) thay vì so LỚP. Nó
qua đủ **bốn vế** của `A6` và **sống toàn suite `1715/1715`** — phiên này đo lại độc lập, ra
đúng con số ấy. Phản chứng phân biệt được hai chiều: lớp TRÙNG TÊN khác `id()` ⇒ bản đúng cho
`false_credit:_R378SaiKyVong`, `m11` cho `killed`; lớp CON thật ⇒ ngược lại.

**Đây là điều kiện dừng mà phiên này TỰ ĐĂNG KÝ TRƯỚC**, ghi trong commit `efaf576`:

> *"nếu lượt 4 lại ra một biến thể nữa thì câu trả lời đúng KHÔNG phải vế (e) — mà là viết lại
> `A6` theo MA TRẬN (lớp × thông điệp × oracle có chạy không), và đó là thay đổi đáng có đặc tả
> riêng."*

Reviewer độc lập đi tới đúng kết luận ấy và **không đề nghị vế (e)**. Nên r2 tồn tại vì một điều
kiện dừng đã chạm, không vì có ý tưởng mới.

**Bốn lượt, bốn bản vá đúng-chỗ-được-chỉ, bốn lần còn một cửa không ai chỉ:**

```
lượt 1  m5     mất phủ CỦA CHỈ MỤC khi đổi fixture
lượt 2  m7/m9  bộ phân hạng có BA hạng, ca chỉ canh MỘT
lượt 3  m10    ba hạng đã canh, nhưng canh bằng THÔNG ĐIỆP
lượt 4  m11    canh theo lớp, nhưng so bằng TÊN lớp
```

Cả bốn quanh **CÙNG MỘT thứ**: bộ phân hạng đột biến — tức chính THƯỚC ĐO mà mọi con số của
packet dựa vào. `CLAUDE.md`: *"đếm HÌNH DẠNG lỗi, đừng chỉ đếm lỗi; cùng một hình dạng lặp ba
lần trở lên thì câu hỏi đúng là 'có nên làm việc này không'"*.

**Lý do cấu trúc, và nó là thứ đáng nhớ hơn con số 4:** bốn vế rời là **bốn ĐIỂM** trong một
không gian ba chiều. Mỗi lượt reviewer chỉ cần tìm một điểm chưa ai chạm. Ma trận phủ theo
**TRỤC**, nên một cài đặt sai phải làm ít nhất một Ô đỏ dù nó sai theo chiều nào.

r2 **KHÔNG đổi** bệnh, `write_set`, `ngoai_pham_vi`, hay `M1`–`M5`. Nó viết lại `A6` và thêm
`A11`.

## 1. Bệnh — đo được, `origin/master` `700ca8c7`

Ca `_c378_resolve_phai_o_trong_kho` (`scripts/tl_selftest.py:25123–25148`) dựng phản chứng bằng
**symlink TỆP**:

```
scripts/tl_selftest.py:25133        link.symlink_to(outside)
```

Trên Windows thiếu `SeCreateSymbolicLinkPrivilege` ⇒ `OSError [WinError 1314]` ⇒ `_t110` nuốt
thành `False` ⇒ `[FAIL]`. Đo trên máy chủ kho 20-09-2026 (b7 `02:37Z`): ca ĐỎ ở **cả hai vế**
nền `dc85dd0a` và ứng viên `8c425b1` ⇒ **không phải hồi quy của #565**.

Ca này **không phải ca thường**. Nó là ca **đột biến** đo răng của một chốt an ninh:

```python
cat = _r378_classify("if resolved.is_relative_to(root_resolved):", "if True:", body, oracle, root=root)
return normal and cat == "killed"
```

Mất ca ⇒ mất **bằng chứng rằng chốt chống thoát cây kho còn răng**, không chỉ mất một ca.

### Cách chữa đã có sẵn trong CHÍNH tệp này — và #574 đã đoán ĐÚNG cơ chế, SAI kết luận

`scripts/tl_selftest.py:29571` (`_c41_fragment_read_error`) làm đúng thứ cần, **không cần đặc quyền**:

```python
if _os41.name == "nt":
    junction_result = _sp41.run([COMSPEC, "/d", "/c", "mklink", "/J", str(linked_root), str(physical_root)], ...)
    if junction_result.returncode != 0:
        raise AssertionError(f"JUNCTION_CREATE_FAILED:{rc}:{stderr}")
else:
    try:
        linked_root.symlink_to(physical_root, target_is_directory=True)
    except OSError as exc:
        raise AssertionError("DIRECTORY_SYMLINK_CREATE_FAILED") from exc
```

#574 viết *"KHÔNG PORT THẲNG ĐƯỢC … junction chỉ làm được cho THƯ MỤC"* — **đúng về cơ chế**. Nhưng
kết luận đi kèm (*"hướng khả dĩ … ĐÂY LÀ GIẢ THUYẾT, CHƯA CHẠY"*) nay **hẹp hơn sự thật đo được**:
mẫu ấy **đã tồn tại, đã chạy, đã có `FAIL LOUD`** trong chính tệp này. Việc còn lại không phải nghĩ
ra một hướng, mà là **tái dùng một mẫu đã có**.

Đó là một ca `LOI-KHAI-RONG-HON-PHEP-DO` **ngược chiều** — lời khai HẸP hơn phép đo — và nó cũng
tốn thời gian y như chiều kia. Ghi ra vì bộ đếm của kho chỉ đang đếm một chiều.

## 2. `write_set`

```
scripts/tl_selftest.py
RELEASE_MANIFEST.json
```

Đúng **hai** đường, trong trần `ADR-0044:5` (≤3 tệp). **Không xin ngoại lệ tệp.**

| đường | `ai-dang-giu` 16:13Z 20-09 |
|---|---|
| `scripts/tl_selftest.py` | `rc=0` · **NGƯỜI_GIỮ 0** |
| `RELEASE_MANIFEST.json` | `rc=0` · **NGƯỜI_GIỮ 0** |

Tập tên ref hai nguồn: **482/482**, hai chiều rỗng.

`RELEASE_MANIFEST.json` **bắt buộc** có mặt: `scripts/tl_selftest.py` **nằm trong** manifest, nên
sửa nội dung nó làm `sha256` lệch dù `file_count` không đổi (`CLAUDE.md` §Quy ước deploy mục 5).

## 3. `ngoai_pham_vi`

| thứ CỐ Ý không làm | lý do |
|---|---|
| Sáu ca `r378` còn lại | Không ca nào cần đặc quyền; cả sáu vẫn xanh. Chạm là mở rộng phạm vi. |
| `_c41_fragment_read_error` (`:29571`) | Là **nguồn mẫu**, không phải đích sửa. Đụng nó là đổi một ca đang xanh. |
| `_t110` | #565 vừa sửa; packet này không chạm. |
| Bật Developer Mode / đổi cấu hình máy | Ngoài kho, và không phải thứ một packet mã sửa được. |
| `gate (windows-latest)` | `manual_ci_budget: 0`. Là **CHỌN KHÔNG ĐO**. |
| `_kiem_bia_mo`, lease cũ đã hết hạn | Lease `r330-rig-quyet-mau-r1-g1-claude` **đã hết hạn tự nhiên 16:02Z**; viết bia mộ vào nó là mua một lượt `ops — đăng lease bằng git` ĐỎ (bệnh #579). Lease của packet này khai `thay_the_cho: []`. |

## 4. `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | `_c378_resolve_phai_o_trong_kho` dựng phản chứng bằng **gián tiếp THƯ MỤC**, không bằng symlink TỆP: `outside/` nằm ngoài cây kho, một junction (Windows) hoặc directory symlink (POSIX) trong cây kho trỏ tới nó, và `outside/r378_escape.py` là đích. | `scripts/tl_selftest.py` |
| **M2** | Không dựng được indirection ⇒ `AssertionError` **có tên** (`JUNCTION_CREATE_FAILED:<rc>:<stderr>` hoặc `DIRECTORY_SYMLINK_CREATE_FAILED`) ⇒ ca **ĐỎ**. Tái dùng đúng hình dạng `_c41`, không phát minh hình dạng mới. | `scripts/tl_selftest.py` |
| **M3** | **Răng giữ nguyên:** đột biến `if resolved.is_relative_to(root_resolved):` → `if True:` vẫn phải làm ca ĐỎ, và `_r378_classify` vẫn trả `"killed"`. | `scripts/tl_selftest.py` |
| **M4** | Kiểm **tiền đề** trước khi đo: nếu đường đã dựng mà `link.resolve()` **không** thoát ra ngoài `root` thì ném `AssertionError("PATH_MISMATCH_NOT_CREATED")` — đúng nếp `_c41`. Thiếu chốt này thì ca có thể xanh vì phản chứng chưa từng tồn tại. | `scripts/tl_selftest.py` |
| **M5** | Tái sinh `RELEASE_MANIFEST.json` sau khi sửa. | `RELEASE_MANIFEST.json` |

## 5. `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | phép đo làm nó **ĐỎ** |
|---|---|---|
| **A1** | **RĂNG — tiêu chí quan trọng nhất.** Đột biến `if resolved.is_relative_to(root_resolved):` → `if True:` làm ca ĐỎ; `_r378_classify` trả `"killed"`. | Chạy chính `_r378_classify` của ca. Bản vá nào làm đột biến ấy SỐNG SÓT là **biến một ca an ninh thành ca trang trí** ⇒ DỪNG, không phải vá tiếp. |
| **A2** | Ca ĐẠT trên POSIX. | Chạy `tl.py --selftest`; ca phải `[OK]`. |
| **A3** | Ca **không còn** `symlink_to` cho một TỆP. | `grep -n 'symlink_to' quanh thân ca` ⇒ chỉ còn dạng `target_is_directory=True`. Đột biến quay về symlink tệp ⇒ tiêu chí ĐỎ. |
| **A4** | Không dựng được indirection ⇒ **ĐỎ có tên**, không bỏ qua êm. | Ca tiêm: ép nhánh dựng trả lỗi ⇒ phải thấy `AssertionError` mang đúng tên, và `_t110` in ra kiểu ngoại lệ (đường đã có từ #565). Đột biến nuốt thành `return False` câm ⇒ ĐỎ. |
| **A5** | **M4**: indirection dựng xong mà `resolve()` không thoát khỏi `root` ⇒ `PATH_MISMATCH_NOT_CREATED`. | Ca tiêm: trỏ indirection vào một thư mục NẰM TRONG `root` ⇒ phải ném. Đột biến bỏ chốt ⇒ ca ĐỎ. **Đây là chốt chống "ca có MẶT khác ca có ĐO".** |
| **A6** (VIẾT LẠI ở r2 — **MA TRẬN**, thay bốn vế rời của r1) | `_r378_classify` phải đúng trên **MỘT MA TRẬN BA TRỤC**, không phải trên bốn điểm rời. Trục **LỚP**: lớp THẬT · lớp CON · lớp **TRÙNG TÊN khác `id()`** · lớp THƯỜNG. Trục **THÔNG ĐIỆP**: giống hệt oracle đúng · khác · rỗng. Trục **ORACLE**: chạy-và-ném · chạy-và-thoả · KHÔNG chạy (khâu dựng hỏng). Tổng **14 ô**: 4×3 khối A, 1 khối B, 1 khối C. | Mỗi ô có `expected` ghi sẵn là **DỮ LIỆU**, KHÔNG suy từ chính `_r378_classify` — nếu suy ra từ đó thì ma trận chỉ chứng minh bộ phân hạng nhất quán với chính nó (reviewer lượt 4 cảnh báo đúng chỗ này). Hỏng ô nào thì ném `AssertionError` nêu **ĐÚNG toạ độ ô** kèm `expected`/`observed`/`oracle_calls` — không trả `False` câm. Trục LỚP dùng cờ `bat_duoc` viết tay **kèm chốt tự kiểm** so với `issubclass`, để bảng fixture không âm thầm trôi. **GIỮ NGUYÊN ngữ nghĩa `except` của Python**: lớp CON vẫn là `killed`; ma trận ĐO bộ phân hạng, nó KHÔNG tự quyết đổi sang so kiểu chính xác. |
| **A11** (mới ở r2) | Ma trận phải **CÓ RĂNG với cả bốn đột biến lịch sử**, và **ô đỏ của mỗi cái là một phép ĐO, không phải một dự đoán**. | Chạy TOÀN suite, TUẦN TỰ (xem §8.4 — chạy song song làm hai lượt chết vì trạng thái dùng chung), ghi lại ô đỏ THẬT của từng đột biến kèm `expected`/`observed`/`oracle_calls`. **Nếu hai đột biến khác nhau làm CÙNG một tập ô đỏ thì chúng là bộ TƯƠNG ĐƯƠNG**, ma trận đang đo ÍT trục hơn nó khai, và điều đó phải được KHAI — không được đếm thành hai. **Và tiêu chí này KHÔNG ghi trước ô nào ứng với đột biến nào**: bản nháp của chính r2 từng ghi *"`m7` ⇒ ô `LỚP=that`"* và phép đo BÁC ngay — `_R378SaiKyVong` kế thừa `RuntimeError`, nên `except RuntimeError` của `m7` vẫn bắt được nó; ô đỏ thật là `LỚP=thuong, TĐ=goc`. Một tiêu chí nghiệm thu ghi sẵn ô đích là một tiêu chí có thể SAI trước khi ai chạy nó. |
| **A7** | `tl.py --selftest` **DELTA so `origin/master` = 0** trên POSIX, và `r378_l7_resolve_phai_o_trong_kho` ở tập ĐẠT của cả hai vế. | **Đo hai vế trong MỘT lệnh**, cùng các bước, chạy liền nhau. So **TẬP TÊN** ca đỏ, không so số đếm — *"mất một ca đỏ cũ, thêm một ca đỏ mới, tổng không đổi"* là ca mà phép đếm không bắt được. Nền đo 20-09 trên Linux: **1711/1711**; **đo lại trước khi tin** (L5). |
| **A8** | `release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true` **và** `expected == checked`. | Chạy **tại chỗ, đúng lệnh của lane LAND**. Lane PR **KHÔNG** bắt được lệch manifest (`if: github.ref == 'refs/heads/master'`; lane WORKER sinh manifest tạm nên hấp thụ mọi thay đổi nội dung) ⇒ PR xanh, master ĐỎ. |
| **A9** | `numstat` chạm **đúng hai** đường của `write_set`. | Đột biến thêm đường thứ ba ⇒ ĐỎ. Chốt write-set exclusion §5. |
| **A10** | `doctrine-scan` · `adr-song` · `doc-claims-check --strict` · `git diff --check` `rc=0`, `core.abbrev = 7`. | `rc` đọc **trực tiếp**, không qua pipe (nợ `RC-QUA-PIPE-KHONG-CO-CHOT`). |

## 6. `hinh_dang_ke_thua` (L4) — chép từ #565

| hình dạng | số lần | nguồn |
|---|---|---|
| `RIG-QUYET-MAU-CUA-PHEP-DO` | **5** | Chép từ #565 (4 ca `CLAUDE.md` 24-08 + `Đ1`). **Packet này chạm đúng lớp ấy**: một ca đỏ vì RIG (thiếu đặc quyền), không vì mã. |
| `NGOAI-LE-BI-NUOT-LANG` | **2** | Chép từ #565. Ca r378 từng đỏ **câm** trước khi `Đ2` land — chính nó là ca thứ hai. |
| `LOI-KHAI-RONG-HON-PHEP-DO` | 7 → **9** | Chép 6 từ biên nhận #565. **+1**: câu *"KHÔNG PORT THẲNG ĐƯỢC … giả thuyết, chưa chạy"* của #574 **hẹp hơn** phép đo — mẫu ấy đã có sẵn và đã chạy trong cùng tệp. Lời khai lệch phép đo **theo chiều hẹp** cũng là lệch. |

`RIG-QUYET-MAU-CUA-PHEP-DO` đã ở mức **5**, quá ngưỡng ba lần từ lâu. Hệ quả bắt buộc: `M1` chữa
bằng **KIẾN TRÚC** — bỏ hẳn nhu cầu đặc quyền khỏi đường chính — chứ **không** bằng một `try` bọc
thêm quanh `symlink_to`.

## 7. `chua_do_duoc`

1. **Junction có thật sự làm `resolve()` thoát khỏi `root` trên Windows không** — **KHÔNG ĐO ĐƯỢC**
   từ phiên này: container là Linux, không dựng được nền thiếu đặc quyền để phản chứng. Cơ sở
   hiện có là `_c41` dùng đúng cơ chế ấy và **đang xanh**, kèm chốt `PATH_MISMATCH_NOT_CREATED`
   chứng tỏ nó có thoát. Đó là **bằng chứng gián tiếp mạnh, KHÔNG phải phép đo cho ca này.**
   Đóng bằng một lượt chạy trên máy chủ kho sau khi vá.
2. **`WinError 1314` có phải chặn DUY NHẤT của ca không** (#574 §Việc phải làm mục 1) — chưa đo.
   Nếu gỡ nó ra mà ca vẫn đỏ vì một lý do khác thì `M1` mới chỉ bóc một lớp.
3. **`gate (windows-latest)`** — **CHỌN KHÔNG ĐO** (`manual_ci_budget: 0`), không phải không đo
   được. Nên sau packet này vẫn **không ai biết** ca ấy xanh hay đỏ trên runner — đúng lớp
   *"cổng không nói dối, nó VẮNG MẶT"*.
4. **Số dòng thêm** — r1 ước **+40…+90**; **ước ấy đã sai**, đo thật ở `efaf576` là **+246/-6**
   cho `scripts/tl_selftest.py` cộng `5/5` cho manifest. Reviewer lượt 4 xác nhận và ghi rõ đó
   là một ƯỚC bị trôi, không phải một phép đo bị sai. Trần `sensitive` là **300**; chủ kho đã
   nới trần DÒNG cho đợt 21-09-2026 lên **3000** (xem `ops/specs/dang-lease-dau-truoc-kiem-sau-r5.md`
   §8 — cùng chỉ thị, cùng đợt). **Đo lại ở head cuối, đừng chép con số này.**
5. **Số ca của suite** — nền đo **1711/1711** trên Linux ngày 20-09, head `efaf576` đo
   **1715/1715**. Con số ấy **sẽ trôi**; đo lại ở cả hai vế trước khi kết luận, đừng chép.
6. **Bốn ca BỎ QUA NGẦM mà vẫn in `[OK]`** — 2 toàn bộ + 2 một phần, reviewer lượt 3 đo và lượt
   4 xác nhận. Bốn hàm ấy **không đổi so base** ⇒ nợ KẾ THỪA, ngoài `write_set`. Hệ quả phải
   nhớ, và nó đã làm packet này khai sai một lần: **`[FAIL]=0` KHÔNG hàm ý "bỏ qua = 0"**, vì
   harness không in gì cho ca bỏ qua.
7. **Toàn suite có `1714` tên phân biệt** vì `r3_bust_cache_after_write` xuất hiện HAI lần — một
   trùng THẬT, có từ trước packet này, ở chỗ khác. Reviewer lượt 4 đo. Chưa ai truy nó.
8. **Windows thật** — vẫn **KHÔNG ĐO ĐƯỢC**. Bốn lượt cross-review đều chạy trên Linux.

## 8. Bốn lượt cross-review — và r2 là hệ quả của lượt 4

| lượt | `reviewed_sha` | verdict | finding | đột biến sống sót |
|---|---|---|---|---|
| 1 | — | `changes_requested` | `m5` | mất phủ CỦA CHỈ MỤC |
| 2 | — | `changes_requested` | `phan-hang-giet-gia-thieu-doi-chung` | `m7`, `m9` |
| 3 | `20641d5` | `changes_requested` | cùng slug, ĐỔI HÌNH DẠNG | `m10` |
| 4 | `efaf576` | `changes_requested` | cùng slug, **VÁ HỜ** | **`m11`** |

`VERDICT.md` lượt 4: `sha256 5161cfb9b0623e4fac3e0fbdad9f9eb8280152f10e9e2a5b5d32088418fd527e`,
130272 B, 4457 dòng. `reviewed_tree` `2a34c288`.

### 8.1 — Reviewer xác nhận khớp (liệt kê cả cái KHỚP)

```
selftest head 1715/1715 rc=0 · base 1711/1711 rc=0 · DELTA = 0, không mất tên
ca bỏ qua     2 toàn bộ + 2 một phần, đều in [OK] — và r378 KHÔNG thêm ca skip nào
numstat       246/6 + 5/5 = đúng 2 tệp write set
release       ok=true · 180 == 180 · package_hash_match=true
năm cổng      doctrine-scan · adr-song · doc-claims-check --strict · diff-check · golden-test  đều rc=0
m7 · m9 · m10 mỗi cái 1714/1715 rc=1, đỏ ĐÚNG một ca A6
SPEC r1       f6cb467e… byte-identical với blob trong git
manifest      chỉ 5 leaf đổi; tái dựng từ manifest nền + byte selftest mới ⇒ BẰNG head hoàn toàn
diff          không tràn mục tiêu: 1 định nghĩa cũ đổi + 3 helper + 4 ca r378
```

Phân hạng đột biến của reviewer: `m1`–`m10` **giết thật** ở ca đích; `m11` **sống sót**. Không
tín dụng giả nào bị đếm nhầm thành giết.

### 8.2 — HAI lời khai SAI của executor, cùng một cơ chế

**Ghi cả hai vào đặc tả** vì cơ chế lặp lại mới là thứ đáng giữ, không phải hai con số.

**(1) Lượt 3 bắt:** `20641d5` khai *"1715/1715, không ca nào FAIL/BỎ QUA"*. Sai. Cơ chế:
`grep "[BO QUA]"` ra **0 dòng** ⇒ khai *"không ca nào bỏ qua"*. Harness **không in gì** cho ca
bỏ qua — chúng vẫn in `[OK]`. Thật: **2 toàn bộ + 2 một phần**.

**(2) Lượt 4 bắt:** `efaf576`, trong **chính đoạn rút lời khai (1)**, khai thêm *"`_t110` được
gọi 711 lần với 710 TÊN phân biệt — `r210_loop_khong_ghi_trong_cay` đăng ký HAI lần"*. **Cũng
sai.** Đo lại bằng `ast`:

```
AST   : 708 lời gọi · 707 đối số là HẰNG CHUỖI · 707 tên PHÂN BIỆT · 0 trùng
        + 1 lời gọi đối số KHÔNG phải hằng (dòng 30129, `fragment.test_id`)
REGEX : 711 khớp · 710 phân biệt · "trùng" r210_loop_khong_ghi_trong_cay ×2
```

Cái "trùng" ấy là **một chuỗi fixture** ở dòng 30199 — văn bản NẰM TRONG một fixture, không phải
một lời gọi. Runtime đúng **711/711**.

**Cơ chế GIỐNG HỆT nhau**: cả hai lần đo bằng một **MẪU VĂN BẢN** rồi khai thành một **SỰ KIỆN
CẤU TRÚC**. Và lần hai nằm trong chính đoạn sửa lần một — sửa một lời khai sai bằng một lời khai
sai cùng lớp. Đó là lý do `LOI-KHAI-RONG-HON-PHEP-DO` ở §6 nhảy 7 → 9.

**Chốt rút ra, và nó rẻ:** hỏi một câu về CẤU TRÚC (*"có bao nhiêu lời gọi"*, *"ca nào bị bỏ
qua"*) thì phải đo bằng công cụ hiểu cấu trúc — `ast`, hoặc runtime. `grep`/regex trả lời một câu
KHÁC: *"có bao nhiêu chỗ TRÔNG GIỐNG"*. Hai câu ấy trùng nhau đủ thường để ru ngủ, và lệch nhau
đúng lúc có một fixture chứa mã.

### 8.3 — Điều r2 KHÔNG khai

- **Không** khai ma trận đóng được `m12` nào đó chưa ai nghĩ ra. Nó phủ ba trục ĐÃ BIẾT; một
  trục thứ tư chưa ai nêu vẫn có thể tồn tại. `A11` đòi mỗi đột biến lịch sử làm một ô KHÁC
  nhau đỏ — đó là bằng chứng ba trục độc lập, **không** phải bằng chứng đủ trục.
- **Không** khai `cross_approved`. Bốn lượt review máy không cấp được `human_audited`, và
  verdict của chúng tự nói đúng điều đó.
- **Không** khai lượt Windows nào đã chạy.

### 8.4 — Ma trận ĐÃ ĐO: bốn đột biến, bốn Ô KHÁC NHAU

Nền và cả bốn đột biến chạy **TUẦN TỰ** trên bản sao rời, mỗi lượt là một `tl.py --selftest`
TOÀN BỘ:

| | ô đỏ ĐẦU TIÊN | `expected` | `observed` | `oracle_calls` |
|---|---|---|---|---|
| **nền** | — | — | `1715/1715`, `rc=0` | — |
| `m7` `except _R378SaiKyVong`→`except RuntimeError` | `lop=thuong,td=goc` | `false_credit:RuntimeError` | `killed` | 1 |
| `m9` `return "survived"`→`return "killed"` | `oracle=thoa` | `survived` | `killed` | 1 |
| `m10` bắt mọi `Exception`, so CHUỖI | `lop=that,td=khac` | `killed` | `false_credit:_R378SaiKyVong` | 1 |
| `m11` so `type(exc).__name__` | `lop=lopcon,td=goc` | `killed` | `false_credit:_LopCon` | 1 |

Mỗi đột biến `1714/1715`, `rc=1`, và ca đỏ **duy nhất** là `r378_ma_tran_phan_hang`.

**BỐN Ô KHÁC NHAU ⇒ ba trục ĐỘC LẬP, không phải một bộ tương đương.** Đó là điều `A11` đòi, và
nó là thứ bốn vế rời của r1 KHÔNG chứng minh được: bốn vế ấy chỉ là bốn điểm, và `m11` đi qua
được cả bốn.

Đọc từng ô cho thấy mỗi đột biến chết theo một CHIỀU khác nhau, chứ không phải bốn cách viết của
cùng một chiều:

- `m7` chết ở trục **LỚP** phía *"bắt quá rộng"* — một `RuntimeError` TRẦN được cấp `killed`.
- `m10` chết ở trục **THÔNG ĐIỆP** — một `_R378SaiKyVong` THẬT với thông điệp KHÁC bị từ chối.
- `m11` chết ở trục **LỚP** phía *"nhận diện bằng tên"* — một lớp CON thật bị từ chối.
- `m9` chết ở trục **ORACLE** — oracle thoả mà vẫn khai `killed`.

**KHAI CHO ĐÚNG, ba giới hạn:**

1. **Ca DỪNG ở ô hỏng ĐẦU TIÊN**, nên cột trên là *"ô đỏ đầu tiên"*, KHÔNG phải *"ô đỏ duy
   nhất"*. `m11` chẳng hạn cũng phải làm ô `lop=trungten` đỏ, nhưng `lopcon` đứng trước trong
   vòng lặp. Muốn biết TẬP ô đỏ đầy đủ của từng đột biến thì phải sửa ca thành thu thập thay vì
   ném ngay — r2 **không** làm việc đó, và khai ra đây thay vì để người đọc suy.
2. **Bốn ô khác nhau chứng minh ba trục ĐÃ BIẾT là độc lập.** Nó **không** chứng minh không còn
   trục thứ tư. Một `m12` theo một chiều chưa ai nêu vẫn có thể tồn tại — xem §8.3.
3. **Windows thật vẫn KHÔNG ĐO ĐƯỢC.** Cả năm lượt trên đều là Linux.

### 8.5 — Chạy SONG SONG bốn lượt selftest làm HAI lượt chết vì lý do vô can

Lần đo đầu chạy bốn `tl.py --selftest` **song song**. `m7`/`m9` xong bình thường; `m10` chết
`KeyError: 'rootFolderId'`, `m11` chết `json.decoder.JSONDecodeError: Expecting value: line 1
column 1` — **không ca nào của `r378` liên quan**. Chạy lại TUẦN TỰ ⇒ cả bốn cho kết quả sạch ở
bảng trên.

Ghi vào đặc tả vì nó đúng lớp `RIG-QUYET-MAU-CUA-PHEP-DO` mà §6 đang đếm, và vì nó suýt thành
một kết luận sai: *"m10/m11 làm suite vỡ"* nghe như một finding, trong khi sự thật là **bộ
selftest dùng chung trạng thái trên đĩa nên không chạy song song được**. Ai đo đột biến trên
`scripts/tl_selftest.py` phải chạy tuần tự.
