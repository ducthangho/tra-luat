# ĐẶC TẢ — `R378-SYMLINK-DOI-DAC-QUYEN` — **revision 9, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `packet_id` | `R378-SYMLINK-DOI-DAC-QUYEN` |
| `revision` | **9** |
| `thay_the_cho` | revision 8, `b001234e418d5a03ee90db6441581d327308aac9504ceadd54dbc77f2acf0bb6` |
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
| `phan-hang-giet-gia-thieu-doi-chung` (b) | mỗi nhãn một đại diện; câu khai của r2 dòng 67, nguyên văn *"dù nó sai theo chiều nào"* *(r3–r8: một cụm diễn ý trong ngoặc như lời r2 — r9 sửa, §0.8)* | `A6`, §8.3 |
| **(c) — không reviewer nào nêu; phiên điều phối TỰ ĐO khi thi hành chính `A11`** | ma trận SÁU dạng — bản đầu của ma trận theo HỌ ở `576774b` (r6 sửa nhãn — bản trước ghi *"ma trận r2"*) không phân biệt nổi `m10` (so bằng CHUỖI) với `m14` (so bằng `args`): **cùng 27 ô, CÙNG một tập 27 toạ độ** ⇒ một BỘ TƯƠNG ĐƯƠNG. Trục `DOI_SO` phủ SỐ LƯỢNG đối số mà không phủ NỘI DUNG. | `A6` (dạng thứ bảy `moc_kem_doi_so_2`), §8.5 |

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

### 0.4 — Vì sao có revision 5

Chủ kho, phiên 24-09-2026, nguyên văn: **"Đồng ý r5, windows để sau"** — trả lời báo cáo cross-review
codex (`gpt-6-astra`, effort `medium`) trên head `34cb21f`, verdict `changes_requested`, **P1 0 · P2 1 ·
P3 0**, lớp `loi-khai-rong-hon-phep-do`. Hai trong ba biểu hiện của finding ấy nằm trong **đặc tả đã
đóng băng**, và phiên điều phối đo ra thêm một biểu hiện thứ tư cũng nằm trong đặc tả. Đặc tả đóng
băng không sửa được tại chỗ ⇒ revision.

**Ba thứ đổi ở r5 — cả ba là SỬA LỜI KHAI cho khớp PHÉP ĐO, không mở rộng phạm vi:**

1. **`A6` — số hạng.** r3 thêm dạng đối số thứ bảy `moc_kem_doi_so_2` và sửa `A11` + §8.3 thành 79 ô,
   nhưng **bỏ sót** ô `A6`: nó vẫn ghi 6 dạng · khối A 11×6 = 66 · tổng 68 — tức số của ma trận theo HỌ
   bản đầu `576774b` (r5 ghi *"ma trận r2"* — SAI, r6 sửa; xem §0.5).
   AST head `34cb21f`: `LOP=11`, `DOI_SO=7` ⇒ 77 + 1 + 1 = **79**. r5 sửa `A6` về 79.
2. **`A6` — phản chứng.** r3/r4 khai *"bỏ dạng `khong_doi_so` phải làm `m14` SỐNG LẠI"*. Reviewer đo
   toàn suite: rút `khong_doi_so` thì `m14` **vẫn đỏ**, `1714/1715`, `27/68` ô. Phiên điều phối đo thêm
   (phép cô lập trên AST, thay `_r378_run` bằng báo cáo rỗng vì oracle ma trận không đọc nó):

   ```
   mutant  rút khỏi trục                          LOP DOI_SO  kết quả
   —       (không rút)                             11   7     không ô nào đỏ
   m14     khong_doi_so                            11   6     ĐỎ, 27 toạ độ
   m14     moc_kem_doi_so_2                        11   6     ĐỎ, 27 toạ độ
   m14     khong_doi_so + moc_kem_doi_so_2         11   5     ĐỎ, 23 toạ độ
   m3      thuong_assert                           10   7     SỐNG (0 ô đỏ)
   m13     con_khac_module                         10   7     SỐNG (0 ô đỏ)

   tách m10/m14:   đủ 7 dạng      |m10|=34 |m14|=31  BẰNG NHAU=False  chỉ-m10=7 chỉ-m14=4
                   rút moc_kem_…  |m10|=27 |m14|=27  BẰNG NHAU=True   chỉ-m10=0 chỉ-m14=0
   ```

   ⇒ lời khai *"rút `khong_doi_so` làm `m14` sống lại"* **SAI VỀ NGUYÊN LÝ**, không chỉ vì dạng thứ
   bảy: rút cả hai dạng `m14` vẫn đỏ. Trục DẠNG ĐỐI SỐ **không có** phản chứng "hồi sinh" nào đo được;
   phản chứng THẬT của nó là **TÁCH `m10` khỏi `m14`** — đúng lý do r3 thêm dạng thứ bảy. Số cô lập
   `34`/`31`/`7`/`4` khớp **đúng** số toàn suite của reviewer. r5 thay phản chứng trong `A6`.
3. **`A11` — phạm vi.** r3/r4 đòi *"TOÀN BỘ bộ hồi quy lịch sử `m1`–`m14`"*. Quét cả bốn bản
   `r1`–`r4`: **không bản nào định nghĩa `m1` `m2` `m4` `m5` `m6` `m8`**; §8.4 định nghĩa đúng TÁM.
   Đọc các verdict trên PR #588 cho thấy vì sao: nhãn `mN` là nhãn **THEO TỪNG LƯỢT** và bị dùng lại
   với nghĩa khác — comment `5758435757` có `m1`–`m5` (`m5` = nới containment riêng nhánh tên trần);
   `5758802877` có `m2`–`m9` qua `scratch/target.py`; `5761292277` có `m1`–`m11` *"giết thật"*;
   `5763021895` nói *"giữ TRỌN bộ hồi quy `m1`–`m11`"*. Định nghĩa nằm trong scratchpad đã mất.
   ⇒ `A11` như r4 viết **không thoả mãn được bởi bất kỳ ai**, và reviewer lượt 24-09 đã đúng khi
   **từ chối** khai *"14/14 còn bị bắt"*. r5 thu `A11` về **tám** đột biến có định nghĩa, và đặt
   các định nghĩa ấy **BỀN** vào Phụ lục A — để lần sau không ai phải đi tìm lại.

**Không đổi ở r5:** `objective` · `write_set` (`scripts/tl_selftest.py`, `RELEASE_MANIFEST.json`) ·
`executor` · `environment` · `review_class` `sensitive` · `assurance_target` `human_audited` ·
§9 điều kiện dừng · các tiêu chí `A1`–`A5`, `A7`–`A10`. Phần mã của head `34cb21f` **không cần
đổi** vì r5 — r5 chỉ sửa cái THƯỚC ĐO mà mã phải đạt. Việc còn lại trong `write_set` là hai chú
thích sai số (§7 mục 12), và đó là việc của executor dưới lease mới.

