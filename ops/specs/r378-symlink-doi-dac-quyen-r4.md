# ĐẶC TẢ — `R378-SYMLINK-DOI-DAC-QUYEN` — **revision 4, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `packet_id` | `R378-SYMLINK-DOI-DAC-QUYEN` |
| `revision` | **4** |
| `thay_the_cho` | revision 3, `e433d35c3dbdaa13a0ec4e6f5deafac6d66b0c88f5bb977cda6ed25b90b27658` |
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

### 0.2 — Vì sao có revision 3

Cross-review `codex` **lượt 5** — lượt ĐẦU chạy theo **trục LỚP** — phán
`phan-hang-giet-gia-thieu-doi-chung` là **`VÁ SINH LỖI MỚI`**, lần thứ **NĂM** cùng slug. Hai
chuyện từ reviewer, và chúng KHÁC NHAU — cộng một chuyện **thứ ba** mà phiên điều phối tự đo
được khi đi thi hành chính `A11` mới (xem cuối mục này và §8.5):

**(a) MẤT PHỦ `m3` — hồi quy do CHÍNH r2 gây ra.** Bốn vế rời của r1 có đối chứng
`AssertionError`. Ma trận của r2 thay **TRỌN** chúng và đánh rơi trục đó: `r1/m3` ⇒ `False`
(bắt được), `r2/m3` ⇒ `1715/1715` (SỐNG). r2 viết *"thay bốn vế rời"* mà **không kiểm bộ hồi quy
cũ còn bị bắt không**. Reviewer đặt tên cho lớp ấy — `L7 KHONG-THOAI-LUI-HO-DOT-BIEN-KHI-DOI-CA`
— và nó phát biểu một thứ mọi refactor bộ test đều phải chịu: **mọi mutant lịch sử đã bị bắt
trước refactor phải tiếp tục bị bắt.**

**(b) NHÃN RỘNG HƠN TẬP FIXTURE.** `LOP` của r2 lấy **MỘT đại diện** cho mỗi nhãn:
`RuntimeError` là toàn bộ lớp "thường"; lớp con duy nhất dựng **cùng module**; mọi ngoại lệ tạo
bằng **một đối số chuỗi**. Ba cài đặt sai **nằm ngay trong các trục r2 đã khai** vẫn qua cả 14 ô:
`m12` (tuple/`ValueError`) lọt ở `LỚP=thường`, `m13` (giới hạn theo module) lọt ở `LỚP=con`,
`m14` (theo `args`) lọt ở thông điệp rỗng.

**Tức lời khai của r2 RỘNG HƠN phép đo**, và đây là chỗ đáng nhớ nhất của cả năm lượt: ma trận
CÓ trục, nhưng **mỗi trục chỉ có MỘT ĐIỂM**, nên nó vẫn là 14 điểm được sắp thành bảng. Nó không
thoát khỏi cái bẫy nó sinh ra để thoát — nó chỉ đổi hình dạng của cái bẫy.

| finding | r2 sai ở đâu | r3 sửa ở |
|---|---|---|
| `phan-hang-giet-gia-thieu-doi-chung` (a) | `A11` không đòi bộ hồi quy còn bị bắt | `A11` |
| `phan-hang-giet-gia-thieu-doi-chung` (b) | mỗi nhãn một đại diện; câu khai "bất kỳ chiều nào" | `A6`, §8.3 |
| **(c) — không reviewer nào nêu; phiên điều phối TỰ ĐO khi thi hành chính `A11`** | ma trận r2 không phân biệt nổi `m10` (so bằng CHUỖI) với `m14` (so bằng `args`): **cùng 27 ô, CÙNG một tập 27 toạ độ** ⇒ một BỘ TƯƠNG ĐƯƠNG. Trục `DOI_SO` phủ SỐ LƯỢNG đối số mà không phủ NỘI DUNG. | `A6` (dạng thứ bảy `moc_kem_doi_so_2`), §8.5 |

### 0.3 — Vì sao có revision 4

**MỘT lý do, và nó không phải một finding: chủ kho đổi ĐIỀU KIỆN DỪNG.**

Chỉ thị 21-09-2026, bản chiếu `issues/574#issuecomment-5765691395` (bản đầy đủ ở
`issues/579#issuecomment-5765688081`):

