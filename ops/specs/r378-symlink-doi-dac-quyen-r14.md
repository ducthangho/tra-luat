# ĐẶC TẢ — `R378-SYMLINK-DOI-DAC-QUYEN` — **revision 14, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `packet_id` | `R378-SYMLINK-DOI-DAC-QUYEN` |
| `revision` | **14** |
| `thay_the_cho` | revision 13, `3c812540bd58b19099906df8e6fb00e22ec21728c1c880087ada4406af33b318` |
| `packet_issue` | **#574** |
| `nguon_cap_viec` | Nợ #574, mở theo chỉ thị chủ kho 20-09-2026 (*"Land xong thì mở nợ r378"* ⟦nguon:chi-thi⟧). Chỉ thị cấp lease r1: *"Cấp lease cho r378 đi"* ⟦nguon:chi-thi⟧, cùng phiên ~16:2xZ. **r2** là hệ quả của cross-review lượt 4, dưới chỉ thị 21-09-2026: *"Chạy lặp cross review, vá, đăng verdict cho tới khi approve"* ⟦nguon:chi-thi⟧. Xem §8. |
| `review_class` | **`sensitive`** — chạm `scripts/tl_selftest.py`, harness dùng chung, và ca đích đo một **chốt an ninh**. Cùng lớp mà #565 đã dùng cho chính tệp này. |
| `assurance_target` | **`human_audited`** — không đổi. **ĐÍNH CHÍNH lời khai của r1:** r1 viết `cross_approved` không đạt được vì quota ⟦r1:10 #2e1a63d5|KHÔNG ĐẠT ĐƯỢC⟧. Câu ấy **hết hiệu lực** — **bốn** lượt cross-review codex đã chạy trọn trên packet này (§8). Hạn quota là trạng thái tại thời điểm đo, không phải thuộc tính của đường. Điều KHÔNG đổi: một lượt review máy vẫn **không** cấp được `human_audited`. |
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
(bắt được), `r2/m3` ⇒ `1715/1715` (SỐNG). r2 viết là thay bốn vế rời ⟦r2:167 #5090d8c6|thay bốn vế rời⟧ mà **không kiểm bộ hồi quy
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
| `phan-hang-giet-gia-thieu-doi-chung` (b) | mỗi nhãn một đại diện; câu khai của r2 ⟦r2:67 #a64cff8f|dù nó sai theo chiều nào⟧ *(r3–r8: một cụm diễn ý trong ngoặc như lời r2; r9 trích mảnh; r10 thay bằng con trỏ — §0.9)* | `A6`, §8.3 |
| **(c) — không reviewer nào nêu; phiên điều phối TỰ ĐO khi thi hành chính `A11`** | ma trận SÁU dạng — bản đầu của ma trận theo HỌ ở `576774b` (r6 sửa nhãn — bản trước gọi nó là ma trận r2 ⟦r3:100 #37b637f2|ma trận r2 không phân biệt nổi⟧) không phân biệt nổi `m10` (so bằng CHUỖI) với `m14` (so bằng `args`): **cùng 27 ô, CÙNG một tập 27 toạ độ** ⇒ một BỘ TƯƠNG ĐƯƠNG. Trục `DOI_SO` phủ SỐ LƯỢNG đối số mà không phủ NỘI DUNG. | `A6` (dạng thứ bảy `moc_kem_doi_so_2`), §8.5 |

### 0.3 — Vì sao có revision 4

**MỘT lý do, và nó không phải một finding: chủ kho đổi ĐIỀU KIỆN DỪNG.**

Chỉ thị 21-09-2026, bản chiếu `issues/574#issuecomment-5765691395` (bản đầy đủ ở
`issues/579#issuecomment-5765688081`):

> *"Chuyển điều kiện dừng là tới khi không còn findings P1, P2, P3"* ⟦nguon:chi-thi⟧

`dieu_kien_dung` là **acceptance**, và §3.2 nói thẳng: *"Đổi objective, acceptance, write set,
dependency, executor hoặc environment tạo revision mới và làm lease cũ mất hiệu lực."* ⟦nguon:doctrine⟧ Không có
đường nào cho một chỉ thị như thế vào mà không qua revision. Lease `r378-symlink-doi-dac-quyen-
r3-g2-claude` neo r3 ⇒ mất hiệu lực theo đúng câu ấy.

**Phần kỹ thuật của r3 KHÔNG đổi một chữ.** `A6` (ma trận theo HỌ, 79 ô), `A11` (đòi bộ hồi quy,
so bằng TẬP), §8.4–§8.7 đều giữ nguyên. r4 thêm **§9 — điều kiện dừng**, và chỉ thế.

**Nói thẳng một điều r4 KHÔNG có:** packet này **chưa có lượt cross-review nào** dưới luật mới.
Điều kiện dừng mới đòi một lượt cho `0` finding P1/P2/P3, và tính tới lúc đóng băng r4 con số ấy
là **KHÔNG ĐO ĐƯỢC** — chưa lượt nào chạy trên head `ce9de50`. Đó không phải một khoảng trống
được tha; nó là việc còn lại.

### 0.4 — Vì sao có revision 5

Chủ kho, phiên 24-09-2026, nguyên văn: **"Đồng ý r5, windows để sau"** ⟦nguon:chi-thi⟧ — trả lời báo cáo cross-review
codex (`gpt-6-astra`, effort `medium`) trên head `34cb21f`, verdict `changes_requested`, **P1 0 · P2 1 ·
P3 0**, lớp `loi-khai-rong-hon-phep-do`. Hai trong ba biểu hiện của finding ấy nằm trong **đặc tả đã
đóng băng**, và phiên điều phối đo ra thêm một biểu hiện thứ tư cũng nằm trong đặc tả. Đặc tả đóng
băng không sửa được tại chỗ ⇒ revision.

**Ba thứ đổi ở r5 — cả ba là SỬA LỜI KHAI cho khớp PHÉP ĐO, không mở rộng phạm vi:**

1. **`A6` — số hạng.** r3 thêm dạng đối số thứ bảy `moc_kem_doi_so_2` và sửa `A11` + §8.3 thành 79 ô,
   nhưng **bỏ sót** ô `A6`: nó vẫn ghi 6 dạng · khối A 11×6 = 66 · tổng 68 — tức số của ma trận theo HỌ
   bản đầu `576774b` (r5 gọi nó là ma trận r2 ⟦r5:100 #37b637f2|ma trận r2 không phân biệt nổi⟧ — SAI, r6 sửa; xem §0.5).
   AST head `34cb21f`: `LOP=11`, `DOI_SO=7` ⇒ 77 + 1 + 1 = **79**. r5 sửa `A6` về 79.
2. **`A6` — phản chứng.** r3/r4 khai (diễn ý, không trích) rằng bỏ dạng `khong_doi_so` phải làm `m14` sống lại — nguồn ⟦r3:197 #b2abee10|phải làm m3/m13/m14 SỐNG LẠI⟧. Reviewer đo
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

   ⇒ lời khai ấy của r3/r4 (⟦r3:197 #b2abee10|phải làm m3/m13/m14 SỐNG LẠI⟧) **SAI VỀ NGUYÊN LÝ**, không chỉ vì dạng thứ
   bảy: rút cả hai dạng `m14` vẫn đỏ. Trục DẠNG ĐỐI SỐ **không có** phản chứng hồi sinh nào đo được;
   phản chứng THẬT của nó là **TÁCH `m10` khỏi `m14`** — đúng lý do r3 thêm dạng thứ bảy. Số cô lập
   `34`/`31`/`7`/`4` khớp **đúng** số toàn suite của reviewer. r5 thay phản chứng trong `A6`.
3. **`A11` — phạm vi.** r3/r4 đòi toàn bộ bộ hồi quy lịch sử `m1`–`m14` (⟦r3:198 #d0619027|TOÀN BỘ bộ hồi quy lịch sử⟧). Quét cả bốn bản
   `r1`–`r4`: **không bản nào định nghĩa `m1` `m2` `m4` `m5` `m6` `m8`**; §8.4 định nghĩa đúng TÁM.
   Đọc các verdict trên PR #588 cho thấy vì sao: nhãn `mN` là nhãn **THEO TỪNG LƯỢT** và bị dùng lại
   với nghĩa khác — comment `5758435757` có `m1`–`m5` (`m5` = nới containment riêng nhánh tên trần);
   `5758802877` có `m2`–`m9` qua `scratch/target.py`; `5761292277` có `m1`–`m11` *"giết thật"* ⟦nguon:verdict⟧;
   `5763021895` nói *"giữ TRỌN bộ hồi quy `m1`–`m11`"* ⟦nguon:verdict⟧. Định nghĩa nằm trong scratchpad đã mất.
   ⇒ `A11` như r4 viết **không thoả mãn được bởi bất kỳ ai**, và reviewer lượt 24-09 đã đúng khi
   **từ chối** khai rằng 14/14 còn bị bắt. r5 thu `A11` về **tám** đột biến có định nghĩa, và đặt
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
suýt lặp nó ngay trong lúc soạn r5: §9 của bản NHÁP r5 ghi §7 có mười mục, mà r5 thêm hai mục vào §7 —
đã sửa thành mười hai. **Khi sửa một con số, tìm mọi câu đếm thứ mình vừa đổi.**

### 0.5 — Vì sao có revision 6

Cross-review codex lượt 2 (24-09, `gpt-6-astra` effort `medium`) trên head `cf465b2` theo thước r5:
`changes_requested`, **P1 0 · P2 0 · P3 1**. F1a, F1b, F1c của lượt 1 **ĐÓNG**; `A11` đo TRỌN phạm vi
r5 (tám định nghĩa Phụ lục A tái tạo đúng từng byte, 8 lượt toàn suite, 28/28 cặp TẬP khác nhau). Lớp
`loi-khai-rong-hon-phep-do` **chưa đóng** vì một biểu hiện mới, **F1d**, và nó do CHÍNH r5 đưa vào.
Chủ kho đã cho phép: *"mở r6 nếu cần"* ⟦nguon:chi-thi⟧.

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
tiêu đề và thân §8.5). r6 sửa nhãn ở cả sáu chỗ và đánh dấu tại chỗ rằng bản trước gọi nó là ma
trận r2 ⟦r5:100 #37b637f2|ma trận r2 không phân biệt nổi⟧. Các chỗ nhắc "r2" khác trong tệp nói đúng về ma trận đại diện 4×3 và **giữ nguyên**.
*(r7: câu vừa rồi RỘNG HƠN phép đo — hai câu giải thích trong thân §8.5 vẫn gán cấu trúc của
`576774b` cho r2, và §8.3 trích r2 bằng một câu không có trong r2. Xem §0.6.)*

**Việc của executor, trong `write_set`:** chú thích `scripts/tl_selftest.py:25326` ghi bộ tương
đương m10/m14 thuộc *"ma trận r2/r3-bản-đầu"* ⟦nguon:ma⟧. Phép đo chỉ có trên ma trận sáu dạng `576774b`;
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
hạng đúng"* ⟦nguon:doctrine⟧ — áp y hệt cho nhãn: **một con số đúng không chứng minh nhãn gắn với nó đúng.**

### 0.6 — Vì sao có revision 7

Cross-review codex lượt 3 (24-09, `gpt-6-astra` effort `medium`) trên head `aff0089` theo thước r6:
`changes_requested`, **P1 0 · P2 0 · P3 1**. F1a, F1b, F1c **ĐÓNG**; `A11` đo TRỌN (8/8 định nghĩa
Phụ lục A bằng byte, 8 lượt toàn suite, 28/28 cặp TẬP khác nhau); mã head **không có finding**. Lớp
`loi-khai-rong-hon-phep-do` **chưa đóng**: F1d còn hai câu trong thân §8.5, và câu của r6 ở ⟦r6:211 #29350ea3|khác trong tệp nói đúng⟧
mà r6 thêm vào §0.5 bị chính hai câu ấy bác.
Chủ kho đã cho phép, trả lời đề nghị đẩy spec r7 và cấp lease g7 cho #574 (24-09): *"Đồng ý cả
2. Làm đi"* ⟦nguon:chi-thi⟧.

**Hai câu reviewer chỉ, sửa ở r7:**
- §8.5, đoạn so cơ chế `m10`/`m14`: câu ⟦r6:522 #79173d92|không phân biệt nổi⟧ → ma trận sáu dạng
  `576774b`. Đo bằng `ast` trên blob Git: r2 (`5b1772d`) có `LOP` 4 × `TD` 3 — **không** có trục `DOI_SO`.
- §8.5, đoạn ⟦r6:525 #8440d2a1|Chỗ tách chúng⟧: câu ⟦r6:527 #e223594b|Trục DOI_SO của r2 có⟧ → trục `DOI_SO` của `576774b`.
  Trục thông điệp của r2 là `TD = (goc, khac, rong)`; `DOI_SO` và `hai_doi_so` xuất hiện từ `576774b`.

**Chỗ THỨ BA, không reviewer nào nêu — tìm ra khi quét:** §8.3 viết câu ⟦r3:317 #5253fa78|một cài đặt sai theo bất kỳ chiều nào⟧, đặt
một câu diễn ý trong ngoặc như trích NGUYÊN VĂN của r2. Câu ấy
**không có trong r2** (tìm chuỗi trên blob r2 ⇒ 0 lần; có trong r3–r6, tức nó sinh ra ở r3). Câu thật
của r2: ⟦r2:67 #a64cff8f|dù nó sai theo chiều nào⟧. Nghĩa
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

**Cùng lớp:** bộ đếm `LOI-KHAI-RONG-HON-PHEP-DO` **12 → 13** — lần này do chính lời khai quét
đủ của r6 (⟦r6:211 #29350ea3|khác trong tệp nói đúng⟧). Bài học, nói cho hẹp: sửa NHÃN ở những chỗ đã chỉ không phải là quét; quét là liệt kê
bằng máy rồi phân loại từng dòng, và khai rõ phép liệt kê ấy mù ở đâu.

### 0.7 — Vì sao có revision 8

Cross-review codex lượt 4 (25-09, `gpt-6-astra` medium) trên head `aff0089` theo thước r7: `changes_requested`,
**P1 0 · P2 0 · P3 1** — F1d tiếp diễn: §6 vẫn trích r2 bằng câu diễn ý đặt trong ngoặc như nguyên văn, và
docstring `scripts/tl_selftest.py` mang đúng câu ấy. Lời khai quét đủ của r7 §0.6 (⟦r7:258 #c9c048b4|còn lại khớp⟧) SAI. Chủ kho duyệt mở r8
+ lease mới, với điều kiện quét BẰNG MÁY (25-09: *"Mở r8 + g8, quét bằng máy"* ⟦nguon:chi-thi⟧).

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
| 211, 216 | lời của r5 / chú thích mã cũ (⟦r7:210-211 #ab320aa1|ma trận r2⟧, ⟦r7:216 #dc9ac47f|ma trận r2/r3-bản-đầu⟧) *(r12 sửa con trỏ đầu: r11 trỏ `r7:211` với mảnh của câu kế tiếp — lời r6; lượt 7 F1d(a), §0.11)* | trích bản KHÁC, không gán cho r2 — đúng |
| 243, 245 ×2 | các câu của r6 mà §0.6 dẫn lại | trích r6 — đúng |
| 567 ×2 | mảnh do ngoặc lồng trong ghi chú r7 tự thêm | tạo tác của regex — không phải trích dẫn |
| **376** | ⟦r7:376 #7a9efbc1|BẤT KỲ CHIỀU NÀO⟧ | **GÁN SAI cho r2** — r8 sửa |
| **538** | ⟦r7:538 #eb2d15f9|bốn ô ĐẦU TIÊN khác nhau⟧ | **GÁN SAI cho r2** (r2 chỉ có tiêu đề cột ⟦r2:286 #38bd7f77|ô đỏ ĐẦU TIÊN⟧, không có câu này) — r8 sửa |

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
`r2` ở tiêu đề bảng cách ba dòng, ngoài cửa sổ hai dòng. Chủ kho duyệt (25-09): *"Mở r9 + g9, quét theo ngữ cảnh"* ⟦nguon:chi-thi⟧.

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
| 100, 136, 210, 216, 243, 245 ×2, 590, 600 *(r9 ghi ×3 — sai, bộ quét chỉ ra hai chuỗi ở dòng 245; r10 sửa, §0.9)* | chữ của r3–r6 (nhãn *ma trận r2* sai và các câu §8.5) được dẫn lại để nói bản trước ghi sai | trích bản KHÁC — đúng |
| 138 | lời khai của r3/r4 | *(r9 phán trích r3/r4 — đúng: SAI, đó là câu DIỄN Ý rút gọn; r10 thay bằng con trỏ, §0.9)* |
| 237, 239 ×2, 248, 274, 275, 291 ×2, 294, 295 | chữ của r7/r8 và chỉ thị chủ kho, dẫn lại khi MÔ TẢ lỗi cũ | trích bản KHÁC / chỉ thị — đúng |
| 401, 402, 403, 606 ×2 | mảnh do dấu nháy trong ô bảng / ngoặc lồng ghép sai cặp | tạo tác của regex — không phải lời trích |
| 537 | cụm của CHÍNH r3 (⟦r3:323-324 #e70e42b5|mọi cài đặt sai có thể viết bằng Python⟧): phạm vi ma trận KHÔNG phủ | cách nói của r3 — đúng *(r10 trỏ dòng 322 — sai span, cụm ở 323–324; r11 sửa, §0.10)* |
| 577 | ghi chú r8 mô tả cụm gán sai cũ | mô tả lỗi cũ — đúng |
| 584 | luật của kho (*so TẬP, đừng so SỐ ĐẾM*) | trích doctrine — đúng |
| 598, 599 | hằng chuỗi trong mã | mã — không phải lời trích |

**Và một chỗ NGOÀI đặc tả mà bộ quét mới bắt được** — nên phải khai: docstring `scripts/tl_selftest.py` ở
`677ef37` đặt cụm *mọi cài đặt sai có thể viết bằng Python* (cách nói của r3 — r9 ghi §8.4, SAI; nguồn thật là §8.3 ⟦r3:323-324 #e70e42b5|mọi cài đặt sai có thể viết bằng Python⟧, r10 sửa) trong ngoặc kép, NGAY sau câu
*"r2 đã khai quá rộng đúng chỗ này"* ⟦nguon:ma⟧ — đọc như lời r2. Không reviewer nào nêu; bộ quét r9 gắn cờ. Mã head
`19f2141` bỏ dấu trích và ghi nguồn; `RELEASE_MANIFEST.json` tái sinh (strict 180/180).

**Chạy lại cùng bộ quét trên CHÍNH r9:** 46 chuỗi — 13 `KHỚP_R2` (12 cũ + dòng 99 nay trích đúng mảnh), 33
`KHÔNG_KHỚP` = 30 chuỗi của bảng trên (bỏ dòng 99; số dòng dịch) + 3 chuỗi do CHÍNH mục này thêm: chỉ thị chủ kho,
cụm *r3 khai lại* ở bảng trên, và câu của docstring được dẫn lại ngay trên. *(r10: câu sau SAI — lượt 6 đo ra dòng 138 và dòng 245 phân loại tay sai; §0.9.)* Không chuỗi nào gán sai cho r2 —
trong MIỀN của bộ quét (xem giới hạn).

**Giới hạn, khai thẳng:** bộ quét chỉ thấy lời gán cho r2 khi token `r2` nằm trong CÙNG khối hoặc tiêu đề gần
nhất. Một lời gán qua đại từ (*"bản ấy"*), qua tham chiếu mục ở khối khác, hoặc dùng ngoặc đơn / in nghiêng không
ngoặc thì nó KHÔNG thấy. Phân loại `KHÔNG_KHỚP` là việc của người đọc, không phải của máy — bảng trên là phán
của phiên soạn r9, reviewer phải đo lại.

**Không đổi ở r9:** mọi số hạng, phép đo, `A6`, `A11`, Phụ lục A, Phụ lục B (giữ làm lịch sử), §7, §9,
`write_set`. Mã head đổi DUY NHẤT một docstring (`scripts/tl_selftest.py`, bỏ dấu trích cụm của r3) và manifest
tái sinh theo.

### 0.9 — Vì sao có revision 10: ĐỔI KIẾN TRÚC, không vá lần thứ bảy

Cross-review lượt 6 trên head `19f2141` theo r9 **không trọn**: reviewer codex hết hạn mức giữa lượt (`ma_thoat=1`,
1554s). Checkpoint nó để lại vẫn có phép đo tái hiện được: F1d `loi-khai-rong-hon-phep-do`, P3, **ba biểu hiện mới**:

- (a) r9 §0.8 và docstring `19f2141` gán cụm của r3 cho **§8.4**; nguồn thật là **§8.3** — lỗi của chính phiên soạn r9.
- (b) bảng phân loại tay §0.8 kê dòng 245 **×3**; bộ quét chỉ ra **hai** chuỗi ở dòng ấy.
- (c) bảng tay phán dòng 138 là trích r3/r4 đúng; nó là một câu **diễn ý rút gọn** đặt trong ngoặc.

**Lần THỨ SÁU cùng hình dạng** (r5 → r6 → r7 → r8 → r9 → lượt 6). Lease tự khai: lặp lần thứ BA thì DỪNG và hỏi có nên
làm việc này theo cách này không. Đã hỏi (`issues/574#issuecomment-5825742786`); chủ kho chọn **đổi kiến trúc** — phương
án executor đề xuất, chuyển qua phiên điều phối (25-09). Lý lẽ: sáu lần vá theo danh sách đều ĐÚNG và đều HẸP; lớp lỗi chỉ
chết khi không còn lời gán viết tay để lệch.

**Kiến trúc r10:**

1. **Lời của một revision KHÁC không còn được đặt trong ngoặc.** Nó được dẫn bằng **CON TRỎ** `⟦rN:L #h⟧` (hoặc
   `⟦rN:L-M #h⟧`): dòng `L` (tới `M`) của đặc tả revision `N`, và `h` là 8 hex đầu của sha256 nội dung các dòng ấy sau chuẩn
   hoá khoảng trắng. Con trỏ do MÁY sinh (`con_tro.py sinh`), không gõ tay. Trỏ sai dòng thì `h` lệch và cổng ĐỎ.
   Cần nói ý của câu thì viết DIỄN Ý, không ngoặc, cạnh con trỏ.
2. **Mọi chuỗi trong ngoặc kép còn lại** (thẳng hoặc cong, ≥ 8 ký tự, vắt nhiều dòng được) nằm trong một khối có nhắc
   một revision thì PHẢI mang **nhãn nguồn** `⟦nguon:K⟧` với `K` thuộc `chi-thi` · `verdict` · `commit` · `ma` ·
   `doctrine` · `issue` — tức chuỗi ấy KHÔNG phải lời của một revision. Thiếu nhãn là `VI_PHAM` và cổng ĐỎ.
3. **Cổng** `con_tro.py kiem` (Phụ lục D, nguyên văn) in số con trỏ theo BA trạng thái — `DUNG` · `LECH` ·
   `KHONG_DO_DUOC` (thiếu tệp nguồn) — cộng `VI_PHAM` và `CO_NHAN`; `rc=0` CHỈ khi `LECH = VI_PHAM = KHONG_DO_DUOC = 0`.
   Tệp `.py` được đọc qua `ast` (hằng chuỗi > 40 ký tự), giới hạn bằng `--ham` vào đúng ba hàm write set cho sửa.
4. **Cổng phải ĐỎ được — đo, không suy.** `con_tro.py tu-kiem` dựng nguồn tạm và tám ca: con trỏ đúng (phải qua) ·
   trỏ SAI dòng · trỏ NGOÀI phạm vi · thiếu tệp nguồn · trích KHÔNG nhãn · trích vắt dòng không nhãn (năm ca phải ĐỎ) ·
   trích CÓ nhãn · chuỗi trong mã inline (phải qua). Kết quả: `TU_KIEM DAT 8/8`. Và trên CHÍNH tệp này: hai ca âm dựng trên BẢN SAO của r10 — đổi `⟦r2:67 …⟧` thành dòng 68 giữ nguyên băm ⇒ `LECH 1`, `rc=1`; chèn một câu trong ngoặc không nhãn vào một khối có nhắc r2 ⇒ `VI_PHAM 1`, `rc=1`.

**Phép đo — tệp nguồn là chín revision `r1`…`r9` lấy từ blob `364686e`:**

| tệp | `DUNG` | `LECH` | `KHONG_DO_DUOC` | `VI_PHAM` | `CO_NHAN` | `rc` |
|---|---:|---:|---:|---:|---:|---:|
| r9 (`7caffe2e…`), trước khi đổi | 0 | 0 | 0 | **59** | 0 | 1 |
| **r10** | **33** | 0 | 0 | **0** | 19 | **0** |
| docstring `19f2141` (`--ham` ba hàm) | 0 | 0 | 0 | 1 | 0 | 1 |
| **docstring `d52a79a`** (`--ham` ba hàm) | **2** | 0 | 0 | **0** | 0 | **0** |

Trên r9 bộ quét tìm 83 chuỗi trong ngoặc toàn tệp, 68 trong khối có nhắc revision; bỏ phần nằm trong mã inline (giữa
hai dấu backtick — mã, không phải lời trích) còn **59**. Mỗi chỗ được xử bằng một trong ba cách: thay bằng con trỏ
(lời của một revision), gắn nhãn nguồn (chỉ thị, verdict, doctrine, Issue, mã), hoặc bỏ ngoặc (cụm tự đặt của chính
tệp, không phải lời trích của ai). Số ở bảng là số MÁY đếm trên r10: 33 con trỏ, 19 chuỗi có nhãn. **Không có** phép
đếm tách 59 chỗ theo ba cách — 33 + 19 không bằng 59 vì có con trỏ được THÊM cạnh một câu diễn ý vốn không có ngoặc,
và một bảng tay chia 59 chỗ chính là loại lời khai đã sai ở lượt 6. `rc` đọc TRỰC TIẾP, không qua pipe.

**PHẠM VI — phần nào đã bịt, phần nào còn hở, khai thẳng để lần thứ bảy không bị tính là đã đóng:**

- **Bịt:** mọi lời của revision khác mà tệp này DẪN bằng con trỏ — máy kiểm đúng DÒNG và đúng NỘI DUNG dòng ấy.
- **Bịt:** mọi chuỗi trong ngoặc kép, trong khối có nhắc revision, mà KHÔNG mang nhãn — máy bắt.
- **CÒN HỞ — diễn ý cạnh con trỏ:** câu viết tay nói con trỏ ấy có ý gì thì máy KHÔNG kiểm. Một diễn ý sai nghĩa vẫn
  qua cổng; người đọc phải mở dòng nguồn.
- **CÒN HỞ — chuỗi có nhãn:** nhãn nói chuỗi KHÔNG phải lời revision; máy KHÔNG kiểm chuỗi có đúng với chỉ thị, verdict,
  commit, doctrine hay Issue được nhãn chỉ ra không. Gắn nhãn sai loại để lách luật cũng qua.
- **CÒN HỞ — gán nguồn không dùng ngoặc kép:** in nghiêng không ngoặc, ngoặc đơn, hay đại từ (bản ấy, câu kia) ở khối
  khác — máy KHÔNG thấy.
- **CÒN HỞ — khối không nhắc revision:** chuỗi trong ngoặc ở khối không có token `rN` nằm ngoài luật.
- **Ngoài write set:** `_c378_phan_hang_tin_dung_gia` có một nhãn mã trong ngoặc (`r378-mutant-vo-can`) — không phải lời
  trích, và hàm ấy KHÔNG thuộc phạm vi lease cho sửa; không chạm.
- **Lịch sử:** Phụ lục B (script r8) và Phụ lục C (bộ quét r9) giữ nguyên làm lịch sử; các số đếm ở §0.7, §0.8 là số của
  bộ quét cũ trên bản cũ.

**Mã head** `d52a79a`: docstring `_c378_ma_tran_phan_hang` thay lời r2 và cụm của r3 bằng hai con trỏ (sửa luôn §8.4 →
§8.3); `RELEASE_MANIFEST.json` tái sinh. selftest 1715/1715, release-verify strict ok 180/180, golden `rc=0`.

**Không đổi ở r10:** mọi số hạng, phép đo, `A6`, `A11`, Phụ lục A, §7, §9, `write_set`, điều kiện dừng.

**Reviewer:** chỉ thị chủ kho 25-09 đổi sang reviewer CÙNG nhà cung cấp, effort/mô hình cao hơn (codex hết hạn mức tới
2026-09-28). Lượt ấy KHÔNG tạo ra `cross_approved`; nó đạt tối đa `advisory_review`. Quyền land vẫn là `human_audited`.

### 0.10 — Vì sao có revision 11: con trỏ mang MẢNH NEO, bộ tự kiểm đếm CHÍNH XÁC

Cross-review lượt 6, chạy lại trọn bằng codex (`gpt-6-astra` medium, 2347s, `ma_thoat=0`) trên head `d52a79a` theo r10:
`changes_requested`, **P1 0 · P2 1 · P3 1**. F1a, F1b, F1c, A11 ĐÓNG; ba biểu hiện F1d của checkpoint trước ĐÓNG tại chỗ.

- **F2 (P2) `tu-kiem-con-tro-thieu-truc-dau-vao`:** tám ca tự kiểm của r10 chỉ dùng `.md` và đặt token revision ngay trong
  thân đoạn. Đột biến CÔNG CỤ cho nhánh đọc `.py` trả rỗng, hoặc bỏ ngữ cảnh tiêu đề, vẫn cho 8/8 — và trên văn bản có sẵn
  thì chuyển đỏ thành xanh.
- **F1d (P3), biểu hiện mới:** bảng §0.8 hàng 537 trỏ dòng 322 của r3 cho một cụm nằm ở 323–324. Con trỏ ĐÚNG băm của
  dòng nó trỏ — chỉ là người chọn sai dòng. Đây đúng là lỗ diễn ý cạnh con trỏ mà §0.9 đã tự khai, nay có hậu quả đo được.

Lần thứ BẢY cùng họ lời gán nguồn. Theo lease, phiên executor dừng và hỏi; chủ kho duyệt đề xuất (25-09, trực tiếp trong
phiên executor): *"Đồng ý"* ⟦nguon:chi-thi⟧ — đề xuất ấy là: bổ sung ca tự kiểm cho `.py`/tiêu đề, và mỗi con trỏ mang một
mảnh chữ lấy từ chính dòng nguồn, máy kiểm mảnh có nằm trong dòng được trỏ.

**Đổi ở r11 (công cụ Phụ lục E, nguyên văn; Phụ lục D giữ làm lịch sử):**

1. **Con trỏ** `⟦rN:L #h|mảnh⟧`: `mảnh` BẮT BUỘC, ≥ 6 ký tự, là cụm mà câu dẫn con trỏ đang nói tới; nó phải NẰM TRONG các
   dòng được trỏ (so sau khi bỏ dấu nhấn `*` và dấu backtick, gộp khoảng trắng). Thiếu mảnh là `VI_PHAM`; mảnh không nằm trong
   dòng là `LECH`. `sinh` từ chối sinh con trỏ khi mảnh không có trong dòng — con trỏ vẫn do MÁY sinh.
2. **Tự kiểm có BỘ ĐẾM KỲ VỌNG chính xác** cho từng ca (`DUNG`, `LECH`, `KHONG_DO_DUOC`, `VI_PHAM`, `CO_NHAN`), không chỉ
   đạt/không đạt; 15 ca, phủ: con trỏ đúng · sai dòng · ngoài phạm vi · thiếu tệp nguồn · sai băm mà mảnh vẫn khớp · sai mảnh
   mà đúng băm · thiếu mảnh · trích không nhãn · trích có nhãn · vắt dòng · trong mã inline · token chỉ ở TIÊU ĐỀ · dòng bắt đầu
   bằng `#` mà không phải tiêu đề · docstring `.py` · `.py` với `--ham`. Kết quả `TU_KIEM DAT 15/15`.
3. **Tiêu đề Markdown** là dòng khớp `#{1,6}` + khoảng trắng; dòng như `#574 viết …` không còn bị coi là tiêu đề (reviewer lượt 6
   ghi nhận, không có hậu quả trên văn bản đã đo; nay có ca riêng).

**Đo, không suy — tệp nguồn là r1…r9 (blob `364686e`):**

| đầu vào | `DUNG` | `LECH` | `KHONG_DO_DUOC` | `VI_PHAM` | `CO_NHAN` | `rc` |
|---|---:|---:|---:|---:|---:|---:|
| **r11 (tệp này)** | **33** | 0 | 0 | **0** | 19 | **0** |
| r10 dưới công cụ r11 (con trỏ chưa có mảnh) | 0 | 0 | 0 | 33 | 19 | 1 |
| bản sao r11, con trỏ hàng 537 đưa về dòng 322 với ĐÚNG băm dòng 322, giữ mảnh | 32 | **1** | 0 | 0 | 19 | 1 |
| docstring `76f199e` (`--ham` ba hàm write set) | **2** | 0 | 0 | **0** | 0 | **0** |

Hàng thứ ba là CHÍNH ca F1d của lượt 6: công cụ r10 cho nó qua (băm đúng), công cụ r11 bắt `LECH`.

**Đột biến CÔNG CỤ, mỗi cái một bản sao, chạy `tu-kiem`** (hai cái đầu là hai đột biến F2 của reviewer):

| đột biến | kết quả |
|---|---|
| nhánh `.py` trả rỗng | ĐỎ — `py_docstring`, `py_ham` |
| bỏ ngữ cảnh tiêu đề | ĐỎ — `chi_tieu_de` |
| bỏ kiểm băm | ĐỎ — `sai_bam_manh_van_khop` |
| bỏ kiểm mảnh | ĐỎ — `sai_manh_dung_bam` |
| mảnh thành tuỳ chọn | ĐỎ — `thieu_manh` |
| bỏ tăng `VI_PHAM` | ĐỎ — nhiều ca trích |
| bỏ báo thiếu tệp | ĐỎ — `thieu_tep` |
| nhận tiêu đề bằng `startswith("#")` | ĐỎ — `gach_so_khong_phai_tieu_de` |
| bỏ `--ham` | ĐỎ — `py_ham` |
| bỏ che mã inline | ĐỎ — `trong_code` |
| bỏ báo ngoài phạm vi | **SỐNG — KHÔNG tương đương** *(r12 sửa: r11 xếp là tương đương vì tưởng lát cắt ngoài phạm vi cho chuỗi rỗng; sai với span vượt CUỐI tệp — `L[0:999]` là cả tệp. Lượt 7 F1d(b), §0.11; công cụ v3 bắt nó)* |

**PHẠM VI — phần bịt thêm, phần vẫn hở:**

- **Bịt thêm:** con trỏ đúng băm mà sai dòng CẦN trỏ — khi câu dẫn nói tới một cụm có trong dòng đúng mà không có trong dòng
  bị trỏ nhầm.
- **VẪN HỞ — mảnh do người chọn:** máy kiểm mảnh NẰM TRONG dòng được trỏ, không kiểm mảnh có đúng là cụm câu dẫn đang nói tới.
  Chọn một mảnh có mặt ở dòng sai thì vẫn qua.
- **VẪN HỞ — diễn ý:** câu viết tay nói ý của dòng nguồn thì máy không kiểm nghĩa.
- **VẪN HỞ** như §0.9: chuỗi có nhãn không được kiểm nội dung; gán nguồn không dùng ngoặc kép; khối không nhắc revision.

**Mã head** `76f199e` (đã hoà master `4c53c76` — không chạm write set): docstring dùng hai con trỏ có mảnh; manifest tái sinh.
selftest 1715/1715, release-verify strict ok 180/180, golden `rc=0`.

**Không đổi ở r11:** mọi số hạng, phép đo, `A6`, `A11`, Phụ lục A–D, §7, §9, `write_set`, điều kiện dừng.

### 0.11 — Vì sao có revision 12: tự kiểm theo TRỤC ĐẦU VÀO, sửa một con trỏ chọn sai mảnh, rút một lời khai tương đương

Cross-review lượt 7 (codex `gpt-6-astra` medium, run `7c8942cb`, `ma_thoat=0`) trên head `76f199e` theo r11: `blocked`,
**P1 0 · P2 1 · P3 2**. Mã POSIX, `A11` (8/8, 28/28 tập khác nhau) và manifest (180/180) đạt trong miền đã đo; hai finding
lượt 6 đóng tại chỗ nhưng **chưa đóng cấp lớp**. Nguồn của r12 — chủ kho 25-09-2026, trả lời đề xuất sau lượt 7, bản chiếu
`issues/574#issuecomment-5831890944`: *"Mở r12 + g12 (đề xuất)"* ⟦nguon:chi-thi⟧, giữ hạn `2026-09-26T06:00:00Z`.

- **F2 (P2) `tu-kiem-con-tro-thieu-truc-dau-vao`:** reviewer chạy 22 đột biến công cụ; 11 SỐNG với `TU_KIEM DAT 15/15`, và cả
  11 có phản chứng không tương đương: `no_range`, `no_curly`, `no_label_validation`, `no_min_fragment`, `no_star`, `no_backtick`,
  `no_space`, `no_span`, `no_fence`, `no_table_boundary`, `no_py_split`.
- **F1d (P3) `loi-khai-rong-hon-phep-do`, hai biểu hiện:** (a) bảng §0.7 hàng r7 211 trỏ `r7:211` với mảnh của câu KẾ TIẾP — lời
  quét của r6 — trong khi chuỗi đang được phân loại là nhãn ma trận r2 vắt qua r7:210–211; (b) §0.10 xếp đột biến bỏ kiểm phạm vi
  là tương đương. Sai: Python cắt `L[0:999]` thành CẢ tệp chứ không thành rỗng, nên con trỏ `r1:1-999` có băm đúng lát cắt ấy
  được bản đột biến nhận `DUNG`.
- **L1 (P3) `ho-so-lease-thoi-diem-placeholder`:** bia mộ `g10` ghi `da_bi_thay_the_luc` là một chuỗi có `xx` thay cho phút, và
  `g11` ghi `write_set_do_luc_cap.do_luc` cùng dạng. Cả hai không parse được. Sửa ở hồ sơ lease (mục L1 dưới), không ở mã.

**Đổi ở r12:**

1. **Công cụ con trỏ v3 — Phụ lục F, nguyên văn** (Phụ lục E giữ làm lịch sử). Chỉ `tu_kiem` đổi; `kiem`, `sinh`, `tim` và cú
   pháp con trỏ GIỮ NGUYÊN byte. Thêm một BẢNG LỚP ĐẦU VÀO, mỗi trục một cặp âm/dương, con trỏ VIẾT SẴN với băm tính độc lập
   (`hashlib` trên chuỗi đã chuẩn hoá bằng tay) — oracle không đi qua `sinh`/`bam`, tức không qua hàm đang bị đột biến. Thêm
   nguồn thứ hai `r2.md` cho các trục dấu markup. Giữ nguyên 15 ca cũ.

| trục | ca âm (phải đỏ ở đột biến) | ca dương / đối chứng |
|---|---|---|
| phạm vi dòng | cuối vượt TOÀN tệp `1-999` · cuối vượt một phần `2-9` · đầu `0` · đảo `3-2` — cả bốn `LECH` | một dòng `r1:2` → `DUNG` |
| span nhiều dòng | — | `r1:2-3`, mảnh vắt qua ranh hai dòng → `DUNG` |
| kiểu ngoặc | ngoặc cong không nhãn → `VI_PHAM` | ngoặc cong có nhãn → `CO_NHAN` |
| nhãn nguồn | nhãn ngoài danh sách cho phép → `VI_PHAM` | nhãn hợp lệ (ca cũ `trich_co_nhan`) |
| độ dài mảnh | mảnh 4 ký tự → `VI_PHAM` | mảnh đúng 6 ký tự → `DUNG` |
| dấu markup trong nguồn | — | bỏ `*` · bỏ backtick · gộp khoảng trắng đôi: mỗi cái → `DUNG` |
| rào mã Markdown | chuỗi SAU rào, khối nhắc `r1` → `VI_PHAM` | chuỗi TRONG rào, kể cả dòng nhắc `r1` → 0 |
| biên bảng | hàng bảng tự nhắc `r1` → `VI_PHAM` | hàng bảng không nhắc bản nào, đứng sau đoạn nhắc `r1` → 0 |
| đoạn docstring `.py` | (ca cũ `py_docstring`) | đoạn hai không nhắc bản nào, đoạn một nhắc `r1` → 0 |

2. **Đo, không suy — `tu-kiem`: `TU_KIEM DAT 34/34`.** 23 đột biến công cụ, mỗi cái một bản sao, một tiến trình, chạy `tu-kiem`:
   11 đột biến sống của lượt 7, 11 đột biến của §0.10 (kể cả đột biến bỏ báo ngoài phạm vi, nay xếp KHÔNG tương đương), và
   `no_fence_toan_bo` (gỡ hẳn xử lý rào). **Cả 23 ĐỎ**, mỗi cái chỉ tên ca đỏ. Cùng bộ đột biến trên công cụ r11: đúng 11 đột
   biến của lượt 7 cho `TU_KIEM DAT 15/15` — tái lập bảng của reviewer.

| đột biến (lượt 7) | ca đỏ ở v3 |
|---|---|
| `no_range` | `pv_cuoi_vuot_toan_tep`, `pv_cuoi_vuot_mot_phan` |
| `no_curly` | `ngoac_cong_am`, `ngoac_cong_co_nhan` |
| `no_label_validation` | `nhan_khong_hop_le` |
| `no_min_fragment` | `manh_4_am` |
| `no_star` · `no_backtick` · `no_space` | `manh_bo_sao` · `manh_bo_backtick` · `manh_gop_khoang_trang` |
| `no_span` | `span_nhieu_dong_duong` |
| `no_fence` · `no_fence_toan_bo` | `rao_code_bo_qua` |
| `no_table_boundary` | `bang_tach_khoi_doan` |
| `no_py_split` | `py_tach_doan` |

3. **F1d(a) — sửa con trỏ tại chỗ** ở bảng §0.7: hàng r7 211 nay trỏ span `r7:210-211` với mảnh là chính chuỗi đang phân loại.
   Inventory của hàng ấy và các hàng cùng bảng (đối tượng → mảnh → dòng nguồn → revision xuất hiện đầu, đo bằng `tim`):

| đối tượng phân loại | mảnh | dòng nguồn | câu nguồn xuất hiện đầu (đo bằng `tim`) |
|---|---|---|---|
| nhãn ma trận r2 do r5 gán, r6 đánh dấu | `ma trận r2` | `r7:210-211` (vắt dòng) | câu dẫn của r6 ở `r6:210-211` |
| chú thích mã cũ | `ma trận r2/r3-bản-đầu` | `r7:216` | `r6:214` |
| câu gán sai cho r2 (r8 sửa) | `BẤT KỲ CHIỀU NÀO` | `r7:376` | `r3:210` |
| câu gán sai cho r2 (r8 sửa) | `bốn ô ĐẦU TIÊN khác nhau` | `r7:538` | `r3:363` |
| tiêu đề cột thật của r2 | `ô đỏ ĐẦU TIÊN` | `r2:286` | `r2:286` |

   Mảnh cũ của hàng r7 211 — cụm lời quét của r6 — xuất hiện đầu ở `r6:211`, tức là lời r6 chứ không phải lời r5: đúng điều
   reviewer đo. Máy VẪN không kiểm mảnh có phải đúng cụm câu dẫn nói tới (§0.10, VẪN HỞ); inventory trên là phép đo tay có ghi
   lệnh, không phải cổng.
4. **F1d(b) — rút lời khai tương đương** ở bảng đột biến của §0.10, đánh dấu tại chỗ. Ca `pv_cuoi_vuot_toan_tep` là chính phản
   chứng của reviewer, đưa vào `tu-kiem`.

**L1 — hồ sơ lease, không phải đặc tả.** `g12` ghi thời điểm THẬT, lấy từ lệnh `date -u` lúc đo và từ commit bền. Hai trường
placeholder của `g10`/`g11` được sửa trong chính tệp lease: giá trị là committer date của commit chứa sự kiện (tạo bia mộ,
tạo lease), kèm trường ghi NGUỒN của thời điểm ấy. Đó là cận trên — phép đo chạy trước commit — và được khai là cận trên,
không phải phút đo thật. Không đổi liên kết hai chiều, hạn, write set.

**Đo lại cổng con trỏ bằng công cụ v3, nguồn r1…r9 (blob `364686e`), `rc` đọc trực tiếp từ tiến trình:**

| đầu vào | `DUNG` | `LECH` | `KHONG_DO_DUOC` | `VI_PHAM` | `CO_NHAN` | `rc` |
|---|---:|---:|---:|---:|---:|---:|
| **r12 (tệp này)** | **33** | 0 | 0 | **0** | 20 | **0** |
| r11 | 33 | 0 | 0 | 0 | 19 | 0 |
| bản sao r12, hàng r7 211 đưa về con trỏ CŨ của r11 | 33 | 0 | 0 | 0 | 20 | 0 |
| docstring `76f199e` (`--ham` ba hàm write set) | 2 | 0 | 0 | 0 | 0 | 0 |

Hàng thứ ba nói thẳng giới hạn: con trỏ cũ ĐÚNG băm và mảnh có nằm trong dòng, nên máy vẫn nhận nó. F1d(a) được sửa bằng
inventory đo tay ở mục 3, không bằng cổng — đúng lỗ VẪN HỞ mà §0.10 đã khai. Công cụ v3 và v2 bằng byte ngoài `tu_kiem`
(so bằng `ast` theo từng hàm và so phần văn bản trước/sau hàm).

**Mã:** không đổi — head vẫn `76f199e`, không đẩy gì lên #588.

**Không đổi ở r12:** mọi số hạng, `A6`, `A11`, Phụ lục A–E, §7, §9, `write_set`, điều kiện dừng, hạn.

### 0.12 — Vì sao có revision 13: tự kiểm theo MIỀN HỮU HẠN của cú pháp, và qua đường CLI thật

Cross-review lượt 8 (codex `gpt-6-astra` medium) trên head `76f199e` theo r12: `blocked`, **P1 0 · P2 1 · P3 0 · P4 0**.
F1d và L1 của lượt 7 ĐÓNG; 11 đột biến cũ của F2 đỏ đúng ca trên công cụ v3. Nguồn của r13 — chủ kho 25-09-2026, trong
phiên điều phối, bản chiếu `issues/574#issuecomment-5833730614`: *"Mở r13 + g13 (đề xuất)"* ⟦nguon:chi-thi⟧, giữ hạn
`2026-09-26T06:00:00Z`.

- **F2 (P2) `tu-kiem-con-tro-thieu-truc-dau-vao`, tiếp diễn:** chín đột biến MỚI sống với `TU_KIEM DAT 34/34`:
  `new_rv_no_boundaries`, `new_rv_single_digit`, `new_quote_min9`, `new_cli_ignore_ham`, `new_label_only_two`,
  `new_pointer_single_rev`, `new_pointer_single_line`, `new_heading_h2_only`, `new_fence_literal3`. Nặng nhất:
  `new_pointer_single_line` làm cổng không còn thấy con trỏ nào vào dòng từ 10 trở đi — trên r12 ra `DUNG 0`, `rc=0`;
  `new_cli_ignore_ham` làm hỏng đường `--ham` mà bộ tự kiểm (gọi thẳng `kiem`) không đi qua.

**Đổi ở r13 — công cụ con trỏ v4, Phụ lục G, nguyên văn** (Phụ lục E, F giữ làm lịch sử). Chỉ `tu_kiem` đổi; `kiem`, `sinh`,
`tim`, `main` và mọi biểu thức chính quy GIỮ NGUYÊN byte so với v3 (so phần văn bản trước và sau `tu_kiem`). Thêm nguồn
`r3.md` (12 dòng) và `r12.md`. Bảng MIỀN HỮU HẠN — mỗi ô là một ca có bộ đếm kỳ vọng viết tay, con trỏ có băm tính độc lập:

| trục | các giá trị trong miền |
|---|---|
| số revision trong con trỏ | một chữ số (ca cũ) · hai chữ số `r12:1` → `DUNG` |
| số dòng trong con trỏ | một chữ số (ca cũ) · hai chữ số `r3:12` → `DUNG`; span `r3:10-11` → `DUNG`; `r3:12` sai băm → `LECH` |
| token revision trong văn bản | đứng riêng một chữ số (ca cũ) · đứng riêng hai chữ số `r12` → `VI_PHAM` · nằm trong từ `error1`, `r1x` → 0 |
| độ dài trích | 7 · 8 · 9 ký tự × ngoặc thẳng và ngoặc cong: 7 → 0; 8, 9 → `VI_PHAM` |
| nhãn nguồn | CẢ SÁU nhãn cho phép trong một khối → `CO_NHAN 6`; nhãn ngoài danh sách (ca r12) |
| tiêu đề | `#` đến `######` (sáu ca) → `VI_PHAM`; bảy dấu `#` không phải tiêu đề → 0; `#574` (ca cũ) |
| rào mã | ba backtick có thông tin ngôn ngữ · bốn backtick có thông tin ngôn ngữ → 0 |
| đường CLI thật | tiến trình con qua `main`: `--ham f` → `rc=0`, 0 vi phạm; `--ham f,g` → `rc=1`, 1; không `--ham` → `rc=1`, 1; con trỏ hai chữ số → `rc=0`, `DUNG 1` |

**Đo, không suy (`rc` đọc trực tiếp từ tiến trình):**

- `tu-kiem`: **`TU_KIEM DAT 60/60`** (56 ca gọi `kiem` + 4 ca CLI).
- **32 đột biến công cụ**, mỗi cái một bản sao, một tiến trình: 11 của §0.10, 11 của lượt 7 (kể cả `no_fence_toan_bo`), 9 của
  lượt 8, và `no_range` bản lượt 7. **Cả 32 ĐỎ**, mỗi cái nêu tên ca đỏ. Cùng chín đột biến lượt 8 trên công cụ v3: cả chín
  `34/34`, `rc=0` — tái lập bảng của reviewer.

| đột biến (lượt 8) | ca đỏ ở v4 |
|---|---|
| `new_rv_no_boundaries` | `rv_trong_tu_khong_phai_token` |
| `new_rv_single_digit` | `rv_hai_chu_so_token` |
| `new_quote_min9` | `trich_8_thang`, `trich_8_cong`, … |
| `new_cli_ignore_ham` | `cli_ham_f` |
| `new_label_only_two` | `moi_nhan_hop_le` |
| `new_pointer_single_rev` | `rv_hai_chu_so_con_tro` |
| `new_pointer_single_line` | `dong_hai_chu_so_con_tro`, `span_hai_chu_so`, … |
| `new_heading_h2_only` | `tieu_de_cap_1`, `tieu_de_cap_3` … `tieu_de_cap_6` |
| `new_fence_literal3` | `rao_3_co_thong_tin`, `rao_4_co_thong_tin` |

**Ngưỡng tối thiểu con trỏ khi chạy văn bản thật — CÂN NHẮC và KHÔNG làm ở r13.** Một cổng trả `rc=0` với `DUNG 0` đúng là
đang coi trạng thái không có gì để kiểm là đạt. Nhưng thêm ngưỡng là đổi `kiem`/`main` — tức đổi hành vi cổng, không chỉ bộ tự kiểm —
trong khi r13 cố ý giữ công cụ ngoài `tu_kiem` bằng byte để phạm vi thay đổi đo được. Thay vào đó: (a) ca CLI con trỏ hai
chữ số khoá đúng đường đã sập; (b) mọi phép đo trên văn bản thật trong đặc tả này ghi SỐ `DUNG`, và tiêu chí là **`DUNG 33`
trên đặc tả, `DUNG 2` trên docstring** — không phải `rc=0`. Một phiên bản làm `DUNG` tụt thì phép đo ấy đỏ theo tiêu chí.

**PHẠM VI — miền đã phủ và phần CHƯA đo:** miền trên là hữu hạn và theo cú pháp đã chốt. CHƯA đo: số revision/dòng từ ba
chữ số; trích dài hơn 9 ký tự mà vắt nhiều khối; tiêu đề kiểu gạch dưới (Setext); rào bằng dấu ngã; danh sách lồng; chuỗi
Python f-string và chuỗi nối. Không khai bộ tự kiểm phủ mọi Markdown hay mọi Python.

**Đo lại cổng con trỏ bằng công cụ v4, nguồn r1…r9 (blob `364686e`):** xem bảng cuối mục.

**Mã:** không đổi — head vẫn `76f199e`, không đẩy gì lên #588.

**Không đổi ở r13:** mọi số hạng, `A6`, `A11`, Phụ lục A–F, §7, §9, `write_set`, điều kiện dừng, hạn.

| đầu vào (công cụ v4) | `DUNG` | `LECH` | `KHONG_DO_DUOC` | `VI_PHAM` | `CO_NHAN` | `rc` |
|---|---:|---:|---:|---:|---:|---:|
| **r13 (tệp này)** | **33** | 0 | 0 | **0** | 21 | **0** |
| r12 | 33 | 0 | 0 | 0 | 20 | 0 |
| docstring `76f199e` (`--ham` ba hàm write set) | **2** | 0 | 0 | 0 | 0 | 0 |

### 0.13 — Vì sao có revision 14: ma trận hợp đồng CLI, bốn cặp parser, và MỘT định nghĩa tiêu chí số

Cross-review lượt 9 (codex `gpt-6-astra` medium) trên head `76f199e` theo r13: `blocked`, **P1 0 · P2 1 · P3 0 · P4 1**.
Chín đột biến của lượt 8 đều đỏ trên v4. Nguồn của r14 — chủ kho 25-09-2026, trong phiên điều phối, bản chiếu
`issues/574#issuecomment-5834415321`: *"Mở r14 + g14 (đề xuất)"* ⟦nguon:chi-thi⟧, giữ hạn `2026-09-26T06:00:00Z`.

- **F2 (P2), tiếp diễn — bảy đột biến sống `60/60`:** ba ở ĐƯỜNG CLI mà r13 khai đã khoá — `l9_cli_last_ham` (chỉ xử lý tên
  CUỐI của `--ham`), `l9_cli_ignore_lech` và `l9_cli_ignore_missing` (`main` bỏ `LECH` hoặc `KHONG_DO_DUOC` khỏi điều kiện mã
  thoát); bốn ở parser — `l9_label_no_markup` (trên r13 thật: `VI_PHAM 19 · CO_NHAN 2`, rc=1), `l9_curly_no_multiline`,
  `l9_rv_hyphen`, `l9_min_fragment5`. Lời khai r13 rằng bốn ca CLI khoá đường chuyển tham số là RỘNG hơn phép đo: chúng khoá
  một tên hàm và một bộ đếm lỗi, không khoá mã thoát theo TỪNG bộ đếm.
- **P4 `nguong-con-tro-chua-noi-bang-nghiem-thu`:** tiêu chí `DUNG 33` / `DUNG 2` nằm ở §0.12 mà bảng §5 không dẫn tới.

**Đổi ở r14 — công cụ con trỏ v5, Phụ lục H, nguyên văn** (Phụ lục E, F, G giữ làm lịch sử). Chỉ `tu_kiem` đổi; phần văn bản
trước và sau `tu_kiem` bằng byte với v4. Thêm:

| trục | ca |
|---|---|
| mã thoát theo TỪNG bộ đếm, qua `main` trong tiến trình con | chỉ `LECH` → `rc=1` · chỉ `KHONG_DO_DUOC` → `rc=1` · chỉ `VI_PHAM` → `rc=1` · sạch có một con trỏ đúng → `rc=0` |
| `--ham` nhiều tên, tệp ba hàm a (xấu) · b (sạch) · c (xấu) | `a,b` lỗi ở ĐẦU → `rc=1`, 1 · `b,c` lỗi ở CUỐI → `rc=1`, 1 · `a,b,c` → `rc=1`, 2 · `b` → `rc=0`, 0 |
| nhãn sau markup | `*"…"* ⟦nguon:chi-thi⟧` và `**"…"** ⟦nguon:verdict⟧` → `CO_NHAN` (nhãn thường: ca cũ) |
| ngoặc cong vắt dòng | `“abcd` / `efgh”` trong một khối → `VI_PHAM` (ngoặc thẳng vắt dòng: ca cũ) |
| ranh giới trái của token | `ma-r1` → 0 |
| độ dài mảnh | 5 ký tự → `VI_PHAM` (6 ký tự → `DUNG`: ca cũ) |

**Đo, không suy (`rc` đọc trực tiếp):** `tu-kiem` **`TU_KIEM DAT 73/73`**. **39 đột biến công cụ** — 32 của các lượt trước và
7 của lượt 9 — mỗi cái một bản sao, một tiến trình: **cả 39 ĐỎ**, mỗi cái nêu tên ca đỏ. Cùng bảy đột biến lượt 9 trên v4:
cả bảy `60/60`, rc=0 — tái lập bảng của reviewer.

| đột biến (lượt 9) | ca đỏ ở v5 |
|---|---|
| `l9_cli_last_ham` | `cli_ham_loi_dau`, `cli_ham_hai_loi` |
| `l9_cli_ignore_lech` | `cli_chi_LECH` |
| `l9_cli_ignore_missing` | `cli_chi_KHONG_DO_DUOC` |
| `l9_label_no_markup` | `nhan_sau_markup`, `nhan_sau_markup_dam` |
| `l9_curly_no_multiline` | `ngoac_cong_vat_dong` |
| `l9_rv_hyphen` | `rv_sau_gach_noi` |
| `l9_min_fragment5` | `manh_5_am` |

**TIÊU CHÍ SỐ CỦA CỔNG CON TRỎ — định nghĩa CÓ THẨM QUYỀN, duy nhất (từ r14).** Mọi chỗ khác chỉ DẪN CHIẾU mục này; số
trong các bảng đo lịch sử (§0.9–§0.12) là số đo tại thời điểm ấy, không phải tiêu chí. Công cụ là khối Python của phụ lục
MỚI NHẤT; nguồn r1…r9 là blob `364686e`; `rc` đọc trực tiếp từ tiến trình.

| phép đo | đạt khi và chỉ khi |
|---|---|
| **N1** `tu-kiem` | `rc=0` và dòng `TU_KIEM DAT n/n` với hai số bằng nhau, `n` bằng số ca của phụ lục mới nhất |
| **N2** `kiem` trên CHÍNH đặc tả revision hiện hành | `rc=0` · **`DUNG 33`** · `LECH 0` · `KHONG_DO_DUOC 0` · `VI_PHAM 0` (CO_NHAN không phải tiêu chí) |
| **N3** `kiem --ham _c378_ma_tran_phan_hang,_r378_classify,_c378_resolve_phai_o_trong_kho scripts/tl_selftest.py` tại head review | `rc=0` · **`DUNG 2`** · `LECH 0` · `KHONG_DO_DUOC 0` · `VI_PHAM 0` |

`DUNG` phải BẰNG số kỳ vọng, không chỉ lớn hơn 0: mất một con trỏ là đỏ. Thêm hay bớt con trỏ trong một revision mới thì
revision ấy phải đổi số ở ĐÂY và nói lý do. Bảng §5 dòng `A12` dẫn tới mục này.

**Đo lại tại r14 bằng v5:** N1 `73/73`, rc=0 · N2 `DUNG 33`, lỗi 0, rc=0 (`CO_NHAN 22`) · N3 `DUNG 2`, lỗi 0, rc=0.

**PHẠM VI CHƯA đo** giữ như §0.12, thêm: ký tự markup khác `*` và `_` trước nhãn; ngoặc cong lồng ngoặc thẳng.

**Mã:** không đổi — head vẫn `76f199e`, không đẩy gì lên #588. **Không đổi ở r14:** mọi số hạng, `A1`–`A11`, Phụ lục A–G,
§7, §9, `write_set`, điều kiện dừng, hạn.

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
| **A5** | **M4**: indirection dựng xong mà `resolve()` không thoát khỏi `root` ⇒ `PATH_MISMATCH_NOT_CREATED`. | Ca tiêm: trỏ indirection vào một thư mục NẰM TRONG `root` ⇒ phải ném. Đột biến bỏ chốt ⇒ ca ĐỎ. **Đây là chốt chống "ca có MẶT khác ca có ĐO" ⟦nguon:doctrine⟧.** |
| **A6** (VIẾT LẠI ở **r3**; **SỬA SỐ HẠNG và PHẢN CHỨNG ở r5** — §0.4) | `_r378_classify` phải đúng trên một ma trận mà **mỗi nhãn mang một HỌ thành viên**, không một đại diện. Trục **LỚP**, 11 thành viên: lớp THẬT · con CÙNG module · con **KHÁC module** · **ĐA KẾ THỪA** · `RuntimeError` · **`AssertionError`** · **`ValueError`** · `TypeError` · `KeyError` · **TRÙNG TÊN** khác `id()` · **TRÙNG TÊN và là lớp con của `ValueError`**. Trục **DẠNG ĐỐI SỐ**, **7** dạng: không đối số · chuỗi rỗng · thông điệp gốc · thông điệp khác · hai đối số · **`moc_kem_doi_so_2`** (thêm ở r3 để tách `m10` khỏi `m14`, §8.5) · `None`. Trục **ORACLE**: chạy-và-ném (khối A, 11×7 = **77** ô) · chạy-và-thoả (khối B) · khâu DỰNG hỏng (khối C). Tổng **79** ô — khớp `A11`, §8.3 và AST của head `34cb21f` (`LOP=11`, `DOI_SO=7`). **r3 và r4 ghi ô này là 6 dạng / 66 / 68 — đó là số của ma trận theo HỌ bản đầu `576774b`, bị bỏ sót khi `ce9de50` thêm dạng thứ bảy** (r5 gọi nhầm nó là ma trận r2 ⟦r5:100 #37b637f2|ma trận r2 không phân biệt nổi⟧; ma trận r2 là 4×3 ĐẠI DIỆN ở `5b1772d` — §0.5). Ca **THU TẬP ĐẦY ĐỦ** tập ô đỏ rồi mới ném một lần, KHÔNG dừng ở ô hỏng đầu tiên — `A11` đòi so TẬP ô, dừng sớm thì không so được. Khối B và C chốt thêm **SỐ LẦN GỌI** oracle (đúng 1 · đúng 0). | Mỗi ô có `expected` là **DỮ LIỆU** — suy từ cờ `bat_duoc` VIẾT TAY và `lop.__name__`, KHÔNG từ chính `_r378_classify`. Bảng fixture có **chốt tự kiểm**: `bat_duoc` phải khớp `issubclass`; hai lớp `trung_ten*` phải thật sự trùng `__name__`; lớp `con_khac_module` phải thật sự khác `__module__` — trôi cái nào thì ném `R378_MA_TRAN_FIXTURE_TROI`. **Phép đo làm A6 ĐỎ — BA phản chứng cho hình dạng HỌ, cả ba ĐÃ ĐO (§0.4):** (1) rút `thuong_assert` khỏi trục LỚP ⇒ `m3` **SỐNG LẠI** (0 ô đỏ); (2) rút `con_khac_module` ⇒ `m13` **SỐNG LẠI**; (3) rút `moc_kem_doi_so_2` khỏi trục DẠNG ĐỐI SỐ ⇒ **TẬP ô đỏ của `m10` BẰNG TẬP của `m14`** (27 = 27, hai hiệu tập rỗng) — bộ tương đương của §8.5 tái xuất hiện; với đủ 7 dạng thì `m10` 34 · `m14` 31 · chỉ-`m10` 7 · chỉ-`m14` 4. **KHÔNG được khai** rằng rút `khong_doi_so` làm `m14` sống lại: r3/r4 khai như vậy và phép đo **BÁC** — rút riêng nó `m14` vẫn đỏ 27/68, rút cùng `moc_kem_doi_so_2` vẫn đỏ 23 toạ độ. **GIỮ NGUYÊN ngữ nghĩa `except` của Python**: lớp CON vẫn là `killed`; ma trận ĐO bộ phân hạng, nó KHÔNG tự quyết đổi sang so kiểu chính xác. |
| **A11** (VIẾT LẠI ở **r3**; **THU PHẠM VI về bộ CÓ ĐỊNH NGHĨA BỀN ở r5** — §0.4) | Ma trận phải bắt **TOÀN BỘ bộ hồi quy đã định nghĩa BỀN ở Phụ lục A** — **TÁM** đột biến `m3` `m7` `m9` `m10` `m11` `m12` `m13` `m14` — và **ô đỏ của mỗi cái là một phép ĐO, không phải một dự đoán**. **r3/r4 đòi `m1`–`m14`; điều đó KHÔNG thoả mãn được**: các nhãn `m1` `m2` `m4` `m5` `m6` `m8` là nhãn **THEO TỪNG LƯỢT review**, được dùng lại với nghĩa KHÁC NHAU qua các lượt, và định nghĩa của chúng nằm trong scratchpad đã mất cùng container — không bản đặc tả nào `r1`–`r4` định nghĩa chúng (§0.4). Lớp `L7 KHONG-THOAI-LUI-HO-DOT-BIEN-KHI-DOI-CA` vẫn nguyên: *mọi mutant lịch sử đã bị bắt trước refactor phải tiếp tục bị bắt* — nhưng một mutant chỉ **thuộc** bộ hồi quy khi định nghĩa của nó **nằm BỀN trong kho** dưới dạng neo/thay chạy được. Mutant mới muốn vào bộ phải vào Phụ lục A qua một revision. | Chạy TOÀN suite, **TUẦN TỰ** (§8.7), mỗi đột biến một lượt `tl.py --selftest` đầy đủ trên một `git clone` có `.git` THẬT, `core.abbrev = 7`, và `commit.gpgsign=false` CHỈ trong tiến trình test (fixture ký commit hỏng trong sandbox — cả hai reviewer lượt 24-09 đều vấp, §0.4); ghi lại **TẬP ô đỏ** kèm `expected`/`observed`/`oracle_calls`. **So bằng TẬP, KHÔNG bằng SỐ ĐẾM**: đủ **28 cặp** của tám đột biến phải khác nhau đôi một. **Đường đọc**: TẬP ô phải đọc từ bản sao RIG đã nới `_TRAN_CHAN_DOAN_110` (harness cắt chẩn đoán ở 400 ký tự, §8.3). **Tiêu chí này KHÔNG ghi trước ô nào ứng với đột biến nào** — r2 từng ghi ô đỏ của `m7` (⟦r2:168 #a17ee73d|m7 ⇒ ô⟧) và phép đo BÁC. **Đo ở r5 trên head `34cb21f`** (cross-review 24-09): cả tám `1714/1715`, `rc=1`, ca đỏ DUY NHẤT `r378_ma_tran_phan_hang`, ô đỏ 7·8·1·34·35·14·7·31 trên 79, **28/28 cặp khác nhau**. |
| **A7** | `tl.py --selftest` **DELTA so `origin/master` = 0** trên POSIX, và `r378_l7_resolve_phai_o_trong_kho` ở tập ĐẠT của cả hai vế. | **Đo hai vế trong MỘT lệnh**, cùng các bước, chạy liền nhau. So **TẬP TÊN** ca đỏ, không so số đếm — mất một ca đỏ cũ, thêm một ca đỏ mới, tổng không đổi: đó là ca mà phép đếm không bắt được. Nền đo 20-09 trên Linux: **1711/1711**; **đo lại trước khi tin** (L5). |
| **A8** | `release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true` **và** `expected == checked`. | Chạy **tại chỗ, đúng lệnh của lane LAND**. Lane PR **KHÔNG** bắt được lệch manifest (`if: github.ref == 'refs/heads/master'`; lane WORKER sinh manifest tạm nên hấp thụ mọi thay đổi nội dung) ⇒ PR xanh, master ĐỎ. |
| **A9** | `numstat` chạm **đúng hai** đường của `write_set`. | Đột biến thêm đường thứ ba ⇒ ĐỎ. Chốt write-set exclusion §5. |
| **A10** | `doctrine-scan` · `adr-song` · `doc-claims-check --strict` · `git diff --check` `rc=0`, `core.abbrev = 7`. | `rc` đọc **trực tiếp**, không qua pipe (nợ `RC-QUA-PIPE-KHONG-CO-CHOT`). |
| **A12** (MỚI ở **r14**) | Cổng con trỏ đạt **N1–N3** — tiêu chí số CÓ THẨM QUYỀN ở §0.13, không chép lại ở đây. | Đột biến `new_pointer_single_line` (§0.12) làm N2 ra `DUNG 0` với `rc=0` ⇒ N2 ĐỎ vì `DUNG` ≠ 33, dù `rc=0`; đột biến bất kỳ trong 39 đột biến công cụ ⇒ N1 ĐỎ. |

## 6. `hinh_dang_ke_thua` (L4) — chép từ #565

| hình dạng | số lần | nguồn |
|---|---|---|
| `RIG-QUYET-MAU-CUA-PHEP-DO` | **5** | Chép từ #565 (4 ca `CLAUDE.md` 24-08 + `Đ1`). **Packet này chạm đúng lớp ấy**: một ca đỏ vì RIG (thiếu đặc quyền), không vì mã. |
| `NGOAI-LE-BI-NUOT-LANG` | **2** | Chép từ #565. Ca r378 từng đỏ **câm** trước khi `Đ2` land — chính nó là ca thứ hai. |
| `LOI-KHAI-RONG-HON-PHEP-DO` | 7 → **10** | Chép 6 từ biên nhận #565. **+1**: câu *"KHÔNG PORT THẲNG ĐƯỢC … giả thuyết, chưa chạy"* ⟦nguon:issue⟧ của #574 **hẹp hơn** phép đo — mẫu ấy đã có sẵn và đã chạy trong cùng tệp. Lời khai lệch phép đo **theo chiều hẹp** cũng là lệch. **+1 ở r3**: câu của r2 ⟦r2:67 #a64cff8f|dù nó sai theo chiều nào⟧ *(r3–r7 trích bằng câu diễn ý trong ngoặc; r8 trích nguyên văn; r10 thay bằng con trỏ — §0.9)* — **rộng hơn**, và lượt 5 bác bằng ba phản chứng nằm ngay trong các trục r2 đã khai (§8.3). |
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
   *"cổng không nói dối, nó VẮNG MẶT"* ⟦nguon:doctrine⟧.
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
   nhớ, và nó đã làm packet này khai sai một lần: **`[FAIL]=0` KHÔNG hàm ý `bỏ qua = 0`**, vì
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

**r2 khai** ⟦r2:67 #a64cff8f|dù nó sai theo chiều nào⟧.
*(r3–r6 trích bằng một câu diễn ý đặt trong ngoặc; r7 thay bằng câu thật; r10 thay bằng con trỏ — §0.6, §0.9.)* Câu ấy **RỘNG
HƠN phép đo**, và lượt 5 bác nó bằng ba phản chứng nằm NGAY TRONG các trục r2 đã khai (`m12`,
`m13`, `m14`). Đây là lần thứ **mười** của lớp `LOI-KHAI-RONG-HON-PHEP-DO` trong sổ §6 — và lần
này nạn nhân là chính câu viết ra để tổng kết một bộ đo.

**r3 khai lại, hẹp đúng bằng phép đo:** ma trận bảo đảm cho **MIỀN ĐÃ LIỆT KÊ** — 11 lớp × 7
dạng đối số × 3 trạng thái oracle, tức **79 ô** — và **không** cho mọi cài đặt sai có thể viết
bằng Python. Ba điều còn lại, khai thẳng:

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
toạ độ riêng — không ô nào sinh hai mục, nên `số ô` và `số toạ độ` trùng nhau ở mọi lượt.

**So TẬP đôi một, đủ 28 cặp: KHÔNG cặp nào trùng.** Đó là thứ `A11` đòi, và nó mạnh hơn hẳn bảng
bốn ô của r2 — ở đó bằng chứng chỉ là bốn ô đỏ đầu tiên khác nhau (r2 §8.4, cột ⟦r2:286 #38bd7f77|ô đỏ ĐẦU TIÊN⟧), vì ca dừng ngay ô hỏng đầu. *(r3–r7 đặt một câu diễn ý trong ngoặc như lời r2 — ⟦r3:363 #eb2d15f9|bốn ô ĐẦU TIÊN khác nhau⟧; r2 không có câu ấy; r8 sửa, §0.7.)*

Hai tập đọc kỹ cho thấy ma trận đang đo TRỤC chứ không đo điểm:

- `m3` đỏ **đúng 7 ô**, tất cả ở `lop=thuong_assert`, trải hết **cả 7 dạng đối số** — một lát cắt
  SẠCH theo trục LỚP. Đây chính là phủ mà r2 đánh rơi.
- `m13` cũng đỏ **đúng 7 ô**, tất cả ở `lop=con_khac_module`, cũng trải hết 7 dạng. Cùng lực
  lượng, **tập khác hẳn** — minh hoạ sống cho luật "so TẬP, đừng so SỐ ĐẾM" ⟦nguon:doctrine⟧.

### 8.5 — `m10` và `m14` là một BỘ TƯƠNG ĐƯƠNG dưới ma trận SÁU dạng (`576774b`) — và không ai phát hiện ra

Đây là phát hiện đắt nhất của r3, và **không reviewer nào nêu**: nó lộ ra vì `A11` đòi so TẬP.

Đo trên ma trận **sáu dạng của bản đầu theo HỌ, `576774b`** (6 dạng đối số, 68 ô; r3–r5 gọi nhầm là ma trận r2 — ⟦r3:372 #f04e93cf|BỘ TƯƠNG ĐƯƠNG dưới ma trận r2⟧), hai lượt `--selftest` riêng:

```
m10  27/68 ô đỏ · 27 toạ độ
m14  27/68 ô đỏ · 27 toạ độ
comm -23 = 0 · comm -13 = 0 · chung = 27      <- HAI TẬP BẰNG NHAU
```

`m10` phân hạng bằng **chuỗi** (`"R378_EXPECTATION_MISMATCH" in str(exc)`), `m14` bằng **`args`**
(`exc.args == ("R378_EXPECTATION_MISMATCH",)`). Hai cài đặt sai khác hẳn nhau về cơ chế, mà ma
trận sáu dạng `576774b` **không phân biệt nổi** *(r3–r6 gọi là ma trận r2 — ⟦r3:386 #79173d92|không phân biệt nổi⟧ — sai, r7 sửa; §0.6)* — nó đang đo ÍT trục hơn nó khai, đúng một tầng nữa của cùng bệnh
mà r2 sinh ra để chữa.

**Chỗ tách chúng, và vì sao trục cũ không có:** một ngoại lệ mang mốc đúng **KÈM đối số thứ hai**.
`str()` của nó là `('R378_EXPECTATION_MISMATCH', 'x')` — **CHỨA** mốc, nên `m10` cấp `killed`;
`args` thì **KHÁC** tuple một phần tử, nên `m14` cấp tín dụng giả. Trục `DOI_SO` của `576774b` có
`hai_doi_so` (`("a","b")`) *(r3–r6 gán trục này cho r2 — ⟦r3:391 #e223594b|Trục DOI_SO của r2 có⟧ — r2 không có trục `DOI_SO`; §0.6)* nhưng **không** có dạng hai đối số trong đó cái đầu là mốc đúng —
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

**Kết luận không cặp nào trùng KHÔNG bị lung lay** bởi lỗi này — bỏ sót ô chỉ có thể làm hai tập
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

> *"Chuyển điều kiện dừng là tới khi không còn findings P1, P2, P3"* ⟦nguon:chi-thi⟧

**Vòng lặp vá / cross-review của packet này dừng khi một lượt cho `0` finding ở CẢ BA mức `P1`,
`P2`, `P3`.** Bốn điều phải khai kèm, vì chúng quyết định luật này chặt hay lỏng:

- **Chặt hơn `cross_approved`.** Một verdict `approve` vẫn có thể kèm P3 — năm lượt đã chạy trên
  packet này đều có finding, nên **không lượt nào trong số đó dừng được** dưới luật mới.
- **`P4` / giới hạn đã khai KHÔNG nằm trong điều kiện dừng**, theo đúng chữ của chỉ thị. Nhưng
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

## Phụ lục D — cổng CON TRỎ của §0.9 (MỚI ở r10, nguyên văn)

Chạy từ gốc kho: `python3 con_tro.py kiem --nguon <thư mục chứa các revision> --mau 'r378-symlink-doi-dac-quyen-r{n}.md' <tệp>`; `tu-kiem` cho tám ca tự kiểm. Phụ lục B, C giữ nguyên làm lịch sử.

```python
"""Con tro nguon cho dac ta R378 (r10 #574) — thay moi loi trich VIET TAY cua revision khac.

  CON TRO   ⟦rN:L #h⟧ hoac ⟦rN:L-M #h⟧ : dong L (den M) cua dac ta revision N; h = 8 hex dau cua sha256 noi
            dung cac dong ay sau chuan hoa (bo khoang trang dau/cuoi moi dong, gop khoang trang). Tro sai dong
            => h lech => DO. Sinh bang lenh `sinh`, KHONG go tay.
  NHAN NGUON ⟦nguon:K⟧ ngay sau mot chuoi trong ngoac: chuoi ay KHONG phai loi cua mot revision (K thuoc
            chi-thi | verdict | commit | ma | doctrine | issue). May KHONG kiem noi dung chuoi co nhan.
  LUAT      Trong moi KHOI (bang, doan, docstring) co nhac mot revision (token rN), MOI chuoi trong ngoac kep
            (thang hoac cong, >= 8 ky tu, vat nhieu dong duoc) PHAI mang nhan nguon. Chuoi thieu nhan => VI_PHAM.
            Loi cua revision khac chi duoc dan bang CON TRO, khong duoc dat trong ngoac.
Lenh:
  sinh  --nguon DIR --mau MAU rN L[-M]         in con tro cho dong ay
  tim   --nguon DIR --mau MAU "cum tu"         in con tro cua moi dong (moi revision) chua cum tu
  kiem  --nguon DIR --mau MAU TEP [TEP...]     .md: khoi markdown; .py: hang chuoi qua ast. rc=0 chi khi LECH=0,
                                               VI_PHAM=0, KHONG_DO_DUOC=0. In so da kiem theo ba trang thai.
  tu-kiem                                      ca am/duong tren nguon tam — cong phai DO duoc.
"""
import ast, hashlib, re, sys, tempfile
from pathlib import Path
CT = re.compile(r"⟦r(\d+):(\d+)(?:-(\d+))? #([0-9a-f]{8})⟧")
NHAN = re.compile(r"[*_]*\s*⟦nguon:(chi-thi|verdict|commit|ma|doctrine|issue)⟧")
Q = re.compile(r'"([^"]{8,}?)"|“([^”]{8,}?)”', re.S)
CODE = re.compile(r"`[^`\n]*`")
def che_code(k): return CODE.sub(lambda m: " " * len(m.group(0)), k)  # chuoi trong `code` la MA, khong phai loi trich
RV = re.compile(r"(?<![\w-])r\d+(?![\w])")
def chuan(ds): return "\n".join(re.sub(r"\s+", " ", x.strip()) for x in ds)
def bam(ds): return hashlib.sha256(chuan(ds).encode("utf-8")).hexdigest()[:8]
def nguon(dir_, mau, n):
    p = Path(dir_) / mau.format(n=n)
    return p.read_text(encoding="utf-8").split("\n") if p.is_file() else None
def sinh(dir_, mau, n, a, b=None):
    L = nguon(dir_, mau, n); b = b or a
    if L is None or not (1 <= a <= b <= len(L)): raise SystemExit(f"KHONG_DO_DUOC r{n}:{a}-{b}")
    return f"⟦r{n}:{a}{'' if b == a else '-' + str(b)} #{bam(L[a-1:b])}⟧"
def khoi_md(van):
    L, kq, cur, dau, td, rao = van.split("\n"), [], [], 0, "", False
    def day():
        if cur: kq.append((dau + 1, td, "\n".join(cur)))
    for i, l in enumerate(L):
        if l.lstrip().startswith("```"):
            day(); cur.clear(); rao = not rao; continue
        if rao: continue
        bang = l.lstrip().startswith("|")
        if l.startswith("#"):
            day(); cur.clear(); td = l; continue
        if not l.strip() or (cur and bang != cur[-1].lstrip().startswith("|")):
            day(); cur.clear()
            if not l.strip(): continue
        if not cur: dau = i
        cur.append(l)
    day(); return kq
def khoi_py(van, ham=None):
    """Hang chuoi > 40 ky tu; `ham` (tap ten) gioi han vao than cac ham ay — write set chi cho sua mot so ham."""
    kq = []; goc = ast.parse(van)
    vung = [(f.lineno, f.end_lineno) for f in ast.walk(goc) if isinstance(f, ast.FunctionDef) and f.name in ham] if ham else None
    for n in ast.walk(goc):
        if vung is not None and not any(a <= n.lineno <= b for a, b in vung if hasattr(n, "lineno")): continue
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) > 40:
            off = 0
            for doan in re.split(r"(\n\s*\n)", n.value):
                if doan.strip() and not re.fullmatch(r"\n\s*\n", doan):
                    kq.append((n.lineno + n.value[:off].count("\n"), "", doan))
                off += len(doan)
    return kq
def kiem(dir_, mau, tep, ham=None):
    van = Path(tep).read_text(encoding="utf-8"); dem = {"DUNG": 0, "LECH": 0, "KHONG_DO_DUOC": 0, "VI_PHAM": 0, "CO_NHAN": 0}
    for m in CT.finditer(van):
        n, a, b, h = int(m.group(1)), int(m.group(2)), int(m.group(3) or m.group(2)), m.group(4)
        d = van[:m.start()].count("\n") + 1
        L = nguon(dir_, mau, n)
        if L is None: dem["KHONG_DO_DUOC"] += 1; print(f"KHONG_DO_DUOC {tep}:{d} {m.group(0)} (khong co tep r{n})"); continue
        if not (1 <= a <= b <= len(L)): dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (ngoai pham vi 1..{len(L)})"); continue
        if bam(L[a-1:b]) != h: dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (bam that {bam(L[a-1:b])})"); continue
        dem["DUNG"] += 1
    for dong, td, k in (khoi_py(van, ham) if str(tep).endswith(".py") else khoi_md(van)):
        if not (RV.search(k) or RV.search(td)): continue
        kc = k if str(tep).endswith(".py") else che_code(k)
        for m in Q.finditer(kc):
            if NHAN.match(k, m.end()): dem["CO_NHAN"] += 1; continue
            dem["VI_PHAM"] += 1
            print(f"VI_PHAM {tep}:{dong + k[:m.start()].count(chr(10))} chuoi trong ngoac khong nhan nguon: {(m.group(1) or m.group(2))[:90]!r}")
    return dem
def tu_kiem():
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "r1.md").write_text("dong mot\ndong hai co noi dung\ndong ba\n", encoding="utf-8")
        ct = sinh(t, "r{n}.md", 1, 2)
        ca = {"duong": (f"Theo r1 {ct} thi dung.\n", True),
              "sai_dong": (f"Theo r1 {ct.replace(':2 ', ':3 ')} thi sai.\n", False),
              "ngoai_pham_vi": (f"Theo r1 {ct.replace(':2 ', ':9 ')}.\n", False),
              "thieu_tep": (f"Theo r1 {ct.replace('⟦r1', '⟦r7')}.\n", False),
              "trich_khong_nhan": ('Theo r1 thi "dong hai co noi dung" la loi cua no.\n', False),
              "trich_co_nhan": ('Theo r1, chu kho noi "lam tiep di nhe" ⟦nguon:chi-thi⟧.\n', True),
              "vat_dong": ('r1 viet "dong hai\nco noi dung" khong nhan.\n', False),
              "trong_code": ('r1 dung `x == "dong hai co noi dung"` trong ma.\n', True)}
        hong = []
        for ten, (doc, phai_dat) in ca.items():
            p = Path(t) / f"{ten}.md"; p.write_text(doc, encoding="utf-8")
            d = kiem(t, "r{n}.md", p); dat = d["LECH"] == d["VI_PHAM"] == d["KHONG_DO_DUOC"] == 0
            if dat != phai_dat: hong.append(ten)
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{len(ca) - len(hong)}/{len(ca)}")
        return 0 if not hong else 1
def main(a):
    if a[:1] == ["tu-kiem"]: return tu_kiem()
    cmd, co, rest, i = a[0], {}, [], 1
    while i < len(a):
        if a[i] in ("--nguon", "--mau", "--ham"): co[a[i]] = a[i + 1]; i += 2
        else: rest.append(a[i]); i += 1
    dir_, mau = co["--nguon"], co["--mau"]
    ham = set(co["--ham"].split(",")) if "--ham" in co else None
    if cmd == "sinh":
        n = int(rest[0].lstrip("r")); ab = rest[1].split("-"); print(sinh(dir_, mau, n, int(ab[0]), int(ab[-1]))); return 0
    if cmd == "tim":
        cum = re.sub(r"\s+", " ", rest[0]).strip(); n = 1
        while True:
            L = nguon(dir_, mau, n)
            if L is None: break
            for k, l in enumerate(L, 1):
                if cum in re.sub(r"\s+", " ", l): print(f"r{n}:{k} {sinh(dir_, mau, n, k)} {l.strip()[:100]}")
            n += 1
        return 0
    if cmd == "kiem":
        tong = {}
        for tep in rest:
            for k, v in kiem(dir_, mau, tep, ham).items(): tong[k] = tong.get(k, 0) + v
        print("TONG", tong); return 0 if tong["LECH"] == tong["VI_PHAM"] == tong["KHONG_DO_DUOC"] == 0 else 1
    raise SystemExit("lenh la: sinh | tim | kiem | tu-kiem")
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
```

## Phụ lục E — cổng CON TRỎ có MẢNH NEO của §0.10 (MỚI ở r11, nguyên văn)

Chạy từ gốc kho: `python3 con_tro.py kiem --nguon <thư mục chứa các revision> --mau 'r378-symlink-doi-dac-quyen-r{n}.md' <tệp>`; `tu-kiem` cho 15 ca có bộ đếm kỳ vọng. Phụ lục D (bản r10) giữ nguyên làm lịch sử.

```python
"""Con tro nguon cho dac ta R378 (r10 #574) — thay moi loi trich VIET TAY cua revision khac.

  CON TRO   ⟦rN:L #h|manh⟧ hoac ⟦rN:L-M #h|manh⟧ : dong L (den M) cua dac ta revision N; h = 8 hex dau cua
            sha256 noi dung cac dong ay sau chuan hoa (bo khoang trang dau/cuoi moi dong, gop khoang trang). Tro sai
            dong => h lech => DO. `manh` (BAT BUOC tu r11, >= 6 ky tu) la cum chu ma cau dan con tro dang noi toi; no
            phai NAM TRONG cac dong duoc tro (so sau khi bo `*` va dau backtick, gop khoang trang) — tro dung bam ma
            sai dong CAN TRO (F1d #574 luot 6: r3:322 thay vi 323-324) => DO. Sinh bang lenh `sinh`, KHONG go tay.
  NHAN NGUON ⟦nguon:K⟧ ngay sau mot chuoi trong ngoac: chuoi ay KHONG phai loi cua mot revision (K thuoc
            chi-thi | verdict | commit | ma | doctrine | issue). May KHONG kiem noi dung chuoi co nhan.
  LUAT      Trong moi KHOI (bang, doan, docstring) co nhac mot revision (token rN), MOI chuoi trong ngoac kep
            (thang hoac cong, >= 8 ky tu, vat nhieu dong duoc) PHAI mang nhan nguon. Chuoi thieu nhan => VI_PHAM.
            Loi cua revision khac chi duoc dan bang CON TRO, khong duoc dat trong ngoac.
Lenh:
  sinh  --nguon DIR --mau MAU rN L[-M]         in con tro cho dong ay
  tim   --nguon DIR --mau MAU "cum tu"         in con tro cua moi dong (moi revision) chua cum tu
  kiem  --nguon DIR --mau MAU TEP [TEP...]     .md: khoi markdown; .py: hang chuoi qua ast. rc=0 chi khi LECH=0,
                                               VI_PHAM=0, KHONG_DO_DUOC=0. In so da kiem theo ba trang thai.
  tu-kiem                                      ca am/duong tren nguon tam — cong phai DO duoc.
"""
import ast, hashlib, re, sys, tempfile
from pathlib import Path
CT = re.compile(r"⟦r(\d+):(\d+)(?:-(\d+))? #([0-9a-f]{8})(?:\|([^⟧]*))?⟧")
NHAN = re.compile(r"[*_]*\s*⟦nguon:(chi-thi|verdict|commit|ma|doctrine|issue)⟧")
Q = re.compile(r'"([^"]{8,}?)"|“([^”]{8,}?)”', re.S)
CODE = re.compile(r"`[^`\n]*`")
def che_code(k): return CODE.sub(lambda m: " " * len(m.group(0)), k)  # chuoi trong `code` la MA, khong phai loi trich
RV = re.compile(r"(?<![\w-])r\d+(?![\w])")
def chuan(ds): return "\n".join(re.sub(r"\s+", " ", x.strip()) for x in ds)
def bo_dau(x): return re.sub(r"\s+", " ", x.replace("*", "").replace("`", "")).strip()
def bam(ds): return hashlib.sha256(chuan(ds).encode("utf-8")).hexdigest()[:8]
def nguon(dir_, mau, n):
    p = Path(dir_) / mau.format(n=n)
    return p.read_text(encoding="utf-8").split("\n") if p.is_file() else None
def sinh(dir_, mau, n, a, b=None, manh=None):
    L = nguon(dir_, mau, n); b = b or a
    if L is None or not (1 <= a <= b <= len(L)): raise SystemExit(f"KHONG_DO_DUOC r{n}:{a}-{b}")
    if manh is None or len(bo_dau(manh)) < 6 or bo_dau(manh) not in bo_dau(" ".join(L[a-1:b])):
        raise SystemExit(f"MANH khong nam trong r{n}:{a}-{b}: {manh!r}")
    return f"⟦r{n}:{a}{'' if b == a else '-' + str(b)} #{bam(L[a-1:b])}|{bo_dau(manh)}⟧"
def khoi_md(van):
    L, kq, cur, dau, td, rao = van.split("\n"), [], [], 0, "", False
    def day():
        if cur: kq.append((dau + 1, td, "\n".join(cur)))
    for i, l in enumerate(L):
        if l.lstrip().startswith("```"):
            day(); cur.clear(); rao = not rao; continue
        if rao: continue
        bang = l.lstrip().startswith("|")
        if re.match(r"#{1,6} ", l):   # tieu de Markdown THAT (`#` + khoang trang); `#574 viet ...` khong phai tieu de
            day(); cur.clear(); td = l; continue
        if not l.strip() or (cur and bang != cur[-1].lstrip().startswith("|")):
            day(); cur.clear()
            if not l.strip(): continue
        if not cur: dau = i
        cur.append(l)
    day(); return kq
def khoi_py(van, ham=None):
    """Hang chuoi > 40 ky tu; `ham` (tap ten) gioi han vao than cac ham ay — write set chi cho sua mot so ham."""
    kq = []; goc = ast.parse(van)
    vung = [(f.lineno, f.end_lineno) for f in ast.walk(goc) if isinstance(f, ast.FunctionDef) and f.name in ham] if ham else None
    for n in ast.walk(goc):
        if vung is not None and not any(a <= n.lineno <= b for a, b in vung if hasattr(n, "lineno")): continue
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) > 40:
            off = 0
            for doan in re.split(r"(\n\s*\n)", n.value):
                if doan.strip() and not re.fullmatch(r"\n\s*\n", doan):
                    kq.append((n.lineno + n.value[:off].count("\n"), "", doan))
                off += len(doan)
    return kq
def kiem(dir_, mau, tep, ham=None):
    van = Path(tep).read_text(encoding="utf-8"); dem = {"DUNG": 0, "LECH": 0, "KHONG_DO_DUOC": 0, "VI_PHAM": 0, "CO_NHAN": 0}
    for m in CT.finditer(van):
        n, a, b, h = int(m.group(1)), int(m.group(2)), int(m.group(3) or m.group(2)), m.group(4)
        d = van[:m.start()].count("\n") + 1
        L = nguon(dir_, mau, n)
        if L is None: dem["KHONG_DO_DUOC"] += 1; print(f"KHONG_DO_DUOC {tep}:{d} {m.group(0)} (khong co tep r{n})"); continue
        if not (1 <= a <= b <= len(L)): dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (ngoai pham vi 1..{len(L)})"); continue
        if bam(L[a-1:b]) != h: dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (bam that {bam(L[a-1:b])})"); continue
        manh = m.group(5)
        if manh is None or len(bo_dau(manh)) < 6:
            dem["VI_PHAM"] += 1; print(f"VI_PHAM {tep}:{d} {m.group(0)} (thieu manh neo, hoac ngan hon 6 ky tu)"); continue
        if bo_dau(manh or "") not in bo_dau(" ".join(L[a-1:b])):
            dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (manh KHONG nam trong dong duoc tro)"); continue
        dem["DUNG"] += 1
    for dong, td, k in (khoi_py(van, ham) if str(tep).endswith(".py") else khoi_md(van)):
        if not (RV.search(k) or RV.search(td)): continue
        kc = k if str(tep).endswith(".py") else che_code(k)
        for m in Q.finditer(kc):
            if NHAN.match(k, m.end()): dem["CO_NHAN"] += 1; continue
            dem["VI_PHAM"] += 1
            print(f"VI_PHAM {tep}:{dong + k[:m.start()].count(chr(10))} chuoi trong ngoac khong nhan nguon: {(m.group(1) or m.group(2))[:90]!r}")
    return dem
def tu_kiem():
    """Ca am/duong voi BO DEM KY VONG chinh xac (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN) — khong chi dat/khong
    dat. Phu MOI nhanh dau vao duoc dung cho hop dong: .md than doan, .md chi co token o TIEU DE, .py qua ast, .py voi
    --ham (vi pham ngoai ham bi bo qua), manh neo. Tung la lo cua r10 (#574 luot 6, F2): bo han nhanh .py hoac vi
    tieu de ma tu kiem van 8/8."""
    import hashlib as _h
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "r1.md").write_text("dong mot\ndong hai co noi dung\ndong ba co cum khac\ndong bon co noi dung\n", encoding="utf-8")
        ct = sinh(t, "r{n}.md", 1, 2, manh="hai co noi dung")
        sai_manh = ct.replace("|hai co noi dung", "|ba co cum khac")
        khong_manh = ct.split("|")[0] + "⟧"
        Q2 = chr(34)
        py_xau = "def f():\n    " + Q2 * 3 + "Docstring noi ve r1: " + Q2 + "dong hai co noi dung" + Q2 + " khong nhan, du dai de qua nguong 40.\n    " + Q2 * 3 + "\n\n\ndef g():\n    " + Q2 * 3 + "Ham ngoai pham vi nhac r1: " + Q2 + "dong ba co cum khac" + Q2 + " khong nhan, du dai.\n    " + Q2 * 3 + "\n"
        ca = {  # ten: (ten tep, noi dung, --ham, ky vong (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN))
            "duong": ("a.md", f"Theo r1 {ct} thi dung.\n", None, (1, 0, 0, 0, 0)),
            "sai_dong": ("a.md", f"Theo r1 {ct.replace(':2 ', ':3 ')} thi sai.\n", None, (0, 1, 0, 0, 0)),
            "ngoai_pham_vi": ("a.md", f"Theo r1 {ct.replace(':2 ', ':9 ')}.\n", None, (0, 1, 0, 0, 0)),
            "thieu_tep": ("a.md", f"Theo r1 {ct.replace('⟦r1', '⟦r7')}.\n", None, (0, 0, 1, 0, 0)),
            "sai_bam_manh_van_khop": ("a.md", f"Theo r1 {sinh(t, 'r{n}.md', 1, 2, manh='co noi dung').replace(':2 ', ':4 ')}.\n", None, (0, 1, 0, 0, 0)),
            "sai_manh_dung_bam": ("a.md", f"Theo r1 {sai_manh}.\n", None, (0, 1, 0, 0, 0)),
            "thieu_manh": ("a.md", f"Theo r1 {khong_manh}.\n", None, (0, 0, 0, 1, 0)),
            "trich_khong_nhan": ("a.md", "Theo r1 thi " + Q2 + "dong hai co noi dung" + Q2 + " la loi cua no.\n", None, (0, 0, 0, 1, 0)),
            "trich_co_nhan": ("a.md", "Theo r1, chu kho noi " + Q2 + "lam tiep di nhe" + Q2 + " ⟦nguon:chi-thi⟧.\n", None, (0, 0, 0, 0, 1)),
            "vat_dong": ("a.md", "r1 viet " + Q2 + "dong hai\nco noi dung" + Q2 + " khong nhan.\n", None, (0, 0, 0, 1, 0)),
            "trong_code": ("a.md", "r1 dung `x == " + Q2 + "dong hai co noi dung" + Q2 + "` trong ma.\n", None, (0, 0, 0, 0, 0)),
            "chi_tieu_de": ("a.md", "## Nhan xet ve r1\n\nKhoi nay khong nhac ban nao ma viet " + Q2 + "dong hai co noi dung" + Q2 + ".\n", None, (0, 0, 0, 1, 0)),
            "gach_so_khong_phai_tieu_de": ("a.md", "Theo r1 thi\n#574 noi " + Q2 + "dong hai co noi dung" + Q2 + " khong nhan.\n", None, (0, 0, 0, 1, 0)),
            "py_docstring": ("a.py", py_xau, None, (0, 0, 0, 2, 0)),
            "py_ham": ("a.py", py_xau, {"f"}, (0, 0, 0, 1, 0)),
        }
        hong = []
        for ten, (tep, doc, ham, mong) in ca.items():
            p = Path(t) / ten / tep; p.parent.mkdir(); p.write_text(doc, encoding="utf-8")
            d = kiem(t, "r{n}.md", p, ham)
            thuc = (d["DUNG"], d["LECH"], d["KHONG_DO_DUOC"], d["VI_PHAM"], d["CO_NHAN"])
            if thuc != mong: hong.append(f"{ten}: mong {mong}, thuc {thuc}")
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{len(ca) - len(hong)}/{len(ca)}")
        return 0 if not hong else 1
def main(a):
    if a[:1] == ["tu-kiem"]: return tu_kiem()
    cmd, co, rest, i = a[0], {}, [], 1
    while i < len(a):
        if a[i] in ("--nguon", "--mau", "--ham"): co[a[i]] = a[i + 1]; i += 2
        else: rest.append(a[i]); i += 1
    dir_, mau = co["--nguon"], co["--mau"]
    ham = set(co["--ham"].split(",")) if "--ham" in co else None
    if cmd == "sinh":
        n = int(rest[0].lstrip("r")); ab = rest[1].split("-"); print(sinh(dir_, mau, n, int(ab[0]), int(ab[-1]), rest[2] if len(rest) > 2 else None)); return 0
    if cmd == "tim":
        cum = re.sub(r"\s+", " ", rest[0]).strip(); n = 1
        while True:
            L = nguon(dir_, mau, n)
            if L is None: break
            for k, l in enumerate(L, 1):
                if cum in re.sub(r"\s+", " ", l): print(f"r{n}:{k} {sinh(dir_, mau, n, k, manh=cum) if len(bo_dau(cum)) >= 6 and bo_dau(cum) in bo_dau(l) else '(cum co dau markdown)'} {l.strip()[:100]}")
            n += 1
        return 0
    if cmd == "kiem":
        tong = {}
        for tep in rest:
            for k, v in kiem(dir_, mau, tep, ham).items(): tong[k] = tong.get(k, 0) + v
        print("TONG", tong); return 0 if tong["LECH"] == tong["VI_PHAM"] == tong["KHONG_DO_DUOC"] == 0 else 1
    raise SystemExit("lenh la: sinh | tim | kiem | tu-kiem")
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
```

## Phụ lục F — cổng CON TRỎ v3: tự kiểm theo TRỤC ĐẦU VÀO của §0.11 (MỚI ở r12, nguyên văn)

Cùng cách chạy như Phụ lục E; `tu-kiem` cho 34 ca có bộ đếm kỳ vọng. So với Phụ lục E chỉ `tu_kiem` đổi. sha256 của khối mã dưới (tệp `con_tro.py`, không kể dòng rào): `fa6ac6d688950069fa9e00470c6bbb512fea088849f68ba2f6f104e2641193b0`.

```python
"""Con tro nguon cho dac ta R378 (r10 #574) — thay moi loi trich VIET TAY cua revision khac.

  CON TRO   ⟦rN:L #h|manh⟧ hoac ⟦rN:L-M #h|manh⟧ : dong L (den M) cua dac ta revision N; h = 8 hex dau cua
            sha256 noi dung cac dong ay sau chuan hoa (bo khoang trang dau/cuoi moi dong, gop khoang trang). Tro sai
            dong => h lech => DO. `manh` (BAT BUOC tu r11, >= 6 ky tu) la cum chu ma cau dan con tro dang noi toi; no
            phai NAM TRONG cac dong duoc tro (so sau khi bo `*` va dau backtick, gop khoang trang) — tro dung bam ma
            sai dong CAN TRO (F1d #574 luot 6: r3:322 thay vi 323-324) => DO. Sinh bang lenh `sinh`, KHONG go tay.
  NHAN NGUON ⟦nguon:K⟧ ngay sau mot chuoi trong ngoac: chuoi ay KHONG phai loi cua mot revision (K thuoc
            chi-thi | verdict | commit | ma | doctrine | issue). May KHONG kiem noi dung chuoi co nhan.
  LUAT      Trong moi KHOI (bang, doan, docstring) co nhac mot revision (token rN), MOI chuoi trong ngoac kep
            (thang hoac cong, >= 8 ky tu, vat nhieu dong duoc) PHAI mang nhan nguon. Chuoi thieu nhan => VI_PHAM.
            Loi cua revision khac chi duoc dan bang CON TRO, khong duoc dat trong ngoac.
Lenh:
  sinh  --nguon DIR --mau MAU rN L[-M]         in con tro cho dong ay
  tim   --nguon DIR --mau MAU "cum tu"         in con tro cua moi dong (moi revision) chua cum tu
  kiem  --nguon DIR --mau MAU TEP [TEP...]     .md: khoi markdown; .py: hang chuoi qua ast. rc=0 chi khi LECH=0,
                                               VI_PHAM=0, KHONG_DO_DUOC=0. In so da kiem theo ba trang thai.
  tu-kiem                                      ca am/duong tren nguon tam — cong phai DO duoc.
"""
import ast, hashlib, re, sys, tempfile
from pathlib import Path
CT = re.compile(r"⟦r(\d+):(\d+)(?:-(\d+))? #([0-9a-f]{8})(?:\|([^⟧]*))?⟧")
NHAN = re.compile(r"[*_]*\s*⟦nguon:(chi-thi|verdict|commit|ma|doctrine|issue)⟧")
Q = re.compile(r'"([^"]{8,}?)"|“([^”]{8,}?)”', re.S)
CODE = re.compile(r"`[^`\n]*`")
def che_code(k): return CODE.sub(lambda m: " " * len(m.group(0)), k)  # chuoi trong `code` la MA, khong phai loi trich
RV = re.compile(r"(?<![\w-])r\d+(?![\w])")
def chuan(ds): return "\n".join(re.sub(r"\s+", " ", x.strip()) for x in ds)
def bo_dau(x): return re.sub(r"\s+", " ", x.replace("*", "").replace("`", "")).strip()
def bam(ds): return hashlib.sha256(chuan(ds).encode("utf-8")).hexdigest()[:8]
def nguon(dir_, mau, n):
    p = Path(dir_) / mau.format(n=n)
    return p.read_text(encoding="utf-8").split("\n") if p.is_file() else None
def sinh(dir_, mau, n, a, b=None, manh=None):
    L = nguon(dir_, mau, n); b = b or a
    if L is None or not (1 <= a <= b <= len(L)): raise SystemExit(f"KHONG_DO_DUOC r{n}:{a}-{b}")
    if manh is None or len(bo_dau(manh)) < 6 or bo_dau(manh) not in bo_dau(" ".join(L[a-1:b])):
        raise SystemExit(f"MANH khong nam trong r{n}:{a}-{b}: {manh!r}")
    return f"⟦r{n}:{a}{'' if b == a else '-' + str(b)} #{bam(L[a-1:b])}|{bo_dau(manh)}⟧"
def khoi_md(van):
    L, kq, cur, dau, td, rao = van.split("\n"), [], [], 0, "", False
    def day():
        if cur: kq.append((dau + 1, td, "\n".join(cur)))
    for i, l in enumerate(L):
        if l.lstrip().startswith("```"):
            day(); cur.clear(); rao = not rao; continue
        if rao: continue
        bang = l.lstrip().startswith("|")
        if re.match(r"#{1,6} ", l):   # tieu de Markdown THAT (`#` + khoang trang); `#574 viet ...` khong phai tieu de
            day(); cur.clear(); td = l; continue
        if not l.strip() or (cur and bang != cur[-1].lstrip().startswith("|")):
            day(); cur.clear()
            if not l.strip(): continue
        if not cur: dau = i
        cur.append(l)
    day(); return kq
def khoi_py(van, ham=None):
    """Hang chuoi > 40 ky tu; `ham` (tap ten) gioi han vao than cac ham ay — write set chi cho sua mot so ham."""
    kq = []; goc = ast.parse(van)
    vung = [(f.lineno, f.end_lineno) for f in ast.walk(goc) if isinstance(f, ast.FunctionDef) and f.name in ham] if ham else None
    for n in ast.walk(goc):
        if vung is not None and not any(a <= n.lineno <= b for a, b in vung if hasattr(n, "lineno")): continue
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) > 40:
            off = 0
            for doan in re.split(r"(\n\s*\n)", n.value):
                if doan.strip() and not re.fullmatch(r"\n\s*\n", doan):
                    kq.append((n.lineno + n.value[:off].count("\n"), "", doan))
                off += len(doan)
    return kq
def kiem(dir_, mau, tep, ham=None):
    van = Path(tep).read_text(encoding="utf-8"); dem = {"DUNG": 0, "LECH": 0, "KHONG_DO_DUOC": 0, "VI_PHAM": 0, "CO_NHAN": 0}
    for m in CT.finditer(van):
        n, a, b, h = int(m.group(1)), int(m.group(2)), int(m.group(3) or m.group(2)), m.group(4)
        d = van[:m.start()].count("\n") + 1
        L = nguon(dir_, mau, n)
        if L is None: dem["KHONG_DO_DUOC"] += 1; print(f"KHONG_DO_DUOC {tep}:{d} {m.group(0)} (khong co tep r{n})"); continue
        if not (1 <= a <= b <= len(L)): dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (ngoai pham vi 1..{len(L)})"); continue
        if bam(L[a-1:b]) != h: dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (bam that {bam(L[a-1:b])})"); continue
        manh = m.group(5)
        if manh is None or len(bo_dau(manh)) < 6:
            dem["VI_PHAM"] += 1; print(f"VI_PHAM {tep}:{d} {m.group(0)} (thieu manh neo, hoac ngan hon 6 ky tu)"); continue
        if bo_dau(manh or "") not in bo_dau(" ".join(L[a-1:b])):
            dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (manh KHONG nam trong dong duoc tro)"); continue
        dem["DUNG"] += 1
    for dong, td, k in (khoi_py(van, ham) if str(tep).endswith(".py") else khoi_md(van)):
        if not (RV.search(k) or RV.search(td)): continue
        kc = k if str(tep).endswith(".py") else che_code(k)
        for m in Q.finditer(kc):
            if NHAN.match(k, m.end()): dem["CO_NHAN"] += 1; continue
            dem["VI_PHAM"] += 1
            print(f"VI_PHAM {tep}:{dong + k[:m.start()].count(chr(10))} chuoi trong ngoac khong nhan nguon: {(m.group(1) or m.group(2))[:90]!r}")
    return dem
def tu_kiem():
    """r12: them BANG LOP DAU VAO (pham vi dong, ngoac cong, nhan, do dai manh, dau markup, span, rao code, bien bang,
    doan docstring) voi con tro viet san — 11 dot bien song cua #574 luot 7 phai DO.
    Ca am/duong voi BO DEM KY VONG chinh xac (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN) — khong chi dat/khong
    dat. Phu MOI nhanh dau vao duoc dung cho hop dong: .md than doan, .md chi co token o TIEU DE, .py qua ast, .py voi
    --ham (vi pham ngoai ham bi bo qua), manh neo. Tung la lo cua r10 (#574 luot 6, F2): bo han nhanh .py hoac vi
    tieu de ma tu kiem van 8/8."""
    import hashlib as _h
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "r1.md").write_text("dong mot\ndong hai co noi dung\ndong ba co cum khac\ndong bon co noi dung\n", encoding="utf-8")
        (Path(t) / "r2.md").write_text("dong **mot** co noi dung\ndong mot  co noi dung\ndong `ma ba` co chu\n", encoding="utf-8")
        ct = sinh(t, "r{n}.md", 1, 2, manh="hai co noi dung")
        sai_manh = ct.replace("|hai co noi dung", "|ba co cum khac")
        khong_manh = ct.split("|")[0] + "⟧"
        Q2 = chr(34)
        py_xau = "def f():\n    " + Q2 * 3 + "Docstring noi ve r1: " + Q2 + "dong hai co noi dung" + Q2 + " khong nhan, du dai de qua nguong 40.\n    " + Q2 * 3 + "\n\n\ndef g():\n    " + Q2 * 3 + "Ham ngoai pham vi nhac r1: " + Q2 + "dong ba co cum khac" + Q2 + " khong nhan, du dai.\n    " + Q2 * 3 + "\n"
        ca = {  # ten: (ten tep, noi dung, --ham, ky vong (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN))
            "duong": ("a.md", f"Theo r1 {ct} thi dung.\n", None, (1, 0, 0, 0, 0)),
            "sai_dong": ("a.md", f"Theo r1 {ct.replace(':2 ', ':3 ')} thi sai.\n", None, (0, 1, 0, 0, 0)),
            "ngoai_pham_vi": ("a.md", f"Theo r1 {ct.replace(':2 ', ':9 ')}.\n", None, (0, 1, 0, 0, 0)),
            "thieu_tep": ("a.md", f"Theo r1 {ct.replace('⟦r1', '⟦r7')}.\n", None, (0, 0, 1, 0, 0)),
            "sai_bam_manh_van_khop": ("a.md", f"Theo r1 {sinh(t, 'r{n}.md', 1, 2, manh='co noi dung').replace(':2 ', ':4 ')}.\n", None, (0, 1, 0, 0, 0)),
            "sai_manh_dung_bam": ("a.md", f"Theo r1 {sai_manh}.\n", None, (0, 1, 0, 0, 0)),
            "thieu_manh": ("a.md", f"Theo r1 {khong_manh}.\n", None, (0, 0, 0, 1, 0)),
            "trich_khong_nhan": ("a.md", "Theo r1 thi " + Q2 + "dong hai co noi dung" + Q2 + " la loi cua no.\n", None, (0, 0, 0, 1, 0)),
            "trich_co_nhan": ("a.md", "Theo r1, chu kho noi " + Q2 + "lam tiep di nhe" + Q2 + " ⟦nguon:chi-thi⟧.\n", None, (0, 0, 0, 0, 1)),
            "vat_dong": ("a.md", "r1 viet " + Q2 + "dong hai\nco noi dung" + Q2 + " khong nhan.\n", None, (0, 0, 0, 1, 0)),
            "trong_code": ("a.md", "r1 dung `x == " + Q2 + "dong hai co noi dung" + Q2 + "` trong ma.\n", None, (0, 0, 0, 0, 0)),
            "chi_tieu_de": ("a.md", "## Nhan xet ve r1\n\nKhoi nay khong nhac ban nao ma viet " + Q2 + "dong hai co noi dung" + Q2 + ".\n", None, (0, 0, 0, 1, 0)),
            "gach_so_khong_phai_tieu_de": ("a.md", "Theo r1 thi\n#574 noi " + Q2 + "dong hai co noi dung" + Q2 + " khong nhan.\n", None, (0, 0, 0, 1, 0)),
            "py_docstring": ("a.py", py_xau, None, (0, 0, 0, 2, 0)),
            "py_ham": ("a.py", py_xau, {"f"}, (0, 0, 0, 1, 0)),
        }
        # r12 (#574 luot 7, F2): BANG LOP DAU VAO — moi truc mot cap am/duong. Con tro VIET SAN, bam tinh DOC LAP
        # (hashlib tren chuoi da chuan hoa bang tay) — KHONG sinh bang `sinh`/`bam`, de oracle khong di qua ham bi dot bien.
        CT0 = lambda x: chr(0x27E6) + x + chr(0x27E7)  # dung con tro luc chay: tep KHONG chua con tro lien, vi `kiem` quet ca khoi ma
        ca.update({
            "pv_duong_1_dong": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|hai co noi dung") + ".\n", None, (1, 0, 0, 0, 0)),
            "pv_cuoi_vuot_toan_tep": ("a.md", "Theo r1 " + CT0("r1:1-999 #7aad2135|dong mot dong hai") + ".\n", None, (0, 1, 0, 0, 0)),
            "pv_cuoi_vuot_mot_phan": ("a.md", "Theo r1 " + CT0("r1:2-9 #04a7a73c|hai co noi dung") + ".\n", None, (0, 1, 0, 0, 0)),
            "pv_dau_0": ("a.md", "Theo r1 " + CT0("r1:0-2 #e3b0c442|hai co noi dung") + ".\n", None, (0, 1, 0, 0, 0)),
            "pv_dao": ("a.md", "Theo r1 " + CT0("r1:3-2 #e3b0c442|hai co noi dung") + ".\n", None, (0, 1, 0, 0, 0)),
            "span_nhieu_dong_duong": ("a.md", "Theo r1 " + CT0("r1:2-3 #f4d0ba3e|noi dung dong ba") + ".\n", None, (1, 0, 0, 0, 0)),
            "ngoac_cong_am": ("a.md", "Theo r1: “dong hai co noi dung”.\n", None, (0, 0, 0, 1, 0)),
            "ngoac_cong_co_nhan": ("a.md", "Theo r1: “dong hai co noi dung” ⟦nguon:verdict⟧.\n", None, (0, 0, 0, 0, 1)),
            "nhan_khong_hop_le": ("a.md", "Theo r1: " + Q2 + "dong hai co noi dung" + Q2 + " ⟦nguon:khong-hop-le⟧.\n", None, (0, 0, 0, 1, 0)),
            "manh_6_duong": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|hai co") + ".\n", None, (1, 0, 0, 0, 0)),
            "manh_4_am": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|dong") + ".\n", None, (0, 0, 0, 1, 0)),
            "manh_bo_sao": ("a.md", "Theo r2 " + CT0("r2:1 #457257c7|dong mot co") + ".\n", None, (1, 0, 0, 0, 0)),
            "manh_bo_backtick": ("a.md", "Theo r2 " + CT0("r2:3 #c9a99cf5|dong ma ba co") + ".\n", None, (1, 0, 0, 0, 0)),
            "manh_gop_khoang_trang": ("a.md", "Theo r2 " + CT0("r2:2 #88a4ea24|dong mot co") + ".\n", None, (1, 0, 0, 0, 0)),
            "rao_code_bo_qua": ("a.md", "Theo r1:\n```\nr1 = " + Q2 + "dong hai co noi dung" + Q2 + "\n```\n", None, (0, 0, 0, 0, 0)),
            "rao_code_ngoai_rao_van_do": ("a.md", "Theo r1:\n```\nx = 1\n```\nr1 viet " + Q2 + "dong hai co noi dung" + Q2 + ".\n", None, (0, 0, 0, 1, 0)),
            "bang_tach_khoi_doan": ("a.md", "Theo r1 thi\n| " + Q2 + "dong hai co noi dung" + Q2 + " |\n", None, (0, 0, 0, 0, 0)),
            "bang_tu_nhac_ban": ("a.md", "Theo r1 thi\n| r1 | " + Q2 + "dong hai co noi dung" + Q2 + " |\n", None, (0, 0, 0, 1, 0)),
            "py_tach_doan": ("a.py", "def f():\n    " + Q2 * 3 + "Doan mot nhac r1 va du dai de qua nguong bon muoi ky tu.\n\n    Doan hai trich "
                             + Q2 + "dong hai co noi dung" + Q2 + " ma khong nhac ban nao ca.\n    " + Q2 * 3 + "\n", None, (0, 0, 0, 0, 0)),
        })
        hong = []
        for ten, (tep, doc, ham, mong) in ca.items():
            p = Path(t) / ten / tep; p.parent.mkdir(); p.write_text(doc, encoding="utf-8")
            d = kiem(t, "r{n}.md", p, ham)
            thuc = (d["DUNG"], d["LECH"], d["KHONG_DO_DUOC"], d["VI_PHAM"], d["CO_NHAN"])
            if thuc != mong: hong.append(f"{ten}: mong {mong}, thuc {thuc}")
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{len(ca) - len(hong)}/{len(ca)}")
        return 0 if not hong else 1
def main(a):
    if a[:1] == ["tu-kiem"]: return tu_kiem()
    cmd, co, rest, i = a[0], {}, [], 1
    while i < len(a):
        if a[i] in ("--nguon", "--mau", "--ham"): co[a[i]] = a[i + 1]; i += 2
        else: rest.append(a[i]); i += 1
    dir_, mau = co["--nguon"], co["--mau"]
    ham = set(co["--ham"].split(",")) if "--ham" in co else None
    if cmd == "sinh":
        n = int(rest[0].lstrip("r")); ab = rest[1].split("-"); print(sinh(dir_, mau, n, int(ab[0]), int(ab[-1]), rest[2] if len(rest) > 2 else None)); return 0
    if cmd == "tim":
        cum = re.sub(r"\s+", " ", rest[0]).strip(); n = 1
        while True:
            L = nguon(dir_, mau, n)
            if L is None: break
            for k, l in enumerate(L, 1):
                if cum in re.sub(r"\s+", " ", l): print(f"r{n}:{k} {sinh(dir_, mau, n, k, manh=cum) if len(bo_dau(cum)) >= 6 and bo_dau(cum) in bo_dau(l) else '(cum co dau markdown)'} {l.strip()[:100]}")
            n += 1
        return 0
    if cmd == "kiem":
        tong = {}
        for tep in rest:
            for k, v in kiem(dir_, mau, tep, ham).items(): tong[k] = tong.get(k, 0) + v
        print("TONG", tong); return 0 if tong["LECH"] == tong["VI_PHAM"] == tong["KHONG_DO_DUOC"] == 0 else 1
    raise SystemExit("lenh la: sinh | tim | kiem | tu-kiem")
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
```

## Phụ lục G — cổng CON TRỎ v4: tự kiểm theo MIỀN HỮU HẠN và qua CLI thật, §0.12 (MỚI ở r13, nguyên văn)

Cùng cách chạy như Phụ lục E; `tu-kiem` cho 60 ca (4 ca chạy CLI trong tiến trình con). So với Phụ lục F chỉ `tu_kiem` đổi. sha256 của khối mã dưới (tệp `con_tro.py`, không kể dòng rào): `8bf153249de92a99c740b7a84f200fb8485e82724ba20b9ae3dc3ee0f67a651e`.

```python
"""Con tro nguon cho dac ta R378 (r10 #574) — thay moi loi trich VIET TAY cua revision khac.

  CON TRO   ⟦rN:L #h|manh⟧ hoac ⟦rN:L-M #h|manh⟧ : dong L (den M) cua dac ta revision N; h = 8 hex dau cua
            sha256 noi dung cac dong ay sau chuan hoa (bo khoang trang dau/cuoi moi dong, gop khoang trang). Tro sai
            dong => h lech => DO. `manh` (BAT BUOC tu r11, >= 6 ky tu) la cum chu ma cau dan con tro dang noi toi; no
            phai NAM TRONG cac dong duoc tro (so sau khi bo `*` va dau backtick, gop khoang trang) — tro dung bam ma
            sai dong CAN TRO (F1d #574 luot 6: r3:322 thay vi 323-324) => DO. Sinh bang lenh `sinh`, KHONG go tay.
  NHAN NGUON ⟦nguon:K⟧ ngay sau mot chuoi trong ngoac: chuoi ay KHONG phai loi cua mot revision (K thuoc
            chi-thi | verdict | commit | ma | doctrine | issue). May KHONG kiem noi dung chuoi co nhan.
  LUAT      Trong moi KHOI (bang, doan, docstring) co nhac mot revision (token rN), MOI chuoi trong ngoac kep
            (thang hoac cong, >= 8 ky tu, vat nhieu dong duoc) PHAI mang nhan nguon. Chuoi thieu nhan => VI_PHAM.
            Loi cua revision khac chi duoc dan bang CON TRO, khong duoc dat trong ngoac.
Lenh:
  sinh  --nguon DIR --mau MAU rN L[-M]         in con tro cho dong ay
  tim   --nguon DIR --mau MAU "cum tu"         in con tro cua moi dong (moi revision) chua cum tu
  kiem  --nguon DIR --mau MAU TEP [TEP...]     .md: khoi markdown; .py: hang chuoi qua ast. rc=0 chi khi LECH=0,
                                               VI_PHAM=0, KHONG_DO_DUOC=0. In so da kiem theo ba trang thai.
  tu-kiem                                      ca am/duong tren nguon tam — cong phai DO duoc.
"""
import ast, hashlib, re, sys, tempfile
from pathlib import Path
CT = re.compile(r"⟦r(\d+):(\d+)(?:-(\d+))? #([0-9a-f]{8})(?:\|([^⟧]*))?⟧")
NHAN = re.compile(r"[*_]*\s*⟦nguon:(chi-thi|verdict|commit|ma|doctrine|issue)⟧")
Q = re.compile(r'"([^"]{8,}?)"|“([^”]{8,}?)”', re.S)
CODE = re.compile(r"`[^`\n]*`")
def che_code(k): return CODE.sub(lambda m: " " * len(m.group(0)), k)  # chuoi trong `code` la MA, khong phai loi trich
RV = re.compile(r"(?<![\w-])r\d+(?![\w])")
def chuan(ds): return "\n".join(re.sub(r"\s+", " ", x.strip()) for x in ds)
def bo_dau(x): return re.sub(r"\s+", " ", x.replace("*", "").replace("`", "")).strip()
def bam(ds): return hashlib.sha256(chuan(ds).encode("utf-8")).hexdigest()[:8]
def nguon(dir_, mau, n):
    p = Path(dir_) / mau.format(n=n)
    return p.read_text(encoding="utf-8").split("\n") if p.is_file() else None
def sinh(dir_, mau, n, a, b=None, manh=None):
    L = nguon(dir_, mau, n); b = b or a
    if L is None or not (1 <= a <= b <= len(L)): raise SystemExit(f"KHONG_DO_DUOC r{n}:{a}-{b}")
    if manh is None or len(bo_dau(manh)) < 6 or bo_dau(manh) not in bo_dau(" ".join(L[a-1:b])):
        raise SystemExit(f"MANH khong nam trong r{n}:{a}-{b}: {manh!r}")
    return f"⟦r{n}:{a}{'' if b == a else '-' + str(b)} #{bam(L[a-1:b])}|{bo_dau(manh)}⟧"
def khoi_md(van):
    L, kq, cur, dau, td, rao = van.split("\n"), [], [], 0, "", False
    def day():
        if cur: kq.append((dau + 1, td, "\n".join(cur)))
    for i, l in enumerate(L):
        if l.lstrip().startswith("```"):
            day(); cur.clear(); rao = not rao; continue
        if rao: continue
        bang = l.lstrip().startswith("|")
        if re.match(r"#{1,6} ", l):   # tieu de Markdown THAT (`#` + khoang trang); `#574 viet ...` khong phai tieu de
            day(); cur.clear(); td = l; continue
        if not l.strip() or (cur and bang != cur[-1].lstrip().startswith("|")):
            day(); cur.clear()
            if not l.strip(): continue
        if not cur: dau = i
        cur.append(l)
    day(); return kq
def khoi_py(van, ham=None):
    """Hang chuoi > 40 ky tu; `ham` (tap ten) gioi han vao than cac ham ay — write set chi cho sua mot so ham."""
    kq = []; goc = ast.parse(van)
    vung = [(f.lineno, f.end_lineno) for f in ast.walk(goc) if isinstance(f, ast.FunctionDef) and f.name in ham] if ham else None
    for n in ast.walk(goc):
        if vung is not None and not any(a <= n.lineno <= b for a, b in vung if hasattr(n, "lineno")): continue
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) > 40:
            off = 0
            for doan in re.split(r"(\n\s*\n)", n.value):
                if doan.strip() and not re.fullmatch(r"\n\s*\n", doan):
                    kq.append((n.lineno + n.value[:off].count("\n"), "", doan))
                off += len(doan)
    return kq
def kiem(dir_, mau, tep, ham=None):
    van = Path(tep).read_text(encoding="utf-8"); dem = {"DUNG": 0, "LECH": 0, "KHONG_DO_DUOC": 0, "VI_PHAM": 0, "CO_NHAN": 0}
    for m in CT.finditer(van):
        n, a, b, h = int(m.group(1)), int(m.group(2)), int(m.group(3) or m.group(2)), m.group(4)
        d = van[:m.start()].count("\n") + 1
        L = nguon(dir_, mau, n)
        if L is None: dem["KHONG_DO_DUOC"] += 1; print(f"KHONG_DO_DUOC {tep}:{d} {m.group(0)} (khong co tep r{n})"); continue
        if not (1 <= a <= b <= len(L)): dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (ngoai pham vi 1..{len(L)})"); continue
        if bam(L[a-1:b]) != h: dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (bam that {bam(L[a-1:b])})"); continue
        manh = m.group(5)
        if manh is None or len(bo_dau(manh)) < 6:
            dem["VI_PHAM"] += 1; print(f"VI_PHAM {tep}:{d} {m.group(0)} (thieu manh neo, hoac ngan hon 6 ky tu)"); continue
        if bo_dau(manh or "") not in bo_dau(" ".join(L[a-1:b])):
            dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (manh KHONG nam trong dong duoc tro)"); continue
        dem["DUNG"] += 1
    for dong, td, k in (khoi_py(van, ham) if str(tep).endswith(".py") else khoi_md(van)):
        if not (RV.search(k) or RV.search(td)): continue
        kc = k if str(tep).endswith(".py") else che_code(k)
        for m in Q.finditer(kc):
            if NHAN.match(k, m.end()): dem["CO_NHAN"] += 1; continue
            dem["VI_PHAM"] += 1
            print(f"VI_PHAM {tep}:{dong + k[:m.start()].count(chr(10))} chuoi trong ngoac khong nhan nguon: {(m.group(1) or m.group(2))[:90]!r}")
    return dem
def tu_kiem():
    """r12: them BANG LOP DAU VAO (pham vi dong, ngoac cong, nhan, do dai manh, dau markup, span, rao code, bien bang,
    doan docstring) voi con tro viet san — 11 dot bien song cua #574 luot 7 phai DO.
    Ca am/duong voi BO DEM KY VONG chinh xac (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN) — khong chi dat/khong
    dat. Phu MOI nhanh dau vao duoc dung cho hop dong: .md than doan, .md chi co token o TIEU DE, .py qua ast, .py voi
    --ham (vi pham ngoai ham bi bo qua), manh neo. Tung la lo cua r10 (#574 luot 6, F2): bo han nhanh .py hoac vi
    tieu de ma tu kiem van 8/8."""
    import hashlib as _h
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "r1.md").write_text("dong mot\ndong hai co noi dung\ndong ba co cum khac\ndong bon co noi dung\n", encoding="utf-8")
        (Path(t) / "r3.md").write_text("".join(f"dong so {i} co noi dung\n" for i in range(1, 13)), encoding="utf-8")
        (Path(t) / "r12.md").write_text("dong muoi hai co noi dung\n", encoding="utf-8")
        (Path(t) / "r2.md").write_text("dong **mot** co noi dung\ndong mot  co noi dung\ndong `ma ba` co chu\n", encoding="utf-8")
        ct = sinh(t, "r{n}.md", 1, 2, manh="hai co noi dung")
        sai_manh = ct.replace("|hai co noi dung", "|ba co cum khac")
        khong_manh = ct.split("|")[0] + "⟧"
        Q2 = chr(34)
        py_xau = "def f():\n    " + Q2 * 3 + "Docstring noi ve r1: " + Q2 + "dong hai co noi dung" + Q2 + " khong nhan, du dai de qua nguong 40.\n    " + Q2 * 3 + "\n\n\ndef g():\n    " + Q2 * 3 + "Ham ngoai pham vi nhac r1: " + Q2 + "dong ba co cum khac" + Q2 + " khong nhan, du dai.\n    " + Q2 * 3 + "\n"
        ca = {  # ten: (ten tep, noi dung, --ham, ky vong (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN))
            "duong": ("a.md", f"Theo r1 {ct} thi dung.\n", None, (1, 0, 0, 0, 0)),
            "sai_dong": ("a.md", f"Theo r1 {ct.replace(':2 ', ':3 ')} thi sai.\n", None, (0, 1, 0, 0, 0)),
            "ngoai_pham_vi": ("a.md", f"Theo r1 {ct.replace(':2 ', ':9 ')}.\n", None, (0, 1, 0, 0, 0)),
            "thieu_tep": ("a.md", f"Theo r1 {ct.replace('⟦r1', '⟦r7')}.\n", None, (0, 0, 1, 0, 0)),
            "sai_bam_manh_van_khop": ("a.md", f"Theo r1 {sinh(t, 'r{n}.md', 1, 2, manh='co noi dung').replace(':2 ', ':4 ')}.\n", None, (0, 1, 0, 0, 0)),
            "sai_manh_dung_bam": ("a.md", f"Theo r1 {sai_manh}.\n", None, (0, 1, 0, 0, 0)),
            "thieu_manh": ("a.md", f"Theo r1 {khong_manh}.\n", None, (0, 0, 0, 1, 0)),
            "trich_khong_nhan": ("a.md", "Theo r1 thi " + Q2 + "dong hai co noi dung" + Q2 + " la loi cua no.\n", None, (0, 0, 0, 1, 0)),
            "trich_co_nhan": ("a.md", "Theo r1, chu kho noi " + Q2 + "lam tiep di nhe" + Q2 + " ⟦nguon:chi-thi⟧.\n", None, (0, 0, 0, 0, 1)),
            "vat_dong": ("a.md", "r1 viet " + Q2 + "dong hai\nco noi dung" + Q2 + " khong nhan.\n", None, (0, 0, 0, 1, 0)),
            "trong_code": ("a.md", "r1 dung `x == " + Q2 + "dong hai co noi dung" + Q2 + "` trong ma.\n", None, (0, 0, 0, 0, 0)),
            "chi_tieu_de": ("a.md", "## Nhan xet ve r1\n\nKhoi nay khong nhac ban nao ma viet " + Q2 + "dong hai co noi dung" + Q2 + ".\n", None, (0, 0, 0, 1, 0)),
            "gach_so_khong_phai_tieu_de": ("a.md", "Theo r1 thi\n#574 noi " + Q2 + "dong hai co noi dung" + Q2 + " khong nhan.\n", None, (0, 0, 0, 1, 0)),
            "py_docstring": ("a.py", py_xau, None, (0, 0, 0, 2, 0)),
            "py_ham": ("a.py", py_xau, {"f"}, (0, 0, 0, 1, 0)),
        }
        # r12 (#574 luot 7, F2): BANG LOP DAU VAO — moi truc mot cap am/duong. Con tro VIET SAN, bam tinh DOC LAP
        # (hashlib tren chuoi da chuan hoa bang tay) — KHONG sinh bang `sinh`/`bam`, de oracle khong di qua ham bi dot bien.
        CT0 = lambda x: chr(0x27E6) + x + chr(0x27E7)  # dung con tro luc chay: tep KHONG chua con tro lien, vi `kiem` quet ca khoi ma
        ca.update({
            "pv_duong_1_dong": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|hai co noi dung") + ".\n", None, (1, 0, 0, 0, 0)),
            "pv_cuoi_vuot_toan_tep": ("a.md", "Theo r1 " + CT0("r1:1-999 #7aad2135|dong mot dong hai") + ".\n", None, (0, 1, 0, 0, 0)),
            "pv_cuoi_vuot_mot_phan": ("a.md", "Theo r1 " + CT0("r1:2-9 #04a7a73c|hai co noi dung") + ".\n", None, (0, 1, 0, 0, 0)),
            "pv_dau_0": ("a.md", "Theo r1 " + CT0("r1:0-2 #e3b0c442|hai co noi dung") + ".\n", None, (0, 1, 0, 0, 0)),
            "pv_dao": ("a.md", "Theo r1 " + CT0("r1:3-2 #e3b0c442|hai co noi dung") + ".\n", None, (0, 1, 0, 0, 0)),
            "span_nhieu_dong_duong": ("a.md", "Theo r1 " + CT0("r1:2-3 #f4d0ba3e|noi dung dong ba") + ".\n", None, (1, 0, 0, 0, 0)),
            "ngoac_cong_am": ("a.md", "Theo r1: “dong hai co noi dung”.\n", None, (0, 0, 0, 1, 0)),
            "ngoac_cong_co_nhan": ("a.md", "Theo r1: “dong hai co noi dung” ⟦nguon:verdict⟧.\n", None, (0, 0, 0, 0, 1)),
            "nhan_khong_hop_le": ("a.md", "Theo r1: " + Q2 + "dong hai co noi dung" + Q2 + " ⟦nguon:khong-hop-le⟧.\n", None, (0, 0, 0, 1, 0)),
            "manh_6_duong": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|hai co") + ".\n", None, (1, 0, 0, 0, 0)),
            "manh_4_am": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|dong") + ".\n", None, (0, 0, 0, 1, 0)),
            "manh_bo_sao": ("a.md", "Theo r2 " + CT0("r2:1 #457257c7|dong mot co") + ".\n", None, (1, 0, 0, 0, 0)),
            "manh_bo_backtick": ("a.md", "Theo r2 " + CT0("r2:3 #c9a99cf5|dong ma ba co") + ".\n", None, (1, 0, 0, 0, 0)),
            "manh_gop_khoang_trang": ("a.md", "Theo r2 " + CT0("r2:2 #88a4ea24|dong mot co") + ".\n", None, (1, 0, 0, 0, 0)),
            "rao_code_bo_qua": ("a.md", "Theo r1:\n```\nr1 = " + Q2 + "dong hai co noi dung" + Q2 + "\n```\n", None, (0, 0, 0, 0, 0)),
            "rao_code_ngoai_rao_van_do": ("a.md", "Theo r1:\n```\nx = 1\n```\nr1 viet " + Q2 + "dong hai co noi dung" + Q2 + ".\n", None, (0, 0, 0, 1, 0)),
            "bang_tach_khoi_doan": ("a.md", "Theo r1 thi\n| " + Q2 + "dong hai co noi dung" + Q2 + " |\n", None, (0, 0, 0, 0, 0)),
            "bang_tu_nhac_ban": ("a.md", "Theo r1 thi\n| r1 | " + Q2 + "dong hai co noi dung" + Q2 + " |\n", None, (0, 0, 0, 1, 0)),
            "py_tach_doan": ("a.py", "def f():\n    " + Q2 * 3 + "Doan mot nhac r1 va du dai de qua nguong bon muoi ky tu.\n\n    Doan hai trich "
                             + Q2 + "dong hai co noi dung" + Q2 + " ma khong nhac ban nao ca.\n    " + Q2 * 3 + "\n", None, (0, 0, 0, 0, 0)),
        })
        # r13 (#574 luot 8, F2): MIEN HUU HAN theo cu phap duoc ho tro — so revision/dong MOT va NHIEU chu so, token dung
        # rieng va nam trong tu, trich 7/8/9 ky tu x hai kieu ngoac, TUNG nhan hop le, MOI cap tieu de, rao 3/4 backtick co
        # thong tin. Bam viet san (hashlib tren chuoi chuan hoa tay), khong qua `sinh`/`bam`.
        Q8, C8 = Q2 + "abcdefgh" + Q2, "“abcdefgh”"
        ca.update({
            "rv_hai_chu_so_con_tro": ("a.md", "Theo r12 " + CT0("r12:1 #afdc1a0a|muoi hai co noi dung") + ".\n", None, (1, 0, 0, 0, 0)),
            "dong_hai_chu_so_con_tro": ("a.md", "Theo r3 " + CT0("r3:12 #ab858a93|so 12 co noi dung") + ".\n", None, (1, 0, 0, 0, 0)),
            "span_hai_chu_so": ("a.md", "Theo r3 " + CT0("r3:10-11 #20031634|so 10 co noi dung") + ".\n", None, (1, 0, 0, 0, 0)),
            "dong_hai_chu_so_sai_bam": ("a.md", "Theo r3 " + CT0("r3:12 #00000000|so 12 co noi dung") + ".\n", None, (0, 1, 0, 0, 0)),
            "rv_hai_chu_so_token": ("a.md", "Theo r12: " + Q8 + ".\n", None, (0, 0, 0, 1, 0)),
            "rv_trong_tu_khong_phai_token": ("a.md", "Theo error1 va r1x: " + Q8 + ".\n", None, (0, 0, 0, 0, 0)),
            "trich_7_thang": ("a.md", "Theo r1: " + Q2 + "abcdefg" + Q2 + ".\n", None, (0, 0, 0, 0, 0)),
            "trich_8_thang": ("a.md", "Theo r1: " + Q8 + ".\n", None, (0, 0, 0, 1, 0)),
            "trich_9_thang": ("a.md", "Theo r1: " + Q2 + "abcdefghi" + Q2 + ".\n", None, (0, 0, 0, 1, 0)),
            "trich_7_cong": ("a.md", "Theo r1: “abcdefg”.\n", None, (0, 0, 0, 0, 0)),
            "trich_8_cong": ("a.md", "Theo r1: " + C8 + ".\n", None, (0, 0, 0, 1, 0)),
            "trich_9_cong": ("a.md", "Theo r1: “abcdefghi”.\n", None, (0, 0, 0, 1, 0)),
            "moi_nhan_hop_le": ("a.md", "Theo r1: " + " ".join(Q8 + " " + chr(0x27E6) + "nguon:" + k + chr(0x27E7)
                                for k in ("chi-thi", "verdict", "commit", "ma", "doctrine", "issue")) + ".\n", None, (0, 0, 0, 0, 6)),
            **{f"tieu_de_cap_{n}": ("a.md", "#" * n + " Nhan xet r1\n\nDoan nay viet " + Q8 + ".\n", None, (0, 0, 0, 1, 0)) for n in range(1, 7)},
            "bay_thang_khong_phai_tieu_de": ("a.md", "####### Nhan xet r1\n\nDoan nay viet " + Q8 + ".\n", None, (0, 0, 0, 0, 0)),
            "rao_3_co_thong_tin": ("a.md", "```python\nr1 = " + Q8 + "\n```\n", None, (0, 0, 0, 0, 0)),
            "rao_4_co_thong_tin": ("a.md", "````python\nr1 = " + Q8 + "\n````\n", None, (0, 0, 0, 0, 0)),
        })
        hong = []
        for ten, (tep, doc, ham, mong) in ca.items():
            p = Path(t) / ten / tep; p.parent.mkdir(); p.write_text(doc, encoding="utf-8")
            d = kiem(t, "r{n}.md", p, ham)
            thuc = (d["DUNG"], d["LECH"], d["KHONG_DO_DUOC"], d["VI_PHAM"], d["CO_NHAN"])
            if thuc != mong: hong.append(f"{ten}: mong {mong}, thuc {thuc}")
        # CLI THAT (tien trinh con, qua `main`): khoa lop chuyen tham so, ke ca `--ham` mot/nhieu ten. Ky vong: (rc, TONG).
        import subprocess as _sp
        py_cli = ("def f():\n    " + Q2 * 3 + "Ham f nhac r1 va khong trich gi ca, du dai de qua nguong bon muoi.\n    " + Q2 * 3
                  + "\n\n\ndef g():\n    " + Q2 * 3 + "Ham g nhac r1: " + Q8 + " khong nhan, du dai de qua nguong.\n    " + Q2 * 3 + "\n")
        (Path(t) / "cli").mkdir(); pc = Path(t) / "cli" / "a.py"; pc.write_text(py_cli, encoding="utf-8")
        pm = Path(t) / "cli" / "b.md"; pm.write_text("Theo r3 " + CT0("r3:12 #ab858a93|so 12 co noi dung") + ".\n", encoding="utf-8")
        cli = {"cli_ham_f": (["--ham", "f", str(pc)], 0, (0, 0, 0, 0, 0)), "cli_ham_f_g": (["--ham", "f,g", str(pc)], 1, (0, 0, 0, 1, 0)),
               "cli_khong_ham": ([str(pc)], 1, (0, 0, 0, 1, 0)), "cli_con_tro_hai_chu_so": ([str(pm)], 0, (1, 0, 0, 0, 0))}
        for ten, (doi, rc_mong, mong) in cli.items():
            r = _sp.run([sys.executable, "-B", str(Path(__file__).resolve()), "kiem", "--nguon", t, "--mau", "r{n}.md", *doi],
                        capture_output=True, text=True)
            tong = [x for x in r.stdout.splitlines() if x.startswith("TONG ")]
            d = ast.literal_eval(tong[-1][5:]) if tong else {}
            thuc = (r.returncode, tuple(d.get(k) for k in ("DUNG", "LECH", "KHONG_DO_DUOC", "VI_PHAM", "CO_NHAN")))
            if thuc != (rc_mong, mong): hong.append(f"{ten}: mong {(rc_mong, mong)}, thuc {thuc}")
        n_ca = len(ca) + len(cli)
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{n_ca - len(hong)}/{n_ca}")
        return 0 if not hong else 1
def main(a):
    if a[:1] == ["tu-kiem"]: return tu_kiem()
    cmd, co, rest, i = a[0], {}, [], 1
    while i < len(a):
        if a[i] in ("--nguon", "--mau", "--ham"): co[a[i]] = a[i + 1]; i += 2
        else: rest.append(a[i]); i += 1
    dir_, mau = co["--nguon"], co["--mau"]
    ham = set(co["--ham"].split(",")) if "--ham" in co else None
    if cmd == "sinh":
        n = int(rest[0].lstrip("r")); ab = rest[1].split("-"); print(sinh(dir_, mau, n, int(ab[0]), int(ab[-1]), rest[2] if len(rest) > 2 else None)); return 0
    if cmd == "tim":
        cum = re.sub(r"\s+", " ", rest[0]).strip(); n = 1
        while True:
            L = nguon(dir_, mau, n)
            if L is None: break
            for k, l in enumerate(L, 1):
                if cum in re.sub(r"\s+", " ", l): print(f"r{n}:{k} {sinh(dir_, mau, n, k, manh=cum) if len(bo_dau(cum)) >= 6 and bo_dau(cum) in bo_dau(l) else '(cum co dau markdown)'} {l.strip()[:100]}")
            n += 1
        return 0
    if cmd == "kiem":
        tong = {}
        for tep in rest:
            for k, v in kiem(dir_, mau, tep, ham).items(): tong[k] = tong.get(k, 0) + v
        print("TONG", tong); return 0 if tong["LECH"] == tong["VI_PHAM"] == tong["KHONG_DO_DUOC"] == 0 else 1
    raise SystemExit("lenh la: sinh | tim | kiem | tu-kiem")
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
```

## Phụ lục H — cổng CON TRỎ v5: ma trận hợp đồng CLI và bốn cặp parser, §0.13 (MỚI ở r14, nguyên văn)

Cùng cách chạy như Phụ lục E; `tu-kiem` cho 73 ca (14 ca chạy CLI trong tiến trình con). So với Phụ lục G chỉ `tu_kiem` đổi. sha256 của khối mã dưới (tệp `con_tro.py`, không kể dòng rào): `efadecb873d7b45b255f3a89fff736cfbd93ead364e3ecf9094ffce6ad1d097b`.

```python
"""Con tro nguon cho dac ta R378 (r10 #574) — thay moi loi trich VIET TAY cua revision khac.

  CON TRO   ⟦rN:L #h|manh⟧ hoac ⟦rN:L-M #h|manh⟧ : dong L (den M) cua dac ta revision N; h = 8 hex dau cua
            sha256 noi dung cac dong ay sau chuan hoa (bo khoang trang dau/cuoi moi dong, gop khoang trang). Tro sai
            dong => h lech => DO. `manh` (BAT BUOC tu r11, >= 6 ky tu) la cum chu ma cau dan con tro dang noi toi; no
            phai NAM TRONG cac dong duoc tro (so sau khi bo `*` va dau backtick, gop khoang trang) — tro dung bam ma
            sai dong CAN TRO (F1d #574 luot 6: r3:322 thay vi 323-324) => DO. Sinh bang lenh `sinh`, KHONG go tay.
  NHAN NGUON ⟦nguon:K⟧ ngay sau mot chuoi trong ngoac: chuoi ay KHONG phai loi cua mot revision (K thuoc
            chi-thi | verdict | commit | ma | doctrine | issue). May KHONG kiem noi dung chuoi co nhan.
  LUAT      Trong moi KHOI (bang, doan, docstring) co nhac mot revision (token rN), MOI chuoi trong ngoac kep
            (thang hoac cong, >= 8 ky tu, vat nhieu dong duoc) PHAI mang nhan nguon. Chuoi thieu nhan => VI_PHAM.
            Loi cua revision khac chi duoc dan bang CON TRO, khong duoc dat trong ngoac.
Lenh:
  sinh  --nguon DIR --mau MAU rN L[-M]         in con tro cho dong ay
  tim   --nguon DIR --mau MAU "cum tu"         in con tro cua moi dong (moi revision) chua cum tu
  kiem  --nguon DIR --mau MAU TEP [TEP...]     .md: khoi markdown; .py: hang chuoi qua ast. rc=0 chi khi LECH=0,
                                               VI_PHAM=0, KHONG_DO_DUOC=0. In so da kiem theo ba trang thai.
  tu-kiem                                      ca am/duong tren nguon tam — cong phai DO duoc.
"""
import ast, hashlib, re, sys, tempfile
from pathlib import Path
CT = re.compile(r"⟦r(\d+):(\d+)(?:-(\d+))? #([0-9a-f]{8})(?:\|([^⟧]*))?⟧")
NHAN = re.compile(r"[*_]*\s*⟦nguon:(chi-thi|verdict|commit|ma|doctrine|issue)⟧")
Q = re.compile(r'"([^"]{8,}?)"|“([^”]{8,}?)”', re.S)
CODE = re.compile(r"`[^`\n]*`")
def che_code(k): return CODE.sub(lambda m: " " * len(m.group(0)), k)  # chuoi trong `code` la MA, khong phai loi trich
RV = re.compile(r"(?<![\w-])r\d+(?![\w])")
def chuan(ds): return "\n".join(re.sub(r"\s+", " ", x.strip()) for x in ds)
def bo_dau(x): return re.sub(r"\s+", " ", x.replace("*", "").replace("`", "")).strip()
def bam(ds): return hashlib.sha256(chuan(ds).encode("utf-8")).hexdigest()[:8]
def nguon(dir_, mau, n):
    p = Path(dir_) / mau.format(n=n)
    return p.read_text(encoding="utf-8").split("\n") if p.is_file() else None
def sinh(dir_, mau, n, a, b=None, manh=None):
    L = nguon(dir_, mau, n); b = b or a
    if L is None or not (1 <= a <= b <= len(L)): raise SystemExit(f"KHONG_DO_DUOC r{n}:{a}-{b}")
    if manh is None or len(bo_dau(manh)) < 6 or bo_dau(manh) not in bo_dau(" ".join(L[a-1:b])):
        raise SystemExit(f"MANH khong nam trong r{n}:{a}-{b}: {manh!r}")
    return f"⟦r{n}:{a}{'' if b == a else '-' + str(b)} #{bam(L[a-1:b])}|{bo_dau(manh)}⟧"
def khoi_md(van):
    L, kq, cur, dau, td, rao = van.split("\n"), [], [], 0, "", False
    def day():
        if cur: kq.append((dau + 1, td, "\n".join(cur)))
    for i, l in enumerate(L):
        if l.lstrip().startswith("```"):
            day(); cur.clear(); rao = not rao; continue
        if rao: continue
        bang = l.lstrip().startswith("|")
        if re.match(r"#{1,6} ", l):   # tieu de Markdown THAT (`#` + khoang trang); `#574 viet ...` khong phai tieu de
            day(); cur.clear(); td = l; continue
        if not l.strip() or (cur and bang != cur[-1].lstrip().startswith("|")):
            day(); cur.clear()
            if not l.strip(): continue
        if not cur: dau = i
        cur.append(l)
    day(); return kq
def khoi_py(van, ham=None):
    """Hang chuoi > 40 ky tu; `ham` (tap ten) gioi han vao than cac ham ay — write set chi cho sua mot so ham."""
    kq = []; goc = ast.parse(van)
    vung = [(f.lineno, f.end_lineno) for f in ast.walk(goc) if isinstance(f, ast.FunctionDef) and f.name in ham] if ham else None
    for n in ast.walk(goc):
        if vung is not None and not any(a <= n.lineno <= b for a, b in vung if hasattr(n, "lineno")): continue
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) > 40:
            off = 0
            for doan in re.split(r"(\n\s*\n)", n.value):
                if doan.strip() and not re.fullmatch(r"\n\s*\n", doan):
                    kq.append((n.lineno + n.value[:off].count("\n"), "", doan))
                off += len(doan)
    return kq
def kiem(dir_, mau, tep, ham=None):
    van = Path(tep).read_text(encoding="utf-8"); dem = {"DUNG": 0, "LECH": 0, "KHONG_DO_DUOC": 0, "VI_PHAM": 0, "CO_NHAN": 0}
    for m in CT.finditer(van):
        n, a, b, h = int(m.group(1)), int(m.group(2)), int(m.group(3) or m.group(2)), m.group(4)
        d = van[:m.start()].count("\n") + 1
        L = nguon(dir_, mau, n)
        if L is None: dem["KHONG_DO_DUOC"] += 1; print(f"KHONG_DO_DUOC {tep}:{d} {m.group(0)} (khong co tep r{n})"); continue
        if not (1 <= a <= b <= len(L)): dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (ngoai pham vi 1..{len(L)})"); continue
        if bam(L[a-1:b]) != h: dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (bam that {bam(L[a-1:b])})"); continue
        manh = m.group(5)
        if manh is None or len(bo_dau(manh)) < 6:
            dem["VI_PHAM"] += 1; print(f"VI_PHAM {tep}:{d} {m.group(0)} (thieu manh neo, hoac ngan hon 6 ky tu)"); continue
        if bo_dau(manh or "") not in bo_dau(" ".join(L[a-1:b])):
            dem["LECH"] += 1; print(f"LECH {tep}:{d} {m.group(0)} (manh KHONG nam trong dong duoc tro)"); continue
        dem["DUNG"] += 1
    for dong, td, k in (khoi_py(van, ham) if str(tep).endswith(".py") else khoi_md(van)):
        if not (RV.search(k) or RV.search(td)): continue
        kc = k if str(tep).endswith(".py") else che_code(k)
        for m in Q.finditer(kc):
            if NHAN.match(k, m.end()): dem["CO_NHAN"] += 1; continue
            dem["VI_PHAM"] += 1
            print(f"VI_PHAM {tep}:{dong + k[:m.start()].count(chr(10))} chuoi trong ngoac khong nhan nguon: {(m.group(1) or m.group(2))[:90]!r}")
    return dem
def tu_kiem():
    """r12: them BANG LOP DAU VAO (pham vi dong, ngoac cong, nhan, do dai manh, dau markup, span, rao code, bien bang,
    doan docstring) voi con tro viet san — 11 dot bien song cua #574 luot 7 phai DO.
    Ca am/duong voi BO DEM KY VONG chinh xac (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN) — khong chi dat/khong
    dat. Phu MOI nhanh dau vao duoc dung cho hop dong: .md than doan, .md chi co token o TIEU DE, .py qua ast, .py voi
    --ham (vi pham ngoai ham bi bo qua), manh neo. Tung la lo cua r10 (#574 luot 6, F2): bo han nhanh .py hoac vi
    tieu de ma tu kiem van 8/8."""
    import hashlib as _h
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "r1.md").write_text("dong mot\ndong hai co noi dung\ndong ba co cum khac\ndong bon co noi dung\n", encoding="utf-8")
        (Path(t) / "r3.md").write_text("".join(f"dong so {i} co noi dung\n" for i in range(1, 13)), encoding="utf-8")
        (Path(t) / "r12.md").write_text("dong muoi hai co noi dung\n", encoding="utf-8")
        (Path(t) / "r2.md").write_text("dong **mot** co noi dung\ndong mot  co noi dung\ndong `ma ba` co chu\n", encoding="utf-8")
        ct = sinh(t, "r{n}.md", 1, 2, manh="hai co noi dung")
        sai_manh = ct.replace("|hai co noi dung", "|ba co cum khac")
        khong_manh = ct.split("|")[0] + "⟧"
        Q2 = chr(34)
        py_xau = "def f():\n    " + Q2 * 3 + "Docstring noi ve r1: " + Q2 + "dong hai co noi dung" + Q2 + " khong nhan, du dai de qua nguong 40.\n    " + Q2 * 3 + "\n\n\ndef g():\n    " + Q2 * 3 + "Ham ngoai pham vi nhac r1: " + Q2 + "dong ba co cum khac" + Q2 + " khong nhan, du dai.\n    " + Q2 * 3 + "\n"
        ca = {  # ten: (ten tep, noi dung, --ham, ky vong (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN))
            "duong": ("a.md", f"Theo r1 {ct} thi dung.\n", None, (1, 0, 0, 0, 0)),
            "sai_dong": ("a.md", f"Theo r1 {ct.replace(':2 ', ':3 ')} thi sai.\n", None, (0, 1, 0, 0, 0)),
            "ngoai_pham_vi": ("a.md", f"Theo r1 {ct.replace(':2 ', ':9 ')}.\n", None, (0, 1, 0, 0, 0)),
            "thieu_tep": ("a.md", f"Theo r1 {ct.replace('⟦r1', '⟦r7')}.\n", None, (0, 0, 1, 0, 0)),
            "sai_bam_manh_van_khop": ("a.md", f"Theo r1 {sinh(t, 'r{n}.md', 1, 2, manh='co noi dung').replace(':2 ', ':4 ')}.\n", None, (0, 1, 0, 0, 0)),
            "sai_manh_dung_bam": ("a.md", f"Theo r1 {sai_manh}.\n", None, (0, 1, 0, 0, 0)),
            "thieu_manh": ("a.md", f"Theo r1 {khong_manh}.\n", None, (0, 0, 0, 1, 0)),
            "trich_khong_nhan": ("a.md", "Theo r1 thi " + Q2 + "dong hai co noi dung" + Q2 + " la loi cua no.\n", None, (0, 0, 0, 1, 0)),
            "trich_co_nhan": ("a.md", "Theo r1, chu kho noi " + Q2 + "lam tiep di nhe" + Q2 + " ⟦nguon:chi-thi⟧.\n", None, (0, 0, 0, 0, 1)),
            "vat_dong": ("a.md", "r1 viet " + Q2 + "dong hai\nco noi dung" + Q2 + " khong nhan.\n", None, (0, 0, 0, 1, 0)),
            "trong_code": ("a.md", "r1 dung `x == " + Q2 + "dong hai co noi dung" + Q2 + "` trong ma.\n", None, (0, 0, 0, 0, 0)),
            "chi_tieu_de": ("a.md", "## Nhan xet ve r1\n\nKhoi nay khong nhac ban nao ma viet " + Q2 + "dong hai co noi dung" + Q2 + ".\n", None, (0, 0, 0, 1, 0)),
            "gach_so_khong_phai_tieu_de": ("a.md", "Theo r1 thi\n#574 noi " + Q2 + "dong hai co noi dung" + Q2 + " khong nhan.\n", None, (0, 0, 0, 1, 0)),
            "py_docstring": ("a.py", py_xau, None, (0, 0, 0, 2, 0)),
            "py_ham": ("a.py", py_xau, {"f"}, (0, 0, 0, 1, 0)),
        }
        # r12 (#574 luot 7, F2): BANG LOP DAU VAO — moi truc mot cap am/duong. Con tro VIET SAN, bam tinh DOC LAP
        # (hashlib tren chuoi da chuan hoa bang tay) — KHONG sinh bang `sinh`/`bam`, de oracle khong di qua ham bi dot bien.
        CT0 = lambda x: chr(0x27E6) + x + chr(0x27E7)  # dung con tro luc chay: tep KHONG chua con tro lien, vi `kiem` quet ca khoi ma
        ca.update({
            "pv_duong_1_dong": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|hai co noi dung") + ".\n", None, (1, 0, 0, 0, 0)),
            "pv_cuoi_vuot_toan_tep": ("a.md", "Theo r1 " + CT0("r1:1-999 #7aad2135|dong mot dong hai") + ".\n", None, (0, 1, 0, 0, 0)),
            "pv_cuoi_vuot_mot_phan": ("a.md", "Theo r1 " + CT0("r1:2-9 #04a7a73c|hai co noi dung") + ".\n", None, (0, 1, 0, 0, 0)),
            "pv_dau_0": ("a.md", "Theo r1 " + CT0("r1:0-2 #e3b0c442|hai co noi dung") + ".\n", None, (0, 1, 0, 0, 0)),
            "pv_dao": ("a.md", "Theo r1 " + CT0("r1:3-2 #e3b0c442|hai co noi dung") + ".\n", None, (0, 1, 0, 0, 0)),
            "span_nhieu_dong_duong": ("a.md", "Theo r1 " + CT0("r1:2-3 #f4d0ba3e|noi dung dong ba") + ".\n", None, (1, 0, 0, 0, 0)),
            "ngoac_cong_am": ("a.md", "Theo r1: “dong hai co noi dung”.\n", None, (0, 0, 0, 1, 0)),
            "ngoac_cong_co_nhan": ("a.md", "Theo r1: “dong hai co noi dung” ⟦nguon:verdict⟧.\n", None, (0, 0, 0, 0, 1)),
            "nhan_khong_hop_le": ("a.md", "Theo r1: " + Q2 + "dong hai co noi dung" + Q2 + " ⟦nguon:khong-hop-le⟧.\n", None, (0, 0, 0, 1, 0)),
            "manh_6_duong": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|hai co") + ".\n", None, (1, 0, 0, 0, 0)),
            "manh_4_am": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|dong") + ".\n", None, (0, 0, 0, 1, 0)),
            "manh_bo_sao": ("a.md", "Theo r2 " + CT0("r2:1 #457257c7|dong mot co") + ".\n", None, (1, 0, 0, 0, 0)),
            "manh_bo_backtick": ("a.md", "Theo r2 " + CT0("r2:3 #c9a99cf5|dong ma ba co") + ".\n", None, (1, 0, 0, 0, 0)),
            "manh_gop_khoang_trang": ("a.md", "Theo r2 " + CT0("r2:2 #88a4ea24|dong mot co") + ".\n", None, (1, 0, 0, 0, 0)),
            "rao_code_bo_qua": ("a.md", "Theo r1:\n```\nr1 = " + Q2 + "dong hai co noi dung" + Q2 + "\n```\n", None, (0, 0, 0, 0, 0)),
            "rao_code_ngoai_rao_van_do": ("a.md", "Theo r1:\n```\nx = 1\n```\nr1 viet " + Q2 + "dong hai co noi dung" + Q2 + ".\n", None, (0, 0, 0, 1, 0)),
            "bang_tach_khoi_doan": ("a.md", "Theo r1 thi\n| " + Q2 + "dong hai co noi dung" + Q2 + " |\n", None, (0, 0, 0, 0, 0)),
            "bang_tu_nhac_ban": ("a.md", "Theo r1 thi\n| r1 | " + Q2 + "dong hai co noi dung" + Q2 + " |\n", None, (0, 0, 0, 1, 0)),
            "py_tach_doan": ("a.py", "def f():\n    " + Q2 * 3 + "Doan mot nhac r1 va du dai de qua nguong bon muoi ky tu.\n\n    Doan hai trich "
                             + Q2 + "dong hai co noi dung" + Q2 + " ma khong nhac ban nao ca.\n    " + Q2 * 3 + "\n", None, (0, 0, 0, 0, 0)),
        })
        # r13 (#574 luot 8, F2): MIEN HUU HAN theo cu phap duoc ho tro — so revision/dong MOT va NHIEU chu so, token dung
        # rieng va nam trong tu, trich 7/8/9 ky tu x hai kieu ngoac, TUNG nhan hop le, MOI cap tieu de, rao 3/4 backtick co
        # thong tin. Bam viet san (hashlib tren chuoi chuan hoa tay), khong qua `sinh`/`bam`.
        Q8, C8 = Q2 + "abcdefgh" + Q2, "“abcdefgh”"
        ca.update({
            "rv_hai_chu_so_con_tro": ("a.md", "Theo r12 " + CT0("r12:1 #afdc1a0a|muoi hai co noi dung") + ".\n", None, (1, 0, 0, 0, 0)),
            "dong_hai_chu_so_con_tro": ("a.md", "Theo r3 " + CT0("r3:12 #ab858a93|so 12 co noi dung") + ".\n", None, (1, 0, 0, 0, 0)),
            "span_hai_chu_so": ("a.md", "Theo r3 " + CT0("r3:10-11 #20031634|so 10 co noi dung") + ".\n", None, (1, 0, 0, 0, 0)),
            "dong_hai_chu_so_sai_bam": ("a.md", "Theo r3 " + CT0("r3:12 #00000000|so 12 co noi dung") + ".\n", None, (0, 1, 0, 0, 0)),
            "rv_hai_chu_so_token": ("a.md", "Theo r12: " + Q8 + ".\n", None, (0, 0, 0, 1, 0)),
            "rv_trong_tu_khong_phai_token": ("a.md", "Theo error1 va r1x: " + Q8 + ".\n", None, (0, 0, 0, 0, 0)),
            "trich_7_thang": ("a.md", "Theo r1: " + Q2 + "abcdefg" + Q2 + ".\n", None, (0, 0, 0, 0, 0)),
            "trich_8_thang": ("a.md", "Theo r1: " + Q8 + ".\n", None, (0, 0, 0, 1, 0)),
            "trich_9_thang": ("a.md", "Theo r1: " + Q2 + "abcdefghi" + Q2 + ".\n", None, (0, 0, 0, 1, 0)),
            "trich_7_cong": ("a.md", "Theo r1: “abcdefg”.\n", None, (0, 0, 0, 0, 0)),
            "trich_8_cong": ("a.md", "Theo r1: " + C8 + ".\n", None, (0, 0, 0, 1, 0)),
            "trich_9_cong": ("a.md", "Theo r1: “abcdefghi”.\n", None, (0, 0, 0, 1, 0)),
            "moi_nhan_hop_le": ("a.md", "Theo r1: " + " ".join(Q8 + " " + chr(0x27E6) + "nguon:" + k + chr(0x27E7)
                                for k in ("chi-thi", "verdict", "commit", "ma", "doctrine", "issue")) + ".\n", None, (0, 0, 0, 0, 6)),
            **{f"tieu_de_cap_{n}": ("a.md", "#" * n + " Nhan xet r1\n\nDoan nay viet " + Q8 + ".\n", None, (0, 0, 0, 1, 0)) for n in range(1, 7)},
            "bay_thang_khong_phai_tieu_de": ("a.md", "####### Nhan xet r1\n\nDoan nay viet " + Q8 + ".\n", None, (0, 0, 0, 0, 0)),
            "rao_3_co_thong_tin": ("a.md", "```python\nr1 = " + Q8 + "\n```\n", None, (0, 0, 0, 0, 0)),
            "rao_4_co_thong_tin": ("a.md", "````python\nr1 = " + Q8 + "\n````\n", None, (0, 0, 0, 0, 0)),
            # r14 (#574 luot 9, F2): cap nhan thuong / nhan sau markup; ngoac cong vat dong; `-` o ranh gioi trai token;
            # manh 5 ky tu (am) canh manh 6 ky tu (ca duong cu `manh_6_duong`).
            "nhan_sau_markup": ("a.md", "Theo r1: *" + Q8 + "* " + chr(0x27E6) + "nguon:chi-thi" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
            "nhan_sau_markup_dam": ("a.md", "Theo r1: **" + Q8 + "** " + chr(0x27E6) + "nguon:verdict" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
            "ngoac_cong_vat_dong": ("a.md", "Theo r1: “abcd\nefgh”.\n", None, (0, 0, 0, 1, 0)),
            "rv_sau_gach_noi": ("a.md", "Theo ma-r1: " + Q8 + ".\n", None, (0, 0, 0, 0, 0)),
            "manh_5_am": ("a.md", "Theo r1 " + CT0("r1:1 #2bf318fb|ong m") + ".\n", None, (0, 0, 0, 1, 0)),
        })
        hong = []
        for ten, (tep, doc, ham, mong) in ca.items():
            p = Path(t) / ten / tep; p.parent.mkdir(); p.write_text(doc, encoding="utf-8")
            d = kiem(t, "r{n}.md", p, ham)
            thuc = (d["DUNG"], d["LECH"], d["KHONG_DO_DUOC"], d["VI_PHAM"], d["CO_NHAN"])
            if thuc != mong: hong.append(f"{ten}: mong {mong}, thuc {thuc}")
        # CLI THAT (tien trinh con, qua `main`): khoa lop chuyen tham so, ke ca `--ham` mot/nhieu ten. Ky vong: (rc, TONG).
        import subprocess as _sp
        py_cli = ("def f():\n    " + Q2 * 3 + "Ham f nhac r1 va khong trich gi ca, du dai de qua nguong bon muoi.\n    " + Q2 * 3
                  + "\n\n\ndef g():\n    " + Q2 * 3 + "Ham g nhac r1: " + Q8 + " khong nhan, du dai de qua nguong.\n    " + Q2 * 3 + "\n")
        (Path(t) / "cli").mkdir(); pc = Path(t) / "cli" / "a.py"; pc.write_text(py_cli, encoding="utf-8")
        pm = Path(t) / "cli" / "b.md"; pm.write_text("Theo r3 " + CT0("r3:12 #ab858a93|so 12 co noi dung") + ".\n", encoding="utf-8")
        # r14 (luot 9): MA TRAN hop dong CLI — moi bo dem loi RIENG qua `main` phai cho rc=1; `--ham` nhieu ten voi loi o
        # DAU, CUOI, GIUA. p3: a xau, b sach, c xau.
        p3 = Path(t) / "cli" / "c.py"
        p3.write_text("".join(f"def {n}():\n    " + Q2 * 3 + f"Ham {n} nhac r1 " + (Q8 + " khong nhan" if xau else "va khong trich gi")
                              + ", du dai de qua nguong bon muoi.\n    " + Q2 * 3 + "\n\n\n" for n, xau in (("a", 1), ("b", 0), ("c", 1))), encoding="utf-8")
        def md(ten, noi):
            q = Path(t) / "cli" / ten; q.write_text(noi, encoding="utf-8"); return str(q)
        cli = {"cli_ham_f": (["--ham", "f", str(pc)], 0, (0, 0, 0, 0, 0)), "cli_ham_f_g": (["--ham", "f,g", str(pc)], 1, (0, 0, 0, 1, 0)),
               "cli_khong_ham": ([str(pc)], 1, (0, 0, 0, 1, 0)), "cli_con_tro_hai_chu_so": ([str(pm)], 0, (1, 0, 0, 0, 0)),
               "cli_chi_LECH": ([md("l.md", "Theo r3 " + CT0("r3:12 #00000000|so 12 co noi dung") + ".\n")], 1, (0, 1, 0, 0, 0)),
               "cli_chi_KHONG_DO_DUOC": ([md("k.md", "Theo r9 " + CT0("r9:1 #00000000|khong co tep") + ".\n")], 1, (0, 0, 1, 0, 0)),
               "cli_chi_VI_PHAM": ([md("v.md", "Theo r1: " + Q8 + ".\n")], 1, (0, 0, 0, 1, 0)),
               "cli_sach": ([md("s.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|hai co noi dung") + ".\n")], 0, (1, 0, 0, 0, 0)),
               "cli_ham_loi_dau": (["--ham", "a,b", str(p3)], 1, (0, 0, 0, 1, 0)),
               "cli_ham_loi_cuoi": (["--ham", "b,c", str(p3)], 1, (0, 0, 0, 1, 0)),
               "cli_ham_hai_loi": (["--ham", "a,b,c", str(p3)], 1, (0, 0, 0, 2, 0)),
               "cli_ham_sach_giua": (["--ham", "b", str(p3)], 0, (0, 0, 0, 0, 0))}
        for ten, (doi, rc_mong, mong) in cli.items():
            r = _sp.run([sys.executable, "-B", str(Path(__file__).resolve()), "kiem", "--nguon", t, "--mau", "r{n}.md", *doi],
                        capture_output=True, text=True)
            tong = [x for x in r.stdout.splitlines() if x.startswith("TONG ")]
            d = ast.literal_eval(tong[-1][5:]) if tong else {}
            thuc = (r.returncode, tuple(d.get(k) for k in ("DUNG", "LECH", "KHONG_DO_DUOC", "VI_PHAM", "CO_NHAN")))
            if thuc != (rc_mong, mong): hong.append(f"{ten}: mong {(rc_mong, mong)}, thuc {thuc}")
        n_ca = len(ca) + len(cli)
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{n_ca - len(hong)}/{n_ca}")
        return 0 if not hong else 1
def main(a):
    if a[:1] == ["tu-kiem"]: return tu_kiem()
    cmd, co, rest, i = a[0], {}, [], 1
    while i < len(a):
        if a[i] in ("--nguon", "--mau", "--ham"): co[a[i]] = a[i + 1]; i += 2
        else: rest.append(a[i]); i += 1
    dir_, mau = co["--nguon"], co["--mau"]
    ham = set(co["--ham"].split(",")) if "--ham" in co else None
    if cmd == "sinh":
        n = int(rest[0].lstrip("r")); ab = rest[1].split("-"); print(sinh(dir_, mau, n, int(ab[0]), int(ab[-1]), rest[2] if len(rest) > 2 else None)); return 0
    if cmd == "tim":
        cum = re.sub(r"\s+", " ", rest[0]).strip(); n = 1
        while True:
            L = nguon(dir_, mau, n)
            if L is None: break
            for k, l in enumerate(L, 1):
                if cum in re.sub(r"\s+", " ", l): print(f"r{n}:{k} {sinh(dir_, mau, n, k, manh=cum) if len(bo_dau(cum)) >= 6 and bo_dau(cum) in bo_dau(l) else '(cum co dau markdown)'} {l.strip()[:100]}")
            n += 1
        return 0
    if cmd == "kiem":
        tong = {}
        for tep in rest:
            for k, v in kiem(dir_, mau, tep, ham).items(): tong[k] = tong.get(k, 0) + v
        print("TONG", tong); return 0 if tong["LECH"] == tong["VI_PHAM"] == tong["KHONG_DO_DUOC"] == 0 else 1
    raise SystemExit("lenh la: sinh | tim | kiem | tu-kiem")
if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
```