**Windows để sau** — nguyên văn chủ kho. §7 mục 1, 2, 8 **vẫn** `KHÔNG ĐO ĐƯỢC` và vẫn giữ cổng ĐỎ.
"Để sau" là HOÃN, không phải THA.

**Trạng thái tại lúc đóng băng r5:** head `34cb21f` đã có MỘT lượt cross-review (24-09) — nhưng lượt
ấy đo theo thước r4. Theo thước r5, điều kiện dừng §9 là **`KHÔNG ĐO ĐƯỢC`** cho tới khi một lượt
review chạy với r5 làm hợp đồng.

**Cùng lớp lỗi, lần thứ mấy — khai cho đủ:** biểu hiện thứ tư này (`A11` đòi thứ không tồn tại) là
`LOI-KHAI-RONG-HON-PHEP-DO`. Bộ đếm lớp ấy của packet này từ **10** lên **11**. Và phiên điều phối
suýt lặp nó ngay trong lúc soạn r5: §9 viết *"§7 liệt kê mười mục"*, mà r5 thêm hai mục vào §7 —
đã sửa thành mười hai. **Khi sửa một con số, tìm mọi câu đếm thứ mình vừa đổi.**

### 0.5 — Vì sao có revision 6

Cross-review codex lượt 2 (24-09, `gpt-6-astra` effort `medium`) trên head `cf465b2` theo thước r5:
`changes_requested`, **P1 0 · P2 0 · P3 1**. F1a, F1b, F1c của lượt 1 **ĐÓNG**; `A11` đo TRỌN phạm vi
r5 (tám định nghĩa Phụ lục A tái tạo đúng từng byte, 8 lượt toàn suite, 28/28 cặp TẬP khác nhau). Lớp
`loi-khai-rong-hon-phep-do` **chưa đóng** vì một biểu hiện mới, **F1d**, và nó do CHÍNH r5 đưa vào.
Chủ kho đã cho phép: *"mở r6 nếu cần"*.

**F1d — r5 gán ma trận sáu dạng / 68 ô cho "r2". Sai.** Đo bằng `ast` trên blob Git thật, hàm
`_c378_ma_tran_phan_hang` trong `run()` của `scripts/tl_selftest.py`:

```
5b1772d  (r2, "A6 thành MA TRẬN BA TRỤC")          LOP=4   TD=3      — ma trận ĐẠI DIỆN
576774b  ("ma trận theo HỌ")                        LOP=11  DOI_SO=6  — 11×6 + 2 = 68 ô
ce9de50  ("dạng đối số thứ BẢY")                    LOP=11  DOI_SO=7  — 11×7 + 2 = 79 ô
cf465b2  (head lượt 2)                              LOP=11  DOI_SO=7  — 79 ô
```

Reviewer đo độc lập cùng kết quả, và thêm: bỏ docstring rồi rút phần tử thứ bảy khỏi head cho AST
**bằng chính xác** `576774b`. Nên ma trận 68 ô là **bản đầu của ma trận theo HỌ**, không phải của r2.

**Quét toàn r5 ra SÁU chỗ gán nhầm, không chỉ hai chỗ reviewer chỉ** — hai câu viết mới ở r5
(§0.4 mục 1, ô `A6`) và BỐN đoạn lịch sử kế thừa nguyên văn từ r3 (§0.2 bảng mục (c), §8.3,
tiêu đề và thân §8.5). r6 sửa nhãn ở cả sáu chỗ và đánh dấu tại chỗ rằng bản trước ghi *"ma
trận r2"*. Các chỗ nhắc "r2" khác trong tệp nói đúng về ma trận đại diện 4×3 và **giữ nguyên**.
*(r7: câu vừa rồi RỘNG HƠN phép đo — hai câu giải thích trong thân §8.5 vẫn gán cấu trúc của
`576774b` cho r2, và §8.3 trích r2 bằng một câu không có trong r2. Xem §0.6.)*

**Việc của executor, trong `write_set`:** chú thích `scripts/tl_selftest.py:25326` ghi bộ tương
đương m10/m14 thuộc *"ma trận r2/r3-bản-đầu"*. Phép đo chỉ có trên ma trận sáu dạng `576774b`;
chưa ai đo m10/m14 trên ma trận 4×3 của r2 ⇒ vế "r2" là lời khai rộng hơn phép đo. Sửa thành
ma trận sáu dạng ở `576774b`, rồi tái sinh `RELEASE_MANIFEST.json`.

**Không đổi ở r6:** mọi SỐ HẠNG và mọi PHÉP ĐO của r5 — `A6` 79 ô và ba phản chứng, `A11` tám đột
biến, Phụ lục A từng byte, §7 (vẫn mười hai mục), §9. r6 chỉ sửa **NHÃN PHIÊN BẢN** gắn vào các
con số. Phần mã của head **không** cần đổi vì r6; chỉ một chú thích.

**Vì sao vẫn phải là revision** dù không số nào đổi: ô `A6` là acceptance và câu sai nằm trong
chính ô ấy. Đặc tả đã đóng băng không sửa được tại chỗ.

**Cùng lớp, và khai cho đủ:** bộ đếm `LOI-KHAI-RONG-HON-PHEP-DO` của packet này **11 → 12**.
Cách nó lọt: khi soạn r5 phiên điều phối sửa CON SỐ bằng phép đo, còn NHÃN gắn vào con số thì chép
từ văn bản cũ mà không đo. Chính bài học r5 đã viết — *"một quan hệ đúng không chứng minh các số
hạng đúng"* — áp y hệt cho nhãn: **một con số đúng không chứng minh nhãn gắn với nó đúng.**

### 0.6 — Vì sao có revision 7

Cross-review codex lượt 3 (24-09, `gpt-6-astra` effort `medium`) trên head `aff0089` theo thước r6:
`changes_requested`, **P1 0 · P2 0 · P3 1**. F1a, F1b, F1c **ĐÓNG**; `A11` đo TRỌN (8/8 định nghĩa
Phụ lục A bằng byte, 8 lượt toàn suite, 28/28 cặp TẬP khác nhau); mã head **không có finding**. Lớp
`loi-khai-rong-hon-phep-do` **chưa đóng**: F1d còn hai câu trong thân §8.5, và câu *"các chỗ nhắc r2
khác … đúng"* mà r6 thêm vào §0.5 bị chính hai câu ấy bác.
Chủ kho đã cho phép, trả lời đề nghị "đẩy spec r7 và cấp lease g7 cho #574" (24-09): *"Đồng ý cả
2. Làm đi"*.