> *"Chuyển điều kiện dừng là tới khi không còn findings P1, P2, P3"*

`dieu_kien_dung` là **acceptance**, và §3.2 nói thẳng: *"Đổi objective, acceptance, write set,
dependency, executor hoặc environment tạo revision mới và làm lease cũ mất hiệu lực."* Không có
đường nào cho một chỉ thị như thế vào mà không qua revision. Lease `r378-symlink-doi-dac-quyen-
r3-g2-claude` neo r3 ⇒ mất hiệu lực theo đúng câu ấy.

**Phần kỹ thuật của r3 KHÔNG đổi một chữ.** `A6` (ma trận theo HỌ, 79 ô), `A11` (đòi bộ hồi quy,
so bằng TẬP), §8.4–§8.7 đều giữ nguyên. r4 thêm **§9 — điều kiện dừng**, và chỉ thế.

**Nói thẳng một điều r4 KHÔNG có:** packet này **chưa có lượt cross-review nào** dưới luật mới.
Điều kiện dừng mới đòi một lượt cho `0` finding P1/P2/P3, và tính tới lúc đóng băng r4 con số ấy
là **KHÔNG ĐO ĐƯỢC** — chưa lượt nào chạy trên head `ce9de50`. Đó không phải một khoảng trống
được tha; nó là việc còn lại.

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
| **A6** (VIẾT LẠI ở **r3** — ma trận theo **HỌ**; r2 là ma trận theo **ĐẠI DIỆN**) | `_r378_classify` phải đúng trên một ma trận mà **mỗi nhãn mang một HỌ thành viên**, không một đại diện. Trục **LỚP**, 11 thành viên: lớp THẬT · con CÙNG module · con **KHÁC module** · **ĐA KẾ THỪA** · `RuntimeError` · **`AssertionError`** · **`ValueError`** · `TypeError` · `KeyError` · **TRÙNG TÊN** khác `id()` · **TRÙNG TÊN và là lớp con của `ValueError`**. Trục **DẠNG ĐỐI SỐ**, 6 dạng: không đối số · chuỗi rỗng · thông điệp gốc · thông điệp khác · hai đối số · `None`. Trục **ORACLE**: chạy-và-ném (khối A, 11×6 = **66** ô) · chạy-và-thoả (khối B) · khâu DỰNG hỏng (khối C). Tổng **68** ô. Ca **THU TẬP ĐẦY ĐỦ** tập ô đỏ rồi mới ném một lần, KHÔNG dừng ở ô hỏng đầu tiên — `A11` đòi so TẬP ô, dừng sớm thì không so được. Khối B và C chốt thêm **SỐ LẦN GỌI** oracle (đúng 1 · đúng 0); r2 chỉ chốt kết quả, nên một cài đặt gọi oracle hai lần vẫn cho `survived` mà không ô nào đỏ. | Mỗi ô có `expected` là **DỮ LIỆU** — suy từ cờ `bat_duoc` VIẾT TAY và `lop.__name__`, KHÔNG từ chính `_r378_classify`. Bảng fixture có **chốt tự kiểm**: `bat_duoc` phải khớp `issubclass`; hai lớp `trung_ten*` phải thật sự trùng `__name__`; lớp `con_khac_module` phải thật sự khác `__module__` — trôi cái nào thì ném `R378_MA_TRAN_FIXTURE_TROI`. **Phép đo làm A6 ĐỎ:** rút một họ về một đại diện (bỏ `AssertionError` khỏi lớp thường, bỏ `con_khac_module`, bỏ dạng `khong_doi_so`) phải làm `m3`/`m13`/`m14` SỐNG LẠI — đó là phản chứng cho chính hình dạng HỌ. **GIỮ NGUYÊN ngữ nghĩa `except` của Python**: lớp CON vẫn là `killed`; ma trận ĐO bộ phân hạng, nó KHÔNG tự quyết đổi sang so kiểu chính xác. |
| **A11** (VIẾT LẠI ở **r3** — nay **ĐÒI** bộ hồi quy, r2 chỉ đòi bốn đột biến đương thời) | Ma trận phải bắt **TOÀN BỘ bộ hồi quy lịch sử** `m1`–`m14`, và **ô đỏ của mỗi cái là một phép ĐO, không phải một dự đoán**. Đây là chỗ r2 sập: r2 thay TRỌN bốn vế rời của r1 mà **không kiểm bộ cũ còn bị bắt không** ⇒ `m3` sống lại (`r1/m3` ⇒ `False`, `r2/m3` ⇒ `1715/1715`). Reviewer lượt 5 đặt tên lớp ấy: **`L7 KHONG-THOAI-LUI-HO-DOT-BIEN-KHI-DOI-CA`** — *mọi mutant lịch sử đã bị bắt trước refactor phải tiếp tục bị bắt.* Từ r3, **đổi hình dạng ca là phải chạy lại CẢ bộ**, không chỉ các đột biến của lượt hiện tại. | Chạy TOÀN suite, **TUẦN TỰ** (§8.7 — song song làm hai lượt chết vì lý do vô can), mỗi đột biến một lượt `tl.py --selftest` đầy đủ; ghi lại **TẬP ô đỏ** kèm `expected`/`observed`/`oracle_calls`. **So bằng TẬP, KHÔNG bằng SỐ ĐẾM**, và đây KHÔNG phải một lo xa: đo thật ở §8.5, với sáu dạng đối số của r2, `m10` và `m14` cùng cho **27** ô đỏ **VÀ CÙNG MỘT TẬP 27 toạ độ, hai chiều rỗng** — một bộ TƯƠNG ĐƯƠNG mà phép đếm không thể thấy. Hai đột biến có TẬP ô đỏ bằng nhau thì ma trận đang đo ÍT trục hơn nó khai; điều đó phải được **KHAI**, hoặc **ĐÓNG** bằng một thành viên mới tách được chúng — r3 chọn đóng, bằng dạng đối số thứ bảy `moc_kem_doi_so_2`. **Và tiêu chí phải nói ĐƯỜNG ĐỌC**: một lượt `--selftest` thường chỉ cho SỐ ĐẾM (harness cắt chẩn đoán ở 400 ký tự, §8.3), nên TẬP ô phải đọc từ một bản sao RIG đã nới `_TRAN_CHAN_DOAN_110`. Đọc TẬP từ lượt chạy thường là đọc **năm** toạ độ đầu rồi tưởng đã có cả tập. **Tiêu chí này KHÔNG ghi trước ô nào ứng với đột biến nào**: bản nháp r2 từng ghi *"`m7` ⇒ ô `LỚP=that`"* và phép đo BÁC ngay — `_R378SaiKyVong` kế thừa `RuntimeError`, nên `except RuntimeError` của `m7` vẫn bắt được nó; ô đỏ thật là `lop=thuong_runtime`. Một tiêu chí nghiệm thu ghi sẵn ô đích là một tiêu chí có thể SAI trước khi ai chạy nó. |
| **A7** | `tl.py --selftest` **DELTA so `origin/master` = 0** trên POSIX, và `r378_l7_resolve_phai_o_trong_kho` ở tập ĐẠT của cả hai vế. | **Đo hai vế trong MỘT lệnh**, cùng các bước, chạy liền nhau. So **TẬP TÊN** ca đỏ, không so số đếm — *"mất một ca đỏ cũ, thêm một ca đỏ mới, tổng không đổi"* là ca mà phép đếm không bắt được. Nền đo 20-09 trên Linux: **1711/1711**; **đo lại trước khi tin** (L5). |
| **A8** | `release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true` **và** `expected == checked`. | Chạy **tại chỗ, đúng lệnh của lane LAND**. Lane PR **KHÔNG** bắt được lệch manifest (`if: github.ref == 'refs/heads/master'`; lane WORKER sinh manifest tạm nên hấp thụ mọi thay đổi nội dung) ⇒ PR xanh, master ĐỎ. |
| **A9** | `numstat` chạm **đúng hai** đường của `write_set`. | Đột biến thêm đường thứ ba ⇒ ĐỎ. Chốt write-set exclusion §5. |
| **A10** | `doctrine-scan` · `adr-song` · `doc-claims-check --strict` · `git diff --check` `rc=0`, `core.abbrev = 7`. | `rc` đọc **trực tiếp**, không qua pipe (nợ `RC-QUA-PIPE-KHONG-CO-CHOT`). |

