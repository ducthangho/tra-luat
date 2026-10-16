# ĐẶC TẢ — `R378-SYMLINK-DOI-DAC-QUYEN` — **revision 1, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `packet_id` | `R378-SYMLINK-DOI-DAC-QUYEN` |
| `revision` | 1 |
| `packet_issue` | **#574** |
| `nguon_cap_viec` | Nợ #574, mở theo chỉ thị chủ kho 20-09-2026 (*"Land xong thì mở nợ r378"*). Chỉ thị cấp lease: *"Cấp lease cho r378 đi"*, cùng phiên ~16:2xZ. |
| `review_class` | **`sensitive`** — chạm `scripts/tl_selftest.py`, harness dùng chung, và ca đích đo một **chốt an ninh**. Cùng lớp mà #565 đã dùng cho chính tệp này. |
| `assurance_target` | **`human_audited`** — `cross_approved` **KHÔNG ĐẠT ĐƯỢC**, không phải *"chưa đo"*: codex đăng *"You have reached your Codex usage limits for code reviews"* trên PR #577 lúc 10:52Z 20-09; agy hết quota; claude là executor. |
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
| **A6** | Ca chết vì môi trường **không** được phân hạng là GIẾT. | Ca tiêm cho `_r378_classify`: mutant chết vì `JUNCTION_CREATE_FAILED` phải rơi vào **tín dụng giả**, không phải `giet_that`. Phân hạng bằng **LỚP ngoại lệ riêng + TÊN CA**, không bằng chuỗi thông điệp — bài học #355/#359: một `except` đổi kiểu giả được chuỗi. |
| **A7** | `tl.py --selftest` **DELTA so `origin/master` = 0** trên POSIX, và `r378_l7_resolve_phai_o_trong_kho` ở tập ĐẠT của cả hai vế. | **Đo hai vế trong MỘT lệnh**, cùng các bước, chạy liền nhau. So **TẬP TÊN** ca đỏ, không so số đếm — *"mất một ca đỏ cũ, thêm một ca đỏ mới, tổng không đổi"* là ca mà phép đếm không bắt được. Nền đo 20-09 trên Linux: **1711/1711**; **đo lại trước khi tin** (L5). |
| **A8** | `release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true` **và** `expected == checked`. | Chạy **tại chỗ, đúng lệnh của lane LAND**. Lane PR **KHÔNG** bắt được lệch manifest (`if: github.ref == 'refs/heads/master'`; lane WORKER sinh manifest tạm nên hấp thụ mọi thay đổi nội dung) ⇒ PR xanh, master ĐỎ. |
| **A9** | `numstat` chạm **đúng hai** đường của `write_set`. | Đột biến thêm đường thứ ba ⇒ ĐỎ. Chốt write-set exclusion §5. |
| **A10** | `doctrine-scan` · `adr-song` · `doc-claims-check --strict` · `git diff --check` `rc=0`, `core.abbrev = 7`. | `rc` đọc **trực tiếp**, không qua pipe (nợ `RC-QUA-PIPE-KHONG-CO-CHOT`). |

## 6. `hinh_dang_ke_thua` (L4) — chép từ #565

| hình dạng | số lần | nguồn |
|---|---|---|
| `RIG-QUYET-MAU-CUA-PHEP-DO` | **5** | Chép từ #565 (4 ca `CLAUDE.md` 24-08 + `Đ1`). **Packet này chạm đúng lớp ấy**: một ca đỏ vì RIG (thiếu đặc quyền), không vì mã. |
| `NGOAI-LE-BI-NUOT-LANG` | **2** | Chép từ #565. Ca r378 từng đỏ **câm** trước khi `Đ2` land — chính nó là ca thứ hai. |
| `LOI-KHAI-RONG-HON-PHEP-DO` | 6 → **7** | Chép 6 từ biên nhận #565. **+1**: câu *"KHÔNG PORT THẲNG ĐƯỢC … giả thuyết, chưa chạy"* của #574 **hẹp hơn** phép đo — mẫu ấy đã có sẵn và đã chạy trong cùng tệp. Lời khai lệch phép đo **theo chiều hẹp** cũng là lệch. |

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
4. **Số dòng thêm** — ước **+40…+90**. Trần `sensitive` là **300**. Vượt ⇒ DỪNG và xin, không tự
   làm tròn, và **không** viết vào thân PR rằng cổng `ADR-0044` "ĐẠT".
5. **Số ca của suite** — nền đo **1711/1711** trên Linux ngày 20-09. Con số ấy **sẽ trôi**; đo lại
   ở cả hai vế trước khi kết luận, đừng chép.