**Hai câu reviewer chỉ, sửa ở r7:**
- §8.5, đoạn so cơ chế `m10`/`m14`: *"mà ma trận r2 **không phân biệt nổi**"* → ma trận sáu dạng
  `576774b`. Đo bằng `ast` trên blob Git: r2 (`5b1772d`) có `LOP` 4 × `TD` 3 — **không** có trục `DOI_SO`.
- §8.5, đoạn *"Chỗ tách chúng"*: *"Trục `DOI_SO` của r2 có `hai_doi_so`"* → trục `DOI_SO` của `576774b`.
  Trục thông điệp của r2 là `TD = (goc, khac, rong)`; `DOI_SO` và `hai_doi_so` xuất hiện từ `576774b`.

**Chỗ THỨ BA, không reviewer nào nêu — tìm ra khi quét:** §8.3 viết *"**r2 khai:** 'một cài đặt sai
theo bất kỳ chiều nào phải làm ít nhất một ô đỏ'"*, đặt trong ngoặc như trích NGUYÊN VĂN. Câu ấy
**không có trong r2** (tìm chuỗi trên blob r2 ⇒ 0 lần; có trong r3–r6, tức nó sinh ra ở r3). Câu thật
của r2, dòng 67: *"nên một cài đặt sai phải làm ít nhất một Ô đỏ dù nó sai theo chiều nào."* Nghĩa
tương đương; lỗi ở chỗ một câu DIỄN Ý mang dấu TRÍCH DẪN. r7 thay bằng câu thật.

**Cách quét, để lời khai "đủ" lần này có phạm vi:** liệt kê MỌI dòng chứa `r2` trong r6 (37 dòng, `grep -c`
kể cả tiêu đề, §0.5 và sổ đếm), phân loại từng dòng: (i) nói về r2 như một revision/sự kiện; (ii) gán
một cấu trúc ma trận cho r2; (iii) trích lời r2. Mọi dòng loại (ii) được đối chiếu với AST blob
`5b1772d` (4×3+2 = 14 ô); mọi dòng loại (iii) được tìm nguyên văn trong blob r2. Kết quả: hai dòng
(ii) sai (hai câu trên), một dòng (iii) sai (câu §8.3); còn lại khớp. *(r8: lời khai này SAI — phép
phân loại làm BẰNG MẮT đã sót hai câu loại (iii) nữa, ở §6 và §8.4; cross-review lượt 4 bắt câu §6, phép quét
bằng máy ở r8 bắt thêm câu §8.4. Xem §0.7.)* Phạm vi của lời khai này là
**các dòng chứa chuỗi `r2`** — một câu gán sai mà không nêu tên phiên bản thì phép quét này không thấy.

**Không đổi ở r7:** mọi số hạng, phép đo, `A6`, `A11`, Phụ lục A từng byte, §7, §9, `write_set`. Mã
head **không** cần đổi vì r7.

**Cùng lớp:** bộ đếm `LOI-KHAI-RONG-HON-PHEP-DO` **12 → 13** — lần này do chính lời khai "đã quét
đủ" của r6. Bài học, nói cho hẹp: sửa NHÃN ở những chỗ đã chỉ không phải là quét; quét là liệt kê
bằng máy rồi phân loại từng dòng, và khai rõ phép liệt kê ấy mù ở đâu.

### 0.7 — Vì sao có revision 8

Cross-review codex lượt 4 (25-09, `gpt-6-astra` medium) trên head `aff0089` theo thước r7: `changes_requested`,
**P1 0 · P2 0 · P3 1** — F1d tiếp diễn: §6 vẫn trích r2 bằng câu diễn ý đặt trong ngoặc như nguyên văn, và
docstring `scripts/tl_selftest.py` mang đúng câu ấy. Lời khai "đã quét đủ" của r7 §0.6 SAI. Chủ kho duyệt mở r8
+ lease mới, với điều kiện quét BẰNG MÁY (25-09: *"Mở r8 + g8, quét bằng máy"*).

**Đây là lần THỨ TƯ cùng một hình dạng** (lời khai về r2 trôi khỏi nguồn: r5 gán nhãn, r6 hai câu §8.5, r7
§8.3/§6). Ba lần trước đều vá theo danh sách người khác chỉ hoặc theo phép đọc bằng mắt. Lần này phép quét là
một SCRIPT, và kết quả của nó ghi vào đây để lần sau lặp lại được:

- **Miền:** mọi chuỗi trong ngoặc kép `"…"` dài ≥ 12 ký tự trên một dòng mà dòng ấy hoặc dòng ngay trước có
  token `r2` đứng riêng (không khớp `r2xx`, `r210…`). Chuẩn hoá cả hai phía: bỏ `*`, `**`, dấu backtick, gộp
  khoảng trắng.
- **Phép so:** chuỗi có nằm NGUYÊN VĂN trong blob đặc tả r2 (`ops/specs/r378-symlink-doi-dac-quyen-r2.md`)?
  Nếu không, có phải một tiêu đề commit thật (`git log --all --format=%s`)?
- **Kết quả trên r7** — 19 chuỗi: 8 `KHỚP_R2`, 2 `TIÊU_ĐỀ_COMMIT`, 9 `KHÔNG_KHỚP`. Chín chuỗi không khớp, phân
  loại từng cái:

| dòng r7 | chuỗi | phân loại |
|---|---|---|
| 211, 216 | lời của r5 / chú thích mã cũ (`"ma trận r2"`, `"ma trận r2/r3-bản-đầu"`) | trích bản KHÁC, không gán cho r2 — đúng |
| 243, 245 ×2 | các câu của r6 mà §0.6 dẫn lại | trích r6 — đúng |
| 567 ×2 | mảnh do ngoặc lồng trong ghi chú r7 tự thêm | tạo tác của regex — không phải trích dẫn |
| **376** | *"một cài đặt sai theo BẤT KỲ CHIỀU NÀO …"* | **GÁN SAI cho r2** — r8 sửa |
| **538** | *"bốn ô ĐẦU TIÊN khác nhau"* | **GÁN SAI cho r2** (r2 có cột *"ô đỏ ĐẦU TIÊN"*, không có câu này) — r8 sửa |

**Chạy lại cùng script trên CHÍNH r8:** hai dòng gán sai (376, 538 của r7) đã hết; còn 12 chuỗi không khớp =
7 chuỗi vô hại như bảng trên (vị trí dịch dòng) + 4 chuỗi do r8 tự thêm khi MÔ TẢ lỗi cũ (ba dòng bảng §0.7, một
ghi chú ở §8.4) + 1 chuỗi là biểu thức chính quy trong mã script ở Phụ lục B. Không chuỗi nào gán sai cho r2.
*(r9: câu cuối SAI — nó đúng trong MIỀN của script, không đúng cho tài liệu. Dòng 99 của r8, bảng §0.2, vẫn trích
một cụm diễn ý như lời r2; token `r2` nằm ở tiêu đề bảng cách ba dòng, ngoài cửa sổ hai dòng. Cross-review lượt 5
bắt. Xem §0.8.)*