## 6. `hinh_dang_ke_thua` (L4) — chép từ #565

| hình dạng | số lần | nguồn |
|---|---|---|
| `RIG-QUYET-MAU-CUA-PHEP-DO` | **5** | Chép từ #565 (4 ca `CLAUDE.md` 24-08 + `Đ1`). **Packet này chạm đúng lớp ấy**: một ca đỏ vì RIG (thiếu đặc quyền), không vì mã. |
| `NGOAI-LE-BI-NUOT-LANG` | **2** | Chép từ #565. Ca r378 từng đỏ **câm** trước khi `Đ2` land — chính nó là ca thứ hai. |
| `LOI-KHAI-RONG-HON-PHEP-DO` | 7 → **10** | Chép 6 từ biên nhận #565. **+1**: câu *"KHÔNG PORT THẲNG ĐƯỢC … giả thuyết, chưa chạy"* của #574 **hẹp hơn** phép đo — mẫu ấy đã có sẵn và đã chạy trong cùng tệp. Lời khai lệch phép đo **theo chiều hẹp** cũng là lệch. **+1 ở r3**: câu của r2 *"một cài đặt sai theo BẤT KỲ CHIỀU NÀO phải làm ít nhất một ô đỏ"* — **rộng hơn**, và lượt 5 bác bằng ba phản chứng nằm ngay trong các trục r2 đã khai (§8.3). |
| `KHONG-THOAI-LUI-HO-DOT-BIEN-KHI-DOI-CA` (**L7**, lớp MỚI, reviewer lượt 5 đặt tên) | **1** | Lần đầu đo được ở chính packet này: r2 thay TRỌN bốn vế rời của r1 bằng ma trận và đánh rơi đối chứng `AssertionError` ⇒ `m3` sống lại. Chốt: **mọi mutant lịch sử đã bị bắt trước refactor phải tiếp tục bị bắt** — nay là `A11`. |

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
4. **Số dòng thêm** — r1 ước **+40…+90**; **ước ấy đã sai**, và nó đã trôi tiếp HAI lần: đo ở
   `efaf576` là **+246/−6**, ở `ce9de50` (head của r3) là **+336/−6** cho `scripts/tl_selftest.py`,
   cộng `5/5` cho manifest ở cả hai. Reviewer lượt 4 xác nhận và ghi rõ đó
   là một ƯỚC bị trôi, không phải một phép đo bị sai. Trần `sensitive` là **300**; chủ kho đã
   nới trần DÒNG cho đợt 21-09-2026 lên **3000** (xem `ops/specs/dang-lease-dau-truoc-kiem-sau-r5.md`
   §8 — cùng chỉ thị, cùng đợt). **Đo lại ở head cuối, đừng chép con số này.**