**Giới hạn của phép quét, khai thẳng:** nó chỉ thấy chuỗi trong ngoặc KÉP `"…"`, dài ≥ 12, gần token `r2`. Một
lời trích dùng ngoặc khác, ngắn hơn, hoặc gán cho r2 mà không nêu tên phiên bản trong hai dòng thì nó KHÔNG thấy.

**Không đổi ở r8:** mọi số hạng, phép đo, `A6`, `A11`, Phụ lục A, §7, §9, `write_set`. Mã head đổi DUY NHẤT một
docstring (`scripts/tl_selftest.py`, câu r2 → nguyên văn) và manifest tái sinh theo.

### 0.8 — Vì sao có revision 9

Cross-review codex lượt 5 (25-09, `gpt-6-astra` medium, 2104s) trên head `677ef37` theo thước r8:
`changes_requested`, **P1 0 · P2 0 · P3 1**. F1a, F1b, F1c ĐÓNG (vá thật). F1d `loi-khai-rong-hon-phep-do` còn
MỘT biểu hiện: bảng §0.2 dòng 99 của r8 đặt một cụm diễn ý trong dấu ngoặc dưới cột tiêu đề `r2 sai ở đâu`, tức
trích như lời r2 — cụm ấy không có trong r2, kể cả sau chuẩn hoá. Script của r8 (Phụ lục B) không thấy vì token
`r2` ở tiêu đề bảng cách ba dòng, ngoài cửa sổ hai dòng. Chủ kho duyệt (25-09): *"Mở r9 + g9, quét theo ngữ cảnh"*.

**Lần THỨ NĂM cùng hình dạng.** Bốn lần trước sửa theo chỗ được chỉ (r5, r6, r7) hoặc theo một phép quét có cửa
sổ cố định (r8). Reviewer lượt 5 nói đúng chỗ đáng nhớ: nới cửa sổ thêm vài dòng chỉ dời chỗ mù. r9 đổi ĐƠN VỊ
quét, không đổi kích thước cửa sổ.

**Bộ quét theo ngữ cảnh (Phụ lục C, nguyên văn):**

- **Đơn vị = KHỐI:** một bảng (các dòng `|` liền nhau, gồm cả hàng tiêu đề) hoặc một đoạn (cách nhau bằng dòng
  trống), cộng tiêu đề `#` gần nhất. Mọi lời trích trong khối thuộc ngữ cảnh r2 khi khối HOẶC tiêu đề có token
  `r2` đứng riêng. Khối mã có rào bị bỏ qua (mã, không phải lời trích).
- **Lời trích:** chuỗi trong ngoặc kép thẳng hoặc ngoặc kép cong, dài ≥ 8, **được vắt qua nhiều dòng** trong
  cùng khối.
- **Tệp `.py`:** mọi hằng chuỗi > 40 ký tự (docstring) lấy bằng `ast`, tách đoạn theo dòng trống — đường của
  docstring `aff0089` mà script r8 không thấy.
- **Phân loại:** `KHỚP_R2` (có nguyên văn trong r2 sau chuẩn hoá) · `TIEU_DE_COMMIT` · `KHÔNG_KHỚP`. Có mặt
  trong một revision KHÁC **không** phải bằng chứng: các revision sau CHÉP lại chính cụm gán sai (dòng 99 có ở
  r3–r8). Script chỉ GHI bản nào cũng chứa chuỗi ấy, để người đọc thấy nó đã truyền qua bao nhiêu bản.
- `KHÔNG_KHỚP` KHÔNG phải lỗi. Nó là danh sách phải PHÂN LOẠI BẰNG TAY — bảng dưới.

**Ca biết trước đáp án — chạy TRƯỚC khi tin bộ quét** (bài học `quet_lease.py`: hỏi công cụ một ca đã biết
đáp án). Cả bốn ĐẠT:

| đầu vào | phải | ra |
|---|---|---|
| r8 (`b001234e…`) | gắn cờ dòng 99 | `KHÔNG_KHỚP :99: bất kỳ chiều nào` |
| docstring `scripts/tl_selftest.py` ở `aff0089` | gắn cờ câu diễn ý vắt ba dòng | `KHÔNG_KHỚP :25315:` (câu cũ) |
| docstring ở `677ef37` | câu dòng 67 là `KHỚP_R2` | `KHỚP_R2` — nhưng còn một `KHÔNG_KHỚP` (xem dưới) |
| docstring ở `19f2141` | không còn chuỗi gán sai | 1 chuỗi, `KHỚP_R2` |

**Kết quả trên r8 — 43 chuỗi trong ngữ cảnh r2: 12 `KHỚP_R2`, 31 `KHÔNG_KHỚP`.** Phân loại từng nhóm theo số
dòng r8:

| dòng r8 | nhóm | phán |
|---|---|---|
| **99** | cụm diễn ý dưới cột `r2 sai ở đâu` | **GÁN SAI cho r2** — r9 sửa, trích đúng mảnh dòng 67 |
| 100, 136, 210, 216, 243, 245 ×3, 590, 600 | chữ của r3–r6 (nhãn *ma trận r2* sai và các câu §8.5) được dẫn lại để nói bản trước ghi sai | trích bản KHÁC — đúng |
| 138 | lời khai của r3/r4 | trích r3/r4 — đúng |
| 237, 239 ×2, 248, 274, 275, 291 ×2, 294, 295 | chữ của r7/r8 và chỉ thị chủ kho, dẫn lại khi MÔ TẢ lỗi cũ | trích bản KHÁC / chỉ thị — đúng |
| 401, 402, 403, 606 ×2 | mảnh do dấu nháy trong ô bảng / ngoặc lồng ghép sai cặp | tạo tác của regex — không phải lời trích |
| 537 | cụm của CHÍNH r3 (*"r3 khai lại"*): phạm vi ma trận KHÔNG phủ | cách nói của r3 — đúng |
| 577 | ghi chú r8 mô tả cụm gán sai cũ | mô tả lỗi cũ — đúng |
| 584 | luật của kho (*so TẬP, đừng so SỐ ĐẾM*) | trích doctrine — đúng |
| 598, 599 | hằng chuỗi trong mã | mã — không phải lời trích |

**Và một chỗ NGOÀI đặc tả mà bộ quét mới bắt được** — nên phải khai: docstring `scripts/tl_selftest.py` ở
`677ef37` đặt cụm *mọi cài đặt sai có thể viết bằng Python* (cách nói của r3 §8.4) trong ngoặc kép, NGAY sau câu
*"r2 đã khai quá rộng đúng chỗ này"* — đọc như lời r2. Không reviewer nào nêu; bộ quét r9 gắn cờ. Mã head
`19f2141` bỏ dấu trích và ghi nguồn; `RELEASE_MANIFEST.json` tái sinh (strict 180/180).

**Chạy lại cùng bộ quét trên CHÍNH r9:** 46 chuỗi — 13 `KHỚP_R2` (12 cũ + dòng 99 nay trích đúng mảnh), 33
`KHÔNG_KHỚP` = 30 chuỗi của bảng trên (bỏ dòng 99; số dòng dịch) + 3 chuỗi do CHÍNH mục này thêm: chỉ thị chủ kho,
cụm *r3 khai lại* ở bảng trên, và câu của docstring được dẫn lại ngay trên. Không chuỗi nào gán sai cho r2 —
trong MIỀN của bộ quét (xem giới hạn).

**Giới hạn, khai thẳng:** bộ quét chỉ thấy lời gán cho r2 khi token `r2` nằm trong CÙNG khối hoặc tiêu đề gần
nhất. Một lời gán qua đại từ (*"bản ấy"*), qua tham chiếu mục ở khối khác, hoặc dùng ngoặc đơn / in nghiêng không
ngoặc thì nó KHÔNG thấy. Phân loại `KHÔNG_KHỚP` là việc của người đọc, không phải của máy — bảng trên là phán
của phiên soạn r9, reviewer phải đo lại.

**Không đổi ở r9:** mọi số hạng, phép đo, `A6`, `A11`, Phụ lục A, Phụ lục B (giữ làm lịch sử), §7, §9,
`write_set`. Mã head đổi DUY NHẤT một docstring (`scripts/tl_selftest.py`, bỏ dấu trích cụm của r3) và manifest
tái sinh theo.

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
| **A6** (VIẾT LẠI ở **r3**; **SỬA SỐ HẠNG và PHẢN CHỨNG ở r5** — §0.4) | `_r378_classify` phải đúng trên một ma trận mà **mỗi nhãn mang một HỌ thành viên**, không một đại diện. Trục **LỚP**, 11 thành viên: lớp THẬT · con CÙNG module · con **KHÁC module** · **ĐA KẾ THỪA** · `RuntimeError` · **`AssertionError`** · **`ValueError`** · `TypeError` · `KeyError` · **TRÙNG TÊN** khác `id()` · **TRÙNG TÊN và là lớp con của `ValueError`**. Trục **DẠNG ĐỐI SỐ**, **7** dạng: không đối số · chuỗi rỗng · thông điệp gốc · thông điệp khác · hai đối số · **`moc_kem_doi_so_2`** (thêm ở r3 để tách `m10` khỏi `m14`, §8.5) · `None`. Trục **ORACLE**: chạy-và-ném (khối A, 11×7 = **77** ô) · chạy-và-thoả (khối B) · khâu DỰNG hỏng (khối C). Tổng **79** ô — khớp `A11`, §8.3 và AST của head `34cb21f` (`LOP=11`, `DOI_SO=7`). **r3 và r4 ghi ô này là 6 dạng / 66 / 68 — đó là số của ma trận theo HỌ bản đầu `576774b`, bị bỏ sót khi `ce9de50` thêm dạng thứ bảy** (r5 ghi nhầm là *"ma trận r2"*; ma trận r2 là 4×3 ĐẠI DIỆN ở `5b1772d` — §0.5). Ca **THU TẬP ĐẦY ĐỦ** tập ô đỏ rồi mới ném một lần, KHÔNG dừng ở ô hỏng đầu tiên — `A11` đòi so TẬP ô, dừng sớm thì không so được. Khối B và C chốt thêm **SỐ LẦN GỌI** oracle (đúng 1 · đúng 0). | Mỗi ô có `expected` là **DỮ LIỆU** — suy từ cờ `bat_duoc` VIẾT TAY và `lop.__name__`, KHÔNG từ chính `_r378_classify`. Bảng fixture có **chốt tự kiểm**: `bat_duoc` phải khớp `issubclass`; hai lớp `trung_ten*` phải thật sự trùng `__name__`; lớp `con_khac_module` phải thật sự khác `__module__` — trôi cái nào thì ném `R378_MA_TRAN_FIXTURE_TROI`. **Phép đo làm A6 ĐỎ — BA phản chứng cho hình dạng HỌ, cả ba ĐÃ ĐO (§0.4):** (1) rút `thuong_assert` khỏi trục LỚP ⇒ `m3` **SỐNG LẠI** (0 ô đỏ); (2) rút `con_khac_module` ⇒ `m13` **SỐNG LẠI**; (3) rút `moc_kem_doi_so_2` khỏi trục DẠNG ĐỐI SỐ ⇒ **TẬP ô đỏ của `m10` BẰNG TẬP của `m14`** (27 = 27, hai hiệu tập rỗng) — bộ tương đương của §8.5 tái xuất hiện; với đủ 7 dạng thì `m10` 34 · `m14` 31 · chỉ-`m10` 7 · chỉ-`m14` 4. **KHÔNG được khai** rằng rút `khong_doi_so` làm `m14` sống lại: r3/r4 khai như vậy và phép đo **BÁC** — rút riêng nó `m14` vẫn đỏ 27/68, rút cùng `moc_kem_doi_so_2` vẫn đỏ 23 toạ độ. **GIỮ NGUYÊN ngữ nghĩa `except` của Python**: lớp CON vẫn là `killed`; ma trận ĐO bộ phân hạng, nó KHÔNG tự quyết đổi sang so kiểu chính xác. |
| **A11** (VIẾT LẠI ở **r3**; **THU PHẠM VI về bộ CÓ ĐỊNH NGHĨA BỀN ở r5** — §0.4) | Ma trận phải bắt **TOÀN BỘ bộ hồi quy đã định nghĩa BỀN ở Phụ lục A** — **TÁM** đột biến `m3` `m7` `m9` `m10` `m11` `m12` `m13` `m14` — và **ô đỏ của mỗi cái là một phép ĐO, không phải một dự đoán**. **r3/r4 đòi `m1`–`m14`; điều đó KHÔNG thoả mãn được**: các nhãn `m1` `m2` `m4` `m5` `m6` `m8` là nhãn **THEO TỪNG LƯỢT review**, được dùng lại với nghĩa KHÁC NHAU qua các lượt, và định nghĩa của chúng nằm trong scratchpad đã mất cùng container — không bản đặc tả nào `r1`–`r4` định nghĩa chúng (§0.4). Lớp `L7 KHONG-THOAI-LUI-HO-DOT-BIEN-KHI-DOI-CA` vẫn nguyên: *mọi mutant lịch sử đã bị bắt trước refactor phải tiếp tục bị bắt* — nhưng một mutant chỉ **thuộc** bộ hồi quy khi định nghĩa của nó **nằm BỀN trong kho** dưới dạng neo/thay chạy được. Mutant mới muốn vào bộ phải vào Phụ lục A qua một revision. | Chạy TOÀN suite, **TUẦN TỰ** (§8.7), mỗi đột biến một lượt `tl.py --selftest` đầy đủ trên một `git clone` có `.git` THẬT, `core.abbrev = 7`, và `commit.gpgsign=false` CHỈ trong tiến trình test (fixture ký commit hỏng trong sandbox — cả hai reviewer lượt 24-09 đều vấp, §0.4); ghi lại **TẬP ô đỏ** kèm `expected`/`observed`/`oracle_calls`. **So bằng TẬP, KHÔNG bằng SỐ ĐẾM**: đủ **28 cặp** của tám đột biến phải khác nhau đôi một. **Đường đọc**: TẬP ô phải đọc từ bản sao RIG đã nới `_TRAN_CHAN_DOAN_110` (harness cắt chẩn đoán ở 400 ký tự, §8.3). **Tiêu chí này KHÔNG ghi trước ô nào ứng với đột biến nào** — bản nháp r2 từng ghi *"`m7` ⇒ ô `LỚP=that`"* và phép đo BÁC. **Đo ở r5 trên head `34cb21f`** (cross-review 24-09): cả tám `1714/1715`, `rc=1`, ca đỏ DUY NHẤT `r378_ma_tran_phan_hang`, ô đỏ 7·8·1·34·35·14·7·31 trên 79, **28/28 cặp khác nhau**. |
| **A7** | `tl.py --selftest` **DELTA so `origin/master` = 0** trên POSIX, và `r378_l7_resolve_phai_o_trong_kho` ở tập ĐẠT của cả hai vế. | **Đo hai vế trong MỘT lệnh**, cùng các bước, chạy liền nhau. So **TẬP TÊN** ca đỏ, không so số đếm — *"mất một ca đỏ cũ, thêm một ca đỏ mới, tổng không đổi"* là ca mà phép đếm không bắt được. Nền đo 20-09 trên Linux: **1711/1711**; **đo lại trước khi tin** (L5). |
| **A8** | `release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true` **và** `expected == checked`. | Chạy **tại chỗ, đúng lệnh của lane LAND**. Lane PR **KHÔNG** bắt được lệch manifest (`if: github.ref == 'refs/heads/master'`; lane WORKER sinh manifest tạm nên hấp thụ mọi thay đổi nội dung) ⇒ PR xanh, master ĐỎ. |
| **A9** | `numstat` chạm **đúng hai** đường của `write_set`. | Đột biến thêm đường thứ ba ⇒ ĐỎ. Chốt write-set exclusion §5. |
| **A10** | `doctrine-scan` · `adr-song` · `doc-claims-check --strict` · `git diff --check` `rc=0`, `core.abbrev = 7`. | `rc` đọc **trực tiếp**, không qua pipe (nợ `RC-QUA-PIPE-KHONG-CO-CHOT`). |