5. **Số ca của suite** — nền `714f36e` đo **1711/1711** trên Linux ngày 20-09; head `efaf576` đo
   **1715/1715**; head `ce9de50` của r3 cũng **1715/1715** (ma trận vẫn là MỘT ca, mở rộng trục
   không thêm ca). Con số ấy **sẽ trôi**; đo lại ở cả hai vế trước khi kết luận, đừng chép.
   **ĐIỀU KIỆN ĐO, không được bỏ:** rig phải là `git clone` có `.git` THẬT và `core.abbrev = 7` —
   `git archive` làm SÁU ca vô can đỏ và cho `1708/1715` (§8.7).
6. **Bốn ca BỎ QUA NGẦM mà vẫn in `[OK]`** — 2 toàn bộ + 2 một phần, reviewer lượt 3 đo và lượt
   4 xác nhận. Bốn hàm ấy **không đổi so base** ⇒ nợ KẾ THỪA, ngoài `write_set`. Hệ quả phải
   nhớ, và nó đã làm packet này khai sai một lần: **`[FAIL]=0` KHÔNG hàm ý "bỏ qua = 0"**, vì
   harness không in gì cho ca bỏ qua.
7. **Toàn suite có `1714` tên phân biệt** vì `r3_bust_cache_after_write` xuất hiện HAI lần — một
   trùng THẬT, có từ trước packet này, ở chỗ khác. Reviewer lượt 4 đo. Chưa ai truy nó.