## 6. `hinh_dang_ke_thua` (L4) — chép từ #565

| hình dạng | số lần | nguồn |
|---|---|---|
| `RIG-QUYET-MAU-CUA-PHEP-DO` | **5** | Chép từ #565 (4 ca `CLAUDE.md` 24-08 + `Đ1`). **Packet này chạm đúng lớp ấy**: một ca đỏ vì RIG (thiếu đặc quyền), không vì mã. |
| `NGOAI-LE-BI-NUOT-LANG` | **2** | Chép từ #565. Ca r378 từng đỏ **câm** trước khi `Đ2` land — chính nó là ca thứ hai. |
| `LOI-KHAI-RONG-HON-PHEP-DO` | 7 → **10** | Chép 6 từ biên nhận #565. **+1**: câu *"KHÔNG PORT THẲNG ĐƯỢC … giả thuyết, chưa chạy"* của #574 **hẹp hơn** phép đo — mẫu ấy đã có sẵn và đã chạy trong cùng tệp. Lời khai lệch phép đo **theo chiều hẹp** cũng là lệch. **+1 ở r3**: câu của r2 (dòng 67, nguyên văn) *"nên một cài đặt sai phải làm ít nhất một Ô đỏ dù nó sai theo chiều nào."* *(r3–r7 trích bằng câu diễn ý trong ngoặc; r8 sửa — §0.7)* — **rộng hơn**, và lượt 5 bác bằng ba phản chứng nằm ngay trong các trục r2 đã khai (§8.3). |
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
11. **Sáu nhãn đột biến `m1` `m2` `m4` `m5` `m6` `m8`** — **KHÔNG ĐO ĐƯỢC, và không khôi phục được.** Nhãn
    theo từng lượt, dùng lại với nghĩa khác nhau; định nghĩa nằm trong scratchpad của các phiên review
    21-09 (`…/scratchpad/xr588/scratch/target.py`), đã mất cùng container. Vì vậy chúng **ra khỏi**
    `A11` ở r5 (§0.4). Nếu ai dựng lại được một định nghĩa có neo SHA, nó vào Phụ lục A qua revision.
12. **Hai chú thích trong `scripts/tl_selftest.py` ghi SAI số đo** — `23 toạ độ` cho bộ tương đương
    `m10`/`m14` dưới ma trận SÁU dạng, trong khi đo được **27** (dòng `25326` và `25427` ở head `34cb21f`;
    dòng `25328` cùng đoạn đã ghi `27`). Số 23 là của ma trận **NĂM** dạng (rút thêm `khong_doi_so`, §0.4).
    Đây là việc của EXECUTOR, trong `write_set`: sửa hai chú thích, KHÔNG rút fixture để khớp số cũ.

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

**r2 khai** (dòng 67, nguyên văn): *"nên một cài đặt sai phải làm ít nhất một Ô đỏ dù nó sai theo
chiều nào."* *(r3–r6 trích bằng một câu diễn ý đặt trong ngoặc; r7 thay bằng câu thật — §0.6.)* Câu ấy **RỘNG
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
độ đầu. Đo thật: cùng một lượt `m10` (ma trận sáu dạng `576774b`, ca tự khai `27/68`), bản cắt ở 400 ký tự đọc ra được
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
bốn ô của r2 — ở đó bằng chứng chỉ là bốn ô đỏ đầu tiên khác nhau (r2 §8.4, cột *"ô đỏ ĐẦU TIÊN"*), vì ca dừng ngay ô hỏng đầu. *(r3–r7 đặt "bốn ô ĐẦU TIÊN khác nhau" trong ngoặc như lời r2 — r2 không có câu ấy; r8 sửa, §0.7.)*

Hai tập đọc kỹ cho thấy ma trận đang đo TRỤC chứ không đo điểm:

- `m3` đỏ **đúng 7 ô**, tất cả ở `lop=thuong_assert`, trải hết **cả 7 dạng đối số** — một lát cắt
  SẠCH theo trục LỚP. Đây chính là phủ mà r2 đánh rơi.
- `m13` cũng đỏ **đúng 7 ô**, tất cả ở `lop=con_khac_module`, cũng trải hết 7 dạng. Cùng lực
  lượng, **tập khác hẳn** — minh hoạ sống cho luật "so TẬP, đừng so SỐ ĐẾM".

### 8.5 — `m10` và `m14` là một BỘ TƯƠNG ĐƯƠNG dưới ma trận SÁU dạng (`576774b`) — và không ai phát hiện ra

Đây là phát hiện đắt nhất của r3, và **không reviewer nào nêu**: nó lộ ra vì `A11` đòi so TẬP.

Đo trên ma trận **sáu dạng của bản đầu theo HỌ, `576774b`** (6 dạng đối số, 68 ô; r3–r5 ghi nhầm là *"ma trận r2"*), hai lượt `--selftest` riêng:

```
m10  27/68 ô đỏ · 27 toạ độ
m14  27/68 ô đỏ · 27 toạ độ
comm -23 = 0 · comm -13 = 0 · chung = 27      <- HAI TẬP BẰNG NHAU
```

`m10` phân hạng bằng **chuỗi** (`"R378_EXPECTATION_MISMATCH" in str(exc)`), `m14` bằng **`args`**
(`exc.args == ("R378_EXPECTATION_MISMATCH",)`). Hai cài đặt sai khác hẳn nhau về cơ chế, mà ma
trận sáu dạng `576774b` **không phân biệt nổi** *(r3–r6 ghi "ma trận r2" — sai, r7 sửa; §0.6)* — nó đang đo ÍT trục hơn nó khai, đúng một tầng nữa của cùng bệnh
mà r2 sinh ra để chữa.

**Chỗ tách chúng, và vì sao trục cũ không có:** một ngoại lệ mang mốc đúng **KÈM đối số thứ hai**.
`str()` của nó là `('R378_EXPECTATION_MISMATCH', 'x')` — **CHỨA** mốc, nên `m10` cấp `killed`;
`args` thì **KHÁC** tuple một phần tử, nên `m14` cấp tín dụng giả. Trục `DOI_SO` của `576774b` có
`hai_doi_so` (`("a","b")`) *(r3–r6 ghi "của r2" — r2 không có trục `DOI_SO`; §0.6)* nhưng **không** có dạng *"hai đối số trong đó cái đầu là mốc đúng"* —
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
  phải thứ được đếm ở đây. §7 của đặc tả này liệt kê **mười hai** mục (từ r5; r4 là mười) `KHÔNG ĐO ĐƯỢC`; không mục nào
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

## Phụ lục A — bộ hồi quy của `A11`: TÁM đột biến, định nghĩa BỀN (MỚI ở r5)

**Vì sao có phụ lục này:** `A11` của r3/r4 đòi `m1`–`m14`, và sáu nhãn trong đó **không còn định
nghĩa nào** — chúng sống trong scratchpad của các phiên review rồi mất cùng container (§0.4, §7 mục
11). Một bộ hồi quy mà thành viên chỉ có TÊN thì không chạy lại được. Từ r5, **một đột biến chỉ thuộc
bộ hồi quy khi định nghĩa neo/thay của nó nằm ở đây.**

**Mỏ neo:** hàm `_r378_classify` lồng trong `run()` của `scripts/tl_selftest.py`, head
`34cb21fc38388d81f318446dcd57148169b23f8f`, dòng `25056`–`25064`. Khối nguồn gốc (lấy bằng `ast`,
`lineno`…`end_lineno`, giữ ký tự xuống dòng):

```python
    def _r378_classify(old, new, body, oracle, root=None):
        """Ba hạng: killed / false_credit / survived; chỉ exception riêng của oracle là kill thật."""
        try:
            oracle(_r378_run(body, _r378_mutant(old, new), root=root))
        except _R378SaiKyVong:
            return "killed"
        except Exception as exc:  # noqa: BLE001
            return "false_credit:" + type(exc).__name__
        return "survived"
```

`sha256` của đúng khối trên = `6c4f2a8ce0803898039cb8e77d5dadc85db269287fafad399d56a0ef93fa7bb3`;
khối xuất hiện **đúng 1 lần** trong tệp. **Trước khi áp đột biến, kiểm băm này** — lệch thì mỏ neo đã
trôi và định nghĩa bên dưới phải được neo lại, không áp mù.

**Nhóm I — đổi mệnh đề `except`** (thay chuỗi `except _R378SaiKyVong:`, xuất hiện đúng 1 lần trong khối):

| nhãn | thay bằng |
|---|---|
| `m3` | `except (_R378SaiKyVong, AssertionError):` |
| `m7` | `except RuntimeError:` |
| `m12` | `except (_R378SaiKyVong, ValueError):` |

**Nhóm II — đổi giá trị trả về** (thay chuỗi `return "survived"`, đúng 1 lần):

| nhãn | thay bằng |
|---|---|
| `m9` | `return "killed"` |

**Nhóm III — thay cả đuôi phân hạng.** Từ dòng `        except _R378SaiKyVong:` (tám dấu cách, đúng 1
lần) tới hết khối, thay bằng:

```python
        except Exception as exc:
            if <ĐIỀU_KIỆN>:
                return "killed"
            return "false_credit:" + type(exc).__name__
        return "survived"
```

| nhãn | `<ĐIỀU_KIỆN>` | nó bắt chước kiểu phân hạng sai nào |
|---|---|---|
| `m10` | `"R378_EXPECTATION_MISMATCH" in str(exc)` | so bằng CHUỖI thông điệp |
| `m11` | `type(exc).__name__ == _R378SaiKyVong.__name__` | so bằng TÊN lớp |
| `m13` | `isinstance(exc, _R378SaiKyVong) and type(exc).__module__ == _R378SaiKyVong.__module__` | giới hạn lớp con theo MODULE |
| `m14` | `exc.args == ("R378_EXPECTATION_MISMATCH",)` | so bằng `args` |

**Rig bắt buộc cho mỗi lượt** (§8.7, và bẫy đã trả giá 24-09):
- một `git clone` riêng có `.git` THẬT, `git config core.abbrev 7`;
- CHỈ trong bản sao rig: `_TRAN_CHAN_DOAN_110 = 400` → `100000`, để đọc được đủ TẬP toạ độ;
- tiến trình test chạy với `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`
  — **chỉ** cho tiến trình ấy, không đổi cấu hình kho hay hệ thống. Thiếu nó thì fixture ký commit hỏng
  trong sandbox và suite ra `1709/1711` (nền) · `1713/1715` (head) — đỏ GIẢ, cả hai reviewer 24-09
  đều vấp rồi tự chuẩn hoá;