8. **Windows thật** — vẫn **KHÔNG ĐO ĐƯỢC**. Năm lượt cross-review đều chạy trên Linux.
9. **Còn trục thứ tư của ma trận hay không** — **KHÔNG ĐO ĐƯỢC**, và không thể đo được bằng cách
   nào hiện có. 79 ô phủ ba trục ĐÃ BIẾT; §8.3 nói thẳng rằng mỗi lượt review từ lượt 2 tới lượt
   5 đều nêu một chiều mà lượt trước không nêu, nên tiên nghiệm là **còn**. Điều r3 khai được chỉ
   là: các chiều đã biết nay phân biệt được đôi một (§8.4, 28 cặp).
10. **Bộ trích toạ độ** là một script nháp của phiên điều phối, không có cổng, không có ca test —
    và nó **đã sai một lần** (§8.6). Nó nay đối chiếu với số ca tự khai, nhưng đó là một chốt
    chứ không phải một phép chứng minh.

## 8. NĂM lượt cross-review — và r3 là hệ quả của lượt 5

| lượt | `reviewed_sha` | verdict | finding | đột biến sống sót |
|---|---|---|---|---|
| 1 | — | `changes_requested` | `m5` | mất phủ CỦA CHỈ MỤC |
| 2 | — | `changes_requested` | `phan-hang-giet-gia-thieu-doi-chung` | `m7`, `m9` |
| 3 | `20641d5` | `changes_requested` | cùng slug, ĐỔI HÌNH DẠNG | `m10` |
| 4 | `efaf576` | `changes_requested` | cùng slug, **VÁ HỜ** | **`m11`** |
| 5 (trục **LỚP**) | `efaf576` | `changes_requested` | cùng slug, **`VÁ SINH LỖI MỚI`** — (a) mất phủ `m3` do chính r2 gây ra · (b) nhãn rộng hơn tập fixture | **`m12`, `m13`, `m14`** (và `m3` sống lại) |

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
sai cùng lớp. Đó là lý do `LOI-KHAI-RONG-HON-PHEP-DO` ở §6 nhảy 7 → 9 (và r3 đẩy tiếp lên 10, xem §8.3).