- chạy **TUẦN TỰ**, mỗi đột biến một lượt `python scripts/tl.py --selftest` TOÀN BỘ.

**Kết quả đã đo** (cross-review 24-09 trên `34cb21f`, reviewer codex; nền `515d16a` `1711/1711`,
head `1715/1715`):

| nhãn | rc | kết quả | ô đỏ / 79 | toạ độ phân biệt |
|---|---:|---|---:|---:|
| `m3` | 1 | 1714/1715, chỉ `r378_ma_tran_phan_hang` đỏ | 7 | 7 |
| `m7` | 1 | nt | 8 | 8 |
| `m9` | 1 | nt | 1 | 1 |
| `m10` | 1 | nt | 34 | 34 |
| `m11` | 1 | nt | 35 | 35 |
| `m12` | 1 | nt | 14 | 14 |
| `m13` | 1 | nt | 7 | 7 |
| `m14` | 1 | nt | 31 | 31 |

**28/28 cặp TẬP khác nhau.** `m3` và `m13` cùng 7 ô mà hai tập rời nhau hoàn toàn — đúng ca mà so
SỐ ĐẾM sẽ gộp nhầm.

**KHÔNG thuộc bộ:** `m14_without_noarg` (probe của reviewer 24-09: `m14` trên ma trận rút
`khong_doi_so`) là phép đo cho §0.4, không phải thành viên. Sáu nhãn `m1` `m2` `m4` `m5` `m6` `m8`
**không** thuộc bộ (§7 mục 11).

## Phụ lục B — script quét trích dẫn r2 của §0.7 (MỚI ở r8, nguyên văn)

Chạy: `python3 quet.py <đặc tả r2> <tệp cần quét>`, từ gốc kho (cần `git log`).

```python
import re, sys, subprocess
def chuan(s): return re.sub(r"\s+", " ", s.replace("**", "").replace("`", "").replace("*", "")).strip(" .…")
nguon = chuan(open(sys.argv[1], encoding="utf-8").read())
tieu_de = chuan(subprocess.run(["git","log","--all","--format=%s"],capture_output=True,text=True).stdout)
R2 = re.compile(r"(?<![\w-])r2(?![\w])")
Q = re.compile(r'"([^"\n]{12,})"')
L = open(sys.argv[2], encoding="utf-8").read().split("\n")
for i, l in enumerate(L):
    if not R2.search((L[i-1] if i else "") + " " + l): continue
    for m in Q.finditer(l):
        q = chuan(m.group(1))
        loai = "KHỚP_R2" if q in nguon else ("TIEU_DE_COMMIT" if q in tieu_de else "KHÔNG_KHỚP")
        print(f"{loai:15s} :{i+1}: {m.group(1)[:120]}")
```

## Phụ lục C — bộ quét trích dẫn r2 THEO NGỮ CẢNH của §0.8 (MỚI ở r9, nguyên văn)

Chạy: `python3 quet_v2.py <đặc tả r2> <tệp .md|.py> [<đặc tả khác> ...]`, từ gốc kho (cần `git log`). Phụ lục B giữ nguyên làm lịch sử.

```python
import ast, re, sys, subprocess
from pathlib import Path
# Dung: python3 quet.py <dac ta r2> <tep .md|.py> [<dac ta khac> ...]
# Don vi = KHOI (bang lien tiep, hoac doan cach nhau bang dong trong) + TIEU DE gan nhat.
# Mot loi trich thuoc ngu canh r2 khi KHOI hoac TIEU DE ay co token r2 dung rieng.
# Tep .py: moi hang chuoi > 40 ky tu (docstring) qua ast, tach doan theo dong trong.
# Khoi ma co rao ``` trong .md bi bo qua. KHÔNG_KHỚP khong phai loi — la cho phai PHAN LOAI bang tay.
def chuan(s): return re.sub(r"\s+", " ", s.replace("**", "").replace("`", "").replace("*", "")).strip(" .…,;:")
R2 = re.compile(r"(?<![\w-])r2(?![\w])")
Q = re.compile(r'"([^"]{8,}?)"|“([^”]{8,}?)”', re.S)
def khoi_md(van):
    L, tieu_de, kq, cur, dau, rao = van.split("\n"), "", [], [], 0, False
    def day():
        if cur: kq.append((dau + 1, tieu_de, "\n".join(cur)))
    for i, l in enumerate(L):
        if l.lstrip().startswith("```"):   # khoi ma co rao: la MA, khong phai loi trich — bo qua
            day(); cur = []; rao = not rao; continue
        if rao: continue
        la_bang = l.lstrip().startswith("|")
        if l.startswith("#"):
            day(); cur = []; tieu_de = l; continue
        if not l.strip() or (cur and la_bang != cur[-1].lstrip().startswith("|")):
            day(); cur = []
            if not l.strip(): continue
        if not cur: dau = i
        cur.append(l)
    day(); return kq
def khoi_py(van):
    kq = []
    for n in ast.walk(ast.parse(van)):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) > 40:
            for j, doan in enumerate(re.split(r"\n\s*\n", n.value)):
                kq.append((n.lineno, f"<chuoi dong {n.lineno}>", doan))
    return kq
def main(r2, dich, khac):
    nguon = chuan(Path(r2).read_text(encoding="utf-8"))
    ban = {Path(p).name: chuan(Path(p).read_text(encoding="utf-8")) for p in khac}
    tieu = chuan(subprocess.run(["git", "log", "--all", "--format=%s"], capture_output=True, text=True).stdout)
    van = Path(dich).read_text(encoding="utf-8")
    dem = {}
    for dong, td, k in (khoi_py if dich.endswith(".py") else khoi_md)(van):
        if not (R2.search(k) or R2.search(td)): continue
        for m in Q.finditer(k):
            raw = m.group(1) or m.group(2); q = chuan(raw)
            if q in nguon: loai = "KHỚP_R2"
            else:
                hit = [t for t, s in ban.items() if q in s]
                # Co trong ban KHAC khong phai bang chung: ban khac co the CHEP lai chinh loi gan sai.
                loai = "TIEU_DE_COMMIT" if q in tieu else ("KHÔNG_KHỚP" + (" (cung co o " + ",".join(sorted(hit)) + ")" if hit else ""))
            dem[loai.split(" ")[0]] = dem.get(loai.split(" ")[0], 0) + 1
            d = dong + k[:m.start()].count("\n") if not dich.endswith(".py") else dong
            print(f"{loai:40s} :{d}: {re.sub(chr(10), ' ', raw)[:110]}")
    print("TONG", dem)
main(sys.argv[1], sys.argv[2], sys.argv[3:])
```