**Chốt rút ra, và nó rẻ:** hỏi một câu về CẤU TRÚC (*"có bao nhiêu lời gọi"*, *"ca nào bị bỏ
qua"*) thì phải đo bằng công cụ hiểu cấu trúc — `ast`, hoặc runtime. `grep`/regex trả lời một câu
KHÁC: *"có bao nhiêu chỗ TRÔNG GIỐNG"*. Hai câu ấy trùng nhau đủ thường để ru ngủ, và lệch nhau
đúng lúc có một fixture chứa mã.

### 8.3 — Điều r3 KHÔNG khai — và câu khai QUÁ RỘNG của r2, thu hẹp lại

**r2 khai:** *"một cài đặt sai theo bất kỳ chiều nào phải làm ít nhất một ô đỏ"*. Câu ấy **RỘNG
HƠN phép đo**, và lượt 5 bác nó bằng ba phản chứng nằm NGAY TRONG các trục r2 đã khai (`m12`,
`m13`, `m14`). Đây là lần thứ **mười** của lớp `LOI-KHAI-RONG-HON-PHEP-DO` trong sổ §6 — và lần
này nạn nhân là chính câu viết ra để tổng kết một bộ đo.

**r3 khai lại, hẹp đúng bằng phép đo:** ma trận bảo đảm cho **MIỀN ĐÃ LIỆT KÊ** — 11 lớp × 7
dạng đối số × 3 trạng thái oracle, tức **79 ô** — và **không** cho *"mọi cài đặt sai có thể viết
bằng Python"*. Ba điều còn lại, khai thẳng:

- **Không** khai ma trận đóng được một `m17` theo chiều chưa ai nêu. `A11` đòi bằng chứng cho các
  chiều **ĐÃ BIẾT**; nó không đòi — và không thể cấp — bằng chứng phủ định về chiều chưa biết.
  Bằng chứng ngược chiều đã có thật: mỗi lượt cross-review từ lượt 2 tới lượt 5 đều tìm ra một
  chiều mà lượt trước không nêu.
- **Không** khai `cross_approved`. Năm lượt review máy không cấp được `human_audited`, và verdict
  của chúng tự nói đúng điều đó.
- **Không** khai lượt Windows nào đã chạy.

Và một giới hạn về ĐƯỜNG ĐỌC, mới ở r3 vì chính r3 đụng phải: **một lượt `tl.py --selftest`
THƯỜNG KHÔNG đọc được TẬP ô đỏ.** Harness cắt thân chẩn đoán ở `_TRAN_CHAN_DOAN_110 = 400` ký tự
(`scripts/tl_selftest.py:9114`), nên thứ một lượt chạy thường cho ra là **SỐ ĐẾM** cộng vài toạ
độ đầu. Đo thật: cùng một lượt `m10` (ma trận r2, ca tự khai `27/68`), bản cắt ở 400 ký tự đọc ra được
**5** toạ độ; bản nới trần trong bản sao RIG đọc ra **27** — tức đủ, và khớp con số ca tự khai. `A11` đòi so TẬP, nên nó phải nói rõ đường đọc — xem chính `A11`. Trần ấy **KHÔNG**
đổi trong `write_set`; nới nó là việc của RIG.

### 8.4 — Ma trận ĐÃ ĐO ở r3: TÁM đột biến, TÁM TẬP ô đỏ PHÂN BIỆT

Nền và cả tám đột biến chạy **TUẦN TỰ**, mỗi lượt một `tl.py --selftest` TOÀN BỘ trên một
`git clone` riêng (rig phải có `.git` THẬT — xem §8.7). Trần chẩn đoán nới trong bản sao RIG để
đọc được TẬP ô; `write_set` **không** đổi trần ấy.

| | ô đỏ | toạ độ phân biệt | ca đỏ |
|---|---:|---:|---|
| **nền** | — | — | **1715/1715**, `rc=0`, không ca nào đỏ |
| `m3` `except _R378SaiKyVong` → `except (…, AssertionError)` | **7**/79 | 7 | chỉ `r378_ma_tran_phan_hang` |
| `m7` → `except RuntimeError` | **8**/79 | 8 | nt |
| `m9` `return "survived"` → `return "killed"` | **1**/79 | 1 | nt |
| `m10` bắt mọi `Exception`, so **CHUỖI** | **34**/79 | 34 | nt |
| `m11` so `type(exc).__name__` | **35**/79 | 35 | nt |
| `m12` → `except (…, ValueError)` | **14**/79 | 14 | nt |
| `m13` giới hạn lớp con theo **module** | **7**/79 | 7 | nt |
| `m14` phân hạng theo **`args`** | **31**/79 | 31 | nt |

Cả tám: `1714/1715`, `rc=1`, và ca đỏ **DUY NHẤT** là `r378_ma_tran_phan_hang`. Mỗi ô đỏ là một
toạ độ riêng — không ô nào sinh hai mục, nên "số ô" và "số toạ độ" trùng nhau ở mọi lượt.

**So TẬP đôi một, đủ 28 cặp: KHÔNG cặp nào trùng.** Đó là thứ `A11` đòi, và nó mạnh hơn hẳn bảng
bốn ô của r2 — ở đó bằng chứng chỉ là "bốn ô ĐẦU TIÊN khác nhau", vì ca dừng ngay ô hỏng đầu.

Hai tập đọc kỹ cho thấy ma trận đang đo TRỤC chứ không đo điểm:

- `m3` đỏ **đúng 7 ô**, tất cả ở `lop=thuong_assert`, trải hết **cả 7 dạng đối số** — một lát cắt
  SẠCH theo trục LỚP. Đây chính là phủ mà r2 đánh rơi.
- `m13` cũng đỏ **đúng 7 ô**, tất cả ở `lop=con_khac_module`, cũng trải hết 7 dạng. Cùng lực
  lượng, **tập khác hẳn** — minh hoạ sống cho luật "so TẬP, đừng so SỐ ĐẾM".

### 8.5 — `m10` và `m14` là một BỘ TƯƠNG ĐƯƠNG dưới ma trận r2 — và không ai phát hiện ra

Đây là phát hiện đắt nhất của r3, và **không reviewer nào nêu**: nó lộ ra vì `A11` đòi so TẬP.

Đo trên ma trận **r2** (6 dạng đối số, 68 ô), hai lượt `--selftest` riêng:

```
m10  27/68 ô đỏ · 27 toạ độ
m14  27/68 ô đỏ · 27 toạ độ
comm -23 = 0 · comm -13 = 0 · chung = 27      <- HAI TẬP BẰNG NHAU
```

`m10` phân hạng bằng **chuỗi** (`"R378_EXPECTATION_MISMATCH" in str(exc)`), `m14` bằng **`args`**
(`exc.args == ("R378_EXPECTATION_MISMATCH",)`). Hai cài đặt sai khác hẳn nhau về cơ chế, mà ma
trận r2 **không phân biệt nổi** — nó đang đo ÍT trục hơn nó khai, đúng một tầng nữa của cùng bệnh
mà r2 sinh ra để chữa.

**Chỗ tách chúng, và vì sao trục cũ không có:** một ngoại lệ mang mốc đúng **KÈM đối số thứ hai**.
`str()` của nó là `('R378_EXPECTATION_MISMATCH', 'x')` — **CHỨA** mốc, nên `m10` cấp `killed`;
`args` thì **KHÁC** tuple một phần tử, nên `m14` cấp tín dụng giả. Trục `DOI_SO` của r2 có
`hai_doi_so` (`("a","b")`) nhưng **không** có dạng *"hai đối số trong đó cái đầu là mốc đúng"* —
nó phủ SỐ LƯỢNG đối số mà không phủ **NỘI DUNG** đối số.

r3 thêm dạng thứ bảy `moc_kem_doi_so_2`. Đo lại trên 79 ô:

```
chỉ m10: 7 ô   — lop=thuong_{assert,key,runtime,type,value} · trung_ten · trung_ten_con
chỉ m14: 4 ô   — lop=that · con_cung_module · con_khac_module · da_ke_thua
```

**Cả 11 ô lệch đều nằm trên `ds=moc_kem_doi_so_2`** — đúng thành viên thêm vào để tách chúng, và
không ô nào khác. Đó là phản chứng cho chính hình dạng HỌ: rút dạng ấy ra thì bộ tương đương
quay lại.

### 8.6 — Phép đo TẬP của chính r3 SAI một lần, và nó sai đúng lớp §8.2

Lượt trích toạ độ đầu tiên dùng `grep -o '\[lop=[a-z_0-9]*,ds=[a-z_0-9]*\]'`. Mẫu ấy có **chữ
thường**, mà một dạng đối số tên là `doi_so_None` — **chữ N hoa**. Kết quả: mọi tập bị rụng lặng
lẽ các ô `ds=doi_so_None`, và bảng đầu tiên cho `m3` = `7 mục / 6 toạ độ` — một chênh lệch không
có thật, mà tôi suýt ghi vào đặc tả kèm một lời giải thích bịa ra cho nó.

**Cùng cơ chế với cả hai lời khai sai ở §8.2:** đo bằng một **MẪU VĂN BẢN** rồi khai thành một
**SỰ KIỆN CẤU TRÚC**. Lần này nạn nhân là phép đo viết ra để cưỡng chế `A11` — tức chính cái
chốt dựng lên để chống bị lừa.

Chốt: bộ trích toạ độ phải **ĐỐI CHIẾU** số mục nó trích được với số mục ca tự khai
(`R378_MA_TRAN_O_SAI (N/79 ô)`). Lệch ⇒ bộ trích sai, không phải dữ liệu sai. Bảng §8.4 in cả hai
cột đúng vì lý do đó, và cả tám lượt nay khớp `entries_khai == entries_trích`.

**Kết luận "không cặp nào trùng" KHÔNG bị lung lay** bởi lỗi này — bỏ sót ô chỉ có thể làm hai tập
trông GIỐNG nhau hơn, không thể làm chúng trông KHÁC nhau hơn — nhưng các con số thì có, và chúng
đã được đo lại toàn bộ bằng bộ trích đã sửa.

### 8.7 — RIG quyết mẫu của phép đo: HAI cách hỏng, cả hai đã đo

**(1) `git archive` — rig KHÔNG có `.git` — sinh SÁU ca đỏ vô can.** Đo 21-09 khi dựng bản sao cho
`m10`/`m14`: suite trả `1708/1715` thay vì `1714/1715`, và sáu ca thừa là
`r328_deploy_ep_utf8_hai_chieu` · `r218_docclaims_sach_khong_bao_gia` ·
`r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` · `r244_script_deploy_khong_vao_goi` ·
`r249_bao_cao_rasoat_ngoai_goi` · `r251_deploy_guard_chiu_duoc_banner_gws` — tất cả đều hỏi git
hoặc `core.abbrev`. Sáu ca ấy đỏ **ở CẢ HAI vế** nên delta của ô ma trận vẫn đọc được, nhưng con
số `N/1715` thì vô nghĩa. Dựng lại bằng `git clone` + `git config core.abbrev 7` ⇒ nền về
`1715/1715` sạch. **Rig đo `tl_selftest.py` phải có `.git` THẬT và `core.abbrev = 7`.**

**(2) Chạy SONG SONG.** Lần đo đầu chạy bốn `tl.py --selftest` **song song**. `m7`/`m9` xong bình thường; `m10` chết
`KeyError: 'rootFolderId'`, `m11` chết `json.decoder.JSONDecodeError: Expecting value: line 1
column 1` — **không ca nào của `r378` liên quan**. Chạy lại TUẦN TỰ ⇒ cả bốn cho kết quả sạch ở
bảng trên.

Ghi vào đặc tả vì nó đúng lớp `RIG-QUYET-MAU-CUA-PHEP-DO` mà §6 đang đếm, và vì nó suýt thành
một kết luận sai: *"m10/m11 làm suite vỡ"* nghe như một finding, trong khi sự thật là **bộ
selftest dùng chung trạng thái trên đĩa nên không chạy song song được**. Ai đo đột biến trên
`scripts/tl_selftest.py` phải chạy tuần tự.

## 9. `dieu_kien_dung` — MỚI Ở r4

Chỉ thị chủ kho 21-09-2026 (§0.3):

> *"Chuyển điều kiện dừng là tới khi không còn findings P1, P2, P3"*

**Vòng lặp vá / cross-review của packet này dừng khi một lượt cho `0` finding ở CẢ BA mức `P1`,
`P2`, `P3`.** Bốn điều phải khai kèm, vì chúng quyết định luật này chặt hay lỏng:

- **Chặt hơn `cross_approved`.** Một verdict `approve` vẫn có thể kèm P3 — năm lượt đã chạy trên
  packet này đều có finding, nên **không lượt nào trong số đó dừng được** dưới luật mới.
- **`P4` / "giới hạn đã khai" KHÔNG nằm trong điều kiện dừng**, theo đúng chữ của chỉ thị. Nhưng
  `KHÔNG ĐO ĐƯỢC` **vẫn làm cổng ĐỎ** theo doctrine ba trạng thái — nó không biến mất, chỉ không
  phải thứ được đếm ở đây. §7 của đặc tả này liệt kê **mười** mục `KHÔNG ĐO ĐƯỢC`; không mục nào
  trong đó được luật mới xoá.
- **Executor KHÔNG được xin hạ mức một finding để đóng vòng lặp.** Mức nặng là phán quyết của
  reviewer. Một luật dừng đếm theo MỨC thì cám dỗ đầu tiên là đi xin hạ mức, và đó là cách luật
  này chết. Mọi lần hạ mức phải do reviewer tự làm, tự nêu lý do ĐO ĐƯỢC.
- **`0` finding mà verdict KHÔNG phải `approve` là MÂU THUẪN phải giải, không phải điểm dừng.**

**KHÔNG thay `human_audited`.** §0 của đặc tả này và lease đều khai `assurance_target:
human_audited`, và `cross_approved` không thay được nó. Điều kiện dừng là một điều kiện **THÊM**:
packet xong khi CẢ BA cùng đạt — `0` finding P1/P2/P3 · một lượt thẩm định của NGƯỜI · một lượt
CI đầy đủ trên head cuối.

**Trạng thái tại lúc đóng băng r4: `KHÔNG ĐO ĐƯỢC`.** Head `ce9de50` chưa qua lượt cross-review
nào. Năm lượt trước đo trên các head cũ (`20641d5`, `efaf576`, …) nên verdict của chúng **không
chuyển sang head này** — `reviewed_sha` là mỏ neo, và head đổi thì verdict cũ hết hiệu lực.
